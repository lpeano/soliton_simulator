# IL PROGETTO DEGLI STRUMENTI DELLA FCC *(sulla carta: nessun codice, nessuna decisione)*

> ### **Il mandato:** di Luca, «chiudere il capitolo dei triangoli e progettare gli strumenti della FCC» *([[PIANO-2D-3D]]; il task history `doc/TASK_HISTORY/2026-10-24_progetto_fcc.md`)*.
> ### **Per ogni punto: che cosa SERVE, che cosa si RIUSA** *(le funzioni dei triangoli)*, ### **che cosa si SCRIVE, e il CONTROLLO DI SERVIZIO che ne prova la correttezza.** ### **Il nucleo non si tocca: tutto
> in `csv/`, in memoria, come sui triangoli.** ### **Ogni fatto «dal codice» e' letto dal sorgente.**

## 1. LA SCENA

### **IL RETICOLO** *(il reticolo `A3` dei gruppi di radici: NON l'assioma `A3` di `doc/ASSIOMI.md`)*
- ### **La base primitiva** *(il primo vicino a distanza `1`)*: ### **`a1 = (0, 1, 1)/sqrt2`, `a2 = (1, 0, 1)/sqrt2`, `a3 = (1, 1, 0)/sqrt2`** *(la base di Setyawan-Curtarolo: la stessa della tabella della zona)*. ### **I `12` vicini: `+-a1`, `+-a2`, `+-a3`, `+-(a1 - a2)`, `+-(a1 - a3)`,
  `+-(a2 - a3)`: le permutazioni di `(+-1, +-1, 0)/sqrt2`.** ### **Nella forma `A3`: i punti di `Z^4` a somma nulla, i vicini `e_i - e_j`; fissato `i`, i tre `e_i - e_j` sono un TRIEDRO, e i `12` vicini sono QUATTRO triedri.**
- ### **Gli spostamenti propri del nodo** *(`d = 6`: un arco per coppia `+-`)*: ### **`(1,0,0)`, `(0,1,0)`, `(0,0,1)`, `(1,-1,0)`, `(1,0,-1)`, `(0,1,-1)` nelle coordinate della base** *(la riga FCC della
  docstring di `csv/_triangoli.py`)*, ### **con le direzioni `a1`, `a2`, `a3`, `a1 - a2`, `a1 - a3`, `a2 - a3` normalizzate.** ### ⚠ **La docstring NON dice quale spostamento va con quale direzione: va FISSATO e
  CONTROLLATO** *(sotto)*.
- ### **IL TORO A LATI DIVERSI:** ### **`lati = (L1, L2, L3)` lungo `a1`, `a2`, `a3`.** ### ⚠ **Sulla FCC `doc/PROGETTO_TRIANGOLI.md` conta i nodi in coordinate CUBICHE** *(`(i, j, l)` su `L^3` con `i + j + l` pari: `L^3/2`
  nodi)*; ### **nella base primitiva il toro `L x L x L` ha `L^3` nodi.** ### **Sono due tori diversi** *(il cubico e' il toro della cella convenzionale)*: ### **va dichiarato quale.**

| | il valore | dal codice |
|---|---|---|
| le estremita' per nodo | `2d = 12` | `_triangoli.versori`, `celle` |
| il vuoto per estremita' | `VUOTO = 1.0`, quindi `Lambda0 = 12` per nodo | `_triangoli.VUOTO` |
| la cella | `6d = 36` complessi *(`psi` `24`, `phi` `12`)*, `72` reali | `_triangoli.celle` |
| la matrice del tick | `36 x 36` complessa per `k` *(materia `24 x 24`, vuoto `12 x 12`)* | `_triangoli.matrice_tick`, generalizzata |

- ### **SI RIUSA:** ### **`_triangoli.toro_spostamenti`** *(GIA' generale in dimensione: `nn = prod(lati)`)*, ### **`scena_toro`** *(con `lati` di tre elementi)*, ### **`versori`, `celle`, `camminata`, `bipartito`** *(sul grafo)*;
  ### **`cs` per nodo come sui triangoli** *(`mot.cs`, `mot.lambda_c = None`)*.
