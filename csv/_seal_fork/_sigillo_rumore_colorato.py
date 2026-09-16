# -*- coding: utf-8 -*-
"""SIGILLO del TAGLIO SPETTRALE (`--rumore-colorato`) — N1, N1b, N2, N3, N6, N7.

COSA SI STA SIGILLANDO
----------------------
Il calcio termico del vuoto (`:~1908`) era `rng.normal` INDIPENDENTE a ogni passo: rumore BIANCO,
banda infinita fino a Nyquist. Ora, col flag ON, e' un processo di Ornstein-Uhlenbeck correlato su
`tau_c = LAM/CS_M` (il tempo-luce del solitone: DERIVATO, non scelto), con `dt_n = DT*r`.

IL SIGILLO PIU' IMPORTANTE E' N7, E NON E' OVVIO PERCHE'
--------------------------------------------------------
N1..N6 provano la STRUTTURA (che il ramo OFF sia intatto, che il flag faccia qualcosa, che lo
stato si erediti, che nulla esploda). **Passerebbero IDENTICI anche se la ricorsione usasse `DT`
nudo al posto di `dt_n`** — cioe' col tic di COORDINATA al posto del tempo proprio del nodo, che
e' un frame preferito (par.9). E' ESATTAMENTE il bug gia' preso nello Strato 1, dove S1..S6
passavano identici e solo S7 lo ha stanato. N7 e' quel sigillo, per questo pezzo.

PUREZZA
-------
N2, N3, N7 girano IN-PROCESS con SPIE PURE-READ (`rng.normal` e `ritmo()` avvolti, non
ri-chiamati) su una rete VERA. Nessuna spia scrive stato; la sola lettura extra e' la copia degli
array gia' committati.

USO
---
python csv/_seal_fork/_sigillo_rumore_colorato.py
"""
import contextlib
import io as _io
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PY = sys.executable
NEW = os.path.join(ROOT, "soliton_simulator.py")
OLD = os.path.join(HERE, "_old_sim_pre_rumore.py")
BLOB_PRE = "08784685eeb17835389d248a2d1d07db4f0d1305"   # il blob PRIMA del cablaggio
PASSI = 150
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", str(PASSI),
        "--ogni", str(PASSI), "--db-ogni", str(PASSI),
        "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
        "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
        "--fork-su2", "--fork-su2-mem"]

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-52s %s" % ("PASS" if ok else "FAIL", nome, misura))


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
    """max|A-B| sugli array numerici COMUNI; segnala a parte le shape diverse."""
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


# =============================================================== N1: OFF = BYTE-IDENTICO
print("=" * 104)
print("SIGILLO N1 — flag OFF = BYTE-IDENTICO al codice PRIMA del cablaggio (%d passi, seed 1)" % PASSI)
print("=" * 104)
if not os.path.exists(OLD):
    # ESTRAZIONE BINARIA: con text=True git darebbe newline universali e il file avrebbe un BLOB
    # DIVERSO dall'originale. Il blob e' il timbro (par.2.6) e va conservato byte per byte.
    src = subprocess.run(["git", "cat-file", "-p", BLOB_PRE], cwd=ROOT, capture_output=True)
    with open(OLD, "wb") as f:
        f.write(src.stdout)
    print("  (creato %s dal blob %s = codice PRIMA del taglio spettrale)"
          % (os.path.basename(OLD), BLOB_PRE[:8]))
