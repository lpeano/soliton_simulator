"""[branch dev-spinoriale] VERDETTO covariante FASE 3 (ON vs OFF, N-appaiato).

Legge i diaglog csv/fase3_cov/diag_{on,off}_s{1,2,3}.csv e risponde alla DOMANDA:
  in ON (forze = overlap spinoriale) il SEGNO di doppia-copertura diventa un ATTRATTORE
  (segno_arco_coer resta alto a N appaiato), mentre in OFF DECADE (par.48 = repulsore)?

REGOLA COVARIANTE (CLAUDE.md): NON confrontare a step-coordinata fisso. Il sistema si espande
(N cresce), quindi appaiamo per N (bin logaritmici) e confrontiamo ON vs OFF nello stesso bin di N.
Osservabili gia' relazionali/adimensionali: segno_arco_coer, spin_overlap_arco, verso_arco_coer,
berry_spin_media (firmata), berry_spin_media_assoluta, coer_01.

Uso: python csv/fase3_cov/_verdetto_fase3.py
Per Claude: doppio-check indipendente. Rigenera i diaglog con run_covariante_fase3.ps1.
"""
import os, csv, glob
import numpy as np

BASE = os.path.dirname(__file__)
SEEDS = [1, 2, 3]
COLS = ["segno_arco_coer", "spin_overlap_arco", "verso_arco_coer",
        "berry_spin_media", "berry_spin_media_assoluta", "coer_01", "m0_coer_nucleo"]


def carica(path):
    if not os.path.exists(path):
        return None
    righe = [l for l in open(path) if not l.lstrip().startswith("#")]
    d = list(csv.DictReader(righe))
    if not d:
        return None
    out = {}
    for k in ["step", "n"] + COLS:
        if k in d[0]:
            out[k] = np.array([float(x[k]) for x in d if x.get(k) not in ("", None)])
    return out


def bins_N(nmin, nmax, nbin=8):
    return np.unique(np.round(np.linspace(nmin, nmax, nbin + 1)).astype(int))


print("=== VERDETTO FASE 3 covariante (ON vs OFF, N-appaiato) ===\n")

# range N comune (intersezione ON/OFF su tutti i seed) per appaiamento onesto
tutti_on, tutti_off = {}, {}
for s in SEEDS:
    on = carica(os.path.join(BASE, f"diag_on_s{s}.csv"))
    off = carica(os.path.join(BASE, f"diag_off_s{s}.csv"))
    if on:  tutti_on[s] = on
    if off: tutti_off[s] = off

if not tutti_on or not tutti_off:
    print("Dati incompleti: attendo che i run producano diag_on_s*/diag_off_s*.csv")
    raise SystemExit(0)

# N-range appaiato: [max dei min, min dei max] su tutti i run disponibili
nmins = [d["n"].min() for d in list(tutti_on.values()) + list(tutti_off.values())]
nmaxs = [d["n"].max() for d in list(tutti_on.values()) + list(tutti_off.values())]
lo, hi = max(nmins), min(nmaxs)
edges = bins_N(lo, hi, 8)
print(f"N-range appaiato: [{lo:.0f}, {hi:.0f}]  bin={list(edges)}\n")


def media_per_bin(d, col, edges):
    if col not in d:
        return np.full(len(edges) - 1, np.nan)
    N, v = d["n"], d[col]
    out = np.full(len(edges) - 1, np.nan)
    for b in range(len(edges) - 1):
        m = (N >= edges[b]) & (N < edges[b + 1])
        if m.sum() > 0:
            out[b] = np.nanmean(v[m])
    return out


for col in COLS:
    print(f"--- {col} (media per bin di N, appaiata) ---")
    print("  %-10s %10s %10s %10s" % ("bin_N", "ON", "OFF", "ON-OFF"))
    on_stack, off_stack = [], []
    for s in SEEDS:
        if s in tutti_on:  on_stack.append(media_per_bin(tutti_on[s], col, edges))
        if s in tutti_off: off_stack.append(media_per_bin(tutti_off[s], col, edges))
    on_m = np.nanmean(np.vstack(on_stack), axis=0) if on_stack else np.full(len(edges) - 1, np.nan)
    off_m = np.nanmean(np.vstack(off_stack), axis=0) if off_stack else np.full(len(edges) - 1, np.nan)
    for b in range(len(edges) - 1):
        etic = f"{edges[b]}-{edges[b+1]}"
        print("  %-10s %10.4f %10.4f %+10.4f" % (etic, on_m[b], off_m[b], on_m[b] - off_m[b]))
    d_late = np.nanmean((on_m - off_m)[len(on_m) // 2:])
    print("  DELTA ON-OFF (meta' alta di N): %+.4f\n" % d_late)

print("=== LETTURA ===")
print("Se segno_arco_coer ON-OFF > 0 e CRESCE/RESTA a N alto -> l'ordine e' ATTRATTORE")
print("  (la visione spinoriale RIBALTA il par.48: il segno ordina, non-abeliano EMERGE).")
print("Se ON-OFF ~ 0 su tutti i bin -> abeliano piu' profondo del previsto (risultato onesto,")
print("  le forze spinoriali non bastano a rendere l'ordine attrattore).")
print("berry_spin_media (firmata) != 0 in ON = fase geometrica non-abeliana accumulata.")
