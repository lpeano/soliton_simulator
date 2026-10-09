# IL REFERTO DELLE CHIUSURE, DELLE SUPERATE E DELLA TERZA LETTURA

> ### ⭐ **«IL COMMIT DI CHIUSURA SI RICAVA, NON SI INVENTA.»** Nel giro scorso avevo lasciato ### **`47` chiusure non fatte** scrivendo *«un commit non si inventa»*: ### **non inventarlo era giusto, fermarsi li- era una RINUNCIA.** ### ⛔ **E l'errore sotto l'errore: cercavo lo sha DENTRO LA RIGA**, e una riga di documento ### **non ha nessun motivo di portare lo sha del commit che l'ha scritta.**

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_chiusure_e_strumenti_era2.md`, ### **committato PRIMA del lavoro** *(`c24bbd5`)* |
| **i due file del guardiano** | `correzioni_guardiano_2026-10-09.txt` *(`165` righe, `67c12fa`)* e `correzioni_guardiano_2026-10-09_b.txt` *(`59` righe, `3926dbb`)*, ### **ciascuno committato DA SOLO** |
| **i commit** | `570d43a` *(`1`)* · `6101c09` *(`2`)* · `7e4c59c` *(`3`)* · `7545c1a` *(`4`)* · `3926dbb`+`43c4dc2` *(`5`)*, piu' questo |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |
| **i controlli** | ### **6/6** · presidi ### **59/59** · indice ### **26/26** |

---

## ① PUNTO `1` — **il commit di chiusura si RICAVA**: `46` su `47`

| | quante | |
|---|--:|---|
| ### **commit RICAVATO dalla storia** | ### **`46`** | `git log -S'<frase>' --reverse -- <file>`, ### **il PRIMO** — quello che ### **INTRODUCE** la frase |
| ### **dal tag `era-1-secondo-ordine`** | `1` | la stessa regola della migrazione. ### **Il tag dice «ENTRO QUI», non «proprio qui»** |
| ### ⚠ **frasi GENERICHE** | `9` | la citazione compare in ### **piu' di tre righe del file**: il commit c'e', ### **ma la frase non identifica la riga** |

### ⛔ **DUE FALSI, TROVATI GUARDANDO L'USCITA PRIMA DI SCRIVERE.** La citazione di `REGISTRO_FISICA:T4` e' *«PASS»* e ### **«passato» la contiene**; quella di `REGISTRO_FISICA:P3` e' *«TIENE»* e ### **«CONTIENE» la contiene.** Le due combaciavano con la ### **riga `1`** e la ### **riga `11`** del registro — ### **il TITOLO del documento** — e il commit *«ricavato»* sarebbe stato ### **quello che ha creato il file.** ### ⭐ **E- la TERZA volta che una parola dentro un'altra parola mi inganna** *(la prima: `infinito` contiene `FINITO`)*: adesso si cerca ### **a confine di parola.**

| id | come | commit | dove si e- trovata la frase |
|---|---|---|---|
| `C13` | ### **RICAVATO** | `fa42066` | riga 215 di `doc/RAMIFICAZIONI.md` |
| `C17` | ### **RICAVATO** | `fa42066` | riga 215 di `doc/RAMIFICAZIONI.md` |
| `C18` | ### **RICAVATO** | `fa42066` | riga 215 di `doc/RAMIFICAZIONI.md` |
| `C22` | ### **RICAVATO** | `fa42066` | riga 215 di `doc/RAMIFICAZIONI.md` |
| `C23` | ### **RICAVATO** | `fa42066` | riga 215 di `doc/RAMIFICAZIONI.md` |
| `C24` | ### **RICAVATO** | `fa42066` | riga 215 di `doc/RAMIFICAZIONI.md` |
| `C1-PEQ-ESATTO` | ### **RICAVATO** | `72df045` | riga 42 di `doc/STATO_RUN.md`; ### ATTENZIONE: 88 righe del file contengono la frase, quindi e- GENERICA |
| `C1BIS-ANOM-SIMM` | ### **RICAVATO** | `72df045` | riga 42 di `doc/STATO_RUN.md`; ### ATTENZIONE: 88 righe del file contengono la frase, quindi e- GENERICA |
| `C2-PEQ-NASCITA` | ### **RICAVATO** | `72df045` | riga 42 di `doc/STATO_RUN.md`; ### ATTENZIONE: 88 righe del file contengono la frase, quindi e- GENERICA |
| `C3-SCALA-MIN-PASSO` | ### **RICAVATO** | `72df045` | riga 42 di `doc/STATO_RUN.md`; ### ATTENZIONE: 88 righe del file contengono la frase, quindi e- GENERICA |
| `C4-COES-CAUSALE` | ### **RICAVATO** | `72df045` | riga 42 di `doc/STATO_RUN.md`; ### ATTENZIONE: 88 righe del file contengono la frase, quindi e- GENERICA |
| `D0` | ### **RICAVATO** | `a48cd96` | riga 434 di `doc/STATO_RUN.md` |
| `CHK2` | ### **RICAVATO** | `1b40fdb` | riga 433 di `doc/STATO_RUN.md` |
| `COMPONENTI:S3b` | ### **RICAVATO** | `5c6e770` | riga 76 di `doc/COMPONENTI_PROMOSSE.md` |
| `COMPONENTI:S3c` | ### **RICAVATO** | `5c6e770` | riga 76 di `doc/COMPONENTI_PROMOSSE.md` |
| `D34` | ### **RICAVATO** | `29c7c0b` | riga 652 di `doc/STATO_RUN.md` |
| `G2` | ### **RICAVATO** | `fedda6c` | riga 436 di `doc/STATO_RUN.md` |
| `G3` | ### **RICAVATO** | `52486f0` | riga 437 di `doc/STATO_RUN.md` |
| `G4` | ### **RICAVATO** | `f6d432c` | riga 438 di `doc/STATO_RUN.md` |
| `S03` | ### **RICAVATO** | `fbd3bc9` | riga 721 di `doc/STATO_RUN.md` |
| `S04` | ### **RICAVATO** | `8c97e76` | riga 722 di `doc/STATO_RUN.md` |
| `Z13` | ### **RICAVATO** | `fa1089c` | riga 322 di `doc/RAMIFICAZIONI.md` |
| `REGISTRO_FISICA:P2` | ### **RICAVATO** | `afb461e` | riga 4286 di `doc/REGISTRO_FISICA.md` |
| `Z29` | ### **RICAVATO** | `fa1089c` | riga 338 di `doc/RAMIFICAZIONI.md` |
| `Z30` | ### **RICAVATO** | `fa1089c` | riga 339 di `doc/RAMIFICAZIONI.md` |
| `Z53` | ### **RICAVATO** | `fa1089c` | riga 362 di `doc/RAMIFICAZIONI.md` |
| `Z5` | ### **RICAVATO** | `fa1089c` | riga 448 di `doc/RAMIFICAZIONI.md`; ### ATTENZIONE: 8 righe del file contengono la frase, quindi e- GENERICA |
| `Z28` | ### **RICAVATO** | `fa1089c` | riga 337 di `doc/RAMIFICAZIONI.md` |
| `REGISTRO_FISICA:T3` | ### **RICAVATO** | `3c5e404` | riga 3239 di `doc/REGISTRO_FISICA.md` |
| `REGISTRO_FISICA:T4` | ### **RICAVATO** | `0432dac` | riga 3200 di `doc/REGISTRO_FISICA.md` |
| `REGISTRO_FISICA:T5` | ### **RICAVATO** | `3c5e404` | riga 3239 di `doc/REGISTRO_FISICA.md` |
| `REGISTRO_FISICA:U2-5` | ### **RICAVATO** | `3c5e404` | riga 3239 di `doc/REGISTRO_FISICA.md` |
| `REGISTRO_FISICA:U2-6` | ### **RICAVATO** | `3c5e404` | riga 3239 di `doc/REGISTRO_FISICA.md` |
| `T3a` | ### **RICAVATO** | `6bc1bd2` | riga 15 di `csv/_seal_fork/_sigillo_scena_ii.py` |
| `T3b` | ### **RICAVATO** | `6bc1bd2` | riga 15 di `csv/_seal_fork/_sigillo_scena_ii.py` |
| `Z142` | ### **RICAVATO** | `3e5b7b3` | riga 442 di `doc/RAMIFICAZIONI.md` |
| `C5` | ### **RICAVATO** | `fa42066` | riga 215 di `doc/RAMIFICAZIONI.md` |
| `H1` | ### **RICAVATO** | `55a7edc` | riga 9431 di `RELAZIONE_PER_CLAUDE.md`; ### ATTENZIONE: 6 righe del file contengono la frase, quindi e- GENERICA |
| `H3` | ### **RICAVATO** | `d90a547` | riga 8 di `doc/REFERTO_h3_termostato_2026-10-07.md`; ### ATTENZIONE: 6 righe del file contengono la frase, quindi e- GENERICA |
| `DE-ACCOPPIABILITA` | ### **RICAVATO** | `515aaf7` | riga 158 di `doc/INDAGINE_scuotimento.md` |
| `REGISTRO_FISICA:P3` | ### **RICAVATO** | `89ad8cd` | riga 71 di `doc/REGISTRO_FISICA.md`; ### ATTENZIONE: 18 righe del file contengono la frase, quindi e- GENERICA |
| `Z27` | ### **RICAVATO** | `fa1089c` | riga 336 di `doc/RAMIFICAZIONI.md` |
| `REGISTRO_FISICA:E4-LAM` | ### **RICAVATO** | `e8d8ba1` | riga 4913 di `doc/REGISTRO_FISICA.md` |
| `COMPONENTI:A1` | ### **RICAVATO** | `5c6e770` | riga 59 di `doc/COMPONENTI_PROMOSSE.md` |
| `L-SOGLIA` | ### **RICAVATO** | `33433dd` | riga 137 di `doc/PATTERN_DI_PROVA.md` |
| `STANDARD-4` | ### **RICAVATO** | `33433dd` | riga 137 di `doc/PATTERN_DI_PROVA.md` |
| `MITOSI-2LAM-ACCESO` | ### ⚠ **DAL TAG** | `dde9bc8` | la frase e- nel file (riga 23 di `doc/PIANO_riordino_mitosi.md`) ma `git log -S` non la trova nella storia |

### ⚠ **E SEI VOCI SONO CHIUSE DALLO STESSO COMMIT `fa42066`**, perche' la loro frase e' *«C. DIAGNOSI CHIUSE»* — ### **un'INTESTAZIONE DI SEZIONE.** Il commit che l'ha introdotta ### **ha chiuso tutte le diagnosi che stanno sotto**: e' corretto, ### **ma e- GROSSO**, e lo dichiaro.

---

## ② PUNTO `2` — **`F12` e le `chiusura` ORFANE**: `40` si svuotano, `1` chiude

> ### ⭐ **ERA IL ROVESCIO DI UN CONTROLLO CHE C'ERA GIA-:** `valida` pretendeva `chiusura.criterio` e `chiusura.commit` ### **quando lo stato e- `CHIUSA`**. Che una `chiusura` piena ### **implichi** `CHIUSA` ### **non lo chiedeva nessuno** — e ### **una delle due direzioni non e- un controllo: e- MEZZO controllo.**

### ⚠ **Erano `42` quando il mandato le ha contate; il punto `1` ne ha chiusa UNA**, quindi quando ci sono arrivato erano ### **`41`.** Il numero del mandato era giusto ### **al momento in cui l'ha scritto**, e lo dico perche' ### **un numero che non torna va spiegato, non aggiustato.**

### **LA RIGA CHIUDE → `CHIUSA`: `1`**

| id | prima | commit ricavato | la lettura della riga |
|---|---|---|---|
| `Z22` | `APERTA` | `fa1089c` | la riga dice <<FATTO>> (la PRIMA parola di stato): nei 74 script (tocca ogni strumento: va fatto in un commit dedicato, non dentro un es |

### **LA RIGA NON CHIUDE → la `chiusura` SI SVUOTA: `40`**

### ⭐ **E si svuota la `chiusura`, NON si muove lo stato:** lo stato ### **l'ha deciso un lavoro che ha letto la riga**; la `chiusura` e' ### **cio- che e- rimasto indietro** dalla migrazione. ### **Fra un campo deciso leggendo e un campo trascinato, cede il secondo.**

| id | resta | la lettura della riga | la `chiusura` che si toglie |
|---|---|---|---|
| `A1-TREVIE` | `SOSPESA` | NESSUNA parola decide: / A1-TREVIE / la catena a TRE VIE di step — if CHI_CORE… / elif VERSO_CHI… / elif not(…) / :3623  | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `A2-ANELLO` | `SOSPESA` | la riga dice <<NON CURATO>> (la PRIMA parola di stato): doc/RAMIFICAZIONI.md Z70 / registrato, NON curato. A6 nella sua  | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `A3-CHIRALE` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): i conserva / doc/RAMIFICAZIONI.md Z71 / APERTA. I due punti di scrit | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `A5-PANNELLO` | `SOSPESA` | la riga dice <<NON INIZIATO>> (la PRIMA parola di stato): ziale) / la ex-LISTA 3 di questo file / non iniziato / un pann | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `B1` | `SOSPESA` | la riga dice <<NON INIZIATO>> (la PRIMA parola di stato): /RAMIFICAZIONI.md Z47, doc/ASSIOMI.md / NON INIZIATO, e il reg | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `B10` | `SOSPESA` | NESSUNA parola decide: / B10 / --override-blob e la COPIA del driver / csv/_test_fork/_scena_video_ripresa.py (e68bb8c5, | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `B3` | `SOSPESA` | nessuna riga d'origine | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `B4` | `SOSPESA` | NESSUNA parola decide: / B4 / i np.zeros / tutto il simulatore / mai guardati / sono 116, non ~10. Il numero utile non è | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `B5` | `SOSPESA` | la riga dice <<APERTO>> (la PRIMA parola di stato): CLAUDE.md §9, registro C14, fronte A / aperto e noto: theta ~ 39-129 | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `B8` | `SOSPESA` | NESSUNA parola decide: / B8 / IL BLOCCO DEL RUN A 6000 AL PASSO 2700 / doc/REFERTO_blocco_run6000.md (131 righe), csv/_t | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `COPPIA-RAMP` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): / ❓ COPPIA-RAMP — APERTA il 2026-09-26 / PERCHE' LA COPPIA NON P | *chiusa nell'era 1 (stato `non-difetto` al tag era-1-secondo-ordine)* |
| `D27` | `SOSPESA` | la riga dice <<APERTO>> (la PRIMA parola di stato): / Z65 / DIFETTO / D27 (APERTO) / Il grafo e' in QUATTRO COMPONENTI c | *chiusa nell'era 1 (stato `non-difetto` al tag era-1-secondo-ordine)* |
| `DRIVER-SCENA-II` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): / OSSERVABILE-P1 — APERTA il 2026-09-26 (rilievo di Luca) / NON E | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `H-FILE` | `APERTA` | nessuna riga d'origine | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `H-NON-TRACCIATI` | `APERTA` | nessuna riga d'origine | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `H-STASH` | `APERTA` | nessuna riga d'origine | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `LUNGA-BATTITO-CADUTA` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): cade al passo 1, e cade su una STAMPA (Aperta il 2026-10-06. Strumen | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `SOGLIA-MITOSI-3PI` | `SOSPESA` | NESSUNA parola decide: ## SOGLIA-MITOSI-3PI — la soglia porta un π di dipolo che quasi nessun arco ha (Aperta il 2026-10 | *la riga dice <<FATTO>> (la PRIMA parola di stato): teva una voce dedicata alla s* |
| `X1` | `SOSPESA` | la riga dice <<SI CHIUDE QUANDO>> (la PRIMA parola di stato): tingue materia e antimateria) e' buono. Si chiude quando ( | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Y2` | `SOSPESA` | NESSUNA parola decide: / Y2 VALE SEMPRE [EPOCA 1 · MISURA] / Due osservabili U(1) hanno il nullo SBAGLIATO o NON VERIFIC | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z10` | `SOSPESA` | la riga dice <<SI CHIUDE QUANDO>> (la PRIMA parola di stato): ndipendenti e' una decisione di regime. Si chiude quando l | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z19` | `SOSPESA` | NESSUNA parola decide: / Z19 VALE SEMPRE [EPOCA 1 · MISURA] / QUARTA VOLTA: una grandezza letta in un momento del passo  | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z2` | `SOSPESA` | NESSUNA parola decide: / Z2 VALE SEMPRE [EPOCA 1 · MISURA] / spinta: A2 e A3 sono stati tolti, A1 NO (2026-09-17) / La c | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z20` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): i, non dal codice del driver. Lacuna P6 aperta: # RUN_PARAMS non con | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z31` | `SOSPESA` | NESSUNA parola decide: / Z31 VALE SEMPRE [EPOCA 1 · MISURA] / QUATTRO SIGILLI NON SONO PIU' RI-GIRABILI: il loro termine | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z40` | `SOSPESA` | la riga dice <<APERTO>> (la PRIMA parola di stato): la tensione esisteva in doc/ASSIOMI.md APERTO #2, oggi ha un numero) | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z55` | `SOSPESA` | la riga dice <<CHIUDE CHI>> (la PRIMA parola di stato): e. Nessuna delle due tocca i VALORI.) / Chiude chi misura da dov | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z59` | `SOSPESA` | la riga dice <<CHIUDE CHI>> (la PRIMA parola di stato): sistema degenerato la sta riempiendo. / Chiude chi misura se il  | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z6` | `SOSPESA` | NESSUNA parola decide: / Z6 VALE SEMPRE [EPOCA 1 · MISURA] / IL TRANSITORIO DI ACCENSIONE E' UN BLOCCO STRUTTURALE — ha  | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z7` | `SOSPESA` | la riga dice <<SI CHIUDE QUANDO>> (la PRIMA parola di stato): be cs^-4) non rompe nessun consumatore. Si chiude quando ① | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z71` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): _CRIT, cioe' un dato sulla TORSIONE). / APERTA, e la decisione e' di | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z75` | `SOSPESA` | la riga dice <<CHIUDE CHI>> (la PRIMA parola di stato): modo di saperlo. CRITERIO DI CHIUSURA: chiude chi registra nsub  | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z76` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): originali — sei ordini di grandezza. / APERTA. NON e' un difetto dic | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z78` | `SOSPESA` | la riga dice <<SI CHIUDE QUANDO>> (la PRIMA parola di stato): saturo in tutti i campioni. Questa voce si chiude quando L | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z8` | `SOSPESA` | NESSUNA parola decide: / Z8 VALE SEMPRE [EPOCA 1 · MISURA] / Lo 0.3457 % di nodi ancora al pavimento 1e-6 NON e' caratte | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z80` | `SOSPESA` | la riga dice <<CHIUDE CHI>> (la PRIMA parola di stato): due e' misurata). CRITERIO DI CHIUSURA: chiude chi deriva la sca | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z81` | `SOSPESA` | la riga dice <<CHIUDE CHI>> (la PRIMA parola di stato): curare il fratello S09: si REGISTRA»). CHIUDE chi decide se il t | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z83` | `SOSPESA` | la riga dice <<DOMANDA APERTA>> (la PRIMA parola di stato): / Z83 VALE SEMPRE [EPOCA 1 · MISURA] / DOMANDA APERTA: d0 DE | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z84` | `SOSPESA` | la riga dice <<CHIUDE CHI>> (la PRIMA parola di stato): venga la LORO tensione non e' misurato. CHIUDE chi risale la cat | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |
| `Z85` | `SOSPESA` | la riga dice <<APERTA>> (la PRIMA parola di stato): CHI_DA_SPINORE (→ resta su perc_chi). / APERTA — serve UNA decisione | *chiusa nell'era 1 (stato `chiuso` al tag era-1-secondo-ordine)* |

