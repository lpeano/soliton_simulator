# -*- coding: utf-8 -*-
r"""**[M1013] C-1, I CASI NOTI DELLA CURA DEL FLIP ILLEGALE** *(DECISIONE DI LUCA, 2026-11-28 10:13; la carta `doc/CARTA_mitosi.md`, sezione
«C, LA CURA DEL FLIP ILLEGALE E LA LETTURA SU 0-16250»; nessun tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/flip_illegale_noto.py > doc/referti_l2/flip_illegale_noto.txt

`mitosi_regola_v2.flip_illegale(nb, n, x, y)` e `flip_illegali(ii, jj, n, ori, a)`:
- (CF1) il toro triangolare `6 x 6`: una nascita, i quattro flip LEGALI;
- (CF2) un vertice di grado 4 *(il disco `i` con l'anello `j - k - m - l`)*: il flip `i - k` crea il 3-ciclo `n - m - l` che non e' una faccia: ILLEGALE;
- (CF3) un vertice di grado 3 *(un triangolo del toro diviso da un nodo)*: il flip crea l'arco doppio: ILLEGALE;
- (CF4) DEVE FALLIRE: con il controllo dei vicini comuni tolto, CF2 passa per legale;
- (CF5) il rigioco topologico delle nascite di `M0026/C/nascite.json` *(602)* dal toro della scena: nessun flip illegale fra i quattro lati di
  NESSUNA nascita *(la corsa ne aveva calcolati i candidati tutti senza fermarsi)*, e il grafo finale = `stato_016250` *(ii, jj)* come insieme di archi;
- (CF6) `flip_illegali` sugli array = la versione a insiemi, sugli archi attorno a `26431` e `26547` di `stato_016250`;
- il censimento a `k 16250`: quanti archi avrebbero almeno un flip illegale se nascessero ora *(una lettura, non un DEVE)*.
"""
import collections
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_regola_v2 as MR2  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
D_C = os.path.join(CTRL, "M0026", "C")
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def adiacenza(ii, jj):
    adj = collections.defaultdict(set)
    for a, b in zip(np.asarray(ii).tolist(), np.asarray(jj).tolist()):
        adj[a].add(b)
        adj[b].add(a)
    return adj


def nasci_adj(adj, i, j, k, l, n):
    adj[i].discard(j)
    adj[j].discard(i)
    for v in (i, j, k, l):
        adj[n].add(v)
        adj[v].add(n)


def lati(i, j, k, l):
    return ((i, k), (j, k), (j, l), (i, l))


