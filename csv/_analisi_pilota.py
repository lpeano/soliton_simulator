import csv, numpy as np, sys

def leggi(path):
    f = open(path); next(f)  # salta la riga di metadata
    return list(csv.DictReader(f))

def m2(rows, col):
    v = np.array([float(x[col]) for x in rows if x.get(col) not in (None, "")])
    h = v[len(v) // 4:]  # dal 25% in poi
    return float(np.mean(h)), float(np.std(h)), len(v)

base = sys.argv[1] if len(sys.argv) > 1 else "csv/deparam_pilota_chi"
on = leggi(f"{base}/on.csv")
off = leggi(f"{base}/off.csv")
print(f"[{base}] righe ON={len(on)} (ultimo step {on[-1]['step']})  OFF={len(off)} (ultimo step {off[-1]['step']})")
print(f"{'osservabile':20s} {'ON media':>12s} {'OFF media':>12s} {'ON-OFF':>11s}   dispersione")
for c in ["segno_arco_coer", "verso_arco_coer", "segno_ov_absmedia", "spin_axis_R"]:
    mo, so, no = m2(on, c)
    mf, sf, nf = m2(off, c)
    print(f"{c:20s} {mo:+12.5f} {mf:+12.5f} {mo-mf:+11.5f}   (sd ON {so:.4f} OFF {sf:.4f})")
