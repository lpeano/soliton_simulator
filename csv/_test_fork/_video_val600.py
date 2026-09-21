# -*- coding: utf-8 -*-
"""IL VIDEO DEL RUN DI VALIDAZIONE -- **per guardarlo, non per misurarlo**.

⚠⚠ **ESISTE GIA' UNO STRUMENTO VIDEO, E VA LETTO PRIMA DI USARE QUESTO:**
  **`csv/_test_fork/_video_da_snapshot.py`** *(task history `2026-09-20_video-da-snapshot.md`,
  commit `d20a3ea`)*, che ha gia' prodotto `video_g6000.mp4` da 46 fotogrammi.
  **Quello ha un pregio che QUESTO non ha: NON ESEGUE NESSUNA FISICA.** Legge gli snapshot e
  chiama **solo** le funzioni di disegno -- `diagnostica()`, `campo_spaziale()`,
  `pozzo_grafo()`, `intensita()` -- verificate dal sorgente come pure di rendering.
  **E' la strada piu' sicura, e se bastano pochi fotogrammi si usa QUELLA.**

  **PERCHE' ALLORA QUESTO ESISTE, ed e' l'unica ragione:** la validazione ha **CINQUE**
  snapshot *(uno ogni 120 passi)*, quindi `_video_da_snapshot.py` su `_val600` darebbe
  **5 fotogrammi = 0.25 s di video a 20 fps**. Per averne 100 servirebbero 100 snapshot da
  ~36 MB, cioe' **~3.6 GB**. Questo strumento li ottiene **rigiocando**, al costo di
  **rieseguire la fisica** *(~35 minuti)* e di dover **DIMOSTRARE** che la rigiocata e'
  quel run -- che e' cio' che fa il confronto al passo 600.

  **LA SCELTA FRA I DUE E' DI LUCA, e i numeri per deciderla sono questi:**
  `_video_da_snapshot.py` -> **5 fotogrammi, ZERO fisica, subito**;
  `_video_val600.py`      -> **100 fotogrammi, fisica rieseguita, ~35 min + disegno**.

⚠⚠ LE POSIZIONI SONO UN DISEGNO, NON FISICA (`Z47`), E IL VIDEO NON DEVE FAR CREDERE IL CONTRARIO.
  `pos` e' prodotta da `rilassa_disegno()`, che e' un LAYOUT: serve a vedere il grafo, non e' la
  geometria del sistema. **Ogni fotogramma porta la riga fissa
  «posizioni = disegno (Z47); colori = fisica».** La fisica sta **nei COLORI e nei NUMERI**.

PERCHE' SI RIGIOCA invece di usare gli snapshot: la validazione ne ha **5**, uno ogni 120 passi --
**troppo pochi per un video**. Il sistema e' **deterministico** e la rigiocata e' **sigillata**,
quindi si rigioca **dalla semina con la STESSA configurazione, byte per byte**, e si prende un
fotogramma ogni `OGNI` passi.

⚠ E LA PROVA CHE E' QUEL RUN, non un altro: al passo **600** lo stato si confronta con
  `csv/_test_fork/_val600/scena_000600.pkl.gz`, campo per campo. **Se non coincide, il video NON
  mostra la validazione, e lo strumento lo DICE invece di montarlo lo stesso.**

⚠ LA SCALA DEI COLORI E' FISSA PER TUTTO IL VIDEO, e non e' una scelta estetica: riscalarla
  fotogramma per fotogramma **farebbe sparire un cambiamento vero**, perche' ogni fotogramma
  sembrerebbe uguale al precedente.
  **`d/d0` in `[0.5, 1.5]` con `1.0` AL CENTRO**, e il centro non e' scelto: **`d/d0 = 1` e'
  l'assenza di tensione E di compressione**, cioe' il punto neutro fisico. L'ampiezza `±0.5`
  copre il campo misurato nella validazione *(`0.69`-`0.84`)* con margine da entrambe le parti,
  **cosi' una eventuale TENSIONE si vedrebbe quanto la compressione**.

I DUE PANNELLI, e non di piu': **un pannello in piu' e' un pannello che nessuno guarda.**
  (1) **LA RETE** -- archi colorati per `d/d0`, nodi per REGIONE *(vuoto / massa / nato)*;
  (2) **IL TEMPO** -- mediane di `d`, `d0` e `d/d0` dall'inizio, con il marcatore sul fotogramma.

⚠ IL VIDEO E I FOTOGRAMMI NON VANNO IN GIT: vanno su `E:\\soliton_archivio\\`. In git va SOLO
  questo strumento.
ASCII PURO.
"""
import glob
import gzip
import io
import os
import pickle
import subprocess
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)

