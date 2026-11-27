# -*- coding: utf-8 -*-
r"""**[M2245-C] L'ANIMAZIONE DEL VENTO DEL VUOTO** *(DECISIONE DI LUCA, 2026-11-24 22:49; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-terdecies`; sola lettura degli stati di [M2210], nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/anima_vento.py

**Tre colonne** *(r1 gradino, r2 rampa, r3 V0)*, **quattro righe**, dagli stati ogni `250`, nella finestra di raggio `40` attorno al centro di partenza:
1. `rho_psi` per nodo, la scala sul massimo di `k 0`, col cerchio di raggio `25` attorno al baricentro di quello stato;
2. `rho_phi - rho_phi(k 0)`, la scala simmetrica attorno a zero fissata sul massimo assoluto di tutta la serie *(tre corse, tutti i `k`, nella finestra)*;
3. `J_phi` come frecce, una ogni `4` nodi *(`m1` e `m2` multipli di `4`)*, la lunghezza proporzionale e la scala fissata sul massimo di tutta la serie, il colore col segno di `J_y`. `J_y` e' quella di `vento_vuoto_v2`; `J_x = rho_phi arg(conj(Z(m1-1, m2)) Z(m1+1, m2))/2`, coi nodi a `+-1` esatti lungo `x`;
4. la fase di `phi` lungo `y` *(l'arg della somma sulla riga `m2`)*: **assoluta** a colori, quella di `k 0` in grigio, e **la fase acquistata da `k 0` tratteggiata**.

**Il titolo** porta `k`; **sotto**, `w(k)` *(`torneo_tenuta.misura` sugli stati)* e K per finestra *(letta da `legge_fondo_v3.txt`)*. **L'interpolazione:** lineare a `10` passi per intervallo per le righe 1-3, `10 fps`; **la riga 4 non si interpola** *(gli angoli attraversano `+-pi`)* e mostra lo stato precedente. **L'uscita:** `doc/referti_l2/anima_vento.mp4` *(meno di `20 MB`)*, i png in `E:/soliton_simulator/controllo/M2245/png/`. **Il caso noto:** a `k 0` le righe 1-4 sono uguali al bit nelle tre colonne.
"""
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import vento_vuoto_v2 as VV2  # noqa: E402

VV = VV2.VV
V3, F1, PF = VV.V3, VV.F1, VV.PF
TIPI = VV.TIPI
KS = VV.KS
PASSI, FPS, FINESTRA, OGNI_FRECCIA = 10, 10, 40.0, 4
D_PNG = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M2245", "png")
USCITA = os.path.join(_QUI, "anima_vento.mp4")
REF_K = os.path.join(_QUI, "legge_fondo_v3.txt")
NOMI = {"gradino": "r1 gradino", "rampa": "r2 rampa", "v0": "r3 V0"}


def k_dal_referto():
    """### `{tipo: [(k0, k1, K)]}` dalle righe «K CIMA PESATA» di `legge_fondo_v3.txt`."""
    out = {"gradino": [], "rampa": []}
    for r in open(REF_K, encoding="utf-8").read().splitlines():
        m = re.match(r"\s+(gradino|rampa)\s+\[\s*(\d+),\s*(\d+)\]:.*K CIMA PESATA ([+-][0-9.]+)", r)
        if m:
            out[m.group(1)].append((int(m.group(2)), int(m.group(3)), float(m.group(4))))
    assert out["gradino"] and out["rampa"], "K per finestra: non trovate in legge_fondo_v3.txt"
    return out


