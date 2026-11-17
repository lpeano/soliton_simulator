# -*- coding: utf-8 -*-
r"""**LA LETTURA PER LA SOGLIA DELLA NASCITA** *(Luca `2026-11-17` `13:16`, parte 4; SOLA LETTURA; la carta `doc/TASK_HISTORY/2026-11-17_CPT_F3_soglia.md`, sez. `2.4`)*.

    E:\python\py3132\python.exe doc/referti_l2/soglia_nascita.py > doc/referti_l2/soglia_nascita.txt

**I termini di H** *(`primo_ordine/energia_pesata.termini_di_h`, letti nel codice)*: **nodo** `-Omega (0.5 nrm_psi - |S_psi|^2/d) - Omega (0.5 nrm_phi - |S_phi|^2/d) + eps h + N(rho, Lambda)`; **arco** `Omega Re(incro_psi) + Omega Re(conj(phi_coda) phi_testa)`.
**4.1 IL SEGNO:** le famiglie di termini, sommate e per segno, sul vuoto F3 puro della scena S162 *(`psi = 0`)* e sul mattone `L162_MGU_03000` *(il motore, la geometria e il `par` della scena)*.
**4.2 LA TENSIONE D'ARCO** *(la definizione, SCELTA MIA, dichiarata)*: `T(a) = Omega Re(conj(phi_coda) phi_testa)`, **il termine D'ARCO del vuoto di `termini_di_h`**; sul vuoto F3 puro; il profilo per anello `0`-`60` attorno al mattone, al triangolo *(`legati_t120_03000.npz`)* e alla coppia *(`legati_GU_*.npz` se c'e')*.
**4.3 TRE CANDIDATE PER IL «CALORE» `Q(a)`:** **Q1** `T(a) - T_F3` *(la tensione sopra il vuoto puro)*; **Q2** l'energia del vuoto per nodo, la media sui due nodi dell'arco, sopra il fondo F3; **Q3** `|J(a)|`, la corrente di energia sull'arco *(`energia.corrente`)*; per ognuna: il valore nel vuoto puro, il profilo, e **QUANTI ARCHI superano il costo `C`** *(una SCELTA mia per dare un ordine di grandezza: `C = 26.11`, il `Delta H` di v4-F3 all'anello `60`, `divisione_vuoto_F3.txt`)*.
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
for _p in (_SOL, _CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

COSTO = 26.11            # divisione_vuoto_F3.txt, (c) v4-F3, l'anello 60: una scelta per l'ordine di grandezza (la carta)
ANELLI = (0, 5, 10, 13, 14, 15, 20, 25, 30, 40, 50, 60)


def main():
    import _presidio
    import energia as EN
    import energia_pesata as EP
    import materia_vuoto as MV
    import mattone as MT
    from solitone import toro as TO
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA LETTURA PER LA SOGLIA DELLA NASCITA (Luca 2026-11-17 13:16, parte 4); sola lettura; OMEGA_H %r" % EP.OMEGA_H)
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        mot, par = Z["mot"], Z["par"]
        inc = mot.inc
        nodo = np.asarray(inc.nodo)
        ii, jj = np.asarray(inc.ii), np.asarray(inc.jj)
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        phi_v = np.asarray(Z["phi_v"]).copy()
        stati = {"il vuoto F3 puro (psi = 0)": (np.zeros((len(nodo), 2), dtype=complex), phi_v)}
        for nome, f in (("il mattone L162_MGU_03000", "L162_MGU_03000.npz"), ("il triangolo legati_t120_03000", "legati_t120_03000.npz"), ("la coppia legati_GU_06000", "legati_GU_06000.npz")):
            p = os.path.join(MT.DIR_E, f)
            if os.path.exists(p):
                with np.load(p) as d:
                    stati[nome] = (d["psi_h"].copy(), d["phi_h"].copy())
            else:
                print("### %s: %s NON c'e' su E: (saltato)" % (nome, p))

        def termini(psi, phi):
            st = dict(Z["st"])
            st["psi_h"], st["phi_h"] = psi, phi
            st["h_int"] = np.zeros(n)
            Om = EP.OMEGA_H
            nrm_psi = np.zeros(n); np.add.at(nrm_psi, nodo, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2)
            nrm_phi = np.zeros(n); np.add.at(nrm_phi, nodo, np.abs(phi) ** 2)
            S_psi = np.zeros((n, 2), dtype=complex); np.add.at(S_psi, nodo, psi)
            S_phi = np.zeros(n, dtype=complex); np.add.at(S_phi, nodo, phi)
            d = np.asarray(inc.grado, dtype=float)
            g_psi = -Om * (0.5 * nrm_psi - (np.abs(S_psi[:, 0]) ** 2 + np.abs(S_psi[:, 1]) ** 2) / d)
            g_phi = -Om * (0.5 * nrm_phi - np.abs(S_phi) ** 2 / d)
            h = mot.elicita(st)
            mon = float(par.get("eps")) * h
            Nn = MV.N(nrm_psi, nrm_phi)
            U = mot.geo.U
            w = psi.reshape(len(ii), 2, 2)
            a_psi = Om * np.real(np.einsum("ai,aji,aj->a", np.conj(w[:, 0, :]), np.conj(U), w[:, 1, :]))
            f = phi.reshape(len(ii), 2)
            a_phi = Om * np.real(np.conj(f[:, 0]) * f[:, 1])
            pn, pa = EP.termini_di_h(mot, st, par)
            ctrl = max(float(np.max(np.abs(pn - (g_psi + g_phi + mon + Nn)))), float(np.max(np.abs(pa - (a_psi + a_phi)))))
            return {"Grover nodo psi": g_psi, "Grover nodo phi": g_phi, "moneta": mon, "N (materia-vuoto)": Nn, "arco psi": a_psi, "arco phi (la tensione)": a_phi}, ctrl, nrm_psi, st

        # ---------------------------------------------------------------- 4.1
        print("### 4.1 IL SEGNO: le famiglie di termini (la somma; quanto ne e' negativo); il controllo: la ricostruzione contro termini_di_h")
        R = {}
        for nome, (psi, phi) in stati.items():
            T, ctrl, rho, st = termini(psi, phi)
            R[nome] = (T, rho, psi, phi, st)
            print("    %s (la ricostruzione contro termini_di_h: %.1e):" % (nome, ctrl))
            for k, x in T.items():
                print("        %-24s la somma %+.6e   (la parte negativa %+.6e, la positiva %+.6e)" % (k, float(x.sum()), float(x[x < 0].sum()), float(x[x > 0].sum())))
            print("        %-24s %+.6e" % ("IL TOTALE", float(sum(float(x.sum()) for x in T.values()))))
        # ---------------------------------------------------------------- 4.2 e 4.3
        T0 = R["il vuoto F3 puro (psi = 0)"][0]["arco phi (la tensione)"]
        print("-" * 130)
        print("### 4.2 LA TENSIONE D'ARCO T(a) = Omega Re(conj(phi_coda) phi_testa): sul vuoto F3 puro da %+.9e a %+.9e (la media %+.9e)" % (float(T0.min()), float(T0.max()), float(T0.mean())))
        Tf3 = float(np.median(T0))
        vn0 = R["il vuoto F3 puro (psi = 0)"][0]["Grover nodo phi"]
        vf3 = float(np.median(vn0))
        print("    il fondo F3: T_F3 = %+.9e (la mediana); l'energia del vuoto per nodo (Grover nodo phi) %+.9e" % (Tf3, vf3))
        for nome, (T, rho, psi, phi, st) in R.items():
            cb = TO.centro(rho, m1, m2, L)[:2] if rho.sum() > 0 else (L / 2.0, L / 2.0)
            mi_ = 0.5 * (TO.scarti(m1[ii], m2[ii], cb[0], cb[1], L) + TO.scarti(m1[jj], m2[jj], cb[0], cb[1], L))
            ra = np.hypot(mi_[:, 0], mi_[:, 1])
            Q1 = T["arco phi (la tensione)"] - Tf3
            Q2 = 0.5 * (T["Grover nodo phi"][ii] + T["Grover nodo phi"][jj]) - vf3
            J = np.asarray(EN.corrente(st, mot, par, None), dtype=float)
            Q3 = np.abs(J)
            print("-" * 130)
            print("### %s: il baricentro (%.2f, %.2f); per anello (la media sugli archi col punto medio nell'anello [r, r+1)):" % (nome, cb[0], cb[1]))
            print("    %5s %14s %14s %14s %14s" % ("r", "T(a)", "Q1", "Q2", "Q3 |J|"))
            for r0 in ANELLI:
                s = (ra >= r0) & (ra < r0 + 1)
                if s.any():
                    print("    %5d %+14.6e %+14.6e %+14.6e %14.6e" % (r0, float(T["arco phi (la tensione)"][s].mean()), float(Q1[s].mean()), float(Q2[s].mean()), float(Q3[s].mean())))
            for qn, Q in (("Q1", Q1), ("Q2", Q2), ("Q3", Q3)):
                j = int(np.argmax(Q))
                print("    %s: nel vuoto lontano (anelli 55-60) la media %+.3e; il massimo %+.6e all'arco col punto medio a %.2f nodi; gli archi con %s >= %.2f (il costo C): %d su %d" % (
                    qn, float(Q[(ra >= 55) & (ra < 60)].mean()), float(Q[j]), float(ra[j]), qn, COSTO, int(np.sum(Q >= COSTO)), len(Q)))
            sys.stdout.flush()
        Z["metti"]()
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
