#!/usr/bin/env python3
"""
Launcher script for RUSTOM-II MALE UAV Digital Twin Simulator & C2 Server.
Hosts FastAPI REST APIs, WebSocket 20Hz Telemetry, and the compiled WebGL Simulation on port 3000.
"""

import os
import sys
import socket
import subprocess
import webbrowser
import http.server
import socketserver
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = int(os.environ.get("PORT", 3000))
BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "dist"

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class DroneSimHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        super().end_headers()

    def do_GET(self):
        req_path = self.translate_path(self.path)
        if not os.path.exists(req_path) and not req_path.endswith((".js", ".css", ".png", ".jpg", ".svg", ".json", ".woff", ".woff2")):
            self.path = "/index.html"
        return super().do_GET()

    def guess_type(self, path):
        if str(path).endswith((".js", ".mjs")):
            return "text/javascript"
        if str(path).endswith(".css"):
            return "text/css"
        if str(path).endswith(".svg"):
            return "image/svg+xml"
        if str(path).endswith(".json"):
            return "application/json"
        if str(path).endswith(".wasm"):
            return "application/wasm"
        return super().guess_type(path)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def main():
    if not DIST_DIR.exists() or not (DIST_DIR / "index.html").exists():
        print(f"[!] Production build not found in {DIST_DIR}. Building now with npm...")
        ret = os.system("npm run build")
        if ret != 0:
            print("[ERROR] npm run build failed. Please run 'npm install' and 'npm run build'.")
            sys.exit(1)

    lan_ip = get_lan_ip()
    local_url = f"http://localhost:{PORT}"
    lan_url = f"http://{lan_ip}:{PORT}"
    mobile_url = f"http://{lan_ip}:{PORT}/?mode=remote"
    docs_url = f"http://localhost:{PORT}/docs"
    ws_url = f"ws://localhost:{PORT}/ws/telemetry"

    # Optional integrated Cloudflare live tunnel
    tunnel_proc = None
    if "--tunnel" in sys.argv or "--live" in sys.argv or os.environ.get("TUNNEL") == "1":
        print("[+] Launching Cloudflare public tunnel in background...")
        try:
            tunnel_proc = subprocess.Popen(["node", str(BASE_DIR / "tunnel.mjs")], cwd=str(BASE_DIR))
        except Exception as e:
            print(f"[!] Could not start tunnel: {e}")

    print("=" * 70)
    print("  MALE UAV DIGITAL TWIN FLIGHT SIMULATION & HEALTH MONITORING C2")
    print("=" * 70)
    print(f"  [+] Local C2 Dashboard:   {local_url}")
    print(f"  [+] LAN / Wi-Fi Network:   {lan_url}")
    print(f"  [+] MOBILE RC CONTROLLER: {mobile_url}")
    print(f"  [+] OpenAPI Swagger Docs:  {docs_url}")
    print(f"  [+] WebSocket Telemetry:   {ws_url}")
    print(f"  [+] Serving Client From:   {DIST_DIR}")
    print("=" * 70)
    print("  * Open the MOBILE RC CONTROLLER link on any phone or tablet!")
    print("  * Dual-stick joystick controls flight on this screen with <15ms latency.")
    print("  * Press Ctrl+C to stop the server.")
    print("=" * 70)

    # Automatically open browser
    try:
        webbrowser.open(local_url)
    except Exception:
        pass

    # Attempt to start with FastAPI + Uvicorn
    try:
        import uvicorn
        from backend.app.main import app
        uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
    except ImportError:
        print("[!] Uvicorn/FastAPI not found in current environment. Falling back to multithreaded static server.")
        with ThreadedTCPServer(("0.0.0.0", PORT), DroneSimHTTPHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user.")
    except OSError as e:
        if e.errno == 10048 or "Address already in use" in str(e):
            print(f"[!] Port {PORT} is already in use. Please check running tasks or select another port.")
        else:
            raise
    finally:
        if tunnel_proc:
            try:
                tunnel_proc.terminate()
            except Exception:
                pass

if __name__ == "__main__":
    main()
