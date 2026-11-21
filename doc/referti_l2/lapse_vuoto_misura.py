# -*- coding: utf-8 -*-
r"""**IL LAPSE DAL VUOTO, SOLO MISURA: LA STRADA (a)** *(il mandato unico di Luca `2026-11-21` `15:07`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `4`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lapse_vuoto_misura.py > doc/referti_l2/lapse_vuoto_misura.txt

**Solo lettura** *(le corse non si toccano)*: gli stati `k 3000` *(C2)*, `15000`, `29000` *(il tronco del ramo `mitosi`, su `E:`)*, lo sha1 controllato; **`1 - N_U`** dal referto della (b) *(`mitosi_lapse_U.txt` nel worktree `mitosi`, lo sha1 dei byte stampato)*.
**La strada (a):** `cs = Lambda / (Lambda + lambda_c)` *(`flussi_parziali.cs`)*; **`lambda_c` UNA volta** dal centro di C2: `lambda_c = Lambda_c (1 - s N(rho)_c) / (s N(rho)_c)`; `s` = la mediana di `cs_prec / N(rho)`; `N(rho) = 1 / (1 + rho / rho_c)`.
**Le definizioni** *(sez. `4.4`)*: `Lambda` da `phi_h`, `rho` da `psi_h`; il centro del tronco; «al centro» = il nodo piu' vicino; `Lambda_lontano` = la media sui nodi con `r >= 85`; il ritmo `pi |cs_i - cs_j|`; il primo quanto `2 pi / ritmo` da `Theta = 0`.
**I casi noti per primi** *(M4)*: `|phi_h|` uniforme -> `Lambda` e `cs` costanti AL BIT; **DEVE CAMBIARE:** un nodo raddoppiato -> non uniformi.
"""
import hashlib
import json
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(_QUI, "..", "..", "csv"), os.path.join(_QUI, "..", "..", "csv", "solitone")):
    if p not in sys.path:
        sys.path.insert(0, p)
L, N0 = 186, 186 * 186
E_ = "E:" + os.sep
STATI = (("C2 k 3000", os.path.join(E_, "soliton_simulator", "controllo", "C2", "stato_03000.npz")),
         ("tronco k 15000", os.path.join(E_, "soliton_simulator", "controllo", "mitosi_rami", "TRONCO", "stato_15000.npz")),
         ("tronco k 29000", os.path.join(E_, "soliton_simulator", "controllo", "mitosi_rami", "TRONCO", "stato_29000.npz")))
F_B = os.path.join("C:" + os.sep, "Users", "lpeano", "wt_mitosi", "doc", "referti_l2", "mitosi_lapse_U.txt")
ANELLI = list(range(0, 31, 2)) + list(range(35, 81, 5))
R_LONTANO, CONFINE = 85.0, 23.81


def sha1b(f):
    with open(f, "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()


def toro():
    v = np.arange(N0)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    ii = np.repeat(v, 3)
    jj = np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1)
    return ii, jj, m1.astype(float), m2.astype(float)


def raggi(m1, m2, c):
    from solitone import toro as TO
    S = TO.scarti(m1, m2, c[0], c[1], L)
    return np.hypot(S[:, 0], S[:, 1])


def mezzo(m1, m2, i, j):
    d1 = ((m1[j] - m1[i] + 0.5 * L) % L) - 0.5 * L
    d2 = ((m2[j] - m2[i] + 0.5 * L) % L) - 0.5 * L
    return (m1[i] + 0.5 * d1) % L, (m2[i] + 0.5 * d2) % L


def per_nodo(nodo, valori_h):
    return np.bincount(nodo, weights=valori_h, minlength=N0)


