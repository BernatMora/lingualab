#!/usr/bin/env python3
"""Servidor estàtic de LinguaLab per a la Raspberry Pi (BernatLab).

Patró de la secció 3b del RUNBOOK de la RPi: carpeta d'estàtics + servidor Python + pm2.

    pm2 start lingualab-server.py --name lingualab
    pm2 save
"""

import http.server
import socketserver

PORT = 3054
DIRECTORY = "/home/bernat/lingualab"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
            return
        return super().do_GET()

    def end_headers(self):
        # El manifest ha de sortir amb un tipus correcte perquè la PWA s'instal·li.
        if self.path.endswith(".webmanifest"):
            self.send_header("Content-Type", "application/manifest+json")
        super().end_headers()


with ReusableTCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"LinguaLab servit a http://0.0.0.0:{PORT}/ des de {DIRECTORY}", flush=True)
    httpd.serve_forever()
