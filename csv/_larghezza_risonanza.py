# -*- coding: utf-8 -*-
r"""**LA LARGHEZZA DELLA RISONANZA** *(UNA DIAGNOSI, NON UNA CURA; il mandato di Luca delle `14:51` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_larghezza_risonanza.md`)*: ### **uno strumento di DIAGNOSI, mai nel nucleo.**
### **La corsa dallo stato fermo di `S1` a `s 0.15`; a ogni tick, dopo il tick, le componenti sulle piatte** *(`P0`, `Ppi`: gli autovettori del tick libero, per impulso)*
### **moltiplicate per `e^{-i delta_p s}`:** ### **`ph_p` sale di `delta_p` per unita' di tempo; lo scarto della coppia di `delta_P0 + delta_Ppi`.**

    python csv/_larghezza_risonanza.py --referto > doc/referti_l2/larghezza_risonanza.txt
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

CASO = "S1_s0.150"
P0 = (6, 7, 8, 9)
PPI = (0, 1, 2, 3)
DELTA_STESSA = (0.0, 0.025, -0.025, 0.05, -0.05, 0.1, -0.1, 0.2, -0.2, 0.4, -0.4, 0.8, -0.8)
DELTA_OPPOSTE = (0.2, 0.8)
DELTA_UNA = (0.2, 0.8)
T_FIS = 180.0
T_DA_FIS = 60.0
PASSO_FIS = 3.0
FATTORE_RUMORE = 1e3
SATURAZIONE = 1e-2
TASSO_DFB = 0.15108            # ### dfb5ab7e, s 0.15
TOLL_DFB = 1e-3
TOLL_NORMA = 1e-10
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


class Spostamento:
    """### **Le componenti piatte moltiplicate per `e^{-i delta_p s}`** *(per impulso: `fft2`, `Z(k)^H`, la fase, `Z(k)`, `ifft2`)*."""

    def __init__(self, Z, L, s, d_p0, d_ppi):
        self.Z, self.L = Z, L
        self.f = np.ones(12, dtype=complex)
        self.f[list(P0)] = np.exp(-1j * d_p0 * s)
        self.f[list(PPI)] = np.exp(-1j * d_ppi * s)

    def __call__(self, psi_h, potenza=1):
        L = self.L
        f = np.fft.fft2(psi_h.reshape(L, L, 12), axes=(0, 1))
        c = np.einsum("abji,abj->abi", self.Z.conj(), f) * (self.f ** potenza)
        g = np.fft.ifft2(np.einsum("abij,abj->abi", self.Z, c), axes=(0, 1))
        return g.reshape(psi_h.shape)


