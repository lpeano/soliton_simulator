# I TRIANGOLI, PRIMO GRADINO: GLI SPETTRI, DOVE STA LA FISICA DI BASSA ENERGIA, LA GRAVITA' DI HAMILTON

> **Il mandato:** di Luca, «SOLO TRIANGOLI» *(la parte `0` in `406b32f0`: [[DECISIONE-SOLO-TRIANGOLI]])*. ### **Una MISURA su spettri, in memoria: non sceglie niente.** ### **`leggi.yaml`,
> l'impronta `2e7f795d2a52fbe7` e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE; git `e96ca41a`)*. ### **Importati, non copiati:** `_triangoli` *(`matrice_tick`,
> `ruota60`, `scarto_c6`, `bipartito`, `toro_spostamenti`, `camminata`, `TRIANGOLI`, `EPS_MONETA`)*, `_zero_simmetrico.convenzione_simmetrica`, `_segno_gravita.convenzione_lambda`,
> `_scala_e_zero` *(`H_eff`, `esponente`, `punti_fini`)*, `_gravita_collettiva.dproprio`, `_moneta_massa.fit_massa`.

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica.**
2. **Il gradino:** ### **`(a)` i controlli** *(la simmetria a `60` gradi, un pezzo solo, la griglia non bipartita)*; ### **`(b)` dove sta il salto della coppia massiva e che cosa vale li'**; ### **`(c)` Hamilton.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **Il lato `48`** *(divisibile per `3` e per `2`: `K` e `M` sono punti della griglia)*, ### **il cammino nella zona e le griglie in `s` sono SCELTE DI
   MISURA, dichiarate.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` uniforme** *(a `cs` uniforme `s = dtau`: `matrice_tick` prende `dtau`)*; ### **il segno della forza e' una delle domande.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **sui triangoli, dove stanno i modi leggeri, e cadono nel verso giusto?**

## 1. LA GEOMETRIA *(dal codice)*

- ### **`_triangoli.TRIANGOLI`: gli spostamenti `(1, 0)`, `(0, 1)`, `(1, 1)`, i versori a `0`, `120`, `60` gradi**: ### **`a1`, `a2` con l'angolo di `120` gradi, e `a1 + a2` il terzo vicino** *(grado `6`)*.
  ### **`k` sulla griglia `L x L`: le fasi per legame `theta_1 = 2 pi m_1/L`, `theta_2 = 2 pi m_2/L`.** ### **I PUNTI SPECIALI:** ### **`Gamma = (0, 0)`; `K = (2 pi/3, 2 pi/3)`, `K' = (4 pi/3, 4 pi/3)`; `M =
  (pi, 0)`, `(0, pi)`, `(pi, pi)`.** ### **Il tensore della curvatura in coordinate cartesiane: `H_k = J^T H_theta J`, `J` con le righe `a1 = (1, 0)`, `a2 = (-1/2, sqrt3/2)`.**
- ### **La cella: `12` complessi di materia** *(`4 d`, `d = 3`)* ### **e `6` di vuoto** *(`_triangoli.celle`)*.

## 2. COSA HA MOSTRATO L'ESPLORAZIONE IN MEMORIA *(nessun file del repo scritto; i numeri li ristampa lo strumento)*

- ### **`eps 0, s 0.3`, zero simmetrico, lato `48`:** ### **a `Gamma` i livelli `+-0.9425 = +-pi s`** *(con molteplicita')* ### **piu' `0` e `-pi s`; a `M` `+-0.530`; a `K` e `K'` `+-0.458`**; ### **i livelli
  `0` e `-pi s` restano su tutta la zona: bande PIATTE.** ### **La simmetria a `60` gradi: `1.4e-15`.**
- ### ⚠ **IL «SALTO MINIMO FRA LIVELLI DISTINTI» su tutta la griglia NON e' fisica:** ### **viene vicino a `Gamma`** *(`1e-5` a `m = (0, 47)`)* ### **dalla separazione lenta dei livelli DEGENERI a `Gamma`.**
  ### **Il salto va misurato sulla COPPIA MASSIVA, seguita banda per banda.**

## 3. IL METODO

