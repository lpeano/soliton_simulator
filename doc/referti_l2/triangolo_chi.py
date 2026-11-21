# -*- coding: utf-8 -*-
r"""**IL TRIANGOLO CON `chi`: LE TRE SFASATE SUL VUOTO E IL GEMELLO RUOTATO** *(il mandato di Luca `2026-11-21` `23:23`; la carta `doc/TASK_HISTORY/2026-11-21_triangolo_chi.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi.py compat > doc/referti_l2/triangolo_chi_compat.txt
    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi.py costo > doc/referti_l2/triangolo_chi_costo.txt
    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi.py prova > doc/referti_l2/triangolo_chi_prova.txt
    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi.py tronco --quale t120 --fino 200000 --registro <voce>

**La scena** *(`mattone_triangolo.corsa` riga per riga fino al tick `0`, coi ganci di `triangolo_120` e di `triangolo_ruotato`: i file NON si toccano)*: la scena di S162 *(`mattone.scena(CORSA_162, T_162)`)*, **NIENTE bordo sorbente** *(Luca: `g_e = 0`)*, il vuoto fresco, **tre francobolli del mattone di `L 162`** *(`triangolo_video.francobollo_L162`)* ai vertici equilateri *(`triangolo_120.vertici`; il ruotato `triangolo_ruotato.vertici_ruotati`, `+15` gradi)*, `psi_h` per `exp(i 0, 120, 240 gradi)`, la materia per SOMMA, il vuoto per PRODOTTO; il campo `porto.campi` *(`A = 0`, `E` da Gauss)*.
**`chi`:** `chi_tick_v2` *(l'inerzia `f`, `kappa` il NUMERO)*; `m0` dallo stato di partenza del triangolo *(la regola del mattone)*; `chi` al profilo statico, `pi = 0`, `Theta = 0`. **Il tronco:** dopo ogni tick `scattati = |theta_a| >= 2 pi`: lo stato PRIMA della regola, `scatto.json`, l'uscita `10`; gli stati ogni `250`.
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
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402
import chi_mattone as CM  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "triangolo")
QUALI = ("t120", "t120r")
FASI = (0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0)
QUANTO, SCATTO = 2.0 * math.pi, 10
OGNI, OGNI_STATO = 50, 250
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


def moduli():
    import mattone as MT
    import mattone_triangolo as MTR
    import triangolo_120 as T1
    import triangolo_ruotato as TRU
    import triangolo_video as TV
    import porto as PO
    return MT, MTR, T1, TRU, TV, PO


def prepara(Z, quale):
    """### lo stato del tick `0` *(le righe di `mattone_triangolo.corsa`)*, SENZA bordo; `(C, info)`."""
    MT, MTR, T1, TRU, TV, PO = moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    c0 = Z["bordo"]["c0"]
    fr = TV.francobollo_L162(0)
    V = T1.vertici(c0, fr, L) if quale == "t120" else TRU.vertici_ruotati(c0, fr, L)
    centri = [list(v) for v in V]
    Z["g_e"] = np.zeros_like(Z["g_e"])                                 # ### Luca: NIENTE bordo sorbente
    MT.vuoto_fresco(Z, t0)
    vuoto_psi = float(np.max(np.abs(st["psi_h"])))
    phi_F3 = st["phi_h"].copy()
    vuoto = {x: st[x].copy() for x in Z["chiavi"]}
    soli = []
    for j, c in enumerate(centri):
        for x in Z["chiavi"]:
            st[x][...] = vuoto[x]
        MT.incolla(Z, fr, c, True)
        if FASI[j] != 0.0:
            st["psi_h"][...] = st["psi_h"] * np.exp(1j * FASI[j])
        soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
    psi = soli[0][0].copy()
    phi = soli[0][1].copy()
    for s_ in soli[1:]:
        psi = psi + s_[0]
        phi = phi * (s_[1] / phi_F3)
    st["psi_h"][...] = psi
    st["phi_h"][...] = phi
    C = PO.campi(Z, rho_c, e)
    lati = [MT.distanza(L, centri[a], centri[b]) for a, b in ((0, 1), (1, 2), (2, 0))]
    return C, {"quale": quale, "centri": centri, "lati": lati, "vuoto_psi": vuoto_psi, "masse_soli": [float(np.sum(np.abs(s_[0]) ** 2)) for s_ in soli],
               "francobollo": fr.get("file", "L162_MGU_03000"), "c0": list(c0)}


