# 2026-11-05 — LE TRE CARTE STATICHE *(Luca `2026-11-05` `15:28` e l'ordine delle `15:42`: la voce `3` della coda)* -- **NESSUNA CORSA**

> **Le tre carte** *(minuti l'una, un calcolo alla volta, dopo `TBS`)*: ① **la dispersione del vuoto attorno a `F3`** *(per il `lambda` della legge di forza della coppia)*; ② **la curva `E_int(d)` della coppia** *(da `24` a `80` ogni `2` nodi, centri sui nodi, fase `0` e `pi`)*; ③ **la dimensione del solitone della scena** a `N` da `2.5e5` a `4e6`. **Poi FERMO:** Luca sceglie le corse alla loro luce.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

### 1.0 Come si costruisce la scena *(vale per tutte e tre)*
- `V.scena` *(`_vuoto_vivo_B`)* = `D.configura(forma, s, N)` *(mette in memoria `VC.FORMA`, `VC.S`, `DC.N` e li rimette all'uscita)* + `DC.prepara(s)` + `rec["fattore"] = (L - 0.1) / rec["larghezza"]` + `DC.nuovo(rec, vuoto)`; **asserisce `z["L"] == 81`**.
- ### **La larghezza del solitone in nodi viene dal profilo del CONTINUO a quella `N`** *(`DC.prepara`: `MPS.largo(VC.FORMA, c, s, N)["larghezza"]` = `w0`)*; **il reticolo ha passo `1` nodo** *(`scena_l2.scena_toro`, `1.0`)*; ### **`L = 3 ceil(fattore w0 / 3)`**, e col `fattore` di sopra **`L = 81` qualunque sia `w0`.** Quindi: ### **a un'altra `N` la larghezza in nodi CAMBIA** *(e la carta ③ ha senso)*, **e `L` resta quello chiesto.**
- ### ⚠ **`L` E' UN MULTIPLO DI `3`** *(il fattore di valle `e^{2 pi i (m1 + m2) / 3}` del profilo, `EL.stato`)*: ### **«`L ~160`» della coppia vuol dire `159` o `162`, non `160`.** **Lo segnalo a Luca** *(la coppia e' dopo il FERMO: decide lui)*; **per la carta ② propongo `162`** *(la meta' del periodo `81`: la distanza massima `80` lungo `A1` ci sta)*.
- **`D.iniziale(forma, s, L)`** costruisce gia' la scena su un `L` qualsiasi *(il `fattore` ricalcolato)*: **le carte la usano con `N` e `L` espliciti**, senza toccare i globali della corsa *(`V.N`, `V.L`)*. **La partenza** = quella di `V.partenza` *(`"BG"`: la coppia `CB.coppia`, l'inviluppo `CO.inviluppo(z, pK, q, N)`)* **con `N` esplicito**, poi il vuoto `F3` sostituito come in `TF3`.
- ### **Il controllo positivo comune** *(`CS0`, mio)*: **a `N = 1e6`, `L = 81` la scena e la partenza costruite cosi' sono quelle di `V.scena` / `V.partenza` AL BIT** *(gli sha)*.

### 1.1 La dispersione del vuoto attorno a `F3` *(carta ①)*
- **Il vuoto vive sulle estremita'** *(`phi_h`, `2m` valori complessi: per nodo `3` archi, `6` estremita')*; **il tick vivo intero** *(`AC.tick` dopo la rampa)* **lo fa girare** *(`F3 -> e^{i omega} F3` per tick, `omega = 3 pi / 20`, `fase_F3.txt`)*.
- ### **Cosa NON so: se l'aggiornamento del vuoto e' lineare e complesso-lineare in `phi`.** **Quindi la misura e' REALE-lineare** *(generale)*: un disturbo `delta` *(reale, poi immaginario)* su una componente di un nodo, **`psi = 0`**, un tick, meno il tick del vuoto imperturbato, diviso per l'ampiezza, **nel riferimento che gira** *(moltiplicato per `e^{-i omega}`)*; **`12` gradi di liberta' reali per cella**; la matrice di Bloch `T(k)` `12 x 12` *(per `k` qualsiasi, come `carta_isotropia`)*; gli autovalori: **le fasi** *(le frequenze `omega_v(k)`)* **e i moduli** *(se `|lambda| != 1` il vuoto non e' neutro: scritto)*.
- **I DEVE proposti:** `VD-L` **la linearita'** *(la risposta a `amp` e a `2 amp` uguali entro `1e-6` relativo: se no, il vuoto non e' lineare a quell'ampiezza e la carta si ferma)*; `VD-T` **l'invarianza per traslazione**; `VD-G` **per `k` qualsiasi = `fft2` sulla griglia**; ### **`VD-0` il modo di Goldstone:** **la rotazione globale di fase** *(`delta = i F3`)* **a `Gamma` e' un autovettore con autovalore `1`** *(nel riferimento che gira)*: **un controllo positivo che puo' fallire**.
- **Il risultato:** le bande `omega_v(k)`, **il gap a `Gamma`** *(escluso il Goldstone)*, la curvatura; ### **il `lambda` per la coppia** *(una PROPOSTA di lettura, dichiarata)*: per una banda `omega = Delta + a k^2`, **il disturbo statico decade come `e^{-r / lambda}` con `lambda = sqrt(a / Delta)`** *(`omega(i kappa) = 0`)*. ### ⚠ **Cosa NON so:** **a quale frequenza il solitone eccita il vuoto** *(la sorgente oscilla, nel riferimento che gira, alla frequenza del solitone meno quella del vuoto)*: **il `lambda` «statico» puo' non essere quello giusto**, e lo scrivo nel referto.

