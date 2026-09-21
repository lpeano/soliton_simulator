# -*- coding: utf-8 -*-
"""ANALISI DEL RAMO D -- e OGNI TABELLA E' GENERATA DA QUI, MAI RICOPIATA A MANO.

⚠ PERCHE' ESISTE: il 2026-09-21 ho ricopiato a mano una tabella dal mio stesso file grezzo e
  **ho fatto slittare due righe**, attribuendo al passo 600 i valori del 360 e al 1080 quelli del
  600. **Su quella tabella sbagliata ho poi scritto una conclusione ROVESCIATA su `peq`**
  (`994f0ed`, voce `Z90`). Rilievo di Claude web, che aveva letto il file grezzo e non il commit.
  **Da qui in avanti: si genera e si incolla l'output. Mai la mano.**

COSA CALCOLA, tutto dagli snapshot e niente a memoria:
  T1  la tabella dei criteri ASSOLUTI, snapshot per snapshot
  T2  i RAPPORTI DI CRESCITA fra uno snapshot e il successivo -- l'espansione accelera?
  T3  `peq`: dove vive il minimo, in quale REGIONE, e `(rho - peq)/peq` su quegli archi
  T4  la coesione come motore di `d0`: e' esclusa dai numeri o no?
  T5  il CRICCHETTO: `d/d0` contro `_ab_C_solo_chicoop_FERMATO` (stessa base di epoca 2, ma
      `SCALA_MIN` e `COES_ADIM` SPENTI) -- il confronto LEGITTIMO dentro l'epoca 2

REGIONI, per origine: vuoto = nodi `< 900`, masse = `900..2390`, nati = `>= 2391`.
⚠ `N0 = 2391` e' l'`n` ALLA SEMINA, MISURATO dal disco -- NON l'`n` del primo snapshot, che e'
gia' cresciuto. Quell'errore c'era, e le percentuali per regione di `T3` erano sbagliate. Un arco e' del vuoto se ENTRAMBI i capi lo sono, di massa se
entrambi lo sono, altrimenti CONFINE.
ASCII PURO.
"""
import glob
import gzip
import io
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
D_LOC = os.path.join(RADICE, "csv", "_test_fork", "_ab_D")
C_EXT = r"E:\soliton_archivio\csv\_test_fork\_ab_C_solo_chicoop_FERMATO"
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "ANALISI_ramoD_2026-09-21.txt")
LAM = 0.8
N_VUOTO = 900
# ⚠ CORRETTO IL 2026-09-21, stesso difetto dell'estrattore: `N0` veniva dal PRIMO SNAPSHOT
#   (passo 120, n = 2663) invece che dalla SEMINA, quindi i nati con indice 2391-2662
#   risultavano MASSA e le percentuali per regione di `T3` erano sbagliate.
#   MISURATO DAL DISCO: n = 2391 alla semina.
N0_SEMINA = 2391


def carica(p):
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def passo(p):
    return int(os.path.basename(p).split("_")[1].split(".")[0])


def serie(d):
    return sorted(glob.glob(os.path.join(d, "scena_??????.pkl*")), key=passo)


