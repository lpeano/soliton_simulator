# -*- coding: utf-8 -*-
"""PUNTO `0` DELLA SECONDA PARTE — **i metodi dell'era `1`, uno per uno, nell'era `2`.**

### ⛔ **IL PERIMETRO NON LO SCELGO IO: LO CALCOLA L'INDICE**, da ### **campi a
vocabolario chiuso** *(`classe in (STANDARD, PRESIDIO)`)*, piu' le ### **cure di
architettura** che il mandato nomina ### **per ID.**

### ⭐ **E IL PRESIDIO E' PIU' FORTE DI <<un metodo citato senza riga>>:** pretende
che ### **OGNI metodo del perimetro abbia una riga**, citato o no. ### **Cosi' una voce
`STANDARD` o `PRESIDIO` nuova, aggiunta domani, FA RIFIUTARE IL COMMIT** finche' non si
dice ### **come si applica all'era `2`** — e il documento ### **non puo' invecchiare
in silenzio.**

### ⚠ **LA COLONNA `stato` E' A VOCABOLARIO CHIUSO**, e il perche' e' il principio
del mandato: *«le decisioni si prendono SOLO da campi strutturati»*. ### **Una
colonna di prosa qui sarebbe la prosa che una macchina deve leggere** — cioe'
esattamente il difetto che questo mandato cura.
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
VOCI = os.path.join(RADICE, "doc", "indice", "voci.jsonl")
FUORI = os.path.join(RADICE, "doc", "METODI_era1_in_era2.md")

# ### ⛔ **IL VOCABOLARIO CHIUSO DI `stato`.**
# ### ⛔ **LA DICHIARAZIONE DELL-ID** *(punto `12(a)`)*: ### **un file, UN
# ### presidio**, quindi `PRESIDIO`. `P-C1` verifica che la voce esista e che
# ### abbia ### **`classe: PRESIDIO`** -- e la classe e- ### **un CAMPO.**
PRESIDIO = "P-M1"

STATI = ("PORTATO", "DA_PORTARE", "NON_SI_APPLICA", "DA_DECIDERE")

# ### Le CLASSI che fanno di una voce ### **un METODO.**
CLASSI_METODO = ("STANDARD", "PRESIDIO")

# ### Le ### **cure di architettura** che il mandato nomina per ID: non sono `STANDARD`
# ### ne' `PRESIDIO` *(sono `CURA`, `MISURA`, `DIFETTO`, `FRONTE`)*, e ### **il mandato le
# ### vuole comunque nel censimento.**
CURE_ARCHITETTURA = (
    "ETC-PASSO", "SCHED-PASSO", "SCHED-T1", "SCHED-T2-TIPI", "SCHED-T2-VALIDA",
    "SCHED-T3-REGOLE", "NASCITA-PUNTO-UNICO", "C5", "Z100",
    "VELENO-ARCHI-KEEP", "VELENO-AUTORINFRESCO", "VELENO-DOMINI", "VELENO-ORIENTATO",
    "RIPIEGHI-ZERO", "MAX-NODI-FERMA", "RIPRESA-ARGV", "Z54",
    # ### E questi tre li nomina la QUARTA versione del mandato: il punto `0` guadagna
    # ### `CONFIG-1`, `H-P3`, `H-P5`, `Z20`, e `AUDIT-CURE` sta nel punto `10`.
    "CONFIG-1", "Z20", "AUDIT-CURE",
)

# =====================================================================================
#   LA TABELLA -- una riga per metodo: (come si applica, dove, stato)
# -------------------------------------------------------------------------------------
#   ### ⚠ **Le righe le ho scritte IO, leggendo le voci.** Il perimetro no: quello
#   ### lo calcola l-indice. ### **Se una riga dice il falso e- un difetto MIO**, e si
#   ### corregge qui -- ma ### **una riga che MANCA fa rifiutare il commit.**
# =====================================================================================
METODI = {
    # ------------------------------------------------------------------ gli ASSIOMI
    "A1": ("ogni parametro in `leggi.yaml` porta `valore` E `origine`, e lo schema "
           "rifiuta un parametro senza origine", "`leggi/schema.py`", "PORTATO"),
    "A2": ("nessuna scorciatoia globale: un `termine_nodo` NON PUO- avere una variabile "
           "d-arco nell-ambito, e i simboli dei vicini non esistono nel suo ambiente",
           "`leggi/schema.py` + `_genera.py::ambiente`", "PORTATO"),
    "A3": ("niente si normalizza sul proprio insieme: nessuna legge dell-era 2 "
           "normalizza, e il generatore non ha nessuna forma che lo faccia. "
           "### E CI STA DENTRO ANCHE IL CASO `A3c` (un rapporto confrontato con un "
           "massimo): non c-e- nessun rapporto cosi- nell-era 2",
           "nessun sito: da verificare a ogni legge nuova", "DA_PORTARE"),
    # ### ⛔ **LA RIGA DI `A3c` STAVA QUI, E LA DECISIONE DI LUCA LA HA TOLTA DAL
    # ### PERIMETRO:** il blocco `2` delle `43` dice *<<`A3c` NON e- un assioma ma un
    # ### caso della tabella di `A3` -> `CRITERIO`/`METODO`/`ENTRAMBE`>>*, e
    # ### `CRITERIO` ### **non e- nel perimetro dei metodi** *(`STANDARD` e
    # ### `PRESIDIO`)*. ### **`P-M1` ha RIFIUTATO IL COMMIT chiedendo questa cura**,
    # ### e ha ragione. ### ⭐ **E il fatto MISURATO non si perde: e- ripiegato
    # ### dentro `A3`**, che la decisione stessa nomina come suo padre.
    "A4": ("stratificazione causale: ### E- IL CUORE DELLA FOTOGRAFIA PER STRATO, e il "
           "cono si MISURA (1 arco per strato, esattamente zero oltre)",
           "`passo.py::strati` + `_collauda_passo.py` sezione (C)", "PORTATO"),
    "A5": ("causalita- della mediazione: l-integratore LOCALE ha un cono esatto; "
           "### il GLOBALE no, e la sua dipendenza dalla tolleranza e- misurata",
           "`_collauda_passo.py` sezione (C); la scelta e- di Luca", "DA_DECIDERE"),
    "A6": ("inerzia come teorema: nessuna legge dell-era 2 la pretende ancora",
           "nessun sito oggi", "DA_PORTARE"),
    "A7": ("conservazione e stato: lo stato e- DICHIARATO in `leggi.yaml` e `stato.py` "
           "si GENERA, quindi non esiste uno stato non dichiarato",
           "`_genera_stato.py` + `P-E3`", "PORTATO"),
    "A7b": ("uno stato non nasce indefinito: `stato.py::nuovo` azzera ESPLICITAMENTE, e "
            "### il punto 3 del mandato lo estende alla NASCITA di un nodo",
            "`stato.py`; `crescita.py` ancora da generare", "DA_PORTARE"),
    "A8": ("un ramo silenzioso non e- un ramo: il `np.real` che scartava Im e- diventato "
           "una VERIFICA SIMBOLICA di realta- piu- un assert con tolleranza dichiarata",
           "`_genera.py::e_reale` + i moduli generati", "PORTATO"),
    "A8b": ("nessuna cache cross-passo: `senza_cache()` confronta TUTTE le costanti di "
            "modulo prima e dopo tre passi, e il presidio scatta",
            "`passo.py::senza_cache` + `_collauda_passo.py` sezione (E)", "PORTATO"),
    "A9": ("un presidio che non impedisce non e- un presidio: `P-E1`..`P-E7` sono SENZA "
           "VIA D-USCITA, e ### la CI e- dichiarata RETE CHE SEGNALA, non presidio",
           "`csv/_presidi_era2.py` + il referto", "PORTATO"),
    "A10": ("una sola grandezza puo- legare due domini: oggi lo stato e- solo `psi`, "
            "quindi non ci sono due domini da legare",
            "nessun sito oggi; torna vero alla decisione 9", "NON_SI_APPLICA"),
    "A11": ("un limite e- una legge: ### IL PUNTO 2 DEL MANDATO lo rende un presidio -- "
            "il generatore rifiutera- `Min`, `Max`, `Piecewise`, `clip`, `Abs` con soglia",
            "`_genera.py` (da fare, punto 2)", "DA_PORTARE"),
    "A12": ("un difetto dimostrato si cura: i difetti trovati in questo mandato sono "
            "stati curati nel commit successivo, o DICHIARATI aperti con il perche-",
            "il referto dell-infrastruttura, sezione dei limiti", "PORTATO"),
    "A13": ("`lam` e- la scala di Planck del sistema: l-era 2 non ha ancora `lam`",
            "nessun sito oggi", "DA_PORTARE"),
    "A14": ("conservazione locale e dissipazione globale: la norma e l-energia si "
            "MISURANO (deriva 1.2e-15 e 3.9e-5 su 200 passi); ### il BILANCIO di una "
            "`regola` lo pretende come campo obbligatorio",
            "`_collauda_passo.py` sezione (D) + `schema.py` campo `bilancio`", "PORTATO"),
    "A15": ("la memoria e- dinamica e locale: nessuna memoria nell-era 2 finche- la "
            "decisione 13 e- aperta -- e il tipo `coppia_coniugata` e- AMMESSO e NON USATO",
            "`schema.py::TIPI_VARIABILE`; decisione 13", "DA_DECIDERE"),
    # ### ⚠ **E QUESTI DUE SONO ARRIVATI TARDI, perche- NON ERANO NELL-INDICE:**
    # ### `A16` e `A17` sono decisioni di Luca del `2026-10-08` e ### **nessuna voce li
    # ### nominava.** ### **Li ha trovati `P-RIF`**, rifiutando un `@rif` verso `A17`.
    "A16": ("lo stato e- UNO e evolve al PRIMO ORDINE sotto una sola `H`. ### E- L-ASSIOMA "
            "CHE DA- IL NOME AL RAMO, ed e- VERIFICATO DIRETTAMENTE: il punto 8 misura la "
            "REVERSIBILITA- su quattro semi, e entrambi gli integratori tornano entro "
            "4e-15 -- quattro ordini sotto la lettura fissata",
            "`_collauda_passo.py` sezione (G); `A16` e- il nome del ramo", "PORTATO"),
    "A17": ("ogni comportamento e- determinato SOLO dal suo ambito. ### CABLATO IN TRE "
            "POSTI: i simboli VIETATI dello schema (pos, x, y, z, coord, xyz), `P-E4` (la "
            "fisica non importa osservatori/ ne- driver) e `P-E5` (gli osservatori non "
            "scrivono lo stato, MISURATO AL BYTE)",
            "`leggi/schema.py::VIETATI`, `csv/_presidi_era2.py::pe4` e `::pe5`",
            "PORTATO"),
    # ------------------------------------------------------------------ i HOOK
    "H-FILE": ("la lista `FILE CAMBIATI` si GENERA da `git diff --cached --name-only`, e "
               "vale per ogni commit -- compresi quelli dell-era 2",
               "`.githooks/commit-msg` + `cm.py`", "PORTATO"),
    "H-FISICA-FUORI-LISTA": ("un `.py` sotto `primo_ordine/` non nella LISTA fa rifiutare "
                             "il commit. ### E HA UN BUCO MISURATO: legge `FILE_FISICA` "
                             "DAL DISCO mentre giudica i percorsi STAGED",
                             "`.githooks/pre-commit` + `csv/_file_fisica.py`",
                             "DA_PORTARE"),
    "H-ID-OBBLIGATORIO": ("un commit che tocca la fisica dell-era 2 o un referto DEVE "
                          "citare un ID: e- il rovescio di `H-INDICE`",
                          "`.githooks/commit-msg` + `csv/_hook_id_obbligatorio.py`",
                          "PORTATO"),
    "H-INDICE": ("un ID citato che non e- nell-indice fa rifiutare il commit: vale per "
                 "gli ID dell-era 2 come per gli altri",
                 "`.githooks/commit-msg`", "PORTATO"),
    "H-NON-TRACCIATI": ("file non tracciati e non ignorati sotto `csv/` o `doc/` "
                        "BLOCCANO: ha bloccato questo mandato piu- volte",
                        "`.githooks/commit-msg`", "PORTATO"),
    "H-P1-bis": ("un referto committato senza toccare la relazione: il referto "
                 "dell-infrastruttura e- stato committato CON il suo paragrafo",
                 "`.githooks/commit-msg`", "PORTATO"),
    "H-P3": (
        'un sigillo che configura il modulo a mano invece di passare dal CLI. ### GENERALIZZATO dal punto 15(a): ### LA RIGA DI COMANDO SCEGLIE SOLO IL FILE, e un argomento in piu- e- UN ERRORE -- quindi non esiste un modo di configurare a mano',
        '`primo_ordine/driver.py::main`, e lo schema della configurazione', "PORTATO"),
    # ### ⚠ **QUESTA RIGA L-AVEVO INGHIOTTITA** con una sostituzione il cui indice
    # ### di fine cercava ### **il primo `"DA_PORTARE"),` dopo l-inizio**, e quello era
    # ### il terminatore ### **di H-P5, non di H-P3.** ### **Me l-ha detto `P-M1`.**
    "H-P5": (
        'un referto che non dichiara la configurazione INTERA. ### PORTATO: il timbro porta la configurazione INTERA piu- la sua impronta, e il referto dell-era 2 stampa il conto delle leggi',
        '`timbro.py::righe_timbro`, stampato dal driver', "PORTATO"),
    "H-P7": ("ogni flag porta il suo commento: ### l-era 2 NON HA FLAG di fisica, e il "
             "punto 15(c) dice che non ne avra- -- una legge e- in tabella o non c-e-",
             "`SCHEDA_NEL_REGISTRO` lo limita al simulatore", "NON_SI_APPLICA"),
    "H-P8": ("un confronto che prende il codice di prima da `HEAD` invece che dal PADRE: "
             "l-era 2 non ha ancora confronti prima/dopo",
             "`.githooks/pre-commit`", "DA_PORTARE"),
    "H-P9": ("uno strumento che avanza una rete fuori dall-esecutore: ### IL PUNTO 9 LO "
             "GENERALIZZA all-era 2, e ### il caso da rifiutare potrebbe essere "
             "`_collauda_passo.py`, che chiama `mezzo_implicito` direttamente",
             "`.githooks/pre-commit`; punto 9", "DA_PORTARE"),
    "H-REG-R": ("una legge che cambia senza la sua scheda: ### nell-era 2 la scheda SI "
                "GENERA in `doc/leggi_era2/<id>.md`, quindi `SCHEDA_NEL_REGISTRO` limita "
                "`H-REG-R` al simulatore -- DUE POSTI PER LA STESSA SCHEDA SAREBBERO "
                "DUE FONTI",
                "`csv/_file_fisica.py::SCHEDA_NEL_REGISTRO`", "PORTATO"),
    "H-RIGHE": ("`CLAUDE.md` sotto le 400 righe: ### IL PUNTO 2 DELLE REGOLE DI GESTIONE "
                "(mandato 6) genera la sezione delle regole dall-indice",
                "`.githooks/pre-commit`", "PORTATO"),
    "H-STASH": ("`git stash` bloccato da `permissions.deny`: non e- un hook e non ha via "
                "d-uscita. Vale per ogni lavoro, era 2 compresa",
                "`.claude/settings`", "PORTATO"),
    "H-VALIDATORE": ("un indice mal formato o con una voce persa: gira nel `pre-commit` e "
                     "ha fermato questo mandato (`PI-STORICO-SENZA-COMMIT`, riga di storico senza `commit`)",
                     "`.githooks/pre-commit` + `csv/indice.py valida`", "PORTATO"),
    "H-ETC-1": ("presidio PROPOSTO e NON CABLATO nell-era 1: non ha un corrispondente "
                "nell-era 2, dove non esiste `calcola_psi`",
                "nessun sito", "NON_SI_APPLICA"),
    "H-ETC-2": ("permutare le leggi deve dare lo STESSO stato: ### PORTATO E MISURATO -- "
                "e la misura dice che per il GRADIENTE serve l-ordine canonico, perche- "
                "`fsum` non si puo- usare su array complessi",
                "`_collauda_passo.py` sezione (A), livelli 1 e 1-bis", "PORTATO"),
    "Q6": ("confrontava i valori dopo il passo, quando il rilassamento li aveva mossi: "
           "e- un presidio dell-era 1 SOSPESO per un difetto suo",
           "nessun sito nell-era 2", "NON_SI_APPLICA"),
    "R3": ("pretendeva `bias == 0.0` esatto e falliva su due ulp: ### LA LEZIONE E- "
           "PORTATA -- nessun braccio dell-era 2 pretende l-uguaglianza esatta di un "
           "float calcolato, e la norma si misura con una tolleranza DICHIARATA",
           "`_collauda_passo.py` sezione (D)", "PORTATO"),
    "R5": ("contava 25 aperture su 24 passi perche- l-iniezione del test apriva il freno: "
           "### LA LEZIONE E- PORTATA -- i casi che devono fallire dell-era 2 verificano "
           "anche che, TOLTO il finto, il presidio TACCIA",
           "`_collauda_passo.py` sezione (F), ultimo braccio", "PORTATO"),
    "U3": ("confrontava con uno sviluppo invece del valore esatto: ### LA LEZIONE E- "
           "PORTATA -- la derivata generata si confronta con la differenza finita, non "
           "con una forma approssimata scritta a mano",
           "`_collauda_genera.py`", "PORTATO"),
    "REG-R": ("la regola mantenuta del registro della fisica: nell-era 2 la scheda si "
              "genera, e il registro resta la casa delle leggi dell-era 1",
              "`csv/_file_fisica.py::SCHEDA_NEL_REGISTRO`", "PORTATO"),
    "STATI-LOCALI": (
        'gli stati pesanti restano locali, in git solo sha1, percorso e comando. ### PORTATO: `db_era2/*.npz` e- nel `.gitignore`, e IL `.timbro.json` ACCANTO SI TRACCIA -- e- leggero e porta l-impronta della tabella, dei generati e della configurazione, cioe- IL COMANDO CHE RIPRODUCE QUEL DATO',
        '`.gitignore` + `timbro.py::salva`', "PORTATO"),
    # ------------------------------------------------------------------ le REGOLE DI LAVORO
    "P1": ("non usare l-associazione senza verificare lo storico: in questo mandato ho "
           "riletto dal disco prima di ogni cura, e due volte la rilettura mi ha smentito",
           "metodo, non codice", "PORTATO"),
    "P1-bis": ("la relazione si scrive nello stesso commit del riscontro: ogni commit di "
               "questo mandato ha il suo paragrafo",
               "`RELAZIONE_PER_CLAUDE.md` + `H-P1-bis`", "PORTATO"),
    "P1-quater": ("ogni sostituzione si asserisce per se-: l-helper `sost()` conta "
                  "l-ancora e FALLISCE se non e- unica. ### E LA LEZIONE SI E- ALLARGATA: "
                  "non solo gli escape, ma il NESTING -- i heredoc di bash si sono rotti "
                  "tre volte sull-apostrofo, e i patch script si scrivono con lo strumento "
                  "di scrittura",
                  "ogni patch script di questo mandato", "PORTATO"),
    "P1-sexies": (
        'un criterio si collauda su un caso a risposta nota, e il caso che DEVE fallire e- il piu- importante. ### CABLATO DUE VOLTE: i sei casi di `_collauda_passo.py`, e ORA `P-E9` che RIFIUTA un sigillo senza il criterio `deve-fallire`',
        '`_collauda_passo.py` sezione (F) + `csv/_presidi_era2.py::pe9`', "PORTATO"),
    "P2": ("prima di escludere un flag: forza o corregge? ### L-era 2 non ha flag di "
           "fisica, e il punto 15(c) dice che non ne avra-",
           "nessun sito", "NON_SI_APPLICA"),
    "P3": ("nessuna statistica senza barra d-errore: ### l-era 2 non ha ancora una "
           "statistica -- le misure fatte sono DETERMINISTICHE (byte, cono, deriva)",
           "nessun sito oggi", "DA_PORTARE"),
    "P4": ("prima di misurare se una grandezza cambia, verificare che sia LIBERA di "
           "cambiare: il braccio <<il cono del globale cambia con la tolleranza>> l-ha "
           "fatto -- ho misurato a TRE tolleranze invece di una",
           "`_collauda_passo.py` sezione (C)", "PORTATO"),
    "P5": ("ogni ramo `else`/fallback su un percorso fisico va CONTATO: ### IL PUNTO 2 lo "
           "rende un presidio -- le guardie fuori dalla fisica avranno un contatore",
           "punto 2, da fare", "DA_PORTARE"),
    "P6": (
        'ogni csv di misura porta blob, seme e flag. ### SUPERATA nell-era 1, e IL PUNTO 5 LA RIFA- MEGLIO: il TIMBRO porta l-impronta della TABELLA, dei GENERATI e della CONFIGURAZIONE, piu- la scena, il seme e le versioni -- non una lista di flag, perche- ### i flag non ci sono',
        '`primo_ordine/timbro.py::timbro`, stampato dal driver', "PORTATO"),
    "L-DOPO-STOP": ("dopo uno STOP si lavora solo la coda: ### e Luca ha cambiato la "
                    "regola per questa coda -- lo STOP vale come CHECKPOINT e si passa al "
                    "mandato successivo SENZA aspettare",
                    "metodo; la deroga e- in `doc/CODA_2026-10-09.md`", "PORTATO"),
    "L-MEMORIA-PRIMA": ("prima di proporre una cura si valuta se una MEMORIA la cura: "
                        "### l-era 2 non ha memorie finche- la decisione 13 e- aperta",
                        "decisione 13", "DA_DECIDERE"),
    "L-NUMERI": ("ogni numero di un commit o di un referto esce da uno script: il referto "
                 "dell-infrastruttura e- GENERATO dall-uscita dei sette collaudi, e la CI "
                 "lo rigenera facendo `git diff`",
                 "`csv/_referto_infrastruttura_era2.py`", "PORTATO"),
    "L-PATCH": ("le patch in primo piano, niente `git stash`, niente escape: vedi "
                "`P1-quater`",
                "`H-STASH` + ogni patch script", "PORTATO"),
    "L-SOGLIA": ("una soglia non si calcola dai dati che giudica, e si collauda sul caso "
                 "nullo: ### SUPERATA nell-era 1. Nell-era 2 le tolleranze sono "
                 "DICHIARATE a priori (`TOLL_IM`, `toll` del punto fisso), non calcolate "
                 "dai dati",
                 "i moduli generati + `passo.py`", "PORTATO"),
    "L-STELLA": ("le cinque domande per iscritto nel task history: ### FATTE per la tappa "
                 "5, e LA 3 HA TROVATO UN DIFETTO -- la dipendenza del cono globale dalla "
                 "tolleranza",
                 "`doc/TASK_HISTORY/2026-10-09_era2_infrastruttura.md`", "PORTATO"),
    "L-UN-PROMPT": ("un prompt alla volta, i rilievi in CODA: in questo mandato sono "
                    "arrivate SEI voci di coda, tutte registrate e nessuna eseguita "
                    "fuori ordine",
                    "`doc/CODA_2026-10-09.md`", "PORTATO"),
    "P-DECADIMENTO": ("ogni decadimento e- una trasformazione: ### lo pretende il campo "
                      "`bilancio` di una `regola`, che lo schema rende OBBLIGATORIO",
                      "`leggi/schema.py`; nessuna `regola` ancora", "DA_PORTARE"),
    "P-MEMORIA": ("uno scalare con memoria acquista un verso: decisione 13 aperta",
                  "decisione 13", "DA_DECIDERE"),
    "ROBUSTEZZA-FISICA": ("i tre gradini: ### il mandato dell-infrastruttura arriva al "
                          "gradino (a) e SOLO quello, dichiarato nella stella polare -- "
                          "non (b) e non (c), perche- le leggi sono di prova",
                          "il task history, sezione LA STELLA POLARE", "PORTATO"),
    "STANDARD-4": (
        'snapshot contro snapshot allo stesso istante. ### PORTATO nel modello di sigillo (punto 7): i bracci partono dallo STESSO SEME e fanno lo STESSO numero di passi, e il confronto e- AL BYTE. ### E il <<prima>> NON E- PIU- UNA COPIA PATCHATA: si ottiene mettendo a ZERO il coefficiente, quindi il braccio zero e- byte-identico PER COSTRUZIONE',
        '`primo_ordine/sigilli/_modello.py`', "PORTATO"),
    "STANDARD-6": ("ogni difetto acclarato si registra SUBITO: i difetti di questo "
                   "mandato sono nei commit e nella relazione. ### MA DUE NON HANNO UNA "
                   "VOCE: il buco di `H-FISICA-FUORI-LISTA` e la dipendenza del cono "
                   "globale dalla tolleranza",
                   "la relazione; le voci mancano", "DA_PORTARE"),
    "STANDARD-8": ("un difetto dimostrato si cura: ### SUPERATA, assorbita in `A12`",
                   "vedi `A12`", "PORTATO"),
    "STANDARD-10": (
        'una cura non aumenta il numero delle leggi. ### IL PUNTO 10 LO RENDE STAMPATO: ogni referto porta IL CONTO, per tipo, e dice quante sono `prova: true` -- oggi 3 su 3, cioe- ZERO leggi vere',
        '`timbro.py::conto_leggi`, nel referto', "PORTATO"),
    "AUTO-MANUTENZIONE": ("tieni aggiornati i documenti vivi: l-inventario e la relazione "
                          "sono stati aggiornati in OGNI commit, e ### DUE NUMERI "
                          "DELL-INVENTARIO ERANO GIA- SCADUTI quando li ho guardati",
                          "`doc/INVENTARIO_strumenti.md`", "PORTATO"),
    "TAGLIA-FINITA": ("lo scaling di taglia finita come via al limite continuo: l-era 2 "
                      "non ha ancora una misura di taglia",
                      "nessun sito oggi", "DA_PORTARE"),
    "Z22": ("il par.5-quinquies esisteva ed e- stato violato: la lezione e- che "
            "### UN OUTPUT DA UN FILE NON TRACCIATO NON E- RIPRODUCIBILE -- e il timbro "
            "di `_presidio.avvia` lo dice a ogni giro",
            "`csv/_presidio.py`", "PORTATO"),
    # ------------------------------------------------------------------ le CURE DI ARCHITETTURA
    "ETC-PASSO": ("il passo diventa SINCRONO, fotografia a inizio passo: ### SUPERATA, e "
                  "il mandato stesso l-ha corretta -- la regola giusta e- "
                  "LA FOTOGRAFIA PER STRATO, non <<lo stato di inizio passo>>, perche- "
                  "quella contraddiceva i passi unitari arco per arco",
                  "`passo.py` + la correzione nella coda", "PORTATO"),
    "SCHED-PASSO": ("il passo pieno diventa uno SCHEDULATORE: ### PORTATO -- "
                    "`passo.py` separa strati, composizione, validazione e integrazione",
                    "`passo.py`", "PORTATO"),
    "SCHED-T1": ("la composizione e- una LISTA e c-e- UN SOLO esecutore: ### PORTATO -- "
                 "`COMPOSIZIONE_GLOBALE` e `composizione_locale()` sono liste dichiarate. "
                 "### MA <<un solo esecutore>> NON E- ANCORA UN PRESIDIO: e- il punto 9",
                 "`passo.py`; il presidio e- il punto 9", "DA_PORTARE"),
    "SCHED-T2-TIPI": ("gli 8 tipi del registro del passo: nell-era 2 i tipi sono 4 "
                      "(`termine_nodo`, `termine_arco`, `regola`, `osservatore`) e stanno "
                      "in UN vocabolario chiuso",
                      "`leggi/schema.py::TIPI`", "PORTATO"),
    "SCHED-T2-VALIDA": ("l-esecutore VALIDA la composizione: ### PORTATO E PIU- FORTE -- "
                        "`valida_composizione()` ha quattro controlli (vocabolario, "
                        "palindromo di nomi E pesi, nessun doppione, pesi a 1) e "
                        "### ognuno ha il suo caso che deve fallire",
                        "`passo.py::valida_composizione`", "PORTATO"),
    "SCHED-T3-REGOLE": ("le regole di composizione, 94 scritture in cinque forme: "
                        "### nell-era 2 le regole non esistono ancora -- e- il punto 11(a)",
                        "punto 11(a), da fare", "DA_PORTARE"),
    "NASCITA-PUNTO-UNICO": ("le grandezze della nascita si scrivono in UN SOLO punto, con "
                            "una regola dichiarata per ciascuna: ### e- IL PUNTO 3, e "
                            "`crescita.py` e- ancora uno stub",
                            "punto 3, da fare", "DA_PORTARE"),
    "C5": ("`tauluce = d/cs` e- piatto: e- una misura dell-era 1 su una scena dell-era 1",
           "nessun sito nell-era 2", "NON_SI_APPLICA"),
    "Z100": (
        "gli invarianti: il programma si ferma quando sono violati. ### PORTATO dal "
        "punto 1 nella forma dei DOMINI -- ogni tipo dichiara la sua forma, e il "
        "controllo FERMA. ### Gli invarianti di FISICA (norma, energia) si MISURANO "
        "invece, e la deriva e- stampata: fermare su una deriva numerica sarebbe "
        "fermare su un arrotondamento",
        "`primo_ordine/stato.py::controlla_domini`; la deriva in `_collauda_passo.py`",
        "PORTATO"),
    "VELENO-ARCHI-KEEP": ("il veleno allunga le derivate d-arco e non applica `keep`: "
                          "### l-era 2 non ha derivati da avvelenare -- lo stato e- SOLO "
                          "`psi`. ### Il punto 4 e- VERO E VUOTO oggi, e lo dico",
                          "nessun derivato; punto 4", "NON_SI_APPLICA"),
    "VELENO-AUTORINFRESCO": ("il veleno romperebbe i siti AUTO-RINFRESCO: idem, nessun "
                             "derivato nell-era 2",
                             "nessun sito", "NON_SI_APPLICA"),
    "VELENO-DOMINI": ("una derivata avvelenata viola il dominio per costruzione: "
                      "### E- UN VINCOLO SUL PUNTO 1 -- i domini e il veleno "
                      "SI CONTRADDICONO, e quando entrambi esisteranno va deciso quale "
                      "viene prima",
                      "punti 1 e 4; da decidere", "DA_DECIDERE"),
    "VELENO-ORIENTATO": ("il veleno cade su UNO dei due archi figli, e quale dipende "
                         "dall-orientamento: ### LA LEZIONE E- PORTATA -- `strati()` usa "
                         "la chiave `(min, max)`, quindi l-arco `(3,7)` e `(7,3)` hanno "
                         "LA STESSA chiave e lo strato non dipende da come e- scritto",
                         "`passo.py::strati`", "PORTATO"),
    "RIPIEGHI-ZERO": (
        "zero ripieghi che cambiano la fisica in silenzio. ### PORTATO in DUE "
        "modi: il generatore RIFIUTA i rami nei termini (punto 2), e il controllo "
        "di dominio FERMA invece di troncare (punto 1)",
        "`leggi/schema.py::RAMI` + `stato.py::controlla_domini`",
        "PORTATO"),
}


# ### ⚠ **E QUESTI OTTO SONO NATI NELL-ERA `2`, non portati dall-era `1`.**
# ### Stanno qui perche- ### **il perimetro e- <<ogni metodo>>**, calcolato da
# ### `classe`, e ### **non <<ogni metodo dell-era 1>>**: se il perimetro escludesse i
# ### nati nell-era `2`, ### **un presidio nuovo sfuggirebbe al documento** -- che e-
# ### esattamente cio- che `P-M1` esiste per impedire.
# ### ⭐ **Il loro `stato` e- `PORTATO` nel senso preciso: SONO NELL-ERA `2`.**
METODI["P-E1"] = (
    "NATO NELL-ERA 2. La BIIEZIONE fra legge in tabella, file generato, riga di "
    "registro e scheda, nei DUE VERSI, e `LEGGE` si legge VIA AST. "
    "### Allargato agli OSSERVATORI il 2026-10-09: prima un osservatore in tabella era "
    "INVISIBILE alla biiezione",
    "`csv/_presidi_era2.py::pe1`, `pre-commit` + CI, SENZA via d-uscita", "PORTATO")
METODI["P-E2"] = (
    "NATO NELL-ERA 2. L-IMPRONTA: un generato ritoccato a mano, o una tabella cambiata "
    "senza rigenerare. ### SI RIGENERA, NON SI CORREGGE IL FILE -- e la CI rigenera e "
    "fa `git diff --exit-code`",
    "`csv/_presidi_era2.py::pe2`, `pre-commit` + CI", "PORTATO")
METODI["P-E3"] = (
    "NATO NELL-ERA 2. Le variabili nei due versi: una variabile dichiarata in DUE "
    "POSTI divergerebbe, e per questo `stato.py` SI GENERA",
    "`csv/_presidi_era2.py::pe3`, `pre-commit` + CI", "PORTATO")
METODI["P-E4"] = (
    "NATO NELL-ERA 2, ed e- `A17` cablato: la fisica non importa `osservatori/` ne- "
    "`driver`. ### E HA IMPOSTO UNA FORMA: il collaudo del cono misura la NORMA, che e- "
    "un osservatore, quindi e- dovuto andare in un file SUO",
    "`csv/_presidi_era2.py::pe4`, `pre-commit` + CI", "PORTATO")
METODI["P-E5"] = (
    "NATO NELL-ERA 2. Gli osservatori leggono, e si MISURA AL BYTE. ### Fino al "
    "2026-10-09 PASSAVA A VUOTO e lo diceva da se-: un braccio vero e vuoto non e- una "
    "misura. Con `PROVA-NORMA` ha materia",
    "`csv/_presidi_era2.py::pe5`, `pre-commit` + CI", "PORTATO")
METODI["P-E6"] = (
    "NATO NELL-ERA 2. La tabella che cambia senza la riga di registro e senza l-ID nel "
    "messaggio: lega il cambiamento della fonte unica alla sua tracciabilita-",
    "`csv/_presidi_era2.py::pe6`, stadio `commit-msg`", "PORTATO")
METODI["P-E7"] = (
    "NATO NELL-ERA 2. I riferimenti esistono: la scheda sul disco, e ### dal 2026-10-09 "
    "la `voce` di un osservatore RISOLVE nell-indice -- prima era una stringa che "
    "nessuno verificava",
    "`csv/_presidi_era2.py::pe7`, `pre-commit` + CI", "PORTATO")
METODI["P-E8"] = (
    "NATO NELL-ERA 2, ed e- IL SOLO che NON IMPEDISCE: senza protezione del ramo la CI "
    "gira DOPO il push. ### E- UNA RETE CHE SEGNALA (`A9`), e qui avevo scritto il "
    "contrario. ### E non e- mai stata osservata girare",
    "`.github/workflows/era2.yml`; ### SEGNALA, non impedisce", "PORTATO")


# ### ⚠ **E I DODICI PRESIDI DEL VALIDATORE DELL-INDICE.** Si chiamavano
# ### `F1`…`F12`, e quei nomi ### **COLLIDEVANO con ID veri** -- il punto `12(b)`
# ### li ha rinominati, e il nome vecchio vive come ### **alias NAMESPACED**
# ### *(`VALIDATORE:F1`)*. ### **Sono dell-era `1` nell-origine e valgono per
# ### ENTRAMBE**, perche- l-indice e- uno.
METODI['PI-GEMELLE'] = (
    'due voci col titolo che cita l-altra e dominio o era differenti. ### SEGNALA e non dec'
    'ide, perche- <<come lo stesso fatto>> NON E- RILEVABILE da un programma -- e il guardi'
    'ano mi ha corretto: lo STATO e- uscito dal controllo',
    '`csv/indice.py::_f1_gemelle`, ### SEGNALA', "PORTATO")
METODI['PI-SIMBOLI-ERA1'] = (
    'una voce dell-era 2 che nomina un simbolo dell-era 1. ### E HA SCATTATO SULLA SUA PROP'
    'RIA VOCE, che elenca i simboli che cerca: chiuso con l-eccezione che cita il testo',
    '`csv/indice.py::_f2_era2`, ### SEGNALA', "PORTATO")
METODI['PI-PAROLE-STRUMENTO'] = (
    'una voce FISICA il cui titolo dice le parole dello strumento (`A17`). ### LEGGE IL TIT'
    'OLO, e per questo SEGNALA -- ed e- uno dei sei difetti che il principio del mandato no'
    'mina',
    '`csv/indice.py::_f3_fisica_strumenti`, ### SEGNALA', "PORTATO")
METODI['PI-ETICHETTA-DEFINITA'] = (
    'un-etichetta rimossa che un documento vivo DEFINISCE ancora. ### E le viste GENERATE n'
    'on contano: una riga di `doc/INDICE.md` ELENCA un ID, non lo DEFINISCE',
    '`csv/indice.py::_f4_etichette`, ### SEGNALA', "PORTATO")
METODI['PI-STORICO-SENZA-COMMIT'] = (
    'una riga di storico GIA- COMMITTATA e senza `commit`. ### E- L-UNICO DEI DODICI CHE ER'
    'A UN ERRORE DAL PRIMO GIORNO, e ha fermato questo mandato CINQUE volte: non e- una ten'
    'da',
    '`csv/indice.py::_f5_storico`, ### ERRORE (rifiuta)', "PORTATO")
METODI['PI-NOTA-CONTRADDICE-LISTA'] = (
    'una nota che nomina una lista del guardiano e ne contraddice dominio, era o stato. ###'
    ' LA PRIMA STESURA LEGGEVA LA PROSA: 11 dei 13 segnali erano UNA SOLA FRASE, e l-ha tro'
    'vato il presidio stesso guardando la sua uscita',
    '`csv/indice.py::_f6_note`, ### SEGNALA', "PORTATO")
METODI['PI-FISICA-ERA1-NON-SOSPESA'] = (
    'una voce FISICA dell-era 1 con uno stato che non e- SOSPESA ne- CHIUSA. ### NASCE DA U'
    'N ERRORE MIO: ho messo nel campo `stato` l-<<APERTO>> di un documento, che e- lo stato'
    ' DELL-ERA 1 e va in `stato_era_1`',
    '`csv/indice.py::_f7_stato`, ### ERRORE (rifiuta)', "PORTATO")
METODI['PI-OGGETTI-ERA1'] = (
    'una voce ENTRAMBE che nomina un oggetto concreto dell-era 1. ### E IL GUARDIANO MI HA '
    'CORRETTO: il marcatore <<nomina un `.py`>> e- STATO TOLTO, perche- 6 dei 20 segnali er'
    'ano suoi -- nominare un file non e- parlare del vecchio codice',
    '`csv/indice.py::_f8_era1`, ### SEGNALA', "PORTATO")
METODI['PI-ERA-STATO'] = (
    'era ENTRAMBE o era 2 con uno stato impossibile. ### L-era 2 ammette solo AGENDA, perch'
    'e- NON E- COMINCIATA. Acceso NELLO STESSO COMMIT delle correzioni che lo rendono vero,'
    ' e l-ordine giusto me l-ha corretto Luca',
    '`csv/indice.py::_f9_era_stato`, ### ERRORE (rifiuta)', "PORTATO")
METODI['PI-CRITERIO-METODO'] = (
    'una voce classe CRITERIO in un dominio che non e- METODO: un criterio e- un MODO DI VE'
    'RIFICARE, e dirlo FISICA confonderebbe cio- che si misura con come si misura (`A17`)',
    '`csv/indice.py::_f10_criterio_metodo`, ### ERRORE (rifiuta)', "PORTATO")
METODI['PI-REPLAY'] = (
    'l-indice e- il REPLAY del suo storico. ### E- IL PRESIDIO CHE RENDE VERA la frase <<si'
    ' scrive SOLO con la via unica>>. ### E HA UN LIMITE MISURATO: blocca `aggiorna` singol'
    'o, perche- quello valida CON i derivati PRIMA di appendere la sua riga -- la via che f'
    'unziona e- `aggiorna-lotto`',
    '`csv/indice.py::_f11_replay`, ### ERRORE (rifiuta)', "PORTATO")
METODI['PI-CHIUSURA-ORFANA'] = (
    'una `chiusura` piena su una voce che non e- CHIUSA: una chiusura che nessuno ha applic'
    'ato',
    '`csv/indice.py::_f12_chiusura_orfana`, ### ERRORE (rifiuta)', "PORTATO")

# ### I TRE che la QUARTA versione del mandato aggiunge al punto `0`.
# ### ⚠ **QUESTE TRE RIGHE LE HO INGHIOTTITE DUE VOLTE**, con una sostituzione
# ### il cui indice di fine cercava ### **il primo `"DA_PORTARE"),` dopo l-inizio** --
# ### e quello era ### **il terminatore della riga DOPO.** ### **Me l-ha detto `P-M1`,
# ### entrambe le volte.**
METODI["MAX-NODI-FERMA"] = (
    "una guardia di MEMORIA non cambia la fisica in silenzio: deve FERMARE. "
    "### PORTATO dal punto 1: ogni tipo dichiara la sua FORMA di dominio, e il "
    "controllo generato in `stato.py` SOLLEVA -- e il passo lo chiama a OGNI passo, "
    "verificato VIA AST",
    "`primo_ordine/stato.py::controlla_domini`, chiamato da `passo.py`", "PORTATO")
METODI["RIPRESA-ARGV"] = (
    'la ripresa si fida dell-argv. ### PORTATO: la riga di comando sceglie SOLO il file (punto 15a) e LA RIPRESA RIFIUTA se tabella, generati o configurazione sono cambiati -- RIFIUTA, non avverte, perche- riprendere con una tabella diversa continua una corsa che NON E- QUELLA',
    '`timbro.py::riprendi`', "PORTATO")
METODI["Z54"] = (
    'l-archivio a serie. ### IL PUNTO 15(e) e il 6 lo rifanno meglio: versione del formato nel timbro, scrittura ATOMICA (temporaneo + rinomina, perche- il PC si riavvia fra 00:00 e 02:00), e la RIPRESA CHE RIFIUTA se la tabella e- cambiata',
    '`timbro.py::scrivi_atomico`, `::salva`, `::riprendi`', "PORTATO")
METODI["CONFIG-1"] = (
    "28 leggi su 31 giravano SPENTE in sei misure, per 140 costanti di modulo. "
    "### IL PUNTO 15 L-HA CHIUSO, e non con un presidio sui flag: ### TOGLIENDO I "
    "FLAG. Una legge e- in `leggi_attive` PER ID, oppure NON GIRA -- e un ID che non "
    "e- in `leggi.yaml` FA RIFIUTARE il file di configurazione",
    "`primo_ordine/config/schema_config.py` + `driver.py::termini_attivi`",
    "PORTATO")
METODI["Z20"] = (
    "due bracci di un confronto che differivano in piu- di un posto. ### PORTATO: "
    "`P-AB` pretende IL CAMPO UNICO dichiarato, e se i bracci differiscono anche "
    "altrove ### IL CONFRONTO NON PARTE -- non avverte, NON PARTE, perche- una corsa "
    "lunga non si rifa- per una diagnosi",
    "`csv/_confronti_e_dati.py::valida_confronto`", "PORTATO")
# ### ⭐ **E QUESTO E' IL PRESIDIO CHE SI APPLICA A SE' STESSO.** Appena `P-M1` e'
# ### diventato una voce `classe: PRESIDIO`, ### **il perimetro lo ha incluso e il
# ### presidio HA RIFIUTATO IL COMMIT** chiedendogli la sua riga. ### **Non l'ho
# ### previsto: me l'ha detto lui**, ed e- la prova che il controllo `1` funziona
# ### ### **su una voce che non esisteva quando l-ho scritto.**
METODI["P-M1"] = (
    "e- il presidio di questo punto: ### SI APPLICA A SE- STESSO -- appena la sua voce e- "
    "nata, il perimetro lo ha incluso e lui ha RIFIUTATO IL COMMIT chiedendo questa riga. "
    "### Non l-ho previsto: me l-ha detto lui",
    "`csv/_metodi_era2.py::controlla`, cablato nel `pre-commit` e nella CI", "PORTATO")
METODI["P-C1"] = (
    "NATO NELL-ERA 2, ed e- il presidio del punto 12(a): il codice dichiara l-ID e la "
    "macchina verifica la biiezione, con DUE severita- -- un ID dichiarato e non "
    "nell-indice RIFIUTA, una voce PRESIDIO che nessun codice dichiara SEGNALA (A9). "
    "### E HA PRESO SE- STESSO, come P-M1",
    "`csv/_controlli_nell_indice.py::controlla`, `pre-commit` + CI", "PORTATO")
METODI["P-T1"] = (
    "NATO NELL-ERA 2, ed e- il principio del mandato CABLATO: un presidio dichiarato "
    "ERRORE non puo- NOMINARE un campo di testo (via AST), e chi legge la prosa PUO- SOLO "
    "SEGNALARE. ### Non ripara: MANTIENE -- la misura dice che oggi e- gia- vero",
    "`csv/_testo_e_metadati.py::controlla`, `pre-commit` + CI", "PORTATO")
METODI["P-R1"] = (
    "NATO NELL-ERA 2: `A8` e `P5` cablati. Il CONTEGGIO dei rami lo misura l-AST, il "
    "RUOLO e- dichiarato a vocabolario chiuso. ### 27 rami in 12 funzioni, e NOVE SONO "
    "`default` -- un DEBITO che il punto 15(b) vietera-, dichiarato invece che nascosto",
    "`csv/_rami_era2.py::controlla`, `pre-commit` + CI", "PORTATO")
METODI["P-T2"] = (
    "NATO NELL-ERA 2: il REPLAY su TUTTI i registri (4 REPLAY, 5 REPERTO col blob "
    "dichiarato) e i testi generati BYTE-IDENTICI (9 file, VELOCI nel pre-commit e "
    "LENTI solo nella CI). ### E metadati.jsonl e- un REPERTO PER NECESSITA-: ha "
    "una via di scrittura e ZERO storico",
    "`csv/_replay_registri.py::controlla`, `pre-commit` + CI", "PORTATO")
METODI["P-T3"] = (
    "NATO NELL-ERA 2: una citazione e- {file, riga, commit, impronta, frase} e si "
    "RI-VERIFICA su `git show`. ### Il par.2 dice che i numeri di riga SONO SHIFTATI: "
    "con il commit una citazione e- vera PER SEMPRE, senza e- destinata a diventare "
    "falsa",
    "`csv/_citazioni_strutturate.py::controlla`, `pre-commit` + CI", "PORTATO")
METODI["P-RIF"] = (
    "NATO NELL-ERA 2: un ID nel codice e- un `@rif`, o non esiste. ### Un ID in un "
    "COMMENTO e- prosa, e un riferimento che una macchina segue non vive nella prosa; "
    "i DOCSTRING restano, ed e- una scelta DICHIARATA. ### E si e- fatto piu- forte "
    "quando l-indice si e- completato: appena `A16` e `A17` sono diventati voci, ha "
    "trovato 4 commenti in piu-",
    "`csv/_rif_nel_codice.py::controlla` + `primo_ordine/_rif.py`, `pre-commit` + CI",
    "PORTATO")
METODI["P-ES1"] = (
    "NATO NELL-ERA 2, e generalizza `H-P9`: chi avanza lo stato passa dallo "
    "schedulatore. ### Le eccezioni sono DICHIARATE una per una con il loro perche- "
    "(almeno 40 caratteri), e guarda le chiamate E I NOMI -- il driver assegna la "
    "funzione a una variabile, e un presidio che guardasse solo le chiamate NON "
    "VEDREBBE NIENTE",
    "`csv/_un_solo_esecutore.py::controlla`, `pre-commit` + CI", "PORTATO")
METODI['P-MOD'] = (
    'NATO NELL-ERA 2: la mappa dichiara CHI IMPORTA CHI, e un import fuori mappa, un CICLO, un modulo non in mappa o una dipendenza dichiarata e NON USATA sono rifiutati. ### Piu- il TETTO di righe e la responsabilita- in UNA RIGA: se non ci sta, IL MODULO FA DUE COSE',
    '`csv/_modularita_era2.py::controlla` + `primo_ordine/_mappa.yaml`', "PORTATO")
# ### ⚠ **E QUI AVEVO MESSO LE RIGHE DI `DEC-REGOLA-FORMA` e `DEC-NASCITA-PSI`,
# ### e `P-M1` LE HA RIFIUTATE COME ORFANE** -- ### **giustamente:** sono di classe
# ### `DECISIONE`, che ### **non e- nel perimetro dei METODI** *(`STANDARD` e
# ### `PRESIDIO`)*. ### ⭐ **Una domanda a Luca NON E- UN METODO**, e il posto
# ### dove vive e- ### **`DA_DECIDERE_LUCA.md`**, che la raccoglie ### **da se-.**
METODI['P-E9'] = (
    'NATO NELL-ERA 2: ogni sigillo dichiara `LEGGE` e `CRITERI`, letti VIA AST, e il criterio `deve-fallire` e- OBBLIGATORIO. ### Un sigillo che DICE di avere criteri senza averli e- PEGGIO di uno senza criteri: il primo SEMBRA FATTO',
    '`csv/_presidi_era2.py::pe9`, `pre-commit` + CI', "PORTATO")
METODI['P-AB'] = (
    'NATO NELL-ERA 2: un `A`/`B` dichiara IL CAMPO UNICO in cui i bracci differiscono, e se ne differiscono due ### IL CONFRONTO NON PARTE (la lezione di `Z20`: due misure sovrapposte). ### Piu- i dati con la versione del formato e nessun file a meta-',
    '`csv/_confronti_e_dati.py::controlla`, `pre-commit` + CI', "PORTATO")
METODI['P-GUIDA'] = (
    "NATO NELL-ERA 2: `doc/COME_SI_AGGIUNGE_UNA_LEGGE.md` si ESEGUE, e un collaudo la "
    "esegue DAVVERO -- aggiunge una legge di prova alla tabella VERA, genera, verifica, e "
    "rimette tutto controllando lo sha1. ### E OGNI PASSO DICHIARA SE E- `MECCANICO` O DI "
    "`DECISIONE`: un passo di decisione NON SI ESEGUE (fingere di eseguirlo sarebbe un "
    "falso-uno), e il collaudo verifica che sia DICHIARATO tale. ### Legge la tabella dei "
    "passi DALLA GUIDA, non da una lista sua: cosi- la guida NON PUO- INVECCHIARE IN "
    "SILENZIO",
    "`primo_ordine/_collauda_guida.py` (12/12), nel comando unico e nel `pre-commit`",
    "PORTATO")
METODI['P-TEMPI'] = (
    "NATO NELL-ERA 2: `python primo_ordine/collauda.py` fa girare TUTTI i collaudi "
    "dichiarati, stampa il tempo di ognuno, e confronta il totale col budget di 120 s. "
    "### E OLTRE IL BUDGET E- UN SEGNALE, NON UN RIFIUTO: il tempo di una macchina non e- "
    "una proprieta- del repo, e fermare su quello vorrebbe dire rifiutare un commit "
    "perche- il computer era occupato. ### Ma un `pre-commit` troppo lento E- UNA RAGIONE "
    "PER DARE `--no-verify`, che e- `A9` dal lato del tempo. ### AL PRIMO GIRO HA "
    "CORRETTO UNA MIA CLASSIFICAZIONE SBAGLIATA: la catena era dichiarata <<lenta, oltre "
    "120 s>> e misura 2.55 s",
    "`primo_ordine/collauda.py`; MISURATO: 17 collaudi, pre-commit 44.4 s su 120 (37%)",
    "PORTATO")
METODI['DECISIONE-VUOLE-UN-CAMPO'] = (
    "una decisione che serve a un PROGRAMMA vuole un CAMPO: nessuno strumento legge "
    "`titolo` o `descrizione` per decidere qualcosa. ### PORTATA, e questo mandato la "
    "APPLICA A SE STESSO: `_regole_gestione.py` sceglie le regole da `classe` e "
    "`dominio`, quelle in `CLAUDE.md` dal metadato `in_claude`, e il loro gruppo da "
    "`dettaglio_regola` -- TRE CAMPI, ZERO TITOLI",
    "`csv/_regole_gestione.py`; e `PI-PAROLE-STRUMENTO` + `P-T1` la coprono in parte",
    "PORTATO")
METODI['PRECEDENZA-IN-CODA'] = (
    "fra piu- versioni di un mandato in coda vale SOLO L-ULTIMA, e l-ordine di esecuzione "
    "si REGISTRA. ### PORTATA nell-era 2: i cinque mandati del 2026-10-09 sono stati "
    "eseguiti NELL-ORDINE REGISTRATO, e lo si verifica DA GIT -- ogni task history e- "
    "ANTENATO dei commit del suo lavoro. ### Ma e- una REGOLA SCRITTA: nessun presidio la "
    "impedisce (`A9`)",
    "`doc/CODA_2026-10-09.md`; la verifica e- `git merge-base --is-ancestor`",
    "PORTATO")
METODI['P-REG'] = (
    "NATO NELL-ERA 2: ogni regola di gestione e- una VOCE (`STANDARD` se scritta, "
    "`PRESIDIO` se cablata), e porta IL FILE DI DETTAGLIO e CHI LA FA RISPETTARE. ### E la "
    "sezione delle regole di `CLAUDE.md` SI GENERA da quei campi: modificata a mano, e- "
    "RIFIUTATA. ### E <<chi la fa rispettare>> e- UN CAMPO, quindi <<quante regole non "
    "hanno nessuno che le faccia rispettare>> e- UN NUMERO (9 su 24) -- in prosa non si "
    "contava. ### Il braccio che conta e- <<NESSUNA REGOLA SI PERDE>>, misurato contro "
    "`git`: `CLAUDE.md` piu- corto NON e- un successo, e- un SOSPETTO",
    "`csv/_regole_gestione.py::errori`; collaudo in `csv/_collauda_regole.py` (13/13)",
    "PORTATO")
METODI['P-BARRIERA'] = (
    "NATO NELL-ERA 2: ogni strumento verifica all-avvio che i hook LOCALI siano attivi "
    "(`core.hooksPath`, i due file, LA LORO IMPRONTA) e SI RIFIUTA DI PARTIRE (codice 3). "
    "### Sta in `_presidio.avvia()`, che OGNI strumento chiama: metterla in ognuno "
    "vorrebbe dire ricordarsela ogni volta, e il primo che la dimentica non ha nessuna "
    "barriera. ### E TACE FUORI DAL PC (`CI=true`): la- non si committa, e il mandato "
    "preso alla lettera farebbe FALLIRE SEMPRE la CI -- E- UNA MIA INFERENZA, "
    "DICHIARATA. ### E cio- che NON puo- fare: `--no-verify` non e- impedibile in "
    "locale, e l-impronta e- in un file TRACCIATO -- non impedisce di cambiare un hook, "
    "LO RENDE VISIBILE IN UNA DIFF",
    "`csv/_barriera.py::errori`, dentro `csv/_presidio.py::avvia`; collaudo 11/11 col "
    "ramo END-TO-END", "PORTATO")
METODI['P-SIM'] = (
    "NATO NELL-ERA 2: ogni termine dichiara le `simmetrie` (almeno `U1-FASE-GLOBALE`) e "
    "cio- che `conserva`; il generatore verifica le simmetrie SIMBOLICAMENTE (la "
    "differenza deve essere ZERO in sympy) e il collaudo le conservazioni "
    "NUMERICAMENTE. ### E LE SOGLIE SONO DERIVATE DALL-ORDINE DEL METODO: `NORMA` -> "
    "`passi * eps` (invariante quadratico: solo arrotondamento), `ENERGIA` -> `dt^2` "
    "(metodo simmetrico, nessuna deriva secolare). ### Undici ordini di grandezza di "
    "differenza, e dicono una cosa vera: la norma e- conservata DALLA STRUTTURA, "
    "l-energia solo APPROSSIMATA",
    "`primo_ordine/simmetrie.py::rompe` dentro `valida_legge`; collaudo in "
    "`primo_ordine/_collauda_simmetrie.py` (13/13)", "PORTATO")
METODI['P-DIM'] = (
    "NATO NELL-ERA 2: ogni variabile e ogni parametro dichiarano la loro `dimensione`, "
    "e il generatore RIFIUTA un-espressione incoerente -- ogni ADDENDO ha la stessa "
    "dimensione, un TERMINE di `H` e- `E^1`, un OSSERVATORE dichiara la sua. ### UNA "
    "SOLA BASE, `E`, perche- `A16` implica `hbar = 1` e il tempo e- `E^-1`: una base in "
    "piu- sarebbe una manopola. ### E la dimensione sta SULLA VARIABILE, non sul tipo -- "
    "al contrario del dominio, perche- due `reale_nodo` possono essere un-energia e un "
    "tempo",
    "`primo_ordine/leggi/schema.py::dimensioni_incoerenti`, dentro `valida_legge`; "
    "collaudi 34/34 e 24/24 col ramo END-TO-END", "PORTATO")
METODI['P-DET'] = (
    "NATO NELL-ERA 2: nessun RNG globale (via AST: 6 usi, 6 `default_rng`, 0 globali), "
    "le CINQUE variabili dei thread fissate a 1 E TIMBRATE, e le versioni bloccate in "
    "`primo_ordine/versioni.lock`. ### E IL BRACCIO CHE CONTA SONO DUE PROCESSI CON LA "
    "STESSA CONFIGURAZIONE: 548 byte IDENTICI. ### Dice cio- che i thread non posso "
    "misurare (`threadpoolctl` non c-e-): se due processi danno byte identici, i thread "
    "NON stanno rompendo il determinismo",
    "`primo_ordine/determinismo.py::controlla`; collaudo in "
    "`primo_ordine/_collauda_determinismo.py` (13/13)", "PORTATO")
METODI['P-GRAFO'] = (
    "NATO NELL-ERA 2: il grafo si controlla A OGNI PASSO, dentro `passo_globale` e "
    "`passo_locale`, PRIMA di avanzare -- auto-archi, doppioni (anche nei due versi), "
    "indici fuori intervallo, liste di lunghezza diversa. ### E FERMA, NON CORREGGE: "
    "correggere cambierebbe la fisica IN SILENZIO. ### Il costo e- MISURATO: 5.70% di un "
    "passo globale, perche- un presidio che decuplicasse il costo si spegnerebbe il primo "
    "giorno",
    "`primo_ordine/grafo.py::controlla`, dentro il passo; collaudo in "
    "`primo_ordine/_collauda_grafo.py` (11/11)", "PORTATO")
METODI['P-ALB'] = (
    "NATO NELL-ERA 2: l-albero delle scelte ha la sua fonte in `doc/ALBERO_era2.yaml`, i "
    "nodi di `decisioni.jsonl` SI GENERANO da li-, e ### UN NODO `presa` CON UNA "
    "DIPENDENZA NON `presa` FA FALLIRE `valida`. ### Piu- il ciclo, l-arco rotto, "
    "l-etichetta locale usata come id, e un nodo PRESA di cui non si sa l-argomento. "
    "### E- la differenza fra una DIREZIONE DICHIARATA e una DECISIONE PRESA: su `D9` "
    "Luca ha dichiarato una direzione e il mandato dice NELLA STESSA FRASE che non e- "
    "una decisione presa",
    "`csv/_albero_era2.py::controlla`, dentro `indice.py valida` + `pre-commit` + CI",
    "PORTATO")
METODI['P-ID'] = (
    "un ID che NASCE non puo- collidere con un ID, un alias o uno dei significati "
    "dichiarati di un omonimo, e ha almeno 4 caratteri. ### Decisione di Luca, blocco 1 "
    "delle 43. ### E <<che NASCE>> e- MISURATO: 420 ID esistenti sono piu- corti di 4, e "
    "rinominarli PERDEREBBE degli ID",
    "`csv/_id_nuovo.py::controlla_nuovo`, cablato in `crea-lotto`", "PORTATO")
METODI['VELENO-ARCHI-KEEP'] = (
    'il veleno allunga le derivate d-arco e non applica `keep`. ### IL PUNTO 4 E- VERO E VUOTO, e il collaudo lo MISURA: zero derivati, perche- lo stato e- solo `psi`. ### E la garanzia arriva dall-altro lato -- `senza_cache` rifiuta una memoria non dichiarata (`A8b`) -- quindi non c-e- IL BERSAGLIO',
    '`_collauda_passo.py` sezione (I); il braccio FALLIRA- al primo derivato', "PORTATO")
METODI["AUDIT-CURE"] = (
    "il censimento delle cure e del loro costo: ### IL PUNTO 10 chiede che ogni referto "
    "STAMPI il numero delle leggi, e che un commit che lo aumenta lo DICHIARI",
    "punto 10, da fare", "DA_PORTARE")


# =====================================================================================
#   IL PERIMETRO -- lo calcola l'INDICE, da CAMPI, non io
# =====================================================================================

def voci():
    return [json.loads(r) for r in io.open(VOCI, encoding="utf-8").read().split(NL)
            if r.strip()]


def perimetro(v=None):
    """### Gli ID che sono ### **un METODO**, da ### **campi a vocabolario chiuso.**

    ### ⛔ **NON si legge nessun `titolo` e nessuna `descrizione`** per decidere se
    una voce e- un metodo: si legge ### **`classe`**, piu- l-elenco di ID che
    ### **il mandato nomina.** ### **E- il principio del mandato applicato a se- stesso.**
    """
    v = voci() if v is None else v
    per = {x["id"]: x for x in v}
    fuori = {x["id"] for x in v if x["classe"] in CLASSI_METODO}
    fuori |= {i for i in CURE_ARCHITETTURA if i in per}
    return fuori, per


# =====================================================================================
#   IL PRESIDIO -- `P-M1`
# =====================================================================================

def controlla(v=None):
    """### Gli errori, o `[]`. ### **Quattro controlli, e ognuno ha il suo perche-.**"""
    err = []
    peri, per = perimetro(v)
    # --- `1` COMPLETEZZA: ogni metodo del perimetro ha una riga.
    # ### ⭐ **E- la forma FORTE di <<un metodo citato senza riga e- rifiutato>>:**
    # ### non solo i citati, ### **TUTTI** -- cosi- una voce `STANDARD` o `PRESIDIO`
    # ### nuova ### **fa rifiutare il commit** finche- non si dice come si applica.
    for i in sorted(peri - set(METODI)):
        err.append("`P-M1` `%s`: e- un METODO (`classe: %s`) e NON HA UNA RIGA in "
                   "`csv/_metodi_era2.py`. ### Il documento dei metodi non puo- "
                   "invecchiare in silenzio: si dice COME SI APPLICA all-era 2, anche "
                   "solo con `NON_SI_APPLICA` e il perche-" % (i, per[i]["classe"]))
    # --- `2` nessuna riga ORFANA.
    for i in sorted(set(METODI) - peri):
        err.append("`P-M1` `%s`: c-e- una riga e NON e- nel perimetro. ### O la voce e- "
                   "sparita dall-indice, o la sua `classe` e- cambiata: la riga va tolta "
                   "o il perimetro va allargato DICHIARANDOLO" % i)
    # --- `3` il vocabolario chiuso di `stato`.
    for i, riga in sorted(METODI.items()):
        if len(riga) != 3:
            err.append("`P-M1` `%s`: la riga non ha TRE campi (come, dove, stato)" % i)
            continue
        if riga[2] not in STATI:
            err.append("`P-M1` `%s`: `stato` %r fuori vocabolario: %s"
                       % (i, riga[2], list(STATI)))
        for k, nome in ((0, "come"), (1, "dove")):
            if not str(riga[k] or "").strip():
                err.append("`P-M1` `%s`: `%s` vuoto" % (i, nome))
    # --- `4` un `NON_SI_APPLICA` o un `DA_DECIDERE` DEVE dire il perche'.
    # ### ⚠ **Il par.11 lo pretende per la stella polare** *(una risposta
    # ### <<non si applica>> senza il perche- NON e- una risposta)*, e
    # ### **vale qui per la stessa ragione.**
    for i, riga in sorted(METODI.items()):
        if len(riga) == 3 and riga[2] in ("NON_SI_APPLICA", "DA_DECIDERE") \
                and len(str(riga[0])) < 40:
            err.append("`P-M1` `%s`: `%s` con una spiegazione di %d caratteri. "
                       "### Una risposta <<non si applica>> SENZA IL PERCHE- non e- una "
                       "risposta" % (i, riga[2], len(str(riga[0]))))
    return err


