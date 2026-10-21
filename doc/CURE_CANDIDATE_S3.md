# LE CURE CANDIDATE PER L'INSTABILITA' DI `S3` — **NESSUNA SCELTA**

> **Il mandato:** decisione di Luca del `2026-10-20` alle `21:34`. Task history
> `doc/TASK_HISTORY/2026-10-20_cure_candidate_s3.md` *(`71d07ae6`)*.
> ### ⛔ **Questo e' un DOCUMENTO: nessun codice di fisica, nessuna corsa, nessuna cura scelta.**
> Impronta `2e7f795d2a52fbe7` e `leggi.yaml` intatti. ### **Le scelte sono di Luca.**
> ### **`LINEARE`, `Lambda_c`, le letture «alla Jeans» o di modulazione, lo stato finale FERMI;
> `D4` da rileggere.**

**Nomi:** in questo documento `C1`...`C5` sono ### **le CURE**. I controlli di strada `(d)` si
scrivono per intero, «`C1`-`C5` di strada `(d)`», per non confonderli.

---

## 1. I FATTI DI PARTENZA *(citati dai referti, coi commit)*

| | il fatto | il numero | il referto |
|---|---|---|---|
| `F1` | ### **senza `S3` nessuna crescita** | la camminata sola, esatta: `max |ln|lambda|| = 4.0e-14` su ogni `k` *(lato `31`)*; `2.1e-13` a lato `32`, `N dtau 100` | `c38367db`; `594417f6` |
| `F2` | ### **la famiglia del PICCO** *(`R1`: `cs` + `CAMM-FASE-VUOTO`)* | pendenza della seconda meta': `(pi, pi)` `0.545` / `0.541` *(lati `32` / `64`)*; la crescita ### **sale monotona lungo `(m, 0)` fino al bordo della zona**, `(pi, 0)` `0.480` / `0.477` | `594417f6` |
| `F3` | ### **la famiglia della BANDA** *(`R2`: `S3` sola)* | `~0.5 pi`: `0.407` / `0.406`; `(pi, pi)` `0.351` | `594417f6` |
| `F4` | ### **il massimo di `R2` si sposta col rapporto `nu_S3 / OMEGA_H`** | `0.31` → `(pi, pi)` *(`0.438`)*; `0.26` → `0.58 pi` *(`0.375`)*; `0.08` → `0.45 pi` *(`0.272`)* | `c38367db` *(intervallo `N dtau 25`, non asintotico)* |
| `F5` | ### **tutto fisso IN NUMERO DI ARCHI al raffinamento** | verdetto `A`; lati `32` e `64` entro l'`1%` | `83edbaa7`; `594417f6` |
| `F6` | `k = 0` ### **transitorio**; ### **Courant ininfluente** | `R1` `0.528`, `0.529`, `0.529` a `dtau` `0.25`, `0.125`, `0.0625` | `594417f6`; `c38367db` |

### ⛔ **QUINDI: un DIFETTO ALLA SCALA DEL RETICOLO, nato da `S3`, in due famiglie.**
**`nu_S3`** e' definito in `c38367db` *(task history `2026-10-20_stabilita_lineare.md`)*: ###
**`nu_S3 = rho d(alpha)/d(rho) = Lambda^2 / (rho + Lambda)^2`**, il ritmo della non linearita'
di `S3` per unita' di `dtau_nodo`; **`OMEGA_H = pi`** e' il coefficiente dei generatori di Grover e
di hop.

### ⚠ **ERRORE `n.27` DEL GUARDIANO** *(registrato in relazione)*: l'ipotesi *«la banda sta dove la
camminata ha la velocita' di gruppo massima»* e' ### **CONTRADDETTA da `F4`**: la velocita' di
gruppo e' una proprieta' della sola camminata e ### **non dipende da `nu_S3`**, mentre il massimo
### **si sposta con lui.** ### **Resta l'ipotesi della RISONANZA** *(`D0`)*.

---

### ⛔ **ANNOTAZIONE DEL `2026-10-21`, `10:00`: `F4` CORRETTO, E LE SUE CONSEGUENZE** *(mandato di Luca sullo STOP di `ac9d0d7d`; si annota, la tabella sopra resta com'era)*

- ### **`F4` CORRETTO:** con la base proiettata, `N dtau 100` e lo stimatore della norma *(`ac9d0d7d`, rifatto al bit in `d0_risonanza_bis`)*, ### **il massimo di `R2` LUNGO `(m, 0)` sta a `m = 8, 8, 7`, cioe' `0.50`, `0.50`, `0.44 pi`** per `x` `0.01`, `0.1`, `1`: ### **QUASI FERMO.**
  - ### **Lo «spostamento con `nu_S3`» di `c38367db` veniva da due cose:** ### **l'intervallo corto** *(`N dtau 25`, non asintotico)* e ### **il massimo GLOBALE**, che ### **salta fra le due famiglie** -- la banda sull'asse, il picco a `(pi, pi)` a `x 0.01` *(dove la diagonale ha il massimo a `m = 16`)*.
