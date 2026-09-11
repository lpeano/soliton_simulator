"""CHECK del fix presidio (segno_arco_coer_materia) — presidi di Luca:
 (1) criterio di successo = baseline ~0 (frustrato), NON solo "diverso da +1";
 (2) riporta il NUMERO di archi materia-materia (statistica solida?);
 (3) purezza diaglog: OFF byte-identico con/senza --diaglog (il diaglog non contamina la fisica).
Run corti (150 passi), baseline (NIENTE --orologio-segno)."""
import subprocess, sys, os, pickle, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NEW = os.path.join(ROOT, "soliton_simulator.py")
PY = sys.executable
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", "150",
        "--ogni", "150", "--db-ogni", "150",
        "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
        "--calore-scal", "--deparam-orologio", "--verlet"]


def run(dbpath, diag=None):
    csvp = dbpath + ".cond.csv"
    cmd = [PY, NEW] + BASE + ["--csv", csvp, "--sync-db", dbpath, "--db-cleanup"]
    if diag:
        cmd += ["--diaglog", diag]
    print(">>", "con diaglog" if diag else "SENZA diaglog")
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:]); print("STDERR:", r.stderr[-2000:]); raise SystemExit("run FALLITO")
    return pickle.load(open(dbpath, "rb"))["attrs"]


diagA = os.path.join(HERE, "_check_baseline.csv")
A = run(os.path.join(HERE, "_check_diagA.pkl"), diag=diagA)   # con diaglog
B = run(os.path.join(HERE, "_check_diagB.pkl"))               # senza diaglog

# (3) PUREZZA DIAGLOG: A (con diaglog) vs B (senza) devono avere stato fisico IDENTICO
worst = 0.0; bad = {}
for k in A:
    if k in B and isinstance(A[k], np.ndarray) and isinstance(B[k], np.ndarray) and A[k].dtype != object:
        if A[k].shape != B[k].shape:
            bad[k] = ("SHAPE", A[k].shape, B[k].shape); continue
        if A[k].size:
            d = float(np.max(np.abs(A[k].astype(np.complex128) - B[k].astype(np.complex128))))
            if d > 0:
                bad[k] = d
            worst = max(worst, d)
puro = (not bad) and worst == 0.0
print(f"\n[PRESIDIO 3] purezza diaglog (con vs senza --diaglog): max|A-B|={worst:.3e} "
      f"-> {'PASS byte-identico (il diaglog NON contamina la fisica)' if puro else 'FAIL: ' + str(bad)}")

# (1)+(2) leggi il diaglog baseline: segno_materia deve essere ~0, riporta n_arco_materia
with open(diagA) as f:
    righe = [r for r in f if not r.startswith("#")]
rd = list(csv.DictReader(righe))
def col(c): return np.array([float(r.get(c, "nan") or "nan") for r in rd])
sm = col("segno_arco_coer_materia"); st = col("segno_arco_coer")
nm = col("n_arco_materia"); fneg = col("frac_chi_neg")
sm = sm[np.isfinite(sm)]; st = st[np.isfinite(st)]
print(f"\n[PRESIDIO 1] segno_arco_coer_materia BASELINE (senza firma):")
print(f"   valori: primi3={np.mean(sm[:3]):+.5f}  ultimi3={np.mean(sm[-3:]):+.5f}  media2ameta={np.mean(sm[len(sm)//2:]):+.5f}")
print(f"   costante +1? {'SI (ANCORA DEGENERE!)' if np.allclose(sm, 1.0) else 'NO'}")
media = float(np.mean(sm[len(sm)//2:])); sd = float(np.std(sm[len(sm)//2:]))
if np.allclose(sm, 1.0):
    esito = "DEGENERE (+1 costante) -> STOP"
elif abs(media) < 0.1:
    esito = "~0 FRUSTRATO -> FIX BUONO (metrica discrimina, baseline abeliano come atteso)"
else:
    esito = f"valore alto/strano ({media:+.3f}) -> INVESTIGARE"
print(f"   media2ameta={media:+.5f} sd={sd:.5f} -> {esito}")
print(f"\n[PRESIDIO 2] statistica: n_arco_materia (archi materia-materia usati):")
print(f"   min={int(np.nanmin(nm))} max={int(np.nanmax(nm))} ultimo={int(nm[-1])}  "
      f"(frac_chi_neg ultimo={fneg[-1]:.3f}); segno_arco_coer TOTALE media2ameta={np.mean(st[len(st)//2:]):+.5f}")
