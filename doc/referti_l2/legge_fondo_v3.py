# -*- coding: utf-8 -*-
r"""**[M2210] IL FRENO CHE SEGUE IL TEMPO: RAMPA E NORMA LONTANA** *(DECISIONE DI LUCA, 2026-11-24 22:10; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-decies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v3.py noto > doc/referti_l2/legge_fondo_v3_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v3.py corsa --tipo gradino      (r1; rampa = r2, v0 = r3: dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v3.py lettura > doc/referti_l2/legge_fondo_v3.txt

**L'oggetto:** quello del giro 4 *(`puntofisso_v3b/giro_3/stato_006000.npz`, come B3)*; il gradiente `x1`; `2000` tick; **gli stati ogni `250`** *(e `k 0`)* in `M1330/b3v3/<nome>/`. **Il ciclo** e' `fondo_1c.ciclo` riga per riga, con `N` che puo' cambiare a ogni tick: **(r1) gradino** = `N` dall'inizio *(come B3)*; **(r2) rampa** = `N(t) = 1 + (N - 1) min(t/500, 1)`, con `t = kk`, il tick che si fa; **(r3) V0** = `N = 1`, `cs_N False` *(come `fondo_1c.COLL["V0"]`)*. La serie ogni `MC.OGNI` ha le cinque colonne di B3 *(la quinta: `<dN/dy>` pesato col gradiente PIENO)*. **A fine corsa:** `stato_000250.npz` deve esistere *(il caso noto di Luca)*, altrimenti esce `1`.
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
import legge_fondo_v2 as LF  # noqa: E402
import fondo_puntofisso_v3b4 as G4  # noqa: E402
import gradiente_pesato as GP  # noqa: E402

F1 = LF.F1
PF = G4.PF
OGGETTO = G4.PARTENZA_G4
BASE = os.path.join(LF.CTRL, "M1330", "b3v3")
TIPI = {"gradino": "r1_gradino", "rampa": "r2_rampa", "v0": "r3_V0"}
K_RAMPA = 500         # ### Luca: la rampa su 500 tick
OGNI_STATO = 250      # ### Luca: gli stati ogni 250
RAGGIO = 25.0         # ### Luca: il raggio di 25 nodi dal baricentro
FIN_R1 = ((200, 800), (800, 1400), (1400, 2000))
FIN_R2 = ((700, 2000), (800, 1400), (1400, 2000))


def N_di(tipo, N, kk):
    """### `N` al tick `kk` *(1..2000)*: il gradino `N`, la rampa `1 + (N - 1) min(kk/500, 1)` *(letterale)*, la V0 `1`."""
    if tipo == "gradino":
        return N
    if tipo == "rampa":
        return 1.0 + (N - 1.0) * min(kk / float(K_RAMPA), 1.0)
    return None


def ciclo(Z, C, quanti, dopo, MV, P0, N_t, cs_N, segno):
    """### `fondo_1c.ciclo` riga per riga, con `N_t(kk)` al posto di `N` fisso."""
    import ripresa_F0_v2 as RF
    _G20, _ia, e0, MT = F1.CL.parametri()
    s = float(Z["s"])
    with RF.col_nucleo(MV, P0), MV.forma_esplicita(F1.FORMA_OGG):
        assert MV.ATTIVA == F1.FORMA_OGG and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            F1.CS.tick_var(Z["z"], C.campo, s, e0, N_t(kk), cs_N, segno)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


def caduta(tipo, quanti, nome, salva_stati):
    """### una corsa; `F1.OGGETTO` e `F1.BASE` come sono ora. Restituisce la serie e le informazioni."""
    MV, P0 = F1.TT.nucleo()
    G20, _ia, _e0, _MT = F1.CL.parametri()
    import chi_parametri_v2 as CP2
    t1 = time.time()
    d = os.path.join(F1.BASE, nome)
    with F1.TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = F1.FS.carica(Z, "K", 3000)
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        if tipo == "v0":
            N, cs_N = np.ones(n), False
            N_t = lambda kk: N  # noqa: E731
        else:
            _chi, N = F1.CL.campo_N(Z, info, A, +1.0)
            cs_N = True
            N_t = lambda kk: N_di(tipo, N, kk)  # noqa: E731
        y = np.asarray(Z["m2"], float) * math.sqrt(3.0) / 2.0
        g_nodo = GP.dNdy(y, info["y_c"], A, Ly, CP2.KAPPA)
        print("### %s (%s): %s; y_c %.6f; A %.6e; N da %.10f a %.10f; l'impronta %s" % (nome, tipo, info["file"], info["y_c"], A, float(N.min()), float(N.max()), F1.TT.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b[0]), float(b[1]), float(rho.sum()), float((rho * g_nodo).sum() / rho.sum())))

        def salva(kk):
            f = os.path.join(d, "stato_%06d.npz" % kk)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            PF.salva_stato(f, dati, dict(info, k=kk, tipo=tipo, nome=nome))

        def dopo(kk, prima):
            if kk % F1.MC.OGNI == 0:
                misura(kk)
            if salva_stati and kk % OGNI_STATO == 0:
                salva(kk)
            if kk % 250 == 0:
                print("    k %d: y %+.5f, <dN/dy> %+.6e (%.0f s)" % (kk, serie[-1][2], serie[-1][4], time.time() - t1))
                sys.stdout.flush()
        if salva_stati:
            os.makedirs(d, exist_ok=True)
            salva(0)
        misura(0)
        ciclo(Z, C, quanti, dopo, MV, P0, N_t, cs_N, 0)
        Z["metti"]()
    print("### %d tick in %.0f s" % (quanti, time.time() - t1))
    return {"tipo": tipo, "serie": serie, "info": info, "G20": G20, "A": A, "centro": -CP2.KAPPA * A * 2.0 * math.pi / Ly, "k_rampa": K_RAMPA if tipo == "rampa" else None}