### ⚠ **E TRE DELLE `40` SONO I HOOK** — `H-FILE`, `H-NON-TRACCIATI`, `H-STASH`: non hanno riga d'origine, e la loro `chiusura` era ### **un residuo della migrazione.** Il punto `4` del mandato precedente li ha portati ad `APERTA` perche' ### **sono IN VIGORE**, e la `chiusura` ### **e- rimasta.**

---

## ③ PUNTO `3` — **`superata_da` accetta anche una VOCE**

> ### ⛔ **LA MIA REGOLA DI IERI ERA MEZZA VERA.** Avevo rifiutato `S02` scrivendo *«una voce superata deve essere superata DA UNA DECISIONE, e un difetto non decide niente»*: ### **vero per una DECISIONE, falso per una PROMOZIONE.** `S02` e' ### **«PROMOSSO»** a `D31`, e *«promosso a»* ### **non e- «deciso da»**.

| | |
|---|---|
| `S02` | `DIFETTO`/`SOSPESA` → ### **`SUPERATA`**, `superata_da` = ### **`D31`** |
| `Z21` | ### ⚠ **NON applicata al punto `3`**: il file vecchio chiede `SUPERATA` ### **senza dire da che cosa**, e il `superata_da` lo porta ### **la terza lettura** *(`Z26`)*. Applicata al punto `5` |
| ### **e `F9` ammette `SUPERATA` per `ENTRAMBE`** | correggeva ### **un'altra mia strettezza**: avevo scritto *«`ENTRAMBE` ⇒ `APERTA` o `CHIUSA`»* ### **alla lettera del mandato.** ### ⭐ **«Superata» non e' «rimandata»: e' RISOLTA DA FUORI** |
| ### **il collaudo, nei due versi** | una VOCE → ### **accettata**; un id che non e' ne' decisione, ne' assioma, ne' voce → ### **rifiutato.** ### ⛔ **Senza il verso negativo la regola nuova non e' una regola: e' un PERMESSO** |

