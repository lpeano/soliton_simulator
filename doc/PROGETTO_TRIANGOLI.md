# IL PROGETTO DELLA GRIGLIA A TRIANGOLI SUL TORO, PENSATO PER LA FCC IN 3D — *su carta*

> **Il mandato:** decisione di Luca del `2026-10-21` alle `14:08`, con l'aggiunta delle `14:14`.
> Task history `doc/TASK_HISTORY/2026-10-21_progetto_triangoli.md` *(`535fae08`)*.
> ### ⛔ **Un PROGETTO: nessun codice di fisica, nessuna corsa, nessuna scelta di fisica.**
> Impronta `2e7f795d2a52fbe7` e `leggi.yaml` intatti. ### **Le scelte sono di Luca.**
> ### **La voce e' `[[GRIGLIA-A-TRIANGOLI]]`** *(`AGENDA`)*.

> ### ⭐ **LA MOTIVAZIONE DI LUCA, alla lettera:** *«I triangoli si scelgono come LA FISICA PIU'
> PULITA (nessun numero da tarare, geometria dalle sole connessioni), NON come cura
> dell'instabilita'. Stella Polare, domanda 5: una geometria scelta per ragioni sue; se poi
> stabilizza, e' un RISULTATO, non un rimedio.»*

**L'obiettivo dichiarato:** il gradino 2D *(triangoli sul toro)* si progetta ### **PENSANDO GIA'
al gradino 3D, la FCC.** Per ogni voce: ### **la forma 2D e la forma FCC**, e ### **se una scelta
2D non si generalizza, lo si dice** e si propone quella che si generalizza.

**Da dove vengono i numeri:** dalle formule scritte accanto, o dai comandi scritti accanto. ###
**Nessun numero ricopiato.**

---

## a) IL GRAFO

| | oggi *(toro quadrato)* | 2D *(toro triangolare)* | FCC *(toro 3D)* |
|---|---|---|---|
| i nodi | `(i, j)` su `L x L` | ### **gli stessi** `(i, j)` | `(i, j, l)` su `L^3`, ### **con `i + j + l` pari** *(o, equivalente, i nodi di un reticolo cubico a facce centrate)* |
| i vicini | `4`: `+-x`, `+-y` | ### **`6`:** `+-(1,0)`, `+-(0,1)`, ### **`+-(1,1)`** *(una diagonale per quadrato, sempre nello stesso verso)* | ### **`12`:** le permutazioni di `(+-1, +-1, 0)` |
| gli archi PROPRI del nodo | `2` *(asse `0`, `1`)* | ### **`3`** *(asse `0`, `1`, `2` = la diagonale)* | ### **`6`** *(i `12` vicini a coppie opposte: il nodo possiede i `6` «in avanti»)* |
| le estremita' per nodo | `4` | ### **`6`** | ### **`12`** |
| la cella *(reali)* | `4 x (2 + 1) x 2 = 24` | ### **`6 x 3 x 2 = 36`** | ### **`12 x 3 x 2 = 72`** |
| la zona di Brillouin | il quadrato | ### **l'esagono** | ### **l'ottaedro troncato** *(il reticolo reciproco della FCC e' la BCC)* |

- ### **LA REGOLARITA':** in tutti e tre ### **ogni nodo vede lo stesso intorno** *(la traslazione di un nodo e' un automorfismo del grafo)*: ### **l'invarianza per traslazione resta**, e con lei ### **la scomposizione per onda di `csv/_stabilita_lineare.py`.**
- ### **LA CONVENZIONE DEGLI INDICI**, generalizzando quella di `corrente.toro` *(«l'arco `k` e' `(nodo = k // d, asse = k % d)`»)*: ### **`d` = il numero di archi propri** *(`3` in 2D, `6` in FCC)*; le estremita' di `k` sono `2k` e `2k+1`. ### **Si generalizza senza cambiare la forma.**
- ### **IL TORO NON E' BIPARTITO** in nessuno dei due *(ogni nodo sta su un triangolo: `(0,0) -> (1,0) -> (1,1) -> (0,0)` in 2D; `(0,0,0) -> (1,1,0) -> (1,0,1) -> (0,0,0)` in FCC, perche' `(0,1,-1)` e' anche lui un vicino)*: ### **il modo alternato `+1`/`-1` non esiste.**

