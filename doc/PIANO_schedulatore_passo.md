# LO SCHEDULATORE DEL PASSO — **analisi e piano** *(2026-09-27)*

> **Decisione di Luca:** *«Il passo pieno diventa uno SCHEDULATORE. Lo schedulatore POSSIEDE il
> passo. Le regole del passo (sincronia, scala minima, 4 π, ordine) non sono più intenzioni dentro
> le leggi controllate a posteriori dai presidi: sono l'ARCHITETTURA, e il codice non offre il modo
> di violarle.»*
> **Sostituisce la forma della cura `(c)` di `ETC-PASSO`**; `(c)1` resta valido fino alla tappa `T1`.
>
> ### 🛑 **SOLO ANALISI E PIANO. Nessun codice.** Blob del simulatore **`e06dcb4e`**, prima e dopo.

**Lo strumento che genera i dati:** `csv/_test_fork/_etc_schedulatore.py`, referto
`_etc_schedulatore.json`. **Riusa** la FASE 0 *(`_etc_letture.py`)*, la 0-bis *(`_etc_progetto.py`)*
e il rilievo `(b)3` *(`_etc_rami_morti.py`)*.

---

# 1. OGNI FUNZIONE DEL PASSO, COL TIPO PROPOSTO

**Il tipo è dedotto da CIÒ CHE LA FUNZIONE SCRIVE**, non da come si chiama. **57 funzioni** girano
nel passo pieno.

| tipo | n. | quali |
|---|---|---|
| **`dinamica`** | **9** | `scuoti_vuoto` · `step` · `memoria_hebbiana_moto` · `_passo_spinoriale` · `calcola_psi` · `ritmo` · `_aggiorna_lift_spinoriale` · `_estendi_psi_spinor` · `_eredita_spinore_figli` |
| **`vincolo`** | **1** | `_smp_chiudi` |
| **`disegno`** | **2** | `rilassa_disegno` · `_togli_rotazione_rigida` *(ramo morto, `L_CONSERVA`)* |
| **`osservatore`** | **44** | tutto il resto: scrive **solo** contatori `_g_*` / tracce, oppure **niente** |
| ### **`AMBIGUA`** | ### **1** | ### **`mitosi`** |

## 1.1 — ⚠ **Le tre cose che questa tabella NON cattura, e vanno dette**

### **① `mitosi` è AMBIGUA perché scrive STRUTTURA e STATO FISICO insieme.**
**Non è un difetto della tassonomia: è il cuore del problema.** Nel progetto è `strutturale`, ma
oggi **fa anche la dinamica** *(30 scritture di stato)*. **`T3` e `T4` devono separarla**, ed è il
punto più delicato del piano.

### **② I VINCOLI non sono funzioni di tipo `vincolo`: sono funzioni PURE applicate dai writer.**
`_nasce`, `_smorza`, `_sd0`, `_pav_*`, `satura`, `% _dphi()` risultano **`osservatore`** — perché
**calcolano** e **non scrivono**. ### **È chi le chiama a scrivere.**
**E questa è esattamente l'inversione che lo schedulatore deve fare:** oggi il vincolo è **applicato
dalla legge dinamica**; nel progetto deve essere **applicato dal compositore, una volta.**
*(Solo `_smp_chiudi` risulta `vincolo` perché scrive `d0` lui stesso — ed è **già** il modello
giusto: `C3`.)*

### **③ Un `osservatore` può violare `A3-DISEGNO` senza scrivere niente.**
`chiralita_core_locale` è `osservatore` *(scrive solo contatori)*, **legge `pos`**, e **il suo
risultato entra nella fisica** — `step:5271` lo usa per `twn` quando `CHI_CORE` è acceso *(e il
driver lo accende)*. ### **Il tipo per SCRITTURE non basta: serve anche «da dove legge».**
**Nel progetto la fotografia senza `pos` chiude anche questo caso** — ma solo se `chiralita_core_locale`
riceve la fotografia invece di `self`.

---

# 2. CHE COSA SCRIVE OGNI LEGGE, E SE PUÒ RESTITUIRE VARIAZIONI

| legge | tipo | scritture di STATO | forme |
|---|---|---|---|
| `scuoti_vuoto` | `dinamica` | **1** | `incremento` 1 |
| `step` | `dinamica` | **26** | `assegnazione` 14 · `incremento` 8 · `vincolo` 4 |
| `mitosi` | **`AMBIGUA`** | **30** | `assegnazione` 26 · `vincolo` 4 |
| `rilassa_disegno` | `disegno` | ### **0** | — |
| `memoria_hebbiana_moto` | `dinamica` | **10** | `assegnazione` 3 · `incremento` 6 · `vincolo` 1 |

