# -*- coding: utf-8 -*-
r"""**[M0149] LA SUITE v3: LE COPPIE COL CONTROLLO GIUSTO DELLA TRASLAZIONE** *(la v2 `fondo_suite_v2.py` c0abc3e6 falli' sul suo assert: l'uguaglianza AL BIT di due `bincount` sommati in ordine diverso, a0424002; qui `rho` traslata contro `rho` spostata entro `1e-12` relativo, stampato; il resto la v2 riga per riga)*. **IL TITOLO DELLA v2: LA FASE CON FH/FT E m* DI F0 LUNGO LA TENUTA** *(la carta `doc/CARTA_torneo_nonlinearita.md`, sez. 14; `fondo_suite.py` resta com'e')*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_suite_v2.py calcio --sorgente FH --kstato 1500 --k 0.010      (sorgente F0, FH, FT; kstato 0, 500, 1000, 1500, 3000; k 0 o 0.010, asse 1)
    E:\python\py3132\python.exe doc/referti_l2/fondo_suite_v2.py coppia --sorgente FH --gradi 180                  (2000 tick, d 35)
    E:\python\py3132\python.exe doc/referti_l2/fondo_suite_v2.py caduta --sorgente FH                              (V2, 2000 tick)
    E:\python\py3132\python.exe doc/referti_l2/fondo_suite_v2.py lettura > doc/referti_l2/fondo_suite_v2.txt

**La partenza:** lo stato a `k kstato` della tenuta `tenuta/<forma>_cima` *(F0 = S1)*, col campo `A`, `E` dal file *(`fondo_suite.carica` riga per riga, la sorgente generalizzata)*, la forma coi `pezzi` del NUCLEO dentro la scena. **`calcio`:** le righe di `fondo_suite.calcio` *(`1000` tick, il baricentro ogni `10`)* **piu' `omega` per tick** *(`-arg vdot(psi(k-1), psi(k))`)*. **`coppia`** *(la carta sez. 14)*: la seconda copia = lo stato TRASLATO di `35` nodi lungo `A1` *(la permutazione dei semiarchi `(a, b) -> (a + 35 A1, b + 35 A1)`, coi due capi d'arco; il controllo: `rho` traslata = `rho` spostata, al bit)* per `e^{i delta}`; `psi = psi1 + psi2`, `phi = phi1 phi2 / phi_vuoto` *(`phi_vuoto = c(t0 + kstato) phi_v`)*; **il campo da Gauss** *(`PO.campi`)*; il tick V0, `2000` tick; ogni `10` tick `D` fra i baricentri delle due meta' *(il piano a meta' strada, ortogonale ad `A1`)*; **a ogni tick `omega` di ciascun corpo** *(`-arg` della sovrapposizione fra tick sui nodi entro `r 15` dal suo baricentro a `k 0`)*. **`caduta`:** V2 *(`chi` acceso, `cs = s N`, senza la fase (a); `caduta_libera.campo_N` con `y_c` dal baricentro dello stato e `A` di `caduta_libera.corsa`)*, `2000` tick, il baricentro ogni `10`. **`lettura`:** m* e `omega` di F0 lungo la tenuta; m* di FH, FT, F0 *(`k/(v - v0)` e `k/v`)*; `a` delle coppie, `A`, `B`, il Pound-Rebka *(`omega` del corpo meno quello del corpo isolato, media su `[500, 2000]`)*; la caduta *(`a_y` dal fit quadratico meno quello della corsa a `k 0` della stessa sorgente; in unita' di `c^2 |dN/dy|`, `|dN/dy| = G20` allo zero; c_banda `0.5664 s`, c_sol `0.588 s`; VERSO se `a_y > 0`, verso `N` piu' basso)*.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import massa_calcio as MC  # noqa: E402
import ripresa_F0_v2 as RF  # noqa: E402
import torneo_tenuta as TT  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0133")          # ### la stessa cartella della v2: la lettura trova i calci isolati (il Pound-Rebka)
FORMA = {"F0": "S1", "FH": "FH", "FT": "FT"}
D_COPPIA, K_COPPIA, K_CADUTA, R_CORPO = 35, 2000, 2000, 15.0
C_BANDA, C_SOL = 0.5664, 0.588
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py", "massa_calcio.py", "ripresa_F0_v2.py", "torneo_tenuta.py", "fondo_suite.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def stato_di(sorgente, kstato):
    return os.path.join(TT.DIR, "%s_cima" % FORMA[sorgente], "stato_%06d.npz" % kstato)


def carica(Z, sorgente, kstato):
    """### `fondo_suite.carica` riga per riga, con la sorgente `(forma, kstato)`: `(C, info, dxy, forma, X)`."""
    import gravita_due_corpi_misure as GM
    import _u1_prototipo as U1
    from solitone import toro as TO
    f, forma = stato_di(sorgente, kstato), FORMA[sorgente]
    X, meta = GM.leggi(f)
    C, _info = CL.prepara(Z)
    Z["metti"]({x: X[x] for x in Z["chiavi"]})
    C.campo.A[...] = X["campo_A"]
    C.campo.E[...] = X["campo_E"]
    U1.scrivi_U(Z["mot"], C.campo)
    nodo = np.asarray(Z["mot"].inc.nodo)
    n, L = Z["n"], Z["L"]
    rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
    i = int(np.argmax(TT.lisciata(rho, L)))
    c = (int(Z["m1"][i]), int(Z["m2"][i]))
    d = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2]
    bari = (d * rho[:, None]).sum(axis=0) / rho.sum()
    info = {"centro": list(c), "bari": bari.tolist(), "y_c": float(c[1] * math.sqrt(3.0) / 2.0 + bari[1]), "massa": float(rho.sum()), "file": f, "k_file": int(meta["k"]), "forma": forma}
    return C, info, d - bari, forma, X


