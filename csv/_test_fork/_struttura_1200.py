# -*- coding: utf-8 -*-
"""LA STRUTTURA A 1200 PASSI -- post-processing dei quattro snapshot. **NESSUNA CURA, SOLA LETTURA.**

Progettazione in doc/TASK_HISTORY/2026-09-18_struttura-1200.md (fb87640).
Previsioni QUALITATIVE scritte PRIMA in doc/PREVISIONI_qualitative.md (stesso commit).

⚠ IN TESTA, E NON IN FONDO (presidio par.3 del mandato):
  * `Z9` E' APERTA: tutto cio' che si vede e' su un kernel CHE NON HA FINITO DI ACCENDERSI;
  * il run usa `--tau-luce`, IL CUI SIGILLO E' FALLITO (CLAUDE.md par.0): ramo NON CERTIFICATO;
  * UN SEME SOLO: non e' un dato, e' un'osservazione da rifare;
  * NESSUN VERDETTO DI FISICA. Si riportano i NUMERI e la FORMA.

1  MATURAZIONE: `ramp = min(1, eta/TAU_A)` e la frazione con `f = 0`, ai quattro istanti.
2  IL GUSCIO: profilo RADIALE dal baricentro (= l'origine: i tre centri sono a 2pi k/3 su un
   cerchio di raggio `sep`), in bin di raggio: `|psi|`, `rho_spin`, `cs/CS_M`, `|<n>|`, E IL
   CONTEGGIO DEI NODI PER BIN.
3  LE FASI: media circolare di `phi` per coorte -- assegnazione PER POSIZIONE al centro piu' vicino,
   perche' il tracking (`conc_nodi`) NON e' salvato nel `.pkl` (liste, non ndarray). DICHIARATO.
4  IL CONTRASTO: centro contro guscio, `n`, `Lam`, stress `max|d-d0|/d0`.

⚠ E I TRE FALSIFICATORI, APPLICATI PRIMA DI DESCRIVERE IL GUSCIO:
  a) `eta` dei nodi del guscio contro quella del centro -> se e' PIU' BASSA e' il transitorio Z44;
  b) il minimo di `|psi|` coincide coi bin a POCHI NODI? -> minimo di STATISTICA, non di campo;
  c) il minimo sta all'estremo del raggio popolato? -> e' il BORDO della nube, non una parete.
ASCII PURO.
"""
import os
import pickle
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
D = os.path.join("csv", "_test_fork", "_g1200")
PASSI = [120, 400, 800, 1200]
SEP = 8.0
NB = 26

print("=" * 118)
print("LA STRUTTURA A 1200 PASSI -- i numeri e la forma. NESSUN VERDETTO DI FISICA.")
print("=" * 118)
print("""  ⚠ PRESIDI, IN TESTA:
    * `Z9` e' APERTA: il kernel non ha finito di accendersi;
    * `--tau-luce` ha il SIGILLO FALLITO (CLAUDE.md par.0): ramo NON CERTIFICATO;
    * UN SEME: non e' un dato.""")

S = {}
for p in PASSI:
    f = os.path.join(D, "stato_%d.pkl" % p)
    if not os.path.exists(f):
        print("\n  MANCA %s -- il run non e' arrivato a %d passi. DICHIARATO." % (f, p))
        continue
    st = pickle.load(open(f, "rb"))
    S[p] = st["attrs"]
    S[p]["__blob"] = st.get("blob"); S[p]["__dirty"] = st.get("dirty")
if not S:
    print("  NESSUNO snapshot: non si puo' misurare."); sys.exit(1)
p0 = sorted(S)[0]
print("\n  snapshot presenti: %s" % sorted(S))
print("  blob dello stato salvato: %s   dirty: %s   (P6: letto DAI DATI)"
      % (str(S[p0]["__blob"])[:8], S[p0]["__dirty"]))


def A(p, k, d=None):
    v = S[p].get(k, d)
    return v if v is not None else d