blob_old = subprocess.run(["git", "hash-object", OLD], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
verdetto("N1.0 il riferimento e' il blob PRE-cablaggio", blob_old == BLOB_PRE,
         "blob(%s) = %s  (atteso %s)" % (os.path.basename(OLD), blob_old[:8], BLOB_PRE[:8]))

A = run(OLD, os.path.join(HERE, "_n1_old.pkl"))
B = run(NEW, os.path.join(HERE, "_n1_off.pkl"))
nA, nB = len(A.get("phi", ())), len(B.get("phi", ()))
# PRESIDIO (2026-09-14): PRIMA le shape. `max|A-B| = 0` su array di shape diversa e' MANCANZA DI
# CONFRONTO, non identita'.
verdetto("N1.0b stesso numero di nodi (il confronto ESISTE)", nA == nB and nA > 0,
         "nodi: PRE = %d, POST(OFF) = %d" % (nA, nB))
worst, bad = diff(A, B)
verdetto("N1 flag OFF vs codice pre-cablaggio: byte-identico", worst == 0.0 and not bad,
         "max|A-B| = %.3e%s" % (worst, "" if not bad else "  DIVERGENTI: " + str(list(bad)[:5])))

# =============================================================== N1b: CONTROLLO POSITIVO
print()
print("=" * 104)
print("SIGILLO N1b — CONTROLLO POSITIVO: con il flag ON i due run DEVONO differire")
print("=" * 104)
print("  Senza questo, N1 non prova che il flag SERVA: passerebbe identico anche su codice morto.")
C = run(NEW, os.path.join(HERE, "_n1_on.pkl"), extra=["--rumore-colorato"])
nC = len(C.get("phi", ()))
worst2, bad2 = diff(B, C)
n_shape = sum(1 for v in bad2.values() if isinstance(v, tuple) and v[0] == "SHAPE")
verdetto("N1b ON != OFF (il flag FA qualcosa)", bool(bad2),
         "nodi OFF = %d, ON = %d;  array divergenti %d (di cui %d per SHAPE);  max|OFF-ON| = %.3e"
         % (nB, nC, len(bad2), n_shape, worst2))

# =============================================================== in-process: N2, N3, N6, N7
print()
print("=" * 104)
print("SIGILLI N2, N3, N6, N7 — in-process sul PERCORSO REALE, con spie PURE-READ")
print("=" * 104)
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"] + BASE + ["--rumore-colorato", "--passi", "1",
                                              "--csv", os.path.join(HERE, "_nrc.csv")]
import soliton_simulator as S  # noqa: E402

_a_cli = S._cli()
S._applica_regime(_a_cli)
with contextlib.redirect_stdout(_io.StringIO()):
    S._applica_flag(_a_cli)
TAU_C = S.LAM / S.CS_M
print("  tau_c = LAM/CS_M = %.4g  = %.0f passi     DT = %.4g     RUMORE_COLORATO = %s"
      % (TAU_C, TAU_C / S.DT, S.DT, S.RUMORE_COLORATO))
print("  TEMPO_SEGNO = %s (se True, dt_n_s puo' essere NEGATIVO: la guardia |dt| serve a quello)"
      % S.TEMPO_SEGNO)


def passo(net):
    S.scuoti_vuoto(net); net.step(); net.mitosi()
    net.rilassa_disegno(); net.memoria_hebbiana_moto()


def scena(seed, n_passi):
    net = S.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(net)
    Nc = S.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    for _ in range(n_passi):
        passo(net)
    return net


# ---- SPIE (pure-read): registrano, non alterano -------------------------------------------
class Spia(object):
    def __init__(self, net):
        self.net = net
        self.draws = []          # tutte le estrazioni normal(), con la loro shape
        self.r = None
        self._rng_vero = net.rng
        self._orig_ritmo = S.Rete.ritmo

    def __enter__(self):
        # `numpy.random.Generator.normal` e' READ-ONLY: non si puo' monkeypatchare il metodo.
        # Si avvolge l'OGGETTO `rng`, che e' un attributo normale della rete: un proxy che
        # inoltra TUTTO all'originale e registra solo le estrazioni `normal`. Pure-read: non
        # cambia ne' l'ordine ne' il numero delle estrazioni, quindi lo stato dell'RNG evolve
        # esattamente come senza spia.
        _spia = self

        class _Proxy(object):
            def __init__(self, vero):
                object.__setattr__(self, "_vero", vero)

            def normal(self, *a, **k):
                v = object.__getattribute__(self, "_vero").normal(*a, **k)
                _spia.draws.append(np.asarray(v).copy())
                return v

            def __getattr__(self, nome):
                return getattr(object.__getattribute__(self, "_vero"), nome)

        self._rng_vero = self.net.rng
        self.net.rng = _Proxy(self.net.rng)

        def ritmo(selfr):
            out = self._orig_ritmo(selfr)
            if selfr is self.net:
                self.r = None if out is None else np.asarray(out, float).copy()
            return out
        S.Rete.ritmo = ritmo
        return self

    def __exit__(self, *exc):
        self.net.rng = self._rng_vero
        S.Rete.ritmo = self._orig_ritmo
        return False


