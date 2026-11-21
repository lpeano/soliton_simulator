# L'ORIENTAMENTO COMBINATORIO: LA CURA DEI TRIANGOLI DEGENERI *(il mandato di Luca `2026-11-21` `22:12` e la sua aggiunta; i rami `mitosi` e `mitosi-chi`)* [[PROGETTO-MITOSI]]

## 0. IL MANDATO *(copiato)*

**PREMESSE**
- Il ramo MITOSI e' caduto alle `20:10` alla decima nascita *(`cef41cbd`)*. In `u1_generico.CampoGenerico._placchetta` il triangolo `(13482, 34601, 34605)` ha il prodotto vettoriale dei vettori d'arco **ESATTAMENTE 0**. La chiamata viene da `mitosi_regola.candidato` -> `cresci` -> `_topologia`.
- **Lettura del guardiano, da verificare:** i «vettori d'arco» sono i versori V3 *(`self.vec`)*. La regola delle estremita' li COPIA *(`n -> i = j -> i`)*. Nascite in fila sulla stessa «linea» danno quindi versori identici: lo zero esatto e' strutturale, non un caso, e tornera' piu' spesso al crescere delle nascite.
- Oggi l'orientamento di ogni triangolo *(il verso del giro e il segno del flusso di `A`)* si decide dal segno di un prodotto vettoriale. Lo spazio e' relazionale: i legami non hanno lunghezza e le posizioni servono a disegnare. **L'orientamento deve venire dalla combinatoria.**
- Lo stato `k 36250` del ramo MITOSI c'e' *(sha1 `64999c5b`, `n 34605`)*. Il ramo C2-EXT prosegue e NON va toccato. Il ramo `mitosi-chi` usa la stessa regola: senza cura cadra' allo stesso modo.
- Valgono tutte le regole: nucleo intatto; script in uso mai riscritti *(file nuovi, v2...)*; un commit e un push per pezzo; previsioni prima; post-hoc dichiarati; al massimo `5` processi con `1` filo; R-AMBIENTE; R-QUALITA'.

**LE SCELTE**
- **DECISIONE DI LUCA: cura (a).** Ogni triangolo nuovo EREDITA l'orientamento *(l'ordine ciclico)* dai triangoli da cui nasce. Alla nascita sull'arco `(i, j)` con la stella `i-k-j-l`: nel ciclo del triangolo vecchio si sostituisce `i` oppure `j` con `n`. Al flip del quadrilatero `n-x-m-y`: l'ordine ciclico del quadrilatero si ricava dai due triangoli orientati che condividono la diagonale vecchia, e i due triangoli nuovi lo seguono.
- **DECISIONE DI LUCA:** scartate (b) «scartare i candidati degeneri» e (c) «spostare i versori».
- **Del guardiano su delega di Luca:** a `k 0` l'orientamento si prende UNA volta dalla geometria del reticolo triangolare regolare *(dove non ci sono degeneri)*, poi solo eredita'; l'orientamento va nello STATO salvato *(la ripresa non lo ricalcola dalla geometria)*; `_placchetta` nuova SENZA prodotto vettoriale; la sorgente e i segni restano come oggi, presi dal ciclo ereditato.

