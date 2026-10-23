# IL VERSO E L'INTENSITA' DELLA FORZA DA `cs`: UN PACCHETTO DI MATERIA IN UN GRADIENTE DI `cs`

> **Il mandato:** di Luca, dopo `44d4963d`. ### **Una MISURA, non sceglie niente.** ### **`cs` per nodo SOLO nella scena, in memoria** *(`mot.cs` come array,
> `mot.lambda_c = None`, come la misura `2` di `51f45268`)*; `leggi.yaml`, l'impronta `2e7f795d2a52fbe7` e il nucleo intatti; ### **`soliton_simulator.py` al blob
> `b8c21049`** *(sha1-BYTE; git `e96ca41a`)*. ### **`matrice()` e `rami_seguiti()` di `csv/_massa_vicino_al_cono.py`, `spettro()`, `catene()` e `blob()` di
> `csv/_universalita_massa.py` IMPORTATI, non copiati.** ### **La previsione si fissa PRIMA della corsa, e dopo NON si corregge.**
> *(Un mio abbozzo dello stesso mandato, del `2026-10-22`, mai committato, e' stato sostituito da questo: vale l'ultima versione del mandato, [[PRECEDENZA-IN-CODA]].)*

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*.
2. **Il gradino:** `(a)` ### **i controlli** *(`eta = 0`, lo specchio, la linearita', il caso che deve fallire, le taglie)*; `(b)` ### **la previsione semiclassica dai soli
   spettri uniformi, fissata e committata PRIMA della corsa**; `(c)` ### **il verso della forza**.
3. **Aggiunge un numero o una legge?** ### **No.** ### **La larghezza `W`, la finestra del fit e il criterio di «gradiente quasi costante» sono SCELTE DI MISURA**, non di
   fisica, ### **dichiarate qui**; ### **le taglie le mettono alla prova** *(raddoppiando `Lx` raddoppiano `W` e la finestra)*.
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'**, a mano e in memoria: ### **e' la variabile della prova.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **un gradiente di `cs` SPINGE un pacchetto di materia, e verso dove?** *(verso `cs` basso come la relativita' generale, o
   verso `cs` alto: repulsiva)*

## 1. LE VERIFICHE NEL CODICE E NEI REFERTI, FATTE PRIMA *(il mandato le chiede)*

- ### **`(i)` `s` PER NODO = `dtau_nodo / dtau_rif`** *(`flussi_parziali.s_nodo`)*, ### **con `dtau_nodo = dtau * cs`** *(`flussi_parziali.dtau_nodo`, il ramo della forma
  `cs`: con `mot.cs = None` ritorna `mot.dtau` tale e quale)* ### **e `dtau_rif = 1`** *(`flussi_parziali.dtau_rif`)*. ### **`s` PER ARCO = LA MEDIA ARMONICA dei due capi**
  *(`flussi_parziali.s_arco`, scritta `S/2 - D^2/(2S)` con `S = d_i + d_j`, `D = d_i - d_j`, divisa per `dtau_rif`)*. ### **Il cono `0 < s <= 1` e' ASSERITO** *(`_nel_cono`,
  per nodo e per arco)*. ### **CONFERMATO.**
- ### **`(ii)` `CAMM-MONETA-SPIN` usa il `dtau` DEL NODO, `cs` compreso:** ### **`motore._moneta_spin` fa `np.take(FP.dtau_nodo(self), nodo, ...)`** *(il nodo di ogni
  ESTREMITA')* ### **e moltiplica per `eps * frazione`.** ### **E le coppie al bit di `51f45268` girarono ANCHE a `eps 0.5`**, ### **a tutte e due le taglie**
  *(`doc/referti_l2/massa_vicino_al_cono.txt`, la misura `2`: `lato 32 eps 0.5` e `lato 64 eps 0.5`, tre coppie ciascuno, `PASSA 0.000e+00`)*. ### **QUINDI LA MASSA DA MONETA
  SENTE `cs`, attraverso `s`, come quella del generatore.**
