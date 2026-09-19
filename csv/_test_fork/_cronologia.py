# -*- coding: utf-8 -*-
"""LA CRONOLOGIA DELLA DEGENERAZIONE -- chi si muove per primo, sui 45 snapshot.

Letture e soglie FISSATE PRIMA: doc/TASK_HISTORY/2026-09-19_cronologia-degenerazione.md (8def0af).
NESSUN RUN. NESSUNA CURA. Si legge, uno snapshot alla volta.

IL PUNTO DI ATTRAVERSAMENTO, definito prima di aver visto un numero:
    t50(X) = primo passo in cui X >= sqrt(min*max)   se min > 0     (meta' dell'escursione in LOG)
                                      (min+max)/2    altrimenti
La scala LOG non e' un vezzo: omega_s va da 0 a 1e5, d0 da 1 a 400. Con soglia LINEARE il t50 di
una grandezza che cresce di cinque ordini cadrebbe SEMPRE alla fine, e l'ordine sarebbe un
ARTEFATTO DELLA SCALA.

LE QUATTRO LETTURE
  A EVENTO       tutti i t50 entro 2 snapshot (120 passi)
  B UNA PRECEDE  il t50 minimo almeno 3 snapshot (180 passi) prima del secondo
  C GRADUALE     ogni grandezza supera il 10 % dell'escursione entro i primi 3 snapshot E nessun
                 intervallo singolo ne porta piu' del 30 %
  D NESSUNA      si riporta cosi', senza inventarne una quinta

DUE SOGLIE DERIVATE DAL CODICE, non scelte:
  il TETTO di ritmo() e' sqrt(2) (:2122-2124), il PAVIMENTO sqrt(2)*1e-6 -- ed e' esattamente
  l'1.414213e-06 che Z46 aveva misurato. Il GRADO DI NASCITA e' 2.
  Datare "_deg p50 = 2" e "_r_corrente p75 = tetto" e' datare un evento STRUTTURALE.

A3c: le distribuzioni bimodali si riportano coi PERCENTILI, mai con una mediana da sola.
UN SEME, UNA SCENA. --tau-luce sigillo 6/7.
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

ARCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join("csv", "_test_fork", "_g6000")
TETTO = math.sqrt(2.0)            # DERIVATO da ritmo(), non scelto
PAVIMENTO = math.sqrt(2.0) * 1e-6
GRADO_NASCITA = 2                 # DERIVATO: il figlio nasce con due archi verso i genitori


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def passo_di(p):
    return int(re.search(r"_(\d{6})\.", p).group(1))


def pc(v, q):
    a = np.asarray(v, float).ravel()
    a = a[np.isfinite(a)]
    return float(np.percentile(a, q)) if a.size else float("nan")


def norma(v):
    a = np.asarray(v, float)
    return np.linalg.norm(a, axis=1) if a.ndim > 1 else np.abs(a)


def t50(passi, val):
    """Il punto di attraversamento, con la regola fissata PRIMA."""
    x = np.asarray(val, float)
    ok = np.isfinite(x)
    if not ok.any():
        return None, float("nan"), "tutti non finiti"
    x = x[ok]; p = np.asarray(passi)[ok]
    lo, hi = float(x.min()), float(x.max())
    if hi <= lo:
        return None, float("nan"), "costante"
    if lo > 0:
        soglia = math.sqrt(lo * hi); scala = "log"
    else:
        soglia = 0.5 * (lo + hi); scala = "lineare (min<=0)"
    k = np.argmax(x >= soglia)
    return int(p[k]), soglia, scala


def main():
    fs = sorted(glob.glob(os.path.join(ARCH, "scena_??????.pkl*")))
    print("snapshot: %d, passi %d-%d, cadenza %d"
          % (len(fs), passo_di(fs[0]), passo_di(fs[-1]),
             passo_di(fs[1]) - passo_di(fs[0]) if len(fs) > 1 else 0))
    print("soglie DERIVATE: tetto di ritmo() = %.8f   pavimento = %.3e   grado di nascita = %d"
          % (TETTO, PAVIMENTO, GRADO_NASCITA))
    print("")

    R = []
    for p in fs:
        at = carica(p)["attrs"]
        n = len(at["eta"])
        om = norma(at["omega_s"])
        d0 = np.asarray(at["d0"], float)
        fcs = np.asarray(at.get("_fatt_cs_ultimo", []), float)
        r = np.asarray(at.get("_r_corrente", []), float)
        r = r[np.isfinite(r)]
        deg = np.asarray(at["_deg"], float)[:n]
        peq = np.asarray(at["peq"], float)
        tw = np.abs(np.asarray(at["tw"], float))
        pav = at.get("_inerzia_al_pavimento", 0); tot = at.get("_inerzia_tot", 1)
        R.append(dict(
            passo=passo_di(p), n=n, archi=len(at["i"]), nati=at.get("nati", 0),
            om50=pc(om, 50), om95=pc(om, 95), ommax=float(om.max()),
            d050=pc(d0, 50), d095=pc(d0, 95), d0max=float(d0.max()),
            fcs50=pc(fcs, 50) if fcs.size else float("nan"),
            fcsmax=float(fcs.max()) if fcs.size else float("nan"),
            r25=pc(r, 25) if r.size else float("nan"), r50=pc(r, 50) if r.size else float("nan"),
            r75=pc(r, 75) if r.size else float("nan"),
            deg25=pc(deg, 25), deg50=pc(deg, 50), deg75=pc(deg, 75),
            peq50=pc(peq, 50), peqmax=float(peq.max()),
            tw50=pc(tw, 50), twmax=float(tw.max()),
            pav=pav, tot=tot))
        del at

    print("=" * 132)
    print("LA CRONOLOGIA")
    print("=" * 132)
    print("%-6s %-6s %-7s %-6s | %-9s %-9s | %-8s %-8s | %-7s %-7s | %-6s %-6s %-6s | %-5s %-5s %-6s"
          % ("passo", "n", "archi", "nati", "om p50", "om max", "d0 p50", "d0 max",
             "fcs p50", "fcs max", "r p25", "r p50", "r p75", "dg25", "dg50", "dg75"))
    for x in R:
        print("%-6d %-6d %-7d %-6d | %-9.3g %-9.3g | %-8.3g %-8.3g | %-7.4g %-7.4g | %-6.4f %-6.4f %-6.4f | %-5.0f %-5.0f %-6.0f"
              % (x["passo"], x["n"], x["archi"], x["nati"], x["om50"], x["ommax"],
                 x["d050"], x["d0max"], x["fcs50"], x["fcsmax"],
                 x["r25"], x["r50"], x["r75"], x["deg25"], x["deg50"], x["deg75"]))

    passi = [x["passo"] for x in R]
    GRAND = [("omega_s p50", [x["om50"] for x in R]), ("omega_s max", [x["ommax"] for x in R]),
             ("d0 p50", [x["d050"] for x in R]), ("d0 max", [x["d0max"] for x in R]),
             ("fatt_cs max", [x["fcsmax"] for x in R]),
             ("peq p50", [x["peq50"] for x in R]), ("tw max", [x["twmax"] for x in R]),
             ("r p75", [x["r75"] for x in R]),
             ("inerzia pav/tot", [x["pav"] / max(x["tot"], 1) for x in R])]

    print("")
    print("=" * 132)
    print("I PUNTI DI ATTRAVERSAMENTO  t50  (regola fissata PRIMA: meta' escursione, in LOG se min>0)")
    print("=" * 132)
    print("%-18s %-10s %-12s %-12s %-12s %-10s" % ("grandezza", "t50", "soglia", "min", "max", "scala"))
    tab = []
    for nome, v in GRAND:
        t, s, sc = t50(passi, v)
        a = np.asarray(v, float); a = a[np.isfinite(a)]
        print("%-18s %-10s %-12.4g %-12.4g %-12.4g %-10s"
              % (nome, t if t is not None else "-", s, a.min() if a.size else float("nan"),
                 a.max() if a.size else float("nan"), sc))
        if t is not None:
            tab.append((t, nome))

    print("")
    print("=" * 132)
    print("GLI EVENTI STRUTTURALI (soglie DERIVATE dal codice, non scelte)")
    print("=" * 132)
    ev = []
    k = next((x["passo"] for x in R if x["deg50"] <= GRADO_NASCITA), None)
    print("  _deg p50 scende al GRADO DI NASCITA (%d): passo %s" % (GRADO_NASCITA, k))
    if k: ev.append((k, "_deg p50 = grado di nascita"))
    k = next((x["passo"] for x in R if x["deg25"] <= GRADO_NASCITA), None)
    print("  _deg p25 scende al grado di nascita:     passo %s" % k)
    if k: ev.append((k, "_deg p25 = grado di nascita"))
    k = next((x["passo"] for x in R if x["r75"] >= TETTO - 1e-9), None)
    print("  _r_corrente p75 raggiunge il TETTO sqrt(2): passo %s" % k)
    if k: ev.append((k, "r p75 = tetto"))
    k = next((x["passo"] for x in R if x["r50"] >= TETTO - 1e-9), None)
    print("  _r_corrente p50 raggiunge il tetto:      passo %s" % k)
    if k: ev.append((k, "r p50 = tetto"))
    k = next((x["passo"] for x in R if x["r25"] <= PAVIMENTO * 10), None)
    print("  _r_corrente p25 scende verso il PAVIMENTO: passo %s" % k)

    print("")
    print("=" * 132)
    print("IL VERDETTO, secondo le quattro letture fissate PRIMA")
    print("=" * 132)
    tab.sort()
    print("  ordine cronologico dei t50:")
    for t, nome in tab:
        print("     passo %-8d %s" % (t, nome))
    if not tab:
        print("  NESSUN t50 calcolabile -> lettura D")
        return 0
    primo, ultimo = tab[0][0], tab[-1][0]
    cad = passi[1] - passi[0]
    span = (ultimo - primo) / cad
    secondo = next((t for t, _ in tab if t > primo), primo)
    ritardo = (secondo - primo) / cad
    print("")
    print("  finestra dei t50: dal passo %d al %d  = %.0f snapshot" % (primo, ultimo, span))
    print("  ritardo fra il PRIMO e il SECONDO: %.0f snapshot (%d passi)" % (ritardo, secondo - primo))
    # C: gradualita'
    grad_ok, dett = True, []
    for nome, v in GRAND:
        a = np.asarray(v, float)
        ok = np.isfinite(a)
        if ok.sum() < 4:
            continue
        a = a[ok]
        lo, hi = a.min(), a.max()
        if hi <= lo:
            continue
        fr = (a - lo) / (hi - lo)
        primo10 = fr[:3].max() >= 0.10
        salto = float(np.max(np.diff(fr)))
        if not (primo10 and salto <= 0.30):
            grad_ok = False
            dett.append("%s (10%% nei primi 3: %s, salto max %.2f)" % (nome, primo10, salto))
    print("")
    if span <= 2:
        print("  -> LETTURA A: E' UN EVENTO. Tutti i t50 entro %d snapshot." % span)
        print("     Si DATA al passo %d e si va a vedere cosa accade li' (rigiocata, §4)." % primo)
    elif ritardo >= 3:
        print("  -> LETTURA B: UNA PRECEDE LE ALTRE di %.0f snapshot (%d passi)." % (ritardo, secondo - primo))
        print("     CANDIDATA CAUSA: %s (t50 = passo %d)." % (tab[0][1], primo))
    elif grad_ok:
        print("  -> LETTURA C: GRADUALE FIN DAL PRIMO SNAPSHOT.")
        print("     NON c'e' una transizione: il sistema era GIA' COSI', e il blocco e' solo il")
        print("     punto in cui i numeri diventano impraticabili. IL DIFETTO E' NELLA FORMA DELLE")
        print("     LEGGI, non in un evento.")
    else:
        print("  -> LETTURA D: NESSUNA DELLE TRE.")
        print("     span %.0f snapshot (A vuole <=2), ritardo %.0f (B vuole >=3), gradualita' NO:"
              % (span, ritardo))
        for d in dett[:6]:
            print("        %s" % d)
        print("     Si riporta COSI', senza inventarne una quinta.")
    print("")
    print("UN SEME, UNA SCENA. --tau-luce sigillo 6/7. Nessuna identificazione, nessun verdetto di fisica.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
