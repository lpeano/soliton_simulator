# -*- coding: utf-8 -*-
"""IL PASSO 198: evento FISICO o ECCEZIONE NUMERICA?

Letture e criteri FISSATI PRIMA: doc/TASK_HISTORY/2026-09-19_passo198.md (8132be8).
Dati: csv/_test_fork/_fin_B, 11 snapshot a 6 passi (180-240), rigiocata sigillata 3/3.
NESSUN RUN. NESSUNA CURA. Si legge, uno snapshot alla volta.

IL FATTO: omega_s max fa 0.31 -> 401 in SEI passi, a popolazione COSTANTE (nati 3 -> 3).

LE DUE LETTURE
  A POPOLAZIONE  log(p50_198/p50_192)/log(max_198/max_192) >= 0.3  -> fenomeno del SISTEMA
  B POCHI NODI   nodi sopra 10*p99_192 <= 100 E p50 cresce meno di x2 -> profilo di ARTEFATTO

I TRE CANDIDATI NUMERICI, DA DATARE
  1 _cs_lam_degenere: se _Lam = mean(I) <= 1e-30 allora _scala = 1e-30, sqrt(1/_scala) = 1e15 e
    cs_floor COLLASSA. cs sta al DENOMINATORE di tau = d/cs (--tau-luce ATTIVO): tau esplode e il
    freno -omega/tau sparisce. Al 2700 il contatore vale 2: QUANDO sono scattate?
  2 _fatt_cs_ultimo: atteso ~1, al 2700 vale 142.8.
  3 NaN / inf / overflow non ancora inf (oltre 1e10, oltre 1e15).

IL MASSIMO NON E' LA DISTRIBUZIONE (A3c): si riportano p25/p50/p75/p95/p99/max, tutti.
I contatori sono CUMULATIVI: si datano con le DIFFERENZE.
ASCII PURO.
"""
import glob
import gzip
import math
import os
import pickle
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

ARCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join("csv", "_test_fork", "_fin_B")
SOGLIE = (1e1, 1e2, 1e3, 1e4)
CONTATORI = ("_cs_lam_degenere", "_cs_fallback", "_cs_in_fallback", "_taup_cs_clamp",
             "_inerzia_al_pavimento", "_ritmo_med_sul_pavimento", "_ritmo_f_tutto_nullo",
             "_sfondo_ko_rho", "_sfondo_ko_peq", "_rep_taupp_clamp", "_taup_peq_degenere")
CAMPI_NAN = ("omega_s", "psi", "psi_spin", "peq", "_cs_nodo_prev", "_fatt_cs_ultimo", "d", "tw")


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def passo_di(p):
    return int(re.search(r"_(\d{6})\.", p).group(1))


def mod(v):
    a = np.asarray(v)
    return np.abs(a).ravel().astype(float) if a.dtype.kind == "c" else np.abs(a.astype(float)).ravel()


def norma(v):
    a = np.asarray(v, float)
    return np.linalg.norm(a, axis=1) if a.ndim > 1 else np.abs(a)


def q(a, p):
    a = a[np.isfinite(a)]
    return float(np.percentile(a, p)) if a.size else float("nan")