- ### **LE BANDE:** ### **`matrice_tick(TRIANGOLI, 48, s)`** *(`eps` in `_triangoli.EPS_MONETA`, in memoria)*, ### **il blocco della materia `12 x 12`**, ### **seguite per sovrapposizione dei vettori propri lungo
  il cammino `Gamma -> K -> M -> Gamma`** *(e `Gamma -> K'`)*. ### **La COPPIA MASSIVA:** ### **le bande che a `Gamma` stanno a `+- pi s`** *(nella simmetrica)* ### **e che DISPERDONO** *(variazione lungo il
  cammino `> 1e-3`)*; ### **il loro SALTO lungo il cammino** *(la distanza fra le due)*, ### **il minimo e DOVE sta.** ### **A `eps > 0`: la coppia che si apre da quella di `eps 0`** *(la banda dispersiva
  piu' vicina a ciascuna di `eps 0` a `Gamma`)*.
- ### **I PUNTI SENZA MASSA a `eps 0`:** ### **dove il salto della coppia si annulla** *(`< 1e-6`)*.
- ### **I LIVELLI ai punti speciali, con la molteplicita'**, ### **e la simmetria a `60` gradi** *(`scarto_c6`)*.
- ### **AL PUNTO DEL SALTO MINIMO, per ciascuna banda della coppia:** ### **la fase continua da `s` piccolo** *(il blocco a quel `k` al lato `6`, che contiene `Gamma`, `K`, `K'`, `M`: lo stesso al bit che al lato `48`, verificato; un cammino fine in `s` col passo di `_scala_e_zero.punti_fini`, l'autovalore seguito per FASE PIU' VICINA)*, ### **`salto/s`, la fase al centro della
  coppia `/s`, la curvatura** *(il tensore `2 x 2` dalle fasi esatte ai vicini `+-1`, `+-2` passi, convertito in cartesiano: isotropo?)*, ### **`v`** *(il fit lungo `theta_1`)*, ### **`E0 = omega/s`, `M = omega''/s`,
  `D`**, ### **`a_H/a_RG = s (omega''/v^2) d omega/ds`** *(lungo `theta_1`: il rapporto non dipende dalla scala della direzione)* ### **a `lambda 0` e `1/2`**, ### **e `lambda*`.**
- ### **IL PASSO:** ### **un pezzo solo** *(`_triangoli.camminata` avvolta in memoria perche' salti tutti gli altri pezzi)*: ### **`delta(s)` a `Gamma` e a `k = (2 pi/16, 0)`**; ### **e `delta(s)` del passo intero, l'esponente su
  `s <= 0.3`** *(contro `s - 0.02` e contro `s`)*.
- ### **`eps` in `(0, 0.25, 0.5, 1.0)`, `s` in `(0.05, 0.1, 0.3, 0.5, 0.9)`.**

## 4. LE PREVISIONI *(prima dei numeri)*

- ### **IL SALTO MINIMO DELLA COPPIA: a `K` e `K'`** *(l'esplorazione)*, ### **NON NULLO a `eps 0`: sui triangoli NESSUN punto senza massa per la coppia** *(sul quadrato si toccava a `(pi, pi)`; i triangoli
  non sono bipartiti)*.
- ### **LA CURVATURA A `K` E' ISOTROPA** *(`K` e' fisso sotto la rotazione di `120` gradi: un tensore simmetrico invariante per `120` gradi e' un multiplo dell'identita')* ### **-- NIENTE SELLA**; ### **a `M` NO**
  *(solo la simmetria a `180` gradi)*.
- ### **`lambda* = 1/2` A `K`** *(due bande con lo stesso salto e curvature opposte: lo stesso argomento di `e31366ec`)*.
- ### **`delta(s)`: esponente `2`** *(il palindromo; `05055fc6`)*.
- ### **Il segno di `E0 M` e di `a_H/a_RG` a `K`: NON lo prevedo.**

## 5. I CRITERI, FISSATI ORA *(dal mandato)*

