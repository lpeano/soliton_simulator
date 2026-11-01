# 2026-11-01 — IL VUOTO VIVO: L'ENERGIA E IL RESPIRO *(il mandato di Luca delle `11:22`, sull'esito di `326747d0`; [[LIBRO-DEI-CONTI]], [[VUOTO-SUL-FONDO]], [[PIANO-2D-3D]]; NESSUNA MODIFICA AL NUCLEO)*

> **La coda** *(Luca `11:31`, PRECEDENZA)*: questo mandato viene **prima** di quelli delle `01:22`, `01:27` e `01:28`. L'ordine registrato: **11:22 → ⑦ (01:22) → ⑧ (01:27 + 01:28).**

## 1. LE PREMESSE DAL CODICE

- **(a) Il vuoto, per ogni `s`?** `_vuoto_vivo_B.scena(s, vuoto, eps)` costruisce tutto **a ogni corsa**: `_diagnosi_s4.configura(FORMA, s, N)` mette `s` in memoria, `_deriva_congelato.prepara(s)` rifa' il risolutore a quel `s`, e `_deriva_congelato.nuovo` chiama `_energia_del_legame.stato`. **Il vuoto pero' NON dipende da `s` per costruzione:** `_solitone_con_la_buca.vuoto_iniziale` mette `phi_h` a `scena_l2.VUOTO_PER_ESTREMITA = 1.0` *(U)* oppure a `_solitone_dal_fondo.fondo_con_fasi(inc, L, F0)` *(F)*: **dipende solo dal grafo** *(`inc`, `L`)*, e `L = 81` a tutti e due i passi. **Credo quindi che (a) non sia la causa** *(e anche in `99eb7a42` il vuoto uniforme era lo stesso a ogni `s`)*; **lo controllo al bit** *(`phi_h` a `s 0.15` = a `s 0.075`)*.
- **(c) La definizione di `H_tot`: QUI C'E' UNA DIFFERENZA, e credo sia la causa.** `_libro_dei_conti.conti_per_nodo` → `_energia_del_legame.per_nodo` → `energia_pesata.termini_di_h(mot, s, PAR)` con **`_energia_del_legame.PAR = {"eps": 0.0}` FISSO**. `termini_di_h` aggiunge per nodo **`eps * mot.elicita(st)`**, il termine della moneta di spin *(`CAMM-MONETA-SPIN`)*. **Le corse girano con `z["par"]["eps"] = 0.5`, ma il libro dei conti conta l'energia come se eps fosse `0`:** il termine della moneta **manca da `H_tot`**. In `99eb7a42` eps era `0` *(`_energia_del_legame.stato`)*, e le due cose coincidevano.
- **(b) Lo stato iniziale:** l'inviluppo non e' un autostato del tick *(il residuo per tick `3.3e-2` a `s 0.15`, `1.7e-2` a `0.075`: scende come `s`)*. **Non so** quanto contribuisca a `H(t) - H(0)` indipendentemente da `s`.
- **Il precedente scritto in `doc/PATTERN_DI_PROVA.md`** *(la cautela del sigillo `(iv)`, `4f6a4bd7`)*: col legame `S1` la deviazione di `H_tot` **non andava come `s^2`** *(rapporto `0.62` fra `s 0.3` e `0.15`)*. **Ma `99eb7a42`, dopo, fra `0.15` e `0.075` misuro' `3.69`** sul totale. Li tengo tutti e due presenti.

### Cosa NON so

