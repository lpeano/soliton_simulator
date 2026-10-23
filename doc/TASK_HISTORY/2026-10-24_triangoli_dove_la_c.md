# DOVE NASCE UN MODO SENZA MASSA SUI TRIANGOLI (LA c DEL MODELLO): IL REGIME s -> 1, LA MONETA, LA PARTICELLA VESTITA DAL VUOTO

> **Il mandato:** di Luca, «dove nasce un modo senza massa sui triangoli» *([[DECISIONE-SOLO-TRIANGOLI]]; [[LUCE-VINCOLO-LAMPI-GAMMA]]; [[SPAZIOTEMPO-3PIU1]]; il gradino prima e' `77f9f850`)*.
> ### **Solo spettri, in memoria.** ### **`leggi.yaml`, l'impronta `2e7f795d2a52fbe7`, la convenzione nel repo e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE)*.
> ### **Importati, non copiati:** `_triangoli`, `_triangoli_bassa_energia`, `_triangoli_forza`, `_triangoli_fattore`, `_triangoli_luce`, `_triangoli_dove_la_luce` *(la riga delle parti `A` e `B`)*,
> `_stabilita_triangoli`, `_stabilita_lineare`, `_screening_forme_s3`, `_zero_simmetrico`.
> ### **LA PRECISAZIONE DI LUCA:** ### **qui NON si cerca la luce** *(l'onda del campo `U(1)` sugli archi, oggi senza dinamica)*: ### **si cerca un MODO SENZA MASSA qualunque che fissi la `c` del modello.** ### **Nei
> referti: «modo senza massa».** ### **LE PAROLE:** ### **«il limite `s <= 1»`, «il regime `s -> 1`», «`v_max`»**, ### **nessuna chiamata «cono» senza dire quale.**

### ⚠ **L'ORDINE DELLA CODA** *([[PRECEDENZA-IN-CODA]])*: ### **questo mandato SOSTITUISCE «dove puo' nascere la luce sui triangoli»** *(le stesse parti `A` e `B`, piu' la `C`)*: ### **quel task
history** *(`e462e840`)* ### **e il suo strumento** *(`csv/_triangoli_dove_la_luce.py`, `2ce6ad86`)* ### **restano; la sua corsa l'ho FERMATA a un terzo** *(era mia)* ### **e i suoi file parziali li ho
tolti: le parti `A` e `B` le rigira QUESTO strumento, importando la sua riga.**

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica.** 2. **Il gradino:** ### **`(A)` il regime `s -> 1`; `(B)` la moneta; `(C)` la vestizione.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o
il segno?** ### **No: `cs` uniforme; il legame acceso solo nella parte `C`, con le forme in memoria.** 5. **Emergente o imposto?** ### **E' la domanda:** ### **un modo senza massa nasce, e la particella si
accorda con `v_max`?**

## 1. VISTO IN MEMORIA, prima di scrivere *(i numeri li ristampa lo strumento)*

- ### **Parti `A` e `B`** *(dal task history `e462e840` e dalla sua prova a vuoto)*: ### **a `s = 1` la scena NON e' rifiutata; il tocco lineare e' a `Gamma` attraverso la fase `pi`** *(pendenza `0.7071 s`, isotropa)*,
  ### **non a `K`** *(il salto a `K` resta `2 pi/3`)*; ### **`v_max/s -> 0.70711`; `v_b/s` della coppia a `K` scende verso `0.550`.**
- ### **PARTE `C`, LA VESTIZIONE:** ### **la base `e^{i K.r} u_K` a densita' uniforme e' STAZIONARIA** *(il legame dipende solo da `rho` e `Lambda`: residuo `4.8e-15`)*; ### **la famiglia delle onde piane
  `e^{i (K+q).r} u(q)` lo e' anche, e la sua frequenza per tick `omega(q)` e' la dispersione della particella VESTITA.** ### **`omega''` NON cambia** *(`0.116536` per ogni forma e `x`: a densita' fissa la fase
  del legame non dipende da `q`)*; ### **cambia solo `omega(0)`, quindi `v_b`.** ### ⚠ **E `S4` A `x -> 0` NON TORNA NUDA:** ### **`alpha_4(x -> 0) = -pi`** *(`-3.14154` a `x 1e-8`, da `_screening_forme_s3._ab`)*:
  ### **una fase `-pi s` per tick ANCHE senza materia, che trasforma lo zero simmetrico in quello di oggi** *(`omega(0) = -0.4845` contro `+0.4580`)*.

## 2. IL METODO

### **PARTI `A` E `B`:** ### **la riga di `_triangoli_dove_la_luce`** *(i livelli sul cerchio ai quattro punti, i tocchi e il loro esponente, `v_max` di tutti i settori, la coppia a `K` col salto e `v_b` dal fit
di `7daa8840`, la coppia attraverso `pi` a `Gamma`, la `c6` nelle due convenzioni)*, ### **con le `s` e le `eps` del mandato; l'andamento verso `s = 1`.** ### **«Il modo massivo piu' basso»: la coppia a `K` seguita in
`eps`** *(dichiarato)*.

### **PARTE `C`** *(eps `0` e `0.5`; `s` in `(0.1, 0.3, 0.5)`; `x` in `(1e-4, 1e-3, 1e-2, 1e-1)`; `S1`, `S3`, `S4`; le due bande della coppia; zero simmetrico; lato `48`)*
- ### **LA CELLA DI TRE NODI CHE RIPORTA `K` A `Gamma`, realizzata come GAUGE:** ### **la perturbazione si scrive `delta psi = e^{i K.r} eta`, e la mappa su `eta` e' invariante per traslazione** *(la camminata
  diventa `A(K + q)`, il legame vede solo `|psi|^2`)*: ### **equivale alla cella di tre nodi, e accoppia `K + q` con `K - q`** *(Bogoliubov a `K`)*.
- ### **LA BASE:** ### **`e^{i K.r} u_K`, `u_K` il primo vettore della banda a `K`, riscalata a `rho/Lambda = x`; `phi = 1`; la stazionarieta' di un tick entro `1e-12`** *(se no: un risultato, e il punto non si misura)*.
- ### **LA PARTICELLA VESTITA:** ### **le onde piane `e^{i(K+q).r} u(q)`, `q = 2 pi j/48`, `j` in `(-2..2)`, `u(q)` lo spazio della banda seguito; `omega(q)` = la fase di un tick; `omega(0)`, `omega''` col Richardson**
  *(cartesiano `x 3/4`)*, ### **`v_b vestita = sqrt(|omega(0)| omega'')`; il fit iperbolico con `j` fino a `4`.** ### **La NUDA: lo stesso conto sulle fasi della camminata sola** *(`A(K+q)`)*.
- ### **LA GREEN di un tick nel gauge, DIFFERENZE CENTRATE** *(`e = 1e-4` della scala: l'arrotondamento `~1e-12`, la non linearita' `O(e^2)`)*, ### **nel riferimento che ruota con le due fasi:** ### **il tasso;
  il ramo per `0` a `q = 0`** *(la continuazione della particella: il modo di Goldstone della base)*: ### **esponente in `q`, e se lineare la velocita'** *(un SUONO: un modo senza massa)*; ### **`v_max`
  dell'accoppiato** *(le pendenze delle fasi ordinate lungo tre linee: una stima, dichiarata)*.
