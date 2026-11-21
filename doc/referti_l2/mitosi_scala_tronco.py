# -*- coding: utf-8 -*-
r"""**LA SCALA DEL MATTONE NEL TEMPO CONTRO IL RITMO DEL CONTATORE, SUL TRONCO** *(la domanda di Luca `2026-11-21` `14:22`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `18.3`-`18.4`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_scala_tronco.py --base E:\soliton_simulator\controllo\mitosi_rami > doc/referti_l2/mitosi_scala_tronco.txt

**Legge, non tocca:** la serie del tronco *(l'ultima: ogni `50` tick da `k 3000`)* e gli stati ai confini dei tratti *(lo sha1 controllato)*.
**Per tratti di `2500` tick** *(i confini di `mitosi_ritmo_contatore.confini`)*: la media sul tratto di `D_w`, `D_r50`, `D_r90` *(passi)*, `raggio` *(euclideo)*, `Min_12.4`, `Min_25`; **il massimo di `rho`** *(dalle estremita', la media dei due confini)*; **il ritmo dei primi `20` archi** da `Theta` *(`mitosi_ritmo_contatore.ritmi`)* **e da `cs_prec`** *(`pi |cs_i - cs_j|`, la media dei due confini: IL CONTROLLO, entro il `10%`)*; **`Lambda` e `cs` alle estremita' dei `20` archi.**
**La lettura scritta prima** *(18.4)*: la correlazione si stampa e NON risponde; **risponde la forma:** `ritmo / max rho` circa costante -> segue il PICCO; `ritmo * w` *(o `* r90`, `* raggio`)* circa costante -> segue l'ALLARGAMENTO; **circa costante = la variazione relativa minore di quella del ritmo.** Entrambi o nessuno: **NON DECIDIBILE.**
"""
import argparse
import glob
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(_QUI, "..", "..", "csv"), _QUI):
    if p not in sys.path:
        sys.path.insert(0, p)
import mitosi_ritmo_contatore as RT          # ### usato, non riscritto: confini, ritmi, theta, sha1
import mitosi_anelli as AN                   # ### usato, non riscritto: toro

N0 = 186 * 186
SOGLIA_CONTROLLO = 0.10


