# -*- coding: utf-8 -*-
r"""**IL FLUSSO DELLA PLACCHETTA: PERCHE' K3 FALLISCE** *(POST-HOC, dichiarato: la prova di gauge di `flusso_placchetta.py` da' `2.178e-10` contro la soglia `1e-12`)*. [[PROGETTO-U1]]

    E:\python\py3132\python.exe doc/referti_l2/flusso_placchetta_K3.py > doc/referti_l2/flusso_placchetta_K3.txt

**L'ipotesi** *(scritta prima di questa corsa)*: **non e' la gauge che si rompe, e' l'ARROTONDAMENTO:** se `|A|` e' molto piu' grande della circolazione `somma +-A` *(un `A` quasi tutto gradiente)*, aggiungere e togliere `chi` della scala di `A` perde cifre per CANCELLAZIONE. **Le due prove:** (1) **la scala:** `max |A|`, `std(A)`, `max |somma +-A|`, e il limite dell'arrotondamento `3 eps max(|A| + 2|chi|) / max|somma +-A|`; (2) **lo scarto relativo contro l'ampiezza di `chi`** *(`std(A)` per `1, 1e-2, 1e-4, 1e-6`)*: **se e' arrotondamento, lo scarto scende con `chi` fino al pavimento di `A`; se fosse la gauge, NON cambierebbe** -- e (3) **la gauge in aritmetica ESATTA:** `chi` intero piccolo *(multipli di `2^-20`)* e `A` arrotondato a multipli di `2^-40`: **ogni somma e' esatta, quindi Delta Phi deve essere `0` al bit.** **La soglia di K3 NON si cambia:** P-B4 resta FALSA come scritta; **qui si dice PERCHE'.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import flusso_placchetta as FP  # noqa: E402


def main():
    import _presidio
    import p6_u_breve as PB
    _presidio.avvia(os.path.join(_QUI, "flusso_placchetta.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL FLUSSO DELLA PLACCHETTA: PERCHE' K3 FALLISCE (POST-HOC, dichiarato)")
    print("=" * 130)
    e = PB.E_DECISO
    L = FP.L
    n = L * L
    P, S, _off = FP.placchette(L)
    v = np.arange(n)
    ii = np.repeat(v, 3)
    jj = np.stack([((v // L + 1) % L) * L + v % L, (v // L) * L + (v % L + 1) % L, ((v // L + 1) % L) * L + (v % L + 1) % L], axis=1).reshape(-1)
    A, _c = FP.carica("C2", 3000)
    circ = A[P[:, 0]] * S[:, 0] + A[P[:, 1]] * S[:, 1] + A[P[:, 2]] * S[:, 2]
    f = e * circ
    eps = np.finfo(float).eps
    print("(1) LA SCALA (C2 k 3000): max |A| %.4e, std(A) %.4e, max |somma +-A| %.4e (il rapporto max|A| / max|circolazione| %.3e)" % (
        float(np.max(np.abs(A))), float(np.std(A)), float(np.max(np.abs(circ))), float(np.max(np.abs(A)) / np.max(np.abs(circ)))))
    rng = np.random.default_rng(0)
    g = rng.standard_normal(n)
    esiti = []
    righe = []
    for s in (1.0, 1e-2, 1e-4, 1e-6):
        chi = float(np.std(A)) * s * g
        d = float(np.max(np.abs(FP.phi(A + chi[jj] - chi[ii], P, S, e) - f))) / float(np.max(np.abs(f)))
        lim = 3 * eps * float(np.max(np.abs(A) + 2 * np.max(np.abs(chi)))) / float(np.max(np.abs(circ)))
        righe.append((s, d, lim))
        print("(2) chi = std(A) * %.0e: max |Delta Phi| / max |Phi| = %.3e; il limite dell'arrotondamento 3 eps max(|A| + 2|chi|) / max|circ| = %.3e" % (s, d, lim))
    esiti.append(("(2) lo scarto sta sotto il limite dell'arrotondamento a ogni ampiezza di chi", all(d <= lim for _s, d, lim in righe)))
    # (3) l'aritmetica esatta
    Aq = np.round(A * 2.0 ** 40) / 2.0 ** 40
    chiq = rng.integers(-8, 9, size=n).astype(float) / 2.0 ** 20
    cq = Aq[P[:, 0]] * S[:, 0] + Aq[P[:, 1]] * S[:, 1] + Aq[P[:, 2]] * S[:, 2]
    Ag = Aq + chiq[jj] - chiq[ii]
    cg = Ag[P[:, 0]] * S[:, 0] + Ag[P[:, 1]] * S[:, 1] + Ag[P[:, 2]] * S[:, 2]
    print("(3) l'aritmetica ESATTA (A a multipli di 2^-40, chi interi su 2^20): le circolazioni diverse dopo la gauge: %d su %d" % (int(np.sum(cg != cq)), cq.size))
    esiti.append(("(3) in aritmetica esatta la circolazione e' invariata per gauge AL BIT", bool(np.array_equal(cg, cq))))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
