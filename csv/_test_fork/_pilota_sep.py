# -*- coding: utf-8 -*-
"""IL PILOTA CHE DECIDE `sep` -- le tre masse si parlano, o no?

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_run-masse-interagenti.md (eb94a48).

NON tocca il simulatore ne' il driver: e' uno script a parte, perche' `_scena_video.py` ha
`--sep 8` CABLATO nel suo sys.argv e il pilota deve poter variare `sep`.

LA GEOMETRIA, MISURATA e non assunta (vedi task history): `sep` e' il RAGGIO DEL CERCHIO, non la
distanza fra le masse. Con nm=3 la distanza fra due masse e' sep*sqrt(3), e fra i BORDI
1.7321*sep - 2r. Col vecchio sep=8 i bordi stavano a 12.44 contro un rc <= 2.4.

COSA MISURA, a piu' istanti:
  1  median(lambda_nodi()) e quindi rc VERO = 3*median, con la sua TRAIETTORIA;
  2  numero di COMPONENTI CONNESSE e taglie;
  3  ARCHI FRA COMPONENTI DIVERSE, e separatamente MASSA-MASSA contro MASSA-VUOTO;
  4  DURATA per 100 passi e dimensione del primo snapshot compresso;
  5  n.

LA QUINTA CASELLA, che il mandato non aveva: il vuoto e' una sfera di raggio ~4, quindi con sep
piccolo le masse ci finiscono DENTRO e le componenti possono unirsi ATTRAVERSO IL VUOTO senza che
due masse si tocchino mai. Un solo numero non distingue i due casi: si contano separati.

COME SI CLASSIFICANO GLI ARCHI, ed e' esatto: solo i nodi SEMINATI hanno un gruppo certo
(vuoto = i primi SEME_INIZIALE, masse = le coorti registrate da `_massa`). I nodi NATI DOPO non
hanno lignaggio ricostruibile qui, quindi gli archi che li toccano si contano A PARTE invece di
attribuirli. Alla semina la classificazione e' completa per costruzione.

IL PILOTA NON E' IL RUN: i suoi numeri servono a scegliere `sep`, non entrano in un referto.
ASCII PURO.
"""
import os
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))

SEP = "1.8"
PASSI = 300
OGNI = 5          # ogni quanti FRAME si misura
# --solo-semina: misura la SEMINA e basta, senza i 300 passi e senza la fermata sulla lettura C.
# Serve per SCANSIONARE sep: la domanda "a quale sep le masse si toccano" si decide alla semina,
# perche' e' li' che `_allaccia` collega, e spendere 300 passi per ogni valore sarebbe sprecato.
SOLO_SEMINA = "--solo-semina" in sys.argv
DEST = None
for _x in sys.argv[1:]:
    if _x.startswith("--sep="):
        SEP = _x.split("=", 1)[1]
    elif _x.startswith("--passi="):
        PASSI = int(_x.split("=", 1)[1])
    elif _x.startswith("--ogni="):
        OGNI = int(_x.split("=", 1)[1])
    elif _x.startswith("--dest="):
        DEST = _x.split("=", 1)[1]
if DEST is None:
    DEST = os.path.join(RADICE, "csv", "_test_fork", "_pilota_sep_%s" % SEP.replace(".", "p"))

# ------------------------------------------------- gli STESSI flag del driver, percorso UFFICIALE
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", SEP,
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]
sys.path.insert(0, RADICE)
os.chdir(RADICE)
import soliton_simulator as S

