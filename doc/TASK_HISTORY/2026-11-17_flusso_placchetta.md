# IL FLUSSO DI B NELLA PLACCHETTA, SOLO MISURA *(il mandato unico di Luca `2026-11-17` `19:40`)*

> **Il mandato:** **prima di scegliere l'innesco fra (a) il contatore del lapse, (c) la riserva del calore e (d) il flusso della placchetta, si misura (d) sugli stati GIA' SALVATI di C1 e C2.** **Nessuna corsa nuova, nessuna scelta; nessun file del nucleo.** **La definizione** *(del guardiano su delega di Luca)*: **per ogni placchetta `p` (triangolo, verso antiorario) `Phi_p = e * somma sul bordo di +-A_a`**; il valore GREZZO e quello ridotto in `(-pi, pi]`; il quanto `|Phi_p| = 2 pi`. **Le prove prima** *(K1-K4)*, **la misura** *(M1-M5)*, **la sez. `14` della carta della mitosi** *(la lettura del guardiano su K2, la `14.7`)*, **FERMO per Luca fra (a), (c), (d).**
> **L'ordine dei lavori:** **M3-bis** *(l'aggiunta delle `18:48`)* **gira** *(5 processi, i segmenti di C2)*: **non si ferma**; **questa misura parte al primo posto libero** *(un processo; al piu' 5)*.

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

- ### **IL CAMPO DELLE CORSE E' NON COMPATTO:** **`csv/solitone/p6_u_breve.py`: `FORMA = "noncompatto"`** *(«Luca, sez. `11.3`, `11.7`: non compatta, come T3»)*; **`mattone.Campi`** costruisce il campo con `PB.FORMA`; **`_u1_prototipo.Campo.g`**: `compatto` -> `sin(e B) / (e AREA)`, **`noncompatto` -> `B / AREA`**: ### **la spinta magnetica usa `B`, NON `sin(B)`.** **Quindi il quanto `2 pi` qui NON ha il senso pieno** *(nel non compatto `Phi` e `Phi + 2 pi` NON sono la stessa configurazione: l'energia `B^2 / 2 AREA` le distingue)* -- [[PROGETTO-U1]], la decisione aperta.
- **La costante:** **`e = p6_u_breve.E_DECISO = 6.315414e-05`** *(«Luca 20:52, sez. `11.9`»)*; **`campo.e = e`** a ogni tick *(`controllo_senza_bordo.corsa_senza_bordo`, `Campi.tick`)*.
- **Gli archi e le placchette** *(`_u1_prototipo.Campo`)*: **l'arco `3 v + a`** *(`a1`, `a2`, `a1 + a2` dal nodo `v`)*; **le placchette `su`** *(`3v, 3(v+a1)+1, 3v+2`, segni `+ + -`)* **e `giu`** *(`3v+2, 3(v+a2), 3v+1`, segni `+ - -`)*, **tutte antiorarie**; ### **`Campo.B()` E' GIA' LA CIRCOLAZIONE `somma +-A_a`** *(la densita' e' `B / AREA` in `g`)*: ### **quindi `Phi_p = e * B_p`, e K4 confronta con `e * Campo.B()`, NON con `B_p * area_p`** *(la definizione del mandato presume `B` una densita': nel codice NON lo e'; lo scrivo come correzione, la grandezza resta quella)*. **Il link e' `u = exp(i e A)`** *(`Campo.u`)*: **la fase del giro e' `e * somma A`, cioe' `Phi_p`.**
- **Gli stati** *(`E:/soliton_simulator/controllo/<C1|C2>/stato_<k>.npz`, `campo_A`)*: **`12`, da `k 250` a `3000`**; ### **`k 0` NON e' salvato**: **la' `A = 0` PER COSTRUZIONE** *(`porto.campi` con `A = None`: `C.campo.A[...] = 0.0`)*: **K1 la prova sull'array che la corsa usa a `k 0`** *(gli zeri di `porto.campi`, dichiarato)*. **L'ordine degli archi di `campo_A`** e' quello di `Campo` *(`_u1_oggi.campo_della_scena` lo ASSERISCE)*: **lo script costruisce `_u1_prototipo.Campo` sul toro `L 186` senza la scena.**
- **CIO' CHE NON SO:** **la scala di `Phi`**. **`A` cresce da `E`** *(`deriva`: `A += w E`)*, **ed `E` e' di Gauss, proporzionale a `e`**: **`Phi = e * somma A` va come `e^2`** -- **mi aspetto `Phi` MOLTO piccolo** *(ordine `1e-6` o meno)*. **Il rischio di aliasing:** gli stati ogni `250` tick, la misura istantanea: **un'oscillazione di `A` piu' veloce di `500` tick NON si vede** *(dichiarato)*.

## 2. LE PROVE E LA MISURA: COME *(fissate PRIMA)*

- **K1:** `A = 0` -> `Phi = 0` al bit. **K2:** `somma_p Phi_p = 0` entro l'arrotondamento *(ogni arco in due placchette con segni opposti)*, su ogni stato. **K3:** `chi` casuale per nodo *(seme `0`, scala la deviazione di `A`)*, `A -> A + chi_j - chi_i`: `max |Delta Phi| / max |Phi|` entro `1e-12`; **DEVE FALLIRE:** un arco solo cambiato. **K4:** `Phi` dalle placchette costruite DA ME *(i vicini sul reticolo, i segni dal verso antiorario)* contro `e * Campo.B()`: entro `1e-12` relativo.
- **M1:** a ogni stato `max |Phi|` *(grezzo e ridotto)*, dove *(il baricentro della placchetta dal centro della corsa, `meta["centro"]`)*, il profilo per anello *(media di `|Phi|` e massimo, `su` e `giu` separati)*, il segno medio. **M2:** `max |Phi|` e `|Phi|` medio all'anello del massimo contro `k`; la retta dei minimi quadrati, la pendenza con l'errore standard; **cresce** *(pendenza oltre `3` errori, positiva)*, **cala** *(oltre `3` errori, negativa)*, **resta** *(entro `3` errori)* -- **soglia dichiarata ORA.** **M3:** `max |Phi| / 2 pi`; se cresce, il tick del primo quanto `(2 pi - max) / pendenza` con l'errore. **M4:** C1 contro C2, stato per stato. **M5:** la mappa di `Phi` a `k 3000` *(C2; scala lineare simmetrica; `12.4` e `23.81` segnati)*.

## 3. LE PREVISIONI DEL GUARDIANO *(copiate PRIMA delle misure; anche nella carta della mitosi, sez. `14.7`)*

- **P-B1.** In C2 `max |Phi_p|` resta sotto `1e-2` rad su tutti gli stati (molto sotto `2 pi`).
- **P-B2.** Il massimo sta entro `25` nodi dal baricentro (nel guscio della materia).
- **P-B3.** C1 e C2 differiscono per meno del `10%` su `max |Phi|` a ogni stato.
- **P-B4.** K3 passa (invarianza di gauge entro `1e-12`).
- ### **LE MIE, accanto:** **P-B1 VERA, e di molti ordini** *(`Phi ~ e^2`, sez. `1`)*; **P-B2: NON so** *(`A` e' un integrale di `E`, che e' radiale attorno alla materia: nel non compatto senza correnti la circolazione di un campo radiale e' piccola ovunque, e il massimo puo' stare dove il numerico lo mette)*; **P-B3: VERA fino a `k 1000`** *(C1 e C2 sono al bit fino a li', il referto del controllo)*, **dopo NON so**; **P-B4 VERA** *(e' un'identita' algebrica: l'arrotondamento)*.

## 4. TODO DEL NEXT STEP

1. questa carta: commit, push;
2. lo script `doc/referti_l2/flusso_placchetta.py` *(K1-K4 e M1-M5 in una corsa: la misura e' breve, sugli stati)*: commit, push; la corsa al primo posto libero; il referto `doc/referti_l2/flusso_placchetta.txt` con la mappa: commit, push;
3. la carta della mitosi, sez. `14`: la lettura del guardiano su K2 *(come sua, accanto alla mia)* e la `14.7`; **FERMO per Luca fra (a), (c), (d).**