def main():
    import _presidio
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import animation
    V3.avvia()
    for m in ("vento_vuoto.py", "vento_vuoto_v2.py", "legge_fondo_v3.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    nodo, n, L, m1, m2, dxy, su, giu, info = VV.geometria()
    dx_p = ((m1 + 1) % L) * L + m2
    sx_m = ((m1 - 1) % L) * L + m2
    KW = k_dal_referto()
    vis = np.hypot(dxy[:, 0], dxy[:, 1]) <= FINESTRA
    fr = vis & (m1 % OGNI_FRECCIA == 0) & (m2 % OGNI_FRECCIA == 0)
    D = {t: {} for t in TIPI}
    W = {t: [] for t in TIPI}
    for t in TIPI:
        _p0, phi0 = VV.leggi_stato(os.path.join(V3.BASE, TIPI[t], "stato_000000.npz"))
        for k in KS:
            f = os.path.join(V3.BASE, TIPI[t], "stato_%06d.npz" % k)
            ps, ph = VV.leggi_stato(f)
            b, rpsi = VV.bari(ps, nodo, n, dxy)
            rho, Zn = VV.per_nodo(ph, phi0, nodo, n)
            Jy = rho * VV.dtheta_dy(Zn, su, giu)
            Jx = rho * np.angle(np.conj(Zn[sx_m]) * Zn[dx_p]) / 2.0
            Za = np.bincount(nodo, weights=ph.real, minlength=n) + 1j * np.bincount(nodo, weights=ph.imag, minlength=n)
            ab = np.array([np.angle(Za[m2 == r_].sum()) for r_ in range(L)])
            ac = np.array([np.angle(Zn[m2 == r_].sum()) for r_ in range(L)])
            D[t][k] = dict(rpsi=rpsi, rphi=rho, Jx=Jx, Jy=Jy, b=b, ab=ab, ac=ac)
            W[t].append(F1.TT.misura(f, nodo, n, L)[0])
        for k in KS:
            D[t][k]["drphi"] = D[t][k]["rphi"] - D[t][0]["rphi"]
    uguali = all(np.array_equal(D[t][0][q], D["gradino"][0][q]) for t in TIPI for q in ("rpsi", "drphi", "Jx", "Jy", "ab", "ac"))
    print("### il caso noto: il fotogramma k 0 uguale AL BIT nelle tre colonne (rho_psi, rho_phi - rho_phi(0), J_x, J_y, le due fasi): %s" % ("PASSA" if uguali else "### FALLISCE"))
    x, y = dxy[vis, 0], dxy[vis, 1]
    vmax1 = float(max(D[t][0]["rpsi"][vis].max() for t in TIPI))
    vmax2 = float(max(np.abs(D[t][k]["drphi"][vis]).max() for t in TIPI for k in KS))
    jmax = float(max(np.hypot(D[t][k]["Jx"][fr], D[t][k]["Jy"][fr]).max() for t in TIPI for k in KS))
    print("### le scale: rho_psi %.4e (k 0); |rho_phi - rho_phi(0)| %.4e; |J| %.4e (tutta la serie, nella finestra)" % (vmax1, vmax2, jmax))
    ym = np.arange(L) * math.sqrt(3.0) / 2.0 - info["y_c"]
    os.makedirs(D_PNG, exist_ok=True)
    fig = plt.figure(figsize=(15, 16), dpi=72)
    ax = [[fig.add_axes([0.03 + 0.325 * c, 0.76 - 0.19 * r, 0.30, 0.17]) for c in range(3)] for r in range(4)]
    axw = fig.add_axes([0.06, 0.03, 0.88, 0.13])
    theta = np.linspace(0, 2 * math.pi, 200)

    def interp(t, k_i, k_j, f, q):
        a = D[t][k_i][q]
        return a if f == 0.0 else (1 - f) * a + f * D[t][k_j][q]

    def disegna(tt):
        i = min(int(tt), len(KS) - 1)
        f = tt - i if i < len(KS) - 1 else 0.0
        ki, kj = KS[i], KS[min(i + 1, len(KS) - 1)]
        kk = ki + f * (kj - ki)
        for riga in ax:
            for a in riga:
                a.clear()
        axw.clear()
        for c, t in enumerate(TIPI):
            r1 = interp(t, ki, kj, f, "rpsi")
            b = interp(t, ki, kj, f, "b")
            a = ax[0][c]
            a.scatter(x, y, c=r1[vis], s=5, cmap="viridis", vmin=0.0, vmax=vmax1, marker="h", linewidths=0)
            a.plot(b[0] + 25 * np.cos(theta), b[1] + 25 * np.sin(theta), "w--", lw=0.8)
            a.set_title("%s   k %d" % (NOMI[t], int(round(kk))), fontsize=11)
            a = ax[1][c]
            a.scatter(x, y, c=interp(t, ki, kj, f, "drphi")[vis], s=5, cmap="RdBu_r", vmin=-vmax2, vmax=vmax2, marker="h", linewidths=0)
            a.set_title("rho_phi - rho_phi(k 0)", fontsize=9)
            a = ax[2][c]
            jx, jy = interp(t, ki, kj, f, "Jx")[fr], interp(t, ki, kj, f, "Jy")[fr]
            a.quiver(dxy[fr, 0], dxy[fr, 1], jx, jy, np.sign(jy), cmap="coolwarm", clim=(-1, 1), angles="xy", scale_units="xy", scale=jmax / 4.0, width=0.004)
            a.set_xlim(-FINESTRA, FINESTRA)
            a.set_ylim(-FINESTRA, FINESTRA)
            a.set_title("J_phi (scala fissa; rosso J_y > 0, blu < 0)", fontsize=9)
            for a in (ax[0][c], ax[1][c], ax[2][c]):
                a.set_aspect("equal")
                a.set_xticks([])
                a.set_yticks([])
            a = ax[3][c]
            a.plot(ym, D[t][0]["ab"], "-", color="0.7", lw=1.0, label="assoluta, k 0")
            a.plot(ym, D[t][ki]["ab"], "-", color="tab:blue", lw=1.0, label="assoluta, k %d" % ki)
            a.plot(ym, D[t][ki]["ac"], "--", color="tab:red", lw=1.2, label="acquistata da k 0")
            a.set_ylim(-math.pi - 0.2, math.pi + 0.2)
            a.set_xlabel("y - y_c", fontsize=8)
            a.set_title("arg phi lungo y (la somma su x)", fontsize=9)
            a.legend(fontsize=7, loc="lower left")
        for t, col in zip(TIPI, ("tab:blue", "tab:orange", "tab:green")):
            axw.plot(KS, W[t], "-o", color=col, ms=3, label="w, " + NOMI[t])
            axw.plot([kk], [np.interp(kk, KS, W[t])], "o", color=col, ms=8)
        txt = "   ".join("%s: %s" % (NOMI[t], ", ".join("[%d,%d] %.4f" % w for w in KW[t])) for t in ("gradino", "rampa"))
        axw.set_title("K CIMA pesata per finestra (legge_fondo_v3.txt)   " + txt, fontsize=9)
        axw.set_xlabel("k (tick)")
        axw.set_ylabel("w")
        axw.legend(loc="upper left", fontsize=8)
        axw.set_xlim(-50, 2050)
    for i, k in enumerate(KS):
        disegna(float(i))
        fig.savefig(os.path.join(D_PNG, "vento_k%04d.png" % k))
    print("### %d png in %s" % (len(KS), D_PNG))
    tempi = [i + s / PASSI for i in range(len(KS) - 1) for s in range(PASSI)] + [float(len(KS) - 1)]
    an = animation.FuncAnimation(fig, lambda tt: disegna(tt), frames=tempi, interval=1000 / FPS)
    an.save(USCITA, writer=animation.FFMpegWriter(fps=FPS, bitrate=1800))
    mb = os.path.getsize(USCITA) / 1e6
    print("### %d fotogrammi a %d fps: %s (%.2f MB; il tetto 20 MB: %s)" % (len(tempi), FPS, USCITA, mb, "PASSA" if mb < 20.0 else "### FALLISCE"))
    print("### w(k): " + "; ".join("%s %s" % (NOMI[t], " ".join("%.3f" % w for w in W[t])) for t in TIPI))
    return 0 if (uguali and mb < 20.0) else 1


if __name__ == "__main__":
    sys.exit(main())