- ### **LE CONSEGUENZE:**
  - ### **la previsione di `C1`** *(«il massimo si sposta a `k` piu' piccoli», scheda di `C1`, `(e)`)* ### **perde la sua base**, perche' si appoggiava su `F4`. ### **Si riformula:** con il filtro binomiale `C1` ### **abbassa la banda di un fattore fra `0.75` e `9/16`**, e ### **del suo spostamento non si sa niente** -- ### **non si prevede.**
  - ### **L'errore `n.27` del guardiano va RIDIMENSIONATO:** l'ipotesi della velocita' di gruppo era stata ritirata ### **per `F4`**, e `F4` ### **non regge** sull'intervallo lungo. ### **L'ipotesi non era contraddetta: era solo non provata.**
  - ### **`D0` E' CADUTO** *(`d0_risonanza_bis`)*: nessuna condizione della lista chiusa tiene. ### ⚠ **MA QUASI TUTTE SONO NON INFORMATIVE** *(specificita' oltre il `20%`: con `12` rami gli incroci sono fitti)*: ### **`D0` non conferma la risonanza, e non la smentisce con forza.** ### **Per la regola di questo documento, `C4` PERDE la sua ragione di RISONANZA.**

### 📌 **UN'IPOTESI NUOVA, POST HOC** *(formulata DOPO aver visto i numeri di `ac9d0d7d`, e dichiarata tale)*: ### **«la banda di `S3` sta dove la camminata ha la VELOCITA' DI GRUPPO massima»**

- ### **L'INFORMAZIONE, non un verdetto** *(`d0_risonanza_bis`, `d omega_a / dk` lungo `(m, 0)` dai rami gia' misurati)*: ### **i sei rami dispersivi** *(`3`, `4`, `5`, `9`, `10`, `11`)* ### **hanno `|v_g|` massimo a `m = 9`, cioe' `0.56 pi`** *(`0.45`-`0.46`)*; gli altri sei sono quasi piatti *(`|v_g| <= 0.08`)*. ### **La banda di `R2` sta a `m = 8, 8, 7`.** ### **Vicine, a `1`-`2` passi: compatibile, non provato.**
- ### **LA PROVA VERA SI PROGETTA, non si fa:** serve ### **una manopola che sposti il massimo della velocita' di gruppo SENZA toccare `S3`** -- per esempio ### **la moneta** *(il suo `eps`, o il peso del Grover)*. ### **E' un cambio di fisica: la decisione e' di Luca.**
  - ### **LA PROVEREBBE:** spostando il massimo di `v_g` di `Delta m` passi, ### **la banda di `R2` si sposta degli stessi `Delta m`** *(entro `1` passo)*, ### **a tutti e tre gli `x`.**
  - ### **LA SMENTIREBBE:** il massimo di `v_g` si sposta ### **e la banda resta dov'e'**; oppure la banda si sposta ### **in verso opposto.**
- ### **SE REGGESSE:** `C4` ### **ritroverebbe una ragione**, diversa dalla risonanza *(la banda segue la propagazione, non un accordo di frequenze)*; e `C1`/`C2` ### **agirebbero sull'ampiezza, non sulla posizione.**

---

### ⛔ **ANNOTAZIONE DEL `2026-10-21`, `13:49`: `D0` CHIUSO, NON DECIDIBILE** *(decisione di Luca; si annota)*

- ### **`D0` e' NON DECIDIBILE** *(lato `32` e `64`: nessuna condizione tiene; lato `128` interrotto)*; ### **l'ipotesi post hoc della velocita' di gruppo SI INDEBOLISCE** *(la banda si muove con `x`, `|v_g|` no)*.
- ### **LE CONSEGUENZE:** ### **la scelta della cura NON si appoggia su un meccanismo diagnosticato.** ### **La strada e' lo SCREENING DIRETTO:** ### **`gamma(k)` prima e dopo la cura**, con lo strumento lineare *(`csv/_stabilita_lineare.py --proiettata`)*.
- ### **Il prossimo passo e' una domanda per Luca: quali criteri di screening approvare** *(la domanda `2` della sez.`5`)*.

---

## 2. LA DIAGNOSI PROPOSTA, PRIMA DELLE CURE: `D0` — LA RISONANZA *(da scrivere, NON fatta)*

