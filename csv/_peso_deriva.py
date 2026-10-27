# -*- coding: utf-8 -*-
r"""**QUANTO PESA LA DERIVA DI `H_tot` SUI RISULTATI DI OGGI** *([[ENERGIA-NON-CONSERVATA-S1]], [[LIBRO-DEI-CONTI]], [[ENERGIA-DEL-LEGAME]]; la risposta di Luca delle `19:25`;
il task history `doc/TASK_HISTORY/2026-10-27_energia_non_conservata_s1.md`)*: ### **`D = |H_tot(t) - H_tot(0)|` contro gli scambi** *(vuoto, cinetica, legame)*
### **di `15df5c63` alla vita e a `T_MAX`; e il residuo del toro contro i flussi del disco `2 w_in` della strada `A`.** ### **Il criterio di Luca: sotto il `5%` il verso resta.**
### **Nessuna corsa nuova.**

Gira con:  python csv/_peso_deriva.py > doc/referti_l2/peso_deriva.txt
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
for _p in (_QUI, os.path.join(RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

RIF_E = os.path.join(RADICE, "doc", "referti_l2", "energia_del_legame.jsonl")
RIF_A = os.path.join(RADICE, "doc", "referti_l2", "libro_dei_conti.jsonl")
SOGLIA = 0.05                  # ### il criterio di Luca (19:25)
T_MAX = 2000
SCAMBI = (("vuo", "il vuoto"), ("cin", "la cinetica"), ("leg", "il legame"))


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("QUANTO PESA LA DERIVA DI H_tot (IL LEGAME S1) SUI RISULTATI DI OGGI: contro gli scambi di 15df5c63 e i flussi della strada A; il criterio di Luca, sotto il 5%% il verso resta")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("csv/_peso_deriva.py", "doc/referti_l2/energia_del_legame.jsonl", "doc/referti_l2/libro_dei_conti.jsonl")}
    print("  i blob nel repo: %s" % "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items()))
    print("  la configurazione: SOGLIA %g T_MAX %d; le corse di 15df5c63 col tick intero e lo zero simmetrico" % (SOGLIA, T_MAX))
    print("-" * 130)
    cc = [json.loads(l) for l in io.open(RIF_E, encoding="utf-8")]
    cc = [x for x in cc if x.get("tipo") == "corsa" and x["modo"] == "intero" and x["zero"] == "simm"]
    print("### 15df5c63: D = |Delta H_tot| contro gli scambi |Delta E_p| sul toro intero")
    reggono = []
    for x in sorted(cc, key=lambda x: (-x["N"], x["L"])):
        s0 = x["serie"][0]["E"]["totale"]
        for t in (x["vita20"], T_MAX):
            st = [s for s in x["serie"] if s["t"] == t][0]["E"]["totale"]
            D = abs(st["tot"] - s0["tot"])
            parti = []
            ok = True
            for k, nome in SCAMBI:
                X = abs(st[k] - s0[k])
                r = D / X if X > 0 else float("inf")
                ok &= r < SOGLIA
                parti.append("%s %+.4e (D/X %.4f)" % (nome, st[k] - s0[k], r))
            reggono.append(ok)
            print("  N %-7g L %3d t %4d: Delta H_tot %+.4e; %s -> %s" % (x["N"], x["L"], t, st["tot"] - s0["tot"], "; ".join(parti), "IL VERSO REGGE (sotto il 5%)" if ok else "### OLTRE IL 5%"))
    print("-" * 130)
    a = [json.loads(l) for l in io.open(RIF_A, encoding="utf-8")]
    A = [x for x in a if x.get("tipo") == "strada_A"][0]["dischi"]
    print("### IL LIBRO DEI CONTI, LA STRADA A (N 1e5 L 48): il residuo del toro (la deriva) contro i flussi del disco 2 w_in (VICINO), in N |e_K(0)|")
    for quando, e, u in (("fino alla vita", "entrate_vita", "uscite_vita"), ("dopo la vita", "entrate_dopo", "uscite_dopo")):
        tor, d2 = A["toro"], A["disco_2"]
        r_ass = (tor[e] - tor[u]) / (d2[e] - d2[u])
        r_sal = abs(tor[e] + tor[u]) / abs(d2[e] + d2[u])
        print("  %s: il toro entrate %+.4e uscite %+.4e (saldo %+.4e); il disco 2 entrate %+.4e uscite %+.4e (saldo %+.4e); il rapporto dei valori assoluti %.4f, dei saldi %.4f"
              % (quando, tor[e], tor[u], tor[e] + tor[u], d2[e], d2[u], d2[e] + d2[u], r_ass, r_sal))
    print("-" * 130)
    print("### LA LETTURA: il verso regge sotto il 5%% in %d casi su %d (corsa per corsa, alla vita e a T_MAX)" % (sum(reggono), len(reggono)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
