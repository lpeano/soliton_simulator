# -*- coding: utf-8 -*-
r"""**[M0951] IL VIDEO DELLA COPPIA d1'** *(DECISIONE DI LUCA, 2026-11-27 `09:51`; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-vicies`, il seguito [M0951], scritta PRIMA; sola lettura dei `25` stati di `M2034/coppia/d1`, nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/anima_coppia.py > doc/referti_l2/anima_coppia.txt

**Due pannelli:** a sinistra `rho_psi` per nodo *(la scala fissa, da `0` al massimo su tutti i quadri nel riquadro)*, a destra `chi` *(la scala fissa, dal minimo al massimo su tutti i quadri nel riquadro, con `12` curve di livello uguali in tutti i quadri)*. **In alto:** `k`, `d(k)` e `omega` dei due corpi *(la media della serie per tick su `[k-250, k)`; a `k 0`, `[0, 250)`)*. **Il riquadro** e' di lato `120`, centrato sul baricentro della coppia *(la media pesata con le masse dei due baricentri della `serie.json` al tick `k`)*. **25 quadri a `4 fps`, `1280x640`, `libx264` `yuv420p`**; se supera `5 MB`, si rifa' a `960x480`. **I due controlli PRIMA del video:** `d(3250)` entro il `10%` di `6.795`; a `k 0` il baricentro di `rho_psi` di ciascuna meta' coincide entro `0.5` con quello della serie.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_lettura_v4 as L4  # noqa: E402

L2, PF, VV = L4.L2, L4.PF, L4.VV
D1 = os.path.join(L4.BASE, "d1")
KS = L4.KS
MEZZO, FPS, LIVELLI, D_MIN, K_MIN = 60.0, 4, 12, 6.795, 3250
USCITA = os.path.join(_QUI, "anima_coppia.mp4")
TETTO_MB = 5.0


def main():
    import _presidio
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import animation
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "due_corpi_lettura_v4.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0951] IL VIDEO DELLA COPPIA d1' (%s, %d stati)" % (D1, len(KS)))
    print("=" * 130)
    with VV.F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        Z["metti"]()
    f = os.path.join(D1, "serie.json")
    PF.controlla(f)
    S = json.load(open(f, encoding="utf-8"))
    sr = np.array(S["serie"])
    om = [np.array(o) for o in S["omega"]]
    b = S["meta"]["centro_coppia"]
    dxy = np.asarray(TO.scarti(m1, m2, b[0], b[1], L))[:, :2]
    Q = {}
    for k in KS:
        X = L2.leggi(os.path.join(D1, "stato_%06d.npz" % k))
        r = sr[sr[:, 0] == k][0]
        ma, mb = r[3], r[6]
        cb = np.array([(ma * r[1] + mb * r[4]) / (ma + mb), (ma * r[2] + mb * r[5]) / (ma + mb)])
        a0, a1 = (max(k - 250, 0), max(k, 250))
        Q[k] = dict(rho=np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n), chi=np.asarray(X["chi"], float), cb=cb, d=float(np.hypot(r[4] - r[1], r[5] - r[2])), om=(float(om[0][a0:a1].mean()), float(om[1][a0:a1].mean())), corpi=(r[1:3], r[4:6]))
        Q[k]["vis"] = (np.abs(dxy[:, 0] - cb[0]) <= MEZZO) & (np.abs(dxy[:, 1] - cb[1]) <= MEZZO)
    # ### i due controlli, PRIMA del video
    dk = Q[K_MIN]["d"]
    ok1 = abs(dk / D_MIN - 1.0) < 0.10
    print("  DEVE: (il mandato) d a k %d = %.6f, entro il 10%% di %.3f (%.2f%%)   %s" % (K_MIN, dk, D_MIN, 100 * abs(dk / D_MIN - 1.0), "PASSA" if ok1 else "### FALLISCE"))
    r0 = Q[0]["rho"]
    scarti = []
    for j, mm in enumerate((dxy[:, 1] < 0.0, dxy[:, 1] >= 0.0)):
        w = r0 * mm
        c = (dxy * w[:, None]).sum(axis=0) / w.sum()
        scarti.append(float(np.hypot(*(c - Q[0]["corpi"][j]))))
        print("  il corpo %d a k 0: il baricentro di rho_psi (%+.4f, %+.4f); la serie (%+.4f, %+.4f); lo scarto %.4f" % (j + 1, c[0], c[1], Q[0]["corpi"][j][0], Q[0]["corpi"][j][1], scarti[-1]))
    ok2 = max(scarti) < 0.5
    print("  DEVE: (il riferimento) lo scarto massimo %.4f < 0.5   %s" % (max(scarti), "PASSA" if ok2 else "### FALLISCE"))
    if not (ok1 and ok2):
        print("### UN CONTROLLO FALLISCE: IL VIDEO NON SI FA")
        print("=" * 130)
        return 1
    rmax = float(max(Q[k]["rho"][Q[k]["vis"]].max() for k in KS))
    cmin = float(min(Q[k]["chi"][Q[k]["vis"]].min() for k in KS))
    cmax = float(max(Q[k]["chi"][Q[k]["vis"]].max() for k in KS))
    liv = np.linspace(cmin, cmax, LIVELLI)
    print("  le scale fisse: rho_psi [0, %.4e]; chi [%+.4f, %+.4f], %d livelli" % (rmax, cmin, cmax, LIVELLI))
    for k in KS:
        print("  k %4d: d %8.4f; omega %.6f %.6f; il baricentro della coppia (%+.3f, %+.3f); chi min nel riquadro %+.3f" % (k, Q[k]["d"], Q[k]["om"][0], Q[k]["om"][1], Q[k]["cb"][0], Q[k]["cb"][1], float(Q[k]["chi"][Q[k]["vis"]].min())))

    def fai(dpi):
        fig = plt.figure(figsize=(16, 8), dpi=dpi)
        ax = [fig.add_axes([0.03, 0.06, 0.44, 0.80]), fig.add_axes([0.53, 0.06, 0.44, 0.80])]

        def disegna(i):
            k = KS[i]
            q = Q[k]
            v = q["vis"]
            x, y = dxy[v, 0] - q["cb"][0], dxy[v, 1] - q["cb"][1]
            for a in ax:
                a.clear()
            ax[0].scatter(x, y, c=q["rho"][v], s=4, cmap="viridis", vmin=0.0, vmax=rmax, marker="h", linewidths=0)
            ax[0].set_title("rho_psi (la materia)", fontsize=12)
            ax[1].scatter(x, y, c=q["chi"][v], s=4, cmap="magma", vmin=cmin, vmax=cmax, marker="h", linewidths=0)
            ax[1].tricontour(x, y, q["chi"][v], levels=liv, colors="w", linewidths=0.6)
            ax[1].set_title("chi (il pozzo)", fontsize=12)
            for a in ax:
                a.set_xlim(-MEZZO, MEZZO)
                a.set_ylim(-MEZZO, MEZZO)
                a.set_aspect("equal")
                a.set_xticks([])
                a.set_yticks([])
            fig.suptitle("coppia d1'   k %d   d %.3f   omega %.5f / %.5f" % (k, q["d"], q["om"][0], q["om"][1]), fontsize=15)
        an = animation.FuncAnimation(fig, disegna, frames=range(len(KS)), interval=1000 / FPS)
        an.save(USCITA, writer=animation.FFMpegWriter(fps=FPS, codec="libx264", extra_args=["-pix_fmt", "yuv420p"]))
        plt.close(fig)
        return os.path.getsize(USCITA) / 1e6
    mb = fai(80)
    print("  il video a 1280x640: %.3f MB" % mb)
    if mb >= TETTO_MB:
        mb = fai(60)
        print("  oltre %.0f MB: rifatto a 960x480: %.3f MB" % (TETTO_MB, mb))
    ok3 = mb < TETTO_MB
    print("### %d quadri a %d fps: %s (%.3f MB; il tetto %.0f MB: %s)" % (len(KS), FPS, USCITA, mb, TETTO_MB, "PASSA" if ok3 else "### FALLISCE"))
    print("=" * 130)
    return 0 if ok3 else 1


if __name__ == "__main__":
    sys.exit(main())
