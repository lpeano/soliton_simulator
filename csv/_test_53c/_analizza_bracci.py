"""Analisi TEST MOD 5.3c (3 bracci) — osservabili covarianti + PRESIDIO CRITICO (solo-materia).
Legge i diaglog csv/_test_53c/*.csv, riporta per braccio/seed: segno_arco_coer TOTALE,
segno_arco_coer_materia SOLO-MATERIA, spin_overlap_arco, m0_Lz. Verdetto (A) ordine / (B) separazione.
Funziona anche su risultati PARZIALI (legge i CSV presenti)."""
import os, csv, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ["segno_arco_coer", "segno_arco_coer_materia", "spin_overlap_arco", "m0_Lz"]
# punto 3 (asimmetria materia/antimateria): frazione di antimateria e raggio relativo dei due settori
COLS_ASIMM = ["frac_chi_neg", "rchi_ratio"]


def leggi(path):
    with open(path) as f:
        righe = [r for r in f if not r.startswith("#")]
    if len(righe) < 3:
        return None
    rd = csv.DictReader(righe)
    dati = {c: [] for c in COLS + COLS_ASIMM + ["n", "step"]}
    for row in rd:
        for c in dati:
            try:
                dati[c].append(float(row.get(c, "") or "nan"))
            except Exception:
                dati[c].append(float("nan"))
    return {c: np.array(v) for c, v in dati.items()}


def sintesi(v, meta_frac=0.5):
    """media 2a meta' + trend (primi3 vs ultimi3) + verdetto sale/resta/oscilla."""
    x = v[np.isfinite(v)]
    if len(x) < 4:
        return dict(media=float("nan"), primi=float("nan"), ultimi=float("nan"), stato="pochi-dati")
    k = int(len(x) * meta_frac)
    media = float(np.mean(x[k:]))
    primi = float(np.mean(x[:3]))
    ultimi = float(np.mean(x[-3:]))
    sd2 = float(np.std(x[k:]))
    # stato: SALE/RESTA (|media| significativa e stabile) vs OSCILLA/~0 (media dentro il rumore)
    if abs(media) > 3 * sd2 / max(np.sqrt(len(x[k:])), 1) and abs(media) > 0.05:
        stato = "SALE/RESTA"
    elif abs(ultimi) > 0.1 and abs(ultimi) > 2 * abs(primi - ultimi):
        stato = "sale-tardi?"
    else:
        stato = "OSCILLA/~0"
    return dict(media=media, primi=primi, ultimi=ultimi, sd=sd2, stato=stato)


files = sorted(glob.glob(os.path.join(HERE, "b*_s*.csv")))
files = [f for f in files if not f.endswith("_cond.csv")]
if not files:
    print("Nessun diaglog trovato in csv/_test_53c/. Il test non e' ancora partito o e' in corso.")
    raise SystemExit(0)

print(f"{'run':22s} {'N_fin':>6s} {'passi':>6s} | {'segno_TOT(2a met)':>18s} {'stato':>11s} | "
      f"{'segno_MATERIA':>14s} {'stato':>11s} | {'spin_ovl':>9s} | {'m0_Lz':>9s}")
print("-" * 130)
risult = {}
for f in files:
    tag = os.path.basename(f)[:-4]
    d = leggi(f)
    if d is None:
        print(f"{tag:22s}  (in corso / pochi dati)")
        continue
    n_fin = int(d["n"][-1]) if len(d["n"]) else 0
    passi = int(d["step"][-1]) if len(d["step"]) else 0
    st = {c: sintesi(d[c]) for c in COLS + COLS_ASIMM}
    risult[tag] = dict(n=n_fin, passi=passi, **st)
    print(f"{tag:22s} {n_fin:6d} {passi:6d} | "
          f"{st['segno_arco_coer']['media']:+18.5f} {st['segno_arco_coer']['stato']:>11s} | "
          f"{st['segno_arco_coer_materia']['media']:+14.5f} {st['segno_arco_coer_materia']['stato']:>11s} | "
          f"{st['spin_overlap_arco']['media']:9.4f} | {st['m0_Lz']['media']:+9.5f}")

print("\n=== TREND segno_arco_coer_materia (primi3 -> ultimi3) ===")
for tag in sorted(risult):
    m = risult[tag]["segno_arco_coer_materia"]
    print(f"{tag:22s}: {m['primi']:+.4f} -> {m['ultimi']:+.4f}  (2a met {m['media']:+.5f}, stato {m['stato']})")

print("\n=== VERDETTO PRESIDIO CRITICO (per braccio, per seed) ===")
print("(A) ORDINE VERO = solo-materia SALE/RESTA; (B) SEPARAZIONE/abeliano = solo-materia OSCILLA/~0")
for tag in sorted(risult):
    sm = risult[tag]["segno_arco_coer_materia"]
    tot = risult[tag]["segno_arco_coer"]
    verd = "(A) ORDINE VERO" if sm["stato"] == "SALE/RESTA" else "(B) SEPARAZIONE/abeliano"
    print(f"  {tag:22s}: solo-materia {sm['media']:+.5f} [{sm['stato']}] -> {verd}"
          f"   (totale {tot['media']:+.5f})")

print("\n=== PUNTO 3: ASIMMETRIA MATERIA/ANTIMATERIA (frac_chi_neg 2a met, rchi_ratio) ===")
print("frac_chi_neg = frazione antimateria (perc_chi<0); rchi_ratio>1 = antimateria piu' esterna (guscio).")
print("Confronta B2/B3 (firma) vs B1 (baseline): la 5.3c sbilancia i settori (fisica) o no (rumore)?")
for tag in sorted(risult):
    fc = risult[tag].get("frac_chi_neg", {})
    rr = risult[tag].get("rchi_ratio", {})
    if fc:
        print(f"  {tag:22s}: frac_chi_neg {fc.get('media', float('nan')):+.4f} "
              f"(primi {fc.get('primi', float('nan')):+.4f} -> ultimi {fc.get('ultimi', float('nan')):+.4f})"
              f" | rchi_ratio {rr.get('media', float('nan')):+.4f}")
