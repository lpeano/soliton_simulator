# -*- coding: utf-8 -*-
r"""**LA REGOLA INTERA NELLA CORSA** *(il ramo `mitosi`; Luca `2026-11-20` `13:33`, `13:54`, `14:53`, `16:37`, `17:03`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `9`-`10`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_regola.py caso > doc/referti_l2/mitosi_regola_caso.txt

**La regola** *(sullo stato VERO della corsa: il motore, il campo `CampoGenerico`, il contatore, le posizioni)*:
1. **la nascita di stella sull'arco `a = i -> j`** *(D-COVSTELLA: `n -> i` = l'estremita' di `a` in `j`, `n -> j` = quella in `i`, `n -> k` la media di `i -> k` e `j -> k`, l'estremita' nuova di `k` la media di `k -> i` e `k -> j`, le due estremita' di `a` trasportate; il fattore uniforme sulla stella `i, j, k, l, n`, per `psi` e per `phi`)*;
   **i versori** *(D-VERSORE, V1)*: **gli stessi indici, le medie NORMALIZZATE**, nessun fattore;
2. **i quattro flip di stella** `(i, k)`, `(j, k)`, `(j, l)`, `(i, l)` *(D-FLIP-AMPIEZZE: le medie in `n` e in `m` verso `x` e `y`, il fattore sul quadrilatero `n, x, m, y`)*; **i versori** *(V3)*: `v` = la differenza normalizzata delle due medie, **`+v` in `n`, `-v` in `m`**;
3. **il campo di ogni candidato:** `A` degli archi nuovi di B3 alla nascita *(D-A-NASCITA)*; **al flip `A(n -> m)` = la media dei due cammini `n -> x -> m` e `n -> y -> m`** *(= il flusso del quadrilatero a meta' in aritmetica esatta: D-A-FLIP)*; `E` dei nuovi a `0`, poi **Gauss vero** *(`p6_u_breve.gauss_sparso`, la correzione di norma minima)*; l'area `AREA`, `l/l* = sqrt(3)` *(D-AREA)*, `s_a` il valore uniforme;
4. **l'energia della corsa di ogni candidato** *(D-H-CORSA: `_libro_dei_conti.conti_per_nodo` + `K + V`, su un `Motore` costruito sul grafo del candidato)*; **la scelta (A)** *(il piu' basso; il pari merito sotto `GUARDIA |H|`: nessun flip)*;
5. **lo stato scelto nel motore VERO in UNA crescita** *(`Motore.cresci` fra `apri_tick` e `chiudi_tick`: tolti `a` e `x - y`, nati `n -> i, j, k, l, m`; il grafo controllato uguale ai due passi)*; il campo scelto; `Theta` *(i nuovi da `0`)*; le posizioni *(B4)*; `cs` del nodo nuovo dalla legge; `lapse_caldo.STATO["cs"]` la media di `i` e `j`; **l'energia RILETTA col conto della corsa** *(P9 alla nascita)*.

**`caso`** *(la carta sez. `10.3`)*: dallo stato di C2 a `k 3000`, la nascita FORZATA sul primo arco nell'ordine di scatto *(`candidati.npz`, il tempo `T`)*: **K0** *(il conto di un motore costruito sugli array = il conto della corsa, AL BIT)*, **V-0** *(i versori di oggi = le direzioni dei vettori d'arco, entro `4` ulp: il riferimento di V-b)*, **V-a, V-b, F3, P1, P3, P9**, i casi che devono fallire, **il costo.**
"""
import copy
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_corsa as MC  # noqa: E402  (aggiunge csv/, csv/solitone/; controllo_senza_bordo)

PS = MC.PS
GUARDIA = 1e-12
EPS = np.finfo(float).eps
DIR_T = MC.DIR_T


# ------------------------------------------------------------------------------------------ il grafo
def nodo_h(ii, jj):
    h = np.empty(2 * len(ii), dtype=np.int64)
    h[0::2] = ii
    h[1::2] = jj
    return h


def arco_fra(ii, jj, x, y):
    e = np.nonzero(((ii == x) & (jj == y)) | ((ii == y) & (jj == x)))[0]
    assert len(e) == 1, "fra %d e %d ci sono %d archi" % (x, y, len(e))
    return int(e[0])


