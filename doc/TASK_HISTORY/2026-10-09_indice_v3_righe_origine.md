# INDICE `v3`: **stato e classe DALLA RIGA D'ORIGINE**

> **Mandato di Luca del 2026-10-09**, otto punti, **un commit per punto**. Nessuna corsa,
> simulatore `b8c21049` intatto.
>
> ### ⚠ **Si committa e si pusha PRIMA del lavoro** *(par.8)*.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐ **LA FRASE CHE GOVERNA TUTTO IL GIRO: «LA VALIDITA' NON E' LO STATO»**

*«`VALE SEMPRE`»*, *«`VALE PER QUELLA SCENA`»*, *«`LIMITE DICHIARATO`»* ### **non dicono se
una cosa e' fatta**: dicono ### **fin dove vale cio' che si e' trovato.** Vanno in
`meta.validita`, e ### **non decidono lo stato.** ### ⛔ **L'indice le ha trattate come stato
per tutta la migrazione**, e lo stato vero sta ### **nella riga d'origine.**

### ⛔ **I QUATTRO ERRORI CHE IL GUARDIANO DICHIARA, e due sono miei da ripetizione**

| | l'errore | di chi |
|---|---|---|
| `(a)` | `CURA1-CORTO`, `CURA2-CORTO`, `SIGILLO-CURA2`, `SIGILLO-CURA2-RIPARATO` ### **NON sono sospese: sono corse FINITE** *(«chiuso 2026-09-24 … FINITO»)* | del guardiano, ### **e io le ho toccate DUE VOLTE** *(ripristinate `APERTA`, poi portate a `SOSPESA`)* senza mai ### **aprire la sezione sotto l'intestazione** |
| `(b)` | `G1` e' ### **«FATTO»** | del guardiano, e io ### **l'ho spostata di era** leggendo solo il titolo |
| `(c)` | `F8` era ### **troppo stretto** | del guardiano |
| `(d)` | la riverifica precedente ### **non aveva aperto le righe troncate** | ### **del guardiano e mia insieme**: i titoli sono `<= 100` caratteri, e ### **un troncamento taglia esattamente dove la riga dice lo stato** |

### ⭐ **E l'errore `(d)` e' quello che spiega gli altri tre.** Esempio misurato: il titolo di
`Z83` finisce *«… ⏳[EPOCA 1 · MISURA] | DO…»*; la riga intera dice ### **«DOMANDA APERTA: `d0`
DEVE STARE SOPRA `LAM`?»** — e la voce e' ### **`CHIUSA`.** ### **Il titolo tagliava due
caratteri prima della parola che decide.**

### **CHE COSA HO MISURATO PRIMA DI SCRIVERE QUESTO FILE**

| | |
|---|--:|
| voci con una ### **riga d'origine ritrovabile** | ### **`452`** |
| voci ### **senza** | `394` |
| di cui ### **segnaposto** `NON_DEFINITA` | `142` |

### **E i SETTE casi di collaudo del mandato si ritrovano TUTTI**, dopo tre correzioni
all'attrezzo che dichiaro perche' sono il mestiere di questo giro:
① il prefisso di `fonte` e' ### **senza i `**` e i backtick** della riga vera *(senza
spogliarli, `1` caso su `7` si ritrovava)*; ② alcune ### **emoji di stato** sono nel titolo e
altre no *(`Z25` tiene il suo `🟨`, `Z47` ha perso il `🟩`)*; ③ un prefisso puo' essere
### **contenuto in un nome piu' lungo** — `APERTO SIGILLO-CURA2` sta anche in
`APERTO SIGILLO-CURA2-RIPARATO` — e allora ### **vince la riga piu' corta**, perche' la'
il prefisso e' ### **tutto il contenuto.**

### ⛔ **CHE COSA NON SO, E NON INVENTO**

1. **Quante voci il punto `1` cambiera'.** Previsione larga: ### **fra `40` e `160`
   cambiano stato**, e ### **fra `10` e `80` restano ambigue** *(la riga dice parole di
   entrambi i gruppi, o nessuna)*.
