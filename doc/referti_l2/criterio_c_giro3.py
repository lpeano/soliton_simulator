# -*- coding: utf-8 -*-
r"""**[M2034-B] A POSTERIORI: IL CRITERIO C SU `w` APPLICATO AL GIRO 3 STESSO** *(dopo `due_corpi_fondo_v6.txt`, che ha dato `0` finestre valide su `12`; una lettura dichiarata a posteriori, non una soglia nuova)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/criterio_c_giro3.py > doc/referti_l2/criterio_c_giro3.txt

Dal `giro.json` del giro 3 di [M0414] *(`w` e il pozzo ogni `100` tick, `omega` per tick)*: per ogni finestra da `500`, **tutti i valori di `w` nella finestra** *(`6` campioni)* entro il `5%` di `4.5`, `omega` medio entro il `5%` di `0.0833`, **tutti i valori del pozzo** entro il `10%` di `-102`. **La domanda:** il criterio puo' passare sull'oggetto che fa da riferimento?
"""
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_lettura_v3 as L3  # noqa: E402


def main():
    import _presidio
    _presidio.avvia(__file__)
    f = os.path.join(L3.GIRO3, "giro.json")
    L3.PF.controlla(f)
    g = json.load(open(f, encoding="utf-8"))
    w, p, o = g["w"], g["profondita"], g["omega"]
    print("[M2034-B] a posteriori: il criterio C sul giro 3 (%s); w %d campioni, il pozzo %d, omega %d" % (f, len(w), len(p), len(o)))
    nw = no = np_ = nt = 0
    for k0, k1 in L3.FIN:
        ws, ps = w[k0 // 100:k1 // 100 + 1], p[k0 // 100:k1 // 100 + 1]
        om = sum(o[k0:k1]) / (k1 - k0)
        okw = all(abs(x / L3.RIF_W - 1) < L3.TOL_W for x in ws)
        oko = abs(om / L3.RIF_OM - 1) < L3.TOL_OM
        okp = all(abs(x / L3.RIF_POZZO - 1) < L3.TOL_POZZO for x in ps)
        nw, no, np_, nt = nw + okw, no + oko, np_ + okp, nt + (okw and oko and okp)
        print("  [%4d, %4d]: w %s (%s); omega %.6f (%s); il pozzo %s (%s)" % (
            k0, k1, " ".join("%.3f" % x for x in ws), "si" if okw else "NO", om, "si" if oko else "NO", " ".join("%.1f" % x for x in ps), "si" if okp else "NO"))
    print("### il giro 3: w nelle soglie su %d finestre, omega su %d, il pozzo su %d; valide %d su %d; w da %.4f a %.4f" % (nw, no, np_, nt, len(L3.FIN), min(w), max(w)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