**TODO**
- **T0. Diagnosi SENZA corse**, dallo stato `k 36250`: quale arco scatta alla decima; quale candidato di flip; i versori dei due archi *(uguali al bit? da quale copia vengono?)*; la storia del nodo `34601`. **AL POSTO DELL'ELENCO DEGLI USI DI `vec` (l'aggiunta):** **il censimento A17 dell'era 2**, sul modello di `_censimento_pos.py`, in un file NUOVO: ogni lettura di `vec`/versori E di posizioni nei due rami, con la riga, DIRETTO/INDIRETTO, e per ognuna «decide fisica si'/no»; il referto dentro `degenere_diagnosi.txt`. Referto `doc/referti_l2/degenere_diagnosi.txt`. **Se versori o posizioni decidono altra fisica oltre all'orientamento delle placchette: FERMO e relazione** *(e' un'altra decisione di Luca)*.
- **T1.** La carta *(prima del codice)*: la regola di eredita' per nascita e flip, per esteso; dove vive nello stato; le prove.
- **T2.** Il codice in file NUOVI *(`u1_generico_v2.py` o equivalente; `mitosi_regola_v2` se serve; lo specchio e il lanciatore che puntano alle versioni nuove)*.
- **T3.** Le prove: **O1** *(su `k 36250` l'orientamento ereditato lungo le `9` nascite = quello di oggi, `0` differenze)*; **O2** *(dal tronco `k 35976` col codice nuovo fino a `k 36250`: lo stato al bit con `64999c5b`; Q-P1 dichiarato prima, circa `274` tick x `4.7` s piu' le nascite)*; **O3** *(da `k 36250` la decima nascita passa; P1, P3, P9 a `0`, F3 a ogni nascita)*; **O4** *(deve fallire: un triangolo col ciclo invertito a mano -> F3 o P3 cadono)*; **O5** *(P8 col codice nuovo, orientamento compreso, al bit; un byte cambiato -> la ripresa rifiuta)*.
- **T4.** Se O1-O5 passano: il ramo MITOSI riparte da `k 36250` col codice nuovo *(registro: voce nuova, la vecchia resta FALLITO)*. C2-EXT non si tocca.
- **T5.** Il ramo `mitosi-chi`: la stessa cura *(file nuovi)*; le nascite forzate *(guscio e `r 30`: `DH -1.192932` e `+0.279569` al bit)* e P8. Poi il resto del mandato delle `19:40`.
- **T6.** Lo stato della corsa lunga del mattone con `chi`: una riga nella relazione, solo lettura.

**CRITERI:** il nucleo intatto *(`git diff --stat 42638304 -- primo_ordine`: solo `_mappa.yaml` e `motore_numba.py`)*; O1 con `0` differenze, O2 al bit: senza questi niente ripresa; P9 a `0.0` e F3 a ogni nascita; nessun AssertionError di degenere; ogni numero dai referti.

**PREVISIONI DEL GUARDIANO** *(scritte prima)*
- **P-O1:** i due archi del triangolo degenere hanno versori uguali al bit, copiati da `n -> i = j -> i` *(o dal flip)*, non uguali per caso numerico. Fiducia `80%`.
- **P-O2:** O1 da' `0` differenze; O2 e' al bit. Fiducia `85%`.
- **P-O3:** i versori decidono solo l'orientamento delle placchette *(e il disegno)*, non l'ordine delle estremita' nel passo della camminata. Fiducia `60%`. **Se falso: FERMO.**
- **P-O4:** la decima nascita passa ed e' nel guscio, a `r` fra `18` e `20`.
- **P-O5:** nel ramo `mitosi-chi` le nascite forzate ridanno gli stessi `DH` al bit col codice nuovo.
- **P-O6** *(l'aggiunta)*: oltre a `_placchetta`, il censimento trova letture che decidono fisica in `mitosi_regola`, nella scelta dei candidati o del flip. Fiducia `50%`.
- **La premessa in piu' dell'aggiunta:** A17, la revisione relazionale dell'8/10 *(`a34cc48c`)*: «nelle formule della fisica non ci deve essere `pos`»; i cicli dell'era 1 erano gia' combinatori. **I versori V3 sono una geometria nascosta: la cura (a) e' A17 applicata all'era 2.**
- **FINE:** FERMO dopo T6, oppure prima se T0 trova che i versori decidono altra fisica.

## 1. LE PREMESSE DAL CODICE *(cosa credo PRIMA del referto, e cosa NON so)*

1. ### **CI SONO DUE GEOMETRIE, NON UNA** *(lette nel codice prima di girare niente)*:
   - **`CampoGenerico.vec`** *(`csv/solitone/u1_generico.py`)*: **un vettore 2D per ARCO**, il «vettore d'arco» del campo. **E' quello del prodotto vettoriale che e' caduto** *(`_placchetta`: `dy = _verso(vec, ii, adj[x][y], x)`, `dz = ...`, `cr = dy x dz`)*. Alla nascita *(`mitosi_regola.candidato`)*: gli archi nuovi `n -> i`, `n -> j`, `n -> k`, `n -> l` hanno `-va/2`, `+va/2`, `v(i,k) - va/2`, `v(i,l) - va/2` *(`va` il vettore dell'arco diviso: il PUNTO MEDIO)*; al flip `v(n,x) + v(x,m)`. **NON sono copie: sono somme di vettori d'arco** *(la costruzione del punto medio)*.
   - **`Motore.geo.n`** *(`primo_ordine/motore.py`, `Geometria`)*: **un versore 3D per ESTREMITA'** *(due per arco)*. Alla nascita *(`nasci_array(..., "versore")`)*: le due estremita' di `a` sono TRASPORTATE *(l'estremita' `n -> i` riceve quella di `a` in `j`, cioe' `j -> i`: **la copia «`n -> i = j -> i`» della lettura del guardiano e' QUESTA**)*, le altre le MEDIE NORMALIZZATE; al flip `+v`, `-v` *(la differenza normalizzata delle medie)*.
   - **Quindi la lettura del guardiano mette insieme le due:** la COPIA e' nei versori `geo.n`; il prodotto vettoriale che cade e' sui vettori d'arco `vec`. **Il referto lo deve dire coi numeri** *(P-O1 si decide su `vec`, e accanto si stampano i `geo.n` delle stesse estremita')*.
