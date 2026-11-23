# IL FONDO GIUSTO (alpha < 0 AL FONDO DELLA BANDA DELLA MATERIA) E L'ABLAZIONE DELLO SPETTRO *(Luca, 2026-11-23, [M1658]; scritta PRIMA del codice e dei numeri, dalle `17:03` da `date`)* [[PROGETTO-MITOSI]]

## 0. L'ERRORE DEL GUARDIANO, DICHIARATO *(dal mandato)*

- **n.240:** «il fondo della banda» letto come il minimo dello spettro *(la piatta a `-0.4827`)*: il torneo semino' `lambda < 0` alla cima e sulla piatta, **mai al fondo della banda della materia** *(`+0.245`)*.

## 1. COSA DICE GIA' `spettro_gap_v2.txt` *(letto alle `17:02`, PRIMA di ogni codice)*

- **La banda della materia sono DUE bande** *(«la penultima» e «l'ultima»)*: **tutte e due hanno il minimo `+0.2453383` a `k = (32, 32)/96`** e il massimo `+0.4767266` a Gamma *(la cima, molteplicita' `2`)*. **`(32, 32)/96 = (B0 + B1)/3`: e' il punto K** *(l'angolo della zona di Brillouin)*, **non Gamma.**
- ### **QUINDI, DETTO PRIMA:** al fondo le due bande **si toccano** *(molteplicita' almeno `2`)*. **Se si toccano a CONO** *(`E - E_K ~ |delta k|`, un punto di Dirac)* **la curvatura `d2E/dk2` non e' definita** e K2 *(«la curvatura positiva»)* non si chiude come scritto: lo dico, e K2 FALLISCE. **Se si toccano con una curvatura** *(`~ delta k^2`)*, K2 si legge col suo segno.
- **Il gap sotto:** da `+0.011870` a `+0.245338` *(largo `0.233468`)*; il bersaglio del mandato `~+0.095` ci sta dentro.

## 2. 1a: LA LETTURA, LE DEFINIZIONI *(fissate qui)*

- `A(k)` dalle righe di `spettro_gap.bande` *(la risposta lineare di un tick sul vuoto fresco della scena di chi, `12` impulsi `+-`, il tick U con `cs = s`: come `torneo_fondo_v2.py`)*. **I punti:** K `(B0 + B1)/3` e K' `(2 B0 + B1)/3`.
- **La molteplicita':** le quasi-energie entro `1e-9` da `+0.2453383` *(e il caso noto: il minimo uguale a quello di `spettro_gap_v2` entro `1e-6`)*.
- **Cono o curvatura:** lungo `B0`, `B1` e la loro bisettrice, a `delta = 0.0025, 0.005, 0.01, 0.02` *(in unita' di `|B0|`)*: le quasi-energie della coppia *(le due piu' vicine a `+0.2453` nella finestra `[0.20, 0.30]`)*; **l'esponente** `p = log2((E(2 delta) - E_K)/(E(delta) - E_K))` *(`p ~ 1`: CONO; `p ~ 2`: CURVATURA, e allora `d2E/dk2 = 2 (E(delta) - E_K)/delta^2`)*. **Il criterio:** `|p - 2| < 0.2` per la curvatura, `|p - 1| < 0.2` per il cono, ai due `delta` piu' piccoli.
- **Lo stampo nel sottospazio di K** *(come `torneo_fondo_v2`: il mattone di `caduta_libera.prepara`, i nodi con `rho > 1e-3 rho_max`, la frazione pesata di `|psi(x) e^{-i k.d}|^2` nel sottospazio)*; **per confronto la stessa frazione nel sottospazio della CIMA a Gamma.**
- **Il doppietto di spin:** il residuo sotto la stessa SU(2) casuale *(il seme `20261122`)*.

## 3. I CRITERI *(copiati)* E LE PREVISIONI

