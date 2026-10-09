# -*- coding: utf-8 -*-
"""IL PUNTO `4`: **le due convenzioni, lette da `CLAUDE.md`.**

> ### ⛔ **`PRESIDIO` E' SOLO CIO' CHE E' CABLATO**, e lo dice `A9`: *«un presidio che non
> impedisce non e' un presidio»*. ### **Le REGOLE DI LAVORO del §`11` non impediscono
> niente**: sono ### **`STANDARD`.** ### **I cablati del §`12`** *(hook, assert,
> `permissions.deny`)* ### **sono `PRESIDIO`.**
>
> ### ⭐ **E UNA REGOLA O UN HOOK IN VIGORE E' `APERTA`:** `CHIUSA` ### **solo se ritirato
> o fuso in un altro.** ### **Una regola non si «finisce»: VALE** — ed e' la stessa frase
> degli assiomi del giro scorso.

### 📌 **GLI ID SI LEGGONO DA `CLAUDE.md`, NON DA ME:** le due tabelle del §`11` e del §`12`.
### ⛔ **«In vigore» = «citata in `CLAUDE.md` OGGI»**, non *«mi pare in uso»* — e se un ID
spariva dalle tabelle, ### **questo attrezzo lo smetterebbe di dichiarare in vigore da se'.**

Gira con:  python csv/_due_convenzioni.py
"""
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
BT = chr(96)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"
_RIGA = re.compile(r"^\|\s*\*\*" + BT + r"([^" + BT + r"]+)" + BT + r"\*\*\s*\|", re.M)


def tabella(da, a):
    """### Gli ID nella prima colonna della tabella fra due intestazioni di `CLAUDE.md`."""
    testo = io.open(os.path.join(RADICE, "CLAUDE.md"), encoding="utf-8").read()
    k = testo.index(da)
    fine = testo.index(a, k) if a else len(testo)
    fuori = [m.group(1) for m in _RIGA.finditer(testo[k:fine], ) if m.group(1)]
    fuori = [x for x in fuori if x not in ("id",)]
    assert fuori, "nessun ID nella tabella fra %r e %r" % (da[:30], (a or "")[:30])
    return fuori


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    regole = tabella("## 11. LE REGOLE DI LAVORO", "## 12. I PRESIDI AUTOMATICI")
    cablati = tabella("## 12. I PRESIDI AUTOMATICI", None)
    print("  §11, LE REGOLE DI LAVORO (%d): %s" % (len(regole), " ".join(regole)))
    print("  §12, I CABLATI (%d): %s" % (len(cablati), " ".join(cablati)))
    lotto, fuori_indice, gia = [], [], []
    for i in regole:
        if i not in per:
            fuori_indice.append((i, "§11"))
            continue
        v = per[i]
        campi = {}
        if v["classe"] != "STANDARD":
            campi["classe"] = "STANDARD"
        if v["stato"] == "CHIUSA":
            campi["stato"] = "APERTA"
        if not campi:
            gia.append((i, "§11", "gia- `STANDARD` e non `CHIUSA`"))
            continue
        lotto.append({"id": i, "quando": DATA, "campi": campi,
                      "motivo": ("(4) LE DUE CONVENZIONI: `%s` e- una REGOLA DI LAVORO del "
                                 "§11 di CLAUDE.md, e una regola scritta NON IMPEDISCE "
                                 "NIENTE (`A9`): e- uno `STANDARD`, non un `PRESIDIO` -- "
                                 "`PRESIDIO` e- solo cio- che e- CABLATO (§12). %s"
                                 % (i, ("E una regola IN VIGORE e- `APERTA`: una regola non "
                                        "si <<finisce>>, VALE -- `CHIUSA` solo se ritirata "
                                        "o fusa in un-altra."
                                        if "stato" in campi else ""))).strip()})
    for i in cablati:
        if i not in per:
            fuori_indice.append((i, "§12"))
            continue
        v = per[i]
        campi = {}
        if v["classe"] != "PRESIDIO":
            campi["classe"] = "PRESIDIO"
        if v["stato"] == "CHIUSA":
            campi["stato"] = "APERTA"
        if not campi:
            gia.append((i, "§12", "gia- `PRESIDIO` e non `CHIUSA`"))
            continue
        lotto.append({"id": i, "quando": DATA, "campi": campi,
                      "motivo": ("(4) LE DUE CONVENZIONI: `%s` e- CABLATO -- sta nella "
                                 "tabella del §12 di CLAUDE.md, cioe- IMPEDISCE "
                                 "STRUTTURALMENTE -- quindi e- un `PRESIDIO`. %s"
                                 % (i, ("E UN HOOK IN VIGORE E- `APERTA`: <<in vigore>> "
                                        "vuol dire CITATO IN CLAUDE.md OGGI, e `CHIUSA` "
                                        "solo se ritirato o fuso in un altro."
                                        if "stato" in campi else ""))).strip()})
    p = os.path.join(D, "_lotti", "v3_convenzioni.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_convenzioni.jsonl: %d voci" % len(lotto))
    for x in lotto:
        v = per[x["id"]]
        print("   %-20s %-10s/%-9s -> %s" % (x["id"], v["classe"], v["stato"],
                                             json.dumps(x["campi"], ensure_ascii=True)))
    print("  ### GIA- A POSTO: %d  -> %s" % (len(gia), " ".join(i for i, _s, _p in gia)))
    print("  ### CITATI IN CLAUDE.md MA NON VOCI: %d  -> %s"
          % (len(fuori_indice), " ".join("%s (%s)" % x for x in fuori_indice)))
    io.open(os.path.join(D, "_p4_convenzioni.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(
                {"regole_11": regole, "cablati_12": cablati,
                 "cambiate": [x["id"] for x in lotto],
                 "gia_a_posto": [i for i, _s, _p in gia],
                 "citati_non_voci": fuori_indice}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
