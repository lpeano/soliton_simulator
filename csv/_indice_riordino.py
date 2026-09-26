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
    # ⚠ TRE REGOLE CITATE DAI HOOK E MAI ENTRATE NELL'INDICE: le ha trovate il controllo `C5`
    #   del riordino. Un nome che un presidio stampa e che l'indice non conosce e' un nome che
    #   nessuno puo' risolvere -- e' il difetto che l'indice esiste per curare.
    ("P1-bis", "LA RELAZIONE SI SCRIVE NELLO STESSO COMMIT DEL RISCONTRO", "CLAUDE.md par.4",
     "presidio",
     "col riordino del 2026-09-26 ha ASSORBITO `P1-bis-bis`, `par.5-ter`, `par.5-sexies` e "
     "`par.5-octies` in una regola sola: tutto cio' che si dice a Luca va nel repo nello "
     "stesso giro. Il PRESIDIO del hook che portava questo nome ora e' `H-P1-bis`."),
    ("P1-quater", "OGNI SOSTITUZIONE DI TESTO SI ASSERISCE PER SE', MAI IN BLOCCO",
     "CLAUDE.md par.11", "presidio",
     "contiene anche `L-PATCH` (patch in primo piano, niente escape nei patch script)."),
    ("P1-sexies", "UN CRITERIO SI COLLAUDA SU UN CASO A RISPOSTA NOTA, e il caso che DEVE "
                  "fallire e' il piu' importante", "doc/PATTERN_DI_PROVA.md", "standard",
     "col riordino del 2026-09-26 ha ASSORBITO `L-SOGLIA`: una soglia non si calcola dai dati "
     "che giudica. Spostata da `CLAUDE.md` al posto 2."),
    # i criteri LOCALI della misura 0 di `DRIVER-SCENA-II`: `M0b` e `M0c` esistevano come
    #   "citato, mai definito"; ora hanno una definizione e un referto.
    # i criteri LOCALI del sigillo di `OSSERVABILE-P1`, e sono la SOSTITUZIONE di un
    #   criterio dettato che si e' rivelato insoddisfacibile a passo 0.
    ("K2a", "SIGILLO osservabile-P1: si cambia SOLO `d` (un arco del cammino minimo x10) e la distanza DEVE cambiare", "csv/_seal_fork/_sigillo_osservabile_p1.py",
     "criterio-locale",
     "definito il 2026-09-27. Sostituisce, con `K2b`, il criterio dettato `L_d != L_pos`: quello NON e' soddisfacibile a passo 0, perche' `d` E' la distanza euclidea (`_allaccia` crea l'arco con `d = dd` dal KD-tree su `pos`). Misurato: L_d/L_pos = 1.000000 esatto."),
    ("K2b", "SIGILLO osservabile-P1: si cambia SOLO `pos` (un nodo di 10 LAM) e la distanza NON deve cambiare, esattamente", "csv/_seal_fork/_sigillo_osservabile_p1.py",
     "criterio-locale",
     "definito il 2026-09-27. E' la meta' NEGATIVA della coppia: isola la dipendenza da `d` invece di dedurla da due numeri diversi."),
    # i criteri LOCALI del sigillo di `DRIVER-SCENA-II`. `T1`..`T5` esistono gia' come
    #   etichette locali di altri sigilli; `T3a` e `T3b` no.
    ("T3a", "SIGILLO scena (ii): lo STESSO seme due volte da' byte IDENTICI -- 219 firme sha1 su 219", "csv/_seal_fork/_sigillo_scena_ii.py", "criterio-locale",
     "definito il 2026-09-26. Un processo per braccio (STANDARD 1), firme dei byte (STANDARD 2). E' la meta' che dimostra il DETERMINISMO."),
    ("T3b", "SIGILLO scena (ii): semi DIVERSI danno reti diverse -- 99 firme su 219 cambiano", "csv/_seal_fork/_sigillo_scena_ii.py", "criterio-locale",
     "definito il 2026-09-26. E' la meta' che dimostra che il seme MORDE: senza, `--seme` sarebbe un'opzione inerte e il criterio 3 passerebbe per costruzione."),
    ("M0a", "MISURA 0 di DRIVER-SCENA-II: `--nodi 0` NON e' rispettato -- net.n = 455 "
            "dopo `_applica_flag` con SEMINA_LAM", "csv/_test_fork/_misura0_scena_ii.py",
     "criterio-locale",
     "definito il 2026-09-26. Atteso scritto PRIMA nel task history: > 0. Misurato 455 "
     "(saturazione col seme 42). E' il termine di paragone del criterio 2 del sigillo."),
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
    ("D021", "ID SINTETICO del collaudo di `INDICE-LEGGERO`: esiste solo dentro un indice finto, per provare che `--cerca D02` NON lo trova. Non e' una voce del repo"),
    ("DE-DUPLICATI", "locuzione del testo (il conteggio dei titoli de-duplicati), non un identificatore"),
    ("INSIEME-INSIEME", "locuzione del testo: `distanza INSIEME-INSIEME` e' il nome di una misura in prosa, non un identificatore di difetto"),
    ("H-P", "pezzo del modello `ESENTE-H-P<n>` nei messaggi dei presidi, non un id"),
    ("H-Pn", "segnaposto del modello `ESENTE-<H-Pn>` nei messaggi dei presidi, non un id"),
    ("N-MASSE", "nome di una SCENA del simulatore (`TESTS`), non un identificatore di difetto"),
    ("MASSE-COERENTI", "nome di una SCENA del simulatore (`TESTS`), non un identificatore di difetto"),
    ("TERRA-BUCONERO", "nome di una SCENA del simulatore (`TESTS`), non un identificatore di difetto"),
    ("H-CLI", "nome SCARTATO: era la proposta di nome semantico per un presidio del hook, e Luca ha deciso il 2026-09-26 di tenere il nome vecchio col prefisso (H-P3, H-P5, ...). Si cita nei referti e nei commit come cosa NON scelta: non deve diventare una voce (RIORDINO-NOMI-H)"),
    ("H-CONFIG", "nome SCARTATO: era la proposta di nome semantico per un presidio del hook, e Luca ha deciso il 2026-09-26 di tenere il nome vecchio col prefisso (H-P3, H-P5, ...). Si cita nei referti e nei commit come cosa NON scelta: non deve diventare una voce (RIORDINO-NOMI-H)"),
    ("H-ANCORA", "nome SCARTATO: era la proposta di nome semantico per un presidio del hook, e Luca ha deciso il 2026-09-26 di tenere il nome vecchio col prefisso (H-P3, H-P5, ...). Si cita nei referti e nei commit come cosa NON scelta: non deve diventare una voce (RIORDINO-NOMI-H)"),
    ("A-B", "locuzione del testo (`max|A-B|`), non un identificatore"),
    ("U-U", "locuzione del testo (l'unitarieta' `U^dag U`), non un identificatore"),
]


