# -*- coding: utf-8 -*-
r"""**M3-bis, IL REFERTO DEI 12 SEGMENTI: C'E' UNA DERIVA NETTA?** *(Luca `2026-11-17` `21:00`, TODO 1; la carta `doc/TASK_HISTORY/2026-11-17_innesco_contatore.md`, sez. `1`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/torsione_segmenti.py > doc/referti_l2/torsione_segmenti.txt

**I dati:** i `12` segmenti di C2 *(`torsione_tempo_proprio_v2.py segmento`, `E:/soliton_simulator/controllo/torsione/C2_<k0>.npz`)*: Theta accumulata tick per tick su ogni arco, e il ritmo di ogni tick per gli archi entro `45` nodi dal centro.
**IL CRITERIO DI LUCA** *(scritto prima del referto)*: **sugli archi del massimo** *(i `20` con `|Theta|` totale piu' grande entro `45` nodi)* **la pendenza della retta su Theta(t), `k 0`-`3000`, e' diversa da zero oltre `3 sigma`, E la deriva netta `|pendenza| * 3000` supera l'ampiezza della parte oscillante** *(il MASSIMO di `|residuo|`)*. **Si legge sull'arco del massimo; accanto, quanti dei `20` lo passano.**
**Il ritmo netto per arco** *(entro `45` nodi)*: la pendenza dei minimi quadrati su Theta(t), con l'errore standard dai residui *(vettoriale su tutti gli archi)*; **fuori dai `45` nodi** *(nessuna serie)*: `Theta(3000) / 3000`, dichiarato. **Il tempo al primo `2 pi`:** per ogni arco con la pendenza oltre `3 sigma`, la retta prolungata da `k 3000`; **gli archi a `2 pi` entro `1e4`, `1e5`, `1e6`.** **I candidati** *(entro `1e5`)* **salvati per il conto di S1** *(`candidati.npz`)*.
**Il caso noto** *(Q-A4)*: per gli archi entro `45` nodi, la somma dei `12` accumuli = l'ultimo valore della serie cumulata *(stessi addendi, ordine diverso: entro `1e-12` relativo alla scala)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import torsione_tempo_proprio as T1  # noqa: E402
import torsione_tempo_proprio_v2 as T2  # noqa: E402

N_MASSIMO = 20


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "torsione_tempo_proprio_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("M3-bis, IL REFERTO DEI 12 SEGMENTI DI C2: C'E' UNA DERIVA NETTA? (Luca 2026-11-17 21:00)")
    print("=" * 130)
    segs = T2.carica("C2")
    assert segs is not None, "i 12 segmenti non ci sono tutti"
    esiti = []
    al_bit = [s["al_bit"] for s in segs]
    print("### i 12 segmenti: lo stato d'arrivo al bit con lo stato salvato successivo in %d su 12" % sum(al_bit))
    esiti.append(("i 12 segmenti arrivano al bit allo stato salvato successivo", all(al_bit)))
    centro = segs[0]["centro"]
    sel = segs[0]["sel"]
    with T1.PS.CV.scena_L(186, T1.PS.FATTORE_R_A * T1.PS.R_OGG_MAX) as Z:
        r, cosr, _mid = T1.geometria_archi(Z, centro)
        Z["metti"]()
    Th = np.sum([s["acc"] for s in segs], axis=0)
    serie = np.concatenate([s["serie"] for s in segs], axis=0)
    Tt = np.cumsum(serie, axis=0)
    scala = float(np.max(np.abs(Th)))
    cn = float(np.max(np.abs(Th[sel] - Tt[-1]))) / scala
    print("### il caso noto: la somma dei 12 accumuli contro la serie cumulata (entro 45 nodi, %d archi): max differenza / scala %.3e" % (sel.size, cn))
    esiti.append(("il caso noto: la somma dei segmenti = la serie cumulata entro 1e-12 della scala", cn <= 1e-12))
    # ---------------------------------------------------- la retta su ogni arco (vettoriale)
    T = Tt.shape[0]
    t = np.arange(1, T + 1, dtype=float)
    tm = t.mean()
    Stt = float(np.sum((t - tm) ** 2))
    ym = Tt.mean(axis=0)
    pend = ((t - tm) @ (Tt - ym)) / Stt
    q = ym - pend * tm
    res = Tt - (np.outer(t, pend) + q)
    sig = np.sqrt(np.sum(res ** 2, axis=0) / (T - 2))
    err = sig / math.sqrt(Stt)
    amp = np.max(np.abs(res), axis=0)
    rms = np.sqrt(np.mean(res ** 2, axis=0))
    top = np.argsort(-np.abs(Tt[-1]))[:N_MASSIMO]
    print("-" * 130)
    print("GLI ARCHI DEL MASSIMO (i %d con |Theta| totale piu' grande entro 45 nodi): la retta su Theta(t), t = 1..3000" % N_MASSIMO)
    print("    %7s %7s %13s %13s %11s %8s %13s %13s %11s %s" % ("arco", "r", "Theta(3000)", "pendenza", "sigma", "p/sigma", "deriva 3000", "max|res|", "rms res", "il criterio"))
    passano = []
    for k_, i in enumerate(top):
        a = int(sel[i])
        ok = abs(pend[i]) > 3 * err[i] and abs(pend[i]) * 3000 > amp[i]
        passano.append(ok)
        print("    %7d %7.2f %+13.6e %+13.5e %11.3e %8.1f %13.5e %13.5e %11.3e %s" % (a, float(r[a]), float(Tt[-1, i]), float(pend[i]), float(err[i]), float(abs(pend[i]) / err[i]), float(abs(pend[i]) * 3000), float(amp[i]), float(rms[i]), "PASSA" if ok else "no"))
    print("    l'arco del massimo: %s; dei %d, lo passano %d" % ("PASSA" if passano[0] else "NON PASSA", N_MASSIMO, sum(passano)))
    esiti.append(("IL CRITERIO DI LUCA (P-L1): sull'arco del massimo la pendenza oltre 3 sigma E la deriva in 3000 tick oltre il max |residuo|", bool(passano[0])))
    # ---------------------------------------------------- il ritmo netto: dove
    rs = r[sel]
    an = np.floor(rs).astype(int)
    signif = np.abs(pend) > 3 * err
    ap = np.abs(pend)
    i_max = int(np.argmax(np.where(signif, ap, 0.0)))
    media_an = np.bincount(an, weights=np.where(signif, ap, 0.0)) / np.maximum(np.bincount(an), 1)
    print("-" * 130)
    print("IL RITMO NETTO (la pendenza, entro 45 nodi; %d archi su %d con la pendenza oltre 3 sigma): il massimo %.5e +- %.2e rad per tick all'arco %d, r %.2f (anello %d); l'anello della media massima %d (%.4e)" % (
        int(signif.sum()), sel.size, float(ap[i_max]), float(err[i_max]), int(sel[i_max]), float(rs[i_max]), int(an[i_max]), int(np.argmax(media_an)), float(media_an.max())))
    print("    il ritmo netto medio per anello (solo gli archi oltre 3 sigma, gli altri contano 0): " + "  ".join("%d: %.2e" % (j, media_an[j]) for j in range(0, min(46, media_an.size), 3)))
    fuori = np.ones(r.size, dtype=bool)
    fuori[sel] = False
    print("    fuori dai 45 nodi (nessuna serie: |Theta(3000)| / 3000, dichiarato): il massimo %.4e a r %.2f" % (float(np.max(np.abs(Th[fuori]))) / 3000.0, float(r[fuori][int(np.argmax(np.abs(Th[fuori])))])))
    esiti.append(("P-L2: il ritmo netto massimo fra 12 e 22 nodi (r %.2f)" % float(rs[i_max]), 12.0 <= float(rs[i_max]) <= 22.0))
    # ---------------------------------------------------- il tempo al primo 2 pi
    th3 = Tt[-1]
    stesso = np.sign(th3) == np.sign(pend)
    with np.errstate(divide="ignore", invalid="ignore"):
        resto = np.where(stesso, 2 * math.pi - np.abs(th3), 2 * math.pi + np.abs(th3))
        Tk = np.where(signif & (ap > 0), 3000.0 + resto / ap, np.inf)
        Tk_lo = np.where(signif, 3000.0 + resto / (ap + err), np.inf)
        Tk_hi = np.where(signif & (ap > err), 3000.0 + resto / (ap - err), np.inf)
    gia = np.abs(th3) >= 2 * math.pi
    Tk = np.where(gia, 0.0, Tk)
    j = int(np.argmin(Tk))
    print("-" * 130)
    print("IL PRIMO 2 pi (la retta prolungata da k 3000; gli archi entro 45 nodi con la pendenza oltre 3 sigma): l'arco %d a r %.2f, al tick %.4e (con +- una sigma della pendenza: fra %.4e e %.4e); gia' oltre 2 pi a k 3000: %d" % (
        int(sel[j]), float(rs[j]), float(Tk[j]), float(Tk_lo[j]), float(Tk_hi[j]), int(gia.sum())))
    for TT in (1e4, 1e5, 1e6):
        dentro = Tk <= TT
        print("    entro %.0e tick: %d archi a 2 pi (r da %s a %s)" % (TT, int(dentro.sum()), ("%.2f" % float(rs[dentro].min())) if dentro.any() else "-", ("%.2f" % float(rs[dentro].max())) if dentro.any() else "-"))
    esiti.append(("P-L3: il primo arco a 2 pi fra 1e4 e 1e5 tick (%.4e)" % float(Tk[j]), 1e4 <= float(Tk[j]) <= 1e5))
    cand = np.where(Tk <= 1e5)[0]
    np.savez(os.path.join(T2.DIR_T, "candidati.npz"), archi=sel[cand], T=Tk[cand], r=rs[cand], pend=pend[cand], err=err[cand], theta3000=th3[cand], centro=centro)
    print("### i candidati entro 1e5 tick (%d archi) salvati in %s" % (cand.size, os.path.join(T2.DIR_T, "candidati.npz")))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
