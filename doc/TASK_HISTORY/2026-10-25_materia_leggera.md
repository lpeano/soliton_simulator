# LA MATERIA LEGGERA, SULLA CARTA: IL LIMITE `v_max/c` DIPENDE DALLA MASSA RISPETTO ALLA GRANA?

> **Il mandato:** di Luca, `2026-10-25`, con la DECISIONE delle `21:07` *(la misura si fa, dopo la mitosi)* ### **e la sua domanda: «il limite troppo basso della materia rispetto alla luce dipende dal fatto che l'universo non ha abbastanza nodi?»** *([[MATERIA-LEGGERA]], [[LORENTZ-MATERIA-INTERFERENZA]], [[V-MAX-DIREZIONI]])*.
> ### **La risposta del guardiano, DA VERIFICARE:** ### **NO, non il numero dei nodi** *(gli spettri sono del reticolo infinito)*, ### **ma `(1)` gli OROLOGI** *(`v_b/c = pi/4` a `r 1`)* ### **e `(2)` la massa alla scala della grana** *(`v_max/v_b = 0.76304`: `mu0 = 1/2` e' meta' della larghezza della banda)*.
> ### **Sulla carta: il generatore e gli spettri, nessuna dinamica, nessun file del nucleo.** ### **Lo script `csv/_materia_leggera.py`, il referto `doc/referti_l2/materia_leggera.{txt,jsonl}`.**

**LIVELLO:** una misura sugli spettri.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica.** 2. **Il gradino:** ### **la struttura della banda della coppia** *(`m`, `W`, `v_b`, `v_max`)*. 3. **Aggiunge un numero o una legge?** ### **No: esamina le manopole che CI SONO.** 4. **Tocca `c_s`?** ### **No.** 5. **Emergente o imposto?** ### **La domanda e' se la massa della coppia sia fissata dalla struttura del passo.**

## 1. LE GRANDEZZE *(fissate qui)*

- ### **LE UNITA': quelle del generatore** *(`mu`, il tempo proprio in unita' di `pi s` per tick)*: ### **`v_b/s = pi v_b`, `v_max/s = pi v_max`, `c = 1/pi` a `r 1`** *(i referti `afba052b`, `b0edae62`)*.
- ### **`m` = `mu0`, il livello della coppia a `K` dallo zero;** ### **`W` = l'escursione della banda della coppia sulla zona** *(`max - min` di `mu` su quella banda)*; ### **`v_b = sqrt(mu0 mu'')`** *(`mu''` la curvatura a `K`, differenze centrate a `h = 1e-3` lungo `x` E lungo `y`: l'ISOTROPIA = lo scarto fra le due)*; ### **`v_max` = il massimo di `|grad_k mu|` sulla banda: la griglia `48`, poi Nelder-Mead dai `5` punti migliori** *(il metodo di `_curvatura_0bis.vmax_ottimizzato`)*; ### **la convergenza: la griglia `96`, lo scarto sotto `1e-6`.** ### **L'UNIVERSALITA' FRA LE BANDE: `m` e `v_b` della banda ALTA e della BASSA della coppia uguali entro `1e-6`.**
- ### **LA BANDA DELLA COPPIA:** ### **l'indice ordinato che a `K` porta `+mu0`** *(e quello che porta `-mu0` per la bassa)*; ### **il salto minimo con le bande vicine sulla griglia riportato** *(sotto `1e-3` la banda non e' isolata, e si dice)*.

## 2. LE MISURE E I CRITERI

- ### **`L1` LA SCOMPOSIZIONE:** ### **`v_max/c = (v_b/c) (v_max/v_b)` a `r 1`, DAI NUMERI DEL JSONL di `afba052b`** *(`doc/referti_l2/curvatura_0bis_v2.jsonl`, `rapporti["1.0"]`)*.
- ### **`L2` LE MANOPOLE** *(ognuna resta un flusso di proiettore)*: ### **`(a)` `alpha/beta`** *(la famiglia della parte `2`: `beta/alpha` in `0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20`; `alpha = beta` scalati insieme NON contano, e si verifica a `2, 2`)*; ### **`(b)` `eps` della moneta** *(`0, 0.1, 0.25, 0.5, 1, 1.5`)*; ### **`(c)` `s` del tick** *(le fasi `-arg(lambda)/(pi s)` dei blocchi di `_triangoli_forza.blocchi(0, s)`, `s` in `0.01, 0.05, 0.3, 0.5, 0.7, 0.9, 0.99`)*; ### **`(d)` LO ZERO** *(lo spostamento `delta` in `-0.4, -0.2, 0, 0.2, 0.4` da `Z1`: il prezzo e' l'universalita')*; ### **`(e)` I TERMINI `S`** *(`CAMM-MATERIA-VUOTO`: su un vuoto uniforme e' una FASE uniforme per nodo, cioe' uno spostamento dello zero dipendente da `rho`: e' la `(d)`, e NON si misura a parte; DICHIARATO)*. ### **Per ognuna: la curva `v_max/v_b` contro `m/W`, l'isotropia, l'universalita'.**
- ### **`L3` IL RIFERIMENTO:** ### **il Dirac a nido d'ape con la massa di Semenoff** *(`H = [[D, f], [f*, -D]]`, `f = 1 + e^{ik.a1} + e^{-ik.a2}`, il reticolo dei triangoli *(i vicini `0`, `a1`, `-a2`: il punto di Dirac in `K`)*; `D` in `1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005`)*: ### **`m = D`, `W = sqrt(D^2 + 9) - D`, la stessa curva.**
- ### **`L4` LA LETTURA:** ### **quanto piccolo puo' diventare `m/W` con le manopole del modello; se nessuna lo rende piccolo, dirlo.** ### **La pista della massa COLLETTIVA di Luca** *(un solitone di molti nodi)* ### **accennata come domanda, non misurata.**

