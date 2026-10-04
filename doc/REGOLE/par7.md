# dettaglio di `CLAUDE.md` par.7 — **il codice di una misura dev'essere recuperabile**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col
loro numero. Non rimanda ad altri file di `doc/REGOLE/`.)*

## PERCHE' «PER COSTRUZIONE» E NON «PER DILIGENZA»

Un numero senza il codice che l'ha prodotto **non e' una misura**: e' un'affermazione. E la
diligenza non basta, perche' il momento in cui serve il codice e' **mesi dopo**, quando
nessuno ricorda piu' che versione girava.

### **Quindi i due stati ammessi sono entrambi VERIFICABILI DA UNA MACCHINA:**

| | |
|---|---|
| **1** | il blob sul disco **coincide con quello COMMITTATO** — *il caso normale, e quello da preferire* |
| **2** | accanto ai dati resta una **COPIA ESATTA** del file che ha girato, **committata insieme a quei dati** |

## ED E' CABLATO, non raccomandato

`csv/_test_fork/_osserva_vuoto.py` confronta il **proprio blob** con
`git rev-parse HEAD:soliton_simulator.py` e, se differiscono, scrive da solo
`<base>._sim.py` accanto all'output, col motivo in `<base>._sim.motivo.txt`.

### 📌 **SU FILE E NON SOLO A STDOUT, e il perche' e' operativo:** dentro un sigillo lo stdout
e' **catturato**, quindi un avviso stampato **non si vede**. ### **Un presidio che parla dove
nessuno ascolta non e' un presidio.**

## GLI STATI SONO TRE, NON DUE

Si confronta col **BLOB a `HEAD`**, mai con `git status`. ### ⚠ **Perche' esiste un terzo
stato: *stesso CONTENUTO, byte DIVERSI*** — la trappola **CRLF**. `git status` lo chiama
*pulito*, lo `sha1` dei byte dice *diverso*.

### **Per ripristinare i byte esatti NON si usa `git checkout`:** si usa
`git cat-file -p <commit>:<path>`, scritto **in binario**.

### **E il `.gitattributes` c'e' dal 2026-09-16** e copre anche `.githooks/*` con
`text eol=lf`: su Linux un hook coi `^M` muore con `bad interpreter`, e ### **un presidio che
non parte e' peggio di uno assente** — perche' chi lo crede attivo smette di controllare a
mano.

## IL PRESIDIO DELL'ENCODING, e le OTTO volte

Lo stdout di Windows e' **`cp1252`** e **uccide gli script**. Ogni script di sigillo o di
misura comincia con **`_presidio.avvia(__file__)`** *(`csv/_presidio.py`)*, che riconfigura
`stdout`/`stderr` in **UTF-8** **e** **timbra il blob** dello script.

### ⛔ **`# -*- coding: utf-8 -*-` NON BASTA:** riguarda il **sorgente**, non lo **stdout**.

### **E' successo OTTO volte.** La **settima** allo script che stava **contando le
precedenti**; l'**ottava** il 2026-10-04 a `csv/_struttura_regole.py` — lo strumento del
riordino delle regole — che e' morto al **primo giro utile** su un `UnicodeEncodeError`
mentre stampava il proprio referto.

> ### 📌 **E IL TIMBRO SERVE A UNA COSA CHE NESSUNO AVEVA PREVISTO.** Il 2026-10-04, dei `15`
> file non tracciati e non citati, **sei erano catture di stdout redirette a mano**: nessuno
> strumento le scrive, e **nessun `grep` sul codice le avrebbe attribuite.**
> ### **Li ha resi attribuibili il `[TIMBRO]` nella prima riga, che nomina lo strumento E il
> blob.** ### **Un presidio nato per l'encoding ha reso decidibile una questione di
> provenienza due settimane dopo.**
