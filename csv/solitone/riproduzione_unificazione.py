# -*- coding: utf-8 -*-
r"""**U4 DELL'UNIFICAZIONE: LA RIPRODUZIONE DELLE CORSE** *(Luca `2026-11-12` `10:39`; il task history `doc/TASK_HISTORY/2026-11-12_unificazione.md`, sez. `2`)*. [[PIANO-2D-3D]] [[H-NUCLEO-CONGELATO]]

    python csv/solitone/riproduzione_unificazione.py --misura --radice <albero> --corsa <C35-pi|TBS> --uscita <file.npz>
    python csv/solitone/riproduzione_unificazione.py --confronta <vecchio_C35.npz> <nuovo_C35.npz> <vecchio_TBS.npz> <nuovo_TBS.npz> > doc/referti_l2/unificazione_riproduzione.txt

**La misura** *(sull'albero `--radice`: i suoi `csv/` e `primo_ordine/` per primi in `sys.path`, come `zero_nel_nucleo.py`)*: **lo stato della corsa** *(C35-pi a `60000`, TBS a `10000`:
gli stati del jsonl, controllati con lo `sha`)*, **`N_TICK = 1000` tick col ciclo della corsa** *(`accensione.tick` e `bordo.assorbi` col riferimento `c(t) F3`, il bordo
dell'ultima riga)*; **alla fine:** `rho` per nodo, la norma, la distanza della coppia dai semipiani *(C35-pi)*, i conti del toro *(`fsum`)*, `e_K`, gli `sha`.
**Il confronto** *(Luca)*: **la rms di `rho` relativa sotto `1e-10`; la norma; la distanza; l'energia CONVERTITA** *(`tot + pi (M + V)`)* **entro `1e-10` relativo;** **se al bit, lo
si scrive;** **DEVE FALLIRE: l'energia SENZA conversione entro `1e-10`.**
"""
import importlib.util
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
STATI = {"C35-pi": 60000, "TBS": 10000}   # ### Luca (U4)
N_TICK = 1000                            # ### Luca (U4)
TOLL_RHO = 1e-10                         # ### Luca (U4): la rms di rho relativa
TOLL_E = 1e-10                           # ### Luca (U4): l'energia convertita, relativa
OK = [0, 0]
FALLITE = []


def prendi(argv, nome):
    return argv[argv.index(nome) + 1] if nome in argv else None


