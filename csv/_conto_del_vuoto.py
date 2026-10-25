# -*- coding: utf-8 -*-
r"""**IL CONTO DEL VUOTO** *(la parte C3, l'aggiunta di Luca delle 20:53; [[PROGETTO-MITOSI]], [[D-BILANCIO-NASCITA]])*: ### **la nascita `(b1)` con `D7` e il flip `2 <-> 2` sul toro
perfetto: `Delta H_tot` separato in materia, vuoto e legame; la capacita' del vuoto locale; la rotazione che annullerebbe il conto, e che cosa fa a `cs`.**

> ### ⛔ **Il task history e' `2026-10-25_conto_del_vuoto.md`.** ### **Sulla carta: nessuna dinamica, nessun file del nucleo.**
> ### **Importati, non copiati:** `energia_pesata.termini_di_h` e `g_dello_stato` *(`H_tot`)*, `incidenza`, `motore`, `stato` *(il `Motore` della scena, come `scena_l2.scena_toro`)*,
> `_massa_nei_difetti` *(`toro`, `sdoppia`, `H_diretto`)*, `_u1_terzo.H_gen` *(la coppia a `K`)*, `_triangoli.X`, `scena_l2.VUOTO_PER_ESTREMITA`.

Gira con:  python csv/_conto_del_vuoto.py > doc/referti_l2/conto_del_vuoto.txt
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LATI = (24, 36)
TOLL_NORMA = 1e-14
TOLL_CONTROLLO = 1e-12
TOLL_CONV = 0.01
SOGLIA_CHIAVE = 1e-6
LC_SU_L6 = (0.1, 1.0, 10.0)
PAR = {"eps": 0.0}
JSONL = os.path.join(RADICE, "doc", "referti_l2", "conto_del_vuoto.jsonl")
OK = [0, 0]
FALLITE = []
A1 = np.array([1.0, 0.0])
A2 = np.array([-0.5, math.sqrt(3.0) / 2.0])


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


# =====================================================================================
#   LA SCENA
# =====================================================================================
def motore(ii, jj, nn, dirs, psi, phi):
    """### Il `Motore` della scena *(le stesse chiamate di `scena_l2.scena_toro`)*: `U = I`, i versori `+dir` sul lato `2k`, `-dir` sul `2k + 1`, `cs` spento."""
    import incidenza as IN
    import motore as MO
    import stato as ST
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE), np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    m = inc.m
    nv = np.zeros((2 * m, 3))
    d = np.asarray(dirs, dtype=float)
    d = d / np.linalg.norm(d, axis=1)[:, None]
    nv[0::2, :2] = d
    nv[1::2, :2] = -d
    U = np.zeros((m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, m)
    st["psi_h"][...] = psi
    st["phi_h"][...] = phi
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.ones(nn), "numpy")
    mot.cs = None
    mot.lambda_c = None
    return mot, st


def parti(mot, st):
    """### `(totale, materia, vuoto, legame, per_nodo)`: ### **la materia `H(psi, 0)`, il vuoto `H(0, phi)`, il legame il resto.**"""
    import energia_pesata as EP

    def H(s):
        pn, pa = EP.termini_di_h(mot, s, PAR)
        return float(np.sum(pn)) + float(np.sum(pa)), pn.copy()
    tot, pn = H(st)
    s0 = dict(st)
    s0["phi_h"] = np.zeros_like(st["phi_h"])
    mat, _ = H(s0)
    s1 = dict(st)
    s1["psi_h"] = np.zeros_like(st["psi_h"])
    vuo, _ = H(s1)
    return tot, mat, vuo, tot - mat - vuo, pn


