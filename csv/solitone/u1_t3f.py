# -*- coding: utf-8 -*-
r"""**T3, d6' RIFATTO E d8: IL POTENZIALE CHE CRESCE** *(Luca `2026-11-08` `19:10`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `14.11`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t3f.py > doc/referti_l2/u1_t3f.txt

### **La scena e lo stato di `u1_t3e`** *(`TBS` al tick `100000`, `e*` rifatto)*. **`G6` = `N` avanti, `T`, `N` avanti, `T`, confrontato su `psi` e `phi`.**
**(d6')** l'errore ASSOLUTO col campo e senza alla stessa norma *(`x 1e-3, 1e-1, 1`)*, ### **con `U = I` rimessa prima di ogni braccio senza campo** *(la cura del mio errore di `b2f6e1b4`)*.
**(d8)** `G6` a `N = 10, 30, 100, 300` *(compatto)* **con `max|e A|` accanto**; la lettura di Luca: l'errore cresce con `max|e A|` *(la pendenza log-log fra `0.5` e `2`, mia)*.
**La cura COMPATTA:** `e A` ridotto modulo `2 pi` dopo ogni deriva *(in un `avvolto` di questo script)*; **il DEVE:** `G6` col campo compatto a `e*` e la riduzione entro `2` volte (0);
**il DEVE FALLIRE:** senza la riduzione. **`_u1_prototipo` e `_u1_oggi` non si toccano.**
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
NN_D8 = (10, 30, 100, 300)     # ### Luca 19:10 (d8)
PENDENZA_D8 = (0.5, 2.0)       # ### mia, dichiarata: "circa in proporzione"
FATTORE = 2.0                  # ### il criterio del braccio di controllo (sez. 14.5)
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
def avvolto_ridotto(mot, campo, sorgente):
    """### **`_u1_prototipo.avvolto` con `e A` RIDOTTO modulo `2 pi` dopo la deriva** *(solo per il compatto: Luca `19:10`)*; la sorgente come l'originale."""
    import _u1_prototipo as U1
    assert campo.forma == "compatto", "la riduzione modulo 2 pi e' lecita SOLO nel compatto"
    op = mot.operatori
    vero_sp, vero_sv = op["spostamento_trasporto"], op["spostamento_scalare"]
    conta = [0]
    m = campo.m

    def sp(st, par, fr):
        v = st["psi_h"].reshape(m, 2, 2)
        prima = np.sum(np.abs(v[:, 0, :]) ** 2, axis=1)
        out = vero_sp(st, par, fr)
        J = np.sum(np.abs(v[:, 0, :]) ** 2, axis=1) - prima
        if sorgente:
            campo.E -= campo.e * J
        return out

    def sv(st, par, fr):
        out = vero_sv(st, par, fr)
        conta[0] += 1
        if conta[0] % 2 == 1:
            campo.deriva(0.5)
            campo.deriva(0.5)
            campo.A[...] = (np.mod(campo.e * campo.A + math.pi, 2.0 * math.pi) - math.pi) / campo.e
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
    print("T3, d6' RIFATTO E d8 (Luca 19:10): %s; N_D %d; le norme %s; N di d8 %s; la soglia assoluta %.3e; il fattore %g" % (FILE_LIB, N_D, F_NORMA, NN_D8, tol, FATTORE))
    print("=" * 130)
    with UO.scena(E0_PROVA, "noncompatto") as (z, campo, K, s):
        st, mot, inc = z["st"], z["mot"], z["inc"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def carica(f=1.0):
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]
            if f != 1.0:
                st["psi_h"][...] = st["psi_h"] * math.sqrt(f)
                r = np.zeros(inc.n)
                np.add.at(r, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
                st["rho"][...] = r

        def U_identita():
            UO.scrivi_U(mot, UO.campo_della_scena(z, 0.0, "noncompatto"))     # ### la cura del mio errore: U = I esatto
            assert float(np.max(np.abs(mot.geo.U - np.eye(2)[None]))) == 0.0

        def avanti(c, n, t0, ridotto, eA=None, eb=None):
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                for t in range(t0 + 1, t0 + n + 1):
                    if c is None:
                        AC.tick(z, t, K)
                        continue
                    c.spinta(0.5)
                    with (avvolto_ridotto(mot, c, True) if ridotto else U1.avvolto(mot, c, True)):
                        AC.tick(z, t, K)
                    c.spinta(0.5)
                    if eA is not None:
                        eA[0] = max(eA[0], float(np.max(np.abs(c.e * c.A))))
                    if eb is not None:
                        eb[0] = max(eb[0], float(np.max(np.abs(c.e * c.B()))))

        def T_(c):
            if c is None:
                psi = st["psi_h"]
                psi[...] = np.conj(psi[:, ::-1]).copy()
                st["phi_h"][...] = np.conj(st["phi_h"]).copy()
            else:
                UO.rovescia(st, mot, c)

        def G6(c, n, ridotto):
            """dallo stato CORRENTE: (relativo, assoluto psi, assoluto phi, max|e A|)."""
            psi0, phi0 = st["psi_h"].copy(), st["phi_h"].copy()
            eA = [0.0]
            avanti(c, n, TICK0, ridotto, eA)
            T_(c)
            avanti(c, n, TICK0 + n, ridotto, eA)
            T_(c)
            return (max(U1.rel(psi0, st["psi_h"]), U1.rel(phi0, st["phi_h"])),
                    float(np.max(np.abs(psi0 - st["psi_h"]))), float(np.max(np.abs(phi0 - st["phi_h"]))), eA[0])

        # ------------------------------------------------------------ (0), e*
        U_identita()
        carica()
        r0 = G6(None, N_D, False)
        print("  (0) SENZA il campo: relativo %.3e; assoluto psi %.3e phi %.3e" % r0[:3])
        eb0 = [0.0]
        carica()
        c0 = UO.campo_della_scena(z, E0_PROVA, "noncompatto")
        avanti(c0, N_D, TICK0, False, eb=eb0)
        e_star = E0_PROVA * math.sqrt(EB_MODERATO / eb0[0])
        print("  e* = %g sqrt(%g / %.4e) = %.6e (come u1_t3b)" % (E0_PROVA, EB_MODERATO, eb0[0], e_star))
        # ------------------------------------------------------------ (d6') rifatto: U = I nei bracci senza campo
        for f in F_NORMA:
            U_identita()
            carica(f)
            senza = G6(None, N_D, False)
            carica(f)
            con = G6(UO.campo_della_scena(z, e_star, "noncompatto"), N_D, False)
            print("  (d6') la norma x %g: assoluto psi col campo %.3e senza %.3e (rapporto %.2f); phi col %.3e senza %.3e (rapporto %.2f); relativo col %.3e senza %.3e"
                  % (f, con[1], senza[1], con[1] / senza[1] if senza[1] > 0 else float("inf"), con[2], senza[2], con[2] / senza[2] if senza[2] > 0 else float("inf"), con[0], senza[0]))
            sys.stdout.flush()
        # ------------------------------------------------------------ (d8) la prova: G6 a N crescenti con max|e A|
        prova = []
        for n in NN_D8:
            carica()
            r = G6(UO.campo_della_scena(z, e_star, "compatto"), n, False)
            U_identita()
            carica()
            rz = G6(None, n, False)
            prova.append((n, r[0], r[3], rz[0]))
            print("  (d8) compatto, N %3d: G6 relativo %.3e con max|e A| %.3e (senza campo %.3e)" % (n, r[0], r[3], rz[0]))
            sys.stdout.flush()
        pend = float(np.polyfit(np.log10([p[2] for p in prova]), np.log10([p[1] for p in prova]), 1)[0])
        print("  (d8) la pendenza di log10(G6) contro log10(max|e A|): %.3f" % pend)
        # ------------------------------------------------------------ la cura compatta
        carica()
        rc = G6(UO.campo_della_scena(z, e_star, "compatto"), N_D, True)
        carica()
        rv = G6(UO.campo_della_scena(z, e_star, "compatto"), N_D, False)
        print("  la cura (compatto, e A ridotto modulo 2 pi): G6 relativo %.3e (max|e A| %.3e); senza la riduzione %.3e (max|e A| %.3e)" % (rc[0], rc[3], rv[0], rv[3]))
    print("=" * 130)
    regge = PENDENZA_D8[0] <= pend <= PENDENZA_D8[1]
    print("  LA LETTURA (d8, Luca 19:10): %s" % ("l'errore cresce con max|e A|: l'ipotesi del potenziale che cresce REGGE" if regge else "l'errore NON cresce con max|e A| come previsto: l'ipotesi CADE"))
    esito("DEVE PASSARE: d8 la pendenza log-log di G6 contro max|e A| fra %g e %g" % PENDENZA_D8, regge, "%.3f" % pend)
    esito("DEVE PASSARE: d8-C la cura compatta (e A modulo 2 pi): G6 entro %g volte (0)" % FATTORE, rc[0] <= FATTORE * r0[0], "%.3e (0: %.3e)" % (rc[0], r0[0]))
    esito("DEVE FALLIRE: d8-F senza la riduzione: G6 entro %g volte (0)" % FATTORE, not rv[0] <= FATTORE * r0[0], "%.3e" % rv[0])
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
