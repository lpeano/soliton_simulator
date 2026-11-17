# -*- coding: utf-8 -*-
r"""**LA PROVA DELLA U(1) SUL GRAFO GENERICO** *(il ramo `mitosi`, B3; mandato di Luca `2026-11-17` `16:38`)*.

    E:\python\py3132\python.exe csv/solitone/prova_u1_generico.py > doc/referti_l2/mitosi_B3_u1.txt

**Il caso noto** *(il toro `L 24`, gli archi `a1`, `a2`, `a1 + a2`; `A`, `E`, `s_a` casuali, seme `0`)*: **`CampoGenerico` contro `_u1_prototipo.Campo`**: `forza`, `div`, `K` AL BIT; **`B` come insieme AL BIT** *(le placchette in un altro ordine)*; **`V` entro `8` ulp relativi** *(una somma su tutte le placchette in un altro ordine: DICHIARATO)*; **`200` passi di `tick_campo`: `A` e `E` AL BIT**, **forma compatta e non compatta.**
**La crescita** *(la divisione dell'arco `i -> j` col nodo `n -> i, j, k, l`, come `nascita_dentro_fuori.nasci`; `A` degli archi nuovi a META' flusso)*:
- **le placchette `m - n`, ogni arco in due**; **il flusso dei due triangoli vecchi = la somma dei quattro nuovi, e META' ciascuno** *(entro `1e-15` assoluto)*;
- **le aree dei triangoli SOPRAVVISSUTI restano al bit**; **`cresci` = il campo COSTRUITO sul grafo nuovo** *(stesse `A`, `E`, `s_a`, `hodge`, aree): `forza`, `div`, `K`, `V` AL BIT*;
- **Gauss sul grafo nuovo** *(`p6_u_breve.gauss_sparso`, e `gauss_riuso` con la cache: SVUOTATA da `cresci`)*: **il residuo `max |div E - b| / max |b|` sotto `1e-12`**;
- **I CASI CHE DEVONO FALLIRE:** `A_nuovi` della taglia sbagliata; **un grafo con un arco in UN solo triangolo** *(il toro con un arco tolto)*; **la cache di Gauss NON svuotata** *(rimessa a mano dopo `cresci`: DEVE alzare o dare un residuo grande)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
_RADICE = os.path.dirname(_CSV)
for _p in (_QUI, _CSV, os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

L, SEME, PASSI = 24, 0, 200
EPS = np.finfo(float).eps


def toro(L):
    import toro as TO
    v = np.arange(L * L)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    ii = np.repeat(v, 3)
    jj = np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1)
    A1, A2 = TO.vettori()
    A1, A2 = np.asarray(A1, dtype=float)[:2], np.asarray(A2, dtype=float)[:2]
    vec = np.tile(np.stack([A1, A2, A1 + A2]), (L * L, 1))
    return ii, jj, L * L, vec


def dividi(ii, jj, n, vec, a):
    """### la divisione dell'arco `a = i -> j`: `(tieni, nuovi_ii, nuovi_jj, vec_nuovi, nodi)` -- gli archi `n -> i, j, k, l` (`k` a sinistra di `i -> j`)."""
    i, j = int(ii[a]), int(jj[a])
    vic = lambda x: set(jj[ii == x].tolist()) | set(ii[jj == x].tolist())  # noqa: E731
    com = sorted(vic(i) & vic(j))
    assert len(com) == 2

    def d(x, y):
        q = np.where((ii == x) & (jj == y))[0]
        return vec[q[0]] if len(q) else -vec[np.where((ii == y) & (jj == x))[0][0]]
    va = vec[a]
    cr = [va[0] * d(i, c)[1] - va[1] * d(i, c)[0] for c in com]
    k, l = (com[0], com[1]) if cr[0] > 0 else (com[1], com[0])
    tieni = np.ones(len(ii), dtype=bool)
    tieni[a] = False
    vn = np.array([-0.5 * va, 0.5 * va, d(i, k) - 0.5 * va, d(i, l) - 0.5 * va])
    return tieni, [n] * 4, [i, j, k, l], vn, {"n": n, "i": i, "j": j, "k": k, "l": l}, d


