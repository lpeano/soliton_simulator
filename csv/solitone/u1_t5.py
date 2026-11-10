# -*- coding: utf-8 -*-
r"""**T5 (A), IL LIMITE DELLA MATERIA A VUOTO NULLO** *(Luca `2026-11-10` `01:22`: T5 chiuso per derivazione, si fa solo (A); il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `25.3`, `25.4`)*. [[PIANO-2D-3D]] [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t5.py > doc/referti_l2/u1_t5.txt

**`v_max/s` e `v_b/s`** *(`u1_p1.vb`: le funzioni di P1)* **a `s` in `_u1_terzo.S_VAR` piu' `0.15`, `eps` `0` e `0.5`; il limite a `s -> 0`** *(l'intercetta del fit di grado `2` sui punti di `S_VAR`)* **e la dispersione fra i gradi `1`-`3`.**
**`v_b` stampato, senza letture** *(dipende dallo zero, P1)*. **T5-R** *(`0.588137` a `s 0.15`, `eps 0.5`, entro `1e-6`)*; **T5-F** *(DEVE FALLIRE: contro `0.588137 + 1e-5`)*.
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

S_CORSA = 0.15                 # ### sez. 25.4: il passo delle corse, per T5-R
RIF_R = 0.588137               # ### P1 (u1_p1.txt): v_max/s a s 0.15, eps 0.5
TOLL_R = 1e-6                  # ### sez. 25 (T5-R)
SPOSTA_F = 1e-5                # ### sez. 25.4 (T5-F)
GRADI = (1, 2, 3)              # ### sez. 25.3
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


def limite(ss, yy):
    """### Le intercette dei fit di grado `1`, `2`, `3` *(il limite a `s -> 0`)*; il limite e' quella del grado `2`, la dispersione max - min."""
    ic = {g: float(np.polyfit(ss, yy, g)[-1]) for g in GRADI}
    return ic, ic[2], max(ic.values()) - min(ic.values())


def main():
    import _presidio
    import _u1_terzo as U3
    from solitone import u1_p1 as P1
    _presidio.avvia(os.path.join(_QUI, "u1_p1.py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_terzo.py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_triangoli_forza.py"))
    _presidio.avvia(__file__)
    SS = tuple(U3.S_VAR)
    print("=" * 130)
    print("T5 (A), IL LIMITE DELLA MATERIA A VUOTO NULLO (sez. 25.3-25.4): eps %s; s %s piu' %g; il limite col fit di grado 2, la dispersione fra i gradi %s" % (U3.EPS_VAR, SS, S_CORSA, GRADI))
    print("=" * 130)
    t00 = time.time()
    ris = {}
    for eps in U3.EPS_VAR:
        for s in SS + (S_CORSA,):
            t1 = time.time()
            out, vm = P1.vb(eps, s)
            ris[(eps, s)] = (out, vm)
            print("  eps %.1f s %-6g: v_max/s %.8f | v_b/s dei due rami %s (lo zero spostato di +pi s/2: %s; di -pi s/2: %s) | %.0f s"
                  % (eps, s, vm / s, ", ".join("%.6f" % (o[0] / s) for o in out), ", ".join("%.6f" % (o[2][0] / s) for o in out), ", ".join("%.6f" % (o[2][1] / s) for o in out), time.time() - t1))
            sys.stdout.flush()
    print("-" * 130)
    for eps in U3.EPS_VAR:
        ss = np.array(SS)
        vm = np.array([ris[(eps, s)][1] / s for s in SS])
        ic, lim, disp = limite(ss, vm)
        print("  eps %.1f: v_max/s, il limite a s -> 0 (grado 2) %.6f; le intercette %s; la dispersione %.3e" % (eps, lim, ", ".join("grado %d %.6f" % kv for kv in ic.items()), disp))
        for b in range(len(ris[(eps, SS[0])][0])):
            vb = np.array([ris[(eps, s)][0][b][0] / s for s in SS])
            if np.all(np.isfinite(vb)):
                icb, limb, dispb = limite(ss, vb)
                print("  eps %.1f: v_b/s del ramo %d (STAMPATO, senza letture: dipende dallo zero), il limite %.6f; la dispersione %.3e" % (eps, b, limb, dispb))
            else:
                print("  eps %.1f: v_b/s del ramo %d: un fit non definito in qualche s (stampato sopra)" % (eps, b))
    print("-" * 130)
    v15 = ris[(0.5, S_CORSA)][1] / S_CORSA
    esito("T5-R v_max/s a s %g, eps 0.5 = %.6f (P1) entro %g" % (S_CORSA, RIF_R, TOLL_R), abs(v15 - RIF_R) <= TOLL_R, "%.8f (lo scarto %.2e)" % (v15, v15 - RIF_R))
    esito("T5-F lo stesso controllo contro %.6f + %g" % (RIF_R, SPOSTA_F), abs(v15 - (RIF_R + SPOSTA_F)) <= TOLL_R, "lo scarto %.2e" % (v15 - RIF_R - SPOSTA_F), deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
