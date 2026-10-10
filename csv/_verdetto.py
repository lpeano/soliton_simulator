# -*- coding: utf-8 -*-
"""IL VERDETTO DI UN COLLAUDO IN UN REFERTO — **✅ SOLO se `N` su `N`.**

> ### ⛔ **Il difetto, trovato dal guardiano il `2026-10-10`:** rigenerato su un
> fallimento, `doc/REFERTO_seconda_parte_era2.md` scriveva ### **«✅ `20`/`22`»**.
> ### **Un referto che marca VERDE un fallimento è un FALSO-UNO**, e peggio di un referto
> che non dice niente: ### **chi lo legge non ha motivo di guardare l'uscita vera.**

### 📌 **E LA FORMA SBAGLIATA ERA LA STESSA IN DUE GENERATORI**, con lo stesso codice
copiato: `### ✅ **N/M**` scritto ### **senza guardare se `N == M`.**

### ⭐ **E GLI ALTRI QUATTRO AVEVANO UN DIFETTO PIU' SILENZIOSO: scrivevano `12/13`
NUDO.** ### ⚠ **Un numero senza verdetto non è neutro: è illeggibile.** ### **Chi scorre
una tabella di `17` righe non confronta `17` coppie di numeri — cerca il simbolo.**

### ✅ **QUINDI UNA FUNZIONE SOLA, e tutti la chiamano:** ### **✅ solo se `N == N`**,
### **⛔ col numero** altrimenti, e ### **⛔ anche quando il numero NON SI LEGGE** — perché
un collaudo di cui non si è potuto leggere l'esito ### **non è un collaudo passato.**
"""
import sys

__all__ = ("verdetto", "VERDE", "ROSSO")

# ### ⛔ **E QUI NON C-E- UN `PRESIDIO = ...`, e me lo ha detto `P-C1`:**
# ### l-avevo scritto, e il presidio ha risposto che ### **la voce ha**
# ### ### **`classe: DIFETTO`**, non `PRESIDIO`. ### ⭐ **E ha ragione per la
# ### ragione giusta: questo modulo NON IMPEDISCE NIENTE -- FORMATTA un verdetto.**
# ### ⚠ **Cio- che impedisce il difetto e- il collaudo dei generatori, non
# ### questa funzione:** chiamare <<presidio>> un formattatore vorrebbe dire
# ### ### **contare una barriera che non c-e-.**

VERDE = "✅"
ROSSO = "⛔"


def verdetto(a, b, rc=None):
    """### La cella di un referto per UN collaudo.

    * `a`, `b` — ### **passati** e ### **in tutto**, oppure `None` se non si leggono
    * `rc` — il codice d'uscita, ### **se c'è**

    ### ⛔ **✅ SOLO se `a == b` e `b > 0`** *(e `rc` nullo o zero)*. ### **In ogni altro
    caso ⛔, col numero se c'è.**
    """
    if a is not None and b:
        if a == b and (rc in (None, 0)):
            return "### %s **`%d`/`%d`**" % (VERDE, a, b)
        return "### %s **`%d`/`%d`**%s" % (
            ROSSO, a, b, (" *(codice `%d`)*" % rc) if rc not in (None, 0) else "")
    # ### ⚠ **NESSUN NUMERO: il verdetto viene dal CODICE D-USCITA, e se manca anche
    # ### quello e- ### **ROSSO** -- un collaudo di cui non si sa niente
    # ### ### **non e- un collaudo passato.**
    if rc == 0:
        return "### %s **passa** *(nessun numero da leggere)*" % VERDE
    if rc is None:
        return ("### %s **ESITO NON LETTO**: ne- un <<`N` su `M`>> ne- un codice "
                "d-uscita" % ROSSO)
    return "### %s **FALLISCE** *(codice `%d`)*" % (ROSSO, rc)


def totale(coppie):
    """### Il verdetto della SOMMA: ### **✅ solo se ogni collaudo e- pieno.**

    `coppie` e- una lista di `(a, b)`. ### ⛔ **Sommare `12`+`13` e `14`+`14` e
    scrivere `26`/`27` con un ✅ sarebbe lo stesso difetto un livello piu- in su:**
    ### **il totale e- verde SOLO se NESSUN addendo era rosso.**
    """
    a = sum(x for x, _y in coppie if x is not None)
    b = sum(y for _x, y in coppie if y)
    pieni = all(x == y and y for x, y in coppie)
    if pieni:
        return "### %s **`%d`/`%d`**" % (VERDE, a, b)
    rotti = [(x, y) for x, y in coppie if not (x == y and y)]
    return ("### %s **`%d`/`%d`** -- e %d collaudi NON sono pieni: %s"
            % (ROSSO, a, b, len(rotti),
               ", ".join("`%s`/`%s`" % (x, y) for x, y in rotti[:4])))


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-58s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEL VERDETTO -- nei DUE VERSI")
    print("=" * 100)
    esito("NON deve scattare: `13`/`13` e- VERDE", VERDE in verdetto(13, 13),
          "### un collaudo pieno e- l-unico caso verde")
    esito("### DEVE scattare: `20`/`22` NON e- verde",
          ROSSO in verdetto(20, 22) and VERDE not in verdetto(20, 22),
          "### e- IL DIFETTO che il guardiano ha trovato: "
          "`REFERTO_seconda_parte` scriveva <<✅ 20/22>>")
    esito("### e il numero RESTA nella cella rossa", "`20`/`22`" in verdetto(20, 22),
          "### ⛔ col NUMERO: <<FALLISCE>> senza il numero non dice QUANTO")
    esito("### DEVE scattare: `13`/`13` ma col CODICE D-USCITA non nullo",
          ROSSO in verdetto(13, 13, rc=1),
          "### un collaudo che conta 13 su 13 e poi ESCE 1 NON e- passato: il codice "
          "d-uscita e- l-ultima parola")
    esito("NON deve scattare: nessun numero ma codice `0`",
          VERDE in verdetto(None, None, rc=0),
          "### alcuni strumenti non stampano <<N su M>>: il codice d-uscita basta")
    esito("### DEVE scattare: NE- numero NE- codice",
          ROSSO in verdetto(None, None, rc=None) and "NON LETTO" in verdetto(None, None),
          "### un collaudo di cui non si sa niente NON e- un collaudo passato -- ed e- "
          "il caso che un referto rigenerato su un difetto produce")
    esito("### DEVE scattare: `0`/`0` NON e- verde",
          ROSSO in verdetto(0, 0),
          "### zero su zero e- UN COLLAUDO SENZA BRACCI: passerebbe per vacuita-")
    esito("NON deve scattare: un TOTALE di collaudi tutti pieni",
          VERDE in totale([(13, 13), (14, 14)]),
          "`27`/`27`")
    esito("### DEVE scattare: un TOTALE con un addendo ROTTO",
          ROSSO in totale([(12, 13), (14, 14)]),
          "### sommare `12`+`14` e scrivere `26`/`27` con un ✅ sarebbe LO STESSO "
          "DIFETTO un livello piu- in su")
    print("=" * 100)
    print("IL COLLAUDO DEL VERDETTO: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _presidio
    _presidio.avvia(__file__)
    sys.exit(collaudo())
