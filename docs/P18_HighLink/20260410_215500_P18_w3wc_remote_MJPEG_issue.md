# P18.w3wc -> MacBook Handover: MJPEG Remote Embedding Issue

## Current Status

MJPEG architecture improved on company PC, but **embedding MJPEG video inside Streamlit page does NOT work remotely**.

- **Local (company PC)**: All methods work
- **Remote (MacBook Safari/Chrome)**: Streamlit UI + FPS info shows, but **video area is black/empty**
- **MJPEG viewer direct access**: `https://xxx.trycloudflare.com/viewer` in browser -> **WORKS PERFECTLY**

## Root Cause

Streamlit (port 8501) and MJPEG (port 8502) use **different Cloudflare Quick Tunnel domains**.
Browser blocks cross-origin resource loading inside Streamlit's page.

```
Streamlit: https://aaa.trycloudflare.com (port 8501)
MJPEG:     https://bbb.trycloudflare.com (port 8502)
-> Different domains -> iframe/img cross-origin blocked
```

## Attempted Methods (ALL failed remotely)

| # | Method | Result |
|---|--------|--------|
| 1 | st.components.v1.html() + JS polling | srcdoc iframe origin=null, cross-origin blocked |
| 2 | st.markdown() + img src | Broken image icon |
| 3 | st.components.v1.iframe(viewer_url) | Empty/invisible |
| 4 | st.markdown() + iframe sandbox="allow-scripts allow-same-origin" | Still empty |

## What Was Fixed

### ThreadingMixIn (CRITICAL bug fix)
- HTTPServer was single-threaded -> /stream long connection blocked ALL other requests
- Applied ThreadingMixIn for concurrent request handling
- File: app/streamlit/stream_server.py

### New Endpoints
- /viewer: MJPEG viewer HTML page (img src="/stream"), for direct browser access
- /snapshot: Single JPEG frame, for JS polling

### MJPEG URL Automation
- Tunnel URL saved to /tmp/mjpeg_tunnel_url.txt on tunnel start
- app.py auto-reads this file (manual input UI removed)
- Auto start(port=8502) on module import

## Solutions to Try on MacBook (priority order)

### Solution 1: Single Port Integration (MOST PROMISING)
Serve MJPEG through Streamlit's Tornado server on same port 8501.
Same tunnel domain -> no cross-origin.

Add custom Tornado handler to Streamlit server for /mjpeg/stream, /mjpeg/snapshot.

### Solution 2: Server-side Proxy
Streamlit app fetches from localhost:8502/snapshot server-side, displays via st.image().
No browser cross-origin. But WebSocket overhead (original reason for MJPEG switch).
Compromise: limit to ~5 FPS for remote.

### Solution 3: Viewer Popup
Give up embedding. Provide window.open(viewer_url) button in Streamlit.
User views video in separate tab/window.

### Solution 4: Nginx Reverse Proxy
Nginx merges 8501+8502 into single port:
/ -> localhost:8501 (Streamlit)
/mjpeg/ -> localhost:8502 (MJPEG)
Single tunnel. Requires Nginx on company PC.

## Current Code State (main branch, commit 1b9f964)

app/streamlit/app.py - st.markdown iframe (not working remotely)
app/streamlit/stream_server.py - ThreadingMixIn + /viewer + /snapshot + auto-start
