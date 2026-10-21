# LA REGRESSIONE DEL COLLAUDO `D0`: IL PUNTO FISSO DI `Omega` NON CONVERGE, DA `7395cd9a`

> **Il mandato:** decisione di Luca del `2026-10-21` alle `19:24`, dopo `3008bd13`.
> ### **Nucleo, CRITERIO NUMERICO: nessuna legge nuova, nessun numero di fisica.** `leggi.yaml`
> intatto. ### **Il secondo gradino dei triangoli ASPETTA questo mandato.**
> ### ⚠ **Il testo del mandato arriva TRONCATO al punto `3`** *(«misura quanto dura
> `primo_ordine/collauda.py`. Se»)*: ### **del punto `3` faccio solo la misura della durata, e
> chiedo a Luca il resto.**

**LIVELLO:** nucleo, criterio numerico.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica**: il criterio d'arresto di un punto fisso ### **non cambia una
   legge**; ### **se la cura cambiasse un valore fisico oltre gli ulp, non si applica** *(sez. `2`)*.
2. **Il gradino:** `(a)` ### **la cura tolta deve far tornare rosso `D0`**; `(b)` ### **la scena di
   `C5` deve convergere coi giri di prima**; `(c)` ### **non si applica.**
3. **Aggiunge un numero o una legge?** ### **Una cura, se c'e', e' un CRITERIO D'ARRESTO, non una
   costante di fisica**; ### **se introduce un numero, si dichiara quale e da dove viene.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No:** cambia ### **quando il punto fisso si ferma**, non
   la legge.
5. **Emergente o imposto?** ### **Non si applica.**

## 1. ⛔ L'ERRORE `n.30` DEL GUARDIANO

### **Il guardiano ha verificato `7395cd9a` e `418546c8` senza far girare la suite completa**; ###
**`C.7` mio e' lo stesso difetto dalla mia parte.**

## 2. RAGIONAMENTO PRELIMINARE

- ### **L'IPOTESI DEL GUARDIANO** *(da verificare, non assunta)*: il tetto di `Omega` e' proporzionale
  a `|cs'|`; ### **nella forma di `D0` `cs'` e' (quasi) zero**, quindi il tetto e' (quasi) zero, ###
  **la tolleranza «8 ulp del tetto» e' (quasi) zero**, e il punto fisso ### **non puo' fermarsi se lo
  scarto non e' esattamente `0`.**
- ### **LETTO DAL CODICE PRIMA DEI NUMERI, e la scrivo perche' pesa sull'ipotesi:**
  - il braccio che cade e' ### **`braccio_accesa`** di `primo_ordine/_collauda_cs.py`: `corri(nn, seme, LC_DI_PROVA)`, ### **con `FP.accendi_cs(mot, 8.0, st)` prima di OGNI tick** e poi `TK.tick` *(il passo di oggi)*; ### **`DTAU = 1.0`, `250` tick, `VUOTO_MODULO = 2`**, le scene `(16, 7)` e `(12, 11)`;
  - ### **arriva in `energia_pesata.applica` perche' `accendi_cs` mette `mot.cs` e `mot.lambda_c`**; ### **il ramo «forma spenta»** *(`mot.cs is None`)* ### **e' il braccio `None`, che esce subito e passa.**
  - ### **Quindi in `D0` la forma NON e' spenta, e `cs' = Lambda_c / (Lambda + Lambda_c)^2` NON e' zero per costruzione** *(con `Lambda_c = 8` e `Lambda` dello stesso ordine e' `~1/32`)*. ### **Credo che l'ipotesi CADA**, e che la causa sia ### **un pavimento di arrotondamento dello scarto** *(a `dtau 1` il pezzo e' grande)* ### **sopra `8` ulp del tetto.** ### **Da vedere coi numeri.**
- **Cosa NON so:** che criterio usava `3b467aa4` *(dove `D0` passa)*, e ### **se lo scarto cala coi giri e poi si ferma, o oscilla.**

## 3. LA DIAGNOSI E LA LETTURA, FISSATE QUI *(copiate dal mandato)*

- ### **Nel collaudo `D0`, a ogni giro del punto fisso:** `max|cs'|`, `max tetto_k`, ### **la scala del criterio** *(`EPS_OMEGA * max tetto`)*, ### **lo scarto.** ### **Lo strumento di diagnosi** *(`csv/_diagnosi_d0.py`)* ### **ripete il ciclo di `applica` stampando**, e ### **deve riprodurre l'eccezione** *(lo stesso scarto finale, `1.252e-12`)*: ### **e' il controllo che ripete la cosa giusta.**
- ### **LA LETTURA:** ### **l'ipotesi TIENE se la scala del criterio e' `<= 64` ulp di uno scarto non nullo che non cala coi giri**; ### **altrimenti CADE**, e si scrive la causa vera.

