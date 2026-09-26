# -*- coding: utf-8 -*-
"""**LE VOCI CHE IL RIORDINO DEL 2026-09-26 AGGIUNGE A `doc/INDICE_ID.tsv`.**

**Un ID e' una CHIAVE**, e il hook `H-INDICE` rifiuta un ID citato in un documento vivo che non
sia nell'indice. Il riordino ne introduce **due famiglie**:

* i **presidi dei hook col prefisso `H-`** *(punto `d` del mandato)*;
* le **regole di lavoro `L-`** dettate da Luca il 2026-09-26.

**E i NOMI VECCHI RESTANO**, con la riga `nota` che dice **in che cosa sono stati rinominati o
fusi**: *i reperti non si riscrivono* (`CLAUDE.md` par.9). Qui le vecchie righe **non si
cancellano**: si **annotano**.

**IDEMPOTENTE:** una voce gia' presente **non si duplica e non si sovrascrive**; lo script dice
quante ne ha aggiunte e quante ne ha trovate gia' li'.

    python csv/_indice_riordino.py --prova   # dice cosa farebbe
    python csv/_indice_riordino.py           # scrive

ASCII puro.
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Aggiunge righe a un TSV.

NL = chr(10)
TAB = chr(9)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FONTE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")

_R = "rinominato il 2026-09-26: il PRESIDIO del hook ha preso il prefisso `H-`, che dice " \
     "'lo impedisce una macchina'. Il nome nudo resta per i reperti."

# (id, titolo_breve, fonte_principale, tipo, nota)
NUOVE = [
    ("H-P3", "PRESIDIO DEL HOOK: un sigillo che configura il modulo A MANO invece di passare "
             "dal CLI", "csv/_hook_presidi.py", "presidio",
     "si chiamava `P3`, che era ANCHE la regola di metodo: due regole diverse con lo stesso "
     "nome. Collisione curata il 2026-09-26."),
    ("H-P5", "PRESIDIO DEL HOOK: un referto che non dichiara la configurazione INTERA",
     "csv/_hook_presidi.py", "presidio",
     "si chiamava `P5`, che era ANCHE la regola di metodo. Collisione curata il 2026-09-26."),
    ("H-P7", "PRESIDIO DEL HOOK: un flag il cui commento cambia senza nominare quel flag",
     "csv/_presidio_commenti_flag.py", "presidio", _R),
    ("H-P8", "PRESIDIO DEL HOOK: un confronto che prende il codice di prima da HEAD invece che "
             "dal PADRE", "csv/_hook_presidi.py", "presidio", _R),
    ("H-P1-bis", "PRESIDIO DEL HOOK: un referto committato senza toccare la relazione",
     "csv/_hook_relazione.py", "presidio",
     "si chiamava `P1-bis`, come la regola di flusso, e sono due cose diverse: il hook guarda "
     "i FILE toccati, la regola guarda tutto cio' che si dice a Luca."),
    ("H-REG-R", "PRESIDIO DEL HOOK: una legge che cambia senza la sua scheda in REGISTRO_FISICA",
     "csv/_hook_fisica.py", "presidio", _R),
    ("H-INDICE", "PRESIDIO DEL HOOK: un ID citato in un documento vivo o nel messaggio che non "
                 "e' nell'indice", "csv/_presidio_indice.py", "presidio", _R),
    ("H-VALIDATORE", "PRESIDIO DEL HOOK: un indice mal formato o con una voce persa rispetto "
                     "al tag", "csv/_indice_id.py", "presidio",
     "gira nel `pre-commit` dal 2026-09-26; non aveva un nome prima."),
    ("H-RIGHE", "PRESIDIO DEL HOOK: CLAUDE.md oltre le 400 righe", "csv/_presidio_righe.py",
     "presidio",
     "nato col riordino del 2026-09-26 (mandato di Luca, punto h). Collaudo 4/4 nei DUE versi. "
     "Sta in `commit-msg` perche' la via d'uscita [CLAUDE-OLTRE-400] vive nel MESSAGGIO."),
    ("L-NUMERI", "OGNI NUMERO SCRITTO IN UN COMMIT O IN UN REFERTO ESCE DA UNO SCRIPT",
     "CLAUDE.md par.11", "presidio",
     "regola di Luca, 2026-09-26. ASSORBE `P1-ter`, che lo diceva per le sole tabelle."),
    ("L-UN-PROMPT", "UN PROMPT ALLA VOLTA: i rilievi che arrivano durante un lavoro vanno in CODA",
     "CLAUDE.md par.11", "presidio", "regola di Luca, 2026-09-26."),
    ("L-DOPO-STOP", "DOPO UNO STOP, se Luca non risponde si lavora SOLO la coda: nessuna cura "
                    "fisica, nessun run lungo, nessuna decisione al suo posto",
     "CLAUDE.md par.11", "presidio", "regola di Luca, 2026-09-26."),
    ("L-PATCH", "LE PATCH SI LANCIANO IN PRIMO PIANO; niente git stash con una patch in corso; "
                "nei patch script niente escape, si usa chr() o replace",
     "CLAUDE.md par.11", "presidio",
     "regola di Luca, 2026-09-26. VIVE DENTRO `P1-quater`, che parla delle sostituzioni di "
     "testo: stesso oggetto, stesso posto, nessuna regola in piu'. La riga qui c'e' perche' "
     "l'ID e' CITATO, e un ID citato senza riga e' quello che `H-INDICE` rifiuta -- come ha "
     "fatto al commit 4/6."),
    ("L-SOGLIA", "UNA SOGLIA NON SI CALCOLA DAI DATI CHE GIUDICA, e si collauda sul caso nullo",
     "doc/PATTERN_DI_PROVA.md", "standard",
     "regola di Luca, 2026-09-26. FUSA dentro `P1-sexies` per decisione di Luca: e' il suo "
     "stesso presidio visto dal lato della soglia."),
    ("STANDARD 4", "SNAPSHOT CONTRO SNAPSHOT, ALLO STESSO ISTANTE", "doc/PATTERN_DI_PROVA.md",
     "standard", "FUSA dentro `STANDARD 3` il 2026-09-26: entrambe dicono CHE COSA si confronta "
     "con CHE COSA. Il nome resta per i reperti."),
    ("STANDARD 6", "OGNI DIFETTO ACCLARATO SI REGISTRA SUBITO NELLA CODA UNICA",
     "doc/INDICE_ID.tsv", "standard",
     "ASSORBITA dall'indice il 2026-09-26: un difetto nuovo E' una riga dell'indice, e il hook "
     "`H-INDICE` lo impedisce. Da regola di metodo a fatto meccanico."),
    ("STANDARD 8", "UN DIFETTO DIMOSTRATO SI CURA: MISURARE NON E' CURARE",
     "doc/ASSIOMI.md", "standard",
     "e' `A12` parola per parola: resta l'assioma, e `doc/PATTERN_DI_PROVA.md` lo RICHIAMA. "
     "Una regola in due posti e' una regola che si puo' aggiornare a meta'."),
]

# le righe VECCHIE che vanno annotate, non cancellate: (id, nota da aggiungere)
ANNOTA = [
    ("P3", "il PRESIDIO del hook che si chiamava `P3` ora e' `H-P3` (2026-09-26): questa riga "
           "e' la REGOLA DI METODO, che vive in doc/PATTERN_DI_PROVA.md e ha assorbito "
           "`P6` e `par.9-bis`."),
    ("P5", "il PRESIDIO del hook che si chiamava `P5` ora e' `H-P5` (2026-09-26): questa riga "
           "e' la REGOLA DI METODO, che vive in doc/PATTERN_DI_PROVA.md."),
    ("P6", "FUSA dentro `P3` il 2026-09-26 (un numero porta barra, seme, flag ed epoca)."),
    ("P7", "rinominata `H-P7` il 2026-09-26 (presidio del hook)."),
    ("P8", "rinominata `H-P8` il 2026-09-26 (presidio del hook)."),
    ("REG-R", "rinominata `H-REG-R` il 2026-09-26 (presidio del hook)."),
    ("P1", "resta in CLAUDE.md par.11 dopo il riordino del 2026-09-26."),
    ("P2", "resta in CLAUDE.md par.11 dopo il riordino del 2026-09-26."),
    ("P4", "resta SOLA in doc/PATTERN_DI_PROVA.md: Luca ha RIFIUTATO la fusione con `L-SOGLIA` "
           "il 2026-09-26."),
]


# l'ALIAS di chi ha una coda minuscola: la FORMA del presidio si ferma prima di `-bis`, quindi
#   `H-P1-bis` nella prosa si legge `H-P1`. E' lo stesso che gia' succede a `P1-bis` -> `P1`.
ALIAS = {"H-P1-bis": "H-P1"}

ESCLUSI = os.path.join(RADICE, "doc", "INDICE_ID_ESCLUSI.tsv")

# forme che la FORMA cattura e che NON sono identificatori: si dichiarano col motivo
NON_ID = [
    ("CLAUDE-OLTRE-400", "via d'uscita dichiarata del presidio `H-RIGHE`, non un identificatore"),
    ("DA-CLAUDE-MD-2026-09-26", "marcatore HTML dell'innesto del riordino, non un identificatore"),
    ("ESENTE-H-P5", "marcatore di esenzione ai presidi, non un identificatore"),
    ("UTF-8", "nome di una codifica, non un identificatore"),
    ("A-B", "locuzione del testo (`max|A-B|`), non un identificatore"),
    ("U-U", "locuzione del testo (l'unitarieta' `U^dag U`), non un identificatore"),
]


def leggi():
    t = io.open(FONTE, encoding="utf-8", newline="").read()
    righe = t.split(NL)
    return righe[0], [r for r in righe[1:] if r.strip()]


def riga_nuova(i, titolo, fonte, tipo, nota):
    #  id alias titolo fonte stato blocca tipo famiglia stato_da avanzamento revisione motivo nota
    return TAB.join([i, ALIAS.get(i, ""), titolo, fonte, "teoria", "NO", tipo, "?", "",
                     "FATTO", "", "", nota])


def esclusi(scrivi):
    """Le forme che NON sono id: si dichiarano, col motivo. Idempotente."""
    t = io.open(ESCLUSI, encoding="utf-8", newline="").read()
    righe = [r for r in t.split(NL) if r.strip()]
    gia = set(r.split(TAB)[0] for r in righe[1:])
    agg = 0
    for forma, motivo in NON_ID:
        if forma in gia:
            continue
        righe.append(TAB.join([forma, motivo, "0"]))
        agg += 1
    if scrivi and agg:
        io.open(ESCLUSI, "w", encoding="utf-8", newline=NL).write(NL.join(righe) + NL)
    return agg, len(righe) - 1


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    intest, corpo = leggi()
    presenti = dict((r.split(TAB)[0], k) for k, r in enumerate(corpo))
    print("=" * 92)
    print("VOCI DEL RIORDINO -> doc/INDICE_ID.tsv%s"
          % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)
    agg = gia = 0
    for i, titolo, fonte, tipo, nota in NUOVE:
        if i in presenti:
            gia += 1
            print("  gia' presente  %-14s (non la tocco)" % i)
            continue
        corpo.append(riga_nuova(i, titolo, fonte, tipo, nota))
        agg += 1
        print("  AGGIUNTA       %-14s %s" % (i, titolo[:54]))
    presenti = dict((r.split(TAB)[0], k) for k, r in enumerate(corpo))
    ann = saltate = 0
    for i, nota in ANNOTA:
        if i not in presenti:
            print("  ** non trovata, NON annotata: %s **" % i)
            saltate += 1
            continue
        c = corpo[presenti[i]].split(TAB)
        while len(c) < 13:
            c.append("")
        if nota in c[12]:
            print("  nota gia' li'  %-14s" % i)
            continue
        c[12] = (c[12] + "  " if c[12] else "") + nota
        corpo[presenti[i]] = TAB.join(c)
        ann += 1
        print("  ANNOTATA       %-14s" % i)
    # l'alias su una riga gia' presente (idempotente: se c'e' gia', non lo tocco)
    for i, al in ALIAS.items():
        if i not in presenti:
            continue
        c = corpo[presenti[i]].split(TAB)
        while len(c) < 13:
            c.append("")
        if al not in c[1].split(","):
            c[1] = (c[1] + "," if c[1] else "") + al
            corpo[presenti[i]] = TAB.join(c)
            print("  ALIAS          %-14s -> %s" % (i, al))
    n_esc, tot_esc = esclusi(scrivi)
    print("  ESCLUSI        %d forme nuove dichiarate (totale %d)" % (n_esc, tot_esc))
    print("  --------------------------------------------------")
    print("  aggiunte %d   gia' presenti %d   annotate %d   non trovate %d"
          % (agg, gia, ann, saltate))
    print("  voci totali dopo: %d" % len(corpo))
    if scrivi:
        io.open(FONTE, "w", encoding="utf-8", newline=NL).write(
            NL.join([intest] + corpo) + NL)
        print("  SCRITTO doc/INDICE_ID.tsv")
    sys.exit(1 if saltate else 0)