def nn(p):
    return int(len(A(p, "pos", np.zeros((0, 3)))))


def raggi(p):
    q = np.asarray(A(p, "pos"))[:nn(p)]
    return np.linalg.norm(q[:, :2], axis=1)


# ------------------------------------------------------------------ 1
print("\n--- (1) LA MATURAZIONE: `ramp = min(1, eta/TAU_A)` e la frazione con `f = 0` ---")
print("  %-8s %-7s %-11s %-11s %-11s %-11s %-13s %-11s"
      % ("passo", "n", "eta med", "ramp p05", "RAMP MED", "ramp p95", "frac ramp=0", "Lam"))
for p in sorted(S):
    e = np.asarray(A(p, "eta", np.zeros(0)), float)[:nn(p)]
    ta = float(A(p, "_TAU_A_run", 50.0)) if A(p, "_TAU_A_run") else 50.0
    r = np.minimum(1.0, e / ta)
    ps = np.asarray(A(p, "psi", np.zeros(0, complex)))[:nn(p)]
    lam = float(np.mean(np.abs(ps) ** 2)) if ps.size else float("nan")
    print("  %-8d %-7d %-11.6g %-11.6g %-11.6g %-11.6g %-13.6f %-11.6g"
          % (p, nn(p), np.median(e), np.percentile(r, 5), np.median(r), np.percentile(r, 95),
             float(np.mean(r <= 0)), lam))
print("    riferimento a 120 passi (ALTRA SCENA, n~450): ramp 0.0002 / 0.0102 / 0.0212 ai passi 1/60/120")
print("    ⚠ NON si confrontano direttamente: scena diversa, n diverso (A3c). Si guarda LA FORMA.")
print("\n  `f = 0` (la verifica diretta di `Z44`: qui la mitosi e' quasi ferma)")
print("  %-8s %-9s %-13s %-13s" % ("passo", "n", "nodi |psi|=0", "frazione"))
for p in sorted(S):
    ps = np.asarray(A(p, "psi", np.zeros(0, complex)))[:nn(p)]
    z = int(np.sum(np.abs(ps) == 0.0)) if ps.size else 0
    print("  %-8d %-9d %-13d %-13.6f" % (p, nn(p), z, z / max(nn(p), 1)))
print("  (a 120 passi, scena-sonda con mitosi viva: 0.44 %. La previsione era: QUASI NULLA qui.)")

# ------------------------------------------------------------------ 2
print("\n--- (2) IL GUSCIO: profilo RADIALE dal baricentro (l'origine) ---")
print("    (i tre centri stanno a 2pi*k/3 su un cerchio di raggio sep = %.1f -> baricentro = origine)" % SEP)
PROF = {}
for p in sorted(S):
    n = nn(p); R = raggi(p)
    ps = np.asarray(A(p, "psi", np.zeros(0, complex)))[:n]
    rs = np.asarray(A(p, "rho_spin", np.zeros(n)), float)[:n] if A(p, "rho_spin") is not None else np.full(n, np.nan)
    cs = np.asarray(A(p, "_cs_nodo_prev", np.zeros(0)), float)
    cs = cs[:n] if cs.size >= n else np.full(n, np.nan)
    nb = np.asarray(A(p, "_nb", np.zeros((n, 3))), float)[:n]
    et = np.asarray(A(p, "eta", np.zeros(n)), float)[:n]
    rmax = float(np.percentile(R, 99.5))
    bordi = np.linspace(0.0, rmax, NB + 1)
    righe = []
    for b in range(NB):
        m = (R >= bordi[b]) & (R < bordi[b + 1])
        if m.sum() == 0:
            righe.append(None); continue
        righe.append(dict(r=0.5 * (bordi[b] + bordi[b + 1]), cnt=int(m.sum()),
                          psi=float(np.median(np.abs(ps[m]))) if ps.size else np.nan,
                          rho=float(np.median(rs[m])),
                          cs=float(np.median(cs[m])) if np.isfinite(cs[m]).any() else np.nan,
                          coer=float(np.linalg.norm(np.mean(nb[m], axis=0))),
                          eta=float(np.median(et[m])),
                          z=int(np.sum(np.abs(ps[m]) == 0.0)) if ps.size else 0))
    PROF[p] = righe
    print("\n  passo %d   (n = %d, r99.5 = %.2f)" % (p, n, rmax))
    print("    %-8s %-8s %-12s %-12s %-10s %-10s %-10s %s"
          % ("r", "nodi", "|psi| med", "rho_spin", "cs/CS_M", "|<n>|", "eta med", "psi=0"))
    for q in righe:
        if q is None:
            continue
        print("    %-8.2f %-8d %-12.5g %-12.5g %-10.5g %-10.5g %-10.5g %d"
              % (q["r"], q["cnt"], q["psi"], q["rho"], q["cs"] / 2.0 if q["cs"] == q["cs"] else float("nan"),
                 q["coer"], q["eta"], q["z"]))

