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

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. La diagnosi *(`csv/_diagnosi_d0.py`)*: commit, corsa, referto.
3. La cura, se c'e' e se la condizione regge; la suite; i referti a campione.
4. La durata di `collauda.py`; ### **la domanda a Luca sul punto `3` troncato.**
