# IL CONFRONTO FRA LA TABELLA DELLE LEGGI E IL BANCO CONGELATO

> **Mandato di Luca, 2026-10-12:** *«E' il TERZO disallineamento della stessa famiglia.
> Non devono piu' venire fuori uno alla volta mentre si scrive il motore.»*
> ### ⛔ **Si fa UNA VOLTA, PRIMA del flusso di saturazione e PRIMA del criterio di
> passaggio.**

| | |
|---|---|
| **il riferimento del FATTO** | `proto_camminata/` *(il banco **congelato**)*, letto **DAL CODICE** e non dai commenti |
| **il riferimento della DECISIONE** | la carta della fisica *(`F1`..`F10`, `A1`..`A5`)* |
| ### ⚠ **come si citano le prove** | ### **PER NOME DI FUNZIONE, mai per riga** — i numeri di riga sono di blob vecchi e **sono shiftati** *(par.`2`)*, e `[[P-RIF]]` me le ha gia' rifiutate scritte a riga |
| **il collaudo che lo rifa'** | `python primo_ordine/_collauda_confronto.py` |
| **il presidio che lo IMPEDISCE** | **`P-E10`** in `csv/_presidi_era2.py`: una variabile in tabella **senza la sua riga qui** fa **rifiutare il commit** |

---

## I CONTEGGI, PER ESITO

| esito | variabili | leggi | operatori del banco | che cosa vuol dire |
|---|---|---|---|---|
| **`COINCIDE`** | `5` | `8` | — | tabella, banco e carta d'accordo |
| **`ERRORE DI TRASCRIZIONE`** | `0` *(era `1`, corretto)* | `0` | — | banco e carta d'accordo, tabella no ⟹ **si corregge la tabella** |
| **`CONFLITTO`** | `1` | `0` | — | ### ⛔ **NON si corregge: va a Luca** |
| **`MANCANTE`** | `0` | — | `12` | un operatore del banco **usato nelle misure** senza la sua legge |
| **`NUOVA`** | `1` | `3` | — | dell'era `2`, **senza riferimento**, col punto della carta |
| **`ORFANA`** | `0` | `0` | — | ### **si segnala e NON si toglie** |

### ⭐⭐ **E `rho` E' ENTRATA IN TABELLA IL `2026-10-15` (`23:30`), e NON E' <<NUOVA>>:**
la decisione di Luca che sostituisce la saturazione con `CAMM-MATERIA-VUOTO` prende come
sorgente la ### **densita' di materia**, e ### **il banco congelato CE L'HA GIA'** —
`camminata.rho_nodo`, che e' ### **la stessa formula riga per riga**
*(`np.add.at(out, nodo, somma |psi|^2 sulle bande)`)*. ### ✅ **Quindi l'esito e'
`COINCIDE`, non `NUOVA`: non ho dovuto citare un punto della carta perche' la variabile
### **non e' un'invenzione dell'era `2`.**

### ⚠⚠ **E IL BANCO DICE ANCHE UNA COSA CHE VA LETTA CON LA DECISIONE, e la riporto
perche' e' MISURATA la' dentro:** `nonlineare2.fase_pari2` e' la forma `(A)`,
`phi_k = g rho_k dtau_k`, e il suo docstring dice ### **<<PARI sotto `C` ⟹ ROMPE `C`>>**,
mentre `fase_elicita` *(la forma `(B)`, con `h`)* e' ### **DISPARI e commuta con `C`.**
### ⛔ **Cioe' il cambio di sorgente da `h` a `rho` CAMBIA LA PARITA' DEL TERMINE SOTTO
`C`**, e la simmetria del passo ### **va RIMISURATA, non dedotta** — e' il punto `2(b)`
del mandato del quinto pezzo. ### **Lo scrivo qui prima di misurarlo, perche' il banco lo
diceva gia' e io stavo per non guardarlo.**

### ⚠ **E IL `CONFLITTO` E' UNO SOLO, ma non e' piccolo: LE CONDIZIONI INIZIALI.**
La tabella **non ha un posto dove dichiararle**, e il generato fa `np.zeros`.
### ⛔ **Uno stato a zero non e' una condizione iniziale: e' l'ASSENZA di una.**

---

## 1. LE VARIABILI DI STATO

