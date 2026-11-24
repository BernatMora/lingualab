"""actualitza-aula.py — deixa la insígnia de la targeta de LinguaLab de l'Aula al dia.

Els números no s'intenten endevinar: els passos tu, perquè són els que ensenya l'app a
Biblioteca («Textos disponibles» i «Paraules per practicar»). Així no queden mai desfasats
si la manera d'escriure els textos al fitxer canvia.

    python3 tools/actualitza-aula.py 32 213 /ruta/al/aprenentatge/index.html
"""
import io
import re
import sys

if len(sys.argv) < 4:
    sys.exit(__doc__)
textos, expressions, AULA = sys.argv[1], sys.argv[2], sys.argv[3]
badge = f"{textos} textos · {expressions} expressions"
print(f"insígnia a posar: {badge}")

# ── actualització a l'Aula ──
with io.open(AULA, encoding="utf-8") as f:
    aula = f.read()

patro = re.compile(r'("badge":\s*")[^"]*(",\s*"href":\s*"https://bernatmora\.github\.io/lingualab/")')
if not patro.search(aula):
    sys.exit("ERROR: no trobo la targeta de LinguaLab a la portada de l'Aula")

nou, n = patro.subn(lambda mm: mm.group(1) + badge + mm.group(2), aula, count=1)
if n != 1:
    sys.exit("ERROR: substitució ambigua")

if nou == aula:
    print("l'Aula ja tenia la insígnia bona")
    sys.exit(0)

with io.open(AULA, "w", encoding="utf-8") as f:
    f.write(nou)
print("targeta de l'Aula actualitzada")
