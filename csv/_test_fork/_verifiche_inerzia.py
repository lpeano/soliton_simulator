# -*- coding: utf-8 -*-
"""LE QUATTRO VERIFICHE PRELIMINARI DI (1) -- mandato par.2. **NON e' un cablaggio.**

  inerzia = (rho_sorgente / peq_nodo) * (d_nodo / cs_nodo)**2

 1. `peq` e' disponibile e VALIDO nel punto dove si calcola `inerzia`? Archi/grado aggiornati?
 2. `peq` puo' essere NaN o <= 0 li'? (`inerzia` si calcola PRIMA o DOPO la calibrazione?)
 3. `_tempo_luce_nodo` e' chiamabile li', senza ricalcoli?
 4. `_fatt_cs` va rimosso o resta? Chi legge `_fatt_cs_ultimo`?

 +  UNA QUINTA, che il mandato non chiede ma che un riscontro gia' committato impone (voce Z1):
    `_rho_sorgente()` e `peq` sono la STESSA grandezza?

Il wrapper OSSERVA e DELEGA: non cambia nessuna legge, non tocca l'RNG.
ASCII PURO.
"""
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO"):
    setattr(S, _f, True)

print("=" * 116)
print("VERIFICHE PRELIMINARI DI (1) -- inerzia = (rho_sorgente/peq_nodo) * (d/cs)^2")
print("=" * 116)

# ---------------------------------------------------------------- (4) chi legge _fatt_cs_ultimo
src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
usi = [ln.strip() for ln in src.splitlines() if "_fatt_cs_ultimo" in ln.split("#")[0]]
print("\n--- (4) `_fatt_cs_ultimo`: chi lo LEGGE? ---")
for u in usi:
    print("   %s" % u)
print("  occorrenze nel CODICE: %d  -> %s" %
      (len(usi), "SOLO LA SCRITTURA: NESSUNO LO LEGGE" if len(usi) == 1 else "ha lettori"))
print("""  LETTURA: il commento dice "per la metrica (solo lettura a valle)", ma a valle NON C'E'
  NESSUNO. E' il QUARTO caso della stessa famiglia (_passo_spinoriale "ORFANO" ma vivo, VERSO_CHI
  cablato ma muto, spin_locale mai chiamata): lo stato di vita del codice non e' leggibile dal
  codice. CONSEGUENZA OPERATIVA: togliere `_fatt_cs` dall'inerzia NON rompe nessun consumatore.""")

# ---------------------------------------------------------------- (1)(2) peq nel punto dell'inerzia
osserva = []
orig_ps = S.Rete._passo_spinoriale


def spia(self, i, j, w, dt_n, *a, **k):
    n = self.n
    peq = np.asarray(getattr(self, "peq", []), float)
    ii = np.asarray(self.i, int)
    jj = np.asarray(self.j, int)
    deg = getattr(self, "_deg", None)
    rec = dict(passo=len(osserva), n=n, archi=len(peq),
               peq_nan=int(np.isnan(peq).sum()) if len(peq) else -1,
               peq_nonpos=int(((peq <= 0) & np.isfinite(peq)).sum()) if len(peq) else -1,
               ij_ok=(len(ii) == len(peq) and len(jj) == len(peq)),
               deg_ok=(deg is not None and len(deg) == n))
    if len(peq) and len(ii) == len(peq):
        sp = np.bincount(ii, np.nan_to_num(peq), minlength=n) + \
             np.bincount(jj, np.nan_to_num(peq), minlength=n)
        pn = sp / np.maximum(deg if deg is not None else 1, 1)
        rec["pn_nan"] = int(np.isnan(pn).sum())
        rec["pn_nonpos"] = int((pn <= 0).sum())
        rec["pn_med"] = float(np.median(pn))
    rec["tempo_luce_ok"] = hasattr(self, "_tempo_luce_nodo")
    try:
        t = self._tempo_luce_nodo(i, j)
        rec["T"] = (float(np.min(t)), float(np.median(t)), float(np.max(t)))
    except Exception as e:
        rec["T"] = "ERRORE: %s" % e
    rs = self._rho_sorgente()
    I = np.abs(self.psi[:n]) ** 2
    rec["rs_vs_I"] = float(np.corrcoef(rs, I)[0, 1]) if n > 2 and np.std(I) > 0 and np.std(rs) > 0 else float("nan")
    osserva.append(rec)
    return orig_ps(self, i, j, w, dt_n, *a, **k)


