# -*- coding: utf-8 -*-
"""IL COLLAUDO DI `csv/_file_fisica.py` — **su una cartella di PROVA, in una COPIA.**

> ### ⛔ **La cartella dell'era `2` è VUOTA**, e il mandato lo impone: *«NON la scegli tu»*.
> ### ⚠ **Quindi sull'albero vero il presidio non impedisce niente** — per `A9`
> ### **non è un presidio, è una tenda.**
>
> ### ✔ **E ALLORA IL COLLAUDO LO PROVA ALTROVE:** si copia `_file_fisica.py` in una
> cartella temporanea, ### **si scrive un nome di prova nella COSTANTE della copia**, e si
> fanno scattare i casi. ### **Così il codice è provato oggi e il presidio diventa vero il
> giorno in cui Luca dà il nome, cambiando UNA STRINGA.**

### ⭐ **E il collaudo prova anche la cosa più importante: che con la cartella VUOTA il
presidio TACE.** ### **Un presidio che tace va provato che taccia**, altrimenti nessuno sa
se tace perché è spento o perché è rotto.

Gira con:  python csv/_collaudo_file_fisica.py
"""
import importlib.util
import io
import os
import shutil
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
# ### ⛔ **LA PULIZIA NON SI SILENZIA** *(decisione di Luca, 2026-10-10)*:
# ### `shutil.rmtree(..., ignore_errors=True)` ### **non cancella gli oggetti di
# ### `git`, che sono in SOLA LETTURA, e NON LO DICE** -- e cosi- il `%TEMP%` si era
# ### riempito di ### **24 cartelle** che nessuno vedeva.
import _pulizia                                              # noqa: E402
_presidio.avvia(__file__)
import _file_fisica as FF                                    # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Collauda due costanti.
NL = chr(10)
PROVA = "codice_era2_di_prova"
_ok = [0, 0]


def esito(che, passa, nota=""):
    _ok[1] += 1
    _ok[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))


