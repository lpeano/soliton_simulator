r"""**IL VIDEO DELLA SCENA DEL PILOTA** — due pannelli, dagli stessi fotogrammi.

*(Richiesta di Luca, 2026-09-27. Criteri in `doc/TASK_HISTORY/2026-09-27_video-scena.md`,
committati **prima** del codice. Voce `VIDEO-SCENA`.)*

> ## ⚠⚠ **CHE COSA QUESTO VIDEO PUO' MENTIRE: LA VICINANZA.**
> Le posizioni sono **`pos`**, che e' **IL DISEGNO**. La fisica di questo repo vive **sugli ARCHI**:
> le distanze sono `net.d` **lungo il grafo**, e `pos` **non entra nella dinamica** (`A3-DISEGNO`).
> **Due nodi possono apparire vicini sullo schermo ed essere lontani sul grafo.**
> **La didascalia lo dice in OGNI fotogramma, ed e' il criterio `V5`: se manca, il video non si
> consegna.**

**I DUE PANNELLI:**

| | che cosa mostra | scala |
|---|---|---|
| **SINISTRA** | **la vista di sempre del simulatore**: nodi `magma` su `phi_g` *(il pozzo)*, archi `plasma` su `\|dpozzo\|` | ⚠ **`vmax` FISSO al massimo del PASSO 0**, non del fotogramma |
| **DESTRA** | **`cos(phi_k - dphi/2)`**: la coerenza con la fase delle masse | **fissa `[-1, +1]`**, colormap divergente |

> ### ⚠ **PERCHE' `vmax` FISSO, ed e' il cuore del mandato:** la vista di sempre usa
> ### `phi_max = max(phi_g)` **del fotogramma corrente** (`soliton_simulator.py:7698`).
> Con una scala che si **ricalibra a ogni fotogramma**, un pozzo che si appiattisce mostra **sempre
> lo stesso contrasto**: **lo scioglimento viene ricalibrato via.** E' `A3` applicato a un'immagine
> — la stessa famiglia del *«normalizzato sulla propria mediana»*.
> **IL RENDERER DI SEMPRE NON E' TOCCATO:** la scala fissa vive **qui**.

**IL BORDO** marca i nodi delle tre masse **DEL PASSO 0**, e solo quelli (`V3`): si vede **chi era
massa**, non chi lo sembra adesso.

    python csv/_test_fork/_video_scena.py                      # seme 11, tutti i fotogrammi
    python csv/_test_fork/_video_scena.py --fps 10 --dpi 120
    python csv/_test_fork/_video_scena.py --max-frame 6         # giro corto d'impianto

ASCII puro.
"""
import glob
import hashlib
import io
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: non costruisce nessuna scena e non carica il simulatore: legge i fotogrammi `.npz`
#   di un run che ha GIA' dichiarato la propria configurazione intera nel suo referto. E' un
#   RENDERER, non una misura, e non entra in nessun referto.

import matplotlib                                                      # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                        # noqa: E402
from matplotlib.animation import FFMpegWriter                          # noqa: E402
from matplotlib.collections import LineCollection                      # noqa: E402

NL = chr(10)
DEST = os.path.join(_QUI, "_pilota_prova1")
STATI = os.path.join(DEST, "stati")
DIDASCALIA = "posizioni = disegno (A3-DISEGNO), non distanze fisiche"


def fotogrammi(seme):
    v = sorted(glob.glob(os.path.join(STATI, "frame_seme%d_passo*.npz" % seme)))
    return v


def coorti0(seme):
    """Le tre regioni del passo 0, dal `misura.json` -- e se non ci sono, si DICE."""
    p = os.path.join(DEST, "seme_%d" % seme, "misura.json")
    if not os.path.exists(p):
        return None, "nessun misura.json per il seme %d" % seme
    d = json.load(io.open(p, encoding="utf-8"))
    n0 = int(d.get("n0", 0))
    return (d, "") if n0 else (None, "il misura.json non porta `n0`")


def diagnostici(d, passo):
    """`coer_campo` per massa e `n_fase`, dal blocco del checkpoint PIU' VICINO (e si dice quale)."""
    if not d:
        return None
    cps = sorted(int(b["passo"]) for b in d["blocchi"])
    vicino = min(cps, key=lambda c: abs(c - passo))
    b = [x for x in d["blocchi"] if int(x["passo"]) == vicino][0]
    masse = sorted(b["forma_passo0"].keys())
    return dict(passo_blocco=vicino,
                coer=[(k, float(b["forma_passo0"][k]["coer_campo"])) for k in masse],
                n_fase=[(k, int(b["fase"]["per_massa"][k]["n"])) for k in masse])


