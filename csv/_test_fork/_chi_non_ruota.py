# -*- coding: utf-8 -*-
"""CHI NON RUOTA, E PERCHE' -- le cinque misure del mandato. **NESSUNA CURA, strumentazione inerte.**

Progettazione in doc/TASK_HISTORY/2026-09-18_chi-non-ruota.md (0d9abac).

5a  la distribuzione di `perc_chi` nel tempo, e QUALE dei tre rami la genera -- CONTATI, non dedotti
    (A8): nascita `rng.choice([-1,1])` (:1835), mitosi UGUALE (:3945), Schwinger OPPOSTO (:4066).
    Il ramo Schwinger si conta dall'UNICO suo marcatore: `_eredita_spinore_figli(aa, segno=-1)`.
5b  ⚠ il `perc_chi` dei nodi con `f = 0`, contro IL NULLO VERO -- che NON e' 0.5 ma LA FRAZIONE DI
    `+1` DELLA POPOLAZIONE NELLO STESSO ISTANTE (A3c: stessa popolazione, stesso istante).
3   `|psi_spin[:,0]|` e `|psi_spin|` dei nodi fermi: la fase e' DEFINITA? `angle(0) = 0` e' una
    CONVENZIONE di numpy, non una misura.
4   `ramp = min(1, eta/TAU_A)` ed `eta` dei nodi fermi contro tutti -- il collegamento con `Z9`.
2   `|psi_spin(t) - psi_spin(t-1)|` dei nodi fermi: lo stato evolve mentre `f = 0`?
1   l'IDENTITA': gli indici si ripetono fra passi?

⚠ E SI RIPORTA LA FRAZIONE VERA di nodi con `f = 0`, non 'meta'': 'meta'' e' ARITMETICA della
mediana (se median(|f|) = 0 allora almeno meta' e' zero), NON una misura.
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
print("CHI NON RUOTA, E PERCHE'   [120 passi, seme 5]   -- NESSUNA CURA")
print("=" * 118)
print("  blob invariato. TAU_A = %s   DT = %s" % (S.TAU_A, S.DT))
print("\n  I FLAG CHE DANNO A `perc_chi` UN CANALE VERSO LA DINAMICA (verificati, non assunti):")
for nome in ("CALORE_VETTORIALE", "OROLOGIO_SEGNO", "TEMPO_SEGNO", "CHI_BASC", "CHI_DA_SPINORE",
             "CHI_CORE", "TORS_4PI", "COMPAT_CHI", "SPIN_POSITIVI"):
    print("    %-20s %s" % (nome, getattr(S, nome, "ASSENTE")))
print("    _CALORE_INIT         %s" % getattr(S, "_CALORE_INIT", "ASSENTE"))
print("""
  ⚠ `CALORE_VETTORIALE = True` E' IL CANALE, ed e' ACCESO di default:
     `scuoti_vuoto` (:538-540) fa  `phivel[:n] += rng.normal(0,1)*ampiezza * perc_chi`  A OGNI PASSO.
     Quindi `perc_chi` -> `phivel` -> `phi` -> `psi` -> `psi_spin` -> `f`: IL CANALE ESISTE.
     ⚠ MA e' un SEGNO su un rumore SIMMETRICO: la distribuzione marginale di un nodo `+1` e di uno
     `-1` e' LA STESSA. Puo' agire solo attraverso le CORRELAZIONI, non sul singolo nodo.""")

REG = []
CNT = {"mitosi_chiamate": 0, "mitosi_nodi": 0, "schwinger_chiamate": 0, "schwinger_nodi": 0,
       "semina_chiamate": 0, "semina_nodi": 0}
_orig_ritmo = S.Rete.ritmo
_orig_mit = S.Rete.mitosi
_orig_sem = S.Rete.semina
_orig_ered = S.Rete._eredita_spinore_figli


def ered(self, src, segno=1):
    if segno == -1:
        CNT["schwinger_chiamate"] += 1
        CNT["schwinger_nodi"] += int(np.size(src))
    return _orig_ered(self, src, segno)


def mit(self, *a, **k):
    n0 = self.n
    out = _orig_mit(self, *a, **k)
    CNT["mitosi_chiamate"] += 1
    CNT["mitosi_nodi"] += max(self.n - n0, 0)
    return out


def sem(self, n, *a, **k):
    out = _orig_sem(self, n, *a, **k)
    CNT["semina_chiamate"] += 1
    CNT["semina_nodi"] += int(n)
    return out


def spia(self):
    out = _orig_ritmo(self)
    try:
        n = self.n
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        if not (_ps is not None and _psp is not None and len(_ps) == n and len(_psp) == n
                and S.CAMPO_SPINORIALE):
            REG.append(None); return out
        ps = np.asarray(_ps); psp = np.asarray(_psp)
        a = np.angle(ps[:, 0]) - np.angle(psp[:, 0])
        f = np.abs(((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / S.DT)
        REG.append(dict(
            n=n, f=f,
            c0=np.abs(ps[:, 0]), tot=np.sqrt(np.sum(np.abs(ps) ** 2, axis=1)),
            dps=np.sqrt(np.sum(np.abs(ps - psp) ** 2, axis=1)),          # (2) distanza VERA
            eta=np.asarray(self.eta[:n], float).copy(),
            chi=(np.asarray(self.perc_chi[:n]).copy() if len(getattr(self, "perc_chi", [])) >= n
                 else np.zeros(n, int)),
            idx=np.where(f == 0.0)[0].copy()))
    except Exception:
        REG.append(None)
    return out


S.Rete.ritmo = spia; S.Rete.mitosi = mit; S.Rete.semina = sem
S.Rete._eredita_spinore_figli = ered
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
S.Rete.ritmo = _orig_ritmo; S.Rete.mitosi = _orig_mit; S.Rete.semina = _orig_sem
S.Rete._eredita_spinore_figli = _orig_ered

B = [x for x in REG if x is not None]
print("\n  invocazioni utilizzabili: %d su %d   n finale %d" % (len(B), len(REG), r.n))
if len(B) < 20:
    print("  TROPPO POCHE."); sys.exit(1)

# ------------------------------------------------------------------ 5a
print("\n--- (5a) `perc_chi`: la distribuzione, e QUALE ramo la genera (CONTATI) ---")
print("    %-26s chiamate %-6s nodi aggiunti %s" % ("ramo", "", ""))
print("    %-26s %-15d %d" % ("semina/nuova_massa (:1850)", CNT["semina_chiamate"], CNT["semina_nodi"]))
print("    %-26s %-15d %d" % ("mitosi UGUALE (:3945)", CNT["mitosi_chiamate"], CNT["mitosi_nodi"]))
print("    %-26s %-15d %d" % ("Schwinger OPPOSTO (:4066)", CNT["schwinger_chiamate"], CNT["schwinger_nodi"]))
print("    (il ramo Schwinger si conta dal suo UNICO marcatore: _eredita_spinore_figli(.., segno=-1))")
print("\n    %-10s %-8s %-12s %-12s %-12s" % ("istante", "n", "frazione +1", "n(+1)", "n(-1)"))
IDX = [0, len(B) // 4, len(B) // 2, len(B) - 1]
for lab, k in zip(("primo", "1/4", "meta'", "ultimo"), IDX):
    c = B[k]["chi"]
    print("    %-10s %-8d %-12.6f %-12d %-12d"
          % (lab, len(c), float(np.mean(c > 0)), int(np.sum(c > 0)), int(np.sum(c < 0))))
fr = np.array([float(np.mean(x["chi"] > 0)) for x in B])
print("    frazione +1 su tutti i passi: min %.6f  mediana %.6f  max %.6f" % (fr.min(), np.median(fr), fr.max()))

# ------------------------------------------------------------------ la frazione VERA
print("\n--- LA FRAZIONE VERA di nodi con `f = 0` (NON 'meta'': quella e' aritmetica della mediana) ---")
fz = np.array([float(np.mean(x["f"] == 0.0)) for x in B])
deg = [k for k in range(len(B)) if fz[k] > 0]
print("    passi con almeno un nodo a f = 0 : %d su %d" % (len(deg), len(B)))
print("    frazione di nodi a f = 0: max %.6f   mediana sui passi degeneri %.6f"
      % (fz.max(), np.median(fz[fz > 0]) if (fz > 0).any() else 0.0))
for k in deg[:10]:
    print("      passo %-4d n %-6d nodi a f=0 %-6d frazione %.6f   median(|f|) %.6g"
          % (k, B[k]["n"], len(B[k]["idx"]), fz[k], float(np.median(B[k]["f"]))))

if not deg:
    print("\n  NESSUN passo con `f = 0`: le misure 1-5b non hanno popolazione. Si ferma qui.")
    sys.exit(0)


def confronta(campo, eti, fmt="%.6g"):
    """nodi FERMI contro TUTTI, nello STESSO istante e sulla STESSA popolazione (A3c)."""
    print("    %-22s %-13s %-13s | %-13s %-13s" % (eti, "fermi med", "fermi max", "tutti med", "tutti p05"))
    for k in deg:
        v = B[k][campo]; m = B[k]["idx"]
        if len(m) == 0:
            continue
        print(("      passo %-4d           " + fmt + "      " + fmt + "  | " + fmt + "      " + fmt)
              % (k, np.median(v[m]), np.max(v[m]), np.median(v), np.percentile(v, 5)))


# ------------------------------------------------------------------ 5b
print("\n--- (5b) ⚠ `perc_chi` DEI NODI FERMI, contro IL NULLO VERO (la frazione della popolazione) ---")
print("    %-8s %-8s %-14s %-16s %-14s" % ("passo", "n fermi", "frazione +1", "NULLO (pop.)", "scarto"))
for k in deg:
    m = B[k]["idx"]; c = B[k]["chi"]
    if len(m) == 0:
        continue
    fe = float(np.mean(c[m] > 0)); nu = float(np.mean(c > 0))
    print("    %-8d %-8d %-14.6f %-16.6f %+.6f" % (k, len(m), fe, nu, fe - nu))
print("    ⚠ il valore sotto ipotesi nulla NON e' 0.5: e' la frazione della POPOLAZIONE (A3c).")
print("    SI' = tutti lo stesso segno (frazione 0 o 1).  MISTO = vicino al nullo.")

# ------------------------------------------------------------------ 3
print("\n--- (3) `|psi_spin|`: la fase e' DEFINITA? (`angle(0) = 0` e' una CONVENZIONE di numpy) ---")
confronta("c0", "|psi_spin[:,0]|", "%.4e")
confronta("tot", "|psi_spin| totale", "%.4e")

# ------------------------------------------------------------------ 4
print("\n--- (4) `ramp = min(1, eta/TAU_A)` ed `eta`: il collegamento con `Z9` ---")
ta = float(S.TAU_A)
print("    %-8s %-8s %-15s %-15s | %-15s %-15s" % ("passo", "n fermi", "eta fermi med", "ramp fermi", "eta tutti med", "ramp tutti"))
for k in deg:
    m = B[k]["idx"]; e = B[k]["eta"]
    if len(m) == 0:
        continue
    ef = float(np.median(e[m])); et = float(np.median(e))
    print("    %-8d %-8d %-15.6g %-15.6g | %-15.6g %-15.6g"
          % (k, len(m), ef, min(1.0, ef / ta), et, min(1.0, et / ta)))

# ------------------------------------------------------------------ 2
print("\n--- (2) `|psi_spin(t) - psi_spin(t-1)|`: lo stato EVOLVE mentre `f = 0`? ---")
confronta("dps", "|delta psi_spin|", "%.4e")
print("    (se e' ZERO -> congelamento vero. Se NON e' nullo con f = 0 -> difetto dell'OSSERVABILE.)")

# ------------------------------------------------------------------ 1
print("\n--- (1) L'IDENTITA': sono sempre gli stessi nodi? ---")
if len(deg) >= 2:
    for a_, b_ in zip(deg[:-1], deg[1:]):
        A = set(B[a_]["idx"].tolist()); Bs = set(B[b_]["idx"].tolist())
        u = len(A | Bs)
        print("    passi %-4d -> %-4d : |A| %-6d |B| %-6d  intersezione %-6d  Jaccard %.4f"
              % (a_, b_, len(A), len(Bs), len(A & Bs), (len(A & Bs) / u) if u else 0.0))
else:
    print("    un solo passo degenere: l'identita' fra passi NON e' misurabile. DICHIARATO.")

print("""
  COME SI LEGGE -- le sei letture erano fissate PRIMA (task history 0d9abac):
    5b SI' (frazione 0 o 1, lontana dal nullo) -> il tempo proprio distingue le chiralita': STOP.
    4  ramp ~ 0 sui fermi                      -> Z33/Z43 sono SINTOMI di Z9: la cura e' a monte.
    3  |psi| ~ 0                               -> f = 0 e' una CONVENZIONE di numpy, non fisica.
    2  evolve ma angle non lo vede             -> difetto dell'OSSERVABILE.
    1  sempre gli stessi                       -> congelamento.
    nessuna regge                              -> si dice, e NON si inventa la sesta.
  ⚠ E (3) e (4) POSSONO REGGERE ENTRAMBE senza contraddirsi: sarebbero LO STESSO FATTO A DUE LIVELLI
    (ramp ~ 0 -> pesi a zero -> psi ~ 0 -> angle indefinita). NON e' un conflitto.""")

print("\n" + "=" * 118)
