# -*- coding: utf-8 -*-
r"""**[M2245-27] A4, LE TRE SFASATE: IL NUMERO DI VORTICE, LA CORRENTE CIRCOLANTE, Theta SUL GIRO** *(DECISIONE DI LUCA, 2026-11-27 22:45;
la carta `doc/CARTA_mitosi.md`, A4; il pezzo 0 di [M-GM]; solo letture, nessun tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/triangoli_vortice.py > doc/referti_l2/triangoli_vortice.txt

**Gli stati** *(`controllo/CHI/triangolo/{t120, t120r28, t000}`, `L 162`)*: `k 0` ricostruito con `triangolo_chi_v4.prepara` *(nessun tick)*, il primo
salvato *(`250`)*, uno ogni `5000`, l'ultimo. **`t120r28` ha le STESSE fasi e lo STESSO verso di `t120`: un «sinistro» con `chi` non c'e'** *(dichiarato)*.
**Il giro** = `triangolo_120.giro_di` *(la somma delle differenze di fase ridotte in `(-pi, pi]` su `N_CERCHIO` punti, la `psi` nel disco `R_DISCO`)*
sulla componente di norma massima, attorno al baricentro dei tre vertici, a `r` = il raggio CIRCOSCRITTO `R` *(il principale: la carta)*, `0.5 R`, `1.5 R`
e il raggio inscritto *(quello del DEVE di `triangolo_120`)*. **«Giro intero»** se `|g - round(g)| < 0.1` a `R`.
**`J_theta`** per anello `[0, R/2)`, `[R/2, R)`, `[R, 3R/2)`: `J_a = Im(somma_c conj(psi_i,c) psi_j,c)` sull'arco `a = (i, j)` *(SENZA il legame `A`:
dichiarato; `max |campo_A|` stampato)*, proiettata sulla tangente al punto medio dell'arco, media sugli archi dell'anello.
**`Theta` sul giro:** un cammino CHIUSO del grafo vicino al cerchio `R` *(i nodi piu' vicini a `N_CERCHIO` punti, uniti dai cammini minimi)*, ogni arco
col suo verso: **DEVE essere `0` entro `1e-9`** *(il caso noto, non una misura: l'errore n.261)*; **DEVE FALLIRE** con un campo d'arco a caso.
**Casi noti:** (K1) a `k 0` il giro di `t120` e' `+1` e quello di `t000` `0` *(a `R`)*; (K2) DEVE FALLIRE: `conj(psi)` di `t120` a `k 0` da' `-1`; (K3) `Theta`.
**[M-GM] D4:** se ne' `t120` ne' `t120r28` hanno un giro intero DIVERSO DA ZERO all'ultimo stato, [M-GM] si ferma qui.
"""
import collections
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "primo_ordine")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import triangolo_chi_v4 as TC  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "triangolo")
QUALI = ("t120", "t120r28", "t000")
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def stati_di(q):
    ks = sorted(int(f[6:12]) for f in os.listdir(os.path.join(BASE, q)) if f.startswith("stato_") and f.endswith(".npz"))
    scelti = [ks[0]] + [k for k in ks if k % 5000 == 0 and k not in (ks[0], ks[-1])] + [ks[-1]]
    return [(k, os.path.join(BASE, q, "stato_%06d.npz" % k)) for k in scelti]