def _tick_loop(Z, C, forma, quanti, dopo, MV, P0, N, cs_N):
    _G20, _ia, e0, MT = CL.parametri()
    s = float(Z["s"])
    with RF.col_nucleo(MV, P0), MV.forma_esplicita(forma):
        assert MV.ATTIVA == forma and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, 0)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


def calcio(sorgente, kstato, k):
    avvia()
    MV, P0 = TT.nucleo()
    nome = "calcio_%s_k%04d_%s" % (sorgente, kstato, MC.nome(k, 1))
    d_out = os.path.join(BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = carica(Z, sorgente, kstato)
        u = MC.asse_u(1)
        if k:
            Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * float(k) * (dxy @ u))[nodo][:, None]
        print("### %s: %s (k %d), la forma %s; il centro %s; l'impronta %s" % (nome, info["file"], info["k_file"], forma, info["centro"], TT.impronta(Z, C)[:12]))
        serie, om = [], []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b @ u), float(b[0]), float(b[1]), float(rho.sum()), float(rho.max())))

        def dopo(kk, prima):
            om.append(float(-np.angle(np.vdot(prima, Z["st"]["psi_h"]))))
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: lungo l'asse %+.5f, omega %+.6f (%.0f s)" % (kk, serie[-1][1], om[-1], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        _tick_loop(Z, C, forma, MC.K_FINO, dopo, MV, P0, np.ones(n), False)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"sorgente": sorgente, "kstato": kstato, "k": k, "serie": serie, "omega": om, "info": info}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (MC.K_FINO, time.time() - t1))
    return 0


def permutazione(Z, passo):
    """### i semiarchi traslati di `passo` nodi lungo `A1`: `perm[h]` = il semiarco immagine di `h`."""
    inc = Z["mot"].inc
    nodo = np.asarray(inc.nodo)
    L = Z["L"]
    m1, m2 = Z["m1"], Z["m2"]
    T = ((m1 + passo) % L) * L + m2
    a, b = nodo[0::2], nodo[1::2]
    chiave = {(int(x), int(y)): j for j, (x, y) in enumerate(zip(a, b))}
    perm = np.empty(len(nodo), dtype=int)
    for j, (x, y) in enumerate(zip(a, b)):
        jj = chiave.get((int(T[x]), int(T[y])))
        verso = 0
        if jj is None:
            jj = chiave[(int(T[y]), int(T[x]))]
            verso = 1
        perm[2 * j] = 2 * jj + verso
        perm[2 * j + 1] = 2 * jj + 1 - verso
    assert np.array_equal(nodo[perm], T[nodo]), "la traslazione dei semiarchi non porta i nodi giusti: FERMO"
    return perm, T