## b) LE DIREZIONI `n_h`

- **Oggi:** `n_h` e' ### **la direzione dell'arco uscente** *(`scena_l2.versori_geometrici`: «le due estremita' di un arco hanno `n` OPPOSTI»)*, letta dall'asse del toro quadrato.
- ### **2D:** le `6` direzioni ### **`n = (cos(k pi/3), sin(k pi/3), 0)`**, `k = 0..5`; ### **FCC:** le `12` ### **`(+-1, +-1, 0)/sqrt 2` e permutazioni.**
- ### **CHE COSA VUOL DIRE «GEOMETRICHE» SENZA POSIZIONI:** ### **le direzioni sono un DATO DEL GRAFO REGOLARE**, non coordinate di nodi:
  - un grafo regolare *(un reticolo)* ha ### **un gruppo di automorfismi** *(le simmetrie che fissano un nodo: `D6` in 2D, il gruppo cubico `Oh` in FCC)*;
  - ### **le `n_h` sono l'unica assegnazione di vettori unitari agli archi uscenti che COMMUTA con quel gruppo** *(a meno di una rotazione globale)*: ### **l'automorfismo che porta un arco in un altro porta la sua `n` nell'altra.**
  - ### **Nessuna posizione serve:** serve ### **sapere quale arco e' «opposto» a quale** *(`n(-h) = -n(h)`)* e ### **come il gruppo li permuta.** ### **E' la stessa informazione che `corrente.toro` gia' ha** *(l'asse e il verso)*.
  - ### ⚠ **Il limite:** questa costruzione ### **vale SOLO su un grafo regolare.** ### **Su un grafo che nasce dalla dinamica** *(la mitosi, `L3`)* ### **le `n_h` non hanno questa definizione**, e il problema aperto della voce speculativa *(`[[SPAZIO-TRIANGOLAZIONE-SENZA-POSIZIONI]]`: «da dove vengano le direzioni») ### **resta.**

## c) LA MONETA

### Che cosa e' oggi *(`leggi.yaml`, `CAMM-MONETA-SPIN`)*

- ### **`exp(-i eps dtau sigma.n_h)` per estremita'**, esatta *(`cos a I - i sin a sigma.n`)*, unitaria al bit; ### **`eps = 0.5`**, «il valore del banco», ### **la sua origine fisica APERTA** *(il posto `A1`: «`eps * dtau` e' cio' che conta»)*.
- **Che cosa conserva:** ### **la norma per estremita'** *(e' unitaria)* e ### **l'elicita' `psi^dagger sigma.n_h psi` per estremita'** *(commuta con `sigma.n_h`)*.
- **Gli altri due pezzi della camminata non hanno numeri:** ### **il Grover** `P_u + e^{i theta}(I - P_u)` *(«il `2/d` viene dal GRADO del nodo»)* e ### **lo spostamento** `alpha I + beta S_U` per arco. ### **Si scrivono per `d = 6` e `d = 12` SENZA cambiare forma.**

### La derivazione su `6` (e `12`) direzioni

**Le condizioni:**
1. ### **unitaria** *(la camminata resta unitaria)*;
2. ### **locale, per estremita'** *(«NON legge il vicino»)*;
3. ### **covariante sotto il gruppo della griglia:** se l'automorfismo `g` porta l'estremita' `h` in `g h`, ### **la moneta in `g h` e' la moneta in `h` ruotata da `g`** *(sullo spin)*;
4. ### **conserva l'elicita' lungo `n_h`** *(come oggi)*.

**Che cosa ne segue:** una matrice `2 x 2` unitaria che commuta con `sigma.n_h` ### **e' `exp(i (a I + b sigma.n_h))`**; la fase globale `a` ### **e' la `U(1)` di `U1-FASE-GLOBALE`** *(non osservabile)*; ### **resta UN SOLO numero, `b = - eps dtau`**, ### **lo stesso per tutte le estremita' per la condizione `3`.** ### **Quindi: `6` direzioni in 2D, `12` in FCC, la STESSA forma di oggi, e UN grado di liberta' libero: `eps dtau`.**

- ### **I GRADI DI LIBERTA' LIBERI, contati: `1`** *(`eps dtau`)* -- ### **lo stesso di oggi.** ### **E' una domanda per Luca, non una scelta.**
- ### ⚠ **Un secondo grado di liberta', se si toglie la condizione `4`:** una moneta che ### **non** commuta con `sigma.n_h` *(una rotazione attorno a un altro asse legato alla griglia)*. ### **La condizione `4` e' cio' che oggi lega lo spin al moto** *(`[[N-DIREZIONI-DI-MOTO]]`)*: ### **toglierla e' una scelta di fisica**, e non la propongo.

### ⭐ LA DOMANDA DEI SOTTOGRUPPI FINITI DI `SU(2)` *(esaminata qui, NON registrata nell'indice)*

**La domanda:** ### **il grado di liberta' libero `eps dtau` si puo' fissare SENZA un numero scelto a mano, chiedendo che la moneta stia in un SOTTOGRUPPO FINITO di `SU(2)` coerente con la simmetria della griglia?**

**Il fatto che decide** *(matematica nota, scritta come conto)*: ### **la moneta e' una rotazione di spin di angolo `2 eps dtau` attorno all'asse `n_h`**, e ### **`n_h` e' un asse DOPPIO** del gruppo di simmetria del punto *(un asse attorno a cui la simmetria ammette solo la rotazione di `pi`)*:
- in 2D le `n_h` stanno nel piano: ### **sono gli assi doppi del diedrale `D6`** *(visto come gruppo di rotazioni in 3D: la rotazione di `pi` attorno a un asse del piano)*;
- in FCC le `n_h = (+-1, +-1, 0)/sqrt 2` ### **sono gli assi doppi dell'ottaedrico `O`** *(le `6` diagonali delle facce del cubo)*;
- **e oggi**, sul quadrato, le `n_h` sono gli assi doppi del diedrale `D4`.

**Nel doppio ricoprimento** `2G subset SU(2)`, ### **gli elementi di rotazione attorno a un asse doppio sono SOLO `+- i sigma.n`** *(la rotazione di `pi`, mezzo angolo `pi/2`)*, ### **piu' l'identita'** `+- I`. Quindi:

| il gruppo | dove | l'ordine | contiene `-i sigma.n_h`? | che cosa fissa |
|---|---|---|---|---|
| ### **binario diedrale di `D6`** *(`Dic6`)* | 2D | `24` *(`2 x 12`)* | ### **si'** *(le `6` rotazioni di `pi` attorno agli assi del piano -- gli assi a passi di `30` gradi, fra cui le `3` delle `n_h` -- si alzano a `+- i sigma.n`)* | ### **`eps dtau = pi/2`** *(mod `pi`)* |
| binario diedrale di `D4` *(`Dic4`)* | oggi *(quadrato)* | `16` | si' | ### **`eps dtau = pi/2`** |
| ### **binario ottaedrico** `2O` | FCC | `48` | ### **si'**: i suoi `12` elementi `(+-i +-j)/sqrt 2`, `(+-i +-k)/sqrt 2`, `(+-j +-k)/sqrt 2` *(quaternioni)* ### **sono esattamente `-i sigma.n` per le `12` direzioni FCC** | ### **`eps dtau = pi/2`** |
| binario tetraedrico `2T` *(i `24` di Hurwitz, la `24`-celle)* | FCC | `24` | ### **NO:** i suoi elementi immaginari puri sono ### **`+-i, +-j, +-k`** *(gli assi `x, y, z`)*; ### **le diagonali delle facce non sono suoi assi** | ### **incompatibile con le `n_h` della FCC** |
| binario icosaedrico `2I` | confronto | `120` | ### **NO** nella sua orientazione standard *(contiene `2T`, non `2O`: non ha gli assi quadrupli del cubo)* | ### **incompatibile con la simmetria cubica** |

- ### **IL RISULTATO DEL CONTO:** ### **se la moneta sta nel doppio ricoprimento del gruppo della griglia, `eps dtau = pi/2`** *(mod `pi`)*, ### **la STESSA risposta su quadrato, triangoli e FCC**, e ### **zero gradi di liberta' liberi.** ### **La moneta diventa `-i sigma.n_h`**: ### **una rotazione di spin di `pi` attorno alla direzione di moto.**
- ### **LE CONSEGUENZE, scritte perche' Luca le pesi:**
  - ### **`eps dtau = pi/2` vale per QUALE `dtau`?** ### **Al passo dell'automa** *(`dtau = dtau_rif = 1`, la risposta di principio del `2026-10-20`: l'automa vero e' a stati finiti nelle scelte)* ### **`eps = pi/2`**; ### **ai sotto-passi** *(`dtau < 1`, il limite continuo)* la moneta del sotto-passo ### **NON sta nel gruppo** *(e' una sua radice)*. ### **E' coerente con «finito nelle scelte, continuo nelle relazioni»** *(la scelta finita e' il passo intero)*, ### **ma va deciso.**
  - ### **Oggi `eps = 0.5`**, cioe' `eps dtau_rif = 0.5`, ### **non `pi/2 = 1.5708`**: ### **cambiarlo cambia la fisica di tutti i referti di `L2`.**
  - ### **Sullo spinore ALLINEATO** *(autovettore `+1` di `sigma.n_h`)* ### **`-i sigma.n_h` e' una FASE** *(`-i`)*: ### **sulla materia uniforme la moneta non mescola niente.** ### **Il termine della moneta in `H`** *(`eps h`)*, ### **che `69094682` ha visto precedere**, ### **cambierebbe valore** *(`eps` da `0.5` a `pi/2`)*.
  - ### **E' «la legge, non il numero»** *(`A1`)*: ### **il numero lo darebbe la simmetria.** ### **Ma e' una DERIVAZIONE CONDIZIONATA** -- ### **regge solo se si accetta che la moneta stia in un gruppo finito**, e ### **quella premessa e' di Luca.**
- ### **SE NON REGGE:** ### **se la moneta non deve stare in un gruppo finito**, `eps dtau` ### **resta libero** *(come oggi)* e va ### **derivato da altro** *(il posto `A1`)*.

## d) LO STATO DI MATERIA

- ### **Lo spinore allineato `sigma.n_h`** per estremita' *(`statica_protocollo.chi_allineato`, `scena_l2.spinore_allineato`)*: ### **si generalizza senza cambiare forma** *(l'autovettore `+1` di `sigma.n_h` per ogni `h`)*.
- ### **LE DIREZIONI USCENTI SOMMANO A ZERO?** ### **Si', in 2D e in FCC, per costruzione:** ### **vengono a coppie opposte** *(`n(-h) = -n(h)`: `6` = `3` coppie, `12` = `6` coppie)*, quindi ### **`sum_h n_h = 0` esatto.** ### **E' la stessa ragione di oggi** *(`scena_l2`: «le direzioni uscenti -- che su un toro sommano a zero»)*.
- ### ⚠ **Ma la somma delle ELICITA' del nodo** *(`h_k = sum_h psi_h^dagger sigma.n_h psi_h`)* ### **non e' zero** sullo stato allineato *(ogni estremita' da' `+|psi_h|^2`)*: ### **e' cio' che fa la materia uniforme di oggi, e resta.**
- ### **La materia uniforme a `x` dato:** `rho_k = x Lambda_m` come oggi; ### **con `6` estremita' `Lambda_m` per nodo cambia** *(vedi `f`)*.

## e) L'OLONOMIA

- ### **La plaquette e' il TRIANGOLO di `3` archi**; ### **l'olonomia di un quadrato** *(il ciclo di `4` archi `(0,0) -> (1,0) -> (1,1) -> (0,1) -> (0,0)`)* ### **e' il prodotto delle olonomie dei due triangoli** in cui la diagonale lo divide *(la diagonale si percorre in versi opposti e si cancella)*.
- ### **FCC:** le facce triangolari ### **dei tetraedri e degli ottaedri** del nido d'ape *(sez. `i`)*; ### **ogni ciclo si scompone in triangoli.**
- ### **IL QUANTO DI OLONOMIA** *(`[[MITOSI-QUANTO-OLONOMIA]]`)* ### **vivrebbe sul triangolo**, il ciclo piu' corto.
- ### **LA FUNZIONE `proto_camminata/geometria.py` `olonomia(sc, U, ciclo)`** ### **e' gia' definita su cicli qualsiasi** *(costruisce il prodotto lungo un ciclo dato come lista di nodi)*. ### **VERIFICATO: il passo dei `14` pezzi NON la usa** -- `grep -rn olonomia primo_ordine/*.py` non trova chiamate; ### **`proto_camminata/geometria` la importa solo `primo_ordine/_collauda_confronto.py`** *(un collaudo)*. ### **Oggi le `U` d'arco sono FISSE** *(`[[PROVV-U-FISSE-TRE-SCENE]]`)*, e l'olonomia ### **non entra in nessuna legge del passo.**

## f) LE `7` LEGGI E `S3`, con `6` *(e `12`)* estremita'

| la legge | che cosa cambia | la derivazione |
|---|---|---|
| `CAMM-MONETA-SPIN` | le `n_h` *(`b`)*; ### **`eps`** *(`c`)* | ### **regge** *(la forma e' per estremita')*; il numero e' la domanda |
| `CAMM-GROVER` | ### **`d = 6`** *(`12`)* nel `P_u` | ### **regge senza cambiare:** il `2/d` e' gia' «dal grado del nodo» |
| `CAMM-SPOSTAMENTO` | `3` *(`6`)* archi propri; ### **le `U` su `3` assi** | ### **regge** *(per arco)*; ### **la media armonica di `dtau_arco` (`B-3`) uguale** |
| `CAMM-GROVER-VUOTO` | `d = 6` *(`12`)* | ### **regge** |
| `CAMM-SPOSTAMENTO-VUOTO` | per arco | ### **regge** |
| `CAMM-MATERIA-VUOTO` *(`S3`)* | ### **`rho` e `Lambda` per nodo sommano `6` *(`12`)* estremita'** | ### **la forma regge** *(`N(rho, Lambda) = rho ln(rho/(rho+Lambda))` per nodo)*; ### **cambia il CONFRONTO:** a vuoto per estremita' uguale ### **`Lambda_m` passa da `4` a `6`** *(`12`)* -- ### **la regola di scala va estesa fra geometrie** *(domanda per Luca: si tiene fisso il vuoto per estremita', o `Lambda` per nodo, o il rapporto `rho/Lambda`? Per la precisazione delle `11:45` del `2026-10-20` contano i RAPPORTI)* |
| `CAMM-FASE-VUOTO` | ### **`Omega` contiene tutti i termini di `H`** *(Grover, hop, moneta, `N`)* | ### **la derivazione regge** *(il punto fisso e' sul nodo)*; ### **va RIMISURATA** *(`C1`-`C5` di strada `(d)`)* |

- ### **IL PALINDROMO DI `14` PEZZI RESTA:** ### **l'ordine e' delle LEGGI, non della griglia** *(`composizione.ORDINE`)*; ### **e lo spostamento agisce su TUTTI gli archi insieme** *(ogni arco scambia le sue due estremita')*, ### **qualunque sia il loro numero.** ### **Quindi anche l'IMPRONTA `2e7f795d2a52fbe7` potrebbe restare** *(e' l'impronta dell'ordine)* -- ### **da verificare: se cambia solo la scena, la tabella delle leggi non cambia.**
- ### **`A14`** *(la conservazione locale)*: ### **ogni legge e' per estremita', per nodo o per arco** *(raggio `0`)*, ### **e lo resta**; ### **i collaudi che la provano vanno rifatti sulla griglia nuova** *(sez. `g`)*.
- ### **La `C`-simmetria e `PTheta`:** dipendono dalla moneta e dall'ordine, ### **non dal grado**: ### **da rimisurare, non da rifare.**

## g) CHE COSA VA RIMISURATO *(contato)*

| | che cosa | il costo stimato |
|---|---|---|
| ### **`M-B1`** | il raccordo AL BIT col motore vecchio | ### ⛔ **NON si puo' rifare:** il motore vecchio e' quadrato. ### **Il sostituto proposto:** un raccordo con ### **il banco di `proto_camminata`**, che lavora su ### **grafi qualsiasi** *(`sc["archi"]`)* -- ### **da verificare**, `~1` giorno |
| `M-B2` | `H_tot` al secondo ordine | ### **si rifa' cosi' com'e'** su una scena triangolare, minuti |
| `C1`-`C5` di strada `(d)` | la conservazione di `G` col termine della fase | si rifanno, ### **`~1` ora** *(oggi `C1` gira in minuti)* |
| ### **i collaudi della suite** | `python primo_ordine/collauda.py` | ### **`64` voci** *(comando: `grep -c '^    ("' primo_ordine/collauda.py`)*; ### **quelli che costruiscono una scena quadrata vanno estesi** -- ### **da censire uno per uno**, `~1`-`2` giorni |
| ### **l'impronta** | `2e7f795d2a52fbe7` | ### **forse invariata** *(sez. `f`)*: un comando, `_genera.carica` |
| ### **i referti di `L2`** | `doc/referti_l2/*.txt` | ### **`54` file** *(comando: `ls doc/referti_l2/*.txt \| wc -l`)*; ### **restano validi AL LORO COMMIT** *(sono del quadrato)*; ### **si rifanno solo quelli che il piano chiede** *(sez. `k`)* |

## h) GLI STRUMENTI

- ### **La stabilita' lineare** *(`csv/_stabilita_lineare.py`)*: ### **la cella da `24` a `36` reali** *(`NC = 12` complessi diventa `18`; `celle()` e `perturba()` hanno le `4` estremita' scritte dentro, `reshape(n, 8)` e `reshape(n, 4)`)*; ### **la trasformata di Fourier sulle celle** resta, con ### **le coordinate del reticolo triangolare** *(`k` nella zona esagonale)*. ### **FCC: `72` reali**, Fourier in 3D. ### **Costo:** l'estensione `~1` giorno; ### **la corsa** a lato `32` in 2D ### **`~1.5` volte** quella di oggi *(`36` contro `24` impulsi)*.
- ### **La scena:** `scena_l2.scena` e `corrente.toro` ### **costruiscono il toro QUADRATO** *(grado `2 d`)*: ### **serve `toro_triangolare`** *(e `toro_fcc`)*, con ### **la stessa convenzione degli indici** *(sez. `a`)* e ### **le `n_h` del grafo** *(sez. `b`)*.
- ### **Il toro a `6` vicini:** e' `toro_triangolare`; ### **verificare che sia regolare e non bipartito** *(un collaudo: il ciclo di `3`)*.
- ### **Il censimento dei punti fissi** *(`csv/_censimento_punti_fissi.py`)*: ### **legge il codice, non la scena**: ### **non cambia.**

## i) IL 3D: LE TRAPPOLE, SCRITTE

- ### **La BCC** *(`8` vicini)* ### **e' BIPARTITA** *(i due sottoreticoli cubici)*: ### **NON toglie il modo alternato.** ### **Non e' una strada.**
- ### **I tetraedri REGOLARI da soli NON tassellano lo spazio:** il loro angolo diedro e' ### **`arccos(1/3) = 70.53`** gradi; ### **`5` attorno a uno spigolo fanno `352.64`**, e mancano ### **`360 - 5 arccos(1/3) = 7.36`** gradi.
- ### **Il nido d'ape tetraedri-ottaedri e' PIATTO:** l'angolo diedro dell'ottaedro e' ### **`pi - arccos(1/3) = 109.47`** gradi, e ### **attorno a ogni spigolo `2` tetraedri + `2` ottaedri danno `2 x 70.53 + 2 x 109.47 = 360` esatti.** ### **I suoi vertici SONO la FCC.**
- ### **E un trucco da non fare:** ### **cercare un reticolo «piu' isotropo» del necessario.** La FCC ha ### **`12` vicini, il massimo dell'impacchettamento**: ### **basta lei.**

## j) LE PREVISIONI, scritte prima di ogni conto *(dalla scheda `C3` di `c82b51dd` e da `594417f6`)*

- ### **`R1`:** ### **il picco a `(pi, pi)` sparisce come tale** *(il modo alternato non esiste)*; il massimo va ### **al bordo della zona esagonale** *(i punti `K` o `M`)* con un `gamma` ### **fra quello di `(pi, 0)` di oggi** *(`0.48`)* ### **e quello della banda** *(`0.41`)*.
- ### **`R2`:** ### **la banda resta entro `~10%`** *(`0.37`-`0.45`)*.
- ### **Se la banda di `R2` cambiasse molto, dipenderebbe dalla geometria** e non solo da `S3`.
- ### ⚠ **Le previsioni presuppongono la STESSA moneta** *(`eps = 0.5`)*: ### **con `eps dtau = pi/2`** *(sez. `c`)* ### **la camminata e' un'altra**, e ### **le previsioni valgono solo per il confronto a moneta invariata.**

## k) IL PIANO A GRADINI, coi criteri di STOP

| il gradino | che cosa | lo STOP | il costo |
|---|---|---|---|
| `T0` | ### **le decisioni di Luca** *(la moneta: `eps` libero o `pi/2`; la regola di scala fra geometrie)* | ### **nessun codice prima** | -- |
| `T1` | ### **`toro_triangolare` e la scena**, coi collaudi del grafo *(regolare, non bipartito, `n_h` covarianti, `sum n_h = 0`)* | ### **un collaudo del grafo che cade** | `~1` giorno |
| `T2` | ### **la camminata sui triangoli** *(il passo di `14` pezzi sulla scena nuova)*, ### **unitaria al bit**, la camminata sola senza crescita, ### **il raccordo che sostituisce `M-B1`**, `M-B2`, `C1`-`C5` di strada `(d)` | ### **la norma non al bit; il raccordo che cade; `M-B2` sotto la pendenza `1.9`** | `~2`-`3` giorni |
| `T3` | ### **la stabilita' lineare a `36` reali**: `R1` e `R2`, le previsioni `j` | ### **il caso che deve fallire** *(la camminata sola)* ### **che cresce** | `~1` giorno + le corse |
| `T4` | ### **la FCC sul toro 3D** *(`72` reali)*, gli stessi gradini | ### **gli stessi** | ### **settimane** *(la cella e le corse: a lato `16` la FCC ha `16^3 / 2 = 2048` nodi, a lato `32` `16384`)* |
| *(in agenda)* | ### **la sfera e la topologia** *(`[[SPAZIO-TRIANGOLAZIONE-SENZA-POSIZIONI]]`)* | ### **si apre solo dopo un risultato MISURATO di `T3`** | -- |

---

## LE DOMANDE PER LUCA *(una alla volta, nella relazione)*

1. ### **I gradi di liberta' che la derivazione della moneta lascia liberi sono `1` (`eps dtau`). Un sottogruppo finito di `SU(2)`** *(il doppio ricoprimento del gruppo della griglia: `Dic6` in 2D, `2O` in FCC)* ### **lo fissa a `pi/2`.** ### **Si accetta la premessa «la moneta sta in un gruppo finito», e a quale `dtau` (il passo dell'automa, `dtau = 1`)?**
2. *(dopo la prima)* ### **La regola di scala fra geometrie:** quale grandezza si tiene fissa nel confronto `4` contro `6` vicini.
3. *(dopo la seconda)* ### **Il sostituto di `M-B1`.**
