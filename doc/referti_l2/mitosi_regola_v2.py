# -*- coding: utf-8 -*-
r"""**LA REGOLA INTERA CON L'ORIENTAMENTO EREDITATO -- LA V2** *(D2 di Luca `2026-11-21` `23:13`; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `4.2`)*. [[PROGETTO-MITOSI]]

**`mitosi_regola.py` e' IN USO e non si tocca:** qui `candidato` e `regola` riga per riga, con TRE differenze:
1. **`indici_nascita_v2`:** `k` = il terzo vertice del triangolo il cui CICLO contiene `i -> j`, `l` quello dell'altro *(dall'orientamento del campo, nessun prodotto vettoriale)*;
2. **`nascita_ori`, `flip_ori`:** l'orientamento dei triangoli nuovi EREDITATO *(la nascita: nel ciclo di `T_k` e di `T_l` si sostituisce `j`, poi `i`, con `n`; il flip: il ciclo del quadrilatero `n - x - m - y` dai due triangoli orientati della diagonale vecchia, e i due nuovi lo seguono)*;
3. **il campo del candidato cresce con `ori=`** *(`campo_orientato.CampoOrientato`)*.
**Il resto** *(le ampiezze, i versori, `A`, `E`, Gauss, il motore del candidato, l'energia della corsa, la scelta (A), `applica`)* **e' `mitosi_regola`, importato.** **`ricostruisci`:** l'orientamento lungo le nascite registrate *(O1)*.
"""
import copy
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_regola as MR  # noqa: E402
import campo_orientato as CO  # noqa: E402

MC, PS = MR.MC, MR.PS
GUARDIA = MR.GUARDIA
nodo_h, arco_fra, h_in, vicini, A_da, dove_di, _v, _fattore, nasci_array, flip_array, residuo, energia_corsa, applica, grafo_ok = (
    MR.nodo_h, MR.arco_fra, MR.h_in, MR.vicini, MR.A_da, MR.dove_di, MR._v, MR._fattore, MR.nasci_array, MR.flip_array, MR.residuo, MR.energia_corsa, MR.applica, MR.grafo_ok)


def indici_nascita_v2(ii, jj, ori, a):
    """### `(i, j, k, l)`: `k` il terzo vertice del triangolo il cui ciclo contiene `i -> j` *(D2 b)*."""
    i, j = int(ii[a]), int(jj[a])
    com = sorted(vicini(ii, jj, i) & vicini(ii, jj, j))
    assert len(com) == 2, "l'arco %d non ha due vicini comuni (%s)" % (a, com)
    dentro = [CO.contiene(list(ori[tuple(sorted((i, j, c)))]), i, j) for c in com]
    assert dentro[0] != dentro[1], "i due triangoli dell'arco %d percorrono %d -> %d nello STESSO verso: l'orientamento NON e' coerente" % (a, i, j)
    k, l = (com[0], com[1]) if dentro[0] else (com[1], com[0])
    return i, j, k, l


def _sost(cyc, vecchio, nuovo):
    return tuple(nuovo if v == vecchio else v for v in cyc)


def nascita_ori(ori, i, j, k, l, n):
    """### l'orientamento dopo la nascita di `n` sull'arco `i -> j` della stella `i - k - j - l`."""
    out = dict(ori)
    Tk, Tl = ori[tuple(sorted((i, j, k)))], ori[tuple(sorted((i, j, l)))]
    assert CO.contiene(list(Tk), i, j) and CO.contiene(list(Tl), j, i), "la stella non e' orientata come la regola vuole"
    del out[tuple(sorted((i, j, k)))], out[tuple(sorted((i, j, l)))]
    for T in (Tk, Tl):
        for vecchio in (j, i):
            c = _sost(T, vecchio, n)
            out[tuple(sorted(c))] = CO.canonico(c)
    return out


def flip_ori(ori, n, x, y, m):
    """### l'orientamento dopo il flip di `x - y` in `n - m` nel quadrilatero `n - x - m - y`."""
    out = dict(ori)
    T1, T2 = list(ori[tuple(sorted((n, x, y)))]), list(ori[tuple(sorted((m, x, y)))])
    if CO.contiene(T1, x, y):
        assert CO.contiene(T2, y, x), "i due triangoli della diagonale %d - %d NON sono orientati in modo coerente" % (x, y)
        nuovi = ((n, x, m), (n, m, y))
    else:
        assert CO.contiene(T1, y, x) and CO.contiene(T2, x, y), "i due triangoli della diagonale %d - %d NON sono orientati in modo coerente" % (x, y)
        nuovi = ((n, y, m), (n, m, x))
    del out[tuple(sorted((n, x, y)))], out[tuple(sorted((m, x, y)))]
    for c in nuovi:
        out[tuple(sorted(c))] = CO.canonico(c)
    return out


