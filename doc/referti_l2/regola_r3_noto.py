# -*- coding: utf-8 -*-
r"""**[M1056] R3, I CASI NOTI DI `mitosi_regola_v2.regola_r3`** *(DECISIONE DI LUCA, 2026-11-28 10:56; la carta `doc/CARTA_mitosi.md`, «C, R3 E LA
RIPRESA DA 16250»; nessun motore: `candidato` e, per CF5', `flip_illegale` sostituiti da stub)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/regola_r3_noto.py > doc/referti_l2/regola_r3_noto.txt

- (CF-eq) tutti i lati legali *(il toro 6 x 6)*: `R` *(le chiavi di `regola`)* e `S` di `regola_r3` = quelli di `regola` AL BIT, anche nel caso «pari»;
- (CF5') UN lato illegale *(`flip_illegale` stub: solo il lato 1)*: la nascita avviene, e il flip e' il migliore fra i tre legali, anche quando il
  migliore in assoluto era quello scartato;
- (CF-coppie) il grafo a mano col vertice `i` di grado 4 *(e `j` di grado 5)*: `flip_illegale` vero scarta ESATTAMENTE i lati `i - k` e `i - l`;
- (CF6') il grafo a mano coi vertici `i` e `j` di grado 4: i quattro lati illegali, `nas` *(`scelto -1`)*, `senza_flip`.
"""
import collections
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_regola_v2 as MR2  # noqa: E402

OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def dopo_nascita(ii, jj, i, j, k, l, n):
    keep = ~(((ii == i) & (jj == j)) | ((ii == j) & (jj == i)))
    return np.concatenate([ii[keep], [n] * 4]), np.concatenate([jj[keep], [i, j, k, l]])


def stub(ii, jj, i, j, k, l, n, H):
    """### `candidato` finto: `nas` col grafo dopo la nascita, ogni lato con la sua `H` dalla tabella `H` *(chiave: il lato, o None)*."""
    ii2, jj2 = dopo_nascita(np.asarray(ii), np.asarray(jj), i, j, k, l, n)

    def cand(Z, C, a, lato, giro, *_a, **_k):
        nd = {"i": i, "j": j, "k": k, "l": l, "n": n}
        if lato is not None:
            nd["m"] = -1
        return {"H": H[lato], "nodi": nd, "ii": ii2, "jj": jj2, "t": 0.0, "lato": lato}
    return cand


def toro(L):
    ii, jj = [], []
    for p in range(L):
        for q in range(L):
            v = p * L + q
            for dp, dq in ((1, 0), (0, 1), (1, 1)):
                ii.append(v)
                jj.append(((p + dp) % L) * L + (q + dq) % L)
    return np.array(ii), np.array(jj)


