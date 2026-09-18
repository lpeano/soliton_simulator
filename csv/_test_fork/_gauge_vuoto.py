# -*- coding: utf-8 -*-
"""GAUGE DEL VUOTO -- la misura PRELIMINARE BLOCCANTE del mandato (par.1), piu' due passi miei.

Progettazione in doc/TASK_HISTORY/2026-09-18_gauge-vuoto-r.md (0e571b4). **NESSUNA CURA.**

A  `cs/CS_M`: distribuzione e `cs_std/cs` SUL BLOB ATTUALE. Il registro dice 0.0086 % PRIMA di
   cs_floor, il mandato dice 11 % oggi: NON si trasporta un numero vecchio (P1), si misura.
B  DOVE STA IL NODO MEDIANO di `f` -- il gauge attuale e' `median(|f|)`, quindi `x ~ 1` E' il nodo
   mediano per identita'. Si riportano il suo `cs/CS_M` e il suo `rho/peq` CONTRO la distribuzione
   completa, stesso istante e stessa popolazione (A3c).
C  ⚠ IL GAUGE PROPOSTO E' ESSO STESSO ANCORATO? `cs_floor = CS_M/(1 + sqrt(I)*sqrt(1/mean(I)))`:
   il vuoto sta solo nel NUMERATORE, la scala e' `mean(I)`, UNA STATISTICA SULLA PROPRIA
   POPOLAZIONE. Si misura `median(I)/mean(I)` a DUE istanti: se e' stabile, l'ancoraggio c'e' e la
   cura sposta il problema invece di risolverlo.
D  ⚠ `f*d_nodo/CS_M` E' O(1)? Il ginocchio di `x/sqrt(1+x^2)` sta a x = 1. Se il valore tipico e'
   fuori scala, il bottleneck degenera PER TUTTI -- e M4 ('la scala si apre') PASSEREBBE lo stesso,
   perche' una scala appiattita su sqrt(2) HA aperto il tetto. Serve la coppia.
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
print("GAUGE DEL VUOTO -- la misura preliminare BLOCCANTE   [120 passi, seme 5]")
print("=" * 118)
print("  config: CAMPO_SPINORIALE=%s SPINORE_VIVO=%s SPIN_FEEDBACK=%s STEP2_OROLOGIO=%s CS_DINAMICO=%s"
      % (S.CAMPO_SPINORIALE, S.SPINORE_VIVO, S.SPIN_FEEDBACK, S.STEP2_OROLOGIO, S.CS_DINAMICO))
print("  CS_M = %.6g   LAM = %.6g   DT = %.6g" % (S.CS_M, S.LAM, S.DT))

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
    else:
        out = np.full(n, S.LAM)
    return np.maximum(out, 1e-12)


def _peq_nodo(rete):
    """proiezione arco->nodo di `peq`: la STESSA forma gia' usata a :2295-2297."""
    n = rete.n
    ii = np.asarray(rete.i); jj = np.asarray(rete.j)
    pa = np.asarray(rete.peq, float)
    if len(ii) == 0 or len(pa) != len(ii):
        return np.full(n, np.nan)
    m = (ii < n) & (jj < n) & np.isfinite(pa) & (pa > 0)
    num = np.zeros(n); den = np.zeros(n)
    np.add.at(num, ii[m], pa[m]); np.add.at(num, jj[m], pa[m])
    np.add.at(den, ii[m], 1.0);   np.add.at(den, jj[m], 1.0)
    out = np.where(den > 0, num / np.maximum(den, 1.0), np.nan)
    return out


def spia(self):
    out = _orig(self)
    try:
        n = self.n
        # `f` RICALCOLATO CON LA STESSA LEGGE DEL CODICE (:2058-2076), stesso ramo 4pi
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        if (_ps is not None and _psp is not None and len(_ps) == n and len(_psp) == n
                and S.CAMPO_SPINORIALE):
            a = np.angle(np.asarray(_ps)[:, 0]) - np.angle(np.asarray(_psp)[:, 0])
            signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / S.DT
            ramo = "4pi"
        else:
            if self._psi_prec is None or len(self._psi_prec) != n:
                REG.append(None); return out
            a = np.angle(self.psi) - np.angle(self._psi_prec)
            signed = ((a + np.pi) % (2 * np.pi) - np.pi) / S.DT
            ramo = "2pi"
        f = np.abs(signed) if not S.TEMPO_PROPRIO_ORIENTATO else signed
        csp = getattr(self, "_cs_nodo_prev", None)
        if csp is None or len(csp) < n:
            REG.append(None); return out
        cs = np.asarray(csp, float)[:n]
        I = np.abs(self.psi[:n]) ** 2 if len(self.psi) >= n else np.zeros(n)
        REG.append(dict(n=n, ramo=ramo, f=np.abs(f), cs=cs, I=I,
                        d=_d_nodo(self), peq=_peq_nodo(self)))
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
print("\n  invocazioni utilizzabili: %d su %d   (rami: %s)"
      % (len(B), len(REG), ", ".join(sorted(set(x["ramo"] for x in B))) if B else "-"))
if len(B) < 10:
    print("  TROPPO POCHE: la misura non si puo' fare."); sys.exit(1)
print("  fallback cs=CS_M in _tempo_luce_nodo: %s su %s chiamate"
      % (getattr(r, "_cs_fallback", 0), getattr(r, "_cs_chiamate", 0)))

ULT = B[-30:]


def q(v, eti, fmt="%.6g"):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    if v.size == 0:
        print("    %-24s : VUOTO" % eti); return
    print(("    %-24s : min " + fmt + "   p05 " + fmt + "   MEDIANA " + fmt +
           "   p95 " + fmt + "   max " + fmt + "   (n = %d)")
          % (eti, v.min(), np.percentile(v, 5), np.median(v),
             np.percentile(v, 95), v.max(), v.size))


