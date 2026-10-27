# -*- coding: utf-8 -*-
r"""**IL SIGILLO `(iv)` DEL LIBRO DEI CONTI, CORRETTO DOPO I NUMERI** *([[LIBRO-DEI-CONTI]]; la risposta di Luca delle `18:45`; il task history
`doc/TASK_HISTORY/2026-10-27_libro_dei_conti_strumento.md`, paragrafo `5`)*: ### **la serie `H_tot(t)` a `s 0.3` e `0.15` sullo stesso tempo fisico;
l'assestamento `t_a`, il SALTO iniziale, l'errore del passo e la deriva DOPO `t_a`; il rapporto.**

> ### **Importato, non copiato:** `_libro_dei_conti` *(`scena`, `conti_per_nodo`, le costanti)*.

Gira con:  python csv/_libro_dei_conti_iv.py > doc/referti_l2/libro_dei_conti_iv.txt
"""
import io
import json
import math
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

JSONL = os.path.join(RADICE, "doc", "referti_l2", "libro_dei_conti_iv.jsonl")
TAU = 600.0                    # ### il tempo fisico: 2000 tick a s 0.3
S_PASSI = (0.3, 0.15)
CRESCITA = 0.01                # ### l'assestamento: il massimo progressivo cresce meno dell'1% fino alla fine
RAPPORTO_ATTESO = 4.0
TOLL = 0.2


def assestamento(D):
    """### `t_a`: il primo tick dopo il quale il massimo progressivo di `|D|` cresce meno di `CRESCITA` fino alla fine."""
    run = np.maximum.accumulate(np.abs(D))
    fine = run[-1]
    k = np.flatnonzero(run * (1.0 + CRESCITA) >= fine)
    return int(k[0])


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _libro_dei_conti as LC
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL SIGILLO (iv) DEL LIBRO DEI CONTI, CORRETTO DOPO I NUMERI (Luca, 18:45): l'assestamento, il salto iniziale, l'errore del passo e la deriva dopo l'assestamento")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_libro_dei_conti_iv.py", "csv/_libro_dei_conti.py", "csv/_energia_del_legame.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: TAU %g S_PASSI %s CRESCITA %g RAPPORTO_ATTESO %g TOLL %g; da _libro_dei_conti: N_RIF %g FATTORE %g ZERO %s LAM_ZERO %g"
          % (TAU, S_PASSI, CRESCITA, RAPPORTO_ATTESO, TOLL, LC.N_RIF, LC.FATTORE, LC.ZERO, LC.LAM_ZERO))
    print("  ### IL CRITERIO, CORRETTO DOPO I NUMERI: l'errore del passo = max_{t >= t_a} |H_tot(t) - H_tot(t_a)|; t_a = il primo tick dopo il quale il massimo progressivo di |H_tot - H_tot(0)| cresce meno dell'1%")
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(VC.S)
        rec = {"larghezza": MPS.largo(VC.FORMA, cc, VC.S, LC.N_RIF)["larghezza"], "c": cc}
    finally:
        MPS.LAM0 = vero
    L, inc, mot, st, par, rr, w = LC.scena(rec, False)
    _L, _i, _m, _s, _p, _pos, _rr, Q, m1, m2, _r = __import__("_energia_del_legame").stato(LC.N_RIF, LC.FATTORE, rec)
    incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
    Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
    e_K = Eu / Mu
    sc = LC.N_RIF * abs(e_K)
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA}, sort_keys=True) + "\n")
    ris = {}
    for s in S_PASSI:
        t0 = time.time()
        _L1, inc1, mot1, st1, par1, _rr1, _w1 = LC.scena(rec, False)
        mot1.cs = np.full(inc1.n, s)
        n_t = int(round(TAU / s))
        hh = []
        with SF.forma(VC.FORMA), BE.conv(LC.ZERO):
            for t in range(n_t + 1):
                hh.append(math.fsum(LC.conti_per_nodo(inc1, mot1, st1, e_K, LC.LAM_ZERO)["tot"].tolist()))
                if t < n_t:
                    TK.percorri_tick(st1, mot1, par1, (), None, len(CM.ORDINE))
        H = np.array(hh)
        D = H - H[0]
        ta = assestamento(D)
        dopo = H[ta:] - H[ta]
        err = float(np.max(np.abs(dopo)))
        tt = np.arange(ta, n_t + 1) * s
        der = float(np.polyfit(tt, H[ta:], 1)[0]) if len(tt) >= 3 else None
        ris[s] = {"t_a": ta, "tau_a": ta * s, "salto": float(D[ta]), "errore": err, "deriva": der, "max_tutto": float(np.max(np.abs(D)))}
        print("  s %g: %d tick; t_a %d (tempo fisico %.2f); il SALTO %+.6e = %+.3e N |e_K(0)|; l'errore del passo dopo t_a %.6e = %.3e N |e_K(0)|; la deriva %+.4e per unita' di tempo fisico; il max su tutto %.6e (%.0f s)"
              % (s, n_t, ta, ta * s, D[ta], D[ta] / sc, err, err / sc, der if der is not None else float("nan"), np.max(np.abs(D)), time.time() - t0))
        with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(dict(ris[s], tipo="passo", s=s, serie_ogni_10=[float(x) for x in D[::10]]), sort_keys=True) + "\n")
    rap = ris[S_PASSI[0]]["errore"] / ris[S_PASSI[1]]["errore"] if ris[S_PASSI[1]]["errore"] > 0 else math.inf
    ok = abs(rap / RAPPORTO_ATTESO - 1.0) <= TOLL
    print("-" * 130)
    print("  %-110s %s   %.4f" % ("DEVE PASSARE (iv'): l'errore del passo dopo l'assestamento va come s^2: il rapporto s %g / s %g entro %g +- %g%%" % (S_PASSI[0], S_PASSI[1], RAPPORTO_ATTESO, 100 * TOLL), "PASSA" if ok else "### FALLISCE", rap))
    print("  il rapporto dei SALTI (una lettura): %.4f" % (ris[S_PASSI[0]]["salto"] / ris[S_PASSI[1]]["salto"] if ris[S_PASSI[1]]["salto"] else math.inf))
    print("ESITO: %d/1; DEVE fallite: %d" % (1 if ok else 0, 0 if ok else 1))
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"tipo": "esito", "rapporto": rap, "passa": ok}, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
