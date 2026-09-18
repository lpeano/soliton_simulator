# -*- coding: utf-8 -*-
"""LA STRUTTURA CHE SI GONFIA E SI RICOMPRIME -- le tre misure, dai `.pkl` della scena VIDEO.

Progettazione: doc/TASK_HISTORY/2026-09-18_struttura-che-si-gonfia.md
Previsioni QUALITATIVE scritte PRIMA: doc/PREVISIONI_qualitative.md (515ed53). **NESSUNA CURA.**

⚠ IN TESTA, NON IN FONDO:
  * **`--tau-luce` HA IL SIGILLO FALLITO** (CLAUDE.md par.0): la scena include una legge **NON
    CERTIFICATA**, e OGNI numero di questa misura lo eredita;
  * **`--chi-basc` attivo**: `perc_chi` non e' un'etichetta di lignaggio;
  * **UN SEME, UNA SCENA.** **NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.**

⚠ E LA RISERVA DEL TASK HISTORY, APPLICATA: i raggi `4 / 8 / 12` sono ASSOLUTI, ma il sistema
DILATA e poi si RICOMPRIME (`d medio` quasi x2). CLAUDE.md par.4: *«mai confronti a passo fisso su un
sistema che si espande: genera ALIASING; normalizza sulla scala COMOVENTE»*.
**Si riportano ENTRAMBE le letture**, e la comovente usa **`R_anello(t)` MISURATO** — il raggio
mediano dei nodi seminati a `t = 0` (indice < n0) **a quell'istante** — non il `sep = 8` di semina.

1 PROFILO RADIALE: `rho_spin`, `|psi|`, coerenza `|<nb>|`, `eta`, `d_nodo`, GRADO, e IL CONTEGGIO.
2 IL CICLO: `d medio` ai sei istanti; il RAGGIO della regione interna sopra soglia -- cresce,
  ingloba l'anello, si ritrae?
3 DI COSA E' FATTA: `eta` interna contro anello; **quanti NATI DOPO** (indice >= n0: esatto);
  `perc_chi` nel tempo.
  ⚠ LIMITE DICHIARATO: la separazione *«assegnato dalla MITOSI»* contro *«riscritto da `chi_basc`»*
  **NON e' ricavabile dai `.pkl`**: servirebbero contatori DURANTE il run. Si riporta il NETTO, e la
  separazione resta da fare con una corsa strumentata.
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
D = os.path.join("csv", "_test_fork", "_gvideo")
PPF = 6
NB = 30
R_FLOOR = 1e-6 / (1.0 / np.sqrt(2.0) + 1e-6)

print("=" * 118)
print("LA STRUTTURA CHE SI GONFIA E SI RICOMPRIME -- i numeri e la forma. NESSUN VERDETTO.")
print("=" * 118)
print("""  ⚠ PRESIDI, IN TESTA:
    * `--tau-luce` HA IL SIGILLO FALLITO (par.0): ramo NON CERTIFICATO, ogni numero lo eredita;
    * `--chi-basc` attivo: `perc_chi` non e' un'etichetta di lignaggio;
    * UN SEME, UNA SCENA. Nessun verdetto di fisica, nessuna identificazione.""")

S = {}
for p in sorted(glob.glob(os.path.join(D, "frame_*.pkl"))):
    a = pickle.load(open(p, "rb"))["attrs"]
    S[int(a.get("_db_step", -1))] = a
F = sorted(S)
N0 = len(S[F[0]]["pos"])
print("\n  istanti (FRAME; il passo di motore e' frame*%d): %s" % (PPF, F))
for f in F:
    print("    frame %-5d = passo %-6d  n = %d" % (f, f * PPF, len(S[f]["pos"])))
print("  n0 (nodi presenti al primo istante) = %d  -> indice >= n0 significa NATO DOPO" % N0)


def campi(f):
    a = S[f]; n = len(a["pos"])
    P = np.asarray(a["pos"])[:n]
    R = np.linalg.norm(P[:, :2], axis=1)
    ps = np.asarray(a.get("psi", np.zeros(n, complex)))[:n]
    rs = np.asarray(a.get("rho_spin", np.full(n, np.nan)), float)[:n]
    nb = np.asarray(a.get("_nb", np.zeros((n, 3))), float)[:n]
    et = np.asarray(a.get("eta", np.zeros(n)), float)[:n]
    ch = np.asarray(a.get("perc_chi", np.zeros(n, int)))[:n]
    ii = np.asarray(a.get("i", np.zeros(0, int))); jj = np.asarray(a.get("j", np.zeros(0, int)))
    dd = np.asarray(a.get("d", np.zeros(0)), float)
    gr = np.zeros(n); dn = np.full(n, np.nan)
    if ii.size and dd.size == ii.size:
        m = (ii < n) & (jj < n)
        gr = (np.bincount(ii[m], minlength=n) + np.bincount(jj[m], minlength=n)).astype(float)
        sm = (np.bincount(ii[m], weights=dd[m], minlength=n) +
              np.bincount(jj[m], weights=dd[m], minlength=n))
        dn = sm / np.maximum(gr, 1.0)
    return dict(n=n, R=R, psi=np.abs(ps), rho=rs, nb=nb, eta=et, chi=ch, grado=gr,
                dnodo=dn, dmed=float(np.median(dd)) if dd.size else np.nan)


C = {f: campi(f) for f in F}
# R_anello MISURATO: raggio mediano dei nodi seminati a t=0 (indice < N0), a OGNI istante
RA = {f: float(np.median(C[f]["R"][:N0])) for f in F}
print("\n  ⚠ R_anello MISURATO (mediana del raggio dei nodi seminati a t=0), per la lettura COMOVENTE:")
for f in F:
    print("    frame %-5d R_anello = %-8.4f   (a t=0 la semina e' a sep = 8)" % (f, RA[f]))

# ------------------------------------------------------------------ 2: il ciclo (prima: e' la firma)
print("\n--- (2) IL CICLO: `d medio` e il raggio della nube ---")
print("  %-8s %-8s %-10s %-12s %-12s %-12s %-12s"
      % ("frame", "passo", "n", "d MEDIANO", "R_anello", "R p95 nube", "coer |<nb>|"))
for f in F:
    c = C[f]
    print("  %-8d %-8d %-10d %-12.5f %-12.5f %-12.5f %-12.5f"
          % (f, f * PPF, c["n"], c["dmed"], RA[f], np.percentile(c["R"], 95),
             float(np.linalg.norm(np.mean(c["nb"], axis=0)))))
print("  (la tabella dei fotogrammi dava d medio 0.934 / 1.454 / 1.676 / 1.753 / 1.483 ai frame")
print("   10 / 115 / 190 / 270 / 375: SI CONFRONTA LA FORMA, e questi sono LO STESSO RUN.)")

# ------------------------------------------------------------------ 1: profilo radiale
print("\n--- (1) IL PROFILO RADIALE -- ASSOLUTO e COMOVENTE ---")
for f in F:
    c = C[f]; R = c["R"]; ra = RA[f]
    print("\n  frame %-5d (passo %-6d, n = %-6d, R_anello = %.3f)" % (f, f * PPF, c["n"], ra))
    print("    %-9s %-9s %-8s %-11s %-11s %-11s %-11s %-9s"
          % ("r ASS", "r/R_an", "nodi", "rho_spin", "|psi|", "eta med", "d_nodo", "grado"))
    bordi = np.linspace(0.0, float(np.percentile(R, 99)), NB + 1)
    for b in range(NB):
        m = (R >= bordi[b]) & (R < bordi[b + 1])
        if m.sum() < 5:
            continue
        rc = 0.5 * (bordi[b] + bordi[b + 1])
        print("    %-9.3f %-9.3f %-8d %-11.4e %-11.4e %-11.4g %-11.4g %-9.4g"
              % (rc, rc / ra, int(m.sum()), np.median(c["rho"][m]), np.median(c["psi"][m]),
                 np.median(c["eta"][m]), np.nanmedian(c["dnodo"][m]), np.median(c["grado"][m])))

# ------------------------------------------------------------------ le tre regioni
print("\n--- LE TRE REGIONI -- ASSOLUTE (r<4 / 6-10 / >12) e COMOVENTI (stesse in unita' R_anello) ---")
for eti, sel in (("ASSOLUTA", "ass"), ("COMOVENTE", "com")):
    print("\n  lettura %s" % eti)
    print("    %-8s %-10s %-9s %-11s %-11s %-11s %-11s %-9s"
          % ("frame", "regione", "nodi", "rho_spin", "|psi|", "eta med", "frac NATI", "grado"))
    for f in F:
        c = C[f]; R = c["R"] if sel == "ass" else c["R"] / RA[f]
        lim = ((0, 4.0, "INTERNA"), (6.0, 10.0, "ANELLO"), (12.0, 1e9, "ESTERNO")) if sel == "ass" \
            else ((0, 0.5, "INTERNA"), (0.75, 1.25, "ANELLO"), (1.5, 1e9, "ESTERNO"))
        for lo, hi, nome in lim:
            m = (R >= lo) & (R < hi)
            if m.sum() < 5:
                print("    %-8d %-10s %-9d  (troppo pochi)" % (f, nome, int(m.sum()))); continue
            idx = np.where(m)[0]
            print("    %-8d %-10s %-9d %-11.4e %-11.4e %-11.4g %-11.4f %-9.4g"
                  % (f, nome, int(m.sum()), np.median(c["rho"][m]), np.median(c["psi"][m]),
                     np.median(c["eta"][m]), float(np.mean(idx >= N0)), np.median(c["grado"][m])))

# ------------------------------------------------------------------ 3: di cosa e' fatta
print("\n--- (3) DI COSA E' FATTA -- eta, nati dopo, `r` ricavato, `perc_chi` ---")
print("  %-8s %-12s %-12s %-12s %-12s %-12s"
      % ("frame", "nati dopo", "frac su n", "eta INTERNA", "eta ANELLO", "frac +1"))
for f in F:
    c = C[f]; n = c["n"]; R = c["R"]
    mi = R < 4.0; ma = (R >= 6.0) & (R < 10.0)
    print("  %-8d %-12d %-12.4f %-12.5g %-12.5g %-12.5f"
          % (f, n - N0, (n - N0) / n,
             np.median(c["eta"][mi]) if mi.sum() > 5 else float("nan"),
             np.median(c["eta"][ma]) if ma.sum() > 5 else float("nan"),
             float(np.mean(c["chi"] > 0))))

print("\n  ⚠ `r` DEI NODI, ricavato da `eta += DT*r` fra istanti consecutivi (il discriminante di `Z46`)")
print("  %-16s %-14s %-14s %-14s %-12s" % ("intervallo", "r INTERNA med", "r ANELLO med", "r ESTERNO", "r/r_floor int"))
DT = 0.01
for a_, b_ in zip(F[:-1], F[1:]):
    na = C[a_]["n"]; nb_ = C[b_]["n"]; m = min(na, nb_)
    rr = (C[b_]["eta"][:m] - C[a_]["eta"][:m]) / (DT * (b_ - a_) * PPF)
    R = C[b_]["R"][:m]
    mi = R < 4.0; ma = (R >= 6.0) & (R < 10.0); me = R >= 12.0
    vi = np.median(rr[mi]) if mi.sum() > 5 else float("nan")
    print("  %-16s %-14.6e %-14.6e %-14.6e %-12.4f"
          % ("%d -> %d" % (a_, b_), vi,
             np.median(rr[ma]) if ma.sum() > 5 else float("nan"),
             np.median(rr[me]) if me.sum() > 5 else float("nan"), vi / R_FLOOR))
print("  (r/r_floor ~ 1 -> la regione interna e' FERMA come i nodi di `Z46`, e «materia nuova» sarebbe")
print("   SBAGLIATO. Era il discriminante fissato nelle previsioni.)")
print("""
  ⚠ LIMITE DICHIARATO: la separazione «assegnato dalla MITOSI» contro «riscritto da `chi_basc`» NON
  e' ricavabile dai `.pkl`: servirebbero CONTATORI durante il run. Qui si riporta solo il NETTO
  (`frac +1`), e la separazione resta DA FARE con una corsa strumentata.""")
print("\n" + "=" * 118)
