# -*- coding: utf-8 -*-
r"""**[M2155] L'ANIMAZIONE DELLA TENUTA AL FONDO A K** *(Luca, 2026-11-23 21:55; SOLA LETTURA degli stati salvati, nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/anima_tenuta.py

**Gli stati** `stato_000000 ... stato_003000` *(ogni `250`)* di `M1658/tenuta/L-1_proiezione_K` *(a sinistra)* e `L0_proiezione_K` *(il controllo, a destra)*. **Per ogni `k`:** `|psi|^2` per nodo, scatter sulle coordinate del favo *(`toro.scarti` dal centro dell'oggetto, una finestra di raggio `40`)*, **la stessa scala di colore fissata sul massimo di `k 0`**; il titolo con `k`, `omega` *(il tick `k` da `omega.npy`)* e `w(k)` **letta dal referto** `doc/referti_l2/tenuta_fondo.txt`; sotto `w(k)` delle due corse e il punto corrente. **Interpolazione lineare** fra i fotogrammi: `10` passi per intervallo, `130` fotogrammi, `10 fps`. **Uscita:** `doc/referti_l2/anima_tenuta_fondo.mp4` *(ffmpeg; se no la gif)*; i `13` png grezzi in `E:/soliton_simulator/controllo/M1658/tenuta/png/` *(non nel repo)*. **Il controllo:** `k 0` delle due corse uguale AL BIT *(la stessa semina)*.
"""
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "tenuta")
CORSE = ("L-1_proiezione_K", "L0_proiezione_K")
KS = list(range(0, 3001, 250))
PASSI, FPS, FINESTRA = 10, 10, 40.0
REFERTO = os.path.join(_QUI, "tenuta_fondo.txt")
USCITA = os.path.join(_QUI, "anima_tenuta_fondo.mp4")


def w_dal_referto():
    out, cur = {}, None
    for r in open(REFERTO, encoding="utf-8"):
        m = re.match(r"\s+(\S+_K): \{", r)
        if m:
            cur = m.group(1)
            out[cur] = {}
            continue
        m = re.match(r"\s+k\s+(\d+): w ([0-9.]+),", r)
        if m and cur:
            out[cur][int(m.group(1))] = float(m.group(2))
    return out


def main():
    import _presidio
    import gravita_due_corpi_misure as GM
    from solitone import toro as TO
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _presidio.avvia(__file__)
    W = w_dal_referto()
    assert all(len(W[c]) == len(KS) for c in CORSE), "w(k) dal referto: mancano dei k"
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        Z["metti"]()
    R, OM, centro = {}, {}, None
    for c in CORSE:
        R[c] = []
        om = np.load(os.path.join(DIR, c, "omega.npy"))
        OM[c] = om
        for k in KS:
            X, meta = GM.leggi(os.path.join(DIR, c, "stato_%06d.npz" % k))
            R[c].append(np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n))
            if centro is None:
                centro = meta["centro"]
    uguali = np.array_equal(R[CORSE[0]][0], R[CORSE[1]][0])
    print("### il controllo: k 0 delle due corse uguale AL BIT: %s" % ("PASSA" if uguali else "### FALLISCE"))
    d = np.asarray(TO.scarti(m1, m2, centro[0], centro[1], L))[:, :2]
    vis = np.hypot(d[:, 0], d[:, 1]) <= FINESTRA
    x, y = d[vis, 0], d[vis, 1]
    vmax = float(R[CORSE[0]][0][vis].max())
    d_png = os.path.join(DIR, "png")
    os.makedirs(d_png, exist_ok=True)
    fig = plt.figure(figsize=(12, 8), dpi=90)
    ax = [fig.add_axes([0.04, 0.32, 0.44, 0.62]), fig.add_axes([0.52, 0.32, 0.44, 0.62]), fig.add_axes([0.08, 0.06, 0.86, 0.2])]
    wk = {c: np.array([W[c][k] for k in KS]) for c in CORSE}

    def disegna(t):
        i = min(int(t), len(KS) - 1)
        f = t - i if i < len(KS) - 1 else 0.0
        kk = KS[i] + f * (KS[min(i + 1, len(KS) - 1)] - KS[i])
        for a in ax:
            a.clear()
        for p, c in enumerate(CORSE):
            r = R[c][i] if f == 0.0 else (1 - f) * R[c][i] + f * R[c][i + 1]
            ax[p].scatter(x, y, c=r[vis], s=6, cmap="viridis", vmin=0.0, vmax=vmax, marker="h", linewidths=0)
            ax[p].set_aspect("equal")
            ax[p].set_xticks([])
            ax[p].set_yticks([])
            wv = np.interp(kk, KS, wk[c])
            ko = int(round(kk))
            om = OM[c][ko - 1] if ko >= 1 else OM[c][0]
            ax[p].set_title("%s   k %d   omega %+.4f   w %.2f" % ("lambda = -1" if c.startswith("L-1") else "L0 (il controllo)", ko, om, wv), fontsize=11)
        for c, col in zip(CORSE, ("tab:blue", "tab:orange")):
            ax[2].plot(KS, wk[c], "-o", color=col, ms=3, label=("lambda = -1" if c.startswith("L-1") else "L0") + " (proiezione al fondo a K)")
            ax[2].plot([kk], [np.interp(kk, KS, wk[c])], "o", color=col, ms=9)
        ax[2].set_xlabel("k (tick)")
        ax[2].set_ylabel("w (dal referto)")
        ax[2].legend(loc="upper right", fontsize=9)
        ax[2].set_xlim(-50, 3050)
    for i, k in enumerate(KS):
        disegna(float(i))
        fig.savefig(os.path.join(d_png, "tenuta_k%04d.png" % k))
    print("### %d png in %s" % (len(KS), d_png))
    from matplotlib import animation
    tempi = [i + s / PASSI for i in range(len(KS)) for s in range(PASSI)]
    an = animation.FuncAnimation(fig, lambda t: disegna(t), frames=tempi, interval=1000 / FPS)
    try:
        an.save(USCITA, writer=animation.FFMpegWriter(fps=FPS, bitrate=1800))
        f_out = USCITA
    except Exception as e:  # ### ffmpeg assente: la gif
        print("### l'mp4 NON riesce (%s): la gif" % type(e).__name__)
        f_out = USCITA[:-4] + ".gif"
        an.save(f_out, writer=animation.PillowWriter(fps=FPS))
    print("### %d fotogrammi a %d fps: %s (%.2f MB)" % (len(tempi), FPS, f_out, os.path.getsize(f_out) / 1e6))
    return 0 if uguali else 1


if __name__ == "__main__":
    sys.exit(main())
