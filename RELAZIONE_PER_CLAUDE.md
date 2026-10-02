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

## L'ARCHIVIO PER GIORNO - **il file vivo tiene SOLO 2026-10-02**

> **Regola di Luca, 2026-09-26.** A 20436 righe questo file non lo leggeva nessuno per intero, **quindi il suo scopo era gia' perso**. I giorni chiusi stanno in `doc/relazioni/`, uno per giorno, e `git log` resta l'indice.
> *(Diviso da `csv/_archivio_relazioni.py`, che dichiara la regola di taglio.)*

| giorno | righe | file |
|---|--:|---|
| `2026-09-14` | 134 | [`doc/relazioni/2026-09-14.md`](doc/relazioni/2026-09-14.md) |
| `2026-09-15` | 1310 | [`doc/relazioni/2026-09-15.md`](doc/relazioni/2026-09-15.md) |
| `2026-09-16` | 5551 | [`doc/relazioni/2026-09-16.md`](doc/relazioni/2026-09-16.md) |
| `2026-09-19` | 555 | [`doc/relazioni/2026-09-19.md`](doc/relazioni/2026-09-19.md) |
| `2026-09-20` | 1444 | [`doc/relazioni/2026-09-20.md`](doc/relazioni/2026-09-20.md) |
| `2026-09-21` | 5371 | [`doc/relazioni/2026-09-21.md`](doc/relazioni/2026-09-21.md) |
| `2026-09-24` | 1360 | [`doc/relazioni/2026-09-24.md`](doc/relazioni/2026-09-24.md) |
| `2026-09-25` | 3094 | [`doc/relazioni/2026-09-25.md`](doc/relazioni/2026-09-25.md) |
| `2026-09-26` | 2214 | [`doc/relazioni/2026-09-26.md`](doc/relazioni/2026-09-26.md) |
| `2026-09-27` | 2787 | [`doc/relazioni/2026-09-27.md`](doc/relazioni/2026-09-27.md) |
| `2026-09-28` | 1707 | [`doc/relazioni/2026-09-28.md`](doc/relazioni/2026-09-28.md) |
| `2026-09-29` | 1122 | [`doc/relazioni/2026-09-29.md`](doc/relazioni/2026-09-29.md) |
| `2026-10-01` | 1519 | [`doc/relazioni/2026-10-01.md`](doc/relazioni/2026-10-01.md) |

---

# 📁 **PASSO 1: LA RELAZIONE E' ARCHIVIATA PER GIORNO, e lo strumento aveva DUE difetti** *(2026-10-02)*

> ### **Luca, la violazione del par.4 piu' vecchia della coda e' chiusa: il file vivo tiene SOLO oggi.**

**Nessuna riga del simulatore:** blob **`3ddc56d9`** prima e dopo *(sha1 dei byte grezzi)*.

## ✅ **LO STATO, verificato PRIMA di toccare qualunque cosa**

| | |
|---|---|
| `HEAD` | **`e4993ab`**, e coincide con `origin/fork-su2`: ### **atteso, e torna** |
| blob del simulatore sul **disco** | ### **`3ddc56d9`** *(sha1 byte grezzi)* — ### **atteso, e torna** |
| e il disco coincide col **committato** | `git hash-object` da' **`00c6437a`** = `git rev-parse HEAD:soliton_simulator.py`: ### **par.7 stato 1**, il caso normale |

### ⚠ **E le due convenzioni di hash danno due numeri DIVERSI dello stesso file** *(par.2)*: `3ddc56d9` e' il sha1 dei **byte grezzi** *(quello dei presidi e dei referti)*, `00c6437a` e' `git hash-object` *(che applica il filtro `clean`)*. **Sono lo stesso file.**

## 📊 **I NUMERI DELL'ARCHIVIO** *(generati dallo strumento, non ricopiati)*

| | |
|---|---|
| file vivo | da ### **9407 a 61 righe** |
| giorni staccati | **5**: `2026-09-26` *(2214)* · `2026-09-27` *(2787)* · `2026-09-28` *(1707)* · `2026-09-29` *(1122)* · `2026-10-01` *(1519)* |
| gli **8 giorni** dal `2026-09-14` al `2026-09-25` | ### **NON riscritti** — non sono fra i giorni riconosciuti, e lo strumento dice *«SCRITTI 5 file»* |
| conservazione delle righe | ### **9408 in ingresso = 9408 in uscita** *(preambolo 38 + indice scartato 21 + i 5 giorni)* |

### ✅ **E UN CONTROLLO INDIPENDENTE, perche' il conto dello strumento prova solo se stesso**
Ho confrontato il **multiset delle righe non vuote** fra il file a `HEAD` e *(file vivo + i 5 file d'archivio senza le loro 4 righe d'intestazione)*: **7026 contro 7032**, e le **sette** differenze sono ### **esattamente le righe dell'indice rigenerato** *(l'intestazione col giorno nuovo, le 5 righe di tabella nuove, il segnaposto di oggi)*, piu' **una persa** che e' l'intestazione dell'indice col giorno vecchio.
### ➜ **Nessuna riga di CONTENUTO e' persa o cambiata.** *(`L-NUMERI`: il conto dello strumento e la verifica vengono da due conti diversi.)*

## ⛔ **DIFETTO 1 DELLO STRUMENTO: l'indice dell'archivio finiva DENTRO un giorno**

L'intestazione che lo strumento genera e' `## L'ARCHIVIO PER GIORNO - **il file vivo tiene SOLO 2026-09-26**`, e ### **CONTIENE UNA DATA.** La regola di taglio taglia su *«ogni intestazione che contiene una data»*: quindi ### **l'indice di COME SI LEGGE la relazione veniva archiviato come se fosse un fatto del 2026-09-26.**
### ➜ **Cura:** il blocco si **scarta prima del taglio** e si **rigenera**; e se i blocchi non sono esattamente **UNO** lo strumento ### **si ferma senza toccare niente** (`A9`).
### ⚠ **E la regola nuova e' basata sul TESTO, lo dichiaro:** vale perche' quel testo lo scrive **questa stessa funzione**. Il presidio contro la fragilita' non e' la mia attenzione: e' che **un numero di blocchi diverso da 1 FERMA il giro.**

## ⛔ **DIFETTO 2, e l'ho trovato GUARDANDO IL MIO OUTPUT prima di committarlo**

Il primo giro ha prodotto ### **due `---` di fila.** Causa: il blocco dell'indice viveva **fra** un `---` del preambolo e un `---` suo; da quando lo scarto, il `---` del preambolo **resta nel preambolo** e `testa_viva` ne aggiunge un altro.
### ➜ **Non e' cosmetico: lo strumento cosi' NON era IDEMPOTENTE** — a ogni rilancio il file avrebbe guadagnato una riga che nessuno ha deciso.
### ✅ **Curato in un commit a se'** *(par.5: la correzione non si infila nel commit dell'output)*, e il giro vero e' stato **rifatto dal blob di `HEAD` ripristinato in BINARIO** *(par.7: **non** `git checkout`)*.

## ⚠ **E IL TERZO, che era GIA' nello strumento e che la cura ha dovuto prendere**

`testa_viva` costruiva la tabella dai **soli giorni presenti nel file vivo**: ### **le 8 righe dei giorni dal `2026-09-14` al `2026-09-25` sarebbero SPARITE.** Ora i loro conteggi si **ricopiano dalla tabella vecchia**, e ### **non si ricalcolano dai file**: quei file hanno **4 righe d'intestazione d'archivio** in testa, quindi un conteggio rifatto darebbe un numero **diverso** da quello che il giorno aveva — cioe' ### **un numero inventato** (`L-NUMERI`).

## 📖 **CHE COSA HO LETTO, e che cosa NON ho letto per intero — lo dico invece di lasciarlo supporre**

| | |
|---|---|
| **per intero** | `2026-10-01` *(1519 righe)* e `2026-09-29` *(1122)* |
| **in larga parte** | `2026-09-28` e `2026-09-27` |
| ### **NON per intero** | ### **`2026-09-26`**: ne ho letto **le intestazioni e le righe di conclusione** *(`#`, `✅`, `⛔`, `⚠`, `📌`, `🎯`, `➜`)*, non il corpo |
| **i documenti, per intero** | `doc/PIANO_riordino_mitosi.md` · `doc/MITOSI_storia.md` · `doc/PIANO_divisione_e_calore.md` · `doc/REGOLE_nascita.tsv` · la **visione** e la **stella polare** in `doc/REGISTRO_FISICA.md` · le **11 voci** dell'indice chieste · la coda di `doc/INVENTARIO_strumenti.md` |

### ➜ **Perche' lo dichiaro:** il `2026-09-26` e' il giorno dell'**indice** e della **lista chiusa**, e le sue conclusioni vivono in `CLAUDE.md` par.9, nell'indice e nell'inventario — ### **che ho letto.** Ma *«l'ho letto»* vale solo se dico **che cosa**, ed e' la lezione di `dir_laterale` del 2026-10-01: ### **una verifica dichiarata su cio' che non si e' guardato e' peggio di una non fatta.**

---

# ⭐⭐ **PASSO 2: LA REVISIONE DELLA VISIONE E LA PROPOSTA DEL VUOTO LOCALE SONO NEL REPO** *(2026-10-02)*

> ### **Luca, le tue sei cose sono registrate. Un commit di SOLI DOCUMENTI: nessuna riga del simulatore, blob `3ddc56d9` prima e dopo.**

