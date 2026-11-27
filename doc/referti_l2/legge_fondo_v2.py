# -*- coding: utf-8 -*-
r"""**[M1330-B3] LA LEGGE DEL FONDO DALL'OGGETTO SENZA RESPIRO, COL GRADIENTE PESATO** *(DECISIONE DI LUCA, 2026-11-24 13:30 [M1330] e 17:35 [M1735]: «se passa, B3 parte da solo, le quattro cadute»; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-septies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2.py noto > doc/referti_l2/legge_fondo_v2_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2.py caduta --coll V0               (M1330B3_V0, dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2.py caduta --coll V2 --scala 0.5   (0.5, 1.0, 2.0)
    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2.py lettura > doc/referti_l2/legge_fondo_v2.txt

**L'oggetto:** `M1330/puntofisso_v3b/giro_3/partenza_giro_3.npz`, lo stato la cui evoluzione di `6000` tick ha passato il criterio *(la carta: perche' questo e non `partenza_giro_4`)*. **Le uscite** in `M1330/b3/<nome>/serie.json`. **La V0:** `fondo_1c.caduta("V0")` cosi' com'e'. **Le V2:** `fondo_s3.caduta` riga per riga, con una sola aggiunta in `misura`: **`<dN/dy>` pesato con `rho`** *(la formula di `gradiente_pesato.dNdy`)*, una quinta colonna della serie che non tocca la dinamica. **La lettura:** K CIMA per finestra, col gradiente al centro *(come S3)* e col gradiente pesato *(la media della colonna nella finestra)*; `m*` e `omega_psi(N1)` sono quelli di 1c *(la carta)*.
"""
import argparse
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import gradiente_pesato as GP  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
OGGETTO_B3 = os.path.join(CTRL, "M1330", "puntofisso_v3b", "giro_3", "partenza_giro_3.npz")
BASE_B3 = os.path.join(CTRL, "M1330", "b3")
BASE_1C, OGGETTO_1C = F1.BASE, F1.OGGETTO
FINESTRE = ((200, 2000), (200, 800), (800, 1400), (1400, 2000))
SCALE = (0.5, 1.0, 2.0)
K_NOTO = 100


def su_b3():
    F1.OGGETTO, F1.BASE = OGGETTO_B3, BASE_B3


def su_1c():
    F1.OGGETTO, F1.BASE = OGGETTO_1C, BASE_1C


def caduta_v2(scala, quanti, nome):
    """### `fondo_s3.caduta` riga per riga *(F1.OGGETTO e F1.BASE come sono ora)*, piu' `<dN/dy>` pesato in `misura`; `quanti` tick."""
    MV, P0 = F1.TT.nucleo()
    G20, _ia, _e0, _MT = F1.CL.parametri()
    import chi_parametri_v2 as CP2
    t1 = time.time()
    with F1.TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = F1.FS.carica(Z, "K", 3000)
        Ly = L * math.sqrt(3.0) / 2.0
        A = float(scala) * G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        _chi, N = F1.CL.campo_N(Z, info, A, +1.0)
        y = np.asarray(Z["m2"], float) * math.sqrt(3.0) / 2.0
        g_nodo = GP.dNdy(y, info["y_c"], A, Ly, CP2.KAPPA)
        print("### %s: %s; y_c %.6f; A %.6e (x%.1f); N da %.10f a %.10f; l'impronta %s" % (nome, info["file"], info["y_c"], A, scala, float(N.min()), float(N.max()), F1.TT.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b[0]), float(b[1]), float(rho.sum()), float((rho * g_nodo).sum() / rho.sum())))

        def dopo(kk, prima):
            if kk % F1.MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: y %+.5f, <dN/dy> %+.6e (%.0f s)" % (kk, serie[-1][2], serie[-1][4], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        F1.ciclo(Z, C, quanti, dopo, MV, P0, N, True, 0)
        Z["metti"]()
    print("### %d tick in %.0f s" % (quanti, time.time() - t1))
    return {"coll": "V2", "scala": scala, "serie": serie, "info": info, "G20": G20, "A": A, "centro": -CP2.KAPPA * A * 2.0 * math.pi / Ly}


