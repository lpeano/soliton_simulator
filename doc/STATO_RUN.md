<!-- INDIRIZZO:INIZIO -->
# ⚠⚠⚠ L'INDIRIZZO DEL LAVORO — **decisione di Luca, 2026-09-24**

> ### **«La doppia copertura deve vivere in UN posto solo, lo spinore; oggi vive anche in `phi`,
> ### dove è finta, e da lì governa la generazione di materia e un tempo proprio.
> ### Il `4pi` e il tempo unico si sistemano INSIEME, prima di tutto il resto.»**
>
> *(parole di Luca, riportate verbatim: sono la motivazione, non una mia parafrasi)*

## COSA SIGNIFICA, operativamente

**Non si cura `FASE_2PI` da sola e non si cura `TEMPO_UNICO` da solo.** Sono **due facce dello
stesso difetto**: `phi` porta una doppia copertura che **non le appartiene**, e da lì la passa
alla **torsione**, che la passa alla **mitosi**, alla **creazione di coppia** e a un **tempo
proprio**. Curare un anello alla volta sposta il difetto invece di toglierlo — **ed è
esattamente quello che `Z127` ha misurato**: portare `phi` su `2pi` ha dimezzato `tw` e
**fermato la generazione di materia**, perché le soglie restavano ancorate al `4pi` vecchio.

## ⛔ SOSPESI — **e non si riaprono senza Luca**

| lavoro | stato |
|---|---|
| **la prova di `FASE_2PI`** *(600 passi)* | ⛔ **SOSPESA** |
| **la cura di `D36`** *(soglie in frazione del dominio)* | ⛔ **SOSPESA** — era il punto 5 del mandato precedente, **non è stata cominciata** |
| **`TEMPO_UNICO` come cura a sé** | ⛔ **SOSPESO**: va progettato **insieme** al `4pi` |
| `PROBLEMI-CHK3` · `FAMIGLIE` · `FASCE-TAU` | ⛔ **SOSPESI** |
| **ogni run** | ⛔ **SOSPESO** |
| **ogni cura nuova in codice** | ⛔ **NESSUNA** |

> **Cosa si fa invece:** la **MAPPA del `4pi`**, la domanda **`S08`** *(che cos'è `phi`)*, la
> **MAPPA dei tempi**, e poi **UNA SCHEDA DI PROPOSTA nel registro** — **derivata, senza
> codice**. Tutto **sola lettura**.

## ⏳ IN CODA, e NON bloccano le cure *(`A12` regola 1)*

**Decisione di Luca, 2026-09-24.** Due lavori del prompt unico **vanno in coda**, perché sono
**misure** e `A12` dice che una misura nuova non passa davanti a una cura derivabile:

| | lavoro | perché è in coda |
|--:|---|---|
| **⛔ ANCORE-1 — APERTA il 2026-09-25** | **25 SIGILLI PRENDONO «IL CODICE DI PRIMA» DA `HEAD`** (**43** occorrenze su **310** file di `csv/` — **il 39 pubblicato la mattina era un SOTTOCONTO**, corretto dal collaudo di `P8` che ha trovato la finestra cieca del rilevatore; elenco generato in `doc/ANCORE_prima_da_HEAD.md`, strumento `csv/_ancore_prima.py`). **Erano giusti quando sono girati** — la cura non era committata — ma **rigirarli OGGI da' un `PASS` che confronta il ramo spento CON SE STESSO.** Gemello speculare di *«un sigillo che non viene rigirato non protegge nulla»*: **qui uno che VIENE rigirato mente.** *(31 altre occorrenze usano `HEAD` in modo LEGITTIMO — la guardia del par.5-quinquies — e si lasciano in pace; 10 restano `DA GUARDARE A MANO`, non assolte.)* | **LA CURA ESISTE GIA' ED E' UNA RIGA:** `_cli_flag.sim_prima_del_flag(flag, dest)`, che ancora al **PADRE del commit che ha introdotto il flag** e **asserisce** che il file estratto non contenga il flag (`A9`). **CRITERIO DI CHIUSURA:** i 25 convertiti **e rigirati**, uno per volta, ciascuno col suo referto — e **ogni conversione puo' far cadere un `PASS` storico**, che va committato come `FAIL` invece di essere aggiustato. **PIU'** il controllo `P8 ANCORA «PRIMA» NON SCADUTA` fra i presidi automatici, **senza il quale il difetto torna** (`A9`). |
| **✅✅ POTENZE-1 — CHIUSA il 2026-09-26 con la CURA A (`rho_s/W^2`), sigillo **`6/6`**: `F2` da `x47 000` a `x1.4`, `F1` `2.427` contro `2.4567` previsto, e `C1` **PASSA nella forma COL SEGNO** (`|media|/SE` `0.9656` lunghi, `1.2640` corti; `2ba2482`). **La cura e' NEL DRIVER** *(`--contrasto-intensivo` in ogni run, sigillo del driver `16/16`, 14 obbligatorie)*.** **❌❌ RITIRATO il 2026-09-26 (Luca) — «il residuo `~0.06` di `C1` e' quello dell'aritmetica degli esponenti»: le differenze `pend(contrasto)-pend(coppia)` hanno **SEGNI MISTI** *(`-0.0247` sui corti, `-0.0511` sui lunghi)*, quindi **non esiste un residuo con un verso**; e l'aritmetica prevedeva `-0.04`, **negativo**, contro una media di **moduli**, positiva per costruzione. *(NB di onesta': quella frase viveva nella RELAZIONE, **non in questa riga** — il ritiro e' registrato qui perche' Luca lo ha chiesto in entrambi i posti, non perche' l'avessi scritta qui.)** | **UN'ASIMMETRIA DI POTENZE DEL VICINATO CON TRE SINTOMI, NON TRE DIFETTI.** Misurato sui figli della mitosi con `R2` alto: **`rho_s ~ ramp^1.95`** *(`R2 = 0.99`, due semi: `1.9133`/`1.9866`)* — **DUE** potenze *(pesi `ramp_i·ramp_j` × modulo quadro)*; **`peq ~ ramp^0`** *(`0.017`/`-0.204`, `R2` `0.01`/`0.21`: **PIATTO**, ed **EREDITATO** dall'arco del genitore, `:6226`)* — **NESSUNA** potenza; **la coppia UNA** *(`B = B/max(deg,1e-9)` a `:3251`, gia' una media)*. **CONSEGUENZA MISURATA: un figlio ha `|omega| ~ 600` contro `0.013` di un maturo — FATTORE ~47 000** — perche' `contrasto` e' 3-4 ordini troppo PICCOLO *(`rho` parte da `2e-04`, `peq` e' ereditato a `1.37`)*, e **a eta' 14 e' ancora `0.011` contro `8.4`**. **❌ RITIRATA il 2026-09-25 (rilievo di Luca) l'affermazione «non e' un transitorio perche' il divario di `|omega|` DIVERGE»:** nella **stessa finestra** `R1` e' **NON MISURATO** perche' `peq` non si e' rilassato, e **la stessa condizione vale per `omega`** — usare una finestra come insufficiente per un criterio e decisiva per l'altro **e' una lettura incoerente**. **IL DATO CHE SI PUO' USARE sono i bracci `corti`:** `|peq-rho|/rho` recupera **×11.4** e **×13.3** *(`17.54 -> 1.541`, `13.51 -> 1.019`)* mentre la differenza di pendenza cala solo **-17.6 %** e **-14.0 %** *(`2.7980 -> 2.3059`, `2.7325 -> 2.3491`)*: **il divario NON e' proporzionale allo scarto di `peq`**, e il ritardo spiega **meno di un quinto** del residuo **in questa finestra**. ⚠ E' un **LIMITE SUPERIORE**, non un'esclusione: lo scarto residuo e' ancora `1.0`-`1.5`, **dieci volte** sopra l'equilibrio. **`R1` resta NON MISURATO.** | **TRE LETTURE, TUTTE VERE IN PARTE, NESSUNA DA SOLA:** ① *estensivita'* — regge la **direzione** (la normalizzazione pesata **dimezza** il divario: `1.25 -> 0.62`, `2.78 -> 1.44`), cade sull'**esponente** (`C1''` FAIL: e' `2`, non `1`); ② *ritardo di `peq`* — regge che **l'eredita' e' un difetto**, cade come **ritardo** (`R1` **NON MISURATO**: `|peq-rho|/rho` finale `0.70`-`1.54` contro `< 0.1`); ③ *esponenti di `ramp`* — **RESTA APERTO, non «caduto»** *(correzione di Luca)*: `|omega| ~ ramp^-0.31/-0.78` non e' `-1`, **ma la COPPIA sui figli NON E' NEI JSON** *(verificato: la `storia` ha otto campi e la coppia non c'e')*, quindi **non e' misurato** se l'asimmetria di esponenti ci sia. **E la mia spiegazione «`omega` e' al plateau» E' RITIRATA:** il plateau va come `|F|·sqrt(dt·tau/2)`, quindi **dovrebbe CALARE come `1/ramp`** (×5 fra eta' 2 e 14), e `omega` misurato **e' piatto** (`457.7 -> 608.4`, **+33 %**). **Non l'ho misurato: l'ho raccontato.** **✅ SCOMPOSIZIONE MISURATA il 2026-09-26** *(`K1` PASS su **4300** campioni, scarto `3.553e-15`; `K2` PASS; collaudo **4/4**)*: **`T2` = `107`-`114 %`**, **`T3` (peq ereditato) = `-3` a `-6 %`**, **`T1` = `-4` a `-8 %`**. **IL DIVARIO E' TUTTO NEL PESO DI VICINATO, AL QUADRATO**, e la struttura si vede diretta: `rho ~ ramp^2.74`, `W ~ ramp^1.37` -> **`rho ~ W^2.00`**. **❌ E RIBALTA la mia lettura precedente** *(«il `peq` ereditato a 1.37 e' la causa»)*: **`T3` e' NEGATIVO**, il `peq` del figlio e' **piu' piccolo** di quello dei maturi e **riduce** il divario — avevo confrontato `peq` con `rho` **dentro il figlio** e concluso qualcosa **sul confronto coi maturi** *(errore di popolazione, `A3`)*. **E `R3bis` CADE**: `coppia ~ ramp^0.15/0.04` — la coppia **non porta `ramp`**, quindi l'asimmetria e' **`0` contro `2.8`**, **piu' grande** di quanto l'ipotesi prevedeva. **⚠ MA LE FRAZIONI DICONO DI COSA E' FATTO IL DIVARIO, NON COSA FAREBBE UNA CURA:** per la **A** il legame e' **esatto** *(rimuove `T2` per costruzione)*; per la **B** **no** — `T3` e' il contributo **attuale** del rapporto dei `peq`, e una cura che calibrasse `peq_f` sul `rho` locale *(da `1.37` a `~2e-04`)* **sposterebbe `T3` di una quantita' enorme**. **Non e' misurato cosa farebbe la B.** | **CRITERIO DI CHIUSURA — DUE CURE DISTINTE, e decide Luca quale prima:** ⓐ l'**esponente del vicinato** *(`rho_s/W^2` chiuderebbe `C1'`/`C1''`, **ma non tocca i figli**)*; ⓑ il **`peq` alla NASCITA** *(tocca i figli, **ma non l'esponente**)*. **Non sono varianti: sono due sintomi della stessa asimmetria, e nessun calcolo dice quale venga prima.** |
| **✅ OKN-ASSERT — CHIUSA il 2026-09-26, a run finito (residuo rilevato da Luca)** | **UN `getattr(..., default)` CHE DECIDE AL POSTO MIO SENZA DIRLO.** In `csv/_test_fork/_scomposizione_figli.py`: `OK_N = np.asarray(getattr(net, "_diag_ok_n", np.ones(n, bool)))`. **Se la riga diagnostica mancasse, quel `np.ones` direbbe «tutti validi» e nessuno se ne accorgerebbe** — e' `RIPIEGO-1` in miniatura *(un ripiego che non si annuncia)*, e la famiglia che `P5` delle regole descrive: **un fallback mai misurato e' un comportamento sconosciuto**. | **OGGI NON MORDE, e il perche' conta:** la postcondizione `P9` garantisce che la riga ci sia. **Ma la garanzia sta in un ALTRO presidio, non qui:** se un giorno la lista delle righe dichiarate cambiasse, **il difetto tornerebbe muto**. **CURA (Luca: «alla prossima occasione, senza fermare niente»):** un `assert` sulla presenza di `_diag_ok_n`, con il messaggio che dice **quale riga manca**. **✅ APPLICATA a run chiuso**, nello stesso commit del referto: `assert hasattr(net, "_diag_ok_n")` col messaggio che dice **quale riga manca e cosa accadrebbe senza** *(i nodi col contrasto di convenzione entrerebbero nell'identita')*. |
| **✅ RIPIEGO-1 — APERTA E CHIUSA il 2026-09-25 (difetto mio, rilevato da LUCA)** | **UN RIPIEGO GLOBALE SU UNA CONDIZIONE LOCALE E' UN VERDETTO VACUO MASCHERATO** (`P6`). Nella variante pesata di `INERZIA-1(C)` il ripiego era `if ... or np.any(_wn <= 0.0)`: **un solo nodo con somma dei pesi zero spegneva la cura per TUTTA la rete in quel passo**. **E non era un caso raro: era IL CASO** — i figli della mitosi nascono con `ramp = 0`, quindi i loro archi hanno `w = 0` e la loro somma e' `0`: **ogni nascita spegneva la cura**, e i figli sono **esattamente cio' che la cura doveva sistemare**. | **STRADA 2 del mandato globale** *(INVALIDA la voce in corso -> si cura prima di chiuderla)*, **dichiarata nel commit**. ✅ **CURATO:** ripiego **per nodo** (`np.where`), contatori **per NODO** (`_g_ci_nodi_senza_peso` su `_g_ci_nodi_tot`) piu' **quanti di quei nodi sono NATI IN DINAMICA** *(`eta` finito contro `+inf`; senza `SEMINA_MATURA` il contatore vale `-1`, dichiarato)*. **✅ E NESSUN NUMERO E' DA RITIRARE, VERIFICATO DAL REFERTO:** il sigillo girato e' sul blob **`3e8bb8dd`**, cioe' **la variante A CONTEGGIO**; la pesata (`b4dd0d5f`) **non aveva ancora girato**. **Ma se avesse girato, i suoi numeri non avrebbero misurato la variante** — ed e' il motivo per cui il difetto e' registrato invece di essere solo corretto. Blob curato: **`1fc6a1c5`**. |
| **❓ P1BIS-DELTA — in coda per la LISTA CHIUSA, famiglia G (ordine di Luca, 2026-09-25)** | **`P1-bis` VERIFICA LA PRESENZA DI `RELAZIONE_PER_CLAUDE.md` FRA I FILE STAGED, NON IL SUO DELTA.** Caso reale: **`009d49a`** ha committato `R3 bis` nel task history **senza la relazione**, perche' lo script che la scriveva e' morto con `UnicodeEncodeError: surrogates not allowed` e il file era staged **senza modifiche** — **git non si lamenta di un file che non cambia, e il hook nemmeno**. **E' la forma piu' silenziosa del difetto che quel presidio esiste per impedire.** | **CURA:** `csv/_hook_relazione.py` deve confrontare **il contenuto** di `RELAZIONE_PER_CLAUDE.md` fra `HEAD` e l'indice *(come fa `P7` per i commenti dei flag: `git show HEAD:<file>` contro il disco)*, e **rifiutare se il delta e' VUOTO**. **COL SUO COLLAUDO CHE DEVE BLOCCARE** (`P1-sexies`): un caso sintetico in cui il file e' staged **identico** deve essere **rifiutato**, e uno in cui e' **cambiato** deve passare. **CRITERIO DI CHIUSURA:** il collaudo nei due versi, piu' una prova sul caso reale (`009d49a` sarebbe stato rifiutato). |
| **❓ REPERTI-IMMUTABILI — APERTA il 2026-09-26 (proposta di Luca), famiglia G** | **UN COMMIT PUO' TOCCARE UN REPERTO GIA' CITATO DA UN REFERTO.** Luca lo ha rilevato su `csv/_seal_fork/_sig_cura_A/_sim_A.py`, la copia diagnostica archiviata col sigillo. **✅ MISURATO COMMIT PER COMMIT, e la storia e' l'opposto di come l'ho raccontata la prima volta:**
```
3c5e404   copia 1554e2f9   referto cita 1554e2f9    coerente
e062fdb   copia 1554e2f9   referto cita 3cd1dd4f    ⚠ INCOERENTE
aae56ba   copia 3cd1dd4f   referto cita 3cd1dd4f    coerente
HEAD      copia 3cd1dd4f   referto cita 3cd1dd4f    coerente, e l'albero e' pulito
```
**IL DISALLINEAMENTO C'ERA DAVVERO, e l'ha creato `e062fdb`**, che ha committato **il referto nuovo senza la copia rigenerata**. **`aae56ba` — il commit che Luca segnala — e' quello che l'ha RIPARATO.** **A `HEAD` non c'e' niente da ripristinare**, e un ripristino a `1554e2f9` lo ricreerebbe. ⚠ **Ma il rilievo di Luca coglie un difetto REALE**: un commit **ha** lasciato un reperto incoerente, e nessun presidio se n'e' accorto. | **LA PROPOSTA RESTA VALIDA, con una distinzione che serve o il presidio blocca ogni rigiro legittimo:** sotto `csv/_seal_fork/*/` convivono **due nature diverse** — ① **REPERTI IMMUTABILI**: il referto e i `json` dei bracci, che **non si toccano** dopo essere stati citati; ② **ARTEFATTI RIGENERATI**: la copia diagnostica `_sim_*.py`, che **per costruzione** si riscrive a ogni run *(e `P9` lo pretende: «si genera al run dal file corrente, mai committata e riusata»)*. **CRITERIO DI CHIUSURA:** un controllo che rifiuti una modifica a un file di `csv/_seal_fork/*/` **il cui blob e' citato da un referto CHE NON CAMBIA nello stesso commit** — cosi' un rigiro (referto + copia insieme) passa, e una modifica solitaria no. **Col suo collaudo nei due versi.** |
| **⚠ RIPRESA-ARGV — APERTA il 2026-09-26 (limite di un meccanismo che ho costruito io)** | **LA RIPRESA SI FIDA DEL BLOB, E IL BLOB NON CERTIFICA L'ARGV.** Caso reale: i json dei bracci `off_*` del sigillo della cura A portavano **il blob giusto** *(il codice non era cambiato)* **con la configurazione sbagliata** *(giravano col flag ACCESO, perche' `ARGV_OFF` conteneva l'opzione)*. **Un giro successivo li avrebbe RIPRESI e avrebbe ripubblicato numeri sbagliati**, e ho dovuto cancellarli a mano. | **CURA:** il json porta **anche l'ARGV** *(o il suo hash)*, e `riusabile()` la confronta con quella del giro corrente. **E' una riga in piu' nel json e un confronto in piu' nella ripresa**, e chiude la lacuna alla radice: *un dato si riusa solo se **codice E configurazione** coincidono*. **CRITERIO DI CHIUSURA:** un collaudo in cui un json con l'argv diversa **NON viene ripreso**, e il referto lo dichiara col motivo. **Famiglia G.** |
| **❓ OMEGA-ETA — APERTA il 2026-09-26 (Luca: da seguire nel run base, NON una cura)** | **IL RAPPORTO `|omega|` FIGLIO/MATURO SALE CON L'ETA':** `1.05` (eta' 2) -> `1.42` (eta' 8) -> `1.86` (eta' 14), su **entrambi** i semi *(`1.08` -> `1.42` -> `1.83` sul secondo)*. **Dopo la cura A il figlio gira come un maturo entro un fattore 2**, ma **il fattore CRESCE mentre il figlio matura**, e all'eta' 14 `ramp` e' solo `~0.29`: **non si sa cosa faccia quando `ramp` arriva a `1`.** | **NON E' UNA CURA, e non si apre un'indagine adesso** *(vincolo del mandato globale: finche' la lista e' attiva, niente indagini nuove che non servano a una voce)*. **SI SEGUE NEL RUN BASE** — scena `(ii)(a)`, 4 semi, 600 passi — dove i figli hanno il tempo di arrivare a `ramp = 1`. **CRITERIO DI OSSERVAZIONE:** il rapporto **si stabilizza** oppure **continua a salire**? *(`1.86` a `ramp 0.29` extrapolato ingenuamente darebbe `~6` a `ramp 1`, ma **l'estrapolazione non e' un dato** e non la uso come previsione.)* |
| **❓ COPPIA-RAMP — APERTA il 2026-09-26** | **PERCHE' LA COPPIA NON PORTA `ramp`?** Misurato sui figli (2 semi, media geometrica, maturi dello stesso passo): **`coppia ~ ramp^0.15` e `^0.04`** *(`R2` `0.58`/`0.05`)*, mentre il peso d'arco porta `ramp_i*ramp_j` (`:3850`) e `_tq` e' moltiplicato per `ramp` a `:3554`. **Ci si aspetterebbe `^1`, si misura `^0`.** | **NON E' UN DIFETTO DELL'INERZIA:** riguarda il termine `_tq*ramp` e il `ramp_i*ramp_j` dentro `B` *(che e' poi diviso per `deg`, `:3251`)*. **CRITERIO DI CHIUSURA:** misurare i **due addendi di `correzione` separatamente** contro `ramp` sui figli — `cross(B, nb)` e `_tq*ramp` — e vedere **quale dei due** non scala. *(Il sigillo della cura A ha gia' le righe diagnostiche per `correzione` INTERA, non per i due addendi: serve una riga in piu'.)* **Aperta come domanda, NON come cura.** |
| **DRIVER-SCENA-II — APERTA il 2026-09-26 (rilievo di Luca)** | **IL DRIVER NON SA FARE LA SCENA `(ii)`, e sono QUATTRO cose insieme** *(verificate alle righe citate)*: ① `csv/_test_fork/_scena_video.py` **fissa `--test N-MASSE`** *(`:223` nell'argv, `:328` `S.avvia_test("N-MASSE")`)*; ② **`N-MASSE` con `SEMINA_LAM` va in `SystemExit`** dentro `_massa` *(`:7187`)*; ③ **`_applica_flag` semina il vuoto anche con `--nodi 0`** *(`:8681`, `net.semina(-1 if SEMINA_LAM else a.nodi)`)* **e la scena `(ii)` rifiuta una rete non vuota**; ④ **manca un `--seme` reale**. | **❗ BLOCCANTE: senza un driver che faccia la scena `(ii)`(a) non esiste il RUN BASE**, e senza run base non esistono le tre prove. | **CRITERIO DI CHIUSURA:** un comando solo che produce la scena `(ii)`(a) con la configurazione del driver e un seme dichiarato, **e un collaudo che lo dimostri nei due versi**. |
| **OSSERVABILE-P1 — APERTA il 2026-09-26 (rilievo di Luca)** | **NON ESISTE UNO STRUMENTO UFFICIALE PER LA DISTANZA FRA LE MASSE.** La `PROVA 1` chiede *«due masse si avvicinano?»*, e la distanza del sistema e' **lungo il GRAFO pesato con `d`** *(`A13`: la distanza sta sugli archi, non su `pos`)*. Oggi ci sono **solo script di analisi**, nessun osservabile con un nome. | **❗ BLOCCANTE: e' la grandezza che la `PROVA 1` misura.** Senza di essa la prova non ha un numero. | **CRITERIO DI CHIUSURA:** un osservabile inventariato che, dati due insiemi di nodi, dia la distanza **sul grafo pesato con `d`**, col suo collaudo *(due masse a distanza nota)*. |
| **MITOSI-TASSO — APERTA il 2026-09-26 (era una voce PERSA: viveva senza ID)** | **CHE IL TASSO DI MITOSI RESTI DELLO STESSO ORDINE E' UN'ASSUNZIONE NON DERIVATA**, ed e' il punto `4` di `COSA NON SO DERIVARE` della scheda ⑨ di `doc/REGISTRO_FISICA.md` *(`1/tau_pp ∈ (0,1]` con mediana vicina a...)*. | **Prima viveva come voce di ELENCO IN PROSA, senza etichetta: per questo NON compariva in nessuna vista.** Ora ha un ID. | **CRITERIO DI CHIUSURA:** misurare il tasso di mitosi prima e dopo `CURA 2`, **in configurazione del driver**, e dire se resta dello stesso ordine. **NON blocca il run base:** e' una misura di controllo. |
| **✅ LETTORI-INDICE — CHIUSA il 2026-09-26 (decisioni di Luca)** | **ESITO: `1` RITIRATO, `1` CONVERTITO, `4` FUORI PERIMETRO — e i quattro sono dichiarati tali col motivo.** ① **`_triage_difetti` RITIRATO** *(`STANDARD 10`: lo smistamento dell'indice fa lo stesso lavoro — una cura non aumenta il numero delle leggi, e nemmeno degli strumenti)*, spostato in `csv/_archivio/`. ② **`_punto_della_situazione` CONVERTITO**: legge **solo** `doc/INDICE_ID.tsv`, col campo nuovo **`avanzamento`** e il collaudo nei due versi. ③ **FUORI PERIMETRO, col motivo:** **`_cure_verificate`** e **`_quadro_unico`** leggono il **CODICE** e aprono `STATO_RUN` **per SCRIVERCI** *(sono GENERATORI di sezioni, non cercano difetti)*; **`_blob_nelle_voci`** ha per **oggetto la PROSA** dei registri *(convertirlo misurerebbe l'indice invece dei registri)*; **`_inventario_passo`** legge **gli script di `csv/`** e non apre nessuno dei tre registri. **Gli IMPORTATORI restano sul Markdown: costruiscono l'indice.** | **NON BLOCCA il run base** *(famiglia `G`)*. | **La condizione di fine e' verificata dall'inventario rigirato: nessun CONSUMATORE apre piu' `STATO_RUN`, `RAMIFICAZIONI` o `REGISTRO_FISICA` per TROVARE DIFETTI.** |<!-- vecchio testo, per storia: SEI LETTORI LEGGONO ANCORA I REGISTRI IN MARKDOWN. --> Sono `_cure_verificate` *(352 righe)*, `_quadro_unico` *(313)*, `_triage_difetti` *(302)*, `_inventario_passo` *(269)*, `_punto_della_situazione` *(162)*, `_blob_nelle_voci` *(87)*. **`_lista_chiusa` e' passato all'indice il 2026-09-26**; gli **importatori** *(`_indice_id`, `_collisioni_id`, `_rinomina_collisioni`)* **devono** leggere il Markdown, perche' sono cio' che COSTRUISCE l'indice. | **CRITERIO DI CHIUSURA:** ciascuno legge `doc/INDICE_ID.tsv` come unica fonte, **col suo collaudo nei due versi**. **Stima: 25-40 min l'uno.** | **NON BLOCCA il run base:** e' arretrato di strumenti, non una legge *(famiglia `G`)*. |
| **❓ REGISTRO STRUTTURATO — PROPOSTA DI LUCA, 2026-09-26: DA DECIDERE** | **IL DIFETTO E' IL FORMATO, NON IL PARSER** *(parole di Luca)*: le tabelle sono scritte per essere lette, e il parser deve **INFERIRE** tre cose che sono **decisioni** — che cosa e' una voce *(`6` righe su `43`: tabella interrotta da un blocco di codice)*, qual e' il suo stato *(`VALE SEMPRE` = chiusa in `RAMIFICAZIONI`, **aperta** in `STATO_RUN`)*, a quale famiglia appartiene *(`111` senza famiglia, `CLI-1` finito in `A`)*. **Tutti e tre i difetti di oggi sono fallimenti di INFERENZA, non errori di codice.** | **LA VALUTAZIONE E' SCRITTA E COMMITTATA: `doc/VALUTAZIONE_registro_strutturato.md`.** Parere: **la proposta e' giusta**, e **consiglio UN FILE PER VOCE** (`doc/difetti/<ID>.yaml`) invece di un `difetti.yaml` unico — perche' **git da' una storia PER DIFETTO** e *«nessuna voce si cancella»* diventa `git diff --diff-filter=D`, **un fatto di git e non di un parser**. `PyYAML 6.0.3` **c'e' gia'**. Tre campi in piu' rispetto alla proposta, e ciascuno nasce da un difetto di oggi: **`alias`** *(le citazioni storiche)*, **`stato_da`** *(la FRASE verbatim da cui ho letto lo stato)*, **`stato: da-decidere`** *(una migrazione che non puo' dire «non lo so» produce trecento indovinelli)*. **Rischio piu' grosso: `R4`, la COLLISIONE DI ID** — `A3`, `B5`, `M1`, `M2`, `C21` sono **voci DIVERSE in due registri**: servono ID **namespaced**. **Sweep misurato: `436` ID distinti in `217` file `.md`, e dei `170` nomi col trattino ~META' E' RUMORE.** **Stima: `~250-320` voci, `~7-10 h` in 6-8 passi, di cui `3-5 h` di REVISIONE A MANO non comprimibile.** | **CRITERIO DI CHIUSURA: la decisione di Luca fra (a) un file per voce, (b) un `difetti.yaml` unico, (c) no / non ora.** **Finche' non decide NON SI TOCCA NIENTE**: nessun `.yaml`, nessuna intestazione «fa fede», nessun hook nuovo. **E il lavoro di oggi NON va buttato:** il lettore delle cinque fonti **diventa l'importatore**, e il parser **resta come SECONDO LETTORE INDIPENDENTE** per contare le voci perse. |
| **❓ MANDATO GLOBALE — LISTA CHIUSA / LINEA D'ARRIVO (Luca, 2026-09-25)** **▶ BOZZA RIFATTA il 2026-09-26 su rilievo di Luca: la prima leggeva UNA FONTE SOLA (`STANDARD 9`), e il parser perdeva 37 righe su 43 perche' la tabella `IN CODA` e' INTERROTTA da un blocco di codice. Ora CINQUE fonti, `624` voci, `405` in lista, `219` FUORI LISTA col motivo, `48` sezioni dichiarate fuori portata, e un collaudo `2/2` che IMPEDISCE la scrittura se una delle 15 voci nominate da Luca non compare in lista.** | **SI CURANO TUTTI I DIFETTI NOTI PRIMA DI CHIUDERE L'EPOCA**, e perche' sia finibile **la lista si CHIUDE** e si lavora **per famiglie**. **⚠ REGISTRATO, NON ESEGUITO:** Luca ha detto di metterlo **in coda alla variante pesata di `INERZIA-1(C)`**, che e' in corso. | **CINQUE PARTI:** ① **generare `doc/LISTA_CHIUSA.md`** — da `STATO_RUN`, dal registro e dai referti di oggi, **tutti** i difetti ACCLARATI ancora aperti, ciascuno con *id, una riga, prova (commit), stato, dipendenze, dimensione, famiglia*, **ordinati per DIPENDENZE**; le famiglie proposte sono **A** inerzia e avvio, **B** tempo unico, **C** doppia copertura e creazione, **D** soglie tarate sotto Planck, **E** disegno e statistiche globali, **F** freno e contrazione, **G** arretrato strumenti — **da correggere se i dati dicono altro, dichiarandolo**; i **SOSPETTI restano separati**. **STOP: Luca APPROVA la lista, e da li' e' la linea d'arrivo.** ② **regola per i difetti NUOVI** (dopo l'approvazione): si registrano subito, poi **quattro strade dichiarate nel commit** — *blocca* (si cura ora, il minimo), *invalida la voce in corso* (prima di chiuderla), *stessa radice di una voce* (entra in quella famiglia, Luca conferma), *altrimenti* **`doc/LISTA_DOPO.md`, non si tocca**. **E finche' la lista e' attiva NON si aprono indagini nuove** (inventari, controlli a tappeto, sonde esplorative) **se non servono a una voce**. ③ **`P9`**: ogni copia diagnostica si **GENERA al run** dal file corrente *(mai committata e riusata)*, e prima di girare si verifica **per diff** che differisca **SOLO** per le righe `self._diag_*` dichiarate, altrimenti **STOP**; il referto stampa **entrambi i blob**; collaudo: una copia con una legge alterata **deve essere bloccata**. ④ **LA LINEA D'ARRIVO**, a lista vuota: **BASE** = scena `(ii)(a)`, configurazione del driver con **TUTTE** le cure, **4 semi**, **600 passi**, passo pieno, `P5` attivo, referto con *bilancio di `d0` per scrittore, mitosi, omega mediano ed estremo, invarianti, distanza vera fra i nuclei contro il vuoto di controllo*, **tag `base-epoca-4`**; poi **PROVA 1** sulla base *(le masse si avvicinano piu' del vuoto?)*, **criteri scritti prima**. ⑤ **OGNI GIORNO in `STATO_RUN`:** quante voci chiuse, aperte, nuove **e in quale delle quattro strade** sono finite. **La lista deve ACCORCIARSI: se in un giorno cresce, lo si scrive IN TESTA.** |
| **⚠ INERZIA-1(C) — CURATA e SIGILLATA `3/6` il 2026-09-25: GIUSTA e INSUFFICIENTE** | **LA CURA TOGLIE ESATTAMENTE `-1.0000` DI PENDENZA, in tutti e 4 i bracci** *(inerzia OFF `1.52/2.34/1.49/2.36` -> ON `0.52/1.34/0.49/1.36`)*: dividere per il CONTEGGIO dei vicini toglie **una** potenza di `k`, a quattro cifre. **✅ `C3`: byte-identico al codice PRECEDENTE** (`a2a60534^`, **non `HEAD`**), 121 campi, 0 diversi, 2 semi — **la cura E' LOCALE, provato**. **✅ `C5`:** il pavimento `1e-6` non morde (min `0.0655` su 4252 nodi, 4 ordini sopra). **✅ `C6`:** la scala scende `×0.0149 ~ 1/77`, cioe' di quanto deve. **⛔ `C1`/`C2`: NON BASTA.** Residuo di estensivita' **`+0.49`** togliendo i lunghi e **`+1.34`** togliendo i corti; `|omega|` da `×5.7` a **`×1.5`** (curato) togliendo i lunghi, ma da `×176` a **`×35`** togliendo i corti. | **LA DIAGNOSI, dai numeri:** il residuo viene **DAI PESI**, non dal conteggio — `rho_s` e' una **somma PESATA** `Σ w_ij` con `w = exp(-d/lam)`, e **dividere per il NUMERO di vicini non e' dividere per il PESO totale**. Lo dice quale taglio fa piu' danno: togliendo **i corti** si togliono **i pesi maggiori**, e li' la correzione per conteggio **sotto-corregge di piu'**. **CANDIDATO (non eseguito, DECIDE LUCA):** normalizzare sul **peso totale `Σ w_ij`**, la media pesata vera — la grandezza che `_mat(w)` gia' costruisce, **zero numeri nuovi**. **PREVISIONE FALSIFICABILE:** se il residuo viene dai pesi, quella forma deve portare la differenza delle pendenze **sotto `0.7` anche nel taglio «corti»**; **se non lo fa, la mia diagnosi e' sbagliata.** **⚠ E `C4` e' un FAIL DEL MIO CRITERIO:** il braccio spento e' generato bene e `C1` su di esso fallisce davvero, ma `C4` pretendeva in piu' una separazione `3×` — **ho duplicato `C1` con una soglia piu' stretta**. **NON l'ho corretto dopo aver visto i numeri** (`P1-sexies`): la forma giusta e' *«generato togliendo l'opzione»* + *«su di esso `C1` non passa»*, senza soglia propria. |
| **✅ CONFIG-1/a — `limite di accoppiamento` RIFATTO il 2026-09-25 in configurazione del driver** | **LA LEGGE DELL'INERZIA NON REGGE IL LIMITE, IN TUTTI E 4 I BRACCI** *(2 semi × 2 versi del taglio, 20 bersagli per seme, `P5`: zero differenze su 78)*. Da `k = 77` a `k = 2`: **COPPIA ×2.1-2.7**, **INERZIA ×2e-4 … ×4.6e-3**, rapporto **×427 … ×1.5e4**, e **`|omega|` ×4.4 … ×176** — il controllo dice che **la catena arriva alla dinamica** *(nella versione sbagliata `|omega|` faceva ×4.1)*. **IL COLPEVOLE HA UN NOME: `_contrasto`, non `T2`.** Pendenze su `log k`: **COPPIA `-0.19…-0.30` (INTENSIVA)**, **`_contrasto` `+1.06…+2.47` (ESTENSIVO)**, `T2` `-0.15…+0.44` *(si comporta come la geometria impone: e' un controllo che torna)*. **E il pavimento `1e-6` NON morde: `0/20` in ogni riga.** | **DECIDE LUCA.** I numeri indicano la direzione **(C)** con un bersaglio misurato: **`_contrasto` deve diventare intensivo**, cioe' `rho_s` normalizzato **come lo e' gia' `_peq_nodo`** (una media sul vicinato, non una somma) — e combacia col difetto di struttura gia' letto dal codice (`rho_s` e' una SOMMA pesata, `_peq_nodo` una MEDIA). **NON eseguita** (`STOP` del mandato). **⚠ E NON E' OVVIA:** non e' misurato che rendere `_contrasto` intensivo **non rompa altro** — `rho_s` estensivo entra anche altrove. **CRITERIO DI CHIUSURA:** una decisione di Luca sulla forma, **piu'** la misura d'impatto su cio' che legge `rho_s`. |
| **⛔ CONFIG-1 — APERTA il 2026-09-25** | **LE SEI MISURE DI OGGI GIRAVANO CON 28 LEGGI SU 31 SPENTE**, misurato (`csv/_config_delle_misure.py`, per AST; `doc/CONFIGURAZIONE_misure_2026-09-25.md`). Nessuna era in configurazione del driver: tutte **default del sorgente + 4-5 flag a mano**. Fra le spente: **`FORK_SU2`, `FORK_SU2_MEM`, `CAMPO_SPINORIALE`, `SPINORE_CORRETTO`, `STEP2_OROLOGIO`, `VERLET`, `CS_DINAMICO`, `TAU_LUCE`** — **il sistema PRE-FORK piu' le due cure nuove.** | **SI RIFANNO SOLO QUELLE DA CUI DIPENDE UNA DECISIONE** *(priorita' dichiarata da Luca)*: ① **`chi comprime d0`** (il bilancio per scrittore, `-36 %`, `-57.5 %`, il verdetto su `S12_coesione`); ② **`limite di accoppiamento`** (il `×1521` e il salto a `k = 2`, su cui poggia `INERZIA-1`). **CRITERIO DI CHIUSURA:** le due rifatte **con l'argv catturata dal driver** (`_cli_flag`), col confronto contro i numeri vecchi **dichiarato come confronto fra DUE SISTEMI**, non come ripetizione. Le altre quattro restano **marcate**, non ritirate. |
| **❓ RAMPA-2/c — LA CANDIDATA DI LUCA, 2026-09-25** | **INIZIALIZZARE `_cs_nodo_prev` valutando LA STESSA LEGGE (`_cs_nodo`) sullo stato iniziale, prima del primo passo.** Con `SEMINA_MATURA` il campo esiste gia' al passo 0 (`ramp = 1`), quindi `I` e i pesi **ci sono**. **E' DERIVATA:** non introduce un valore iniziale per `cs`, **usa la legge di `cs`** — la forma di `C7` (*il figlio eredita dal padre*) portata al caso in cui **un padre non c'e'**: invece di ereditare, **si valuta**. | **LA VERIFICA PRECEDE, e Luca l'ha posta in tre punti:** ① **CIRCOLARITA'** — la legge di `cs` dipende da qualcosa che al passo 0 **non esiste**? *(`cs = CS_M/(1+GAMMA*sqrt(I))` con `_Lam = mean(I)`: se `I` al passo 0 e' definito non c'e' circolo)*; ② **altri stati «prec» nella stessa condizione** — `C7` e `C11` sono curati **per la mitosi**: lo sono anche **per il passo 0**?; ③ **poi** la misura d'impatto sulle 12 leggi **su questa candidata**, non su un `cs` preso dal passo 1 a posteriori *(un `cs` preso dopo non e' un `cs` iniziale: e' un'anticipazione impossibile)*. **NON eseguita: `RAMPA-1` e' in corso e Luca ha detto di non interromperlo.** |
| **⛔ RAMPA-2 — APERTA il 2026-09-25 (richiesta di Luca)** | **AL PASSO 0 TUTTI LEGGONO `cs = CS_M`.** La cache `_cs_nodo_prev` **non esiste** al passo 0, quindi il tempo-luce usa il valore di modulo **ovunque**; al passo 1 il `cs` vero e' **`p50 1.672`** su `CS_M = 2` (`cs_std/cs = 19.07 %`). **Bias sistematico del ~20 %, nella stessa direzione per tutti.** **MISURATO per AST** (`csv/_chi_usa_il_tempo_luce.py`, `doc/RAMPA2_chi_usa_il_tempo_luce.md`): **13 funzioni, 40 punti** — `step` (14), `_passo_spinoriale` (8), `_cs_nodo` (3), `_tau_arco_causale`, `mitosi`, `memoria_hebbiana_moto`, `_pesi`, `_bloch_ritardato`… **`RAMPA-1` ne ha curata UNA** (la maturita': ora non legge piu' niente). **Stessa famiglia di `B1` e `C7`.** | **NON HO UNA CURA DERIVATA, e lo dico invece di proporne una:** la forma che ha funzionato due volte (**EREDITARE**, `C7`) **qui non si applica** — al passo 0 non c'e' un padre; e inventare un `cs` iniziale sarebbe **scegliere un numero** (par.3). **CRITERIO DI CHIUSURA — la misura che la decide:** *quante delle 12 leggi restanti cambiano risultato se al passo 0 ricevessero il `cs` del passo 1 invece di `CS_M`* — un **contrasto misurabile**, 2 semi, passo pieno. **E prima di ogni cura: i fallback su `CS_M` sono CONTATI?** (`P5`; in `C7` uno scattava nel **71.88 %** senza che nessun sigillo lo vedesse). |
| **✅ RAMPA-1 — CHIUSA il 2026-09-25, strada (3) (decisione di Luca): sigillo `9/9` dal CLI, `ramp = 1.000000000000000` per 120 passi, **zero cali**, `n` da 4252 a 4352** | **«MATURO» NON RESTA MATURO.** Col sigillo di `CURA 4` rifatto **dal CLI** (configurazione della campagna), al **passo ZERO** `ramp = 1.000000000000000` su **tutti** i 4252 nodi, e al **passo 1** su **54 su 4252** (`min 0.3265`, `_g_rampa_cali = 4198`). **`A2` = FAIL.** **Causa MISURATA** (`csv/_test_fork/_perche_ramp_cala.py`): fra i due passi `eta` cresce **×1.011** e `_tempo_rampa` **×1.196** — **il denominatore corre 18 volte più del numeratore**. Al passo zero la cache `_cs_nodo_prev` **non esiste**, quindi il tempo-luce usa `cs = CS_M = 2`; al passo 1 il `cs` vero è `p50 1.672` (`cs_std/cs = 19.07 %`). **La maturità alla nascita è assegnata con un `cs` che il nodo non ha.** | **DUE STRADE, nessuna mia:** ① la maturità si assegna col **`cs` del luogo**, che richiede la cache **alla semina** *(oggi non c'è: stessa famiglia di `C7`)*; ② **il calo è la legge** e `A2` si riscrive come **limite** *(passo zero esatto, passo 1 ≫ del braccio spento)* invece di un'uguaglianza. **CRITERIO DI CHIUSURA:** una decisione di Luca su quale delle due, **più** il sigillo rigirato con `A2` nella forma scelta. **⚠ E non si chiude «rigirando»: il `FAIL` è committato così com'è** (`STOP` del task history di `CLI-1`, scritto **prima** dei numeri). |
| **❗ CLI-1** | **I SIGILLI DI `CURA 4` E `CURA 5` NON HANNO MAI PROVATO IL PERCORSO CLI:** impostavano `S.SEMINA_MATURA = True` e `S.MITOSI_2LAM = True` **direttamente sul modulo**. E infatti i due flag **erano MORTI** *(assegnazione in `esegui_headless`, `global` in `_applica_flag`)*, e **i sigilli passavano ugualmente**. | **VANNO RIFATTI PASSANDO DAL CLI**, perché **quello è il percorso che la campagna usa**. `7/7` e `8/8` restano validi **per la LEGGE**, ma non dicevano niente **sul FLAG**. **⚠ E vale come regola generale: un sigillo che imposta il modulo a mano prova la legge, NON il flag** — e la differenza si vede solo quando qualcuno lancia da riga di comando. |
| **✅ SCENA-1 — CHIUSA il 2026-09-25, strada (1) (decisione di Luca)** | **`SEMINA_LAM` era approvata ma INCOMPATIBILE con la scena di DEFAULT del driver:** `semina(900)` in raggio `4.0` **RIFIUTA**, saturazione vera **`455`**. | **DA DECIDERE (Luca).** Le strade che vedo, e **nessuna è mia**: ① il driver passa `--nodi 0` di default *(ma allora ogni scena diversa dalla `(ii)` resta senza vuoto)*; ② si riduce `--nodi` *(ma la capienza **dipende dal seme**: `12807/12783/12812/12790`, ed è l'errore già preso)*; ③ `SEMINA_LAM` resta **esclusa** dal driver e si accende **solo** sulle scene compatibili. **Il criterio `S5` del sigillo del driver MISURA il conflitto a ogni corsa**, quindi il giorno in cui la scena cambia lo dice da sé. **✅ SCELTA DA LUCA: STRADA (1), che non era fra le tre — il vuoto di default diventa `semina(-1)`, LA SATURAZIONE, senza un numero.** Il driver fa `net.semina(-1 if SEMINA_LAM else a.nodi)`; `SEMINA_LAM` passa fra le **OBBLIGATORIE** (NUDA = CAMPAGNA, 13); le scene che seminano masse SOPRA il vuoto (`N-MASSE`, `TERRA-BUCONERO`…) sono **EPOCA PRE-`A13`** e **RIFIUTANO di partire dicendolo** (`A9`): `_massa` solleva. **`S5` riscritto — provava `semina(SEME_INIZIALE)`, cioè la domanda di IERI — e ora dice `✅ COMPATIBILE`; sigillo del driver **15/15**. |
| **⛔ CONTAGIO** | **DAL PASSO `120` GLI ORIGINALI RAGGIUNGONO IL LIVELLO DI `omega` DEI FIGLI.** Rapporto del `\|omega\|` MASSIMO fra nati e originali: **`39.17`** al passo `5`, `17.27` al `20`, `12.71` al `60`, **`1.021`** al `120`, `0.8017` al `200`, `1.695` al `300`. | **⛔ NESSUNA CORSA LUNGA PRIMA DELLA CURA DELL'INERZIA** *(decisione di Luca, 2026-09-25)*: **finché la legge dell'inerzia non è curata, ogni corsa lunga ne è CONTAMINATA.** All'inizio il disordine sta nei figli *(grado `2`, dove la legge cede)*; **dal passo `120` i due gruppi sono allo stesso livello**, quindi **non resta confinato**. **⚠ E LA VIA NON È MISURATA:** potrebbe essere propagazione, o potrebbe essere che gli originali diventano **vicini di nati**. **Va misurato, non dedotto** — ma la conseguenza operativa non dipende da quale sia. |
| **❗ INERZIA-1** | **LA LEGGE DELL'INERZIA CEDE A `k = 2`, ED È UN DIFETTO DIMOSTRATO** *(misura 3, `f8b27d9`)*: coppia `×2.39`, inerzia `×0.016`, rapporto **`×1521`** da `k = 77` a `k = 2`; e `\|omega\|` è **piatto fino a `k = 4`** e salta solo a `k = 2` — **il grado di nascita**. | **PRIMA DELLA CURA, SOLA LETTURA** *(Luca)*: da dove vengono `_contrasto` e `_T2` *(`:3226` e dintorni)*, **perché crollano a `k = 2` e non a `k = 4`**, e **quale forma DERIVATA resta regolare nel limite** senza numeri nuovi *(`STANDARD 10`: contare le leggi prima e dopo)*. **CRITERI SCRITTI PRIMA:** `\|omega\|` a `k = 2` **dello stesso ordine** di `k = 77`; **flag spento byte-identico**. |
| **❌ NODI-1 — RITIRATA** *(Luca, 2026-09-25)*. **NON cancellata: resta come storia, col motivo.** **PERCHE' È CADUTA, ed è una ragione DI FISICA, non di costo:** allacciare il figlio entro `R_CONN` **trasformerebbe la mitosi da CREAZIONE DI SPAZIO in ADDENSAMENTO**. Con il figlio legato **ai soli genitori**, la relazione fra i due genitori passa da `1` a `2` passi e **il nuovo nodo non accorcia niente**: è spazio nuovo. Con `R_CONN`, il figlio aprirebbe **`~77` scorciatoie** e il grafo si **addenserebbe** invece di crescere. **✅ LA DIREZIONE DI LAVORO È LA STRADA `(c)`: il figlio nasce legato ai soli genitori. Un nodo appena nato, DEBOLMENTE ACCOPPIATO, È FISICA.** — e non è ancora una cura. | *(il testo originale della voce, che resta leggibile:)* **«NESSUN NODO DI SECONDA CLASSE» VALE ANCHE PER I NODI NATI IN DINAMICA.** Un nodo nato da **mitosi**, **Schwinger** o **faccia** si allaccia con la **STESSA REGOLA della semina** *(`R_CONN`)*, **non solo ai genitori**. | **IL MOTIVO È MISURATO** *(`343d302`)*: i figli di mitosi nascono con **grado `2` contro `77`**, **densità `1/21`**, e **sono il top `0.1 %` di `\|omega\|`** *(arricchimento `×161` fra i nati dopo il passo zero)*. `omega = coppia/inerzia` con densità `21×` più bassa fa il resto. **Non è una legge che diverge: è un nodo che nasce con due soli archi in una regione rada.** **⛔ SI CURA INSIEME ALLA NUOVA LEGGE DI CREAZIONE** *(torsione / creazione di faccia)*, **non prima**: un nodo che nasce al centro di un triangolo con tre archi è già meno «di seconda classe» di uno che nasce su un arco con due, e le due cose vanno decise insieme. **E il calcolo delle distanze passerà DAGLI ARCHI quando il disegno uscirà dalla dinamica** *(`A3`)*. |
| **⛔ PASSO-1** | **❗ IL PASSO NON È `step()`: SONO CINQUE CHIAMATE**, e **`24` script sotto `csv/` avanzano in modo INCOMPLETO** *(inventario generato: `doc/INVENTARIO_passo_incompleto.md`)*. Di questi **`11` sono MISURA** e **`3` ENTRAMBI**. | **È il difetto di metodo più grande trovato oggi**, e tocca **le misure di stamattina e probabilmente alcune dei giorni scorsi** *(rilievo di Luca)*. Con il solo `step()` mancano **la MITOSI**, il **FRENO su `d0`**, la **GRAVITÀ** *(entrambi dentro `memoria_hebbiana_moto`)* e lo **SCUOTIMENTO**. **La cura strutturale c'è: `csv/_passo.py`**, che legge l'ordine per AST da `update()` e lo verifica contro il driver. **Resta da PORTARE i `24` script su quel modulo**, uno per uno, guardando **quale conclusione registrata** ne dipende. |
| **❗ PASSO-2** | **UN AVANZAMENTO INCOMPLETO NEL SIMULATORE STESSO, `:8404`:** `for _ in range(300): net.step()` nel percorso di ricostruzione con `--seed`/`--nodi`, seguito da `rilassa_disegno(30)`. | **TRECENTO passi senza mitosi, senza scuotimento e senza memoria del moto**, per «invecchiare» la rete. **È lo stesso difetto delle sonde, DENTRO il codice che le sonde imitano** — e il criterio che lo distingue dall'altro sito *(`:6846`, dove la sequenza è solo spezzata dal cronometro)* **è cablato in `_passo.soli()`**. **⚠ E tocca la famiglia di `Z88`:** è un percorso di **costruzione del vuoto**, quindi decide **da quale stato parte** un run lanciato con `--seed`/`--nodi`. |
| **❗ S-MIT1** | **LA MITOSI HA UNA SOGLIA DI DENSITÀ CON STATISTICA GLOBALE.** `0.5*(I[a]+I[b]) >= QMIN_M * median(peq)` *(`:5749`)*: un arco si divide o no **in base alla MEDIANA di `peq` su TUTTA la rete**. **Famiglia `D01`/`D03`** *(una legge locale decisa da una statistica globale)*. | **⚠ DA ACCLARARE PRIMA DI LEGGERE LA MITOSI NEL GIRO DELLA SCENA `(ii)`** *(Luca)*: lì il vuoto è **il `90 %` dei nodi**, quindi **la mediana la decide il VUOTO** e la soglia che governa la divisione **dentro le masse** viene fissata da fuori. **Misurato oggi nel sigillo `U2`: `median(peq) = 0.0` e `negate = 0`** — su una rete giovane la soglia è **inerte**, il che non dice nulla su come si comporterà con un vuoto maturo. |
| **S-MIT2** | **LA FINESTRA DI CREAZIONE DELLA MITOSI, MISURATA DAL CODICE:** `avv ∈ (1.500, 1.750) · PHI_CRIT`, cioè una **banda larga `1/6` della soglia**. **Sopra, la stessa legge è REPULSIONE** *(`segno = -tanh(3*(tau_pp - centro))` cambia segno a `centro = 2.75`)*, e **sopra `TW_TETTO = 4π` si spegne** *(`discesa → 0`)*. | **DA TENERE NEL REFERTO DELLA SCENA `(ii)` quando si legge se la mitosi è VIVA** *(Luca)*. **Numeri dal codice:** `soglia0 = 3π = 9.4248` *(non `2π`: `TORS_4PI` è ON e `FASE_2PI` OFF)*, `TW_TETTO = 12.5664`, `tau_soglia = 2.5`, `tau_tetto = 3.0`, `centro = 2.75`. **⚠ E l'ho imparato sbagliando due volte:** avevo messo `tw = 1e3` e poi `1.2·PHI_CRIT`, **entrambi fuori dalla finestra**, e la mitosi non scattava. |
| **FRAG1** | **`mitosi()` SU UNA RETE SENZA CAMPO VA IN `IndexError` INVECE DI DICHIARARLO.** `I = self._rho_sorgente()` è **vuoto** finché non è girato un `step()`, e `I[a]` a `:5749` solleva `index 6 is out of bounds for axis 0 with size 0`. | **FRAGILITÀ, NON DIFETTO DI FISICA** *(Luca)*: serve **una guardia `A8` che lo DICA** invece di schiantarsi. **⚠ E è la stessa modalità già costata giorni:** il sigillo dello Strato 1 **si schiantava** *(`FintaRete` senza `_tempo_luce_nodo`)* e nessuno se n'era accorto — **non FALLIVA, SI SCHIANTAVA**, la modalità più facile da non notare. |
| **⛔ U1** | **❗ URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO — `massa_critica_collasso`: `21` usi DENTRO LEGGI FISICHE** *(`mitosi`, `step`, `lambda_nodi`, `_passo_spinoriale`, `chiralita_core_locale`)*. La soglia è **`48×` irraggiungibile** con `A13` *(`621` nodi chiesti in una palla di raggio `LAM` che ne contiene `13`)*. | **NON SI RITARA CON UN NUMERO** *(Luca)*: **si ricava di nuovo o si toglie, LEGGE PER LEGGE.** Ritararla sarebbe scegliere un numero *(par.3)*, e toglierla in blocco cambierebbe cinque leggi in un colpo *(par.1)*. **⚠ E tocca il giro della scena `(ii)`:** quelle cinque leggi girano nel run, quindi **ciò che misureremo contiene anche il loro non funzionare** — sta scritto nella scheda ⑫. |
| **⛔ U2** | **❗ `M2` DIVENTA URGENTE — la mitosi mette figli SOTTO la scala di Planck.** Con la semina nuova **gli archi stanno fra `1` e `3 LAM`**, e **una buona parte *(stima di Luca: `~1/4`)* sotto `2 LAM`**. Ognuno di quelli, dividendosi, mette il figlio a `d/2 < LAM` — e **`_nasce` lo porta a `LAM`, cioè FABBRICA LUNGHEZZA**. | **La cura candidata resta «divisione solo se `d >= 2 LAM`», NON DECISA** *(Luca)*. **⚠ E la stima `~1/4` VA MISURATA**, non assunta: al passo zero si conta la frazione di archi sotto `2 LAM`. **È il secondo motore del gonfiamento, e nel giro della scena `(ii)` sarà ATTIVO.** |
| **A1-COSTANTI** | **AUDIT DELLE COSTANTI TARATE** — **`~90` commenti «misurato/tarato»** nel sorgente. Si separano le **COSTANTI TARATE** *(es. `389/484` della massa critica)* dai **semplici conteggi**. | **Le tarate sono candidate a essere state fissate NEL REGIME SOTTO PLANCK**, cioè su un sistema che `A13` dichiara inesistente. **È la stessa famiglia di `U1`, generalizzata**: `massa_critica_collasso` è quella che si è trovata per caso. |
| **A2-DXD** | **RIMISURARE NEL REGIME NUOVO:** `\|dx\|/d` del freno-legge *(criterio di riapertura: quota `> 0.5` non nulla)* e gli esiti del **giro corto di `CURA 2`**. | I numeri di ieri sono **dell'epoca pre-`A13`**: `max \|dx\|/d = 0.0531` decise la forma `1+tanh`, e **con archi fra `1` e `3 LAM` invece che troncati a `LAM` quel numero può cambiare**. *(`9-bis`: ogni numero porta la sua epoca.)* |
| **❗ A3-DISEGNO** | **IL DISEGNO ESCE DALLA DINAMICA** — cura a sé, **prima delle tre prove**. `pos` entra nella fisica in `memoria_hebbiana_moto` *(`:6129`, `:6300`, `:6517`)*, `pozzo_grafo` *(`:6088`)*, `step` *(`:4921`)*, `chiralita_core_locale` *(`:2063`)*, **e nel ramo SCHWINGER della mitosi *(`:5889`)*, dove la lunghezza dei nuovi archi viene da METÀ DELLA DISTANZA NEL DISEGNO invece che da `d`**. | **❗ IL SITO SCHWINGER È UN RILIEVO NUOVO DI LUCA, DA ACCLARARE** — non è `D02` *(che legge `pos` per una FORZA)*: qui `pos` **fissa la LUNGHEZZA di un arco nuovo**, cioè entra nella geometria come se fosse `d`. **Da verificare anche `campo_spaziale` e `classifica_topologia`.** **⚠ LE RIGHE SONO AL COMMIT `7384faf` e VANNO RICONTROLLATE SULL'HEAD** *(par.0: si cerca per NOME, non per riga)*. |
| **I1** | **IDEA DI LUCA, per dopo:** costruire **UNA** massa, **farla maturare**, leggerne la struttura **sul grafo** e **REPLICARLA come modello** per le tre masse, invece di seminare regioni nello spazio. | **Non è un difetto né una cura: è un cambio di METODO** — la massa smetterebbe di essere una **regione geometrica** e diventerebbe una **struttura misurata**. *(E risponde da sé alla domanda che `S10` pone: se una massa maturata regge, replicarla parte da qualcosa che ha già retto.)* |
| **❗ M1** | **LA MATERIA È UNO STATO, NON UNA SOSTANZA — e non c'è SCARICO.** Nel codice la materia è la condizione **`I > Λ`** *(`:4117-4120`: «**sotto `Λ` sei vuoto, sopra sei materia**»)*, cioè uno **STATO del nodo**. E **i nodi non vengono MAI TOLTI**: verificato dall'AST, le scritture di `self.pos` sono **SETTE** e nessuna rimuove — `:1532` azzeramento all'avvio · `:2400`, `:5552`, `:5700` **`vstack`** *(aggiunta)* · `:5831`, `:5833`, `:5834` **muovono il disegno** *(embedding)*. **Sorgente sì, scarico no: nessun flusso di vuoto verso le masse.** | **❓ DOMANDA PER LUCA: quando il vuoto diventa materia, qualcosa si SPOSTA?** È una domanda di **ontologia**, non una misura: decide **se serva un termine di trasporto** o se lo stato basti. **Segnata da Luca, 2026-09-24. Non si esegue.** *(⚠ E una cosa che ho visto passando e NON è questa voce: `:5834` fa `self.pos -= self.pos.mean(axis=0)`, una **media GLOBALE**. È sul DISEGNO, non su una forza, quindi par.4 non è violato — ma **va guardato, non dedotto**. In coda a sua volta.)* |
| **❗ M2** | **LA MITOSI — DUE DIFETTI DA ACCLARARE.** ① **il figlio nasce nel PUNTO MEDIO**: `pos_figlio = 0.5 * (self.pos[a] + self.pos[b])` *(`:5529`; lo Schwinger idem, `:5700`)*, quindi a **`d/2` da ciascun genitore** — **sotto `LAM` se `d < 2·LAM`, e allora **viola `A13`**. ② **le metà portate a `LAM` da `_nasce` FABBRICANO LUNGHEZZA**: due archi da `d/2` diventano due archi da `LAM`, cioè `2·LAM` al posto di `d`. **È un SECONDO MOTORE del gonfiamento**, distinto dal freno di `D31`. | **CURA CANDIDATA, NON DECISA** *(Luca)*: **divisione solo se `d >= 2·LAM`**. **È UNA CURA SEPARATA DALLA SEMINA** — un interruttore alla volta *(par.1)*. **Segnata da Luca, 2026-09-24. Non si esegue ora:** prima finisce la cura della semina. **⚠ E `S4` della scheda ⑩ rileva solo il PASSO ZERO**, quindi questi due difetti **non sarebbero visti** dai criteri di `SEMINA_LAM`. |
| **(3)** | **`S08`: che cos'è `phi`** — la catena che lo aggiorna, e se si ottiene dalla fase globale `U(1)` dello spinore *(il Bloch è caduto: `Z121`)* | è una **misura**, e la sua risposta **non cambia** nessuna delle tre cure |
| **(4)** | **LA MAPPA DEI TEMPI** — ogni lettore di `r`, `dt_n`, `tau_pp`, `d/cs`, e l'anello `A6` | idem. **E una parte è già fatta:** la provenienza dell'orologio è nel grafo della mappa del `4pi`, misurata |

> **Servono per la torsione dal trasporto `SU(2)`**, che è **dopo** il `CHECKPOINT`.

<!-- INDIRIZZO:FINE -->

<!-- DA-CLAUDE-MD-2026-09-26:par.6 -->

> *(Era **`CLAUDE.md` par.6** fino al riordino del 2026-09-26. **Verbatim**, dal tag `regole-pre-riordino`. La storia di quella sezione sta in `doc/STORIA_REGOLE.md`.)*

## 6. STATO E ORDINE DEL LAVORO
Ordine: **prima il FORK (non-abeliano), poi il resto.** GAMMA / Step 2 (cs<->orologio) / verifica
EM<->curvatura sono A VALLE: non toccarli finche' il fork non gira (a densita' reali cs e' MORTO,
I~0.05 vs soglia ~400 -> tutti i test cs-dipendenti oggi sono NULLI).

Il fork si costruisce a strati (ognuno un flag OFF, ognuno si riduce a quello sotto):
- **STRATO 0 — connessione Berry statica (arc-connection): IL PRIMO MATTONE.**
  `U_ij = exp(-i (chi/2) m_hat . sigma)`, `chi=arccos(n_i.n_j)`, `m_hat=(n_j x n_i)/|n_j x n_i|`.
  Peso antipodalita': `w_ij = |n_j x n_i| = sin(chi)` (NIENTE soglia netta, NIENTE coeff. tarato).
  Sostituzione nella forza (`_coppia_interferenza`, righe 2207-2208): `Im<psi_i|psi_j> -> w_ij * Im<psi_i| U_ij |psi_j>`.
  Flag OFF (es. `FORK_SU2=False`). Sigillo: OFF -> byte-identico scalare; ON+allineati -> scalare.
- **STRATO 1 — connessione con MEMORIA (ritardazione): FATTO** (2026-09-14, flag `FORK_SU2_MEM`
  / `--fork-su2-mem`, OFF di default; sigillo `csv/_seal_fork/_sigillo_strato1.py`, **23/23 PASS**).
  Realizzato come **ritardazione dei BLOCH**, non come memoria della matrice: `_bloch_ritardato()`
  rilassa il versore `n_ret` verso quello corrente con **slerp geodetico** e
  `alpha = 1 - exp(-dt_n/tau)`, `tau = d_nodo/cs_nodo`. Si rilassa il Bloch e NON U/N perche' un
  blend lineare di matrici uscirebbe da SU(2) (par.4). Il trasporto resta sugli spinori CORRENTI.
  **E' il pezzo che ACCENDE il fork:** rompe il teorema di inerzia dello Strato 0 (vedi par.9).
  Riduce a Strato 0 per tau->0 (esatto, 0.000e+00) e a riposo (5.3e-15).
- **STRATO 2 — memoria hebbiana saturata (relazionale):** `dg/dt=c_ij*g*(1-g/G(rho))/tau`, tetto
  `G(rho)` legato alla DENSITA' col GAMMA di cs ("sorelle non catena": G da rho, NON da cs diretto).
  Riduce a Strato 1 per g=cost.

**FATTO STABILITO (non ri-derivare male):** il trasporto attuale e' SCALARE (righe 2207-2208, stessa A
applicata ad a e b) -> il sistema e' abeliano per STRUTTURA -> l'olonomia e' banale (W=2) qualunque
cosa facciano gli spinori on-site. **La dinamica sugli ARCHI (arc-connection) e' il pezzo mancante:
senza, non c'e' olonomia.** L'evoluzione on-site esistente (`SPINORE_VIVO`, `KURAMOTO_SU2`) e'
COMPLEMENTARE (fornisce stati di nodo variati da trasportare), non sostitutiva.

<!-- DA-CLAUDE-MD-2026-09-26:par.6 FINE -->

---


<!-- PUNTO-DI-RIPRESA:INIZIO -->
# ⚠⚠ PUNTO DI RIPRESA — **si legge PER PRIMO dopo un riavvio**

> **Aggiornato 2026-09-24 sera · HEAD `43f3a89` · branch `fork-su2`.**
> **Simulatore blob `49fc54d2`.** **Nessun processo vivo, niente a metà.**
>
> ### ✅ **`CURA 1` E `CURA 2` SONO APPROVATE E IL DRIVER LE ACCENDE IN OGNI RUN.**
> **I loro default nel sorgente restano `False`: i default si cambiano all'EPOCA 3.**
> **Sotto c'è IL QUADRO UNICO, generato: cosa è acquisito, cosa è deciso e non ancora in
> codice, cosa è aperto.** **Si legge quello, non questa testa.**

## ⚠ CI SI È FERMATI QUI: **`CURA 2` chiusa e accesa; il prossimo passo è `CURA 3`**

**Nessun run in corso.** `CURA 2` è **approvata, accesa nel driver e verificata**: sigillo
`5/5` con **un processo per braccio**, giro corto `120` passi contro `_cura1_corto`, `T4`
**rifatto con la firma dei byte** *(`206` uguali, `0` diversi — le due strade concordano)*,
e un sigillo nuovo che certifica **che il driver la accende davvero**.
**Il prossimo passo è `CURA 3`** *(`φ` su `2π` con le soglie che la seguono)*, **e dopo un
CHECKPOINT: Luca decide se il freno-legge viene prima o dopo.**

### ⚠ E LA SEZIONE QUI SOTTO È STORICA — `FASE_2PI`, che è CADUTA

> **Si legge per sapere COM'ERA**, non come stato attuale. `FASE_2PI` resta **l'unica cura
> del quadro che il driver NON accende**, e il perché è qui.

**Nessun run in corso.** Il giro corto di `FASE_2PI` è finito e **la sua prova la
boccia**: la cura fa ciò che dichiara su `φ`, **ma la generazione di materia si ferma**
*(mitosi `62` → `1` evento, Schwinger `28` → `0`)*, perché **`|tw|` si dimezza e nessun
arco raggiunge più la soglia** *(`MAX 4.37 = 1.39π` contro `2π`)*.
**→ `D36` acclarato · `Z127` · il punto 2 del §D va riaperto.**
**⚠ E `SCALE-TW` NON è prerequisito di `D36`** — lo avevo scritto, **ed era sbagliato**:
con `TORS_4PI` la torsione si avvolge con **`_w8`**, finestra **`8π`**, che su incrementi
piccoli è **l'identità**. **A dimezzare `tw` è l'INGRESSO** *(`dph` e `twp` passano da
`_wphi` e stanno in `(-π, π]`)*. **`SCALE-TW` torna in coda al suo posto.**

## COS'ALTRO NON C'È IN CORSO

Il run di `D34` **è finito** *(`Z123`)*, e il sigillo di `FASE_2PI` **è finito `6/6`**
*(`Z124`)*. **Il prossimo run è la prova di `FASE_2PI` a 600 passi**, e quando parte questo
blocco lo dirà qui sopra.

<!-- QUADRO-INIZIO -->

## IL QUADRO UNICO — **tre elenchi, GENERATI** *(decisione di Luca, 2026-09-24)*

> *«Troppi fili aperti, il lavoro buono non deve perdersi per strada.»*
> **Generato da `csv/_quadro_unico.py`, e si rigira a ogni commit che cambia una cura o
> una decisione.** **Il DEFAULT e la colonna *driver* si leggono dal DISCO a ogni giro**;
> il testo delle decisioni e dei fronti e' **scritto a mano**, ciascuno col suo commit —
> *un'interpretazione non si genera, una condizione del codice si'.*

### A. ✅ ACQUISITO — **in codice E acceso nei run**

| flag | cura | default | **NUDA** | **CAMPAGNA** | sigillo |
|---|---|:--:|:--:|:--:|--:|
| `PEQ_ESATTO` | `C1` rilassamento di `peq` in forma ESATTA | **`False`** | ✅ | ✅ | `7/7` |
| `PEQ_NASCITA_LOCALE` | `C2` nascita LOCALE di `peq` | **`False`** | ✅ | ✅ | `6/6` |
| `SCALA_MIN_PASSO` | `C3` il freno UNA VOLTA per passo | **`False`** | ✅ | ✅ | `6/6` |
| `COES_CAUSALE` | `C4` coesione: istante unico e cono LOCALE | **`False`** | ✅ | ✅ | `5/5` |
| `COES_ADIM` | coesione ADIMENSIONALE | **`False`** | ✅ | ✅ | — *(non ha un sigillo suo)* |
| `ANOM_SIMM` | `C1-bis` anomalia simmetrica, senza pavimento | **`False`** | ✅ | ✅ | `6/6` |
| `INVARIANTI` | `C5` domini di stato, due livelli | **`True`** | ✅ | ✅ | `3/3` |
| `RITMO_WRAP_2PI` | **`A1`** il wrap del ritmo sul periodo GIUSTO *(`2π`)* | **`False`** | ✅ | ✅ | `4/4` + **`6/6` di `CURA 1`** *(`csv/_seal_fork/_sig_cura1/REFERTO.txt`)* |
| `CHI_COOP` | **COOPERAZIONE**: la GEOMETRIA in `perc_geom`, la CARICA in `perc_chi` | **`False`** | ✅ | ✅ | ⚠ *(vedi stato)* |
| `TEMPO_UNICO_MITOSI` | **`CURA 2`** UN SOLO OROLOGIO dentro `mitosi()` | **`False`** | ✅ | ✅ | ⏸ *(l'esito si legge dal referto)* |
| `FASE_2PI` | **§D** `φ` come fase ordinaria su `[0, 2π)` | **`False`** | ❌ | ❌ | ⏸ *(l'esito si legge dal referto)* |

> **LE DUE COLONNE SI LEGGONO DAL SIGILLO DEL DRIVER** — `_cli()` + `_applica_flag(a)`
> in un processo nuovo, stato letto **dal MODULO**. **NUDA** = i soli argomenti
> posizionali; **CAMPAGNA** = gli argomenti che `_g4_prova.py` passa davvero.

**Accese in CAMPAGNA: 10 su 11.** *(Il `default` nel sorgente resta `False`: **i default si cambiano all'epoca 3**, voce `B`.)*

> ### ✅ **NUDA = CAMPAGNA: il driver accende TUTTE le cure approvate da sé.**
> **Un solo modo di lanciare**, e nessuna cura si puo' dimenticare *(decisione di
> Luca, 2026-09-24)*.

### B. 🟨 DECISO DA LUCA, **non ancora in codice**

| decisione | contenuto | dove vive | commit | **già in codice?** |
|---|---|---|--:|:--:|
| **IL FRENO-LEGGE: la forma** | `(d - LAM) <- (d - LAM) * (1 + tanh(dx/d))`. Deriva **esattamente nulla**, e il suo unico prezzo -- la saturazione a `2` -- **si paga zero volte**: `max |dx|/d = 0.0531` su `125 731 076` campioni, **zero oltre `0.5`**. | scheda (11) par.4-quinquies + `D31` nella `STATO` della scheda (1) | `19cea14` | ⚠ **SÌ — la riga va spostata in `A`** |
| **`LAM` STRUTTURALE** | *«nessuna lunghezza sotto `LAM`»* deve diventare **strutturale**, non un freno che ci arriva. Oggi `E4-LAM` la **VERIFICA sempre** (`6/6`), ma la **realizzazione** e' ancora il freno a senso unico. | `D31`, e il punto (2) di `E4-LAM` | `e8d8ba1` | — *(non verificabile da un marcatore)* |
| **EPOCA 3 = i default nel sorgente** | i `default` dei flag delle cure **restano `False`** e si cambiano **all'epoca 3**. Fino ad allora **le accende il DRIVER**, run per run. | questa sezione, colonna *driver* di `A` | *(decisione di Luca, 2026-09-24)* | — *(non verificabile da un marcatore)* |
| **`CURA-3` -- `phi` su `2pi` con le soglie che la seguono** | nella **forma decisa**: frazioni che sul dominio `4pi` danno **ESATTAMENTE** i valori di oggi, flag spento, sigillo con **un processo per braccio**, giro corto contro `CURA 2`. | mandato di Luca; scheda da scrivere | *(mandato del 2026-09-24)* | no *(verificato dal sorgente)* |
| **`TW_SPINORE` bloccato PER SEMPRE** | e' **gia' in codice** come presidio (il simulatore **rifiuta di partire**), ma la decisione *«per sempre»* e' di Luca e va letta qui: **non e' una cura, e' un IMPEDIMENTO** -- la legge non ha mai girato, quindi non ha prodotto nulla da curare. | `CURE VERIFICATE`, sezione *presidio strutturale* | `dd82794a` | ⚠ **SÌ — la riga va spostata in `A`** |

> **La colonna *già in codice* è GENERATA**: cerca il marcatore nel sorgente a ogni giro.
> **È il solo modo perché `B` non diventi una lista di buoni propositi**: il giorno in cui
> una decisione entra nel codice, **la riga si segnala da sola**.

### C. 🟥 APERTO — **una riga per voce, col posto dove vive**

| | fronte | dove vive | esiste ancora? |
|--:|---|---|:--:|
| `1` | **`S08`** -- **se `phi` non e' l'azimut del Bloch, CHE COS'E'?** `Z121` ha **refutato** la frase del docstring *(`R <= 0.18` contro un nullo di `0.016`, criterio `>= 0.90`)*, **ma non ha detto che cosa `phi` SIA**. **E' la domanda del PONTE VERO** *(voce 8)*, presa dall'altro capo | `doc/STATO_RUN.md`, tabella dei sospetti, riga `S08` | — |
| `2` | **`S08_proj`** -- **NON e' `S08`, ed e' un'altra cosa**: `proj` e' ADIMENSIONALE e viene sommato a una LUNGHEZZA; l'unica cosa che gli da' unita' e' il clip *(`A11`)*. **Li avevo confusi nel primo quadro** *(rilievo di Luca)* | scheda (2) `memoria-del-moto`; `Z112` | ✅ **sì** |
| `3` | **LA MAPPA DEI TEMPI** -- quanti tempi ha il sistema, e quali sono la stessa cosa con nomi diversi. **Sospesa dal `PROMPT UNICO`, mai ripresa** | mandato del 2026-09-24, punto (4) | — |
| `4` | **`D33`** -- la repulsione che si spegne al tetto. **E' dentro il perimetro di `CURA 2`** e il criterio `R` l'ha sfiorato: `d0` si muove del `+-3 %`, non del `x2.5` previsto | scheda (7) `mitosi-schwinger` | — |
| `5` | **CHI SPINGE CONTRO IL MURO** -- quali siti spingono `d` verso `LAM` e con che peso. Il bilancio dice **chi fa crescere `d0`**; questo chiede **chi la fa scendere** | scheda (1) + il bilancio di `G4` | — |
| `6` | **IL CLAMP MORTO IN `_cs_arco_da_nodo`** -- `np.maximum(cs_i + cs_j, 1e-12)`. **Protegge da un errore, e `A11` dice di cercare l'errore**: `cs > 0` e' DERIVATO (`cs_floor > 0`), quindi il clamp non puo' mordere. **E' EREDITATO da `step()`, non l'ho aggiunto io** -- e la cura e' toglierlo **dal sito originale**, non solo dalla copia | scheda (9) par.10.1; `:4791` e il metodo estratto | ✅ **sì** |
| `7` | **`S09`** -- l'orologio *non si sposta, si allarga*: il criterio va **riformulato** (rilievo di Luca sul `0746144`) | `CURA 1`, referto dell'orologio | — |
| `8` | **`S11`** e **`S13`** -- sospetti mai promossi ne' chiusi | coda dei sospetti | — |
| `9` | **IL PONTE VERO** -- la torsione presa dal **trasporto SU(2)**, non da `phi`. **E' il motivo per cui `TW_SPINORE` e' bloccato**: quel ponte era INVERSO. Il ponte giusto non esiste ancora | mappa del `4pi`, le due voci `INVERSA`; scheda (8) | — |
| `10` | **IL MERGE DI `main`** -- `doc/PIANO_merge_main.md`. **`fork-su2` e' l'unico ramo vivo.** **E' una DECISIONE DI LUCA: si segnala, non si fa** | `doc/PIANO_merge_main.md` | — |
| `11` | **`mean((dx/d)^2)` NON REGISTRATO** -- direbbe **di quanto** la forma piana sarebbe stata peggiore. **Costa ZERO run in piu'**: una somma, sugli stessi campioni | scheda (11) par.4-quinquies | — |
| `12` | **LA LEGGE DI `CURA 2` E' SALVA PER L'ORDINE DELLE CHIAMATE, non per una guardia** -- `_r_nodo_mitosi` legge `_r_corrente` **prima** che la mitosi allunghi `n`. **Basta spostare una riga.** Le tre guardie hanno **zero salti**, e non per merito loro | scheda (9) par.10; referto di `CURA 2` par.4 | — |

### I RAMI — **letti da `git` a ogni giro**

| ramo | ultimo commit |
|---|---|
| `fork-su2` | 118cabf 2026-09-24 |
| `main` | 252630f 2026-09-10 |

> **`fork-su2` è l'unico ramo vivo.** **Il merge è una DECISIONE DI LUCA**
> *(`doc/PIANO_merge_main.md`)*: **si segnala, non si fa** — ed è la voce `9` di `C`.

<!-- QUADRO-FINE -->

## LO STATO DELLE CURE — **la tabella vera è `CURE VERIFICATE`, più sotto**

| flag | in codice | sigillo | prova |
|---|:--:|--:|---|
| `MEM_MOTO` *(spegnimento)* | ✅ | `8/8` | ✅ `G4` |
| `MEM_MOTO_TUTTO` *(spegnimento)* | ✅ | `10/10` | ✅ `G4-bis` |
| **`RITMO_WRAP_2PI`** *(cura `D34`)* | ✅ | `4/4` | ✅ 600 passi *(`Z123`)* |
| **`FASE_2PI`** *(cura `D35`)* | ✅ | **`6/6`** *(`Z124`)* | ❌ **`2/4` sul giro CORTO: `E1` NON PASSA** *(`Z127`)* |

> **⚠ TUTTI SPENTI O AL LORO DEFAULT: nessuna cura è accesa, e nessuna decisione di default
> è stata presa.** Il passaggio a `True` è la voce **`E3` della coda** *(l'epoca 3)*, ed è
> **una decisione di Luca**.
> **⚠ E `E3` DENOTA DUE COSE in questo documento:** la voce dell'epoca 3 **e** il terzo test
> del §E. **È `Z125`**, ed è dichiarato invece di essere rinominato in silenzio.

## POI, NELL'ORDINE DEL MANDATO

| | lavoro | stato |
|--:|---|---|
| ① | **`A1` / `D34`**: misura · flag · sigillo · prova | ✅✅✅✅ *(`Z117`, `Z123`)* |
| ② | **censimento** `PARTE C` + classi `T/L/E` | ✅ girato sul sorgente vero |
| ③ | **le schede** per §D | ✅ **sette schede** nel registro |
| ④ | **`FASE_2PI`** in codice, dietro flag, **sigillata** | ✅ `6/6` *(`Z124`)* |
| ⑤ | **la prova + i test `E1`-`E4`** | ❌ **il giro CORTO la BOCCIA: `E1` NON PASSA** *(`Z127`)*. Il run a 600 passi **NON è stato lanciato** |
| ⑥ | **`TEMPO_UNICO`**: scheda, flag, sigillo, prova | ⏸ la seconda cura |
| ⑦ | **`PROBLEMI-CHK3`**, `FAMIGLIE`, `FASCE-TAU`, `PAT-1`/`PAT-2` | ⏸ |
| ⑧ | **`CHECKPOINT`** — **ci si ferma e si aspetta Luca** | ⏸ |

## LAVORI A METÀ — **nessuno**

Ogni lavoro è a un punto pulito. **I fallimenti sono committati come reperti e poi corretti,
coi giri rifatti per intero.**

<!-- PUNTO-DI-RIPRESA:FINE -->

> ## ⚠ DAL TAG `epoca-2`: **SISTEMA D**
> **Nuova carica (dallo spinore), scala minima `LAM` su `d` e `d0`, coesione adimensionale e causale** — piu' la **cura del mondo-dopo-i-flag**, che cambia ogni run.
> **Ogni numero misurato PRIMA appartiene all'EPOCA 1 e NON si confronta con l'epoca 2.**
> `EPOCA 2 = blob del simulatore del tag (`4954fe5b`, byte grezzi) + configurazione con `CHI_COOP`, `SCALA_MIN`, `COES_ADIM` ACCESI`. **Un run a flag spenti su quel blob e' ancora EPOCA 1**, e non e' un'opinione: lo provano `Z1` e `Z1c`, byte-identici.

> ### ⚠ CORREZIONE DEL 2026-09-21 — **la frase qui sopra e' IMPRECISA, e la lascio leggibile**
> **Cio' che avevo scritto:** *«un run a flag spenti su quel blob e' ancora EPOCA 1, lo provano `Z1`
> e `Z1c`».* **VALE SOLO CON L'ARGV NUDO.**
> **Perche' e' sbagliata:** `Z1c` confronta contro **«PRIMA + la cura del mondo»**, non contro
> **«PRIMA»** — la cura e' innestata su ENTRAMBI i bracci di proposito, senno' il sigillo misurerebbe
> LEI invece dei tre flag. **Quindi `Z1c` NON dice nulla sull'equivalenza con l'epoca 1.** A dirlo e'
> `Z1b`, che misura la differenza: **`n` 2569 -> 2580, archi 527 308 -> 526 202.** La cura e'
> **categoria D** e fa finalmente agire gli **otto** flag sul vuoto.
>
> **LA CLASSIFICAZIONE CORRETTA, in quattro righe:**
> ```
> EPOCA 1       blob PRECEDENTE al tag, qualunque configurazione
>
> EPOCA 1       blob del tag, argv NUDO, tre flag spenti
>               -> byte-identico, lo prova Z1
>
> EPOCA 1-bis   blob del tag, argv del FORK, tre flag spenti
>               -> NON e' epoca 1: e' epoca 1 CON LA CURA DEL MONDO.
>                  Il vuoto nasce coi flag del run invece che coi default. Lo misura Z1b.
>
> EPOCA 2       blob del tag + CHI_COOP, SCALA_MIN, COES_ADIM ACCESI
> ```
>
> **⚠ LA CONSEGUENZA PRATICA, ed e' operativa:** **i run del FORK di epoca 1 NON si riproducono sul
> blob nuovo, nemmeno a flag spenti** — **e NON E' UN DIFETTO.** Chi vuole rigirarli deve usare il
> **blob PRECEDENTE** (`git cat-file -p <commit>:soliton_simulator.py`, scritto in BINARIO).
>
> **Il tag NON si sposta e NON si riscrive:** un tag pubblicato che cambia sotto i piedi e' peggio
> dell'imprecisione. La correzione vive qui e in una `git notes` sul commit del tag.



---

## ⓪ LE CANCELLAZIONI DEL 2026-09-21 — **l'elenco completo, prima di spostare qualunque cosa**

**Criterio applicato:** nessun file tracciato da git; scratch ricreato dagli script stessi.
**Verificato DOPO:** `git status` non segnala **nessun** file tracciato mancante.

### Dentro il repository — **611 MB**, scratch di sigilli
| cartella | MB | chi la ricrea | verdetto salvato? |
|---|---|---|---|
| `csv/_seal_fork/_sig_sep` | 180 | `_sigillo_sep_driver.py` | `_sigillo_sep_driver.txt` |
| `csv/_seal_fork/_sig_chibasc` | 167 | `_sigillo_chibasc_driver.py` | `_sigillo_chibasc_driver.txt` |
| `csv/_seal_fork/_sig_ramo_D` | 131 | `_sigillo_ramo_D.py` | `_sigillo_ramo_D_2026-09-21_*.txt` |
| `csv/_seal_fork/_sig_chicoop` | 50 | `_sigillo_chicoop.py` | ⚠ **NESSUNO** — vedi sotto |
| `csv/_seal_fork/_sig_traccia_d0` | 50 | `_sigillo_traccia_d0.py` | ⚠ **NESSUNO** — vedi sotto |
| `csv/_seal_fork/_sig_z1c` | 34 | `_sigillo_Z1c.py` | `_sigillo_Z1c_2026-09-21.txt` |

**Piu' due copie del driver, MAI tracciate e rigenerate a ogni giro del sigillo:**
`csv/_test_fork/_driver_prima_chibasc.py` · `csv/_test_fork/_driver_prima_sep.py`.

### ⚠ UN ERRORE, e il file e' stato RIPRISTINATO
`csv/_seal_fork/_sig_traccia_d0/` conteneva **`_sim_prima.py`, che ERA TRACCIATO** — ed e' una
**copia del simulatore**, cioe' esattamente cio' che il par.5-quinquies impone di conservare.
**Ripristinato** con `git cat-file -p HEAD:` scritto in **binario** *(mai `git checkout`: trappola
CRLF)*, `sha1` byte grezzi **`01146a16`**.
**Perche' e' sfuggito:** il mio censimento contava i file tracciati **solo** per le cartelle sopra
i 40 MB della tabella; per gli scratch dei sigilli mi sono fidato della **regola generale**
*(«sono usa-e-getta»)* invece di ricontrollare cartella per cartella. **La regola era giusta per
sei cartelle su sette.**

### ⚠ DUE SIGILLI SENZA OUTPUT COMMITTATO, ed e' un debito aperto
`_sigillo_chicoop` (**8/8**) e `_sigillo_traccia_d0` (**4/4**): il par.5 dice *«committa gli output
col verdetto»* e **non l'ho fatto** — i numeri vivono solo nei messaggi di commit. **Lo scratch non
li conteneva** (sono `.npz`, non stdout), quindi cancellarlo non ha perso nulla: **i due sigilli
vanno RIGIRATI e i loro output committati.**

### Fuori dal repository — **1.2 GB**
| percorso | MB | cosa era |
|---|---|---|
| `%TEMP%/claude/c--Users-lpeano-soliton-simulator/b8f19b37-.../` | 1100 | scratchpad di una **sessione morta**, file piu' recente del **2026-09-19** |
| `%TEMP%/claude/bash-edit-diff` | 106 | cache temporanea dell'editor |

**Verificato prima di cancellare:** l'unico processo `python` vivo era il ramo D — **nessuna
sessione parallela**.

### ⚠ E IL CONSUMATORE VERO NON ERA NESSUNO DI QUESTI
Il disco continuava a scendere anche dopo le pulizie. **E' il PAGEFILE**, cresciuto da **18.7 a
19.7 GB** sotto i run pesanti. **E' gestito da Windows e non lo tocco**, ma spiega i cali che
attribuivo al repo.

### Cosa NON e' stato cancellato, e perche'
| cartella | MB | motivo |
|---|---|---|
| `_ab_grav_ampiezza` · `_ab_coppia_reciproca` | 506 + 506 | **NON in `INVENTARIO`**: senza il comando documentato sono **gia' irrecuperabili**. Cancellarle perderebbe cio' che nessuno puo' rifare |
| `_g6000` | 1314 | in inventario, rigenerabile — ma **ore di CPU** |
| `_ab_A` · `_ab_B` | 923 + 105 | i dati dell'A/B di `chi_basc`, dietro `Z73`-`Z77` |
| `_ab_C_solo_chicoop_FERMATO` | 346 | l'archivio del primo lancio di D, **conservato** |

---


---

## 🗃 TABELLA DI CORRISPONDENZA — **gli archivi `.pkl` spostati su `E:` il 2026-09-21**

> **I documenti STORICI non sono stati riscritti** — referti, task history, voci del registro
> continuano a citare i percorsi `C:`, **ed e' corretto cosi'**: un referto del 19 settembre
> riscritto con un percorso del 21 diventa un documento che non e' mai esistito.
> **Questa tabella e' il ponte.** Radice nuova: **`E:\soliton_archivio\`**, con la **stessa
> struttura di cartelle** del repository.
> **Verifica:** `sha1` dei byte del file **compresso**, originale contro copia, **187 file su 187**.
> Il registro riga-per-riga, con ogni `sha1`, e' in **`doc/SPOSTAMENTO_archivi.tsv`**.

| percorso VECCHIO (citato nei documenti storici) | percorso NUOVO | file | MB |
|---|---|---:|---:|
| `csv/_test_fork/_g6000/` | `E:\soliton_archivio\csv\_test_fork\_g6000\` | 45 | 1313.6 |
| `csv/_test_fork/_ab_A/` | `E:\soliton_archivio\csv\_test_fork\_ab_A\` | 25 | 923.0 |
| `csv/_test_fork/` | `E:\soliton_archivio\csv\_test_fork\` | 36 | 631.7 |
| `csv/_seal_fork/` | `E:\soliton_archivio\csv\_seal_fork\` | 24 | 428.7 |
| `csv/_test_fork/_ab_C_solo_chicoop_FERMATO/` | `E:\soliton_archivio\csv\_test_fork\_ab_C_solo_chicoop_FERMATO\` | 10 | 345.8 |
| `csv/_test_fork/_fin_B/` | `E:\soliton_archivio\csv\_test_fork\_fin_B\` | 11 | 308.3 |
| `csv/_seal_fork/_ab_grav_ampiezza/B/` | `E:\soliton_archivio\csv\_seal_fork\_ab_grav_ampiezza\B\` | 9 | 253.5 |
| `csv/_seal_fork/_ab_coppia_reciproca/B/` | `E:\soliton_archivio\csv\_seal_fork\_ab_coppia_reciproca\B\` | 9 | 253.5 |
| `csv/_seal_fork/_ab_coppia_reciproca/A/` | `E:\soliton_archivio\csv\_seal_fork\_ab_coppia_reciproca\A\` | 9 | 252.7 |
| `csv/_seal_fork/_ab_grav_ampiezza/A/` | `E:\soliton_archivio\csv\_seal_fork\_ab_grav_ampiezza\A\` | 9 | 252.7 |

**⚠ E il COMANDO che rigenera un archivio NON e' stato cambiato da nessuna parte.**
La **posizione** di un archivio e il **comando** che lo produce sono due cose diverse:
un run scrive su `C:`, e solo dopo l'archivio viene spostato. Cambiare i comandi in
`INVENTARIO_strumenti.md` li renderebbe **sbagliati**.

---
# ⚠ LA CODA UNICA — **l'ordine del lavoro, e l'UNICA fonte dell'ordine**

> **Decisione di Luca, 2026-09-21.** **Se un mandato sembra contraddire questa coda, VINCE LA CODA
> e lo si SEGNALA a Luca.** Ogni voce si spunta quando e' fatta.

| # | voce | mandato | stato |
|---|---|---|---|
| 1-5 | `CHI_COOP` · `SCALA_MIN`+`COES_ADIM` · sigillo `11/11`+`Z1c` · ramo D · tag `epoca-2` | perentorio, EPOCA | ✅ **FATTE** |
| **4-bis** | **DIAGNOSI DEI PICCHI DI `n1`** | GLOBALE §1 | ✅ **passo `1126`, arco `3352-506`, `peq = -4.85e-04`**; i tre numeri misurati *(`Z93`, `Z94`)* |
| **C1-PEQ-ESATTO** | `PEQ_ESATTO` — rilassamento in forma esatta | GLOBALE §2① | ✅ **`7/7`** *(`Z95`)* |
| **C2-PEQ-NASCITA** | `PEQ_NASCITA_LOCALE` — nascita locale di `peq` | GLOBALE §2② | ✅ **`6/6`** *(`Z96`)* |
| **C3-SCALA-MIN-PASSO** | `SCALA_MIN_PASSO` — il freno una volta per passo | GLOBALE §2③ | ✅ **`6/6`** *(`Z97`)* |
| **C4-COES-CAUSALE** | `COES_CAUSALE` — istante unico e cono locale | GLOBALE §2④ | ✅ **`5/5`** *(`Z98`)* |
| **C1BIS-ANOM-SIMM** | `ANOM_SIMM` — il pavimento `1e-9` tolto | 21/9 §② | ✅ **`6/6`** *(`Z99`)* |
| **C5-INVARIANTI** | `INVARIANTI` — 42 domini, due livelli | mandato `C5` | ✅ **`3/3`** *(`Z100`)*; **accesi di default** |
| **driver** | inoltra tutte le cure | 21/9 §① | ✅ **`3/3`**, 9 opzioni su 9 in entrambi i versi |
| **V** | **VALIDAZIONE a 600 passi** | GLOBALE §3 | ⚠ **`6` criteri su `8`** *(`Z101`)*. **`nsub` max `4`**, `peq >= 0`, zero sotto `LAM`, **zero violazioni**. **NON reggono `d0` e `d/d0`** |
| **CHK2** | **CHECKPOINT 2** | GLOBALE §3 | ✅ **raggiunto e riferito a Luca.** **IL RUN LUNGO NON SI LANCIA** |
| **D0** | **CHI FA SCAPPARE `d0`** | 21/9 | ✅ **MISURATO: e' IL FRENO.** Gli scrittori spingono **giu'** `-1.543e+05`, il vincolo **aggiunge** `+3.205e+05`. **`S10` inerte, `S09` verso il BASSO** *(`Z102`)*. **La spinta e' la DISCESA CANCELLATA**, `|dx|·min(1, LAM/d0)`, e **si indebolisce da sola**: dal `91 %` al `24 %` |
| **G1** | **§1 QUANTO CONTA IL DISEGNO** — `L_disegno/d` per arco, per regione, nel tempo, e la correlazione col CENTRO del disegno | GLOBALE-DISEGNO §1 | ✅ **FATTO** *(`3c03223`, `Z103`)*: mediana `L/d` da **`0.982`** a **`1.217`**, **un arco su quattro oltre il doppio** al passo 600, e **dipendenza dal centro su 5 snapshot su 5**. **Entrambe le letture fissate prima si verificano** |
| **G2** | **§2 DOVE SPINGE LA GRAVITA'** | GLOBALE-DISEGNO §2 | ✅ **FATTO.** Il saldo vive **sul CONFINE vuoto-massa** *(`-1.4150`/arco, `107 %` del totale, `Z105`)*; i 20 archi col `|saldo|` maggiore sono **`20/20` nel VUOTO** e il confine e' **DIFFUSO** su `96 429` archi all'**`85 %` del plateau**; e **l'`85.05 %` degli archi-passo e' INCOLLATO AL TETTO**, con il **`99.69 %` del saldo** da incrementi saturi *(`Z106`)*. **`A11` corollario 6** |
| **G3** | **§3 PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE** | GLOBALE-DISEGNO §3 | ✅ **FATTA.** ✅ sigillo `7/7` · ✅ controllo involucro `206/0`. **ESITO: la gravita' NON e' il motore.** Rapporto di `d0` **`1.2321` → `1.2211`**, differenza `0.9 %`. **La compressione PEGGIORA** *(`d/d0` `0.7489` → `0.6258`)* e **lo stress CROLLA del `70 %`** *(`7.866` → `2.321`)*. `6/8` in entrambi, **gli stessi due**. `S08_proj` e' il maggior scrittore positivo *(`Z107`)* |
| **G4** | **§4 PROVA DI SPEGNIMENTO: la MEMORIA DEL MOTO** — flag `MEM_MOTO` | GLOBALE-DISEGNO §4 | ✅ **FATTO** *(finito 14:39:27)*. **La memoria del moto NON e' il motore** — `d0` cresce ancora *(`1.1607`)* — **ma ne porta il `62 %`**, e **spegnendola la COMPRESSIONE SPARISCE**: `d/d0` da `0.7489` a `0.8546`, **`7` criteri su `8`**, il migliore mai misurato. **Il motore resta IL FRENO: `+218 %`** *(`Z109`)* |
| **G4-bis** | **IL SECONDO BRACCIO: spegnere l'INTERO blocco di `mem_mot`** | richiesta di Luca, 2026-09-22 | ✅ **CHIUSO, letture comprese.** Bilancio **`9.498e-14`**, **`Δ` NON monotono** *(`Z115`)*. **I TRE BRACCI: `6/8` · `7/8` · `6/8`** — **il parziale e' il migliore** *(`Z116`)*. **E `d/d0` dell'intero-blocco vale `1.000` per 360 passi — il migliore mai misurato — poi CROLLA mentre `n` fa `+30 %`** |
| **G4-MEMARCO** | **`MEM_ARCO` — LA MEMORIA DEL MOTO TRADOTTA IN FORMA RELAZIONALE** *(aggiunta di Luca al §4, 2026-09-22)* | GLOBALE-DISEGNO §4 | ⏸ **DERIVATA SI', CODICE NO, prima del `CHK3`.** **Dopo** lo spegnimento di `MEM_MOTO`: se il sistema **si rompe** senza, `MEM_ARCO` e' **la cura da proporre**; se **sta in piedi**, resta **registrata come alternativa** |
| **SCALE-TW** | **LE SCALE DELLA TORSIONE: un'analisi completa, DA CAPO** | mandato di Luca **ricevuto alle 17:44** del 2026-09-22 | ⏸ **NON SI COMINCIA OGGI — LO DICE IL MANDATO STESSO.** Posizione: **dopo** l'esito di `G4-bis` *(✅ fatto)* e **`REG-R`**, **prima** del `CHK3`, perché le sue proposte alimentano le cure di **`D31`** e **`D33`**. **IL PERCHÉ:** tutte le soglie in multipli di `π` sono state decise **PRIMA DEL FORK**, e oggi **tre premesse pre-fork sono cadute** — `D25`, `D27` e il **`2.5π` di `D33`**. **LE QUATTRO PARTI:** ① **CENSIMENTO da AST** di ogni scala in `π` *(`PHI_CRIT`, `2π+π`, `0.3·tanh`, il punto medio `~3.5π`, `TW_TETTO`, `_w8`/`_w4`, `satura()`/`GAMMA`, `tau_pp`, **e le costanti dentro le formule**: il `3.0` di `tanh(3·(…))`, il `0.02` della repulsione, il `0.3`)*, **col caso nascosto `PHI_CRIT + twist_max`, che non è un letterale** · ② **MISURA del regime di OGGI** sugli snapshot già scritti · ③ **ANALISI con `A11`**, scala per scala, **7 punti ciascuna**, comprese **le DISCONTINUITÀ** *(il `%` di `_w8` fa **saltare** il valore di `8π`)* e **la SIMMETRIA** · ④ **PROPOSTA DERIVATA** *(TIENI / MODIFICA / RENDI MORBIDA / TRASFORMA / TOGLI / DA DECIDERE)*. **IL PRIMO DIFETTO È GIÀ INDICATO DA LUCA:** `TORS_4PI` a `:789` dice *«soglia 4π»* e *«default off»*, **ma la soglia è `3π` e il flag è ACCESO** — commento contro codice, e **fa fede il codice**. **ESITO: una SCHEDA nuova nel registro** più una **tabella una-riga-per-scala** per il `CHK3` |
| **PROBLEMI-CHK3** | **IL PIANO DEI PROBLEMI APERTI** — per ciascuno: **la domanda da chiudere · la misura o derivazione che la chiude · da che scheda dipende · cosa blocca**. **NESSUNA CURA.** | mandato di Luca, 2026-09-22 | ⏸ **NON COMINCIATO** *(triage: non ci sta entro le 17:45)*. **E' il documento che Luca guardera' per decidere.** **I sette problemi sono gia' elencati nel mandato e nelle schede**: `D31` freno *(5 candidati, e il test che devono passare e' gia' scritto: `Z113`)* · **LA SPINTA VERSO IL MURO** *(chi spinge il `13.7 %` contro il confine? `A11`: un vincolo che lavora tanto e' un ALLARME, e la legge che spinge va trovata PRIMA di scegliere il vincolo)* · `MEM_ARCO` *(`Z104`, `Z112`, `Z115`)* · `SPINTA_LOCALE`/`POZZO_D` · `D32` i due tempi *(**se si unificano, le leggi che usano `tau_pp` cambiano significato: vanno elencate**)* · `D33` *(dipende da `SCALE-TW`)* · **l'ORDINE motivato dai numeri e dalle dipendenze fra schede** |
| **FAMIGLIE** | **IL CERCATORE DI FAMIGLIE DI DIFETTI** — uno strumento che legge il sorgente *(AST)* e segnala i punti che ricadono nelle famiglie **gia' note**, ciascuna nata da **difetti reali**. **SOLA LETTURA: nessuna cura, e NESSUNA PROPOSTA DI SOLUZIONE** | mandato di Luca, 2026-09-22 | ⏸ **NON COMINCIATO.** Posizione: **dopo** `PROBLEMI-CHK3`.
| **FASCE-TAU** | **LA CRESCITA E' COORDINATA COL TEMPO PROPRIO?** — l'espansione non dev'essere omogenea in senso **assoluto**, ma omogenea **DENTRO UNA FASCIA DI TEMPO PROPRIO**: cio' che condivide lo stesso `r` cresce insieme, e fasce diverse crescono in modo diverso, **in proporzione a quanto il tempo scorre li'** | idea di Luca, 2026-09-22 sera | ⏸ **NON COMINCIATA.** Posizione: **dopo `PROBLEMI-CHK3`**, **insieme alle misure cosmologiche `M1`-`M4`**, con cui condivide la domanda *(stiramento contro nucleazione, espansione senza centro)*.
**L'ANALOGIA, ed e' quella che da' senso alla misura:** le fasce di `r` sono **la foliazione del modello** — l'analogo delle **ipersuperfici a tempo cosmico costante** di Friedmann.
**LA MISURA — solo snapshot GIA' SCRITTI, nessun run:** dividere la popolazione in fasce di `r`; per ogni fascia il **fattore di crescita di `d0` fra snapshot consecutivi**; e poi **confrontare la DISPERSIONE DENTRO una fascia con la DIFFERENZA FRA fasce** *(e' il rapporto che decide: senza di esso una differenza fra fasce non si distingue dal rumore interno)*.
**LE DUE LETTURE, SCRITTE PRIMA:** ① i fattori **DIFFERISCONO fra fasce, in proporzione ai tempi propri** → **la crescita e' coordinata col tempo proprio, l'ipotesi REGGE**; ② i fattori sono **UGUALI in tutte le fasce** → **la crescita e' omogenea in tempo di COORDINATA**, cioe' **la firma di un vincolo applicato a ogni passo, CIECO al tempo proprio**. **⚠ La lettura ② e' anche un TEST INDIPENDENTE SU `D31`**, e non usa il bilancio: arriverebbe alla stessa conclusione da un'altra strada.
**DOVE:** sul braccio **INTERO-BLOCCO di `G4-bis`**, **nei 360 passi in cui `d/d0` vale `1.000`** *(`Z116`)*, **dove l'espansione era trasparente** — senza tensione ne' compressione a coprirla.
**⚠ E UN VINCOLO DI ORDINE, posto da Luca:** `r` **di oggi e' la grandezza su cui pesano `D32` e `D34`.** **La misura si fa DOPO la correzione del ritmo, oppure si rifa'.** *(Misurare la foliazione con un orologio che si sa difettoso darebbe fasce sbagliate, non una risposta sbagliata: peggio, perche' sembrerebbe una risposta.)* |
• **`F1` NUMERI SCELTI** nelle formule fisiche: costanti **letterali non derivate** *(`D01`; il `0.02` della repulsione, il `0.3` della modulazione, il `3.0` di `tanh(3·…)`, il `π/4` dello shift di fase)*.
• **`F2` STATISTICHE GLOBALI IN LEGGI LOCALI**: `median`, `mean`, `sum` su array dell'**intero sistema** dentro una legge che agisce su **un arco o un nodo** *(`D01`, `A2`)*.
• **`F3` LIMITI**: ogni `clip`, `maximum`, `minimum`, pavimento o tetto, **col valore** e **se ha un contatore** *(`A11`, `D31`)*.
• **`F4` SCRITTURE DI STATO SENZA TRACCIA** *(`D04`)* — **gia' fatto per `d0`: si RIUSA il criterio** di `csv/_test_fork/_scrittori_non_tracciati.py`, **rami esclusivi compresi**, esteso alle altre grandezze.
• **`F5` FASI COL PERIODO SBAGLIATO** *(`D34`)*, **dal censimento in corso**.
**PER OGNI PUNTO:** riga · funzione · **flag che lo governa** · famiglia · **attivo o dormiente** · **se e' gia' coperto** da un `Dxx` o da una scheda.
**⚠ E L'ESITO E' OBBLIGATORIO PER OGNI PUNTO, senza eccezioni:** «**gia' noto**» · «**candidato**» · «**NON e' un difetto, perche'…**». **Nessun punto resta senza esito**, e **non si classifica come difetto cio' che non lo e'** — un cercatore che segnala tutto non lo legge nessuno *(e' il difetto gia' misurato di `csv/_blob_nelle_voci.py`)*.
**⚠ I CANDIDATI NON DIVENTANO DIFETTI ACCLARATI AUTOMATICAMENTE:** vanno nei **`SOSPETTI`**, e **si promuovono UNO PER UNO con la prova**. *(Un cercatore che crea difetti da solo li crea anche dove non ci sono.)*
**COLLAUDO `P1-sexies` PER FAMIGLIA**, ciascuno **col caso che DEVE fallire** e **un caso NASCOSTO**: una costante passata da una **variabile**, una mediana calcolata in **un'altra funzione**. |
| **CHK3** | **CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate PRIMA** | GLOBALE-DISEGNO §5 | ⏸ **QUI CI SI FERMA.** Le cure solo **DERIVATE, non scritte** |
| **CHK3-D** | **Nel referto del `CHK3`, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE»** — `D27` *(quattro componenti)* e `D25` *(il tempo che non scorre)* **contro `G1`, `G2`, `G3`, `G4`** | richiesta di Luca, 2026-09-22 | ⏸ **AL CHECKPOINT, non prima.** **Solo misure e letture del sorgente, nessuna cura.** **Le conseguenze sulle tre prove dell'ipotesi si scrivono come DOMANDE.** Il costo e' dichiarato qui sotto, e **i run si fanno solo col via libera di Luca** |
| **PATTERN** | **`doc/PATTERN_DI_PROVA.md`** — la lista di controllo di ogni prova | MANDATO-PATTERN | ✅ **SCRITTO** *(48 righe)*, **5 STANDARD + 1 IN PROVA**, una riga sola in `CLAUDE.md`. **Il collaudo del §4 NON e' tutto verde:** vedi le due voci qui sotto |
| **PAT-1** | **`_dove_spinge_la_gravita.py` non rispetta il pattern `5`** *(nessun CONTROLLO DELL'INVOLUCRO)* | PATTERN §4 | ⏸ **PRIMA del suo prossimo uso.** Sostituisce `_traccia_d0` e rigioca dalla semina, **senza mai verificare che la rigiocata riproduca `_val600`**. **I numeri di `Z105`/`Z106` restano quelli misurati**, ma la loro FEDELTA' alla validazione **non e' stata dimostrata** |
| **PAT-2** | **`_spegni_grav_bifase.py:184` non rispetta il pattern `2`** *(usa `max\|Δ\|` invece delle FIRME)* | PATTERN §4 | ⏸ **PRIMA del suo prossimo uso.** `confronta()` e' un controllo di IDENTITA' e va fatto sui **byte**: oggi `+0.0` contro `-0.0` passerebbe per identico. *(Il cast dei complessi e' gia' corretto, `abc5b49`.)* |
| **PROVE** | **LE TRE PROVE DELL'IPOTESI DELLA GRAVITA' A SPINTA** — ① due masse si avvicinano? ② con che legge? ③ tutti i corpi cadono uguale? | `doc/IPOTESI_gravita_a_spinta.md` | ⏸ **DOPO il run lungo dell'epoca 3.** **CONDIZIONI DI AVVIO, TUTTE:** il **disegno FUORI dalla gravita'** *(`Z103`, sigillato)* · la **spinta LOCALE con le dimensioni giuste** *(via il `median(d0)`)* · un **run lungo SANO** coi criteri assoluti che reggono *(oggi 6 su 8)* · la **memoria del moto risolta** *(`Z104`)*. **Fino ad allora sono il BERSAGLIO, non un compito** |

| **C5RES-INVARIANTI** | **I RESIDUI DI `C5`** — **`I4`** la scatola nera *(rigiocare da solo il passo in cui scatta un invariante)*, **`I5`** la tabella degli underflow **per RIGA**, e la **MODALITA' FINE** *(controllo dopo OGNI scrittura invece che a fine passo)* | mandato `C5`, decisione di Luca 21/9 | ⏸ **DOPO la cura di `d0` e PRIMA del run lungo. Stasera no.** |
| **8-bis** | **ARCHIVIO A ROTAZIONE** — si scrive su `C:`, ogni snapshot completo va su `E:` con `sha1` dei byte compressi, sigilli `R1`-`R5` | archivio | 🔒 prima del run lungo |
| **PROVA-COMB** | **LA PROVA COMBINATA: TUTTE LE CURE APPROVATE ACCESE INSIEME** — 600 passi, stesso seme e scena, **letture della validazione** *(8 criteri)* **e BILANCIO di `d0`**, contro il **riferimento di `G4`** | decisione di Luca, 2026-09-22 | 🔒 **PRIMA del tag `epoca-3`, e dopo che Luca ha approvato le singole cure.** **PERCHE' SERVE, ed e' il par.1 letto al contrario:** la regola d'oro dice *un interruttore alla volta* **per capire**; ma un sistema che gira con **otto** cure accese non e' mai stato provato **in quella configurazione**. **Ogni cura e' sigillata DA SOLA; l'insieme no.** **COSA DECIDE:** se i criteri che REGGONO da sole reggono anche **insieme**, e se il bilancio di `d0` **chiude** con tutte accese. **Se un criterio cade solo nella combinazione, e' un'INTERAZIONE fra cure**, e va trovata prima dell'epoca 3. **LE CURE DA ACCENDERE si leggono dalla sezione `CURE VERIFICATE`** — solo quelle con stato **APPROVATA DA LUCA**. **Il riferimento di paragone e' `_g4_riferimento`**, gia' sul disco: nessun run in piu' per il confronto |
| **E3** | **EPOCA 3 + RUN LUNGO** — tag `epoca-3`, 3000 passi, `M1`/`M4` leggere durante il run | GLOBALE §4 | 🔒 **solo dopo che i criteri REGGONO.** Nessun confronto con le epoche precedenti.
**⚠⚠ CHE COSA E' L'EPOCA 3, deciso da Luca il 2026-09-22:** **sono i DEFAULT CAMBIATI NEL SORGENTE, non un elenco di flag da ricordare.** *(Oggi **`1` cura su `9`** ha il default acceso: le altre **le accende l'argv del driver, run per run**. Non sono «nel codice», e dal sorgente non si vedrebbe — `P2`.)*
**① UN COMMIT A SE' PER OGNI CURA APPROVATA.** Il default passa a **`True`** nel codice, **una cura per commit** *(par.5: un commit = un cambiamento logico)*.
**② CON IL SIGILLO CHE DIMOSTRA L'EQUIVALENZA:** un run **con i VECCHI argomenti** *(cioe' col flag passato esplicitamente)* **resta IDENTICO** a prima del cambio di default. **E' la stessa forma del `T9` di `MEM_MOTO_TUTTO`** *(`206` campi identici, `0` diversi)*: **cambiare un default NON deve cambiare un run che quel flag lo passava gia'**.
**⚠ E IL PRECEDENTE DICE PERCHE' SERVE:** quando `STEP2_OROLOGIO` passo' a `ON` di default, *«l'assenza del flag»* smise di significare `OFF`, e **i rami di controllo diventarono duplicati del ramo di prova** — un sigillo che sarebbe **PASSATO SEMPRE**. **Quando si ribalta un default si cercano, NELLO STESSO COMMIT, tutti i punti che ottenevano il vecchio comportamento per OMISSIONE.**
**③ E DUE PRESIDI, perche' una regola che dipende dal ricordarsene non e' un presidio** *(`A9`)*: **(a)** il **driver RIFIUTA DI PARTIRE** se una cura **approvata** risulta **spenta** — non un avviso, un rifiuto; **(b)** il **referto di OGNI run STAMPA LO STATO DI TUTTE LE CURE**, cosi' la configurazione **sta nel dato**, non nel comando *(`P6`: un file che si distingue solo per il nome non e' un dato)*.
**LA LISTA DELLE CURE APPROVATE si legge dalla sezione `CURE VERIFICATE`**, che e' generata: **una sola fonte, e il driver la legge invece di avere una copia sua.** |
| 6 | strumento cosmologico `M1`-`M4`, **sul nuovo D** | COSMOLOGICO | ⏸ |
| 7 | **`Z47` PARTE ①** — ricognizione di `pos` nella fisica *(sola lettura)* | `MANDATO_Z47_coda` | ⏸ |
| 8 | `M2`/`M3` cosmologici *(pesanti)* | COSMOLOGICO | ⏸ |
| 9 | **CHECKPOINT FINALE a Luca** | — | ⏸ |
| 10 | `Z47` PARTE ② — lo stacco | `MANDATO_Z47_coda` | 🔒 **NON parte senza il via libera di Luca** |

> **⚠ AGGIUNTA DI LUCA AL §4 (2026-09-22): LA MEMORIA DEL MOTO NON SI BUTTA, SI TRADUCE.**
> **L'osservazione, e il codice la conferma** (`:5631-5648`): la legge **parte gia' da una
> grandezza RELAZIONALE**, `dtw = twn[jj] - twn[ii]` **sull'arco**; la porta in un **vettore di
> nodo** con `dirarc` *(che viene da `pos`, cioe' dal DISEGNO)*; e poi la **riproietta sull'arco**
> con lo stesso `dirarc`. **In `d0` entra `proj`, un numero CON SEGNO PER ARCO.**
> **`MEM_ARCO`** *(flag nuovo, spento di default, byte-inerte)*: la memoria vive **sull'arco
> orientato**, positiva da `i` a `j`, e si aggiorna con la stessa legge,
> `m_arco <- (1-plast)*m_arco + plast*dtw`. **Nessuna posizione, nessuna direzione del disegno.**
> `plast` e il peso della massa **derivati in forma LOCALE, senza `Imed` globale**. **Il tetto e'
> il PASSO CAUSALE**, non `0.01*median(d0)`.
> La parte **«di lato»** *(`dir_laterale`, lo spostamento di fase a `:6016`, la rotazione
> orbitale)* diventa **CIRCOLAZIONE sui giri chiusi di archi**, **la stessa grandezza
> dell'olonomia**. **Per ora solo DERIVATA e riportata, non scritta.**
>
> **⚠ E UN FATTO DAL SORGENTE CHE LA DERIVAZIONE DEVE AFFRONTARE, non un'obiezione:** il giro
> per il nodo **non e' l'identita'**. `np.bincount(ii, dtw*dirarc) + np.bincount(jj, dtw*dirarc)`
> diviso `_deg` **MEDIA l'arco con TUTTI GLI ALTRI ARCHI DELLO STESSO NODO**, pesati dalle loro
> direzioni **nel disegno**. **Cio' che passa per `pos` non e' solo un giro: e' il PESO con cui i
> vicini si mescolano.** Una `m_arco` puramente per-arco **perderebbe l'accoppiamento col
> vicinato**, e la derivazione deve dire **se quell'accoppiamento serve** — e se si', **da
> dove viene il peso una volta tolto il disegno.**

> **▶ `G3` IN CORSO — avvio committato il 2026-09-22.**
> **① SIGILLO, PASSATO PRIMA DELLA PROVA:** `csv/_seal_fork/_sigillo_spegni_grav.py` blob
> `cb506019`, **`7/7`** *(commit `76114e0`)*. `T5` e' il criterio che lo chiude ed e'
> **strutturale**: l'AST dice che **una sola ramificazione** dipende da `GRAV_BIFASE` *(riga
> `5661`)*, quindi **nessun'altra legge PUO' essere gated su quel nome**.
> **② CONTROLLO POSITIVO: ✅ PASSATO, `206` campi identici e `0` diversi.** 120 passi a flag
> INVARIATO, **snapshot contro snapshot** al passo 120 con `_val600/scena_000120.pkl.gz`.
> **⚠ AL PRIMO GIRO AVEVA DETTO `1` CAMPO DIVERSO, E A SBAGLIARE ERA IL CONFRONTO:** metteva la
> **rete VIVA a fine processo** contro uno snapshot del **passo 120**, e `_g_kernel_alpha_tot`
> — un contatore diagnostico di `_pesi()` — continua a salire dopo la scrittura. **Non una
> differenza fra i due run: una differenza fra due ISTANTI.** I due snapshot hanno entrambi
> `1523`. **Il run non e' stato rifatto: era giusto, ed e' stata riparata la LETTURA.**
> **Serve a un'affermazione DIVERSA da quella del sigillo:** il sigillo dice che *il FLAG* e'
> chirurgico, il controllo dice che *il mio INVOLUCRO* e' inerte. **Senza, una differenza
> misurata nella prova sarebbe attribuibile all'involucro invece che allo spegnimento.**
> **③ LA PROVA a 600 passi parte SOLO se il controllo passa.**
>
> **I COMANDI, verbatim:**
> ```
> python csv/_test_fork/_spegni_grav_bifase.py --controllo
> python csv/_test_fork/_spegni_grav_bifase.py --prova
> python csv/_test_fork/_letture_validazione.py --dir=csv/_test_fork/_g3_senza_bifase
> ```
> **Le letture sono gli STESSI OTTO CRITERI ASSOLUTI della validazione.** Nessun confronto fra
> epoche.

---

## DIFETTI APERTI — **ogni difetto ACCLARATO, con la sua prova**

> **REGOLA (Luca, 2026-09-22).** Un difetto e' **ACCLARATO** quando e' sostenuto, **e committato**,
> da **almeno una** fra: una **MISURA** · una **LETTURA DEL SORGENTE** con la riga citata e
> verificata sul blob corrente · una **VIOLAZIONE DIMOSTRATA di un assioma** con la riga.
> **Entra qui NELLO STESSO COMMIT in cui diventa acclarato**, con la riga
> `DIFETTO ACCLARATO: Dxx` nel messaggio. **Un SOSPETTO non e' un difetto:** va nella sezione
> sotto, e si **promuove** solo con la prova (`PROMOSSO: Sxx -> Dyy`).
> **ID stabili, mai riusati. Un difetto CURATO non si cancella: resta, col commit della cura.**
> **Stato, uno solo:** `APERTO` · `CURA DERIVATA` · `CURA IN CODICE` · `CURATO`
> · `NON E' UN DIFETTO`.
> **⚠ RICOSTRUITA DAI FILE, NON DA MEMORIA** *(commit, `RAMIFICAZIONI.md`, relazione)*.

| ID | il difetto, in una riga | la prova | cura | stato |
|---|---|---|---|---|
| **D38** | **`_nasce` (`:3850`) e' gated su `SCALA_MIN or SCALA_MIN_PASSO`: la legge «nessun arco sotto `LAM`» e' VERIFICATA sempre (`E4-LAM`) ma FATTA RISPETTARE ALLA NASCITA da un'OPZIONE** | `C1` (2026-09-24, `csv/_seal_fork/_prova_nasce_identita.py`, passo ZERO, un processo per braccio): **identita' di BYTE** `d_on == max(d_off, LAM)`, `0` elementi diversi su `525 973`; **`223 380` archi (`42.47 %`) nascono sotto `LAM`**, `min(d_off)/LAM = 0.012098`. **Coi default del SORGENTE la legge e' violata al passo zero.** | **`D-b` di Luca: CURA DELLA SEMINA** -- non deve NASCERE un arco sotto `LAM`; `_nasce` **resta come PRESIDIO** | **APERTO** |
| **D01** | **`S09` clippa al passo causale — quindi e' gia' una LUNGHEZZA — e poi moltiplica per `median(d0)`: statistica GLOBALE e lunghezza AL QUADRATO** | `G2` `fedda6c`: **`85.05 %`** degli archi-passo saturi, **`99.69 %`** del saldo da incrementi saturi · `Z81`, `Z106` · `A2`, `A5`, `A11` cor.6 | **`SPINTA_LOCALE`** | `APERTO` |
| **D02** | **`pozzo_grafo` calcola `L` da `self.pos` — IL DISEGNO — mentre il suo docstring dichiara «la distanza REALE»** | `G1` `3c03223`, `Z103`: mediana `L/d` `0.98`→`1.22`, **un arco su quattro oltre il doppio** al passo 600, e **dipendenza dal centro su 5 snapshot su 5** · `A1` · il pavimento `1e-9` su `L` e' `A11` cor.1 | **`POZZO_D`** | `APERTO` |
| **D03** | **La memoria del moto prende le direzioni da `pos`, normalizza su `Imed` GLOBALE, e ha un tetto `0.01*median(d0)`** | `Z104` `f80503c`, letto da `:5631-5648` · `A1` + `A2` + `A11` cor.2 e 7 · **`Z112` MISURA il tetto: SATURO nel `78 %`-`89 %` degli archi** *(`A11` cor.6)*, e la scheda dice perche' e' strutturale — **`proj` e' ADIMENSIONALE e si somma a una LUNGHEZZA: il clip non limita, fa da SCALA** | **`MEM_ARCO`** | `CURA DERIVATA` *(derivata, non scritta — **e deve rispondere alla domanda dimensionale PRIMA**)* |
| **D04** | **`_smp_chiudi()` RISCRIVE tutto `d0` a fine passo e NON ha nessun `_traccia_d0` attorno: e' una scrittura invisibile alla traccia** | lettura del sorgente `:3677`, commit `0989b78` · e' il buco che in `Z107` lasciava il bilancio aperto | **un sito di traccia** *(o il bilancio come presidio)* | `APERTO` *(nel runner di `G4` e' aggirato avvolgendo `_smorza`, ma il SIMULATORE resta senza sito)* |
| **D05** | **I residui di `C5`: `I4` scatola nera, `I5` underflow per riga, modalita' fine** | il mandato `C5` e la coda | — | `APERTO` |
| **D06** | **`_fatt_cs_ultimo` e' SCRITTO e MAI LETTO** *(quarto caso della stessa famiglia)* | `Z7`, letto dal codice | — | `APERTO` |
| **D07** | **`TAU_A` e' UN SOLO numero per DUE leggi fisiche distinte** | `Z10`, `Z9-bis` | — | `APERTO` |
| **D08** | **Il terzo ramo di `calcola_psi` (`elif` sotto `REPULS_LEGGE`) e' DICHIARATO, non corretto** | `Z14`, letto dal codice | — | `APERTO` |
| **D09** | **`chi_basc` BLOCCA la mitosi e DIMEZZA l'olonomia netta: fa l'OPPOSTO del suo scopo dichiarato** | `Z73`, **RITIRATA** | **nessuna: il difetto NON C'E'** | **`NON E' UN DIFETTO`** — *`Z73` ritirata una seconda volta, e la smentita e' nel MESSAGGIO di `48a3555`:* **da 2672 a 7323 nodi, 4651 nati in 1560 passi CON `chi_basc` acceso**. La misura di partenza era su **60 passi, un seme**: **era CORTA, non sbagliata**. |
| **D10** | **`nsub` governa il costo dell'intero sistema ed e' INVISIBILE: nessun contatore, nessuna colonna** | `Z75` | — | `APERTO` |
| **D11** | **`d` scende DIECI VOLTE sotto `LAM` mentre `SCALA_MIN` e' acceso, e la causa NON e' trovata** | `Z87` | **la cura di `Z87`: il mondo si costruisce SEMPRE dopo i flag** *(`01eda44`, categoria D)* | **`CURATO`** — *decisione della revisione storica, 2026-09-26:* **la causa ERA che i flag non agivano sul vuoto**; curata in `01eda44`, e in scena `(ii)` con i flag del driver gli archi sotto `LAM` sono **ZERO**, con `min(d)/LAM = 1.000000` esatto *(`Z148`)*. |
| **D12** | **`1755 MB` di `.pkl` non hanno il comando che li rigenera** *(par.5-quinquies: «un dato che nessuno potra' rifare»)* | `Z89` | — | `APERTO` |
| **D13** | **I sigilli storici non sono stati rigirati sul blob corrente** | `Z11` | — | `APERTO` |
| **D14** | **`median(\|f\|)` fa TRE mestieri, non due: e' anche il rompi-anello** | `Z41` | — | `APERTO` |
| **D15** | **`A7`: la carica chirale NON si conserva** | `Z71`, letto dal codice | — | `APERTO` |
| **D16** | **`SCALA_MIN` frenava OGNI scrittura separatamente: il risultato dipendeva dall'ORDINE delle leggi** | `Z91` | `SCALA_MIN_PASSO` *(`C3`)* | **`CURATO`** |
| **D17** | **`peq` diventava NEGATIVO e il pavimento `max(peq, 1e-9)` NE RIBALTAVA IL SEGNO** *(da `-3.72` a `+1.8e+06`)* | `Z94` | `PEQ_ESATTO` + `ANOM_SIMM` *(`C1`, `C1-bis`)* | **`CURATO`** |
| **D18** | **`COES_ADIM` leggeva ISTANTI MISTI e il suo tetto era GLOBALE** | `Z92` · `A5` | `COES_CAUSALE` *(`C4`)* | **`CURATO`** |
| **D19** | **OTTO grandezze che la semina legge erano INERTI SUL VUOTO in ogni run di epoca 1** | `Z88` | la cura del mondo-dopo-i-flag | **`CURATO`** |
| **REG-A** | **FASE A del registro della fisica: l'INVENTARIO degli scrittori di stato** | MANDATO-REGISTRO §2 | ✅ **FATTA** *(`1214283`, blob `2c70e4ad`)*: **`164` scritture fisiche su `27` grandezze, di cui `65` CONCATENAZIONI**, piu' `313` scritture su attributi **non dichiarati fisici**, elencati e non nascosti |
| **REG-B** | **FASE B: le SCHEDE**, a lotti, **un commit per lotto** | MANDATO-REGISTRO §2 | ✅ **LE QUATTRO DELL'ORDINE DI LUCA SONO SCRITTE.** ① freno di `SCALA_MIN` *(`DIFETTOSA`, i TRE CANDIDATI come domande)* · ② memoria del moto *(`DIFETTOSA`, **`proj` adimensionale sommato a una lunghezza**)* · ③ gravita' bifase *(`DIFETTOSA`, **`spinta` clippata a `[L]` e poi moltiplicata per `median(d0)`: `[L²]`**)* · ④ coesione *(`DA VERIFICARE`, **l'unica con le unita' giuste senza che un clip gliele dia**)*. ⏸ **RESTANO:** mitosi, Schwinger, rilassamento di `peq`, poi le altre attive, poi le dormienti — e **i 164 scrittori dell'inventario** |
| **REG-C** | **FASE C: LA STORIA** di ogni legge, e le schede delle leggi TOLTE | MANDATO-REGISTRO §2 | ⏸ cio' che non si ricostruisce si scrive **NON RICOSTRUITO** |
| **REG-R** | **LA REGOLA MANTENUTA del registro della fisica** — la riga in `CLAUDE.md` *(«nessuna legge fisica entra, cambia o esce dal simulatore senza passare da `doc/REGISTRO_FISICA.md`»)* **e l'hook che RIFIUTA un commit che tocca `soliton_simulator.py` senza toccare il registro**, salvo `[SENZA-FISICA: motivo]` | MANDATO-REGISTRO §4 | ⏸ **NON FATTA, e me ne accorgo facendo il punto.** **Non poteva essere fatta prima:** l'hook rifiuterebbe ogni commit al simulatore, e `doc/REGISTRO_FISICA.md` **non esiste ancora** — va con la **fase B** |
| **REG-V** | **`_verifica_registro.py`**: completezza, esistenza, coerenza con la traccia di `d0` e col registro dei domini di `C5` | MANDATO-REGISTRO §3 | ⏸ col collaudo `P1-sexies`, **compreso un registro volutamente sbagliato che DEVE fallire** |
> **⚠ SULL'ETICHETTA «EPOCA 3», e va detta prima di usarla ancora.**
> **IL TAG `epoca-3` NON ESISTE.** E' un lavoro ancora in coda *(voce `E3`)*, e finche' non c'e'
> **«archivi di epoca 3» non identifica niente**: e' un'etichetta che ho usato come se
> fosse un fatto.
> **CIO' CHE INTENDEVO, e che d'ora in poi si scrive per esteso:** gli **archivi delle cure** — `_val600` e `_g3_senza_bifase` *(simulatore blob `9557a867`)*, `_g4_controllo` e `_g4_riferimento` *(blob `ab685eac`)*.
> **Sono DUE blob diversi**, e il secondo e' byte-inerte rispetto al primo a `MEM_MOTO` acceso
> *(sigillo `T7`, `206` campi identici)* — **ed e' per questo che i numeri dei due si
> confrontano.** Senza quel sigillo, sarebbero due sistemi.

> **⚠⚠ IL VINCOLO CHE GOVERNA IL CHECKPOINT (Luca, 2026-09-22), e viene prima di ogni
> cura:**
> **LE CURE DEL `CHK3` NON PARTONO FINCHE' LE SCHEDE DELLE COMPONENTI DA CURARE NON ESISTONO.**
> **Il registro serve esattamente a questo: una cura deve NASCERE DALLA SCHEDA** — dalla
> formula, dalle dimensioni, da cosa legge e cosa scrive, dai limiti classificati con `A11`.
> **Se la scheda non c'e', si cura di nuovo alla cieca**, ed e' il modo in cui sono nati
> `D01`-`D31`.
> **Conseguenza operativa:** `SPINTA_LOCALE`, `POZZO_D`, `MEM_ARCO` e **il freno simmetrico di
> `D31`** **non si scrivono in codice** finche' le loro schede non stanno in
> `doc/REGISTRO_FISICA.md`.

<!-- CURE-INIZIO -->

## ✅ CURE VERIFICATE — **flag · sigillo · prova · esito · stato**

> **Decisione di Luca, 2026-09-22.** Si aggiorna **nello stesso commit** in cui una cura viene sigillata o provata.
> **Generata da `csv/_cure_verificate.py`:** il **DEFAULT** si legge dal sorgente a ogni giro e l'esito del sigillo dal suo referto; **prova, esito e stato sono LETTURE**, scritte a mano.
>
> **⚠ IL FATTO CHE LA TABELLA RENDE VISIBILE:** **quasi tutte le cure hanno default `False`** e **le accende il DRIVER, run per run**. Non sono «nel codice»: sono **nell'argv**. **Un run che dimentica un flag gira su un sistema che si sa difettoso** *(`P2`)*, e nessuno se ne accorgerebbe dal sorgente.

| flag | cura | **default** | sigillo | prova | esito | stato |
|---|---|:--:|--:|---|---|---|
| `PEQ_ESATTO` | `C1` rilassamento di `peq` in forma ESATTA | **`False`** | `7/7` *(letto dal referto)* | in **ogni** run del fork *(`--peq-esatto=on`)* | `peq` non puo' piu' scavalcare sotto zero: combinazione convessa, **dimostrato** e non imposto. Cura `D17` | VERIFICATA-SPENTA *(default `False`, accesa dal driver)* |
| `PEQ_NASCITA_LOCALE` | `C2` nascita LOCALE di `peq` | **`False`** | `6/6` *(letto dal referto)* | in **ogni** run del fork | una sola legge di nascita; via la mediana GLOBALE *(`A2`)* | VERIFICATA-SPENTA *(default `False`, accesa dal driver)* |
| `SCALA_MIN_PASSO` | `C3` il freno UNA VOLTA per passo | **`False`** | `6/6` *(letto dal referto)* | `G4` riferimento e i due spegnimenti, 600 passi | cura il cricchetto **d'ORDINE** di `Z91`. **⚠ MA NON IL CRICCHETTO DI VERSO:** `Z113` lo DIMOSTRA sulla formula, ed e' **`D31`** | VERIFICATA-SPENTA — **e la legge che applica e' DIFETTOSA** |
| `COES_CAUSALE` | `C4` coesione: istante unico e cono LOCALE | **`False`** | `5/5` *(letto dal referto)* | in **ogni** run del fork | cura `D18`. Il tetto locale **non e' sempre piu' stretto**: dove il cono e' veloce **allarga** | VERIFICATA-SPENTA *(default `False`, accesa dal driver)* |
| `COES_ADIM` | coesione ADIMENSIONALE | **`False`** | — *(non ha un sigillo suo)* | in **ogni** run del fork | `|F_adim| <= 1` **per costruzione**. **L'unica legge delle quattro schede con le unita' giuste senza che un clip gliele dia** | VERIFICATA-SPENTA |
| `ANOM_SIMM` | `C1-bis` anomalia simmetrica, senza pavimento | **`False`** | `6/6` *(letto dal referto)* | in **ogni** run del fork | toglie `max(peq, 1e-9)`, che con `peq < 0` **RIBALTAVA IL SEGNO** *(`Z94`, `D17`)* | VERIFICATA-SPENTA |
| `INVARIANTI` | `C5` domini di stato, due livelli | **`True`** | `3/3` *(letto dal referto)* | in **ogni** run: **zero violazioni** in tutti e tre i bracci di `G4` | legge soltanto; su un run sano non cambia un bit | **ACCESA DI DEFAULT** *(`True`)* |
| `RITMO_WRAP_2PI` | **`A1`** il wrap del ritmo sul periodo GIUSTO *(`2π`)* | **`False`** | `4/4` + **`6/6` di `CURA 1`** *(`csv/_seal_fork/_sig_cura1/REFERTO.txt`)* | ✅ **`G4`, 600 passi** *(`Z123`)* + **giro corto di `CURA 1`** | cura **`D34`** *(`Z117`: il wrap a `4π` e' l'IDENTITA')*. **`6/8` come previsto e il bilancio CHIUDE (`9.595e-14`), ma TUTTI gli aggregati peggiorano e la mia previsione ⑤ era SBAGLIATA** *(la quota al tetto SALE: -> `S09`)* | ✅✅ **APPROVATA DA LUCA il 2026-09-24. IL DRIVER LA ACCENDE IN OGNI RUN** *(`--ritmo-wrap-2pi`)*. Default nel sorgente **`False`**, come tutte le cure pre-epoca-3. **`D34` passa da difetto aperto a CURA IN CODICE.** |
| `CHI_COOP` | **COOPERAZIONE**: la GEOMETRIA in `perc_geom`, la CARICA in `perc_chi` | **`False`** | ⚠ *(vedi stato)* | ✅ **in OGNI run da `G3` in poi** -- e' **una delle TRE leggi che DEFINISCONO l'EPOCA 2** (`CLAUDE.md` par.9-bis) | `chi_basc` NON si spegne per accendere lo spinore: i due fanno lavori DIVERSI e devono COOPERARE. Spegnere `chi_basc` toglierebbe la GEOMETRIA insieme alla CARICA, e **un confronto con due variabili cambiate insieme non si legge** | ⚠⚠ **ERA FUORI DA QUESTA TABELLA FINO AL 2026-09-24**, e per questo il sigillo del driver **non poteva vederla**: era passata `=on` da ogni comando di campagna mentre il default del driver diceva `"off"`. **ORFANO FUORI DALLA LISTA** -- il caso che il controllo delle orfane doveva impedire *(rilievo di Luca)*. **⚠⚠ E IL SUO SIGILLO NON E' PIU' RIGIRABILE, e NON per l'argv:** confronta il simulatore di OGGI con uno **VECCHIO** (`b46835bd`) che le opzioni delle cure **non le ha**. Senza le cure il braccio nuovo **si schianta** su `d >= LAM` (**`Z148`**); con le cure il braccio vecchio **non parte**; darle a uno solo farebbe differire i bracci **per le cure** invece che per `CHI_COOP`. **DICHIARATO NON RIGIRABILE invece che truccato: e' un `Z31` NUOVO.** Ora **ACCESA DAL DRIVER** *(`--chi-coop`)* |
| `TEMPO_UNICO_MITOSI` | **`CURA 2`** UN SOLO OROLOGIO dentro `mitosi()` | **`False`** | `5/5` *(letto dal referto)* | ✅ **giro corto di 120 passi contro `_cura1_corto`** *(un interruttore di differenza, due processi freschi a un solo braccio)* | gli usi di `tau_pp` come TEMPO passano all'orologio `dt_e`; i **quattro** usi come POSIZIONE sull'asse della torsione restano INTOCCATI *(dall'AST, `T3`)*. **La mitosi vive** *(eventi `67` -> `76`)*, **il bilancio chiude** *(`5.304e-14`)*, e **la saturazione di `tanh(grad)` passa da `0.0034 %` a ZERO** *(`A11` cor.6; il massimo misurato `0.8861` contro il `0.8884` PREVISTO dall'intervallo di `r`)*. **⚠ MA due delle tre sostituzioni formali sono INERTI in questo regime:** il clip alto su `prob` non morde **mai** *(0 su 63 128 409)* e l'Eulero non ha **mai** `dt/τ > 1`. **⚠ E la previsione di `×2.5`-`×3` su `d0` NON regge: `±3 %`** | ✅✅ **APPROVATA DA LUCA il 2026-09-24. IL DRIVER LA ACCENDE IN OGNI RUN** *(`--tempo-unico-mitosi`)*. Default nel sorgente **`False`**, come tutte le cure pre-epoca-3. |
| `FASE_2PI` | **§D** `φ` come fase ordinaria su `[0, 2π)` | **`False`** | `6/6` *(letto dal referto)* | ❌ **PROVATA sul giro CORTO (120 passi, `Z127`): `2/4`, `E1` NON PASSA** | **LA LETTURA CADE.** La cura fa cio' che dichiara su `phi` *(`E4` PASSA, bilancio `4.041e-14`)*, **ma la generazione di materia SI FERMA**: mitosi `62` -> `1` evento, Schwinger `28` -> `0`. **`|tw|` si dimezza e nessun arco raggiunge piu' la soglia** *(`MAX 4.37 = 1.39 pi` contro `2pi`)*. **-> `D36`** | ❌ **IN CODICE e SIGILLATA, ma la PROVA la BOCCIA.** Default **SPENTO**, e ci resta: il punto 2 del par.D va riaperto *(decisione di Luca)* |

**Cure con default ACCESO: 1 su 11.**

### ⛔ E QUESTO NON E' UNA CURA: e' un **PRESIDIO STRUTTURALE**

> Non corregge un difetto MISURATO, perche' la legge **non ha mai girato** e quindi non ha prodotto nulla da curare. **Impedisce** che venga accesa. Metterlo fra le cure gonfierebbe il conto.

| flag | che cosa impedisce | **default** | come | sigillo |
|---|---|:--:|---|--:|
| `TW_SPINORE` | **il PONTE INVERSO**: `tw` (la cui scala viene da `phi`) scrive lo SPINORE — `tw` -> `omega_s` -> `_psi_spinor` (`:3090-3100`). Le **uniche due** `INVERSA` su 139 punti della mappa del `4pi` | **`False`** | il simulatore **RIFIUTA DI PARTIRE** in `_applica_flag`, col messaggio che nomina la ragione. **Il ramo resta** (par.10) | **`6/6`** *(`CURA 1`)* |

### ⚠ E QUESTE NON SONO CURE: sono **PROVE DI SPEGNIMENTO**

> Il flag e' **`True`** — la legge **gira** — e **spegnerlo e' il test**. Metterle fra le cure gonfierebbe il conto.

| flag | legge | **default** | sigillo | prova | esito |
|---|---|:--:|--:|---|---|
| `GRAV_BIFASE` | la gravita' bifase | **`True`** | `7/7` | `G3`, 600 passi | **NON e' il motore di `d0`** *(`Z107`)* |
| `MEM_MOTO` | la scrittura della memoria del moto su `d0` | **`True`** | `8/8` | `G4`, 600 passi | **non e' il motore**, ma pesa *(`Z109`)* |
| `MEM_MOTO_TUTTO` | l'INTERO blocco della memoria del moto | **`True`** | `10/10` | `G4-bis`, 600 passi | **spegnere di piu' da' PIU' crescita** *(`Z115`, `Z116`)* |

<!-- CURE-FINE -->

<!-- DIFETTI-NUOVI-INIZIO -->
| **D20** | La correzione (1) su `inerzia` NON e' stata cablata, e **il gate che la autorizzava aveva misurato UN'ALTRA GRANDEZZA** | `Z1` | — | `APERTO` |
| **D21** | `_floor_d0` e' SOSPESA, e **i due rami violano assiomi DIVERSI**: la scelta non e' stata fatta | `Z4` | — | `APERTO` |
| **D22** | Il DENOMINATORE PER GRADO: la misura non distingue (A) da (B), ma **(B) cade per DIMOSTRAZIONE**, e lo stesso schema e' in **almeno quattro punti** | `Z24` | — | `CURATO` |
| **D23** | **La cucitura dello snapshot FALLISCE su entrambi i fronti**, e si DIMOSTRA perche'. **NON CABLATA** | `Z37` | — | `APERTO` |
| **D24** | **`A2` e' VIOLATO da `Lam = mean(I)`** -- una media GLOBALE dentro una legge locale -- **e la violazione e' la ragione per cui il pezzo funziona** | `Z40` | — | `APERTO` |
| **D25** | **Il gauge del tempo e' la costante `1e-9`**, e il `93 %` dei nodi non invecchia | `Z46` — **MISURATO IN EPOCA 1**, blob **`a1ae5090`**, run continuo a **1200 passi** | — | ✅ **RIMISURATO col riferimento ESTERNO `r = 1`** *(`3828281`, documento `csv/_test_fork/_diag_D/COMPONENTI_E_TEMPO.md`)*: **IL `93 %` NON REGGE QUI.** I nodi con `r < 0.1` sono lo **`0.30 %`** *(`_val600`, `_g4_riferimento`)*, il **`4.98 %`** *(`_g4_senza_memmoto`)* e il **`18.69 %`** *(`_g3_senza_bifase`)*; la **quota di TEMPO** nei fermi sta fra lo **`0.01 %`** e l'**`1.83 %`**. **Come `D27`, la premessa cade sugli archivi attuali e la voce NON si cancella** *(`par.9-bis`: l'epoca ritira le MISURE, non i difetti)*. **Resta aperta la domanda con il numero nuovo:** una quota di tempo cosi' piccola basta a falsare la PROVA 3, o e' trascurabile? |
| **D26** | Le coorti **non sopravvivevano allo SNAPSHOT**: dopo un salva/ricarica il lignaggio ripartiva VUOTO | `Z53`, sigillo `9/9` | la cura di `Z53` | **`CURA INEFFICACE PER LA SCENA N-MASSE`** — **la cura preserva una registrazione che qui NON AVVIENE MAI**: `_massa` chiama `semina` **senza `mass_id`** *(`:6209`)*, quindi `masse_info` resta VUOTO e `conc_nodi` tutto liste vuote. **→ `D30`.** La cura in se' **resta valida**: e' il percorso di questa scena a non arrivarci |
| **D27** | **Il grafo e' in QUATTRO COMPONENTI che non si toccano mai** | `Z65`, **misurato in ORIGINE su un ALTRO sistema**: blob **`775ceab7`**, i **45 snapshot di `_g6000`** *(quello che il registro etichetta `EPOCA 1`)* | — | **`NON E' UN DIFETTO NEL SISTEMA ATTUALE`** — **LA PROVA: UNA SOLA componente**, su gli **archivi delle cure** — `_val600` e `_g3_senza_bifase` *(simulatore blob `9557a867`)*, `_g4_controllo` e `_g4_riferimento` *(blob `ab685eac`)*, **12 snapshot su 12** *(`944064a`, strumento blob `6520c98c`)*. **La voce NON si cancella:** resta col numero d'origine e col fatto che **l'ho importata da un altro sistema senza riverificarla** (`par.9-bis`) |
| **D28** | **`nsub` esplode e lo tira `max(|vd|)` su POCHISSIMI archi**: il costo dell'intero sistema e' governato da una manciata di archi | `Z74` | — | `APERTO` |
| **D29** | **CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema**: il vuoto ha degli HUB, e non dovrebbe averne | `Z77` | — | `APERTO` |
| **D30** | **`_massa` chiama `semina` SENZA `mass_id` (`:6209`), quindi `masse_info` non viene MAI popolato e `_registra_concorrenza` non parte: negli snapshot di epoca 3 `masse_info` e' VUOTO e `conc_nodi` e' tutto liste vuote** | lettura del sorgente `:6209` + misurato su `_val600/scena_000120` | — | `APERTO` |
| **D31** | **Il freno di `SCALA_MIN` (`_smp_chiudi`) E' IL MOTORE della crescita di `d0`: vale il `117.41 %` del `Δ`, mentre gli scrittori fisici tirano GIU' per il `-17.43 %`** | `Z108`: bilancio che **CHIUDE** a `1.138e-13` su **600 passi**, blob `ab685eac` · **promosso da `S02`** · **`Z113` lo DIMOSTRA SULLA FORMULA**, `4/4`: deriva `+1.582064e-03` contro l'attesa derivata `+1.582007e-03`, **scarto `0.0 %`**, e i due casi che devono dare zero lo danno · **`Z113` misura anche DOVE morde:** al passo 600 il `13.74 %` degli archi e' incollato a `[1.0,1.1)·LAM` *(annullamento `99.96 %`)* e porta il `35.80 %` del freno · **❗ `Z148` (2026-09-24): LA LEGGE `d >= LAM` REGGE PERCHE' QUESTA CURA E' ACCESA.** Due bracci, stessa scena/seme/blob `49fc54d2`, UN passo: **SENZA le cure `223 396` archi su `526 047` sotto `LAM` -- il `42.47 %` -- e `min(d)/LAM = 0.0625`; CON le cure **ZERO**, e **`min(d)/LAM = 1.000000` ESATTO**. **Il `1.000000` e' esso stesso il reperto: gli archi non stanno SOPRA il muro, STANNO SUL MURO** (`A11` cor.6). `csv/_seal_fork/_reperto_lam_senza_freno.py` | **il freno simmetrico** *(`A11` cor.4)*, **da derivare al `CHK3`** · la **scheda ①** del registro e' scritta | `APERTO`  **✅✅ DECISIONE DI LUCA, 2026-09-24 — E RIBALTA IL MODO DI LEGGERE `D31`:** *«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema»* è una **LEGGE**, e **deve diventare STRUTTURALE**: sempre accesa, **candidata all'epoca 3**. **LA LEGGE E' GIUSTA. L'IMPLEMENTAZIONE NO.** **La realizzazione di quella legge OGGI e' il FRENO A SENSO UNICO, cioe' esattamente `D31`:** si frena la discesa e non la salita, e da li' viene il cricchetto *(dimostrato sulla formula, `Z113`, deriva `+1.582064e-03` contro l'attesa derivata `+1.582007e-03`, scarto `0.0 %`)*. **QUINDI `D31` NON SI CURA TOGLIENDO IL PAVIMENTO:** il pavimento e' la legge. **Si cura cambiando COME lo si realizza**, e la forma giusta non e' un freno asimmetrico. **⚠ E OGGI LA LEGGE NON E' NEMMENO VERIFICATA SEMPRE:** l'invariante `d >= LAM` di `C5` e' **gated** su `SCALA_MIN or SCALA_MIN_PASSO` (`:3657`, `:3702`); a flag spenti degrada a `d > 0`. **Una legge verificata solo quando un flag e' acceso non e' una legge: e' un'opzione.** → voce `E4-LAM`.  **✅ LA REALIZZAZIONE PROPOSTA E' SCRITTA — scheda ⑪ `freno-legge`, 2026-09-24, NESSUN CODICE.** La forma: **`(d − LAM) ← (d − LAM)·exp(dx/d)`**, cioè **la stessa mobilita' `(d−LAM)/d` di oggi, applicata in ENTRAMBI i versi** invece che nella sola discesa. **Al primo ordine e' esattamente il freno di oggi**; cambia **il verso in cui si applica**, non la legge. **LA DERIVA:** oggi `(a/2)·(LAM/d)`, **primo ordine e MASSIMA AL CONFINE** *(`→ a/2` per `d → LAM`)*; con la proposta `u·(cosh(a/d) − 1) ≈ u·a²/(2d²)`, **SECONDO ordine, NULLA al confine** *(perche' `u → 0`)* **e decrescente lontano**. **IL RAPPORTO da' una CONDIZIONE:** `nuova/oggi = a·(d−LAM)/(d·LAM)`, quindi la proposta e' migliore **ovunque** se e solo se **`a < LAM`** — e **`a` NON E' MISURATO**: e' il punto `V1` della verifica. **⚠ E NON ELIMINA LA DERIVA:** `cosh(x) >= 1` sempre, quindi `E[Δu] >= 0` **sempre**. **Cambia l'ORDINE, non il segno**, e dire «il cricchetto sparisce» sarebbe falso. **CODICE SOLO DOPO LA PROVA DI `CURA 2`** *(decisione di Luca)*. **E resta SEPARATA la domanda di chi spinge gli archi contro il muro: `D33`, `S05`.**  **❓ E UNA SECONDA FORMA, proposta dal guardiano il 2026-09-24 — LA CORREZIONE DI ITO:** `(d−LAM) ← (d−LAM)·exp(dx/d − (dx/d)²/2)`. **Verificata numericamente** *(`csv/_test_fork/_z147_ito.txt`)*: la deriva **scende dal 2° al 4° ordine** *(raddoppiando `s`: piana `×4.004`, Itô `×15.950`)* **e CAMBIA SEGNO, diventando negativa** — verso il muro invece che lontano. **Ed e' anche piu' FEDELE** alla legge `u(1+x)`: i termini in `x²` si cancellano esattamente *(a `x=0.3`: eccesso `−9.54e-03` contro `+4.99e-02`)*. **❌ MA NON E' MONOTONA:** massimo in `x = 1` *(`√e = 1.6487`)*, e **per `x > 2` UNA SALITA FA SCENDERE** *(a `x = 2.5` il fattore vale `0.535`)*; su `[0,3]` ha `2000` incrementi negativi su `3000`, la piana **zero**. **E' la firma di `A11`: una spinta piu' grande con un effetto piu' piccolo.** **LA SCELTA FRA LE DUE E' DI LUCA, e il criterio e' MISURABILE:** la **distribuzione di `|dx|/d`** — se `max ≪ 1` la non-monotonia non si manifesta mai e Itô e' migliore su tutto; se arriva a `1` il tetto morde, a `2` inverte. → punti `V8`/`V9`.  **✅ E UNA TERZA FORMA, proposta da Luca il 2026-09-24, CHE DOMINA LA SECONDA:** `(d−LAM) ← (d−LAM)·(1 + tanh(dx/d))`. **Verificata collo stesso strumento:** deriva **ZERO ESATTO** per rumore simmetrico *(`0.000000000000000e+00` a ogni `s` provato: `(1+tanh x)+(1+tanh(−x)) = 2` per disparita', non e' un'approssimazione)* · **MONOTONA** *(`0` incrementi negativi su `6000`, contro i `2000` su `3000` di Ito)* · **mai sotto `LAM`** *(`1+tanh ∈ (0,2)`)* · **fedelta' `O(x³)`, anzi un po' MIGLIORE di Ito** *(a `x=0.3`: `−8.687e-03` contro `−9.538e-03`)*. **LIMITE: una salita al piu' RADDOPPIA `(d−LAM)`** — una **saturazione**, `A11` cor.6, **ma MENO restrittiva del tetto `√e` di Ito e senza la non-monotonia.** **❗ QUINDI ITO ESCE DAL CONFRONTO: non c'e' nessun asse su cui sia preferibile.** **LA SCELTA VERA E' FRA `piana` E `tanh`:** la piana **non ha tetto ma HA deriva**, `tanh` **non ha deriva ma SATURA a 2**. **La decide la DISTRIBUZIONE di `|dx|/d` (`V8`/`V9`), e la decide Luca DOPO quella misura.** |
| **D32** | **I TEMPI PROPRI DICHIARATI SONO TRE, E SONO TRE GRANDEZZE DIVERSE: `r`, `tau_pp` e `d/cs`.** `corr(r, tau_pp)` fra `-0.25` e `+0.26`, **segno non concorde**; `corr(r, d/cs)` **positiva ovunque** ma in calo; `d/cs` **cresce monotono** mentre `tau_pp` e' inchiodato | `Z110`: 20 snapshot, 4 archivi delle cure, strumento blob `20bd4b3e` · **dal sorgente:** `TEMPO_SEGNO = False`, quindi `ritmo()` e' de Broglie normalizzato *(`:2553` non gira)* e `tau_pp` e' torsione *(`:5160`)* · `A10` | **dire QUALE delle due e' il tempo proprio**, nella scheda del registro | `APERTO` |
| **D33** | **La repulsione alla massima compressione e' AZZERATA proprio dove serve: dal `75 %` al `96 %` degli archi oltre l'inversione riceve `resp` ESATTAMENTE ZERO** | `Z111`: `discesa = clip(1-|tw|/4pi,0,1)` e' zero per `|tw| >= 4pi` *(`:5153`)* mentre il segno si inverte a `~3.5pi`: **finestra larga mezzo `pi`** · contraddice il commento della legge *(`:5153-5156`)* | **da decidere al `CHK3`** *(uno dei tre candidati del freno)* | `APERTO` |
| **D34** ✅`CURATO IN CODICE il 2026-09-24` | **Il wrap «a 4π» di `ritmo()` (`:2584-2585`) NON AVVOLGE: su `(-2π, 2π)` e' l'IDENTITA'. Ogni attraversamento del taglio a `±π` registra una frequenza spuria di `~2π/DT`** | `Z117`: dimostrazione algebrica *(`max|w4(a) - a| = 0` su `100 001` punti)* + misura a 120 passi · **attivo nel fork** *(`--campo-spinoriale`)* · rilievo di Luca | **`RITMO_WRAP_2PI`** — flag, sigillo, prova a 600 passi. **Eccezione dichiarata alla regola «nessuna cura prima del `CHK3`»** | ✅**`CURATO IN CODICE`** — e il marchio nell'ID non bastava: **questa colonna diceva ancora `APERTO`**, ed è stato Luca a prenderlo. Una correzione che aggiorna l'ID e lascia lo `stato` è una correzione **a metà**. | **LA CURA E' IN CODICE E IL DRIVER LA ACCENDE IN OGNI RUN** *(`--ritmo-wrap-2pi`, `Z134`, sigillo `6/6`)*. **Approvata da Luca.** Il default nel sorgente resta `False`, come tutte le cure pre-epoca-3: il braccio di confronto si ottiene **omettendo il flag**, e `CONFIGURAZIONE.txt` mostra quale dei due e' girato.
| **D35** | **L'antiparticella di Schwinger nasce con `+2π` (`:5443`) e nel campo `F = Σ exp(iφ)` E' IDENTICA alla particella, non opposta. Il commento dice `+π`** | `Z119`: letto dal sorgente · **il ramo E' ATTIVO**, `COPPIA_MIT = 1.0`, e `S07_schwinger` scatta `90`-`172` volte su 600 passi nei tre bracci di `G4` · rilievo di Luca | **DIPENDE DA §`B1`** *(che cosa e' `φ`)*: **non si corregge prima della decisione di Luca** | `APERTO` |
| **D36** | **LA SOGLIA DELLA MITOSI E' IN UNITA' ASSOLUTE DI `tw`, MENTRE LA SCALA DI `tw` DIPENDE DAL DOMINIO DI `phi`: le due NON SI POSSONO CAMBIARE UNA PER VOLTA** (`:5152-5156`, `soglia0 = PHI_CRIT + twist_max` oppure `PHI_CRIT`) | **ACCLARATO PER MISURA, `Z127`** *(2026-09-24, blob `445e2896`, 120 passi, seme 42)*: portando `phi` su `2pi` **`|tw|` si dimezza** *(`p99` `6.391` → `3.147`; `MAX` `34.35` → `4.37 = 1.39 pi`)* mentre la soglia scende solo di un terzo *(`3pi` → `2pi`)*: **gli archi sopra soglia passano da `7047` a `0`** e la generazione di materia si **ferma** *(mitosi `62` → `1` evento; Schwinger `28` → `0`)*. | **PERCHE' E' UN DIFETTO E NON UN ACCOPPIAMENTO LEGITTIMO:** una soglia in unita' **assolute** di una grandezza la cui scala e' fissata da una **convenzione** *(il dominio di avvolgimento)* **non e' una legge fisica: e' una manopola travestita**. La stessa famiglia di `A2`/`A3`. **E la crepa era GIA' DICHIARATA da Luca** — *l'argomento vale per una differenza ISTANTANEA, `tw` e' un ACCUMULO* — **e `E1` l'ha giudicata.** | **LA CURA CANDIDATA E' DERIVABILE, e NON la applico:** esprimere la soglia come **frazione del dominio** invece che in valore assoluto — se un arco porta una differenza fino a `_dphi()/2` e il quanto e' il dominio intero, la soglia e' `_dphi()/2` *(cioe' `pi` su `2pi`, `2pi` su `4pi`)*. **MA QUESTO CAMBIA IL PUNTO 2 DEL par.D, CHE E' UNA DECISIONE DI LUCA**, e la sua regola e' esplicita: *«se un test fallisce, la decisione cade E SI SCRIVE»*. **Scritta, non applicata.** **E va misurato PRIMA se `tw` si dimezzi DAVVERO per costruzione o per caso:** il censimento aveva lasciato `_w4`/`_w8` sulla torsione ACCUMULATA **fuori** dalla cura, di proposito *(era `SCALE-TW`)* — **quindi oggi l'INGRESSO di `tw` vive su `2pi` e il suo AVVOLGIMENTO su `4pi`: due scale diverse nella stessa grandezza.** **⚠ CORREZIONE del 2026-09-24, rilievo di Luca, verificata dal sorgente: l'avvolgimento NON C'ENTRA.** Con `TORS_4PI` acceso la torsione si avvolge con **`_w8` (`:4698`)**, la cui finestra e' **`8π`** *(`_w8(a) = (a + 4π) % 8π - 4π`)*: **su incrementi piccoli e' l'IDENTITA' e non fa nulla.** **A dimezzare `tw` e' l'INGRESSO:** `dph = self._wphi(...)` (`:4675`) e `twp = self._w8(dph + twist_dip)`, e con `FASE_2PI` acceso `dph` sta in **`(-π, π]`** *(e `|twist_dip| <= π` per costruzione, quindi la somma sta in `(-2π, 2π]` e `_w8` la lascia intatta)*. **CONSEGUENZA: `SCALE-TW` NON e' prerequisito di `D36`** — torna **in coda al suo posto** *(`A12`)*. **Cio' che resta vero e' il difetto: la soglia e' in unita' assolute di `tw`, e `tw` prende la sua scala da `phi`.** |
| **D37** ✅`CURATO il 2026-09-24` | **CHIAVE DUPLICATA NEI `DOMINI`: `'_cs_nodo_prev'` compare DUE VOLTE** (`:226` e `:257`) | **ACCLARATO, e l'ha mostrato il sigillo stesso:** `T2` di `_sigillo_e4lam.py` stampa la descrizione della voce attiva, e **non e' quella che avevo scritto io** — e' `'velocita delle onde metriche: una VELOCITA e positiva'` (`:257`) invece di `'la velocita d onda di nodo...'` (`:226`). **In un letterale di dict la chiave duplicata vince l'ULTIMA**, quindi la mia è **codice morto**. | **È UN DIFETTO MIO, DI OGGI, e la causa è `P1`:** avevo cercato la voce con `sed -n '213,240p' | grep cs` e **la voce sta a `:257`, FUORI da quella finestra**. **Ho concluso un'ASSENZA da una ricerca PARZIALE**, e ho aggiunto una cosa che c'era già. **Una finestra di 28 righe non è «il disco».** | **CURA: si toglie la MIA voce (`:226`) e si tiene quella preesistente (`:257`).** **È inerte** — `T5` dà `206` campi identici e `0` diversi comunque — **ma una chiave duplicata è un difetto: silenzioso, e nasconde quale delle due descrizioni valga.** **E la derivazione resta valida: `cs > 0` era GIÀ un invariante, fatto da qualcun altro prima di me.** → `Z142`  **✅ CURATO nello stesso giorno in cui è nato:** la mia voce (`:226`) è **via**, e **la derivazione di `cs > 0` è stata SPOSTATA sulla voce preesistente** invece di essere buttata. **`DOMINI` ha `42` chiavi e `0` duplicate, verificato DALL'AST** *(`T1b` del sigillo `E4-LAM`)*. **E ora c'è un TEST PERMANENTE:** `T1b` rifiuta qualunque chiave duplicata, col suo collaudo `K7`/`K8`. |
<!-- DIFETTI-NUOVI-FINE -->


<!-- TRIAGE-INIZIO -->

### ESITO DI OGNI VOCE `CODICE` DI `RAMIFICAZIONI.md` — **tabella GENERATA**

> **GENERATA DA CODICE** (`P1-ter`) da `csv/_seal_fork/_triage_difetti.py`. **Nessuna voce resta senza esito**, e non e' una promessa: se una sola ne fosse priva, **lo script fallisce e non scrive niente**.
>
> **⚠ L'ELENCO NON E' RIPRODUCIBILE DA UN FILTRO MECCANICO, e va detto:** sul file di oggi il **tag** `[... · CODICE]` marca **11** voci, la parola `CODICE` in maiuscolo **20**, `codice` senza distinzione di maiuscole **49**. **Nessuno di questi da' 36.** L'elenco autorevole e' quello **esplicito di Luca**: le **15** gia' coperte da `D01`-`D19` **piu' le 21** che ha nominato. Lo script **verifica che ognuna esista** nel registro.
>
> **⚠ E IL MIO ERRORE DI ESTRAZIONE, dichiarato:** cercavo l'ultimo `**Zxx**` *prima* della parola `CODICE`, ma **le righe CITANO altre voci nel corpo**, quindi l'ID pescato era spesso quello **citato**. Ora si parte dai **confini di riga**.

**10 DIFETTI nuovi · 20 gia' coperte · 7 non sono difetti — 37 voci in tutto.**

| voce | esito | ID | perche' |
|---|---|---|---|
| **`Z1`** | **DIFETTO** | **`D20`** *(APERTO)* | La correzione (1) su `inerzia` NON e' stata cablata, e **il gate che la autorizzava aveva misurato UN'ALTRA GRANDEZZA** |
| **`Z4`** | **DIFETTO** | **`D21`** *(APERTO)* | `_floor_d0` e' SOSPESA, e **i due rami violano assiomi DIVERSI**: la scelta non e' stata fatta |
| **`Z7`** | GIA' COPERTA | `D06` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z9-bis`** | GIA' COPERTA | `D07` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z10`** | GIA' COPERTA | `D07` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z11`** | GIA' COPERTA | `D13` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z14`** | GIA' COPERTA | `D08` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z24`** | **DIFETTO** | **`D22`** *(CURATO)* | Il DENOMINATORE PER GRADO: la misura non distingue (A) da (B), ma **(B) cade per DIMOSTRAZIONE**, e lo stesso schema e' in **almeno quattro punti** |
| **`Z25`** | GIA' COPERTA | `D22` | E' la CHIUSURA di `Z24`: il denominatore per grado era un errore ed e' stato TOLTO, sigillo `12/12` |
| **`Z33`** | GIA' COPERTA | `D14` | La mediana di `ritmo()` fa DUE mestieri; `Z41` **la supera sullo stesso oggetto** dicendo che ne fa TRE ed e' anche il rompi-anello |
| **`Z36`** | NON E' UN DIFETTO | — | **Ri-letta da `Z37`**: il `64.7 %` e' **un rapporto su una grandezza minuscola**, e gli stati consecutivi hanno overlap `> 0.99` nel `100 %` dei casi. **E' una lettura corretta di un numero, non un difetto del codice** |
| **`Z37`** | **DIFETTO** | **`D23`** *(APERTO)* | **La cucitura dello snapshot FALLISCE su entrambi i fronti**, e si DIMOSTRA perche'. **NON CABLATA** |
| **`Z38`** | NON E' UN DIFETTO | — | Il gauge attuale sta NELLA MATERIA e **la mia obiezione e' REFUTATA**. Una premessa che cade non e' un difetto: e' un riscontro |
| **`Z39`** | NON E' UN DIFETTO | — | **Un fatto stabile di `CLAUDE.md` e' caduto** *(`cs` e' vivo)*, e `CLAUDE.md` e' gia' stato corretto. **Il lavoro che ne discende e' il fronte `A`, non un difetto del codice** |
| **`Z40`** | **DIFETTO** | **`D24`** *(APERTO)* | **`A2` e' VIOLATO da `Lam = mean(I)`** -- una media GLOBALE dentro una legge locale -- **e la violazione e' la ragione per cui il pezzo funziona** |
| **`Z41`** | GIA' COPERTA | `D14` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z46`** | **DIFETTO** | **`D25`** *(APERTO)* | **Il gauge del tempo e' la costante `1e-9`**, e il `93 %` dei nodi non invecchia: sono sempre gli stessi, e sono le tre masse |
| **`Z53`** | **DIFETTO** | **`D26`** *(CURATO)* | Le coorti **non sopravvivevano allo SNAPSHOT**: dopo un salva/ricarica il lignaggio ripartiva VUOTO |
| **`Z65`** | **DIFETTO** | **`D27`** *(APERTO)* | **Il grafo e' in QUATTRO COMPONENTI che non si toccano mai**, e la bimodalita' del grado e' la semina. **Una distanza SUL GRAFO fra componenti diverse non esiste**, e le tre prove dell'ipotesi la usano |
| **`Z70`** | NON E' UN DIFETTO | — | **Corregge una lettura precedente**: l'anello `A6` c'e', ma non e' istantaneo e non passa dalla riga che era stata citata. **La correzione di una lettura non e' un difetto del codice** |
| **`Z71`** | GIA' COPERTA | `D15` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z73`** | GIA' COPERTA | `D09` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z74`** | **DIFETTO** | **`D28`** *(APERTO)* | **`nsub` esplode e lo tira `max(|vd|)` su POCHISSIMI archi**: il costo dell'intero sistema e' governato da una manciata di archi |
| **`Z75`** | GIA' COPERTA | `D10` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z77`** | **DIFETTO** | **`D29`** *(APERTO)* | **CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema**: il vuoto ha degli HUB, e non dovrebbe averne |
| **`Z79`** | GIA' COPERTA | `D18` | Il clip della coesione **scalava con `d0` stesso** *(`A11` cor.2)*; `COES_ADIM` lo ha sostituito col passo causale. **⚠ DA RIVERIFICARE sul blob corrente** |
| **`Z83`** | NON E' UN DIFETTO | — | E' una **DOMANDA dichiarata** *(`d0` deve stare sopra `LAM`?)*, e la decisione spetta a Luca. **Una domanda aperta non e' un difetto** |
| **`Z84`** | NON E' UN DIFETTO | — | **Descrive un MECCANISMO** -- `d` e `d0` sono un anello, ed e' `cs^2*lap` ad allungare l'arco. **Alimenta il sospetto `S01`**, non e' un difetto di per se' |
| **`Z86`** | NON E' UN DIFETTO | — | **E' un difetto di CRITERIO, non di codice**, e l'errore era mio. Vive in `doc/PATTERN_DI_PROVA.md` e in `P1-sexies`, non fra i difetti del simulatore |
| **`Z87`** | GIA' COPERTA | `D11` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z88`** | GIA' COPERTA | `D19` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z89`** | GIA' COPERTA | `D12` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z90`** | GIA' COPERTA | `D17` | La divergenza del ramo D *(`nsub = 22591`)* risaliva a **`peq` negativo**, curato da `PEQ_ESATTO`: `Z101` misura che **l'esplosione e' sparita** |
| **`Z91`** | GIA' COPERTA | `D16` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z92`** | GIA' COPERTA | `D18` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z94`** | GIA' COPERTA | `D17` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
| **`Z104`** | GIA' COPERTA | `D03` | gia' nella sezione DIFETTI APERTI dal recupero di `ccf1f73` |
<!-- TRIAGE-FINE -->

## SOSPETTI — **registrati, NON promossi**

> Un sospetto porta **la misura che lo decidera'**, non una prova. **Si promuove solo con la prova
> committata**, e la promozione si dichiara con `PROMOSSO: Sxx -> Dyy`.

| ID | il sospetto | la misura che lo decidera' | stato |
|---|---|---|---|
| **S01** | **Chi fa crescere `d0`**: in `G3` gli scrittori sommano `-1.6e+03` e `med d0` RADDOPPIA lo stesso | **il BILANCIO COMPLETO di `G4`** *(scritture + freno + nascite−morti)*, che dira' la percentuale di ciascuno | in attesa |
| **S02** | **Il freno di `SCALA_MIN` e' il motore di `d0`** | ✅ **DECISO da `Z108`**: bilancio che CHIUDE a `1.138e-13` su 600 passi, **il freno vale `+117.41 %` della crescita** | **PROMOSSO → `D31`** |
| **S03** | **La memoria del moto fa scappare `d0`** | ✅ **DECISO da `Z109`**: spegnendola `d0` **cresce ancora** *(`1.1607`)*, quindi **NON e' il motore** — ma la crescita **cala del `62 %`** e **la compressione sparisce** | **NON E' IL MOTORE, ma pesa il `62 %`** |
| **S04** | **La crescita e' NUCLEAZIONE, non stiramento** | ❌ **CADE con `Z108`**: nascite meno morti valgono lo **`0.01 %`** del `Δ` *(`+254.4` su `+1.731e+06`)* | **NON E' IL MOTORE** |
| **S05** | **La compressione `d/d0 < 1` e' un difetto** e non una fase | `G3` dice che **peggiora** senza gravita' *(`0.7489`→`0.6258`)*: serve una misura che ne trovi la CAUSA | in attesa |
| **S06** | **Il «muro dell'1 %» dell'antifase e' causato da `D35`**: l'antifase «non annichila» perche' **`+2π` letto da `exp(iφ)` non e' un'antifase, e' la stessa fase** | rimisurare l'annichilazione **dopo** la decisione su `φ` *(e' il test `E2` del §E)* | **in attesa** — «non annichila» e' una misura **PRE-FORK** *(par.9-bis)* e **non l'ho rimisurata** |
| **S07** | **`dphi_arc = angle(exp(1j·Δφ))` (`:5894`) COLLASSA a `2π` una differenza che vive su `4π`** — e' `B3` del mandato | **DORMIENTE**: `K_FRANGE = 0`, il ramo non gira. Da riesaminare **se** `K_FRANGE` venisse acceso, **o** quando `φ` passa a `2π` *(con `φ` su `2π` la riga diventa CORRETTA per costruzione)* | **in attesa** — **non e' un distinguitore**, e' un difetto di un'altra famiglia |
| **S08** | **Se `φ` non e' l'azimut del Bloch, CHE COS'E'?** | `Z121` ha **refutato** la frase del docstring *(`R ≤ 0.18` contro un nullo di `0.016`, criterio `≥ 0.90`)*, **ma non ha detto che cosa `φ` sia**. Serve una lettura della catena che la AGGIORNA *(`phivel`, `_phc`, `omega_clk`)* | **in attesa** — **refutare non e' spiegare**, e la differenza si scrive |
| **S09** | **IL TETTO DI `r` E' RAGGIUNTO PER UNA VIA CHE NON CONOSCIAMO** — *lettura di Luca, 2026-09-22*: **la quota di nodi al tetto SALE dopo aver tolto un meccanismo che ce li SPINGEVA** *(`Z123`: `+22 %`, `+49 %`, `+4 %` ai tre istanti)*. **Se togliendo una causa l'effetto cresce, la causa vera e' un'altra.** | ① rimisurare `median(|f|)` **a 600 passi** coi due wrap in parallelo *(a 120 passi `Z117` lo trovava INVARIATO, `1.000000`)* · ② e su **piu' semi**, perche' con uno la direzione non e' attribuibile | **in attesa.** **⚠ E' LO STESSO SCHEMA DEL FRENO:** *un limite che lavora tanto e' un ALLARME* *(`A11` cor.6)*. **La mia ipotesi — il gauge che si abbassa — e' UNA candidata, non la lettura**: quella di Luca e' piu' generale e non presuppone il meccanismo  **🟨 RIFORMULATO il 2026-09-24, e la formulazione vecchia era SBAGLIATA NEL MECCANISMO:** dicevo *«il gauge si abbassa, quindi `x = f/med` SALE PER TUTTI e piu' nodi arrivano al tetto»*. **MISURATO nel giro corto di `CURA 1` (`Z135`): `median(r)` SCENDE del `33 %`** *(`1.018363` → `0.680787`)* **e la quota al tetto SALE comunque** *(`0.76 %` → `1.02 %`)*. **Le due cose insieme dicono che LA DISTRIBUZIONE SI ALLARGA, non che si sposta:** la mediana cala e la coda al tetto cresce. **È la lettura di Luca, non la mia.** **CRITERIO DI CHIUSURA AGGIORNATO:** misurare la **DISPERSIONE** di `r` *(non la mediana)* su `>= 4` semi e a passi diversi, e capire **che cosa** allarga la distribuzione. |
| **S10** ❌**RITIRATA il 2026-09-24** | ~~Il tetto `1.414213` di `r` viene da un ramo di `ritmo()` che NON GIRA~~ | — | **RITIRATA, e la premessa era sbagliata DUE VOLTE.** **① `_g_temposegno_tot` sale a `:4406`, PRIMA del controllo `if TEMPO_SEGNO`, e in una FUNZIONE DIVERSA da `ritmo()`**: conta le INVOCAZIONI, non il ramo attivo, e **varrebbe `600` comunque**. **② `TEMPO_SEGNO` e' `False` in TUTTI i run ricostruibili** *(9 su 11, `--tempo-segno` assente da ogni lanciatore committato)*, **quindi il ramo che chiamavo «vivo» e' MORTO e quello che chiamavo «morto» e' VIVO.** **Il tetto `1.414213` E' del ramo che gira, e `Z117`/`Z123` lo citavano CORRETTAMENTE.** → `Z130` |
| **S11** | **`r` E' SATURO AL SUO TETTO PER UN TERZO DEI NODI, e la quota CRESCE: `0.76 %` -> `29.57 %` in 600 passi** *(`A11` cor.6: un limite che satura e' un allarme)* | rimisurare la quota al tetto su **>= 4 semi** e a passi diversi, e **capire perche' `median(r)` oscilla di un fattore 4** *(`1.018` / `0.594` / `0.763` / `0.344` / `1.409` ai cinque istanti)* quando il gauge lo ancorerebbe a `1` | **in attesa — EMERSO dal ritiro di `S10`, e va IN CODA (`A12` regola 1).** **MISURATO** su `_g4_riferimento`, 1 seme, 5 istanti *(`_r_corrente` dagli snapshot, commit `bc30e626`)*: quota con `r > 0.999 * tetto` **`0.76` / `1.19` / `0.83` / `3.35` / `29.57 %`**; `min(r)` al passo 360 vale **`1.414e-06`**, che e' la **firma dichiarata dal codice stesso** *(`f` identicamente nullo -> `x = 0`)*. **⚠ E NON E' UN DIFETTO DELLA CURA DELL'ANELLO ISTANTANEO:** il gauge e' il `median(|f|)` del passo **PRECEDENTE** *(cura di categoria D, 2026-09-18, che ha rotto il punto fisso di `A6`/`A3` DI PROPOSITO)*. Ricostruendo `r` col `median` CORRENTE si ottiene **mediana `1.000000` esatta**, cioe' il punto fisso pre-cura: **la differenza e' la cura, non un errore.** **Cio' che NON so e' perche' lo sfasamento produca una saturazione del 30 %**, e non lo inseguo adesso |
| **S12** ✅`APPROVATO DA LUCA il 2026-09-24` | **IL RILASSAMENTO DI `_rep` DENTRO `mitosi()` (`:5280`) E' UN EULERO ESPLICITO, e `par.4` LO VIETA** — `self._rep += _dte*(rep - self._rep)/max(tau_pp, 1e-12)` | riscriverlo nella forma **ESATTA** `_rep <- rep + (_rep - rep)*exp(-dt/tau)` e **misurare quante volte `dt_e/tau > 1`**, che e' la condizione in cui l'Eulero scavalca | **✅ APPROVATO: entra in `CURA 2` (par.3 della scheda ⑨).** E i difetti sulla riga erano **TRE**, non due: oltre all'Eulero e al `tau_pp` non-durata, **la dilatazione era contata DUE VOLTE** — `_dte` contiene gia' `0.5(r_i+r_j)`, e dividere anche per `tau_pp` la conta di nuovo. `CLAUDE.md` par.4: *«per il RILASSAMENTO di primo ordine usa il passo ESATTO, NON Verlet»* — e un Eulero esplicito e' **peggio** di Verlet su questo punto. **E' la stessa famiglia che `PEQ_ESATTO` (`C1`) ha curato per `peq`**, dove l'Eulero **scavalcava sotto zero** per `dt_e/tau > 1` *(misurato `1.2018` al passo 1126 del ramo D)*. **NON lo tocco in `CURA 2`:** mescolare *«quale tempo»* con *«quale integratore»* renderebbe il risultato ininterpretabile (par.1). **Ma curare il tempo e lasciare l'integratore sbagliato e' mezzo lavoro sulla stessa riga**, e la scelta e' di Luca. → scheda ⑨, par.5 ② |
| **S13** | **IL TEMPO D'ARCO DOVREBBE ESSERE `min(r_i, r_j)` INVECE DELLA MEDIA ARITMETICA?** — proposta per **TUTTO il sistema**, non per la mitosi | misurare, su >= 4 semi, quanto `min(r)` e `0.5(r_i+r_j)` differiscono **in pratica** *(se la dispersione di `r` fra vicini e' piccola, la differenza e' irrilevante e la proposta cade da se')*, e **derivare** se un processo d'arco possa avanzare piu' in fretta del suo estremo lento | **in attesa — nata dal mandato di `CURA 2`, e SPOSTATA QUI DA LUCA.** L'argomento causale e': un processo che vive sull'arco coinvolge **entrambi** i nodi, quindi non puo' avanzare piu' in fretta del **piu' lento** — altrimenti l'estremo lento riceverebbe, **nel proprio tempo proprio**, piu' di quanto il suo orologio ha battuto. **MA `dt_e = DT*0.5*(r_i+r_j)` (`:4352`) e' IL tempo d'arco del sistema**, e cambiarlo dentro la mitosi da sola creerebbe un **SECONDO orologio d'arco**: e' esattamente l'errore che `CURA 2` esiste per togliere. **Se la proposta vale, vale OVUNQUE.** **⚠ E IL SISTEMA HA GIA' DUE MEDIE D'ARCO, ciascuna col suo dominio:** **aritmetica** per il TEMPO (`dt_e`), **armonica** per la VELOCITA' (`cs_arco`, `:4774`, col commento *«collo di bottiglia causale: media armonica, non media aritmetica»*). **Una terza non si inventa senza una ragione derivata.** |
| **E4-LAM** ✅`FATTO il 2026-09-24` | **LA LEGGE «NESSUNA LUNGHEZZA SOTTO `LAM`» DEVE DIVENTARE STRUTTURALE** — sempre accesa, **candidata all'epoca 3** *(decisione di Luca, 2026-09-24)* | **DUE cose, distinte:** ① l'**INVARIANTE** `d >= LAM` di `C5` va reso **INCONDIZIONATO** *(oggi è gated su `SCALA_MIN or SCALA_MIN_PASSO`, `:3702`, e a flag spenti degrada a `d > 0`)*; ② la **REALIZZAZIONE** della legge va cambiata, perché oggi è il **freno a senso unico** = **`D31`** | **in attesa — NON è parte di `CURA 2`.** Rendere l'invariante incondizionato **cambierebbe il comportamento di una configurazione diversa da quella dei run**: a flag spenti un `d < LAM` oggi **passa**, domani **fermerebbe il run** con riga e indici. **È una decisione su `C5`, e la prende Luca.** **Per `CURA 2` non serve:** nei run `SCALA_MIN_PASSO` è acceso, l'invariante controlla `d >= LAM` davvero, e **misurato: `min(d) = 0.800000 = LAM` esatto, `0` archi sotto su `526302`**.  **✅ PUNTO ① FATTO: l'invariante è INCONDIZIONATO.** Sigillo `csv/_seal_fork/_sigillo_e4lam.py` **`6/6`**, collaudo **`8/8` con QUATTRO casi che devono fallire**. `T3`: un arco sotto `LAM` a flag SPENTI **ferma il run** con riga, regola, indici e arco. `T5`: **`206` campi identici, `0` diversi** contro `_cura1_corto`. **`_lam_attivo` non ha piu' riferimenti di CODICE** *(dall'AST: `[]`)*. **⏸ IL PUNTO ② RESTA APERTO:** la **REALIZZAZIONE** della legge è ancora il **freno a senso unico**, cioè **`D31`**. La scheda del freno-legge è il lavoro successivo. |


> **⚠⚠ `CHK3-D`: LA SEZIONE DEL CHECKPOINT SUI DIFETTI NUOVI, E IL SUO COSTO.**
> **Richiesta di Luca, 2026-09-22.** Nel referto del `CHK3` va una sezione **«I DIFETTI
> NUOVI CONTRO LE MISURE GIA' FATTE»**:
> **① `D27` — IL GRAFO IN QUATTRO COMPONENTI.** Per `G1`, `G2`, `G3` e `G4`: **quanti
> archi e nodi** stanno in ciascuna componente, e **se i numeri principali cambiano misurati
> componente per componente** *(saturazione, saldo per regione, crescita di `d0`, bilancio)*.
> **E le tre masse della scena stanno in componenti diverse?**
> **② `D25` — IL TEMPO CHE NON SCORRE.** **Quali schede del registro leggono il tempo
> proprio**, e **quanto del loro effetto si perde nel `93 %` dei nodi fermi**.
>
> **IL COSTO, DICHIARATO PRIMA DI FARE QUALUNQUE RUN** *(e dopo aver verificato dal disco cosa
> contengono gli snapshot: `i`, `j` e **`_r_corrente`** ci sono gia')*:
>
> | cosa | run? | costo |
> |---|---|---|
> | `D27` archi/nodi per componente + **dove stanno le tre masse** | **no**, da snapshot | ~2 min |
> | `D27` crescita di `d0` per componente su `G1`/`G3`/`G4` | **no**, da snapshot | incluso |
> | `D27` saturazione e saldo per regione, per componente | **si'**, rigiocata 120 passi | **~7 min** |
> | `D27` **bilancio** per componente, `G4` | **si'**, 600 passi per braccio | **~35 min × 2** |
> | `D25` quali leggi leggono il tempo proprio | **no**, lettura del sorgente | ~15 min |
> | `D25` quanti nodi fermi, distribuzione di `r` | **no**, `_r_corrente` e' nello snapshot | incluso |
> | `D25` effetto perso **per legge** | **si'**, la stessa rigiocata da 120 passi | incluso |
>
> **TOTALE: ~17 minuti senza il bilancio per componente, ~87 con.** Il pezzo caro e' **uno solo**,
> e **l'alternativa e' farlo su UN braccio (35 min)**: la domanda *«le componenti si
> comportano diversamente?»* riceve risposta gia' da uno.
>
> **⚠ COSA NON FARO' SENZA VIA LIBERA, e lo segnalo perche' sarebbe tentante:** il braccio di
> spegnimento **non e' ancora partito**, quindi potrei aggiungergli il conteggio per componente
> «gratis». **NON lo faccio: cambierebbe il blob dello strumento fra i due bracci e li
> renderebbe NON CONFRONTABILI.** I due bracci restano identici.

> **⚠⚠ IL MANDATO DEI PATTERN DI PROVA (2026-09-22), col §3 GIA' SOSTITUITO
> DALL'INTEGRAZIONE DI LUCA.**
> **PERCHE' ESISTE:** in `G3` sono emersi **cinque** pattern che hanno salvato la misura, e
> **nessuno di essi e' in `CLAUDE.md`** *(verificato dal disco: c'e' il controllo positivo nel
> par.10 e `P1-sexies`, ma non gli altri quattro)*. **Oggi li seguo perche' li ho davanti; in una
> sessione nuova, dopo una compattazione, non li avrei.** **Sopravvive solo cio' che sta nel
> repo** — e `CLAUDE.md` e' gia' a **1482 righe**, quindi il rischio opposto e' **diluirli**.
>
> **I CINQUE, gia' STANDARD:** ① **un processo per braccio** *(`b6f3c83`, `96c7f22`)* ·
> ② **firme dei byte, non `max|delta|`** *(`96c7f22`)* · ③ **assenza STRUTTURALE
> ≠ dato mancante**, e per chi concatena **lunghezze + firma della coda + firma dell'intero**
> *(`40f79dc`, `691eeba`)* · ④ **snapshot contro snapshot, allo STESSO ISTANTE**, e
> niente cast dei complessi *(`abc5b49`)* · ⑤ **il controllo dell'INVOLUCRO prima di
> ogni prova** *(`b812f92`, `c901456`)*.
>
> **⚠ IL §3 E' STATO SOSTITUITO DA LUCA, e la versione che vale e' questa —
> PROPOSTE «IN PROVA» COL VETO DI LUCA:**
> **NON aggiungo voci STANDARD da solo.** Un pattern nuovo — nato da un **fallimento di
> metodo** *oppure* da una **soluzione che ha funzionato** *(come il controllo dell'involucro)*
> — entra nella sezione **`IN PROVA`** con **quattro** cose: la regola in **una riga**, il
> **commit** in cui e' nato, il **difetto che previene o ha scoperto**, e **come si verifica che
> uno strumento lo rispetti**.
> **LO USO SUBITO**, senza aspettare, e **lo segnalo nel messaggio a Luca prima di `PUSHATO`**
> con la riga **`PROPOSTA IN PROVA: <regola>`**.
> **Diventa STANDARD solo col SI' ESPLICITO di Luca**, anche dato in blocco al checkpoint.
> **Se Luca non dice niente, resta IN PROVA.** **Se lo respinge**, va in fondo nella sezione
> **`RESPINTE`** **col motivo**, cosi' non si ripropone.
> **Ammissione solo se:** nasce da un **caso reale col suo commit** · si dice in **una
> riga** · **si puo' verificare**. **Ogni 10 voci standard, propongo anche cosa TOGLIERE o
> FONDERE.**
>
> **§4, IL COLLAUDO DEL DOCUMENTO:** rileggere **uno per uno** gli strumenti di prova attivi
> e scrivere, **per ciascun pattern, quali lo rispettano e quali no**. **NON si correggono
> subito:** chi non lo rispetta va in CODA **prima del suo prossimo utilizzo**. **Il runner di
> `G4` deve nascere gia' conforme ai cinque.**

> **⚠⚠ IL MANDATO DEL 2026-09-22: IL DISEGNO DENTRO LA FISICA.**
> **Tre fatti letti dal codice e VERIFICATI dal disco:**
> **①** `pozzo_grafo` **dichiara nel suo docstring** *«il pozzo non usa la geometria del rendering
> ... diviso per la DISTANZA REALE dell'arco»*, **e poi calcola `L` da `self.pos`, che E' il
> disegno.** La distanza reale esiste, ed e' **`d`**. **Il commento dice il FALSO**, e il pavimento
> `1e-9` su `L` e' **un'altra toppa** (`A11`).
> **②** `S09` clippa `spinta` al **passo causale** — quindi e' **gia' una LUNGHEZZA** — e poi la
> **moltiplica per `median(d0[mask])`**: statistica **GLOBALE** (`A2`, `A5`) **e lunghezza AL
> QUADRATO**. *(E il VERSO lo decide la TORSIONE, non la massa: e' una scelta di fisica forte, e va
> registrata come DOMANDA, non come difetto.)*
> **③** `mem_mot` prende le **direzioni da `pos`**, normalizza su `Imed` **globale**, e ha un tetto
> `0.01 * median(d0)` che viola **quattro** cose in una riga: coefficiente scelto (`A1`), statistica
> globale (`A2`), **dipende da cio' che limita** e **taglio secco** (`A11` corollari 2 e 7).
>
> **PRIMA SI MISURA E SI SPEGNE, POI SI CURA.** Nessuna cura fino al `CHK3`.


> **⚠ PERCHE' I RESIDUI DI `C5` VANNO PRIMA DEL RUN LUNGO E NON PRIMA DELLA CURA DI `d0`**
> *(decisione di Luca, 2026-09-21, 22:30)*:
> **gli invarianti CI SONO GIA' nella parte che conta** — accesi di default, 42 grandezze a ogni
> passo, completezza verificata, e **hanno dimostrato che avrebbero preso il caso del passo 1126**.
> La validazione di stasera e' girata **con loro accesi e senza una violazione**.
> **Cio' che manca serve al RUN LUNGO, non alla diagnosi di `d0`:** tre ore di calcolo in cui, se
> qualcosa va storto, **si vuole sapere SUBITO DOVE**.
> **E la modalita' FINE si e' gia' dimostrata utile STASERA STESSA:** per scattare sul passo 1126
> l'invariante ha dovuto **aspettare la fine del passo intero, circa mezz'ora**. **La modalita'
> fine l'avrebbe preso subito.**


> **⚠ PERCHE' IL COSMOLOGICO E' IN FONDO:** **le misure cosmologiche su un run che esplode NON
> misurano la cosmologia.** `M1`-`M4` chiedono se l'espansione sia senza centro e localmente
> trasparente; un run che attraversa picchi di `nsub` a `22591`, con `peq` fuori dal dominio fisico,
> **non e' il sistema di cui si vuole sapere questo.** **Prima si cura, poi si misura.**

> **⚠ REGISTRATI E NON CURATI IN QUESTO GIRO** *(GLOBALE §6, restano nel SOSPESO)*: **`n3`
> normalizzato su `median(d)`** · **la spinta `S09` moltiplicata per `median(d0)`** · **`Z47`** ·
> **la carica che non produce forze.**


> **⚠ Se una voce si blocca, le successive ASPETTANO: non si passa avanti.**
>
> **⚠⚠ SEGNALAZIONE A LUCA, come la coda stessa impone — IL MANDATO DEL 2026-09-21 CONTRADDICE QUESTA CODA, E LA CODA DICE DI SEGNALARLO.**
> **La coda** mette il **CHECKPOINT** alla voce **9**, cioe' **dopo** il cosmologico `M1`-`M4` (6), `Z47` parte ① (7), `M2`/`M3` (8) e l'archivio a rotazione (8-bis).
> **Il mandato** dice *«ORDINE: 1 lancia la rigiocata, 2 la lettura, 3 commit e push, 4 FERMATI: checkpoint a Luca»* — cioe' **checkpoint SUBITO, saltando 6, 7, 8 e 8-bis**.
> **Cosa ho fatto:** ho eseguito il mandato *(la diagnosi e' la voce **4-bis**, e la voce 4 era la prima non spuntata, quindi la diagnosi del suo esito sta al posto giusto)*, **e mi fermo al checkpoint senza toccare 6, 7, 8 e 8-bis**.
> **✅ RISOLTA il 2026-09-21: Luca ha RIORDINATO la coda lui**, ed e' l'ordine scritto qui sopra. La segnalazione resta leggibile perche' mostra che il meccanismo ha funzionato: **la coda ha vinto sul mandato, e' stato segnalato, e l'ordine l'ha deciso Luca.**

---

## SOSPESO

- **`Z47`, RICOGNIZIONE in coda:** parte dopo il lancio del ramo D (vedi `MANDATO_Z47_coda`), voce
  `7` della coda unica. **Sola lettura, nessuna CPU al run.**

---

# STATO DEI RUN — registro append-only

**Scritto AUTOMATICAMENTE da `csv/_stato_run.py`.** Il commit NON è
automatico (vedi la dichiarazione nel modulo): ma **il file esiste sempre**,
quindi dopo un riavvio lo stato si legge **dal disco**, non dalla memoria.

**Una voce `APERTO` senza `chiuso` = quel run è morto senza dirlo.**


## APERTO batch-1200 (campagna struttura)

- **avvio** `2026-09-18 17:42:46` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python soliton_simulator.py --batch --nmasse 3 --sep 8 --passi 1200 --ogni 10 --csv csv/_test_fork/_g1200/cond.csv --diaglog csv/_test_fork/_g1200/diag.csv --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com --guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part --sync-db csv/_test_fork/_g1200/stato.pkl --db-ogni 10 --db-cleanup
  ```
- **note** voce RICOSTRUITA dai dati sul disco: il registro non esisteva quando il run e' partito.
- *2026-09-18 17:42:46* — seed 900, letto da run.log. Una sola invocazione, 0 righe `[db] stato CARICATO`.
- *2026-09-18 17:42:46* — snapshot presi ai passi VERI 120 / 130 / 470 / 800 / 840 / 1200 (i primi tre mislabellati dal watcher e RINOMINATI col loro `_db_step`).

**chiuso 2026-09-18 17:42:46 — FINITO** Ultima riga di `diag.csv`: **passo 1200**, 21662 righe, `n = 1204`. **Dati COMPLETI.** Analisi fatta: `doc/REFERTO_chi_non_invecchia.md` (`Z46`/`Z9`). ⚠ **MANCA il referto dei QUATTRO BLOCCHI** del mandato «struttura a 1200» (maturazione / guscio / fasi / contrasto): la sonda `csv/_test_fork/_struttura_1200.py` e' COMMITTATA (`35a5786`) ma **NON E' MAI STATA GIRATA**.

## APERTO scena-video TENTATIVO 1

- **avvio** `2026-09-18 17:42:46` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_gvideo 10,115,190,270,375
  ```
- **note** voce RICOSTRUITA: il commit `b84702b` dice «RUN FERMATO» ma NON diceva a che punto.

**chiuso 2026-09-18 17:42:47 — FERMATO** Fermato al **frame ~50 su 400** *(`n` 2391 -> 2576, `14.1 s/frame`)*. **Motivo:** l'equivalenza del driver col `update()` del video era **DEDOTTA, non verificata**. **I dati parziali sono stati CANCELLATI** perche' su una traiettoria non certificata: **non servono.** Il sigillo `_sigillo_driver_video.py` ha poi dato **PASS** (14 array, `max|A-B| = 0.000e+00`, shape uguali).

## APERTO scena-video TENTATIVO 2 (in corso)

- **avvio** `2026-09-18 17:42:47` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_gvideo 10,115,190,270,375 > csv/_test_fork/_gvideo_run.log 2>&1
  ```
- **note** Rilanciato DOPO il PASS del sigillo del driver (`94e2ec0`).
- *2026-09-18 17:42:47* — **IN CORSO** al momento della scrittura: frame **170 su 400**, `n` 2391 -> 4120, `15.6 s/frame`. Snapshot gia' presi: **frame 10, frame 115**. Prossimi: 190 / 270 / 375.
- *2026-09-18 17:42:47* — ⚠ La scena include **`--tau-luce`, il cui SIGILLO E' FALLITO** (CLAUDE.md par.0): **ramo NON CERTIFICATO**, e ogni numero che ne esce lo eredita. E **`--chi-basc` riscrive `perc_chi` a ogni passo**: non e' un'etichetta di lignaggio.
- *2026-09-18 17:42:47* — ⚠ `PASSI_PER_FRAME = 6`: **400 frame = 2400 PASSI**. La tabella dei fotogrammi va RIMAPPATA (**frame 375 = passo 2250**), o i confronti con `Z46` (1200 passi) sbagliano di 2.
- *2026-09-18 17:46:16* — ✅ **IL REFERTO MANCANTE C'E'**: `doc/REFERTO_struttura_1200.md` (`Z48`). Letti gli istanti 120/800/1200; **130/470/840 NON letti** (la sonda cerca per NOME). La voce del batch e' CHIUSA e completa.
- *2026-09-18 18:10:22* — **frame 275/400** (`n` 2391 -> 5520, `15.6 s/frame`, ~33 min alla fine). Snapshot presi: **10, 115, 190, 270**. Manca **375**. ⚠ **L'INVERSIONE DELLA DILATAZIONE E' GIA' VISIBILE NEI MIEI DATI: `dil` da `+10.97 %` (frame 265) a `+8.59 %` (frame 275).** E al frame 270 `n = 5443` contro `5465` della tabella dei fotogrammi, `dil +10.75 %` contro `+10.3 %`: **e' la stessa scena.**
- *2026-09-18 18:42:13* — **frame 385/400**, `n = 7694`, `16.2 s/frame`. **TUTTI E CINQUE gli snapshot presi** (10/115/190/270/**375**). ⚠ **LA DILATAZIONE HA INVERTITO E STA OSCILLANDO:** `dil` = `-7.439 %` (370), `-2.704 %` (375), `-4.214 %` (380), `+2.797 %` (385). **Non e' solo «si ricomprime»: RIMBALZA.** `coer_l` continua a salire: `0.622 -> 0.631`. Al frame 375 `n = 7480` contro `7503` della tabella dei fotogrammi: **stessa scena.**

**chiuso 2026-09-18 18:47:44 — FINITO** **400 frame = 2400 passi in 6535 s (1h49)**, `16.34 s/frame`, **`n` da 2391 a 8018**. **SEI snapshot** (10/115/190/270/375/**400**). Stato finale: `coer_l = 0.669`, `dil = -1.13 %`. ⚠ **La dilatazione INVERTE e poi RIMBALZA**: `-7.44 %` (370) -> `-2.70 %` (375) -> `-4.21 %` (380) -> `+2.80 %` (385) -> `-1.13 %` (400). **La tabella dei fotogrammi si fermava al 375 e non poteva vederlo.** Dati in `csv/_test_fork/_gvideo/`; i `.pkl` NON si committano (48 MB l'uno).
- *2026-09-18 18:50:21* — ✅ **ANALISI FATTA**: `doc/REFERTO_struttura_video.md` (`Z49`). Sei istanti letti (frame 10/115/190/270/375/400 = passi 60/690/1140/1620/2250/2400).

## APERTO due-masse CONTROLLO (A/B su --nmasse)

- **avvio** `2026-09-18 19:40:56` · **blob** `a1ae5090` · **HEAD** `8f94cf4`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_g2m 10,115,190,270,375 fisica 2
  ```
- **note** A/B A VARIABILE SINGOLA contro `Z49`: cambia SOLO `--nmasse` (3 -> 2). **La PREDIZIONE DI LUCA e' committata PRIMA, in `a4fbe42`.**
- *2026-09-18 19:40:57* — pilota MISURATO: `n = 1894` alla semina, **`13.68 s/frame`** -> ~**1h35** per 400 frame. ⚠ **Il primo falsificatore scatta in parte: attendevo `n ~ 1594` (2/3 di 2391), misurato `1894` = il 79 %.** La semina per massa **NON e' lineare nel numero di masse**: le due scene differiscono anche per POPOLAZIONE, in modo non proporzionale. **Va nel referto.**

**chiuso 2026-09-18 21:10:45 — FINITO** **400 frame = 2400 passi in 5357.8 s (1h29)**, `13.40 s/frame`, **`n` da 1894 a 5878**. **SEI snapshot** (10/115/190/270/375/400) in `csv/_test_fork/_g2m/`. I `.pkl` NON si committano. **Confronto col run a TRE masse (`Z49`): `n` finale `5878` contro `8018`.**

## APERTO pilota-6000 (BLOCCANTE, prima del run lungo)

- **avvio** `2026-09-19 09:49:38` · **blob** `b9e07c73` · **HEAD** `d7b3a33`
- **comando**
  ```
  python soliton_simulator.py --batch --nmasse 3 --sep 8 --passi 300 --ogni 50 --db-ogni 300 --seed 900 --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com --guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part --sync-db csv/_test_fork/_pilota6000/pilota.pkl --csv csv/_test_fork/_pilota6000/pilota.csv
  ```
- **note** PILOTA BLOCCANTE del mandato par.1: il batch matura entro 6000 passi, o `r` e' al pavimento come dice `Z46`? Seme 900, lo STESSO di `Z46`, cosi' il confronto e' sulla stessa scena (A3c).

**chiuso 2026-09-19 09:49:38 — FINITO** **300 passi in 371 s = `123.7 s/100`** (il batch a 1200 dava `127.5`: REGGE). `.pkl` **26.45 MB**. **VERDETTO: il batch NON MATURA. `93.0 %` dei nodi e' al pavimento con `r/r_floor = 1.0000`, e il loro tasso da' `1.5 MILIONI` di passi per `ramp = 1`.** **IL RUN A 6000 SUL BATCH NON SI LANCIA.**

## APERTO run-6000 SCENA VIDEO (l'archivio a serie)

- **avvio** `2026-09-19 14:38:00` · **blob** `7c4dec1d` *(SIGILLATO 12/12)* · **HEAD** `406d31f`
- **seme effettivo** `42` — **letto da `Rete.__init__`, NON 900**: `SEME_INIZIALE = 900` e' il
  NUMERO DI NODI seminati (`:4532`), e solo nel `--batch` lo stesso 900 e' riusato come seme
  (`:6407`). Scrivere «seed 900» qui sarebbe falso.
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 1000 csv/_test_fork/_g6000 --serie=10 --csv-progresso=csv/_test_fork/_g6000/prog.csv
  ```
  → **1000 frame x 6 = 6000 passi**, snapshot **ogni 10 frame = 60 passi** → **100 snapshot**
  `scena_%06d.pkl.gz` (compressi a livello 1).
- **cadenza DERIVATA dal pilota**, non scelta: budget dichiarato **5.0 GB** prima di vedere i
  numeri; peso stimato **2.95-3.02 GB**; la cadenza 30 passi darebbe ~6 GB (oltre).
- **previsioni committate PRIMA**: `doc/PREVISIONI_run6000_scena.md`.
- **note** `--tau-luce` e' nel comando: sigillo **6/7**, `T3` e' un risultato dichiarato. Ogni
  numero di questo run lo eredita. `--chi-basc` riscrive `perc_chi`: non e' lignaggio.
- **attesa** ~**7.5 h** col modello lineare, **che SOTTOSTIMA** (il costo per frame cresce con `n`).
- **Z9-a all'avvio**: `passi(ramp=1) = 5098` sui mobili, contro i 6000 del run — **margine 18 %**,
  e `r` si e' mosso del **+149 % in 120 passi**: e' un'istantanea, non una previsione.

### ⚠ DA FARE A RUN FINITO — **la patch della ripresa, e la verifica che la precede**

> **✅ ASSORBITA il 2026-09-20 nella sezione «IL SOSPESO — LA LISTA UNICA» (voce `C`), e CHIUSA:**
> la ripresa **è** sul driver vero. Il testo resta per la cronaca, non come cosa da fare.

> **A RUN FINITO: portare la patch della ripresa sul driver vero** (`csv/_test_fork/_scena_video.py`,
> da **`f14ea4bd`** a **`7a02c5c3`**, la versione **sigillata 5/5** in
> `csv/_seal_fork/_sigillo_ripresa_scena.txt`). **NON prima che il run sia chiuso.**
>
> *(La patch era già stata applicata il 2026-09-19 alle ~15:55 **mentre il run girava**, e
> **ripristinata** alle 15:57:52 — commit `228eb07`. Non c'è stato danno, ed è **misurato**:
> `23f783e`, `3/3`, ripartendo dal passo 1800 si riottiene identico lo snapshot 1860 scritto
> durante quella finestra. **Ma «stavolta è andata bene» non è «era sicuro».**)*

> **PRIMA di applicare la patch, verificare DAL CODICE — non assumere — che gli snapshot di QUESTO
> run restino caricabili dopo che il driver è cambiato.**
>
> **Il ragionamento dice di sì:** `carica_stato` verifica il blob di **`soliton_simulator.py`**, non
> quello del driver, e il simulatore è **intatto** (`7c4dec1d` per tutta la sequenza).
> **Ma va CONFERMATO:** cercare dove viene usato il **blob del driver** (`f14ea4bd` → `7a02c5c3`) e
> se **BLOCCA** qualcosa.
>
> **Se esiste un controllo che include il driver e rifiuta:** il discriminante va riportato al blob
> del **SIMULATORE**, perché è quello che definisce la **FISICA** — e **solo perché** il sigillo del
> driver esteso ha dato **PASS** (`14 array, max|A-B| = 0.000e+00`). **Senza quel sigillo, NON si
> accetta.**
>
> **E la prova finale, dopo la patch:** ricaricare uno snapshot **di questo run** e riprendere.
> **Deve funzionare.**

**chiuso 2026-09-19 19:05 — FERMATO DA LUCA, dopo 2h30 di stallo.** **`450` frame su 1000 =
`2700` passi su 6000**, in `7013 s` di progresso utile più **~2h30 in cui il processo era VIVO e
non avanzava** (`15 817 s` di CPU totali, `99.6 %` su **un solo core**, nessuna scrittura dopo le
`16:35:05`).

**L'ARCHIVIO È INTATTO E COMPLETO fino al passo 2700**, verificato dopo l'arresto:
**45 snapshot su 45** si aprono, il `_db_step` **nel file** coincide con quello **nel nome**, serie
**contigua** da 60 a 2700 a cadenza 60, **nessun buco**, **nessun `.tmp`** lasciato a metà
*(`os.replace` è atomico: o il file c'è completo, o non c'è)*. **1.3 GB**, blob `7c4dec1d` ovunque.

**Il blocco NON è spiegato.** Escluso misurando: memoria *(287 MB usati, 11.5 GB liberi)*, disco
*(17 GB)*, CFL *(`_taup_cfl_max` fermo a `0.5657`, zero clamp)*, `MAX_NODI` *(9511 su 4 000 000)*,
`NaN`/`inf` *(zero su tutti gli array)*. → `doc/REFERTO_blocco_run6000.md`, dati grezzi in
`csv/_test_fork/_dump_2700.txt`.

**COSA RESTA FATTIBILE, e non è poco:** le misure del §3 del mandato — `Z9-b`, `ramp` per coorte,
`p95/p05`, le conseguenze, il ciclo — **si fanno su questi 45 snapshot senza rigirare niente**.
L'analizzatore è pronto: `csv/_test_fork/_misure_run6000.py`.

**E la ripresa è sigillata `5/5`:** si può ripartire dal passo 2700 — **ma prima va capito perché
si è fermato**, altrimenti si riparte verso lo stesso muro.

---

## CHECKPOINT 2026-09-20 — **chiusa la topologia (`Z65`). Il simulatore non è stato toccato.**

**HEAD `3a02819` · blob `775ceab7` · albero pulito · nessun processo in esecuzione.**

**Fatto oggi, tutto sui 45 snapshot già in archivio, senza rigirare niente:** le somme (`Z63`), `f`
e `median(|f|)` (`Z64`), e **la topologia (`Z65`)** — quattro componenti connesse che in 2700 passi
non si scambiano **nemmeno un arco**, i due picchi del grado che sono **la semina** (tre grafi
**completi** da 497 nodi al passo 6) e non una forma emersa, e il **grado 2 permanente** (84 % dopo
2100 passi). → `doc/REFERTO_topologia.md`.

**Un presidio che prima era un'assunzione, ora misurato:** `eta[k]` non diminuisce in **nessuna**
delle 44 transizioni → **gli indici dei nodi sono stabili**, e ogni misura di coorte fatta finora
poggiava su quello senza averlo verificato.

### Cosa resta da fare quando il run è definitivamente chiuso

> **✅ ASSORBITA il 2026-09-20 in «IL SOSPESO — LA LISTA UNICA»:** il punto 1 è **CHIUSO**
> (voce `C`), il punto 2 puntava al **bersaglio sbagliato** (voce `B10`), il punto 3 è la voce
> `B9`. Il testo resta per la cronaca.

1. **riapplicare la patch di ripresa** a `csv/_test_fork/_scena_video.py` (`f14ea4bd` → `7a02c5c3`),
   **dopo** aver verificato dal codice che gli snapshot dell'archivio restano caricabili col blob
   del driver cambiato; poi rigirare il sigillo del driver e **provare davvero** un ricarico +
   ripresa da uno snapshot reale;
2. **togliere `--override-blob`** dal driver: è un presidio **deliberatamente indebolito**,
   accettabile solo finché gli esperimenti su `COPPIA_RECIPROCA` / `GRAV_AMPIEZZA` sono aperti;
3. **i fronti aperti che nessuna misura di oggi ha chiuso:** perché il run si sia fermato al 2700;
   perché la catena `f → x → r` non riproduca `r` dal passo 24 (`Z64`, famiglia `Z19`); perché 1455
   nodi stiano a `10⁻¹³` nel ramo A e qualunque perturbazione della coppia li accenda (`Z63`); se
   il profilo identico delle due cure sia **divergenza caotica** — servirebbe un terzo braccio con
   perturbazione nulla, o un secondo seme.

---

## 2026-09-20 — **L'ORDINE DEL LAVORO, deciso da Luca: ① → ② → ③**

**HEAD `e403e15` · simulatore `f81c4fe1`** *(sha1 byte grezzi; blob git `af8a96f1`)* · albero
pulito · **nessun run in esecuzione.**

```
①  LE GUARDIE DI PRECONDIZIONE          <- in corso
②  IL PANNELLO FEDELE                   <- dopo ①
③  IL RUN LUNGO a sep = 4.0             <- PER ULTIMO
```

**Nessun run parte finché ① e ② non sono chiusi.**

### Cosa è già pronto per ③, e resta sigillato

- **il driver** `csv/_test_fork/_scena_video.py`: `--sep=X` nominale *(sigillo `4/4`)* e la
  **ripresa** `--riprendi` *(sigillo `5/5` sul driver VERO)*;
- **il pilota a `sep = 4.0`**: archi massa-massa **0**, archi massa-vuoto **97 447** stabili
  *(−0.15 % in 300 passi)*, **una componente**, **196 nodi `MISTO`**;
- **la cadenza proposta**: `--serie=20` *(= `--db-ogni 120` passi)* → **83 snapshot, 3.0-4.5 GB**
  su **15 GB liberi** *(disco al 97 %)*;
- **il costo misurato**: `2.922 s/passo` → **8.1 ore come LIMITE INFERIORE** per 10.000 passi.

### ⚠ E una regola che sarebbe servita due giorni fa

> **Prima di interpretare QUALUNQUE struttura vista in un pannello, verificare che ci siano ARCHI
> in quella regione.**

**Il caso reale:** nel run a `sep = 8` il pannello del campo mostrava interferenza **fra le masse**,
e le masse stavano in **quattro componenti connesse con ZERO archi fra loro** *(`Z65`)*. Il
pannello non mentiva — `campo_spaziale` somma su **tutti i nodi**, non sugli archi — **ma la
lettura sì.** Il tool del video (`csv/_test_fork/_video_da_snapshot.py`) stampa il conteggio degli
archi fra componenti **su ogni frame**, proprio per questo.

---

## 2026-09-20 (sera) — **L'ORDINE SI ALLUNGA: ① → ② → ③ → ④**

```
①  LE GUARDIE                      CHIUSO   Z67 (5/5) · Z68 (3/3) · Z69 (3/4 + 1 atteso)
②  IL PANNELLO FEDELE              prossimo
③  LE METRICHE DEL SETTORE CHIRALE + un giro breve a sep = 4.0
④  IL RUN LUNGO a sep = 4.0        per ultimo
```

**Le metriche vanno PRIMA del run: otto ore senza i dati che servono sarebbero da rifare.**

### ⚠ E l'`83 %` a `-1` del passo 2700 NON VALE — ma non per la ragione che sembrava

**Non è (solo) che il grafo fosse in quattro componenti scollegate.** È che **`perc_chi` non è un
lignaggio**: con `CHI_BASC = 1` *(ed era `1` nel run)* la riga `:3765` **riscrive l'intero array a
ogni passo** da `twn > PHI_CRIT`.

> **Quell'`83 %` è la frazione di nodi che NON hanno completato un giro di olonomia.**
> **È un dato sulla TORSIONE, letto come se fosse un dato sulla CHIRALITÀ.**

**E l'eredità chirale della mitosi (`:4294`) e la coppia opposta di Schwinger (`:4415`) sono
appese DOPO `chi_basc` nel ciclo, quindi sopravvivono ESATTAMENTE ZERO passi completi.**
*(Dettaglio e righe in `doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md`.)*

### La voce TODO del ② — il pannello fedele

> **✅ ASSORBITA il 2026-09-20 in «IL SOSPESO — LA LISTA UNICA», voce `A5`.**
> Il testo resta: contiene i VINCOLI, che la lista non ripete.

**Il problema, misurato:** `campo_spaziale` somma su **tutti i nodi** con la FFT; `calcola_psi`
solo **sugli archi**. Nel run a `sep = 8` il pannello mostrava interferenza **fra masse in quattro
componenti con zero archi fra loro**.
**Cosa fare:** **un pannello IN PIÙ** che **interpola `psi`** sulla stessa griglia. **Entrambi
restano** — `campo_spaziale` dà **continuità**, l'interpolazione dà **fedeltà**, il grafo dà la
**topologia**.
**Vincoli:** non si tocca `campo_spaziale` né la FFT · **il blob del simulatore NON cambia: è
rendering** · **l'interpolazione LEGGE `psi`, non lo RICALCOLA** *(precedente `lambda_vuoto`)* · i
buchi si **dichiarano** · uno smoothing, se serve, ha la scala **derivata** · **si misura il costo.**

---

# IL SOSPESO — **LA LISTA UNICA** (censita il 2026-09-20, verificata DAL DISCO)

> **Questa è LA lista.** Le tre liste parziali che esistevano prima — *«DA FARE A RUN FINITO»*,
> *«Cosa resta da fare quando il run è definitivamente chiuso»*, *«La voce TODO del ② — il pannello
> fedele»* — **sono ASSORBITE qui** e portano un rimando. **Non se ne apre una quarta.**

**⚠ COME È STATA FATTA, perché cambia quanto ci si può fidare:** l'elenco di partenza veniva dalla
conversazione. **Ogni voce è stata verificata dal disco**, e la verifica ha prodotto **tre
correzioni all'elenco di partenza e due miei errori** *(§ «Cosa la verifica ha cambiato»)*.

### La legenda della validità — **il presidio contro le tre ritrattazioni di oggi**

```
VALE SEMPRE            un difetto di codice, una legge, un fatto letto dal sorgente
VALE PER QUELLA SCENA  un numero misurato su sep = 8 / quattro componenti / una finestra
DA RIVERIFICARE        la premessa sotto è cambiata (scena nuova, blob nuovo, cura applicata)
```
**Il discriminante è una domanda sola:** *«se rigirassi questo su un'altra scena, il numero
cambierebbe?»* Se sì → `VALE PER QUELLA SCENA`. Se la domanda non ha senso perché non c'è un numero
(è una lettura del codice) → `VALE SEMPRE`.

---

## A — LASCIATE A METÀ OGGI (2026-09-20)

| # | la voce | dove sta | a che punto è | cosa manca | chi decide | validità |
|---|---|---|---|---|---|---|
| **A1-TREVIE** | **la catena a TRE VIE di `step`** — `if CHI_CORE… / elif VERSO_CHI… / elif not(…)` | **`:3623` · `:3626` · `:3632`** *(⚠ era citata `:3517`-`:3526`: **slittata di 106 righe**, ritrovata per CONTENUTO)*; `doc/REFERTO_classifica_18_guardie.md` righe 25-27, 90-91 | **né applicata né scartata.** Verificato: **nessun contatore** sulla catena, mentre la gemella `:2366` ne ha quattro | **la FORMA**: tre contatori `_salti` (uno per ramo) **oppure** uno con tre conteggi «quale ramo». Io avevo già dichiarato di preferire **nessuno dei due** *(un contatore per ramo su una scelta a tre vie non misura un fallimento, misura una selezione)* — e l'avevo dichiarata come **mia deviazione dal mandato** | **LUCA** | `VALE SEMPRE` |
| **A2-ANELLO** | **l'anello `A6` di `Z70`** — periodo 2, via `chiralita_core_locale`/`CHI_CORE` | `doc/RAMIFICAZIONI.md` `Z70` | **registrato, NON curato.** `A6` nella sua *lettera* non è violato (ogni gamba legge lo snapshot d'inizio passo), ma `perc_chi` è **schiava** di `tw` | la cura è **un giro a sé** e non è stata fatta | **LUCA** *(è una cura, non una misura)* | `VALE SEMPRE` |
| **A3-CHIRALE** | **`Z71` — la carica chirale non si conserva** | `doc/RAMIFICAZIONI.md` `Z71` | **APERTA.** I due punti di scrittura sono verificati dal codice: **`:4294`** eredita UGUALE *(rompe)*, **`:4415`** antinodo OPPOSTO *(conserva)* | **una decisione di FISICA**: *la carica chirale deve conservarsi?* Se sì `:4294` è un difetto; se no, è il meccanismo. **Non si cura senza quella decisione** | **LUCA** | `VALE SEMPRE` |
| **A4-METRICHE** | **le METRICHE DEL SETTORE CHIRALE** | **`doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md`** *(⚠ il documento **ESISTE**: vedi i miei errori, §E)* | **punto 1 del TODO fatto** *(il §1 verificato dal codice)*; **punti 2-5 aperti** | il pannello fedele **viene prima** *(è `A5`)*, poi le metriche byte-inerti, il sigillo, la voce nel registro | **io** | **`DA RIVERIFICARE`** — la metrica ④ era *«flip di `chi_basc`»* e **non è misurabile così**; ma **nel ramo B del run in corso `chi_basc` è SPENTO, quindi `perc_chi` È una carica** e la metrica torna misurabile nella forma «confronto di `perc_chi` prima/dopo» |
| **A5-PANNELLO** | **il PANNELLO FEDELE** *(interpolazione di `psi` accanto a `campo_spaziale`)* | la **ex-LISTA 3** di questo file | **non iniziato** | un pannello **in più**, che **legge** `psi` e non lo ricalcola; i buchi dichiarati; il costo misurato. Il blob del simulatore **non cambia: è rendering** | **io** | `VALE SEMPRE` |
| **A6-PERCCHI** | **`perc_chi` FA DUE LAVORI CON REGOLE OPPOSTE: `chi_basc` lo tratta da CHIRALITA', `TEMPO_SEGNO` da CARICA** — e finche' condividono un array **nessuno dei due puo' essere fatto bene** | `:3558` *(`TEMPO_SEGNO` legge `perc_chi` e ne ricava il VERSO DEL TEMPO)* · `:3765` *(`chi_basc` lo RISCRIVE a ogni passo dalla torsione)* · `:4294` / `:4466` *(le nascite)* · `Z70` `Z71` `Z73` | **REGISTRATA il 2026-09-20, NON iniziata.** **Nasce da un RAGIONAMENTO, non da una misura**, e va letta come tale | **LA PROPOSTA — da decidere, NON eseguita:** separare in **due grandezze**: una **CARICA** nuova, **scritta SOLO alla nascita e mai ricalcolata**, **opposta nelle coppie di Schwinger** (`:4466`), **letta da `TEMPO_SEGNO`**; e **`perc_chi` lasciata libera di essere GEOMETRIA**. *(Il nome della carica nuova NON lo invento: e' una scelta di progetto.)* **⚠ E LA FISICA DISTINGUE DAVVERO LE DUE COSE: la chiralita' NON si conserva** *(una particella con massa la cambia viaggiando)*, **una carica si' — sempre.** **Il NOME e' quello della prima, l'USO di `TEMPO_SEGNO` e' quello della seconda.** **⚠ PERCHE' LA DECISIONE CAMBIA RISPETTO A PRIMA:** la separazione in due array era gia' stata valutata e **SCARTATA**, con la ragione che la seconda grandezza sarebbe rimasta **SENZA LETTORI** — cioe' `A8`, un ramo silenzioso. **Un lettore ora c'e': `TEMPO_SEGNO` (`:3558`).** **⚠⚠ MA VERIFICATO DAL DISCO, E VA DETTO: `TEMPO_SEGNO = False` di default (`:858`), e il driver dei due run A/B NON lo passa — quindi nei run era SPENTO.** **Il lettore esiste nel CODICE ed e' INERTE nei fatti: la ragione dello scarto e' decaduta a META', non del tutto.** **COSA SISTEMEREBBE:** **`Z71`** *(la carica non si conserva: `:4294` eredita UGUALE e rompe, `:4415` OPPOSTA e conserva)* **diventerebbe una domanda DECIDIBILE invece che ambigua**; l'ambiguita' **`A10`** *(un solo significato per grandezza)*; e la domanda **«ogni nascita deve essere una COPPIA?»**, che e' `Z71` in un'altra forma — **se `perc_chi` e' una carica la coppia e' obbligata, se e' un'etichetta no.** **⚠ E COSA NON SISTEMEREBBE, verificato e non assunto: NON tocca il problema di `d0`.** La **coesione relazionale** (`:4877`), che nella traccia risulta **dominante e in giu'** (`-3.68e+03` su 120 passi), lavora su **geometria pura** — `cos2 = (r_rad/H)^2`, `radiale = grav*cos2` — **e `memoria_hebbiana_moto` (righe `4694-5016`) contiene ZERO occorrenze di `perc_chi`.** **I due problemi sono INDIPENDENTI e si curano separatamente**, e lo scrivo perche' domani non vengano legati per comodita' | **LUCA** — **e' una decisione di FISICA, non di codice** | 🟩`VALE SEMPRE` |

---

## B — APERTE DA PRIMA

| # | la voce | dove sta | a che punto è | cosa manca | chi decide | validità |
|---|---|---|---|---|---|---|
| **B1** | **`Z47` — `pos` nella fisica: l'ultimo SFONDO** | `doc/RAMIFICAZIONI.md` `Z47`, `doc/ASSIOMI.md` | **NON INIZIATO**, e il registro lo qualifica già *«progetto di lungo periodo»* | **il costo DECIDE**: non è una modifica, è la **riscrittura di QUATTRO settori** | **LUCA** | `VALE SEMPRE` |
| **B2** | **`Z31` — i sigilli non ri-girabili** | `Z31`, citata in **17 file** | **rifatta TRE volte**, l'ultima ieri | il recupero sistematico → **è il §2.2 del mandato di oggi**, in corso | **io** | `VALE SEMPRE` |
| **B3** | **i rami di `memoria_hebbiana_moto`** | `soliton_simulator.py:4616-4918` | **mai guardati** | ⚠ **sono `25`, non `23`** *(contati dal codice: `if`/`elif`/`else`/`try`/`except` nel corpo della funzione, 303 righe)*. Quanti siano su un **percorso fisico** non è misurato | **io** | `VALE SEMPRE` |
| **B4** | **i `np.zeros`** | tutto il simulatore | **mai guardati** | ⚠ **sono `116`, non `~10`**. Il numero utile non è questo: serve **restringere al percorso fisico**, e quel conto **non esiste ancora** | **io** | `VALE SEMPRE` |
| **B5** | **`theta` / l'aliasing del settore di spin** | `CLAUDE.md` §9, registro `C14`, fronte `A` | **aperto e noto**: `theta` ~ 39-129 giri/passo | `C14` chiude solo con `theta` sotto il tetto `2π·cs/λ`. **È il collo di bottiglia del programma** | **LUCA** *(è la voce `A`)* | `VALE SEMPRE` |
| **B6** | **le due cure OFF: `COPPIA_RECIPROCA` e `GRAV_AMPIEZZA`** | `:739` e `:732` *(entrambe `= False`)*, `doc/REFERTO_somme.md`, due task history del 19/9 | **A/B NEGATIVI** — ma fatti su **QUATTRO COMPONENTI SCOLLEGATE** | **rifare gli A/B sulla scena connessa `sep = 4.0`** | **io** | **`DA RIVERIFICARE`** |
| **B7** | **i reperti DA RIMISURARE sulla scena nuova** | `Z43`, `Z46`, `Z48`-`Z52`, `coer_g` | **misurati su `sep = 8`** | rimisura sulla scena connessa. **Marcatura già presente su 4 su 7**: `Z48`/`Z50`/`Z51` portano «QUALIFICATA», `Z49` dice «scena VIDEO»; **`Z46` non porta NESSUNA marcatura** | **io** | **`VALE PER QUELLA SCENA`** |
| **B8** | **⚠ IL BLOCCO DEL RUN A 6000 AL PASSO 2700** | **`doc/REFERTO_blocco_run6000.md`** *(131 righe)*, `csv/_test_fork/_dump_2700.txt` | ⚠ **NON «mai diagnosticato»: PARZIALMENTE diagnosticato.** **Sei** ipotesi **escluse misurandole** *(memoria, disco, CFL, `MAX_NODI`, `NaN`, contatori)*; la degenerazione documentata *(`d0` max `43 → 395`, `1227` archi sopra `10×p50`)*; lo **stato al 2700 CATTURATO** (45 snapshot + dump di 113 chiavi). **Ciò che NON fu catturato è lo STACK** | **la causa resta ③ «non lo so»**, dichiarata come tale nel referto | **io** | `VALE PER QUELLA SCENA` *(i numeri)* + `VALE SEMPRE` *(le esclusioni)* |
| **B9** | **`Z63` / `Z64`** — i 1455 nodi a `10⁻¹³`; la catena `f → x → r` che non riproduce `r` | registro, **ex-LISTA 2 punto 3** | aperti | vedi le rispettive voci | **io** | `VALE PER QUELLA SCENA` |
| **B10** | **⚠ `--override-blob` e la COPIA del driver** | `csv/_test_fork/_scena_video_ripresa.py` *(`e68bb8c5`, 17466 byte)* e `csv/_seal_fork/_ab_reciprocita.py` | ⚠ **DUE fatti nuovi.** ① **`--override-blob` NON è nel driver vero** *(`0` occorrenze in `_scena_video.py`)*: la ex-LISTA 2 punto 2 **puntava al bersaglio sbagliato**. ② **la COPIA `_scena_video_ripresa.py` ESISTE ANCORA ed è tracciata da git**, mentre il docstring del driver vero dice *«la copia è stata rimossa»* | **un docstring STALE** *(la classe di difetto che `CLAUDE.md` §0 chiama per nome)*, e **un secondo driver nel repo che porta un presidio deliberatamente indebolito** | **io** *(il docstring)* · **LUCA** *(se la copia va tolta)* | `VALE SEMPRE` |

---

## C — CHIUSE DALLA VERIFICA DI OGGI *(tolte dalla lista, e si dice perché)*

| la voce | era | ora | la prova |
|---|---|---|---|
| **ex-LISTA 1** e **ex-LISTA 2 punto 1** — *«riapplicare la patch della ripresa al driver vero»* | **DA FARE A RUN FINITO** | **✅ CHIUSA** | la ripresa **è** nel driver vero *(`10` occorrenze di `--riprendi`/`RIPRENDI` in `_scena_video.py`)*, e il driver attuale `9aee4fc2` la contiene |
| **ex-LISTA 2 punto 2** — *«togliere `--override-blob` dal driver»* | DA FARE | **✅ CHIUSA PER IL DRIVER VERO** *(0 occorrenze)* — **ma resta aperta altrove: → `B10`** | `grep` sul disco |

---

## D — IL CONTO

```
voci sospese CENSITE          15      (5 lasciate a meta' oggi + 10 aperte da prima)
  di cui DECIDE LUCA           5      A1, A2, A3, B1, B5   (+ meta' di B10)
  di cui decido io            10
voci CHIUSE dalla verifica     2      le due ex-liste sulla patch della ripresa
```

**E il registro, misurato nello stesso giro** *(`doc/RAMIFICAZIONI.md`)*:
```
righe-voce                   138
  con un segnale ESPLICITO di apertura      24
  con un segnale ESPLICITO di chiusura      22
  con ENTRAMBI (ambigue)                    19
  MUTE (nessuno dei due)                    73      <- il 53 %
```
> **⚠ Le `73` mute non sono «73 voci aperte»: sono voci il cui stato NON SI LEGGE senza leggerle
> tutte.** È la misura, non il verdetto — e dice che **il registro non è interrogabile
> meccanicamente**.

---

## E — COSA LA VERIFICA HA CAMBIATO, **inclusi due errori miei**

**Tre correzioni all'elenco di partenza:**
1. **il blocco al 2700 NON è «mai diagnosticato»** — c'è un referto di 131 righe con sei ipotesi
   escluse **per misura**. Quello che manca è **lo stack**, non la diagnosi *(→ `B8`)*;
2. **i rami di `memoria_hebbiana_moto` sono `25`, non `23`**, e i `np.zeros` sono **`116`, non
   `~10`** — contati dal codice *(→ `B3`, `B4`)*;
3. **`--override-blob` non è nel driver vero**: il punto della ex-lista puntava al bersaglio
   sbagliato, e il bersaglio giusto è una **copia del driver che doveva essere stata rimossa**
   *(→ `B10`)*.

**Due errori MIEI, dichiarati:**
- ho riportato *«metriche chirali: 0 file»* e *«23 rami: 0 file»*. **Falso in entrambi i casi:** il
  mio `grep` usava `-e "a|b"` **senza `-E`**, quindi l'alternanza era cercata come testo letterale.
  **`doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md` ESISTE** *(→ `A4`)*;
- le righe `:3517`-`:3526` che avevo citato **erano slittate di 106 righe** — è il §0 di
  `CLAUDE.md` *(«cerca per NOME, non per riga»)* applicato contro me stesso *(→ `A1`)*.

---

## F — UN PRESIDIO CHE ORA ESISTE DAVVERO: `py-spy`

`doc/REFERTO_blocco_run6000.md` §5 diceva: *«quello che servirebbe è banale e non ce l'ho:
`py-spy dump` legge lo stack di un processo vivo dall'esterno, senza toccarlo. Non è installato.»*

> **Installato oggi (`0.4.2`) ed ESERCITATO su un run VIVO**, non su un test:
> ```
> py-spy dump --pid 9264      (ramo A, mentre gira)
>   chiralita_core_locale (soliton_simulator.py:1556)
>   step (soliton_simulator.py:3624)
>   <module> (_scena_video.py:231)
> ```
> **`A9`: un presidio provato quando NON serve è un presidio; uno scritto e mai esercitato è una
> nota.** La volta scorsa il processo fu ucciso senza catturare lo stack, **e non si saprà mai**.

**PID dei due run in corso: ramo A `9264`, ramo B `30996`.**
**Se uno si pianta — soglia: più di ~1500 s senza uno snapshot nuovo — `py-spy dump` PRIMA di
qualunque altra cosa, e NON si uccide.**

---

## APERTO ab_sep4_A_e_B

- **avvio** `2026-09-20 16:26:43` · **blob** `b44f50ce` · **HEAD** `0f12645`
- **comando**
  ```
  ramo A (chi_basc ON, il default):
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_A --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_A/prog.csv
ramo B (chi_basc OFF):
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_B --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_B/prog.csv --chi-basc=off
  ```
- **note** A/B COMPLETO di chi_basc a sep=4.0, i DUE rami IN PARALLELO, 500 frame = 3000 passi ciascuno, uno snapshot ogni 20 frame = 120 passi = 25 per ramo. UNA sola voce per DUE processi perche' sono UN esperimento: un interruttore solo, tutto il resto identico. Geometria verificata alla semina: componenti = 1, archi massa-vuoto = 97590, massa-massa = 0. Disco: 14 GB liberi, stima 1.95 GB. CPU: 6 fisici, parallelo misurato 26.03 s/frame per ramo, stima 3.8-4.5 h. Driver 9aee4fc2, sigillo --chi-basc= 5/5.
- *2026-09-20 19:16:19* — RAMO B FERMATO alle 19:15:26 per decisione di Luca, al frame 65 di 500 (passo 390 di 3000). NON e chiuso l intero esperimento: il ramo A continua, quindi la voce resta APERTA e si chiudera quando A finisce. ARCHIVIO PARZIALE DI B INTATTO E VERIFICATO: 3 snapshot (120, 240, 360), nessun .tmp orfano, tutti caricabili, blob b44f50ce, e il passo nei DATI coincide col nome. MOTIVO: proiezione oltre 33 ore e in peggioramento. CATTURA FINALE PRIMA DELLO STOP, ed e il reperto piu importante dello stop stesso: nsub era passato da 206 a 15594, e IL VINCOLO VINCENTE ERA CAMBIATO -- n3 (|vd|) fermo a 205, ma n1 (la SORGENTE) esploso a 15594. Seconda fase della divergenza, che si sarebbe persa uccidendo senza catturare. File: csv/_test_fork/_diag_B/stack_FINALE_1915.txt

**chiuso 2026-09-20 20:21:06 — FINITO** ESITO ASIMMETRICO, e sono due esiti diversi non uno. RAMO A (chi_basc ACCESO): ARRIVATO INTATTO ai 3000 passi alle 20:20 circa. 500 frame, 28.014 s/frame medio, n da 2391 a 18000, archi 546792, coer_l finale 0.7324, dil +126.96 per cento. 25 snapshot su 25 scritti, 0 saltati, 0 FALLITI, 0.97 GB. Il costo per frame e cresciuto da 27.457 a 28.015, cioe del 2 per cento su 3000 passi: PIATTO. nsub restava 4, il pavimento. RAMO B (chi_basc SPENTO): FERMATO da Luca alle 19:15 al frame 65 di 500, passo 390 di 3000, con nsub a 15594 e proiezione oltre 73 ore. 3 snapshot intatti e verificati. LIMITE DA TENERE: UN SEME PER RAMO, quindi la differenza NON e attribuibile a chi_basc -- il nullo di un confronto fra bracci e la dispersione FRA SEMI, che questo esperimento non misura. Referti: REFERTO_ramoB_sottopassi_CFL, REFERTO_fuga_vd_ramoB, REFERTO_venti_archi_e_nsub, REFERTO_innesco_cinque, REFERTO_rigiocata_0_120. Voci: Z74 Z75 Z76 Z77, piu Z73 corretta in loco due volte.

## APERTO ramo_D_epoca2

- **avvio** `2026-09-21 10:15:20` · **blob** `26fa354d` (git) / `4954fe5b` (byte grezzi) · **HEAD** `ccf3aba`
- ⚠ **NOTA SUL BLOB, e vale per TUTTE le voci precedenti di questo file:** fino a oggi `_stato_run._blob_byte()` calcolava il blob **GIT** dichiarando di calcolare i **byte grezzi**. **Diceva l'opposto di cio' che faceva.** Nessun dato e' perso — un blob git si recupera con `git cat-file` — ma **l'etichetta era falsa**, e mandava chi verifica a cercare un oggetto nella convenzione sbagliata. **Corretto: ora si stampano ENTRAMBE.** Le voci storiche vanno lette come **blob GIT**.
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_D --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_D/prog.csv --chi-coop=on --scala-min=on --coes-adim=on
  ```
- **note** RAMO D -- EPOCA 2. Le TRE modifiche accese insieme (CHI_COOP, SCALA_MIN, COES_ADIM) piu' la cura del mondo-dopo-i-flag (categoria D, nessun flag). 500 frame = 3000 passi, uno snapshot ogni 20 frame = 120 passi = 25 snapshot. Sigillo 11/11 (d69e5bae sul simulatore 4954fe5b). PRESIDI PRIMA DEL LANCIO: componenti connesse = 1; min(d) = min(d0) = 0.800000000 = LAM, archi sotto LAM 0 e 0; mediana d/d0 = 1.000000 (nasce NON teso); n = 2391, archi = 525973; processi python vivi 0. DISCO: 5.9 GB liberi su 476, 99 per cento pieno -- il ramo A produsse 0.97 GB in 25 snapshot quindi D ci sta, MA IL MARGINE E' STRETTO. ⚠ NESSUN CONFRONTO CON A, B o C: sono epoca 1, e le letture di D vanno contro criteri ASSOLUTI. ⚠ E con tre interruttori accesi insieme nessun esito e' attribuibile a nessuno dei tre: i confronti legittimi verranno DOPO e DENTRO il sistema nuovo.
- *2026-09-21 11:29:33* — ⚠ FERMATO alle 11:05 al frame 205 di 500 (passo 1230) -- CONFIGURAZIONE SBAGLIATA, non una scelta: il driver NON inoltrava --scala-min e --coes-adim al simulatore. Letto DAL MODULO: CHI_COOP True ma SCALA_MIN False e COES_ADIM False. Le opzioni erano PARSATE e IGNORATE, in silenzio. py-spy dump catturato PRIMA dello stop (csv/_test_fork/_diag_D/stack_STOP_config_sbagliata.txt). Archivio parziale INTATTO e verificato: 10 snapshot (120..1200), tutti caricabili, 0 .tmp orfani.

**chiuso 2026-09-21 11:29:33 — FERMATO** NON E' IL RAMO D: e' un run con CHI_COOP acceso e SCALA_MIN/COES_ADIM spenti, su blob di epoca 2 -- cioe' la COOPERAZIONE da sola. I dati parziali NON si buttano (10 snapshot leggibili, 120..1200 passi) ma NON rispondono alla domanda del mandato perentorio, che chiede le TRE modifiche insieme. CAUSA: la patch al driver usava str.replace con un solo assert GLOBALE, soddisfatto dalle ALTRE sostituzioni; la terza non ha attaccato in silenzio. Nessun sigillo poteva prenderlo: quelli esistenti costruiscono sys.argv da soli e NON passano dal driver. Presidio nuovo: csv/_seal_fork/_sigillo_flag_driver.py. IL RAMO D VA RILANCIATO DA ZERO dopo che il sigillo passa.

## APERTO ramo_D_epoca2_bis

- **avvio** `2026-09-21 11:32:04` · **blob** `26fa354d (git) / 4954fe5b (byte grezzi)` · **HEAD** `ec41deb`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_D --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_D/prog.csv --chi-coop=on --scala-min=on --coes-adim=on
  ```
- **note** RAMO D, SECONDO LANCIO -- il primo (10:15-11:05) girava con SCALA_MIN e COES_ADIM SPENTI perche' il driver non li inoltrava: difetto trovato, riparato, e coperto dal presidio nuovo csv/_seal_fork/_sigillo_flag_driver.py (3/3: ogni opzione arriva al MODULO in entrambi i versi, e l'elenco delle opzioni e' SCOPERTO dal sorgente invece che scritto a mano). Il driver e' ora 5544f3b9 -> riparato. L'archivio del primo lancio e' conservato in csv/_test_fork/_ab_C_solo_chicoop_FERMATO (10 snapshot, 120..1200, tutti leggibili): NON e' il ramo D, e' la COOPERAZIONE da sola su blob di epoca 2. Questa volta il primo controllo dopo l'avvio e' il blocco FLAG ATTIVI letto DAL MODULO.
- *2026-09-21 12:57:51* — ⚠ DIVERGENZA: nsub = 22591 contro il pavimento 4, catturato con py-spy dump --locals sul PID 19912 (PROCESSO NON UCCISO). Il vincolo vincente e' n1 = 22591 (la SORGENTE), mentre n3 = 3 e n2 = 1: NON e' |vd| a esplodere. Stessa firma del ramo B, ma li' chi_basc era SPENTO e qui e' ACCESO con le tre modifiche attive. Il processo calcola (8.4 s CPU su 12 s reali): e' LENTO, non morto. Ultimo dato pulito: frame 185 a 20.537 s/frame; ultimo snapshot su disco: passo 1080 (9 file). A questo nsub i 315 frame restanti sono GIORNI. Referto: doc/REFERTO_nsub_ramoD.md, voce Z90.

**chiuso 2026-09-21 13:14:20 — FERMATO** Fermato al frame 205 di 500 (passo 1230) dopo py-spy dump. nsub = 22591 con n1 = 22591 (la SORGENTE), n2 = 1, n3 = 3: a quel ritmo i 295 frame restanti erano GIORNI. ARCHIVIO INTATTO: 10 snapshot (120..1200), tutti apribili, zero .tmp orfani, ed e arrivato anche il 1200 che al momento della diagnosi mancava. I DATI SERVONO e sono gia analizzati: csv/_analisi_ramoD.py, output in csv/_test_fork/_diag_D/ANALISI_ramoD_2026-09-21.txt. RISULTATO PRINCIPALE: i due flag hanno INVERTITO il regime rispetto al solo CHI_COOP -- da TENSIONE con d0 inchiodato a 0.83 e 55909 archi sotto LAM, a COMPRESSIONE con d0 a 30 e ZERO archi sotto LAM. E peq CROLLA di 14 ordini (1.38e-14 al passo 1200) subito prima dell esplosione di n1.

## APERTO run_S_solo_scalamin

- **avvio** `2026-09-21 13:25:11` · **blob** `26fa354d (git) / 4954fe5b (byte grezzi)` · **HEAD** `5ab29e6`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 50 csv/_test_fork/_run_S --sep=4.0 --serie=10 --csv-progresso=csv/_test_fork/_run_S/prog.csv --chi-coop=on --scala-min=on --coes-adim=off
  ```
- **note** §1 del mandato: CHI DEI DUE fa scappare d0. RUN S = SOLO SCALA_MIN (COES_ADIM SPENTO), 50 frame = 300 passi. TRACCIA_D0 va acceso a mano nel driver? NO: si accende dal simulatore, e il driver non lo passa -- verificato, quindi questo run misura d0 SENZA la traccia per scrittore. LETTURE FISSATE PRIMA: se d0 scappa solo in S -> e' il CRICCHETTO di SCALA_MIN; solo in K -> e' il contrappeso perso di COES_ADIM; in entrambi -> tutte e due; in nessuno -> e' l'INTERAZIONE. Uno alla volta, MAI in parallelo.

**chiuso 2026-09-21 14:31:19 — FINITO** 50 frame = 300 passi, 17.340 s/frame, 5 snapshot su 5, 0 falliti, 0.18 GB. RISULTATO: d0 NON SCAPPA con SCALA_MIN da solo -- med d0 resta 0.89, 0.81, 0.80, 0.80, 0.81 mentre med d cresce da 1.02 a 2.03 e d/d0 sale a 2.48 (TENSIONE). E ZERO archi sotto LAM a ogni snapshot, contro i 55909 del ramo C senza i due flag: SCALA_MIN fa il suo mestiere SENZA far scappare d0. Il cricchetto DA SOLO non spiega la fuga del ramo D.

## APERTO run_K_solo_coesadim

- **avvio** `2026-09-21 14:31:36` · **blob** `26fa354d (git) / 4954fe5b (byte grezzi)` · **HEAD** `6981a0f`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 50 csv/_test_fork/_run_K --sep=4.0 --serie=10 --csv-progresso=csv/_test_fork/_run_K/prog.csv --chi-coop=on --scala-min=off --coes-adim=on
  ```
- **note** §1 del mandato, SECONDO run: K = SOLO COES_ADIM (SCALA_MIN SPENTO), 300 passi. Il run S ha gia' ESCLUSO il cricchetto da solo: con SCALA_MIN acceso e COES_ADIM spento, med d0 resta ~0.80 piatto. LETTURA FISSATA PRIMA: se d0 scappa in K -> e' il CONTRAPPESO PERSO di COES_ADIM; se non scappa nemmeno in K -> e' l'INTERAZIONE fra i due, e va detto cosi'. Uno alla volta.

**chiuso 2026-09-21 15:20:16 — FINITO** 50 frame = 300 passi, 20.711 s/frame, 5 snapshot su 5, 0 falliti, 0.18 GB. RISULTATO: d0 in K CRESCE ma piano -- da 0.9728 a 1.3124, cioe' x1.35 su 300 passi -- mentre in S resta piatto (x0.91) e in D scappa (x15 su 1080 passi, e gia' a 2.02 al passo 120 quando K e' a 0.997). NESSUNO DEI DUE FLAG DA SOLO RIPRODUCE LA FUGA: e' l'INTERAZIONE, ed e' la terza possibilita' fissata PRIMA. E K ha d/d0 ~1.2, il piu' vicino alla trasparenza fra tutte le configurazioni, ma con 71114 archi sotto LAM perche' SCALA_MIN e' spento.

## APERTO validazione-600

- **avvio** `2026-09-21 21:10:40` · **blob** `f2628c16 (git) / 9557a867 (byte grezzi)` · **HEAD** `92fe29e`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 100 csv/_test_fork/_val600 --sep=4.0 --serie=20 --chi-basc=on --chi-coop=on --scala-min=off --coes-adim=on --peq-esatto=on --peq-nascita-locale=on --scala-min-passo=on --coes-causale=on --anom-simm=on --invarianti=on --csv-progresso=csv/_test_fork/_val600/prog.csv
  ```
- **note** VALIDAZIONE delle SEI cure (C1, C2, C3, C4, C1-bis, C5) + le tre modifiche di epoca 2. 600 passi, sep=4.0, stesso seme, invarianti ACCESI, archivio a SERIE ogni 20 frame (RIPRENDIBILE: il PC si riavvia fra mezzanotte e le due). --scala-min=off perche' SCALA_MIN_PASSO lo SOSTITUISCE. CHECKPOINT 2: a run finito ci si FERMA e si aspetta Luca.

**chiuso 2026-09-21 22:30:54 — FINITO** 600 passi completati in 2100.5 s (21.0 s/frame). 5 snapshot, 0.18 GB, 0 falliti. SEI criteri su OTTO REGGONO: nsub massimo 4 (il pavimento, contro 22591 del ramo D), peq >= 0 sempre (min 2.04e-07), zero archi sotto LAM, ZERO violazioni di dominio, stress finito 7.87, coesione al massimo al 23.8% del cono locale. NON REGGONO: d0 scappa ancora (med d0 da 1.4150 a 3.3180, rapporto COSTANTE 1.2320 = ESPONENZIALE) e d/d0 sta fra 0.69 e 0.84, cioe' COMPRESSIONE. I due criteri che cadono NON sono quelli che le cure dovevano curare: la fuga di d0 e' il fronte S09/S10, escluso da questo giro dal mandato globale. IL RUN LUNGO NON SI LANCIA. I dati servono: sono la base del prossimo giro.

## APERTO F2P-CORTO

- **avvio** `2026-09-24 11:54:57` · **blob** `024747ef (git) / 445e2896 (byte grezzi)` · **HEAD** `b5e9a9a`
- **comando**
  ```
  python csv/_test_fork/_g4_prova.py --fase-2pi-corto
  ```
- **note** STANDARD 7: il giro CORTO (120 passi) prima del giro vero. Serve a misurare il COSTO: se la mitosi accelera del fattore previsto (5x-100x), archi e tempo esplodono. Criteri committati PRIMA in b5e9a9a. Destinazione csv/_test_fork/_f2p_corto.
- *2026-09-24 11:55:34* — PARTITO: PID Windows 15112 (il processo python.exe, NON la shell), 2026-09-24 ~11:5x. 20 frame = 120 passi. Log: csv/_test_fork/_f2p_corto_log.txt

**chiuso 2026-09-24 12:06:04 — FINITO** 120 passi in 444.7 s, 1 snapshot + BILANCIO (chiude a 4.041e-14). ESITO DEI TEST 2/4: E1a NON PASSA (mitosi 1 evento contro 62, Schwinger 0 contro 28), E1c NON PASSA (0.345x contro la banda 5x-100x: MIA previsione sbagliata NEL VERSO), E1b e E4 PASSANO. I dati parziali SERVONO: sono la prova di D36. Il run a 600 passi NON e stato lanciato (par.5: si committa il fallimento e si ferma).

## APERTO CURA1-CORTO

- **avvio** `2026-09-24 14:41:14` · **blob** `0e06edf2 (git) / dd82794a (byte grezzi)` · **HEAD** `9d6e43e`
- **comando**
  ```
  python csv/_test_fork/_g4_prova.py --cura1-corto
  ```
- **note** Il giro corto della CURA 1: 120 passi col driver che accende --ritmo-wrap-2pi. Sigillo 6/6 (287e27d). Destinazione csv/_test_fork/_cura1_corto. Confronto: _g4_riferimento, che ha girato SENZA la cura.
- *2026-09-24 14:41:14* — PARTITO: PID Windows 27128, 2026-09-24 ~14:40. 20 frame = 120 passi.

**chiuso 2026-09-24 14:51:33 — FINITO** 120 passi in 509.0 s. CONFIGURAZIONE.txt conferma RITMO_WRAP_2PI=True e TW_SPINORE=False. Bilancio CHIUDE (4.721e-14). La mitosi NON muore: 209 nati/67 eventi contro 203/62. Unico effetto sopra il nullo: median(r) -33 percento. I dati SERVONO: sono la prova di CURA 1.

## APERTO SIGILLO-CURA2

- **avvio** `2026-09-24 18:41:03` · **blob** `800666c2 (git) / b881db89 (byte grezzi)` · **HEAD** `c04d2b0`
- **comando**
  ```
  python csv/_seal_fork/_sigillo_cura2.py
  ```
- **note** Sigillo di CURA 2. T4 byte-inerzia a flag SPENTO contro _cura1_corto/scena_000120.pkl.gz; T5 controllo positivo a flag ACCESO. Due giri da 120 passi, ~17 min. Collaudo 6/6 e T1/T2/T3 gia' PASS. Codice: c04d2b0, blob b881db89. Sigillo: a11e3c5.

**chiuso 2026-09-24 18:53:50 — FINITO** Stampato 5/5 ma T5 e INVALIDO (Z145): i due bracci girano nello stesso processo e il secondo e partito da un mondo piu piccolo (n 901 contro 2660, archi 59731 contro 526302, 33.3 s contro 404.5 s), e n NON PUO scendere. T1/T2/T3/T4 valgono: T4 da 206 campi identici al riferimento fresco, quindi la byte-inerzia a flag spento e certificata. Il controllo positivo di CURA 2 NON e stabilito. I dati SERVONO: T4 risponde al criterio K (clip su prob e clip alto su rep: ZERO su 63148047). Giro corto NON lanciato: reperto, commit, stop.

## APERTO CURA2-CORTO

- **avvio** `2026-09-24 19:06:12` · **blob** `67ea1a19 (git) / 49fc54d2 (byte grezzi)` · **HEAD** `7a36ae5`
- **comando**
  ```
  python csv/_test_fork/_g4_prova.py --cura2-corto
  ```
- **note** Il giro corto di CURA 2: 120 passi, PROCESSO FRESCO A UN SOLO BRACCIO (standard 1). E la decisione di Luca: T5 := questo run contro _cura1_corto, che e anchesso un processo fresco a un solo braccio. E anche V8/V9 (distribuzione di |dx|/d) e il clip a ZERO di prob. Codice 7a36ae5, blob 49fc54d2. Riferimento: csv/_test_fork/_cura1_corto.
- *2026-09-24 19:12:11* — frame 10/20 (passo 60): n 2393 -> 2459, archi ~526061. LA MITOSI E VIVA. Confronto col T5 contaminato: quello dava n=901 e 59731 archi. Z145 confermato dal disco.

**chiuso 2026-09-24 19:17:24 — FINITO** 120 passi in 520.1 s. n 2393 -> 2575, archi 526204. Bilancio CHIUDE (5.304e-14). V8/V9 nel BILANCIO_d0.txt: |dx|/d max 0.0531, ZERO campioni sopra 0.5. I dati SERVONO: sono T5 (il controllo positivo rifatto in processo fresco, dopo Z145) e la misura che sceglie la forma del freno-legge.

## APERTO SIGILLO-CURA2-RIPARATO

- **avvio** `2026-09-24 19:26:36` · **blob** `67ea1a19 (git) / 49fc54d2 (byte grezzi)` · **HEAD** `1afa968`
- **comando**
  ```
  python csv/_seal_fork/_sigillo_cura2.py
  ```
- **note** Decisione di Luca (1a): T4 byte-inerzia sul blob 49fc54d2 col sigillo RIPARATO, UN PROCESSO PER BRACCIO (standard 1). Due bracci in subprocess, ~17 min. Il T4 precedente era sul blob b881db89, PRIMA del contatore del clip a zero: questo ri-certifica la byte-inerzia sul blob che ha girato il giro corto. Sigillo 2f5155b.

**chiuso 2026-09-24 19:42:22 — FINITO** 5/5. T4 PASS sul blob 49fc54d2: 206 campi identici, 0 diversi -- la byte-inerzia del contatore del clip a zero era DICHIARATA per costruzione, ora e MISURATA. T5 PASS, e l n del braccio acceso e 2575, lo stesso del giro corto: riproducibilita fra processi diversi. Bracci: SPENTO 398.3 s, ACCESO 379.9 s, ciascuno nel suo processo. I dati SERVONO. E ne e uscito il controllo STANDARD 5 (involucro di _g4_prova inerte, 217 firme identiche) e un difetto del mio confronta_snap: usa array_equal, che su NaN dichiara diversi due array identici.

## APERTO pilota-prova1

- **avvio** `2026-09-27 09:06:45` · **blob** `c968d4d8 (git) / e203f9a8 (byte grezzi)` · **HEAD** `4a7597e`
- **comando**
  ```
  python csv/_test_fork/_pilota_prova1.py   (4 semi 11-14, 120 passi, checkpoint 0/40/80/120)
  ```
- **note** PILOTA della PROVA 1, NON il run base (5 SI aperti). Driver con POZZO_D acceso, scena (ii)(a) sep 6.1158, passo_pieno (H-P9), un processo per seme. Criteri V1-V6 in doc/TASK_HISTORY/2026-09-27_pilota-prova1.md, committati PRIMA. Nessuna conclusione sulla gravita' dal pilota: solo i numeri e i limiti.

**chiuso 2026-09-27 09:09:11 — FERMATO** FERMATO da Luca dopo ~4 minuti (nessun checkpoint oltre il passo 0 raggiunto: il primo e' a 40). DIFETTO BLOCCANTE nello strumento, non nel run: `controlli()` RISCEGLIE i punti di controllo a ogni checkpoint sulla distanza del momento, quindi la loro variazione e' ~0 PER COSTRUZIONE e l'osservabile (masse - controlli) si riduce al solo avvicinamento delle masse: V2 non separa piu' la gravita' dalla contrazione globale, che e' il suo UNICO scopo. I DATI PARZIALI NON SERVONO: nessun json e' stato scritto (il braccio scrive alla fine). Si rilancia dopo la cura dei controlli FISSI, committata prima.

## APERTO pilota-prova1-bis

- **avvio** `2026-09-27 09:22:28` · **blob** `c968d4d8 (git) / e203f9a8 (byte grezzi)` · **HEAD** `2ebbd25`
- **comando**
  ```
  python csv/_test_fork/_pilota_prova1.py   (4 semi 11-14, 120 passi, checkpoint 0/40/80/120)
  ```
- **note** RILANCIO dopo la cura CTRL-RISCELTA (controlli FISSI, K5 2/2). PILOTA, NON il run base (5 SI aperti). Driver con POZZO_D acceso, scena (ii)(a) sep 6.1158, passo_pieno (H-P9), un processo per seme. Criteri V1-V6 committati PRIMA. Nessuna conclusione sulla gravita'.

**chiuso 2026-09-27 09:58:32 — FINITO** 4 semi su 4 arrivati in fondo, 120 passi, checkpoint 0/40/80/120. Referto in csv/_test_fork/_pilota_prova1/REFERTO.txt, confronto con la previsione in CONFRONTO_previsione.txt. ESITO: l'osservabile A(t) coi controlli FISSI e' negativo OLTRE l'IC95 su 2 coppie su 3 al passo 40 e 2 su 3 al passo 80; a 120 nessuna, perche' la sd fra semi delle masse cresce di ~30x (voce PROVA1-40-80). Due mie previsioni su tre FALSIFICATE (a: le masse si avvicinano piu' dei controlli; b: nessun allungamento), la terza col meccanismo giusto e le soglie sbagliate (c). ZERO nascite nelle masse e nel varco: tutte nel vuoto. Il 39 % delle coppie Schwinger accorcia il grafo (SCHW-CORTI). Quattro difetti nuovi dai miei criteri: V5-SOGLIA, FOGLIO-NULLO, FORMA-N-VUOTO, e il residuo A2 S09-MEDIANA trovato leggendo. NESSUNA conclusione sulla gravita': il pilota non e' il run base (5 SI aperti).

## APERTO pilota-prova1-stati

- **avvio** `2026-09-27 10:46:43` · **blob** `c968d4d8 (git) / e203f9a8 (byte grezzi)` · **HEAD** `0e7810b`
- **comando**
  ```
  python csv/_test_fork/_pilota_prova1.py --salva-stati --ogni 2   (4 semi, 120 passi)
  ```
- **note** IL RUN UNICO che serve a TRE cose: (1) gli STATI del grafo ai checkpoint per la scomposizione del CAMMINO (TRATTI) e per MASSA-ID offline; (2) i FOTOGRAMMI ogni 2 passi sul seme 11 per il video (VIDEO-SCENA); (3) la ripetizione della misura del pilota. Tutti i .npz restano LOCALI (STATI-LOCALI, gia' in .gitignore). Strumenti committati in 0e7810b PRIMA del lancio (par.5).

**chiuso 2026-09-27 11:29:11 — FINITO** 4 semi su 4 in fondo, 120 passi. Prodotti: 16 stati del grafo ai checkpoint (i, j, d, phi, pos, n), 61 fotogrammi pos/phi/phi_g/dpozzo/ii/jj sul seme 11, 4 file di coorti del passo 0 -- 81 .npz in tutto, TUTTI LOCALI (STATI-LOCALI, .gitignore). Piu' i 4 misura.json, committabili. kappa scelto 3. Il run serve a TRE cose: la scomposizione del CAMMINO (TRATTI), MASSA-ID-FISSO offline, e il video (VIDEO-SCENA). Strumenti committati in 0e7810b e c8b6dd9 PRIMA del lancio.

---

## `SCHW-SOTTO-LAM` — lo Schwinger fa nascere archi SOTTO `LAM`, e `_nasce` li alza

*(aperto il 2026-10-04, su mandato del guardiano. **Da REGISTRARE, non da curare:** la
cura la decide Luca.)*

**IL FATTO, e viene da un referto committato**, non da un sospetto: nel sigillo del `6a`
*(`1927b45`)* i contatori dicono **`_sm_trd_schwinger = 46`** e
**`_sm_trd0_schwinger = 46`** sulla somma delle quattro scene. ### **Quarantasei archi
nascono dallo Schwinger piu' corti di `LAM`, e `_nasce` li ALZA al pavimento.**

> ### 📌 **QUINDI `A13` ALLA NASCITA — *un arco non nasce piu' corto della lunghezza
> d'onda* — vale per la MITOSI e NON per lo SCHWINGER.** Ed e' proprio la legge che il
> commit `6b` rende **incondizionata** sul sito della mitosi: rendere incondizionato quel
> cancello ### **lascia lo Schwinger esattamente come e'.**

### **PERCHE' ACCADE, letto dal codice** *(non dedotto)*: la lunghezza dei due archi
nuovi dello Schwinger viene da **`pos`** — la distanza fra `aa` e `bb` —
**non da `d`** come nella mitosi:

```
_L_sch = np.linalg.norm(self.pos[aa] - self.pos[bb], axis=1)
_dd_a  = np.maximum(FRAZ_NASCITA * _L_sch, 0.05)
_dd_b  = np.maximum((1.0 - FRAZ_NASCITA) * _L_sch, 0.05)
```

### **E nessun cancello confronta `_L_sch` con `LAM` prima di creare gli archi:** il solo
limite e' il `np.maximum(..., 0.05)`, che e' ### **un pavimento assoluto, non `LAM`** —
cioe' `A11` applicato, `A13` no.

### **IL LEGAME CON `SCHW-CORTI`, e la differenza — che conta**

| voce | che cosa guarda | che cosa dice |
|---|---|---|
| **`SCHW-CORTI`** | la **SOMMA** | il `39 %` delle coppie **accorcia il grafo** (`2*dd < d`) |
| **`SCHW-SOTTO-LAM`** | il **SINGOLO ARCO** | `46` archi nascono **sotto `LAM`** e vengono alzati |

### ⚠ **Sono due sintomi della STESSA origine** *(la lunghezza viene da `pos` e nessuno la
confronta con `LAM`)*, ### **ma curare una non cura automaticamente l'altra:** un cancello
su `LAM` per singolo arco non impedisce che la somma accorci, e un vincolo sulla somma non
impedisce che un singolo arco nasca corto.

### ✅ **E IL TRONCAMENTO NON E' INVISIBILE: `_nasce` lo CONTA.** E' per questo che il
numero `46` esiste invece di essere un'impressione — ### **il contatore e' il motivo per
cui questa voce si puo' scrivere con un numero.**

**CRITERIO DI CHIUSURA** *(una voce senza criterio e' un desiderio, non un fronte)*: una
**decisione di Luca** su ① se il cancello di `A13` alla nascita vada **esteso** al sito
Schwinger, e ② se la lunghezza da confrontare con `LAM` sia quella da **`pos`** o una
**derivata da `d`**. ### ⛔ **NON SI DECIDE AL SUO POSTO** *(`L-DOPO-STOP`)*.

---

## `NON-TRACCIATI` — le decisioni di Luca del 2026-10-04, e il controllo che BLOCCA

**Il censimento** *(`csv/_censimento_non_tracciati.py`, referto `0b3b2a0`)* ha classificato
**484** file non tracciati: **32** copie rigenerabili del simulatore, **212** stub,
**85** binari di stato, **155** candidati — di cui **98 citati** e **57 no**.

### ⚠ **E IL NUMERO CHE CONTA SONO I 98, non i 57** *(disaccordo del guardiano col mio
referto, accolto da Luca)*. Un file **non citato e non tracciato** e' **rumore**: nessuno
lo cerca. Un file **CITATO e non tracciato** e' **un riferimento al vuoto** —
### **chi verifica dal repo lo cerca e non lo trova.** ### **E' il caso `_sonda_scherm`.**

### ⛔ **IL `COMMIT 1` E' BLOCCATO DAL SUO PROPRIO CONTROLLO: `67` file TRACCIATI**
sarebbero coperti dalle regole nuove, non i soli casi del par.7 che la decisione
prevedeva. ### **Il caso decisivo sono i `31` `_corsa.txt`: il nome generico E' la
convenzione committata.**

### 📌 **E l'effetto sarebbe l'OPPOSTO dello scopo:** la decisione nasce per far
significare *«non tracciato» = «dimenticato»*; una regola che rende **invisibile un
referto scritto correttamente** lo fa significare *«coperto da una riga `!` che nessuno ha
aggiunto»*.

**Il dettaglio, la tabella dei 67, il vincolo tecnico su `csv/**/_tmp/` e le due strade
stanno in `doc/TASK_HISTORY/2026-10-04_file-non-tracciati.md`.**
### ⛔ **La scelta fra (A) e (B) e' di Luca** *(`L-DOPO-STOP`)*, e i `COMMIT 2`…`7` non
dipendono da quella regola.

## `CONTA-RIGHE` — **due convenzioni per contare le righe, e una non e' quella del
presidio** *(aperto il 2026-10-04)*

**IL DIFETTO, curato:** i due strumenti del riordino di `CLAUDE.md` contavano
`count(NL) + 1`; **`H-RIGHE`** — ### **il presidio che IMPONE il tetto delle 400 righe**
— conta i **fine-riga** in `csv/_presidio_righe.conta`, come `wc -l`. Su un file che
**termina** con un fine-riga le due formule differiscono di **uno**, e il referto del
riordino dichiaro' **`392 → 282`** dove il vero era **`391 → 281`**.
**Curati** in `12625c2` importando `_presidio_righe.conta`: ### **una sola definizione nel
repo, non una seconda formula corretta** — che sarebbe **una legge in piu'** *(`9-ter`)*.

### 📌 **IL SEGNALE ERA NEL MANDATO.** Luca aveva scritto *«CLAUDE.md e' a 391
righe su 400»*; io ho scritto **392** in sei messaggi e cinque commit **senza fermarmi
sulla differenza**. ### **Un numero che non coincide con quello di chi te l'ha dato non e'
un arrotondamento: e' un conteggio diverso.** *(Stessa forma di `P1`: un dato stabilito,
non confrontato col mio.)*

**IL FRONTE CHE RESTA, e non e' quel difetto:** se **altri** strumenti del repo contino
righe con una formula propria. ### ⚠ **NON LI HO CENSITI**, e il difetto e' per sua
natura **ripetibile**: ogni script che stampa *«N righe»* in un referto puo' averlo.

**PERCHE' CONTA:** un numero di righe compare nei referti e nei messaggi di commit, dove
**serve a decidere** *(il tetto, il «quanto e' cresciuto»)*. ### **Due convenzioni che
differiscono di uno producono numeri che NON SI POSSONO CONFRONTARE fra un referto e
l'altro** — ed e' **la stessa specie** del difetto dei **due hash** del par.2, dove la
cura fu *«quando si cita un blob si dice QUALE DELLE DUE»*.

### ✅ **IL CRITERIO DI CHIUSURA** *(una voce senza criterio e' un desiderio — par.4)*:
si chiude quando uno strumento ha **censito ogni punto del repo che conta righe di un
file** — e la ricerca e' **per FORMA, non per nome**: `count(NL)`, `splitlines()`,
`readlines()`, `wc -l`, `enumerate(open(...))` — e per ciascuno si e' detto **se usa
`_presidio_righe.conta`** o **se la sua convenzione e' DICHIARATA sul posto**.
### **Si chiude anche se il censimento trova ZERO altri punti:** il verdetto
*«nessun altro»* **e' un risultato**, purche' **misurato e non supposto** — oggi non
e' misurato, e per questo la voce e' **aperta**.

### ⛔ **E UNA SECONDA COSA, trovata dalla STESSA operazione, della stessa specie e
### GIA' CURATA.** Aggiungendo questa voce con un normale *leggi-testo, scrivi-testo*,
`git diff --numstat` ha detto **`3 aggiunte, 1 tolta`** dove ne aggiungevo **una**: il mio
write aveva **SPEZZATO UNA RIGA ESISTENTE**. ### **La causa: in 657 KB di `INDICE_ID.tsv`
c'era UN CR isolato**, e leggere con le *universal newlines* di Python lo trasforma in un
**fine-riga**.

### 📌 **E IL CR STAVA DENTRO LA FRASE CHE DESCRIVE L'INIEZIONE DI CR** *(la nota di
`H-NON-TRACCIATI`: «con l'uscita testuale su Windows si infila un … in ogni riga»)*:
### **dove volevo scrivere il NOME del carattere avevo scritto il CARATTERE.** La frase
sulla trappola **conteneva** la trappola.

**Curato:** i byte ripristinati con **`git cat-file -p` in binario** *(par.7: **non**
`git checkout`)*, il CR sostituito col suo **nome**, e la voce nuova aggiunta in
### **APPEND BINARIO**, verificando che i **657854 byte precedenti siano identici**.
### ⚠ **LA REGOLA OPERATIVA CHE NE ESCE: un TSV non si riscrive INTERO per aggiungere
una riga.** Si apre in `ab` e si appende — ### **cosi' un byte sporco altrove non puo'
diventare un danno.**

### ⛔ **IL PRECEDENTE DA NON RIFARE:** la cura giusta e' l'**import** della definizione
unica, **non** una seconda formula scritta bene. ### **Due formule corrette che vivono in
due file tornano a divergere alla prima modifica di una delle due.**

## `PIATTAFORMA-NON-TIMBRATA` — **i referti non dicono su che macchina sono nati**
*(aperto il 2026-10-04)*

I tre referti del 2026-10-01 dichiarano **`blob_sim_sha1_byte`** e **`blob_strumento`**, e
### **non dichiarano la piattaforma:** ne' `python`, ne' `numpy`, ne' il sistema.

**PERCHE' CONTA:** la stella polare documenta che i **conteggi assoluti** dipendono dalla
piattaforma — sulla stessa scena **`16/14/6/6`** su Linux/numpy 2.5.3 contro
**`14/12/4/4`** su Windows/numpy 2.3.0 — ### **mentre l'identita' prima/dopo no.**
Quindi davanti a uno **scarto** fra due referti **non si puo' separare** *«e' cambiato il
simulatore»* da *«e' cambiata la macchina»*, ### **e quella e' la prima cosa da
escludere.**

### ✅ **E IL CONFRONTO DEL 2026-10-04 NON NE HA SOFFERTO, il che va detto per non far
### passare la voce come urgente:** le due misure **dinamiche** sono risultate
**identiche** *(`3043` foglie su `3044` e `279` su `280`, e l'unica cambiata in ciascuna e'
il **timbro del blob stesso**)*. ### **Un limite che renderebbe ambiguo uno SCARTO non
rende ambigua un'IDENTITA'.** ### ⚠ **Ma la prossima volta che un conteggio cambia, il
limite morde.**

### ✅ **IL CRITERIO DI CHIUSURA:** si chiude quando **ogni** strumento che scrive un
referto `json` mette nel referto `python`, `numpy`, `sistema` e `macchina` — **e** quando
`csv/_presidio.py` offre **UNA** funzione che li produce, invece che ogni strumento se li
costruisca. ### **Due costruzioni corrette che vivono in due file tornano a divergere**, ed
e' appena successo col conteggio delle righe *(`CONTA-RIGHE`)*.

### ⛔ **E IL MODO SBAGLIATO DI CHIUDERLA, da non fare:** aggiungere il campo e
riempirlo con la piattaforma di **oggi** anche nei referti vecchi. ### **Sarebbe inventare
un dato che nessuno ha misurato** — e **i reperti non si riscrivono** *(par.9)*: si chiude
**sugli strumenti**, non sui referti gia' scritti.

## `VELENO-ORIENTATO` — **il veleno cade su UNO dei due archi figli, e quale dipende
dall'orientamento** *(aperto il 2026-10-04)*

**MISURATO**, non letto: confrontando `BASE` e `SCAMBIO` sui due archi figli di una
divisione — accoppiati **per insieme degli estremi** — tre grandezze danno elementi
**non finiti diversi**, e ### **i valori sono SCAMBIATI fra i due archi:**

| evento | grandezza | primo arco | secondo arco |
|---|---|---|---|
| divisione | `_sin2_vir` | BASE `0.0057085209267975336` / SCAMBIO `nan` | BASE `nan` / SCAMBIO `0.0057085209267975336` |
| schwinger | `_dt_e_ultimo` | BASE `0.0062105321832223361` / SCAMBIO `nan` | BASE `nan` / SCAMBIO `0.0062105321832223361` |
| schwinger | `_sin2_vir` | BASE `0.14077152702241497` / SCAMBIO `nan` | BASE `nan` / SCAMBIO `0.14077152702241497` |

### **Quindi uno dei due archi figli EREDITA un valore finito e l'altro riceve il
veleno, e QUALE DEI DUE dipende dall'orientamento `(i,j)` dell'arco genitore.**
### ⚠ **E' la stessa famiglia del difetto `(iii)` di `DIVISIONE-AUTOCONSISTENTE`:**
un'orientazione arbitraria che **decide** qualcosa.

### ✅ **E NON VA SOPRAVVALUTATA, e lo dico subito invece di lasciarlo scoprire:** il
simulatore **dichiara il veleno INERTE** per queste grandezze —
`memoria_hebbiana_moto` riscrive `_sin2_vir` **intera** nello stesso passo, **dopo**
`mitosi`, e `step` riscrive `_dt_e_ultimo`. ### **E' un'asimmetria della CONTABILITA' su
un valore sovrascritto prima di essere letto, non della dinamica.**

### 📌 **PERCHE' ALLORA APRIRLA:** perche' quell'inerzia e' una proprieta'
**dell'ORDINE DELLE VOCI di un passo**, non della legge. ### **Se un giorno una voce
leggesse `_sin2_vir` fra `mitosi` e `memoria_hebbiana_moto`, l'orientamento entrerebbe
nella dinamica senza che nessuno abbia toccato la nascita.**

### ✅ **IL CRITERIO DI CHIUSURA:** si chiude quando si e' detto, **per ciascuna** delle
tre grandezze, se il valore finito del primo arco figlio sia **VOLUTO** *(eredita dal
genitore `a`, come le altre 12 grandezze asimmetriche)* oppure un **RESIDUO dello shift
di `keep`** — cioe' se il veleno **non l'abbia coperto**.
### ⛔ **LA DIFFERENZA E' SOSTANZIALE:** nel primo caso e' una regola di nascita come le
altre, e la tratta la **legge**; nel secondo e' un **BUCO DEL VELENO**, e ### **il veleno
esiste proprio per non avere buchi.**

### 📌 **E COME SI DECIDE, con un sospetto preciso:** si legge `_avvelena_derivate` e si
guarda se avvelena **tutti** gli archi nuovi o **solo quelli con indice `>=` la lunghezza
vecchia**. ### **Quella seconda forma e' ESATTAMENTE la trappola dello shift di `keep`
che ha fatto sbagliare lo strumento di questa misura** *(gli archi nuovi NON sono quelli
con indice `>= A`, perche' `keep` ne toglie uno)*. ### **Se il veleno usasse quella
regola, il buco sarebbe della stessa forma.** **NON MISURATO, e non lo suppongo.**

## `VELENO-ARCHI-KEEP` — **il veleno allunga in coda e non applica `keep`**
*(aperto il 2026-10-05; `IN CORSO`, passo (1) = la misura)*

### **IL DIFETTO, letto dal codice e NON ancora misurato** *(il passo (1) lo misura)*

Alla nascita la mitosi ricostruisce le colonne d'arco con
**`i = concat(i[keep], a, m)`** *(`:1743`, e `:1750` per `j`)*: ### **toglie archi e ne
aggiunge in coda.** `_avvelena_derivate` *(`:1521`, chiamata a `:1707`)* allunga in coda
le derivate d'arco con `NaN` quando `len(v) < bersaglio`, e ### **NON applica `keep`** —
la parola non compare **mai** in quella funzione.
### ⛔ **Quindi, dopo il primo arco tolto, ogni arco legge il valore di UN ALTRO arco:
un valore FINITO, che il veleno non segnala.**

### ⚠ **E L'ORDINE E' DELIBERATO**, lo dice il commento del codice: il veleno sta
**dopo** le regole perche' deve conoscere le **lunghezze nuove**.
### **E' proprio questo a far mordere l'omissione.**

### 📌 **IL CONTO CHE RENDE IL DIFETTO SILENZIOSO**

Con `s` archi divisi: tolti `s`, aggiunti `2s`, quindi il veleno appende
`quanti = (m+s) - m = `**`s`** celle `NaN` — ### **mentre gli archi NUOVI sono `2s`.**
### **Il veleno copre META' degli archi nuovi, e l'altra meta' riceve un valore FINITO
preso da un arco vecchio.** ### **Un valore finito non fa scattare nessun controllo.**

**Le derivate d'arco con classe `avvelena` sono DUE**, censite dall'AST sul
`REGISTRO_DERIVATE` *(`:1300`)*: **`_dt_e_ultimo`** e **`_sin2_vir`**.

### ✅ **IL FATTO CHE SOSTIENE L'IPOTESI**, dal referto `eeb54be`: le `166` verifiche con
differenze sono **esattamente** quelle dei passi con **una nascita**, e la prima e' al
passo **`42`** — il passo della **prima divisione**.

### ✅ **IL CASO CHE DISCRIMINA, e viene gratis dalla stessa corsa:** la **divisione** usa
`keep`, lo **Schwinger NO** *(`concat(net.i, aa, k)`, `:2171`)*. ### **Negli eventi
Schwinger le differenze DEVONO essere ZERO** — e se comparissero, l'ipotesi e'
**sbagliata** e la cura **non si propone**.

### **LE DUE VIE, riportate SENZA sceglierne una** *(decisione di Luca dopo il referto)*

| | la via | il conto delle leggi |
|---|---|---|
| **`(i)`** | la nascita applica `keep` a **tutte** le derivate d'arco **prima** del veleno | ### **non aggiunge leggi: ne RIPARA una**, e per `9-ter` **toglie un'eccezione** — oggi le colonne d'arco si riallineano e le derivate no |
| **`(ii)`** | chi deve leggere `dt_e` dopo la mitosi lo **ricalcola** da `r` | ### **aggiunge una SECONDA SCRITTURA della stessa legge** — cio' che il simulatore dichiara di non voler fare, accanto a `_dt_e_ultimo` |

### ⚠ **E UNA COSA SUL SIGILLO:** *byte-identico sullo **STATO*** si puo' chiedere,
*byte-identico sulle **DERIVATE*** **no** — il `COMMIT 4` lo ha gia' dichiarato per se
stesso, e ### **una cura che riallinea le derivate le cambia PER DEFINIZIONE.**

### **PERCHE' RIENTRA NELL'ECCEZIONE AL CONGELAMENTO:** e' un difetto d'**infrastruttura**
che **falserebbe la cura di `TETTO-CAUSALE-TEMPO-COORDINATO` passo (2)**, la quale vuole
far leggere `dt_e` a `memoria_hebbiana_moto`.
### **E la voce sorella e' `VELENO-ORIENTATO`:** li' il veleno risultava cadere su **uno**
dei due archi figli e non sull'altro, e il criterio di chiusura chiedeva di decidere se
fosse **una regola** o **un buco del veleno**. ### **Questa voce e' la risposta a quella
domanda, se la misura confermera'.**

### **`blocca_run_base = NO`, e il perche':** oggi il difetto e' sui **valori di due
cache**, e se nessun lettore vivo le legge dopo la nascita **non muove la dinamica**.
### ⚠ **Ma blocca la CURA del tetto causale, ed e' per questo che viene prima.**

## `VELENO-ARCHI-KEEP` — **CHIUSA: il sigillo della cura, 2026-10-05**

> ### **La cura e' sigillata, e il numero e' `0`: le divergenze di STATO
> ### su 150 passi, 290 attributi per passo, confrontando
> ### `vars(net)` INTERO.**

**LA CURA, decisione di Luca del 2026-10-05, VIA (i):** la nascita applica `keep` a
**tutte** le derivate d'arco **prima** del veleno — `_riallinea_derivate_arco`,
chiamata immediatamente prima di `_avvelena_derivate`. Simulatore `0f060670` ->
**`e2940b3c`**. **La via `(ii)` e' stata scartata** *(curava un lettore solo, lasciava
`_sin2_vir` col difetto, e aggiungeva una seconda scrittura della legge di `dt_e`)*.

**GLI OTTO CRITERI, fissati prima del codice in `b17caec`, PASSANO TUTTI** — il
referto e' `doc/REFERTO_veleno_archi_keep_cura_2026-10-05.md`. I due numeri che contano:

| | prima | dopo |
|---|--:|--:|
| confronti di divisione **con differenze** | `166` su `166` | ### **`0`** |
| elementi diversi in totale | `63 802 623` | ### **`0`** |
| copertura del veleno *(min = max su 166)* | `0.5000` | ### **`1.0000`** |
| il tetto causale: verifiche (A) con differenze | `166` su `300` | ### **`0`** |

### ✅ **E QUESTA VOCE E' LA RISPOSTA ALLA DOMANDA DI `VELENO-ORIENTATO`:** li' il
veleno risultava cadere su **uno** dei due archi figli e non sull'altro, e il criterio di
chiusura chiedeva di decidere se fosse **una regola** o **un buco del veleno**.
### **Era un buco del veleno**, e la misura lo ha detto con `0.5000` esatto.

### ⛔ **E RESTA UNA CONSEGUENZA, registrata e NON decisa:** dopo la cura gli archi
**nati** nel passo hanno `dt_e = NaN` — prima avevano un valore **finito preso da un
altro arco**, che e' peggio ma **non si vedeva**. ### **Il passo (2) di
`TETTO-CAUSALE-TEMPO-COORDINATO` avra' bisogno di una REGOLA per loro, e quella e' una
DECISIONE DI LUCA da prendere ALLORA.**

## `SIGILLO-REGISTRO-NON-CONFRONTABILE` — **il comparatore del sigillo non sa
## confrontare un dizionario di array**

**IL FATTO, misurato:** `_veleno_registro` e' un **dizionario che contiene array**, e il
comparatore di `csv/_seal_fork/_sigillo_veleno_keep.py` lo classifica
**<<non confrontabile>>** in **`83` passi su 150**.

### ⚠ **E NON E' ESENTATO: il sigillo lo CONTA FRA LE DIFFERENZE**, perche'
### **un attributo non confrontabile non e' un attributo uguale.** La via dell'esenzione
era disponibile e non l'ho presa: lo stesso comparatore, lo stesso giorno, ha
**imparato** `_S` *(una `csr_matrix`)* e `rng` *(un `Generator`)* invece di esentarseli
*(`a5c2bfb`)*, e quei due avevano prodotto ### **un FALSO-UNO che mi avrebbe fatto
concludere che la cura era sbagliata.**

**PERCHE' NON FALSA IL RISULTATO:** e' classificato `contatore/registro` e **non**
`STATO`, e il criterio 1 del sigillo *(stato identico al byte)* da' `0`
comunque.

**CHE COSA MANCA:** insegnare al comparatore i **dizionari di array**, nello stesso modo
in cui gli si sono insegnate la matrice sparsa e il generatore.

**IN CODA** per il **congelamento dell'infrastruttura** *(decisione di Luca del
2026-10-04)*: i difetti degli strumenti che non falsano il risultato **si annotano e si
mettono in coda**.

## `SIGILLO-SENZA-CONFIGURAZIONE` — **il sigillo non TIMBRA la configurazione con cui
## ha girato**

**IL FATTO:** `csv/_seal_fork/_sigillo_veleno_keep.py` configura il modulo **passando
dal CLI del driver** *(`_cli_flag.argv_del_driver`, `:204`)* — quindi **non e'
configurato a mano** e `H-P3` e' rispettato — ### **ma non scrive la configurazione
nel suo json.**

**LA CONSEGUENZA, e l'ho dovuta dichiarare nel referto:** il referto ha dovuto
**RICOSTRUIRE** la dichiarazione di `P5` chiamando **lo stesso helper sullo stesso
driver**, *dopo* la corsa. Quella ricostruzione vale **solo** perche' il blob del driver
e' quello di `HEAD` *(`42ed4904`, non sporco)* — ### **verificato, e scritto nel
referto.** ### ⛔ **Se il driver fosse cambiato fra la corsa e il referto, la
ricostruzione MENTIREBBE.**

### ⚠ **E IL PRESIDIO NON LO PRENDE, per `A9`:** `H-P5` guarda i file sotto `csv/`
che **scrivono un referto** *(una `write` su un `DEST`/`REFERTO`)*, e questo sigillo
scrive un **json**. ### **I hook non impediscono cio' che non guardano.**

**CHE COSA MANCA:** il sigillo deve **timbrare** la sua configurazione nel json, come
fanno gli strumenti del tetto causale e del passo (1).

## `CELLE-NAN-APPESE-NOME-SCADUTO` — **un campo che misurava la cosa giusta solo
## finche' la cura non esisteva**

**IL FATTO, misurato rigirando lo strumento:** il campo `celle_nan_appese` di
`csv/_test_fork/_veleno_archi_keep.py` *(`425b8d47`)* e' calcolato come
`len_dopo - len_prima`, dove `len_prima` e' la lunghezza **prima delle regole di
nascita**. Quella quantita' coincideva con *<<quante celle appende il veleno>>*
### **solo finche' la cura non esisteva**: dopo la cura il veleno appende `2s` celle, ma
il campo continua a dire `s`.

| | sul VECCHIO `0f060670` | sul CURATO `e2940b3c` |
|---|---|---|
| `celle_nan_appese`, valori distinti | `1 … 32` | `1 … 32` — ### **invariato** |
| `non_finite_in_coda`, valori distinti | `1 … 32` | ### **`2 … 64`** |

**PERCHE' NON FALSA IL RISULTATO:** la misura del criterio 5 usa `non_finite_in_coda`,
che e' ### **LETTA DALL'ARRAY** e non dedotta dalle lunghezze, ed e' quella che da' `2s`.

> ### **E' UN NOME SCADUTO, NON UN NUMERO SBAGLIATO** — ed e' esattamente la classe
> di difetto che il par.2 di `CLAUDE.md` nomina: ### **i commenti, e i nomi, possono
> essere scaduti, e in questo repo lo sono stati.**

### ⛔ **E LO STRUMENTO `425b8d47` NON SI MODIFICA:** e' il blob con cui sono state
prese **le misure del passo (1)** e **i criteri 3-6 del sigillo**, e
### **un sigillo si rigira con `git checkout` del commit che ha sigillato** *(par.6)*.

## `FASE-TRASCINAMENTO-3D` — **la direzione trasversale privilegia l'asse `z` del
## LABORATORIO, e i nodi stanno in 3D**

> ### ⛔ **E' LEGGE NUOVA, NON UNA RIPARAZIONE** — il mandato di Luca lo dice con
> queste parole, ### **e per questo la legge NON si scrive adesso.**

*(Aperta il 2026-10-05 su **decisione di Luca del 2026-10-04**, col passo (1) di
`MEM-HEBB-VERSO`.)*

**IL FATTO, letto dal codice sul blob `e2940b3c`** *(`:9506`)*:

```python
dir_laterale = np.stack([-dir_radiale[:, 1], dir_radiale[:, 0],
                         np.zeros_like(dir_radiale[:, 0])], axis=1)
```

La direzione trasversale si costruisce ### **ruotando di 90 gradi NEL PIANO `xy`** e
### **azzerando la terza componente.** ### ⛔ **Questo privilegia l'asse `z` del
### laboratorio, che NON e' una grandezza del sistema:** i nodi stanno in **3D**
*(`:4940`, `u = self.rng.normal(size=(n, 3))`)*, e ### **nessuna legge del modello
distingue `z` da `x` o da `y`.**

**CHE COSA SERVE:** ### **un asse FISICO LOCALE al posto di `z`.**

### ⚠ **E UNA COSA CHE HO VERIFICATO INVECE DI SOSPETTARLA:** `dir_laterale` e'
### **SIMMETRICO per scambio `i<->j`** — nasce da `dir_radiale`, che **si inverte**, e
la rotazione e' **lineare**, quindi anche `dir_laterale` si inverte e il prodotto con
una grandezza d'arco e' invariante. ### **Quindi NON e' uno dei siti del verso: e' un
difetto DIVERSO**, ed e' per questo che ha una voce propria invece di stare dentro
`MEM-HEBB-VERSO`.

### 📌 **TRE DIFETTI NELLO STESSO SITO, TRE VOCI DISTINTE, perche' le cure sono
### diverse**

| difetto | dove vive |
|---|---|
| solo l'estremo `ii` riceve | `MEM-HEBB-VERSO` |
| `phi[ii] = ...` con indici ripetuti tiene l'**ultima** scrittura | `MEM-HEBB-VERSO` |
| `dir_laterale` privilegia l'asse `z` del laboratorio | ### **questa voce** |

**LA DECISIONE DI LUCA, non reinterpretata:** il sito ### **si SPEGNE con un flag
proprio**, e ### **`MEM_MOTO_TUTTO` e `MEM_MOTO` restano come sono.** Questa voce resta
**aperta** come difetto da curare con una **legge nuova**, ### **dopo.**

**I CRITERI DEL SIGILLO dello spegnimento** sono gia' fissati nel task history:

1. con il flag nuovo ### **ACCESO**: ### **identita' AL BYTE col blob di oggi**
   *(`e2940b3c`)* — e' il controllo che il flag e' **byte-inerte a default**;
2. con il flag ### **SPENTO**: ### **le differenze devono stare SOLO in `phi` e a
   valle.** ### ⚠ **Se una differenza comparisse altrove, lo spegnimento non e'
   recintato dove credo.**

## `SIGILLO-COMPARATORE-DUPLICATO` — **il comparatore del lockstep esiste in DUE
## COPIE, e la seconda l'ho fatta io**

*(Aperta il 2026-10-05 scrivendo il sigillo della cura (2) di `MEM-HEBB-VERSO`.)*

**IL FATTO:** il comparatore che confronta **due reti attributo per attributo** — quello
che sa confrontare una `csr_matrix`, un `Generator` e un **dizionario di array**, e che
### **CONTA fra le differenze cio' che non sa confrontare** — esiste ora in
### **DUE COPIE:**

| dove | blob |
|---|---|
| `csv/_seal_fork/_sigillo_veleno_keep.py` | `ee1df224` |
| `csv/_seal_fork/_sigillo_mem_fase.py` | `a5cb4c60` |

### ⛔ **PERCHE' E' UN DIFETTO: due copie possono divergere, ed e' la STESSA OBIEZIONE
### che `9-ter` fa alle leggi.** Se una delle due imparasse a confrontare un tipo nuovo e
l'altra no, ### **due sigilli darebbero verdetti diversi sugli stessi dati.**

### ⚠ **E NON E' UN RISCHIO TEORICO: IL PRIMO COMPARATORE HA GIA' DOVUTO IMPARARE.**
Il 2026-10-05, in `a5c2bfb`, ha imparato `csr_matrix` e `Generator` ### **dopo un
FALSO-UNO** che mi avrebbe fatto concludere che la cura di `VELENO-ARCHI-KEEP` era
sbagliata. ### **Quella lezione vive in UNA delle due copie per costruzione, e l'altra la
ha solo perche' l'ho copiata A MANO.**

**PERCHE' NON FALSA IL SIGILLO DI OGGI:** la copia e' stata fatta **ora** e le due sono
identiche nella sostanza. ### **Il difetto e' il RISCHIO FUTURO, non un errore presente.**

**CHE COSA MANCA:** estrarlo in un **modulo comune** sotto `csv/`, e farlo **importare**
dai due sigilli. ### ✅ **E L'HO DICHIARATO NEL COMMENTO DEL CODICE invece di
nasconderlo**, nel punto esatto in cui la copia comincia.

**IN CODA** per il **congelamento dell'infrastruttura** *(decisione di Luca del
2026-10-04)*: estrarre un modulo comune e' un **riordino**, e il congelamento lo vieta
salvo che un difetto falsi **la misura in corso** — e questo ### **non la falsa.**

### ⚠ **E UNA NOTA SU COME ANDRA' FATTA, perche' non e' un riordino gratuito:**
l'estrazione ### **andra' fatta CON UN SIGILLO**, perche' i due sigilli esistenti devono
restare ### **RI-GIRABILI ai loro commit** *(par.6: un sigillo si rigira con
`git checkout` del commit che ha sigillato)*. ### **E' una cura che tocca DUE STRUMENTI
DI CERTIFICAZIONE, e va fatta con la stessa cura di una legge.**

## `CS-LAMBDA-GLOBALE` — **`_cs_nodo` non e' del tutto locale: il PAVIMENTO legge una
## media su TUTTA la rete**

*(Aperta il 2026-10-05 su **decisione di Luca**, dal **fatto del guardiano**. ### ⛔ **E
da NON curare ora: si cura DOPO.**)*

### ✅ **VERIFICATO DALL'AST, e il numero e' UNO**

`_cs_nodo` *(`:7107-7160`)* contiene ### **esattamente UNA** riduzione su tutta la rete:

```
:7151   _Lam = float(np.mean(_I))        # _I = max(I[:n], 0.0)
```

| | |
|---|---|
| la **transizione** | `u_nodo = I / media dei VICINI` *(`W_loc @ I / W_loc @ 1`)* — ### ✅ **LOCALE** |
| il **pavimento** | `_scala = max(_Lam, 1e-30)/GAMMA_TURBO^2`, `cs_floor = CS_M/(1 + sqrt(_I)*sqrt(1/_scala))` — ### ⛔ **porta `_Lam`, GLOBALE** |

### ⛔ **QUINDI `cs` PORTA UN RIFERIMENTO GLOBALE**, e con la decisione `(2)` di `Z43`
*(`r = cs/CS_M`)* lo porterebbe ### **anche `r`.** E lo stesso termine tocca **gia'
oggi** il **tetto causale**, il **tempo-luce** e l'**orologio**.

## 📌 LA STORIA: **e' uno SCHEMA RICORRENTE, non un incidente**

`48d5ce2`, del **2026-09-16**: *«`cs_floor` RELAZIONALE cablato come CORREZIONE DI
DIFETTO (categoria D, NESSUN FLAG). Sigillo 16/16 PASS, R1 byte-identico»*.
Tolse la **densita' critica ASSOLUTA** *(`GAMMA = 0.05`, cioe' `400`)* e la sostitui'
con **`Lam`, l'energia del vuoto che il sistema CALCOLA da se'**.

> ### ⛔ **TOLSE UN NUMERO A MANO E INTRODUSSE UN RIFERIMENTO GLOBALE.**
> ### **E' LO STESSO SCAMBIO fatto per il gauge di `r`** — la mediana **globale** di
> `abs(f)`.
> ### ✅ **E nessuna delle due era sbagliata DA SOLA:** entrambe togliavano una
> ### **COSTANTE ARBITRARIA**, che e' il difetto peggiore *(`A1`: la legge, non il
> numero)*.
> ### 📌 **MA IL PREZZO E' LO STESSO OGNI VOLTA, e ora si vede: una legge LOCALE che
> ### legge una MEDIA GLOBALE non e' piu' locale.**

**LA CURA NATURALE**, nominata dal mandato: ### **un vuoto LOCALE per nodo** — la
proposta di Luca del **2026-10-02**, `VUOTO-LOCALE-DETERMINISTICO`.
### ⚠ **E richiede PRIMA un'energia definita** *(`ENERGIA-NON-DEFINITA`)*: ### **per
questo `blocca_run_base` e' `DA-DECIDERE` e non `NO` — non e' una cura che si possa
scegliere oggi.**

### 📌 **NB PER CHI LA CURERA': il termine globale NON e' un dettaglio del pavimento**

La **`PARTE B`** di `Z43` *(`r = cs_nodo_prev / CS_M`)* fa di `cs` la ### **DEFINIZIONE
del tempo proprio.** ### **Dopo quella cura `_Lam` entra nel TEMPO di ogni legge
locale.** ### ✅ **Ed e' per questo che il sigillo della `PARTE B` ha un criterio di
LOCALITA' che MISURA** di quanto cambia `r` di un nodo quando si perturba un nodo
**lontano**, con atteso ### **`~1/n` e NON zero.**

**Collegata a:** `INVARIANZA-LOCALE-CS`, `Z43`, `VUOTO-LOCALE-DETERMINISTICO`.

## `PHI-FUORI-DOMINIO` — **una delle dieci scritture di `phi` NON normalizza, e il
## sito della fase lo copriva PER CASO**

*(Aperta il 2026-10-05 dal sigillo di `MEM_FASE` — `fddb6a5`. ### ⛔ **Da NON cercare
ora: in coda DOPO `Z43`**, decisione di Luca.)*

### ✅ **IL FATTO, ed e' un numero**

Col flag `MEM_FASE` **spento**, al **passo 1**, l'unica differenza era `phi` — e il
**massimo scarto** era:

| | |
|---|--:|
| max scarto su `phi` | `1.256349e+01` |
| `4*pi`, cioe' `_dphi()` | `1.256637e+01` |
| ### **rapporto** | ### **`0.999770`** |
| mediana di `abs(shift)` *(referto `2717308`)* | `4.262912e-03` |
| ### **quante volte lo scarto e' piu' grande** | ### **`2947`** |

### ⛔ **LO SCARTO E' QUASI ESATTAMENTE `4pi`: E' IL MODULO, NON LO SHIFT.** Su almeno
un nodo l'effetto dominante del sito ### **non era il trascinamento di fase: era la
NORMALIZZAZIONE.** Quel nodo aveva `phi` ### **fuori dal dominio**, e il `% _dphi()` lo
riportava dentro ### **a ogni passo.**

### 📌 **CHE COSA NE SEGUE, e non e' un'ipotesi: e' aritmetica.** Se il sito della fase
era l'unica cosa che riportava `phi` nel dominio, allora ### **c'e' una scrittura di
`phi` che lo lascia uscire.** ### **Le scritture sono DIECI**, censite dall'AST nel task
history della cura (2) di `MEM-HEBB-VERSO`: `:1832` e `:2261` *(regole di nascita)*,
`:3888` *(`__init__`)*, `:4959` *(`semina`)*, `:7757` *(`step`)*, `:8739-8751`
*(`mitosi`, tre siti)*, `:9881` *(`_semina_masse_coerenti`)*, e il sito della fase.
### **QUALE LASCIA IL DOMINIO? Non lo so, e non l'ho cercato.**

### ⛔ **E IL FATTO CHE LA RENDE URGENTE SENZA RENDERLA PRIORITARIA**

> ### **La cura di `MEM_FASE` HA SPENTO quel `% _dphi()`** *(`7a03063`, default
> ### `MEM_FASE = False`)*.
> ### **Quindi da quel commit il buco NON e' piu' coperto**, e se `phi` esce dal dominio
> ### **ci resta.**
> ### ⚠ **Lo scrivo perche' e' il tipo di cosa che si scopre due mesi dopo come un
> ### <<difetto nuovo>>, e non lo sarebbe: sarebbe QUESTO, non cercato.**

### ⚠ **E UNA COSA CHE QUESTA VOCE NON DICE:** ### **non dice che sia un difetto
GRAVE.** `phi` fuori dal dominio puo' essere innocuo per le leggi che la leggono
*(molte usano `cos`, `sin` o `exp(i phi)`, che sono periodiche)*. ### **Dice che c'e' una
scrittura che non rispetta un'invariante che il resto del codice assume**, e che
### **finora era coperta da un sito che oggi e' spento.**

**Collegata a:** `MEM-HEBB-VERSO`, `FASE-TRASCINAMENTO-3D`.
---

## `RITMO-FLAG-SENZA-OGGETTO` — **due flag e due sigilli perdono il loro OGGETTO**

*(APERTA il 2026-10-05 dalla `CURA (2)` di `Z43`: `r = cs_nodo / CS_M`. **Non e' un difetto**,
e il tipo nell'indice e' `altro`: e' una **conseguenza misurata** di una cura, e la decisione
su che farne **e' di Luca**.)*

### IL FATTO, **censito dal sorgente e non supposto**

Dopo la cura `r` **non legge piu' la fase**. Cercando i lettori dei due flag **fuori** da
`ritmo()`, resta:

| flag | che cosa resta fuori da `ritmo()` | nella fisica |
|---|---|---|
| `RITMO_WRAP_2PI` | la dichiarazione *(`:3631`)*, la `global` e l'assegnazione dal CLI *(`:10923`)* | ### **NIENTE** |
| `TEMPO_PROPRIO_ORIENTATO` | gli stessi tre, **piu' un `print` d'avviso** *(`:11084`)* | ### **NIENTE** |

### **E NON SONO STATI TOLTI**, ed e' una scelta che dichiaro invece di nasconderla

**Toglierli sarebbe estendere la cura da soli** *(par.2)*. Il mandato nominava i rami che
escono, e **questi due flag non c'erano**. Restano **accettati dal CLI** e **inerti**, e
### **la loro sorte e' una decisione di Luca.**
**NB:** il driver **accende** `--ritmo-wrap-2pi`. Da oggi quell'accensione **non fa niente**,
ed e' scritto nel `README` perche' chi legge il comando non creda il contrario.

### ⚠ **E DUE SIGILLI PERDONO IL LORO OGGETTO. NESSUNO DEI DUE E' SBAGLIATO**

* **`csv/_seal_fork/_sigillo_ritmo_wrap.py`** — la cura **`D34`**, `4/4`, piu' la prova a 600
  passi `Z123`. **La sua misura resta vera:** un wrap su `4pi` applicato a una differenza di
  `np.angle` *(periodo `2pi`)* e' **l'identita'**, con `max|w4(a) - a| = 0.000e+00` su
  **100 001** punti. ### **Ma la legge che curava non c'e' piu'.**
* **`csv/_seal_fork/_sigillo_anello.py`** — asserisce *(`:201`-`:204`)* che `ritmo()` **non**
  scriva `_med_f_prec` e che `step()` **lo promuova**. ### **Da questa cura FALLISCE a `HEAD`,
  e DEVE:** la promozione e' uscita.

> ### 📌 **E QUESTO NON E' UN DIFETTO DI PAR.6**, e la distinzione conta: la regola dice che
> un sigillo ### **non piu' ri-girabile AL SUO COMMIT** e' un difetto nuovo. ### **Questi due
> si rigirano al loro commit senza cambiare una virgola.** ### **Un sigillo non si giudica su
> un codice che non ha sigillato.**

### **E DUE REGISTRI MORTI DELLA STESSA CURA**, da aprire come voce a parte

`_med_f_prec` e `_med_f_ultimo` restano **dichiarati a `None`** in `__init__` *(`A7b`)* e
### **da oggi nessuno li scrive**; `_psi_prec` resta **promosso** da `step()` e **non e' piu'
letto dalla fisica**.
**NON si tolgono in questa cura**, e il perche' e' concreto: `_med_f_*` sono letti da **due
strumenti di misura** — `csv/_test_fork/_f_e_median.py` e `csv/_test_fork/_z43_tempo_proprio.py`
— che leggerebbero **un attributo INESISTENTE invece di `None`**. ### **Ed e' lo stesso
criterio con cui `r_node` e' rimasto nella `CURA (1)`:** chi li togliesse **non starebbe
pulendo**, starebbe **cancellando la traccia di una legge che c'era**.

**Collegata a:** `Z43`, `CS-LAMBDA-GLOBALE`.

---

## `RELAZIONE-BINARIA` — **un NUL letterale rende la relazione binaria per git**

*(APERTA il 2026-10-05 scrivendo il referto della `PARTE B` di `Z43`. ### **Il difetto
PREESISTE a quel commit**, e l'ho trovato perche' `grep` ha risposto *<<Binary file
RELAZIONE_PER_CLAUDE.md matches>>* mentre controllavo una cosa d'altro.)*

### IL FATTO, **misurato**

`RELAZIONE_PER_CLAUDE.md` contiene **UN** byte `NUL` *(`0x00`)* all'offset **`294368`**,
**dentro una frase che spiega il formato dell'`oid` di git** -- *<<l'`oid` di git e' lo sha1
di `blob <len>`+`NUL`+`contenuto`>>* -- dove e' stato scritto ### **un `NUL` LETTERALE invece
del testo che lo rappresenta.**

### LA CONSEGUENZA, e non e' estetica

**git classifica il file come BINARIO.** Quindi:
* `git diff RELAZIONE_PER_CLAUDE.md` ### **non mostra le righe**, dice solo che il file e'
  cambiato;
* `grep` risponde *<<Binary file matches>>* invece delle righe.

### ⚠ **E questo e' il documento che chi legge il repo DA FUORI usa per primo** *(par.4: <<chi
legge il repo non ha la conversazione, ha solo i file>>)*. ### **Un suo diff illeggibile e'
un costo di REVISIONE**, non un dettaglio.

### CHE COSA **NON** ROMPE, e va detto per non gonfiarlo

* ### **non falsa nessuna misura:** nessun numero di nessun referto passa da qui;
* ### **`H-P1-bis` continua a funzionare:** git rileva comunque la modifica, quindi il
  presidio che pretende la relazione **non e' disarmato**.

### PERCHE' NON L'HO CURATA

**La cura sarebbe di UN byte** -- sostituire il `NUL` letterale col testo che lo rappresenta,
lasciando la frase **piu' corretta di prima**. ### **Non l'ho fatto perche' e' una modifica a
un paragrafo STORICO, fuori dal mandato in corso** *(congelamento dell'infrastruttura del
2026-10-04: i difetti degli strumenti che non falsano il risultato si **annotano** e si
mettono **in coda**)*.

### DA VERIFICARE SE SI DECIDE DI CURARLA

1. che **nessun altro documento** abbia lo stesso problema;
2. che quel byte **non sia citato** da un presidio o da un sigillo come parte di una misura
   sull'identita' dei blob — ### **la frase in cui vive parla ESATTAMENTE di quello**, ed e'
   la ragione per cui non l'ho toccata di mia iniziativa.

**Collegata a:** `Z43` *(l'ho trovata lavorandoci)*.

---

## `GRAVITA-POTENZIALE` — **due potenziali nel codice, e Poisson e' un VINCOLO DI SCALA**

*(APERTA il 2026-10-05 per **decisione di Luca**, **da curare DOPO**. ### **Direzione
discussa, NON decisa.**)*

### I DUE POTENZIALI, **verificati dal sorgente** sul blob `f7237563`

| | dove | la forma | chi lo usa | la coda |
|---|---|---|---|---|
| **1** | `pozzo_grafo` *(`:9058`)* | `np.add.at(phi_g, ii, I[jj]/L)`, simmetrico su `jj`: la somma di `I/L` sui **SOLI VICINI DIRETTI** del grafo | la **FORZA** di `GRAV_BIFASE` | ### **NESSUNA** |
| **2** | il blocco Kuramoto *(`K_SYNC`, `:7705`-`:7727`)* | `cmv` = centro di massa pesato da `I2`; `r_cm = |pos - cmv| + LAM*0.5`; `pozzo = I2.sum()/r_cm` | **SOLO le FASI** | ### **`M/d` GLOBALE**, con addolcimento |

### ✔ **E UNA PRECISAZIONE CHE IL SORGENTE AGGIUNGE, e cambia il peso del fatto (2):**
quel pozzo entra nella legge **solo** attraverso `prof_rel = pozzo / media_p`, un
### **RAPPORTO LOCALE** sui vicini topologici. ### **Quindi la coda `M/d` viene in gran parte
NORMALIZZATA VIA prima di diventare forza:** il potenziale globale **c'e'**, ma il suo
**gradiente a lungo raggio** no.

### ⛔ **DOVE E' POISSON NEL SISTEMA** — e Luca ricorda di averlo gia' messo: ### **non come
### equazione risolta**

Le **cinque** occorrenze della parola nel simulatore sono **due cose sole**:

1. ### **LA FORMA DI PROBABILITA' DELLA MITOSI** *(`:8448`, `:11565`)*: `1 - exp(-lambda)`.
   E' un **processo** di Poisson, ### **non l'equazione** di Poisson.
2. ### **UN VINCOLO DI SCALA DEL COARSE-GRAINING** *(`:331`-`:336` e `:6238`-`:6240`)*: le
   regole di scala di `SCALA_B` sono state **derivate imponendo la conservazione di tre
   leggi al continuo**, e ### **Poisson e' una delle tre** --
   *«`massa/solitone = SCALA_B * massa_fine` (ogni blocco pesa `SCALA_B` fini: **preserva
   Poisson**)»*, perche' *«la sorgente e' `rho = |Psi|^2`»*.

> ### ✔ **QUINDI: Poisson entra come VINCOLO SU COME SI CAMBIA SCALA, non come legge
> ### risolta sul grafo.** ### ⚠ **E oggi e' INERTE: `SCALA_B = 1.0`**, quindi quelle
> regole di scala sono **l'identita'**. ### **Questa e' la risposta al <<da chiarire
> dove>>, e va riletta da qui prima di cercarlo altrove.**

### CHE COSA CAMBIA CON `r = cs/CS_M`

Il tempo proprio segue la **densita' LOCALE**: ### **niente coda `M/d` fuori dalle masse**, e
e' previsto un **alone di orologi piu' VELOCI al bordo** *(`u < 1`, dove la transizione di
`_cs_nodo` sale verso `0.880797`)*.
### ✔ **E il criterio `5` del sigillo della `PARTE B` lo ha MISURATO:** oltre due salti il
cambiamento relativo di `cs` e' un **pavimento piatto** a `0.40`-`0.51` volte `1/n` che
**non decade con la distanza** -- cioe' ### **una coda GLOBALE di ampiezza `1/n`, non una
coda `1/d`.**

### LA DIREZIONE, **discussa e NON decisa**

Un potenziale ### **PROPAGATO sul grafo a velocita' `cs`** *(limite statico Poisson, coda
`1/d`)* che entri ### **nella FORZA e in `cs`**.

**Collegata a:** `Z43`, `CS-LAMBDA-GLOBALE`, `TETTO-CAUSALE-TEMPO-COORDINATO`, `Z47`.

---

## `CRESCITA-DOPO-Z43` — **con `r = cs/CS_M` la rete quasi non cresce piu'**

*(APERTA il 2026-10-05 dal mandato di Luca, dopo il sigillo della `PARTE B` di `Z43`
*(`9731201`)*. La misura e' in
`doc/TASK_HISTORY/2026-10-05_crescita-dopo-z43-misura.md`.)*

### IL FATTO, **misurato su due piattaforme**

Dal criterio `7` del referto `9731201` e da una misura **indipendente** del guardiano su
Linux: al passo `150`, `n = 12827` nella `PARTE B` contro **`14328`** nella `PARTE A`, da una
partenza di `12802`. Cioe' ### **~25 nascite contro ~1500**, e nella `PARTE B` concentrate in
**13 passi su 150**.

### ⚠ **E IL RALLENTAMENTO UNIFORME NON LO SPIEGA**

`r` mediano e' `0.815126`, e il fattore di tempo entra nella probabilita' **UNA volta sola**
*(`ampiezza = ampiezza_int * dt_e/DT`)*: gli eventi attesi scalano di **`~0.815`**.
### **Un fattore `0.815` non fa un fattore `~60`.**

### L'IPOTESI DEL GUARDIANO — **da verificare, non da assumere**

```
grad_modula = |r[i] - r[j]|
soglia      = soglia0 * (1.0 - 0.3 * tanh(grad_modula))
```

Con l'altalena, `r` spaziava su `[1.4142e-06, 1.4142]`: il gradiente fra vicini era
**enorme**, `tanh -> ~0.888`, e la soglia **crollava** fino a `~0.73 * soglia0`. Con `r`
liscio il gradiente e' piccolo e la soglia **resta `soglia0`**.
### ⛔ **Se e' cosi', gran parte della crescita misurata finora era alimentata
### DALL'ARTEFATTO DELL'OROLOGIO.**

### ✔ **E UNA TERZA CAUSA POSSIBILE CHE IL MANDATO NON NOMINA, registrata qui**

`avv = |tw|` ### **non e' un dato esterno:** la torsione si integra in `dt_e`, cioe' **nel
tempo proprio**. Con `r` diverso, ### **`|tw|` al passo `k` E' UNA GRANDEZZA DIVERSA.** I
bracci potrebbero separarsi **non perche' la soglia e' piu' alta, ma perche' `avv` e' piu'
bassa** — e il censimento dei cancelli **da solo non distingue i due casi**: li distingue il
confronto fra la **distribuzione di `avv`** e quella di **`soglia`**.

### ⚠ **E UN LIMITE DEL CONTROFATTUALE, dichiarato PRIMA di girarlo**

Riscalare `r` per `1/mediana(r) ~ 1.227` moltiplica **anche** `|r_i - r_j|` per `1.227`:
### **i gradienti NON restano intatti, crescono del 23 %.** Questo rende la conclusione
*<<non e' il rallentamento>>* ### **piu' forte, non piu' debole** — ma se le nascite
**risalissero**, quel `23 %` sarebbe una **causa confondente** da dichiarare.

> ### ⛔ **SOLO NUMERI: la crescita e la soglia di mitosi sono DECISIONI DI LUCA.**

**Collegata a:** `Z43`, `MITOSI-SOGLIA-GRAD`, `Z47`.

---

## `ARCHI-OLTRE-4PI` — **~109 archi oltre il tetto dal passo `2`, e non rilassano**

*(APERTA il 2026-10-05 da una **verifica del guardiano** sui dati di `CRESCITA-DOPO-Z43`.
### ⛔ **DA NON INDAGARE ORA** — decisione di Luca.)*

### IL FATTO, e **e' un'identita', non una stima**

Nel censimento dei cancelli di `decidi_divisione`, gli archi che passano il cancello `1`
*(`avv > soglia`)* e **non** il cancello `2` *(`avv < 4pi`)* sono ### **esattamente quelli
con `|tw| >= 4pi`.**

**Contati per passo:** ### **ZERO al passo `1`, `109` AL PASSO `2`**, e da li' una
popolazione **quasi costante** per tutta la corsa *(mediana per passo `~105`, massimo
`110`)*.

| braccio | passi-arco oltre `4pi` | frazione di `Sum g1` |
|---|--:|--:|
| `Ap` *(la `PARTE A`)* | `~14981` | `~10 %` |
| `Bp` *(la `PARTE B`)* | `~14338` | `~62 %` |
| `Bc` *(il controfattuale)* | `~14153` | `~45 %` |

> ### ✔ **E I PESI SONO QUASI UGUALI NEI TRE BRACCI: QUINDI NON DIPENDONO DALLA LEGGE DEL
> ### TEMPO PROPRIO.** Ci sono con `r` dalla fase e con `r = cs/CS_M` **allo stesso modo**.
> ### **Le frazioni diversissime vengono dal DENOMINATORE** *(`Sum g1` e' molto piu' piccolo
> nella `PARTE B`)*, **non dalla popolazione.**

### PERCHE' E' UN DIFETTO

Il cancello `2` esiste per ### **SPEGNERE la mitosi verso il tetto** *(omeostasi: la campana
si azzera a `4pi`)*. Un arco che **nasce** oltre il tetto e **non rilassa** e' un arco
**permanentemente nel regime di spegnimento** — cioe' ### **una legge di omeostasi che su
quella popolazione non ha niente da regolare.**

### E FALSA UN SALTO DEL CENSIMENTO, ed e' per questo che e' stata trovata

Il salto `x0.425` che avevo attribuito al cancello `2` e' ### **INTERAMENTE la diluizione di
questa popolazione fissa:** il salto **NETTO** del cancello `2`, togliendola, vale
### **`1.0000` in entrambi i bracci.** ### **Il cancello `2` non e' un canale.**

### ⛔ NON INDAGATA, e lo dico: **non so da dove vengano, ne' perche' non rilassino**

**DUE STRADE DA GUARDARE**, scritte per chi la prendera' e ### **non verificate:**
1. la **scena iniziale `MASSE-COERENTI`** potrebbe costruire archi che arrivano oltre `4pi`
   al primo passo di dinamica — ### **la popolazione e' zero al passo `1` e `109` al passo
   `2`, quindi nasce nel PRIMO passo di evoluzione e non dalla semina**;
2. il **wrapping della torsione**: `TORS_4PI` mette `tw` sul dominio doppio e
   `TW_TETTO = 4pi` ne e' l'estremo, quindi un arco che arriva **al bordo** potrebbe non
   avere nessuna legge che lo riporti dentro.

**IL MODO PIU' DIRETTO DI CERCARLA:** un controllo d'invariante su `|tw|` a fine passo **con
gli INDICI** degli archi che superano `4pi`, girato per i **primi tre** passi.
### **Se sono sempre gli stessi `109` indici e' una popolazione FISSA; se cambiano e' un
FLUSSO**, e sono due difetti diversi.

**Collegata a:** `CRESCITA-DOPO-Z43`, `MITOSI-SOGLIA-GRAD`, `Z43`.


---

## `KAPPA-TW-COMMENTO` — **il commento dice `kappa = 3.1831`, il codice restituisce `1`**

*(Aperta il 2026-10-06 da una lettura del codice fatta per la misura del **tetto della
torsione**: e' la verifica **(a)** delle tre che il mandato chiede ### **prima** del task
history. ### **Il simulatore non e' stato toccato:** `f7237563`.)*

### IL FATTO, **dal sorgente e non dal commento**

`_tau_tw_locale` *(`:584`)* porta **due** affermazioni su `kappa_tw`:

| dove | che cosa dice |
|---|---|
| il **docstring** | *«`kappa_tw = TAU_TW/(2pi)` resta come rapporto `O(1)`»* |
| il **commento nel corpo** | *«`tau_tw = kappa_tw * 2pi/|dw|`, con `kappa_tw = TAU_TW/(2pi)` rapporto `O(1)`»* |
| ### **la riga che GIRA** | `return np.maximum((2*np.pi) / dom, 1e-3)` — ### ⛔ **senza NESSUN fattore `TAU_TW`** |
| il commento **di quella riga** | *«`kappa=1: tau_tw = 2pi/|dw_locale|`»* |

### ⛔ **I DUE COMMENTI DELLA STESSA FUNZIONE SI CONTRADDICONO FRA LORO.** Con
`TAU_TW = 20.0` *(`:583`)* il docstring implica `kappa_tw` = `20/(2pi)` = **`3.1831`**;
### **il codice da' `kappa = 1` ESATTAMENTE.**

### PERCHE' E' UN DIFETTO E NON UNA SVISTA

`tau_tw` e' il **tempo di scarica** della torsione, quindi `kappa` entra **direttamente** nel
tetto di equilibrio

```
tw* = kappa * 2pi * (r_i*w_i - r_j*w_j) / ( r_medio * (|w_i - w_j| + 1e-3) )
```

| con | il tetto | e la soglia di mitosi `3pi` ... |
|---|--:|---|
| `kappa = 1` *(il codice)* | **`2pi`** | ### e' **IRRAGGIUNGIBILE** in equilibrio: la mitosi e' **marginale per costruzione** |
| `kappa = 3.1831` *(il commento)* | **`20`** | sarebbe **tre volte** la soglia: la mitosi sarebbe ### **generica** |

> ### ⛔ **LE DUE LETTURE DANNO FISICHE OPPOSTE**, e un commento non e' una fonte: in questo
> repo i commenti ### **sono stati scaduti**, e `CLAUDE.md` par.2 lo dice come regola.

### ⚠ **E `TAU_TW = 20.0` NON E' MORTA**

La usa il ramo **non locale** *(`TAU_LOCALI = False`)*. ### **Quindi la costante non si puo'
togliere:** si puo' correggere il commento, oppure **derivare** `kappa`.

### ⛔ **NON CURATA: `kappa` E' UNA DECISIONE DI LUCA**

Il mandato del tetto lo dice: *«`kappa`, la soglia, il dipolo locale e il `0.3` sono decisioni
sue»*. **LE TRE STRADE**, scritte per chi la prendera' e ### **non verificate**:

1. **il commento e' sbagliato** e `kappa = 1` e' la legge ⟹ si corregge il commento e si
   dichiara che ### **`kappa = 1` e' UN NUMERO SCRITTO A MANO** *(`A1`)*;
2. **il commento e' giusto** e il codice ha perso il fattore ⟹ ### **il tetto e' `3.1831`
   volte piu' alto e OGNI lettura fatta finora sulla torsione va rifatta**;
3. ### **`kappa` va DERIVATO e non scelto**, che e' cio' che `A1` chiede.

> ### 📌 **E LA (2) NON SI DECIDE DAL COMMENTO:** si decide da ### **`git log` sulla riga del
> `return`** -- `STANDARD 9` dice che `git log` e' parte del repo e va cercato anche lui.

### ⛔ **ANNOTAZIONE DEL 2026-10-06 — IL TERZO CONSUMATORE, che questo documento
### non dichiarava**

*(Rilievo del guardiano, ### **confermato da me sul sorgente committato.** Il testo qui sopra
### **non si riscrive:** diceva *«la usa il ramo NON locale»*, ed e' **incompleto**.)*

`TAU_TW` entra in gioco per ### **TRE vie, non due**:

| | dove |
|--:|---|
| **1** | il ramo **non locale** *(`TAU_LOCALI = False`)* |
| **2** | il **docstring**, che dice `kappa_tw = TAU_TW/(2pi)` = `3.1831` mentre il codice da' `kappa = 1` |
| ### **3** | ### **`_tau_tw_locale` STESSA, a `:591`:** `return TAU_TW` nel proprio ramo di guardia, `if len(net.phivel) < net.n or len(i) == 0` |

### ⛔ **E LA TERZA E' LA PIU' INSIDIOSA:** se scattasse, `tau_tw` passerebbe da ### **`~2`-`6`**
*(misurato: mediana `2.4055` al passo `50`, `1.9738` al passo `140`)* a ### **`20`** -- un
fattore `3`-`10` sul tetto di equilibrio -- ### **e nessun contatore lo conta.**
### **E' un fallback NON MISURATO, la classe di `P5` e `A8`: un ramo silenzioso non e' un
ramo.** La misura del tetto *(`eebe24f`)* ### **non l'ha censito.**

> ### 📌 **DECISIONE DI LUCA, presa:** il contatore `A8` *(invocazioni, salti, forma,
> quando)* entra ### **nella cura di `TORS-W8-AVVOLGIMENTO`**, byte-inerte, e il suo numero
> va ### **nella misura finale.**

**Collegata a** `SCALE-TW` *(che chiede l'analisi completa delle scale della torsione, e di
cui questa e' **un pezzo**)*, `ARCHI-OLTRE-4PI`, `CENS-B4`, `MITOSI-SOGLIA-GRAD`.


---

## `TORS-W8-AVVOLGIMENTO` — **`_w8` ha periodo `8π`, l'avvolgimento di `dph` e' di `4π`**

*(Aperta il 2026-10-06 da una **derivazione verificata con uno script**, fatta per la misura
del **tetto della torsione**: e' la verifica **(b)** delle tre che il mandato chiede
### **prima** del task history. ### **Il simulatore non e' stato toccato:** `f7237563`.)*

### IL FATTO — **un'identita', non una statistica**

La spinta della torsione nel ramo `TORS_4PI` *(`:7795`)* e'

```
self.tw += self._w8(dph + twist_dip - self.twp) - dt_e * self.tw / _ttw
self.twp  = self._w8(dph + twist_dip)
```

Con `FASE_2PI = False` *(`:3543`)*, `dph = _wphi(phi_i - phi_j)` vive su un periodo di
### **`4π`**: quando la differenza di fase gira, ### **`dph` SALTA DI `-4π`.**
### ⛔ **E `_w8` ha periodo `8π`: un salto di `4π` NON e' un multiplo del suo periodo,
### quindi NON lo ripara.**

### MISURATO, su un caso sintetico con incremento vero `delta = 0.013`

| ramo | che cosa restituisce | errore |
|---|--:|--:|
| **`TORS_4PI`** *(quello che **gira**)*, `_w8` | `-12.553371` | ### ⛔ **`-12.566371`, cioe' `-4π` ESATTI** |
| **non-`4π`** *(`TORS_4PI = False`)*, `_w4` + `twp = dph` | `+0.013000` | ### ✔ **`-1.9e-15`** |

> ### ⛔ **QUINDI IL RAMO CHE GIRA NELLA SCENA HA UN DIFETTO CHE L'ALTRO NON HA**, e il motivo
> e' **strutturale**: ### **un avvolgimento di `4π` e' INVISIBILE a un modulo di periodo
> `4π` e VISIBILE a uno di periodo `8π`.**

### ⚠ **PERCHE' `_w8` C'E', e non e' un errore gratuito**

Serve a far vivere `dph + twist_dip` su `±3π` ### **senza avvolgerlo** *(`twist_dip` arriva a
`±π`)*, e quello ### **lo ottiene** -- la derivazione sta nel task history del tetto:
`|dph + twist_dip| <= 3π < 4π`, quindi ### **`twp` non avvolge MAI.**
### **Il costo e' la perdita della riparazione.**

### ⛔ **NON CURATA, e la cura NON E' UNA SCELTA FRA `_w4` E `_w8`**

Si possono avere ### **entrambe** le cose: avvolgere con periodo `4π` la **differenza di
`dph`** e sommare la differenza di `twist_dip` **non avvolta**, cioe'

```
_w4(dph - dph_prec)  +  (twist_dip - twist_dip_prec)
```

### ⚠ **NON L'HO VERIFICATA, e non la applico:** toccare la legge della torsione e'
### **una decisione di Luca**, e il mandato del tetto lo dice.

### ⚠ **PERCHE' PUO' CONTARE MOLTO, e perche' NON lo dichiaro dimostrato**

Un calcio di `-4π` porta un arco ### **oltre `TW_TETTO = 4π` in un passo solo**, ed e'
### **esattamente il sintomo di `ARCHI-OLTRE-4PI`** *(`~109` archi sopra `4π` dal passo `2`,
che non rilassano, e la cui **seconda strada** ipotizzata era ### **proprio il wrapping della
torsione**)*.

> ### ⛔ **MA `ARCHI-OLTRE-4PI` E' <<DA NON INDAGARE>> PER DECISIONE DI LUCA.** Quindi riporto
> il ### **meccanismo** e il ### **puntatore**, e ### **NON faccio la verifica che li
> collegherebbe.** ### **Quanto succeda davvero lo misura `M6`** della misura del tetto.

**Collegata a** `SCALE-TW` *(di cui e' un pezzo)*, `ARCHI-OLTRE-4PI`, `KAPPA-TW-COMMENTO`,
`MITOSI-SOGLIA-GRAD`.


---

## `PRESTAZIONI-CORSE` — **le corse costano: sei strade, da affrontare a modello STABILE**

*(Aperta il 2026-10-06 ### **su decisione di Luca**, e ### ⛔ **IN CODA, NON ADESSO.**)*

### ⛔ **PERCHE' NON ADESSO, e non e' prudenza**

### **Ottimizzare un modello che sta cambiando legge significa ottimizzare codice che non ci
sara'.** La cura di `TORS-W8-AVVOLGIMENTO` ha appena sostituito il blocco della torsione;
`κ`, la soglia `3π` e il `0.3` sono ### **decisioni aperte di Luca.**
### **Si tocca il tempo di calcolo quando la fisica sta ferma.**

### IL FATTO CHE LA MOTIVA

Le misure sono passate da `150` a ### **`1000` passi** *(la misura lunga di questa stessa
cura)*, e una corsa a **quattro bracci** su `150` passi costa ### **circa un'ora e mezza** su
questa macchina. ### **Non e' un fastidio: e' il motivo per cui una domanda in piu' costa una
giornata.**

### LE SEI STRADE, **nell'ordine in cui Luca le ha date e NON in ordine di merito**

| | la strada | il vincolo che porta con se' |
|---|---|---|
| **(a)** | ### **PROFILARE i tempi per legge PRIMA di ottimizzare** | ### ✔ **E' gia' il criterio di chiusura di `RISCRITTURA-GO`**, che dice *«il profilo NON ESISTE»*: farla serve a **entrambe** |
| **(b)** | partire da uno **stato gia' stabilizzato** | ### ⛔ **`carica_stato` RIFIUTA uno stato di un blob diverso** *(`raise RuntimeError` a `:7054`, **prima** del ciclo sugli attributi)*: ### **ogni cura invalida gli stati salvati**, ed e' una protezione, non un intralcio |
| **(c)** | **bracci e semi in processi separati**, sui core della macchina | e' la via senza costi di correttezza: ### **`STANDARD 1` la pretende GIA'** *(un processo per braccio)* |
| **(d)** | una **scena piu' piccola** per le domande esplorative | ### ⚠ **`TAGLIA-FINITA` dice che due taglie non sono uno scaling:** la verifica *«i risultati non dipendono dalla taglia»* va fatta **una volta** e ### **va fatta bene**, altrimenti e' una scorciatoia travestita |
| **(e)** | **accelerare il calcolo** *(Numba, GPU)*, con **due** modalita' | ### ⛔ **ESATTA per sigilli e cure, VELOCE con tolleranza DICHIARATA per l'esplorazione.** Una tolleranza **non dichiarata** e' il modo in cui un sigillo diventa una formalita' |
| **(f)** | chiedersi se **il passo di tempo si puo' allungare**, col contatore `CFL` | il contatore c'e' gia': ### **la domanda e' se `DT` e' stretto per una ragione o per abitudine** |

### ⚠ **E UNA FRASE DI `RISCRITTURA-GO` VA RIMISURATA, non ricopiata**

Quella voce dice *«la velocita' non e' il collo di bottiglia: nessuno dei `6` SI e' il
simulatore lento»*. ### **E' del 2026-09-27, quando le misure erano a `120`-`150` passi.**
### ⛔ **Oggi una misura e' a `1000` passi, e quella frase va RIMISURATA prima di riusarla.**

### ⛔ **NON INDAGATA, NON INIZIATA.** Collegata a ### **`RISCRITTURA-GO`**, e il
collegamento non e' decorativo: ### **la strada `(a)` e' il criterio di chiusura di quella
voce, quindi non si aprono due lavori.**