def coppia(sorgente, gradi, kstato=1500):
    from solitone import bordo as BO
    from solitone import toro as TO
    avvia()
    MV, P0 = TT.nucleo()
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    nome = "coppia_%s_k%04d_D%d" % (sorgente, kstato, gradi)
    d_out = os.path.join(BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        _C, info, _dxy, forma, X = carica(Z, sorgente, kstato)
        perm, T = permutazione(Z, D_COPPIA)
        psi1, phi1 = Z["st"]["psi_h"].copy(), Z["st"]["phi_h"].copy()
        psi2, phi2 = np.empty_like(psi1), np.empty_like(phi1)
        psi2[perm] = psi1
        phi2[perm] = phi1
        rho1 = np.bincount(nodo, weights=np.sum(np.abs(psi1) ** 2, axis=1), minlength=n)
        rho2 = np.bincount(nodo, weights=np.sum(np.abs(psi2) ** 2, axis=1), minlength=n)
        r_sp = np.empty_like(rho1)
        r_sp[T] = rho1
        scarto = float(np.max(np.abs(rho2 - r_sp))) / float(np.max(rho1))
        print("### la traslazione: max |rho traslata - rho spostata| / max rho = %.2e (la soglia 1e-12)" % scarto)
        assert scarto <= 1e-12, "rho traslata != rho spostata oltre 1e-12: FERMO"
        phi_v = BO.c_di(MT.G2.T0 + kstato, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
        Z["st"]["psi_h"][...] = psi1 + psi2 * np.exp(1j * math.radians(gradi))
        Z["st"]["phi_h"][...] = phi1 * (phi2 / phi_v)
        C = PO.campi(Z, MT.rho_c_assoluto(), MT.PB.E_DECISO)
        A1 = np.asarray(TO.vettori()[0], float)[:2]
        a1 = A1 / np.hypot(*A1)
        c = info["centro"]
        M = np.array(c, float) + np.array([0.5 * D_COPPIA, 0.0])
        dxy = TO.scarti(Z["m1"], Z["m2"], M[0], M[1], L)[:, :2]
        lato = dxy @ a1
        rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
        b0 = [(dxy[s_] * rho[s_][:, None]).sum(axis=0) / rho[s_].sum() for s_ in (lato < 0.0, lato >= 0.0)]
        reg = [np.hypot(*(dxy - b).T) < R_CORPO for b in b0]
        hreg = [r_[nodo] for r_ in reg]
        print("### %s: la sorgente %s (k %d), la forma %s; d %d lungo A1; delta %d; D a k 0 %.4f; i nodi dei due corpi %d, %d; l'impronta %s" % (
            nome, sorgente, kstato, forma, D_COPPIA, gradi, float(np.hypot(*(b0[1] - b0[0]))), int(reg[0].sum()), int(reg[1].sum()), TT.impronta(Z, C)[:12]))
        Ds, om = [], [[], []]

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = [(dxy[s_] * rho[s_][:, None]).sum(axis=0) / rho[s_].sum() for s_ in (lato < 0.0, lato >= 0.0)]
            Ds.append((kk, float(np.hypot(*(b[1] - b[0])))))

        def dopo(kk, prima):
            for i in (0, 1):
                om[i].append(float(-np.angle(np.vdot(prima[hreg[i]], Z["st"]["psi_h"][hreg[i]]))))
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: D %.4f, omega %+.6f %+.6f (%.0f s)" % (kk, Ds[-1][1], om[0][-1], om[1][-1], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        _tick_loop(Z, C, forma, K_COPPIA, dopo, MV, P0, np.ones(n), False)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"sorgente": sorgente, "kstato": kstato, "gradi": gradi, "D": Ds, "omega": om, "info": info}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_COPPIA, time.time() - t1))
    return 0


def caduta(sorgente, kstato=1500):
    avvia()
    MV, P0 = TT.nucleo()
    G20, _ia, _e0, _MT = CL.parametri()
    import chi_parametri_v2 as CP2
    nome = "caduta_V2_%s_k%04d" % (sorgente, kstato)
    d_out = os.path.join(BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = carica(Z, sorgente, kstato)
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        _chi, N = CL.campo_N(Z, info, A, +1.0)
        s = float(Z["s"])
        print("### %s: %s (k %d), la forma %s; y_c %.6f; A %.6e (G20 %.6e); N da %.10f a %.10f; l'impronta %s" % (nome, info["file"], info["k_file"], forma, info["y_c"], A, G20, float(N.min()), float(N.max()), TT.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b[0]), float(b[1]), float(rho.sum())))

        def dopo(kk, prima):
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: y %+.5f (%.0f s)" % (kk, serie[-1][2], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        _tick_loop(Z, C, forma, K_CADUTA, dopo, MV, P0, N, True)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"sorgente": sorgente, "kstato": kstato, "serie": serie, "info": info, "G20": G20, "A": A}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_CADUTA, time.time() - t1))
    return 0


def _leggi(nome):
    f = os.path.join(BASE, nome, "serie.json")
    if not os.path.exists(f + ".sha1"):
        return None
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f)
    return json.load(open(f, encoding="utf-8"))


def lettura():
    import gravita_due_corpi_misure as GM
    avvia()
    print("=" * 130)
    print("[M0133] LA SUITE v2 (la carta sez. 14)")
    print("=" * 130)
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()

    def m_star(sorgente, kstato):
        r0 = _leggi("calcio_%s_k%04d_%s" % (sorgente, kstato, MC.nome(0.0, 1)))
        r1 = _leggi("calcio_%s_k%04d_%s" % (sorgente, kstato, MC.nome(0.010, 1)))
        if r0 is None or r1 is None:
            return None
        v0, s0, _ = MC.velocita(r0["serie"])
        v1, s1, _ = MC.velocita(r1["serie"])
        om0 = float(np.mean(r0["omega"]))
        return v0, s0, v1, s1, 0.010 / v1, 0.010 / (v1 - v0), math.hypot(s1, s0), om0, r0["omega"]
    print("  (1) m* E omega DI F0 LUNGO LA TENUTA (il calcio k 0.010 asse 1 e k 0 dagli stati salvati)")
    for ks in (0, 500, 1000, 1500, 3000):
        r = m_star("F0", ks)
        if r is None:
            print("    k %4d: non c'e' ancora" % ks)
            continue
        w, p, _mx, _M = TT.misura(stato_di("F0", ks), nodo, n, L)
        v0, s0, v1, s1, mkv, mkd, sg, om0, _o = r
        print("    k %4d: w %.3f; omega %+.7f; v0 %+.3e +- %.1e, v %+.3e +- %.1e; m* = k/v %+.3f, k/(v - v0) %+.3f (|v - v0| = %.1f sigma)" % (ks, w, om0, v0, s0, v1, s1, mkv, mkd, abs(v1 - v0) / sg))
    print("  (2) m* DI FH, FT, F0 DA k 1500")
    om_iso = {}
    for sg_ in ("F0", "FH", "FT"):
        r = m_star(sg_, 1500)
        if r is None:
            print("    %s: non c'e' ancora" % sg_)
            continue
        v0, s0, v1, s1, mkv, mkd, sg, om0, oms = r
        om_iso[sg_] = float(np.mean(oms[499:]))
        print("    %s: omega %+.7f; v0 %+.3e +- %.1e, v %+.3e +- %.1e; m* = k/v %+.3f, k/(v - v0) %+.3f (%.1f sigma)" % (sg_, om0, v0, s0, v1, s1, mkv, mkd, abs(v1 - v0) / sg))
    print("  (3) LE COPPIE A d %d: a da D(k) col segno (negativo = si avvicinano); A, B coi due punti; il Pound-Rebka (omega del corpo, media [500, %d], - omega isolato, media [500, 1000] della corsa di calcio a k 0)" % (D_COPPIA, K_COPPIA))
    for sg_ in ("F0", "FH", "FT"):
        a = {}
        for g in (0, 180):
            r = _leggi("coppia_%s_k1500_D%d" % (sg_, g))
            if r is None:
                print("    %s delta %d: non c'e' ancora" % (sg_, g))
                continue
            ks = np.array([x[0] for x in r["D"]], float)
            Dv = np.array([x[1] for x in r["D"]], float)
            fb = GM.fit(ks, Dv)
            a[g] = (fb[2], fb[3])
            pr = [float(np.mean(np.array(r["omega"][i])[499:])) for i in (0, 1)]
            dpr = " - ".join("%+.3e" % (x - om_iso[sg_]) for x in pr) if sg_ in om_iso else "(manca omega isolato)"
            print("    %s delta %3d: D da %.4f a %.4f; a %+.4e +- %.1e (il residuo %.2e); omega dei corpi %+.7f %+.7f; il Pound-Rebka %s" % (sg_, g, Dv[0], Dv[-1], fb[2], fb[3], fb[4], pr[0], pr[1], dpr))
        if 0 in a and 180 in a:
            A_ = 0.5 * (a[0][0] - a[180][0])
            B_ = 0.5 * (a[0][0] + a[180][0])
            sgm = 0.5 * math.hypot(a[0][1], a[180][1])
            print("    %s: A %+.4e, B %+.4e, sigma %.1e; in fase %s, in antifase %s" % (sg_, A_, B_, sgm, "si avvicinano" if a[0][0] < 0 else "si allontanano", "si avvicinano" if a[180][0] < 0 else "si allontanano"))
    print("  (4) LA CADUTA V2 DA k 1500: a_y (fit quadratico) - a_y della corsa a k 0 della stessa sorgente; in unita' di c^2 |dN/dy| (|dN/dy| = G20)")
    for sg_ in ("F0", "FH", "FT"):
        r = _leggi("caduta_V2_%s_k1500" % sg_)
        r0 = _leggi("calcio_%s_k1500_%s" % (sg_, MC.nome(0.0, 1)))
        if r is None or r0 is None:
            print("    %s: non c'e' ancora" % sg_)
            continue
        ks = np.array([x[0] for x in r["serie"]], float)
        fb = GM.fit(ks, np.array([x[2] for x in r["serie"]], float))
        k0 = np.array([x[0] for x in r0["serie"]], float)
        f0 = GM.fit(k0, np.array([x[3] for x in r0["serie"]], float))
        ay = fb[2] - f0[2]
        sy = math.hypot(fb[3], f0[3])
        g = float(r["G20"])
        print("    %s: a_y %+.4e +- %.1e (V2 %+.4e, il riferimento %+.4e); a/(c^2 |dN/dy|) %+.4f (c_banda), %+.4f (c_sol): %s" % (
            sg_, ay, sy, fb[2], f0[2], ay / ((C_BANDA * 0.15) ** 2 * g), ay / ((C_SOL * 0.15) ** 2 * g), "VERSO" if ay > 0 else "VIA"))
    print("=" * 130)
    return 0 if all(ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("calcio", "coppia", "caduta", "lettura"))
    ap.add_argument("--sorgente", choices=sorted(FORMA))
    ap.add_argument("--kstato", type=int, default=1500)
    ap.add_argument("--k", type=float)
    ap.add_argument("--gradi", type=int, choices=(0, 180))
    a = ap.parse_args(argv)
    if a.cosa == "calcio":
        return calcio(a.sorgente, a.kstato, a.k)
    if a.cosa == "coppia":
        return coppia(a.sorgente, a.gradi, a.kstato)
    if a.cosa == "caduta":
        return caduta(a.sorgente, a.kstato)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
