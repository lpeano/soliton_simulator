# -*- coding: utf-8 -*-
r"""**LA TABELLA DI `c(t)`: IL VUOTO DI RIFERIMENTO CHE GIRA** *(Luca `2026-11-04` `09:00`, la scelta (a); il task history `doc/TASK_HISTORY/2026-11-03_TB3_bordo_assorbente.md`, sez. 5)*
    python csv/solitone/carta_fase.py > doc/referti_l2/fase_F3.txt
### **La tabella** *(`bordo.tabella_fase`)*: il vuoto `F3` da solo col tick vivo sui `K` tick della rampa piu' `DOPO`; `omega` su quei `DOPO`; **scritta in `db/accensione_lenta/fase_F3.npz`**
*(`c`, `omega`, `K`, `DOPO`; lo sha di `c` nel referto: la corsa `TB3` la legge e lo registra)*. ### **I DEVE:** `OM` `omega = 3 pi / 20` entro `1e-14` *(Luca: se no, FERMO)*; **`C0`** `phi0(t) = c_di(t) F3`
contro il vuoto evoluto DI NUOVO *(una seconda corsa da `F3`, indipendente dalla tabella)* ai tick `TAPPE`, entro `1e-12`; **`C0-F`** *(deve fallire)* `phi0 = F3` fisso contro lo stesso vuoto al tick `TAPPE[-1]`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

DOPO = 1000                    # ### Luca 09:00: almeno 1000 tick dopo la rampa
TOLL_OM = 1e-14                # ### Luca 09:00
TOLL = 1e-12                   # ### Luca 09:00 (C0)
TAPPE = (1, 10, 100, 1000, 6667, 7667)   # ### Luca 09:00
FILE = "fase_F3.npz"

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def main(argv):
    del argv
    import _deriva_congelato as DC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_dal_fondo as SD
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    for m in ("__init__", "accensione", "bordo", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TF3"][0] / s))
    assert TAPPE[-2] == K and TAPPE[-1] == K + DOPO
    print("=" * 130)
    print("LA TABELLA DI c(t) (Luca 09:00, la scelta (a)): %s (s %g, eps %g); K %d DOPO %d; TOLL_OM %g TOLL %g TAPPE %s" % (CA.NOME, s, V.EPS, K, DOPO, TOLL_OM, TOLL, TAPPE))
    print("=" * 130)
    del sol
    with V.scena(s, vuoto, V.EPS) as (_rec, z, _phi0, _pK):
        inc, L = z["inc"], z["L"]
        F3 = SD.fondo_con_fasi(inc, L, tuple(dict(SD.FASI)["F3"]))
        nF = float(np.linalg.norm(F3))
        chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
        salvato = {k: z["st"][k].copy() for k in chiavi}
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            tab, omega = BO.tabella_fase(z, F3, K, DOPO)
            assert all(np.array_equal(z["st"][k], salvato[k]) for k in chiavi), "tabella_fase NON ha rimesso la scena"
            sha = SFM.sha(tab)
            f = os.path.join(CA.DIR_NPZ, FILE)
            np.savez(f.replace(".npz", "_tmp.npz"), c=tab, omega=omega, K=K, dopo=DOPO)
            os.replace(f.replace(".npz", "_tmp.npz"), f)
            print("### LA TABELLA: %d valori (t 0 .. %d); sha %s; scritta in %s" % (len(tab), K + DOPO, sha, f))
            for t in TAPPE:
                print("    c(%5d) = %+.15f %+.15fi  |c| %.15f  arg %+.12e" % (t, tab[t].real, tab[t].imag, abs(tab[t]), np.angle(tab[t])))
            fasi = np.angle(tab[K + 1:] / tab[K:-1])
            print("  ### omega (la media su %d tick da K): %+.17e; scarto max dalla media %.3e; 3 pi / 20 = %+.17e" % (len(fasi), omega, np.abs(fasi - omega).max(), 3 * math.pi / 20))
            esito("DEVE PASSARE: OM omega = 3 pi / 20 entro %g (Luca 09:00: se no, FERMO)" % TOLL_OM, abs(omega - 3 * math.pi / 20) <= TOLL_OM, "%.3e" % abs(omega - 3 * math.pi / 20))
            # ------------------------------------------------------------ C0: il vuoto evoluto di nuovo
            z["st"]["psi_h"][...] = 0.0
            z["st"]["phi_h"][...] = F3
            scarti, ripr, t = [], [], 0
            for tt in TAPPE:
                while t < tt:
                    t += 1
                    AC.tick(z, t, K)
                ph = z["st"]["phi_h"]
                scarti.append(float(np.linalg.norm(ph - BO.c_di(t, tab, K, omega) * F3)) / nF)
                ripr.append(complex(np.vdot(F3, ph) / nF ** 2) == complex(tab[t]))
                print("    tick %5d: |phi - c_di(t) F3| / |F3| %.3e; c della seconda corsa = c della tabella al bit: %s" % (t, scarti[-1], ripr[-1]))
            esito("DEVE PASSARE: C0 phi0(t) = c_di(t) F3 contro il vuoto evoluto di nuovo ai tick %s, entro %g" % (TAPPE, TOLL), max(scarti) <= TOLL, "il peggiore %.3e" % max(scarti))
            fis = float(np.linalg.norm(z["st"]["phi_h"] - F3)) / nF
            esito("DEVE FALLIRE: C0-F phi0 = F3 fisso contro lo stesso vuoto al tick %d, entro %g" % (t, TOLL), not fis <= TOLL, "%.3e" % fis)
            for k in chiavi:
                z["st"][k][...] = salvato[k]
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
