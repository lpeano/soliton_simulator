# -*- coding: utf-8 -*-
"""I QUATTRO REGISTRI DEI VOCABOLARI dell'indice `v2` — **GENERATI dalle fonti**.

`doc/indice/leggi.jsonl` · `variabili.jsonl` · `assiomi.jsonl` · `decisioni.jsonl`

### ⛔ **Nessuno dei quattro si scrive a mano:** ciascuno si ### **estrae dalla sua fonte**, e
lo script ### **ASSERISCE** che la fonte contenga cio' che si aspetta. ### ➜ **Se una fonte
cambia forma, il registro NON si scrive** invece di scriverne uno vecchio.

| registro | la fonte |
|---|---|
| `leggi.jsonl` | la ### **TAVOLA** di `csv/_test_fork/_doc_traduzione.py`, che genera `doc/TRADUZIONE_IN_H.md` |
| `variabili.jsonl` | la lista ### **`GIA_CENSITE`** di `csv/_test_fork/_censimento_leggi.py` *(le variabili di `doc/MEMORIE_MANCANTI.md`)*, piu' quelle ### **trovate dal censimento** |
| `assiomi.jsonl` | le intestazioni di ### **`doc/ASSIOMI.md`**, e i ### **sotto-punti** citati nel testo |
| `decisioni.jsonl` | le ### **schede** `<!-- SCHEDA nome=… -->` di `doc/REGISTRO_FISICA.md` che portano *«decisione di Luca»* |

Gira con:  python csv/_registri_indice.py
"""
import ast
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Estrae dai sorgenti e dai
# documenti con l'AST e con espressioni, e il risultato non dipende da nessun flag.
NL = chr(10)
FUORI = os.path.join(RADICE, "doc", "indice")
P = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def scrivi(nome, righe):
    """### Una voce per riga, ### **ordinate per `id`**, chiavi in ordine fisso."""
    righe = sorted(righe, key=lambda r: r["id"])
    ids = [r["id"] for r in righe]
    assert len(ids) == len(set(ids)), "id duplicati in %s: %s" % (
        nome, [x for x in ids if ids.count(x) > 1][:5])
    p = os.path.join(FUORI, nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(r, ensure_ascii=False, sort_keys=False) for r in righe) + NL)
    stampa("  %-20s %4d voci" % (nome, len(righe)))
    return len(righe)


def slug(s):
    """### Da un nome umano a un pezzo di ID: maiuscole, solo `A-Z0-9-`."""
    s = s.upper()
    s = re.sub(r"[ÀÁÂÃÄ]", "A", s)
    s = re.sub(r"[ÈÉÊË]", "E", s)
    s = re.sub(r"[ÌÍÎÏ]", "I", s)
    s = re.sub(r"[ÒÓÔÕÖ]", "O", s)
    s = re.sub(r"[ÙÚÛÜ]", "U", s)
    s = re.sub(r"[^A-Z0-9]+", "-", s)
    return s.strip("-")


# ==========================================================================
#   `1` LE LEGGI -- dalla TAVOLA del generatore di doc/TRADUZIONE_IN_H.md
# ==========================================================================
def leggi_le_leggi():
    src = io.open(os.path.join(_QUI, "_test_fork", "_doc_traduzione.py"),
                  encoding="utf-8").read()
    albero = ast.parse(src)
    tav = None
    for n in albero.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) \
                and n.targets[0].id == "TAVOLA":
            tav = ast.literal_eval(n.value)
    assert tav, "la TAVOLA non si trova in _doc_traduzione.py"
    assert len(tav) >= 20, "la TAVOLA ha solo %d righe: la fonte e' cambiata" % len(tav)
    fuori = []
    for (nome, anc, var, classe, _ex, _esito) in tav:
        # ### l'ancora e' un NOME DI FUNZIONE o DI FLAG, MAI una riga
        ancora = anc.split("(")[0].strip().strip("`")
        fuori.append({
            "id": "L-" + slug(nome)[:40],
            "titolo": nome,
            "ancora": ancora,
            "variabile": var,
            "classe_traduzione": classe,
            "fonte": "doc/TRADUZIONE_IN_H.md::%s" % slug(nome)[:40],
        })
    return fuori


# ==========================================================================
#   `2` LE VARIABILI -- da GIA_CENSITE piu' il censimento
# ==========================================================================
def leggi_le_variabili():
    src = io.open(os.path.join(_QUI, "_test_fork", "_censimento_leggi.py"),
                  encoding="utf-8").read()
    albero = ast.parse(src)
    gia = None
    for n in albero.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) \
                and n.targets[0].id == "GIA_CENSITE":
            gia = list(ast.literal_eval(n.value))
    assert gia and len(gia) >= 35, "GIA_CENSITE non si trova o e' cambiata"
    cen = json.load(io.open(os.path.join(_QUI, "_test_fork", "_censimento_leggi",
                                         "censimento.json"), encoding="utf-8"))
    scritte = {}
    for s in cen["scritture"]:
        scritte.setdefault(s["variabile"], []).append(s["funzione"])
    fuori = []
    for v in sorted(set(gia)):
        fuori.append({
            "id": "V-" + slug(v),
            "nome": v,
            "censita_in": "doc/MEMORIE_MANCANTI.md",
            "scritta_da": sorted(set(scritte.get(v, [])))[:6],
            "scritture": len(scritte.get(v, [])),
        })
    # ### e le QUATTRO trovate dal censimento e NON nel documento: si registrano,
    # ### perche' una voce potrebbe riferirsi a loro
    for v in ("xi_termo", "nati", "negate", "_cura4_maturi"):
        if v in scritte:
            fuori.append({"id": "V-" + slug(v), "nome": v,
                          "censita_in": "csv/_test_fork/_censimento_leggi (NON in "
                                        "doc/MEMORIE_MANCANTI.md)",
                          "scritta_da": sorted(set(scritte[v]))[:6],
                          "scritture": len(scritte[v])})
    return fuori