def main():
    import _presidio
    import _u1_prototipo as U1
    import incidenza as IN
    import p6_u_breve as PB
    import gauss_riuso as GR
    import u1_generico as UG
    _presidio.avvia(os.path.join(_QUI, "u1_generico.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA PROVA DELLA U(1) SUL GRAFO GENERICO (il ramo mitosi, B3; Luca 2026-11-17 16:38)")
    print("=" * 130)
    esiti = []
    ii, jj, n, vec = toro(L)
    m = len(ii)
    rng = np.random.default_rng(SEME)
    s_a = 0.15 * (1.0 + 0.1 * rng.random(m))      # ### attorno al s delle corse (0.15): la dinamica stabile; con s_a fino a 1.5 divergeva (NaN), la prima corsa NON registrata (dichiarato)
    A0, E0 = rng.standard_normal(m), rng.standard_normal(m)
    area_toro = lambda *_: U1.AREA  # noqa: E731
    # ---------------------------------------------------------------- il caso noto
    for forma in U1.FORME:
        p = U1.Campo(ii, jj, (L, L), 0.7, forma, s_a)
        g = UG.CampoGenerico(ii, jj, n, vec, 0.7, forma, s_a, np.full(m, U1.L_SU_LS), area_toro)
        for c in (p, g):
            c.A[...] = A0
            c.E[...] = E0
        Bp, Bg = np.sort(p.B()), np.sort(g.B())
        uguali = {"forza": np.array_equal(p.forza(), g.forza()), "div": np.array_equal(p.div(), g.div()), "K": p.K() == g.K(), "B (insieme)": np.array_equal(Bp, Bg), "w": np.array_equal(p.w, g.w)}
        dV = abs(p.V() - g.V()) / abs(p.V())
        for _ in range(PASSI):
            U1.tick_campo(p)
            U1.tick_campo(g)
        dinamica = np.array_equal(p.A, g.A) and np.array_equal(p.E, g.E)
        print("### il caso noto (%s): %s; V relativa %.1e (%.1f ulp); dopo %d tick_campo A, E al bit: %s" % (forma, uguali, dV, dV / EPS, PASSI, dinamica))
        esiti.append(("il caso noto (%s): forza, div, K, w, B come insieme AL BIT" % forma, all(uguali.values())))
        esiti.append(("il caso noto (%s): V entro 8 ulp relativi (l'ordine delle placchette, dichiarato)" % forma, dV <= 8 * EPS))
        esiti.append(("il caso noto (%s): %d tick_campo, A e E AL BIT" % (forma, PASSI), dinamica))
    # ---------------------------------------------------------------- la crescita
    print("-" * 130)
    a = 3 * (12 * L + 12)
    g = UG.CampoGenerico(ii, jj, n, vec, 0.7, "noncompatto", s_a, np.full(m, U1.L_SU_LS), area_toro)
    g.A[...] = A0
    g.E[...] = E0
    B0 = g.B()
    cic0 = list(g.cicli)
    inc = IN.Incidenza(ii.astype(IN.INDICE), jj.astype(IN.INDICE), n, capacita=2 * m)
    tieni, nii, njj, vn, nodi, d = dividi(ii, jj, n, vec, a)
    i, j, k, l = nodi["i"], nodi["j"], nodi["k"], nodi["l"]
    Aa = A0[a]

    def Ad(x, y):
        q = np.where((ii == x) & (jj == y))[0]
        return A0[q[0]] if len(q) else -A0[np.where((ii == y) & (jj == x))[0][0]]
    A_n = [-0.5 * Aa, 0.5 * Aa, 0.0, 0.0]
    for c, q in ((k, 2), (l, 3)):
        Phi = Aa + Ad(j, c) + Ad(c, i)
        A_n[q] = 0.5 * Phi - 0.5 * Aa - Ad(c, i)        # ### A(n -> c): il mezzo triangolo (i, n, c) porta META' flusso
    dove = inc.cresci(tieni, nii, njj, 1)
    ii2, jj2 = np.asarray(inc.nodo[0::2], dtype=np.int64), np.asarray(inc.nodo[1::2], dtype=np.int64)
    area_mezzi = lambda *_: 0.5 * U1.AREA  # noqa: E731  (i mezzi triangoli: PROVVISORIO, dichiarato)
    GR.accendi()
    try:
        b0 = rng.standard_normal(n)
        b0 -= b0.mean()
        _E, _D = PB.gauss_sparso(g, b0)                               # ### la cache si riempie col grafo VECCHIO
        vecchia = dict(D=GR.CACHE["D"], risolvi=GR.CACHE["risolvi"])
        g.cresci(dove, ii2, jj2, n + 1, vn, A_n, np.zeros(4), np.full(4, 1.0), np.full(4, U1.L_SU_LS), area_mezzi)
        print("### la crescita: l'arco %d (%d -> %d), il nodo %d -> %d, %d, %d, %d; m %d -> %d; le placchette %d (m - n = %d)" % (a, i, j, n, i, j, k, l, m, g.m, len(g.P), g.m - g.n))
        esiti.append(("la crescita: placchette = m - n, ogni arco in due (il controllo del costruttore)", len(g.P) == g.m - g.n))
        # ### il flusso: i due triangoli vecchi (i, j, k), (i, j, l) contro i quattro nuovi
        B1 = g.B()
        vecchi = [q for q, c in enumerate(cic0) if {i, j} <= set(c)]
        nuovi = [q for q, c in enumerate(g.cicli) if n in c]
        Fv = {(set(cic0[q]) - {i, j}).pop(): B0[q] for q in vecchi}
        ok_flusso = True
        for c in (k, l):
            mezzi = [B1[q] for q in nuovi if c in g.cicli[q]]
            ok_flusso &= abs(sum(mezzi) - Fv[c]) <= 1e-15 * max(1.0, abs(Fv[c])) * 4 and all(abs(x - 0.5 * Fv[c]) <= 4e-16 * max(1.0, abs(Fv[c])) for x in mezzi)
            print("    il triangolo (i, j, %d): il flusso di prima %+.17e; i due mezzi %s" % (c, Fv[c], ["%+.17e" % x for x in mezzi]))
        esiti.append(("il flusso dei due triangoli vecchi = la somma dei mezzi, e META' ciascuno (entro pochi ulp)", ok_flusso))
        sopr = {tuple(sorted(c)): q for q, c in enumerate(cic0)}
        aree_ok = all(g.area[q] == U1.AREA for q, c in enumerate(g.cicli) if tuple(sorted(c)) in sopr) and all(g.area[q] == 0.5 * U1.AREA for q in nuovi)
        esiti.append(("le aree: i triangoli sopravvissuti al bit, i nuovi quelle dichiarate", aree_ok))
        # ### cresci = il campo COSTRUITO sul grafo nuovo
        aree_dopo = {tuple(sorted(c)): x for c, x in zip(g.cicli, g.area)}
        h = UG.CampoGenerico(ii2, jj2, n + 1, g.vec, 0.7, "noncompatto", g.s_a, g.hodge_a, lambda *c: aree_dopo[tuple(sorted(c))])
        h.A[...] = g.A
        h.E[...] = g.E
        cos = np.array_equal(h.forza(), g.forza()) and np.array_equal(h.div(), g.div()) and h.K() == g.K() and h.V() == g.V() and np.array_equal(h.P, g.P)
        esiti.append(("cresci = il campo costruito sul grafo nuovo: P, forza, div, K, V AL BIT", cos))
        # ### Gauss sul grafo nuovo, con la cache svuotata da cresci
        b = rng.standard_normal(n + 1)
        b -= b.mean()
        E, D = PB.gauss_sparso(g, b)
        res = float(np.max(np.abs(g.div(E) - b))) / float(np.max(np.abs(b)))
        print("### Gauss sul grafo nuovo (gauss_riuso, la cache svuotata da cresci, %d fattorizzazioni): il residuo %.2e" % (GR.CACHE["costruite"], res))
        esiti.append(("Gauss sul grafo nuovo: il residuo sotto 1e-12", res <= 1e-12))
        # ### DEVE FALLIRE: la cache VECCHIA rimessa a mano
        GR.CACHE.update(campo=g, D=vecchia["D"], risolvi=vecchia["risolvi"])   # ### la cache del grafo VECCHIO, rimessa a mano
        try:
            E_v, _ = PB.gauss_sparso(g, b)
            res_v = float(np.max(np.abs(g.div(E_v) - b))) / float(np.max(np.abs(b)))
            fall = res_v > 1e-6
        except Exception as ex:  # noqa: BLE001
            fall, res_v = True, str(ex)[:60]
        GR.CACHE.update(campo=None, D=None, risolvi=None)
        print("    DEVE FALLIRE: la cache del grafo VECCHIO: %s" % (res_v,))
        esiti.append(("DEVE FALLIRE: Gauss con la cache del grafo vecchio (alza, o il residuo e' grande)", fall))
    finally:
        GR.spegni()
    # ---------------------------------------------------------------- gli altri casi che devono fallire
    g2 = UG.CampoGenerico(ii, jj, n, vec, 0.7, "noncompatto", s_a, np.full(m, U1.L_SU_LS), area_toro)
    inc2 = IN.Incidenza(ii.astype(IN.INDICE), jj.astype(IN.INDICE), n, capacita=2 * m)
    t2, nii2, njj2, vn2, _n2, _d2 = dividi(ii, jj, n, vec, a)
    dove2 = inc2.cresci(t2, nii2, njj2, 1)
    try:
        g2.cresci(dove2, inc2.nodo[0::2], inc2.nodo[1::2], n + 1, vn2, np.zeros(3), np.zeros(4), np.ones(4), np.full(4, U1.L_SU_LS), area_mezzi)
        f1 = False
    except AssertionError as ex:
        f1 = "A_nuovi" in str(ex)
    esiti.append(("DEVE FALLIRE: A_nuovi della taglia sbagliata (per la chiave giusta)", f1))
    try:
        t3 = np.ones(m, dtype=bool)
        t3[a] = False
        UG.CampoGenerico(ii[t3], jj[t3], n, vec[t3], 0.7, "noncompatto", s_a[t3], np.full(m - 1, U1.L_SU_LS), area_toro)
        f2 = False
    except AssertionError as ex:
        f2 = "triangolazione" in str(ex) or "due placchette" in str(ex)
    esiti.append(("DEVE FALLIRE: il toro con un arco tolto (archi in un solo triangolo)", f2))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
