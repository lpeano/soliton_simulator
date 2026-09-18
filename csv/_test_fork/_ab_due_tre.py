# -*- coding: utf-8 -*-
"""A/B **A VARIABILE SINGOLA** su `--nmasse`: TRE masse (`_gvideo`, `Z49`) contro DUE (`_g2m`).

Predizione di Luca committata PRIMA del run: `a4fbe42` (`doc/PREVISIONI_qualitative.md`).
Le TRE letture e i TRE falsificatori sono fissati **li'**, non qui.

IN TESTA, NON IN FONDO:
  * `--tau-luce` HA IL SIGILLO FALLITO (CLAUDE.md par.0): ENTRAMBI i bracci girano su un ramo
    NON CERTIFICATO, e ogni numero lo eredita;
  * `--chi-basc` attivo in entrambi: `perc_chi` non e' un'etichetta di lignaggio;
  * UN SEME PER BRACCIO. NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.
  * E' un A/B su `--nmasse`, NON su "tre corpi": numero di masse, POPOLAZIONE e geometria della
    semina cambiano INSIEME. Le cause non sono separate, ed e' un limite di PROGETTO.

La regione interna e' `r < R_anello(t)/2` con `R_anello(t)` MISURATO (mediana del raggio dei nodi
seminati a `t = 0`), piu' la lettura ASSOLUTA `r < 4` -- si riportano ENTRAMBE (par.4).
ASCII PURO.
"""
import glob
import os
import pickle
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
PPF = 6
DT = 0.02
R_FLOOR = 1e-6 / (1.0 / np.sqrt(2.0) + 1e-6)
BRACCI = [("TRE  (Z49)", os.path.join("csv", "_test_fork", "_gvideo")),
          ("DUE  (ctrl)", os.path.join("csv", "_test_fork", "_g2m"))]


def leggi(D):
    S = {}
    for p in sorted(glob.glob(os.path.join(D, "frame_*.pkl"))):
        a = pickle.load(open(p, "rb"))["attrs"]
        S[int(a.get("_db_step", -1))] = a
    F = sorted(S)
    n0 = len(S[F[0]]["pos"])
    out = {}
    for f in F:
        a = S[f]
        n = len(a["pos"])
        P = np.asarray(a["pos"])[:n]
        R = np.linalg.norm(P[:, :2], axis=1)
        ra = float(np.median(R[:n0]))
        dd = np.asarray(a.get("d", np.zeros(0)), float)
        out[f] = dict(n=n, R=R, ra=ra,
                      rho=np.asarray(a.get("rho_spin", np.full(n, np.nan)), float)[:n],
                      psi=np.abs(np.asarray(a.get("psi", np.zeros(n, complex)))[:n]),
                      eta=np.asarray(a.get("eta", np.zeros(n)), float)[:n],
                      nb=np.asarray(a.get("_nb", np.zeros((n, 3))), float)[:n],
                      chi=np.asarray(a.get("perc_chi", np.zeros(n, int)))[:n],
                      dmed=float(np.median(dd)) if dd.size else np.nan,
                      p95=float(np.percentile(R, 95)))
    return F, n0, out


D = {}
for et, dd in BRACCI:
    D[et] = leggi(dd)

print("=" * 122)
print("A/B SU --nmasse: TRE MASSE (Z49) CONTRO DUE. La predizione di Luca e' in a4fbe42, PRIMA del run.")
print("=" * 122)
print("  PRESIDI, IN TESTA:")
print("    * --tau-luce HA IL SIGILLO FALLITO (par.0): ENTRAMBI i bracci su ramo NON CERTIFICATO;")
print("    * --chi-basc attivo in entrambi; UN SEME per braccio; nessuna identificazione;")
print("    * A/B su --nmasse, NON su 'tre corpi': masse, POPOLAZIONE e geometria cambiano INSIEME.")

F = D[BRACCI[0][0]][0]
assert F == D[BRACCI[1][0]][0], "gli istanti non coincidono: il confronto non si fa"

# ----------------------------------------------------- falsificatore 1: la popolazione
print("")
print("--- FALSIFICATORE 1 (fissato PRIMA): la POPOLAZIONE e' confrontabile? ---")
n3 = D[BRACCI[0][0]][1]
n2 = D[BRACCI[1][0]][1]
print("  n0 TRE = %d   n0 DUE = %d   atteso proporzionale 2/3 = %.0f   MISURATO = %.1f %% (non il 66.7 %%)"
      % (n3, n2, n3 * 2.0 / 3.0, 100.0 * n2 / n3))

# ----------------------------------------------------- falsificatore 2: R_anello aliasing
print("")
print("--- FALSIFICATORE 2 (fissato PRIMA): R_anello varia piu' dell'8 %% -> lettura ASSOLUTA aliasata ---")
for et, _ in BRACCI:
    Ff, _, S = D[et]
    ra = np.array([S[f]["ra"] for f in Ff])
    print("  %-12s R_anello %s   escursione (max-min)/min = %.1f %%"
          % (et, " ".join("%.3f" % v for v in ra), 100.0 * (ra.max() - ra.min()) / ra.min()))
print("  -> si riportano ENTRAMBE le letture, e la COMOVENTE e' quella che decide se divergono.")

