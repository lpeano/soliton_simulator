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

## 5. TODO DEL NEXT STEP

1. questo task history, da solo; 2. `csv/_triangoli_dove_la_c.py` e l'inventario, prima dei numeri; 3. la corsa, il referto, la relazione, i collegamenti, la sezione `6`.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*
