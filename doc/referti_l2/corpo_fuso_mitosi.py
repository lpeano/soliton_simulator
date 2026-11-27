# -*- coding: utf-8 -*-
r"""**[M0026] C: LA COPPIA DA k 0 CON chi E LE NASCITE ACCESE** *(DECISIONE DI LUCA, 2026-11-28 00:26; il task history
`doc/TASK_HISTORY/2026-11-28_m0026_corpo_fuso_nascite.md`; la carta `doc/CARTA_mitosi.md`, «C, LA VIA (d)»)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_mitosi.py noto > doc/referti_l2/corpo_fuso_mitosi_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_mitosi.py corsa           (dalla coda: 18000 tick)

**La scena e la partenza sono quelle di `d1`** *(`due_corpi_fondo_v6.costruisci(Z, 2, STATO_G3)`, `D.parametri`, il ciclo di
`due_corpi_fondo_v2` dentro `col_nucleo` e `forma_esplicita("L-1")`, `chi_tick_v2.tick_chi_v2`)*. **Dopo ogni tick:** gli archi con
`|Theta| >= 2 pi` *(`Theta` = `X["theta_a"]`, accumulato da `tick_chi_v2`: la riga di `contatore.ritmo` col lapse `exp(-kappa chi)`)*;
se ce n'e', nasce il primo *(uno per tick, gli altri in attesa: come la mitosi)*. **Alla prima nascita** il campo prototipo diventa
`CampoGenerico` e poi `CampoOrientato` dal toro *(la via di `mitosi_rami_v2.riprendi_v2`)*. **La nascita** e' `mitosi_rami_v2.Rami.nasci`
riga per riga con DUE cambi *(DECISIONE DI LUCA 00:26)*: **(C-1)** `chi` e `pi` del nato = la media dei due estremi dell'arco;
**(C-2)** l'energia della regola, del P9 e di `DH` e' `chi_tick_v2.energia_chi_v2` *(con `H_chi`)*: `MR2.candidato` si chiama com'e' e la
sua `H` si RICALCOLA con `energia_chi_v2` sul motore e sul campo del candidato. Dopo `MR.applica`: `chi`, `pi` allungati, `Lp` ricostruito,
`X["theta_a"]` = il contatore cresciuto. **INGOLFAMENTO:** oltre `500` archi in attesa -> FERMO *(uscita 2)*.
**`noto`:** (K-pre) lo stato costruito a `k 0` = `d1/stato_000000` AL BIT; (K0) le nascite spente, `250` tick = `d1/stato_000250` AL BIT;
(K0-neg) DEVE FALLIRE contro `d1/stato_000500`; (K-nascita) da `d1L/stato_018000` *(`corpo_fuso.Ripresa10`)* una nascita sull'arco di
`|Theta|` massimo: P9 entro `1e-12`, le lunghezze, `chi` e `pi` del nato = la media AL BIT, `C.residuo()` dopo, F3.
**`corsa`:** `18000` tick, gli stati ogni `250`, la serie ogni `10`, `H` ogni `250`; **(K1) a `k 6000`, se non e' nato nessuno, lo stato
= `d1/stato_006000` AL BIT, altrimenti FERMO** *(la lettera: nessuno scatto entro `6000`)*.
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
import corpo_fuso as CF  # noqa: E402
import due_corpi_fondo_v2 as V2D  # noqa: E402
import mitosi_rami_v2 as RV  # noqa: E402

V6, D, CT, PF = CF.V6, CF.D, CF.CT, CF.PF
CV2 = V6.CV2
ML, MR, MR2, MC, CO = RV.ML, RV.MR, RV.MR2, RV.MC, RV.CO
D1 = os.path.join(PF.CTRL, "M2034", "coppia", "d1")
F_K_NASCITA = os.path.join(PF.CTRL, "M2034", "coppia", "d1L", "stato_018000.npz")
D_OUT = os.path.join(PF.CTRL, "M0026", "C")
K_FINE, K_K1 = 18000, 6000
OGNI_STATO, OGNI_SERIE = 250, 10
ATTESA_MAX = 500
QUANTO = 2.0 * math.pi
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    CF.avvia()
    for m in ("mitosi_rami_v2.py", "mitosi_regola_v2.py", "mitosi_regola.py", "mitosi_lunga.py", "chi_tick_v2.py", "due_corpi_fondo_v6.py", "due_corpi_fondo_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    if not V2D.NUC:
        D.avvia()


def diversi(Z, C, X, f):
    """### le chiavi dello stato di `d1` diverse da quelle in memoria (AL BIT)."""
    out = []
    with np.load(f) as z:
        for x in Z["chiavi"]:
            if not np.array_equal(Z["st"][x], z[x]):
                out.append(x)
        for x, v in (("campo_A", C.campo.A), ("campo_E", C.campo.E)):
            if not np.array_equal(v, z[x]):
                out.append(x)
        for q in CT.CHIAVI_CHI:
            if not np.array_equal(X[q], z[q]):
                out.append(q)
    return out


