# -*- coding: utf-8 -*-
r"""**DOVE FALLISCONO I CRITERI `2` E `3` DEL CONTO DELL'ENERGIA DEL LEGAME** *([[ENERGIA-DEL-LEGAME]])*: ### **legge il jsonl di `csv/_energia_del_legame.py` e dice, per ogni confronto, il peggiore
e DOVE** *(il tempo, la regione, il pezzo)*, ### **alla vita e a `T_MAX` separati.** ### **Non cambia i criteri: e' una diagnosi del fallimento.**

Gira con:  python csv/_energia_del_legame_dove.py > doc/referti_l2/energia_del_legame_dove.txt
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
for _p in (_QUI, os.path.join(RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

RIF = os.path.join(RADICE, "doc", "referti_l2", "energia_del_legame.jsonl")
VITA = {1e6: 320, 1e5: 140}
T_MAX = 2000
PEZZI = ("cost", "cin", "leg", "vuo", "tot")
REGIONI = ("vicino", "lontano", "totale")


def delta(x, t, reg, pz):
    a = [s for s in x["serie"] if s["t"] == t][0]
    return a["E"][reg][pz] - x["serie"][0]["E"][reg][pz]


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("DOVE FALLISCONO I CRITERI 2 (LE TAGLIE) E 3 (I DUE ZERI) DEL CONTO DELL'ENERGIA DEL LEGAME: il peggiore e dove, alla vita e a T_MAX")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("csv/_energia_del_legame_dove.py", "csv/_energia_del_legame.py", "doc/referti_l2/energia_del_legame.jsonl")}
    print("  i blob nel repo: %s" % "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items()))
    print("  la configurazione: VITA %s T_MAX %d PEZZI %s REGIONI %s" % (VITA, T_MAX, PEZZI, REGIONI))
    print("-" * 130)
    cc = [json.loads(l) for l in io.open(RIF, encoding="utf-8")]
    cc = [r for r in cc if r.get("tipo") == "corsa"]
    print("### (2) LE TAGLIE: |Delta E(L1) - Delta E(L2)| / N |e_K(0)|, il totale di ogni pezzo")
    for N in (1e6, 1e5):
        for z in ("simm", "oggi"):
            for m in ("intero", "congelato"):
                a, b = [x for x in cc if x["N"] == N and x["zero"] == z and x["modo"] == m]
                sc = N * abs(a["e_K"])
                for t in (VITA[N], T_MAX):
                    v = [(abs(delta(a, t, "totale", pz) - delta(b, t, "totale", pz)) / sc, pz) for pz in PEZZI]
                    print("  N %-7g %-4s %-9s t %4d: il peggiore %.2e (%s)   %s" % (N, z, m, t, max(v)[0], max(v)[1], "  ".join("%s %.2e" % (p, x) for x, p in v)))
    print("### (3) I DUE ZERI: |Delta E(simm) - Delta E(oggi) - 2 pi (1/2) Delta norma| / N |e_K(0)|, ogni regione e pezzo")
    for N in (1e6, 1e5):
        for L in sorted({x["L"] for x in cc if x["N"] == N}):
            for m in ("intero", "congelato"):
                s_, o_ = [x for x in cc if x["N"] == N and x["L"] == L and x["modo"] == m]
                sc = N * abs(s_["e_K"])
                for t in (VITA[N], T_MAX):
                    peg = (0.0, None)
                    for reg in REGIONI:
                        for pz in PEZZI:
                            c = 0.0
                            if pz in ("cost", "tot"):
                                c += 2 * math.pi * (s_["lambda"] - o_["lambda"]) * delta(o_, t, reg, "M")
                            if pz in ("vuo", "tot"):
                                c += 2 * math.pi * (s_["lambda"] - o_["lambda"]) * delta(o_, t, reg, "V")
                            x = abs(delta(s_, t, reg, pz) - delta(o_, t, reg, pz) - c) / sc
                            if x > peg[0]:
                                peg = (x, "%s %s" % (reg, pz))
                    print("  N %-7g L %3d %-9s t %4d: il peggiore %.2e (%s)" % (N, L, m, t, peg[0], peg[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