- ### **Che cosa si calcola:**
  1. ### **le fasi proprie della camminata** `omega_j(k)`: dalla funzione di Green ESATTA della
     camminata sola *(`braccio_c2_esatto` di `csv/_stabilita_lineare.py`, la stessa di `F1`)*, gli
     autovalori di `R(k)` per un tick sono `exp(-i omega_j(k) dtau)`; ### **`24` reali, cioe' `12`
     coppie `+-omega`.** E' ### **la dispersione del reticolo**;
  2. ### **sovrapposte a `gamma(k)` di `R2`** ai tre `x` di `c38367db` *(`0.01`, `0.1`, `1`)*.
- ### **La domanda:** il massimo di `gamma` sta dove ### **una differenza o una somma di
  `omega_j(k)`** *(per esempio `2 omega_a(0) - omega_b(k) - omega_b(-k)`: le due bande laterali di
  un'instabilita' di modulazione)* ### **uguaglia `nu_S3`**, un suo multiplo, ### **o la precessione
  dell'elicita'** *(`69094682`: il termine della moneta che ruota a ogni tick)*?
- ### **IL CRITERIO, da PROPORRE a Luca:** ### **lo scarto fra il `k` del massimo e il `k` di
  risonanza `<= 1` passo di `k`, a TUTTI E TRE gli `x`.** *(Un passo di `k` e' `2 pi / lato`.)*
  - ### **Una cautela da decidere prima:** i `gamma(k)` di `c38367db` vengono da `N dtau 25`, ###
    **che non e' asintotico** *(`16b5d10f`)*. ### **Meglio i `gamma` della base proiettata**
    *(`594417f6`)*, che pero' esistono ### **solo a `x 0.1`**: servirebbero `R2` a `x 0.01` e `x 1`
    con `--proiettata`.
- ### **IL COSTO**, coi tempi misurati:
  - le `omega_j(k)`: ### **secondi** *(`braccio_c2_esatto` a lato `31` e' un tick per `24` impulsi)*;
  - `R2` proiettato a lato `32`, `N dtau 100`: ### **`128` s per `x`** *(`594417f6`)*, quindi
    ### **circa `5` minuti per i due `x` mancanti**, piu' l'analisi;
  - ### **uno strumento nuovo piccolo** *(le `omega_j(k)` e il confronto)*, ### **nessuna legge.**
- ### **CHE COSA CAMBIEREBBE:**
  - ### **SE TIENE:** il difetto ### **e' un accordo fra due ritmi**, `S3` e la camminata. ###
    **Le cure che SPOSTANO uno dei due ritmi ai `k` grandi** *(`C1`, `C2`, `C4`)* ### **salgono**;
    `C3` ### **colpirebbe solo il picco** *(la risonanza della banda non dipende dalla
    bipartizione)*. ### **E si potrebbe PREVEDERE dove va il massimo prima di provare una cura.**
  - ### **SE CADE:** l'instabilita' ### **e' generica** *(non lineare locale contro dispersione,
    come nelle Schroedinger discrete)*, e ### **le cure che RIDUCONO l'accoppiamento non lineare
    ai `k` grandi** *(`C1`, `C2`)* ### **restano le sole dirette**; `C4` ### **perde la sua
    ragione.**

---

## 3. LE CURE CANDIDATE

### Come si legge una scheda

`(a)` la definizione e i pezzi del passo · `(b)` quale famiglia colpisce, e perche' · `(c)` le cinque
domande della Stella Polare · `(d)` `A14` · `(e)` la previsione falsificabile, scritta prima di ogni
conto · `(f)` lo strumento e il costo · `(g)` che cosa romperebbe.

### Un conto che serve a tutte: **come un filtro sui vicini risponde ai `k` delle famiglie**

Su `L2` *(toro quadrato, `4` vicini)* una media pesata `rho_bar_i = w0 rho_i + w1 sum_vicini rho_j`
moltiplica la perturbazione `delta rho(k)` per ### **`f(k) = w0 + 2 w1 (cos kx + cos ky)`**:

| il filtro | `(pi, pi)` | `(pi, 0)` | `(0.5 pi, 0)` | `k = 0` |
|---|---|---|---|---|
| nodo + `4` vicini, pesi uguali *(`1/5`)* | ### **`-3/5`** *(rovescia il segno)* | `1/5` | `3/5` | `1` |
| i soli `4` vicini *(`1/4`)* | ### **`-1`** *(rovescia, non riduce)* | `0` | `1/2` | `1` |
| ### **binomiale** *(`1/2` al nodo, `1/8` ai vicini)* | ### **`0`** | `1/2` | `3/4` | `1` |

