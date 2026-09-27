# -*- coding: utf-8 -*-
"""**`OSSERVABILE-P1` -- LA DISTANZA FRA DUE MASSE LUNGO IL GRAFO, PESATA CON `d`.**

*(Strumento UFFICIALE. Mandato di Luca, 2026-09-27. I criteri sono in
`doc/TASK_HISTORY/2026-09-27_osservabile-p1.md`, committato prima.)*

> *(❗ ETICHETTA CORRETTA il 2026-09-27, rilievo di Luca: la regola e' **`A3-DISEGNO`**,
> non `A13` -- `A13` e' «`LAM` e' la scala di Planck del sistema». L'avevo propagata
> dalla revisione senza verificarla: `P1` applicato a un'etichetta.)*
>
> ### **La `PROVA 1` chiede *«due masse si avvicinano?»*, e la distanza del sistema STA SUGLI
> ### ARCHI (`A3-DISEGNO`), NON SU `pos`.** I pesi sono **`net.d`**. **`pos` non entra mai**:
> ### compare solo in un **diagnostico** che serve a DIMOSTRARE che non entra.

**CHE COSA DA', su uno snapshot o su una rete viva:**

1. la distanza **fra i CENTRI** di ogni coppia di regioni, lungo il grafo, pesi `d`;
2. la distanza **INSIEME-INSIEME** della stessa coppia *(il minimo fra un nodo qualunque di `A` e
   uno qualunque di `B`)* -- **non ha bisogno di un centro**, e risponde a *«quanto distano le
   superfici»* invece di *«quanto distano i cuori»*;
3. gli stessi due numeri fra **punti di CONTROLLO nel vuoto**, alla **stessa distanza iniziale** e
   **lontani dalle masse**: e' **il braccio di confronto della `PROVA 1`**;
4. la **dispersione FRA SEMI** su `>= 4` semi, con il `t` di Student giusto (`P3`).

**IL CENTRO E' IL MEDOIDE DI GRAFO**, non un baricentro: il nodo della regione che **minimizza la
somma delle distanze pesate con `d`** verso gli altri nodi della regione, **sul sottografo
indotto**. **Nessun `pos`.** *(Pareggi: si prende **l'indice minore**, e il numero dei pari si
DICHIARA.)*

**SE DUE REGIONI SONO IN COMPONENTI DIVERSE la distanza e' `inf`**, e lo strumento **lo dice**:
un `inf` stampato come numero sarebbe illeggibile (`A8`).

    python csv/_osservabile_p1.py --scena                 # costruisce la scena (ii) e misura
    python csv/_osservabile_p1.py --snap <file.pkl[.gz]>  # misura su uno snapshot
    python csv/_osservabile_p1.py --scena --semi 11,12,13,14   # la dispersione fra semi
    python csv/_osservabile_p1.py --collaudo              # K1: i grafi sintetici

ASCII puro.
"""
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
sys.path.insert(0, _QUI)

import _presidio                                                       # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: la configurazione si dichiara solo quando si COSTRUISCE una scena (`--scena`), e
#   li' lo strumento chiama `_cli_flag.dichiara_configurazione`. Su `--snap` e `--collaudo` non
#   c'e' un simulatore configurato da dichiarare: c'e' un file, o un grafo sintetico.

NL = chr(10)
TOLL_CONTROLLO = 0.10          # la tolleranza dei punti di controllo: SCRITTA PRIMA (`K4`)
SCENA2 = "MASSE-COERENTI"


# ============================================================================ IL GRAFO E I CAMMINI
def grafo(i, j, pesi, n):
    """La matrice sparsa del grafo, **con i pesi dati**.

    E' l'idioma dei quattro script che contano le componenti connesse
    (`_letture_ab.py`, `_topologia.py`, `_topologia_blocchi.py`, `_pilota_sep.py`), con **una sola
    differenza, che e' il punto di questo strumento: i loro pesi sono `np.ones` -- il CONTEGGIO
    DEI SALTI -- e qui sono `d`, la LUNGHEZZA.**
    """
    from scipy.sparse import coo_matrix
    i = np.asarray(i, int)
    j = np.asarray(j, int)
    w = np.asarray(pesi, float)
    m = (i < n) & (j < n) & (i >= 0) & (j >= 0) & np.isfinite(w) & (w > 0)
    return coo_matrix((w[m], (i[m], j[m])), shape=(n, n)).tocsr(), int(m.sum()), int((~m).sum())