# =====================================================================================
#   IL DOCUMENTO, GENERATO
# =====================================================================================

ORDINE = ("PORTATO", "DA_PORTARE", "DA_DECIDERE", "NON_SI_APPLICA")
SPIEGA = {
    "PORTATO": "### ✅ **GIA- NELL-ERA `2`**, e `dove` dice dove",
    "DA_PORTARE": "### ⚠ **SI APPLICA, E NON C-E- ANCORA**: `dove` dice "
                  "**quale punto del mandato** lo porta",
    "DA_DECIDERE": "### ⛔ **SERVE UNA DECISIONE DI LUCA**, e `come` dice quale",
    "NON_SI_APPLICA": "### **NON SI APPLICA, E IL PERCHE- E- SCRITTO** — un "
                      "*<<non si applica>>* senza il perche- **non e- una risposta**",
}


def documento():
    peri, per = perimetro()
    L = []
    A = L.append
    A("# I METODI DELL-ERA `1` NELL-ERA `2` — **uno per uno**")
    A("")
    A("> ### ⛔ **QUESTO DOCUMENTO E- GENERATO** da `csv/_metodi_era2.py`: "
      "### **non si modifica a mano.** Il ### **perimetro** lo calcola l-indice "
      "*(`classe in %s`, piu- le cure di architettura che il mandato nomina per ID)*; "
      "le ### **righe** le ho scritte io." % (list(CLASSI_METODO),))
    A("")
    A("> ### ⭐ **E IL PRESIDIO `P-M1` E- LA FORMA FORTE DI *<<un metodo citato senza "
      "riga e- rifiutato>>*:** pretende che ### **OGNI metodo del perimetro abbia una "
      "riga**, citato o no. ### **Cosi- una voce `STANDARD` o `PRESIDIO` aggiunta domani "
      "FA RIFIUTARE IL COMMIT** finche- non si dice come si applica — e il documento "
      "### **non puo- invecchiare in silenzio** *(`A9`, `AUTO-MANUTENZIONE`)*.")
    A("")
    A("### ⚠ **E IL PERIMETRO E- <<OGNI METODO>>, non <<ogni metodo dell-era `1`>>:** "
      "alcune righe sono di presidi ### **NATI NELL-ERA `2`** "
      "*(`P-E1`…`P-E8`, `P-M1`)*, e il loro `come` comincia con "
      "### **<<NATO NELL-ERA 2>>**. ### ⛔ **Se il perimetro li escludesse, un "
      "presidio NUOVO sfuggirebbe al documento** — che e- esattamente cio- che "
      "`P-M1` esiste per impedire.")
    A("")
    cont = {s: 0 for s in STATI}
    for i in METODI:
        cont[METODI[i][2]] += 1
    A("| | quanti |")
    A("|---|--:|")
    for s in ORDINE:
        A("| **`%s`** | `%d` |" % (s, cont[s]))
    A("| **in tutto** | ### **`%d`** |" % len(METODI))
    A("")
    A("### ⚠ **E IL NUMERO `%d` E- MISURATO, non stimato:** viene dal perimetro che "
      "l-indice calcola, e ### **il mandato ne nominava <<una decina>>** per nome piu- "
      "*<<e le cure di architettura>>*. ### **La decina era `%d`.**"
      % (len(METODI), len(CURE_ARCHITETTURA)))
    A("")
    for s in ORDINE:
        A("---")
        A("")
        A("## `%s` — `%d` metodi" % (s, cont[s]))
        A("")
        A("> %s" % SPIEGA[s])
        A("")
        A("| id | classe | come si applica all-era `2` | dove |")
        A("|---|---|---|---|")
        for i in sorted(METODI):
            come, dove, st = METODI[i]
            if st != s:
                continue
            A("| **`%s`** | `%s` | %s | %s |"
              % (i, per.get(i, {}).get("classe", "?"), come, dove))
        A("")
    A("---")
    A("")
    A("*(Il perimetro e le righe: `python csv/_metodi_era2.py`. "
      "Il collaudo nei due versi: `python csv/_metodi_era2.py --collaudo`.)*")
    return NL.join(L) + NL