class Energia(object):
    """### `energia_chi_v2` sulla scena e sul candidato (C-2)."""

    def __init__(self, Z, P):
        self.Z, self.P = Z, P

    def H(self, C, X, Lp):
        return CV2.energia_chi_v2(self.Z["mot"], self.Z["st"], self.Z["par"], self.P, Lp, X, C.campo)

    def candidato(self, X, i, j):
        """### un `MR2.candidato` che RICALCOLA `H` con `energia_chi_v2` sul motore e sul campo del candidato, `chi` e `pi` del nato la media."""
        orig = MR2.candidato
        Z, P = self.Z, self.P

        def cand(Z_, C_, a, lato, regola, fattore=True, inverti=None):
            r = orig(Z_, C_, a, lato, regola, fattore, inverti)
            n = int(r["nodi"]["n"])
            X3 = {"chi": np.append(X["chi"], 0.5 * (X["chi"][i] + X["chi"][j])), "pi": np.append(X["pi"], 0.5 * (X["pi"][i] + X["pi"][j]))}
            assert X3["chi"].size == n + 1
            Lp3 = CT.Laplaciano(r["mot"])
            r["H_libro"] = r["H"]
            r["H"], r["H_chi"] = CV2.energia_chi_v2(r["mot"], r["st"], Z["par"], P, Lp3, X3, r["campo"])
            return r
        return orig, cand


class NasciteChi(RV.Rami):
    """### `mitosi_rami_v2.Rami.nasci` riga per riga, con l'energia di `chi` (C-2) e `chi`, `pi`, `Lp`, `theta_a` che seguono il grafo (C-1)."""

    def __init__(self, cont, gacc, centro, en, X):
        RV.Rami.__init__(self, ML.Nascite(cont, 0.0, 0, True), gacc, centro)
        self.en, self.X = en, X
        self.Lp = None

    def nasci(self, Z, C, a, k, perche, Lp):
        t1 = time.time()
        X = self.X
        ii0, jj0 = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
        i, j = int(ii0[a]), int(jj0[a])
        H0, Hc0 = self.en.H(C, X, Lp)
        orig, cand = self.en.candidato(X, i, j)
        MR2.candidato = cand
        try:
            R, S = MR2.regola(Z, C, int(a), "stella")
        finally:
            MR2.candidato = orig
        assert {R["nodi"]["i"], R["nodi"]["j"]} == {i, j}, "i nodi i, j della regola NON sono gli estremi dell'arco %d" % a
        keep, mb = S["keep"], S["mb"]
        nuovi = len(S["ii"]) - mb
        Ec = S["campo"].E - np.concatenate([C.campo.E[keep], np.zeros(nuovi)])
        assert self.gacc.shape == (keep.size,), "gauss_acc non segue il grafo"
        chi_n, pi_n = 0.5 * (X["chi"][i] + X["chi"][j]), 0.5 * (X["pi"][i] + X["pi"][j])
        inf = MR.applica(Z, C, self.cont, S)
        X["chi"] = np.append(X["chi"], chi_n)
        X["pi"] = np.append(X["pi"], pi_n)
        X["theta_a"] = self.cont.theta
        Lp = CT.Laplaciano(Z["mot"])
        eu, dp, tri, _gradi = MR.grafo_ok(np.asarray(S["ii"]), np.asarray(S["jj"]), int(R["nodi"]["n"]) + 1)
        f3 = bool(eu and dp and tri and S["coerenti"] and bool(np.all(C.campo.asg[:, 0] == -C.campo.asg[:, 1])))
        self.gacc = np.concatenate([self.gacc[keep], np.zeros(nuovi)]) + Ec
        H1, Hc1 = self.en.H(C, X, Lp)
        d9 = abs(H1 - S["H"]) / abs(S["H"])
        self.e_persa -= (H1 - H0)
        self.nascite += 1
        nd = R["nodi"]
        n = nd["n"]
        ii, jj = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
        r_n = float(ML.raggi(Z, self.centro)[n])
        b = {"k": int(k), "a": int(a), "perche": perche, "nodi": {x: int(v) for x, v in nd.items()}, "scelto": int(R["scelto"]), "gap": float(R["gap"]),
             "DH_nascita": float(R["H_nascita"] - H0), "DH_flip": float(S["H"] - R["H_nascita"]) if R["scelto"] >= 0 else 0.0, "DH": float(H1 - H0),
             "DH_chi": float(Hc1 - Hc0), "P9": float(d9), "res": float(S["res"]), "E_persa": self.e_persa, "t": time.time() - t1,
             "ok": bool(inf["ok_fuori"] and inf["ok_geo"] and inf["ok_U"]), "F3": f3, "pos": [float(Z["m1"][-1]), float(Z["m2"][-1])], "r": r_n,
             "chi_n": float(chi_n), "pi_n": float(pi_n), "Ec_norma": float(np.linalg.norm(Ec)), "Ec_max": float(np.max(np.abs(Ec)))}
        self.bilanci.append(b)
        print("    [nascita %d] k %d, l'arco %d (%s): n %d a r %.2f; chi_n %+.4f; DH %+.4e (H_chi %+.4e); P9 %.1e; |Ec| %.3e; E_persa %+.6e (%.1f s)" % (
            self.nascite, k, a, perche, n, r_n, chi_n, b["DH"], b["DH_chi"], d9, b["Ec_norma"], self.e_persa, b["t"]))
        sys.stdout.flush()
        assert b["ok"] and d9 <= 1e-12 and f3, "la nascita NON e' entrata nel motore come il candidato (P9 %.1e) o F3 cade (%s): FERMO" % (d9, f3)
        return b, Lp