def su_v3():
    F1.OGGETTO, F1.BASE = OGGETTO, BASE


def avvia():
    import _presidio
    F1.avvia()
    for m in ("legge_fondo_v2.py", "fondo_puntofisso_v3b4.py", "gradiente_pesato.py", "fondo_s3_v2.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def noto():
    avvia()
    print("=" * 130)
    print("[M2210] IL CASO NOTO DEL CICLO (la carta sez. 3-decies): 100 tick dall'oggetto del giro 4, contro le serie di B3 (M1330/b3)")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    LF.OGGETTO_B3 = OGGETTO
    LF.su_b3()
    b3x1 = [tuple(x) for x in F1.leggi("caduta_V2_x1.0")["serie"] if x[0] <= 100]
    b3v0 = [tuple(x) for x in F1.leggi("caduta_V0")["serie"] if x[0] <= 100]
    r = caduta("gradino", 100, "noto_gradino", False)
    g = [tuple(x) for x in r["serie"]]
    esito("(a) il gradino, 100 tick: le cinque colonne = B3 x1 AL BIT", g == b3x1, "%d righe contro %d" % (len(g), len(b3x1)))
    r = caduta("rampa", 100, "noto_rampa", False)
    ra = [tuple(x) for x in r["serie"]]
    esito("(b) DEVE FALLIRE: la rampa, 100 tick = B3 x1", ra != b3x1, "il y a k 100: rampa %+.6e, gradino %+.6e" % (ra[-1][2], g[-1][2]))
    r = caduta("v0", 100, "noto_v0", False)
    v = [tuple(x[:4]) for x in r["serie"]]
    esito("(c) la V0, 100 tick: le prime quattro colonne = B3 V0 AL BIT", v == b3v0, "%d righe" % len(v))
    Nf = 1.0035207444
    esito("(d) N_di: rampa a 0 tick = 1, a 250 = 1 + (N - 1)/2, a 500 e 2000 = 1 + (N - 1)", N_di("rampa", Nf, 0) == 1.0 and N_di("rampa", Nf, 250) == 1.0 + (Nf - 1.0) * 0.5 and N_di("rampa", Nf, 500) == 1.0 + (Nf - 1.0) and N_di("rampa", Nf, 2000) == 1.0 + (Nf - 1.0), "")
    fall = [k for k, v_ in OK.items() if not v_]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa(tipo):
    avvia()
    assert open(OGGETTO + ".sha1", encoding="utf-8").read().split()[0] == F1.CL.sha1(OGGETTO), "lo sha1 dell'oggetto NON coincide"
    su_v3()
    nome = TIPI[tipo]
    assert not os.path.exists(os.path.join(BASE, nome, "serie.json")), "%s c'e' gia': non si riscrive" % nome
    assert not os.path.exists(os.path.join(BASE, nome, "stato_000000.npz")), "%s ha gia' degli stati: non si riscrive" % nome
    r = caduta(tipo, F1.K_CADUTA, nome, True)
    F1.scrivi(nome, r)
    f250 = os.path.join(BASE, nome, "stato_000250.npz")
    ok = os.path.exists(f250) and os.path.exists(f250 + ".sha1")
    print("### IL CASO NOTO DI LUCA: %s %s" % (f250, "ESISTE" if ok else "### NON ESISTE"))
    return 0 if ok else 1


def lontano(f, nodo, n, dxy):
    """### da uno stato: `(frazione della norma fuori dal raggio, |psi| massimo fuori, il baricentro)`; `|psi|` per nodo = `sqrt(rho)`."""
    import gravita_due_corpi_misure as GM
    X, _m = GM.leggi(f)
    rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
    b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
    fuori = np.hypot(dxy[:, 0] - b[0], dxy[:, 1] - b[1]) > RAGGIO
    return float(rho[fuori].sum() / rho.sum()), float(np.sqrt(rho[fuori].max())), b


def lettura():
    import caduta_finestre as CF
    import fondo_s3_v2 as S3V2
    avvia()
    MC = F1.MC
    print("=" * 130)
    print("[M2210] IL FRENO CHE SEGUE IL TEMPO (la carta sez. 3-decies): K per finestra del gradino (r1) e della rampa (r2), e la norma lontana (raggio %.0f nodi) di r1, r2, r3" % RAGGIO)
    print("=" * 130)
    LF.su_1c()
    r0, r1_ = F1.leggi("calcio_%s" % MC.nome(0.0, 1)), F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    v0_, _s0, _ = MC.velocita(r0["serie"])
    v1_, _s1, _ = MC.velocita(r1_["serie"])
    mstar = 0.010 / (v1_ - v0_)
    _dD, w1 = S3V2.pendenze()
    LF.OGGETTO_B3 = OGGETTO
    LF.su_b3()
    b3x1, b3v0 = F1.leggi("caduta_V2_x1.0")["serie"], F1.leggi("caduta_V0")["serie"]
    su_v3()
    R = {t: F1.leggi(TIPI[t]) for t in TIPI}
    print("  le costanti di 1c (come B3): m* %+.4f; omega_psi(N1) %+.7f" % (mstar, w1))
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    for t in TIPI:
        f250 = os.path.join(BASE, TIPI[t], "stato_000250.npz")
        esito("(Luca) %s: stato_000250.npz esiste" % TIPI[t], os.path.exists(f250 + ".sha1"))
    esito("r1 (il gradino) = B3 x1 AL BIT, tutta la serie (salvare gli stati non tocca la dinamica)", [list(x) for x in R["gradino"]["serie"]] == [list(x) for x in b3x1])
    esito("r3 (la V0) = B3 V0 AL BIT, le prime quattro colonne", [list(x[:4]) for x in R["v0"]["serie"]] == [list(x) for x in b3v0])
    c0 = R["v0"]
    print("-" * 130)
    print("(i) K CIMA PESATA PER FINESTRA (V0 = r3); per r2 il fit DOPO la rampa ([700, 2000] e le finestre di 600 dentro)")
    print("-" * 130)
    for t, fins in (("gradino", FIN_R1 + ((200, 2000),)), ("rampa", FIN_R2)):
        c = R[t]
        s = np.array(c["serie"])
        for w in fins:
            a, sa, _ = CF.fit(c["serie"], *w)
            a0, sa0, _ = CF.fit(c0["serie"], *w)
            m = (s[:, 0] >= w[0]) & (s[:, 0] <= w[1])
            g = float(s[m, 4].mean())
            pp, pc = -(w1 * g) / mstar, -(w1 * float(c["centro"])) / mstar
            da, sda = a - a0, math.hypot(sa, sa0)
            print("  %-8s [%4d, %4d]: a - a(V0) %+.4e +- %.1e; <dN/dy>/centro %.5f; K CIMA PESATA %+.4f +- %.4f (al centro %+.4f)" % (t, w[0], w[1], da, sda, g / float(c["centro"]), da / pp, abs(sda / pp), da / pc))
    print("-" * 130)
    print("(ii) e (iii) LA NORMA FUORI DAL RAGGIO %.0f DAL BARICENTRO (frazione della massa) e |psi| MASSIMO FUORI (|psi| per nodo = sqrt(rho)), per stato" % RAGGIO)
    print("-" * 130)
    su_v3()
    with F1.TC.scena() as Z:
        nodo, n = np.asarray(Z["mot"].inc.nodo), Z["n"]
        _C, _info, dxy, _f, _X = F1.FS.carica(Z, "K", 3000)
        Z["metti"]()
    print("  %6s   %-34s %-34s %-34s" % ("k", "r1 gradino: norma, |psi| max", "r2 rampa: norma, |psi| max", "r3 V0: norma, |psi| max"))
    for k in range(0, F1.K_CADUTA + 1, OGNI_STATO):
        cel = []
        for t in TIPI:
            f = os.path.join(BASE, TIPI[t], "stato_%06d.npz" % k)
            PF.controlla(f)
            fr, mx, _b = lontano(f, nodo, n, dxy)
            cel.append("%.6e, %.4e" % (fr, mx))
        print("  %6d   %-34s %-34s %-34s" % (k, cel[0], cel[1], cel[2]))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    ap.add_argument("--tipo", choices=tuple(TIPI))
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        return corsa(a.tipo)
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
