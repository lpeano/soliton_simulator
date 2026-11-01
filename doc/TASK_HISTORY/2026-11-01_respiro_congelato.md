# 2026-11-01 — IL CONTROLLO A VUOTO CONGELATO DEL RESPIRO SUL FONDO *(il mandato di Luca del `2026-11-01`, dopo `1ee60e19`; [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]], [[PIANO-2D-3D]]; NESSUNA MODIFICA AL NUCLEO, nessun peso tarato)*

> **La coda:** questo mandato e' arrivato a coda ferma *(il mandato delle `11:22` chiuso, ⑦ non ancora cominciato)*, ed e' la continuazione del mandato delle `11:22`, che aveva la precedenza *(Luca `11:31`)*. **Lo faccio prima di ⑦** e lo registro qui; **se Luca vuole un altro ordine, vale il suo.** L'ordine: **questo → ⑦ (01:22) → ⑧ (01:27 + 01:28).**

## 1. LE PREMESSE DAL CODICE

- **Il congelato vero** e' `_congelato_lungo.avanza(z, phi0, 1)`: `_deriva_congelato.tick_congelato` con **i pezzi del vuoto `VC.VUOTO` saltati** *(`CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`, `CAMM-FASE-VUOTO`)* e `phi` rimesso a `phi0` a fine tick. E' quello delle corse di `_consolida_B` *(`20000` unita' a tasso massimo `~1e-4`)*.
- **La stessa configurazione di BG-F-0.15:** `_vuoto_vivo_B.scena(0.15, "fondo", 0.5)`, la partenza `_vuoto_vivo_B.partenza("BG", ...)` *(l'inviluppo per la scelta migliore, la coppia sulla scena)*, lo stato della scena rimesso, `psi_h = p0`: **le righe di `_energia_vuoto_vivo.preparata`**. `phi0` e' il vuoto `F0` della scena, quindi **il vuoto congelato e' `F0`**. Asserisco che `mu`, `w_in` ed `e_K` siano quelli del primo pezzo di BG-F-0.15.
- **Gli stessi campioni:** `_vuoto_vivo_B.misura` ogni `10` tick *(il cuore liscio e netto, `w`, l'alone, il baricentro, `Lambda`, i conti per regione)*, **col libro dei conti col `par` della corsa** *(eps `0.5`; `bc96e739`)*, e le bande di `D` ogni `20` tick.
- **La corsa viva da confrontare:** i pezzi di `_vuoto_vivo_B` BG-F-0.15 *(da `0` a `3000`)* e di `_respiro_sul_fondo` *(da `3000` a `10000`)*, **riletti dai pezzi committati**.
- **La ripartizione dell'energia di `326747d0` col termine della moneta NON e' stata fatta** *(il TODO del mandato)*. **Si fa senza rigirare:** la differenza fra i due libri per regione e' `eps * sum(elicita)` su quella regione, e gli stati iniziale *(`p0`, ricostruibile)* e finale *(lo stato di ripresa di ogni corsa, `db/vuoto_vivo_B/*.npz`, controllato con lo sha1 dell'ultimo pezzo)* ci sono. **La strada `A` tick per tick, invece, non si ricalcola senza rigirare:** lo dichiaro.
- **La soglia della decisione `9`** *(`t_vita` al primo `tau` con `|D|/|psi0| >= 1e-2`)* **e' su `D`, non su `w`**, e a eps `0.5` con l'inviluppo `|D|/|psi0|` e' gia' `~0.1` a tempo `3` *(`326747d0`)*. **Tradurla in un tempo di vita da `w(t)` non e' definito:** se esce (c2) **lo scrivo a Luca** e accanto do il tempo a cui `f_liscia` scenderebbe sotto meta' *(il criterio di dissoluzione delle corse)*, **come estrapolazione dichiarata, non come misura**.

### Cosa NON so

- se a vuoto congelato il solitone su `F0` abbia gia' la stessa crescita di `w`;
- se la crescita sia lineare o esponenziale: con un solo tratto, la distinzione puo' restare indecisa.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `K0` | **DEVE:** la scena e la partenza = quelle di BG-F-0.15 *(`mu`, `w_in`, `e_K` del primo pezzo, uguali)*; la ripresa fra i pezzi **al bit** *(lo sha1 di ogni chiave)*. |
| `K1` | **DEVE:** `M` e `V` entro `1e-10` *(V per costruzione: `phi` rimesso)*. **DEVE:** con eps `0.5` il libro dei conti passa il `par` della corsa *(asserito nello script)*. **Un processo alla volta.** |
| `K2` | **Le misure, sulle due corse, a blocchi di `1000`:** il cuore liscio, `w`, **cuore x `w`**, l'alone, la pendenza dell'alone, il baricentro. |
| `K3` | **La forma della crescita:** la pendenza di `w` e dell'alone per blocco; **il rapporto fra la pendenza dell'ultimo terzo e quella del primo terzo del tratto `5000`-`10000`** *(vicino a `1`: lineare; che cresce: esponenziale)*; e il confronto fra il fit lineare e quello esponenziale, coi residui. |
| `K4` | **Le bande** `A`, `B`, `P0`, `Ppi` in `5` istanti *(`0`, `2500`, `5000`, `7500`, `10000`, i piu' vicini disponibili)*, per tutte e due le corse. |
| `K5` | **La ripartizione di `326747d0` col termine della moneta:** per ognuna delle `6` corse, `(fine - inizio)` per regione col libro a eps `0` **= i numeri del referto di `326747d0`, AL BIT** *(DEVE: il caso nullo)*; poi gli stessi col `par`. |

## 3. LE LETTURE *(di Luca, scritte prima; decide Luca)*

- **(c1)** a vuoto congelato `w` resta limitato fino a `10000`: e' il vuoto vivo a far allargare il solitone *(`Lambda` che cala sotto il solitone)*;
- **(c2)** anche a vuoto congelato `w` cresce in modo simile: l'allargamento appartiene al solitone stesso in `B` su questo vuoto;
- **(c3)** altro.

## 4. LE MOTIVAZIONI

Senza questo controllo non si sa se l'allargamento dopo `~5000` sia un effetto del vuoto vivo o un tratto del solitone stesso. La risposta serve alla **decisione `10`** *(il vuoto del fondo)* e alla **voce `27`** *(il tempo di vita che serve all'esperimento)*.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_respiro_congelato.py` *(`--ripartizione`, `--corsa`, `--referto`)* e la riga d'inventario: committati prima di girare.
3. `--ripartizione > doc/referti_l2/ripartizione_vuoto_vivo.txt` *(breve)*: committato. **Se il caso nullo fallisce: FERMO.**
4. `--corsa` a pezzi di `10000` tick, uno alla volta, ognuno committato *(un driver)*, fino a tick `66667`.
5. `--referto > doc/referti_l2/respiro_congelato.txt`; la MAPPA *(la sezione `2` riga `1`)*; `doc/CHIUDERE_LE_USCITE.md`; `RELAZIONE`; la sezione `6` qui. **Se esce (c2):** il tempo di vita come detto nelle premesse, e **la proposta a Luca, senza eseguirla, di una prova a `L 120`** per escludere gli effetti di bordo.

## 6. L'ESITO


**Il referto** *(`doc/referti_l2/respiro_congelato.txt`, sha1-BYTE `4004db2e`, girato da `csv/_respiro_congelato.py` sha1-BYTE `65a5abef` a `b2774bb7`)*: BG-F-0.15, la stessa scena e la stessa partenza della corsa viva *(`mu`, `w_in`, `e_K` asseriti uguali nello script)*, col tick congelato vero *(`_congelato_lungo.avanza`)* fino a `10000` in `7` pezzi *(`6ce50e1b` .. `b2774bb7`)*, la ripresa al bit fra i pezzi. **`3/3` DEVE:** arriva a `10000`; `dM 3.9e-11`, `dV 0`; il libro dei conti col `par` della corsa.

**I fatti, a blocchi di `1000`:**

| | il cuore | `w` | cuore x `w` | l'alone |
|---|---|---|---|---|
| VIVO `0`-`1000` | `0.460` | `8.07` | `3.685` | `0.0008` |
| VIVO `9000`-`10000` | `0.416` | `9.86` | `4.095` | `0.0218` |
| CONGELATO `0`-`1000` | `0.592` | `6.68` | `3.953` | `0.00037` |
| CONGELATO `9000`-`10000` | `0.600` | `6.63` | `3.976` | `0.00049` |

- **a vuoto congelato `w` non cresce** *(`6.68` -> `6.63`, le pendenze per blocco dei due segni, `|.| <= 2.3e-2` per `1000`)*, **l'alone resta a `~5e-4`** *(contro `0.022` col vuoto vivo)*, **il cuore sale appena** *(`0.592` -> `0.600`)*; `D` resta in `B` *(`0.995`-`0.999` da tempo `2500`; a tempo `3` le due corse sono uguali, `B 0.103`, `P0 0.885`)*;
- **col vuoto vivo la differenza c'e' gia' nel primo blocco** *(il cuore `0.460` contro `0.592`, l'alone che cresce da subito con pendenza `1.3e-3` per `1000`)*: **non comincia a `~5000`**; a `~5000` comincia solo la crescita di `w`;
- **la forma, sul tratto `5000`-`10000` del vivo:** l'alone **lineare** *(il rapporto fra le pendenze dei terzi `0.990`; il residuo del fit lineare `3.8e-5`, dell'esponenziale `4.1e-4`)*; per `w` **indecisa** *(il rapporto `1.099`; i residui `7.9e-2` e `8.1e-2`)*;
- **`Lambda` medio sotto il solitone, col vuoto vivo, SALE** *(`6.000` -> `6.221`)*, e lontano scende *(`6.000` -> `5.976`)*; a vuoto congelato resta `6.000`.

**La lettura, per la domanda posta: (c1)** -- l'allargamento non appartiene al solitone su questo vuoto: **senza vuoto vivo non c'e'.** **Ma la parentesi di (c1)** *(«`Lambda` che cala sotto il solitone»)* **NON e' quella misurata:** sotto il solitone `Lambda` cresce di `0.22`. **Il meccanismo resta aperto**, e per questo la classificazione fra (c1) e (c3) **la lascio a Luca**. Con (c2) escluso, il tempo di vita da `w(t)` e la proposta a `L 120` **non servono**; l'estrapolazione dichiarata del vivo *(il cuore sotto meta' a `~15400`, con la pendenza degli ultimi `3000`)* **non e' una misura**.

**Per la decisione `10`:** il fondo `F0` congelato tiene `BG` fermo per `10000`; **vivo, il vuoto stesso si muove** *(su di `0.22` sotto, giu' di `0.024` lontano)* e il solitone si allarga. **Se il fondo diventa vuoto di riferimento, la domanda e' perche' il fondo vivo non resta fermo sotto il solitone.**
