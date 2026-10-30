# 2026-10-29 — LA STRADA (B): IL LATO `r > 1`, LA SPALLA DI `r 0.65`, LE CORSE ANCHE SENZA STATO FERMO ESATTO *(UNA DIAGNOSI IN `csv/`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `22:25`, dopo `af1758fd` e `4effe55a`)*

> **LIVELLO:** i pesi del tick cambiati IN MEMORIA *(`_strada_b_r.pesi`, gia' controllato al bit a `r 1` in `af1758fd`)*; un conto per anello, Newton, tre corse brevi, una corsa lunga a pezzi; nessun file del nucleo.
> **I nomi:** `a_n`, `b_a` i pesi del nodo e dell'arco per unita' di tempo; `r = b_a/a_n`; `alpha(x)` il legame di `S1`; le frequenze sono **energie per unita' di tempo**, `-arg(lambda)/s`, come `mu`.

## 1. LE PREMESSE DAL CODICE

### Da `af1758fd` *(`doc/referti_l2/strada_b_r.txt`)*

| | `r 1` | `r 0.65` | `r 0.69` |
|---|---|---|---|
| `P0` libera, `(b_a - a_n)/2` | `0` | `-0.625516` | `-0.549215` |
| `Ppi` libera, `-(a_n + b_a)/2` | `-pi` | `-2.948863` | `-2.994110` |
| `mu` | `-0.566022365` *(fermo)* | `-0.568753654` *(NON fermo, `5.757e-06`)* | `-0.568233828` *(NON fermo, `1.262e-06`)* |
| il profilo, anelli `14`-`17` *(rho per nodo)* | `1.32`, `0.087`, `0.0035`, `1.2e-04` | `1.48`, `1.25`, `0.70`, `0.097` | `0.52`, `0.039`, `1.3e-03`, `4.1e-05` |

- **(v1) e (v2) NON valgono come vincoli su `b_a/a_n`** *(`af1758fd`, il punto 0)*: **l'errore `n.82` del guardiano** *(la finestra `r 0.62`-`0.69` e l'esclusione di `r > 1` costruite su di essi)* va nella sezione `8` della MAPPA.

### Il legame non dipende da `r` *(dal codice)*

- `flussi_parziali.z_nodo` e `z_arco` sono chiamati **solo** da `grover`, `hop_psi`, `hop_phi` e dalla convenzione `simm`: **il legame non passa di li'**. Il legame e' `exp(-i alpha(rho/Lambda) dtau f)`, uno scalare per nodo uguale sulle `12` componenti *(`6c720842`)*: sposta ogni banda di `+alpha` per unita' di tempo, **a ogni `r`**.
- **Le frequenze locali per anello:** `P0 + alpha`, `Ppi + alpha` contro `mu`; la coppia `(P0 + alpha) + (Ppi + alpha) - 2 mu = 2 alpha - a_n - 2 mu`.

### Sulla carta, prima dei numeri *(le formule, non i valori)*

- **c1 su `P0`** si annulla dove `alpha = mu - P0 = mu + (a_n - b_a)/2`: possibile solo se `P0 < mu` *(`alpha >= 0`)*, cioe' a `r < 1` con lo spostamento abbastanza grande. A `r 0.65` serve `alpha ~ mu - P0`; a `r 0.69` e a `r > 1` `P0 > mu`: **nessun incrocio di c1 su `P0`**.
- **c1 su `Ppi`:** `Ppi + alpha <= -(a_n + b_a)/2 + 1`, e ai tre `r` del mandato `a_n + b_a` e' `5.90`, `5.99`, `5.91` *(`af1758fd`, `b5fd8ecc`)*: `Ppi + alpha <= -1.9 < mu`, nessun incrocio.
- **⚠ LA COPPIA:** `2 alpha - a_n - 2 mu` si annulla dove `alpha = (a_n + 2 mu)/2`. **A `r > 1`** *(`a_n < pi`)* nel cuore *(`alpha ~ 1`)* vale `2 - a_n - 2 mu`, che con `mu` vicino a `-0.57` **e' positiva**, e nella coda *(`alpha -> 0`)* vale `-a_n - 2 mu < 0`: **la condizione della coppia si annulla in un anello della coda.** **Quindi il lato `r > 1` non ha l'incrocio di c1, ma ha quello della coppia:** la motivazione del mandato *(«il lato `r > 1` non ha questo incrocio»)* vale **per una piatta**, non per la coppia. A `r < 1` la coppia e' negativa nel cuore e nella coda: nessun incrocio. Il punto `1` lo misura.

