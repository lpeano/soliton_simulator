# DUE CONTROLLI DEL PASSO SULLA MATERIA UNIFORME, PRIMA DI QUALUNQUE INTERPRETAZIONE

> **Il mandato:** decisione di Luca del `2026-10-20` alle `09:12`, sull'instabilita' della
> materia uniforme di `29b997da`. ### **Nessun codice di fisica: una misura.**
> ### **`LINEARE`, la scelta di `Lambda_c` e ogni interpretazione «alla Jeans» restano FERME
> fino all'esito.**

**LIVELLO CORRENTE:** `L2`.

**IL FATTO, come l'ha letto il guardiano** nelle serie di `doc/referti_l2/jeans_del_modello.jsonl`:
- il modo dominante e' `(15, 15)` su `31x31`, cioe' `k` circa `pi` in entrambe le direzioni: ### **la scacchiera, il modo del doppione**;
- non c'e' lunghezza minima: crescono tutti gli anelli;
- gamma cresce di `2.8` volte da `x 0.01` a `x 1`, e ### **non come la radice di `rho`**;
- con `cs` ACCESO, `G` cambia gia' fra i primi campioni *(`-968.6`, `-989.4`, `-1009.6`)* mentre lo stato e' uniforme a `1e-16`;
- con `cs` SPENTO, `G` OSCILLA di periodo `2` *(`-1937.2`, `-2321.6`, `-1937.2`)*, e ### **a `cs` spento `G` e' l'energia `H`, che dovrebbe conservarsi.**

## 0. LA STELLA POLARE

1. **`A14`:** ### **E' la domanda di `C1`.** Nessuna legge cambia; si misura ### **se il passo
   conserva `H` sulla materia uniforme**. Se non la conserva, e' ### **un difetto del passo**,
   non una violazione dichiarata.
2. **Il gradino:** `(a)` e' il livello di `C1`: un tick per volta, contro una banda gia'
   misurata, con un caso che deve riuscire *(la scena di `M-B2`)*. `(b)` e' `C2`: ### **si
   toglie `S3`** *(`CAMM-MATERIA-VUOTO`)* e si guarda se la crescita resta. `(c)` ### **non si
   applica:** nessun confronto con un limite noto.
3. **Aggiunge un numero o una legge?** ### **No.** I `20` tick di `C1` e i `2000` di `C2` sono
   ### **parametri della misura**. La banda e la soglia di Student ### **escono da misure e
   strumenti gia' committati.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No:** `cs` e' SPENTO in entrambi i controlli. ### **E
   proprio per questo** dicono se la crescita ha bisogno di `cs`, del passo o di `S3`.
5. **Emergente o imposto?** ### **E' la domanda di `C2`:** se la crescita resta senza `S3`,
   ### **non e' l'accoppiamento a produrla**, e il sospetto cade sulla camminata.

## 1. RAGIONAMENTO PRELIMINARE — cosa credo prima di guardare, e cosa NON so

- **LA CADENZA DI `29b997da`, dichiarata prima** *(letta dal sorgente, `csv/_jeans_del_modello.py`, funzione `braccio`, chiusura `foto`)*:
  - ### **`G` si campionava UNA volta per tick INTERO**, con `EP.g_dello_stato`, dopo ogni `TK.tick` *(cs spento)* o `TK.tick_con_cs`;
  - il primo campione e' al tick `0`, ### **prima del primo tick**;
  - ### **nessun campione a meta' tick.**
  - ### **Quindi il periodo `2` della serie NON e' un aliasing di un campionamento a mezzo tick:** sono tre tick interi consecutivi.
- **A `cs` spento `CAMM-FASE-VUOTO` e' l'identita'** *(`energia_pesata.applica` torna lo stato se `mot.cs` e' `None`)*, e `g_dello_stato` ### **e' `H_tot`**, a meno dell'ordine della somma. ### **Lo verifico, non lo assumo:** la seconda fonte e' `_misura_mb2.h_tot`.
- **Cosa credo:** un'oscillazione del `20%` di `H` a tick intero, sulla materia uniforme, ### **non e' compatibile con un passo di Strang che conserva `H` al secondo ordine.** Pero' `dtau 0.5` mette i pezzi a `theta = pi/2`, ### **lontano dal regime asintotico** *(`M-B2` lo dice)*.
- **Cosa NON so:**
  - se lo stato uniforme e' un punto fisso del passo **senza** `S3`;
  - se `h_tot` vede su questa scena ### **lo stesso `H` che vede `g_dello_stato`**;
  - ### **se la banda di `C1` di strada `(d)`, misurata su un'altra scena, e' quella giusta per questa:** e' il criterio di Luca, e lo applico com'e'. ### **Il caso che deve riuscire** *(la scena di `M-B2`)* **dice se la banda e' troppo stretta.**

