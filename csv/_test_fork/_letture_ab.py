# -*- coding: utf-8 -*-
"""LE LETTURE DEL MANDATO par.4 sui DUE ARCHIVI A/B, agli STESSI passi.

Le letture sono FISSATE PRIMA in `doc/TASK_HISTORY/2026-09-20_due-run-ab-sep4.md` (`bb1d727`,
par.2.4), committato PRIMA del lancio dei run. Questo script le APPLICA, non le sceglie.

*** DUE FASI, E LA DIVISIONE NON E' DI COMODO ***

  FASE RAPIDA (default) -- NON IMPORTA IL SIMULATORE. Legge i `.pkl.gz` come pickle e basta.
    Tutto cio' che serve e' gia' un ARRAY nello snapshot, verificato dal disco:
    `perc_chi`, `tw`, `omega_s`, `_deg`, `i`, `j`, `pos`, `mem_mot`, e i quattro contatori di
    nascita (sono `int`, e il filtro di `salva_stato` a `:3063` accetta `int`).
    **E' la fase che si puo' girare MENTRE i run girano**, perche' non tocca niente e non importa
    nessun modulo che i due processi abbiano caricato. Ci sta dentro **il presidio di `Z65`**:
    le COMPONENTI CONNESSE a ogni snapshot, che vanno sapute SUBITO e non alla fine.

  FASE LENTA (`--olonomia`) -- importa il simulatore e ricostruisce una `Rete` per snapshot con
    `carica_stato`, perche' `olonomia_media`, `berry_spin_media` e `coer_l` **non sono nello
    snapshot**: sono CALCOLATE da `circolazione_topologica()` e `diagnostica()`.
    **Si gira a run FINITI**, non durante: costa, e competerebbe per la CPU.

*** ⚠ L'ORDINE DELLE DUE CHIAMATE NON E' INDIFFERENTE, ED E' UN ERRORE GIA' FATTO ***
  Nella fase lenta `diagnostica()` si chiama **PRIMA** di `circolazione_topologica()`.
  Chiamandole nell'ordine opposto, `coer_l`/`coer_g`/`dil` tornano **`nan`** -- e' successo nell'A/B
  corto del 2026-09-20, e i tre `nan` erano un artefatto del mio ordine di chiamata, non una
  proprieta' del sistema. Qui l'ordine e' cablato, e questo commento dice perche'.

*** COSA QUESTO SCRIPT NON FA, e si scrive qui invece che nelle conclusioni ***
  Non dichiara significativa nessuna differenza fra A e B. **UN SEME PER RAMO**: su questo sistema
  il nullo di un confronto fra bracci non e' zero, e' la dispersione FRA SEMI (par.9), che questo
  esperimento **non misura**. Lo script stampa i numeri e il loro ANDAMENTO nel tempo; la lettura
  sta nel task history, e la decisione e' di Luca.

USO:  python _letture_ab.py [--olonomia] [--ogni=K] [--A=dir] [--B=dir]
ASCII PURO.
"""
import glob
import gzip
import os
import pickle
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DIR_A = os.path.join(RADICE, "csv", "_test_fork", "_ab_A")
DIR_B = os.path.join(RADICE, "csv", "_test_fork", "_ab_B")
OLON = False
OGNI = 1
for _x in sys.argv[1:]:
    if _x == "--olonomia":
        OLON = True
    elif _x.startswith("--ogni="):
        OGNI = int(_x.split("=", 1)[1])
    elif _x.startswith("--A="):
        DIR_A = os.path.abspath(_x.split("=", 1)[1])
    elif _x.startswith("--B="):
        DIR_B = os.path.abspath(_x.split("=", 1)[1])


def serie(d):
    fs = sorted(glob.glob(os.path.join(d, "scena_??????.pkl*")))
    return [(int(re.search(r"_(\d{6})\.", p).group(1)), p) for p in fs]


def attrs(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)["attrs"]


def pct(a, q):
    a = np.asarray(a)
    return float(np.percentile(a, q)) if a.size else float("nan")


def componenti(a):
    """Il presidio di `Z65`. Numero di componenti connesse, e taglia della piu' grande.

    ⚠ Si contano le componenti del grafo sui `n` nodi VIVI, e i nodi ISOLATI contano come
    componenti a se': un nodo che perde tutti gli archi E' scollegato, e nasconderlo dietro
    'componenti fra i soli nodi con archi' sarebbe misurare un grafo diverso da quello che gira.
    """
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    n = len(a["phi"])
    ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
    m = (ii < n) & (jj < n)
    ii, jj = ii[m], jj[m]
    g = coo_matrix((np.ones(len(ii)), (ii, jj)), shape=(n, n))
    nc, lab = connected_components(g, directed=False)
    tg = np.bincount(lab)
    return nc, int(tg.max()), int(np.sum(tg == 1))


