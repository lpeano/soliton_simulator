# IL REFERTO DEI PRESIDI CONTRO LE MESCOLANZE

> ### ⛔ **I presidi SEGNALANO, non decidono**, e il mandato lo dice. ### **I segnali che trovano sull'indice vero NON si correggono: si elencano.** Questo referto e' quell'elenco.

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_presidi.md`, ### **committato PRIMA del lavoro** *(`e00d2ae`)* |
| **il blocco `G`** | `a6ba839` |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |
| **i presidi** | ### **`6`**: `F1`–`F4` e `F6` ### **segnalano**, `F5` e' ### **un ERRORE** |
| **i segnali sull'indice vero** | ### **`103`** su `830` voci |
| **il collaudo** | ### **`15` su `15`** — i `12` fissati nel task history *(`6` presidi × `2` bracci)* piu' `3` sulla ### **forma dell'eccezione** |

---

## ① IL COLLAUDO — **ogni presidio si e' visto SCATTARE**

> ### ⛔ **`P1-sexies`: un presidio che non si e' visto scattare non protegge niente** (`A9`). ### **Due bracci per ciascuno:** il caso che ### **DEVE** scattare, e la voce ### **corretta che NON deve** — altrimenti e' un ### **FALSO-UNO.**

### ⛔ **E MAI SULL'INDICE VERO.** Lo stato di prima si legge con `git show <commit>:<path>`, le liste vivono ### **in memoria**, e `F5` ha ### **una funzione PURA** *(`_f5_righe`)* ### **che esiste proprio per questo.** ### ⚠ **La ragione non e' teorica:** nel giro scorso un controllo che per verificare ### **rilanciava il suo oggetto** mi ha cancellato ### **`867` classificazioni.**

```
  F1  DEVE scattare: B2 cita Z31, e Z31 era FISICA/era 1         PASSA   il titolo di B2 dice <<Z31 -- i sigilli non ri-girabili | Z31, ...>>
  F1  NON deve scattare: con Z31 corretta (METODO/ENTRAMBE)      PASSA
  F2  DEVE scattare: D35 era era 2 e nel titolo ha (:5443)       PASSA   era `2` a 6e5e75b
  F2  NON deve scattare: D35 corretta (era 1)                    PASSA
  F3  DEVE scattare: C28 era FISICA e il titolo dice <<ALCUN SIGILLO>> PASSA   dominio `FISICA` a 6e5e75b
  F3  NON deve scattare: C28 corretta (METODO)                   PASSA
  F4  DEVE scattare: TW-1 era un'etichetta, ed e' DEFINITA in un documento PASSA   doc/SCALE_TW_lettura.md la definisce con una riga di tabella
  F4  NON deve scattare: TW-1 oggi NON e' fra le etichette       PASSA
  F5  DEVE essere un ERRORE: riga 2 GIA' COMMITTATA e senza commit PASSA   n_head=2 -> la riga 2 e' committata, la 3 e' IL RITARDO e NON si segnala
  F5  NON deve scattare: le righe oltre HEAD sono il RITARDO dichiarato PASSA
  F6  DEVE scattare: la nota dice lista 3 (FISICA/1/SOSPESA), la voce e' DOCUMENTAZIONE PASSA
  F6  NON deve scattare: con la nota della correzione v3         PASSA
  ECCEZIONE  DEVE essere un ERRORE: non cita il testo alla lettera PASSA
  ECCEZIONE  NON deve essere un errore: cita 40 caratteri del titolo PASSA
  ECCEZIONE  DEVE essere un ERRORE: fuori forma (manca `F<n>:`)  PASSA
