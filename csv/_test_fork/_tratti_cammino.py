r"""**`TRATTI` — LA SCOMPOSIZIONE DEL CAMMINO**, e il suo collaudo `T7`/`T8` sul GRAFO.

*(Criteri committati **prima**, in `b3cf0ec`: `doc/TASK_HISTORY/2026-09-27_tratti.md` par.4.)*

> ### ⚠ **FILE NUOVO, DI PROPOSITO.** `csv/_osservabile_p1.py` e' **importato dai bracci del run in
> corso**, e `par.5` vieta di modificare un file che un processo ha importato. Qui si **importa**
> quel modulo *(leggerlo non lo tocca)* e si aggiunge **cio' che manca**, in un file che nessuno
> sta usando. **A run chiuso si decidera' se trasferirlo.**

**LA SCOMPOSIZIONE:** il cammino minimo `medoide_A -> medoide_B` e' una **sequenza di nodi**; ogni
**arco** del cammino va a un tratto **secondo l'appartenenza dei suoi due estremi**:

| tratto | regola |
|---|---|
| `interno_A` | **entrambi** gli estremi in `A` |
| `interno_B` | **entrambi** gli estremi in `B` |
| `varco` | **tutto il resto**, compresi gli archi di **CONFINE** *(un estremo dentro, uno fuori)* |

**Gli archi di confine vanno nel VARCO, ed e' una scelta DICHIARATA:** un arco che **esce** dalla
regione **non e' interno** a quella regione. **Si contano** (`T8c`): se pesassero quanto il varco,
la ripartizione sarebbe **una convenzione**, non una misura.

> ### 🎯 **PERCHE' QUESTO STRUMENTO ESISTE: `D_interni` E' UN INDICATORE, E PUO' SBAGLIARE.**
> `D_interni = D_centri - D_varco` usa `insieme_insieme`, **la distanza fra i due nodi PIU'
> VICINI** — che **non sta necessariamente sul cammino** `medoide -> medoide`.
> **`T7c` COSTRUISCE il caso in cui sbaglia, e MISURA di quanto.** Finora quel limite era
> **dichiarato**; qui e' **misurato**. *(Dichiarare un limite non e' misurarlo.)*

    python csv/_test_fork/_tratti_cammino.py --collaudo      # `T7`/`T8`: PRIMA dello strumento vero

ASCII puro.
"""
import os
import sys

import numpy as np
from scipy.sparse.csgraph import dijkstra

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: non costruisce nessuna scena e non carica il simulatore. Il `--collaudo` gira su
#   grafi SINTETICI a risposta nota; sugli stati veri legge `.npz` di un run che ha gia'
#   dichiarato la propria configurazione intera nel suo referto.

NL = chr(10)


# ============================================================================ IL CAMMINO
def cammino(g, a, b):
    """La SEQUENZA DI NODI del cammino minimo `a -> b`. `None` se non sono connessi."""
    d, pred = dijkstra(g, directed=False, indices=[int(a)], return_predecessors=True)
    if not np.isfinite(d[0, int(b)]):
        return None, float("inf")
    seq, k = [int(b)], int(b)
    while k != int(a):
        k = int(pred[0, k])
        if k < 0:
            return None, float("inf")
        seq.append(k)
    seq.reverse()
    return seq, float(d[0, int(b)])


def tratti(g, seq, A, B):
    """`interno_A / varco / interno_B` del cammino, e **la somma CHIUDE** (`T8`)."""
    sa = set(int(x) for x in A)
    sb = set(int(x) for x in B)
    fuori = {"interno_A": 0.0, "varco": 0.0, "interno_B": 0.0,
             "archi": 0, "confine": 0, "lung_confine": 0.0}
    for u, v in zip(seq[:-1], seq[1:]):
        w = float(g[u, v] if g[u, v] != 0 else g[v, u])
        fuori["archi"] += 1
        du, dv = (u in sa or u in sb), (v in sa or v in sb)
        if u in sa and v in sa:
            fuori["interno_A"] += w
        elif u in sb and v in sb:
            fuori["interno_B"] += w
        else:
            fuori["varco"] += w
            if du != dv:                       # CONFINE: un estremo dentro, uno fuori
                fuori["confine"] += 1
                fuori["lung_confine"] += w
    fuori["totale"] = fuori["interno_A"] + fuori["varco"] + fuori["interno_B"]
    return fuori


