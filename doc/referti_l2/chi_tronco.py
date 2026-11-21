# -*- coding: utf-8 -*-
r"""**IL TRONCO CHI** *(il mandato unico di Luca `2026-11-21` `19:40`, T1; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `14`; la carta intera sul ramo `mitosi-chi`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_tronco.py prova > doc/referti_l2/chi_tronco_prova.txt
    E:\python\py3132\python.exe doc/referti_l2/chi_tronco.py corsa --da ultimo --fino 200000 --registro chi-tronco
    E:\python\py3132\python.exe doc/referti_l2/chi_tronco.py proiezione

**`chi_mattone_v2.py` e' IN USO e non si tocca:** `corsa` qui e' la sua riga per riga, **in piu' dopo ogni tick `scattati = |theta_a| >= QUANTO`** *(`QUANTO = 2 pi`, il valore di `contatore.QUANTO` del ramo `mitosi`)*: al primo tick con un arco scattato **lo stato DOPO il tick, PRIMA di qualunque regola** *(`prima_nascita_<k>.npz` + `.sha1`, `scatto.json`)* e **l'uscita `SCATTO = 10`**.
**`--da ultimo`:** l'ultimo stato integro di `DIR_T`; se non ce n'e', `stato_20000` della corsa *(`chi_mattone_v2.DIR`)*. **Al limite senza scatto:** l'uscita `0`.
**`proiezione`:** dai due ultimi stati integri del tronco *(o della corsa)*: per arco la velocita' di `Theta` *(la differenza sui tick)*, il tick in cui `|Theta|` arriva a `2 pi`; il minimo e l'arco.
**`prova`** *(sez. `14.3`)*: DEVE la ripresa `2750 -> 3000` al bit con `stato_03000`; DEVE lo scatto forzato a `k 2761` *(l'uscita `10`, `scatto.json`, lo stato = quello senza forzatura salvo `theta_a` dell'arco)*; DEVE FALLIRE senza forzatura nessuna uscita `10` fino a `k 2770`.
"""
import argparse
import glob
import json
import math
import os
import shutil
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT
import chi_mattone as CM

DIR_M = CM.DIR
DIR_T = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "tronco")
DIR_PROVA = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "prova_tronco")
CHIAVI_P = ("kappa", "c0", "c2", "m2", "e0", "s")
QUANTO = 2.0 * math.pi
SCATTO = 10
K_PARTENZA = 20000


def stati(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, "stato_*.npz"))):
        k = int(os.path.basename(f)[6:11]) if len(os.path.basename(f)) == 15 else int(os.path.basename(f)[6:-4])
        ok = os.path.exists(f + ".sha1") and open(f + ".sha1", encoding="utf-8").read().split()[0] == CM.sha1(f)
        out.append((k, f, ok))
    return sorted(out)


def ultimo(d):
    for k, f, ok in reversed(stati(d)):
        if ok:
            return k, f
        print("### lo stato %s NON e' integro: si prende quello prima" % os.path.basename(f))
    return None


def nome_stato(d, k):
    return os.path.join(d, "stato_%06d.npz" % k if k >= 100000 else "stato_%05d.npz" % k)


