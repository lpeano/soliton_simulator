# -*- coding: utf-8 -*-
r"""**[M2045] LE LETTURE SULLE CADUTE DI B3: IL GRADIENTE RAGGIUNTO, K(v), m*(p), a(V0)** *(DECISIONE DI LUCA, 2026-11-24 20:45; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-nonies`; solo letture, nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2c.py > doc/referti_l2/legge_fondo_v2c.txt

**Le cadute di B3 non hanno salvato gli stati:** solo la serie ogni `MC.OGNI` tick *(il baricentro, la massa, e la quinta colonna, `<dN/dy>` pesato con il `rho` di QUEL tick: il gradiente alla posizione raggiunta)*. Le quattro letture si fanno da li':
(i) `<dN/dy>(k)` contro `<dN/dy>(0)`, e la parte del calo di K al centro che il gradiente spiega;
(ii) K PESATA per finestra contro `v` della finestra *(`v` = `(y(k1) - y(k0))/(k1 - k0)` della V2 meno quella della V0)*;
(iii) `m*(p)` = `dp/dv` letto da `ep_fondo.txt`, interpolato a `p = m*(0) v`, e `K(v)/(m*(0)/m*(p))`;
(iv) `a(V0)` per finestra, da sola.
"""
import math
import os
import re
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import legge_fondo_v2 as LF  # noqa: E402
import fondo_puntofisso_v3b4 as G4  # noqa: E402

LF.OGGETTO_B3 = G4.PARTENZA_G4
F1 = LF.F1
EP_TXT = os.path.join(_QUI, "ep_fondo.txt")
FIN3 = ((200, 800), (800, 1400), (1400, 2000))


def dpdv_da_ep():
    """### `(p, dp/dv)` dalle righe «dp/dv contro gamma^3 m» di `ep_fondo.txt` *(committato pulito: si verifica)*; le due righe devono coincidere."""
    rel = os.path.relpath(EP_TXT, os.path.join(_QUI, "..", "..")).replace("\\", "/")
    q = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=os.path.join(_QUI, "..", ".."))
    assert q.returncode == 0, "ep_fondo.txt non e' quello committato"
    righe = [r for r in open(EP_TXT, encoding="utf-8").read().splitlines() if "dp/dv contro gamma^3 m:" in r]
    assert len(righe) >= 1
    tab = []
    for r in righe:
        t = [(float(a), float(b)) for a, b in re.findall(r"p ([+-][0-9.]+): ([+-][0-9.]+e[+-][0-9]+) /", r)]
        tab.append(t)
    assert all(t == tab[0] for t in tab), "le righe dp/dv di ep_fondo.txt non coincidono"
    p, d = np.array([x[0] for x in tab[0]]), np.array([x[1] for x in tab[0]])
    assert np.all(np.diff(p) > 0)
    return p, d


def mstar_p(p, P, D):
    """### `m*(p)`: l'interpolazione lineare di `dp/dv`; sotto il primo punto, il primo punto *(= `m*(0)`, dichiarato)*."""
    return float(np.interp(abs(p), P, D, left=D[0], right=D[-1]))


def v_fin(serie, k0, k1):
    s = np.array(serie)
    i0, i1 = int(np.where(s[:, 0] == k0)[0][0]), int(np.where(s[:, 0] == k1)[0][0])
    return float((s[i1, 2] - s[i0, 2]) / (k1 - k0))