def copia_con_cartella(dove, nome):
    """### Una COPIA di `_file_fisica.py` con la cartella ### **scritta nella costante.**

    ### ⛔ **Non si tocca il file vero**, e non si usa una variabile d-ambiente: la costante
    ### **e- una costante** *(`A1`: zero manopole)*, e il collaudo ### **ne cambia una COPIA.**
    """
    sorg = io.open(os.path.join(_QUI, "_file_fisica.py"), encoding="utf-8").read()
    # ### ⚠ **L-ANCORA SEGUE LA COSTANTE:** quando il nome e- arrivato, la riga e-
    # ### cambiata e ### **l-assert l-ha detto subito** invece di lasciare il collaudo
    # ### girare su una copia ### **identica all-originale.**
    a = 'CARTELLA_ERA_2 = "primo_ordine/"   # decisione di Luca, 2026-10-09'
    assert sorg.count(a) == 1, "l-ancora della costante non e- unica"
    p = os.path.join(dove, "_ff_prova.py")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        sorg.replace(a, 'CARTELLA_ERA_2 = %r' % nome))
    spec = importlib.util.spec_from_file_location("_ff_prova", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    print("=" * 100)
    print("IL COLLAUDO DI `csv/_file_fisica.py` -- su una cartella di PROVA, in una COPIA")
    print("=" * 100)
    # ### ✔ **PRIMA LA COSA PIU- IMPORTANTE: LA CARTELLA HA UN NOME, E IL PRESIDIO
    # ### ### IMPEDISCE.** *(decisione di Luca del 2026-10-09: `primo_ordine/`)*
    # ### ⛔ **Fino a stamattina la costante era `""` e il presidio era UNA TENDA** (`A9`):
    # ### i tre bracci di prima provavano ### **che TACEVA.** ### **Adesso provano che
    # ### IMPEDISCE**, e il braccio accanto conserva ### **la prova del vecchio stato**,
    # ### perche- ### **cio- che un presidio NON faceva e- una misura, non un ricordo.**
    esito("la CARTELLA dell-era 2 HA UN NOME",
          FF.CARTELLA_ERA_2 == "primo_ordine/",
          "decisione di Luca, 2026-10-09: era `\"\"` e il presidio era UNA TENDA")
    VERA = FF.CARTELLA_ERA_2.rstrip("/")
    print("  la cartella VERA: %r   (esiste sul disco: %s -- e NON l-ho creata io)"
          % (FF.CARTELLA_ERA_2,
             "si-" if os.path.isdir(os.path.join(RADICE, VERA)) else "NO"))
    print()
    print("  (a) SULLA CARTELLA VERA, NEI DUE VERSI -- ed e- cio- che il mandato chiede")
    esito("### DEVE rifiutare: un `.py` FUORI LISTA sotto `%s`" % FF.CARTELLA_ERA_2,
          FF.intrusi(["%s/nuova_fisica.py" % VERA]) == ["%s/nuova_fisica.py" % VERA],
          "fisica che NESSUN presidio sorveglia")
    esito("NON deve rifiutare: un file CHE E- NELLA LISTA",
          FF.intrusi(list(FF.FILE_FISICA)) == [],
          "il presidio non deve impedire proprio cio- che chiede di fare")
    esito("### DEVE rifiutare: anche in una SOTTOCARTELLA di `%s`" % FF.CARTELLA_ERA_2,
          FF.intrusi(["%s/leggi/campo.py" % VERA]) != [],
          "la regola e- <<SOTTO la cartella>>, non <<DENTRO la cartella>>")
    esito("NON deve rifiutare: un file che NON finisce in `.py`",
          FF.intrusi(["%s/dati.json" % VERA, "%s/note.md" % VERA]) == [],
          "la regola del mandato dice <<un `.py` nuovo>>")
    esito("### DEVE rifiutare: lo stesso percorso con le BARRE DI WINDOWS",
          FF.intrusi([VERA + chr(92) + "nuova.py"]) != [],
          "due forme dello stesso percorso NON sono lo stesso percorso per una `==`")
    esito("NON deve rifiutare: un `.py` FUORI dalla cartella",
          FF.intrusi(["csv/indice.py", "altrove/x.py",
                      VERA + "_simile/x.py"]) == [],
          "e nemmeno una cartella col nome che COMINCIA come quella: serve la barra")
    print()
    print("  (b) LA PROVA DEL VECCHIO STATO, su una COPIA con la costante VUOTA")
    _tv = tempfile.mkdtemp(prefix="ff0_")
    try:
        _m0 = copia_con_cartella(_tv, "")
        esito("con la cartella VUOTA `intrusi` era SEMPRE vuoto -- ### ERA UNA TENDA",
              _m0.intrusi(["x.py", "%s/x.py" % VERA, "a/b/c.py"]) == [],
              "e- la misura di cio- che il presidio NON faceva: non un ricordo")
    finally:
        _pulizia.via_finale(_tv)
    # ### ⛔ **E LA LISTA NON PUO- RIPETERSI** *(trovato il 2026-10-10)*: i tre
    # ### file di `config/` c-erano ### **CINQUE VOLTE**, residuo di una patch non
    # ### idempotente. ### ⚠ **Non impediva niente**, ma ### **il conteggio era
    # ### sbagliato: 48 dove i file sono 36** -- e un presidio che conta sbagliato
    # ### ### **prima o poi scrive quel numero in un referto.**
    _dupl = sorted(set(x for x in FF.FILE_FISICA
                       if list(FF.FILE_FISICA).count(x) > 1))
    esito("### la LISTA non ha DUPLICATI", not _dupl,
          "### %d file in lista, %d distinti%s"
          % (len(FF.FILE_FISICA), len(set(FF.FILE_FISICA)),
             (": " + ", ".join(_dupl[:3])) if _dupl else ""))
    print()
    tmp = tempfile.mkdtemp(prefix="ff_")
    try:
        mod = copia_con_cartella(tmp, PROVA)
        print("  la COPIA ha `CARTELLA_ERA_2 = %r`" % mod.CARTELLA_ERA_2)
        esito("### DEVE scattare: un `.py` NUOVO sotto la cartella, non nella LISTA",
              mod.intrusi(["%s/nuova_fisica.py" % PROVA]) == ["%s/nuova_fisica.py" % PROVA],
              "fisica che nessun presidio sorveglia")
        esito("### DEVE scattare: anche in una SOTTOCARTELLA",
              mod.intrusi(["%s/leggi/campo.py" % PROVA]) != [],
              "la regola e- <<sotto la cartella>>, non <<dentro la cartella>>")
        esito("NON deve scattare: un file CHE E- NELLA LISTA",
              mod.intrusi(list(mod.FILE_FISICA)) == [],
              "cio- che e- nella lista e- sorvegliato: e- il caso sano")
        # ### ⚠ **E il caso del file di lista spostato LA- SOTTO:** se un giorno
        # ### `FILE_FISICA` contenesse un percorso dentro la cartella, ### **non deve
        # ### scattare** -- altrimenti il presidio ### **impedirebbe proprio cio- che
        # ### chiede di fare.**
        mod2 = copia_con_cartella(tmp, PROVA)
        mod2.FILE_FISICA = ("%s/campo.py" % PROVA,)
        esito("NON deve scattare: un file DENTRO la cartella ma NELLA LISTA",
              mod2.intrusi(["%s/campo.py" % PROVA]) == [],
              "il presidio non deve impedire proprio cio- che chiede di fare")
        esito("### DEVE scattare: un ALTRO file nella stessa cartella, fuori lista",
              mod2.intrusi(["%s/altro.py" % PROVA]) == ["%s/altro.py" % PROVA])
        esito("NON deve scattare: un file che NON finisce in `.py`",
              mod.intrusi(["%s/dati.json" % PROVA, "%s/note.md" % PROVA]) == [],
              "la regola del mandato dice <<un `.py` nuovo>>")
        # ### ⛔ **E LE BARRE: git dice `a/b.py`, Windows dice `a\\b.py`.**
        esito("### DEVE scattare: lo stesso percorso con le barre di Windows",
              mod.intrusi([PROVA + chr(92) + "nuova.py"]) != [],
              "due forme dello stesso percorso NON sono lo stesso percorso per una `==`")
    finally:
        _pulizia.via_finale(tmp)
    print()
    # ### ✔ **E I DUE PRESIDI LEGGONO LA LISTA, non il nome a mano.**
    for f in ("csv/_hook_fisica.py", "csv/_presidio_commenti_flag.py"):
        t = io.open(os.path.join(RADICE, f), encoding="utf-8").read()
        esito("%s LEGGE la LISTA" % f, "_file_fisica" in t,
              "prima scriveva `soliton_simulator.py` a mano")
    print("=" * 100)
    print("IL COLLAUDO DI `_file_fisica.py`: %d su %d   %s"
          % (_ok[0], _ok[1], "### TUTTI PASSATI" if _ok[0] == _ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if _ok[0] == _ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