def ciclo(Z, C, P, Lp, X, quanti, dopo):
    """### `due_corpi_fondo_v2.ciclo` riga per riga, ma `Lp` e' una SCATOLA (`Lp[0]`) riletta a ogni tick: dopo una nascita il Laplaciano e' nuovo."""
    import ripresa_F0_v2 as RF
    MV, P0 = V2D.NUC
    _G20, _ia, _e0, MT = V2D.F1.CL.parametri()
    with RF.col_nucleo(MV, P0), MV.forma_esplicita(V2D.F1.FORMA_OGG):
        assert MV.ATTIVA == V2D.F1.FORMA_OGG and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            CV2.tick_chi_v2(Z["z"], C.campo, P, Lp[0], X)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


def converti(Z, C):
    """### alla prima nascita: il prototipo -> CampoGenerico -> CampoOrientato dal toro (la via di `riprendi_v2`)."""
    import _u1_prototipo as U1
    ori0 = RV.ori_toro(Z)
    g, info = MC.campo_generico(Z, C)
    C.campo = CO.orientato_da(C.campo, ori0)
    U1.scrivi_U(Z["mot"], C.campo)
    return info


def noto():
    avvia()
    print("=" * 134)
    print("[M0026] C, I CASI NOTI: K-pre, K0, K0-neg (d1), K-nascita (d1L/stato_018000)")
    print("=" * 134)
    with V6.GD.TC.scena() as Z:
        mot = Z["mot"]
        Lp = CT.Laplaciano(mot)
        C, info, X = V6.costruisci(Z, 2, V6.STATO_G3)
        P, Pon, m0 = D.parametri(Z, C, True)
        d = diversi(Z, C, X, os.path.join(D1, "stato_000000.npz"))
        esito("(K-pre) lo stato costruito a k 0 = d1/stato_000000 AL BIT", not d, "diverse %s" % d)
        ciclo(Z, C, P, [Lp], X, OGNI_STATO, lambda kk, prima: None)
        d = diversi(Z, C, X, os.path.join(D1, "stato_000250.npz"))
        esito("(K0) le nascite spente: 250 tick = d1/stato_000250 AL BIT", not d, "diverse %s" % d)
        d = diversi(Z, C, X, os.path.join(D1, "stato_000500.npz"))
        esito("(K0-neg) DEVE FALLIRE: lo stesso stato contro d1/stato_000500", bool(d), "diverse %s" % d)
        Z["metti"]()
    with V6.GD.TC.scena() as Z:
        R = CF.Ripresa10(Z, F_K_NASCITA, 18000, "M0026_noto")
        C, X, P = R.C, R.X, R.P
        t = np.abs(X["theta_a"])
        a = int(np.argmax(t))
        print("  K-nascita: da %s; max |Theta| %.4f all'arco %d; archi oltre 2 pi %d" % (F_K_NASCITA, float(t[a]), a, int((t >= QUANTO).sum())))
        n0, m0_ = Z["mot"].inc.n, Z["mot"].inc.m
        inf = converti(Z, C)
        print("  il campo convertito: %s" % inf)
        import contatore as COn
        cont = COn.Contatore(X["theta_a"])
        cont.theta = X["theta_a"]
        NS = NasciteChi(cont, np.zeros(m0_), R.meta["centro_coppia"], Energia(Z, P), X)
        ii0, jj0 = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
        i, j = int(ii0[a]), int(jj0[a])
        chi_att, pi_att = 0.5 * (X["chi"][i] + X["chi"][j]), 0.5 * (X["pi"][i] + X["pi"][j])
        b, Lp = NS.nasci(Z, C, a, 18000, "K-nascita", R.Lp)
        X = NS.X
        n1, m1_ = Z["mot"].inc.n, Z["mot"].inc.m
        esito("(K-nascita) P9: l'energia di chi riletta dal motore vero = quella del candidato entro 1e-12", b["P9"] <= 1e-12, "%.2e; DH %+.6e, DH_chi %+.6e" % (b["P9"], b["DH"], b["DH_chi"]))
        esito("(K-nascita) n + 1 nodi e m + 3 archi; chi, pi, theta_a, Lp seguono il grafo",
              n1 == n0 + 1 and m1_ == m0_ + 3 and X["chi"].size == n1 and X["pi"].size == n1 and X["theta_a"].size == m1_ and Lp.ii.size == m1_,
              "n %d -> %d, m %d -> %d; chi %d, pi %d, theta %d, Lp %d" % (n0, n1, m0_, m1_, X["chi"].size, X["pi"].size, X["theta_a"].size, Lp.ii.size))
        esito("(K-nascita) chi e pi del nato = la media dei due estremi dell'arco AL BIT", X["chi"][-1] == chi_att and X["pi"][-1] == pi_att, "chi %+.6e, pi %+.6e" % (X["chi"][-1], X["pi"][-1]))
        esito("(K-nascita) F3 e il candidato entrato nel motore (ok)", b["F3"] and b["ok"], "")
        r = R.C.residuo()
        esito("(K-nascita) C.residuo() gira col campo orientato dopo la nascita", r is not None and np.isfinite(r), "%r" % (r,))
        CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
        esito("(K-nascita) un tick dopo la nascita gira (le lunghezze tengono)", X["theta_a"].size == Z["mot"].inc.m and np.all(np.isfinite(X["chi"])), "")
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


