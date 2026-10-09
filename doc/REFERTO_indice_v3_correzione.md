# IL REFERTO DELLA CORREZIONE `v3` — **dopo la verifica del guardiano**

> ### ⛔ **Il guardiano ha letto le voci una per una e ha trovato che ### LE SUE PROPRIE LISTE erano sbagliate.** Questa e' la correzione, e il mandato lo dice: *«Le liste del guardiano si aggiornano ### **DI CONSEGUENZA** (questa e' una correzione chiesta)»*. ### **Non e' un mio disaccordo.**

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **i commit** | `3ad58a2` *(blocchi `A`+`B`)* · `9e2340e` *(`C`)* · `85b5313` *(`D`)*, piu' questo |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa in tutto il giro |
| **le voci toccate** | ### **`64`** *(`22` nel blocco `A`, `26` nel `B`, `16` nel `C`)*, piu' `1` difetto nuovo |
| **le righe di storico** | `982` → ### **`1079`**, e ciascuna porta ### **un motivo che CITA il testo** |

---

## ① I CONTEGGI, PRIMA E DOPO

> **PRIMA** = `git show 6e5e75b:doc/indice/voci.jsonl`. **DOPO** = il disco. ### **Nessun numero ricopiato.**

| `dominio` | prima | dopo | |
|---|--:|--:|---|
| FISICA | `454` | `439` | ### **-15** |
| DA_CLASSIFICARE | `179` | `181` | ### **+2** |
| METODO | `114` | `136` | ### **+22** |
| INFRASTRUTTURA | `43` | `47` | ### **+4** |
| DOCUMENTAZIONE | `23` | `27` | ### **+4** |

| `era` | prima | dopo | |
|---|--:|--:|---|
| 1 | `424` | `445` | ### **+21** |
| DA_CLASSIFICARE | `181` | `182` | ### **+1** |
| ENTRAMBE | `165` | `177` | ### **+12** |
| 2 | `43` | `26` | ### **-17** |

| `stato` | prima | dopo | |
|---|--:|--:|---|
| SOSPESA | `246` | `274` | ### **+28** |
| CHIUSA | `187` | `187` |  |
| DA_CLASSIFICARE | `181` | `182` | ### **+1** |
| APERTA | `156` | `161` | ### **+5** |
| AGENDA | `43` | `26` | ### **-17** |

| `classe` | prima | dopo | |
|---|--:|--:|---|
| DIFETTO | `209` | `210` | ### **+1** |
| NON_DEFINITA | `179` | `181` | ### **+2** |
| FRONTE | `168` | `169` | ### **+1** |
| CRITERIO | `95` | `107` | ### **+12** |
| MISURA | `54` | `55` | ### **+1** |
| CURA | `46` | `46` |  |
| PRESIDIO | `34` | `34` |  |
| STANDARD | `28` | `28` |  |

| | prima | dopo |
|---|--:|--:|
| voci | `813` | ### **`830`** |
| etichette rimosse | `138` | ### **`122`** |
| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |

---

## ② BLOCCO `A` — **la lista `2` del guardiano era un ERRORE SUO**

La lista `2` dava queste voci come ### **lavoro dell'era `2`** *(la riscrittura)*. Leggendole, ### **sono DIFETTI DEL CODICE DELL'ERA `1`**: la loro lezione passa all'era `2`, ### **ma la voce appartiene all'era `1`.**