def stella(ii, jj, a):
    adj = collections.defaultdict(set)
    for x, y in zip(ii.tolist(), jj.tolist()):
        adj[x].add(y)
        adj[y].add(x)
    i, j = int(ii[a]), int(jj[a])
    k, l = sorted(adj[i] & adj[j])
    return i, j, k, l


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_regola_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 134)
    print("[M1056] R3, I CASI NOTI DI regola_r3 (stub di candidato; GUARDIA %r)" % MR2.GUARDIA)
    print("=" * 134)
    orig_c, orig_f = MR2.candidato, MR2.flip_illegale
    try:
        ii, jj = toro(6)
        i, j, k, l = stella(ii, jj, 0)
        n = 36
        lati = ((i, k), (j, k), (j, l), (i, l))
        for nome, Hl in (("netto", (-5.0, -7.0, -6.0, -4.0)), ("pari", (-7.0, -7.0 * (1 + 0.1 * MR2.GUARDIA), -6.0, -4.0))):
            H = {None: -3.0}
            H.update({lt: h for lt, h in zip(lati, Hl)})
            MR2.candidato = stub(ii, jj, i, j, k, l, n, H)
            R1, S1 = MR2.regola(None, None, 0)
            R3, S3 = MR2.regola_r3(None, None, 0)
            comuni = ("H", "H_nascita", "scelto", "gap", "lati", "nodi", "t")
            dR = [x for x in comuni if R1[x] != R3[x]]
            esito("(CF-eq, %s) tutti legali: R (le chiavi di regola) e S di regola_r3 = regola AL BIT" % nome,
                  not dR and S1["lato"] == S3["lato"] and S1["H"] == S3["H"] and R3["scartati"] == [] and not R3["senza_flip"],
                  "scelto %d / %d; diverse %s" % (R1["scelto"], R3["scelto"], dR))
        # ### CF5': un lato illegale (stub), il migliore in assoluto
        H = {None: -3.0}
        H.update({lt: h for lt, h in zip(lati, (-5.0, -9.0, -6.0, -4.0))})
        MR2.candidato = stub(ii, jj, i, j, k, l, n, H)
        MR2.flip_illegale = lambda nb, n_, x, y, controlla_comuni=True: "stub" if (x, y) == lati[1] else None
        R3, S3 = MR2.regola_r3(None, None, 0)
        esito("(CF5') un lato illegale (il migliore in assoluto, H -9): la nascita avviene col migliore dei tre legali (il lato 2, H -6)",
              R3["scartati"] == [1] and R3["scelto"] == 2 and S3["lato"] == lati[2] and not R3["senza_flip"], "scartati %s, scelto %d" % (R3["scartati"], R3["scelto"]))
        MR2.flip_illegale = orig_f
        # ### CF-coppie: i di grado 4, j di grado 5
        I, J, K, Lv, M, M2, Pp, N = 0, 1, 2, 3, 4, 5, 6, 7
        e = [(I, J), (I, K), (I, M), (I, Lv), (J, K), (K, M), (M, Lv), (Lv, J), (J, M2), (K, M2), (J, Pp), (M2, Pp), (Pp, Lv)]
        ii, jj = np.array([x for x, _ in e]), np.array([y for _, y in e])
        lati = ((I, K), (J, K), (J, Lv), (I, Lv))
        H = {None: -3.0}
        H.update({lt: h for lt, h in zip(lati, (-5.0, -7.0, -6.0, -4.0))})
        MR2.candidato = stub(ii, jj, I, J, K, Lv, N, H)
        R3, S3 = MR2.regola_r3(None, None, 0)
        esito("(CF-coppie) i di grado 4: scartati ESATTAMENTE i lati i - k e i - l (gli indici 0 e 3); il flip fra j - k e j - l",
              R3["scartati"] == [0, 3] and R3["scelto"] == 1, "scartati %s %s, scelto %d" % (R3["scartati"], R3["motivi"], R3["scelto"]))
        # ### CF6': i e j di grado 4
        I, J, K, Lv, M, M2, N = 0, 1, 2, 3, 4, 5, 6
        e = [(I, J), (I, K), (I, M), (I, Lv), (J, K), (J, M2), (J, Lv), (K, M), (M, Lv), (K, M2), (M2, Lv)]
        ii, jj = np.array([x for x, _ in e]), np.array([y for _, y in e])
        lati = ((I, K), (J, K), (J, Lv), (I, Lv))
        H = {None: -3.0}
        H.update({lt: h for lt, h in zip(lati, (-5.0, -7.0, -6.0, -4.0))})
        MR2.candidato = stub(ii, jj, I, J, K, Lv, N, H)
        R3, S3 = MR2.regola_r3(None, None, 0)
        esito("(CF6') i e j di grado 4: i quattro lati illegali, la nascita SENZA flip (nas, scelto -1), senza_flip",
              R3["scartati"] == [0, 1, 2, 3] and R3["scelto"] == -1 and S3["lato"] is None and R3["senza_flip"], "scartati %s, scelto %d" % (R3["scartati"], R3["scelto"]))
    finally:
        MR2.candidato, MR2.flip_illegale = orig_c, orig_f
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
