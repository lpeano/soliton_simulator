# -*- coding: utf-8 -*-
r"""**[M0118-02] K A PARITA' DI MASSA, FORMA DIVERSA** *(DECISIONE DI LUCA, 2026-11-24 01:17; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-decies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/k_forma.py caduta --coll V2          (coll V0, V2: 2000 tick, gli stati ogni 250)
    E:\python\py3132\python.exe doc/referti_l2/k_forma.py calcio --k 0.010         (k 0.0, 0.010: per m*, mia aggiunta dichiarata)
    E:\python\py3132\python.exe doc/referti_l2/k_forma.py lettura > doc/referti_l2/k_forma.txt

**`fondo_1c.caduta` e `fondo_1c.calcio` cosi' come sono**, con `fondo_1c.OGGETTO` = `M1658/tenuta_v2/L-1_a1.0_l0.7/stato_003000.npz` e `fondo_1c.BASE` = `M1658/c1_l07`, in memoria; **nella caduta `fondo_1c.ciclo` avvolta** *(dopo il `dopo` di `caduta`, lo stato ogni `250` e a `k 0`: legge e salva, non tocca)*. **La lettura:** `m*`, `K` sull'intera `[200, 2000]` e a finestre di `600` per 1c, a2, l0.7; per l0.7 `K` anche con `m*(1c)`; le eta a due a due.
"""
import argparse
import hashlib
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import eotvos_fondo as EF  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658")
OGG_L07 = os.path.join(CTRL, "tenuta_v2", "L-1_a1.0_l0.7", "stato_003000.npz")
BASE_L07 = os.path.join(CTRL, "c1_l07")
BASE_1C, BASE_A2 = EF.BASE_1C, EF.BASE_A2
FINESTRE = ((200, 800), (800, 1400), (1400, 2000))
OGNI_STATO = 250


def su_l07():
    F1.OGGETTO = OGG_L07
    F1.BASE = BASE_L07


def con_stati(coll):
    CAT = {}
    vero_carica, vero_ciclo = F1.FS.carica, F1.ciclo

    def carica(Z, *a):
        r = vero_carica(Z, *a)
        CAT["info"] = r[1]
        return r

    def ciclo(Z, C, quanti, dopo, MV, P0, N, cs_N, segno):
        d = os.path.join(F1.BASE, "caduta_%s" % coll)
        assert not os.path.exists(d), "%s c'e' gia': non si riscrive" % d
        os.makedirs(d)

        def salva(kk):
            fz = os.path.join(d, "stato_%06d.npz" % kk)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.savez(fz, meta=np.array(json.dumps(dict(CAT["info"], k=kk, coll=coll))), **dati)
            h = hashlib.sha1(open(fz, "rb").read()).hexdigest()
            open(fz + ".sha1", "w", encoding="utf-8").write(h + "\n")
            print("    [stato] k %d sha1 %s" % (kk, h[:8]))
            sys.stdout.flush()

        def dopo2(kk, prima):
            dopo(kk, prima)
            if kk % OGNI_STATO == 0:
                salva(kk)
        salva(0)
        vero_ciclo(Z, C, quanti, dopo2, MV, P0, N, cs_N, segno)
    F1.FS.carica = carica
    F1.ciclo = ciclo


def legge(base):
    """### `(m*, s_m*, serie V2, serie V0, A)` o `None`."""
    ms = EF.mstar_K(base)
    F1.BASE = base
    c, c0 = F1.leggi("caduta_V2"), F1.leggi("caduta_V0")
    if ms is None or c is None or c0 is None:
        return None
    return ms[0], ms[1], c["serie"], c0["serie"], float(c["A"])


def lettura():
    import _presidio
    import caduta_finestre as CF
    import chi_parametri_v2 as CP2
    F1.avvia()
    for m in ("eotvos_fondo.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0118-02] K A PARITA' DI MASSA, FORMA DIVERSA (la carta sez. 2-decies): 1c, a2 (norma x4), l0.7 (larghezza 0.7)")
    print("=" * 130)
    F1.BASE = BASE_1C
    D = {}
    for Nv in (0.9965, 1.0035):
        x = F1.leggi("orologio_V2_N%.4f" % Nv)
        D[Nv] = float((np.array(x["omega"]) - np.array(x["omega_phi"])).mean())
    dw_dN = (D[1.0035] - D[0.9965]) / 0.007
    Ly = 162 * math.sqrt(3.0) / 2.0
    R = {}
    for nome, base in (("1c", BASE_1C), ("a2", BASE_A2), ("l0.7", BASE_L07)):
        x = legge(base)
        if x is None:
            print("  %s: NON FINITA" % nome)
            continue
        ms, sms, s2, s0, A = x
        gw = dw_dN * (-CP2.KAPPA * A * 2.0 * math.pi / Ly)
        a, sa, _n = CF.fit(s2, 200, 2000)
        a0, sa0, _n0 = CF.fit(s0, 200, 2000)
        da, sda = a - a0, math.hypot(sa, sa0)
        K = da / (-gw / ms)
        sK = abs(K) * math.hypot(sda / da, sms / ms)
        R[nome] = dict(ms=ms, sms=sms, da=da, sda=sda, K=K, sK=sK, gw=gw, s2=s2, s0=s0)
        print("  %-5s m* %+.4f +- %.4f; [200, 2000] a - a(V0) %+.4e +- %.1e; K %+.4f +- %.4f" % (nome, ms, sms, da, sda, K, sK))
        for w in FINESTRE:
            aw, saw, _ = CF.fit(s2, *w)
            a0w, sa0w, _ = CF.fit(s0, *w)
            dw, sdw = aw - a0w, math.hypot(saw, sa0w)
            Kw = dw / (-gw / ms)
            print("        [%4d, %4d] a - a(V0) %+.4e +- %.1e; K %+.4f +- %.4f" % (w[0], w[1], dw, sdw, Kw, abs(Kw) * math.hypot(sdw / dw, sms / ms)))
    if "l0.7" in R and "1c" in R:
        r, r1 = R["l0.7"], R["1c"]
        K1 = r["da"] / (-r["gw"] / r1["ms"])
        print("### l0.7 con m*(1c) (a parita' di massa, la lettura di Luca): K %+.4f; con m*(l0.7) %+.4f; K(1c) %+.4f; K(l0.7)/K(1c): %.4f (m* proprio), %.4f (m* di 1c)" % (
            K1, r["K"], r1["K"], r["K"] / r1["K"], K1 / r1["K"]))
    nomi = [x for x in ("1c", "a2", "l0.7") if x in R]
    for i in range(len(nomi)):
        for j in range(i + 1, len(nomi)):
            p, q = R[nomi[i]], R[nomi[j]]
            eta = 2.0 * abs(p["da"] - q["da"]) / (p["da"] + q["da"])
            se = 4.0 * math.hypot(q["da"] * p["sda"], p["da"] * q["sda"]) / (p["da"] + q["da"]) ** 2
            print("### eta(%s, %s) = %.4f +- %.4f" % (nomi[i], nomi[j], eta, se))
    print("=" * 130)
    return 0


def main(argv):
    import _presidio
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("caduta", "calcio", "lettura"))
    ap.add_argument("--coll", choices=("V0", "V2"))
    ap.add_argument("--k", type=float)
    a = ap.parse_args(argv)
    if a.cosa == "lettura":
        return lettura()
    su_l07()
    _presidio.avvia(__file__)
    if a.cosa == "caduta":
        con_stati(a.coll)
        return F1.caduta(a.coll)
    return F1.calcio(a.k)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
