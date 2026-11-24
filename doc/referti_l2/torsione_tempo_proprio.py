# -*- coding: utf-8 -*-
r"""**LA TORSIONE DEL TEMPO PROPRIO, SOLO MISURA** *(Luca `2026-11-17` `18:04`; la carta `doc/TASK_HISTORY/2026-11-17_torsione_tempo_proprio.md`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/torsione_tempo_proprio.py k1 > doc/referti_l2/torsione_tempo_proprio_K1.txt
    E:\python\py3132\python.exe doc/referti_l2/torsione_tempo_proprio.py k3 > doc/referti_l2/torsione_tempo_proprio_K3.txt
    E:\python\py3132\python.exe doc/referti_l2/torsione_tempo_proprio.py k2 > doc/referti_l2/torsione_tempo_proprio_K2.txt
    E:\python\py3132\python.exe doc/referti_l2/torsione_tempo_proprio.py misura > doc/referti_l2/torsione_tempo_proprio.txt

**La definizione** *(letta dal codice, la carta sez. `1.2`)*: **`Theta_a = pi * somma_t (dtau_nodo_i(t) - dtau_nodo_j(t)) / dtau_rif`**, `i = ii[a]`, `j = jj[a]`, **`dtau_nodo = mot.dtau * cs`** *(`flussi_parziali.dtau_nodo`)*, **`dtau_rif = 1`** *(`omega = pi`)*, **`cs` il lapse del punto fisso del tick** *(`lapse_caldo.cs_prec()`: lo stesso che gli stati salvano)*. **Il ritmo dell'arco:** `pi (dtau_nodo_i - dtau_nodo_j)` per tick. **Il quanto:** `|Theta_a| = 2 pi`.
**K1** il vuoto F3 puro *(`psi = 0`)*, un tick della corsa senza bordo: `Theta = 0` al bit; DEVE FALLIRE: `cs` perturbato di `1e-12` su un nodo.
**K3** da `stato_01500` di C2, `250` tick: l'accumulo tick per tick contro il trapezio fra gli estremi; lo stato d'arrivo contro `stato_01750` di C2.
**K2** da `stato_03000` di C2, `50` tick: l'avanzamento della fase RELATIVA delle due estremita' del vuoto *(`arg(phi_coda(t+1)/phi_coda(t)) - arg(phi_testa(t+1)/phi_testa(t))`)* contro `pi (dtau_nodo_i - dtau_nodo_j)`, sugli archi oltre `30` nodi *(e, dichiarato accanto, per anelli piu' interni)*; il rapporto, mediana e dispersione, e la SCALA.
**misura** M1-M6 sugli stati di C2 e di C1 *(`E:/soliton_simulator/controllo/`)*; la figura `torsione_tempo_proprio.png`.
"""
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_QUI, _SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import controllo_senza_bordo as CSB  # noqa: E402  (importato, NON modificato: e' in uso da C1 e C2)

PS = CSB.PS
DIR = CSB.DIR
R_MATERIA, CONFINE = 12.4, 23.81
OLTRE_K2 = 30.0
TICK_K2 = 50
DA_K3, A_K3 = 1500, 1750
STATI = tuple(range(250, 3001, 250))
RADIALE_COS, TANGENZIALE_COS = math.cos(math.radians(30.0)), math.cos(math.radians(60.0))


def dtau_nodo(mot, cs):
    assert np.all(mot.dtau == 1.0), "mot.dtau non e' 1: la definizione va riletta (la carta sez. 1.2)"
    return np.asarray(mot.dtau, dtype=float) * np.asarray(cs, dtype=float)


def ritmo(mot, cs):
    """### `pi (dtau_nodo_i - dtau_nodo_j)` per arco (`dtau_rif = 1`)."""
    d = dtau_nodo(mot, cs)
    nodo = np.asarray(mot.inc.nodo)
    return math.pi * (d[nodo[0::2]] - d[nodo[1::2]])


