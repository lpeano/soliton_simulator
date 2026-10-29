# -*- coding: utf-8 -*-
r"""**LA DIAGNOSI COL FILTRO SULLE BANDE PIATTE** *(NON una cura; il mandato di Luca delle `10:22` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_filtro_bande_piatte.md`)*: ### **uno strumento di DIAGNOSI, mai nel nucleo.**
### **La corsa dallo stato fermo di `S1`; a ogni tick, dopo il tick, la proiezione sulle bande piatte** *(`P0`, `Ppi`: gli autovettori del tick libero)* ### **tolta, e `psi` rinormalizzata a `N`.**
### **L'esame di `5f06dbfb`, rispetto allo stato fermo e allo stato fermo filtrato una volta.**

> ### **Il filtro non e' locale e rompe le conservazioni: una prova del canale, non una modifica del modello.**

    python csv/_filtro_bande_piatte.py --referto > doc/referti_l2/filtro_bande_piatte.txt
"""
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

CASI = ("S1_s0.300", "S1_s0.150")
PIATTE = (0, 1, 2, 3, 6, 7, 8, 9)   # ### Ppi e P0 per indice di fase (_dove_va_la_materia.GRUPPI)
T_FIS = 180.0
T_DA_FIS = 60.0
PASSO_FIS = 3.0
FATTORE_RUMORE = 1e3
SATURAZIONE = 1e-2
SOGLIE_FORMA = (1e-4, 1e-3)
TOLL_PARSEVAL = 1e-12
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


class Filtro:
    """### **Toglie da `psi` la proiezione sulle piatte** *(per impulso: `fft2`, `Z(k)^H`, a zero gli indici `PIATTE`, `Z(k)`, `ifft2`)*."""

    def __init__(self, Z, L, n):
        self.Z, self.L, self.n = Z, L, n
        self.tieni = np.ones(12)
        self.tieni[list(PIATTE)] = 0.0

    def __call__(self, psi_h):
        L = self.L
        f = np.fft.fft2(psi_h.reshape(L, L, 12), axes=(0, 1))
        c = np.einsum("abji,abj->abi", self.Z.conj(), f) * self.tieni
        g = np.fft.ifft2(np.einsum("abij,abj->abi", self.Z, c), axes=(0, 1))
        return g.reshape(psi_h.shape)

    def peso_piatte(self, psi_h):
        L = self.L
        f = np.fft.fft2(psi_h.reshape(L, L, 12), axes=(0, 1))
        c = np.einsum("abji,abj->abi", self.Z.conj(), f)
        P = np.abs(c) ** 2 / (L * L)
        return float(P[:, :, list(PIATTE)].sum()), float(P.sum())


