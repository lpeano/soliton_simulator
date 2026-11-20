# LA NASCITA NEL GUSCIO A ENERGIA NULLA *(il mandato unico di Luca `2026-11-20` `10:31`)*

> **La ripresa** da `doc/SOSPESO_2026-11-17_MITOSI_INNESCO.md` *(`b1996407`)*, letto prima. [[MITOSI-QUANTO-OLONOMIA]]
> **Le decisioni di Luca** *(`10:31`)*: **(1) la strada (i):** lo spazio puo' nascere **NEL GUSCIO della materia**, dove scatta il contatore del lapse *(carta della mitosi `15.2`: `10`-`22` nodi)*; **S1 del `2026-11-17`** *(il filtro della materia all'`1%`)* **e' TOLTA**; **il «vicino ma fuori» del `2026-11-17` e' SUPERATO** *(il contatore scatta solo dove il tempo e' curvo; A3: lo spazio in se' non costa)*. **(2) la nascita e' A ENERGIA NULLA:** la regola della MATERIA sulle estremita' nuove si sceglie, nascita per nascita, perche' `DH` totale `= 0` *(con FA per il vuoto)*; **la compensazione di A3 resta SOLO come riserva** dove la materia e' trascurabile *(li' la famiglia non ha radice: sul vuoto puro `DH = +3.48` con FA)*.
> **In vigore:** l'innesco (a) `|Theta_a| >= 2 pi` *(15.1)*, D-M1, D-M2, D-M4, **D-M3 = FA**, D-R4, D-R5, D-R1-D-R3 sospese, il bordo tolto, C2 braccio senza mitosi, il mattone su `L 186`; S2 e S4 del `2026-11-17` `21:00`.
> **Le scelte del guardiano** *(su delega di Luca)*: **S1** la famiglia a un parametro `alpha`; **S2** la radice per bisezione a numero fisso di passi; **S3** il risparmio *(C2-EXT, e MITOSI dallo stato prima del primo scatto)*.

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

### 1.1 LA NASCITA DI OGGI, LETTA SUL CODICE *(`doc/referti_l2/nascita_dentro_fuori.py`, `nasci`; `doc/referti_l2/regole_fase_F3.py`, `regola` e `nascita`)*

- **La divisione:** l'arco `a = (i -> j)` tolto; `k`, `l` i due vicini comuni *(`k` a sinistra di `i -> j`)*; il nodo nuovo `n`; gli archi nuovi `n -> i, j, k, l` in coda. **Le estremita' dell'arco tolto TRASPORTATE:** l'estremita' in `i` va sull'estremita' in `i` di `n -> i`, quella in `j` sull'estremita' in `j` di `n -> j`. Le estremita' nuove in `k` e `l`: `psi = 0`.
- **D7 su `psi`, sul PADRE `i`** *(il nodo SORGENTE dell'arco, `ii[a]`)*: **tutte le estremita' di `i`** *(compresa quella trasportata)* **divise per `sqrt(2)`**; **le `4` estremita' di `n`** a `(1/sqrt(2)) sqrt(N_i/4) chi/|chi|`, con `N_i` la norma di `psi` in `i` e `chi` la somma delle sue estremita' *(prima della divisione)*. **La norma e' conservata:** `i` tiene `N_i/2`, `n` riceve `N_i/2`.
- **FA su `phi`** *(D-M3)*: le fasi «antipodali», i moduli v4 *(uniformi sul sottospazio di `n` alla norma di prima)*. **Non dipende da come si sceglie `psi`.**
- **Il conto:** `nascita_dentro_fuori.famiglie` *(il motore della carta: `U = I`, `cs` spento, `eps = 0`; `energia_pesata.termini_di_h`)*: **lo stesso conto di `innesco_S1.txt`**, da cui viene il `-1.2e3`.

### 1.2 LA FAMIGLIA *(S1, del guardiano: proposta QUI, prima di misurare)*

- ### **LA FAMIGLIA: `alpha` E' LA FRAZIONE DELLA NORMA DEL PADRE CHE PASSA AL NODO NUOVO** *(in unita' di quella di D7)*. **Per `alpha` in `[0, 1]`:**
  - **le estremita' di `i`** divise per `sqrt(2 / (2 - alpha))`: `i` tiene `N_i (1 - alpha/2)`;
  - **le `4` estremita' di `n`** a `sqrt(alpha) (1/sqrt(2)) sqrt(N_i/4) chi/|chi|`: `n` riceve `alpha N_i / 2`;
  - **tutto il resto come in `nasci`** *(il trasporto, `k` e `l` a `0`, `phi` con FA)*.
- **`alpha = 1` E' D7 AL BIT** *(`2/(2-1) = 2` esatto, `sqrt(1) = 1` esatto, e le operazioni nello stesso ordine)*: **il caso noto** *(Q-A4)*: a `alpha = 1` gli array e `DH` coincidono AL BIT con `regole_fase_F3.nascita(..., "FA")`.
- **`alpha = 0` E' «`psi` TRASPORTATA SENZA DIVIDERLA»** *(definita sul codice)*: `i` non si tocca *(diviso per `sqrt(1)`)*, `n` riceve `psi = 0`; restano il trasporto delle due estremita' dell'arco tolto e `k`, `l` a `0`.
- **Le proprieta':** **la norma conservata** per ogni `alpha` *(`N_i (1 - alpha/2) + alpha N_i/2 = N_i`; se `chi = 0`, come in D7, `n` riceve `0`: contato)*; **locale** *(cambiano solo le estremita' di `i` e di `n`)*; **deterministica**; **la simmetria allo specchio: VEDI 1.3.**
- **LE ALTRE FAMIGLIE NATURALI, scritte e scartate** *(la piu' semplice, dichiarato)*: **(B)** l'interpolazione LINEARE delle ampiezze fra `alpha = 0` e D7, poi rinormalizzata: due operazioni invece di una, e a `alpha = 1` non e' D7 al bit *(la rinormalizzazione arrotonda)*; **(C)** D7 diviso fra `i` e `j` *(meta' della quota da ciascuno)*: **simmetrica fra `i` e `j`, ma a `alpha = 1` NON e' D7** *(il mandato vuole D7 a un estremo)*. **Si prende la (A), sopra.**

### 1.3 ### ⚠ **LA PREMESSA CHE MI PREOCCUPA: IL PADRE DI D7 DIPENDE DAL VERSO DELL'ARCO**

- **D7 sceglie il padre `i = ii[a]`, il SORGENTE dell'arco.** **Lo specchio a `30` gradi** *(quello di `specchio_carta.py`)* **manda gli archi nella direzione `A1` in `A2` e viceversa col verso conservato, ma gli archi nella terza direzione li ROVESCIA** *(`mappa_archi`, `rov`)*. **Su un arco rovesciato l'immagine della nascita ha il padre nell'ALTRO estremo:** **la famiglia, come D7, NON e' simmetrica allo specchio su quegli archi** -- **a meno che il risultato non dipenda dal padre, cosa che non credo.**
- **Quindi la prova dello specchio** *(P5, sotto)* **si stampa SEPARATA per gli archi conservati e per quelli rovesciati.** **Se sui rovesciati fallisce:** **e' un difetto EREDITATO da D7** *(il padre scelto dal verso, una convenzione d'indice)*, **non della famiglia; la cura** *(per esempio il padre scelto da una grandezza dello stato, il pari merito senza nascita)* **e' una decisione di Luca.**