def geometria_archi(Z, centro):
    """### `r` del punto medio dell'arco dal centro, e il coseno fra l'arco e il raggio."""
    from solitone import toro as TO
    L = Z["L"]
    nodo = np.asarray(Z["mot"].inc.nodo)
    ii, jj = nodo[0::2], nodo[1::2]
    m1, m2 = Z["m1"], Z["m2"]
    Di = TO.scarti(m1[ii], m2[ii], centro[0], centro[1], L)[:, :2]
    de = TO.scarti(m1[jj], m2[jj], m1[ii], m2[ii], L)[:, :2]
    mid = Di + 0.5 * de
    r = np.hypot(mid[:, 0], mid[:, 1])
    with np.errstate(invalid="ignore", divide="ignore"):
        c = np.abs(np.sum(mid * de, axis=1)) / (r * np.hypot(de[:, 0], de[:, 1]))
    return r, c, mid


class Avvio(object):
    """### la scena di C1/C2 e la corsa (le righe di `controllo_senza_bordo.corsa`)."""

    def __init__(self, Z, bordo):
        self.Z, self.bordo = Z, bordo
        self.MT, self.CT, self.PO, self.LC = PS.MT, PS.CT, PS.PO, PS.LC
        self.rho_c = self.MT.rho_c_assoluto()
        self.e = self.MT.PB.E_DECISO
        self.t0 = self.MT.G2.T0

    def da_stato(self, nome, k):
        f = os.path.join(DIR, nome, "stato_%05d.npz" % k)
        C, meta, cs, s = CSB.riprendi(self.Z, f, self.bordo, self.rho_c, self.e)
        return C, meta, cs, s

    def corsa(self, C, centro, k):
        self.R = (self.CT.Corsa if self.bordo else CSB.corsa_senza_bordo())(self.Z, C)
        self.R.etichette([centro])
        self.R.inizio(k)
        return self.R


def k1():
    MT, PO, LC = PS.MT, PS.PO, PS.LC
    print("K1: IL VUOTO F3 PURO, UN TICK DELLA CORSA SENZA BORDO: THETA = 0 AL BIT")
    esiti = []
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        A = Avvio(Z, False)
        MT.vuoto_fresco(Z, A.t0)
        C = PO.campi(Z, A.rho_c, A.e)
        PO.accendi(None)
        try:
            R = A.corsa(C, [Z["L"] / 2.0, Z["L"] / 2.0], 0)
            R.passo(1, A.t0 + 1, 1.0, A.e)
            cs = LC.cs_prec()
        finally:
            LC.spegni()
        mot = Z["mot"]
        rit = ritmo(mot, cs)
        print("### psi = 0: la massa %.3e; cs: min %.17g max %.17g (s = %r); il ritmo per arco: max |pi (dtau_i - dtau_j)| = %.3e; archi diversi da 0: %d su %d" % (
            float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2)), float(cs.min()), float(cs.max()), Z["s"], float(np.max(np.abs(rit))), int(np.sum(rit != 0)), rit.size))
        esiti.append(("K1: il vuoto F3 puro, Theta di un tick = 0 AL BIT su tutti gli archi", bool(np.all(rit == 0.0))))
        cs2 = cs.copy()
        cs2[0] += 1e-12
        rit2 = ritmo(mot, cs2)
        print("    DEVE FALLIRE: cs perturbato di 1e-12 sul nodo 0: archi diversi da 0: %d (max %.3e)" % (int(np.sum(rit2 != 0)), float(np.max(np.abs(rit2)))))
        esiti.append(("K1, DEVE FALLIRE: cs perturbato di 1e-12 su un nodo da' Theta != 0 sui suoi archi", int(np.sum(rit2 != 0)) == int(np.sum(np.asarray(mot.inc.nodo) == 0))))
        Z["metti"]()
    return esiti


