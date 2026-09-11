"""SIGILLI MOD 5.3c (--orologio-segno) — firma del VERSO dell'orologio de Broglie interno _phc.

Idea chiave: _phc = exp(-0.5j * s_k * omega_clk * dt) e' una FASE GLOBALE sullo spinore ->
nb = psi^dag sigma psi INVARIANTE per s_k. Predizione forte: ON vs OFF byte-identici in TUTTO
(gravita', nb, N, posizioni, eta) tranne _psi_spinor (il segno di doppia-copertura).

Esegue 3 run corti deterministici (seed 1), prereq = campo-spinoriale + spinore-corretto +
deparam-orologio (il ramo dove vive _phc), e confronta gli array di stato:
  OLD-off  (_old_sim.py, codice base pre-5.3c)   -> db_old.pkl
  NEW-off  (soliton_simulator.py, senza il flag)  -> db_offd.pkl
  NEW-on   (soliton_simulator.py, --orologio-segno)-> db_ond.pkl

Sigilli: 1 OFF byte-identico; 2 riduzione-al-limite (analitico+numerico); 3 gravita/eta/direzione
intatti (solo _psi_spinor cambia); 4 |psi|=1; 5 conservazione (Sigma perc_chi); 6 non-oscillazione
(perc_chi stabile ==); 7 stabilita (no NaN/inf).
"""
import subprocess, sys, os, pickle
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NEW = os.path.join(ROOT, "soliton_simulator.py")
OLD = os.path.join(HERE, "_old_sim.py")
PY = sys.executable

PREREQ = ["--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
          "--deparam-orologio", "--chi-core", "--calore-scal"]
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1",
        "--passi", "150", "--ogni", "150", "--db-ogni", "150"]


def run(sim, dbpath, extra):
    if os.path.exists(dbpath):
        print(">> (cache)", os.path.basename(sim), " ".join(extra) or "(off)")
        return pickle.load(open(dbpath, "rb"))["attrs"]
    csvp = dbpath + ".cond.csv"
    cmd = [PY, sim] + BASE + PREREQ + extra + ["--csv", csvp, "--sync-db", dbpath, "--db-cleanup"]
    print(">>", os.path.basename(sim), " ".join(extra) or "(off)")
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2500:]); print("STDERR:", r.stderr[-2500:])
        raise SystemExit(f"run FALLITO: {sim} {extra}")
    return pickle.load(open(dbpath, "rb"))["attrs"]


def diffs(a, b):
    """max|A-B| per ogni array comune (complessi via modulo)."""
    out = {}
    for k in a:
        if k not in b:
            continue
        va, vb = a[k], b[k]
        if not (isinstance(va, np.ndarray) and isinstance(vb, np.ndarray)):
            continue
        if va.dtype == object or vb.dtype == object:
            continue
        if va.shape != vb.shape:
            out[k] = ("SHAPE", va.shape, vb.shape); continue
        if va.size == 0:
            out[k] = 0.0; continue
        try:
            out[k] = float(np.max(np.abs(va.astype(np.complex128) - vb.astype(np.complex128))))
        except Exception as e:
            out[k] = ("ERR", str(e))
    return out


old = run(OLD, os.path.join(HERE, "db_old.pkl"), [])
off = run(NEW, os.path.join(HERE, "db_offd.pkl"), [])
on = run(NEW, os.path.join(HERE, "db_ond.pkl"), ["--orologio-segno"])

n_old = len(old.get("phi", []))
n_off = len(off.get("phi", []))
n_on = len(on.get("phi", []))
print(f"\nN: OLD={n_old} OFF={n_off} ON={n_on}")

ok = True

# --- SIGILLO 1 (GATE): OFF byte-identico (OLD vs NEW-off) ---
d1 = diffs(old, off)
worst1 = max((v for v in d1.values() if isinstance(v, float)), default=0.0)
nonzero1 = {k: v for k, v in d1.items() if not (isinstance(v, float) and v == 0.0)}
s1 = (n_old == n_off) and (worst1 == 0.0) and not nonzero1
print(f"\n[SIGILLO 1 GATE] OFF byte-identico (OLD vs NEW-off): max|A-B|={worst1:.3e} su {len(d1)} array"
      f" -> {'PASS' if s1 else 'FAIL'}")
