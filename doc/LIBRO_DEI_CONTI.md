# IL LIBRO DEI CONTI DELL'ENERGIA — dare e avere, per ogni conto e ogni regione

> **Il mandato:** di Luca, `2026-10-27`, dopo la decisione delle `12:54` *([[LIBRO-DEI-CONTI]], [[ENERGIA-DEL-LEGAME]])*: ### **i bilanci dell'energia per ogni elemento, col dare e l'avere, non solo il saldo.** ### **E' l'applicazione generale della regola di `primo_ordine/crescita.py`:** *«una regola che aggiunge o toglie gradi di liberta' sposta energia; cio' che esce da `H` deve andare DA QUALCHE PARTE»*.
> ### **Il task history e' `doc/TASK_HISTORY/2026-10-27_libro_dei_conti.md`.** ### **Questo documento viene PRIMA del codice** *(`csv/_libro_dei_conti.py`)*.
> ### ⛔ **STATO: SCRITTO, CON UNA DOMANDA APERTA** *(il paragrafo `(c)`)*: ### **la corrente del nucleo NON e' la corrente dell'energia dei bilanci, e quella esatta non si calcola sulle nostre scene.** ### **La definizione della corrente sul confine e' una scelta di metodo: lo strumento aspetta la risposta.**

> **I riferimenti** *(le righe sono del blob di OGGI, `sha1-BYTE` fra parentesi; si cerca per NOME di funzione, `CLAUDE.md` par.2)*: ### `primo_ordine/energia_pesata.py` *(`7889c512`)*, `primo_ordine/energia.py` *(`a8e66695`)*, `primo_ordine/corrente.py` *(`52d1d72b`)*, `primo_ordine/materia_vuoto.py` *(`68ff3ffd`)*, `primo_ordine/crescita.py` *(`0d15bc4a`)*, `csv/_energia_del_legame.py` *(`0197ecc0`)*, `csv/_scomposizione_solitone.py` *(`17dde60a`)*.

## (a) I CONTI

| il conto | la definizione locale | dove vive | da dove viene |
|---|---|---|---|
| **la MATERIA** *(la camminata di `psi`)* | ### `H_cam(psi)`: ### **per nodo `-pi [(nrm_psi - pu_psi)] + eps h`;** ### **per arco `-pi (nrm_a - 2 Re <p0|U^+|p1>)/2`** | ### **nodo, e arco diviso a META' fra i suoi due nodi** | `energia_pesata.termini_di_h` *(r.`148`; il nodo r.`173`, la moneta r.`184`, l'arco r.`197` e r.`202`)*, ### **chiamata col vuoto messo a ZERO** *(cosi' il suo `N` vale `0`)*; ### **la divisione a meta'**: `_energia_del_legame.per_nodo` *(r.`102`)* |
| ↳ **i COSTITUENTI** | ### `rho_k e_K(lambda)` | nodo | ### `e_K` = l'energia per unita' di norma dello stato uniforme del ramo *(`_scomposizione_solitone.stato_uniforme`, `parti` r.`107`)* |
| ↳ **la CINETICA** | ### `H_cam(psi)_k - rho_k e_K` | nodo | ### **per differenza** |
| **il LEGAME** *(la forma ATTIVA, dichiarata in ogni uscita)* | ### **`S1` in memoria:** `Lambda_k F_1(rho_k / Lambda_k)`, `F_1(x) = x - arctan x`; ### **`S3` nel nucleo:** `rho_k ln(rho_k / (rho_k + Lambda_k))` | nodo | ### **`S1`:** `_scomposizione_solitone.F1` *(r.`54`)*, la fase `alpha_1 = F_1'` da `_screening_forme_s3.pezzi_di`; ### **`S3`:** `energia_pesata.termini_di_h` *(r.`191`)*, `materia_vuoto.alpha` *(r.`80`)* e `beta` *(r.`94`)* |
| **il VUOTO** *(la camminata di `phi`)* | ### `H_cam(phi)`: ### **per nodo `-pi (nrm_phi - pu_phi)`, per arco `-pi (|f0|^2 + |f1|^2 - 2 Re f0* f1)/2`** | nodo, e arco a meta' | `energia_pesata.termini_di_h` *(r.`173`, r.`202`)*, ### **chiamata con la materia a ZERO** |
| **la LUCE** *(il campo `U(1)`)* | ### **predisposto, VUOTO: il campo non esiste** | arco *(il collegamento)* | — |
| **lo SPAZIO** *(i nodi nati, la mitosi)* | ### **predisposto, VUOTO: nessuna regola di crescita accesa** | nodo | `primo_ordine/crescita.py` *(il bilancio dichiarato: `ingressi`, `uscite`, `bilancio`)* |