def corsa(f_da, k_fino, reg, d_out, forza=None, scatta=True):
    """### dallo stato `f_da` *(le serie accanto, `serie_<k>`, `serie_chi_<k>`)* fino a `k_fino`; `(codice, k, fine)`; `forza = (k, arco)`: SOLO nella prova."""
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(os.path.join(_QUI, "chi_mattone.py"))
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
    d_in = os.path.dirname(f_da)
    codice = 0
    print("=" * 140)
    print("IL TRONCO CHI (Luca 2026-11-21 19:40, T1; il task history del ramo lapse-u, sez. 14): da %s fino a k %d%s; gli stati in %s" % (
        f_da, k_fino, " ### lo scatto FORZATO a k %d sull'arco %d (SOLO nella prova)" % forza if forza else "", d_out))
    print("=" * 140)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        Lp = CT.Laplaciano(mot)
        s = float(Z["s"])
        C0 = PS.PO.campi(Z, rho_c, e)
        e0 = float(C0.e0)
        P, m0, a, _c = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "C2")
        C, meta, cs, sh = CSB.riprendi(Z, f_da, False, rho_c, e)
        assert cs is None, "lo stato ha un cs_prec: non e' della corsa con chi"
        k_da = int(meta["k"])
        pm = meta["parametri"]
        for q in CHIAVI_P:
            assert getattr(P, q) == pm[q], "il parametro %s ricalcolato %r contro %r nel meta: FERMO" % (q, getattr(P, q), pm[q])
        assert m0 == pm["m0"], "m0 ricalcolato %r contro %r nel meta: FERMO" % (m0, pm["m0"])
        with np.load(f_da) as d:
            X = {q: d[q].copy() for q in CT.CHIAVI_CHI}
        print("### la ripresa da %s (k %d, sha1 %s, ricontrollato); i parametri ricalcolati AL BIT con quelli del meta: %r; m0 %+.12e; max |Theta| %.6f" % (
            f_da, k_da, sh[:8], P, m0, float(np.max(np.abs(X["theta_a"])))))
        sys.stdout.flush()
        M = CSB.Misure(Z, meta["centro"])
        sfx = os.path.basename(f_da)[6:-4]
        with np.load(os.path.join(d_in, "serie_%s.npz" % sfx)) as d:
            M.S = {x: list(d[x]) for x in d.files}
        with np.load(os.path.join(d_in, "serie_chi_%s.npz" % sfx)) as d:
            EX = {x: list(d[x]) for x in d.files}
        assert M.S["k"][-1] == k_da and EX["k"][-1] == k_da
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
                CT.tick_chi(Z_["z"], C_.campo, P, Lp, X)
                totp = float(np.sum(CTO.CO.conti_nodo(Z_)["tot"]))
                self.registra(k, totp, self.kv(), float(np.sum(np.abs(Z_["st"]["psi_h"]) ** 2)))

        def misura_chi(k):
            rh = MT.rho_di(Z)
            H, Hc = CT.energia_chi(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
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

        def salva(k, fz, scatto=False):
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k, tronco_scatto=scatto))), **dati)
            h = CM.sha1(fz)
            with open(fz + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            if not scatto:
                sx = os.path.basename(fz)[6:-4]
                M.salva(os.path.join(d_out, "serie_%s.npz" % sx))
                np.savez(os.path.join(d_out, "serie_chi_%s.npz" % sx), **{q: np.array(v_) for q, v_ in EX.items()})
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
                if forza is not None and k == forza[0]:
                    th = float(X["theta_a"][forza[1]])
                    X["theta_a"][forza[1]] = th + QUANTO * (1.0 if th >= 0.0 else -1.0)      # ### SOLO nella prova: lo scatto forzato
                if scatta:
                    sc = np.nonzero(np.abs(X["theta_a"]) >= QUANTO)[0]
                    if sc.size:
                        fp = os.path.join(d_out, "prima_nascita_%06d.npz" % k)
                        h = salva(k, fp, scatto=True)
                        with open(os.path.join(d_out, "scatto.json"), "w", encoding="utf-8") as fh:
                            json.dump({"k": k, "file": fp, "sha1": h, "archi": [int(x) for x in sc[:20]], "quanti": int(sc.size),
                                       "theta": [float(X["theta_a"][x]) for x in sc[:20]]}, fh)
                        print("### IL PRIMO SCATTO a k %d (%d archi, il primo %d, Theta %+.6f): lo stato PRIMA della regola %s sha1 %s; il tronco esce (%d)" % (
                            k, sc.size, int(sc[0]), float(X["theta_a"][sc[0]]), os.path.basename(fp), h[:8], SCATTO))
                        sys.stdout.flush()
                        if reg:
                            RC.tappa(reg, "IL PRIMO SCATTO a k %d: %s sha1 %s" % (k, os.path.basename(fp), h[:8]))
                        codice = SCATTO
                        break
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            if k > k_da and k % CTO.OGNI == 0:
                RC_.etichette([c])
                meta["lab"] = [float(x) for x in c]
            if k % PS.OGNI == 0:
                R5, _rr, _b = PS.r5(Z, t0 + k)
                rg = MR.raggio(Z, rho, c)
            if k % PS.OGNI_MAPPA == 0:
                PS.PO.dphi_nodi(Z, t0 + k)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k > k_da and k % CM.OGNI == 0:
                M.misura(k, RC_, R5, rg)
                misura_chi(k)
            if k > k_da and k % 250 == 0:
                S = M.S
                print("    k %6d  la massa %.12e  l'energia %+.10e  il raggio %.4f  Min12.4 %.6e  il picco %.4e  H %+.10e  H_chi %+.4e  1-N centro %.4e  max|Theta| %.4f  (%.0f s)" % (
                    k, S["M"][-1], S["E"][-1], S["raggio"][-1], S["Min_12.4"][-1], EX["picco"][-1], EX["H"][-1], EX["H_chi"][-1], EX["uN_0"][-1], EX["max_theta"][-1], time.time() - t00))
                sys.stdout.flush()
            if k > k_da and k % CM.OGNI_STATO == 0:
                h = salva(k, nome_stato(d_out, k))
                print("    [stato] k %d sha1 %s" % (k, h[:8]))
            adesso = time.time()
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                RC.tappa(reg, "k %d; %.3f s per tick; max |Theta| %.4f; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), float(np.max(np.abs(X["theta_a"]))), MT.memoria_gb()))
                t_tappa = adesso
        fine = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy(), CT.copia_X(X))
        Z["metti"]()
    print("-" * 140)
    print("### il tronco: %d tick in %.0f s (%.3f s per tick); il codice %d" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), codice))
    print("=" * 140)
    return codice, k, fine