- ### **LA SIMMETRIA:** ### **la base a `K` ha la simmetria di `120` gradi, non di `60`** *(`60` gradi porta `K` in `K'`)*: ### **nella cella di tre nodi il controllo e' a `120` gradi** *(dichiarato: il `60` non si applica a una base
  che lo rompe)*.

## 3. LE PREVISIONI *(prima dei numeri dello strumento)*

- ### **PARTE `A`:** ### **la previsione del guardiano e' smentita da cio' che ho visto** *(il tocco lineare e' a `Gamma` attraverso `pi`, a `0.707 s`, non a `K`)*; ### **il primo PUO' FALLISCE** *(`v_max/s = 0.707`)*, ### **il
  secondo PASSA.**
- ### **PARTE `B`:** ### **nessun lineare a `s <= 0.5`: il terzo PUO' FALLISCE** *(non sicuro)*.
- ### **PARTE `C`:** ### **la vestizione NON cambia l'inerzia, cambia l'energia a riposo:** ### **`v_b vestita/v_b nuda = sqrt(omega_vestita(0)/omega_nuda(0))`**; ### **con `S1` cresce poco** *(`0.770 -> 0.773` a `x 0.1`)*; ### **con
  `S4` scende** *(`0.792 -> 0.412`)*; ### **con `S3` e' singolare.** ### **Il quarto PUO'** *(un punto STABILE con `v_b vestita/v_max` entro il `5%` da `1`)*: ### **`S1` e' stabile ma `v_b` resta `~1.25 v_max`;
  `S4` attraversa `v_max` ma e' instabile** *(`77f9f850`)*: ### **prevedo che FALLISCA.**
- ### ⛔ **IL DEVE DELLA PARTE `C`** *(`x 1e-8`: `v_b vestita = nuda` entro `1e-4` per `S1` e `S4`)*: ### **prevedo che FALLISCA PER `S4`, per la ragione di FISICA della sezione `1`** *(`alpha_4(0) = -pi`)*: ### **il criterio
  NON lo cambio; se fallisce, mi FERMO dopo il referto.**

## 4. I CRITERI, FISSATI ORA *(dal mandato)*

- ### **DEVE: a `s 0.3, eps 0`, il salto della coppia a `K` e `v_b` = `8781162c` e `7daa8840` entro `1e-9`; `v_max` = `77f9f850` entro `1e-6`.**
- ### **DEVE: lo spettro invariante per `60` gradi entro `1e-12` a ogni `(eps, s)`** *(le due convenzioni)*; ### **nella cella di tre nodi a `120` gradi** *(sopra)*.
- ### **DEVE: parte `C`, a `x 1e-8`, `v_b vestita = v_b nuda` entro `1e-4` per `S1` e `S4`** *(`S3` singolare: saltato, dichiarato)*.
- ### **DEVE FALLIRE, per la chiave giusta: «a `eps 0`, `s 0.3` esiste un modo lineare senza massa»** *(la chiave: dei tocchi trovati, nessuno lineare)*.
- ### **PUO': a `s = 1`, `eps 0`, `v_max/s` entro `0.01` da `1`.** ### **PUO': a `s = 1`, `eps 0`, esiste un tocco lineare.** ### **PUO': un `(eps, s <= 0.5)` con un modo lineare senza massa a velocita' entro il `5%`
  da `v_b` della coppia a `K`.** ### **PUO': parte `C`, un punto STABILE con `v_b vestita/v_max` entro il `5%` da `1`** *(`v_max` dell'accoppiato; STABILE: il tasso `<= 1e-6`)*.
- ### **IL VERDETTO DI FISICA: le tabelle.** ### **A parte: tre righe; la definizione di Luca; la vestizione; la tensione col principio di equivalenza** *(sui triangoli NON misurato)*; ### **che cosa resta per il campo
  `U(1)` e per le onde di `cs`.**

### 📝 **ANNOTAZIONE 1** *(prima della corsa, nel commit dello strumento)*: ### **la prova a vuoto della parte `C`** *(`eps 0, s 0.3`, `S1` e `S4`, `x 1e-2`)* ### **ha trovato DUE miei difetti, corretti, e
UNA scelta che cambio prima dei numeri:**
- ### **`(a)` `v_b = sqrt(omega(0) omega'')` col PRODOTTO** *(la banda bassa ha `omega(0) < 0` e `omega'' < 0`)*: ### **la radice di `|omega(0)| omega''` alzava un errore.** ### **Dove il prodotto e' negativo** *(`S4` sulla banda
  alta: `omega(0) < 0`, `omega'' > 0`)* ### **`v_b` NON e' definita, e si scrive.**
- ### **`(b)` la stima di `v_max` dell'accoppiato dalle fasi ORDINATE dava `1.06 s`** *(l'ordinamento salta quando un autovalore passa per `+-pi`)*; ### **con l'accoppiamento ungherese fra `q` vicini `0.816 s` -- ancora
  sopra il nudo `0.612 s` a `x 1e-2`, dove la vestizione sposta `omega(0)` di `3e-5`: agli incroci la griglia `2 pi/48` confonde i rami.** ### **LA SCELTA:** ### **il rapporto `v_b vestita/v_max` del quarto PUO' usa `v_max`
  NUDO di tutti i settori** *(`_triangoli_dove_la_luce.vmax_tutti`)*; ### **la stima resta stampata come LETTURA.**
- ### **I NUMERI VISTI** *(non li uso)*: ### **il controllo a `120` gradi `8.3e-12`; `S1` a `x 1e-8` = la nuda entro `2e-13`; `S4` a `x 1e-8` NO** *(`0.75`: `alpha_4(0) = -pi`, come previsto)*; ### **`S1` stabile, `S4`
  instabile** *(`0.017`-`0.042`)*; ### **il ramo per `0` quadratico** *(esponente `1.97`-`2.00`: nessun suono)*.

## 5. TODO DEL NEXT STEP

1. questo task history, da solo; 2. `csv/_triangoli_dove_la_c.py` e l'inventario, prima dei numeri; 3. la corsa, il referto, la relazione, i collegamenti, la sezione `6`.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*

> **La corsa:** ### **strumento `csv/_triangoli_dove_la_c.py` sha1-BYTE `a2846472`; referto `doc/referti_l2/triangoli_dove_la_c.txt` sha1-BYTE `020e9cf5`, `.jsonl` `0870eadc`; `38` minuti.** ### **Le tabelle sono GENERATE dal
> `.jsonl`.** ### **`5` controlli su `9`.**

### ⛔ 6.0 I CONTROLLI -- **UN DEVE FALLISCE, come avevo previsto per `S4`: MI FERMO**

