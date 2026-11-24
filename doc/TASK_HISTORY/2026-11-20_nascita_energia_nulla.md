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

## 6. LE AGGIUNTE DI LUCA DELLE `10:41` E DELLE `10:47` *(scritte PRIMA delle misure che chiedono)*

### 6.1 LA SPINTA E LA SATURAZIONE *(`10:41`)*

- **La domanda di Luca:** la crescita attorno alla massa **SI SATURA** o **NO**. ### **Le due letture ALLA PARI** *(`10:47`)*: **IPOTESI G** *(si satura: una distorsione stabile attorno alla massa, come la gravita')* e **IPOTESI E** *(non si satura: un'espansione centrata sulla materia; con tanti grumi, attesa una legge tipo Hubble)*. **Nessuna delle due e' «riuscito» o «fallito».** **La lettura si scrive DOPO, coi numeri**; se una corsa di circa `7000` tick non basta, si dice, con la stima di quanto servirebbe.
- **«Spinto in la'» = la DISTANZA IN PASSI lungo il grafo** dal centro all'esterno; **le posizioni restano solo per disegnare** *(B4, fuori dal nucleo)*.
- **LO STRUMENTO** `doc/referti_l2/distanza_passi.py` *(nuovo)*: **D1** una visita in ampiezza del grafo dal nodo piu' vicino al baricentro della materia *(`toro.centro` sulle posizioni)*; **gli anelli `40` e `60` scelti dalle POSIZIONI dei nodi ORIGINARI** *(i nodi con la distanza dal centro in `[R - 0.5, R + 0.5)`, fissati una volta allo stato di partenza: dichiarato)*: la mediana, il minimo e il massimo dei passi. **D2** le nascite per finestre di `1000` tick, e il ritmo del contatore sugli archi NATI contro quello dei loro padri. **D3** l'anello di ogni nascita nel tempo. **E1** *(`10:47`)* **la scala della materia CONTATA IN PASSI:** il raggio che contiene il `50%` e il `90%` della massa *(la `rho` per nodo cumulata per passi)*, e **la larghezza `w` = la radice di `somma rho d^2 / somma rho`** *(`d` i passi dal centro: la definizione e' MIA, dichiarata)*. **In MITOSI e in C2-EXT, a ogni stato salvato** *(ogni `250` tick)*.
- **Il caso noto:** **sul toro piatto `L 186` senza nascite i passi dal nodo centrale = la distanza esagonale del reticolo** *(con gli archi `a1`, `a2`, `a1 + a2`: per lo scarto `(d1, d2)` negli indici, `max(|d1|, |d2|)` se `d1 d2 >= 0`, altrimenti `|d1| + |d2|`; sul toro il minimo sulle immagini)* **AL PASSO**; **dopo una nascita FORZATA nel guscio i passi verso l'anello `40` crescono di `0` o di `1`, mai di piu'** *(e mai calano: la divisione toglie un arco, e il cammino `i - n - j` e' lungo `2`)*. **Una figura nel referto della corsa:** i passi all'anello `40` contro il tick, MITOSI e C2-EXT.
- **Annotato, nessuna misura ora:** il RITARDO DI SHAPIRO *(il tempo di volo di un pacchetto attraverso il guscio, MITOSI contro C2-EXT)*.

### 6.2 LA MATERIA E LA METRICA *(`10:47`)*

- **L'osservazione di Luca:** se lo spazio si espande, si espande la metrica di cui e' fatta anche la materia; i conti di energia devono tenerne conto.
- ### **LA NOTA DEL GUARDIANO** *(sua)*: **se TUTTO si espande insieme, l'espansione non si vede; si vede solo se la materia ha una scala sua.** **In un'espansione vera si conservano i CONTEGGI** *(da noi la norma e la carica U(1))*, **non l'energia** *(lo spostamento verso il rosso)*. **La regola a energia nulla e' una scelta da metrica STATICA.**
- **D-PRINCIPIO, APERTA, DI LUCA, DOPO I NUMERI:** **ENERGIA NULLA** *(`H` costante: il mandato delle `10:31`)* **oppure COVARIANTE** *(la nascita copia lo stato come se lo spazio si fosse dilatato; norma e carica esatte, l'energia libera)*. **Il mandato prosegue con l'energia nulla.** Nella carta, dopo i numeri, le due strade coi pro e i contro: **FERMO per Luca** insieme alla stima delle corse.

### 6.3 LA REGOLA COVARIANTE, PER SCRITTO *(E2; SOLO MISURATA: nessuna nascita covariante nella corsa)*

- **L'idea:** **le estremita' nuove ricevono il valore che il campo avrebbe li' se lo spazio si fosse DILATATO**: il nodo `n` sta a meta' fra `i` e `j`, e **ogni sua estremita' e' la MEDIA delle estremita' di `i` e di `j` nella STESSA DIREZIONE** *(un'interpolazione lineare a meta' strada)*. **Per `psi` e per `phi` allo stesso modo:**
  - `n -> j` *(in `n`, la direzione `+a`)*: la media dell'estremita' di `i` verso `j` *(l'arco tolto, in `i`)* e dell'estremita' di `j` verso il suo vicino in `+a` *(`regole_fase_F3.opposto`)*;
  - `n -> i` *(la direzione `-a`)*: la media dell'estremita' di `j` verso `i` *(l'arco tolto, in `j`)* e dell'estremita' di `i` verso il suo vicino in `-a`;
  - `n -> k`, `n -> l`: la media dell'estremita' di `i` verso `k` *(o `l`)* e di quella di `j` verso `k` *(o `l`)*;
  - **in `i` e in `j`:** il TRASPORTO dell'arco tolto *(come `nasci`)*; **in `k`, sull'arco `n -> k`:** la media delle estremita' di `k` verso `i` e verso `j` *(fra le quali l'arco nuovo si infila)*; in `l` lo stesso.
- **Poi la NORMA:** **un fattore UNIFORME sulla STELLA dell'arco** *(tutte le estremita' dei nodi `i`, `j`, `k`, `l`, `n` dopo la nascita)* **perche' la norma su quei nodi torni quella di prima** *(su `i`, `j`, `k`, `l`)*: **un fattore per `psi`** *(la norma della materia, e quindi la carica U(1): `rho` e' la norma)* **e uno per `phi`** *(la norma del vuoto `V`)*. **Locale; simmetrica allo specchio per costruzione** *(le medie sono simmetriche fra `i` e `j` e fra `k` e `l`: NESSUN padre)*; deterministica.
- **IL CASO NOTO** *(dichiarato PRIMA: che cosa DEVE dare)*: **sul vuoto F3 puro** *(`psi = 0`, la scena S162 di `regole_fase_F3.py`)* **la covariante non cambia l'energia PER NODO: `DH_cov = H / n`** *(l'energia per nodo del vuoto)*. ### ⚠ **Credo che NON torni esatto:** il vuoto F3 ha le fasi a periodo `3` per classe di direzione, la media di due estremita' con fasi diverse ha un modulo minore *(poi riscalato)*, e la nascita lascia un `4`-`7`-`7`. **Si stampa lo scarto, e si legge.**
- **Le misure:** sugli stessi `2929` archi, lo stato di C2 a `k 3000`: **`DH_cov` per arco e per anello, scomposto per termine, accanto a `DH(0)`, `DH(1)`, `alpha*`** *(dal referto della nascita a energia nulla)*; uno script NUOVO, `doc/referti_l2/nascita_covariante.py` *(`nascita_energia_nulla.py` e' in uso: non si tocca)*.

### 6.4 LE PREVISIONI DEL GUARDIANO *(copiate PRIMA delle misure e della corsa)*

- **P-S1.** In MITOSI la mediana dei passi all'anello `40` CRESCE dopo la prima nascita; in C2-EXT resta costante al passo.
- **P-S2.** LA CRESCITA RALLENTA: le nascite nell'ultimo terzo della corsa MITOSI sono meno di quelle nel terzo centrale *(un arco diviso da' due archi con meta' della differenza di tempo: meta' del ritmo, un quanto dopo un tempo doppio; e la materia diluita abbassa il gradiente del lapse)*.
- **P-S3.** Le nascite restano nel guscio *(`10`-`22` nodi)* per tutta la corsa.
- **P-E1.** Il mattone TORNA alla sua larghezza in passi: entro `1000` tick dall'ultima nascita, `w` in passi in MITOSI entro il `10%` di C2-EXT.
- **P-E2.** `DH_cov` e' NEGATIVO nel guscio su piu' della meta' dei `2929` archi.
- ### **LE MIE, accanto:** **P-S1:** i passi crescono solo se una nascita cade su TUTTI i cammini minimi verso un nodo dell'anello, e le nascite stanno a `10`-`22` nodi, dentro l'anello: **credo VERA, ma di `0` o `1` passo e non a ogni nascita**; in C2-EXT costante **per costruzione** *(il grafo non cresce: un braccio di controllo)*. **P-S2: non lo so** *(il ragionamento regge per l'arco diviso, ma i figli `n -> k`, `n -> l` stanno di traverso al gradiente)*. **P-S3: VERA in `7000` tick.** **P-E1: non lo so.** **P-E2: non lo so** *(nel guscio `DH(1)` e' fortemente negativo, ma la covariante non ha un padre e muove meno materia)*.

## 7. L'ESITO E LE ANNOTAZIONI ALLE PREMESSE *(le premesse sopra NON si riscrivono)*

- **1.4, «NON SO il segno di `DH(0)`»:** **NEGATIVO su tutti i `2929`** *(mediana `-566`)*: **la radice non esiste** *(`doc/referti_l2/nascita_energia_nulla.txt`)*. **FERMO del mandato** *(oltre il `20%`)*. Il perche' e le strade: la carta della mitosi, sez. `16.5`.
- **1.3, il padre di D7 e lo specchio:** **NON misurato** -- senza radice la prova dello specchio passa a vuoto *(il caso che deve fallire da' `0`: un FALSO-UNO, dichiarato nel referto)*.
- **6.3, la covariante (E2):** **scritta, NON misurata**: il FERMO viene prima; la raccomandazione e' di farla per prima alla ripresa.
- **TODO 3 (il ramo):** B4 `68089e6d`, la memoria `Theta` `c14a087b`, la suite `67/67`; i referti delle due prove sul ramo.