def misura(radice, corsa, uscita):
    radici = [os.path.normcase(os.path.abspath(os.path.join(radice, *q))) for q in (("primo_ordine", "leggi"), ("primo_ordine",), ("csv",))]
    questo = os.path.normcase(os.path.dirname(_QUI))
    sys.path[:] = [p for p in sys.path if os.path.normcase(os.path.abspath(p)) not in radici + [questo]]
    for p in reversed(radici):
        sys.path.insert(0, p)
    import numpy as np
    import flussi_parziali as FP
    import solitone
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
    from solitone import carta_coppia as CC
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    from solitone import toro as TO
    for mod in (FP, solitone, V, CA):
        assert os.path.normcase(os.path.abspath(mod.__file__)).startswith(os.path.normcase(os.path.abspath(radice))), ("NON e' l'albero --radice", mod.__file__)
    for m in (FP.__file__, CA.__file__, AC.__file__, BO.__file__, BE.__file__):
        _presidio.avvia(m)
    t0 = STATI[corsa]
    sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE[corsa][0] / s))
    rr = CA.serie(corsa)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == t0]
    assert len(x_st) == 1, "lo stato di %s a %d NON e' uno solo nel jsonl" % (corsa, t0)
    bor = rr[-1]["bordo"]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
        assert int(d["K"]) == K
    with CA.con_L(CA.LCORSA.get(corsa)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, corsa)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, inc, mot, par = z["st"], z["inc"], z["mot"], z["par"]
        n, L = inc.n, z["L"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        with np.load(x_st[0]["file"]) as d:
            assert int(d["t"]) == t0
            for k in chiavi:
                st[k][...] = d[k]
        assert V.shas(z) == x_st[0]["sha"], "lo stato NON e' quello registrato"
        g_e, _gn, _r = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(t0 + 1, t0 + N_TICK + 1):
                AC.tick(z, t, K)
                BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v)
        rho = np.zeros(n)
        np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        co = LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)
        conti = {c: math.fsum(co[c].tolist()) for c in ("M", "V", "cin", "cost", "leg", "tot", "vuo")}
        dist = float("nan")
        if corsa in CA.COPPIA:
            v_ = np.arange(n)
            m1, m2 = v_ // L, v_ % L
            x = TO.scarti(m1, m2, bor["c0"][0], bor["c0"][1], L)[:, 0]
            cA, cB = CC.centri_semipiani(rho, m1, m2, L, x, 0.0)
            dist = float(np.hypot(*CC.vettore(cA, cB, L)))
        sh = V.shas(z)
    np.savez(uscita, rho=rho, meta=json.dumps({"radice": radice, "corsa": corsa, "t0": t0, "N": N_TICK, "e_K": e_K, "conti": conti, "d": dist, "sha": sh,
                                                 "flussi_parziali": FP.__file__}))
    print("scritto %s: %s da %d, %d tick; M %r, tot %r, d %r, e_K %r" % (uscita, corsa, t0, N_TICK, conti["M"], conti["tot"], dist, e_K))
    return 0


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def confronta(files):
    sys.path.insert(0, os.path.dirname(_QUI))
    import numpy as np
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("U4, LA RIPRODUZIONE: %d tick col nucleo vecchio e col nucleo unificato dallo stesso stato; la rms di rho relativa < %g, l'energia convertita entro %g" % (N_TICK, TOLL_RHO, TOLL_E))
    print("=" * 130)
    for fv, fn in ((files[0], files[1]), (files[2], files[3])):
        a, b = np.load(fv), np.load(fn)
        mv, mn = json.loads(str(a["meta"])), json.loads(str(b["meta"]))
        assert mv["corsa"] == mn["corsa"] and mv["t0"] == mn["t0"] and mv["N"] == mn["N"]
        c = mv["corsa"]
        rv, rn = a["rho"], b["rho"]
        rms = float(np.sqrt(np.mean((rn - rv) ** 2)) / np.sqrt(np.mean(rv ** 2)))
        albit = bool(np.array_equal(rn, rv)) and mv["sha"] == mn["sha"]
        cv, cn = mv["conti"], mn["conti"]
        conv = cv["tot"] + math.pi * (cv["M"] + cv["V"])
        e_c = abs(cn["tot"] - conv) / abs(cn["tot"])
        e_s = abs(cn["tot"] - cv["tot"]) / abs(cn["tot"])
        print("### %s da %d, %d tick: il vecchio %s, il nuovo %s" % (c, mv["t0"], mv["N"], mv["radice"], mn["radice"]))
        print("    rho: la rms relativa %.3e; AL BIT (rho e gli sha di ogni chiave): %s; la norma vecchio %r nuovo %r; V %r %r" % (rms, albit, cv["M"], cn["M"], cv["V"], cn["V"]))
        print("    la distanza della coppia: vecchio %r nuovo %r" % (mv["d"], mn["d"]))
        print("    tot: vecchio %r, convertito %r, nuovo %r; lo scarto relativo convertito %.3e, senza conversione %.3e; e_K %r -> %r" % (cv["tot"], conv, cn["tot"], e_c, e_s, mv["e_K"], mn["e_K"]))
        esito("%s: la rms di rho relativa < %g" % (c, TOLL_RHO), rms < TOLL_RHO, "%.3e" % rms)
        esito("%s: la norma M e V uguali entro %g" % (c, TOLL_RHO), abs(cn["M"] - cv["M"]) <= TOLL_RHO * abs(cv["M"]) and abs(cn["V"] - cv["V"]) <= TOLL_RHO * abs(cv["V"]), "")
        if c == "C35-pi":
            esito("%s: la distanza della coppia uguale entro %g relativo" % (c, TOLL_RHO), abs(mn["d"] - mv["d"]) <= TOLL_RHO * abs(mv["d"]), "%r %r" % (mv["d"], mn["d"]))
        esito("%s: l'energia CONVERTITA (tot + pi (M + V)) entro %g relativo" % (c, TOLL_E), e_c <= TOLL_E, "%.3e" % e_c)
        esito("%s: l'energia SENZA conversione entro %g relativo" % (c, TOLL_E), e_s <= TOLL_E, "%.3e" % e_s, deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--misura":
        sys.exit(misura(prendi(a, "--radice"), prendi(a, "--corsa"), prendi(a, "--uscita")))
    if a and a[0] == "--confronta":
        sys.exit(confronta(a[1:5]))
    sys.exit("uso: --misura --radice <albero> --corsa <C35-pi|TBS> --uscita <file.npz> | --confronta <vC35> <nC35> <vTBS> <nTBS>")
