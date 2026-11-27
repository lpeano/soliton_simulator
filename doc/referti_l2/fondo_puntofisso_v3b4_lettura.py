# -*- coding: utf-8 -*-
r"""**[M1932] LA LETTURA DEL QUARTO GIRO, CORRETTA** *(`fondo_puntofisso_v3b4.py lettura` cadde sulla riga del verdetto: «5% E» letto come specificatore di formato, errore mio; quello script e' usato e non si riscrive; la carta sez. `3-octies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3b4_lettura.py > doc/referti_l2/fondo_puntofisso_v3b4.txt

**Una sola differenza:** il verdetto si compone senza l'operatore `%` sui testi che contengono `%`. **Il resto:** `fondo_puntofisso_v3b4.fascia`, `.respiro` e i file del giro 4 cosi' come sono. **Il caso noto della stampa:** prima del giro 4, il verdetto per `0.0499`, `0.0582` e `0.0801` si stampa senza errore e nomina la fascia giusta.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_puntofisso_v3b4 as G4  # noqa: E402

PF, V3B = G4.PF, G4.V3B


def verdetto(r):
    f = G4.fascia(r)
    if f == "PASSA":
        return "PASSA (sotto il 5 per cento)"
    if f == "RESIDUO":
        return "FRA IL 5 E L'8 PER CENTO: B3 PARTE, IL RESPIRO RESIDUO " + ("%.2f" % (100 * r)) + " PER CENTO DICHIARATO"
    return "OLTRE L'8 PER CENTO: FERMO"


def lettura():
    import _presidio
    for m in ("fondo_puntofisso.py", "fondo_puntofisso_v3.py", "fondo_puntofisso_v3b.py", "fondo_puntofisso_v3b4.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1932] IL QUARTO GIRO DELLA v3b (la carta sez. 3-octies), LA LETTURA CORRETTA: il criterio sotto il 5 per cento; fra il 5 e l'8 B3 parte col respiro residuo dichiarato; oltre FERMO")
    print("=" * 130)
    ok = True
    for r, atteso in ((0.0499, "PASSA"), (0.0582, "FRA IL 5"), (0.0801, "OLTRE")):
        v = verdetto(r)
        ok = ok and v.startswith(atteso)
        print("  DEVE (la stampa): %.4f -> %s %s" % (r, v, "PASSA" if v.startswith(atteso) else "### FALLISCE"))
    assert ok, "il caso noto della stampa fallisce"
    f = os.path.join(PF.DIR, "giro_%d" % G4.G, "giro.json")
    fp = os.path.join(PF.DIR, "giro_%d" % G4.G, "periodo_v3b.json")
    PF.controlla(f)
    PF.controlla(fp)
    x, p = json.load(open(f, encoding="utf-8")), json.load(open(fp, encoding="utf-8"))
    ws = x["w"]
    r = G4.respiro(ws)
    print("  giro %d: la partenza %s" % (G4.G, x["partenza"]))
    print("  giro %d: w (k 0, %d, ..., %d): %s" % (G4.G, PF.OGNI, PF.K_GIRO, " ".join("%.2f" % w for w in ws)))
    print("          i minimi della lisciata ai k %s; %s; w min %.3f, max %.3f, medio %.3f" % (p.get("minimi_lisciata_k"), V3B.descrivi(p), min(ws), max(ws), float(np.mean(ws))))
    print("### IL CRITERIO sul giro %d: (max - min)/medio %.4f: " % (G4.G, r) + verdetto(r))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(lettura())
