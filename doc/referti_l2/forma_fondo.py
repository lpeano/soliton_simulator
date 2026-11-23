# -*- coding: utf-8 -*-
r"""**[M2221] LA FORMA DELL'OGGETTO AL FONDO A K** *(Luca, 2026-11-23 22:21; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-quinquies`; SOLA LETTURA degli stati salvati)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/forma_fondo.py > doc/referti_l2/forma_fondo.txt

**Tre stati a `k 3000`:** (a) lambda `-1` al fondo a K per proiezione; (b) L0 con la stessa semina; (c) il mattone alla cima, L-1, di [M1631]. **Per ciascuno:** il baricentro di `rho`; sugli anelli `[4, 8)`, `[8, 12)`, `[12, 16)` `|S_m|/somma rho` e `-arg(S_m)/m` per `m = 3, 6`, `S_m = somma rho e^{-i m theta}`. **Il caso noto:** `rho = 1 + cos(6 theta)` sull'anello. **Il fondo del favo:** `rho = 1` sull'anello. **Le immagini:** `forma_fondo_ab_lineare.png`, `forma_fondo_ab_log.png`, `forma_fondo_c.png`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
STATI = (("a", "lambda -1, proiezione al fondo a K", os.path.join(CTRL, "M1658", "tenuta", "L-1_proiezione_K", "stato_003000.npz")),
         ("b", "L0, proiezione al fondo a K (il controllo)", os.path.join(CTRL, "M1658", "tenuta", "L0_proiezione_K", "stato_003000.npz")),
         ("c", "il mattone alla cima, L-1 ([M1631] tenuta_v2/L-1_cima)", os.path.join(CTRL, "M1631", "tenuta_v2", "L-1_cima", "stato_003000.npz")))
ANELLI = ((4.0, 8.0), (8.0, 12.0), (12.0, 16.0))
EMME = (3, 6)
FINESTRA, DECADI = 30.0, 4
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def momenti(rho, th, sel, m):
    S = complex(np.sum(rho[sel] * np.exp(-1j * m * th[sel])))
    return abs(S) / float(np.sum(rho[sel])), math.degrees(-np.angle(S) / m)


def geometria(rho, m1, m2, L):
    from solitone import toro as TO
    c = TO.centro(rho, m1, m2, L)[:2]
    d = np.asarray(TO.scarti(m1, m2, c[0], c[1], L))[:, :2]
    b = (d * rho[:, None]).sum(axis=0) / rho.sum()
    d = d - b
    return d, np.hypot(d[:, 0], d[:, 1]), np.arctan2(d[:, 1], d[:, 0])


def main():
    import _presidio
    import gravita_due_corpi_misure as GM
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _presidio.avvia(__file__)
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        Z["metti"]()
    print("=" * 130)
    print("[M2221] LA FORMA DELL'OGGETTO AL FONDO A K (la carta sez. 2-quinquies): gli anelli %s attorno al baricentro di rho; m = 3, 6" % (ANELLI,))
    print("=" * 130)
    G = {}
    for sig, nome, f in STATI:
        X, meta = GM.leggi(f)
        rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        d, r, th = geometria(rho, m1, m2, L)
        G[sig] = (nome, f, rho, d, r, th, int(meta["k"]))
    # ### il caso noto e il fondo del favo (sulla geometria di (a))
    _n, _f, rho_a, d, r, th, _k = G["a"]
    fondo = {}
    print("  IL FONDO DEL FAVO (rho = 1 sull'anello) e IL CASO NOTO (rho = 1 + cos(6 theta)), sulla geometria di (a):")
    for lo, hi in ANELLI:
        sel = (r >= lo) & (r < hi)
        uno = np.ones(n)
        f3, o3 = momenti(uno, th, sel, 3)
        f6, o6 = momenti(uno, th, sel, 6)
        fondo[(lo, hi)] = (f3, f6)
        sint = 1.0 + np.cos(6.0 * th)
        s6, so6 = momenti(sint, th, sel, 6)
        print("    [%2g, %2g): %d nodi; il fondo |S3|/somma %.5f, |S6|/somma %.5f; il caso noto |S6|/somma %.5f, l'orientamento %+.3f gradi" % (lo, hi, int(sel.sum()), f3, f6, s6, so6))
        esito("il caso noto [%g, %g): |S6|/somma = 0.5 entro il fondo + 0.01, l'orientamento 0 entro 1 grado" % (lo, hi), abs(s6 - 0.5) <= f6 + 0.01 and abs(so6) <= 1.0, "%.5f, %+.3f" % (s6, so6))
    print("-" * 130)
    print("  %-50s %-10s %-24s %-24s %s" % ("lo stato", "l'anello", "m = 3: |S|/somma, orient.", "m = 6: |S|/somma, orient.", "il fondo del favo (m 3, m 6)"))
    for sig, (nome, f, rho, d, r, th, k) in G.items():
        print("  (%s) %s: %s, k %d; il baricentro raffinato; la massa %.6f, il picco %.4e" % (sig, nome, os.path.basename(os.path.dirname(f)) + "/" + os.path.basename(f), k, float(rho.sum()), float(rho.max())))
        for lo, hi in ANELLI:
            sel = (r >= lo) & (r < hi)
            a3, o3 = momenti(rho, th, sel, 3)
            a6, o6 = momenti(rho, th, sel, 6)
            print("      [%2g, %2g)    %.5f, %+8.3f gradi     %.5f, %+8.3f gradi     %.5f, %.5f" % (lo, hi, a3, o3, a6, o6, fondo[(lo, hi)][0], fondo[(lo, hi)][1]))
    # ### le immagini
    def pannello(ax, sig, log):
        nome, f, rho, d, r, th, k = G[sig]
        vis = r <= FINESTRA
        if log:
            v = np.log10(np.maximum(rho[vis], 1e-300))
            vmax = float(np.log10(rho[vis].max()))
            sc = ax.scatter(d[vis, 0], d[vis, 1], c=v, s=7, cmap="viridis", vmin=vmax - DECADI, vmax=vmax, marker="h", linewidths=0)
        else:
            sc = ax.scatter(d[vis, 0], d[vis, 1], c=rho[vis], s=7, cmap="viridis", vmin=0.0, vmax=float(rho[vis].max()), marker="h", linewidths=0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("(%s) %s, k %d%s" % (sig, nome, k, ", log10 rho (%d decadi)" % DECADI if log else ", lineare (il suo massimo)"), fontsize=9)
        plt.colorbar(sc, ax=ax, fraction=0.046)
    uscite = []
    for nome_f, coppie in (("forma_fondo_ab_lineare.png", (("a", False), ("b", False))), ("forma_fondo_ab_log.png", (("a", True), ("b", True))), ("forma_fondo_c.png", (("c", False), ("c", True)))):
        fig, ax = plt.subplots(1, 2, figsize=(12, 5.6), dpi=80)
        for a_, (sig, log) in zip(ax, coppie):
            pannello(a_, sig, log)
        fp = os.path.join(_QUI, nome_f)
        fig.savefig(fp)
        plt.close(fig)
        uscite.append((nome_f, os.path.getsize(fp)))
    print("-" * 130)
    print("### le immagini: %s" % ", ".join("%s (%.0f kB)" % (x, s / 1e3) for x, s in uscite))
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0


if __name__ == "__main__":
    sys.exit(main())