def h_in(ii, jj, x, y):
    """### l'indice dell'estremita' in `x` dell'arco fra `x` e `y`."""
    a = arco_fra(ii, jj, x, y)
    return 2 * a if int(ii[a]) == x else 2 * a + 1


def vicini(ii, jj, v):
    return set(jj[ii == v].tolist()) | set(ii[jj == v].tolist())


def A_da(ii, jj, A, x, y):
    """### `A` dell'arco percorso da `x` a `y` (col segno del verso)."""
    a = arco_fra(ii, jj, x, y)
    return A[a] if int(ii[a]) == x else -A[a]


def indici_nascita(ii, jj, vec, a):
    """### `(i, j, k, l)`: `k` a sinistra di `i -> j` (dai vettori d'arco: come `nascita_dentro_fuori.nasci`)."""
    i, j = int(ii[a]), int(jj[a])
    com = sorted(vicini(ii, jj, i) & vicini(ii, jj, j))
    assert len(com) == 2, "l'arco %d non ha due vicini comuni (%s)" % (a, com)
    va = vec[a]
    vic = [_v(ii, jj, vec, i, c) for c in com]
    cr = [va[0] * v[1] - va[1] * v[0] for v in vic]
    k, l = (com[0], com[1]) if cr[0] > 0 else (com[1], com[0])
    return i, j, k, l


def _v(ii, jj, vec, x, y):
    a = arco_fra(ii, jj, x, y)
    return vec[a] if int(ii[a]) == x else -vec[a]


def dove_di(keep):
    """### la permutazione delle estremita' di `Incidenza.cresci`: i tenuti nell'ordine, i tolti a `-1`."""
    m = keep.size
    r = np.cumsum(keep) - 1
    dove = np.full(2 * m, -1, dtype=np.int64)
    q = np.nonzero(keep)[0]
    dove[2 * q] = 2 * r[q]
    dove[2 * q + 1] = 2 * r[q] + 1
    return dove


# ------------------------------------------------------------------------------------------ la nascita e il flip sugli array
def _fattore(x_old, h_old, y, h_new):
    Nb = float(np.sum(np.abs(x_old[h_old]) ** 2))
    Na = float(np.sum(np.abs(y[h_new]) ** 2))
    if Nb > 0.0 and Na > 0.0:
        y[h_new] *= math.sqrt(Nb / Na)


def _normalizza(v):
    return v / np.linalg.norm(v)


def nasci_array(ii, jj, a, nodi, x, modo):
    """### `x` per estremita' sul grafo nato (gli archi `n -> i, j, k, l` in coda). `modo`: `"ampiezza"` (la media, poi il fattore di stella: lo fa chi chiama) o `"versore"` (le medie normalizzate)."""
    i, j, k, l = nodi["i"], nodi["j"], nodi["k"], nodi["l"]
    m = len(ii)
    keep = np.ones(m, dtype=bool)
    keep[a] = False
    b = m - 1
    y = np.zeros((2 * (m + 3),) + x.shape[1:], dtype=x.dtype)
    y[:2 * b] = x[np.repeat(keep, 2)]
    y[2 * b + 1] = x[2 * a]
    y[2 * (b + 1) + 1] = x[2 * a + 1]
    y[2 * b] = x[2 * a + 1]
    y[2 * (b + 1)] = x[2 * a]
    medie = ((2 * (b + 2), (i, k), (j, k)), (2 * (b + 3), (i, l), (j, l)), (2 * (b + 2) + 1, (k, i), (k, j)), (2 * (b + 3) + 1, (l, i), (l, j)))
    for h, p, q in medie:
        y[h] = 0.5 * (x[h_in(ii, jj, *p)] + x[h_in(ii, jj, *q)])
        if modo == "versore":
            y[h] = _normalizza(y[h])
    return y


