# -*- coding: utf-8 -*-
r"""**[M1020] IL VIDEO DI C: IL CORPO FUSO CON LE NASCITE** *(DECISIONE DI LUCA, 2026-11-28 10:20; la carta `doc/CARTA_mitosi.md`, «IL VIDEO DI C»;
nessun tick: solo letture)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/anima_corpo_fuso_nascite.py > doc/referti_l2/anima_corpo_fuso_nascite.txt
    E:\python\py3132\python.exe doc/referti_l2/anima_corpo_fuso_nascite.py --fino 18000 --da-r3 > ...   (a ripresa chiusa: gli stati di M0026/C_R3 dopo 16250)

**I quadri:** gli stati di `M0026/C` ogni `250`, da `k 10000` a `16250` *(26 quadri)*; con `--da-r3` gli stati dopo `16250` da `M0026/C_R3`. **Tre
pannelli** attorno al centro periodico di `rho_psi` *(finestra `+-32`)*: `log10 rho_psi`, `chi`, e il RETICOLO *(gli archi con i due estremi entro
`r 30` dal centro)*, coi nodi nati in evidenza: ACCESI *(giallo, grandi)* nel quadro in cui nascono, poi un colore FISSO *(ciano)*; i nodi del toro grigi.
**Il tempo delle nascite:** ogni quadro dura `2 s` *(60 fotogrammi a 30 fps)*; le nascite del registro con `k` nell'intervallo `(k - 250, k]` si
accendono in ordine, al fotogramma `ceil(60 (k_b - k + 250) / 250)`. **Il reticolo** del pannello e' quello dello stato a `k` *(gli archi dei nati
dell'intervallo ci sono gia' dal primo fotogramma: una semplificazione, dichiarata)*. **In sovrimpressione:** `k`, le nascite cumulate al fotogramma,
`R`, `max rho_psi`, `E_persa` *(dello stato)*. `1280 x 720`, `30 fps`, un fermo di `3 s` sul primo e sull'ultimo quadro. **Il video NON va in git**
*(`*.mp4` e' in `.gitignore`)*; il PNG dell'ultimo quadro si'. **Il caso noto:** i nodi in evidenza nell'ultimo fotogramma = le nascite del log con
`k <=` l'ultimo `k`.
"""
import argparse
import json
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import corpo_fuso_mitosi as CFM  # noqa: E402  (### anche il percorso di csv/, per _presidio)

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
D_C, D_R3 = os.path.join(CTRL, "M0026", "C"), os.path.join(CTRL, "M0026", "C_R3")
LOG = os.path.join(CTRL, "M1446", "log", "M0026_C.txt")
LOG_R3 = os.path.join(CTRL, "M1446", "log", "M0026_C_R3.txt")
USCITA = os.path.join(_QUI, "anima_corpo_fuso_nascite.mp4")
PNG = os.path.join(_QUI, "anima_corpo_fuso_nascite_ultimo.png")
K_DA, OGNI, FPS, PER_QUADRO, FERMO_S = 10000, 250, 30, 60, 3
MEZZO, R_RETICOLO = 32.0, 30.0
TITOLO = "[M0026] C \u2014 la coppia con le nascite accese; non \u00e8 un'immagine, \u00e8 lo stato della corsa"


def nascite_log(f):
    out = []
    if os.path.exists(f):
        for r in open(f, encoding="utf-8", errors="replace"):
            m = re.match(r"^    \[nascita (\d+)\] k (\d+), l'arco \d+ \([^)]*\): n (\d+) ", r)
            if m:
                out.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return out