- ### **`H_tot` = la materia + il legame + il vuoto, coefficiente `1`** *(letto dal codice in `b04ec0d3`: tutti i pezzi applicano una fase `-s` volte la derivata della loro energia)*.
- ### ⚠ **I DUE LEGAMI NON SI MESCOLANO:** ### **se gira `S1`** *(in memoria, `_screening_forme_s3.forma`)* ### **il conto del legame e' `S1`, e `termini_di_h` si chiama coi campi separati;** ### **se gira il nucleo, `S3`.** ### **L'uscita dice quale.**

## (b) LE REGIONI

- ### **Una PARTIZIONE dei nodi dichiarata da chi misura** *(dischi, anelli, semipiani: una maschera per regione)*, ### **e ogni nodo in UNA sola regione.** ### **Un arco con i due nodi in due regioni diverse e' un ARCO DI CONFINE:** ### **il suo termine va a meta' fra le due.**
- ### **LA SOMMA DELLE REGIONI = IL TOTALE:** ### **AL BIT se le somme si fanno con `math.fsum` sui valori per nodo** *(la somma esatta, arrotondata una volta)*; ### **con la somma di `numpy` solo entro l'arrotondamento** *(l'ordine delle somme cambia)*. ### **Lo strumento usa `fsum`, e il sigillo `(i)` lo controlla.**

## (c) LE CORRENTI — ⛔ LA PREMESSA CHE CADE, E LE QUATTRO STRADE

### **LA PREMESSA DEL MANDATO:** ### **«dalla corrente d'energia sugli archi gia' nel nucleo» (`corrente.py`, `energia.py`).** ### **LETTO DAL CODICE, NON REGGE, per tre motivi:**

1. ### **E' LA CORRENTE DI UN'ALTRA ENERGIA.** ### **`energia.py` definisce `e_h = Re[conj(psi_h) . (W psi)_h]`** *(`densita_estremita`, r.`74`)*, ### **con `W` = moneta → grover → spostamento** *(il tick LINEARE dell'era `1`)*: ### **una correlazione fra due tempi** *(il docstring di `corrente.py` lo dice)*, ### **non la `H_tot` di `termini_di_h` dei bilanci di `15df5c63`.** ### **E il suo legame e' `N` di `S3`** *(`densita_nodo`, r.`103`)*.
2. ### **`energia.corrente`** *(r.`141`, «cio' che lo spostamento porta»)* ### **NON CHIUDE IL BILANCIO:** ### **lo dice l'annotazione del `2026-10-13` nello stesso file** *(«quella candidata NON CHIUDE il bilancio, ed e' misurato»)*.
3. ### **LA CORRENTE ESATTA, `corrente.py`, ESISTE MA NON SI CALCOLA QUI:** ### **si costruisce dalla forma quadratica di `Delta e_k`** *(`forma_quadratica`, r.`102`)* ### **con `D + D(D-1)/2` valutazioni del tick, `D = 8m`** *(`dim`, r.`46`)*; ### **sul toro a triangoli `L 48` gli archi sono `m = 3 L^2 = 6912`, `D = 55296`:** ### **circa `1.5e9` tick per UNO stato** *(il docstring: «su una scena grande non si fa»)*. ### **E vale per un tick LINEARE:** ### **col legame `S1` il tick dipende dallo stato, e `Re <psi|T(psi) psi>` non si conserva.**

### **LE QUATTRO STRADE** *(nessuna scelta: la decide Luca)*