def k3():
    LC = PS.LC
    print("K3: L'INTEGRALE FRA STATI -- da C2 k %d a k %d, l'accumulo tick per tick contro il trapezio" % (DA_K3, A_K3))
    esiti = []
    t00 = time.time()
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        A = Avvio(Z, False)
        C, meta, cs0, s = A.da_stato("C2", DA_K3)
        print("### la ripresa da C2 stato_%05d (sha1 %s, ricontrollato)" % (DA_K3, s[:8]))
        mot = Z["mot"]
        PS.PO.accendi(cs0)
        acc = np.zeros(mot.inc.m)
        try:
            R = A.corsa(C, meta["lab"], DA_K3)
            for k in range(DA_K3 + 1, A_K3 + 1):
                R.passo(k, A.t0 + k, 1.0, A.e)
                if k > DA_K3 and (k % PS.CT.OGNI == 0):
                    rho = PS.MT.rho_di(Z)
                    R.etichette([PS.MT.centro_di(Z, rho)])
                acc += ritmo(mot, LC.cs_prec())
            cs1 = LC.cs_prec()
        finally:
            LC.spegni()
        trap = 0.5 * (A_K3 - DA_K3) * (ritmo(mot, cs0) + ritmo(mot, cs1))
        scala = float(np.max(np.abs(acc)))
        diff = float(np.max(np.abs(trap - acc)))
        top = np.abs(acc) >= 0.5 * scala
        rel_top = float(np.max(np.abs(trap - acc)[top] / np.abs(acc)[top]))
        print("### Theta su %d tick: max |accumulo| %.6e rad; max |trapezio - accumulo| %.3e (relativo alla scala %.3e); sugli archi con |Theta| >= meta' del massimo (%d): la differenza relativa massima %.3e" % (
            A_K3 - DA_K3, scala, diff, diff / scala, int(top.sum()), rel_top))
        f = os.path.join(DIR, "C2", "stato_%05d.npz" % A_K3)
        uguale = []
        with np.load(f) as d:
            for x in Z["chiavi"]:
                uguale.append((x, bool(np.array_equal(d[x], Z["st"][x]))))
            uguale.append(("campo_A", bool(np.array_equal(d["campo_A"], C.campo.A))))
            uguale.append(("campo_E", bool(np.array_equal(d["campo_E"], C.campo.E))))
            uguale.append(("cs_prec", bool(np.array_equal(d["cs_prec"], cs1))))
        print("### lo stato d'arrivo contro C2 stato_%05d: %s" % (A_K3, uguale))
        esiti.append(("K3: lo stato d'arrivo = C2 stato_%05d AL BIT (l'accumulo e' quello della corsa)" % A_K3, all(u for _x, u in uguale)))
        esiti.append(("K3: l'errore del trapezio stampato (Q-A5): relativo alla scala %.3e" % (diff / scala), True))
        np.savez(os.path.join(DIR, "torsione_K3.npz"), acc=acc, trap=trap)
        Z["metti"]()
    print("### %.0f s" % (time.time() - t00))
    return esiti