def ricostruisci(ori0, bilanci):
    """### O1: l'orientamento lungo le nascite registrate *(la nascita, poi il flip col lato scelto)*; e `k`, `l` dall'ordine ciclico contro quelli registrati. `(ori, diversi_kl)`."""
    ori = dict(ori0)
    diversi = []
    for b in bilanci:
        nd = b["nodi"]
        i, j, n = nd["i"], nd["j"], nd["n"]
        com = [c for c in (nd["k"], nd["l"])]
        dentro = [CO.contiene(list(ori[tuple(sorted((i, j, c)))]), i, j) for c in com]
        k_c = com[0] if dentro[0] else com[1]
        if k_c != nd["k"]:
            diversi.append((b["k"], nd["k"], k_c))
        ori = nascita_ori(ori, i, j, nd["k"], nd["l"], n)
        if b["scelto"] >= 0:
            lati = ((i, nd["k"]), (j, nd["k"]), (j, nd["l"]), (i, nd["l"]))
            x, y = lati[b["scelto"]]
            ori = flip_ori(ori, n, x, y, nd["m"])
    return ori, diversi


# ------------------------------------------------------------------------------------------ il candidato: mitosi_regola.candidato riga per riga
def candidato(Z, C, a, lato, regola, fattore=True, inverti=None):
    """### `mitosi_regola.candidato` riga per riga; `k`, `l` e l'orientamento dei nati dallo STATO. `inverti`: un triangolo il cui ciclo si inverte a mano *(SOLO la prova O4)*."""
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
    assert isinstance(g0, CO.CampoOrientato), "il campo NON ha l'orientamento: la v2 lo vuole"
    t0 = time.time()
    i, j, k, l = indici_nascita_v2(ii, jj, g0.ori, a)
    nodi = {"i": i, "j": j, "k": k, "l": l, "n": n}
    ori = nascita_ori(g0.ori, i, j, k, l, n)
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
        A_n.append(0.5 * Phi - 0.5 * Aa - A_da(ii, jj, g0.A, c, i))
    A2 = np.concatenate([g0.A[keep_a], A_n])
    E2 = np.concatenate([g0.E[keep_a], np.zeros(4)])
    vec2 = np.concatenate([g0.vec[keep_a], np.array([-0.5 * va, 0.5 * va, _v(ii, jj, g0.vec, i, k) - 0.5 * va, _v(ii, jj, g0.vec, i, l) - 0.5 * va])])   # ### il DISEGNO
    keep = keep_a
    ii3, jj3, psi3, phi3, geo3, A3, E3, vec3, m_ = ii2, jj2, psi2, phi2, geo2, A2, E2, vec2, None
    if lato is not None:
        x_, y_ = lato
        com = vicini(ii2, jj2, x_) & vicini(ii2, jj2, y_)
        assert len(com) == 2 and n in com, "il quadrilatero di (%d, %d) non e' definito: %s" % (x_, y_, sorted(com))
        m_ = int(sorted(com - {n})[0])
        nodi["m"] = m_
        ori = flip_ori(ori, n, x_, y_, m_)
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
        keep[e if e < a else e + 1] = False
        assert np.array_equal(ii3[:keep.sum()], ii[keep]) and np.array_equal(jj3[:keep.sum()], jj[keep]), "il grafo dei due passi NON e' quello di una crescita sola"
    if inverti is not None:
        c = ori[tuple(sorted(inverti))]
        ori[tuple(sorted(inverti))] = CO.canonico((c[0], c[2], c[1]))          # ### SOLO la prova O4
    mb = int(keep.sum())
    nuovi = len(ii3) - mb
    s0 = float(g0.s_a[0])
    assert np.all(g0.s_a == s0), "s_a NON e' uniforme: il valore degli archi nuovi non e' derivato (FERMO)"
    g = copy.deepcopy(g0)
    g.cresci(dove_di(keep), ii3, jj3, n + 1, vec3[mb:], A3[mb:], E3[mb:], np.full(nuovi, s0), np.full(nuovi, U1.L_SU_LS), lambda *_: U1.AREA, ori=ori)
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
            "res": res, "res_senza_gauss": res_senza, "media_b": media_b, "coerenti": coerenti, "lato": lato, "t": time.time() - t0, "mb": mb, "ori": ori}


def regola(Z, C, a, giro="stella"):
    """### `mitosi_regola.regola` riga per riga, con `candidato` della v2."""
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