def stato_K(L):
    """### Il toro perfetto con la coppia a `K` *(il livello alto, spin su, `rho = X` per nodo)* e il vuoto uniforme."""
    import _massa_nei_difetti as MD
    import _triangoli as T
    import _u1_terzo as U3
    import scena_l2 as SL
    ii, jj, nn, dirs = MD.toro(L)
    lam, V = np.linalg.eigh(U3.H_gen(2 * np.pi / 3, 2 * np.pi / 3))
    u = V[:, 0]
    assert abs((1.0 - lam[0]) - 0.5) < 1e-12, "il livello alto della coppia non e' +1/2"
    m = len(ii)
    psi = np.zeros((2 * m, 2), dtype=complex)
    v = np.arange(nn)
    c0, c1 = v // L, v % L
    fase = np.exp(1j * (2 * np.pi / 3) * (c0 + c1))
    for k in range(m):
        a = k % 3
        psi[2 * k, 0] = u[a] * fase[ii[k]]
        psi[2 * k + 1, 0] = u[3 + a] * fase[jj[k]]
    psi *= math.sqrt(T.X)
    phi = np.full(2 * m, SL.VUOTO_PER_ESTREMITA, dtype=complex)
    return ii, jj, nn, dirs, psi, phi


def nascita(L, ii, jj, nn, dirs, psi, phi):
    """### La nascita `(b1)` con `D7` e il trasporto DICHIARATO *(il padre `i`)*."""
    import _massa_nei_difetti as MD
    ii2, jj2, nn2, dirs2, nodi = MD.sdoppia(L)
    i, j = nodi["i"], nodi["j"]
    a = 3 * i + 0
    keep = np.ones(len(ii), dtype=bool)
    keep[a] = False
    nuovi = np.where(keep)[0]
    m2 = len(ii2)
    psi2 = np.zeros((2 * m2, 2), dtype=complex)
    phi2 = np.zeros(2 * m2, dtype=complex)
    for kn, ko in enumerate(nuovi):
        psi2[2 * kn:2 * kn + 2] = psi[2 * ko:2 * ko + 2]
        phi2[2 * kn:2 * kn + 2] = phi[2 * ko:2 * ko + 2]
    base = len(nuovi)                             # ### gli archi nuovi: n->i, n->j, n->k, n->l
    assert list(jj2[base:]) == [nodi["i"], nodi["j"], nodi["k"], nodi["l"]]
    # ### il trasporto: l'estremita' dell'arco tolto in i -> quella di n-i in i; in j -> quella di n-j in j
    psi2[2 * (base + 0) + 1] = psi[2 * a]
    phi2[2 * (base + 0) + 1] = phi[2 * a]
    psi2[2 * (base + 1) + 1] = psi[2 * a + 1]
    phi2[2 * (base + 1) + 1] = phi[2 * a + 1]
    # ### D7 sul padre i
    nodo2 = np.empty(2 * m2, dtype=int)
    nodo2[0::2] = ii2
    nodo2[1::2] = jj2
    hp = np.where(nodo2 == i)[0]
    Np_psi = float(np.sum(np.abs(psi2[hp]) ** 2))
    Np_phi = float(np.sum(np.abs(phi2[hp]) ** 2))
    chi = psi2[hp].sum(axis=0)
    chiv = phi2[hp].sum()
    psi2[hp] /= math.sqrt(2.0)
    phi2[hp] /= math.sqrt(2.0)
    hf = [2 * (base + q) for q in range(4)]
    for h in hf:
        psi2[h] = (1.0 / math.sqrt(2.0)) * math.sqrt(Np_psi / 4.0) * chi / np.linalg.norm(chi)
        phi2[h] = (1.0 / math.sqrt(2.0)) * math.sqrt(Np_phi / 4.0) * chiv / abs(chiv)
    # ### le estremita' nuove in k e in l (verso n) restano 0
    return ii2, jj2, nn2, dirs2, psi2, phi2, nodi, ["n"]