---

## ④ PUNTO `4` — **la nota di `G1`, e `C3` si allinea al file**

| | |
|---|---|
| la nota di `G1` | ### **TOLTA** *(`meta_togli`)*. Diceva *«correzione v3 blocco G2: FISICA/era 1/SOSPESA»* e la voce e' `CHIUSA` |
| ### **si toglie, non si riscrive** | la sua storia vive ### **in `storico.jsonl`**, quindi togliere la nota ### **non perde niente** — e ### **una domanda a cui si e' risposto non si riscrive: si TOGLIE** |
| `CLI-1` e `POTATURA-GUARDIE` | ### **vale il file**, e ### **lo conferma il guardiano.** Avevo scritto *«ho scelto la FORMA, non il merito»* e ### **l'ho portato a Luca**: ### ⭐ **una decisione portata a chi tocca e tornata indietro non e' piu' mia** |
| ### ⚠ **e un braccio di collaudo si sarebbe spento da se'** | il caso *«`F6` DEVE scattare su `G1`»* ### **legge la nota**, e il punto `4` ### **la toglie.** Ancorato a `7e4c59c`, piu' il braccio che prova che ### **sulla `G1` di oggi `F6` tace.** ### **Un caso a risposta nota e' una FOTO, non uno specchio** |

---