def corsa():
    import contatore as COn
    from solitone import _registro_corse as RC
    avvia()
    assert not os.path.exists(os.path.join(D_OUT, "stato_000000.npz")), "%s c'e' gia': non si riscrive" % D_OUT
    os.makedirs(D_OUT, exist_ok=True)
    codice = [0]
    with V6.GD.TC.scena() as Z:
        mot = Z["mot"]
        Lp = [CT.Laplaciano(mot)]
        C, info, X = V6.costruisci(Z, 2, V6.STATO_G3)
        P, Pon, m0 = D.parametri(Z, C, True)
        en = Energia(Z, P)
        meta = dict(info, corsa="M0026_C", parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f, "kappa_on": Pon.kappa},
                    nascite_accese=True, quanto=QUANTO, chi_nato="media degli estremi", energia_regola="energia_chi_v2")
        centro = info["centro_coppia"]
        cont = COn.Contatore(X["theta_a"])
        cont.theta = X["theta_a"]
        NS = NasciteChi(cont, np.zeros(mot.inc.m), centro, en, X)
        G = {}

        def geometria():
            G["nodo"] = np.asarray(Z["mot"].inc.nodo)
            G["n"] = Z["mot"].inc.n
            G["dxy"], M0 = D.corpi(Z, centro, 2)
            G["masch"] = [mm[G["nodo"]] for mm in M0]
            G["M0"] = M0
        geometria()
        serie, om, serie_H = [], [[], []], []
        t1 = time.time()
        convertito = [False]

        def salva(k):
            fz = os.path.join(D_OUT, "stato_%06d.npz" % k)
            m = Z["mot"]
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: NS.X[q] for q in CT.CHIAVI_CHI}, gauss_acc=NS.gacc)
            if NS.nascite:
                dati.update(ii=np.asarray(m.inc.nodo[0::2]), jj=np.asarray(m.inc.nodo[1::2]), geo_n=m.geo.n, campo_vec=C.campo.vec,
                            ori_cicli=C.campo.ori_cicli(), m1=np.asarray(Z["m1"], dtype=float), m2=np.asarray(Z["m2"], dtype=float))
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k, E_persa=NS.e_persa, nascite=NS.nascite, n=int(m.inc.n)))), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
            open(os.path.join(D_OUT, "nascite.json"), "w", encoding="utf-8").write(json.dumps(NS.bilanci))
            H, Hc = en.H(C, NS.X, Lp[0])
            serie_H.append([k, H, Hc, NS.e_persa, NS.nascite, int(m.inc.n)])

        def misura(kk):
            rho = np.bincount(G["nodo"], weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=G["n"])
            riga = [kk]
            for mm in G["M0"]:
                w = rho * mm
                c = (G["dxy"] * w[:, None]).sum(axis=0) / w.sum()
                riga += [float(c[0]), float(c[1]), float(w.sum())]
            riga.append(float(np.max(np.abs(NS.X["chi"]))))
            serie.append(riga)

        class Fermo(Exception):
            pass

        def dopo(kk, prima):
            for jx, ms in enumerate(G["masch"]):
                om[jx].append(float(-np.angle(np.vdot(prima[ms], Z["st"]["psi_h"][ms]))))
            sc = np.nonzero(np.abs(NS.X["theta_a"]) >= QUANTO)[0]
            if sc.size > ATTESA_MAX:
                print("### INGOLFAMENTO a k %d: %d archi in attesa (> %d): FERMO" % (kk, sc.size, ATTESA_MAX))
                codice[0] = 2
                salva(kk)
                raise Fermo()
            if sc.size:
                if not convertito[0]:
                    print("    [il campo] alla prima nascita (k %d): %s" % (kk, converti(Z, C)))
                    convertito[0] = True
                _b, Lp[0] = NS.nasci(Z, C, int(sc[0]), kk, "scattato; %d in attesa" % (sc.size - 1), Lp[0])
                geometria()
            if kk == K_K1:
                if NS.nascite == 0:
                    dd = diversi(Z, C, NS.X, os.path.join(D1, "stato_%06d.npz" % K_K1))
                    print("### (K1) a k %d nessuna nascita; lo stato contro d1/stato_%06d: %s" % (kk, K_K1, "AL BIT" if not dd else "### DIVERSE %s" % dd))
                    if dd:
                        codice[0] = 1
                        raise Fermo()
                else:
                    print("### (K1) FALLISCE: %d nascite prima di k %d (la lettera: nessuna): FERMO" % (NS.nascite, K_K1))
                    codice[0] = 1
                    salva(kk)
                    raise Fermo()
            if kk % OGNI_SERIE == 0:
                misura(kk)
            if kk % OGNI_STATO == 0:
                salva(kk)
                print("    k %d: %s; max|chi| %.4e; nascite %d, n %d; H %+.10e, E_persa %+.6e (%.0f s)" % (
                    kk, " ".join("y%d %+.4f" % (q + 1, serie[-1][2 + 3 * q]) for q in range(2)), serie[-1][-1], NS.nascite, G["n"], serie_H[-1][1], NS.e_persa, time.time() - t1))
                sys.stdout.flush()

        print("### [M0026] C: la coppia da k 0 (d1), chi acceso, le nascite ACCESE; %d tick; gli stati in %s; i parametri %r" % (K_FINE, D_OUT, meta["parametri"]))
        sys.stdout.flush()
        salva(0)
        misura(0)
        try:
            ciclo(Z, C, P, Lp, NS.X, K_FINE, dopo)
        except Fermo:
            pass
        f = os.path.join(D_OUT, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"meta": meta, "serie": serie, "omega": om, "H": serie_H}))
        PF.firma(f)
        if NS.nascite == 0:
            Z["metti"]()
    print("### %s in %.0f s; nascite %d; il codice %d" % ("FERMO" if codice[0] else "%d tick" % K_FINE, time.time() - t1, NS.nascite, codice[0]))
    return codice[0]


def main(argv):
    a = argparse.ArgumentParser()
    a.add_argument("modo", choices=("noto", "corsa"))
    x = a.parse_args(argv)
    return noto() if x.modo == "noto" else corsa()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
