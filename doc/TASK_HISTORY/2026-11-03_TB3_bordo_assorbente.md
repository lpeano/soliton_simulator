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