class Geo:
    """### la geometria della scena: posizioni, archi, cammino chiuso, anelli."""

    def __init__(self, Z, centri):
        from solitone import toro as TO
        self.TO = TO
        self.L, self.n = Z["L"], Z["n"]
        self.m1, self.m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        inc = Z["mot"].inc
        self.ii, self.jj = np.asarray(inc.ii, int), np.asarray(inc.jj, int)
        self.righe = Z["righe"]
        self.cen = (sum(c[0] for c in centri) / 3.0, sum(c[1] for c in centri) / 3.0)
        d = np.asarray(TO.scarti(self.m1, self.m2, self.cen[0], self.cen[1], self.L))[:, :2]
        dv = [np.asarray(TO.scarti(np.array([float(c[0])]), np.array([float(c[1])]), self.cen[0], self.cen[1], self.L))[0, :2] for c in centri]
        self.R = float(np.mean([np.hypot(*v) for v in dv]))
        mezzi = [((centri[a][0] + centri[b][0]) / 2.0, (centri[a][1] + centri[b][1]) / 2.0) for a, b in ((0, 1), (1, 2), (2, 0))]
        self.r_in = float(np.mean([np.hypot(*np.asarray(TO.scarti(np.array([q[0]]), np.array([q[1]]), self.cen[0], self.cen[1], self.L))[0, :2]) for q in mezzi]))
        # ### gli archi: il vettore (j - i) e il punto medio rispetto al centro
        e = np.asarray(TO.piu_vicina(self._diff(self.jj, self.ii), self.L))[:, :2]
        pm = d[self.ii] + 0.5 * e
        rr = np.hypot(pm[:, 0], pm[:, 1])
        tx, ty = -pm[:, 1] / np.maximum(rr, 1e-300), pm[:, 0] / np.maximum(rr, 1e-300)
        self.proiez = (e[:, 0] * tx + e[:, 1] * ty) / np.maximum(np.hypot(e[:, 0], e[:, 1]), 1e-300)
        self.r_arco = rr
        self.anelli = ((0.0, 0.5 * self.R), (0.5 * self.R, self.R), (self.R, 1.5 * self.R))
        self.cammino = self._cammino(d)

    def _diff(self, a, b):
        A1, A2 = self.TO.vettori()
        d1 = ((self.m1[a] - self.m1[b] + 0.5 * self.L) % self.L) - 0.5 * self.L
        d2 = ((self.m2[a] - self.m2[b] + 0.5 * self.L) % self.L) - 0.5 * self.L
        return d1[:, None] * A1 + d2[:, None] * A2

    def _cammino(self, d):
        """### `[(arco, segno)]` di un cammino chiuso vicino al cerchio `R`."""
        import triangolo_120 as T1
        vic = collections.defaultdict(list)
        for a, (i, j) in enumerate(zip(self.ii, self.jj)):
            vic[i].append((j, a, +1))
            vic[j].append((i, a, -1))
        punti = []
        for t in range(T1.N_CERCHIO):
            th = 2.0 * math.pi * t / T1.N_CERCHIO
            p = np.array([self.R * math.cos(th), self.R * math.sin(th)])
            punti.append(int(np.argmin(np.hypot(d[:, 0] - p[0], d[:, 1] - p[1]))))
        archi = []
        for s, t in zip(punti, punti[1:] + punti[:1]):
            if s == t:
                continue
            prec = {s: None}
            coda = collections.deque([s])
            while coda and t not in prec:
                u = coda.popleft()
                for v, a, sg in vic[u]:
                    if v not in prec:
                        prec[v] = (u, a, sg)
                        coda.append(v)
            tratto, v = [], t
            while prec[v] is not None:
                u, a, sg = prec[v]
                tratto.append((a, sg))
                v = u
            archi += tratto[::-1]
        return archi

    def giro_theta(self, campo):
        return float(sum(sg * campo[a] for a, sg in self.cammino))

    def psi(self, psi_h):
        return psi_h[self.righe].reshape(self.n, -1)

    def giri(self, psi_n):
        import triangolo_120 as T1
        g = int(np.argmax(np.sum(np.abs(psi_n) ** 2, axis=0)))
        out = {}
        for nome, r in (("R", self.R), ("0.5R", 0.5 * self.R), ("1.5R", 1.5 * self.R), ("r_in", self.r_in)):
            out[nome] = float(T1.giro_di(psi_n[:, [g]], self.m1, self.m2, self.L, self.cen, r)[0])
        out["somma@R"] = float(T1.giro_di(psi_n.sum(axis=1, keepdims=True), self.m1, self.m2, self.L, self.cen, self.R)[0])
        return g, out

    def j_theta(self, psi_n):
        J = np.imag(np.sum(np.conj(psi_n[self.ii]) * psi_n[self.jj], axis=1))
        Jt = J * self.proiez
        return [float(Jt[(self.r_arco >= a) & (self.r_arco < b)].mean()) for a, b in self.anelli]


