# -*- coding: utf-8 -*-
r"""**LA MASSA NEI DIFETTI** *(la parte C1 del mandato delle 20:44; [[PROGETTO-MITOSI]], sezione `4`)*: ### **il generatore `(I - P_u) + P_-` su un toro a triangoli con UNO sdoppiamento d'arco**
*(il nodo nuovo a `4`, i due opposti a `7`)*: ### **gli stati nella banda proibita, il bordo locale dallo spettro locale, la convergenza in `L`, e `Lambda_k`.**

> ### ⛔ **Il task history e' `2026-10-25_massa_nei_difetti.md`** *(`71959f32`)*. ### **Sulla carta: il generatore, nessuna dinamica; nessun file del nucleo.**
> ### **Importati, non copiati:** `corrente.toro_spostamenti` *(il toro)*, `scena_l2.GRIGLIE` e `VUOTO_PER_ESTREMITA`, `_u1_terzo.H_gen` e `_curvatura_parte2.H_moneta` *(il controllo di Bloch)*.

Gira con:  python csv/_massa_nei_difetti.py > doc/referti_l2/massa_nei_difetti.txt
"""
import io
import json
import math
import os
import sys
import time
from collections import deque

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LATI_EPS0 = (24, 36, 48)
LATI_EPS = (24, 36)
EPS = 0.5
TOLL_BLOCH = 1e-12
TOLL_PIATTA = 1e-10
DELTA_BANDA = 1e-8
R_LOC = 3
PESO_LOC = 0.5
IPR_LOC = 50.0
FF = (0.005, 0.02)
R_MAX = 8
SOGLIA_DECADE = 0.01
SOGLIA_CHIAVE = 1e-6
LC_SU_L6 = (0.1, 1.0, 10.0)
JSONL = os.path.join(RADICE, "doc", "referti_l2", "massa_nei_difetti.jsonl")
OK = [0, 0]
FALLITE = []
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


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


def _vec(o):
    """### La posizione dell'offset `(o0, o1)`: `o0 a1 + o1 a2`, con `a1`, `a2` le direzioni di `GRIGLIE["triangoli"]`."""
    import scena_l2 as SL
    d = SL.GRIGLIE["triangoli"][1]
    return o[0] * np.asarray(d[0][:2]) + o[1] * np.asarray(d[1][:2])


def toro(L):
    """### Il toro perfetto: `(ii, jj, nn, dirs)`, `dirs[k]` la direzione dell'arco `k` dal lato `ii`."""
    import corrente as CO
    import scena_l2 as SL
    sp, d = SL.GRIGLIE["triangoli"]
    ii, jj, nn = CO.toro_spostamenti((L, L), sp)
    ii = np.asarray(ii, dtype=int)
    jj = np.asarray(jj, dtype=int)
    for k in (0, 1, 2, 3 * (L + 1) + 2):
        v, a = divmod(k, 3)
        c0, c1 = divmod(v, L)
        assert ii[k] == v and jj[k] == ((c0 + sp[a][0]) % L) * L + (c1 + sp[a][1]) % L, "la convenzione del toro non e' quella attesa"
    dirs = np.array([np.asarray(d[k % 3][:2]) for k in range(len(ii))])
    return ii, jj, nn, dirs


def sdoppia(L):
    """### Lo sdoppiamento `(b1)` dell'arco `i -> i + (1,0)` a `i = (L/2, L/2)`: `(ii, jj, nn, dirs, nodi)`."""
    ii, jj, nn, dirs = toro(L)
    c = L // 2

    def nodo(o0, o1):
        return ((c + o0) % L) * L + (c + o1) % L
    i, j, k, l = nodo(0, 0), nodo(1, 0), nodo(1, 1), nodo(0, -1)
    a = 3 * i + 0
    assert ii[a] == i and jj[a] == j
    keep = np.ones(len(ii), dtype=bool)
    keep[a] = False
    n = nn
    m = _vec((0.5, 0.0))
    nuovi = []
    for x, o in ((i, (0, 0)), (j, (1, 0)), (k, (1, 1)), (l, (0, -1))):
        v = _vec(o) - m
        nuovi.append((x, v / np.linalg.norm(v)))
    ii2 = np.concatenate([ii[keep], [n] * 4])
    jj2 = np.concatenate([jj[keep], [x for x, _ in nuovi]])
    dirs2 = np.concatenate([dirs[keep], np.array([v for _, v in nuovi])])
    return ii2, jj2, nn + 1, dirs2, {"n": n, "i": i, "j": j, "k": k, "l": l}


