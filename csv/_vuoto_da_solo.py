# -*- coding: utf-8 -*-
r"""**IL VUOTO DA SOLO** *(il mandato breve del 2026-10-27, 02:43; [[SOLITONE-VUOTO-CONGELATO]], [[CANALE-CS-SECONDA-SORGENTE]])*: ### **le scene di `74f99039` con la materia a ZERO, il tick intero:
il vuoto uniforme resta uniforme, o e' instabile per conto suo?** ### **Il controllo col vuoto congelato.**

> ### ⛔ **Il task history e' `2026-10-27_vuoto_da_solo.md`.** ### **In memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_solitone_vuoto_congelato` *(`S`, `FORMA`, `VUOTO`)*, `_screening_forme_s3.forma`, `scena_l2.scena_toro`, `tick.percorri_tick`.

Gira con:  python csv/_vuoto_da_solo.py > doc/referti_l2/vuoto_da_solo.txt
"""
import io
import json
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LATI = (48, 69, 81, 120)
T_MAX = 2000
OGNI = 20
SOGLIE = (0.1, 1.0)
TOLL_NORMA = 1e-10
TOLL_UNIF = 1e-6
T_SOLITONE = 320
RIF = os.path.join(RADICE, "doc", "referti_l2", "solitone_vuoto_congelato.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "vuoto_da_solo.jsonl")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def corsa(L, congelato):
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    import scena_l2 as SL
    import tick as TK
    inc, mot, st, par = SL.scena_toro("triangoli", (L, L), 1.0, 0.1)
    n = inc.n
    mot.cs = np.full(n, VC.S)
    mot.lambda_c = None
    par = dict(par)
    par["eps"] = 0.0
    st["psi_h"][...] = 0.0
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    phi0 = st["phi_h"].copy()
    nodo = inc.nodo
    gr = np.bincount(nodo, minlength=n).astype(float)

    def lam_e():
        x = np.zeros(n)
        np.add.at(x, nodo, np.abs(st["phi_h"]) ** 2)
        return x / gr
    l0 = lam_e()
    V0 = float(np.sum(np.abs(st["phi_h"]) ** 2))
    serie, dV, bit = [], 0.0, True
    primo = {s_: None for s_ in SOGLIE}
    salta = VC.VUOTO if congelato else ()
    t0 = time.time()
    with SF.forma(VC.FORMA):
        for t in range(T_MAX + 1):
            if t % OGNI == 0:
                le = lam_e()
                sc = float(np.std(le))
                serie.append([t, float(le.min()), float(le.max()), sc])
                dV = max(dV, abs(float(np.sum(np.abs(st["phi_h"]) ** 2)) - V0) / V0)
                bit &= le.tobytes() == l0.tobytes()
                for s_ in SOGLIE:
                    if primo[s_] is None and sc > s_:
                        primo[s_] = t
            if t < T_MAX:
                TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))
                if congelato:
                    st["phi_h"][...] = phi0
    return {"tipo": "corsa", "L": L, "congelato": congelato, "dV": dV, "al_bit": bit, "scarto_max": max(x[3] for x in serie), "scarto_finale": serie[-1][3],
            "min_finale": serie[-1][1], "max_finale": serie[-1][2], "primo": {str(k): v for k, v in primo.items()}, "serie": serie, "secondi": time.time() - t0}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL VUOTO DA SOLO: le scene di 74f99039 con la materia a zero, il tick intero; il controllo col vuoto congelato")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_vuoto_da_solo.py", "csv/_solitone_vuoto_congelato.py", "doc/referti_l2/solitone_vuoto_congelato.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LATI %s T_MAX %d OGNI %d SOGLIE %s TOLL_NORMA %g TOLL_UNIF %g T_SOLITONE %d; da _solitone_vuoto_congelato: S %g FORMA %s VUOTO %s; la materia a zero, lambda_c None"
          % (LATI, T_MAX, OGNI, SOGLIE, TOLL_NORMA, TOLL_UNIF, T_SOLITONE, VC.S, VC.FORMA, VC.VUOTO))
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    ris = []
    for L in LATI:
        for cong in (False, True):
            r = corsa(L, cong)
            ris.append(r)
            scrivi(r)
            print("  L %3d %-10s: lo scarto di Lambda per estremita' massimo %.3e, finale %.3e (min %.9f, max %.9f); il primo tick oltre 0.1: %s, oltre 1: %s; dV %.1e; al bit %s (%.0f s)"
                  % (L, "congelato" if cong else "intero", r["scarto_max"], r["scarto_finale"], r["min_finale"], r["max_finale"], r["primo"]["0.1"], r["primo"]["1.0"], r["dV"], r["al_bit"], r["secondi"]))
            sys.stdout.flush()
    print("### ACCANTO: il tick intero col solitone di 74f99039 (lo zero di oggi), Lambda per estremita' al centro e lontano")
    for l in io.open(RIF, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "corsa" and d["modo"] == "intero" and d["zero"] == "oggi":
            a = [x for x in d["serie"] if x[0] == T_SOLITONE]
            print("  N %-7g L %3d: a %d tick il centro %s, lontano %s; alla fine il centro %.4f, lontano %.4f; la vita %s"
                  % (d["N"], d["L"], T_SOLITONE, "%.4f" % a[0][3] if a else "-", "%.4f" % a[0][4] if a else "-", d["lam_centro_fine"], d["lam_lontano_fine"], d["vita"]))
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (1): V conservato entro %g relativo" % TOLL_NORMA, all(r["dV"] <= TOLL_NORMA for r in ris), "il peggiore %.1e" % max(r["dV"] for r in ris))
    esito("DEVE PASSARE (2): il controllo, col vuoto congelato Lambda per estremita' uniforme AL BIT", all(r["al_bit"] for r in ris if r["congelato"]), "")
    sc = max(r["scarto_max"] for r in ris if not r["congelato"])
    esito("PUO' FALLIRE (3): il vuoto da solo resta uniforme entro %g fino a T_MAX (a ogni L)" % TOLL_UNIF, sc <= TOLL_UNIF, "lo scarto massimo %.3e" % sc, deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
