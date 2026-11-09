# -*- coding: utf-8 -*-
r"""**LA STAZIONARIETA' COL PERIODO VERO E LA RISOLUZIONE DEL CRITERIO** *(Luca `2026-11-09` `08:56`; il task history `doc/TASK_HISTORY/2026-11-07_allungamenti_coppia_30000.md`, sez. `7.15`)*. [[PIANO-2D-3D]]

    python csv/solitone/stazionarieta_v3.py > doc/referti_l2/stazionarieta_v3.txt

**`W = 3 P` PER GRANDEZZA**, `P` col metodo di M3 *(`periodo_tb3.picchi` sugli INCREMENTI, `stesso_periodo` alle due lunghezze)*; `W_RIPIEGO` se non si trova.
**Il criterio di `stazionarieta.lettura`** *(le medie per le conservate, le pendenze per le altre, `FATTORE_DIFF` volte `sig`, `CONTROLLI_DI_FILA` di fila)*, **con un `W` per grandezza; la RISOLUZIONE `FATTORE_DIFF x sig` stampata.**
**I DEVE:** `ST-F-C`, `ST-F-P`; `ST-R` *(DEVE FALLIRE: l'accelerazione a `5` volte la risoluzione nel regime)*; `ST-R-0` e `ST-R-N` stampe.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

P_BASE = 1450.0                # ### sez. 7.15: il periodo di TB3 (M3, un fatto)
PHI_BASE = 0.9                 # ### come la versione 2
AMP_BASE = 2.0                 # ### come la versione 2
DERIVA = 5e-4                  # ### come la versione 2
FATT_R = 5.0                   # ### sez. 7.15 (Luca 19:21): 5 volte la risoluzione
FATT_RN = 0.5                  # ### sez. 7.15: sotto la risoluzione, stampata
SEME = 11                      # ### come la versione 2
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def lettura_w(ST, t, serie, Wd, t_controlli):
    """### Le righe di `stazionarieta.lettura`, con `W` PER GRANDEZZA (`Wd`); i controlli dove tutte hanno le due finestre. `(t_X o None, righe)`; nelle righe `(m1, m2, sig, passa, W)`."""
    t = np.asarray(t, dtype=float)
    Wmax = max(Wd.values())
    righe, di_fila, t_x = [], 0, None
    for T in t_controlli:
        if T - 2.0 * Wmax < ST.T_RAMPA or T > t[-1] + 1e-9:
            continue
        ok, det = True, {}
        for nome, x in serie.items():
            W = Wd[nome]
            x = np.asarray(x, dtype=float)
            a = (t >= T - 2.0 * W) & (t < T - W)
            b = (t >= T - W) & (t <= T)
            if nome in ST.CONSERVATE:
                m1, m2 = float(x[a].mean()), float(x[b].mean())
                e1, e2 = ST.errore_media(x[a]), ST.errore_media(x[b])
            else:
                m1, e1 = ST.pendenza(t[a], x[a])
                m2, e2 = ST.pendenza(t[b], x[b])
            sig = math.sqrt(e1 * e1 + e2 * e2)
            passa = abs(m2 - m1) < ST.FATTORE_DIFF * sig if sig > 0 else m2 == m1
            ok = ok and passa
            det[nome] = (m1, m2, sig, passa, W)
        di_fila = di_fila + 1 if ok else 0
        if di_fila >= ST.CONTROLLI_DI_FILA and t_x is None:
            t_x = T
        righe.append((T, ok, di_fila, det))
    return t_x, righe


def periodo_m3(PT, t, x):
    """### Il metodo di M3 (q-a): gli incrementi dopo `T_DA`, Welch alle due lunghezze, `stesso_periodo`. `(P o None, il piu' forte per lunghezza)`."""
    PT.INCR[0] = True
    sel = t >= PT.T_DA
    tt, xx = PT.prepara(t[sel], x[sel])
    out = {}
    for L in PT.SEGMENTI:
        sopra, forte, passo, _phi, _nu, _K = PT.picchi(tt, xx, L)
        out[L] = (sopra, forte, passo)
    si, P = PT.stesso_periodo(out)
    return (P if si else None), {L: (o[1], o[2]) for L, o in out.items()}


