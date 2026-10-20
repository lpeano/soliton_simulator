# -*- coding: utf-8 -*-
r"""**LA SCALA DEL SALTO DI `H` SULLA MATERIA UNIFORME** — *una misura, nessun codice di fisica.*

> ### ⛔ **Il task history e' `2026-10-20_controllo_passo_materia_uniforme.md`**, sez.`2-bis`
> *(`11d69c84`)*: decisione di Luca delle `09:58` sullo STOP di `363c6559`. ### **«Difetto del
> passo» si dice solo dopo questa misura.** ### **`LINEARE`, `Lambda_c` e le letture «alla
> Jeans» restano FERMI.**

## ⭐ `S1` LA MISURA *(a tempo totale fisso `T = 10`)*

Sulla materia uniforme, `cs` spento, `dtau` in `{0.5, 0.25, 0.125}` e `x` in `{0.01, 0.1, 1}`:
### **il salto di `H` a mezzo tick, per nodo**. Sulla scena di `M-B2`: ### **l'escursione.**

## ⭐ `S2` LE DUE PREVISIONI

`P2` ordinario *(pendenza `2`)* · `P1` non conservato al primo ordine *(pendenza `1`)*. ### **La
barra** e' la curvatura delle due pendenze a coppie, in quadratura con la dispersione; ### **la
soglia** e' la `t` di Student a `1` grado al `99.73%`.

## ⭐ `S3` LA SCOMPOSIZIONE *(`dtau 0.5`, `x 0.1`)*, verificata AL BIT contro `termini_di_h`

## ⛔ `S4` IL CASO CHE DEVE RIUSCIRE: `M-B2` con pendenza `2`

Gira con:  python csv/_scala_salto.py
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _controllo_passo as CP                                   # noqa: E402
import _jeans_del_modello as JM                                 # noqa: E402

EPS = float(np.finfo(float).eps)
TEMPO = 10.0                   # dichiarato nel task history (20 tick a dtau 0.5)
DTAU = (0.5, 0.25, 0.125)
XX = (0.01, 0.1, 1.0)
X_SCOMP = 0.1
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def t_un_grado():
    import scipy.stats as SS
    return float(SS.t.ppf(1.0 - (1.0 - JM.COPERTURA) / 2.0, 1))


def tick_di(dtau):
    return int(round(TEMPO / dtau))


def scena_mb2(dtau):
    import _misura_mb2 as MB2
    import deriva as DV
    return DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                    vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)


def intreccia(intero, mezzo, k):
    """### `H` (o la colonna `k`) a `t, t + 1/2, t + 1, ...`."""
    fuori = []
    for t in range(len(mezzo)):
        fuori += [intero[t][k], mezzo[t][k]]
    fuori.append(intero[len(mezzo)][k])
    return np.asarray(fuori, dtype=float)


def pendenza(dt, y):
    """### `(p, p_coppia_1, p_coppia_2)` di `log y` contro `log dtau`."""
    lx, ly = np.log(np.asarray(dt)), np.log(np.asarray(y))
    p = float(np.polyfit(lx, ly, 1)[0])
    p1 = float((ly[1] - ly[0]) / (lx[1] - lx[0]))
    p2 = float((ly[2] - ly[1]) / (lx[2] - lx[1]))
    return p, p1, p2


def barra(dt, p1, p2, sig_rel):
    """### La curvatura, in quadratura con la propagazione della dispersione relativa."""
    lx = np.log(np.asarray(dt))
    stat = float(np.sqrt(np.sum(np.asarray(sig_rel) ** 2) / np.sum((lx - lx.mean()) ** 2)))
    curv = abs(p1 - p2) / 2.0
    return float(np.hypot(curv, stat)), curv, stat


def verdetto(p, b, ts):
    v2 = abs(p - 2.0) <= ts * b
    v1 = abs(p - 1.0) <= ts * b
    if v2 and not v1:
        return "P2"
    if v1 and not v2:
        return "P1"
    return "ne' l'una ne' l'altra" if not (v1 or v2) else "entrambe (non separabili)"