## ⑤ PUNTO `5` — **la terza lettura**, riga per riga tutte e `59`

| verdetto | quante |
|---|--:|
| ### **`APPLICATA`** | ### **`47`** |
| ### **`NON_APPLICATA`** | ### **`11`** |
| ### **`NIENTE_DA_FARE`** | ### **`1`** |
| ### **in tutto** | ### **`59`** — e DEVE fare `59` |

| livello | quante |
|---|--:|
| `T0` | `10` |
| `T1` | `8` |
| `T3` | `5` |
| `T4` | `25` |

### ⛔ **TRE DIFETTI MIEI, E NESSUNO L'HO TROVATO IO**

| | il difetto | chi l'ha trovato |
|---|---|---|
| `1` | ### **`superata_da` giudicato come campo INDIPENDENTE**: `Z21` e `L-SOGLIA` hanno perso ### **entrambi** i campi — il `superata_da` cadeva per *«in `T3` non basta»*, e poi lo `stato` cadeva per ### **«SUPERATA senza dire da che cosa»**, cioe' ### **per la mancanza del campo che avevo appena scartato io** | ### **lo schema**, rifiutando |
| `2` | ### **la regola di `superata_da` era DUPLICATA**: la copia nell'applicatore diceva *«ne' decisione, ne' assioma»* e il validatore ### **accettava gia' una voce** | ### **il rifiuto stesso**, che citava ### **una ragione che il repo aveva smesso di avere** |
| `3` | ### **la `chiusura` restava piena su una voce che usciva da `CHIUSA`**: `L-SOGLIA` passava a `SUPERATA` ### **portandosi dietro il commit di chiusura** | ### **`F12`**, acceso ### **due commit prima**, rifiutando il lotto ### **senza scrivere niente** |

