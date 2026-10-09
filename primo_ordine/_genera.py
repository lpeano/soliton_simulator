# -*- coding: utf-8 -*-
"""IL GENERATORE — **dalla tabella al codice e alla scheda.**

> ### ⛔ **LA TABELLA E' L'UNICA FONTE.** Questo attrezzo legge
> `primo_ordine/leggi/leggi.yaml` e scrive ### **un modulo numerico per termine** in
> `primo_ordine/termini/` e ### **una scheda** in `doc/leggi_era2/`.
> ### **I file generati NON si modificano a mano**, e `P-E2` lo impedisce.

### **I QUATTRO PASSI, come il mandato li chiede**

| | |
|---|---|
| `(a)` | i simboli liberi dell'espressione sono ### **DENTRO l'ambito**, e ### **`pos` non esiste** *(`A17` per costruzione)*. ### **Un termine di nodo non vede i vicini** |
| `(b)` | ### **`dH/dpsi*` per differenziazione simbolica**, con `psi` e `psi*` ### **simboli INDIPENDENTI** *(derivata di Wirtinger)* |
| `(c)` | il ### **modulo numerico** *(`numpy` vettorizzato)* con in testa `LEGGE = "<id>"` e ### **l'IMPRONTA della riga di tabella** |
| `(d)` | la ### **scheda** `doc/leggi_era2/<id>.md` |

### ⭐ **COME `psi` DIVENTA SIMBOLI, e perché così:** una variabile
`complesso_c2_nodo` chiamata `psi` diventa ### **quattro simboli** — `psi_0`, `psi_1` e i
### **coniugati INDIPENDENTI** `psi_0c`, `psi_1c`. ### ⛔ **Indipendenti e non
`conjugate(psi_0)`:** la derivata che serve è ### **quella di Wirtinger**, e `sympy` su
`conjugate()` darebbe ### **zero o una forma inutilizzabile.**

### ⚠ **E I NOMI DEI SIMBOLI SONO I NOMI DELLE VARIABILI LOCALI DEL MODULO GENERATO**, di
proposito: così l'espressione stampata da `sympy` ### **è già il codice**, e non c'è
### **nessuna sostituzione testuale** fra la derivata e il file — ### **una sostituzione è
un posto dove la formula può cambiare senza che nessuno lo veda.**

Gira con:  python primo_ordine/_genera.py            # genera tutto
           python primo_ordine/_genera.py --prova    # il collaudo del generatore
"""
import hashlib
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import schema as SCH                                         # noqa: E402

NL = chr(10)
Q3 = chr(34) * 3
TABELLA = os.path.join(_QUI, "leggi", "leggi.yaml")
TERMINI = os.path.join(_QUI, "termini")
SCHEDE = os.path.join(RADICE, "doc", "leggi_era2")


# =====================================================================================
#   I SIMBOLI -- e l'IMPRONTA
# =====================================================================================

def impronta(riga):
    """### L'IMPRONTA di una riga di tabella: `sha1` del `json` ### **a chiavi ordinate.**

    ### ⛔ **A chiavi ordinate perche- l-ordine di un dizionario NON E- UN DATO:** se
    l-impronta dipendesse dall-ordine, ### **riordinare lo yaml rifiuterebbe ogni file** --
    e il presidio accuserebbe ### **una modifica che non c-e- stata.**
    """
    return hashlib.sha1(json.dumps(riga, sort_keys=True, ensure_ascii=False)
                        .encode("utf-8")).hexdigest()[:16]


def simboli_di(nome, tipo, lato=""):
    """### I nomi dei simboli di una variabile. ### **Sono anche i nomi delle locali.**

    `lato` e- `""` per un termine di nodo, `"i"`/`"j"` per i due capi di un arco.
    """
    s = nome + (("_" + lato) if lato else "")
    if tipo == "complesso_c2_nodo":
        return [s + "_0", s + "_1", s + "_0c", s + "_1c"]
    if tipo == "coppia_coniugata":
        # ### ⚠ **AMMESSA E NON USATA** *(decisione `13`, aperta)*: i simboli esistono, e
        # ### ### **nessuna legge li nomina.**
        return [s + "_q", s + "_p"]
    return [s]


