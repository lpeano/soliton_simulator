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
| **DESTRA** | **`cos(phi_k - phibar_m(t))`**: la coerenza con la fase **CORRENTE** della propria massa | **fissa `[-1, +1]`**, colormap divergente |

> ### ⚠ **IL RIFERIMENTO DI DESTRA E' CO-ROTANTE, E SI RICALCOLA A OGNI FOTOGRAMMA.**
> `phibar_m(t) = arg <e^{i phi}>` sui **nodi della massa `m` AL PASSO 0**.
> **Perche' non la fase iniziale:** una **rotazione RIGIDA** della massa — tutti i nodi che
> girano insieme — con un riferimento fisso apparirebbe come uno **SCIOGLIMENTO**, e non lo
> e'. Col riferimento co-rotante **una rotazione rigida resta ACCESA**, e si spegne **solo**
> cio' che perde coerenza **INTERNA**.
>
> ### 🎯 **LO SCOPO DICHIARATO: distinguere FRANTUMAZIONE da MESCOLAMENTO.**
> | sinistra *(pozzo)* | destra *(coerenza interna)* | lettura |
> |---|---|---|
> | **a chiazze** | **spenta** | ### **FRANTUMAZIONE**: la massa si rompe in grumi |
> | **spenta** | **spenta** | ### **MESCOLAMENTO**: la massa si diluisce nel vuoto |
> | piena | **accesa** | la massa tiene *(anche se ruota)* |
>
> **⚠ E IL VUOTO CON CHE COSA SI CONFRONTA? SCELTA DICHIARATA (`V10`), fra tre possibili:**
> **NON** con la `phibar` della **massa piu' vicina sul disegno** — metterebbe **`pos` dentro
> una grandezza di FASE**, e il colore cambierebbe quando **il disegno si rilassa**;
> **NON** con **`dphi/2` fisso** — **non co-ruota**, e su una rotazione rigida globale le masse
> resterebbero accese mentre il vuoto cambia colore: **le due meta' dello stesso pannello
> direbbero cose incoerenti**.
> **SI', coi tre insiemi di massa PRESI INSIEME**
> (`arg <e^{i phi}>` su tutti i loro nodi). **E' una scelta DICHIARATA, non l'unica
> possibile**: serve a rispondere a *«il vuoto e' in fase con le masse?»*. **Se le tre
> `phibar_m` divergessero fra loro, quel riferimento perderebbe senso** — e per questo **si
> stampa la loro dispersione in sovrimpressione**, invece di lasciarla implicita.

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
from matplotlib.patches import Polygon                                 # noqa: E402
from scipy.spatial import ConvexHull                                   # noqa: E402

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


SIGMA_SCENA = 0.05          # la dispersione che LA SCENA scrive: non e' mia
KAPPA = 3                   # la stessa tolleranza calibrata dal pilota (`R-VICINO`)


