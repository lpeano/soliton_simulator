# LA GRAVITA' COLLETTIVA SULLA CARTA: LA FREQUENZA A RIPOSO DELLA MATERIA LEGATA AL VARIARE DI `s` (`S1`, `S3`, `S4`)

> **Il mandato:** di Luca, dopo `682e15ef`. ### **Una MISURA su spettri e stati stazionari: nessuna dinamica lunga, non sceglie niente.** ### **`dtau`, `eps`, `cs` e la forma
> della non linearita' SOLO nella scena, in memoria**; `leggi.yaml`, l'impronta `2e7f795d2a52fbe7` e il nucleo intatti; ### **`soliton_simulator.py` al blob `b8c21049`**
> *(sha1-BYTE; git `e96ca41a`)*. ### **Importati, non copiati:** `matrice()` e `rami_seguiti()` *(via `_forza_da_cs.rami`)*, `_forza_da_cs.spazio_del_ramo`, `segui`, `avvolgi`,
> `_stabilita_lineare.green`, `celle`, `passo`, `S3`, `_screening_forme_s3.forma` e `pezzi_di` *(le forme `S1` e `S4`, quelle di `csv/_lineare_s1_s4.py` a sha1-BYTE `dc166098`:
> lo strumento le prende da `_screening_forme_s3`, che da allora non e' cambiato)*. ### **L'ipotesi di Luca, da provare e NON decisa:** ### **la massa e' collettiva, e la gravita'
> deve esserlo anche lei: le particelle sono i SOLITONI, non i rami lineari.**

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*.
2. **Il gradino:** ### **`(a)` i controlli** *(la pendenza `1` della sola parte non lineare sul ramo basso; il caso che deve fallire; quello che puo' fallire)*; ### **`(b)` il
   livello `1`** *(lo stato uniforme)*; ### **`(c)` il livello `2`** *(il solitone efficace)*.
3. **Aggiunge un numero o una legge?** ### **No.** ### **Le densita' `x` e le norme `N` sono SCELTE DI MISURA, dichiarate qui**; ### **la griglia radiale del livello `2` e' uno
   strumento numerico, e la sua validita' si controlla** *(la larghezza contro il passo e contro la scatola)*.
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'** *(uniforme a mano: `s = cs`, `dtau = 1`)*: ### **e' la variabile della prova.** ### **E la forma della non linearita'**
   *(`S1`, `S3`, `S4`)* ### **in memoria.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **la frequenza a riposo di un oggetto LEGATO scala come `s`** *(pendenza `+1`, la legge della relativita' generale)* ### **per
   oggetti diversi, o no?**

## 1. LE VERIFICHE NEL CODICE *(il mandato le chiede; ricontrollate, cercando per nome)*

- ### **`CAMM-MATERIA-VUOTO`:** ### **`materia_vuoto.applica` usa `dtau = FP.dtau_nodo(mot)`**, ### **cioe' `dtau * cs`** *(e' la riga che il guardiano cita, la `136` del blob di oggi)*:
  ### **CONFERMATO.** ### **La fase per estremita' e' `alpha(rho, Lambda) * dtau_nodo * frazione` sulla materia e `beta * dtau_nodo * frazione` sul vuoto.**
- ### **`CAMM-MONETA-SPIN`:** ### **`motore._moneta_spin` usa `FP.dtau_nodo`** *(`557d94d6`)*: ### **CONFERMATO.**
- ### ⚠ **`CAMM-SATURAZIONE`:** ### **`motore._saturazione` usa `FP.dtau_nodo`: CONFERMATO**, ### **MA `CAMM-SATURAZIONE` NON E' NELL'ORDINE** *(`composizione.ORDINE`: `14` pezzi, `7` leggi,
  nessuna e' la saturazione)*: ### **e' la scheda SUPERATA da `CAMM-MATERIA-VUOTO`, e NON GIRA nel passo.** ### **Il guardiano la conta fra i pezzi: nel passo di oggi non c'e'.**
- ### **`CAMM-FASE-VUOTO`:** ### **`energia_pesata.applica` usa `tau = mot.dtau[0] * frazione`, il `dtau` GLOBALE, e asserisce che sia uniforme**: ### **CONFERMATO**, ### **e il
  docstring lo DERIVA** *(il generatore pesato e' `cs_k H_k`, il parametro di flusso e' il tick)*. ### ⭐ **E IN QUESTA MISURA NON C'E':** ### **con `mot.lambda_c = None` la legge
  «non esiste»** *(la sua scheda: «a forma spenta questa legge non esiste»; e con `cs` costante a mano il termine e' zero per definizione)*.
- ### **QUINDI:** ### **sullo stato uniforme la fase non lineare per tick della materia e' `alpha(rho0, Lambda0) * s`**, ### **pendenza `+1` in `s` a densita' fissata.** ### **La domanda e'
  se lo resta per un oggetto legato.**

## 2. IL METODO

### LIVELLO 1 -- LO STATO UNIFORME

- ### **La scena:** ### **il quadrato di `51f45268`** *(`scena_l2.scena` attraverso `_stabilita_lineare.scena`, lati `32` e `64`)*, ### **`dtau = 1`, `mot.cs = s` uniforme,
  `mot.lambda_c = None`**; ### **il vuoto uniforme `phi = VUOTO = 1` per estremita'** *(`Lambda0 = 4` per nodo)*; ### **la materia: OGNI cella = `a * e`**, ### **`e` il vettore
  (normalizzato) dello spazio di un ramo massivo a `k = 0`** *(`_forza_da_cs.spazio_del_ramo`: i vettori del ramo al primo `k`, proiettati sullo spazio a `k = 0`)*, ### **`a` tale che
  `rho0 / Lambda0 = x`** *(asserito sulla scena)*.
- ### **I rami:** ### **OGNI ramo massivo valido** *(le definizioni di `44d4963d`: dispersivo, fit `<= 5%`, `0 < Dt <= pi`; da `_forza_da_cs.rami`, lato `64`)*, ### **raggruppati per
  `(Dt, omega(0))` distinti entro `1e-6`.** ### **A `eps 0, s 1` non ce n'e'** *(il gap e' nullo)*: ### **si scrive.**
- ### **Le densita' `x = rho0/Lambda0`** *(una sotto e due sopra la soglia di stabilita' NOTA)*: ### **`S1`: `0.01`, `0.3`, `1`** *(`lineare_s1_s4_materia`: stabile a `0.01`, instabile da
  `0.1`)*; ### ⚠ **`S3`: `1e-4`, `0.1`, `1`** ### **e `S4`: `0.01`, `0.3`, `1`** ### **-- per `S3` e `S4` UNA SOGLIA NOTA NON C'E'** *(`S3` instabile fino a `1e-4`, `s3_diluita`; `S4`
  instabile gia' a `0.01`)*: ### **il primo valore e' il PIU' BASSO MISURATO, non uno «sotto la soglia».** ### **Lo dira' la stabilita' misurata qui.**
- ### **`s` in `(0.85, 0.9, 0.95, 0.99, 1.0)`, `eps` in `(0, 0.5)`.**
- ### **La stazionarieta':** ### **un tick** *(`_stabilita_lineare.passo`, il passo intero coi `14` pezzi)*: ### **`psi' = e^{-i omega_tot} psi` entro `1e-12`** *(relativo, in norma)* ### **e
  `phi' = e^{-i omega_v} phi` entro `1e-12`.** ### ⚠ **«UNA fase globale» NON PUO' valere per lo stato intero:** ### **la materia prende `alpha s`, il vuoto `beta s`, e `alpha != beta`**:
  ### **lo stato e' stazionario a meno di UNA FASE PER SETTORE** *(il passo ha la simmetria `U(1) x U(1)`: le fasi dipendono solo dai moduli)*. ### **Lo scrivo prima, e lo misuro.**
- ### **La scomposizione:** ### **`omega_tot = omega_ramo(0) + alpha(rho0, Lambda0) s` entro `1e-12`** *(mod `2 pi`)*. ### **`omega_ramo(0)`** ### **dallo spettro lineare** *(la fase per tick
  a `k = 0`)*.