# ==========================================================================
#   `3` GLI ASSIOMI -- dalle intestazioni di doc/ASSIOMI.md
# ==========================================================================
def leggi_gli_assiomi():
    t = io.open(os.path.join(RADICE, "doc", "ASSIOMI.md"), encoding="utf-8").read()
    righe = t.split(NL)
    fuori, visti = [], set()
    for i, r in enumerate(righe, 1):
        m = re.match(r"^##\s+`?(A\d+)`?\s*[—-]", r)
        if not m:
            continue
        a = m.group(1)
        if a in visti:
            continue
        visti.add(a)
        tit = re.sub(r"^##\s+`?A\d+`?\s*[—-]\s*", "", r)
        tit = re.sub(r"[*#❗`]", "", tit).strip()
        fuori.append({"id": a, "titolo": tit[:100], "riga_fonte": i,
                      "fonte": "doc/ASSIOMI.md::%s" % a, "sotto_punti": []})
    assert len(fuori) >= 15, "trovati solo %d assiomi: la fonte e' cambiata" % len(fuori)
    # ### I SOTTO-PUNTI: si cercano NEL TESTO (`A14.2`, `A15.3`, `A16.1`, `A17.4`, `A3b`)
    per_id = {x["id"]: x for x in fuori}
    for m in re.finditer(r"\bA(\d+)\.(\d)\b", t):
        a, s = "A" + m.group(1), m.group(1) + "." + m.group(2)
        if a in per_id and ("A" + s) not in per_id[a]["sotto_punti"]:
            per_id[a]["sotto_punti"].append("A" + s)
    for x in fuori:
        x["sotto_punti"] = sorted(x["sotto_punti"])
    # ### le VARIANTI con lettera (`A3b`, `A3c`) si registrano come id a se'
    for m in sorted(set(re.findall(r"\bA(\d+[a-c])\b", t))):
        i2 = "A" + m
        if i2 not in per_id:
            fuori.append({"id": i2, "titolo": "(variante di A%s, citata nel testo)"
                          % re.sub(r"[a-c]", "", m), "riga_fonte": 0,
                          "fonte": "doc/ASSIOMI.md::%s" % i2, "sotto_punti": []})
    return fuori


# ==========================================================================
#   `4` LE DECISIONI -- dalle schede di doc/REGISTRO_FISICA.md
# ==========================================================================
def leggi_le_decisioni():
    t = io.open(os.path.join(RADICE, "doc", "REGISTRO_FISICA.md"), encoding="utf-8").read()
    pezzi = re.split(r"<!--\s*SCHEDA nome=([a-z0-9-]+)[^>]*-->", t)
    fuori = []
    # pezzi = [testa, nome1, corpo1, nome2, corpo2, ...]
    for k in range(1, len(pezzi) - 1, 2):
        nome, corpo = pezzi[k], pezzi[k + 1]
        m = re.search(r"[Dd]ecisione di Luca[^.]*?(\d{4}-\d{2}-\d{2})", corpo)
        m2 = re.search(r"DECISIONE DEL (\d{4}-\d{2}-\d{2})", corpo)
        data = (m.group(1) if m else (m2.group(1) if m2 else ""))
        if not re.search(r"[Dd]ecisione di Luca", corpo):
            continue                       # ### non e' una decisione: e' una scheda di legge
        tit = ""
        mt = re.search(r"^##\s+(.+)$", corpo, re.M)
        if mt:
            tit = re.sub(r"[*#⛔⭐❗`]", "", mt.group(1)).strip()
        presa = bool(re.search(r"PRESA", corpo))
        fuori.append({"id": "DEC-" + slug(nome), "nome_scheda": nome,
                      "titolo": tit[:100], "data": data, "presa": presa,
                      "fonte": "doc/REGISTRO_FISICA.md::SCHEDA nome=%s" % nome})
    # ### E GLI ASSIOMI SONO DECISIONI DI LUCA: `A16` e `A17` si registrano anche qui,
    # ### perche' una voce puo' essere SUPERATA DA un assioma.
    for a, data, tit in (("A16", "2026-10-08", "lo stato e' uno, ed evolve al primo ordine "
                                               "sotto una sola H"),
                         ("A17", "2026-10-08", "ogni comportamento e' determinato solo dal "
                                               "suo ambito: niente pos nella fisica")):
        fuori.append({"id": "DEC-" + a, "nome_scheda": "", "titolo": tit, "data": data,
                      "presa": True, "fonte": "doc/ASSIOMI.md::%s" % a})
    assert len(fuori) >= 5, "trovate solo %d decisioni: la fonte e' cambiata" % len(fuori)
    return fuori


def main():
    os.makedirs(FUORI, exist_ok=True)
    stampa("=" * 104)
    stampa("I QUATTRO REGISTRI DEI VOCABOLARI -- generati dalle fonti, non scritti a mano")
    stampa("=" * 104)
    n1 = scrivi("leggi.jsonl", leggi_le_leggi())
    n2 = scrivi("variabili.jsonl", leggi_le_variabili())
    n3 = scrivi("assiomi.jsonl", leggi_gli_assiomi())
    n4 = scrivi("decisioni.jsonl", leggi_le_decisioni())
    stampa()
    stampa("  in tutto: %d ID di vocabolario" % (n1 + n2 + n3 + n4))
    io.open(os.path.join(FUORI, "_registri.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