- ### **LE PENDENZE DEL GUARDIANO, RICONTROLLATE dal `jsonl` di `44d4963d`** *(lato `64`, `d ln(Dt per tick)/ds` fra `s 0.99` e `s 1`, con `Dt = s * Delta per tempo proprio`;
  conto in memoria sul `jsonl` committato)*: ### **i numeri COINCIDONO** *(`-1.686`, `-1.635`, `-1.212`, `-0.612`)*, ### **ma con due precisazioni:**
  - ### ⚠ **a `eps 0.25` il `-1.69` e' della `catena 1`, NON della catena principale** *(la `catena 0` di `eps 0.25` si ferma a `s 0.9`: non ha `s 0.99` e `1`)*;
  - ### ⚠ **«TUTTE NEGATIVE» vale per le catene principali, non per tutte le specie:** ### **le catene `1` di `eps 0.5`, `0.75` e `1` hanno pendenza POSITIVA**
    *(`+3.45`, `+1.84`, `+1.41`)*.
- ### ⭐ **E UNA PREMESSA DELLA PREVISIONE CHE NON REGGE, vista nell'esplorazione in memoria** *(nessun file scritto; i numeri li ristampa la parte `A` dello strumento)*:
  ### **le pendenze sono quelle del `Dt` del FIT** *(la curvatura del ramo)*, ### **ma la «fase per tick globale a `k = 0`», `omega(0)`, NON e' il `Dt` del fit.** ### **A `eps 0`
  la catena principale e' fatta di DUE rami** *(ciascuno doppio)*: ### **uno con `omega(0) = 0` a ogni `s`** *(curvatura NEGATIVA)*, ### **l'altro con `omega(0) = 2 pi (1 - s)`**
  *(curvatura POSITIVA)*, ### **mentre il `Dt` del fit e' circa `pi s (1 - s)`**: ### **e' un punto di Dirac col centro del gap SPOSTATO a `pi (1 - s)`.** ### **A `eps 0.5` la catena
  principale ha un solo `omega(0)`, NEGATIVO**, ### **che cresce in modulo verso il cono** *(mentre il `Dt` del fit scende)*.

## 2. RAGIONAMENTO PRELIMINARE *(cosa credo prima di guardare, e cosa NON so)*

