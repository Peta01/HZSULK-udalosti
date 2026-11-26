/**
 * HZSULK Events card – mapa zásahů s propojeným seznamem.
 *
 * type: custom:hzsulk-events-card
 * title: Zásahy hasičů        # volitelné
 * map_height: 400              # výška mapy v px
 * list_height: 400             # max. výška seznamu v px (0 = bez omezení)
 * show_home: true              # značka zóny Domov
 */

const CARD_VERSION = "2.2.0";
const SOURCE = "hzsulk_events";
const BASE = new URL(".", import.meta.url).pathname;
const TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";
const ATTRIBUTION =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> · data HZS ÚK';

let leafletPromise;
const loadLeaflet = () => (leafletPromise ??= import(`${BASE}leaflet/leaflet-src.esm.js`));

const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch]
  );

class HzsulkEventsCard extends HTMLElement {
  constructor() {
    super();
    this._config = {};
    this._events = [];
    this._signature = "";
    this._selected = null;
    this._markers = new Map();
    this._fitted = false;
    this.attachShadow({ mode: "open" });
  }

  static getStubConfig() {
    return { title: "Zásahy hasičů" };
  }

  setConfig(config) {
    this._config = {
      map_height: 400,
      list_height: 400,
      show_home: true,
      ...config,
    };
    this._built = false;
    this._build();
  }

  set hass(hass) {
    this._hass = hass;
    const dark = Boolean(hass.themes?.darkMode);
    if (dark !== this._dark) {
      this._dark = dark;
      this._setTiles();
    }
    const events = Object.values(hass.states)
      .filter(
        (s) =>
          s.entity_id.startsWith("geo_location.") &&
          s.attributes.source === SOURCE &&
          typeof s.attributes.latitude === "number"
      )
      .sort((a, b) => String(b.attributes.reported).localeCompare(String(a.attributes.reported)));
    const signature = events.map((s) => `${s.entity_id}@${s.last_updated}`).join("|");
    if (signature === this._signature) return;
    this._signature = signature;
    this._events = events;
    if (this._selected && !events.some((s) => s.entity_id === this._selected)) {
      this._selected = null;
    }
    this._renderList();
    this._renderMarkers();
  }

  getCardSize() {
    return 10;
  }

  getGridOptions() {
    return { columns: "full", min_columns: 6, min_rows: 6 };
  }

  connectedCallback() {
    this._build();
    if (this._map) setTimeout(() => this._map.invalidateSize(), 0);
  }

  disconnectedCallback() {
    this._resizeObserver?.disconnect();
    this._resizeObserver = undefined;
  }

  // ---------- DOM ----------