### Altro

- `eps = 0` in tutte le scene di `S1`; il congelato vero *(`_congelato_lungo.avanza`)*; `s 0.15`, `L 81`, `N 1e6`.
- **La partenza di Newton a `r 1.5247`:** lo stato fermo a `r 1` di `dfb5ab7e`, come a `r < 1`. Lo spostamento libero e' `+0.806` *(`b5fd8ecc`)*, quasi il doppio di quello di `r 0.65`, e di segno opposto: **non so se Newton converge**.
- **La deriva di uno stato non fermo:** dal residuo per tick, `|D|` puo' crescere al piu' di `residuo/s` per unita' di tempo *(Luca)*: a `r 0.65` `5.757e-06/0.15`, a `r 0.69` `1.262e-06/0.15`. Il modo instabile a `r 1` cresce col tasso `0.151` *(`dfb5ab7e`)*.
- La corsa di riferimento *(il cuore `0.630 -> 0.454`)* e' a **`s 0.3`** *(`26300537`)*; questa a `s 0.15`: due `s`, dichiarato.

### Cosa NON so

- se la spalla di `r 0.65` sta dove c1 si incrocia *(il profilo di `r 0.65` alza `alpha` proprio negli anelli della spalla: il conto usa l'`alpha` del profilo di ogni `r`)*;
- se Newton converge a `r 1.5247`;
- la forma della crescita di `D` da stati non fermi.

## 2. I CRITERI

- **Lo script** `csv/_strada_b_lati.py`; importa da `csv/_strada_b_r.py` i pesi in memoria, la scena e **Newton** *(`_strada_b_r.cerca`, il metodo di `26300537`: residuo `< 1e-9`, al piu' `30` passi; invariato)*. **I file di `r 1.5247` si chiamano `r1.52`** *(il nome di `_strada_b_r.nome_r`)*; il `.json` porta `r` intero.
- **(1) `--referto`, il conto c1 per anello** *(nessuna corsa)*, a `r` `0.65`, `0.69`, `1.5247`:
  - il profilo: lo stato di Newton migliore a `0.65` e `0.69`; **lo stato a `r 1` di `dfb5ab7e` per `1.5247`**, dichiarato, con `mu` = il quoziente di Rayleigh di quello stato col tick coi pesi di `1.5247`; **in piu', dichiarato come aggiunta:** lo stesso conto con lo stato di Newton del punto `2`, se c'e';
  - le piatte **misurate** dal tick libero coi pesi *(la media sulla zona dei gruppi `P0`, `Ppi`)*, **DEVE**: piatte entro `1e-9` e uguali alla formula entro `1e-9`;
  - per anello *(`floor` della distanza dal baricentro di `rho`, come `6c720842`)*: `rho` per nodo, `alpha` medio *(`SF.pezzi_di(forma)(rho, lam)[0]`)*, `P0 + alpha - mu`, `Ppi + alpha - mu`, la coppia `(P0 + alpha) + (Ppi + alpha) - 2 mu`; **gli incroci** = un cambio di segno fra l'anello `k` e `k+1`;
  - **la lettura della spalla:** la spalla e' **quella di Luca, gli anelli `14`-`17`** *(dal referto di `af1758fd`)*; **`(s1)` se un incrocio di c1 su `P0` a `r 0.65` cade fra gli anelli `k`, `k+1` con `k` in `13`..`16`** *(l'incrocio dentro la spalla o sul suo bordo interno)*; **`(s2)` altrimenti**.
- **(2) `--cerca 1.5247`** = `_strada_b_r.cerca`; il `.json` in `doc/referti_l2/strada_b/` **committato subito**. Nel referto: il tick libero *(le piatte, `A(K)`, la coppia a `K`, la curvatura di `A` a `K` contro `r 1`; **DEVE** il tick coi pesi = quello ricomposto entro `1e-10`)*; lo stato: `mu`, `w/w_in`, il cuore, il picco, il profilo, lo scarto nel cuore `2 - a_n - 2 mu`.
- **(3) `--forma R`**, `R` in `0.65`, `0.69`, `1.5247`: `180` unita' di tempo dallo stato di Newton **anche non fermo** *(dichiarato col suo residuo)*; `D(t) = e^{i mu s t} psi(t) - psi0`; **`|D|/|psi0|` ogni `3` unita' di tempo da `3` a `180`**. **DEVE:** `M` entro `1e-10`.
  - **LA FORMA, scritta prima:** sui campioni con `|D|/|psi0| < 1e-2` *(la saturazione di `dfb5ab7e`)*, due adattamenti ai minimi quadrati, **giudicati nella stessa misura** *(lo scarto quadratico medio di `ln(|D|/fit)`)*: **(L)** `|D| = c + v t`; **(E)** `ln|D| = a + gamma t`. **Esponenziale se (E) ha lo scarto minore, lineare altrimenti.** Stampati accanto: `v` contro **la pendenza attesa `residuo/s`**; `gamma`; la pendenza locale `d ln|D|/dt` a ogni campione accanto a `1/t` *(una crescita lineare da zero ha `1/t`, una esponenziale una costante)*.
  - **se esponenziale:** il tasso nella finestra di `dfb5ab7e` *(fit di `ln|D|` fra `10 x residuo` e `1e-2`, la deroga di `6c720842`)*, se ha `>= 3` campioni;
  - **le bande e gli anelli di `D`** *(come `_filtro_bande_piatte.esame`: i `3` anelli maggiori, i pesi per gruppo dagli autovettori del tick libero coi pesi)* **a `90` e a `180`** unita' di tempo.
- **(4) `--lunga`**: lo script sceglie dai `.json` del punto `3`: **`r 1.5247` se la sua forma non e' esponenziale; altrimenti `r 0.69` se la sua non lo e'; altrimenti nessuna.** `20000` tick a pezzi di `2000`, ogni `10` tick `_congelato_lungo.punto` *(la larghezza, il cuore, l'alone, il picco)*; ogni pezzo riparte dallo stato salvato *(lo sha1 della fine del pezzo prima, al bit)*; ogni pezzo committato. Nel referto: finestre di `500` unita' di tempo contro la corsa a `r 1` di `26300537` *(`s 0.3`)* allo stesso tempo. **DEVE:** `M` entro `1e-10` relativo.

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **a `r 1.5247`:** `(c1)` nessuna crescita esponenziale e il cuore regge nella corsa lunga: la strada (B) con `r > 1` cura `S1`; `(c2)` nessuna crescita esponenziale ma il cuore si svuota: un'altra causa *(dove va `D`)*; `(c3)` crescita esponenziale: lo scarto nel solitone non e' quello libero *(di quanto)*, o un'altra risonanza *(quale, dal conto del punto `1`)*; `(c4)` altro.
- **a `r 0.65`:** `(s1)` la spalla e' la risonanza c1 del punto `1`; `(s2)` no.
- **a `r 0.69`:** come `(c1)`-`(c4)`.

## 4. LE MOTIVAZIONI

- Dal lato `r < 1` lo spostamento che spegne la coppia *(`<= -0.4`)* porta `P0` sotto `mu` e apre la risonanza di una piatta *(l'ipotesi del punto `1`)*; il lato `r > 1` non ha questo incrocio *(Luca)*. **Il guardiano aggiunge, dalla formula:** a `r > 1` si apre l'incrocio della coppia nella coda *(sezione `1`)*.

## 5. TODO

1. questo file, DA SOLO, e aspettare il push;
2. `csv/_strada_b_lati.py`, la voce d'inventario, commit;
3. `--cerca 1.5247` *(in fondo)*; intanto `--forma 0.69` e `--forma 0.65`; ogni `.json` committato appena scritto;
4. `--forma 1.5247`, commit;
5. `--lunga` pezzo per pezzo, ogni pezzo committato;
6. `--referto` -> `doc/referti_l2/strada_b_lati.txt`; RELAZIONE; MAPPA *(la riga `d` della sezione `3`; l'errore `n.82` nella sezione `8`)*; questo file annotato; commit.

## 6. ANNOTAZIONE DOPO IL REFERTO *(`doc/referti_l2/strada_b_lati.txt`; lo script `sha1-BYTE 0011b1ac`, `b9e3c565`; `15/15`)*

| | `r 0.65` | `r 0.69` | `r 1.5247` |
|---|---|---|---|
| lo stato | NON fermo, `5.757e-06` | NON fermo, `1.262e-06` | **fermo: Newton in `16` passi, `1.686e-10`**, `mu -0.568613109` |
| il conto c1 *(punto `1`)* | **c1 su `P0` fra gli anelli `14`-`15`**; c1 su `P0` `+0.001`, `-0.009`, `-0.030`, `-0.054` agli anelli `14`-`17` *(fuori `-0.057`)* | nessun incrocio *(c1 su `P0` `+0.019` fuori)* | **la coppia fra gli anelli `13`-`14`** *(col profilo di `r 1` e col proprio)*; c1 nessuno |
| la corsa breve, `D` a `180` | `1.18e-02` | `1.51e-03` | `1.97e-07` |
| la forma | **la regola dice ESPONENZIALE per un artefatto:** il fit lineare ha intercetta negativa, il suo scarto in `ln` e' `inf`; l'esponenziale ha scarto `0.357`; **la pendenza locale scende** *(`0.070` a `15`, `0.0077` a `180`)*: **sopra-lineare, non esponenziale** | **lineare**, `v` = `0.998` della pendenza attesa | **lineare**, `v` = `0.977` della pendenza attesa |
| dove sta `D` *(a `90`, `180`)* | **`P0` `0.861`, `0.926`; anelli `14`-`15`** | banda `A` `1.000`; anelli `3`-`6` | banda `A` `0.999`; anelli `4`-`7` |
| il tasso piu' piccolo che la corsa breve vede *(`ln(D_180/residuo)/180`)* | `0.042` | `0.039` | `0.039` |

**La corsa lunga** *(`r 1.5247`, la sua forma lineare; `20000` tick, `M` entro `5.4e-12`)*:

| `tau` | il cuore `f_win` | `w/w_in` | `r 1` *(`26300537`, `s 0.3`)*: il cuore |
|---|---|---|---|
| `0` -> `500` | `0.66280` -> `0.66280` *(pendenza `-2.7e-11`)* | `0.92412` -> `0.92412` | `0.630` -> `0.584` |
| `500` -> `1000` | -> `0.58384` | -> `1.01747` | -> `0.522` |
| `1000` -> `2000` | -> `0.53960` | -> `1.10005` | -> `0.466` |
| `2000` -> `3000` | -> `0.51006` | -> `1.15207` | -> `0.454` |

| la lettura | l'esito |
|---|---|
| `r 1.5247` | **alla lettera `(c2)`:** nessuna crescita esponenziale nella corsa breve, e il cuore si svuota nella lunga. **Ma la corsa breve non vede un tasso sotto `0.039`** *(la deriva lineare del residuo copre `D`)*: **un modo lento, partito da `~1e-10`, darebbe proprio un cuore fermo per `500` e poi in caduta.** **`(c2)` e un `(c3)` lento NON SI SEPARANO con questi dati.** Il candidato dal punto `1`: **la coppia nella coda, anelli `13`-`14`.** Rispetto a `r 1`: il cuore regge `500` unita' di tempo invece di cadere subito, e a `3000` e' `0.510` contro `0.454` *(due `s`)* |
| `r 0.65` | **`(s1)`:** l'incrocio di c1 su `P0` sta nella spalla *(`14`-`15`)*, c1 vi e' quasi zero su `4` anelli, e la crescita di `D` sta per l'`86`-`93%` in `P0` negli anelli `14`-`15` |
| `r 0.69` | nessuna crescita esponenziale sopra `0.039` in `180`; `D` e' la deriva dello stato non fermo, in `A`. **La corsa lunga non era sua** *(la scelta del mandato: `r 1.5247` prima)*: **`(c1)`-`(c4)` non si decidono** |

- **Il mio errore:** il secondo pezzo della corsa lunga e' caduto su `os.replace` *(`np.load` teneva aperto il `.npz`, su Windows)*; lo stato ripristinato dal `_tmp` dopo il controllo dello sha1, la correzione in `b9e3c565`. **Lo stesso difetto e' in `csv/_strada_b_r.corsa`**, mai partita: non toccato.
- **La regola della forma ha un buco:** un fit lineare con intercetta negativa la fa pendere verso l'esponenziale. Dichiarato, non corretto dopo i numeri.
- **Dichiarato:** prima del commit dello script ho girato `--referto` una volta come prova *(non scrive file)*: il conto per anello l'ho visto prima del commit, a criteri gia' committati.
