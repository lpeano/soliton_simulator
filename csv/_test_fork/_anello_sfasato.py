# -*- coding: utf-8 -*-
"""ANELLO ISTANTANEO -- la misura PRELIMINARE (mandato par.1). **NESSUNA CURA CABLATA.**

Progettazione in doc/TASK_HISTORY/2026-09-18_anello-istantaneo.md (fd198ba).

A  il rapporto `median(|f|)_t / median(|f|)_{t-1}`: mediana, p05, p95, e LA TRAIETTORIA. Se fosse
   ~1 con dispersione trascurabile, la cura sarebbe COSMETICA e ci si ferma.
B  ⚠ `median(x)` con il `med` SFASATO: vale ancora 1? E CON QUANTE CIFRE? (atteso NO: numeratore e
   denominatore di due istanti diversi -> il punto fisso A3 si scioglie da solo)
C  quanti nodi CAMBIANO REGIME (da sopra a sotto `x = 1`), per passo.
D  ⚠ MIO, e P3 da solo non lo vedrebbe: LA DISPERSIONE DI `median(x)` FRA PASSI. `median(|f|)`
   oscilla del 62 % fra passi; con `med` sfasato di uno, `x` EREDITA quell'oscillazione invece di
   dividerla via. L'anello sarebbe rotto ma IL METRO RESTEREBBE BALLERINO, e va detto.
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
print("ANELLO ISTANTANEO -- misura preliminare: `med` del passo PRIMA   [120 passi, seme 5]")
print("=" * 118)
print("  config: CAMPO_SPINORIALE=%s SPINORE_VIVO=%s SPIN_FEEDBACK=%s STEP2_OROLOGIO=%s"
      % (S.CAMPO_SPINORIALE, S.SPINORE_VIVO, S.SPIN_FEEDBACK, S.STEP2_OROLOGIO))
print("  NESSUNA CURA CABLATA: la sonda OSSERVA, il simulatore e' il blob invariato.")

REG = []
_orig = S.Rete.ritmo


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
        REG.append(dict(n=n, f=f, med=max(float(np.median(f)), 1e-9)))
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
IDX = [0, len(B) // 4, len(B) // 2, len(B) - 1]

# ---------------------------------------------------------------- A
print("\n--- (A) il rapporto `median(|f|)_t / median(|f|)_(t-1)` ---")
rap = np.array([B[k]["med"] / max(B[k - 1]["med"], 1e-300) for k in range(1, len(B))])
fin = rap[np.isfinite(rap)]
print("    min %.6g   p05 %.6g   MEDIANA %.6g   p95 %.6g   max %.6g   (n = %d passi)"
      % (fin.min(), np.percentile(fin, 5), np.median(fin), np.percentile(fin, 95), fin.max(), fin.size))
print("    traiettoria: t=1 %.6g   t=1/4 %.6g   t=meta' %.6g   t=ultimo %.6g"
      % (rap[0], rap[len(rap) // 4], rap[len(rap) // 2], rap[-1]))
print("    frazione fuori da [0.5, 2] : %.4f      std/mediana : %.4g"
      % (float(np.mean((fin < 0.5) | (fin > 2.0))), float(np.std(fin) / max(np.median(fin), 1e-300))))
print("  (se il rapporto fosse ~1 con dispersione trascurabile, la cura sarebbe COSMETICA)")

# ---------------------------------------------------------------- B
print("\n--- (B) ⚠ `median(x)` col `med` SFASATO: il punto fisso A3 si scioglie? ---")
mx_att, mx_sfa = [], []
for k in range(1, len(B)):
    f = B[k]["f"]
    mx_att.append(float(np.median(f / max(B[k]["med"], 1e-300))))
    mx_sfa.append(float(np.median(f / max(B[k - 1]["med"], 1e-300))))
mx_att = np.array(mx_att); mx_sfa = np.array(mx_sfa)
print("  %-16s %-15s %-15s %-15s %-15s | %-12s" % ("", "t=1", "t=1/4", "t=meta'", "t=ultimo", "max|med-1|"))
for eti, v in (("ATTUALE", mx_att), ("SFASATO", mx_sfa)):
    print("  %-16s %-15.10g %-15.10g %-15.10g %-15.10g | %-12.6g"
          % (eti, v[0], v[len(v) // 4], v[len(v) // 2], v[-1], float(np.max(np.abs(v - 1.0)))))
viv = mx_att > 0
print("  ATTUALE, esclusi i passi degeneri (`Z33`, median(x) = 0): max|med-1| = %.3e  su %d passi"
      % (float(np.max(np.abs(mx_att[viv] - 1.0))) if viv.any() else float("nan"), int(viv.sum())))
viv2 = mx_sfa > 0
print("  SFASATO, esclusi gli stessi passi              : max|med-1| = %.6g  su %d passi"
      % (float(np.max(np.abs(mx_sfa[viv2] - 1.0))) if viv2.any() else float("nan"), int(viv2.sum())))
print("  (il punto fisso A3 e' `median(x) = 1` ESATTO. Si guardano LE CIFRE, non un si'/no.)")

# ---------------------------------------------------------------- C
print("\n--- (C) quanti nodi CAMBIANO REGIME (attraversano `x = 1`)? ---")
camb = []
for k in range(1, len(B)):
    f = B[k]["f"]
    a = f / max(B[k]["med"], 1e-300)
    s = f / max(B[k - 1]["med"], 1e-300)
    camb.append(float(np.mean((a >= 1.0) != (s >= 1.0))))
camb = np.array(camb)
print("    frazione di nodi che cambiano lato di `x = 1` : mediana %.4f   p05 %.4f   p95 %.4f   max %.4f"
      % (np.median(camb), np.percentile(camb, 5), np.percentile(camb, 95), camb.max()))

# ---------------------------------------------------------------- D
print("\n--- (D) ⚠ il metro resta BALLERINO? dispersione di `median(x)` FRA PASSI ---")
for eti, v in (("median(x) ATTUALE", mx_att), ("median(x) SFASATO", mx_sfa)):
    vv = v[v > 0]
    print("    %-22s : mediana %.6g   p05 %.6g   p95 %.6g   std/med %.4g"
          % (eti, np.median(vv), np.percentile(vv, 5), np.percentile(vv, 95),
             float(np.std(vv) / max(np.median(vv), 1e-300))))
mm = np.array([x["med"] for x in B])
print("    %-22s : mediana %.6g                                  std/med %.4g"
      % ("median(|f|) (il metro)", np.median(mm), float(np.std(mm) / max(np.median(mm), 1e-300))))
print("""
  COME SI LEGGE -- fissato PRIMA (task history fd198ba):
    rapporto ~1, dispersione trascurabile -> cura COSMETICA: si dice e ci si ferma.
    median(x) resta 1 a dieci cifre       -> L'ANELLO NON E' ROTTO: fermarsi e capire perche'.
    median(x) si stacca da 1              -> A3 si scioglie: si procede alla cura.
    median(x) oscilla quanto median(|f|)  -> si procede LO STESSO (A6 viene prima) ma si DICHIARA
                                             che il metro resta ballerino: e' un fronte nuovo.""")

print("\n" + "=" * 118)
