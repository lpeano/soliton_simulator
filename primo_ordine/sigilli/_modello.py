# -*- coding: utf-8 -*-
"""PUNTI `7` e `12(c)` — **IL MODELLO DI UN SIGILLO DELL'ERA `2`.**

> ### ⛔ **Il punto `7`:** *«il MODELLO DI SIGILLO DI UNA LEGGE, col rito adattato:
> **coefficiente zero = byte-identico**, riduzione al limite, controllo positivo, caso che
> deve fallire, **un processo per braccio**, firme dei byte, stesso istante, giro corto
> prima»*.
> ### ⛔ **Il punto `12(c)`:** *«ogni sigillo dichiara `LEGGE` e `CRITERI`»*.

### ⭐ **E IL RITO ADATTATO NON E' IL RITO TRADOTTO: UNA COSA CAMBIA, e e' la piu'
importante.** Nell'era `1` il *«prima»* era ### **una COPIA del simulatore patchata a
mano** — `13k` righe, estratte dal padre del commit. ### ✅ **Nell'era `2` il
*«prima»* si OTTIENE METTENDO A ZERO IL COEFFICIENTE NELLA TABELLA e RIGENERANDO:** non
c'e' nessuna copia da costruire, nessuna patch da applicare, ### **e il braccio zero e'
BYTE-IDENTICO per costruzione, non per fortuna.**

| il braccio | che cosa prova | perche' SENZA di lui il sigillo non vale |
|---|---|---|
| **`zero`** | il coefficiente a `0` da' uno stato ### **BYTE-IDENTICO** a quello senza la legge | se non lo fosse, ### **la legge agisce anche quando e' spenta**: un confronto fra <<con>> e <<senza>> ### **non misura lei** |
| **`limite`** | la legge ### **si riduce a una forma nota** in un limite *(un grafo di due nodi, un coefficiente piccolo)* | una legge che non ha ### **nessun limite riconoscibile** puo' essere qualunque cosa |
| **`positivo`** | la grandezza che si misura ### **PUO' cambiare** | ### ⛔ **e' il braccio che impedisce un `FALSO-ZERO`**: uno zero garantito dall'insieme scelto |
| **`deve-fallire`** | un caso in cui il criterio ### **DEVE** dire no | ### **il piu' importante** *(`P1-sexies`)*: senza, il criterio ### **non distingue niente** |

### ⛔ **E I CRITERI SI FISSANO PRIMA, nel `CRITERI` del modulo:** letti ### **via
AST** da `P-SIG`, che ### **rifiuta un sigillo senza `LEGGE` o senza `CRITERI`.**

### ⚠ **UN PROCESSO PER BRACCIO, e nell'era `2` costa meno:** un braccio e'
### **una configurazione** piu' ### **una tabella**, e le due cose sono ### **due file** —
quindi un braccio ### **non ha bisogno di una copia del codice**, solo di
### **un'impronta diversa.** ### **E l'impronta la scrive il TIMBRO.**
"""
import hashlib
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
PO = os.path.dirname(_QUI)
RADICE = os.path.dirname(PO)
for _p in (PO, os.path.join(PO, "config"), os.path.join(PO, "leggi"),
           os.path.join(RADICE, "csv")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                           # noqa: E402

import hamiltoniana as HAM                                   # noqa: E402
import passo as PA                                           # noqa: E402
import stato as ST                                           # noqa: E402
import timbro as TB                                          # noqa: E402

NL = chr(10)

# ### ⛔ **IL PUNTO `12(c)`: `LEGGE` e `CRITERI`, letti VIA AST.**
LEGGE = "PROVA-LOCALE"

# ### ⛔ **I CRITERI, FISSATI PRIMA.** `nome -> (che cosa, la lettura)`
CRITERI = {
    "zero": ("il coefficiente `g = 0` da- uno stato BYTE-IDENTICO a quello senza la "
             "legge", "uguaglianza AL BYTE, non entro una tolleranza"),
    "limite": ("con `g` piccolo l-energia della legge tende a `0` come `g`",
               "il rapporto energia/g resta costante entro il 1 per mille"),
    "positivo": ("con `g = 0.5` l-energia della legge NON e- zero",
                 "> 1e-6 in valore assoluto"),
    "deve-fallire": ("il braccio `zero` DEVE fallire se si confronta uno stato con `g` "
                     "DIVERSO da zero", "i byte DEVONO differire"),
}


def _byte(st):
    return tuple((k, st[k].tobytes()) for k in sorted(st))


def _termini(g):
    """I termini con il coefficiente `g` ### **messo a mano nel modulo caricato.**

    ### ⚠ **E QUESTA E- L-UNICA COSA CHE SI TOCCA A MANO, e la dichiaro:** il rito
    vero mette `g` ### **NELLA TABELLA** e ### **rigenera**, e il braccio zero e- allora
    ### **byte-identico per costruzione.** ### ⛔ **Qui si scrive `PARAMETRI['g']`
    sul modulo gia- caricato**, che e- ### **la stessa aritmetica** *(il modulo legge
    `PARAMETRI[k]` a ogni chiamata)* ma ### **non passa dal generatore** -- quindi
    ### **non prova che la TABELLA sia la fonte.**
    ### ✅ **Il braccio che quello lo prova e- `P-E2`**, che confronta l-impronta del
    generato con la riga di tabella: ### **e- cablato, e gira a ogni commit.**
    """
    T = HAM.carica_termini()
    for m in T:
        if m.LEGGE == LEGGE:
            m.PARAMETRI["g"] = g
    return T


def _corsa(g, n, dt, passi, seme, iterazioni, toll, senza=False):
    """Una corsa: ### **un braccio.** `senza=True` ### **toglie la legge.**"""
    T = _termini(g)
    if senza:
        T = [m for m in T if m.LEGGE != LEGGE]
    ii = np.arange(n - 1, dtype=int)
    jj = np.arange(1, n, dtype=int)
    ss = PA.strati(ii, jj)
    st = ST.nuovo(n)
    rng = np.random.default_rng(seme)
    for k in st:
        st[k][...] = (rng.normal(size=st[k].shape)
                      + 1j * rng.normal(size=st[k].shape))
    e0 = HAM.energia(st, ii, jj, T)
    for _ in range(passi):
        st = PA.passo_locale(st, ii, jj, dt, T, iterazioni, toll, ss)[0]
    return st, e0, HAM.energia(st, ii, jj, T)


def energia_della_legge(g, n, seme):
    """Il contributo ### **della sola legge** a `H`, sullo stato iniziale."""
    T = _termini(g)
    mio = [m for m in T if m.LEGGE == LEGGE]
    ii = np.arange(n - 1, dtype=int)
    jj = np.arange(1, n, dtype=int)
    st = ST.nuovo(n)
    rng = np.random.default_rng(seme)
    for k in st:
        st[k][...] = (rng.normal(size=st[k].shape)
                      + 1j * rng.normal(size=st[k].shape))
    return HAM.energia(st, ii, jj, mio)


def sigillo(n=7, dt=0.01, passi=30, seme=11, iterazioni=64, toll=1e-14):
    """### Il sigillo: ### **i quattro bracci, e il verdetto.**"""
    ok = [0, 0]
    righe = []

    def esito(nome, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        righe.append((nome, passa, nota))
        print("  %-30s %s   %s" % (nome, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL SIGILLO DI `%s` -- il MODELLO dell-era 2 (punto 7)" % LEGGE)
    print("=" * 100)
    for k, (che, lett) in sorted(CRITERI.items()):
        print("  CRITERIO `%-14s` %s" % (k, che))
        print("  %-17s  la lettura: %s" % ("", lett))
    print()
    # ------------------------------------------------------------------ `zero`
    a, _e0a, _e1a = _corsa(0.0, n, dt, passi, seme, iterazioni, toll)
    b, _e0b, _e1b = _corsa(0.5, n, dt, passi, seme, iterazioni, toll, senza=True)
    esito("zero = byte-identico", _byte(a) == _byte(b),
          "### il coefficiente a `0` e la legge TOLTA danno gli STESSI BYTE")
    # ------------------------------------------------------------------ `deve-fallire`
    c, _e0c, _e1c = _corsa(0.5, n, dt, passi, seme, iterazioni, toll)
    esito("### DEVE fallire: `g` != 0", _byte(a) != _byte(c),
          "### senza questo braccio il primo non distinguerebbe NIENTE (`P1-sexies`)")
    # ------------------------------------------------------------------ `positivo`
    ep = energia_della_legge(0.5, n, seme)
    esito("positivo: l-energia della legge NON e- zero", abs(ep) > 1e-6,
          "`%.6f`: ### la grandezza PUO- cambiare, quindi lo zero di sopra non e- un "
          "FALSO-ZERO" % ep)
    # ------------------------------------------------------------------ `limite`
    rap = []
    for g in (1e-3, 1e-4, 1e-5):
        rap.append(energia_della_legge(g, n, seme) / g)
    sp = (max(rap) - min(rap)) / abs(sum(rap) / len(rap))
    esito("limite: l-energia tende a zero COME `g`", sp < 1e-3,
          "il rapporto energia/g varia di `%.2e` su tre decadi: ### la legge e- LINEARE "
          "in `g`, come la sua forma dice" % sp)
    # ------------------------------------------------------------------ e il TIMBRO
    import schema_config as CFG
    cfg = CFG.carica(os.path.join(PO, "config", "prova.yaml"))
    t = TB.timbro(cfg, CFG.impronta(cfg))
    print()
    for r in TB.righe_timbro(t):
        print("  " + r)
    print("  #   firma A    %s" % hashlib.sha1(
        b"".join(x[1] for x in _byte(a))).hexdigest()[:16])
    print("  #   firma C    %s" % hashlib.sha1(
        b"".join(x[1] for x in _byte(c))).hexdigest()[:16])
    print()
    print("=" * 100)
    print("IL SIGILLO DI `%s`: %d su %d   %s"
          % (LEGGE, ok[0], ok[1],
             "### SIGILLATA" if ok[0] == ok[1] else "### NON SIGILLATA: NON SI COMMITTA"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    del argv
    return sigillo()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