## 2. PROGETTAZIONE — i passi, cosa decide ciascuno, e cosa mi fa FERMARE

**Lo strumento:** `csv/_controllo_passo.py`. ### **Riusa** `_jeans_del_modello.scena`, `t_soglia`, `gamma_k`, e `_instabilita_vuoto.gamma_del_tratto` e `onda`. **Seconda fonte di `H`:** `_misura_mb2.h_tot`. ### **Il mezzo tick:** una COPIA dello stato avanzata con `TK.percorri_tick(copia, mot, par, (), None, TK.meta_del_palindromo())`, cioe' ### **il centro del palindromo**, nello stesso modo in cui lo raggiunge `cs_al_centro`.

### `P0` — LE PROVE DELLO STRUMENTO *(se una cade: STOP)*

- **`P0a`, il rivelatore del periodo `2`** *(il caso che DEVE scattare e quello che NON deve)*:
  - una serie sintetica `H0 (1 + 3 B (-1)^t)` ### **deve** dare «periodo `2`»;
  - una serie costante con rumore `1e-3 B` ### **non** deve.
- **`P0b`, LA BANDA `B`:** si rifa' il braccio `k = 1` di `C1` di strada `(d)` *(`_misura_strada_d.corsa(0.5, 16, True, "centro", 1)`)*.
  - L'escursione ### **deve coincidere** con quella del referto `doc/referti_l2/c1_tetto_omega.txt` *(riga `k = 1`, letta dal file)* **alle `7` cifre stampate**.
  - ### **`B` = escursione / `|G(0)|`** della stessa scena e dello stesso stato *(la pre-corsa di `_misura_hw`, `cs` acceso, `Lambda_c` = la media)*.
- **`P0c`, LA RIPRODUZIONE DI `29b997da`:** i `21` campioni di `G` ai tick interi di `C1` ### **devono essere BIT-IDENTICI** ai primi `21` della serie `G` del braccio `D2 cs SPENTO` nel `jsonl`. ### **Questo prova che la cadenza dichiarata sopra e' quella vera.**

### `C1` — `G` E `H` A `CS` SPENTO, TICK PER TICK

- **La scena:** quella di `D2` *(`x 0.1`, rapporto `1`, `dtau 0.5`, nessuna perturbazione, `cs` spento)*. ### **`20` tick.**
- **I campioni:**
  - a ogni tick intero `t = 0..20`: `G` *(`g_dello_stato`)* e `H` *(`h_tot`, da zero)*;
  - a ogni meta' tick `t + 1/2`, `t = 0..19`: gli stessi, ### **sulla copia al centro del palindromo.**
- **La seconda fonte:** `|G - H|` ### **entro `4096` ulp** *(`_misura_hw.ULP_SECONDA_FONTE`)* della somma dei valori assoluti dei termini *(i tetti di `termini_di_h`)*, ### **a ogni campione.** Se cade: STOP *(le due funzioni non misurano la stessa cosa)*.
- ### **IL CRITERIO, fissato qui:**
  - **(i) CONSERVA:** `max_t |H(t) - H(0)| / |H(0)|` sui tick interi `t = 1..20` e' `<= B`.
  - **(ii) PERIODO `2`:** per ogni `t = 0..18`, `dH_t = H(t+1) - H(t)` e `dH_(t+1)` hanno ### **segno opposto**, e `|dH_t| > B |H(0)|`.
- **Il caso che DEVE RIUSCIRE:** ### **la scena di `M-B2`** *(`DV.scena(MB2.NN, MB2.SEME, 0.5, ...)`, il suo stato di partenza, `cs` spento)*, ### **lo stesso strumento, `20` tick:** deve dare **(i) si'** e **(ii) no**. ### **Se non riesce, lo strumento o la banda sono sbagliati: STOP**, e nessun verdetto su `C1`.
- **IL VERDETTO DI `C1`:** se **(ii)**, oppure se **(i)** cade, ### **il passo NON conserva `H` sulla materia uniforme**: e' ### **un difetto del passo, indipendente da `cs`**, e ### **si FERMA TUTTO**: `C2` non gira.

