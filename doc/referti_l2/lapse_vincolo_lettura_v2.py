# -*- coding: utf-8 -*-
r"""**[M0528-R] LE LETTURE DEL LAPSE COME MOLTIPLICATORE -- LA V2** *(la v1 `lapse_vincolo_lettura.py`, sha1 dei byte `e5f4604f`, e' usata e non si riscrive: il suo riassunto contava **3** fallimenti invece di **4**, perche' `esito()` salvava un `numpy.bool_` e il riassunto cercava `v is False`; il referto della v1 e' committato in `cd87afb8`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo_lettura_v2.py > doc/referti_l2/lapse_vincolo_v2.txt

**Due cose, e nient'altro:**
1. **la correzione:** `esito()` della v1 sostituito in memoria da uno che salva `bool(ok)`; tutte le letture della v1 girano identiche;
2. ### **due letture in piu', FATTE DOPO AVER VISTO I NUMERI** *(nessun DEVE: sono controlli, non criteri)*:
   - **il controllo di scala della stazionarieta':** `max` sugli anelli di `|uN(2000) - uN(1500)|` *(`uN = 1 - N` mediato sull'anello, dalle `serie_chi_02000`)* **per chi con la portata** *(`CHI/mattone`)* **e per le tre righe**, misurato allo stesso modo: dice se la soglia `1e-6` di K1 era raggiungibile dal riferimento stesso;
   - **la norma senza nessun vincolo** *(`k 0` -> `k 2000`)*: le cadute di [M0908] *(`CHI/caduta` V0, V1, V2, V3)*, le cadute di Eotvos di [M1446] *(V2, V3 a x0.8, x1.2)*, il mattone di chi: dice se la norma di V3 a `1.2e-12` e' del vincolo o del tick senza `cs_N`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import lapse_vincolo_lettura as LL  # noqa: E402


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    LL.OK[che] = ok
    print("  DEVE: %-112s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def var_anelli(d):
    with np.load(os.path.join(d, "serie_chi_02000.npz")) as z:
        ks = list(z["k"])
        v = [abs(float(z["uN_%d" % R][ks.index(2000)]) - float(z["uN_%d" % R][ks.index(1500)])) for R in LL.ANELLI]
    return max(v), LL.ANELLI[int(np.argmax(v))]


def norma_mattone(d):
    with np.load(os.path.join(d, "serie_02000.npz")) as z:
        Mn = np.asarray(z["M"])
    return abs(Mn[-1] / Mn[0] - 1.0)


def dopo():
    print("### LE LETTURE IN PIU' DELLA V2 -- FATTE DOPO AVER VISTO I NUMERI DELLA V1 (nessun DEVE):")
    print("  IL CONTROLLO DI SCALA DELLA STAZIONARIETA' (agli anelli %s, max |uN(2000) - uN(1500)|, uN = 1 - N sull'anello):" % (LL.ANELLI,))
    v, R = var_anelli(LL.RIF_CHI)
    print("    chi con la portata (CHI/mattone): %.3e (all'anello %d); la norma k 0 -> 2000 %.2e" % (v, R, norma_mattone(LL.RIF_CHI)))
    for r in LL.RIGHE:
        d = os.path.join(LL.LV.BASE, "mattone_%s" % r)
        v, R = var_anelli(d)
        print("    %-4s col vincolo:              %.3e (all'anello %d); la norma k 0 -> 2000 %.2e" % (r, v, R, norma_mattone(d)))
    print("  LA NORMA SENZA NESSUN VINCOLO (k 0 -> 2000):")
    for q in ("V0", "V1", "V2", "V3"):
        print("    [M0908] caduta %s: %.2e" % (q, LL.norma(os.path.join(LL.RIF_CADUTA, q), 0, 2000)))
    for r in ("V2", "V3"):
        for sc in (0.8, 1.2):
            print("    [M1446] Eotvos %s x%.1f: %.2e" % (r, sc, LL.norma(os.path.join(LL.RIF_EOTVOS, "x%.1f" % sc, "caduta_" + r), 0, 2000)))
    for sc in (0.8, 1.2):
        print("    [M0528] V2V3 x%.1f senza vincolo: %.2e" % (sc, LL.norma(os.path.join(LL.LV.BASE, "caduta_V2V3_x%.1f_senza" % sc), 0, 2000)))
    print("=" * 140)


def main():
    import _presidio
    _presidio.avvia(__file__)
    LL.esito = esito
    LL.main()
    dopo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
