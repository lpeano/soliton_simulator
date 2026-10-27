# -*- coding: utf-8 -*-
r"""**IL CRITERIO `5` DELLA SCOMPOSIZIONE A UNO ZERO `lambda`, CORRETTO DOPO I NUMERI** *(la risposta di Luca del 2026-10-27, 10:35; [[SCOMPOSIZIONE-ZERO-LAMBDA]])*: ### **le ENERGIE alle due taglie, non le
frazioni** *(le frazioni hanno `E0` al denominatore ed esplodono dove `E0` passa per zero)*: ### **`N e_K`, la cinetica, il legame ed `E0` dopo `2000` tick, entro `1e-3` relativo a `N |e_K(0)|`, a ogni `lambda`.**

> ### ⛔ **Una CORREZIONE DEL CRITERIO DOPO I NUMERI, dichiarata** *(il task history `2026-10-27_scomposizione_zero_lambda.md`, l'annotazione `6`)*. ### **Non rigira niente: legge il jsonl committato in `0fb93b8c`.**

Gira con:  python csv/_scomposizione_zero_lambda_c5.py > doc/referti_l2/scomposizione_zero_lambda_c5.txt
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

TOLL = 1e-3
QUANDO = "t2000"
LETTURA = 0.5
RIF = os.path.join(RADICE, "doc", "referti_l2", "scomposizione_zero_lambda.jsonl")
VOCI = ("N_eK", "E_cin", "E_legame", "E0")


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL CRITERIO 5 CORRETTO DOPO I NUMERI: le energie alle due taglie dopo 2000 tick, entro %g relativo a N |e_K(0)|, a ogni lambda" % TOLL)
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("csv/_scomposizione_zero_lambda_c5.py", "csv/_scomposizione_zero_lambda.py", "doc/referti_l2/scomposizione_zero_lambda.jsonl")}
    print("  i blob nel repo: %s" % "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items()))
    print("  la configurazione: TOLL %g QUANDO %s LETTURA %g VOCI %s" % (TOLL, QUANDO, LETTURA, VOCI))
    print("-" * 130)
    rr = [json.loads(l) for l in io.open(RIF, encoding="utf-8")]
    a, b = [r for r in rr if r.get("tipo") == "scomposizione"]
    scala = a["righe"][0]["M"] * abs(a["e_K0"])
    print("  le taglie L %d e L %d; la scala N |e_K(0)| = %.6e" % (a["L"], b["L"], scala))
    peg, ok = 0.0, True
    for x, y in zip(a["righe"], b["righe"]):
        assert x["quando"] == y["quando"] and x["lambda"] == y["lambda"]
        if x["quando"] != QUANDO:
            continue
        sc = {k: abs(x[k] - y[k]) / scala for k in VOCI}
        m = max(sc.values())
        peg = max(peg, m)
        ok &= m <= TOLL
        print("  lambda %.2f: %s" % (x["lambda"], "  ".join("%s %.2e" % (k, v) for k, v in sc.items())))
    print("-" * 130)
    print("### LA LETTURA a lambda %g (t 0, L %d): in parti dei costituenti" % (LETTURA, a["L"]))
    r = [x for x in a["righe"] if x["quando"] == "t0" and x["lambda"] == LETTURA][0]
    print("  il legame %+.4f, la cinetica %+.4f, l'energia a riposo (il solitone) %+.4f di N e_K" % (r["E_legame"] / r["N_eK"], r["E_cin"] / r["N_eK"], r["E0"] / r["N_eK"]))
    print("-" * 130)
    print("### IL CRITERIO")
    print("  %-110s %s   %s" % ("DEVE PASSARE (5 corretto): N e_K, cinetica, legame, E0 alle due taglie dopo 2000 tick entro %g di N |e_K(0)|, a ogni lambda" % TOLL,
                               "PASSA" if ok else "### FALLISCE", "il peggiore %.2e" % peg))
    print("ESITO: %d/1" % (1 if ok else 0))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