def k2():
    LC = PS.LC
    print("K2: IL LEGAME CON LA FASE VERA -- da C2 k 3000, %d tick" % TICK_K2)
    esiti = []
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        A = Avvio(Z, False)
        C, meta, cs0, s = A.da_stato("C2", 3000)
        print("### la ripresa da C2 stato_03000 (sha1 %s, ricontrollato)" % s[:8])
        mot = Z["mot"]
        r, _c, _mid = geometria_archi(Z, meta["centro"])
        PS.PO.accendi(cs0)
        mis = np.zeros(mot.inc.m)
        pre = np.zeros(mot.inc.m)
        try:
            R = A.corsa(C, meta["lab"], 3000)
            phi = Z["st"]["phi_h"].copy()
            for k in range(3001, 3001 + TICK_K2):
                R.passo(k, A.t0 + k, 1.0, A.e)
                nuovo = Z["st"]["phi_h"]
                d = np.angle(nuovo * np.conj(phi))
                mis += d[0::2] - d[1::2]
                pre += ritmo(mot, LC.cs_prec())
                phi = nuovo.copy()
        finally:
            LC.spegni()
        for nome, sel in (("oltre %.0f nodi (il mandato)" % OLTRE_K2, r > OLTRE_K2), ("fra 20 e 30 nodi (dichiarato accanto)", (r > 20) & (r <= 30)), ("fra 10 e 20 nodi (dichiarato accanto)", (r > 10) & (r <= 20))):
            p, q = pre[sel], mis[sel]
            sc = float(np.max(np.abs(p)))
            ok = np.abs(p) > 1e-3 * sc
            rap = q[ok] / p[ok]
            print("### %s: %d archi; la scala max |omega somma(dtau_i - dtau_j)| su %d tick %.3e rad; la fase relativa misurata: max %.3e, mediana |.| %.3e; il rapporto misurata/omega dtau (archi con |pre| > 1e-3 della scala, %d): mediana %+.4e, i quartili %+.4e %+.4e" % (
                nome, int(sel.sum()), TICK_K2, sc, float(np.max(np.abs(q))), float(np.median(np.abs(q))), int(ok.sum()), float(np.median(rap)), float(np.percentile(rap, 25)), float(np.percentile(rap, 75))))
            if nome.startswith("oltre"):
                esiti.append(("K2 (P-T5): il rapporto mediano entro 1%% da 1 oltre %.0f nodi" % OLTRE_K2, abs(float(np.median(rap)) - 1.0) <= 0.01))
        np.savez(os.path.join(DIR, "torsione_K2.npz"), mis=mis, pre=pre, r=r)
        Z["metti"]()
    return esiti


def carica_cs(nome, k):
    f = os.path.join(DIR, nome, "stato_%05d.npz" % k)
    with np.load(f) as d:
        return d["cs_prec"].copy(), json.loads(str(d["meta"]))


def cs_k0(Z, A, nome):
    """### `cs` a `k 0`: il `cs` del PRIMO tick dallo stato preparato (dichiarato)."""
    LC = PS.LC
    C, _meta = CSB.prepara(Z, 186, A.bordo, A.rho_c, A.e, A.t0)
    rho = PS.MT.rho_di(Z)
    PS.PO.accendi(None)
    try:
        R = A.corsa(C, [float(x) for x in PS.MT.centro_di(Z, rho)], 0)
        R.passo(1, A.t0 + 1, 1.0, A.e)
        return LC.cs_prec()
    finally:
        LC.spegni()


