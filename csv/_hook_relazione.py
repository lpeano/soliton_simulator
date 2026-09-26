# -*- coding: utf-8 -*-
"""IMPEDIMENTO `P1-bis` -- un commit che contiene un RISCONTRO non passa senza la RELAZIONE.

⚠ PERCHE' ESISTE, e non e' una precauzione teorica: **misurato due volte**. Il 2026-09-20,
**7 relazioni su 52 commit**. Il 2026-09-21, **10 su 32 in un giorno solo -- 22 riscontri saltati**,
e fra quelli i piu' grossi della giornata. **Luca ha dovuto dirlo TRE volte.**
`CLAUDE.md` aveva gia' il par.5-ter, e poi `P1-bis`: **due regole SCRITTE non hanno cambiato il
numero.** `A9` dice che **un presidio che non impedisce non e' un presidio**, e questo e' il
tentativo di renderlo tale.

COSA BLOCCA: un commit che tocca un file da cui si vede che c'e' un riscontro --
  * `doc/RAMIFICAZIONI.md`      una voce del registro E' un riscontro, per definizione
  * `doc/REFERTO_*.md`          un referto E' un riscontro
  * `csv/_seal_fork/*.txt`      l'output di un sigillo E' un verdetto
  * `csv/**/_diag_*/**`         dati diagnostici estratti
-- e che **NON tocca `RELAZIONE_PER_CLAUDE.md`**.

LA VIA D'USCITA, e obbliga a DICHIARARE: si mette nel messaggio di commit la riga
    [SENZA-RELAZIONE: <motivo>]
Cosi' un'eccezione resta possibile ma **lascia una traccia leggibile in `git log`**, invece di
passare in silenzio. E' la stessa forma di `_stato_run.apri(forza=True)`.

⚠ DICHIARAZIONE ONESTA, per `A9`: i hook NON sono versionati da git. Un clone nuovo **non ce
  l'ha**, e va installato con `python csv/_hook_relazione.py --installa`. **Questo lo rende meno
  di un presidio completo, e va detto invece di chiamarlo tale.**
ASCII PURO.
"""
import io
import os
import re
import subprocess
import sys

RISCONTRO = (
    (r"^doc/RAMIFICAZIONI\.md$", "una voce del registro"),
    (r"^doc/REFERTO_.*\.md$", "un referto"),
    (r"^csv/_seal_fork/.*\.txt$", "l'output di un sigillo"),
    (r"^csv/.*/_diag_[^/]*/", "dati diagnostici"),
)
RELAZIONE = "RELAZIONE_PER_CLAUDE.md"
FUGA = re.compile(r"\[SENZA-RELAZIONE:\s*(.+?)\]", re.I)

# [2026-09-22, regola di Luca] OGNI DIFETTO ACCLARATO SI REGISTRA SUBITO NELLA CODA UNICA.
#   Un commit che DICHIARA un difetto, un sospetto o una promozione ma NON tocca la coda sta
#   perdendo esattamente cio' che la regola vuole salvare: dopo una compattazione quel
#   difetto non esiste piu'. Due cure sicure -- SPINTA_LOCALE e POZZO_D -- sono vissute per
#   giorni solo nella relazione e nei mandati. Qui si IMPEDISCE, non si raccomanda (A9).
CODA = "doc/STATO_RUN.md"
DIFETTO = re.compile(r"^\s*(DIFETTO ACCLARATO|SOSPETTO|PROMOSSO)\s*:", re.I | re.M)