def corsa(contesto, d_p0, d_ppi, etichetta):
    import _modo_al_variare_di_s as MS
    z, phi0, psi0, mu, s, forma, Z, r1 = contesto
    L = MS.L
    sp = Spostamento(Z, L, s, d_p0, d_ppi)
    M0 = float(np.sum(np.abs(psi0) ** 2))
    ogni = int(round(PASSO_FIS / s))
    t_fine = int(round(T_FIS / s))
    t_da = int(round(T_DA_FIS / s))
    psi = psi0.copy()
    dn = 0.0
    nD = {}
    s0 = time.time()
    for t in range(1, t_fine + 1):
        psi = MS.tick(z, phi0, psi, forma)
        prima = float(np.sum(np.abs(psi) ** 2))
        psi = sp(psi)
        dn = max(dn, abs(float(np.sum(np.abs(psi) ** 2)) / prima - 1.0))
        if t % ogni == 0 and t >= t_da:
            rif = sp(psi0, t)
            nD[t] = float(np.linalg.norm(np.exp(1j * mu * s * t) * psi - rif)) / math.sqrt(M0)
    ts = sorted(nD)
    v = np.array([nD[t] for t in ts])
    fin = [i for i in range(len(ts)) if FATTORE_RUMORE * r1 < v[i] < SATURAZIONE]
    tasso = None
    nota = ""
    if len(fin) >= 3:
        a, b = fin[0], fin[-1]
        tt = np.array(ts[a:b + 1], dtype=float)
        pend = float(np.polyfit(tt, np.log(v[a:b + 1]), 1)[0])
        tasso = pend / s
        nota = "la finestra tempo %.0f .. %.0f (|D| %.1e .. %.1e)" % (ts[a] * s, ts[b] * s, v[a], v[b])
    else:
        nota = "la finestra ha %d campioni" % len(fin)
    print("  %-26s dP0 %+6.3f dPpi %+6.3f (lo scarto %+6.3f): il tasso %s; %s; |D| a tempo 60, 120, 180: %.1e %.1e %.1e; la norma %.1e; %.0f s"
          % (etichetta, d_p0, d_ppi, d_p0 + d_ppi, ("%+.5f" % tasso) if tasso is not None else "--", nota, nD[ts[0]], nD[ts[len(ts) // 2]], nD[ts[-1]], dn, time.time() - s0))
    sys.stdout.flush()
    return tasso, dn


def referto():
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    print("=" * 130)
    print("LA LARGHEZZA DELLA RISONANZA (Luca 14:51; UNA DIAGNOSI): le piatte spostate in frequenza a ogni tick; %s, %g unita' di tempo per corsa" % (CASO, T_FIS))
    print("=" * 130)
    print("  la configurazione: CASO %s P0 %s PPI %s DELTA_STESSA %s DELTA_OPPOSTE %s DELTA_UNA %s T_FIS %g T_DA_FIS %g PASSO_FIS %g FATTORE_RUMORE %g SATURAZIONE %g TASSO_DFB %g TOLL_DFB %g TOLL_NORMA %g"
          % (CASO, P0, PPI, DELTA_STESSA, DELTA_OPPOSTE, DELTA_UNA, T_FIS, T_DA_FIS, PASSO_FIS, FATTORE_RUMORE, SATURAZIONE, TASSO_DFB, TOLL_DFB, TOLL_NORMA))
    print("  IL SEGNO: e^{-i delta_p s} sulle componenti della piatta p alza ph_p = -arg(lambda) di delta_p s per tick; lo scarto ph_P0 + ph_Ppi - 2 ph_sol cambia di delta_P0 + delta_Ppi per unita' di tempo")
    print("  D(t) = e^{i mu s t} psi(t) - psi_ref(t), psi_ref = lo stato fermo con le sue componenti piatte ruotate dello stesso spostamento (a delta 0: lo stato fermo)")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (w1) nella stessa direzione il tasso cala con |delta| e si spegne; (w2) non cala fino a 0.8; (w3) cala per un segno e cresce per l'altro; (w4) altro;"
          " (k1) opposte ~0.151 e una piatta a delta = la stessa direzione a delta/2; (k2) no")
    _n, forma, s, N = MS.caso(CASO)
    psi0, mu, cj, ok = MS.carica(CASO)
    esito("DEVE PASSARE: %s, lo stato fermo = la ricerca (sha1), e fermo" % CASO, ok and cj["convergito"], "%.3e" % cj["residuo_finale"])
    with D.configura(forma, s, N):
        _rec, z, phi0, _p = MS.scena(forma, s, N)
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
        ctx = (z, phi0, psi0, mu, s, forma, Z, cj["residuo_finale"])
        print("-" * 130)
        print("### LA STESSA DIREZIONE (P0 e Ppi di delta: lo scarto 2 delta)")
        stessa = {}
        dnmax = 0.0
        for d in DELTA_STESSA:
            t, dn = corsa(ctx, d, d, "stessa delta %+.3f" % d)
            stessa[d] = t
            dnmax = max(dnmax, dn)
        print("-" * 130)
        print("### I CONTROLLI DEL MECCANISMO")
        opposte, una = {}, {}
        for d in DELTA_OPPOSTE:
            t, dn = corsa(ctx, d, -d, "opposte delta %.3f" % d)
            opposte[d] = t
            dnmax = max(dnmax, dn)
        for d in DELTA_UNA:
            t, dn = corsa(ctx, d, 0.0, "solo P0 delta %.3f" % d)
            una[d] = t
            dnmax = max(dnmax, dn)
    print("-" * 130)
    esito("DEVE PASSARE: lo spostamento conserva la norma entro %g (il massimo su tutte le corse)" % TOLL_NORMA, dnmax < TOLL_NORMA, "%.1e" % dnmax)
    t0 = stessa[0.0]
    esito("DEVE PASSARE: delta 0 ridà il tasso di dfb5ab7e (%.5f) entro %g relativo" % (TASSO_DFB, TOLL_DFB), t0 is not None and abs(t0 / TASSO_DFB - 1.0) < TOLL_DFB, "%s" % t0)
    print("### LA SINTESI (il tasso per unita' di tempo)")
    print("  la stessa direzione: %s" % "  ".join("%+.3f: %s" % (d, ("%.4f" % stessa[d]) if stessa[d] is not None else "--") for d in sorted(stessa)))
    print("  le opposte: %s; solo P0: %s; da confrontare con la stessa direzione a delta/2: %s"
          % ("  ".join("%.1f: %s" % (d, ("%.4f" % opposte[d]) if opposte[d] is not None else "--") for d in DELTA_OPPOSTE),
             "  ".join("%.1f: %s" % (d, ("%.4f" % una[d]) if una[d] is not None else "--") for d in DELTA_UNA),
             "  ".join("%.1f: %s" % (d / 2, ("%.4f" % stessa[d / 2]) if stessa.get(d / 2) is not None else "--") for d in DELTA_UNA)))
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