  _build() {
    if (this._built || !this._config) return;
    this._built = true;
    const { title, map_height, list_height } = this._config;
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="${BASE}leaflet/leaflet.css">
      <style>
        :host { display: block; }
        ha-card { overflow: hidden; }
        .title { padding: 12px 16px 8px; font-size: 1.2em; font-weight: 500; }
        #map { height: ${Number(map_height) || 400}px; background: var(--secondary-background-color); z-index: 0; }
        .list { overflow-y: auto; ${Number(list_height) ? `max-height: ${Number(list_height)}px;` : ""} }
        .empty { padding: 16px; color: var(--secondary-text-color); }
        .item {
          display: flex; gap: 12px; padding: 10px 16px; cursor: pointer;
          border-top: 1px solid var(--divider-color);
          border-left: 4px solid transparent;
          transition: background-color .2s;
        }
        .item:hover { background: var(--secondary-background-color); }
        .item.selected {
          background: rgba(var(--rgb-primary-color, 3, 169, 244), .14);
          border-left-color: var(--primary-color);
        }
        .badge {
          flex: none; width: 32px; height: 32px; border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          background: var(--disabled-color, #9e9e9e); color: #fff; --mdc-icon-size: 18px;
        }
        .active .badge { background: var(--error-color, #db4437); }
        .body { flex: 1; min-width: 0; }
        .name { font-weight: 500; }
        .meta { color: var(--secondary-text-color); font-size: .9em; margin-top: 2px; }
        .live { color: var(--error-color, #db4437); font-weight: 500; }
        .desc { font-style: italic; margin-top: 4px; }
        .vehicles { margin: 4px 0 0; padding: 0; list-style: none; font-size: .9em; }
        .vehicles li::before { content: "🚒 "; }
        .info {
          flex: none; align-self: flex-start; background: none; border: 0; padding: 4px;
          color: var(--secondary-text-color); cursor: pointer; border-radius: 50%;
        }
        .info:hover { color: var(--primary-color); }
        /* značky na mapě */
        .hz-marker {
          width: 26px; height: 26px; border-radius: 50%; box-sizing: border-box;
          display: flex; align-items: center; justify-content: center;
          background: #757575; color: #fff; border: 2px solid #fff;
          box-shadow: 0 1px 4px rgba(0,0,0,.45); --mdc-icon-size: 15px;
          transition: transform .15s;
        }
        .hz-marker.active { background: #d32f2f; }
        .hz-marker.selected {
          transform: scale(1.45); border-color: var(--primary-color, #03a9f4);
          box-shadow: 0 0 0 3px rgba(3,169,244,.45), 0 1px 6px rgba(0,0,0,.5);
        }
        .hz-home { background: var(--primary-color, #03a9f4); }
        .fit {
          background: var(--card-background-color, #fff); color: var(--primary-text-color);
          width: 30px; height: 30px; border: 0; cursor: pointer; --mdc-icon-size: 18px;
          display: flex; align-items: center; justify-content: center;
        }
        .leaflet-container { font: inherit; }
        #map.dark .leaflet-tile-pane {
          filter: invert(1) hue-rotate(180deg) brightness(.9) contrast(.9) saturate(.6);
        }
        #map.dark .leaflet-control-attribution { background: rgba(0,0,0,.6); color: #ccc; }
        #map.dark .leaflet-bar a, #map.dark .fit { background: #2b2b2b; color: #e1e1e1; border-color: #444; }
      </style>
      <ha-card>
        ${title ? `<div class="title">${esc(title)}</div>` : ""}
        <div id="map"></div>
        <div class="list"></div>
      </ha-card>`;
    this._list = this.shadowRoot.querySelector(".list");
    this._list.addEventListener("click", (ev) => this._onListClick(ev));
    this._map = undefined;
    this._markers.clear();
    this._fitted = false;
    this._initMap();
    this._renderList();
  }

  async _initMap() {
    const L = await loadLeaflet();
    this._L = L;
    const container = this.shadowRoot.getElementById("map");
    if (!container || this._map) return;
    this._map = L.map(container, { zoomControl: true, attributionControl: true }).setView(
      [50.6, 13.9],
      9
    );
    this._map.attributionControl.setPrefix(false);
    this._layer = L.layerGroup().addTo(this._map);

    const FitControl = L.Control.extend({
      onAdd: () => {
        const btn = L.DomUtil.create("button", "fit leaflet-bar");
        btn.title = "Zobrazit vše";
        btn.innerHTML = '<ha-icon icon="mdi:fit-to-screen-outline"></ha-icon>';
        L.DomEvent.disableClickPropagation(btn);
        L.DomEvent.on(btn, "click", () => this._fitAll());
        return btn;
      },
    });
    new FitControl({ position: "topright" }).addTo(this._map);
    this._map.on("click", () => this._select(null));

    this._resizeObserver = new ResizeObserver(() => this._map?.invalidateSize());
    this._resizeObserver.observe(container);
    this._setTiles();
    this._renderMarkers();
  }

  _setTiles() {
    const container = this.shadowRoot.getElementById("map");
    container?.classList.toggle("dark", Boolean(this._dark));
    if (!this._map || !this._L || this._tiles) return;
    this._tiles = this._L
      .tileLayer(TILE_URL, { attribution: ATTRIBUTION, maxZoom: 19 })
      .addTo(this._map);
  }

  // ---------- mapa ----------

  _markerIcon(stateObj, selected) {
    const active = stateObj.attributes.active ? " active" : "";
    const sel = selected ? " selected" : "";
    return this._L.divIcon({
      className: "",
      html: `<div class="hz-marker${active}${sel}"><ha-icon icon="${esc(
        stateObj.attributes.icon || "mdi:fire-truck"
      )}"></ha-icon></div>`,
      iconSize: [26, 26],
      iconAnchor: [13, 13],
    });
  }

  _renderMarkers() {
    if (!this._map || !this._L) return;
    const L = this._L;
    this._layer.clearLayers();
    this._markers.clear();

    const home = this._hass?.states["zone.home"];
    if (this._config.show_home && home?.attributes.latitude != null) {
      this._homeLatLng = [home.attributes.latitude, home.attributes.longitude];
      L.marker(this._homeLatLng, {
        icon: L.divIcon({
          className: "",
          html: '<div class="hz-marker hz-home"><ha-icon icon="mdi:home"></ha-icon></div>',
          iconSize: [26, 26],
          iconAnchor: [13, 13],
        }),
        interactive: false,
        keyboard: false,
      }).addTo(this._layer);
    }

    // starší dole, novější a probíhající nahoře
    [...this._events].reverse().forEach((s, index) => {
      const selected = s.entity_id === this._selected;
      const marker = L.marker([s.attributes.latitude, s.attributes.longitude], {
        icon: this._markerIcon(s, selected),
        title: s.attributes.friendly_name,
        zIndexOffset: selected ? 10000 : (s.attributes.active ? 5000 : 0) + index,
      });
      marker.on("click", (ev) => {
        L.DomEvent.stopPropagation(ev);
        this._select(s.entity_id, "map");
      });
      marker.addTo(this._layer);
      this._markers.set(s.entity_id, marker);
    });

    if (!this._fitted && this._events.length) {
      this._fitted = true;
      this._fitAll();
    }
  }

  _fitAll() {
    if (!this._map || !this._L) return;
    const points = this._events.map((s) => [s.attributes.latitude, s.attributes.longitude]);
    if (this._homeLatLng) points.push(this._homeLatLng);
    if (!points.length) return;
    if (points.length === 1) {
      this._map.setView(points[0], 13);
    } else {
      this._map.fitBounds(this._L.latLngBounds(points), { padding: [24, 24], maxZoom: 14 });
    }
  }

  // ---------- výběr ----------

  _select(entityId, origin) {
    if (entityId === this._selected && origin !== "list") return;
    const previous = this._selected;
    this._selected = entityId;

    for (const id of [previous, entityId]) {
      if (!id) continue;
      const marker = this._markers.get(id);
      const stateObj = this._events.find((s) => s.entity_id === id);
      if (marker && stateObj) {
        marker.setIcon(this._markerIcon(stateObj, id === entityId));
        marker.setZIndexOffset(id === entityId ? 10000 : stateObj.attributes.active ? 5000 : 0);
      }
    }

    this._list.querySelectorAll(".item").forEach((el) => {
      el.classList.toggle("selected", el.dataset.id === entityId);
    });

    if (!entityId) return;
    if (origin === "map") {
      const item = this._list.querySelector(`.item[data-id="${CSS.escape(entityId)}"]`);
      if (item) {
        // posunout jen seznam, ne celou stránku
        const top = item.offsetTop - this._list.offsetTop;
        if (this._list.scrollHeight > this._list.clientHeight) {
          this._list.scrollTo({ top: top - 8, behavior: "smooth" });
        } else {
          item.scrollIntoView({ block: "nearest", behavior: "smooth" });
        }
      }
    } else if (origin === "list") {
      const marker = this._markers.get(entityId);
      if (marker && this._map) {
        this._map.setView(marker.getLatLng(), Math.max(this._map.getZoom(), 12), {
          animate: true,
        });
      }
    }
  }

  _onListClick(ev) {
    const info = ev.target.closest(".info");
    const item = ev.target.closest(".item");
    if (!item) return;
    if (info) {
      this.dispatchEvent(
        new CustomEvent("hass-more-info", {
          detail: { entityId: item.dataset.id },
          bubbles: true,
          composed: true,
        })
      );
      return;
    }
    this._select(item.dataset.id, "list");
  }

  // ---------- seznam ----------

  _formatTime(iso) {
    if (!iso) return "";
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleString(this._hass?.locale?.language || "cs", {
      day: "numeric",
      month: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  _renderList() {
    if (!this._list) return;
    if (!this._events.length) {
      this._list.innerHTML = `<div class="empty">Žádné události.</div>`;
      return;
    }
    const lang = this._hass?.locale?.language || "cs";
    this._list.innerHTML = this._events
      .map((s) => {
        const a = s.attributes;
        const distance = Number(s.state);
        const meta = [
          this._formatTime(a.reported),
          a.active ? `<span class="live">${esc(a.status || "probíhá")}</span>` : esc(a.status),
          Number.isFinite(distance)
            ? `${distance.toLocaleString(lang, { maximumFractionDigits: 1 })} km`
            : "",
        ]
          .filter(Boolean)
          .join(" · ");
        const vehicles = (a.vehicles || []).map((v) => `<li>${esc(v)}</li>`).join("");
        return `
          <div class="item${a.active ? " active" : ""}${
            s.entity_id === this._selected ? " selected" : ""
          }" data-id="${esc(s.entity_id)}">
            <div class="badge"><ha-icon icon="${esc(a.icon || "mdi:fire-truck")}"></ha-icon></div>
            <div class="body">
              <div class="name">${esc(a.friendly_name)}</div>
              <div class="meta">${meta}</div>
              ${a.description ? `<div class="desc">${esc(a.description)}</div>` : ""}
              ${vehicles ? `<ul class="vehicles">${vehicles}</ul>` : ""}
            </div>
            <button class="info" title="Podrobnosti"><ha-icon icon="mdi:information-outline"></ha-icon></button>
          </div>`;
      })
      .join("");
  }
}

if (!customElements.get("hzsulk-events-card")) {
  customElements.define("hzsulk-events-card", HzsulkEventsCard);
  window.customCards = window.customCards || [];
  window.customCards.push({
    type: "hzsulk-events-card",
    name: "Zásahy HZS ÚK",
    description: "Mapa zásahů hasičů s propojeným seznamem a podrobnostmi.",
    preview: false,
    documentationURL: "https://github.com/Peta01/HZSULK-udalosti",
  });
  console.info(`%c HZSULK-EVENTS-CARD %c ${CARD_VERSION} `, "background:#d32f2f;color:#fff", "");
}
