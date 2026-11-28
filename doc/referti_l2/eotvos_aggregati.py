# -*- coding: utf-8 -*-
r"""**[M0141] D-P3: EOTVOS CON GLI AGGREGATI** *(DECISIONE DI LUCA, 2026-11-28 01:41; la carta `doc/CARTA_mitosi.md`, «D-P3»)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/eotvos_aggregati.py noto > doc/referti_l2/eotvos_aggregati_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/eotvos_aggregati.py M            (dalla coda: la caduta di [M2210] V2 rifatta fino a 6000)
    E:\python\py3132\python.exe doc/referti_l2/eotvos_aggregati.py agg          (dalla coda: l'aggregato destro + sinistro, 6000 tick)
    E:\python\py3132\python.exe doc/referti_l2/eotvos_aggregati.py lettura > doc/referti_l2/eotvos_aggregati.txt

**La scena** *(`caduta_libera`, [M2210], la variante V2: `chi` dipinto acceso, `cs = s N`, la fase (a) spenta; `tick_var`; `g_e = 0`; il campo
U(1) acceso come nelle scene del triangolo, `e = E_DECISO`)*. **M:** `caduta_libera.prepara` *(un francobollo `L162`)*, `y_c` sul suo
baricentro, 6000 tick in `controllo/M0141/M`; **(K5)** gli stati `0..2000` = `CHI/caduta/V2` AL BIT *(altrimenti FERMO)*. **L'aggregato:**
il destro = le righe di `triangolo_chi_v4.prepara` per `t120` *(fasi `0, 120, 240`)*; il sinistro = gli stessi vertici `+81` in `m1`
*(`x`)*, le fasi `0, -120, -240`; la materia per SOMMA, il vuoto per PRODOTTO *(come `prepara`)*; `y_c` sul baricentro dell'aggregato;
6000 tick in `controllo/M0141/agg`. **G** = `somma_i m_i dN/dy(y_i) / (somma_i m_i dN/dy(y_c))`, `y_i` il baricentro del francobollo `i` da
solo, `m_i` la sua massa *(`prepara`)*; `dN/dy = -kappa A (2 pi/L_y) cos(2 pi (y - y_c)/L_y) N(y)`. **Casi noti:** (K1) a `k 0` il giro del
sinistro `-1`, del destro `+1`, e `J_theta` del sinistro = `-J_theta` del destro entro `1e-9`; (K2) la carica TOPOLOGICA `+1 - 1 = 0`
*(stampate anche `e somma rho` -- la massa, NON zero -- e la sorgente di Gauss, zero per costruzione)*; (K3) dichiarato: [M0222] girava col
tick di `chi` dinamico, qui `tick_var` col `chi` dipinto: AL BIT non e' confrontabile; (K4) `G_M` entro `1e-3` da `1`; (K5) nella corsa di M.
"""
import argparse
import glob
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
import caduta_libera as CLb  # noqa: E402
import triangoli_vortice as TV4  # noqa: E402

