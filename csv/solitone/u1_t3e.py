# -*- coding: utf-8 -*-
r"""**T3, d5', d6', d7: LA SORGENTE SPENTA SU UN CAMPO ACCESO, LA MISURA ASSOLUTA, `J` BILINEARE** *(Luca `2026-11-08` `17:57`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `14.9`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t3e.py > doc/referti_l2/u1_t3e.txt

### **La scena e lo stato di `u1_t3d`** *(`TBS` al tick `100000`, `e*` rifatto, non compatto)*. **`G6` = `N_D` avanti, `T`, `N_D` avanti, `T`.**
**(d5')** `N_D` tick con la sorgente *(il campo maturo)*, poi da li' `G6` a sorgente SPENTA, e lo stesso a sorgente accesa. **(d6')** l'errore ASSOLUTO `max|psi - psi0|`, `max|phi - phi0|`,
col campo e senza, alla stessa norma `x 1e-3, 1e-1, 1`, e il loro rapporto. **(d7)** `J` dalla forma BILINEARE *(`sin^2(theta/2)(|w1|^2 - |v0|^2) + 2 Re(conj(alpha) beta <v0, w1>)`,
dallo stato PRIMA del pezzo)* **in un `avvolto` di questo script** *(`_u1_prototipo` non si tocca)*; **il servizio:** `J` bilineare = `J` di oggi su un tick entro `64 eps rho_max`;
**il DEVE:** `G6` col campo e la `J` bilineare sotto `1.33e-12` o entro `2` volte (0); **il DEVE FALLIRE:** la forma vecchia.
"""
import contextlib
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TICK0 = 100000
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
E0_PROVA = 0.1
EB_MODERATO = 0.1
F_NORMA = (1e-3, 1e-1, 1.0)    # ### Luca 17:57 (d6')
FATTORE = 2.0                  # ### il criterio del braccio di controllo (sez. 14.5): entro 2 volte (0)
VICINO = 10.0                  # ### come u1_t3c, u1_t3d
SERVIZIO_ULP = 64.0            # ### mio, dichiarato: J bilineare = J di oggi entro 64 eps rho_max
EPS = float(np.finfo(float).eps)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


@contextlib.contextmanager
def avvolto_bilineare(mot, campo, sorgente, registro=None):
    """### **`_u1_prototipo.avvolto` con la `J` BILINEARE:** la sorgente dallo stato PRIMA del pezzo; la deriva come l'originale *(dopo il PRIMO `spostamento_scalare`)*."""
    import flussi_parziali as FP
    import _u1_prototipo as U1
    op = mot.operatori
    vero_sp, vero_sv = op["spostamento_trasporto"], op["spostamento_scalare"]
    conta = [0]
    m = campo.m

    def sp(st, par, fr):
        v = st["psi_h"].reshape(m, 2, 2)
        v0, v1 = v[:, 0, :], v[:, 1, :]
        w1 = np.einsum("aji,aj->ai", np.conj(mot.geo.U), v1)
        z = FP.z_arco(mot, fr).reshape(-1).copy()
        al, be = (1.0 + z) / 2.0, (1.0 - z) / 2.0
        J = (np.abs(be) ** 2) * (np.sum(np.abs(w1) ** 2, axis=1) - np.sum(np.abs(v0) ** 2, axis=1)) \
            + 2.0 * np.real(np.conj(al) * be * np.sum(np.conj(v0) * w1, axis=1))
        prima = np.sum(np.abs(v0) ** 2, axis=1)
        out = vero_sp(st, par, fr)
        if registro is not None:
            registro.append((J, np.sum(np.abs(v[:, 0, :]) ** 2, axis=1) - prima))
        if sorgente:
            campo.E -= campo.e * J
        return out

    def sv(st, par, fr):
        out = vero_sv(st, par, fr)
        conta[0] += 1
        if conta[0] % 2 == 1:
            campo.deriva(0.5)
            campo.deriva(0.5)
            U1.scrivi_U(mot, campo)
        return out
    op["spostamento_trasporto"], op["spostamento_scalare"] = sp, sv
    try:
        yield
    finally:
        op["spostamento_trasporto"], op["spostamento_scalare"] = vero_sp, vero_sv