def flip_array(ii2, jj2, nodi, x2, y_, m_, x, modo, regola):
    """### `x` per estremita' dopo il flip di `x_ - y_` in `n -> m` (l'arco nuovo in coda). `modo` `"ampiezza"` o `"versore"`; `regola` `"stella"` o `"verso"` (il caso che DEVE fallire)."""
    n = nodi["n"]
    e = arco_fra(ii2, jj2, x2, y_)
    m2 = len(ii2)
    keep = np.ones(m2, dtype=bool)
    keep[e] = False
    y = np.zeros((2 * m2,) + x.shape[1:], dtype=x.dtype)
    y[:2 * (m2 - 1)] = x[np.repeat(keep, 2)]
    hn, hm = 2 * (m2 - 1), 2 * (m2 - 1) + 1
    if regola == "verso":
        y[hn], y[hm] = x[2 * e], x[2 * e + 1]
        return y
    mn = 0.5 * (x[h_in(ii2, jj2, n, x2)] + x[h_in(ii2, jj2, n, y_)])
    mm = 0.5 * (x[h_in(ii2, jj2, m_, x2)] + x[h_in(ii2, jj2, m_, y_)])
    if modo == "versore":
        v = _normalizza(mn - mm)
        y[hn], y[hm] = v, -v
    else:
        y[hn], y[hm] = mn, mm
    return y