2. **Se `AGENDA` sia la scelta giusta per l'era `2`.** Il mandato dice *«`SOSPESA` (era `1`)
   o `AGENDA` (era `2`)»*, e lo applico; ### **ma `era 2` sono `24` voci**, e credo che
   quasi nessuna abbia una riga d'origine con quelle parole.
3. **Quante delle `394` senza riga siano un problema.** `142` sono segnaposto, e per loro
   ### **non esiste una riga d'origine**: sono ID che il codice nomina. Le altre `252`
   ### **le conto e le dichiaro**, non le indovino.
4. **Se le `35` voci dei punti `3` e `4` abbiano una riga d'origine.** Se non l'hanno,
   ### **l'era e il dominio li da' il mandato** *(sono «esplicite»)* e lo stato
   ### **resta quello che e'**: lo scrivo invece di inventarlo.

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### **LE DUE REGOLE, FISSATE QUI PRIMA DI APPLICARLE**

> ### ⓵ **LO STATO DALLA RIGA** *(punto `1`)*
> ### **CHIUSA** se la riga dice `CHIUSA`, `CHIUSO`, `CURATO/A E SIGILLATO`,
> `CURA IN CODICE`, `FATTO/A`, `FINITO`, `RITIRATA`, `✅` ### **e NON dice nessuna parola
> dell'altro gruppo**;
> ### **SOSPESA** *(era `1`)* o ### **AGENDA** *(era `2`)* se dice `APERTA/O`,
> `DOMANDA APERTA`, `NON INIZIATO`, `NON CURATO`, `DA RIVERIFICARE`, «Si chiude quando»,
> «Chiude chi», «resta aperta»;
> ### ⚠ **e `APERTO` NON conta se e' l'intestazione di un registro di corse seguita da
> «chiuso … FINITO»** — e' ### **l'errore `(a)`**, e si riconosce ### **solo aprendo la
> sezione sotto.**
> ### ⛔ **Entrambi i gruppi, o nessuno: NON si tocca**, e si elenca con la frase.

> ### ⓶ **LA CLASSE DALLA RIGA** *(punto `2`)*
> `CURATO`/`SIGILLATO`/`CURA IN CODICE` → ### **`CURA`**; `CHIUSA PER MISURA` o un
> ### **esito misurato** → ### **`MISURA`**; «e' un DIFETTO»/«DIFETTO ACCLARATO» →
> ### **`DIFETTO`**; ### **`FRONTE` SOLO se la voce e' aperta e il testo e' una domanda o un
> programma.** ### **Ambigui: si elencano, non si toccano.**

### **I PASSI** — un commit per punto, nell'ordine del mandato.

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura |
|---|---|
| ### **il collaudo del punto `1`** | `Z83` → `SOSPESA` · `Z47` → ### **non si tocca** *(il punto `5` lo riserva a Luca)* · `Z25` → `CHIUSA` · `Z42` → `CHIUSA` · `CURA1-CORTO` → `CHIUSA` · `G1` → `CHIUSA` · `A2-ANELLO` → `SOSPESA`. ### ⛔ **Se UN SOLO caso esce diverso, la regola e' sbagliata: FERMO** |
| il punto `1` | `40`–`160` cambiate, `10`–`80` ambigue |
| il collaudo di `F8` allargato | ### **DEVE** scattare su `CONFIG-1` e `PAT-1` a `ba400c0`, ### **NON deve** su `P6` ne' su `FALSO-ZERO` |
| i punti `5`, `6`, `7` | ### **NON cambiano ne' stato ne' classe ne' era ne' dominio:** aggiungono ### **note e metadati.** Se un conteggio di `classe`/`dominio`/`era`/`stato` cambia in quei tre commit, ### **ho sbagliato** |
| alla fine | `953` ID conservati, `valida` passa ### **`F7` compreso** |

### ⛔ **CHE COSA MI FA FERMARE**

1. **Un caso noto del collaudo esce diverso** ⇒ la regola e' sbagliata, e il mandato lo dice
   esplicitamente.