def leggi(f, nodo):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1b(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        psi_h, phi_h, cs, meta = d["psi_h"], d["phi_h"], d["cs_prec"].copy(), json.loads(str(d["meta"]))
    return int(meta["k"]), per_nodo(nodo, np.sum(np.abs(psi_h) ** 2, axis=1)), per_nodo(nodo, np.abs(phi_h) ** 2), cs, meta


def anello(r, y, R):
    w = (r >= R - 0.5) & (r < R + 0.5)
    return float(y[w].mean()) if w.any() else math.nan


def nu_dalla_b():
    """### `1 - N_U` per anello dei tre stati, LETTO dal referto della (b): `{indice dello stato: {r: valore}}`."""
    out, i = {}, -1
    with open(F_B, encoding="utf-8") as fh:
        for riga in fh:
            if riga.startswith("### C2 k 3000") or riga.startswith("### tronco k"):
                i += 1
                out[i] = {}
            m = re.match(r"^\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$", riga)
            if m and i >= 0:
                out[i][int(m.group(1))] = float(m.group(4))
    return out


def main():
    import _presidio
    _presidio.avvia(__file__)
    import mattone as MT
    rho_c = MT.rho_c_assoluto()
    ii, jj, m1, m2 = toro()
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    print("=" * 160)
    print("IL LAPSE DAL VUOTO, SOLO MISURA: LA STRADA (a) (Luca 2026-11-21 15:07; il task history del ramo lapse-u, sez. 4)")
    print("=" * 160)
    # ---------------------------------------------------------------- M4: I CASI NOTI, per primi
    ph = np.full(2 * len(ii), 0.7 * np.exp(0.3j))
    lu = per_nodo(nodo, np.abs(ph) ** 2)
    csu = lu / (lu + 3.21)
    ph2 = ph.copy()
    ph2[nodo == 17204] *= 2.0
    l2 = per_nodo(nodo, np.abs(ph2) ** 2)
    cs2 = l2 / (l2 + 3.21)
    noto = bool(np.all(lu == lu[0]) and np.all(csu == csu[0]))
    cambia = bool(not np.all(l2 == l2[0]) and not np.all(cs2 == cs2[0]))
    print("### M4 IL CASO NOTO (|phi_h| uniforme sul toro): Lambda uniforme %s, cs costante %s -> %s; DEVE CAMBIARE (un nodo raddoppiato): Lambda %d valori, cs %d valori -> %s" % (
        bool(np.all(lu == lu[0])), bool(np.all(csu == csu[0])), "AL BIT" if noto else "NON AL BIT: FERMO", len(np.unique(l2)), len(np.unique(cs2)), "CAMBIA" if cambia else "NON CAMBIA: FERMO"))
    if not (noto and cambia):
        return 1
    NU = nu_dalla_b()
    print("### la (b): %s, sha1 dei byte %s (il commit e29a165d del ramo mitosi); %d stati letti" % (F_B, sha1b(F_B)[:8], len(NU)))
    lam_c = None
    for idx, (nome, f) in enumerate(STATI):
        k, rho, lam, csp, meta = leggi(f, nodo)
        if idx == 0:
            with np.load(STATI[-1][1]) as d:
                centro = [float(c) for c in json.loads(str(d["meta"]))["centro"]]
            r = raggi(m1, m2, centro)
            c0 = int(np.argmin(r))
            x1, x2 = mezzo(m1, m2, ii, jj)
            ra = raggi(x1, x2, centro)
        Nr = 1.0 / (1.0 + rho / rho_c)
        s = float(np.median(csp / Nr))
        if lam_c is None:
            lam_c = lam[c0] * (1.0 - s * Nr[c0]) / (s * Nr[c0])
            print("### lambda_c (UNA volta, dal centro di C2 a k 3000, il nodo %d, r %.4f): Lambda al centro %.10e, N(rho) al centro %.10e, s %.12f -> lambda_c %.10e (DERIVATO)" % (
                c0, r[c0], lam[c0], Nr[c0], s, lam_c))
        cs = lam / (lam + lam_c)
        ll = float(lam[r >= R_LONTANO].mean())
        dv = 1.0 - lam / ll
        dcs = 1.0 - cs / s
        rit = math.pi * np.abs(cs[ii] - cs[jj])
        print("-" * 160)
        print("### %s (k %d): Lambda al centro %.10e, Lambda_lontano (r >= %.0f, %d nodi) %.10e; cs al centro %.10e, cs/s lontano %.10f" % (
            nome, k, lam[c0], R_LONTANO, int(np.sum(r >= R_LONTANO)), ll, cs[c0], float(cs[r >= R_LONTANO].mean()) / s))
        print("    ### M3 IL SEGNO: Lambda al centro %s Lambda_lontano -> cs(Lambda) al centro %s quello lontano: %s" % (
            "<" if lam[c0] < ll else ">=", "<" if cs[c0] < float(cs[r >= R_LONTANO].mean()) else ">=", "PIU' BASSO sul mattone (il segno delle prove G+U)" if lam[c0] < ll else "NON piu' basso: il segno SBAGLIATO"))
        print("    il profilo per anello (r euclideo; i ritmi degli archi col punto medio nell'anello, 1e-4 per tick; 1 - N_U dalla b):")
        print("      r    1 - L/L_lontano     1 - cs/s (a)      1 - N(rho)        1 - N_U (b)     ritmo (a)   ritmo N(rho)")
        dv0, nr0 = dv[c0], 1.0 - Nr[c0]
        for R in ANELLI:
            v_dv = dv0 if R == 0 else anello(r, dv, R)
            v_cs = dcs[c0] if R == 0 else anello(r, dcs, R)
            v_nr = nr0 if R == 0 else anello(r, 1.0 - Nr, R)
            print("    %3d   %14.6e   %14.6e   %14.6e   %14.6e    %10.4f   %10.4f" % (
                R, v_dv, v_cs, v_nr, NU.get(idx, {}).get(R, math.nan), anello(ra, rit, R) * 1e4, anello(ra, math.pi * np.abs(csp[ii] - csp[jj]), R) * 1e4))
        a = int(np.argmax(rit))
        with np.errstate(divide="ignore"):
            T = 2.0 * math.pi / rit
        print("    ### M2 (a): il ritmo massimo %.4e per tick all'arco %d (r %.2f); il primo a 2 pi da Theta = 0 a %.0f tick; oltre r %.2f: entro 1e5 tick %d archi, entro 1e6 %d archi (il primo oltre il confine a %.0f tick, r %.2f)" % (
            rit[a], a, ra[a], T[a], CONFINE, int(np.sum((ra > CONFINE) & (T <= 1e5))), int(np.sum((ra > CONFINE) & (T <= 1e6))),
            float(T[ra > CONFINE].min()), float(ra[ra > CONFINE][np.argmin(T[ra > CONFINE])])))
        q40, q60 = anello(r, dv, 40) / dv0, anello(r, dv, 60) / dv0
        print("    ### LE PREVISIONI su questo stato: P-L1 (il vuoto depresso sul mattone): %s; P-L2 (1 - L/L_lontano all'anello 40 sopra 1e-3 del centro): %.3e -> %s; P-L3 (all'anello 60 sotto il 10%% del centro): %.4f -> %s; P-L4 (un arco oltre 23.81 a 2 pi entro 1e6): %s" % (
            "VERA" if lam[c0] < ll else "FALSA", q40, "VERA" if q40 > 1e-3 else "FALSA", q60, "VERA" if q60 < 0.1 else "FALSA",
            "VERA" if int(np.sum((ra > CONFINE) & (T <= 1e6))) > 0 else "FALSA"))
    print("=" * 160)
    return 0


if __name__ == "__main__":
    sys.exit(main())
