# -*- coding: utf-8 -*-
"""SIGILLO PEZZO 3 — cablaggio dell'arc-connection SU(2) nella forza (flag --fork-su2).

Qui il fork smette di essere una funzione isolata: entra nella dinamica. Quindi il sigillo
"OFF = byte-identico" NON vale piu' per costruzione (c'e' un call-site) e va verificato con
DUE RUN VERI, confrontando tutti gli array dello stato.

SIGILLI (CLAUDE.md par.2):
  1. FLAG OFF = BYTE-IDENTICO al codice precedente al cablaggio      -> max|A-B| = 0.000e+00
  2. RIDUZIONE AL LIMITE: Bloch allineati -> ramo ON identico al ramo scalare
  3. NORMA |psi| = 1, nessun NaN/inf
  4. STABILITA': nessun runaway nella finestra provata
  5. AZIONE-REAZIONE: la somma della coppia su tutti i nodi resta nulla (hermitianita' del
     trasporto: senza, la coppia i-j creerebbe momento dal nulla)
  6. IL FLAG ON FA QUALCOSA (se ON == OFF il cablaggio e' morto)

NB sulla finestra: 150 passi bastano per un BYTE-IDENTICO (una divergenza si manifesta al primo
passo) e per un no-runaway, NON per una conclusione fisica. Il par.2.7 (niente conclusioni sotto
~2000 passi, mai un solo seme) riguarda la FISICA, non i sigilli tecnici: qui non si conclude
nulla sulla fisica.
"""
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NEW = os.path.join(ROOT, "soliton_simulator.py")
OLD = os.path.join(HERE, "_old_sim_pre_pezzo3.py")
PY = sys.executable
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", "150",
        "--ogni", "150", "--db-ogni", "150",
        "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
        "--calore-scal", "--deparam-orologio", "--verlet"]

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-46s %s" % ("PASS" if ok else "FAIL", nome, misura))


def run(sim, dbpath, extra=()):
    cmd = [PY, sim] + BASE + list(extra) + ["--csv", dbpath + ".cond.csv",
                                            "--sync-db", dbpath, "--db-cleanup"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-1500:])
        print("STDERR:", r.stderr[-1500:])
        raise SystemExit("run FALLITO: " + " ".join(cmd[1:6]))
    with open(dbpath, "rb") as f:
        return pickle.load(f)["attrs"]


def diff(A, B):
    """max|A-B| su tutti gli array numerici comuni; segnala shape diverse."""
    worst = 0.0
    bad = {}
    for k in A:
        if k in B and isinstance(A[k], np.ndarray) and isinstance(B[k], np.ndarray) \
                and A[k].dtype != object:
            if A[k].shape != B[k].shape:
                bad[k] = ("SHAPE", A[k].shape, B[k].shape)
                continue
            if A[k].size:
                d = float(np.max(np.abs(A[k].astype(np.complex128) - B[k].astype(np.complex128))))
                if d > 0:
                    bad[k] = d
                worst = max(worst, d)
    return worst, bad


# ---------------------------------------------------------------- SIGILLO 1: OFF byte-identico
print("=" * 92)
print("SIGILLO 1 — FLAG OFF = BYTE-IDENTICO (due run veri, 150 passi, seed 1)")
print("=" * 92)
if not os.path.exists(OLD):
    with open(OLD, "w", encoding="utf-8", newline="") as f:
        f.write(subprocess.run(["git", "show", "HEAD:soliton_simulator.py"], cwd=ROOT,
                               capture_output=True, text=True).stdout)
    print("  (creato %s da HEAD = codice PRIMA del cablaggio)" % os.path.basename(OLD))
A = run(OLD, os.path.join(HERE, "_p3_old.pkl"))
B = run(NEW, os.path.join(HERE, "_p3_off.pkl"))
worst, bad = diff(A, B)
verdetto("S1 OFF vs codice pre-cablaggio", worst == 0.0 and not bad,
         "max|A-B| = %.3e%s" % (worst, "" if not bad else "  DIVERGENTI: " + str(list(bad)[:5])))

# ---------------------------------------------------------------- SIGILLO 6: ON fa qualcosa
print()
print("=" * 92)
print("SIGILLO 6 — IL FLAG ON FA QUALCOSA (se ON == OFF il cablaggio e' morto)")
print("=" * 92)
C = run(NEW, os.path.join(HERE, "_p3_on.pkl"), extra=["--fork-su2"])
worst_on, _ = diff(B, C)
verdetto("S6 ON != OFF (il cablaggio e' vivo)", worst_on > 0.0, "max|OFF-ON| = %.3e" % worst_on)

# ---------------------------------------------------------------- SIGILLI 3/4: norma, NaN, runaway
print()
print("=" * 92)
print("SIGILLI 3 e 4 — norma |psi| = 1, nessun NaN/inf, nessun runaway (run ON)")
print("=" * 92)
psp = C.get("_psi_spinor")
if psp is not None and len(psp):
    nor = np.linalg.norm(np.asarray(psp), axis=1)
    verdetto("S3 norma |psi| = 1 sullo spinore", np.max(np.abs(nor - 1.0)) < 1e-9,
             "max| |psi| - 1 | = %.3e su %d nodi" % (np.max(np.abs(nor - 1.0)), len(nor)))