# =====================================================================================
#   IL COLLAUDO -- NEI DUE VERSI
# =====================================================================================

def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    v = voci()
    peri, _per = perimetro(v)
    print("=" * 100)
    print("IL COLLAUDO DI `P-M1` -- nei DUE VERSI")
    print("=" * 100)
    esito("sul disco: `P-M1` TACE", controlla(v) == [],
          "%d metodi nel perimetro, %d righe" % (len(peri), len(METODI)))
    esito("### il braccio sopra HA MATERIA (il perimetro non e- vuoto)", len(peri) > 50,
          "%d metodi: se fosse 0 il braccio sarebbe un FALSO-UNO" % len(peri))
    # --- il verso che DEVE scattare: una voce `STANDARD` nuova senza riga
    finta = dict(v[0], id="STANDARD-FINTO-PER-IL-COLLAUDO", classe="STANDARD")
    esito("### DEVE scattare: una voce `STANDARD` NUOVA senza riga",
          any("NON HA UNA RIGA" in e for e in controlla(v + [finta])),
          "### e- il cuore del punto `0`: il documento non invecchia in silenzio")
    # --- una riga ORFANA
    METODI["ID-CHE-NON-ESISTE"] = ("x" * 50, "y", "PORTATO")
    try:
        esito("### DEVE scattare: una riga ORFANA (niente voce nell-indice)",
              any("NON e- nel perimetro" in e for e in controlla(v)))
    finally:
        del METODI["ID-CHE-NON-ESISTE"]
    # --- uno `stato` fuori vocabolario
    salva = METODI["A1"]
    METODI["A1"] = (salva[0], salva[1], "QUASI_PORTATO")
    try:
        esito("### DEVE scattare: uno `stato` FUORI VOCABOLARIO",
              any("fuori vocabolario" in e for e in controlla(v)),
              "### il vocabolario CHIUSO e- il principio del mandato")
    finally:
        METODI["A1"] = salva
    # --- un `NON_SI_APPLICA` senza il perche'
    METODI["A1"] = ("corto", salva[1], "NON_SI_APPLICA")
    try:
        esito("### DEVE scattare: un `NON_SI_APPLICA` SENZA IL PERCHE-",
              any("SENZA IL PERCHE" in e for e in controlla(v)),
              "`L-STELLA` lo pretende per le cinque domande, e vale qui")
    finally:
        METODI["A1"] = salva
    esito("NON deve scattare: rimesso tutto a posto, `P-M1` TACE di nuovo",
          controlla(v) == [],
          "### i bracci di sopra scattavano per LORO, non per un residuo")
    # --- e il documento si rigenera byte-identico
    if os.path.exists(FUORI):
        atteso = documento()
        esito("### il documento RIGENERATO e- BYTE-IDENTICO a quello sul disco",
              io.open(FUORI, encoding="utf-8").read() == atteso,
              "### altrimenti qualcuno l-ha modificato a mano")
    print("=" * 100)
    print("IL COLLAUDO DI `P-M1`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    if err:
        for e in err[:14]:
            print("  ### %s" % e)
        print("  ### `P-M1` FALLISCE: %d errori" % len(err))
        return 1
    peri, _ = perimetro()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(documento())
    print("  `P-M1`: %d metodi nel perimetro, %d righe, TUTTO A POSTO"
          % (len(peri), len(METODI)))
    cont = {}
    for i in METODI:
        cont[METODI[i][2]] = cont.get(METODI[i][2], 0) + 1
    print("  %s" % "   ".join("%s=%d" % (s, cont.get(s, 0)) for s in ORDINE))
    print("  scritto doc/METODI_era1_in_era2.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