def scena():
    MT = moduli()[0]
    return MT.scena(MT.CORSA_162, MT.T_162)


def compat():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(__file__)
    MT, MTR, T1, TRU, TV, PO = moduli()
    print("=" * 130)
    print("P0, LA COMPATIBILITA' DEL TRIANGOLO CON CHI (Luca 2026-11-21 23:23): sola lettura, nessun tick")
    print("=" * 130)
    for quale in QUALI:
        with scena() as Z:
            print("### %s: la scena %s (T %d): L %d, n %d, m %d; s %r; rho_c %r, e %r; la forma %s; il bordo della scena R_A %.3f, c0 %s; il bordo nelle corse con chi: NESSUNO (g_e = 0)" % (
                quale, MT.CORSA_162, MT.T_162, Z["L"], Z["mot"].inc.n, Z["mot"].inc.m, float(Z["s"]), MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.PB.FORMA, Z["bordo"]["R_A"], Z["bordo"]["c0"]))
            C, info = prepara(Z, quale)
            print("    i vertici %s; i lati %s; il vuoto senza materia prima dell'incollatura %s (max |psi_h| %.1e); le masse dei francobolli da soli %s" % (
                info["centri"], ["%.4f" % x for x in info["lati"]], info["vuoto_psi"] == 0.0, info["vuoto_psi"], ["%.12e" % x for x in info["masse_soli"]]))
            s_a = np.asarray(C.campo.s_a)
            print("    il campo U(1): s_a uniforme %s, %r; w %r; il Laplaciano di chi sul grafo della scena (n %d)" % (bool(np.all(s_a == s_a[0])), float(s_a[0]), float(C.campo.w[0]), Z["mot"].inc.n))
            P, m0 = CV2.parametri_v2(Z, None, None, MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0, float(Z["s"]), float(C.e0), stato={x: Z["st"][x] for x in Z["chiavi"]})
            print("    i parametri di chi (v2): %r; m0 dello stato di partenza %+.12e" % (P, m0))
            Z["metti"]()
    print("=" * 130)
    return 0


