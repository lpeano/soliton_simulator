# -*- coding: utf-8 -*-
"""Z33 -- IL GAUGE DEGENERE: cosa collassa, quando, e cosa succede a `r`.  (mandato par.2)

Progettazione in doc/TASK_HISTORY/2026-09-18_Z33-gauge-degenere.md (aff0df6, committato PRIMA).
**NESSUNA CURA.** Questo script OSSERVA.

A       IL CHIAMANTE -- la domanda che viene PRIMA di tutte: le degeneri sono nel percorso FISICO
        (`step()` -> `dt_n` -> `eta`) o sono chiamate DIAGNOSTICHE che `eta` non vede mai?
B (2.1) COSA collassa: `f` IDENTICAMENTE nullo / META' esattamente zero con altri non nulli /
        mediana piccola ma non zero. TRE CASI, TRE CURE.
C (2.2) QUANDO: transitorio o regime, e coincidenza con le MITOSI.
D (2.3) COSA SUCCEDE a `r` e a `dt_n`: ENTRAMBE le code (`->1.4e-06` e `->sqrt(2)`), perche' il
        mandato ne prevede una sola e la lettura del sorgente suggerisce l'altra.

⚠ CONFIGURAZIONE: le campagne usano il ramo 4pi SPINORIALE. Misurare lo scalare 2pi direbbe qualcosa
  su una configurazione che nessuno gira -- errore gia' fatto ieri, e prima ancora con --cs-dinamico.
  Lo script ACCENDE i flag delle campagne e LI STAMPA.
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

for _f in ("CAMPO_SPINORIALE", "CS_DINAMICO", "CHI_CORE", "FORK_SU2", "FORK_SU2_MEM",
           "SPINORE_CORRETTO"):
    setattr(S, _f, True)
PASSI = int(_ARGV[_ARGV.index("--passi") + 1]) if "--passi" in _ARGV else 120

print("=" * 118)
print("Z33 -- IL GAUGE DEGENERE: cosa collassa, quando, e cosa succede a r   [%d passi, seme 5]" % PASSI)
print("=" * 118)
print("  config: CAMPO_SPINORIALE=%s  SPINORE_VIVO=%s  SPIN_FEEDBACK=%s  CS_DINAMICO=%s  TAU_LOC=%s"
      % (S.CAMPO_SPINORIALE, S.SPINORE_VIVO, S.SPIN_FEEDBACK, S.CS_DINAMICO, S.TAU_LOC))

REG = []
_orig = S.Rete.ritmo
STATO = {"passo": 0, "n_pre": 0, "nati": 0}


def spia(self):
    chiamante = sys._getframe(1).f_code.co_name
    out = _orig(self)
    if out is None:
        return out
    rec = dict(chiamante=chiamante, passo=STATO["passo"], nati=STATO["nati"], n=self.n,
               r=np.asarray(out, float).copy(), f=None, ramo=None)
    try:
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        if (S.CAMPO_SPINORIALE and _ps is not None and _psp is not None
                and len(_ps) == self.n and len(_psp) == self.n):
            a = np.angle(_ps[:, 0]) - np.angle(_psp[:, 0])
            rec["f"] = np.abs(((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / S.DT)
            rec["ramo"] = "4pi"
            # la causa candidata (1): lo snapshot e' IDENTICO a psi_spin?
            rec["snap_identico"] = bool(np.array_equal(_ps, _psp))
        elif self._psi_prec is not None and len(self._psi_prec) == self.n:
            a = np.angle(self.psi) - np.angle(self._psi_prec)
            rec["f"] = np.abs(((a + np.pi) % (2 * np.pi) - np.pi) / S.DT)
            rec["ramo"] = "2pi"
            rec["snap_identico"] = bool(np.array_equal(self.psi, self._psi_prec))
        else:
            rec["ramo"] = "primo passo"
        # la causa candidata (2): le lunghezze combaciano?
        rec["len_ps"] = (len(_ps) if _ps is not None else -1)
        rec["len_psp"] = (len(_psp) if _psp is not None else -1)
    except Exception as e:
        rec["ramo"] = "ERRORE %s" % e
    REG.append(rec)
    return out


S.Rete.ritmo = spia
_orig_step = S.Rete.step


def spia_step(self):
    STATO["n_pre"] = self.n
    return _orig_step(self)


S.Rete.step = spia_step

r = S.Rete(5)
r.semina(80)
for _ in range(6):
    S.scuoti_vuoto(r); n0 = r.n; r.step(); r.mitosi(); STATO["nati"] = r.n - n0
    r.rilassa_disegno(); r.memoria_hebbiana_moto(); STATO["passo"] += 1
Nc = S.N_CRITICO() if callable(getattr(S, "N_CRITICO", None)) else 200
for k in range(3):
    a = 2 * np.pi * k / 3
    r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                  centro=(8.0 * np.cos(a), 8.0 * np.sin(a), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for _ in range(PASSI):
    S.scuoti_vuoto(r); n0 = r.n; r.step(); r.mitosi(); STATO["nati"] = r.n - n0
    r.rilassa_disegno(); r.memoria_hebbiana_moto(); STATO["passo"] += 1
S.Rete.ritmo = _orig
S.Rete.step = _orig_step

buoni = [x for x in REG if x["f"] is not None and x["f"].size > 3]
deg = [x for x in buoni if float(np.median(x["f"])) <= 0.0]
sani = [x for x in buoni if float(np.median(x["f"])) > 0.0]

# ---------------------------------------------------------------- A: il chiamante
print("\n--- (A) IL CHIAMANTE -- le degeneri sono nel PERCORSO FISICO? ---")
ch = {}
for x in REG:
    ch[x["chiamante"]] = ch.get(x["chiamante"], 0) + 1
print("  TUTTE le invocazioni, per chiamante : %s"
      % ", ".join("%s=%d" % kv for kv in sorted(ch.items(), key=lambda t: -t[1])))
chd = {}
for x in deg:
    chd[x["chiamante"]] = chd.get(x["chiamante"], 0) + 1
print("  le DEGENERI, per chiamante          : %s"
      % (", ".join("%s=%d" % kv for kv in sorted(chd.items(), key=lambda t: -t[1])) if chd else "NESSUNA"))
print("""  -> se le degeneri vengono SOLO da un diagnostico, `eta` non le vede mai (solo la chiamata
     dentro `step()` alimenta `dt_n`), e Z33 NON e' un difetto della fisica.""")

