# -*- coding: utf-8 -*-
r"""**IL MATTONE CON `chi` ALLA VELOCITA' DELLA LUCE: LA CORSA E LE PROVE S1, S2, S3, S5** *(il mandato di Luca `2026-11-21` `23:30`; la carta `doc/TASK_HISTORY/2026-11-21_lorentz_locale.md`, sez. `4.3`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_mattone_v3.py s1_s2 > doc/referti_l2/chi_v2_s1_s2.txt
    E:\python\py3132\python.exe doc/referti_l2/chi_mattone_v3.py s3 > doc/referti_l2/chi_v2_s3.txt
    E:\python\py3132\python.exe doc/referti_l2/chi_mattone_v3.py s5 > doc/referti_l2/chi_v2_s5.txt
    E:\python\py3132\python.exe doc/referti_l2/chi_mattone_v3.py corsa --fino 20000 --registro chi-mattone-v2

**`corsa`:** il cammino di `chi_mattone.corsa` *(da `k 0` di C2, `prepara` senza bordo, `chi` al profilo statico, le stesse misure ogni `50`, gli stati ogni `250`)* e, con `--da`, quello di `chi_mattone_v2.corsa` *(la ripresa da uno stato)*, **col passo `chi_tick_v2.tick_chi_v2`, l'energia `energia_chi_v2`, i parametri `parametri_v2`** *(`kappa` il numero, `f`)*; gli stati in `E:/soliton_simulator/controllo/CHI/mattone_v2/`.
**S1:** `chi_statico` coi `Parametri` di oggi = coi `Parametri2`, AL BIT. **S2:** l'onda stazionaria del solo `chi` *(toro `48`, `400` tick, il passo v2 con la sola forza)*: `omega` = `acos(1 - f (c2 lambda + m2)/2)` entro `1e-10`; `v` senza massa `0.15` entro `1e-6`; DEVE FALLIRE `f = 1`. **S3:** `500` tick da `k 0` col passo v2 e col passo di oggi: la deriva relativa massima di `H` *(ogni `50` tick)* v2 non oltre `10` volte quella di oggi `+ 1e-12`; DEVE FALLIRE l'energia vecchia *(`pi^2/2`)* sulla dinamica v2. **S5:** `10` tick di fila contro `5` + salva + riprendi + `5`, AL BIT; un byte cambiato -> RIFIUTA.
"""
import argparse
import json
import math
import os
import shutil
import sys
import time
import types

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402
import chi_mattone as CM  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "mattone_v2")
DIR_PROVA = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "prova_v2")
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  %-112s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def fine():
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def corsa(k_fino, reg, d_out, f_da=None, v1=False, energia_ogni=None):
    """### da `k 0` *(f_da None)* o dallo stato `f_da`; `v1`: il passo e l'energia di OGGI *(solo S3)*. `(k, fine, serie_H)`."""
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    from solitone import _registro_corse as RC
    from solitone import toro as TO
    MT, CTO, CV, MR = PS.MT, PS.CT, PS.CV, PS.MR
    PS.presidi()
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    t00 = time.time()
    os.makedirs(d_out, exist_ok=True)
    serie_H = []
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)
        C0 = PS.PO.campi(Z, rho_c, e)
        e0 = float(C0.e0)
        P, m0 = CV2.parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, "C2")
        if v1:
            P = CT.Parametri(P.kappa, P.c0, P.s, P.e0, P.c2, P.m2)
        tick = CT.tick_chi if v1 else CV2.tick_chi_v2
        energia = CT.energia_chi if v1 else CV2.energia_chi_v2
        if f_da is None:
            C, meta = CSB.prepara(Z, 186, False, rho_c, e, t0)
            rho = MT.rho_di(Z)
            meta["centro"] = [float(x) for x in MT.centro_di(Z, rho)]
            meta["lab"] = meta["centro"]
            meta["parametri"] = {"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": getattr(P, "f", 1.0)}
            M = CSB.Misure(Z, meta["centro"])
            X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0))
            EX = {x: [] for x in ("k", "picco", "H", "H_chi", "chi_medio", "max_theta") + tuple("uN_%d" % R for R in CM.ANELLI) + tuple("rit_%d" % R for R in CM.ANELLI)}
            k_da = 0
        else:
            C, meta, cs, sh = CSB.riprendi(Z, f_da, False, rho_c, e)
            k_da = int(meta["k"])
            pm = meta["parametri"]
            for q in ("kappa", "c0", "c2", "m2", "e0", "s", "f"):
                assert getattr(P, q) == pm[q], "il parametro %s %r contro %r nel meta: FERMO" % (q, getattr(P, q), pm[q])
            with np.load(f_da) as d:
                X = {q: d[q].copy() for q in CT.CHIAVI_CHI}
            M = CSB.Misure(Z, meta["centro"])
            sfx = os.path.basename(f_da)[6:-4]
            with np.load(os.path.join(os.path.dirname(f_da), "serie_%s.npz" % sfx)) as d:
                M.S = {x: list(d[x]) for x in d.files}
            with np.load(os.path.join(os.path.dirname(f_da), "serie_chi_%s.npz" % sfx)) as d:
                EX = {x: list(d[x]) for x in d.files}
        print("### %s da k %d fino a k %d (%s); i parametri %r; m0 %+.12e; gli stati in %s" % ("IL PASSO DI OGGI" if v1 else "IL PASSO V2 (l'inerzia f)", k_da, k_fino, os.path.basename(f_da) if f_da else "prepara", P, m0, d_out))
        sys.stdout.flush()
        r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], meta["centro"][0], meta["centro"][1], Z["L"]).T[:2])
        c0n = int(np.argmin(r))
        nodo = np.asarray(mot.inc.nodo)
        ra = 0.5 * (r[nodo[0::2]] + r[nodo[1::2]])

        class CorsaChi(CTO.Corsa):
            def passo(self, k, t, r_, e_):
                C_, Z_ = self.C, self.Z
                if e_ > 0.0 and C_.e_prec == 0.0:
                    rh = MT.rho_di(Z_)
                    C_.campo.A[...] = 0.0
                    C_.campo.E[...] = C_.gauss(e_ * (rh - rh.mean()))
                elif C_.e_prec > 0.0:
                    C_.campo.E *= e_ / C_.e_prec
                C_.campo.e = e_
                C_.e_prec = e_
                tick(Z_["z"], C_.campo, P, Lp, X)
                totp = float(np.sum(CTO.CO.conti_nodo(Z_)["tot"]))
                self.registra(k, totp, self.kv(), float(np.sum(np.abs(Z_["st"]["psi_h"]) ** 2)))

        def misura_chi(k):
            rh = MT.rho_di(Z)
            H, Hc = energia(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
            uN = 1.0 - np.exp(-P.kappa * X["chi"])
            cs_ = P.s * np.exp(-P.kappa * X["chi"])
            rit = math.pi * np.abs(cs_[nodo[0::2]] - cs_[nodo[1::2]])
            EX["k"].append(k)
            EX["picco"].append(float(rh.max()))
            EX["H"].append(H)
            EX["H_chi"].append(Hc)
            EX["chi_medio"].append(float(X["chi"].mean()))
            EX["max_theta"].append(float(np.max(np.abs(X["theta_a"]))))
            for R in CM.ANELLI:
                EX["uN_%d" % R].append(float(uN[c0n]) if R == 0 else CM.anello(r, uN, R))
                EX["rit_%d" % R].append(CM.anello(ra, rit, R) if R > 0 else float(np.mean(rit[(nodo[0::2] == c0n) | (nodo[1::2] == c0n)])))

        def salva(k):
            fz = os.path.join(d_out, "stato_%05d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = CM.sha1(fz)
            with open(fz + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            M.salva(os.path.join(d_out, "serie_%05d.npz" % k))
            np.savez(os.path.join(d_out, "serie_chi_%05d.npz" % k), **{q: np.array(v_) for q, v_ in EX.items()})
            return h

        RC_ = CorsaChi(Z, C)
        RC_.etichette([meta["lab"]])
        RC_.inizio(k_da)
        t1 = t_tappa = time.time()
        R5 = rg = float("nan")
        k = k_da
        for k in range(k_da, k_fino + 1):
            if k > k_da:
                RC_.passo(k, t0 + k, 1.0, e)
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            if k > 0 and k > k_da and k % CTO.OGNI == 0:
                RC_.etichette([c])
                meta["lab"] = [float(x) for x in c]
            if k % PS.OGNI == 0:
                R5, _rr, _b = PS.r5(Z, t0 + k)
                rg = MR.raggio(Z, rho, c)
            if k % PS.OGNI_MAPPA == 0:
                PS.PO.dphi_nodi(Z, t0 + k)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % CM.OGNI == 0 and (k > k_da or f_da is None):
                M.misura(k, RC_, R5, rg)
                misura_chi(k)
            if energia_ogni and k % energia_ogni == 0:
                H, Hc = energia(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
                Hv = CT.energia_chi(mot, Z["st"], Z["par"], P, Lp, X, C.campo)[0] if not v1 else H
                serie_H.append((k, H, Hv))
            if k % 250 == 0 and (k > k_da or f_da is None):
                S = M.S
                print("    k %5d  la massa %.12e  il raggio %.4f  Min12.4 %.6e  il picco %.4e  H %+.10e  H_chi %+.4e  1-N centro %.4e  max|Theta| %.4f  (%.0f s)" % (
                    k, S["M"][-1], S["raggio"][-1], S["Min_12.4"][-1], EX["picco"][-1], EX["H"][-1], EX["H_chi"][-1], EX["uN_0"][-1], EX["max_theta"][-1], time.time() - t00))
                sys.stdout.flush()
            if k > k_da and (k % CM.OGNI_STATO == 0 or k == k_fino):
                h = salva(k)
                print("    [stato] k %d sha1 %s" % (k, h[:8]))
            adesso = time.time()
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                RC.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), MT.memoria_gb()))
                t_tappa = adesso
        fin = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy(), CT.copia_X(X))
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick)" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da)))
    return k, fin, serie_H