### **`rilassa_disegno` scrive ZERO stato fisico.** È la conferma che **non è una legge del passo**:
è un disegno, e nel progetto **esce dalla sequenza**.

## 2.1 — La trasformabilità, riusando la FASE 0-bis

La 0-bis aveva classificato **120 scritture** di stato in cinque forme; **13 non erano esprimibili
come variazione**, e ### **sono già sciolte**:

| gruppo | quante | stato |
|---|---|---|
| **pavimenti** *(`_pav_d0` ×7, `maximum(…, 0.05)` su `d`)* | 8 | ### ✅ **usciti** in `(b)1` — erano **morti col driver**, sigillo byte-identico |
| **`phi` avvolta** `% _dphi()` | 4 | ### ✅ **approvato**: una volta sola a fine passo, **ed è il DOMINIO della doppia copertura**, non un clip |
| **`_nb` normalizzato** | 1 | ### ✅ **approvato**: una volta sola |

### **Quindi al netto, le scritture si compongono:** incrementi per somma *(20)*, la mescola come
`δ = p·(E−X)` *(1)*, le assegnazioni indipendenti come `δ = nuovo − foto` *(46)*, e le estensioni
strutturali **dopo** *(40)*.

> ### ⚠ **MA C'È UN PUNTO CHE LA 0-bis NON HA RISOLTO, e va detto qui:** le **assegnazioni
> indipendenti** *(46, la classe più numerosa)* diventano variazioni **solo se due leggi non
> assegnano lo stesso attributo**. ### **E la FASE 0-bis ha misurato che TUTTI E 21 gli attributi
> sono CONCORRENTI.**
> **Dove due leggi assegnano lo stesso attributo, «somma delle variazioni» non è definito** senza
> dire **quale vince** o **come si compongono**. **Non è un caso ipotetico:** `d0` è scritto da
> `step`(4) + `mitosi`(4) + `memoria_hebbiana_moto`(12).
> ### **È la prima domanda che `T3` deve rispondere, e la decisione è di Luca.**

---

# 3. TUTTE LE LETTURE DI `pos` NELLE LEGGI FISICHE — il lavoro di `T4`

### **11 siti, in 5 funzioni.**

| riga | dentro | tipo | a cosa serve |
|---|---|---|---|
| `:2200` `:2201` | `chiralita_core_locale` | `osservatore` | **centro** del gruppo e **raggio** di appartenenza: `pos` definisce *chi sta nel core* |
| `:5363` `:5364` | `step` | `dinamica` | ### **il Kuramoto**: `cmv` = centro di massa **da `pos`**, e `r_cm` la distanza da lì → `pozzo` |
| `:6185` | `mitosi` | `AMBIGUA` | **la posizione del figlio**: `0.5·(pos[a] + pos[b])` |
| `:6352` | `mitosi` | `AMBIGUA` | ### **la lunghezza dell'arco Schwinger**: `0.5·‖pos[aa] − pos[bb]‖` |
| `:6565` | `pozzo_grafo` | `osservatore` | la lunghezza dell'arco **nel ramo `else` di `POZZO_D`** *(già curato da `D02`: col flag la lunghezza è `d`)* |
| `:6607` | `memoria_hebbiana_moto` | `dinamica` | ### **`dirarc`** → `grad_tw` → `mem_mot` e il blocco `GRAV_BIFASE`. **Nessuna guardia** |
| `:6777` `:6778` | `memoria_hebbiana_moto` | `dinamica` | `_cen`, `_rmid` per `tangenz` — **dentro `LS_AZIM`, che il driver NON accende** |
| `:6991` | `memoria_hebbiana_moto` | `dinamica` | ### **`dir_radiale`** → `dir_laterale` → con `MEM_MOTO_TUTTO` **scrive `self.phi`** |

## 3.1 — ⚠ **E l'incrocio «è in un ramo morto?» NON È AFFIDABILE, per la TERZA volta**

Ho incrociato gli 11 siti col rilievo `(b)3`. Il risultato dice che `:6185` starebbe in un ramo
morto *(`ANTIFASE_ADD`)*. ### **È falso, e si vede leggendo:** `:6185` è
`pos_figlio = 0.5·(pos[a] + pos[b])`, cioè **come nasce la posizione di un figlio** — gira a ogni
mitosi.