### ⚠ **La conseguenza:** ### **non ogni media spegne il picco**; lo spegne ### **solo un peso
preciso**, e ### **quel peso e' un numero da DERIVARE** *(altrimenti e' `A1`)*.
### ⛔ **CORREZIONE del `2026-10-21`** *(segnalata dal guardiano; mandato di Luca delle `09:22`)*: ###
**il «segno rovesciato» delle prime due righe NON vale per `C1`.** In `C1` il filtro sta ### **nel
GENERATORE**, e la perturbazione ci passa ### **due volte** *(in `rho_bar` e nella trasposta del
flusso)*: ### **l'accoppiamento a `k` e' `f(k)^2 >= 0`**, che ### **riduce o spegne, ma non
rovescia mai** *(coi pesi uguali `9/25` a `(pi, pi)`, coi soli vicini `1`)*. ### **Il segno
rovesciato vale solo per una legge INNESTATA** *(una `S3` che legga `rho_bar` una volta sola, senza
derivarne il flusso)*, ### **e per `C5` dipende da come la fase e' riderivata.** ### **Nella prima
versione avevo scritto «vale per `C1` e `C5`»: era incoerente con la scheda di `C1`, che usava gia'
`f(k)^2`.**

---

### `C1` — **`S3` CHE LEGGE `rho` E `Lambda` MEDIATE SUI VICINI** *(un filtro passa-basso)*