# ------------------------------------------------------------------------------------------ un candidato
def candidato(Z, C, a, lato, regola, fattore=True):
    """### Lo stato di un candidato (`lato` None: la sola nascita; `(x, y)`: col flip), costruito sugli array, col SUO campo, il SUO Gauss, il SUO motore e la SUA energia della corsa."""
    import _u1_prototipo as U1
    import incidenza as IN
    import motore as MO
    import p6_u_breve as PB
    import _libro_dei_conti as LB
    import _vuoto_vivo_B as V
    mot, st, g0 = Z["mot"], Z["st"], C.campo
    inc = mot.inc
    ii, jj, n = np.asarray(inc.nodo[0::2], dtype=np.int64), np.asarray(inc.nodo[1::2], dtype=np.int64), int(inc.n)
    assert np.array_equal(ii, g0.ii) and np.array_equal(jj, g0.jj), "il campo e il motore NON hanno lo stesso grafo"
    t0 = time.time()
    i, j, k, l = indici_nascita(ii, jj, g0.vec, a)
    nodi = {"i": i, "j": j, "k": k, "l": l, "n": n}
    m = len(ii)
    keep_a = np.ones(m, dtype=bool)
    keep_a[a] = False
    ii2 = np.concatenate([ii[keep_a], [n] * 4])
    jj2 = np.concatenate([jj[keep_a], [i, j, k, l]])
    h_old = np.nonzero(np.isin(nodo_h(ii, jj), [i, j, k, l]))[0]
    h_new = np.nonzero(np.isin(nodo_h(ii2, jj2), [i, j, k, l, n]))[0]
    psi2 = nasci_array(ii, jj, a, nodi, st["psi_h"], "ampiezza")
    phi2 = nasci_array(ii, jj, a, nodi, st["phi_h"], "ampiezza")
    if fattore:
        _fattore(st["psi_h"], h_old, psi2, h_new)
        _fattore(st["phi_h"], h_old, phi2, h_new)
    geo2 = nasci_array(ii, jj, a, nodi, mot.geo.n, "versore")
    va = g0.vec[a]
    Aa = g0.A[a]
    A_n = [-0.5 * Aa, 0.5 * Aa]
    for c in (k, l):
        Phi = Aa + A_da(ii, jj, g0.A, j, c) + A_da(ii, jj, g0.A, c, i)
        A_n.append(0.5 * Phi - 0.5 * Aa - A_da(ii, jj, g0.A, c, i))      # ### B3: il mezzo triangolo (i, n, c) porta meta' flusso
    A2 = np.concatenate([g0.A[keep_a], A_n])
    E2 = np.concatenate([g0.E[keep_a], np.zeros(4)])
    vec2 = np.concatenate([g0.vec[keep_a], np.array([-0.5 * va, 0.5 * va, _v(ii, jj, g0.vec, i, k) - 0.5 * va, _v(ii, jj, g0.vec, i, l) - 0.5 * va])])
    keep = keep_a
    ii3, jj3, psi3, phi3, geo3, A3, E3, vec3, m_ = ii2, jj2, psi2, phi2, geo2, A2, E2, vec2, None
    if lato is not None:
        x_, y_ = lato
        com = vicini(ii2, jj2, x_) & vicini(ii2, jj2, y_)
        assert len(com) == 2 and n in com, "il quadrilatero di (%d, %d) non e' definito: %s" % (x_, y_, sorted(com))
        m_ = int(sorted(com - {n})[0])
        nodi["m"] = m_
        e = arco_fra(ii2, jj2, x_, y_)
        assert e < m - 1, "l'arco girato NON e' un arco vecchio: una crescita sola non basta"
        keep3 = np.ones(len(ii2), dtype=bool)
        keep3[e] = False
        quad = [n, x_, m_, y_]
        hq_old = np.nonzero(np.isin(nodo_h(ii2, jj2), quad))[0]
        ii3 = np.concatenate([ii2[keep3], [n]])
        jj3 = np.concatenate([jj2[keep3], [m_]])
        hq_new = np.nonzero(np.isin(nodo_h(ii3, jj3), quad))[0]
        psi3 = flip_array(ii2, jj2, nodi, x_, y_, m_, psi2, "ampiezza", regola)
        phi3 = flip_array(ii2, jj2, nodi, x_, y_, m_, phi2, "ampiezza", regola)
        if regola == "stella" and fattore:
            _fattore(psi2, hq_old, psi3, hq_new)
            _fattore(phi2, hq_old, phi3, hq_new)
        geo3 = flip_array(ii2, jj2, nodi, x_, y_, m_, geo2, "versore", regola)
        A_nm = 0.5 * ((A_da(ii2, jj2, A2, n, x_) + A_da(ii2, jj2, A2, x_, m_)) + (A_da(ii2, jj2, A2, n, y_) + A_da(ii2, jj2, A2, y_, m_)))
        A3 = np.concatenate([A2[keep3], [A_nm]])
        E3 = np.concatenate([E2[keep3], [0.0]])
        vec3 = np.concatenate([vec2[keep3], [_v(ii2, jj2, vec2, n, x_) + _v(ii2, jj2, vec2, x_, m_)]])
        keep = keep_a.copy()
        keep[e if e < a else e + 1] = False                              # ### `e` e' un indice di G2: sul grafo VECCHIO e' `e` (prima di `a`) o `e + 1`
        assert np.array_equal(ii3[:keep.sum()], ii[keep]) and np.array_equal(jj3[:keep.sum()], jj[keep]), "il grafo dei due passi NON e' quello di una crescita sola"
    mb = int(keep.sum())
    nuovi = len(ii3) - mb
    # ### il campo del candidato
    s0 = float(g0.s_a[0])
    assert np.all(g0.s_a == s0), "s_a NON e' uniforme: il valore degli archi nuovi non e' derivato (FERMO)"
    g = copy.deepcopy(g0)
    g.cresci(dove_di(keep), ii3, jj3, n + 1, vec3[mb:], A3[mb:], E3[mb:], np.full(nuovi, s0), np.full(nuovi, U1.L_SU_LS), lambda *_: U1.AREA)
    assert np.array_equal(g.A, A3), "A del campo cresciuto NON e' quella della regola"
    coerenti = bool(np.all(g.asg[:, 0] == -g.asg[:, 1]))
    rho3 = np.zeros(n + 1)
    np.add.at(rho3, nodo_h(ii3, jj3), np.sum(np.abs(psi3) ** 2, axis=1))
    res_senza = residuo(g, rho3)
    b = g.e * (rho3 - rho3.mean()) - g.div()
    media_b = float(b.mean())
    b = b - media_b
    Ec, _D = PB.gauss_sparso(g, b)
    g.E = g.E + Ec
    res = residuo(g, rho3)
    # ### il motore del candidato e la sua energia
    U3 = np.zeros((len(ii3), 2, 2), dtype=complex)
    u = g.u()
    U3[:, 0, 0] = u
    U3[:, 1, 1] = u
    inc3 = IN.Incidenza(ii3.astype(IN.INDICE), jj3.astype(IN.INDICE), n + 1, capacita=len(ii3))
    st3 = {"psi_h": psi3, "phi_h": phi3, "rho": np.zeros(n + 1), "Lambda": np.zeros(n + 1), "h_int": np.zeros(n + 1), "psi": np.zeros((n + 1, 2), dtype=complex)}
    dtau = np.asarray(mot.dtau, dtype=float)
    assert np.all(dtau == dtau[0]), "dtau NON uniforme: il valore del nodo nuovo non e' derivato"
    mot3 = MO.Motore(inc3, MO.Geometria(geo3, U3), st3, np.full(n + 1, dtau[0]), mot.sommatoria)
    mot3.densita_materia(st3)
    mot3.densita_vuoto(st3)
    mot3.elicita(st3)
    H = float(np.sum(LB.conti_per_nodo(inc3, mot3, st3, Z["e_K"], V.LAM_ZERO, Z["par"])["tot"])) + g.K() + g.V()
    return {"H": H, "nodi": nodi, "keep": keep, "ii": ii3, "jj": jj3, "psi": psi3, "phi": phi3, "geo": geo3, "U": U3, "campo": g, "st": st3, "mot": mot3,
            "res": res, "res_senza_gauss": res_senza, "media_b": media_b, "coerenti": coerenti, "lato": lato, "t": time.time() - t0, "mb": mb}


