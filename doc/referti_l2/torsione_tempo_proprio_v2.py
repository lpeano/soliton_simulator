# -*- coding: utf-8 -*-
r"""**LA TORSIONE DEL TEMPO PROPRIO, v2: M3-bis, THETA TICK PER TICK** *(Luca `2026-11-17` `18:48`, l'aggiunta al mandato delle `18:04`; la carta `doc/TASK_HISTORY/2026-11-17_torsione_tempo_proprio.md`, sez. `4`)*. [[MITOSI-QUANTO-OLONOMIA]]

### **UNA VERSIONE NUOVA, DICHIARATA:** `torsione_tempo_proprio.py` *(v1, `a28a838c`)* **resta com'e'** *(k1, k3, k2 vengono da li')*; **qui M3-bis e le misure che la usano.** **Il perche'** *(K3, `torsione_tempo_proprio_K3.txt`)*: **il trapezio fra stati ogni `250` tick sbaglia Theta del `96%` della scala.**

    E:\python\py3132\python.exe doc/referti_l2/torsione_tempo_proprio_v2.py segmento C2 <k0>      (k0 = 0, 250, ..., 2750; un processo per segmento)
    E:\python\py3132\python.exe doc/referti_l2/torsione_tempo_proprio_v2.py analisi > doc/referti_l2/torsione_tempo_proprio.txt

**`segmento NOME k0`:** dallo stato salvato di `NOME` a `k0` *(`k0 = 0`: lo stato preparato come la corsa, `controllo_senza_bordo.prepara`)*, `250` tick della corsa *(senza bordo per C2, col bordo per C1)*; **Theta accumulata TICK PER TICK su ogni arco** *(la definizione della v1: `pi (dtau_nodo_i - dtau_nodo_j)` per tick, `cs` del punto fisso del tick)*; **il ritmo di ogni tick salvato per gli archi entro `45` nodi dal centro della corsa** *(per Theta(t))*; **il controllo: lo stato d'arrivo = lo stato salvato a `k0 + 250` AL BIT.** Il file: `E:/soliton_simulator/controllo/torsione/<NOME>_<k0>.npz`.
**`analisi`:** Theta totale = la somma dei `12` segmenti; M1 *(il ritmo NETTO per arco su ogni segmento: Theta del segmento / `250`)*, M2, M3-bis, **CRESCE O OSCILLA** *(per gli archi del massimo: Theta(t) tick per tick su tutta la corsa, la retta dei minimi quadrati -- la pendenza = il ritmo netto, con l'errore standard dei residui -- e l'ampiezza attorno alla retta)*, M4, M5 *(se C1 c'e')*, M6 *(la mappa)*; le previsioni P-T1..P-T4 *(P-T2 sul ritmo NETTO)*.
"""
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI,):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import torsione_tempo_proprio as T1  # noqa: E402  (la v1: la definizione, la geometria degli archi, l'avvio)

PS, CSB = T1.PS, T1.CSB
DIR_T = os.path.join(T1.DIR, "torsione")
SEGMENTO = 250
K0S = tuple(range(0, 3000, SEGMENTO))
R_SERIE = 45.0
N_MASSIMO = 20          # ### gli archi del massimo per CRESCE/OSCILLA: i 20 con |Theta| totale piu' grande (dichiarato prima)


