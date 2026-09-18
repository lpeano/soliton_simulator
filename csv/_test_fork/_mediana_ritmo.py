# -*- coding: utf-8 -*-
"""LA MEDIANA IN `ritmo()`: normalizzazione o GAUGE?  (mandato par.2, punto 2.4 + supporto a 2.1)

Progettazione in doc/TASK_HISTORY/2026-09-18_mediana-in-ritmo.md (committato PRIMA, bb058c0).
**NESSUN CABLAGGIO.** Questo script OSSERVA.

2.1  che cos'e' `f`: distribuzione, segno, dimensione (la dimensione si legge dal sorgente:
     `signed = Delta_angolo / DT` -> 1/T, e lo script ne misura la SCALA).
2.4  `median(|f|)` EVOLVE nel tempo, o e' anch'essa pinnata?
     Se la scala su cui si normalizza CRESCE coi passi, allora `x` e' gia' rapportato a una
     grandezza che evolve, e il difetto e' PARZIALE: si riporta di quanto.

E si misura anche cio' che il difetto costa davvero:
  - `median(r)` contro `r_unit` (l'ancoraggio, gia' visto: ~1.0);
  - la DISPERSIONE di `r`: la mediana e' pinnata, ma lo SPREAD no -- ed e' li' che vive la fisica
    che resta. Se lo spread cresce coi passi, il sistema differenzia i tempi propri ANCHE con la
    mediana ancorata.
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
_ARGV = list(sys.argv)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

PASSI = int(_ARGV[_ARGV.index("--passi") + 1]) if "--passi" in _ARGV else 120

print("=" * 118)
print("LA MEDIANA IN ritmo(): normalizzazione o GAUGE?   [%d passi, seme 5]" % PASSI)
print("=" * 118)
print("  config: SPINORE_VIVO=%s  SPIN_FEEDBACK=%s  CAMPO_SPINORIALE=%s  TEMPO_SEGNO=%s  TAU_LOC=%s"
      % (S.SPINORE_VIVO, S.SPIN_FEEDBACK, S.CAMPO_SPINORIALE, S.TEMPO_SEGNO, S.TAU_LOC))
print("  TEMPO_PROPRIO_ORIENTATO=%s  -> f = %s"
      % (S.TEMPO_PROPRIO_ORIENTATO, "signed (con SEGNO)" if S.TEMPO_PROPRIO_ORIENTATO else "|signed|"))

# ---------------------------------------------------------------- la sonda su ritmo()
REG = []
_orig = S.Rete.ritmo


def spia(self):
    out = _orig(self)
    if out is None:
        return out
    # si RICOSTRUISCE `f` con le stesse espressioni del sorgente, sugli stessi ingressi
    try:
        if S.TEMPO_SEGNO and len(getattr(self, "tw", [])):
            REG.append(dict(ramo="TEMPO_SEGNO", f=None, r=np.asarray(out, float).copy()))
            return out
        if self._psi_prec is None or len(self._psi_prec) != self.n:
            REG.append(dict(ramo="primo passo", f=None, r=np.asarray(out, float).copy()))
            return out
        a = np.angle(self.psi) - np.angle(self._psi_prec)
        signed = ((a + np.pi) % (2 * np.pi) - np.pi) / S.DT
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        ramo = "scalare 2pi"
        if (S.CAMPO_SPINORIALE and _ps is not None and _psp is not None
                and len(_ps) == self.n and len(_psp) == self.n):
            a = np.angle(_ps[:, 0]) - np.angle(_psp[:, 0])
            signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / S.DT
            ramo = "spinoriale 4pi"
        f = signed if S.TEMPO_PROPRIO_ORIENTATO else np.abs(signed)
        REG.append(dict(ramo=ramo, f=np.asarray(f, float).copy(),
                        r=np.asarray(out, float).copy(), n=self.n))
    except Exception as e:
        REG.append(dict(ramo="ERRORE: %s" % e, f=None, r=None))
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
for _ in range(PASSI):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
S.Rete.ritmo = _orig

buoni = [x for x in REG if x.get("f") is not None and x["f"].size > 3]
print("\n  invocazioni di ritmo() : %d   di cui con `f` ricostruibile : %d" % (len(REG), len(buoni)))
rami = {}
for x in REG:
    rami[x["ramo"]] = rami.get(x["ramo"], 0) + 1
print("  per RAMO: %s" % ", ".join("%s=%d" % kv for kv in sorted(rami.items(), key=lambda t: -t[1])))
if not buoni:
    print("  NESSUNA invocazione utile: la misura non si puo' fare."); sys.exit(1)

# ---------------------------------------------------------------- 2.1 la scala di f
print("\n--- (2.1) CHE COS'E' `f`: la SCALA, e come si muove ---")
print("  dal sorgente: `signed = Delta_angolo / DT`  ->  DIMENSIONE 1/T (una FREQUENZA), PER NODO.")
print("  quindi `x = f/med` e' ADIMENSIONALE, e la divisione SERVE a quello.")
print("\n  %-8s %-9s %-13s %-13s %-13s %-13s" % ("invoc.", "n", "median|f|", "p05|f|", "p95|f|", "max|f|"))
idx = [0, len(buoni) // 4, len(buoni) // 2, 3 * len(buoni) // 4, len(buoni) - 1]
for k in idx:
    x = buoni[k]; f = np.abs(x["f"])
    print("  %-8d %-9d %-13.5g %-13.5g %-13.5g %-13.5g"
          % (k, x["n"], np.median(f), np.percentile(f, 5), np.percentile(f, 95), f.max()))

# ---------------------------------------------------------------- 2.4 median(|f|) evolve?
print("\n--- (2.4) `median(|f|)` EVOLVE nel tempo, o e' anch'essa pinnata? ---")
med = np.array([float(np.median(np.abs(x["f"]))) for x in buoni])
print("  median(|f|) : prima %.6g   ultima %.6g   -> rapporto %.4g" % (med[0], med[-1], med[-1] / max(med[0], 1e-300)))
print("  min %.6g   max %.6g   -> escursione %.4g ordini di grandezza"
      % (med.min(), med.max(), np.log10(med.max() / max(med.min(), 1e-300))))
q = len(med) // 4
print("  per QUARTI del run: %s" % "  ".join("%.5g" % np.median(med[i * q:(i + 1) * q]) for i in range(4)))
print("""
  COME SI LEGGE: se `median(|f|)` si muove di ORDINI DI GRANDEZZA, allora `x` e' rapportato a una
  scala che EVOLVE, e la normalizzazione non e' un ancoraggio statico: il difetto e' PARZIALE.
  Se invece e' quasi costante, la scala e' di fatto una COSTANTE mascherata da statistica.""")

# ---------------------------------------------------------------- l'ancoraggio e la dispersione
print("\n--- L'ANCORAGGIO e cio' che RESTA LIBERO ---")
rr = [x["r"] for x in buoni]
mr = np.array([float(np.median(v)) for v in rr])
print("  median(r) : mediana %.9f   (r_unit e' fisso: la mediana di r e' pinnata -- C12)" % np.median(mr))
disp = np.array([float(np.percentile(v, 95) - np.percentile(v, 5)) for v in rr])
iqr = np.array([float(np.percentile(v, 75) - np.percentile(v, 25)) for v in rr])
print("  DISPERSIONE di r (p95-p05) : prima %.6g   ultima %.6g   -> rapporto %.4g"
      % (disp[0], disp[-1], disp[-1] / max(disp[0], 1e-300)))
print("  IQR di r                   : prima %.6g   ultima %.6g   -> rapporto %.4g"
      % (iqr[0], iqr[-1], iqr[-1] / max(iqr[0], 1e-300)))
print("  per QUARTI (p95-p05): %s" % "  ".join("%.5g" % np.median(disp[i * q:(i + 1) * q]) for i in range(4)))
print("""
  ⚠ QUESTA E' LA DOMANDA CHE CONTA DAVVERO: la MEDIANA e' pinnata per identita', ma lo SPREAD no.
  Se lo spread CRESCE, il sistema differenzia i tempi propri anche con la mediana ancorata, e il
  difetto e' di AMPIEZZA, non di esistenza. Se lo spread e' PIATTO, il tempo proprio e' quasi
  uniforme e l'ancoraggio e' l'intera storia.""")

print("\n" + "=" * 118)