- **K1** casi noti: 2a senza ablazione al bit; 1b L0 non regge. **K2** 1a: la curvatura al fondo `+0.245` POSITIVA e non degenere *(molteplicita' `<= 2`)*. **K3** 1b: `lambda = -1` al fondo regge `3000` tick *(K-T v2)* con `omega` nel gap. **K4** 1c: `m*` positiva; NATURA se orologio come `N` e caduta VERSO in almeno un collegamento. **K5** 2a: la piatta sparisce con (iii) = «e' Grover»; la cima a massa negativa resta in tutte = «e' il cammino».
- **DEL GUARDIANO** *(copiate)*: P1 K2 `60%`. P2 K3 regge `45%`; se regge `m* > 0` `85%`, NATURA in V2 `55%`, TOPPA per Eotvos `50%`. P3 la piatta di Grover `70%`; la cima negativa resta tranne (iii) `55%`.
- **LE MIE** *(prima dei numeri)*: **la molteplicita' al fondo e' `2` `90%`** *(il testo di `spettro_gap_v2`)*; **le due bande si toccano a CONO `55%`** *(un punto K di un reticolo a favo con due bande che si toccano e' il posto classico di un cono di Dirac)*; **lo stampo nel sottospazio di K pesa meno del `1%` `80%`** *(il mattone e' fermo: e' a Gamma)*.

## 4. LA PARTE 2 *(l'ablazione)*: la sua sezione si scrive prima del suo codice, dopo 1a.

## 2-bis. 1b: LA SEMINA AL FONDO *(scritta dopo 1a e PRIMA del codice di 1b)*

- **1a ha detto** *(`fondo_materia.txt`, `a8116845`)*: il fondo a K `(B0 + B1)/3`, `E = +0.2453383`, molteplicita' `2`, **curvatura positiva `+0.0560`** *(isotropa)*: K2 passa, **1b si fa.**
- **L'onda di Bloch** *(dalle righe: `A(k) = somma_x R(x) e^{-i k.d(x)}`, quindi `psi'(x) = somma_z R(z) psi(x - z)`)*: **`v e^{+i k.x}`**. **Le semine** *(`torneo_tenuta_v2.corsa` riga per riga, la scena di `caduta_libera.prepara`)*:
  - **`stampo_K`:** `psi_h(x) <- psi_cima(x) e^{+i K.d(x)}` *(`d` lo scarto dal centro del mattone; `rho` non cambia: lo stesso mattone con la portante a K)*;
  - **`proiezione_K`:** `psi(x) <- Q_K Q_K^dag psi_cima(x) e^{+i K.d(x)}` nodo per nodo, poi uno scalare per la norma *(`Q_K` = la base QR del sottospazio a `+0.2453383` di `A(K)`)*: **un oggetto nuovo**, non il mattone spostato.
- **Le corse, `3000` tick:** **L-1 `stampo_K`**, **L-1 `proiezione_K`**, ### **L0 `stampo_K` e L0 `proiezione_K`** *(il mandato: «L0 alla stessa semina»; non dice quale: **tutte e due**, una corsa in piu', dichiarata)*.
- **I casi noti del codice** *(in memoria, prima delle corse)*: la semina `cima` con L-1 ridà `M1631/tenuta_v2/L-1_cima/stato_000250` **al bit**; la proiezione a Gamma *(`k = 0`, la quasi-energia piu' bassa: la somma `R[sup].sum(axis=0)` di `torneo_tenuta_v2`)* ridà `L-1_proiezione_Gamma/stato_000000` **al bit**; **DEVE FALLIRE:** `stampo_K` a `k 0` diverso dalla cima in `psi_h`.
- **La lettura** *(K-T v2, `torneo_kt_v2`)*: **REGGE** se `w(3000)/w(1500)` in `[0.7, 1.3]` e un pezzo solo a `k 3000`; **K3:** regge **e** `omega` *(la media su `[2500, 3000]`, `-arg vdot`)* **nel gap `(0.011870, 0.245338)`**. **K1:** L0 NON regge *(con la stessa semina della L-1 che regge; se nessuna regge, il controllo e' a vuoto: lo dico)*.
- **LE MIE PREVISIONI** *(prima dei numeri)*: `stampo_K` regge `25%` *(la polarizzazione di Gamma pesa solo `~25%` nel sottospazio di K: tre quarti in altre bande)*; `proiezione_K` regge `40%`; `omega` nel gap se regge `60%`.

## 4. LA PARTE 2: L'ABLAZIONE DELLO SPETTRO *(scritta PRIMA del suo codice, `17:34` da `date`)*

- **Il metodo e' quello di `spettro_gap_v2`** *(la risposta lineare di UN tick sul vuoto fresco della scena di chi, `A(k)` sulla griglia `96 x 96`)*, **non quello di `_bande_piatte.py`** *(un'altra scena, la FFT su `L x L`: non potrebbe ridare `spettro_gap_v2` al bit, che e' il caso noto del mandato)*. **Il tick:** `caduta_segno_v2.tick_var` riga per riga *(`cs = s`, segno `0`)* **con la lista `salta` di `percorri_tick`** *(che `tick_var` passa vuota)* **e, per (ii), una sostituzione IN MEMORIA** *(il nucleo non si tocca: come `fh_suite.con_forma`)*.
- **I pezzi** *(`composizione.ORDINE`, la prima meta')*: `CAMM-MATERIA-VUOTO` *(il legame)*, `CAMM-FASE-VUOTO`, `CAMM-MONETA-SPIN`, `CAMM-GROVER`, `CAMM-SPOSTAMENTO`, `CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`; poi la seconda meta' a specchio.
- **Le ablazioni, una alla volta:**
  - **(0) nessuna:** il caso noto, `E(k)` = `spettro.npz` di `spettro_gap_v2` **AL BIT** *(le stesse operazioni, nello stesso ordine)*;
  - **(i) la moneta di spin -> l'identita':** `salta = (CAMM-MONETA-SPIN,)`;
  - **(ii) lo zero simmetrico -> lo zero di prima:** `flussi_parziali.grover`, `hop_psi`, `hop_phi` **senza il fattore `conj(z)`** *(sostituite in memoria: le stesse righe meno l'ultima)*. **Prima dei numeri:** `z_nodo` e `z_arco` dipendono solo da `s_nodo`, `s_arco`, **uniformi qui**: **(ii) e' uno spostamento RIGIDO dello spettro** *(curvature e piatte uguali)*: **e' una previsione che si verifica;**
  - **(iii) Grover -> la moneta di Fourier a sei vie:** ### **NON DEFINITA senza una scelta, e la scelta e' di Luca.** Grover entra come **mezzo passo `e^{i theta (I - 2P)/2}`**: un generatore HERMITIANO *(la riflessione `I - 2P`, `G^2 = I`)*. **La matrice di Fourier `F` non e' hermitiana** *(`F^4 = I`)*: il mezzo passo `F^{theta/pi}` vuole un ramo del logaritmo; `(F + F^dag)/2` e' hermitiana ma non e' `F`. **Tre strade:** (a) il ramo principale di `log F`; (b) il passo intero `F` una volta per tick, senza `theta`; (c) la parte hermitiana. **Nessuna e' derivata: e' una manopola (A1). (iii) NON si fa; FERMO su (iii), la domanda a Luca;**
  - **(iv) il legame col vuoto spento:** `salta = (CAMM-MATERIA-VUOTO,)`; **e, separata, `CAMM-FASE-VUOTO`** *(il ritmo del vuoto: non e' il legame ma tocca la fase; una riga in piu', dichiarata)*;
  - **(v) il reticolo quadrato:** ### **NON si fa:** `triangolo_chi_v4.scena` costruisce solo il favo; un quadrato vorrebbe una scena nuova del nucleo *(e [[DECISIONE-SOLO-TRIANGOLI]] lo ammette solo come controllo di servizio)*: **lo dico.**
- **Le letture per ablazione:** le `12` bande ordinate per valore *(il minimo, il massimo, la larghezza)*; **«piatta»** se la larghezza `< 1e-6`; **la cima della materia:** a Gamma, l'autovettore con la sovrapposizione massima col `q` della cima senza ablazione *(stampata)*, la sua `E` e `d2E/dk2` lungo `B0`, `B1` *(il seguito di `spettro_gap.bande`, `DK = 0.02`)*; **il fondo a K** allo stesso modo *(la sovrapposizione col sottospazio del fondo senza ablazione)*.
- **K5 come scritto:** «la piatta sparisce con (iii)» **non si giudica** *(iii non c'e')*; **«la cima a massa negativa resta in tutte»** si giudica su (i), (ii), (iv).
- **LE MIE PREVISIONI** *(prima dei numeri)*: (ii) rigido entro `1e-12` `90%`; con (i) la piatta resta `70%` *(la piatta e' del favo e di Grover, non dello spin)*; con (iv) la cima resta a massa negativa `55%`.

## 2-ter. [v2] DI [M1658]: IL FIT QUADRATICO E IL FIT LINEARE A K *(Luca, la versione 2 del mandato; scritta PRIMA del codice, `17:56` da `date`)*

- **1a e' gia' fatta** *(`a8116845`: l'esponente `p = 2.000` ai due `delta` piu' piccoli: CURVATURA)*; **la v2 aggiunge una riga**, e la faccio come addendum: `doc/referti_l2/fondo_K.py` -> `fondo_K.txt`.
- **Una premessa della v2 che non torna:** «il fit di Dirac a K: il basso `c -0.003`, l'errore `0.5`, la curvatura `+3.9e-5`» -- **in `spettro_gap_v2.txt` quel fit e' A GAMMA** *(«(iv) i gap attorno alla banda della materia, a Gamma, `|k| < 0.3`»)*, sul ramo basso del gap sotto la materia, **non al fondo a K.** Lo dico, e la lettura qui e' a K.
- **Le definizioni:** lungo `B0`, `B1` *(versori)*, `20` punti `delta` in `(0, 0.15]` *(`|k - k_K|` assoluto)*; per ciascuno dei due rami della coppia *(le due quasi-energie nella finestra `[0.20, 0.30]`)*: **(Q)** `E - E_K = a delta^2` e **(L)** `E - E_K = v delta`, minimi quadrati senza intercetta; l'errore di `a` e `v` dai residui; **«regge»** se il residuo relativo massimo `|E - fit|/(E - E_K)` e' `< 5%`. **Il verdetto:** **FONDO CURVO** se (Q) regge con `a > 0` su tutti e due i rami e i due assi e la molteplicita' `<= 2`; **CONO** se regge (L) con `v > 0` e (Q) no; **PIATTO** se `|E - E_K| < 1e-6` su tutto l'intervallo.
- **LE PREVISIONI** *(copiate, [v2])*: P1 FONDO CURVO `35%`, CONO `35%`, PIATTO `30%`. **La mia** *(dopo 1a, quindi non cieca: lo dico)*: FONDO CURVO `90%`.

## 4-bis. (iii) GROVER -> FOURIER, COL VIA DI LUCA *(Luca: «SI', in memoria, con lo stesso metodo; (v) NO»; scritta PRIMA del codice, `19:14` da `date`)*

- **Luca non sceglie fra (a), (b), (c)** *(sez. 4)*. **La mia lettura di «lo stesso metodo», dichiarata:** Grover nel nucleo e' un FLUSSO, `G(theta) = P_u + e^{i theta}(I - P_u) = e^{i theta (I - P_u)}`, che a `theta = pi` e' la riflessione `2 P_u - I`; **l'analogo con lo stesso schema e' (a):** `F(theta) = e^{i theta H_F/pi}`, `H_F = -i log F` *(il ramo principale: `F` unitaria, `H_F` hermitiana)*, **che a `theta = pi` e' ESATTAMENTE `F`.** Il pezzo: `F(theta/2)` due volte, poi lo zero simmetrico `conj(z)` *(come `flussi_parziali.grover`)*. **(b) e (c) NON si fanno.**
- **`F_ab = omega^{ab}/sqrt 6`**, `omega = e^{2 pi i/6}`, `a, b` = le sei direzioni del favo attorno al nodo **in senso antiorario a partire da `A1`** *(una CONVENZIONE: l'origine degli indici cambia `F` per fasi diagonali; lo dico)*; **su ogni nodo, l'identita' sullo spin.** Solo il Grover della MATERIA *(`CAMM-GROVER`)*: quello del vuoto non tocca lo spettro lineare di `psi` *(come il legame, sez. 4)*.
- **I controlli:** le sei estremita' di ogni nodo hanno UNA direzione ciascuna *(il toro perfetto: l'assert)*; **a `theta = pi` il pezzo e' `F` entro `1e-12`**; `|lambda| = 1` a Gamma *(unitario)*.
- **Le letture** come sez. 4 *(le bande, le piatte, la coppia, la cima e la sua curvatura, il fondo a K)*. **K5:** «la piatta sparisce con (iii)» = «e' Grover».
- **LE MIE PREVISIONI** *(prima dei numeri)*: le piatte spariscono `60%`; la cima resta a massa negativa `40%`.
