# -*- coding: utf-8 -*-
"""`f` E `median(|f|)`, SEPARATI -- il metro si accorcia o la grandezza cresce?

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_f-e-median.md (929d61e).
NESSUN RUN: i dati bastano. `psi_spin` e `_psi_spin_prec` sono ENTRAMBI negli snapshot, a un passo
di distanza, e `_med_f_prec` -- il `med` USATO dopo `Z42` -- e' salvato.

LA CONTRADDIZIONE DA SCIOGLIERE (algebra di Claude web, DA FALSIFICARE PER PRIMA):
  invertendo r = (x/sqrt(1+x^2) + 1e-6)/r_unit si otterrebbe x ~ 1.6 (passo 12), ~4.35 (18),
  ~224 (24) e da li' mai piu' giu'. Ma una crescita di f di centinaia di volte PER PASSO sostenuta
  per 2700 passi e' impossibile, e senza il pavimento x non puo' restare enorme -- e il contatore
  `_ritmo_med_sul_pavimento` vale DUE su 2700. UNA DELLE TRE AFFERMAZIONI E' FALSA.

LA FORMULA E' LETTA DAL SORGENTE (`ritmo()`), non ricordata:
  a      = angle(_ps[:,0]) - angle(_psp[:,0])
  signed = ((a + 2pi) % (4pi) - 2pi) / DT          wrapping su 4pi (l'otto)
  f      = signed se TEMPO_PROPRIO_ORIENTATO altrimenti |signed|

LE QUATTRO LETTURE
  alpha  median(|f|) CROLLA      -> il METRO si accorcia (A3): f puo' essere tranquillo
  beta   f CRESCE davvero        -> la causa e' nella dinamica
  gamma  nessuno dei due si muove-> l'algebra e' sbagliata, e si chiude li'
  delta  il pavimento scatta > 2 volte per passo -> il contatore conta un'altra cosa

f e x sono DUE COSE DIVERSE: si riportano SEPARATI. |f| coi percentili, mai una mediana da sola.
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

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
FINESTRE = [("0 -> 60", "csv/_test_fork/_fin_A"), ("180 -> 240", "csv/_test_fork/_fin_B")]
# l'x DEDOTTO invertendo r, dal mandato: e' QUELLO da falsificare
X_DEDOTTO = {12: 1.6, 18: 4.35, 24: 224.0}


def carica(p):
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def passo_di(p):
    return int(re.search(r"_(\d{6})\.", p).group(1))


def q(a, p):
    a = a[np.isfinite(a)]
    return float(np.percentile(a, p)) if a.size else float("nan")


def main():
    sys.path.insert(0, RADICE)
    import soliton_simulator as S
    DT = float(S.DT)
    print("DT = %s   TEMPO_PROPRIO_ORIENTATO = %s (default del modulo)   r_unit = 1/sqrt(2)+1e-6"
          % (DT, S.TEMPO_PROPRIO_ORIENTATO))
    print("")

    for titolo, d in FINESTRE:
        fs = sorted(glob.glob(os.path.join(RADICE, d, "scena_??????.pkl*")))
        if not fs:
            print("FINESTRA %s: nessuno snapshot in %s" % (titolo, d))
            continue
        print("=" * 124)
        print("FINESTRA %s   (%d snapshot)" % (titolo, len(fs)))
        print("=" * 124)
        print("%-7s | %-10s %-10s %-10s %-10s %-10s | %-11s %-11s | %-9s %-7s"
              % ("passo", "|f| p05", "|f| p25", "|f| p50", "|f| p95", "|f| max",
                 "med_f_prec", "med_f_ult", "x = p50/med", "pav+"))
        prec_pav = None
        righe = []
        for p in fs:
            at = carica(p)
            passo = passo_di(p)
            _ps = at.get("psi_spin"); _psp = at.get("_psi_spin_prec")
            if _ps is None or _psp is None:
                print("%-7d | psi_spin o _psi_spin_prec ASSENTI" % passo)
                continue
            _ps = np.asarray(_ps); _psp = np.asarray(_psp)
            n = min(len(_ps), len(_psp), len(at["eta"]))
            a = np.angle(_ps[:n, 0]) - np.angle(_psp[:n, 0])
            signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / DT
            f = signed if S.TEMPO_PROPRIO_ORIENTATO else np.abs(signed)
            fa = np.abs(f)
            medp = at.get("_med_f_prec"); medu = at.get("_med_f_ultimo")
            pav = at.get("_ritmo_med_sul_pavimento")
            dpav = (pav - prec_pav) if (prec_pav is not None and pav is not None) else None
            prec_pav = pav
            x = (q(fa, 50) / medp) if (medp not in (None, 0)) else float("nan")
            righe.append(dict(passo=passo, med=medp, f50=q(fa, 50), x=x,
                              fmax=float(np.nanmax(fa)) if fa.size else float("nan")))
            print("%-7d | %-10.4g %-10.4g %-10.4g %-10.4g %-10.4g | %-11.6g %-11.6g | %-9.4g %-7s"
                  % (passo, q(fa, 5), q(fa, 25), q(fa, 50), q(fa, 95),
                     float(np.nanmax(fa)) if fa.size else float("nan"),
                     medp if medp is not None else float("nan"),
                     medu if medu is not None else float("nan"),
                     x, ("+%d" % dpav) if dpav is not None else "-"))
            del at
        print("")
        if len(righe) >= 2:
            a0, a1 = righe[0], righe[-1]
            print("  |f| MEDIANA:  %.6g -> %.6g   (x%.4g)"
                  % (a0["f50"], a1["f50"], a1["f50"] / a0["f50"] if a0["f50"] else float("nan")))
            print("  med USATO  :  %.6g -> %.6g   (x%.4g)"
                  % (a0["med"], a1["med"], a1["med"] / a0["med"] if a0["med"] else float("nan")))
            m = [r["med"] for r in righe if r["med"]]
            if len(m) > 1:
                osc = max(abs(m[k] / m[k - 1] - 1) for k in range(1, len(m)))
                print("  OSCILLAZIONE massima di `med` fra passi consecutivi: %.1f %%   (Z43 dava 62 %%)"
                      % (100 * osc))
        print("")

    # ------------------------------------------------ il controllo che puo' chiudere tutto
    print("=" * 124)
    print("IL CONTROLLO: x RICALCOLATO contro x DEDOTTO invertendo r  (l'algebra da FALSIFICARE)")
    print("=" * 124)
    fs = sorted(glob.glob(os.path.join(RADICE, "csv/_test_fork/_fin_A", "scena_??????.pkl*")))
    print("%-7s | %-14s %-14s | %-10s" % ("passo", "x DEDOTTO", "x RICALCOLATO", "rapporto"))
    esito = []
    for p in fs:
        passo = passo_di(p)
        if passo not in X_DEDOTTO:
            continue
        at = carica(p)
        _ps = np.asarray(at["psi_spin"]); _psp = np.asarray(at["_psi_spin_prec"])
        n = min(len(_ps), len(_psp))
        a = np.angle(_ps[:n, 0]) - np.angle(_psp[:n, 0])
        signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / DT
        fa = np.abs(signed)
        med = at.get("_med_f_prec")
        xr = q(fa, 50) / med if med else float("nan")
        xd = X_DEDOTTO[passo]
        print("%-7d | %-14.6g %-14.6g | %-10.4g" % (passo, xd, xr, xr / xd if xd else float("nan")))
        esito.append((passo, xd, xr))
        del at
    print("")
    ok = all(0.5 <= (xr / xd) <= 2.0 for _, xd, xr in esito if xd and np.isfinite(xr))
    if esito and ok:
        print("-> l'algebra del mandato REGGE entro un fattore 2: x e' davvero enorme.")
    elif esito:
        print("-> *** L'ALGEBRA DEL MANDATO NON REGGE: x ricalcolato NON coincide con x dedotto. ***")
        print("   Era la prima cosa da falsificare, ed e' falsificata. La pista si chiude qui,")
        print("   e `r = sqrt(2)` ha un'altra spiegazione.")
    else:
        print("-> nessun passo confrontabile.")
    print("")
    print("UN SEME, UNA SCENA. Nessun verdetto di fisica.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