| | il criterio | il tipo |
|---|---|---|
| `1` | `L1`: il prodotto `(v_b/c)(v_max/v_b)` = `v_max/c` entro `1e-5` *(e i valori `0.785398` e `0.76304`)* | DEVE |
| `2` | `L3`: a `m/W -> 0` la curva tende a `v_max/v_b = 1` *(entro `1e-2` a `m/W <= 0.01`)* | DEVE |
| `3` | il controllo: `(a)` a `alpha = beta = 1` e la `(b)` a `eps 0` e la `(c)` a `s 0.01` *(la correzione del tick e' `O(s^2)`)* danno `m = 1/2`, `W = 1/2`, `v_max/v_b = 0.76304` entro `1e-4` *(lo stesso punto da tre strade)*; `alpha = beta = 2` lo stesso `m/W` e `v_max/v_b` entro `1e-10` | DEVE |
| `4` | ### **per ogni manopola del modello che rende `m/W` piccolo, `v_max/v_b -> 1` entro `1e-2` a `m/W <= 0.01`** | PUO' FALLIRE |
| `5` | ### **esiste almeno una manopola che rende `m/W < 0.1` senza rompere l'universalita' fra le bande o l'isotropia** | PUO' FALLIRE |
| `6` | ### **«`v_max/v_b` non dipende da `m/W`» sul riferimento** | ### **DEVE FALLIRE, PER LA CHIAVE GIUSTA: fra `D = 1` e `D = 0.005` `v_max/v_b` cambia di piu' di `0.1`** |

### **Mi FERMO** ### **se `1`, `2` o `3` fallisce.**

## 2-bis. ANNOTAZIONE, PRIMA DEL COMMIT DELLO SCRIPT E DELLA CORSA *(una prova di costruzione, NON il referto)*

- ### ⚠ **LA PREVISIONE `2` DEL GUARDIANO** *(«il riferimento a `m/W -> 0` tende a `v_max/v_b = 1`»)* ### **NON TIENE, e lo so gia':** ### **nel nido d'ape senza massa il massimo di `|grad |f||` sulla zona e' `1`, a `t = (pi, pi/2)`** *(dove `|f| = 1`)*, ### **mentre `v_F = sqrt(3)/2`: il rapporto e' `2/sqrt(3) = 1.1547`** *(un conto indipendente su `600 x 600`, e la prova dello script a `D = 0.01`: `1.154659`)*. ### **La velocita' di gruppo massima di un Dirac su reticolo NON e' quella del cono: la deformazione trigonale la porta piu' su lontano da `K`.**
- ### **IL CRITERIO NON SI RISCRIVE:** ### **resta la DEVE del guardiano, e FALLIRA'** *(-> `FERMO` dopo il referto, con lo stato committato)*. ### **La lettura di `L4` si fara' contro i DUE riferimenti** *(il cono, `1`; il reticolo, `2/sqrt 3`)*.
- ### **GLI ALTRI NUMERI GIA' VISTI** *(la stessa prova)*: ### **`alpha = beta = 1`: `v_max/v_b = 0.763035`; `eps 0.5`: `m/W 1.076`, `0.7456`; `s 0.3`: `m/W 0.945`, `0.7953`; `beta/alpha` `0.1` e `20`: `m/W` `6.53` e `13.2`; il riferimento a `D = 1`: `m/W 0.462`, `0.9342`.** ### **Le soglie del §2 erano fissate prima, e non cambiano.**

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice *(la voce `MATERIA-LEGGERA`)*.