def scomponi(g, A, B):
    """`(tratti, L_tot, medoide_A, medoide_B)` -- **cogli STESSI `medoide()` dello strumento**."""
    ma, _pa, _ra = OP.medoide(g, A)
    mb, _pb, _rb = OP.medoide(g, B)
    seq, L = cammino(g, ma, mb)
    if seq is None:
        return None, float("inf"), ma, mb
    return tratti(g, seq, A, B), L, ma, mb


# ============================================================================ I GRAFI DEL COLLAUDO
def _grafo_sperone():
    """**`T7c`** — il grafo in cui **il nodo piu' vicino NON sta sul cammino**.

    ```
        p0 --(60)-- m0 --(100)-- m1 --(60)-- p1          A = {m0, p0}   B = {m1, p1}
         |                                     |
         +---------------(30)------------------+         <- lo SPERONE
    ```

    * **`centro_centro` = 100** *(la via diretta; quella per lo sperone costa `60+30+60 = 150`)*;
    * **`insieme_insieme` = 30** — **e sta sullo SPERONE, che il cammino NON usa.**

    **Accorciando SOLO lo sperone**, `D_varco` si muove e `D_centri` no: **l'indicatore inventa una
    variazione degli INTERNI che non esiste.** La scomposizione del cammino, che guarda la via
    diretta, **dice correttamente che non e' cambiato niente**.
    """
    def costruisci(w_sperone):
        i = np.array([0, 2, 0, 1], int)          # m0-p0, m1-p1, m0-m1, p0-p1
        j = np.array([1, 3, 2, 3], int)
        w = np.array([60.0, 60.0, 100.0, float(w_sperone)], float)
        g, _u, _s = OP.grafo(i, j, w, 4)
        return g
    A, B = np.array([0, 1], int), np.array([2, 3], int)
    return costruisci, A, B


def _anello_tagliato(peso_interno=1.0, peso_varco=1.0):
    """L'anello di `_osservabile_p1`, coi pesi separati **dentro le masse** e **nel varco**."""
    net, coorti = OP._anello()
    i, j = np.asarray(net.i, int), np.asarray(net.j, int)
    A = np.asarray(coorti["massa_0"], int)
    B = np.asarray(coorti["massa_1"], int)
    sa, sb = set(A.tolist()), set(B.tolist())
    w = np.full(len(i), 1.0)
    dentro = np.array([(u in sa and v in sa) or (u in sb and v in sb) for u, v in zip(i, j)])
    w[dentro] = peso_interno
    # il VARCO: gli archi fra le due masse, cioe' il segmento 19..200
    varco = np.array([(min(u, v) >= 19 and max(u, v) <= 200) and not d
                      for u, v, d in zip(i, j, dentro)])
    w[varco] = peso_varco
    g, _u, _s = OP.grafo(i, j, w, net.n)
    return g, A, B


