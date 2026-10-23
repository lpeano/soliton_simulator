> ### ⛔ **GRIGLIA QUADRATA -- risultato da rifare sui triangoli (DECISIONE-SOLO-TRIANGOLI)**

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

### **LA CORSA:** `python csv/_forza_da_cs.py B`, strumento blob sha1-BYTE `e8789ea9` *(committato e pulito)*, ### **la previsione letta da `forza_da_cs_previsione.jsonl`
committata in `f6f7b108`** *(blob sha1-BYTE `4465cfc4`)*. ### **`1` controllo su `5`.** ### **I criteri NON si cambiano.**

- ### **DEVE FALLIRE «`a = 0`» a `eta 1e-2`: FALLISCE, per la chiave giusta** *(`14` righe con `a_H != 0`, `|a|/sigma_a` da `24` a `180`)*: ### **lo strumento vede una forza
  quando c'e'.**
- ### ⚠ **`eta = 0`: FALLISCE** ### **a `eps 0.5, s0 0.9, Lx 128`** *(`a = -1.44e-5`, `2.3 sigma_a`)* ### **e a `eps 0, s0 0.99`** *(tutti e due i rami e le due taglie: li' la
  norma fuori dal ramo e' `27`-`42%`, il pacchetto NON e' semiclassico)*.
- ### ⚠ **LO SPECCHIO: FALLISCE dappertutto contro `1e-6`**: ### **sulle righe pulite lo scarto e' `1e-3`-`1e-2`** *(il migliore `6.0e-6`, `eps 0` alto `s0 0.9 Lx 256 eta 1e-3`)*,
  ### **e scende passando da `Lx 128` a `256`.** ### **La camminata NON e' simmetrica per specchio al bit su questa scena**, ### **o il pacchetto non lo e'**: ### **non lo so separare.**
- ### ⚠ **LA LINEARITA': FALLISCE sulle righe dove `a` e' nullo** *(il ramo BASSO: un rapporto di due zeri)* ### **e a `s0 0.99`, `eps 0`**; ### **sulle righe con una forza vera
  sta entro il `5%`** *(`1.90`-`2.04`)*, ### **tranne `eps 0.5, s0 0.9, Lx 128, eta 1e-3`** *(`2.635`)*.
- ### ⚠ **LE TAGLIE: FALLISCONO** *(il peggiore `5.543`, sul ramo BASSO dove `a` e' nullo)*; ### **sulla riga piu' pulita** *(`eps 0` alto `s0 0.9`)* ### **lo scarto e' `5.3`-`6.5%`**,
  ### **appena fuori.**

### 7.1 LA TABELLA *(`eta > 0`; `a/a_RG > 0` = verso `cs` BASSO, `< 0` = verso `cs` ALTO)*

