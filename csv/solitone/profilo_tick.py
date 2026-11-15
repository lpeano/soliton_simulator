# -*- coding: utf-8 -*-
r"""**LA PROFILAZIONE DEL TICK** *(Luca `2026-11-15` `12:24` e `12:32`, parte B; SOLO LETTURA, nessun codice del simulatore cambiato)*.

    python csv/solitone/profilo_tick.py > doc/referti_l2/mattone/profilo_tick.txt

**Il mattone di `L 162`** *(`L162_MGU_03000`, `U` dal campo)* **da solo nella scena di S162, il bordo da `R_A 60`; `50` tick col tick di `mattone.Campi`:** **COL lapse = il mondo (MGU)** *(G+U: il punto fisso
di `cs`)*; **SENZA = il mondo (MU)** *(solo U, `N = 1`: mia lettura di «senza il lapse», dichiarata)*. **`cProfile`** *(`line_profiler` NON c'e' nell'ambiente delle corse: non si installa niente)*: **le prime `15` funzioni
per tempo proprio; la frazione del tempo in `tick_lapse.cs_al_centro`** *(il tempo cumulato contro quello di tutti i tick)*; **la frazione dei nodi in cui `|N - 1| > 1e-12`** *(al tick `0` e al `50`)*.
### **La macchina e' CARICA** *(le corse lunghe in giro)*: **le misure in FRAZIONI, non in secondi assoluti.**
"""
import cProfile
import io
import json
import os
import pstats
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

N_TICK = 50
SOGLIA_N = 1e-12


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    from solitone import tick_lapse as TL
    for m in ("mattone", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    t_s = int(ct["t"])
    print("=" * 130)
    print("LA PROFILAZIONE DEL TICK (Luca 12:24, 12:32 B): %s da solo nella scena di S162, il bordo da R_A %g; %d tick COL lapse (MGU) e SENZA (MU); cProfile; la macchina CARICA: le FRAZIONI" % (ct["file"], MTR.R_A_SCENA, N_TICK))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        with np.load(ct["file"]) as d:
            dati = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
        for caso in ("MGU", "MU"):
            Z["metti"](dati)
            C = MT.Campi(Z, caso, rho_c, e)
            C.campo.A[...] = A0
            C.campo.E[...] = E0
            C.campo.e = e
            C.e_prec = e
            U1.scrivi_U(Z["mot"], C.campo)
            fr = []
            if caso == "MGU":
                N = TL.N_di(MT.rho_di(Z), C.legge)
                fr.append(float(np.mean(np.abs(N - 1.0) > SOGLIA_N)))
            pr = cProfile.Profile()
            pr.enable()
            for k in range(1, N_TICK + 1):
                C.tick(k, t_s + k, 1.0, e)
            pr.disable()
            if caso == "MGU":
                N = TL.N_di(MT.rho_di(Z), C.legge)
                fr.append(float(np.mean(np.abs(N - 1.0) > SOGLIA_N)))
            st = pstats.Stats(pr)
            tot = st.total_tt
            cum_tick = max(v[3] for (f, _l, nome), v in st.stats.items() if nome == "tick" and os.path.basename(f) == "mattone.py")     # ### Campi.tick
            cs = [v for (f, _l, nome), v in st.stats.items() if nome == "cs_al_centro"]
            print("-" * 130)
            print("### (%s) %s: il tempo totale del profilo %.2f s (%d tick, %.3f s per tick, la macchina CARICA); il tick (Campi.tick, cumulato) %.2f s" % (caso, "COL lapse" if caso == "MGU" else "SENZA lapse", tot, N_TICK, tot / N_TICK, cum_tick))
            if cs:
                print("    LA FRAZIONE DEL TEMPO NEL PUNTO FISSO DEL LAPSE (tick_lapse.cs_al_centro, cumulato / il tick): %.4f (%.2f s su %.2f)" % (cs[0][3] / cum_tick, cs[0][3], cum_tick))
            if fr:
                print("    LA FRAZIONE DEI NODI con |N - 1| > %g: al tick 0 %.4f, al tick %d %.4f (%d nodi)" % (SOGLIA_N, fr[0], N_TICK, fr[1], Z["n"]))
            s = io.StringIO()
            pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(15)
            righe = [r for r in s.getvalue().splitlines() if r.strip()]
            i = next(j for j, r in enumerate(righe) if "ncalls" in r)
            print("    LE PRIME 15 FUNZIONI PER TEMPO PROPRIO (tottime; la frazione del totale accanto):")
            print("      %8s %s" % ("frazione", righe[i]))
            for r in righe[i + 1:i + 16]:
                p = r.split()
                try:
                    q = float(p[1]) / tot
                except (ValueError, IndexError):
                    q = float("nan")
                print("      %8.4f %s" % (q, r))
        Z["metti"]()
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
