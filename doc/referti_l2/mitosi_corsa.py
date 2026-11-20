# -*- coding: utf-8 -*-
r"""**LA CORSA MITOSI SUL RAMO** *(Luca `2026-11-20` `16:37`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `9`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_corsa.py p6 > doc/referti_l2/mitosi_p6_0.txt

**Il passo della corsa MITOSI** = **il passo di C2** *(`controllo_senza_bordo.corsa_senza_bordo`, NON toccato: importato)* **con due cose in piu':**
1. **il campo `u1_generico.CampoGenerico` (B3) al posto di `_u1_prototipo.Campo`** *(costruito dagli STESSI archi, `s_a`, `e`, forma, `A`, `E`; `l/l* = sqrt(3)` e `AREA` sul toro: i valori del prototipo)*: **il prototipo ha `m = 3 n` cablato e non puo' crescere**;
2. **il contatore `Theta`** *(`contatore.Contatore`)* **accumulato DOPO ogni tick col `cs` del punto fisso del tick** *(`mot.cs`, controllato uguale a `lapse_caldo.cs_prec()`)*.
### **LA NASCITA NON C'E' ANCORA** *(il versore `geo_n` delle estremita' nuove: la carta sez. `9.3`, FERMO per Luca)*: **se un arco scatta, ALZA.**

**`p6` -- P6.0, IL BRACCIO 0** *(la carta sez. `9.5`)*: **dallo stato di C2 a `k 3000`** *(`E:/soliton_simulator/controllo/C2/stato_03000.npz`, ripreso con `controllo_senza_bordo.riprendi`)*, **`N_P6` tick col passo di C2 e `N_P6` col passo di MITOSI, nello stesso processo:**
**ogni chiave dello stato** *(salvo `h_int`, come i casi K2 e K3 di C2: stampata a parte)*, **`A`, `E`, `cs_prec` AL BIT**; **l'energia registrata** *(`totd + KVd`)* **entro `8` ulp relativi** *(`V` di B3 somma le placchette in un altro ordine: DICHIARATO)*.
**Accanto:** `s_a` del campo uniforme? *(se no: FERMO, la carta sez. `9.6`)*; **i segni delle placchette COERENTI** *(ogni arco nelle sue due placchette con segni OPPOSTI)*; `w` di B3 = `w` del prototipo AL BIT; **`Theta`:** il massimo dopo i tick, nessuno scattato; **il tempo per tick dei due passi** *(Q-P1, la parte senza nascite)*.
**IL CASO CHE DEVE FALLIRE:** **il passo di MITOSI con `E` di UN arco** *(quello che esce dal nodo piu' vicino al centro di C2)* **spostato di UN ulp prima del primo tick**: **deve risultare DIVERSO.**
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import controllo_senza_bordo as CSB  # noqa: E402  (aggiunge csv/, csv/solitone/; NON si tocca)

PS = CSB.PS
F_C2 = os.path.join(CSB.DIR, "C2", "stato_03000.npz")
K_C2 = 3000
DIR_T = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "torsione")
K0S = tuple(range(0, 3000, 250))
N_P6 = 20
EPS = np.finfo(float).eps


def campo_generico(Z, C):
    """### **`C.campo` (il prototipo) sostituito da `CampoGenerico`** con gli stessi archi, `s_a`, `e`, forma, `A`, `E`; `U` riscritta *(dalla stessa `A`: la stessa `U`)*. `(g, info)`."""
    import _u1_prototipo as U1
    import u1_generico as UG
    from solitone import toro as TO
    p = C.campo
    assert isinstance(p, U1.Campo), "il campo di partenza non e' il prototipo: %r" % type(p)
    A1, A2 = TO.vettori()
    A1, A2 = np.asarray(A1, dtype=float)[:2], np.asarray(A2, dtype=float)[:2]
    vec = np.tile(np.stack([A1, A2, A1 + A2]), (p.n, 1))          # ### l'arco 3 v + a: a1, a2, a1 + a2 (il prototipo lo controlla nel costruttore)
    g = UG.CampoGenerico(p.ii, p.jj, p.n, vec, p.e, p.forma, p.s_a, np.full(p.m, U1.L_SU_LS), lambda *_: U1.AREA)
    g.A[...] = p.A
    g.E[...] = p.E
    info = {"s_a_uniforme": bool(np.all(p.s_a == p.s_a[0])), "s_a": float(p.s_a[0]), "s_a_min": float(p.s_a.min()), "s_a_max": float(p.s_a.max()),
            "segni_coerenti": bool(np.all(g.asg[:, 0] == -g.asg[:, 1])), "w_al_bit": bool(np.array_equal(g.w, p.w)), "placchette": int(len(g.P))}
    C.campo = g
    U1.scrivi_U(Z["mot"], g)
    return g, info