| `eps` | `s0` | ramo | `Lx` | `eta` | `a_mis` | `sigma_a` | `a_mis/a_RG` | `a_prev/a_RG` | `a_prev[Dt]/a_RG` | `a_H/a_RG` | `a_mis/a_H` | verso misurato | si legge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.9` | alto | `128` | `0.001` | `-3.951e-04` | `9.5e-06` | `-17.806` | `-9.000` | `-8.366` | `-19.938` | `+0.893` | verso cs ALTO | si' |
| `0` | `0.9` | alto | `128` | `0.01` | `-3.880e-03` | `6.3e-05` | `-17.486` | `-9.024` | `-8.391` | `-19.938` | `+0.877` | verso cs ALTO | si' |
| `0` | `0.9` | alto | `256` | `0.001` | `-2.065e-04` | `1.5e-06` | `-18.612` | `-9.000` | `-8.366` | `-19.938` | `+0.933` | verso cs ALTO | si' |
| `0` | `0.9` | alto | `256` | `0.01` | `-2.046e-03` | `1.1e-05` | `-18.442` | `-9.024` | `-8.391` | `-19.938` | `+0.925` | verso cs ALTO | si' |
| `0` | `0.95` | alto | `128` | `0.001` | `-8.292e-04` | `4.2e-05` | `-35.838` | `-19.002` | `-18.776` | `-41.044` | `+0.873` | verso cs ALTO | si' |
| `0` | `0.95` | alto | `128` | `0.01` | `-7.761e-03` | `2.6e-04` | `-33.544` | `-19.234` | `-19.017` | `-41.044` | `+0.817` | verso cs ALTO | si' |
| `0` | `0.95` | alto | `256` | `0.001` | `-4.130e-04` | `8.0e-06` | `-35.705` | `-19.002` | `-18.776` | `-41.044` | `+0.870` | verso cs ALTO | si' |
| `0` | `0.95` | alto | `256` | `0.01` | `-4.047e-03` | `6.2e-05` | `-34.982` | `-19.234` | `-19.017` | `-41.044` | `+0.852` | verso cs ALTO | si' |
| `0` | `0.99` | alto | `128` | `0.001` | `-3.166e-03` | `1.2e-04` | `-133.447` | `-99.325` | `-106.163` | `-222.169` | `+0.601` | verso cs ALTO | **NO** |
| `0` | `0.99` | alto | `128` | `0.01` | `-1.866e-02` | `7.7e-04` | `-78.648` | `-264.665` | `-877.066` | `-222.169` | `+0.354` | verso cs ALTO | **NO** |
| `0` | `0.99` | alto | `256` | `0.001` | `-2.114e-03` | `2.9e-05` | `-178.208` | `-99.325` | `-106.163` | `-222.169` | `+0.802` | verso cs ALTO | **NO** |
| `0` | `0.99` | alto | `256` | `0.01` | `-1.680e-02` | `4.1e-04` | `-141.600` | `-264.665` | `-877.066` | `-222.169` | `+0.637` | verso cs ALTO | **NO** |
| `0` | `0.9` | basso | `128` | `0.001` | `+1.044e-05` | `9.6e-06` | `+0.471` | -- | `-8.366` | `-0.000` | -- | nessuno (a nullo) | **NO** |
| `0` | `0.9` | basso | `128` | `0.01` | `+5.642e-05` | `8.6e-05` | `+0.254` | -- | `-8.391` | `-0.000` | -- | nessuno (a nullo) | **NO** |
| `0` | `0.9` | basso | `256` | `0.001` | `+1.347e-06` | `1.6e-06` | `+0.121` | -- | `-8.366` | `-0.000` | -- | nessuno (a nullo) | si' |
| `0` | `0.9` | basso | `256` | `0.01` | `+6.970e-06` | `1.3e-05` | `+0.063` | -- | `-8.391` | `-0.000` | -- | nessuno (a nullo) | **NO** |
| `0` | `0.95` | basso | `128` | `0.001` | `-3.993e-05` | `5.5e-05` | `-1.726` | -- | `-18.776` | `+0.000` | -- | nessuno (a nullo) | **NO** |
| `0` | `0.95` | basso | `128` | `0.01` | `-3.958e-04` | `5.1e-04` | `-1.711` | -- | `-19.017` | `-0.000` | -- | nessuno (a nullo) | **NO** |
| `0` | `0.95` | basso | `256` | `0.001` | `+9.379e-06` | `1.0e-05` | `+0.811` | -- | `-18.776` | `+0.000` | -- | nessuno (a nullo) | **NO** |
| `0` | `0.95` | basso | `256` | `0.01` | `+3.320e-05` | `7.8e-05` | `+0.287` | -- | `-19.017` | `-0.000` | -- | nessuno (a nullo) | **NO** |
| `0` | `0.99` | basso | `128` | `0.001` | `-1.455e-03` | `7.3e-05` | `-61.337` | -- | `-106.163` | `+0.000` | -- | verso cs ALTO | **NO** |
| `0` | `0.99` | basso | `128` | `0.01` | `-1.444e-02` | `6.0e-04` | `-60.857` | -- | `-877.066` | `-1.122` | -- | verso cs ALTO | **NO** |
| `0` | `0.99` | basso | `256` | `0.001` | `-5.786e-04` | `4.8e-05` | `-48.771` | -- | `-106.163` | `+0.000` | -- | verso cs ALTO | **NO** |
| `0` | `0.99` | basso | `256` | `0.01` | `-1.056e-02` | `1.6e-04` | `-89.027` | -- | `-877.066` | `-1.122` | -- | verso cs ALTO | **NO** |
| `0.5` | `0.9` | unico | `128` | `0.001` | `+5.968e-05` | `6.9e-06` | `+3.005` | `+7.286` | `-2.536` | `+3.913` | `+0.768` | verso cs BASSO | **NO** |
| `0.5` | `0.9` | unico | `128` | `0.01` | `+7.250e-04` | `2.6e-05` | `+3.651` | `+7.285` | `-2.533` | `+3.916` | `+0.932` | verso cs BASSO | si' |
| `0.5` | `0.9` | unico | `256` | `0.001` | `+3.716e-05` | `4.9e-07` | `+3.743` | `+7.286` | `-2.536` | `+3.913` | `+0.956` | verso cs BASSO | si' |
| `0.5` | `0.9` | unico | `256` | `0.01` | `+3.699e-04` | `3.6e-06` | `+3.726` | `+7.285` | `-2.533` | `+3.916` | `+0.951` | verso cs BASSO | si' |
| `0.5` | `0.95` | unico | `128` | `0.001` | `+1.386e-04` | `1.0e-05` | `+6.921` | `+7.514` | `-2.184` | `+6.868` | `+1.008` | verso cs BASSO | si' |
| `0.5` | `0.95` | unico | `128` | `0.01` | `+1.316e-03` | `3.4e-05` | `+6.571` | `+7.511` | `-2.182` | `+6.869` | `+0.957` | verso cs BASSO | si' |
| `0.5` | `0.95` | unico | `256` | `0.001` | `+6.591e-05` | `7.8e-07` | `+6.583` | `+7.514` | `-2.184` | `+6.868` | `+0.959` | verso cs BASSO | si' |
| `0.5` | `0.95` | unico | `256` | `0.01` | `+6.534e-04` | `5.3e-06` | `+6.526` | `+7.511` | `-2.182` | `+6.869` | `+0.950` | verso cs BASSO | si' |
| `0.5` | `0.99` | unico | `128` | `0.001` | `+1.761e-04` | `7.2e-06` | `+8.972` | `+7.370` | `-1.682` | `+9.928` | `+0.904` | verso cs BASSO | si' |
| `0.5` | `0.99` | unico | `128` | `0.01` | `+1.761e-03` | `3.8e-05` | `+8.971` | `+7.367` | `-1.685` | `+9.926` | `+0.904` | verso cs BASSO | si' |
| `0.5` | `0.99` | unico | `256` | `0.001` | `+9.374e-05` | `7.7e-07` | `+9.550` | `+7.370` | `-1.682` | `+9.928` | `+0.962` | verso cs BASSO | si' |
| `0.5` | `0.99` | unico | `256` | `0.01` | `+9.280e-04` | `6.4e-06` | `+9.455` | `+7.367` | `-1.685` | `+9.926` | `+0.953` | verso cs BASSO | si' |

### 7.2 I CONTROLLI, RIGA PER RIGA *(`spec` = `| |a(-eta)| - |a(eta)| | / |a(eta)|`, `lin` = `a(eta)/a(eta/2)`, `fuori` = la norma fuori dal ramo, massimo nella finestra)*

| `eps` | `s0` | ramo | `Lx` | `a(eta=0)` | `sigma_a(0)` | `spec 1e-3` | `spec 1e-2` | `lin 1e-3` | `lin 1e-2` | `fuori` |
|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.9` | alto | `128` | `-4.04e-06` | `5.6e-06` | `2.0e-02` | `1.8e-03` | `1.979` | `1.985` | `0.018` |
| `0` | `0.9` | alto | `256` | `-1.58e-08` | `2.9e-07` | `6.0e-06` | `1.6e-03` | `2.000` | `1.986` | `0.009` |
| `0` | `0.95` | alto | `128` | `-1.92e-05` | `2.4e-05` | `4.6e-02` | `1.0e-03` | `1.954` | `1.929` | `0.078` |
| `0` | `0.95` | alto | `256` | `-1.52e-06` | `1.5e-06` | `6.8e-03` | `4.2e-03` | `1.992` | `1.980` | `0.038` |
| `0` | `0.99` | alto | `128` | `-4.93e-04` | `2.3e-05` | `3.1e-01` | `1.0e-01` | `1.729` | `1.466` | `0.420` |
| `0` | `0.99` | alto | `256` | `-1.20e-04` | `5.5e-06` | `1.1e-01` | `1.5e-02` | `1.886` | `1.649` | `0.348` |
| `0` | `0.9` | basso | `128` | `+4.20e-06` | `5.6e-06` | `8.1e-01` | `1.9e-01` | `1.426` | `1.649` | `0.017` |
| `0` | `0.9` | basso | `256` | `+2.13e-08` | `2.9e-07` | `3.2e-02` | `1.8e-02` | `1.961` | `1.209` | `0.005` |
| `0` | `0.95` | basso | `128` | `+1.95e-05` | `2.4e-05` | `9.7e-01` | `2.5e-02` | `3.897` | `1.544` | `0.078` |
| `0` | `0.95` | basso | `256` | `+1.52e-06` | `1.5e-06` | `3.3e-01` | `1.8e-01` | `1.715` | `0.977` | `0.025` |
| `0` | `0.99` | basso | `128` | `+4.92e-04` | `2.3e-05` | `6.8e-01` | `9.7e-02` | `3.018` | `1.614` | `0.382` |
| `0` | `0.99` | basso | `256` | `+1.20e-04` | `5.5e-06` | `4.2e-01` | `3.0e-02` | `2.521` | `3.141` | `0.273` |
| `0.5` | `0.9` | unico | `128` | `-1.44e-05` | `6.3e-06` | `4.8e-01` | `3.8e-02` | `2.635` | `2.037` | `0.010` |
| `0.5` | `0.9` | unico | `256` | `+7.13e-08` | `3.2e-07` | `3.6e-03` | `1.6e-03` | `1.996` | `1.996` | `0.003` |
| `0.5` | `0.95` | unico | `128` | `+7.05e-06` | `1.0e-05` | `1.0e-01` | `8.0e-03` | `1.903` | `1.982` | `0.017` |
| `0.5` | `0.95` | unico | `256` | `+2.75e-07` | `5.1e-07` | `8.1e-03` | `1.6e-03` | `1.992` | `1.992` | `0.005` |
| `0.5` | `0.99` | unico | `128` | `-1.39e-06` | `9.7e-06` | `1.6e-02` | `7.6e-03` | `2.016` | `1.992` | `0.023` |
| `0.5` | `0.99` | unico | `256` | `+4.03e-07` | `5.1e-07` | `8.4e-03` | `6.9e-04` | `1.991` | `1.990` | `0.007` |