def corsa(quale, k_fino, reg, d_out, f_da=None, scatta=True, v1=False, energia_ogni=None):
    """### il tick con `chi` sul triangolo, da `k 0` *(prepara)* o da `f_da`. `(codice, k, fine, serie_H)`."""
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(__file__)
    MT, MTR, T1, TRU, TV, PO = moduli()
    from solitone import _registro_corse as RC
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    os.makedirs(d_out, exist_ok=True)
    codice, serie_H = 0, []
    t00 = time.time()
    with scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)
        if f_da is None:
            C, info = prepara(Z, quale)
            P, m0 = CV2.parametri_v2(Z, None, None, rho_c, e, t0, s, float(C.e0), stato={x: Z["st"][x].copy() for x in Z["chiavi"]})
            Z["g_e"] = np.zeros_like(Z["g_e"])                         # ### NIENTE bordo, anche dopo metti
            X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0))
            meta = dict(info, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f})
            k_da = 0
            EX = {x: [] for x in ("k", "M", "H", "H_chi", "chi_medio", "max_theta", "picco")}
        else:
            assert open(f_da + ".sha1", encoding="utf-8").read().split()[0] == CM.sha1(f_da), "lo sha1 di %s NON coincide: la ripresa RIFIUTA" % f_da
            with np.load(f_da) as d:
                Xf = {x: d[x].copy() for x in d.files}
            meta = json.loads(str(Xf.pop("meta")))
            Z["metti"]({x: Xf[x] for x in Z["chiavi"]})
            Z["g_e"] = np.zeros_like(Z["g_e"])
            C = PO.campi(Z, rho_c, e, Xf["campo_A"], Xf["campo_E"])
            pm = meta["parametri"]
            P = CV2.Parametri2(pm["kappa"], pm["c0"], pm["s"], pm["e0"], pm["f"], pm["c2"], pm["m2"])
            m0 = pm["m0"]
            X = {q: Xf[q] for q in CT.CHIAVI_CHI}
            k_da = int(meta["k"])
            sfx = os.path.basename(f_da)[6:-4]
            with np.load(os.path.join(os.path.dirname(f_da), "serie_%s.npz" % sfx)) as d:
                EX = {x: list(d[x]) for x in d.files}
        if v1:
            P = CT.Parametri(P.kappa, P.c0, P.s, P.e0, P.c2, P.m2)
        tick = CT.tick_chi if v1 else CV2.tick_chi_v2
        energia = CT.energia_chi if v1 else CV2.energia_chi_v2
        print("### IL TRIANGOLO %s CON CHI (%s): da %s fino a k %d; i parametri %r; m0 %+.12e; gli stati in %s" % (
            quale, "il passo di OGGI" if v1 else "il passo v2", os.path.basename(f_da) if f_da else "k 0 (prepara)", k_fino, P, m0, d_out))
        sys.stdout.flush()

        def salva(k, fz, scatto=False):
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k, tronco_scatto=scatto))), **dati)
            h = CM.sha1(fz)
            with open(fz + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            if not scatto:
                np.savez(os.path.join(d_out, "serie_%s.npz" % os.path.basename(fz)[6:-4]), **{q: np.array(v_) for q, v_ in EX.items()})
            return h

        def misura(k):
            H, Hc = energia(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
            rh = CT.rho_di(mot, Z["st"])
            for x, v_ in (("k", k), ("M", float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2))), ("H", H), ("H_chi", Hc), ("chi_medio", float(X["chi"].mean())),
                          ("max_theta", float(np.max(np.abs(X["theta_a"])))), ("picco", float(rh.max()))):
                EX[x].append(v_)
            return H

        t1 = t_tappa = time.time()
        k = k_da
        if f_da is None:
            misura(0)
        for k in range(k_da + 1, k_fino + 1):
            tick(Z["z"], C.campo, P, Lp, X)
            if scatta:
                sc = np.nonzero(np.abs(X["theta_a"]) >= QUANTO)[0]
                if sc.size:
                    fp = os.path.join(d_out, "prima_nascita_%06d.npz" % k)
                    h = salva(k, fp, scatto=True)
                    with open(os.path.join(d_out, "scatto.json"), "w", encoding="utf-8") as fh:
                        json.dump({"k": k, "file": fp, "sha1": h, "archi": [int(x) for x in sc[:20]], "quanti": int(sc.size)}, fh)
                    print("### IL PRIMO SCATTO a k %d (%d archi, il primo %d): %s sha1 %s; il tronco esce (%d)" % (k, sc.size, int(sc[0]), os.path.basename(fp), h[:8], SCATTO))
                    if reg:
                        RC.tappa(reg, "IL PRIMO SCATTO a k %d: %s sha1 %s" % (k, os.path.basename(fp), h[:8]))
                    codice = SCATTO
                    break
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % OGNI == 0:
                H = misura(k)
                if k % 250 == 0:
                    print("    k %6d  la massa %.12e  H %+.12e  H_chi %+.4e  max|Theta| %.4f  il picco %.4e  (%.0f s)" % (k, EX["M"][-1], H, EX["H_chi"][-1], EX["max_theta"][-1], EX["picco"][-1], time.time() - t00))
                    sys.stdout.flush()
            if energia_ogni and k % energia_ogni == 0:
                serie_H.append((k, energia(mot, Z["st"], Z["par"], P, Lp, X, C.campo)[0]))
            if k % OGNI_STATO == 0 or k == k_fino:
                hh = salva(k, os.path.join(d_out, "stato_%06d.npz" % k))
                if k % OGNI_STATO == 0:
                    print("    [stato] k %d sha1 %s" % (k, hh[:8]))
            adesso = time.time()
            if reg and adesso - t_tappa >= 3600.0:
                RC.tappa(reg, "k %d; %.3f s per tick; max |Theta| %.4f" % (k, (adesso - t1) / max(1, k - k_da), float(np.max(np.abs(X["theta_a"])))))
                t_tappa = adesso
        fin = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy(), CT.copia_X(X))
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick); il codice %d" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), codice))
    return codice, k, fin, serie_H


def costo():
    print("=" * 130)
    print("P1, IL COSTO DEL TICK CON CHI SUL TRIANGOLO (Luca 2026-11-21 23:23): 50 tick per scena")
    print("=" * 130)
    for quale in QUALI:
        corsa(quale, 50, None, os.path.join(BASE, "costo", quale), scatta=False)
    return 0


