# -*- coding: utf-8 -*-
"""**`H-LANCIATORI` -- UN LANCIATORE NUOVO, O UNA MODIFICA AL LANCIATORE, VUOLE LA RIGA DI LUCA CON L'ORA.** *(DECISIONE DI LUCA, 2026-11-24 13:30, [M1330-D1]; la regola [M2145] di `CLAUDE.md` par. 2: "Gestione (lanciatori, code, script di controllo, ...) NON esiste senza una riga di Luca con l'ora")*

> ### `A9` -- la regola era SCRITTA, e il 2026-11-23 ho fatto nascere un lanciatore bis
> ### (`coda_m1446_bis.py`) di mia iniziativa: una regola scritta non impedisce. Questo si'.

**STA IN `commit-msg`** *(come `H-RIGHE`: in `pre-commit` il messaggio non esiste ancora)*.

**CHE COSA RIFIUTA:** un commit il cui diff staged contiene **(a)** un file NUOVO *(stato `A`)* in
`doc/referti_l2/` il cui nome comincia per `coda_`, `lancia_` o `dispatcher_`, **o (b)** una
modifica *(stato `M`)* a `doc/referti_l2/coda_m1446.py` -- **SENZA** che il messaggio citi
**`DECISIONE DI LUCA (hh:mm)`** *(le parentesi e l'ora a due cifre dopo i due punti)*.
**Le voci della coda** *(`coda_m1446.json`)* **non sono un lanciatore** e non le guarda.

**NESSUNA VIA D'USCITA:** la via d'uscita E' la riga di Luca.

    python csv/_presidio_lanciatori.py --controlla MSGFILE   # dal hook commit-msg
    python csv/_presidio_lanciatori.py --collaudo            # i casi noti, in un repo di prova

ASCII puro nel codice.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge il diff staged e il messaggio.

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
CARTELLA = "doc/referti_l2/"
PREFISSI = ("coda_", "lancia_", "dispatcher_")
LANCIATORE = "doc/referti_l2/coda_m1446.py"
FRASE = re.compile(r"DECISIONE DI LUCA \(\d{1,2}:\d{2}\)")


def toccati(radice):
    """### `[(stato, percorso)]` del diff staged che il presidio guarda."""
    q = subprocess.run(["git", "diff", "--cached", "--name-status", "--no-renames"], cwd=radice, capture_output=True)
    fuori = []
    for riga in q.stdout.decode("utf-8", "replace").splitlines():
        parti = riga.split("\t")
        if len(parti) < 2:
            continue
        st, p = parti[0][:1], parti[-1].replace("\\", "/")
        nome = p.rsplit("/", 1)[-1]
        if st == "A" and p.startswith(CARTELLA) and "/" not in p[len(CARTELLA):] and nome.startswith(PREFISSI):
            fuori.append((st, p))
        elif st == "M" and p == LANCIATORE:
            fuori.append((st, p))
    return fuori


def decidi(radice, messaggio):
    """### `(codice, testo)`: `0` passa, `1` rifiuta."""
    t = toccati(radice)
    if not t:
        return 0, ""
    if FRASE.search(messaggio):
        return 0, "[H-LANCIATORI] %d lanciatori toccati, la riga di Luca c'e': %s\n" % (len(t), FRASE.search(messaggio).group(0))
    return 1, ("[H-LANCIATORI] RIFIUTATO: il commit tocca %s SENZA 'DECISIONE DI LUCA (hh:mm)' nel messaggio. "
               "Un lanciatore nuovo o una modifica al lanciatore NON esiste senza una riga di Luca con l'ora "
               "(CLAUDE.md par. 2, [M2145]).\n" % ", ".join("%s %s" % x for x in t))


def controlla(f_msg):
    with open(f_msg, encoding="utf-8", errors="replace") as fh:
        m = fh.read()
    q = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True)
    radice = q.stdout.decode("utf-8", "replace").strip() or RADICE
    cod, testo = decidi(radice, m)
    (sys.stderr if cod else sys.stdout).write(testo)
    return cod