def s1_s2():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("S1 E S2 DI CHI V2 (Luca 2026-11-21 23:30; la carta sez. 4.3)")
    print("=" * 130)
    import lorentz_velocita as LV
    c2, m2c = CT.C_CHI ** 2, (1.0 / CT.PORTATA) ** 2
    s = 0.15
    f = CV2.inerzia(s, c2)
    print("### f = (s / (c sqrt(3/2)))^2 = %r (s %r, c2 %r)" % (f, s, c2))
    # ### S1: il pozzo invariato, sul toro 48 con una sorgente a caso
    L = 48
    ii, jj, m1, m2_ = LV.toro(L)
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    Lp = CT.Laplaciano(types.SimpleNamespace(inc=types.SimpleNamespace(nodo=nodo, n=L * L)))
    rng = np.random.default_rng(7)
    sorg = rng.standard_normal(L * L)
    P1 = CT.Parametri(2.5e-4, 3.8e-4, s, 0.5)
    P2 = CV2.Parametri2(2.5e-4, 3.8e-4, s, 0.5, f)
    a, b = Lp.statico(P1, sorg), CT.Laplaciano(types.SimpleNamespace(inc=types.SimpleNamespace(nodo=nodo, n=L * L))).statico(P2, sorg)
    print("### S1: il profilo statico (c2 L + m2)^-1 sorgente coi Parametri e coi Parametri2: %s" % ("AL BIT" if np.array_equal(a, b) else "### DIVERSO %.1e" % float(np.max(np.abs(a - b)))))
    esito("S1: il pozzo statico invariato AL BIT (la formula non contiene f)", np.array_equal(a, b))
    # ### S2: l'onda stazionaria
    a1, a2 = LV.vettori()
    dirs = (a1, a2, a1 + a2)
    r = LV.posizioni(L)
    k = LV.k_griglia(1, 0, L)
    for m2 in (0.0, m2c):
        x = np.cos(r @ k)
        p = np.zeros_like(x)
        serie = []
        for _t in range(401):
            if _t:
                p += 0.5 * f * (c2 * Lp.delta(x) - m2 * x)
                x += 0.5 * p
                x += 0.5 * p
                p += 0.5 * f * (c2 * Lp.delta(x) - m2 * x)
            serie.append(float(x @ np.cos(r @ k)) / float(np.cos(r @ k) @ np.cos(r @ k)))
        om_m, _sp = LV.misura_omega(serie)
        om_f = math.acos(1.0 - 0.5 * f * (c2 * LV.lam_chi(k, dirs) + m2))
        err = abs(om_m - om_f) / om_f
        print("### S2 (m2 %r): omega misurata %.14f, formula con f %.14f (lo scarto %.1e)" % (m2, om_m, om_f, err))
        esito("S2 (m2 %r): omega dell'onda stazionaria = la formula con f entro 1e-10" % m2, err <= 1e-10, "%.1e" % err)
    kk = 1e-4
    v = math.acos(1.0 - 0.5 * f * c2 * LV.lam_chi(np.array([kk, 0.0]), dirs)) / kk
    v1 = math.acos(1.0 - 0.5 * 1.0 * c2 * LV.lam_chi(np.array([kk, 0.0]), dirs)) / kk
    print("### S2: v senza massa a |k| 1e-4: %.10f archi per tick (la luce %.10f); con f = 1: %.10f" % (v, s, v1))
    esito("S2: v senza massa = 0.15000 entro 1e-6", abs(v - s) <= 1e-6, "%.10f" % v)
    esito("S2 DEVE FALLIRE: con f = 1 la velocita' NON e' 0.15 (0.6124)", abs(v1 - s) > 1e-3, "%.4f" % v1)
    return fine()