### `C2` — LA MATERIA SENZA `CAMM-MATERIA-VUOTO` *(senza `S3`)*, `cs` spento

- **La scena di `D2`**, `2000` tick, ### **`TK.percorri_tick(st, mot, par, ("CAMM-MATERIA-VUOTO",), None, len(CM.ORDINE))`**. Resta la camminata lineare e unitaria.
- **Il braccio `0`** *(controllo positivo, deve riuscire)*: ### **lo stesso ciclo con `salta = ()`**.
  - Deve riprodurre `D2` di `29b997da` ### **al bit**: `m_rho`, `m_lam` e `G` uguali al `jsonl`.
  - ### **Se non riesce: STOP.**
- **Si riportano, come in `29b997da`:**
  - `gamma` di `rho` e di `Lambda` *(in tick e in tempo proprio)*;
  - il modo dominante *(`onda`)*, ### **`k = pi` o no**;
  - gli anelli sopra la soglia;
  - `max|delta rho| / rho_m` alla fine.
- ### **«CRESCE» se `gamma >= t_(99.73%, 4) * barra`** *(la soglia di `29b997da`, `6.62`)*.
  - ### ⚠ **Se `max|delta rho|` e' ZERO ESATTO in qualche tick del tratto**, `log` non esiste: si scrive ### **«zero esatto: lo stato uniforme e' un punto fisso al bit»**, che e' ### **«non cresce»**.
