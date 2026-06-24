---
title: Discover HZSULK API
description: Analyze the udalosti.hzsulk.cz website to find the API endpoint and data structure for events
---

# Discover HZSULK API

## Goal
Reverse engineer the https://udalosti.hzsulk.cz/ website to find:
1. Exact API endpoint used to fetch events
2. Request/Response structure
3. Authentication requirements
4. Rate limiting/update frequency

## Methods

### Method 1: Network Analysis (Preferred)
1. Open DevTools in browser (F12)
2. Go to Network tab
3. Reload the page
4. Look for XHR/Fetch requests containing:
   - API endpoint (likely `/api/getapi`, `/api/events`, `/api/udalosti`, etc.)
   - Request: query params, headers, auth
   - Response: JSON structure with event fields

### Method 2: Static Analysis
1. View page source (Ctrl+U)
2. Search for:
   - `.fetch(`, `.ajax(`, `axios.get(` - API calls
   - `api`, `endpoint`, `getapi` - URL patterns
   - API key patterns in headers/localStorage

### Method 3: Browser Console
Execute in DevTools Console:
```javascript
// Check for API URLs in window/global objects
console.log(window.__INITIAL_STATE__);
console.log(window.__API_CONFIG__);

// Monitor fetch calls
const originalFetch = window.fetch;
window.fetch = function(...args) {
  console.log('FETCH:', args[0]);
  return originalFetch.apply(this, args);
};
```

## Expected Output

Document the following:

```
### API Endpoint
- URL: [exact endpoint]
- Method: GET/POST
- Base URL: https://udalosti.hzsulk.cz/api/...

### Request Structure
- Query params: [list]
- Headers: [important headers]
- Body: [if POST]
- Auth: [token, API key, or none]

### Response Structure
Example response with field names and types:
```json
{
  "events": [
    {
      "id": "string",
      "timestamp": "datetime",
      "status": "string",
      "type": "string",
      "type_detail": "string",
      "region": "string",
      "district": "string",
      "city": "string",
      "place": "string",
      "street": "string",
      "description": "string",
      "count": "number"
    }
  ],
  "total": "number",
  "updated_at": "datetime"
}
```

### Update Frequency
- Polling interval: [e.g. 60 seconds]
- Real-time: [yes/no, WebSocket?]
- Cache headers: [if any]

### Limitations
- Rate limit: [if any]
- CORS: [enabled/disabled]
- Authentication required: [yes/no]
```

## Success Criteria
- ✅ Exact API endpoint documented
- ✅ Request/Response examples captured
- ✅ Data fields mapped to event properties
- ✅ Update mechanism understood
- ✅ Ready for HA integration development
