# -*- coding: utf-8 -*-
r"""**S5.1: IL DEVE DEL BANCO DEL LAPSE** *(sul ramo laterale; Luca `2026-11-11` `13:22`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.13`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_banco.py > doc/referti_l2/s5_banco.txt

**La scena di `TBS` a `10000`** *(lo stato e il suo sha)*. **DEVE:** `tick_lapse.tick` con `N = 1` costante ridà `tick_lapse.tick_di_oggi` *(`mot.cs = s`, `mot.lambda_c = None`)* **AL BIT** per `1000` tick
*(lo sha1 di `psi_h` e `phi_h` ai tick `1`, `10`, `100`, `1000`)*. **DEVE FALLIRE:** con `rho_c = 1e6` lo sha differisce gia' al tick `1`. **Accanto:** `E_N` all'inizio, e i giri dei punti fissi.
"""
import hashlib
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402

N_TICK = 1000                    # ### Luca: 1000 tick
FERMI = (1, 10, 100, 1000)       # ### sez. 31.13
RHO_C_F = 1e6                    # ### sez. 31.13: il DEVE FALLIRE
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def sha(a):
    return hashlib.sha1(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import tick_lapse as TL
    for m in ("__init__", "corsa_accensione", "carta_punto_fisso", "tick_lapse"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0 = CA.serie(CPF.CORSA)[0]
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    t00 = time.time()
    print("=" * 130)
    print("S5.1 (sez. 31.13): il banco del lapse con N = 1 contro il tick di oggi (cs = s = %g, lambda_c None), %d tick, gli sha ai tick %s; il DEVE FALLIRE rho_c %g" % (s, N_TICK, FERMI, RHO_C_F))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par = z["st"], z["mot"], z["par"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        xs = stati[CPF.TICK_D4]

        def carica():
            for k in chiavi:
                st[k][...] = salvato[k]
            with np.load(xs["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            carica()
            print("### lo stato %s: E_N con N = 1 (= s H) %.10e; con rho_c %g %.10e" % (os.path.basename(xs["file"]), TL.energia(mot, st, par, s, ("uno",)), RHO_C_F, TL.energia(mot, st, par, s, ("rho_c", RHO_C_F))))
            ogg, ban = {}, {}
            t0 = time.time()
            for k in range(1, N_TICK + 1):
                TL.tick_di_oggi(mot, st, par, s)
                if k in FERMI:
                    ogg[k] = (sha(st["psi_h"]), sha(st["phi_h"]))
            t_o = time.time() - t0
            carica()
            t0 = time.time()
            giri = []
            for k in range(1, N_TICK + 1):
                g = TL.tick(mot, st, par, s, ("uno",))
                giri.append(g["giri_cs"])
                if k in FERMI:
                    ban[k] = (sha(st["psi_h"]), sha(st["phi_h"]))
            t_b = time.time() - t0
            print("### il tick di oggi %.0f s; il banco con N = 1 %.0f s (i giri del punto fisso di cs: da %d a %d)" % (t_o, t_b, min(giri), max(giri)))
            for k in FERMI:
                print("    tick %4d: oggi psi %s phi %s; il banco psi %s phi %s" % (k, ogg[k][0], ogg[k][1], ban[k][0], ban[k][1]))
            esito("S5.1: il banco con N = 1 = il tick di oggi AL BIT ai tick %s (psi_h e phi_h)" % (FERMI,), all(ogg[k] == ban[k] for k in FERMI))
            carica()
            g = TL.tick(mot, st, par, s, ("rho_c", RHO_C_F))
            f1 = (sha(st["psi_h"]), sha(st["phi_h"]))
            print("### il DEVE FALLIRE: rho_c %g, un tick: psi %s phi %s; i giri: cs %d, la reazione %d e %d" % (RHO_C_F, f1[0], f1[1], g["giri_cs"], g["giri_r1"], g["giri_r2"]))
            esito("S5.1-F: con rho_c %g lo stato al tick 1 = quello del tick di oggi al bit" % RHO_C_F, f1 == ogg[1], "", deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