### ⭐ **E IL TERZO E' LA PROVA CHE I PRESIDI SERVONO:** `F12` l'ho scritto ### **stamattina**, e ### **mi ha fermato nel pomeriggio su un caso che non avevo previsto.**

### ✔ **E LE DUE CORREZIONI DEL GUARDIANO A SE' STESSO**

| | la correzione | che cosa cambia |
|---|---|---|
| `(a)` | la classe `(B)` del censimento e' ### **«COSTRUITA E MAI MISURATA»**, non testo falso | le `13` `CENS-B*` sono ### **FRONTI aperti.** ### **Io leggevo «censimento delle intenzioni» come «il testo dichiara il falso»** |
| `(b)` | `REGISTRO_FISICA:P*` sono ### **PREVISIONI, non esiti** | `6` voci a ### **`CRITERIO`/`METODO`.** ### ⭐ **E questo spiega perche' la riga di `P2` dice «P2 E' FALLITA»: non e' l'esito di una misura, e' IL CONFRONTO fra la previsione e la misura** |

### **LE `47` APPLICATE**

| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |
|---|---|---|---|---|---|
| `Z7` | `classe=DIFETTO stato=CHIUSA` | *① CABLATA* | `alta` | `FRONTE`/`INFRASTRUTTURA`/`SOSPESA` → ### **`DIFETTO`/`INFRASTRUTTURA`/`CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T3` (alta) |
| `RAMI-OFF-CURA2` | `classe=CURA stato=CHIUSA` | *COPIATI DAL SORGENTE* | `media` | `DIFETTO`/`INFRASTRUTTURA`/`SOSPESA` → ### **`CURA`/`INFRASTRUTTURA`/`CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T4` (media) |
| `INDICE-LEGGERO` | `stato=CHIUSA` | *IL TITOLO BREVE DEV'ESSERE BREVE* | `media` | `FRONTE`/`INFRASTRUTTURA`/`APERTA` → ### **`FRONTE`/`INFRASTRUTTURA`/`CHIUSA`** | ['chiusura', 'stato'] in `T4` (media) |
| `B7-SHAKE` | `stato=CHIUSA` | *la precessione mutua non organizza* | `media` | `MISURA`/`FISICA`/`SOSPESA` → ### **`MISURA`/`FISICA`/`CHIUSA`** | ['chiusura', 'stato'] in `T0` (media) |
| `Z24` | `stato=CHIUSA` | *Z24 CHIUSA* | `media` | `FRONTE`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`CHIUSA`** | ['chiusura', 'stato'] in `T3` (media) |
| `Z21` | `stato=SUPERATA superata_da=Z26` | *era UN SEME* | `media` | `MISURA`/`FISICA`/`SOSPESA` → ### **`MISURA`/`FISICA`/`SUPERATA`** | ['stato', 'superata_da'] in `T3` (media) |
| `L-SOGLIA` | `stato=SUPERATA superata_da=P1-sexies` | *fusa dentro* | `media` | `STANDARD`/`METODO`/`APERTA` → ### **`STANDARD`/`METODO`/`SUPERATA`** | ['chiusura', 'stato', 'superata_da'] in `T4` (media) |
| `P4` | `classe=STANDARD` | *LIBERA di cambiare* | `alta` | `PRESIDIO`/`METODO`/`APERTA` → ### **`STANDARD`/`METODO`/`APERTA`** | ['classe'] in `T0` (alta) |
| `P5` | `classe=STANDARD` | *va CONTATO* | `alta` | `PRESIDIO`/`METODO`/`APERTA` → ### **`STANDARD`/`METODO`/`APERTA`** | ['classe'] in `T0` (alta) |
| `L-MEMORIA-PRIMA` | `classe=STANDARD` | *LA REGOLA PERMANENTE* | `alta` | `PRESIDIO`/`METODO`/`APERTA` → ### **`STANDARD`/`METODO`/`APERTA`** | ['classe'] in `T1` (alta) |
| `P1-bis` | `classe=STANDARD` | *LA RELAZIONE SI SCRIVE NELLO STESSO COMMIT* | `media` | `PRESIDIO`/`METODO`/`APERTA` → ### **`STANDARD`/`METODO`/`APERTA`** | ['classe'] in `T0` (media) |
| `CENS-B1` | `classe=FRONTE` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T4` (alta) |
| `CENS-B2` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B3` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B5` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B6` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B7` | `classe=FRONTE` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T4` (alta) |
| `CENS-B9` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B10` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B11` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B12` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B13` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B14` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `CENS-B15` | `classe=FRONTE dominio=FISICA` | *COSTRUITA E MAI MISURATA* | `alta` | `DIFETTO`/`DOCUMENTAZIONE`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `REG-B` | `classe=FRONTE dominio=METODO era=1 stato=SOSPESA` | *RESTANO* | `media` | `DIFETTO`/`DOCUMENTAZIONE`/`APERTA` → ### **`FRONTE`/`METODO`/`SOSPESA`** | ['classe', 'dominio', 'era', 'stato'] in `T1` (media) |
| `REG-C` | `classe=FRONTE dominio=METODO era=1 stato=SOSPESA` | *FASE C* | `media` | `DIFETTO`/`DOCUMENTAZIONE`/`APERTA` → ### **`FRONTE`/`METODO`/`SOSPESA`** | ['classe', 'dominio', 'era', 'stato'] in `T0` (media) |
| `REGISTRO_FISICA:P1` | `classe=CRITERIO dominio=METODO` | *LE PREVISIONI ANALITICHE* | `alta` | `MISURA`/`FISICA`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`SOSPESA`** | ['classe', 'dominio'] in `T3` (alta) |
| `REGISTRO_FISICA:P2` | `classe=CRITERIO dominio=METODO` | *LE PREVISIONI ANALITICHE* | `alta` | `MISURA`/`FISICA`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`CHIUSA`** | ['classe', 'dominio'] in `T4` (alta) |
| `REGISTRO_FISICA:P3` | `classe=CRITERIO dominio=METODO` | *LE PREVISIONI ANALITICHE* | `alta` | `MISURA`/`FISICA`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`CHIUSA`** | ['classe', 'dominio'] in `T4` (alta) |
| `REGISTRO_FISICA:P3b` | `classe=CRITERIO dominio=METODO` | *LE PREVISIONI ANALITICHE* | `alta` | `MISURA`/`FISICA`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`SOSPESA`** | ['classe', 'dominio'] in `T3` (alta) |
| `REGISTRO_FISICA:P4` | `classe=CRITERIO dominio=METODO` | *LE PREVISIONI ANALITICHE* | `alta` | `MISURA`/`FISICA`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `REGISTRO_FISICA:P5` | `classe=CRITERIO dominio=METODO` | *LE PREVISIONI ANALITICHE* | `alta` | `MISURA`/`FISICA`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`SOSPESA`** | ['classe', 'dominio'] in `T4` (alta) |
| `M1` | `classe=FRONTE` | *È una domanda di ontologia* | `media` | `DIFETTO`/`FISICA`/`AGENDA` → ### **`FRONTE`/`FISICA`/`AGENDA`** | ['classe'] in `T1` (media) |
| `CELLE-NAN-APPESE-NOME-SCADUTO` | `classe=DIFETTO` | *NOME SCADUTO* | `media` | `FRONTE`/`INFRASTRUTTURA`/`SOSPESA` → ### **`DIFETTO`/`INFRASTRUTTURA`/`SOSPESA`** | ['classe'] in `T0` (media) |
| `COMPONENTI:D1` | `classe=CURA` | *5/5 PASS* | `media` | `MISURA`/`FISICA`/`CHIUSA` → ### **`CURA`/`FISICA`/`CHIUSA`** | ['classe'] in `T0` (media) |
| `COMPONENTI:D2` | `classe=CURA` | *6/6 PASS* | `media` | `MISURA`/`FISICA`/`CHIUSA` → ### **`CURA`/`FISICA`/`CHIUSA`** | ['classe'] in `T0` (media) |
| `D09` | `classe=MISURA` | *il difetto NON C'E'* | `media` | `DIFETTO`/`FISICA`/`CHIUSA` → ### **`MISURA`/`FISICA`/`CHIUSA`** | ['classe'] in `T4` (media) |
| `S10` | `classe=MISURA` | *RITIRATA* | `media` | `DIFETTO`/`FISICA`/`CHIUSA` → ### **`MISURA`/`FISICA`/`CHIUSA`** | ['classe'] in `T0` (media) |
| `REG-V` | `classe=FRONTE` | *col collaudo* | `media` | `DIFETTO`/`INFRASTRUTTURA`/`APERTA` → ### **`FRONTE`/`INFRASTRUTTURA`/`APERTA`** | ['classe'] in `T4` (media) |
| `REG-R` | `dominio=METODO` | *l'hook che RIFIUTA* | `media` | `PRESIDIO`/`INFRASTRUTTURA`/`APERTA` → ### **`PRESIDIO`/`METODO`/`APERTA`** | ['dominio'] in `T1` (media) |
| `CURA-3` | `classe=FRONTE` | *scheda da scrivere* | `media` | `CURA`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T1` (media) |
| `COPPIA-RAMP` | `classe=FRONTE` | *Aperta come domanda, NON come cura* | `media` | `MISURA`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T1` (media) |
| `A3-CHIRALE` | `classe=FRONTE` | *una decisione di FISICA* | `media` | `DIFETTO`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T1` (media) |
| `CARICA-ROTAZIONE` | `classe=FRONTE` | *LA MISURA IN CODA* | `media` | `MISURA`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T4` (media) |
| `MITOSI-TASSO` | `classe=FRONTE` | *CRITERIO DI CHIUSURA: misurare* | `media` | `MISURA`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T1` (media) |
| `FILI-CORTI` | `classe=FRONTE` | *o OVUNQUE?* | `media` | `DIFETTO`/`FISICA`/`SOSPESA` → ### **`FRONTE`/`FISICA`/`SOSPESA`** | ['classe'] in `T0` (media) |
| `POTATURA-GUARDIE` | `classe=FRONTE` | *la pulizia SI RIMANDA* | `media` | `CURA`/`INFRASTRUTTURA`/`SOSPESA` → ### **`FRONTE`/`INFRASTRUTTURA`/`SOSPESA`** | ['classe'] in `T4` (media) |