- ### **DEVE PASSARE:** ### **lo spettro invariante per `60` gradi entro `1e-12`** *(`scarto_c6`, ogni `eps` e `s`)*.
- ### **DEVE PASSARE:** ### **un pezzo solo, `delta(s) < 1e-12`.**
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«la griglia a triangoli e' bipartita»** *(`bipartito` da' `False` e un ciclo dispari, stampato)*.
- ### **PUO' FALLIRE:** ### **l'esponente di `delta` fra `1.8` e `2.2`** *(contro `s`)*.
- ### **PUO' FALLIRE:** ### **`lambda* = 1/2` entro `1e-6` al punto del salto minimo.**
- ### **DI SERVIZIO:** ### **il blocco al lato `6` = al lato `48` ai punti speciali, entro `1e-12`.**
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE: le tabelle.** ### **A parte: la lettura in tre righe; dove sta la fisica di bassa energia sui triangoli; quali risultati del quadrato hanno un
  corrispondente qui e quali no.**

### 📝 **ANNOTAZIONE 1** *(prima della corsa dello strumento committato, nel commit dello strumento)*: ### **la prova a vuoto in memoria** *(`eps 0` e `0.5`, `s 0.3`; il `jsonl` negli appunti)*
### **ha mostrato tre cose del MIO METODO, corrette prima della corsa, e dei numeri che dichiaro:**
- ### **(a) LA DERIVATA MISTA:** ### **col solo stencil `+-1` sulla diagonale** *(secondo ordine)* ### **la curvatura a `K` usciva anisotropa dell'`1.5%`**; ### **ora `h12` viene dalla derivata seconda
  lungo `(1, 1)` col Richardson** *(quarto ordine)*, ### **e «isotropa» vuol dire entro `1e-3` relativo** *(l'errore numerico `O(k_1^4)`; la previsione resta: isotropa ESATTAMENTE per simmetria)*.
- ### **(b) UNA BANDA PIATTA al punto del salto** *(a `eps 0.5` il salto minimo e' a `Gamma`, `0.013`, fra il livello spaccato dalla moneta e uno PIATTO li': curvatura `0`, `v 0`, e un `a_H/a_RG ~
  1e31`)*: ### **si scrive «PIATTA» e Hamilton non si calcola** *(come in `9fbfede3`)*; ### **`lambda*` solo per coppie non piatte.**
- ### **(c) A `Gamma`, `K`, `K'` UNA BANDA VERA E' ISOTROPA** *(fissi per `120` gradi)*: ### **se la curvatura misurata li' non lo e' oltre `1e-3`, la tracciatura ai vicini ha cambiato banda**
  *(a `eps 0.5, Gamma`: `8.3e-2`, e `v = 6.1`, fra livelli lontani `0.013`)*: ### **si scrive «NON AFFIDABILE» e Hamilton non si calcola.**
- ### **I NUMERI VISTI** *(non li uso; le previsioni restano)*: ### **`eps 0, s 0.3`: la coppia a `K`, salto `0.916`, `lambda* = 0.50000000`, simmetrica `a_H/a_RG = +2.03` sulle due bande** *(verso
  `cs` BASSO)*; ### **oggi `+6.47` e `-2.41`**; ### **`delta`: esponente `2.12`-`2.14` contro `s`**; ### **un pezzo solo `4.3e-15`**; ### **`60` gradi `2.0e-15`.**

## 6. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_triangoli_bassa_energia.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima dei numeri;
3. la corsa, il referto, la relazione, la sezione `7`.

## 7. I RISULTATI *(scritti dopo la corsa, sotto)*

> **La corsa:** ### **strumento `csv/_triangoli_bassa_energia.py` sha1-BYTE `74be8455`** *(`fc65f1a8`)*; ### **referto `doc/referti_l2/triangoli_bassa_energia.txt` sha1-BYTE `6f54311a`, `.jsonl` `3bbff4aa`.**
> ### **Le tabelle sono GENERATE dal `.jsonl`** *(nessun numero ricopiato)*.

### 7.0 I CONTROLLI

| criterio | esito | il numero |
|---|---|---|
| DEVE FALLIRE: la griglia e' bipartita | **fallisce, come deve** | ciclo dispari `[48, 0, 47]` |
| DEVE PASSARE: `60` gradi entro `1e-12` *(sul cerchio, dopo `fc65f1a8`)* | **PASSA** | il peggiore `5.91e-15` |
| DI SERVIZIO: lato `6` = lato `48` ai punti speciali | **PASSA** | `0.00e+00` |
| DEVE PASSARE: un pezzo solo, `delta < 1e-12` | **PASSA** | il peggiore `4.31e-15` |
| PUO' FALLIRE: esponente di `delta` fra `1.8` e `2.2` *(contro `s`)* | **PASSA** | `2.140`, `2.127`, `2.123`, `2.122` |
| PUO' FALLIRE: `lambda* = 1/2` entro `1e-6` | ### **FALLISCE** | ### **`0.50000000` a `eps 0`; a `eps > 0` da `0.50003` a `0.50162`** *(tabella 7.1)* |

