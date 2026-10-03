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
    # ### L'INTESTAZIONE SI RICONOSCE PER STRUTTURA, NON PER SOTTOSTRINGA -- e anche
    #   questa cura nasce da un difetto MISURATO sul messaggio di `46432b4`.
    #   ### \u26d4 La prima stesura prendeva la PRIMA riga che CONTENEVA l'etichetta.
    #   In quel messaggio la prima era una menzione ### **IN PROSA** a riga 16
    #   *(<<Un messaggio la cui sezione FILE CAMBIATI non coincide...>>)*, e il parser
    #   ha letto come <<lista dei file>> le due righe di PROSA che la seguivano:
    #   ### **2 voci invece di 4, e un RIFIUTO che non c'entrava niente.**
    #   ### \u26a0 **E' LA STESSA RADICE DELLA VIA D'USCITA CITATA: un marcatore
    #   riconosciuto per SOTTOSTRINGA invece che per STRUTTURA.** Due volte nello stesso
    #   file, nella stessa ora -- una che produceva FALSI PASSAGGI *(silenzio)*, l'altra
    #   FALSI RIFIUTI *(rumore)*. ### **La stessa svista cade in ENTRAMBE le direzioni.**
    #   ### \u2705 Ora l'intestazione deve stare a INIZIO RIGA, e fra piu' intestazioni
    #   valide si prende ### **l'ULTIMA**: la convenzione la mette in fondo al messaggio.
    righe = testo.split(NL)
    teste = [i for i, r in enumerate(righe) if r.startswith(ETICHETTA)]
    if not teste:
        return [], False
    fuori = []
    for r in righe[teste[-1] + 1:]:
        if not r.strip():
            break
        if not (r.startswith(" ") or r.startswith(chr(9))):
            break
        fuori.append(r.strip().strip("`").strip())
    return fuori, True


def confronta(veri, detti):
    """### IL CONFRONTO, PURO: nessun git, nessun file. ### Cosi' il collaudo lo puo'
    esercitare ### **senza dipendere dall'indice** -- la prima batteria che ho scritto
    dipendeva, e una sua attesa e' ### **scaduta fra due esecuzioni** perche' avevo
    messo un file nell'indice nel frattempo. ### **Un collaudo che dipende dallo stato
    del mondo misura il mondo, non lo strumento.**
    """
    return ([f for f in veri if f not in detti],
            [f for f in detti if f not in veri])


def collaudo():
    """### LA BATTERIA, RIPRODUCIBILE: `python csv/_hook_file_cambiati.py --collaudo`."""
    casi = (
        ("lista giusta", ["a.py", "b.md"], "FILE CAMBIATI" + NL + "  a.py" + NL + "  b.md", 0),
        ("un file OMESSO", ["a.py", "b.md"], "FILE CAMBIATI" + NL + "  a.py", 1),
        ("un file INVENTATO", ["a.py"],
         "FILE CAMBIATI" + NL + "  a.py" + NL + "  z.md", 1),
        ("sezione ASSENTE", ["a.py"], "nessuna lista qui", 1),
        ("uscita a INIZIO RIGA", ["a.py"], USCITA + " merge]", 0),
        ("uscita CITATA, rientrata", ["a.py"],
         "x" + NL + "    " + USCITA + " citata]", 1),
        ("etichetta in PROSA, poi quella vera", ["a.py"],
         "parlo di FILE CAMBIATI qui" + NL + "  prosa" + NL + "  altra prosa" + NL + NL
         + "FILE CAMBIATI" + NL + "  a.py", 0),
        ("backtick attorno al nome", ["a.py"],
         "FILE CAMBIATI" + NL + "  `a.py`", 0),
    )
    brutte = 0
    for nome, veri, msg, atteso in casi:
        if any(r.startswith(USCITA) for r in msg.split(NL)):
            avuto = 0
        else:
            detti, c_e = dichiarati(msg)
            if not c_e:
                avuto = 1
            else:
                m, i = confronta(veri, detti)
                avuto = 1 if (m or i) else 0
        ok = (avuto == atteso)
        brutte += 0 if ok else 1
        print("  %-38s atteso %d  ottenuto %d  %s"
              % (nome, atteso, avuto, "OK" if ok else "*** DIVERSO ***"))
    print("  ### %s" % ("tutti e %d i casi passano." % len(casi) if not brutte
                        else "*** %d CASI FALLISCONO ***" % brutte))
    return 1 if brutte else 0


def principale():
    if "--collaudo" in sys.argv:
        return collaudo()
    if "--controlla" not in sys.argv:
        print(__doc__)
        print("  ### E QUESTO PRESIDIO IMPEDISCE QUALCOSA SOLO SE E' INSTALLATO:")
        print("  ###   git config core.hooksPath .githooks")
        return 0
    p = sys.argv[sys.argv.index("--controlla") + 1]
    testo = io.open(p, encoding="utf-8", errors="replace").read()

    # ### LA VIA D'USCITA SI RICONOSCE SOLO A INIZIO RIGA, SENZA RIENTRO -- e la cura
    #   nasce da un falso-passaggio del PRIMO commit di questo presidio.
    #   ### ⛔ `46432b4` -- il commit che INTRODUCE `H-FILE` -- e' passato con
    #   *<<eccezione DICHIARATA>>* perche' il messaggio ### **CITAVA** la stringa d'uscita
    #   due volte: nel riassunto di `CLAUDE.md` e nella tabella del collaudo.
    #   ### **Cercare la stringa in TUTTO il testo rende la via d'uscita attivabile
    #   DESCRIVENDOLA**, e un presidio che si disarma parlando di se' non e' un presidio.
    #   ### ✅ Ora deve stare a INIZIO RIGA e senza rientro: una menzione dentro una
    #   tabella, un elenco o una frase ### **non apre niente.**
    if any(r.startswith(USCITA) for r in testo.split(NL)):
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

    # ### LA STESSA FUNZIONE CHE IL COLLAUDO ESERCITA, e non una copia: se qui ci
    #   fosse il confronto scritto in linea, ### **`--collaudo` proverebbe
    #   un'implementazione PARALLELA** e passerebbe anche con questa rotta.
    #   ### **Un collaudo che non attraversa il codice vero non e' un collaudo.**
    mancanti, inventati = confronta(veri, detti)
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