**Dove sta ciascuna:** `doc/REGISTRO_FISICA.md` *(la revisione, la reversibilita', `:M7`)* · `doc/PIANO_divisione_e_calore.md` *(i par. **(C-ter)**, **(C-quater)**, **(D-ter)**, **(I)**)* · `doc/INDICE_ID.tsv` *(**5 voci nuove**, **3 annotazioni**)* · `doc/MITOSI_storia.md` *(la violazione del par.4 chiusa)*.

## ✅ **(a) `:M7`: IL TERMOSTATO FRENA PIU' DI QUANTO RIFORNISCA — e i numeri li ho RIDERIVATI dal `json`**

| | |
|---|---|
| **rifornisce** | **55** passi, ### **`+3.678130e+03`** |
| ### **frena** | ### **94** passi, ### **`−1.169060e+05`** |
| ### **netto** | ### **`−1.132279e+05`** su 150 passi *(149 misurati)* ⇒ ### **il prelievo e' `31.8` volte il rifornimento** |
| ### **dopo il picco al passo 88** | ### **rifornisce ZERO volte e frena in TUTTI e 62 i passi** *(`W = −9.9126e+04`)* |
| il vuoto copre il termostato | ### **SI', margine `48.2`**, e **da solo** in 149 passi su 149 |

### ⛔ **IL RISCHIO DEL PIANO ERA ROVESCIATO, e l'ho annotato invece di riscriverlo** *(par.8)*
Il par. **(C)** diceva *«senza un «fuori» il sistema puo' SOLO PERDERE»*. ### **Misurato: senza il termostato il sistema non si spegne, CRESCE SENZA FRENO.**
### ➜ **E la conseguenza e' nel piano, come chiedi: la proposta del calore locale deve dire COME FRENA, non solo come rifornisce.** È il par. **(C-ter)**, e il requisito non e' negoziabile: ### **chi sostituisce il Nose-Hoover senza dirlo sostituirebbe la meta' PICCOLA del meccanismo e butterebbe la GRANDE.**

### 📌 **E una PRECISAZIONE di un numero di ieri, dallo stesso `json`**
Avevo scritto *«`xi` cambia segno UNA volta, al passo 56»*. ### **Il 56 e' l'ULTIMO con `xi < 0`** *(`−7.480e-03`)* **e il 57 il PRIMO con `xi > 0`** *(`+2.871e-02`)*: il cambio sta **fra i due**. *(Che sia **una volta sola** e' confermato.)* — ### **l'ho derivata dalla serie, non ricopiata** (`L-NUMERI`).

## ⭐ **(f) LA REVISIONE DELLA VISIONE, e RIVEDE TRE RIGHE registrate ieri**

| la riga vecchia | cio' che la sostituisce |
|---|---|
| *«la nascita ha TRE ESITI»* | ### **UN SOLO tipo di nascita di nodo, in TRE REGIMI** *(vuoto -> spazio · interferenza costruttiva -> rafforza una massa · regime di coppie)* |
| **criterio 8** *«due NODI nuovi, `+1` e `−1`»* | ### **una coppia di PATTERN (masse) con verso di rotazione OPPOSTO**, che nascono e si annichilano insieme e **in modo reversibile**. ### **La nascita di nodi e' SOLO SPAZIO, e resta l'UNICA FRECCIA** |
| **decisione 1** *«`tw` e' simile a una CARICA»* | ### **`tw` e' una TENSIONE che paga lo spazio, NON una carica.** La carica e' il **verso di rotazione** |

### ✅ **E TRE AFFERMAZIONI LE HO VERIFICATE SUL SORGENTE PRIMA DI SCRIVERLE COME FATTI**

| | |
|---|---|
| *«la materia e' il baricentro dell'interferenza»* | ### **e' nel codice, in DUE punti**: in `mitosi` *(«il baricentro dell'interferenza **(=la materia)** trasla»)* e in `classifica_topologia` *(«dove sta **davvero** la massa»)*. ### **Cercati per NOME DI FUNZIONE, con l'AST, non per riga** |
| *«`omega = phivel`»* | lo dichiara il registro: `'phivel': ('finito', 'velocita di fase: entrambi i segni')` |
| ### *«termostato e scuotimento scrivono `phivel`»* | ### **confermato**: `step` fa `self.phivel = _phivel_t + delta_phivel`, e `scuoti_vuoto` fa ### **`net.phivel[:net.n] += calcio`** — ### **l'unica scrittura di stato di quella voce** |

### ⛔ **E UN MIO ERRORE DI MISURA, preso in tempo e dichiarato**
Il mio primo scan AST di `scuoti_vuoto` ha risposto ### **«nessun attributo scritto»**, e avrei potuto scriverlo come fatto. ### **Cercavo `self.X` e la riga e' `net.phivel[...]`:** quella voce e' una ### **funzione di modulo che riceve `net`**, non un metodo.
### ➜ **E' di nuovo la forma dell'errore che ho fatto sei volte: una regola basata sulla SINTASSI** *(`self.`)* **invece che su cio' che fa.** ### **La relazione di ieri aveva ragione e il mio strumento no**, e l'ho visto leggendo la riga invece di fidarmi del conteggio.

### ⛔ **`perc_chi` NON E' QUESTA CARICA, e l'ho DICHIARATO** *(come chiedi)*
`perc_chi` e' il **segno del foglio della doppia copertura**, e il suo segno e' una convenzione ### **al 100 %** *(`CARICA-DI-GAUGE`: 12812/12812, 12782/12782, 14000/14000 ribaltate)*. ### **La carica della revisione viene da `|psi|^2 · phivel`: sono DUE grandezze diverse**, e chiamarle entrambe *«carica»* sarebbe la collisione di nomi che l'indice esiste per curare.
### ⚠ **E questo NON risolve `CARICA-DI-GAUGE`:** dice che quel difetto riguarda `perc_chi`, non la grandezza che la visione vuole conservare.

### 🗣 **LA NOTA DI LINGUAGGIO c'e'**, con la tabella: in fisica *«solitone»* e' lo **stato collettivo localizzato** *(qui: la MASSA)*, e i **nodi** di questo modello ### **somigliano a quanti di spazio.** ### **Il repo mantiene i suoi nomi** *(par.9: un reperto non si riscrive, e «nodo» vive in centinaia di `json`)*, **ma la corrispondenza e' dichiarata.**

### 🛑 **E LE VOCI SULLA CARICA E SULLE COPPIE NON SI IMPLEMENTANO** finche' non chiudi la revisione: ### **la revisione cambia CHE COSA SIA la carica, quindi cambierebbe l'OBIETTIVO delle loro cure.** Curarle ora vorrebbe dire ### **far nascere le coppie neutre in una grandezza che fra una settimana non e' piu' quella che si conserva.**

## ⭐ **(b) `VUOTO-LOCALE-DETERMINISTICO`: la voce c'e', con la FORMA che hai chiarito**

### **UNA SOLA LEGGE PER NODO** — fase <-> gradi di liberta' del vuoto, trasporto lungo gli archi — ### **SENZA temperatura obiettivo**, e ### **NON tanti termostati gerarchici.** ### **La gerarchia EMERGE** dalla geometria: dentro un grumo il calore circola in fretta e il grumo raggiunge una sua temperatura; fra grumi passa lentamente attraverso il vuoto; **il vuoto e' il serbatoio grande, come lo spazio per una stella**; e ### **l'espansione raffredda da sola**, perche' i nodi nuovi portano gradi di liberta' nuovi.

### ✅ **E «il vuoto contiene la maggior parte dei nodi» l'ho verificato invece di assumerlo**
`PESO-MAX` *(2026-09-27, quattro semi)*: i nodi in una massa sono ### **1237 · 1217 · 1239 · 1212 su 12802**, cioe' ### **circa il 9.7 %.**
### ⚠ **E il limite va detto: e' la scena `MASSE-COERENTI` a 3 masse**, non una proprieta' generale del modello.

### ⛔ **LA SOTTIGLIEZZA, e l'ho messa PER PRIMA perche' puo' far cadere tutto**
### **La diffusione e' IRREVERSIBILE PER COSTRUZIONE:** l'equazione del calore non ha un'inversa stabile — invertire il tempo **amplifica il rumore** invece di tornare indietro. ### ➜ **Quindi «il calore si conduce lungo gli archi» scritto come diffusione CONTRADDICE «lo scambio e' reversibile»**, e la contraddizione ### **non e' nei numeri: e' nella FORMA DELL'EQUAZIONE.**
### ✅ **La via che la scioglie:** il calore portato da ### **gradi di liberta' REVERSIBILI** *(oscillatori del vuoto per nodo che **propagano**: un'equazione d'onda, non di diffusione)*, e ### **la diffusione EMERGE dal caos.**
### 🛑 **E LA SCELTA FRA (a) diffusivo e (b) oscillatori NON LA PRENDO IO**, col prezzo di ciascuna scritto. ### **E dico che cosa la deciderebbe: se `REVERSIBILITA-LOCALE` diventa una DECISIONE o resta una direzione.** ### **Sono la stessa domanda posta due volte.**

### 📌 **E per `9-ter` il conto delle leggi NON cresce:** una legge per nodo da cui la gerarchia emerge e' **UNA**, e togliere la *«temperatura obiettivo»* toglie anche ### **`P-EQ-MEDIANA-ARCHI`** *(la fetta arbitraria `median(d0[:n])`)* **e il `clip(±2)` di `xi`** che `:M3` misura ### **non scattare mai** — ### **tre cose in meno, non una in piu'.**

## 🔄 **(c) `REVERSIBILITA-LOCALE`: registrata come `teoria`, NON come decisione**

Lo scrivo cosi' perche' ### **l'hai data cosi'**: una direzione **da valutare**. Il criterio misurabile c'e' — ### *«l'eco di Loschmidt fallisce SOLO nella voce della nascita»* — e ### **cio' che la deciderebbe e' `LOSCHMIDT-ECO`.**
### ⚠ **E ho scritto le TRE cose che la direzione implicherebbe di cambiare**, perche' serve averle in mano **prima** di chiamarla una decisione: il **termostato** *(un attrito: frena in 94 passi su 149)*, le **estrazioni casuali** *(tornare indietro vuol dire ri-pescare da `net.rng` in ordine inverso)*, e ### **`phi[ii]` dove vince l'ultimo** *(una scelta fatta dall'ordine di un array **non ha un'inversa**)*.
### ➜ **Nessuna delle tre e' un argomento CONTRO.** Sono l'elenco del costo.

## 📐 **(d) `LOSCHMIDT-ECO`: in coda, con la LETTURA fissata PRIMA dei numeri**

| che cosa si vede | che cosa significa |
|---|---|
| ### **errore SUBITO e GRANDE in una voce** | ### **IRREVERSIBILITA' DEL CODICE**, e il nome della voce ### **E' il luogo** |
| ### **errore da `~1e-16` che cresce in modo esponenziale REGOLARE** | ### **CAOS che amplifica gli arrotondamenti**, e ### **la pendenza E' l'esponente di Lyapunov** |

### **I due si distinguono PER COSTRUZIONE, non a occhio:** il primo e' grande ### **al primo passo di ritorno**, il secondo e' alla precisione di macchina.
**I sospetti sono elencati PRIMA di girare** *(cosi' un esito atteso non diventa una conferma a posteriori)*: termostato · `beta·vd` · i rilassamenti · le estrazioni · `phi[ii]` · la divisione · `_nasce` a `LAM` · i clip · l'integratore. ### **E la DIVISIONE e' la voce in cui l'eco DEVE fallire**, se la direzione e' soddisfatta.
### ⛔ **E UNA TRAPPOLA DI NOME, presa prima di caderci dentro:** nel simulatore esiste ### **`TEMPO_SEGNO`** *(`False`, e **non gira in nessun run**)*, ed e' ### **un'ALTRA cosa** — il verso del **tempo proprio** alla Feynman-Stuckelberg. ### **Non e' l'inversione del verso del tempo di questa misura.**
**Dipendenze dichiarate:** l'**energia definita** e ### **`MEM-HEBB-VERSO`** *(senza la cura, l'eco misurerebbe anche l'asimmetria del verso dell'arco, e i due effetti non si separano)*.

## ⚠ **(e) `RITMO-AVVIO-FREDDO`: in coda, e NON ho inferito il perche'**

`ritmo()` cade nel suo ramo di sicurezza *(`_ritmo_sicurezza`)* ### **al PASSO 1**, e il passo 1 e' **l'unico squalificato su 150**. Quando scatta restituisce ### **un orologio UNIFORME**; negli altri 149 passi `r` va da `2.06e-05` a `1.4142`.
### ➜ **E' LO STESSO RIPIEGO CHE HA PRODOTTO IL BRACCIO `C` FALSO** *(`SOGLIA-NON-MODULATA`, chiusa come FALSA)*.
### ⛔ **Il «perche'» l'ho scritto come SOSPETTO, non come fatto:** l'avvio a freddo e' il candidato *(al passo 1 manca il passato)*, ### **ma la condizione del fallback e' `r is None or len(r) < n` e i due casi al passo 1 sono DISTINGUIBILI** — ### **va verificato sul sorgente, e non l'ho fatto.**
**Le due cose da decidere sono distinte:** ### **perche'** scatta, e ### **se va dichiarato come REGOLA INIZIALE** *(e allora va nel registro col suo motivo misurato, come le tolleranze di `_nb_ret`)* ### **oppure CURATO.** `blocca_run_base = DA-DECIDERE`.

## 📋 **L'ORDINE DI LAVORO e' nel piano** *(par. **(I)**)*, e ciascun passo dice **perche' viene li'**
### **riordino della mitosi** *(commit 3 e seguenti)* -> ### **`MEM-HEBB-VERSO`** -> ### **energia definita** -> ### **`LOSCHMIDT-ECO` sul nucleo** -> ### **`VUOTO-LOCALE-DETERMINISTICO`** -> ### **verifica che lo scuotimento deterministico inneschi ancora la materia** *(e la misura che lo direbbe **esiste gia'**: `SCUOT-INNESCO`)*.

## ⚠ **UNA DIVERGENZA FRA UNA REGOLA SCRITTA E LA PRATICA, e la dichiaro invece di scegliere in silenzio**

Il **par.9** dice: *«un difetto nuovo = una riga nell'indice, **piu' la spiegazione lunga in `doc/STATO_RUN.md` con lo STESSO ID**»*.
### ⛔ **Misurato: NESSUNA delle cinque voci nuove del 2026-10-01 sta in `STATO_RUN.md`** — `TERMOSTATO-E-FRENO`, `CARICA-DI-GAUGE`, `SCUOT-INNESCO`, `MEM-HEBB-VERSO`, `FINESTRA-DEL-PICCO`: **`0` occorrenze ciascuna.**
### ➜ **Ho seguito la PRATICA in uso** — la spiegazione lunga vive nel `nota` dell'indice e nella `fonte_principale` — ### **e lo dico invece di far finta che la regola sia soddisfatta.** E' un `A9`: ### **quella parte del par.9 non e' un presidio, e oggi non impedisce niente.**
### 📌 **Che cosa la deciderebbe:** se `STATO_RUN.md` sia ancora il posto della spiegazione lunga **o** se il par.9 vada riscritto su cio' che si fa davvero. ### **Decidi tu**, e nel frattempo l'informazione **non e' persa**: sta nell'indice, interrogabile col comando.

---

# 📋 **IL TASK HISTORY DEL COMMIT 3, committato PRIMA del lavoro** *(2026-10-02)*

`doc/TASK_HISTORY/2026-10-02_commit3-nascita-evento-unico.md`. ### **Nessuna riga del simulatore:** blob **`3ddc56d9`** prima e dopo. **Il rito del par.8: il ragionamento si scrive prima, e il suo commit dev'essere ANTENATO dei commit del lavoro** — così l'ordine è **verificabile da git** invece che asserito da me.

## ⚠ **LE CINQUE COSE CHE CREDO E NON HO VERIFICATO, scritte prima di guardare**

| # | cosa credo | perché può essere falso |
|--:|---|---|
| **1** | le estrazioni casuali nella nascita sono **DUE** *(`ANTIFASE_ADD` e `COPPIA_MIT`)* | ### **non ho verificato il DEFAULT di `ANTIFASE_ADD`**, e non ho guardato se `_nasce`, `_grado` o `_smp_chirurgia` peschino |
| **2** | il ramo **stocastico** non gira, quindi la sua estrazione non entra nel contratto | verificato il 2026-10-01, ### **ma solo per la configurazione del driver** |
| ### **3** | ### **assorbire i due `_eredita_*` è la parte DIFFICILE, non la tabella** | portano **sei contatori** e **rami condizionali sulla LUNGHEZZA delle cache**: ### **byte-identico sui CONTATORI vuol dire riprodurre anche i rami che NON scattano** |
| **4** | `conc_nodi` è il **punto cieco** *(cresce con `.append`)* | l'hanno persa **due strumenti diversi**, nello stesso modo |
| ### **5** | ### **l'ordine delle SOMME conta quanto l'estrazione** | `psi` del nato è `0.5*(cur[a] + cur[b])`: ### **se la tabella la calcolasse in un ordine diverso, cambierebbe l'ultimo bit** |

## ✅ **COME MISURO L'ORDINE DELLE ESTRAZIONI — e NON leggendo il codice**

### **Avvolgendo `net.rng`** con un oggetto che inoltra e registra *(metodo, `size`, ordine d'arrivo)*, con l'attribuzione alla **voce** presa dalla spia sui confini del **commit 1**.
### ➜ **Perché non l'AST:** l'AST vede `self.rng.random(...)` **in cinque posti** e ### **non sa quali rami girano** — `ANTIFASE_ADD` e `COPPIA_DENSITA` sono flag, quindi ### **un conteggio statico direbbe 5 dove il runtime dice 1 o 2.** È la regola che in questa sessione ho violato **sei volte**: ### **non leggere il codice, guardare il runtime.**
### 🛑 **E il controllo che rende la misura valida:** ### **lo stesso passo CON e SENZA la spia deve essere byte-identico.** Se non lo è, la spia **consuma il generatore** e ### **la misura misura la spia.**

### 📌 **E UNA LETTURA FISSATA ORA, prima dei numeri**
### **Se le estrazioni nella nascita risultassero ZERO** nella configurazione di riferimento, allora ### **il rischio dichiarato nel piano NON si applica a questo commit**, e lo dirò così invece di tenere in piedi un pericolo che i numeri hanno escluso. ### **Ma le SOMME restano, e quelle non dipendono da un flag.**

## 🛑 **I CINQUE PUNTI IN CUI MI FERMO, scritti prima**

**①** la spia su `net.rng` **perturba** il passo · **②** ### **il byte-identico cade SOLO per l'ordine delle estrazioni o delle somme** · **③** un caso che deve fallire **passa** · **④** il punto unico richiede di ### **RIORDINARE** le scritture *(non solo di spostarle)* · **⑤** assorbire i due `_eredita_*` richiede di ### **cambiare un contatore.**
### ➜ **Il ② è quello che conta, e lo scrivo perché è la tentazione più forte di questo lavoro:** allentare il criterio a *«identico tranne l'ultimo bit»* farebbe passare il commit e ### **butterebbe via la sola prova che la riorganizzazione non è una cura mascherata.**

## ⚠ **E UNA LACUNA DEL REPO CHE HO TROVATO LEGGENDO I FATTI, come il par.0 impone**

`doc/FATTI_dal_codice.md` ha **2 fatti** su `mitosi` e **1** su `_eredita_spinore_figli`. ### **Ma `_eredita_psi_figli`, `semina`, `_allaccia`, `_nasce` e `decidi_divisione` hanno ZERO fatti.**
### ➜ **Sto per toccare cinque funzioni su cui il repo non ha un solo fatto verificato**, ed è la ### **stessa lacuna di `pozzo_grafo`** che ha fatto allargare `FATTI-AVVIO` il 2026-09-27. ### **In CODA, non in questo giro** *(`L-UN-PROMPT`)*, **ma registrata invece che scoperta dopo.**

## ⚠ **E DUE COSE CHE NON SO SE SIANO FATTIBILI, e le dico ADESSO**

| | |
|---|---|
| ### **la SEMINA e l'ALLACCIO nello stesso punto della DIVISIONE** | nascono in un momento del tutto diverso *(la costruzione della scena, non il passo)*: ### **metterli nella stessa funzione potrebbe essere la cosa giusta o un'astrazione forzata**, e non lo so prima di provarci |
| ### **se le 30 grandezze abbiano DAVVERO una regola per ogni evento** | la tabella dichiara **32** regole su `grandezza x evento`, ### **non 30x4 = 120.** Un presidio che pretendesse una regola per ogni coppia ### **chiederebbe 120 righe dove ce ne sono 32** — e allora il presidio sarebbe sbagliato, non la tabella |

**PROSSIMO: lo strumento che misura l'ordine delle estrazioni, committato PRIMA di girarlo.**

---

# 🔧 **LO STRUMENTO DEL PASSO 1 DEL COMMIT 3, committato PRIMA di girare** *(2026-10-02)*

`csv/_test_fork/_ordine_estrazioni.py` *(blob **`99bc86dc`**)*. ### **Nessuna riga del simulatore:** blob **`3ddc56d9`** prima e dopo. **Si committa prima perche' il par.5 lo impone e perche' `_presidio.avvia` RIFIUTA DI GIRARE uno script non committato e pulito** — ### **e' un meccanismo, non una nota** *(`A9`)*.

## ⛔ **E UNA PREMESSA DEL MIO TASK HISTORY E' GIA' CADUTA, PRIMA DI GIRARE** *(par.8: si annota, non si riscrive)*

**Avevo scritto, due ore fa:** *«le estrazioni casuali nella nascita, nella configurazione di riferimento, sono DUE: `ANTIFASE_ADD` e `COPPIA_MIT»*.
### ⛔ **Ne mancava una, e NON e' un dettaglio: `decidi_divisione` pesca SEMPRE** — `nasce = self.rng.random(len(avv)) < prob`. ### **E' la decisione stessa di quali archi si dividono.**
### ➜ **E il codice me lo diceva: il COMMIT 2 l'ha gia' DICHIARATA**, in una tabella del docstring di `decidi_divisione`:
> *«l'estrazione casuale `self.rng.random(len(avv))` — il generatore **AVANZA**: spostarla cambia l'**ORDINE delle estrazioni**, e il run non sarebbe piu' byte-identico. ### **(E' esattamente cio' che il commit 3 deve dichiarare.)**»*
### 📌 **Quindi il contratto di questo commit era GIA' SCRITTO da ieri, e io l'ho cercato dopo aver scritto la mia previsione sbagliata.** ### **La lezione e' `P1`: ho proposto per associazione** *(«le estrazioni stanno nella mitosi»)* **invece di rileggere dal disco cio' che era gia' stabilito su quel punto.**

## ✅ **LO STRUMENTO, e la cosa che dichiara per prima: QUALE STRUMENTO VALE PER QUALE DOMANDA**

| la misura | con che cosa | **perche' quello** |
|---|---|---|
| ### **(A) le ESTRAZIONI** | ### **il RUNTIME** — `net.rng` avvolto da un oggetto che **inoltra e registra** | ### ⛔ **l'AST vede `rng.<metodo>` in NOVE posti e NON SA QUALI RAMI GIRANO:** `ANTIFASE_ADD` e `COPPIA_DENSITA` sono flag, quindi ### **un conteggio statico direbbe nove dove il runtime dice uno o due** |
| ### **(B) l'ordine degli ADDENDI** | ### **l'AST** | ### **e qui l'AST E' lo strumento giusto: l'ordine di `a + b` E' un fatto della SINTASSI**, e non c'e' un runtime che lo dica meglio |

### 📌 **E il fatto di aver dovuto SCRIVERE questa distinzione e' il punto.** La forma dell'errore che in questa sessione si e' ripetuta **sei volte** e' ### **usare la sintassi per rispondere a una domanda di RUNTIME.** ### **Non e' «l'AST e' sbagliato»: e' che va usato dove la domanda e' sintattica.**

## ✅ **IL CONTROLLO CHE RENDE LA MISURA VALIDA, e se fallisce lo strumento SI FERMA**

### **Lo stesso passo CON e SENZA la spia deve essere byte-identico — grandezze E CONTATORI.** Se non lo e', il referto scrive ### **`vale: false`** col motivo, e ### **non si riporta nessun numero.**
### ➜ **E la spia INOLTRA, non reimplementa:** ogni chiamata arriva al `Generator` vero, cogli stessi argomenti e nello stesso ordine. ### **Lo stream non si tocca: si annota.** *(E `bit_generator` si inoltra, perche' `salva_stato` ne legge lo stato e una copia romperebbe la ripresa.)*

## ⚠ **TRE COSE CHE LO STRUMENTO NON FA, dichiarate PRIMA dei numeri**

**①** ### **non decide se il byte-identico del commit 3 passera':** dice ### **qual e' l'ordine da RISPETTARE.** E' il **contratto**, non la verifica. · **②** ### **non copre i rami spenti:** se un flag cambia, l'ordine cambia — e per questo il referto porta la **configurazione INTERA** (`H-P5`). · **③** le estrazioni della **semina** *(che gira alla costruzione della scena, non nel passo)* si riportano ### **a parte**, da un conteggio sul passo zero.

**PROSSIMO: il run, e il referto. Poi la tabella `doc/REGOLE_nascita.tsv` estesa col contratto.**

---

# ⛔ **IL GIRO CORTO HA TROVATO DUE DIFETTI DEL MIO STRUMENTO, e uno era un FALSO ZERO** *(2026-10-02)*

> ### **Luca, lo strumento rispondeva «la semina pesca ZERO». E' falso, e un numero falso in un referto si legge come un fatto.**

`csv/_test_fork/_ordine_estrazioni.py` da **`99bc86dc`** a ### **`59ef30a4`**. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo. **Il fallimento non si aggiusta nel commit dell'output: la correzione e' un commit a se'** *(par.5)*, e ### **il giro vero parte dopo.**

## ✅ **CIO' CHE IL GIRO CORTO HA DETTO DI BUONO, e va detto per primo**

| | |
|---|---|
| ### **IL CONTROLLO TIENE** | lo stesso passo **CON** e **SENZA** la spia su `net.rng` e' ### **BYTE-IDENTICO**, su ### **188 grandezze e contatori** confrontati |
| ### **la configurazione e' quella del driver** | **zero differenze su 81 booleani** (`H-P5`) |
| ### **e la sequenza di un passo SENZA nascite e' TRE estrazioni** | `scuoti_vuoto` → `rng.normal` *(12802)* · `step` → `rng.normal` *(38406)* · ### **`mitosi` → `rng.random` (471564)** |

### ⭐ **E IL TERZO NUMERO CONFERMA CIO' CHE IL COMMIT 2 AVEVA DICHIARATO**
### **`471564` elementi = TUTTI gli archi**, ed e' l'estrazione di `decidi_divisione` *(`nasce = self.rng.random(len(avv)) < prob`)*. ### **Pesca a OGNI passo, anche quando non nasce niente** — e il docstring del commit 2 lo diceva: *«il generatore AVANZA: spostarla cambia l'ORDINE delle estrazioni»*.
### ➜ **Quindi la mia premessa 1 del task history era sbagliata DUE volte:** non erano due estrazioni ma ### **tre**, e quella che credevo ci fosse *(`ANTIFASE_ADD`)* ### **non si e' vista affatto nella finestra misurata.**

## ⛔ **DIFETTO 1, ed e' il peggiore dei due: UN FALSO ZERO**

| | |
|---|---|
| che cosa diceva | *«LE ESTRAZIONI DELLA SEMINA ... **estrazioni: 0**»* |
| ### **perche' e' FALSO** | la `semina` pesca, e si legge nel suo corpo: `rng.random`, `rng.normal`, `rng.choice`. ### **Uno zero li' non vuol dire «non pesca»: vuol dire CHE LA SPIA NON C'ERA** |
| ### **la CAUSA, verificata sul sorgente e non supposta** | mettevo la spia **sottoclassando `S.Rete`**, ### **dopo `carica_dal_cli`.** Ma ### **`_applica_flag` crea la `Rete` (`:9830`) e chiama `net.semina(...)` (`:9847`) DENTRO `carica_dal_cli`**: quando la mia sottoclasse esiste, ### **la semina e' GIA' AVVENUTA** |
| ### **la cura** | si avvolge ### **`np.random.default_rng`** — ### **l'UNICO punto in cui il file costruisce un generatore** *(`:2564`, verificato: una sola occorrenza)* — **prima** del caricamento, e si ripristina dopo. ### **Cosi' la spia c'e' dal primo numero pescato** |
| ### **e un presidio, perche' A9** | se le estrazioni fuori dal passo risultassero **zero**, il referto ora ### **DICE CHE NON SI LEGGE COME UN FATTO** e marca `misurato: false`. ### **Un numero che non si puo' ottenere non deve poter essere stampato come se si fosse ottenuto** |

### 📌 **E LA FAMIGLIA DI QUESTO ERRORE E' GIA' NEL REPO, di ieri**
### **E' lo `0` del primo run sul `--regime`** *(«zero differenze» perche' lo strumento non aveva creato il secondo sistema)*. ### **Stessa forma: uno zero che non e' una misura, e' l'assenza di una misura.**
### ➜ **E la lezione operativa e' secca: un numero che NON TORNA si guarda; uno che TORNA si crede.** Qui lo zero ### **tornava** — e' quello che rende il caso pericoloso.

## ⚠ **DIFETTO 2: l'ordine degli addendi NON conta sui CONTATORI, e metterli nel contratto lo diluisce**

La misura (B) elencava ### **82 scritture**, e fra loro ### **`getattr(self, '_g_nati_mitosi', 0) + int(len(a))`**: una somma di ### **INTERI**, dove ### **l'ordine degli addendi non cambia il risultato.**
### ➜ **Ora ogni riga porta DUE cose in piu': se la grandezza e' nel REGISTRO, e se la somma e' in VIRGOLA MOBILE** — e ### **il tipo viene dal registro, non da un'euristica sul nome.** ### **Il CONTRATTO e' il solo sottoinsieme in virgola mobile**; gli interi si riportano **separati e dichiarati inerti**, e cio' che il registro non dichiara si marca ### **`(non dichiarata)` invece di assumerlo.**

## ✅ **E CHE COSA QUESTO DICE DI `STANDARD 7`**

Il giro corto e' costato ### **meno di un minuto** e ha preso **due difetti**, di cui uno ### **avrebbe messo un numero falso in un contratto.** ### **I collaudi dei criteri non avrebbero preso nessuno dei due**, perche' non c'era un criterio: c'era un **conteggio** — e un conteggio sbagliato ### **non fallisce, risponde.**

**PROSSIMO: il giro VERO, dal passo 40 al 72, sulla scena grande, dove le nascite ci sono.**

---

# ⛔ **TERZO DIFETTO DELLO STRUMENTO, e l'ho visto nel referto del giro VERO** *(2026-10-02)*

> ### **Luca, il referto diceva che per `i` e `j` «l'ordine NON conta». E' la topologia del grafo.**

Strumento da **`59ef30a4`** a ### **`6297a6d6`**. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo. **Il giro vero si rifa' dopo questa cura** *(par.5: la correzione e' un commit a se', PRIMA del nuovo giro)*.

## ⛔ **LA RIGA FALSA, per intero**

```
E 15 scritture di grandezze del registro in cui l'ordine NON conta (INTERI):
    :7414   i   [None]   self.i[keep] | a | m
    :7415   j   [None]   self.j[keep] | m | b
```

### ➜ **`np.concatenate([self.i[keep], a, m])` E' LA TOPOLOGIA.** Permutare quei tre pezzi ### **non sposta un ultimo bit: cambia quali nodi sono collegati.** Dirlo «inerte» in un **contratto** sarebbe stato ### **autorizzare esattamente la cosa che il contratto esiste per vietare.**

## 🔎 **LA CAUSA: due passaggi leciti, una conclusione falsa**

| | |
|---|---|
| **1** | `i` e `j` sono **METRI**, e `REGISTRO_METRI` e' `(("phi","nodo"), ("i","arco"), ("j","arco"))`: ### **NON dichiara un tipo** |
| **2** | il mio codice leggeva *«tipo assente»* e concludeva *«non e' virgola mobile»*, quindi ### **«l'ordine e' inerte»** |
| ### ➜ | ### **nessuno dei due passaggi e' sbagliato; la CATENA lo e'** — perche' la domanda *«l'ordine conta?»* ### **non si decide dal TIPO quando la forma e' una CONCATENAZIONE** |

## ✅ **LE DUE COSE, ora separate, e sono DIVERSE in natura**

| forma | l'ordine conta | perche' |
|---|---|---|
| ### **CONCATENAZIONE** *(`concatenate`, `vstack`)* | ### **SEMPRE, per qualunque tipo** | decide ### **quale valore va a quale INDICE**: non e' l'ultimo bit, e' ### **il SIGNIFICATO** |
| ### **SOMMA aritmetica** *(`a + b`)* | ### **solo in VIRGOLA MOBILE** | cambia ### **l'ULTIMO BIT.** Sugli interi *(i contatori)* e' **inerte**, e li' la cura ② aveva ragione |

### 📌 **E LA FORMA DELL'ERRORE E' LA MIA, di nuovo: una regola che parte da un ATTRIBUTO** *(il tipo)* **invece che da CIO' CHE L'ESPRESSIONE FA** *(concatenare contro sommare)*. ### **E' la settima volta in questa sessione**, e stavolta non l'ha trovata un presidio: ### **l'ho letta nel mio referto** — che e' il motivo per cui un referto si legge invece di committarlo.

## ✅ **CIO' CHE IL GIRO VERO HA GIA' DETTO, e che resta valido**

| | |
|---|---|
| ### **il CONTROLLO tiene** | con e senza spia: ### **byte-identico**, 188 grandezze e contatori |
| ### **la sequenza di un passo SENZA nascite: TRE estrazioni** | `scuoti_vuoto`→`normal`(12802) · `step`→`normal`(38406) · ### **`mitosi`→`random`(471564)** |
| ### **CON nascite: QUATTRO** | le stesse tre, piu' ### **`mitosi`→`random`(1)** |
| ### **e il falso zero e' curato** | fuori dal passo: ### **42 estrazioni**, non 0 — **6** nel vuoto di `_applica_flag`, **36** nella scena |

**PROSSIMO: il giro vero RIFATTO, e poi il contratto nella tabella.**

---

# ⛔ **QUARTO DIFETTO, ANCORA UN FALSO ZERO — e la cura porta DUE misure che non avevo** *(2026-10-02)*

> ### **Luca, il referto diceva «0 somme in virgola mobile». Ma `psi` del nato E' una somma: `0.5*(cur[a] + cur[b])`. Guardavo solo la forma piu' esterna.**

Strumento da **`6297a6d6`** a ### **`e4ccf2d0`**. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo.

## ⛔ **IL DIFETTO: la somma era ANNIDATA dentro un pezzo della concatenazione**

```
self.psi = np.concatenate([cur[:n0], 0.5 * (cur[a] + cur[b])])
                                           ^^^^^^^^^^^^^^^^^  <- QUESTA
```
Il mio classificatore trovava la forma **esterna** *(`concatenate`)*, la metteva fra le concatenazioni e ### **si fermava**. ### ➜ **Quindi il conteggio delle somme in virgola mobile era ZERO per COSTRUZIONE**, non per misura. ### **Terzo falso zero in un giorno, e tutti miei.**

## ⭐ **E LA CURA MI HA FATTO MISURARE UNA COSA CHE NON SAPEVO, e cambia il contratto**

> ### **In IEEE-754 l'addizione e' COMMUTATIVA ma NON ASSOCIATIVA. Quindi l'ordine degli addendi conta da TRE in su, NON da due.**

**MISURATO dallo strumento stesso**, su valori scelti per metterla in crisi *(scale `1e8` e `1e-8`, 200000 elementi)*:

| | |
|---|---|
| ### **DUE addendi** | `a+b` contro `b+a`: ### **BYTE-IDENTICI** |
| ### **TRE addendi** | `(a+b)+c` contro `a+(b+c)`: ### **DIVERSI in 48083 casi su 200000** |

### ➜ **E questo RESTRINGE il contratto, invece di allargarlo:** le somme della nascita — `0.5*(cur[a]+cur[b])`, `0.5*(phivel[a]+phivel[b])`, `0.5*(pos[a]+pos[b])` — hanno ### **DUE addendi**, quindi ### **il loro ordine NON va nel contratto.** ### **E non e' una mia assicurazione: e' una misura che lo strumento rifa' a ogni giro.**

## ✅ **E IL BUCO DEGLI ALIAS LOCALI, CHIUSO CON UNA MISURA invece che inseguito**

Il mio classificatore parte dalle scritture di `self.<nome>`, quindi ### **perde le somme che passano da una VARIABILE LOCALE** — e ce n'e' una che conta: ### **`pos_figlio = 0.5 * (self.pos[a] + self.pos[b])`**, il figlio della mitosi. ### **E' il punto cieco degli alias locali, che in questa sessione ha gia' nascosto cose QUATTRO volte.**
### ➜ **Invece di inseguirlo, ho misurato la cosa che INVALIDEREBBE la conclusione:** ### **esiste nel perimetro UNA somma di tre addendi o piu'?**

| | |
|---|---|
| somme `+` nelle 5 funzioni, ### **qualunque bersaglio, locali comprese** | ### **39** |
| con **due** addendi | ### **39** |
| ### **con TRE o piu'** | ### **ZERO** |

### ➜ **Quindi il buco NON PUO' CAMBIARE IL VERDETTO**, e lo dico con un numero invece di con una promessa. ### **E' la forma giusta di chiudere un limite: non «ho guardato bene», ma «ecco la misura che lo renderebbe irrilevante».**

## ✅ **E UNA TERZA COSA CHE IL REFERTO ORA PORTA: le RIDUZIONI**

`np.add.at` e `np.bincount` ### **non sono somme SCRITTE: sono ACCUMULAZIONI su molti termini**, e li' l'associativita' morde davvero. Nel perimetro sono ### **DUE**, entrambe in `mitosi`:
```
:7304  np.add.at(twn, self.i[self.i < self.n], np.abs(self.tw)[...])
:7305  np.add.at(twn, self.j[self.j < self.n], np.abs(self.tw)[...])
```
### ➜ **E vivono nel ramo `if MITOSI_DIR != 0.0`, che dal RUNTIME vale `0.0`: NON GIRANO.**
### ⚠ **Resta DICHIARATO, e non e' una formalita':** se un giorno `MITOSI_DIR != 0`, ### **l'ordine di `add.at` entra nel contratto — e il contratto di OGGI non lo copre.**

**PROSSIMO: il giro vero rifatto, il contratto nella tabella, e il referto.**

---

# ⛔ **UNA MIA FRASE SUL PRESIDIO ERA FALSA, e l'ha smentita il mio stesso run** *(2026-10-02)*

> ### **Luca: ho scritto che `_presidio.avvia` RIFIUTA DI GIRARE uno script non committato. Per il mio strumento NON E' VERO, e il mio strumento ha girato dirty fino in fondo.**

**Dove l'ho scritta:** nel messaggio del commit **`dacec29`** e nel suo paragrafo di relazione —
*«`_presidio.avvia` RIFIUTA DI GIRARE uno script non committato e pulito — e' un meccanismo, non una nota (`A9`)»*.
### **Le due righe RESTANO leggibili** *(par.8: si annota)*, e questa e' la correzione.

## 🔎 **IL CODICE, letto invece che ricordato** *(`csv/_presidio.py`, `:121`)*

```
if nome.startswith("_sigillo_") and (t["repo"] is not None) and (not t["tracciato"] or t["dirty"]):
    print("[TIMBRO] RIFIUTO DI GIRARE: ... Per un diagnostico
          questo controllo NON blocca: dichiara e prosegue.")
    sys.exit(2)
```

### ➜ **Il rifiuto e' CONDIZIONATO AL NOME: solo `_sigillo_*`.** Per ogni altro script il timbro dice ### **`!! MODIFICATO rispetto a HEAD`** e ### **si prosegue** — e il commento del codice ### **lo dichiara apertamente.**

## ✅ **E NON L'HO INFERITO: L'HO MISURATO**

| | |
|---|---|
| `csv/_test_fork/_ordine_estrazioni.py` | **tracciato** `True` · ### **dirty `True`** · `sha1-byte` `e4ccf2d0` |
| il nome comincia con `_sigillo_`? | ### **NO** |
| ### **ha girato?** | ### **SI', fino in fondo, uscita `0`, e ha prodotto un referto** |

## ⚠ **E IL DIFETTO NON E' DEL CODICE: E' DELLA FRASE CHE LO DESCRIVE, e sta negli ASSIOMI**

`doc/ASSIOMI.md`, dentro **`A9`**, dice: *«`avvia(__file__)` forza utf-8, timbra lo script con git, e **rifiuta di girare** se lo script non e' committato e pulito»* — ### **senza la condizione sul nome.**
### ➜ **E io ho ricopiato quella frase senza verificarla sul codice.** ### **E' `P1` applicato a un presidio**, ed e' la forma d'errore che questo repo chiama *«verifica dal codice, non dai commenti»* — ### **stavolta il commento stava in un documento d'avvio.**

### 📌 **PERCHE' CONTA, e non e' una pedanteria**
`A9` cita questo meccanismo come ### **L'ESEMPIO di «un MECCANISMO, non una nota»**, cioe' come la prova che `A9` non viola se stesso. ### **Ma per i DIAGNOSTICI — la grande maggioranza degli script di `csv/` — il meccanismo NON IMPEDISCE: DICHIARA.** Quindi per quella classe la protezione del par.7 e' ### **un timbro da leggere, non un blocco** — ed e' esattamente la differenza che `A9` esiste per nominare.

## 🛑 **LE TRE VIE, e NON ne scelgo nessuna** *(`PRESIDIO-RIFIUTO-SOLO-SIGILLI`)*

**(a)** si **precisa la frase** di `A9` con la condizione sul nome — ### ⚠ **ma `doc/ASSIOMI.md` e' dichiarato INTOCCABILE** (`CLAUDE.md` par.0), **quindi la decidi tu**. · **(b)** il rifiuto si estende a ### **OGNI script che produce un referto COMMITTATO**, non solo a quelli chiamati `_sigillo_*` — e allora il criterio ### **non e' piu' il NOME ma CIO' CHE LO SCRIPT FA**, che e' la forma giusta *(ed e' la lezione che in questa sessione si e' ripetuta **sette** volte)*. · **(c)** resta com'e' e **si DICHIARA**, con `A9` applicato a se stesso.

### 📐 **CHE COSA LA DECIDEREBBE:** contare ### **quanti script di `csv/` producono un referto committato e NON si chiamano `_sigillo_*`.** Se sono molti, la **(b)** e' la via, perche' la protezione del par.7 oggi ### **non li copre.** ### **Quel conteggio NON L'HO FATTO, e lo dico invece di stimarlo.**

## ✅ **E UNA COSA CHE IL REFERTO DI OGGI FA BENE COMUNQUE**
Il referto porta ### **`blob_strumento`** dentro il `json`, quindi ### **quale blob ha prodotto quel numero e' scritto nel dato**, non nel timbro a stdout. ### **La ricostruibilita' non dipende dal presidio che non ha bloccato** — ma dipendeva da me, e questo e' il punto di `A9`.

---

# ✅ **IL GUARDIANO HA TROVATO UN BUCO VERO: le riduzioni non sono solo `add.at`** *(2026-10-02)*

> ### **Luca, il rilievo e' giusto e il caso concreto esiste: `mitosi` scrive `ultima_prob_coppia = float(prob_coppia.mean())`, una MEDIA IN VIRGOLA MOBILE sugli archi di `sel`. Il mio rilevatore la perdeva.**

Strumento da **`e4ccf2d0`** a ### **`acf50d19`**, piu' `csv/_conta_referti.py` *(`d6592303`)*. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo. **Il giro vero si fa DOPO questa cura, come chiedi.**

## ✅ **PRIMA LA RISPOSTA ALLA TUA DOMANDA, che e' la piu' importante: IL SIGILLO LE CONFRONTA?**

### **NO. E non e' una rassicurazione: e' un BUCO DEL SIGILLO.**

La regola del braccio `B` *(letta dal codice, `csv/_seal_fork/_sig_controllo_unico.py`, `_contatori`)* confronta ### **DUE insiemi**: le grandezze di `REGISTRO_NOMI`, e i **contatori** = ogni attributo che ### **comincia con `_` ED E' UN INTERO.**

| grandezza | nel registro? | contatore? | ### **il sigillo la confronta?** |
|---|---|---|---|
| `ultima_prob_coppia` | NO | NO *(e' un **float** senza `_`)* | ### **NO** |
| `ultima_frac_antifase` | NO | NO | ### **NO** |
| ### **`_g_peqn_mediana`** | NO | ### **NO, ed e' il caso peggiore: COMINCIA con `_` ma e' un FLOAT** | ### **NO** |

### ➜ **Quindi se il commit 3 cambiasse l'ordine degli archi, il sigillo NON CADREBBE: ci passerebbe accanto IN SILENZIO.** ### **E' `A8` applicato al sigillo** — *un comportamento che non si conta e' un comportamento sconosciuto*.
### ✅ **CONSEGUENZA OPERATIVA, e la scrivo PRIMA e non dopo: il sigillo del commit 3 DEVE confrontare anche queste tre.** ### **La regola «`_` piu' intero» e' una regola sul NOME e sul TIPO, non su cio' che la grandezza FA** — ed e' la settima volta in questa sessione che una regola di quella forma nasconde cio' che cerca.
### 📌 **E `_g_peqn_mediana` e' l'esempio che vale da solo:** porta il prefisso `_g_` dei contatori, ### **quindi un lettore la crede coperta**, e non lo e' perche' e' un `float`.

## 📊 **IL CENSIMENTO DELLE RIDUZIONI, allargato — col GATE e coi flag dal RUNTIME**

| riga | scrive | forma | gate | ### **gira?** |
|---|---|---|---|---|
| `:7304` `:7305` | *(locale `twn`)* | `np.add.at` | `MITOSI_DIR != 0.0` | ### **NO** *(`0.0`)* |
| `:7334` | `ultima_frac_antifase` | `flip.mean` | `ANTIFASE_ADD` | ### **NO** *(`False`)* |
| ### **`:7479`** | ### **`ultima_prob_coppia`** | ### **`prob_coppia.mean`** | `COPPIA_MIT > 0.0` | ### **SI'** *(`1.0`)* |
| `:7501` `:7505` | *(locale `pmed`)*, `_g_peqn_mediana` | `np.median` | `COPPIA_MIT > 0` e `estratto.any()` | si', **ma la MEDIANA non dipende dall'ordine** |
| `:7495` `:3708` | *(locali `dd`, `u`)* | `np.linalg.norm(axis=1)` | — | si', **ma somma TRE componenti in ordine FISSO** |

### ✅ **E le due «inerti» sono MISURATE, non dichiarate a parole:** mediana ### **0 permutazioni su 200** la cambiano · `norm(axis=1)` ### **deterministica** · media di **BOOLEANI** *(il caso di `flip.mean()`)* ### **0 su 200.**

## ⭐ **E SULLA `.mean()` CHE GIRA, la misura dice una cosa piu' FINE di «dipende dall'ordine»**

**Permutazioni (su 200) che cambiano una media in virgola mobile, PER TAGLIA:**

> ### ⛔ **QUESTA TABELLA E' SBAGLIATA, e la lascio leggibile** *(par.8)*. **Rilievo del guardiano, 2026-10-02:** il test usava ### **UN SOLO vettore per taglia**, e per `n = 3` e `n = 4` quel vettore dava `0` ### **per caso**. ### **La soglia vera e' `3`**, e la tabella corretta sta nel paragrafo *«UN SETTIMO ERRORE»* piu' sotto.
>
> | `n` | 1 | 2 | 3 | 4 | 8 | 64 | 4096 |
> |---|--:|--:|--:|--:|--:|--:|--:|
> | ~~cambiano~~ | **0** | **0** | ~~**0**~~ | ~~**0**~~ | ~~44~~ | ~~6~~ | ~~97~~ |

**E `len(sel)` nella finestra misurata vale:** ### **`1` in sette eventi su otto, `2` al passo 70.**
### ➜ **Quindi `ultima_prob_coppia` e' inerte all'ordine OGGI — ma PER TAGLIA, non per LEGGE.** ~~Da ~8 archi in su la media cambia per permutazione~~ ### ⛔ **IL «~8» E' SBAGLIATO: la soglia e' `3`** *(rilievo del guardiano; la riga resta leggibile, par.8)*, e una scena che si dividesse piu' spesso la renderebbe ordine-dipendente ### **senza che nessuna legge sia cambiata.**
### 📌 **E' esattamente la forma che `A8` chiama pericolosa:** *un'inerzia che dipende da un numero di oggi* ### **non e' un'inerzia: e' una coincidenza che vale finche' dura.** Va nel contratto **cosi'**, non come *«non conta»*.

## ✅ **E IL CONTEGGIO CHE HAI CHIESTO** *(`PRESIDIO-RIFIUTO-SOLO-SIGILLI`, e SOLO il conteggio)*

**Nessuna modifica a `csv/_presidio.py` ne' a `doc/ASSIOMI.md`.** `csv/_conta_referti.py`:

| | |
|---|--:|
| script `.py` sotto `csv/` *(escluso `_archivio` e `__pycache__`)* | **573** |
| chiamati `_sigillo_*` | **75** |
| ### **NON** chiamati `_sigillo_*` | **498** |
| di questi, che **scrivono** un file | **366** |
| ### **e di questi, con almeno un referto TRACCIATO da git** | ### **89** |
| per confronto, i `_sigillo_*` con un referto tracciato | **43** su 75 |

### ➜ **`89` script che il rifiuto del presidio NON copre mettono un referto nel repo, contro `43` sigilli che copre: il rapporto e' `2.1` a 1.**
### ⚠ **E i TRE limiti sono dichiarati nel docstring, non arrotondati:** la convenzione *«una cartella col nome dello script»* ### **non e' cablata** *(chi scrive altrove non e' contato ⇒ **SOTTOSTIMA**)*; *«contiene `open(...,'w')`»* e' una regola ### **sulla SINTASSI**, quindi il numero si legge come un **tetto dei candidati** incrociato con un **fatto di git**; e ### **non dice se quei referti siano STATI prodotti da un blob dirty** — dice quanti script stanno nella classe in cui ### **potrebbe succedere.**
### 🛑 **La voce resta IN CODA e la decisione e' tua**, come hai detto.

**PROSSIMO: il giro vero, il contratto nella tabella, il referto. Poi il commit 3 e il suo sigillo.**

---

# ⛔ **UN SETTIMO ERRORE, E UN SETTIMO FALSO ZERO: un vettore per taglia non e' una misura** *(2026-10-02)*

> ### **Luca, il guardiano ha ragione e l'errore e' grave: avevo scritto «inerte fino a 4, ordine-dipendente da ~8». La soglia e' TRE, e me lo diceva una misura MIA dello stesso strumento.**

Strumento da **`acf50d19`** a ### **`a4c65607`**, generatore del contratto a **`14ed832c`**. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo.

## ⛔ **IL DIFETTO: UN SOLO VETTORE PER TAGLIA**

Il controllo provava ### **200 permutazioni di UN SOLO vettore**, per ogni taglia. Con le scale `1e9`/`1e-9` ### **quel vettore, per `n = 3` e `n = 4`, dava `0` PER CASO** — gli addendi si assorbivano.
### ➜ **Un campione di UNO non e' una misura: e' un aneddoto.** E l'ho stampato come numero.

| | con **UN** vettore *(sbagliato)* | ### **con 200 vettori DIVERSI** *(giusto)* |
|---|--:|--:|
| `n = 1` | 0 | **0** |
| `n = 2` | 0 | **0** |
| ### **`n = 3`** | ### **0** | ### **10 su 200** |
| ### **`n = 4`** | ### **0** | ### **25 su 200** |
| `n = 5` | — | **38** |
| `n = 8` | 44 | **61** |
| `n = 4096` | 97 | **62** |

## ⛔⛔ **E LA COSA PEGGIORE: IL REFERTO CONTRADDICEVA UN'ALTRA MISURA DELLO STESSO STRUMENTO**

Lo stesso referto porta la misura ### **IEEE-754**: ### **due addendi commutativi AL BIT, tre NO.** ### ➜ **Quella misura da' la soglia `3`**, ed e' ### **esattamente quella giusta.**
### **Quindi avevo due numeri miei che si contraddicevano, nello stesso file, e non li ho incrociati.**
### 📌 **E' la stessa forma dell'errore del 2026-10-01**, quando una conclusione cablata in un `print` contraddiceva il numero stampato sopra: ### **li' la conclusione contraddiceva il dato, qui un dato contraddice l'altro.** ### **La cura e' la stessa: il verdetto si DERIVA incrociando le misure, non si scrive.**

## ✅ **LA CURA, in tre pezzi**

| | |
|---|---|
| **1** | ### **`200` vettori DIVERSI per taglia**, uno per permutazione. La soglia misurata e' ### **`3`**, e lo strumento ### **la stampa accanto alla misura IEEE-754 dicendo che le due si CONFERMANO** |
| **2** | il test sulla `norm` era una ### **TAUTOLOGIA** *(confrontava la stessa chiamata con se stessa)*: ora ### **permuta le RIGHE e confronta riga per riga** — cioe' misura cio' che conta, che l'ordine delle **righe** non entri nella norma di una riga. ### **Misurato: `0` su 50** |
| ### **3** | ### **il verdetto su `ultima_prob_coppia` si DERIVA**, incrociando ### **la soglia misurata** con ### **la distribuzione VERA di `len(sel)`** — non lo scrivo io |

## ⭐ **E LA REGOLA DEL CONTRATTO CAMBIA, e diventa PIU' STRETTA**

> ### **`ultima_prob_coppia` e' inerte all'ordine SOLO SE `len(sel) <= 2`. Da `3` in su DIPENDE dall'ordine degli archi.**

**E le taglie vere di `len(sel)` nella finestra misurata:** ### **`1` in sette eventi su otto, `2` al passo 70.**
### ➜ **Quindi e' inerte nella finestra, ma il MARGINE E' DI UN SOLO ARCO.** ### **Un passo con TRE divisioni la renderebbe ordine-dipendente senza che nessuna legge sia cambiata** — e con *«~8»* quel margine sembrava **sei volte** piu' largo di quello che e'.
### 📌 **E' esattamente per questo che l'errore conta:** non cambiava il verdetto *(inerte oggi)*, ### **cambiava di quanto siamo lontani dal non esserlo.**

**PROSSIMO: il giro vero, il contratto generato, il referto. Poi il commit 3 e il suo sigillo, che confronta anche le tre grandezze scoperte.**

---

# ✅ **PASSI 1 E 2 DEL COMMIT 3 CHIUSI: L'ORDINE E' MISURATO, IL CONTRATTO E' NEL REPO** *(2026-10-02)*

> ### **Luca: il contratto c'e', e porta un REQUISITO per il sigillo che prima non c'era.**

**Referto:** `csv/_test_fork/_ordine_estrazioni/_ordine_estrazioni.json` *(`vale: true`, strumento **`a4c65607`**)* · **contratto:** `doc/CONTRATTO_nascita.md` *(**`340d06c8`**, 142 righe, **generato**)* · **tabella:** `doc/REGOLE_nascita.tsv` *(**`84bb5d7f`**, da **7 a 8** colonne)*. ### **Nessuna riga del simulatore:** blob **`3ddc56d9`** prima e dopo.

## ✅ **IL CONTROLLO, per primo: la misura VALE**

| | |
|---|---|
| lo stesso passo **CON** e **SENZA** la spia su `net.rng` | ### **BYTE-IDENTICO**, su **188** grandezze **e contatori** |
| la configurazione | **zero differenze su 81 booleani** (`H-P5`) |
| lo strumento | ### **`a4c65607`, committato e pulito** |

## 📊 **LA SEQUENZA DELLE ESTRAZIONI — la parte stretta del contratto**

| | passo SENZA nascite *(41)* | passo CON nascite *(42)* |
|---|---|---|
| **1** | `scuoti_vuoto` → `rng.normal` *(12802)* | idem |
| **2** | `step` → `rng.normal` *(38406)* | idem |
| ### **3** | ### **`mitosi` → `rng.random` (471564)** = **tutti gli archi**: e' ### **`decidi_divisione`**, e pesca a **OGNI** passo | idem |
| ### **4** | — | ### **`mitosi` → `rng.random` (1)** = gli archi **selezionati**: e' lo ### **SCHWINGER** |

### ⛔ **E `ANTIFASE_ADD` pescherebbe ma e' SPENTO:** l'assenza di quell'estrazione ### **e' parte del contratto**, e se un giorno si accendesse la sequenza avrebbe **cinque** estrazioni e ### **questo contratto non la coprirebbe.** Scritto nel documento.
**E fuori dal passo: 42 estrazioni** — **6** nel vuoto di `_applica_flag`, **36** nella scena.

## ⭐ **L'ORDINE DEGLI ADDENDI: la misura RESTRINGE il contratto**

### **Due addendi sono commutativi AL BIT; tre no** *(48083 differenze su 200000)* ⇒ ### **l'ordine conta DA TRE IN SU.** E nel perimetro: ### **39 somme, TUTTE a due addendi, ZERO con tre o piu'** — **locali comprese**, e questo ### **chiude il buco degli alias locali con una MISURA invece che con una promessa.**
### ➜ **Quindi il contratto delle somme e' VUOTO, e il contratto vero sta nelle 68 CONCATENAZIONI** — dove l'ordine decide ### **quale valore va a quale INDICE**, cioe' **il significato**. *(Permutare `concatenate([i[keep], a, m])` ### **cambia quali nodi sono collegati.**)*
**Riga per riga sta nella colonna `ordine_pezzi`**, abbinata ### **PER ANCORA**: **14** righe a una sola concatenazione · **17** senza *(col **motivo**)* · ### **1 con ancora NON UNIVOCA, nominata.**

## ⛔ **E IL CONTRATTO PORTA UN REQUISITO PER IL SIGILLO, che prima non c'era**

### **Tre grandezze scritte da una riduzione NON sono confrontate dal sigillo:** `ultima_prob_coppia`, `ultima_frac_antifase`, ### **`_g_peqn_mediana`** *(il caso peggiore: ha il prefisso `_g_` dei contatori, ### **quindi un lettore la crede coperta**, e non lo e' perche' e' un `float`)*.
### ➜ **Il sigillo del commit 3 DEVE confrontarle**, ed e' scritto nel contratto ### **prima** di scrivere il sigillo.
### ⭐ **E la regola su `ultima_prob_coppia`, DERIVATA e non scritta da me:** ### **inerte all'ordine solo se `len(sel) <= 2`; da `3` in su DIPENDE.** Le taglie vere nella finestra sono ### **`1` sette volte e `2` una** ⇒ ### **inerte, con margine UNO.** ### **Non per legge: perche' la scena divide poco.**

## ✅ **E DUE CONTROLLI SULLA TABELLA, perche' un lettore non si rompa in silenzio**

**①** le **prime SETTE colonne**: ### **0 righe su 33 cambiate**, verificato **anche dall'esterno** contro il blob a `HEAD`. · **②** ho ### **rigirato il lettore** `_referto_ordine.py`: ### **33 differenze, TUTTE E 33 soli NUMERI DI RIGA, zero d'altro tipo** — il documento era **stantio** su un blob vecchio, e ora porta le righe di oggi. **32 ancore verificate su 32, 1 dubbio** *(il `perc_geom` alla Schwinger, che resta APERTA)*.

## ⛔⛔ **E UN RISCONTRO CHE CAMBIA UN CRITERIO DEL PIANO: `MITOSI_2LAM` E' GIA' ACCESO**

> ### **Luca, il piano dichiara `MITOSI_2LAM` OFF. Il DRIVER lo ACCENDE, e dal runtime vale `True`.**

| | |
|---|---|
| **default di modulo** | `MITOSI_2LAM = False` *(`:441`)* · `PLAST_DIN = False` *(`:1736`)* |
| ### **l'argv del DRIVER** | contiene ### **`--mitosi-2lam`** e ### **`--plast-din`** |
| ### **dal RUNTIME** | ### **`MITOSI_2LAM = True`** · ### **`PLAST_DIN = True`** |

### ➜ **LA CONSEGUENZA, ed e' su un CRITERIO:** il piano descrive il **commit 6b** come ### **«NON byte-identico, ATTESO»**. ### **Ma se il flag e' GIA' ON nella configurazione su cui girano TUTTI i sigilli, far uscire il ramo `else` e' BYTE-IDENTICO IN QUELLA CONFIGURAZIONE** — lo sarebbe non-byte-identico ### **solo con l'argv NUDO.**
### ⚠ **E che il flag AGISCA non l'ho misurato:** lo direbbe ### **`_g_m2l_negati`** sulla finestra dei 72 passi. ### **Quella misura NON l'ho girata**, e la dichiaro *(`L-UN-PROMPT`)*.
### 📌 **E `PLAST_DIN` acceso rende STANTIO un fatto di `doc/FATTI_dal_codice.md`:** quel documento dice che *«la compressione osservata e' il regime di default (dimezzamento `d0 = d/2`)»*, ### **ma con `PLAST_DIN` acceso il ramo che gira e' `d0h = dh*(1 + fattore_plastico)`**, perche' nella catena `if/elif/else` ### **`PLAST_DIN` viene PRIMA.** ### ✅ **`doc/REGOLE_nascita.tsv` invece era GIA' CORRETTA**: nomina `PLAST_DIN` e dice che i tre rami scelgono **solo il fattore**.
### ➜ **La forma dell'errore e' quella del par.6 punto 2 — «il DEFAULT conta piu' della descrizione» — letta al contrario:** ### **la DESCRIZIONE ha preso il default e ha ignorato che il driver lo ribalta.** Stessa famiglia di `CENS-A4`. Voce ### **`MITOSI-2LAM-ACCESO`**, e le annotazioni sono nel piano accanto alle righe vecchie.

## 📋 **IL TODO DEL TASK HISTORY, aggiornato** *(par.5-bis: un TODO aggiornato «dopo» e' un TODO falso)*

**0** task history → ### **FATTO** *(`59e9b99`)* · **1** strumento → ### **FATTO**, con ### **SEI cure** *(tre falsi zero, una tautologia, un rilevatore troppo stretto, un campione di uno)* · **2** run e referto → ### **FATTO** · **3** contratto nella tabella → ### **FATTO** · **4** il CODICE → ### **PROSSIMO** · **5** il sigillo → **DA FARE**, ### **e ora ha un requisito in piu': le tre grandezze scoperte** · **6** referto e **STOP** → **DA FARE** · **7** i fatti mancanti → **IN CODA**.

**PROSSIMO: la misura che decide se il punto unico si puo' scrivere SENZA RIORDINARE le scritture — ed e' il punto ④ in cui il mio task history dice di FERMARMI, se la risposta e' no.**

---

# 🔧 **LO STRUMENTO DEL PUNTO DI STOP ④, committato PRIMA di girare** *(2026-10-02)*

`csv/_test_fork/_punto_unico_fattibile.py` *(blob **`b771ad6a`**)*. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo.

## ⭐ **PERCHE' QUESTA MISURA VIENE PRIMA DEL CODICE**

Il mio task history fissa come ### **punto di STOP numero ④**: *«il punto unico richiede di RIORDINARE le scritture (non solo di spostarle) ⇒ STOP: riordinare CAMBIA LA FISICA»*. ### **E non e' un timore teorico: `doc/MITOSI_non_si_spezza_per_tipo.md` lo ha GIA' MISURATO una volta** — il 2026-09-28, per lo spezzamento per TIPO, e la risposta fu ### **che non si poteva.**
### ➜ **Quindi si misura PRIMA, invece di scoprirlo quando il sigillo cade.**

## 📐 **LA DOMANDA, scomposta in tre — e la terza e' quella che decide**

| # | la domanda | lo strumento |
|--:|---|---|
| **1** | dove sono le **scritture** delle grandezze del registro, in ordine di sorgente | l'AST. ### **I nomi del registro si leggono DALLE TABELLE del simulatore**, non si scrivono a mano; e ### **la CHIAMATA a `_eredita_*` E' una scrittura**, con le grandezze ricavate dal **loro** AST |
| **2** | quali istruzioni **NON-di-scrittura** stanno fra la prima e l'ultima | idem, ### **scendendo dentro gli `if` e i cicli** *(una scrittura dentro `if COPPIA_MIT > 0.0` E' una scrittura della nascita: trattare quel blocco come UNA istruzione nasconderebbe la domanda)* |
| ### **3** | ### **quante di quelle DEVONO restare dov'e' sono?** | una ### **DIPENDENZA IN DUE VERSI**: l'istruzione ### **legge** qualcosa che una scrittura precedente produce ### **E** produce qualcosa che una scrittura successiva consuma. ### **Chi soddisfa entrambe non si puo' spostare ne' prima ne' dopo** |

## ⭐ **IL CRITERIO, FISSATO ORA, PRIMA DEI NUMERI**

> ### **Se esiste ANCHE UNA SOLA istruzione non-di-scrittura che DEVE stare fra due scritture, allora un blocco contiguo richiede di RIORDINARE ⇒ STOP.**

### ⚠ **E IL VERSO OPPOSTO E' DICHIARATO, perche' senza di lui il criterio sarebbe sbilanciato:** ### **zero dipendenze NON dice che il punto unico sia facile.** Dice solo che ### **non e' impedito da un riordino.** Restano ### **i contatori**, ### **i rami condizionali sulle lunghezze delle cache** *(i sei dei due `_eredita_*`)*, e ### **`conc_nodi`, che cresce per MUTAZIONE IN POSTO** — i tre punti che il task history ha dichiarato come la parte difficile.
### 📌 **Questa misura risponde a UNA domanda, non a tutte**, e lo scrivo perche' un criterio che risponde a una domanda sola ### **va letto per quella.**

**PROSSIMO: il run, e il verdetto. Se dice STOP, mi fermo li' e lo dico.**

---

# 🛑🛑 **IL PUNTO DI STOP ④ E' SCATTATO: IL BLOCCO CONTIGUO RICHIEDE DI RIORDINARE. NON HO SCRITTO IL CODICE DEL COMMIT 3** *(2026-10-02)*

> ### **Luca, mi fermo qui, ed e' il punto che il mio task history aveva fissato PRIMA di cominciare. Ma il blocco e' UNO SOLO, e NON e' una legge di fisica: e' una riga DIAGNOSTICA.**

**Referto:** `csv/_test_fork/_punto_unico_fattibile/_punto_unico_fattibile.json` *(strumento **`be5c8133`**)*. ### **Nessuna riga del simulatore:** blob **`3ddc56d9`** prima e dopo.

## 📊 **I NUMERI, e come si assottigliano da 7 a UNO**

| | |
|---|--:|
| istruzioni di `mitosi` *(scendendo dentro `if` e cicli)* | **139** |
| di cui **scrivono** una grandezza del registro | **47** |
| istruzioni fra la **prima** *(`:7335`)* e l'**ultima** *(`:7563`)* | **111** |
| di queste, **NON** di scrittura | **64** |
| ### **segnalate come LEGATE in mezzo** | ### **7** |
| che **girano** con la configurazione del driver | **5** |
| ### **GENUINE anche a granularita' di INDICE** | ### **3** |
| ### **che NON si possono spostare per davvero** | ### **1** |

## ⭐ **IL BLOCCO VERO, ed e' UNA RIGA**

```
:7433   self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])   <- scrittura
:7505   self._g_peqn_mediana = float(np.median(self.peq))                           <- LEGATA
:7552   self.peq = np.concatenate([self.peq, np.full(2 * nc, pmed)])                <- scrittura
```

### ➜ **E' una MEDIANA GLOBALE su `peq`, presa FRA le due scritture di `peq`.** ### **Non si puo' spostare PRIMA** *(leggerebbe il `peq` pre-mitosi)* ### **ne' DOPO** *(leggerebbe quello post-Schwinger)*. ### **E la dipendenza e' GENUINA anche a granularita' di indice, perche' `:7433` FILTRA con `keep`:** dopo quella riga lo stesso indice punta a ### **un'ALTRA voce**, e una mediana sull'intero array cambia.
### ➜ **Quindi raccogliere le scritture di `peq` in un blocco contiguo la SCAVALCA, e scavalcarla cambia un numero.**

## ⚠ **E LE ALTRE QUATTRO NON SONO LA PROVA: lo dico invece di contarle tutte e sette**

| riga | perche' NON e' la prova |
|---|---|
| `:7472` `peq_sel = self.peq[sel]` | ### **NON GIRA**: `COPPIA_DENSITA = False` *(dal runtime)* |
| `:7547` `_tr_pre = self.d0.copy()` | ### **NON GIRA**: `TRACCIA_D0 = False` |
| `:7375` `chi_a`/`chi_b = self.perc_chi[a]`/`[b]` | ### **SPURIA a granularita' di indice:** `:7342` e' una ### **PURA ESTENSIONE** *(`concatenate([perc_chi, perc_chi[a]])`)*, e `a`/`b` sono indici di ### **genitori PREESISTENTI** ⇒ il valore e' lo stesso prima e dopo |
| `:7494` `dd = ...norm(pos[aa] - pos[bb])...` | la lettura di `pos` e' ### **spuria** *(estensione, indici preesistenti)*; resta il flusso locale `dd → :7546`, ### **che si soddisfa calcolando `dd` PRIMA del blocco** |
| `:7501` `pmed = np.nan if PEQ_NASCITA_LOCALE else ...median(peq)` | con `PEQ_NASCITA_LOCALE = True` *(runtime)* ### **la mediana NON VIENE NEMMENO VALUTATA**: `pmed = np.nan`, e ### **nessuna lettura di `peq` avviene** |

### ⚠ **E questa tabella e' una LETTURA DEL SORGENTE, non un'uscita dello strumento:** lo strumento dice ### **3 genuine**, io dico ### **1**, e la differenza sta in due cose che l'AST non sa vedere — ### **il corto circuito di un'espressione condizionale** *(`:7501`)* e ### **un flusso di VALORE locale che si puo' sollevare prima del blocco** *(`:7494`)*. ### **Lo dichiaro cosi' invece di correggere il numero dello strumento a mano** *(`L-NUMERI`)*.

## ⭐ **E IL FATTO CHE CONTA DAVVERO: IL BLOCCO NON E' UNA LEGGE DI FISICA**

| | |
|---|---|
| ### **che cos'e' `_g_peqn_mediana`** | un ### **DIAGNOSTICO**: *«cio' che si EVITA»* — la mediana globale che `PEQ_NASCITA_LOCALE` esiste per **non** usare. **Non e' nel registro.** |
| ### **il sigillo lo confronta?** | ### **NO** — e' una delle **tre** grandezze che il contratto di stamattina ha trovato **scoperte** *(ha il prefisso `_g_` dei contatori ### **ma e' un `float`**, e `_contatori` prende solo gli INTERI)* |
| ### ⛔ **la conseguenza, ed e' scomoda** | ### **se scrivessi il commit 3 raccogliendo le scritture, `_g_peqn_mediana` cambierebbe E IL SIGILLO NON LO VEDREBBE.** Il commit passerebbe, ### **e il difetto sarebbe silenzioso.** |

### 📌 **E' `A8` in forma pura:** ### **l'unico ostacolo al punto unico e' un numero che nessuno controlla.** Se il sigillo non lo guardasse, non ci sarebbe nemmeno un ostacolo — ### **ci sarebbe un difetto.**

## 🛑 **LE DUE VIE, e NON ne scelgo nessuna**

| | la via | il prezzo |
|---|---|---|
| ### **(a)** | ### **il punto unico LASCIA `:7505` dov'e'** e raccoglie tutto il resto | ### **non e' piu' «un punto solo»: e' un punto piu' una riga.** Il piano dice *«da TRE posti a UNO»*, e questo sarebbe ### **UNO e mezzo** — e va detto cosi', non arrotondato |
| ### **(b)** | ### **si cura `_g_peqn_mediana` PRIMA**: quel diagnostico si prende **una volta**, a un istante **dichiarato**, invece che fra due scritture | e' ### **un commit a se', e NON byte-identico su quel numero** — ma ### **il sigillo oggi non lo confronta**, quindi ### **il primo lavoro e' ESTENDERE IL SIGILLO**, non cambiare il codice |

### ➜ **E la mia raccomandazione, perche' me la chiedi sempre: (b), e nell'ordine `sigillo → diagnostico → punto unico`.** ### **Estendere il sigillo PRIMA e' l'unica cosa che rende visibile il cambiamento che poi si fa** — e senza quello la (a) e la (b) ### **sono indistinguibili dai numeri.**

## 📋 **IL TODO DEL TASK HISTORY, aggiornato** *(par.5-bis)*

**0** task history → **FATTO** · **1** strumento → **FATTO** *(sei cure)* · **2** run e referto → **FATTO** · **3** contratto → **FATTO** · ### **4 il CODICE → NON FATTO, e il punto di STOP ④ e' la ragione** · **5** sigillo → **DA FARE**, ### **e ora ha DUE requisiti nuovi: le tre grandezze scoperte, e il verdetto su `_g_peqn_mediana`** · **6** referto e STOP → **qui** · **7** i fatti mancanti → **IN CODA**.

## ✅ **CHE COSA RESTA IN PIEDI DI TUTTO IL GIRO, perche' non e' poco**

**Il contratto dell'ordine e' nel repo e non c'era** · **la sequenza delle estrazioni e' misurata** · **la soglia dell'associativita' e' misurata e coincide con due misure indipendenti** · ### **tre grandezze scoperte dal sigillo sono state TROVATE PRIMA di scrivere il sigillo** · ### **e il blocco al punto unico ha un nome, una riga e una causa** invece di essere scoperto da un sigillo che cade.

### 🛑 **MI FERMO QUI.** Il punto di STOP ④ e' quello che il task history ha fissato **prima** di cominciare, ### **e scattava proprio per non farmi riordinare le scritture credendo di spostarle.**

---

# ⛔ **UN DIFETTO LATENTE NEL SIMULATORE: `mitosi` legge `peq` AGLI ARCHI SBAGLIATI, in silenzio** *(2026-10-02)*

> ### **Luca, il rilievo del guardiano e' giusto, e il mio strumento aveva trovato LA RIGA ma non IL DIFETTO: la segnalava come «non spostabile», non come «lettura gia' sbagliata».**

Strumento da **`be5c8133`** a ### **`2f2fc229`**. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo. **Voce: `PEQ-SEL-STANTIO`.**

## ⛔ **IL DIFETTO, in tre righe**

```
:7287   sel = ...                                                                  <- l'indice
:7433   self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])   <- RIFILTRA
:7472   peq_sel = self.peq[sel]        # dentro `if COPPIA_DENSITA:`                <- STANTIO
```

### ➜ **Dopo `:7433` lo stesso indice punta a UN'ALTRA VOCE**, perche' `keep` ha **tolto** gli archi spezzati. ### **E lo fa IN SILENZIO**, e la ragione e' precisa: l'array e' ### **PIU' LUNGO** *(`m − len(sel) + 2·len(sel) = m + len(sel)`)*, quindi ### **l'indice resta VALIDO** — nessuna eccezione, nessun `NaN`, nessuna lunghezza fuori posto.
### ✅ **OGGI NON GIRA:** il gate e' `COPPIA_MIT > 0.0 AND COPPIA_DENSITA`, e ### **`COPPIA_DENSITA = False`** sia come default di modulo *(`:1714`)* sia **dal runtime** con l'argv del driver. ### **E' un difetto LATENTE.**

## ✅ **IL CASO CHE DEVE FALLIRE: lo strumento l'ha trovato DA SOLO**

Come chiedi, l'ho usato come ### **caso che deve fallire del mio stesso strumento**, e il rilevatore nuovo lo trova ### **per quello che e'**:

```
### TROVATE: 1
### :7472  `peq_sel = self.peq[sel]`  <- legge `peq[sel]` con l'indice STANTIO
        la riscrittura CON FILTRO e' a :7433, maschera `keep`
        l'indice `sel` e' assegnato a :7287 e NON riassegnato in mezzo
        gate: COPPIA_MIT > 0.0  AND  COPPIA_DENSITA
        ### GIRA col driver: NO   (COPPIA_DENSITA = False)
