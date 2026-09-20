# -*- coding: utf-8 -*-
"""IL VIDEO DAGLI SNAPSHOT -- si legge e si disegna, nient'altro.

Scelte FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_video-da-snapshot.md (d20a3ea).

NESSUN RUN DI FISICA. Non si chiama step(), mitosi(), rilassa_disegno(),
memoria_hebbiana_moto(), scuoti_vuoto(). Si chiamano SOLO le funzioni di disegno del simulatore:
diagnostica(), campo_spaziale(), pozzo_grafo(), intensita(). Verificato dal sorgente che nessuna
chiama calcola_psi() e che scrivono solo cache di rendering.

IL BLOB: gli snapshot sono del blob 7c4dec1d, il codice e' 775ceab7, e carica_stato li RIFIUTA.
Si usa la STRADA B, DICHIARATA: la logica di carica_stato MENO la verifica del blob, compresa
l'invalidazione delle cache derivate (_S, _perm, _ker_cache). Nessun flag nuovo nel simulatore.
Le funzioni di disegno sono IDENTICHE nei due blob (confronto per funzione da git cat-file).

E' UNO STRUMENTO DI ISPEZIONE, NON UNA MISURA: nessun numero che esce di qui entra in un referto.
ASCII PURO nel codice.
"""
import glob
import gzip
import os
import pickle
import re
import subprocess
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
ARCHIVIO = os.path.join(RADICE, "csv", "_test_fork", "_g6000")
PROG = os.path.join(ARCHIVIO, "prog.csv")
DEST = os.path.join(RADICE, "csv", "_test_fork", "_video_g6000")
FPS = 20
# quattro colori netti, uno per componente, ordinati per indice-ancora crescente
COLORI = ["#4da6ff", "#ff6b3d", "#3ddc84", "#ffd23d"]
SOLO_PRIMO = "--solo-primo" in sys.argv

# --------------------------------------------------------------- i flag, col percorso UFFICIALE
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "8",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]
import soliton_simulator as S

_a = S._cli()
S._applica_regime(_a)
S._applica_flag(_a)


def passo_di(p):
    return int(re.search(r"_(\d{6})\.", p).group(1))


def verifica_flag():
    """P6: i flag del MODULO contro i 20 che il run stesso ha scritto in prog.csv. Se uno solo
    differisce si ferma: il disegno dipende da SCHERMATURA/CAMPO_SPINORIALE/GAMMA/LAM."""
    if not os.path.exists(PROG):
        return ["prog.csv ASSENTE: i flag del run non sono verificabili"]
    testa = []
    with open(PROG, "r", encoding="utf-8", errors="replace") as f:
        for r in f:
            if r.startswith("#"):
                testa.append(r.strip())
            else:
                break
    guai = []
    attesi = {}
    for r in testa:
        for tok in r.lstrip("# ").split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                attesi[k] = v
    print("  i 20 flag scritti dal RUN, contro quelli del MODULO adesso:")
    for k, v in sorted(attesi.items()):
        if k in ("blob", "seme_effettivo", "nmasse", "sep"):
            continue
        ora = getattr(S, k, "ASSENTE")
        if isinstance(ora, bool):
            ok = (str(int(ora)) == v)
            mostra = str(int(ora))
        else:
            try:
                ok = abs(float(ora) - float(v)) <= 1e-12
            except Exception:
                ok = (str(ora) == v)
            mostra = str(ora)
        print("    %-22s run=%-8s modulo=%-8s %s" % (k, v, mostra, "" if ok else "*** DIVERSO ***"))
        if not ok:
            guai.append("%s: run=%s modulo=%s" % (k, v, mostra))
    return guai


def carica_override(path):
    """La logica di carica_stato MENO la verifica del blob. DICHIARATA, non silenziosa."""
    _ap = gzip.open if str(path).endswith(".gz") else open
    with _ap(path, "rb") as fh:
        st = pickle.load(fh)
    for k, v in st["attrs"].items():
        setattr(S.net, k, v)
    S.net.rng.bit_generator.state = st["rng_state"]
    S.net._S = None
    if hasattr(S.net, "_perm"):
        S.net._perm = None
    if hasattr(S.net, "_ker_cache"):
        S.net._ker_cache = {}
    return str(st.get("blob"))[:8]


def componenti(n, i, j, deg_sal):
    """Stessa costruzione del referto (simmetrizzata, niente auto-anelli) e STESSO presidio P0."""
    A = sp.coo_matrix((np.ones(len(i), np.float32), (i, j)), shape=(n, n)).tocsr()
    A = ((A + A.T) > 0).astype(np.float32)
    A.setdiag(0)
    A.eliminate_zeros()
    deg = np.asarray(A.sum(1)).ravel().astype(np.int64)
    p0 = int(np.sum(deg != deg_sal[:n])) if deg_sal is not None and len(deg_sal) >= n else -1
    nc, lab = connected_components(A, directed=False)
    dim = np.bincount(lab)
    ancore = [int(np.flatnonzero(lab == c).min()) for c in range(nc)]
    ordine = np.argsort(ancore)
    rimappa = np.zeros(nc, int)
    for nuovo, vecchio in enumerate(ordine):
        rimappa[vecchio] = nuovo
    lab = rimappa[lab]
    dim = dim[ordine]
    ancore = [ancore[k] for k in ordine]
    # archi fra componenti diverse: deve restare 0
    fra = int(np.sum(lab[i] != lab[j]))
    return lab, dim, ancore, fra, p0, deg