def main():
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import periodo_tb3 as PT
    from solitone import stazionarieta as ST
    for m in ("corsa_accensione", "stazionarieta", "periodo_tb3"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    print("=" * 130)
    print("LA STAZIONARIETA' COL PERIODO VERO (sez. 7.15): W = 3 P per grandezza (M3 sugli incrementi, L %s; ripiego %g); controlli ogni %g, %d di fila, FATTORE_DIFF %g; la base AR(1) phi %g + %g sin(2 pi t / %g)"
          % (PT.SEGMENTI, ST.W_RIPIEGO, ST.PASSO_CONTROLLI, ST.CONTROLLI_DI_FILA, ST.FATTORE_DIFF, PHI_BASE, AMP_BASE, P_BASE))
    print("=" * 130)
    # ------------------------------------------------------------ i casi costruiti
    ts = np.arange(0.0, 30000.0, 1.5)
    rg = np.random.default_rng(SEME)
    e = rg.normal(size=len(ts))
    ar = np.empty(len(ts))
    ar[0] = e[0]
    for i_ in range(1, len(ts)):
        ar[i_] = PHI_BASE * ar[i_ - 1] + e[i_]
    base = ar + AMP_BASE * np.sin(2 * math.pi * ts / P_BASE)
    W = 3.0 * P_BASE
    t_c = np.arange(ST.PASSO_CONTROLLI, ts[-1] + 1e-9, ST.PASSO_CONTROLLI)
    _tx, rr = lettura_w(ST, ts, {"x": base}, {"x": W}, t_c)
    ris = float(np.median([ST.FATTORE_DIFF * d["x"][2] for _T, _o, _f, d in rr]))
    print("  ST-R-0 (stampa) la risoluzione della pendenza sulla base, W %.0f: FATTORE_DIFF x sig, la mediana su %d controlli = %.4e" % (W, len(rr), ris))
    costante = base + DERIVA * ts
    tx_c, _r = lettura_w(ST, ts, {"x": costante}, {"x": W}, t_c)
    pd, pde = ST.pendenza(ts[ts >= ST.T_RAMPA], costante[ts >= ST.T_RAMPA])
    esito("ST-F-C la deriva COSTANTE %g piu' la base: il regime raggiunto" % DERIVA, tx_c is not None, "da t %s" % tx_c)
    esito("ST-F-P la pendenza misurata ritrova la deriva entro 2 volte il suo errore", abs(pd - DERIVA) <= 2 * pde, "%.4e +- %.1e" % (pd, pde))
    for fatt, deve in ((FATT_R, True), (FATT_RN, False)):
        c = fatt * ris / (2.0 * W)            # ### x = base + c t^2: la pendenza 2 c t, il cambio fra le due finestre 2 c W = fatt x la risoluzione
        acc = base + c * ts * ts
        tx_a, ra = lettura_w(ST, ts, {"x": acc}, {"x": W}, t_c)
        cambi = [abs(d["x"][1] - d["x"][0]) / (ST.FATTORE_DIFF * d["x"][2]) for _T, _o, _f, d in ra]
        nota = "c %.3e; il cambio misurato / la risoluzione: mediana %.2f; nel regime da t %s" % (c, float(np.median(cambi)), tx_a)
        if deve:
            esito("ST-R l'accelerazione a %g volte la risoluzione risulta nel regime" % fatt, tx_a is not None, nota, deve=False)
        else:
            print("  ST-R-N (stampa, NON RISOLVIBILE) l'accelerazione a %g volte la risoluzione: %s" % (fatt, nota))
    # ------------------------------------------------------------ TB3 e TBS
    for nome in ("TB3", "TBS"):
        print("-" * 130)
        t, ser = ST.serie_singolo(nome, s)
        Wd, righe_p = {}, []
        for k in sorted(ser):
            P, forti = periodo_m3(PT, t, ser[k])
            Wd[k] = 3.0 * P if P else ST.W_RIPIEGO
            righe_p.append("%s: P %s -> W %.0f (%s)" % (k, ("%.0f" % P) if P else "nessuno", Wd[k], "; ".join("L %.0f il piu' forte %.0f a %.2f" % (L, f[0][0], f[0][1]) for L, f in sorted(forti.items()))))
        print("### %s fino a t %.0f: i periodi (M3 sugli incrementi) e i W" % (nome, t[-1]))
        for r_ in righe_p:
            print("    %s" % r_)
        t_c = np.arange(ST.PASSO_CONTROLLI, t[-1] + 1e-9, ST.PASSO_CONTROLLI)
        t_x, righe = lettura_w(ST, t, ser, Wd, t_c)
        for T, ok, df, det in righe:
            print("    T %7.0f  %s di fila %d  %s" % (T, "si" if ok else "no", df, "  ".join("%s %s(%.1f; ris %.1e)" % (k, "ok" if v[3] else "NO", abs(v[1] - v[0]) / (ST.FATTORE_DIFF * v[2]) if v[2] else float("inf"), ST.FATTORE_DIFF * v[2])
                                                                                    for k, v in sorted(det.items()))))
        print("    LA LETTURA %s: %s" % (nome, ("stazionario da t %.0f entro la finestra osservata" % t_x) if t_x is not None else "il regime NON raggiunto entro t %.0f (la finestra osservata)" % t[-1]))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