# ============================================================================ IL COLLAUDO
def collaudo():
    """`T7a`/`T7b`/`T7c` + `T8`/`T8b`/`T8c`. **Ogni numero esce dal GRAFO**, nessuno e' costruito."""
    P = print
    P("=" * 108)
    P("`T7`/`T8` -- IL COLLAUDO SUL GRAFO (non l'aritmetica: `T4` era tautologico)")
    P("=" * 108)
    ok, tot = 0, 0

    def esito(nome, buono, testo):
        nonlocal ok, tot
        tot += 1
        ok += 1 if buono else 0
        P("  %-46s %s" % (nome, "PASS" if buono else "** FAIL **"))
        P("      %s" % testo)

    # ---------------------------------------------------------------- `T7a`
    g0, A, B = _anello_tagliato(1.0, 1.0)
    t0, L0, ma0, mb0 = scomponi(g0, A, B)
    c0 = float(dijkstra(g0, directed=False, indices=[ma0])[0, mb0])
    s0 = OP.fra_insiemi(g0, A, B)
    g1, _, _ = _anello_tagliato(1.0, 0.95)            # solo il VARCO si accorcia
    t1, L1, ma1, mb1 = scomponi(g1, A, B)
    c1 = float(dijkstra(g1, directed=False, indices=[ma1])[0, mb1])
    s1 = OP.fra_insiemi(g1, A, B)
    d_i = (c1 - c0) - (s1 - s0)
    esito("T7a  traslazione RIGIDA (solo il varco)", abs(d_i) < 1e-9,
          "D_centri %+.4f   D_varco %+.4f   D_interni %+.4f   (medoidi %d->%d, %d->%d)"
          % (c1 - c0, s1 - s0, d_i, ma0, ma1, mb0, mb1))

    # ---------------------------------------------------------------- `T7b`
    g2, _, _ = _anello_tagliato(0.95, 1.0)            # solo l'INTERNO si accorcia
    t2, L2, ma2, mb2 = scomponi(g2, A, B)
    c2 = float(dijkstra(g2, directed=False, indices=[ma2])[0, mb2])
    s2 = OP.fra_insiemi(g2, A, B)
    d_i2 = (c2 - c0) - (s2 - s0)
    esito("T7b  contrazione SOLO INTERNA", abs(s2 - s0) < 1e-9 and d_i2 < -1e-9,
          "D_centri %+.4f   D_varco %+.4f   D_interni %+.4f   -> tutto negli interni, come deve"
          % (c2 - c0, s2 - s0, d_i2))

    # ---------------------------------------------------------------- `T7c` e `T8b`
    costruisci, As, Bs = _grafo_sperone()
    ga, gb = costruisci(30.0), costruisci(20.0)
    ca = float(dijkstra(ga, directed=False, indices=[OP.medoide(ga, As)[0]])[0,
                                                                             OP.medoide(ga, Bs)[0]])
    cb = float(dijkstra(gb, directed=False, indices=[OP.medoide(gb, As)[0]])[0,
                                                                             OP.medoide(gb, Bs)[0]])
    sa_, sb_ = OP.fra_insiemi(ga, As, Bs), OP.fra_insiemi(gb, As, Bs)
    d_ic = (cb - ca) - (sb_ - sa_)
    esito("T7c  lo SPERONE: l'indicatore DEVE sbagliare", abs(d_ic) > 1e-9,
          "D_centri %+.4f (il cammino NON usa lo sperone)   D_varco %+.4f   "
          "D_interni %+.4f  <- INVENTATO" % (cb - ca, sb_ - sa_, d_ic))

    ta, La, _, _ = scomponi(ga, As, Bs)
    tb, Lb, _, _ = scomponi(gb, As, Bs)
    dif = max(abs(tb[k] - ta[k]) for k in ("interno_A", "varco", "interno_B"))
    esito("T8b  il CAMMINO da' la risposta GIUSTA", dif < 1e-9,
          "tratti prima  A %.2f  varco %.2f  B %.2f  (L %.2f)" % (
              ta["interno_A"], ta["varco"], ta["interno_B"], La) + NL +
          "      tratti dopo   A %.2f  varco %.2f  B %.2f  (L %.2f)   max|delta| %.2e"
          % (tb["interno_A"], tb["varco"], tb["interno_B"], Lb, dif))

    # ---------------------------------------------------------------- `T8` e `T8c`
    chiusure = [abs(t["totale"] - L) for t, L in ((t0, L0), (t1, L1), (t2, L2),
                                                  (ta, La), (tb, Lb))]
    esito("T8   la somma CHIUDE su tutti i casi", max(chiusure) < 1e-9,
          "max |interno_A + varco + interno_B - L_tot| = %.3e su %d casi"
          % (max(chiusure), len(chiusure)))
    esito("T8c  gli archi di CONFINE si CONTANO", True,
          "anello: %d archi di confine su %d, lunghezza %.2f su %.2f del varco"
          % (t0["confine"], t0["archi"], t0["lung_confine"], t0["varco"]) + NL +
          "      (se pesassero quanto il varco, la ripartizione sarebbe una CONVENZIONE)")

    P()
    P("  LA RIGA CHE CONTA E' `T7c`: costruisce il caso in cui l'indicatore SBAGLIA, e `T8b`")
    P("  mostra che la scomposizione del CAMMINO, sullo STESSO grafo, non sbaglia. Senza `T7c`")
    P("  il limite di `D_interni` resterebbe DICHIARATO invece che MISURATO.")
    P()
    P("  %d/%d" % (ok, tot))
    return ok, tot


if __name__ == "__main__":
    if "--collaudo" in sys.argv[1:]:
        n, t = collaudo()
        raise SystemExit(0 if n == t else 1)
    print(__doc__)