def distanze(g, sorgenti):
    """Dijkstra da `sorgenti` sul grafo NON orientato. Matrice `(len(sorgenti), n)`."""
    from scipy.sparse.csgraph import dijkstra
    return dijkstra(g, directed=False, indices=np.asarray(sorgenti, int))


def componenti(g):
    from scipy.sparse.csgraph import connected_components
    nc, lab = connected_components(g, directed=False)
    return int(nc), lab


def medoide(g, idx):
    """**IL CENTRO: il medoide di grafo della regione, sul SOTTOGRAFO INDOTTO. Nessun `pos`.**

    Restituisce `(nodo, quanti_pari, raggiungibili)`. Il sottografo indotto e' la scelta giusta:
    un medoide calcolato sul grafo INTERO potrebbe scegliere un nodo il cui cammino verso la
    regione passa **fuori** dalla regione, e allora non sarebbe il centro di quella regione.
    """
    idx = np.asarray(sorted(set(int(x) for x in idx)), int)
    if len(idx) == 0:
        return -1, 0, 0
    if len(idx) == 1:
        return int(idx[0]), 1, 1
    sub = g[idx, :][:, idx]
    d = distanze(sub, np.arange(len(idx)))
    fin = np.isfinite(d)
    somma = np.where(fin, d, 0.0).sum(axis=1)
    somma[fin.sum(axis=1) < fin.sum(axis=1).max()] = np.inf     # chi raggiunge meno nodi perde
    best = float(np.min(somma))
    pari = int(np.sum(somma == best))
    # PAREGGI: si prende l'INDICE MINORE. Regola dichiarata, non caso taciuto.
    k = int(np.argmin(somma))
    return int(idx[k]), pari, int(fin.sum(axis=1).max())


def fra_insiemi(g, a, b):
    """La distanza INSIEME-INSIEME: il minimo fra un nodo di `a` e uno di `b`. Nessun centro."""
    a = np.asarray(sorted(set(int(x) for x in a)), int)
    b = np.asarray(sorted(set(int(x) for x in b)), int)
    if not len(a) or not len(b):
        return float("nan")
    d = distanze(g, a)[:, b]
    return float(np.min(d))


# ============================================================================ LE MISURE SULLA RETE
def misura(net, coorti, r_regione=None, pesi_da_pos=False):
    """Il dizionario delle misure. `pesi_da_pos=True` e' **il caso che DEVE fallire** (`K2`)."""
    n = int(net.n)
    if pesi_da_pos:
        p = np.asarray(net.pos, float)
        w = np.linalg.norm(p[np.asarray(net.i, int)] - p[np.asarray(net.j, int)], axis=1)
        etichetta = "pos (DIAGNOSTICO: serve a dimostrare che la misura vera NON lo usa)"
    else:
        w = np.asarray(net.d, float)
        etichetta = "d (net.d, la lunghezza d'arco)"
    g, usati, scartati = grafo(net.i, net.j, w, n)
    nc, lab = componenti(g)
    masse = sorted(k for k in coorti if k.startswith("massa_"))
    o = {"pesi": etichetta, "n": n, "archi_usati": usati, "archi_scartati": scartati,
         "componenti": nc, "masse": masse, "coppie": {}, "centri": {}, "pari_medoide": {}}
    for k in masse:
        c, pari, ragg = medoide(g, coorti[k])
        o["centri"][k] = c
        o["pari_medoide"][k] = pari
    for x in range(len(masse)):
        for y in range(x + 1, len(masse)):
            ka, kb = masse[x], masse[y]
            ca, cb = o["centri"][ka], o["centri"][kb]
            dc = float(distanze(g, [ca])[0, cb]) if ca >= 0 and cb >= 0 else float("nan")
            o["coppie"]["%s|%s" % (ka, kb)] = {
                "centro_centro": dc,
                "insieme_insieme": fra_insiemi(g, coorti[ka], coorti[kb]),
                "stessa_componente": bool(ca >= 0 and cb >= 0 and lab[ca] == lab[cb])}
    o["_g"], o["_lab"] = g, lab
    return o


