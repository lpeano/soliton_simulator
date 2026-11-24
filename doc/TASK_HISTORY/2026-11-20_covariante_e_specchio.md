# LA COVARIANTE, LA FAMIGLIA D7-COVARIANTE E LO SPECCHIO VERO *(il mandato unico di Luca `2026-11-20` `11:57`)*

> **Da dove:** la carta della mitosi sez. `16.5` *(la famiglia `alpha` senza radice su `2929` archi su `2929`; il perche': `k` e `l` con `psi = 0`, l'arco diviso che porta via il suo termine)*. [[MITOSI-QUANTO-OLONOMIA]]
> **La decisione di Luca** *(`11:57`)*: **si allarga la famiglia verso la COVARIANTE**, che mette `psi` anche sulle estremita' nuove in `k` e in `l`. **Prima E2** *(la covariante da sola)*, **poi la famiglia D7-covariante con la radice.** Il mandato delle `10:31` e le aggiunte delle `10:41` e `10:47` restano; **D-PRINCIPIO resta aperta.**
> **Le scelte del guardiano** *(su delega)*: S1 la covariante esplicita su `k` e `l`; S2 la famiglia `beta`; S3 lo specchio vero, col caso che deve fallire costruito apposta.

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

### 1.1 LA COVARIANTE *(S1)*: E' QUELLA DELLA `6.3`, RESA ESPLICITA

- **Confrontata con la `6.3` della carta delle `10:31`: COINCIDE** *(le estremita' di `n` = la media di quelle di `i` e di `j` nella stessa direzione; quella nuova di `k` = la media delle estremita' di `k` verso `i` e verso `j`; lo stesso per `l`; in `i` e in `j` il trasporto; un fattore uniforme sulla stella per `psi` e uno per `phi`)*. **Nessuna differenza da dichiarare.**
- **Sul codice** *(gli indici di `nasci`: gli archi nuovi `n -> i, j, k, l` in coda, l'estremita' pari in `n`)*: `n -> j` in `n` = `(e(i -> j) + e(j -> j+))/2` *(`j+` il vicino di `j` in `+a`, `regole_fase_F3.opposto`)*; `n -> i` in `n` = `(e(j -> i) + e(i -> i-))/2`; `n -> k` in `n` = `(e(i -> k) + e(j -> k))/2`; `n -> l` lo stesso; **in `k` sull'arco `n -> k`** = `(e(k -> i) + e(k -> j))/2`; in `l` lo stesso; in `i` e `j` il trasporto *(la `psi` di PRIMA, senza D7)*. **La stella:** le estremita' dei nodi `i, j, k, l, n` dopo la nascita; **il fattore `sqrt(N_prima / N_dopo)`**, `N_prima` la norma sulle estremita' di `i, j, k, l` prima. **Se `N_prima = 0`** *(il vuoto puro per `psi`)*: nessun fattore *(resta `0`)*.

### 1.2 LA FAMIGLIA `beta` *(S2)*