# ------------------------------------------------------------------ falsificatori
print("\n--- ⚠ I TRE FALSIFICATORI, PRIMA di descrivere il guscio ---")
for p in sorted(S):
    righe = [q for q in PROF[p] if q is not None and q["cnt"] >= 5]
    if len(righe) < 5:
        print("  passo %d: troppi pochi bin popolati. DICHIARATO." % p); continue
    vals = np.array([q["psi"] for q in righe])
    k = int(np.argmin(vals))
    rmin = righe[k]
    tot = sum(q["cnt"] for q in righe)
    interni = [q for q in righe if q["r"] < rmin["r"]]
    esterni = [q for q in righe if q["r"] > rmin["r"]]
    eta_in = np.median([q["eta"] for q in interni]) if interni else float("nan")
    print("  passo %-5d minimo di |psi| a r = %-7.2f  (|psi| = %.5g, nodi %d = %.1f %% del totale)"
          % (p, rmin["r"], rmin["psi"], rmin["cnt"], 100.0 * rmin["cnt"] / max(tot, 1)))
    print("      (a) eta del bin minimo %.5g  contro eta mediana INTERNA %.5g   -> rapporto %.3g"
          % (rmin["eta"], eta_in, rmin["eta"] / eta_in if eta_in else float("nan")))
    print("      (b) nodi nel bin minimo %d ; mediana dei nodi per bin %d   -> %s"
          % (rmin["cnt"], int(np.median([q["cnt"] for q in righe])),
             "POCHI: sospetto minimo di STATISTICA" if rmin["cnt"] < 0.3 * np.median([q["cnt"] for q in righe])
             else "popolazione confrontabile"))
    print("      (c) bin oltre il minimo: %d   -> %s"
          % (len(esterni), "IL MINIMO E' AL BORDO: non e' una parete" if len(esterni) <= 1
             else "c'e' popolazione OLTRE il minimo"))
    if interni and esterni:
        ci = np.median([q["coer"] for q in interni]); ce = np.median([q["coer"] for q in esterni])
        pi_ = np.median([q["psi"] for q in interni]); pe = np.median([q["psi"] for q in esterni])
        print("      contrasto: |<n>| dentro %.5g / fuori %.5g   |psi| dentro %.5g / fuori %.5g"
              % (ci, ce, pi_, pe))

# ------------------------------------------------------------------ 3
print("\n--- (3) LE FASI DELLE TRE MASSE (coorti PER POSIZIONE: il tracking NON e' nel .pkl) ---")
C = [(SEP * np.cos(2 * np.pi * k / 3), SEP * np.sin(2 * np.pi * k / 3)) for k in range(3)]
print("  %-8s %-9s %-9s %-9s | %-11s %-11s %-11s | %-10s %-10s"
      % ("passo", "n1", "n2", "n3", "d(1-2)", "d(2-3)", "d(3-1)", "coer INT", "coer FRA"))