def installa():
    """⚠ IL HOOK E' `commit-msg`, NON `pre-commit`, e il perche' e' un difetto trovato PROVANDOLO.

    La prima versione stava in `pre-commit`, che gira **PRIMA** che git scriva il messaggio: li'
    `COMMIT_EDITMSG` contiene ancora quello del commit PRECEDENTE, e la via d'uscita
    `[SENZA-RELAZIONE: ...]` **non poteva funzionare** — bloccava anche quando era dichiarata.
    **Trovato al primo giro perche' l'ho PROVATA:** un presidio non provato e' una nota.
    `commit-msg` riceve il file del messaggio come primo argomento, e vede anche l'indice.
    """
    d = subprocess.check_output(["git", "rev-parse", "--git-dir"], text=True).strip()
    vecchio = os.path.join(d, "hooks", "pre-commit")
    if os.path.exists(vecchio):
        try:
            if "_hook_relazione" in io.open(vecchio, encoding="utf-8", errors="replace").read():
                os.remove(vecchio)
                print("rimosso il hook SBAGLIATO: %s" % vecchio)
        except OSError:
            pass
    h = os.path.join(d, "hooks", "commit-msg")
    os.makedirs(os.path.dirname(h), exist_ok=True)
    io.open(h, "w", encoding="utf-8", newline="\n").write(
        "#!/bin/sh\n"
        "# IMPEDIMENTO P1-bis -- vedi csv/_hook_relazione.py\n"
        'exec python csv/_hook_relazione.py --controlla "$1"\n')
    try:
        os.chmod(h, 0o755)
    except OSError:
        pass
    print("installato: %s" % h)
    return 0


