# -*- coding: utf-8 -*-
r"""**P2, L'ISOTROPIA SU GRANDEZZE CHE NON DIPENDONO DALLO ZERO** *(Luca `2026-11-09` `13:16`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `23`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/isotropia_p2.py > doc/referti_l2/isotropia_p2.txt

**`carta_isotropia.main` rigirato tale e quale**, i cerchi catturati *(un involucro di `cerchi`, il modulo non si tocca)*; **la pendenza dell'escursione ASSOLUTA `esc` di `omega` e dell'anisotropia di `|v_g|`.**
**I DEVE:** `P2-P` *(il triangolare di prova: `esc ~ k^6` entro `0.5`)*; `P2-F` *(DEVE FALLIRE: il quadrato di prova, lo stesso)*. **Le letture:** `i1` / `i2`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL = 0.5                     # ### sez. 23 (come TOLL_P di carta_isotropia)
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
    from solitone import carta_isotropia as CI
    _presidio.avvia(os.path.join(_QUI, "carta_isotropia.py"))
    _presidio.avvia(__file__)
    presi = []
    vera = CI.cerchi

    def cerchi(omega_di, kM, nome, s_om=1.0):
        kk, out = vera(omega_di, kM, nome, s_om)
        presi.append((nome, kk, out))
        return kk, out
    CI.cerchi = cerchi
    print("=" * 130)
    print("P2 (sez. 23): carta_isotropia.main rigirato tale e quale; sotto, le pendenze di esc (Delta omega assoluta) e di a_v (|v_g| relativa) fra %s k_M" % (CI.FIT,))
    print("=" * 130)
    try:
        CI.main([])
    finally:
        CI.cerchi = vera
    print("=" * 130)
    print("### P2: LE PENDENZE CHE NON DIPENDONO DALLO ZERO")
    pend = {}
    for nome, kk, out in presi:
        pe, n = CI.pendenza(kk, np.array([o["esc"] for o in out]))
        pv, _n = CI.pendenza(kk, np.array([o["a_v"] for o in out]))
        pr, _n = CI.pendenza(kk, np.array([o["a_om"] for o in out]))
        pend[nome] = (pe, pv, pr)
        print("  %-12s: esc %.3f | a_v %.3f | (la relativa a_om %.3f, che dipende dallo zero) | %d raggi" % (nome, pe, pv, pr, n))
    print("  i nomi catturati: %s" % [p[0] for p in presi])
    tri = [k for k in pend if k == "tri"]          # ### i nomi di carta_isotropia.main: "tri" (omega0 4), "qua", "tri3" (omega0 3)
    qua = [k for k in pend if k == "qua"]
    if tri:
        esito("P2-P il triangolare di prova (%s): la pendenza di esc = 6 entro %g" % (tri[0], TOLL), abs(pend[tri[0]][0] - 6.0) <= TOLL, "%.3f" % pend[tri[0]][0])
    if qua:
        esito("P2-F il quadrato di prova (%s): la pendenza di esc = 6 entro %g" % (qua[0], TOLL), abs(pend[qua[0]][0] - 6.0) <= TOLL, "%.3f" % pend[qua[0]][0], deve=False)
    mat = [k for k in pend if k.startswith("B")]
    ok = bool(mat) and all(abs(pend[k][0] - 6.0) <= TOLL and abs(pend[k][1] - 4.0) <= TOLL for k in mat)
    print("  LA LETTURA: (%s)" % ("i1: la materia ha esc ~ k^6 e a_v ~ k^4: l'anisotropia D6 e' k^6 in Delta omega ASSOLUTA" if ok else "i2: altro, coi numeri sopra"))
    print("=" * 130)
    print("ESITO P2: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
