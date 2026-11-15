# -*- coding: utf-8 -*-
r"""**IL VIDEO DEL TRIANGOLO** *(Luca `2026-11-14` `21:46`, (2); la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `19.15`)*.

    python csv/solitone/triangolo_video.py --registro triangolo-video > <scratchpad>/triangolo_video.txt   (poi doc/referti_l2/mattone/triangolo_video.txt; le mappe in triangolo_video_mappe.npz)

### **(T-fase) RIFATTO COL MATTONE COTTO SU `L 162`** *(`L162_MGU_03000`, al posto di `MGU_10000`)*: **`mattone_triangolo.corsa` COSI' COM'E'** *(la scena di S162, il bordo da `60`, G+U, `2000` tick, le stesse misure;
`mattone_triangolo.py` NON si tocca)*, **con tre cose IN MEMORIA:** **(1) una variante `video`** *(tre copie dello stesso francobollo; i file `triangolo_video_*`, cosi' non si sovrascrivono quelli di (T-fase))*;
**(2) `mattone_triangolo.francobollo`: il mattone di `L 162` ritagliato nella scena di S162** *(il vuoto fresco al tick dello stato, `63000`)*; **(3) `mattone_cottura.Corsa`: una sottoclasse che a `k 0` e ogni `20` tick
salva le TRE MAPPE** *(`rho`; `|phi - phi0|` sulle `6` estremita', `phi0 = c(t) F3`; `|E|` sui `3` archi uscenti da ogni nodo)* **e i centri dei tre solitoni** *(il centro periodico di `rho` sul pezzo di ciascuno, le
etichette della corsa)*: **`101` fotogrammi, `float32`, compresso, in `doc/referti_l2/mattone/triangolo_video_mappe.npz`.** ### **Il DEVE «le tre masse uguali» di `mattone_triangolo` e' legato al nome `fase`: qui NON
scatta** *(le masse dei francobolli da soli si stampano)*: **dichiarato.**
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
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

OGNI_FOTO = 20                          # ### Luca 21:46: ogni 20 tick
FOTO = {"k": [], "rho": [], "dphi": [], "E": [], "centri": []}
_Corsa = CT.Corsa


def francobollo_L162(k):
    """### Il mattone cotto su `L 162` *(`cottura_L162_MGU.json`)*, ritagliato nella scena di S162 *(come `mattone_triangolo.francobollo` per `L 81`)*."""
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    assert ct["cotto"]
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
        fr["raggio81"] = MTR.MR.raggio(Z, rho, c)          # ### il nome della chiave e' quello di mattone_triangolo: qui il raggio su L 162
        fr["file"] = ct["file"]
    return fr


class CorsaVideo(_Corsa):
    """### `mattone_cottura.Corsa` com'e', in piu' le mappe a `k 0` e ogni `20` tick."""

    def foto(self, k, t):
        from solitone import bordo as BO
        from solitone import toro as TO
        Z, C = self.Z, self.C
        n = Z["n"]
        rho = MT.rho_di(Z)
        phi0 = BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
        d = np.sqrt(np.sum(np.abs(Z["st"]["phi_h"] - phi0).reshape(n * 6, -1) ** 2, axis=1))
        FOTO["k"].append(k)
        FOTO["rho"].append(rho.astype(np.float32))
        FOTO["dphi"].append(np.sqrt(np.sum(d[Z["righe"]] ** 2, axis=1)).astype(np.float32))
        FOTO["E"].append(np.sqrt(np.sum(C.campo.E.reshape(n, 3) ** 2, axis=1)).astype(np.float32))
        FOTO["centri"].append(np.array([TO.centro(np.where(self.lab == j, rho, 0.0), Z["m1"], Z["m2"], Z["L"])[:2] for j in range(self.n_sol)], dtype=np.float32))

    def inizio(self, k):
        _Corsa.inizio(self, k)
        self.foto(k, MT.G2.T0 + k)

    def passo(self, k, t, r, e):
        _Corsa.passo(self, k, t, r, e)
        if k % OGNI_FOTO == 0:
            self.foto(k, t)


def main(argv):
    import _presidio
    from solitone import toro as TO
    for m in ("mattone_triangolo", "mattone_cottura", "mattone"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    MTR.VARIANTI["video"] = (10000, 10000, 10000)          # ### tre copie (il numero non conta: il francobollo e' quello di L 162)
    MTR.francobollo = francobollo_L162
    CT.Corsa = CorsaVideo
    print("### IL VIDEO DEL TRIANGOLO (Luca 21:46): mattone_triangolo.corsa con la variante video, il francobollo di L 162 e la Corsa con le mappe ogni %d tick, SOSTITUITI in memoria" % OGNI_FOTO)
    try:
        ok = MTR.main(["corsa", "--variante", "video"] + list(argv))
    finally:
        CT.Corsa = _Corsa
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        A1, A2 = TO.vettori()
        xy = Z["m1"][:, None] * A1[None, :] + Z["m2"][:, None] * A2[None, :]
        geo = dict(m1=Z["m1"].astype(np.int16), m2=Z["m2"].astype(np.int16), x=xy[:, 0].astype(np.float32), y=xy[:, 1].astype(np.float32), L=np.int16(Z["L"]))
    f = os.path.join(MT.DIR_REF, "triangolo_video_mappe.npz")
    np.savez_compressed(f, tick=np.array(FOTO["k"], dtype=np.int16), rho=np.stack(FOTO["rho"]), dphi=np.stack(FOTO["dphi"]), E=np.stack(FOTO["E"]), centri=np.stack(FOTO["centri"]), **geo)
    print("### LE MAPPE: %d fotogrammi (k %d ... %d) in %s, %.1f MB" % (len(FOTO["k"]), FOTO["k"][0], FOTO["k"][-1], f, os.path.getsize(f) / 1e6))
    return ok


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