def controlli(o, coorti, r_regione, toll=TOLL_CONTROLLO):
    """I punti di CONTROLLO nel vuoto: **stessa distanza entro `toll`**, **lontani dalle masse**.

    «Lontani» ha un metro DICHIARATO e preso dalla scena, non scelto: la distanza di grafo da
    **ogni** nodo di massa deve superare `r_regione`. Se non se ne trovano, si DICE -- e `K4`
    fallisce, invece di allargare la tolleranza dopo aver guardato (`P1-sexies`).
    """
    g = o["_g"]
    vuoto = np.asarray(sorted(set(int(x) for x in coorti.get("vuoto", []))), int)
    tutte = np.asarray(sorted(set(int(x) for k in o["masse"] for x in coorti[k])), int)
    fuori = {}
    if not len(vuoto) or not len(tutte):
        return {"trovati": 0, "coppie": {}, "nota": "nessun vuoto o nessuna massa"}
    # distanza di OGNI nodo dalle masse: una sola Dijkstra multi-sorgente
    dm = distanze(g, tutte).min(axis=0)
    lontani = vuoto[np.isfinite(dm[vuoto]) & (dm[vuoto] > float(r_regione))]
    fuori["candidati_lontani"] = int(len(lontani))
    fuori["metro_lontananza"] = float(r_regione)
    if len(lontani) < 2:
        fuori.update(trovati=0, coppie={},
                     nota="meno di due nodi di vuoto oltre `r_regione` dalle masse")
        return fuori
    # per ogni coppia di masse, si cerca una coppia di controllo alla STESSA distanza
    rng = np.random.default_rng(0)          # la scelta dei candidati e' DETERMINISTICA (`K3`)
    quanti = min(120, len(lontani))
    scelti = np.sort(rng.choice(lontani, size=quanti, replace=False)) if len(lontani) > quanti \
        else lontani
    dd = distanze(g, scelti)[:, scelti]
    trovate = {}
    for nome, v in o["coppie"].items():
        bersaglio = v["centro_centro"]
        if not np.isfinite(bersaglio) or bersaglio <= 0:
            continue
        rel = np.abs(dd - bersaglio) / bersaglio
        np.fill_diagonal(rel, np.inf)
        k = int(np.argmin(rel))
        a, b = np.unravel_index(k, rel.shape)
        trovate[nome] = {"nodo_a": int(scelti[a]), "nodo_b": int(scelti[b]),
                         "distanza": float(dd[a, b]),
                         "bersaglio": float(bersaglio),
                         "scarto_relativo": float(rel[a, b]),
                         "entro_toll": bool(rel[a, b] <= toll)}
    fuori.update(trovati=len(trovate), coppie=trovate, toll=float(toll))
    return fuori


# ============================================================================ LA DISPERSIONE (P3)
_T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
         9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 15: 2.131, 20: 2.086, 30: 2.042}


def dispersione(valori):
    """`(media, sd, se, ic95, t_usato, gdl)`. **Sotto 4 semi non si restituisce una barra.**"""
    v = np.asarray([x for x in valori if np.isfinite(x)], float)
    k = len(v)
    if k < 2:
        return dict(n=k, media=float(v[0]) if k else float("nan"), sd=float("nan"),
                    se=float("nan"), ic95=None, t=None, gdl=0,
                    nota="un solo seme: nessuna barra (`P3`)")
    gdl = k - 1
    sd = float(np.std(v, ddof=1))
    se = sd / np.sqrt(k)
    t = _T975.get(gdl, 1.96)
    o = dict(n=k, media=float(np.mean(v)), sd=sd, se=se, t=t, gdl=gdl,
             ic95=(float(np.mean(v) - t * se), float(np.mean(v) + t * se)))
    if k < 4:
        o["nota"] = ("SOTTO I 4 SEMI: con %d gdl il `t` vale %.3f e l'IC95 e' inutilizzabile "
                     "(`P3`). Il numero si riporta, la BARRA no." % (gdl, t))
    return o


