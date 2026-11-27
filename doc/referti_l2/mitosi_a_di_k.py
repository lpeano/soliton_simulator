# -*- coding: utf-8 -*-
r"""**[M2245-27] A2, a(k) = sqrt(n(k)) DALLA FIAMMATA** *(DECISIONE DI LUCA, 2026-11-27 22:45; la carta `doc/CARTA_mitosi.md`, A2; solo letture; nessuna ipotesi Lambda)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_a_di_k.py > doc/referti_l2/mitosi_a_di_k.txt

`n(k)` = `n0` + le nascite con `k_nascita < k` *(`n0` e le nascite come in A1, `mitosi_costo_nodo.py`)*, letto ai bordi delle finestre di `500` da
`k 36000` a `46000`; `a = sqrt(n)`; `H_i = (a_{i+1} - a_{i-1}) / (2 * 500 * a_i)`; `a''_i = (a_{i+1} - 2 a_i + a_{i-1}) / 500^2`;
`q_i = - a''_i a_i / a'_i^2` *(`a'_i` la differenza centrata)*. **La lettura:** «c'e' una fase con `q > 0` prima di una con `q < 0`?» = esiste `i`
con `q > 0` nelle finestre prima e `q < 0` in almeno `2` finestre consecutive dopo. **Casi noti:** (K1) `a` lineare: `q = 0` entro `1e-12`;
(K2) `a` esponenziale: `q = -1` entro l'errore della differenza finita *(stampato)*; (K3) `a ~ k^(1/2)`: `q = +1` con lo stesso criterio.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_costo_nodo as A1  # noqa: E402
import mitosi_dati as MD  # noqa: E402

PASSO = 500
BORDI = np.arange(36000, 46001, PASSO)
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def hq(a, passo):
    """### `H_i`, `q_i` sui punti interni `1..len-2`."""
    a = np.asarray(a, dtype=float)
    d1 = (a[2:] - a[:-2]) / (2.0 * passo)
    d2 = (a[2:] - 2.0 * a[1:-1] + a[:-2]) / passo ** 2
    return d1 / a[1:-1], -d2 * a[1:-1] / d1 ** 2


def fase_prima_dopo(q):
    """### esiste `i` con `q > 0` per tutte le finestre `< i` (almeno una) e `q < 0` in `i, i+1`?"""
    for i in range(1, len(q) - 1):
        if np.all(q[:i] > 0) and q[i] < 0 and q[i + 1] < 0:
            return i
    return None


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_dati.py"))
    _presidio.avvia(os.path.join(_QUI, "mitosi_costo_nodo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2245-27] A2, a(k) = sqrt(n(k)) DALLA FIAMMATA (la carta doc/CARTA_mitosi.md, A2): H e q per finestra di %d" % PASSO)
    print("=" * 130)
    kk = BORDI.astype(float)          # ### gli stessi bordi dei dati: la differenza finita ha lo stesso passo relativo
    _, q = hq(3.0 + 0.002 * kk, PASSO)
    esito("(K1) a lineare: q = 0 entro 1e-12", float(np.max(np.abs(q))) < 1e-12, "max |q| %.3e" % float(np.max(np.abs(q))))
    _, q = hq(np.exp(kk / 4000.0), PASSO)
    err = (PASSO / 4000.0) ** 2 / 3.0
    esito("(K2) a esponenziale (tau 4000): q = -1 entro l'errore della differenza finita %.2e" % err, float(np.max(np.abs(q + 1.0))) < 2 * err, "max |q + 1| %.3e" % float(np.max(np.abs(q + 1.0))))
    _, q = hq(np.sqrt(kk), PASSO)
    esito("(K3) a ~ k^(1/2): q = +1 entro 0.05", float(np.max(np.abs(q - 1.0))) < 0.05, "max |q - 1| %.3e" % float(np.max(np.abs(q - 1.0))))
    # ### i dati
    nas = A1.nascite()
    ks = np.array([int(x["k"]) for x in nas])
    with np.load(os.path.join(MD.R, "MITOSI", "stato_36000.npz"), allow_pickle=True) as z:
        meta = json.loads(str(z["meta"]))
    n0 = int(meta["n"]) - int(meta["nascite"])
    n = np.array([n0 + int((ks < b).sum()) for b in BORDI], dtype=float)
    a = np.sqrt(n)
    H, q = hq(a, PASSO)
    print("-" * 130)
    print("  il bordo     n        a         nascite nella finestra prima       H (1/tick)        q")
    print("-" * 130)
    for i, b in enumerate(BORDI):
        nf = int(n[i] - n[i - 1]) if i else int((ks < b).sum())
        if 1 <= i <= len(BORDI) - 2:
            print("  k %5d  %6d  %.6f  %4d                        %+.4e      %+9.3f" % (b, int(n[i]), a[i], nf, H[i - 1], q[i - 1]))
        else:
            print("  k %5d  %6d  %.6f  %4d                        (bordo)" % (b, int(n[i]), a[i], nf))
    print("-" * 130)
    pos, neg, nul = int((q > 0).sum()), int((q < 0).sum()), int((q == 0).sum())
    print("  i segni di q (%d finestre interne): %s" % (len(q), "".join("+" if x > 0 else ("-" if x < 0 else "0") for x in q)))
    print("  q > 0 in %d, q < 0 in %d, q = 0 in %d" % (pos, neg, nul))
    i = fase_prima_dopo(q)
    print("### UNA FASE CON q > 0 PRIMA DI UNA CON q < 0 (>= 2 finestre consecutive): %s" % (
        "SI', il cambio al bordo k %d" % BORDI[i + 1] if i is not None else "NO"))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
