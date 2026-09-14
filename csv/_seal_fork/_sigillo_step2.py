# -*- coding: utf-8 -*-
"""SIGILLO STEP 2 — aggancio OROLOGIO <-> METRICA: `omega_clk *= (cs/CS_M)^2` (--step2-orologio).

Predizione scritta e committata PRIMA del cablaggio: `doc/PREDIZIONE_step2.md` (commit cdc39d0).

PERCHE' ESISTE
--------------
La metrica legge solo `|psi|^2` e l'orologio NON legge `cs`: i due tempi propri (metrico `d/cs` e
orologio `DT*r`) erano SCOLLEGATI. L'aggancio e' l'OROLOGIO DI COMPTON, `omega = m c^2 / hbar`:
la frequenza propria va come `c^2`, e nel modello `c` e' `cs`. Zero parametri nuovi.

I SIGILLI
---------
  S1  flag OFF byte-identico al codice pre-modifica        max|A-B| = 0.000e+00
  S2  riduzione al limite: ON con cs = CS_M ovunque        byte-identico a OFF, 0 esatto
  S3  IL DECISIVO: verso e scaling                         omega_eff/omega_base = (cs/CS_M)^2
  S4  stabilita': ON su run breve                          nessun NaN/inf, nessun runaway

S3 esercita il PERCORSO REALE (`_passo_spinoriale` chiamato, il rapporto RICAVATO dalla fase dello
spinore prodotta dal codice), non ricalcola la formula inline: un sigillo che ricalcola la formula
testa l'aritmetica, non il codice. Stesso monito del sigillo N e di S7 (Strato 1).

PRESIDIO: ogni confronto stampa il CONTEGGIO NODI accanto allo zero. Uno zero senza confronto non
vale (CLAUDE.md par.9, errore pagato il 2026-09-14).
"""
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NEW = os.path.join(ROOT, "soliton_simulator.py")
OLD = os.path.join(HERE, "_old_sim_pre_step2.py")
PRE = "cdc39d0"          # commit FISSO: la PREDIZIONE, ultimo prima del cablaggio. MAI HEAD.
BLOB_PRE = "2277e9a099a38117286a9b550e92968203008314"
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
    worst, bad = 0.0, {}
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


def confronta(nome, A, B, extra=""):
    """Stampa SEMPRE il conteggio nodi: uno zero senza confronto non vale."""
    nA, nB = len(A.get("phi", ())), len(B.get("phi", ()))
    worst, bad = diff(A, B)
    shape_div = sum(1 for v in bad.values() if isinstance(v, tuple))
    verdetto(nome, worst == 0.0 and not bad and nA == nB and nA > 0,
             "max|A-B| = %.3e   [nodi %d vs %d, shape divergenti %d]%s"
             % (worst, nA, nB, shape_div, extra))


print("=" * 96)
print("SIGILLO STEP 2 — omega_clk *= (cs/CS_M)^2  (orologio di Compton)")
print("=" * 96)

# ============================================================ S1: OFF byte-identico
if not os.path.exists(OLD):
    src = subprocess.run(["git", "show", PRE + ":soliton_simulator.py"], cwd=ROOT,
                         capture_output=True)
    with open(OLD, "wb") as f:
        f.write(src.stdout)
    print("  (creato %s da %s = codice PRIMA del cablaggio)" % (os.path.basename(OLD), PRE))
