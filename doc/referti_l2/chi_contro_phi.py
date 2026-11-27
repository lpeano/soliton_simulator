# -*- coding: utf-8 -*-
r"""**[M2048] IL LAPSE LO PORTA GIA' phi? chi CONTRO rho_phi E CONTRO L'OROLOGIO LOCALE DEL VUOTO** *(DECISIONE DI LUCA, 2026-11-26 20:48, dalla posta; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-duodevicies`; una lettura, un tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_contro_phi.py noto > doc/referti_l2/chi_contro_phi_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/chi_contro_phi.py lettura > doc/referti_l2/chi_contro_phi.txt      (e chi_contro_phi.png)

**Lo stato:** `M0414/puntofisso_accoppiato/giro_3/partenza_giro_4.npz` *(chi, `pi = 0`, i campi)*. **Un tick** di `tick_chi_v2` *(kappa acceso, i parametri del giro 1 di [M0137], la forma `L-1`: la macchina di `fondo_puntofisso_chi_v2`)*. **Per nodo:** `rho_phi = somma |phi_h|^2`; **`omega_phi` locale** `= -arg somma conj(phi_h(k)) phi_h(k+1)` sulle mezze-spighe del nodo *(il prodotto in reali)*; chi; `N = exp(-kappa chi)`. **Le tre coppie** `(chi, rho_phi)`, `(chi, omega_phi)`, `(chi, N)`: Pearson e Spearman su tutti i nodi e per anello dal baricentro di `rho_psi`; la mediana di chi per decile dell'osservabile. **S3:** «phi lo porta» se `|Spearman| > 0.9` su tutti i nodi E la mediana per decile monotona.
"""
import argparse
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_puntofisso_chi_v2 as FPC2  # noqa: E402

FPC = FPC2.FPC
D, F1, PF, CT = FPC.D, FPC.F1, FPC.PF, FPC.CT
STATO = os.path.join(FPC2.DIR, "giro_3", "partenza_giro_4.npz")
ANELLI = ((0.0, 8.0), (8.0, 16.0), (16.0, 32.0), (32.0, 45.0), (45.0, 90.0))


def z_nodo(a, b, nodo, n):
    """### `somma conj(a) b` per nodo, col prodotto in reali."""
    ar, ai, br, bi = a.real, a.imag, b.real, b.imag
    return np.bincount(nodo, weights=ar * br + ai * bi, minlength=n) + 1j * np.bincount(nodo, weights=ar * bi - ai * br, minlength=n)


def un_tick(f, ticks=1):
    """### `(phi_prima, phi_dopo, X, Z-dati)`: `ticks` tick di `tick_chi_v2` dallo stato `f`, chi e `pi` dal file."""
    P = FPC.parametri_giro1()
    with D.GD.TC.scena() as Z:
        mot = Z["mot"]
        Lp = CT.Laplaciano(mot)
        F1.OGGETTO = f
        C, info = D.costruisci(Z, 1, campi_stato=True)
        with np.load(f) as z:
            X = {"chi": z["chi"].copy(), "pi": z["pi"].copy(), "theta_a": z["theta_a"].copy()}
        phi0, psi0, chi0 = Z["st"]["phi_h"].copy(), Z["st"]["psi_h"].copy(), X["chi"].copy()
        D.ciclo(Z, C, P, Lp, X, ticks, lambda kk, prima: None)
        out = dict(phi0=phi0, phi1=Z["st"]["phi_h"].copy(), psi0=psi0, psi1=Z["st"]["psi_h"].copy(), chi0=chi0,
                   nodo=np.asarray(mot.inc.nodo), n=Z["n"], L=Z["L"], m1=np.asarray(Z["m1"]), m2=np.asarray(Z["m2"]), P=P)
        Z["metti"]()
    return out


def spearman(a, b):
    from scipy.stats import spearmanr
    return float(spearmanr(a, b).statistic)


def decili(x, chi):
    q = np.quantile(x, np.linspace(0, 1, 11))
    med = []
    for i in range(10):
        m = (x >= q[i]) & ((x < q[i + 1]) if i < 9 else (x <= q[i + 1]))
        med.append(float(np.median(chi[m])) if m.any() else float("nan"))
    dm = np.diff(med)
    return med, bool(np.all(dm > 0) or np.all(dm < 0))


