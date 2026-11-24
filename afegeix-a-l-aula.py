#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Afegeix LinguaLab a la portada nova de l'Aula BernatLab (l'índex amb RESOURCES).

La portada del 23/11 és un document amb `const RESOURCES = [...]` i
`const categories = ['Tot', ...]`; les targetes i els filtres es generen d'aquí.
Aquest guió, doncs:
  1. afegeix la categoria «Anglès» (si no hi és),
  2. afegeix el recurs de LinguaLab a RESOURCES (si no hi és),
  3. afegeix l'enllaç a la llista del <noscript> (per si algú navega sense JS).

És idempotent: si ja hi és, no toca res.
"""

import io
import json
import re
import sys

INDEX = sys.argv[1] if len(sys.argv) > 1 else "index.html"

RECURS = {
    "title": "LinguaLab · anglès B2–C1",
    "description": (
        "Textos bilingües (anglès → castellà) de notícies i històries, per nivell B2–C1: "
        "lectura en veu alta, vocabulari clau amb pronúncia, flashcards, quiz de traducció, "
        "favorits i el progrés desat al navegador. Es pot instal·lar com a app i funciona sense connexió."
    ),
    "badge": "24 textos · 147 expressions",
    "href": "https://bernatmora.github.io/lingualab/",
    "category": "Anglès",
    "accent": "learn",
    "links": [],
    "private": False,
}

with io.open(INDEX, encoding="utf-8") as f:
    t = f.read()

canvis = []

# ── 1. Categoria nova ──
m = re.search(r"const categories=\[([^\]]*)\]", t)
if not m:
    sys.exit("ERROR: no trobo `const categories=[...]`")
llista = [c.strip().strip("'\"") for c in m.group(1).split(",") if c.strip()]
if "Anglès" not in llista:
    if "Preferits" in llista:
        llista.insert(llista.index("Preferits"), "Anglès")
    else:
        llista.append("Anglès")
    nova = "const categories=[" + ",".join("'%s'" % c for c in llista) + "]"
    t = t[:m.start()] + nova + t[m.end():]
    canvis.append("categoria Anglès")

# ── 2. Recurs a RESOURCES ──
if "lingualab" not in t:
    m = re.search(r"const RESOURCES = (\[.*?\]);", t, re.S)
    if not m:
        sys.exit("ERROR: no trobo `const RESOURCES = [...]`")
    inici, fi = m.span(1)
    bloc = json.dumps(RECURS, ensure_ascii=False)
    tancament = fi - 1
    previ = t[inici:tancament].rstrip()
    separador = "" if previ.endswith("[") else ", "
    t = t[:tancament] + separador + bloc + t[tancament:]
    canvis.append("recurs a RESOURCES")

# ── 3. Llista del <noscript> ──
anc = '<li><a href="./Radio/index.html">Ràdio</a></li>'
if "lingualab" not in t and t.count(anc) == 1:
    nou = (anc + '<li><a href="https://bernatmora.github.io/lingualab/">'
                'LinguaLab · anglès B2–C1</a></li>')
    t = t.replace(anc, nou, 1)
    canvis.append("enllaç al noscript")

if not canvis:
    print("ja hi era: la portada ja té LinguaLab")
    sys.exit(0)

# ── comprovació que el JSON queda vàlid abans d'escriure ──
m = re.search(r"const RESOURCES = (\[.*?\]);", t, re.S)
try:
    d = json.loads(m.group(1))
except json.JSONDecodeError as e:
    sys.exit(f"ERROR: el JSON quedaria trencat ({e}); no escric res")
assert any("lingualab" in r["href"] for r in d), "el recurs nou no hi és"

with io.open(INDEX, "w", encoding="utf-8") as f:
    f.write(t)
print("portada actualitzada:", ", ".join(canvis), f"({len(d)} recursos)")
