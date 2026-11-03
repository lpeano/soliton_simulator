# -*- coding: utf-8 -*-
r"""**LA CARTA DELLA DERIVA E DELLA FRECCIA DEL VUOTO** *(Luca `2026-11-03` `08:29`; il task history `doc/TASK_HISTORY/2026-11-03_deriva_e_freccia.md`)*:
### **`TF3` (e `TFI`, se c'e') accanto a `TP1000`, il centro periodico srotolato.**
    python csv/solitone/carta_freccia.py > doc/referti_l2/deriva_e_freccia.txt      # dopo la corsa TF3 (e TFI, se la condizione)
### **I DEVE:** `T0` il vuoto a `t = 0` al bit di `fondo_con_fasi`; `T1` il primo campione al bit di `TP1000`; `T1-F` *(deve fallire)* lo `sha_fine` del primo pezzo uguale;
`A3` *(`accensione.a3`)*, `A4`; ### **`TM` la definizione del tempo del moto ridà su `TP1000` `9000 +- 2000`** *(il controllo della definizione)*.
### **Le misure a blocchi di `1000`:** la posizione, la velocita', la direzione *(e i coseni con `A1`, `A2`, `A1+A2`)*, il cuore, `w`, l'alone, la freccia del vuoto; il logaritmo dello
spostamento *(`carta_deriva.logaritmo`)*; lo spostamento totale; ### **la condizione di `TFI`** *(sez. `2` del task history)*.
### **IL TEMPO DEL MOTO, la definizione MIA, scritta prima di vedere `TF3`:** ### **l'inizio del primo blocco di `1000`, dopo `T_acc`, con la velocita' almeno META' della massima
velocita' a blocchi della stessa corsa** *(fino alla fine valida, `3 w < R`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

BLOCCO = 1000.0                # ### Luca 08:29: a blocchi di 1000
META_V = 0.5                   # ### il tempo del moto: la velocita' a meta' della massima (la definizione dichiarata)
T_MOTO_TP = (7000.0, 11000.0)  # ### TM: su TP1000 il moto parte a ~9000 (Luca 08:29); il controllo della definizione, 9000 +- 2000 (il task history, sez. 2)
TFI_SPOSTAMENTO = 0.5          # ### la condizione di TFI (sez. 2): lo spostamento a 16000 sotto meta' di TP1000 ...
TFI_ANGOLO = 30.0              # ### ... o la direzione a piu' di 30 gradi ...
TFI_TEMPO = 2000.0             # ### ... o il tempo del moto fuori da quello di TP1000 +- 2000 (sez. 2: 9000 +- 2000)
STATI_F0 = (("TM1000", (13333, 40000, 66667)),)   # ### la freccia di F0 nel tempo: gli stati completi di TM1000 (al bit di TP1000; doc/referti_l2/mappe_indice.txt)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def tempo_moto(righe, T_acc, fine):
    """### **Il tempo del moto** *(la definizione dichiarata nel docstring)*: `(t, v_max)`."""
    rr = [r for r in righe if r[0] >= T_acc and r[1] <= fine + 1e-9]
    if not rr:
        return None, float("nan")
    vmax = max(r[2] for r in rr)
    for r in rr:
        if r[2] >= META_V * vmax:
            return r[0], vmax
    return None, vmax


def coseni(v):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    n = math.hypot(*v)
    if n == 0:
        return (float("nan"),) * 3
    return tuple(float(np.dot(v, a) / (n * math.hypot(*a))) for a in (A1, A2, A1 + A2))


def angolo(a, b):
    d = (a - b + 180.0) % 360.0 - 180.0
    return abs(d)