def toro(L):
    ii, jj = [], []
    for p in range(L):
        for q in range(L):
            v = p * L + q
            for dp, dq in ((1, 0), (0, 1), (1, 1)):
                ii.append(v)
                jj.append(((p + dp) % L) * L + (q + dq) % L)
    return np.array(ii), np.array(jj)


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_regola_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 134)
    print("[M1013] C-1, I CASI NOTI DELLA CURA DEL FLIP ILLEGALE (mitosi_regola_v2.flip_illegale, flip_illegali)")
    print("=" * 134)
    # ### CF1: il toro 6 x 6, la nascita sull'arco 0
    ii, jj = toro(6)
    adj = adiacenza(ii, jj)
    i, j = int(ii[0]), int(jj[0])
    k, l = sorted(adj[i] & adj[j])
    n = 36
    nasci_adj(adj, i, j, k, l, n)
    mot = [MR2.flip_illegale(adj.__getitem__, n, x, y) for x, y in lati(i, j, k, l)]
    esito("(CF1) il toro 6 x 6, la nascita sull'arco %d - %d: i quattro flip LEGALI" % (i, j), all(x is None for x in mot), "%s" % mot)
    # ### CF2: il disco col vertice i di grado 4, l'anello j - k - m - l
    I, J, K, M, Lv, N = 0, 1, 2, 3, 4, 5
    adj = adiacenza([I, I, I, I, J, K, M, Lv], [J, K, M, Lv, K, M, Lv, J])
    assert adj[I] & adj[J] == {K, Lv}
    nasci_adj(adj, I, J, K, Lv, N)
    m2 = MR2.flip_illegale(adj.__getitem__, N, I, K)
    esito("(CF2) il vertice di grado 4: il flip i - k crea il 3-ciclo n - m - l, ILLEGALE", m2 is not None and "3-ciclo" in m2, "%r" % m2)
    m4 = MR2.flip_illegale(adj.__getitem__, N, I, K, controlla_comuni=False)
    esito("(CF4) DEVE FALLIRE: senza il controllo dei vicini comuni CF2 passa per legale", m4 is None, "%r" % m4)
    # ### CF3: un triangolo del toro diviso da un nodo v (grado 3); la nascita su v - c1
    ii, jj = toro(6)
    adj = adiacenza(ii, jj)
    c1, c2, c3 = 0, 1, 7                      # ### il triangolo (0, 1, 7): (p, q) -> (p, q+1), (p+1, q+1)
    assert c2 in adj[c1] and c3 in adj[c1] and c3 in adj[c2]
    v = 36
    for c in (c1, c2, c3):
        adj[v].add(c)
        adj[c].add(v)
    kk, ll = sorted(adj[v] & adj[c1])
    nasci_adj(adj, v, c1, kk, ll, 37)
    m3 = [MR2.flip_illegale(adj.__getitem__, 37, x, y) for x, y in lati(v, c1, kk, ll)]
    esito("(CF3) il vertice di grado 3: i flip dal lato del nodo diviso creano l'arco DOPPIO, ILLEGALE", any(x is not None and "doppio" in x for x in m3), "%s" % m3)
    # ### CF5: il rigioco topologico delle nascite di M0026/C
    import corpo_fuso_mitosi as CFM
    with CFM.V6.GD.TC.scena() as Z:
        ii0, jj0, n0 = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2]), int(Z["mot"].inc.n)
        Z["metti"]()
    adj = adiacenza(ii0, jj0)
    B = json.load(open(os.path.join(D_C, "nascite.json"), encoding="utf-8"))
    illegali, coerenti, n_att = [], 0, n0
    for q, b in enumerate(B):
        nd = b["nodi"]
        i, j, k, l, n = nd["i"], nd["j"], nd["k"], nd["l"], nd["n"]
        ok = n == n_att and j in adj[i] and adj[i] & adj[j] == {k, l}
        nasci_adj(adj, i, j, k, l, n)
        for x, y in lati(i, j, k, l):
            mt = MR2.flip_illegale(adj.__getitem__, n, x, y)
            if mt is not None:
                illegali.append((q + 1, b["k"], (x, y), mt))
        if b["scelto"] >= 0:
            x, y = lati(i, j, k, l)[b["scelto"]]
            m = next(iter((adj[x] & adj[y]) - {n}))
            ok = ok and m == nd["m"]
            adj[x].discard(y)
            adj[y].discard(x)
            adj[n].add(m)
            adj[m].add(n)
        coerenti += int(ok)
        n_att += 1
    with np.load(os.path.join(D_C, "stato_016250.npz")) as z:
        iiF, jjF, ori_c = z["ii"], z["jj"], z["ori_cicli"]
        meta = json.loads(str(z["meta"]))
    E_rig = set((min(a, b), max(a, b)) for a in adj for b in adj[a])
    E_st = set((min(a, b), max(a, b)) for a, b in zip(iiF.tolist(), jjF.tolist()))
    print("  CF5: %d nascite rigiocate (meta di stato_016250: %d); coerenti col registro (n, l'arco i - j, i vicini comuni {k, l}, m) %d; flip illegali %d" % (
        len(B), meta["nascite"], coerenti, len(illegali)))
    esito("(CF5) il rigioco: tutte le nascite coerenti col registro e il grafo finale = stato_016250 come insieme di archi",
          coerenti == len(B) == meta["nascite"] and E_rig == E_st, "archi %d contro %d; diversi %d" % (len(E_rig), len(E_st), len(E_rig ^ E_st)))
    esito("(CF5) nessun flip illegale fra i quattro lati di nessuna delle %d nascite (la corsa li aveva calcolati tutti)" % len(B), not illegali, "%s" % illegali[:3])
    # ### CF6 e il censimento a 16250
    nF = int(meta["n"])
    ori = {tuple(sorted(c)): tuple(c) for c in ori_c.tolist()}
    adjF = adiacenza(iiF, jjF)
    archi = [a for a in range(len(iiF)) if {int(iiF[a]), int(jjF[a])} & {26431, 26547}]
    diversi = 0
    for a in archi:
        arr = MR2.flip_illegali(iiF, jjF, nF, ori, a)
        i, j = int(iiF[a]), int(jjF[a])
        k, l = sorted(adjF[i] & adjF[j])
        ad = collections.defaultdict(set, {v: set(s) for v, s in adjF.items()})
        nasci_adj(ad, i, j, k, l, nF)
        st = sorted(tuple(sorted(lt)) for lt in lati(i, j, k, l) if MR2.flip_illegale(ad.__getitem__, nF, lt[0], lt[1]) is not None)
        diversi += int(sorted(tuple(sorted(lt)) for lt, _m in arr) != st)
    esito("(CF6) flip_illegali sugli array = la versione a insiemi, sui %d archi attorno a 26431 e 26547" % len(archi), diversi == 0, "diversi %d" % diversi)
    cens, tipi = 0, collections.Counter()
    for a in range(len(iiF)):
        i, j = int(iiF[a]), int(jjF[a])
        com = adjF[i] & adjF[j]
        if len(com) != 2:
            tipi["l'arco senza due vicini comuni"] += 1
            continue
        k, l = sorted(com)

        def nb(v, i=i, j=j, k=k, l=l):
            s = set(adjF[v])
            if v == i:
                s.discard(j)
            if v == j:
                s.discard(i)
            if v in (i, j, k, l):
                s.add(nF)
            return s if v != nF else {i, j, k, l}
        mm = [MR2.flip_illegale(nb, nF, x, y) for x, y in lati(i, j, k, l)]
        mm = [x for x in mm if x is not None]
        if mm:
            cens += 1
            for x in mm:
                tipi["doppio" if "doppio" in x else "3-ciclo"] += 1
    print("  IL CENSIMENTO a k 16250: %d archi su %d avrebbero almeno un flip illegale se nascessero ora; i flip illegali per tipo %s" % (cens, len(iiF), dict(tipi)))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