# le voci DECISE da Luca: (id, stato, avanzamento, fonte_nuova|None, nota_da_aggiungere)
#   Idempotente: se la nota c'e' gia', la riga non si tocca.
DECISE = [
    ("RIORDINO-POSTO2", "chiuso", "FATTO", None,
     "CHIUSA il 2026-09-26, decisione di Luca: `STANDARD 10` ESCE dal posto 2 e va in "
     "`CLAUDE.md` par.9-ter, perche' e' il criterio con cui si sceglie fra CURE e non il "
     "metodo di una MISURA. Il posto 2 torna a 10 e IL TETTO NON SI ALZA. Misurato: "
     "la tabella `STANDARD` ha 10 righe su un tetto di 10."),
    ("RIORDINO-NOMI-H", "chiuso", "FATTO", None,
     "CHIUSA il 2026-09-26, decisione di Luca: si tengono `H-P3`, `H-P5`, ... com'e'. I nomi "
     "semantici della proposta (`H-CLI`, `H-CONFIG`, `H-ANCORA`) restano scartati."),
    # ⚠ QUESTA VOCE CAMBIA ANCHE `blocca_run_base`, e il validatore lo impone: `chiuso`
    #   con `blocca = SI` e' una contraddizione. Il criterio di chiusura era scritto in
    #   doc/REVISIONE_SI_2026-09-26.md e ora e' SODDISFATTO, punto per punto.
    ("OSSERVABILE-P1", "chiuso", "FATTO", "csv/_osservabile_p1.py",
     "CHIUSA il 2026-09-27. Il criterio era: un osservabile INVENTARIATO che, dati due insiemi di nodi, dia la distanza SUL GRAFO PESATO CON `d`, col collaudo su due masse a distanza nota. Soddisfatto: `csv/_osservabile_p1.py` (inventariato, blob 77b93d1b), pesi `net.d`, centro = medoide di grafo senza `pos`; sigillo 6/6 con il collaudo su grafi SINTETICI a distanza nota (errore 0.000e+00) invece che su due masse a distanza 'nota' che al passo 0 non e' nota ma MISURATA. K5 da' la barra fra semi: sd 0.146-0.510 su distanze ~10.7, cioe' 1.4-4.8 %."),
    ("DRIVER-SCENA-II", "chiuso", "FATTO", None,
     "CHIUSA il 2026-09-26. Il criterio era: UN COMANDO SOLO che produce la scena (ii)(a) in configurazione del driver, con UN SEME DICHIARATO, e UN COLLAUDO NEI DUE VERSI. Soddisfatto: `python csv/_test_fork/_scena_video.py 1 <dest> --scena=MASSE-COERENTI` (un comando); `--seme` inoltra `--seed` e `SEME_EFFETTIVO` lo legge da `a.seed` (seme dichiarato); sigillo 6/6 con i due versi su T1/T5 e su T3a/T3b (csv/_seal_fork/_sig_scena_ii/REFERTO.txt). net.n 0 -> 4256 col sep del driver, AST della scena INTATTO, 0 differenze su 79 booleani."),
    ("M0b", "chiuso", "FATTO", "csv/_test_fork/_misura0_scena_ii.py",
     "ORA DEFINITO (2026-09-26): la scena (ii) RIFIUTA una rete non vuota -- SystemExit "
     "«LA RETE HA GIA' 455 NODI». Era «citato, mai definito»."),
    ("M0c", "chiuso", "FATTO", "csv/_test_fork/_misura0_scena_ii.py",
     "ORA DEFINITO (2026-09-26): N-MASSE con SEMINA_LAM rifiuta -- SystemExit «SCENA DI "
     "EPOCA PRE-A13». E' il presidio che il criterio 5 del sigillo NON deve rompere."),
    ("STANDARD 10", "teoria", "FATTO", "CLAUDE.md par.9-ter",
     "USCITA DAL POSTO 2 il 2026-09-26, per decisione di Luca: vive in `CLAUDE.md` par.9-ter. "
     "Il posto 2 la RICHIAMA, non la copia."),
]


