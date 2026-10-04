# dettaglio di `CLAUDE.md` par.4 — **tutto cio' che si dice a Luca va nel repo**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col
loro numero. Non rimanda ad altri file di `doc/REGOLE/`.)*

## PERCHE', in una frase

> ### **Un riscontro non relazionato e' un riscontro perso.**
> Chi legge il repo da fuori — Claude web, una sessione nuova, Luca fra tre giorni —
> **non ha la conversazione: ha solo i file.**

## LA FORMA E' LARGA, ed e' voluto

Va nel repo ogni **misura**, ogni **lettura del codice**, ogni **sigillo** che passa o che
fallisce, ogni **premessa che cade**, ogni **proprio errore**, e inoltre ogni **RIEPILOGO**,
ogni **CORREZIONE** di cosa gia' scritta, ogni **DOMANDA**, ogni **CHECKPOINT**.
### **Se una cosa vive solo in chat, per chi legge il repo NON E' MAI STATA DETTA.**

## DOVE

Un paragrafo in **`RELAZIONE_PER_CLAUDE.md`** *(il file vivo tiene **solo il giorno
corrente**; i giorni chiusi stanno in `doc/relazioni/`)*, **piu'** un documento dedicato in
`doc/` quando il riscontro e' un pezzo di lavoro, **piu'** la riga nell'**indice** se cambia
uno stato.

## QUANDO: **SUBITO**

La frase-spia e' **«appena finisce, committo»**.
### ⛔ **Un blocco di recupero non sana la violazione: la CONFERMA.** Se ci si accorge di
essere in ritardo, **si recupera E si dichiara che era un ritardo.**

## UNA DOMANDA E' UN RISCONTRO

Quando si pone una domanda a Luca o si lascia una decisione aperta, **il ragionamento che ci
porta si committa nello stesso giro**: la domanda arriva in chat, la risposta arriva **ore o
giorni dopo**, e in chat non c'e' piu' il ragionamento.
### **Ogni domanda aperta ha un CRITERIO DI CHIUSURA** — *cosa esattamente la deciderebbe*.
### ⚠ **Una voce senza criterio non e' un fronte: e' un desiderio.**

## ANCHE A META' RUN

Un run che gira **senza un resoconto pushato** e', se la macchina si riavvia, **un run che
nessuno sa che esisteva**. `csv/_stato_run.py` scrive `doc/STATO_RUN.md` da solo
*(`R.apri` / `R.tappa` / `R.chiudi`)* e **rifiuta di aprire un run se il precedente e' ancora
APERTO**; il **commit** pero' **non e' automatico** e va dato **al primo momento utile**.

## `PUSHATO: <hash>`, e perche' e' una forma e non un automatismo

Ogni messaggio a Luca finisce con **`PUSHATO: <hash>`**, oppure **`NIENTE DA PUSHARE`** *e il
perche'*. **L'hash e' quello del commit che contiene cio' che si e' appena detto.**
### 📌 **E' un obbligo di forma VERIFICABILE DAL DESTINATARIO:** il hook guarda **i file
toccati**, non la chat — quindi sulla forma allargata di questo paragrafo **nessuna macchina
puo' impedire nulla**, e il presidio e' quella riga, che Luca vede a colpo d'occhio.

## IL MESSAGGIO DI COMMIT NON CONTA COME RELAZIONE

E' visibile **solo a chi scorre `git log` sapendo gia' cosa cercare**.

### ⚠ **E UNA FRASE CHE NON PROSEGUE:** *«proseguo con…»* alla **fine di un turno** non
prosegue — il turno si chiude e il lavoro **si ferma** fino al messaggio successivo.
### **E' successo il 2026-10-04 dopo `9bb1df8`, e sono andate perse due ore.** Se un controllo
o una decisione fermano il lavoro, si chiude con **`FERMO: <motivo>`**; altrimenti **si
continua fino alla fine.**