_a = S._cli()
S._applica_regime(_a)
S._applica_flag(_a)
S._NMASSE_VIDEO["n"] = max(2, int(getattr(_a, "nmasse", 3)))
S._NMASSE_VIDEO["sep"] = float(getattr(_a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None


def adiacenza():
    n = int(S.net.n)
    i = np.asarray(S.net.i)
    j = np.asarray(S.net.j)
    A = sp.coo_matrix((np.ones(len(i), np.float32), (i, j)), shape=(n, n)).tocsr()
    A = ((A + A.T) > 0).astype(np.float32)
    A.setdiag(0)
    A.eliminate_zeros()
    return n, i, j, A


MISTO = 4     # etichetta dei nodi nati da un arco fra due gruppi DIVERSI


def propaga(n, A, gruppo, n_sem):
    """Il LIGNAGGIO dei nodi nati dopo la semina, e dichiaro come.

    `conc_nodi` e' VUOTO in questa scena (verificato: `semina()` registra la concorrenza solo se
    `mass_id is not None`, e `_massa()` non lo passa), quindi la via del mandato non esiste.
    Ma un nodo nasce al PUNTO MEDIO di un arco, con esattamente due archi verso i due genitori,
    ENTRAMBI DI INDICE MINORE (CLAUDE.md par.9): una sola passata in ordine di indice basta.

    Se i due genitori hanno etichette DIVERSE il nodo e' MISTO e si conta A PARTE. Non se ne
    sceglie una: un nodo nato da un arco massa-vuoto non appartiene a nessuna delle due, e
    attribuirlo gonfierebbe proprio il numero che decide."""
    g = np.full(n, -1, np.int64)
    m = min(n_sem, n)
    g[:m] = gruppo[:m]
    ip, ix = A.indptr, A.indices
    for k in range(m, n):
        vic = ix[ip[k]:ip[k + 1]]
        et = set(int(x) for x in np.unique(g[vic[vic < k]]) if x >= 0)
        if len(et) == 1:
            g[k] = et.pop()
        elif len(et) > 1:
            g[k] = MISTO
    return g


def misura(gruppo, n_sem):
    n, i, j, A = adiacenza()
    nc, lab = connected_components(A, directed=False)
    dim = np.sort(np.bincount(lab))[::-1]
    fra = int(np.sum(lab[i] != lab[j]))
    g = propaga(n, A, gruppo, n_sem)
    gi, gj = g[i], g[j]
    massa_i = (gi >= 1) & (gi <= 3)
    massa_j = (gj >= 1) & (gj <= 3)
    mm = int(np.sum(massa_i & massa_j & (gi != gj)))                    # massa A - massa B
    mv = int(np.sum((massa_i & (gj == 0)) | (massa_j & (gi == 0))))     # massa - vuoto
    mis = int(np.sum((gi == MISTO) | (gj == MISTO)))                    # tocca un MISTO
    senza = int(np.sum((gi < 0) | (gj < 0)))                            # non etichettabile
    li = S.net.lambda_nodi()
    rc = 3.0 * float(np.median(li))
    return dict(n=n, archi=len(i), nc=nc, dim=dim, fra=fra, mm=mm, mv=mv, nuovi=mis,
                n_misto=int(np.sum(g == MISTO)), senza=senza,
                lam_med=float(np.median(li)), lam_min=float(li.min()), lam_max=float(li.max()),
                rc=rc)


def riga(et, m):
    print("%-11s n=%-6d archi=%-8d comp=%-3d | mm=%-7d mv=%-8d | archi_misti=%-8d "
          "nodi_misti=%-6d senza=%-5d | lam_med=%.4f rc=%.4f"
          % (et, m["n"], m["archi"], m["nc"], m["mm"], m["mv"], m["nuovi"],
             m["n_misto"], m["senza"], m["lam_med"], m["rc"]))


def main():
    os.makedirs(DEST, exist_ok=True)          # NON si cancella: Z31
    sep = float(SEP)
    r = 0.7
    print("=" * 130)
    print("PILOTA sep=%s   %d passi   (%d frame x %d passi)" % (SEP, PASSI, PASSI // int(S.PASSI_PER_FRAME), int(S.PASSI_PER_FRAME)))
    print("=" * 130)
    print("  LAM = %s   R_CONN() = 3*LAM = %.4f   (il rc usato SOLO quando non ci sono ancora archi)"
          % (S.LAM, S.R_CONN()))
    print("  GEOMETRIA ATTESA (sep e' il RAGGIO DEL CERCHIO, non la distanza):")
    print("     distanza fra i CENTRI = sep*sqrt(3) = %.4f      fra i BORDI = %.4f"
          % (sep * np.sqrt(3), sep * np.sqrt(3) - 2 * r))
    print("     massa-vuoto: centri = sep = %.4f" % sep)
    print("")

    S.avvia_test("N-MASSE")()      # il costruttore UFFICIALE della scena
    n_sem = int(S.net.n)
    coorti = S.test["dati"].get("coorti", {})
    gruppo = np.zeros(n_sem, np.int64)          # 0 = vuoto (i primi SEME_INIZIALE)
    for k in range(S._n_masse_video()):
        idx = coorti.get("massa_%d" % k)
        if idx is not None:
            gruppo[np.asarray(idx)] = k + 1
    print("  SEMINA: n = %d   vuoto = %d   masse = %s"
          % (n_sem, int(np.sum(gruppo == 0)),
             " / ".join(str(int(np.sum(gruppo == k + 1))) for k in range(S._n_masse_video()))))
    # la geometria VERA, misurata
    P = S.net.pos[:n_sem]
    cen = {}
    for k in range(S._n_masse_video() + 1):
        m = (gruppo == k)
        if m.any():
            c = P[m].mean(0)
            rr = float(np.percentile(np.linalg.norm(P[m] - c, axis=1), 95))
            cen[k] = (c, rr)
            print("     gruppo %d  n=%-5d centro=[%7.3f %7.3f %7.3f]  raggio p95=%.3f"
                  % (k, int(m.sum()), c[0], c[1], c[2], rr))
    print("     DISTANZE MISURATE fra i bordi:")
    for a in sorted(cen):
        for b in sorted(cen):
            if b <= a:
                continue
            d = float(np.linalg.norm(cen[a][0] - cen[b][0]))
            print("        gruppo %d - gruppo %d : centri %7.3f   bordi %8.3f" % (a, b, d, d - cen[a][1] - cen[b][1]))
    print("")

    m0 = misura(gruppo, n_sem)
    riga("SEMINA", m0)
    if SOLO_SEMINA:
        print("SCAN sep=%s nc=%d mm=%d mv=%d bordi_mm=%.4f bordi_mv=%.4f rc=%.4f n=%d archi=%d"
              % (SEP, m0["nc"], m0["mm"], m0["mv"], sep * np.sqrt(3) - 2 * r,
                 sep - cen[0][1] - cen[1][1] if 0 in cen and 1 in cen else float("nan"),
                 m0["rc"], m0["n"], m0["archi"]))
        return 0
    if m0["nc"] == 1:
        print("\n  *** LETTURA C: UNA SOLA COMPONENTE GIA' ALLA SEMINA -- le masse si sono")
        print("      COMPENETRATE. Non sono tre masse, e' un blocco solo. sep TROPPO PICCOLO.")
        print("      Mi fermo: si risale.")
        return 3
    print("")

    nframe = max(1, PASSI // int(S.PASSI_PER_FRAME))
    S.stato["nframe"] = 0
    t0 = time.time()
    t_100 = None
    storia = [(0, m0)]
    for k in range(nframe):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(S.net)
            S.net.step()
            S.net.mitosi()
            S.net.rilassa_disegno()
            S.net.memoria_hebbiana_moto()
        S.stato["nframe"] += 1
        fr = k + 1
        passo = fr * int(S.PASSI_PER_FRAME)
        if passo >= 100 and t_100 is None:
            t_100 = (time.time() - t0) * 100.0 / passo
        if fr % OGNI == 0 or fr == nframe:
            m = misura(gruppo, n_sem)
            storia.append((passo, m))
            riga("passo %d" % passo, m)

    el = time.time() - t0
    print("")
    print("  DURATA: %.1f s per %d passi  ->  %.2f s/100 passi  (misurato a 100: %.2f s/100)"
          % (el, nframe * int(S.PASSI_PER_FRAME),
             100.0 * el / max(nframe * int(S.PASSI_PER_FRAME), 1), t_100 or float("nan")))

    # ---- lo SNAPSHOT: quanto pesa compresso
    sp_path = os.path.join(DEST, "pilota_%06d.pkl.gz" % (nframe * int(S.PASSI_PER_FRAME)))
    S.net._db_step = nframe * int(S.PASSI_PER_FRAME)
    ts = time.time()
    S.net.salva_stato(sp_path)
    dts = time.time() - ts
    mb = os.path.getsize(sp_path) / 1e6
    print("  SNAPSHOT: %.2f MB in %.1f s  (n = %d)  ->  %s" % (mb, dts, S.net.n, os.path.basename(sp_path)))

    # ---- il VERDETTO secondo le letture fissate prima
    print("")
    print("=" * 130)
    print("IL VERDETTO, secondo le letture fissate PRIMA")
    print("=" * 130)
    print("  traiettoria di rc:   " + "  ".join("%d:%.3f" % (p, m["rc"]) for p, m in storia))
    print("  traiettoria di comp: " + "  ".join("%d:%d" % (p, m["nc"]) for p, m in storia))
    print("  traiettoria di mm:   " + "  ".join("%d:%d" % (p, m["mm"]) for p, m in storia))
    ncs = [m["nc"] for _, m in storia]
    mms = [m["mm"] for _, m in storia]
    fine = storia[-1][1]
    if min(ncs) < 4 and max(ncs[ncs.index(min(ncs)):]) > min(ncs):
        print("  -> LETTURA D: le componenti si sono FUSE e poi RISEPARATE. E' un fenomeno, non un")
        print("     errore di setup. Si riporta.")
    elif fine["nc"] < 4 and fine["mm"] > 0:
        print("  -> LETTURA A: componenti %d < 4 e archi MASSA-MASSA = %d > 0."
              % (fine["nc"], fine["mm"]))
        print("     LE MASSE SI PARLANO DIRETTAMENTE. Si procede con sep = %s." % SEP)
    elif fine["nc"] < 4 and fine["mm"] == 0:
        print("  -> QUINTA CASELLA: componenti %d < 4 MA archi massa-massa = 0 (massa-vuoto = %d)."
              % (fine["nc"], fine["mv"]))
        print("     LE MASSE NON SI PARLANO FRA LORO: parlano col VUOTO, che parla con tutti.")
        print("     Si riporta a Luca PRIMA di lanciare: e' una scena diversa da quella descritta.")
    elif fine["nc"] == 4:
        print("  -> LETTURA B: le componenti sono ancora 4. sep = %s e' ANCORA TROPPO GRANDE."
              % SEP)
        print("     I bordi massa-massa stanno a %.3f contro rc = %.3f."
              % (sep * np.sqrt(3) - 2 * r, fine["rc"]))
        print("     Si riprova piu' stretto: serve sep < (rc + 1.4)/sqrt(3) = %.3f."
              % ((fine["rc"] + 1.4) / np.sqrt(3)))
    else:
        print("  -> nessuna delle caselle: componenti %d, mm %d, mv %d. Si riporta cosi'."
              % (fine["nc"], fine["mm"], fine["mv"]))
    print("")
    print("  IL PILOTA NON E' IL RUN: questi numeri scelgono sep, non entrano in un referto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