def s3():
    print("=" * 130)
    print("S3 DI CHI V2: L'ENERGIA (Luca 2026-11-21 23:30; la carta sez. 4.3): 500 tick da k 0 col passo v2 e col passo di oggi")
    print("=" * 130)
    _k, _f, Hv2 = corsa(500, None, os.path.join(DIR_PROVA, "s3_v2"), energia_ogni=50)
    _k, _f, Hv1 = corsa(500, None, os.path.join(DIR_PROVA, "s3_v1"), v1=True, energia_ogni=50)
    H2 = np.array([h for _k, h, _v in Hv2])
    Hvecchia = np.array([v for _k, _h, v in Hv2])
    H1 = np.array([h for _k, h, _v in Hv1])
    d2 = float(np.max(np.abs(H2 - H2[0]))) / abs(H2[0])
    d1 = float(np.max(np.abs(H1 - H1[0]))) / abs(H1[0])
    dv = float(np.max(np.abs(Hvecchia - Hvecchia[0]))) / abs(Hvecchia[0])
    print("### S3: la deriva relativa massima di H in 500 tick (ogni 50): v2 (pi^2/2f) %.3e; il passo di oggi %.3e; l'energia vecchia (pi^2/2) sulla dinamica v2 %.3e" % (d2, d1, dv))
    for (k, h, v), (_k1, h1, _v1) in zip(Hv2, Hv1):
        print("    k %4d: H v2 %+.12e   H oggi %+.12e   l'energia vecchia sulla v2 %+.12e" % (k, h, h1, v))
    esito("S3: la deriva di H v2 non oltre 10 volte quella di oggi + 1e-12", d2 <= 10.0 * d1 + 1e-12, "%.2e contro %.2e" % (d2, 10.0 * d1 + 1e-12))
    esito("S3 DEVE FALLIRE: l'energia vecchia sulla dinamica v2 oltre la stessa soglia", dv > 10.0 * d1 + 1e-12, "%.2e" % dv)
    return fine()