- **(a) LA DEFINIZIONE.** `S3` oggi e' il flusso di `N(rho_i, Lambda_i) = rho_i ln(rho_i / (rho_i +
  Lambda_i))`, per nodo *(`materia_vuoto.applica`: fase `alpha dtau` su `psi`, `beta dtau` su
  `phi`)*. ### **`C1`:** il generatore diventa ### **`sum_i N(rho_bar_i, Lambda_bar_i)`**, con
  `rho_bar = W rho`, `Lambda_bar = W Lambda` *(un filtro `W` sui vicini)*. ### **Il flusso ESATTO di
  quel generatore** ruota la fase di `psi` nel nodo `j` di ### **`(W^T alpha(rho_bar, Lambda_bar))_j
  dtau`** -- ### **non di `alpha(rho_bar_j)`**: e' la differenza fra derivare e innestare. ### **Tocca
  un solo pezzo**, `CAMM-MATERIA-VUOTO` *(le due posizioni nell'ordine)*.
- **(b) LA FAMIGLIA.** ### **La perturbazione entra in `S3` due volte attraverso `W`** *(in `rho_bar`
  e nella trasposta)*, quindi l'accoppiamento non lineare a `k` diventa ### **`f(k)^2` volte quello di
  oggi.** Col filtro binomiale: ### **`0` a `(pi, pi)`, `1/4` a `(pi, 0)`, `9/16` a `(0.5 pi, 0)`**.
  ### **Colpisce il PICCO del tutto, il BORDO molto, la BANDA in parte.** Coi pesi uguali
  `f^2 = 9/25` a `(pi, pi)`: ### **riduce, non spegne.**
- **(c) LE CINQUE DOMANDE.**
  1. `A14`: sotto `(d)`.
  2. ### **Gradino:** lo screening lineare e' `(a)`; ### **`(b)`** sarebbe la stessa prova col
     filtro tolto *(e' `F1`/`F3` di oggi)*.
  3. ### **Un numero: i pesi `w0`, `w1`.** ### **Se scelti per spegnere `(pi, pi)` sono una TOPPA**
     *(compensano un difetto)*. ### **Derivati** *(per esempio dalla densita' «di un nodo» come
     media sulla sua cella duale)* ### **sarebbero una costante di accoppiamento.** ### **Oggi non
     c'e' una derivazione.** Non e' un clip.
  4. ### **Tocca `rho` e `Lambda`** dentro `S3`, ### **in entrambi i versi** *(materia → vuoto con
     `beta`, vuoto → materia con `alpha`)*.
  5. ### **Imposta, se i pesi si scelgono per stabilizzare.**
- **(d) `A14`.** ### **La norma si conserva ESATTAMENTE** *(il flusso mette solo fasi, e le fasi non
  cambiano `rho`: `rho_bar` resta fermo durante il pezzo, il flusso resta esatto)*. ### **L'energia
  si conserva LOCALMENTE** con un generatore di raggio `1` *(una corrente fra vicini)*: ### **si'**,
  se il flusso e' quello del generatore e non un'imitazione.
- **(e) LA PREVISIONE** *(scritta prima)*: con il filtro binomiale, ### **l'accoppiamento di `S3` a `(pi, pi)` e' zero:**
  ### **`R2` a `(pi, pi)` scende verso `0`** *(oggi `0.351`)*; ### **`R1` a `(pi, pi)` misura cio' che resta, cioe' il canale di `cs`
  e della fase SENZA `S3` a quel `k`** -- ### **mai misurato** *(`F1` e' la camminata a `cs` spento)*, quindi ### **nessuna previsione
  numerica per `R1`**;
  ### **`R2` la banda scende di un fattore fra `sqrt(9/16) = 0.75` e `9/16`**, cioe' ### **`0.23`-`0.31`**,
  e ### **il massimo si sposta a `k` piu' piccoli** *(per `F4`: un `nu_S3` efficace minore)*. ### **Se
  la banda NON scende, `F4` era letto male.**
- **(f) LO STRUMENTO.** ### **`csv/_stabilita_lineare.py` cosi' com'e'** *(cella `24` reali, la mappa
  tangente numerica non sa niente della legge)*. ### **Ma serve la LEGGE nel passo**: ### **una
  variante di `CAMM-MATERIA-VUOTO` in `leggi.yaml` con `prova: true`**, generata. ### **Costo:** la
  legge `~1` giorno *(gli `8` passi di `doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`)*; il conto ### **`~10`
  minuti** a lato `32` *(`R1` `622` s, `R2` `128` s in `594417f6`)*.
- **(g) CHE COSA ROMPEREBBE.** ### **L'impronta** *(una legge cambia)*; `M-B1` ### **no** *(non tocca la
  camminata)*; ### **`C1`-`C5` di strada `(d)` vanno rifatti** *(`G` contiene `N`)*; `H_tot` di
  `_misura_mb2` ### **va riscritto** *(la sua `N` e' per nodo)*.

---

### `C2` — **UN TERMINE CHE RENDE COSTOSI I MODI CORTI** *(tipo Wilson, o un gradiente nella legge)*

- **(a) LA DEFINIZIONE.** ### **Un termine nuovo in `H`:** ### **`kappa sum_archi (Lambda_i -
  Lambda_j)^2`** *(o su `rho`)*. ### **Il suo flusso esatto** ruota la fase di `phi` *(o di `psi`)*
  nel nodo `i` di ### **`2 kappa (L Lambda)_i dtau`**, con `L` il laplaciano del grafo. ### **E' la
  «RIGIDITA' DEL VUOTO» `(e)` della mappa, sez.`22`** *(proposta di Luca del `2026-10-17`)*, con la
  sua condizione scritta: ### **REVERSIBILE, un'energia del gradiente nel generatore, MAI una
  diffusione.** ### **Un pezzo nuovo** nell'ordine *(palindromo: due mezze posizioni)*.
- **(b) LA FAMIGLIA.** Il laplaciano vale ### **`8` a `(pi, pi)`, `4` a `(pi, 0)`, `2` a `(0.5 pi,
  0)`**, `0` a `k = 0`: ### **un costo che cresce coi `k`.** ### **Colpisce il PICCO piu' di tutto,
  poi il BORDO, la BANDA meno.** ### **Ma il SEGNO decide:** il termine stabilizza solo se ###
  **sposta le bande laterali FUORI dalla risonanza** *(o, se `D0` cade, se ha il segno opposto alla
  non linearita' di `S3`)*. ### **Col segno sbagliato PEGGIORA.**
- **(c) LE CINQUE DOMANDE.**
  1. `A14`: sotto `(d)`.
  2. Gradino `(a)` lo screening; `(b)` con `kappa = 0` e' oggi.
  3. ### **Un numero: `kappa`.** ### **Se tarato per fermare la crescita: una TOPPA.** ### **Se
     derivato** *(la rigidita' del vuoto come proprieta' del vuoto, con la sua scala dal modello)*:
     ### **una costante di accoppiamento.** ### **E la mappa dice gia' che la rigidita' «non
     risolve da sola il criterio `(2)` di `D3`»: e' un ingrediente diverso, non una cura** -- ###
     **usarla COME cura e' esattamente il rischio della domanda `3`.**
  4. ### **Tocca `Lambda`** *(o `rho`)*, ### **non il verso dell'accoppiamento**, ma ### **`cs`
     legge `Lambda`**: ### **una rigidita' sul vuoto cambia la «gravita'»** *(la nota del guardiano
     in sez.`22`: «la non uniformita' di `cs` E' la gravita'»)*.
  5. ### **Imposta, se `kappa` si sceglie per stabilizzare.**
- **(d) `A14`.** ### **Si'**: un termine di `H` di raggio `1`, flusso esatto *(fasi; i moduli non
  cambiano durante il pezzo)*; ### **conserva norma ed energia localmente.** ### **Una diffusione
  NO** *(romperebbe `PTheta` e riaprirebbe `L1`)*.
- **(e) LA PREVISIONE.** Con `kappa` del segno giusto: ### **il picco a `(pi, pi)` scende per primo**,
  ### **la banda per ultima**; ### **sopra un `kappa` critico** la crescita a `(pi, pi)` si spegne,
  ### **e il massimo di `gamma` migra verso `k` piccoli.** ### **L'ordine di grandezza del `kappa`
  critico NON lo scrivo:** ### **un numero che non esce da un conto non ha provenienza** *(`[[L-NUMERI]]`)*, e ### **e' la ragione per cui serve
  la spazzata.** ### **Se il picco NON scende per
  primo, la lettura «costo dei modi corti» e' sbagliata.**
- **(f) LO STRUMENTO.** `csv/_stabilita_lineare.py` cosi' com'e'; ### **serve la legge** *(un termine
  nuovo in `leggi.yaml`, `prova: true`, il suo operatore, il suo posto nell'ordine)*. ### **Costo:**
  `~1`-`2` giorni la legge; il conto ### **una spazzata in `kappa`**, `~10` minuti per punto.
- **(g) CHE COSA ROMPEREBBE.** ### **L'impronta; `M-B1` no** *(a `kappa = 0` il passo resta)*;
  ### **`C1`-`C5` di strada `(d)` e `H_tot` vanno estesi** *(un termine in piu' in `G`)*;
  ### **`cs` diventa piu' liscio** *(il vuoto si irrigidisce)*: ### **`D4` andrebbe rifatto.**

---

### `C3` — **LA GRIGLIA A TRIANGOLI** *(voce `[[GRIGLIA-A-TRIANGOLI]]`, in `AGENDA`)*

- **(a) LA DEFINIZIONE.** ### **Non una legge: la connettivita'.** Una diagonale per quadrato,
  sempre nello stesso verso; ### **`6` vicini, `3` archi e `6` estremita' per nodo.** ### **Vanno
  ridefinite** la moneta, l'olonomia *(la plaquette diventa il triangolo)* e ### **ogni legge che
  legge le estremita'**, `S3` compresa.
- **(b) LA FAMIGLIA.** ### **Toglie il modo ALTERNATO** *(la bipartizione non c'e' piu': nessun modo
  `+1`/`-1` sui vicini)*, quindi ### **colpisce il PICCO a `(pi, pi)` per costruzione.** ### **Il
  BORDO** *(`(pi, 0)`)* **e la BANDA no**: ### **sulla zona esagonale ci sono altri punti di bordo**
  *(`K`, `M`)*, e ### **la banda segue `nu_S3`, non la bipartizione** *(`F4`)*. ### **Il limite e'
  gia' scritto nella voce.**
- **(c) LE CINQUE DOMANDE.**
  1. `A14`: sotto `(d)`.
  2. Gradino `(a)` lo screening; `(b)` ### **non si applica** *(non c'e' una «legge da togliere»: e'
     un'altra geometria)*.
  3. ### **Nessun numero nuovo** *(la diagonale e' topologia, non una lunghezza)*: ### **ne' costante,
     ne' toppa, ne' clip.** ### **MA SE SI SCEGLIE PERCHE' SPEGNE IL PICCO, e' una geometria scelta
     per compensare un difetto** -- ### **la voce lo dice: «come prova di cura SOLO se a regime
     vince il picco»**, e `594417f6` dice ### **che vince con `cs`, non con `S3` sola.**
  4. ### **Non tocca le leggi**; cambia ### **i vicini di tutte.**
  5. ### **Se la stabilita' venisse dalla geometria, sarebbe emergente rispetto a `S3`**, ###
     **imposta rispetto al reticolo.**
- **(d) `A14`.** ### **Da rifare per ogni legge** sulla nuova connettivita': la camminata a `6`
  vicini ### **deve restare unitaria**, e ### **ogni legge locale resta locale** *(il raggio non
  cambia)*.
- **(e) LA PREVISIONE.** ### **`R1`: il picco a `(pi, pi)` sparisce come tale**; il massimo va ###
  **al bordo della zona esagonale** con un `gamma` ### **fra quello di `(pi, 0)` di oggi** *(`0.48`)*
  ### **e quello della banda** *(`0.41`)*. ### **`R2`: la banda resta entro `~10%`** *(`~0.37`-`0.45`)*.
  ### **Se la banda di `R2` cambiasse molto, la banda dipenderebbe dalla geometria e non solo da
  `nu_S3`.**
- **(f) LO STRUMENTO.** ### **Nuovo:** la cella da `24` a `36` reali, ### **la zona esagonale**, la
  scena *(`scena_l2` e `corrente.toro` a `6` vicini)*, ### **la moneta e l'olonomia nuove.** ###
  **Costo: settimane**, e ### **e' gia' una voce con la sua condizione di apertura.**
- **(g) CHE COSA ROMPEREBBE.** ### **Quasi tutto cio' che e' verificato:** `M-B1` *(il motore vecchio e'
  quadrato)*, ### **le `7` leggi** *(ridefinite)*, l'impronta, ### **`C1`-`C5` di strada `(d)`**, ###
  **tutti i referti di `L2`** *(da rifare)*.

---

### `C4` — **NESSUNA CURA DI `S3`: LA CURA NELLA CAMMINATA** *(se `D0` dice risonanza)*

- **(a) LA DEFINIZIONE.** ### **Cambiare la dispersione della camminata ai `k` grandi** senza toccare
  `S3`: ### **una moneta che dia «massa» ai modi del bordo della zona**, come ### **il termine di
  Wilson da' massa ai doppioni** dei fermioni sul reticolo *(un termine di hop che pesa diversamente
  i modi con `k` vicino a `pi`)*. ### **Tocca `CAMM-MONETA-SPIN`, `CAMM-GROVER` o
  `CAMM-SPOSTAMENTO`.**
- **(b) LA FAMIGLIA.** ### **Quella RISONANTE, se `D0` tiene:** spostando `omega_j(k)` ai `k` grandi
  ### **la condizione di risonanza** `2 omega(0) - omega(k) - omega(-k) = nu_S3` ### **cade a `k`
  diversi o sparisce.** ### **Se `D0` cade, `C4` non ha ragione.**
- **(c) LE CINQUE DOMANDE.**
  1. `A14`: sotto `(d)`.
  2. Gradino `(a)`; `(b)` col termine tolto.
  3. ### **Un numero: il peso del termine di Wilson** *(`r` nella letteratura)*. ### **Toppa, se
     scelto per stonare la risonanza; costante di accoppiamento, se derivato** *(per esempio dal
     limite continuo della camminata, dove i doppioni devono sparire)*.
  4. ### **Non tocca `rho` ne' `cs`**; ### **tocca il TEMPO PROPRIO della camminata** *(la
     dispersione)*.
  5. ### **Il rischio piu' grande:** ### **la camminata e' il cuore dell'era `2`**, e cambiarla per
     curare una legge che le sta accanto ### **sposta il difetto invece di capirlo.**
- **(d) `A14`.** ### **Si'**, se la nuova moneta e' unitaria e locale *(un pezzo unitario come oggi)*.
- **(e) LA PREVISIONE.** Se `D0` tiene: ### **il massimo di `R2` si sposta col termine**, e ### **la
  banda si spegne quando la risonanza esce dalla zona**; ### **il picco di `R1` si spegne solo se la
  sua crescita e' anch'essa risonante.** Se `D0` cade: ### **cambio di `gamma` piccolo** *(`< 10%`)*.
- **(f) LO STRUMENTO.** `csv/_stabilita_lineare.py` cosi' com'e', ### **e il caso che deve fallire
  cambia** *(la camminata sola NUOVA deve restare a modulo `1`)*. ### **Serve la legge** *(una moneta
  in tabella)*. ### **Costo:** `~1`-`2` giorni.
- **(g) CHE COSA ROMPEREBBE.** ### **`M-B1`** *(ad angolo `pi` il passo riproduce al bit il motore
  vecchio: con una moneta nuova NO)*, ### **la `C`-simmetria e `PTheta`** *(da rifare)*, ### **`L1`,
  che e' chiuso**, ### **tutti i referti della camminata.** ### **E' la cura che rompe di piu' fra
  quelle che lasciano `S3` intatta.**

---

### `C5` — **`cs` LETTO DA `Lambda` MEDIATA** *(CURA MIA, dichiarata tale)*

- **Perche' la propongo:** il picco di `R1` ### **lo alzano `cs` e la fase**: `(pi, pi)` va da
  `0.351` *(`R2`, `S3` sola)* a `0.545` *(`R1`)*; e ### **senza `CAMM-FASE-VUOTO`, con `cs` acceso,
  il massimo torna `0.378` a `0.45 pi`** *(`c38367db`)*. ### **Il canale che porta la crescita a
  `(pi, pi)` passa per `cs`.**
- **(a) LA DEFINIZIONE.** `cs_i = Lambda_bar_i / (Lambda_bar_i + Lambda_c)` con `Lambda_bar = W
  Lambda` *(lo stesso filtro di `C1`)*, e ### **la fase sul vuoto coerente** *(`CAMM-FASE-VUOTO` e'
  costruita da `cs'(Lambda)`: con `cs` mediato ### **cambia anche lei**, e va ### **RIDERIVATA**,
  non adattata)*.