for p in sorted(S):
    n = nn(p); q = np.asarray(A(p, "pos"))[:n, :2]
    ph = np.asarray(A(p, "phi", np.zeros(n)), float)[:n]
    dd = np.stack([np.linalg.norm(q - np.array(c), axis=1) for c in C], axis=1)
    lab = np.argmin(dd, axis=1)
    vic = dd.min(axis=1) < SEP    # solo i nodi VICINI a una massa: il vuoto lontano non e' una coorte
    zs, cs_int, nl = [], [], []
    for k in range(3):
        m = (lab == k) & vic
        nl.append(int(m.sum()))
        if m.sum() < 5:
            zs.append(np.nan); cs_int.append(np.nan); continue
        z = np.mean(np.exp(1j * ph[m]))
        zs.append(np.angle(z)); cs_int.append(abs(z))
    dphi = [((zs[a] - zs[b] + np.pi) % (2 * np.pi) - np.pi) if (zs[a] == zs[a] and zs[b] == zs[b]) else np.nan
            for a, b in ((0, 1), (1, 2), (2, 0))]
    zz = [np.exp(1j * z) for z in zs if z == z]
    cfra = abs(np.mean(zz)) if len(zz) >= 2 else np.nan
    print("  %-8d %-9d %-9d %-9d | %+11.5f %+11.5f %+11.5f | %-10.5g %-10.5g"
          % (p, nl[0], nl[1], nl[2], dphi[0], dphi[1], dphi[2], np.nanmedian(cs_int), cfra))
print("    (2pi/3 = %.5f. «Convergere» significa RESTARCI: tre fasi che derivano passano di li' ogni tanto.)"
      % (2 * np.pi / 3))

# ------------------------------------------------------------------ 4
print("\n--- (4) IL CONTRASTO e la SANITA' ---")
print("  %-8s %-9s %-12s %-12s %-12s %-14s %-12s"
      % ("passo", "n", "rho centro", "rho guscio", "centro/gusc", "max|d-d0|/d0", "NaN/inf"))
for p in sorted(S):
    righe = [q for q in PROF[p] if q is not None and q["cnt"] >= 5]
    if not righe:
        continue
    vals = np.array([q["psi"] for q in righe]); k = int(np.argmin(vals))
    interni = [q for q in righe if q["r"] < righe[k]["r"]]
    rc = np.median([q["rho"] for q in interni]) if interni else float("nan")
    rg = righe[k]["rho"]
    d = np.asarray(A(p, "d", np.zeros(0)), float); d0 = np.asarray(A(p, "d0", np.zeros(0)), float)
    st = float(np.max(np.abs(d - d0) / np.maximum(d0, 1e-12))) if d.size and d.size == d0.size else float("nan")
    ps = np.asarray(A(p, "psi", np.zeros(0, complex)))
    fin = bool(np.all(np.isfinite(ps))) and bool(np.all(np.isfinite(d)))
    print("  %-8d %-9d %-12.5g %-12.5g %-12.5g %-14.5g %-12s"
          % (p, nn(p), rc, rg, rc / rg if rg else float("nan"), st, "no" if fin else "SI'"))

print("\n--- I CONTATORI (A8) a fine run ---")
for c in ("_ritmo_chiamate", "_ritmo_med_assente", "_ritmo_med_identico", "_ritmo_med_non_promosso",
          "_ritmo_f_tutto_nullo", "_ritmo_med_sul_pavimento", "_ritmo_sicurezza", "_ritmo_guard4pi_ko",
          "_cs_chiamate", "_cs_fallback", "_sfondo_ko_peq", "_cs_lam_degenere"):
    print("    %-28s %s" % (c, A(sorted(S)[-1], c, "assente")))

print("\n" + "=" * 118)
print("NESSUN VERDETTO DI FISICA. I numeri e la forma, un seme, Z9 aperta, --tau-luce non certificato.")
print("=" * 118)
