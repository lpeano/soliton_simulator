# -*- coding: utf-8 -*-
r"""**[M1748] IL PUNTO FISSO v3, IL PERIODO DAL MASSIMO AL MINIMO DELLA w LISCIATA** *(DECISIONE DI LUCA, 2026-11-24 17:48; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-sexies`; `fondo_puntofisso.py`, `_v2` e `_v3` sono usati e non si riscrivono)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3b.py noto > doc/referti_l2/fondo_puntofisso_v3b_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3b.py corsa          (M1748_puntofisso_v3b, dalla coda: tre giri)
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v3b.py lettura > doc/referti_l2/fondo_puntofisso_v3b.txt

`P = 2 (k_min - k_max)`: `k_min` e' il primo minimo stretto della lisciata *(`fondo_puntofisso_v3.lisciata`, 500 tick)*, `k_max` l'argmax della lisciata prima di `k_min`. La finestra e' `[k_max - P/2, k_max + P/2]`, accorciata al giro e dichiarata. **Il giro e' `fondo_puntofisso.giro` cosi' com'e'**; `minimi` si sostituisce in memoria e la decisione si scrive in `giro_<g>/periodo_v3b.json`.
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
import fondo_puntofisso_v3 as V3  # noqa: E402

PF.K_GIRO, PF.OGNI = 6000, 100
PF.DIR = os.path.join(PF.CTRL, "M1330", "puntofisso_v3b")
ULTIMA = {}


def periodo(ws, ogni, k_giro):
    """### `dict`: la lisciata, `k_min`, `k_max`, `P`, la finestra (accorciata e dichiarata), oppure `fermo`."""
    ks, v = V3.lisciata(ws, ogni)
    mi = [i for i in range(1, len(v) - 1) if v[i] < v[i - 1] and v[i] < v[i + 1]]
    d = {"lisciata_k": ks, "lisciata": [float(x) for x in v], "minimi_lisciata_k": [ks[i] for i in mi]}
    if not mi:
        d["fermo"] = "nessun minimo della w lisciata"
        return d
    i_min = mi[0]
    i_max = int(np.argmax(v[:i_min]))
    k_min, k_max = ks[i_min], ks[i_max]
    P = 2 * (k_min - k_max)
    intera = [k_max - P // 2, k_max + P // 2]
    fin = [max(0, intera[0]), min(k_giro, intera[1])]
    d.update(k_min=k_min, k_max=k_max, periodo=P, finestra_intera=intera, finestra=fin,
             accorciata=fin != intera, massimo_al_bordo=i_max == 0)
    return d


def minimi_v3b(ws):
    """### sostituisce `fondo_puntofisso.minimi`: gli INDICI della finestra, o `[]` per il FERMO."""
    d = periodo(ws, PF.OGNI, PF.K_GIRO)
    ULTIMA.clear()
    ULTIMA.update(d)
    if "fermo" in d:
        return []
    return [d["finestra"][0] // PF.OGNI, d["finestra"][1] // PF.OGNI]


def descrivi(d):
    if "fermo" in d:
        return "### FERMO: " + d["fermo"]
    return "k_max %d, k_min %d, P %d, la finestra %s%s%s" % (d["k_max"], d["k_min"], d["periodo"], d["finestra"],
                                                           " (ACCORCIATA da %s)" % d["finestra_intera"] if d["accorciata"] else "",
                                                           " (### il massimo AL BORDO)" if d["massimo_al_bordo"] else "")


def noto():
    import _presidio
    PF.F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1748] IL CASO NOTO DEL PERIODO (la carta sez. 3-sexies): P = 2 (k_min - k_max) sulla lisciata di %d tick" % V3.LISCIA)
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-90s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    PF.controlla(V3.W_V2_GIRO1)
    ws = json.load(open(V3.W_V2_GIRO1, encoding="utf-8"))["w"]
    assert len(ws) == 61
    d = periodo(ws, 100, 6000)
    print("  la lisciata del giro 1 della v2 (k %d..%d): %s" % (d["lisciata_k"][0], d["lisciata_k"][-1], " ".join("%.4f" % x for x in d["lisciata"])))
    print("  i minimi della lisciata ai k %s; %s" % (d["minimi_lisciata_k"], descrivi(d)))
    p = d.get("periodo")
    esito("(a) di Luca: il giro 1 della v2, P fra 4000 e 5000", p is not None and 4000 <= p <= 5000, "P %s" % p)
    mi = PF.minimi(ws)
    p2 = 100 * (mi[1] - mi[0]) if len(mi) >= 2 else None
    esito("(b) DEVE FALLIRE: il metodo della v2 sulla stessa serie, P fra 4000 e 5000", not (p2 is not None and 4000 <= p2 <= 5000), "il periodo della v2 %s" % p2)
    kk = np.arange(0, 6001, 100)
    d = periodo(list(10 + 3 * np.cos(2 * math.pi * (kk - 2000) / 4000.0)), 100, 6000)
    esito("(c) cos di periodo 4000, il massimo a 2000: P 4000, finestra [0, 4000], non accorciata", d.get("periodo") == 4000 and d.get("finestra") == [0, 4000] and d.get("accorciata") is False, descrivi(d))
    d = periodo(list(10 + 3 * np.cos(2 * math.pi * (kk - 1000) / 3000.0)), 100, 6000)
    esito("(d) cos, il massimo a 1000: P 3000, [-500, 2500] accorciata a [0, 2500]", d.get("periodo") == 3000 and d.get("finestra") == [0, 2500] and d.get("accorciata") is True, descrivi(d))
    d = periodo(list(10 + kk / 1000.0), 100, 6000)
    esito("(e) w crescente: FERMO", "fermo" in d, descrivi(d))
    d = periodo(list(10 + ((kk - 1000) / 1000.0) ** 2), 100, 6000)
    esito("(f) il minimo a 1000, l'argmax al bordo (k 200): dichiarato", d.get("massimo_al_bordo") is True and d.get("k_max") == 200, descrivi(d))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa():
    """### `fondo_puntofisso.corsa` con la partenza della v3; dopo ogni giro, `periodo_v3b.json`."""
    import _presidio
    PF.F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3.py"))
    _presidio.avvia(__file__)
    PF.controlla(V3.PARTENZA_V3)
    PF.minimi = minimi_v3b
    MV, P0 = PF.F1.TT.nucleo()
    Q = PF.leggi_Q()
    massa = PF.massa_di(PF.PARTENZA_1)
    print("### [M1748] la partenza %s (massa %.9f); la massa imposta %.9f" % (V3.PARTENZA_V3, PF.massa_di(V3.PARTENZA_V3), massa))
    f = V3.PARTENZA_V3
    for g in range(1, PF.GIRI + 1):
        ULTIMA.clear()
        f = PF.giro(g, f, Q, massa, MV, P0)
        fp = os.path.join(PF.DIR, "giro_%d" % g, "periodo_v3b.json")
        open(fp, "w", encoding="utf-8").write(json.dumps(dict(ULTIMA)))
        PF.firma(fp)
        print("### giro %d: i minimi della lisciata ai k %s; %s" % (g, ULTIMA.get("minimi_lisciata_k"), descrivi(ULTIMA)))
        sys.stdout.flush()
        if f is None:
            return 2
    return 0


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1748] IL PUNTO FISSO v3b (la carta sez. 3-sexies): %d tick per giro, w ogni %d, P = 2 (k_min - k_max) sulla lisciata di %d tick; il criterio (w_max - w_min)/w_medio < %.0f%% sull'ultimo giro" % (PF.K_GIRO, PF.OGNI, V3.LISCIA, 100 * PF.SOGLIA))
    print("=" * 130)
    G = []
    for g in range(1, PF.GIRI + 1):
        f = os.path.join(PF.DIR, "giro_%d" % g, "giro.json")
        fp = os.path.join(PF.DIR, "giro_%d" % g, "periodo_v3b.json")
        if not os.path.exists(f + ".sha1"):
            break
        PF.controlla(f)
        PF.controlla(fp)
        x = json.load(open(f, encoding="utf-8"))
        x["v3b"] = json.load(open(fp, encoding="utf-8"))
        G.append(x)
    for x in G:
        ws, p = x["w"], x["v3b"]
        print("  giro %d: w (k 0, %d, ..., %d): %s" % (x["giro"], PF.OGNI, PF.K_GIRO, " ".join("%.2f" % w for w in ws)))
        print("          i minimi della lisciata ai k %s; %s; (max - min)/medio %.4f" % (p.get("minimi_lisciata_k"), descrivi(p), (max(ws) - min(ws)) / float(np.mean(ws))))
    if len(G) == PF.GIRI and "fermo" not in G[-1] and "fermo" not in G[-1]["v3b"]:
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