def main(argv):
    import _presidio
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.tri as mtri
    from matplotlib import animation
    from matplotlib.collections import LineCollection
    from solitone import toro as TO
    a = argparse.ArgumentParser()
    a.add_argument("--fino", type=int, default=16250)
    a.add_argument("--da-r3", action="store_true")
    x = a.parse_args(argv)
    _presidio.avvia(__file__)
    print("=" * 134)
    print("[M1020] IL VIDEO DI C: da k %d a %d ogni %d; %d fps, %d fotogrammi a quadro, il fermo %d s" % (K_DA, x.fino, OGNI, FPS, PER_QUADRO, FERMO_S))
    print("=" * 134)
    with CFM.V6.GD.TC.scena() as Z:
        nodo0 = np.asarray(Z["mot"].inc.nodo)
        n0, L = int(Z["mot"].inc.n), int(Z["L"])
        m1s, m2s = np.asarray(Z["m1"], dtype=float), np.asarray(Z["m2"], dtype=float)
        Z["metti"]()
    # ### il registro delle nascite: quello di C fino a 16250 (e fino alla 651 dal log), poi quello della ripresa
    B = json.load(open(os.path.join(D_C, "nascite.json"), encoding="utf-8"))
    if x.da_r3:
        B = json.load(open(os.path.join(D_R3, "nascite.json"), encoding="utf-8"))
    kb = np.array([b["k"] for b in B])
    nb = np.array([b["nodi"]["n"] for b in B])
    KS = list(range(K_DA, x.fino + 1, OGNI))

    def stato(k):
        d = D_R3 if (x.da_r3 and k > 16250) else D_C
        f = os.path.join(d, "stato_%06d.npz" % k)
        with np.load(f) as z:
            psi, chi = z["psi_h"], z["chi"]
            meta = json.loads(str(z["meta"]))
            if "ii" in z.files:
                ii, jj, m1, m2 = z["ii"], z["jj"], z["m1"], z["m2"]
            else:
                ii, jj, m1, m2 = nodo0[0::2], nodo0[1::2], m1s, m2s
        nodo = np.empty(2 * len(ii), dtype=np.int64)
        nodo[0::2], nodo[1::2] = ii, jj
        n = len(m1)
        rho = np.bincount(nodo, weights=np.sum(np.abs(psi) ** 2, axis=1), minlength=n)
        c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
        d = np.asarray(TO.scarti(m1, m2, c1, c2, L))[:, :2]
        r = np.hypot(d[:, 0], d[:, 1])
        R = float(np.sqrt(np.sum(rho * r ** 2) / np.sum(rho)))
        return {"k": k, "rho": rho, "chi": np.asarray(chi, float), "d": d, "r": r, "ii": ii, "jj": jj, "n": n, "R": R, "E_persa": float(meta["E_persa"]),
                "nascite": int(meta["nascite"])}
    Q = [stato(k) for k in KS]
    vis = [(np.abs(q["d"][:, 0]) <= MEZZO) & (np.abs(q["d"][:, 1]) <= MEZZO) for q in Q]
    lmin = math.log10(max(min(float(q["rho"][v][q["rho"][v] > 0].min()) for q, v in zip(Q, vis)), 1e-12))
    lmax = math.log10(max(float(q["rho"][v].max()) for q, v in zip(Q, vis)))
    cmin = min(float(q["chi"][v].min()) for q, v in zip(Q, vis))
    cmax = max(float(q["chi"][v].max()) for q, v in zip(Q, vis))
    print("  %d quadri; le scale fisse: log10 rho_psi [%.3f, %.3f]; chi [%+.3f, %+.3f]" % (len(KS), lmin, lmax, cmin, cmax))
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    ax = [fig.add_axes([0.005 + 0.333 * i, 0.06, 0.323, 0.74]) for i in range(3)]
    testo = fig.text(0.5, 0.86, "", ha="center", fontsize=12, family="monospace")
    fig.text(0.5, 0.95, TITOLO, ha="center", fontsize=13)
    stato_qd = {}

    def base(i):
        q, v = Q[i], vis[i]
        for a_ in ax:
            a_.clear()
        tri = mtri.Triangulation(q["d"][v, 0], q["d"][v, 1])
        lr = np.log10(np.maximum(q["rho"][v], 10 ** lmin))
        ax[0].tripcolor(tri, lr, shading="gouraud", cmap="viridis", vmin=lmin, vmax=lmax)
        ax[0].set_title("log10 rho_psi (scala fissa)", fontsize=10)
        ax[1].tripcolor(tri, q["chi"][v], shading="gouraud", cmap="magma", vmin=cmin, vmax=cmax)
        ax[1].set_title("chi (scala fissa)", fontsize=10)
        dentro = q["r"] <= R_RETICOLO
        e = dentro[q["ii"]] & dentro[q["jj"]]
        seg = np.stack([q["d"][q["ii"][e]], q["d"][q["jj"][e]]], axis=1)
        lun = np.hypot(seg[:, 1, 0] - seg[:, 0, 0], seg[:, 1, 1] - seg[:, 0, 1])
        seg = seg[lun < 3.0]                                     # ### gli archi che attraversano il bordo periodico non si disegnano
        ax[2].add_collection(LineCollection(seg, colors="0.55", linewidths=0.35))
        vecchi = np.nonzero(dentro[:n0])[0]
        ax[2].plot(q["d"][vecchi, 0], q["d"][vecchi, 1], ".", color="0.45", ms=1.5)
        ax[2].set_title("il reticolo entro r %.0f: i nati accesi, poi ciano" % R_RETICOLO, fontsize=10)
        for a_ in ax:
            a_.set_xlim(-MEZZO, MEZZO)
            a_.set_ylim(-MEZZO, MEZZO)
            a_.set_aspect("equal")
            a_.set_xticks([])
            a_.set_yticks([])
        k_prec = KS[i] - OGNI
        stato_qd["fissi"] = ax[2].plot([], [], "o", color="c", ms=3.0)[0]
        stato_qd["accesi"] = ax[2].plot([], [], "o", color="yellow", mec="r", ms=6.5)[0]
        stato_qd["prima"] = np.nonzero(kb <= k_prec)[0]
        stato_qd["qui"] = np.nonzero((kb > k_prec) & (kb <= KS[i]))[0]

    def fotogramma(i, s):
        """### il fotogramma `s` del quadro `i`: le nascite dell'intervallo con `k_b - k_prec <= (s + 1) * 250 / 60`."""
        q = Q[i]
        k_prec = KS[i] - OGNI
        qui = stato_qd["qui"]
        acc = qui[(kb[qui] - k_prec) * PER_QUADRO <= (s + 1) * OGNI] if s >= 0 else qui[:0]
        fis = stato_qd["prima"]
        fis = fis[nb[fis] < q["n"]]
        dn = q["d"][nb[fis]]
        dentro = (np.abs(dn[:, 0]) <= MEZZO) & (np.abs(dn[:, 1]) <= MEZZO)
        stato_qd["fissi"].set_data(dn[dentro, 0], dn[dentro, 1])
        da = q["d"][nb[acc]]
        stato_qd["accesi"].set_data(da[:, 0], da[:, 1])
        tot = len(fis) + len(acc)
        testo.set_text("k %5d   nascite %3d   R %6.2f   max rho %.3e   E_persa %+.4e" % (KS[i], tot, q["R"], float(q["rho"].max()), q["E_persa"]))
        return tot, len(fis), len(acc)
    W = animation.FFMpegWriter(fps=FPS, codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
    nf = 0
    with W.saving(fig, USCITA, dpi=100):
        for i in range(len(KS)):
            base(i)
            if i == 0:
                fotogramma(0, -1)
                for _ in range(FERMO_S * FPS):
                    W.grab_frame()
                    nf += 1
            for s in range(PER_QUADRO):
                ultimo = fotogramma(i, s)
                W.grab_frame()
                nf += 1
            if i == len(KS) - 1:
                for _ in range(FERMO_S * FPS):
                    W.grab_frame()
                    nf += 1
                fig.savefig(PNG, dpi=100)
    plt.close(fig)
    tot, nfis, nacc = ultimo
    nl = sum(1 for _q, k, _n in nascite_log(LOG) + (nascite_log(LOG_R3) if x.da_r3 else []) if k <= KS[-1])
    if x.da_r3:
        nl = len([b for b in B if b["k"] <= KS[-1]])
    ok = tot == nl == Q[-1]["nascite"]
    print("  %d fotogrammi (%.1f s); il video %s (%.2f MB); il png %s" % (nf, nf / FPS, USCITA, os.path.getsize(USCITA) / 1e6, PNG))
    print("  DEVE: i nodi in evidenza nell'ultimo fotogramma (%d: fissi %d, accesi %d) = le nascite del log con k <= %d (%d) = meta (%d): %s" % (
        tot, nfis, nacc, KS[-1], nl, Q[-1]["nascite"], "PASSA" if ok else "### FALLISCE"))
    print("  (i nati fuori dalla finestra +-%.0f non si disegnano ma si contano: il conto e' sul registro)" % MEZZO)
    print("=" * 134)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
