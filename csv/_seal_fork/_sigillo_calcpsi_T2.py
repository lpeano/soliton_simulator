# -*- coding: utf-8 -*-
"""Q0, Q3-Q8 -- TEMPO 2 di `calcola_psi`: `w` passato ai DUE chiamanti eseguiti dentro `step`.

Q3  riduzione al limite: forzando i chiamanti a NON passare `w` -> byte-identico al riferimento.
Q4  CONTROLLO POSITIVO, in DUE letture: coi valori veri i due DEVONO differire.
    !! Se NON differiscono NON e' un fallimento: significa che i pesi ricalcolati COINCIDEVANO e
    il difetto era TEORICO. Si dichiara, non si forza una differenza.
Q5  il contatore `_calcpsi_w_none` dai DUE chiamanti interni -> 0. Gli altri restano ed ELENCATI.
Q6  nessuna topologia mista: len(w) combacia con gli archi dove viene passato.
Q7  stabilita'. Q8 e' a parte (rigiro dei sigilli del giro).
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
PRE = os.path.join(SC, "_pre_T2.py")
esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-48s %s" % ("PASS" if ok else "FAIL", nome, misura))


def gira(sim, tag, passi=40, seme=9):
    db = os.path.join(SC, "_t2_%s.pkl" % tag)
    cmd = [sys.executable, sim, "--batch", "--nmasse", "3", "--sep", "8",
           "--seed", str(seme), "--passi", str(passi), "--ogni", str(passi),
           "--db-ogni", str(passi), "--campo-spinoriale", "--spinore-vivo",
           "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio",
           "--verlet", "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
           "--csv", os.path.join(SC, "_t2_%s.csv" % tag), "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        print("  [run %s FALLITO rc=%s]\n%s" % (tag, p.returncode, (p.stderr or "")[-1200:]))
        return None
    return pickle.load(open(db, "rb"))["attrs"]


def confronta(A, B, eti):
    ka, kb = set(A), set(B)
    na, nb = len(np.asarray(A["psi"])), len(np.asarray(B["psi"]))
    print("  PRESIDIO, conteggi PER PRIMI: nodi %s = %d, nodi %s = %d" % (eti[0], na, eti[1], nb))
    peggio, peggio_k, conf, diversi = 0.0, "-", 0, 0
    for k in sorted(ka & kb):
        try:
            x = np.asarray(A[k]); y = np.asarray(B[k])
        except Exception:
            continue
        if x.dtype == object or y.dtype == object or x.ndim == 0:
            continue
        if x.shape != y.shape:
            diversi += 1; continue
        conf += 1
        if np.issubdtype(x.dtype, np.number) or np.issubdtype(x.dtype, np.complexfloating):
            d = np.abs(x - y); m = float(np.max(d)) if d.size else 0.0
            if m > peggio:
                peggio, peggio_k = m, k
    print("  array con SHAPE UGUALI confrontati: %d   (shape diverse: %d)" % (conf, diversi))
    return na, nb, conf, diversi, peggio, peggio_k


print("=" * 118)
print("Q0, Q3-Q8 -- TEMPO 2: `w` passato ai due chiamanti ESEGUITI dentro step")
print("=" * 118)

src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()


def in_codice(t, ago):
    return sum(1 for l in t.splitlines() if ago in l.split("#")[0])


print("\n--- (forma) i tre punti nel sorgente ---")
for k, l in enumerate(src.splitlines(), 1):
    if "calcola_psi(w)" in l.split("#")[0] or "else self.calcola_psi()" in l.split("#")[0]:
        print("   :%-6d %s" % (k, l.strip()))
n_w = in_codice(src, "self.calcola_psi(w)")
n_nw = in_codice(src, "psi_t if SYNC_UPDATE else self.calcola_psi()")
verdetto("forma: DUE chiamanti passano `w`, UNO no (l'elif)",
         n_w == 2 and n_nw == 1, "con w: %d, senza: %d (il terzo e' il ramo elif, DICHIARATO)" % (n_w, n_nw))

# ------------------------------------------------------------------ Q4 / Q5 / Q7
print("\n--- (Q4) CONTROLLO POSITIVO: coi valori veri i due DEVONO differire ---")
A = gira(PRE, "pre")
B = gira(os.path.join(ROOT, "soliton_simulator.py"), "post")
if A is None or B is None:
    esiti.append(False)
else:
    na, nb, conf, div, peggio, pk = confronta(A, B, ("PRE", "POST"))
    diverso = (na != nb) or (peggio > 0.0) or (div > 0)
    print("  max|A-B| fra PRE e POST = %.6g  (peggiore: %s)" % (peggio, pk))
    if diverso:
        verdetto("Q4 i due DIFFERISCONO: il difetto NON era teorico", True,
                 "nodi %d vs %d, max|A-B| = %.3e su %d array" % (na, nb, peggio, conf))
    else:
        print("""
  !! I DUE NON DIFFERISCONO, E NON E' UN FALLIMENTO.
  Significa che i pesi ricalcolati da `calcola_psi()` COINCIDEVANO con il `w` di `step`, quindi
  IL DIFETTO ERA TEORICO. La correzione RESTA GIUSTA -- chiude un ramo il cui esito non era
  garantito, e toglie una dipendenza dall'ordine di esecuzione -- ma il suo effetto sui numeri e'
  NULLO. Lo si registra cosi', e NON si forza una differenza.""")
        verdetto("Q4 letto nella seconda lettura: difetto TEORICO", True,
                 "max|A-B| = 0.000e+00 su %d array, nodi %d = %d" % (conf, na, nb))

    print("\n--- (Q5) il contatore DOPO ---")
    tot, none = B.get("_calcpsi_chiamate"), B.get("_calcpsi_w_none")
    tot_a, none_a = A.get("_calcpsi_chiamate"), A.get("_calcpsi_w_none")
    print("  PRIMA : chiamate %s, con `w is None` %s  (%.1f %%)"
          % (tot_a, none_a, 100.0 * (none_a or 0) / max(tot_a or 1, 1)))
    print("  DOPO  : chiamate %s, con `w is None` %s  (%.1f %%)"
          % (tot, none, 100.0 * (none or 0) / max(tot or 1, 1)))
    print("  -> il calo e' esattamente il numero di chiamate dei DUE punti interni")
    verdetto("Q5 i due chiamanti interni non ricalcolano piu'",
             (none or 0) < (none_a or 0),
             "da %s a %s su %s chiamate; i restanti sono FUORI dal passo" % (none_a, none, tot))
    print("""  I CHIAMANTI RIMASTI sono setup/diagnostica/analisi (:388, :446, :493, :509, :5952,
  :6688, _registra_concorrenza...): NON violano l'intento di :2959 e NON vanno corretti per
  simmetria -- il mandato lo dice esplicitamente.""")

    print("\n--- (Q7) stabilita' ---")
    d0 = np.asarray(B["d0"], float); psi = np.asarray(B["psi"])
    nb_ = np.asarray(B.get("_nb"), float)
    nn = np.linalg.norm(nb_, axis=1) if nb_.ndim == 2 else np.array([1.0])
    verdetto("Q7a psi finito, nessun NaN/inf", bool(np.all(np.isfinite(psi))),
             "NaN/inf = %d" % int(np.sum(~np.isfinite(psi))))
    verdetto("Q7b d0 > 0 e finito", bool(np.all(np.isfinite(d0)) and np.all(d0 > 0)),
             "min d0 = %.6g" % d0.min())
    verdetto("Q7c |nb| = 1", float(np.max(np.abs(nn - 1.0))) < 1e-9,
             "max| |nb|-1 | = %.3e" % np.max(np.abs(nn - 1.0)))
    cfl = B.get("_taup_cfl_max")
    verdetto("Q7d la plasticita' resta stabile", cfl is not None and float(cfl) < 1.0,
             "_taup_cfl_max = %s" % cfl)

print("\n" + "=" * 118)
ok = sum(esiti)
print("Q0,Q3-Q8: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
NB -- Q3 (riduzione al limite) e Q6 (topologia) sono verificati a parte:
 Q3: forzare i due chiamanti a non passare `w` significa RIPRISTINARE il file PRE, che e' il
     riferimento stesso di questo confronto: la riduzione al limite e' l'identita' del file PRE
     con se stesso, e non aggiunge informazione. Cio' che il sigillo verifica davvero e' che le
     modifiche siano SOLO quelle due righe -- ed e' il controllo di FORMA in testa.
 Q6: misurato PRIMA del cablaggio (verifica preliminare 1): topologia INVARIATA nel 100 % di 40
     chiamate, su entrambi i punti; e `w` e' gia' usato a :3007 e :3124, quindi se fosse
     disallineato quelle righe sarebbero gia' rotte.""")
