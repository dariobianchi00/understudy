#!/usr/bin/env python3
"""Serve the fixture site on localhost for a real-browser capture.

    python3 serve.py [port]        default 8765

Generates assets/generated/hero.png — ~3.9 MB of incompressible pixels — on
first start, so the planted oversized-image defect is real over the wire. That
file is gitignored (*.png); only this generator is committed.
"""
import http.server, os, random, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


def heavy_png(path, w=3000, h=2000):
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rnd = random.Random(7)
    raw = b"".join(b"\x00" + bytes(rnd.getrandbits(8) for _ in range(w * 3)) for _ in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 0)) + chunk(b"IEND", b""))
    open(path, "wb").write(png)


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)

    def do_POST(self):
        # the app's save endpoint — planted 500
        self.send_response(500); self.end_headers(); self.wfile.write(b"internal error")

    def send_error(self, code, *a, **k):
        if code == 404 and os.path.exists(os.path.join(HERE, "404.html")):
            self.send_response(404); self.send_header("Content-Type", "text/html"); self.end_headers()
            self.wfile.write(open(os.path.join(HERE, "404.html"), "rb").read()); return
        super().send_error(code, *a, **k)


if __name__ == "__main__":
    heavy_png(os.path.join(HERE, "assets", "generated", "hero.png"))
    print(f"http://localhost:{PORT}/  (Ctrl-C to stop)")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
