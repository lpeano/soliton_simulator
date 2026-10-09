# -*- coding: utf-8 -*-
"""DOVE VIVE LA FISICA — **due costanti, e una la decide Luca.**

> ### ⛔ **Finora ogni presidio scriveva `soliton_simulator.py` A MANO.** Erano `3`
> *(`csv/_hook_fisica.py`, `csv/_presidio_commenti_flag.py`, e il testo d'aiuto di
> `csv/_hook_presidi.py`)*, e ### **il giorno in cui la fisica vive in due file la metà dei
> presidi guarda ancora UN FILE SOLO** — senza dirlo, perché ### **un presidio che guarda il
> posto sbagliato PASSA.**

### 📌 **LA LISTA è l'unica fonte:** chi sorveglia la fisica ### **la legge da qui.**

### ⛔ **E LA CARTELLA DELL'ERA `2` È VUOTA, PERCHÉ IL NOME LO DECIDE LUCA.**
*«In `csv/_file_fisica.py` due costanti: la LISTA dei file di fisica (oggi
`soliton_simulator.py`) e la CARTELLA del codice dell'era `2`, che resta vuota con "da
decidere da Luca".»*

> ### ⚠ **E FINCHÉ È VUOTA, IL PRESIDIO SULLA CARTELLA NON IMPEDISCE NIENTE.** Per `A9`
> ### **quella non è un presidio: è una TENDA** — e lo scrivo qui invece di farlo scoprire
> a qualcuno. ### ✔ **Il codice c'è, il collaudo gira su una cartella di PROVA, e il giorno
> in cui Luca dà il nome il presidio diventa vero cambiando UNA STRINGA.**

Gira con:  python csv/_file_fisica.py            # che cosa sorveglia, e che cosa no
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)

NL = chr(10)

# =====================================================================================
#   LE DUE COSTANTI
# =====================================================================================

# ### **LA LISTA DEI FILE DI FISICA SORVEGLIATI.** Percorsi relativi alla radice del repo.
# ### ⚠ **Oggi e- UNO**, e il mandato lo dice: *<<oggi `soliton_simulator.py`>>*.
# ### ⛔ **Non si aggiunge un file qui per comodita-:** ### **cio- che sta in questa lista e-
# ### ### SOGGETTO A `H-REG-R`** -- nessuna legge cambia senza la sua scheda nel registro --
# ### e a `H-P7`, il commento di ogni flag. ### **Mettere un file qui gli mette addosso
# ### DUE presidi.**
FILE_FISICA = (
    "soliton_simulator.py",
)

# ### ✔ **LA CARTELLA DEL CODICE DELL-ERA `2`: `primo_ordine/`** -- ### **decisione di Luca
# ### del 2026-10-09.** ### ⭐ **E da questo momento `H-FISICA-FUORI-LISTA` IMPEDISCE:**
# ### finche- la costante era `""` era ### **una TENDA** *(`A9`)*, e l-avevo dichiarato in
# ### quattro posti. ### **Adesso un `.py` nuovo la- sotto che non e- nella LISTA fa
# ### RIFIUTARE il commit.**
# ### ⚠ **LA CARTELLA NON ESISTE ANCORA, e NON l-ho creata:** il mandato da- ### **il
# ### nome**, non l-ordine di crearla -- e creare la cartella del codice dell-era `2` e-
# ### ### **un atto di FISICA**, non di indice. ### ✔ **Il presidio funziona comunque,
# ### perche- guarda I PERCORSI STAGED e non il disco:** impedisce ### **dal primo `.py`
# ### che qualcuno metta la-.**
# ### ### **«da decidere da Luca»** -- e il mandato e- esplicito:
# ### *<<la cartella del codice dell-era 2 NON ESISTE e NON la scegli tu>>*.
# ### ⚠ **Finche- e- `""` il presidio sulla cartella NON GUARDA NIENTE**, ed e- dichiarato
# ### nel referto: per `A9` ### **non e- un presidio, e- una tenda.** ### ✔ **Il giorno in
# ### cui Luca da- il nome, diventa vero cambiando QUESTA STRINGA e nient-altro.**
CARTELLA_ERA_2 = "primo_ordine/"   # decisione di Luca, 2026-10-09


# =====================================================================================
#   CHI LEGGE
# =====================================================================================

def sorvegliati():
    """### I file di fisica, ### **come tupla di percorsi relativi.**"""
    return tuple(FILE_FISICA)