| id | prima | dopo | il testo che lo dice |
|---|---|---|---|
| `CARICA-ROTAZIONE` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | REGISTRATA il 2026-10-02 dalla REVISIONE DELLA VISIONE di Luca del 2026-10-01 sera, e NON DA FARE OGGI. LA MIS |
| `CARICA-SIMMETRIA-FASE` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | APERTA il 2026-10-03, DECISIONE DI LUCA, ed e LA PRIMA MISURA DEL FILONE DELLA CARICA -- si puo fare anche PRI |
| `CARICA-DI-GAUGE` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | MISURATO il 2026-10-01 su TRE run (seme 11/72, seme 12/72, seme 11/150). perc_chi viene riscritta a ogni passo |
| `CARICA-PERCORSO` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | APERTA il 2026-10-03, DECISIONE DI LUCA: non e un difetto nuovo, e L ORDINE in cui si chiudono le voci della c |
| `D03` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: La memoria del moto prende le direzioni da pos, normalizza su Imed GLOBALE, e ha un tetto |
| `D15` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | A7: la carica chirale NON si conserva / Z71, letto dal codice / — / APERTO |
| `D35` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: L'antiparticella di Schwinger nasce con +2π (:5443) e nel campo F = Σ exp(iφ) E' IDENTICA |
| `D38` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: nasce (:3850) e' gated su SCALAMIN or SCALAMINPASSO: la legge «nessun arco sotto LAM» e'  |
| `FASE-TRASCINAMENTO-3D` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | APERTA il 2026-10-05 su DECISIONE DI LUCA del 2026-10-04, col passo (1) di MEM-HEBB-VERSO. E LEGGE NUOVA, NON  |
| `MEM-HEBB-PIANO-XY` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | NOTATO il 2026-10-01 mentre cercavo i siti di MEM-HEBB-VERSO: dir_laterale = np.stack([-dir_radiale[:,1], dir_ |
| `SCHW-SOTTO-LAM` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | APERTO il 2026-10-04, su mandato del guardiano, e DA REGISTRARE SENZA CURARE: la cura la decide Luca. IL FATTO |
| `SCHWINGER-UN-NODO` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | MISURATO il 2026-10-01. Lo Schwinger aggiunge SOLO l antinodo, accanto a un genitore CHE C ERA GIA, con perc_c |
| `TETTO-CAUSALE-TEMPO-COORDINATO` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | APERTO il 2026-10-03, TROVATO DAL GUARDIANO, e da CURARE in un commit A SE (non ora: lo STOP del commit 4 vien |
| `Y1` | `FISICA`/era `2`/`AGENDA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: Y1 DA RIVERIFICARE ⏳[EPOCA 1 · MISURA] / Il settore U(1) non ha un'osservabile dell'OROLO |
| `AUDIT-CURE` | `FISICA`/era `2`/`AGENDA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | APERTA il 2026-10-04, DECISIONE DI LUCA. LA DOMANDA, per ogni legge aggiunta al simulatore: e stata introdotta |
| `LOSCHMIDT-ECO` | `FISICA`/era `2`/`AGENDA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | REGISTRATA il 2026-10-02 nel par. (D-ter) del piano del calore, su mandato di Luca, e NON DA FARE OGGI. LA MIS |
| `RISCRITTURA-GO` | `FISICA`/era `2`/`AGENDA` | ### **`INFRASTRUTTURA`/era `ENTRAMBE`/`APERTA`** | riscrivere il simulatore in Go: valutato, NON deciso |
| `M-LEGAMI` | `FISICA`/era `2`/`AGENDA` | ### **NON TOCCATA** | CANDIDATA REGISTRATA il 2026-10-07 e NON DECISA, dal rapporto doc/MEMORIE_MANCANTI.md paragrafo 5, coi sette c |
| `M-ISTERESI` | `FISICA`/era `2`/`AGENDA` | ### **NON TOCCATA** | CANDIDATA REGISTRATA il 2026-10-07 e NON DECISA, dal rapporto doc/MEMORIE_MANCANTI.md paragrafo 5, coi sette c |
| `MEM-VERSO` | `FISICA`/era `2`/`AGENDA` | ### **NON TOCCATA** | CANDIDATA REGISTRATA il 2026-10-07 e NON DECISA, dal rapporto doc/MEMORIE_MANCANTI.md paragrafo 5, coi sette c |
| `M-FLUSSO` | `FISICA`/era `2`/`AGENDA` | ### **NON TOCCATA** | CANDIDATA REGISTRATA il 2026-10-07 e NON DECISA, dal rapporto doc/MEMORIE_MANCANTI.md paragrafo 5, coi sette c |
| `M-MASSA` | `FISICA`/era `2`/`AGENDA` | ### **NON TOCCATA** | CANDIDATA REGISTRATA il 2026-10-07 e NON DECISA, dal rapporto doc/MEMORIE_MANCANTI.md paragrafo 5, coi sette c |

### ⛔ **LE CINQUE CHE NON HO TOCCATO, e il perche':** `M-LEGAMI`, `M-ISTERESI`, `MEM-VERSO`, `M-FLUSSO`, `M-MASSA` restano `FISICA`/era `2`/`AGENDA` e portano ### **solo** la nota *«da decidere da Luca: era `1` o `2`»*. Il mandato dice ### **NON toccare**, e ### **una voce di cui non si sa l'era non si sposta per simmetria con le altre.** ### **Sono l'unico posto dove l'indice dice «non lo so» sull'era**, e non e' un difetto: e' una domanda a Luca ### **scritta nella voce.**

---

## ③ BLOCCO `B` — **le GEMELLE, i fuori posto, e `D13`/`Z11`**

### ⚠ **DUE REGOLE DI STATO DIVERSE, e il mandato le distingue** — l'avevo letta male, e l'ho presa ### **prima di applicare:**

| il gruppo | lo stato |
|---|---|
| le ### **GEMELLE** → `METODO/ENTRAMBE` | *«lo stato attuale ### **se CHIUSA**, altrimenti ### **APERTA**»* |
| `DOCUMENTAZIONE` e `INFRASTRUTTURA` → era `1` | *«### **lo stato ATTUALE**»* — ### **non si tocca** |

### ⛔ **Avevo scritto la prima regola per TUTTE**, e avrebbe portato `5` voci da `SOSPESA` ad `APERTA` ### **senza che il mandato lo chieda.** Il perche' sta nel sorgente di `agg`, in `csv/_fase3_correzione.py`.

| id | prima | dopo | il testo che lo dice |
|---|---|---|---|
| `Z31` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`CHIUSA`** | titolo_breve INTERO: Z31 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / QUATTRO SIGILLI NON SONO PIU' RI-GIRABILI |
| `Z100` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`CHIUSA`** | titolo_breve INTERO: Z100 CURATA E SIGILLATA ⏳[EPOCA 3 · CURA] / INVARIANTI (C5): il programma si fe |
| `C28` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`CHIUSA`** | titolo_breve INTERO: C28 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / 14 FLAG SU 16 NON HANNO ALCUN SIGILLO. Ti |
| `Z20` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`CHIUSA`** | Z20 VALE SEMPRE ⏳[EPOCA 1 · MISURA] / UN DRIVER CHE FORZA UN FLAG IN TUTTI I BRACCI RENDE L'A/B NON… |
| `Z86` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`CHIUSA`** | titolo_breve INTERO: Z86 VALE SEMPRE ⏳[EPOCA 2 · CODICE] / IL CRITERIO Z4a DEL SIGILLO DEL RAMO D ER |
| `Z145` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`CHIUSA`** | CHIUSO — T5 del sigillo di CURA 2 era invalido: dv 0 letto come effetto (2026-09-24) |
| `CHI-TORS-ZERO-FALSO` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`CHIUSA`** | APERTA il 2026-10-06 dalla misura del 0.3 a zero (strumento 16dced88 su cf2a1ac8). IL FATTO: il ganc |
| `H-ETC-1` | `FISICA`/era `1`/`SOSPESA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | titolo_breve INTERO: PRESIDIO PROPOSTO E NON CABLATO (A9: oggi NON impedisce nulla): conta dall'AST  |
| `REGISTRO_FISICA:A5` | `FISICA`/era `1`/`SOSPESA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | CONTROLLO POSITIVO: ON e OFF DEVONO differire |
| `REGISTRO_FISICA:U2-6` | `FISICA`/era `1`/`SOSPESA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | 6 È IL CASO CHE DEVE FALLIRE (P1-sexies, ed è il criterio più importante): la |
| `COMPONENTI:S2` | `FISICA`/era `1`/`SOSPESA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | titolo_breve INTERO: riduzione al limite sul blob ATTUALE: ON (cs=CSM) vs OFF byte-identico / 0.000e |
| `COMPONENTI:S3` | `FISICA`/era `1`/`SOSPESA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | S3.0 / IL CONTROLLO POSITIVO: il test VEDE l'effetto / 39/40 nodi con \/f(1)−f(0)\/ 1e-13 |
| `CENS-A6` | `FISICA`/era `1`/`SOSPESA` | ### **`DOCUMENTAZIONE`/era `1`/`SOSPESA`** | titolo_breve INTERO: [classe A del censimento] `README.md`: *"Tutti gli script di lancio includono e |
| `CENS-A7` | `FISICA`/era `1`/`SOSPESA` | ### **`DOCUMENTAZIONE`/era `1`/`SOSPESA`** | titolo_breve INTERO: [classe A del censimento] il commento di `calcola_psi`: *"~19 chiamanti"*, misu |
| `SMP-APRI-COMMENTO` | `FISICA`/era `1`/`SOSPESA` | ### **`DOCUMENTAZIONE`/era `1`/`SOSPESA`** | TROVATO il 2026-10-01 da un CONTATORE che contraddice un COMMENTO, mentre giravo la prova di fumo de |
| `MITOSI-2LAM-ACCESO` | `FISICA`/era `1`/`SOSPESA` | ### **`DOCUMENTAZIONE`/era `1`/`SOSPESA`** | MISURATO il 2026-10-02 dal RUNTIME, caricando il simulatore con l ARGV DEL DRIVER (_cli_flag.argv_de |
| `C25` | `FISICA`/era `1`/`CHIUSA` | ### **`INFRASTRUTTURA`/era `1`/`CHIUSA`** | C25 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / UN FILE NON SI PUO' COMMITTARE PER IL SUO ESSERE CRLF: git lo… |
| `PERC-TW-MORTA` | `FISICA`/era `1`/`SOSPESA` | ### **`INFRASTRUTTURA`/era `1`/`SOSPESA`** | APERTA il 2026-10-07. TROVATA DAL CENSIMENTO DELLO STATO del paragrafo 2 del rapporto, e NON era nel |
| `TRATTI-INTERNI` | `METODO`/era `ENTRAMBE`/`APERTA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: la scomposizione in unita' assolute D_interni = D_centri - D_varco esclude lo z |
| `CHK2` | `METODO`/era `ENTRAMBE`/`APERTA` | ### **`FISICA`/era `1`/`SOSPESA`** | CHECKPOINT 2 / GLOBALE §3 / raggiunto e riferito a Luca. IL RUN LUNGO NON SI LANCIA |
| `CHK3` | `METODO`/era `ENTRAMBE`/`APERTA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: CHECKPOINT: referto dei quattro esiti, ciascuno contro le sue letture fissate P |
| `CHK3-D` | `METODO`/era `ENTRAMBE`/`APERTA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: Nel referto del CHK3, la sezione «I DIFETTI NUOVI CONTRO LE MISURE GIA' FATTE»  |
| `E3` | `METODO`/era `ENTRAMBE`/`APERTA` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: EPOCA 3 + RUN LUNGO — tag epoca-3, 3000 passi, M1/M4 leggere durante il run / G |
| `B7` | `FISICA`/era `DA_CLASSIFICARE`/`DA_CLASSIFICARE` | ### **`FISICA`/era `1`/`SOSPESA`** | titolo_breve INTERO: i reperti DA RIMISURARE sulla scena nuova / Z43, Z46, Z48-Z52, coerg / misurati |
| `D13` | `METODO`/era `ENTRAMBE`/`APERTA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | I sigilli storici non sono stati rigirati sul blob corrente / Z11 / — / APERTO |
| `Z11` | `FISICA`/era `1`/`CHIUSA` | ### **`METODO`/era `ENTRAMBE`/`APERTA`** | titolo_breve INTERO: Z11 VALE SEMPRE ⏳[EPOCA 1 · CODICE] / RIGIRO DEI SIGILLI STORICI — lavoro PREVI |

### ⭐ **`D13` e `Z11` SONO LO STESSO FATTO, e lo stato si allinea su `APERTA`**

| | il testo | com'era |
|---|---|---|
| `D13` | *«I sigilli storici non sono stati rigirati sul blob corrente | `Z11`»* | `APERTA` |
| `Z11` | *«RIGIRO DEI SIGILLI STORICI — ### **lavoro PREVISTO, non ancora fatto**»* | ### **`CHIUSA`**, con una chiusura |

### ⛔ **Il testo di `Z11` dice DA SE' che il lavoro non e' fatto:** una voce `CHIUSA` su un lavoro non fatto e' ### **un FALSO CHIUSO.** ➜ **Allineate su `APERTA`**, la chiusura di `Z11` ### **tolta**, e ### **collegate nei due versi.**

### ⚠ **`superata_da` NON si poteva usare**, e lo scrivo perche' il mandato offriva quella strada: lo schema vuole ### **un id di DECISIONE o di ASSIOMA**, non di un'altra voce. ➜ `collegate`.

---

## ④ BLOCCO `C` — **la mia regola era SBAGLIATA**

> ### ⛔ **La fase `2` diceva:** *«se tutte le citazioni stanno in documenti, e' un'etichetta»*. ### **E' FALSO:** un documento e' ### **esattamente il posto in cui un ID si DEFINISCE.**

| | che cos'e' |
|---|---|
| ### ✔ **DEFINIZIONE** | una ### **RIGA DI TABELLA** che apre con l'ID, o un'### **INTESTAZIONE** che lo contiene |
| ### ⚠ **citazione** | tutto il resto, ### **nel corpo del testo** |

Il vecchio indice diceva di queste `16` *«CITATO `N` volte, ### **MAI definito in un registro**»*: ### **vero alla lettera** *(non stanno in un registro)* e ### **falso nella sostanza** — ### **sono definite.**

### ⛔ **LA TRAPPOLA, E L'HO PRESA PRIMA DI APPLICARE**

La prima stesura cercava la definizione in ### **tutti** i file citanti, e trovava ### **`37`** definizioni invece di `28`: perche' cercava anche in ### **`doc/LISTA_CHIUSA.md`, CHE E' LA LISTA DEGLI ID.** Ogni ID ci compare ### **per definizione di cos'e' quel file**, quindi trovarci una riga di tabella e' ### **un FALSO-UNO** — un verdetto garantito da qualcosa che ### **non parla del merito.** `TW-1` risultava definito in `LISTA_CHIUSA.md:711` invece che in `doc/SCALE_TW_lettura.md:227`, che e' il posto dove la riga ### **dice che cosa e'.**

### ⭐ **E' LO STESSO DIFETTO DEL CONTROLLO `C4`**, che leggeva `doc/INDICE.md` — ### **un file che genera lui stesso.** Le ### **viste generate** sono escluse, e il perche' sta nel sorgente.

| id | classe | dominio/era/stato | definita da | dove |
|---|---|---|---|---|
| `O4` | `FRONTE` | `FISICA`/`1`/`SOSPESA` | riga di tabella | `doc/IPOTESI_gravita_a_spinta.md` |
| `SHAKE-THEN-FREEZE` | `MISURA` | `FISICA`/`1`/`CHIUSA` | riga di tabella | `STATO_CLAUDE_fork-su2.md` |
| `TS-1` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/LETTURA_accensione_e_torsione.md` |
| `TS-2` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/LETTURA_accensione_e_torsione.md` |
| `TS-3` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/LETTURA_accensione_e_torsione.md` |
| `TS-4` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/LETTURA_accensione_e_torsione.md` |
| `TS-5` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/LETTURA_accensione_e_torsione.md` |
| `TS-6` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/LETTURA_accensione_e_torsione.md` |
| `TW-1` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/SCALE_TW_lettura.md` |
| `TW-2` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/SCALE_TW_lettura.md` |
| `TW-3` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/SCALE_TW_lettura.md` |
| `TW-4` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/SCALE_TW_lettura.md` |
| `TW-5` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/SCALE_TW_lettura.md` |
| `TW-6` | `CRITERIO` | `METODO`/`1`/`SOSPESA` | riga di tabella | `doc/SCALE_TW_lettura.md` |
| `D5` | `NON_DEFINITA` | `DA_CLASSIFICARE`/`DA_CLASSIFICARE`/`DA_CLASSIFICARE` | ### **OMONIMO** | `doc/CENSIMENTO_intenzioni.md` |
| `D6` | `NON_DEFINITA` | `DA_CLASSIFICARE`/`DA_CLASSIFICARE`/`DA_CLASSIFICARE` | ### **OMONIMO** | `doc/CENSIMENTO_intenzioni.md` |

### ⭐ **`O4` STAVA FRA LE ETICHETTE, ED E' UNA DELLE OBIEZIONI AL BERSAGLIO DEL PROGETTO:** *«CONSERVAZIONE DELL'ENERGIA. L'energia assorbita non si riesce a bilanciare»*, Maxwell e Poincare', ### **«la massa della Terra raddoppierebbe in una frazione di secondo»** — `doc/IPOTESI_gravita_a_spinta.md:47`.

### ⛔ **`D5` e `D6`: OMONIMI, E NON SI SCEGLIE**

| id | una definizione | l'altra |
|---|---|---|
| `D5` | doc/CENSIMENTO_intenzioni.md:315 -- `:936` (`SYNC_UPDATE`) e le sue motivazioni sparse nei documenti | doc/MAPPA_accoppiamenti_spin.md:70 -- `omega_s`, `- omega_src/_tau`: IL POZZO |
| `D6` | doc/CENSIMENTO_intenzioni.md:316 -- `Checkpoint.md` nel suo insieme (~640 righe), ~40 voci [TODO]/[IN VERIFICA] | doc/MAPPA_accoppiamenti_spin.md:71 -- `calcio_omega` in `semina()`: punto zero ALLA NASCITA, non per passo |

Nascono `NON_DEFINITA`, con le due definizioni nel metadato `omonimo` *(registrato in `9e2340e`)*. ### **Il mandato dice «NON scegliere», e la scelta e' di Luca.**

### ✔ **E DUE CHE SEMBRAVANO OMONIMI E NON LO SONO**, verificate leggendo le due righe:

| id | perche' NON e' un omonimo |
|---|---|
| `O4` | `doc/IPOTESI_gravita_a_spinta.md:47` e `doc/relazioni/2026-09-21.md:1876` sono ### **la STESSA obiezione** *(energia, Maxwell/Poincare', la massa della Terra che raddoppierebbe)*: la relazione ne riporta ### **una tavola riassunta** |
| `ROMPI-ANELLO` | due intestazioni ### **nello STESSO file** *(`doc/REFERTO_frequenza_riferimento.md`, righe `1` e `138`)*: ### **il titolo del referto e una sua sezione** |

### ⛔ **CHE COSA RESTA A LUCA, E PERCHE' NON L'HO DECISO IO**

Il ripasso dice che ### **`28` delle `53`** sono DEFINITE. Il mandato ne nomina ### **`16`** con la loro classificazione. ### **Le altre `12` le lascio fra le etichette, e lo dichiaro:** il mandato non dice ### **con quale CLASSE e DOMINIO** devono nascere, e sceglierlo io ### **sarebbe decidere al posto di Luca.**

| id | definita da | dove |
|---|---|---|
| `ARCHI-PASSO` | intestazione | `RELAZIONE_PER_CLAUDE.md:5110` |
| `AUTO-MANUTENZIONE` | intestazione | `doc/STORIA_REGOLE.md:479` |
| `DA-DECIDERE` | intestazione | `RELAZIONE_PER_CLAUDE.md:5025` |
| `DE-ACCOPPIABILITA` | intestazione | `doc/INDAGINE_scuotimento.md:156` |
| `DOMANDE-BUSSOLA` | intestazione | `doc/BUSSOLA_dev-spinoriale.md:50` |
| `FORK-FIRST` | intestazione | `CLAUDECONNECT.md:469` |
| `GLOBALE-DIS` | intestazione | `doc/relazioni/2026-09-26.md:1068` |
| `POST-HOC` | intestazione | `doc/REFERTO_due_masse.md:69` |
| `RI-ETICHETTATO` | intestazione | `doc/REPERTO_cs_dinamico_spento.md:97` |
| `RI-VERIFICATI` | intestazione | `doc/PIANO_merge_main.md:55` |
| `ROMPI-ANELLO` | intestazione | `doc/REFERTO_frequenza_riferimento.md:1` |
| `SOVRA-CORREGGE` | intestazione | `CLAUDECONNECT.md:504` |

### ⚠ **SONO TUTTE INTESTAZIONI, nessuna riga di tabella, e questo e' il motivo del dubbio:** un'intestazione che contiene un ID puo' essere ### **la sua definizione** oppure ### **solo un titolo che lo NOMINA.** Per le `16` del mandato la lettura l'ha fatta il guardiano; ### **per queste no.** Stanno in `doc/indice/_ripasso_restano_a_luca.json`, con la riga che le definisce.

---

## ⑤ BLOCCO `D` — **il campo `commit` dello storico**

| commit | righe |
|---|--:|
| `a7569dd` | `313` |
| `179e293` | `188` |
| `9eee882` | `179` |
| `a80b3e9` | `167` |
| `6cac9f4` | `135` |
| `3ad58a2` | `48` |
| `9e2340e` | `48` |
| `### **(vuoto)**` | `1` |

Lo storico e' ### **solo in aggiunta**, quindi per ogni commit che l'ha toccato le righe `[quante_prima, quante_dopo)` sono ### **esattamente quelle che quel commit ha scritto.** ### **Non e' una stima: e' una partizione.** ### ✔ **E la premessa si VERIFICA:** per ogni commit la funzione rilegge la sua versione e controlla che sia ### **un PREFISSO** di quella di oggi, riga per riga su `(id, quando, motivo)`; se lo storico fosse stato riscritto, ### **si ferma.** Non si e' fermata.

### ⛔ **LA COSA CHE IL MANDATO CHIEDE E CHE NON E' POSSIBILE**

Il mandato dice *«da ora in avanti `aggiorna-lotto` lo scrive»*. ### **Non e' letteralmente possibile:** quando il lotto gira, ### **il commit che lo conterra' NON ESISTE ANCORA.** Il `pre-commit` e il `commit-msg` girano ### **prima** che l'oggetto commit ci sia, e un `post-commit` che riempisse il campo dovrebbe ### **riscrivere il commit appena fatto.**

| | che cosa ho fatto al suo posto |
|---|---|
| ### **`commit_base`** | lo ### **timbra la via di scrittura**, automaticamente: `HEAD` nel momento in cui scrive. ### **Quello si sa**, ed e' ### **il codice su cui la modifica e' stata fatta** |
| ### **`commit`** | lo riempie ### **`storico-commit`** dai log, ed e' ### **ri-girabile in ogni momento** |
| ### ⚠ **un lotto di RITARDO** | le righe dell'ultimo commit si riempiono ### **al giro successivo.** ### **Non e' un difetto nascosto: e' la conseguenza di QUANDO esiste un commit** |

### ⚠ **`commit_base` manca alle `1078` righe vecchie**, e non si ricostruisce a posteriori senza indovinare: ### **non lo invento.** Da adesso ce l'hanno tutte quelle nuove.

---

## ⑥ I CONTROLLI

```
  C1 CONSERVAZIONE: ogni ID vecchio in UNO E UNO SOLO posto PASSA   persi 0, doppi 0
  C2 la TRACCIA copre ogni ID vecchio, con la REGOLA       PASSA   senza traccia 0
  C3 LE LISTE DEL GUARDIANO: classificazione come indicata PASSA   fuori posto 0
  C4 IDEMPOTENZA (NON si rilancia: c'e' lavoro di dopo)    PASSA   storico.jsonl ha 1079 righe -> verificata al commit 6b8cb90; e la migrazione ha un PRESIDIO che la ferma
  C5 `indice.py valida` passa                              PASSA     unicita', metadati, indice invertito e viste: **TUTTO A PO
  C6 la VISTA passa IL VALIDATORE VECCHIO (quello del pre-commit) e la domanda PASSA   12 bloccanti su 830 voci
```

| | |
|---|---|
| `python csv/_controlli_indice_v2.py` | ### **6 su 6** |
| `python csv/indice.py collaudo` | ### **21 su 21** |
| `python csv/indice.py valida` | ### **passa** |
| `python csv/_indice_id.py` *(il validatore del `pre-commit`)* | ### **passa** |
| ### **gli ID vecchi** | ### **`953` conservati**, `0` persi, `0` doppi |

---

## ⑦ I DIFETTI MIEI DI QUESTO GIRO — **tre presi, uno aperto**

| | il difetto | chi l'ha preso |
|---|---|---|
| `1` | la regola dello stato del blocco `B`: avevo applicato *«se `CHIUSA` tieni, altrimenti `APERTA`»* ### **anche a `DOCUMENTAZIONE` e `INFRASTRUTTURA`**, dove il mandato dice *«stato attuale»*. `5` voci da `SOSPESA` ad `APERTA` ### **senza che il mandato lo chieda** | ### **io, rileggendo il mandato prima di applicare** |
| `2` | il ripasso del blocco `C` cercava la definizione anche in ### **`doc/LISTA_CHIUSA.md`, che e' la lista degli ID**: `37` definizioni invece di `28`, ### **un FALSO-UNO** | ### **io, guardando i nomi dei file nell'uscita** |
| `3` | alle `16` voci nuove mancava ### **`tipo_era1`**, e la vista compatibile ci mette `classe.lower()` = `criterio`, che ### **non sta nel vocabolario dell'era `1`** *(`criterio-locale`)* | ### **il `pre-commit`**, con `12` righe rifiutate |
| `4` | ### ⛔ **il controllo `C6` era PIU' DEBOLE DEL HOOK:** girava solo `_indice_id.py --blocca SI` — ### **un'interrogazione** — mentre il `pre-commit` gira ### **il VALIDATORE** | ### **il `pre-commit`, bloccando dove `C6` diceva PASSA** |

### ⭐ **IL `4` E' IL PEGGIORE DEI QUATTRO**, e lo scrivo per primo nel sorgente: ### **un controllo che gira un comando piu' debole di quello del presidio non protegge niente** (`A9`). ➜ **Adesso `C6` gira ENTRAMBI, il validatore PRIMA** — e ### **la prima volta che l'ho girato ha preso subito DUE COLLISIONI DI TITOLO** che io non avevo visto:

| | la collisione | che cos'era |
|---|---|---|
| `D6` ≡ `D5` | titolo identico | ### **l'avevo scritto io uguale per entrambi**: ci va l'ID, e adesso c'e' |
| `TW-1` ≡ `TS-6` | titolo identico | ### **NON e' un difetto del generatore:** le due righe ### **dicono davvero la stessa cosa** — *«flag OFF = byte-identico, firma dei byte, un processo per braccio»* — scritte in ### **due documenti diversi.** Il titolo porta il documento |

### ⛔ **E UNO CHE RESTA APERTO, perche' non l'ho curato:** ### **`INDICE-COLLAUDO-SCRITTURA`** — `python csv/indice.py collaudo` dice ### **`21` su `21`**, ma ### **i `21` casi provano `valida` IN MEMORIA** e ### **nessuno prova una via di SCRITTURA.** `crea-lotto` e `storico-commit` sono nati oggi e sono entrati in uso ### **su `64` voci, senza un caso che DEBBA fallire.** La spiegazione lunga sta in `doc/STATO_RUN.md` ### **con lo stesso ID.**

---

## ⑧ CHE COSA RESTA A LUCA

| | quanti | che cosa |
|---|--:|---|
| ### **i concetti da definire** | `181` | erano segnaposto, e ### **il codice o i sigilli li NOMINANO.** `D5` e `D6` ci sono ### **da adesso**, come ### **OMONIMI** |
| ### **l'era di `5` voci** | `5` | `M-LEGAMI` `M-ISTERESI` `MEM-VERSO` `M-FLUSSO` `M-MASSA`: ### **era `1` o `2`?** Il mandato dice NON toccare |
| ### **le `12` etichette definite** | `12` | ### **con quale classe e dominio** devono nascere |
| ### **gli assiomi riclassificati** | `20` | ciascuno con *«da confermare da Luca»* |
| ### **la traccia della migrazione** | — | dice ancora `(fase2-b2)` per le `16` ripristinate, cioe' *«diventata etichetta»*. ### **NON l'ho riscritta:** la traccia dice ### **che cosa ha fatto la MIGRAZIONE**, lo storico dice ### **che cosa e' stato corretto dopo** |

> ### ⭐ **E il criterio che ho tenuto in tutto il giro:** dove il mandato ### **nomina** la classificazione, l'ho applicata; dove ### **non la nomina**, ### **ho lasciato la voce dov'era e l'ho scritta qui.** ### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un difetto.**

