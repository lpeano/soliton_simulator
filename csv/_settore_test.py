import pickle, numpy as np, sys

def load(p):
    return pickle.load(open(p, "rb"))["attrs"]

def canon(nb):
    nb = np.asarray(nb, float).reshape(-1, 3)
    th = np.arccos(np.clip(nb[:, 2], -1.0, 1.0))
    ph = np.arctan2(nb[:, 1], nb[:, 0])
    return np.stack([np.cos(th / 2.0), np.sin(th / 2.0) * np.exp(1j * ph)], axis=1)

def analizza(path, nome):
    A = load(path)
    n = A["phi"].shape[0]
    nb = np.asarray(A["_nb"])[:n]
    psi = np.asarray(A["_psi_spinor"])[:n]
    chi = np.asarray(A["perc_chi"])[:n]
    i = np.asarray(A["i"]); j = np.asarray(A["j"])
    ov = np.sum(np.conj(canon(nb)) * psi, axis=1)     # e^{i alpha}
    sgn = np.sign(np.real(ov)).astype(float)          # foglio +-1
    m = (i < n) & (j < n)
    ii = i[m]; jj = j[m]
    si = sgn[ii]; sj = sgn[jj]
    ci = chi[ii]; cj = chi[jj]
    prod = si * sj
    # classi d'arco per chiralita' (materia perc_chi=+1, antimateria -1)
    mm = (ci > 0) & (cj > 0)
    aa = (ci < 0) & (cj < 0)
    ma = ((ci > 0) & (cj < 0)) | ((ci < 0) & (cj > 0))
    tot = len(prod)
    n_mat = int((chi > 0).sum()); n_anti = int((chi < 0).sum())
    print(f"=== {nome} (N={n}) ===")
    print(f"  nodi: materia(+1)={n_mat} ({100*n_mat/n:.0f}%)  antimateria(-1)={n_anti} ({100*n_anti/n:.0f}%)")
    print(f"  archi: tot={tot}  mat-mat={mm.sum()} ({100*mm.sum()/tot:.0f}%)  anti-anti={aa.sum()} ({100*aa.sum()/tot:.0f}%)  mat-anti={ma.sum()} ({100*ma.sum()/tot:.0f}%)")
    g = float(prod.mean())
    print(f"  segno_arco_coer GLOBALE (tutti archi) = {g:+.4f}")
    for lab, msk in (("mat-mat  <s_i s_j>", mm), ("anti-anti <s_i s_j>", aa), ("mat-anti  <s_i s_j>", ma)):
        if msk.sum() > 0:
            print(f"    {lab} = {float(prod[msk].mean()):+.4f}   (n={int(msk.sum())})")
        else:
            print(f"    {lab} = (nessun arco)")
    # commitment per settore
    print(f"    |media sgn| materia={abs(sgn[chi>0].mean()):.4f}  antimateria={abs(sgn[chi<0].mean()):.4f}")
    print()

base = sys.argv[1] if len(sys.argv) > 1 else "db/deparam_pilota_sfo"
analizza(f"{base}/db_on.pkl", "ON  (--sync-fase-orologio)")
analizza(f"{base}/db_off.pkl", "OFF (baseline)")