def segmento(nome, k0):
    LC = PS.LC
    bordo = {"C2": False, "C1": True}[nome]
    os.makedirs(DIR_T, exist_ok=True)
    out = os.path.join(DIR_T, "%s_%05d.npz" % (nome, k0))
    assert not os.path.exists(out), "%s esiste gia': non si sovrascrive" % out
    print("M3-bis: %s, il segmento da k %d a k %d, Theta tick per tick" % (nome, k0, k0 + SEGMENTO))
    t00 = time.time()
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        A = T1.Avvio(Z, bordo)
        mot = Z["mot"]
        if k0 == 0:
            C, meta = CSB.prepara(Z, 186, bordo, A.rho_c, A.e, A.t0)
            rho = PS.MT.rho_di(Z)
            meta["centro"] = [float(x) for x in PS.MT.centro_di(Z, rho)]
            meta["lab"] = meta["centro"]
            cs0 = None
            print("### lo stato di k 0 preparato come la corsa; il centro %s" % meta["centro"])
        else:
            C, meta, cs0, s = A.da_stato(nome, k0)
            print("### la ripresa da %s stato_%05d (sha1 %s, ricontrollato)" % (nome, k0, s[:8]))
        r, _c, _mid = T1.geometria_archi(Z, meta["centro"])
        sel = np.where(r <= R_SERIE)[0]
        PS.PO.accendi(cs0)
        acc = np.zeros(mot.inc.m)
        serie = np.zeros((SEGMENTO, sel.size))
        try:
            R = A.corsa(C, meta["lab"], k0)
            for q, k in enumerate(range(k0 + 1, k0 + SEGMENTO + 1)):
                R.passo(k, A.t0 + k, 1.0, A.e)
                if k % PS.CT.OGNI == 0:
                    rho = PS.MT.rho_di(Z)
                    R.etichette([PS.MT.centro_di(Z, rho)])
                rit = T1.ritmo(mot, LC.cs_prec())
                acc += rit
                serie[q] = rit[sel]
            cs1 = LC.cs_prec()
        finally:
            LC.spegni()
        f = os.path.join(T1.DIR, nome, "stato_%05d.npz" % (k0 + SEGMENTO))
        uguale = []
        with np.load(f) as d:
            for x in Z["chiavi"]:
                uguale.append((x, bool(np.array_equal(d[x], Z["st"][x]))))
            uguale.append(("campo_A", bool(np.array_equal(d["campo_A"], C.campo.A))))
            uguale.append(("campo_E", bool(np.array_equal(d["campo_E"], C.campo.E))))
            uguale.append(("cs_prec", bool(np.array_equal(d["cs_prec"], cs1))))
        ok = all(u for _x, u in uguale)
        np.savez(out, acc=acc, serie=serie, sel=sel, centro=np.array(meta["centro"]), al_bit=np.array(ok), uguale=np.array(json.dumps(uguale)))
        Z["metti"]()
    print("### Theta del segmento: max |.| %.6e rad; lo stato d'arrivo contro stato_%05d: %s" % (float(np.max(np.abs(acc))), k0 + SEGMENTO, uguale))
    print("  DEVE: lo stato d'arrivo = lo stato salvato a k %d AL BIT   %s" % (k0 + SEGMENTO, "PASSA" if ok else "### FALLISCE"))
    print("### %.0f s; il file %s" % (time.time() - t00, out))
    return 0 if ok else 1


def carica(nome):
    segs = []
    for k0 in K0S:
        f = os.path.join(DIR_T, "%s_%05d.npz" % (nome, k0))
        if not os.path.exists(f):
            return None
        with np.load(f) as d:
            segs.append({"k0": k0, "acc": d["acc"].copy(), "serie": d["serie"].copy(), "sel": d["sel"].copy(), "centro": d["centro"].copy(), "al_bit": bool(d["al_bit"])})
    return segs