def e_di_fisica(percorso):
    """### `True` se quel percorso e- ### **un file di fisica sorvegliato.**

    ### ⚠ **Si confronta con le barre NORMALIZZATE:** git dice `a/b.py`, Windows dice
    `a\\b.py`, e ### **due forme dello stesso percorso non sono lo stesso percorso** per una
    `==`.
    """
    q = (percorso or "").replace(chr(92), "/").lstrip("./")
    return q in tuple(x.replace(chr(92), "/") for x in FILE_FISICA)


def sotto_la_cartella(percorso):
    """### `True` se quel percorso sta ### **sotto la cartella dell-era `2`.**

    ### ⛔ **Con la cartella vuota torna SEMPRE `False`**, e non e- un caso limite da
    aggirare: ### **e- lo stato dichiarato.** ### **Un presidio che non guarda niente
    non deve FINGERE di guardare.**
    """
    if not CARTELLA_ERA_2:
        return False
    base = CARTELLA_ERA_2.replace(chr(92), "/").rstrip("/") + "/"
    return (percorso or "").replace(chr(92), "/").lstrip("./").startswith(base)


def intrusi(percorsi):
    """### I `.py` ### **sotto la cartella dell-era `2` che NON sono nella LISTA.**

    ### ⭐ **Il presidio del punto `7`:** *<<un `.py` nuovo sotto la CARTELLA che non e-
    nella LISTA -> commit rifiutato>>*. ### **Il perche-: un file di fisica che nessuno
    sorveglia e- peggio di un file che non esiste**, perche- ### **sembra sorvegliato.**
    """
    return [p for p in (percorsi or ())
            if p.endswith(".py") and sotto_la_cartella(p) and not e_di_fisica(p)]


def main():
    # ### ⛔ **IL PRESIDIO ENCODING STA QUI, NON ALL-IMPORT, e la ragione e- precisa:**
    # ### questo modulo e- ### **importato dai hook** *(`H-REG-R`, `H-P7`)*, e
    # ### `_presidio.avvia` ### **STAMPA un TIMBRO** -- all-import avrebbe sporcato
    # ### l-uscita del `pre-commit` di una riga che nessuno ha chiesto.
    # ### ⭐ **Un modulo che e- SIA libreria SIA script si timbra quando e- SCRIPT.**
    # ### ⚠ **E senza, questa funzione MORIVA su `cp1252`:** e- la NONA volta che il
    # ### presidio encoding serve, e la nona volta che l-ho scoperto girando.
    sys.path.insert(0, _QUI)
    import _presidio
    _presidio.avvia(__file__)
    print("  I FILE DI FISICA SORVEGLIATI: %d" % len(FILE_FISICA))
    for x in FILE_FISICA:
        q = os.path.join(RADICE, x)
        print("   %-28s %s" % (x, "c-e-" if os.path.isfile(q) else "### NON C-E-"))
    print()
    if CARTELLA_ERA_2:
        print("  LA CARTELLA DELL-ERA 2: %r" % CARTELLA_ERA_2)
    else:
        print("  ### LA CARTELLA DELL-ERA 2 E- VUOTA: <<da decidere da Luca>>.")
        print("  ### ⛔ QUINDI IL PRESIDIO SULLA CARTELLA NON IMPEDISCE NIENTE (`A9`): il")
        print("  ###    codice c-e- e il collaudo gira su una cartella di PROVA, ma")
        print("  ###    SULL-ALBERO VERO non guarda niente. E- UNA TENDA, e lo dichiaro.")
    print()
    print("  CHI LEGGE LA LISTA (e prima scriveva il nome a mano):")
    for f in ("csv/_hook_fisica.py", "csv/_presidio_commenti_flag.py"):
        t = io.open(os.path.join(RADICE, f), encoding="utf-8").read()
        print("   %-34s %s" % (f, "legge la LISTA" if "_file_fisica" in t
                               else "### SCRIVE IL NOME A MANO"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
