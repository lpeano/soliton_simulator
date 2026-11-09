# -*- coding: utf-8 -*-
r"""**T4-B, LA VISIBILITA' ALLA BREZZI DELLE BANDE DI `U`** *(il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `16`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t4b.py > doc/referti_l2/u1_t4b.txt

**Lo sfondo:** l'onda piana UNIFORME di `psi` a `K` sul toro `24 x 24` *(`scena_materia` senza la gaussiana)*, `s = 0.15`, il campo non compatto, la convenzione `oggi`.
**(->) il campo visto dalla materia:** `delta x = eps Re[u_b e^{i k r}]` sugli `A`, `E`; un tick accoppiato a `+-eps`; `V = |psi_+ - psi_-| / (2 |delta x|)`.
**(<-) la materia vista dal campo:** `delta psi = eps psi_0 cos(k r)` *(ampiezza)* e `i eps psi_0 cos(k r)` *(fase)*; la differenza dei campi proiettata sulle bande a `+-k`
con gli autovettori SINISTRI delle bande fisiche *(la gauge e' il resto)*; `V = |la parte della banda| / (2 |delta psi|)`.
**I DEVE:** `T4B-R` *(servizio: lo stesso tick due volte dallo stesso stato, al bit)*; `T4B-S` *(servizio: `s_a = s` su ogni arco, se no le bande di `blocchi_campo(s)` non sono quelle)*;
`T4B-L` *(la linearita': `eps` `1e-4` e `5e-5` entro `1e-6` relativo, fotone, due versi, ogni `k`)*; `T4B-F` *(DEVE FALLIRE: a `e = 0` il fotone visibile)*; `T4B-P` *(a `e*` il minimo su `k` sopra `1000` volte il pavimento)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

L = 24                         # ### sez. 16 (L_MAT, multiplo di 3)
S = 0.15                       # ### sez. 16
EPS = (1e-4, 5e-5)             # ### sez. 16: T4B-L
TOLL_L = 1e-6                  # ### sez. 16
FATT_P = 1000.0                # ### sez. 16: T4B-P
CONV = "oggi"                  # ### sez. 16: il nucleo del principale
N_K = range(1, 13)             # ### sez. 16
DIREZ = ((1, 0), (1, 1))       # ### sez. 16
BANDE = ("fotone", "ottica", "gauge A", "gauge E")
FISICHE = ("fotone", "ottica")
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


def scena(U1, e):
    """### `scena_materia` con la gaussiana `= 1`: l'onda piana uniforme, norma `1`."""
    _inc, mot, st, par, c = U1.scena_materia(S, L, e, "noncompatto")
    n = mot.inc.n
    v = np.arange(n)
    m1, m2 = v // L, v % L
    cel = np.ones(n)[:, None] * U1.u_K(S)[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
    cel /= np.sqrt(np.sum(np.abs(cel) ** 2))
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    return mot, st, par, c, m1, m2


class Banco(object):
    """### Lo stato dello sfondo fotografato, e un tick accoppiato da li' con una perturbazione."""

    def __init__(self, U1, e):
        self.U1 = U1
        self.mot, self.st, self.par, self.c, self.m1, self.m2 = scena(U1, e)
        self.foto = {k: v.copy() for k, v in self.st.items()}
        self.A0, self.E0 = self.c.A.copy(), self.c.E.copy()

    def tick(self, dA=None, dE=None, dpsi=None):
        U1, st, c = self.U1, self.st, self.c
        for k, v in self.foto.items():
            st[k][...] = v
        c.A[...] = self.A0 + (0 if dA is None else dA)
        c.E[...] = self.E0 + (0 if dE is None else dE)
        if dpsi is not None:
            st["psi_h"][...] += dpsi
        U1.scrivi_U(self.mot, c)
        with U1.avvolto(self.mot, c, True):
            U1.tick(st, self.mot, self.par, c)
        return st["psi_h"].copy(), c.A.copy(), c.E.copy()


def bande_k(U1, bl, t1, t2):
    """### Le fasi e gli autovettori del tick libero a `k`: la gauge `|lambda - 1| <= GAUGE_VICINO`; delle altre `4`, le due di fase piu' piccola il fotone, le altre l'ottica.
    ### Gli autovettori SINISTRI delle bande fisiche normalizzati `w^H u = 1`."""
    M = U1.blocco_k(bl, t1, t2)
    lam, R = np.linalg.eig(M)
    gau = np.abs(lam - 1.0) <= U1.GAUGE_VICINO
    fis = np.flatnonzero(~gau)
    assert len(fis) == 4, "le fasi fuori dalla gauge non sono 4: %s" % lam
    fis = fis[np.argsort(np.abs(np.angle(lam[fis])), kind="stable")]
    lamH, Wl = np.linalg.eig(M.conj().T)
    out = {}
    for nome, idx in (("fotone", fis[:2]), ("ottica", fis[2:])):
        uu, ww = [], []
        for i in idx:
            j = int(np.argmin(np.abs(lamH - np.conj(lam[i]))))
            w = Wl[:, j] / np.conj(np.vdot(Wl[:, j], R[:, i]))
            uu.append(R[:, i])
            ww.append(w)
        out[nome] = (lam[idx], uu, ww)
    return out, int(np.sum(gau)), lam


def main():
    import _presidio
    import _u1_prototipo as U1
    import _triangoli_forza as TF
    import flussi_parziali as FP
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    estar = U1.E_PROVA[1]
    E_LISTA = (estar, estar / 2.0, 0.0)
    pav_ar = np.finfo(float).eps / EPS[0]
    print("=" * 130)
    print("T4-B, LA VISIBILITA' ALLA BREZZI DELLE BANDE DI U (sez. 16): L %d, s %g, e %s, eps %s, conv %s; k = 2 pi n d / L, n %s, d %s; l'arrotondamento eps_macchina/eps %.2e"
          % (L, S, ["%.10f" % e for e in E_LISTA], EPS, CONV, list(N_K), DIREZ, pav_ar))
    print("=" * 130)
    bl, fuori, ricostr = U1.blocchi_campo(S)
    print("### i blocchi del tick libero a s %g: oltre +-%d celle %.1e, la ricostruzione %.1e" % (S, U1.SUPPORTO, fuori, ricostr))
    ris = {}
    with TF.conv(CONV):
        for e in E_LISTA:
            B = Banco(U1, e)
            c = B.c
            n, m = c.n, c.m
            if e == E_LISTA[0]:
                sa = FP.s_arco(B.mot)
                esito("T4B-S s_a = s su ogni arco (le bande di blocchi_campo(s) sono quelle del tick accoppiato)", float(np.max(np.abs(sa - S))) <= 4 * np.finfo(float).eps,
                      "max|s_a - s| %.2e" % float(np.max(np.abs(sa - S))))
                p1, a1, e1 = B.tick()
                p2, a2, e2 = B.tick()
                esito("T4B-R lo stesso tick due volte dallo stesso stato: psi, A, E al bit", np.array_equal(p1, p2) and np.array_equal(a1, a2) and np.array_equal(e1, e2), "")
                print("  lo sfondo in un tick: max|A| %.3e, max|E| %.3e (la sorgente dell'onda piana uniforme)" % (float(np.max(np.abs(a1))), float(np.max(np.abs(e1)))))
            D = c.matrice_div()
            r1n, r2n = B.m1, B.m2
            nodo = B.mot.inc.nodo
            psi0 = B.foto["psi_h"]
            for d in DIREZ:
                for nk in N_K:
                    t1, t2 = 2 * math.pi * nk * d[0] / L, 2 * math.pi * nk * d[1] / L
                    bk, ngau, lam = bande_k(U1, bl, t1, t2)
                    fase = t1 * r1n + t2 * r2n
                    # ---------------- (->) le perturbazioni del campo
                    pert = {}
                    for nome in FISICHE:
                        u = bk[nome][1][0]
                        u = u * np.exp(-1j * np.angle(u[int(np.argmax(np.abs(u)))]))
                        x = np.zeros(2 * m)
                        for i in range(6):
                            x[(i // 3) * m + 3 * np.arange(n) + (i % 3)] = np.real(u[i] * np.exp(1j * fase))
                        pert[nome] = (x[:m], x[m:])
                    grad = D.T @ np.cos(fase)
                    pert["gauge A"] = (grad, np.zeros(m))
                    pert["gauge E"] = (np.zeros(m), grad)
                    for nome in BANDE:
                        dA, dE = pert[nome]
                        nx = float(np.sqrt(np.sum(dA * dA) + np.sum(dE * dE)))
                        for ep in EPS:
                            pp = B.tick(dA=ep * dA / nx, dE=ep * dE / nx)[0]
                            pm = B.tick(dA=-ep * dA / nx, dE=-ep * dE / nx)[0]
                            ris[(e, d, nk, "->", nome, ep)] = float(np.sqrt(np.sum(np.abs(pp - pm) ** 2))) / (2 * ep)
                    # ---------------- (<-) le perturbazioni della materia
                    cosn = np.cos(fase)[nodo]
                    kk = [(t1, t2)]
                    if not (abs(math.remainder(2 * t1, 2 * math.pi)) < 1e-12 and abs(math.remainder(2 * t2, 2 * math.pi)) < 1e-12):
                        kk.append((-t1, -t2))
                    for pnome, fatt in (("ampiezza", 1.0), ("fase", 1j)):
                        dpsi = fatt * psi0 * cosn[:, None]
                        npsi = float(np.sqrt(np.sum(np.abs(dpsi) ** 2)))
                        for ep in EPS:
                            _, ap, eP = B.tick(dpsi=ep * dpsi / npsi)
                            _, am, eM = B.tick(dpsi=-ep * dpsi / npsi)
                            dX = np.concatenate([ap - am, eP - eM]) / (2 * ep)
                            tot2 = float(np.sum(dX * dX))
                            parte = {nm: 0.0 for nm in FISICHE + ("gauge",)}
                            cattur = 0.0
                            for (s1, s2) in kk:
                                bks = bk if (s1, s2) == (t1, t2) else bande_k(U1, bl, s1, s2)[0]
                                ph = np.exp(-1j * (s1 * r1n + s2 * r2n))
                                xh = np.array([np.sum(dX[(i // 3) * m + 3 * np.arange(n) + (i % 3)] * ph) for i in range(6)]) / (L * L)
                                cattur += L * L * float(np.vdot(xh, xh).real)
                                resto = xh.copy()
                                for nm in FISICHE:
                                    vec = sum(uu * np.vdot(ww, xh) for uu, ww in zip(bks[nm][1], bks[nm][2]))
                                    resto = resto - vec
                                    parte[nm] += L * L * float(np.vdot(vec, vec).real)
                                parte["gauge"] += L * L * float(np.vdot(resto, resto).real)
                            for nm, v in parte.items():
                                ris[(e, d, nk, "<-" + pnome, nm, ep)] = math.sqrt(v)
                            ris[(e, d, nk, "<-" + pnome, "quota", ep)] = cattur / tot2 if tot2 > 0 else float("nan")
                    if e == E_LISTA[0]:
                        print("  e* d %s n %2d: le fasi %s; nella gauge %d" % (d, nk, " ".join("%+.5f" % a for a in np.sort(np.angle(lam))), ngau))
                        sys.stdout.flush()
    # ------------------------------------------------------------------ le tabelle
    for e in E_LISTA:
        print("-" * 130)
        print("### e = %.10f: V a eps %g (->: |psi_+ - psi_-|/(2|dx|); <-: la parte della banda/(2|dpsi|), la quota catturata da +-k)" % (e, EPS[0]))
        print("  %6s %3s | %11s %11s %11s %11s | %11s %11s %11s %7s | %11s %11s %11s %7s" % ("d", "n", "-> fotone", "-> ottica", "-> gauge A", "-> gauge E",
              "<-amp fot", "<-amp ott", "<-amp gau", "quota", "<-fase fot", "<-fase ott", "<-fase gau", "quota"))
        for d in DIREZ:
            for nk in N_K:
                g = lambda ver, b: ris[(e, d, nk, ver, b, EPS[0])]  # noqa: E731
                print("  %6s %3d | %11.4e %11.4e %11.4e %11.4e | %11.4e %11.4e %11.4e %7.4f | %11.4e %11.4e %11.4e %7.4f" % (
                    "%d,%d" % d, nk, g("->", "fotone"), g("->", "ottica"), g("->", "gauge A"), g("->", "gauge E"),
                    g("<-ampiezza", "fotone"), g("<-ampiezza", "ottica"), g("<-ampiezza", "gauge"), g("<-ampiezza", "quota"),
                    g("<-fase", "fotone"), g("<-fase", "ottica"), g("<-fase", "gauge"), g("<-fase", "quota")))
    print("-" * 130)
    VERSI = ("->", "<-ampiezza", "<-fase")

    def fot(e, ver, ep):
        return [ris[(e, d, nk, ver, "fotone", ep)] for d in DIREZ for nk in N_K]
    peg = 0.0
    for ver in VERSI:
        a, b = np.array(fot(estar, ver, EPS[0])), np.array(fot(estar, ver, EPS[1]))
        peg = max(peg, float(np.max(np.abs(a - b) / np.maximum(np.abs(a), np.finfo(float).tiny))))
    esito("T4B-L la linearita' a e*: V del fotone a eps %g e %g, entro %g relativo, nei tre versi, a ogni k" % (EPS[0], EPS[1], TOLL_L), peg <= TOLL_L, "%.3e" % peg)
    z = max(max(fot(0.0, ver, ep)) for ver in VERSI for ep in EPS)
    esito("T4B-F a e = 0 il fotone e' visibile (V > 0 in qualche verso, a qualche k)", z > 0.0, "max V a e = 0: %.3e" % z, deve=False)
    pav = max(z, pav_ar)
    for ver in VERSI:
        mn = min(fot(estar, ver, EPS[0]))
        esito("T4B-P a e* il minimo su k di V del fotone (%s) sopra %g x il pavimento %.2e" % (ver, FATT_P, pav), mn > FATT_P * pav, "min %.4e" % mn)
    print("  STAMPA V/e, il fotone e l'ottica, a e* e a e*/2 (il minimo e il massimo su k, e il rapporto dei minimi):")
    for ver in VERSI:
        for b in FISICHE:
            vv = {e: [ris[(e, d, nk, ver, b, EPS[0])] / e for d in DIREZ for nk in N_K] for e in E_LISTA[:2]}
            print("    %-11s %-7s: e* min %.4e max %.4e | e*/2 min %.4e max %.4e | min(e*)/min(e*/2) %.6f" % (
                ver, b, min(vv[E_LISTA[0]]), max(vv[E_LISTA[0]]), min(vv[E_LISTA[1]]), max(vv[E_LISTA[1]]), min(vv[E_LISTA[0]]) / min(vv[E_LISTA[1]])))
    print("  STAMPA la pendenza di ln V contro ln n a e*, n 1..4 (b3: V -> 0 con k -> 0?):")
    for d in DIREZ:
        for ver in VERSI:
            for b in FISICHE:
                y = np.log([ris[(estar, d, nk, ver, b, EPS[0])] for nk in (1, 2, 3, 4)])
                print("    d %s %-11s %-7s: %+.3f" % (d, ver, b, float(np.polyfit(np.log([1, 2, 3, 4]), y, 1)[0])))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