def residuo(g, rho):
    """### `max |div E - e (rho - media)| / (e max rho)`: la formula di `mattone.Campi.residuo`."""
    G = g.div() - g.e * (rho - rho.mean())
    return float(np.max(np.abs(G))) / (g.e * float(rho.max()))


def energia_corsa(Z, C):
    import conti as CO
    return float(np.sum(CO.conti_nodo(Z)["tot"])) + C.campo.K() + C.campo.V()


def regola(Z, C, a, giro="stella"):
    """### I cinque candidati e la scelta (A). `(R, scelto)`."""
    nas = candidato(Z, C, a, None, giro)
    nd = nas["nodi"]
    lati = ((nd["i"], nd["k"]), (nd["j"], nd["k"]), (nd["j"], nd["l"]), (nd["i"], nd["l"]))
    cand = [candidato(Z, C, a, lt, giro) for lt in lati]
    Hs = np.array([c["H"] for c in cand])
    o = np.argsort(Hs, kind="stable")
    gap = float(Hs[o[1]] - Hs[o[0]])
    pari = gap < GUARDIA * abs(float(Hs[o[0]]))
    scelto = nas if pari else cand[int(o[0])]
    R = {"H": Hs.tolist(), "H_nascita": nas["H"], "scelto": -1 if pari else int(o[0]), "gap": gap / abs(float(Hs[o[0]])), "lati": lati, "nodi": scelto["nodi"],
         "t": [nas["t"]] + [c["t"] for c in cand], "cand": [nas] + cand}
    return R, scelto