```

### ⚠ **E la differenza fra i due criteri non e' cosmetica:** il criterio vecchio chiedeva *«questa istruzione si puo' spostare?»*; ### **il nuovo chiede «questa lettura e' GIA' sbagliata?»** — e sono due domande diverse che cadono sulla stessa riga per ragioni diverse.
### ⭐ **LA REGOLA E' DICHIARATA, perche' il verdetto dipende da lei:** una riscrittura e' ### **con FILTRO** se il pezzo che porta il vecchio contenuto e' `self.x[M]` **indicizzato** *(### **una pura estensione non conta**: non sposta gli indici preesistenti)*; e un indice e' ### **STANTIO** se e' assegnato **prima** della riscrittura e ### **non riassegnato in mezzo.**
### ⚠ **E il LIMITE, dichiarato:** un indice **passato a una funzione che lo rimappa** ### **non si vede** — l'analisi e' locale alla funzione.

## ✅ **E HO CERCATO ALTRI CASI, come chiedi: nel perimetro e' L'UNICO**

Sulle cinque funzioni *(`mitosi`, `semina`, `_allaccia`, i due `_eredita_*`)*: ### **1 trovato, 0 che girano.**
### ➜ **E la ragione per cui gli altri non ci sono e' strutturale, non fortuna:** le altre riscritture per arco *(`d`, `d0`, `vd`, `_rep`, `tw`, `twp`, `i`, `j`)* sono ### **rifiltrate con `keep` ma NON vengono piu' lette a indice pre-mitosi dopo**; e le grandezze per ### **NODO sono solo ESTESE**, quindi gli indici dei genitori restano validi. ### **Lo dico cosi' perche' «non ce ne sono altri» con una ragione vale, senza una ragione e' una speranza.**

## 📌 **E UNA COSA CHE LA CURA, QUANDO SI FARA', DOVRA' GUARDARE IN FACCIA**

Gli archi di `sel` sono ### **esattamente quelli con `keep` FALSE**: dopo `:7433` ### **non esistono piu' affatto.** ### ➜ **Quindi non c'e' una «rimappatura» dell'indice: c'e' la constatazione che quella lettura NON HA UN SIGNIFICATO dopo la riscrittura.** ### **Che cosa la chiuderebbe: una decisione su che cosa `COPPIA_DENSITA` debba leggere** — il `peq` dell'arco **PADRE** prima dello spezzamento *(e allora la lettura va prima)*, oppure quello dei due archi **FIGLI** *(e allora gli indici sono altri)*. ### **Non la prendo io.**

## ✅ **E NON LA CURO ORA, come hai deciso**

Il commit 3 deve ### **preservare il comportamento dei rami che GIRANO**, e una cura di un ramo spento infilata la' dentro sarebbe ### **un secondo cambiamento nello stesso commit** *(par.5)*. ### **E se il blocco unico spostasse NATURALMENTE quella lettura prima della riscrittura, lo DICHIARO come cura del ramo spento, separata e nominata** — non assorbita in silenzio.

---

# 🔧 **VIA (b) PASSO 1: LA REGOLA DI CONFRONTO ESTESA E IL SUO SIGILLO, committati PRIMA di girare** *(2026-10-02)*

> ### **Luca, ho preso la tua decisione nell'ordine che hai dato. E il presidio mi ha RIFIUTATO di girare il sigillo prima del commit: la scelta del nome ha funzionato.**

`csv/_confronto_nascita.py` *(**`cf00b8dc`**)* · `csv/_seal_fork/_sigillo_confronto_esteso.py` *(**`f1f7d783`**)*. ### **Nessuna riga del simulatore:** blob `3ddc56d9` prima e dopo.

## ⭐ **LA REGOLA NUOVA: TRE INSIEMI, e il terzo parte da CIO' CHE LA GRANDEZZA E'**

| # | l'insieme | da dove viene |
|--:|---|---|
| **1** | **REGISTRO** | `REGISTRO_NOMI` del modulo — **45** |
| **2** | **CONTATORI** | `_` piu' **INTERO** *(la regola di oggi)* — **14** |
| ### **3** | ### **SCRITTE NELLA NASCITA** | ### **l'AST**: ogni `self.<nome>` scritto dal perimetro della nascita, che non sia in (1) ne' (2), ### **e di cui qualcuno si accorga** — letto altrove nel simulatore **oppure** riportato in un file **TRACCIATO** da git — **7** |

### ✅ **PERCHE' LA TERZA CONDIZIONE NON E' UN CAPRICCIO**
Senza di lei l'insieme prenderebbe ### **anche le variabili di servizio che nessuno guarda**, e ### **un sigillo che confronta cio' che nessuno legge fallirebbe per RUMORE.** Con lei una grandezza entra ### **se e solo se un cambiamento su di lei sarebbe VISIBILE a qualcuno** — il codice o un referto. ### **E' la definizione di «cio' che la grandezza E'», non del suo nome.**

## ⛔ **E UN DIFETTO CHE HO PRESO AL PRIMO GIRO, e non era ovvio**

Col solo `hasattr`, ### **`_g_peqn_mediana` NON entrava nell'insieme**: non esiste sulla rete appena costruita, nasce ### **solo dopo uno Schwinger.** ### ➜ **Quindi avevo la regola giusta e la grandezza sfuggiva comunque, perche' la foto si prendeva troppo presto.**
### ✅ **Curato: le ASSENTI entrano MARCATE**, e il referto dice ### **quali non sono MAI apparse** invece di tacerle — ed e' il **braccio `F`** del controllo unico, applicato qui. ### **Sono 37**, fra cui `_g_peqn_mediana` e `ultima_frac_antifase` *(quest'ultima non esistera' mai, perche' `ANTIFASE_ADD` e' spento: e lo si DICE)*.

## ✅ **IL SIGILLO: TRE bracci, e il terzo non e' facoltativo**

| braccio | che cosa dimostra |
|---|---|
| ### **A -- LA REGOLA** | elenca ### **che cosa confronta e PERCHE'**, e nomina ### **cio' che la regola di oggi si perde.** Fallisce se le **tre** grandezze del contratto non ci sono |
| ### **B -- IL CASO CHE DEVE FALLIRE** | una COPIA del simulatore con ### **`_g_peqn_mediana` cambiata di UN ULP** *(`np.nextafter`: la perturbazione **piu' piccola possibile**, ### **non un numero scelto**)*. ### **La regola NUOVA deve CADERE, quella di OGGI NO** — e se la vecchia la vedesse, ### **il caso non proverebbe nulla** |
| ### **C -- L'INVOLUCRO** | due bracci sul simulatore ### **NON modificato** devono dare ### **zero differenze con ENTRAMBE** le regole |

### ⭐ **PERCHE' `C` NON E' FACOLTATIVO, e lo scrivo prima:** `STANDARD 1` dice che ### **un criterio di DIFFERENZA passa piu' facilmente PROPRIO col banco rotto.** Il braccio `B` chiede *«i due DEVONO differire»*, quindi ### **prima vanno confrontati due bracci IDENTICI** — senno' lo `0` della regola vecchia potrebbe voler dire *«il banco e' rotto»* invece di *«la regola vecchia non vede»*.

### ✅ **E `_g_peqn_mediana` E' IL CASO GIUSTO, non una scelta comoda:** e' ### **solo ASSEGNATA e mai LETTA da nessun codice** *(verificato su tutto il repo: le occorrenze sono il simulatore, le sue copie, e i referti)*. ### ➜ **Quindi un ulp su di lei e' INERTE su tutto il resto**, e la differenza che il sigillo deve vedere e' ### **esattamente UNA.** ### **Se il braccio `B` ne trovasse due, la copia non e' chirurgica — e il sigillo lo dice.**

## ⛔⛔ **E IL RILIEVO SUL PRESIDIO E' PIU' GRAVE DI COME L'AVEVO SCRITTO: I SIGILLI DI QUESTO LAVORO NON SONO COPERTI**

**Misurato:** `csv/` ha ### **68 script `_sigillo_*`** *(coperti dal rifiuto)* e ### **SEI `_sig_*`** *(NON coperti)*. E i sei sono:

| | referti TRACCIATI |
|---|--:|
| ### **`_sig_controllo_unico`** *(il sigillo del **COMMIT 1** del riordino)* | ### **7** |
| ### **`_sig_nascita_psi`** *(`PSI-FLASH`)* | ### **6** |
| ### **`_sig_decisione_separata`** *(il sigillo del **COMMIT 2**)* | ### **2** |
| `_sig_max_nodi` · `_sig_sched_tipi` · `_sig_segni_una_legge` | 0 |

### ➜ **Il rifiuto e' condizionato a `startswith('_sigillo_')`, e `_sig_` NON lo soddisfa:** ### **quei tre sigilli potrebbero girare DIRTY e produrre un referto committato senza che nulla lo impedisca.**
### ⚠ **E la cosa peggiore e' che il prefisso SOMIGLIA:** chi legge `_sig_` ### **crede di essere nella classe protetta.**
### ✅ **NON HO RINOMINATO NIENTE:** una rinomina cambierebbe il nome di ### **tre sigilli con referti committati**, e ### **i reperti non si riscrivono** *(par.9)*. Il sigillo **nuovo** si chiama `_sigillo_*` ### **di proposito**, e ### **il presidio HA RIFIUTATO DAVVERO** al primo tentativo, prima del commit — che e' la prova che la scelta funziona.
### 🛑 **DECIDE LUCA:** rinominare i tre, oppure ### **cambiare il criterio del rifiuto da «il NOME» a «CIO' CHE LO SCRIPT FA»** *(produce un referto committato)* — che e' la via **(b)** gia' scritta in `PRESIDIO-RIFIUTO-SOLO-SIGILLI`.

**PROSSIMO: il giro corto, poi il giro vero del sigillo, e il suo referto.**

---

# ✅✅ **IL SIGILLO DELLA REGOLA ESTESA PASSA: TRE BRACCI SU TRE** *(2026-10-02, via (b) passo 1)*

> ### **Luca: la regola nuova vede l'ULP e quella di oggi NON lo vede. E' esattamente il caso che hai chiesto, nei due versi.**

*(72 passi, scena grande, seme 11. Sigillo `f1f7d783`, regola `cf00b8dc`, simulatore **`3ddc56d9`** — ### **nessuna riga toccata.** Referto: `csv/_seal_fork/_sigillo_confronto_esteso/`.)*

## ✅ **BRACCIO `B` — IL CASO CHE DEVE FALLIRE, e passa nei DUE versi**

| | |
|---|---|
| la **copia** | ### **CHIRURGICA: UNA riga diversa**, `:7505`, con `np.nextafter(..., inf)` — ### **la perturbazione piu' piccola possibile**, non un numero scelto |
| ### **la regola NUOVA** | ### **1 differenza, ed e' ESATTAMENTE `_g_peqn_mediana`**: `1.7026985177180012` contro `1.7026985177180014`, ### **1 ulp** |
| ### **la regola di OGGI** | ### **0 differenze** — ### **non la vede** |

### ➜ **E il secondo verso e' quello che rende il caso una PROVA e non una constatazione:** se la regola vecchia l'avesse vista, ### **vorrebbe dire che era gia' coperta** e il caso non proverebbe niente.
### ✅ **E che la differenza sia UNA SOLA conferma che `_g_peqn_mediana` e' il caso giusto:** e' ### **solo assegnata, mai letta**, quindi un ulp su di lei ### **non propaga.** Se il braccio ne avesse trovate due, la copia non era chirurgica.

## ✅ **BRACCIO `C` — L'INVOLUCRO: 0 differenze su ENTRAMBE le regole**

Due bracci sul simulatore **non modificato**, 72 passi: ### **zero differenze su 231 grandezze scattate.**
### ➜ **Senza questo braccio lo `0` della regola vecchia nel `B` sarebbe illeggibile** — potrebbe voler dire *«il banco e' rotto»* invece di *«la regola vecchia non vede»*. ### **E' `STANDARD 1` letto al contrario, e qui serviva davvero.**

## ✅ **BRACCIO `A` — LA REGOLA: che cosa confronta, e PERCHE'**

| classe | quante |
|---|--:|
| **registro** | 45 |
| **contatori** *(`_` piu' intero)* | 179 |
| ### **scritte nella nascita** | ### **24** |
| ### **TOTALE nell'insieme** | ### **248** |
| scattate nella foto | 231 |
| ### **che la regola di OGGI si perde** | ### **24** |

### ✅ **E le TRE del contratto ci sono tutte:** `_g_peqn_mediana` · `ultima_prob_coppia` · `ultima_frac_antifase`.
**Le altre 21 che oggi sfuggono** sono `conc_archi`, `coppie_nate`, `masse_info`, `nati`, `negate` *(lette fuori dal perimetro)* e i contatori nati dentro la nascita.

## ✅ **E LE 17 «MAI APPARSE» SI DICONO, invece di tacerle** *(il braccio `F` del controllo unico, applicato qui)*

Fra loro ### **`ultima_frac_antifase`** *(`ANTIFASE_ADD` e' **spento**: non esistera' mai in questa configurazione)* e ### **`_smp_d` / `_smp_d0`**, che sono ### **grandezze a FINESTRA**: esistono **solo dentro** il passo, e la foto si prende **fra** due passi.
### ➜ **Nessuna delle due e' un difetto, ed e' la ragione per cui vanno DETTE:** un'assenza dichiarata e' informazione; ### **un'assenza silenziosa e' un buco.**

## ⚠ **E IL GIRO CORTO E' UN DATO, non un inconveniente**

A **3 passi** il braccio `B` ### **FALLISCE**, perche' senza uno Schwinger ### **`_g_peqn_mediana` non nasce** e non c'e' niente da confrontare.
### ➜ **Quindi il sigillo NON PASSA A VUOTO**, e questo l'ho visto **prima** del giro vero. ### **Un sigillo che passasse anche quando la grandezza non esiste non starebbe misurando la regola: starebbe misurando se stesso** (`P1-sexies`).

**PROSSIMO: il passo 2 — `_g_peqn_mediana` presa UNA volta, a un istante DICHIARATO. Il disegno e' pronto e il codice NON e' ancora scritto.**

---

# 🔧 **VIA (b) PASSO 2: `_g_peqn_mediana` HA UN ISTANTE DICHIARATO. Il blocco al punto unico non c'e' piu'** *(2026-10-02)*

> ### **Luca, il codice c'e' e il sigillo NON e' ancora girato: lo committo prima, come chiede il par.5. E il blocco e' sparito: la misura lo dice.**

Simulatore da **`3ddc56d9`** a ### **`3d78cfd2`** *(sha1 byte grezzi)*. ### **DUE sostituzioni**, ognuna asserita per se'.

## ⭐ **L'ISTANTE, e perche' QUESTO e non un altro**

> ### **LO STATO DA CUI LA NASCITA DEL PASSO PARTE.**

| | |
|---|---|
| ### **perche' e' l'unico NON AMBIGUO** | *«dopo la nascita completa»* dipenderebbe da ### **quali rami sono scattati** dentro `mitosi` *(Schwinger si'/no, quanti archi)*: due passi darebbero mediane prese su stati diversi ### **per ragioni diverse** |
| ### **la FORMA, minima** | il valore si **cattura in una LOCALE** in testa a `mitosi`; ### **l'assegnazione resta DOV'ERA**, sotto le sue tre condizioni ⇒ ### **il GATE non cambia, cambia SOLO il numero** |
| ### **e l'assegnazione smette di essere una LETTURA di `peq`** | ed e' ### **esattamente** cio' che la toglie dalla strada del punto unico |

### ⛔ **E IL NUMERO CAMBIA, e lo dichiaro prima di misurarlo:** era la mediana ### **DOPO** la riscrittura della mitosi, ora e' quella ### **PRIMA**. ### **La differenza e' esattamente l'effetto di quella riscrittura sulla mediana** — e il sigillo esteso deve vedere ### **QUELLA e nient'altro.**

## ✅ **IL COSTO, MISURATO e non stimato**

`np.median` su **471564** float: ### **`0.0053 s`**, cioe' lo ### **`0.187 %`** di un passo da `2.849 s`. E il gate della cattura e' **cheap** *(due booleani e una lunghezza)*, quindi ### **la mediana si paga solo nei passi in cui una divisione c'e' davvero.**

## ✅ **E IL BLOCCO AL PUNTO UNICO NON C'E' PIU': la misura lo dice**

Rigirato `csv/_test_fork/_punto_unico_fattibile.py` sul simulatore nuovo:

| | prima | ### **dopo** |
|---|--:|--:|
| segnalate | 7 | **6** |
| girano col driver | 5 | **4** |
| ### **GENUINE a granularita' di indice** | ### **3** | ### **2** |

### ➜ **E le due che restano sono quelle che avevo GIA' dichiarate non-bloccanti**, col loro perche': `:7524 dd` *(la lettura di `pos` e' una pura **estensione**, e il flusso locale `dd` si solleva prima del blocco)* e `:7531 pmed` *(con `PEQ_NASCITA_LOCALE = True` ### **la mediana non viene nemmeno valutata**)*.
### ✅ **Quindi il blocco e' caduto, e non per una mia lettura: per la stessa misura che l'aveva trovato.**

## ⚠ **E LA RAGIONE PER CUI IL SIGILLO E' VENUTO PRIMA, detta col numero**

La regola di confronto di ieri *(registro piu' `_`-e-intero)* ### **NON guardava `_g_peqn_mediana`** — comincia con `_` ### **ma e' un `float`.** ### ➜ **Quindi questa cura sarebbe passata IN SILENZIO**, e ### **il difetto non sarebbe stato il cambiamento: sarebbe stato il non vederlo** (`A8`). ### **L'ordine che hai dato era quello giusto, e ora ha un numero.**

## 📌 **E `PEQ-SEL-STANTIO` NON e' curato qui, come hai deciso**

Il difetto latente di `:7472` *(`COPPIA_DENSITA`, il `peq` degli archi sbagliati)* ### **resta registrato e intatto.** ### **E questa cura non lo tocca:** sposta la cattura di un **diagnostico**, ### **non la lettura di `peq_sel`** — che vive in un ramo spento e va decisa a parte.

**PROSSIMO: il sigillo del passo 2 — la differenza ATTESA invece che INIETTATA. Deve essere UNA.**

---

# ⛔ **UN'OMISSIONE MIA, recuperata subito: il referto che prova il commit precedente non era nel commit precedente** *(2026-10-02)*

Nel messaggio di **`f541261`** ho scritto i numeri del punto unico *(segnalate `7 -> 6`, girano `5 -> 4`, ### **genuine `3 -> 2`**)* ### **citandoli come prova che il blocco e' caduto** — e ### **il referto che li contiene non era in quel commit.**

| | |
|---|---|
| i file | `csv/_test_fork/_punto_unico_fattibile/_corsa.txt` e `_punto_unico_fattibile.json`, **rigirati** sul simulatore `3d78cfd2` |
| ### **che cosa sarebbe successo** | chi legge `f541261` da un clone fresco ### **trova i numeri nel messaggio e nel repo il referto VECCHIO**, quello del simulatore `3ddc56d9` — ### **cioe' il referto che dice che il blocco C'E'** |
| ### **la famiglia** | ### **e' `git add` di cio' che il commit DICHIARA invece di cio' che prova**, ed e' ### **la stessa omissione di `_guasto_ripieghi.json` del 2026-10-01** *(un referto rigirato e mai committato)* |

### ➜ **E' un RITARDO, e il recupero non lo sana: lo conferma** *(par.4)*. ### **Lo dico invece di infilare i due file nel prossimo commit come se ci fossero sempre stati.**
### 📌 **E la causa e' precisa:** ho guardato `git status` *(come mi ero imposto)*, ho visto i due file ### **e ho messo nel `git add` solo cio' che avevo in testa** — il codice e i documenti. ### **Guardare lo stato non basta se non si legge cio' che dice.**

---

# 🔧 **IL BRACCIO `D` DEL SIGILLO ESTESO: LA DIFFERENZA ATTESA, committato PRIMA di girare** *(2026-10-02)*

Sigillo da **`f1f7d783`** a ### **`80863806`**. ### **Nessuna riga del simulatore:** blob `3d78cfd2` prima e dopo.

## ⭐ **LA DIFFERENZA FRA `B` E `D`, ed e' il punto**

| | |
|---|---|
| ### **`B`** | ### **INIETTA** una differenza *(un ulp, in una copia guasta)* → mostra che la regola ### **la VEDE** |
| ### **`D`** | ### **NE ASPETTA UNA** *(quella della cura)* → mostra che la regola vede ### **esattamente cio' che e' cambiato e NIENTE DI PIU'** |

### ➜ **Sono i due versi della stessa domanda, e servono entrambi.** E i criteri di `D` sono fissati **ora**: ### **DUE differenze ⇒ la cura ha toccato qualcos'altro e il commit NON passa; ZERO ⇒ la cura non ha fatto niente.**

## ⚠ **E IL «PRIMA» NON VIENE DA `HEAD`**

Viene da ### **`_cli_flag.sim_prima_del_flag`**, ancorato al ### **PADRE del commit che introduce `_peqn_med_pre`**, estratto ### **in BINARIO** *(par.7: non `git checkout`)* e con l'assertazione che ### **quell'ancora NON ci sia nel file estratto.**
### 📌 **E' `H-P8`, e il difetto che esiste per impedire ha un numero:** ### **`ANCORE-1`, 25 sigilli che prendevano «il codice di prima» da `HEAD`** e ### **diventavano VUOTI appena la cura era committata.**

**PROSSIMO: il giro vero, quattro bracci. Poi il referto, e il commit 3.**

---

# ⛔ **IL SIGILLO SI E' RIFIUTATO DI GIRARE, E AVEVA RAGIONE: la mia ancora nominava la FORMULA invece del BERSAGLIO** *(2026-10-02)*

> ### **Luca, il giro a quattro bracci non e' partito. Non ha prodotto un verdetto sbagliato: si e' FERMATO, e il motivo e' un difetto mio.**

Sigillo da **`80863806`** a ### **`8df62ea6`**. ### **Nessuna riga del simulatore:** blob `3d78cfd2` prima e dopo.

## ⛔ **CHE COSA HA DETTO, per intero**

```
** l'ancora della copia guasta e' presente 0 volte (attesa 1). NON scrivo la copia. **
```

### **L'ancora era `self._g_peqn_mediana = float(np.median(self.peq))`** — cioe' ### **il MODO in cui il valore si calcola.** E ### **il passo 2 ha cambiato ESATTAMENTE quella riga** *(ora legge la locale `_peqn_med_pre`)*. ### ➜ **Quindi l'ancora non c'era piu'.**

## ✅ **IL PRESIDIO HA FUNZIONATO, e va detto per primo**

Il sigillo ### **non ha scritto una copia non guasta** e ### **non ha consegnato un verdetto**: si e' fermato con l'assertazione dell'ancora *(`P1-quater`: si conta l'ancora e si FALLISCE se non e' unica)*.
### 📌 **Se non l'avessi messa, la copia sarebbe stata IDENTICA all'originale**, il braccio `B` avrebbe trovato ### **ZERO differenze**, e ### **avrei letto quello zero come «la regola nuova non vede l'ulp»** — cioe' avrei concluso ### **il contrario del vero.** ### **Un quarto falso zero, evitato da un'assertazione.**

## ⛔ **MA L'ANCORA ERA FRAGILE PER COSTRUZIONE, e questo e' il difetto mio**

| | |
|---|---|
| che cosa **nominava** | ### **la FORMULA**: `= float(np.median(self.peq))` |
| che cosa il sigillo **perturba** | ### **il VALORE MEMORIZZATO** in `self._g_peqn_mediana` |
| ### ➜ **lo scarto** | ### **nominava il MODO invece del BERSAGLIO** — e un modo cambia, un bersaglio no |

### ✅ **LA CURA: l'ancora e' l'ASSEGNAZIONE**, `self._g_peqn_mediana = _peqn_med_pre`, e la copia guasta avvolge ### **il membro destro qualunque sia**: `float(np.nextafter(_peqn_med_pre, np.inf))`.
### ➜ **Cosi' sopravvive a un cambio di come il valore si calcola** — che e' esattamente cio' che e' appena successo.
*(E `np.nextafter(nan, inf)` resta `nan`: col gate falso la copia e' inerte, come l'originale.)*

## ⚠ **E UNA CONSEGUENZA SUL REFERTO DI PRIMA, che dichiaro**

Il referto di **`81b0c24`** e' stato prodotto sul simulatore ### **`3ddc56d9`**, e il suo `json` lo porta scritto *(`blob_sim_sha1_byte`)*. ### **Sul simulatore di ora (`3d78cfd2`) quel sigillo, come era committato allora, SI RIFIUTEREBBE di girare.**
### ➜ **Non e' un referto sbagliato: e' il referto di un BLOB PRECISO**, e si legge con quel blob davanti — ### **che e' la ragione per cui il blob sta nel `json` e non solo nel messaggio di commit.**
### ✅ **E il giro che segue lo SOSTITUISCE**, su `3d78cfd2`, con ### **quattro bracci invece di tre.**

## 📌 **E LA FAMIGLIA DELL'ERRORE E' GIA' NEL REPO, col suo nome**

### **E' `ANCORE-1`** — *25 sigilli che prendevano «il codice di prima» da `HEAD` e diventavano VUOTI appena la cura era committata.* ### **Qui non e' il «prima» a essere scaduto: e' l'ANCORA DELL'INIEZIONE** — e la forma e' la stessa: ### **un sigillo che si svuota perche' il codice sotto si e' mosso.**
### ⚠ **E la lezione operativa sta in una riga:** ### **un'ancora d'iniezione nomina CIO' CHE SI PERTURBA, non come lo si calcola.**

**PROSSIMO: il giro vero, quattro bracci, sul simulatore `3d78cfd2`.**

---

# ⛔ **IL BRACCIO `D` E' MORTO SU UN MIO ERRORE DI API. Committo il fallimento PRIMA di correggerlo** *(2026-10-02)*

> ### **Luca, `A`, `B` e `C` passano sul simulatore nuovo. Il braccio `D` non e' nemmeno partito, e la ragione e' banale e mia.**

**Il reperto:** `csv/_seal_fork/_sigillo_confronto_esteso/_corsa_2026-10-02_FALLITO_braccio_D.txt`. ### **Nessuna riga del simulatore:** blob `3d78cfd2`.

## ✅ **CIO' CHE IL GIRO HA GIA' DETTO, e va detto per primo**

| | |
|---|---|
| la **copia guasta** | ### **CHIRURGICA**: una riga, `:7539` — ### **l'ancora nuova ha funzionato** |
| ### **braccio `B`** | ### **PASSA**: la regola nuova vede ### **1 differenza, ed e' `_g_peqn_mediana`** *(`1.7026802215251897` contro `1.70268022152519`, ### **1 ulp**)*; la regola di OGGI ne vede ### **ZERO** |
| ### **braccio `C`** | ### **PASSA**: 0 differenze con ### **entrambe** le regole |
| **braccio `A`** | **PASSA** |

### 📌 **E il valore della mediana e' CAMBIATO rispetto a ieri sera**, come avevo dichiarato: ### **`1.7026985177180012` prima, `1.7026802215251897` ora.** ### **E' l'effetto della cura del passo 2** — e il braccio `D` esiste proprio per misurarlo invece di constatarlo.

## ⛔ **L'ERRORE: ho usato il VALORE DI RITORNO come un PERCORSO**

```
FileNotFoundError: No such file or directory: 'f54126119edc92157688c07b6449d2ce5588615d'
```

### **`_cli_flag.sim_prima_del_flag(nome_flag, dest)` SCRIVE su `dest` e RESTITUISCE L'HASH DEL COMMIT** che introduce l'ancora. ### **Io ho trattato il ritorno come il percorso del file.**
### ➜ **E l'ho letto nel docstring DOPO**, non prima: ### **e' `P1` — ho usato un'API per associazione** *(«una funzione che estrae un file restituisce il file»)* ### **invece di leggere che cosa restituisce.**

## ✅ **CHE COSA QUESTO NON E', e conta dirlo**

### **Non e' un fallimento del SIGILLO: e' un errore dello STRUMENTO.** `A`, `B` e `C` hanno misurato e passato ### **prima** che `D` morisse, e i loro numeri sono nel reperto.
### ⚠ **Ma il referto `json` NON e' stato scritto** *(il crash e' arrivato prima)*, quindi ### **quei tre bracci non hanno un referto strutturato**: resta ### **la stampa**, committata come reperto. ### **Lo dico invece di citare numeri che nel repo non hanno un `json`.**

## ✅ **E IL FALLIMENTO SI COMMITTA PRIMA DELLA CORREZIONE** *(par.5)*
### **La correzione e' un commit a se', e il giro si rifa' dopo.** ### **Non lo aggiusto dentro questo commit.**

---

# ✅ **LA CORREZIONE DEL BRACCIO `D`, un commit a se'** *(2026-10-02)*

Sigillo da **`8df62ea6`** a ### **`11b4f20e`**. ### **Nessuna riga del simulatore:** blob `3d78cfd2`.

### **`dest` e' il PERCORSO, il valore di ritorno e' il COMMIT.** E il ritorno non si butta: ### **si RIPORTA nel referto** come *«il commit che introduce l'ancora»*, perche' ### **dice a chi legge su quale coppia di blob il confronto e' ancorato** — ed e' l'informazione che `H-P8` esiste per rendere verificabile.
### 📌 **E il commento sul difetto resta nel codice**, accanto alla riga: ### **letto il docstring DOPO, non prima** — `P1` applicato a un'API, usata per **associazione** *(«una funzione che estrae un file restituisce il file»)* invece che per cio' che **dichiara**.

**PROSSIMO: il giro vero, quattro bracci.**

---

# ✅✅ **IL SIGILLO A QUATTRO BRACCI PASSA. IL PASSO 2 E' CHIUSO CON LA SUA PROVA** *(2026-10-02)*

> ### **Luca: la cura ha cambiato ESATTAMENTE un numero, e la regola di OGGI non lo avrebbe visto. Il tuo ordine era quello giusto, e ora ha due numeri invece di uno.**

*(72 passi, scena grande, seme 11. Sigillo **`11b4f20e`**, regola `cf00b8dc`, simulatore **`3d78cfd2`**.)*

## ✅ **BRACCIO `D` — LA DIFFERENZA ATTESA, ed e' UNA**

| | |
|---|---|
| il **«prima»** | ### **`3ddc56d9`**, dal ### **PADRE del commit che introduce `_peqn_med_pre`** *(`f541261^`)*, estratto **in BINARIO** |
| ### **la regola NUOVA** | ### **1 differenza**: `_g_peqn_mediana` da ### **`1.7026985177180012`** a ### **`1.7026802215251897`** |
| ### **la regola di OGGI** | ### **0 differenze** — ### **NON la vede** |

### ➜ **E questo e' il numero che giustifica l'ordine che hai dato:** ### **la cura del passo 2 sarebbe passata IN SILENZIO** col sigillo di ieri. ### **Non perche' fosse sbagliata — perche' nessuno la guardava** (`A8`).
### ✅ **E che la differenza sia UNA SOLA e' il criterio che avevo fissato prima:** ### **due ⇒ la cura aveva toccato qualcos'altro e il commit non passava; zero ⇒ non aveva fatto niente.** ### **E' una, ed e' quella.**

## ✅ **E GLI ALTRI TRE, sul simulatore nuovo**

| braccio | esito |
|---|---|
| **`A`** la regola | ### **PASSA** |
| ### **`B`** l'ulp **iniettato** | ### **PASSA**: 1 differenza *(`_g_peqn_mediana`, **1 ulp**)*, e ### **0 con la regola di oggi** |
| **`C`** l'involucro | ### **PASSA**: ### **0 differenze con ENTRAMBE** le regole |
| la **copia guasta** | ### **CHIRURGICA**: una riga, `:7539` — ### **l'ancora sull'ASSEGNAZIONE tiene** dove quella sulla formula era caduta |

### 📌 **E `B` e `D` insieme dicono due cose diverse, ed e' per questo che sono due:** `B` prova che la regola ### **vede anche un ULP**; `D` prova che vede ### **esattamente cio' che e' cambiato e niente di piu'.**

## ✅ **E NEMMENO IL «PRIMA» SI COMMITTA, per la stessa ragione della copia guasta**

Lo ### **estrae `sim_prima_del_flag`** dal padre del commit, a ogni giro. ### **Il repo ha GIA' quel blob nella sua storia:** committarne una copia ### **sarebbe duplicare git** — e creare un secondo artefatto che puo' scadere. E' in `.gitignore` col motivo.

## 📋 **IL PUNTO DOVE SIAMO, sulla tua decisione**

| passo | stato |
|---|---|
| **1** — ### **il SIGILLO** | ### **FATTO e PROVATO** *(quattro bracci)* |
| **2** — ### **il DIAGNOSTICO** | ### **FATTO e PROVATO**: la differenza attesa e' **una**, e la regola di ieri non l'avrebbe vista |
| **3** — il **PUNTO UNICO** | ### **PROSSIMO** |

---

# ⛔ **IL QUINTO FALSO ZERO DELLA SESSIONE, E L'HO TROVATO IO PRIMA DI USARLO** *(2026-10-02)*

> ### **Luca: prima di scrivere una riga del commit 3 ho misurato una cosa che lo strumento dello STOP 4 NON aveva misurato. La prima risposta era ZERO, ed era FALSA. Te la racconto perche' lo zero l'ho smontato io, e perche' questa forma d'errore ora ha un NOME nell'indice.**

## 📌 **LA DOMANDA CHE MANCAVA, e sono DUE domande diverse**

| | |
|---|---|
| lo **STOP 4** chiedeva | le scritture della nascita si possono rendere ### **CONTIGUE**? *(si puo' spostare FUORI il codice che sta fra loro)* |
| ### **questa chiede** | le scritture si possono ### **PERMUTARE FRA LORO**? *(il piano vuole <<**nell'ordine del REGISTRO**>>)* |

### ➜ **La seconda puo' dire NO con la prima che dice SI**, e ### **non l'avevo misurata.** *(Strumento nuovo: `csv/_test_fork/_ordine_registro.py`.)*

## ⛔ **LA PRIMA RISPOSTA: <<zero dipendenze, l'ordine del registro e' raggiungibile>>. FALSA.**

### **Il motivo e' sempre lo stesso, ed e' il quinto:** facevo girare l'analisi sul ### **solo `REGISTRO_STATO`** (30 voci) — e cosi'

| grandezza | dove sta davvero | che cosa l'esclusione nascondeva |
|---|---|---|
| `phi`, `i`, `j` | ### **`REGISTRO_METRI`** | `i`/`j` sono la ### **topologia**; `phi` e' la fase che ### **`twp` LEGGE** |
| `_peqn_idx` | ### **in NESSUN registro** | il commento al sorgente `:7588` ### **DICHIARA** la dipendenza: *<<la marca va QUI, DOPO il `concatenate`: gli indici si riferiscono all'array FINALE>>* |

### ⛔ **Cioe': l'insieme su cui misuravo ESCLUDEVA per costruzione le grandezze intrecciate.** ### **Uno zero cosi' non e' una misura: e' una tautologia.**

## ✅ **LA CURA, e non e' <<stare piu' attento>>: NESSUN INSIEME SCELTO A MANO**

Si prendono ### **TUTTE** le scritture del perimetro, si costruisce il ### **grafo delle dipendenze**, e ### **i contatori escono da se'** — perche' ### **non leggono e non sono letti**, non perche' io li abbia classificati.
### ✅ **E ogni arco si CLASSIFICA**, perche' un arco conservativo non e' un ostacolo: e' ### **INERTE** se la scrittura letta e' una ### **pura ESTENSIONE** e la lettura e' sui ### **soli GENITORI** *(indici `< n0`)* — li' l'ordine non puo' cambiare il valore.

## ✅ **LA MISURA VERA: 4 vincoli GENUINI, e l'ordine del registro li rispetta TUTTI**

| vincolo | perche' |
|---|---|
| ### **`phi` prima di `twp`** | `twp` legge `phi[a,b]` ### **DOPO il calcio**, e il calcio e' una scrittura INDICIZZATA sui genitori: non e' un'estensione, quindi l'arco e' **genuino** |
| ### **`peq` prima di `_peqn_idx`** | `_peqn_idx` legge `peq` ### **INTERA** — ed e' esattamente cio' che il commento DICHIARA |

### ✅ **E l'ordine del registro e' un ordine TOPOLOGICO valido:** `phi` sta in `METRI`, cioe' ### **prima** di tutto `STATO` *(dove sta `twp`)*; e `_peqn_idx`, che in nessun registro sta, va ### **dichiarato dopo `peq`** nella tabella.
*(E ci sono ### **6 chiamate con EFFETTO** — `_smp_chirurgia`, `_traccia_d0`, `_grado`, tre per evento — che ### **NON sono regole di nascita** e vanno collocate a mano e dichiarate.)*

## 📌 **E ORA LA FORMA HA UN NOME NELL'INDICE: `FALSO-ZERO`**

Ho cercato *<<falso zero>>* nell'indice: ### **ZERO voci su 879** — benche' in questa sessione la forma abbia morso ### **CINQUE volte**, e ogni volta ### **mi avesse convinto.** Ora e' una voce, con ### **le cinque occorrenze** e ### **un criterio di chiusura**.

### ➜ **LA REGOLA, in tre righe:**
### **① uno ZERO si dichiara INSIEME all'insieme su cui e' misurato** — *<<zero su N, e N comprende X>>*, mai *<<zero>>* da solo.
### **② ogni misura che PUO' rispondere zero vuole un CONTROLLO POSITIVO** (`STANDARD 2`) — ed e' esattamente cio' che ha salvato il caso dell'ancora, dove l'assertazione ha trasformato un falso zero in un ### **rifiuto**.
### **③ nessun insieme scelto a mano: l'insieme si DERIVA dal sorgente.**

### ⚠ **E oggi e' una REGOLA SCRITTA, non un presidio** (`A9`): la voce si chiude ### **quando un referto che stampa uno zero senza dichiarare l'insieme fa FALLIRE il commit.** Non e' cablato.

**PROSSIMO: il commit 3, il punto unico — e ora l'ordine della tabella e' MISURATO prima di scriverlo, non scoperto dopo.**

---

# ✅ **IL CONTRATTO DELL'ORDINE E' MISURATO. E LO STRUMENTO AVEVA TRE BUCHI, NON UNO** *(2026-10-02)*

> ### **Luca: ti ho scritto un'ora fa che la forma `FALSO-ZERO` aveva morso cinque volte. Subito dopo ha morso altre DUE, nello stesso strumento che l'aveva appena dichiarata. Le registro, perche' una voce che elenca solo i casi comodi non serve a niente.**

## ⛔ **IL SESTO: `self.n` E' UNA `@property`, e io la trattavo come un attributo**

`self.n` e' `len(self.phi)` *(`:2651`)*. ### ➜ **Quindi leggere `n` E' leggere `phi`** — e i due `_eredita_*` fanno ### **`n0 = self.n - k`**, cioe' ### **dipendono dall'estensione di `phi`.**
Lo strumento vedeva `n` come un attributo ### **senza scrittore**, e quell'arco non esisteva.
### ✅ **Cura:** le `@property` si ### **DERIVANO dal sorgente** *(nel simulatore ce n'e' **una sola**, e il referto lo dichiara)*, e una lettura di property si risolve negli attributi che legge, ### **marcati come letti INTERI** — perche' `len()` cambia a ogni estensione.

## ⛔ **IL SETTIMO: le LOCALI INTERPOSTE, e questo e' il piu' sottile**

Guardavo solo le letture ### **DENTRO** lo statement di scrittura. Ma `n0 = self.n - k` ### **non scrive `self.X`**: scrive una ### **locale.** E una locale definita ### **FRA** le scritture legge `self.*` a uno ### **STATO INTERMEDIO.**
### ✅ **Cura:** una passata sulle locali definite fra la **prima** e l'**ultima** scrittura dell'evento, con la ### **stessa classificazione genuino/inerte** degli archi.

## ✅ **E LA CLASSIFICAZIONE PAGA IN DUE DIREZIONI, che e' la ragione per cui c'e'**

| | |
|---|---|
| ### **trova 4 casi GENUINI** | tutte e quattro `n0`, e ### **leggendo il sorgente NON le avevo viste** |
| ### **scarta 2 casi INERTI** | `chi_a`/`chi_b` al `:7405` leggono `perc_chi` ### **gia' estesa** al `:7372` — ma ### **sui GENITORI**, e una pura estensione non tocca i primi `n0`. ### **Contarli per ostacoli avrebbe gonfiato la cura** (`9-ter`) |

## ✅ **IL CONTRATTO DEL COMMIT 3, ed e' SCRITTO PRIMA DEL CODICE**

| | il vincolo |
|---|---|
| **1** | ### **`phi` prima di `twp`** — rispettato: `phi` sta in `METRI`, prima di tutto `STATO` |
| **2** | ### **`peq` prima di `_peqn_idx`** — e `_peqn_idx`, che in nessun registro sta, va **dichiarato** li' |
| **3** | ### **`n0` nel CONTESTO**, calcolato nella fase di PREPARAZIONE — la regola ### **non legge `self.n`** |
| **4** | ### **6 chiamate con EFFETTO** *(`_smp_chirurgia`, `_traccia_d0`, `_grado`, tre per evento)*: ### **non sono regole**, si collocano a mano e si **dichiarano** |

### ✅ **E L'ORDINE DEL REGISTRO E' UN ORDINE TOPOLOGICO VALIDO: 0 violazioni su 4 vincoli.** La forma che il piano chiede ### **si puo' usare**, e ora lo so ### **per misura**, non per fiducia.

**PROSSIMO: il codice del commit 3, con questo contratto davanti.**

---

# 📌 **LE DUE NOTE DEL GUARDIANO, REGISTRATE PRIMA DI SCRIVERE IL COMMIT 3** *(2026-10-02)*

> ### **Nessuna delle due si cura dentro il commit 3, e nessuna delle due resta in chat.**

## ⛔ **NOTA 1 — LA MIA FRASE SULL'ANCORA E' SBAGLIATA, e il guardiano ha ragione**

Ho scritto in `6ab31f7` che l'ancora d'iniezione ora vale *<<**qualunque sia il membro destro**>>*.
### **E NON E' VERO.** L'ancora e'

```
ANCORA = "self._g_peqn_mediana = _peqn_med_pre"
```

### ➜ **e il membro destro E' DENTRO.** Se la locale cambia nome, ### **l'ancora si rompe di nuovo** — cioe' ho curato *questo* caso, non ### **la FORMA** del caso.

### ✅ **Che cosa NON e':** non e' grave. Il presidio ### **la ferma** invece di scrivere una copia non guasta, ed e' esattamente cio' che e' successo la prima volta. ### **Ma la frase prometteva una generalita' che il codice non ha**, e una frase cosi' e' ### **peggio** di nessuna frase, perche' la prossima volta mi fiderei.

### 📌 **IN CODA, COMMIT A SE' DOPO IL COMMIT 3** *(decisione di Luca)*, e ### **scelgo la seconda via**: rendere l'ancora ### **il solo BERSAGLIO** — prefisso `self._g_peqn_mediana = ` e sostituzione ### **fino a fine riga.** ### ➜ **Toglie il difetto invece di descriverlo** *(e `9-ter`: a parita' d'effetto si preferisce togliere un'eccezione)*.

## 📌 **NOTA 2 — UNA DOMANDA APERTA DI FISICA, e NON un difetto** *(`DIVISIONE-AUTOCONSISTENTE`)*

| | si calcola | legge |
|---|---|---|
| `fm` — la **fase del figlio** | `:7339-7341`, ### **PRIMA del calcio** | i genitori ### **come ERANO** |
| `twp` — la **torsione degli archi figli** | `:7470`, ### **DOPO il calcio** | `phi[a]`, `phi[b]` ### **GIA' CALCIATI** |

### ➜ **Cioe': il figlio nasce alla fase media dei genitori COME ERANO, e i suoi archi misurano la differenza di fase dai genitori COME SONO DIVENTATI.** ### **Due numeri dello stesso evento, presi a due ISTANTI diversi dello stesso passo.**

### ✅ **E IL COMMIT 3 LO PRESERVA, ed e' la cosa giusta:** e' ### **il vincolo 1 del contratto dell'ordine** *(`phi` prima di `twp`)*, misurato — e il commit 3 e' una ### **RIORGANIZZAZIONE**: se cambiasse questo ### **non sarebbe byte-identico, e non sarebbe un riordino.**

### 📌 **IL CRITERIO DI CHIUSURA** *(una voce senza criterio e' un desiderio, par.4)*: si misura se `twp` calcolato sui genitori ### **PRE-calcio** cambia l'evoluzione ### **oltre la barra d'errore.**
### ① **se NON la cambia** ⇒ i due istanti sono equivalenti, e la voce si chiude come ### **non-difetto**.
### ② **se la cambia** ⇒ allora la scelta dell'istante ### **E' FISICA**, e va ### **derivata** — non ereditata dall'ordine in cui le righe sono state scritte.
### ⚠ **NON MISURATO.**

---

# ✅ **COMMIT 3: LA NASCITA E' UN EVENTO UNICO. Il codice c'e', il sigillo NON HA ANCORA GIRATO** *(2026-10-02)*

> ### **Luca: i posti che scrivevano le grandezze della nascita erano TRE. Ora e' UNO. E il codice si committa PRIMA del run, come dice il par.5 — quindi questo messaggio NON porta un verdetto, porta il codice e il criterio.**

Simulatore da **`3d78cfd2`** a ### **`f103989b`**.

## ✅ **IL NUMERO, ed e' il bersaglio del par.(c)**

| | prima | ora |
|---|---|---|
| i **posti** che scrivono le grandezze della nascita | ### **3** *(`mitosi`, i due `_eredita_*`, piu' la MUTAZIONE di `conc_nodi`)* | ### **1** *(`nascita()`)* |
| le **regole** | sparse, due in funzioni separate | ### **72 righe** in `REGOLE_NASCITA` *(36 grandezze x 2 eventi)* |
| una grandezza **dimenticata** | passa in silenzio | ### **FERMA IL RUN** |

### ✅ **E IL PRESIDIO GIRA ALL'IMPORT**, non al primo run: una riga che manca ### **ferma il processo PRIMA che un run cominci.** *(Provato a secco: togliendo `peq` dalla tabella, `regola di nascita non dichiarata per `peq` all'evento `divisione``.)*

