# -*- coding: utf-8 -*-
"""LA RIGIOCATA `0 -> 120` DEL RAMO B, campionata a OGNI PASSO. L'ORIGINE, non l'escalation.

Criteri FISSATI PRIMA in `doc/TASK_HISTORY/2026-09-20_rigiocata-0-120.md` (`23834ff`).

*** ⚠ IL SIGILLO INTERNO [BLOCCANTE] -- senza, questa rigiocata non vale niente ***
  La rigiocata deve riprodurre **ESATTAMENTE** il ramo B. Se il ciclo differisse di una chiamata da
  quello del driver, la traiettoria **divergerebbe** e si starebbe misurando **un altro run**.
  **CRITERIO: al passo 120 lo stato deve essere IDENTICO a `_ab_B/scena_000120.pkl.gz`**, campo per
  campo, col criterio `uguale_contenuto` dei sigilli. **Se fallisce, il risultato e' BUTTATO e si
  riporta il fallimento invece di pubblicare i numeri.**

*** IL CICLO SI COPIA DAL DRIVER, NON SI REINVENTA ***
  Da `csv/_test_fork/_scena_video.py`:
      passo_test()  una volta per frame
      poi PASSI_PER_FRAME volte:
          scuoti_vuoto(net) ; net.step() ; net.mitosi() ; net.rilassa_disegno() ; net.memoria_hebbiana_moto()
  E l'argv e' quello del ramo B: `--sep 4.0`, tutti i flag, **SENZA `--chi-basc`**.

*** CADENZA: OGNI PASSO, e il perche' e' un numero ***
  Un passo costa ~4 s, la misura ~2 ms (percentili su array gia' in memoria): **lo 0.05 %**.
  Campionare cinque volte piu' fitto **non si vede nel costo**.
  **Tutte le misure sono PURE READ**: si leggono gli attributi. **Nessuna `diagnostica()`**, che scrive.

*** ⚠ NUMERATORE E DENOMINATORE SEPARATI ***
  `d/d0` puo' salire perche' `d` CRESCE o perche' `d0` CALA: **sono due fenomeni diversi**, e si
  stampano **entrambi**, mai solo il rapporto.

*** COSA NON E' RICOSTRUIBILE, e si dichiara ***
  `n1` e `n2` sono locali di `step` (`src`, `beta`): **non ricostruibili da fuori**. Solo **`n3`**.
ASCII PURO.
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, os.path.join(RADICE, "csv", "_seal_fork"))
os.chdir(RADICE)

CINQUE = [16, 481, 621, 627, 837]
COPPIA = (16, 481)          # l'arco che al 120 e' gia' il piu' teso, e al 240 il peggiore
NPASSI = 120
DT, CS_M = 0.01, 2.0        # dichiarati, per `n3`

# ---- l'argv del RAMO B, copiato dal driver (senza `--chi-basc`)
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--plast-din",
            "--viriale", "--olon-part"]
import soliton_simulator as S

a = S._cli()
S._applica_regime(a)
S._applica_flag(a)
S._NMASSE_VIDEO["n"] = 3
S._NMASSE_VIDEO["sep"] = 4.0
S._NMASSE_VIDEO["size"] = None
print("CHI_BASC dal MODULO (dev'essere False): %s" % S.CHI_BASC)
S.avvia_test("N-MASSE")()
net = S.net
print("semina: n = %d  archi = %d" % (net.n, len(net.i)))
assert net.n == 2391, "n alla semina e' %d, non 2391: NON e' la stessa scena" % net.n


def arco(i0, j0):
    """l'indice dell'arco (i0,j0) CERCATO PER COPPIA DI NODI, non per posizione"""
    ii = np.asarray(net.i); jj = np.asarray(net.j)
    s = ((ii == i0) & (jj == j0)) | ((ii == j0) & (jj == i0))
    k = np.flatnonzero(s)
    return int(k[0]) if len(k) else -1


def rango(v, x):
    return 100.0 * float(np.mean(np.asarray(v) < x))


def misura(passo):
    d = np.asarray(net.d); d0 = np.asarray(net.d0); vd = np.abs(np.asarray(net.vd))
    ii = np.asarray(net.i); jj = np.asarray(net.j)
    m = min(len(d), len(d0), len(vd), len(ii), len(jj))
    d, d0, vd, ii, jj = d[:m], d0[:m], vd[:m], ii[:m], jj[:m]
    rap = d / np.maximum(d0, 1e-12)
    n = net.n
    dg = np.asarray(net._deg)[:n]
    pv = np.abs(np.asarray(net.phivel))[:n]
    k = arco(*COPPIA)
    r = dict(passo=passo, n=n, archi=m,
             # la POPOLAZIONE
             pd50=float(np.median(rap)), pd99=float(np.percentile(rap, 99)), pdmax=float(rap.max()),
             pv50=float(np.median(vd)), pv99=float(np.percentile(vd, 99)), pvmax=float(vd.max()),
             pd0=float(np.median(d0)), pdd=float(np.median(d)),
             n3=float(np.ceil(vd.max() * DT / (0.1 * max(float(np.median(d)), 0.1)))),
             # L'ARCO 16-481: numeratore e denominatore SEPARATI
             k=k, ad=float(d[k]) if k >= 0 else np.nan,
             ad0=float(d0[k]) if k >= 0 else np.nan,
             arap=float(rap[k]) if k >= 0 else np.nan,
             avd=float(vd[k]) if k >= 0 else np.nan)
    for x in CINQUE:
        s = (ii == x) | (jj == x)
        r["deg_%d" % x] = int(dg[x])
        r["pv_%d" % x] = float(pv[x])
        r["pvr_%d" % x] = rango(pv, pv[x])
        r["rap50_%d" % x] = float(np.median(rap[s])) if s.any() else np.nan
        r["rapmax_%d" % x] = float(rap[s].max()) if s.any() else np.nan
        r["vdmax_%d" % x] = float(vd[s].max()) if s.any() else np.nan
    return r


def geometria():
    """par.2 del mandato: i cinque sono i piu' connessi PERCHE' stanno al centro?"""
    n = net.n
    pos = np.asarray(net.pos)[:n]
    dg = np.asarray(net._deg)[:n]
    bar = pos.mean(axis=0)
    r = np.linalg.norm(pos - bar, axis=1)
    print("")
    print("--- par.2  LA GEOMETRIA ALLA SEMINA: `_deg` e' la distanza dal baricentro? ---")
    print("  baricentro = [%.3f %.3f %.3f]   |r| p50 %.4g  p99 %.4g  max %.4g"
          % (bar[0], bar[1], bar[2], np.median(r), np.percentile(r, 99), r.max()))
    cc = float(np.corrcoef(r, dg)[0, 1])
    print("  CORRELAZIONE fra distanza dal baricentro e `_deg`, su tutti i %d nodi: %+.4f" % (n, cc))
    print("  (il NULLO per variabili indipendenti su n=%d e' ~1/sqrt(n) = %.4f; 3 sigma = %.4f)"
          % (n, 1.0 / np.sqrt(n), 3.0 / np.sqrt(n)))
    print("  %-7s %10s %10s %10s %10s" % ("nodo", "|r|", "rango |r|", "_deg", "rango deg"))
    for x in CINQUE:
        print("  %-7d %10.4g %9.1f%% %10d %9.1f%%"
              % (x, r[x], rango(r, r[x]), dg[x], rango(dg, dg[x])))
    # e i nodi PIU connessi in assoluto: dove stanno?
    top = np.argsort(-dg)[:20]
    print("  i 20 nodi PIU' connessi: |r| p50 %.4g (contro %.4g di tutti) -> rango medio %.1f%%"
          % (np.median(r[top]), np.median(r), np.mean([rango(r, r[q]) for q in top])))


def main():
    geometria()
    print("")
    print("--- LA SERIE `0 -> %d`, campionata a OGNI PASSO ---" % NPASSI)
    print("  arco %d-%d: si segue per COPPIA DI NODI. Indice alla semina: %d"
          % (COPPIA[0], COPPIA[1], arco(*COPPIA)))
    print("")
    print("  %-6s %-6s | %9s %9s %9s %9s | %8s %8s %8s | %6s %8s"
          % ("passo", "n", "16-481 d", "16-481 d0", "d/d0", "|vd|",
             "pop d/d0", "pop |vd|", "pop d0", "n3", "pop dmax"))
    S.stato["nframe"] = 0
    serie = [misura(0)]
    r = serie[0]
    print("  %-6d %-6d | %9.4g %9.4g %9.4g %9.4g | %8.4g %8.4g %8.4g | %6.0f %8.4g"
          % (0, r["n"], r["ad"], r["ad0"], r["arap"], r["avd"],
             r["pd50"], r["pv50"], r["pd0"], r["n3"], r["pdmax"]))
    t0 = time.time()
    passo = 0
    for fr in range(NPASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step(); net.mitosi()
            net.rilassa_disegno(); net.memoria_hebbiana_moto()
            passo += 1
            r = misura(passo)
            serie.append(r)
            if passo % 5 == 0 or passo <= 3:
                print("  %-6d %-6d | %9.4g %9.4g %9.4g %9.4g | %8.4g %8.4g %8.4g | %6.0f %8.4g"
                      % (passo, r["n"], r["ad"], r["ad0"], r["arap"], r["avd"],
                         r["pd50"], r["pv50"], r["pd0"], r["n3"], r["pdmax"]), flush=True)
        S.stato["nframe"] += 1
    print("  [%d passi in %.1f s = %.2f s/passo]" % (passo, time.time() - t0,
                                                     (time.time() - t0) / max(passo, 1)))

    # ---- i cinque, ogni 10 passi
    print("")
    print("--- I CINQUE: `_deg`, `phivel` (col rango), e la tensione dei loro archi ---")
    print("  %-6s | %s" % ("passo", " | ".join("%-28s" % ("nodo %d: deg  pv(rango) d/d0max" % x)
                                               for x in CINQUE[:3])))
    for r in serie:
        if r["passo"] % 10:
            continue
        pezzi = []
        for x in CINQUE[:3]:
            pezzi.append("%4d %6.1f(p%4.1f) %7.4g"
                         % (r["deg_%d" % x], r["pv_%d" % x], r["pvr_%d" % x], r["rapmax_%d" % x]))
        print("  %-6d | %s" % (r["passo"], " | ".join(pezzi)))

    # ---- IL SIGILLO INTERNO [BLOCCANTE]
    print("")
    print("=" * 118)
    print("SIGILLO INTERNO [BLOCCANTE]: la rigiocata riproduce il ramo B?")
    print("=" * 118)
    import gzip, pickle
    from _sigillo_archivio import uguale_contenuto
    with gzip.open("csv/_test_fork/_ab_B/scena_000120.pkl.gz", "rb") as f:
        rif = pickle.load(f)["attrs"]
    mio = {}
    for kk, vv in net.__dict__.items():
        if kk == "rng":
            continue
        if isinstance(vv, (np.ndarray, int, float, bool, np.integer, np.floating, str)):
            mio[kk] = vv
    com = sorted(set(rif) & set(mio))
    diff = [kk for kk in com if not uguale_contenuto(rif[kk], mio[kk])]
    print("  campi confrontati: %d   DIVERSI: %d" % (len(com), len(diff)))
    if diff:
        print("  *** FALLITO. Primi diversi: %s ***" % diff[:8])
        print("  *** LA RIGIOCATA NON RIPRODUCE IL RAMO B: i numeri qui sopra NON VALGONO. ***")
        return 1
    print("  PASS -- %d campi IDENTICI. La rigiocata E' il ramo B, e la serie vale." % len(com))
    print("  (e lo zero non e' mancanza di confronto: %d campi confrontati, n=%d in entrambi)"
          % (len(com), net.n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
