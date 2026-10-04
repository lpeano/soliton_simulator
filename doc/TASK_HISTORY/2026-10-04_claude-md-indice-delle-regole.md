# `CLAUDE.md` DIVENTA L'INDICE DELLE REGOLE — **decisione di Luca, 2026-10-04**

*(registrata **PRIMA del lavoro**, par.8.)*

## 1. LA STRUTTURA, come Luca l'ha fissata

| | la regola della struttura |
|---|---|
| **①** | **DUE LIVELLI, non di piu'.** `CLAUDE.md` contiene le **REGOLE**, ciascuna in **2-3 righe** al massimo. Il dettaglio *(perche' e' nata, l'incidente che l'ha motivata, gli esempi)* va in **un file per paragrafo**: `doc/REGOLE/par<N>.md`. ### **Da `CLAUDE.md` al dettaglio c'e' UN SOLO salto** |
| **②** | **NIENTE CATENE NE' CICLI.** Un file di `doc/REGOLE/` **non rimanda MAI** a un altro file di `doc/REGOLE/`, e non rimanda a `CLAUDE.md` se non con **una riga di intestazione**. Puo' citare **reperti, task history e referti**, che non contengono regole |
| **③** | **UNA SOLA CASA PER OGNI REGOLA.** Una regola sta in `CLAUDE.md`, **una volta**. I file di dettaglio **non contengono regole nuove**: solo spiegazioni di regole che stanno gia' in `CLAUDE.md`, citate col loro id o numero |
| **④** | **COME SI CRESCE DOPO**, cosi' il riordino **non si ripete**: una regola nuova entra in `CLAUDE.md` con **al massimo 3 righe**, e la spiegazione va nel file del suo paragrafo. ### **Va scritto in `CLAUDE.md` par.0**, accanto a *«dove sta tutto il resto»* |
| **⑤** | il tetto resta **400** righe *(`H-RIGHE`)*, e l'obiettivo del riordino e' **circa 250** — ### **cosi' resta margine** |

### 📌 **PERCHE' LA ② E' LA REGOLA PORTANTE, e non una precauzione formale.** Un sistema di
documenti a **profondita' 1** si puo' leggere **in due letture**: la regola, e il suo perche'.
Un sistema con **catene** obbliga a seguire un cammino di lunghezza ignota per sapere se una
regola ha un'eccezione — ### **e un ciclo lo rende impossibile da leggere per intero.**
### **Il tetto di 400 righe protegge la LUNGHEZZA; la ② protegge la LEGGIBILITA', che e' la
cosa che il tetto da solo non da'.**

## 2. I DUE CONTROLLI CHE POSSONO FALLIRE

| | che cosa prova | la prova che DEVE fallire |
|---|---|---|
| **`(a)`** CONSERVAZIONE | l'insieme delle regole in `CLAUDE.md` **prima** e **dopo** **coincide** | una copia in cui **una regola e' stata TOLTA** deve essere **scoperta, col nome della regola** |
| **`(b)`** NESSUN LOOP | il grafo dei rimandi fra `CLAUDE.md` e `doc/REGOLE/` e' **un albero di profondita' 1** | una copia con **un rimando fra due file di `doc/REGOLE/`** deve essere **scoperta** |

### ⚠ **E IL CONTROLLO `(a)` HA BISOGNO DI UNA DEFINIZIONE, altrimenti non e' un controllo.**
*«L'insieme delle regole»* non e' un concetto che una macchina legge da sola. ### **Lo fisso
qui, prima di scrivere lo strumento**, cosi' non lo adatto ai risultati:

| cosa si estrae | come |
|---|---|
| **i TITOLI** | ogni riga che comincia con `#` |
| **gli ID** | i token **fra backtick** che combaciano con `[A-Z][A-Z0-9-]*`, lunghi `>= 2` — ### **e' la forma con cui `CLAUDE.md` scrive gli id**: `` `L-UN-PROMPT` ``, `` `H-FILE` ``, `` `P1-quater` ``, `` `A14` `` |
| **i PUNTI numerati** | ogni riga che comincia con `<cifre>.` |