def nodi_e_cs(f, archi, ii, jj):
    """### da uno stato: il massimo di `rho` *(dalle estremita')*, `pi |cs_i - cs_j|` sui `20` archi, `Lambda` e `cs` medi alle loro estremita'."""
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == RT.sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        psi_h, phi_h, cs = d["psi_h"], d["phi_h"], d["cs_prec"].copy()
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    rho = np.bincount(nodo, weights=np.sum(np.abs(psi_h) ** 2, axis=1), minlength=N0)
    lam = np.bincount(nodo, weights=np.abs(phi_h) ** 2, minlength=N0)
    e = np.concatenate([ii[archi], jj[archi]])
    return float(rho.max()), math.pi * np.abs(cs[ii[archi]] - cs[jj[archi]]), float(lam[e].mean()), float(cs[e].mean())


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    x = ap.parse_args(argv)
    d = os.path.join(x.base, "TRONCO")
    F = RT.stati(d)
    kU = max(F)
    with np.load(os.path.join(d, "serie_%05d.npz" % kU)) as s:
        S = {c: np.asarray(s[c], dtype=float) for c in ("k", "raggio", "Min_12.4", "Min_25", "D_k", "D_w", "D_r50", "D_r90")}
    U = RT.theta(F[kU])
    archi = np.argsort(-np.abs(U))[:RT.N_ARCHI]
    cc = RT.confini(F)
    T, R, mid = RT.ritmi(F, cc, archi)
    ii, jj, _, _ = AN.toro()
    C = {k: nodi_e_cs(F[k], archi, ii, jj) for k in cc}
    print("=" * 140)
    print("LA SCALA DEL MATTONE CONTRO IL RITMO DEL CONTATORE, SUL TRONCO (la domanda di Luca 2026-11-21 14:22; la carta sez. 18)")
    print("=" * 140)
    print("### il tronco: la serie fino a k %d (%d righe, da k %d); %d tratti; i primi %d archi (|Theta| maggiore a k %d)" % (kU, len(S["k"]), int(S["k"][0]), len(cc) - 1, RT.N_ARCHI, kU))
    rows = []
    for j in range(len(cc) - 1):
        a, b = cc[j], cc[j + 1]
        mk = (S["k"] >= a) & (S["k"] <= b)
        md = (S["D_k"] >= a) & (S["D_k"] <= b)
        rT = float(R[j].mean())
        rC = float(np.mean([C[a][1].mean(), C[b][1].mean()]))
        rows.append(dict(t="%d-%d" % (a, b), w=S["D_w"][md].mean(), r50=S["D_r50"][md].mean(), r90=S["D_r90"][md].mean(), rg=S["raggio"][mk].mean(),
                         m12=S["Min_12.4"][mk].mean(), m25=S["Min_25"][mk].mean(), pk=0.5 * (C[a][0] + C[b][0]), rT=rT, rC=rC,
                         lam=0.5 * (C[a][2] + C[b][2]), cs=0.5 * (C[a][3] + C[b][3])))
    print("### LE MEDIE PER TRATTO (il ritmo in 1e-4 per tick; w, r50, r90 in passi; il raggio euclideo; Lambda e cs alle estremita' dei 20 archi):")
    print("    il tratto       w       r50     r90    raggio   M<12.4      M<25       max rho     ritmo(Theta)  ritmo(cs)   cs/Theta   Lambda(20)   cs(20)")
    ok = True
    for r in rows:
        q = r["rC"] / r["rT"]
        ok &= abs(q - 1.0) <= SOGLIA_CONTROLLO
        print("    %-12s %7.3f %7.2f %7.2f %8.4f  %9.4f  %9.4f  %12.6e   %9.4f   %9.4f   %7.4f   %11.6e  %8.6f" % (
            r["t"], r["w"], r["r50"], r["r90"], r["rg"], r["m12"], r["m25"], r["pk"], r["rT"] * 1e4, r["rC"] * 1e4, q, r["lam"], r["cs"]))
    print("### IL CONTROLLO (il ritmo da cs_prec entro il %d%% di quello da Theta, a ogni tratto): %s" % (int(SOGLIA_CONTROLLO * 100), "PASSA" if ok else "NON PASSA: FERMO (il contatore non legge cs_prec come credo)"))
    v = lambda key: np.array([r[key] for r in rows])
    rit = v("rT")
    var = lambda y: float(y.max() / y.min() - 1.0)
    print("### LE GRANDEZZE SUL PRIMO TRATTO (l'ultimo tratto diviso il primo):")
    for key, nome in (("rT", "il ritmo"), ("w", "w"), ("r50", "r50"), ("r90", "r90"), ("rg", "il raggio"), ("m12", "M<12.4"), ("m25", "M<25"), ("pk", "max rho"), ("lam", "Lambda(20)"), ("cs", "cs(20)")):
        y = v(key)
        print("    %-11s %.4f   (la correlazione col ritmo %+.4f)" % (nome, y[-1] / y[0], float(np.corrcoef(y, rit)[0, 1])))
    print("### LA FORMA (la variazione relativa sui tratti, max/min - 1; il ritmo stesso: %.4f):" % var(rit))
    inv = {"ritmo / max rho (il PICCO)": rit / v("pk"), "ritmo * w (l'ALLARGAMENTO, in passi)": rit * v("w"), "ritmo * r90 (l'ALLARGAMENTO, in passi)": rit * v("r90"),
           "ritmo * raggio (l'ALLARGAMENTO, euclideo)": rit * v("rg")}
    sotto = {}
    for nome, y in inv.items():
        sotto[nome] = var(y) < var(rit)
        print("    %-44s %.4f  -> %s" % (nome, var(y), "circa costante" if sotto[nome] else "NON costante"))
    pic = sotto["ritmo / max rho (il PICCO)"]
    alla = any(sotto[n] for n in inv if "ALLARGAMENTO" in n)
    print("### LA LETTURA (scritta prima): %s" % ("il calo segue il PICCO" if pic and not alla else "il calo segue l'ALLARGAMENTO" if alla and not pic else "NON DECIDIBILE da queste serie (%s)" % ("entrambi circa costanti" if pic else "nessuno circa costante")))
    print("=" * 140)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