### 1.4 LA RADICE *(S2)*

- **`alpha*` con `DH_tot(alpha*) = 0`, per BISEZIONE a `53` passi fissi** *(`53`: **l'intervallo scende a `2^-53`, sotto la risoluzione del double in `[0.5, 1]`** -- **un numero di PRECISIONE, non di fisica**: dichiarato)*; nessun criterio d'arresto dai dati. **Il segno:** **se `DH(0)` e `DH(1)` hanno lo STESSO segno** *(o uno dei due e' zero esatto: allora quello e' la radice)*: **nessuna radice.**
- **Il conto della bisezione:** **le cinque famiglie scritte a mano** *(`famiglie` senza il motore, `U = I`: la stessa formula, il controllo `ctrl` di `famiglie` dice quanto coincidono)* -- **per il tempo** *(`famiglie` costruisce il motore: `0.31` s a nascita, `innesco_S1.txt`: `922` s per `2929`)*; **alla radice, `DH` col conto PIENO** *(`famiglie`)*, **e il residuo stampato.** **Dichiarato.**
- **NON SO se la radice e' UNICA:** **`DH(alpha)` su `11` punti di `alpha`** *(`0, 0.1, ..., 1`)*, **i cambi di segno contati** *(una diagnosi, non un criterio)*.
- **NON SO il segno di `DH(0)`:** il trasporto senza divisione toglie il termine d'arco di `a` e aggiunge `k`, `l` con `psi = 0` *(il grado cresce: `|S|^2/d` scende)*; **perche' la radice esista serve `DH(0) > 0`** *(`DH(1)` e' negativo, `innesco_S1.txt`)*.

### 1.5 LO STATO

- **Lo stato di C2 a `k 3000`** *(`E:/soliton_simulator/controllo/C2/stato_03000.npz`)*, **NON quello allo scatto** *(che sta a `2.8e4`-`1e5` tick: non esiste)*: **dichiarato**, come per `innesco_S1.txt`.
- **I candidati:** i `2929` archi che arrivano a `2 pi` entro `1e5` tick *(`E:/soliton_simulator/controllo/torsione/candidati.npz`, `torsione_segmenti.py`)*, **nell'ordine di scatto** *(il tempo previsto `T`)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO *(i passi, cosa decide ciascuno, cosa mi farebbe FERMARE)*

1. **Lo script** `doc/referti_l2/nascita_energia_nulla.py`, **committato PRIMA della corsa** *(un file nuovo: `nascita_dentro_fuori.py` e `regole_fase_F3.py` non si toccano)*. **I sottocomandi:** `parte K NP` *(gli archi `q` con `q mod NP = K`)*; `det` *(i primi `100` archi nell'ordine di scatto e la fila: due processi, il confronto AL BIT dei risultati salvati)*; `referto` *(il caso noto, lo specchio, la fila, la raccolta delle parti, le previsioni)*. **I dati** in `E:/soliton_simulator/controllo/nascita_nulla/` *(non nel repo: il dato e' il comando)*.
2. **Il caso noto** *(Q-A4)*: **a `alpha = 1`, sui primi `20` archi nell'ordine di scatto: `psi`, `phi` e ogni termine di `DH` AL BIT** con `regole_fase_F3.nascita(..., "FA")`. ### **Se fallisce: FERMO.**
3. **Per ogni arco:** `DH(0)`, `DH(1)`, `alpha*` *(se esiste)*, `DH` scomposto per termine alla radice *(col conto pieno)*, il residuo, i cambi di segno sugli `11` punti. **La distribuzione di `alpha*` per anello.** ### **Se la radice manca su PIU' DEL `20%` degli archi: FERMO** *(il mandato)*.
4. **La fila:** **`20` nascite IN FILA alla radice**, sugli archi in ordine di scatto, ognuna sullo stato lasciato dalla precedente; **`H` totale** *(il conto pieno)* **dopo ognuna**, `|H(dopo) - H(prima)| / |H|`. **Un candidato il cui arco non esiste piu'** *(diviso da una nascita prima)* **o senza radice: SALTATO e contato** *(A3 e' della regola del ramo, TODO 4: qui non si applica)*. **Solo la divisione:** il flip D-M2 e' della regola intera *(TODO 4)*. **Dichiarato.**
5. **Il determinismo:** `det` in **due processi** contemporanei, **i risultati AL BIT** *(gli sha1 dei byte)*, e **contro le parti** sugli stessi archi.
6. **Lo specchio (P5):** **lo specchio a `30` gradi per il nodo piu' vicino al centro di C2** *(le mappe di `specchio_carta.py`: i nodi, gli archi, il verso)*; **lo stato RIFLESSO per estremita'** *(`psi` e `phi` permutati; nessuna trasformazione dello spinore: la regola e' covariante per un unitario globale, e `fase` per il coniugio e il segno)*; **sui primi `200` archi nell'ordine di scatto: la nascita sull'arco immagine nello stato riflesso contro la nascita sull'arco nello stato vero** -- `alpha*`, `DH(0)`, `DH(1)` e i termini *(somme: invarianti per permutazione)*; **la soglia `1e-10` relativo** *(la tabella P5 della carta della mitosi, sez. `7`)*; **SEPARATI gli archi a verso conservato e quelli rovesciati** *(1.3)*. **Il controllo:** `H` dello stato riflesso = `H` dello stato *(entro la stessa soglia)*. **Il caso che DEVE fallire:** la nascita sull'arco immagine nello stato NON riflesso.
7. **Il costo** *(parte di Q-P1, per P-Z5)*: il tempo di una nascita *(la divisione, FA, la bisezione)* in questo script, contro il tick misurato di C2 *(`3.690` s)*; **la CSR e Gauss rifattorizzato NON ci sono:** P-Z5 si chiude nel TODO 4.
8. **I processi:** `3` parti + `2` per `det` = `5`, `1` filo ciascuno, numba spento; **una voce del registro per ciascuno.**

## 3. LE PREVISIONI *(copiate PRIMA delle misure; anche nella carta della mitosi, sez. `16`)*

- **P-Z1.** La radice `alpha*` esiste su almeno il `95%` dei `2929` archi.
- **P-Z2.** `alpha*` sta strettamente dentro `(0, 1)` sulla maggior parte degli archi *(ne' D7 ne' il trasporto puro sono a energia nulla)*.
- **P-Z3.** Alla radice la nascita e' deterministica al bit e simmetrica allo specchio.
- **P-Z4.** Nelle `20` nascite in fila `|H(dopo) - H(prima)| / |H|` resta sotto `1e-10` dopo ognuna.
- **P-Z5.** Una nascita *(bisezione, divisione, CSR, Gauss rifattorizzato)* costa meno di `10` tick.
- ### **LE MIE, accanto:** **P-Z1: non lo so** *(serve `DH(0) > 0`: 1.4)*; **P-Z2: se la radice c'e', VERA**; **P-Z3: deterministica SI'; simmetrica SOLO sugli archi a verso conservato -- sui rovesciati credo che FALLISCA** *(1.3: il padre di D7)*; **P-Z4: VERA** *(la bisezione scende a `2^-53` in `alpha`; il residuo col conto pieno dovrebbe stare a `1e-12` di `|H|`)*; **P-Z5: qui solo la parte senza CSR e Gauss.**

## 4. LA STELLA POLARE *(le cinque domande; il TODO 4 cambiera' la fisica sul ramo)*

1. **A14:** la regola della materia della nascita non e' piu' fissata a D7: **la sceglie un vincolo** *(`DH = 0`)*, nascita per nascita -- **una legge di conservazione, non un parametro.**
2. **Il gradino di ROBUSTEZZA-FISICA:** misura su uno stato, nessuna corsa; **la regola intera si prova sul ramo** *(P6 per prima)*.
3. **Numeri o leggi aggiunti:** **nessuna legge nuova nel tick** *(la nascita e' gia' della carta)*; **un numero di precisione** *(`53` passi: dichiarato)*; **S1 del `2026-11-17` TOLTA: un numero in meno** *(l'`1%`)*.
4. **Verso EM-curvatura:** la nascita nel guscio, dove il tempo e' curvo, **e' il primo passo perche' la curvatura del grafo segua il lapse** *(P7 riscritta, S4)*.
5. **Emergente o imposto:** **il DOVE e' emergente** *(il contatore del lapse)*; **il COME e' imposto da un vincolo** *(l'energia nulla)*, **non tarato.**

## 5. TODO DEL NEXT STEP

1. questa carta + la sez. `16` della carta della mitosi *(le decisioni, il «vicino ma fuori» superato, le previsioni)*: commit, push;
2. lo script `doc/referti_l2/nascita_energia_nulla.py`: commit, push; **poi** le `5` corse *(il registro)*; il referto `doc/referti_l2/nascita_energia_nulla.txt`: commit, push;
3. **in parallelo, sul ramo `mitosi`:** B4 *(le posizioni, il confine, le mappe, `righe` -> CSR)*, **poi** la memoria per arco `Theta` nello stato *(cresce con `cresci`: gli archi nuovi a `0`, l'arco diviso consumato; nella ripresa: P8)*: un commit per pezzo, la suite;
4. dopo 2 e 3: la regola completa sul ramo *(contatore -> divisione -> flip D-M2 -> FA -> `alpha*` -> eventuale A3)*; le prove P6 *(PER PRIMA, riscritta a parita' di `E` e `cs`)*, P1, P3, P5, P8, P9 *(`H` entro `1e-10` relativo)*, la nascita FORZATA nel guscio; Q-P1: commit, push;
5. la stima di C2-EXT e di MITOSI *(ore MISURATE)*: **FERMO per Luca prima di lanciare.**
