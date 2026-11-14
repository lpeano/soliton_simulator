# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DI `conti.py`** *(Luca `2026-11-13` `23:47`, la voce `15`)*.

    python csv/solitone/test_conti.py > doc/referti_l2/bilancio/collaudo_conti.txt

**DEVE PASSARE:** **la somma dei pezzi = il totale ESATTA** *(lo stato di C35-pi a `60000`, i due centri)*; ### **`K + V` di `conti.pezzi` = quello di un referto gia' scritto AL BIT, sullo stesso stato:**
**lo stato `E:\soliton_simulator\mattone\MGU_05000.npz`** *(con `A`, `E`)* **e la serie di (MGU) committata sul ramo `strumento-mattone`** *(`git show strumento-mattone:doc/referti_l2/mattone/MGU_serie.npz`, il valore a `k 5000`)*.
**DEVE FALLIRE:** **lo stesso confronto col campo `E` cambiato di `1e-9` relativo nell'arco piu' grande.**
"""
import io
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import conti as CO  # noqa: E402

OK = [0, 0]
FALLITE = []
STATO_MGU = r"E:\soliton_simulator\mattone\MGU_05000.npz"
SERIE_MGU = "strumento-mattone:doc/referti_l2/mattone/MGU_serie.npz"


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))


def main():
    import _presidio
    import p6_u_breve as PB
    from solitone import _u1_oggi as UO
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "conti.py"))
    _presidio.avvia(__file__)
    print("=" * 120)
    print("IL COLLAUDO DI conti.py")
    print("=" * 120)
    with CO.scena("C35-pi", 60000) as Z:
        rho = PB.rho_nodi(Z["st"], Z["nodo"], Z["n"])
        x = TO.scarti(Z["m1"], Z["m2"], Z["bordo"]["c0"][0], Z["bordo"]["c0"][1], Z["L"])[:, 0]
        a, b = CC.centri_semipiani(rho, Z["m1"], Z["m2"], Z["L"], x, 0.0)
        P = CO.pezzi(Z, [a, b], None)
        print("### C35-pi a 60000: la materia A %.6e B %.6e fuori %.6e; il vuoto A %.6e B %.6e lontano %.6e; tot %.10e; tot - pezzi (l'arrotondamento di em = cost + cin) %.2e"
              % (P["materia"][0], P["materia"][1], P["materia"][2], P["vuoto"][0], P["vuoto"][1], P["vuoto"][2], P["tot"], P["tot_meno_pezzi"]))
        esito("la somma dei pezzi = il totale ESATTA (razionale)", P["somma_esatta_ok"], "", True)
    raw = subprocess.check_output(["git", "show", SERIE_MGU], cwd=os.path.dirname(_CSV))
    serie = np.load(io.BytesIO(raw))
    i5 = list(serie["k"]).index(5000)
    kv_ref = float(serie["KV"][i5])
    with CO.scena("TBS", 10000) as Z:
        with np.load(STATO_MGU) as d:
            Z["metti"]({k: d[k] for k in Z["chiavi"]})
            A, E = d["campo_A"].copy(), d["campo_E"].copy()
        campo = UO.campo_della_scena(Z["z"], PB.E_DECISO, PB.FORMA)
        campo.A[...] = A
        campo.E[...] = E
        kv = CO.pezzi(Z, [(40.5, 40.5)], campo)["KV"]
        esito("K + V di conti.pezzi = la serie di (MGU) a k 5000 AL BIT (%s)" % SERIE_MGU, kv == kv_ref, "%r contro %r" % (kv, kv_ref), True)
        i_max = int(np.argmax(np.abs(campo.E)))
        campo.E[i_max] = campo.E[i_max] * (1.0 + 1e-9)     # ### abbastanza da vedersi in K (un ulp potrebbe sparire nella somma)
        kv2 = CO.pezzi(Z, [(40.5, 40.5)], campo)["KV"]
        esito("lo stesso col campo E cambiato di 1e-9 relativo nell'arco piu' grande", kv2 == kv_ref, "%r contro %r" % (kv2, kv_ref), False)
        Z["metti"]()
        Z["mot"].geo.U[...] = Z["U0"]
    print("=" * 120)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
