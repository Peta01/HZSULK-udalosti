"""Převod souřadnic S-JTSK (Křovák) na WGS84."""

from __future__ import annotations

from math import atan, cos, exp, log, pi, sin, sqrt


def jtsk_to_wgs84(x: float, y: float, height: float = 300.0) -> tuple[float, float]:
    """Převeď S-JTSK (X = sever-jih, Y = západ-východ, kladné) na (lat, lon) WGS84.

    Přepis známého algoritmu (Křovákovo zobrazení → Bessel → Helmertova
    transformace → WGS84). Přesnost je v řádu metrů, což pro mapu stačí.
    """
    # Křovákovo zobrazení → zeměpisné souřadnice na Besselově elipsoidu
    e = 0.081696831215303
    n = 0.97992470462083
    konst_u_ro = 12310230.12797036
    sin_uq = 0.863499969506341
    cos_uq = 0.504348889819882
    sin_vq = 0.420215144586493
    cos_vq = 0.907424504992097
    alfa = 1.000597498371542
    k = 1.003419163966575

    ro = sqrt(x * x + y * y)
    epsilon = 2 * atan(y / (ro + x))
    d = epsilon / n
    s = 2 * atan(exp(1 / n * log(konst_u_ro / ro))) - pi / 2
    sin_s, cos_s = sin(s), cos(s)
    sin_d, cos_d = sin(d), cos(d)
    sin_u = sin_uq * sin_s - cos_uq * cos_s * cos_d
    cos_u = sqrt(1 - sin_u * sin_u)
    sin_dv = sin_d * cos_s / cos_u
    cos_dv = sqrt(1 - sin_dv * sin_dv)
    sin_v = sin_vq * cos_dv - cos_vq * sin_dv
    cos_v = cos_vq * cos_dv + sin_vq * sin_dv
    lon_b = 2 * atan(sin_v / (1 + cos_v)) / alfa
    t = exp(2 / alfa * log((1 + sin_u) / cos_u / k))
    pom = (t - 1) / (t + 1)
    for _ in range(50):
        sin_b = pom
        pom = t * exp(e * log((1 + e * sin_b) / (1 - e * sin_b)))
        pom = (pom - 1) / (pom + 1)
        if abs(pom - sin_b) < 1e-15:
            break
    lat_b = atan(pom / sqrt(1 - pom * pom))

    # Bessel → pravoúhlé geocentrické souřadnice
    a = 6377397.15508
    f_1 = 299.152812853
    e2 = 1 - (1 - 1 / f_1) ** 2
    rn = a / sqrt(1 - e2 * sin(lat_b) ** 2)
    gx = (rn + height) * cos(lat_b) * cos(lon_b)
    gy = (rn + height) * cos(lat_b) * sin(lon_b)
    gz = ((1 - e2) * rn + height) * sin(lat_b)

    # Helmertova transformace S-JTSK → WGS84
    dx, dy, dz = 570.69, 85.69, 462.84
    sec = pi / 180 / 3600
    wz = -5.2611 * sec
    wy = -1.58676 * sec
    wx = -4.99821 * sec
    m = 3.543e-6
    xn = dx + (1 + m) * (gx + wz * gy - wy * gz)
    yn = dy + (1 + m) * (-wz * gx + gy + wx * gz)
    zn = dz + (1 + m) * (wy * gx - wx * gy + gz)

    # Geocentrické → zeměpisné na WGS84
    a = 6378137.0
    f_1 = 298.257223563
    a_b = f_1 / (f_1 - 1)
    p = sqrt(xn * xn + yn * yn)
    e2 = 1 - (1 - 1 / f_1) ** 2
    theta = atan(zn * a_b / p)
    st, ct = sin(theta), cos(theta)
    t = (zn + e2 * a_b * a * st**3) / (p - e2 * a * ct**3)
    lat = atan(t)
    lon = 2 * atan(yn / (p + xn))

    return lat * 180 / pi, lon * 180 / pi


def parse_jtsk(gis1: str | None, gis2: str | None) -> tuple[float, float] | None:
    """Z polí API gis1 (Y) a gis2 (X) vrať (lat, lon), nebo None."""
    try:
        y = abs(float(gis1))  # type: ignore[arg-type]
        x = abs(float(gis2))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if not (400_000 < y < 950_000 and 900_000 < x < 1_300_000):
        return None
    try:
        return jtsk_to_wgs84(x, y)
    except (ValueError, ZeroDivisionError):
        return None