def rapido(p):
    a = attrs(p)
    n = len(a["phi"])
    pc = np.asarray(a["perc_chi"])[:n]
    np1 = int(np.sum(pc > 0)); nm1 = int(np.sum(pc < 0)); nz = int(np.sum(pc == 0))
    tw = np.abs(np.asarray(a["tw"]))
    twn = np.zeros(n)
    ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
    mk = (ii < n) & (jj < n)
    np.add.at(twn, ii[mk], tw[mk]); np.add.at(twn, jj[mk], tw[mk])
    twn = twn / np.maximum(np.asarray(a["_deg"])[:n], 1)
    om = np.linalg.norm(np.asarray(a["omega_s"])[:n], axis=1)
    P = np.asarray(a["pos"])[:n]
    M = np.asarray(a.get("mem_mot", np.zeros_like(P)))[:n]
    L = np.cross(P - P.mean(axis=0), M).sum(axis=0) if len(P) == len(M) else np.zeros(3)
    nc, tgmax, iso = componenti(a)
    return dict(
        passo=int(a.get("_db_step", -1)), n=n, archi=int(len(ii)),
        nati_mit=int(a.get("_g_nati_mitosi", 0)), ev_mit=int(a.get("_g_nati_mitosi_ev", 0)),
        nati_sch=int(a.get("_g_nati_schwinger", 0)), ev_sch=int(a.get("_g_nati_schwinger_ev", 0)),
        Np1=np1, Nm1=nm1, Nz=nz, diff=np1 - nm1,
        comp=nc, comp_max=tgmax, isolati=iso,
        tw50=pct(tw, 50), tw95=pct(tw, 95), twn50=pct(twn, 50), twn95=pct(twn, 95),
        om50=pct(om, 50), om95=pct(om, 95), deg50=pct(np.asarray(a["_deg"])[:n], 50),
        Lx=float(L[0]), Ly=float(L[1]), Lz=float(L[2]), Lmod=float(np.linalg.norm(L)))


def lento(p):
    """olonomia FIRMATA, berry, e `coer_l`. IMPORTA IL SIMULATORE: si gira a run FINITI."""
    import soliton_simulator as S
    net = S.Rete()
    net.carica_stato(p)
    # ⚠ `diagnostica()` PRIMA: nell'ordine opposto `coer_l`/`coer_g`/`dil` tornano `nan`.
    dg = net.diagnostica()
    c = net.circolazione_topologica()
    return dict(coer_l=float(dg.get("coer_l", float("nan"))),
                coer_g=float(dg.get("coer_g", float("nan"))),
                dil=float(dg.get("dil", float("nan"))),
                n_cicli=int(c.get("n_cicli", 0)),
                olon_media=float(c.get("olonomia_media", float("nan"))),
                olon_ass=float(c.get("olonomia_media_assoluta", float("nan"))),
                olon_rms=float(c.get("olonomia_rms", float("nan"))),
                olon_max=float(c.get("olonomia_max", float("nan"))),
                circ_media=float(c.get("circolazione_media", float("nan"))),
                berry=float(c.get("berry_spin_media", float("nan"))),
                berry_segno=float(c.get("berry_segno_media", float("nan"))))


