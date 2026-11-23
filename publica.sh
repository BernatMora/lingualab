#!/bin/bash
# Publica LinguaLab a la Raspberry Pi (BernatLab, port 3054).
#
#   ./publica.sh              # copia i reinicia el servei
#   ./publica.sh --git        # a més, fa commit i push a GitHub (Pages es refresca sol)
#
# Requereix l'alies SSH `hortosona` (vegeu ~/.ssh/config).
set -euo pipefail
cd "$(dirname "$0")"

FITXERS=(index.html manifest.webmanifest sw.js icons/)
REMOT="hortosona"
DESTI="~/lingualab/"

echo "== RPi: assegurant la carpeta"
ssh -o BatchMode=yes "$REMOT" 'mkdir -p ~/lingualab/icons'

echo "== RPi: copiant"
rsync -az --delete --exclude 'server.py' "${FITXERS[@]}" "$REMOT:$DESTI"

echo "== RPi: servidor"
scp -q lingualab-server.py "$REMOT:~/lingualab-server.py"
ssh -o BatchMode=yes "$REMOT" 'chmod 644 ~/lingualab/*.html ~/lingualab/*.webmanifest ~/lingualab/*.js 2>/dev/null; \
  cd ~ && (pm2 describe lingualab >/dev/null 2>&1 && pm2 restart lingualab || pm2 start ~/lingualab-server.py --name lingualab --interpreter python3) && pm2 save >/dev/null && \
  sleep 1 && curl -s -o /dev/null -w "   http://100.115.134.76:3054/ -> %{http_code}\n" http://127.0.0.1:3054/'

if [ "${1:-}" = "--git" ]; then
  echo "== GitHub"
  git add -A
  git commit -q -m "LinguaLab: actualització $(date +%Y-%m-%d)" || echo "   (res a committar)"
  git push -q origin main
  echo "   pujat · Pages: https://bernatmora.github.io/lingualab/"
fi

echo "== fet. Recorda que el service worker fa memòria cau: per veure canvis al mòbil,"
echo "   tanca i obre l'app (o recarrega dues vegades)."
