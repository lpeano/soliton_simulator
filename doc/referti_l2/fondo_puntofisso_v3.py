# -*- coding: utf-8 -*-
r"""**[M1735] IL PUNTO FISSO -- LA V3: IL PERIODO DA w LISCIATA** *(DECISIONE DI LUCA, 2026-11-24 17:35; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-quinquies`; `fondo_puntofisso.py` e `fondo_puntofisso_v2.py` sono usati e non si riscrivono)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3.py noto > doc/referti_l2/fondo_puntofisso_v3_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3.py corsa          (M1735_puntofisso_v3, dalla coda: tre giri)
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3.py lettura > doc/referti_l2/fondo_puntofisso_v3.txt

**Il giro e' `fondo_puntofisso.giro` cosi' com'e'**, con `K_GIRO 6000`, `OGNI 100` e la cartella `M1330/puntofisso_v3` in memoria. **Cambia solo `minimi`**, sostituita in memoria: restituisce gli indici della finestra `[k_min, k_min + periodo]`, dove il periodo si legge dai minimi della `w` lisciata *(media mobile centrata di `5` campioni = `500` tick)*. Con un solo minimo il periodo e' `4500`. Senza minimi, o se la finestra non sta nel giro, restituisce `[]`: e' il FERMO di `giro`. **La decisione si scrive in `giro_<g>/periodo_v3.json`.**
"""
import argparse
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_puntofisso as PF  # noqa: E402

PF.K_GIRO, PF.OGNI = 6000, 100
PF.DIR = os.path.join(PF.CTRL, "M1330", "puntofisso_v3")
PARTENZA_V3 = os.path.join(PF.CTRL, "M1330", "puntofisso_v2", "giro_3", "stato_006000.npz")
W_V2_GIRO1 = os.path.join(PF.CTRL, "M1330", "puntofisso_v2", "giro_1", "giro.json")
LISCIA = 500          # ### Luca: la media mobile su 500 tick
RIPIEGO = 4500        # ### Luca: il periodo con un solo minimo (dal giro 1 della v2)
ULTIMA = {}           # ### la decisione dell'ultima chiamata di minimi_v3, per periodo_v3.json


def lisciata(ws, ogni):
    """### la media mobile centrata di `LISCIA/ogni` campioni, solo finestre intere: `(k, valori)`."""
    m = LISCIA // ogni
    assert m * ogni == LISCIA and m % 2 == 1, "la finestra di %d tick non e' un numero dispari di campioni da %d" % (LISCIA, ogni)
    v = np.convolve(np.asarray(ws, dtype=float), np.ones(m) / m, mode="valid")
    h = m // 2
    return [ogni * (i + h) for i in range(len(v))], v


def periodo(ws, ogni, k_giro):
    """### `dict`: la lisciata, i suoi minimi stretti, la finestra `[ka, kb]` e la fonte, oppure `fermo`."""
    ks, v = lisciata(ws, ogni)
    mk = [ks[i] for i in range(1, len(v) - 1) if v[i] < v[i - 1] and v[i] < v[i + 1]]
    d = {"lisciata_k": ks, "lisciata": [float(x) for x in v], "minimi_lisciata_k": mk}
    if not mk:
        d["fermo"] = "nessun minimo della w lisciata"
    elif len(mk) >= 2:
        d.update(finestra=[mk[0], mk[1]], fonte="due minimi", periodo=mk[1] - mk[0])
    elif mk[0] + RIPIEGO > k_giro:
        d["fermo"] = "un solo minimo, a k %d, e la finestra del ripiego (%d) esce dal giro (%d)" % (mk[0], RIPIEGO, k_giro)
    else:
        d.update(finestra=[mk[0], mk[0] + RIPIEGO], fonte="ripiego %d (un solo minimo)" % RIPIEGO, periodo=RIPIEGO)
    return d