def flip(L, ii, jj, nn, dirs, psi, phi):
    """### Il flip dell'arco `i -> j` in `l -> k`, ### **una permutazione delle ampiezze** *(l'estremita' in i va in l, quella in j va in k)*."""
    c = L // 2

    def nodo(o0, o1):
        return ((c + o0) % L) * L + (c + o1) % L
    i, j, k, l = nodo(0, 0), nodo(1, 0), nodo(1, 1), nodo(0, -1)
    a = 3 * i + 0
    assert ii[a] == i and jj[a] == j
    keep = np.ones(len(ii), dtype=bool)
    keep[a] = False
    ii2 = np.concatenate([ii[keep], [l]])
    jj2 = np.concatenate([jj[keep], [k]])
    dk = np.array([0.0, 1.0])
    dirs2 = np.concatenate([dirs[keep], dk[None, :]])
    e = np.repeat(keep, 2)
    psi2 = np.concatenate([psi[e], psi[[2 * a, 2 * a + 1]]])
    phi2 = np.concatenate([phi[e], phi[[2 * a, 2 * a + 1]]])
    return ii2, jj2, nn, dirs2, psi2, phi2, {"i": i, "j": j, "k": k, "l": l}, ["i", "j", "k", "l"]


# =====================================================================================
#   LA CAPACITA' E LA ROTAZIONE
# =====================================================================================
def sottospazio(ii, jj, nn, nodi_mossa):
    nodo = np.empty(2 * len(ii), dtype=int)
    nodo[0::2] = ii
    nodo[1::2] = jj
    S = set(nodi_mossa)
    for a, b in zip(ii, jj):
        if a in nodi_mossa:
            S.add(int(b))
        if b in nodi_mossa:
            S.add(int(a))
    return np.where(np.isin(nodo, sorted(S)))[0], sorted(S), nodo


def estremi_sfera(A, b, N):
    """### Il minimo e il massimo di `x.A x + 2 b.x` su `|x|^2 = N` *(x reale)*: `(fmin, xmin, fmax, xmax)`."""
    lam, Q = np.linalg.eigh(A)
    c = Q.T @ b

    def x_di(nu):
        return -(Q @ (c / (lam - nu)))

    def risolvi(lato):
        l0 = lam[0] if lato < 0 else lam[-1]
        deg = np.abs(lam - l0) < 1e-12
        if np.linalg.norm(c[deg]) < 1e-14:
            # ### il caso difficile: la componente nell'autospazio estremo e' nulla
            ok = ~deg
            xp = -(Q[:, ok] @ (c[ok] / (lam[ok] - l0)))
            r2 = N - float(xp @ xp)
            if r2 >= 0:
                x = xp + math.sqrt(r2) * Q[:, np.where(deg)[0][0]]
                return x
        lo, hi = (l0 - 1.0, l0 - 1e-15) if lato < 0 else (l0 + 1e-15, l0 + 1.0)
        while True:
            xx = x_di(lo if lato < 0 else hi)
            if float(xx @ xx) < N:
                break
            if lato < 0:
                lo = l0 - 2.0 * (l0 - lo)
            else:
                hi = l0 + 2.0 * (hi - l0)
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            xx = x_di(mid)
            n2 = float(xx @ xx)
            if lato < 0:
                if n2 > N:
                    hi = mid
                else:
                    lo = mid
            else:
                if n2 > N:
                    lo = mid
                else:
                    hi = mid
        return x_di(0.5 * (lo + hi))
    xmin, xmax = risolvi(-1), risolvi(+1)

    def f(x):
        return float(x @ A @ x + 2.0 * b @ x)
    return f(xmin), xmin, f(xmax), xmax, float(lam[0]), float(lam[-1])


