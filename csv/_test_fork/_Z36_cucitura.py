# -*- coding: utf-8 -*-
"""Z36 -- QUALE CANDIDATO DOMINA, e la CUCITURA CONSERVA IL SEGNALE?  (mandato par.2 + par.7.2)

Progettazione in doc/TASK_HISTORY/2026-09-18_Z36-cucire-snapshot.md (02ac909). **NESSUNA CURA.**

A  `|psi_spin[:,0]| / |psi_spin|` -- il candidato del mandato: `angle(z)` e' mal definito per
   |z| -> 0, e uno spinore RUOTA fra le due componenti. Si riporta il RAPPORTO, non il valore
   assoluto (A3c: |psi_spin| stesso cambia scala nel tempo).
B  i salti di `f` CORRELANO con la componente piccola?
C  `|<psi_prec|psi>|` dove `f` salta: se e' vicino a 1, gli stati erano VICINI e il salto e' un
   artefatto della PARAMETRIZZAZIONE, non fisica.
D  ⚠ LA MISURA CHE DECIDE SE CABLARE, e serve LA COPPIA non un numero solo:
     a_curato = a_originale - angle(overlap)
   - il SALTO |delta a|/|a| deve SCENDERE (e' lo scopo della cucitura);
   - MA il LIVELLO median|a| deve RESTARE. Se crolla verso zero, la cura ha tolto IL SEGNALE, non
     il rumore -- e `L1` da solo sarebbe un FALSO PASS.
   Il conto (task history par.1): se lo spinore ruota RIGIDAMENTE di una fase phi, allora
   angle(overlap) = phi E a_originale = phi, quindi a_curato = 0. L'orologio si fermerebbe
   ESATTAMENTE nel caso che deve misurare. SI MISURA, non si assume.
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
print("Z36 -- quale candidato domina, e la CUCITURA conserva il segnale?   [120 passi, seme 5]")
print("=" * 118)
print("  config: CAMPO_SPINORIALE=%s SPINORE_VIVO=%s SPIN_FEEDBACK=%s TEMPO_PROPRIO_ORIENTATO=%s"
      % (S.CAMPO_SPINORIALE, S.SPINORE_VIVO, S.SPIN_FEEDBACK, S.TEMPO_PROPRIO_ORIENTATO))

REG = []
_orig = S.Rete.ritmo


def spia(self):
    out = _orig(self)
    try:
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        if (_ps is None or _psp is None or len(_ps) != self.n or len(_psp) != self.n):
            REG.append(None); return out
        ps = np.asarray(_ps); psp = np.asarray(_psp)
        # la grandezza ORIGINALE
        a_or = np.angle(ps[:, 0]) - np.angle(psp[:, 0])
        a_or = (a_or + 2 * np.pi) % (4 * np.pi) - 2 * np.pi
        # l'overlap su ENTRAMBE le componenti, e la grandezza CURATA
        ov = np.sum(np.conj(psp) * ps, axis=1)
        a_cu = a_or - np.angle(ov)
        a_cu = (a_cu + 2 * np.pi) % (4 * np.pi) - 2 * np.pi
        nps = np.sqrt(np.sum(np.abs(ps) ** 2, axis=1)) + 1e-300
        npp = np.sqrt(np.sum(np.abs(psp) ** 2, axis=1)) + 1e-300
        REG.append(dict(n=self.n,
                        a_or=a_or, a_cu=a_cu,
                        comp0=np.abs(ps[:, 0]) / nps,              # A: il RAPPORTO, non il valore
                        ovn=np.abs(ov) / (nps * npp)))             # C: overlap NORMALIZZATO
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
    a = 2 * np.pi * k / 3
    r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                  centro=(8.0 * np.cos(a), 8.0 * np.sin(a), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for _ in range(120):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
S.Rete.ritmo = _orig

B = [x for x in REG if x is not None]
print("\n  invocazioni utilizzabili: %d su %d" % (len(B), len(REG)))
if not B:
    print("  NESSUNA: la misura non si puo' fare."); sys.exit(1)

# ---------------------------------------------------------------- A
print("\n--- (A) `|psi_spin[:,0]| / |psi_spin|` -- la componente si annulla? ---")
c0 = np.concatenate([x["comp0"] for x in B[-30:]])
print("  su %d nodi-istanza (ultimi 30 passi):" % len(c0))
print("    mediana %.6g   p05 %.6g   p01 %.6g   min %.6g" %
      (np.median(c0), np.percentile(c0, 5), np.percentile(c0, 1), c0.min()))
for s in (1e-1, 1e-2, 1e-3, 1e-6, 1e-9):
    print("    frazione sotto %-8.0e : %.6f" % (s, float(np.mean(c0 < s))))
print("  (se una frazione non trascurabile e' sotto 1e-3, `angle` su quella componente e' rumore)")

# ---------------------------------------------------------------- C
print("\n--- (C) `|<psi_prec|psi>|` NORMALIZZATO -- gli stati erano vicini? ---")
ov = np.concatenate([x["ovn"] for x in B[-30:]])
print("    mediana %.6g   p05 %.6g   frazione > 0.99 : %.4f   > 0.9 : %.4f" %
      (np.median(ov), np.percentile(ov, 5), float(np.mean(ov > 0.99)), float(np.mean(ov > 0.9))))
print("  (vicino a 1 = stati VICINI: allora un salto di `f` e' un artefatto della parametrizzazione)")

# ---------------------------------------------------------------- B: la correlazione
print("\n--- (B) i salti di `f` correlano con la componente piccola? ---")
salti_nodo, comp_nodo = [], []
for k in range(1, len(B)):
    p, c = B[k - 1], B[k]
    m = min(len(p["a_or"]), len(c["a_or"]))
    if m < 20:
        continue
    d = np.abs(np.abs(c["a_or"][:m]) - np.abs(p["a_or"][:m]))
    sc = np.maximum(np.abs(p["a_or"][:m]), 1e-30)
    salti_nodo.append(d / sc)
    comp_nodo.append(c["comp0"][:m])
if salti_nodo:
    SS = np.concatenate(salti_nodo); CC = np.concatenate(comp_nodo)
    ok = np.isfinite(SS) & np.isfinite(CC) & (SS < 1e6)
    cc = float(np.corrcoef(np.log10(np.maximum(CC[ok], 1e-30)), np.log10(np.maximum(SS[ok], 1e-30)))[0, 1])
    print("  corr( log|comp0/|psi||, log(salto relativo) ) = %+.4f   su %d nodi-coppia" % (cc, int(ok.sum())))
    for lo, hi, eti in ((0.0, 1e-2, "comp0 < 1e-2"), (1e-2, 1e-1, "1e-2..1e-1"), (1e-1, 1.1, "> 1e-1")):
        sel = ok & (CC >= lo) & (CC < hi)
        if sel.sum() > 20:
            print("    %-14s : salto relativo MEDIANO %.5g   (n = %d)" % (eti, np.median(SS[sel]), int(sel.sum())))
    print("  (se il salto e' MOLTO piu' grande dove comp0 e' piccola, domina la PARAMETRIZZAZIONE)")

# ---------------------------------------------------------------- D: la misura che decide
print("\n--- (D) ⚠ LA CUCITURA CONSERVA IL SEGNALE? Serve LA COPPIA: salto E livello ---")
print("  %-26s %-16s %-16s" % ("", "a ORIGINALE", "a CURATO"))
liv_or = np.median([np.median(np.abs(x["a_or"])) for x in B[-30:]])
liv_cu = np.median([np.median(np.abs(x["a_cu"])) for x in B[-30:]])
print("  %-26s %-16.6g %-16.6g" % ("LIVELLO  median|a|", liv_or, liv_cu))
sal_or, sal_cu = [], []
for k in range(1, len(B)):
    p, c = B[k - 1], B[k]
    m = min(len(p["a_or"]), len(c["a_or"]))
    if m < 20:
        continue
    for key, acc in (("a_or", sal_or), ("a_cu", sal_cu)):
        a0 = np.abs(p[key][:m]); a1 = np.abs(c[key][:m])
        vivi = (a0 > 0) & (a1 > 0)
        if vivi.sum() > 10:
            acc.append(float(np.median(np.abs(a1[vivi] - a0[vivi])) / max(float(np.median(a0[vivi])), 1e-300)))
print("  %-26s %-16.6g %-16.6g" % ("SALTO  |delta a|/|a|", np.median(sal_or), np.median(sal_cu)))
print("  %-26s %-16s %-16.6g" % ("rapporto LIVELLO cu/or", "", liv_cu / max(liv_or, 1e-300)))
print("""
  COME SI LEGGE -- le letture erano fissate PRIMA (task history 02ac909):
    salto SCENDE e livello RESTA   -> la cura funziona: si cabla.
    salto SCENDE ma livello CROLLA -> LA CURA TOGLIE IL SEGNALE, non il rumore. NON si cabla,
                                      e `L1` da solo sarebbe un FALSO PASS.
    salto NON scende               -> la cucitura non e' il meccanismo: reperto, e si ferma.
  Riferimento: il lift CUCITO (G6) salta dello 0.35 %; `f` non cucito salta del 64.7 %.""")

print("\n" + "=" * 118)
