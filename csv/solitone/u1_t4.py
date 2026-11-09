# -*- coding: utf-8 -*-
r"""**T4, LE CARTE STATICHE DEL CAMPO `U` ATTORNO A `U = I`** *(Luca `2026-11-09` `01:31`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `15`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t4.py > doc/referti_l2/u1_t4.txt

**Il campo libero non compatto** *(`_u1_prototipo.blocchi_campo`, i blocchi del tick `tick_campo`)*; `omega(k) = omega_fotone(bl, t_di(k)) / s` *(la banda del fotone: la fase non di gauge piu' piccola)*.
**L'isotropia con la misura di `carta_isotropia`** *(`cerchi`, `anisotropie`, `pendenza`: `60` cerchi da `0.005 k_M` a `k_M`, `144` direzioni)* **a `s` `0.05`, `0.15`, `0.3`.**
**I DEVE:** `T4-D6` *(la rotazione di `60` gradi sotto `1e-12` assoluti)*; `T4-P` *(la pendenza dell'anisotropia di `omega` = `4` entro `0.5`)*; `T4-P-F` *(DEVE FALLIRE: una dispersione `D2` costruita)*;
`T4-C` *(`omega / (s |k|)` al cerchio piu' piccolo = `1` entro `0.01`)*; `T4-CO` *(il Courant per bisezione = `2 / sqrt 24` entro `1e-6`; `s = 0.45` instabile)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

S_T4 = (0.05, 0.15, 0.3)       # ### sez. 15: 0.15 e' il passo delle corse
P_ATTESA = 4.0                 # ### sez. 15: la mia derivazione (D6: k^6 cos 6 theta in omega^2)
TOLL_UNO = 0.01                # ### come _u1_prototipo.TOLL_UNO
TOLL_CO = 1e-6                 # ### sez. 15
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


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import carta_isotropia as CI
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(os.path.join(_QUI, "carta_isotropia.py"))
    _presidio.avvia(__file__)
    kM = 2 * math.pi / math.sqrt(3.0)
    print("=" * 130)
    print("T4, LE CARTE STATICHE DEL CAMPO U attorno a U = I (Luca 01:31): s %s; k_M %.6f; i cerchi di carta_isotropia (N_K %d, N_TH %d, K_MIN %g, FIT %s, TOLL_P %g, TOLL_D6_ASS %g); P_ATTESA %g"
          % (S_T4, kM, CI.N_K, CI.N_TH, CI.K_MIN, CI.FIT, CI.TOLL_P, CI.TOLL_D6_ASS, P_ATTESA))
    print("=" * 130)
    # ------------------------------------------------------------------ T4-P-F: la dispersione costruita D2
    kk_f, out_f = CI.cerchi(lambda k: float(np.hypot(*k)) * (1.0 + 0.1 * float(np.hypot(*k)) ** 2 * math.cos(2 * math.atan2(k[1], k[0]))), kM, "D2")
    pf, nf = CI.pendenza(kk_f, np.array([o["a_om"] for o in out_f]))
    esito("T4-P-F la dispersione COSTRUITA omega = k (1 + 0.1 k^2 cos 2 theta) (D2): la pendenza dell'anisotropia = %g entro %g" % (P_ATTESA, CI.TOLL_P),
          abs(pf - P_ATTESA) <= CI.TOLL_P, "%.3f su %d raggi" % (pf, nf), deve=False)
    for s in S_T4:
        bl, fuori, ricostr = U1.blocchi_campo(s)
        print("### s %.2f: i blocchi oltre +-%d celle %.1e, la ricostruzione %.1e" % (s, U1.SUPPORTO, fuori, ricostr))

        def om(k):
            return U1.omega_fotone(bl, *U1.t_di(float(k[0]), float(k[1]))) / s
        kk, out = CI.cerchi(om, kM, "U s %g" % s)
        print("  %9s %9s %14s %12s %12s %10s %12s %12s %12s" % ("|k|/k_M", "lambda", "omega/(s|k|)", "an. omega", "an. |v_g|", "6 lobi", "fase6 (gr)", "rot 60", "non-6"))
        for i, (kr, o) in enumerate(zip(kk, out)):
            if i % 3 == 0 or i == len(kk) - 1:
                print("  %9.4f %9.2f %14.10f %12.3e %12.3e %10.3e %+12.2f %12.3e %12.3e" % (kr, 2 * math.pi / (kr * kM), o["media"] / (kr * kM), o["a_om"], o["a_v"], o["lobi6"], o["fase6"], o["rot"], o["non6"]))
        rot = max(max(o["rot"], o["non6"]) for o in out)
        esito("T4-D6 s %.2f: omega(theta + 60) = omega(theta) e le armoniche non multiple di 6, sotto %g assoluti, su ogni cerchio" % (s, CI.TOLL_D6_ASS), rot <= CI.TOLL_D6_ASS, "%.3e" % rot)
        p, n = CI.pendenza(kk, np.array([o["a_om"] for o in out]))
        esito("T4-P s %.2f: la pendenza di ln an.omega contro ln |k| fra %s k_M = %g entro %g" % (s, CI.FIT, P_ATTESA, CI.TOLL_P), abs(p - P_ATTESA) <= CI.TOLL_P, "%.3f su %d raggi" % (p, n))
        c0 = out[0]["media"] / (kk[0] * kM)
        esito("T4-C s %.2f: omega / (s |k|) al cerchio piu' piccolo (|k| %.4f k_M) = 1 entro %g" % (s, kk[0], TOLL_UNO), abs(c0 - 1.0) <= TOLL_UNO, "%.10f" % c0)
        for chi in ("a_om", "a_v"):
            aa = np.array([o[chi] for o in out])
            pezzi = []
            for sg in CI.SOGLIE:
                sopra = np.flatnonzero(aa > sg)
                pezzi.append("%g: %s" % (sg, ("lambda %.2f nodi (|k|/k_M %.4f)" % (2 * math.pi / (kk[sopra[0]] * kM), kk[sopra[0]])) if len(sopra) else "mai entro k_M"))
            print("  STAMPA s %.2f, %s: l'anisotropia supera la soglia a %s" % (s, "omega" if chi == "a_om" else "|v_g|", "; ".join(pezzi)))
    # ------------------------------------------------------------------ T4-CO: il Courant (le righe di _u1_prototipo.parte_F)
    bl45, _f, _r = U1.blocchi_campo(U1.S_COURANT)
    inst45, dove45 = U1.max_instabile(bl45, U1.L_COURANT)
    esito("T4-CO-F s %.2f STABILE (max|lambda| fuori dalla gauge <= 1 + %g)" % (U1.S_COURANT, U1.INSTABILE), inst45 <= 1.0 + U1.INSTABILE, "max|lambda| %.6f a %s" % (inst45, dove45), deve=False)
    lo, hi = U1.S_STABILE, U1.S_COURANT
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        bl, _, _ = U1.blocchi_campo(mid)
        if U1.max_instabile(bl, 6)[0] > 1.0 + U1.INSTABILE:
            hi = mid
        else:
            lo = mid
    car = 2.0 / math.sqrt(24.0)
    esito("T4-CO il Courant per bisezione (griglia 6x6, Gamma compreso) = 2/sqrt(24) entro %g" % TOLL_CO, abs(0.5 * (lo + hi) - car) <= TOLL_CO, "fra %.8f e %.8f, la carta %.8f" % (lo, hi, car))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