## 📌 **I DUE `_eredita_*` SONO ASSORBITI, e DUE COSE NON OVVIE SONO CONSERVATE**

Le loro **13 grandezze** sono righe della tabella, e ### **la ragione per cui esistevano** *(le cure `C7`/`C11`/`PSI-FLASH`)* vive nella `derivazione` di ciascuna regola — ### **nel posto dove chi legge quella grandezza la trova.**

### ⚠ **E due cose che un riordino distratto avrebbe perso:**
### **① `_nb_prec` era estesa SOLO DENTRO il ramo di `_nb`** — una dipendenza di ### **CONTROLLO**, non di dato, che ### **nessun grafo sui dati vedrebbe.** Ora passa per `c["_nb_esteso"]`.
### **② `conc_nodi` cresceva con `.append` DENTRO un ciclo**, quindi `len` cresceva a ogni giro e ### **un indice scartato all'inizio poteva passare il test piu' tardi.** La regola costruisce la lista nuova e appende ### **A QUELLA**, non alla vecchia: stesso comportamento ### **anche nel caso limite.**

## ✅ **E UN CONTATORE L'HO TOLTO, ed e' la cosa di cui vado piu' contento**

La prima stesura di `nascita()` aveva `_g_nascite`. ### **L'ho tolto**, per due ragioni:
### **① il criterio del commit 3 e' BYTE-IDENTICO**, e un contatore nuovo obbligherebbe il sigillo a ### **DICHIARARE UN'ECCEZIONE** — e ### **un criterio con un'eccezione e' piu' debole di uno senza.** Tu l'hai detto per l'ordine delle estrazioni, e vale qui.
### **② `9-ter`**: una cura non aumenta il numero delle grandezze. Gli eventi di nascita ### **sono GIA' contati, e PER RAMO**, da `_g_nati_mitosi_ev` e `_g_nati_schwinger_ev` — che e' il conto ### **che serve**, perche' i due rami fanno cose diverse alla carica.

