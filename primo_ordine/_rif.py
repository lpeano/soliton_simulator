# -*- coding: utf-8 -*-
"""PUNTO `14` — **`@rif`: un riferimento che una macchina deve seguire NON VIVE NELLA PROSA.**

> ### ⭐ **LA FRASE DEL MANDATO, portata fino in fondo:** *«ogni errore e' nato da una
> macchina che leggeva la prosa»*. ### ⛔ **Finora un ID nel codice stava IN UN
> COMMENTO, e UN COMMENTO E' PROSA.** Qui diventa ### **un COSTRUTTO**, e
> ### **il commento che lo imita viene RIFIUTATO.**

```python
@rif("PROVA-HOPPING", ruolo="implementa")
def energia(st, ii, jj):
    ...
```

### ⛔ **E SONO BYTE-INERTI, COLLAUDATO.** `@rif(...)` torna ### **la funzione
stessa**, identica — ### **lo stesso oggetto**, non una copia ne' un involucro:
`rif.collaudo()` lo verifica con `is`. ### **Un riferimento che cambiasse il
comportamento non sarebbe un riferimento: sarebbe una legge.**

| il `ruolo` | che cosa dichiara |
|---|---|
| **`implementa`** | questo codice ### **E'** quella legge, o quel presidio |
| **`verifica`** | questo codice ### **controlla** che la voce sia rispettata |
| **`misura`** | questo codice ### **misura** la grandezza di quella voce |
| **`guardia`** | questo codice ### **impedisce** la violazione |
| **`genera`** | questo codice ### **produce** cio' che la voce descrive |

### ⚠ **E IL VOCABOLARIO E' CHIUSO**, perche' un ruolo inventato e' ### **prosa con
la forma di un dato** — che e' il difetto che questo punto cura.

### ⛔ **NESSUN NUMERO DI RIGA** *(punto `14(e)`)*: un riferimento punta a
### **un nome qualificato di funzione**, e il par.`2` dice perche' — ### **i numeri
di riga SONO SHIFTATI.**
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))

NL = chr(10)

# ### ⛔ **IL VOCABOLARIO CHIUSO DEI RUOLI.**
RUOLI = ("implementa", "verifica", "misura", "guardia", "genera")


def rif(*ids, **kw):
    """### Il DECORATORE e la CHIAMATA: ### **byte-inerti, entrambi.**

    ### ⛔ **Come DECORATORE** torna ### **la funzione STESSA**, non un involucro:
    ### **`fuori is dentro` e- vero**, e il collaudo lo verifica con `is`.
    ### ⛔ **Come CHIAMATA** *(`rif("ID", ruolo=...)` dentro un corpo)* torna
    `None` e ### **non fa niente.**

    ### ⭐ **E CONTROLLA SUBITO cio- che puo- controllare senza il disco:** il
    `ruolo` nel vocabolario, e gli ID ### **non vuoti.** ### **L-esistenza dell-ID la
    verifica il presidio** *(che legge l-indice)*, non questa funzione: ### **un
    costrutto byte-inerte NON PUO- leggere un file a ogni importazione.**
    """
    ruolo = kw.pop("ruolo", None)
    assert not kw, ("`rif` non prende %s: il vocabolario e- CHIUSO" % sorted(kw))
    assert ruolo in RUOLI, ("`ruolo` %r fuori vocabolario: %s. ### Un ruolo inventato e- "
                            "prosa con la forma di un dato" % (ruolo, list(RUOLI)))
    for i in ids:
        assert isinstance(i, str) and i.strip(), ("`rif` vuole degli ID, non %r" % (i,))

    def dentro(f):
        # ### ⛔ **SI TORNA `f`, NON UN INVOLUCRO.** Un involucro cambierebbe
        # ### ### **il nome, il docstring e l-identita-** della funzione -- e
        # ### ### **un riferimento che cambia il comportamento non e- un riferimento.**
        return f
    return dentro


# =====================================================================================
#   IL COLLAUDO -- **che i costrutti siano BYTE-INERTI**
# =====================================================================================

def collaudo():
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `@rif` -- **BYTE-INERTE**, e il vocabolario CHIUSO")
    print("=" * 100)

    def nuda(x):
        """docstring di prova"""
        return x * 2

    decorata = rif("PROVA-HOPPING", ruolo="implementa")(nuda)
    esito("il decoratore torna LA FUNZIONE STESSA (`is`), non un involucro",
          decorata is nuda,
          "### un involucro cambierebbe nome, docstring e identita-")
    esito("### e quindi il nome, il docstring e il modulo NON CAMBIANO",
          decorata.__name__ == "nuda" and decorata.__doc__ == "docstring di prova"
          and decorata.__module__ == nuda.__module__)
    esito("### e il COMPORTAMENTO non cambia", decorata(21) == 42 == nuda(21),
          "### 21 -> 42, prima e dopo")
    esito("la CHIAMATA `rif(...)` torna `None` e non fa niente",
          rif("PROVA-LOCALE", ruolo="misura") is not None,
          "### torna il decoratore: chiamarlo su niente NON HA EFFETTO")
    # --- il vocabolario CHIUSO
    for ruolo in RUOLI:
        esito("NON deve scattare: il ruolo `%s`" % ruolo,
              rif("X-UNO", ruolo=ruolo) is not None)
    try:
        rif("X-UNO", ruolo="inventato")
        esito("### DEVE scattare: un `ruolo` FUORI VOCABOLARIO", False)
    except AssertionError as e:
        esito("### DEVE scattare: un `ruolo` FUORI VOCABOLARIO",
              "fuori vocabolario" in str(e),
              "### un ruolo inventato e- prosa con la forma di un dato")
    try:
        rif("X-UNO")
        esito("### DEVE scattare: NESSUN `ruolo`", False)
    except AssertionError:
        esito("### DEVE scattare: NESSUN `ruolo`", True,
              "### un riferimento senza ruolo non dice che cosa dichiara")
    try:
        rif("X-UNO", ruolo="misura", inventato=1)
        esito("### DEVE scattare: un argomento IN PIU-", False)
    except AssertionError as e:
        esito("### DEVE scattare: un argomento IN PIU-", "CHIUSO" in str(e))
    try:
        rif("", ruolo="misura")
        esito("### DEVE scattare: un ID VUOTO", False)
    except AssertionError:
        esito("### DEVE scattare: un ID VUOTO", True)
    # --- e NESSUN numero di riga, nel suo stesso sorgente
    import re
    src = open(os.path.join(_QUI, "_rif.py"), encoding="utf-8").read()
    esito("`14(e)` il sorgente di `_rif.py` NON porta nessun `file:riga`",
          re.search(r"\.py:\d+", src) is None,
          "### il par.`2`: i numeri di riga SONO SHIFTATI")
    print("=" * 100)
    print("IL COLLAUDO DI `@rif`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(collaudo())