print()
print("  costruzione della scena (30 passi)...")
net = scena(1, 30)
n0 = net.n
xi_prima = np.asarray(getattr(net, "_xi_rumore", np.zeros((0, 3))), float).copy()
print("  nodi %d   len(_xi_rumore) = %d   chiamate %s   fallback %s"
      % (n0, len(xi_prima), getattr(net, "_xi_chiamate", "n/d"), getattr(net, "_xi_fallback", "n/d")))

# ---- N7: il tic e' il TEMPO PROPRIO dt_n = DT*r, non DT --------------------------------------
print()
print("  N7 — un passo con le spie, per ricostruire la ricorsione NODO PER NODO")
with Spia(net) as sp:
    passo(net)
xi_dopo = np.asarray(net._xi_rumore, float).copy()
nn = min(len(xi_prima), len(xi_dopo), n0)
r_vec = np.ones(nn) if sp.r is None else np.asarray(sp.r, float)[:nn]
cand = [d for d in sp.draws if d.ndim == 2 and d.shape[1] == 3 and d.shape[0] >= nn]
print("     estrazioni normal() nel passo: %d   candidate di shape (n,3): %d   r: %s"
      % (len(sp.draws), len(cand), "per nodo" if sp.r is not None else "GLOBALE (r=None)"))

a_prop = np.exp(-np.abs(S.DT * r_vec) / TAU_C)          # LA LEGGE: dt_n = DT*r, per nodo
b_prop = np.sqrt(np.maximum(1.0 - a_prop * a_prop, 0.0))
a_bug = float(np.exp(-abs(S.DT) / TAU_C))               # IL BUG: DT nudo, UGUALE per tutti
b_bug = float(np.sqrt(max(1.0 - a_bug * a_bug, 0.0)))

err_prop, err_bug, quale = None, None, -1
for k, g in enumerate(cand):
    gg = g[:nn]
    e_p = float(np.max(np.abs(xi_dopo[:nn] - (xi_prima[:nn] * a_prop[:, None] + b_prop[:, None] * gg))))
    e_b = float(np.max(np.abs(xi_dopo[:nn] - (xi_prima[:nn] * a_bug + b_bug * gg))))
    if err_prop is None or e_p < err_prop:
        err_prop, err_bug, quale = e_p, e_b, k

verdetto("N7 la ricorsione usa dt_n = DT*r PER NODO",
         err_prop is not None and err_prop < 1e-12,
         "max|xi_misurato - xi_atteso(dt_n)| = %s   (estrazione #%d di %d)"
         % ("n/d" if err_prop is None else "%.3e" % err_prop, quale, len(cand)))
verdetto("N7b col BUG (DT nudo) NON tornerebbe",
         err_bug is not None and err_bug > 1e-9,
         "max|xi_misurato - xi_atteso(DT nudo)| = %s   (dev'essere GRANDE)"
         % ("n/d" if err_bug is None else "%.3e" % err_bug))
verdetto("N7c il ritmo locale CONTA (con DT nudo `a` sarebbe uguale per tutti)",
         float(np.std(a_prop)) > 1e-9,
         "std(a) fra i nodi = %.3e   a in [%.9f, %.9f]   a col bug = %.9f"
         % (float(np.std(a_prop)), float(a_prop.min()), float(a_prop.max()), a_bug))