2. **Il punto `1` vorrebbe cambiare una voce che il punto `5` riserva a Luca** ⇒
   ### **la salta**, e la elenca: `Z47`, `A3-DISEGNO`, `G4-MEMARCO`, `Z104`, `O4`, `K2a`,
   `K2b`, `SPINORE-SENZA-FASE`, `MASSA-CRITICA-LOCALE`.
3. **Un cambio di stato violerebbe `F7`** *(era `1` → stato diverso da
   `SOSPESA`/`CHIUSA`/`SUPERATA`)* ⇒ ### **il lotto non parte**, e va bene: e' il presidio
   che funziona.
4. **Le ambigue sono piu' di `80`** ⇒ i due gruppi di parole ### **si sovrappongono troppo**,
   e la regola va ridetta, non applicata.
5. **Una transizione e' vietata** *(es. `CHIUSA` → `SOSPESA`, che `TRANSIZIONI` non ammette)*
   ⇒ ### **lo dichiaro e NON forzo**: `CHIUSA` esce solo verso `APERTA` o `SUPERATA`, e
   ### **questo e' un ostacolo vero fra la regola e lo schema.**

### ⚠ **E IL QUINTO E' QUELLO CHE MI ASPETTO DI INCONTRARE:** `Z83` e' ### **`CHIUSA`** e la
riga dice ### **«DOMANDA APERTA»** ⇒ servirebbe `CHIUSA` → `SOSPESA`, e
### **`TRANSIZIONI` NON LA AMMETTE** *(da `CHIUSA` si esce solo verso `APERTA` o `SUPERATA`)*.
### ➜ **Credo che la via sia `CHIUSA` → `APERTA` → `SOSPESA` nello STESSO lotto**, e se non si
puo' ### **lo dico invece di allargare `TRANSIZIONI`.**

### **`L-STELLA`: le cinque domande di `doc/STELLA_POLARE.md`**

### ⛔ **NON SI APPLICA, e il perche' e' parte della risposta:** nessuna legge cambia, il
simulatore non si tocca *(`b8c21049`)*, niente gira. Si leggono ### **righe di documenti** e
si correggono ### **stato, classe, era e dominio** di voci dell'indice dei difetti.
### **Le cinque domande chiedono di un gradino di robustezza fisica, di numeri o leggi
aggiunti, del verso EM-curvatura e di emergente-contro-imposto: su un cambiamento che non
entra nel simulatore NON HANNO UN SOGGETTO.**

---

## ③ TODO DEL NEXT STEP — *operativo*

- [ ] **`1`** `meta.validita`; lo stato dalla riga d'origine. ### **Il collaudo sui `7` casi
      PRIMA di applicare**, su una COPIA.
- [ ] **`2`** la classe dalla riga, stessa tecnica. ### **Ambigui: elencati.**
- [ ] **`3`** era `1` per l'elenco dichiarato di `doc/CURE_fisica_ordine.md` + le `38` nominate;
      ### **`F8` allargato** *(funzioni e variabili del simulatore, `csv/_test_fork`,
      `csv/_seal_fork`)* + collaudo su `CONFIG-1`, `PAT-1`, `P6`, `FALSO-ZERO`.
- [ ] **`4`** il dominio delle esplicite, ### **ogni motivo con la frase.**
- [ ] **`5`** le `9` a Luca: ### **SENZA toccarle**, in `DA_DECIDERE_LUCA.md`.
- [ ] **`6`** gemelle e duplicati: `meta.duplicato_di` + `collegate`, ### **NON fusi**; `F1`
      esteso allo stato ### **solo per lo schema `D`/`Z`.**
- [ ] **`7`** `meta.da_dividere` con le due parti e la frase, ### **NON dividere.**
- [ ] **`8`** controlli + `doc/REFERTO_indice_v3_righe_origine.md`, ### **voce per voce.**
- [ ] **par.6** a ogni commit; ### **le due VISTE GENERATE nel `git add`**; e
      **`storico-commit`** dopo ogni push.
