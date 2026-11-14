# -*- coding: utf-8 -*-
r"""**LA CONVERGENZA SU `L 243`, RIPARTITA** *(Luca `2026-11-14` `20:47`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `19.13`)*.

    python csv/solitone/convergenza_243.py --mondo U|GU --registro conv-<mondo>-L243 > <scratchpad>/conv_<mondo>_L243.txt

### **`convergenza.py` COSI' COM'E'** *(e' in uso da `conv-GU-L162b28`: non si tocca)*, **con DUE funzioni sostituite IN MEMORIA prima di `convergenza.main(["corsa", ..., "--L", "243"])`:**
1. **`controlla_vuoto`:** **il DEVE della scena riscritto ESCLUDENDO LA CUCITURA del toro** *(Luca `20:47`)*. ### **CHE COSA E' LA CUCITURA, letto dal codice** *(`_solitone_dal_fondo.fondo_con_fasi`)*: **il vuoto F3 da' a ogni estremita' una fase che dipende SOLO dalla direzione dell'arco e da coda/testa: e' INVARIANTE PER TRASLAZIONE.** **Lo scarto viene dal CONTROLLO: le `6` estremita' di un nodo prese nell'ordine di `argsort(nodo)`; nei nodi della RIGA `0` gli archi che entrano dall'altra parte del toro hanno indici piu' alti, e l'ordine delle estremita' e' PERMUTATO.** **La cucitura lungo `A1`: i nodi con `m1 = 0` e quelli con `m1 + 3 = L`** *(confrontati con la riga `0`)*: **`2L` nodi; lungo `A2` lo stesso con `m2`.** **Il DEVE: fuori dalla cucitura lo scarto sotto `1e-12`, e dentro gli scarti oltre `1e-12` su non piu' dei `2L` nodi della cucitura** *(come sulle scene buone di `L 81` e `L 162`, `6b07fca5`)*.
2. **`francobollo`, per (MGU):** **il mattone COTTO SU `L 162`, `L162_MGU_03000`, ritagliato nella scena di S162** *(il vuoto fresco al tick `63000`)*, **non `MGU_10000` di `L 81`** *(Luca `20:47`, dichiarato)*. **Per (MU) il francobollo di `convergenza.py`** *(`MU_05000`, `L 81`)*.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import convergenza as CV  # noqa: E402
import mattone as MT  # noqa: E402


def controlla_vuoto_senza_cucitura(Z):
    """### `(e1, e3, nd)` come `convergenza.controlla_vuoto`, ma `e3` FUORI dalla cucitura *(la riga 0 e quella che si confronta con lei: `2L` nodi)*; se lo scarto sta su piu' di `2L` nodi, `e3 = inf`."""
    L, n, righe = Z["L"], Z["n"], Z["righe"]
    st = Z["st"]
    p2 = np.zeros((n, 6))
    r6 = np.arange(6 * n)
    np.add.at(p2, (Z["nodo"], 2 * ((r6 // 2) % 3) + r6 % 2), np.abs(st["phi_h"]) ** 2)
    dentro = Z["g_nodo"] == 0.0
    e1 = float(np.max(np.abs(p2[dentro] - 1.0)))
    m1, m2 = Z["m1"], Z["m2"]
    ph = st["phi_h"][righe]
    e3 = 0.0
    for nome, d1, d2 in (("A1", 3, 0), ("A2", 0, 3)):
        w = ((m1 + d1) % L) * L + (m2 + d2) % L
        D = np.abs(ph[w] - ph).reshape(n, -1).max(axis=1)
        mm = m1 if d1 else m2
        cucitura = (mm == 0) | ((mm + 3) % L == 0)                       # ### la riga 0 e quella che si confronta con la riga 0: 2L nodi
        fuori = float(D[~cucitura].max())
        n_cuc = int((D[cucitura] > 1e-12).sum())
        print("### LA CUCITURA (Luca 20:47) lungo %s: %d nodi (la riga 0 e quella che si confronta con lei); lo scarto oltre 1e-12 su %d di essi (al piu' 2L = %d); FUORI dalla cucitura il massimo %.3e"
              % (nome, int(cucitura.sum()), n_cuc, 2 * L, fuori))
        e3 = max(e3, fuori if n_cuc <= 2 * L else float("inf"))
    return e1, e3, int(dentro.sum())


def francobollo_L162(caso, k):
    """### **(MGU):** il mattone cotto su `L 162` *(`cottura_L162_MGU.json`)*, ritagliato nella scena di S162; `fr["picco81"]` e' il suo picco *(il nome della chiave e' quello di `convergenza.py`)*."""
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    assert ct["cotto"] and caso == "MGU"
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        with np.load(ct["file"]) as d:
            Z["metti"]({x: d[x] for x in Z["chiavi"]})
        rho = MT.rho_di(Z)
        c = MT.centro_di(Z, rho)
        st = {x: Z["st"][x].copy() for x in Z["chiavi"]}
        MT.vuoto_fresco(Z, int(ct["t"]))
        phi_rif = Z["st"]["phi_h"].copy()
        Z["metti"](st)
        fr = MT.ritaglia(Z, c, phi_rif)
        fr["picco81"] = float(rho.max())
        fr["file"] = ct["file"]
    print("### IL MATTONE (Luca 20:47): %s, cotto su L 162 (k %d), ritagliato nella scena di S162: R_t %.1f, %d nodi, il picco %.4e" % (ct["file"], ct["k"], fr["R_t"], len(fr["w"]), fr["picco81"]))
    return fr


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "convergenza.py"))
    _presidio.avvia(__file__)
    i = list(argv).index("--mondo")
    mondo = argv[i + 1]
    CV.controlla_vuoto = controlla_vuoto_senza_cucitura
    if mondo == "GU":
        CV.francobollo = francobollo_L162
    print("### LA CONVERGENZA SU L 243 (Luca 20:47): convergenza.controlla_vuoto%s SOSTITUITE in memoria (dichiarato)" % (" e convergenza.francobollo" if mondo == "GU" else ""))
    return CV.main(["corsa", "--L", "243"] + list(argv))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