# ---------------------------------------------------------------- A
print("\n--- (A) `cs / CS_M`: il gauge proposto ha varianza? ---")
cs_all = np.concatenate([x["cs"] for x in ULT]) / S.CS_M
q(cs_all, "cs/CS_M (30 passi)")
print("    frazione > 0.99 : %.6f     > 0.9 : %.6f     < 0.5 : %.6f"
      % (float(np.mean(cs_all > 0.99)), float(np.mean(cs_all > 0.9)), float(np.mean(cs_all < 0.5))))
_rap = [float(np.std(x["cs"]) / max(np.mean(x["cs"]), 1e-30)) for x in ULT]
print("    cs_std/cs per passo    : mediana %.6g   min %.6g   max %.6g"
      % (np.median(_rap), np.min(_rap), np.max(_rap)))
print("  (il registro dice 0.0086 % PRIMA di cs_floor; il mandato dice 11 % oggi. Questo e' il blob attuale.)")

# ---------------------------------------------------------------- B
print("\n--- (B) DOVE STA IL NODO MEDIANO di `f` (cioe' x ~ 1, il gauge ATTUALE)? ---")
sel_cs, sel_rp, tut_rp = [], [], []
for x in ULT:
    f = x["f"]
    med = max(float(np.median(f)), 1e-9)
    xx = f / med
    m = (xx >= 0.9) & (xx <= 1.1)
    if m.sum() < 5:
        continue
    sel_cs.append(x["cs"][m] / S.CS_M)
    rp = x["I"] / np.where(np.isfinite(x["peq"]) & (x["peq"] > 0), x["peq"], np.nan)
    sel_rp.append(rp[m]); tut_rp.append(rp)
if sel_cs:
    q(np.concatenate(sel_cs), "cs/CS_M dei nodi x~1")
    q(cs_all, "cs/CS_M di TUTTI")
    q(np.concatenate(sel_rp), "rho/peq dei nodi x~1")
    q(np.concatenate(tut_rp), "rho/peq di TUTTI")
    print("  (cs/CS_M del mediano ~ 1  -> i due gauge quasi coincidono: cura COSMETICA.")
    print("   cs/CS_M del mediano << 1 -> il gauge e' DENTRO la materia: l'allineamento vale.)")
else:
    print("    nessun passo con abbastanza nodi a x~1")

# ---------------------------------------------------------------- C
print("\n--- (C) ⚠ IL GAUGE PROPOSTO E' ESSO STESSO ANCORATO? `I / mean(I)` a DUE istanti ---")
print("  %-10s %-14s %-14s %-14s %-14s" % ("passo", "mean(I)", "median(I)", "median/mean", "frac I>mean"))
for lab, x in (("primo", B[0]), ("1/4", B[len(B) // 4]), ("meta'", B[len(B) // 2]), ("ultimo", B[-1])):
    I = x["I"]; mI = float(np.mean(I))
    print("  %-10s %-14.6g %-14.6g %-14.6g %-14.6g"
          % (lab, mI, float(np.median(I)), float(np.median(I)) / max(mI, 1e-30),
             float(np.mean(I > mI))))
print("  (mean(I/mean(I)) = 1 per IDENTITA'. La domanda e' se il nodo TIPICO -- la MEDIANA -- sia")
print("   anch'esso inchiodato: se median/mean e' stabile fra istanti, l'ancoraggio morde davvero.)")
_cf = [float(np.median(x["cs"])) / S.CS_M for x in B]
print("    cs/CS_M MEDIANO nel tempo: primo %.6g   1/4 %.6g   meta' %.6g   ultimo %.6g"
      % (_cf[0], _cf[len(_cf) // 4], _cf[len(_cf) // 2], _cf[-1]))

# ---------------------------------------------------------------- D
print("\n--- (D) ⚠ `f * d_nodo / CS_M` E' O(1)? (se no, il bottleneck degenera PER TUTTI) ---")
xv = np.concatenate([x["f"] * x["d"] / S.CS_M for x in ULT])
xl = np.concatenate([x["f"] * x["d"] / np.maximum(x["cs"], 1e-30) for x in ULT])
xo = np.concatenate([x["f"] / max(float(np.median(x["f"])), 1e-9) for x in ULT])
q(xv, "f*d/CS_M   (candidato)")
q(xl, "f*d/cs     (tempo-luce)")
q(xo, "f/median|f| (ATTUALE)")
for nome, v in (("f*d/CS_M", xv), ("f*d/cs", xl), ("f/median|f|", xo)):
    v = v[np.isfinite(v)]
    print("    %-12s : frazione x < 1e-3 (pavimento) %.6f   x > 1e3 (saturazione) %.6f   in [0.1,10] %.6f"
          % (nome, float(np.mean(v < 1e-3)), float(np.mean(v > 1e3)),
             float(np.mean((v >= 0.1) & (v <= 10.0)))))
print("""
  COME SI LEGGE -- le letture erano fissate PRIMA (task history 0e571b4):
    cs/CS_M mediano ~ 1            -> i due gauge quasi coincidono: cura COSMETICA, ci si ferma.
    cs/CS_M mediano << 1           -> il gauge e' nella materia: l'allineamento vale.
    cs_std/cs trascurabile         -> `cs` non puo' fare da gauge: la via CADE.
    median(I)/mean(I) stabile ~ 1  -> il gauge PROPOSTO ha il proprio ancoraggio: si RIFORMULA.
    f*d/CS_M fuori da O(1) di >3   -> NON CABLABILE: il bottleneck degenera per tutti, e M4 da solo
    ordini                            sarebbe un FALSO PASS.""")

print("\n" + "=" * 118)