### ⛔ **PERCHE' <<FRA BACKTICK>> E NON <<MAIUSCOLO NEL TESTO>>:** una ricerca sul maiuscolo
nudo prenderebbe ### **ogni parola enfatizzata** — e questo file ne e' pieno — producendo un
insieme che cambia a ogni riscrittura di una frase. ### **Un controllo che si accende quando
cambio una parola in grassetto non e' un controllo: e' rumore**, e dopo tre falsi allarmi
nessuno lo guarda piu' *(`A9`)*.

### ✅ **E LO STRUMENTO RESTA NEL REPO** e si rigira a ogni modifica di `CLAUDE.md`:
### **e' il presidio contro il loop NEL TEMPO**, non solo durante il riordino. *(Se diventare
un hook e' una decisione di Luca: lo strumento lo propone, non lo decide.)*

## 3. UN PUNTO D'ORDINE, e va deciso da Luca prima del riordino

### ⛔ **IL MANDATO DICE *«in coda DOPO il commit 7 dei file non tracciati»*, E QUEI COMMIT
NON ESISTONO.** Il lavoro sui non tracciati e' **fermo al `COMMIT 1`**, che si e' bloccato
sul proprio controllo *(`67` file tracciati coperti dalle regole nuove)* in attesa della
scelta fra **(A)** e **(B)**.

### ⚠ **E QUESTA VOLTA L'ORDINE NON E' FORMALE:** il `COMMIT 6` di quel lavoro deve
**modificare `CLAUDE.md` par.12** *(il conteggio dei hook, per `H-NON-TRACCIATI`)* —
### **lo stesso file che il riordino ristruttura.**

> ### 📌 **Ristrutturare `CLAUDE.md` mentre una sequenza di sette commit e' sospesa a meta'
> significa far cambiare il file SOTTO un lavoro che riprendera' scritto contro la versione
> vecchia.** ### **E' la classe di errore che ho gia' fatto due volte in questi giorni:** il
> sigillo girato su una scena che non era quella del driver, e il braccio che citava un json
> di un altro blob. ### **In entrambi i casi l'oggetto era cambiato sotto il lavoro, e il
> lavoro non si era accorto.**

### ✅ **AGGIORNAMENTO, poche ore dopo: LUCA HA DECISO LA STRADA (B) e il lavoro sui non
tracciati RIPRENDE** dal `COMMIT 2`, col `COMMIT 1` ridotto. ### **Quindi l'ordine che il
mandato fissa diventa SODDISFACIBILE**, e il riordino di `CLAUDE.md` resta in coda dove
Luca l'ha messo — **dopo il `COMMIT 7`** — invece di essere bloccato dietro una decisione
che non arrivava. ### **Il punto d'ordine qui sopra resta scritto perche' era vero quando
l'ho posto, e perche' la risposta e' arrivata: non si cancella una domanda che ha avuto
risposta.**

### ✅ **QUINDI: task history e strumento SI**, perche' il mandato li mette **prima** e perche'
### **non toccano `CLAUDE.md`**; ### ⛔ **il RIORDINO no**, finche' l'ordine che Luca ha
fissato non e' soddisfatto. ### **Non scelgo io di saltarlo** *(`L-DOPO-STOP`)*.

### **E CIO' CHE SI PUO' FARE SENZA DECIDERE NIENTE:** lo strumento, girato sulla versione di
oggi, stabilisce **la fotografia del PRIMA** — che il controllo `(a)` richiede comunque,
qualunque sia l'ordine. ### **Senza quella fotografia il riordino non sarebbe verificabile a
posteriori.**

## 4. TODO DEL NEXT STEP

1. ☐ **committare e pushare QUESTO FILE** *(par.8)*
2. ☐ lo **strumento** + voce d'inventario, committato, poi girato sulla versione di **oggi**:
   e' la **fotografia del PRIMA** e il collaudo dei due controlli
3. ☐ **STOP** — e il riordino aspetta che l'ordine fissato da Luca sia soddisfatto
4. ☐ *(dopo)* il riordino, un commit per paragrafo o per gruppi, **con lo strumento rigirato
   a ogni commit**
5. ☐ *(dopo)* il **referto finale** con le righe prima/dopo e i due controlli

### ⚠ **E NESSUN CONTENUTO SI PERDE:** cio' che esce da `CLAUDE.md` va in `doc/REGOLE/`,
**verbatim** oppure riassunto **con il testo originale citato**.
