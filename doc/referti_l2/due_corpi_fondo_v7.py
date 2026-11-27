# -*- coding: utf-8 -*-
r"""**[M1016] LA CORSA LUNGA d1'': LA COPPIA RIPRESA DA UNO STATO** *(DECISIONE DI LUCA, 2026-11-27 `10:16`; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-vicies`, il seguito [M1016], «LA CORSA LUNGA d1''», scritta PRIMA; `due_corpi_fondo_v6.py` e' usato e non si riscrive: la v7 lo importa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v7.py noto > doc/referti_l2/due_corpi_fondo_v7_noto.txt      (K0', K0'-neg)
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v7.py corsa       (d1'': da stato_006000 a k 18000; dalla coda)

**La via di d1':** `costruisci` della v6 e `D.parametri` *(nello stesso ordine della corsa: `P` e `m0` PRIMA di caricare lo stato; asseriti uguali al meta di `serie.json`, e `centro_coppia` pure)*; poi lo stato in place *(le chiavi di `st`, `campo_A`/`campo_E` in `C.campo`, `chi, pi, theta_a` in `X`)*; il ciclo e' il corpo di `due_corpi_fondo.ciclo` **col tick ASSOLUTO** *(`C.residuo` a `k % OGNI_GAUSS == 0` come nella corsa originale)*. **(K0')** da `stato_005750` per `250` tick: lo stato uguale AL BIT a `stato_006000` in ogni chiave, la serie `5760..6000` e `omega` dei tick `5751..6000` uguali AL BIT a `serie.json`; **(K0'-neg)** la stessa senza caricare `campo_E`: lo stato DEVE essere diverso. **Prima del ciclo** la riga della serie a `k_da` uguale AL BIT a quella di `serie.json`. **La corsa** in `M2034/coppia/d1L`: gli stati ogni `250` col `k` ASSOLUTO, la serie ogni `10`, `omega[j][i]` = il tick `k_da + 1 + i`.
"""
import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v6 as V6  # noqa: E402

V4, D, F1, PF, CT, CV2, GD = V6.V4, V6.D, V6.F1, V6.PF, V6.CT, V6.CV2, V6.GD
D1 = os.path.join(PF.CTRL, "M2034", "coppia", "d1")
D_OUT = os.path.join(PF.CTRL, "M2034", "coppia", "d1L")
K_DA, K_A, OGNI_STATO, OGNI_SERIE = 6000, 18000, 250, 10


