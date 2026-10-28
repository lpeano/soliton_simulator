# -*- coding: utf-8 -*-
r"""**LA DEVE `(0)` DELLO ZERO DEL VUOTO, CORRETTA DOPO I NUMERI** *([[ZERO-DEL-VUOTO]]; la risposta di Luca del `2026-10-28` `08:31`)*: ### **«al bit» diventa
«entro `1e-12` relativo»** *(come per la torsione in fase, `11410186`)*, ### **rivalutata sul jsonl di `csv/_zero_del_vuoto.py`** *(`eaa6a2b1`)*.
### **Relativo a che cosa** *(dichiarato)*: ### **`d rho` al massimo di `rho_k` dello stato iniziale, `d |phi|` al massimo di `|phi_h|` dello stato iniziale** *(lo
stesso `stato_uniforme` di `(0)`, ricostruito: nessuna dinamica)*. ### **Nessuna corsa nuova.**

Gira con:  python csv/_zero_del_vuoto_c0.py > doc/referti_l2/zero_del_vuoto_c0.txt
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

RIF = os.path.join(RADICE, "doc", "referti_l2", "zero_del_vuoto.jsonl")
TOLL_REL = 1e-12               # ### la correzione di Luca (`08:31`)


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _scomposizione_solitone as SC
    import _triangoli_forza as TF
    import _zero_del_vuoto as ZV
    import scena_l2 as SL
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA DEVE (0) DELLO ZERO DEL VUOTO, CORRETTA DOPO I NUMERI (Luca, 2026-10-28 08:31): ENTRO 1e-12 RELATIVO")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("csv/_zero_del_vuoto_c0.py", "csv/_zero_del_vuoto.py", "doc/referti_l2/zero_del_vuoto.jsonl")}
    print("  i blob nel repo: %s" % "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items()))
    print("  la configurazione: TOLL_REL %g; L0 %d S0 %g (da _zero_del_vuoto)" % (TOLL_REL, ZV.L0, ZV.S0))
    print("  ### LA CORREZIONE, DICHIARATA DOPO I NUMERI: una fase globale moltiplicata a meta' prima e a meta' dopo il tick aggiunge arrotondamenti; 'al bit' non e' il criterio giusto (Luca, 08:31)")
    print("  ### LE SCALE (dichiarate): il massimo di rho_k e di |phi_h| nello stato iniziale di (0), ricostruito senza dinamica")
    print("-" * 130)
    righe = [json.loads(l) for l in io.open(RIF, encoding="utf-8")]
    testa = [r for r in righe if r.get("tipo") == "testata"][0]
    print("  il referto rivalutato: csv/_zero_del_vuoto.py %s" % testa["blobs"]["csv/_zero_del_vuoto.py"]["sha1-BYTE"])
    u = [r for r in righe if r.get("tipo") == "uniforme"][0]
    Q0 = TF.coppia_K(0.0, ZV.S0)[0]["Q"][:, 0]
    inc, mot, st = SC.stato_uniforme(ZV.L0, Q0, np.arange(ZV.L0 * ZV.L0) // ZV.L0, np.arange(ZV.L0 * ZV.L0) % ZV.L0)
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    rho = np.zeros(inc.n)
    np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    s_rho = float(np.max(rho))
    s_phi = float(np.max(np.abs(st["phi_h"])))
    x_rho = u["d_rho"] / s_rho
    x_phi = u["d_phi"] / s_phi
    print("  rho:   max |d rho| %.3e, la scala %.6e -> %.3e relativo" % (u["d_rho"], s_rho, x_rho))
    print("  |phi|: max |d |phi|| %.3e, la scala %.6e -> %.3e relativo" % (u["d_phi"], s_phi, x_phi))
    ok = x_rho <= TOLL_REL and x_phi <= TOLL_REL
    print("  %-110s %s" % ("DEVE PASSARE (0'): delta uniforme: rho_k e |phi_h| entro %g relativo con e senza, %d tick" % (TOLL_REL, ZV.T0), "PASSA" if ok else "### FALLISCE"))
    pf = [r for r in righe if r.get("tipo") == "caduta"]
    print("  (le due PUO' FALLIRE (2) e (3) restano come nel referto: fallite; le cadute rilette: %d righe)" % len(pf))
    print("### ESITO DOPO LA CORREZIONE: %d/3 controlli passano; DEVE fallite: %d" % (1 if ok else 0, 0 if ok else 1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