> ### 📌 **È la STESSA fragilità che `(b)3` ha già trovato due volte: l'intervallo di RIGHE non è
> l'unità giusta per un RAMO.** In `(b)3` l'ho corretta due volte *(37 righe, poi 1)* e **qui si
> ripresenta in una terza forma** — il `end_lineno` di un `If` che ingloba righe sorelle.
>
> ### **Conseguenza per il piano: la lista di `T4` sono gli 11 siti, ognuno da validare LEGGENDO.**
> **Non accetto un conteggio automatico di «quanti sono vivi»**, e non lo scrivo. **Gli unici due
> che dichiaro morti con certezza sono `:6777`/`:6778`** — `LS_AZIM` **non è nell'argv del driver**,
> verificato nella tabella dei flag di `(b)3` — **e `:6565`**, il ramo `else` di `POZZO_D`.

## 3.2 — I quattro casi che `T4` deve portare a Luca

| | il caso | perché è una decisione di teoria |
|---|---|---|
| **①** | **il Kuramoto** `:5363-5364` | `cmv` è il **centro di massa geometrico**, e `r_cm` la distanza da lì. **Senza `pos` non esiste un «centro»**: il sistema relazionale non ha coordinate. Serve una **riformulazione**, non una sostituzione |
| **②** | **`dirarc`** `:6607` | la **direzione** di un arco. In un grafo puro esiste la **lunghezza** (`d`), **non la direzione**. `grad_tw` è un **gradiente lungo una direzione** |
| **③** | **`dir_radiale`** `:6991` | idem, e **scrive `phi`** |
| **④** | **la posizione del figlio** `:6185` e **l'arco Schwinger** `:6352` | il figlio **deve** nascere da qualche parte nel disegno. Ma `:6352` **usa `pos` per una LUNGHEZZA**, e la lunghezza è `d`: ### **questo somiglia a `D02`, ed è probabilmente curabile allo stesso modo** |

**`chiralita_core_locale` `:2200-2201`** è un quinto caso e sta a parte: **è un `osservatore` il cui
risultato entra nella fisica** *(par.1.1 ③)*.

---

# 4. COSA SUCCEDE AI PRESIDI

