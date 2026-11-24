# -*- coding: utf-8 -*-
r"""**LA STIMA DELLA CORSA GEMELLA** *(Luca `2026-11-17` `21:00`, TODO 4; la carta `doc/TASK_HISTORY/2026-11-17_innesco_contatore.md`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/innesco_stima.py > doc/referti_l2/innesco_stima.txt

**La domanda:** **quanto deve durare la corsa perche' nascano almeno `10` nodi OLTRE il confine** *(`23.81`; e, accanto, oltre `29.81`, dove la nascita FA ha la materia sotto l'`1%` -- `regole_fase_F3.txt`: `2.4e-03`)*. **Il tempo al primo `2 pi` di ogni arco:** la retta di M3-bis prolungata da `k 3000` *(`torsione_segmenti.py`: la pendenza vettoriale, solo gli archi oltre `3 sigma`; entro `45` nodi)*; **oltre `45` nodi** *(nessuna serie)*: `|Theta(3000)| / 3000` come ritmo, dichiarato **e NON significativo** *(nessuna retta)*. **Il costo:** il tick MISURATO di C2 *(`3.690` s, la chiusura di `controllo-C2` in `doc/REGISTRO_CORSE.md`, letto da li')*.
**Il caso noto** *(Q-A4)*: **il primo `2 pi` su tutti gli archi entro `45` nodi = `2.7888e+04`** *(`torsione_segmenti.txt`)*.
"""
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import torsione_tempo_proprio as T1  # noqa: E402
import torsione_tempo_proprio_v2 as T2  # noqa: E402

CONFINI = (23.81, 29.81)
N_NASCITE = 10


def tick_misurato():
    testo = open(os.path.join(_RADICE, "doc", "REGISTRO_CORSE.md"), encoding="utf-8").read()
    righe = [x for x in testo.splitlines() if '"nome": "controllo-C2"' in x and '"CHIUSO"' in x]
    assert len(righe) == 1, "la chiusura di controllo-C2 non e' una sola"
    m = re.search(r"([0-9.]+) s per tick", righe[0])
    return float(m.group(1))


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "torsione_segmenti.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA STIMA DELLA CORSA GEMELLA (Luca 2026-11-17 21:00): quanti tick perche' nascano %d nodi oltre il confine" % N_NASCITE)
    print("=" * 130)
    segs = T2.carica("C2")
    centro, sel = segs[0]["centro"], segs[0]["sel"]
    with T1.PS.CV.scena_L(186, T1.PS.FATTORE_R_A * T1.PS.R_OGG_MAX) as Z:
        r, _c, _m = T1.geometria_archi(Z, centro)
        Z["metti"]()
    Th = np.sum([s["acc"] for s in segs], axis=0)
    Tt = np.cumsum(np.concatenate([s["serie"] for s in segs], axis=0), axis=0)
    T = Tt.shape[0]
    t = np.arange(1, T + 1, dtype=float)
    tm = t.mean()
    Stt = float(np.sum((t - tm) ** 2))
    pend = ((t - tm) @ (Tt - Tt.mean(axis=0))) / Stt
    q = Tt.mean(axis=0) - pend * tm
    err = np.sqrt(np.sum((Tt - (np.outer(t, pend) + q)) ** 2, axis=0) / (T - 2)) / math.sqrt(Stt)
    th3 = Tt[-1]
    ap = np.abs(pend)
    signif = ap > 3 * err
    resto = np.where(np.sign(th3) == np.sign(pend), 2 * math.pi - np.abs(th3), 2 * math.pi + np.abs(th3))
    with np.errstate(divide="ignore"):
        Tk = np.where(signif, 3000.0 + resto / ap, np.inf)
    esiti = [("il caso noto: il primo 2 pi entro 45 nodi = 2.7888e+04 (torsione_segmenti.txt)", "%.4e" % float(Tk.min()) == "2.7888e+04")]
    print("### il caso noto: il primo 2 pi entro 45 nodi %.4e" % float(Tk.min()))
    dt = tick_misurato()
    print("### il tick misurato di C2 (il registro): %.3f s" % dt)
    rs = r[sel]
    fuori = np.ones(r.size, dtype=bool)
    fuori[sel] = False
    rit_f = np.abs(Th[fuori]) / 3000.0
    with np.errstate(divide="ignore"):
        Tf = np.where(rit_f > 0, 2 * math.pi / rit_f, np.inf)
    for R in CONFINI:
        dentro45 = rs >= R
        Tin = np.sort(Tk[dentro45])
        sig_n = int(np.sum(signif & dentro45))
        print("-" * 130)
        print("OLTRE %.2f NODI: entro 45 nodi %d archi, con la pendenza oltre 3 sigma %d; il ritmo netto massimo %.4e rad per tick" % (R, int(dentro45.sum()), sig_n, float(np.max(np.where(signif & dentro45, ap, 0.0)))))
        if np.isfinite(Tin[:N_NASCITE]).all() and Tin.size >= N_NASCITE:
            T10 = float(Tin[N_NASCITE - 1])
            print("    il %d-esimo arco a 2 pi (la retta prolungata): tick %.4e = %.3e ore al tick misurato (%.1f anni); il primo: tick %.4e" % (N_NASCITE, T10, T10 * dt / 3600.0, T10 * dt / 3600.0 / 24.0 / 365.0, float(Tin[0])))
        else:
            print("    meno di %d archi con la pendenza significativa: il tempo NON e' stimabile dalla retta" % N_NASCITE)
        Tfs = np.sort(Tf[r[fuori] >= R])
        print("    oltre 45 nodi (|Theta|/3000, NON significativo): il %d-esimo arco a 2 pi al tick %.4e" % (N_NASCITE, float(Tfs[N_NASCITE - 1])))
    print("-" * 130)
    print("### l'estensione di C2 alla stessa lunghezza: lo stesso costo (il braccio senza mitosi gira allo stesso tick)")
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