- ### **LA SCENA, la stessa griglia di `51f45268`:** ### **il QUADRATO di `scena_l2.scena`** *(versori geometrici, `U = I`, lo stato azzerato: la camminata attorno allo
  stato nullo)*, ### **su un toro RETTANGOLARE `Lx x Ly`, `Ly = 4`** *(il pacchetto e' uniforme in `y`, `k_y = 0`)*; ### **`dtau = 1 = dtau_rif`**, quindi ### **`s = cs`
  per nodo** ### **e il tempo coordinato e' il tick**; ### **`cs(x) = s0 (1 + eta cos(2 pi x / Lx))`** *(cioe' `cs0 = s0`)*. ### **Il nodo piu' veloce ha `s = s0 (1 + |eta|) <=
  0.99 * 1.01 = 0.9999`**: ### **nessun nodo fuori dal cono**, ### **e lo strumento lo verifica PRIMA di correre** *(oltre all'assert del motore)*.
- ### **IL PACCHETTO:** ### **a `x0 = Lx/4`**, dove il gradiente e' MASSIMO e la curvatura del profilo e' NULLA: ### **`ds/dx = - s0 eta 2 pi / Lx`** *(per `eta > 0` `s` scende
  verso `+x`)*; ### **li' `s = s0`**, ### **e lo spettro uniforme e' quello a `s0`.** ### **`psi_x = e * exp(-(x - x0)^2 / (2 W^2))`**, ### **`e` un vettore proprio della catena
  principale a `k = 0`** *(il blocco `8 x 8` della materia di `A(0)`, l'autovalore con `-angle = omega(0)` del ramo)*, ### **`W = Lx / 16`** *(`8` archi a `Lx 128`, `16` a `256`:
  molti archi, `W = (Lx/4)/4`; e `Lx = 4 * (4 W)`, cioe' quattro volte la larghezza piu' il tragitto, che resta sotto `Lx/32`)*. ### **Fermo** *(`v_g = 0` a `k = 0`)*.
- ### **LE TAGLIE:** `Lx` in `(128, 256)`.
- ### **L'OSSERVABILE:** ### **il baricentro CIRCOLARE del modulo quadro nel settore della materia**, `<x> = Lx/(2 pi) arg sum_x |psi_x|^2 e^{2 pi i x / Lx}` *(sul toro le
  code non si avvolgono; per un pacchetto simmetrico da' il centro esatto)*, ### **a ogni tick.**
- ### **IL CRITERIO DEL TEMPO** *(dichiarato)*: ### **la finestra va da `t = 0` al PRIMO tick in cui `|<x> - x0| >= Lx/32`** *(li' il gradiente vale `cos(2 pi/32) = 0.981` del
  massimo: entro il `2%`, «quasi costante»)*, ### **e al piu' fino a `T = Lx/4` tick.** ### **Almeno `6` punti** *(tre parametri e tre gradi di liberta')*, ### **altrimenti NON
  LEGGIBILE.**
- ### **IL FIT:** `<x>(t) = x0 + v0 t + a t^2/2`, ### **minimi quadrati, con l'errore standard `sigma_a`** *(dalla varianza dei residui)*: ### **il «rumore del fit».**
- ### **LA NORMA FUORI:** ### **a ogni tick, `1 - sum_x ||P psi_x||^2 / (sum ||psi||^2 + sum ||phi||^2)`**, ### **`P` il proiettore sullo spazio proprio del ramo a `k = 0` e
  `s0`** *(degenere: tutti i vettori propri con lo stesso `omega(0)` entro `1e-9`)*: ### **la frazione nel settore del VUOTO o in ALTRI RAMI.** ### **Oltre il `10%` nella
  finestra: quel punto e' NON LEGGIBILE.**
- ### **CHE COSA CREDO, prima della corsa:** ### **a `eps 0` il ramo ALTO** *(`omega(0) = 2 pi (1 - s)`, curvatura positiva)* ### **va verso `omega` piu' basso, cioe' verso
  `s` ALTO, cioe' verso `cs` ALTO: REPULSIVO**; ### **il ramo BASSO** *(`omega(0) = 0` a ogni `s`)* ### **non sente niente al primo ordine.** ### **A `eps 0.5`** *(`omega(0)` negativo e
  piu' negativo verso il cono, curvatura negativa)* ### **le equazioni di Hamilton dicono verso `cs` BASSO.** ### **Ma sono conti su spettri: la dinamica li puo' smentire.**
- ### **COSA NON SO:** ### **se a `s0 = 0.99` il pacchetto e' ancora semiclassico** *(`D/v` contro `1/W`: lo stampo)*; ### **se la camminata e' simmetrica per specchio in `x`**
  *(lo dice lo specchio)*; ### **se il ramo scelto resta isolato** *(lo dice la norma fuori)*.

## 3. LA PREVISIONE SEMICLASSICA *(PARTE `A`): LE FORMULE, FISSATE ORA*

### **Dagli spettri uniformi** *(lato `64`, `matrice(64, 1.0, eps, cs=s)` e `rami_seguiti`; le definizioni di ramo massivo di `44d4963d`: dispersivo, fit `<= 5%`, `0 < Dt <= pi`)*,
### **la CATENA PRINCIPALE** = ### **la `catena 0` di `catene()`** *(su `spettro()` a `S_LISTA` e lato `64`)*; ### **a un `s` fuori da `S_LISTA`** *(`0.85` e i punti `s0 (1 +- eta)`)*
### **il ramo valido col `Dt` piu' vicino** *(in senso relativo)* ### **a quello della catena `0` al punto di `S_LISTA` piu' vicino.** ### **Dentro la catena, OGNI `omega(0)`
distinto** *(entro `1e-6`)* ### **e' una riga a se'** *(a `eps 0`: il ramo ALTO e il ramo BASSO)*.

1. ### **LA TABELLA DEL MANDATO:** ### **`omega(0)`** *(la fase per tick globale a `k = 0`, in `(-pi, pi]`)*, ### **`Dt` e `v`** *(il fit di `51f45268`, `sqrt(Dt^2 + v^2 k^2) - Dt`)*,
   ### **il segno della curvatura** *(`2 (phi(k_1) - phi(0)) / k_1^2`)*, ### **a `s` in `(0.85, 0.9, 0.95, 0.99)`, `eps` in `(0, 0.5)`.**
2. ### **`a_prev`, LA FORMULA DEL MANDATO:** `a_prev = - v^2 (d ln Delta/ds) (ds/dx)`, ### **con `Delta = |omega(0)|`** *(il mandato: `omega(k, x) = sqrt(Delta^2 + v^2 k^2)`,
   quindi `Delta = omega(0)`)*; ### **non definita dove `omega(0) = 0`.** ### **`d ln Delta/ds` per DIFFERENZA CENTRATA fra `s0 (1 - eta)` e `s0 (1 + eta)`** *(lo stesso
   intervallo di `s` che il profilo copre; gli spettri a quei due `s`, il ramo seguito per `omega(0)` piu' vicino)*. ### **E, a parte, `a_prev[Dt]`: la stessa formula col `Dt` del
   fit** *(e' cio' su cui sono fatte le pendenze del guardiano)*.
3. ### **`a_H`, LE EQUAZIONI DI HAMILTON senza supporre `omega(0) = Delta`:** `dk/dt = - d omega/dx`, `dx/dt = d omega/dk`, ### **per un pacchetto fermo**
   `a_H = - omega''(0) (d omega(0)/ds) (ds/dx)`, ### **con `omega''(0) = (segno della curvatura) * v^2 / Dt`** ### **e `d omega(0)/ds` per la stessa differenza centrata.**
   ### **Coincide con `a_prev` se e solo se `omega(0) = Dt`.**
4. ### **`a_RG = - v^2 d ln cs/dx = - v^2 (ds/dx) / s0`** *(con la stessa luce locale: punta verso `cs` BASSO)*, ### **e `a_prev/a_RG`, `a_prev[Dt]/a_RG`, `a_H/a_RG` per ogni
   `(s0, eps, ramo)`.**
5. ### **IL VERSO PREVISTO:** ### **`a/a_RG > 0` = verso `cs` BASSO** *(come la relativita' generale)*; ### **`< 0` = verso `cs` ALTO** *(repulsiva)*.

### ⛔ **LA PARTE `A` GIRA DA SOLA** *(`python csv/_forza_da_cs.py A`)* ### **e il suo referto** *(`doc/referti_l2/forza_da_cs_previsione.jsonl` e `.txt`)* ### **si committa PRIMA
che parta la parte `B`**, ### **che lo LEGGE e non ricalcola la previsione.**

## 4. LA CORSA *(PARTE `B`)* E I CRITERI, FISSATI ORA

- ### **LA GRIGLIA:** `s0` in `(0.9, 0.95, 0.99)` x `eta` in `(0, +5e-4, +1e-3, -1e-3, +5e-3, +1e-2, -1e-2)` x `eps` in `(0, 0.5)` x i rami della catena principale x `Lx` in
  `(128, 256)`. ### **Il segno meno e' il PROFILO SPECCHIATO** *(`cos -> -cos`, stesso punto di partenza)*; ### **i mezzi `eta` servono alla linearita'** *(raddoppiare `eta`)*:
  ### **`2e-2` NON si puo' usare** *(a `s0 0.99` porterebbe `s` a `1.0098`, fuori dal cono)*.
- ### **La camminata SOLA** *(`S3` saltata, `passo(..., False, (S3,), 0.0)` di `_stabilita_lineare`)*: ### **niente autointerazione.**
- ### **DEVE PASSARE, `eta = 0`:** ### **`|a| <= 2 sigma_a`, oppure `|a| < 1e-12`** *(il pavimento della doppia precisione per un pacchetto che per simmetria non si muove)*.
- ### **DEVE PASSARE, LO SPECCHIO:** ### **`a(-eta)` di segno opposto a `a(eta)`** ### **e `| |a(-eta)| - |a(eta)| | / |a(eta)| < 1e-6`**, a `eta` `1e-3` e `1e-2`.
- ### **DEVE PASSARE, LA LINEARITA':** ### **`a(eta) / a(eta/2) = 2` entro il `5%`**, a `eta` `1e-3` e `1e-2`; ### **se no, il regime non e' lineare e i numeri di quel punto non si
  leggono.**
- ### **DEVE FALLIRE, «`a = 0`» a `eta = 1e-2`:** ### **l'asserzione `|a| <= 2 sigma_a or |a| < 1e-12` deve dare FALSO**, ### **e per la chiave giusta** *(`a` e `sigma_a` finiti,
  stampati, e `|a|/sigma_a` grande: non per un `NaN` o un'eccezione)*. ### **Si applica alle righe dove `a_H != 0`**; ### **dove `d omega(0)/ds = 0`** *(`|.| < 1e-9`: il ramo BASSO a
  `eps 0`)* ### **`a_H = 0`, e li' `|a|/sigma_a` e' UNA MISURA, non un controllo.**
- ### **LE TAGLIE** *(SCELTA DI LUCA)*: ### **entro il `5%`, solo per la catena principale e i punti con `Dt > 0.01` per tick**; ### **gli altri si riportano senza criterio.**
  ### ⚠ **LA MIA LETTURA, dichiarata:** ### **il gradiente vale `s0 eta 2 pi / Lx`, quindi a `eta` fisso `a` scala come `1/Lx`**: ### **si confronta `a * Lx`** *(l'accelerazione a
  PARI GRADIENTE)*, ### **e `a` grezzo si stampa accanto.** ### **Si applica a `eta` `+-1e-3`, `+-1e-2`.**
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE:** ### **il VERSO** ### **e la tabella `a_mis`, `a_prev`, `a_prev[Dt]`, `a_H`, `a_RG`, `a_mis/a_prev`, `a_mis/a_RG`**;
  ### **l'esponente `p` di `|a_mis/a_RG|` contro `s0/(1 - s0)`** *(fit log-log sui tre `s0`, per `(eps, ramo, eta, Lx)`)*, ### **senza imporlo.** ### **Niente conclusioni oltre la
  tabella; la lettura in tre righe a parte.**
- ### ⛔ **SE PREVISIONE E MISURA NON COINCIDONO NEL VERSO, LA PREVISIONE NON SI CORREGGE:** ### **si riportano tutte e due e si scrive QUALE IPOTESI DELLA PREVISIONE CADE.**
- ### **COSA MI FA FERMARE:** ### **un nodo fuori dal cono**; ### **la norma che non si conserva** *(oltre `1e-10` relativo)*; ### **la parte `A` non committata quando parte la
  `B`.**

### 📝 **ANNOTAZIONE 1** *(prima di ogni corsa dello strumento committato, nel commit dello strumento)*: ### **la prova a vuoto delle funzioni, in memoria** *(lo strumento
nel blocco degli appunti, nessun file del repo scritto; `s0` `0.9` e `0.99`, `Lx 128`, pochi `eta`)*, ### **ha mostrato che a `eps 0` lo spazio a `k = 0` con l'`omega(0)` del ramo
ALTO ha dimensione `4`, non `2`**: ### **ci stanno anche rami NON massivi, degeneri a `k = 0`.** ### **Quindi il vettore del pacchetto e il proiettore `P` NON vengono piu' da tutto
lo spazio proprio a `k = 0`** *(come scritto al punto `2`)*, ### **ma dallo SPAZIO DEL RAMO**: ### **i vettori del ramo al primo `k` lungo `x`** *(`omega(k_1)`)* ### **proiettati
sullo spazio a `k = 0`**, ### **col rango che deve uguagliare il numero delle copie** *(asserito)*. ### **Le formule della previsione e i criteri NON cambiano.** ### ⚠ **E lo
dichiaro: la prova a vuoto ha stampato anche dei valori di `a`**; ### **non li uso, e la previsione e' gia' fissata in formule da `cbc1114f`.**

## 5. I TRIANGOLI: **NON IN QUESTA MISURA, E PERCHE'**

### **La stessa funzione NON lo permette:** ### **`_triangoli.scena` costruisce solo il toro QUADRATO `(lato, lato)`** *(non il rettangolo lungo in `x`)*; ### **e la catena
principale e il suo vettore a `k = 0` vengono da `matrice()`, `rami_seguiti()` e `spettro()`**, ### **che lavorano sul blocco `8 x 8` della cella del QUADRATO** *(i triangoli
hanno `12` complessi di materia per cella)*. ### **Servirebbe uno spettro dei triangoli, cioe' uno strumento nuovo: resta in coda, scritto nel referto.**

## 6. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_forza_da_cs.py` *(parti `A` e `B`)* e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima di ogni corsa;
3. la parte `A`, il suo referto committato *(la previsione)*;
4. la parte `B`, il referto committato con la relazione e la sezione `7` qui sotto *(le tabelle, i controlli, il confronto)*.

## 7. I RISULTATI *(scritti dopo la corsa, sotto)*