def collaudo():
    """### i casi noti con COMMIT VERI in un repo di prova, col hook `commit-msg` che chiama QUESTO file:
    (1) coda_prova.py senza la frase: RIFIUTATO; (2) con la frase: ENTRA; (3) lancia_ e dispatcher_ senza: RIFIUTATO;
    (4) coda_m1446.py modificato senza: RIFIUTATO; (5) con (9:05): ENTRA; (6) un file qualunque senza: ENTRA;
    (7) coda_m1446.json modificato senza: ENTRA; (8) la frase senza parentesi: RIFIUTATO."""
    d = tempfile.mkdtemp(prefix="h_lanciatori_")
    ok = []
    try:
        def g(*a, controlla_=True):
            return subprocess.run(["git"] + list(a), cwd=d, capture_output=True, check=controlla_)
        g("init", "-q")
        g("config", "user.email", "prova@prova")
        g("config", "user.name", "prova")
        os.makedirs(os.path.join(d, "doc", "referti_l2"))
        ganci = d + "_ganci"
        os.makedirs(ganci)
        for nome in ("coda_m1446.py", "coda_m1446.json"):
            open(os.path.join(d, "doc", "referti_l2", nome), "w").write("x\n")
        g("add", "-A")
        g("commit", "-q", "-m", "base")
        py = sys.executable.replace("\\", "/")
        me = os.path.abspath(__file__).replace("\\", "/")
        # ### il hook di prova sta FUORI dal repo di prova: dentro, `git clean` lo cancellava a ogni caso
        # ### (la prima stesura del collaudo, mai committata: 5 casi su 8 falliti per questo)
        open(os.path.join(ganci, "commit-msg"), "w", newline="\n").write('#!/bin/sh\n"%s" "%s" --controlla "$1" || exit 1\n' % (py, me))
        g("config", "core.hooksPath", ganci.replace("\\", "/"))

        def caso(che, scrivi, msg, entra):
            g("reset", "-q", "--hard")
            g("clean", "-qfd")
            prima = g("rev-parse", "HEAD").stdout.strip()
            for p, t in scrivi:
                open(os.path.join(d, *p.split("/")), "w").write(t)
            g("add", "-A")
            assert g("diff", "--cached", "--quiet", controlla_=False).returncode == 1, "il caso %r non ha niente in stage: il collaudo e' mal costruito" % che
            fm = os.path.join(d, "..", os.path.basename(d) + "_msg.txt")
            open(fm, "w", encoding="utf-8").write(msg + "\n")
            q = g("commit", "-q", "-F", fm, controlla_=False)
            os.remove(fm)
            dopo = g("rev-parse", "HEAD").stdout.strip()
            e = dopo != prima
            ok.append(e == entra)
            print("  DEVE: %-80s %s (il commit %s; atteso %s)" % (che, "PASSA" if e == entra else "### FALLISCE", "ENTRATO" if e else "RIFIUTATO", "ENTRA" if entra else "RIFIUTATO"))
            if not e and q.stderr:
                print("        il hook: %s" % q.stderr.decode("utf-8", "replace").strip()[:160])
        caso("coda_prova.py nuovo SENZA la frase", [("doc/referti_l2/coda_prova.py", "y\n")], "un commit qualunque", False)
        caso("coda_prova.py nuovo CON la frase", [("doc/referti_l2/coda_prova.py", "y\n")], "DECISIONE DI LUCA (13:30): il lanciatore", True)
        caso("lancia_x.py e dispatcher_y.py nuovi SENZA", [("doc/referti_l2/lancia_x.py", "y\n"), ("doc/referti_l2/dispatcher_y.py", "y\n")], "niente", False)
        caso("coda_m1446.py modificato SENZA", [("doc/referti_l2/coda_m1446.py", "z\n")], "niente", False)
        caso("coda_m1446.py modificato CON (9:05)", [("doc/referti_l2/coda_m1446.py", "z\n")], "x DECISIONE DI LUCA (9:05) y", True)
        caso("un file qualunque nuovo in referti_l2 SENZA", [("doc/referti_l2/fondo_x.py", "y\n")], "niente", True)
        caso("coda_m1446.json modificato (le voci) SENZA", [("doc/referti_l2/coda_m1446.json", "z\n")], "niente", True)
        caso("la frase SENZA le parentesi (DECISIONE DI LUCA 13:30)", [("doc/referti_l2/coda_altra.py", "y\n")], "(DECISIONE DI LUCA 13:30)", False)
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(d + "_ganci", ignore_errors=True)
    print("### %d casi: %d PASSANO, %d FALLISCONO" % (len(ok), sum(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


def main(argv):
    if argv[:1] == ["--controlla"] and len(argv) == 2:
        return controlla(argv[1])
    if argv[:1] == ["--collaudo"]:
        return collaudo()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