def intero(g):
    return abs(g - round(g)) < 0.1


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "triangolo_chi_v4.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2245-27] A4, LE TRE SFASATE (la carta doc/CARTA_mitosi.md, A4; il pezzo 0 di [M-GM]): il giro di fase, J_theta, Theta sul giro")
    print("=" * 130)
    ultimo = {}
    rng = np.random.default_rng(20261127)
    for q in QUALI:
        with TC.scena() as Z:
            C, info = TC.prepara(Z, q)
            G = Geo(Z, info["centri"])
            print("-" * 130)
            print("### %s: i vertici %s, le fasi %s gradi; il centro (%.3f, %.3f); R circoscritto %.4f, r inscritto %.4f; il cammino chiuso %d archi" % (
                q, info["centri"], ["%.1f" % x for x in info["fasi_gradi"]], G.cen[0], G.cen[1], G.R, G.r_in, len(G.cammino)))
            p0 = G.psi(Z["st"]["psi_h"])
            g, gi = G.giri(p0)
            print("    k      0 (prepara): la componente %2d; il giro a R %+.4f, 0.5R %+.4f, 1.5R %+.4f, r_in %+.4f; la somma delle componenti a R %+.4f" % (
                g, gi["R"], gi["0.5R"], gi["1.5R"], gi["r_in"], gi["somma@R"]))
            if q == "t120":
                esito("(K1) t120 a k 0: il giro a R = +1 (entro 0.1)", abs(gi["R"] - 1.0) < 0.1, "%+.4f" % gi["R"])
                gc, gic = G.giri(np.conj(p0))
                esito("(K2) DEVE FALLIRE il +1: conj(psi) di t120 a k 0 da' -1 (entro 0.1)", abs(gic["R"] + 1.0) < 0.1, "%+.4f" % gic["R"])
            if q == "t000":
                esito("(K1) t000 a k 0: il giro a R = 0 (entro 0.1)", abs(gi["R"]) < 0.1, "%+.4f" % gi["R"])
            caso = rng.standard_normal(len(G.ii))
            esito("(K3) %s: DEVE FALLIRE lo zero: un campo d'arco a caso sul cammino chiuso NON somma a zero" % q, abs(G.giro_theta(caso)) > 1e-3, "%+.4e" % G.giro_theta(caso))
            print("    k        giro a R   0.5R     1.5R     r_in    somma@R  comp   J_theta [0,R/2)  [R/2,R)     [R,3R/2)    Theta sul giro   max|Theta|  max|A|")
            for k, f in stati_di(q):
                with np.load(f, allow_pickle=True) as z:
                    psi_h, th, cA = z["psi_h"], z["theta_a"].copy(), z["campo_A"].copy()
                    pn = G.psi(psi_h)
                g, gi = G.giri(pn)
                jt = G.j_theta(pn)
                tg = G.giro_theta(th)
                esito("(K3) %s k %d: Theta sommato sul cammino chiuso = 0 entro 1e-9" % (q, k), abs(tg) < 1e-9, "%+.3e" % tg)
                print("    %6d  %+8.4f %+8.4f %+8.4f %+8.4f %+8.4f   %2d    %+.4e  %+.4e  %+.4e   %+.3e       %.4f      %.3e" % (
                    k, gi["R"], gi["0.5R"], gi["1.5R"], gi["r_in"], gi["somma@R"], g, jt[0], jt[1], jt[2], tg, float(np.max(np.abs(th))), float(np.max(np.abs(cA)))))
                ultimo[q] = (k, gi["R"])
            Z["metti"]()
    print("=" * 130)
    for q in QUALI:
        k, g = ultimo[q]
        print("### %s all'ultimo stato (k %d): il giro a R %+.4f -> %s" % (q, k, g, ("INTERO, n = %+d" % round(g)) if intero(g) else "NON INTERO"))
    vivi = [q for q in ("t120", "t120r28") if intero(ultimo[q][1]) and round(ultimo[q][1]) != 0]
    print("### [M-GM] D4: %s" % ("si prosegue: un giro intero diverso da zero in %s" % vivi if vivi else "NESSUNA delle sfasate ha un giro intero diverso da zero all'ultimo stato: [M-GM] SI FERMA QUI"))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
