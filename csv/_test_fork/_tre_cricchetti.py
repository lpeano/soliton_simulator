# -*- coding: utf-8 -*-
"""I TRE CRICCHETTI, misurati sui 45 snapshot del run fermato al passo 2700.

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-19_tre-cricchetti.md (05b1391).
NESSUN RUN NUOVO. NESSUNA CURA. Il simulatore non si tocca: si LEGGE.

  1. chi_basc AZZERA L'ANTIMATERIA
       frac(perc_chi == +1) nel tempo, e il CONTROLLO DI CONSISTENZA: twn ricostruito dal codice
       (:3530-3534) deve riprodurre perc_chi. Se non lo riproduce, LA MISURA NON VALE.
  2. omega_s ACCUMULA
       percentili di |omega_s| nel tempo: MONOTONO = cricchetto (A7); PLATEAU = no.
       Piu' `_tau` EFFETTIVO -- che in questo run e' `_tempo_luce_nodo`, NON `TAU_A*(...)`:
       --tau-luce e' ON, e il ramo del mandato NON GIRA (verificato dal codice, :2438).
  3. LA PORTATA SI ACCORCIA  (ipotesi di Claude web, DEDOTTA: puo' cadere)
       rc = 3*median(lambda_nodi()) contro median(d), e il GRADO per percentili.
       REGGE se rc/d scende sotto 1 E il grado si separa NELLO STESSO INTERVALLO. Altrimenti CADE.
  4. l'INERZIA AL PAVIMENTO per INTERVALLO (i contatori sono CUMULATIVI: si fanno le differenze).

*** DUE COSE CHE QUESTO SCRIPT FA E CHE VANNO DETTE ***
(a) `lambda_nodi` NON viene ricostruito: si RICARICA lo snapshot in una `Rete` e si chiama IL
    METODO VERO. E' una catena ricorsiva (lambda_nodi -> massa_critica_adattiva -> _pesi ->
    lambda_nodi), e ricostruirla fuori e' l'errore gia' fatto su `correzione`.
(b) NON si tengono gli snapshot in RAM: 45 x ~50 MB decompressi = ~2 GB. Si legge uno alla volta e
    si trattengono solo i NUMERI.

`_deg` e' BIMODALE ESTREMA (mediana 2, p75 501): la mediana non descrive niente, si riportano i
percentili (A3c). UN SEME, UNA SCENA. --tau-luce ha sigillo 6/7.
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

ARCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join("csv", "_test_fork", "_g6000")


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def passo_di(p):
    return int(re.search(r"_(\d{6})\.", p).group(1))


def pc(a, q):
    a = np.asarray(a, float).ravel()
    a = a[np.isfinite(a)]
    return float(np.percentile(a, q)) if a.size else float("nan")


def main():
    sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..", "..")))
    import soliton_simulator as S
    print("costanti LETTE dal modulo: PHI_CRIT=%.6f  LAM=%s  TAU_A=%s  DT=%s"
          % (S.PHI_CRIT, S.LAM, S.TAU_A, S.DT))
    print("pavimento di lambda_nodi = LAM*0.15 = %.4f   ->   rc al pavimento = %.4f"
          % (S.LAM * 0.15, 3 * S.LAM * 0.15))

    fs = sorted(glob.glob(os.path.join(ARCH, "scena_??????.pkl*")))
    print("snapshot: %d, dal passo %d al %d" % (len(fs), passo_di(fs[0]), passo_di(fs[-1])))
    print("")

    # ------------------------------------------------------------------ 1 + 2 + 4
    print("=" * 118)
    print("1) chi_basc  |  2) omega_s  |  4) inerzia al pavimento")
    print("=" * 118)
    print("%-7s %-7s | %-9s %-9s %-7s | %-10s %-10s %-10s | %-9s %-9s | %-8s"
          % ("passo", "n", "fr(+1)", "fr(twn>s)", "OK?", "|om| p50", "|om| p90", "|om| max",
             "twn/s p50", "cambi", "inerz.pav"))
    prec = None
    righe = []
    for p in fs:
        at = carica(p)["attrs"]
        passo, n = passo_di(p), len(at["eta"])
        chi = np.asarray(at["perc_chi"], int)[:n]
        fr1 = float(np.mean(chi == 1))
        # RICOSTRUZIONE di twn, ESATTAMENTE come :3530-3534
        i = np.asarray(at["i"], np.int64); j = np.asarray(at["j"], np.int64)
        twabs = np.abs(np.asarray(at["tw"], float))
        twn = np.zeros(n)
        np.add.at(twn, i, twabs); np.add.at(twn, j, twabs)
        deg = np.asarray(at["_deg"], float)[:n]
        twn = twn / np.maximum(deg, 1)
        frtw = float(np.mean(twn > S.PHI_CRIT))
        # il controllo di consistenza: le DUE frazioni devono coincidere
        concorda = float(np.mean((twn > S.PHI_CRIT) == (chi == 1)))
        # |omega_s| e' la NORMA del vettore (n,3), non il modulo componente per componente:
        # confondere le due cose darebbe percentili su 3n scalari invece che su n moduli.
        _o = np.asarray(at["omega_s"], float)
        om = np.linalg.norm(_o, axis=1) if _o.ndim > 1 else np.abs(_o)
        cambi = float("nan")
        if prec is not None:
            m = min(len(prec["chi"]), len(chi))
            cambi = float(np.mean(prec["chi"][:m] != chi[:m]))
        pav = at.get("_inerzia_al_pavimento", 0); tot = at.get("_inerzia_tot", 0)
        dpav = (pav - prec["pav"]) / max(tot - prec["tot"], 1) if prec else float("nan")
        righe.append(dict(passo=passo, n=n, fr1=fr1, frtw=frtw, conc=concorda,
                          om50=pc(om, 50), om90=pc(om, 90), ommax=float(om.max()),
                          twn50=pc(twn / S.PHI_CRIT, 50), cambi=cambi, dpav=dpav,
                          d50=pc(at["d"], 50), deg25=pc(deg, 25), deg50=pc(deg, 50),
                          deg75=pc(deg, 75), file=p))
        print("%-7d %-7d | %-9.4f %-9.4f %-7s | %-10.4g %-10.4g %-10.4g | %-9.3f %-9s | %-8s"
              % (passo, n, fr1, frtw, "SI" if concorda > 0.999 else "NO %.3f" % concorda,
                 pc(om, 50), pc(om, 90), om.max(), pc(twn / S.PHI_CRIT, 50),
                 "%.4f" % cambi if np.isfinite(cambi) else "-",
                 "%.4f" % dpav if np.isfinite(dpav) else "-"))
        prec = dict(chi=chi, pav=pav, tot=tot)

    print("")
    peggio = min(r["conc"] for r in righe)
    print("CONTROLLO DI CONSISTENZA (1): accordo MINIMO fra twn>PHI_CRIT e perc_chi = %.6f" % peggio)
    if peggio > 0.999:
        print("  -> la ricostruzione di twn RIPRODUCE perc_chi: la misura 1 vale.")
    else:
        print("  -> *** NON RIPRODUCE: ho ricostruito male, e la lettura di 1 NON VALE. ***")

    # ------------------------------------------------------------------ 3
    print("")
    print("=" * 118)
    print("3) LA PORTATA -- lambda_nodi CHIAMATO DAL CODICE VERO, non ricostruito")
    print("=" * 118)
    print("%-7s %-7s | %-10s %-10s %-9s %-7s | %-8s %-8s %-8s"
          % ("passo", "n", "med(lam)", "rc=3*med", "med(d)", "rc/d", "deg p25", "deg p50", "deg p75"))
    sub = fs[::max(1, len(fs) // 15)]
    if fs[-1] not in sub:
        sub.append(fs[-1])
    for p in sub:
        net = S.Rete(seed=1)
        try:
            net.carica_stato(p)
        except Exception as e:
            print("%-7d  carica_stato RIFIUTA: %s" % (passo_di(p), e))
            continue
        try:
            lam = np.asarray(net.lambda_nodi(), float)
        except Exception as e:
            print("%-7d  lambda_nodi FALLISCE: %s: %s" % (passo_di(p), type(e).__name__, e))
            continue
        med = float(np.median(lam)); rc = 3.0 * med
        d50 = float(np.median(np.asarray(net.d, float))) if len(getattr(net, "d", [])) else float("nan")
        deg = np.asarray(net._deg, float)[:net.n]
        print("%-7d %-7d | %-10.5f %-10.5f %-9.4f %-7.3f | %-8.0f %-8.0f %-8.0f"
              % (passo_di(p), net.n, med, rc, d50, rc / d50 if d50 else float("nan"),
                 pc(deg, 25), pc(deg, 50), pc(deg, 75)))
        del net

    # ------------------------------------------------------------------ 2b
    print("")
    print("=" * 118)
    print("2b) _tau EFFETTIVO -- in QUESTO run e' _tempo_luce_nodo (TAU_LUCE=1), NON TAU_A*(...)")
    print("=" * 118)
    print("%-7s | %-11s %-11s %-11s | %-11s"
          % ("passo", "tau p25", "tau p50", "tau p75", "tau p50 / TAU_A"))
    for p in sub:
        net = S.Rete(seed=1)
        try:
            net.carica_stato(p)
            t = np.asarray(net._tempo_luce_nodo(np.asarray(net.i), np.asarray(net.j)), float)
        except Exception as e:
            print("%-7d  NON CALCOLABILE: %s: %s" % (passo_di(p), type(e).__name__, e))
            del net
            continue
        print("%-7d | %-11.5g %-11.5g %-11.5g | %-11.5g"
              % (passo_di(p), pc(t, 25), pc(t, 50), pc(t, 75), pc(t, 50) / float(S.TAU_A)))
        del net

    # ------------------------------------------------------------------ letture
    print("")
    print("=" * 118)
    print("LE LETTURE, come fissate PRIMA")
    print("=" * 118)
    a, b = righe[0], righe[-1]
    salita = [r["passo"] for r in righe if 0.05 < r["fr1"] < 0.95]
    print("1) fr(+1): da %.4f (passo %d) a %.4f (passo %d)" % (a["fr1"], a["passo"], b["fr1"], b["passo"]))
    print("   snapshot con fr(+1) fra 0.05 e 0.95 (cioe' la TRANSIZIONE): %d su %d  -> %s"
          % (len(salita), len(righe),
             "RIBALTAMENTO NETTO" if len(salita) <= 3 else "TRANSIZIONE GRADUALE"))
    if salita:
        print("   la transizione copre i passi %d - %d" % (min(salita), max(salita)))
    om = [r["om50"] for r in righe]
    cresc = sum(1 for k in range(1, len(om)) if om[k] > om[k - 1])
    print("2) |omega_s| mediana: da %.4g a %.4g (x%.3g). Intervalli in CRESCITA: %d su %d"
          % (om[0], om[-1], om[-1] / om[0] if om[0] else float("inf"), cresc, len(om) - 1))
    print("   -> %s" % ("MONOTONO: e' un CRICCHETTO (A7)" if cresc >= 0.9 * (len(om) - 1)
                        else "NON monotono: %d intervalli scendono" % (len(om) - 1 - cresc)))
    dp = [r["dpav"] for r in righe if np.isfinite(r["dpav"])]
    cre4 = sum(1 for k in range(1, len(dp)) if dp[k] > dp[k - 1])
    print("4) inerzia al pavimento PER INTERVALLO (non cumulata): da %.4f a %.4f, max %.4f"
          % (dp[0], dp[-1], max(dp)))
    print("   intervalli in crescita: %d su %d" % (cre4, len(dp) - 1))
    print("")
    print("UN SEME, UNA SCENA. --tau-luce ha sigillo 6/7. Nessuna identificazione, nessun verdetto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