- ### **LA PENDENZA:** ### **`omega_tot` e' definita a meno di `2 pi`**; ### **la frequenza «assoluta» che serve al logaritmo e' `omega_ramo(0)` in `(-pi, pi]` PIU' `alpha s`**
  *(verificata contro la misura mod `2 pi`)*. ### **`d ln |omega_tot| / d ln s` per DIFFERENZA CENTRATA a `s (1 +- h)`, `h = 1e-3`**, ### **all'indietro a `s = 1`** *(oltre il cono non
  si va)*; ### **il ramo seguito con `_forza_da_cs.segui`**; ### **`omega_tot` misurata a tutti e tre gli `s`.**
- ### **LO STATO PIU' BASSO** a una densita': ### **il ramo con `omega_tot` minima** *(la quasi-energia per tick, con `omega_ramo(0)` in `(-pi, pi]`)*. ### ⚠ **Su un reticolo una
  quasi-energia e' definita mod `2 pi`: «piu' basso» e' relativo a questa convenzione, ed e' dichiarato.**
- ### **LA STABILITA' LINEARE:** ### **`_stabilita_lineare.green`** *(la funzione di Green di UN tick, `R(k)`, coordinate reali, `eps_rel 1e-7`)*, ### **riportata nel riferimento che
  ruota**: ### **`R'(k) = Phi^{-1} R(k)`**, ### **`Phi` la rotazione di `omega_tot` sulla materia e di `omega_v` sul vuoto** *(lo stato e' stazionario in quel riferimento, quindi
  `R'` e' COSTANTE e i suoi autovalori danno la crescita esatta: e' Floquet, non serve integrare)*. ### **Il tasso per tempo proprio `gamma = max_k ln max|lambda(R'(k))| / s`**;
  ### **STABILE se `gamma < 1e-3 * 0.4018 = 4.0e-4`** *(la soglia di `_lineare_s1_s4`, decisione di Luca delle `18:09`, col massimo di riferimento `R2`)*.

### LIVELLO 2 -- IL SOLITONE EFFICACE