# ---- N2: riduzione al limite, tau_c -> 0 torna al rumore BIANCO -------------------------------
print()
print("  N2 — tau_c -> 0: la ricorsione deve collassare sul rumore BIANCO (xi = g)")
print("     COME si manda tau_c a zero, e perche' NON alzando CS_M: `tau_c = LAM/CS_M`, ma `cs`")
print("     governa anche il CFL (`beta = 2*zeta*cs/d`, `n2 = ceil(max(beta)*DT/0.2)`, :3062-3073).")
print("     Con CS_M = 1e9 servirebbero ~5e8 SOTTOPASSI: il sigillo non fallisce, SI PIANTA — ed e'")
print("     successo, 46 minuti al 68 %% di CPU prima che me ne accorgessi. Si abbassa invece LAM,")
print("     che NON entra nel conteggio dei sottopassi.")
print("     NON e' una byte-identita' di run intero: l'inizializzazione di xi da N(0,1) consuma")
print("     un'estrazione in piu', ed e' una scelta DICHIARATA (stazionarieta' esatta invece di un")
print("     transitorio di ~40 passi).")
lam_orig = S.LAM
try:
    S.LAM = lam_orig / 1.0e4                         # tau_c = LAM/CS_M -> 4e-5, dt_n/tau_c ~ 250
    tau0 = S.LAM / S.CS_M
    # RETE PICCOLA e NESSUNA massa: a N2 serve solo un passo su cui leggere `xi`, non una scena.
    net2 = S.Rete(2); net2.semina(80)
    for _ in range(4):
        passo(net2)
    xi2_prima = np.asarray(getattr(net2, "_xi_rumore", np.zeros((0, 3))), float).copy()
    with Spia(net2) as sp2:
        passo(net2)
    xi2 = np.asarray(net2._xi_rumore, float).copy()
    m2 = min(len(xi2), len(xi2_prima), net2.n)
    cand2 = [d for d in sp2.draws if d.ndim == 2 and d.shape[1] == 3 and d.shape[0] >= m2]
    e2 = min([float(np.max(np.abs(xi2[:m2] - d[:m2]))) for d in cand2]) if cand2 else None
    a0 = float(np.exp(-S.DT / tau0))
    verdetto("N2 tau_c -> 0: xi collassa su g (rumore BIANCO)",
             e2 is not None and e2 < 1e-9,
             "tau_c = %.3e (= %.4g passi)   a = %.3e   max|xi - g| = %s su %d nodi"
             % (tau0, tau0 / S.DT, a0, "n/d" if e2 is None else "%.3e" % e2, m2))
finally:
    S.LAM = lam_orig

# ---- N3: lo stato xi e' ESTESO alla mitosi ----------------------------------------------------
print()
print("  N3 — `_xi_rumore` esteso alla mitosi (il difetto di C7 e C11, scritto PRIMA stavolta)")
net3 = scena(3, 5)
# IL CONTATORE VA LETTO COME DELTA, NON IN ASSOLUTO. Il ramo di estensione scatta LEGITTIMAMENTE
# quando i nodi crescono SENZA passare da `_eredita_spinore_figli`: e' il caso di `semina()` e di
# `nuova_massa()`, cioe' della COSTRUZIONE DELLA SCENA (la terza via di crescita, voce H del
# registro). Li' l'estensione e' CORRETTA: i nodi esistenti conservano il loro `xi` (vstack sulla
# testa) e solo i NUOVI ricevono un'estrazione stazionaria — un nodo appena nato non ha passato.
# Cio' che NON deve succedere e' che scatti sulla MITOSI, dove l'eredita' deve bastare.
_fall0 = int(getattr(net3, "_xi_fallback", 0))
_chiam0 = int(getattr(net3, "_xi_chiamate", 0))
print("     alla fine della costruzione della scena: fallback %d su %d chiamate"
      " (semina + 3 nuova_massa: LEGITTIMO, non passano da _eredita_spinore_figli)"
      % (_fall0, _chiam0))
lung, nodi, ok3 = [], [], True
for _ in range(25):
    passo(net3)
    L = len(getattr(net3, "_xi_rumore", ()))
    lung.append(L); nodi.append(net3.n)
    if L != net3.n:
        ok3 = False
chiam = int(getattr(net3, "_xi_chiamate", 0))
fall = int(getattr(net3, "_xi_fallback", 0))
cresciuti = sum(1 for k in range(1, len(nodi)) if nodi[k] != nodi[k - 1])
verdetto("N3 len(_xi_rumore) == n dopo OGNI passo", ok3,
         "25 passi, n da %d a %d, passi con mitosi/potatura %d;  disallineamenti %d"
         % (nodi[0], nodi[-1], cresciuti, sum(1 for k in range(len(lung)) if lung[k] != nodi[k])))