PASSI = 600
OGNI = 6                       # 600 / 6 = 100 fotogrammi
DEST = r"E:\soliton_archivio\video_val600"
RIF = os.path.join(RADICE, "csv", "_test_fork", "_val600", "scena_000600.pkl.gz")
SOLO_PROVA = False             # `--prova`: 12 passi, per vedere che monta
for _a in sys.argv[1:]:
    if _a.startswith("--passi="):
        PASSI = int(_a.split("=", 1)[1])
    if _a.startswith("--ogni="):
        OGNI = int(_a.split("=", 1)[1])
    if _a.startswith("--dest="):
        DEST = _a.split("=", 1)[1]
    if _a == "--prova":
        SOLO_PROVA = True
        PASSI, OGNI = 12, 6

# LA SCALA FISSA, dichiarata QUI e non dedotta fotogramma per fotogramma
DD0_MIN, DD0_MAX = 0.5, 1.5

ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part",
        "--peq-esatto", "--peq-nascita-locale", "--scala-min-passo", "--coes-causale",
        "--anom-simm", "--invarianti=on"]

N_VUOTO, N0_SEMINA = 900, 2391   # vuoto = [0,900)  masse = [900,2391)  nati = >= 2391


def confronta_col_riferimento(net, S):
    """LA PROVA che il video mostra QUEL run: lo stato al passo 600 contro lo snapshot vero."""
    if not os.path.exists(RIF):
        return None, "lo snapshot di riferimento NON esiste: %s" % RIF
    with gzip.open(RIF, "rb") as f:
        a = pickle.load(f)["attrs"]
    campi = ("d", "d0", "vd", "peq", "psi", "phi", "eta", "perc_chi", "perc_geom", "tw")
    diversi, confrontati = [], 0
    for k in campi:
        if k not in a or not hasattr(net, k):
            continue
        x = np.asarray(a[k]); y = np.asarray(getattr(net, k))
        confrontati += 1
        if x.shape != y.shape:
            diversi.append("%s(shape %s vs %s)" % (k, x.shape, y.shape))
        elif not np.array_equal(x, y):
            diversi.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(x - y)))))
    return (not diversi) and confrontati >= 8, (
        "%d campi confrontati, %s" % (confrontati,
                                      "IDENTICI" if not diversi else "DIVERSI: %s" % diversi[:4]))