def main():
    import _presidio
    import caduta_finestre as CF
    import fondo_s3_v2 as S3V2
    F1.avvia()
    for m in ("legge_fondo_v2.py", "fondo_puntofisso_v3b4.py", "fondo_s3_v2.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    MC = F1.MC
    print("=" * 130)
    print("[M2045] LE LETTURE SULLE CADUTE DI B3 (la carta sez. 3-nonies): dalle serie (gli stati non sono salvati); nessuna corsa")
    print("=" * 130)
    LF.su_1c()
    r0, r1 = F1.leggi("calcio_%s" % MC.nome(0.0, 1)), F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    v0_, _s0, _ = MC.velocita(r0["serie"])
    v1_, _s1, _ = MC.velocita(r1["serie"])
    mstar = 0.010 / (v1_ - v0_)
    _dD, w1 = S3V2.pendenze()
    LF.su_b3()
    c0 = F1.leggi("caduta_V0")
    C = {sc: F1.leggi("caduta_V2_x%.1f" % sc) for sc in LF.SCALE}
    P, D = dpdv_da_ep()
    m0 = float(D[0])
    print("  le costanti di 1c (come B3): m* %+.4f; omega_psi(N1) %+.7f. Da ep_fondo.txt: dp/dv ai p %s = %s; m*(0) = dp/dv al primo punto %.4f" % (mstar, w1, " ".join("%.4f" % x for x in P), " ".join("%.4f" % x for x in D), m0))
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))

    def kp(c, w):
        s = np.array(c["serie"])
        a, sa, _ = CF.fit(c["serie"], *w)
        a0, sa0, _ = CF.fit(c0["serie"], *w)
        m = (s[:, 0] >= w[0]) & (s[:, 0] <= w[1])
        g = float(s[m, 4].mean())
        pp, pc = -(w1 * g) / mstar, -(w1 * float(c["centro"])) / mstar
        return (a - a0) / pp, (a - a0) / pc, abs(math.hypot(sa, sa0) / pp), g
    k1, kc1, _, _ = kp(C[1.0], (200, 800))
    esito("(a) il caso noto: K PESATA x1 [200, 800] = 1.0014 di legge_fondo_v2.txt (4 decimali)", round(k1, 4) == 1.0014, "%.6f" % k1)
    esito("(b) DEVE FALLIRE: la stessa col gradiente al centro = 1.0014", round(kc1, 4) != 1.0014, "%.6f" % kc1)
    esito("(c) dp/dv di ep_fondo.txt al primo punto (p 0.0099) = 19.036", abs(P[0] - 0.0099) < 1e-12 and abs(m0 - 19.036) < 1e-9, "p %.4f, %.4f" % (P[0], m0))
    print("-" * 130)
    print("(i) IL GRADIENTE ALLA POSIZIONE RAGGIUNTA: <dN/dy>(k) (la quinta colonna, il rho di quel tick) contro <dN/dy>(0)")
    print("-" * 130)
    for sc in LF.SCALE:
        s = np.array(C[sc]["serie"])
        g0 = s[0, 4]
        sel = [i for i in range(len(s)) if int(s[i, 0]) % 400 == 0]
        print("  x%.1f: y(k) - y(0) e <dN/dy>(k)/<dN/dy>(0): %s" % (sc, "; ".join("k %d: %+.4f, %.5f" % (int(s[i, 0]), s[i, 2] - s[0, 2], s[i, 4] / g0) for i in sel)))
        ka, kca, _, ga = kp(C[sc], FIN3[0])
        kb, kcb, _, gb = kp(C[sc], FIN3[-1])
        cg, ck = 1.0 - gb / ga, 1.0 - kcb / kca
        print("      dalla prima all'ultima finestra: il gradiente medio cala del %.3f%%, K al centro del %.2f%%: il gradiente spiega il %.2f%% del calo" % (100 * cg, 100 * ck, 100 * cg / ck))
    print("-" * 130)
    print("(ii) e (iii) K PESATA PER FINESTRA CONTRO v, E RISCALATA CON m*(p): p = m*(0) v, R = m*(0)/m*(p), K/R")
    print("-" * 130)
    print("  %5s %12s %13s %10s %10s %9s %9s %9s" % ("scala", "finestra", "v - v(V0)", "p", "m*(p)", "R", "K", "K/R"))
    tutti = []
    for sc in LF.SCALE:
        for w in FIN3:
            v = v_fin(C[sc]["serie"], *w) - v_fin(c0["serie"], *w)
            p = m0 * v
            mp = mstar_p(p, P, D)
            R = m0 / mp
            K, _kc, sK, _g = kp(C[sc], w)
            tutti.append((v, K, K / R))
            print("  x%-4.1f [%4d,%4d] %+13.5e %+10.5f %10.4f %9.5f %+9.4f %+9.4f   (+- %.4f)" % (sc, w[0], w[1], v, p, mp, R, K, K / R, sK))
    T = np.array(tutti)
    o = np.argsort(T[:, 0])
    print("  le tre scale insieme, per v crescente: " + "; ".join("v %+.3e: K %.4f, K/R %.4f" % (T[i, 0], T[i, 1], T[i, 2]) for i in o))
    print("### K/R: da %.4f a %.4f; il massimo scarto da 1: %.4f" % (float(T[:, 2].min()), float(T[:, 2].max()), float(np.max(np.abs(T[:, 2] - 1.0)))))
    print("-" * 130)
    print("(iv) a(V0) PER FINESTRA, DA SOLA (la caduta senza gradiente: l'oggetto del giro 4, N = 1)")
    print("-" * 130)
    for w in ((200, 2000),) + FIN3:
        a0, sa0, nn = CF.fit(c0["serie"], *w)
        print("  [%4d, %4d]: a(V0) %+.4e +- %.1e (%d punti); v(V0) %+.4e" % (w[0], w[1], a0, sa0, nn, v_fin(c0["serie"], *w)))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