```

---

## ② I SEGNALI, PRESIDIO PER PRESIDIO

| | che cosa guarda | segnali | su | ### **atteso** *(dal task history, PRIMA di misurare)* |
|---|---|--:|--:|---|
| ### **`F1`** | GEMELLE: il titolo cita l'ID di un'altra, e dominio o era differiscono | ### **`49`** | `830` | fra `10` e `60`; ### **troppo grosso oltre `83`** *(il `10%` di `830`)* |
| ### **`F2`** | ERA 2 PULITA: una voce dell'era 2 che nomina simboli dell'era 1 | ### **`9`** | `25` | *«pochi»* — solo `25` voci sono era `2` |
| ### **`F3`** | FISICA CHE PARLA DI STRUMENTI: il titolo di una voce FISICA | ### **`15`** | `439` | *«molti»*; ### **troppo grosso oltre `44`** *(il `10%` di `439`)* |
| ### **`F4`** | ETICHETTA CON DEFINIZIONE: un'etichetta che un documento DEFINISCE | ### **`30`** | `122` | fra `10` e `28`; ### **sotto `12` il rilevatore e' ROTTO**, non l'indice |
| ### **`F6`** | NOTE COERENTI: una nota che nomina una lista e la contraddice | ### **`0`** | `117` | ### **zero**, perche' il blocco `G3` corregge le note PRIMA |
| ### **`F5`** | una riga di storico ### **gia' committata** e senza `commit` — ### **E' UN ERRORE** | ### **`0`** | `1089` | ### **zero** |

### `F1` — **49 segnali su 830**

### ✔ **NON troppo grosso** *(`49` contro `83`)*, e la previsione `10`–`60` regge. ### ⚠ **Ma `12` dei `49` puntano a una voce `DA_CLASSIFICARE`:** un segnaposto ### **non ha ancora un dominio ne' un'era**, quindi *«differiscono»* e' vero per costruzione. ### **Non e' un falso in senso stretto** — un titolo che cita un ID non definito e' un fatto — ma ### **non e' la mescolanza che `F1` cerca.** Lo scrivo e non lo cambio: ### **il mandato dice che i segnali si elencano, non si correggono**, e restringere il rilevatore sarebbe una decisione.

| id | `dominio`/era/stato | il segnale |
|---|---|---|
| `A2-ANELLO` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A6`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `A8b` | `METODO`/`ENTRAMBE`/`APERTA` | il titolo cita `CROSS'PASSO`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `METODO`/era `ENTRAMBE` |
| `AB-CONTROLLI` | `METODO`/`ENTRAMBE`/`APERTA` | il titolo cita `W5`, che e' `FISICA`/era `1`, mentre questa e' `METODO`/era `ENTRAMBE` |
| `C5-INVARIANTI` | `METODO`/`ENTRAMBE`/`CHIUSA` | il titolo cita `C5`, che e' `FISICA`/era `1`, mentre questa e' `METODO`/era `ENTRAMBE` |
| `C5RES-INVARIANTI` | `FISICA`/`1`/`SOSPESA` | il titolo cita `I4`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `COLLAUDO-NON-ESEGUITO` | `METODO`/`ENTRAMBE`/`APERTA` | il titolo cita `C4`, che e' `FISICA`/era `1`, mentre questa e' `METODO`/era `ENTRAMBE` |
| `COMPONENTI:A6` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A6`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `COMPONENTI:A8` | `FISICA`/`1`/`SOSPESA` | il titolo cita `Y5`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `COMPONENTI:Y0-Y10` | `FISICA`/`1`/`CHIUSA` | il titolo cita `Y10`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `D05` | `FISICA`/`1`/`SOSPESA` | il titolo cita `I4`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `D05` | `FISICA`/`1`/`SOSPESA` | il titolo cita `I5`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `D18` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A5`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `D24` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A2`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `E3` | `FISICA`/`1`/`SOSPESA` | il titolo cita `M4`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `E3` | `FISICA`/`1`/`SOSPESA` | il titolo cita `M1`, che e' `FISICA`/era `2`, mentre questa e' `FISICA`/era `1` |
| `ETICHETTA-A13` | `DOCUMENTAZIONE`/`ENTRAMBE`/`CHIUSA` | il titolo cita `A3'DISEGNO`, che e' `FISICA`/era `2`, mentre questa e' `DOCUMENTAZIONE`/era `ENTRAMBE` |
| `ETICHETTA-A13` | `DOCUMENTAZIONE`/`ENTRAMBE`/`CHIUSA` | il titolo cita `A13`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `DOCUMENTAZIONE`/era `ENTRAMBE` |
| `FUGA-MULTIRIGA` | `INFRASTRUTTURA`/`ENTRAMBE`/`APERTA` | il titolo cita `H'P1'bis`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `INFRASTRUTTURA`/era `ENTRAMBE` |
| `FUGA-MULTIRIGA` | `INFRASTRUTTURA`/`ENTRAMBE`/`APERTA` | il titolo cita `H'REG'R`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `INFRASTRUTTURA`/era `ENTRAMBE` |
| `H-REGR-LARGA` | `INFRASTRUTTURA`/`ENTRAMBE`/`APERTA` | il titolo cita `H'REG'R`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `INFRASTRUTTURA`/era `ENTRAMBE` |
| `M-MASSA` | `FISICA`/`2`/`AGENDA` | il titolo cita `MASSA'ID`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `2` |
| `POTENZE-1` | `FISICA`/`1`/`CHIUSA` | il titolo cita `F1`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `POTENZE-1` | `FISICA`/`1`/`CHIUSA` | il titolo cita `F2`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `PRESIDIO-RIFIUTO-SOLO-SIGILLI` | `INFRASTRUTTURA`/`ENTRAMBE`/`APERTA` | il titolo cita `A9`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `INFRASTRUTTURA`/era `ENTRAMBE` |
| `REGISTRO_FISICA:A13` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A13`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `REGISTRO_FISICA:A4` | `FISICA`/`1`/`SOSPESA` | il titolo cita `P3`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `REGISTRO_FISICA:A4` | `FISICA`/`1`/`SOSPESA` | il titolo cita `P2`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `REGISTRO_FISICA:A6` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A2`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `REGISTRO_FISICA:S2` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A13`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `REGISTRO_FISICA:U2-6` | `METODO`/`1`/`SOSPESA` | il titolo cita `P1'sexies`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `METODO`/era `1` |
| `RIORDINO-NOMI-H` | `DOCUMENTAZIONE`/`ENTRAMBE`/`CHIUSA` | il titolo cita `H'P3`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `DOCUMENTAZIONE`/era `ENTRAMBE` |
| `S09-MEDIANA` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A2`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `SCHW-SOTTO-LAM` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A13`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `TS-1` | `METODO`/`1`/`SOSPESA` | il titolo cita `A13`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `METODO`/era `1` |
| `TS-5` | `METODO`/`1`/`SOSPESA` | il titolo cita `P1'sexies`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `METODO`/era `1` |
| `TW-5` | `METODO`/`1`/`SOSPESA` | il titolo cita `P1'sexies`, che e' `METODO`/era `ENTRAMBE`, mentre questa e' `METODO`/era `1` |
| `Z100` | `METODO`/`ENTRAMBE`/`CHIUSA` | il titolo cita `C5`, che e' `FISICA`/era `1`, mentre questa e' `METODO`/era `ENTRAMBE` |
| `Z127` | `FISICA`/`1`/`SOSPESA` | il titolo cita `E1`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `Z16` | `FISICA`/`1`/`CHIUSA` | il titolo cita `Y5`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `FISICA`/era `1` |
| `Z17` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A6`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z2` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A1`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z2` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A3`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z2` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A2`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z40` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A2`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z5` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A3`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z5` | `FISICA`/`1`/`SOSPESA` | il titolo cita `A2`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z70` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A6`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z71` | `FISICA`/`1`/`CHIUSA` | il titolo cita `A7`, che e' `FISICA`/era `ENTRAMBE`, mentre questa e' `FISICA`/era `1` |
| `Z86` | `METODO`/`ENTRAMBE`/`CHIUSA` | il titolo cita `Z4a`, che e' `DA_CLASSIFICARE`/era `DA_CLASSIFICARE`, mentre questa e' `METODO`/era `ENTRAMBE` |

---

### `F2` — **9 segnali su 25**

### ✔ **NON troppo grosso, e la soglia del `10%` qui NON VUOL DIRE NIENTE:** il `10%` di `25` e' `2,5`. ### **Una percentuale su un denominatore di `25` non e' una misura.** I `9` segnali sono ### **tutti veri**: `Nose-Hoover`, `phivel`, `M_PH`, `mem_mot`, `perc_chi`, `perc_geom`, `scuotimento`, `sync`, e ### **quattro numeri di riga** — e un numero di riga in una voce dell'era `2` e' ### **il segno piu' chiaro che quella voce parla ancora del vecchio codice.**

| id | `dominio`/era/stato | il segnale |
|---|---|---|
| `CONSERVAZIONE-LOCALE` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: Nose'Hoover |
| `ENERGIA-NON-DEFINITA` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: phivel, M_PH, un numero di riga `:6334` |
| `FRECCE-IMPOSTE` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: mem_mot, un numero di riga `:6554` |
| `GRAVITA-POTENZIALE` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: sync, un numero di riga `:9058` |
| `INVARIANZA-LOCALE-CS` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: un numero di riga `:7746` |
| `M-FLUSSO` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: mem_mot |
| `M-ISTERESI` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: perc_chi, perc_geom |
| `MASSE-PESI-SOVRAPPOSTE` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: un numero di riga `:4858` |
| `VUOTO-LOCALE-DETERMINISTICO` | `FISICA`/`2`/`AGENDA` | era `2` ma nomina l'era `1`: Nose'Hoover, scuotimento |

---

### `F3` — **15 segnali su 439**

### ✔ **NON troppo grosso** *(`15` contro `44`)*. La previsione diceva *«molti»* e ### **ho sbagliato**: temevo che la parola `criterio` facesse valanga, e invece ne porta `4`. ### **Il motivo e' che il mandato dice «il cui TITOLO»**, e il titolo e' `<= 100` caratteri: ### **guardare solo il titolo e' cio' che tiene `F3` stretto.** Se si guardasse anche la descrizione sarebbe un'altra cosa, e ### **non l'ho allargato da solo.**

| id | `dominio`/era/stato | il segnale |
|---|---|---|
| `A2-DXD` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `criterio` |
| `COMPONENTI:B1` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `commento` |
| `COMPONENTI:B10` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `criterio` |
| `D02` | `FISICA`/`1`/`CHIUSA` | `FISICA`, ma il titolo parla di strumenti: `docstring` |
| `G3` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `sigillo` |
| `POTENZE-1` | `FISICA`/`1`/`CHIUSA` | `FISICA`, ma il titolo parla di strumenti: `sigillo` |
| `RAMPA-1` | `FISICA`/`1`/`CHIUSA` | `FISICA`, ma il titolo parla di strumenti: `sigillo` |
| `REGISTRO_FISICA:A6` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `caso che deve fallire` |
| `REGISTRO_FISICA:C2` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `criterio` |
| `REGISTRO_FISICA:V6` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `caso che deve fallire` |
| `S08` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `docstring` |
| `SCHERMATURA-LEGGE-REVISIONE` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `commento` |
| `SCHWINGER-UN-NODO` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `commento` |
| `W5` | `FISICA`/`1`/`SOSPESA` | `FISICA`, ma il titolo parla di strumenti: `criterio` |
| `Z124` | `FISICA`/`1`/`CHIUSA` | `FISICA`, ma il titolo parla di strumenti: `sigillo` |

---

### `F4` — **30 segnali su 122**

### ✔ **Il rilevatore NON e' rotto** *(`30` ≥ `12`)*, e il numero e' sopra la previsione `10`–`28`. ### **`12` erano gia' noti** — sono quelli che il referto `v3` ha lasciato a Luca — e ### **`18` sono NUOVI.** La soglia del `10%` e' superata, ### **ma `F4` non e' troppo grosso: e' un ritrovato.** ### ⛔ **Nessuna di queste `30` si corregge qui**, e per la stessa ragione del giro scorso: ### **il mandato non dice con quale classe e dominio debbano nascere.**

| id | `dominio`/era/stato | il segnale |
|---|---|---|
| `ARCHI-PASSO` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:5110` |
| `AUTO-MANUTENZIONE` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/STORIA_REGOLE.md:479` |
| `CURA1-CORTO` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/STATO_RUN.md:1330` |
| `CURA2-CORTO` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/STATO_RUN.md:1353` |
| `D3` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:5177` |
| `D4` | *(etichetta rimossa)* | etichetta rimossa, ma una riga di tabella la DEFINISCE in `doc/CENSIMENTO_intenzioni.md:314` |
| `DA-DECIDERE` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:5025` |
| `DE-ACCOPPIABILITA` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/INDAGINE_scuotimento.md:156` |
| `DOMANDE-BUSSOLA` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/BUSSOLA_dev'spinoriale.md:50` |
| `F4` | *(etichetta rimossa)* | etichetta rimossa, ma una riga di tabella la DEFINISCE in `doc/relazioni/2026'09'21.md:3572` |
| `F5` | *(etichetta rimossa)* | etichetta rimossa, ma una riga di tabella la DEFINISCE in `doc/relazioni/2026'09'21.md:3573` |
| `FORK-FIRST` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `CLAUDECONNECT.md:469` |
| `GLOBALE-DIS` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/relazioni/2026'09'26.md:1068` |
| `H1` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:9416` |
| `H2` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:9540` |
| `H3` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:9492` |
| `MASSE-COERENTI` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:176` |
| `POST-HOC` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/REFERTO_due_masse.md:69` |
| `RI-ETICHETTATO` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/REPERTO_cs_dinamico_spento.md:97` |
| `RI-LETTO` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/REFERTO_Z36_cucitura.md:96` |
| `RI-VERIFICATI` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/PIANO_merge_main.md:55` |
| `ROMPI-ANELLO` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/REFERTO_frequenza_riferimento.md:1` |
| `S1` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:9345` |
| `S3` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:6312` |
| `SIGILLO-CURA2` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/STATO_RUN.md:1342` |
| `SIGILLO-CURA2-RIPARATO` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/STATO_RUN.md:1365` |
| `SOVRA-CORREGGE` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `CLAUDECONNECT.md:504` |
| `STEP2` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/REFERTO_z43_cura1_2026'10'05.md:56` |
| `T1` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `RELAZIONE_PER_CLAUDE.md:10431` |
| `TEMPO-LUCE` | *(etichetta rimossa)* | etichetta rimossa, ma un'intestazione la DEFINISCE in `doc/RAMPA2_chi_usa_il_tempo_luce.md:1` |

---

### `F6` — **0 segnali su 117**

### ✔ **Zero, esattamente come previsto**, e la previsione era scritta ### **prima**: *«`F6` dopo `G3` ⇒ zero; se segnala ancora, `G3` e' incompleto»*. ### **`G3` era completo.**

---

## ③ I DUE DIFETTI DEI PRESIDI, PRESI DAI PRESIDI STESSI

| | il difetto |
|---|---|
| `1` | ### ⛔ **`F6` LEGGEVA LA PROSA.** Cercava nella nota le parole `SUPERATA`, `SOSPESA`, `fisica`… e le prendeva per ### **asserzioni di stato**: ### **`11` dei `13` segnali erano UNA SOLA FRASE** — *«candidata ### **SUPERATA** dalla decisione sulla sincronizzazione»*, che e' ### **prosa.** ➜ Riscritto: confronta la voce con ### **cio' che la lista `N` DICEVA** *(`LISTE_GUARDIANO`, una tabella dichiarata)*, e ### **una nota che si dichiara «correzione» non si guarda** — segnalarla sarebbe un FALSO-UNO. ### **I segnali sono passati da `13` a `0`.** |
| `2` | ### ⚠ **L'etichetta «TROPPO GROSSO» era un GIUDIZIO stampato da un attrezzo.** La soglia del `10%` l'avevo fissata nel task history ### **prima di misurare**, ed e' un fatto utile; ma su un denominatore di `25` ### **una percentuale non e' una misura**, e `F2` risultava *«troppo grosso»* con `9` segnali ### **tutti veri.** ➜ L'attrezzo adesso dice ### **che la soglia e' superata** *(il fatto)*, e ### **la LETTURA sta qui** *(il giudizio)*. |

### ⭐ **Il primo l'ha trovato il presidio stesso**, guardando la propria uscita: ### **`13` segnali di cui `11` con la stessa frase non sono `13` difetti, sono un rilevatore che legge male.** ### **E' il controllo che chiede «quel segnale poteva essere diverso?»**, ed e' la domanda che tiene lontano un FALSO-UNO.

---

## ④ CHE COSA RESTA A LUCA

| | che cosa, e perche' non l'ho deciso io |
|---|---|
| ### **i `103` segnali** | ### **non si correggono**, lo dice il mandato. Ciascuno si chiude ### **correggendo la voce** oppure con ### **`meta.eccezione_presidio`**, che deve ### **citare il testo alla lettera** — e la forma la ### **impone `valida`**, altrimenti l'eccezione sarebbe una via di fuga a costo zero |
| ### **`F5`, la mia derivazione** | il mandato dice *«storico senza commit → errore»*. ### ⛔ **Nella forma letterale BLOCCHEREBBE OGNI COMMIT DI UN LOTTO**, perche' `aggiorna-lotto` scrive righe con `commit` vuoto — il commit che le conterra' ### **non esiste ancora.** ➜ **`F5` e' un errore solo per le righe GIA' COMMITTATE** *(quelle in `HEAD`)*; le altre sono ### **il ritardo dichiarato nel blocco `D`.** ### **E' una MIA derivazione, scritta nel task history PRIMA di provarla** |
| ### **`F3` guarda solo il titolo** | il mandato dice *«il cui ### **TITOLO** parla di…»*, e l'ho ### **preso alla lettera.** ### **E' cio' che tiene `F3` stretto** *(`15` segnali invece dei «molti» che prevedevo)*. Allargarlo alla descrizione ### **cambierebbe il presidio**, e non lo faccio da solo |
| ### **`F1` e i segnaposto** | `12` dei `49` segnali di `F1` puntano a una voce `DA_CLASSIFICARE`, che ### **non ha ancora un dominio ne' un'era.** Restringere il rilevatore e' una decisione: ### **lo scrivo, non lo cambio** |
| ### **il costo nel `pre-commit`** | `valida` adesso ### **conta i segnali a ogni commit**, e `F4` apre i documenti citati da `122` etichette: ### **circa `4,5` secondi.** Nel task history avevo scritto che oltre ### **`5` secondi** l'avrei proposto fuori dal `pre-commit`: ### **ci sta sotto, ma di poco** — se cresce, `F4` va spostato in un comando a parte |

> ### ⭐ **Il criterio, lo stesso del giro scorso:** dove il mandato ### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un difetto.**