### 7.3 L'ESPONENTE `p` di `|a_mis/a_RG|` contro `s0/(1 - s0)` *(solo i punti leggibili)*

| `eps` | ramo | `Lx` | `eta` | punti | `p` |
|---|---|---|---|---|---|
| `0` | alto | `128` | `0.001` | `2` | `0.936` |
| `0` | alto | `128` | `0.01` | `2` | `0.872` |
| `0` | alto | `256` | `0.001` | `2` | `0.872` |
| `0` | alto | `256` | `0.01` | `2` | `0.857` |
| `0` | basso | `128` | `0.001` | `0` | -- |
| `0` | basso | `128` | `0.01` | `0` | -- |
| `0` | basso | `256` | `0.001` | `0` | -- |
| `0` | basso | `256` | `0.01` | `0` | -- |
| `0.5` | unico | `128` | `0.001` | `2` | `0.157` |
| `0.5` | unico | `128` | `0.01` | `3` | `0.344` |
| `0.5` | unico | `256` | `0.001` | `3` | `0.363` |
| `0.5` | unico | `256` | `0.01` | `3` | `0.361` |

### 7.4 IL CONFRONTO FRA PREVISIONE E MISURA

- ### **IL VERSO:** ### **`eps 0`, ramo ALTO: verso `cs` ALTO** *(repulsivo; `a_mis/a_RG` da `-17.5` a `-35.8` sulle righe leggibili)*, ### **come prevedevano tutte e tre le formule.**
  ### **`eps 0.5`: verso `cs` BASSO** *(come la relativita' generale; `a_mis/a_RG` da `+3.65` a `+9.55`)*, ### **come prevedevano `a_prev` e `a_H`.** ### **`eps 0`, ramo BASSO: `a`
  nullo entro l'errore** *(a `s0 0.9` e `0.95`)*, ### **come prevedeva `a_H`.**