# =====================================================================================
#   S3: I TERMINI, con le operazioni e l'ordine di `termini_di_h`
# =====================================================================================
def termini(mot, st, par):
    import energia_pesata as EP
    inc = mot.inc
    psi, phi = st["psi_h"], st["phi_h"]
    m = inc.m
    U = mot.geo.U
    nrm_psi = EP._per_nodo(mot, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2,
                           np.empty(inc.n, dtype=float))
    nrm_phi = EP._per_nodo(mot, np.abs(phi) ** 2, np.empty(inc.n, dtype=float))
    S_psi = np.zeros((inc.n, 2), dtype=complex)
    np.add.at(S_psi, inc.nodo, psi)
    S_phi = np.zeros(inc.n, dtype=complex)
    np.add.at(S_phi, inc.nodo, phi)
    d = inc.grado.astype(float)
    pu_psi = (np.abs(S_psi[:, 0]) ** 2 + np.abs(S_psi[:, 1]) ** 2) / d
    pu_phi = np.abs(S_phi) ** 2 / d
    h = mot.elicita(st).copy()
    eps = float(par["eps"])
    rho, lam = nrm_psi, nrm_phi
    N = np.zeros(inc.n, dtype=float)
    vivi = rho > 0.0
    if np.any(vivi):
        N[vivi] = rho[vivi] * np.log(rho[vivi] / (rho[vivi] + lam[vivi]))
    v = psi.reshape(m, 2, 2)
    p0, p1 = v[:, 0, :], v[:, 1, :]
    incro = np.einsum("ai,aji,aj->a", np.conj(p0), np.conj(U), p1)
    nrm_a = (np.abs(p0) ** 2).sum(axis=1) + (np.abs(p1) ** 2).sum(axis=1)
    w = phi.reshape(m, 2)
    f0, f1 = w[:, 0], w[:, 1]
    nrm_f = np.abs(f0) ** 2 + np.abs(f1) ** 2
    inc_f = np.real(np.conj(f0) * f1)
    # ### la RICOSTRUZIONE, nello stesso ordine di `termini_di_h`
    per_nodo = -EP.OMEGA_H * ((nrm_psi - pu_psi) + (nrm_phi - pu_phi))
    per_nodo = per_nodo + eps * h
    per_nodo = per_nodo + N
    arco_psi = (nrm_a - 2.0 * np.real(incro)) / 2.0
    arco_phi = (nrm_f - 2.0 * inc_f) / 2.0
    per_arco = -EP.OMEGA_H * (arco_psi + arco_phi)
    pezzi = {
        "nodo psi": float(np.sum(-EP.OMEGA_H * (nrm_psi - pu_psi))),
        "nodo phi": float(np.sum(-EP.OMEGA_H * (nrm_phi - pu_phi))),
        "moneta (eps h)": float(np.sum(eps * h)),
        "N": float(np.sum(N)),
        "arco psi norma": float(np.sum(-EP.OMEGA_H * nrm_a / 2.0)),
        "arco psi incrocio": float(np.sum(EP.OMEGA_H * np.real(incro))),
        "arco phi norma": float(np.sum(-EP.OMEGA_H * nrm_f / 2.0)),
        "arco phi incrocio": float(np.sum(EP.OMEGA_H * inc_f)),
    }
    return per_nodo, per_arco, pezzi


def al_bit(mot, st, par):
    """### `(ok, pezzi)`: i due vettori ricostruiti contro `termini_di_h`, e `G` contro la somma."""
    import energia_pesata as EP
    pn, pa, pezzi = termini(mot, st, par)
    rn, ra = EP.termini_di_h(mot, st, par)
    g = EP.g_dello_stato(mot, st, par)
    ok = (np.array_equal(pn, rn) and np.array_equal(pa, ra)
          and float(np.sum(pn)) + float(np.sum(pa)) == g)
    return ok, pezzi, g