### 1.2 La curva `E_int(d)` della coppia *(carta ②)*
- **La scena:** `L 162` *(1.0)*, `N = 1e6`, `F3`; **la partenza singola** `p1` *(la partenza di `TF3` su questa scena)*; **la seconda** `p2` = `p1` **traslata di `d` nodi lungo `A1`** *(`m1 -> m1 + d`: una simmetria del reticolo)*, per **`e^{i 0}` o `e^{i pi}`**.
- ### ⚠ **LA FASE RELATIVA, DEFINITA:** la traslazione porta anche il fattore di valle *(`e^{2 pi i (m1 + m2) / 3}` diventa `e^{-2 pi i d / 3}` volte quello di prima)*: ### **«fase `0`» = la copia ESATTA traslata** *(lo stesso stato fisico spostato)*, **«fase `pi`» = la copia traslata per `-1`**. **Non e' la fase della portante locale nel punto medio** *(che dipende da `d` modulo `3`)*: **dichiarato**.
- ### ⚠ **L'ENERGIA DI INTERAZIONE, DEFINITA:** il libro dei conti conta **anche l'energia del vuoto** *(`E[0]`, la scena con `psi = 0`)*. **`E(coppia) - 2 E(singolo)` del mandato la conterebbe due volte** *(= `E_int - E[0]`)*. ### **La definizione proposta: `E_int(d) = E[p1 + p2] - E[p1] - E[p2] + E[0]`** *(il vuoto una volta sola)*; **la forma del mandato stampata accanto.** **Lo segnalo a Luca.**
- **`F_s(d) = -dE_int / dd`** *(differenze centrali sui `d` della griglia)*.
- **I DEVE proposti:** `EI-T` **`E[p2] = E[p1]`** *(la traslazione e' una simmetria)* **entro `1e-12` relativo**; `EI-0` **`E[p1 + 0 * p2]`** *(il caso banale)* **= `E[p1]` al bit**; `EI-F` *(deve fallire)* **`E[p1 + p2] - 2 E[p1]` = `E_int`** *(la forma col vuoto contato due volte: deve differire di `E[0]`)*.
- ### ⚠ **La coppia statica non e' uno stato della coppia:** la somma di due partenze non lineari *(`E_int` dice l'energia della SOVRAPPOSIZIONE, non di una coppia rilassata)*: dichiarato *(il task history della coppia, 2.5)*.

### 1.3 La dimensione del solitone *(carta ③)*
- **`N` = `2.5e5`, `5e5`, `1e6`, `2e6`, `4e6`**, `L 81`, `F3`: **per ognuna la scena** *(`w0` del continuo)*, **la partenza**, e sulla densita' a `t 0`: **`w`** *(`toro.misure`)*, **lo spessore del bordo e l'esagonalita'** *(`carta_forma.forma`)*.
- ### ⚠ **LE SOGLIE SCALANO CON `N`:** `rho` va come `N`; **le soglie della forma** *(`1`, `10`, `100`, `300` a `N = 1e6`)* **si scalano per `N / 1e6`** *(gli stessi livelli relativi)*, **e le assolute si stampano accanto**. **Il mare a `t 0` non c'e'** *(la partenza)*: tutte le soglie contano.
- **Cosa NON so:** se la scena a un'altra `N` passa i controlli della scena *(`DC.prepara` restituisce un `verdetto` del risolutore: stampato)*; **se `L 81` basta per `N = 2.5e5`** *(il solitone piu' largo: `w0` contro la meta' del periodo `40.5`, stampato; se `3 w0 > 40.5`, la riga non conta)*.
- **I DEVE proposti:** `CS0` *(sopra)*; `DM-F` *(deve fallire)* **`w` a `N = 2e6` = `w` a `N = 1e6`** *(se fossero uguali, la carta non vedrebbe `N`)*.

## 2. PROGETTAZIONE
| | il passo | cosa decide | cosa mi farebbe FERMARE |
|---|---|---|---|
| `1` | una carta sola, `csv/solitone/carta_statiche.py`, coi modi `--vuoto`, `--coppia`, `--dimensione`; **committata prima di girarla** | -- | -- |
| `2` | a `TBS` finita *(e dopo il suo referto)*: `--vuoto`, poi `--coppia`, poi `--dimensione`, un commit ciascuna col referto | il `lambda`, `E_int(d)`, `w(N)` | `CS0` fallisce *(la scena non e' quella della corsa)*; `VD-L` fallisce *(il vuoto non lineare)*; un DEVE fallito |
| `3` | **FERMO: Luca sceglie le corse** | -- | -- |

## 3. TODO
1. Questo task history, un commit.
2. `carta_statiche.py`, `D6` *(un `.py` nuovo di `csv/solitone`)*, committati.
3. A `TBS` finita: il referto di `TBS`; la patch del pilota *(gia' pronta)*; la cassetta; poi le tre carte, un calcolo alla volta.
4. Le due cose da dire a Luca: **`L 159` o `162`** *(non `160`)*; **`E_int` col vuoto una volta sola**.

## 4. LA DECISIONE DI LUCA *(`2026-11-05` `16:28`; non mia)*
1. **La coppia su `L 162`** *(multiplo di `3`)*: **vale per la carta statica e per le corse della coppia.**
2. **`E_int = E[p1 + p2] - E[p1] - E[p2] + E[0]`** *(il vuoto contato una volta)*. **La formula del mandato, `E(coppia) - 2 E(singolo)`, era sbagliata** *(Luca la registra come l'errore `n.107` del guardiano)*: **si stampa accanto, solo come confronto** *(e' cio' che fa `carta_statiche.py`, `c1027d67`: la colonna e il DEVE `EI-F`)*.
3. **Il resto come proposto** *(il `lambda` statico come proposta di lettura, il Goldstone escluso dal gap e dichiarato)*. **Le carte girano a `TBS` finita.**

## 5. L'ESITO DI `--vuoto` *(`doc/referti_l2/statica_vuoto.txt`, `carta_statiche.py` `ddc1389c`)*: **`4/5`, `VD-T` FALLISCE** -- ### **FERMO: decide Luca**
- **Passano:** `CS0` *(la scena al bit)*; **`VD-L` `4.066e-09`** *(soglia `1e-6`)*; **`VD-G` `3.514e-16`**; **`VD-0` il Goldstone `4.343e-09`** *(soglia `1e-6`)*.
- ### **FALLISCE `VD-T`:** **la risposta da un altro nodo (`412`), riportata indietro, contro quella dal nodo `0`: `1.639e-09` relativo, soglia `1e-12`.**
- ### **LA MIA LETTURA, UN'IPOTESI E NON UNA MISURA:** **`1e-12` sta sotto il pavimento aritmetico della differenza finita.** **La risposta e' `(tick(F3 + AMP e) - tick(F3)) / AMP`, con `AMP = 1e-7`:** **l'errore di arrotondamento della sottrazione e' `~eps |phi| / AMP ~ 1e-16 / 1e-7 = 1e-9`** *(se `|phi| ~ 1`)*, **cioe' la grandezza di `VD-T` (`1.6e-9`), di `VD-L` (`4.1e-9`) e del Goldstone (`4.3e-9`).** **`VD-G` passa a `3.5e-16` perche' confronta due conti sulle STESSE risposte** *(la somma sui vettori contro `fft2`)*, **non due risposte.** ### **E' L'ERRORE DI `deve-contro-la-propria-premessa` di nuovo:** **ho messo a `VD-T` la tolleranza di `VD-G` (`TOLL_A`) senza confrontarla col pavimento della misura.**
- ### **Un criterio di chiusura proposto** *(non lo giro senza Luca)*: **`VD-T` ad `AMP = 1e-6` e `1e-5`:** **se e' il pavimento, `eT` cala come `1 / AMP`** *(`~1.6e-10`, `~1.6e-11`)* **mentre `VD-L` cresce come `AMP`**; **se no, la traslazione non e' una simmetria del vuoto `F3` alla precisione detta, e va cercato perche'.** **La proposta di correzione:** **`VD-T` con la tolleranza di `VD-L` (`1e-6`, la scala della linearita')**, **piu' la prova di scala sopra come controllo che la soglia non nasconda nulla.**
- ### **IL RESTO DEL REFERTO, CON IL FALLIMENTO ACCANTO** *(non lo leggo come risultato finche' `VD-T` non e' chiuso)*:
  - **a `Gamma` le `12` fasi per tick, nel riferimento che gira:** `0` *(sei, entro `2e-9`)*, `+-4.712389e-01` *(due coppie)*, `+-9.424778e-01`: **`0`, `+-omega`, `+-2 omega`** *(`omega = 3 pi / 20 = 0.4712389`)*; **i moduli da `0.999999999` a `1.000000012`** *(il vuoto neutro)*.
  - ### **il ramo del gap e' PIATTO:** `Delta = 3.141593` per unita' di tempo *(`omega / s`)*, **e lungo `A1` da `|k| 0.01` a `0.10` lo stesso numero alle `7` cifre stampate**; **la curvatura `-5.2e-10`** *(dentro il pavimento)*: ### **`lambda = sqrt(|a| / Delta)` = `0.0000` nodi: la proposta di lettura del `lambda` statico NON da' una lunghezza.** **Il supporto della risposta di un tick e' `7` nodi** *(il nodo e i `6` vicini)*: **non so se la parte fuori dal nodo sia fisica o del pavimento** *(la carta non stampa la sua ampiezza)*.
- **Le due carte che restano** *(`--coppia`, `--dimensione`)* **non dipendono da `VD-T`**, ma la regola dice **FERMATI**: **non le giro senza Luca.**