| | la strada | che cosa da' | il limite | il costo |
|---|---|---|---|---|
| **A** | ### **LA CORRENTE NETTA PER ANELLI, NEL TEMPO:** ### **regioni annidate** *(dischi)*; ### **la corrente netta attraverso il bordo del disco `j` in un tick = `-Delta E(disco j)`** *(meno il residuo, vedi `(d)`)* | ### **il DARE e l'AVERE NEL TEMPO:** ### **i tick in cui l'energia entra e quelli in cui esce, separati, e le loro somme** *(la domanda di `15df5c63`: il vuoto lontano rimanda indietro?)* | ### **NON separa entrante e uscente NELLO STESSO tick** *(su archi diversi del confine)*; ### **il residuo locale non e' separabile dalla corrente:** ### **se ne conosce solo la somma su tutto il toro** *(`Delta H_tot`)* | ### **un `H_tot` per regione per tick:** ### **come `15df5c63`, a ogni tick** |
| **B** | ### **PEZZO PER PEZZO:** ### **la variazione di ogni conto in ogni regione dopo OGNI pezzo del tick** *(`tick.percorri_tick` coi pezzi uno alla volta)*; ### **solo gli SPOSTAMENTI muovono ampiezza fra nodi** | ### **la quadratura ESATTA per costruzione** *(la somma dei pezzi e' il tick)*; ### **chi scambia con chi, pezzo per pezzo** | ### ⚠ **ogni pezzo conserva il SUO termine e cambia gli ALTRI di ordine `s`:** ### **il Grover sposta energia nei termini d'arco, lo spostamento nei termini di nodo, e si compensano solo nel palindromo** *(il saldo del tick e' di ordine `s^2`)*. ### **Il dare e l'avere pezzo per pezzo sarebbe dominato da questo va-e-vieni del passo, non dalla fisica** | ### **`14` valutazioni dell'energia per tick** |
| **C** | ### **LA CORRENTE ESATTA del nucleo** *(`corrente.py`)* ### **per l'energia conservata ESATTAMENTE da un tick unitario, `Re <psi|T psi>`** | ### **una corrente locale che CHIUDE la continuita', portata misurata `3` archi** *(`doc/REFERTO_corrente_locale.md`)* | ### **solo il tick LINEARE, e solo scene piccole** *(`1.5e9` tick a `L 48`)*; ### **e' un'altra energia** | ### **proibitivo qui** |
| **D** | ### **UNA CORRENTE NUOVA per `H_tot`, DERIVATA:** ### **lungo il flusso di ogni pezzo `d<H_R>/d theta = i <[G, H_R]>`, che vive dove il supporto di `G` attraversa il confine di `R`** | ### **la corrente locale di `H_tot`, entrante e uscente per arco** | ### **e' un lavoro di derivazione, non uno strumento:** ### **il commutatore ha anche una parte INTERNA** *(i pezzi non commutano)*, ### **che e' l'errore del passo, e va separata** | ### **da stimare** |

### ⭐ **LA MIA RACCOMANDAZIONE** *(non una decisione)*: ### **`A` per il dare e l'avere sul confine** *(e' cio' che risponde alla domanda di `15df5c63`, e costa come `15df5c63`)*, ### **piu' `B` come DIAGNOSI** ### **per misurare quanto e' grande il va-e-vieni del passo pezzo per pezzo** *(se e' piccolo rispetto ai flussi, `B` diventa leggibile)*. ### **`D` e' la strada giusta a lungo termine, ma e' una derivazione.**

### **GLI SCAMBI NELLO STESSO NODO** *(la materia col legame, il legame col vuoto)*: ### **con `A` NON SI SCRIVONO** *(si vede solo il saldo di ogni conto per regione)*; ### **con `B` si scrivono pezzo per pezzo:** ### **il pezzo del legame cambia le fasi di `psi` e `phi` nel nodo, quindi NON cambia il legame** *(`rho`, `Lambda` fissi)* ### **e cambia i termini d'ARCO della camminata** *(la differenza di fase sull'arco)*: ### **lo scambio del legame e' verso la camminata, sugli archi del nodo.**

## (d) LA QUADRATURA

### **Per ogni regione e ogni tick:** ### `Delta E_R = (entrante - uscente) + scambi + residuo`.

- ### **IL RESIDUO HA DUE PARTI:** ### **l'errore del passo** *(la composizione palindroma conserva `H_tot` a meno di termini LIMITATI di ordine `s^2`: `b04ec0d3`)* ### **e cio' che resta** *(zero entro l'arrotondamento, o un conto mancante)*.
- ### **L'ERRORE DEL PASSO SI MISURA:** ### **la deviazione massima di `H_tot` sulla corsa, a `s 0.3` e a `s 0.15` sullo stesso tempo fisico:** ### **il rapporto deve essere `4` se e' di ordine `s^2`.** ### **Questo NON dipende dalla strada della corrente.**
- ### ⚠ **CON LA STRADA `A`** ### **la quadratura per regione non e' un controllo indipendente:** ### **la corrente netta e' DEFINITA dalla differenza.** ### **Il controllo e' sul totale:** ### **`sum_R residuo_R = Delta H_tot`, che deve stare dentro l'errore del passo misurato.**
- ### ⚠ **CON LA STRADA `B`** ### **la quadratura e' un'IDENTITA'** *(la somma dei pezzi e' il tick)*: ### **il contenuto non banale e' come si distribuisce il residuo fra le regioni.**

## (e) LE CONVENZIONI

- ### **LO ZERO, in ogni uscita:** ### **`lambda`** *(`1/2` lo zero simmetrico, `0` quello di oggi)*; ### **la costante `2 pi lambda` per unita' di norma della materia, e la stessa per il vuoto** *(misurata in `0fb93b8c`, entro `8.9e-15`)*. ### **Le DIFFERENZE nel tempo per regione cambiano di `2 pi lambda` volte la differenza di norma della regione.**
- ### **LE UNITA':** ### **le energie in unita' di `N |e_K(0)|` per i confronti** *(la lezione di `0fb93b8c`: mai frazioni con `E0` al denominatore)*.
- ### **LA FORMA DEL LEGAME** *(`S1` o `S3`)* ### **e `cs`** *(acceso o spento)* ### **in ogni uscita.**
