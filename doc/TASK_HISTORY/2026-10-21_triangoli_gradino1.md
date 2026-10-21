# TRIANGOLI, PRIMO GRADINO: LA SCENA A 6 VICINI E LA CAMMINATA SOLA, VERIFICATE

> **Il mandato:** decisione di Luca del `2026-10-21` alle `17:53`; il progetto e' `a840e8f7`.
> ### **SOLO LA CAMMINATA:** nessuna legge *(`S3` e le altre)* gira sui triangoli in questo
> mandato. ### **Sulla griglia quadrata TUTTO resta AL BIT:** impronta `2e7f795d2a52fbe7`,
> `leggi.yaml`, i collaudi, i referti. ### **Le scelte di fisica sono di Luca.**

**LIVELLO CORRENTE:** `L2`, il gradino `T1`-`T2` *(solo la camminata)* del piano del progetto.

## 0. LA DECISIONE DI LUCA *(`17:53`)*, alla lettera

> ### **«La moneta sui triangoli usa `eps = 0.5`, LA STESSA DI OGGI, perche' il passaggio dai
> quadrati ai triangoli cambi UNA SOLA COSA (la connettivita'). Il gruppo finito (`eps dtau =
> pi/2`) resta aperto, legato alla domanda di `L1` (`b8197923`, `f9c5521e`: non speciale per la
> stabilita').»**

## 1. LA STELLA POLARE

1. **`A14`:** ### **la camminata sola deve restare UNITARIA** *(il controllo di unitarieta')*:
   ### **e' la conservazione della norma, locale per costruzione** *(ogni pezzo e' per
   estremita', per nodo o per arco)*.
2. **Il gradino:** `(a)` ### **i controlli che devono riuscire e quelli che devono fallire**;
   `(b)` e `(c)` ### **non si applicano:** e' la verifica di una scena, non un risultato fisico.
3. **Aggiunge un numero o una legge?** ### **No:** la connettivita' e' topologia; ### **`eps = 0.5`
   e' quello di oggi, per decisione di Luca.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No:** `cs` spento, nessuna legge della materia.
5. **Emergente o imposto?** ### **Non si applica:** si verifica che la camminata sui triangoli
   sia quella che il progetto dice.

## 2. RAGIONAMENTO PRELIMINARE — che cosa credo PRIMA

- ### **LETTO DAL CODICE:** il passo e' gia' scritto per un grafo QUALUNQUE:
  - `incidenza.Incidenza(ii, jj, nn)` prende ### **archi qualsiasi**;
  - `motore.Motore(inc, Geometria(nv, U), st, dtau, ...)` prende ### **le direzioni per estremita' (`nv`) e le `U` per arco**;
  - ### **il Grover usa `inc.grado`**, lo spostamento lavora ### **per arco**, la moneta ### **per estremita'**.
  - ### **Quindi NON serve toccare il passo.** Serve ### **un costruttore della scena** che dia `ii`, `jj` e `nv` per i triangoli: ### **lo scrivo NUOVO, in `csv/_triangoli.py`**, e ### **non tocco `corrente.toro` ne' `scena_l2`** -- cosi' la griglia quadrata ### **resta al bit per costruzione.**
- ### **IL COSTRUTTORE, generale:** un toro su `lati` con ### **una lista di SPOSTAMENTI INTERI** *(gli archi propri del nodo, in coordinate degli indici)* e ### **una lista di DIREZIONI** *(un versore 3D per spostamento)*:
  - **quadrato:** spostamenti `(1, 0)`, `(0, 1)`; direzioni `0`, `90` gradi;
  - ### **triangoli:** spostamenti `(1, 0)`, `(0, 1)`, `(1, 1)`; ### **direzioni `0`, `120`, `60` gradi** *(se `(1, 0)` sta a `0` e `(1, 1) = (1, 0) + (0, 1)` a `60`, allora `(0, 1)` sta a `120`: le `6` direzioni uscenti, coi loro opposti, sono quelle dell'esagono)*;
  - ### **FCC: NON serve un sottoreticolo** -- nella BASE PRIMITIVA della FCC i nodi sono ### **tutto un toro `L^3`** e i `6` spostamenti propri sono `(1,0,0)`, `(0,1,0)`, `(0,0,1)`, `(1,-1,0)`, `(1,0,-1)`, `(0,1,-1)`. ### **Lo stesso costruttore, con `d = 6`.** ### **Si generalizza.**
  - ### **Il controllo che il costruttore e' giusto:** col quadrato ### **deve ridare AL BIT** `ii`, `jj` e `nv` di `scena_l2` *(`corrente.toro` e `versori_geometrici`)*.
- ### **LA CONVENZIONE:** l'arco `k = v d + a`, le estremita' `2k` *(sul nodo `v`, direzione `+e_a`)* e `2k + 1` *(sul vicino, direzione `-e_a`)*: ### **quella del progetto e di oggi.** ### **La cella** e' il nodo coi suoi `d` archi: `2d` estremita', ### **`36` reali** in 2D.
- **Che cosa credo:** che ### **tutti i controlli che devono riuscire riescano** *(il passo e' generale)*, e che ### **l'isotropia `C6` sia il controllo piu' delicato**: ### **la moneta lega lo spin alle direzioni**, e la rotazione di `60` gradi deve ruotare insieme spazio e spin.
- **Cosa NON so:** se i `64` collaudi della suite ### **girano tutti** senza toccare niente *(non dovrebbero vedere il file nuovo)*.

## 3. I CONTROLLI, FISSATI QUI *(copiati dal mandato prima dei numeri)*

### DEVONO RIUSCIRE

- ### **IL COSTRUTTORE SUL QUADRATO = `scena_l2` AL BIT** *(`ii`, `jj`, `nv`)* -- ### **il mio controllo in piu', dichiarato.**
- ### **UNITARIETA':** la camminata sola *(senza `CAMM-MATERIA-VUOTO`, `cs` spento)*, `N` tick a lato `32`, ### **conserva la norma entro `N * 64` ulp** *(su uno stato casuale)*; ### **ed e' ESATTA come `braccio_c2_esatto`**: ### **ogni autovalore della matrice di un tick per cella** *(`18` complessi, `36` reali)* ### **elevata a `N`** ha modulo `1` entro `N * 64` ulp.
- ### **INVARIANZA PER TRASLAZIONE:** la base uniforme *(materia allineata `x 0.1`, vuoto `1`)* ### **resta uniforme entro `1e3` ulp** sotto la camminata sola, per `N` tick.
- ### **ISOTROPIA `C6`:** la dispersione `omega_a(k)` della camminata sola ### **e' invariata dalla rotazione di `60` gradi di `k`** nella zona esagonale, ### **entro `64` ulp** *(sulle fasi per tick, scala `pi`)*, stampato lo scarto massimo. ### **La rotazione negli indici di `k`:** `(m_x, m_y) -> (-m_y, m_x + m_y)` *(e' l'inversa trasposta della rotazione dei vettori del reticolo, `(a, b) -> (a - b, a)`)*.
- ### **LO STATO DI MATERIA:** lo spinore allineato `sigma.n_h` per estremita' ### **esiste** *(`sigma.n_h chi = chi` entro `64` ulp)*, e ### **le `6` direzioni uscenti di un nodo sommano a zero** *(verificato per conto, su ogni nodo)*.

### DEVONO FALLIRE

- ### **L'ISOTROPIA `C6` sulla griglia QUADRATA:** lo scarto deve superare di molto la soglia *(`> 1e6` volte)*. ### **Se passa, il test e' cieco: STOP.**
- ### **LA BIPARTIZIONE:** il grafo triangolare ### **NON si colora in due** *(un ciclo di `3` trovato e stampato)*; il grafo quadrato ### **SI'** *(a lato pari)*. ### **Se il triangolare risultasse bipartito: STOP.**

### E SULLA GRIGLIA QUADRATA

- ### **i collaudi esistenti** *(`python primo_ordine/collauda.py`)* ### **e l'impronta al bit.**

## 4. I PARAMETRI

- lato `32`, `dtau 0.125` *(come i conti di `L2`)*, `eps = 0.5`; `N = 800` *(`N dtau = 100`)* per l'esattezza e l'invarianza; `N = 200` per la norma su stato casuale *(seme `7`)*.

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_triangoli.py` e l'inventario: ### **un commit a se'.**
3. La corsa: `python csv/_triangoli.py > doc/referti_l2/triangoli_gradino1.txt`, con `.jsonl`; i collaudi della suite.
4. Il referto, la voce `[[GRIGLIA-A-TRIANGOLI]]` *(il primo gradino fatto)*, la relazione *(la domanda sul gradino `2`)*: un commit.
