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
    ("H-P9", "PRESIDIO DEL HOOK: uno strumento che fa avanzare una rete con net.step() invece di passo_pieno", "csv/_hook_presidi.py", "presidio",
     "nato il 2026-09-27 (mandato di Luca). Nasce da PASSO-1: 25 strumenti caduti su «net.step() non e' un passo», e il 25esimo era il sigillo di D32 -- dove mitosi() girava ZERO volte in 14 giri e la byte-identita' certificava codice MAI ESEGUITO. E la mia correzione aveva ricopiato le cinque chiamate a mano: il 26esimo posto in cui quell'ordine vive cablato. Il nome e' `H-P9` perche' la regex delle esenzioni accetta gia' `ESENTE-H-P<cifra>`. Le cinque chiamate NON sono ricopiate nel hook: si leggono da `_passo.ordine()`. Collaudo 10/10 nei due versi. ARRETRATO misurato: 26 file su 370."),
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
    ("DE-INDENTARE", "verbo della prosa (togliere indentazione), non un identificatore"),
    ("D021", "ID SINTETICO del collaudo di `INDICE-LEGGERO`: esiste solo dentro un indice finto, per provare che `--cerca D02` NON lo trova. Non e' una voce del repo"),
    ("DE-DUPLICATI", "locuzione del testo (il conteggio dei titoli de-duplicati), non un identificatore"),
    ("INSIEME-INSIEME", "locuzione del testo: `distanza INSIEME-INSIEME` e' il nome di una misura in prosa, non un identificatore di difetto"),
    ("H-P", "pezzo del modello `ESENTE-H-P<n>` nei messaggi dei presidi, non un id"),
    ("H-Pn", "segnaposto del modello `ESENTE-<H-Pn>` nei messaggi dei presidi, non un id"),
    ("ESENTE-H-P9", "marcatore di esenzione al presidio H-P9, non un identificatore"),
    ("ESENTE-H-P", "pezzo del marcatore `ESENTE-H-P<n>`, non un identificatore"),
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
    ("CURA2-STRUTTURALE", "chiuso", "FATTO", "doc/REGISTRO_FISICA.md::tempo-nella-mitosi",
     "CHIUSA il 2026-09-27. Sei passi fatti: tag `pre-cura2-strutturale` (blob dd4f5ccf); archivio csv/_archivio/rami_off_cura2.py (4 rami, 13 righe, copiate dal sorgente); riga RAMI-OFF-CURA2; rimozione dei QUATTRO rami else per AST (0 rimasti); sigillo 4/4 (C1 byte-identici col flag acceso, 214 campi 0 diversi su 2 semi; C2 il caso che DEVE fallire -- al tag col flag spento 116 campi DIVERSI, quindi i rami FACEVANO qualcosa; C3 driver 0 differenze su 79 booleani; C4 la mitosi ha girato, taupp_tot 5.66e6); schede `tempo-nella-mitosi`, `tempo-proprio` e `mitosi-schwinger` aggiornate. FORMA DEL FLAG: costante True che RESTA booleano di modulo (cosi' H-P5 la enumera), opzione CLI accettata come NO-OP dichiarato che AVVISA, assegnazione tolta da _applica_flag, e NESSUN `--senza-` perche' il braccio OFF vive al tag e non in un flag."),
    ("D02", "chiuso", "FATTO", "doc/REGISTRO_FISICA.md::gravita-bifase",
     "CHIUSO il 2026-09-27, decisione di Luca dopo W5: `POZZO_D` e' ACCESO NEL DRIVER. `pozzo_grafo` prendeva `L` da `self.pos` (IL DISEGNO) e il risultato entra nella spinta S09, mentre il suo docstring dichiarava «la distanza REALE dell'arco». Cura: `L = self.d[mask]`, e il pavimento 1e-9 esce dal ramo acceso coi `d <= 0` CONTATI. Sigillo 4/4: W1 byte-identico a flag spento (214 campi, 0 diversi); W2 la spinta cambia (max|dpozzo| 1.07e-01 a 12 passi); W3 zero `d <= 0` su 6.1e6 archi e 4 semi, min(d) 0.8000377 contro LAM 0.8; W4 IL CASO CHE DEVE FALLIRE -- muovendo SOLO `pos` il pozzo non cambia di un bit (0.000000e+00) e a flag spento cambia di 5.38e+02. W5 (A/B, 4 semi, 120 passi): effetto NON MISURATO, IC95 contengono lo zero, limite 1.3-2.7 %. E' una scelta DI PRINCIPIO -- A3-DISEGNO, non A13 -- e A3-DISEGNO basta da sola: si misura per promuovere, si DIMOSTRA per escludere."),
    ("POZZO-D", "chiuso", "FATTO", "doc/REGISTRO_FISICA.md::gravita-bifase",
     "ACCESA NEL DRIVER il 2026-09-27 (decisione di Luca). Il flag resta nel codice come braccio di confronto: e' una CURA accesa dal driver, non una promozione a default nel sorgente (par.10). Sigillo 4/4, A/B W5 a 4 semi."),
    ("ETICHETTA-A13", "chiuso", "FATTO", None,
     "CHIUSA il 2026-09-27. Corretti: doc/TASK_HISTORY/2026-09-27_d02-pozzo-d.md, doc/REGISTRO_FISICA.md (scheda 3), il commento del flag POZZO_D, la nota DENTRO la cura (:6571) e l'HELP del CLI (:9007) in soliton_simulator.py, piu' le due citazioni in csv/_osservabile_p1.py. Le due nel codice sono arrivate DOPO, perche' il run A/B di W5 importava quei file e par.5 lo vieta. NE AVEVO MANCATE DUE (:6571 e :9007, l'help che l'utente legge): le ha trovate un ricontrollo dei residui, non la sostituzione. Sigillo POZZO-D rigirato 4/4 INVARIATO. RESTA: la revisione (righe 55 e 76) porta ancora A13 ed e' l'ORIGINE dell'errore, ma e' un reperto datato e testo di Luca -- decide lui."),
    ("D32", "chiuso", "FATTO", "doc/REGISTRO_FISICA.md::tempo-proprio",
     "CHIUSO il 2026-09-27, decisione di Luca: il tempo proprio del sistema e' `r` (e `dt_e` sull'arco); `d/cs` e' il TEMPO-LUCE, grandezza diversa e legittima; e `tau_pp` non e' un tempo affatto -- e' una POSIZIONE sull'asse della torsione, rinominata `pos_torsione`. I tre «tempi propri» erano TRE GRANDEZZE: il difetto non era che fossero diverse, era che si chiamassero allo stesso modo. VERIFICATO DAL SORGENTE (AST): col flag TEMPO_UNICO_MITOSI acceso gli usi come tempo sono ZERO nel ramo che gira, e 2 nel ramo else, PROPOSTI per la rimozione. Sigillo 5/5 (byte-identico, 214 campi, 0 diversi, e N5 prova che il codice rinominato HA girato). Z117, il pavimento del ritmo, resta APERTA a parte."),
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
    ("RAMI-OFF-CURA2", "i rami a flag spento di TEMPO_UNICO_MITOSI, archiviati COPIATI dal sorgente", "csv/_archivio/rami_off_cura2.py", "altro",
     "TAG: pre-cura2-strutturale (commit 8e3cf9c, blob del simulatore dd4f5ccf, sha1 byte grezzi). ARCHIVIO: csv/_archivio/rami_off_cura2.py -- QUATTRO rami, 13 righe di codice, ciascuno con funzione, righe al tag, cosa faceva, perche' e' uscito e il comando per rilanciarlo. Si rilancia con: git cat-file -p pre-cura2-strutturale:soliton_simulator.py scritto in BINARIO (git checkout riscriverebbe le newline, par.5-quinquies). Nulla si perde: l'archivio non si importa e non gira."),
    ("PASSO-PIENO", "un hook che rifiuta uno script che avanza con net.step() invece di csv/_passo.py passo_pieno", "csv/_passo.py", "presidio",
     "MANDATO di Luca, 2026-09-27, IN CODA dopo CURA2-STRUTTURALE. Il sigillo di D32 e' il 25esimo strumento caduto su PASSO-1 (net.step() non e' un passo), E LA MIA CORREZIONE HA RICOPIATO LE CINQUE CHIAMATE A MANO invece di usare csv/_passo.py passo_pieno -- che ESISTE, e il cui docstring dice l'UNICO modo di avanzare in una sonda, e che legge l'ordine DAL CODICE cosi' non scade. Ho curato il sintomo con una copia cablata. TRE PASSI: (1) hook che rifiuta uno script nuovo o modificato sotto csv/ che avanzi con net.step() senza passo_pieno o le cinque chiamate, con via d'uscita dichiarata per chi misura il solo step, collaudato nei due versi; (2) il sigillo di D32 passa a passo_pieno, byte-identici col giro appena fatto; (3) la voce IMPL-2. CRITERIO DI CHIUSURA: il hook rifiuta e il collaudo passa nei due versi."),
    ("IMPL-2", "una SECONDA implementazione indipendente, scritta dalle LEGGI e non dal codice", "doc/VALUTAZIONE_go.md", "fronte",
     "MANDATO di Luca, 2026-09-27, DOPO IL RUN BASE. Serve a verificare che la gravita' NON DIPENDA DA UN BUG: un secondo programma scritto dalle SCHEDE DI REGISTRO_FISICA (le leggi), non dal sorgente Python, che riproduca le tre prove. E' la ragione per cui una riscrittura in Go avrebbe senso -- ma DOPO, con un termine di paragone vero, non PRIMA come sostituzione (doc/VALUTAZIONE_go.md). CRITERIO DI CHIUSURA: la seconda implementazione riproduce il segno e l'ordine di grandezza delle tre prove partendo dalle sole schede; se NON li riproduce, dice che una delle due dipende da un dettaglio non dichiarato -- ed e' un riscontro, non un fallimento."),
    ("RISCRITTURA-GO", "riscrivere il simulatore in Go: valutato, NON deciso", "doc/VALUTAZIONE_go.md", "da-decidere",
     "DOMANDA di Luca, 2026-09-27. Valutazione in doc/VALUTAZIONE_go.md. Misurato: 10 592 righe, 1754 chiamate numpy, e 122 script su 361 (34 percento) dipendono dall'INTROSPEZIONE di Python (doppio import dello stesso modulo, exec del testo del driver, vars(S), monkeypatch, AST) -- cioe' i PRESIDI. Una riscrittura NON puo' essere byte-identica, quindi ogni sigillo si ristabilisce da zero e ogni numero cambia epoca (par.9-bis). E la velocita' non e' il collo di bottiglia: nessuno dei 6 SI e' il simulatore lento. CRITERIO DI CHIUSURA: un PROFILO che mostri il tempo concentrato in codice PYTHON e non in kernel C, per una frazione che giustifichi la riscrittura. Il profilo NON ESISTE."),
    ("CURA2-STRUTTURALE", "la CURA 2 diventa STRUTTURALE: i rami `else` di TEMPO_UNICO_MITOSI escono dal simulatore senza perderli", "soliton_simulator.py", "cura",
     "MANDATO di Luca, 2026-09-27, ricevuto mentre girava il sigillo di D32 e messo in coda come lui ha chiesto. SEI PASSI, un commit ciascuno: (1) tag `pre-cura2-strutturale`; (2) archivio csv/_archivio/rami_off_cura2.py coi rami COPIATI, e per ciascuno funzione, riga, cosa faceva, perche' e' uscito, il tag da cui si rilancia; (3) la riga `RAMI-OFF-CURA2` nell'indice; (4) rimozione dei rami e forma del flag che non rompe P5; (5) sigillo committato prima: byte-identici col flag ACCESO (2 semi) piu' il caso che DEVE fallire (al tag, flag SPENTO, byte DIVERSI); (6) la scheda dice «strutturale dal <commit>». CRITERIO DI CHIUSURA: i sei passi fatti, e il sigillo PASS."),
    ("W5", "CRITERIO di POZZO-D: A/B nel driver, scena (ii)(a), 4 semi, 120 passi, con la barra fra semi", "doc/TASK_HISTORY/2026-09-27_d02-pozzo-d.md", "criterio-locale",
     "definito il 2026-09-27. La distanza fra le masse si misura con csv/_osservabile_p1.py, flag ON contro OFF, e la barra e' quella FRA SEMI (P3, almeno 4). Il nullo non e' zero: al passo 0 la sd fra semi vale 0.146-0.510 su distanze ~10.7, cioe' 1.4-4.8 percento -- un effetto piu' piccolo di quello NON SI LEGGE. Giro corto: 120 passi, nessun run lungo."),
    ("FILI-CORTI", "i fili si accorciano SOLO FRA LE MASSE o OVUNQUE? Il calo della distanza viene dai `d`, non dalle nascite", "csv/_test_fork/_ab_pozzo_d/REFERTO.txt",
     "misura",
     "APERTA il 2026-09-27, dal RITIRO della mia spiegazione «piu' nodi = piu' scorciatoie». VERIFICATO DAL SORGENTE: la mitosi SOSTITUISCE l'arco (a,b) con (a,m),(m,b) lunghi d/2 (:6272, :6292-6293), quindi il cammino attraverso il figlio e' lungo QUANTO PRIMA -- le nascite NON accorciano il grafo. L'unico cammino nuovo e' lo Schwinger, che aggiunge un PARALLELO lungo 2*dd = ||pos_a - pos_b|| (:6368-6369, :6416): residuo A3-DISEGNO, ed e' scorciatoia SOLO SE 2*dd < d. Quindi l'avvicinamento viene dalle LUNGHEZZE DEI FILI. CRITERIO DI CHIUSURA: il pilota della PROVA 1 misura la distanza fra le masse E fra i punti di CONTROLLO nel vuoto; se calano ENTRAMBE allo stesso modo e' contrazione globale e NON e' gravita'; se cala solo fra le masse, e' specifico delle masse."),
    ("MASSA-MIGRA", "la massa segue i NODI o la COERENZA? E come cambia la sua FORMA?", "doc/TASK_HISTORY/2026-09-27_pilota-prova1.md", "misura",
     "MANDATO di Luca, 2026-09-27, DUE aggiunte al pilota della PROVA 1. (a) IL METRO SEGUE GLI STESSI NODI DEL PASSO 0, ma una massa e' una regione di COERENZA DI FASE, e la coerenza potrebbe migrare su nodi vicini -- un'onda che si sposta mentre l'acqua resta ferma. A ogni checkpoint (0/40/80/120) la regione si RIDEFINISCE DALLA FASE, col criterio che la scena (ii) usa, LETTO DAL CODICE; si riportano sovrapposizione col passo 0 e spostamento del medoide, e la distanza calcolata SIA sui nodi del passo 0 SIA sulle regioni attuali. CRITERI PRIMA: sovrapposizione >= 90 percento E spostamento del medoide < LAM -> la massa segue i nodi e il metro attuale basta; altrimenti LA MASSA MIGRA e la PROVA 1 va misurata sulle REGIONI. (b) LA FORMA: numero di nodi, raggio (distanza media dal medoide), quantili p10/p50/p90 delle distanze interne, e la coerenza (parametro d'ordine della fase); per ogni coppia, distanza fra i CENTRI e fra le SUPERFICI AFFACCIATE. CRITERIO: la forma e' costante se ogni grandezza resta entro la dispersione fra semi del passo 0; se le superfici si avvicinano PIU' dei centri oltre la barra si riporta un ALLUNGAMENTO (possibile effetto mareale) -- E' UN RISULTATO, non un difetto, e NON VA CORRETTO. Tutto sulle distanze lungo il grafo pesate con `d`, MAI `pos`. blocca NO finche' il pilota non dice di si'."),
    ("AB-CONTROLLI", "l'A/B di W5 non ha salvato i punti di CONTROLLO nel vuoto, e senza quelli la densificazione non si separa dall'attrazione", "csv/_test_fork/_ab_pozzo_d.py",
     "difetto",
     "TROVATO il 2026-09-27 leggendo W5. La distanza fra le masse CALA in ENTRAMBI i bracci (-0.45 a -0.89 su ~10.5, e 2 IC95 su 6 non contengono lo zero), ma nello stesso intervallo nascono ~640 nodi: piu' nodi = piu' scorciatoie = distanza di grafo piu' corta, MECCANICAMENTE. I due effetti con questi dati NON SI SEPARANO. La separazione esiste ed e' gia' scritta: i punti di CONTROLLO nel vuoto di csv/_osservabile_p1.py (criterio K4), che il mio braccio NON HA SALVATO -- ha registrato solo le coppie di masse. E' un difetto dello STRUMENTO, non del sistema. CRITERIO DI CHIUSURA: il braccio salva anche `controlli`, e l'A/B riporta la distanza delle masse MENO quella dei controlli -- cosi' la densificazione si cancella e resta cio' che e' specifico delle masse."),
    ("ETICHETTA-A13", "l'etichetta sbagliata `A13` dove la regola e' `A3-DISEGNO`: corretta nei documenti, non ancora nel codice", "doc/REVISIONE_SI_2026-09-26.md", "difetto",
     "RILIEVO DI LUCA, 2026-09-27. `A13` e' «LAM e' la scala di Planck del sistema»; la regola che dice «il disegno esce dalla dinamica: pos non entra nella fisica» e' `A3-DISEGNO`. CORRETTI: doc/TASK_HISTORY/2026-09-27_d02-pozzo-d.md e doc/REGISTRO_FISICA.md. NON ANCORA CORRETTI, e non per dimenticanza: il commento del flag in soliton_simulator.py e le due citazioni in csv/_osservabile_p1.py -- entrambi file che il run A/B di W5 STA IMPORTANDO, e par.5 vieta di modificare un file del percorso in uso mentre un run gira. L'ORIGINE E' LA REVISIONE STESSA (righe 55 e 76, testo di Luca): io l'ho PROPAGATA senza verificare cosa dicesse `A13` -- e' P1 applicato a un'etichetta. CRITERIO DI CHIUSURA: a run finito, le tre citazioni nel codice corrette; e Luca decide se la revisione -- che e' un reperto datato -- si annota o si lascia."),
    ("POZZO-D", "la cura di D02 (flag `POZZO_D` nel codice): nel pozzo del grafo `L` viene da `self.d` e non da `pos`", "soliton_simulator.py", "cura",
     "MANDATO di Luca, 2026-09-27, primo SI di FISICA della spinta. Criteri W1-W5 in doc/TASK_HISTORY/2026-09-27_d02-pozzo-d.md, committati PRIMA del codice. Spento di default. CRITERIO DI CHIUSURA: W1 byte-identico a flag spento; W2 la spinta S09 CAMBIA (riportato come RAPPORTO, non come «diversi»); W3 il contatore dei `d <= 0` a flag acceso e' 0 (e si CONTA, non si assume); W4 il caso che DEVE fallire -- con `pos` alterato a `d` costante il pozzo NON cambia a flag acceso e CAMBIA a flag spento; W5 A/B a 4 semi, 120 passi, con csv/_osservabile_p1.py e la barra fra semi. POI DECIDE LUCA se accenderla nel driver."),
    ("COLLAUDO-NON-ESEGUITO", "un collaudo che si RIFIUTA di girare esce con 2, e il controllo C4 lo conta come PASS", "csv/_controlli_riordino.py", "difetto",
     "TROVATO il 2026-09-27. `csv/_collaudo_istruzioni.py` fa `git add`, quindi si RIFIUTA di girare se c'e' qualcosa in STAGE -- e fa bene. Ma esce con 2, e `C4` di `_controlli_riordino.py` guarda `returncode == 0`: un 2 NON e' 0, quindi C4 lo dava per FAIL... e invece il file di output finiva nel repo dicendo «NON ESEGUITO», che SEMBRA un esito e non lo e'. Committato una volta cosi', e corretto rigirandolo su albero pulito (6/6). CRITERIO DI CHIUSURA: `_controlli_riordino.py` distingue i tre casi -- PASS, FAIL e NON ESEGUITO -- e un NON ESEGUITO non conta come PASS ne' come FAIL: conta come «il controllo non c'e' stato» (A9)."),
    ("D32-CONTATORE", "i contatori `_rep_taupp_*` contano un clamp che NON ESISTE PIU'", "soliton_simulator.py", "difetto",
     "APERTA il 2026-09-27. `_rep_taupp_clamp` conta `pos_torsione < 1e-12`, cioe' il clamp del ramo `else` che la CURA 2 strutturale ha TOLTO: ora conta un clamp che non esiste. RESTANO di proposito perche' servono alla byte-identita' (C1 confronta gli stessi campi) e a C4 (provano che la mitosi ha girato), e perche' sono REPERTI nei json (par.9). CRITERIO DI CHIUSURA: decidere se `_rep_taupp_clamp` si toglie (e allora C1 va rifatto contro un altro insieme di campi) o si rinomina in un contatore di INVOCAZIONI, che e' cio' che di fatto misura."),
    ("RITMO-PAVIMENTO", "IL PAVIMENTO DEL RITMO MORDE: min(r) = 1.414212e-06 e' ESATTAMENTE il pavimento, non un valore raggiunto", "doc/REGISTRO_FISICA.md::tempo-proprio", "difetto",
     "APERTA a parte per decisione di Luca, 2026-09-27, chiudendo D32. ⚠ E SERVIVA UNA VOCE PROPRIA: `Z117` nell'indice e' CHIUSO e riguarda IL WRAP a 4pi di ritmo() (cioe' D34), mentre REGISTRO_FISICA cita `Z117` anche per IL PAVIMENTO -- un ID per DUE cose, la stessa collisione che l'indice esiste per curare. CRITERIO DI CHIUSURA: dire se il pavimento e' un VINCOLO FISICO dichiarato o una DIFESA (`A11`): un nodo con f = 0 che tempo proprio ha? Zero e' una risposta fisica, 1.414e-6 e' un numero SCELTO."),
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