TC, CS, CP2 = CLb.TC, CLb.CS, CLb.CP2
CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
D_M, D_AGG, D_V2 = os.path.join(CTRL, "M0141", "M"), os.path.join(CTRL, "M0141", "agg"), os.path.join(CLb.BASE, "V2")
CS_N, SEGNO, SEGNO_CHI = True, 0, 1.0            # ### V2 (Luca 01:41)
DX = 81
K_FINE, OGNI = 6000, 250
FASI_D = (0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0)
FASI_S = (0.0, -2.0 * math.pi / 3.0, -4.0 * math.pi / 3.0)
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py", "triangoli_vortice.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def semina_agg(Z):
    """### le righe di `triangolo_chi_v4.prepara` per DUE triangoli: il destro (t120) e il sinistro (+81 in m1, le fasi rovesciate). `(C, info)`."""
    from solitone import toro as TO
    MT, _MTR, T1, _TRU, TV, PO = TC.moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    fr = TV.francobollo_L162(0)
    VD = [list(v) for v in T1.vertici(Z["bordo"]["c0"], fr, L)]
    VS = [[v[0] + DX, v[1]] for v in VD]                # ### NON ridotti: il centro di Geo e' la media dei vertici (toro.scarti e' periodico)
    Z["g_e"] = np.zeros_like(Z["g_e"])
    MT.vuoto_fresco(Z, t0)
    phi_F3 = st["phi_h"].copy()
    vuoto = {x: st[x].copy() for x in Z["chiavi"]}
    soli = []
    for V, F in ((VD, FASI_D), ([[v[0] % L, v[1]] for v in VS], FASI_S)):      # ### incollati ridotti in [0, L)
        for j, c in enumerate(V):
            for x in Z["chiavi"]:
                st[x][...] = vuoto[x]
            MT.incolla(Z, fr, c, True)
            if F[j] != 0.0:
                st["psi_h"][...] = st["psi_h"] * np.exp(1j * F[j])
            soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
    psi = soli[0][0].copy()
    phi = soli[0][1].copy()
    for s_ in soli[1:]:
        psi = psi + s_[0]
        phi = phi * (s_[1] / phi_F3)
    st["psi_h"][...] = psi
    st["phi_h"][...] = phi
    C = PO.campi(Z, rho_c, e)
    nodo = np.asarray(Z["mot"].inc.nodo)
    n = Z["n"]
    m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)

    def bari_y(ph):
        r = np.bincount(nodo, weights=np.sum(np.abs(ph) ** 2, axis=1), minlength=n)
        c1, c2, _x, _y = TO.centro(r, m1, m2, L)
        return float(c2 * math.sqrt(3.0) / 2.0), float(r.sum()), (c1, c2)
    yi, mi, ci = zip(*[bari_y(s_[0]) for s_ in soli])
    y_c, M_tot, c_agg = bari_y(psi)
    return C, {"destro": VD, "sinistro": VS, "fasi_destro_gradi": [math.degrees(x) for x in FASI_D], "fasi_sinistro_gradi": [math.degrees(x) for x in FASI_S],
               "y_i": list(yi), "m_i": list(mi), "c_i": [list(c) for c in ci], "y_c": y_c, "massa": M_tot, "centro": list(c_agg), "dx": DX}


def dNdy(y, y_c, A, Ly):
    k = CP2.KAPPA
    ph = 2.0 * math.pi * (np.asarray(y) - y_c) / Ly
    return -k * A * (2.0 * math.pi / Ly) * np.cos(ph) * np.exp(-k * A * np.sin(ph))


def G_di(y_i, m_i, y_c, A, Ly):
    y_i, m_i = np.asarray(y_i, float), np.asarray(m_i, float)
    return float(np.sum(m_i * dNdy(y_i, y_c, A, Ly)) / (np.sum(m_i) * dNdy(y_c, y_c, A, Ly)))


def ampiezza(Z):
    G20, ia, e0, MT = CLb.parametri()
    L = Z["L"]
    Ly = L * math.sqrt(3.0) / 2.0
    return G20 * Ly / (2.0 * math.pi * CP2.KAPPA), Ly, G20, e0