def avvia():
    D.avvia()
    import _presidio
    for m in ("due_corpi_fondo_v4.py", "due_corpi_fondo_v6.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def serie_d1():
    f = os.path.join(D1, "serie.json")
    PF.controlla(f)
    return json.load(open(f, encoding="utf-8"))


class Ripresa:
    """### la scena di d1' ripresa da `stato_<k_da>`: `Z, C, P, Lp, X`, le maschere e la misura."""

    def __init__(self, Z, k_da, campo_E=True):
        S = serie_d1()
        mt = S["meta"]
        self.Z, self.k_da = Z, k_da
        mot = Z["mot"]
        self.n = mot.inc.n
        self.nodo = np.asarray(mot.inc.nodo)
        self.Lp = CT.Laplaciano(mot)
        self.C, info, self.X = V6.costruisci(Z, 2, V6.STATO_G3)
        self.P, Pon, m0 = D.parametri(Z, self.C, True)
        par = {"kappa": self.P.kappa, "c0": self.P.c0, "m0": m0, "c2": self.P.c2, "m2": self.P.m2, "e0": self.P.e0, "s": self.P.s, "f": self.P.f, "kappa_on": Pon.kappa}
        assert par == mt["parametri"], "i parametri NON sono quelli di d1': %r contro %r" % (par, mt["parametri"])
        assert info["centro_coppia"] == mt["centro_coppia"], "centro_coppia NON e' quello di d1'"
        self.meta = dict(info, corsa="d1L", da=os.path.join(D1, "stato_%06d.npz" % k_da), k_da=k_da, parametri=par)
        self.dxy0, M0 = D.corpi(Z, info["centro_coppia"], 2)
        self.maschere = [mm[self.nodo] for mm in M0]
        self.M0 = M0
        f = os.path.join(D1, "stato_%06d.npz" % k_da)
        PF.controlla(f)
        with np.load(f) as z:
            for x in Z["chiavi"]:
                assert Z["st"][x].shape == z[x].shape
                Z["st"][x][...] = z[x]
            self.C.campo.A[...] = z["campo_A"]
            if campo_E:
                self.C.campo.E[...] = z["campo_E"]
            for q in CT.CHIAVI_CHI:
                self.X[q][...] = z[q]
        self.serie, self.om = [], [[] for _ in M0]

    def misura(self, kk):
        rho = np.bincount(self.nodo, weights=np.sum(np.abs(self.Z["st"]["psi_h"]) ** 2, axis=1), minlength=self.n)
        riga = [kk]
        for mm in self.M0:
            w = rho * mm
            c = (self.dxy0 * w[:, None]).sum(axis=0) / w.sum()
            riga += [float(c[0]), float(c[1]), float(w.sum())]
        riga.append(float(np.max(np.abs(self.X["chi"]))))
        return riga

    def gira(self, ticks, dopo_extra=None):
        """### il corpo di `due_corpi_fondo.ciclo` col tick ASSOLUTO `k_da + 1 .. k_da + ticks`."""
        import ripresa_F0_v2 as RF
        Z, C, P, Lp, X = self.Z, self.C, self.P, self.Lp, self.X
        MV, P0 = F1.TT.nucleo()
        _G20, _ia, _e0, MT = F1.CL.parametri()
        assert MT.OGNI_GAUSS == 250 and self.k_da % MT.OGNI_GAUSS == 0
        with RF.col_nucleo(MV, P0), MV.forma_esplicita(F1.FORMA_OGG):
            assert MV.ATTIVA == F1.FORMA_OGG and MV.pezzi is P0
            for kk in range(self.k_da + 1, self.k_da + ticks + 1):
                prima = Z["st"]["psi_h"].copy()
                CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
                if kk % MT.OGNI_GAUSS == 0:
                    C.residuo()
                for j, ms in enumerate(self.maschere):
                    self.om[j].append(float(-np.angle(np.vdot(prima[ms], Z["st"]["psi_h"][ms]))))
                if kk % OGNI_SERIE == 0:
                    self.serie.append(self.misura(kk))
                if dopo_extra is not None:
                    dopo_extra(kk)

    def dati(self):
        d = {x: self.Z["st"][x] for x in self.Z["chiavi"]}
        d.update(campo_A=self.C.campo.A, campo_E=self.C.campo.E, **{q: self.X[q] for q in CT.CHIAVI_CHI})
        return d


def noto():
    avvia()
    print("=" * 130)
    print("[M1016] (K0') LA RIPRESA DA UNO STATO: da stato_005750, 250 tick, contro stato_006000 e serie.json AL BIT; (K0'-neg) senza campo_E")
    print("=" * 130)
    S = serie_d1()
    rif = {int(r[0]): r for r in S["serie"]}
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    with np.load(os.path.join(D1, "stato_006000.npz")) as z:
        fin = {x: z[x].copy() for x in z.files if x != "meta"}
    for neg in (False, True):
        t1 = time.time()
        with GD.TC.scena() as Z:
            R = Ripresa(Z, 5750, campo_E=not neg)
            r0 = R.misura(5750)
            if not neg:
                esito("(carica) la riga della serie a k 5750 = quella di serie.json AL BIT", r0 == rif[5750], "%r" % r0[:3])
            R.gira(250)
            dd = R.dati()
            diversi = [x for x in fin if not np.array_equal(np.asarray(dd[x]), fin[x])]
            if not neg:
                esito("(K0') lo stato a k 6000 = stato_006000.npz AL BIT, in ogni chiave (%d)" % len(fin), not diversi, "diverse: %s" % diversi)
                ks = [int(r[0]) for r in R.serie]
                esito("(K0') la serie %d..%d (%d righe) = serie.json AL BIT" % (ks[0], ks[-1], len(ks)), all(r == rif[int(r[0])] for r in R.serie))
                esito("(K0') omega dei tick 5751..6000, i due corpi = serie.json AL BIT", all(R.om[j] == S["omega"][j][5750:6000] for j in range(2)))
            else:
                esito("(K0'-neg) senza campo_E lo stato a k 6000 e' DIVERSO da stato_006000", bool(diversi), "diverse: %s" % diversi)
            Z["metti"]()
        print("    (%s: %.0f s)" % ("K0'-neg" if neg else "K0'", time.time() - t1))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa():
    avvia()
    assert not os.path.exists(os.path.join(D_OUT, "stato_%06d.npz" % (K_DA + OGNI_STATO))), "%s c'e' gia': non si riscrive" % D_OUT
    os.makedirs(D_OUT, exist_ok=True)
    S = serie_d1()
    t1 = time.time()
    with GD.TC.scena() as Z:
        R = Ripresa(Z, K_DA)
        r0 = R.misura(K_DA)
        assert r0 == [r for r in S["serie"] if int(r[0]) == K_DA][0], "la riga a k %d NON e' quella di serie.json" % K_DA
        R.serie.append(r0)
        print("### [M1016] d1'': da %s, %d tick (fino a k %d); la riga a k %d = serie.json AL BIT" % (R.meta["da"], K_A - K_DA, K_A, K_DA))
        sys.stdout.flush()

        def salva(kk):
            if kk % OGNI_STATO:
                return
            fz = os.path.join(D_OUT, "stato_%06d.npz" % kk)
            np.savez(fz, meta=np.array(json.dumps(dict(R.meta, k=kk))), **R.dati())
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
            u = R.serie[-1]
            print("    k %d: y1 %+.4f y2 %+.4f; max|chi| %.4e (%.0f s)" % (kk, u[2], u[5], u[-1], time.time() - t1))
            sys.stdout.flush()
        R.gira(K_A - K_DA, salva)
        f = os.path.join(D_OUT, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"meta": R.meta, "serie": R.serie, "omega": R.om}))
        PF.firma(f)
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_A - K_DA, time.time() - t1))
    ok = os.path.exists(os.path.join(D_OUT, "stato_%06d.npz.sha1" % K_A))
    print("### stato_%06d.npz %s" % (K_A, "ESISTE" if ok else "### NON ESISTE"))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa"))
    a = ap.parse_args(argv)
    return noto() if a.cosa == "noto" else corsa()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