def analisi():
    esiti = []
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        dati = {}
        for nome in ("C2", "C1"):
            segs = carica(nome)
            if segs is None:
                print("### %s: i 12 segmenti NON ci sono tutti: %s non entra nell'analisi (dichiarato)" % (nome, nome))
                continue
            centro = segs[0]["centro"]
            assert all(np.array_equal(s["centro"], centro) for s in segs), "il centro cambia fra i segmenti"
            r, cosr, mid = T1.geometria_archi(Z, centro)
            dati[nome] = {"segs": segs, "r": r, "cos": cosr, "mid": mid}
        Z["metti"]()
    for nome, D in dati.items():
        segs, r, cosr = D["segs"], D["r"], D["cos"]
        an = np.floor(r).astype(int)
        print("=" * 130)
        print("%s: i 12 segmenti ripresi; lo stato d'arrivo al bit in %d su 12" % (nome, sum(s["al_bit"] for s in segs)))
        esiti.append(("%s: ogni segmento arriva allo stato salvato successivo AL BIT" % nome, all(s["al_bit"] for s in segs)))
        Th = np.sum([s["acc"] for s in segs], axis=0)
        D["Th"] = Th
        # ---------------------------------------------------- M1-M2: il ritmo NETTO per segmento
        print("M1-M2: il ritmo NETTO |Theta del segmento| / 250 per anello (rad per tick): media, massimo per arco; radiali (entro 30 gradi) e tangenziali (oltre 60)")
        rad, tan = cosr >= T1.RADIALE_COS, cosr <= T1.TANGENZIALE_COS
        for s in (segs[0], segs[5], segs[-1]):
            a = np.abs(s["acc"]) / SEGMENTO
            media = np.bincount(an, weights=a) / np.maximum(np.bincount(an), 1)
            L_ = an.max() + 1
            mr = np.bincount(an[rad], weights=a[rad], minlength=L_) / np.maximum(np.bincount(an[rad], minlength=L_), 1)
            mt = np.bincount(an[tan], weights=a[tan], minlength=L_) / np.maximum(np.bincount(an[tan], minlength=L_), 1)
            i_arc, i_med = int(np.argmax(a)), int(np.argmax(media))
            print("  k %4d-%4d: il massimo per arco %.4e a r %.2f; l'anello della media massima %d (%.4e); oltre 40 nodi il massimo %.3e (%.3e del massimo)" % (
                s["k0"], s["k0"] + SEGMENTO, float(a.max()), float(r[i_arc]), i_med, float(media[i_med]), float(a[r > 40].max()), float(a[r > 40].max() / a.max())))
            for j0 in range(0, 46, 5):
                print("         " + "  ".join("%2d: %.2e %.2e %.2e" % (j, media[j], mr[j], mt[j]) for j in range(j0, min(j0 + 5, 46))))
        aT = np.abs(Th) / 3000.0
        i_arc = int(np.argmax(aT))
        print("  su tutta la corsa (|Theta| / 3000): il massimo per arco %.4e a r %.2f; oltre 40 nodi %.3e del massimo" % (float(aT.max()), float(r[i_arc]), float(aT[r > 40].max() / aT.max())))
        if nome == "C2":
            esiti.append(("P-T1: il ritmo netto massimo (|Theta| / 3000) fra 10 e 22 nodi (C2: r %.2f)" % float(r[i_arc]), 10.0 <= float(r[i_arc]) <= 22.0))
            esiti.append(("P-T4: oltre 40 nodi sotto l'1%% del massimo (C2: %.3e)" % float(aT[r > 40].max() / aT.max()), float(aT[r > 40].max() / aT.max()) < 0.01))
        # ---------------------------------------------------- M3-bis
        print("M3-bis: Theta totale (la somma dei 12 segmenti, tick per tick): max |Theta| %.6e rad (%.4f di 2 pi) all'arco a r %.2f; archi oltre 2 pi entro 3000: %d" % (
            float(np.abs(Th).max()), float(np.abs(Th).max() / (2 * math.pi)), float(r[int(np.argmax(np.abs(Th)))]), int(np.sum(np.abs(Th) >= 2 * math.pi))))
        # ---------------------------------------------------- CRESCE O OSCILLA
        sel = segs[0]["sel"]
        assert all(np.array_equal(s["sel"], sel) for s in segs)
        serie = np.concatenate([s["serie"] for s in segs], axis=0)     # (3000, archi entro 45)
        Tt = np.cumsum(serie, axis=0)
        top = np.argsort(-np.abs(Tt[-1]))[:N_MASSIMO]
        t = np.arange(1, Tt.shape[0] + 1, dtype=float)
        print("CRESCE O OSCILLA: i %d archi con |Theta| totale piu' grande (entro 45 nodi): la retta dei minimi quadrati su Theta(t), t = 1..3000" % N_MASSIMO)
        print("    %7s %7s %14s %12s %14s %14s %10s" % ("arco", "r", "Theta(3000)", "pendenza", "err. pend.", "ampiezza rms", "max |res|"))
        pend = []
        for q in top:
            y = Tt[:, q]
            X = np.vstack([t, np.ones_like(t)]).T
            coef, *_ = np.linalg.lstsq(X, y, rcond=None)
            res = y - X @ coef
            sig = float(np.sqrt(np.sum(res ** 2) / (len(t) - 2)))
            err = sig / float(np.sqrt(np.sum((t - t.mean()) ** 2)))
            a = int(sel[q])
            pend.append((abs(float(coef[0])), err, a))
            print("    %7d %7.2f %+14.6e %+12.4e %14.3e %14.4e %10.4e" % (a, float(r[a]), float(y[-1]), float(coef[0]), err, float(np.sqrt(np.mean(res ** 2))), float(np.max(np.abs(res)))))
        pmax, emax, amax = max(pend)
        t2pi = 2 * math.pi / pmax
        print("    il ritmo NETTO massimo %.4e +- %.1e rad per tick (l'arco %d, r %.2f): 2 pi al ritmo netto in %.0f tick" % (pmax, emax, amax, float(r[amax]), t2pi))
        for T in (1e4, 1e5):
            prog = np.abs(Th) * (T / 3000.0)
            print("    al ritmo netto medio della corsa (|Theta| / 3000 per arco): archi oltre 2 pi entro %.0e tick: %d" % (T, int(np.sum(prog >= 2 * math.pi))))
        if nome == "C2":
            esiti.append(("P-T2: il primo arco a 2 pi al ritmo NETTO fra 100 e 10000 tick (C2: %.0f)" % t2pi, 100.0 <= t2pi <= 10000.0))
        # ---------------------------------------------------- M4
        i_med = int(np.argmax(np.bincount(an, weights=np.abs(Th)) / np.maximum(np.bincount(an), 1)))
        selA = an == i_med
        prime = float(np.mean(np.abs(segs[0]["acc"][selA] + segs[1]["acc"][selA]))) / 500.0
        ultime = float(np.mean(np.abs(segs[-2]["acc"][selA] + segs[-1]["acc"][selA]))) / 500.0
        print("M4: all'anello del massimo di |Theta| (%d): il ritmo netto medio sulle prime 500 %.4e, sulle ultime 500 %.4e: il rapporto %.4f" % (i_med, prime, ultime, ultime / prime))
        if nome == "C2":
            esiti.append(("P-T3: ultime 500 contro prime 500 entro il 10%% (C2: %.4f)" % (ultime / prime), abs(ultime / prime - 1.0) <= 0.10))
    # ---------------------------------------------------- M5
    print("=" * 130)
    if "C1" in dati and "C2" in dati:
        a1, a2 = np.abs(dati["C1"]["Th"]), np.abs(dati["C2"]["Th"])
        big = a2 > 0.01 * a2.max()
        print("M5: C1 contro C2, |Theta| a k 3000: il massimo %.4e contro %.4e (rapporto %.4f); la differenza relativa per arco (archi sopra l'1%% del massimo di C2): mediana %.3e, massimo %.3e" % (
            float(a1.max()), float(a2.max()), float(a1.max() / a2.max()), float(np.median(np.abs(a1 - a2)[big] / a2[big])), float(np.max(np.abs(a1 - a2)[big] / a2[big]))))
    else:
        print("M5: C1 non c'e' ancora (dichiarato): il confronto dopo")
    # ---------------------------------------------------- M6
    if "C2" in dati:
        D = dati["C2"]
        T1.figura({"mid": D["mid"], "Th": D["Th"], "r": D["r"]})
        print("M6: la mappa di |Theta| a k 3000 (C2, M3-bis): torsione_tempo_proprio.png")
    return esiti


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "torsione_tempo_proprio.py"))
    _presidio.avvia(os.path.join(_QUI, "controllo_senza_bordo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA TORSIONE DEL TEMPO PROPRIO, v2 (Luca 2026-11-17 18:48): %s" % " ".join(argv))
    print("=" * 130)
    if argv[0] == "segmento":
        return segmento(argv[1], int(argv[2]))
    esiti = analisi()
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