def coniugati_di(nome, tipo, lato=""):
    """### I soli simboli ### **CONIUGATI**: sono quelli ### **rispetto a cui si deriva.**"""
    if tipo != "complesso_c2_nodo":
        return []
    s = nome + (("_" + lato) if lato else "")
    return [s + "_0c", s + "_1c"]


def ambiente(legge, variabili):
    """### `(simboli, coniugati)`: i nomi che l-espressione di questa legge puo- usare.

    ### ⛔ **Un `termine_nodo` NON ha il lato `i`/`j`**, e questo e- il secondo presidio
    contro ### **<<un termine di nodo che vede i vicini>>**: il primo e- l-ambito nello
    schema, il secondo e- che ### **i simboli dei vicini NON ESISTONO** nell-ambiente.
    """
    sim, con = [], []
    lati = ("i", "j") if legge["tipo"] == "termine_arco" else ("",)
    for v in legge["ambito"]:
        t = variabili[v]
        for lato in lati:
            if t == "reale_arco" or t == "fase_arco":
                # ### una variabile d-ARCO non ha due capi: e- dell-arco.
                if lato in ("", "i"):
                    sim += simboli_di(v, t)
            else:
                sim += simboli_di(v, t, lato)
                con += coniugati_di(v, t, lato)
    for k in (legge.get("parametri") or {}):
        sim.append(k)
    return (sorted(set(sim)), sorted(set(con)))


# =====================================================================================
#   (a) IL CONTROLLO, (b) LA DERIVATA
# =====================================================================================

def controlla(legge, variabili):
    """### `(a)`: i simboli liberi ### **dentro l-ambiente**, e ### **`pos` mai.**"""
    import sympy
    fuori = []
    idv = legge["id"]
    viet = SCH.simboli_vietati(legge["espressione"])
    if viet:
        fuori.append("`%s`: l-espressione nomina %s, ### VIETATO (`A17`: una posizione non "
                     "entra nella fisica, e la decisione 9 e- APERTA)" % (idv, viet))
    sim, _con = ambiente(legge, variabili)
    try:
        e = sympy.sympify(legge["espressione"], locals={k: sympy.Symbol(k) for k in sim})
    except Exception as exc:
        fuori.append("`%s`: l-espressione non si legge: %s" % (idv, exc))
        return fuori, None
    liberi = sorted(str(x) for x in e.free_symbols)
    extra = [x for x in liberi if x not in sim]
    if extra:
        fuori.append("`%s`: i simboli %s sono FUORI DALL-AMBITO (ammessi: %s). "
                     "### Un termine di nodo NON VEDE I VICINI, e i simboli dei vicini "
                     "NON ESISTONO nel suo ambiente" % (idv, extra, sim))
    return fuori, e


def derivata(e, coniugati):
    """### `(b)`: `dH/dpsi*` per ogni coniugato. ### **Wirtinger, e per questo i coniugati
    sono simboli INDIPENDENTI.**"""
    import sympy
    return {c: sympy.simplify(sympy.diff(e, sympy.Symbol(c))) for c in coniugati}


# =====================================================================================
#   (c) IL MODULO NUMERICO
# =====================================================================================

def _npy(e):
    """L-espressione in sintassi `numpy`. ### **I nomi sono quelli delle locali.**"""
    from sympy.printing.numpy import NumPyPrinter
    return NumPyPrinter({"fully_qualified_modules": False}).doprint(e)


