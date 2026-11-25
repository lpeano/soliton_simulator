# -*- coding: utf-8 -*-
r"""**[M0137-6] LA RISERVA: LA COPPIA A 41.57 LUNGO y CON kappa IN RAMPA LINEARE SU 1500 TICK** *(il criterio C non e' passato in tre giri: il mandato prevede la riserva, dichiarata nella carta sez. `3-sedecies`; `due_corpi_fondo_v4.py` e' usato e non si riscrive)*. **La v4, con tre differenze:** la partenza e' l'oggetto del giro 4 SENZA chi *(`chi = pi = 0`)*; **`kappa` e `c0` crescono come `min(t/1500, 1)`** *(`c0 = kappa m0`, la sorgente scala con `kappa`)*; le uscite in `M0137/coppia_rampa/`. **LA V4:** *(DECISIONE DI LUCA, 2026-11-25 01:37, dalla posta; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-sedecies`; `due_corpi_fondo.py`, `_v2`, `_v3` sono usati e non si riscrivono)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v5.py noto > doc/referti_l2/due_corpi_fondo_v5_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v5.py corsa --quale d1      (d1 due chi on in rampa, d2 due chi off, d3 uno chi on in rampa)

**Lo stato di partenza** *(`--da`)*: la nuova partenza del giro del punto fisso con chi che passa C *(`psi` mediato e riproiettato, i campi, `chi`, `pi` da `k 6000`)*. **La coppia** *(Luca, A e B)*: il secondo corpo e' lo stato traslato di **`(+24, +48)`** *(`41.57` lungo `y`, `0` lungo `x`: `A2 = (-1/2, sqrt3/2)`)*; **materia per SOMMA, vuoto per PRODOTTO** *(il fondo `a phi_v` fittato a `d > 45`, come la v1)*, **chi per SOMMA** `chi_A + chi_B - chi_fondo` *(`chi_fondo` = la media di `chi_A` a `d > 45`)*, **e `pi` allo stesso modo** *(dichiarato: Luca nomina chi)*. **`theta_a` riparte da zero** *(un accumulatore che il tick non rilegge)*. **I campi:** `porto.campi` in tutte e tre *(come [M2330])*. **I parametri:** `gravita_due_corpi.parametri` sulla configurazione *(`c0 = kappa m0`)*, con `U` riscritto *(la v3)*; off: `kappa = 0`. **Il ciclo:** quello della v2 *(il nucleo preso prima della scena)*. Gli stati ogni `250`, la serie ogni `10`, `omega` per tick per corpo, in `M0137/coppia/<d>/`.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v3 as D3  # noqa: E402

D = D3.D
F1, PF, CT, CV2, GD = D.F1, D.PF, D.CT, D.CV2, D.GD
TRASLA = (24, 48)
BASE = os.path.join(PF.CTRL, "M0137", "coppia_rampa")
K_RAMPA = 1500          # ### Luca, la riserva: la rampa lineare di kappa in 1500 tick
DA = D.G4.PARTENZA_G4   # ### l'oggetto del giro 4, senza chi
R_FONDO = D.R_FONDO
K_FINE, OGNI_STATO, OGNI_SERIE = 6000, 250, 10
QUALI = D.QUALI


def costruisci(Z, quanti, da):
    """### lo stato del tick `0` e `X`: `(C, info, X)`."""
    from solitone import porto as PO
    from solitone import toro as TO
    MT = GD.TC.moduli()[0]
    F1.OGGETTO = da
    C, info, dxy, _forma, _X = F1.FS.carica(Z, "K", 3000)
    st = Z["st"]
    mot = Z["mot"]
    nodo, n, L = np.asarray(mot.inc.nodo), Z["n"], Z["L"]
    chiA, piA = np.zeros(n), np.zeros(n)     # ### la riserva: chi parte da zero
    info = dict(info)
    d = np.hypot(dxy[:, 0], dxy[:, 1])
    if quanti == 2:
        psiA, phiA = st["psi_h"].copy(), st["phi_h"].copy()
        lon = (d > R_FONDO)[nodo]
        pv = np.asarray(Z["phi_v"])
        a = complex(np.sum(np.conj(pv[lon]) * phiA[lon]) / np.sum(np.abs(pv[lon]) ** 2))
        fondo = a * pv
        res = np.abs(phiA[lon] - fondo[lon]) / np.abs(fondo[lon])
        src, dst = D.trasla_idx(Z, TRASLA)
        psiB = np.zeros_like(psiA)
        phiB = np.empty_like(phiA)
        psiB[dst] = psiA[src]
        phiB[dst] = phiA[src]
        st["psi_h"][...] = psiA + psiB
        st["phi_h"][...] = phiA * phiB / fondo
        v = np.arange(n)
        Tv = ((v // L + TRASLA[0]) % L) * L + (v % L + TRASLA[1]) % L
        cf, pf = float(chiA[d > R_FONDO].mean()), float(piA[d > R_FONDO].mean())
        chiB, piB = np.empty_like(chiA), np.empty_like(piA)
        chiB[Tv], piB[Tv] = chiA[v], piA[v]
        chi, pi = chiA + chiB - cf, piA + piB - pf
        info.update(trasla=list(TRASLA), a_fondo=[a.real, a.imag], residuo_fondo=[float(res.mean()), float(res.max())],
                    chi_fondo=cf, pi_fondo=pf, masse=[float(np.sum(np.abs(psiA) ** 2)), float(np.sum(np.abs(psiB) ** 2))])
    else:
        chi, pi = chiA, piA
    C = PO.campi(Z, MT.rho_c_assoluto(), MT.PB.E_DECISO)
    rho = np.bincount(nodo, weights=np.sum(np.abs(st["psi_h"]) ** 2, axis=1), minlength=n)
    b = TO.centro(rho, Z["m1"], Z["m2"], L)[:2]
    info["centro_coppia"] = [float(b[0]), float(b[1])]
    X = {"chi": np.array(chi, float), "pi": np.array(pi, float), "theta_a": np.zeros(mot.inc.m)}
    return C, info, X


def ciclo_rampa(Z, C, P_t, Lp, X, quanti, dopo):
    """### `due_corpi_fondo_v2.ciclo` riga per riga, coi parametri del tick `P_t(kk)` *(la rampa)*."""
    import ripresa_F0_v2 as RF
    MV, P0 = D3.D2.NUC
    _G20, _ia, _e0, MT = F1.CL.parametri()
    with RF.col_nucleo(MV, P0), MV.forma_esplicita(F1.FORMA_OGG):
        assert MV.ATTIVA == F1.FORMA_OGG and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            CV2.tick_chi_v2(Z["z"], C.campo, P_t(kk), Lp, X)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


def noto(da):
    D.avvia()
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0137-4] I CASI NOTI DELLA COPPIA (la carta sez. 3-sedecies): lo stato di partenza %s" % da)
    print("=" * 130)
    PF.controlla(da)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    with GD.TC.scena() as Z:
        L, n = Z["L"], Z["n"]
        v = np.arange(n)
        Tv = ((v // L + TRASLA[0]) % L) * L + (v % L + TRASLA[1]) % L
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        A1, A2 = TO.vettori()
        dm = np.stack([((m1[Tv] - m1 + 0.5 * L) % L) - 0.5 * L, ((m2[Tv] - m2 + 0.5 * L) % L) - 0.5 * L], axis=1)
        sp = dm[:, :1] * A1 + dm[:, 1:] * A2
        dx, dy = float(np.max(np.abs(sp[:, 0]))), float(np.max(np.abs(sp[:, 1] - 48.0 * math.sqrt(3.0) / 2.0)))
        esito("(G) lo spostamento di ogni nodo: |dx| < 1e-9 e |dy - 48 sqrt3/2| < 1e-9", dx < 1e-9 and dy < 1e-9, "max |dx| %.1e, max |dy - 41.5692| %.1e" % (dx, dy))
        imp = {}
        for q in ("d1", "d2"):
            C, info, X = costruisci(Z, 2, da)
            P, Pon, m0 = D.parametri(Z, C, QUALI[q][1])
            imp[q] = GD.impronta(Z, C, X)
            if q == "d1":
                ms = info["masse"]
                esito("(T) le masse dei due corpi uguali entro 1e-9 relativo", abs(ms[0] / ms[1] - 1.0) < 1e-9, "%r" % ms)
                print("  la coppia: a del fondo %+.6f%+.6fi; il residuo del fondo (d > %.0f) medio %.3e, massimo %.3e; chi_fondo %+.4f, pi_fondo %+.3e; max|chi| %.3f; il centro %s; P on %r; m0 %.6e" % (
                    info["a_fondo"][0], info["a_fondo"][1], R_FONDO, info["residuo_fondo"][0], info["residuo_fondo"][1], info["chi_fondo"], info["pi_fondo"], float(np.max(np.abs(X["chi"]))), info["centro_coppia"], Pon, m0))
            Z["metti"]()
        esito("(K2) d2' a k 0 = d1' a k 0 AL BIT (l'impronta: le chiavi, A, E, chi, pi, Theta)", imp["d1"] == imp["d2"], "%s %s" % (imp["d1"][:12], imp["d2"][:12]))
        fr = [min(kk / float(K_RAMPA), 1.0) for kk in (0, 750, 1500, 6000)]
        esito("(R) la rampa: il fattore a k 0, 750, 1500, 6000 = 0, 0.5, 1, 1 esatti", fr == [0.0, 0.5, 1.0, 1.0], "%s" % fr)
    fall = [k for k, v_ in OK.items() if not v_]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa(quale, da):
    D.avvia()
    import _presidio
    _presidio.avvia(__file__)
    PF.controlla(da)
    quanti, chi_on = QUALI[quale]
    d_out = os.path.join(BASE, quale)
    assert not os.path.exists(os.path.join(d_out, "stato_000000.npz")), "%s c'e' gia': non si riscrive" % d_out
    os.makedirs(d_out, exist_ok=True)
    with GD.TC.scena() as Z:
        mot = Z["mot"]
        n = mot.inc.n
        nodo = np.asarray(mot.inc.nodo)
        Lp = CT.Laplaciano(mot)
        C, info, X = costruisci(Z, quanti, da)
        P, Pon, m0 = D.parametri(Z, C, chi_on)
        meta = dict(info, corsa=quale, da=da, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f, "kappa_on": Pon.kappa})
        dxy0, M0 = D.corpi(Z, info["centro_coppia"], quanti)
        maschere = [mm[nodo] for mm in M0]
        print("### [M0137-4] %s: %d oggett%s, chi %s; da %s; i parametri %r; m0 %+.12e; l'impronta %s" % (quale, quanti, "o" if quanti == 1 else "i", "on" if chi_on else "off", da, P, m0, GD.impronta(Z, C, X)))
        sys.stdout.flush()
        serie, om = [], [[] for _ in M0]
        t1 = time.time()

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            riga = [kk]
            for mm in M0:
                w = rho * mm
                c = (dxy0 * w[:, None]).sum(axis=0) / w.sum()
                riga += [float(c[0]), float(c[1]), float(w.sum())]
            riga.append(float(np.max(np.abs(X["chi"]))))
            serie.append(riga)

        def dopo(kk, prima):
            for j, ms in enumerate(maschere):
                om[j].append(float(-np.angle(np.vdot(prima[ms], Z["st"]["psi_h"][ms]))))
            if kk % OGNI_SERIE == 0:
                misura(kk)
            if kk % OGNI_STATO == 0:
                salva(kk)
                print("    k %d: %s; max|chi| %.4e (%.0f s)" % (kk, " ".join("y%d %+.4f" % (j + 1, serie[-1][2 + 3 * j]) for j in range(quanti)), serie[-1][-1], time.time() - t1))
                sys.stdout.flush()
        salva(0)
        misura(0)
        def P_t(kk):
            f = min(kk / float(K_RAMPA), 1.0)
            return CV2.Parametri2(P.kappa * f, P.c0 * f, P.s, P.e0, P.f, P.c2, P.m2)
        ciclo_rampa(Z, C, P_t, Lp, X, K_FINE, dopo)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"meta": meta, "serie": serie, "omega": om}))
        PF.firma(f)
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_FINE, time.time() - t1))
    ok = os.path.exists(os.path.join(d_out, "stato_000250.npz.sha1"))
    print("### stato_000250.npz %s" % ("ESISTE" if ok else "### NON ESISTE"))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa"))
    ap.add_argument("--quale", choices=tuple(QUALI))
    ap.add_argument("--da", default=DA)
    a = ap.parse_args(argv)
    return noto(a.da) if a.cosa == "noto" else corsa(a.quale, a.da)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