## 4. LA CURA *(solo se e' un criterio numerico e non cambia nient'altro)*, LA CONDIZIONE COPIATA

- **se l'ipotesi tiene:** il criterio d'arresto con una scala che ### **non degenera quando il termine e' nullo per costruzione**, la forma piu' semplice, dichiarata col suo tipo.
- ### **CONDIZIONE PER APPLICARLA SENZA CHIEDERE:** con la cura, ### **l'impronta `2e7f795d2a52fbe7`, TUTTI i collaudi della suite** *(`D0` compreso, che torna verde)* ### **e i referti di `L2` rifatti a campione** *(almeno `C1` di strada `(d)`, `594417f6` `R2` a lato `32`, `triangoli_gradino1`)* ### **restano AL BIT, o cambiano SOLO nel numero di giri del punto fisso.** ### **Se anche un solo valore fisico cambia oltre gli ulp: STOP**, niente cura applicata, la domanda a Luca coi numeri.
- ### **DEVE FALLIRE:** la cura tolta, `D0` torna rosso. ### **DEVE RIUSCIRE:** una scena con `cs` acceso e `cs'` grande *(quella di `C5`)* converge con gli stessi giri di prima.
- ### ⚠ **Se l'ipotesi CADE**, la cura va derivata dalla causa vera: ### **la condizione per applicarla senza chiedere resta la stessa.**

## 4-bis. ANNOTAZIONE DEL `2026-10-21`, `20:06`, PRIMA DEL CODICE: LA CURA `(a)`, `GIRI_MAX_OMEGA` DA 120 A 200 *(decisione di Luca dopo `5ed71b6d`; si annota)*

- ### ⛔ **L'ERRORE `n.31` DEL GUARDIANO:** l'ipotesi «`cs'` zero, tolleranza zero» ### **veniva dalla frase «la forma `cs` spenta» di `3008bd13`, non dalla lettura del collaudo**: ### **il braccio che cade ha `cs` ACCESO** *(`Lambda_c 8`, `DTAU 1`)*. ### **E l'imprecisione di quella frase e' MIA:** in `3008bd13` ho scritto il TITOLO del collaudo *(«la forma `cs` spenta e' il passo di oggi»)* come se dicesse in quale forma il punto fisso cadeva.
- ### **LA DECISIONE DI LUCA:** ### **`GIRI_MAX_OMEGA` da `120` a `200`.** ### **Stella Polare, domanda `3`:** ### **e' un limite di sicurezza del punto fisso, non una costante di fisica**; ### **dove il punto fisso converge entro `120` giri, il risultato non cambia di un bit** *(il ciclo si ferma allo stesso giro, con gli stessi conti)*.
- ### **E L'AVVISO:** a ogni chiamata ### **il fattore di contrazione stimato** *(il rapporto fra gli ultimi due scarti)*; ### **se supera `0.9`, un AVVISO contato** *(non un errore)*, col fattore e il `dtau`, ### **un contatore nel motore** *(come `giri_omega`)*. ### **`0.9` e' una soglia di AVVISO, non di fisica.** ### ⚠ **Il contatore NON deve toccare i conti:** si legge, non si usa.
- ### **I CONTROLLI, copiati prima dei numeri:**
  - ### **DEVE RIUSCIRE:** `D0` *(`braccio_accesa`)* ### **torna verde**; i giri usati stampati *(`~137` attesi)*;
  - ### **AL BIT:** l'impronta `2e7f795d2a52fbe7`; ### **la SUITE COMPLETA tutta verde**; ### **a campione `C1` di strada `(d)`, `594417f6` `R2` a lato `32`, `triangoli_gradino1`**, identici al bit *(dove il punto fisso convergeva gia')*. ### **Se anche un solo valore fisico cambia: STOP**, e la domanda a Luca;
  - ### **DEVE FALLIRE:** con `120` giri `D0` torna rosso;
  - ### **LA MISURA DEL FATTORE** *(informazione per la domanda di `L1` sull'automa)*: ### **il fattore di contrazione sulla scena di `D0` a `dtau` `0.5`, `1`, `1.25` (e `1.5` se converge)**: il medio e il massimo, ### **e se a qualche `dtau` non converge entro `200` giri** *(dirlo: non e' un errore della misura)*.
- ### **LA REGOLA DELLA SUITE** *(in `CLAUDE.md`, regola scritta, `A9`)* e ### **il file generato** `doc/REFERTO_infrastruttura_era2.md` *(stato nel working tree, e perche' era scaduto)*.

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. La diagnosi *(`csv/_diagnosi_d0.py`)*: commit, corsa, referto.
3. La cura, se c'e' e se la condizione regge; la suite; i referti a campione.
4. La durata di `collauda.py`; ### **la domanda a Luca sul punto `3` troncato.**