### 7.1 LA COPPIA DISPERSIVA PIU' STRETTA *(zero simmetrico, lato `48`)*

| `eps` | `s` | dove | salto | salto/`s` | le fasi | il centro/`s` | `lambda*` |
|---|---|---|---|---|---|---|---|
| `0` | `0.05` | K' `(32, 32)` | `0.15696` | `3.1392` | `-0.0785` `+0.0785` | `+0.0000` | `0.50000000` |
| `0` | `0.1` | K `(16, 16)` | `0.31319` | `3.1319` | `-0.1566` `+0.1566` | `+0.0000` | `0.50000000` |
| `0` | `0.3` | K `(16, 16)` | `0.91597` | `3.0532` | `-0.4580` `+0.4580` | `+0.0000` | `0.50000000` |
| `0` | `0.5` | K `(16, 16)` | `1.44547` | `2.8909` | `-0.7227` `+0.7227` | `+0.0000` | `0.50000000` |
| `0` | `0.9` | Gamma `(0, 0)` | `0.62832` | `0.6981` | `-2.8274` `+2.8274` | `-3.4907` | -- |
| `0.25` | `0.05` | K `(16, 16)` | `0.15894` | `3.1787` | `-0.0795` `+0.0795` | `-0.0001` | `0.50003066` |
| `0.25` | `0.1` | K `(16, 16)` | `0.31715` | `3.1715` | `-0.1586` `+0.1585` | `-0.0002` | `0.50012282` |
| `0.25` | `0.3` | K `(16, 16)` | `0.92789` | `3.0930` | `-0.4646` `+0.4633` | `-0.0022` | `0.50112378` |
| `0.25` | `0.5` | Gamma `(0, 0)` | `0.00777` | `0.0155` | `-1.5786` `-1.5708` | `-3.1494` | -- |
| `0.25` | `0.9` | Gamma `(0, 0)` | `0.07407` | `0.0823` | `-2.8314` `-2.7574` | `-3.1049` | -- |
| `0.5` | `0.05` | K' `(32, 32)` | `0.16472` | `3.2945` | `-0.0824` `+0.0824` | `-0.0002` | `0.50011709` |
| `0.5` | `0.1` | K `(16, 16)` | `0.32872` | `3.2872` | `-0.1644` `+0.1643` | `-0.0009` | `0.50046922` |
| `0.5` | `0.3` | Gamma `(0, 0)` | `0.01345` | `0.0448` | `-0.9641` `-0.9506` | `-3.1911` | -- |
| `0.5` | `0.5` | Gamma `(0, 0)` | `0.03062` | `0.0612` | `-1.6014` `-1.5708` | `-3.1722` | -- |
| `0.5` | `0.9` | Gamma `(0, 0)` | `0.24418` | `0.2713` | `-2.8432` `-2.5990` | `-3.0234` | -- |
| `1` | `0.05` | K' `(32, 32)` | `0.18608` | `3.7216` | `-0.0931` `+0.0930` | `-0.0006` | `0.50040404` |
| `1` | `0.1` | K' `(32, 32)` | `0.37137` | `3.7137` | `-0.1859` `+0.1854` | `-0.0026` | `0.50162143` |
| `1` | `0.3` | Gamma `(0, 0)` | `0.04919` | `0.1640` | `-1.0237` `-0.9746` | `-3.3305` | -- |
| `1` | `0.5` | Gamma `(0, 0)` | `0.11596` | `0.2319` | `-1.6868` `-1.5708` | `-3.2576` | -- |
| `1` | `0.9` | K `(16, 16)` | `0.62637` | `0.6960` | `+0.3699` `+0.9962` | `+0.7589` | -- |

### 7.2 I MODI AL PUNTO DEL SALTO *(curvatura cartesiana, `v`, e Hamilton nelle due convenzioni)*