| criterio | esito | il numero |
|---|---|---|
| DEVE: a `s 0.3, eps 0` il salto a `K`, `v_b`, `v_max` = `8781162c`, `7daa8840`, `77f9f850` | **PASSA** | `2.2e-16`, `0.0`, `0.0` |
| DEVE: `60` gradi a ogni `(eps, s)`, le due convenzioni | **PASSA** | `3.02e-15` |
| DEVE: nella cella di tre nodi, `120` gradi | **PASSA** | `4.54e-10` |
| DEVE: a `x 1e-8` la vestita = la nuda entro `1e-4`, `S1` e `S4` | ### **FALLISCE** *(previsto)* | ### **`S1` entro `2e-13`; `S4` NO: `0.73`-`0.75` sulla banda bassa, non definita sulla alta** *(`alpha_4(0) = -pi`)* |
| DEVE FALLIRE: a `eps 0, s 0.3` un modo lineare senza massa | **fallisce, come deve** | `19` tocchi, `0` lineari |
| PUO': a `s = 1` `v_max/s` entro `0.01` da `1` | ### **FALLISCE** *(previsto)* | `0.7071` |
| PUO': a `s = 1` un tocco lineare | **PASSA** *(previsto)* | `12` rami, tutti a `0.7071 s` |
| PUO': a `s <= 0.5` un lineare a `v_b` entro il `5%` | ### **FALLISCE** *(previsto)* | `0` lineari a `s <= 0.5` |
| PUO': parte `C`, un punto stabile con `v_b vestita/v_max` entro il `5%` da `1` | ### **FALLISCE** *(previsto)* | `38` punti stabili, `v_b/v_max` da `1.152` a `1.31` |

### **IL FALLIMENTO, letto:** ### **`S4` NON ha il limite della particella nuda a densita' nulla:** ### **`alpha_4(x -> 0) = -pi`, una fase `-pi s` per tick anche senza materia** *(trasforma lo zero simmetrico in quello di oggi)*.
### **Non e' un difetto della misura: e' una proprieta' della forma `S4`.** ### **Il criterio non lo cambio: e' di Luca dire se `S4` resta una candidata, o come si legge.**

### 6.1 PARTI `A` E `B` *(la particella nuda; `v_b` dal fit di `7daa8840`; «lineari»: i rami lineari dei tocchi, materia e vuoto, le due convenzioni)*

| parte | `eps` | `s` | `v_max/s` *(tutti i settori)* | salto a `K` | `v_b/s` *(le due bande)* | `v_b/v_max` | lineari, e la loro `v/s` | il salto attraverso `pi` a `Gamma` |
|---|---|---|---|---|---|---|---|---|
| A | `0` | `0.5` | `0.6351` | `1.4455` | `0.7391` `0.7391` | `1.164` `1.164` | 0  | `3.1416` |
| A | `0` | `0.7` | `0.6658` | `1.8469` | `0.6848` `0.6848` | `1.028` `1.028` | 0  | `1.8850` |
| A | `0` | `0.9` | `0.6962` | `2.0660` | `0.6018` `0.6018` | `0.864` `0.864` | 0  | `0.6283` |
| A | `0` | `0.95` | `0.7024` | `2.0873` | `0.5766` `0.5766` | `0.821` `0.821` | 0  | `0.3142` |
| A | `0` | `0.99` | `0.7063` | `2.0941` | `0.5553` `0.5553` | `0.786` `0.786` | 0  | `0.0628` |
| A | `0` | `0.999` | `0.7070` | `2.0944` | `0.5504` `0.5504` | `0.778` `0.778` | 0  | `0.0063` |
| A | `0` | `1` | `0.7071` | `2.0944` | `0.5498` `0.5498` | `0.778` `0.778` | 12 `0.7071` | `0.0000` |
| B | `0` | `0.05` | `0.5990` | `0.1570` | `0.7850` `0.7850` | `1.310` `1.310` | 0  | `5.9690` |
| B | `0` | `0.3` | `0.6122` | `0.9160` | `0.7701` `0.7701` | `1.258` `1.258` | 0  | `4.3982` |
| B | `0` | `0.9` | `0.6962` | `2.0660` | `0.6018` `0.6018` | `0.864` `0.864` | 0  | `0.6283` |
| B | `0.1` | `0.05` | `0.5990` | `0.1573` | `0.7850` `0.7850` | `1.310` `1.310` | 0  | `5.9688` |
| B | `0.1` | `0.3` | `0.6122` | `0.9179` | `0.7701` `0.7700` | `1.258` `1.258` | 0  | `4.3970` |
| B | `0.1` | `0.5` | `0.6351` | `1.4487` | `0.7391` `0.7389` | `1.164` `1.163` | 0  | `3.1403` |
| B | `0.1` | `0.9` | `0.6962` | `2.0714` | `0.6014` `0.6006` | `0.864` `0.863` | 0  | `0.6399` |
| B | `0.25` | `0.05` | `0.5990` | `0.1589` | `0.7850` `0.7850` | `1.310` `1.310` | 0  | `5.9675` |
| B | `0.25` | `0.3` | `0.6122` | `0.9279` | `0.7699` `0.7695` | `1.258` `1.257` | 0  | `4.3907` |
| B | `0.25` | `0.5` | `0.6351` | `1.4654` | `0.7386` `0.7374` | `1.163` `1.161` | 0  | `3.1338` |
| B | `0.25` | `0.9` | `0.6962` | `2.0989` | `0.5996` `0.5943` | `0.861` `0.854` | 0  | `0.6944` |
| B **(eps 0.5)** | `0.5` | `0.05` | `0.5990` | `0.1647` | `0.7850` `0.7849` | `1.310` `1.310` | 0  | `5.9632` |
| B **(eps 0.5)** | `0.5` | `0.3` | `0.6122` | `0.9626` | `0.7694` `0.7677` | `1.257` `1.254` | 0  | `4.3685` |
| B **(eps 0.5)** | `0.5` | `0.5` | `0.6351` | `1.5225` | `0.7374` `0.7318` | `1.161` `1.152` | 0  | `3.1110` |
| B **(eps 0.5)** | `0.5` | `0.9` | `0.6962` | `2.1859` | `0.5957` `0.5712` | `0.856` `0.820` | 0  | `0.8410` |
| B | `0.75` | `0.05` | `0.5990` | `0.1739` | `0.7850` `0.7848` | `1.310` `1.310` | 0  | `5.9562` |
| B | `0.75` | `0.3` | `0.6122` | `1.0172` | `0.7687` `0.7644` | `1.256` `1.249` | 0  | `4.3327` |
| B | `0.75` | `0.5` | `0.6351` | `1.6106` | `0.7357` `0.7216` | `1.158` `1.136` | 0  | `3.0743` |
| B | `0.75` | `0.9` | `0.6962` | `2.3083` | `0.5919` `0.5300` | `0.850` `0.761` | 0  | `1.0135` |
| B | `1` | `0.05` | `0.5990` | `0.1861` | `0.7849` `0.7847` | `1.310` `1.310` | 0  | `5.9468` |
| B | `1` | `0.3` | `0.6122` | `1.0884` | `0.7672` `0.7593` | `1.253` `1.240` | 0  | `4.2849` |
| B | `1` | `0.5` | `0.6351` | `1.7232` | `0.7324` `0.7059` | `1.153` `1.111` | 0  | `3.0256` |
| B | `1` | `0.9` | `0.6962` | `2.4584` | `0.5854` `0.4608` | `0.841` `0.662` | 0  | `1.1927` |
| B | `1.571` | `0.05` | `0.5990` | `0.2220` | `0.7847` `0.7842` | `1.310` `1.309` | 0  | `5.9182` |
| B | `1.571` | `0.3` | `0.6122` | `1.2965` | `0.7590` `0.7404` | `1.240` `1.210` | 0  | `4.1388` |
| B | `1.571` | `0.5` | `0.6351` | `2.0445` | `0.7101` `0.6424` | `1.118` `1.012` | 0  | `2.8798` |
| B | `1.571` | `0.9` | `0.6962` | `2.9513` | `0.5135` | `0.738` | 0  | `1.6030` |

