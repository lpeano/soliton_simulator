# -*- coding: utf-8 -*-
r"""**LA DIVISIONE DEL VUOTO, SULLA CARTA** *(la parte 2 del mandato del 2026-10-26; [[PROGETTO-MITOSI]], [[CONTO-DEL-VUOTO]], [[D-BILANCIO-NASCITA]])*: ### **cinque regole di trasporto di `phi`
alla nascita `(b1)`** *(e il flip)*, ### **con lo strumento di `C3`: `Delta H_tot`, `V`, `Lambda` e `cs`, e la rotazione che porterebbe il conto a `0`.**

> ### ⛔ **Il task history e' `2026-10-26_divisione_vuoto.md`.** ### **Sulla carta: nessuna dinamica, nessun file del nucleo.**
> ### **Importato, non copiato:** `_conto_del_vuoto` *(`stato_K`, `nascita`, `flip`, `conto`, `sottospazio`, `estremi_sfera`)*, `_massa_nei_difetti.H_diretto`.

Gira con:  python csv/_divisione_vuoto.py > doc/referti_l2/divisione_vuoto.txt
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
REGOLE = ("v1", "v2", "v3", "v4", "v5")
CONSERVANO = ("v1", "v3", "v4", "v5")
TOLL_NORMA = 1e-14
TOLL_V5 = 1e-12
SOGLIA_ZERO = 1e-10
LC_SU_L6 = (0.1, 1.0, 10.0)
JSONL = os.path.join(RADICE, "doc", "referti_l2", "divisione_vuoto.jsonl")
RIF = os.path.join(RADICE, "doc", "referti_l2", "conto_del_vuoto.jsonl")
OK = [0, 0]
FALLITE = []


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


def nodo_h(ii, jj):
    h = np.empty(2 * len(ii), dtype=int)
    h[0::2] = ii
    h[1::2] = jj
    return h


def phi_regola(nome, mossa, sc, dopo):
    """### `phi` sul grafo dopo la mossa, secondo la regola. ### **`(v1)` e' quello della mossa di `C3`.**"""
    import _conto_del_vuoto as C3
    import _massa_nei_difetti as MD
    ii2, jj2, nn2, _d2, _psi2, phi1, nodi, chi = dopo
    if nome == "v1":
        return phi1.copy()
    V0 = float(np.sum(np.abs(sc[5]) ** 2))
    uno = np.ones(len(phi1), dtype=complex) * sc[5][0]
    if nome == "v2":
        return uno
    if nome == "v3":
        return uno * math.sqrt(V0 / float(np.sum(np.abs(uno) ** 2)))
    nh = nodo_h(ii2, jj2)
    hS, nodiS, _ = C3.sottospazio(ii2, jj2, nn2, [nodi[x] for x in chi])
    # ### la norma di S PRIMA della mossa: le estremita' dei nodi di S che c'erano gia', sul grafo di prima
    nh0 = nodo_h(sc[0], sc[1])
    vecchi = [v for v in nodiS if v < sc[2]]
    N_S = float(np.sum(np.abs(sc[5][np.isin(nh0, vecchi)]) ** 2))
    ph = uno.copy()
    ph[hS] = math.sqrt(N_S / len(hS))
    if nome == "v4":
        return ph
    # ### v5: il massimo della parte quadratica su S, il resto fisso, alla norma N_S
    H = MD.H_diretto(ii2, jj2, nn2)
    O = np.setdiff1d(np.arange(H.shape[0]), hS)
    A = -np.pi * H[np.ix_(hS, hS)]
    b = -np.pi * (H[np.ix_(hS, O)] @ np.real(ph[O]))
    _fmin, _xmin, _fmax, xmax, _l0, _l1 = C3.estremi_sfera(A, b, N_S)
    ph[hS] = xmax
    return ph


