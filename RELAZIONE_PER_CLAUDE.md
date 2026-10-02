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