## ✅ **E HO CURATO UN BUCO CHE AVREBBE INDEBOLITO IL SIGILLO IN SILENZIO**

Le regole sono ### **funzioni di modulo** e scrivono ### **`net.<nome>`, non `self.<nome>`.** Lo scanner del perimetro in `csv/_confronto_nascita.py` cercava ### **solo `self`** ⇒ ### **non le avrebbe viste**, e l'insieme da confrontare si sarebbe ### **RISTRETTO.**

### ⛔ **E' il difetto peggiore che un sigillo possa avere: non sbagliare un verdetto, ma SMETTERE DI GUARDARE.** Avrebbe detto *<<0 differenze>>* ### **perche' non le cercava piu'.**

### ✅ **Due cure, e la seconda e' quella che conta:**
**①** il perimetro ### **si ALLARGA** *(il prefisso `_rn_`, il ricevitore `net`)*, e ### **i due `_eredita_*` RESTANO nella lista** anche se il simulatore di oggi non li ha: il braccio `D` gira sul blob ### **PRIMA**, dove ci sono.
### **② IL BRACCIO `A` ORA CONFRONTA L'INSIEME COL REFERTO COMMITTATO**, e ### **una grandezza PERSA fa FALLIRE il braccio.** E se il referto precedente non c'e', lo ### **DICE** invece di dedurre *<<nessuna perdita>>* — che sarebbe un ### **NON MISURATO** travestito (`FALSO-ZERO`).

## 📌 **IL CRITERIO, ed e' il braccio `E` del sigillo, NON la mia parola**

| | |
|---|---|
| il **«prima»** | dal ### **PADRE del commit 3**, estratto in BINARIO *(`H-P8`, `sim_prima_del_flag`)* |
| ### **il criterio** | ### **ZERO differenze, SENZA ECCEZIONI** — grandezze **e** contatori |
| **e il controllo** | ### **se non ci sono state NASCITE il braccio FALLISCE**: *«zero differenze su zero nascite»* non e' un sigillo, e' un ### **NON MISURATO** |

### ⚠ **IL SIGILLO NON HA ANCORA GIRATO, e questo commit NON dice che passa.** Il codice si committa ### **PRIMA** del run *(par.5)*, e solo allora il *«prima»* esiste nella storia da cui `sim_prima_del_flag` lo estrae. ### **Se il braccio `E` fallisce, committo il fallimento e mi fermo** — e ### **non allento il criterio.**

### 📌 **E una SONDA ha girato prima, ma NON e' una prova e lo dice da se':** `csv/_test_fork/_sonda_commit3.py` prende il *«prima»* da una ### **copia**, non da `git`. Serve a una cosa sola: ### **non committare codice che non ha mai girato.**

---