S.Rete._passo_spinoriale = spia

r = S.Rete(seed=13)
for c in [(-4., 0, 0), (4., 0, 0), (0., 4., 0)]:
    r.nuova_massa(120, raggio=2.0, centro=c, fase=0.0)
for _ in range(25):
    r.step()
    r.mitosi()

print("\n--- (1)(2) `peq` NEL PUNTO IN CUI SI CALCOLA `inerzia` (dentro _passo_spinoriale) ---")
print("  NB dal codice: _passo_spinoriale e' chiamato a :3062, la CALIBRAZIONE di peq e' a :3147.")
print("  Quindi l'inerzia si calcola PRIMA che peq sia calibrato, nello stesso passo.\n")
print("  %-7s %-7s %-8s %-9s %-11s %-9s %-11s %-9s" %
      ("passo", "n", "archi", "peq NaN", "peq <=0", "pn NaN", "pn <=0", "i/j ok"))
for o in osserva[:8]:
    print("  %-7d %-7d %-8d %-9d %-11d %-9s %-11s %-9s" %
          (o["passo"], o["n"], o["archi"], o["peq_nan"], o["peq_nonpos"],
           o.get("pn_nan", "-"), o.get("pn_nonpos", "-"), o["ij_ok"]))
print("  ...")
for o in osserva[-3:]:
    print("  %-7d %-7d %-8d %-9d %-11d %-9s %-11s %-9s" %
          (o["passo"], o["n"], o["archi"], o["peq_nan"], o["peq_nonpos"],
           o.get("pn_nan", "-"), o.get("pn_nonpos", "-"), o["ij_ok"]))

nan_passi = [o["passo"] for o in osserva if o["peq_nan"] > 0]
np_passi = [o["passo"] for o in osserva if o.get("pn_nonpos", 0) > 0]
print("\n  passi con peq NaN nel punto dell'inerzia : %s" % (nan_passi if nan_passi else "NESSUNO"))
print("  passi con peq_nodo <= 0                  : %s" % (np_passi if np_passi else "NESSUNO"))
print("  i/j allineati agli archi in tutti i passi : %s" % all(o["ij_ok"] for o in osserva))
print("  _deg allineato ai nodi in tutti i passi   : %s" % all(o["deg_ok"] for o in osserva))

# ---------------------------------------------------------------- (3) _tempo_luce_nodo
print("\n--- (3) `_tempo_luce_nodo` chiamabile nel punto dell'inerzia? ---")
print("  presente come metodo: %s" % all(o["tempo_luce_ok"] for o in osserva))
for o in osserva[:3] + osserva[-2:]:
    print("     passo %-3d  T = d/cs : min %s" % (o["passo"], o["T"] if isinstance(o["T"], str)
                                                  else "%.4g  mediana %.4g  max %.4g" % o["T"]))

# ---------------------------------------------------------------- (5) la quinta verifica
print("\n--- (5) `_rho_sorgente()` e `peq` sono la STESSA grandezza? (voce Z1, gia' committata) ---")
cs = [o["rs_vs_I"] for o in osserva if np.isfinite(o["rs_vs_I"])]
print("  correlazione rho_sorgente <-> |psi|^2, per passo: %s"
      % ["%.3f" % x for x in cs[:8]])
print("  (se rho_sorgente FOSSE |psi|^2, varrebbe 1.000 esatto a ogni passo)")