def main():
    os.makedirs(DEST, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    os.chdir(RADICE)
    sys.argv = list(ARGV)
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    for f in ("PEQ_ESATTO", "PEQ_NASCITA_LOCALE", "SCALA_MIN_PASSO", "COES_CAUSALE",
              "ANOM_SIMM", "INVARIANTI"):
        if not getattr(S, f):
            raise SystemExit("[video] %s e' SPENTO: non e' la configurazione della validazione" % f)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    PPF = int(S.PASSI_PER_FRAME)

    serie = {"passo": [], "med_d": [], "med_d0": [], "med_dd0": []}
    quadri = []
    t0 = time.time()
    for k in range(1, PASSI + 1):
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net); net.step(); net.mitosi()
        net.rilassa_disegno(); net.memoria_hebbiana_moto()
        d = np.asarray(net.d, float); d0 = np.asarray(net.d0, float)
        serie["passo"].append(k)
        serie["med_d"].append(float(np.median(d)))
        serie["med_d0"].append(float(np.median(d0)))
        serie["med_dd0"].append(float(np.median(d / np.maximum(d0, 1e-300))))
        if k % OGNI:
            continue
        # ---------------- IL FOTOGRAMMA
        n = net.n
        pos = np.asarray(net.pos)[:n, :2]
        ii = np.asarray(net.i); jj = np.asarray(net.j)
        m = (ii < n) & (jj < n)
        dd0 = np.clip(d[m] / np.maximum(d0[m], 1e-300), DD0_MIN, DD0_MAX)
        seg = np.stack([pos[ii[m]], pos[jj[m]]], axis=1)
        reg = np.where(np.arange(n) < N_VUOTO, 0, np.where(np.arange(n) < N0_SEMINA, 1, 2))

        fig, (ax, ax2) = plt.subplots(1, 2, figsize=(16, 8), facecolor="#0b0b10",
                                      gridspec_kw={"width_ratios": [2, 1]})
        ax.set_facecolor("#0b0b10")
        lc = LineCollection(seg, cmap="coolwarm_r", norm=plt.Normalize(DD0_MIN, DD0_MAX),
                            linewidths=0.35, alpha=0.75)
        lc.set_array(dd0)
        ax.add_collection(lc)
        for r, col, et in ((0, "#4d5a6a", "vuoto"), (1, "#ffd166", "massa"),
                           (2, "#06d6a0", "nato")):
            s = reg == r
            if np.any(s):
                ax.scatter(pos[s, 0], pos[s, 1], s=(1.2 if r == 0 else 5.0), c=col,
                           linewidths=0, label="%s (%d)" % (et, int(np.sum(s))))
        ax.autoscale_view(); ax.set_aspect("equal"); ax.axis("off")
        ax.legend(loc="upper right", facecolor="#14141c", edgecolor="#333",
                  labelcolor="#ddd", fontsize=9, framealpha=0.9)
        cb = fig.colorbar(lc, ax=ax, fraction=0.03, pad=0.01)
        cb.set_label("d/d0   <1 COMPRESSO   1 neutro   >1 TESO   (scala FISSA)",
                     color="#ddd", fontsize=9)
        cb.ax.tick_params(colors="#ddd", labelsize=8)
        cb.outline.set_edgecolor("#444")

        nsub = int(getattr(net, "_g_smp_d_nsub", 0))
        ax.set_title("VALIDAZIONE -- passo %4d / %d     n = %d     archi = %d\n"
                     "med d = %.4f     med d0 = %.4f     med d/d0 = %.4f     nsub max = %d"
                     % (k, PASSI, n, int(np.sum(m)), serie["med_d"][-1], serie["med_d0"][-1],
                        serie["med_dd0"][-1], nsub),
                     color="#eee", fontsize=11, loc="left")

        ax2.set_facecolor("#0b0b10")
        ax2.plot(serie["passo"], serie["med_d"], color="#4cc9f0", lw=1.4, label="med d")
        ax2.plot(serie["passo"], serie["med_d0"], color="#f72585", lw=1.4, label="med d0")
        ax2.plot(serie["passo"], serie["med_dd0"], color="#ffd166", lw=1.4, label="med d/d0")
        ax2.axhline(1.0, color="#666", lw=0.8, ls="--")
        ax2.axvline(k, color="#fff", lw=0.8, alpha=0.6)
        ax2.set_xlim(0, PASSI)
        ax2.set_ylim(0, max(4.0, max(serie["med_d0"]) * 1.1))
        ax2.tick_params(colors="#bbb", labelsize=8)
        for sp in ax2.spines.values():
            sp.set_color("#444")
        ax2.legend(facecolor="#14141c", edgecolor="#333", labelcolor="#ddd", fontsize=9)
        ax2.set_title("le mediane nel tempo (la riga tratteggiata e' d/d0 = 1)",
                      color="#ddd", fontsize=10)

        # ⚠ LA RIGA FISSA, in OGNI fotogramma
        fig.text(0.5, 0.012,
                 "posizioni = DISEGNO (Z47) -- prodotte da rilassa_disegno(), NON sono la geometria "
                 "del sistema   |   colori = FISICA   |   scala dei colori FISSA per tutto il video",
                 ha="center", color="#9aa4b2", fontsize=10)
        fig.tight_layout(rect=(0, 0.03, 1, 1))
        p = os.path.join(DEST, "frame_%05d.png" % k)
        fig.savefig(p, dpi=96, facecolor=fig.get_facecolor())
        plt.close(fig)
        quadri.append(p)
        print("  fotogramma %d/%d (passo %d)  [%.1f s]" % (len(quadri), PASSI // OGNI, k,
                                                           time.time() - t0))

    # ---------------- LA PROVA: e' QUEL run?
    ok, dettaglio = (None, "confronto non eseguito (passi != 600)")
    if PASSI == 600:
        ok, dettaglio = confronta_col_riferimento(net, S)
    rel = io.open(os.path.join(DEST, "REFERTO.txt"), "w", encoding="utf-8", newline="\n")
    rel.write("VIDEO DELLA VALIDAZIONE -- %d fotogrammi, uno ogni %d passi\n" % (len(quadri), OGNI))
    rel.write("scala dei colori FISSA: d/d0 in [%.2f, %.2f], 1.0 al centro (punto neutro FISICO)\n"
              % (DD0_MIN, DD0_MAX))
    rel.write("posizioni = DISEGNO (Z47). I colori portano la fisica.\n")
    rel.write("PROVA che e' il run della validazione: %s -> %s\n"
              % ("PASSA" if ok else ("FALLISCE" if ok is False else "n/d"), dettaglio))
    rel.write("tempo: %.1f s\n" % (time.time() - t0))
    rel.close()
    print("\nPROVA che e' QUEL run: %s -- %s"
          % ("PASSA" if ok else ("*** FALLISCE ***" if ok is False else "n/d"), dettaglio))
    if ok is False:
        print("*** IL VIDEO NON MOSTRA LA VALIDAZIONE: non lo monto. ***")
        return 1

    # ---------------- IL MONTAGGIO
    mp4 = os.path.join(DEST, "val600.mp4")
    cmd = ["ffmpeg", "-y", "-framerate", "12", "-pattern_type", "glob",
           "-i", os.path.join(DEST, "frame_*.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", mp4]
    pr = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if pr.returncode == 0 and os.path.exists(mp4):
        print("VIDEO: %s  (%.1f MB, %d fotogrammi a 12 fps = %.1f s)"
              % (mp4, os.path.getsize(mp4) / 2 ** 20, len(quadri), len(quadri) / 12.0))
    else:
        print("ffmpeg ha FALLITO (rc=%d):\n%s" % (pr.returncode, pr.stderr[-800:]))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