# ============================================================================ LE DUE SORGENTI
def da_scena(seme=None, sep=None):
    """Costruisce la scena `(ii)` **passando dal CLI del driver** e restituisce `(net, coorti, r)`.

    ⚠ **`_NMASSE_VIDEO` VA RIEMPITO**: le tre righe che lo riempiono stanno **DOPO** l'ancora
    `_applica_flag`, quindi `argv_del_driver` non le esegue. Senza questo la scena girerebbe col
    `sep` di MODULO (`3.0`) invece di quello del driver: **misurato il 2026-09-26, `n = 2124`
    invece di `12 814`**, ed e' un numero misurato in un'altra configurazione (`CONFIG-1`).
    """
    import _cli_flag
    extra = []
    if seme is not None:
        extra.append("--seme=%d" % int(seme))
    if sep is not None:
        extra.append("--sep=%s" % sep)
    _S0, argv = _cli_flag.argv_del_driver(extra=extra,
                                         dest=os.path.join(_QUI, "_test_fork", "_scarto_cli"))
    S, a = _cli_flag.carica_dal_cli(argv, nome="sim_op1_%s" % (seme if seme is not None else "def"))
    S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
    S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test(SCENA2)()
    dati = S.test["dati"]
    return S, dati["coorti"], float(dati["scena_ii"]["r_regione"]), argv


class _ReteFinta(object):
    """La rete letta da uno snapshot: solo i campi che servono al cammino."""

    def __init__(self, attrs):
        self.i = np.asarray(attrs["i"], int)
        self.j = np.asarray(attrs["j"], int)
        self.d = np.asarray(attrs["d"], float)
        self.pos = np.asarray(attrs["pos"], float)
        self.n = int(len(attrs["phi"]))


def da_snapshot(percorso):
    """`(net_finta, coorti, r_regione)` da uno snapshot. Le coorti devono ESSERCI."""
    import pickle
    ap = (__import__("gzip").open if percorso.endswith(".gz") else open)
    with ap(percorso, "rb") as f:
        dd = pickle.load(f)
    attrs = dd.get("attrs") or {}
    net = _ReteFinta(attrs)
    co = attrs.get("conc_nodi")
    dati = dd.get("test_dati") or {}
    coorti = dati.get("coorti") or {}
    if not coorti:
        raise SystemExit(
            "[osservabile-p1] LO SNAPSHOT NON PORTA LE COORTI, e senza quelle non si sa DOVE"
            + NL + "  sono le masse. Non le invento da `pos` (`A3-DISEGNO`): si rigira la scena,"
            + NL + "  usa `--scena`. *(`conc_nodi` presente: %s -- ma la scena (ii) NON lo tocca,"
            % (co is not None) + NL + "  di proposito: le regioni non sono masse seminate.)*")
    return net, coorti, float(dati.get("scena_ii", {}).get("r_regione", 0.0))