def minimi_v3(ws):
    """### sostituisce `fondo_puntofisso.minimi`: gli INDICI della finestra, o `[]` per il FERMO."""
    d = periodo(ws, PF.OGNI, PF.K_GIRO)
    ULTIMA.clear()
    ULTIMA.update(d)
    if "fermo" in d:
        return []
    return [d["finestra"][0] // PF.OGNI, d["finestra"][1] // PF.OGNI]


def noto():
    import _presidio
    PF.F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1735] IL CASO NOTO DEL PERIODO (la carta sez. 3-quinquies): la lisciata di %d tick, il ripiego %d" % (LISCIA, RIPIEGO))
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-90s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    PF.controlla(W_V2_GIRO1)
    ws = json.load(open(W_V2_GIRO1, encoding="utf-8"))["w"]
    assert len(ws) == 61
    d = periodo(ws, 100, 6000)
    print("  la lisciata del giro 1 della v2 (k %d..%d): %s" % (d["lisciata_k"][0], d["lisciata_k"][-1], " ".join("%.2f" % x for x in d["lisciata"])))
    print("  i minimi della lisciata ai k %s; la finestra %s; la fonte %s" % (d["minimi_lisciata_k"], d.get("finestra"), d.get("fonte", d.get("fermo"))))
    p = d.get("periodo")
    esito("(a) di Luca: il giro 1 della v2, il periodo fra 4000 e 5000", p is not None and 4000 <= p <= 5000, "periodo %s" % p)
    mi = PF.minimi(ws)
    p2 = 100 * (mi[1] - mi[0]) if len(mi) >= 2 else None
    esito("(b) DEVE FALLIRE: il metodo della v2 sulla stessa serie, il periodo fra 4000 e 5000", not (p2 is not None and 4000 <= p2 <= 5000), "il periodo della v2 %s" % p2)
    kk = np.arange(0, 6001, 100)
    d = periodo(list(10 + 3 * np.cos(2 * math.pi * kk / 3000.0)), 100, 6000)
    esito("(c) 10 + 3 cos(2 pi k/3000): due minimi, periodo 3000, finestra [1500, 4500]", d.get("finestra") == [1500, 4500] and d.get("fonte") == "due minimi", "finestra %s, %s" % (d.get("finestra"), d.get("fonte", d.get("fermo"))))
    d = periodo(list(10 + ((kk - 1000) / 1000.0) ** 2), 100, 6000)
    esito("(d) un solo minimo a k 1000: il ripiego, finestra [1000, 5500]", d.get("finestra") == [1000, 5500] and d.get("fonte", "").startswith("ripiego"), "finestra %s, %s" % (d.get("finestra"), d.get("fonte", d.get("fermo"))))
    d = periodo(list(10 + kk / 1000.0), 100, 6000)
    esito("(e) w crescente: nessun minimo, FERMO", "fermo" in d, d.get("fermo", "%s" % d.get("finestra")))
    d = periodo(list(10 + ((kk - 2000) / 1000.0) ** 2), 100, 6000)
    esito("(f) un solo minimo a k 2000, 2000 + 4500 > 6000: FERMO", "fermo" in d, d.get("fermo", "%s" % d.get("finestra")))
    print("  la massa: della partenza della v1 (quella usata) %.9f; dello stato di partenza della v3 %.9f" % (PF.massa_di(PF.PARTENZA_1), PF.massa_di(PARTENZA_V3)))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa():
    """### `fondo_puntofisso.corsa` con la partenza della v3; dopo ogni giro, `periodo_v3.json`."""
    import _presidio
    PF.F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(__file__)
    PF.controlla(PARTENZA_V3)
    PF.minimi = minimi_v3
    MV, P0 = PF.F1.TT.nucleo()
    Q = PF.leggi_Q()
    massa = PF.massa_di(PF.PARTENZA_1)
    print("### [M1735] la partenza %s (massa %.9f); la massa imposta %.9f" % (PARTENZA_V3, PF.massa_di(PARTENZA_V3), massa))
    f = PARTENZA_V3
    for g in range(1, PF.GIRI + 1):
        ULTIMA.clear()
        f = PF.giro(g, f, Q, massa, MV, P0)
        fp = os.path.join(PF.DIR, "giro_%d" % g, "periodo_v3.json")
        open(fp, "w", encoding="utf-8").write(json.dumps(dict(ULTIMA)))
        PF.firma(fp)
        print("### giro %d: i minimi della lisciata ai k %s; %s" % (g, ULTIMA.get("minimi_lisciata_k"), ULTIMA.get("fermo") or "la finestra %s (%s)" % (ULTIMA.get("finestra"), ULTIMA.get("fonte"))))
        sys.stdout.flush()
        if f is None:
            return 2
    return 0


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1735] IL PUNTO FISSO, LA V3 (la carta sez. 3-quinquies): %d tick per giro, w ogni %d, il periodo dalla lisciata di %d tick; il criterio (w_max - w_min)/w_medio < %.0f%% sull'ultimo giro" % (PF.K_GIRO, PF.OGNI, LISCIA, 100 * PF.SOGLIA))
    print("=" * 130)
    G = []
    for g in range(1, PF.GIRI + 1):
        f = os.path.join(PF.DIR, "giro_%d" % g, "giro.json")
        fp = os.path.join(PF.DIR, "giro_%d" % g, "periodo_v3.json")
        if not os.path.exists(f + ".sha1"):
            break
        PF.controlla(f)
        PF.controlla(fp)
        x = json.load(open(f, encoding="utf-8"))
        x["v3"] = json.load(open(fp, encoding="utf-8"))
        G.append(x)
    for x in G:
        ws, p = x["w"], x["v3"]
        print("  giro %d: w (k 0, %d, ..., %d): %s" % (x["giro"], PF.OGNI, PF.K_GIRO, " ".join("%.2f" % w for w in ws)))
        print("          i minimi della lisciata ai k %s; %s; (max - min)/medio %.4f" % (p.get("minimi_lisciata_k"), ("### FERMO: " + p["fermo"]) if "fermo" in p else "la finestra %s (%s)" % (p.get("finestra"), p.get("fonte")), (max(ws) - min(ws)) / float(np.mean(ws))))
    if len(G) == PF.GIRI and "fermo" not in G[-1] and "fermo" not in G[-1]["v3"]:
        ws = G[-1]["w"]
        r = (max(ws) - min(ws)) / float(np.mean(ws))
        print("### IL CRITERIO sull'ultimo giro: %.4f %s %.2f: %s" % (r, "<" if r < PF.SOGLIA else ">=", PF.SOGLIA, "PASSA" if r < PF.SOGLIA else "NON PASSA"))
    else:
        print("### IL CRITERIO: NON MISURATO (%d giri su %d, o un FERMO)" % (len(G), PF.GIRI))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    a = ap.parse_args(argv)
    return {"noto": noto, "corsa": corsa, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
