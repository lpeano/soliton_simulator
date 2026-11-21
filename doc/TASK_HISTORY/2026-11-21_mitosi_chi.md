# LA MITOSI CON CHI, IN PARALLELO *(il ramo `mitosi-chi`; il mandato unico di Luca `2026-11-21` `19:40`)* [[PROGETTO-MITOSI]]

## 0. IL MANDATO *(copiato)*

**PREMESSE**
- **DECISIONE DI LUCA:** si apre il ramo `mitosi-chi`, che **UNISCE** il codice del ramo `mitosi` *(la crescita del grafo, il campo U generico, le posizioni, il contatore, la regola di nascita: covariante di stella, flip di stella scelto per energia, versori, `E_persa`, P9)* col **tick con `chi`** del ramo `lapse-u` *(`exp(- kappa chi)`, la sorgente `Q` con la forma (a), lo sfondo `c0`, la massa con portata `100`, `c_chi 0.5`)*. **Le due navi madri restano intatte; nulla si riunisce a `primo-ordine` (R-NAVI). Questo mandato autorizza SOLO l'unione nel ramo nuovo.**
- **Le corse in uso NON si toccano:** il tronco e i rami del ramo `mitosi`; la corsa del mattone con `chi` del ramo `lapse-u`. **Al piu' `5` processi in tutto; `1` filo; numba spento; R-AMBIENTE. R-QUALITA' in vigore.**
- **Il motivo** *(dal guardiano)*: con `chi` il contatore ha una coda lunga *(a `r 30` circa il `60%` del massimo, `chi_mattone.txt`)* e il tick costa `0.2` volte quello di C2: **la mitosi guidata da `chi` e' la prova del «vicino ma fuori».**

**IL TRONCO CHI** *(il trucco del `2026-11-20`)*
- **T1.** La corsa del mattone con `chi` del ramo `lapse-u` *(decisione delle `19:28`, fino a `k 20000`)* **NON si ferma a `k 20000`:** dallo stato di `k 20000` **PROSEGUE come TRONCO CHI** con le nascite spente, `Theta` tick per tick *(lo stesso contatore della mitosi, col `cs` da `chi`)*, stati ogni `250` tick con sha1, **fino al primo arco a `2 pi`**; **il limite di sicurezza `k 200000`** *(oltre: FERMO con la proiezione)*. **Lo stato salvato PRIMA dello scatto e' il punto di ramificazione.** Se la corsa fino a `k 20000` e' gia' partita senza `Theta`, il tronco la riprende dal suo ultimo stato e `Theta` parte da li' *(dichiarato)*.
- **T2.** Il referto dell'allungamento a `k 20000` *(oscilla, collassa, si assesta)* **resta come deciso alle `19:28`, prima del resto.**