2. ### **`geo.n` ENTRA NELLA FISICA DEL MOTORE** *(letto, non ancora censito)*: **la moneta di spin** `exp(- i ang (sigma . n))` *(`Motore._ruota_attorno_a_n`, `nx, ny, nz = self.geo.n[...]`)* e **l'elicita'** `h = s . n` *(`Motore.elicita`, «e' qui che la geometria entra nella saturazione»)*. **Se il censimento lo conferma, P-O3 e' FALSA nel senso del mandato** *(i versori decidono altra fisica oltre all'orientamento delle placchette)* **e T0 finisce con un FERMO.** ### **NON SO** se Luca considera `geo.n` una «posizione» *(A17)* o una variabile di stato come `U`: e' la decisione che il FERMO gli porta.
3. **`vec` fuori da `_placchetta`:** lo uso del costruttore e di `cresci` *(segue la crescita)*; `w = s_a^2 hodge_a` e `AREA` NON lo leggono *(costanti)*. Il censimento lo dice per riga.
4. **Le posizioni** `Z["m1"]`, `Z["m2"]` *(`csv/solitone/posizioni.py`, B4)*: le leggono le misure *(`raggi`, `misure_su`, il centro)*, il luogo delle nascite *(D3)*, il disegno. **NON SO** se qualcosa nella regola o nel passo le legge: il censimento lo dice.
5. **La scelta del flip** *(P-O6)*: `mitosi_regola.regola` sceglie per ENERGIA *(il minimo di `H` dei quattro candidati)*; **l'energia dipende da `geo.n`** *(l'elicita' entra nel conto per nodo?)* **e da `U`** *(la `A` del flip: la media dei due cammini)*. Se il conto legge `geo.n`, la scelta del flip e' decisa INDIRETTAMENTE da una geometria: il censimento lo marca INDIRETTO.

## 2. LA PROGETTAZIONE DI T0 *(le letture fissate PRIMA dei numeri)*

### 2.1 LA DIAGNOSI DALLO STATO `k 36250` *(nessun tick)*

- **Lo stato:** `E:/soliton_simulator/controllo/mitosi_rami/MITOSI/stato_36250.npz`, ripreso con `mitosi_lunga.riprendi` *(il grafo cresciuto, la sha1)*; il lapse acceso come nella corsa *(`PS.PO.accendi(cs)`)*.
- **L'arco della decima:** **senza tick non si sa quale arco scatta dopo `k 36250`** *(Theta cresce ancora)*: **si cercano i candidati** = gli archi la cui stella *(`i, j, k, l` di `mitosi_regola.indici_nascita`)* contiene `13482` o `34601`, in ordine di `|Theta|` decrescente; per ciascuno **la regola intera** *(`mitosi_regola.regola`)* **con `_placchetta` sorvegliata** *(un involucro IN MEMORIA, nel solo processo della diagnosi, che registra `x, y, z`, i due archi, i due `vec`, il prodotto e rilancia: NESSUN file toccato)*. **L'arco della decima = il primo che riproduce il triangolo `(13482, 34601, 34605)`**; il referto stampa `|Theta|` e il ritmo *(`|Theta| / k`)* per dire quanto vicino era a `2 pi`.
- **Quale candidato:** la sola nascita o quale dei quattro flip *(il lato)*.
- **I due vettori d'arco:** i valori, **uguali al bit? paralleli con quale rapporto?**; **la provenienza:** l'arco `13482 - 34601` *(nato alla sesta nascita? con quale formula: `+-va/2`, `v(i,c) - va/2`, o il flip)*, l'arco `13482 - 34605` del candidato *(la formula)*; **accanto, i versori `geo.n` delle stesse estremita'.**
- **La storia del nodo `34601`:** la nascita che lo ha creato *(`nascite_36250.json`: `k`, `i, j, k, l`, il flip)*, i suoi vicini, le nascite successive che lo toccano.
- **Le letture:** **P-O1 VERA** se i due `vec` del triangolo sono uguali al bit *(o opposti al bit)* e la provenienza e' una formula di copia/trasporto; **«paralleli per costruzione»** se il rapporto e' un numero razionale semplice dalla formula *(es. `va/2` e `va`)*; **«per caso numerico»** altrimenti.