else:
    verdetto("S3 norma |psi| = 1 sullo spinore", False, "_psi_spinor assente nello stato")
finiti = all(np.all(np.isfinite(v)) for v in C.values()
             if isinstance(v, np.ndarray) and v.dtype != object
             and np.issubdtype(v.dtype, np.number))
verdetto("S4a nessun NaN/inf in tutto lo stato (ON)", finiti, "tutti finiti")
nb_on, nb_off = C.get("n", None), B.get("n", None)
pos = C.get("x", None)
scala = float(np.max(np.abs(np.asarray(pos)))) if pos is not None and len(pos) else float("nan")
verdetto("S4b nessun runaway di scala nella finestra", np.isfinite(scala) and scala < 1e6,
         "max|x| = %.4g  (N_on = %s, N_off = %s)" % (scala, nb_on, nb_off))

# ---------------------------------------------------------------- SIGILLI 2 e 5: in-process
print()
print("=" * 92)
print("SIGILLO 2 — RIDUZIONE AL LIMITE: Bloch allineati -> ON identico al ramo scalare")
print("=" * 92)
sys.path.insert(0, ROOT)
import soliton_simulator as S  # noqa: E402


class FintaRete(object):
    """Guscio minimo: espone solo cio' che `_coppia_interferenza` usa (n, i, j, _psi_spinor,
    struttura sparsa). Non fa fisica: serve a confrontare i DUE RAMI sullo stesso stato."""
    _S = None
    _perm = None
    n = 0
    i = None
    j = None

    _costruisci_struttura = S.Rete._costruisci_struttura
    _mat = S.Rete._mat
    _mat2 = S.Rete._mat2
    _link_su2_N = staticmethod(S.Rete._link_su2_N)
    _coppia_interferenza = S.Rete._coppia_interferenza


def prepara(nodi, seed, allineati):
    g = np.random.default_rng(seed)
    r = FintaRete()
    r.n = nodi
    ii, jj = np.triu_indices(nodi, 1)
    sel = g.random(len(ii)) < 0.45
    r.i, r.j = ii[sel], jj[sel]
    r._S = None
    if allineati:
        # STESSO Bloch per tutti (+z) ma FASI GLOBALI DIVERSE: e' il caso che con il peso
        # sin(chi) faceva perdere il canale EM. Qui deve ridurre ESATTAMENTE allo scalare.
        ps = np.zeros((nodi, 2), complex)
        ps[:, 0] = np.exp(1j * g.random(nodi) * 2 * np.pi)
    else:
        ps = g.normal(size=(nodi, 2)) + 1j * g.normal(size=(nodi, 2))
        ps /= np.linalg.norm(ps, axis=1)[:, None]
    r._psi_spinor = ps
    A = g.normal(size=len(r.i))
    z = np.exp(1j * g.random(nodi) * 2 * np.pi)
    return r, A, z


def coppia(r, A, z, fork):
    vecchio = S.FORK_SU2
    S.FORK_SU2 = fork
    try:
        return np.asarray(S.Rete._coppia_interferenza(r, A, z)).copy()
    finally:
        S.FORK_SU2 = vecchio


S.CAMPO_SPINORIALE = True
r, A, z = prepara(60, 4242, allineati=True)
c_off = coppia(r, A, z, False)
c_on = coppia(r, A, z, True)
d = float(np.max(np.abs(c_on - c_off)))
verdetto("S2 allineati: ON == ramo scalare", d < 1e-12,
         "max|ON - OFF| = %.3e  (con il peso sin(chi) qui si perdeva l'EM)" % d)

r2, A2, z2 = prepara(60, 909, allineati=False)
c_off2 = coppia(r2, A2, z2, False)
c_on2 = coppia(r2, A2, z2, True)
verdetto("S2b Bloch generici: ON != scalare (mescola a,b)",
         float(np.max(np.abs(c_on2 - c_off2))) > 1e-6,
         "max|ON - OFF| = %.3e" % float(np.max(np.abs(c_on2 - c_off2))))

print()
print("=" * 92)
print("SIGILLO 5 — AZIONE-REAZIONE: la somma della coppia su tutti i nodi resta nulla")
print("=" * 92)
for nome, cc in (("ramo scalare (OFF)", c_off2), ("arc-connection (ON)", c_on2)):
    tot = float(np.sum(cc))
    scala_ = float(np.max(np.abs(cc))) or 1.0
    verdetto("S5 somma coppia ~ 0 — %s" % nome, abs(tot) < 1e-9 * max(scala_, 1.0) * len(cc),
             "sum = %+.3e  (max|c| = %.3e)" % (tot, scala_))

print("=" * 92)
tot_, ok_ = len(esiti), sum(esiti)
print("SIGILLO PEZZO 3: %d/%d PASS -> %s" % (ok_, tot_, "PASS" if ok_ == tot_ else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
Che il cablaggio sia CORRETTO e SICURO, non che la fisica che produce sia giusta. Non e' stata
misurata l'olonomia W(r) (doc/PROTOCOLLO_test_olonomia.md), ne' la stabilita' su orizzonti lunghi
(par.2.7: niente conclusioni sotto ~2000 passi, mai un solo seme). Il flag resta OFF di default.
""")
sys.exit(0 if ok_ == tot_ else 1)
