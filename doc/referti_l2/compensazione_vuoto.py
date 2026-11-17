# -*- coding: utf-8 -*-
r"""**A3: QUANTO PUO' TOGLIERE UNA OPERAZIONE LOCALE SUL VUOTO CHE CONSERVA LA NORMA** *(Luca `2026-11-17` `16:38`, D-R3; la carta `doc/TASK_HISTORY/2026-11-17_mitosi_verso_il_test.md`, sez. `1`)*.

    E:\python\py3132\python.exe doc/referti_l2/compensazione_vuoto.py > doc/referti_l2/compensazione_vuoto.txt

**L'energia del vuoto** *(`energia_pesata.termini_di_h`, le parti di `phi`: il codice)* **e' una forma QUADRATICA esatta:** `H_v = phi^dag Q phi`, `Q = -Omega/2 I + Omega sum_v (1/d_v) 1_v 1_v^T + Omega/2 sum_a (E_{2a,2a+1} + E_{2a+1,2a})` *(reale)*. **Con le estremita' fuori da un insieme `S` fisse e la norma su `S` fissata, il MINIMO di `H_v` e' un problema sulla sfera** *(`_conto_del_vuoto.estremi_sfera`)*: **e' il massimo che QUALUNQUE operazione su `S` che conserva la norma** *(una rotazione di fase compresa)* **puo' togliere.**
**Per la nascita** *(la divisione generica; le fasi FA e v4-F3 di `regole_fase_F3.py`)*: `S1` = le estremita' dei nodi di `S` *(la mossa e i vicini a un passo)*, `S2`, `S3` a due e tre passi; **`Delta H_v` dopo la nascita e il minimo raggiungibile, contro `Delta H_v = 0`** *(il costo tolto tutto)*.
**Il caso noto:** sul vuoto F3 SENZA nascita il minimo su `S` a norma fissata = F3 stesso *(F3 e' il minimo locale: la differenza `0` all'arrotondamento)*; e `H_v` dalla forma `Q` = le famiglie di `nascita_dentro_fuori.famiglie` *(`G_phi + a_phi`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
_PO = os.path.join(_RADICE, "primo_ordine")
for _p in (_QUI, _SOL, _CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import nascita_dentro_fuori as ND  # noqa: E402
import regole_fase_F3 as RF  # noqa: E402


def Hv(G, phi):
    import energia_pesata as EP
    ii, jj, nn, _v = G
    Om = EP.OMEGA_H
    nodo = ND.nodo_h(ii, jj)
    S = np.zeros(nn, dtype=complex)
    np.add.at(S, nodo, phi)
    d = np.bincount(nodo, minlength=nn).astype(float)
    nrm = np.zeros(nn)
    np.add.at(nrm, nodo, np.abs(phi) ** 2)
    f = phi.reshape(len(ii), 2)
    return float(np.sum(-Om * (0.5 * nrm - np.abs(S) ** 2 / d))) + float(np.sum(Om * np.real(np.conj(f[:, 0]) * f[:, 1])))


def vicini_k(ii, jj, semi, k):
    S = set(semi)
    for _ in range(k):
        nuovo = set(S)
        for a, b in zip(ii.tolist(), jj.tolist()):
            if a in S:
                nuovo.add(b)
            if b in S:
                nuovo.add(a)
        S = nuovo
    return sorted(S)


def minimo(G, phi, nodiS):
    """### il minimo di `H_v` sulle estremita' dei nodi `nodiS` a norma fissata, il resto fisso: `(H_v attuale, H_v minimo)`."""
    import _conto_del_vuoto as C3
    import energia_pesata as EP
    ii, jj, nn, _v = G
    Om = EP.OMEGA_H
    nodo = ND.nodo_h(ii, jj)
    hS = np.where(np.isin(nodo, nodiS))[0]
    pos = {int(h): q for q, h in enumerate(hS)}
    m = len(hS)
    d = np.bincount(nodo, minlength=nn).astype(float)
    Q = np.zeros((m, m))
    for q, h in enumerate(hS):
        Q[q, q] += -0.5 * Om
    for v in nodiS:
        hv = [pos[int(h)] for h in np.where(nodo == v)[0]]
        for p in hv:
            for r in hv:
                Q[p, r] += Om / d[v]
    b = np.zeros(m, dtype=complex)
    for q, h in enumerate(hS):
        c = int(h) ^ 1
        if c in pos:
            Q[q, pos[c]] += 0.5 * Om
        else:
            b[q] += 0.5 * Om * phi[c]
    x0 = phi[hS]
    N = float(np.sum(np.abs(x0) ** 2))
    A = np.block([[Q, np.zeros_like(Q)], [np.zeros_like(Q), Q]])
    bb = np.concatenate([np.real(b), np.imag(b)])
    y0 = np.concatenate([np.real(x0), np.imag(x0)])
    fmin, _xmin, _fmax, _xmax, _l0, _l1 = C3.estremi_sfera(A, bb, N)
    f0 = float(y0 @ A @ y0 + 2.0 * bb @ y0)
    H0 = Hv(G, phi)
    return H0, H0 - f0 + fmin