def misura():
    esiti = []
    out = {}
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        for nome, bordo in (("C2", False), ("C1", True)):
            A = Avvio(Z, bordo)
            cs = {0: cs_k0(Z, A, nome)}
            meta = None
            for k in STATI:
                cs[k], meta = carica_cs(nome, k)
            centro = meta["centro"]
            r, cosr, mid = geometria_archi(Z, centro)
            ks = (0,) + STATI
            R = {k: ritmo(mot, cs[k]) for k in ks}
            out[nome] = {"R": R, "r": r, "cos": cosr, "mid": mid, "ks": ks, "centro": centro}
        Z["metti"]()
    for nome in ("C2", "C1"):
        o = out[nome]
        R, r, cosr, ks = o["R"], o["r"], o["cos"], o["ks"]
        an = np.floor(r).astype(int)
        print("=" * 130)
        print("%s (centro %s)" % (nome, ["%.3f" % x for x in o["centro"]]))
        # ---------------------------------------------------- M1, M2
        print("M1-M2: il ritmo |pi (dtau_i - dtau_j)| per anello (rad per tick): la media, il massimo, la media sui radiali (entro 30 gradi) e sui tangenziali (oltre 60)")
        for k in (0, 250, 1500, 3000):
            a = np.abs(R[k])
            media = np.bincount(an, weights=a) / np.maximum(np.bincount(an), 1)
            mx = np.zeros(an.max() + 1)
            np.maximum.at(mx, an, a)
            rad, tan = cosr >= RADIALE_COS, cosr <= TANGENZIALE_COS
            mr = np.bincount(an[rad], weights=a[rad], minlength=an.max() + 1) / np.maximum(np.bincount(an[rad], minlength=an.max() + 1), 1)
            mt = np.bincount(an[tan], weights=a[tan], minlength=an.max() + 1) / np.maximum(np.bincount(an[tan], minlength=an.max() + 1), 1)
            i_med, i_arc = int(np.argmax(media)), int(np.argmax(a))
            print("  k %4d: il massimo per arco %.4e a r %.2f; l'anello della media massima %d (%.4e); oltre 40 nodi: il massimo per arco %.3e (%.3e del massimo)" % (
                k, float(a.max()), float(r[i_arc]), i_med, float(media[i_med]), float(a[r > 40].max()), float(a[r > 40].max() / a.max())))
            print("         gli anelli 0..45 (media; radiali; tangenziali):")
            for j0 in range(0, 46, 5):
                print("         " + "  ".join("%2d: %.2e %.2e %.2e" % (j, media[j], mr[j], mt[j]) for j in range(j0, min(j0 + 5, 46))))
            if nome == "C2" and k == 3000:
                esiti.append(("P-T1: il ritmo massimo per arco fra 10 e 22 nodi dal baricentro (C2 k 3000: r %.2f)" % float(r[i_arc]), 10.0 <= float(r[i_arc]) <= 22.0))
                esiti.append(("P-T4: oltre 40 nodi il ritmo sotto l'1%% del massimo (C2 k 3000: %.3e)" % float(a[r > 40].max() / a.max()), float(a[r > 40].max() / a.max()) < 0.01))
        # ---------------------------------------------------- M3
        Th = np.zeros_like(R[0])
        primo = None
        for k0, k1_ in zip(ks[:-1], ks[1:]):
            dT = 0.5 * (k1_ - k0) * (R[k0] + R[k1_])
            nuovo = Th + dT
            sopra = (np.abs(nuovo) >= 2 * math.pi) & (np.abs(Th) < 2 * math.pi)
            if sopra.any() and primo is None:
                # ### l'interpolazione LINEARE nel tratto (il trapezio: Theta e' quadratico nel tratto; dichiarato)
                fr = (2 * math.pi - np.abs(Th[sopra])) / np.abs(dT[sopra])
                q = int(np.argmin(fr))
                primo = (int(np.where(sopra)[0][q]), k0 + float(fr[q]) * (k1_ - k0))
            Th = nuovo
        a3 = np.abs(R[3000])
        print("M3: Theta accumulata da k 0 a 3000 (il trapezio sugli stati ogni 250; l'errore in K3): max |Theta| %.4e rad (%.4f di 2 pi) all'arco a r %.2f; archi oltre 2 pi entro 3000: %d" % (
            float(np.abs(Th).max()), float(np.abs(Th).max() / (2 * math.pi)), float(r[int(np.argmax(np.abs(Th)))]), int(np.sum(np.abs(Th) >= 2 * math.pi))))
        print("    il primo arco a 2 pi: %s" % ("l'arco %d a r %.2f al tick %.0f" % (primo[0], float(r[primo[0]]), primo[1]) if primo else "nessuno entro 3000"))
        for T in (1e4, 1e5):
            prog = np.abs(Th + R[3000] * (T - 3000))
            print("    al ritmo di fine corsa (lineare da k 3000): archi oltre 2 pi entro %.0e tick: %d (il piu' lontano dal centro a r %.2f)" % (T, int(np.sum(prog >= 2 * math.pi)), float(r[prog >= 2 * math.pi].max()) if np.any(prog >= 2 * math.pi) else float("nan")))
        tmin = 2 * math.pi / float(a3.max())
        print("    il tempo minimo 2 pi / ritmo massimo (k 3000): %.1f tick" % tmin)
        if nome == "C2":
            t_primo = primo[1] if primo else 3000.0 + float(np.min((2 * math.pi - np.abs(Th)) / np.maximum(a3, 1e-300)))
            esiti.append(("P-T2: il primo arco a 2 pi (o al ritmo misurato) fra 100 e 10000 tick (C2: %.0f)" % t_primo, 100.0 <= t_primo <= 10000.0))
        # ---------------------------------------------------- M4
        i_med = int(np.argmax(np.bincount(an, weights=a3) / np.maximum(np.bincount(an), 1)))
        sel = an == i_med
        prime = np.mean([np.mean(np.abs(R[k][sel])) for k in (0, 250, 500)])
        ultime = np.mean([np.mean(np.abs(R[k][sel])) for k in (2500, 2750, 3000)])
        print("M4: all'anello del massimo (%d): il ritmo medio sulle prime 500 (k 0, 250, 500) %.4e, sulle ultime 500 (k 2500, 2750, 3000) %.4e: il rapporto %.4f" % (i_med, prime, ultime, ultime / prime))
        if nome == "C2":
            esiti.append(("P-T3: all'anello del massimo, ultime 500 contro prime 500 entro il 10%% (C2: %.4f)" % (ultime / prime), abs(ultime / prime - 1.0) <= 0.10))
        o["Th"] = Th
    # ---------------------------------------------------- M5
    print("=" * 130)
    a1, a2 = np.abs(out["C1"]["R"][3000]), np.abs(out["C2"]["R"][3000])
    print("M5: C1 (col bordo) contro C2 (senza), k 3000: il ritmo massimo %.4e contro %.4e (rapporto %.4f); max |Theta| %.4e contro %.4e" % (
        float(a1.max()), float(a2.max()), float(a1.max() / a2.max()), float(np.abs(out["C1"]["Th"]).max()), float(np.abs(out["C2"]["Th"]).max())))
    for k in (250, 1500, 3000):
        b1, b2 = np.abs(out["C1"]["R"][k]), np.abs(out["C2"]["R"][k])
        print("    k %4d: la differenza relativa massima del ritmo per arco (sugli archi sopra l'1%% del massimo di C2) %.3e" % (k, float(np.max(np.abs(b1 - b2)[b2 > 0.01 * b2.max()] / b2[b2 > 0.01 * b2.max()]))))
    # ---------------------------------------------------- M6
    figura(out["C2"])
    print("M6: la mappa di |Theta| a k 3000 (C2): torsione_tempo_proprio.png")
    return esiti