# ---------------------------------------------------------------- B: cosa collassa
print("\n--- (B / 2.1) COSA COLLASSA: `f` tutto nullo, meta' zero, o mediana piccola? ---")
print("  invocazioni con `f` ricostruibile : %d   di cui DEGENERI (median = 0) : %d  (%.1f %%)"
      % (len(buoni), len(deg), 100.0 * len(deg) / max(len(buoni), 1)))
if deg:
    print("\n  %-7s %-7s %-7s %-7s %-11s %-11s %-11s %-9s %-9s" %
          ("passo", "n", "nati", "ramo", "fraz f=0", "p95|f|", "max|f|", "snap==", "len ps/psp"))
    for x in deg:
        f = x["f"]
        print("  %-7d %-7d %-7d %-7s %-11.4f %-11.5g %-11.5g %-9s %d/%d" %
              (x["passo"], x["n"], x["nati"], x["ramo"], float(np.mean(f == 0.0)),
               float(np.percentile(f, 95)), float(f.max()),
               x.get("snap_identico"), x.get("len_ps", -1), x.get("len_psp", -1)))
    tutti_nulli = sum(1 for x in deg if float(np.max(x["f"])) == 0.0)
    print("\n  con `f` IDENTICAMENTE NULLO (max = 0) : %d su %d" % (tutti_nulli, len(deg)))
    print("  con META' zero ma altri NON nulli      : %d su %d" % (len(deg) - tutti_nulli, len(deg)))
    print("  con snapshot IDENTICO a psi_spin       : %d su %d   <- causa candidata (1)"
          % (sum(1 for x in deg if x.get("snap_identico")), len(deg)))

# ---------------------------------------------------------------- C: quando
print("\n--- (C / 2.2) QUANDO: transitorio o regime? e coincidono con le MITOSI? ---")
if deg:
    pp = [x["passo"] for x in deg]
    print("  passi degeneri : %s" % pp)
    print("  su %d passi totali -> primi 10 passi: %d   dopo il passo 20: %d"
          % (STATO["passo"], sum(1 for p in pp if p < 10), sum(1 for p in pp if p >= 20)))
    nati_deg = [x["nati"] for x in deg]
    nati_sani = [x["nati"] for x in sani]
    print("  NODI NATI nel passo: degeneri %s   |   sani: mediana %.1f, frazione con nati>0 %.2f"
          % (nati_deg, float(np.median(nati_sani)) if nati_sani else float("nan"),
             float(np.mean([n > 0 for n in nati_sani])) if nati_sani else float("nan")))
    print("  -> se i degeneri hanno nati>0 e i sani no, la causa candidata (2) e' confermata")

# ---------------------------------------------------------------- D: r e dt_n
print("\n--- (D / 2.3) COSA SUCCEDE a `r` e a `dt_n` -- ENTRAMBE le code ---")
print("  %-10s %-7s %-13s %-13s %-13s %-13s %-13s" %
      ("gruppo", "quanti", "median(r)", "std(r)", "p95-p05", "fraz r>1.4", "fraz r<1e-5"))
for eti, grp in (("DEGENERI", deg), ("SANI", sani)):
    if not grp:
        print("  %-10s 0" % eti); continue
    med = [float(np.median(x["r"])) for x in grp]
    sd = [float(np.std(x["r"])) for x in grp]
    sp = [float(np.percentile(x["r"], 95) - np.percentile(x["r"], 5)) for x in grp]
    alto = [float(np.mean(x["r"] > 1.4)) for x in grp]
    basso = [float(np.mean(x["r"] < 1e-5)) for x in grp]
    print("  %-10s %-7d %-13.6g %-13.6g %-13.6g %-13.4f %-13.4f" %
          (eti, len(grp), np.median(med), np.median(sd), np.median(sp), np.median(alto), np.median(basso)))
print("""
  `dt_n = DT * r`, quindi std(dt_n) = DT * std(r): se std(r) COLLASSA nei degeneri, la DILATAZIONE
  TEMPORALE E' SPARITA in quei passi -- tutti i nodi allo stesso ritmo.
  ⚠ E si guardano ENTRAMBE le code: il mandato prevede `r -> +-1` (x -> inf), ma se `f` e'
  IDENTICAMENTE nullo allora `x = 0` e `r -> 1.414e-06`. Sono due regimi OPPOSTI.""")

print("\n" + "=" * 118)