def controlla():
    try:
        st = subprocess.check_output(["git", "diff", "--cached", "--name-only"],
                                     text=True).splitlines()
    except subprocess.CalledProcessError:
        return 0
    st = [x.strip().replace("\\", "/") for x in st if x.strip()]
    if not st:
        return 0
    motivi = []
    for f in st:
        for pat, perche in RISCONTRO:
            if re.search(pat, f):
                motivi.append((f, perche))
                break
    # il messaggio serve a DUE controlli: si legge UNA volta sola.
    msg0 = ""
    _arg = [x for x in sys.argv[1:] if not x.startswith("--")]
    if _arg and os.path.exists(_arg[0]):
        msg0 = io.open(_arg[0], encoding="utf-8", errors="replace").read()

    # --- IL CONTROLLO DELLA CODA: chi DICHIARA un difetto deve REGISTRARLO.
    _d = DIFETTO.search(msg0)
    if _d and CODA not in st:
        sys.stderr.write(
            "\n[DIFETTI] *** COMMIT RIFIUTATO: il messaggio dichiara `" + _d.group(1)
            + "` ma\n"
            "           `" + CODA + "` NON e' nel commit. ***\n\n"
            "  Un difetto acclarato che non entra nella CODA UNICA si PERDE alla prima\n"
            "  compattazione, ed e' esattamente cio' che la regola del 2026-09-22 impedisce.\n\n"
            "  CHE FARE: aggiungi la riga nella sezione DIFETTI APERTI (o SOSPETTI) di\n"
            "  " + CODA + " e mettila nel commit.\n\n")
        return 1

    # --- [REG-R, 2026-09-22] NESSUNA LEGGE CAMBIA SENZA CHE CAMBI LA SUA SCHEDA.
    #   Sta QUI e non in un hook suo perche' `commit-msg` e' uno solo: due hook che se lo
    #   contendono e' il modo in cui un presidio sparisce in silenzio.
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import _hook_fisica
        _c, _t = _hook_fisica.controlla(st, msg0)
        if _t:
            sys.stderr.write(_t)
        if _c:
            return _c
    except Exception as _e:            # A8: un presidio che si schianta NON deve bloccare
        sys.stderr.write("[H-REG-R] il controllo NON e' girato (%s): dichiarato, non nascosto.\n"
                         % _e)

    # [INDICE, 2026-09-26] gli ID citati NEL MESSAGGIO: qui e' l'unico punto in cui git lo ha
    #   gia' scritto. Sta accanto a `REG-R` per la stessa ragione: `commit-msg` e' UNO SOLO.
    try:
        import _presidio_indice
        # le righe AGGIUNTE ai documenti vivi **piu'** il messaggio: e' l'unico stadio in cui
        #   entrambi sono disponibili, quindi il controllo intero vive qui.
        _ig, _am = _presidio_indice.esamina(_presidio_indice._aggiunte() + "\n" + msg0)
        if _ig or _am:
            if "[SENZA-INDICE:" in msg0:
                sys.stderr.write("[H-INDICE] eccezione DICHIARATA nel messaggio.\n")
            else:
                sys.stderr.write("\n[H-INDICE] *** COMMIT RIFIUTATO ***\n\n"
                                 "  ID citati nel MESSAGGIO e non nell'indice: %s\n"
                                 % ", ".join((_ig + _am)[:20])
                                 + "  CHE FARE: definirli in un registro e rigenerare"
                                 " (python csv/_indice_id.py), oppure\n"
                                 "    aggiungerli a doc/INDICE_ID_ESCLUSI.tsv col motivo,"
                                 " oppure dichiarare\n"
                                 "    [SENZA-INDICE: <motivo>] nel messaggio.\n\n")
                return 1
    except Exception as _e2:           # A8: un presidio che si schianta NON deve bloccare
        sys.stderr.write("[H-INDICE] il controllo NON e' girato (%s): dichiarato, non nascosto.\n"
                         % _e2)

    # [H-RIGHE, 2026-09-26] `CLAUDE.md` non passa le 400 righe. Sta QUI per la stessa ragione di
    #   `H-INDICE`: la via d'uscita `[CLAUDE-OLTRE-400: ...]` si legge **nel messaggio**, e in
    #   `pre-commit` il messaggio non esiste ancora. `commit-msg` e' UNO SOLO, e i presidi che
    #   hanno bisogno del messaggio stanno tutti qui dentro.
    try:
        import _presidio_righe
        _cr, _tr = _presidio_righe.controlla(msg0)
        if _tr:
            sys.stderr.write(_tr)
        if _cr:
            return _cr
    except Exception as _e3:           # A8: un presidio che si schianta NON deve bloccare
        sys.stderr.write("[H-RIGHE] il controllo NON e' girato (%s): dichiarato, non nascosto.\n"
                         % _e3)

    if not motivi:
        return 0
    if RELAZIONE in st:
        return 0
    # la via d'uscita, che obbliga a DICHIARARE. Il messaggio arriva come argomento del hook
    # `commit-msg`: e' l'unico punto in cui git lo ha gia' scritto (vedi `installa`).
    m = FUGA.search(msg0)
    if m:
        sys.stderr.write("[H-P1-bis] eccezione DICHIARATA: %s\n" % m.group(1).strip())
        return 0
    sys.stderr.write(
        "\n[H-P1-bis] *** COMMIT RIFIUTATO: c'e' un RISCONTRO e manca la RELAZIONE. ***\n\n"
        "  Questi file dicono che il commit contiene un riscontro:\n")
    for f, perche in motivi[:8]:
        sys.stderr.write("    %-50s  (%s)\n" % (f, perche))
    sys.stderr.write(
        "\n  ma `%s` NON e' nel commit.\n\n"
        "  Un riscontro non relazionato e' un riscontro PERSO: chi legge il repo da fuori\n"
        "  -- Claude web, una sessione nuova, Luca fra tre giorni -- non ha la conversazione,\n"
        "  ha solo i file. E il messaggio di commit NON conta: lo vede solo chi scorre\n"
        "  `git log` gia' sapendo cosa cercare.\n\n"
        "  CHE FARE:\n"
        "    1. scrivi il paragrafo in %s e aggiungilo al commit;  oppure\n"
        "    2. se davvero non serve, mettilo NERO SU BIANCO nel messaggio:\n"
        "         [SENZA-RELAZIONE: <motivo>]\n"
        "       L'eccezione resta possibile, ma lascia una traccia in `git log`.\n\n"
        % (RELAZIONE, RELAZIONE))
    return 1


if __name__ == "__main__":
    if "--installa" in sys.argv:
        sys.exit(installa())
    sys.exit(controlla())