def conto(L, ii, jj, nn, dirs, psi, phi, ii2, jj2, nn2, dirs2, psi2, phi2, nodi, chi_mossa):
    import _massa_nei_difetti as MD
    mot0, st0 = motore(ii, jj, nn, dirs, psi, phi)
    mot1, st1 = motore(ii2, jj2, nn2, dirs2, psi2, phi2)
    p0 = parti(mot0, st0)
    p1 = parti(mot1, st1)
    M0, M1 = float(np.sum(np.abs(psi) ** 2)), float(np.sum(np.abs(psi2) ** 2))
    V0, V1 = float(np.sum(np.abs(phi) ** 2)), float(np.sum(np.abs(phi2) ** 2))
    dH = p1[0] - p0[0]
    # ### la capacita'
    mossa = [nodi[x] for x in chi_mossa]
    hS, nodiS, nodo = sottospazio(ii2, jj2, nn2, mossa)
    H = MD.H_diretto(ii2, jj2, nn2)
    O = np.setdiff1d(np.arange(H.shape[0]), hS)
    A = -np.pi * H[np.ix_(hS, hS)]
    xO = np.real(phi2[O])
    bb = -np.pi * (H[np.ix_(hS, O)] @ xO)
    x0 = np.real(phi2[hS]).copy()
    assert np.max(np.abs(np.imag(phi2))) == 0.0, "il vuoto della scena non e' reale"
    N = float(x0 @ x0)
    fmin, xmin, fmax, xmax, lmin, lmax = estremi_sfera(A, bb, N)
    f0 = float(x0 @ A @ x0 + 2.0 * bb @ x0)
    serve = f0 - dH                                # ### il valore della parte di S del vuoto che annulla Delta H_tot
    spettro = (lmin * N, lmax * N)
    basta_esatto = fmin <= serve <= fmax
    # ### lo SPETTRO soltanto (il mandato): la parte quadratica di S puo' andare in [lmin N, lmax N]; serve -dH su di lei
    q0 = float(x0 @ A @ x0)
    basta_spettro = spettro[0] - q0 <= -dH <= spettro[1] - q0
    # ### la rotazione: sul cerchio massimo fra x0 e l'estremo nel verso giusto, con N incluso (H_tot pieno)
    xe = xmin if serve < f0 else xmax
    u0 = x0 / math.sqrt(N)
    e = xe - (xe @ u0) * u0
    rot = {"esiste": False}
    if np.linalg.norm(e) > 1e-14:
        e /= np.linalg.norm(e)
        th_e = math.atan2(float(xe @ e), float(xe @ u0))

        def Htot(th):
            st = dict(st1)
            ph = phi2.copy()
            ph[hS] = math.sqrt(N) * (math.cos(th) * u0 + math.sin(th) * e)
            st["phi_h"] = ph
            return parti(mot1, st)[0] - p0[0], ph
        g0, _ = Htot(0.0)
        ge, _ = Htot(th_e)
        if g0 == 0.0 or (g0 > 0) != (ge > 0):
            lo, hi = 0.0, th_e
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                gm, _ = Htot(mid)
                if (gm > 0) == (g0 > 0):
                    lo = mid
                else:
                    hi = mid
            th = 0.5 * (lo + hi)
            gfin, ph = Htot(th)
            lam_prima = np.zeros(nn2)
            np.add.at(lam_prima, nodo, np.abs(phi2) ** 2)
            lam_dopo = np.zeros(nn2)
            np.add.at(lam_dopo, nodo, np.abs(ph) ** 2)
            gr = np.bincount(nodo, minlength=nn2)
            l6 = 6.0
            righe = []
            for v in nodiS:
                r = {"nodo": int(v), "grado": int(gr[v]), "Lambda_prima": float(lam_prima[v]), "Lambda_dopo": float(lam_dopo[v])}
                for lc in LC_SU_L6:
                    Lc = lc * l6
                    cp, cd = lam_prima[v] / (lam_prima[v] + Lc), lam_dopo[v] / (lam_dopo[v] + Lc)
                    cpe = (lam_prima[v] / gr[v]) / (lam_prima[v] / gr[v] + Lc / 6.0)
                    cde = (lam_dopo[v] / gr[v]) / (lam_dopo[v] / gr[v] + Lc / 6.0)
                    r["dcs_nodo_%g" % lc] = (cd - cp) / cp
                    r["dcs_estr_%g" % lc] = (cde - cpe) / cpe
                righe.append(r)
            rot = {"esiste": True, "angolo": th, "residuo": gfin, "V_dopo": float(np.sum(np.abs(ph) ** 2)), "nodi": righe}
        else:
            rot = {"esiste": False, "perche": "sul cerchio fino all'estremo Delta H_tot non cambia segno: %.6e -> %.6e" % (g0, ge)}
    return {"L": L, "H_prima": p0[:4], "H_dopo": p1[:4], "dH": dH, "dH_materia": p1[1] - p0[1], "dH_vuoto": p1[2] - p0[2], "dH_legame": p1[3] - p0[3],
            "M": (M0, M1), "V": (V0, V1), "S_estremita": int(len(hS)), "S_nodi": len(nodiS), "N_S": N, "f0": f0, "serve": serve, "esatto": (fmin, fmax), "spettro": spettro,
            "lambda": (lmin, lmax), "basta_esatto": bool(basta_esatto), "basta_spettro": bool(basta_spettro), "rotazione": rot,
            "per_nodo_prima": (float(np.min(p0[4])), float(np.max(p0[4]))),
            "permutazione": bool(np.array_equal(np.sort(np.abs(psi.ravel())), np.sort(np.abs(psi2.ravel()))) and np.array_equal(np.sort(np.abs(phi)), np.sort(np.abs(phi2))))}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    import energia_pesata as EP
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL CONTO DEL VUOTO: la nascita (b1) con D7 e il flip 2<->2 sul toro perfetto; Delta H_tot in materia, vuoto e legame; la capacita' del vuoto locale; la rotazione e cs")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_conto_del_vuoto.py", "csv/_massa_nei_difetti.py", "csv/_u1_terzo.py", "primo_ordine/energia_pesata.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LATI %s TOLL_NORMA %g TOLL_CONTROLLO %g TOLL_CONV %g SOGLIA_CHIAVE %g LC_SU_L6 %s PAR %s; OMEGA_H %g" % (LATI, TOLL_NORMA, TOLL_CONTROLLO, TOLL_CONV, SOGLIA_CHIAVE, LC_SU_L6, PAR, EP.OMEGA_H))
    print("  la materia: la coppia a K, il livello alto, spin su, rho = X per nodo; il vuoto 1 per estremita'; il padre della nascita: i (il capo di partenza dell'arco tolto)")
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    ris = {}
    ctrl = []
    for L in LATI:
        sc = stato_K(L)
        mot0, st0 = motore(*sc)
        g = EP.g_dello_stato(mot0, st0, PAR)
        p0 = parti(mot0, st0)
        ctrl.append((L, abs(g - p0[0]), float(np.ptp(p0[4]))))
        for nome, fn in (("nascita", nascita), ("flip", flip)):
            dopo = fn(L, *sc)
            r = conto(L, *sc, *dopo)
            r["mossa"] = nome
            ris[(nome, L)] = r
            scrivi(dict(r, tipo="conto"))
            print("### %s, L %d" % (nome.upper(), L))
            print("  H_tot prima %.12f (materia %.12f, vuoto %.12f, legame %.12f)" % tuple(r["H_prima"]))
            print("  H_tot dopo  %.12f (materia %.12f, vuoto %.12f, legame %.12f)" % tuple(r["H_dopo"]))
            print("  Delta H_tot %+.6e = materia %+.6e + vuoto %+.6e + legame %+.6e" % (r["dH"], r["dH_materia"], r["dH_vuoto"], r["dH_legame"]))
            print("  le norme: M %.17g -> %.17g (rel %.1e); V %.17g -> %.17g (rel %.1e)" % (r["M"][0], r["M"][1], abs(r["M"][1] - r["M"][0]) / r["M"][0], r["V"][0], r["V"][1], abs(r["V"][1] - r["V"][0]) / r["V"][0]))
            print("  (iii) S: %d estremita' su %d nodi, |phi_S|^2 %.6f; il vuoto di S ora %.6e, serve %.6e; l'intervallo ESATTO [%.6e, %.6e]; lo SPETTRO x norma [%.6e, %.6e] (lambda %.4f, %.4f): basta %s (esatto), %s (spettro)"
                  % (r["S_estremita"], r["S_nodi"], r["N_S"], r["f0"], r["serve"], r["esatto"][0], r["esatto"][1], r["spettro"][0], r["spettro"][1], r["lambda"][0], r["lambda"][1], r["basta_esatto"], r["basta_spettro"]))
            ro = r["rotazione"]
            if ro["esiste"]:
                print("  (iv) la rotazione: angolo %.6e rad, il residuo di Delta H_tot %.1e, V dopo %.17g" % (ro["angolo"], ro["residuo"], ro["V_dopo"]))
                for q in ro["nodi"]:
                    print("      nodo %6d grado %d: Lambda %.6f -> %.6f; dcs/cs per nodo %s; per estremita' %s" % (q["nodo"], q["grado"], q["Lambda_prima"], q["Lambda_dopo"],
                          " ".join("%+.3e" % q["dcs_nodo_%g" % lc] for lc in LC_SU_L6), " ".join("%+.3e" % q["dcs_estr_%g" % lc] for lc in LC_SU_L6)))
            else:
                print("  (iv) la rotazione NON ESISTE su quel cerchio: %s" % ro.get("perche", ""))
    print("-" * 130)
    print("### I CRITERI")
    nn_ok = all(abs(ris[("nascita", L)]["M"][1] - ris[("nascita", L)]["M"][0]) / ris[("nascita", L)]["M"][0] <= TOLL_NORMA and abs(ris[("nascita", L)]["V"][1] - ris[("nascita", L)]["V"][0]) / ris[("nascita", L)]["V"][0] <= TOLL_NORMA for L in LATI)
    fl_ok = all(ris[("flip", L)]["permutazione"] for L in LATI)
    ro_ok = all((not r["rotazione"]["esiste"]) or abs(r["rotazione"]["V_dopo"] - r["V"][1]) / r["V"][1] <= TOLL_NORMA for r in ris.values())
    esito("DEVE PASSARE (1): la nascita conserva M e V entro %g relativo (non al bit: la nota di D7)" % TOLL_NORMA, nn_ok, "")
    esito("DEVE PASSARE (1): il flip conserva le norme AL BIT (una permutazione: gli stessi moduli, ordinati, byte per byte)", fl_ok, "")
    esito("DEVE PASSARE (1): la rotazione conserva V entro %g" % TOLL_NORMA, ro_ok, "")
    c_ok = all(d <= TOLL_CONTROLLO and p <= TOLL_CONTROLLO for _L, d, p in ctrl)
    esito("DEVE PASSARE (2): H_tot = energia_pesata.g_dello_stato, e uguale a ogni nodo del toro perfetto, entro %g" % TOLL_CONTROLLO, c_ok, " ".join("L %d: %.1e %.1e" % c for c in ctrl))
    for nome in ("nascita", "flip"):
        esito("PUO' FALLIRE (3): la capacita' del vuoto locale basta per la %s (l'intervallo esatto, a ogni L)" % nome, all(ris[(nome, L)]["basta_esatto"] for L in LATI),
              " ".join("L %d: serve %.4e in [%.4e, %.4e]" % (L, ris[(nome, L)]["serve"], ris[(nome, L)]["esatto"][0], ris[(nome, L)]["esatto"][1]) for L in LATI), deve=False)
    for nome in ("nascita", "flip"):
        a, b = ris[(nome, LATI[0])]["dH"], ris[(nome, LATI[1])]["dH"]
        esito("DEVE PASSARE (4): Delta H_tot della %s converge in L (scarto sotto il %g%%)" % (nome, 100 * TOLL_CONV), abs(a - b) <= TOLL_CONV * abs(b), "%+.6e %+.6e" % (a, b))
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA (5): la mossa non cambia l'energia; la chiave: |Delta H_tot| > %g per la nascita E per il flip" % SOGLIA_CHIAVE,
          all(abs(ris[(n, L)]["dH"]) > SOGLIA_CHIAVE for n in ("nascita", "flip") for L in LATI), " ".join("%+.3e" % ris[(n, LATI[-1])]["dH"] for n in ("nascita", "flip")))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