### **LE `11` NON APPLICATE**

| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |
|---|---|---|---|---|---|
| `DRIVER-SCENA-II` | `classe=CURA stato=CHIUSA` | *6/6 PASS* | `alta` | `DIFETTO`/`INFRASTRUTTURA`/`SOSPESA` → ### **`DIFETTO`/`INFRASTRUTTURA`/`SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/STATO_RUN.md` |
| `M0a` | `classe=MISURA stato=CHIUSA` | *3/3 come atteso* | `media` | `DIFETTO`/`INFRASTRUTTURA`/`SOSPESA` → ### **`DIFETTO`/`INFRASTRUTTURA`/`SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `csv/_test_fork/_misura0_scena_ii.py` |
| `REGISTRO_FISICA:V8` | `stato=CHIUSA` | *LA MISURA CHE L'HA DECISA* | `media` | `CRITERIO`/`METODO`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`SOSPESA`** | ### COMPARE NEL FILE `doc/REGISTRO_FISICA.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `REGISTRO_FISICA:V9` | `stato=CHIUSA` | *LA MISURA CHE L'HA DECISA* | `media` | `CRITERIO`/`METODO`/`SOSPESA` → ### **`CRITERIO`/`METODO`/`SOSPESA`** | ### COMPARE NEL FILE `doc/REGISTRO_FISICA.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `Z119` | `classe=MISURA` | *non si corregge prima della decisione di Luca* | `media` | `DIFETTO`/`FISICA`/`CHIUSA` → ### **`DIFETTO`/`FISICA`/`CHIUSA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/RAMIFICAZIONI.md` |
| `ETC-PASSO` | `stato=SUPERATA superata_da=SCHED-PASSO` | *chiusa come superata il 2026-09-28* | `alta` | `CURA`/`FISICA`/`CHIUSA` → ### **`CURA`/`FISICA`/`CHIUSA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/TASK_HISTORY/2026-09-27_etc-passo.md` |
| `P6` | `classe=STANDARD stato=SUPERATA superata_da=P3` | *fuse dentro* | `alta` | `PRESIDIO`/`METODO`/`APERTA` → ### **`PRESIDIO`/`METODO`/`APERTA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `CLAUDE.md` |
| `STANDARD-8` | `stato=SUPERATA superata_da=A12` | *e non si duplica* | `media` | `STANDARD`/`METODO`/`APERTA` → ### **`STANDARD`/`METODO`/`APERTA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/ASSIOMI.md` |
| `STANDARD-6` | `stato=SUPERATA superata_da=H-INDICE` | *il hook* | `media` | `STANDARD`/`METODO`/`APERTA` → ### **`STANDARD`/`METODO`/`APERTA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/INDICE_ID.tsv` |
| `P3` | `classe=STANDARD` | *del hook* | `alta` | `PRESIDIO`/`METODO`/`APERTA` → ### **`PRESIDIO`/`METODO`/`APERTA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `CLAUDE.md` |
| `M-SPINORE` | `classe=FRONTE` | *è un fronte, non una cura* | `alta` | `CURA`/`FISICA`/`AGENDA` → ### **`CURA`/`FISICA`/`AGENDA`** | ### COMPARE NEL FILE `doc/MEMORIE_MANCANTI.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |

