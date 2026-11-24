# -*- coding: utf-8 -*-
r"""**[M2330] IL MODELLO INTERO: DUE OGGETTI AL FONDO A K CON CHI VERO** *(DECISIONE DI LUCA, 2026-11-24 23:30; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-quattuordecies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo.py noto > doc/referti_l2/due_corpi_fondo_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo.py corsa --quale d1      (d1 due chi on, d2 due chi off, d3 uno chi on; dalla coda)

**L'oggetto:** il punto fisso del giro 4 *(`puntofisso_v3b/giro_3/stato_006000.npz`)*. **Il secondo** e' lo stesso stato traslato di `(dm1, dm2) = (-24, +48)` *(multipli di `3`, il disegno di fase di K; `+41.57` lungo `y`, `0` lungo `x`)* con `Z["righe"]`, come `mattone.incolla`. **La materia per SOMMA; il vuoto per PRODOTTO** *(come `gravita_due_corpi.prepara_coppia`)*: `phi = phi_A phi_B / phi_fondo`, **`phi_fondo = a phi_v`** con `a` il fit complesso di `phi_A` su `phi_v` sui nodi a distanza `> 45` dall'oggetto *(non serve il tick assoluto)*. **I campi** `porto.campi` *(`A = 0`, `E` da Gauss)*, in tutte e tre le corse. **`chi`:** `chi_tick_v2`, i parametri di `gravita_due_corpi.parametri` *(`kappa`, `f`, `c2`, `m2` uguali a quelli di `CHI/due_corpi/F-on`: si verifica; `c0 = kappa m0` della configurazione)*; **off:** `kappa = 0`, lo stesso `c0`. **Il tick:** `chi_tick_v2.tick_chi_v2` **dentro la forma `L-1` del nucleo** *(come `fondo_1c.ciclo`: l'oggetto al fondo esiste in quella forma)*; `C.residuo` ogni `OGNI_GAUSS`. **Gli stati ogni `250`**; **la serie ogni `10` tick:** per corpo il baricentro e la massa *(i corpi separati dal segno di `dy` dal centro della coppia)*, e `omega` per tick per corpo *(`-arg <psi_prima|psi_dopo>` sulle mezze-spighe della meta' del corpo, la maschera fissata a `k 0`)*.
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
import fondo_1c as F1  # noqa: E402
import fondo_puntofisso_v3b4 as G4  # noqa: E402
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402

PF = G4.PF
OGGETTO = G4.PARTENZA_G4
BASE = os.path.join(PF.CTRL, "M2330")
TRASLA = (-24, 48)
K_FINE, OGNI_STATO, OGNI_SERIE = 6000, 250, 10
R_FONDO = 45.0
F_ON = os.path.join(PF.CTRL, "CHI", "due_corpi", "F-on", "stato_000000.npz")
QUALI = {"d1": (2, True), "d2": (2, False), "d3": (1, True)}


def avvia():
    import _presidio
    F1.avvia()
    for m in ("fondo_puntofisso_v3b4.py", "gravita_due_corpi.py", "chi_tick_v2.py", "triangolo_chi_v4.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    F1.OGGETTO = OGGETTO


def trasla_idx(Z, dm):
    """### `(src, dst)` delle mezze-spighe: il nodo `v` va in `T(v) = ((m1 + dm1) % L) L + (m2 + dm2) % L`, con `Z["righe"]`."""
    L, n = Z["L"], Z["n"]
    v = np.arange(n)
    Tv = ((v // L + dm[0]) % L) * L + (v % L + dm[1]) % L
    righe = np.asarray(Z["righe"])
    nodo = np.asarray(Z["mot"].inc.nodo)
    assert np.all(nodo[righe[Tv]] == Tv[:, None]), "le righe del nodo traslato non sono del nodo traslato"
    return righe[v].ravel(), righe[Tv].ravel()


def costruisci(Z, quanti, campi_stato=False):
    """### lo stato del tick `0`: uno o due oggetti; `(C, info)`."""
    from solitone import porto as PO
    from solitone import toro as TO
    MT = GD.TC.moduli()[0]
    C, info, dxy, _forma, _X = F1.FS.carica(Z, "K", 3000)
    st = Z["st"]
    nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
    info = dict(info)
    if quanti == 2:
        psiA, phiA = st["psi_h"].copy(), st["phi_h"].copy()
        d = np.hypot(dxy[:, 0], dxy[:, 1])
        lon = (d > R_FONDO)[nodo]
        pv = np.asarray(Z["phi_v"])
        a = complex(np.sum(np.conj(pv[lon]) * phiA[lon]) / np.sum(np.abs(pv[lon]) ** 2))
        fondo = a * pv
        res = np.abs(phiA[lon] - fondo[lon]) / np.abs(fondo[lon])
        src, dst = trasla_idx(Z, TRASLA)
        psiB = np.zeros_like(psiA)
        phiB = np.empty_like(phiA)
        psiB[dst] = psiA[src]
        phiB[dst] = phiA[src]
        st["psi_h"][...] = psiA + psiB
        st["phi_h"][...] = phiA * phiB / fondo
        vicino = (d < 20.0)[nodo]
        dA = float(np.max(np.abs(st["phi_h"][vicino] / phiA[vicino] - 1.0)))
        info.update(trasla=list(TRASLA), a_fondo=[a.real, a.imag], residuo_fondo=[float(res.mean()), float(res.max())], phi_vicino_A=dA,
                    masse=[float(np.sum(np.abs(psiA) ** 2)), float(np.sum(np.abs(psiB) ** 2))])
    if not campi_stato:
        C = PO.campi(Z, MT.rho_c_assoluto(), MT.PB.E_DECISO)
    rho = np.bincount(nodo, weights=np.sum(np.abs(st["psi_h"]) ** 2, axis=1), minlength=n)
    b = TO.centro(rho, Z["m1"], Z["m2"], L)[:2]
    info["centro_coppia"] = [float(b[0]), float(b[1])]
    return C, info


def corpi(Z, b, quanti):
    """### le maschere per nodo dei corpi: dal centro `b` della coppia, il segno di `dy`."""
    from solitone import toro as TO
    dxy = TO.scarti(Z["m1"], Z["m2"], b[0], b[1], Z["L"])[:, :2]
    if quanti == 1:
        return dxy, [np.ones(Z["n"], bool)]
    return dxy, [dxy[:, 1] < 0.0, dxy[:, 1] >= 0.0]


def parametri(Z, C, chi_on):
    P, Pon, m0 = GD.parametri(Z, C, chi_on)
    with np.load(F_ON) as z:
        pf = json.loads(str(z["meta"]))["parametri"]
    for q in ("kappa_on", "f", "c2", "m2", "s", "e0"):
        v = Pon.kappa if q == "kappa_on" else getattr(Pon, q)
        assert v == pf[q], "il parametro %s (%r) NON e' quello di F-on (%r)" % (q, v, pf[q])
    return P, Pon, m0


def ciclo(Z, C, P, Lp, X, quanti, dopo):
    import ripresa_F0_v2 as RF
    MV, P0 = F1.TT.nucleo()
    _G20, _ia, _e0, MT = F1.CL.parametri()
    with RF.col_nucleo(MV, P0), MV.forma_esplicita(F1.FORMA_OGG):
        assert MV.ATTIVA == F1.FORMA_OGG and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


def noto():
    avvia()
    print("=" * 130)
    print("[M2330] I CASI NOTI (la carta sez. 3-quattuordecies)")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    import gravita_due_corpi_misure as GM
    with GD.TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        # ### (K1) il tick nella forma L-1 con kappa 0 e i campi dello stato = la tenuta del giro 4, 100 tick
        C, info = costruisci(Z, 1, campi_stato=True)
        P, Pon, m0 = parametri(Z, C, False)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        ciclo(Z, C, P, Lp, X, 100, lambda kk, prima: None)
        Xg, _m = GM.leggi(os.path.join(PF.DIR, "giro_4", "stato_000100.npz"))
        dv = [x for x in Z["chiavi"] if not np.array_equal(Z["st"][x], Xg[x])] + [q for q, a_, b_ in (("A", C.campo.A, Xg["campo_A"]), ("E", C.campo.E, Xg["campo_E"])) if not np.array_equal(a_, b_)]
        esito("(K1) kappa 0, i campi dello stato, 100 tick nella forma L-1 = la tenuta del giro 4 a k 100 AL BIT (le chiavi, A, E)", not dv, "diverse %s" % dv)
        Z["metti"]()
        # ### (K1-on) lo stesso con chi acceso: l'esito si dichiara
        C, info = costruisci(Z, 1, campi_stato=True)
        P, Pon, m0 = parametri(Z, C, True)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        ciclo(Z, C, P, Lp, X, 100, lambda kk, prima: None)
        dpsi = float(np.max(np.abs(Z["st"]["psi_h"] - Xg["psi_h"])))
        print("  (K1-on, si dichiara) chi acceso, 100 tick: max |psi - psi(tenuta)| %.3e (max |psi| %.3e); m0 %.6e, c0 %.6e" % (dpsi, float(np.max(np.abs(Xg["psi_h"]))), m0, P.c0))
        Z["metti"]()
        # ### (K2) d2 a k 0 = d1 a k 0 AL BIT; la traslazione
        imp = {}
        for q in ("d1", "d2"):
            C, info = costruisci(Z, 2)
            P, Pon, m0 = parametri(Z, C, QUALI[q][1])
            X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
            imp[q] = GD.impronta(Z, C, X)
            if q == "d1":
                print("  la coppia: la traslazione %s; a del fondo %+.6f%+.6fi; il residuo del fondo (d > %.0f) medio %.3e, massimo %.3e; phi vicino ad A (d < 20) cambiato al massimo di %.3e; le masse %s; il centro %s; P on %r" % (
                    info["trasla"], info["a_fondo"][0], info["a_fondo"][1], R_FONDO, info["residuo_fondo"][0], info["residuo_fondo"][1], info["phi_vicino_A"], info["masse"], info["centro_coppia"], Pon))
                src, dst = trasla_idx(Z, TRASLA)
                rho = np.bincount(np.asarray(mot.inc.nodo), weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
                esito("(T) le masse dei due oggetti uguali AL BIT", info["masse"][0] == info["masse"][1], "%r" % info["masse"])
                L = Z["L"]
                v = np.arange(n)
                Tv = ((v // L + TRASLA[0]) % L) * L + (v % L + TRASLA[1]) % L
                Tb = ((v // L - TRASLA[0]) % L) * L + (v % L - TRASLA[1]) % L
                esito("(T) la traslazione e la sua inversa = l'identita' AL BIT", np.array_equal(Tb[Tv], v))
                esito("(T) DEVE FALLIRE: rho della coppia simmetrico per T (rho(T v) = rho(v)) -- non lo e', i corpi sono due", not np.array_equal(rho[Tv], rho), "")
            Z["metti"]()
        esito("(K2) d2 a k 0 = d1 a k 0 AL BIT (l'impronta: le chiavi, A, E, chi, pi, Theta)", imp["d1"] == imp["d2"], "%s %s" % (imp["d1"][:12], imp["d2"][:12]))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa(quale):
    avvia()
    assert open(OGGETTO + ".sha1", encoding="utf-8").read().split()[0] == PF.sha1(OGGETTO)
    quanti, chi_on = QUALI[quale]
    d_out = os.path.join(BASE, quale)
    assert not os.path.exists(os.path.join(d_out, "stato_000000.npz")), "%s c'e' gia': non si riscrive" % d_out
    os.makedirs(d_out, exist_ok=True)
    with GD.TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        nodo = np.asarray(mot.inc.nodo)
        Lp = CT.Laplaciano(mot)
        C, info = costruisci(Z, quanti)
        P, Pon, m0 = parametri(Z, C, chi_on)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        meta = dict(info, corsa=quale, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f, "kappa_on": Pon.kappa})
        dxy0, M0 = corpi(Z, info["centro_coppia"], quanti)
        maschere = [mm[nodo] for mm in M0]
        print("### [M2330] %s: %d oggett%s, chi %s; i parametri %r; m0 %+.12e; l'impronta %s" % (quale, quanti, "o" if quanti == 1 else "i", "on" if chi_on else "off", P, m0, GD.impronta(Z, C, X)))
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
        ciclo(Z, C, P, Lp, X, K_FINE, dopo)
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
    a = ap.parse_args(argv)
    return noto() if a.cosa == "noto" else corsa(a.quale)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