def s5():
    print("=" * 130)
    print("S5 DI CHI V2: LA RIPRESA (Luca 2026-11-21 23:30; la carta sez. 4.3): 10 tick di fila contro 5 + salva + riprendi + 5")
    print("=" * 130)
    if os.path.isdir(os.path.join(DIR_PROVA, "s5")):
        shutil.rmtree(os.path.join(DIR_PROVA, "s5"))
    _k, fila, _h = corsa(10, None, os.path.join(DIR_PROVA, "s5", "fila"))
    _k, _f, _h = corsa(5, None, os.path.join(DIR_PROVA, "s5", "spezza"))
    fm = os.path.join(DIR_PROVA, "s5", "spezza", "stato_00005.npz")
    _k, rip, _h = corsa(10, None, os.path.join(DIR_PROVA, "s5", "spezza"), f_da=fm)
    st1, A1, E1, X1 = fila
    st2, A2, E2, X2 = rip
    dd = [x for x in st1 if not np.array_equal(st1[x], st2[x])] + [x for x, a, b in (("A", A1, A2), ("E", E1, E2)) if not np.array_equal(a, b)] + [q for q in CT.CHIAVI_CHI if not np.array_equal(X1[q], X2[q])]
    print("### S5: 10 tick di fila contro la ripresa da %s (sha1 %s): %s" % (os.path.basename(fm), CM.sha1(fm)[:8], "AL BIT (ogni array, A, E, chi, pi, theta_a)" if not dd else "### DIVERSE: %s" % dd))
    esito("S5: la ripresa col passo v2 AL BIT", not dd)
    fr = os.path.join(DIR_PROVA, "s5", "rotto", "stato_00005.npz")
    os.makedirs(os.path.dirname(fr), exist_ok=True)
    shutil.copyfile(fm, fr)
    shutil.copyfile(fm + ".sha1", fr + ".sha1")
    for x in ("serie_00005.npz", "serie_chi_00005.npz"):
        shutil.copyfile(os.path.join(os.path.dirname(fm), x), os.path.join(os.path.dirname(fr), x))
    with open(fr, "r+b") as fh:
        fh.seek(os.path.getsize(fr) // 2)
        b = fh.read(1)
        fh.seek(os.path.getsize(fr) // 2)
        fh.write(bytes([b[0] ^ 0x01]))
    rifiuta = False
    try:
        corsa(6, None, os.path.join(DIR_PROVA, "s5", "rotto"), f_da=fr)
    except AssertionError as ex:
        rifiuta = "sha1" in str(ex)
        print("### S5 DEVE FALLIRE: un byte cambiato: %s" % ex)
    esito("S5 DEVE FALLIRE: un byte dello stato cambiato -> la ripresa RIFIUTA (lo sha1)", rifiuta)
    return fine()


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for x in ("s1_s2", "s3", "s5"):
        sub.add_parser(x)
    c = sub.add_parser("corsa")
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--da")
    c.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd == "corsa":
        corsa(x.fino, x.registro, DIR, f_da=x.da)
        return 0
    return {"s1_s2": s1_s2, "s3": s3, "s5": s5}[x.cmd]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