| `eps` | `s` | punto | banda | autovalori cartesiani | anisotropia | `v` | oggi `E0` | oggi `E0 M` | oggi `D` | oggi `a_H/a_RG` | simm `E0` | simm `E0 M` | simm `a_H/a_RG` | nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.05` | K' | `0` | `-0.0196` `-0.0196` | `7.7e-04` | `0.0301` | `-4.7112` | + | `+4.85e-02` | `+6.7953` | `-1.5696` | + | `+2.2616` |  |
| `0` | `0.05` | K' | `1` | `+0.0196` `+0.0196` | `7.7e-04` | `0.0301` | `-1.5720` | - | `-4.85e-02` | `-2.2721` | `+1.5696` | + | `+2.2616` |  |
| `0` | `0.1` | K | `0` | `-0.0392` `-0.0392` | `7.7e-04` | `0.0603` | `-4.7075` | + | `+9.72e-02` | `+6.7664` | `-1.5659` | + | `+2.2415` |  |
| `0` | `0.1` | K | `1` | `+0.0392` `+0.0392` | `7.7e-04` | `0.0603` | `-1.5756` | - | `-9.72e-02` | `-2.2834` | `+1.5659` | + | `+2.2415` |  |
| `0` | `0.3` | K | `0` | `-0.1166` `-0.1165` | `7.4e-04` | `0.1816` | `-4.6682` | + | `+2.98e-01` | `+6.4694` | `-1.5266` | + | `+2.0305` |  |
| `0` | `0.3` | K | `1` | `+0.1165` `+0.1166` | `7.4e-04` | `0.1816` | `-1.6150` | - | `-2.98e-01` | `-2.4083` | `+1.5266` | + | `+2.0305` |  |
| `0` | `0.5` | K | `0` | `-0.1891` `-0.1889` | `7.1e-04` | `0.3029` | `-4.5871` | + | `+5.16e-01` | `+5.9463` | `-1.4455` | + | `+1.6310` |  |
| `0` | `0.5` | K | `1` | `+0.1889` `+0.1891` | `7.1e-04` | `0.3029` | `-1.6961` | - | `-5.16e-01` | `-2.6842` | `+1.4455` | + | `+1.6310` |  |
| `0` | `0.9` | Gamma | `0` | `-1.7153` `+1.7876` | `2.0e+00` | `0.0000` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0` | `0.9` | Gamma | `1` | `-1.6792` `-1.5346` | `8.6e-02` | `0.7905` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.25` | `0.05` | K | `0` | `-0.0194` `-0.0194` | `7.4e-04` | `0.0299` | `-4.7310` | + | `+4.60e-02` | `+6.8242` | `-1.5894` | + | `+2.2904` |  |
| `0.25` | `0.05` | K | `1` | `+0.0194` `+0.0194` | `7.4e-04` | `0.0299` | `-1.5523` | - | `-5.07e-02` | `-2.2438` | `+1.5893` | + | `+2.2899` |  |
| `0.25` | `0.1` | K | `0` | `-0.0388` `-0.0387` | `7.4e-04` | `0.0599` | `-4.7276` | + | `+9.21e-02` | `+6.7964` | `-1.5860` | + | `+2.2712` |  |
| `0.25` | `0.1` | K | `1` | `+0.0387` `+0.0388` | `7.4e-04` | `0.0599` | `-1.5561` | - | `-1.02e-01` | `-2.2559` | `+1.5855` | + | `+2.2690` |  |
| `0.25` | `0.3` | K | `0` | `-0.1149` `-0.1148` | `7.2e-04` | `0.1802` | `-4.6903` | + | `+2.83e-01` | `+6.5113` | `-1.5487` | + | `+2.0695` |  |
| `0.25` | `0.3` | K | `1` | `+0.1150` `+0.1151` | `7.2e-04` | `0.1804` | `-1.5973` | - | `-3.13e-01` | `-2.3895` | `+1.5443` | + | `+2.0496` |  |
| `0.25` | `0.5` | Gamma | `0` | `+0.0670` `+0.1766` | `6.2e-01` | `0.0048` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.25` | `0.5` | Gamma | `1` | `+0.0711` `+0.1807` | `6.1e-01` | `9.8495` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.25` | `0.9` | Gamma | `0` | `-0.0363` `+0.5052` | `1.1e+00` | `0.0000` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.25` | `0.9` | Gamma | `1` | `+0.7404` `+0.9668` | `2.3e-01` | `0.8885` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.5` | `0.05` | K' | `0` | `-0.0187` `-0.0187` | `6.7e-04` | `0.0294` | `-4.7891` | + | `+3.97e-02` | `+6.9146` | `-1.6475` | + | `+2.3768` |  |
| `0.5` | `0.05` | K' | `1` | `+0.0187` `+0.0187` | `6.7e-04` | `0.0294` | `-1.4946` | - | `-5.70e-02` | `-2.1627` | `+1.6470` | + | `+2.3747` |  |
| `0.5` | `0.1` | K | `0` | `-0.0374` `-0.0373` | `6.7e-04` | `0.0588` | `-4.7861` | + | `+7.95e-02` | `+6.8904` | `-1.6445` | + | `+2.3600` |  |
| `0.5` | `0.1` | K | `1` | `+0.0374` `+0.0374` | `6.7e-04` | `0.0588` | `-1.4988` | - | `-1.14e-01` | `-2.1770` | `+1.6428` | + | `+2.3515` |  |
| `0.5` | `0.3` | Gamma | `0` | `-0.0000` `+0.0000` | `1.1e+00` | `0.0000` | -- | -- | -- | -- | -- | -- | -- | PIATTA |
| `0.5` | `0.3` | Gamma | `1` | `+0.0947` `+0.1033` | `8.3e-02` | `6.0992` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.5` | `0.5` | Gamma | `0` | `+0.0869` `+0.1043` | `1.7e-01` | `0.0140` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.5` | `0.5` | Gamma | `1` | `+0.1273` `+0.1453` | `1.2e-01` | `11.7985` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.5` | `0.9` | Gamma | `0` | `+0.1917` `+0.2124` | `9.7e-02` | `0.0856` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `0.5` | `0.9` | Gamma | `1` | `+0.5157` `+0.5358` | `3.8e-02` | `1.6179` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `1` | `0.05` | K' | `0` | `-0.0166` `-0.0165` | `4.8e-04` | `0.0275` | `-5.0030` | + | `+2.67e-02` | `+7.3174` | `-1.8614` | + | `+2.7213` |  |
| `1` | `0.05` | K' | `1` | `+0.0165` `+0.0166` | `4.8e-04` | `0.0275` | `-1.2814` | - | `-7.78e-02` | `-1.8792` | `+1.8602` | + | `+2.7139` |  |
| `1` | `0.1` | K' | `0` | `-0.0330` `-0.0330` | `4.8e-04` | `0.0548` | `-5.0010` | + | `+5.36e-02` | `+7.3080` | `-1.8594` | + | `+2.7122` |  |
| `1` | `0.1` | K' | `1` | `+0.0330` `+0.0330` | `4.8e-04` | `0.0549` | `-1.2873` | - | `-1.56e-01` | `-1.9009` | `+1.8543` | + | `+2.6825` |  |
| `1` | `0.3` | Gamma | `0` | `-0.0236` `+0.0252` | `1.9e+00` | `0.0075` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `1` | `0.3` | Gamma | `1` | `+0.0943` `+0.0954` | `1.1e-02` | `5.2647` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `1` | `0.5` | Gamma | `0` | `+0.0924` `+0.0936` | `1.2e-02` | `0.0407` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `1` | `0.5` | Gamma | `1` | `+0.1214` `+0.1225` | `8.9e-03` | `7.3792` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `1` | `0.9` | K | `0` | `-0.0312` `-0.0308` | `1.2e-02` | `1.8022` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |
| `1` | `0.9` | K | `1` | `+0.1725` `+0.1728` | `1.6e-03` | `0.5144` | -- | -- | -- | -- | -- | -- | -- | NON AFFIDABILE |

