# [M1623] LE 538 NASCITE DI MITOSI-v2: LA LETTURA *(i numeri da `nascite_538.txt`, `nascite_lettura.py` sha1 dei byte `ec1571ea`, la corsa di lettura `16:42:21`-`16:42:33` da `date`; la carta `doc/CARTA_nascite_lettura.md`)* [[PROGETTO-MITOSI]]

> **Solo lettura** dai file sul disco *(`E:/soliton_simulator/controllo/mitosi_rami/`, gli stati con lo sha1)*. ### **«Prima» e «dopo» una nascita hanno la risoluzione dei dati** *(`50` tick la norma, `250` Theta e il grafo)*: **leggerli al tick vorrebbe una corsa, che il mandato esclude.** **K3 e la parte «scende» di K4 sono garantite dal codice** *(la carta sez. `2`)*.

## I CRITERI

| | il criterio | l'esito |
|---|---|---|
| **K1** | le prime 9 contro M1-M3; la norma fuori dalle nascite | **PASSA** *(4 DEVE su 4)*: gli angoli **al bit** con `coppie_57.angolo_e_r` *(una funzione mia, scarto `0.000e+00`)*; il massimo dall'asse `7.79` gradi; `8` cinque e `8` sette, tutti legati; **`|dM/M|` senza nascite al massimo `3.3e-16`** |
| **K2** *(S13)* | IMPRONTA se `> 0.9` con `p < 1e-4`; si sfuma se `< 0.7` | ### **SI SFUMA:** sull'asse *(entro `10` gradi)* **`190` su `538` = `0.353`**; il nullo uniforme `1/3` *(`p = 0.18`)*; **i nodi dell'anello `0.338`** *(`902` nodi, `p = 0.24`)*. **Per tempo:** le nascite `1-100` **`0.78`**, `101-300` `0.30`, `301-538` **`0.22`**; le prime 9 restano `1.00` nello stato finale |
| **K3** *(Z3)* | CONSERVATA se `< 1e-10` | **CONSERVATA:** `|dM/M|` negli intervalli di `50` tick con nascite al massimo **`8.9e-16`** *(`184` intervalli, `538` nascite)*; `phi` `8.9e-16`. ### **E' il codice** *(`_fattore` riscala la norma della stella)*: **conferma che il codice fa quello che dice, non che la fisica conservi** |
| **K4** *(B1, Z4)* | CHIUDE se genitore+nato `< 0.5 x` e i vicini a 1 passo `<= +20%` | **CHIUDE:** genitore+nato `21.17 -> 9.01` *(`0.425`; diviso il controllo `0.423`)*; **i vicini a 1 passo `0.957`** *(diviso il controllo `0.952`)*, a 2 passi `0.984`; il controllo `1.006`. ### **Ma lo scendere del genitore+nato e' garantito** *(gli archi nuovi da `Theta = 0`, l'arco che scatta consumato)*, **e anche una parte del calo dei vicini lo e'** *(l'arco girato dal flip e' fra due vicini: nasce a `0`)* |
| **K5** *(N3)* | il ritmo col fit dichiarato | ### **RALLENTA:** per `1000` tick `69, 69, 75, 54, 52, 51, 51, 42, 36, 39`; il costante AIC `-3210.2` *(chi2 `29.8` su `9`)*; **il lineare `-3234.0`** *(`b = -4.05 +- 0.79` per finestra, `-5.1 sigma`; chi2 `3.9` su `8`)*; **l'esponenziale `-3234.0`** *(`c = -0.077 +- 0.015`, `-5.0 sigma`)*: lineare ed esponenziale indistinguibili, **tutti e due in calo a 5 sigma** |

## LE LETTURE IN PIU' *(le definizioni nella carta; i numeri dal referto)*

