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
