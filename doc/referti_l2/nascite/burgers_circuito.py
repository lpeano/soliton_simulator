# -*- coding: utf-8 -*-
r"""**[M1751-L] S5 RIFATTO: IL BURGERS COL CIRCUITO CHIUSO** *(la decisione di Luca: «la somma dei vettori d'arco lungo un anello che racchiude il 5 e il 7, contro lo stesso anello nel favo perfetto; se anche cosi' e' un pareggio, dirlo e chiudere S5»; `burgers.py` e' usato e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/nascite/burgers_circuito.py > doc/referti_l2/nascite/burgers_circuito.txt

**L'anello:** i nodi a UN passo dalla coppia `{5, 7}` *(il primo guscio)*; **deve essere un ciclo semplice** *(ogni nodo dell'anello con due vicini nell'anello)*: se no, la coppia si conta e si salta. **Il verso:** antiorario attorno al punto medio della coppia. **Il favo perfetto:** ogni passo dell'anello -> la piu' vicina delle sei direzioni *(un vettore unitario)*; **PAREGGIO** se il passo sta a meta' fra due direzioni *(entro `1e-6` gradi da `30`)*. **`b` = la somma dei vettori unitari** *(nel favo perfetto l'anello si chiude: `b = 0`)*. **I controlli:** due nodi adiacenti di grado `6` lontani dai difetti *(`b = 0`, DEVE)*; a `k 36000` *(una nascita)* la somma dei `b` delle due coppie zero *(DEVE)*. **Le posizioni:** una volta dal centro della materia a `k 45976` *(come `burgers.py`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import nascite_lettura as NL  # noqa: E402
import burgers as BG  # noqa: E402

TOLL_PARI = 1e-6
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def circuito(A, XY, a, b):
    """### `(b_vec, n_anello, pareggi, ok)` per la coppia `(a, b)`."""
    S = set(A[a].indices.tolist()) | set(A[b].indices.tolist())
    S -= {a, b}
    S = sorted(S)
    if len(S) < 3:
        return None, len(S), 0, False
    Ss = set(S)
    vic = {v: [w for w in A[v].indices.tolist() if w in Ss] for v in S}
    if any(len(vic[v]) != 2 for v in S):
        return None, len(S), 0, False
    giro = [S[0]]
    prec = None
    while True:
        cur = giro[-1]
        nx = [w for w in vic[cur] if w != prec]
        if len(giro) > 1 and nx[0] == giro[0]:
            break
        prec = cur
        giro.append(nx[0])
        if len(giro) > len(S):
            return None, len(S), 0, False
    if len(giro) != len(S):
        return None, len(S), 0, False
    c = 0.5 * (XY[a] + XY[b])
    P = XY[giro] - c
    area = 0.5 * float(np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1]))
    if area < 0:
        giro = giro[::-1]
    bv = np.zeros(2)
    pari = 0
    for i in range(len(giro)):
        d = XY[giro[(i + 1) % len(giro)]] - XY[giro[i]]
        ang = math.degrees(math.atan2(d[1], d[0])) % 360.0
        r = ang - 60.0 * round(ang / 60.0)
        if abs(abs(r) - 30.0) < TOLL_PARI:
            pari += 1
        q = int(round(ang / 60.0)) % 6
        bv += BG.DIREZIONI[q]
    return bv, len(S), pari, True


def main():
    import _presidio
    from solitone import toro as TO
    import coppie_57 as CP
    _presidio.avvia(os.path.join(NL._SU, "coppie_57.py"))
    _presidio.avvia(os.path.join(_QUI, "nascite_lettura.py"))
    _presidio.avvia(os.path.join(_QUI, "burgers.py"))
    _presidio.avvia(__file__)
    print("=" * 140)
    print("[M1751-L] S5 RIFATTO: IL BURGERS COL CIRCUITO CHIUSO (il primo guscio attorno alla coppia 5-7, contro il favo perfetto; PAREGGIO se un passo sta a 30 gradi da due direzioni)")
    print("=" * 140)
    Sf = CP.stato(os.path.join(NL.D_2, "stato_45976.npz"))
    XY = np.asarray(TO.scarti(Sf["m1"], Sf["m2"], Sf["centro"][0], Sf["centro"][1], NL.L))[:, :2]
    for k, f in ((36000, os.path.join(NL.D_1, "stato_36000.npz")), (36250, os.path.join(NL.D_1, "stato_36250.npz")), (45976, os.path.join(NL.D_2, "stato_45976.npz"))):
        X = NL.leggi(f)
        P, n5, n7, _altri, A = BG.coppie(X)
        if k == 45976:
            g = np.bincount(np.concatenate([X["ii"], X["jj"]]), minlength=X["n"])
            r = Sf["r"]
            lont = [v for v in range(NL.L * NL.L) if 60 < r[v] < 70 and g[v] == 6 and all(g[w] == 6 for w in A[v].indices)]
            v0 = lont[0]
            w0 = [w for w in A[v0].indices if g[w] == 6][0]
            b0, n0, p0, ok0 = circuito(A, XY, v0, int(w0))
            esito("il controllo: due nodi perfetti (%d, %d, r %.1f) -> b = 0, l'anello di %d, nessun pareggio" % (v0, w0, r[v0], n0), ok0 and float(np.linalg.norm(b0)) < 1e-9 and p0 == 0, "b %s, pareggi %d" % (np.round(b0, 6).tolist() if b0 is not None else None, p0))
        righe = []
        validi, pari_tot, lun = [], 0, []
        for p in P:
            bv, nn, pari, ok = circuito(A, XY, p["cinque"], p["sette"])
            lun.append(nn)
            if not ok:
                continue
            validi.append((p, bv, pari))
            pari_tot += int(pari > 0)
        con_pari = sum(1 for _p, _b, pr in validi if pr > 0)
        print("  k %d: %d coppie legate; l'anello un ciclo semplice in %d (le lunghezze: %s); con almeno un passo a PAREGGIO %d su %d" % (
            k, len(P), len(validi), dict(sorted(__import__("collections").Counter(lun).items())), con_pari, len(validi)))
        senza = [(p, bv) for p, bv, pr in validi if pr == 0]
        if senza:
            bs = np.array([bv for _p, bv in senza])
            mod = np.linalg.norm(bs, axis=1)
            print("    senza pareggi (%d): |b| %s; la somma dei b %s" % (len(senza), dict(sorted(__import__("collections").Counter(np.round(mod, 6)).items())), np.round(bs.sum(axis=0), 6).tolist()))
        if k == 36000:
            if len(validi) == 2 and con_pari == 0:
                sb = validi[0][1] + validi[1][1]
                esito("K1 a k 36000: la somma dei b delle due coppie zero", float(np.linalg.norm(sb)) < 1e-9, "%s" % np.round(sb, 6).tolist())
            else:
                esito("K1 a k 36000: la somma dei b delle due coppie zero", None, "anelli validi %d, con pareggio %d" % (len(validi), con_pari))
    print("=" * 140)
    fall = [k for k, v in OK.items() if v is False]
    nm = [k for k, v in OK.items() if v is None]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s, %d NON MISURATI %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall, len(nm), nm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