def _locali(legge, variabili):
    """Le righe che legano i ### **simboli** alle ### **fette degli array.**"""
    fuori = []
    arco = legge["tipo"] == "termine_arco"
    for v in legge["ambito"]:
        t = variabili[v]
        if t == "complesso_c2_nodo":
            for lato in (("i", "j") if arco else ("",)):
                s = v + (("_" + lato) if lato else "")
                sorg = ("st[%r][%s]" % (v, {"i": "ii", "j": "jj"}[lato])) if lato \
                    else "st[%r]" % v
                fuori += ["    %s_0 = %s[:, 0]" % (s, sorg),
                          "    %s_1 = %s[:, 1]" % (s, sorg),
                          "    %s_0c = np.conj(%s_0)" % (s, s),
                          "    %s_1c = np.conj(%s_1)" % (s, s)]
        elif t in ("reale_arco", "fase_arco"):
            fuori.append("    %s = st[%r]" % (v, v))
        else:
            fuori.append("    %s = st[%r]" % (v, v))
    for k, d in (legge.get("parametri") or {}).items():
        fuori.append("    %s = PARAMETRI[%r]" % (k, k))
    return fuori


def modulo(legge, variabili, e, grad, imp):
    """### `(c)`: il modulo numerico, ### **con `LEGGE` e l-IMPRONTA in testa.**"""
    idv = legge["id"]
    arco = legge["tipo"] == "termine_arco"
    L = ["# -*- coding: utf-8 -*-",
         Q3 + "GENERATO da `primo_ordine/leggi/leggi.yaml` — "
         "### **NON si modifica a mano.**",
         "",
         "### ⛔ **`P-E2` confronta l-IMPRONTA qui sotto con la riga di tabella e "
         "RIFIUTA il commit** se non corrispondono. ### **Per cambiare questo file si "
         "cambia LA TABELLA e si rigenera.**",
         "",
         "### **La scheda:** `doc/leggi_era2/%s.md`." % idv,
         Q3,
         "import numpy as np",
         "",
         "# ### L-ID DELLA LEGGE: `P-E1` lo legge ### **via AST**, non per regex.",
         "LEGGE = %r" % idv,
         "# ### L-IMPRONTA della riga di tabella *(`sha1` del `json` a chiavi ordinate)*.",
         "IMPRONTA = %r" % imp,
         "TIPO = %r" % legge["tipo"],
         "AMBITO = %r" % (tuple(legge["ambito"]),),
         "PROVA = %r" % bool(legge["prova"]),
         "PARAMETRI = %r" % {k: d["valore"]
                             for k, d in (legge.get("parametri") or {}).items()},
         "",
         ""]
    # ------------------------------------------------------------------ l'energia
    L += ["def energia(st, ii=None, jj=None):",
          '    """### Il contributo di questa legge a `H`. ### **Reale.**"""']
    L += _locali(legge, variabili)
    L += ["    _e = %s" % _npy(e),
          "    return float(np.real(np.sum(_e)))",
          "",
          ""]
    # ------------------------------------------------------------------ il gradiente
    L += ["def gradiente(st, fuori, ii=None, jj=None):",
          '    """### `dH/dpsi*`, ### **accumulato in `fuori`**.',
          "",
          "    ### ⚠ **Si ACCUMULA** *(`+=`)*: `hamiltoniana.py` somma i termini",
          "    ### **in un solo posto**, e un termine che SCRIVESSE invece di accumulare",
          "    ### **cancellerebbe i termini prima di lui.**",
          '    """']
    L += _locali(legge, variabili)
    for c, g in sorted(grad.items()):
        # ### il nome del coniugato dice ### **la variabile, il lato e la componente.**
        m = re.match(r"^(.+?)(?:_(i|j))?_([01])c$", c)
        assert m, c
        nome, lato, comp = m.group(1), m.group(2), int(m.group(3))
        if arco and lato:
            L += ["    _g = %s" % _npy(g),
                  "    np.add.at(fuori[%r][:, %d], %s, _g * np.ones_like(%s_%s_%dc))"
                  % (nome, comp, {"i": "ii", "j": "jj"}[lato], nome, lato, comp)]
        else:
            L += ["    fuori[%r][:, %d] += %s" % (nome, comp, _npy(g))]
    L += ["    return fuori", ""]
    return NL.join(L) + NL


# =====================================================================================
#   (d) LA SCHEDA
# =====================================================================================