def main(argv):
    del argv
    import _presidio
    import _stato_fermo as SFM
    import _solitone_dal_fondo as SD
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import carta_deriva as CD
    from solitone import corsa_accensione as CA
    from solitone import vuoto as VU
    for m in ("__init__", "toro", "vuoto", "accensione", "corsa_accensione", "carta_deriva"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    corse = ["TP1000", "TF3"] + (["TFI"] if CA.nomi("TFI") else [])
    print("=" * 130)
    print("LA DERIVA E LA FRECCIA DEL VUOTO (Luca 2026-11-03 08:29): %s, il centro periodico srotolato; BLOCCO %g META_V %g T_MOTO_TP %s; la condizione di TFI: spostamento < %g x TP1000,"
          % (", ".join(corse), BLOCCO, META_V, T_MOTO_TP, TFI_SPOSTAMENTO))
    print("  o la direzione a piu' di %g gradi, o il tempo del moto a piu' di %g da TP1000; STATI_F0 %s" % (TFI_ANGOLO, TFI_TEMPO, STATI_F0))
    print("  le letture di Luca, scritte prima: (a1) su F3 non si muove (o molto meno), sull'ibrido in mezzo: la causa e' la freccia; (a2) su F3 come su F0: la freccia non c'entra;")
    print("  (a3) su F3 in un'altra direzione; (a4) F3 non regge il solitone come F0 (gia' prima di 9000); (a5) altro")
    print("  ### IL TEMPO DEL MOTO (la definizione MIA, scritta prima): l'inizio del primo blocco dopo T_acc con la velocita' >= %g della massima a blocchi della stessa corsa" % META_V)
    print("=" * 130)
    S = {n: CA.serie(n) for n in corse}
    # ------------------------------------------------------------------ i DEVE
    with V.scena(s, "fondo", V.EPS) as (_rec, z, _phi0, _pK):
        inc, L = z["inc"], z["L"]
        idx, dirs = VU.celle(inc, L)
        for n in corse[1:]:
            r0 = S[n][0][0]
            phi_n = SD.fondo_con_fasi(inc, L, CA.fasi_vuoto(n))
            esito("DEVE PASSARE: T0 %s il vuoto a t = 0 e' fondo_con_fasi(%s) AL BIT (lo sha registrato, ricalcolato)" % (n, CA.fasi_vuoto(n)), r0["sha_vuoto"] == SFM.sha(phi_n),
                  "le fasi registrate %s" % r0["vuoto_fasi"])
        fr0 = {"TP1000": VU.freccia_media(VU.freccia(_phi0, idx, dirs))}
        frs = {}
        for nome, tt_ in STATI_F0:
            for t in tt_:
                f = os.path.join(CA.base_e(nome), "stati", nome, "%s_stato_%06d.npz" % (nome, t))
                with np.load(f) as d:
                    frs[t * s] = VU.freccia_media(VU.freccia(d["phi_h"], idx, dirs))
    cp0 = S["TP1000"][1][0]
    for n in corse[1:]:
        c0 = S[n][1][0]
        uguali = c0["per"] == cp0["per"] and c0["E"]["totale"]["M"] == cp0["E"]["totale"]["M"] and c0["E"]["totale"]["V"] == cp0["E"]["totale"]["V"]
        esito("DEVE PASSARE: T1 %s il primo campione (le misure sul toro, M, V) e' quello di TP1000 AL BIT" % n, uguali, "")
        esito("DEVE FALLIRE: T1-F %s lo sha_fine del primo pezzo e' quello di TP1000" % n, S[n][0][0]["sha_fine"] != S["TP1000"][0][0]["sha_fine"], "")
        rr, cc = S[n][0], S[n][1]
        t3 = np.array([c["t"] for c in cc]) * s
        okM, nM = AC.a3(t3, np.array([c["E"]["totale"]["M"] for c in cc]), cc[-1]["t"], V.TOLL_NORMA)
        okV, nV = AC.a3(t3, np.array([c["E"]["totale"]["V"] for c in cc]), cc[-1]["t"], V.TOLL_NORMA)
        esito("DEVE PASSARE: A3 %s M e V (accensione.a3)" % n, okM and okV, "M %s; V %s" % (nM, nV))
        esito("DEVE PASSARE: A4 %s il libro col par della corsa" % n, all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rr), "")
        pv = rr[0].get("partenza_vuoto")
        print("  %s LA PARTENZA COSTRUITA SUL SUO VUOTO (solo registrata): %s; quella usata: mu %.12f (TP1000)" % (n, pv, rr[0]["info"]["mu"]))
    # ------------------------------------------------------------------ le misure
    D = {}
    for n in corse:
        tt, X, ww, fl, T_acc, che, R = CD.dati(n)
        fine = CD.fine_valida(tt, ww, R, BLOCCO)
        righe = CD.finestre(n, tt, X, ww, fl, 0.0, min(fine, tt[-1]), BLOCCO, False)
        tm, vmax = tempo_moto(righe, T_acc, fine)
        D[n] = {"tt": tt, "X": X, "ww": ww, "fl": fl, "T_acc": T_acc, "fine": fine, "righe": righe, "tm": tm, "vmax": vmax, "camp": S[n][1]}
    tm_tp = D["TP1000"]["tm"]
    esito("DEVE PASSARE: TM la definizione del tempo del moto ridà su TP1000 un tempo in %s (il controllo della definizione)" % (T_MOTO_TP,),
          tm_tp is not None and T_MOTO_TP[0] <= tm_tp <= T_MOTO_TP[1], "TP1000: %s (la velocita' massima a blocchi %.3f per 1000)" % (tm_tp, D["TP1000"]["vmax"]))
    for n in corse:
        d = D[n]
        print("-" * 130)
        print("### %s: %s; la fine valida (3 w < R) %g; il tempo del moto %s (la velocita' massima %.3f per 1000)" % (n, "il centro periodico srotolato", d["fine"], d["tm"], d["vmax"]))
        print("  %-17s %-20s %-9s %-9s %-23s %-9s %-9s %-9s %-11s %-11s" % ("blocco", "X medio", "v/1000", "angolo", "cos A1 / A2 / A1+A2", "cuore", "w", "alone", "|freccia|", "scarto"))
        cc = d["camp"]
        tc = np.array([c["t"] for c in cc]) * s
        al = np.array([c["per"]["alone"] for c in cc])
        fm = np.array([c["freccia"]["modulo"] if "freccia" in c else np.nan for c in cc])
        fsc = np.array([c["freccia"]["scarto"] if "freccia" in c else np.nan for c in cc])
        for a, b, v, ang, wm, _amp, Xm in d["righe"]:
            m = (tc >= a) & (tc < b)
            vv = (math.cos(math.radians(ang)) * v, math.sin(math.radians(ang)) * v)
            cs = coseni(vv)
            print("  %7.0f .. %7.0f (%+8.3f, %+8.3f) %-9.3f %+9.2f %+6.3f / %+6.3f / %+6.3f %-9.5f %-9.4f %-9.5f %-11.4e %-11.4e"
                  % (a, b, Xm[0], Xm[1], v, ang, cs[0], cs[1], cs[2], float(d["fl"][(d["tt"] >= a) & (d["tt"] < b)].mean()), wm, float(al[m].mean()),
                     float(np.nanmean(fm[m])) if np.isfinite(fm[m]).any() else float("nan"), float(np.nanmax(fsc[m])) if np.isfinite(fsc[m]).any() else float("nan")))
        CD.logaritmo(n, d["tt"], d["X"], d["T_acc"], d["fine"], BLOCCO)
    print("-" * 130)
    print("### LA FRECCIA DEL VUOTO DI TP1000 (F0) NEL TEMPO, dagli stati completi di TM1000 (al bit di TP1000): il modulo medio, lo scarto massimo fra i nodi, la media (Re, Im)")
    print("  tempo 0: modulo %.6f scarto %.3e media %s" % (fr0["TP1000"]["modulo"], fr0["TP1000"]["scarto"], fr0["TP1000"]["media"]))
    for t in sorted(frs):
        print("  tempo %.2f: modulo %.6f scarto %.3e media %s" % (t, frs[t]["modulo"], frs[t]["scarto"], frs[t]["media"]))
    # ------------------------------------------------------------------ lo spostamento totale e la condizione di TFI
    print("-" * 130)
    print("### LO SPOSTAMENTO TOTALE (l'ultimo campione meno il primo, srotolato) E LA CONDIZIONE DI TFI (il task history, sez. 2)")
    tot = {}
    for n in corse:
        dX = D[n]["X"][-1] - D[n]["X"][0]
        tot[n] = (float(math.hypot(*dX)), math.degrees(math.atan2(dX[1], dX[0])))
        print("  %-7s lo spostamento %.3f nodi a %+.2f gradi (a tempo %.1f); il tempo del moto %s" % (n, tot[n][0], tot[n][1], D[n]["tt"][-1], D[n]["tm"]))
    meno = tot["TF3"][0] < TFI_SPOSTAMENTO * tot["TP1000"][0]
    dir_ = angolo(tot["TF3"][1], tot["TP1000"][1]) > TFI_ANGOLO
    tmp = D["TF3"]["tm"] is None or tm_tp is None or abs(D["TF3"]["tm"] - tm_tp) > TFI_TEMPO
    print("  ### LA CONDIZIONE DI TFI: meno %s (%.3f contro %g x %.3f); la direzione %s (%.2f gradi); il tempo del moto %s (%s contro %s) => TFI %s"
          % (meno, tot["TF3"][0], TFI_SPOSTAMENTO, tot["TP1000"][0], dir_, angolo(tot["TF3"][1], tot["TP1000"][1]), tmp, D["TF3"]["tm"], tm_tp,
             "SI GIRA" if (meno or dir_ or tmp) else "NON si gira"))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


if __name__ == "__main__":
    main(sys.argv[1:])