def main():
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# ANALISI DEL RAMO D -- ogni tabella GENERATA DA `csv/_analisi_ramoD.py`, mai a mano\n")
    W("# EPOCA 2: CHI_COOP + SCALA_MIN + COES_ADIM accesi, piu' la cura del mondo-dopo-i-flag\n")
    W("# LAM = %.2f   vuoto = nodi < %d\n\n" % (LAM, N_VUOTO))

    F = serie(D_LOC)
    if not F:
        W("NESSUNO SNAPSHOT\n"); o.close(); return 1
    righe = []
    for p in F:
        a = carica(p)
        d = np.asarray(a["d"]); d0 = np.asarray(a["d0"]); vd = np.asarray(a["vd"])
        peq = np.asarray(a["peq"]); n = len(np.asarray(a["phi"]))
        st = np.abs(d - d0) / np.maximum(d0, 1e-300)
        pf = peq[np.isfinite(peq)]
        righe.append(dict(passo=passo(p), n=n, archi=len(d),
                          md=float(np.median(d)), md0=float(np.median(d0)),
                          rap=float(np.median(d / np.maximum(d0, 1e-300))),
                          smax=float(st.max()), s99=float(np.percentile(st, 99)),
                          v50=float(np.percentile(np.abs(vd), 50)),
                          vmax=float(np.abs(vd).max()),
                          sotto_d=int((d < LAM).sum()), sotto_d0=int((d0 < LAM).sum()),
                          peqmin=float(pf.min()) if pf.size else float("nan"),
                          nonfin=int((~np.isfinite(peq)).sum())))
    W("=" * 104 + "\nT1  I CRITERI ASSOLUTI, snapshot per snapshot\n" + "=" * 104 + "\n")
    W("%6s %6s %8s | %9s %9s %7s | %9s %9s | %8s %9s | %6s %6s | %10s\n"
      % ("passo", "n", "archi", "med d", "med d0", "d/d0", "stress99", "stressMAX",
         "|vd|p50", "|vd|max", "d<LAM", "d0<LAM", "peq min"))
    for r in righe:
        W("%6d %6d %8d | %9.4f %9.4f %7.4f | %9.4g %9.4g | %8.4g %9.4g | %6d %6d | %10.3e\n"
          % (r["passo"], r["n"], r["archi"], r["md"], r["md0"], r["rap"], r["s99"], r["smax"],
             r["v50"], r["vmax"], r["sotto_d"], r["sotto_d0"], r["peqmin"]))
    W("\nCRITERIO ASSOLUTO 'frazione di archi sotto LAM = zero a ogni snapshot': %s\n"
      % ("SODDISFATTO" if all(r["sotto_d"] == 0 and r["sotto_d0"] == 0 for r in righe)
         else "NON soddisfatto"))
    W("CRITERIO ASSOLUTO 'd/d0 vicino a 1 (trasparenza)': d/d0 va da %.4f a %.4f -> %s\n"
      % (righe[0]["rap"], righe[-1]["rap"], "NON soddisfatto: i legami sono COMPRESSI"))

    W("\n" + "=" * 104 + "\nT2  RAPPORTI DI CRESCITA fra uno snapshot e il successivo\n")
    W("    (>1 = cresce; se il rapporto CRESCE a sua volta, l'espansione ACCELERA)\n" + "=" * 104 + "\n")
    W("%12s | %8s %8s %8s %8s %8s\n" % ("intervallo", "med d", "med d0", "|vd|p50", "n", "peqmin"))
    for k in range(1, len(righe)):
        a, b = righe[k - 1], righe[k]
        W("%5d->%5d | %8.4f %8.4f %8.4f %8.4f %8.4g\n"
          % (a["passo"], b["passo"], b["md"] / a["md"], b["md0"] / a["md0"],
             b["v50"] / max(a["v50"], 1e-300), b["n"] / a["n"],
             b["peqmin"] / max(a["peqmin"], 1e-300)))
    W("\nmediana di `d`: da %.4f a %.4f = %.1f VOLTE in %d passi\n"
      % (righe[0]["md"], righe[-1]["md"], righe[-1]["md"] / righe[0]["md"],
         righe[-1]["passo"] - righe[0]["passo"]))
    W("|vd| p50:       da %.4f a %.4f = %.1f VOLTE  -> cresce TUTTA la popolazione, non una coda\n"
      % (righe[0]["v50"], righe[-1]["v50"], righe[-1]["v50"] / righe[0]["v50"]))

    W("\n" + "=" * 104 + "\nT3  `peq`: la traiettoria del minimo, e DOVE vive\n" + "=" * 104 + "\n")
    W("%6s %12s %10s | dove vive il minimo\n" % ("passo", "peq min", "non fin."))
    for p in F:
        a = carica(p)
        peq = np.asarray(a["peq"]); i = np.asarray(a["i"]); j = np.asarray(a["j"])
        fin = np.isfinite(peq)
        if not fin.any():
            continue
        k = int(np.argmin(np.where(fin, peq, np.inf)))
        def reg(x):
            return "vuoto" if x < N_VUOTO else ("massa" if x < N0_SEMINA else "nato")
        W("%6d %12.4e %10d | arco %d-%d  (%s - %s)\n"
          % (passo(p), peq[k], int((~fin).sum()), i[k], j[k], reg(i[k]), reg(j[k])))
    # la coda bassa di peq all'ultimo snapshot, per regione
    a = carica(F[-1])
    peq = np.asarray(a["peq"]); i = np.asarray(a["i"]); j = np.asarray(a["j"])
    fin = np.isfinite(peq)
    q = np.percentile(peq[fin], 1)
    bassi = fin & (peq <= q)
    def regione_arco(ii, jj):
        rv = (ii < N_VUOTO) & (jj < N_VUOTO)
        rm = (ii >= N_VUOTO) & (jj >= N_VUOTO) & (ii < N0_SEMINA) & (jj < N0_SEMINA)
        rn = (ii >= N0_SEMINA) | (jj >= N0_SEMINA)
        return rv, rm, rn
    rv, rm, rn = regione_arco(i, j)
    W("\nall'ultimo snapshot (passo %d), l'1%% piu' BASSO di `peq` (%d archi, peq <= %.3e):\n"
      % (passo(F[-1]), int(bassi.sum()), q))
    for nome, m in (("vuoto-vuoto", rv), ("massa-massa", rm), ("coinvolge un NATO", rn)):
        tot = int((m & fin).sum())
        W("   %-20s %6d archi bassi su %7d della regione  (%5.2f%%)\n"
          % (nome, int((bassi & m).sum()), tot, 100.0 * (bassi & m).sum() / max(tot, 1)))
    # (rho - peq)/peq sugli archi bassi, se rho e' ricostruibile
    try:
        psi = np.asarray(a["psi"]); I = np.abs(psi) ** 2
        rho_arc = 0.5 * (I[i] + I[j])
        anom = (rho_arc - peq) / np.maximum(peq, 1e-9)   # IL PAVIMENTO DEL CODICE, :4215
        W("\n(rho_arco - peq)/peq  -- il fattore che entra in `src`:\n")
        W("   su TUTTI gli archi:      p50=%.4g  p99=%.4g  max=%.4g\n"
          % (np.percentile(anom[fin], 50), np.percentile(anom[fin], 99), anom[fin].max()))
        W("   sull'1%% con peq basso:   p50=%.4g  p99=%.4g  max=%.4g\n"
          % (np.percentile(anom[bassi], 50), np.percentile(anom[bassi], 99), anom[bassi].max()))
    except Exception as e:
        W("\n(rho - peq)/peq NON calcolabile: %s\n" % e)

    W("\n" + "=" * 104 + "\nT4  LA COESIONE E' IL MOTORE DI `d0`?\n" + "=" * 104 + "\n")
    W("%6s %14s %14s %12s %14s\n" % ("passo", "_g_coes_max", "_g_coes_tetto", "saturi", "med d0"))
    for p, r in zip(F, righe):
        a = carica(p)
        W("%6d %14s %14s %12s %14.4f\n"
          % (passo(p), a.get("_g_coes_max", "assente"), a.get("_g_coes_tetto", "assente"),
             a.get("_g_coes_satura", "assente"), r["md0"]))
    W("\nLETTURA: se `_g_coes_max` e' costante e piccolo mentre `med d0` cresce di ordini,\n")
    W("  la coesione NON puo' essere il motore di `d0`. Il numero decide, non l'impressione.\n")

    W("\n" + "=" * 104 + "\nT5  IL CRICCHETTO: `d/d0` con SCALA_MIN+COES_ADIM contro SENZA\n")
    W("    (confronto LEGITTIMO: stessa base di EPOCA 2, cambiano solo i due flag)\n" + "=" * 104 + "\n")
    G = serie(C_EXT) if os.path.isdir(C_EXT) else []
    if not G:
        W("  `_ab_C_solo_chicoop_FERMATO` NON trovato in %s -- confronto NON fatto.\n" % C_EXT)
    else:
        W("%6s | %9s %9s %7s %8s | %9s %9s %7s %8s\n"
          % ("passo", "D med d", "D med d0", "D d/d0", "D d<LAM", "C med d", "C med d0",
             "C d/d0", "C d<LAM"))
        gp = {passo(x): x for x in G}
        for p, r in zip(F, righe):
            k = passo(p)
            if k not in gp:
                continue
            b = carica(gp[k])
            dd = np.asarray(b["d"]); dd0 = np.asarray(b["d0"])
            W("%6d | %9.4f %9.4f %7.4f %8d | %9.4f %9.4f %7.4f %8d\n"
              % (k, r["md"], r["md0"], r["rap"], r["sotto_d"],
                 float(np.median(dd)), float(np.median(dd0)),
                 float(np.median(dd / np.maximum(dd0, 1e-300))), int((dd < LAM).sum())))
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
