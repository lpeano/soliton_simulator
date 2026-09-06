"""Analisi COVARIANTE di diaglog (il sistema si estende: N cresce, le d0 si stirano).

Regola del progetto: mai confrontare a passo-coordinata fisso, mai medie che diluiscono con N.
Questo strumento confronta una metrica a N APPAIATO (e riporta il tempo proprio cumulativo),
cosi' ogni verdetto e' covariante. Uso:

    python analisi_covariante.py <metrica> <diag1.csv> [diag2.csv ...] [--n 8000,12000,16000]

Esempio A/B:
    python analisi_covariante.py spin_cluster_modulo out_tw_spinore/diag_on_s1.csv out_tw_spinore/diag_off_s1.csv
"""
import sys, numpy as np

DT = 0.02  # passo coordinata (per tau_cum ~ Sum tau_mean*DT)


def _carica(p):
    rows = []; h = None
    for line in open(p):
        if line.startswith("#"):
            continue
        if h is None:
            h = line.rstrip("\n").split(","); continue
        rows.append(line.rstrip("\n").split(","))
    idx = {c: i for i, c in enumerate(h)}

    def col(nm):
        if nm not in idx:
            return np.full(len(rows), np.nan)
        i = idx[nm]
        out = []
        for r in rows:
            try:
                out.append(float(r[i]))
            except Exception:
                out.append(np.nan)
        return np.array(out)
    return col


def _at_N(n, y, Nq):
    """valore di y interpolato al numero di nodi Nq (misura covariante: a scala appaiata)."""
    m = np.isfinite(n) & np.isfinite(y)
    if m.sum() < 4:
        return np.nan
    n, y = n[m], y[m]
    o = np.argsort(n)
    n, y = n[o], y[o]
    if Nq < n.min() or Nq > n.max():
        return np.nan
    return float(np.interp(Nq, n, y))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__); return
    metrica = args[0]; files = args[1:]
    Ns = [8000, 12000, 16000]
    for a in sys.argv:
        if a.startswith("--n"):
            try:
                Ns = [int(x) for x in a.split("=")[-1].split(",")]
            except Exception:
                pass
    print(f"# metrica '{metrica}' a N APPAIATO (covariante); Ns={Ns}")
    hdr = "file".ljust(40) + "N_fin".rjust(8) + "tau_cum".rjust(9)
    for N in Ns:
        hdr += f"@N={N}".rjust(11)
    print(hdr)
    for p in files:
        col = _carica(p)
        n = col("n"); y = col(metrica); tau = col("tau_mean")
        tau_cum = float(np.nansum(np.maximum(tau, 0.0) * DT))
        riga = p.ljust(40) + f"{int(np.nanmax(n)):>8}" + f"{tau_cum:>9.2f}"
        for N in Ns:
            v = _at_N(n, y, N)
            riga += (f"{v:>11.4f}" if np.isfinite(v) else "        n/a")
        print(riga)


if __name__ == "__main__":
    main()
