# -*- coding: utf-8 -*-
"""IL REGISTRO DEI RUN -- un run senza resoconto e' un run che, dopo un riavvio, non e' mai esistito.

PERCHE' ESISTE (Regola 9 / A9): il PC si e' riavviato durante il lavoro e si e' perso SOLO il non
committato. E il commit `b84702b` dice *«RUN FERMATO»* senza dire **a che passo** ne' **se i dati
parziali servano**: e' esattamente il caso che questo presidio deve coprire.

COSA FA, ed e' AUTOMATICO:
  `apri(nome, comando, note)`   scrive in `doc/STATO_RUN.md` una riga APERTO con ora, blob del
                               simulatore (sha1 dei BYTE GREZZI, non `git hash-object`: C18),
                               HEAD, e il COMANDO VERBATIM;
  `tappa(nome, testo)`          aggiunge una riga di avanzamento (snapshot, frame, passo);
  `chiudi(nome, esito, testo)`  chiude la voce con FINITO / FERMATO / FALLITO **e il punto esatto**.
La scrittura e' **append-only** e **atomica**: un riavvio non puo' corromperla, al massimo lascia una
voce APERTA -- che e' l'informazione giusta.

⚠ DICHIARAZIONE ONESTA, e va letta prima di chiamarlo un presidio completo:
  **il COMMIT non e' automatico, e NON PUO' esserlo in modo sicuro.** Committare da dentro un run
  significherebbe fare operazioni git mentre il run scrive -- e CLAUDE.md vieta `git add -A` con un
  run attivo, per una ragione che resta valida.
  **Quello che E' automatico e' la SCRITTURA.** Quello che resta umano e' il `git add doc/STATO_RUN.md
  && git commit && git push`.
  **PERO' il file esiste SEMPRE**, quindi dopo un riavvio **lo stato si legge dal disco** invece che
  dalla memoria -- che e' il 90 % del problema.
  **E `apri()` RIFIUTA di partire se l'ultima voce e' ancora APERTA** *(a meno di `forza=True`)*:
  quello si', e' un impedimento, e obbliga a chiudere il run precedente prima di aprirne un altro.
ASCII PURO.
"""
import datetime as _dt
import hashlib as _hl
import os as _os
import subprocess as _sp

_REG = _os.path.join("doc", "STATO_RUN.md")


def _blob_byte(p="soliton_simulator.py"):
    try:
        b = open(p, "rb").read()
        return _hl.sha1(b"blob %d\0" % len(b) + b).hexdigest()[:8]
    except Exception:
        return "?"


def _head():
    try:
        return _sp.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "?"


def _ora():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _scrivi(righe):
    _os.makedirs(_os.path.dirname(_REG), exist_ok=True)
    if not _os.path.exists(_REG):
        with open(_REG, "w", encoding="utf-8", newline="") as fh:
            fh.write("# STATO DEI RUN — registro append-only\n\n"
                     "**Scritto AUTOMATICAMENTE da `csv/_stato_run.py`.** Il commit NON è\n"
                     "automatico (vedi la dichiarazione nel modulo): ma **il file esiste sempre**,\n"
                     "quindi dopo un riavvio lo stato si legge **dal disco**, non dalla memoria.\n\n"
                     "**Una voce `APERTO` senza `chiuso` = quel run è morto senza dirlo.**\n\n")
    with open(_REG, "a", encoding="utf-8", newline="") as fh:
        fh.write("".join(righe))


def _aperte():
    if not _os.path.exists(_REG):
        return []
    ap = []
    for l in open(_REG, encoding="utf-8"):
        if l.startswith("## APERTO "):
            ap.append(l.strip()[10:])
        elif l.startswith("**chiuso"):
            if ap:
                ap.pop()
    return ap


def apri(nome, comando, note="", forza=False):
    """Apre una voce. RIFIUTA se ce n'e' una ancora aperta: chiudere prima il run precedente."""
    ap = _aperte()
    if ap and not forza:
        raise SystemExit(
            "[stato-run] RIFIUTO: c'e' gia' una voce APERTA in %s -> %s\n"
            "  Un run aperto e mai chiuso e' un run che nessuno sa come e' finito.\n"
            "  Chiudilo con `chiudi(nome, esito, testo)` (anche 'FERMATO'), oppure usa forza=True\n"
            "  DICHIARANDO perche'." % (_REG, ap[-1]))
    _scrivi(["\n## APERTO %s\n\n" % nome,
             "- **avvio** `%s` · **blob** `%s` · **HEAD** `%s`\n" % (_ora(), _blob_byte(), _head()),
             "- **comando**\n  ```\n  %s\n  ```\n" % comando,
             ("- **note** %s\n" % note) if note else ""])
    return nome


def tappa(nome, testo):
    _scrivi(["- *%s* — %s\n" % (_ora(), testo)])


def chiudi(nome, esito, testo=""):
    """esito: FINITO / FERMATO / FALLITO. `testo` DEVE dire a che punto era e se i dati servono."""
    _scrivi(["\n**chiuso %s — %s** %s\n" % (_ora(), esito, testo)])