def leggi():
    t = io.open(FONTE, encoding="utf-8", newline="").read()
    righe = t.split(NL)
    return righe[0], [r for r in righe[1:] if r.strip()]


# le DECISIONI che restano a Luca: `stato = da-decidere`, e **col criterio di chiusura**, perche'
#   una voce senza criterio non e' un fronte, e' un desiderio (`CLAUDE.md` par.4).
APERTE = [
    ("RIORDINO-POSTO2", "IL POSTO 2 HA 11 REGOLE E IL TETTO E' 10: quale si fonde",
     "doc/PATTERN_DI_PROVA.md", "fronte",
     "CRITERIO DI CHIUSURA: Luca sceglie una delle tre candidate scritte in fondo a "
     "doc/PATTERN_DI_PROVA.md (STANDARD 10 -> CLAUDE.md par.11; P5 dentro STANDARD 3; "
     "P4 dentro P1-sexies), oppure alza il tetto dichiarandolo. NON scelgo io: la fusione "
     "che Luca ha RIFIUTATO il 2026-09-26 era una di queste. Misurato: anche la proposta "
     "ne dava 12, non 10 -- quel numero era sbagliato in aritmetica."),
    ("FUGA-MULTIRIGA", "la via d'uscita di H-REG-R e H-P1-bis e' una regex SENZA re.S: una dichiarazione su PIU' RIGHE viene IGNORATA e il commit rifiutato lo stesso",
     "csv/_hook_fisica.py", "difetto",
     "CRITERIO DI CHIUSURA: `re.S` nelle due FUGA, piu' un caso di collaudo col messaggio su piu' righe in ciascuno dei due collaudi. Trovato il 2026-09-26 scrivendo un motivo su sette righe: e' lo STESSO difetto curato lo stesso giorno su `H-RIGHE`. `H-INDICE` non ce l'ha: usa un test di sottostringa, non una regex. Non curato dentro DRIVER-SCENA-II per `L-UN-PROMPT`."),
    ("H-REGR-LARGA", "H-REG-R associa una scheda per NOME DI FUNZIONE: scatta su qualunque modifica a `_applica_flag`, 450 righe che applicano TUTTI i flag",
     "csv/_hook_fisica.py", "da-decidere",
     "CRITERIO DI CHIUSURA: Luca decide se l'associazione va STRETTA (per legge toccata, non per nome citato nella scheda) o se il costo dell'eccezione dichiarata e' accettabile. Misurato il 2026-09-26: la cura di DRIVER-SCENA-II non tocca la scheda `tempo-proprio`, e il presidio l'ha chiesta comunque."),
    ("INDICE-LEGGERO", "l'indice pesa 169 KB e leggerlo intero non fa risparmiare contesto: serve un comando di interrogazione", "csv/_indice_id.py", "fronte",
     "CRITERIO DI CHIUSURA (mandato di Luca, 2026-09-27): `--cerca ID` (uguaglianza ESATTA, mai prefisso), `--aperti`, `--blocca SI`, `--famiglia X`, `--dettaglio ID`, `--testo PAROLA` (ricerca sul testo COMPLETO, troncamento SOLO in stampa); il validatore impone titolo_breve <= 100 caratteri e rifiuta due titoli brevi IDENTICI; una riga nella sezione 11 di CLAUDE.md; collaudo nei DUE versi. Da fare DOPO OSSERVABILE-P1."),
    ("FATTI-AVVIO", "la catena di AVVIO non ha un solo fatto in FATTI_dal_codice.md: _applica_flag, avvia_test, _massa, semina", "doc/FATTI_dal_codice.md", "fronte",
     "CRITERIO DI CHIUSURA: una sezione per ciascuna delle quattro funzioni, coi fatti LETTI DAL CODICE e la riga misurata dall'AST. Trovato il 2026-09-26 lavorando a DRIVER-SCENA-II: il mandato indicava i fatti di _applica_flag e _massa, e non esistono -- ne in FATTI_dal_codice.md ne in par.9 al tag. E' la catena che decide CON CHE MONDO PARTE OGNI RUN."),
    ("RIORDINO-NOMI-H", "il prefisso `H-` e' sui NOMI VECCHI (H-P3) e non sui nomi semantici "
                        "(H-CLI) che la proposta suggeriva",
     "CLAUDE.md par.12", "da-decidere",
     "CRITERIO DI CHIUSURA: Luca conferma `H-P3`/`H-P5`/... oppure chiede i nomi semantici. "
     "Ho letto alla lettera il suo `(H-P3, H-P5, ...)`, e la ragione in piu' e' che cosi' "
     "ogni citazione storica (`P5` in un referto del 25/9) resta leggibile. Si cambia "
     "rigirando csv/_rinomina_hook.py con le coppie nuove."),
]


