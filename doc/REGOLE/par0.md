# dettaglio di `CLAUDE.md` par.0 — **che cosa si legge, e dove sta il resto**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col
loro numero. Non rimanda ad altri file di `doc/REGOLE/`.)*

## I FILE CHE SI APRONO **QUANDO SERVE**, e quando

| file | quando si apre |
|---|---|
| `doc/FATTI_dal_codice.md` | **prima di toccare una funzione del simulatore** |
| `doc/INDICE_ID.tsv` | per un difetto, un fronte, una misura: **e' la fonte** |
| `doc/STATO_RUN.md` | dove siamo, che cosa gira, la coda unica |
| `doc/STORIA_REGOLE.md` | **da quale errore** una regola e' nata. **Non si legge all'avvio** |
| `doc/REGISTRO_FISICA.md` | *«questa e' la legge»*: forma, derivazione, dimensioni, limiti |
| `doc/COMPONENTI_PROMOSSE.md` | che cosa e' **fisica di default**, che cosa **esperimento**, che cosa **cura** |
| `doc/INVENTARIO_strumenti.md` | **quale script produce quale numero**, col blob di ciascuno |
| `doc/STELLA_POLARE.md` | le **cinque domande** obbligatorie nel task history di un commit di fisica |
| `RELAZIONE_PER_CLAUDE.md` | il giorno corrente; i giorni chiusi in `doc/relazioni/<AAAA-MM-GG>.md` |
| `doc/BUSSOLA_*.md`, `doc/ROADMAP_fork_SU2.md`, `doc/PROTOCOLLO_test_olonomia.md`, `doc/SYSTASIS_nota_concettuale.md` | **prima di lavorare sul fork SU(2)** |
| `doc/IPOTESI_gravita_a_spinta.md` | il bersaglio e le sue quattro condizioni di avvio |

## PERCHE' `FATTI_dal_codice.md` HA UNA REGOLA SUA

Quel documento e' **ordinato per funzione**, col nome della funzione come intestazione e la
**riga di oggi misurata dall'AST**. Contiene cio' che e' **gia' stato verificato o misurato**
su quella funzione — comprese **le trappole e i commenti scaduti**.
### ⛔ **Non leggerlo significa rifare un errore che e' gia' scritto.**

### **E IL CASO CHE LO DIMOSTRA:** il commit `6b` ha scoperto che quel file **non aveva una
voce** per `decidi_divisione` ne' per `MITOSI_2LAM`. ### **Non c'era niente da leggere, e due
numeri sbagliati sono passati** — il *«primo candidato al passo 74»*, misurato su una scena
che non era quella del driver, **mentre il `6a` aveva misurato 42 sulla scena giusta.**

## IL RETAGGIO COPILOT

**Se esiste `.github/copilot-instructions.md`**: `CLAUDE.md` **lo SOSTITUISCE**. Si legge solo
come contesto storico; in caso di conflitto **vince `CLAUDE.md`**.

## PERCHE' SI RILEGGE DOPO UNA COMPATTAZIONE

Il **riassunto di sessione non contiene queste regole** — e' un limite noto di Claude Code.
### ⚠ **Quindi dopo una compattazione o una continuazione, le regole vanno rilette dal file
PRIMA di agire:** la memoria della sessione le ha perse, il file no.

## LA STRUTTURA A DUE LIVELLI, e perche' NON puo' crescere in catene

*(decisione di Luca, 2026-10-04.)*

| | |
|---|---|
| **`CLAUDE.md`** | le **REGOLE**, ciascuna in **2-3 righe** |
| **`doc/REGOLE/par<N>.md`** | il **dettaglio** di quel paragrafo: perche' la regola e' nata, l'incidente che l'ha motivata, gli esempi |

### **TRE VINCOLI, e il terzo e' quello che impedisce il disordine di tornare**

### **① UN SOLO SALTO.** Da `CLAUDE.md` al dettaglio, e basta.
### **② NIENTE CATENE NE' CICLI.** Un file di `doc/REGOLE/` **non rimanda MAI** a un altro file
di `doc/REGOLE/`, e a `CLAUDE.md` **solo con l'intestazione**. Puo' citare **reperti, task
history e referti**, che non contengono regole.
### **③ UNA SOLA CASA PER OGNI REGOLA.** I file di dettaglio **non contengono regole nuove**.

> ### 📌 **PERCHE' LA ② E' LA PORTANTE, e non una precauzione formale.** Un sistema a
> **profondita' 1** si legge **in due letture**: la regola, e il suo perche'. Un sistema con
> **catene** obbliga a seguire un cammino di **lunghezza ignota** per sapere se una regola ha
> un'eccezione — ### **e un ciclo lo rende impossibile da leggere per intero.**
> ### **Il tetto di 400 righe protegge la LUNGHEZZA; la ② protegge la LEGGIBILITA', che il
> tetto da solo non da'.**

## DOV'E' IL TESTO DI PRIMA DEL RIORDINO

> ### 📌 **IL `CLAUDE.md` DI PRIMA DEL RIORDINO DEL 2026-10-04 STA IN
> ### `da79cc1:CLAUDE.md`** *(391 righe)*. Si legge con
> `git show da79cc1:CLAUDE.md`, e ### **si va a prenderlo quando una frase di oggi sembra
> aver perso una sfumatura:** meta' del testo uscito e' **riassunto**, non trasferito.

**E «riassunto» ha due numeri, non uno, perche' i due modi di contare dicono cose
diverse** *(misurati il 2026-10-04 sulle 282 righe di contenuto di `da79cc1`)*:

| come si conta | ritrovato oggi *(in `CLAUDE.md` + `doc/REGOLE/`)* | che cosa significa |
|---|---|---|
| **per RIGA, verbatim** | **86 su 282, il 30%** | il numero **sovrastima la perdita**: riavvolgere un paragrafo cambia **ogni** riga anche a contenuto identico |
| **per PAROLA, con molteplicita'** | **2914 su 2951, il 99%** | il contenuto **c'e'**: e' **riformulato**, non perso |

### ⚠ **E LE `37` OCCORRENZE DAVVERO USCITE SONO UN ELENCO DI ESEMPIO, non una
### regola.** La riga 99 di `da79cc1` diceva *«le leggi fisiche da non violare (SU(2)
nell'algebra di Lie, **Verlet solo sul second'ordine**, niente medie globali …)»*; oggi
il par.3 **rimanda a `doc/REGISTRO_FISICA.md`**, dove *Verlet* compare **15** volte e
*second'ordine* **4**. ### **L'esempio e' uscito dal flusso di lavoro ed e' rimasto dove
la legge e' autorevole — che era lo scopo del riordino, non un effetto collaterale.**

### ✅ **E IL PRESIDIO C'E':** `python csv/_struttura_regole.py` verifica che **l'insieme delle
regole si conservi** e che **il grafo sia un albero di profondita' 1**. Si rigira a ogni
modifica di `CLAUDE.md`.