def uguali(a, b):
    st1, A1, E1, X1 = a
    st2, A2, E2, X2 = b
    return [x for x in st1 if not np.array_equal(st1[x], st2[x])] + [x for x, p, q in (("A", A1, A2), ("E", E1, E2)) if not np.array_equal(p, q)] + [q for q in CT.CHIAVI_CHI if not np.array_equal(X1[q], X2[q])]


def prova():
    print("=" * 130)
    print("P2, LA PROVA BREVE DEL TRIANGOLO CON CHI (Luca 2026-11-21 23:23): 250 tick di fila contro 125 + salva + riprendi + 125; un byte; l'energia")
    print("=" * 130)
    for quale in QUALI:
        d = os.path.join(BASE, "prova", quale)
        if os.path.isdir(d):
            shutil.rmtree(d)
        _c, _k, fila, H2 = corsa(quale, 250, None, os.path.join(d, "fila"), energia_ogni=50)
        corsa(quale, 125, None, os.path.join(d, "spezza"))
        fm = os.path.join(d, "spezza", "stato_000125.npz")
        _c, _k, rip, _h = corsa(quale, 250, None, os.path.join(d, "spezza"), f_da=fm)
        dd = uguali(fila, rip)
        print("### %s: 250 tick di fila contro la ripresa da %s: %s" % (quale, os.path.basename(fm), "AL BIT (psi, phi, A, E, chi, pi, Theta)" if not dd else "### DIVERSE: %s" % dd))
        esito("P2 %s: la ripresa AL BIT su ogni chiave" % quale, not dd)
        fr = os.path.join(d, "rotto", "stato_000125.npz")
        os.makedirs(os.path.dirname(fr), exist_ok=True)
        for x in ("stato_000125.npz", "stato_000125.npz.sha1", "serie_000125.npz"):
            shutil.copyfile(os.path.join(d, "spezza", x), os.path.join(d, "rotto", x))
        with open(fr, "r+b") as fh:
            fh.seek(os.path.getsize(fr) // 2)
            b = fh.read(1)
            fh.seek(os.path.getsize(fr) // 2)
            fh.write(bytes([b[0] ^ 0x01]))
        rif = False
        try:
            corsa(quale, 126, None, os.path.join(d, "rotto"), f_da=fr)
        except AssertionError as ex:
            rif = "sha1" in str(ex)
            print("### %s: un byte cambiato: %s" % (quale, ex))
        esito("P2 %s DEVE FALLIRE: un byte cambiato -> la ripresa RIFIUTA" % quale, rif)
        _c, _k, _f, H1 = corsa(quale, 250, None, os.path.join(d, "oggi"), v1=True, energia_ogni=50)
        h2, h1 = np.array([h for _k, h in H2]), np.array([h for _k, h in H1])
        d2 = float(np.max(np.abs(h2 - h2[0]))) / abs(h2[0])
        d1 = float(np.max(np.abs(h1 - h1[0]))) / abs(h1[0])
        print("### %s: la deriva relativa massima di H in 250 tick: il passo v2 %.3e, il passo di oggi %.3e" % (quale, d2, d1))
        esito("P2 %s: l'energia con chi v2 entro 10 volte la deriva del passo di oggi + 1e-12 (il criterio di K5)" % quale, d2 <= 10.0 * d1 + 1e-12, "%.2e" % d2)
    return fine()


def tronco(quale, k_fino, reg):
    d = os.path.join(BASE, quale)
    fs = sorted((f for f in glob.glob(os.path.join(d, "stato_*.npz")) if os.path.exists(f + ".sha1")), key=lambda f: int(os.path.basename(f)[6:-4]))
    f_da = fs[-1] if fs else None
    cod, _k, _f, _h = corsa(quale, k_fino, reg, d, f_da=f_da)
    return cod


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for x in ("compat", "costo", "prova"):
        sub.add_parser(x)
    t = sub.add_parser("tronco")
    t.add_argument("--quale", choices=QUALI, required=True)
    t.add_argument("--fino", type=int, required=True)
    t.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd == "tronco":
        return tronco(x.quale, x.fino, x.registro)
    return {"compat": compat, "costo": costo, "prova": prova}[x.cmd]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