def noto():
    avvia()
    print("=" * 134)
    print("[M0141] D-P3, I CASI NOTI E G: K1 (il giro e J_theta), K2 (la carica topologica), K3 (dichiarato), K4 (G_M); G_agg e G_M a k 0")
    print("=" * 134)
    with TC.scena() as Z:
        A, Ly, G20, e0 = ampiezza(Z)
        C, info = CLb.prepara(Z)
        nodo = np.asarray(Z["mot"].inc.nodo)
        r = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=Z["n"])
        G_M = G_di([info["y_c"]], [info["massa"]], info["y_c"], A, Ly)
        print("  M (caduta_libera.prepara): il centro %s, y_c %.6f, la massa %.6e; G_M %.12f" % (info["centro"], info["y_c"], info["massa"], G_M))
        esito("(K4) G_M entro 1e-3 da 1", abs(G_M - 1.0) < 1e-3, "%.3e" % abs(G_M - 1.0))
        Z["metti"]()
    with TC.scena() as Z:
        A, Ly, G20, e0 = ampiezza(Z)
        C, info = semina_agg(Z)
        G_agg = G_di(info["y_i"], info["m_i"], info["y_c"], A, Ly)
        print("  A %.6e (G20 %.6e, L_y %.6f, kappa %r), e0 %r, e %r" % (A, G20, Ly, CP2.KAPPA, e0, C.campo.e))
        print("  l'aggregato: il destro %s, il sinistro %s; y_c %.6f; la massa %.6e" % (info["destro"], info["sinistro"], info["y_c"], info["massa"]))
        for q, (y, m) in enumerate(zip(info["y_i"], info["m_i"])):
            print("    il francobollo %d: y %.6f (y - y_c %+.6f), la massa %.6e; dN/dy / dN/dy(y_c) %.6f" % (q, y, y - info["y_c"], m, float(dNdy(y, info["y_c"], A, Ly) / dNdy(info["y_c"], info["y_c"], A, Ly))))
        print("### G_agg %.12f (la media pesata con le masse del gradiente sulle posizioni dei sei francobolli); G_M 1 a k 0" % G_agg)
        psi = Z["st"]["psi_h"]
        G = {}
        for nome, V, F in (("destro", info["destro"], FASI_D), ("sinistro", info["sinistro"], FASI_S)):
            geo = TV4.Geo(Z, V)
            g, gi = geo.giri(geo.psi(psi))
            G[nome] = (gi["R"], geo.j_theta(geo.psi(psi)))
            print("    %s: il giro a R %+.4f (componente %d), J_theta %s" % (nome, gi["R"], g, ["%+.10e" % x for x in G[nome][1]]))
        dj = max(abs(a + b) for a, b in zip(G["destro"][1], G["sinistro"][1]))
        esito("(K1) a k 0: il destro +1, il sinistro -1, J_theta del sinistro = -J_theta del destro entro 1e-9",
              abs(G["destro"][0] - 1) < 0.1 and abs(G["sinistro"][0] + 1) < 0.1 and dj < 1e-9, "giri %+.4f %+.4f; max |J_s + J_d| %.3e" % (G["destro"][0], G["sinistro"][0], dj))
        q_top = round(G["destro"][0]) + round(G["sinistro"][0])
        rho = np.bincount(np.asarray(Z["mot"].inc.nodo), weights=np.sum(np.abs(psi) ** 2, axis=1), minlength=Z["n"])
        esito("(K2) la carica TOPOLOGICA dell'aggregato (la somma dei giri) = 0", q_top == 0, "%+d; e somma rho %.6e (la massa: NON zero); la sorgente di Gauss somma %.3e (zero per costruzione)" % (
            q_top, C.campo.e * float(rho.sum()), float(np.sum(C.campo.e * (rho - rho.mean())))))
        print("  (K3) DICHIARATO: [M0222] girava col tick di chi dinamico (chi_tick_v2); qui tick_var col chi dipinto: il confronto AL BIT non e' definito")
        Z["metti"]()
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