def theta_C2():
    """### `Theta` a `k 3000` dai `12` segmenti di C2 *(come `csv/solitone/prova_contatore.py`)*."""
    import contatore as CO
    acc = []
    for k0 in K0S:
        with np.load(os.path.join(DIR_T, "C2_%05d.npz" % k0)) as d:
            acc.append(d["acc"].copy())
    return CO.Contatore.da_segmenti(acc)


def corsa_mitosi(cont):
    """### **Il passo di C2, poi `Theta`.** La nascita NON c'e' ancora: **se un arco scatta, ALZA.**"""
    Base = CSB.corsa_senza_bordo()
    LC = PS.LC

    class CorsaMitosi(Base):
        def passo(self, k, t, r, e):
            Base.passo(self, k, t, r, e)
            mot = self.Z["mot"]
            cs = LC.cs_prec()
            assert cs is not None and np.array_equal(cs, mot.cs), "il cs del tick non e' quello del punto fisso"
            cont.accumula(mot, mot.cs)
            sc = cont.scattati()
            assert sc.size == 0, "k %d: %d archi scattati (il primo %d) e la nascita NON c'e' ancora (la carta sez. 9.3: FERMO)" % (k, sc.size, int(sc[0]))
    return CorsaMitosi


def corri(Z, quale, n_tick, tocca, rho_c, e, t0):
    """### Dallo stato di C2 a `k 3000`, `n_tick` tick col passo `quale` (`"C2"` o `"MITOSI"`); `tocca`: l'arco il cui `E` si sposta di un ulp prima del primo tick."""
    LC, PO = PS.LC, PS.PO
    C, meta, cs, s = CSB.riprendi(Z, F_C2, False, rho_c, e)
    PO.accendi(cs)
    info, cont = None, None
    try:
        if quale == "MITOSI":
            _g, info = campo_generico(Z, C)
            cont = theta_C2()
            R = corsa_mitosi(cont)(Z, C)
        else:
            R = CSB.corsa_senza_bordo()(Z, C)
        if tocca is not None:
            C.campo.E[tocca] = np.nextafter(C.campo.E[tocca], np.inf)
        R.etichette([meta["lab"]])
        R.inizio(K_C2)
        tt = []
        for k in range(K_C2 + 1, K_C2 + n_tick + 1):
            t1 = time.time()
            R.passo(k, t0 + k, 1.0, e)
            tt.append(time.time() - t1)
        out = {"st": {x: Z["st"][x].copy() for x in Z["chiavi"]}, "A": C.campo.A.copy(), "E": C.campo.E.copy(), "cs_prec": LC.cs_prec(),
               "H": np.array(R.T["totd"]) + np.array(R.T["KVd"]), "tt": tt, "info": info, "sha": s,
               "theta_max": None if cont is None else float(np.max(np.abs(cont.theta))), "scattati": None if cont is None else int(cont.scattati().size)}
    finally:
        LC.spegni()
    Z["metti"]()
    return out


def diverse(a, b):
    d = [x for x in a["st"] if x != "h_int" and not np.array_equal(a["st"][x], b["st"][x])]
    d += [x for x in ("A", "E", "cs_prec") if not np.array_equal(a[x], b[x])]
    return d