### **NIENTE DA FARE**

| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |
|---|---|---|---|---|---|
| `S02` | `stato=SUPERATA superata_da=D31` | *PROMOSSO* | `alta` | `DIFETTO`/`FISICA`/`SOSPESA` → ### **`DIFETTO`/`FISICA`/`SUPERATA`** | `stato` e- GIA- `SUPERATA`; `superata_da` e- GIA- `D31` |

---

## ⑥ I CONTEGGI E I CONTROLLI

> **PRIMA** = `git show c24bbd5` *(il task history, prima di ogni scrittura del giro)*. **DOPO** = il disco. ### **Nessun numero ricopiato.**

| `classe` | prima | dopo | |
|---|--:|--:|---|
| DIFETTO | `207` | `187` | ### **-20** |
| NON_DEFINITA | `187` | `187` |  |
| MISURA | `155` | `146` | ### **-9** |
| FRONTE | `87` | `109` | ### **+22** |
| CRITERIO | `90` | `96` | ### **+6** |
| CURA | `55` | `56` | ### **+1** |
| STANDARD | `38` | `42` | ### **+4** |
| PRESIDIO | `27` | `25` | ### **-2** |

| `dominio` | prima | dopo | |
|---|--:|--:|---|
| FISICA | `372` | `377` | ### **+5** |
| METODO | `205` | `216` | ### **+11** |
| DA_CLASSIFICARE | `187` | `187` |  |
| INFRASTRUTTURA | `53` | `52` | ### **-1** |
| DOCUMENTAZIONE | `29` | `16` | ### **-13** |

| `era` | prima | dopo | |
|---|--:|--:|---|
| 1 | `537` | `539` | ### **+2** |
| DA_CLASSIFICARE | `188` | `188` |  |
| ENTRAMBE | `97` | `97` |  |
| 2 | `24` | `24` |  |