verdetto("N3b sulla MITOSI il ramo di estensione NON scatta (P5)", (fall - _fall0) == 0,
         "estensioni durante i 25 passi: %d su %d chiamate (prima dei passi erano %d su %d, dalla "
         "costruzione della scena). Se fosse > 0, l'eredita' alla mitosi non basterebbe."
         % (fall - _fall0, chiam - _chiam0, _fall0, _chiam0))

# ---- N6: stabilita' ---------------------------------------------------------------------------
print()
print("  N6 — stabilita' sul run ON (dal DB del run N1b, %d passi)" % PASSI)
nbC = np.asarray(C.get("_nb"), float)
nrm = np.linalg.norm(nbC, axis=1) if nbC.ndim == 2 and nbC.size else np.array([np.nan])
finiti = all(np.all(np.isfinite(np.asarray(C[k], dtype=np.complex128)))
             for k in C if isinstance(C[k], np.ndarray) and C[k].dtype != object and C[k].size)
scala = float(np.max(np.abs(np.asarray(C.get("pos"), float)))) if C.get("pos") is not None else np.nan
verdetto("N6a |nb| = 1 su tutti i nodi (run ON)", float(np.max(np.abs(nrm - 1.0))) < 1e-9,
         "max| |nb| - 1 | = %.3e su %d nodi" % (float(np.max(np.abs(nrm - 1.0))), len(nrm)))
verdetto("N6b nessun NaN/inf in tutto lo stato (run ON)", finiti, "tutti finiti")
verdetto("N6c nessun runaway di scala (run ON)", np.isfinite(scala) and scala < 1e6,
         "max|x| = %.4g" % scala)

# ---- N4/N5: theta nelle DUE convenzioni e omega/sqrt(n) ---------------------------------------
print()
print("=" * 104)
print("N4 / N5 — theta nelle DUE convenzioni e omega, ON vs OFF (dai DB dei run N1/N1b)")
print("=" * 104)
print("  ⚠ NON E' UN VERDETTO FISICO: 1 seme, %d passi, e la barra giusta e' la dispersione FRA" % PASSI)
print("    SEMI (~0.03, C10), non questa. Serve solo a vedere il SEGNO e l'ORDINE DI GRANDEZZA.")
for eti, D in (("OFF", B), ("ON ", C)):
    om = np.asarray(D.get("omega_s"), float)
    n_ = len(D.get("phi", ()))
    if om.ndim == 2 and om.size:
        omn = np.linalg.norm(om[:n_], axis=1)
        th_coord = np.degrees(omn * S.DT)
        print("  %s  n %5d   |omega| mediana %10.4g   theta_coord mediana %10.4g giri/passo"
              "   omega/sqrt(n) %10.4g"
              % (eti, n_, float(np.median(omn)), float(np.median(th_coord)) / 360.0,
                 float(np.median(omn)) / np.sqrt(max(n_, 1))))
print("  (theta_PROP richiede `r`, che non e' nel DB: lo da' la campagna con l'osservatore.)")

print()
print("=" * 104)
print("SIGILLO RUMORE COLORATO: %d/%d PASS -> %s"
      % (sum(esiti), len(esiti), "PASS" if all(esiti) else "FAIL"))
print("=" * 104)
print("""COSA QUESTO SIGILLO NON DICE
---------------------------
Che il taglio spettrale MIGLIORI qualcosa. La predizione, scritta PRIMA
(doc/PREDIZIONE_taglio_spettrale.md), dice che `theta` NON scende e semmai SALE di <= 5 %: la
ricorsione PRESERVA la varianza, e il canale su cui agisce vale il 4 % dell'ingresso di `omega`
(R_stoc = 0.041 contro errore atteso 0.097, C6). Si e' cablato perche' il rumore bianco e'
fisicamente SBAGLIATO, non perche' risolva l'aliasing.
Il verdetto fisico lo da' la campagna {OFF, ON} x >= 2 semi, non questo sigillo.""")
sys.exit(0 if all(esiti) else 1)
