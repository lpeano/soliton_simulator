# 2026-11-05 — LA COPPIA: LE DISTANZE, LE FASI, E TUTTE LE MISURE DELLA FORZA E DEI CAMPI *(il mandato di Luca del `2026-11-05` `12:49`; la voce `7` della coda)*

> ### ⛔ **SOLO SCRITTURA. NESSUNA CORSA, NESSUN CALCOLO.** **Il FERMO della coppia resta:** `L`, `R_A`, le distanze, le fasi, il passo statico, il riferimento singolo e il costo **li sceglie Luca, prima del codice.** Qui ci sono **proposte**, non decisioni.
> **La domanda di Luca:** che cosa succede se due solitoni come quello di `TB3` stanno abbastanza vicini da far compenetrare le corone, e piu' vicini ancora. **La decisione di Luca:** misurare TUTTO cio' che serve a capire come si comporta la forza al variare della distanza e come interagiscono i campi.

## 1. LE PREMESSE *(cosa sappiamo dal singolo, e DA DOVE viene ogni numero)*

| il fatto | il numero | la provenienza |
|---|---|---|
| col bordo il solitone e' **legato**: il centro oscilla entro mezzo nodo, il periodo dominante `~1500` lungo `A1` | `0.2` nodi in `x`, `0.12` in `y` | ### **Luca, dall'animazione** *(il task history di `TB3`, 5.13)*; **coerente** col referto *(`tb3_corsa.txt`: `r2` fra `0.11` e `0.18`, la velocita' massima `0.802` per `1000`)* |
| **il riferimento del moto del singolo** *(cio' che la voce `38` chiedeva prima della coppia)* | -- | qui **lo da' il bordo**: ogni moto della coppia molto oltre l'oscillazione del singolo e' interazione |
| il cuore ha un altopiano fino a `~15` nodi, il bordo del solitone spesso | **`4.79 +- 0.14` nodi** *(`~19`-`20`)* | lo spessore: `forma_solitone.txt` *(misurato)*; **l'altopiano a `~15`: di Luca, non misurato nel repo** |
| nel vuoto un anello con `Lambda` piu' basso fra `12` e `20` nodi; oltre `22` il vuoto e' quasi fermo | `~5` piu' basso | ### **di Luca / del guardiano, NON misurato nel repo da me** *(i profili ci sono: `campo_TB3/profili.npz`; la lettura no)* |
| la corona *(`rho` da `1e-2` a `1e-5`, fra `20` e `35` nodi)* e' un campo d'onda casuale che si rimescola in meno di `15` unita' | la correlazione `0.06` fra mappe a `15` unita' | ### **del guardiano, NON nel repo** |
| il flusso netto attraverso `22`, `26`, `30` nodi e' **sempre verso l'esterno** | `99` intervalli su `99`, `+0.023`-`+0.061` per unita' | `corona_tb3.txt` *(misurato)* |
| la corona di `TB3` ha **sei lobi coerenti** allineati ai vertici, quella di `TM1000` no | `49%` a `20`-`22` nodi, la parte coerente `0.96`-`0.99` | `forma_solitone.txt` *(misurato)* |
| le onde piu' lunghe di `~6` nodi sono **isotrope entro lo `0.1%`** | `3.25` *(`omega`)*, `6.09` *(`|v_g|`)* nodi | `isotropia_dispersione.txt` *(misurato)* |
| ### **la crescita caotica** *(la separazione di due copie quasi uguali)* | ### **un e-fold `~25` unita'** *(`D0R`, la mappa voce `1`)* **contro `~35` del mandato** | ### ⚠ **DUE NUMERI DIVERSI per la stessa cosa:** `D0R` *(`1e-12` a `631`, `1e-6` a `957`, `1e-2` a `1179`)* e il mandato. **Da riconciliare prima di usarlo in un DEVE** *(A, il terzo principio)* |

### LE ATTESE *(IPOTESI del guardiano, scritte come tali: NON risultati)*
- **corone che si toccano** *(centri a `~50` nodi)*: onde diluite e lineari, che si sommano e si attraversano; **forza media quasi zero**, al piu' debole e lenta;
- **anelli del vuoto che si toccano** *(centri sotto `~40`)*: **la forza vera passa probabilmente dal vuoto** *(la voce `33` (c), il ponte)*;
- **cuori che si toccano:** conta la fase; per i solitoni non lineari noti, **in fase si attraggono e possono fondersi, in opposizione si respingono**.

### COSA NON SO *(e che pesa sulle proposte)*
- ### **`CL`, `CLc`, `CV` NON SONO DEFINITI NEL REPO:** compaiono solo come nomi nella voce `7` della coda *(il mandato delle `18:31`)*. **Non posso «ricondurli» a `0` e `pi` leggendo il repo:** ### **la corrispondenza e' una domanda a Luca** *(4)*.
- **Se la partenza di `TB3` si puo' centrare a passi di `2.5` nodi:** lungo `A1` due nodi distano un intero; **il mezzo nodo vuole un centro su un punto medio d'arco** *(la partenza simmetrizzata di `TS` lo permette: il centro d'inversione `m2 / 2` e' un nodo o un punto medio)*; **la partenza di `TF3` / `TB3` (`V.partenza`) non lo so** -- da controllare dal codice prima del passo statico.
- **La massa inerziale del solitone non e' misurata** *(la voce `34`)*: `F = mu d''` ha `mu` in unita' della norma `M`, dichiarato; la forza vera vuole l'inerzia.
- **La banda che porta i disturbi di `Lambda`** *(per il `lambda` di E)*: la carta dell'isotropia ha misurato la banda `B` della MATERIA; **la dispersione delle fluttuazioni del VUOTO attorno a `F3`, col suo gap, non e' calcolata** -- serve una carta statica in piu' *(proposta, E)*.

## 2. LE PROPOSTE *(tutte sotto il FERMO di Luca)*

### 2.1 Il reticolo e il bordo
- **`L ~160`** *(i nodi `(160/81)^2 ~3.9` volte quelli di `L 81`)*; **il bordo di `TB3`** *(`g_max 0.03`, `phi0(t) = c(t) F3`, la stessa tabella `fase_F3.npz`: ### **da RIFARE per `L 160`?** la tabella e' del vuoto `F3` di `L 81`; `omega` non dipende da `L` se il vuoto e' uniforme, ma **`C0` va riverificato su `L 160` prima**)*.
- **Il centro del bordo:** il punto medio della coppia; **`R_A` tale che ogni solitone stia ad almeno `30` nodi dalla fascia:** `R_A >= d / 2 + 30` *(per `d = 70`: `65`; la meta' del periodo di `L 160` e' `80`: la fascia `65 .. 80`, `15` nodi contro i `12.5` di `TB3`)*. ### **Un `R_A` per tutte le distanze** *(quello del `d` piu' grande)* **o uno per distanza?** Uno per tutte tiene uguale l'ambiente; per distanza tiene uguale la distanza dalla fascia. **Decide Luca.**
- **Il costo:** **proporzionale ai nodi** *(il tick e il libro dei conti sono locali)*: `~3.9` volte `TB3` per corsa *(`TB3`: `20` pezzi da `844` a `1236` s per `30000` unita' di tempo, il log della corsa)*; ### **il numero vero dal primo pezzo**, come sempre. **Lo spazio:** le mappe `~3.9` volte quelle di `TB3` *(`90751753` byte per `30000`)*; gli stati `~3.9` volte. **Su `C:`** i jsonl *(`~43` MB per `TB3`)*.
- **Le mappe come `TB3`** *(ogni `100` tick)* **e una finestra fitta**; **gli stati completi come `TBS`** *(ogni `1500` piu' `t 0`, con la fase: la corrente nella zona di compenetrazione)*.

### 2.2 Le distanze fra i centri
- **`70`** *(il controllo: lontani)*, **`50`** *(le corone si compenetrano)*, **`35`** *(gli anelli del vuoto si toccano)*.
- **Per la legge di forza, DOPO, se la prima fase mostra una forza:** `30, 35, 40, 45, 50, 60, 70`.
- **La direzione dell'asse:** lungo `A1` *(i vertici e l'oscillazione del singolo stanno li')*; ### **un asse a `30` gradi** *(fra due vertici)* **come controllo dell'anisotropia della forza**, se Luca lo vuole.

### 2.3 Le fasi
- **Per ogni distanza:** la fase relativa **`0`** e **`pi`** *(il secondo solitone per `e^{i pi}`)*. **`CL`, `CLc`, `CV`:** ### **la corrispondenza la chiedo a Luca** *(1, «cosa non so»)*.
- ### **IL PRIMO PASSO MINIMO PROPOSTO:** **`35` in fase e `35` in opposizione**, **piu' il singolo di riferimento** *(2.4)*: **tre corse.**

### 2.4 Il riferimento
- **Un solitone singolo sullo stesso `L`, col bordo e la partenza della coppia** *(il bordo centrato dove sarebbe il punto medio? o sul singolo? -- **per sottrarre i campi della coppia, il singolo va messo dove sta ciascuno dei due, col bordo della coppia: proposta**)*: per sottrarre il singolo dalla coppia, nei campi e nel moto.

### 2.5 Il passo statico *(prima di ogni corsa; nessuna evoluzione)*
- **`E_int(d) = E(coppia a distanza d) - 2 E(singolo)` a `t 0`**, dal libro dei conti, **per `d` da `25` a `80` ogni `2.5`** *(`23` distanze)*, **in fase e in opposizione** *(`46` valutazioni)*; **la forza statica `F_s(d) = -dE_int / dd`** *(differenze centrali)*. **Pochi minuti.** ### ⚠ **Il passo di `2.5`** vuole centri a mezzo nodo *(1, «cosa non so»)*.
- **La coppia statica e' la somma di due partenze:** non e' uno stato stazionario della coppia *(i solitoni non lineari non si sommano)*: `E_int` statico dice **l'energia della sovrapposizione**, non quella di una coppia rilassata. **Dichiarato.**

## 3. LE MISURE *(ciascuna con la sua definizione e il suo DEVE; le soglie in corsivo sono PROPOSTE, da fissare con Luca)*

### A. Il moto e la forza
- **I due centri:** il centro periodico di ciascuno **dal suo semipiano** *(l'asse di separazione: la perpendicolare all'asse iniziale nel punto medio, FISSA, dichiarata)*, e **un adattamento a due gobbe** *(la somma di due copie del profilo del singolo di riferimento, coi centri liberi, ai minimi quadrati)*; `d(t)`, la velocita' relativa, l'accelerazione.
  - **DEVE `A0`:** su una coppia SINTETICA *(due singoli spostati e sommati a `d` noto)* i due metodi ridanno `d` *entro `0.05` nodi*; **`A0-F`** *(deve fallire)*: col semipiano tagliato sull'asse sbagliato *(spostato di `5` nodi)* `d` esce giusto entro `0.05`.
- **La forza lungo l'asse:** `F(d) = mu d''(t)`, **`mu = M / 2`** *(la massa ridotta di due uguali, `M` la norma di ciascuno: dichiarato; l'inerzia vera e' la voce `34`)*; **la componente trasversale** *(una coppia di forze che fa ruotare la coppia: l'angolo dell'asse nel tempo)*.
- **Il terzo principio:** le accelerazioni dei due uguali e opposte, **il baricentro fermo** *(lo scarto stampato)*.
  - **DEVE `A-S`:** con le due partenze identiche, **la simmetria di scambio** *(la rotazione di `180` gradi attorno al punto medio, che scambia i due)* **tiene entro la crescita caotica misurata**: l'asimmetria di scambio cresce **non piu' in fretta di un e-fold ogni `tau`**, ### ⚠ **`tau` da riconciliare** *(`~25` da `D0R`, `~35` dal mandato: 1)*.
- **Il confronto fra la forza dinamica `F(d)` e quella statica `F_s(d)`** *(2.5)*.

### B. L'energia
- **`E_int(t) = E_coppia(t) - 2 E_singolo(t)`** dal libro dei conti, **scomposta per termini** *(il cinetico, il vuoto, l'accoppiamento)*, contro la stessa grandezza del singolo. **La conservazione col bordo:** come in `TB3`, `E + E` assorbita contro il riferimento senza bordo *(il tick vivo non conserva `E` nella rampa: contro `2` volte il singolo, non contro `E0`)*.
  - **DEVE `B0`:** il libro dei conti del singolo di riferimento ridà, a `t 0`, quello di `TB3` scalato al bit *(se il singolo su `L 160` e' lo stesso oggetto)*: **`E` del singolo su `L 160` meno `E` del vuoto = quella su `L 81` meno il suo vuoto**, *entro `1e-10` relativo*.

### C. I campi
- **Il vuoto: il difetto di sovrapposizione** `D(t) = DeltaLambda_coppia - (DeltaLambda_singolo spostato su 1 + spostato su 2)`, la norma relativa: **se `0`, i campi del vuoto si sommano e basta; se no, il vuoto interagisce con se stesso** *(la voce `33` (c))*. **Lo spostamento:** per un intero di nodi *(la parte frazionaria del centro: stimata spostando il singolo di `+-1` nodo, il controllo)*.
  - **DEVE `C0`:** sulla coppia sintetica *(la somma di due singoli)* `D = 0` alla precisione della macchina; **`C0-F`:** con lo spostamento sbagliato di `1` nodo `D` *sotto `1e-3` relativo* *(deve fallire)*.
- **Il profilo di `Lambda` lungo l'asse fra i due e di traverso al punto medio** *(un tubo che si stringe, o un campo che si allarga: la voce `33` (c1))*; **l'energia del vuoto fra i due in funzione di `d`** *(il disco di raggio `d / 4` attorno al punto medio, dichiarato; la voce `33` (c2): **lineare in `d` come un confinamento, o decrescente come una forza a lungo raggio**)*.
- **La materia:** **l'interferenza** -- `rho_coppia - (rho_1 + rho_2)` nella zona di compenetrazione delle corone *(la lente fra i due anelli di `20`-`35` nodi)*; **lo scambio** -- il flusso di materia attraverso l'asse di separazione *(la massa di ciascun semipiano nel tempo)*; **il flusso netto verso l'esterno** come nel singolo *(`carta_corona`, attorno al punto medio, oltre `d / 2 + 35`)*.

### D. Ciascun solitone dentro la coppia
- **`w`, il cuore, l'esagonalita', l'ovalita' e la direzione dei vertici** *(`carta_forma` sul semipiano: **una deformazione di marea**, e **se gli esagoni si allineano**)*; **il respiro** *(il periodo e la fase, `respiro.py`: **se i due si sincronizzano**)*; **la fase relativa dei due** *(l'argomento della proiezione di ciascuno sullo spinore della partenza, sul suo cuore: dichiarato; **se si aggancia**)*; **il ritmo di emissione** contro il singolo.

### E. La legge di forza
- **`F(d)` ed `E_int(d)` contro due forme:** **a corto raggio `exp(-d / lambda)`** *(un portatore con massa: `lambda` dice la massa)*; **a lungo raggio una potenza di `d`** *(nel piano una forza senza massa va come `1/d`)*.
- ### **Nessuna forma scelta prima dei dati. Il criterio, scritto qui:** il `chi^2` delle due forme con le barre d'errore di mappa in mappa; ### **vince la forma col `chi^2` piu' piccolo di almeno un fattore `2`** *(proposta)*; **altrimenti «non distinguibili», e lo si scrive.**
- **`lambda` contro la dispersione del vuoto:** **serve una carta statica in piu'** *(la dispersione delle fluttuazioni del vuoto attorno a `F3`, col suo gap: come `carta_isotropia` ma sul settore `phi`)* -- **proposta, da decidere.**

### F. La fase
- **Se il segno della forza cambia fra `0` e `pi` alla stessa distanza** *(un comportamento come le cariche)*.

### G. Il rumore
- **Con le partenze sparse viste finora, un run per caso e' indicativo;** **dove si legge una forza, la proposta di ripeterla con altri semi** *(la famiglia di `D5`)*.

## 4. LE LETTURE *(di Luca, scritte prima; registrate)*
- **(p1)** Nessuna forza oltre l'oscillazione del singolo a `70` e `50` nodi, una forza a `35`: **l'interazione passa dal vuoto, non dalle corone.**
- **(p2)** Una forza gia' a `50` nodi: **le corone si parlano.**
- **(p3)** Il segno cambia con la fase: **un comportamento come le cariche.**
- **(p4)** Il difetto di sovrapposizione del vuoto non e' zero e il campo fra i due si stringe: **un ponte**, la voce `33` (c).
- **(p5)** Altro, da descrivere.

## 5. LE DOMANDE A LUCA *(il FERMO; il criterio di chiusura: le sue risposte, scritte qui come decisioni sue)*
1. **`L`** *(`~160`?)* e **`R_A`** *(uno per tutte le distanze, `65` per `d = 70`, o uno per distanza?)*; **la tabella `c(t)` riverificata su `L 160`** *(`C0`)* prima.
2. **Le distanze** *(`70`, `50`, `35`; la scansione dopo)* e **l'asse** *(`A1`; il controllo a `30` gradi?)*.
3. **Le fasi** *(`0`, `pi`)*; ### **che cosa sono `CL`, `CLc`, `CV`** *(non sono nel repo)*.
4. **Il primo passo** *(`35` in fase, `35` in opposizione, il singolo: tre corse?)*.
5. **Il passo statico** *(`25 .. 80` ogni `2.5`: i mezzi nodi)*.
6. **Il riferimento singolo** *(dove, con quale bordo)*.
7. **Le soglie proposte dei DEVE** *(`A0`, `C0-F`, il criterio `2` di E)* e **il `tau` della crescita caotica** *(`25` o `35`)*.
8. **La carta statica della dispersione del vuoto** *(per il `lambda` di E)*.
9. **Il costo e lo spazio** *(dal primo pezzo, dopo la decisione)*.