- ### **LA DERIVAZIONE** *(dichiarata, coi suoi limiti)*: ### **un pacchetto lento su UN ramo, `psi = A(x, t) e(k = 0) e^{-i omega0 t}`**; ### **la dispersione del ramo
  `omega(k) = omega0 + c k^2 + ...`** *(isotropa al secondo ordine: il quadrato ha la simmetria di `90` gradi)*, ### **`c = omega''(0)/2` col SEGNO** *(`omega'' = segno della
  curvatura * v^2/Dt`, il fit di `51f45268` e il segno di `2(phi(k_1) - phi(0))/k_1^2`)*; ### **`k^2 -> -lap`**; ### **la fase non lineare per tick `g = s alpha(|A|^2, Lambda0)`**
  *(la forma con il suo fattore `s`)*:
  `i dA/dt = - c(s) lap A + s alpha(|A|^2, Lambda0) A`.
  ### **I LIMITI:** ### **inviluppo lento** *(larghezza `>>` `1` arco: si controlla)*; ### **un ramo solo** *(niente mescolamento)*; ### **`Lambda = Lambda0` fisso** *(il vuoto prende solo
  fasi da `beta`, ma un `beta` non uniforme lo fa camminare e cambia `|phi|`: ### **la reazione del vuoto e' TRASCURATA**)*; ### **la continuita' al posto del reticolo.**
- ### **LO STATO LEGATO:** ### **`mu u = - c lap u + s alpha(u^2) u`**, ### **radiale in `2d`, `u(r)` reale**, ### **norma `N = 2 pi int r u^2 dr`** *(in unita' di `rho` per nodo, un nodo
  per arco quadrato)*. ### **Se `c < 0`** ### **si moltiplica per `-1`**: ### **`(-mu) u = -|c| lap u - s alpha u`** ### **-> si cerca il MINIMO di `int |c| |grad u|^2 + sigma s Lambda0 F(u^2/Lambda0)`**
  *(`sigma` il segno di `c`)*. ### **Il metodo:** ### **il flusso di gradiente normalizzato all'indietro** *(Eulero implicito sul laplaciano e sul potenziale, la norma riportata a
  `N` a ogni passo; il potenziale traslato del suo minimo, che non cambia lo stato)*, ### **griglia `r_j = (j + 1/2) dr`, `u(R) = 0`.** ### **Partenza: una gaussiana.**
  ### **Convergenza: `|delta mu| < 1e-12` e `||delta u|| < 1e-10`**, ### **altrimenti «NON CONVERGE».**
- ### **I VERDETTI DI ESISTENZA** *(risultati, non errori)*: ### **«DISPERSIONE»** se la larghezza supera `R/5` *(lo stato riempie la scatola)*; ### **«COLLASSO»** se scende sotto
  `2 dr`; ### **«L'INVILUPPO LENTO NON VALE»** se la larghezza e' sotto `2` archi.
- ### **LE GRANDEZZE:** ### **`omega_sol(s; N) = omega0(s) + mu`**, ### **la larghezza** `w = sqrt(int r^2 u^2 / int u^2)`, ### **la densita' al centro `u(0)^2`** *(e `x` al centro)*.
- ### **LE NORME `N`:** `1`, `10`, `100` *(dichiarate)*. ### **`s` come al livello `1`**, ### **la pendenza `d ln |omega_sol| / d ln s` con lo stesso `h`**; ### **sui rami dove c'e' uno
  stato legato.**
- ### **IL CONTROLLO CHE PUO' FALLIRE:** ### **`c` fissato a mano COSTANTE in `s`** *(il valore del ramo BASSO a `eps 0, s 0.9`)* ### **e `omega0 = 0`**: ### **la sola dipendenza da
  `s` e' il fattore della non linearita'.**

## 3. LE PREVISIONI *(scritte prima di ogni numero)*

- ### **LIVELLO 1, la scomposizione: TIENE** *(entro `1e-12`)*, ### **perche' la fase non lineare e' UNIFORME su tutte le estremita'**: ### **e' una fase globale sulla materia, commuta con
  la camminata lineare, e l'autovettore resta autovettore.**
- ### **LIVELLO 1, le pendenze:** `omega_tot = omega_ramo(0) + alpha s`:
  - ### **`eps 0`, ramo BASSO** *(`omega_ramo = 0`)*: ### **pendenza `1` ESATTA** *(il controllo che deve passare)*;
  - ### **`eps 0`, ramo ALTO** *(`omega_ramo = 2 pi (1 - s)`)*: ### **`(alpha s - 2 pi s) / (2 pi (1 - s) + alpha s)`**: ### **NON `1`, e DIPENDE DA `rho0`** *(attraverso `alpha`)*:
    ### **una violazione**; ### **a `rho0 -> 0` vale `-s/(1 - s)`** *(il caso che deve fallire: `-9` a `s 0.9`)*;
  - ### **`eps 0.5`** *(`omega_ramo(0)` negativo, `-0.228` a `s 0.9`, `557d94d6`)*: ### **la somma di una parte che scende con `s` e di una che sale: pendenza ne' `1` ne' uguale fra
    densita'.**
- ### **LIVELLO 2, l'esistenza:** ### **`alpha` CRESCE con `rho` in tutte e tre le forme** *(`rho d alpha/d rho > 0`, l'accoppiamento di `2026-10-22`)*: ### **la non linearita' e'
  REPULSIVA dove `c > 0` e ATTRATTIVA dove `c < 0`.** ### **Quindi uno stato legato solo sui rami a curvatura NEGATIVA** *(il ramo BASSO di `eps 0` e il ramo di `eps 0.5`)*;
  ### **sul ramo ALTO: DISPERSIONE.** ### **Fra le forme:** ### **`S3` a poca materia e' logaritmica** *(`alpha ~ ln(rho/Lambda) + 1`)* ### **-> la gaussiana esatta, sempre legata**;
  ### **`S4` va come `x^{2/pi}`, sotto-critica in `2d` -> legata**; ### **`S1` va come `x^2` a poca materia, SOPRA-critica in `2d`** ### **-> sotto una norma critica si disperde, sopra si
  lega** *(la saturazione `x^2/(1 + x^2)` ferma il collasso)*.
- ### **LIVELLO 2, la formula chiusa per `S3`** *(limite `rho << Lambda`, `c < 0`)*: ### **`u = a e^{-r^2/(2 sigma^2)}`, `sigma^2 = |c|/s`, `a^2 = N s/(pi |c|)`**, ### **`mu = s [ln(N s/(pi
  |c|)) - 1 - ln Lambda0]`.** ### **Quindi `omega_sol = omega0(s) + mu` DIPENDE DA `N`** *(attraverso `ln N`)* ### **E DA `c(s)`** *(che vicino al cono va come `v^2/(2 Dt)`, `Dt ~ pi s (1 - s)`:
  CRESCE senza limite)*: ### **la pendenza NON e' `1` e NON e' uguale fra norme diverse: UNA VIOLAZIONE PREVISTA.**
- ### **IL CONTROLLO CHE PUO' FALLIRE** *(`c` costante, `omega0 = 0`)*: ### **la mia previsione e' che FALLISCA**: ### **con `S3` la formula da' `d ln mu/d ln s = 1 + 1/(ln(N s/(pi |c|)) - 1 - ln
  Lambda0)`**, ### **che e' `1` solo se il logaritmo e' grande**: ### **il termine cinetico NON scala con `s`, quindi la forma dello stato si aggiusta e la frequenza non e' `s` per una costante.**
  ### **Se invece passasse, la sola non linearita' darebbe la legge della relativita' generale a ogni norma.**

## 4. I CRITERI, FISSATI ORA

- ### **DEVE PASSARE:** ### **livello `1`, ramo con `omega_ramo(0) = 0` a ogni `s`** *(`eps 0`, BASSO)*: ### **la pendenza della SOLA parte non lineare** *(`omega_tot - omega_ramo(0)`,
  tutte e due misurate)* ### **`= 1` entro `1e-9`**, ### **a ogni `(forma, x, s < 1, lato)`.**
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«pendenza `= 1`» sul ramo ALTO di `eps 0` senza non linearita'** *(`rho0 = 0`: la sola `omega_ramo(0)`)*: ### **l'asserzione
  `|pendenza - 1| < 1e-9` deve dare FALSO** ### **con la pendenza FINITA e stampata** *(non per un `NaN` o un logaritmo di zero)*.
- ### **PUO' FALLIRE:** ### **livello `2`, `c` costante e `omega0 = 0`: la pendenza di `omega_sol` `= 1` entro `1e-6`**, ### **per ogni forma e norma dove c'e' uno stato legato.**
- ### **DI SERVIZIO** *(devono passare perche' i numeri si leggano)*: ### **la stazionarieta' per settore entro `1e-12`**; ### **la scomposizione entro `1e-12`**; ### **`rho0/Lambda0 = x`
  entro `1e-12`.**
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE:** ### **la tabella delle pendenze per `(livello, forma, eps, x o N, ramo)`**, ### **col criterio di lettura del mandato:**
  ### **`+1` e UGUALE per oggetti diversi; qualunque altro valore, o una dipendenza dalla norma o dalla forma, e' una VIOLAZIONE.** ### **Nessuna conclusione oltre la tabella**; ### **la
  lettura in tre righe a parte, piu' UNA riga su che cosa dice per la scelta fra `S1` e `S4`** *(informazione per Luca, non una scelta)*.

### 📝 **ANNOTAZIONE 1** *(prima di ogni corsa dello strumento committato, nel commit dello strumento)*: ### **la prova a vuoto delle funzioni in memoria** *(lo strumento negli
appunti, nessun file del repo scritto)* ### **ha trovato un DIFETTO DEL MIO RISOLUTORE, non della fisica:** ### **nella coda dello stato `u^2` scende sotto il piu' piccolo doppio, e
`alpha` di `S3`** *(`ln(rho/(rho + Lambda))`)* ### **diventa `-inf`.** ### **NON metto un pavimento su `rho`** *(`A11`)*: ### **la scatola si sceglie perche' la coda resti
RAPPRESENTABILE** *(`R = 12 sigma`, `dr = sigma/40`, `sigma = sqrt(|c|/s)`: la coda gaussiana a `R` vale `e^{-144}`)*, ### **e un potenziale non finito marca il caso «NON
RAPPRESENTABILE» invece di dare un numero.** ### **Visto anche:** ### **gli stati legati NON dipendono dalla scatola** *(la stessa larghezza a `R = 12` e `24 sigma`)*, ### **quelli
dispersi crescono con lei**: ### **il criterio `R/5` li separa.** ### **E aggiungo un controllo DI SERVIZIO del risolutore:** ### **sul logaritmo puro** *(`alpha = ln(rho/Lambda) + 1`)*
### **deve dare la gaussiana esatta** *(`mu` entro `1e-6` relativo)*. ### ⚠ **La prova a vuoto ha stampato anche dei valori di livello `1` e `2`: non li uso; le previsioni sono
fissate in `151b31e2`.**

### 📝 **ANNOTAZIONE 2** *(dopo la prima corsa, che si e' FERMATA, `d222af13`; prima della seconda)*: ### ⛔ **LA DIAGNOSI SCRITTA IN `d222af13` ERA SBAGLIATA.** ### **Non si e'
fermata a `eps 0.5`**: ### **si e' fermata a `eps 0, s = 1`**, ### **dove i «rami massivi» hanno `Dt` del fit `1.6e-9` e `3.0e-9`** ### **-- rumore su un cono SENZA massa, appena sopra
la soglia `1e-9` della definizione di `44d4963d`** *(in `51f45268` lo stesso `Delta(1)` era `7.5e-10`, sotto)*: ### **due gruppi da UNA copia** *(`omega(k_1) = +-0.0694`)* ### **e al primo
`k` un autovalore DOPPIO**: ### **l'asserzione di `spazio_del_ramo` e' GIUSTA, li' lo spazio del ramo non e' definito.** ### **Avevo letto il primo `eps` del giro successivo invece
di guardare il punto.** ### **LE DUE CORREZIONI** *(uno strumento nuovo, `6870ee85` -> questo commit)*: ### **(1) un ramo il cui spazio non e' definito SI SCRIVE** *(«RAMO NON
DEFINITO»)* ### **e non si misura**, ne' al livello `1` ne' al `2`; ### **(2) i rami si raggruppano per le FASI PROPRIE `omega(0)` e `omega(k_1)`**, ### **non per il `Dt` del fit**
*(il fit e' rumoroso fino a `~1e-6` fra due copie; nessun caso l'aveva ancora rotto, ma e' la grandezza sbagliata)*. ### **Nessun criterio cambia**; ### **la previsione «a `eps 0, s 1`
non ce n'e'» era giusta nella fisica, e la definizione numerica la contava.**

### 📝 **ANNOTAZIONE 3** *(prima della terza corsa)*: ### **la prova a vuoto dell'intero programma** *(griglia ridotta, il `jsonl` negli appunti)* ### **ha mostrato che il mio
controllo DI SERVIZIO del risolutore FALLISCE con `dr = sigma/40`**: ### **`mu` sbaglia di `9.4e-5` relativo contro la gaussiana esatta** *(la tolleranza fissata e' `1e-6`)*.
### **L'errore e' di DISCRETIZZAZIONE, di ordine `2` misurato** *(in memoria, `c -0.8, s 0.9, N 10`)*:

| `dr` | `sigma/40` | `sigma/80` | `sigma/160` | `sigma/320` | `sigma/640` |
|---|---|---|---|---|---|
| errore relativo di `mu` | `9.4e-5` | `2.3e-5` | `5.9e-6` | `1.5e-6` | `3.7e-7` |

### **`dr = sigma/640`: il PRIMO dimezzamento sotto `1e-6`** *(una regola, non una taratura; costa `0.01` s per stato)*. ### **La tolleranza NON cambia.** ### **Visto anche, e scritto
prima della corsa:** ### **il «deve passare» incontrera' `S4` a `x = 1`, dove `alpha = 0`** *(la fase non lineare si annulla: la sua pendenza logaritmica non esiste)*: ### **fallira' li',
e il criterio resta.**

### 📝 **ANNOTAZIONE 4** *(il mandato di Luca «correzione del criterio, errore del guardiano n.45», arrivato a TERZA CORSA GIA' FINITA, `d6c03598`)*: ### **la pendenza
logaritmica `d ln omega/d ln s` NON e' ben posta** ### **dove `omega` passa per lo zero** *(lo zero di una frequenza non ha significato speciale)* ### **e dove `alpha = 0`**
*(`S4` a `x = 1`)*. ### **IL CRITERIO GIUSTO DELLA RELATIVITA' GENERALE:** ### **la frequenza in TEMPO PROPRIO, `omega/s`, non dipende da `s`** *(`dtau_rif = 1`, `cs = s`)*.
### **AGGIUNTE, SENZA TOGLIERE NIENTE** *(nello strumento di questo commit)*:
- ### **`D = d(omega/s)/ds`** *(assoluta, sempre definita; centrata, all'indietro a `s = 1`)* ### **e `R = s D/(omega/s)` quando `|omega/s| > 1e-6`**, ### **ai due livelli.**
  ### **Criterio di lettura: `D = 0`** *(entro `1e-9` al livello `1`, `1e-6` al livello `2`)* ### **e' la legge della relativita' generale.**
- ### **le pendenze logaritmiche RESTANO nel referto**, ### **marcate NON LEGGIBILI dove `|omega| < 1e-6` o `|alpha| < 1e-12`.**
- ### **IL DEVE-PASSARE DIVENTA:** ### **ramo basso di `eps 0`, `|D| < 1e-9`.** ### **IL DEVE-FALLIRE DIVENTA:** ### **«`D = 0`» sul ramo alto di `eps 0` senza non linearita'**
  *(la sola `omega_ramo(0) = 2 pi (1 - s)`: `D = -2 pi/s^2`)*. ### **I due vecchi si stampano, SENZA verdetto.** ### **Il puo'-fallire del livello `2` resta com'era, e `D` gli sta
  accanto.**
- ### **LA PREVISIONE, sulla carta, prima della corsa nuova:** ### **al livello `1` `omega_tot/s = omega_ramo(0)/s + alpha`**, ### **e `alpha` non dipende da `s` a densita'
  fissata: QUINDI `D_tot = D_ramo`, ESATTAMENTE.** ### **IL LEGAME E' LA LEGGE DELLA RELATIVITA' GENERALE AL BIT; la viola SOLO la parte lineare del ramo** ### **-- sul ramo
  basso `D = 0`, sul ramo alto `-2 pi/s^2`** *(`-7.757` a `s 0.9`)*.

## LA CONVENZIONE DELLO ZERO *(mandato n.45, punto `3`: si MOSTRA, NON si cambia -- e' una decisione di fisica di Luca)*

- ### **COME SONO SCRITTI OGGI I PEZZI PARZIALI** *(cercati per nome, nel blob di oggi)*:
  - ### **`CAMM-GROVER`** *(e `CAMM-GROVER-VUOTO`)*: ### **`flussi_parziali.grover`**, ### **`G(theta) = P_u + e^{i theta} (I - P_u) = exp(i theta (I - P_u))`** *(il docstring; e
    l'intestazione del modulo: «`G = 2 P_u - I = exp(i pi (I - P_u))`»)*, ### **`theta = pi s_nodo frazione`** *(`z_nodo`)*;
  - ### **`CAMM-SPOSTAMENTO`** *(e `CAMM-SPOSTAMENTO-VUOTO`)*: ### **`flussi_parziali.hop_psi` e `hop_phi`**, ### **`alpha I + beta S_U = I + (e^{i theta} - 1) P- = exp(i theta P-)`**,
    ### **`P- = (I - S_U)/2`** *(`_alfa_beta`; l'intestazione: «`exp(i pi P-) = I - 2 P- = S_U`»)*, ### **`theta = pi s_arco frazione`** *(`z_arco`)*;
  - ### **`CAMM-MONETA-SPIN`:** ### **`exp(-i eps dtau_nodo sigma.n)`** *(`motore._moneta_spin`, `_ruota_attorno_a_n`)*: ### **NON e' un pezzo parziale di quella forma** ### **-- il suo
    generatore `sigma.n` ha traccia nulla, le fasi proprie sono `+-a`, gia' centrate**: ### **resta com'e' nelle due convenzioni.**
- ### **L'ALTERNATIVA:** ### **ogni pezzo parziale `exp(-i theta P)`, col proiettore COMPLEMENTARE** *(`P_u` per il Grover, `P+ = (I + S_U)/2` per lo spostamento)*: ### **e' LO STESSO
  pezzo per la fase globale `e^{-i theta}`** *(`exp(i theta (I - P)) = e^{i theta} exp(-i theta P)`)*.
- ### **SULLA CARTA, a `cs` uniforme:** ### **sulla materia, in un tick, i due mezzi Grover tolgono `e^{i pi s}` e i due mezzi spostamenti `e^{i pi s}`**: ### **`lambda_alt = e^{-2 pi i s}
  lambda`**, ### **cioe' `omega_alt(0) = omega(0) + 2 pi s` (mod `2 pi`)** *(con `omega = -angle(lambda)`)*, ### **per OGNI ramo e ogni `k`** *(`Dt` e `v` non cambiano)*.
- ### ⭐ **E COSA FA A `D`:** ### **se la fase si segue CON CONTINUITA'** *(`omega + 2 pi s`)*, ### **`omega_alt/s = omega/s + 2 pi`: `D_alt = D`, LA CONVENZIONE NON PESA.** ### **Se invece
  la fase si riporta in `(-pi, pi]`** *(come fa oggi `omega_ramo(0)`)*, ### **l'intero aggiunto `2 pi k` vale `2 pi k/s` in tempo proprio** ### **e `D` cambia di `-2 pi k/s^2`.**
  ### **La previsione per i due rami di `eps 0`:**

| ramo | `omega(0)` oggi | `D` oggi | `omega(0)` alternativa in `(-pi, pi]` | `D` alternativa avvolta | `D` alternativa continua |
|---|---|---|---|---|---|
| BASSO | `0` | **`0`** | `2 pi s - 2 pi = -2 pi (1 - s)` | `+2 pi/s^2` | **`0`** |
| ALTO | `2 pi (1 - s)` | `-2 pi/s^2` | `2 pi = 0` | **`0`** | `-2 pi/s^2` |

  ### ⚠ **QUINDI: CON LE FASI RIPORTATE IN `(-pi, pi]` LA CONVENZIONE DECIDE QUALE RAMO E' «COME LA RELATIVITA' GENERALE»** *(oggi il BASSO, nell'alternativa l'ALTO)*; ### **con le
  fasi seguite con continuita' non decide niente.** ### **La domanda di fisica per Luca e' quale `2 pi k` e' la frequenza a riposo di un oggetto** *(quale intero ha l'orologio)*.
- ### **LA VERIFICA, con gli spettri** *(nello strumento, in memoria)*: ### **`flussi_parziali.grover`, `hop_psi`, `hop_phi` avvolte per `e^{-i theta}`** *(stessi `z_nodo` e `z_arco`)*,
  ### **gli spettri rifatti**, ### **`omega_alt(0) = omega(0) + 2 pi s` entro `1e-12`** *(DI SERVIZIO)* ### **e `Dt` uguale entro il rumore del fit** *(`1e-6`)*; ### **per ogni ramo: `D`
  oggi, `D` alternativa avvolta, `D` alternativa continua.**

## 5. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_gravita_collettiva.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima di ogni numero;
3. la corsa, il referto `doc/referti_l2/gravita_collettiva.txt` e `.jsonl`, la relazione, e la sezione `6` qui sotto.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*

### **LA CORSA VALIDA E' LA QUARTA** *(strumento sha1-BYTE `9c34fb6a`, `f3180571`, il criterio `D` di n.45)*. ### **Le tre prima:** ### **`d222af13` e `8a0a6fd5` si sono FERMATE**
*(il ramo non definito al cono, la mia diagnosi sbagliata e poi corretta; un `KeyError`)*; ### **`d6c03598` e' completa col criterio vecchio**, ### **sostituita da questa.**

### **`8` controlli su `9`:** ### **le cinque DI SERVIZIO passano** *(stazionarieta' per settore `2.3e-14` su `360` stati; scomposizione `1.1e-14`; `x` `5.6e-16`; la convenzione:
`omega(0)` `1.3e-15`, `Dt` `2.6e-7`; la gaussiana esatta `3.7e-7`)*; ### **DEVE PASSARE: `|D| <= 9.9e-12` su `72` stati del ramo basso: PASSA**; ### **DEVE FALLIRE: «`D = 0`» sul ramo
alto a `rho0 = 0` FALLISCE per la chiave giusta** *(`D = -8.70, -7.76, -6.96, -6.41` a `s 0.85`-`0.99`, uguale a `-2 pi/s^2` alle cifre stampate)*; ### ⚠ **PUO' FALLIRE: FALLISCE**
*(`c` costante: la pendenza `+2.32`..`+3.13` per `S1`, `+0.56`..`+0.74` per `S3`, `+0.54`..`+14.7` per `S4`; e `D` non nullo, `+0.27`..`+1.09`)*. ### **Il criterio vecchio, stampato senza verdetto:**
### **sul ramo basso, dove si legge, `|p - 1| <= 4.3e-8`**; ### **il `652` era `S4` a `x = 1`, dove `alpha = 0`.**

### 6.1 LIVELLO 1: `D = d(omega_tot/s)/ds` per ramo *(il massimo e il minimo su forma, `x` e lato: se coincidono, `D` NON dipende dalla forma ne' dalla densita')*

| `eps` | `s` | ramo | `D` min | `D` max | `D_ramo` *(la sola parte lineare, convenzione di oggi)* | stati |
|---|---|---|---|---|---|---|
| `0` | `0.85` | Dt 0.4074 w0 +0.0000 | `-5.387847e-12` | `+6.269495e-12` | `+6.146570e-13` | `18` |
| `0` | `0.85` | Dt 0.4074 w0 +0.9425 | `-8.696459e+00` | `-8.696459e+00` | `-8.696459e+00` | `18` |
| `0` | `0.9` | Dt 0.2836 w0 +0.0000 | `-7.894919e-12` | `+9.868649e-12` | `+0.000000e+00` | `18` |
| `0` | `0.9` | Dt 0.2836 w0 +0.6283 | `-7.757027e+00` | `-7.757027e+00` | `-7.757027e+00` | `18` |
| `0` | `0.95` | Dt 0.1454 w0 +0.0000 | `-5.901712e-12` | `+3.447535e-12` | `-2.462791e-13` | `18` |
| `0` | `0.95` | Dt 0.1454 w0 +0.3142 | `-6.961985e+00` | `-6.961985e+00` | `-6.961985e+00` | `18` |
| `0` | `0.99` | Dt 0.0280 w0 +0.0628 | `-6.410766e+00` | `-6.410766e+00` | `-6.410766e+00` | `18` |
| `0` | `0.99` | Dt 0.0280 w0 -0.0000 | `-5.382900e-12` | `+5.186648e-12` | `-2.263267e-13` | `18` |
| `0.5` | `0.85` | Dt 0.4902 w0 -0.1524 | `-1.237544e+00` | `-1.237544e+00` | `-1.237544e+00` | `18` |
| `0.5` | `0.9` | Dt 0.0132 w0 +0.6126 | `-7.598298e+00` | `-7.598298e+00` | `-7.598298e+00` | `18` |
| `0.5` | `0.9` | Dt 0.4253 w0 -0.2284 | `-1.772688e+00` | `-1.772688e+00` | `-1.772688e+00` | `18` |
| `0.5` | `0.95` | Dt 0.0163 w0 +0.3054 | `-6.787263e+00` | `-6.787263e+00` | `-6.787263e+00` | `18` |
| `0.5` | `0.95` | Dt 0.3735 w0 -0.3413 | `-2.463685e+00` | `-2.463685e+00` | `-2.463685e+00` | `18` |
| `0.5` | `0.95` | Dt 1.0325 w0 +0.6555 | `-4.498300e+00` | `-4.498300e+00` | `-4.498300e+00` | `18` |
| `0.5` | `0.99` | Dt 0.0189 w0 +0.0609 | `-6.222123e+00` | `-6.222123e+00` | `-6.222123e+00` | `18` |
| `0.5` | `0.99` | Dt 0.3448 w0 -0.4645 | `-3.018999e+00` | `-3.018999e+00` | `-3.018999e+00` | `18` |
| `0.5` | `0.99` | Dt 0.7162 w0 +0.5273 | `-3.391767e+00` | `-3.391767e+00` | `-3.391767e+00` | `18` |
| `0.5` | `1` | Dt 0.0195 w0 +0.0000 | `-6.097366e+00` | `-6.097366e+00` | `-6.097366e+00` | `18` |
| `0.5` | `1` | Dt 0.3392 w0 -0.5000 | `-3.135685e+00` | `-3.135685e+00` | `-3.135685e+00` | `18` |
| `0.5` | `1` | Dt 0.6799 w0 +0.5000 | `-3.153790e+00` | `-3.153790e+00` | `-3.153790e+00` | `18` |

### **LO SCARTO MASSIMO fra forme, densita' e lati a pari `(eps, s, ramo)`: `2.40e-11`.**
### **`|D_tot - D_ramo|` massimo: `1.27e-11`.**


### 6.2 LIVELLO 1: LO STATO PIU' BASSO *(la quasi-energia minima, convenzione dichiarata)* E LA SUA STABILITA' *(lato `32`; soglia `4.0e-4` per tempo proprio)*

| forma | `eps` | `x` | `s 0.85` | `s 0.9` | `s 0.95` | `s 0.99` | `s 1` |
|---|---|---|---|---|---|---|---|
| S1 | `0` | `0.01` | +0.0000, `1.70e-08` **STABILE** | +0.0000, `1.87e-06` **STABILE** | +0.0000, `2.01e-06` **STABILE** | -0.0000, `3.63e-08` **STABILE** | -- |
| S1 | `0` | `0.3` | +0.0000, `1.67e-01` instab. | +0.0000, `1.57e-01` instab. | +0.0000, `1.32e-01` instab. | -0.0000, `4.80e-02` instab. | -- |
| S1 | `0` | `1` | +0.0000, `5.85e-01` instab. | +0.0000, `5.02e-01` instab. | +0.0000, `3.74e-01` instab. | -0.0000, `1.74e-01` instab. | -- |
| S1 | `0.5` | `0.01` | -0.1524, `1.62e-08` **STABILE** | -0.2284, `1.65e-07` **STABILE** | -0.3413, `5.98e-09` **STABILE** | -0.4645, `5.09e-05` **STABILE** | -0.5000, `1.58e-07` **STABILE** |
| S1 | `0.5` | `0.3` | -0.1524, `1.69e-01` instab. | -0.2284, `1.59e-01` instab. | -0.3413, `1.45e-01` instab. | -0.4645, `1.26e-01` instab. | -0.5000, `1.21e-01` instab. |
| S1 | `0.5` | `1` | -0.1524, `5.89e-01` instab. | -0.2284, `5.18e-01` instab. | -0.3413, `4.24e-01` instab. | -0.4645, `3.20e-01` instab. | -0.5000, `2.89e-01` instab. |
| S3 | `0` | `0.0001` | +0.0000, `5.85e-01` instab. | +0.0000, `5.02e-01` instab. | +0.0000, `3.74e-01` instab. | -0.0000, `1.74e-01` instab. | -- |
| S3 | `0` | `0.1` | +0.0000, `5.49e-01` instab. | +0.0000, `4.73e-01` instab. | +0.0000, `3.54e-01` instab. | -0.0000, `1.65e-01` instab. | -- |
| S3 | `0` | `1` | +0.0000, `3.58e-01` instab. | +0.0000, `3.18e-01` instab. | +0.0000, `2.48e-01` instab. | -0.0000, `1.22e-01` instab. | -- |
| S3 | `0.5` | `0.0001` | -0.1524, `5.96e-01` instab. | -0.2284, `5.42e-01` instab. | -0.3413, `4.86e-01` instab. | -0.4645, `4.48e-01` instab. | -0.5000, `4.39e-01` instab. |
| S3 | `0.5` | `0.1` | -0.1524, `5.58e-01` instab. | -0.2284, `5.07e-01` instab. | -0.3413, `4.50e-01` instab. | -0.4645, `4.05e-01` instab. | -0.5000, `3.94e-01` instab. |
| S3 | `0.5` | `1` | -0.1524, `3.60e-01` instab. | -0.2284, `3.26e-01` instab. | -0.3413, `2.71e-01` instab. | -0.4645, `2.00e-01` instab. | -0.5000, `1.78e-01` instab. |
| S4 | `0` | `0.01` | +0.0000, `1.65e-01` instab. | +0.0000, `1.55e-01` instab. | +0.0000, `1.31e-01` instab. | -0.0000, `4.64e-02` instab. | -- |
| S4 | `0` | `0.3` | +0.0000, `6.32e-01` instab. | +0.0000, `5.40e-01` instab. | +0.0000, `4.00e-01` instab. | -0.0000, `1.86e-01` instab. | -- |
| S4 | `0` | `1` | +0.0000, `9.02e-01` instab. | +0.0000, `7.53e-01` instab. | +0.0000, `5.46e-01` instab. | -0.0000, `2.48e-01` instab. | -- |
| S4 | `0.5` | `0.01` | -0.1524, `1.68e-01` instab. | -0.2284, `1.62e-01` instab. | -0.3413, `1.53e-01` instab. | -0.4645, `1.45e-01` instab. | -0.5000, `1.44e-01` instab. |
| S4 | `0.5` | `0.3` | -0.1524, `6.40e-01` instab. | -0.2284, `5.71e-01` instab. | -0.3413, `4.92e-01` instab. | -0.4645, `4.23e-01` instab. | -0.5000, `4.05e-01` instab. |
| S4 | `0.5` | `1` | -0.1524, `9.06e-01` instab. | -0.2284, `7.79e-01` instab. | -0.3413, `6.31e-01` instab. | -0.4645, `4.82e-01` instab. | -0.5000, `4.39e-01` instab. |

### **Stati STABILI in tutto il livello `1`: `40` su `360`.**
### **Dove:** `S1 eps 0 x 0.01`, `S1 eps 0.5 x 0.01`


### 6.3 LIVELLO 2: IL SOLITONE EFFICACE -- `D = d(omega_sol/s)/ds` dove lo stato e' LEGATO ai tre `s` *(e `x` al centro, larghezza)*

| forma | `eps` | ramo | `N` | `s` | `D` | `R` | larghezza | `x` al centro | inviluppo lento |
|---|---|---|---|---|---|---|---|---|---|
| S1 | `0` | Dt 0.2836 w0 +0.0000 | `100` | `0.9` | `-3.7011e+00` | `+11.2924` | `2.103` | `2.46` | si' |
| S1 | `0` | Dt 0.4074 w0 +0.0000 | `100` | `0.85` | `-1.7221e+00` | `+9.4200` | `1.588` | `3.7` | **NO** |
| S1 | `0.5` | Dt 0.3392 w0 -0.5000 | `100` | `1` | `-3.0144e+00` | `+9.1706` | `1.536` | `3.89` | **NO** |
| S1 | `0.5` | Dt 0.3448 w0 -0.4645 | `100` | `0.99` | `-2.9776e+00` | `+9.1840` | `1.539` | `3.88` | **NO** |
| S1 | `0.5` | Dt 0.3735 w0 -0.3413 | `100` | `0.95` | `-2.7690e+00` | `+9.0987` | `1.521` | `3.94` | **NO** |
| S1 | `0.5` | Dt 0.4253 w0 -0.2284 | `100` | `0.9` | `-2.3696e+00` | `+8.7229` | `1.449` | `4.25` | **NO** |
| S1 | `0.5` | Dt 0.4902 w0 -0.1524 | `100` | `0.85` | `-1.9018e+00` | `+8.2064` | `1.356` | `4.7` | **NO** |
| S3 | `0` | Dt 0.0280 w0 -0.0000 | `1` | `0.99` | `-1.0584e+02` | `+35.4344` | `2.960` | `0.00908` | si' |
| S3 | `0` | Dt 0.0280 w0 -0.0000 | `10` | `0.99` | `-9.8442e+01` | `+35.4344` | `3.016` | `0.0866` | si' |
| S3 | `0` | Dt 0.0280 w0 -0.0000 | `100` | `0.99` | `-6.6961e+01` | `+35.4344` | `3.389` | `0.655` | si' |
| S3 | `0` | Dt 0.1454 w0 +0.0000 | `1` | `0.95` | `-1.8575e+01` | `+15.6727` | `1.321` | `0.0454` | **NO** |
| S3 | `0` | Dt 0.1454 w0 +0.0000 | `10` | `0.95` | `-1.4307e+01` | `+15.6727` | `1.422` | `0.379` | **NO** |
| S3 | `0` | Dt 0.1454 w0 +0.0000 | `100` | `0.95` | `-7.0609e+00` | `+15.6727` | `1.836` | `2.11` | **NO** |
| S3 | `0` | Dt 0.2836 w0 +0.0000 | `1` | `0.9` | `-8.4577e+00` | `+11.2924` | `0.961` | `0.0853` | **NO** |
| S3 | `0` | Dt 0.2836 w0 +0.0000 | `10` | `0.9` | `-5.7639e+00` | `+11.2924` | `1.078` | `0.647` | **NO** |
| S3 | `0` | Dt 0.2836 w0 +0.0000 | `100` | `0.9` | `-2.5789e+00` | `+11.2924` | `1.473` | `3.22` | **NO** |
| S3 | `0` | Dt 0.4074 w0 +0.0000 | `1` | `0.85` | `-5.1851e+00` | `+9.4200` | `0.808` | `0.12` | **NO** |
| S3 | `0` | Dt 0.4074 w0 +0.0000 | `10` | `0.85` | `-3.2817e+00` | `+9.4200` | `0.932` | `0.856` | **NO** |
| S3 | `0` | Dt 0.4074 w0 +0.0000 | `100` | `0.85` | `-1.4053e+00` | `+9.4200` | `1.311` | `4.02` | **NO** |
| S3 | `0.5` | Dt 0.3392 w0 -0.5000 | `1` | `1` | `-2.7610e+00` | `+9.1706` | `0.788` | `0.126` | **NO** |
| S3 | `0.5` | Dt 0.3392 w0 -0.5000 | `10` | `1` | `-2.9011e+00` | `+9.1706` | `0.913` | `0.891` | **NO** |
| S3 | `0.5` | Dt 0.3392 w0 -0.5000 | `100` | `1` | `-3.0358e+00` | `+9.1706` | `1.289` | `4.16` | **NO** |
| S3 | `0.5` | Dt 0.3448 w0 -0.4645 | `1` | `0.99` | `-2.8911e+00` | `+9.1840` | `0.789` | `0.126` | **NO** |
| S3 | `0.5` | Dt 0.3448 w0 -0.4645 | `10` | `0.99` | `-2.9389e+00` | `+9.1840` | `0.914` | `0.889` | **NO** |
| S3 | `0.5` | Dt 0.3448 w0 -0.4645 | `100` | `0.99` | `-2.9849e+00` | `+9.1840` | `1.290` | `4.15` | **NO** |
| S3 | `0.5` | Dt 0.3735 w0 -0.3413 | `1` | `0.95` | `-3.4137e+00` | `+9.0987` | `0.782` | `0.128` | **NO** |
| S3 | `0.5` | Dt 0.3735 w0 -0.3413 | `10` | `0.95` | `-3.0564e+00` | `+9.0987` | `0.907` | `0.902` | **NO** |
| S3 | `0.5` | Dt 0.3735 w0 -0.3413 | `100` | `0.95` | `-2.7156e+00` | `+9.0987` | `1.283` | `4.2` | **NO** |
| S3 | `0.5` | Dt 0.4253 w0 -0.2284 | `1` | `0.9` | `-3.6993e+00` | `+8.7229` | `0.752` | `0.139` | **NO** |
| S3 | `0.5` | Dt 0.4253 w0 -0.2284 | `10` | `0.9` | `-2.9540e+00` | `+8.7229` | `0.878` | `0.96` | **NO** |
| S3 | `0.5` | Dt 0.4253 w0 -0.2284 | `100` | `0.9` | `-2.2702e+00` | `+8.7229` | `1.249` | `4.41` | **NO** |
| S3 | `0.5` | Dt 0.4902 w0 -0.1524 | `1` | `0.85` | `-3.4871e+00` | `+8.2064` | `0.710` | `0.155` | **NO** |
| S3 | `0.5` | Dt 0.4902 w0 -0.1524 | `10` | `0.85` | `-2.5826e+00` | `+8.2064` | `0.838` | `1.05` | **NO** |
| S3 | `0.5` | Dt 0.4902 w0 -0.1524 | `100` | `0.85` | `-1.7971e+00` | `+8.2064` | `1.203` | `4.75` | **NO** |
| S4 | `0` | Dt 0.0280 w0 -0.0000 | `100` | `0.99` | `-9.1493e+01` | `+35.4344` | `4.003` | `0.578` | si' |
| S4 | `0` | Dt 0.1454 w0 +0.0000 | `10` | `0.95` | `-1.2877e+01` | `+15.6727` | `2.242` | `0.193` | si' |
| S4 | `0` | Dt 0.1454 w0 +0.0000 | `100` | `0.95` | `-1.7620e+01` | `+15.6727` | `1.417` | `4.14` | **NO** |
| S4 | `0` | Dt 0.2836 w0 +0.0000 | `10` | `0.9` | `-7.8400e+00` | `+11.2924` | `1.281` | `0.565` | **NO** |
| S4 | `0` | Dt 0.2836 w0 +0.0000 | `100` | `0.9` | `-7.6144e+00` | `+11.2924` | `1.015` | `7.78` | **NO** |
| S4 | `0` | Dt 0.4074 w0 +0.0000 | `10` | `0.85` | `-5.2948e+00` | `+9.4200` | `0.980` | `0.94` | **NO** |
| S4 | `0` | Dt 0.4074 w0 +0.0000 | `100` | `0.85` | `-4.5122e+00` | `+9.4200` | `0.855` | `10.8` | **NO** |
| S4 | `0.5` | Dt 0.3392 w0 -0.5000 | `10` | `1` | `-2.7485e+00` | `+9.1706` | `0.944` | `1.01` | **NO** |
| S4 | `0.5` | Dt 0.3392 w0 -0.5000 | `100` | `1` | `-2.8112e+00` | `+9.1706` | `0.834` | `11.3` | **NO** |
| S4 | `0.5` | Dt 0.3448 w0 -0.4645 | `10` | `0.99` | `-2.8870e+00` | `+9.1840` | `0.946` | `1.01` | **NO** |
| S4 | `0.5` | Dt 0.3448 w0 -0.4645 | `100` | `0.99` | `-2.9082e+00` | `+9.1840` | `0.836` | `11.3` | **NO** |
| S4 | `0.5` | Dt 0.3735 w0 -0.3413 | `10` | `0.95` | `-3.4486e+00` | `+9.0987` | `0.934` | `1.03` | **NO** |
| S4 | `0.5` | Dt 0.3735 w0 -0.3413 | `100` | `0.95` | `-3.2851e+00` | `+9.0987` | `0.828` | `11.5` | **NO** |
| S4 | `0.5` | Dt 0.4253 w0 -0.2284 | `10` | `0.9` | `-3.8043e+00` | `+8.7229` | `0.882` | `1.15` | **NO** |
| S4 | `0.5` | Dt 0.4253 w0 -0.2284 | `100` | `0.9` | `-3.4255e+00` | `+8.7229` | `0.797` | `12.3` | **NO** |
| S4 | `0.5` | Dt 0.4902 w0 -0.1524 | `10` | `0.85` | `-3.6639e+00` | `+8.2064` | `0.813` | `1.34` | **NO** |
| S4 | `0.5` | Dt 0.4902 w0 -0.1524 | `100` | `0.85` | `-3.1460e+00` | `+8.2064` | `0.754` | `13.7` | **NO** |

### **L'esistenza** *(su tutti gli stati del livello `2`)*: `S1` DISPERSIONE `53`; `S1` LEGATO `7`; `S3` DISPERSIONE `33`; `S3` LEGATO `27`; `S4` DISPERSIONE `43`; `S4` LEGATO `17`.


### 6.4 IL CONTROLLO CHE PUO' FALLIRE *(`c` costante, `omega0 = 0`)*: `D` e la pendenza

| forma | `N` | `s` | esiste | pendenza | `D` |
|---|---|---|---|---|---|
| S1 | `1` | `0.85` | DISPERSIONE | -- | -- |
| S1 | `1` | `0.9` | DISPERSIONE | -- | -- |
| S1 | `1` | `0.95` | DISPERSIONE | -- | -- |
| S1 | `1` | `0.99` | DISPERSIONE | -- | -- |
| S1 | `1` | `1` | DISPERSIONE | -- | -- |
| S1 | `10` | `0.85` | DISPERSIONE | -- | -- |
| S1 | `10` | `0.9` | DISPERSIONE | -- | -- |
| S1 | `10` | `0.95` | DISPERSIONE | -- | -- |
| S1 | `10` | `0.99` | DISPERSIONE | -- | -- |
| S1 | `10` | `1` | DISPERSIONE | -- | -- |
| S1 | `100` | `0.85` | LEGATO | `+3.1295` | `+5.2116e-01` |
| S1 | `100` | `0.9` | LEGATO | `+2.7387` | `+4.4848e-01` |
| S1 | `100` | `0.95` | LEGATO | `+2.4906` | `+3.9733e-01` |
| S1 | `100` | `0.99` | LEGATO | `+2.3472` | `+3.6533e-01` |
| S1 | `100` | `1` | LEGATO | `+2.3181` | `+3.5857e-01` |
| S3 | `1` | `0.85` | LEGATO | `+0.7388` | `+1.0897e+00` |
| S3 | `1` | `0.9` | LEGATO | `+0.7359` | `+1.0250e+00` |
| S3 | `1` | `0.95` | LEGATO | `+0.7331` | `+9.6719e-01` |
| S3 | `1` | `0.99` | LEGATO | `+0.7310` | `+9.2516e-01` |
| S3 | `1` | `1` | LEGATO | `+0.7305` | `+9.1568e-01` |
| S3 | `10` | `0.85` | LEGATO | `+0.6229` | `+7.5115e-01` |
| S3 | `10` | `0.9` | LEGATO | `+0.6206` | `+6.9855e-01` |
| S3 | `10` | `0.95` | LEGATO | `+0.6184` | `+6.5201e-01` |
| S3 | `10` | `0.99` | LEGATO | `+0.6168` | `+6.1850e-01` |
| S3 | `10` | `1` | LEGATO | `+0.6164` | `+6.1098e-01` |
| S3 | `100` | `0.85` | LEGATO | `+0.5596` | `+3.3864e-01` |
| S3 | `100` | `0.9` | LEGATO | `+0.5586` | `+3.1255e-01` |
| S3 | `100` | `0.95` | LEGATO | `+0.5577` | `+2.8969e-01` |
| S3 | `100` | `0.99` | LEGATO | `+0.5571` | `+2.7337e-01` |
| S3 | `100` | `1` | LEGATO | `+0.5569` | `+2.6972e-01` |
| S4 | `1` | `0.85` | DISPERSIONE | -- | -- |
| S4 | `1` | `0.9` | DISPERSIONE | -- | -- |
| S4 | `1` | `0.95` | DISPERSIONE | -- | -- |
| S4 | `1` | `0.99` | DISPERSIONE | -- | -- |
| S4 | `1` | `1` | DISPERSIONE | -- | -- |
| S4 | `10` | `0.85` | LEGATO | `+0.5850` | `+9.9156e-01` |
| S4 | `10` | `0.9` | LEGATO | `+0.5687` | `+9.5019e-01` |
| S4 | `10` | `0.95` | LEGATO | `+0.5527` | `+9.1163e-01` |
| S4 | `10` | `0.99` | LEGATO | `+0.5401` | `+8.8266e-01` |
| S4 | `10` | `1` | LEGATO | `+0.5372` | `+8.7601e-01` |
| S4 | `100` | `0.85` | LEGATO | `+14.6829` | `+9.8620e-01` |
| S4 | `100` | `0.9` | LEGATO | `+8.6224` | `+9.2282e-01` |
| S4 | `100` | `0.95` | LEGATO | `+6.3564` | `+8.6641e-01` |
| S4 | `100` | `0.99` | LEGATO | `+5.3593` | `+8.2559e-01` |
| S4 | `100` | `1` | LEGATO | `+5.1783` | `+8.1640e-01` |

### 6.5 LA CONVENZIONE DELLO ZERO, MISURATA *(spettri a `cs` uniforme, lato `64`)*

| `eps` | `s` | ramo | `omega(0)` oggi | `omega(0)` alternativa | `D` oggi | `D` alternativa avvolta | `D` alternativa continua |
|---|---|---|---|---|---|---|---|
| `0` | `0.85` | Dt 0.4074 w0 +0.0000 | `+0.000000` | `-0.942478` | `+6.1466e-13` | `+8.6965e+00` | `+0.0000e+00` |
| `0` | `0.85` | Dt 0.4074 w0 +0.9425 | `+0.942478` | `+0.000000` | `-8.6965e+00` | `+0.0000e+00` | `-8.6965e+00` |
| `0` | `0.9` | Dt 0.2836 w0 +0.0000 | `+0.000000` | `-0.628319` | `+0.0000e+00` | `+7.7570e+00` | `+4.9343e-13` |
| `0` | `0.9` | Dt 0.2836 w0 +0.6283 | `+0.628319` | `+0.000000` | `-7.7570e+00` | `+0.0000e+00` | `-7.7570e+00` |
| `0` | `0.95` | Dt 0.1454 w0 +0.0000 | `+0.000000` | `-0.314159` | `-2.4628e-13` | `+6.9620e+00` | `-4.6746e-13` |
| `0` | `0.95` | Dt 0.1454 w0 +0.3142 | `+0.314159` | `+0.000000` | `-6.9620e+00` | `+0.0000e+00` | `-6.9620e+00` |
| `0` | `0.99` | Dt 0.0280 w0 -0.0000 | `-0.000000` | `-0.062832` | `-2.2633e-13` | `+6.4108e+00` | `-4.4857e-13` |
| `0` | `0.99` | Dt 0.0280 w0 +0.0628 | `+0.062832` | `+0.000000` | `-6.4108e+00` | `+0.0000e+00` | `-6.4108e+00` |
| `0.5` | `0.85` | Dt 0.4902 w0 -0.1524 | `-0.152430` | `-1.094907` | `-1.2375e+00` | `+7.4589e+00` | `-1.2375e+00` |
| `0.5` | `0.9` | Dt 0.4253 w0 -0.2284 | `-0.228427` | `-0.856746` | `-1.7727e+00` | `+5.9843e+00` | `-1.7727e+00` |
| `0.5` | `0.9` | Dt 0.0132 w0 +0.6126 | `+0.612570` | `-0.015749` | `-7.5983e+00` | `+1.5873e-01` | `-7.5983e+00` |
| `0.5` | `0.95` | Dt 0.3735 w0 -0.3413 | `-0.341330` | `-0.655489` | `-2.4637e+00` | `+4.4983e+00` | `-2.4637e+00` |
| `0.5` | `0.95` | Dt 0.0163 w0 +0.3054 | `+0.305449` | `-0.008710` | `-6.7873e+00` | `+1.7472e-01` | `-6.7873e+00` |
| `0.5` | `0.95` | Dt 1.0325 w0 +0.6555 | `+0.655489` | `+0.341330` | `-4.4983e+00` | `+2.4637e+00` | `-4.4983e+00` |
| `0.5` | `0.99` | Dt 0.3448 w0 -0.4645 | `-0.464497` | `-0.527329` | `-3.0190e+00` | `+3.3918e+00` | `-3.0190e+00` |
| `0.5` | `0.99` | Dt 0.0189 w0 +0.0609 | `+0.060946` | `-0.001886` | `-6.2221e+00` | `+1.8864e-01` | `-6.2221e+00` |
| `0.5` | `0.99` | Dt 0.7162 w0 +0.5273 | `+0.527329` | `+0.464497` | `-3.3918e+00` | `+3.0190e+00` | `-3.3918e+00` |
| `0.5` | `1` | Dt 0.3392 w0 -0.5000 | `-0.500000` | `-0.500000` | `-3.1357e+00` | `+3.1538e+00` | `-3.1357e+00` |
| `0.5` | `1` | Dt 0.0195 w0 +0.0000 | `+0.000000` | `+0.000000` | `-6.0974e+00` | `+1.9211e-01` | `-6.0974e+00` |
| `0.5` | `1` | Dt 0.6799 w0 +0.5000 | `+0.500000` | `+0.500000` | `-3.1538e+00` | `+3.1357e+00` | `-3.1538e+00` |

### **`|D` alternativa continua `- D` oggi`|` massimo: `1.01e-12`** *(la convenzione non pesa se la fase si segue con continuita')*.


### 6.6 LA LETTURA, IN TRE RIGHE *(nessuna conclusione oltre le tabelle)*

1. ### **IL LEGAME OBBEDISCE ALLA RELATIVITA' GENERALE AL BIT:** ### **al livello `1` `D_tot = D_ramo`** *(scarto `1.3e-11`)*, ### **lo stesso per tutte le forme, densita' e taglie**
   *(`2.4e-11`)*: ### **la fase non lineare `alpha s` da' `omega/s = alpha`, costante.** ### **La violazione viene SOLO dalla frequenza lineare del ramo**, ### **nulla sul ramo basso di `eps 0`**
   *(nella convenzione di oggi)*, ### **`-2 pi/s^2` sul ramo alto**, ### **da `-1.24` a `-7.60` sui rami di `eps 0.5`.**
2. ### **IL SOLITONE NON OBBEDISCE:** ### **dove esiste uno stato legato** *(solo sui rami a curvatura NEGATIVA, come previsto)* ### **`D != 0`, e DIPENDE DALLA NORMA** *(`S3, eps 0,
   s 0.9`: `-8.46`, `-5.76`, `-2.58` per `N` `1`, `10`, `100`)* ### **E DALLA FORMA**; ### **anche con `c` fissato a mano la forma che si aggiusta da' `D` da `+0.27` a `+1.09`.**
   ### **Due solitoni di norma diversa cadono diversamente: per il criterio del mandato, UNA VIOLAZIONE.** ### ⚠ **E molti stati legati hanno larghezza di circa `1` arco: li' l'inviluppo
   lento e' al limite.**
3. ### **LA CONVENZIONE DELLO ZERO PESA SOLO SULLE FASI RIPORTATE IN `(-pi, pi]`:** ### **seguita con continuita' `D` non cambia** *(`1.0e-12`)*; ### **riportata, scambia i rami
   «come la relativita' generale»** *(a `eps 0`: oggi il basso, nell'alternativa l'alto)*. ### **Quale intero `2 pi k` e' la frequenza a riposo e' una domanda di fisica.**

### **E PER LA SCELTA FRA `S1` E `S4`** *(informazione, non una scelta)*: ### **`S1` ha l'UNICO stato uniforme stabile** *(`x 0.01`, `40` stati su `360`)* ### **ma lega solo a `N 100`**
*(`7` stati legati su `60`)*; ### **`S4` lega da `N 10`** *(`17` su `60`)* ### **e la sua `D` varia con `N` meno di quella di `S3`** *(`eps 0.5, s 0.9`: `-3.80` contro `-3.43` per `S4`,
`-3.70` contro `-2.27` per `S3`)*, ### **ma nessuna delle due ha `D = 0`.**