def esame(nome, ts, Dd, n0, r1, s, v, Z, L, etichetta):
    import _dove_va_la_materia as DV
    import _modo_instabile as MI
    ogni = int(round(PASSO_FIS / s))
    nD = np.array([float(np.linalg.norm(Dd[t])) / n0 for t in ts])
    print("  [%s] |D|/|psi0| ogni %d tick da %d: %s" % (etichetta, ogni, ts[0], " ".join("%.1e" % x for x in nD)))
    fin = [i for i in range(len(ts)) if FATTORE_RUMORE * r1 < nD[i] < SATURAZIONE]
    if len(fin) < 3:
        print("  [%s] la finestra lineare ha %d campioni: il tasso non si misura" % (etichetta, len(fin)))
        return None
    a, b = fin[0], fin[-1]
    tt = np.array(ts[a:b + 1], dtype=float)
    pend = float(np.polyfit(tt, np.log(nD[a:b + 1]), 1)[0])
    print("  [%s] la finestra: t %d .. %d (tempo %.0f .. %.0f); il tasso %.5f per tick, %.5f per unita' di tempo" % (etichetta, ts[a], ts[b], ts[a] * s, ts[b] * s, pend, pend / s))
    tc = ts[(a + b) // 2]
    proj = [float(np.real(np.vdot(Dd[tc], Dd[t]))) / (float(np.linalg.norm(Dd[tc])) * float(np.linalg.norm(Dd[t]))) for t in ts[a:b + 1]]
    cambi = [i for i in range(1, len(proj)) if proj[i - 1] * proj[i] < 0.0]
    if len(cambi) >= 2:
        print("  [%s] il periodo: %.2f unita' di tempo (%d cambi)" % (etichetta, 2.0 * ogni * float(np.mean(np.diff(cambi))) * s, len(cambi)))
    else:
        print("  [%s] %d cambi di segno: il periodo non si misura" % (etichetta, len(cambi)))
    istanti = []
    for so in SOGLIE_FORMA:
        c = [t for t, x in zip(ts, nD) if x >= so]
        if c:
            istanti.append(c[0])
    istanti.append(ts[b])
    for t in sorted(set(istanti)):
        dd = Dd[t] / float(np.linalg.norm(Dd[t]))
        _dr, _df = MI.per_nodo(v, dd)
        wd, kk = MI.armoniche(v, _dr)
        prd = np.bincount(kk, weights=np.sum(np.abs(dd.reshape(v.n, 12)) ** 2, axis=1))
        prd = prd / prd.sum()
        top = np.argsort(-prd)[:3]
        Pk = DV.pesi(dd.reshape(v.n, 12), np.ones(v.n), Z, L)
        tot = float(Pk.sum())
        print("  [%s] t %d (tempo %.0f, |D|/|psi0| %.1e): gli anelli maggiori %s; le bande %s"
              % (etichetta, t, t * s, float(np.linalg.norm(Dd[t])) / n0, ", ".join("r %d %.3f" % (k, prd[k]) for k in top),
                 "  ".join("%s %.3f" % (g, float(Pk[:, :, list(idx)].sum()) / tot) for g, idx in DV.GRUPPI)))
    return pend / s


def corsa(nome):
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    _n, forma, s, N = MS.caso(nome)
    print("-" * 130)
    psi0, mu, cj, ok = MS.carica(nome)
    print("### %s: %s, s %g, N %g, L %d; mu %+.9f; il residuo dello stato fermo %.3e" % (nome, forma, s, N, MS.L, mu, cj["residuo_finale"]))
    esito("DEVE PASSARE: %s, lo stato fermo sul disco = quello della ricerca (sha1)" % nome, ok and cj["convergito"], "")
    with D.configura(forma, s, N):
        rec, z, phi0, _p0 = MS.scena(forma, s, N)
        L = MS.L
        n = z["inc"].n
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
        fl = Filtro(Z, L, n)
        pp, tot = fl.peso_piatte(psi0)
        M0 = float(np.sum(np.abs(psi0) ** 2))
        esito("DEVE PASSARE: %s, i pesi per banda sommano a |psi0|^2 (Parseval) entro %g" % (nome, TOLL_PARSEVAL), abs(tot / M0 - 1.0) < TOLL_PARSEVAL, "%.1e" % abs(tot / M0 - 1.0))
        psi0f = fl(psi0)
        psi0f *= math.sqrt(M0 / float(np.sum(np.abs(psi0f) ** 2)))
        print("  il controllo (punto 4): la frazione di |psi0|^2 nelle piatte %.4e; |psi0f - psi0| / |psi0| %.4e" % (pp / M0, float(np.linalg.norm(psi0f - psi0)) / math.sqrt(M0)))
        ogni = int(round(PASSO_FIS / s))
        t_fine = int(round(T_FIS / s))
        t_da = int(round(T_DA_FIS / s))
        psi = psi0.copy()
        Dd, Df = {}, {}
        tolta = []
        s0 = time.time()
        for t in range(1, t_fine + 1):
            psi = MS.tick(z, phi0, psi, forma)
            q = fl(psi)
            nt = float(np.sum(np.abs(q) ** 2))
            tolta.append((M0 - nt) / M0)
            psi = q * math.sqrt(M0 / nt)
            if t % ogni == 0 and t >= t_da:
                rot = np.exp(1j * mu * s * t)
                Dd[t] = rot * psi - psi0
                Df[t] = rot * psi - psi0f
        print("  la corsa filtrata: %d tick in %.0f s" % (t_fine, time.time() - s0))
        tl = np.array(tolta)
        print("  la norma tolta per tick (frazione di N), ogni %d tick: %s" % (ogni, " ".join("%.1e" % x for x in tl[ogni - 1::ogni])))
        print("  la norma tolta: il totale %.4e di N; il primo tick %.3e; il massimo %.3e (tick %d); la media degli ultimi %d tick %.3e"
              % (float(tl.sum()), tl[0], float(tl.max()), int(np.argmax(tl)) + 1, 10 * ogni, float(tl[-10 * ogni:].mean())))
        v = MS.Vista(z, psi0)
    n0 = math.sqrt(M0)
    ts = sorted(Dd)
    r1 = cj["residuo_finale"]
    t1 = esame(nome, ts, Dd, n0, r1, s, v, Z, L, "D rispetto a psi0")
    t2 = esame(nome, ts, Df, n0, r1, s, v, Z, L, "D rispetto a psi0f")
    return nome, s, t1, t2


def referto():
    print("=" * 130)
    print("LA DIAGNOSI COL FILTRO SULLE BANDE PIATTE (Luca 10:22; NON una cura): a ogni tick la proiezione su P0 e Ppi tolta e psi rinormalizzata; l'esame di 5f06dbfb")
    print("=" * 130)
    print("  la configurazione: CASI %s PIATTE %s T_FIS %g T_DA_FIS %g PASSO_FIS %g FATTORE_RUMORE %g SATURAZIONE %g SOGLIE_FORMA %s TOLL_PARSEVAL %g"
          % (CASI, PIATTE, T_FIS, T_DA_FIS, PASSO_FIS, FATTORE_RUMORE, SATURAZIONE, SOGLIE_FORMA, TOLL_PARSEVAL))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (a) col filtro il modo sparisce o il tasso cala molto: le piatte sono il canale; (b) resta con lo stesso tasso: il canale e' un altro; (c) il filtro cambia troppo lo stato fermo; (d) altro")
    print("  SENZA FILTRO (dfb5ab7e): il tasso 0.13870 a s 0.3, 0.15108 a s 0.15 per unita' di tempo")
    righe = [corsa(c) for c in CASI]
    print("-" * 130)
    print("### LA SINTESI (il tasso per unita' di tempo, col filtro)")
    for nome, s, t1, t2 in righe:
        print("  %s s %.2f: rispetto a psi0 %s; rispetto a psi0f %s" % (nome, s, ("%.5f" % t1) if t1 is not None else "--", ("%.5f" % t2) if t2 is not None else "--"))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        if argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