- **(b) LA FAMIGLIA.** ### **Solo il PICCO di `R1`** *(e il bordo, se passa per `cs`)*; ### **`R2`
  non lo vede** *(`cs` e' spento)*. ### **Quindi da sola NON basta**: la banda di `R2` resta.
- **(c) LE CINQUE DOMANDE.** 3: ### **i pesi del filtro** *(come `C1`)*; ### **toppa se scelti per
  stabilizzare.** 4: ### **tocca `c_s`** -- ### **il cuore di `L2`** *(la «gravita'» e' la non
  uniformita' di `cs`)*: ### **un `cs` mediato e' una gravita' a raggio `1`**, e ### **cambia la
  forma che `D4` ha misurato.** 5: imposta, se per stabilizzare.
- **(d) `A14`.** ### **Da verificare:** `cs` entra nei pesi del passo *(il tempo proprio)*, e la
  conservazione di `G` e' ### **quella di strada `(d)`** *(`C1` di strada `(d)`, pendenza `2.091`)*:
  ### **va rifatta.**
- **(e) LA PREVISIONE.** `R1` a `(pi, pi)` ### **scende verso `0.35`-`0.38`** *(il valore senza il
  canale di `cs`)*; ### **`R2` invariato** *(e' il controllo: deve restare `0.407` al bit della
  banda)*.