def p6():
    import _presidio
    MT, CV = PS.MT, PS.CV
    for f in (os.path.join(PS.MT.__file__), os.path.join(_QUI, "controllo_senza_bordo.py")):
        _presidio.avvia(f)
    import u1_generico as UG
    import contatore as CO
    _presidio.avvia(UG.__file__)
    _presidio.avvia(CO.__file__)
    _presidio.avvia(__file__)
    PS.presidi()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    esiti = []
    print("=" * 130)
    print("P6.0, IL BRACCIO 0 DELLA CORSA MITOSI (Luca 2026-11-20 16:37; la carta sez. 9.5): il passo di C2 contro quello di MITOSI, %d tick da C2 a k %d" % (N_P6, K_C2))
    print("=" * 130)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        c2 = corri(Z, "C2", N_P6, None, rho_c, e, t0)
        mi = corri(Z, "MITOSI", N_P6, None, rho_c, e, t0)
        with np.load(F_C2) as d:
            import json
            cen = json.loads(str(d["meta"]))["centro"]
        from solitone import toro as TO
        r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], cen[0], cen[1], Z["L"]).T[:2])
        nodo_c = int(np.argmin(r))
        arco = 3 * nodo_c
        fa = corri(Z, "MITOSI", N_P6, arco, rho_c, e, t0)
    info = mi["info"]
    print("### lo stato di partenza: %s (sha1 %s, ricontrollato da riprendi)" % (F_C2, c2["sha"][:8]))
    print("### il campo generico: le placchette %d; s_a uniforme %s (%.17g, da %.17g a %.17g); i segni delle placchette coerenti %s; w AL BIT col prototipo %s" % (
        info["placchette"], info["s_a_uniforme"], info["s_a"], info["s_a_min"], info["s_a_max"], info["segni_coerenti"], info["w_al_bit"]))
    esiti.append(("s_a del campo di C2 uniforme (se no: FERMO, la carta sez. 9.6)", info["s_a_uniforme"]))
    esiti.append(("i segni delle placchette coerenti (ogni arco in due placchette con segni opposti)", info["segni_coerenti"]))
    esiti.append(("w del campo generico = w del prototipo AL BIT", info["w_al_bit"]))
    d = diverse(c2, mi)
    hi = np.array_equal(c2["st"]["h_int"], mi["st"]["h_int"])
    print("### P6.0: %d tick, C2 contro MITOSI: %s; h_int (fuori dal confronto, come K2 e K3 di C2) %s" % (N_P6, "AL BIT su ogni chiave, A, E, cs_prec" if not d else "### DIVERSE: %s" % d, "al bit" if hi else "diversa"))
    esiti.append(("P6.0: il passo di MITOSI = il passo di C2 AL BIT (ogni chiave salvo h_int, A, E, cs_prec)", not d))
    dH = np.abs(mi["H"] - c2["H"]) / np.abs(c2["H"])
    print("### l'energia registrata (totd + KVd), %d valori: la differenza relativa massima %.2e (%.1f ulp)" % (len(dH), float(dH.max()), float(dH.max()) / EPS))
    esiti.append(("l'energia registrata entro 8 ulp relativi (V: l'ordine delle placchette, dichiarato)", float(dH.max()) <= 8 * EPS))
    print("### Theta: dopo %d tick il massimo |Theta| %.6e rad (2 pi = %.6e); scattati %d" % (N_P6, mi["theta_max"], 2 * np.pi, mi["scattati"]))
    esiti.append(("Theta: nessun arco scattato (la nascita non c'e' ancora)", mi["scattati"] == 0))
    df = diverse(c2, fa)
    print("### DEVE FALLIRE: E dell'arco %d (dal nodo %d, il piu' vicino al centro %s) spostato di un ulp: %s" % (arco, nodo_c, ["%.3f" % x for x in cen], "### UGUALE" if not df else "diverse: %s" % df))
    esiti.append(("DEVE FALLIRE: un ulp in E di un arco prima del primo tick rende il risultato DIVERSO", bool(df)))
    print("### il tempo per tick (Q-P1, senza nascite): C2 la mediana %.3f s, MITOSI %.3f s (il rapporto %.4f)" % (
        float(np.median(c2["tt"])), float(np.median(mi["tt"])), float(np.median(mi["tt"])) / float(np.median(c2["tt"]))))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("p6")
    x = ap.parse_args(argv)
    if x.cmd == "p6":
        return p6()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