- **Solo sulle estremita' della STELLA:** `psi = (1 - beta) D7 + beta COV`, **poi il fattore `sqrt(N_D7 / N_misto)`** con `N_D7` la norma di D7 sulla stella *(fuori dalla stella D7 e COV sono la stessa `psi`, e NON si mescolano: `(1 - beta) x + beta x` non e' `x` al bit)*. **A `beta = 0`:** `1.0 D7 + 0.0 COV = D7` e il fattore `1.0`: **D7 AL BIT** *(il caso noto: `regole_fase_F3.nascita(..., "FA")`)*. **D7 conserva la norma della stella** *(sposta meta' della norma del padre sul nodo nuovo, dentro la stella)*: **`N_D7 = N_prima` all'arrotondamento** -- dichiarato *(il fattore usa `N_D7` perche' a `beta = 0` sia `1.0` esatto)*. **`phi` = FA per tutta la famiglia** *(D-M3)*. **`beta = 1` = la covariante con `phi` FA:** **si stampa quanto differisce da E2** *(che ha anche `phi` covariante)*.
- **La radice:** bisezione a `53` passi fissi sul conto a mano *(`nascita_energia_nulla.F_mano`)*; alla radice il conto pieno.

### 1.3 LO SPECCHIO VERO *(S3)*

- **La prova:** **nascere sull'arco `a` e poi applicare lo specchio** *(i nodi con `sigma`, il nodo nuovo su se stesso)*, **contro specchiare lo stato e nascere sull'arco specchiato.** **Il confronto e' ARRAY PER ARRAY:** ogni estremita' del grafo nato si ritrova nell'altro per la coppia di nodi `(sigma(u), sigma(v))` *(il grafo e' semplice: una coppia, un arco)*; `max |psi_A - psi_B| / max |psi_A|` e lo stesso per `phi`. **Lo spinore NON si trasforma** *(come nel referto delle `10:31`: la regola e' covariante per un unitario globale; `fase` per il segno e il coniugio)*.
- **Le regole provate:** D7 *(FA)*, COV *(E2)*, la radice della famiglia `beta`, **la D7 SIMMETRICA** *(la proposta del mandato, misurata ACCANTO: ognuno dei due capi da' un QUARTO della sua norma al nodo nuovo, `n` riceve `N_i/4 + N_j/4` nella direzione di `chi_i + chi_j`; nessun padre)*, **e il CASO CHE DEVE FALLIRE: D7 col padre = il nodo di INDICE MINORE** *(una regola che dipende dalla numerazione: lo specchio cambia la numerazione)*. **La soglia:** `1e-10` relativo *(la tabella P5)*; **il caso che deve fallire DEVE dare piu' di `1e-6` su almeno un arco**, **o la prova non vale: FERMO.**
- **Separato per classe di direzione:** gli archi che lo specchio ROVESCIA *(una direzione su tre)* contro gli altri.
- **I campioni:** i primi `200` archi nell'ordine di scatto *(come alle `10:31`)*.

### 1.4 COSA NON SO

- **Il caso noto fisico di E2** *(scritto PRIMA: quale numero)*: **sul vuoto F3 puro** *(la scena S162, `psi = 0`, l'arco di `regole_fase_F3.py`)* **la covariante deve lasciare invariata l'energia PER NODO: `DH_cov = H / n`**, con `H` del vuoto di S162 e `n` i suoi nodi *(il toro della scena: lo stampa lo script)*; **lo script stampa il numero `H / n` e `DH_cov` accanto.** ### ⚠ **Credo che NON torni:** il vuoto F3 ha fasi diverse per classe di direzione, la media di due estremita' di direzioni diverse ha un modulo minore, e la stella ha un `4`-`7`-`7`. **E' una previsione, non un caso noto del codice.**
- **Il caso noto del CODICE** *(Q-A4, deve passare)*: **su un campo UNIFORME** *(ogni estremita' lo stesso spinore e lo stesso `phi`)* **le estremita' nuove della covariante, PRIMA del fattore, sono quel valore AL BIT** *(la media di due uguali e' esatta)*; e **`beta = 0` = `regole_fase_F3` FA al bit** *(`psi` e ogni termine)*.
- **Non so** se la radice in `beta` esiste: serve `DH(beta = 1) > 0`, cioe' una covariante con `phi` FA che ALZI l'energia.

## 2. PROGETTAZIONE *(i passi; cosa mi farebbe FERMARE)*

1. **Lo script nuovo** `doc/referti_l2/covariante_e_famiglia.py` *(importa `nascita_energia_nulla.py`, non lo tocca)*: `parte K 2` *(i `2929` archi: E2 scomposta per termine, D7, `DH(beta)` su `11` punti, `beta*`, il conto pieno alla radice, la D7 simmetrica)*; `det a|b` *(i primi `100` e la fila di `20`)*; `specchio` *(S3)*; `referto`. **Commit prima delle corse.** `2` parti + `2` del determinismo + `1` dello specchio = **`5` processi**, il registro per ciascuno.
2. **FERMO se:** il caso noto del codice fallisce; **il caso che deve fallire dello specchio NON fallisce.**
3. **Il referto** `doc/referti_l2/covariante_e_famiglia.txt`; **la sez. `17` della carta della mitosi** con le previsioni VERE/FALSE. **Se la radice c'e' su almeno l'`80%` E la radice e' simmetrica allo specchio:** scrivere che i TODO `4`-`5` delle `10:31` possono ripartire con `beta`, **ma NON ripartirli. FERMO per Luca.**
4. **Se D7 non e' simmetrica:** nessuna correzione decisa; **la D7 simmetrica misurata accanto** *(1.3)*.

## 3. LE PREVISIONI *(copiate PRIMA delle misure)*

- **P-C1.** La covariante mette ampiezza in `k` e `l` e recupera gran parte della caduta: `|DH_cov|` mediano nel guscio sotto il `30%` di `|DH(D7)|` *(mediana `-555`)*.
- **P-C2.** La famiglia `beta` ha la radice su almeno l'`80%` dei `2929` archi.
- **P-C3.** D7 NON e' simmetrica allo specchio sulla classe di direzione rovesciata; la covariante lo e' su tutte.
- **P-C4.** Alla radice la nascita e' deterministica al bit e, nelle `20` in fila, `|H(dopo) - H(prima)| / |H|` resta sotto `1e-10`.
- *(P-E2 delle `10:47`, `DH_cov` negativo su piu' della meta', resta come scritta.)*
- ### **LE MIE, accanto:** **P-C1: non lo so** *(la covariante riempie `k`, `l`, `n`: il termine di nodo dovrebbe tornare; ma il fattore uniforme sulla stella abbassa le ampiezze di tutti)*; **P-C2: non lo so** *(serve che la covariante ALZI l'energia)*; **P-C3: VERA** *(la mia premessa del `16.2`)*; **P-C4: deterministica VERA; la fila VERA se la radice c'e'.** **P-E2: non lo so.**

## 4. TODO

1. questa carta: commit, push;
2. lo script: commit, push; le `5` corse col registro;
3. il referto, la sez. `17`: commit, push; **FERMO.**

## 5. LA CORREZIONE DI LUCA DELLE `12:10` *(prima della misura di E2; la 1.4 sopra NON si riscrive: si annota)*

- ### **IL CASO NOTO FISICO DELLA 1.4 E' MAL POSTO** *(l'errore `n.191` del guardiano)*: **la covariante RIPRISTINA la norma, e a norma fissata l'energia del vuoto non dipende dal numero dei nodi** *(A3, carta della mitosi `13.3`)*. **L'attesa NON e' `DH_cov = H / n`.**
- **Il caso noto fisico diventa:** **sul vuoto F3 puro `DH_cov` vicino a `0`**, con un residuo atteso dalle estremita' nuove di `k` e `l` *(la media di due direzioni con fasi F3 diverse ne riduce l'ampiezza)*; **accanto, la sola parte dovuta a `k` e `l`:** la covariante con `k` e `l` presi da UNA direzione *(verso `i`, e accanto verso `j`)*. **Se quella parte spiega il residuo, il caso e' letto: POST-HOC, dichiarato.**
- **Dove:** `covariante_e_famiglia.py` **e' IN USO dalle `5` corse** *(partite alle `12:07`)* **e non si tocca**: la riga del suo referto sul vuoto F3 *(«`DH_cov = H / n`», un DEVE)* **resta stampata, ed e' SUPERATA da questa correzione**: **il suo verdetto non conta.** **Il caso corretto: uno script NUOVO,** `doc/referti_l2/covariante_vuoto_F3.py`, col suo caso noto del codice *(la covariante ricomposta = `cov_grezza` al bit)*.
- **Il caso noto del CODICE resta quello che deve passare** *(il campo uniforme al bit; `beta = 0` = FA al bit)*. **Nient'altro cambia.**

## 6. L'ESITO E LE ANNOTAZIONI *(le premesse sopra NON si riscrivono; i numeri nella carta della mitosi, sez. `17`)*

- **1.2, «non so se la radice in `beta` esiste»:** **sul `6.73%`** *(`197` archi, al bordo esterno del guscio)*. **FERMO.**
- **1.3, lo specchio:** **la prova vale** *(il padre a indice minore fallisce: `0.51`)*. **D7 asimmetrica sui `68` rovesciati; la covariante simmetrica su tutti; e FA, da sola, asimmetrica sui rovesciati** *(la D7 simmetrica ha `psi` simmetrico e `phi` no)*: **una premessa che non avevo scritto.**
- **1.4, il caso sul vuoto:** mal posto *(sez. `5`, l'errore `n.191`)*; **il caso corretto: `DH_cov +0.034`, con `k` e `l` ANNULLATI dalla media** *(fasi opposte)*: **letto post-hoc.**
- **La fila della v1 e' caduta:** la covariante non e' definita accanto a un difetto gia' nato; **la v2** *(`covariante_det_v2.py`)* salva prima e conta i saltati *(`2`)*.