### 7.3 `delta(s)` DEL PASSO INTERO *(il logaritmo principale, lato `16`)*

| `eps` | `k` | `0.05` | `0.1` | `0.2` | `0.3` | `0.5` | esponente contro `s - 0.02` | contro `s` |
|---|---|---|---|---|---|---|---|---|
| `0` | Gamma | `6.2e-15` | `5.7e-15` | `5.6e-15` | `5.7e-15` | `5.7e-15` | `-0.039` | `-0.047` |
| `0` | k(1,0) | `1.5e-04` | `7.0e-04` | `3.0e-03` | `7.1e-03` | `7.6e-01` | `1.716` | `2.140` |
| `0.25` | Gamma | `2.2e-04` | `1.0e-03` | `4.3e-03` | `1.0e-02` | `1.7e+00` | `1.702` | `2.122` |
| `0.25` | k(1,0) | `2.7e-04` | `1.2e-03` | `5.1e-03` | `1.2e-02` | `1.5e+00` | `1.706` | `2.127` |
| `0.5` | Gamma | `4.4e-04` | `2.0e-03` | `8.5e-03` | `2.0e-02` | `1.7e+00` | `1.702` | `2.122` |
| `0.5` | k(1,0) | `4.6e-04` | `2.1e-03` | `8.9e-03` | `2.1e-02` | `1.5e+00` | `1.703` | `2.123` |
| `1` | Gamma | `8.8e-04` | `4.0e-03` | `1.7e-02` | `4.0e-02` | `1.5e+00` | `1.702` | `2.123` |
| `1` | k(1,0) | `8.8e-04` | `4.0e-03` | `1.7e-02` | `4.0e-02` | `1.5e+00` | `1.702` | `2.122` |

