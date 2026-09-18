# -*- coding: utf-8 -*-
"""LA FREQUENZA DI RIFERIMENTO -- prima il NUMERO (mandato par.1), poi il test dei vincoli (par.2).

Progettazione in doc/TASK_HISTORY/2026-09-18_frequenza-riferimento.md (b6308d1). **NESSUNA CURA,
E NESSUN NUMERO NEL SIMULATORE**: quel che serve alla misura sta QUI.

A  LA TABELLA. Quattro riferimenti, TUTTI in [1/tempo] (A3c: non si confrontano grandezze non
   commensurabili), tutti letti come 'MEDIANA ATTRAVERSO I NODI, PER PASSO':
     median(|f|)      il riferimento ATTUALE          (gia' uno scalare per passo)
     cs_nodo/d_nodo   il tempo-luce del nodo          (il candidato forte del mandato)
     CS_M/d_nodo      il vuoto sulla scala locale
     CS_M/LAM         il vuoto sulla scala fondamentale -- E' UNA COSTANTE, e si riporta col suo zero
   La colonna che DECIDE e' la VARIANZA NEL TEMPO: std/mediana della traiettoria fra passi.
B  IL TEST DEL PUNTO FISSO (vincolo 3). Per ogni riferimento R: la mediana per passo di x = f/R.
   ⚠ E si distinguono DUE cose che il criterio 'si muove / non si muove' confonde:
     COSTANTE PER COSTRUZIONE -> ESATTO cifra per cifra a ogni passo -> punto fisso, A3 violato;
     COSTANTE PER STATO       -> FLUTTUA, e la fluttuazione ha una scala -> legittimo.
   Percio' si riporta max|median(x) - 1| e le CIFRE, non un si'/no.
C  IL NUMERO CHE LUCA HA CHIESTO: median(|f|)/R, mediana e dispersione -> di quanto si sposta `r`.
D  `d_nodo` SI MUOVE? Se fosse quasi costante, CS_M/d_nodo sarebbe CS_M/LAM travestito.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

for _f in ("CAMPO_SPINORIALE", "CS_DINAMICO", "CHI_CORE", "FORK_SU2", "FORK_SU2_MEM",
           "SPINORE_CORRETTO"):
    setattr(S, _f, True)

print("=" * 118)
print("LA FREQUENZA DI RIFERIMENTO -- il numero, e i vincoli   [120 passi, seme 5]")
print("=" * 118)
print("  config: CAMPO_SPINORIALE=%s SPINORE_VIVO=%s SPIN_FEEDBACK=%s STEP2_OROLOGIO=%s CS_DINAMICO=%s"
      % (S.CAMPO_SPINORIALE, S.SPINORE_VIVO, S.SPIN_FEEDBACK, S.STEP2_OROLOGIO, S.CS_DINAMICO))
print("  CS_M = %.6g   LAM = %.6g   DT = %.6g   ->   CS_M/LAM = %.10g  (COSTANTE: LAM e' fisso, :146)"
      % (S.CS_M, S.LAM, S.DT, S.CS_M / S.LAM))

REG = []
_orig = S.Rete.ritmo


def _d_nodo(rete):
    """la STESSA formula di _tempo_luce_nodo (:3036-3044): media di `d` sugli archi incidenti."""
    n = rete.n
    ii = np.asarray(rete.i); jj = np.asarray(rete.j); dd = np.asarray(rete.d, float)
    if len(ii) and len(dd) == len(ii):
        m = (ii < n) & (jj < n)
        grado = (np.bincount(ii[m], minlength=n) + np.bincount(jj[m], minlength=n)).astype(float)
        somma = (np.bincount(ii[m], weights=dd[m], minlength=n) +
                 np.bincount(jj[m], weights=dd[m], minlength=n))
        out = somma / np.maximum(grado, 1.0)
        out[grado <= 0] = S.LAM
        iso = int(np.sum(grado <= 0))
    else:
        out = np.full(n, S.LAM); iso = n
    return np.maximum(out, 1e-12), iso


def spia(self):
    out = _orig(self)
    try:
        n = self.n
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        if not (_ps is not None and _psp is not None and len(_ps) == n and len(_psp) == n
                and S.CAMPO_SPINORIALE):
            REG.append(None); return out
        a = np.angle(np.asarray(_ps)[:, 0]) - np.angle(np.asarray(_psp)[:, 0])
        f = np.abs(((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / S.DT)
        csp = getattr(self, "_cs_nodo_prev", None)
        if csp is None or len(csp) < n:
            REG.append(None); return out
        dn, iso = _d_nodo(self)
        REG.append(dict(n=n, f=f, cs=np.asarray(csp, float)[:n], d=dn, iso=iso))
    except Exception:
        REG.append(None)
    return out


S.Rete.ritmo = spia
r = S.Rete(5)
r.semina(80)
for _ in range(6):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
Nc = S.N_CRITICO() if callable(getattr(S, "N_CRITICO", None)) else 200
for k in range(3):
    ang = 2 * np.pi * k / 3
    r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                  centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for _ in range(120):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
S.Rete.ritmo = _orig

B = [x for x in REG if x is not None]
print("\n  invocazioni utilizzabili: %d su %d" % (len(B), len(REG)))
if len(B) < 20:
    print("  TROPPO POCHE."); sys.exit(1)
print("  nodi ISOLATI (d_nodo -> LAM, il ramo che il mandato vieta): %d su %d invocazioni con >0"
      % (sum(1 for x in B if x["iso"] > 0), len(B)))

# i quattro riferimenti, per passo, per nodo -- TUTTI in [1/tempo]
def rif(x, quale):
    if quale == "att":
        return np.full(x["n"], max(float(np.median(x["f"])), 1e-9))   # scalare, esteso ai nodi
    if quale == "luce":
        return x["cs"] / x["d"]
    if quale == "vuoto":
        return S.CS_M / x["d"]
    return np.full(x["n"], S.CS_M / S.LAM)


NOMI = [("att", "median(|f|)      ATTUALE"),
        ("luce", "cs_nodo/d_nodo   tempo-luce"),
        ("vuoto", "CS_M/d_nodo      vuoto+locale"),
        ("lam", "CS_M/LAM         costante")]
ULT = B[-30:]
IDX = [0, len(B) // 4, len(B) // 2, len(B) - 1]

# ---------------------------------------------------------------- A
print("\n--- (A) LA TABELLA -- quattro riferimenti, tutti in [1/tempo] ---")
print("  %-26s %-11s %-11s %-11s | %-11s %-11s %-11s %-11s | %-10s"
      % ("riferimento", "p05 nodi", "MEDIANA", "p95 nodi", "t=primo", "t=1/4", "t=meta'", "t=ultimo",
         "std/med T"))
for q, eti in NOMI:
    tutti = np.concatenate([rif(x, q) for x in ULT])
    traj = np.array([float(np.median(rif(x, q))) for x in B])
    sd = float(np.std(traj) / max(abs(np.median(traj)), 1e-300))
    print("  %-26s %-11.5g %-11.5g %-11.5g | %-11.5g %-11.5g %-11.5g %-11.5g | %-10.4g"
          % (eti, np.percentile(tutti, 5), np.median(tutti), np.percentile(tutti, 95),
             traj[IDX[0]], traj[IDX[1]], traj[IDX[2]], traj[IDX[3]], sd))
print("  NB: `median(|f|)` e' UNO SCALARE per passo -> la sua distribuzione ATTRAVERSO I NODI e'")
print("      COSTANTE PER COSTRUZIONE (p05 = mediana = p95). Non e' una cella vuota: e' il punto.")
print("  NB: `CS_M/LAM` ha std/med = 0 ESATTO. LAM e' fisso (:146, riassegnato solo da CLI): E' UN NUMERO.")

# ---------------------------------------------------------------- B
print("\n--- (B) ⚠ IL PUNTO FISSO (vincolo 3): `median(x)` con x = f/R, passo per passo ---")
print("  %-26s %-13s %-13s %-13s %-13s | %-12s %-10s"
      % ("riferimento", "t=primo", "t=1/4", "t=meta'", "t=ultimo", "max|med-1|", "std/med"))
for q, eti in NOMI:
    mx = np.array([float(np.median(x["f"] / np.maximum(rif(x, q), 1e-300))) for x in B])
    print("  %-26s %-13.10g %-13.10g %-13.10g %-13.10g | %-12.4g %-10.4g"
          % (eti, mx[IDX[0]], mx[IDX[1]], mx[IDX[2]], mx[IDX[3]],
             float(np.max(np.abs(mx - 1.0))), float(np.std(mx) / max(abs(np.median(mx)), 1e-300))))
print("  COME SI LEGGE -- e distingue due cose che 'si muove / non si muove' confonde:")
print("    max|med-1| ~ 0 A DIECI CIFRE  -> COSTANTE PER COSTRUZIONE: punto fisso, A3 VIOLATO;")
print("    max|med-1| grande e fluttuante -> COSTANTE PER STATO (o nemmeno): LEGITTIMO.")

# ---------------------------------------------------------------- C
print("\n--- (C) IL NUMERO CHIESTO: di quanto si sposterebbe `r`? rapporto median(|f|)/R ---")
print("  %-26s %-13s %-13s %-13s | %-12s" % ("riferimento", "MEDIANA fra T", "min fra T", "max fra T", "std/med"))
for q, eti in NOMI:
    if q == "att":
        continue
    rr = np.array([float(np.median(x["f"])) / max(float(np.median(rif(x, q))), 1e-300) for x in B])
    print("  %-26s %-13.6g %-13.6g %-13.6g | %-12.4g"
          % (eti, np.median(rr), rr.min(), rr.max(), float(np.std(rr) / max(abs(np.median(rr)), 1e-300))))
print("  (il rapporto e' il FATTORE per cui `x` verrebbe moltiplicato passando al nuovo riferimento)")

# ---------------------------------------------------------------- D
print("\n--- (D) `d_nodo` SI MUOVE? (se no, CS_M/d_nodo e' CS_M/LAM travestito) ---")
dt = np.array([float(np.median(x["d"])) for x in B])
print("    d_nodo MEDIANO : t=primo %.6g   t=1/4 %.6g   t=meta' %.6g   t=ultimo %.6g"
      % (dt[IDX[0]], dt[IDX[1]], dt[IDX[2]], dt[IDX[3]]))
print("    std/mediana fra passi %.4g    min %.6g   max %.6g   rapporto max/min %.4g"
      % (float(np.std(dt) / max(np.median(dt), 1e-300)), dt.min(), dt.max(), dt.max() / max(dt.min(), 1e-300)))
dd = np.concatenate([x["d"] for x in ULT])
print("    d_nodo ATTRAVERSO I NODI (30 passi): p05 %.6g   mediana %.6g   p95 %.6g   (LAM = %.6g)"
      % (np.percentile(dd, 5), np.median(dd), np.percentile(dd, 95), S.LAM))
ncs = np.concatenate([x["cs"] for x in ULT]) / S.CS_M
print("    per confronto, cs/CS_M: p05 %.6g   mediana %.6g   p95 %.6g"
      % (np.percentile(ncs, 5), np.median(ncs), np.percentile(ncs, 95)))

print("\n" + "=" * 118)
