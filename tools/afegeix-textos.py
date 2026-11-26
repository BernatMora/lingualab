#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""afegeix-textos.py — afegeix articles/textos nous al LinguaLab (anglès + traducció + vocabulari).

Insereix objectes nous dins el literal `const initialTexts = [ … ]` de l'`index.html`, amb la
mateixa forma que els que ja hi ha:

    { id, title, level, type, en, es, keys }      keys = "en: es" separats per \\n

És idempotent: si l'id ja hi és, no el torna a posar. Valida el resultat amb `node` abans d'escriure.

    python3 tools/afegeix-textos.py            # afegeix els textos del fitxer de dades
    python3 tools/afegeix-textos.py --llista   # només diu què afegiria
"""

import argparse
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE.parent / "index.html"
DADES = HERE / "textos-novells.json"


def literal_initial_texts(html: str) -> tuple[int, int]:
    """Retorna (inici, final) del literal [ … ] de `const initialTexts`."""
    i = html.index("const initialTexts")
    inici = html.index("[", i)
    fons = 0
    for k in range(inici, len(html)):
        if html[k] == "[":
            fons += 1
        elif html[k] == "]":
            fons -= 1
            if fons == 0:
                return inici, k + 1
    raise ValueError("no tanco el literal de initialTexts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llista", action="store_true")
    a = ap.parse_args()

    html = io.open(INDEX, encoding="utf-8").read()
    inici, final = literal_initial_texts(html)
    existeixen = set(re.findall(r'"id":\s*"([^"]+)"', html[inici:final]))
    existeixen |= set(re.findall(r"\bid:\s*['\"]([^'\"]+)['\"]", html[inici:final]))

    nous_tots = json.loads(io.open(DADES, encoding="utf-8").read())
    nous = [t for t in nous_tots if t["id"] not in existeixen]

    print(f"textos al fitxer: {len(nous_tots)} · ja hi són: {len(nous_tots) - len(nous)} · per afegir: {len(nous)}")
    for t in nous:
        print(f"   + {t['id']} · {t['level']:<7} · {t['type']:<7} · {t['title']}")
    if a.llista or not nous:
        return

    blocs = []
    for t in nous:
        ordre = ["id", "title", "level", "type", "en", "es", "keys"]
        blocs.append("  {" + ", ".join(f'"{c}": {json.dumps(t[c], ensure_ascii=False)}' for c in ordre) + "}")
    nou_literal = html[inici:final - 1].rstrip()
    separador = "" if nou_literal.endswith("[") else ", "
    html_nou = html[:final - 1] + separador + ",\n".join(blocs) + html[final - 1:]

    # validació amb node abans d'escriure res (guions a part: res d'escapes dins d'un f-string)
    prova = HERE / "_prova.html"
    io.open(prova, "w", encoding="utf-8").write(html_nou)
    try:
        r = subprocess.run(["node", str(HERE / "valida.js"), str(prova)],
                           capture_output=True, text=True)
    finally:
        prova.unlink(missing_ok=True)
    if r.returncode != 0:
        sys.exit("ERROR: el resultat no és vàlid: " + (r.stderr or "").strip()[:400])
    print("validació:", r.stdout.strip())

    io.open(INDEX, "w", encoding="utf-8").write(html_nou)
    print(f"afegits {len(nous)} textos a {INDEX}")


if __name__ == "__main__":
    main()