def main():
    fs = sorted(glob.glob(os.path.join(ARCH, "scena_??????.pkl*")))
    print("snapshot: %d, passi %d-%d" % (len(fs), passo_di(fs[0]), passo_di(fs[-1])))
    print("")

    # ---------------------------------------------------------------- 1) LA DISTRIBUZIONE
    print("=" * 126)
    print("1) omega_s: LA DISTRIBUZIONE, non il massimo (A3c)")
    print("=" * 126)
    print("%-7s %-7s | %-10s %-10s %-10s %-10s %-10s %-10s | %s"
          % ("passo", "n", "p25", "p50", "p75", "p95", "p99", "max",
             "  ".join("n>%.0e" % s for s in SOGLIE)))
    R = []
    for p in fs:
        at = carica(p)["attrs"]
        om = norma(at["omega_s"])
        n = len(at["eta"])
        sop = {s: set(np.flatnonzero(om > s).tolist()) for s in SOGLIE}
        R.append(dict(passo=passo_di(p), n=n, om=om, sop=sop, at=None,
                      p25=q(om, 25), p50=q(om, 50), p75=q(om, 75),
                      p95=q(om, 95), p99=q(om, 99), mx=float(np.nanmax(om)),
                      cont={k: at.get(k) for k in CONTATORI},
                      fcs=np.asarray(at.get("_fatt_cs_ultimo", []), float).copy(),
                      nan={k: (int(np.sum(~np.isfinite(mod(at[k])))) if k in at else None)
                           for k in CAMPI_NAN},
                      big={k: (int(np.sum(mod(at[k]) > 1e10)) if k in at else None)
                           for k in CAMPI_NAN},
                      huge={k: (int(np.sum(mod(at[k]) > 1e15)) if k in at else None)
                            for k in CAMPI_NAN},
                      file=p))
        print("%-7d %-7d | %-10.4g %-10.4g %-10.4g %-10.4g %-10.4g %-10.4g | %s"
              % (R[-1]["passo"], n, R[-1]["p25"], R[-1]["p50"], R[-1]["p75"],
                 R[-1]["p95"], R[-1]["p99"], R[-1]["mx"],
                 "  ".join("%6d" % len(sop[s]) for s in SOGLIE)))
        del at

    # il verdetto A/B sull'intervallo 192 -> 198
    i192 = next(k for k, x in enumerate(R) if x["passo"] == 192)
    i198 = next(k for k, x in enumerate(R) if x["passo"] == 198)
    a, b = R[i192], R[i198]
    print("")
    print("  INTERVALLO 192 -> 198")
    rap_max = b["mx"] / a["mx"] if a["mx"] > 0 else float("inf")
    rap_p50 = b["p50"] / a["p50"] if a["p50"] > 0 else float("inf")
    print("     max:  %.4g -> %.4g   (x%.4g)" % (a["mx"], b["mx"], rap_max))
    print("     p50:  %.4g -> %.4g   (x%.4g)" % (a["p50"], b["p50"], rap_p50))
    quota = (math.log(rap_p50) / math.log(rap_max)) if (rap_p50 > 0 and rap_max > 1
                                                        and math.isfinite(rap_p50)) else float("nan")
    print("     quota della mediana sul salto (log/log): %.4f   [A vuole >= 0.30]" % quota)
    soglia_b = 10 * a["p99"]
    sopra = int(np.sum(b["om"] > soglia_b)) if math.isfinite(soglia_b) else -1
    print("     nodi sopra 10*p99(192) = %.4g : %d   [B vuole <= 100]" % (soglia_b, sopra))
    print("")
    if math.isfinite(quota) and quota >= 0.30:
        print("  -> LETTURA A: LA POPOLAZIONE SI SPOSTA. E' un fenomeno del sistema.")
    elif sopra <= 100 and rap_p50 < 2.0:
        print("  -> LETTURA B: POCHI NODI SCHIZZANO (%d), e la mediana NON segue (x%.3g)." % (sopra, rap_p50))
        print("     E' IL PROFILO DI UN ARTEFATTO, e si indaga come tale.")
    else:
        print("  -> NESSUNA DELLE DUE: quota %.4f, nodi sopra soglia %d, p50 x%.3g."
              % (quota, sopra, rap_p50))

    # sono SEMPRE GLI STESSI? (Jaccard, metodo di Z46)
    print("")
    print("  SONO SEMPRE GLI STESSI? Jaccard fra istanti consecutivi, sui nodi sopra 1e2")
    for k in range(1, len(R)):
        A_, B_ = R[k - 1]["sop"][1e2], R[k]["sop"][1e2]
        u = len(A_ | B_)
        j = len(A_ & B_) / u if u else float("nan")
        print("     %d -> %-6d |A|=%-5d |B|=%-5d  Jaccard = %s"
              % (R[k - 1]["passo"], R[k]["passo"], len(A_), len(B_),
                 "%.4f" % j if u else "-"))

    # ---------------------------------------------------------------- 2) I CONTATORI, DATATI
    print("")
    print("=" * 126)
    print("2) I CONTATORI, DATATI (differenze: sono CUMULATIVI)")
    print("=" * 126)
    print("%-7s %s" % ("passo", "  ".join("%-22s" % c[:22] for c in CONTATORI)))
    for k, x in enumerate(R):
        if k == 0:
            print("%-7d %s" % (x["passo"], "  ".join("%-22s" % ("(base %s)" % x["cont"][c])
                                                     for c in CONTATORI)))
            continue
        d = []
        for c in CONTATORI:
            v0, v1 = R[k - 1]["cont"][c], x["cont"][c]
            d.append("%-22s" % (("+%d" % (v1 - v0)) if (v0 is not None and v1 is not None)
                                else "-"))
        print("%-7d %s" % (x["passo"], "  ".join(d)))

    # ---------------------------------------------------------------- 3) fatt_cs
    print("")
    print("=" * 126)
    print("3) _fatt_cs_ultimo  (atteso ~1; al passo 2700 vale 142.8)")
    print("=" * 126)
    print("%-7s | %-10s %-10s %-10s %-10s | %-8s" % ("passo", "p50", "p95", "p99", "max", "n>10"))
    for x in R:
        f = x["fcs"]
        if not f.size:
            print("%-7d | ASSENTE" % x["passo"]); continue
        print("%-7d | %-10.5g %-10.5g %-10.5g %-10.5g | %-8d"
              % (x["passo"], q(f, 50), q(f, 95), q(f, 99), float(np.nanmax(f)),
                 int(np.sum(f > 10))))

    # ---------------------------------------------------------------- 4) NaN / estremi
    print("")
    print("=" * 126)
    print("4) NaN / inf  e  VALORI ESTREMI MA FINITI   (zero e' l'atteso)")
    print("=" * 126)
    print("%-7s | %s" % ("passo", "  ".join("%-14s" % c[:14] for c in CAMPI_NAN)))
    tot_nan = 0
    for x in R:
        riga = []
        for c in CAMPI_NAN:
            nn, bg, hg = x["nan"][c], x["big"][c], x["huge"][c]
            if nn is None:
                riga.append("%-14s" % "-")
            else:
                tot_nan += nn
                riga.append("%-14s" % ("nan%d/1e10:%d/1e15:%d" % (nn, bg, hg)
                                       if (nn or bg or hg) else "."))
        print("%-7d | %s" % (x["passo"], "  ".join(riga)))
    print("")
    print("  TOTALE non finiti su tutti i campi e tutti gli istanti: %d" % tot_nan)
    print("  ('.' = zero NaN, zero oltre 1e10, zero oltre 1e15)")
    print("")
    print("UN SEME, UNA SCENA. --tau-luce sigillo 6/7. Nessun verdetto di fisica.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