| | tipo in tabella | la funzione del banco | `dtype` e forma | dove vive | esito |
|---|---|---|---|---|---|
| **`psi_h`** | `complesso_c2_estremita` | `camminata.stato_casuale` | `complex128`, `(2m, 2)` | estremita' | ### ✅ **`COINCIDE`** |
| **`phi_h`** | `complesso_estremita` | `vuoto3.vuoto_fondo`, `vuoto3.vuoto_zero` | `complex128`, `(2m,)` | estremita' | ### ✅ **`COINCIDE`** |
| **`Lambda`** | `reale_nodo` | `vuoto3.lambda_nodo` | `float64`, `(n,)` | nodo | ### ✅ **`COINCIDE`** |
| **`h_int`** | `reale_nodo` | `nonlineare2.elicita_nodo` | `float64`, `(n,)` | nodo | ### ✅ **`COINCIDE`** |
| **`rho`** | `reale_nodo` | `camminata.rho_nodo` | `float64`, `(n,)` | nodo | ### ✅ **`COINCIDE`** |
| **`psi`** | `complesso_c2_nodo` | ### **nessuna: nel banco NON ESISTE** | `complex128`, `(n, 2)` | nodo | ### ⭐ **`NUOVA`** — punto **`A16`** |

### ⭐ **`phi_h` ERA L'ERRORE DI TRASCRIZIONE, ed e' CORRETTO** *(decisione di Luca,
`4e0659e`)*. Diceva `reale_estremita`; il banco lo tiene **complesso** in **quattro**
punti indipendenti: `vuoto3.vuoto_zero` *(nasce `complex`)*, `vuoto3.grover_scalare`
*(accumula in `complex`)*, `vuoto3.lambda_nodo` *(somma `|phi|^2`)*,
`saturazione3.flusso` *(gli da' una **fase**)*, e `camminata3.coniuga3` **lo CONIUGA**.
### ⛔ **La causa era UNA PAROLA:** *<<neutro>>* vuol dire **senza `U`**, non *<<reale>>*.

### ⭐ **`psi` E' `NUOVA` E NON `ORFANA`, e la tabella lo dice da sola:** e' lo spinore
**di nodo** delle tre leggi di **prova**, deciso da **`A16`**, e la tabella dichiara che
e' **TRANSITORIO** — *«quando andranno via ANDRA' VIA ANCHE `psi`»*. ### **Due spinori
nella stessa tabella sono un fatto dichiarato, non scoperto dopo.**

### ⛔ 1-bis. LE CONDIZIONI INIZIALI — **il `CONFLITTO`**

| | il banco | la tabella |
|---|---|---|
| `psi_h` | `camminata.stato_casuale(sc, seme)`: gaussiano complesso, **NORMALIZZATO**, dal **seme** | ### **niente** |
| `phi_h` | `vuoto3.vuoto_fondo(sc, lam0, seme)`: **modulo uniforme `sqrt(LAMBDA0)`**, **fasi dal seme `seme + 777`**, con **`LAMBDA0 = 1.0`** | ### **niente** |
| `Lambda`, `h_int` | **derivate**, non iniziali | derivate |

### ⛔ **E IL GENERATO FA `np.zeros`.** Con `psi_h = 0` e `phi_h = 0` **ogni operatore e'
l'identita'**, `Lambda = 0` e la saturazione prende **il suo ramo limite**:
### **non e' una scena, e' il vuoto assoluto.**

> ### ⚠ **PERCHE' E' UN `CONFLITTO` E NON UN `ERRORE DI TRASCRIZIONE`:** non e' che la
> tabella dica **una cosa sbagliata** — ### **non ha il CAMPO per dirla.** Aggiungerlo
> **cambia la forma della tabella**, e `LAMBDA0` e' **un numero**: metterlo in tabella
> senza decidere **che cos'e'** violerebbe `A1`. ### **Il banco stesso lo dichiara una
> SONDA e non una costante di una legge.** ### ⛔ **Decide Luca:**
> `[[DOMANDA-CONDIZIONI-INIZIALI-IN-TABELLA]]`.

---

## 2. LE LEGGI

| | tipo | la funzione del banco | posizione e frazione | esito |
|---|---|---|---|---|
| **`CAMM-SATURAZIONE`** | `flusso` | `saturazione3.flusso` | **`1`** e **`7`**, frazione **`0.5`** ciascuna | ### ✅ **`COINCIDE`** |
| **`CAMM-MONETA-SPIN`** | `pezzo_unitario` | `camminata2.moneta_spin` | `2`, frazione `1` | ### ✅ **`COINCIDE`** |
| **`CAMM-GROVER`** | `pezzo_unitario` | `camminata.moneta_grover` | `3`, frazione `1` | ### ✅ **`COINCIDE`** |
| **`CAMM-SPOSTAMENTO`** | `pezzo_unitario` | `camminata2.spostamento_trasporto` | `4`, frazione `1` | ### ✅ **`COINCIDE`** |
| **`CAMM-GROVER-VUOTO`** | `pezzo_unitario` | `vuoto3.grover_scalare` | `5`, frazione `1` | ### ✅ **`COINCIDE`** |
| **`CAMM-SPOSTAMENTO-VUOTO`** | `pezzo_unitario` | `vuoto3.spostamento_scalare` | `6`, frazione `1` | ### ✅ **`COINCIDE`** |
| **`CAMM-FORMA-D`** | `flusso` | `interferenza3.flusso_D`, `flusso_D_fisso` | ### **FUORI dall'ordine** *(posto `A4`)* | ### ✅ **`COINCIDE`** |
| **`PROVA-NORMA`** | `osservatore` | ### **nessuna** | — | ### ⭐ **`NUOVA`** — **`A16`** |
| **`PROVA-LOCALE`** | `termine_nodo` | ### **nessuna** | — | ### ⭐ **`NUOVA`** — **`A16`** |
| **`PROVA-HOPPING`** | `termine_arco` | ### **nessuna** | — | ### ⭐ **`NUOVA`** — **`A16`** |

### ⭐ **L'ORDINE COINCIDE AL PEZZO, e si legge dal codice del banco.**
`camminata3.passo3` fa **`flusso(mezzo)` → `_lineare` → `flusso(mezzo)`**, con
`mezzo = 0.5 * r * dt`; e `_lineare` fa **`camminata2.passo2`** sullo spinore
*(`moneta_spin` → `moneta_grover` → `spostamento_trasporto`)* e
**`spostamento_scalare(grover_scalare(phi))`** sul vuoto.
### ✅ **La tabella dichiara esattamente quella sequenza**, e la somma delle frazioni di
`CAMM-SATURAZIONE` fa **`1` esatto** — lo schema lo verifica.

### ⚠ **E IL FATTORE `r` DEL BANCO: dove e' finito.** Il banco calcola
**`dtau = r * dt`**, e `r` e' **il ritmo del nodo** *(`scena.ritmi`)*. ### Il motore
dell'era `2` prende **`dtau` per nodo** come **dato di ingresso**, quindi `r * dt` e'
**gia' dentro**. ### ✅ **Non e' un disallineamento, ma va detto**: la tabella **non
nomina `r`**, e chi cerca `r` nell'era `2` **deve sapere che vive dentro `dtau`.**

### ⚠ **E LA `C`: non e' una legge, e in tabella sta come SIMMETRIA.** Il banco ha
`camminata.coniuga`, `camminata2.coniuga2` e `camminata3.coniuga3` *(`psi -> i sigma_y
psi*`, `phi -> phi*`)*. ### In tabella ogni legge dichiara `simmetrie: [U1-FASE-GLOBALE]`
e **la `C` NON c'e'**. ### ⛔ **E questo e' il secondo posto dove guardare**, perche' la
carta la decide al punto **`F3`**: sta in
`[[DOMANDA-DOVE-STA-LA-C-IN-TABELLA]]`.

---

## 3. IL VERSO `(a)` — **gli operatori del banco USATI nelle misure, SENZA legge**

> ### ⭐ **IL PERIMETRO SI CALCOLA, non si sceglie:** dai `14` file che hanno prodotto le
> misure registrate *(`_letture*`, `_referto*`, `_guscio_moto`)* si segue la **chiusura
> delle chiamate** via `AST` attraverso i `42` moduli del banco.
> ### ⛔ **E IL CENSIMENTO AVEVA UN BUCO MIO, trovato e corretto:** la prima versione
> guardava solo `ast.Call`, e **una funzione passata come VALORE** — `flusso=S3.flusso` —
> **le sfuggiva**: diceva *«la saturazione NON e' usata»*. ### **Corretto, guarda il NOME
> dovunque sia**, e `saturazione3` passa da `2/8` a **`8/8`**.

| | l'operatore del banco | che cos'e' | esito, e **la natura del buco** |
|---|---|---|---|
| `1` | `camminata.moneta_banda`, `moneta_banda_globale` | `exp(-i dtau sigma_z)`: le due bande prendono **fasi opposte** — ### **<<e' la massa>>** | ### ⛔ **`MANCANTE`**, ed e' **fisica**: nessuna legge in tabella porta il termine di massa |
| `2` | `camminata.spostamento` | lo spostamento del `v1`, ### **SENZA trasporto** | ### ⚠ **`MANCANTE`**, ma **superato**: `CAMM-SPOSTAMENTO` e' la sua versione **con `U`**, e il `v2` lo ha sostituito |
| `3` | `pesi4.grover_pesato` | il Grover ### **PESATO** del `v4` | ### ⛔ **`MANCANTE`**: e' **un'altra moneta**, non la stessa con un parametro |
| `4` | `camminata4.passo4_F`, `passo4_S`, `campo_cs` | il passo del `v4` col ### **campo `cs`** | ### ⛔ **`MANCANTE`** |
| `5` | `frazione4.frazione`, `cs_da_arco`, `frazione_inversa` | la **frazione** del `v4` | ### ⛔ **`MANCANTE`** |
| `6` | `cslocale4.cs_nodo`, `densita`, `contrasto`, `dispersione` | la ### **velocita' locale della luce** | ### ⛔ **`MANCANTE`** |
| `7` | `vuoto4.scatter`, `trasmissione`, `quota_vuoto` | lo scambio col vuoto del `v4` | ### ⛔ **`MANCANTE`** |
| `8` | `nonlineare.fase_dispari` | una fase non lineare ### **DISPARI sotto `C`** | ### ⛔ **`MANCANTE`** |
| `9` | `interferenza3.flusso_E`, `flusso_E_fisso` | la forma **`(E)`**, ### **sorella della `(D)`** | ### ⛔ **`MANCANTE`**, e **salta agli occhi**: la tabella ha la `(D)` e **non la `(E)`** |
| `10` | `interferenza3.flusso_implicito` | la forma **implicita** | ### ⛔ **`MANCANTE`** |
| `11` | `saturazione3.flusso_su_rho`, `flusso_v2` | i ### **DUE CONTROLLI che DEVONO rompere `C`** | ### ⚠ **`MANCANTE` per costruzione**: un **controllo** non e' una legge, e metterlo in tabella **lo renderebbe accendibile** |
| `12` | `camminata.coniuga`, `coniuga2`, `coniuga3` | la ### **`C`** | ### ⚠ **`MANCANTE` come legge**, ma e' **una SIMMETRIA**: vedi la domanda al paragrafo `2` |

### ⭐ **E I `MANCANTI` NON SONO TUTTI LO STESSO BUCO.** Tre famiglie:

| | la famiglia | che cosa chiede |
|---|---|---|
| **`A`** | `1`, `9`, `10` — **fisica del `v2`/`v3` che la tabella non porta** *(la massa, la forma `(E)`, l'implicita)* | ### ⛔ **una decisione di Luca**: entrano nell'era `2` o no |
| **`B`** | `3`..`7` — **tutto il `v4`** *(Grover pesato, campo `cs`, frazione, vuoto `v4`)* | ### ⛔ **una decisione di Luca**: il `v4` e' parte dell'era `2`? |
| **`C`** | `2`, `11`, `12` — **superati o non-leggi** *(lo spostamento del `v1`, i controlli, la `C`)* | ### ✅ **niente**: sono spiegati, e la spiegazione sta qui |

---

## 4. LE DOMANDE CHE NASCONO DA QUI

| | la domanda | perche' NON la decido io |
|---|---|---|
| `1` | **`[[DOMANDA-CONDIZIONI-INIZIALI-IN-TABELLA]]`** | la tabella **non ha il campo**, e aggiungerlo **cambia la sua forma**; e `LAMBDA0` e' **un numero** che `A1` non lascia mettere senza dire **che cos'e'** |
| `2` | **`[[DOMANDA-MASSA-E-FORME-MANCANTI]]`** *(famiglia `A`)* | il termine di **massa**, la forma **`(E)`** e l'**implicita** sono **forme di leggi**: entrano o no e' **fisica** |
| `3` | **`[[DOMANDA-IL-V4-ENTRA-NELL-ERA-2]]`** *(famiglia `B`)* | il `v4` e' **un modello**, non un dettaglio: **cinque** gruppi di operatori |
| `4` | **`[[DOMANDA-DOVE-STA-LA-C-IN-TABELLA]]`** | la `C` e' decisa al punto **`F3`** e **nessuna legge la dichiara**: o e' un campo `simmetrie`, o e' **un'omissione** |

### ⭐ **E LA MIA RACCOMANDAZIONE, SEPARATA DALLA DECISIONE**, sta dentro ciascuna voce.
