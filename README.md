# LinguaLab · Anglès B2–C1

App web d'una sola pàgina per aprendre anglès amb textos bilingües (anglès →
castellà), vocabulari clau, flashcards, quiz de traducció i lectura en veu alta.

- **Pública (GitHub Pages):** <https://bernatmora.github.io/lingualab/>
- **BernatLab (RPi, tailnet):** <http://100.115.134.76:3054/>
- **Targeta al tauler:** Homepage :3000 → grup 🎓 Aprenentatge

## Què fa

| Secció | Què hi ha |
|---|---|
| **Biblioteca** | 48 textos bilingües (notícies, històries i articles) amb nivell B2 → C1, 371 expressions de vocabulari, cercador i filtre per tipus |
| **Lectura** | Text anglès + traducció que es pot amagar, veu `en-GB` (Web Speech), vocabulari clau amb pronúncia |
| **Flashcards** | Targetes anglès → castellà, barreja, només difícils, marcar coneguda |
| **Quiz** | 4 opcions per expressió, encerts acumulats i percentatge |
| **Favorits** | Els textos que hi has posat estrella |
| **Gestionar** | Afegir/editar/esborrar textos, exportar i importar còpia JSON, restaurar mostra |

Extres: tema clar/fosc, barra mòbil, PWA instal·lable i funcionament sense connexió
(service worker).

## Les dades són al navegador

Tot (textos afegits, favorits, progrés, estadístiques) es desa a `localStorage` amb
les claus `bilingual_texts_v3` i `lingualab_prefs_v1`. **No hi ha servidor ni compte.**
Si esborres les dades del navegador ho perds tot: fes servir
**Gestionar → Exportar còpia JSON** de tant en tant.

## Fitxers

```
lingualab/
├── index.html            ← tota l'app (HTML + CSS + JS en un sol fitxer)
├── manifest.webmanifest  ← PWA
├── sw.js                 ← memòria cau offline (puja CACHE quan publiquis una versió nova)
├── icons/                ← icona SVG + PNG (32, 180, 192, 512)
├── lingualab-server.py   ← servidor estàtic de la RPi (port 3054)
├── publica.sh            ← desplega a la RPi (+ GitHub amb --git)
├── afegeix-a-l-aula.py   ← afegeix o actualitza la targeta a l'Aula BernatLab
└── tools/prepara-index.py ← posa la capçalera PWA i el service worker al fitxer nou
```

### Publicar una versió nova (l'app es treballa com un fitxer solt)

```bash
cp ~/Desktop/LinguaLab_English_2026_vX.html /tmp/nova.html
python3 tools/prepara-index.py /tmp/nova.html index.html   # capçalera PWA + service worker
sed -i '' "s/lingualab-v2/lingualab-v3/" sw.js              # puja la versió de la memòria cau
./publica.sh --git                                          # RPi + GitHub Pages
```

## Publicar

Un sol guió ho fa tot: **`./publica.sh`** (copia a la RPi i reinicia el servei) o
**`./publica.sh --git`** (a més, commit + push a GitHub; Pages es refresca sol).

### GitHub Pages

```bash
git add -A && git commit -m "..." && git push origin main
```

Pages publica la branca `main` (arrel) → <https://bernatmora.github.io/lingualab/>.

### BernatLab (Raspberry Pi)

```bash
scp -r index.html manifest.webmanifest sw.js icons lingualab-server.py \
    hortosona:~/lingualab/          # (crear la carpeta abans: ssh hortosona mkdir -p ~/lingualab)
ssh hortosona 'pm2 restart lingualab && pm2 save'
```

El servidor escolta al **port 3054** i serveix `/home/bernat/lingualab`.
La targeta del tauler viu a `~/homelab/compose/homepage/config/services.yaml`
(després de tocar-la: `docker restart homepage`).

## Llicència

Vegeu [`LICENSE`](LICENSE): material personal de Bernat Mora (BernatLab), ús privat
d'aprenentatge; no es pot redistribuir sense permís.