def disegna(fr, passo, lab, dim, ancore, fra, p0, R, vmax_mem, nfr_tot):
    n = int(S.net.n)
    campo, Rc, massa3d = S.net.campo_spaziale(mezzo=R, M=None)
    picco = float(np.percentile(np.abs(campo), 99)) if campo.size else 1.0
    picco = max(picco, 1e-9)
    # la ricetta di colore della GUI: sale subito (0.5), scende piano (0.02), ancorata all'inizio
    if fr <= 25:
        vmax_mem = max(vmax_mem or 0.0, picco)
    else:
        v = vmax_mem or picco
        vmax_mem = v + (0.5 if picco > v else 0.02) * (picco - v)
    vm = max(vmax_mem or 1.0, 1e-9)
    q = np.clip(campo.T / vm, -1, 1)
    contrasto = float(np.abs(q).mean()) if q.size else 0.3
    gr = float(np.clip(0.30 + 0.5 * contrasto, 0.30, 0.60))
    q = np.sign(q) * np.abs(q) ** gr
    rgba = S.CMAP_INTERF((q + 1) / 2)
    soglia = float(np.clip(0.06 + 0.30 * contrasto, 0.06, 0.30))
    rgba[..., 3] = np.clip((np.abs(q) - soglia) / max(1.0 - soglia, 1e-6), 0.0, 1.0)

    fig = plt.figure(figsize=(16, 8.4), facecolor="#0b0b0f")
    ax1 = fig.add_axes([0.005, 0.045, 0.49, 0.90])
    ax1.set_facecolor("#000000")
    ax1.imshow(rgba, origin="lower", extent=[-Rc, Rc, -Rc, Rc], interpolation="bilinear")
    ax1.set_xlim(-Rc, Rc)
    ax1.set_ylim(-Rc, Rc)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("IL CAMPO -- la sola interferenza (fondo incoerente sottratto)\n"
                  "fuoco = materia  ·  ciano = distruzione  ·  nero = nulla",
                  fontsize=10, color="#cfcfd6")

    # ---- pannello destro: il GRAFO, colore = componente, luminosita' = pozzo phi_g
    ax2 = fig.add_axes([0.505, 0.045, 0.49, 0.90])
    ax2.set_facecolor("#000000")
    Iv = S.net.intensita()[:n]
    phi_g, _m, _p = S.net.pozzo_grafo(Iv)
    lg = np.log10(np.maximum(phi_g[:n], 1e-12))
    lo, hi = np.percentile(lg, 2), np.percentile(lg, 98)
    alpha = np.clip((lg - lo) / max(hi - lo, 1e-9), 0.0, 1.0) * 0.85 + 0.15
    P = S.net.pos[:n]
    for c in range(len(dim)):
        m = (lab == c)
        if not m.any():
            continue
        col = matplotlib.colors.to_rgb(COLORI[c % len(COLORI)])
        # UN solo scatter, con alpha PER PUNTO: il colore dice la componente, la
        # trasparenza dice il pozzo. Due scatter sovrapposti falserebbero la luminosita'.
        rgba_n = np.tile(np.array(col + (1.0,)), (int(m.sum()), 1))
        rgba_n[:, 3] = alpha[m]
        ax2.scatter(P[m, 0], P[m, 1], s=3.0, c=rgba_n, linewidths=0,
                    edgecolors="none", rasterized=True)
    ax2.set_xlim(-Rc, Rc)
    ax2.set_ylim(-Rc, Rc)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("IL GRAFO -- un colore per COMPONENTE CONNESSA\n"
                  "(luminosita' dal pozzo phi_g di pozzo_grafo())", fontsize=10, color="#cfcfd6")

    testo = ("passo %-6d  (frame %d/%d)    n = %-7d archi = %-8d\n"
             "componenti: %d    taglie: %s\n"
             "ARCHI FRA COMPONENTI DIVERSE: %d        [P0: deg != _deg su %d nodi]"
             % (passo, fr, nfr_tot, n, len(S.net.i), len(dim),
                " / ".join(str(int(x)) for x in dim), fra, p0))
    fig.text(0.5, 0.012, testo, ha="center", va="bottom", fontsize=11,
             color="#ffffff" if fra == 0 else "#ff4444", family="monospace")
    fig.text(0.5, 0.975,
             "RIGENERATO DAGLI SNAPSHOT -- nessuna fisica eseguita.  stati blob 7c4dec1d, "
             "disegno blob 775ceab7 (funzioni di rendering IDENTICHE).  "
             "cadenza 60 passi/frame contro i 6 dell'originale: dieci volte piu' a scatti.",
             ha="center", va="top", fontsize=8.5, color="#8a8a93")
    out = os.path.join(DEST, "frame_%03d.png" % fr)
    fig.savefig(out, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    return out, vmax_mem


def main():
    os.makedirs(DEST, exist_ok=True)          # NON si cancella: Z31
    print("=" * 112)
    print("IL VIDEO DAGLI SNAPSHOT -- si legge e si disegna. NESSUNA FISICA.")
    print("=" * 112)
    guai = verifica_flag()
    if guai:
        print("\n  *** I FLAG NON COMBACIANO COL RUN: mi fermo. ***")
        for g in guai:
            print("      " + g)
        return 2
    print("  -> i flag del modulo combaciano con quelli scritti dal run. (P6)")

    fs = sorted(glob.glob(os.path.join(ARCHIVIO, "scena_??????.pkl*")))
    if not fs:
        print("nessuno snapshot in %s" % ARCHIVIO)
        return 1
    passi = [passo_di(p) for p in fs]
    print("\n  %d snapshot, passi %d -> %d (cadenza %d)"
          % (len(fs), passi[0], passi[-1], passi[1] - passi[0]))

    # ---- pre-passata: l'inquadratura FISSA. La serie si STAMPA, non si assume monotona.
    print("\n  PRE-PASSATA: max|pos| per snapshot (l'inquadratura e' FISSA per tutti i frame)")
    t0 = time.time()
    est = []
    for p, passo in zip(fs, passi):
        _ap = gzip.open if p.endswith(".gz") else open
        with _ap(p, "rb") as fh:
            at = pickle.load(fh)["attrs"]
        pos = np.asarray(at["pos"])[:len(at["eta"])]
        est.append(float(np.abs(pos).max()))
        del at, pos
    for k in range(0, len(est), 5):
        print("     " + "  ".join("%d:%.2f" % (passi[q], est[q])
                                  for q in range(k, min(k + 5, len(est)))))
    RFISSO = max(est) * 1.12 + 1e-6
    mono = all(est[k + 1] >= est[k] - 1e-9 for k in range(len(est) - 1))
    print("     -> max|pos| %.2f -> %.2f, monotona crescente: %s;  R FISSO = %.3f   [%.1f s]"
          % (est[0], est[-1], "SI" if mono else "NO", RFISSO, time.time() - t0))

    # ---- i frame
    print("\n  I FRAME")
    vmax_mem = None
    ancore0 = None
    t_primo = None
    for k, (p, passo) in enumerate(zip(fs, passi)):
        fr = k + 1
        t1 = time.time()
        bs = carica_override(p)
        n = int(S.net.n)
        i = np.asarray(S.net.i)
        j = np.asarray(S.net.j)
        lab, dim, ancore, fra, p0, deg = componenti(n, i, j, getattr(S.net, "_deg", None))
        if ancore0 is None:
            ancore0 = list(ancore)
            print("     indici-ancora delle componenti (criterio del colore): %s" % ancore0)
        elif ancore != ancore0:
            print("     *** frame %d: gli indici-ancora sono CAMBIATI: %s contro %s. "
                  "Riporto e NON ricoloro in silenzio. ***" % (fr, ancore, ancore0))
        if len(dim) != 4:
            print("     *** frame %d: le componenti sono %d, non 4. ***" % (fr, len(dim)))
        try:
            out, vmax_mem = disegna(fr, passo, lab, dim, ancore, fra, p0, RFISSO,
                                    vmax_mem, len(fs))
        except AttributeError as e:
            print("\n  *** IL DISEGNO CHIEDE UNA GRANDEZZA CHE NON E' NELLO SNAPSHOT: %s ***" % e)
            print("  Mi fermo e la riporto, invece di ricalcolarla.")
            return 3
        dt = time.time() - t1
        if t_primo is None:
            t_primo = dt
        print("     frame %-3d passo %-6d n=%-7d comp=%d taglie=%-28s fra=%d  blob=%s  [%.2f s]"
              % (fr, passo, n, len(dim), "/".join(str(int(x)) for x in dim), fra, bs, dt))
        if SOLO_PRIMO:
            print("\n  --solo-primo: mi fermo dopo il primo frame. COSTO = %.2f s/frame,"
                  " stima per %d frame = %.0f s." % (t_primo, len(fs), t_primo * len(fs)))
            print("  -> %s" % out)
            return 0

    # ---- il video
    print("\n  COMPOSIZIONE (ffmpeg, %d fps -> %.1f s di video)" % (FPS, len(fs) / FPS))
    mp4 = os.path.join(DEST, "video_g6000.mp4")
    cmd = ["ffmpeg", "-y", "-framerate", str(FPS),
           "-i", os.path.join(DEST, "frame_%03d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", mp4]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("     *** ffmpeg FALLITO (rc=%d) ***" % r.returncode)
        print(r.stderr[-1500:])
        return 4
    print("     -> %s  (%.1f MB)" % (mp4, os.path.getsize(mp4) / 1e6))
    print("\n  E' UN'ISPEZIONE: nessun numero di qui entra in un referto come risultato.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
