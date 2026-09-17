# -*- coding: utf-8 -*-
"""V6-V8, V10 -- SIGILLO DI (2) `spinta` e (3) `_rep` (memoria della repulsione).

(2)  spinta = 0.02 * self.d0 * _rep        era  0.02 * np.median(self.d0) * rep   [A2, A3]
(3)  _rep += dt_e * (rep - _rep) / tau_pp   era  rep istantaneo                    [A5, A7]

I criteri sono di DUE tipi, e non si confondono:
 - LIMITE (V6, V7): la forma nuova deve RIDURSI a quella vecchia nel limite in cui la differenza
   non c'e'. E' il rito del par.2.2, e distingue una sostituzione da una riscrittura.
 - CONTROLLO POSITIVO (V8): la forma nuova deve FARE QUALCOSA. Un sigillo che verifica solo il
   limite passerebbe anche su codice morto (par.10, criterio 2).
ASCII PURO.
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
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SC = os.environ.get("SCRATCH", HERE)
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-48s %s" % ("PASS" if ok else "FAIL", nome, misura))


print("=" * 118)
print("V6-V8, V10 -- (2) spinta LOCALE  e  (3) _rep CON MEMORIA")
print("=" * 118)

# ---------------------------------------------------------------- V6: il limite di (2)
print("\n--- (V6) LIMITE di (2): se tutte le d0 fossero uguali, la forma nuova = la vecchia ---")
rng = np.random.default_rng(7)
rep = rng.random(5000)
d0_unif = np.full(5000, 0.37)
vecchio = 0.02 * float(np.median(d0_unif)) * rep
nuovo = 0.02 * d0_unif * rep
verdetto("V6 riduzione al limite (d0 costante): byte-identico",
         float(np.max(np.abs(vecchio - nuovo))) == 0.0,
         "max|A-B| = %.3e su %d archi (shape %s = %s)"
         % (np.max(np.abs(vecchio - nuovo)), len(rep), vecchio.shape, nuovo.shape))

d0_var = rng.lognormal(-1.0, 1.0, 5000)
v2 = 0.02 * float(np.median(d0_var)) * rep
n2 = 0.02 * d0_var * rep
print("  e con d0 REALISTICHE (lognormale) il rapporto nuovo/vecchio va da %.3f a %.1f"
      % ((n2 / np.maximum(v2, 1e-300)).min(), (n2 / np.maximum(v2, 1e-300)).max()))
verdetto("V6b fuori dal limite le due forme DIFFERISCONO (controllo positivo)",
         float(np.max(np.abs(v2 - n2))) > 0.0, "max|A-B| = %.3e" % np.max(np.abs(v2 - n2)))

# ---------------------------------------------------------------- V7: il limite di (3)
print("\n--- (V7) LIMITE di (3): per dt_e/tau_pp -> 1 la memoria torna all'ISTANTANEO ---")
tau = np.ones(5000)
mem = np.zeros(5000)
mem = mem + 1.0 * (rep - mem) / tau          # dt_e = tau  ->  mem := rep
verdetto("V7 riduzione al limite (dt_e = tau_pp): _rep == rep",
         float(np.max(np.abs(mem - rep))) == 0.0, "max|A-B| = %.3e" % np.max(np.abs(mem - rep)))

print("  e il CRICCHETTO: si somministra rep=1 per 20 passi, poi rep=0 per 20.")
tau = np.full(3, 5.0)
ist, memo = [], []
m = np.zeros(3)
for k in range(40):
    r_ = np.ones(3) if k < 20 else np.zeros(3)
    m = m + 1.0 * (r_ - m) / tau
    ist.append(r_[0]); memo.append(m[0])
print("     istantaneo: sale a %.3f, poi cade a %.3f IN UN PASSO" % (ist[19], ist[20]))
print("     con memoria: sale a %.3f, poi decade a %.3f (passo 21), %.3f (passo 40)"
      % (memo[19], memo[20], memo[39]))
verdetto("V7b il contributo PUO' DECRESCERE (A7: il cricchetto e' chiuso)",
         memo[39] < memo[19] and memo[20] < memo[19],
         "da %.4f a %.4f dopo che la causa e' sparita" % (memo[19], memo[39]))
verdetto("V7c e NON e' istantaneo (altrimenti la memoria sarebbe inerte)",
         memo[20] > 0.0, "al primo passo senza causa vale ancora %.4f, non 0" % memo[20])

# ---------------------------------------------------------------- V8/V10: il codice VIVO
print("\n--- (V8/V10) IL CODICE VIVO: 60 passi reali ---")
db = os.path.join(SC, "_v8.pkl")
cmd = [sys.executable, os.path.join(ROOT, "soliton_simulator.py"),
       "--batch", "--nmasse", "3", "--sep", "8", "--seed", "7", "--passi", "60",
       "--ogni", "60", "--db-ogni", "60", "--campo-spinoriale", "--spinore-vivo",
       "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet",
       "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
       "--csv", os.path.join(SC, "_v8.csv"), "--sync-db", db, "--db-cleanup"]
p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
if p.returncode != 0:
    print("  [FAIL] rc=%s\n%s" % (p.returncode, (p.stderr or "")[-1500:]))
    esiti.append(False)
else:
    A = pickle.load(open(db, "rb"))["attrs"]
    _rep = np.asarray(A.get("_rep", []), float)
    d0 = np.asarray(A["d0"], float)
    d = np.asarray(A["d"], float)
    print("  archi %d   len(_rep) %d" % (len(d0), len(_rep)))
    verdetto("V8a `_rep` e' allineato agli ARCHI ai tre punti di nascita",
             len(_rep) == len(d0), "len(_rep) %d == len(d0) %d" % (len(_rep), len(d0)))
    print("  _rep: min %.4g  mediana %.4g  max %.4g  non nulli %.3f %%"
          % (_rep.min(), np.median(_rep), _rep.max(), 100.0 * (_rep != 0).mean()) if len(_rep) else "")
    sc = A.get("_rep_scarto_max")
    print("  scarto massimo memoria-istantaneo: %s" % sc)
    if sc is not None:
        verdetto("V8b CONTROLLO POSITIVO: la memoria NON e' l'istantaneo",
                 float(sc) > 0.0, "max|_rep - rep| = %.6g (se fosse 0, (3) sarebbe inerte)" % float(sc))
    print("  P5 -- contatori dei rami:")
    for k in ("_rep_guardia_tot", "_rep_guardia_salti", "_rep_realloc", "_rep_dte_fallback",
              "_taup_peq_degenere", "_taup_causale_scatti", "_taup_causale_tot",
              "_taup_causale_su_degenere", "_taup_cfl_max"):
        print("     %-28s %s" % (k, A.get(k)))
    tot = A.get("_rep_guardia_tot") or 1
    salti = A.get("_rep_guardia_salti") or 0
    verdetto("V8c la guardia len(d0)==len(avv) e' ora CONTATA",
             A.get("_rep_guardia_tot") is not None,
             "%d chiamate, %d salti (%.2f %%)" % (tot, salti, 100.0 * salti / tot))
    verdetto("V10a stabilita': d0 finito e > 0",
             bool(np.all(np.isfinite(d0)) and np.all(d0 > 0)),
             "min %.6g, NaN %d" % (d0.min(), int((~np.isfinite(d0)).sum())))
    verdetto("V10b stabilita': d finito e > 0",
             bool(np.all(np.isfinite(d)) and np.all(d > 0)), "min %.6g" % d.min())
    nb = np.asarray(A.get("_nb"), float) if A.get("_nb") is not None else None
    if nb is not None and nb.ndim == 2:
        nn = np.linalg.norm(nb, axis=1)
        verdetto("V10c norma di Bloch |nb| = 1", float(np.max(np.abs(nn - 1.0))) < 1e-9,
                 "max| |nb| - 1 | = %.3e" % np.max(np.abs(nn - 1.0)))
    cfl = A.get("_taup_cfl_max")
    if cfl is not None:
        verdetto("V10d tau_p resta stabile anche con (2) e (3) attive",
                 float(cfl) < 1.0, "_taup_cfl_max = %.6g" % float(cfl))

print("\n" + "=" * 118)
ok = sum(esiti)
print("V6-V8, V10: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
NON dice che il sistema smetta di espandersi. (3) chiude il cricchetto sull'INGRESSO: `_rep` puo'
ora calare quando la causa sparisce. `d0` resta cumulativa, e nessuna di queste due correzioni la
rende reversibile. E' scritto cosi' anche in doc/PREVISIONI_qualitative.md, PRIMA del cablaggio.
E (2) NON risolve A1: il coefficiente `0.02` resta un numero SCELTO. Toglie A2 e A3, non A1.""")