def scheda(legge, e, grad, imp):
    idv = legge["id"]
    L = ["# `%s`%s" % (idv, "  — ### ⚠ **PROVA: NON E' FISICA DECISA**"
                       if legge["prova"] else ""),
         "",
         "> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` "
         "*(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**",
         ""]
    if legge["prova"]:
        L += ["> ### ⚠ **E LA LEGGE E' DICHIARATA `prova: true`:** serve a "
              "### **collaudare la catena**, non a dire come va il mondo. "
              "### **Nessuna fisica e' decisa qui.**", ""]
    L += ["| | |", "|---|---|",
          "| **tipo** | `%s` |" % legge["tipo"],
          "| **espressione** | `%s` |" % legge["espressione"],
          "| **ambito** | %s |" % " · ".join("`%s`" % x for x in legge["ambito"]),
          "| **impronta della riga** | `%s` |" % imp,
          "| **assiomi soddisfatti** | %s |"
          % (" · ".join("`%s`" % x for x in legge["assiomi"])
             if legge["assiomi"] else "### ⚠ **nessuno dichiarato**"),
          ""]
    if legge.get("parametri"):
        L += ["## I PARAMETRI", "",
              "> ### ⛔ **`A1`: LA LEGGE, NON IL NUMERO.** Ogni parametro porta "
              "### **il valore E l'origine** — e un numero senza origine e' "
              "### **una manopola.**", "",
              "| | valore | origine |", "|---|--:|---|"]
        for k, d in sorted(legge["parametri"].items()):
            L += ["| `%s` | `%s` | %s |" % (k, d["valore"], d["origine"])]
        L += [""]
    L += ["## LA DERIVATA, GENERATA", "",
          "> ### ⭐ **`dH/dpsi*` per differenziazione simbolica**, con `psi` e `psi*` "
          "### **simboli INDIPENDENTI** *(Wirtinger)*. ### **Non e' scritta a mano in "
          "nessun posto.**", "",
          "| rispetto a | `dH/d(...)` |", "|---|---|"]
    for c, g in sorted(grad.items()):
        L += ["| `%s` | `%s` |" % (c, g)]
    L += ["", "## LA SCHEDA, dalla tabella", "", str(legge["scheda"]).strip(), ""]
    return NL.join(L) + NL


# =====================================================================================
#   IL GIRO
# =====================================================================================

def carica():
    import yaml
    d = yaml.safe_load(io.open(TABELLA, encoding="utf-8").read()) or {}
    leggi = d.get("leggi") or []
    varia = d.get("variabili") or []
    return leggi, varia


def genera(verboso=True):
    leggi, varia = carica()
    err = []
    for v in varia:
        err += SCH.valida_variabile(v)
    vocab = {v["nome"]: v["tipo"] for v in varia}
    for lg in leggi:
        err += SCH.valida_legge(lg, vocab)
    assert not err, ("### LA TABELLA NON PASSA LO SCHEMA, e NON SI GENERA NIENTE:" + NL
                     + NL.join(err[:12]))
    os.makedirs(SCHEDE, exist_ok=True)
    fatti = []
    for lg in leggi:
        if lg["tipo"] not in ("termine_nodo", "termine_arco"):
            continue
        guai, e = controlla(lg, vocab)
        assert not guai, ("### IL CONTROLLO (a) RIFIUTA LA LEGGE, e NON SI GENERA:" + NL
                          + NL.join(guai))
        _sim, con = ambiente(lg, vocab)
        grad = derivata(e, con)
        imp = impronta(lg)
        p1 = os.path.join(TERMINI, lg["id"].lower().replace("-", "_") + ".py")
        io.open(p1, "w", encoding="utf-8", newline=NL).write(
            modulo(lg, vocab, e, grad, imp))
        p2 = os.path.join(SCHEDE, lg["id"] + ".md")
        io.open(p2, "w", encoding="utf-8", newline=NL).write(scheda(lg, e, grad, imp))
        fatti.append((lg["id"], p1, p2, imp, len(grad)))
        if verboso:
            print("   %-18s %s" % (lg["id"], os.path.relpath(p1, RADICE)))
            print("   %-18s %s   impronta %s, %d derivate"
                  % ("", os.path.relpath(p2, RADICE), imp, len(grad)))
    return fatti


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--prova" in argv:
        return collaudo()
    fatti = genera()
    print("  generati: %d termini" % len(fatti))
    return 0