def noto():
    import _presidio
    F1.avvia()
    for m in ("fondo_s3.py", "gradiente_pesato.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1330-B3] IL CASO NOTO DELLE CADUTE (la carta sez. 3-septies): la V2 x1 su 1c per %d tick contro la serie di 1c (M1658/c1/caduta_V2)" % K_NOTO)
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    su_1c()
    r = caduta_v2(1.0, K_NOTO, "noto_x1.0")
    vecchia = [tuple(x) for x in F1.leggi("caduta_V2")["serie"] if x[0] <= K_NOTO]
    nuova = [tuple(x[:4]) for x in r["serie"]]
    esito("(a) le prime 4 colonne = la serie di 1c (k <= %d) AL BIT" % K_NOTO, nuova == vecchia, "%d righe contro %d" % (len(nuova), len(vecchia)))
    x2 = [tuple(x) for x in F1.leggi("caduta_V2_x2.0")["serie"] if x[0] <= K_NOTO]
    esito("(b) DEVE FALLIRE: le stesse colonne = la serie x2 di 1c", nuova != x2, "")
    g0 = r["serie"][0][4]
    esito("(c) <dN/dy>/centro a k 0 = quello di B0 sullo stesso stato (0.95481, k_forma.txt) entro 5e-6", abs(g0 / r["centro"] - 0.95481) < 5e-6, "<dN/dy> %+.6e, il centro %+.6e, il rapporto %.6f" % (g0, r["centro"], g0 / r["centro"]))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def caduta(coll, scala):
    import _presidio
    F1.avvia()
    for m in ("fondo_s3.py", "gradiente_pesato.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    assert open(OGGETTO_B3 + ".sha1", encoding="utf-8").read().split()[0] == F1.CL.sha1(OGGETTO_B3), "lo sha1 dell'oggetto NON coincide"
    su_b3()
    if coll == "V0":
        assert scala is None
        assert not os.path.exists(os.path.join(BASE_B3, "caduta_V0", "serie.json")), "la V0 c'e' gia': non si riscrive"
        return F1.caduta("V0")
    nome = "caduta_V2_x%.1f" % scala
    assert not os.path.exists(os.path.join(BASE_B3, nome, "serie.json")), "%s c'e' gia': non si riscrive" % nome
    r = caduta_v2(scala, F1.K_CADUTA, nome)
    F1.scrivi(nome, r)
    return 0


def lettura():
    import _presidio
    import caduta_finestre as CF
    import fondo_s3_v2 as S3V2
    F1.avvia()
    for m in ("fondo_s3.py", "fondo_s3_v2.py", "gradiente_pesato.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    MC = F1.MC
    print("=" * 130)
    print("[M1330-B3] LA LEGGE DEL FONDO DALL'OGGETTO SENZA RESPIRO (la carta sez. 3-septies): K CIMA col gradiente al centro e col gradiente PESATO")
    print("=" * 130)
    su_1c()
    r0, r1 = F1.leggi("calcio_%s" % MC.nome(0.0, 1)), F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    v0, _s0, _ = MC.velocita(r0["serie"])
    v1, _s1, _ = MC.velocita(r1["serie"])
    mstar = 0.010 / (v1 - v0)
    _dD, w1 = S3V2.pendenze()
    print("  DI 1c (la carta): m* %+.4f; omega_psi(N1) %+.7f" % (mstar, w1))
    su_b3()
    c0 = F1.leggi("caduta_V0")
    assert c0 is not None, "la V0 manca"
    print("  l'oggetto: %s" % c0["info"]["file"])
    Kc = {}
    for sc in SCALE:
        c = F1.leggi("caduta_V2_x%.1f" % sc)
        assert c is not None, "la x%.1f manca" % sc
        s = np.array(c["serie"])
        print("  x%.1f (A %.6e; il centro %+.6e):" % (sc, float(c["A"]), float(c["centro"])))
        for w in FINESTRE:
            a, sa, _ = CF.fit(c["serie"], *w)
            a0, sa0, _ = CF.fit(c0["serie"], *w)
            m = (s[:, 0] >= w[0]) & (s[:, 0] <= w[1])
            g = float(s[m, 4].mean())
            pc, pp = -(w1 * float(c["centro"])) / mstar, -(w1 * g) / mstar
            da, sda = a - a0, math.hypot(sa, sa0)
            kc, kp = da / pc, da / pp
            if w == (200, 2000):
                Kc[sc] = (kc, kp)
            print("    [%4d, %4d]: a - a(V0) %+.4e +- %.1e; <dN/dy>/centro %.5f;   K CIMA al centro %+.4f +- %.4f;   K CIMA PESATO %+.4f +- %.4f" % (w[0], w[1], da, sda, g / float(c["centro"]), kc, abs(sda / pc), kp, abs(sda / pp)))
    for i, nome in ((0, "al centro"), (1, "PESATO")):
        v = [Kc[x][i] for x in SCALE]
        m, sd = float(np.mean(v)), float(np.std(v, ddof=1))
        print("### K CIMA %s su [200, 2000]: %s; la media %+.4f, lo scarto %.4f (%.2f%% della media)" % (nome, ", ".join("%+.4f" % x for x in v), m, sd, 100 * sd / abs(m)))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "caduta", "lettura"))
    ap.add_argument("--coll", choices=("V0", "V2"))
    ap.add_argument("--scala", type=float, choices=SCALE)
    a = ap.parse_args(argv)
    if a.cosa == "caduta":
        return caduta(a.coll, a.scala)
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