# ----------------------------------------------------- LA CURVA CHE DECIDE
for eti, com in (("ASSOLUTA  (r < 4)", False), ("COMOVENTE (r < R_anello(t)/2)", True)):
    print("")
    print("--- LA CURVA CHE DECIDE -- nodi(regione interna), lettura %s ---" % eti)
    print("  %-13s %-8s %-8s %-8s %-8s %-8s %-8s | %-9s %-9s"
          % ("braccio", "f10", "f115", "f190", "f270", "f375", "f400", "min/f10", "f400/min"))
    for et, _ in BRACCI:
        Ff, _, S = D[et]
        v = []
        for f in Ff:
            c = S[f]
            lim = c["ra"] / 2.0 if com else 4.0
            v.append(int((c["R"] < lim).sum()))
        v = np.array(v, float)
        print("  %-13s %-8d %-8d %-8d %-8d %-8d %-8d | %-9.4f %-9.4f"
              % (et, v[0], v[1], v[2], v[3], v[4], v[5], v.min() / v[0], v[-1] / v.min()))
    print("  (frazione sulla popolazione n dello stesso istante)")
    for et, _ in BRACCI:
        Ff, _, S = D[et]
        fr = []
        for f in Ff:
            c = S[f]
            lim = c["ra"] / 2.0 if com else 4.0
            fr.append((c["R"] < lim).sum() / float(c["n"]))
        print("  %-13s %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f %-8.4f" % tuple([et] + fr))

# ----------------------------------------------------- l'ACCENSIONE
print("")
print("--- L'ACCENSIONE (falsificatore 3: ciclo SI ma rho_spin NON si accende?) -- interna COMOVENTE ---")
for gr, nome in (("rho", "rho_spin med"), ("psi", "|psi| med")):
    print("  %-13s %-11s %-11s %-11s %-11s %-11s %-11s | escursione"
          % (nome, "f10", "f115", "f190", "f270", "f375", "f400"))
    for et, _ in BRACCI:
        Ff, _, S = D[et]
        v = []
        for f in Ff:
            c = S[f]
            m = c["R"] < c["ra"] / 2.0
            v.append(float(np.median(c[gr][m])) if m.sum() >= 5 else np.nan)
        v = np.array(v)
        print("  %-13s %-11.4e %-11.4e %-11.4e %-11.4e %-11.4e %-11.4e | x%.4g"
              % (et, v[0], v[1], v[2], v[3], v[4], v[5], np.nanmax(v) / np.nanmin(v)))
    A = []
    for et, _ in BRACCI:
        Ff, _, S = D[et]
        c = S[Ff[-1]]
        m = c["R"] < c["ra"] / 2.0
        A.append(float(np.median(c[gr][m])))
    print("    -> RAPPORTO TRE/DUE all'ultimo istante: x%.4g" % (A[0] / A[1]))

# ----------------------------------------------------- le stesse grandezze di Z49
print("")
print("--- LE STESSE GRANDEZZE DI Z49, AGLI STESSI ISTANTI ---")
print("  %-13s %-7s %-8s %-10s %-10s %-10s %-11s %-10s"
      % ("braccio", "frame", "n", "d MEDIANO", "R_anello", "R p95", "coer|<nb>|", "frac +1"))
for et, _ in BRACCI:
    Ff, _, S = D[et]
    for f in Ff:
        c = S[f]
        print("  %-13s %-7d %-8d %-10.5f %-10.5f %-10.5f %-11.5f %-10.5f"
              % (et, f, c["n"], c["dmed"], c["ra"], c["p95"],
                 float(np.linalg.norm(np.mean(c["nb"], axis=0))), float(np.mean(c["chi"] > 0))))
    print("")

# ----------------------------------------------------- `r` ricavato: interna contro anello
print("--- r RICAVATO da eta += DT*r (il discriminante di Z46) -- interna COMOVENTE contro ANELLO ---")
print("  %-13s %-14s %-14s %-14s %-14s"
      % ("braccio", "intervallo", "r INTERNA", "r ANELLO", "r int / r_floor"))
for et, _ in BRACCI:
    Ff, _, S = D[et]
    for k in range(len(Ff) - 1):
        f0, f1 = Ff[k], Ff[k + 1]
        c0, c1 = S[f0], S[f1]
        nn = min(c0["n"], c1["n"])
        de = (c1["eta"][:nn] - c0["eta"][:nn]) / (DT * (f1 - f0) * PPF)
        R1 = c1["R"][:nn]
        ra = c1["ra"]
        mi = R1 < ra / 2.0
        ma = (R1 >= 0.75 * ra) & (R1 < 1.25 * ra)
        ri = float(np.median(de[mi])) if mi.sum() >= 5 else np.nan
        print("  %-13s %-14s %-14.6e %-14.6e %-14.1f"
              % (et, "%d->%d" % (f0, f1), ri,
                 float(np.median(de[ma])) if ma.sum() >= 5 else np.nan, ri / R_FLOOR))
    print("")
print("  (Z46: i nodi fermi avevano r/r_floor = 1.0000. Qui vale ~1e6 in ENTRAMBI i bracci:")
print("   la regione interna NON e' ferma, e il discriminante di Z46 NON scatta ne' a due ne' a tre.)")
print("=" * 122)