def principale(seme, fps, dpi, max_frame):
    f = fotogrammi(seme)
    if not f:
        raise SystemExit("[video] NESSUN fotogramma in %s: il braccio va girato con "
                         "`--salva-stati --ogni 2`. Non invento un fallback." % STATI)
    if max_frame:
        f = f[:max_frame]
    if not FFMpegWriter.isAvailable():
        raise SystemExit("[video] FFMpegWriter NON disponibile: MI FERMO invece di produrre un "
                         "file monco. (`A9`: uno strumento che tace quando non funziona non e' "
                         "uno strumento.)")
    d, nota = coorti0(seme)
    if nota:
        print("[video] ** %s ** -- il bordo delle masse e i diagnostici NON ci saranno" % nota)

    # ------------------------------------------------------------------ il PASSO 0 fissa le scale
    z0 = np.load(f[0], allow_pickle=False)
    n0 = int(z0["n"])
    # ⚠⚠ AL PASSO 0 IL POZZO E' IDENTICAMENTE ZERO, E NON E' UN BUG: `psi` NON ESISTE ANCORA.
    #   MISURATO: max(phi_g) = 0 al passo 0, 1233.86 al passo 2, 876.35 al passo 4.
    #   Quindi <<il massimo del passo 0>> sarebbe ZERO, e la scala sarebbe degenere. Il
    #   riferimento e' IL PRIMO FOTOGRAMMA COL POZZO VIVO, e **si DICHIARA** -- nel titolo del
    #   pannello e nel resoconto -- invece di prendere il passo 0 e ritrovarsi con `1e-12`.
    #   (La premessa del mandato non regge, e lo si dice: e' `P1`.)
    _rif, PASSO_RIF = None, None
    for _p in f:
        _z = np.load(_p, allow_pickle=False)
        if float(np.max(_z["phi_g"])) > 0.0:
            _rif, PASSO_RIF = _z, int(_z["passo"])
            break
    if _rif is None:
        raise SystemExit("[video] IL POZZO E' ZERO IN OGNI FOTOGRAMMA: mi fermo invece di "
                         "disegnare una scala inventata.")
    VMAX_POZZO = float(np.max(_rif["phi_g"]))
    VMAX_DPOZZO = max(float(np.max(_rif["dpozzo"])) if int(_rif["na"]) else 0.0, 1e-12)
    DPHI = float(z0["dphi"])
    R = max(float(np.max(np.linalg.norm(z0["pos"][:, :2], axis=1))) * 1.18, 1e-6)
    print("[video] n(passo 0) = %d   dphi = %.6f" % (n0, DPHI))
    print("[video] SCALA FISSA dal passo %d (il PRIMO col pozzo vivo; al passo 0 `psi` non esiste "
          "e il pozzo e' ZERO): vmax_pozzo = %.6g   vmax_dpozzo = %.6g"
          % (PASSO_RIF, VMAX_POZZO, VMAX_DPOZZO))

    # i nodi delle tre masse del passo 0 (`V3`)
    bordo = np.zeros(n0, bool)
    if d:
        b0 = [x for x in d["blocchi"] if int(x["passo"]) == 0][0]
        # le coorti non stanno nel json: si ricostruiscono dai medoidi? NO -- si DICE.
        # Il `misura.json` porta le TAGLIE, non gli indici: il bordo si prende dal file
        # `coorti0.npz` se il braccio lo ha salvato, altrimenti NIENTE bordo, dichiarato.
        pc = os.path.join(STATI, "coorti_seme%d.npz" % seme)
        if os.path.exists(pc):
            zc = np.load(pc, allow_pickle=False)
            for k in zc.files:
                if k.startswith("massa_"):
                    idx = np.asarray(zc[k], int)
                    bordo[idx[idx < n0]] = True
            print("[video] bordo: %d nodi delle tre masse del passo 0" % int(bordo.sum()))
        else:
            print("[video] ** nessun `coorti_seme%d.npz`: NIENTE bordo, e lo dico invece di "
                  "inventarlo (`V3` non e' soddisfatto) **" % seme)
        del b0

    fig = plt.figure(figsize=(16.0, 8.4), facecolor="black")
    # ⚠ i pannelli scendono a 0.815 di altezza: con 0.885 i TITOLI andavano a sbattere
    #   sulla sovrimpressione, e il fotogramma diventava illeggibile. Visto su un PNG
    #   estratto dal video, non dedotto.
    axS = fig.add_axes([0.005, 0.060, 0.487, 0.815])
    axD = fig.add_axes([0.505, 0.060, 0.487, 0.815])
    for ax in (axS, axD):
        ax.set_facecolor("black")
    out = os.path.join(DEST, "VIDEO_scena_seme%d.mp4" % seme)
    w = FFMpegWriter(fps=fps, bitrate=6000,
                     metadata=dict(title="Pilota PROVA 1 - scena (ii)(a) - seme %d" % seme))
    t0 = time.time()
    with w.saving(fig, out, dpi=dpi):
        for k, percorso in enumerate(f):
            z = np.load(percorso, allow_pickle=False)
            n = int(z["n"])
            na = int(z["na"])
            passo = int(z["passo"])
            pos = z["pos"]
            phi = z["phi"]
            phi_g = z["phi_g"]
            for ax in (axS, axD):
                ax.clear()
                ax.set_facecolor("black")
                ax.set_xlim(-R, R)
                ax.set_ylim(-R, R)
                ax.set_aspect("equal")
                ax.axis("off")

            # ---------------------------------------------- SINISTRA: la vista di sempre
            if na:
                ii, jj = np.asarray(z["ii"], int), np.asarray(z["jj"], int)
                ok = (ii < n) & (jj < n)
                seg = np.stack([pos[ii[ok], :2], pos[jj[ok], :2]], axis=1)
                lc = LineCollection(seg, cmap="plasma", linewidths=0.8, alpha=0.72, zorder=1)
                lc.set_array(np.clip(z["dpozzo"][ok] / VMAX_DPOZZO, 0.0, 1.0))
                axS.add_collection(lc)
            dim = 18.0 + 38.0 * np.sqrt(np.clip(phi_g / VMAX_POZZO, 0.0, 1.0))
            axS.scatter(pos[:, 0], pos[:, 1], c=phi_g, s=dim, cmap="magma",
                        vmin=0.0, vmax=VMAX_POZZO, edgecolors="white", linewidths=0.35, zorder=3)
            axS.set_title("VISTA DI SEMPRE - pozzo `phi_g` (magma), archi `|dpozzo|` (plasma)"
                          + NL + "vmax FISSO al passo %d (%.4g), non al fotogramma: senza, lo "
                          "scioglimento si ricalibra via" % (PASSO_RIF, VMAX_POZZO),
                          color="white", fontsize=9.5)

            # ---------------------------------------------- DESTRA: la coerenza con le masse
            coer = np.cos(phi - DPHI / 2.0)
            axD.scatter(pos[:, 0], pos[:, 1], c=coer, s=9.0, cmap="coolwarm",
                        vmin=-1.0, vmax=1.0, linewidths=0.0, zorder=2)
            if bordo.any() and n >= n0:
                m = np.zeros(n, bool)
                m[:n0] = bordo
                axD.scatter(pos[m, 0], pos[m, 1], c=coer[m], s=26.0, cmap="coolwarm",
                            vmin=-1.0, vmax=1.0, edgecolors="lime", linewidths=0.55, zorder=4)
            axD.set_title("COERENZA CON LE MASSE  cos(phi - dphi/2)   scala FISSA [-1, +1]"
                          + NL + "bordo verde = i nodi delle tre masse AL PASSO 0",
                          color="white", fontsize=9.5)

            # ---------------------------------------------- la sovrimpressione
            dg = diagnostici(d, passo) if d else None
            righe = ["passo %d    n %d" % (passo, n)]
            if dg:
                righe.append("coer_campo (checkpoint %d): %s"
                             % (dg["passo_blocco"],
                                "  ".join("%s %.4f" % (k.replace("massa_", "m"), v)
                                          for k, v in dg["coer"])))
                righe.append("n_fase: %s"
                             % "  ".join("%s %d" % (k.replace("massa_", "m"), v)
                                         for k, v in dg["n_fase"]))
            fig.text(0.006, 0.995, righe[0], color="white", fontsize=12.0,
                     va="top", family="monospace", weight="bold")
            if len(righe) > 1:
                fig.text(0.175, 0.995, "      ".join(righe[1:]), color="#9fe3ff",
                         fontsize=10.5, va="top", family="monospace")
            fig.text(0.5, 0.012, DIDASCALIA, color="#ffd34d", fontsize=12.5, ha="center",
                     family="monospace")
            w.grab_frame()
            for tx in list(fig.texts):
                tx.remove()
            if k % 10 == 0:
                print("[video] fotogramma %d/%d (passo %d)" % (k + 1, len(f), passo), flush=True)
    plt.close(fig)
    dt = time.time() - t0
    with open(out, "rb") as fh:
        sha = hashlib.sha1(fh.read()).hexdigest()
    mb_f = sum(os.path.getsize(x) for x in f) / 1e6
    mb_v = os.path.getsize(out) / 1e6
    print(NL + "=" * 96)
    print("VIDEO: %s" % out)
    print("  sha1 (byte grezzi) %s" % sha)
    print("  fotogrammi %d (%.2f MB)   video %.2f MB   rendering %.1f s   fps %d   dpi %d"
          % (len(f), mb_f, mb_v, dt, fps, dpi))
    print("  scala del pozzo FISSA dal passo %d: vmax %.6g  (al passo 0 `psi` non esiste e il "
          "pozzo e' ZERO)" % (PASSO_RIF, VMAX_POZZO))
    print("  ⚠ NON VA IN GIT (`STATI-LOCALI`): in git vanno sha1, percorso e questo comando.")
    print("=" * 96)
    return out, sha


if __name__ == "__main__":
    A = sys.argv[1:]

    def opz(nome, dflt):
        return A[A.index(nome) + 1] if nome in A else dflt
    principale(int(opz("--seme", "11")), int(opz("--fps", "8")), int(opz("--dpi", "110")),
               int(opz("--max-frame", "0")))