def diversi(st, A, E, X, f, salvo_arco=None):
    out = []
    with np.load(f) as d:
        for x in st:
            if not np.array_equal(st[x], d[x]):
                out.append(x)
        for x, v in (("campo_A", A), ("campo_E", E)):
            if not np.array_equal(v, d[x]):
                out.append(x)
        for q in CT.CHIAVI_CHI:
            p, w = X[q], d[q]
            if q == "theta_a" and salvo_arco is not None:
                tieni = np.ones(p.size, dtype=bool)
                tieni[salvo_arco] = False
                p, w = p[tieni], w[tieni]
            if not np.array_equal(p, w):
                out.append(q)
    return out


def prova():
    K0, K1, KF, KS = 2750, 3000, 2761, 2770      # ### KF dispari: nessuna delle operazioni periodiche dopo il tick
    esiti = []
    if os.path.isdir(DIR_PROVA):
        shutil.rmtree(DIR_PROVA)
    f0 = os.path.join(DIR_M, "stato_%05d.npz" % K0)
    # ### 1. la ripresa al bit
    cod, k, (st, A, E, X) = corsa(f0, K1, None, os.path.join(DIR_PROVA, "ripresa"), scatta=True)
    dd = diversi(st, A, E, X, os.path.join(DIR_M, "stato_%05d.npz" % K1))
    print("### LA RIPRESA (k %d -> %d, con il controllo dello scatto acceso) contro stato_%05d: %s; il codice %d" % (K0, K1, K1, "AL BIT" if not dd else "### DIVERSE: %s" % dd, cod))
    esiti.append(("la ripresa da k %d a k %d AL BIT con la corsa, nessuno scatto" % (K0, K1), not dd and cod == 0 and k == K1))
    # ### 2. lo scatto forzato
    with np.load(f0) as d:
        th = d["theta_a"].copy()
    arco = int(np.argmax(np.abs(th)))
    dS = os.path.join(DIR_PROVA, "scatto")
    cod, k, _f = corsa(f0, KS, None, dS, forza=(KF, arco))
    with open(os.path.join(dS, "scatto.json"), encoding="utf-8") as fh:
        sj = json.load(fh)
    _c, _k, (st2, A2, E2, X2) = corsa(f0, KF, None, os.path.join(DIR_PROVA, "senza_fino_%d" % KF), scatta=True)
    dd = diversi(st2, A2, E2, X2, sj["file"], salvo_arco=arco)
    with np.load(sj["file"]) as d:
        th_s = float(d["theta_a"][arco])
    print("### LO SCATTO FORZATO (l'arco %d, il Theta piu' grande a k %d, a k %d): il codice %d a k %d; scatto.json %s; lo stato salvato contro la corsa senza forzatura a k %d: %s; Theta dell'arco %+.6f contro %+.6f" % (
        arco, K0, KF, cod, k, json.dumps({x: sj[x] for x in ("k", "archi", "quanti")}), KF, "AL BIT salvo theta_a dell'arco" if not dd else "### DIVERSE: %s" % dd, th_s, float(X2["theta_a"][arco])))
    esiti.append(("lo scatto forzato: l'uscita 10 al tick forzato, scatto.json con l'arco, lo stato AL BIT salvo l'arco", cod == SCATTO and k == KF and sj["k"] == KF and sj["archi"] == [arco] and not dd))
    # ### 3. DEVE FALLIRE: senza forzatura nessuno scatto
    cod, k, _f = corsa(f0, KS, None, os.path.join(DIR_PROVA, "senza"))
    print("### DEVE FALLIRE: senza la forzatura, fino a k %d: il codice %d a k %d -> %s" % (KS, cod, k, "nessuno scatto, come deve" if cod == 0 and k == KS else "### UNO SCATTO"))
    esiti.append(("DEVE FALLIRE: senza la forzatura nessuna uscita 10 fino a k %d" % KS, cod == 0 and k == KS))
    print("-" * 140)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 140)
    return 0 if all(ok for _n, ok in esiti) else 1


