# -*- coding: utf-8 -*-
r"""**LA PROFILAZIONE FINE DEL TICK: LE FUNZIONI DEL NUCLEO** *(Luca `2026-11-15` `15:50`, M2 (a); SOLO LETTURA, nessun codice cambiato)*.

    python csv/solitone/profilo_nucleo.py > doc/referti_l2/mattone/profilo_nucleo.txt

**Il mattone di `L 162`** *(`L162_MGU_03000`, `U` dal campo)* **da solo nella scena di S162, il bordo da `R_A 60`, G+U, `20` tick col tick di `mattone.Campi`, `cProfile`.** **Stampa:** **(1) le funzioni di `primo_ordine/`** *(il nucleo)* **e di
`csv/solitone/tick_lapse.py`, `p6_bracci.py`, `p6_u_breve.py`, `_u1_oggi.py`, `_u1_prototipo.py`, ordinate per tempo PROPRIO, coi conteggi; (2) le stesse per tempo CUMULATO; (3) per le funzioni native che pesano** *(`gssv`, `ufunc.at`,
`ndarray.take`, `einsum`, `ufunc.reduce`)* **CHI le chiama** *(`print_callers`)*. **Le frazioni del tempo totale; la macchina CARICA.**
"""
import cProfile
import io
import json
import os
import pstats
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

N_TICK = 20
DOVE = ("primo_ordine", "tick_lapse.py", "p6_bracci.py", "p6_u_breve.py", "_u1_oggi.py", "_u1_prototipo.py", "bordo.py")
NATIVE = ("gssv", "'at' of 'numpy.ufunc'", "'take' of 'numpy.ndarray'", "c_einsum", "'reduce' of 'numpy.ufunc'")


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    for m in ("mattone", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    t_s = int(ct["t"])
    print("=" * 140)
    print("LA PROFILAZIONE FINE DEL TICK (Luca 15:50, M2 (a)): %s, (MGU), %d tick; cProfile; le funzioni del nucleo e delle librerie del tick; la macchina CARICA: le FRAZIONI" % (ct["file"], N_TICK))
    print("=" * 140)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        with np.load(ct["file"]) as d:
            Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
        C = MT.Campi(Z, "MGU", rho_c, e)
        C.campo.A[...] = A0
        C.campo.E[...] = E0
        C.campo.e = e
        C.e_prec = e
        U1.scrivi_U(Z["mot"], C.campo)
        pr = cProfile.Profile()
        pr.enable()
        for k in range(1, N_TICK + 1):
            C.tick(k, t_s + k, 1.0, e)
        pr.disable()
        Z["metti"]()
    st = pstats.Stats(pr)
    tot = st.total_tt
    print("### il tempo totale %.2f s, %.3f s per tick" % (tot, tot / N_TICK))
    righe = [(f, l, n, v) for (f, l, n), v in st.stats.items() if any(x in f for x in DOVE)]
    for titolo, chiave in (("(1) PER TEMPO PROPRIO", 2), ("(2) PER TEMPO CUMULATO", 3)):
        print("-" * 140)
        print("### %s: le funzioni del nucleo e delle librerie del tick (le prime 30); la frazione del totale" % titolo)
        print("    %8s %8s %10s %10s  %s" % ("frazione", "chiamate", "proprio s", "cumul. s", "la funzione"))
        for f, l, n, v in sorted(righe, key=lambda x: -x[3][chiave])[:30]:
            print("    %8.4f %8d %10.3f %10.3f  %s:%d(%s)" % (v[chiave] / tot, v[1], v[2], v[3], os.path.relpath(f, os.path.dirname(_CSV)) if os.path.isabs(f) else f, l, n))
    print("-" * 140)
    print("### (3) LE FUNZIONI NATIVE CHE PESANO E CHI LE CHIAMA (pstats.print_callers)")
    for nat in NATIVE:
        s = io.StringIO()
        pstats.Stats(pr, stream=s).sort_stats("tottime").print_callers(re.escape(nat))
        testo = [r for r in s.getvalue().splitlines() if r.strip() and ("<-" in r or "->" in r or ":" in r)]
        print("    --- %s" % nat)
        for r in testo[:14]:
            print("      %s" % r[:200])
    print("=" * 140)
    return 0


if __name__ == "__main__":
    sys.exit(main())