- se, col termine della moneta dentro `H_tot`, il rapporto torni fra `3` e `5` **anche** con la partenza dall'inviluppo *(cioe' se (b) pesi)*;
- se l'escursione di `H_tot` a eps `0.5` stia nei primi tick *(lo dice la rilettura dei pezzi committati: il tempo del massimo)*;
- se `BG-F` continuato fino a `10000` tenga il cuore.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `E0` | **La correzione e' una SOLA definizione:** `per_nodo` e `conti_per_nodo` prendono il `par` del tick come argomento **con `_energia_del_legame.PAR` come valore se non passato** *(cosi' ogni chiamata di prima resta uguale al bit)*. **DEVE: col `par` a eps `0`, `tot` = quello di prima, AL BIT** *(il caso nullo)*. **DEVE: col `par` a eps `0.5`, `tot - tot(eps 0)` = `0.5 * sum(elicita)`** *(entro `1e-12` relativo: il termine che manca, e solo quello)*. |
| `E1` | **(a):** `phi_h` della scena a `s 0.15` = a `s 0.075`, **al bit**, per U e per F *(un fatto: se fallisce, (a) diventa un indiziato)*. |
| `E2` | **Le corse brevi, una per `s`, dichiarate:** `BG-U` e `BG-F` a `s 0.15` e `0.075`, **fino a tempo `150`** *(prima della dissoluzione di `BG-U` a `160.5`)*: `1000` e `2000` tick. **DEVE: sono le STESSE corse committate:** `H_tot` del libro *(eps `0`)* ogni `10` tick = i campioni dei pezzi committati, **AL BIT**. |
| `E3` | **IL DEVE DI LUCA, rifatto:** con `H_tot` **col termine della moneta** *(il `par` della corsa)*, il rapporto `max abs(H - H(0))` fra `s 0.15` e `0.075` sul tempo `150`, **fra `3` e `5`**, per `BG-U` e per `BG-F`. Accanto, lo stesso rapporto col libro a eps `0` *(deve ridare il fallimento: un caso che DEVE fallire)*. |
| `E4` | **(b), letto:** sui pezzi committati, il tempo del massimo di `abs(H - H(0))`; sulle corse brevi, `abs(H - H(0))` dopo i primi `10` unita' di tempo e il massimo prima. |
| `R0` | **Il respiro:** `BG-F` a `s 0.15` **continuato dalla fine** *(lo stato di ripresa a tick `20000`: lo sha1 di ogni chiave = `sha_fine` dell'ultimo pezzo committato, DEVE)* **fino a `10000` unita' di tempo** *(tick `66667`)*, a pezzi di `10000` tick committati, la ripresa fra i pezzi al bit *(DEVE)*; `M` e `V` entro `1e-10` *(DEVE)*. Gli stessi campioni di `_vuoto_vivo_B` *(il cuore liscio e netto, `w`, l'alone, il baricentro, `Lambda` sotto e lontano, il libro dei conti, la strada `A`, le bande di `D` ogni `20` tick)*, **piu' `H_tot` col termine della moneta.** |

**Se `E0` o `E2` falliscono: FERMO.** **Se `E3` fallisce col termine della moneta dentro:** si committa, si scrive, e si passa a (h2) *(lo stato vicino al fermo)* solo come pezzo dichiarato **dopo** averlo scritto qui.

## 3. LE LETTURE *(di Luca, scritte prima)*

- **(h1)** era il vuoto non ricalcolato per `s` *(o altro della costruzione)*: corretto, il rapporto torna fra `3` e `5`;
- **(h2)** lo scarto e' dello stato iniziale non fermo: dirlo, e misurare il rapporto su uno stato vicino al fermo;
- **(h3)** altro *(il termine della moneta che manca dal libro dei conti cade qui: e' «altro della costruzione» della MISURA, non della scena)*.
- **(r1)** l'oscillazione del cuore e' limitata *(il minimo non scende sotto `~0.38`)* e l'alone non cresce: il solitone sul fondo e' stabile col vuoto vivo;
- **(r2)** il cuore cala nel tempo: quanto, dove va *(le bande di `D`, il vuoto, l'alone)*;
- **(r3)** altro.

## 4. LE MOTIVAZIONI

Un `H_tot` che non si conserva **toglie valore a ogni lettura energetica** del vuoto vivo *(la strada `A`, dove va la materia)*. E prima di scegliere il vuoto del fondo come vuoto fisico serve sapere **se il solitone ci sta per un tempo lungo**.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. La correzione *(`par` in `_energia_del_legame.per_nodo` e in `_libro_dei_conti.conti_per_nodo`)* e `csv/_energia_vuoto_vivo.py` *(`E0`–`E4`)*, con la riga d'inventario: committati prima di girare.
3. `python csv/_energia_vuoto_vivo.py > doc/referti_l2/energia_vuoto_vivo.txt`; il referto, `RELAZIONE`. **`E0` o `E2` falliti: FERMO.**
4. `csv/_respiro_sul_fondo.py` *(`R0`)*, committato; i pezzi, uno alla volta, ognuno committato; il referto.
5. `doc/CHIUDERE_LE_USCITE.md`; `RELAZIONE`; la `MAPPA` *(la sezione `2` riga `1`: il solitone si scioglie col vuoto UNIFORME, qualunque sia il punto della banda, e regge sul FONDO; la decisione di Luca da prendere: il vuoto del fondo come vuoto fisico del modello)*; la sezione `6` qui. Poi ⑦.

## 6. L'ESITO

### Punto `1`, l'energia *(`doc/referti_l2/energia_vuoto_vivo.txt`, sha1-BYTE `da5bee14`, girato a `029cac81`; `12/12`)*

**Annotazione alle premesse:** (a) **non** era la causa *(il vuoto e' uguale al bit ai due `s`)*; **(c) si'**: il libro dei conti non contava il termine della moneta. **Col termine dentro, il rapporto e' `3.880` (BG-U) e `3.896` (BG-F)**, mentre col libro a eps `0` resta `0.873` e `0.871` *(il caso che DEVE fallire)*. (b) porta un salto nei primi `10` unita' di tempo, ma scala anch'esso col passo. **La lettura e' (h3).**

### Punto `2`, il respiro *(`doc/referti_l2/respiro_sul_fondo.txt`, sha1-BYTE `2893d109`, girato a `f7f9bf77`; `2/2` DEVE)*

**BG-F a `s 0.15` regge fino a `10000`** *(la ripresa da `_vuoto_vivo_B` al bit; `M` e `V` entro `3.9e-11`; `H_tot` col termine della moneta entro `4.1e-5 N |e_K|` sulla continuazione, contro `5.0e-4` col libro a eps `0`)*. **Ma non e' (r1):**

| tempo | il cuore liscio medio | `w` medio | l'alone medio |
|---|---|---|---|
| `3000`-`4000` | `0.509` | `7.92` | `0.0066` |
| `4000`-`5000` | `0.517` | `8.03` | `0.0090` |
| `5000`-`6000` | `0.510` | `8.28` | `0.0115` |
| `6000`-`7000` | `0.491` | `8.64` | `0.0141` |
| `7000`-`8000` | `0.461` | `9.08` | `0.0167` |
| `8000`-`9000` | `0.440` | `9.46` | `0.0192` |
| `9000`-`10000` | `0.416` | `9.86` | `0.0218` |

- **il minimo della continuazione** *(`0.397` a tempo `9537`)* **non scende sotto quello visto fino a `3000`** *(`0.379`)*: questa meta' di (r1) regge;
- **l'alone CRESCE**, regolare, da `0.0055` a `0.0231` *(la pendenza `+2.5e-3` per `1000`)*, e **`w` cresce** da `7.95` a `9.98`: l'altra meta' di (r1) cade;
- **(r2): il cuore cala dopo tempo `~5000`**, da una media di `0.517` a `0.416`. **Dove va:** `D` resta nella banda **`B`** *(`0.95`-`0.99` lungo tutta la continuazione)*: **il solitone si allarga dentro la sua banda, non scappa in altre bande.** Il libro dei conti *(col `par`)* fra tempo `3000` e `10000`: `cin` vicino `-0.0696`, lontano `+0.0519`; **il vuoto lontano `+0.0202`**; il totale `H_tot` `-3.6e-6 N |e_K|`. **La materia e la sua energia escono dal disco, e una parte va al vuoto lontano**; la strada `A` sul disco: netto `-0.0606` *(entrate `+0.733`, uscite `-0.794`)*.
- **Non so** se il calo continui fino alla dissoluzione, ne' con che legge *(lineare o esponenziale)*: la finestra e' **un solo tratto di discesa**, e **non c'e' un secondo passo `s`** per la continuazione.

**La lettura e' (r2)**: sul fondo il solitone vive **molto piu' a lungo** che sul vuoto uniforme *(oltre `10000` contro `160`)*, **ma non e' fermo**: dopo `~5000` si allarga lentamente dentro la banda `B`, e cede materia e energia al lontano e al vuoto.

### Punto `3`, la MAPPA

La sezione `2` riga `1`, la riga `d` della sezione `3`, e **la decisione `10` nella sezione `5`** *(il vuoto del fondo come vuoto fisico del modello: di Luca)*.