def main():
    sA, sB = serie(DIR_A), serie(DIR_B)
    print("=" * 118)
    print("LE LETTURE DEL par.4 -- A = chi_basc ON (default) | B = chi_basc OFF")
    print("  A: %-52s %d snapshot" % (os.path.relpath(DIR_A, RADICE), len(sA)))
    print("  B: %-52s %d snapshot" % (os.path.relpath(DIR_B, RADICE), len(sB)))
    print("=" * 118)
    pA = {p: q for p, q in sA}
    pB = {p: q for p, q in sB}
    com = sorted(set(pA) & set(pB))
    sol_A = sorted(set(pA) - set(pB))
    sol_B = sorted(set(pB) - set(pA))
    if sol_A or sol_B:
        print("  ⚠ passi NON in comune -- solo A: %s | solo B: %s" % (sol_A[-3:], sol_B[-3:]))
    com = com[::OGNI]
    if not com:
        print("  nessun passo in comune: i due archivi non sono ancora confrontabili.")
        return 1

    # ------------------------------------------------ 6) IL PRESIDIO DI Z65, per primo
    print("")
    print("--- par.4.6  COMPONENTI CONNESSE a ogni snapshot (presidio Z65) ---")
    print("  %-8s | %-28s | %-28s" % ("passo", "A: comp / max / isolati", "B: comp / max / isolati"))
    rot = {}
    guai = []
    for p in com:
        ra, rb = rapido(pA[p]), rapido(pB[p])
        rot[p] = (ra, rb)
        print("  %-8d | %6d / %8d / %6d   | %6d / %8d / %6d"
              % (p, ra["comp"], ra["comp_max"], ra["isolati"],
                 rb["comp"], rb["comp_max"], rb["isolati"]))
        if ra["comp"] != 1 or rb["comp"] != 1:
            guai.append((p, ra["comp"], rb["comp"]))
    if guai:
        print("  *** ⚠ IL GRAFO SI E' SCOLLEGATO: %s ***" % guai[:5])
        print("  *** Da quel passo in poi il run misura masse che NON interagiscono (Z65). ***")
    else:
        print("  UNA SOLA COMPONENTE in tutti i %d passi confrontati, in ENTRAMBI i rami." % len(com))

    # ------------------------------------------------ 1) i NATI PER RAMO
    print("")
    print("--- par.4.1  I NATI PER RAMO -- :4294 eredita UGUALE, :4415 antinodo OPPOSTO ---")
    print("  %-8s | %-32s | %-32s" % ("passo", "A: mit(ev) / schw(ev) / n", "B: mit(ev) / schw(ev) / n"))
    for p in com:
        ra, rb = rot[p]
        print("  %-8d | %7d(%4d) /%6d(%4d) /%6d | %7d(%4d) /%6d(%4d) /%6d"
              % (p, ra["nati_mit"], ra["ev_mit"], ra["nati_sch"], ra["ev_sch"], ra["n"],
                 rb["nati_mit"], rb["ev_mit"], rb["nati_sch"], rb["ev_sch"], rb["n"]))

    # ------------------------------------------------ 2) LA CARICA, e Z71
    print("")
    print("--- par.4.2  N(+1), N(-1), DIFFERENZA -- in B deve muoversi SOLO per nascite (Z71) ---")
    print("  %-8s | %-30s | %-30s | %s" % ("passo", "A: Np1 / Nm1 / diff", "B: Np1 / Nm1 / diff",
                                           "B: diff attesa da :4294"))
    for p in com:
        ra, rb = rot[p]
        # ATTESA: ogni nato da `:4294` eredita il segno del genitore e sposta `diff` di +-1; ogni
        # coppia di `:4415` nasce OPPOSTA e la lascia INVARIATA. Quindi |diff| <= |diff_semina| +
        # nati_mitosi e' un LIMITE, non una previsione puntuale: il segno dei genitori non si sa.
        print("  %-8d | %8d /%8d /%8d | %8d /%8d /%8d | |diff| <= %d + semina"
              % (p, ra["Np1"], ra["Nm1"], ra["diff"], rb["Np1"], rb["Nm1"], rb["diff"],
                 rb["nati_mit"]))

    # ------------------------------------------------ 5) i PERCENTILI
    print("")
    print("--- par.4.5  PERCENTILI -- ⚠ `tw` si riporta ma NON regge una conclusione (Z70) ---")
    print("  %-8s | %-38s | %-38s" % ("passo", "A: tw50 twn50 om50 deg50", "B: tw50 twn50 om50 deg50"))
    for p in com:
        ra, rb = rot[p]
        print("  %-8d | %9.4g %9.4g %9.4g %6.1f | %9.4g %9.4g %9.4g %6.1f"
              % (p, ra["tw50"], ra["twn50"], ra["om50"], ra["deg50"],
                 rb["tw50"], rb["twn50"], rb["om50"], rb["deg50"]))

    # ------------------------------------------------ 4) L E IL SUO VERSO
    print("")
    print("--- par.4.4  L E IL SUO VERSO (momento angolare della memoria del moto) ---")
    print("  %-8s | %-40s | %-40s" % ("passo", "A: Lx Ly Lz  |L|", "B: Lx Ly Lz  |L|"))
    for p in com:
        ra, rb = rot[p]
        print("  %-8d | %9.2e %9.2e %9.2e %9.3e | %9.2e %9.2e %9.2e %9.3e"
              % (p, ra["Lx"], ra["Ly"], ra["Lz"], ra["Lmod"],
                 rb["Lx"], rb["Ly"], rb["Lz"], rb["Lmod"]))

    # ------------------------------------------------ 3) L'OLONOMIA FIRMATA (fase lenta)
    if OLON:
        print("")
        print("--- par.4.3  OLONOMIA NETTA FIRMATA e BERRY -- se divergono, e' un reperto ---")
        print("  %-8s | %-44s | %-44s" % ("passo", "A: olon_media / olon_ass / berry / coer_l",
                                          "B: olon_media / olon_ass / berry / coer_l"))
        for p in com:
            la, lb = lento(pA[p]), lento(pB[p])
            print("  %-8d | %11.4e %10.4e %10.4e %8.4g | %11.4e %10.4e %10.4e %8.4g"
                  % (p, la["olon_media"], la["olon_ass"], la["berry"], la["coer_l"],
                     lb["olon_media"], lb["olon_ass"], lb["berry"], lb["coer_l"]))
    else:
        print("")
        print("--- par.4.3  OLONOMIA: NON MISURATA in questa passata (serve `--olonomia`).")
        print("    Non e' nello snapshot: va CALCOLATA da `circolazione_topologica()`, che importa")
        print("    il simulatore. Si gira a run FINITI per non competere per la CPU.")

    print("")
    print("=" * 118)
    print("UN SEME PER RAMO. Il nullo di un confronto fra bracci su questo sistema NON e' zero:")
    print("  e' la dispersione FRA SEMI (par.9), che questo esperimento NON misura. Quindi nessuna")
    print("  differenza qui sopra e' dichiarata significativa. E NON E' UN VERDETTO: e' una misura.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