def lambdas(ii, jj, nn, phi):
    nh = nodo_h(ii, jj)
    lam = np.zeros(nn)
    np.add.at(lam, nh, np.abs(phi) ** 2)
    return lam, np.bincount(nh, minlength=nn)


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _conto_del_vuoto as C3
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA DIVISIONE DEL VUOTO, SULLA CARTA: cinque regole di trasporto di phi alla nascita (b1) e al flip, con lo strumento di C3")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_divisione_vuoto.py", "csv/_conto_del_vuoto.py", "csv/_massa_nei_difetti.py", "doc/referti_l2/conto_del_vuoto.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LATI %s REGOLE %s CONSERVANO %s TOLL_NORMA %g TOLL_V5 %g SOGLIA_ZERO %g LC_SU_L6 %s; psi: D7 col padre i, come in C3" % (LATI, REGOLE, CONSERVANO, TOLL_NORMA, TOLL_V5, SOGLIA_ZERO, LC_SU_L6))
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    rif = {}
    for l in io.open(RIF, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "conto":
            rif[(d["mossa"], d["L"])] = d
    ris = {}
    for L in LATI:
        sc = C3.stato_K(L)
        for mossa, fn in (("nascita", C3.nascita), ("flip", C3.flip)):
            dopo = fn(L, *sc)
            ii2, jj2, nn2, dirs2, psi2 = dopo[:5]
            nodi, chi = dopo[6], dopo[7]
            lam0, g0 = lambdas(sc[0], sc[1], sc[2], sc[5])
            print("### %s, L %d" % (mossa.upper(), L))
            for nome in REGOLE:
                ph = phi_regola(nome, mossa, sc, dopo)
                r = C3.conto(L, *sc, ii2, jj2, nn2, dirs2, psi2, ph, nodi, chi)
                lam, gr = lambdas(ii2, jj2, nn2, ph)
                righe = []
                for chiave in ("n", "i", "j", "k", "l"):
                    if chiave not in nodi:
                        continue
                    v = nodi[chiave]
                    lp, dp = (lam0[v], g0[v]) if v < sc[2] else (6.0, 6)
                    q = {"nodo": chiave, "grado": int(gr[v]), "Lambda_prima": float(lp), "Lambda_dopo": float(lam[v]), "per_estremita_dopo": float(lam[v] / gr[v])}
                    for lc in LC_SU_L6:
                        Lc = lc * 6.0
                        q["dcs_nodo_%g" % lc] = (lam[v] / (lam[v] + Lc)) / (lp / (lp + Lc)) - 1.0
                        q["dcs_estr_%g" % lc] = ((lam[v] / gr[v]) / (lam[v] / gr[v] + Lc / 6.0)) / ((lp / dp) / (lp / dp + Lc / 6.0)) - 1.0
                    righe.append(q)
                r.update(regola=nome, mossa=mossa, nodi_lambda=righe)
                ris[(mossa, L, nome)] = (r, ph)
                scrivi(dict(r, tipo="regola"))
                ro = r["rotazione"]
                print("  %s: Delta H_tot %+.9e = materia %+.6e + vuoto %+.6e + legame %+.6e | V %.6f -> %.6f | la capacita' esatta [%.4e, %.4e], serve %.4e | rotazione %s"
                      % (nome, r["dH"], r["dH_materia"], r["dH_vuoto"], r["dH_legame"], r["V"][0], r["V"][1], r["esatto"][0], r["esatto"][1], r["serve"],
                         ("angolo %.4e, residuo %.1e" % (ro["angolo"], ro["residuo"])) if ro["esiste"] else "NON ESISTE"))
                for q in righe:
                    print("      %s (grado %d): Lambda %.6f -> %.6f (per estremita' %.6f); dcs/cs per nodo %s; per estremita' %s" % (q["nodo"], q["grado"], q["Lambda_prima"], q["Lambda_dopo"], q["per_estremita_dopo"],
                          " ".join("%+.3e" % q["dcs_nodo_%g" % lc] for lc in LC_SU_L6), " ".join("%+.3e" % q["dcs_estr_%g" % lc] for lc in LC_SU_L6)))
                if ro["esiste"]:
                    for q in ro["nodi"]:
                        if q["nodo"] in [nodi[x] for x in ("n", "i", "j", "k", "l") if x in nodi]:
                            print("      dopo la rotazione, nodo %d (grado %d): Lambda %.6f; dcs/cs per nodo %s" % (q["nodo"], q["grado"], q["Lambda_dopo"], " ".join("%+.3e" % q["dcs_nodo_%g" % lc] for lc in LC_SU_L6)))
                sys.stdout.flush()
    print("-" * 130)
    print("### I CRITERI")
    ok1, nota1 = True, []
    for L in LATI:
        r, _ = ris[("nascita", L, "v1")]
        d = rif[("nascita", L)]
        uguale = all(r[k] == d[k] for k in ("dH", "dH_materia", "dH_vuoto", "dH_legame")) and list(r["M"]) == d["M"] and list(r["V"]) == d["V"]
        ok1 &= uguale
        nota1.append("L %d %s" % (L, uguale))
    esito("DEVE PASSARE (1): (v1) ridà i numeri di d999cca7 AL BIT (Delta H_tot e le tre parti, M, V)", ok1, " ".join(nota1))
    ok2 = True
    for L in LATI:
        p1 = ris[("flip", L, "v1")][1]
        for nome in ("v2", "v3", "v4"):
            ok2 &= ris[("flip", L, nome)][1].tobytes() == p1.tobytes()
        ok2 &= float(np.max(np.abs(ris[("flip", L, "v5")][1] - p1))) <= TOLL_V5
    esito("DEVE PASSARE (2): il flip: v2, v3, v4 = v1 AL BIT, v5 entro %g (l'estremo della sfera e' numerico)" % TOLL_V5, ok2, "")
    ok3 = True
    for L in LATI:
        for nome in CONSERVANO:
            r = ris[("nascita", L, nome)][0]
            ok3 &= abs(r["V"][1] - r["V"][0]) / r["V"][0] <= TOLL_NORMA
        r = ris[("nascita", L, "v2")][0]
        ok3 &= r["V"][1] - r["V"][0] == 6.0
    esito("DEVE PASSARE (3): V conservata entro %g per v1, v3, v4, v5; v2 cresce di 6 esatto" % TOLL_NORMA, ok3, "")
    trov = []
    for L in LATI:
        for nome in CONSERVANO:
            r = ris[("nascita", L, nome)][0]
            if abs(r["dH"]) < SOGLIA_ZERO or (r["rotazione"]["esiste"] and abs(r["rotazione"]["residuo"]) < SOGLIA_ZERO):
                trov.append("L %d %s" % (L, nome))
    esito("PUO' FALLIRE (4): una regola con V conservata e |Delta H_tot| < %g per la nascita (con la rotazione di C3, se serve)" % SOGLIA_ZERO, bool(trov), " ".join(trov) or "nessuna", deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
