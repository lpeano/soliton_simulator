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
