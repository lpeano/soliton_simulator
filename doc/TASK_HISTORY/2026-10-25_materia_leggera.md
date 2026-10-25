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

## 4. IL RISULTATO *(dopo `e188773e`)*

### **IL REFERTO DELLA MATERIA LEGGERA:** `doc/referti_l2/materia_leggera.{txt,jsonl}` *(`csv/_materia_leggera.py` `sha1-BYTE e620f287`, al commit `e188773e`)*. ### ⛔ **`3/6`, UNA DEVE FALLITA** *(la `2` del guardiano, gia' annotata prima della corsa)*: ### **`FERMO`.**

- ### **`L1` TORNA:** ### **`v_b/c = 0.7853982`, `v_max/c = 0.5992864`, `v_max/v_b = 0.7630351`; il prodotto `0.5992864`** *(dal jsonl di `afba052b`)*.
- ### **IL CONTROLLO `3`:** ### **`alpha = beta = 1`, `eps 0` e `s 0.01` danno lo stesso punto** *(`m = W = 1/2`, `v_max/v_b = 0.763035`, `0.763070` a `s 0.01`)*; ### **`alpha = beta = 2` lo stesso `m/W` e lo stesso rapporto** *(scalati insieme NON contano)*. ### **La convergenza di `v_max` fra la griglia `48` e la `96`, dopo l'ottimizzatore: `4.4e-9`.**
- ### ⛔ **IL RIFERIMENTO NON VA A `1`** *(la DEVE `2`: FALLISCE)*: ### **il nido d'ape con la massa di Semenoff ha `v_max/v_b` `0.934`, `1.066`, `1.135`, `1.149`, `1.153`, `1.1545`, `1.1547`, `1.1549` a `m/W` `0.46`, `0.20`, `0.071`, `0.034`, `0.017`, `0.0067`, `0.0033`, `0.0017`:** ### **tende a `2/sqrt(3) = 1.1547`** *(il massimo della velocita' di gruppo del reticolo, a `t = (pi, pi/2)`, non quella del cono)*. ### **MA A MASSA PESANTE ANCHE IL RIFERIMENTO HA `v_max/v_b < 1`** *(`0.934` a `m/W 0.46`)*: ### **la piegatura della banda prima di `v_b` e' GENERICA quando `m` e' paragonabile a `W`.**
- ### **`L2`, LE MANOPOLE DEL MODELLO** *(la chiave `6` del riferimento: PASSA, il rapporto cambia di `0.22`)*:
  - ### **`(a)` `alpha/beta`: `m/W` ha il MINIMO a `alpha = beta`** *(`1.000`; `1.366` a `beta/alpha` `0.5` e `2`; `13.18` a `0.05` e `20`: simmetrico)*: ### **qualunque squilibrio APPESANTISCE la coppia** *(e `v_max/v_b` scende a `0.258`)*.
  - ### **`(b)` `eps`: `m/W` CRESCE** *(`1.003`, `1.019`, `1.076`, `1.298`, `1.659` a `eps` `0.1`-`1.5`)*, ### **`v_b` resta `0.25`, `v_max/v_b` scende a `0.642`.**
  - ### **`(c)` `s`: `m/W` SCENDE fino a `0.508` a `s 0.99`** *(`0.945` a `0.3`, `0.852` a `0.5`, `0.724` a `0.7`, `0.576` a `0.9`)*, ### **e `v_max/v_b` SALE OLTRE `1`** *(`0.972` a `0.7`, `1.157` a `0.9`, `1.272` a `0.99`)*: ### **l'unica manopola che alleggerisce, ma solo di un fattore `2` e solo vicino al limite del cono `B-5`.**
  - ### **`(d)` LO ZERO: `m/W` fino a `0.2`** *(`delta 0.4`)*, ### **MA la banda bassa diventa PIU' pesante** *(`m` `0.1` contro `0.9`, `v_b` `0.112` contro `0.335`)*: ### **rompe l'universalita' fra le bande** *(il prezzo che il mandato chiedeva di riportare)*.
  - ### **`(e)` I TERMINI `S`: su un vuoto uniforme sono uno spostamento dello zero** *(la `(d)`)*; ### **non misurati a parte.**
- ### **`(4)` e `(5)`** *(PUO' FALLIRE: FALLISCONO)*: ### **nessuna manopola arriva a `m/W <= 0.01`** *(il minimo `0.2`, lo zero)*; ### **nessuna rende `m/W < 0.1` restando universale e isotropa** *(l'isotropia vale ovunque: `v_b` lungo `x` e `y` uguali)*.

### **`L4`, LA LETTURA** *(informazione per Luca, non scelte)*: ### **il guardiano aveva ragione sul «non i nodi»** *(gli spettri sono del reticolo infinito)* ### **e sulle due cause** *(gli orologi, `pi/4`; la massa alla grana, `0.763`)*. ### **Con le manopole del modello `m/W` non scende sotto `~0.5`** *(e solo con `s -> 1`)*: ### **la massa della coppia `K/K'` e' fissata dalla STRUTTURA del passo alla scala della grana** *(`mu0 = 1/2` contro `W = 1/2`)*: ### **e' il problema della gerarchia nella forma di questo modello.** ### ⚠ **E la correzione del riferimento cambia la domanda:** ### **anche una massa leggera su un reticolo NON darebbe `v_max = v_b`** *(il reticolo dei triangoli porta il massimo a `2/sqrt 3` del cono)*: ### **la richiesta «la materia lenta non supera la luce» va posta sul MASSIMO del reticolo, non sul cono.** ### **LA PISTA DI LUCA, la massa COLLETTIVA** *(un solitone di molti nodi, la cui massa non e' `mu0` di un nodo)*: ### **resta una domanda aperta, non misurata.**