### 7.4 LA LETTURA *(tre righe)*

1. ### **A `eps 0` la coppia dispersiva piu' stretta sta a `K` e `K'`, e NON si chiude:** ### **`salto/s` da `3.14` a `2.89`** *(`s` da `0.05` a `0.5`)*: ### **sui triangoli la coppia e' MASSIVA, nessun punto senza massa** *(la previsione regge)*; ### **la curvatura a `K` e' isotropa entro `7.7e-4`** *(la previsione regge: niente sella)*.
2. ### **`lambda* = 1/2` ESATTO solo a `eps 0`:** ### **a `eps > 0` la moneta sposta il centro della coppia** *(`centro/s` da `-0.0001` a `-0.0026`)* ### **e `lambda*` scarta da `1/2` di `3e-5`-`1.6e-3`, crescendo con `eps` e con `s`**: ### **il PUO'-FALLIRE fallisce, e la previsione «`lambda* = 1/2` a `K`» vale solo senza moneta.**
3. ### **HAMILTON nella convenzione simmetrica: `a_H/a_RG` POSITIVO e UGUALE sulle due bande** *(`+2.26` a `s 0.05` fino a `+1.63` a `s 0.5`, `eps 0`; fino a `+2.72` a `eps 1`)*, ### **verso `cs` BASSO**; ### **in quella di oggi `+6.8` e `-2.3`, di segno opposto.** ### **`delta(s)` va come `s^2.12`-`s^2.14`** *(contro `s - 0.02`: `1.70`; il palindromo prevedeva `2`: dentro la banda, non esatto)*.

### 7.5 DOVE STA LA FISICA DI BASSA ENERGIA SUI TRIANGOLI

### **A `K` e `K'`, a `s` piccolo, con un salto `~ pi s` e curvatura isotropa** *(`eps 0` fino a `s 0.5`; `eps 0.25` fino a `0.3`; `eps 0.5` e `1` fino a `0.1`)*; ### **a `s` piu' grande con la moneta il salto minimo passa a `Gamma`, fra livelli spaccati dalla moneta e bande PIATTE o NON AFFIDABILI: li' Hamilton NON e' misurato.**

### 7.6 CHE COSA DEL QUADRATO HA UN CORRISPONDENTE QUI

### **SI':** ### **`delta ~ s^2`** *(qui `2.12`-`2.14`)*; ### **`lambda* = 1/2`, esatto solo a `eps 0`** *(sul quadrato era unico; qui a `eps > 0` scarta fino a `1.6e-3`)*. ### **NO:** ### **il punto senza massa a `(pi, pi)`** *(qui la coppia non si chiude mai)*; ### **le selle a `k = pi`** *(qui a `K` la curvatura e' isotropa)*. ### **NON ANCORA MISURATO:** ### **`a/a_RG -> -1.85` a `s` piccolo e i solitoni larghi** *(qui il valore simmetrico a `K` e' `+2.26`: ### **il confronto con il numero del quadrato va fatto nella STESSA convenzione e allo stesso tipo di modo, e NON lo asserisco**)*.
