# DOVE PUO' NASCERE LA LUCE SUI TRIANGOLI: IL REGIME s -> 1 E LA MONETA

> **Il mandato:** di Luca, «dove puo' nascere la luce sui triangoli» *([[DECISIONE-SOLO-TRIANGOLI]]; [[LUCE-VINCOLO-LAMPI-GAMMA]]; [[SPAZIOTEMPO-3PIU1]]; il gradino prima e' `77f9f850`)*. ### **Solo
> spettri, in memoria.** ### **`leggi.yaml`, l'impronta `2e7f795d2a52fbe7`, la convenzione nel repo e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE)*. ### **Importati, non copiati:**
> `_triangoli`, `_triangoli_bassa_energia`, `_triangoli_forza`, `_triangoli_fattore`, `_triangoli_luce`, `_zero_simmetrico`. ### **LE PAROLE, da ora:** ### **«il limite `s <= 1`»** *(la regola `B-5`, un arco
> per tick)*, ### **«il regime `s -> 1`», «`v_max`»** *(la velocita' massima di gruppo misurata)*: ### **nessuna delle tre si chiama «cono» senza dire quale.**

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica.**
2. **Il gradino:** ### **`(A)` il regime `s -> 1`; `(B)` la moneta.**
3. **Aggiunge un numero o una legge?** ### **No.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No: `cs` uniforme, `s` come `dtau`.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **un modo lineare senza massa nasce dalla camminata, e a che velocita'?**

## 1. VISTO IN MEMORIA, prima di scrivere *(i numeri li ristampa lo strumento)*

- ### **A `s = 1` ESATTO la scena NON e' rifiutata** *(il limite `s <= 1` e' asserito, non stretto)*: ### **si usa `s = 1.0`.**
- ### **IL TOCCO LINEARE A `s = 1` NON E' A `K`, E' A `Gamma`, ATTRAVERSO LA FASE `pi`:** ### **le bande a `+-pi s` di `Gamma` si toccano quando `-pi = +pi`** *(il salto attraverso `pi` e' `2 pi (1 - s)`)*;
  ### **a `s = 1` la dispersione e' lineare con pendenza `0.71`** *(vicino a `1/sqrt2`)*, ### **materia e vuoto.** ### **La coppia a `K` resta MASSIVA** *(`+-1.0472 = +-pi/3`: il salto `2 pi/3`)*.
- ### ⚠ **UN DIFETTO DEL MIO METODO, corretto prima del codice:** ### **i livelli vanno raggruppati SUL CERCHIO** *(`-pi` e `+pi` sono lo stesso livello: `_triangoli_luce.livelli` non li unisce)*.

## 2. IL METODO

### **PARTE A** *(`eps 0`; `s` in `(0.5, 0.7, 0.9, 0.95, 0.99, 0.999, 1.0)`; materia e vuoto; zero simmetrico e di oggi)*
- ### **Lo spettro** *(`_triangoli_bassa_energia.matrice`, lato `48`)* ### **ai punti `Gamma`, `K`, `K'`, `M` coi livelli SUL CERCHIO; i tocchi** *(molteplicita' `> 1`, o il livello `0`)* ### **e la loro dispersione**
  *(`_triangoli_luce.dispersione`, `16` direzioni, `k` in `(1, 2, 4) x 1e-3`: l'esponente, e per i lineari la pendenza e l'anisotropia)*; ### **il salto minimo fra livelli distinti su tutta la zona, e dove.**
- ### **`v_max` su tutti i settori** *(`_triangoli_forza.v_max` sulla materia e sul vuoto, il vuoto al posto della materia con un'identita' nel resto, come `77f9f850`)*.
- ### **LA COPPIA A `K`** *(`_triangoli_forza.coppia_K`)*: ### **il salto, e `v_b` dal fit iperbolico di `7daa8840`** *(`_triangoli_fattore.ramo_lungo`, `k_max 0.1`, `200` punti)*.
- ### **LA COPPIA ATTRAVERSO `pi` A `Gamma`** *(i due livelli adiacenti a `pi`)*: ### **il salto `2 pi - (w_alto - w_basso)`, la sua `v` di Einstein rispetto al centro `pi`** *(`sqrt(omega_0 omega'')`, `omega_0` il
  mezzo salto, `omega''` dalla dispersione quadratica)*.
- ### **Accanto: il limite `1`, `v_max/s`, `v_b/s`, la pendenza del tocco lineare`/s`;** ### **l'andamento verso `s = 1`: l'esponente locale `d ln|f(1) - f(s)|/d ln(1 - s)` fra `0.9`, `0.99`, `0.999`.**

