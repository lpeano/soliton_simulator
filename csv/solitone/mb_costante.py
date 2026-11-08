# -*- coding: utf-8 -*-
r"""**(m-b) SUL RAMO LATERALE: I CONTI COL NUCLEO NUOVO CONTRO IL VECCHIO, DALLO STESSO STATO** *(Luca `2026-11-08` `21:49`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`)*. [[PIANO-2D-3D]]

    python csv/solitone/mb_costante.py --misura <file.npz> [N]          (in ogni albero: qui il nucleo nuovo, nel worktree del principale il vecchio)
    python csv/solitone/mb_costante.py --confronta <nuovo.npz> <vecchio.npz> <vecchio_N_diverso.npz> > doc/referti_l2/mb_costante.txt

**La misura:** lo stato completo di `TBS` a `100000` *(la libreria)*, `N` tick *(`200`)* del ciclo della corsa *(`AC.tick`, `BO.assorbi` con `c(t) F3`, gli accumulatori del
bordo dal pezzo prima: le righe di `c0_cucitura` del principale)*; a `t0` e alla fine i conti per nodo per TERMINE sommati, la norma, `E + E_ass`, `e_K`, gli sha.
**Il confronto:** (L0) gli sha uguali; (L1) `e_K` nuovo - vecchio = `pi`; (L2) per termine `(nuovo - vecchio) / M` = `0` o `pi`; (L3) `E + E_ass` la stessa costante a `t0` e alla fine;
il DEVE FALLIRE: L0 contro un vecchio con `N` diverso.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"
TICK0 = 100000
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
ACC = ("M_ass", "V_ass", "E_ass")
CONTI = ("cin", "vuo", "leg", "cost", "tot")
EPS = float(np.finfo(float).eps)
TOLL_L2 = 64.0                 # ### mia, dichiarata (sez. 2): 64 eps relativi al termine
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def misura(out, N):
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    for m in ("__init__", "bordo", "accensione", "corsa_accensione", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", "flussi_parziali.py"))
    _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", "energia_pesata.py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr, _camp = CA.serie(CORSA)[:2]
    riga_p = [r for r in rr if r["t1"] == TICK0][0]
    bor0 = rr[0]["bordo"]
    K = int(round(CA.CORSE[CORSA][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, inc, mot, par = z["st"], z["inc"], z["mot"], z["par"]
        g_e, _gn, _r = BO.g_estremita(z, bor0["c0"][0], bor0["c0"][1], bor0["R_A"], bor0["g_max"])
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        with np.load(FILE_LIB) as d:
            assert int(d["t"]) == TICK0
            for k in chiavi:
                st[k][...] = d[k]
        bor = {k: float(riga_p["bordo"][k]) for k in ACC}

        def conti():
            co = LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)
            return {c: math.fsum(co[c].tolist()) for c in CONTI}, math.fsum(co["M"].tolist())

        c_0, M_0 = conti()
        E0 = c_0["tot"] + bor["E_ass"]
        a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
        with a_, b_:
            for t in range(TICK0 + 1, TICK0 + N + 1):
                AC.tick(z, t, K)
                e_pr = float(np.sum(LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"]))
                dM, dV = BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v)
                bor["M_ass"] += dM
                bor["V_ass"] += dV
                bor["E_ass"] += e_pr - float(np.sum(LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"]))
        c_1, M_1 = conti()
        E1 = c_1["tot"] + bor["E_ass"]
        sh = V.shas(z)
    dati = {"N": N, "e_K": e_K, "M0": M_0, "M1": M_1, "E0": E0, "E1": E1, "M_ass": bor["M_ass"], "E_ass": bor["E_ass"],
            "c0": c_0, "c1": c_1, "sha": sh}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=1)
    print("  scritto %s: N %d, e_K %r, M0 %r, E0 %r, E1 %r" % (out, N, e_K, M_0, E0, E1))
    return 0


def confronta(fn, fv, fvN):
    import _presidio
    _presidio.avvia(__file__)
    a, b, bN = (json.load(open(f, encoding="utf-8")) for f in (fn, fv, fvN))
    print("=" * 130)
    print("(m-b) IL NUCLEO NUOVO (%s) CONTRO IL VECCHIO (%s), dallo stato di %s a %d, N %d" % (fn, fv, CORSA, TICK0, a["N"]))
    print("=" * 130)
    assert a["N"] == b["N"] and bN["N"] != a["N"]
    div = sorted(k for k in a["sha"] if a["sha"][k] != b["sha"].get(k))
    esito("(L0) la dinamica: gli sha dello stato alla fine uguali, ogni chiave", not div, "%d chiavi; diverse %s" % (len(a["sha"]), div))
    divN = sorted(k for k in a["sha"] if a["sha"][k] != bN["sha"].get(k))
    esito("(L0-F) contro il vecchio con N %d: gli sha uguali" % bN["N"], not divN, "diverse %s" % divN, deve=False)
    deK = a["e_K"] - b["e_K"]
    esito("(L1) e_K nuovo - vecchio = pi entro 4 eps pi", abs(deK - math.pi) <= 4 * EPS * math.pi, "%r (scarto %.3e)" % (deK, deK - math.pi))
    print("  la norma M a t0: nuovo %r vecchio %r; alla fine %r %r" % (a["M0"], b["M0"], a["M1"], b["M1"]))
    for fase, M in (("c0", a["M0"]), ("c1", a["M1"])):
        for c in CONTI:
            dlt = a[fase][c] - b[fase][c]
            q = dlt / M
            scala = max(abs(a[fase][c]), abs(b[fase][c]), 1e-300)
            cl = "0" if abs(dlt) <= TOLL_L2 * EPS * scala else ("pi" if abs(dlt - math.pi * M) <= TOLL_L2 * EPS * scala else "ALTRO")
            print("  (L2) %s %-4s nuovo %+.15e vecchio %+.15e: (nuovo - vecchio)/M %+.15e -> %s" % ("t0  " if fase == "c0" else "fine", c, a[fase][c], b[fase][c], q, cl))
            esito("(L2) %s il termine %s: (nuovo - vecchio) = 0 o pi M, entro %g eps del termine" % ("t0" if fase == "c0" else "alla fine", c, TOLL_L2), cl != "ALTRO", "%+.6e" % (q - (math.pi if cl == "pi" else 0.0)))
    d0, d1 = a["E0"] - b["E0"], a["E1"] - b["E1"]
    print("  (L3) E + E_ass nuovo - vecchio: a t0 %+.15e (/M0 %+.15e), alla fine %+.15e (/M0 %+.15e); E_ass nuovo - vecchio %+.6e; M_ass %r" % (d0, d0 / a["M0"], d1, d1 / a["M0"], a["E_ass"] - b["E_ass"], a["M_ass"]))
    esito("(L3) E + E_ass: la STESSA costante a t0 e alla fine, entro %g eps di E" % TOLL_L2, abs(d1 - d0) <= TOLL_L2 * EPS * abs(a["E0"]), "scarto %.3e (soglia %.3e)" % (d1 - d0, TOLL_L2 * EPS * abs(a["E0"])))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a and a[0] == "--misura":
        sys.exit(misura(a[1], int(a[2]) if len(a) > 2 else 200))
    if a and a[0] == "--confronta":
        sys.exit(confronta(a[1], a[2], a[3]))
    print(__doc__)
    sys.exit(2)
