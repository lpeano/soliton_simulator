# 2026-10-31 — IL SOLITONE SU `B` A `Gamma`: LA SCELTA DENTRO LA COPPIA E LA CORSA LUNGA ANCHE SENZA STATO FERMO *(UNA PROVA IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `13:52`, sull'esito di `ab7226e7`)*

> **Lo script:** `csv/_coppia_di_B.py` *(importa `_massimo_di_B`: la scena a `eps`, la partenza, Newton)*. **I dati:** `doc/referti_l2/coppia_di_B/`; gli stati in `db/coppia_di_B/` *(ignorato: il dato E' il comando)*. **Il referto:** `doc/referti_l2/coppia_di_B.txt`.

## 1. LE PREMESSE DAL CODICE

### Da `ab7226e7`

- Newton non converge sul massimo di `B` a `Gamma` *(`eps 0.5`: `2.4e-3`, ristagna; `eps 0`: `3.0e-4`, fermo dal passo `13`)*; lo stato migliore resta STRETTO *(`w 6.44`, `6.65`; partenza `6.64`)* con `mu - E0 +0.994`; al `mu` misurato tutte le uscite chiuse *(la minima (c1) `B + B` a `0.988`)*.
- **Il guardiano:** non e' (b3) *(un non legato si allargherebbe)*; **il sospetto e' il metodo:** la coppia di `Gamma` e' DOPPIA e lo stato parte dalla prima colonna QR, arbitraria.

### Dal codice *(letto in questa sessione)*

- **La coppia:** `_massimo_di_B.bloch_B` prende `A(Gamma)` della scena *(`DV.matrice`, a quell'`eps`)*, `eig`, i due livelli piu' alti, **`Q = qr(V[:, top])`**: ### **`q1 = Q[:, 0]`, `q2 = Q[:, 1]`.** La famiglia: `q(theta, phi) = cos(theta) q1 + e^{i phi} sin(theta) q2`, **lo stesso inviluppo** *(`MB.partenza`)*.
- **I `12` componenti:** l'indice e' `2 e + s` *(`e` l'estremita' `0..5` del nodo, `s` lo spin)*. ### **`sigma_z` = `sum_e |q_{e, su}|^2 - |q_{e, giu}|^2`; l'elicita' media = `sum_e q_e^+ (sigma.n_e) q_e`, `n_e` il versore dell'arco dell'estremita'** *(`mot.geo.n`, lo stesso della moneta: `motore._ruota_attorno_a_n`)*; **la distribuzione sulle `6` estremita'** `sum_s |q_{e, s}|^2`.
- **Il residuo per tick:** `lambda = <psi, T psi>/<psi, psi>`, **`|T psi - lambda psi|/|psi|`**, col tick della scena *(`MS.tick`, il congelato vero)*.
- **Newton:** `LP.newton` con la scena a `eps` *(`MB.newton_a`)*, il criterio di `26300537` *(`1e-9`, `30` passi)*.
- **La corsa:** le righe di `MB.lunga`, con la partenza come argomento; `CL.punto` da' `w`, il cuore `f_win` entro `w_in`, `f_3w0` *(l'alone `1 - f_3w0`)*, il picco.
- **Il confronto di Luca** *(`40061005`, `26300537`: il cuore `0.586 -> 0.459` in `3000`)* **e' a `s 0.3`, `eps 0`**: non e' la stessa costruzione. ### **Serve quindi la corsa di confronto:** `A` a `K` a `eps 0.5`, `s 0.15`, `r 1`, `g 1`, **lo stato iniziale della scena** *(l'inviluppo per `Q_K` e la fase di `K`: `_energia_del_legame.stato`)*, `20000` tick. **La dichiaro.** I dati di `26300537` *(`_stato_fermo`, `corsa_L81_*.jsonl`, `s 0.3`)* si stampano accanto, come contesto.

### Cosa NON so

- **Se esiste una simmetria che ruota la coppia** *(una rotazione di spin che il tick e il legame sulla densita' TOTALE rispettano)*: a `eps 0` `sigma_z` commuta col tick libero *(`e92a7f9c`)*; ### **il resto non lo so.**
- **Lo stato di partenza della corsa di `B` e quello di `A` a `K` non sono costruiti allo stesso modo** se il punto `2` non trova uno stato fermo *(`B`: lo stato migliore di Newton; `A` a `K`: l'inviluppo, come chiede Luca)*: ### **lo scrivo accanto ai numeri.**
- **`mu` per `D`** nella corsa di `A` a `K`: non c'e' uno stato fermo; **uso il `mu` di Rayleigh dello stato iniziale** *(`-arg<psi, T psi>/s`)*, dichiarato.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `1` | **la griglia:** `theta = i (pi/2)/6`, `i = 0..6`; `phi = j 2 pi/8`, `j = 0..7` *(`7 x 8 = 56`)*, a `eps 0.5` e `0`. Per ognuno: il residuo, il `mu` di Rayleigh. **Il controllo:** lo stato di `q1` per `8` fasi globali `e^{i chi}` *(una simmetria ESATTA del tick)*: ### **lo scarto `s0` del residuo e' il rumore.** ### **Il residuo DIPENDE dalla scelta se `max - min > 10 s0`** *(`FATTORE_DEROGA`)*; **altrimenti la rotazione dentro la coppia e' una direzione libera: si dice.** **DEVE:** `q1`, `q2` ortonormali entro `1e-12`; `q(theta, phi)` autovettore di `A(Gamma)` entro `1e-10`. **E di `q1`, `q2`:** `sigma_z`, l'elicita' media, le `6` estremita'. |
| `2` | **se dipende:** Newton dalla scelta del residuo minimo, a `eps 0.5` e `0`, ogni stato committato appena trovato. ### **Se la rotazione e' una direzione libera: si scrive e non si insiste** *(il vincolo che la fisserebbe e' una condizione in piu' che non scelgo io: la lascio a Luca)*. |
| `3` | **a `eps 0.5`, `20000` tick** *(`3000` unita' di tempo)* **a pezzi di `4000`, ogni pezzo committato; due corse, una alla volta:** **`B`** dallo stato fermo se il punto `2` lo trova, **altrimenti dallo stato migliore** *(il residuo piu' basso fra `ab7226e7` e il punto `2`, dichiarato)*; **`AK`** dallo stato iniziale della scena. Ogni `10` tick il cuore, la larghezza, l'alone, il picco; ogni `20` `|D|/|psi0|` e le bande di `D`; a fine pezzo le rotazioni per banda *(l'esame di `_scatola`, `40` tick)*. **Le finestre di `500`:** il cuore all'inizio e alla fine, la pendenza, la larghezza, l'alone, il picco medio. **DEVE:** `M` entro `1e-10`; ogni pezzo riparte dalla fine del precedente *(sha1)*. |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **(q1)** il residuo dipende dalla scelta nella coppia e una scelta fa convergere Newton: **il solitone su `B` a `Gamma` esiste** *(poi (b1)/(b2) dalla corsa)*;
- **(q2)** la rotazione dentro la coppia e' una direzione libera: con il vincolo Newton converge, o no;
- **(q3)** nella corsa lunga **il cuore di `B` a `Gamma` RESTA** *(oscilla senza calare)* **mentre quello di `A` a `K` si svuota**: la protezione si vede anche senza stato fermo;
- **(q4)** il cuore di `B` a `Gamma` si svuota: **quale uscita** *(le bande di `D`)*;
- **(q5)** altro.
- ### ⚠ **«Resta» e «si svuota» non hanno soglia** *(Luca)*: **stampo le pendenze del cuore per finestra, `B` e `AK` affiancati**, e la parola la scrivo con quei numeri accanto.

## 4. LE MOTIVAZIONI

La domanda vera e' **se il cuore regge** sul punto dove la regola chiude le uscite: **la protezione, se c'e', si vede nella corsa anche senza stato fermo**, contro `A` a `K` costruito allo stesso modo. **E la scelta dentro la coppia separa il metodo dalla fisica** nel non-converge di `ab7226e7`.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_coppia_di_B.py` e la riga nell'inventario, committati prima di girare.
3. `--griglia` *(il punto `1`)*, committato.
4. `--cerca e05`, `--cerca e0` *(se dipende)*, ciascuno committato appena trovato.
5. `--lunga B` a pezzi, poi `--lunga AK` a pezzi, ogni pezzo committato.
6. `--referto`; `doc/CHIUDERE_LE_USCITE.md` *(l'esito)*; `RELAZIONE`; `MAPPA` *(la riga `d`)*; la sezione `6` qui.

### Annotazione *(dopo la prova a secco, prima della griglia)*

- ### **La premessa «la distribuzione sulle `6` estremita' del nodo» era sbagliata nel dettaglio:** le `6` righe del blocco sono la CELLA *(3 archi, due estremita' ciascuno; `inc.nodo[:6]` `0, 81, 0, 1, 0, 82`)*. **Per uno stato di `Gamma` il peso e' lo stesso** *(ogni nodo riceve le estremita' pari della sua cella e le dispari delle vicine)*: lo script lo dice e lo cabla *(due assert)*.
