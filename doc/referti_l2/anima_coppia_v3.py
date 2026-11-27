# -*- coding: utf-8 -*-
r"""**[M1016] PEZZO 5: IL VIDEO v3 DELLA COPPIA, d1' E d1'', CON LE TRE SCALE** *(DECISIONE DI LUCA, 2026-11-27 `10:16`, S3; la carta `doc/CARTA_fondo_giusto.md`, il seguito [M1016], «PEZZI 4 E 5», scritta PRIMA della chiusura di d1'')*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/anima_coppia_v3.py > doc/referti_l2/anima_coppia_v3.txt

**`73` quadri** *(`k 0..18000` ogni `250`; `M2034/coppia/d1` fino a `6000`, `d1L` dopo)* a **`6 fps`**. **Tre pannelli:** `rho_psi` a scala FISSA *(`0` .. il massimo su tutti i quadri nel riquadro)*, `rho_psi` a scala PER QUADRO *(`0` .. il massimo dello stato)*, `chi` a scala fissa con `12` curve di livello. `tripcolor` `gouraud` sul riquadro di lato `120` centrato sul baricentro totale di `rho_psi` dello stato *(A0: `cb`)*; un `+` su ogni picco di A0. **In sovrimpressione:** `k`, `d_p` se DUE *(altrimenti il verdetto)*, la norma relativa, `max rho`, `R`. **`1440x480`**, `libx264` `yuv420p`, sotto `5 MB` *(altrimenti `1080x360`)*; i png a `k 0, 3250, 6000, 12000, 18000` in `E:/soliton_simulator/controllo/M0951/v3/`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import coppia_a0 as A0  # noqa: E402
import due_corpi_lettura_v6 as L6  # noqa: E402

L2, PF = A0.L2, A0.PF
MEZZO, FPS, LIVELLI = 60.0, 6, 12
USCITA = os.path.join(_QUI, "anima_coppia_v3.mp4")
D_PNG = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0951", "v3")
PNG_K = (0, 3250, 6000, 12000, 18000)
TETTO_MB = 5.0


def main():
    import json
    import _presidio
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.tri as mtri
    from matplotlib import animation
    _presidio.avvia(os.path.join(_QUI, "due_corpi_lettura_v6.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1016] PEZZO 5: IL VIDEO v3 (%d quadri, %d fps, tre pannelli)" % (len(L6.KS), FPS))
    print("=" * 130)
    G = A0.geometria()
    f = os.path.join(A0.D1, "serie.json")
    PF.controlla(f)
    centro = json.load(open(f, encoding="utf-8"))["meta"]["centro_coppia"]
    dxy = np.asarray(G["TO"].scarti(G["m1"], G["m2"], centro[0], centro[1], G["L"]))[:, :2]
    Q = {}
    for k in L6.KS:
        fz = os.path.join(L6.cartella(k), "stato_%06d.npz" % k)
        r = A0.a0(G, fz, centro)
        X = L2.leggi(fz)
        r["rho"] = np.bincount(G["nodo"], weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=G["n"])
        r["chi_c"] = np.asarray(X["chi"], float)
        r["vis"] = (np.abs(dxy[:, 0] - r["cb"][0]) <= MEZZO) & (np.abs(dxy[:, 1] - r["cb"][1]) <= MEZZO)
        Q[k] = r
    N0 = Q[0]["N"]
    rmax = float(max(Q[k]["rho"][Q[k]["vis"]].max() for k in L6.KS))
    cmin = float(min(Q[k]["chi_c"][Q[k]["vis"]].min() for k in L6.KS))
    cmax = float(max(Q[k]["chi_c"][Q[k]["vis"]].max() for k in L6.KS))
    liv = np.linspace(cmin, cmax, LIVELLI)
    print("  le scale fisse: rho_psi [0, %.4e]; chi [%+.4f, %+.4f]" % (rmax, cmin, cmax))

    def fai(dpi):
        fig = plt.figure(figsize=(18, 6), dpi=dpi)
        ax = [fig.add_axes([0.01 + 0.33 * i, 0.04, 0.31, 0.80]) for i in range(3)]

        def disegna(i):
            k = L6.KS[i]
            q = Q[k]
            v = q["vis"]
            x, y = dxy[v, 0] - q["cb"][0], dxy[v, 1] - q["cb"][1]
            tri = mtri.Triangulation(x, y)
            for a in ax:
                a.clear()
            ax[0].tripcolor(tri, q["rho"][v], shading="gouraud", cmap="viridis", vmin=0.0, vmax=rmax)
            ax[0].set_title("rho_psi, scala FISSA", fontsize=11)
            ax[1].tripcolor(tri, q["rho"][v], shading="gouraud", cmap="viridis", vmin=0.0, vmax=float(q["rho"][v].max()))
            ax[1].set_title("rho_psi, scala PER QUADRO", fontsize=11)
            ax[2].tripcolor(tri, q["chi_c"][v], shading="gouraud", cmap="magma", vmin=cmin, vmax=cmax)
            ax[2].tricontour(tri, q["chi_c"][v], levels=liv, colors="w", linewidths=0.8)
            ax[2].set_title("chi (il pozzo), scala fissa", fontsize=11)
            for a in ax:
                for n_ in q["loc"]:
                    a.plot([dxy[n_, 0] - q["cb"][0]], [dxy[n_, 1] - q["cb"][1]], "+", color="r", ms=11, mew=1.5)
                a.set_xlim(-MEZZO, MEZZO)
                a.set_ylim(-MEZZO, MEZZO)
                a.set_aspect("equal")
                a.set_xticks([])
                a.set_yticks([])
            dtxt = ("d_p %.2f" % q["dloc"]) if q["nloc"] == 2 else ("un corpo" if q["nloc"] == 1 else "contatto (%d picchi)" % q["nloc"])
            fig.suptitle("coppia d1'/d1''   k %d   %s   norma %+.1e   max rho %.3e   R %.2f" % (k, dtxt, q["N"] / N0 - 1.0, q["rmax"], q["R"]), fontsize=14)
        os.makedirs(D_PNG, exist_ok=True)
        for i, k in enumerate(L6.KS):
            if k in PNG_K:
                disegna(i)
                fig.savefig(os.path.join(D_PNG, "coppia_v3_k%05d.png" % k))
        an = animation.FuncAnimation(fig, disegna, frames=range(len(L6.KS)), interval=1000 / FPS)
        an.save(USCITA, writer=animation.FFMpegWriter(fps=FPS, codec="libx264", extra_args=["-pix_fmt", "yuv420p"]))
        plt.close(fig)
        return os.path.getsize(USCITA) / 1e6
    mb = fai(80)
    print("  il video a 1440x480: %.3f MB" % mb)
    if mb >= TETTO_MB:
        mb = fai(60)
        print("  oltre %.0f MB: rifatto a 1080x360: %.3f MB" % (TETTO_MB, mb))
    ok = mb < TETTO_MB
    print("### %d quadri a %d fps: %s (%.3f MB; il tetto %.0f MB: %s); i png in %s" % (len(L6.KS), FPS, USCITA, mb, TETTO_MB, "PASSA" if ok else "### FALLISCE", D_PNG))
    print("=" * 130)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