def noto():
    D.avvia()
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_chi_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2048] I CASI NOTI (la carta sez. 3-duodevicies)")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    # ### (K1) il vuoto fresco: nessun oggetto, chi 0, un tick
    P = FPC.parametri_giro1()
    with D.GD.TC.scena() as Z:
        from solitone import porto as PO
        mot = Z["mot"]
        n = Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        Lp = CT.Laplaciano(mot)
        F1.OGGETTO = STATO
        C, info = D.costruisci(Z, 1, campi_stato=True)
        Z["st"]["psi_h"][...] = 0.0
        Z["st"]["phi_h"][...] = np.asarray(Z["phi_v"])
        MT = D.GD.TC.moduli()[0]
        C = PO.campi(Z, MT.rho_c_assoluto(), MT.PB.E_DECISO)
        X = CT.nuovo_X(n, mot.inc.m)
        p0 = Z["st"]["phi_h"].copy()
        D.ciclo(Z, C, P, Lp, X, 1, lambda kk, prima: None)
        p1 = Z["st"]["phi_h"].copy()
        Z["metti"]()
    om = -np.angle(z_nodo(p0, p1, nodo, n))
    og = float(-np.angle(np.vdot(p0, p1)))
    rho = np.bincount(nodo, weights=np.abs(p0) ** 2, minlength=n)
    esito("(K1) il vuoto fresco, un tick: omega_phi locale = omega_phi globale entro 1e-9 su tutti i nodi", float(np.max(np.abs(om - og))) < 1e-9, "omega globale %+.12f, max |d| %.2e" % (og, float(np.max(np.abs(om - og)))))
    esito("(K1) rho_phi del vuoto fresco uniforme entro 1e-9", float(rho.max() - rho.min()) < 1e-9, "da %.12f a %.12f" % (rho.min(), rho.max()))
    # ### (K2)
    with np.load(STATO) as z:
        chi = z["chi"].copy()
    s = spearman(chi, np.exp(-P.kappa * chi))
    esito("(K2) Spearman(chi, N = exp(-kappa chi)) = -1 esatto", s == -1.0, "%r" % s)
    # ### (K3) l'equivalente dichiarato: 250 tick dalla partenza del giro 3 = lo stato a k 250 del giro 3 AL BIT
    import gravita_due_corpi_misure as GM
    out = un_tick(os.path.join(FPC2.DIR, "giro_2", "partenza_giro_3.npz"), 250)
    Xg, _m = GM.leggi(os.path.join(FPC2.DIR, "giro_3", "stato_000250.npz"))
    esito("(K3, l'equivalente) 250 tick dalla partenza del giro 3 = giro_3/stato_000250 AL BIT (psi_h, phi_h)", np.array_equal(out["psi1"], Xg["psi_h"]) and np.array_equal(out["phi1"], Xg["phi_h"]),
          "max |d psi| %.2e" % float(np.max(np.abs(out["psi1"] - Xg["psi_h"]))))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def lettura():
    D.avvia()
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_chi_v2.py"))
    _presidio.avvia(__file__)
    PF.controlla(STATO)
    print("=" * 130)
    print("[M2048] chi CONTRO phi SULLO STATO DEL GIRO 3 (la carta sez. 3-duodevicies): %s" % STATO)
    print("=" * 130)
    o = un_tick(STATO, 1)
    nodo, n, L = o["nodo"], o["n"], o["L"]
    rho = np.bincount(nodo, weights=np.abs(o["phi0"]) ** 2, minlength=n)
    om = -np.angle(z_nodo(o["phi0"], o["phi1"], nodo, n))
    chi = o["chi0"]
    N = np.exp(-o["P"].kappa * chi)
    rpsi = np.bincount(nodo, weights=np.sum(np.abs(o["psi0"]) ** 2, axis=1), minlength=n)
    b = TO.centro(rpsi, o["m1"], o["m2"], L)[:2]
    d = np.hypot(*np.asarray(TO.scarti(o["m1"], o["m2"], b[0], b[1], L))[:, :2].T)
    print("  %d nodi; il centro %s; kappa %.6e; omega_phi globale %+.9f" % (n, ["%.3f" % x for x in b], o["P"].kappa, float(-np.angle(np.vdot(o["phi0"], o["phi1"])))))
    cand = (("rho_phi", rho), ("omega_phi locale", om), ("N (il controllo)", N))
    tot = {}
    for nome, x in cand:
        pe = float(np.corrcoef(chi, x)[0, 1])
        sp = spearman(chi, x)
        med, mono = decili(x, chi)
        tot[nome] = (sp, mono)
        print("-" * 130)
        print("  (chi, %s), tutti i %d nodi: Pearson %+.4f, Spearman %+.4f; la mediana di chi per decile: %s; monotona: %s" % (nome, n, pe, sp, " ".join("%+.2f" % v for v in med), "SI'" if mono else "NO"))
        for lo, hi in ANELLI:
            m = (d >= lo) & (d < hi)
            print("    [%2.0f, %2.0f) (%5d nodi): Pearson %+.4f, Spearman %+.4f" % (lo, hi, int(m.sum()), float(np.corrcoef(chi[m], x[m])[0, 1]), spearman(chi[m], x[m])))
    print("-" * 130)
    pas = [k for k in ("rho_phi", "omega_phi locale") if abs(tot[k][0]) > 0.9 and tot[k][1]]
    if pas:
        vince = max(pas, key=lambda k: abs(tot[k][0]))
        print("### S3: phi LO PORTA, col candidato %s (|Spearman| %.4f, la mediana monotona)%s" % (vince, abs(tot[vince][0]), "; passano entrambi" if len(pas) == 2 else ""))
    else:
        print("### S3: phi NON LO PORTA (|Spearman| rho_phi %.4f, omega_phi %.4f; monotone %s, %s)" % (abs(tot["rho_phi"][0]), abs(tot["omega_phi locale"][0]), tot["rho_phi"][1], tot["omega_phi locale"][1]))
    sr = tot["rho_phi"][0]
    print("### S4, il segno: Spearman(chi, rho_phi) %+.4f: %s" % (sr, "chi cresce dove rho_phi cresce" if sr > 0 else "chi cresce dove rho_phi cala: N = exp(-kappa chi) cala dove il vuoto manca (il tempo e' lento dove il vuoto manca)"))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.5), dpi=80)
    for a, (nome, x) in zip(ax, cand):
        a.scatter(x, chi, s=1, c=d, cmap="viridis", alpha=0.5)
        a.set_xlabel(nome)
        a.set_ylabel("chi")
        a.set_title("Spearman %+.3f" % tot[nome][0], fontsize=10)
    fig.tight_layout()
    fo = os.path.join(_QUI, "chi_contro_phi.png")
    fig.savefig(fo)
    print("### l'immagine: %s (il colore e' la distanza dal centro)" % fo)
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "lettura"))
    a = ap.parse_args(argv)
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