- ### ⚠ **LA TRAPPOLA, dal codice:** ### **`toro_spostamenti` fa `zip(c, s, lati)`, che TRONCA: un `lati` di due elementi con spostamenti di tre perde la `z` in silenzio.** ### **Lo strumento deve ASSERIRE `len(lati) ==
  len(s)`.**
- ### **SI SCRIVE:** ### **la costante `FCC = (spostamenti, direzioni)`; `matrice_tick_3d`** *(`fftn` su tre assi, `(L1, L2, L3, 36, 36)`)*; ### **i blocchi in spazio reale e `A(k)` a un `k` qualunque in tre fasi**
  *(`theta_j = k.a_j`)*; ### **la curvatura come tensore `3 x 3`** *(il Richardson lungo `6` direzioni: le tre `theta_j` e le tre `theta_i + theta_j`)*, ### **convertito in cartesiano con la matrice delle `a_j`.**
- ### **I CONTROLLI DI SERVIZIO:**
  - ### **`(i)` il grado e la geometria:** ### **ogni nodo ha `12` vicini a distanza `1`, le direzioni uscenti sommano a `0`, nessun arco doppio** *(per `L >= 3`)*.
  - ### **`(ii)` la non bipartizione:** ### **`_triangoli.bipartito` deve dare `False` col CICLO DISPARI** *(il triangolo `0 -> a1 -> a2 -> 0`: `a1 - a2` e' un vicino)*; ### **e un caso che DEVE fallire:** ### **la cubica semplice**
    *(`corrente.toro` a tre lati)* ### **e' bipartita.**
  - ### **`(iii)` la camminata unitaria ed esatta, l'invarianza per traslazione, lo spinore allineato** *(gli stessi di `_triangoli.main`)*.
  - ### **`(iv)` la SIMMETRIA DEL RETICOLO:** ### **il gruppo del cubo `O_h`** *(`48` elementi; le rotazioni `O`, `24`)* ### **manda il reticolo in se' e la zona in se': ogni rotazione e' una matrice INTERA sulle coordinate
    `k` della base reciproca** *(un indice `k -> R k mod L` esatto)*; ### **lo spettro a `k` e a `R k` confrontato SUL CERCHIO** *(l'assegnamento ungherese, come `_triangoli.scarto_c6`)*, ### **almeno per i due
    generatori `C4` attorno a `z` e `C3` attorno a `(1,1,1)`.** ### **Sollevato in `SU(2)`: il BINARIO OTTAEDRICO `2O`** *(`48` elementi; i suoi `12` elementi `(+-i +-j)/sqrt2` sono `-i sigma.n` per le `12` direzioni FCC:
    `doc/PROGETTO_TRIANGOLI.md`)*: ### **lo spinore ruota con la stessa matrice che manda le direzioni** *(il controllo: la matrice del tick commuta con la rappresentazione del gruppo, entro `1e-12`)*.
  - ### **`(v)` il caso che DEVE fallire, per la simmetria:** ### **NON la cubica semplice** *(e' cubica anche lei, e la simmetria la ha)*, ### **ma una griglia DEFORMATA** *(un `a_j` allungato)* ### **o il
    toro a lati diversi: rompono il gruppo del cubo, e il controllo `(iv)` deve accorgersene.**

## 2. LA ZONA DI BRILLOUIN

- ### **L'OTTAEDRO TRONCATO** *(il reticolo reciproco della FCC e' la BCC)*. ### **I punti, in frazioni della base reciproca `b_j`** *(la convenzione di Setyawan-Curtarolo, con la base `a1`, `a2`, `a3` sopra)*:

| punto | coordinate | molteplicita' | nota |
|---|---|---|---|
| `Gamma` | `(0, 0, 0)` | `1` | il centro |
| `X` | `(1/2, 0, 1/2)` | `3` | il centro di una faccia quadrata |
| `L` | `(1/2, 1/2, 1/2)` | `4` | il centro di una faccia esagonale |
| `W` | `(1/2, 1/4, 3/4)` | `6` | un vertice |
| `K` | `(3/8, 3/8, 3/4)` | `12` | il mezzo di uno spigolo fra due esagoni |
| `U` | `(5/8, 1/4, 5/8)` | `12` | il mezzo di uno spigolo fra un esagono e un quadrato |

  ### ⚠ **Le coordinate dipendono dalla base: lo strumento le RICAVA da quelle cartesiane** *(`X = (2 pi/a)(1, 0, 0)`, `L = (pi/a)(1, 1, 1)`, `W = (2 pi/a)(1, 1/2, 0)`, `K = (3 pi/2a)(1, 1, 0)`, `U = (2 pi/a)(1, 1/4, 1/4)`, `a = sqrt2` il
  lato del cubo)* ### **e le controlla.**
- ### **I CAMMINI:** ### **`Gamma - X - W - K - Gamma - L - U - W - L - K`** *(il cammino standard)*.
- ### **LA GRIGLIA:** ### **`K` e `U` hanno ottavi: il lato `L` multiplo di `8`** *(`W` di `4`)*: ### **`L = 16`: `4096` punti `k`; `L = 32`: `32768`.**
- ### **IL COSTO** *(una STIMA, il metodo sotto)*: ### **uno spettro completo a `L 16`:** ### **`36` impulsi x un tick su `4096` nodi** *(`~8`-`10 us` per nodo e tick: `~1.3 s`)* ### **piu' `4096` autovalori `36 x 36`** *(`~1 s`)*: ### **`~3 s`.**
  ### **A `L 32`: `~20 s`.**
- ### **I CONTROLLI DI SERVIZIO:** ### **i blocchi `A(k)` dai blocchi in spazio reale = `matrice_tick_3d` ai punti della griglia** *(entro `1e-12`, come al lato `6` sui triangoli)*; ### **i punti speciali come punti della griglia**
  *(l'indice esatto)*; ### **la molteplicita' delle stelle** *(i `12` `K` dati dalla simmetria)*.

## 3. LA CATENA DELLE MISURE *(l'ordine dei triangoli; ogni gradino un mandato)*

| | la misura | si riusa | si scrive | il controllo di servizio |
|---|---|---|---|---|
| `(a)` | gli spettri di materia e vuoto, i tocchi e il loro esponente, il salto minimo e dove, i modi senza massa | `_triangoli_luce.dispersione` *(con `V_di` a tre fasi)*, `livelli`, `_triangoli_dove_la_luce.livelli_cerchio` | la dispersione lungo direzioni sulla SFERA *(non nel piano)*; la ricerca del salto minimo sulla zona `3D` | la simmetria `(iv)`; il vuoto a `eps 0` = due copie della materia? *(sui triangoli era vero: da RIVERIFICARE)* |
| `(b)` | la coppia massiva piu' bassa: `salto/s`, `omega(0)`, `omega''` *(tensore `3 x 3`)*, `v_b`; `v_max` di tutti i settori | `_triangoli_forza.v_max` *(Hellmann-Feynman: da portare a tre derivate)*, `_triangoli_fattore.ramo_lungo` | la coppia NON e' a `K` per costruzione: la si cerca *(il salto minimo)* e la si segue in `eps` | `F = R_t Q_b L` al bit *(un'identita')*; l'anisotropia del tensore ai punti di alta simmetria |
| `(c)` | lo zero universale `lambda*` *(atteso `1/2`)* e Hamilton `a_H/a_RG` | `_zero_simmetrico.convenzione_simmetrica`, `_triangoli_bassa_energia.continua` *(la fase continua in `s`)* | `continua` a tre fasi | `lambda* = 1/2` a `eps 0` sulla coppia trovata |
| `(d)` | la forza col pacchetto di banda e il differenziale | `_triangoli_forza.pacchetto_banda`, `corsa_con`, `_forza_da_cs.fit_moto` | il toro a STRISCIA in `3D` *(lungo e sottile in due direzioni)*; la portante a un `k` della griglia | il nullo a `eta 0`; lo specchio sul DIFFERENZIALE *(`doc/PATTERN_DI_PROVA.md`)*; la semisomma contro `eta 0` |
| `(e)` | `delta(s)` del passo *(atteso esponente `2`)* | `_scala_e_zero.H_eff`, `esponente`; `_triangoli_bassa_energia.un_pezzo` | niente *(e' per `k`)* | un pezzo solo `< 1e-12` |
| `(f)` | l'incrocio `v_b = v_max` al variare di `s` | `_triangoli_dove_la_luce.riga` *(a tre fasi)* | la griglia fine in `s` attorno all'incrocio | a `s = 1` il modo senza massa *(se c'e')* e la sua velocita' |

## 4. LE SCELTE APERTE DI LUCA *(PARAMETRI dello strumento, NON prese)*

| la scelta | come si passa allo strumento, senza toccare il nucleo |
|---|---|
| **lo zero dell'energia** *(oggi o simmetrico)* | `_zero_simmetrico.convenzione_simmetrica()` in memoria *(avvolge `flussi_parziali.grover`, `hop_psi`, `hop_phi`)*: un argomento `zero in ("oggi", "simm")`, **le due sempre stampate** |
| **il regime di `s`** *(la proposta del guardiano, NON decisa: `s <= 0.3`)* | `s` e' il `dtau` della scena a `cs` uniforme, o `mot.cs` per nodo: **una lista di `s` nella configurazione dello strumento**, senza regola |
| **il legame `S1`, `S3`, `S4`** | `_screening_forme_s3.forma(nome)` in memoria *(sostituisce `materia_vuoto.pezzi`)*; `S3` e' la legge del codice |
| **`eps`** *(`0.5` la scelta di Luca per i triangoli)* | la variabile di modulo `EPS_MONETA` dello strumento *(come `_triangoli.EPS_MONETA`)*, **ripristinata dopo ogni uso** |
| **la regola di scala FRA geometrie** *(`doc/PROGETTO_TRIANGOLI.md`: il vuoto per estremita' o per nodo)* | `VUOTO` per estremita' *(oggi `1.0`, `Lambda0 = 12`)* **o** `phi` riscalata a `Lambda0 = 4` o `6` per nodo: un parametro dichiarato |

## 5. IL COSTO E L'ORDINE

### **IL METODO DELLA STIMA:** ### **i tempi MISURATI nel repo** *(`stato_finale_R2T.txt`: la camminata sui triangoli, `cs` spento, `1024` nodi `~5 ms` per tick, `4096` nodi `~15.8 ms`: `3.9`-`4.9 us` per nodo e
tick)*, ### **scalati col numero degli archi propri** *(`d 3 -> 6`: `x2`)*: ### **`~8`-`10 us` per nodo e tick sulla FCC.** ### ⚠ **E' una STIMA: il primo mandato la MISURA.**

| la misura | la taglia | la stima |
|---|---|---|
| la scena e i controlli `(i)`-`(v)` | `L 8`-`16` | minuti |
| uno spettro completo | `L 16` / `L 32` | `~3 s` / `~20 s` per `(eps, s)` |
| `(a)` i tocchi e la loro dispersione | `L 16`, `~10` direzioni sulla sfera per tocco | `~1` minuto per `(eps, s)` |
| `(b)` `v_max` *(Hellmann-Feynman su `4096` `k`, `24 x 24`, direzioni sulla sfera per i gruppi degeneri)* | `L 16` | `~5` minuti per `(eps, s)` *(sui triangoli `25 s` per `2304` `k`, `12 x 12`)*: **da vettorizzare** |
| `(c)` Hamilton e `lambda*` | `L 16` | `~1` minuto per `(eps, s)` |
| `(d)` la forza *(la striscia `96 x 6 x 6` = `3456` nodi, `~400` tick a `s 0.1`)* | `~300` corse | `~12 s` a corsa, `~1` ora |
| `(e)` `delta(s)` | `L 8` | minuti |
| `(f)` l'incrocio | `~10` `s` | `~10` minuti |

### **L'ORDINE DEI MANDATI** *(uno alla volta)*:
1. ### **la scena FCC e i suoi controlli di servizio** *(il punto `1`; e la misura del costo vero)*;
2. ### **la zona, gli spettri, i tocchi** *(`(a)`, e `(e)` che costa poco)*;
3. ### **la coppia piu' bassa, `v_b`, `v_max`** *(`(b)`)*;
4. ### **lo zero universale e Hamilton** *(`(c)`)*;
5. ### **la forza** *(`(d)`)*;
6. ### **l'incrocio `v_b = v_max`** *(`(f)`)*.
### ⚠ **E le scelte del punto `4` restano di Luca:** ### **il guardiano consiglia di decidere lo zero PRIMA degli strumenti** *(cosi' la FCC «nasce col zero giusto»)*: ### **qui resta un parametro.**