### 2.2 IL CENSIMENTO A17 DELL'ERA 2 *(`csv/_test_fork/_censimento_a17_era2.py`, NUOVO)*

- **Cosa cerca, nell'AST:** le LETTURE di **`vec`** *(attributo `.vec`, chiavi `"campo_vec"`)*, di **`geo.n`** *(`.geo.n`, `"geo_n"`, `Geometria(`)*, delle **posizioni** *(`Z["m1"]`, `Z["m2"]`, `raggi(`, `centro_di(`, `toro.scarti(`, `posizioni.`)*.
- **Dove:** i file del cammino delle due corse: `primo_ordine/` *(la chiusura degli import del motore: `motore.py`, `tick.py`, `flussi_parziali.py`, `energia_pesata.py`, `termini/*.py`)*, `csv/solitone/` *(`u1_generico.py`, `posizioni.py`, `contatore.py`, `conti.py`, `_u1_oggi.py`, `p6_u_breve.py`, `porto.py`, `mattone.py`)*, `doc/referti_l2/` *(`mitosi_regola.py`, `mitosi_corsa.py`, `mitosi_lunga.py`, `mitosi_rami.py`, `controllo_senza_bordo.py`; e sul ramo `mitosi-chi` `chi_tick.py`, `mitosi_chi_v4.py`)*.
- **Per ogni lettura:** il file, la riga, la funzione; **DIRETTO** *(la funzione la legge)* / **INDIRETTO** *(la legge una funzione che essa chiama, nel grafo delle chiamate di QUEL file e dei moduli del cammino)*; **«decide fisica si'/no»** = **un CAMPO scritto a mano in una tabella dello script, per funzione, col perche'** *(DECISIONE-VUOLE-UN-CAMPO)*: **lo strumento TROVA, la tabella DICE; una lettura in una funzione non in tabella fa ALZARE lo strumento** *(nessun «no» per omissione)*.
- **La regola del FERMO** *(fissata qui)*: **se una funzione che decide fisica** *(il passo del motore, il conto dell'energia, la regola della nascita o del flip)* **legge `geo.n` o le posizioni**, oltre a `_placchetta` che legge `vec`: **FERMO** e relazione.

## 3. TODO

1. questa carta: commit, push;
2. `doc/referti_l2/degenere_diagnosi.py` e `csv/_test_fork/_censimento_a17_era2.py` *(nuovi)*: commit; l'inventario per il secondo *(`doc/INVENTARIO_strumenti.md`)*;
3. le due corse *(un processo alla volta)*; il referto `doc/referti_l2/degenere_diagnosi.txt` *(la diagnosi e il censimento)*: commit, push; la relazione qui e su `primo-ordine`;
4. **se il censimento conferma la premessa 2: FERMO per Luca** *(con T6, una riga di stato, solo lettura)*; altrimenti T1.

## 3. IL MANDATO DOPO IL FERMO DI T0 *(Luca `2026-11-21` `23:13`, e l'aggiunta M3)*: LE CURE D1-D3 E LE MISURE DELLE COPPIE 5-7 *(scritta PRIMA dei numeri)*

### 3.1 IL MANDATO *(in breve; il testo intero e' nel messaggio di Luca, copiato nella relazione del ramo principale)*

- **D1** *(Luca)*: `geo.n` e' uno STATO DELLA RELAZIONE *(come `U`; una tetrade discreta)*, non una posizione: resta nella fisica *(la moneta, l'elicita')* con le sue regole di nascita di oggi. **«A17 vieta le posizioni del disegno, non gli stati locali della relazione».**
- **D2** *(Luca)*: `vec` esce dalla fisica: (a) l'orientamento di ogni triangolo e' EREDITATO; (b) in `indici_nascita` `k` *(e `l`)* dall'ordine ciclico ereditato della stella *(`k` = il terzo vertice del triangolo orientato che contiene l'arco nel verso `i -> j`; `l` quello dell'altro)*, senza prodotto vettoriale; (c) `vec` resta SOLO per il disegno e le misure.
- **D3** *(Luca)*: `kappa` resta il NUMERO di oggi *(`2.529e-4`, al bit come nello stato e nei referti)*, costante; `parametri()` non lo ricalcola piu' da una posizione; `c0 = kappa m0` come oggi.
- **La nascita come coppia di difetti** *(5 e 7, `+60` e `-60` gradi)*: si MISURA, nessuna legge.
- **TODO:** C1 *(questa carta, la sez. `4`)*; C2 *(il codice nuovo)*; C3 *(O1-O5, O7, O8)*; C4 *(il ramo MITOSI riparte)*; C5 *(il ramo `mitosi-chi`)*; **M1** *(le coppie 5-7)*; **M2** *(il raggruppamento)*; **M3** *(gli angoli, l'aggiunta)*.
- **PREVISIONI DEL GUARDIANO:** P-C1 *(O1 `0` differenze anche per `k`/`l`, `85%`)*; P-C2 *(O2 al bit; la decima nascita nel guscio, `80%`)*; P-C3 *(O8 al bit, `95%`)*; **P-M1** *(dopo una nascita isolata un 5 e un 7 a distanza `1`, `85%`)*; **P-M2** *(a `k 36250` le `8` coppie tutte a distanza `<= 2`, `70%`)*; **P-M3** *(la curvatura netta nella palla di raggio `18` e' `0` a `k 36250`, `75%`)*; **P-M4** *(il raggruppamento oltre il caso: `p < 0.01`, `65%`)*; **P-M5** *(le `9` nascite entro `10` gradi da un asse; `p < 0.01`, `75%`)*; **P-M6** *(fra i `20` archi piu' maturi a `k 36250`, archi vicino ad almeno due ALTRI assi, `0`, `60`, `120`, `240` gradi, `65%`)*.
- **FERMO** dopo C5 e M2, o prima se O1, O2 o O8 non passano.

### 3.2 LE DEFINIZIONI DELLE MISURE *(mie, fissate qui; sola lettura)*

- **Gli stati:** il ramo MITOSI `k 36000` *(UNA nascita: la prima, a `k 35976`)* e `k 36250` *(nove)*; il grafo dello stato *(`ii`, `jj`)*, le posizioni del disegno `m1`, `m2`.
- **La sorgente:** il nodo piu' vicino *(nel disegno)* al centro della materia `toro.centro(rho)` *(la regola di `mitosi_rami`: `argmin raggi(Z, centro_materia)`)*.
- **M1:** il grado di ogni nodo; i nodi di grado `!= 6` col grado, i passi dalla sorgente e `r`; **l'accoppiamento:** per ogni 5 il 7 piu' vicino in passi *(e viceversa)*; **legate** a distanza `1`, **vicine** `2-3`, **separate** `> 3`; **la curvatura netta** `somma (6 - grado) x 60` gradi nelle palle di passi `5, 10, 15, 18, 20, 25` dalla sorgente. **IL CASO NOTO (DEVE):** il toro iniziale *(`186 x 186`)*: tutti i gradi `6`, la curvatura `0` in ogni palla. **P-M1 si legge sullo stato `k 36000`** *(una nascita vera, non forzata: dichiarato)*: VERA se esattamente un 5 e un 7 a distanza `1` e nessun altro difetto. **P-M2 VERA** se a `k 36250` ogni 5 ha il suo 7 piu' vicino a distanza `<= 2`. **P-M3 VERA** se la curvatura nella palla di raggio `18` e' `0`.
- **M2:** i nodi nati *(`nascite_36250.json`, `n`)* sul grafo di `k 36250`; **la statistica** `S` = la media, sulle nascite dalla seconda, della distanza in passi dalla nascita PRECEDENTE piu' vicina; **il confronto:** `10000` estrazioni *(seme `20261121`)* di `9` nodi distinti a caso fra i nodi ORIGINARI con `r` in `[17.5, 19.5)` *(l'anello `18-19`)* sullo stesso grafo, la stessa `S`; **`p` = la frazione delle estrazioni con `S <= S` osservata.** **P-M4 VERA** se `p < 0.01`.
- **M3:** l'angolo di ogni nascita *(il nodo nato)* attorno alla sorgente, nel disegno *(`m1 a1 + m2 a2`, l'immagine minima)*; **la distanza dall'asse del reticolo piu' vicino** *(i multipli di `60` gradi: le direzioni di `a1`, `a1 + a2`, `a2`)*; **la statistica** = il MASSIMO delle `9` distanze; il confronto come in M2 *(gli stessi `10000` nodi a caso)*; **`p` = la frazione col massimo `<=` quello osservato.** **P-M5 VERA** se tutte entro `10` gradi e `p < 0.01`. **Poi a `k 36250`:** i `20` archi con `|Theta|` piu' alto, l'angolo del punto medio e la distanza dall'asse; **P-M6 VERA** se fra loro ce ne sono entro `10` gradi da almeno due assi fra `0`, `60`, `120`, `240`. **IL CASO NOTO DI M3 (DEVE):** sul toro iniziale un `Theta` isotropo costruito a mano *(`Theta = exp(-(r_mid - 18.9)^2 / 2)`, `r_mid` il raggio del punto medio dell'arco dalla stessa sorgente)*: la distanza media dall'asse dei `20` archi con `Theta` piu' alto, contro quella di tutti gli archi con `r_mid` in `[17.5, 19.5)`: **entro `5` gradi** *(la grana del reticolo, dichiarata)*.
- **A17:** l'angolo e `r` usano il disegno solo per MISURARE *(Luca)*.

