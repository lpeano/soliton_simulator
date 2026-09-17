# -*- coding: utf-8 -*-
"""LE CINQUE VERIFICHE PRELIMINARI DI Z9 -- mandato par.2. **NON e' un cablaggio.**

  oggi:   ramp = min(1, eta / TAU_A)
  legge:  ramp = min(1, eta / tempo_luce_nodo_PREC)

 2.1 `_tempo_luce_nodo` chiamabile da `_pesi()`? per NODO? richiede ricalcolo?
 2.2 `d` esiste al primo passo? e i NODI ISOLATI (grado 0)?
 2.3 A6: `d` e `cs` vengono dallo stato PRECEDENTE nel punto in cui `_pesi()` gira?
 2.4 `TAU_A` e' usato altrove? (fatto a parte, dal sorgente)
 2.5 A8b: QUANDO `_pesi()` legge `_cs_nodo_prev` -- prima o dopo :3138? Terzo lettore.

Il wrapper OSSERVA e DELEGA. ASCII PURO.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
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

print("=" * 118)
print("VERIFICHE PRELIMINARI DI Z9 -- ramp = min(1, eta / (d_nodo/cs_nodo))")
print("=" * 118)

# ---------------------------------------------------------------- 2.1 dal sorgente
src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
print("\n--- (2.1) `_tempo_luce_nodo`: forma e dipendenze ---")
print("  chiama `_pesi()`?  %s   <- se SI' ci sarebbe RICORSIONE" %
      ("SI'" if "_pesi()" in src[src.index("def _tempo_luce_nodo"):src.index("def _tempo_luce_nodo") + 3000] else "NO"))
print("  usa `LAM`?         SI', in DUE rami: `d_nodo[grado <= 0] = LAM` e il fallback senza archi")
print("""
  !! IL MANDATO par.6 VIETA `LAM` NELLA NUOVA FORMA. Va distinto:
     - la SCALA PRINCIPALE e' `d_nodo` = media degli archi incidenti -> NON e' LAM;
     - `LAM` entra SOLO nel fallback per i NODI SENZA ARCHI.
     Non e' l'errore bocciato (che era usare LAM/cs come scala), ma E' un uso di LAM nel percorso:
     va CONTATO e dichiarato. La misura sotto dice quanto pesa.""")

# ---------------------------------------------------------------- il wrapper
oss = []
orig_pesi = S.Rete._pesi
orig_tl = S.Rete._tempo_luce_nodo
stato = {"passo": 0, "in_step": False, "cs_scritta": False}


def spia_pesi(self):
    n = self.n
    csp = getattr(self, "_cs_nodo_prev", None)
    grado = (np.bincount(self.i, minlength=n) + np.bincount(self.j, minlength=n)) if len(self.i) else np.zeros(n)
    dd = np.asarray(self.d, float)
    ok_arc = len(dd) == len(self.i) and len(self.i) > 0
    if ok_arc:
        somma = (np.bincount(self.i, weights=dd, minlength=n) +
                 np.bincount(self.j, weights=dd, minlength=n))
        d_nodo = somma / np.maximum(grado, 1.0)
    else:
        d_nodo = np.full(n, float(S.LAM))
    isolati = int(np.sum(grado[:n] <= 0))
    oss.append(dict(passo=stato["passo"], n=n, archi=len(self.i),
                    cs_ok=(csp is not None and len(csp) >= n),
                    cs_len=(len(csp) if csp is not None else -1),
                    cs_scritta_prima=stato["cs_scritta"],
                    isolati=isolati, d_min=float(d_nodo.min()) if n else 0.0,
                    d_med=float(np.median(d_nodo)) if n else 0.0,
                    in_step=stato["in_step"]))
    return orig_pesi(self)


orig_step = S.Rete.step


def spia_step(self):
    stato["in_step"] = True
    stato["cs_scritta"] = False
    r = orig_step(self)
    stato["in_step"] = False
    stato["passo"] += 1
    return r


S.Rete._pesi = spia_pesi
S.Rete.step = spia_step

r = S.Rete(seed=13)
for c in [(-4., 0, 0), (4., 0, 0), (0., 4., 0)]:
    r.nuova_massa(120, raggio=2.0, centro=c, fase=0.0)
for _ in range(15):
    r.step()
    r.mitosi()

# ---------------------------------------------------------------- 2.5 il terzo lettore
print("\n--- (2.5) A8b: `_pesi()` come TERZO LETTORE di `_cs_nodo_prev` ---")
print("  chiamate a `_pesi()` osservate: %d   (in %d passi)" % (len(oss), stato["passo"]))
per_passo = {}
for o in oss:
    per_passo[o["passo"]] = per_passo.get(o["passo"], 0) + 1
vals = sorted(set(per_passo.values()))
print("  chiamate a `_pesi()` PER PASSO: %s   <- se >1, il contatore deve distinguerle" % vals)
dentro = sum(1 for o in oss if o["in_step"])
print("  di cui DENTRO step(): %d   fuori (diagnostici/mitosi/init): %d" % (dentro, len(oss) - dentro))
fb = [o for o in oss if not o["cs_ok"]]
print("  cache `_cs_nodo_prev` NON usabile in %d chiamate su %d  ->  %.4f %%"
      % (len(fb), len(oss), 100.0 * len(fb) / max(len(oss), 1)))
if fb:
    print("     passi in cui accade: %s" % sorted(set(o["passo"] for o in fb))[:12])
    print("     esempio: n=%d  len(cache)=%d" % (fb[0]["n"], fb[0]["cs_len"]))
print("""  CONFRONTO coi due lettori gia' misurati (audit A8, commit 438a02c):
     _tempo_luce_nodo   :  0.0000 %%
     _passo_spinoriale  :  3.0303 %%
     _pesi()            :  %.4f %%   <- QUESTO""" % (100.0 * len(fb) / max(len(oss), 1)))

# ---------------------------------------------------------------- 2.2 nodi isolati e d
print("\n--- (2.2) `d` al primo passo, e i NODI ISOLATI (grado 0) ---")
print("  %-7s %-7s %-9s %-11s %-12s %-12s" % ("passo", "n", "archi", "ISOLATI", "d_nodo min", "d_nodo med"))
for o in oss[:8]:
    print("  %-7d %-7d %-9d %-11d %-12.5g %-12.5g"
          % (o["passo"], o["n"], o["archi"], o["isolati"], o["d_min"], o["d_med"]))
iso_tot = sum(o["isolati"] for o in oss)
print("  nodi isolati TOTALI su tutte le chiamate: %d   (su %d nodi-chiamata)"
      % (iso_tot, sum(o["n"] for o in oss)))
print("  -> e' la frazione in cui `LAM` entrerebbe nella maturazione")

# ---------------------------------------------------------------- 2.3 A6
print("\n--- (2.3) A6: `d` e `cs` vengono dallo stato PRECEDENTE dove `_pesi()` gira? ---")
righe = {}
for k, l in enumerate(src.splitlines(), 1):
    for nome in ("self._cs_nodo_prev = cs_nodo.copy()",
                 "self.d = np.maximum(self.d + dts * self.vd, 0.05)",
                 "ramp = np.minimum(1.0, self.eta / TAU_A)",
                 "self.eta += dt_n"):
        if nome in l and nome not in righe:
            righe[nome] = k
for nome, k in sorted(righe.items(), key=lambda x: x[1]):
    print("   :%-6d %s" % (k, nome))
print("""
  NB: `_pesi()` NON e' chiamata da una riga fissa: la chiama `calcola_psi()`, che gira in piu'
  punti. Per A6 conta QUANDO, e la misura sopra (2.5) lo dice attraverso lo stato della cache.""")

print("\n" + "=" * 118)
print("ESITO -- da leggere insieme, non una per una.")
