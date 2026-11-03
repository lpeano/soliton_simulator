# -*- coding: utf-8 -*-
r"""**`B0`, PRIMA DEL BORDO ASSORBENTE: IL VUOTO `F3` DA SOLO E' FERMO SOTTO IL TICK VIVO?** *(Luca `21:52`; il task history `doc/TASK_HISTORY/2026-11-03_TB3_bordo_assorbente.md`)*
    python csv/solitone/carta_b0.py > doc/referti_l2/b0_vuoto_F3.txt
### **Il bordo riporta `phi` verso `phi0`:** se `F3` da solo non e' fermo, un `phi0` fisso FORZA il vuoto della fascia. ### **La misura:** `psi = 0`, `phi = F3`, il tick vivo *(`AC.tick`,
la rampa di `TP1000`, poi il tick intero)*; ai tick di `TAPPE`: `c = <F3, phi> / |F3|^2`, `|phi - c F3| / |F3|`, `|c|`, `arg c`, l'uniformita' di `Lambda` *(std / media)*; dopo la rampa la fase per tick
`arg(c(t+1) / c(t))`. ### **I tre casi** *(il task history)*: (1) fermo; (2) fermo a meno di una fase; (3) non fermo. ### **E il costo** di un libro dei conti *(`LC.conti_per_nodo`)* contro un tick.
### **I DEVE:** `B0-P` *(il controllo positivo)* con una materia piccola *(la partenza di `TP1000` scalata di `1e-3`)* il vuoto NON resta `F3` entro `TOLL` dopo `TAPPE[-1]` tick *(se restasse, la misura non
legge il vuoto)*. ### **La decisione dal referto e' di Luca** per il caso (2) *(la mia proposta)* e (3).
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL = 1e-12                   # ### come test_simmetrica
DOPO = (1, 10, 100, 1000)      # ### i tick dopo la rampa (dichiarati)
DENTRO = (1, 10, 100, 1000)    # ### i tick nella rampa (dichiarati)
SCALA_P = 1e-3                 # ### B0-P: la materia piccola del controllo positivo

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
    import _libro_dei_conti as LC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_dal_fondo as SD
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    for m in ("__init__", "accensione", "corsa_accensione", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TP1000"][0] / s))
    print("=" * 130)
    print("B0: IL VUOTO F3 DA SOLO SOTTO IL TICK VIVO (Luca 21:52, prima del bordo): %s (s %g, eps %g); K %d; DENTRO %s DOPO %s; TOLL %g SCALA_P %g" % (CA.NOME, s, V.EPS, K, DENTRO, DOPO, TOLL, SCALA_P))
    print("  i tre casi (il task history): (1) fermo, phi0 = F3; (2) fermo a meno di una fase, phi0(t) = c(t) F3 (la mia proposta, da confermare); (3) non fermo: FERMO")
    print("=" * 130)
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        inc, L = z["inc"], z["L"]
        chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
        salvato = {k: z["st"][k].copy() for k in chiavi}
        p0, _info = V.partenza(sol, z, phi0, pK, s)
        for k in chiavi:
            z["st"][k][...] = salvato[k]
        F3 = SD.fondo_con_fasi(inc, L, tuple(dict(SD.FASI)["F3"]))
        n3 = float(np.vdot(F3, F3).real)

        def leggi(t):
            ph = z["st"]["phi_h"]
            c = complex(np.vdot(F3, ph) / n3)
            r = float(np.linalg.norm(ph - c * F3) / np.sqrt(n3))
            la = P.densita_nodo(z, ph[:, None]) if ph.ndim == 1 else None
            u = float(la.std() / la.mean()) if la is not None else float("nan")
            return c, r, u

        def avvia(psi):
            for k in chiavi:
                z["st"][k][...] = salvato[k]
            z["st"]["psi_h"][...] = psi
            z["st"]["phi_h"][...] = F3

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ------------------------------------------------------------ il vuoto da solo
            avvia(np.zeros_like(p0))
            righe, t, c_prec, peggio = [], 0, None, 0.0
            tappe = sorted(set(DENTRO) | {K} | {K + d for d in DOPO})
            fasi = []
            s0 = time.time()
            for tt in tappe:
                while t < tt:
                    t += 1
                    AC.tick(z, t, K)
                    if t > K and t <= K + DOPO[-1]:
                        c, _r, _u = leggi(t)
                        if c_prec is not None:
                            fasi.append(np.angle(c / c_prec))
                        c_prec = c
                c, r, u = leggi(t)
                peggio = max(peggio, r)
                righe.append((t, c, r, u))
            secondi = (time.time() - s0) / t
            print("### IL VUOTO F3 DA SOLO (psi = 0): ai tick %s" % tappe)
            for t_, c, r, u in righe:
                print("    tick %6d (lam %.6f): c = %+.15f %+.15fi  |c| %.15f  arg c %+.6e  |phi - c F3| / |F3| %.3e  Lambda std/media %.3e"
                      % (t_, AC.lam_di(t_, K), c.real, c.imag, abs(c), np.angle(c), r, u))
            fasi = np.array(fasi)
            if len(fasi):
                print("  ### dopo la rampa, la fase per tick arg(c(t+1)/c(t)) su %d tick: media %+.15e, scarto max dalla media %.3e" % (len(fasi), fasi.mean(), np.abs(fasi - fasi.mean()).max()))
            fermo = all(abs(c - 1) <= TOLL and r <= TOLL for _t, c, r, _u in righe)
            fase = all(r <= TOLL and abs(abs(c) - 1) <= TOLL for _t, c, r, _u in righe)
            caso = 1 if fermo else (2 if fase else 3)
            print("  ### IL CASO: (%d) %s; il peggiore |phi - c F3| / |F3| %.3e" % (caso, {1: "F3 FERMO", 2: "F3 fermo a meno di una fase", 3: "F3 NON fermo nemmeno a meno di una fase"}[caso], peggio))
            # ------------------------------------------------------------ il controllo positivo
            avvia(SCALA_P * p0)
            for t in range(1, tappe[-1] + 1):
                AC.tick(z, t, K)
            c, r, _u = leggi(t)
            esito("DEVE PASSARE: B0-P con la materia piccola (la partenza x %g) il vuoto dopo %d tick NON e' piu' c F3 entro %g (la misura legge il vuoto)" % (SCALA_P, t, TOLL),
                  r > TOLL, "|phi - c F3| / |F3| %.3e" % r)
            # ------------------------------------------------------------ il costo del libro dei conti
            e_K = P.e_K(z)
            t1 = time.time()
            LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"])
            libro = time.time() - t1
        for k in chiavi:
            z["st"][k][...] = salvato[k]
    print("  ### il costo: un tick %.4f s (la media su %d tick del vuoto da solo); un libro dei conti %.4f s (%.1f tick)" % (secondi, tappe[-1], libro, libro / secondi))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s; IL CASO (%d)" % (OK[0], OK[1], len(FALLITE), FALLITE, caso))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
