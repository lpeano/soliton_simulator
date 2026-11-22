# -*- coding: utf-8 -*-
r"""**[M1446-L] LA LEGGE DELLA CADUTA -- LA V2** *(la versione nuova del mandato [M1446], la carta sez. `1`: in piu' le `K` DALLO ZERO di ciascuna forma, `K0_i = a_i/(c^2 |grad N|)` contro `K0_th = Delta_i/(|m*| c^2)`, `Delta_i = |d omega/dN|_i`; e lo zero di V4, `omega(1) (1 - rapporto)`, contro `-e0`; il resto la v1 riga per riga)*. **IL TITOLO DELLA V1: LA LEGGE DELLA CADUTA: K_i = (a_i/(c^2 |grad N|)) / (d ln omega/dN)_i** *(il mandato di Luca [M1446], corsia L; la carta `doc/CARTA_E_mc2.md`, sez. `L`; SOLA LETTURA dei referti; POST-HOC, dichiarato)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/legge_caduta_v2.py > doc/referti_l2/legge_caduta.txt

**Letti, non ricopiati:** `a/(c^2 |dN/dy|)` per `c_m` e `s` e il verso da `caduta_libera.txt` *(positivo = VIA)*; `(q - 1)/(N - 1)` = `d ln omega/dN` da `orologio_mattone.txt` *(V1 da `Nm`, V2 da `NmV2`, V3 da `NmV3`)* e, se c'e', da `orologio_V4.txt` *(V4; se no RICAVATO = V2 - V3, dichiarato)*; `omega(N1)`; `m*` da `massa_calcio.txt` *(il solitone)* se c'e', da `spettro_gap.txt` *(la banda)* se c'e', se no da `s5_caduta_segno.txt` *(T-L4b, la banda)*. **K3:** le `K_i` entro il `10%`; la media contro `K_th = omega/(|m*| c^2)` entro il `20%`.
"""
import hashlib
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402,F401  (i percorsi)

C = {"c_m = 0.588 s": 0.588 * 0.15, "c = s": 0.15}


def testo(nome):
    f = os.path.join(_QUI, nome)
    if not os.path.exists(f):
        return None
    print("### %s (sha1 %s)" % (nome, hashlib.sha1(open(f, "rb").read()).hexdigest()[:8]))
    return open(f, encoding="utf-8", errors="replace").read()


def main():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1446-L] LA LEGGE DELLA CADUTA (la carta sez. L; POST-HOC, dichiarato)")
    print("=" * 130)
    cad = testo("caduta_libera.txt")
    a = {}
    for v in ("V1", "V2", "V3", "V4"):
        m = re.search(r"^\s+%s\s+il baricentro\s+.*?: (VERSO|VIA) .*?\|a - a\(V0\)\| / \(c\^2 \|dN/dy\|\) = ([0-9.]+) \(c = 0\.588 s\), ([0-9.]+) \(c = s\)" % v, cad, re.M)
        sg = 1.0 if m.group(1) == "VIA" else -1.0
        a[v] = {"c_m = 0.588 s": sg * float(m.group(2)), "c = s": sg * float(m.group(3))}
    oro = testo("orologio_mattone.txt")
    q = {}
    for v, var in (("V1", "Nm"), ("V2", "NmV2"), ("V3", "NmV3")):
        q[v] = float(re.search(r"^\s+%s\s+N [0-9.]+: q = .*?\(il rapporto ([-+0-9.]+)\)" % var, oro, re.M).group(1))
    w = float(re.search(r"^\s+N1\s+omega ([0-9.]+)", oro, re.M).group(1))
    o4 = testo("orologio_V4.txt")
    m4 = re.search(r"^\s+V4Nm\s+N [0-9.]+: q = .*?\(il rapporto ([-+0-9.]+)\)", o4, re.M) if o4 else None
    if m4:
        q["V4"], v4 = float(m4.group(1)), "misurato (orologio_V4.txt)"
    else:
        q["V4"], v4 = q["V2"] - q["V3"], "RICAVATO = V2 - V3 (l'orologio V4 non c'e' ancora)"
    print("### d ln omega/dN: %s; V4 %s; omega(N1) %.10f" % (", ".join("%s %+.3f" % (k, x) for k, x in q.items()), v4, w))
    ms, fonte = None, None
    mc = testo("massa_calcio.txt")
    if mc:
        mm = re.search(r"m\*_sol: .*; la media ([-+0-9.]+)", mc)
        if mm:
            ms, fonte = float(mm.group(1)), "m*_sol (massa_calcio.txt)"
    if ms is None:
        sp = testo("spettro_gap.txt")
        mm = re.search(r"m\*_banda = 1/\(d2E/dk2\) ([-+0-9.]+)", sp) if sp else None
        if mm:
            ms, fonte = float(mm.group(1)), "m*_banda (spettro_gap.txt)"
    if ms is None:
        t4 = testo("s5_caduta_segno.txt")
        d2 = float(re.search(r"la banda 0: .*?d2 eps/dk2 ([-+0-9.e]+)", t4).group(1))
        ms, fonte = 1.0 / d2, "m*_banda di T-L4b (s5_caduta_segno.txt)"
    print("### m* = %+.4f (%s)" % (ms, fonte))
    print("-" * 130)
    for nome, c in C.items():
        K = {v: a[v][nome] / q[v] for v in a}
        km = float(np.mean(list(K.values())))
        sp_ = (max(K.values()) - min(K.values())) / abs(km)
        Kth = w / (abs(ms) * c * c)
        print("  %s: K_i %s; la media %+.3f, la dispersione (max - min)/|media| %.3f (K3: entro il 10%% %s); K_th = omega/(|m*| c^2) %.3f: la media/K_th %.3f (K3: entro il 20%% %s)" % (
            nome, ", ".join("%s %+.3f" % (v, x) for v, x in K.items()), km, sp_, "SI'" if sp_ <= 0.10 else "NO", Kth, km / Kth, "SI'" if abs(km / Kth - 1.0) <= 0.2 else "NO"))
    print("  (in natura lo stesso numero e' -1: E = m c^2)")
    print("-" * 130)
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    z4 = w * (1.0 - q["V4"])
    print("  LO ZERO DI V4: omega(1) (1 - rapporto) = %+.6f (il rapporto %s) contro -e0 = %+.6f: lo scarto %+.3e" % (z4, v4, -e0, z4 + e0))
    print("  DALLO ZERO DI CIASCUNA FORMA (d ln|omega - omega0|/dN = 1 per costruzione): K0_i = a_i/(c^2 |grad N|) col segno; K0_th = Delta_i/(|m*| c^2), Delta_i = |d omega/dN|_i = |rapporto_i| omega(1)")
    for nome, c in C.items():
        out = []
        for v in a:
            D = abs(q[v]) * w
            K0, K0th = a[v][nome], D / (abs(ms) * c * c)
            out.append("%s K0 %+.3f, K0_th %.3f (Delta %.5f): il rapporto %+.3f" % (v, K0, K0th, D, K0 / K0th))
        print("  %s: %s" % (nome, "; ".join(out)))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