- ### **LE NASCITE SI TOCCANO:** di `537` nascite *(dalla seconda)*, **l'`83%` e' a 1 passo dalla nascita precedente piu' vicina**, il `96%` entro 2, il `98.7%` entro 3 *(la mediana 1, il massimo 38)*; **il tempo dalla precedente: la mediana `12` tick** *(il 10% `2`, il 90% `44`)*. **La mia lettura** *(dopo i numeri)*: **la nascita non spinge Theta sui vicini** *(K4)*, **ma i vicini sono GIA' maturi**: l'anello matura insieme e le nascite scorrono lungo di lui come un fronte. **B1 «Theta scende e non si sposta» e' vero per la nascita; non dice che lo spazio smetta di nascere li' accanto.**
- **La coppia** *(i gradi dei sei nodi nello stato dopo)*: **«5-7» in `506` su `538`**, «altro» `32`.
- **Dove (N6):** **tutte e `538` nel guscio** *(`r` registrato da `16.6` a `22.0`, la mediana `19.8`; i passi dalla sorgente da `18` a `26`)*; **nessuna nel cuore, nessuna fuori.** Nel profilo dello stato finale **`rho` ha il massimo a `r 17`** *(`456.6`)* e alle nascite *(`r 18-21`)* scende da `447` a `308`; **`|phi - phi0|^2` ha il minimo proprio li'** *(`0.17`-`0.18` a `r 19-21`, contro `~1` nel cuore e lontano)*. **Le nascite stanno sul fianco esterno del mattone, dove `phi` e' piu' vicino al valore lontano** *(il fatto; il perche' non lo so)*.
- **L'energia NON e' conservata:** `DH` per nascita la media **`-21.29`** *(da `-57.8` a `-2.5`)*; **la somma `-1.1455e+04` = `E_persa`.** **C5 del progetto dei vincoli** *(«lo spazio nasce perche' l'energia non puo' sparire»)* **nel codice di oggi e' il contrario: la norma e' conservata per costruzione, l'energia sparisce a ogni nascita.** `P9` `0` in tutte, il residuo di Gauss `<= 2.8e-14`, F3 vero `538` su `538`.
- **I nodi** *(N3)*: da `34596` a `35134`; la crescita segue le nascite, che **rallentano**.

## LE PREVISIONI, CONTRO I NUMERI

| | la previsione | l'esito |
|---|---|---|
| **P1** | K1 passa `85%` | **SI'** |
| **P2** | IMPRONTA DEL FAVO `75%` | **NO: SI SFUMA** *(`0.353`; l'impronta era delle prime `100`)* |
| **P3** | CONSERVATA `55%` | **SI'** *(dal codice)* |
| **P4** | CHIUDE `50%`; SI SPOSTA `35%`; RESTA `15%` | **CHIUDE** *(col criterio del mandato; le nascite pero' si toccano: `83%` a 1 passo)* |
| **P5** | ACCELERA `55%`; costante `30%` | **NO: RALLENTA** *(`-5 sigma`)* |
| **P6** | il guscio `> 70%` `60%` | **SI'** *(`100%`)* |
| **mie** | K3 `90%`; genitore+nato scende `90%`; i vicini salgono oltre il `20%` `60%`; IMPRONTA `40%`; il guscio `95%`; ACCELERA `50%` | si'; si'; **no** *(`0.957`)*; no; si'; **no** |

## PER LA SAGOMA

- ### **S13 CADE su 538:** «le nascite cadono sugli assi del favo» vale per le prime `100` *(`0.78`)* e **non per le `538`** *(`0.353` contro `0.338` del nullo, `p = 0.24`)*. **Le coppie 5-7 legate restano** *(`506` su `538`)*.
- **Le righe nuove possibili** *(la decisione e' di Luca)*: **il ritmo delle nascite rallenta** *(`69 -> 39` per `1000` tick, `5 sigma`)*; **le nascite si toccano** *(`83%` a 1 passo, la mediana `12` tick)*; **la nascita conserva la norma per costruzione e perde energia** *(`-21.3` per nascita)*.