### 6.2 PARTE `C` -- LA PARTICELLA VESTITA *(zero simmetrico; `omega(0)` vestito e nudo; `v_b` vestita`/s`; il tasso; il ramo per `0`; `v_b/v_max` col `v_max` nudo; `--` dove `omega(0) omega'' < 0`)*

| `eps` | `s` | banda | forma | `x` | `omega(0)` *(nuda)* | `v_b/s` | tasso | il ramo per `0` | `v_b/v_max` |
|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.1` | `0` | S1 | `1e-08` | `-0.15659` *(`-0.15659`)* | `0.7838` | -- | -- | -- |
| `0` | `0.1` | `0` | S1 | `0.0001` | `-0.15659` *(`-0.15659`)* | `0.7838` | `+1.6e-10` | quadratico 1.97 | `1.306` |
| `0` | `0.1` | `0` | S1 | `0.001` | `-0.15659` *(`-0.15659`)* | `0.7838` | `+1.2e-11` | quadratico 1.97 | `1.306` |
| `0` | `0.1` | `0` | S1 | `0.01` | `-0.15658` *(`-0.15659`)* | `0.7837` | `+1.2e-08` | quadratico 2.00 | `1.306` |
| `0` | `0.1` | `0` | S1 | `0.1` | `-0.15560` *(`-0.15659`)* | `0.7813` | `+2.0e-03` | altro 1.70 | `1.302` |
| `0` | `0.1` | `0` | S3 | `0.0001` | `-0.97765` *(`-0.15659`)* | `1.9583` | `+3.9e-02` | quadratico 1.97 | `3.263` |
| `0` | `0.1` | `0` | S3 | `0.001` | `-0.74757` *(`-0.15659`)* | `1.7125` | `+3.9e-02` | quadratico 1.97 | `2.853` |
| `0` | `0.1` | `0` | S3 | `0.01` | `-0.51910` *(`-0.15659`)* | `1.4270` | `+3.9e-02` | quadratico 1.97 | `2.378` |
| `0` | `0.1` | `0` | S3 | `0.1` | `-0.30547` *(`-0.15659`)* | `1.0947` | `+3.9e-02` | quadratico 1.97 | `1.824` |
| `0` | `0.1` | `0` | S4 | `1e-08` | `-0.47075` *(`-0.15659`)* | `1.3589` | -- | -- | -- |
| `0` | `0.1` | `0` | S4 | `0.0001` | `-0.46897` *(`-0.15659`)* | `1.3563` | `+1.1e-03` | quadratico 1.85 | `2.260` |
| `0` | `0.1` | `0` | S4 | `0.001` | `-0.46312` *(`-0.15659`)* | `1.3478` | `+4.3e-03` | quadratico 1.97 | `2.246` |
| `0` | `0.1` | `0` | S4 | `0.01` | `-0.43896` *(`-0.15659`)* | `1.3122` | `+1.4e-02` | quadratico 1.97 | `2.186` |
| `0` | `0.1` | `0` | S4 | `0.1` | `-0.35290` *(`-0.15659`)* | `1.1766` | `+3.3e-02` | quadratico 1.97 | `1.960` |
| `0` | `0.1` | `1` | S1 | `1e-08` | `+0.15659` *(`+0.15659`)* | `0.7838` | -- | -- | -- |
| `0` | `0.1` | `1` | S1 | `0.0001` | `+0.15659` *(`+0.15659`)* | `0.7838` | `+2.6e-11` | quadratico 1.97 | `1.306` |
| `0` | `0.1` | `1` | S1 | `0.001` | `+0.15659` *(`+0.15659`)* | `0.7838` | `+1.7e-09` | quadratico 1.97 | `1.306` |
| `0` | `0.1` | `1` | S1 | `0.01` | `+0.15660` *(`+0.15659`)* | `0.7838` | `+1.8e-08` | quadratico 1.97 | `1.306` |
| `0` | `0.1` | `1` | S1 | `0.1` | `+0.15758` *(`+0.15659`)* | `0.7862` | `+5.5e-04` | quadratico 1.97 | `1.310` |
| `0` | `0.1` | `1` | S3 | `0.0001` | `-0.66446` *(`+0.15659`)* | -- | `+7.0e-02` | quadratico 1.97 | -- |
| `0` | `0.1` | `1` | S3 | `0.001` | `-0.43438` *(`+0.15659`)* | -- | `+7.0e-02` | quadratico 1.97 | -- |
| `0` | `0.1` | `1` | S3 | `0.01` | `-0.20591` *(`+0.15659`)* | -- | `+6.9e-02` | quadratico 1.97 | -- |
| `0` | `0.1` | `1` | S3 | `0.1` | `+0.00771` *(`+0.15659`)* | `0.1740` | `+5.3e-02` | quadratico 1.97 | `0.290` |
| `0` | `0.1` | `1` | S4 | `1e-08` | `-0.15756` *(`+0.15659`)* | -- | -- | -- | -- |
| `0` | `0.1` | `1` | S4 | `0.0001` | `-0.15578` *(`+0.15659`)* | -- | `+1.0e-04` | quadratico 1.97 | -- |
| `0` | `0.1` | `1` | S4 | `0.001` | `-0.14993` *(`+0.15659`)* | -- | `+6.7e-04` | quadratico 1.97 | -- |
| `0` | `0.1` | `1` | S4 | `0.01` | `-0.12577` *(`+0.15659`)* | -- | `+4.9e-03` | quadratico 1.97 | -- |
| `0` | `0.1` | `1` | S4 | `0.1` | `-0.03971` *(`+0.15659`)* | -- | `+2.4e-02` | quadratico 1.97 | -- |
| `0` | `0.3` | `0` | S1 | `1e-08` | `-0.45798` *(`-0.45798`)* | `0.7701` | -- | -- | -- |
| `0` | `0.3` | `0` | S1 | `0.0001` | `-0.45798` *(`-0.45798`)* | `0.7701` | `+8.9e-12` | quadratico 1.97 | `1.258` |
| `0` | `0.3` | `0` | S1 | `0.001` | `-0.45798` *(`-0.45798`)* | `0.7701` | `+3.1e-09` | quadratico 1.97 | `1.258` |
| `0` | `0.3` | `0` | S1 | `0.01` | `-0.45795` *(`-0.45798`)* | `0.7700` | `+3.6e-08` | quadratico 2.00 | `1.258` |
| `0` | `0.3` | `0` | S1 | `0.1` | `-0.45501` *(`-0.45798`)* | `0.7676` | `+6.1e-03` | altro 1.70 | `1.254` |
| `0` | `0.3` | `0` | S3 | `0.0001` | `-2.92114` *(`-0.45798`)* | `1.9448` | `+1.2e-01` | quadratico 1.97 | `3.177` |
| `0` | `0.3` | `0` | S3 | `0.001` | `-2.23091` *(`-0.45798`)* | `1.6996` | `+1.2e-01` | quadratico 1.97 | `2.776` |
| `0` | `0.3` | `0` | S3 | `0.01` | `-1.54549` *(`-0.45798`)* | `1.4146` | `+1.2e-01` | quadratico 1.97 | `2.311` |
| `0` | `0.3` | `0` | S3 | `0.1` | `-0.90462` *(`-0.45798`)* | `1.0823` | `+1.2e-01` | quadratico 1.97 | `1.768` |
| `0` | `0.3` | `0` | S4 | `1e-08` | `-1.40045` *(`-0.45798`)* | `1.3466` | -- | -- | -- |
| `0` | `0.3` | `0` | S4 | `0.0001` | `-1.39512` *(`-0.45798`)* | `1.3440` | `+3.2e-03` | quadratico 1.85 | `2.196` |
| `0` | `0.3` | `0` | S4 | `0.001` | `-1.37754` *(`-0.45798`)* | `1.3356` | `+1.3e-02` | quadratico 1.97 | `2.182` |
| `0` | `0.3` | `0` | S4 | `0.01` | `-1.30507` *(`-0.45798`)* | `1.2999` | `+4.2e-02` | quadratico 1.97 | `2.124` |
| `0` | `0.3` | `0` | S4 | `0.1` | `-1.04690` *(`-0.45798`)* | `1.1643` | `+9.9e-02` | quadratico 1.97 | `1.902` |
| `0` | `0.3` | `1` | S1 | `1e-08` | `+0.45798` *(`+0.45798`)* | `0.7701` | -- | -- | -- |
| `0` | `0.3` | `1` | S1 | `0.0001` | `+0.45798` *(`+0.45798`)* | `0.7701` | `+1.5e-10` | quadratico 1.97 | `1.258` |
| `0` | `0.3` | `1` | S1 | `0.001` | `+0.45798` *(`+0.45798`)* | `0.7701` | `+1.6e-11` | quadratico 1.97 | `1.258` |
| `0` | `0.3` | `1` | S1 | `0.01` | `+0.45801` *(`+0.45798`)* | `0.7701` | `+1.9e-11` | quadratico 1.97 | `1.258` |
| `0` | `0.3` | `1` | S1 | `0.1` | `+0.46095` *(`+0.45798`)* | `0.7726` | `+1.6e-03` | quadratico 1.97 | `1.262` |
| `0` | `0.3` | `1` | S3 | `0.0001` | `-2.00518` *(`+0.45798`)* | -- | `+2.1e-01` | quadratico 1.97 | -- |
| `0` | `0.3` | `1` | S3 | `0.001` | `-1.31494` *(`+0.45798`)* | -- | `+2.1e-01` | quadratico 1.97 | -- |
| `0` | `0.3` | `1` | S3 | `0.01` | `-0.62952` *(`+0.45798`)* | -- | `+2.1e-01` | quadratico 1.97 | -- |
| `0` | `0.3` | `1` | S3 | `0.1` | `+0.01134` *(`+0.45798`)* | `0.1212` | `+1.7e-01` | quadratico 1.97 | `0.198` |
| `0` | `0.3` | `1` | S4 | `1e-08` | `-0.48448` *(`+0.45798`)* | -- | -- | -- | -- |
| `0` | `0.3` | `1` | S4 | `0.0001` | `-0.47915` *(`+0.45798`)* | -- | `+5.2e-04` | quadratico 1.97 | -- |
| `0` | `0.3` | `1` | S4 | `0.001` | `-0.46158` *(`+0.45798`)* | -- | `+3.2e-03` | quadratico 1.97 | -- |
| `0` | `0.3` | `1` | S4 | `0.01` | `-0.38910` *(`+0.45798`)* | -- | `+1.7e-02` | quadratico 1.97 | -- |
| `0` | `0.3` | `1` | S4 | `0.1` | `-0.13093` *(`+0.45798`)* | -- | `+9.5e-02` | quadratico 1.97 | -- |
| `0` | `0.5` | `0` | S1 | `1e-08` | `-0.72273` *(`-0.72273`)* | `0.7391` | -- | -- | -- |
| `0` | `0.5` | `0` | S1 | `0.0001` | `-0.72273` *(`-0.72273`)* | `0.7391` | `+1.5e-11` | quadratico 1.97 | `1.164` |
| `0` | `0.5` | `0` | S1 | `0.001` | `-0.72273` *(`-0.72273`)* | `0.7391` | `+2.3e-09` | quadratico 1.97 | `1.164` |
| `0` | `0.5` | `0` | S1 | `0.01` | `-0.72268` *(`-0.72273`)* | `0.7391` | `+5.2e-11` | quadratico 2.01 | `1.164` |
| `0` | `0.5` | `0` | S1 | `0.1` | `-0.71778` *(`-0.72273`)* | `0.7366` | `+1.0e-02` | altro 1.70 | `1.160` |
| `0` | `0.5` | `0` | S3 | `0.0001` | `+1.45518` *(`-0.72273`)* | -- | `+2.0e-01` | quadratico 1.97 | -- |
| `0` | `0.5` | `0` | S3 | `0.001` | `+2.60557` *(`-0.72273`)* | -- | `+2.0e-01` | quadratico 1.97 | -- |
| `0` | `0.5` | `0` | S3 | `0.01` | `-2.53525` *(`-0.72273`)* | `1.3843` | `+2.0e-01` | quadratico 1.97 | `2.180` |
| `0` | `0.5` | `0` | S3 | `0.1` | `-1.46714` *(`-0.72273`)* | `1.0531` | `+2.0e-01` | quadratico 1.97 | `1.658` |
| `0` | `0.5` | `0` | S4 | `1e-08` | `-2.29351` *(`-0.72273`)* | `1.3167` | -- | -- | -- |
| `0` | `0.5` | `0` | S4 | `0.0001` | `-2.28463` *(`-0.72273`)* | `1.3141` | `+5.4e-03` | quadratico 1.85 | `2.069` |
| `0` | `0.5` | `0` | S4 | `0.001` | `-2.25534` *(`-0.72273`)* | `1.3057` | `+2.2e-02` | quadratico 1.97 | `2.056` |
| `0` | `0.5` | `0` | S4 | `0.01` | `-2.13455` *(`-0.72273`)* | `1.2702` | `+7.0e-02` | quadratico 1.97 | `2.000` |
| `0` | `0.5` | `0` | S4 | `0.1` | `-1.70426` *(`-0.72273`)* | `1.1350` | `+1.7e-01` | quadratico 1.97 | `1.787` |
| `0` | `0.5` | `1` | S1 | `1e-08` | `+0.72273` *(`+0.72273`)* | `0.7391` | -- | -- | -- |
| `0` | `0.5` | `1` | S1 | `0.0001` | `+0.72273` *(`+0.72273`)* | `0.7391` | `+1.5e-11` | quadratico 1.97 | `1.164` |
| `0` | `0.5` | `1` | S1 | `0.001` | `+0.72273` *(`+0.72273`)* | `0.7391` | `+5.5e-12` | quadratico 1.97 | `1.164` |
| `0` | `0.5` | `1` | S1 | `0.01` | `+0.72278` *(`+0.72273`)* | `0.7392` | `+3.9e-08` | quadratico 1.97 | `1.164` |
| `0` | `0.5` | `1` | S1 | `0.1` | `+0.72768` *(`+0.72273`)* | `0.7417` | `+2.8e-03` | quadratico 1.97 | `1.168` |
| `0` | `0.5` | `1` | S3 | `0.0001` | `+2.90065` *(`+0.72273`)* | `1.4807` | `+3.5e-01` | quadratico 1.97 | `2.331` |
| `0` | `0.5` | `1` | S3 | `0.001` | `-2.23214` *(`+0.72273`)* | -- | `+3.5e-01` | quadratico 1.97 | -- |
| `0` | `0.5` | `1` | S3 | `0.01` | `-1.08978` *(`+0.72273`)* | -- | `+3.4e-01` | quadratico 1.97 | -- |
| `0` | `0.5` | `1` | S3 | `0.1` | `-0.02167` *(`+0.72273`)* | -- | `+2.9e-01` | quadratico 1.97 | -- |
| `0` | `0.5` | `1` | S4 | `1e-08` | `-0.84804` *(`+0.72273`)* | -- | -- | -- | -- |
| `0` | `0.5` | `1` | S4 | `0.0001` | `-0.83916` *(`+0.72273`)* | -- | `+1.5e-03` | quadratico 1.97 | -- |
| `0` | `0.5` | `1` | S4 | `0.001` | `-0.80987` *(`+0.72273`)* | -- | `+6.2e-03` | quadratico 1.97 | -- |
| `0` | `0.5` | `1` | S4 | `0.01` | `-0.68908` *(`+0.72273`)* | -- | `+3.1e-02` | quadratico 1.97 | -- |
| `0` | `0.5` | `1` | S4 | `0.1` | `-0.25879` *(`+0.72273`)* | -- | `+2.0e-01` | quadratico 1.97 | -- |
| `0.5` | `0.1` | `0` | S1 | `1e-08` | `-0.16445` *(`-0.16445`)* | `0.7837` | -- | -- | -- |
| `0.5` | `0.1` | `0` | S1 | `0.0001` | `-0.16445` *(`-0.16445`)* | `0.7837` | `+1.6e-10` | quadratico 1.97 | `1.306` |
| `0.5` | `0.1` | `0` | S1 | `0.001` | `-0.16445` *(`-0.16445`)* | `0.7837` | `+1.5e-11` | quadratico 1.97 | `1.306` |
| `0.5` | `0.1` | `0` | S1 | `0.01` | `-0.16444` *(`-0.16445`)* | `0.7837` | `+1.8e-08` | quadratico 2.00 | `1.306` |
| `0.5` | `0.1` | `0` | S1 | `0.1` | `-0.16346` *(`-0.16445`)* | `0.7813` | `+2.0e-03` | altro 1.67 | `1.302` |
| `0.5` | `0.1` | `0` | S3 | `0.0001` | `-0.98550` *(`-0.16445`)* | `1.9185` | `+4.1e-02` | quadratico 1.97 | `3.196` |
| `0.5` | `0.1` | `0` | S3 | `0.001` | `-0.75542` *(`-0.16445`)* | `1.6797` | `+4.1e-02` | quadratico 1.97 | `2.799` |
| `0.5` | `0.1` | `0` | S3 | `0.01` | `-0.52695` *(`-0.16445`)* | `1.4029` | `+4.1e-02` | quadratico 1.97 | `2.337` |
| `0.5` | `0.1` | `0` | S3 | `0.1` | `-0.31333` *(`-0.16445`)* | `1.0818` | `+4.1e-02` | quadratico 1.97 | `1.802` |
| `0.5` | `0.1` | `0` | S4 | `1e-08` | `-0.47860` *(`-0.16445`)* | `1.3370` | -- | -- | -- |
| `0.5` | `0.1` | `0` | S4 | `0.0001` | `-0.47683` *(`-0.16445`)* | `1.3345` | `+1.1e-03` | quadratico 1.84 | `2.223` |
| `0.5` | `0.1` | `0` | S4 | `0.001` | `-0.47097` *(`-0.16445`)* | `1.3262` | `+4.4e-03` | quadratico 1.97 | `2.210` |
| `0.5` | `0.1` | `0` | S4 | `0.01` | `-0.44681` *(`-0.16445`)* | `1.2918` | `+1.4e-02` | quadratico 1.97 | `2.152` |
| `0.5` | `0.1` | `0` | S4 | `0.1` | `-0.36075` *(`-0.16445`)* | `1.1607` | `+3.4e-02` | quadratico 1.97 | `1.934` |
| `0.5` | `0.1` | `1` | S1 | `1e-08` | `+0.16428` *(`+0.16428`)* | `0.7835` | -- | -- | -- |
| `0.5` | `0.1` | `1` | S1 | `0.0001` | `+0.16428` *(`+0.16428`)* | `0.7835` | `+1.1e-10` | quadratico 1.97 | `1.305` |
| `0.5` | `0.1` | `1` | S1 | `0.001` | `+0.16428` *(`+0.16428`)* | `0.7835` | `+3.4e-11` | quadratico 1.97 | `1.305` |
| `0.5` | `0.1` | `1` | S1 | `0.01` | `+0.16429` *(`+0.16428`)* | `0.7835` | `+5.0e-11` | quadratico 1.97 | `1.305` |
| `0.5` | `0.1` | `1` | S1 | `0.1` | `+0.16527` *(`+0.16428`)* | `0.7859` | `+5.5e-04` | quadratico 1.97 | `1.309` |
| `0.5` | `0.1` | `1` | S3 | `0.0001` | `-0.65678` *(`+0.16428`)* | -- | `+5.3e-02` | quadratico 1.97 | -- |
| `0.5` | `0.1` | `1` | S3 | `0.001` | `-0.42670` *(`+0.16428`)* | -- | `+5.3e-02` | quadratico 1.97 | -- |
| `0.5` | `0.1` | `1` | S3 | `0.01` | `-0.19823` *(`+0.16428`)* | -- | `+5.1e-02` | quadratico 1.97 | -- |
| `0.5` | `0.1` | `1` | S3 | `0.1` | `+0.01539` *(`+0.16428`)* | `0.2398` | `+2.7e-02` | quadratico 1.97 | `0.400` |
| `0.5` | `0.1` | `1` | S4 | `1e-08` | `-0.14988` *(`+0.16428`)* | -- | -- | -- | -- |
| `0.5` | `0.1` | `1` | S4 | `0.0001` | `-0.14810` *(`+0.16428`)* | -- | `+3.1e-10` | quadratico 1.97 | -- |
| `0.5` | `0.1` | `1` | S4 | `0.001` | `-0.14225` *(`+0.16428`)* | -- | `+1.2e-03` | quadratico 1.97 | -- |
| `0.5` | `0.1` | `1` | S4 | `0.01` | `-0.11809` *(`+0.16428`)* | -- | `+6.0e-03` | quadratico 1.97 | -- |
| `0.5` | `0.1` | `1` | S4 | `0.1` | `-0.03203` *(`+0.16428`)* | -- | `+2.0e-02` | quadratico 1.97 | -- |
| `0.5` | `0.3` | `0` | S1 | `1e-08` | `-0.48367` *(`-0.48367`)* | `0.7694` | -- | -- | -- |
| `0.5` | `0.3` | `0` | S1 | `0.0001` | `-0.48367` *(`-0.48367`)* | `0.7694` | `+8.9e-12` | quadratico 1.97 | `1.257` |
| `0.5` | `0.3` | `0` | S1 | `0.001` | `-0.48367` *(`-0.48367`)* | `0.7694` | `+7.6e-10` | quadratico 1.97 | `1.257` |
| `0.5` | `0.3` | `0` | S1 | `0.01` | `-0.48364` *(`-0.48367`)* | `0.7694` | `+7.5e-10` | quadratico 2.01 | `1.257` |
| `0.5` | `0.3` | `0` | S1 | `0.1` | `-0.48070` *(`-0.48367`)* | `0.7671` | `+6.1e-03` | altro 1.67 | `1.253` |
| `0.5` | `0.3` | `0` | S3 | `0.0001` | `-2.94684` *(`-0.48367`)* | `1.8992` | `+1.2e-01` | quadratico 1.97 | `3.102` |
| `0.5` | `0.3` | `0` | S3 | `0.001` | `-2.25660` *(`-0.48367`)* | `1.6620` | `+1.2e-01` | quadratico 1.97 | `2.715` |
| `0.5` | `0.3` | `0` | S3 | `0.01` | `-1.57118` *(`-0.48367`)* | `1.3868` | `+1.2e-01` | quadratico 1.97 | `2.265` |
| `0.5` | `0.3` | `0` | S3 | `0.1` | `-0.93031` *(`-0.48367`)* | `1.0671` | `+1.2e-01` | quadratico 1.97 | `1.743` |
| `0.5` | `0.3` | `0` | S4 | `1e-08` | `-1.42614` *(`-0.48367`)* | `1.3212` | -- | -- | -- |
| `0.5` | `0.3` | `0` | S4 | `0.0001` | `-1.42081` *(`-0.48367`)* | `1.3187` | `+3.3e-03` | quadratico 1.84 | `2.154` |
| `0.5` | `0.3` | `0` | S4 | `0.001` | `-1.40324` *(`-0.48367`)* | `1.3106` | `+1.3e-02` | quadratico 1.97 | `2.141` |
| `0.5` | `0.3` | `0` | S4 | `0.01` | `-1.33076` *(`-0.48367`)* | `1.2763` | `+4.3e-02` | quadratico 1.97 | `2.085` |
| `0.5` | `0.3` | `0` | S4 | `0.1` | `-1.07259` *(`-0.48367`)* | `1.1458` | `+1.0e-01` | quadratico 1.97 | `1.872` |
| `0.5` | `0.3` | `1` | S1 | `1e-08` | `+0.47890` *(`+0.47890`)* | `0.7676` | -- | -- | -- |
| `0.5` | `0.3` | `1` | S1 | `0.0001` | `+0.47890` *(`+0.47890`)* | `0.7676` | `+1.3e-10` | quadratico 1.97 | `1.254` |
| `0.5` | `0.3` | `1` | S1 | `0.001` | `+0.47890` *(`+0.47890`)* | `0.7676` | `+2.0e-09` | quadratico 1.97 | `1.254` |
| `0.5` | `0.3` | `1` | S1 | `0.01` | `+0.47893` *(`+0.47890`)* | `0.7677` | `+3.2e-10` | quadratico 1.97 | `1.254` |
| `0.5` | `0.3` | `1` | S1 | `0.1` | `+0.48187` *(`+0.47890`)* | `0.7700` | `+1.6e-03` | quadratico 1.97 | `1.258` |
| `0.5` | `0.3` | `1` | S3 | `0.0001` | `-1.98426` *(`+0.47890`)* | -- | `+1.7e-01` | quadratico 1.97 | -- |
| `0.5` | `0.3` | `1` | S3 | `0.001` | `-1.29403` *(`+0.47890`)* | -- | `+1.7e-01` | quadratico 1.97 | -- |
| `0.5` | `0.3` | `1` | S3 | `0.01` | `-0.60861` *(`+0.47890`)* | -- | `+1.6e-01` | quadratico 1.97 | -- |
| `0.5` | `0.3` | `1` | S3 | `0.1` | `+0.03226` *(`+0.47890`)* | `0.1992` | `+1.1e-01` | quadratico 1.97 | `0.325` |
| `0.5` | `0.3` | `1` | S4 | `1e-08` | `-0.46356` *(`+0.47890`)* | -- | -- | -- | -- |
| `0.5` | `0.3` | `1` | S4 | `0.0001` | `-0.45824` *(`+0.47890`)* | -- | `+3.3e-04` | quadratico 1.97 | -- |
| `0.5` | `0.3` | `1` | S4 | `0.001` | `-0.44066` *(`+0.47890`)* | -- | `+4.1e-03` | quadratico 1.97 | -- |
| `0.5` | `0.3` | `1` | S4 | `0.01` | `-0.36819` *(`+0.47890`)* | -- | `+1.9e-02` | quadratico 1.97 | -- |
| `0.5` | `0.3` | `1` | S4 | `0.1` | `-0.11002` *(`+0.47890`)* | -- | `+6.3e-02` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `0` | S1 | `1e-08` | `-0.77273` *(`-0.77273`)* | `0.7374` | -- | -- | -- |
| `0.5` | `0.5` | `0` | S1 | `0.0001` | `-0.77273` *(`-0.77273`)* | `0.7374` | `+1.5e-11` | quadratico 1.97 | `1.161` |
| `0.5` | `0.5` | `0` | S1 | `0.001` | `-0.77273` *(`-0.77273`)* | `0.7374` | `+2.1e-11` | quadratico 1.97 | `1.161` |
| `0.5` | `0.5` | `0` | S1 | `0.01` | `-0.77268` *(`-0.77273`)* | `0.7374` | `+1.7e-11` | quadratico 2.01 | `1.161` |
| `0.5` | `0.5` | `0` | S1 | `0.1` | `-0.76778` *(`-0.77273`)* | `0.7351` | `+1.0e-02` | altro 1.66 | `1.157` |
| `0.5` | `0.5` | `0` | S3 | `0.0001` | `+1.40518` *(`-0.77273`)* | -- | `+2.1e-01` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `0` | S3 | `0.001` | `+2.55558` *(`-0.77273`)* | -- | `+2.1e-01` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `0` | S3 | `0.01` | `-2.58524` *(`-0.77273`)* | `1.3488` | `+2.1e-01` | quadratico 1.97 | `2.124` |
| `0.5` | `0.5` | `0` | S3 | `0.1` | `-1.51713` *(`-0.77273`)* | `1.0333` | `+2.1e-01` | quadratico 1.97 | `1.627` |
| `0.5` | `0.5` | `0` | S4 | `1e-08` | `-2.34350` *(`-0.77273`)* | `1.2842` | -- | -- | -- |
| `0.5` | `0.5` | `0` | S4 | `0.0001` | `-2.33463` *(`-0.77273`)* | `1.2818` | `+5.5e-03` | quadratico 1.84 | `2.018` |
| `0.5` | `0.5` | `0` | S4 | `0.001` | `-2.30534` *(`-0.77273`)* | `1.2737` | `+2.2e-02` | quadratico 1.97 | `2.005` |
| `0.5` | `0.5` | `0` | S4 | `0.01` | `-2.18454` *(`-0.77273`)* | `1.2399` | `+7.1e-02` | quadratico 1.97 | `1.952` |
| `0.5` | `0.5` | `0` | S4 | `0.1` | `-1.75426` *(`-0.77273`)* | `1.1111` | `+1.7e-01` | quadratico 1.97 | `1.749` |
| `0.5` | `0.5` | `1` | S1 | `1e-08` | `+0.74975` *(`+0.74975`)* | `0.7317` | -- | -- | -- |
| `0.5` | `0.5` | `1` | S1 | `0.0001` | `+0.74975` *(`+0.74975`)* | `0.7317` | `+3.1e-10` | quadratico 1.97 | `1.152` |
| `0.5` | `0.5` | `1` | S1 | `0.001` | `+0.74975` *(`+0.74975`)* | `0.7317` | `+4.0e-09` | quadratico 1.97 | `1.152` |
| `0.5` | `0.5` | `1` | S1 | `0.01` | `+0.74980` *(`+0.74975`)* | `0.7318` | `+1.0e-08` | quadratico 1.97 | `1.152` |
| `0.5` | `0.5` | `1` | S1 | `0.1` | `+0.75470` *(`+0.74975`)* | `0.7342` | `+2.7e-03` | quadratico 1.97 | `1.156` |
| `0.5` | `0.5` | `1` | S3 | `0.0001` | `+2.92766` *(`+0.74975`)* | `1.4460` | `+3.0e-01` | quadratico 1.97 | `2.277` |
| `0.5` | `0.5` | `1` | S3 | `0.001` | `-2.20513` *(`+0.74975`)* | -- | `+3.0e-01` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `1` | S3 | `0.01` | `-1.06276` *(`+0.74975`)* | -- | `+2.9e-01` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `1` | S3 | `0.1` | `+0.00535` *(`+0.74975`)* | `0.0618` | `+2.2e-01` | quadratico 1.97 | `0.097` |
| `0.5` | `0.5` | `1` | S4 | `1e-08` | `-0.82102` *(`+0.74975`)* | -- | -- | -- | -- |
| `0.5` | `0.5` | `1` | S4 | `0.0001` | `-0.81215` *(`+0.74975`)* | -- | `+4.2e-10` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `1` | S4 | `0.001` | `-0.78285` *(`+0.74975`)* | -- | `+6.7e-03` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `1` | S4 | `0.01` | `-0.66206` *(`+0.74975`)* | -- | `+3.3e-02` | quadratico 1.97 | -- |
| `0.5` | `0.5` | `1` | S4 | `0.1` | `-0.23178` *(`+0.74975`)* | -- | `+1.1e-01` | quadratico 1.97 | -- |

### 6.3 LA LETTURA *(tre righe)*

1. ### **UN SOLO MODO SENZA MASSA, e SOLO A `s = 1` ESATTO:** ### **a `Gamma`, attraverso la fase `pi`** *(le bande a `+-pi s` si toccano quando `-pi = +pi`; il salto `2 pi (1 - s)`, esponente `1.000`)*, ### **lineare,
   isotropo, a `0.7071 s = 1/sqrt2` -- uguale a `v_max`** *(che tende a `0.70711` con esponente `~1`)*. ### **La coppia a `K` resta MASSIVA anche a `s = 1`** *(il salto `2 pi/3`)*; ### **la previsione del guardiano** *(il
   salto a `K` si chiude)* ### **e' smentita.**
2. ### **LA MONETA NON APRE MODI SENZA MASSA:** ### **nessun ramo lineare a `s <= 0.9` per nessuna `eps` fino a `pi/2`;** ### **a `s` piccolo `v_b/v_max` resta `1.31`** *(la moneta conta come `eps^2`)*, ### **a `s 0.9` scende con
   `eps`** *(`0.864` a `eps 0`, `0.662` a `eps 1` sulla banda alta)*.
3. ### **LA VESTIZIONE NON CAMBIA L'INERZIA, CAMBIA L'ENERGIA A RIPOSO:** ### **`omega''` e' quello nudo a ogni forma e `x`; `omega(0)` si sposta** *(con `S1`: dell'`1%%` a `x 0.1`, su o giu' secondo la banda)*; ### **`S1` stabile fino a
   `x 1e-2`, instabile a `x 0.1`; `S3` e `S4` instabili quasi ovunque** *(`S4` stabile solo sulla banda alta a `eps 0.5`, `x 1e-4`, dove `v_b` non e' definita)*; ### **nessun suono** *(il ramo per `0` quadratico)*.

### 6.4 LA DEFINIZIONE DI LUCA *(la `c` = un arco per tick)*

### **NON si realizza:** ### **l'unico modo senza massa va a `1/sqrt2` archi per tick** *(`0.7071`)*, ### **e solo a `s = 1` esatto; a `s < 1` e' massivo con salto `2 pi (1 - s)`.** ### **A `s = 1` la sua velocita' coincide con `v_max`: il
modello ha, al limite, UNA velocita' per il modo senza massa e per i segnali, `1/sqrt2`.**

### 6.5 LA VESTIZIONE *(l'osservazione di Luca)*

### **Il vuoto NON cambia l'inerzia della particella** *(`omega''` identico)*: ### **cambia la sua energia a riposo, e cosi' `v_b`** *(`v_b ~ sqrt(omega(0))`)*. ### **Con `S1`** *(la sola stabile)* ### **lo spostamento e' piccolo**
*(`v_b` `+-0.3%%` a `x 0.1`)* ### **e il verso dipende dalla banda: la vestizione NON porta `v_b` a `v_max`.** ### **Con `S3` e `S4` `v_b` cambia molto, ma sono instabili.**

### 6.6 LA TENSIONE COL PRINCIPIO DI EQUIVALENZA

### **Sul quadrato il principio di equivalenza e' violato d'ordine `1` nel regime `s -> 1`** *(`05055fc6`)*: ### **sui triangoli NON e' ancora misurato.** ### **Il modo senza massa nasce solo a `s = 1`: se la `c` del modello
e' quella, la si ha proprio dove sul quadrato l'equivalenza cade.**

### 6.7 CHE COSA RESTA PER IL CAMPO `U(1)` E PER LE ONDE DI `cs`

### **Nella camminata a `s < 1` NON c'e' un modo senza massa** *(nudo, con la moneta, vestito)*: ### **la `c` del modello, se c'e', deve venire da un ALTRO settore: l'onda del campo `U(1)` sugli archi** *(la luce vera, oggi senza
dinamica)* ### **o le onde di `cs`** *(quando il canale di `cs` sara' aperto: le onde gravitazionali del modello)*.