def corsa(quale):
    avvia()
    d_out = D_M if quale == "M" else D_AGG
    assert not glob.glob(os.path.join(d_out, "stato_*.npz")), "%s ha gia' degli stati: non si riscrive" % d_out
    os.makedirs(d_out, exist_ok=True)
    codice = 0
    with TC.scena() as Z:
        A, Ly, G20, e0 = ampiezza(Z)
        C, info = CLb.prepara(Z) if quale == "M" else semina_agg(Z)
        s = float(Z["s"])
        chi, N = CLb.campo_N(Z, info, A, SEGNO_CHI)
        MT = TC.moduli()[0]
        meta = dict(info, corsa="M0141_" + quale, variante="V2", cs_N=CS_N, segno_fase=SEGNO, segno_chi=SEGNO_CHI, A=A, G20=G20, L_y=Ly, kappa=CP2.KAPPA, s=s, e0=e0)
        print("### [M0141] %s: A %.6e, y_c %.6f; N da %.10f a %.10f; l'impronta %s; in %s" % (quale, A, info["y_c"], float(N.min()), float(N.max()), CLb.impronta(Z, C), d_out))
        sys.stdout.flush()

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, chi=chi, N=N)
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
            if quale == "M" and k <= 2000:
                fv = os.path.join(D_V2, "stato_%06d.npz" % k)
                with np.load(fz) as a, np.load(fv) as b:
                    dd = [x for x in a.files if x != "meta" and (x not in b.files or not np.array_equal(a[x], b[x]))]
                print("    (K5) k %d contro CHI/caduta/V2: %s" % (k, "AL BIT" if not dd else "### DIVERSE %s" % dd))
                return not dd
            return True
        assert salva(0), "(K5) lo stato a k 0 NON e' quello di CHI/caduta/V2: FERMO"
        t1 = time.time()
        for k in range(1, K_FINE + 1):
            CS.tick_var(Z["z"], C.campo, s, e0, N, CS_N, SEGNO)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % OGNI == 0:
                if not salva(k):
                    print("### (K5) FALLISCE a k %d: FERMO" % k)
                    codice = 1
                    break
                print("    [stato] k %d (%.0f s)" % (k, time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    print("### %s: il codice %d" % (quale, codice))
    return codice


def y_bari(d, ks):
    from solitone import toro as TO
    out = []
    with TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        Z["metti"]()
    meta0 = None
    for k in ks:
        with np.load(os.path.join(d, "stato_%06d.npz" % k)) as z:
            rho = np.bincount(nodo, weights=np.sum(np.abs(z["psi_h"]) ** 2, axis=1), minlength=n)
            if meta0 is None:
                meta0 = json.loads(str(z["meta"]))
        c = meta0["centro"]
        dxy = np.asarray(TO.scarti(m1, m2, c[0], c[1], L))[:, :2]
        out.append(float((dxy * rho[:, None]).sum(axis=0)[1] / rho.sum()))
    return np.array(out), meta0


def fit_a(ks, y):
    k = np.asarray(ks, float)
    X = np.column_stack([np.ones_like(k), k, 0.5 * k ** 2])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ c
    s2 = float(r @ r) / max(len(y) - 3, 1)
    return float(c[2]), float(math.sqrt(s2 * np.linalg.inv(X.T @ X)[2, 2]))


def lettura():
    avvia()
    print("=" * 134)
    print("[M0141] D-P3, LA LETTURA: a_M, a_agg (fit di y del baricentro su 0..2000 e su 0..6000), G, lo scarto, eta")
    print("=" * 134)
    K2, K6 = list(range(0, 2001, OGNI)), list(range(0, K_FINE + 1, OGNI))
    yM, mM = y_bari(D_M, K6)
    yA, mA = y_bari(D_AGG, K6)
    G_M = G_di([mM["y_c"]], [mM["massa"]], mM["y_c"], mM["A"], mM["L_y"])
    G_A = G_di(mA["y_i"], mA["m_i"], mA["y_c"], mA["A"], mA["L_y"])
    print("  G_M %.12f, G_agg %.12f" % (G_M, G_A))
    res = {}
    for nome, ks in (("0..2000 (IL VERDETTO)", K2), ("0..6000", K6)):
        aM, sM = fit_a(ks, yM[:len(ks)])
        aA, sA = fit_a(ks, yA[:len(ks)])
        sc = abs(aA / aM - G_A / G_M)
        eta = 2.0 * (aA / G_A - aM / G_M) / (aA / G_A + aM / G_M)
        res[nome] = (aM, sM, aA, sA, sc, eta)
        print("  %s: a_M %+.6e +- %.2e; a_agg %+.6e +- %.2e; a_agg/a_M %.6f contro G_agg/G_M %.6f: lo scarto %.4f (%.2f%%); eta %+.4e" % (
            nome, aM, sM, aA, sA, aA / aM, G_A / G_M, sc, 100 * sc, eta))
    sc = res["0..2000 (IL VERDETTO)"][4]
    aA, aM = res["0..2000 (IL VERDETTO)"][2], res["0..2000 (IL VERDETTO)"][0]
    ver = "PASSA" if sc < 0.01 else ("ALTRO (l'aggregato cade %s di M)" % ("PIU'" if aA / aM > G_A / G_M else "MENO") if sc < 0.05 else "NON PASSA")
    print("### IL VERDETTO (lo scarto su 0..2000, la soglia 1%%): %s" % ver)
    print("  y del baricentro: M %s" % " ".join("%.4f" % x for x in yM[::4]))
    print("                    agg %s" % " ".join("%.4f" % x for x in yA[::4]))
    print("=" * 134)
    return 0


def main(argv):
    a = argparse.ArgumentParser()
    a.add_argument("modo", choices=("noto", "M", "agg", "lettura"))
    x = a.parse_args(argv)
    if x.modo == "noto":
        return noto()
    if x.modo == "lettura":
        return lettura()
    return corsa(x.modo)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