def diagnostici_del_fotogramma(phi, MASSE, n, bar):
    """`V9` -- i diagnostici **DI QUESTO FOTOGRAMMA**, dal `phi` salvato e dalle coorti del passo 0.

    **Prima venivano dal blocco del checkpoint PIU' VICINO**: su 61 fotogrammi mostravano **4**
    valori, e un fotogramma al passo `38` portava i numeri del passo `40`. **Un numero accanto a
    un'immagine, che non e' di quell'immagine, e' peggio di nessun numero.**

    | | |
    |---|---|
    | **`coer_campo_m`** | il modulo di `mean(e^{i phi})` sui nodi della massa `m` **al passo 0** -- **lo stesso insieme del pilota**, quindi lo stesso numero |
    | **`n_coer_m`** | quanti nodi della massa `m` al passo 0 sono ancora entro `KAPPA*SIGMA` dalla **propria `phibar_m(t)`** |

    ⚠ **`n_coer` NON E' IL `n_fase` DEL PILOTA**, e per questo **si chiama diversamente**: `n_fase`
    conta la regione di fase **assegnata SUL GRAFO** (`R-VICINO`), e **il grafo completo non sta nel
    fotogramma** *(gli archi sono sottocampionati a 24000)*. **Dare lo stesso nome a due cose
    diverse sarebbe il difetto che l'indice degli ID ha curato.**
    """
    fuori = {"coer": [], "n_coer": []}
    for k in sorted(MASSE):
        idx = MASSE[k]
        idx = idx[idx < n]
        if not len(idx):
            continue
        p = phi[idx]
        fuori["coer"].append((k, float(abs(np.mean(np.exp(1j * p))))))
        if k in bar:
            dv = np.angle(np.exp(1j * (p - bar[k])))
            fuori["n_coer"].append((k, int(np.sum(np.abs(dv) <= KAPPA * SIGMA_SCENA))))
    return fuori if fuori["coer"] else None


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
        print("[video] ** %s ** -- mancano i DIAGNOSTICI `V4` (coer_campo, n_fase). Il bordo e "
              "il riferimento per massa vengono dalle COORTI, e ci sono lo stesso." % nota)

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
    MASSE = {}          # gli INDICI del passo 0 per massa: servono al riferimento co-rotante
    _hull_saltati = [0]  # `A8`: gli inviluppi degeneri si CONTANO, non si ignorano
    # ⚠ LE COORTI NON DIPENDONO DAL `misura.json`, e prima ci dipendevano: `lancia()` CANCELLA
    #   `misura.json` all'avvio del run, quindi durante il run il bordo e il riferimento
    #   co-rotante SPARIVANO -- e il video usciva senza `V3`, con l'aria di stare bene.
    if True:
        b0 = None
        # le coorti non stanno nel json: si ricostruiscono dai medoidi? NO -- si DICE.
        # Il `misura.json` porta le TAGLIE, non gli indici: il bordo si prende dal file
        # `coorti0.npz` se il braccio lo ha salvato, altrimenti NIENTE bordo, dichiarato.
        pc = os.path.join(STATI, "coorti_seme%d.npz" % seme)
        if os.path.exists(pc):
            zc = np.load(pc, allow_pickle=False)
            for k in sorted(zc.files):
                if k.startswith("massa_"):
                    idx = np.asarray(zc[k], int)
                    idx = idx[idx < n0]
                    MASSE[k] = idx
                    bordo[idx] = True
            print("[video] bordo: %d nodi in %d masse del passo 0"
                  % (int(bordo.sum()), len(MASSE)))
        else:
            print("[video] ** nessun `coorti_seme%d.npz`: NIENTE bordo (`V3` NON soddisfatto) **"
                  % seme)
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

            # ------------------------------- DESTRA: la coerenza con la fase CORRENTE della massa
            # `phibar_m(t) = arg <e^{i phi}>` sui nodi della massa `m` AL PASSO 0, RICALCOLATO
            # a ogni fotogramma: cosi' una ROTAZIONE RIGIDA resta ACCESA e si spegne SOLO cio'
            # che perde coerenza INTERNA. (Mandato di Luca; il riferimento fisso `dphi/2` faceva
            # sembrare scioglimento una rotazione.)
            rif = np.full(n, np.nan)
            _bar = {}
            for _k, _idx in MASSE.items():
                _i = _idx[_idx < n]
                if not len(_i):
                    continue
                _bar[_k] = float(np.angle(np.mean(np.exp(1j * phi[_i]))))
                rif[_i] = _bar[_k]
            if _bar:
                _tutti = np.concatenate([MASSE[k][MASSE[k] < n] for k in _bar])
                _glob = float(np.angle(np.mean(np.exp(1j * phi[_tutti]))))
                # IL VUOTO si confronta con LE TRE MASSE INSIEME: scelta DICHIARATA (docstring).
                rif[np.isnan(rif)] = _glob
            else:
                rif[:] = DPHI / 2.0          # nessuna massa nota: si ricade sul riferimento fisso
            coer = np.cos(phi - rif)
            axD.scatter(pos[:, 0], pos[:, 1], c=coer, s=9.0, cmap="coolwarm",
                        vmin=-1.0, vmax=1.0, linewidths=0.0, zorder=2)
            # `V8`: IL CONTORNO DELLA REGIONE, non un bordo sui nodi.
            #   PRIMA era un secondo scatter piu' GRANDE (`s=26`, `lw=0.55`) e COPRIVA il colore
            #   di fase dentro la massa -- cioe' la grandezza che questo pannello esiste per
            #   mostrare. POI l'ho reso sottile e semitrasparente, e a quel punto era INVISIBILE
            #   fra 12802 nodi. Entrambe viste su un PNG estratto dal video, non dedotte.
            #   Il CONTORNO (inviluppo convesso dei nodi della massa al passo 0, sulle posizioni
            #   CORRENTI) dice DOVE era la massa **senza toccare un solo pixel di colore**.
            for _k, _idx in MASSE.items():
                _i = _idx[_idx < n]
                if len(_i) < 3:
                    continue
                try:
                    _h = ConvexHull(pos[_i, :2])
                    _pc = pos[_i][_h.vertices, :2]
                    axD.add_patch(Polygon(_pc, closed=True, fill=False,
                                          edgecolor=(0.55, 1.0, 0.0, 0.85), linewidth=1.6,
                                          zorder=5))
                except Exception:
                    # un inviluppo degenere (nodi allineati) non e' un errore: si SALTA e si conta
                    _hull_saltati[0] += 1
            axD.set_title("COERENZA INTERNA  cos(phi - phibar_m(t))   riferimento CO-ROTANTE "
                          "per massa, scala FISSA [-1, +1]" + NL + "bordo verde = i nodi delle tre "
                          "masse AL PASSO 0 (contorno)   |   VUOTO riferito alle TRE MASSE"
                          + NL + "INSIEME, non alla piu' vicina: `pos` non entra in una fase",
                          color="white", fontsize=9.0)

            # ---------------------------------------------- la sovrimpressione
            dg = diagnostici_del_fotogramma(phi, MASSE, n, _bar)
            righe = ["passo %-4d n %-6d" % (passo, n)]
            if len(_bar) > 1:
                # ⚠ SE LE TRE `phibar_m` DIVERGONO, il riferimento del VUOTO perde senso:
                #   si stampa, invece di lasciarlo implicito (`A8`).
                _v = np.array(sorted(_bar.values()))
                # il MASSIMO dello scarto angolare dal riferimento medio: `abs` PRIMA del
                # `max`, senno' un massimo negativo darebbe un numero piu' piccolo del vero.
                _sp = float(np.max(np.abs(np.angle(
                    np.mean(np.exp(1j * _v)) * np.exp(-1j * _v)))))
                righe.append("phibar: %s   disp %.3f rad"
                             % ("  ".join("%s %+.2f" % (k.replace("massa_", "m"), _bar[k])
                                          for k in sorted(_bar)), _sp))
            if dg:
                righe.append("coer_campo %s"
                             % "  ".join("%s %.4f" % (k.replace("massa_", "m"), v)
                                         for k, v in dg["coer"]))
                righe.append("n_coer %s"
                             % "  ".join("%s %d" % (k.replace("massa_", "m"), v)
                                         for k, v in dg["n_coer"]))
            # `V9`: il testo si sistema con una COLONNA fissa invece che a occhio -- `passo` e
            #   `n` sono a larghezza fissa nel formato, e il resto parte da 0.20.
            fig.text(0.006, 0.995, righe[0], color="white", fontsize=12.0,
                     va="top", family="monospace", weight="bold")
            if len(righe) > 1:
                fig.text(0.200, 0.995, "     ".join(righe[1:]), color="#9fe3ff",
                         fontsize=10.0, va="top", family="monospace")
            fig.text(0.5, 0.012, DIDASCALIA, color="#ffd34d", fontsize=12.5, ha="center",
                     family="monospace")
            # ⚠ SE UN CRITERIO NON E' SODDISFATTO, LO DEVE DIRE IL FOTOGRAMMA, non lo stdout:
            #   un video che esce con l'aria di star bene e senza il bordo e' peggio di uno che
            #   non esce (`A9`). Stessa logica della didascalia `V5`.
            _manca = []
            if not MASSE:
                _manca.append("V3 bordo/riferimento per massa")
            if not dg:
                _manca.append("V4 coer_campo e n_fase")
            if _manca:
                fig.text(0.5, 0.042, "** MANCA: " + " ; ".join(_manca) +
                         "  (nessun misura.json / coorti: il run e' ancora in corso?) **",
                         color="#ff5555", fontsize=11.5, ha="center", family="monospace")
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
    if _hull_saltati[0]:
        print("  ⚠ contorni saltati (inviluppo degenere): %d" % _hull_saltati[0])
    print("  ⚠ NON VA IN GIT (`STATI-LOCALI`): in git vanno sha1, percorso e questo comando.")
    print("=" * 96)
    return out, sha


if __name__ == "__main__":
    A = sys.argv[1:]

    def opz(nome, dflt):
        return A[A.index(nome) + 1] if nome in A else dflt
    principale(int(opz("--seme", "11")), int(opz("--fps", "8")), int(opz("--dpi", "110")),
               int(opz("--max-frame", "0")))