- **(f) LO STRUMENTO.** `csv/_stabilita_lineare.py` cosi' com'e'; ### **serve la forma di `cs` nuova
  e la fase ridotta.** ### **Costo:** `~1`-`2` giorni *(la fase va riderivata)*.
- **(g) CHE COSA ROMPEREBBE.** ### **`C1`-`C5` di strada `(d)`** *(la fase cambia)*, ### **`D1`-`D4`**
  *(la forma di `cs`)*, l'impronta. `M-B1` no.

---

## 4. IL CONFRONTO

| cura | il PICCO `(pi, pi)` | il BORDO `(pi, 0)` | la BANDA `~0.5 pi` | tipo *(domanda `3`)* | il numero nuovo | lo strumento | il costo | che cosa rompe |
|---|---|---|---|---|---|---|---|---|
| `C1` `S3` sui vicini | ### **spento** *(col binomiale)* | `1/4` | `9/16` | toppa / costante | i pesi `w0`, `w1` | quello di oggi + una legge | legge `~1` g; conto `~10` min | impronta, strada `(d)`, `H_tot` |
| `C2` costo dei modi corti | ### **primo a scendere** | secondo | ultimo | toppa / costante *(la rigidita' `(e)`)* | `kappa` | quello di oggi + una legge | `~1`-`2` g; spazzata | impronta, strada `(d)`, `D4` |
| `C3` triangoli | ### **tolto per costruzione** | no | no | ### **nessun numero** | nessuno | ### **NUOVO** *(`36` reali)* | settimane | ### **quasi tutto** |
| `C4` la camminata | se risonante | se risonante | ### **se `D0` tiene** | toppa / costante | `r` *(Wilson)* | quello di oggi + una moneta | `~1`-`2` g | ### **`M-B1`, `L1`, `PTheta`** |
| `C5` *(mia)* `cs` mediato | ### **scende** *(solo `R1`)* | forse | ### **no** | toppa / costante | i pesi | quello di oggi + `cs` e la fase | `~1`-`2` g | strada `(d)`, `D1`-`D4` |