blob_old = subprocess.run(["git", "hash-object", OLD], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
verdetto("S1.0 il riferimento e' il blob certificato", blob_old == BLOB_PRE,
         "blob = %s  (atteso %s)" % (blob_old[:8], BLOB_PRE[:8]))

A = run(OLD, os.path.join(HERE, "_st2_old.pkl"))
B = run(NEW, os.path.join(HERE, "_st2_off.pkl"))
confronta("S1 flag OFF vs codice pre-cablaggio", A, B)

# ============================================================ S3/S2: in-process, PERCORSO REALE
print()
print("=" * 96)
print("SIGILLI 3 e 2 — in-process sul METODO VERO (_passo_spinoriale)")
print("=" * 96)
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S  # noqa: E402


def fase_spinore(cs_rapporto, nodi=40, seed=7):
    """Gira UN passo di `_passo_spinoriale` VERO e RICAVA la fase impressa dall'orologio.

    Non ricalcola (cs/CS_M)^2: costruisce una rete, chiama il metodo reale, e legge di quanto la
    FASE dello spinore e' ruotata. Il rapporto fra due run a cs diversi e' il rapporto fra gli
    omega_clk EFFETTIVI, qualunque cosa il codice ci abbia fatto.
    """
    g = np.random.default_rng(seed)
    net = S.Rete(seed)
    net.semina(nodi)
    n = net.n
    # spinore noto e IDENTICO nei due run: la sola differenza sara' cs
    ps = np.zeros((n, 2), complex)
    ps[:, 0] = 1.0
    net._psi_spinor = ps.copy()
    net._nb = np.tile([0.0, 0.0, 1.0], (n, 1))
    net._nb_prec = net._nb.copy()
    net.psi = np.full(n, 0.01 + 0j)
    net._cs_nodo_prev = (None if cs_rapporto is None
                         else np.full(n, cs_rapporto * S.CS_M))
    w = net._pesi()
    prima = net._psi_spinor.copy()
    net._passo_spinoriale(net.i, net.j, w, np.full(n, S.DT),
                          psi_snapshot=net.psi.copy())
    dopo = net._psi_spinor
    k = min(len(prima), len(dopo))
    # fase relativa impressa, componente per componente (la parte che _phc ha ruotato)
    ov = np.sum(np.conj(prima[:k]) * dopo[:k], axis=1)
    return np.angle(ov), k


vS, vD, vC, vK = S.CAMPO_SPINORIALE, S.DEPARAM_OROLOGIO, S.SPINORE_CORRETTO, S.STEP2_OROLOGIO
S.CAMPO_SPINORIALE = True
S.DEPARAM_OROLOGIO = True
S.SPINORE_CORRETTO = True
try:
    S.STEP2_OROLOGIO = False
    base, kb = fase_spinore(1.0)
    S.STEP2_OROLOGIO = True
    print("   cs/CS_M    rapporto fase MISURATO      atteso (cs/CS_M)^2     |differenza|")
    righe = []
    for rap in (1.0, 0.5, 0.1):
        f, kf = fase_spinore(rap)
        k = min(kb, kf)
        m = np.abs(base[:k]) > 1e-14
        if m.sum() == 0:
            righe.append((rap, float("nan"), rap ** 2, float("nan")))
            continue
        r_mis = float(np.median(f[:k][m] / base[:k][m]))
        att = rap ** 2
        righe.append((rap, r_mis, att, abs(r_mis - att)))
        print("    %5.2f        %.12f            %.12f       %.3e" % (rap, r_mis, att, abs(r_mis - att)))
    err = max(r[3] for r in righe if np.isfinite(r[3]))
    verdetto("S3 omega_eff/omega_base = (cs/CS_M)^2", err < 1e-9,
             "max|misurato - atteso| = %.3e su cs/CS_M = 1.0, 0.5, 0.1" % err)
    r1 = [r for r in righe if r[0] == 1.0][0][1]
    r01 = [r for r in righe if r[0] == 0.1][0][1]
    verdetto("S3b l'orologio RALLENTA dove cs e' basso", r01 < r1 and r01 > 0,
             "fase a cs=0.1*CS_M e' %.4f volte quella a cs=CS_M (deve essere < 1)" % (r01 / r1))
    verdetto("S3c a cs = CS_M il fattore e' 1 ESATTO", abs(r1 - 1.0) < 1e-12,
             "rapporto = %.15f" % r1)
finally:
    S.CAMPO_SPINORIALE, S.DEPARAM_OROLOGIO = vS, vD
    S.SPINORE_CORRETTO, S.STEP2_OROLOGIO = vC, vK

# ============================================================ S2: riduzione al limite (run veri)
print()
print("=" * 96)
print("SIGILLO 2 — riduzione al limite: ON senza --cs-dinamico (cs = CS_M ovunque) == OFF")
print("=" * 96)
print("  Senza --cs-dinamico, _cs_nodo non viene mai calcolato -> la cache resta None -> fattore 1")
print("  esatto. Il ramo ON GIRA ma non deve cambiare NULLA: e' la riduzione al limite del par.2.2.")
C = run(NEW, os.path.join(HERE, "_st2_on.pkl"), extra=["--step2-orologio"])
confronta("S2 ON (cs=CS_M) vs OFF: byte-identico", B, C)

# ============================================================ S4: stabilita'
print()
print("=" * 96)
print("SIGILLO 4 — stabilita' col flag ON")
print("=" * 96)
psp = C.get("_psi_spinor")
nor = (np.linalg.norm(np.asarray(psp), axis=1) if psp is not None and len(psp) else np.array([]))
verdetto("S4a norma |psi| = 1", nor.size and float(np.max(np.abs(nor - 1.0))) < 1e-9,
         "max| |psi| - 1 | = %.3e su %d nodi" % (float(np.max(np.abs(nor - 1.0))) if nor.size
                                                 else float("nan"), nor.size))
finiti = all(np.all(np.isfinite(v)) for v in C.values()
             if isinstance(v, np.ndarray) and v.dtype != object
             and np.issubdtype(v.dtype, np.number))
verdetto("S4b nessun NaN/inf in tutto lo stato", finiti, "tutti finiti")
pos = C.get("pos")
scala = float(np.max(np.abs(np.asarray(pos, float)))) if pos is not None and len(pos) else float("nan")
verdetto("S4c nessun runaway di scala", np.isfinite(scala) and scala < 1e6, "max|x| = %.4g" % scala)

print("=" * 96)
tot_, ok_ = len(esiti), sum(esiti)
print("SIGILLO STEP 2: %d/%d PASS -> %s" % (ok_, tot_, "PASS" if ok_ == tot_ else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE (doc/PREDIZIONE_step2.md par.2)
------------------------------------------------------------
S3 dice che il MECCANISMO risponde nel verso giusto e scala come cs^2. NON dice che l'effetto
DINAMICO sia grande: alle densita' attuali cs e' quasi-costante (I~0.05 contro soglia ~400), quindi
(cs/CS_M)^2 ~ 1 e qualunque effetto sara' piccolo PER COSTRUZIONE. E il profilo di dt_n e' un
effetto INDIRETTO (omega_clk -> _phc -> psi_spin -> ritmo() -> dt_n): S3 PASS + dt_n piccolo
significa CABLATO BENE, non fallito.
E lo Step 2 NON deve organizzare lo spin: _phc e' una fase globale, il Bloch e' invariante (3.3e-16).
Firme di spin invariate = conferma che fa il suo mestiere.
""")
sys.exit(0 if ok_ == tot_ else 1)