def scomposizione():
    import tick as TK
    inc, mot, st, par = JM.scena(0.5, X_SCOMP)
    meta = TK.meta_del_palindromo()
    serie, tutti = [], True
    for t in range(tick_di(0.5)):
        ok, pz, g = al_bit(mot, st, par)
        tutti &= ok
        serie.append(("%d" % t, pz, g))
        copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
        TK.percorri_tick(copia, mot, par, (), None, meta)
        ok, pz, g = al_bit(mot, copia, par)
        tutti &= ok
        serie.append(("%d.5" % t, pz, g))
        TK.tick(st, mot, par)
    ok, pz, g = al_bit(mot, st, par)
    tutti &= ok
    serie.append(("%d" % tick_di(0.5), pz, g))
    return tutti, serie, inc.n


# =====================================================================================
#   MAIN
# =====================================================================================
def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _misura_mb2 as MB2
    import composizione as CM
    import statica_protocollo as PR
    ts = t_un_grado()
    print("=" * 100)
    print("LA SCALA DEL SALTO DI H SULLA MATERIA UNIFORME -- una misura, nessun codice di fisica")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la materia uniforme (29b997da): lati %s, VUOTO %.1f, cs SPENTO, nessuna"
          " perturbazione; x in %s" % (PR.LATI, PR.VUOTO, XX))
    print("  la scena di M-B2: nn %d, seme %d, norma %s, vuoto_modulo %g, su2 %s"
          % (MB2.NN, MB2.SEME, MB2.NORMA, MB2.VUOTO_MODULO, MB2.SU2))
    print("  dtau in %s, a TEMPO TOTALE FISSO T = %g (tick %s)"
          % (DTAU, TEMPO, [tick_di(d) for d in DTAU]))
    print("  il passo: %d pezzi, impronta %s; la soglia: t di Student a 1 grado al %.2f%% = %.2f"
          % (len(CM.ORDINE), CM.IMPRONTA, 100 * JM.COPERTURA, ts))
    print("-" * 100)
    sys.stdout.flush()

    # ------------------------------------------------------------------ S4 il caso che deve riuscire
    print("### S4, IL CASO CHE DEVE RIUSCIRE: la scena di M-B2, l'escursione di H")
    esc = []
    for dt in DTAU:
        inc, mot, st, par = scena_mb2(dt)
        intero, _m = CP.serie_c1(inc, mot, st, par, tick_di(dt), False)
        H = np.array([c[1] for c in intero])
        esc.append(float(np.max(np.abs(H[1:] - H[0]))))
        print("     dtau %-6g tick %-4d  escursione %.6e   relativa %.3e"
              % (dt, tick_di(dt), esc[-1], esc[-1] / abs(H[0])))
    p, q1, q2 = pendenza(DTAU, esc)
    b, curv, stat = barra(DTAU, q1, q2, [0.0, 0.0, 0.0])
    print("     pendenza %.3f (a coppie %.3f, %.3f), barra %.3f (curvatura)" % (p, q1, q2, b))
    # ### 📌 INFORMAZIONE, NON CRITERIO (aggiunta dopo la prova a vuoto, non tenuta): ### **la
    # ### stessa regola darebbe <<passa>> anche a pendenza `1`?** Se si', il caso che deve
    # ### riuscire ### **non discrimina** -- e lo si stampa invece di cambiare il criterio.
    print("     ### INFORMAZIONE: |p - 1| = %.3f, |p - 2| = %.3f, t*barra = %.3f -> la regola %s"
          % (abs(p - 1.0), abs(p - 2.0), ts * b,
             "NON DISCRIMINA (passerebbe anche p = 1)" if abs(p - 1.0) <= ts * b
             else "discrimina"))
    if not esito("S4 M-B2: |p - 2| <= t * barra", abs(p - 2.0) <= ts * b,
                 "p %.3f, t*barra %.3f" % (p, ts * b)):
        print("### STOP: il caso di M-B2 non riesce -- nessun verdetto sulla materia uniforme")
        return 1
    print("-" * 100)

    # ------------------------------------------------------------------ S1/S2
    print("### S1, LA MATERIA UNIFORME: il salto di H a mezzo tick, PER NODO")
    tab = {}
    for x in XX:
        for dt in DTAU:
            inc, mot, st, par = JM.scena(dt, x)
            rm = float(np.mean(mot.densita_materia(st)))
            intero, mezzo = CP.serie_c1(inc, mot, st, par, tick_di(dt), True)
            H = intreccia(intero, mezzo, 1)
            s = np.abs(np.diff(H)) / inc.n
            esc_u = float(np.max(np.abs(H - H[0])))
            tab[(x, dt)] = (float(np.mean(s)), float(np.min(s)), float(np.max(s)), rm, esc_u)
            print("     x %-5g dtau %-6g rho_medio %.6f  salto/nodo %.6e  [min %.6e, max %.6e]"
                  "  rho_medio*dtau %.6e  escursione %.4e"
                  % (x, dt, rm, tab[(x, dt)][0], tab[(x, dt)][1], tab[(x, dt)][2], rm * dt,
                     esc_u))
            sys.stdout.flush()
    print("### S2, LE PENDENZE E IL VERDETTO")
    for x in XX:
        y = [tab[(x, d)][0] for d in DTAU]
        sig = [(tab[(x, d)][2] - tab[(x, d)][1]) / (2.0 * tab[(x, d)][0]) for d in DTAU]
        p, q1, q2 = pendenza(DTAU, y)
        b, curv, stat = barra(DTAU, q1, q2, sig)
        print("     x %-5g pendenza %.4f (a coppie %.4f, %.4f)  barra %.2e (curvatura %.2e,"
              " dispersione %.2e)  t*barra %.2e  -> %s"
              % (x, p, q1, q2, b, curv, stat, ts * b, verdetto(p, b, ts)))
    # ### 📌 INFORMAZIONE, NON CRITERIO (aggiunta dopo la prova a vuoto, non tenuta):
    # ### ### **l'escursione e' deterministica**, mentre la dispersione dei salti lungo
    # ### l'orbita ### **non e' un'incertezza** -- e' la forma dell'oscillazione.
    print("### INFORMAZIONE, NON CRITERIO: la pendenza dell'ESCURSIONE di H in log dtau")
    for x in XX:
        p, q1, q2 = pendenza(DTAU, [tab[(x, d)][4] for d in DTAU])
        print("     x %-5g pendenza %.4f (a coppie %.4f, %.4f)" % (x, p, q1, q2))
    print("### IN x, a ogni dtau: il salto per nodo diviso quello a x 0.1")
    for dt in DTAU:
        r = [tab[(x, dt)][0] / tab[(0.1, dt)][0] for x in XX]
        lx = np.log(np.asarray(XX))
        px = float(np.polyfit(lx, np.log([tab[(x, dt)][0] for x in XX]), 1)[0])
        print("     dtau %-6g  %s   pendenza in log x %.4f"
              % (dt, "  ".join("x %g: %.4f" % (x, v) for x, v in zip(XX, r)), px))
    print("-" * 100)

    # ------------------------------------------------------------------ S3
    print("### S3, LA SCOMPOSIZIONE a dtau 0.5, x %g, a ogni mezzo tick" % X_SCOMP)
    tutti, serie, n = scomposizione()
    if not esito("S3 per_nodo, per_arco e G ricostruiti AL BIT", tutti):
        print("### STOP: la scomposizione non e' quella di H")
        return 1
    nomi = list(serie[0][1].keys())
    print("     t      " + "  ".join("%-18s" % k[:18] for k in nomi) + "  G")
    for t, pz, g in serie[:9]:
        print("     %-6s " % t + "  ".join("%+.11e" % pz[k] for k in nomi) + "  %+.11e" % g)
    print("     ...")
    print("     il salto medio a mezzo tick, PER NODO, di ciascun termine:")
    for k in nomi:
        v = np.array([pz[k] for _t, pz, _g in serie])
        s = np.abs(np.diff(v)) / n
        print("       %-20s %.6e   [min %.3e, max %.3e]" % (k, float(np.mean(s)),
                                                           float(np.min(s)), float(np.max(s))))
    G = np.array([g for _t, _p, g in serie])
    print("       %-20s %.6e" % ("G (il totale)", float(np.mean(np.abs(np.diff(G)) / n))))
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA INTERPRETAZIONE FISICA. LINEARE e Lambda_c FERMI."
          % tuple(OK))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