def gradi(ii, jj, nn):
    return np.bincount(ii, minlength=nn) + np.bincount(jj, minlength=nn)


def estremita_del_nodo(ii, jj, nn):
    ext = [[] for _ in range(nn)]
    for k in range(len(ii)):
        ext[ii[k]].append(2 * k)
        ext[jj[k]].append(2 * k + 1)
    return ext


def H_diretto(ii, jj, nn):
    """### `H = I - P_u + P_-` sulle `2m` estremita', reale."""
    m = len(ii)
    H = np.eye(2 * m)
    for e in estremita_del_nodo(ii, jj, nn):
        e = np.asarray(e)
        H[np.ix_(e, e)] -= 1.0 / len(e)
    for k in range(m):
        a, b = 2 * k, 2 * k + 1
        H[a, a] += 0.5
        H[b, b] += 0.5
        H[a, b] -= 0.5
        H[b, a] -= 0.5
    return H


def H_spin(ii, jj, nn, dirs, eps):
    """### `H x I_2 - (eps/pi) somma_h sigma.n_h`: `+dir` sul lato `2k`, `-dir` sul lato `2k + 1`."""
    H0 = H_diretto(ii, jj, nn)
    M = 2 * H0.shape[0]
    H = np.zeros((M, M), dtype=complex)
    H[0::2, 0::2] = H0
    H[1::2, 1::2] = H0
    for k in range(len(ii)):
        for h, s in ((2 * k, 1.0), (2 * k + 1, -1.0)):
            nx, ny = s * dirs[k][0], s * dirs[k][1]
            H[2 * h:2 * h + 2, 2 * h:2 * h + 2] -= (eps / np.pi) * (nx * SX + ny * SY)
    return H


def bloch(L, eps):
    """### L'unione su tutte le fasi `2 pi n/L` del blocco di Bloch: `mu = 1 - lambda`."""
    import _u1_terzo as U3
    import _curvatura_parte2 as P2
    out = []
    for n1 in range(L):
        for n2 in range(L):
            t1, t2 = 2 * np.pi * n1 / L, 2 * np.pi * n2 / L
            Hk = U3.H_gen(t1, t2) if eps == 0 else P2.H_moneta(t1, t2, 1.0, 1.0, 1.0, eps)
            out.append(np.linalg.eigvalsh(Hk))
    B = 1.0 - np.array(out)
    piatti = sorted({round(float(B[:, b].mean()), 12) for b in range(B.shape[1]) if np.ptp(B[:, b]) < TOLL_PIATTA})
    return np.sort(B.ravel()), piatti, B


def distanze(ii, jj, nn, da):
    adj = [[] for _ in range(nn)]
    for a, b in zip(ii, jj):
        adj[a].append(b)
        adj[b].append(a)
    d = np.full(nn, -1, dtype=int)
    d[da] = 0
    q = deque([da])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if d[w] < 0:
                d[w] = d[v] + 1
                q.append(w)
    return d


def non_piatto(mu, piatti):
    return np.all(np.abs(np.asarray(mu)[:, None] - np.asarray(piatti)[None, :]) > DELTA_BANDA, axis=1) if piatti else np.ones(len(mu), dtype=bool)


def bordo_rif(mu_bloch, f, piatti):
    a = np.sort(np.abs(mu_bloch[non_piatto(mu_bloch, piatti)]))
    F = np.arange(1, len(a) + 1) / len(a)
    return float(a[int(np.argmax(F >= f - 1e-15))])