### **I CRITERI DI SCREENING, PROPOSTI** *(non fissati: li approva Luca)*

1. ### **Una cura passa lo screening se porta `gamma <= 0` su OGNI `k`** a lato `32`, con la base
   proiettata e `N dtau 100` *(`594417f6`)*, ### **entro il pavimento del metodo** *(`4.4e-8`,
   `c38367db`)* ### **o la banda di linearita'** *(`1e-3` del massimo di oggi)*.
2. ### **Senza toccare la camminata sola:** `braccio_c2_esatto` ### **AL BIT come oggi** *(tranne `C4`,
   che la cambia per definizione: per lei, ### **modulo `1` entro `N * 64` ulp**)*.
3. ### **A lato `32` e `64` lo stesso esito** *(il verdetto `A` non deve tornare: la cura non deve
   essere un altro difetto di reticolo)*.
4. ### **Il numero nuovo dichiarato col suo tipo** *(domanda `3`)*: ### **una toppa passa lo screening
   ma NON la promozione** *(`doc/COMPONENTI_PROMOSSE.md`: «derivata, non tarata»)*.
5. ### **Uno screening parziale** *(una famiglia spenta, l'altra no)* ### **si riporta come tale**, e
   ### **non e' una cura.**

---

## 5. LE DOMANDE PER LUCA *(una alla volta, nella relazione)*

1. ### **Fare `D0` prima delle cure?** *(costo: `~5` minuti di conto e uno strumento piccolo; dice
   se le cure che spostano i ritmi hanno una ragione)*
2. *(dopo la prima)* Quali criteri di screening approvare.
3. *(dopo la seconda)* Quale cura provare per prima, e ### **con quale origine del suo numero.**
