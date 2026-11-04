# IL BORDO ASSORBENTE: IL CAMPO CHE ESCE E NON RIENTRA *(Luca, `2026-11-03` `21:52`)*

**La domanda di Luca:** l'accelerazione del solitone e' data dalla materia che irradia, esce da una parte del toro e rientra dall'altra? **La corsa `TB3`:** `L 81`, `F3`, la partenza di `TF3` *(l'unica differenza: il bordo)*, fino a `30000`; il bordo fuori dal nucleo *(un'operazione in `csv/solitone/` dopo ogni tick, col suo test)*: la fascia `R >= R_A = 28` dal centro iniziale, `psi -> psi (1 - g)`, `phi -> phi0 + (phi - phi0)(1 - g)`, `g = g_max sin^2(pi/2 (R - R_A)/(40.5 - R_A))`; `g_max` il piu' piccolo con la riflessione di un pacchetto in banda `B` sotto `1e-2`; il bilancio `M` dentro + assorbita = `M0` entro `1e-10` *(e `V`, l'energia registrata)*; l'arresto se il cuore *(`3 w`)* entra nella fascia; le mappe. Le letture (b1)-(b5) sono di Luca. **La coda:** dopo `TS` *(in volo)*, prima di `TM3`.

## 1. LE PREMESSE DAL CODICE *(e cio' che NON so)*

- **Il tick vivo** e' `AC.tick` *(la rampa, poi `TK.percorri_tick`)*; conserva `M` a `~4e-12` per `1000` *(`A3`)*: **il bilancio entro `1e-10` e' raggiungibile** se `M` assorbita si somma tick per tick *(`sum |psi|^2` sulla fascia prima e dopo)*.
- ### **LA PREMESSA DA MISURARE PRIMA DI TUTTO: `phi0`.** **Il mandato dice «`phi0` il vuoto `F3` di fondo».** **Se `F3` da solo** *(`psi = 0`)* **non e' fermo sotto il tick vivo** *(anche solo una fase globale che gira a ogni tick, o la rampa che lo cambia)*, **un `phi0` FISSO non assorbe soltanto le onde: FORZA il vuoto della fascia verso uno stato che non e' il suo**, e immette o toglie energia. **In `TM1000` `|Lambda - Lambda(t 0)|` vale `~2` ovunque** *(`campo_TM1000.txt`)*: **il dubbio e' concreto.** ### **`B0`, una carta di minuti:** il vuoto `F3` da solo col tick vivo *(la rampa e dopo)*: `|phi(t) - c(t) F3| / |F3|` con `c(t) = <F3, phi(t)> / |F3|^2`. **Tre casi:**
  1. **`F3` fermo** *(`c = 1`)*: `phi0 = F3`, come dice il mandato;
  2. **`F3` fermo a meno di una fase** *(`|c| = 1`, `arg c` che gira)*: `phi0(t) = c(t) F3`, **con `c(t)` dal vuoto da solo** *(non tarato: misurato)* -- **lo propongo, e Luca lo conferma;**
  3. **`F3` NON fermo nemmeno a meno di una fase:** **`phi0(t)` va evoluto a parte** *(un secondo stato col vuoto da solo, il costo della corsa `~x2`)* **o il bordo agisce solo su `psi`**: **una scelta di Luca: FERMO.**
- **Il pacchetto del test** *(in banda `B`, sul vuoto `F3`, senza solitone, verso la fascia)*: **la costruzione e' mia, da dichiarare:** l'autovettore di banda `B` di `A(k)` *(`DV.matrice`, il `k` sul reticolo del toro)* per un inviluppo gaussiano largo `W`, centrato a `R0` dal centro, `k` lungo la direzione della fascia. **La riflessione:** la frazione di `M` del pacchetto che, dopo l'arrivo, torna verso il centro *(dentro `R < R_A - W`)*, quando la parte trasmessa e' assorbita. **I numeri `W`, `R0`, `k`** sono di protocollo *(non entrano nella fisica della corsa)*, dichiarati prima; **la griglia di `g_max`** *(`1e-4`, `3e-4`, `1e-3`, `3e-3`, `1e-2`, `3e-2`, `1e-1`)* dichiarata prima, e si prende il piu' piccolo sotto `1e-2`. **Il pacchetto e' piccolo** *(`N` del pacchetto `<<` quello del solitone: il regime lineare)*.
- **L'energia assorbita:** il libro dei conti *(`LC.conti_per_nodo`)* costa: **la misuro una volta** *(`B0`)*; se a ogni tick costa troppo, l'energia assorbita si registra **ai campioni** *(la differenza fra il totale e il dentro)* e si dichiara.

## 2. PROGETTAZIONE

1. **`csv/solitone/carta_b0.py`** *(dopo `TS`, minuti)*: `B0` il vuoto `F3` da solo col tick vivo, `10`, `100`, `1000` tick nella rampa e dopo *(dallo stato dopo la rampa del vuoto da solo)*; il tempo di un tick col libro dei conti. **Decide il caso 1, 2 o 3.**
2. **`csv/solitone/bordo.py`** *(la fascia, `g(R)`, l'assorbimento con `phi0`, i conti dell'assorbito)* e **`test_bordo.py`** *(`G0` `g = 0` dentro, `g_max` sull'ultimo anello, la forma `sin^2`; `G1` il bilancio su uno stato di prova; `G1-F` deve fallire: senza contare l'assorbito)*; **`carta_bordo.py`** *(il pacchetto, la riflessione per `g_max` della griglia, il `g_max` scelto)*.
3. **`corsa_accensione`:** `CORSE["TB3"]`, il bordo dopo ogni tick, l'arresto, le mappe; **la patch a `TS` finita** *(il file e' nel percorso di `TS`)*.
4. `D6`, la cassetta, i dischi, la corsa *(~`3.4` ore + il bordo)*; la carta del referto accanto a `TF3` + `TF3C`.

### Che cosa mi farebbe FERMARE
`B0` nel caso 3; nessun `g_max` della griglia sotto `1e-2`; il bilancio fuori da `1e-10`; `C:` sotto `5` GB.

## 3. TODO
- [ ] questo file, la relazione; commit;
- [ ] `carta_b0.py` *(commit; gira dopo `TS`)*; poi le scelte dal suo esito; il resto.

## 4. ESITO DI `B0` *(`doc/referti_l2/b0_vuoto_F3.txt`, `1/1`; `carta_b0.py` `ffa5a941`)*: **IL CASO (2) -- FERMO**

- **`F3` da solo resta `c(t) F3`** in tutte le tappe: il peggiore `|phi - c F3| / |F3|` **`1.4e-14`**, `|c| = 1` entro `1.9e-13`, `Lambda` uniforme *(std/media `<= 7.8e-15`)*. **Ma `c` gira:** `arg c` `2.35` a `1000` *(nella rampa)*, e **dopo la rampa la fase per tick e' costante: `+0.471238898038469`** *(scarto max `3.1e-15` su `999` tick)* **`= 3 pi / 20` entro `5.6e-17`**, cioe' **`pi` per unita' di tempo** *(`s = 0.15`)*. **E' il caso (2).**
- **`B0-P`** *(la materia `x 1e-3`)*: il vuoto si scosta a `6.3e-11`, sopra `1e-12`: **la misura legge il vuoto.** *(Scosta poco: `1e-3` in `psi`, `6e-11` in `phi`.)*
- **Il costo del libro dei conti:** `0.014` s contro `0.0475` s per tick *(`0.3` tick)*. ### **Ma la chiamata ha dato `RuntimeWarning`** *(divisione per zero in `E_leg`, `_scomposizione_solitone.py`)*: **ho misurato solo il TEMPO, non il valore**; prima di usare l'energia assorbita va controllato che il libro dia un numero finito sullo stato della corsa.
- ### **Un `phi0` FISSO = `F3` sarebbe sbagliato:** dopo `n` tick il vuoto vero e' `e^{i 3 pi n / 20} F3`, e il bordo lo riporterebbe a `F3` *(forzandolo, con `|phi - F3|` fino a `2 |F3|`)*.
- **La mia proposta** *(da confermare: la decisione e' di Luca)*: **`phi0(t) = c(t) F3`, con `c(t)` MISURATO** -- la tabella di `c` sui `6667` tick della rampa *(una corsa del vuoto da solo, `~5` minuti)*, poi `c(t) = c(K) e^{i omega (t - K)}` con `omega` misurato *(`3 pi / 20` per tick)*. **Le alternative:** il vuoto da solo evoluto accanto per tutta la corsa *(il costo `~x2`)*; il bordo solo su `psi`.

## 5. IL MANDATO DI LUCA DEL `2026-11-04` `09:00`: `phi0(t) = c(t) F3`, IL CONTROLLO DELLA FASE, `E_leg`

### 5.1 LE DECISIONI DI LUCA *(non mie)*
- **`phi0(t) = c(t) F3` con `c(t)` MISURATO** *(la scelta (a) della sezione 4)*: la tabella di `c` sui `K = 6667` tick della rampa, poi `c(t) = c(K) e^{i omega (t - K)}` con `omega` misurato su almeno `1000` tick dopo la rampa *(atteso `3 pi / 20` entro `1e-14`; se no, FERMO)*. Scartate: il vuoto evoluto accanto, il bordo solo su `psi`.
- **Il controllo della fase nella corsa:** a ogni campione, sui nodi della fascia e PRIMA dell'assorbimento, `d(t) = |phi - c(t) F3| / |F3|` *(medio e massimo)* e lo scarto di fase medio `arg <phi, c(t) F3>`.
- **`E_leg`:** il `RuntimeWarning` va sistemato prima della corsa; il libro dei conti dell'energia assorbita non si usa finche' non da' un numero finito.
- **Il resto come nelle sezioni 1-2:** `L 81`, `F3`, la partenza di `TF3`, fino a `30000`, `R_A = 28`, `bordo.py`.

### 5.2 LE PREMESSE DAL CODICE *(prima di toccare; e cio' che NON so)*
- ### **`E_leg`: la causa e' gia' scritta nel repo** *(`doc/referti_l2/nan_e_leg.txt`, `csv/_nan_e_leg.py`, `2026-10-28`)*: **il `NaN` nasce in `_scomposizione_solitone.parti` sullo STATO UNIFORME di costruzione di `e_K`** *(`stato_uniforme` mette `phi_h = 0`: `Lambda = 0` su TUTTI i nodi, `rho / lam = inf`, `lam * F1(inf) = 0 * inf = nan`)*. **Chi lo chiama:** `_vuoto_vivo_B.e_K_di` *(e `protetto.e_K`)*; **`e_K = E_mat / M` non usa `E_leg`**: il `NaN` viene calcolato e buttato. **Credo che in `B0` l'avviso sia arrivato dalla chiamata `P.e_K(z)`, non dal libro dei conti.** **Il libro dei conti** *(`_libro_dei_conti.conti_per_nodo`)* ha gia' `assert np.all(lam > 0.0)` e in `B0` **non e' scattato**: sullo stato della corsa `Lambda > 0`. *(Da confermare con la diagnosi del passo 2: quale chiamata, quali nodi, quale tick.)*
- ### ⚠ **UNA PREMESSA DEL MANDATO CHE CADE (`E1-F`):** **«la versione vecchia sullo stesso stato da' non finito»** **non vale sullo stato di `B0` ne' su quello della corsa a `t 0`**: li' `Lambda > 0` e la versione vecchia e' gia' finita. **Il solo stato su cui la versione vecchia da' non finito e' lo stato uniforme di costruzione di `e_K`.** **Quindi:** `E1` sui tre stati *(lo stato di `B0`, la corsa a `t 0`, lo stato uniforme di `e_K`)*; **`E1-F` sullo stato uniforme di `e_K`**, l'unico dove il difetto c'e'. **Lo scrivo come premessa caduta, non come scelta nascosta.**
- **Il valore giusto nel limite, DALLA DEFINIZIONE:** `Lambda F1(rho / Lambda) = rho - Lambda arctan(rho / Lambda)`; con `rho >= 0` fisso e `Lambda -> 0+`, `arctan` resta limitato *(`<= pi / 2`)* e il secondo termine va a `0`: **il limite e' `rho`** *(e `0` se anche `rho = 0`)*. **La correzione:** dove `Lambda > 0` la formula vecchia, **operazione per operazione** *(`E0`: al bit)*; dove `Lambda = 0`, `rho`.
- ### ⚠ **UNA SECONDA PREMESSA CHE CADE: L'ARRESTO «SE IL CUORE (`3 w`) ENTRA NELLA FASCIA».** **Misurato** *(`w` = `per.w` dei campioni, dai jsonl; `doc/referti_l2/accensione_lenta/diag_cuore_3w.py.txt` -> `diag_cuore_3w.txt`)*: **in `TF3 + TF3C` `3 w >= 28` la prima volta a `t 2709.0`** *(`w 9.334`)*; **in `TS` a `2947.5`**; `w` arriva a `12.6` *(`TF3C`)* e `12.7` *(`TS`)*. **Il moto parte a `~4000` *(`TS`)* e `~16000` *(`TF3`)*: con l'arresto com'e' scritto, `TB3` si fermerebbe PRIMA di poter rispondere alla domanda.** **`w` cresce per l'alone, non per lo spostamento** *(`alone` da `0.001` a `0.05`)*. ### **E' una scelta di Luca: FERMO prima della corsa** *(i passi 1-3 non ne dipendono e li faccio)*. **Le alternative che propongo:** (i) l'arresto sullo SPOSTAMENTO del centro, `|X - X0| + 3 w_in >= R_A` *(`w_in` `6.64`, la larghezza iniziale: `|X - X0| >= 8.1`)*; (ii) una larghezza del CUORE invece della `w` quadratica *(per esempio il raggio che contiene meta' della materia; una misura nuova, da dichiarare)*; (iii) com'e' scritto *(la corsa finisce a `~2700`)*.
- **Il costo dell'energia assorbita:** due libri dei conti per tick *(prima e dopo l'assorbimento)*, `2 x 0.3` tick: la corsa da `~3.4` a **`~5.4` ore**. **Non lo so ancora con certezza:** la stima vera dopo il primo pezzo.
- **Cio' che NON so:** se `c(t)` nella rampa e' riproducibile al bit da una seconda corsa del vuoto *(lo dice `C0`)*; quanto e' grande `d(t)` nella fascia senza forzatura *(le onde che arrivano)*.

### 5.3 QUALE SCARTO SI LEGGEREBBE COME «IL BORDO FORZA IL VUOTO», E PERCHE' *(scritto prima di girare)*
- **Sulla fascia** *(i nodi con `g > 0`, prima dell'assorbimento)* si scompone `phi = a c(t) F3 + r`, con `a = <c F3, phi>_fascia / |c F3|^2_fascia` e `r` ortogonale. **Le onde** *(materia irradiata, oscillazioni del vuoto)* **hanno proiezione quasi nulla sul vuoto uniforme**: stanno in `r`. **Uno sfasamento del vuoto lontano** *(il vuoto della fascia che gira con un'altra fase o un altro modulo)* **sta in `a - 1`.**
- **Si registra:** `d(t)` *(medio e massimo sui nodi)*, `|a - 1|`, `arg a` *(lo scarto di fase medio di Luca)*, `|r| / |F3|_fascia`.
- ### **La lettura «forzatura»:** **`|a - 1|` confrontabile con `d` o piu' grande** *(lo scarto e' coerente, non onde)* **E con `arg a` dello stesso segno per almeno `3` blocchi di `1000` consecutivi** *(una deriva, non un'oscillazione)*. **Perche':** in quel caso il bordo, a ogni tick, riporta la fase del vuoto della fascia a `c(t)` contro la dinamica: e' una forza. **La lettura «nessuna forzatura»:** `|a - 1| << d` *(le onde dominano)* o `arg a` che cambia segno. **Non e' una soglia d'arresto:** e' una lettura, e il referto mostra i numeri a Luca.
- **Un controllo di scala:** in `B0` *(il vuoto da solo)* `d` vale `~1e-14`; **con la materia `x 1e-3` il vuoto si scosta a `6e-11`** *(`B0-P`)*. **In `TB3` la materia e' intera:** mi aspetto `d` molto sopra `1e-14`, **e non so di quanto.**

### 5.4 LE LETTURE DI LUCA *(scritte prima di girare)*
- **(b1)** con il bordo la corsa non parte entro `30000`, o resta sotto il livello di `TF3` e `TS`: il moto veniva dal giro del toro *(materia e/o vuoto che rientrano)*;
- **(b2)** la corsa parte comunque, con velocita' e persistenza come `TS` / `TF3` / `F0`: il moto e' del solitone, non della scatola;
- **(b3)** altro, da descrivere.
- ### **Da scrivere nel referto:** le partenze gia' viste sono SPARSE *(`~4000` `TS`, `~9500` `F0`, `~16000` `TF3`)*: **con una corsa sola, una partenza tardiva NON basta a dire (b1).**

### 5.5 TODO *(in ordine, un commit ciascuno, il codice committato PRIMA di girarlo)*
1. **questo file** e la relazione; commit.
2. **`E_leg`:** la diagnosi *(uno script: quale chiamata emette l'avviso, quali nodi, quale tick)* scritta qui; poi la correzione in `_scomposizione_solitone.parti` e il test `E0` *(al bit: lo stato di `TS` a `30000` e di `TF3` a `16000`, dai `.npz` di ripresa verificati con lo `sha_fine`)*, `E1` *(i tre stati)*, `E1-F`; la cassetta intera.
3. **La tabella di `c(t)`** *(il vuoto da solo, `K + 1000` tick)* e il test `C0` / `C0-F`.
4. ### **FERMO: l'arresto della corsa** *(5.2)*. Poi la patch della corsa, la corsa, la stima dopo il primo pezzo.
5. La carta del referto; la relazione.

### 5.6 LA DIAGNOSI DI `E_leg` *(`doc/referti_l2/e_leg_diagnosi.txt`; `carta_e_leg.py` `ca0196cb`, `_scomposizione_solitone.py` `17dde60a`)*: **PRIMA della correzione**
- **Quale chiamata:** i due `RuntimeWarning` *(`divide by zero`, `invalid value in multiply`, `_scomposizione_solitone.py:124`)* vengono **SOLO** da `parti <- _vuoto_vivo_B.e_K_di <- protetto.e_K`. **La scena** *(`V.scena`)* **non ne da' nessuno; il libro dei conti nessuno** *(sullo stato di `B0`: `leg` finito, somma `0`; sulla corsa a `t 0`: finito, somma `9.9327e+05`)*.
- **Quali nodi:** lo stato uniforme di `e_K` *(`SC.stato_uniforme`, `phi_h = 0`)* ha **`Lambda = 0` su TUTTI i `6561` nodi**, con `rho = 1` su ciascuno: `rho / Lambda = inf`, `F1(inf) = inf - pi/2 = inf`, `0 * inf = nan`.
- **Quale tick:** **nessuno**: e' la costruzione di `e_K`, una volta per corsa, prima del primo tick.
- **Perche' non ha mai cambiato un numero:** `e_K = E_mat / M` *(`e_K_di`)*: `E_leg` si calcola e si butta *(`e_K` `-4.712275000354643`)*.
- **Il valore giusto nel limite, dalla definizione** *(5.2)*: `Lambda F1(rho / Lambda) = rho - Lambda arctan(rho / Lambda) -> rho`. **La correzione:** in `parti`, dove `Lambda > 0` la formula di prima operazione per operazione, dove `Lambda = 0` il limite `rho`; **nessun numero cambia dove `Lambda > 0`** *(lo dice `E0`)*.
- **Un avviso in piu', non chiesto:** un `ResourceWarning` *(`_livelli_piatti.leggi` lascia aperto `griglia.json`)*: **innocuo, non lo tocco** *(un file che molte corse importano)*; lo segnalo.