def misura(L, eps):
    t0 = time.time()
    spin = eps != 0
    mb, piatti, _B = bloch(L, eps)
    E0 = float(np.min(np.abs(mb[non_piatto(mb, piatti)])))
    # ### il toro perfetto, diretto
    ii, jj, nn, dirs = toro(L)
    Hp = H_diretto(ii, jj, nn) if not spin else H_spin(ii, jj, nn, dirs, eps)
    mp = np.sort(1.0 - np.linalg.eigvalsh(Hp))
    del Hp
    dB = float(np.max(np.abs(mp - mb))) if len(mp) == len(mb) else float("inf")
    # ### il difetto
    ii2, jj2, nn2, dirs2, nodi = sdoppia(L)
    g = gradi(ii2, jj2, nn2)
    gr = {kk: int(g[v]) for kk, v in nodi.items()}
    altri = np.delete(np.arange(nn2), list(nodi.values()))
    gradi_ok = gr == {"n": 4, "i": 6, "j": 6, "k": 7, "l": 7} and bool(np.all(g[altri] == 6))
    Hd = H_diretto(ii2, jj2, nn2) if not spin else H_spin(ii2, jj2, nn2, dirs2, eps)
    lam, V = np.linalg.eigh(Hd)
    del Hd
    mu = 1.0 - lam
    ext = estremita_del_nodo(ii2, jj2, nn2)
    sp = 2 if spin else 1
    # ### il peso per nodo di ogni stato: P[v, n] = somma_{h in v, spin} |V[h, n]|^2
    A2 = np.abs(V) ** 2
    P = np.zeros((nn2, V.shape[1]))
    for v in range(nn2):
        idx = np.asarray(ext[v])
        if spin:
            idx = np.concatenate([2 * idx, 2 * idx + 1])
        P[v] = A2[idx].sum(axis=0)
    ipr = (A2 ** 2).sum(axis=0) * V.shape[0]
    del A2, V
    dist = distanze(ii2, jj2, nn2, nodi["n"])
    vicini = dist <= R_LOC
    np_ = non_piatto(mu, piatti)
    in_banda = np.where((np.abs(mu) < E0 - DELTA_BANDA) & np_)[0]
    stati = []
    for s in in_banda:
        stati.append({"mu": float(mu[s]), "legame": float(E0 - abs(mu[s])), "peso_entro_3": float(P[vicini, s].sum() / sp), "ipr_2m": float(ipr[s])})
    loc = [s for s in stati if s["peso_entro_3"] >= PESO_LOC and s["ipr_2m"] >= IPR_LOC]
    # ### il bordo locale
    sel = np.where(np_)[0]
    ordine = sel[np.argsort(np.abs(mu[sel]))]
    amu = np.abs(mu)[ordine]
    W = P[:, ordine]
    F = np.cumsum(W, axis=1) / W.sum(axis=1)[:, None]
    bordi = {}
    for f in FF:
        Er = bordo_rif(mb, f, piatti)
        Ev = amu[np.argmax(F >= f - 1e-15, axis=1)]
        dv = (Ev - Er) / Er
        anelli = [float(np.max(np.abs(dv[dist == r]))) if np.any(dist == r) else None for r in range(R_MAX + 1)]
        lontano = int(np.argmax(dist))
        bordi[f] = {"E_rif": Er, "delta": {kk: float(dv[v]) for kk, v in nodi.items()}, "delta_lontano": float(dv[lontano]), "dist_lontano": int(dist[lontano]),
                    "anelli": anelli, "max_da_3": float(np.max(np.abs(dv[dist >= R_LOC])))}
    # ### Lambda_k
    import scena_l2 as SL
    lam_nodo = g * SL.VUOTO_PER_ESTREMITA ** 2
    lam_est = lam_nodo / g
    out = {"L": L, "eps": eps, "E0": E0, "piatti": piatti, "piatti_nel_difetto": int(np.sum(~np_)), "piatti_nel_perfetto": int(np.sum(~non_piatto(mb, piatti))), "dBloch": dB, "dim_perfetto": len(mp), "dim_difetto": len(mu), "gradi": gr, "gradi_ok": gradi_ok,
           "stati_in_banda": stati, "localizzati": loc, "bordi": {str(k): v for k, v in bordi.items()},
           "Lambda_nodo": {kk: float(lam_nodo[v]) for kk, v in nodi.items()}, "Lambda_estremita": {kk: float(lam_est[v]) for kk, v in nodi.items()},
           "Lambda_lontano": float(lam_nodo[int(np.argmax(dist))]),
           "chiave": float(np.max(np.abs(np.sort(mu)[:len(mp)] - mp))), "secondi": time.time() - t0}
    return out


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA MASSA NEI DIFETTI: il generatore (I - P_u) + P_- su un toro a triangoli con uno sdoppiamento d'arco (il nodo nuovo a 4, gli opposti a 7)")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_massa_nei_difetti.py", "csv/_u1_terzo.py", "csv/_curvatura_parte2.py", "primo_ordine/corrente.py", "primo_ordine/scena_l2.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LATI_EPS0 %s LATI_EPS %s EPS %g TOLL_BLOCH %g DELTA_BANDA %g R_LOC %d PESO_LOC %g IPR_LOC %g FF %s R_MAX %d SOGLIA_DECADE %g SOGLIA_CHIAVE %g LC_SU_L6 %s"
          % (LATI_EPS0, LATI_EPS, EPS, TOLL_BLOCH, DELTA_BANDA, R_LOC, PESO_LOC, IPR_LOC, FF, R_MAX, SOGLIA_DECADE, SOGLIA_CHIAVE, LC_SU_L6))
    print("  la scena: i = (L/2, L/2), l'arco i -> i + (1,0) tolto, n legato a i, j = i + (1,0), k = i + (1,1), l = i + (0,-1); n al punto medio di i-j (i versori della moneta: verso il vicino)")
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    ris = {}
    for eps, lati in ((0.0, LATI_EPS0), (EPS, LATI_EPS)):
        for L in lati:
            r = misura(L, eps)
            ris[(eps, L)] = r
            scrivi(dict(r, tipo="misura"))
            print("### eps %g, L %d (%.0f s): dim %d -> %d; E0 (il bordo del toro perfetto) %.10f; lo scarto dal Bloch %.2e; i gradi %s (attesi: %s)"
                  % (eps, L, r["secondi"], r["dim_perfetto"], r["dim_difetto"], r["E0"], r["dBloch"], r["gradi"], r["gradi_ok"]))
            print("  i livelli piatti del toro perfetto %s: stati piatti %d nel perfetto, %d col difetto" % (r["piatti"], r["piatti_nel_perfetto"], r["piatti_nel_difetto"]))
            print("  (i) gli stati con |mu| < E0 - %g, non piatti: %d; localizzati sul difetto: %d" % (DELTA_BANDA, len(r["stati_in_banda"]), len(r["localizzati"])))
            for s in sorted(r["stati_in_banda"], key=lambda z: -z["legame"])[:8]:
                print("      mu %+.10f  il legame %.3e  il peso entro %d %.4f  IPR 2m %.1f" % (s["mu"], s["legame"], R_LOC, s["peso_entro_3"], s["ipr_2m"]))
            for f, b in r["bordi"].items():
                print("  (ii) f %s: E_rif %.6f; delta n %+.4e  k %+.4e  l %+.4e  i %+.4e  j %+.4e  lontano (dist %d) %+.4e; max|delta| per anello r=0..%d: %s; max a r >= %d: %.3e"
                      % (f, b["E_rif"], b["delta"]["n"], b["delta"]["k"], b["delta"]["l"], b["delta"]["i"], b["delta"]["j"], b["dist_lontano"], b["delta_lontano"], R_MAX,
                         " ".join("%.2e" % x for x in b["anelli"]), R_LOC, b["max_da_3"]))
            print("  (v) Lambda per nodo %s (lontano %g); per estremita' %s" % (r["Lambda_nodo"], r["Lambda_lontano"], r["Lambda_estremita"]))
    print("-" * 130)
    print("### I CRITERI")
    b_ok = all(r["dBloch"] <= TOLL_BLOCH for r in ris.values())
    esito("DEVE PASSARE (1): senza difetto lo spettro diretto = l'unione di Bloch entro %g, a ogni L ed eps" % TOLL_BLOCH, b_ok, " ".join("%g/%d %.1e" % (e, L, r["dBloch"]) for (e, L), r in ris.items()))
    esito("DEVE PASSARE (1): i gradi del grafo col difetto (n 4, k e l 7, i e j 6, gli altri 6)", all(r["gradi_ok"] for r in ris.values()), "")
    nloc = {L: len(ris[(0.0, L)]["localizzati"]) for L in LATI_EPS0}
    esito("PUO' FALLIRE (2): nessuno stato LOCALIZZATO nella banda proibita (eps 0, a ogni L)", all(v == 0 for v in nloc.values()), str(nloc), deve=False)
    r48 = ris[(0.0, LATI_EPS0[-1])]
    md = r48["bordi"][str(FF[0])]["max_da_3"]
    esito("PUO' FALLIRE (3): max|delta_v| a distanza >= %d sotto %g (f %g, eps 0, L %d)" % (R_LOC, SOGLIA_DECADE, FF[0], LATI_EPS0[-1]), md < SOGLIA_DECADE, "%.3e" % md, deve=False)
    l_ok = True
    for r in ris.values():
        ln, le, l6 = r["Lambda_nodo"], r["Lambda_estremita"], r["Lambda_lontano"]
        l_ok &= ln["n"] / l6 == 4.0 / 6.0 and ln["k"] / l6 == 7.0 / 6.0 and ln["l"] / l6 == 7.0 / 6.0 and len(set(le.values())) == 1
    esito("DEVE PASSARE (4): Lambda per nodo 4/6 e 7/6 di quello a 6 ESATTI; per estremita' uguale ovunque", l_ok, "")
    print("  (v) cs_v/cs_6 = (Lambda_v/Lambda_6) (1 + Lc/Lambda_6)/(Lambda_v/Lambda_6 + Lc/Lambda_6), per nodo:")
    for lc in LC_SU_L6:
        q4 = (4 / 6) * (1 + lc) / (4 / 6 + lc)
        q7 = (7 / 6) * (1 + lc) / (7 / 6 + lc)
        print("      Lc/Lambda_6 %-5g: il nodo a 4 %.6f, a 7 %.6f; per estremita': 1, 1" % (lc, q4, q7))
        scrivi({"tipo": "cs", "Lc_su_L6": lc, "cs4_su_cs6": q4, "cs7_su_cs6": q7})
    ch = {(e, L): r["chiave"] for (e, L), r in ris.items()}
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA (5): il difetto non cambia niente; la chiave: 6 estremita' in piu' e un livello spostato > %g" % SOGLIA_CHIAVE,
          all(r["dim_difetto"] - r["dim_perfetto"] == 6 * (2 if e else 1) and r["chiave"] > SOGLIA_CHIAVE for (e, L), r in ris.items()), " ".join("%.1e" % v for v in ch.values()))
    print("### (iii) LA CONVERGENZA (eps 0): lo scarto 36-48 minore di 24-36 e minore del 10% del valore")
    for f in FF:
        for kk in ("n", "k", "l", "i"):
            v = [ris[(0.0, L)]["bordi"][str(f)]["delta"][kk] for L in LATI_EPS0]
            d1, d2 = abs(v[1] - v[0]), abs(v[2] - v[1])
            conv = d2 < d1 and d2 < 0.1 * abs(v[2])
            print("  f %-6g delta_%s: %s  -> %s" % (f, kk, " ".join("%+.4e" % x for x in v), "CONVERGE" if conv else "NON CONVERGE"))
            scrivi({"tipo": "convergenza", "f": f, "nodo": kk, "valori": v, "converge": conv})
    for L in LATI_EPS0:
        lg = [s["legame"] for s in ris[(0.0, L)]["localizzati"]]
        print("  i legami degli stati localizzati a L %d: %s" % (L, " ".join("%.4e" % x for x in sorted(lg, reverse=True)) or "nessuno"))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
