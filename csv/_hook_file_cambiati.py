# -*- coding: utf-8 -*-
"""`H-FILE` — IL PRESIDIO DELLA LISTA DEI FILE NEL MESSAGGIO DI COMMIT.

### **Che cosa impedisce:** un messaggio che dichiara una sezione **`FILE CAMBIATI`** la cui
lista **non coincide** con `git diff --cached --name-only`.

### ⛔ **PERCHE' ESISTE** *(decisione di Luca, 2026-10-03)*: la lista a memoria e' sbagliata
**due volte su tre**. I casi, dal repo:

| commit | che cosa diceva | che cosa mancava |
|---|---|---|
| `2ab4ce2` | *<<FILE CAMBIATI, tutti>>* | `doc/INDICE_ID_ESCLUSI.tsv` |
| `1d58764` | *<<FILE CAMBIATI, tutti>>* | `doc/INDICE_ID_ESCLUSI.tsv` |

### **E DOPO QUEI DUE LA REGOLA ERA SCRITTA** *(<<la lista si genera da `git diff --cached
--name-only`>>)*, ### **e una regola scritta non e' un presidio: e' `A9`.** Questo file la
rende una macchina.

### ✅ **E IL SUO PRIMO ATTO E' STATO SCAGIONARE UN COMMIT:** il guardiano ha contestato
`1927b45` come terza recidiva *(<<5 file elencati, 6 cambiati, omette
`doc/INVENTARIO_strumenti.md`>>)*. ### **Verificato con `git log` e `git show`: la lista del
messaggio e quella reale COINCIDONO, sei e sei, l'inventario compreso.** ### **La
contestazione non regge, e il presidio serve anche a questo** — a decidere con un comando una
cosa che altrimenti si decide a memoria, ### **in entrambe le direzioni.**

**LA VIA D'USCITA, e obbliga a dichiarare:** `[SENZA-FILE-CAMBIATI: <motivo>]` nel messaggio.
*(Serve per i commit di merge e per ogni caso in cui la lista non ha senso.)*

### ⚠ **IL LIMITE, per `A9`:** il presidio guarda la sezione **se c'e'**, e **PRETENDE che
ci sia**; ma non puo' verificare che cio' che il messaggio dice **sui** file sia vero. Un
commit che elenca i sei file giusti e li descrive male passa.

**COMANDO:** chiamato dal `commit-msg`. A mano:
`python csv/_hook_file_cambiati.py --controlla <file-del-messaggio>`
"""
import io
import os
import subprocess
import sys

NL = chr(10)
ETICHETTA = "FILE CAMBIATI"
USCITA = "[SENZA-FILE-CAMBIATI:"


def _dillo(*x):
    sys.stderr.write(" ".join(str(y) for y in x) + NL)


def staged():
    """I file dell'INDICE, che e' cio' che il commit contiene davvero."""
    q = subprocess.run(["git", "diff", "--cached", "--name-only"],
                       capture_output=True, text=True)
    if q.returncode != 0:
        return None
    return [r.strip() for r in q.stdout.split(NL) if r.strip()]


def dichiarati(testo):
    """La lista sotto l'intestazione `FILE CAMBIATI`.

    ### Si prende ogni riga RIENTRATA che segue, e si fermano le righe vuote o non
    rientrate. ### I backtick si togliono: la lista si legge, non si decora.
    """
    righe = testo.split(NL)
    dentro = False
    fuori = []
    for r in righe:
        if not dentro:
            if ETICHETTA in r:
                dentro = True
            continue
        if not r.strip():
            break
        if not (r.startswith(" ") or r.startswith("\t")):
            break
        fuori.append(r.strip().strip("`").strip())
    return fuori, dentro


def principale():
    if "--controlla" not in sys.argv:
        print(__doc__)
        print("  ### E QUESTO PRESIDIO IMPEDISCE QUALCOSA SOLO SE E' INSTALLATO:")
        print("  ###   git config core.hooksPath .githooks")
        return 0
    p = sys.argv[sys.argv.index("--controlla") + 1]
    testo = io.open(p, encoding="utf-8", errors="replace").read()

    if USCITA in testo:
        _dillo("[H-FILE] eccezione DICHIARATA nel messaggio.")
        return 0

    # ### UN MERGE NON HA UNA LISTA SENSATA: si salta, e si DICE che si e' saltato.
    if os.path.exists(os.path.join(".git", "MERGE_HEAD")):
        _dillo("[H-FILE] commit di MERGE: la lista non si verifica.")
        return 0

    veri = staged()
    if veri is None:
        _dillo("[H-FILE] `git diff --cached` non risponde: non verifico.")
        return 0

    detti, c_e = dichiarati(testo)
    if not c_e:
        _dillo("=" * 92)
        _dillo("[H-FILE] IL MESSAGGIO NON HA LA SEZIONE `%s`." % ETICHETTA)
        _dillo("  Il par.5 chiede COSA e' cambiato, e la lista si GENERA, non si ricorda:")
        _dillo("      git diff --cached --name-only")
        _dillo("  I %d file di questo commit sono:" % len(veri))
        for f in veri:
            _dillo("      %s" % f)
        _dillo("  Via d'uscita, se la lista non ha senso: %s <motivo>]" % USCITA)
        _dillo("=" * 92)
        return 1

    mancanti = [f for f in veri if f not in detti]
    inventati = [f for f in detti if f not in veri]
    if not mancanti and not inventati:
        _dillo("[H-FILE] la lista coincide: %d file." % len(veri))
        return 0

    _dillo("=" * 92)
    _dillo("[H-FILE] LA LISTA `%s` NON COINCIDE CON L'INDICE." % ETICHETTA)
    _dillo("  dichiarati nel messaggio .. %d" % len(detti))
    _dillo("  davvero nell'indice ....... %d" % len(veri))
    if mancanti:
        _dillo("  ### CAMBIATI MA NON DICHIARATI (%d) -- e' il caso che si ripete:"
               % len(mancanti))
        for f in mancanti:
            _dillo("      %s" % f)
    if inventati:
        _dillo("  ### DICHIARATI MA NON CAMBIATI (%d):" % len(inventati))
        for f in inventati:
            _dillo("      %s" % f)
    _dillo("  ### La lista giusta, da incollare:")
    for f in veri:
        _dillo("      %s" % f)
    _dillo("=" * 92)
    return 1


if __name__ == "__main__":
    sys.exit(principale())
