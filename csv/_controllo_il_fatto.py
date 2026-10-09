# -*- coding: utf-8 -*-
"""IL CONTROLLO DEL DIFETTO «IL FATTO» — **quali voci cambiano, e nient'altro.**

> ### ⛔ **Il mandato dice «SOLO per controllo»:** questo attrezzo ### **non scrive
> sull'indice** e ### **non costruisce un lotto.** Confronta la decisione del punto `1`
> ### **con il filtro** e ### **senza il filtro**, e ### **elenca la differenza.**

### ⭐ **E la differenza si isola spegnendo il filtro, non riscrivendo la regola:** cosi'
### **l'elenco e' esattamente cio' che il difetto ha causato**, non cio' che credo abbia
causato.

Gira con:  python csv/_controllo_il_fatto.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _righe_origine as RO                                  # noqa: E402
import _stato_dalla_riga as SR                               # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge l'indice e documenti.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")

# ### Le SEI che il mandato dichiara attese. ### ⛔ **Non sono un filtro: sono un CONTROLLO**
# ### -- se una di queste NON cambia, la mia regola non e' quella del mandato.
ATTESE = ("SOGLIA-MITOSI-3PI", "Z23", "Z46", "Z56", "Z66", "Z74")


def decisioni(voci, righe):
    """### `{id: (stato, classe)}` con il filtro ### **come e' adesso.**"""
    fuori = {}
    for v in voci:
        r = righe.get(v["id"])
        fuori[v["id"]] = (SR.decidi_stato(v, r)[0], SR.decidi_classe(v, r)[0])
    return fuori


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    righe = {}
    for v in voci:
        r = RO.riga_origine(v)[0]
        righe[v["id"]] = r
    dopo = decisioni(voci, righe)
    # ### ⛔ **IL FILTRO SI SPEGNE, non si riscrive la regola:** `_scarta` torna `False`,
    # ### cioe' ### **il comportamento di prima della cura.**
    vero = SR._scarta
    SR._scarta = lambda t, k, w: False
    try:
        prima = decisioni(voci, righe)
    finally:
        SR._scarta = vero
    cambia = []
    for v in voci:
        i = v["id"]
        if prima[i] != dopo[i]:
            r = righe.get(i)
            cambia.append({"id": i, "prima": prima[i], "dopo": dopo[i],
                           "stato_su_disco": v["stato"], "classe_su_disco": v["classe"],
                           "riga": " ".join((r or "").split())[:300]})
    print("  voci con una riga d'origine: %d su %d"
          % (sum(1 for v in voci if righe.get(v["id"])), len(voci)))
    print("  ### LE VOCI CHE IL DIFETTO <<IL FATTO>> TOCCAVA: %d" % len(cambia))
    for x in cambia:
        print("   %-24s stato %-14s -> %-14s   classe %-12s -> %-12s   (disco: %s/%s)"
              % (x["id"], x["prima"][0], x["dopo"][0], x["prima"][1], x["dopo"][1],
                 x["classe_su_disco"], x["stato_su_disco"]))
        print("        %s" % x["riga"][:150])
    trovate = {x["id"] for x in cambia}
    manca = [i for i in ATTESE if i not in trovate]
    print()
    print("  IL CONTROLLO DELLE SEI ATTESE: %d su %d" % (len(ATTESE) - len(manca),
                                                         len(ATTESE)))
    for i in ATTESE:
        print("   %-24s %s" % (i, "CAMBIA" if i in trovate else "### NON CAMBIA"))
    io.open(os.path.join(D, "_il_fatto.json"), "w", encoding="utf-8", newline=NL).write(
        json.dumps(cambia, ensure_ascii=False, indent=1))
    print("  scritto doc/indice/_il_fatto.json")
    # ### ⛔ **E QUESTO E- UNA CONDIZIONE DI FERMO, scritta nel task history:** se una delle
    # ### sei NON cambia, ### **la regola che ho scritto non e- quella del mandato.**
    assert not manca, ("### NON CAMBIANO, e il mandato le dichiara attese: %s. La regola "
                       "che ho scritto NON e' quella del mandato" % manca)
    return 0


if __name__ == "__main__":
    sys.exit(main())