| `stato` | prima | dopo | |
|---|--:|--:|---|
| SOSPESA | `374` | `325` | ### **-49** |
| CHIUSA | `169` | `221` | ### **+52** |
| DA_CLASSIFICARE | `188` | `188` |  |
| APERTA | `90` | `86` | ### **-4** |
| AGENDA | `24` | `24` |  |
| SUPERATA | `1` | `4` | ### **+3** |

| | prima | dopo |
|---|--:|--:|
| voci | `846` | ### **`848`** *(`2` NUOVE: i due presidi)* |
| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |
| ### **righe di storico** | `1764` | ### **`1903`** |
| ### **`chiusura` ORFANE** | `42` | ### **`0`** *(`F12` le vieta)* |
| ### **voci non allineate allo storico** | ### **non misurato** | ### **`0`** *(`F11` le vieta)* |

| presidio | segnali |
|---|--:|
| `F1` | ### **`8`** |
| `F2` | `0` |
| `F3` | ### **`1`** |
| `F4` | `0` |
| `F6` | ### **`2`** |
| `F8` | ### **`20`** |
| `F5` `F7` `F9` `F10` `F11` `F12` | ### **`0`** — sono ERRORI: se non fossero zero, `valida` ### **non passerebbe** |
| ### **in tutto** | ### **`31`** |

| `F1` | il segnale |
|---|---|
| `D05` | il titolo cita `C5`, che e- `FISICA`/era `1`, mentre questa e- `INFRASTRUTTURA`/era `1` |
| `D06` | il titolo cita `Z7`, che e- `INFRASTRUTTURA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `D08` | il titolo cita `Z14`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `D14` | il titolo cita `Z41`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `D18` | il titolo cita `Z92`, che e- `FISICA`/era `1`/`SOSPESA`, mentre questa e- `FISICA`/era `1`/`CHIUSA` |
| `D19` | il titolo cita `Z88`, che e- `METODO`/era `1`/`SOSPESA`, mentre questa e- `FISICA`/era `1`/`CHIUSA` |
| `D27` | il titolo cita `Z65`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `Z130` | il titolo cita `S10`, che e- `FISICA`/era `1`, mentre questa e- `METODO`/era `1` |

| `F3` | il segnale |
|---|---|
| `CENS-B15` | `FISICA`, ma il titolo parla di strumenti: `commento` |

| `F6` | il segnale |
|---|---|
| `POTATURA-GUARDIE` | la nota nomina la lista `3` del guardiano e la voce NON e- piu- cio- che quella lista diceva: la lista diceva `FISICA`, la voce e- `INFRASTRUTTURA` |
| `REGISTRO_FISICA:U2-6` | la nota DICHIARA una tripla `dominio/era/stato` e la voce non e- piu- quella: la nota dichiara `SOSPESA`, la voce e- `CHIUSA` |

| `F8` | il segnale |
|---|---|
| `A7b` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<calcola_psi>>) |
| `A8` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<mitosi>>) |
| `A8b` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>) |
| `A9` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_presidio.py>>) |
| `CONTA-RIGHE` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_struttura_regole.py>>) |
| `FINESTRA-PRE-NASCITA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<perc_geom>>) |
| `H-FILE` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un flag `--...` (<<--cached>>); un file `.py` del repo (<<_hook_file_cambiati.py>>) |
| `H-FISICA-FUORI-LISTA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_file_fisica.py>>) |
| `H-ID-OBBLIGATORIO` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un flag `--...` (<<--collaudo>>); un file `.py` del repo (<<_file_fisica.py>>) |
| `H-P9` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<net.step>>) |
| `INDICE-COLLAUDO-SCRITTURA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<indice.py>>) |
| `NON-TRACCIATI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un `.pkl` (<<.pkl>>); un file `.py` del repo (<<_censimento_non_tracciati.py>>) |
| `PASSO-PIENO` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<net.step>>); un file `.py` del repo (<<_passo.py>>) |
| `PIATTAFORMA-NON-TIMBRATA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>); un file `.py` del repo (<<_confronto_blob_misure.py>>) |
| `PRESIDIO-RIFIUTO-SOLO-SIGILLI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>); un file `.py` del repo (<<_presidio.py>>) |
| `REG-R` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<soliton_simulator.py>>) |
| `REG-V` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<verificaregistro.py>>) |
| `REPERTI-IMMUTABILI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_seal_fork>>); un file `.py` del repo (<<_sim_A.py>>) |
| `RIPRESA-ARGV` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: il sigillo di una cura (<<sigillo della cura>>) |
| `Z125` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<mitosi>>) |

---

## ⑦ CHE COSA RESTA A LUCA

| | quante | che cosa |
|---|--:|---|
| ### **le frasi GENERICHE** | `9` | il commit c'e', ### **ma la frase compare in piu' di tre righe del file**: se le vuoi piu' strette, servono ### **citazioni piu' lunghe** |
| ### **la chiusura dal TAG** | `1` | `MITOSI-2LAM-ACCESO`: la frase e' nel file ### **ma `git log -S` non la trova nella storia** |
| ### **le `11` NON APPLICATE** della terza lettura | `11` | la citazione ### **non compare**, o compare ### **fuori dalla sezione** della voce |
| ### **i segnali che restano** | `31` | `F1`=`8` `F3`=`1` `F6`=`2` `F8`=`20`, ### **elencati e non corretti** |
| ### **`H-FISICA-FUORI-LISTA`** | `1` | ### **non impedisce niente finche' la cartella dell'era `2` e' vuota** — e ### **il nome lo decidi tu** *(`doc/REFERTO_strumenti_era2.md`)* |

> ### ⭐ **Il criterio, lo stesso di tutto il giro:** dove ### **la storia di git sa la risposta** l'ho cercata invece di rinunciare; dove ### **due campi si contraddicono** ho chiesto ### **al documento**; dove ### **il guardiano contraddice se stesso** ho portato la domanda e ### **ho aspettato la conferma.** ### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un difetto.**

