# -*- coding: utf-8 -*-
"""`H-NON-TRACCIATI` — IL PRESIDIO DEI FILE NON TRACCIATI SOTTO `csv/` E `doc/`.

### **Che cosa impedisce:** un commit fatto mentre esistono file ### **non tracciati e non
ignorati** sotto `csv/` o `doc/`. ### **BLOCCA**, non avvisa.

### ⛔ **PERCHE' ESISTE, e il caso ha un nome: `_sonda_scherm`.** Una sonda e' girata
### **fuori dal repo**, il suo referto e' stato committato e ### **lo strumento no** — quindi
il referto citava uno strumento che nel repo ### **non esisteva.** ### **Il censimento del
2026-10-04 ha misurato quanto sia comune: su `484` non tracciati, `98` erano CITATI da un
documento, da un referto o dall'inventario** — cioe' ### **98 riferimenti al vuoto.**

> ### 📌 **E IL NUMERO CHE CONTA SONO I CITATI, non i dimenticati.** Un file non citato e non
> tracciato e' ### **rumore**: nessuno lo cerca. Un file ### **citato** e non tracciato e'
> ### **una promessa non mantenuta**, e chi verifica dal repo la scopre cercando.

### ⚠ **PERCHE' BLOCCA E NON AVVISA** *(decisione di Luca, 2026-10-04)*: un avviso che
nessuno legge e' `A9`. ### **E la via d'uscita rende il blocco sopportabile**: durante un run
il referto ### **in scrittura** si dichiara, e si committa ### **a run chiuso**.

**LA VIA D'USCITA:** `[SENZA-NON-TRACCIATI: <motivo>]` ### **a INIZIO RIGA**, nel messaggio.
### ⛔ **A inizio riga e senza rientro, come in `H-FILE`, e per lo stesso difetto MISURATO:**
cercando la stringa in ### **tutto** il testo, il commit che introduceva `H-FILE` e' passato
### **senza controllo**, perche' il messaggio la ### **CITAVA** nella tabella del collaudo.
### **Un presidio che si disarma parlando di se' non e' un presidio.**

**COMANDO:** chiamato dal `commit-msg`. A mano:
`python csv/_hook_non_tracciati.py --controlla <file-del-messaggio>` · `--collaudo`
"""
import io
import subprocess
import sys

NL = chr(10)
USCITA = "[SENZA-NON-TRACCIATI:"
SOTTO = ("csv/", "doc/")


def _dillo(*x):
    sys.stderr.write(" ".join(str(y) for y in x) + NL)


def non_tracciati():
    """### I non tracciati e NON IGNORATI sotto `csv/` e `doc/`.

    ### `--untracked-files=all` e' necessario: senza, git ### **riassume una cartella in una
    riga** e il conto sarebbe sbagliato ### **per difetto** — cioe' il presidio lascerebbe
    passare proprio i casi in cui i file dimenticati sono molti.
    ### ⚠ **E i percorsi si leggono con `-z`, a BYTE**: con l'uscita testuale su Windows si
    infila un `\\r` in ogni riga, e il confronto con un prefisso ### **sbaglia in silenzio**.
    *(Misurato il 2026-10-04 sul controllo del `.gitignore`: diceva `12` dove il vero era
    `0`.)*
    """
    q = subprocess.run(["git", "status", "--porcelain", "-z",
                        "--untracked-files=all"], capture_output=True)
    if q.returncode != 0:
        return None
    fuori = []
    for pezzo in q.stdout.split(b"\0"):
        if not pezzo.startswith(b"?? "):
            continue
        rel = pezzo[3:].decode("utf-8", "replace").strip().strip(chr(34))
        if rel.startswith(SOTTO):
            fuori.append(rel)
    return sorted(fuori)


def giudica(elenco, messaggio):
    """### IL GIUDIZIO, PURO: nessun git, nessun file.

    Da' `(uscita, motivo)`. ### Cosi' il collaudo lo esercita ### **con una lista
    INIETTATA** — e non misura lo stato del repo invece dello strumento. *(E' la lezione del
    collaudo di `H-FILE`, la cui prima batteria dipendeva dall'indice di git e una sua attesa
    e' SCADUTA fra due esecuzioni.)*
    """
    if any(r.startswith(USCITA) for r in messaggio.split(NL)):
        return 0, "eccezione DICHIARATA a inizio riga"
    if not elenco:
        return 0, "nessun file non tracciato sotto %s" % ", ".join(SOTTO)
    return 1, "%d file non tracciati e non ignorati" % len(elenco)


def collaudo():
    """### LA BATTERIA, riproducibile: `python csv/_hook_non_tracciati.py --collaudo`."""
    casi = (
        ("lista VUOTA", [], "un messaggio qualunque", 0),
        ("un non tracciato", ["csv/_test_fork/_x.txt"], "un messaggio qualunque", 1),
        ("tre non tracciati", ["csv/a.txt", "doc/b.md", "csv/c/d.json"], "x", 1),
        ("uscita a INIZIO RIGA", ["csv/_test_fork/_x.txt"],
         USCITA + " run in corso]", 0),
        ("uscita CITATA e rientrata", ["csv/_test_fork/_x.txt"],
         "x" + NL + "    " + USCITA + " citata nel collaudo]", 1),
        ("uscita a inizio riga, lista vuota", [], USCITA + " merge]", 0),
    )
    brutte = 0
    for nome, elenco, msg, atteso in casi:
        avuto, motivo = giudica(elenco, msg)
        ok = (avuto == atteso)
        brutte += 0 if ok else 1
        print("  %-34s atteso %d  ottenuto %d  %s"
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
    elenco = non_tracciati()
    if elenco is None:
        _dillo("[H-NON-TRACCIATI] `git status` non risponde: non verifico.")
        return 0
    uscita, motivo = giudica(elenco, testo)
    if uscita == 0:
        _dillo("[H-NON-TRACCIATI] %s." % motivo)
        return 0
    _dillo("=" * 92)
    _dillo("[H-NON-TRACCIATI] *** COMMIT RIFIUTATO: %s ***" % motivo)
    _dillo("  Sotto %s esistono file che git NON traccia e NON ignora."
           % " e ".join(SOTTO))
    _dillo("  ### Un file CITATO e non tracciato e' un RIFERIMENTO AL VUOTO: chi verifica")
    _dillo("  ###   dal repo lo cerca e NON LO TROVA. E' il caso `_sonda_scherm`.")
    for r in elenco[:40]:
        _dillo("      %s" % r)
    if len(elenco) > 40:
        _dillo("      ... e altri %d" % (len(elenco) - 40))
    _dillo("  CHE FARE: committarli, oppure ignorarli in `.gitignore` col motivo,")
    _dillo("    oppure -- se un run li sta SCRIVENDO ADESSO -- dichiarare A INIZIO RIGA:")
    _dillo("      %s <motivo>]" % USCITA)
    _dillo("    e committarli A RUN CHIUSO.")
    _dillo("=" * 92)
    return 1


if __name__ == "__main__":
    sys.exit(principale())