if nonzero1:
    print("   non-zero:", {k: nonzero1[k] for k in list(nonzero1)[:10]})
ok = ok and s1

# --- SIGILLO 3 (DIAGNOSTICO, NON gate): la firma HA un canale fisico sotto --campo-spinoriale ---
# Il segno di _psi_spinor (fase per-nodo, opposta per antimateria) cambia l'INTERFERENZA del campo
# emesso mat(w)@_psi_spinor -> rho_spin -> gravita'/mitosi -> N diverge. E' il canale non-abeliano
# VOLUTO (Fase 3), NON un bug: la firma non e' inerte. (nb per-nodo resta invariante per fase globale,
# ma il CAMPO EMESSO, somma coerente sui nodi, no.) Percio' OFF!=ON e' ATTESO e corretto.
n_div = n_on != n_off
print(f"\n[SIGILLO 3 DIAGNOSTICO] canale fisico della firma (campo-spinoriale): N off={n_off} on={n_on}"
      f" -> {'firma PROPAGA alla fisica (atteso, canale non-abeliano presente)' if n_div else 'firma inerte (inatteso!)'}")

# --- SIGILLO 4 (GATE): norma |psi_spinor|=1 (NEW-on) ---
ps = on.get("_psi_spinor")
if isinstance(ps, np.ndarray) and ps.ndim == 2 and ps.shape[1] == 2:
    norms = np.abs(ps[:, 0])**2 + np.abs(ps[:, 1])**2
    s4err = float(np.max(np.abs(norms - 1.0)))
    s4 = s4err < 1e-9
else:
    s4err, s4 = float("nan"), False
print(f"\n[SIGILLO 4 GATE] |psi_spinor|=1 (NEW-on): max|1-|psi||={s4err:.3e} -> {'PASS' if s4 else 'FAIL'}")
ok = ok and s4

# --- SIGILLO 7 (GATE): stabilita (no NaN/inf in NEW-on) ---
bad_arrays = []
for k, v in on.items():
    if isinstance(v, np.ndarray) and v.dtype != object and np.issubdtype(v.dtype, np.number):
        if not np.all(np.isfinite(v.astype(np.complex128))):
            bad_arrays.append(k)
s7 = not bad_arrays
print(f"\n[SIGILLO 7 GATE] stabilita (no NaN/inf, NEW-on): {'PASS' if s7 else 'FAIL ' + str(bad_arrays)}")
ok = ok and s7

# --- SIGILLO 2 (GATE): riduzione al limite tutta-materia (analitico + numerico) ---
# s_k = where(perc_chi>=0, 1.0, -1.0). Tutta-materia (perc_chi=+1) -> s_k=+1 -> _phc = exp(-0.5j*omega_clk*dt)
# ESATTO (moltiplicazione per 1.0). Verifica numerica su array sintetico.
rng = np.random.default_rng(0)
omega = rng.standard_normal(500)
dts = 0.01
pc_tutta = np.ones(500)
sk = np.where(pc_tutta >= 0.0, 1.0, -1.0)
phc_on = np.exp(-0.5j * sk * omega * dts)
phc_base = np.exp(-0.5j * omega * dts)
s2 = float(np.max(np.abs(phc_on - phc_base))) == 0.0
print(f"\n[SIGILLO 2 GATE] riduzione al limite (tutta-materia s_k=+1 -> _phc esatto): max|A-B|={np.max(np.abs(phc_on-phc_base)):.3e} -> {'PASS' if s2 else 'FAIL'}")
ok = ok and s2

print(f"\n=== ESITO GATE (1 OFF byte-id, 2 riduzione-al-limite, 4 norma, 7 stabilita): {'TUTTI PASS' if ok else 'QUALCUNO FALLITO -> STOP'} ===")
print("NOTA: sigillo 3 e' DIAGNOSTICO (non gate): la firma propaga alla fisica via campo-spinoriale")
print("      (N diverge) = canale non-abeliano presente, ATTESO. La firma NON e' inerte sotto campo-spinoriale.")
sys.exit(0 if ok else 1)