### **PARTE B** *(`s` in `(0.05, 0.3, 0.5, 0.9)`; `eps` in `(0, 0.1, 0.25, 0.5, 0.75, 1.0, pi/2)`)*
- ### **Per ogni `(eps, s)`: i livelli sul cerchio ai quattro punti, i tocchi e il loro esponente, i lineari e la loro velocita'; il salto minimo e dove; `v_max/s` su tutti i settori; la coppia a `K`
  seguita in `eps`** *(«il modo massivo piu' basso»: la coppia di `8781162c`, seguita; DICHIARATO)* ### **col salto, `v_b/s` e `v_b/v_max`.** ### **Le righe di `eps 0.5` in evidenza.**

## 3. LE PREVISIONI *(prima dei numeri dello strumento)*

- ### **LA PREVISIONE DEL GUARDIANO** *(il salto a `K` si chiude a `s = 1` con un tocco lineare)* ### **e' gia' smentita da cio' che ho visto:** ### **a `s = 1` il salto a `K` e' `2 pi/3`; il tocco lineare e' a `Gamma`, attraverso
  `pi`, con velocita' `~0.71`, non `1`.**
- ### **Il primo PUO'-FALLIRE** *(`v_max/s` entro `0.01` da `1` a `s = 1`)*: ### **FALLISCE** *(`v_max/s` cresce da `0.635` a `s 0.5`; prevedo `~0.71` a `s = 1`)*.
- ### **Il secondo** *(un tocco lineare a `s = 1`)*: ### **PASSA.**
- ### **Il terzo** *(un lineare a `s <= 0.5` con `v` entro il `5%` da `v_b`)*: ### **non lo prevedo con sicurezza: la moneta puo' aprire punti; prevedo di NO** *(a `eps 0` nessun tocco lineare a `s <= 0.5`)*.
- ### **LA DEFINIZIONE DI LUCA** *(la luce = un arco per tick)*: ### **prevedo che NON si realizzi nemmeno a `s = 1`: il modo lineare va a `~0.71` archi per tick.**

## 4. I CRITERI, FISSATI ORA *(dal mandato)*

- ### **DEVE PASSARE: a `s 0.3, eps 0`, il salto della coppia a `K` = `8781162c` e `v_b` = `7daa8840` entro `1e-9`; `v_max` = `77f9f850` entro `1e-6`.**
- ### **DEVE PASSARE: lo spettro invariante per `60` gradi** *(`_triangoli.scarto_c6`, sul cerchio)* ### **entro `1e-12` a ogni `(eps, s)`** *(le due convenzioni)*.
- ### **DEVE FALLIRE, per la chiave giusta: «a `eps 0`, `s 0.3` esiste un modo lineare senza massa»** *(la chiave: l'analisi dei tocchi ha trovato dei tocchi, e nessuno e' lineare)*.
- ### **PUO' FALLIRE: a `s = 1`, `eps 0`, `v_max/s` entro `0.01` da `1`.**
- ### **PUO' FALLIRE: a `s = 1`, `eps 0`, esiste un tocco lineare.**
- ### **PUO' FALLIRE: esiste un `(eps, s)` con `s <= 0.5` in cui un modo lineare senza massa ha velocita' entro il `5%` da `v_b` della coppia a `K`.**
- ### **IL VERDETTO DI FISICA: le tabelle.** ### **A parte: tre righe di lettura; una sulla definizione di Luca; una sulla tensione col principio di equivalenza** *(violato d'ordine `1` nel regime `s -> 1` sul quadrato,
  `05055fc6`; sui triangoli NON ancora misurato)*; ### **una su che cosa resta per il campo `U(1)`.** ### **Informazione per Luca, non scelte.**

### 📝 **ANNOTAZIONE 1** *(prima della corsa, nel commit dello strumento)*: ### **la prova a vuoto ridotta** *(`s` in `(0.5, 0.9, 0.99, 0.999, 1)`, e `eps 0, s 0.3`)* ### **ha trovato UN mio difetto, corretto:**
### **il salto attraverso `pi` a `Gamma` usciva `pi` a `s = 1` invece di `0`: si legge sui livelli NON uniti sul cerchio.** ### **I NUMERI VISTI** *(non li uso; le previsioni restano)*: ### **`v_max/s -> 0.70711`
a `s = 1`; il tocco lineare a `Gamma` a `0.7071`, isotropo entro `1e-12`, in materia e vuoto; `v_b/s` della coppia a `K` SCENDE verso `0.550`** *(`v_b/v_max`: `1.26` a `s 0.3`, `0.78` a `s = 1`)*; ### **a `s
0.999` i rami del tocco escono «altro» `1.89`** *(il salto `6.3e-3` e' del passo della dispersione: `k ~ 1e-3`)*.

## 5. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_triangoli_dove_la_luce.py` e la sua voce nell'inventario, committati prima dei numeri;
3. la corsa, il referto, la relazione, i collegamenti a `LUCE-VINCOLO-LAMPI-GAMMA` e `SPAZIOTEMPO-3PIU1`, la sezione `6`.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*