# ============================================================================ IL COLLAUDO (K1)
def collaudo():
    """**`K1`: grafi SINTETICI a distanza NOTA.** Catena e reticolo. Errore atteso `< 1e-12`."""
    print("=" * 96)
    print("COLLAUDO `K1` -- grafi SINTETICI a distanza NOTA (`P1-sexies`)")
    print("=" * 96)
    ok = True
    # --- CATENA: 0-1-2-...-N-1 con pesi w_k. La distanza fra a e b e' la SOMMA del tratto.
    N = 12
    w = np.array([0.5, 1.0, 1.5, 2.0, 0.25, 3.0, 1.25, 0.75, 2.5, 1.75, 0.125], float)
    i = np.arange(N - 1)
    j = np.arange(1, N)
    g, _u, _s = grafo(i, j, w, N)
    for a, b in ((0, N - 1), (2, 7), (5, 6), (0, 1)):
        atteso = float(w[a:b].sum())
        misurato = float(distanze(g, [a])[0, b])
        err = abs(misurato - atteso)
        buono = err < 1e-12
        ok = ok and buono
        print("  catena  %2d -> %2d   atteso %12.9f   misurato %12.9f   errore %.3e  %s"
              % (a, b, atteso, misurato, err, "OK" if buono else "!! SBAGLIATO"))
    # --- RETICOLO m x m a pesi UNITARI: la distanza e' MANHATTAN.
    m = 7
    ii, jj = [], []
    for r in range(m):
        for c in range(m):
            k = r * m + c
            if c + 1 < m:
                ii.append(k); jj.append(k + 1)
            if r + 1 < m:
                ii.append(k); jj.append(k + m)
    g2, _u2, _s2 = grafo(ii, jj, np.ones(len(ii)), m * m)
    for (r1, c1), (r2, c2) in (((0, 0), (6, 6)), ((1, 2), (5, 3)), ((3, 3), (3, 6))):
        atteso = float(abs(r1 - r2) + abs(c1 - c2))
        misurato = float(distanze(g2, [r1 * m + c1])[0, r2 * m + c2])
        err = abs(misurato - atteso)
        buono = err < 1e-12
        ok = ok and buono
        print("  reticolo (%d,%d)->(%d,%d)   atteso %5.1f   misurato %5.1f   errore %.3e  %s"
              % (r1, c1, r2, c2, atteso, misurato, err, "OK" if buono else "!! SBAGLIATO"))
    # --- il caso che DEVE dare `inf`: due componenti staccate
    g3, _u3, _s3 = grafo([0, 2], [1, 3], [1.0, 1.0], 4)
    inf_ok = not np.isfinite(distanze(g3, [0])[0, 3])
    nc3, _l3 = componenti(g3)
    ok = ok and inf_ok and nc3 == 2
    print("  staccati  0 -> 3   atteso inf   misurato %s   componenti %d  %s"
          % (distanze(g3, [0])[0, 3], nc3, "OK" if (inf_ok and nc3 == 2) else "!! SBAGLIATO"))
    # --- il MEDOIDE su una catena a pesi unitari: e' il nodo di mezzo, e si sa quale
    g4, _u4, _s4 = grafo(np.arange(6), np.arange(1, 7), np.ones(6), 7)
    med, pari, _rg = medoide(g4, list(range(7)))
    ok = ok and (med == 3) and (pari == 1)
    print("  medoide  catena di 7 a pesi 1   atteso 3 (unico)   misurato %d (pari %d)  %s"
          % (med, pari, "OK" if (med == 3 and pari == 1) else "!! SBAGLIATO"))
    print()
    print("COLLAUDO `K1`: %s" % ("OK" if ok else "FALLITO"))
    return 0 if ok else 1