def main():
    import _deriva_congelato as DC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _u1_prototipo as U1
    from solitone import _u1_oggi as UO
    from solitone import accensione as AC
    for m in ("__init__", "_u1_oggi", "accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    N_D = U1.N_D
    tol = 2 * N_D * 6.0 * EPS
    print("=" * 130)
    print("T3, d5', d6', d7 (Luca 17:57): %s; N_D %d; le norme %s; la soglia assoluta %.3e; il fattore del braccio di controllo %g" % (FILE_LIB, N_D, F_NORMA, tol, FATTORE))
    print("=" * 130)
    with UO.scena(E0_PROVA, "noncompatto") as (z, campo, K, s):
        st, mot, inc = z["st"], z["mot"], z["inc"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def carica():
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]

        def scala(f):
            st["psi_h"][...] = st["psi_h"] * math.sqrt(f)
            r = np.zeros(inc.n)
            np.add.at(r, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            st["rho"][...] = r

        def un_tick(t, c, sorgente, bil):
            if c is None:
                AC.tick(z, t, K)
                return
            c.spinta(0.5)
            with (avvolto_bilineare(mot, c, sorgente) if bil else U1.avvolto(mot, c, sorgente)):
                AC.tick(z, t, K)
            c.spinta(0.5)

        def avanti(c, n, t0, sorgente, bil, eb=None):
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                for t in range(t0 + 1, t0 + n + 1):
                    un_tick(t, c, sorgente, bil)
                    if eb is not None:
                        eb[0] = max(eb[0], float(np.max(np.abs(c.e * c.B()))))

        def T_(c):
            if c is None:
                psi = st["psi_h"]
                psi[...] = np.conj(psi[:, ::-1]).copy()
                st["phi_h"][...] = np.conj(st["phi_h"]).copy()
            else:
                UO.rovescia(st, mot, c)

        def G6(c, sorgente, bil):
            """dallo stato CORRENTE: (relativo, assoluto psi, assoluto phi)."""
            psi0, phi0 = st["psi_h"].copy(), st["phi_h"].copy()
            avanti(c, N_D, TICK0, sorgente, bil)
            T_(c)
            avanti(c, N_D, TICK0 + N_D, sorgente, bil)
            T_(c)
            return (max(U1.rel(psi0, st["psi_h"]), U1.rel(phi0, st["phi_h"])),
                    float(np.max(np.abs(psi0 - st["psi_h"]))), float(np.max(np.abs(phi0 - st["phi_h"]))))

        # ------------------------------------------------------------ (0), e*
        UO.scrivi_U(mot, UO.campo_della_scena(z, 0.0, "noncompatto"))
        carica()
        r0 = G6(None, True, False)
        print("  (0) SENZA il campo: relativo %.3e; assoluto psi %.3e phi %.3e" % r0)
        eb0 = [0.0]
        carica()
        c0 = UO.campo_della_scena(z, E0_PROVA, "noncompatto")
        avanti(c0, N_D, TICK0, True, False, eb=eb0)
        e_star = E0_PROVA * math.sqrt(EB_MODERATO / eb0[0])
        print("  e* = %g sqrt(%g / %.4e) = %.6e (come u1_t3b)" % (E0_PROVA, EB_MODERATO, eb0[0], e_star))
        # ------------------------------------------------------------ (d5') il campo acceso, poi la sorgente spenta
        carica()
        c5 = UO.campo_della_scena(z, e_star, "noncompatto")
        avanti(c5, N_D, TICK0 - N_D, True, False)
        maturo = ({k: st[k].copy() for k in chiavi}, c5.A.copy(), c5.E.copy())
        print("  (d5') il campo dopo %d tick con la sorgente: max|A| %.3e max|E| %.3e max|e B| %.3e" % (N_D, float(np.max(np.abs(c5.A))), float(np.max(np.abs(c5.E))), float(np.max(np.abs(c5.e * c5.B())))))

        def da_maturo(c):
            for k in chiavi:
                st[k][...] = maturo[0][k]
            c.A[...], c.E[...] = maturo[1], maturo[2]
            UO.scrivi_U(mot, c)
        res5 = {}
        for sorg in (False, True):
            c = UO.campo_della_scena(z, e_star, "noncompatto")
            da_maturo(c)
            res5[sorg] = G6(c, sorg, False)
            print("  (d5') dal campo maturo, la sorgente %s: relativo %.3e; assoluto psi %.3e phi %.3e" % ((("ACCESA" if sorg else "SPENTA"),) + res5[sorg]))
            sys.stdout.flush()
        # ------------------------------------------------------------ (d6') la misura assoluta alla stessa norma
        res6 = {}
        for f in F_NORMA:
            carica()
            if f != 1.0:
                scala(f)
            senza = G6(None, True, False)
            carica()
            if f != 1.0:
                scala(f)
            con = G6(UO.campo_della_scena(z, e_star, "noncompatto"), True, False)
            res6[f] = (con, senza)
            print("  (d6') la norma x %g: assoluto psi col campo %.3e senza %.3e (rapporto %.2f); phi col %.3e senza %.3e (rapporto %.2f)"
                  % (f, con[1], senza[1], con[1] / senza[1], con[2], senza[2], con[2] / senza[2] if senza[2] > 0 else float("inf")))
            sys.stdout.flush()
        # ------------------------------------------------------------ (d7) J bilineare
        reg = []
        carica()
        cS = UO.campo_della_scena(z, e_star, "noncompatto")
        a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
        with a_, b_:
            cS.spinta(0.5)
            with avvolto_bilineare(mot, cS, False, reg):
                AC.tick(z, TICK0 + 1, K)
            cS.spinta(0.5)
        rmax = float(np.max(st["rho"]))
        d_serv = max(float(np.max(np.abs(a - b))) for a, b in reg)
        carica()
        r7 = G6(UO.campo_della_scena(z, e_star, "noncompatto"), True, True)
        carica()
        r7v = G6(UO.campo_della_scena(z, e_star, "noncompatto"), True, False)
        print("  (d7) il servizio: J bilineare contro J di oggi su un tick, %d spostamenti: max|dJ| %.3e (rho_max %.3e, %.1f eps rho_max)" % (len(reg), d_serv, rmax, d_serv / (EPS * rmax)))
        print("  (d7) G6 col campo a e* e la J BILINEARE: relativo %.3e; assoluto psi %.3e phi %.3e" % r7)
        print("  (d7) G6 col campo a e* e la J di OGGI: relativo %.3e; assoluto psi %.3e phi %.3e" % r7v)
    print("=" * 130)
    l5 = res5[False][0] <= VICINO * tol
    print("  LA LETTURA (d5', Luca 17:57): %s" % ("la sorgente: spenta su un campo acceso, G6 torna vicino alla soglia" if l5 else "NON la sorgente sola: spenta su un campo acceso, G6 resta lontano"))
    esito("DEVE PASSARE: d7-S la J bilineare = la J di oggi su un tick entro %g eps rho_max" % SERVIZIO_ULP, d_serv <= SERVIZIO_ULP * EPS * rmax, "%.1f eps rho_max" % (d_serv / (EPS * rmax)))
    esito("DEVE PASSARE: d7 G6 su TBS col campo a e* e la J bilineare sotto %.2e o entro %g volte (0)" % (tol, FATTORE), r7[0] <= tol or r7[0] <= FATTORE * r0[0], "%.3e (0: %.3e)" % (r7[0], r0[0]))
    esito("DEVE FALLIRE: d7-F la J di oggi: sotto %.2e o entro %g volte (0)" % (tol, FATTORE), not (r7v[0] <= tol or r7v[0] <= FATTORE * r0[0]), "%.3e" % r7v[0])
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
