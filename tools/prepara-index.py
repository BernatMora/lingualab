#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prepara-index.py — deixa un index.html de LinguaLab a punt per publicar-lo.

L'app es desenvolupa com un fitxer solt (LinguaLab_English_2026_*.html). Per publicar-la cal
afegir-hi el que fa que sigui instal·lable i que es vegi bé quan es comparteix:

  · manifest.webmanifest, icones (favicon + apple-touch-icon) i meta d'app d'iOS/Android,
  · meta description i Open Graph (per quan s'enganxa l'enllaç),
  · el registre del service worker (funcionar sense connexió).

És idempotent: si el bloc ja hi és, no el duplica.

    python3 tools/prepara-index.py entrada.html sortida.html
    python3 tools/prepara-index.py index.html            # ho fa al mateix fitxer
"""

import io
import re
import sys

CAP = """<meta name="description" content="LinguaLab: textos bilingües anglès/castellà (B2–C1) amb lectura, traducció, vocabulari clau, flashcards, quiz, veu i progrés desat al navegador.">
<meta property="og:title" content="LinguaLab · Anglès B2–C1">
<meta property="og:description" content="Biblioteca de textos bilingües per practicar anglès: llegir, escoltar, vocabulari i quiz.">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="LinguaLab">"""

SW = """<script>
if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
  addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
</script>"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    entrada = sys.argv[1]
    sortida = sys.argv[2] if len(sys.argv) > 2 else entrada

    with io.open(entrada, encoding="utf-8") as f:
        t = f.read()

    canvis = []

    # 1) Capçalera PWA/SEO, just després del theme-color
    if "manifest.webmanifest" not in t:
        m = re.search(r'(<meta name="theme-color"[^>]*>)', t)
        if not m:
            sys.exit("ERROR: no trobo <meta name=\"theme-color\"> on enganxar la capçalera")
        t = t[:m.end()] + "\n" + CAP + t[m.end():]
        canvis.append("capçalera PWA/SEO")

    # 2) Registre del service worker, abans de </body>
    if "serviceWorker" not in t:
        if t.count("</body>") != 1:
            sys.exit("ERROR: no trobo un únic </body>")
        t = t.replace("</body>", SW + "\n</body>", 1)
        canvis.append("registre del service worker")

    with io.open(sortida, "w", encoding="utf-8") as f:
        f.write(t)

    # 3) Comprovació bàsica d'estructura
    problemes = []
    parelles = ((r"<html[\s>]", "</html>"), (r"<head[\s>]", "</head>"), (r"<body[\s>]", "</body>"))
    for obert, tancat in parelles:
        if len(re.findall(obert, t)) != t.count(tancat):
            problemes.append(f"{obert}/{tancat}")
    if problemes:
        print("⚠️  etiquetes descompensades:", ", ".join(problemes))

    print(f"{sortida}: " + (", ".join(canvis) if canvis else "ja estava a punt") +
          f" ({len(t)} octets)")


if __name__ == "__main__":
    main()