def applica(Z, C, cont, S):
    """### Lo stato scelto nel motore VERO in UNA crescita; il campo, `Theta`, le posizioni, `cs`; `(info)`."""
    import _u1_prototipo as U1
    from solitone import posizioni as PZ
    from solitone import tick_lapse as TL
    LC = PS.LC
    mot, st = Z["mot"], Z["st"]
    assert Z["z"]["inc"] is mot.inc, "la scena e il motore NON hanno la stessa incidenza"
    nd, keep, mb = S["nodi"], S["keep"], S["mb"]
    n = nd["n"]
    nuovi_jj = [nd["i"], nd["j"], nd["k"], nd["l"]] + ([nd["m"]] if "m" in nd else [])
    assert float(np.max(np.abs(st["psi"]))) == 0.0, "st['psi'] per nodo NON e' tutto zero: il valore del nodo nuovo non e' derivato (FERMO)"
    st3 = S["st"]
    cs_n = None
    if mot.cs is not None:
        cs_n = float(Z["s"]) * float(TL.N_di(np.array([st3["rho"][n]]), C.legge)[0])      # ### dalla legge (tick_lapse.cs_di sul nodo nuovo)
    ini = {"psi_h": S["psi"][2 * mb:], "phi_h": S["phi"][2 * mb:], "geo_n": S["geo"][2 * mb:], "geo_U": S["U"][mb:], "dtau": [float(mot.dtau[0])],
           "nodo:rho": [st3["rho"][n]], "nodo:Lambda": [st3["Lambda"][n]], "nodo:h_int": [st3["h_int"][n]], "nodo:psi": np.zeros((1, 2), dtype=complex)}
    if cs_n is not None:
        ini["cs"] = [cs_n]
    mot.apri_tick()
    dove = mot.cresci(keep, [n] * len(nuovi_jj), nuovi_jj, 1, ini)
    mot.chiudi_tick()
    assert np.array_equal(np.asarray(mot.inc.nodo), nodo_h(S["ii"], S["jj"])), "il grafo del motore NON e' quello del candidato"
    assert np.array_equal(dove, dove_di(keep)), "la permutazione del motore NON e' quella della regola"
    stella = np.isin(nodo_h(S["ii"], S["jj"]), [nd[x] for x in nd])
    fuori = ~stella
    ok_fuori = bool(np.array_equal(st["psi_h"][fuori], S["psi"][fuori]) and np.array_equal(st["phi_h"][fuori], S["phi"][fuori]))
    st["psi_h"][...] = S["psi"]
    st["phi_h"][...] = S["phi"]
    ok_geo = bool(np.array_equal(mot.geo.n, S["geo"]))
    mot.densita_materia(st)
    mot.densita_vuoto(st)
    mot.elicita(st)
    C.campo = S["campo"]
    U1.scrivi_U(mot, C.campo)
    ok_U = bool(np.array_equal(mot.geo.U, S["U"]))
    cont.cresci(keep, len(nuovi_jj))
    PZ.cresci(Z, nd["i"], nd["j"], 1)
    if LC.STATO["cs"] is not None:
        c = LC.STATO["cs"]
        LC.STATO["cs"] = np.concatenate([c, [0.5 * (c[nd["i"]] + c[nd["j"]])]])
    return {"ok_fuori": ok_fuori, "ok_geo": ok_geo, "ok_U": ok_U, "cs_n": cs_n}


# ------------------------------------------------------------------------------------------ le prove
def grafo_ok(ii, jj, n):
    import scipy.sparse as sp
    d = np.bincount(nodo_h(ii, jj), minlength=n)
    eulero = int(np.sum(6 - d)) == 0 and len(ii) == 3 * n
    u, v = np.minimum(ii, jj), np.maximum(ii, jj)
    doppi = len(np.unique(u * n + v)) == len(u)
    A = sp.csr_matrix((np.ones(2 * len(u)), (np.concatenate([u, v]), np.concatenate([v, u]))), shape=(n, n))
    tri = bool(np.all(np.asarray((A @ A).tocsr()[u, v]).ravel() == 2.0))
    return eulero, doppi, tri, sorted(set(d.tolist()))


def versori_opposti(S, mb):
    """### ogni arco nuovo: `|geo(a -> b) + geo(b -> a)|` massimo, in ulp; e l'ultimo (il flip) al bit."""
    g = S["geo"]
    nuovi = range(mb, len(S["ii"]))
    d = [float(np.max(np.abs(g[2 * q] + g[2 * q + 1]))) for q in nuovi]
    return d