def proiezione():
    import _presidio
    _presidio.avvia(__file__)
    S_ = [x for x in stati(DIR_T) if x[2]] or [x for x in stati(DIR_M) if x[2]]
    assert len(S_) >= 2, "servono due stati integri"
    (k1, f1, _a), (k2, f2, _b) = S_[-2], S_[-1]
    with np.load(f1) as d:
        t1 = d["theta_a"].copy()
    with np.load(f2) as d:
        t2 = d["theta_a"].copy()
    v = (t2 - t1) / float(k2 - k1)
    resto = QUANTO - np.abs(t2)
    vv = np.where(np.sign(v) == np.sign(t2), np.abs(v), 0.0)
    T = np.where(vv > 0.0, resto / np.where(vv > 0.0, vv, 1.0), np.inf)
    a = int(np.argmin(T))
    print("### LA PROIEZIONE LINEARE dagli stati k %d e k %d (%s, %s): l'arco %d, |Theta| %.6f, la velocita' %.4e per tick -> il primo scatto a k %.0f" % (
        k1, k2, os.path.basename(f1), os.path.basename(f2), a, abs(float(t2[a])), float(vv[a]), k2 + float(T[a])))
    return 0


def attendi(winpid):
    """### aspetta l'uscita del processo Windows `winpid` *(la funzione di `mitosi_attendi.attendi` del ramo `mitosi`, riga per riga)*."""
    import ctypes
    SYNCHRONIZE, INFINITE = 0x00100000, 0xFFFFFFFF
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.OpenProcess.restype = ctypes.c_void_p
    h = k32.OpenProcess(SYNCHRONIZE, False, int(winpid))
    if not h:
        print("### il processo %s non si apre (errore %d): gia' uscito, o non c'e'" % (winpid, ctypes.get_last_error()))
        return 1
    print("### aspetto il processo %s dalle %s" % (winpid, time.strftime("%Y-%m-%d %H:%M:%S")))
    sys.stdout.flush()
    r = k32.WaitForSingleObject(ctypes.c_void_p(h), INFINITE)
    k32.CloseHandle(ctypes.c_void_p(h))
    print("### il processo %s e' uscito alle %s (WaitForSingleObject %d)" % (winpid, time.strftime("%Y-%m-%d %H:%M:%S"), r))
    return 0


def decidi():
    """### dai FILE: `TRONCO` *(uscita 20)* se la voce `chi-mattone-lungo` non e' aperta e `stato_20000` e' integro; altrimenti `NIENTE` *(uscita 0)*."""
    from solitone import _registro_corse as RC
    f = os.path.join(DIR_M, "stato_%05d.npz" % K_PARTENZA)
    integro = os.path.exists(f + ".sha1") and open(f + ".sha1", encoding="utf-8").read().split()[0] == CM.sha1(f)
    aperta = "chi-mattone-lungo" in RC.aperte()
    print("TRONCO" if integro and not aperta else "NIENTE (stato_%05d integro %s; la voce chi-mattone-lungo aperta %s)" % (K_PARTENZA, integro, aperta))
    return 20 if integro and not aperta else 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--da", choices=("ultimo",), required=True)
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--registro")
    sub.add_parser("prova")
    sub.add_parser("proiezione")
    sub.add_parser("decidi")
    w = sub.add_parser("attendi")
    w.add_argument("winpid", type=int)
    x = ap.parse_args(argv)
    if x.cmd == "attendi":
        return attendi(x.winpid)
    if x.cmd == "decidi":
        return decidi()
    if x.cmd == "prova":
        return prova()
    if x.cmd == "proiezione":
        return proiezione()
    u = ultimo(DIR_T)
    if u is None:
        f = os.path.join(DIR_M, "stato_%05d.npz" % K_PARTENZA)
        assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CM.sha1(f), "stato_%05d della corsa NON e' integro" % K_PARTENZA
    else:
        f = u[1]
        if x.registro:
            from solitone import _registro_corse as RC
            RC.tappa(x.registro, "RIPRESA del tronco chi da k %d, %s sha1 %s" % (u[0], os.path.basename(f), CM.sha1(f)[:8]))
    cod, _k, _f = corsa(f, x.fino, x.registro, DIR_T)
    return cod


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
