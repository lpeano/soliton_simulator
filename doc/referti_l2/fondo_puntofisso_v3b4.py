# -*- coding: utf-8 -*-
r"""**[M1932] IL QUARTO GIRO DELLA v3b** *(DECISIONE DI LUCA, 2026-11-24 19:32; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-octies`; `fondo_puntofisso_v3b.py` e' usato e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3b4.py noto > doc/referti_l2/fondo_puntofisso_v3b4_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3b4.py corsa          (M1932_puntofisso_v3b4, dalla coda: un giro)
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3b4.py lettura > doc/referti_l2/fondo_puntofisso_v3b4.txt

**Un giro, il `4`**, `fondo_puntofisso.giro` col `minimi` della v3b *(`fondo_puntofisso_v3b.minimi_v3b`)*, `6000` tick, `w` ogni `100`, nella cartella della v3b *(`giro_4`)*. **La partenza:** `giro_3/stato_006000.npz`, lo stato finale del giro 3. **Il verdetto in tre fasce** *(Luca)*: `< 5%` PASSA; da `5%` a `8%` compresi PASSA COL RESPIRO RESIDUO DICHIARATO; `> 8%` FERMO.
"""
import argparse
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_puntofisso as PF  # noqa: E402
import fondo_puntofisso_v3b as V3B  # noqa: E402

PARTENZA_G4 = os.path.join(PF.DIR, "giro_3", "stato_006000.npz")
G = 4
TETTO = 0.08        # ### Luca: fra 5% e 8% B3 parte lo stesso, dichiarando il respiro; oltre l'8% FERMO


def fascia(r):
    """### `"PASSA"`, `"RESIDUO"` (`0.05 <= r <= 0.08`) o `"FERMO"`."""
    if r < PF.SOGLIA:
        return "PASSA"
    if r <= TETTO:
        return "RESIDUO"
    return "FERMO"


def respiro(ws):
    return (max(ws) - min(ws)) / float(np.mean(ws))


def noto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3b.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1932] IL CASO NOTO DEL QUARTO GIRO (la carta sez. 3-octies): le fasce, la partenza, la cartella")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-90s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    f3 = os.path.join(PF.DIR, "giro_3", "giro.json")
    PF.controlla(f3)
    r3 = respiro(json.load(open(f3, encoding="utf-8"))["w"])
    esito("(a) il giro 3 della v3b (0.0582 nel referto) cade nella fascia RESIDUO", fascia(r3) == "RESIDUO", "%.4f -> %s" % (r3, fascia(r3)))
    att = ((0.0499, "PASSA"), (0.05, "RESIDUO"), (0.08, "RESIDUO"), (0.0801, "FERMO"), (0.3079, "FERMO"))
    esito("(b) i bordi delle fasce: 0.0499 PASSA, 0.05 e 0.08 RESIDUO, 0.0801 e 0.3079 FERMO", all(fascia(r) == f for r, f in att), " ".join("%s->%s" % (r, fascia(r)) for r, _ in att))
    esito("(c) DEVE FALLIRE: 0.0801 nella fascia RESIDUO", fascia(0.0801) != "RESIDUO", "")
    PF.controlla(PARTENZA_G4)
    esito("(d) la partenza: giro_3/stato_006000.npz, lo sha1 coincide; giro_4 non esiste ancora", not os.path.exists(os.path.join(PF.DIR, "giro_4")), PARTENZA_G4)
    print("  la massa: della partenza della v1 (quella imposta) %.9f; della partenza del giro 4 %.9f" % (PF.massa_di(PF.PARTENZA_1), PF.massa_di(PARTENZA_G4)))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa():
    import _presidio
    PF.F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3b.py"))
    _presidio.avvia(__file__)
    PF.controlla(PARTENZA_G4)
    PF.minimi = V3B.minimi_v3b
    MV, P0 = PF.F1.TT.nucleo()
    Q = PF.leggi_Q()
    massa = PF.massa_di(PF.PARTENZA_1)
    print("### [M1932] il giro %d dalla partenza %s (massa %.9f); la massa imposta %.9f" % (G, PARTENZA_G4, PF.massa_di(PARTENZA_G4), massa))
    V3B.ULTIMA.clear()
    f = PF.giro(G, PARTENZA_G4, Q, massa, MV, P0)
    fp = os.path.join(PF.DIR, "giro_%d" % G, "periodo_v3b.json")
    open(fp, "w", encoding="utf-8").write(json.dumps(dict(V3B.ULTIMA)))
    PF.firma(fp)
    print("### giro %d: i minimi della lisciata ai k %s; %s" % (G, V3B.ULTIMA.get("minimi_lisciata_k"), V3B.descrivi(V3B.ULTIMA)))
    return 0 if f is not None else 2


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3b.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1932] IL QUARTO GIRO DELLA v3b (la carta sez. 3-octies): il criterio < %.0f%%; fra %.0f%% e %.0f%% B3 parte col respiro residuo dichiarato; oltre FERMO" % (100 * PF.SOGLIA, 100 * PF.SOGLIA, 100 * TETTO))
    print("=" * 130)
    f = os.path.join(PF.DIR, "giro_%d" % G, "giro.json")
    fp = os.path.join(PF.DIR, "giro_%d" % G, "periodo_v3b.json")
    PF.controlla(f)
    PF.controlla(fp)
    x, p = json.load(open(f, encoding="utf-8")), json.load(open(fp, encoding="utf-8"))
    ws = x["w"]
    r = respiro(ws)
    print("  giro %d: la partenza %s" % (G, x["partenza"]))
    print("  giro %d: w (k 0, %d, ..., %d): %s" % (G, PF.OGNI, PF.K_GIRO, " ".join("%.2f" % w for w in ws)))
    print("          i minimi della lisciata ai k %s; %s; w min %.3f, max %.3f, medio %.3f" % (p.get("minimi_lisciata_k"), V3B.descrivi(p), min(ws), max(ws), float(np.mean(ws))))
    print("### IL CRITERIO sul giro %d: (max - min)/medio %.4f: %s" % (G, r, {"PASSA": "PASSA (< 5%)", "RESIDUO": "FRA 5% E 8%: B3 PARTE, IL RESPIRO RESIDUO %.2f%% DICHIARATO" % (100 * r), "FERMO": "OLTRE L'8%: FERMO"}[fascia(r)]))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    a = ap.parse_args(argv)
    return {"noto": noto, "corsa": corsa, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
