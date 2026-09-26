# -*- coding: utf-8 -*-
"""**`H-RIGHE` — `CLAUDE.md` NON PASSA LE 400 RIGHE.** *(mandato di Luca 2026-09-26, punto `h`)*

> ### `A9` — UN PRESIDIO CHE NON IMPEDISCE NON E' UN PRESIDIO.
> Il riordino del 2026-09-26 ha portato `CLAUDE.md` da **1575** righe a poco piu' di trecento.
> **Senza un presidio ricresce**, e non di colpo: **due righe alla volta**, ognuna giustificata.
> Qui il commit **viene rifiutato**.

**STA IN `commit-msg`, NON IN `pre-commit`, E NON E' UN DETTAGLIO.** La via d'uscita dichiarata
si scrive **nel messaggio**, e in `pre-commit` il messaggio **non esiste ancora** (git lo scrive
dopo): leggere `.git/COMMIT_EDITMSG` la' significa leggere **il commit PRECEDENTE**, cioe'
spegnere il presidio per sempre alla prima eccezione. *(E' lo stesso difetto che il collaudo
end-to-end ha trovato su `H-INDICE`.)*

**CHE COSA GUARDA:** il `CLAUDE.md` che **sara'** a `HEAD` dopo questo commit — la versione
**staged** se il file e' nel commit, altrimenti quella di `HEAD`. Cosi' dice la verita' anche
quando il commit non lo tocca.

**LA VIA D'USCITA, che obbliga a dichiarare:**   `[CLAUDE-OLTRE-400: <motivo>]` nel messaggio.

**COLLAUDO** (`P1-sexies`): `--collaudo` prova **QUATTRO** casi a risposta NOTA, **nei due versi**
— e il caso che **DEVE bloccare** e' il piu' importante.

    python csv/_presidio_righe.py            # la misura di oggi
    python csv/_presidio_righe.py --collaudo # i quattro casi sintetici

ASCII puro.
"""
import io
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Conta le righe di un documento.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FILE = "CLAUDE.md"
LIMITE = 400
# ❌ `re.S` AGGIUNTO AL PRIMO USO VERO, 2026-09-26: senza, la via d'uscita **non attraversava le
#   righe**, e una dichiarazione scritta su tre righe -- come si scrive un motivo che vale la pena
#   di leggere -- **veniva ignorata e il commit rifiutato lo stesso**. Il collaudo non l'aveva
#   preso perche' i suoi quattro casi avevano il messaggio su UNA riga: **il caso sintetico era
#   piu' povero del caso reale.** Ora c'e' anche quello (`dichiarato_su_piu_righe`).
FUGA = re.compile(r"\[CLAUDE-OLTRE-400:\s*(.+?)\]", re.I | re.S)


def _git(*a):
    q = subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True)
    return q.returncode, q.stdout.decode("utf-8", "replace")


def testo_da_giudicare():
    """Il `CLAUDE.md` che SARA' a HEAD: lo staged se e' nel commit, altrimenti quello di HEAD."""
    c, fuori = _git("diff", "--cached", "--name-only", "--diff-filter=ACM")
    if c == 0 and FILE in [r.strip().replace(chr(92), "/") for r in fuori.split(NL)]:
        c2, t2 = _git("show", ":" + FILE)
        if c2 == 0:
            return t2, "staged"
    c3, t3 = _git("show", "HEAD:" + FILE)
    if c3 == 0:
        return t3, "HEAD"
    try:
        return io.open(os.path.join(RADICE, FILE), encoding="utf-8").read(), "disco"
    except Exception:
        return "", "assente"


def conta(testo):
    """Le righe del documento: come le conta `wc -l`, cioe' i fine-riga."""
    return testo.count(NL) + (1 if testo and not testo.endswith(NL) else 0)


def giudica(n, msg):
    """`(codice, testo)`. Codice 1 = commit rifiutato."""
    if n <= LIMITE:
        return 0, ""
    m = FUGA.search(msg or "")
    if m:
        return 0, "[H-RIGHE] eccezione DICHIARATA: %s" % m.group(1).strip() + NL
    return 1, (NL + "[H-RIGHE] *** COMMIT RIFIUTATO: `%s` ha %d righe, il tetto e' %d. ***"
               % (FILE, n, LIMITE) + NL + NL
               + "  `CLAUDE.md` e' il FLUSSO DI LAVORO, e basta. Il resto ha gia' un posto:" + NL
               + "    gli assiomi      -> doc/ASSIOMI.md" + NL
               + "    il metodo        -> doc/PATTERN_DI_PROVA.md" + NL
               + "    i fatti          -> doc/FATTI_dal_codice.md" + NL
               + "    lo stato         -> doc/INDICE_ID.tsv, doc/STATO_RUN.md" + NL
               + "    la storia        -> doc/STORIA_REGOLE.md" + NL + NL
               + "  CHE FARE: spostare, non accorciare a forza -- oppure dichiarare" + NL
               + "    [CLAUDE-OLTRE-400: <motivo>] nel messaggio del commit." + NL + NL)


def controlla(msg):
    t, da = testo_da_giudicare()
    if da == "assente":
        return 0, "[H-RIGHE] %s non trovato: il controllo NON e' girato." % FILE + NL
    return giudica(conta(t), msg)


# ============================================================================== IL COLLAUDO
#   quattro casi a risposta NOTA, nei DUE versi. Il caso che DEVE bloccare e' il piu' importante.
CASI = [
    ("sotto_il_tetto", LIMITE - 1, "", False),
    ("sul_confine", LIMITE, "", False),
    ("oltre_il_tetto", LIMITE + 1, "messaggio qualunque", True),
    ("oltre_ma_dichiarato", LIMITE + 1, "cura X [CLAUDE-OLTRE-400: mandato di Luca]", False),
    # il caso che il collaudo NON aveva, e che il primo uso vero ha trovato: la dichiarazione
    #   scritta su piu' righe. Senza `re.S` questo caso BLOCCA, cioe' la via d'uscita non esiste.
    ("dichiarato_su_piu_righe", LIMITE + 1,
     "cura X" + NL + NL + "[CLAUDE-OLTRE-400: il motivo sta" + NL + "su tre righe," + NL
     + "come un motivo vero]" + NL, False),
]


def collaudo():
    print("=" * 96)
    print("COLLAUDO DI `H-RIGHE` -- quattro casi a risposta NOTA, nei DUE versi (`P1-sexies`)")
    print("=" * 96)
    ok = True
    for nome, n, msg, deve_bloccare in CASI:
        codice, _t = giudica(n, msg)
        blocca = bool(codice)
        buono = (blocca == deve_bloccare)
        ok = ok and buono
        print("  %-20s righe %4d  atteso %-7s ottenuto %-7s %s"
              % (nome, n, "BLOCCA" if deve_bloccare else "passa",
                 "BLOCCA" if blocca else "passa", "OK" if buono else "!! SBAGLIATO"))
    print()
    print("COLLAUDO: %s" % ("%d/%d OK" % (len(CASI), len(CASI)) if ok else "FALLITO"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--collaudo" in sys.argv[1:]:
        sys.exit(collaudo())
    t, da = testo_da_giudicare()
    n = conta(t)
    print("%s: %d righe (fonte: %s), tetto %d -> %s"
          % (FILE, n, da, LIMITE, "OK" if n <= LIMITE else "OLTRE IL TETTO"))
    sys.exit(0 if n <= LIMITE else 1)