# =====================================================================================
#   IL COLLAUDO DEL GENERATORE -- i casi che DEVONO fallire
# =====================================================================================

def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    VOC = {"psi": "complesso_c2_nodo", "w": "reale_arco"}

    def lg(**kw):
        d = {"id": "PROVA-X", "tipo": "termine_nodo",
             "espressione": "psi_0c*psi_0 + psi_1c*psi_1",
             "ambito": ["psi"], "parametri": {}, "assiomi": [], "prova": True,
             "scheda": "s"}
        d.update(kw)
        return d

    print("=" * 100)
    print("IL COLLAUDO DEL GENERATORE -- e i casi che DEVONO fallire")
    print("=" * 100)
    g, e = controlla(lg(), VOC)
    esito("il caso SANO: i simboli sono dentro l-ambiente", g == [] and e is not None)
    # ### ⛔ **UN TERMINE DI NODO CHE LEGGE UN VICINO.**
    g, _e = controlla(lg(espressione="psi_i_0c*psi_j_0"), VOC)
    esito("### DEVE rifiutare: un `termine_nodo` che nomina `psi_i`/`psi_j` (il VICINO)",
          any("NON VEDE I VICINI" in x for x in g),
          "i simboli dei vicini NON ESISTONO nell-ambiente di un termine di nodo")
    esito("NON deve rifiutare: lo STESSO con `tipo: termine_arco`",
          controlla(lg(tipo="termine_arco",
                       espressione="psi_i_0c*psi_j_0"), VOC)[0] == [])
    # ### ⛔ **`pos` NELL-ESPRESSIONE.**
    g, _e = controlla(lg(espressione="psi_0c*psi_0 + pos_x"), VOC)
    esito("### DEVE rifiutare: un-espressione che nomina `pos_x` (`A17`)",
          any("VIETATO" in x for x in g))
    # ### ⛔ **UN SIMBOLO FUORI DALL-AMBITO.**
    g, _e = controlla(lg(espressione="psi_0c*psi_0 + w"), VOC)
    esito("### DEVE rifiutare: un simbolo FUORI dall-ambito (`w` non e- dichiarato)",
          any("FUORI DALL-AMBITO" in x for x in g))
    # ### ⭐ **LA DERIVATA: Wirtinger, e si verifica a MANO su un caso noto.**
    import sympy
    _g, e = controlla(lg(), VOC)
    d = derivata(e, ["psi_0c", "psi_1c"])
    esito("la derivata di `psi_0c*psi_0 + psi_1c*psi_1` rispetto a `psi_0c` e- `psi_0`",
          d["psi_0c"] == sympy.Symbol("psi_0"),
          "Wirtinger: `psi` e `psi*` sono simboli INDIPENDENTI")
    _g, e2 = controlla(lg(espressione="(psi_0c*psi_0 + psi_1c*psi_1)**2"), VOC)
    d2 = derivata(e2, ["psi_0c"])
    atteso = 2 * sympy.Symbol("psi_0") * (sympy.Symbol("psi_0c") * sympy.Symbol("psi_0")
                                          + sympy.Symbol("psi_1c") * sympy.Symbol("psi_1"))
    esito("e la derivata del QUADRATO e- `2*psi_0*(psi_0c*psi_0 + psi_1c*psi_1)`",
          sympy.simplify(d2["psi_0c"] - atteso) == 0)
    # ### ⛔ **L-IMPRONTA non dipende dall-ORDINE delle chiavi.**
    a = dict(lg())
    b = {k: a[k] for k in reversed(list(a))}
    esito("l-impronta NON dipende dall-ordine delle chiavi",
          impronta(a) == impronta(b),
          "riordinare lo yaml NON deve rifiutare ogni file")
    c = dict(a, espressione=a["espressione"] + " + 0")
    esito("### e CAMBIA se l-espressione cambia", impronta(a) != impronta(c))
    print("=" * 100)
    print("IL COLLAUDO DEL GENERATORE: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