| presidio | effetto dello schedulatore |
|---|---|
| **`H-P9`** *(si avanza solo con `passo_pieno`)* | ### **si RAFFORZA e cambia natura.** Oggi è una regola sul chiamante; con **un esecutore unico** diventa *«esiste una sola funzione che avanza»*, cioè **architettura**. ⚠ **Ma va riscritto:** oggi guarda `passo_pieno`, e quel nome **cambia** |
| **`H-ETC-1`** *(zero `calcola_psi` senza `w`)* | ### **diventa in gran parte SUPERFLUO**: se `w` è calcolato dal compositore e passato nella fotografia, **una legge non ha modo di non riceverlo**. **Resta come sentinella di regressione**, e il suo conto atteso passa da **8** a **0** |
| **`H-ETC-2`** *(permutare l'ordine dà lo stesso stato)* | ### **resta, ed è IL presidio dello schedulatore.** Ma va **esteso**: oggi permuta 3 volte senza spostare `mitosi`; con le leggi **strutturali separate** dalle dinamiche, **si possono permutare TUTTE le dinamiche** — il presidio diventa più forte |
| **contratto AST di `csv/_passo.py`** | ### **CADE, e va sostituito.** Oggi legge la sequenza dall'AST di `update()` **e verifica che il driver coincida**. Con un elenco di nomi **nella configurazione**, la sequenza **non è più nel codice**: il controllo diventa *«l'elenco effettivo del run è scritto nei risultati»* (`P5`, innesto 2 di Luca) |
| **`_smp_apri`/`_smp_chiudi` di `(c)1`** | `_smp_apri` idempotente **diventa la FASE 1** dello schedulatore e **l'idempotenza non serve più** *(il compositore sa di essere il primo)*. `_smp_chiudi` **diventa la FASE 3**. ### **`(c)1` non è lavoro buttato: è il confine, e `T1` lo assorbe** |
| **`H-REG-R`** | ### **diventa il cancello del REGISTRO** *(innesto 1 di Luca)*: una legge entra nel registro **solo con la sua scheda**. **Da presidio sul commit a precondizione dell'architettura** |
| **`H-P5`** *(un referto dichiara la configurazione intera)* | si **estende** all'elenco delle leggi, ed è l'innesto 2 |

---

# 5. I RISCHI, E COSA NON PUÒ RESTARE BYTE-IDENTICO

| tappa | byte-identico? | il rischio |
|---|---|---|
| **`T1`** scheletro | ### **SÌ, ed è il criterio** | ⚠ **il rischio più alto di tutto il piano:** **sei chiamanti** devono passare per l'esecutore unico, e **una divergenza fra due di loro è invisibile**. È la forma che `(c)1` ha *evitato* con l'idempotenza, e `T1` la **affronta** |
| **`T2`** tipi | ### **SÌ** | basso: è etichettatura. ⚠ **ma `mitosi` è `AMBIGUA`**, e darle un tipo **è già una decisione** |
| **`T3`** fotografia e variazioni | ### **NO, E NON DEVE ESSERLO** | ⚠⚠ **il più delicato:** ① **le assegnazioni concorrenti** (par.2.1) non hanno una regola di composizione; ② `_g_smp_chirurgie > 0` chiede un giro **abbastanza lungo** da dividere archi, e i sigilli finora girano 3 passi; ③ **`mitosi` va spezzata** in dinamica + strutturale |
| **`T4`** disegno fuori | ### **NO** | ⚠ **si ferma per decisione**, come da mandato. E **due dei quattro casi** *(Kuramoto, `dirarc`)* **non hanno una riformulazione ovvia**: chiedono di dire **che cos'è una direzione in un grafo puro** |
| **`T5`** innesti | **SÌ** con l'elenco di default | medio: la configurazione diventa **parte della fisica**, e un elenco sbagliato **non è un errore di sintassi**. Serve che `P5` lo scriva **sempre** |

## 5.1 — Il rischio che non è in nessuna tappa

> ### **Lo schedulatore sposta le regole dai presidi all'architettura — e i presidi sono ciò che ha
> trovato i miei errori.** In questa sessione: `H-REG-R` ha imposto **tre schede che non esistevano**
> *(`SYNC_UPDATE`, `scuoti_vuoto`, `rilassa_disegno`)*; il collaudo di `H-ETC-2` ha trovato **tre
> difetti del presidio stesso**; il controllo di `(b)3` mi ha urlato **due volte** che la riga non è
> l'unità giusta.
>
> ### **Un'architettura che rende una regola impossibile è più forte di un presidio. Ma se
> l'architettura è sbagliata, non c'è nessuno che lo dica.** Quindi **`H-ETC-2` non va indebolito
> mai**, e ogni tappa deve avere **il suo caso che deve fallire**.

---

# 6. STIMA DEL LAVORO, IN COMMIT *(non in tempi)*

| tappa | commit | come si dividono |
|---|---|---|
| **`T1`** | **4** | ① l'esecutore + i 6 chiamanti · ② il sigillo byte-identico · ③ `csv/_passo.py` al nuovo contratto · ④ `H-P9` riscritto |
| **`T2`** | **2** | ① il registro coi tipi + la scheda di `mitosi` come `AMBIGUA` · ② sigillo byte-identico |
| **`T3`** | **6-8** | ① **la decisione di Luca** sulle assegnazioni concorrenti *(documento, nessun codice)* · ② `mitosi` spezzata · ③ la fotografia senza `pos` per le dinamiche · ④ le variazioni · ⑤ i vincoli una volta · ⑥ i flussi casuali per legge · ⑦ il sigillo lungo · ⑧ *(riserva: un fallimento del sigillo è un commit)* |
| **`T4`** | **2 + N** | ① il documento dei 4 casi **per Luca**, e **STOP** · ② `pos` fuori dalla fotografia · **+N** = una cura per caso, e **N lo decide Luca** |
| **`T5`** | **3** | ① il registro per nome · ② `P5` scrive l'elenco · ③ l'avviso di composizione non standard |
| | ### **17-19 + N** | |

**Non stimo tempi:** non ho una misura di quanto duro io, e inventarla sarebbe un numero senza
provenienza *(`L-NUMERI`)*.

---

# 7. LA MIA VALUTAZIONE

## ✅ **Il progetto regge, e regge per una ragione precisa**

> **Le regole che stiamo inseguendo da tre giorni — sincronia, un vincolo una volta, `pos` fuori
> dalla fisica — sono tutte della stessa forma: «questa legge non deve poter fare X».**
> **Un presidio dice «non l'hai fatto». L'architettura dice «non puoi».**
> **E la prova che serve è nei numeri di questa sessione:** `PSI-FLASH` era un'intenzione **scritta
> nel commento di `calcola_psi`** e **non fatta rispettare**; `SYNC_UPDATE` **prometteva Jacobi** e
> lo dava a **un quinto** del passo; `A3-DISEGNO` è **nell'indice da giorni** e ogni cura lo lascia
> lì. ### **Tre regole scritte, tre non rispettate. Non è un problema di attenzione: è un problema
> di architettura.**

## Le tre cose che cambierei

### **① `T3` va spezzata, e la prima cosa non è codice.**
Le **assegnazioni concorrenti** *(par.2.1)* sono un buco nel progetto: **«somma delle variazioni»
non è definito** quando due leggi **assegnano** lo stesso attributo, e **tutti e 21 gli attributi
sono concorrenti**. ### **Propongo che il primo commit di `T3` sia un documento che elenca, per ogni
attributo, QUALI leggi lo assegnano e quale regola di composizione serve — e che la decisione sia
tua.** Altrimenti `T3` la sceglierei io scrivendo codice, che è `A1` al contrario.

### **② `mitosi` va spezzata in `T2`, non in `T3`.**
È l'unica `AMBIGUA`, scrive **30** grandezze di stato **più** la struttura, e `T3` la tocca comunque.
**Spezzarla mentre tutto il resto è ancora byte-identico** la rende un cambiamento **isolabile**;
spezzarla dentro `T3` la mescola con la fotografia e con le variazioni. ### **Un interruttore alla
volta.**

### **③ `T4` mi preoccupa più di `T3`, e per un motivo diverso.**
`T3` è **difficile**; `T4` chiede **una risposta che il modello forse non ha**: ### **che cos'è una
DIREZIONE in un grafo puro?** `dirarc` e `dir_radiale` sono direzioni, e in un sistema con solo
`(i, j, d)` **non esistono**. **Non è un refactor: è fisica da fare.**
**Propongo di separarlo:** **la prima sotto-tappa** = **`pos` esce dalla fotografia** e i siti che restano
**falliscono in modo rumoroso** *(non silenzioso)*; **la seconda** = **le cure, una per caso, con Luca**.
**Così **la prima sotto-tappa** è verificabile e **la seconda** non blocca il resto.**

## Una cosa che **non** cambierei, e va detta

**«La fotografia non contiene `pos`»** è la parte migliore del progetto. ### **Rende `A3-DISEGNO`
impossibile per costruzione invece che vietato per iscritto**, e `A3-DISEGNO` è nell'indice come
`da-decidere` **da giorni**, sopravvissuto a due cure. **Questa è la prima proposta che lo chiude
davvero.**

## ⚠ E un limite mio, che dichiaro

**Tutte le tabelle di questo documento vengono da analisi STATICHE e PER NOME**, e in questa sessione
quel metodo mi ha ingannato **tre volte** sulla granularità delle righe *(par.3.1)*.
### **I numeri qui sono una BASE PER DECIDERE, non un verdetto.** Ogni tappa ha bisogno del suo
sigillo, e `T4` in particolare ha bisogno di **lettura umana sito per sito**.

---

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`SCHED-PASSO` *(nuova)* · `ETC-PASSO` · `ETC-C1-CONFINE` · `A3-DISEGNO` · `PSI-FLASH` ·
`H-ETC-1` · `H-ETC-2` · `CLIP-INVENTARIO` · `DOPPIA-COP` · `D02` · `A1` · `A9`

---

# 8. LA MAPPA DEGLI STRATI, e dove cade ogni pezzo di oggi *(decisione di Luca, 2026-09-27)*

> **Decisione:** *«Il software va strutturato in CLASSI e STRATI, con dipendenze SOLO VERSO IL BASSO.»*
> **Ordine:** gli strati **1-3 nascono DENTRO lo schedulatore** *(`T1`-`T3`)*, non dopo. Gli strati
> **4-6** e la **divisione del file in moduli** sono un **progetto SEPARATO**, dopo `T3`, con una
> **facciata di compatibilità** e sigilli byte-identici.
> ### 🛑 **IL FILE NON SI SPEZZA ORA.**

| strato | che cos'è | dipende da |
|---|---|---|
| **1 · Stato** | **dati puri**: la fotografia, e nient'altro | — |
| **2 · Leggi** | **una classe per legge**, col contratto del suo tipo | 1 |
| **3 · Schedulatore** | possiede il passo: fasi, composizione, vincoli | 1, 2 |
| **4 · Configurazione** | **un oggetto unico**, costruito una volta, **immutabile durante il passo**, validato | — |
| **5 · Strumenti** | diagnostica, presidi, I/O | 1-4 |
| **6 · Interfacce** | CLI, driver, GUI | 1-5 |

## 8.1 — Dove cade ogni pezzo di OGGI

| oggi | strato | note |
|---|---|---|
| i **21 array di stato fisico** + `i`, `j`, `n` | ### **1** | sono già dati puri: vivono come attributi di `Rete` |
| ### **`pos`** | ### **1, ma SEPARATO** | ### **non entra nella fotografia fisica** — decisione (2) di Luca. È dato del **disegno** |
| `scuoti_vuoto` · `step` · `memoria_hebbiana_moto` · `_passo_spinoriale` · `calcola_psi` · `ritmo` · `_aggiorna_lift_spinoriale` · `_estendi_psi_spinor` · `_eredita_spinore_figli` | **2** *(`dinamica`)* | **9 funzioni**, dal referto |
| **`mitosi`** | ### **2, ma DA SPEZZARE** | **`AMBIGUA`**: struttura **e** stato. Si spezza in `T2` |
| `_nasce` · `_smorza` · `_sd0` · `satura` · `% _dphi()` · la normalizzazione di `_nb` | **2** *(`vincolo`)* | ### oggi sono **funzioni pure applicate dai writer**: nello strato 2 diventano **vincoli che il compositore applica** |
| `_smp_chiudi` | **2** *(`vincolo`)* | ### **è già il modello giusto** (`C3`): scrive lui il vincolo, una volta |
| `rilassa_disegno` · `_togli_rotazione_rigida` | ### **2, tipo `disegno`** | **esce dalla sequenza fisica**: muove **solo `pos`** |
| le **44 funzioni `osservatore`** | **2** *(`osservatore`)* o **5** | quelle che servono a una legge restano in **2**; le diagnostiche pure vanno in **5** |
| ### `verifica_invarianti` · `_traccia_d0` · `_traccia_vd` · i contatori `_g_*` | ### **5** | **leggono soltanto** |
| `esegui_passo` + `PASSO_COMPOSIZIONE` *(nasce in `T1`)* | ### **3** | **è lo schedulatore** |
| `_smp_apri` / `_smp_chiudi` come **confine** | **3** | le fasi 1 e 3; `(c)1` è il loro primo abbozzo |
| ### i **~130 flag globali** di modulo | ### **4** | ### **oggi sono globali riassegnati da più funzioni** — `_applica_flag`, `_applica_regime`, `_fattori_coarse` — ed è esattamente ciò che lo strato 4 deve chiudere |
| `_applica_flag` · `_applica_regime` · `_avvisa_leggi_in_uso` · `_cli` | **4** *(costruzione)* e **6** *(la CLI)* | la **costruzione** della configurazione è 4; il **parsing** è 6 |
| `.githooks/*` · `csv/_hook_presidi.py` · `csv/_indice_id.py` · `csv/_presidio.py` | **5** | i presidi |
| `update()` · la GUI · `_scena_video.py` · `csv/_passo.py` · gli script di `csv/` | **6** | le interfacce |

## 8.2 — ⚠ LE TRE COSE CHE LA MAPPA RENDE VISIBILI, e che non erano evidenti prima

### **① Lo strato 4 è il più grosso pezzo di lavoro, e non è nel piano `T1`-`T5`.**
**~130 flag** letti da tutto il file **come globali**, e **riassegnati** da almeno tre funzioni
*(`_applica_flag`, `_applica_regime`, `_fattori_coarse` per `SCALA_B`)*. Un oggetto **immutabile
durante il passo** significa che **ogni lettura di flag diventa una lettura di quell'oggetto**:
### **è il refactor più esteso del progetto**, e va stimato a parte.
> **E ha un effetto collaterale che vale da solo:** `csv/_test_fork/_etc_rami_morti.py` ha dovuto
> **leggere i flag dal modulo dopo la configurazione** e **dichiarare come limite** che *«un flag
> riassegnato durante il passo renderebbe il verdetto falso»*. **Con lo strato 4 quel limite
> sparisce.**

### **② `pos` sta nello strato 1 ma non nella fotografia: è la cosa che rende la decisione (2) implementabile.**
Se `pos` fosse *fuori* dallo stato sarebbe un'invenzione *(esiste, si salva, si disegna)*. **Sta nello
strato 1 come dato del disegno**, e ### **la fotografia che lo strato 3 passa alle leggi fisiche non
lo contiene**. **Non è un divieto: è che il parametro non c'è.**

### **③ Le 44 `osservatore` si dividono fra strato 2 e strato 5, e il criterio NON è il tipo.**
Un `osservatore` **di cui una legge usa il risultato** *(`_pesi`, `_mat`, `_grado`, `_lam_archi`)* è
**strato 2**: la legge ne dipende. Un `osservatore` che **scrive solo una traccia**
*(`_traccia_d0`, `verifica_invarianti`)* è **strato 5**. ### **Il criterio è «qualcuno dipende dal
suo valore?», e va deciso funzione per funzione** — 44 volte.

## 8.3 — La facciata di compatibilità, e perché non è negoziabile

**Gli script di `csv/` fanno `import soliton_simulator as S`** e poi `S.LAM`, `S.Rete`,
`S.scuoti_vuoto`, `S.avvia_test`, `S._NMASSE_VIDEO`… ### **Sono decine di strumenti, e ognuno è un
reperto committato** *(par.7 di `CLAUDE.md`: il codice di una misura dev'essere recuperabile)*.

**Quindi la divisione in moduli mantiene `soliton_simulator.py` come FACCIATA** che re-esporta i
nomi, e ogni passo ha il suo **sigillo byte-identico**. **Un `ImportError` in uno strumento vecchio
non è un fastidio: è un reperto che non si rigira più**, e `CLAUDE.md` lo chiama **un difetto nuovo**.

---

# 9. LE AGGIUNTE A `T3` *(decisioni di Luca, 2026-09-28)*

**Il piano di `T3` non era solo <<separa la mitosi>>.** Luca ha aggiunto **quattro cose**, e tre
sono **registrazioni** *(niente cura ora)*:

| | aggiunta | dove sta scritta | e' una cura? |
|---|---|---|---|
| **a** | ### **LA NASCITA E' UN EVENTO ATOMICO**, e comprende **il RINCULO DEI GENITORI** | `doc/REGOLE_composizione_T3.md` par.4.4 | ### **SI, in `T3`** |
| **b** | la **spinta repulsiva di torsione** e' una **legge dinamica nascosta** in `mitosi()`, con **tre numeri non derivati** | quel documento par.6.1, voce `TORS-SPINTA` | **no: dopo `T3`** |
| **c** | **`MAX_NODI`** diventa **un controllo dello schedulatore che FERMA il run** con un errore esplicito, **mai troncare**, col suo caso che deve fallire | par.6.2, voce `MAX-NODI-FERMA` | ### **SI, in `T3`** |
| **d** | la **soglia di mitosi** modulata dal gradiente di tempo proprio: **ampiezza `0.3` e `tanh` a mano** | par.6.3, voce `MITOSI-SOGLIA-GRAD` | **no: dopo `T3`** |

> ### 📌 **Quindi `T3` ha DUE pezzi di codice, non uno:** la **separazione della mitosi** *(con la
> nascita atomica)* e il **controllo di `MAX_NODI`**. **Sono due commit e due sigilli**, per la
> regola d'oro: un interruttore alla volta.

**E il `MAX_NODI` va prima o dopo?** ### **Prima**, e la ragione e' che non tocca la fisica delle
corse reali *(4 000 000 contro i ~12 800 nodi del pilota)*: e' **un controllo che non cambia un
byte** del run base, quindi si sigilla **byte-identico** e non si mescola con il riordino.
*(Proposta mia; se Luca preferisce l'ordine inverso, si inverte.)*

## E LE DUE COSE CHE RESTANO FUORI DA `T3`, con il loro posto deciso

| | quando |
|---|---|
| **`DOPPIA-COP`** *(il ritmo a `2 pi` da invertire)* | ### **subito DOPO `T3`, PRIMA di `T4`**, cura a se' col suo sigillo: **due cambi di fisica nello stesso sigillo non si attribuiscono** |
| **`CLIP-INVENTARIO`** *(la tabella per FLAG della famiglia 2)* | **dopo `T3`** |