def caso():
    import json
    import _presidio
    from solitone import toro as TO
    MT, CV = PS.MT, PS.CV
    _presidio.avvia(os.path.join(_QUI, "mitosi_corsa.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    esiti = []
    print("=" * 130)
    print("LA REGOLA INTERA NELLA CORSA, I CASI NOTI (Luca 2026-11-20 16:37, 17:03; la carta sez. 10.3): una nascita FORZATA su C2 a k %d" % MC.K_C2)
    print("=" * 130)
    with np.load(os.path.join(DIR_T, "candidati.npz")) as d:
        archi, T = d["archi"].copy(), d["T"].copy()
    a = int(archi[np.argsort(T, kind="stable")[0]])
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, meta, cs, s = MC.CSB.riprendi(Z, MC.F_C2, False, rho_c, e)
        PS.PO.accendi(cs)
        try:
            g, info = MC.campo_generico(Z, C)
            cont = MC.theta_C2()
            mot, st = Z["mot"], Z["st"]
            ii, jj = np.asarray(mot.inc.nodo[0::2]), np.asarray(mot.inc.nodo[1::2])
            # ---------------------------------------------------------------- K0, V-0
            H0 = energia_corsa(Z, C)
            import incidenza as IN
            import motore as MO
            import _libro_dei_conti as LB
            import _vuoto_vivo_B as V
            inc0 = IN.Incidenza(ii.astype(IN.INDICE), jj.astype(IN.INDICE), mot.inc.n, capacita=len(ii))
            st0 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in st.items()}
            mot0 = MO.Motore(inc0, MO.Geometria(mot.geo.n.copy(), mot.geo.U.copy()), st0, np.asarray(mot.dtau, dtype=float).copy(), mot.sommatoria)
            H0b = float(np.sum(LB.conti_per_nodo(inc0, mot0, st0, Z["e_K"], V.LAM_ZERO, Z["par"])["tot"])) + C.campo.K() + C.campo.V()
            print("### K0: l'energia della corsa %.17e; con un motore costruito sugli array %.17e: %s" % (H0, H0b, "AL BIT" if H0 == H0b else "### DIVERSE"))
            esiti.append(("K0: il conto di un motore costruito sugli array = il conto della corsa AL BIT", H0 == H0b))
            vn = C.campo.vec / np.linalg.norm(C.campo.vec, axis=1)[:, None]
            d0 = max(float(np.max(np.abs(mot.geo.n[0::2, :2] - vn))), float(np.max(np.abs(mot.geo.n[1::2, :2] + vn))), float(np.max(np.abs(mot.geo.n[:, 2]))))
            print("### V-0: i versori di oggi contro le direzioni dei vettori d'arco del campo (+ in ii, - in jj, z = 0): lo scarto massimo %.2e (%.1f ulp)" % (d0, d0 / EPS))
            esiti.append(("V-0: i versori di oggi = le direzioni dei vettori d'arco entro 4 ulp (il riferimento di V-b)", d0 <= 4 * EPS))
            M0 = float(np.sum(np.abs(st["psi_h"]) ** 2))
            V0 = float(np.sum(np.abs(st["phi_h"]) ** 2))
            rho0 = MT.rho_di(Z)
            res0 = residuo(C.campo, rho0)
            # ---------------------------------------------------------------- la regola
            t1 = time.time()
            R, S = regola(Z, C, a, "stella")
            t_regola = time.time() - t1
            nd = R["nodi"]
            print("### l'arco %d (%d -> %d), il primo nell'ordine di scatto; k %d, l %d, n %d" % (a, nd["i"], nd["j"], nd["k"], nd["l"], nd["n"]))
            print("    H prima %.10e; la sola nascita %.10e (DH %+.6e)" % (H0, R["H_nascita"], R["H_nascita"] - H0))
            for q, (lt, h) in enumerate(zip(R["lati"], R["H"])):
                print("    il flip %d (%d, %d): H %.10e (DH dalla nascita %+.6e)%s" % (q, lt[0], lt[1], h, h - R["H_nascita"], "   <- SCELTO" if q == R["scelto"] else ""))
            print("    lo scarto fra il migliore e il secondo %.3e |H|; il tempo: %s s (la regola intera %.1f s)" % (R["gap"], ["%.1f" % x for x in R["t"]], t_regola))
            mb = S["mb"]
            # ---------------------------------------------------------------- V-a, V-b
            dv = versori_opposti(S, mb)
            print("### V-a: |geo(a->b) + geo(b->a)| sugli archi nuovi: %s" % ["%.1e" % x for x in dv])
            ok_va = all(x <= 4 * EPS for x in dv[:4]) and (len(dv) < 5 or dv[4] == 0.0)
            esiti.append(("V-a: versori opposti sugli archi nuovi (nascita entro 4 ulp, flip AL BIT)", ok_va))
            nas = R["cand"][0]
            gv = nas["campo"].vec[-4:]
            dirs = gv / np.linalg.norm(gv, axis=1)[:, None]
            gn = nas["geo"][-8:]
            dvb = max(float(np.max(np.abs(gn[0::2, :2] - dirs))), float(np.max(np.abs(gn[1::2, :2] + dirs))), float(np.max(np.abs(gn[:, 2]))))
            print("### V-b: i versori nati contro le direzioni del punto medio (i vettori d'arco nuovi): lo scarto massimo %.2e (%.1f ulp)" % (dvb, dvb / EPS))
            esiti.append(("V-b: la nascita ridà la direzione del punto medio entro 4 ulp", dvb <= 4 * EPS))
            # ---------------------------------------------------------------- F3
            eu, dp, tri, gradi = grafo_ok(S["ii"], S["jj"], nd["n"] + 1)
            print("### F3: Eulero %s, nessun arco doppio %s, ogni arco in due triangoli %s, i gradi %s; i segni delle placchette coerenti %s" % (eu, dp, tri, gradi, S["coerenti"]))
            esiti.append(("F3: Eulero, nessun doppio, due triangoli per arco, placchette coerenti", eu and dp and tri and S["coerenti"]))
            # ---------------------------------------------------------------- P1 (e DEVE FALLIRE senza il fattore)
            M1 = float(np.sum(np.abs(S["psi"]) ** 2))
            V1 = float(np.sum(np.abs(S["phi"]) ** 2))
            dM, dV = abs(M1 - M0) / M0, abs(V1 - V0) / V0
            print("### P1: la materia %.15e -> %.15e (%.1e); il vuoto %.15e -> %.15e (%.1e)" % (M0, M1, dM, V0, V1, dV))
            esiti.append(("P1: le norme M e V entro 1e-12 relativo", dM <= 1e-12 and dV <= 1e-12))
            lato = R["lati"][R["scelto"]] if R["scelto"] >= 0 else None
            Sf = candidato(Z, C, a, lato, "stella", fattore=False)
            dMf = abs(float(np.sum(np.abs(Sf["psi"]) ** 2)) - M0) / M0
            dVf = abs(float(np.sum(np.abs(Sf["phi"]) ** 2)) - V0) / V0
            print("    DEVE FALLIRE: senza il fattore di stella: M %.1e, V %.1e" % (dMf, dVf))
            esiti.append(("DEVE FALLIRE: senza il fattore di stella le norme escono da 1e-12", dMf > 1e-12 or dVf > 1e-12))
            # ---------------------------------------------------------------- P3
            print("### P3: il residuo di Gauss prima %.3e; dopo la nascita (Gauss vero) %.3e; la media tolta dal bersaglio %.1e; DEVE FALLIRE senza Gauss %.3e" % (res0, S["res"], S["media_b"], S["res_senza_gauss"]))
            esiti.append(("P3: il residuo dopo la nascita sotto 10 volte quello di prima", S["res"] <= 10 * res0))
            esiti.append(("DEVE FALLIRE: gli archi nuovi con E = 0 senza Gauss: sopra 10 volte", S["res_senza_gauss"] > 10 * res0))
            # ---------------------------------------------------------------- P9: lo stato scelto nel motore vero
            t1 = time.time()
            inf = applica(Z, C, cont, S)
            H1 = energia_corsa(Z, C)
            d9 = abs(H1 - S["H"]) / abs(S["H"])
            print("### P9: nel motore vero (in %.1f s): fuori dalla stella AL BIT %s, i versori %s, U %s; cs del nodo nuovo %.17g; l'energia della corsa riletta %.17e contro il candidato %.17e: %.1e |H|" % (
                time.time() - t1, inf["ok_fuori"], inf["ok_geo"], inf["ok_U"], inf["cs_n"] if inf["cs_n"] is not None else float("nan"), H1, S["H"], d9))
            esiti.append(("P9: l'energia riletta dal motore vero = H(prima) + DH entro 1e-12 |H|", d9 <= 1e-12))
            esiti.append(("lo stato nel motore vero: fuori dalla stella AL BIT, i versori, U", inf["ok_fuori"] and inf["ok_geo"] and inf["ok_U"]))
            print("    E_persa di questa nascita %+.6e; Theta %d archi; le posizioni del nodo nuovo (%.4f, %.4f)" % (-(H1 - H0), cont.theta.size, Z["m1"][-1], Z["m2"][-1]))
            esiti.append(("Theta e le posizioni seguono il grafo", cont.theta.size == mot.inc.m and len(Z["m1"]) == mot.inc.n))
        finally:
            PS.LC.spegni()
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-112s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("caso")
    x = ap.parse_args(argv)
    if x.cmd == "caso":
        return caso()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