- **LA LETTURA, fissata qui** *(e' quella di Luca)*:
  - ### **SE CRESCE: il difetto e' nella camminata.**
  - ### **SE NON CRESCE: l'instabilita' nasce dall'accoppiamento `S3` materia-vuoto**, e si riporta ### **su quale modo** *(quello del braccio `0`: `k = pi` o no)*.

### ⛔ **COSA MI FA FERMARE:** una prova di `P0` che cade; la seconda fonte che non coincide; il caso di `M-B2` che non riesce; `C1` che cade *(e allora `C2` non gira)*; il braccio `0` di `C2` che non riproduce `D2` al bit.

### ⛔ **NESSUNA INTERPRETAZIONE FISICA**: ne' «alla Jeans», ne' una legge che stabilizzi. ### **`LINEARE` e `Lambda_c` FERMI.**

## 2-bis. ANNOTAZIONE DEL `2026-10-20`, `09:58`, PRIMA DEL CODICE: LA SCALA DEL SALTO DI `H` *(decisione di Luca sullo STOP di `363c6559`; si annota, non si riscrive)*

**IL FATTO, letto dal guardiano** nel referto `doc/referti_l2/controllo_passo.txt`:
- sulla materia uniforme *(`x 0.1`, `cs` spento, `dtau 0.5`)* ### **`H` e' un'ONDA TRIANGOLARE ESATTA di periodo `2` tick** *(`-1937.18`, `-2129.38`, `-2321.58`, `-2129.38`, `-1937.18`, ...)*, ripetuta a `12` cifre;
- ### **lo stato uniforme e' un'orbita periodica esatta del passo, e `H` non e' costante lungo l'orbita**;
- `192.2 / 961 = 0.2` per nodo, `= rho_medio * dtau` *(`0.4 * 0.5`)*: ### **forse una coincidenza.**

### ⚠ **LA CAUTELA DEL GUARDIANO:** il criterio di `C1` prendeva la banda del secondo ordine ### **da un'ALTRA scena** *(`C1` di strada `(d)`)* e la applicava alla materia uniforme. ### **Un passo con `theta = pi dtau` non piccolo puo' avere, su uno stato particolare, un errore di discretizzazione grande ma ORDINARIO, che scala come `dtau^2`.** ### **«Difetto del passo» si dice solo dopo questa misura.** *(Lo STOP di `363c6559` resta com'e', e la sua frase «difetto del passo» si legge con questa cautela.)*

### `S1` — LA MISURA

- **Lo strumento:** `csv/_scala_salto.py`, che riusa `_controllo_passo` *(il campione a tick intero e a meta' tick, la seconda fonte, la scena di `M-B2`)*.
- **Le corse:**
  - **la materia uniforme**, `cs` spento, ### **`dtau` in `{0.5, 0.25, 0.125}`** e ### **`x` in `{0.01, 0.1, 1}`**: `9` corse;
  - **la scena di `M-B2`**, `cs` spento, agli stessi tre `dtau`.
- ### ⚠ **LA DURATA E' A TEMPO TOTALE FISSO, `T = 10`** *(`20` tick a `dtau 0.5`, come il mandato; `40` a `0.25`; `80` a `0.125`)*. ### **Perche':** e' il protocollo di `M-B2` *(a tick fissi l'errore globale ha un'altra pendenza)*, e a tick fissi la corsa a `0.125` durerebbe `2.5` unita' di tempo, ### **forse meno di un periodo dell'oscillazione.** ### **E' una scelta mia, dichiarata qui.**
- **Che cosa si misura:**
  - **sulla materia uniforme:** ### **il salto di `H` a mezzo tick, per nodo** = la media di `|H(t + 1/2) - H(t)|` *(e `|H(t+1) - H(t+1/2)|`)* su tutta la corsa, diviso `n`; la sua dispersione *(min, max)*; e l'escursione `max |H - H(0)|`;
  - **sulla scena di `M-B2`:** ### **l'escursione** `max_t |H(t) - H(0)|` sui tick interi *(lo stato non e' uniforme: il salto non e' costante)*.
- **`rho_medio`** si stampa dallo strumento *(`mean(densita_materia)`)*, ### **non si ricopia.**

### `S2` — LE DUE PREVISIONI, che si escludono *(scritte prima)*

**Partendo da `0.2` per nodo a `dtau 0.5`, `x 0.1`:**

| `dtau` | **`P2` errore ORDINARIO** *(`~ dtau^2`)* | **`P1` termine NON conservato al primo ordine** *(`~ rho_medio * dtau`)* |
|---|---|---|
| `0.5` | `0.2` | `0.2` |
| `0.25` | `0.05` | `0.1` |
| `0.125` | `0.0125` | `0.05` |

- **E in `x`:** sotto `P1` il salto e' ### **proporzionale a `rho_medio`, cioe' a `x`** *(a `dtau 0.5`: `0.02`, `0.2`, `2` per `x` `0.01`, `0.1`, `1`)*; sotto `P2` ### **la previsione in `x` non c'e'**, e si riporta e basta.
- ### **IL VERDETTO, dalla pendenza `p` di `log(salto)` contro `log(dtau)` sui tre punti:**
  - `p` e' il fit ai minimi quadrati sui tre punti; si stampano ### **anche le due pendenze a coppie** *(`0.5 -> 0.25` e `0.25 -> 0.125`)*;
  - ### **LA BARRA, dichiarata qui:** `barra = |p_(0.5->0.25) - p_(0.25->0.125)| / 2`, ### **la curvatura, cioe' quanto i tre punti sono lontani dal regime asintotico**, piu' in quadratura la propagazione della dispersione dei salti *(trascurabile se il salto e' costante a `12` cifre)*. ### **Un fit a tre punti con un parametro libero ha UN grado di liberta':** la soglia e' la `t` di Student a `1` grado al `99.73%`, ### **calcolata dallo strumento.**
  - ### **`P2` se `|p - 2| <= t * barra`; `P1` se `|p - 1| <= t * barra`.** ### **Se valgono entrambe, o nessuna: si riporta il numero, e basta.**
  - **lo stesso verdetto per ognuna delle tre `x`.**

### `S3` — LA SCOMPOSIZIONE, a `dtau 0.5`, `x 0.1`, a ogni mezzo tick

- **I termini**, ### **con le stesse operazioni e nello stesso ordine** di `energia_pesata.termini_di_h`:
  - **nodo:** `psi` *(`-OMEGA_H (nrm_psi - pu_psi)`)*, `phi` *(`-OMEGA_H (nrm_phi - pu_phi)`)*, la moneta *(`eps h`)*, `N`;
  - **arco:** `psi` e `phi`, ### **ciascuno diviso in norma** *(`-OMEGA_H nrm/2`)* **e incrocio** *(`+OMEGA_H Re(incro)`)*.
- ### **LA PROVA AL BIT:** `per_nodo` e `per_arco` ricostruiti dai pezzi ### **coincidono AL BIT, elemento per elemento**, con quelli di `termini_di_h`, e la loro somma con `g_dello_stato`. ### **Se no: STOP** *(la scomposizione non e' quella di `H`)*.
- **Si riporta:** ogni termine a ogni mezzo tick, e ### **quale termine porta il salto** *(il salto di ciascuno, per nodo)*.

### `S4` — IL CASO CHE DEVE RIUSCIRE

- ### **Sulla scena di `M-B2` l'escursione di `H` scala come `dtau^2`:** ### **`|p - 2| <= t * barra`**, con la stessa barra e la stessa soglia.
- ### **E' cio' che `C1` di strada `(d)` ha gia' misurato** *(con `cs` acceso)*: lo strumento sa riconoscere il secondo ordine. ### **Se non riesce: STOP**, nessun verdetto sulla materia uniforme.

### `S5` — DOPO, secondo l'esito *(il mandato di Luca)*

- ### **Se `P2`:** si registra; ### **`C2` gira a un `dtau` per cui il salto di `H` sulla materia uniforme sta entro la banda `B`**, e ### **l'instabilita' di `29b997da` va RIFATTA a quel `dtau`** prima di qualunque lettura. ### **Il `dtau` lo dichiaro PRIMA, in un'annotazione, dai numeri di questa misura.**
- ### **Se `P1`: STOP.** Il termine che salta e la sua legge vanno a Luca; `C2` non gira.
- **Se ne' l'una ne' l'altra:** il numero, e ### **STOP** *(non decido io quale dei due rami si applica)*.

### ⛔ **`LINEARE`, `Lambda_c` e ogni lettura «alla Jeans» restano FERMI.**

## 2-ter. ANNOTAZIONE DEL `2026-10-20`, `10:27` *(si annota, non si riscrive)*

### **IL VERDETTO E' `P2`** *(decisione di Luca del `2026-10-20`, `10:27`, sullo STOP di `69094682`)*
- ### **Come e' stato letto: dalle PREVISIONI NUMERICHE fissate prima** in questo task history *(sez.`2-bis`, tabella di `S2`)*, ### **non da un criterio nuovo.**
  - a `dtau 0.25`: `P2` `0.05`, `P1` `0.1`, ### **misurato `0.038`**;
  - a `dtau 0.125`: `P2` `0.0125`, `P1` `0.05`, ### **misurato `0.0098`**;
  - ### **`P1` e' escluso di un fattore `5`.**
- ### **Il test di significativita' non poteva separare** *(`3` punti, `1` grado di liberta', soglia `235.8`)*: ### **e' un difetto del criterio, non dei dati.**
- ### **LA CAUSA:** il salto di `H` sta ### **TUTTO nel termine della moneta** *(`eps h`)*, che vale `+192.2`, `0`, `-192.2`, `0`: ### **sulla materia uniforme l'elicita' dello spinore PRECEDE a ogni tick**; l'ampiezza va a zero come `dtau^2` *(pendenza `2.17`)*. Gli altri termini sono costanti entro `4e-15` per nodo.
- ### **LA NUMERAZIONE DEGLI ERRORI, allineata:**
  - **errori del guardiano:** ### **`n.20`** e' la correzione detta in chat il `2026-10-20` *(«l'instabilita' potrebbe sparire a `dtau` piu' piccolo»: `D3` di `29b997da` l'aveva gia' escluso, gamma in tempo proprio `0.469` contro `0.468`)*; ### **`n.21`** e' il criterio a tre punti, che non regge un test di significativita';
  - ### **il mio «errore `n.20`» di `69094682` NON e' della serie del guardiano: e' MIO**, e lo rinumero ### **`C.1`**, il primo di una serie mia numerata *(i miei errori precedenti nella relazione non erano numerati in modo coerente)*. ### **`C.1`:** ho messo nella barra ### **la dispersione dei salti lungo l'orbita**, che non e' rumore ma la forma dell'oscillazione.

## 3. TODO DEL NEXT STEP

1. Questo task history, l'**errore `n.19`** nella relazione, e ### **l'OSSERVAZIONE nella mappa** *(la lunghezza dell'era `1`, la scala della griglia)*: commit e push ### **PRIMA del codice**.
2. `csv/_controllo_passo.py`, con la voce in `doc/INVENTARIO_strumenti.md`: ### **un commit a se'.**
3. La corsa dal blob committato e pulito: `python csv/_controllo_passo.py > doc/referti_l2/controllo_passo.txt`.
4. Il referto e la relazione: un commit, poi `PUSHATO` e, se un criterio cade, `FERMO`.