def riga_nuova(i, titolo, fonte, tipo, nota, stato="teoria"):
    #  id alias titolo fonte stato blocca tipo famiglia stato_da avanzamento revisione motivo nota
    return TAB.join([i, ALIAS.get(i, ""), titolo, fonte, stato, "NO", tipo, "?", "",
                     "FATTO" if stato == "teoria" else "IN CODA", "", "", nota])


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
    for i, titolo, fonte, tipo, nota in NUOVE + [
            (a, b, c, ('fronte' if d == 'fronte' else 'altro'), e) for a, b, c, d, e in APERTE]:
        if i in presenti:
            gia += 1
            print("  gia' presente  %-14s (non la tocco)" % i)
            continue
        _ap = i in [x[0] for x in APERTE]
        corpo.append(riga_nuova(i, titolo, fonte, tipo, nota,
                                'da-decidere' if _ap else 'teoria'))
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
    # le DECISIONI di Luca: stato, avanzamento, fonte, e la nota che dice perche'
    dec = 0
    for i, stato, avanz, fonte, nota in DECISE:
        if i not in presenti:
            print("  ** non trovata, NON decisa: %s **" % i)
            saltate += 1
            continue
        c = corpo[presenti[i]].split(TAB)
        while len(c) < 13:
            c.append("")
        if nota in c[12]:
            print("  decisione gia' li' %-16s" % i)
            continue
        c[4], c[9] = stato, avanz
        if stato == "chiuso" and c[5] == "SI":
            c[5] = "NO"          # il validatore vieta `chiuso` + `blocca SI`
        if fonte:
            c[3] = fonte
        c[12] = (c[12] + "  " if c[12] else "") + nota
        corpo[presenti[i]] = TAB.join(c)
        dec += 1
        print("  DECISA         %-14s -> stato `%s`" % (i, stato))
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
