# -*- coding: utf-8 -*-
r"""**T0: LA DIAGNOSI DEL TRIANGOLO DEGENERE, SENZA CORSE** *(il mandato di Luca `2026-11-21` `22:12`; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `2.1`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/degenere_diagnosi.py > doc/referti_l2/degenere_diagnosi_parte1.txt

**Dallo stato `k 36250` del ramo MITOSI** *(`mitosi_lunga.riprendi`, la sha1; il lapse acceso come nella corsa)*, **nessun tick**: gli archi la cui stella contiene `13482` o `34601`, in ordine di `|Theta|` decrescente; per ognuno la sola nascita e i quattro flip *(`mitosi_regola.candidato`)* con **`CampoGenerico._placchetta` sorvegliata IN MEMORIA** *(un involucro in questo processo: registra il triangolo, i due archi, i due vettori d'arco, il prodotto, e rilancia; NESSUN file toccato)*. **L'arco della decima** = il primo che riproduce il triangolo `(13482, 34601, 34605)`.
**Poi:** i due vettori d'arco *(uguali? opposti? il rapporto)*, la provenienza di ciascuno *(la nascita che ha creato l'arco e la formula: `-va/2`, `+va/2`, `v(i,c) - va/2`, il flip)*, i versori `geo.n` delle stesse estremita'; la storia del nodo `34601` *(`nascite_36250.json`)*.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_lunga as ML  # noqa: E402

MR, MC, PS = ML.MR, ML.MC, ML.PS
D = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami", "MITOSI")
F = os.path.join(D, "stato_36250.npz")
FN = os.path.join(D, "nascite_36250.json")
TRI = (13482, 34601, 34605)
N_ARCHI = 12


def main():
    import _presidio
    import u1_generico as UG
    _presidio.avvia(os.path.join(_QUI, "mitosi_regola.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    MT = PS.MT
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    REG = []
    orig = UG.CampoGenerico._placchetta

    def sorvegliata(self, x, y, z, adj):
        try:
            return orig(self, x, y, z, adj)
        except AssertionError:
            axy, axz = adj[x][y], adj[x][z]
            dy, dz = UG._verso(self.vec, self.ii, axy, x), UG._verso(self.vec, self.ii, axz, x)
            REG.append({"tri": (int(x), int(y), int(z)), "axy": int(axy), "axz": int(axz), "m": int(self.m),
                        "ab_xy": (int(self.ii[axy]), int(self.jj[axy])), "ab_xz": (int(self.ii[axz]), int(self.jj[axz])),
                        "vec_xy": self.vec[axy].copy(), "vec_xz": self.vec[axz].copy(), "dy": np.array(dy), "dz": np.array(dz),
                        "cr": float(dy[0] * dz[1] - dy[1] * dz[0])})
            raise
    UG.CampoGenerico._placchetta = sorvegliata
    print("=" * 140)
    print("T0, LA DIAGNOSI DEL TRIANGOLO DEGENERE (Luca 2026-11-21 22:12; la carta sez. 2.1): dallo stato %s, NESSUN tick" % F)
    print("=" * 140)
    with open(FN, encoding="utf-8") as fh:
        B = json.load(fh)
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, NS, meta, cs = ML.riprendi(Z, F, rho_c, e, True)
        PS.PO.accendi(cs)
        try:
            mot = Z["mot"]
            nodo = np.asarray(mot.inc.nodo)
            ii, jj = nodo[0::2].astype(np.int64), nodo[1::2].astype(np.int64)
            vec, th = C.campo.vec, NS.cont.theta
            print("### lo stato: k %d, n %d, m %d, nascite %d, E_persa %+.6e; sha1 %s" % (int(meta["k"]), mot.inc.n, mot.inc.m, NS.nascite, NS.e_persa, ML.sha1(F)[:8]))
            sel = np.zeros(len(ii), dtype=bool)
            for v in TRI[:2]:
                sel |= (ii == v) | (jj == v)
                vv = np.array(sorted(MR.vicini(ii, jj, v)))
                sel |= np.isin(ii, vv) & np.isin(jj, vv)
            cand = np.nonzero(sel)[0]
            cand = cand[np.argsort(-np.abs(th[cand]), kind="stable")][:N_ARCHI]
            print("### gli archi la cui stella contiene %d o %d: %d; i primi %d per |Theta| (2 pi = %.6f; il massimo di |Theta| su tutto il grafo %.6f, l'arco %d):" % (
                TRI[0], TRI[1], int(sel.sum()), len(cand), 2 * np.pi, float(np.max(np.abs(th))), int(np.argmax(np.abs(th)))))
            trovato = None
            for a in cand:
                a = int(a)
                riga = "    l'arco %6d (%d -> %d) |Theta| %.6f (manca %.6f):" % (a, ii[a], jj[a], abs(th[a]), 2 * np.pi - abs(th[a]))
                n0 = len(REG)
                try:
                    nas = MR.candidato(Z, C, a, None, "stella")
                    nd = nas["nodi"]
                    esiti = ["nascita ok"]
                    lati = ((nd["i"], nd["k"]), (nd["j"], nd["k"]), (nd["j"], nd["l"]), (nd["i"], nd["l"]))
                    for q, lt in enumerate(lati):
                        try:
                            MR.candidato(Z, C, a, lt, "stella")
                            esiti.append("flip %d ok" % q)
                        except AssertionError:
                            esiti.append("flip %d (%d, %d) DEGENERE %s" % (q, lt[0], lt[1], REG[-1]["tri"]))
                            if set(REG[-1]["tri"]) == set(TRI) and trovato is None:
                                trovato = (a, "flip %d (%d, %d)" % (q, lt[0], lt[1]), REG[-1], nd, lt)
                except AssertionError:
                    esiti = ["la sola nascita DEGENERE %s" % (REG[-1]["tri"],) if len(REG) > n0 else "la sola nascita ALZA (non degenere)"]
                    if len(REG) > n0 and set(REG[-1]["tri"]) == set(TRI) and trovato is None:
                        trovato = (a, "la sola nascita", REG[-1], None, None)
                print(riga + " " + "; ".join(esiti))
                sys.stdout.flush()
            print("-" * 140)
            if trovato is None:
                print("### NESSUNO dei %d archi riproduce il triangolo %s" % (len(cand), TRI))
            else:
                a, quale, R, nd, lt = trovato
                print("### L'ARCO DELLA DECIMA: %d (%d -> %d), |Theta| %.6f; il candidato: %s" % (a, ii[a], jj[a], abs(th[a]), quale))
                if nd is not None:
                    print("    la stella: i %d j %d k %d l %d, il nodo nuovo n %d" % (nd["i"], nd["j"], nd["k"], nd["l"], nd["n"]))
                print("### IL TRIANGOLO (x, y, z) %s; il grafo del candidato ha %d archi" % (R["tri"], R["m"]))
                for nome, ab, v_, d_ in (("x-y", R["ab_xy"], R["vec_xy"], R["dy"]), ("x-z", R["ab_xz"], R["vec_xz"], R["dz"])):
                    print("    l'arco %s: %d -> %d, il vettore d'arco %s, nel verso da x %s" % (nome, ab[0], ab[1], np.array2string(v_, precision=17), np.array2string(d_, precision=17)))
                dy, dz = R["dy"], R["dz"]
                rap = [dz[q] / dy[q] if dy[q] != 0.0 else float("nan") for q in range(2)]
                print("    il prodotto vettoriale %r; uguali al bit %s; opposti al bit %s; il rapporto per componente %s" % (
                    R["cr"], bool(np.array_equal(dy, dz)), bool(np.array_equal(dy, -dz)), rap))
                # ### la provenienza degli archi: nella stella del candidato o nati prima
                for ab in (R["ab_xy"], R["ab_xz"]):
                    u, w = ab
                    if TRI[2] in ab:
                        altro = u if w == TRI[2] else w
                        ruolo = [r for r in ("i", "j", "k", "l") if nd is not None and nd[r] == altro]
                        if lt is not None and altro == (lt[1] if lt[0] in (nd["i"], nd["j"]) else lt[0]):
                            ruolo.append("m?")
                        print("    l'arco %d-%d e' del CANDIDATO (n = %d): %d e' %s della stella" % (u, w, TRI[2], altro, ruolo or "il nodo m del flip"))
                    else:
                        nati = [b for b in B if b["nodi"]["n"] in ab]
                        for b in nati:
                            nb = b["nodi"]
                            altro = u if w == nb["n"] else w
                            ruolo = [r for r in ("i", "j", "k", "l", "m") if nb.get(r) == altro]
                            print("    l'arco %d-%d e' nato alla nascita di k %d (l'arco %d, n %d): %d e' %s di quella stella%s" % (
                                u, w, b["k"], b["a"], nb["n"], altro, ruolo, " (il flip)" if ruolo == ["m"] else ""))
                        if not nati:
                            print("    l'arco %d-%d e' del toro di partenza" % (u, w))
                # ### i versori geo.n delle stesse estremita' (sul grafo di oggi, per gli archi che ci sono)
                for ab in (R["ab_xy"], R["ab_xz"]):
                    u, w = ab
                    m_ = np.nonzero(((ii == u) & (jj == w)) | ((ii == w) & (jj == u)))[0]
                    if m_.size:
                        q = int(m_[0])
                        print("    i versori geo.n dell'arco %d-%d (oggi, l'arco %d): in %d %s, in %d %s" % (
                            u, w, q, ii[q], np.array2string(mot.geo.n[2 * q], precision=6), jj[q], np.array2string(mot.geo.n[2 * q + 1], precision=6)))
                    else:
                        print("    l'arco %d-%d NON c'e' nel grafo di oggi (e' del candidato)" % (u, w))
            print("-" * 140)
            print("### LA STORIA DEL NODO %d:" % TRI[1])
            for b in B:
                nb = b["nodi"]
                if TRI[1] in nb.values():
                    ruolo = [r for r, v in nb.items() if v == TRI[1]]
                    print("    k %d, l'arco %d: %s; il nodo %d e' %s; il lato scelto %d, DH nascita %+.4e flip %+.4e, r %.3f" % (
                        b["k"], b["a"], json.dumps(nb), TRI[1], ruolo, b["scelto"], b["DH_nascita"], b["DH_flip"], b.get("r", float("nan"))))
            vic = sorted(MR.vicini(ii, jj, TRI[1]))
            print("    i vicini di %d oggi (%d): %s" % (TRI[1], len(vic), vic))
            vic0 = sorted(MR.vicini(ii, jj, TRI[0]))
            print("    i vicini di %d oggi (%d): %s" % (TRI[0], len(vic0), vic0))
        finally:
            PS.LC.spegni()
            UG.CampoGenerico._placchetta = orig
    print("=" * 140)
    return 0


if __name__ == "__main__":
    sys.exit(main())