# ============================================================================ LA STAMPA
def stampa(o, ctrl, P=print):
    P("  pesi del cammino ......... %s" % o["pesi"])
    P("  n %d   archi usati %d   scartati %d   componenti %d"
      % (o["n"], o["archi_usati"], o["archi_scartati"], o["componenti"]))
    P("  centri (MEDOIDE DI GRAFO, nessun `pos`):  %s"
      % "  ".join("%s=%d%s" % (k, v, "" if o["pari_medoide"][k] == 1
                               else " (%d pari, preso l'indice minore)" % o["pari_medoide"][k])
                  for k, v in sorted(o["centri"].items())))
    for nome, v in sorted(o["coppie"].items()):
        P("  %-22s centro-centro %12.6f   insieme-insieme %12.6f   stessa componente %s"
          % (nome, v["centro_centro"], v["insieme_insieme"], v["stessa_componente"]))
        if not v["stessa_componente"]:
            P("      ** COMPONENTI DIVERSE: la distanza e' `inf`, e lo dico invece di stamparla **")
    if ctrl is not None:
        P("  controlli nel vuoto: candidati oltre %.6f dalle masse = %d"
          % (ctrl.get("metro_lontananza", float("nan")), ctrl.get("candidati_lontani", 0)))
        if ctrl.get("nota"):
            P("      nota: %s" % ctrl["nota"])
        for nome, v in sorted((ctrl.get("coppie") or {}).items()):
            P("      %-20s controllo %12.6f   bersaglio %12.6f   scarto %6.2f %%   entro %d %% %s"
              % (nome, v["distanza"], v["bersaglio"], 100.0 * v["scarto_relativo"],
                 int(100 * ctrl["toll"]), "SI" if v["entro_toll"] else "NO"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--collaudo" in a:
        sys.exit(collaudo())
    semi = None
    if "--semi" in a:
        semi = [int(x) for x in a[a.index("--semi") + 1].split(",")]
    sep = a[a.index("--sep") + 1] if "--sep" in a else None
    print("=" * 96)
    print("`OSSERVABILE-P1` -- la distanza fra le masse LUNGO IL GRAFO, pesi `d`")
    print("=" * 96)
    if "--snap" in a:
        net, coorti, rr = da_snapshot(a[a.index("--snap") + 1])
        o = misura(net, coorti)
        stampa(o, controlli(o, coorti, rr))
        sys.exit(0)
    if "--scena" not in a:
        print(__doc__)
        sys.exit(0)
    import _cli_flag
    risultati = {}
    fuori_json = {"semi": {}, "sep": None}
    dichiarata = False
    for s in (semi or [None]):
        S, coorti, rr, argv = da_scena(seme=s, sep=sep)
        print("")
        print("  --- seme %s   sep usato %.6f   n %d"
              % (s if s is not None else "(default 42)", S._NMASSE_VIDEO["sep"], S.net.n))
        o = misura(S.net, coorti)
        c = controlli(o, coorti, rr)      # UNA VOLTA per braccio: costa, ed e' uguale
        stampa(o, c)
        for nome, v in o["coppie"].items():
            risultati.setdefault(nome, []).append(v["centro_centro"])
        fuori_json["sep"] = float(S._NMASSE_VIDEO["sep"])
        fuori_json["semi"][str(s)] = {
            "n": int(S.net.n), "archi": int(len(S.net.d)),
            "r_regione": float(rr), "centri": dict(o["centri"]),
            "pari_medoide": dict(o["pari_medoide"]),
            "coppie": dict((k, dict(v)) for k, v in o["coppie"].items()),
            "controlli": dict((k, dict(v)) for k, v in
                              (c.get("coppie") or {}).items())}
        if not dichiarata:
            _cli_flag.dichiara_configurazione(S, print)   # `H-P5`: una volta, sempre
            dichiarata = True
    if semi and len(semi) >= 2:
        print("")
        print("  DISPERSIONE FRA SEMI (`P3`): %d semi" % len(semi))
        for nome, vals in sorted(risultati.items()):
            d = dispersione(vals)
            print("    %-22s media %12.6f   sd %10.6f   t(%d) %.3f   IC95 [%.6f, %.6f]"
                  % (nome, d["media"], d["sd"], d["gdl"], d["t"] or 0,
                     (d["ic95"] or (float('nan'),) * 2)[0], (d["ic95"] or (float('nan'),) * 2)[1]))
            if d.get("nota"):
                print("      nota: %s" % d["nota"])
            fuori_json.setdefault("dispersione", {})[nome] = d
    if "--json" in a:
        dest = a[a.index("--json") + 1]
        io.open(dest, "w", encoding="utf-8", newline=NL).write(
            json.dumps(fuori_json, indent=1, sort_keys=True, default=str) + NL)
        print(NL + "  scritto %s" % dest)
    sys.exit(0)
