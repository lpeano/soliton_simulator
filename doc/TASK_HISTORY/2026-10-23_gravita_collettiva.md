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

## 5. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_gravita_collettiva.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima di ogni numero;
3. la corsa, il referto `doc/referti_l2/gravita_collettiva.txt` e `.jsonl`, la relazione, e la sezione `6` qui sotto.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*