def main():
    import _presidio
    import _massa_nei_difetti as MD
    import mattone as MT
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "regole_fase_F3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("A3: QUANTO PUO' TOGLIERE UNA OPERAZIONE LOCALE SUL VUOTO CHE CONSERVA LA NORMA (Luca 2026-11-17 16:38, D-R3)")
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        ii, jj, nn, dirs = MD.toro(L)
        phi_v = np.asarray(Z["phi_v"]).copy()
    with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
        psi_m, phi_m = d["psi_h"].copy(), d["phi_h"].copy()
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    esiti = []
    # ---------------------------------------------------------------- i casi noti
    F = ND.famiglie(G, np.zeros_like(psi_m), phi_v)
    h = Hv(G, phi_v)
    print("### il caso noto (1): H_v dalla forma Q %.9e contro G_phi + a_phi di nascita_dentro_fuori.famiglie %.9e (la differenza relativa %.1e)" % (h, F["G_phi"] + F["a_phi"], abs(h - F["G_phi"] - F["a_phi"]) / abs(h)))
    esiti.append(("il caso noto (1): la forma Q = le famiglie del vuoto entro 1e-12", abs(h - F["G_phi"] - F["a_phi"]) / abs(h) < 1e-12))
    c = 81 * L + 81
    for k in (1, 2):
        H0, Hm = minimo(G, phi_v, vicini_k(ii, jj, [c], k))
        print("### il caso noto (2): il vuoto F3 SENZA nascita, il minimo su S a %d passi dal nodo (81, 81): H_v %.9e, il minimo %.9e, la differenza %.3e" % (k, H0, Hm, Hm - H0))
        esiti.append(("il caso noto (2): F3 e' gia' il minimo a %d passi (la differenza entro 1e-9)" % k, abs(Hm - H0) < 1e-9))
    # ---------------------------------------------------------------- la nascita
    v = np.arange(nn)
    m1, m2 = (v // L).astype(float), (v % L).astype(float)
    rho = np.zeros(nn)
    np.add.at(rho, ND.nodo_h(ii, jj), np.abs(psi_m[:, 0]) ** 2 + np.abs(psi_m[:, 1]) ** 2)
    cb = TO.centro(rho, m1, m2, L)[:2]
    D = TO.scarti(m1, m2, cb[0], cb[1], L)
    th = np.arctan2(D[:, 1], D[:, 0])
    rm = np.hypot(D[:, 0] + 0.5, D[:, 1])
    i60 = int(np.argmin(np.abs(rm - 60.0) + 10.0 * np.abs(th)))
    casi = (("il vuoto F3 puro", np.zeros_like(psi_m), phi_v, 3 * c), ("il mattone, l'arco a %.2f nodi" % rm[i60], psi_m, phi_m, 3 * i60))
    for nome_c, psi, phi, a in casi:
        print("-" * 130)
        print("### %s" % nome_c)
        Hb = Hv(G, phi)
        for regola in ("FA", "v4-F3"):
            Dl, out = RF.nascita(G, psi, phi, a, regola)
            if Dl is None:
                print("    %-6s INDEFINITA" % regola)
                continue
            with np.errstate(invalid="ignore", divide="ignore"):
                ph = RF.regola(regola, G, phi, a, out)
            G2 = out[0]
            n = out[3]["n"]
            dHv = Hv(G2, ph) - Hb
            riga = "    %-6s dH totale %+.6e, dH del vuoto %+.6e;" % (regola, Dl["tot"], dHv)
            for k in (1, 2, 3):
                _H0, Hm = minimo(G2, ph, vicini_k(G2[0], G2[1], [n], k))
                riga += "  S a %d passi: il minimo di dH del vuoto %+.6e (tolto %.4e, il %.1f%%)" % (k, Hm - Hb, dHv - (Hm - Hb), 100.0 * (dHv - (Hm - Hb)) / dHv)
            print(riga)
            sys.stdout.flush()
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