def figura(o):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    mid, Th, r = o["mid"], np.abs(o["Th"]), o["r"]
    sel = r <= 60.0
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    sc = ax.scatter(mid[sel, 0], mid[sel, 1], c=Th[sel], s=2, cmap="viridis", vmin=0.0)
    for R, st, nm in ((R_MATERIA, "--", "il raggio della materia 12.4"), (CONFINE, "-", "il confine dell'energia 23.81")):
        t = np.linspace(0, 2 * math.pi, 400)
        ax.plot(R * np.cos(t), R * np.sin(t), st, color="white", lw=1.0, label=nm)
    ax.add_patch(plt.Circle((0, 0), 2 * math.pi, fill=False, lw=0))
    ax.set_aspect("equal")
    ax.set_title("|Theta| a k 3000 (C2, senza bordo); 2 pi = %.3f" % (2 * math.pi))
    ax.set_xlabel("x (nodi, dal baricentro)")
    ax.set_ylabel("y")
    ax.legend(loc="upper right", fontsize=8)
    fig.colorbar(sc, ax=ax, label="|Theta| (rad)")
    fig.savefig(os.path.join(_QUI, "torsione_tempo_proprio.png"), dpi=110)


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "controllo_senza_bordo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA TORSIONE DEL TEMPO PROPRIO, SOLO MISURA (Luca 2026-11-17 18:04): %s" % argv[0])
    print("=" * 130)
    esiti = {"k1": k1, "k3": k3, "k2": k2, "misura": misura}[argv[0]]()
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