## 4. C1: LE CURE D1-D3 PER ESTESO *(scritta PRIMA del codice)*

### 4.1 D1: `geo.n` E' UNO STATO DELLA RELAZIONE

- **Precisazione di A17** *(Luca)*: **«A17 vieta le posizioni del disegno, non gli stati locali della relazione».** `geo.n` *(il versore per estremita')* e' come `U`: uno stato locale, con le sue regole di nascita di oggi *(le estremita' di `a` trasportate, le altre medie normalizzate; al flip `+v`, `-v`)*. **Nessun codice cambia per D1.**

### 4.2 D2: L'ORIENTAMENTO EREDITATO *(`vec` esce dalla fisica)*

- **Lo stato:** **per ogni triangolo il suo CICLO** *(l'ordine dei tre nodi, ruotato in modo canonico: il nodo d'indice minore per primo)*; un dizionario `{la terna ordinata: il ciclo}` nel campo *(`CampoGenerico_v2.ori`)*, e **nello stato salvato** come un array `(F, 3)` dei cicli *(la chiave `ori_cicli`)*: **la ripresa lo LEGGE, non lo ricalcola dalla geometria.**
- **A `k 0` UNA volta dalla geometria:** sul toro regolare il ciclo antiorario dal prodotto vettoriale dei vettori d'arco *(la regola di oggi: sul reticolo regolare non ci sono degeneri)*; **poi solo eredita'.**
- **LA NASCITA sull'arco `a = i -> j`, la stella `i - k - j - l`:** i due triangoli di `a` sono `T_k = (i, j, k)` *(quello il cui ciclo contiene `i -> j`)* e `T_l = (j, i, l)` *(quello il cui ciclo contiene `j -> i`)*; **nel ciclo di ciascuno si sostituisce `j` con `n`, e poi `i` con `n`:** `T_k -> (i, n, k)` e `(n, j, k)`; `T_l -> (j, n, l)` e `(n, i, l)`. **I quattro triangoli nuovi hanno il verso del triangolo da cui nascono.**
- **IL FLIP del lato `x - y` nel quadrilatero `n - x - m - y`:** i due triangoli orientati che condividono la diagonale vecchia, `(n, x, y)` e `(m, y, x)` nel loro verso, danno **il ciclo del quadrilatero** *(se il ciclo del primo contiene `x -> y`, il quadrilatero e' `n -> x -> m -> y`; altrimenti il verso opposto)*; **i due triangoli nuovi lo seguono:** `(n, x, m)` e `(n, m, y)` nel verso del quadrilatero.
- **`k` E `l` DALL'ORDINE CICLICO** *(D2 b)*: **`k` = il terzo vertice del triangolo il cui ciclo contiene `i -> j`; `l` = il terzo dell'altro.** Oggi `k` e' «a sinistra di `i -> j`» dal prodotto vettoriale: **sul triangolo antiorario e' lo stesso nodo** *(P-C1)*.
- **La sorgente e i segni** della placchetta: **dal ciclo ereditato, con le righe di oggi** *(`_placchetta` dopo la scelta del ciclo: il primo arco esce dalla sorgente, i segni dal verso degli archi)*.
- **`vec`** resta **solo per il disegno e le misure** *(i nati continuano ad averlo, con la formula di oggi)*: **nessuna riga di fisica lo legge.**
- **I file NUOVI** *(nessuno in uso si tocca)*: `csv/solitone/u1_generico_v2.py` *(`CampoGenerico_v2`: `ori`, `_placchetta` SENZA prodotto vettoriale, `cresci` con `ori_nuovi`, `orientamento_da_vec` solo a `k 0`)* -- **e' sotto `csv/`, quindi il commit gira la suite** *(SUITE-NEL-COMMIT)*; `doc/referti_l2/mitosi_regola_v2.py` *(`indici_nascita` dall'ordine ciclico; `candidato`, `regola`, `applica` col campo v2 e gli `ori_nuovi`)*; `mitosi_corsa_v2`, `mitosi_lunga_v2`, `mitosi_rami_v2` *(il campo v2 a `k 0`; salva e riprendi con `ori_cicli`)* -- **dove possibile importando i vecchi e cambiando solo le funzioni che toccano l'orientamento.**

### 4.3 D3: `kappa` IL NUMERO DI OGGI

- **`kappa = 2.5289441539...e-04`** *(il valore AL BIT del `meta["parametri"]` della corsa del mattone con `chi`)* **dichiarato costante** in un file nuovo *(`doc/referti_l2/chi_parametri_v2.py`)*: `parametri_v2` restituisce lo STESSO `kappa` senza leggere nessuna posizione; `m0` dallo stato di partenza come oggi; **`c0 = kappa m0` come oggi, al bit.**

### 4.4 LE PROVE *(il mandato: O1-O5, O7, O8; le soglie)*

- **O1** *(senza tick)*: dall'orientamento del toro *(da `vec`, `k 0`)* **ricostruito lungo le `9` nascite di `nascite_36250.json`** *(la nascita e il flip, nell'ordine)* **contro l'orientamento di oggi a `k 36250`** *(il `CampoGenerico` ricostruito dallo stato: il ciclo dal prodotto vettoriale)*: **`0` triangoli diversi**; e **`k`, `l` dall'ordine ciclico = `k`, `l` registrati, nascita per nascita: `0` diversi.**
- **O2** *(una corsa)*: dallo stato del tronco `k 35976` col codice nuovo fino a `k 36250`: **lo stato AL BIT con lo stato `k 36250` del ramo** *(sha1 `64999c5b`: ogni array, il grafo, i versori, `Theta`, le posizioni, `E_persa`; il file nuovo ha in piu' `ori_cicli`, quindi si confrontano gli array, non lo sha1 del file)*. **Q-P1, prima:** `274` tick a `~4.7` s *(il ritmo del ramo, con le altre corse)* piu' `9` nascite a `~15` s: **circa `24` minuti.**
- **O3** *(una corsa)*: da `k 36250` col codice nuovo **fino alla decima nascita piu' `5` tick**: **nessun AssertionError; P1, P3, P9 a `0`, F3** *(Eulero, nessun doppio, due triangoli per arco, placchette coerenti)* **a ogni nascita.**
- **O4** *(deve fallire)*: un triangolo col ciclo invertito a mano nel candidato: **le placchette NON coerenti** *(F3)* **o P3 fuori soglia.**
- **O5:** P8 col codice nuovo *(`ori_cicli` compreso)*: `10` tick di fila contro `5` + salva + riprendi + `5`, AL BIT; un byte cambiato -> la ripresa RIFIUTA.
- **O7:** i due candidati degeneri noti *(l'arco `40445` flip `0`; l'arco `103798` flip `3`)* **sullo stato `k 36250` col codice nuovo: nessun AssertionError**, l'orientamento ereditato dei triangoli nuovi stampato.
- **O8:** `chi_parametri_v2` = `meta["parametri"]` della corsa *(`kappa`, `c0`, `m0`)* **al bit.**
- **Se O1, O2 o O8 non passano: FERMO.**