**IL RAMO `mitosi-chi`** *(il codice, in parallelo al tronco)*
- **R1. L'unione:** il tick con `chi` sul grafo che cresce: **il Laplaciano di `chi` sul grafo nuovo; `chi` e `pi` sul nodo nato con la covariante di stella** *(la media di `i` e `j`)*; **i nodi `k`, `l`, `m` invariati; la variazione di `H_chi` nella nascita e nel flip entra in `E_persa`; la sorgente meno `c0` per nodo** *(`c0` resta la costante per nodo; la somma cambia col nodo nuovo: misurarlo)*; `kappa`, `m`, `c_chi`, `eps_a` come sul ramo `lapse-u`. **Il contatore legge `dtau = mot.dtau x cs` con `cs = s exp(- kappa chi)`.**
- **R2. Le prove** *(coi casi che devono fallire)*: **P6.0** *(senza nascite il ramo = il tick con `chi` del ramo `lapse-u` AL BIT)*; **P1** *(le norme)*; **P3** *(Gauss)*; **P5** *(lo specchio della regola intera con l'energia della corsa, `chi` compreso)*; **P8** *(la ripresa al bit col grafo che cresce e `chi`, `pi`, `Theta` nello stato)*; **P9** *(alla nascita, `H` totale compreso `H_chi`: `H` dopo `-` `H` prima `=` `DH` contato in `E_persa` entro `1e-12 |H|`)*; **una nascita FORZATA nel guscio e una FORZATA a `r 30`** *(fuori dal confine)* come casi noti; **K4 dopo la nascita** *(il fronte di `chi` a un arco per tick sul grafo nuovo)*.
- **R3.** Q-P1: il costo del tick e di una nascita. Commit, push dopo ogni pezzo.
- **R4. La ramificazione:** al primo scatto del tronco `chi`, **due corse in parallelo** dallo stato prima dello scatto: **MITOSI-CHI** *(le nascite accese)* e **CHI-EXT** *(spente)*, **`20000` tick ciascuna**, con le misure del ramo `mitosi` *(D1 i passi, D2-D3 il ritmo e il luogo delle nascite, E1 la scala in passi, la circonferenza e la distanza esterna all'anello `40`, `H + E_persa`)* **e il profilo di `1 - N` per anello. Partono da sole.** Prima di lanciarle, **la prova della ramificazione al bit** *(come `6e51d762`)*.

**PREVISIONI DEL GUARDIANO** *(scritte prima)*
- **P-MC1** Il primo scatto del tronco `chi` arriva fra `k 6e4` e `k 1.5e5`.
- **P-MC2** Il primo arco a scattare sta fra gli anelli `8` e `15` *(il picco del ritmo, che con la contrazione si e' spostato verso l'interno)*.
- **P-MC3** Nei `20000` tick di MITOSI-CHI almeno il `20%` delle nascite sta oltre il confine `23.81` *(contro lo `0%` col lapse `N(rho)`)*.
- **P-MC4** P6.0, P5, P8, P9 passano al bit o alle soglie come sul ramo `mitosi`.

**CRITERI:** ogni numero da un referto committato *(Q-A1)*; casi noti prima *(Q-A4)*; soglie fisse, post-hoc dichiarati.
**FINE DEL MANDATO:** checkpoint *(commit, push)* dopo ogni pezzo; **FERMO PER LUCA solo con un fallimento delle prove R2**; altrimenti i due rami partono al primo scatto e il referto arriva alla loro fine.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di scrivere il codice, e cosa NON so)*

1. **`Theta` C'E' GIA' nella corsa del mattone con `chi`, da `k 0`.** `chi_tick.tick_chi` fa `X["theta_a"] += pi (d_i - d_j)` con `d = mot.dtau * mot.cs` e `mot.cs = s exp(- kappa chi)` di meta' passo; **`contatore.ritmo` del ramo `mitosi` e' la stessa riga** *(`pi (d[nodo[0::2]] - d[nodo[1::2]])`, `d = dtau cs`)* e `Contatore.accumula` fa `theta += r`. **Quindi la clausola «senza `Theta`» di T1 non si applica:** `Theta` parte da `0` a `k 0` di C2 *(`chi_tick.nuovo_X`)*, come il tronco della mitosi. **`max |Theta|` a `k 3000`: `0.2599`** *(`chi_mattone.txt`, `29c13540`)*; `QUANTO = 2 pi` *(`contatore.QUANTO`)*.
2. **I due rami dalla base comune `37e43b3d`:** il ramo `lapse-u` **NON cambia nessun file sotto `csv/`, `primo_ordine/`, `.githooks/`** *(`git diff --stat 37e43b3d lapse-u`: vuoto)*; il ramo `mitosi` ne cambia `17` *(fra cui `primo_ordine/motore.py`, `csv/solitone/contatore.py`, `posizioni.py`, `u1_generico.py`, `primo_ordine/crescita_dati.py`)*. **Quindi l'unione = il nucleo del ramo `mitosi` piu' gli script di `chi` in `doc/referti_l2/`.** ### **Il tick con `chi` NON HA MAI GIRATO sul `motore.py` del ramo `mitosi`:** P6.0 lo confronta con **gli stati salvati della corsa del ramo `lapse-u`** *(`stato_02750` -> `stato_03000`, scritti dal codice dell'altro albero)*: il riferimento piu' forte che c'e'.
3. **`mitosi_regola.applica` da' al nodo nuovo `cs` DALLA LEGGE `N(rho)`** *(`TL.N_di(rho_n, C.legge)`, se `mot.cs` non e' `None`)*: **con `chi` e' sbagliato** *(`cs` viene da `chi`)*. **`mitosi_regola.py`, `mitosi_lunga.py`, `mitosi_rami.py` sono IN USO** *(i due rami della mitosi li hanno importati)* **e NON si toccano:** il codice nuovo sta in un modulo nuovo, `doc/referti_l2/mitosi_chi.py`, che li **importa**.
4. **L'energia della regola:** `mitosi_regola.candidato` calcola `H` col conto della corsa di oggi *(`_libro_dei_conti.conti_per_nodo` + `K + V`, su un `Motore` costruito sul grafo del candidato)*. **Con `chi` l'energia conservata e' quella di `chi_tick.energia_chi`** *(`somma w H` coi pesi di `cs = s N(chi)`, `- e0 somma (N - 1) rho`, `K + V`, `H_chi`)*: **la scelta del flip, `E_persa` e P9 la usano**, calcolata sul motore del candidato, col SUO Laplaciano e il SUO `chi`. ### **NON SO** se `energia_pesata` sul motore del candidato e sul motore vero dopo la crescita danno lo stesso numero entro `1e-12` *(P9 lo dice)*.
5. **Il flip non aggiunge nodi:** `chi`, `pi` su `k`, `l`, `m` restano; cambia il Laplaciano *(l'arco `x - y` diventa `n - m`)*.
6. **Il campo:** il ramo `mitosi` usa `u1_generico.CampoGenerico` *(B3)* al posto del prototipo; **P6.0 del ramo `mitosi` lo ha trovato AL BIT nella dinamica, e `V` entro `8` ulp** *(somma le placchette in un altro ordine)*: le misure di energia possono differire di qualche ulp, lo stato no. **`tick_chi` usa dal campo solo `spinta` e `_u1_oggi.avvolto`**, come il passo di C2.
7. **`Theta` della corsa e il contatore:** `tick_chi` accumula in `X["theta_a"]`; il `Contatore` della mitosi tiene `theta` e lo fa crescere *(`cresci`: i nuovi a `0`, l'arco diviso consumato)*. **Nel ramo `mitosi-chi` sono LO STESSO array** *(dopo ogni crescita si ricollega)*, e **`Contatore.accumula` NON si chiama** *(lo fa gia' il tick)*: si CONTROLLA.
8. **I processi oggi:** la corsa del mattone con `chi`, i due rami della mitosi, l'attesa della proroga *(un processo che aspetta, ma lo conto)*: **`4`.** **Ne resta UNO** per le prove di questo ramo e per l'attesa del tronco `chi`: **non insieme.** ### **NON SO** quando finira' la corsa a `k 20000` *(con i due rami in parallelo il ritmo e' sceso: a `k 3250` `375` s dall'avvio)*.
9. **Il costo:** il tick con `chi` `0.678` s contro `3.407` di C2 *(`chi_prove.txt`)*; una nascita della mitosi `14`-`15` s *(i log dei rami)*; **P5 del ramo `mitosi`: `5` parti da circa `2500` s** *(`mitosi_specchio_v2.txt`)*. ### **NON SO** quanto costa l'energia con `chi` di un candidato.

## 2. LA PROGETTAZIONE *(i passi, cosa decide ciascuno, cosa mi farebbe FERMARE; le soglie fissate QUI)*

### 2.1 IL TRONCO CHI *(T1; il codice sul ramo `lapse-u`, dove gira la corsa)*

- **`chi_tronco.py`** *(ramo `lapse-u`)*: la corsa di `chi_mattone_v2.corsa` riga per riga *(la ripresa da `stato_<k>`, i parametri asseriti al bit, le stesse misure ogni `50` tick)*, **in piu' dopo ogni tick `scattati = |theta_a| >= 2 pi`**: al primo tick con un arco scattato **lo stato DOPO il tick, PRIMA di qualunque regola** *(`prima_nascita_<k>.npz`, `scatto.json`: `k`, gli archi, lo sha1)* **e l'uscita `10`** *(come `mitosi_rami.ciclo` modo `tronco`)*. **Gli stati in `E:/soliton_simulator/controllo/CHI/tronco/`** *(la cartella della corsa a `k 20000` non si tocca)*; le serie continuano da quelle di `k 20000`. **Il limite `k 200000`:** uscita `0` senza scatto -> FERMO con la proiezione *(la riga del ritmo di `mitosi_ritmo_contatore.py`, sullo stesso `Theta`)*.
- **La prova del tronco, PRIMA:** **DEVE** la ripresa da `stato_02750` a `k 3000` AL BIT con `stato_03000` *(come `chi_mattone_v2 prova`: lo stesso cammino)*; **DEVE** uno scatto FORZATO *(`theta_a` di un arco portato a `2 pi` dopo il tick `k 2760`, solo nella prova)* -> l'uscita `10` a `k 2760`, `scatto.json` con quell'arco, lo stato salvato = lo stato della corsa a `k 2760` AL BIT; **DEVE FALLIRE:** senza lo scatto forzato nessuna uscita `10` fino a `k 2770`.
- **Il lancio:** un lanciatore NUOVO *(`chi_lancia_tronco.sh`)* che **aspetta l'uscita del lanciatore in corso** *(`mitosi_attendi.py attendi`, il processo Windows)*, poi **decide dai file**: la voce `chi-mattone-lungo` chiusa e `stato_20000` integro -> il tronco; altrimenti niente, e lo scrive. **Lo lancio solo quando i processi lo permettono** *(premessa 8)*; **se la corsa a `k 20000` finisce prima, il tronco lo lancio io, a mano, con lo stesso lanciatore** *(dichiarato nel registro)*. **Al primo scatto il lanciatore chiama `bash` del lanciatore dei rami del ramo `mitosi-chi`** *(R4)*.

### 2.2 L'UNIONE *(R1; il ramo `mitosi-chi`)*

- **`git merge lapse-u`** nel ramo `mitosi-chi` *(dopo il commit di `chi_tronco.py` sul ramo `lapse-u`, cosi' il ramo nuovo ne ha la copia; lo sha1 dei byte si CONTROLLA uguale)*. **I conflitti** *(attesi solo in `RELAZIONE_PER_CLAUDE.md`, `doc/REGISTRO_CORSE.md`, l'indice)*: **si tengono entrambe le parti**, nell'ordine dei tempi.
- **`doc/referti_l2/mitosi_chi.py`** *(NUOVO; importa `mitosi_regola`, `mitosi_lunga`, `mitosi_rami`, `chi_tick`, `chi_mattone_v2` senza toccarli)*:
  1. **`Campo chi`:** `X = {chi, pi, theta_a}`, il Laplaciano *(`chi_tick.Laplaciano(mot)`, RICOSTRUITO dopo ogni crescita)*, i parametri *(`chi_tick.parametri`, asseriti al bit su quelli del `meta`)*;
  2. **il passo:** il passo di `chi_mattone_v2` *(`campo` = `CampoGenerico`)*; **`Theta` = `X["theta_a"]` = `cont.theta`** *(premessa 7)*;
  3. **`candidato_chi`:** `mitosi_regola.candidato` *(il grafo, `psi`, `phi`, i versori, il campo, il motore del candidato: le righe della mitosi)*, **poi `H` = `energia_chi` sul motore del candidato** *(`chi`, `pi` del candidato: i vecchi, piu' sul nodo `n` la media di `i` e `j`; il Laplaciano del grafo del candidato)*; **`regola_chi`:** la scelta (A) di `mitosi_regola.regola` con questa `H` *(la stessa `GUARDIA`)*;
  4. **`applica_chi`:** `mitosi_regola.applica` con `mot.cs` messo a `None` per la durata *(cosi' NON calcola `cs` dalla legge `N(rho)`)*, poi **`mot.cs` = quello di prima con in coda `s exp(- kappa chi_n)`**; `X["chi"]`, `X["pi"]` col nodo nuovo; `X["theta_a"]` = `cont.theta`; **il Laplaciano ricostruito**;
  5. **la nascita** *(`Rami.nasci` riga per riga, con `energia_chi` al posto di `energia_corsa`)*: `DH`, `E_persa -= H1 - H0`, **P9 a ogni nascita** *(`|H1 - H_candidato| <= 1e-12 |H|`, altrimenti FERMO)*, `gauss_acc`, il luogo; **in piu' `DH_chi`** *(la variazione di `H_chi`)* **e `D somma c0`** *(`= c0`, un nodo in piu': misurato)*;
  6. **salva/riprendi:** lo stato del ramo `mitosi` *(`mitosi_lunga.salva`: il grafo dopo la prima nascita)* **piu' `chi`, `pi`** *(`theta_a` c'e' gia')* e `gauss_acc`; la ripresa: `mitosi_lunga.riprendi` *(il grafo)* **piu' `chi`, `pi`**; **dallo stato del tronco `chi`** *(senza grafo, senza `E_persa`)*: `controllo_senza_bordo.riprendi` + `campo_generico` + `Contatore(theta_a)`;
  7. **il ciclo** *(`mitosi_rami.ciclo` riga per riga)*: i modi `mitosi` *(MITOSI-CHI)* e `ext` *(CHI-EXT)*; le misure del ramo `mitosi` *(D1, E1, `gauss_acc`, `E_persa`, i bilanci delle nascite)* **piu' quelle di `chi`** *(il picco, `H`, `H_chi`, la media di `chi`, `1 - N` e il ritmo per anello, `max |Theta|`)*.

### 2.3 LE PROVE *(R2, R3; le soglie fissate QUI)*

| prova | che cosa | DEVE | DEVE FALLIRE |
|---|---|---|---|
| **P6.0** | il passo del ramo *(CHI-EXT, `CampoGenerico`)* da `stato_02750` della corsa `lapse-u` a `k 3000` | lo stato a `k 3000` *(ogni array, `chi`, `pi`, `theta_a`)* **AL BIT** con `stato_03000`; le misure **AL BIT**, salvo `E` e `H` **entro `8` ulp relativi** *(premessa 6)* | `E` di un arco spostato di `1` ulp alla ripresa: lo stato a `k 3000` DIVERSO |
| **P1** | la nascita FORZATA *(nel guscio)* | `M` e `V` entro `1e-12` relativo | senza il fattore di stella: fuori da `1e-12` |
| **P3** | la stessa | il residuo di Gauss dopo sotto `10` volte quello di prima | gli archi nuovi con `E = 0` senza Gauss: sopra `10` volte |
| **P9** | la stessa, e ogni nascita della corsa | `H` riletta *(`energia_chi` sul motore vero)* `=` `H_candidato` entro `1e-12 |H|`; `E_persa = - DH` | `H` del candidato SENZA `H_chi`: fuori da `1e-12` |
| **i casi noti** | la nascita FORZATA nel guscio *(l'arco a `r` fra `17` e `20` piu' vicino a `18.9`, il luogo della prima nascita della mitosi)* e a `r 30` *(l'arco a `r` piu' vicino a `30`)*, dallo stato `k 3000` della corsa con `chi` | P1, P3, P9 come sopra; **stampati:** `DH_nascita`, `DH_flip`, `DH_chi`, `D somma c0`, il lato scelto | — |
| **K4 dopo la nascita** | l'impulso `chi = 1` sul nodo NATO *(la riga di K4 di `chi_prove.py`, sul Laplaciano del grafo nuovo)* | per `t = 1..30` `chi = 0` esatto oltre `t` passi e non zero a `t` | lo stesso sul Laplaciano del grafo VECCHIO col nodo nuovo isolato: il fronte NON parte |
| **P8** | `10` tick con la nascita forzata al primo, di fila, contro `5` + salva + riprendi + `5` | ogni chiave, `A`, `E`, il grafo, i versori, `Theta`, le posizioni, `E_persa`, **`chi`, `pi`**, `gauss_acc` AL BIT | un byte dello stato salvato cambiato: la ripresa RIFIUTA *(lo sha1)* |
| **P5** | la regola intera sull'arco e sull'immagine nello stato specchiato *(a `30` gradi, la permutazione di `mitosi_specchio_v2`, **piu' `chi`, `pi` permutati**)*, i primi `200` archi nell'ordine di scatto | le soglie di `mitosi_specchio_v2` *(`1e-14`; `E` `1e-10`; `H` `1e-12` relativo)* | il flip col VERSO: scarti sopra `1e-6` o un lato diverso |
| **Q-P1** | il tempo del tick *(prima e dopo una nascita)* e di una nascita | stampato | — |
| **R4** | la ramificazione *(come `6e51d762`)*: lo scatto FORZATO; il tronco `chi` *(la copia di `chi_tronco.py`)* -> `prima_nascita`; i due rami contro le corse continue | R1 MITOSI-CHI = la continua accesa AL BIT; R2 CHI-EXT = la continua spenta AL BIT; R3 la ripresa dopo una nascita AL BIT | MITOSI-CHI senza la nascita iniziale: DIVERSO |

- **P-MC4 VERA** se P6.0, P5, P8, P9 passano come scritto qui.
- ### **SE UNA PROVA DI R2 FALLISCE: FERMO PER LUCA** *(il mandato)*.

### 2.4 LE DEFINIZIONI DELLE PREVISIONI *(mie, fissate qui)*

- **P-MC1:** `k` dello scatto *(`scatto.json` del tronco `chi`)* fra `60000` e `150000` compresi.
- **P-MC2:** **l'anello del primo arco** = `round(r)` del punto medio dei suoi due nodi dal centro delle misure *(`meta["centro"]`, quello della corsa)*: fra `8` e `15` compresi.
- **P-MC3:** **il confine `23.81`:** le nascite di MITOSI-CHI con `r` *(il raggio del nodo nuovo dal centro, il campo `r` dei bilanci)* `> 23.81`, sul totale delle nascite dei `20000` tick: `>= 0.20`.

## 3. TODO DEL NEXT STEP

1. questa carta: commit, push; la riga nella relazione *(questo ramo e `primo-ordine`)*;
2. **ramo `lapse-u`:** la sez. `14` della sua carta *(T1, T2: il rimando a questa)*; `chi_tronco.py`, `chi_lancia_tronco.sh`: commit; la prova del tronco: il referto, commit;
3. **ramo `mitosi-chi`:** `git merge lapse-u`: commit; lo sha1 di `chi_tronco.py` controllato;
4. `mitosi_chi.py` *(R1)*: commit; **P6.0**: il referto, commit;
5. la nascita FORZATA nel guscio e a `r 30` *(P1, P3, P9, i casi noti, K4, Q-P1)*: il referto, commit;
6. **P8**: il referto, commit; **P5**: il referto, commit;
7. **R4:** la prova della ramificazione; il lanciatore dei rami: commit;
8. alla fine della corsa a `k 20000`: **T2, il referto dell'allungamento, PER PRIMO** *(commit, push)*; poi il tronco `chi`. **Il FERMO delle `19:28` non ferma questo mandato:** per PRECEDENZA-IN-CODA vale l'ultimo *(`19:40`)*, che fa FERMO solo su un fallimento di R2 *(dichiarato)*;
9. al primo scatto i due rami partono da soli; **il referto alla loro fine.**