- ### **L'INTENSITA':** ### **`a_mis/a_H` sulle righe leggibili: `0.82`-`0.93` a `eps 0` alto, `0.90`-`1.01` a `eps 0.5`.** ### **`a_prev` sbaglia di un fattore circa `2` a `eps 0`
  alto** *(perche' usa `omega(0)` come se fosse la massa e la curvatura `v^2/omega(0)`)*.
- ### ⛔ **QUALE IPOTESI CADE** *(la previsione NON si corregge)*: ### **`a_prev[Dt]`, cioe' la previsione fatta con le pendenze del `Dt` del fit** *(quelle del guardiano)*,
  ### **sbaglia il VERSO a `eps 0.5`** *(prevede verso `cs` ALTO, la misura va verso `cs` BASSO)* ### **e sbaglia sul ramo BASSO** *(prevede una forza, la misura non la vede)*.
  ### **L'ipotesi che cade e' «l'energia del pacchetto fermo e' il `Dt` del fit», cioe' `omega(0) = Delta`:** ### **la frequenza a riposo e' `omega(0)`, e la curvatura e' `v^2/Dt`**:
  ### **due numeri diversi**, ### **e la forza le vuole tutte e due** *(`a_H`)*.
- ### **L'ESPONENTE:** ### **`eps 0` alto: `p = 0.86`-`0.94`** *(solo `2` punti: `s0 0.99` non si legge)*; ### **`eps 0.5`: `p = 0.16`-`0.36`.** ### **Il conto a mano** *(`p = 1` a `eps 0`)* ### **non
  si puo' confermare con due punti.**

### 7.5 LA LETTURA, IN TRE RIGHE

1. ### **UN GRADIENTE DI `cs` SPINGE IL PACCHETTO, MA IL VERSO DIPENDE DALLA SPECIE:** ### **la massa del solo generatore** *(`eps 0`, ramo ALTO)* ### **va verso `cs` ALTO** *(repulsiva)*;
   ### **quella con la moneta** *(`eps 0.5`)* ### **va verso `cs` BASSO** *(come la relativita' generale)*; ### **il ramo BASSO di `eps 0` non si muove.**
2. ### **LA FORZA LA DANNO LE EQUAZIONI DI HAMILTON CON `omega(0)` E LA CURVATURA MISURATA** *(`a_mis/a_H` `0.82`-`1.01`)*, ### **non le pendenze del `Dt` del fit**, ### **che sbagliano
   il verso a `eps 0.5`.**
3. ### ⚠ **`4` controlli su `5` FALLISCONO:** ### **lo specchio e le taglie mostrano effetti di taglia finita** *(scendono da `Lx 128` a `256`)*, ### **e a `s0 0.99` il pacchetto non e'
   semiclassico.** ### **I versi sono netti** *(`|a|/sigma_a` fino a `180`)*; ### **le intensita' valgono come ordine di grandezza.** ### **Nessuna conclusione oltre la tabella.**
