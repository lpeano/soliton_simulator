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

## 2-quater. 1c: L'OGGETTO AL FONDO A K, MISURATO COME F0 *(1b ha retto: `8fb80c94`; scritta PRIMA del codice)*

- **L'oggetto:** `M1658/tenuta/L-1_proiezione_K/stato_003000.npz` *(la forma L-1; `omega +0.0940` nel gap)*, caricato con `fondo_suite_v2.carica` *(in memoria `stato_di` e `FORMA` di quel modulo puntati su questo file: il modulo non si tocca)*. **Il ciclo:** `caduta_segno_v2.tick_var` riga per riga di `fondo_suite_v2._tick_loop`, col `segno` passato *(quello del modulo e' fisso a `0`)*, la forma `L-1` del nucleo.
- **Il calcio** *(come `fondo_suite_v2.calcio`)*: `k 0` e `k 0.010` lungo `A1`, `1000` tick, il baricentro ogni `10`; **`m* = 0.010/(v - v0)`** *(`massa_calcio.velocita`, il fit da `k 200`)*. **K4: `m*` POSITIVA.**
- **L'orologio** *(come `legge_zeri`)*: `N` uniforme `0.9965`, `1`, `1.0035`, in V2 *(`cs_N`)* e in V3 *(il segno `+1`)*, `500` tick; a ogni tick `omega_psi` *(`-arg vdot` su tutto)* e **`omega_phi` del vuoto lontano** *(i mezzi archi coi due capi a `r > 60` dal centro dell'oggetto)*; **`Delta = omega_psi - omega_phi`** *(lo zero = il vuoto lontano)*; **`d ln Delta / dN`** dalla differenza centrata. **«L'orologio come `N`»** se `d ln Delta/dN` in **`[0.98, 1.02]`** *(Luca, [M2145], `21:45`: «la differenza V2/V3 e' il 2%: con +-10% non si distingue»; la soglia di prima, `[0.9, 1.1]`, era mia; cambiata PRIMA che le corse partissero)*.
- **La caduta** *(come `fondo_suite_v2.caduta`)*: il gradiente di `caduta_libera.campo_N(+1)` *(lo stesso `A`)*, `2000` tick, **V2, V3 e V0** *(`N = 1`: il riferimento)*; `y(k)` ogni `10`; **`a` dal fit `y0 + v k + a k^2/2` su `k >= 200`** *(il `sigma` dai residui)*; **VERSO se `a - a(V0) > 0`** *(verso `N` piu' basso: la convenzione di [M0908])*. ### **K4 NATURA** se in almeno un collegamento l'orologio va come `N` E la caduta e' VERSO.
- **Le corse:** `10` *(il calcio 2; l'orologio 5: `N = 1` in comune, V2 e V3 a `0.9965` e `1.0035` -- V2 e V3 con `N = 1` sono lo stesso tick al bit, CN2 di [M1640]; la caduta 3)*, in `coda_m1446` a priorita' `0` *(il mandato: «in coda a priorita' 0»)*, **dal solo lanciatore** *([M1944])*.
- **La tabella del giudizio contro F0:** S1 *(il segno della massa)*, S3, S4 non *(Eotvos: non fatta, una scala sola)*, S6 *(l'orologio e la caduta)*.
- **LE PREVISIONI** *(copiate)*: P2: `m* > 0` `85%`; NATURA in V2 `55%`; TOPPA per Eotvos `50%`. **Le mie:** `m* > 0` `90%` *(la curvatura `+0.056` al fondo)*; NATURA in almeno un collegamento `35%`.

## 2-quinquies. [M2221] LA FORMA DELL'OGGETTO AL FONDO A K *(Luca, 22:21; solo lettura; scritta PRIMA del codice, `22:23` da `date`)*

- **I tre stati a `k 3000`:** (a) `M1658/tenuta/L-1_proiezione_K/stato_003000.npz`; (b) `L0_proiezione_K/stato_003000.npz`; (c) **`M1631/tenuta_v2/L-1_cima/stato_003000.npz`** *(esiste a `k 3000` esatto)*. La scena `triangolo_chi_v4.scena` per il grafo e le posizioni.
- **Il baricentro:** `toro.centro(rho)` *(periodico)*, poi gli scarti `toro.scarti` e la media pesata con `rho` *(il baricentro raffinato)*; `r`, `theta = atan2(y, x)` *(la convenzione di `segni_vortice.py`)* attorno a lui. **Gli anelli** `[4, 8)`, `[8, 12)`, `[12, 16)`. **`S_m = somma rho e^{-i m theta}`**, `|S_m| / somma rho`, l'orientamento `-arg(S_m)/m` in gradi, per `m = 3` e `m = 6`.
- **Il caso noto:** sull'anello, **`rho = 1 + cos(6 theta)`** *(con `cos(6 theta)` da sola la somma e' zero e il rapporto non e' definito: il `0.5` del mandato e' questa)* -> `|S_6|/somma` `0.5`, l'orientamento `0`; **la tolleranza, fissata qui:** entro il fondo del favo di quell'anello piu' `0.01` *(il reticolo aggiunge la sua impronta)*. **Il controllo negativo: `rho = 1`** su tutti i nodi dell'anello: `|S_3|`, `|S_6|` **del favo stesso**, per anello: la soglia sotto cui c'e' solo il reticolo.
- **Le immagini** *(tre file)*: (a) e (b) a scala lineare sul massimo di CIASCUNO; (a) e (b) in `log10 rho` su `4` decadi; (c) lineare e logaritmica. Una finestra di raggio `30` attorno al baricentro.

## 2-sexies. [M2305] LA NOTTE DEL FONDO A K: S3 (LA LEGGE), LE TENUTE PER S4 E LA ROBUSTEZZA *(Luca, `23:05`; scritta PRIMA del codice, `23:08` da `date`; i criteri numerici sono miei, dichiarati qui)*

- **S3, la legge `a = -grad omega / m*`** *(V2, sull'oggetto `L-1_proiezione_K/stato_003000`)*: la caduta col gradiente di `caduta_libera.campo_N` a **`x0.5` e `x2`** dell'ampiezza `A` di 1c *(`2000` tick)*; con il `x1` di 1c *(`caduta_V2`, `+6.02e-7`)* e **V0 di 1c** *(`+2.74e-8`)* tre punti. **`grad omega`, la mia definizione:** al centro dell'oggetto *(`y = y_c`)* `dN/dy = -kappa A (2 pi / L_y)` *(da `campo_N`: `chi = A sin(2 pi (y - y_c)/L_y)`, `N = e^{-kappa chi}`, `N(y_c) = 1`)*; **`d omega / dN` = la pendenza dell'orologio V2 di 1c** *(`(Delta(1.0035) - Delta(0.9965))/0.007`, `Delta` contato dal vuoto lontano)*; **`grad omega = (d omega/dN)(dN/dy)`**. **`K_i = (a_i - a(V0)) / (-grad omega_i / m*)`**, `m* = +18.916` *(il calcio di 1c)*: **il segno della legge** *(`a = -grad omega / m*`)*: `K = +1` vuol dire la legge col suo segno. **Il criterio** *(Luca)*: la legge vale se lo scarto/la media dei tre `K_i` `< 10%` e `|media - 1| < 0.15`.
- **Le tenute, nuove semine al fondo a K per proiezione** *(`tenuta_fondo.semina` riga per riga; L-1, `3000` tick, K-T v2, `omega` nel gap)*:
  - **(t1) ampiezza `x0.5`, (t2) ampiezza `x2`:** `psi` della semina di 1b moltiplicato per `0.5` e `2` **dopo** la proiezione *(la norma `x0.25` e `x4`: «ampiezza» la leggo alla lettera, come l'ampiezza di `psi`; dichiarato -- l'Eotvos di ieri usava la NORMA `x0.8`, `x1.2`)*;
  - **(t3) larghezza `x0.7`, (t4) larghezza `x1.4`:** lo stampo *(il mattone di `caduta_libera.prepara`, prima della portante e della proiezione)* **ricampionato** `psi_nuovo(x) = psi(nodo piu' vicino a c + (x - c)/s)`, `s = 0.7, 1.4`, **poi riportato alla norma di 1b**, poi la portante a K e la proiezione come 1b *(il profilo cambia, la massa no)*;
  - **(t5) la taglia L 162: NON SI FA** -- ### **la scena di 1b E' gia' L 162** *(`triangolo_chi_v4.scena`: `L 162`, `n 26244`)*: **t5 coinciderebbe con 1b.** Dichiarato e saltato.
  - **i controlli negativi:** L0 per t1 e t2 *(la stessa semina)*.
- **Il caso noto delle semine** *(prima delle corse, in memoria)*: la semina con ampiezza `1` e larghezza `1` a `k 0` = `L-1_proiezione_K/stato_000000` **AL BIT**.
- **Le corse: `8`** *(2 S3 a priorita' `0`; 4 tenute e 2 L0 a priorita' `1`)*, dal solo lanciatore. **E le schede di [M1751] in coda a priorita' `2`** *(due voci, cinque nascite ciascuna)*.
- **I criteri delle tenute** *(come 1b)*: `w(3000)/w(1500)` in `[0.7, 1.3]`, un pezzo, `omega` nel gap; L0 non regge. **Nessun giudizio nella notte.**
- ### **LA CONVENZIONE DELLA CIMA** *(DECISIONE DI LUCA [M0118-00], `01:25`; annotazione `01:24` da `date` -- avevo scritto `01:28` a stima, corretto prima del commit: questa sezione non si riscrive, si annota)*: **«lo zero dal vuoto lontano era una scelta di CC; la convenzione della sagoma e' quella della cima».** **Qui sopra** `d omega/dN` era `d Delta/dN`, `Delta = omega_psi - omega_phi(lontano)` *(lo zero dal vuoto lontano: una scelta MIA)*; **la convenzione della sagoma** *(`legge_caduta_v2`, `K_th = omega_psi(N1)/(|m*| c^2)`)* **prende `omega_psi(N1)` dallo zero del tick**: `grad omega = omega_psi(N1) dN/dy`. **Le K nelle due convenzioni, una accanto all'altra:** `fondo_s3_v2.py` *(S3, `x0.5`, `x1`, `x2`)* e `eotvos_fondo_v2.py` *(1c e a2)*, sull'intera `[200, 2000]` e sulle finestre di `600`; **`omega_psi(N1)` = la media di `omega` dell'orologio V2 di 1c a `N = 1`** *(`M1658/c1/orologio_V2_N1.0000`, `500` tick)*, **lo stesso per a2** *(come il `grad omega` di S3; accanto, per a2, l'`omega` del suo calcio a `k 0`: mia aggiunta, dichiarata)*. **eta non cambia** *(e' un rapporto di `a`, non di K)*. **I referti vecchi restano:** la v2 si aggiunge sotto. **`k_forma.py` (in coda per [M0118-02]) e' nella convenzione vecchia:** la sua lettura v2 stampera' le due.

## 2-septies. [M0037] K = 0.129: LA CADUTA PER PARTI E L'EOTVOS CON 1 E 4 *(Luca, `00:37`; scritta PRIMA del codice, `00:38` da `date`)*

- ### **[M0037-01] NON SI FA come scritto:** **la caduta di 1c NON ha stati salvati** -- `fondo_1c.caduta` scrive solo `serie.json` *(il baricentro ogni `10` tick)*: in `M1658/c1/caduta_V2/` e `caduta_V0/` c'e' solo quello. **Senza `psi` non si scompone in `psi_K` e `psi_R`.** **Servirebbe una corsa nuova** *(la caduta V2 `x1` e la V0 con gli stati ogni `250`)*: **la decisione e' di Luca.** FERMO su 01.
- **[M0037-02] l'Eotvos con le masse `1` e `4`:** `doc/referti_l2/eotvos_fondo.py` **chiama `fondo_1c.caduta` e `fondo_1c.calcio` cosi' come sono**, con **due costanti di quel modulo cambiate IN MEMORIA prima di tutto:** `fondo_1c.OGGETTO` = `M1658/tenuta_v2/L-1_a2.0_l1.0/stato_003000.npz` *(l'oggetto a2, che regge)* -- `fondo_1c.avvia` mette `fondo_suite_v2.stato_di` su `lambda: OGGETTO`, che si legge al momento della chiamata -- e `fondo_1c.BASE` = `M1658/c1_a2` *(le uscite in una cartella nuova)*. **Le corse:** (e1) la caduta V2 col gradiente `x1` di 1c; (e2) la sua V0; (e3) il calcio `k 0.010`; ### **(e3b) il calcio `k 0`, in piu'** *(`m* = 0.010/(v - v0)` vuole `v0`: dichiarato)*. **4 corse**, priorita' `0`, dal solo lanciatore.
- **[M0037-03] la lettura:** `K(a2) = (a - a(V0)) / (-grad omega / m*(a2))` con `grad omega` di S3 *(`d omega/dN` dell'orologio V2 di 1c, `dN/dy` dell'`A` `x1`)*; **`eta = 2 |a1 - a2| / (a1 + a2)`** con `a_i = a - a(V0)` di ciascuna massa *(la mia lettura, dichiarata)*, l'incertezza dai fit.

## 2-octies. [M0037-01bis] LA PARTE IMPULSIVA? LA CADUTA A FINESTRE *(Luca, `00:44`; scritta PRIMA del codice e dei numeri, `00:46` da `date`)*

- **(a) solo lettura** di `serie.json` gia' su disco *(`M1658/c1/caduta_V2`, `caduta_V2_x0.5`, `caduta_V2_x2.0`, `caduta_V0`; un punto ogni `10` tick, `k 0..2000`)*: **`doc/referti_l2/caduta_finestre.py`**, referto **`caduta_finestre.txt`**.
- **Il fit:** la stessa forma di `fondo_1c.fit_a` *(`y = c0 + c1 k + a k^2/2`, minimi quadrati, l'incertezza dai residui)* sulle finestre **`[200, 800]`, `[800, 1400]`, `[1400, 2000]`, estremi COMPRESI** *(il punto `800` e il `1400` stanno in due finestre: dichiarato)*. ### **L'incertezza dai residui ignora la correlazione dei punti vicini: e' un pavimento, non una barra vera** -- dichiarato.
- **Il caso noto:** la finestra intera `[200, 2000]` della V2 `x1` = `fondo_1c.fit_a` **al bit** *(gli stessi punti, lo stesso codice)*, e stampata contro `+6.2969e-07`. **DEVE FALLIRE:** la finestra `[200, 1990]` diversa al bit.
- **La velocita':** `v(k)` = la pendenza di una retta ai minimi quadrati sui punti in `[k - 50, k + 50]` *(«lisciata su `100` tick»: la mia lettura)*, stampata a `k = 200, 400, ..., 1800`, e a `2000` sulla finestra monolatera `[1900, 2000]` *(dichiarato)*.
- ### **(b) LA SOGLIA, la mia lettura del mandato, dichiarata ORA:** il criterio si legge sulla **V2 `x1` NETTA** *(`a - a(V0)` per finestra, la stessa grandezza di K)*: **si lancia se `a_netta[1400, 2000] > 1.2 a_netta[200, 800]`**, sul valore centrale come scritto. **Stampo anche la grezza:** ### **se la netta e la grezza decidono diversamente, FERMO e chiedo.**
- **Se si lancia:** UNA corsa in coda a priorita' `0`, `M0037_caduta_lunga`: la caduta V2 `x1` da `6000` tick dallo stesso oggetto *(`M1658/tenuta/L-1_proiezione_K/stato_003000.npz`)*, gli stati ogni `250`; uno script nuovo *(`fondo_1c.caduta` ha `K_CADUTA = 2000` e non salva stati)*, la lettura a finestre di `1000` a fine corsa. **Se non si lancia:** lo dico, e `[M0037-01]` resta la pista.
- **Le previsioni del guardiano:** `a` cresce fra prima e ultima finestra di piu' del `20%` *(`35%`)*; se cresce, a `6000` tick K sopra `0.5` *(`25%`)*.

## 2-nonies. [M0100] LA CADUTA PER PARTI: LA CORSA *(DECISIONE DI LUCA, `01:00`; scritta PRIMA del codice, `01:04` da `date`)*

- **`git log --all --fixed-strings --grep "[M0100"`: vuoto** *(`01:01`)*: niente fatto prima.
- **La corsa `M0100_caduta_parti`**, priorita' `0`: **`fondo_1c.caduta("V2")` cosi' com'e'** *(lo stato `k 3000` di `L-1_proiezione_K`, `2000` tick, il campo `x1`)*, con **`fondo_1c.BASE` = `M1658/c1_parti`** e **`fondo_1c.ciclo` avvolta IN MEMORIA**: dopo ogni tick chiama il `dopo` di `caduta` e poi, **senza toccare lo stato**, (i) **salva lo stato ogni `250`** *(e a `k 0`: tutte le `Z["chiavi"]` piu' `campo_A`, `campo_E`, come `tenuta_fondo.corsa`, con lo sha1)*; (ii) **ogni `10` tick misura le due parti** -- ### **questa e' una mia scelta dichiarata:** con gli stati ogni `250`, una finestra di `600` ha `2`-`3` stati, **troppo pochi per un fit con tre parametri**; i baricentri delle parti ogni `10` li danno come la serie del totale.
- ### **LE PARTI, la mia definizione dichiarata:** `Q_K` = la base di `tenuta_fondo.base_k(Z, "K")` *(la STESSA della semina `proiezione_K`: `12 x 2`, ortonormale dal QR)*; **`psi_K` = `psi Q_K* Q_K^T` nodo per nodo** *(il proiettore ortogonale sullo spazio interno di `A(K)` al fondo; la fase `e^{iK.d}` della semina e' uno scalare per nodo e non entra)*, **`psi_R = psi - psi_K`**. Per ciascuna: la frazione di norma, il baricentro `(x, y)` con lo stesso `dxy` della serie del totale.
- **`Q_K` si calcola PRIMA, in un processo a parte** *(`caduta_parti.py base`, `24` tick di risposta lineare su una scena sua: `tenuta_fondo.risposta` tocca la scena e la rimette; **non lo faccio dentro la corsa** per non rischiare che tocchi il totale)*, salvato in `M1658/c1_parti/Q_K.npz` con lo sha1; la corsa lo carica.
- **I CASI NOTI della lettura:** **CN1** la serie del totale = `M1658/c1/caduta_V2` **AL BIT** *(le misure in piu' non toccano la caduta)*; **CN2** `f_K y_K + f_R y_R = y` entro `1e-12` a ogni punto *(il proiettore e' ortogonale)*; **CN3** le parti ricalcolate dallo stato salvato a `k 2000` = quelle della serie **al bit**; **CN4** `Q_K` ricalcolato nella lettura = quello del file al bit. **DEVE FALLIRE:** CN2 con `1.1 Q_K` *(non un proiettore)*.
- **La lettura:** il fit di `caduta_finestre.fit` su `[200, 800]`, `[800, 1400]`, `[1400, 2000]` per `y_K`, `y_R` e il totale, e le frazioni. ### **NON c'e' la V0 per parti** *(Luca ha deciso solo la V2)*: **le `a` per parte sono GREZZE**; come riferimento stampo la `a` della V0 del totale per finestra *([M0037-01bis])*.
- **Le schede [M1751]: FERME fino a domani di giorno** *(Luca)*.

### 2-nonies-bis. LA CORREZIONE: LE PARTI PER CELLA *(annotazione, `01:12` da `date`: la 2-nonies NON si riscrive)*

- ### **La 2-nonies diceva «`psi_K` nodo per nodo»: SBAGLIATO, mio.** `psi_h.reshape(n, 12)` e' la **CELLA `v`** *(i tre archi uscenti da `v`, sei mezzi archi per due componenti: il mattone di `A(K)`)*; la corsa cadde sul mio assert *(`859a4067`)*.
- **La v2 (`caduta_parti_v2.py`):** `psi_K = psi Q_K* Q_K^T` **cella per cella**, `psi_R = psi - psi_K`; **il baricentro di ciascuna parte con la posizione del nodo `v` della cella** *(lo stesso `dxy`)*; **e il totale ANCHE per cella**, `y_T`. **CN2 diventa** `(n_K y_K + n_R y_R)/(n_K + n_R) = y_T` entro `1e-12` *(il proiettore e' ortogonale nella cella)*. **CN1** *(la serie per nodo = 1c al bit)*, **CN3**, **CN4** e il **DEVE FALLIRE** restano. **Al posto dell'assert sbagliato, uno giusto:** le code dei tre archi della cella `v` sono `v` *(`nodo[0::2].reshape(n, 3)`)*.
- **La lettura stampa le `a` per finestra di `y_K`, `y_R`, `y_T` (cella) e `y` (nodo)**: `y_T` e `y` sono lo stesso oggetto pesato in due modi; **se le loro `a` differiscono piu' delle barre, lo dico.**
- **`Q_K.npz` resta** *(calcolato `01:07`, sha1 `55e6fb84`: non dipende dalla cella o dal nodo)*. **La voce in coda:** `M0100_caduta_parti_v2`, priorita' `0` *(il nome della v1 resta nel registro come FALLITO)*.

## 2-decies. [M0118] K E LA FORMA *(DECISIONE DI LUCA, `01:17`; scritta PRIMA del codice e dei numeri, `01:21` da `date`)*

- **`git log --all --fixed-strings --grep "[M0118"`: vuoto** *(`01:19`)*.
- ### **[M0118-01] la forma durante la caduta, dagli STATI ogni `250` di `M0100_caduta_parti_v2`** *(`M1658/c1_parti/caduta_V2/stato_<k>.npz`, `k 0..2000`)*, nella lettura `caduta_parti_v3.py` *(la v2 e' IN CORSA: non si tocca; la v3 importa e aggiunge)*, il referto `caduta_parti.txt`:
  - **`w(k)` e i pezzi** = `torneo_tenuta.misura` *(come le tenute)*;
  - **`m = 3`** dell'oggetto intero = `forma_fondo.momenti` sugli anelli `[4, 8)`, `[8, 12)`, `[12, 16)` attorno al baricentro di `rho` *(`forma_fondo.geometria`)*, col fondo del favo accanto;
  - ### **`omega(k)` su `[k, k + 250]`, la MIA lettura dichiarata:** gli stati sono ogni `250`, `omega` per tick NON e' salvato *(`fondo_1c.caduta` non lo scrive)*: **`phi = -arg <psi_k | psi_{k+250}>`, `omega = (phi + 2 pi m)/250`, con `m` intero scelto per l'`omega` piu' vicino a `+0.0940`** *(1b)*. **Univoco solo se il vero `omega` sta entro `pi/250 = 0.01257` da `0.0940`**: un oggetto che scendesse di piu' **verso il bordo `0.01187`** non lo si vedrebbe cosi' -- dichiarato. Accanto: **la fedelta'** `|<psi_k|psi_{k+250}>|/(|psi_k||psi_{k+250}|)`.
  - **IL CASO NOTO di `omega`:** sulla tenuta 1b *(`M1658/tenuta/L-1_proiezione_K`, che ha `omega.npy` per tick)*, `[2500, 2750]` e `[2750, 3000]`: il metodo = la media di `omega.npy` sulla finestra **entro `1e-4`**. **DEVE FALLIRE:** la coppia `[2500, 3000]` divisa per `250` *(la finestra sbagliata)* oltre `1e-4`.
  - **La lettura «si deforma»:** stampo i numeri; **«`omega` cala di piu' di `1e-3`»** e' la previsione del guardiano, la confronto, non la uso per decidere niente.
- ### **[M0118-02] K a parita' di massa, forma diversa:** `doc/referti_l2/k_forma.py`, come `eotvos_fondo.py` *(`fondo_1c` con `OGGETTO` = `M1658/tenuta_v2/L-1_a1.0_l0.7/stato_003000.npz`, `BASE` = `M1658/c1_l07`, in memoria)*, **piu' gli stati ogni `250`** *(`fondo_1c.ciclo` avvolta: legge e salva, non tocca)*. **In coda a priorita' `0`:** la caduta V2 `x1` e la V0 *(Luca)*, ### **e -- mia aggiunta dichiarata, come in [M0037] -- i due calci `k 0.010` e `k 0`:** **K vuole `m*`**, e [M0037-03] ha mostrato che «massa» *(la norma)* e `m*` non vanno insieme. **La lettura stampa K DUE volte:** con `m*(1c)` *(«a parita' di massa», la lettura di Luca)* e con `m*(l0.7)` misurato.
  - **K a finestre di `600`** *(`[200, 800]`, `[800, 1400]`, `[1400, 2000]`, `caduta_finestre.fit`, `a - a(V0)` nella stessa finestra)* per **l0.7, 1c e a2**, e sull'intera `[200, 2000]`. Referto `k_forma.txt`.
- **[M0118-03]:** in `doc/SAGOMA.md` alle righe **S3** e **S4**: le tre K *(1c, a2, l0.7, sull'intera e per finestra)* e le tre eta a due a due, **come numeri, senza giudizio** *(`eta_ij = 2|a_i - a_j|/(a_i + a_j)`, `a = a - a(V0)` sull'intera `[200, 2000]`)*.
- **Le previsioni del guardiano:** `omega` cala durante la caduta di piu' di `1e-3` *(`55%`)*; `K(l0.7)` diverso da `K(1c)` oltre il `5%` *(`60%`)*; `a_K` e `a_R` di segno opposto *(`45%`)*.

## 2-undecies. [M0140] omega COL METODO DI 1b; w DELLA V0 DI l0.7 *(DECISIONE DI LUCA, `01:40`; scritta PRIMA del codice, `01:42` da `date`)*

- **`git log --all --fixed-strings --grep "[M0140"`: vuoto** *(`01:41`)*.
- ### **omega come `tenuta_fondo.corsa`** *(il referto 1b)*: **`omega` per tick = `-arg <psi_prima | psi_dopo>`** su ogni tick. **Gli stati ogni `250` non bastano** *(il metodo vuole il tick)*: **si RIFA' la caduta V2 `x1`**, `fondo_1c.caduta("V2")` cosi' com'e' *(`BASE` = `M1658/c1_omega`)*, con `fondo_1c.ciclo` avvolta: **registra `omega` per tick, e a ogni `k` multiplo di `250` CONFRONTA `psi_h` con lo stato salvato da `M0100_caduta_parti_v2`** *(`M1658/c1_parti/caduta_V2/stato_<k>.npz`)*. **Non salva stati.** `caduta_omega.py corsa`, **in coda a priorita' `0`** *(`M0140_caduta_omega`)*.
- **IL CASO NOTO, entro `1e-4`** *(Luca)*: `caduta_omega.py noto`, **in coda** *(`M0140_omega_noto`)*: **dalla tenuta 1b a `k 2500`** *(`FS.carica` con quello stato)*, `250` tick col tick della tenuta *(`N = 1`, `cs_N False`, `segno 0`; `C.residuo` alla fase GLOBALE `(2500 + kk) % OGNI_GAUSS`, come in `tenuta_fondo.corsa`)*: **la media di `omega` su `[2501, 2750]` = quella di `omega.npy` entro `1e-4`**; **e, piu' stretto, `psi_h` a `2750` = `stato_002750` AL BIT** *(se non al bit, lo dico: il criterio di Luca e' `1e-4`)*. **DEVE FALLIRE:** la media di `omega.npy` su `[2251, 2500]` *(un'altra finestra)* contro quella misurata, oltre `1e-4` *(se non fallisce, lo dico: vorrebbe dire che `omega` e' costante entro `1e-4` e il caso noto non distingue)*.
- **Il controllo della corsa:** la serie del totale = `M1658/c1/caduta_V2` AL BIT, e `psi_h` = gli stati di `c1_parti` AL BIT a ogni `250`. **La lettura** *(`caduta_omega.py lettura`, AGGIUNTA a `caduta_parti.txt`: la colonna omega v2, la vecchia resta)*: `omega` medio su `[k + 1, k + 250]`, `k = 0..1750`, e la differenza fra l'ultima finestra e la prima, contro la previsione del guardiano *(`> 1e-3`)*.
- **[M0140] l0.7:** quando finisce, **`w(k)` della V0 accanto a quella della V2** *(`torneo_tenuta.misura` sugli stati ogni `250` di `M1658/c1_l07/caduta_V0` e `caduta_V2`)* in `forma_l07.py` -> `k_forma.txt` *(insieme a `k_forma_v2.py`: le due convenzioni)*.

## 3-bis. [M1330-B] IL PUNTO FISSO DEL SOLITONE: L'OGGETTO AL FONDO A K SENZA RESPIRO *(DECISIONE DI LUCA, `13:30`; scritta PRIMA del codice, `13:29` da `date`; il mandato dice «sez. 3»: la `3` c'e' gia' -- i criteri di 1a --, questa e' la `3-bis`)*

- **`git log --all --fixed-strings --grep "[M1330"`: vuoto** *(`13:25`)*.
- ### **[M1330-B1] il giro** *(`doc/referti_l2/fondo_puntofisso.py`; le uscite `E:/soliton_simulator/controllo/M1330/puntofisso/giro_<g>/`)*:
  - **(i)** dallo stato di partenza *(giro `1`: `M1658/tenuta/L-1_proiezione_K/stato_003000.npz`)* **`2000` tick a `N = 1`** col tick della tenuta *(`CS.tick_var(..., N = 1, cs_N False, segno 0)`, `C.residuo` ogni `OGNI_GAUSS`, la forma L-1 del nucleo: come `caduta_omega.noto`, che ridiede la tenuta AL BIT)*, **gli stati ogni `50`**, **`omega` per tick** `-arg <psi_prima|psi_dopo>`, **`w` ogni `50`** *(`torneo_tenuta.misura` sullo stato salvato)*.
  - **(ii) il periodo:** **i minimi LOCALI STRETTI di `w` sulla griglia di `50`** *(`w[i] < w[i-1]` e `w[i] < w[i+1]`, estremi esclusi: la mia lettura di «due minimi consecutivi», dichiarata; stampo TUTTI i minimi)*; il periodo = `(k_a, k_b]` fra i primi due. **La media:** `psi_medio = (1/(k_b - k_a)) somma_{j in (k_a, k_b]} psi_j e^{+i theta_j}`, **`theta_j` = la somma degli `omega` misurati fino al tick `j`** *(«riallineata tick per tick»: la mia lettura, dichiarata -- la fase vera di ogni tick, non una `omega` fissa)*; la somma progressiva tenuta in memoria ogni `50`.
  - **(iii)** `psi_medio` **riproiettato su `Q_K` cella per cella** *(`psi Q_K* Q_K^T`, `Q_K` = `M1658/c1_parti/Q_K.npz`, la base della semina)* e **riportato alla massa dello stato di partenza del giro `1`** *(`somma |psi|^2`)*; **le altre chiavi dello stato e i campi `A`, `E` dallo stato a `k_b`** *(mia scelta, dichiarata: come la semina, che sostituisce `psi` lasciando i campi)*. Salvato come `partenza.npz` del giro dopo.
  - **(iv)** **tre giri.** **IL CRITERIO** *(Luca)*: **`(w_max - w_min)/w_medio < 5%` sui `w` dell'ULTIMO giro** *(i `41` valori di `k 0..2000` del giro `3`)*.
  - ### **SE IN UN GIRO NON CI SONO DUE MINIMI LOCALI:** il giro si ferma dopo (i), **lo script esce FERMO** *(codice `2`)* coi `w(k)` stampati. ### **LA MIA PREVISIONE, scritta ora:** **succede gia' al giro `1`** *(`70%`)*: a riposo la tenuta 1b va da `w 15.5` a un minimo vicino a `8.0` verso `k 2000` e risale *(`8.5` a `3000`)*, e la caduta 1c da `k 3000` risale fino a `15.5` a `k 5000`: **il respiro dura piu' di `2000` tick.**
  - **IL CASO NOTO** *(`fondo_puntofisso.py noto`, senza tick)*: **un giro con la media = l'identita'** *(la finestra di un solo stato, `theta = 0`)* **e il proiettore = l'identita' `12 x 12`** ridà lo stato `k 3000` **AL BIT** *(`psi_h`, e tutte le chiavi e i campi dopo `FS.carica`)*; **DEVE FALLIRE:** lo stesso con `Q_K` da' `psi_h` diverso.
- **[M1330-B2]** `fondo_puntofisso.py corsa` = **UNA voce in coda**, `M1330_puntofisso`, **priorita' `1`** *(la seconda versione di [M1330], arrivata alle `13:30` mentre scrivevo: vale SOLO l'ultima -- PRECEDENZA-IN-CODA; la prima diceva `0`)*; la voce si scrive **a lanciatore fermo** *(la lezione di [M0140])* e il lanciatore si rilancia **dopo** il commit.
- **[M1330-B3]** solo se il criterio passa: le cadute V2 `x0.5`, `x1`, `x2` e la V0 dall'oggetto senza respiro, **col gradiente pesato di B0** *(un'altra carta, dopo)*.
- **[M1330-B4]** `omega` per tick dei `2000` tick del giro `1` = **a riposo da `k 3000` a `5000`**: in `fondo_puntofisso.py lettura`, **le finestre di `250` accanto a quelle della caduta di [M0140]** *(`M1658/c1_omega/omega.json`, gli stessi `k`)*, aggiunte a `caduta_parti.txt`. **Nessuna corsa in piu'.**
- **Le previsioni del guardiano** *(dal mandato)*: B1 il respiro sotto il `5%` in tre giri *(`55%`)*; non scende ma si dimezza *(`30%`)*.

## 3-ter. [M1330-B0] IL GRADIENTE PESATO E [M1330-B5] m* IN FUNZIONE DI w *(la seconda versione di [M1330], DECISIONE DI LUCA `13:30`; l'ordine: A, B0, B5, B1/B2, D, C, B3; scritta PRIMA del codice, `13:31` da `date`)*

- ### **[M1330-B0] solo lettura** *(`doc/referti_l2/gradiente_pesato.py`, AGGIUNTO a `k_forma.txt`)*: dagli stati ogni `250` della caduta per parti *(`M1658/c1_parti/caduta_V2/stato_<k>.npz`, 1c V2 `x1`)*, **`<dN/dy> = somma rho dN/dy / somma rho`** con `rho` per nodo *(`bincount(nodo, |psi_h|^2)`)* e **`dN/dy` nodo per nodo derivato da `caduta_libera.campo_N`**: `N = e^{-kappa chi}`, `chi = A sin(2 pi (y - y_c)/L_y)` -> **`dN/dy = -kappa N A (2 pi/L_y) cos(2 pi (y - y_c)/L_y)`** *(`y = m2 sqrt3/2`, `y_c` e `A` dalla corsa)*; **contro il «centro» di S3** `-kappa A 2 pi/L_y`. Accanto, `w` dello stato. **Il caso noto:** un `rho` tutto su un nodo con `y = y_c` ridà il centro *(entro `1e-12` relativo)*; **DEVE FALLIRE:** su un nodo a `y_c + L_y/4` *(`cos = 0`)* non lo ridà.
  - **Se differiscono piu' del `2%`** *(Luca)*: **K CIMA si rilegge col gradiente pesato** -- per finestra, la media di `<dN/dy>` sugli stati nella finestra *(la mia lettura, dichiarata)*. **Lo stampo in ogni caso**, marcato.
- ### **[M1330-B5] l'oggetto efficace** *(`doc/referti_l2/mstar_w.py`)*: **dagli stati della V0 di l0.7** *(`M1658/c1_l07/caduta_V0/stato_001500.npz`, `w 6.965`, e `stato_000500.npz`, `w 14.427`, i valori di `forma_l07`)*, **i calci `k 0.010` e `k 0`, `1000` tick** = `fondo_1c.calcio` cosi' com'e' con `OGGETTO` = quello stato e `BASE` = `M1330/mstar_w/k<k>`. **Quattro corse in coda a priorita' `0`.** **La lettura:** `m*(w 7)`, `m*(w 14)` *(`eotvos_fondo.mstar_K`)*, il rapporto; **K CIMA delle finestre di l0.7 con l'uno e con l'altro `m*`**, accanto a `w` medio della finestra *(dagli stati della V2 di l0.7)* -- **quale sia «la fase giusta» lo dicono i `w`, non lo scelgo io.** Colonna in piu' in `k_forma.txt`.
- **Le previsioni del guardiano** *(dal mandato)*: B0: `<dN/dy>` diverso dal centro meno del `2%` a `w 8.5` *(`80%`)*; piu' del `5%` a `w 15.5` *(`40%`)*. B5: `m*(w 14)/m*(w 7)` fuori da `[0.9, 1.1]` *(`50%`)*; se si', K(w) costante entro il `10%` col `m*` della fase *(`35%`)*.

## 4-ter. [M1330-F] E(p): PARTICELLA O LUCE? *(DECISIONE DI LUCA, `14:45`; scritta PRIMA del codice, `14:47` da `date`; il mandato dice «sez. 4»: la `4` e la `4-bis` ci sono gia' -- l'ablazione --, questa e' la `4-ter`)*

- **`git log --all --fixed-strings --grep "[M1330-F"`: vuoto** *(`14:46`)*.
- ### **LE UNITA', dichiarate PRIMA:** **`spettro_gap_v2.txt` da' `v_max = 0.084955` PER TICK** *(in unita' del reticolo)*; **il `0.566` del mandato e' la stessa velocita' in unita' di `s`** *(`0.566 s`, `s = 0.15`)*. **Le velocita' del baricentro sono PER TICK:** **la `c` fissata nei fit e' `0.084955`.** La lettura stampa anche `m* c`: **se i calci fino a `0.4`-`0.5` stanno molto sotto `p = m* c`, la saturazione non si puo' vedere** -- lo dira' la lettura, non lo decido io.
- ### **L'OGGETTO** *(il punto fisso NON ha passato B1: FERMO al giro 1)*: **l'oggetto che respira, col calcio nella fase di `w` minimo** *(Luca)*: **lo stato `k 300` del giro 1** *(`M1330/puntofisso/giro_1/stato_000300.npz`, `w 8.368`: il primo `argmin` dei `41` valori -- la mia lettura, dichiarata; il minimo LOCALE STRETTO era a `k 1750`, ma `w` li' e' `15.6`, non un minimo vero del respiro)*.
- ### **LE DEFINIZIONI** *(tutte dallo stato calciato a `k 0`, prima dei tick, e dalla corsa di `1000` tick)*:
  - **`p`** = **la media di `k - K` pesata con `|psi~_k|^2`, nella direzione del calcio `u`** *(la mia scelta fra le due del mandato)*: `psi_h` ha **sei mezzi archi per cella** *(i tre archi uscenti da `v`)*; **per ciascuno dei sei e delle due componenti** la trasformata sulle `162 x 162` celle con le posizioni di cella; `k - K` ridotto all'immagine piu' vicina nel reticolo reciproco *(`B0`, `B1` di `toro.vettori`)*. **IL CONTROLLO:** `p(0.010) - p(0)` = `0.010` entro l'`1%` *(il calcio sposta `k` di `k`)*.
  - **`v`** = la velocita' del baricentro lungo `u` su `[200, 1000]` *(`massa_calcio.velocita`, il fit da `k 200`: quella di `m*`)*.
  - ### **`E`, DUE VERSIONI, ENTRAMBE STAMPATE:** **`E_H` = `H(calciato) - H(fermo)` a `k 0`**, con l'H del libro dei conti *(Luca: `somma conti.conti_nodo["tot"] + campo.K() + campo.V()`, la `E` = `totd + KVd` della serie di `prezzo_spazio`)*; **e `E_w` = `<omega>(calciato) - <omega>(fermo)`** su `[1, 1000]`, `omega` per tick `-arg <psi_prima|psi_dopo>` *(la convenzione della cima)*. ### **PERCHE' DUE:** **l'H del libro NON e' la quasi-energia della banda**, mentre **la `c` del reticolo e il caso noto (b) sono nella quasi-energia** *(`-arg lambda` di `A(k)`)*: **il caso noto (b) puo' passare solo per `E_w`; per `E_H` mi aspetto che FALLISCA per costruzione** *(lo scrivo prima)*. **Quale `E` va nei fit «veri» lo decide Luca;** i fit si fanno con tutte e due.
  - **`m`** dalla curvatura a `p -> 0`: `E = p^2/(2m)` sui tre `p` piu' piccoli; **deve ridare `m* = 0.010/(v - v0)`** del calcio *(stampato, contro)*.
  - **I pezzi:** lo stato a `k 1000` *(`fondo_1c.ciclo` avvolta: salva SOLO lo stato finale)*, `torneo_tenuta.misura`; **un pezzo richiesto; se si spezza, quel `k` e' il limite** *(stampato)*.
- ### **I CASI NOTI:**
  - **(a)** **il calcio `0.010` dall'oggetto di 1c, rifatto** *(`fondo_1c.calcio` cosi' com'e', `BASE` = `M1330/ep/noto_a`)*: **la serie e `omega` = `M1658/c1/calcio_k0.010_a1` AL BIT**, quindi `v` e `m*` di 1c al bit. **Una corsa.**
  - **(b)** **un'onda piana lineare** *(L0, la forma del nucleo senza non linearita')* **a `k = K + q`** *(`q` sulla griglia reciproca, il primo punto lungo `u`)*, **con l'ampiezza `A_IMP` di `tenuta_fondo.risposta` e la sua differenza simmetrica `(+A, -A)`** *(cosi' gli ordini pari si cancellano, come per `A(K)`)*: un tick, **`omega` misurato contro `-arg lambda` della banda in `q`**. ### **«AL BIT» NON E' POSSIBILE PER COSTRUZIONE:** le somme del tick su tutto il reticolo e quelle di `A(k)` per cella hanno un ordine diverso; **il criterio, mio e dichiarato: `1e-10` assoluto.** **Senza tick lunghi: dentro la lettura.**
- **LE CORSE** *(in coda a priorita' `1`, DOPO il punto fisso, che e' chiuso)*: **i calci `k = 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5`** *(il `0`: il fermo, per `v0`, `E` e `omega`; il `0.5` in coda subito -- se `v` ha gia' saturato a `0.4` lo dira' la lettura, ma l'ordine «0.5 solo se» vorrebbe una decisione a meta' notte: **mia scelta, dichiarata**)*, `1000` tick, `fondo_1c.calcio` con `OGGETTO` = lo stato `k 300` e `BASE` = `M1330/ep/k<k>`; **piu' il caso noto (a).** **Undici corse.**
- **LA LETTURA:** la tabella `p, v, E_H, E_w`, i pezzi; **per ciascuna `E`, i due fit** *(onda `E = c p + b`; particella `E = sqrt(m^2 c^4 + p^2 c^2) - m c^2`)*, **con `c` libera e con `c = 0.084955`**, il chi quadro di ciascuno *(le barre: `E_w` dalla dispersione di `omega` per tick, `/ sqrt(1000)`; `E_H` senza barra -- chi quadro non pesato, dichiarato)*; `v(p)` contro `p c^2/(E + m c^2)`; `dp/dv` contro `gamma^3 m`. Referto `ep_fondo.txt`. **Nessun giudizio oltre i chi quadri.**
- **Le previsioni del guardiano:** `v` satura sotto `0.566` entro `k 0.4` *(`65%`; in unita' di `s`)*; la particella batte l'onda di piu' di `10` nel chi quadro *(`55%`)*; la `c` libera entro il `10%` di `0.566` *(`50%`)*; `m` entro il `10%` di `m*` *(`60%`)*; si spezza prima di `0.3` *(`30%`)*.

### 4-ter-bis. LA CADUTA DEI CALCI E LA v2 *(annotazione, `15:10` da `date`: la 4-ter non si riscrive)*

- **I calci di `ep_fondo.py` (`8f236e63`) hanno fatto i `1000` tick e sono CADUTI salvando lo stato finale:** la cartella `M1330/ep/k<k>` nasce in `fondo_1c.scrivi`, DOPO il ciclo, e il mio `ciclo` avvolto salvava PRIMA. **La serie non e' stata scritta: i tick sono persi.** **Errore mio.** Il caso noto (a) non salva lo stato finale ed e' finito.
- **La v2** *(`ep_fondo_v2.py`)*: la cartella si crea PRIMA. **Le nove corse si rifanno** *(`M1330F2_calcio_k<k>`, priorita' `1`)*, **messe in coda SOLO a lanciatore fermo** *(i tre calci `0.3`, `0.4`, `0.5` della v1 girano ancora e cadranno alla fine: non li posso fermare)*. **La lettura resta `ep_fondo.py lettura`.**

## 3-quater. [M1540] IL PUNTO FISSO A 6000 TICK PER GIRO *(DECISIONE DI LUCA, `15:40`; scritta PRIMA del codice, `15:46` da `date`)*

- **`git log --all --fixed-strings --grep "[M1540"`: vuoto** *(`15:44`)*.
- **La fase (i) a `6000` tick per giro** *(«due periodi del respiro»)*, **gli stati ogni `100`** *(quindi `w` ogni `100`: `61` valori per giro, e i minimi locali stretti su quella griglia)*; **il resto invariato** *(la sez. `3-bis`: la media sul periodo fra i primi due minimi con `theta` dagli `omega` misurati, la riproiezione su `Q_K`, la massa, tre giri, il criterio `< 5%` sull'ultimo giro, FERMO senza due minimi)*. `fondo_puntofisso_v2.py` *(`K_GIRO`, `OGNI`, la cartella `M1330/puntofisso_v2` in memoria)*. **In coda a priorita' `1`**, `M1540_puntofisso_v2`, **dopo le corse di F** *(finite alle `15:44:24`: la voce si scrive a lanciatore fermo)*.
- **Il caso noto** *(il giro con la media identita' = lo stato al bit)* **non dipende da `K_GIRO` e `OGNI`:** e' quello di `fondo_puntofisso_noto.txt` *(3 su 3)*.


## 3-quinquies. [M1735] IL PUNTO FISSO v3: IL PERIODO DA w LISCIATA *(DECISIONE DI LUCA, `17:35`; scritta PRIMA del codice e dei numeri, `17:36` da `date`)*

- **`git log --all --fixed-strings --grep "[M1735"`: vuoto** *(`17:34:40`)*.
- **Perche':** la v2 *(sez. `3-quater`, `0793e8bd`)* non passa *(`0.3079` sull'ultimo giro)*, ma i minimi locali stretti di `w` grezza erano oscillazioni corte sopra il respiro *(periodi `200`, `2000`, `300` tick)*: il fallimento non distingueva l'oggetto dal metodo.
- **Di Luca:**
  - il periodo si legge da **`w` LISCIATA, media mobile su `500` tick**: i minimi della lisciata, e il periodo e' la distanza fra i primi due;
  - **se ce n'e' UNO SOLO, periodo = `4500`** *(dal giro 1 della v2)*;
  - la media di `psi` *(con `e^{+i theta}`, come nella v2)* su **una finestra intera `[k_min, k_min + periodo]`**;
  - **la partenza: lo stato finale del giro 3 della v2**, `M1330/puntofisso_v2/giro_3/stato_006000.npz` *(`w 12.57`; non `partenza_giro_4.npz`, che e' gia' mediata)*;
  - tre giri da `6000` tick, stati ogni `100`; **il criterio invariato** *(`< 5%` sull'ultimo giro)*; in coda a priorita' `1`.
- **LE MIE SCELTE DI CRITERIO, dichiarate qui prima della corsa** *(il mandato non le fissa)*:
  1. **la media mobile:** `w` e' campionata ogni `100`, quindi `500` tick = **`5` campioni consecutivi**, finestra **centrata**, solo finestre intere *(la lisciata esiste da `k 200` a `k 5800`)*;
  2. **i minimi della lisciata** sono minimi locali **stretti** *(come `fondo_puntofisso.minimi`)*, gli estremi esclusi;
  3. **nessun minimo: FERMO**; **un solo minimo e `k_min + 4500 > 6000`** *(la finestra non sta nel giro)*: **FERMO**; nessun ripiego mio;
  4. **la massa** e' quella della partenza della v1 e della v2 *(`massa_di(PARTENZA_1)`, invariata)*; la massa del nuovo stato di partenza si stampa accanto.
- **IL CODICE** *(`fondo_puntofisso_v3.py`)*: **il giro e' `fondo_puntofisso.giro` cosi' com'e'**. Cambia solo la funzione `minimi`, sostituita in memoria: restituisce gli indici `[k_min, k_min + periodo]/100`, cosi' il giro media su quella finestra e riparte dallo stato a `k_min + periodo`, **come la v2 ripartiva dallo stato al secondo minimo**. La decisione sul periodo *(la lisciata, i suoi minimi, la fonte `due minimi` o `ripiego 4500`, l'eventuale motivo del FERMO)* si scrive in `giro_<g>/periodo_v3.json`. In `giro.json` il campo `minimi_k` contiene **la finestra**, non i minimi: e' il nome che usa la v1.
- **IL CASO NOTO** *(`fondo_puntofisso_v3.py noto`; i DEVE fissati qui)*:
  - (a) **di Luca:** sulla serie `w` del giro 1 della v2 il periodo e' **fra `4000` e `5000`**;
  - (b) **DEVE FALLIRE:** sulla stessa serie il metodo della v2 *(i minimi stretti di `w` grezza)* dava un periodo **fuori** da `[4000, 5000]`;
  - (c) `w = 10 + 3 cos(2 pi k / 3000)` su `k = 0..6000`: due minimi, **periodo `3000`, finestra `[1500, 4500]`**;
  - (d) `w = 10 + ((k - 1000)/1000)^2`: un solo minimo, a `k 1000`: **il ripiego, finestra `[1000, 5500]`**;
  - (e) `w` crescente: **nessun minimo, FERMO**;
  - (f) `w = 10 + ((k - 2000)/1000)^2`: un solo minimo, a `k 2000`, e `2000 + 4500 > 6000`: **FERMO**.
- **SE PASSA** *(il criterio sull'ultimo giro)*: **B3 parte senza chiedere** *(Luca: «B3 parte da solo, le quattro cadute»)*. La coda non ha dipendenze fra voci, quindi: **B3 ha la sua carta e i suoi script, committati mentre la v3 gira; le quattro voci entrano in coda a lanciatore fermo, dopo la lettura della v3, e solo se la v3 passa.** **Se non passa, o si ferma: FERMO, i numeri a Luca.**
- **LE PREVISIONI:**
  - **del guardiano:** il caso noto da' `4500 +- 300` *(`85%`)*; il respiro `< 10%` al giro 2 *(`60%`)*; `< 5%` al giro 3 *(`50%`)*;
  - **mie:** (a) passa *(`80%`)*. **Il criterio al giro 3 `< 5%`: `35%`.** Il motivo, qualitativo: nella v2 il respiro e' calato di giro in giro *(`0.7565`, `0.6325`, `0.3079`)*, ma senza un ritmo che arrivi sotto `0.05` in altri tre giri.


## 3-sexies. [M1748] IL PUNTO FISSO v3, IL PERIODO DAL MASSIMO AL MINIMO DELLA LISCIATA *(DECISIONE DI LUCA, `17:48`; scritta PRIMA del codice e dei numeri, `17:49` da `date`)*

- **`git log --all --fixed-strings --grep "[M1748"`: vuoto** *(`17:47:53`)*.
- **Perche':** il caso noto della sez. `3-quinquies` e' fallito *(`11f57c86`)*: la lisciata del giro 1 della v2 ha un solo minimo *(k `4500`)*.
- **Di Luca:**
  - **`P = 2 x (k del minimo lisciato - k del massimo lisciato precedente)`**;
  - la media su **`[k_max - P/2, k_max + P/2]`**; **se la finestra esce dal giro, si accorcia al giro e si dichiara**;
  - il caso noto sul giro 1 della v2: **`P` fra `4000` e `5000`** *(il massimo a `2200`, il minimo a `4500`: `4600`)*;
  - **il resto invariato** *(la sez. `3-quinquies`: la lisciata di `500` tick, la partenza `puntofisso_v2/giro_3/stato_006000.npz`, tre giri da `6000`, stati ogni `100`, il criterio `< 5%`, priorita' `1`; se passa, B3 parte da solo)*.
- **Il file:** `fondo_puntofisso_v3.py` ha gia' girato il suo caso noto, quindi non si riscrive. Il nuovo e' **`fondo_puntofisso_v3b.py`**, con la cartella **`M1330/puntofisso_v3b`**. Usa la `lisciata` della v3 cosi' com'e', e sostituisce di nuovo `minimi` in memoria; il giro resta `fondo_puntofisso.giro`.
- **LE MIE SCELTE DI CRITERIO, dichiarate qui prima della corsa** *(il mandato non le fissa)*:
  1. **«il minimo lisciato»** e' il **primo** minimo locale stretto della lisciata *(come nella v3)*;
  2. **«il massimo lisciato precedente»** e' il **massimo** della lisciata sui punti prima di quel minimo *(l'argmax, e a parita' il primo)*. **Non uso un massimo locale stretto**, perche' sul giro 1 della v2 la lisciata ha `15.95` sia a k `2200` sia a `2300`, cosi' come stampata. **Se l'argmax cade sul primo punto della lisciata** *(k `200`, un bordo e non un massimo vero)*, **si usa lo stesso e si dichiara** `massimo_al_bordo: true`;
  3. **nessun minimo: FERMO**, come nella v3;
  4. la finestra e' `[k_max - (k_min - k_max), k_min]`, quindi **finisce sempre al minimo**, dentro il giro. **Puo' uscire solo a sinistra:** allora si accorcia a `0` e si dichiara `accorciata` con la finestra intera accanto. Il giro riparte dallo stato alla fine della finestra *(`k_min`)*, come prima.
- **IL CASO NOTO** *(`fondo_puntofisso_v3b.py noto`)*:
  - (a) **di Luca:** il giro 1 della v2, `P` fra `4000` e `5000`;
  - (b) **DEVE FALLIRE:** il metodo della v2 sulla stessa serie, `P` fra `4000` e `5000`;
  - (c) `w = 10 + 3 cos(2 pi (k - 2000)/4000)`: il massimo a `2000`, il minimo a `4000`, **`P 4000`, finestra `[0, 4000]`**, non accorciata *(il periodo `4000`: con `3000` c'e' un minimo gia' a k `500`, prima del massimo; corretto prima del commit)*;
  - (d) `w = 10 + 3 cos(2 pi (k - 1000)/3000)`: **`P 3000`, finestra `[-500, 2500]` accorciata a `[0, 2500]`**;
  - (e) `w` crescente: **FERMO**;
  - (f) `w = 10 + ((k - 1000)/1000)^2`: il minimo a `1000` e l'argmax al bordo *(k `200`)*: **`massimo_al_bordo` dichiarato**.
- **LE PREVISIONI** *(di Luca: `4600`)*: **mie,** (a) passa *(`85%`)*; il criterio al giro 3 `< 5%`: `35%`, come nella sez. `3-quinquies`.


## 3-septies. [M1330-B3] LA LEGGE DEL FONDO DALL'OGGETTO SENZA RESPIRO *(DECISIONE DI LUCA, `13:30` [M1330] e `17:35` [M1735]: «se passa, B3 parte da solo, le quattro cadute»; la sez. `3-bis` diceva «un'altra carta, dopo»: e' questa; scritta PRIMA del codice e dei numeri, mentre la v3b gira; `17:58:47` l'ultimo `date` prima di scriverla)*

- **Che cosa:** **le cadute V2 `x0.5`, `x1`, `x2` e la V0** dall'oggetto senza respiro, **col gradiente pesato di B0**; il referto **`legge_fondo_v2.txt`** *([M1330], seconda versione)*. Lo script e' `doc/referti_l2/legge_fondo_v2.py`, le uscite in `M1330/b3/<nome>/serie.json`.
- **LE MIE SCELTE, dichiarate prima** *(il mandato non le fissa)*:
  1. **l'oggetto:** `M1330/puntofisso_v3b/giro_3/partenza_giro_3.npz`, lo stato **la cui evoluzione di `6000` tick ha passato il criterio**. Non `partenza_giro_4.npz`: quella e' la media del giro 3, e **nessuna corsa ha misurato che non respiri**;
  2. **la macchina:** la V0 e' `fondo_1c.caduta("V0")` cosi' com'e'. Le V2 sono `fondo_s3.caduta` riga per riga, con una sola aggiunta in `misura`: **la quinta colonna `<dN/dy>` pesata con `rho`** *(la formula di `gradiente_pesato.dNdy`, `N` da `campo_N`)*, che non tocca la dinamica. `2000` tick, la serie ogni `MC.OGNI`;
  3. **`m*` e `omega_psi(N1)` sono quelli di 1c** *(il calcio `0.010`/`0` e l'orologio V2 a `N 1`)*, come in S3. **L'oggetto nuovo ha un `w` diverso, e B5 dice che `m*` dipende da `w`** *(il rapporto `1.0535` fra `w 14.4` e `w 7.0`)*. Il suo `m*` vorrebbe **due calci in piu'**, che il mandato non chiede: **lo chiedo a Luca, e non li lancio**;
  4. **la lettura:** per finestra *(`[200, 2000]`, `[200, 800]`, `[800, 1400]`, `[1400, 2000]`)*, `a - a(V0)` col fit di `caduta_finestre`. **K CIMA al centro** *(come S3)* e **K CIMA PESATO** *(il gradiente = la media della quinta colonna nella finestra)*, uno accanto all'altro; **la legge:** la media e lo scarto delle tre K su `[200, 2000]`, in `%` della media. **Nessuna soglia di passaggio:** e' una misura, non un sigillo.
- **IL CASO NOTO** *(`legge_fondo_v2.py noto`, prima delle corse)*:
  - (a) **la V2 `x1` su 1c, `100` tick:** le prime quattro colonne coincidono **AL BIT** con la serie di 1c *(`M1658/c1/caduta_V2`, `k <= 100`)*;
  - (b) **DEVE FALLIRE:** le stesse colonne contro la serie `x2` di 1c;
  - (c) **`<dN/dy>/centro` a `k 0` uguale a quello di B0 sullo stesso stato** *(`0.95481`, `k_forma.txt`)* entro `5e-6`, cioe' l'arrotondamento della quinta cifra.
- **LA CODA:** quattro voci a priorita' `1` *(`M1330B3_V0`, `M1330B3_x0.5`, `M1330B3_x1.0`, `M1330B3_x2.0`)*, **scritte a lanciatore fermo, dopo la lettura della v3b, e solo se la v3b passa.** Se non passa, B3 non parte.
- **LE PREVISIONI, mie, scritte prima:**
  - **le tre K PESATE piu' vicine fra loro delle tre K al centro** *(`55%`)*;
  - **la K PESATA a `x1` entro il `10%` di K CIMA di 1c a `x1`** *(`0.7707`)*: `40%`, perche' `m*` di 1c non e' quello dell'oggetto.

## 3-octies. [M1932] IL QUARTO GIRO DELLA v3b, E B3 COL RESPIRO RESIDUO *(DECISIONE DI LUCA, `19:32`; scritta PRIMA dei numeri, dopo gli script; `19:37:31` l'ultimo `date`)*

- **`git log --all --fixed-strings --grep "[M1932"`: vuoto** *(`19:36:48`)*.
- **Di Luca:**
  - un quarto giro della v3b dallo stato finale del giro 3, `6000` tick, `w` ogni `100`, lo stesso metodo; il criterio resta `< 5%`;
  - **se passa:** B3 parte da solo, le quattro cadute;
  - **fra `5%` e `8%`:** B3 parte lo stesso, **e il respiro residuo si dichiara nel referto** *(«col gradiente pesato un respiro del `5%` su `w` sposta K dello `0.5%`, sotto l'incertezza»)*;
  - **oltre l'`8%`: FERMO.**
- **LE MIE SCELTE, dichiarate prima:**
  1. **«lo stato finale del giro 3»** = `puntofisso_v3b/giro_3/stato_006000.npz` *(`w 10.70`)*. Luca ha usato la stessa frase in [M1735] per lo stato a `k 6000` *(«w 12.6»)*. **Non** `partenza_giro_4.npz`, che e' la media del giro 3 su `[0, 500]`. **Se Luca intendeva quella, questa corsa non e' quella che ha chiesto.**
  2. **le fasce:** `r < 0.05` PASSA; **`0.05 <= r <= 0.08`** RESIDUO *(i bordi compresi)*; `r > 0.08` FERMO;
  3. **l'oggetto di B3** e' la partenza del giro 4, come nella sez. `3-septies` *(«lo stato la cui evoluzione ha passato il criterio»)*. `legge_fondo_v2.py` ha gia' girato il suo caso noto e non si riscrive: **`legge_fondo_v2b.py`** cambia in memoria solo `OGGETTO_B3`, e la sua lettura stampa **prima il respiro del giro 4 e la sua fascia**, poi la lettura di `legge_fondo_v2` cosi' com'e', nel referto `legge_fondo_v2.txt`.
- **Il codice:** `fondo_puntofisso_v3b4.py` fa un giro, il `4`: `fondo_puntofisso.giro` col `minimi_v3b`, nella cartella della v3b *(`giro_4`)*.
- **IL CASO NOTO** *(`fondo_puntofisso_v3b4.py noto`)*:
  - (a) il giro 3 della v3b *(`0.0582`)* cade in RESIDUO;
  - (b) i bordi: `0.0499` PASSA; `0.05` e `0.08` RESIDUO; `0.0801` e `0.3079` FERMO;
  - (c) DEVE FALLIRE: `0.0801` in RESIDUO;
  - (d) lo sha1 della partenza coincide, e `giro_4` non esiste ancora.
  - **Il caso noto di B3 resta quello della sez. `3-septies`** *(3 su 3, `2a6304d8`)*: la macchina e' la stessa, cambia solo l'oggetto.
- **La coda:** `M1932_puntofisso_v3b4` a priorita' `1`, scritta a lanciatore fermo. **Le quattro voci di B3 entrano dopo la lettura del giro 4, a lanciatore fermo, e solo se il giro 4 non e' FERMO.**
- **LE PREVISIONI:**
  - **del guardiano:** il giro 4 sotto il `5%` *(`65%`)*; B3, K nella prima finestra fra `0.95` e `1.00` *(`70%`)*; K costante entro il `5%` su tutte le finestre *(`55%`)*;
  - **mie:** il giro 4 sotto il `5%`: `45%`; sotto l'`8%`: `80%`. Le previsioni su B3 restano quelle della sez. `3-septies`.

## 3-nonies. [M2045] LE LETTURE SULLE CADUTE DI B3 *(DECISIONE DI LUCA, `20:45`; solo letture, nessuna corsa; scritta dopo lo script e PRIMA dei numeri)*

- **`git log --all --fixed-strings --grep "[M2045"`: vuoto** *(`20:43:02`)*.
- **UNA PREMESSA CHE CAMBIA IL MANDATO, dichiarata:** **le cadute di B3 non hanno salvato gli stati.** Salvano solo la serie ogni `MC.OGNI` tick: il tick, il baricentro `x` e `y`, la massa, e la quinta colonna `<dN/dy>` **pesata col `rho` di quel tick**. La quinta colonna **e' gia' il gradiente alla posizione raggiunta**, quindi le quattro letture si fanno dalle serie. Lo script e' `legge_fondo_v2c.py`, il referto `legge_fondo_v2c.txt`.
- **Di Luca, e le mie scelte, dichiarate prima:**
  - **(i)** `<dN/dy>(k)/<dN/dy>(0)` ogni `400` tick, con lo spostamento `y(k) - y(0)`. **La parte del calo spiegata** = il calo del gradiente medio dalla prima all'ultima finestra di `600`, diviso il calo di K CIMA al centro nelle stesse finestre *(la K al centro non contiene il gradiente: e' il calo da spiegare)*;
  - **(ii)** K PESATA per finestra *(`[200, 800]`, `[800, 1400]`, `[1400, 2000]`)* contro **`v` della finestra = `(y(k1) - y(k0))/(k1 - k0)` della V2 meno quella della V0**. Le tre scale insieme, ordinate per `v`;
  - **(iii)** `m*(p)` = **`dp/dv` letto da `ep_fondo.txt`** *(le righe «dp/dv contro gamma^3 m», il file committato pulito: si verifica)*, **interpolato linearmente** a `p = m*(0) v`. **`m*(0)` = `dp/dv` al primo punto** *(`p 0.0099`)*; sotto quel `p`, `m*(p) = m*(0)`. **`R = m*(0)/m*(p)`, e `K/R`.** La curva `dp/dv` e' quella del calcio lungo `u` sull'oggetto di E(p): **la uso per la caduta in `y` sull'oggetto del giro 4**, e lo dichiaro;
  - **(iv)** `a(V0)` per finestra *(e su `[200, 2000]`)*, col fit di `caduta_finestre`, accanto a `v(V0)`.
- **IL CASO NOTO:** (a) la K PESATA `x1 [200, 800]` ridà `1.0014` di `legge_fondo_v2.txt`; (b) **DEVE FALLIRE:** la stessa col gradiente al centro; (c) `dp/dv` al primo punto e' `19.036` *(`ep_fondo.txt`)*.
- **LE PREVISIONI:**
  - **del guardiano:** il gradiente raggiunto spiega meno del `5%` del calo *(`65%`)*; K(v) riscalato con `m*(p)` entro il `10%` di `1` su tutte le finestre *(`45%`)*;
  - **mie:** il gradiente spiega meno del `5%` *(`85%`)*, perche' `<dN/dy>/centro` resta fra `0.937` e `0.942` in tutte le finestre. **Il riscalamento non aiuta** *(`75%`)*: in `ep_fondo.txt` `dp/dv` scende con `p` *(da `19.04` a `0.0099` a `16.98` a `0.2985`)*, quindi `R > 1` e `K/R < K`: **il calo peggiora.**

## 3-decies. [M2210] IL FRENO CHE SEGUE IL TEMPO: RAMPA E NORMA LONTANA *(DECISIONE DI LUCA, `22:10`; scritta dopo lo script e PRIMA dei numeri)*

- **`git log --all --fixed-strings --grep "[M2210"`: vuoto** *(`22:09:02`)*.
- **Di Luca:** dall'oggetto del giro 4 *(`puntofisso_v3b/giro_3/stato_006000.npz`, respiro `6.77%`)*, gradiente `x1`, `2000` tick, **tre corse**, **gli stati ogni `250`** *(il caso noto: `stato_000250.npz` esiste a fine corsa)*:
  - **(r1)** V2 a **GRADINO** come B3;
  - **(r2)** V2 a **RAMPA**: **`N(t) = 1 + (N - 1) min(t/500, 1)`**;
  - **(r3)** V0.
  - Le letture: (i) K per finestra di `600` di r1 e r2, col gradiente pesato, e **per r2 il fit su `[700, 2000]`, dopo la rampa**; (ii) la norma di `psi` fuori da un raggio di `25` nodi dal baricentro, per stato, r1, r2, r3 una accanto all'altra; (iii) `|psi|` massimo fuori dal raggio, per stato. Il referto: `legge_fondo_v3.txt`. Tetto `10`, un filo *(il lanciatore mette gia' `OMP/MKL/OPENBLAS_NUM_THREADS = 1`)*, CPU `< 90%`.
- **LA RAMPA, dichiarata:** `N` entra nel tick solo in `cs = s N` *(`caduta_segno_v2.tick_var`, `cs_N` vero; la fase (a) ha `segno 0`)*. Al tick `kk = 1..2000` si passa **`N(kk) = 1 + (N - 1) min(kk/500, 1)`**, con `N` il campo di `campo_N` a gradiente `x1`. **La formula si usa letterale:** da `kk 500` in poi vale `1 + (N - 1)`, che puo' differire da `N` di un ulp. Prima di `kk 500` anche il gradiente cresce, quindi **il fit di r2 si fa dopo la rampa**: `[700, 2000]`, e le finestre di `600` dentro, `[800, 1400]` e `[1400, 2000]`, confrontabili con quelle di r1.
- **LE MIE SCELTE, dichiarate prima:**
  1. **gli stati:** `k 0` e ogni `250` fino a `2000` *(`9` per corsa)*, in `M1330/b3v3/<r1_gradino|r2_rampa|r3_V0>/`, con lo sha1;
  2. **il ciclo** e' `fondo_1c.ciclo` riga per riga, con `N` che puo' cambiare a ogni tick. La V0 ha `N = 1` e `cs_N` falso, come `fondo_1c.COLL["V0"]`;
  3. **(i)** la V0 da sottrarre e' r3. La quinta colonna e' `<dN/dy>` pesato **col gradiente pieno**, anche per r2: dopo la rampa e' il gradiente vero;
  4. **(ii) il raggio:** la distanza di ogni nodo dal baricentro *(di quello stato)* nel piano, coi `dxy` di `FS.carica` *(gli scarti a immagine minima dal centro di partenza)*. «25 nodi» = `25` passi di reticolo. **La norma lontana** = `somma rho` fuori dal raggio / `somma rho`;
  5. **(iii)** `|psi|` per nodo = `sqrt(rho)`; il massimo fuori dal raggio.
- **IL CASO NOTO** *(`legge_fondo_v3.py noto`, `100` tick, prima delle corse)*: (a) il gradino = B3 `x1` **AL BIT**, cinque colonne; (b) **DEVE FALLIRE:** la rampa = B3 `x1`; (c) la V0 = B3 V0 **AL BIT**; (d) `N_di` ai bordi della rampa. **E A FINE CORSA** *(nella lettura)*: `stato_000250.npz` esiste *(Luca)*; **r1 = B3 `x1` AL BIT su tutta la serie** e r3 = B3 V0 *(salvare gli stati non tocca la dinamica)*.
- **LE PREVISIONI:**
  - **del guardiano:** la norma lontana cresce nel tempo in r1 e non in r3 *(`55%`)*; con la rampa K su `[1400, 2000]` resta sopra `0.90` *(`45%`)*; se la norma lontana NON cresce, il freno non e' il toro e resta aperto *(`35%`)*;
  - **mie:** con la rampa K su `[1400, 2000]` sopra `0.90`: `30%`. La norma lontana cresce in r1 piu' che in r3: `50%`.

## 3-undecies. [M2245] IL VENTO DEL VUOTO *(DECISIONE DI LUCA, `22:49`; solo letture e un'animazione, nessuna corsa; scritta dopo lo script di A e PRIMA dei numeri)*

- **`git log --all --fixed-strings --grep "[M2245"`: vuoto** *(`22:49:55`)*.
- **L'ipotesi** *(del guardiano, `22:40`)*: in V2 tutto scala con `N`, e il vuoto `phi` ha una frequenza propria. Nel gradiente accumula un impulso che cresce col tempo: il vuoto cade, e la caduta misurata e' rispetto alla scatola, non al vuoto.
- **A, le definizioni** *(Luca: «dichiararne la definizione»)*. **Una corrente di `phi` gia' in uso nel codice non c'e':** `anemometro.J_di` e' la corrente della MATERIA *(un mezzo passo di trasporto su `psi`)*. **La mia:**
  - per nodo `rho_phi = somma |phi_h|^2` sulle sei mezze-spighe;
  - **`theta(k)`** = la fase di `Z = somma conj(phi_h(0)) phi_h(k)`, **la fase acquistata dallo stato `k 0` della stessa corsa.** Cosi' non serve il tick assoluto di `bordo.c_di` *(il nodo di [M2210-r4])*;
  - **`d theta/dy`** = `arg(conj(Z_giu) Z_su)/(2 sqrt3)`, coi nodi `(m1 - 1, m2 + 2)` e `(m1 + 1, m2 - 2)`, **esattamente a `+- sqrt3` lungo `y`** *(`x = m1 + m2/2`, `y = m2 sqrt3/2`)*;
  - **`J_phi = rho_phi d theta/dy`**, la corrente di Noether di un campo complesso, **mediata sui nodi a distanza `> 25` dal baricentro di `rho_psi`** *(i `dxy` di `FS.carica`)*;
  - **`v_phi = <J_phi>/<rho_phi>`** sugli stessi nodi. **La riserva:** ha le dimensioni di un numero d'onda, non di una velocita' *(la velocita' vorrebbe la dispersione del vuoto, che non ho)*. Il rapporto con `v` dell'oggetto *(`v - v(V0)`, la differenza centrata a `10` tick della serie)* si stampa come chiesto, con questa riserva;
  - **accanto, un riferimento** *(numeri, non giudizio)*: `omega k_eff <dN/dy>` sugli stessi nodi, cioe' la fase che si accumulerebbe **se la frequenza del vuoto scalasse come `N`**. `omega 0.471239` e' quello della scena; `k_eff = k` a gradino, `somma min(t/500, 1)` con la rampa, `0` in V0.
- **(A3)** il massimo di `sqrt(rho_psi)` fuori dal raggio: il nodo, `d`, la direzione dal baricentro, `y - y_c`, per stato, in r1, r2 e r3. **(A4)** la fase lungo `y` per riga `m2` *(l'arg della somma sulla riga)*, **assoluta** *(`somma phi_h`)* **e acquistata da `k 0`**, a `k 0`, `1000`, `2000` in r1 e r3.
- **I CASI NOTI:**
  - (A1) `J_phi` di `k 0` rispetto a se stesso = `0` **al bit**;
  - (A1) una fase uniforme `0.3`: `|d theta/dy| < 1e-12`. **Non al bit, e lo dico:** `0.3` passa da coseno e seno arrotondati;
  - (A1) **DEVE FALLIRE lo zero:** una rampa di fase `q y` *(3 giri su `L_y`)* ridà `q` entro `1e-9`;
  - (A4) `phi` di `k 0` uguale al bit nelle tre corse.
- **IL CRITERIO PER B, fissato qui:** **«il vuoto scorre»** se in r1 `J - J(V0)`, contro `k` *(`k 250..2000`)*, ha **una pendenza a piu' di `3` sigma e `R^2 > 0.9`**. Altrimenti B non si fa, e lo dico.
- **LE PREVISIONI:**
  - **del guardiano:** A1 `J_phi` lontano cresce linearmente a gradino e non in V0 *(`50%`)*; A2 `v_phi` a `k 2000` fra il `10%` e il `50%` di `v` *(`35%`)*; A3 il massimo vicino a `y_c +- L_y/4` *(`40%`)*; B *(`30%`)*; C *(`50%`, `35%`)*;
  - **mie:** A1 `J - J(V0)` cresce linearmente in r1 *(`60%`)*, **e segue il riferimento `omega k <dN/dy>` entro un fattore `2`** *(`40%`)*; A3 il massimo vicino a `y_c +- L_y/4` *(`30%`)*.


## 3-duodecies. [M2245-B] IL VUOTO SI AMMASSA? *(A dice che il vuoto scorre, per il criterio della sez. `3-undecies`: B si fa; scritta dopo lo script e PRIMA dei numeri)*

- **UNA PREMESSA CHE NON REGGE, dichiarata:** le corse nominate *(`caduta_libera`, le tenute di [M1631] o [M0326])* **non hanno chi VERO**. `caduta_libera` ha `chi` **imposto e fermo** *(negli stati c'e' `N`, non `pi`)*; le tenute di [M1631] **non hanno `chi`** negli stati. **Fra le `112` cartelle con `stato_000250.npz`, `chi` col suo momento `pi` c'e' solo in `CHI/due_corpi/*`** *(`13` stati, `k 0..3000`)* **e in `CHI/triangolo/*`** *(fino a `k 35000`)*.
- **LE CORSE SCELTE, dichiarate:**
  - **`CHI/due_corpi/F-on` contro `F-off`** *([M0417]: due mattoni a `39` nodi, in fase; `chi` acceso contro `kappa = 0`)*: **chi vero, con il suo controllo**;
  - **accanto, chi imposto:** `CHI/caduta/V2` e `V0` *(`caduta_libera`, nominata da Luca)*;
  - **i triangoli no:** tre corpi e `35000` tick, fuori dalla misura di `2000` tick.
- **La misura:** per stato, `rho_phi = somma |phi_h|^2` per nodo, mediata sugli anelli `[0, 8)`, `[8, 16)`, `[16, 32)` attorno al baricentro di `rho_psi` *(`toro.centro`, `toro.scarti`)*. **Con due corpi:** dal centro della coppia, ogni corpo nella sua meta' *(il segno di `dx`)*, il suo baricentro, e gli anelli solo dentro la sua meta'. Accanto, la variazione da `k 0` in `%`, e la somma totale di `rho_phi`.
- **I casi noti:** (a) `rho_phi` costante: le tre medie al bit; (b) **DEVE FALLIRE la costanza:** `rho_phi = d` da' tre medie crescenti.
- **Le previsioni:** del guardiano, `rho_phi` in `[0, 8)` cresce di piu' dell'`1%` in `2000` tick con chi vero *(`30%`)*; **mia:** `20%`.


## 3-terdecies. [M2245-C] L'ANIMAZIONE DEL VENTO DEL VUOTO *(scritta dopo lo script e PRIMA del filmato)*

- **Come `anima_tenuta.py`:** `10` passi per intervallo, `10 fps`, l'mp4 nel repo sotto i `20 MB`, i png in `E:/soliton_simulator/controllo/M2245/png/`. **Tre colonne** *(r1, r2, r3)*, **quattro righe**: `rho_psi` col cerchio di raggio `25`; `rho_phi - rho_phi(k 0)` con la scala simmetrica sul massimo di tutta la serie; `J_phi` a frecce, una ogni `4` nodi, la scala fissa, il colore col segno di `J_y`; la fase lungo `y`. **Sotto,** `w(k)` e K per finestra.
- **LE MIE SCELTE, dichiarate:**
  - la finestra di raggio `40` attorno al centro di partenza, come `anima_tenuta`;
  - **`J_x`** coi nodi `(m1 +- 1, m2)`, a `+-1` esatti lungo `x`; `J_y` come in `vento_vuoto_v2`;
  - «una freccia ogni `4` nodi» = `m1` e `m2` multipli di `4`;
  - **la riga 4** mostra la fase assoluta *(come chiesto)*, quella di `k 0` in grigio, **e in piu' la fase acquistata, tratteggiata**. **Non si interpola:** gli angoli attraversano `+-pi`;
  - `w(k)` con `torneo_tenuta.misura` sugli stati, K letta da `legge_fondo_v3.txt`.
- **Il caso noto:** a `k 0` le quattro righe sono uguali al bit nelle tre colonne; **e l'mp4 sotto i `20 MB`.** L'uscita stampata va in `doc/referti_l2/anima_vento.txt`.
- **Le previsioni:** del guardiano, a gradino le frecce lontane crescono nel tempo tutte nello stesso verso *(`50%`)*; un accumulo di `rho_phi` vicino a `y_c +- L_y/4` *(`35%`)*. **Mie:** le frecce crescono col tempo ma **cambiano verso con `y`**, seguendo `dN/dy` *(`70%`, da A4: la fase acquistata e' una sinusoide in `y`)*; nessun accumulo *(`75%`, da B)*.


## 3-quattuordecies. [M2330] IL MODELLO INTERO: DUE OGGETTI AL FONDO A K CON CHI VERO *(DECISIONE DI LUCA, `23:30`; scritta dopo lo script delle corse e PRIMA dei numeri)*

- **`git log --all --fixed-strings --grep "[M2330"`: vuoto** *(`23:28:50`)*.
- **Le corse** *(Luca)*: `L 162`, il toro, `g_e = 0`, `6000` tick, gli stati ogni `250`; **(d1)** due oggetti del punto fisso, chi VERO acceso; **(d2)** gli stessi, chi spento; **(d3)** un oggetto solo, chi vero. Lo script e' `due_corpi_fondo.py`.
- **LE MIE SCELTE, dichiarate prima** *(il mandato non le fissa)*:
  1. **L'oggetto:** `puntofisso_v3b/giro_3/stato_006000.npz`, la partenza del giro 4 *(come B3 e [M2210])*.
  2. **«A distanza 40 nodi lungo y»:** la traslazione `(dm1, dm2) = (-24, +48)`, cioe' **`+41.57` lungo `y` e `0` lungo `x`**. Le componenti devono essere multipli di `3`, per il disegno di fase di K *(`mattone.incolla`)*: `40` esatti non si possono, `(-21, +42)` darebbe `36.37`.
  3. **La materia per SOMMA, il vuoto per PRODOTTO** *(come `gravita_due_corpi.prepara_coppia`)*: `phi = phi_A phi_B / phi_fondo`. **Il fondo** e' `a phi_v`, con `a` il fit complesso di `phi_A` su `phi_v` sui nodi a distanza `> 45` dall'oggetto: **non serve il tick assoluto.** Il residuo del fit si stampa.
  4. **I campi:** `porto.campi` *(`A = 0`, `E` da Gauss)*, **in tutte e tre le corse**, come la coppia di [M0417]. Cosi' d3 e' confrontabile con d1.
  5. **`chi`:** il tick `chi_tick_v2.tick_chi_v2` *(con la fase (a): `cs = s N` e `e^{i e0 (N - 1)/2}`, **la variante V1, non la V2 della legge del fondo**: lo dico)*. I parametri sono quelli di `gravita_due_corpi.parametri`: **si verifica che `kappa`, `f`, `c2`, `m2`, `s`, `e0` siano uguali a quelli di `CHI/due_corpi/F-on`** *(`kappa 2.5289e-04`, `f 0.06`, `c2 0.25`, `m2 1e-04`, `s 0.15`, `e0 0.4767`)*. **`c0 = kappa m0` della configurazione** *(Luca nomina `kappa`, `f`, la portata; `c0` no)*. Off: `kappa = 0`, lo stesso `c0`. `chi` parte dal profilo statico di «on».
  6. **Il tick dentro la forma `L-1` del nucleo** *(come `fondo_1c.ciclo`: l'oggetto al fondo esiste in quella forma)*.
  7. **La serie ogni `10` tick:** per corpo il baricentro e la massa *(i corpi separati dal segno di `dy` dal centro della coppia a `k 0`)*, `max |chi|`; **`omega` per tick per corpo** sulla meta' del corpo.
- **I CASI NOTI** *(`due_corpi_fondo.py noto`)*:
  - **(K1)** `kappa 0`, i campi dello stato, `100` tick nella forma `L-1` = **la tenuta del giro 4 a `k 100` AL BIT** *(il tick di chi con `N = 1` e' il tick U)*;
  - **(K1-on)** lo stesso con chi acceso: **l'esito si dichiara** *(Luca: «se chi non cambia niente in 100 tick»)*;
  - **(K2)** d2 a `k 0` = d1 a `k 0` **AL BIT** *(l'impronta, chi compreso)*;
  - **(T)** le masse dei due oggetti uguali al bit; la traslazione e la sua inversa = l'identita'; **DEVE FALLIRE:** `rho` della coppia simmetrico per la traslazione.
  - **Le letture** *(i)-(v)* e l'animazione: **uno script a parte, a corse finite**, con la sua carta.
- **LE PREVISIONI:**
  - **del guardiano:** (i) in d1 si avvicinano e in d2 no *(`65%`)*; l'accelerazione cala nel tempo *(`50%`)*. (ii) J radiale verso l'oggetto cresce *(`55%`)*, meno di un decimo del seno *(`60%`)*. (iii) `rho_phi [8, 16)` cambia meno dell'`1%` *(`60%`)*. (iv) la profondita' di chi cambia meno del `5%` *(`55%`)*. (v) il respiro sotto il `10%` *(`70%`)*;
  - **mie:** (i) VERSO in d1 *(`55%`)*; (v) sotto il `10%` *(`50%`)*: con due corpi e la fase (a) l'oggetto non e' piu' al suo punto fisso.


## 3-quindecies. [M2330] LE LETTURE DEL MODELLO INTERO *(scritta dopo lo script e PRIMA dei numeri; le corse chiuse alle `00:51`)*

- **Lo script:** `due_corpi_lettura.py`, il referto **`due_corpi_fondo.txt`**. Solo letture sugli stati ogni `250` e sulle serie ogni `10` tick.
- **LE MIE SCELTE, dichiarate prima:**
  - **(i)** `d(k)` dalla serie *(i baricentri dei due corpi nel riferimento della corsa)*. Il fit `d = c0 + c1 k + a k^2/2` per finestra di `1000` e su `[0, 6000]`. **`a < 0` = si avvicinano.** Accanto, `a(d1) - a(d2)` con la sua barra;
  - **(ii)** `J_phi` come in `vento_vuoto_v2` *(la fase acquistata da `k 0` della stessa corsa)*, e `J_x` coi nodi a `+-1` lungo `x`. **La componente radiale** dal baricentro del corpo, mediata sugli anelli `[8, 16)` e `[16, 32)` dentro la meta' del corpo. **Negativa = verso l'oggetto**;
  - **(iii)** `rho_phi` sugli stessi anelli, con la variazione da `k 0`;
  - **(iv)** `chi` sugli anelli `[0, 4)`, `[4, 8)`, `[8, 16)`, `[16, 32)`; **la profondita' = la media su `[0, 4)`**, con la variazione da `k 0`;
  - **(v)** `w` di ogni corpo = **il raggio quadratico medio di `rho_psi` nella sua meta'** *(non `torneo_tenuta.misura`, che vede un oggetto solo)*; `omega` per tick dalla serie, la media per finestra di `250`; il respiro = `(w_max - w_min)/w_medio` sui `25` stati, accanto al `10%` di Luca.
- **I CASI NOTI:**
  - d2 a `k 0` = d1 a `k 0` al bit *(Luca)*;
  - il baricentro di `k 0` riletto dallo stato = la serie al bit;
  - `J` radiale di `k 0` = `0` al bit;
  - **il segno:** una fase uscente `q r` ridà `J_r = + rho q` entro il `5%`, e **DEVE FALLIRE** che dia un radiale negativo.
- **Le previsioni** sono quelle della sez. `3-quattuordecies`, del guardiano e mie.


## 3-sedecies. [M0137] DUE CORPI CON CHI IN EQUILIBRIO: IL PUNTO FISSO CON CHI ACCESO, POI LA COPPIA A 41.57 LUNGO y *(DECISIONE DI LUCA, `01:37`, arrivata dalla posta, `guardiano/posta/2026-11-25_0137_M0137.md`, `8b6efc0b`; scritta PRIMA del codice del punto fisso)*

- **`git log --all --fixed-strings --grep "[M0137"`:** solo il commit della posta *(`8b6efc0b`)*: niente e' gia' fatto.
- **PEZZO 0, A COSTO ZERO** *(`chi_d3.py`, `chi_d3.txt`)*:
  - **d3** *(un oggetto, chi on)*: `max|chi|` per finestra di `250` va da `69.9` *(`k 250`)* a `168.3`-`169.2` *(`k 1250`-`1500`)*, `52.5` *(`2750`)*, `170.5` *(`4000`)*, `107.9` *(`6000`)*; a `k 0` vale `10.615`;
  - **d1** *(due, chi on)*: lo stesso andamento, coi picchi a `221.5`-`222.4` *(`1250`-`1500`)* e `232.1` *(`4000`)*;
  - `w` *(`torneo_tenuta.misura`)* di d3: da `10.70` a `2.73` *(`k 1500`)*, poi fra `3` e `7.7`; `(max - min)/medio` `1.37`;
  - **IL TRANSITORIO E' DEL GRADINO DI CHI SULL'OGGETTO SOLO, NON DELL'INCONTRO.**
- **LE SCELTE DI LUCA (01:37):**
  - **A.** la coppia a `(dm1, dm2) = (+24, +48)`: `41.57` lungo `y`, `0` lungo `x`. **Caso noto:** `|x_B - x_A| < 1e-9`, `|y_B - y_A| = 48 sqrt3/2`;
  - **B.** chi parte in equilibrio col **punto fisso con chi acceso** *(un oggetto, chi dinamico)*, cioe' lo schema del giro 4 con `tick_chi_v2` dentro la forma `L-1`:
    - la media di `psi` sul periodo, con la fase riallineata, e la riproiezione su `Q_K`;
    - **chi NON si media:** si riparte da `(psi, chi, pi)` di fine giro;
    - **la coppia dallo stato finale:** materia per SOMMA, vuoto per PRODOTTO, **chi per SOMMA** *(`chi_A + chi_B - chi_fondo`, `chi_fondo` = la media di chi a distanza `> 45`)*;
  - **C.** **«equilibrio»** = `max|chi|` cambia meno del `10%` fra il giro `n` e il giro `n + 1`, **e** il respiro di `w` sul giro `< 10%`. Al massimo `3` giri da `6000` tick. **La riserva, se C non passa:** la rampa lineare di `kappa` in `1500` tick sulla coppia, dichiarata qui prima.
- **LE MIE SCELTE, dichiarate prima** *(il mandato non le fissa)*:
  1. **il giro** *(`fondo_puntofisso_chi.py`)*: `6000` tick di `tick_chi_v2` *(kappa acceso)* nella forma `L-1`, col nucleo preso prima della scena e `U` riscritto dopo i parametri *(le due lezioni di `due_corpi_fondo_v2`/`v3`)*; `C.residuo` ogni `OGNI_GAUSS`;
  2. **i parametri di chi** si calcolano **una volta, al giro 1**, sull'oggetto del giro 4 *(`gravita_due_corpi.parametri`, `c0 = kappa m0`)*, **e restano gli stessi nei giri dopo** *(scritti nel `giro.json`)*;
  3. **ogni `100` tick, in memoria:** `w` con la formula di `torneo_tenuta.misura` *(dalla `rho` lisciata)*, `max|chi|`, la somma progressiva di `psi e^{i theta}`. **Gli stati ogni `250`** *(Luca)*;
  4. **il periodo e la finestra della media:** il metodo della v3b *(sez. `3-sexies`: la lisciata di `500` tick = `5` campioni da `100`; `P = 2 (k_min - k_max)`; la finestra accorciata e dichiarata; senza minimi FERMO)*;
  5. **la nuova partenza:** `psi` mediato, riproiettato su `Q_K` e riportato alla massa della partenza della v1 *(come tutti i punti fissi)*. **Le altre chiavi, i campi, `chi`, `pi` e `Theta` dallo stato a `k 6000`** *(«di fine giro»)*;
  6. **C, in numeri:** `max|chi|` del giro = il massimo sui `61` campioni ogni `100`; il respiro = `(w_max - w_min)/w_medio` sugli stessi campioni. **C si valuta dopo il giro `2` e dopo il giro `3`:** `|maxchi(n+1)/maxchi(n) - 1| < 0.10` **e** il respiro del giro `n + 1` `< 0.10`. **Ci si ferma al primo giro che passa;**
  7. **la profondita' del pozzo:** la media di chi sull'anello `[0, 4)` attorno al baricentro;
  8. **un giro = una voce in coda:** il giro dopo entra a lanciatore fermo, a giro chiuso e letto. Cosi' ogni giro ha il suo referto e il suo commit.
- **I CASI NOTI** *(`fondo_puntofisso_chi.py noto`)*:
  - **(K1)** `kappa 0`, `100` tick = la tenuta del giro 4 al bit;
  - **(K2) «chi_statico riprodotto con `dt 0`», l'equivalente dichiarato:** la forza di chi *(`chi_tick.forza`)* sul profilo statico, contro la forza su `chi = 0`. **DEVE:** il massimo e' almeno `100` volte piu' piccolo. **E' un controllo di equilibrio, non al bit:** il profilo statico e' la soluzione del problema lineare, e la forza contiene `N` non lineare;
  - **(K3)** la riproiezione su `Q_K` conserva la norma *(riporta alla massa)* entro `1e-12`.
- **LE MISURE** *(`fondo_puntofisso_chi.txt`, dopo ogni giro)*: `max|chi|` e `w` per finestra di `500`, la profondita' del pozzo, `omega` del corpo, il respiro, il criterio C.
- **DOPO** *(pezzi 4 e 5)*: `due_corpi_fondo_v4.py` con la coppia da A e dallo stato finale, i casi noti G, K2, T *(le masse entro `1e-9`)*; d1', d2', d3' a `6000` tick; le letture con `due_corpi_lettura_v2` *(i nodi giusti)*, `a` per finestra di `500`. **Il controllo negativo prima del verdetto:** `d(k)` di d2' fermo entro `0.5` nodi.
- **LE PREVISIONI DEL GUARDIANO** *(dalla posta)*:
  - P1 *(`75%`)* in d3 chi oscilla come in d1: **SI'** *(il pezzo 0)*;
  - P2 *(`55%`)* il punto fisso con chi passa C entro 3 giri;
  - P3 *(`50%`)* la profondita' stazionaria fra `-100` e `-200`;
  - P4 *(`80%`)* con chi in equilibrio d1' si avvicina e d2' no;
  - P5 *(`60%`)* in d1' il vento radiale `[16, 32)` verso l'oggetto cresce ancora;
  - P6 *(`40%`)* il respiro di `w` in d1' sotto il `15%`.
- **LE MIE:** P2 `30%` *(il modo uniforme di chi ha un periodo di qualche migliaio di tick, e un giro di `6000` ne vede due)*; P4 `65%`.

- **Il pezzo 4, le scelte dichiarate prima** *(`due_corpi_fondo_v4.py`, scritto mentre gira il giro 1)*:
  - **lo stato di partenza** e' la nuova partenza del giro che passa C *(`psi` mediato, i campi, `chi`, `pi` da `k 6000`)*;
  - **`pi` per SOMMA come chi** *(`pi_A + pi_B - pi_fondo`)*, perche' Luca nomina chi e `pi` e' il suo momento;
  - **`theta_a` a zero:** e' un accumulatore che il tick non rilegge;
  - **i campi** `porto.campi` in tutte e tre *(come [M2330])*, quindi d3' a `k 0` non e' esattamente il punto fisso: ha `A = 0`;
  - **i parametri** sulla configurazione *(`c0 = kappa m0`, la regola di `gravita_due_corpi.parametri`)*: per la coppia `m0` e' quello della coppia;
  - **(G)** lo spostamento di ogni nodo per `(+24, +48)`: `|dx| < 1e-9`, `|dy - 48 sqrt3/2| < 1e-9`.

- **IL PEZZO 6, LA RISERVA, le scelte dichiarate prima** *(C non e' passato in tre giri: respiro `1.38`, `0.97`, `0.76`; `due_corpi_fondo_v5.py`, scritta prima dei numeri della riserva)*:
  - **«la rampa lineare di `kappa` in `1500` tick sulla coppia»:** la leggo come **l'accensione graduale.** La coppia parte dall'**oggetto del giro 4 SENZA chi** *(`chi = pi = 0`)*, e **`kappa` cresce come `min(t/1500, 1)`**;
  - **anche `c0` cresce con la stessa rampa**, perche' `c0 = kappa m0`: la sorgente media resta nulla a ogni tick;
  - l'altra lettura possibile *(la coppia dal punto fisso con chi del giro 3, `chi` gia' profondo, e la rampa solo sull'accoppiamento)* **la dico e non la faccio**;
  - il resto e' la v4: `(+24, +48)`, la materia per somma, il vuoto per prodotto, `porto.campi`, i parametri della configurazione, `theta_a` a zero;
  - **d2'** *(chi spento)* ha `kappa = 0` sempre; **d3'** e' un oggetto solo con la stessa rampa. Le uscite in `M0137/coppia_rampa/`;
  - **i casi noti:** G, T, K2 come la v4; **(R)** il fattore della rampa a `k 0`, `750`, `1500`, `6000` = `0`, `0.5`, `1`, `1` esatti.

- ### **[M0414] IL PUNTO FISSO ACCOPPIATO (psi, chi): LA CORREZIONE DI B** *(DECISIONE DI LUCA, `04:14`, arrivata dalla posta, `de84c53a`; letta alle `04:25`; scritta PRIMA del codice)*:
  - **`git log --all --fixed-strings --grep "[M0414"`:** solo il commit della posta.
  - **SOSTITUISCE il pezzo 3 e la riserva:** **la rampa di `kappa` NON si fa.** **Ma le tre corse della rampa** *(d1', d2', d3' in `M0137/coppia_rampa/`)* **erano gia' partite alle `04:20:19`**, dopo il mandato *(04:14)* e prima che lo leggessi *(04:25)*. **Ho provato a fermarle** *(i miei processi, dalla riga di comando)*: **il permesso e' stato negato.** Finiscono da sole; **i loro numeri non entrano in nessun referto di questo mandato.**
  - **I due errori del guardiano** *(ERRORI n.253, n.254, dichiarati da lui)*: (a) chi ripartiva col suo impulso `pi` di fine giro, che rimetteva in moto l'oscillazione a ogni giro; (b) il periodo dalla `w` lisciata dava finestre di `200` tick col massimo al bordo. **Il punto fisso non poteva convergere.**
  - **B'** *(Luca)*: il periodo `P` da `max|chi|(k)`, per finestra di `250`: la distanza fra due picchi consecutivi. Il picco e' un massimo locale con almeno `3` finestre in salita prima e `3` in discesa dopo. **Senza due picchi, `P = 2500` dichiarato.**
  - **B''** *(Luca)*: a fine giro si riparte da **`psi` medio sull'ultimo periodo `P`** *(la fase riallineata tick per tick, la riproiezione su `Q_K`, come il giro 4)*, **chi medio sullo stesso periodo, `pi = 0`**, e i campi `A`, `E` dallo stato di fine giro, col residuo di Gauss ricalcolato.
  - **C:** uguale a [M0137]. **D** *(Luca)*: se dopo `3` giri C non passa ma `max|chi|` e' fermo entro il `10%`, il respiro e' un modo normale del sistema: si misura **`Omega_b = 2 pi / P`** e la profondita' media del pozzo, **e i pezzi 4 e 5 partono comunque dallo stato** *(`psi` medio, chi medio, `pi = 0`)* **del giro 3.**
  - **LE MIE SCELTE, dichiarate prima:**
    1. **`max|chi|` si misura a ogni tick**; per finestra di `250` si tiene il massimo. **«Salita» e «discesa» sono strette:** `v[i-3] < v[i-2] < v[i-1] < v[i] > v[i+1] > v[i+2] > v[i+3]`;
    2. **«due picchi consecutivi» = gli ULTIMI due del giro**, perche' la media si fa sull'ultimo periodo. `P` e' la loro distanza in tick *(un multiplo di `250`)*. **La finestra della media e' `[6000 - P, 6000]`;**
    3. le somme progressive di `psi e^{i theta}` e di chi si tengono ogni `250`;
    4. **la partenza del giro 1:** lo stato di fine del giro 3 di [M0137] *(`M0137/puntofisso_chi/giro_3/stato_006000.npz`)*, **con `pi = 0`** *(come B'')*;
    5. **«col residuo di Gauss ricalcolato»:** all'inizio di ogni giro si ricalcola `C.residuo()` col nuovo `psi` e si stampa. **I campi non si correggono:** e' la lettura minima, dichiarata;
    6. `w` *(la formula di `torneo_tenuta.misura`)* ogni `100` tick, per il respiro; `omega` per tick; la profondita' *(chi medio su `[0, 4)`)* ogni `100`. **I parametri di chi sono quelli del giro 1 di [M0137]** *(`c0 -1.46341e-03`)*;
    7. **(K6) al bit** si puo' solo con valori di chi esatti nella somma: il caso noto usa **un chi costante a valori interi** *(somme di interi esatte fino a `2^53`)*. Lo dichiaro.
  - **I CASI NOTI** *(`fondo_puntofisso_chi_v2.py noto`)*: **(K1)** `kappa 0`, `100` tick = la tenuta del giro 4 al bit; **(K5)** una serie sintetica con due picchi a distanza `2500` da' `P 2500`, **e DEVE FALLIRE** una serie con un solo picco *(il ripiego `2500` dichiarato, non i due picchi)*; **(K6)** la media di un chi costante *(intero)* ridà lo stesso chi al bit, e `pi = 0`.
  - **LE PREVISIONI DEL GUARDIANO** *(dalla posta)*: P1 *(`70%`)* B' trova `P` fra `2300` e `2800` al giro 1; P2 *(`45%`)* C passa entro 3 giri; P3 *(`55%`)* se no, il respiro sotto il `50%` al giro 3; P4 *(`65%`)* `omega` fra `0.080` e `0.090`; P5 *(`60%`)* `max|chi|` del punto fisso fra `110` e `140`.
  - **LE MIE:** P1 `70%` *(i picchi del giro 2 di [M0137] stanno a `[500, 1000]`, `[3000, 3500]` e `[5500, 6000]`, cioe' a circa `2500` l'uno dall'altro)*; P2 `40%`.


## 3-septendecies. [M2034] LA RIPRESA: IL PIANO DI [M0925] *(DECISIONE DI LUCA, 2026-11-26 `20:34`, arrivata dalla posta, `3ec35629`; letta alle `20:35`; scritta PRIMA del codice)*

- **`git log --all --fixed-strings --grep "[M2034"`:** solo il commit della posta.
- **Il piano:** `doc/TODO_domani_2026-11-26.md` *(`b4df4f0f`)*, pezzi A, B, C su `lapse-u`; D sul ramo `mitosi`.
- **LE DECISIONI DI LUCA (20:34):**
  - **F.** la fase di `phi` fresco: **`phi = c(t) phi_v` al tick dello stato del giro 3**. **(V3)**, prima delle corse lunghe: d3' per `250` tick con `phi_v` a fase `0` e con `c(t) phi_v`; se `omega` medio differisce oltre `1e-6`, la fase conta e si dichiara. Si usa comunque `c(t) phi_v`;
  - **D1, si':** la provenienza della corsa MITOSI;
  - **D2, si':** nel vuoto puro il residuo di Gauss senza la normalizzazione a `rho`, dichiarato prima, e K4 rifatto. Le corse della mitosi partono DOPO d1', d2', d3'.
- **IL TICK `t` DELLO STATO DEL GIRO 3: la catena, dichiarata** *(lo stato non porta `t` nel meta)*. **La tenuta** `M1658/tenuta/L-1_proiezione_K/stato_003000.npz` ha nel meta `t0 = 60000`, `k = 3000`, cioe' **`t = 63000`**. Ogni giro dei punti fissi riparte col vuoto *(`phi`)* dello stato a un `k` noto:
  - **v2** *(M1540)*: dallo stato a `k_b` della finestra *(`fondo_puntofisso.giro`: le altre chiavi da `k_b`)*;
  - **v3b** *(M1748)*: lo stesso;
  - **il giro 4** *(M1932)*: e' la partenza, cioe' lo stato a `k 6000` del giro 3 della v3b;
  - **[M0137]** e **[M0414]**: dallo stato a `k 6000`.
  - **`t` si ricostruisce sommando, dai `giro.json` e dai `periodo_v3b.json`.** Lo script stampa la catena.
  - **IL CASO NOTO (V0), prima di usarlo:** su `PARTENZA_G4` la fase di `c(t)` ricostruita deve coincidere con la fase del fit complesso di [M2330] *(`a = +0.987699+0.156418i`, `arg a = 0.1571`)* **entro `0.05` rad**; e sulla tenuta *(`t 63000`)* la stessa cosa col suo fit. **Se non coincide, FERMO:** la catena e' sbagliata, oppure il vuoto non avanza come `c(t)`.
- **A, LA DIAGNOSI DEL VUOTO DEL GIRO 3** *(`vuoto_giro3.py`, letture su `partenza_giro_4.npz` di [M0414])*. **Le mie scelte:**
  - **il centro:** il baricentro di `rho_psi` *(`toro.centro`)*; gli anelli `[45, 60)`, `[60, 75)`, `[75, 90)`;
  - **`rho_phi`** = `somma |phi_h|^2` per nodo; **il rapporto** = la media sull'anello di `rho_phi` dello stato, divisa per la media di `rho_phi` di `phi_v` sullo stesso anello *(il modulo di `c(t)` e' `|tab_c[K]|`: lo stampo)*;
  - **`J_phi`** = `rho_phi grad theta`, con `theta` la fase di `somma conj(phi_v) phi` per nodo *(il riferimento e' il vuoto fresco: la sua fase costante non entra nel gradiente)*. **I nodi giusti:** `(m1 +- 1, m2)` per `x`, `(m1 +- 1, m2 +- 2)` per `y` *(`A2 = (-1/2, sqrt3/2)`)*. **Le componenti radiale e tangenziale** dal centro, la media sull'anello; **negativo = verso l'oggetto**;
  - **`chi(d)`:** la media per anello, e anche per `[0, 15)`, `[15, 30)`, `[30, 45)`;
  - **(V1)** sul vuoto fresco *(`phi = phi_v`)*: il rapporto `1` e la corrente `0` entro `1e-9`. **E DEVE FALLIRE:** una fase `q y` aggiunta da' una corrente non nulla;
  - il referto `doc/referti_l2/vuoto_giro3.txt`.
- **B, LA COPPIA** *(`due_corpi_fondo_v6.py`)*: la v4, con **`phi = c(t) phi_v` fresco** *(F)*, **`psi` e chi dal giro 3** *(`psi_A + psi_B`, `chi_A + chi_B - chi_fondo`, `pi = 0`)*, i campi da Gauss *(`porto.campi`)*. I casi noti: G, T, K2; **(V2)** il vuoto composto a `k 0` e' `c(t) phi_v` al bit a `d > 45` da entrambi *(e dappertutto: `phi` fresco non porta oggetti)*; **(V0)**; **(V3)**.
- **D, LA MITOSI** *(ramo `mitosi`)*: D1 a costo zero; D2 dichiarato nella `doc/CARTA_mitosi.md` prima di rifare K4.


## 3-duodevicies. [M2048] chi CONTRO phi: IL LAPSE LO PORTA GIA' IL VUOTO? *(DECISIONE DI LUCA, 2026-11-26 `20:48`, arrivata dalla posta, `cd581122`; letta alle `21:04`; scritta PRIMA del codice)*

- **`git log --all --fixed-strings --grep "[M2048"`:** solo il commit della posta. **Una lettura a costo zero, mentre gira B di [M2034]**, senza toccarla.
- **LE SCELTE DI LUCA:**
  - **S1.** un tick dallo stato *(`M0414/puntofisso_accoppiato/giro_3/partenza_giro_4.npz`, sha1 `bee0464d6d2e`)*, chi acceso, `tick_chi_v2`, come il giro;
  - **S2.** per nodo le coppie `(chi, rho_phi)`, `(chi, omega_phi locale)`, `(chi, N)`, quest'ultima di controllo: Pearson e Spearman su tutti i nodi; la mediana di chi per decile; gli anelli `[0, 8)`, `[8, 16)`, `[16, 32)`, `[32, 45)`, `[45, 90)`;
  - **S3.** «phi lo porta» se `|Spearman| > 0.9` su tutti i nodi **e** la mediana per decile e' monotona; con due candidati vince il `|Spearman|` maggiore;
  - **S4.** il segno si dichiara.
- **LE MIE SCELTE, dichiarate prima:**
  - **`omega_phi` locale** `= -arg somma_{mezze-spighe del nodo} conj(phi(k)) phi(k+1)`, col prodotto in reali;
  - **il centro** e' il baricentro di `rho_psi`;
  - **la macchina** e' quella di `fondo_puntofisso_chi_v2`: i parametri del giro 1 di [M0137], i campi dallo stato, `U` riscritto, la forma `L-1`;
  - **«monotona»** = le differenze fra decili consecutivi tutte dello stesso segno, strette.
- **I CASI NOTI** *(`chi_contro_phi.py noto`)*:
  - **(K1)** il vuoto fresco *(`phi = phi_v`, `psi = 0`, chi `0`)*, un tick: `omega_phi` locale = `omega_phi` globale entro `1e-9` su tutti i nodi, e `rho_phi` uniforme entro `1e-9`;
  - **(K2)** Spearman`(chi, N) = -1` esatto;
  - **(K3), l'equivalente dichiarato:** il giro 3 non ha salvato lo stato al tick `1`, quindi il «primo tick del giro 3 al bit» non si puo' controllare. **Si fa con `250` tick dalla partenza del giro 3, contro `giro_3/stato_000250` al bit** *(`psi_h`, `phi_h`)*.
- **I referti:** `chi_contro_phi_noto.txt`, `chi_contro_phi.txt`, `chi_contro_phi.png`.
- **LE PREVISIONI DEL GUARDIANO:** P1 *(`55%`)* chi segue l'orologio locale meglio della densita'; P2 *(`60%`)* nessuno dei due passa S3; P3 *(`65%`)* il segno scomodo *(chi grande dove `rho_phi` e' piccolo)*; P4 *(`70%`)* in `[0, 8)` `|Spearman(chi, omega_phi)| > 0.8`.
- **LE MIE:** P2 `70%` *(fuori dall'oggetto chi e' quasi costante, circa `-22`, mentre `rho_phi` fluttua)*.


## 3-undevicies. [M2053] LE DUE LUCI: LA DISPERSIONE DELLE ONDE DEL VUOTO phi CONTRO QUELLA DELLA MATERIA psi *(DECISIONE DI LUCA, 2026-11-26 `20:53`, arrivata dalla posta, `5c9edcef`; letta alle `21:04`; scritta PRIMA del codice)*

- **`git log --all --fixed-strings --grep "[M2053"`:** solo il commit della posta. **Le corse vanno in coda DOPO quelle di B di [M2034] e dopo [M2048]** *(gia' chiusa)*.
- **LE SCELTE DI LUCA:**
  - **S1** `phi = phi_v (1 + eps e^{i q.x})`, `eps = 1e-3`, `q` lungo `x` per `n = 1, 2, 4, 8`, `q = 2 pi 2/L` lungo `y`; la linearita' a `eps = 5e-4` su UNA `q`. Corse da `1000` tick, `N = 1`, chi spento;
  - **S2** la componente di Fourier a `q` nel tempo: `omega(q) - omega_phi`, la velocita' di gruppo `c_phi`, il gap;
  - **S3** `c_psi` non si rimisura: da `ep_fondo.txt`;
  - **S4** «una luce sola» se `|c_phi - c_psi|/c_psi < 10%`; «anisotropo» se `c_phi` lungo `y` e lungo `x` differiscono oltre il `5%`.
- ### **DUE COSE DEL MANDATO CHE IL TORO NON PERMETTE, dichiarate:**
  1. **lungo `x` l'onda `e^{i q x}` e' periodica solo con `n` PARI.** Il toro e' `m1 -> m1 + L`, `m2 -> m2 + L`, con `x = m1 - m2/2`: il secondo passo sposta `x` di `-L/2`, e la fase cambia di `-pi n`. **`n = 1` lungo `x` non esiste.** **Uso `n = 2, 4, 8, 16`**: quattro valori, raddoppiando la lista;
  2. **lungo `y`** le onde ammesse sono `|q| = 2 pi n/L_y`, `L_y = L sqrt3/2`; uso `n = 2` *(`|q| = 0.0896`)*. **L'anisotropia** si confronta con la dispersione lungo `x` interpolata alla stessa `|q|`.
- **IL LATO:** `L = 162` *(il toro della scena del fondo)*.
- **LE MIE SCELTE, dichiarate prima:**
  - **la scena** e' quella del fondo: `psi = 0`, i campi `porto.campi` *(zero senza materia)*, il tick con `N = 1`, `cs_N` falso, `segno 0`, la forma `L-1`;
  - **`C.residuo` assoluto** *(senza dividere per `rho`)*, perche' senza materia `rho = 0`: come D2 di [M2034], solo in questo script;
  - **la misura:** a ogni tick `A_0 = <phi_v|phi>/<phi_v|phi_v>` e `A_q = <phi_v e^{iqx}|phi>/<phi_v|phi_v>`; **`omega(q) - omega_phi` = meno la pendenza del fit lineare della fase svolta di `A_q/A_0`**, su `[0, 1000]` e sulle due meta'. Si stampa anche `|A_q/A_0|/eps`: se oscilla, nell'increspatura ci sono piu' bande;
  - **`c_phi`** = la pendenza fra i due `q` piu' piccoli lungo `x` *(`n = 2` e `4`)*; **il gap** = `a` nel fit `omega(q) - omega_phi = a + b q^2` lungo `x`;
  - **la linearita'** su `x`, `n = 2`;
  - **`c_psi = 0.084955`** per tick, cioe' `ep_fondo.C_RET`, **la velocita' di gruppo MASSIMA della banda della materia** *(definita cosi' in `ep_fondo.py`)*. Nella misura di E(p) `v` e' arrivato solo a `2.84e-02` *(`p 0.50`)*: **la pendenza di E(p) dove l'oggetto si spezza non e' stata misurata.** Il confronto si fa col massimo della banda, e lo dico.
- **LA FORMA ATTESA, scritta prima:**
  - il vuoto sta su un autostato della camminata con `omega_phi = -0.4712 = -3 pi/20`. **Attorno a quel punto la banda puo' avere un cono** *(`omega(q) - omega_phi = +- c_phi |q|`, senza gap, come il grafene)* **o un minimo** *(`omega(q) - omega_phi = Delta + q^2/(2 m_phi)`, col gap `Delta`)*;
  - **non so quale delle due:** e' la domanda;
  - se l'increspatura `phi_v e^{iqx}` non e' un autostato, `A_q` contiene due rami *(`+` e `-`)* e `|A_q|` batte; la fase allora segue il ramo dominante.
- **I CASI NOTI** *(`due_luci.py noto`)*:
  - **(K1)** `eps = 0`, `1000` tick: `omega_phi` per tick costante entro `1e-12`, e `|A_0| = 1` entro `1e-12`. **«Al bit» non lo chiedo:** l'`arg` arrotonda;
  - **(K2)** a `k 0` la componente a `q` vale `eps` entro `1e-12`, e quella a `2q` sta sotto `1e-9`;
  - **(K3)** la lettura su una serie sintetica `e^{-i omega k}` ridà `omega` entro `1e-9`.
- **Le corse:** sei, da `1000` tick, un processo ciascuna: `x` con `n = 2, 4, 8, 16`; `y` con `n = 2`; `x`, `n = 2`, `eps = 5e-4`.
- **LE PREVISIONI DEL GUARDIANO:** P1 *(`60%`)* due luci; P2 *(`55%`)* `c_phi > c_psi`; P3 *(`70%`)* l'anisotropia a `q` piccolo sotto il `5%`; P4 *(`65%`)* le onde del vuoto hanno un gap.
- **LE MIE:** P4 `60%`; P1 `65%`.
- **### [M0024] LA NOTA SUL RUMORE E LA LETTURA** *(DECISIONE DI LUCA, 2026-11-27 `00:24`; annotata dopo `due_luci.txt`, `12d3d40b`; la sezione sopra non si riscrive)*:
  - **l'«anisotropo `-8.19%`» del referto NON e' un'anisotropia.** E' il rapporto fra due spostamenti di frequenza da `~2e-8` per tick *(`-2.50e-08` lungo `y`, `-2.72e-08` lungo `x` interpolato)*, piu' piccoli dello scarto del fit *(`5.32e-04` rad su una fase totale di `~2e-5` rad)*: **e' rumore**;
  - **LA LETTURA:** allo zero simmetrico il vuoto **non propaga** l'increspatura. `omega(q) - omega_phi` sta sotto `1.7e-6` per tick fino a `q 0.62`, e la risposta e' lineare *(`eps 5e-4` = `1e-3` entro `0.000%`)*: **una banda piatta**;
  - **`c_phi` non e' misurabile:** il limite e' `max_q |omega(q) - omega_phi| / q` = `2.681e-06` *(a `x` n `16`, calcolato dai numeri del referto)*, **sotto `1e-5`**, contro `c_psi` di `0.084955`;
  - **S4, «due luci», vale alla lettera:** la seconda luce non c'e';
  - **le previsioni:** P1 giusta; P2 e P4 sbagliate; P3 non decidibile.


## 3-vicies. [M2034-B] LA LETTURA DI d1', d2', d3' COL CRITERIO C *(DECISIONE DI LUCA `09:25` e [M2034] `20:34`; scritta PRIMA dello script e PRIMA di guardare le serie)*

- **LO SCRIPT NUOVO:** `doc/referti_l2/due_corpi_lettura_v3.py`. `due_corpi_lettura_v2.py` e' usato e non si riscrive: la v3 lo importa per `fit_d` e per gli anelli. **Il referto:** `doc/referti_l2/due_corpi_fondo_v6.txt`. **I dati:** `M2034/coppia/{d1,d2,d3}`.
- **LE FINESTRE:** `12` da `500` tick, `[0, 500]`, ..., `[5500, 6000]`.
- **IL CONTROLLO d3'** *(le soglie sono di Luca; come si misura e' una scelta mia)*:
  - **`w`** si calcola con la formula del giro, `fondo_puntofisso_chi.w_di` *(`torneo_tenuta`, sulla `rho_psi` per nodo)*, sui tre stati della finestra *(`k0`, `k0 + 250`, `k0 + 500`)*. **Tutti e tre** devono stare entro il `5%` di `4.5`;
  - **`omega`** e' la media della serie per tick di `serie.json` sulla finestra, entro il `5%` di `0.0833`;
  - **il pozzo** si calcola con `fondo_puntofisso_chi.profondita` *(chi medio su `r < 4` dal centro di `rho_psi`)* sui tre stati, **tutti e tre** entro il `10%` di `-102`;
  - **una finestra e' valida se passa tutte e tre le condizioni.** I riferimenti sono i numeri scritti da Luca *(`4.5`, `0.0833`, `-102`)*. Le medie del giro 3 sulla sua finestra `[3500, 6000]` si stampano accanto, senza contare per la validita';
  - **le finestre valide si stampano PRIMA di qualunque riga su d1'.**
- **IL CONTROLLO d2'** *(Luca)*: `max |d(k) - d(0)|` sulla serie *(ogni `10` tick, `0..6000`)* `< 0.5` nodi. **Se non passa, nessun verdetto su d1'.**
- **LE LETTURE SU d1'** *(solo sulle finestre valide)*:
  - **(i)** `d(k)` e il fit `a` per finestra, per d1' e d2', e la differenza `a(d1') - a(d2')` col suo errore;
  - **(ii)-(v)** come `due_corpi_lettura_v2`, sugli stati delle finestre valide: `J_r` sugli anelli `[8, 16)` e `[16, 32)`, `rho_phi`, chi sugli anelli, `w` *(il raggio quadratico medio nella meta')* e `omega`.
- **IL VERDETTO SU d1', una scelta mia, dichiarata ora:**
  - **«si avvicinano»** se `a(d1') - a(d2') < 0` oltre `2 sigma` su almeno meta' delle finestre valide, e su nessuna e' `> 0` oltre `2 sigma`;
  - **«si allontanano»** nel caso speculare;
  - **«nessun segnale»** altrimenti.
- **I CASI NOTI** *(nello stesso script, prima delle letture)*:
  - **(N1)** `w_di` e `profondita` rifatti su `M0414/puntofisso_accoppiato/giro_3/stato_000500.npz` ridanno `giro.json` `w[5]` e `profondita[5]` **al bit** *(ogni `100` tick, quindi l'indice `5` e' `k 500`)*;
  - **(N2)** la serie di d3' ha `6000` valori di `omega`;
  - **(N3)** il caso che DEVE FALLIRE: con il riferimento di `w` a `4.5 x 1.2`, nessuna finestra di d3' e' valida *(se una lo fosse, vorrebbe dire che `w` si sposta del `20%`: lo stampo comunque)*.
- **LE PREVISIONI:**
  - **di [M0925]:** P3 *(`55%`)* almeno `6` finestre valide su `12`; P4 *(`70%`)* d1' si avvicina e d2' sta fermo; **P5** *(`50%`)* «K fra `0.8` e `1.2`»: **K non e' definito per B nel TODO.** Lo dichiaro **non valutabile**, a meno che Luca non lo definisca;
  - **le mie, prima:** P3 `60%` *(`omega` di d3' parte a `0.08407`, cioe' `+0.9%`)*; P4 `35%` *(nel vuoto fresco il pozzo di chi delle due copie si somma, e la spinta, se c'e', e' piccola rispetto al respiro)*.


### 3-vicies, il seguito. [M0024] IL CRITERIO C', I NUMERI SEMPRE, D2' *(DECISIONE DI LUCA, 2026-11-27 `00:24`, arrivata dalla posta, `e609aafa`; letta alle `00:25`; scritto PRIMA di `due_corpi_lettura_v4.py`)*

- **L'ERRORE n.256 DEL GUARDIANO, e il mio:**
  - il criterio C chiedeva `w` entro il `5%` per finestra di `500`, ma il respiro di `w` e' un modo normale *(D di [M0414], circa `+-20%` con un periodo di `2500` tick)*. **Il giro 3 di riferimento non passa il suo stesso criterio** *(`0` finestre su `12`, `criterio_c_giro3.txt`)*;
  - io l'ho tradotto nella carta senza vederlo.
- **LE SCELTE DI LUCA:**
  - **C'.** Per finestra di `500`, `omega` medio entro il `5%` di `0.0833` e il pozzo medio entro il `10%` di `-102`, come prima. **`w` invece si media sul periodo `P = 2500`**, sulle finestre `[0, 2500]`, `[2500, 5000]` e `[3500, 6000]`, e deve stare entro il `10%` di `4.60` *(la media del giro 3 su `[3500, 6000]`)*. **Le finestre di `500` valide per d1' sono quelle che stanno dentro un periodo valido;**
  - **N.** I numeri si stampano sempre, con o senza verdetto: `d(k)` per finestra di `500` per d1' e d2', col verso *(VERSO o VIA)*; `a(k)`; `J` radiale; `chi(k)`; `w` e `omega` per tutte e tre le corse. **Il verdetto sta su un'altra riga;**
  - **D2'.** d2' e' il controllo negativo. **Il verdetto su d1' si da' solo se `|Delta d|` di d1' supera `3` volte quello di d2' nello stesso intervallo, e nello stesso verso.** Altrimenti: «non distinguibile dalla deriva senza chi». La deriva di d2' si dichiara col suo verso.
- **LE MIE SCELTE, dichiarate prima:**
  - **le medie di d3'** si fanno sugli stati salvati *(ogni `250`)*: il pozzo medio della finestra di `500` sui suoi `3` stati, `w` del periodo sui suoi `11` stati *(gli estremi compresi)*. **Nel giro 3** *(campioni ogni `100`)* le stesse medie si fanno sui campioni, sempre con gli estremi compresi: e' cosi' che e' nato il `4.6015`;
  - **`w` dei periodi** si misura con `fondo_puntofisso_chi.w_di`, la formula del giro;
  - **`Delta d`** di una finestra = `d(k1) - d(k0)` dalla serie *(ogni `10` tick)*; **VERSO** se `< 0`;
  - **il verdetto D2'** si da' **per finestra valida**, e c'e' **una riga di sintesi** *(quante finestre VERSO, VIA, «non distinguibile»)*;
  - **i numeri N per tutte e tre** si stampano sui `25` stati con le formule di `due_corpi_lettura_v2` *(d3' con un corpo solo, tutto il toro)*, e `d(k)` su tutte le `12` finestre;
  - **l'ordine:** (R), poi le finestre valide di d3', poi i numeri N, poi i verdetti.
- **I CASI NOTI:**
  - **(R)** il giro 3 di riferimento passa C': `w` su `[3500, 6000]` = `4.6015` per costruzione, e `omega` e il pozzo `12` su `12`. Lo stampo anche per `[0, 2500]` e `[2500, 5000]`;
  - **(N1)** come nella v3: `w_di` e `profondita` al bit sul giro 3 a `k 500`.
- **IL REFERTO:** `doc/referti_l2/due_corpi_fondo_v6_C.txt`.
- **LE PREVISIONI:**
  - **del guardiano:** P1 *(`70%`)* con C' almeno un periodo di d3' e' valido; P2 *(`60%`)* d2' deriva VERSO; P3 *(`55%`)* d1' si avvicina piu' di `3` volte d2': verdetto VERSO;
  - **le mie, prima:**
    - P1 al `75%`: d3' ha `w` da `3.40` a `6.10` con medie vicine a `4.6`;
    - **P2 al `50%`**: dalla v3 `d2'` *(`d(0) 41.569`)* ha `max |d - d(0)|` `1.50` a `k 6000`, ma il verso non l'ho guardato;
    - P3 al `30%`.
- **LA LETTURA DI «NELLO STESSO VERSO»** *(una mia scelta, aggiunta col commit dello script e prima della corsa)*: la regola chiede **lo stesso segno di `Delta d` di d2'** nella stessa finestra *(la lettura letterale)*. Se `|Delta d1'| > 3 |Delta d2'|` col verso opposto a d2', la finestra conta «non distinguibile», ma si stampa a parte come **«fuori regola»**, perche' sia Luca a leggerla.

- **### [M0106] D2'' E IL VERDETTO RISCRITTO** *(DECISIONE DI LUCA, 2026-11-27 `01:06`, arrivata dalla posta, `4c973b3a`; letta alle `01:07`; scritto PRIMA di `due_corpi_lettura_v5.py`)*:
  - **GLI ERRORI DEL GUARDIANO:**
    - **n.257:** in D2' «nello stesso verso» stava per «nello stesso intervallo». Io l'ho applicato alla lettera e ho segnalato le finestre «fuori regola»;
    - **n.258:** K4' aveva una soglia sotto il pavimento dell'arrotondamento.
  - **D2'', LA SCELTA DI LUCA:** per finestra valida, **VERSO** se `Delta d(d1') < 0` e `|Delta d(d1')| > 3 |Delta d(d2')|` nello stesso intervallo; **VIA** se `Delta d(d1') > 0` con lo stesso rapporto; altrimenti «non distinguibile». **Il verso di d2' si dichiara, ma non entra nella regola;**
  - **LO SCRIPT:** `due_corpi_lettura_v5.py`. La v4 e' usata e non si tocca: **la v5 la fa girare per intero** *(la sua riga D2' resta stampata, marcata come SUPERATA)* e poi aggiunge D2''. **Il referto `due_corpi_fondo_v6_C.txt` si riscrive sugli stessi `25` stati, senza nessuna corsa;**
  - **IN PIU', LE MIE DEFINIZIONI, dichiarate prima:**
    - il minimo di `d(k)` di d1' e il suo tick, dalla serie ogni `10` tick;
    - il massimo dopo il minimo;
    - **il minimo successivo** = il minimo dopo quel massimo, **ma solo se e' interno** *(cioe' non all'ultimo tick)*. Il periodo e' la distanza fra i due minimi. **Se il minimo successivo cade all'ultimo tick, dichiaro che non c'e'**, e stampo il mezzo periodo, minimo -> massimo, **ma non lo chiamo periodo**;
    - **la tabella per finestra di `500`:** `d` medio dalla serie; `omega` medio di ciascun corpo dalla serie per tick; **chi al centro** = chi medio su `r < 4` dal baricentro del corpo nella sua meta', in media sui `3` stati della finestra. Per d1', d2' e d3'.
  - **LA PREVISIONE DEL GUARDIANO:** P1 *(`90%`)* VERSO `8`, VIA `4`. **La mia: la stessa, al `95%`.** I rapporti stampati dalla v4 vanno da `6.78` a `95.5`, tutti sopra `3`.

- **### [M0951] IL VIDEO DELLA COPPIA d1'** *(DECISIONE DI LUCA, 2026-11-27 `09:51`, arrivata dalla posta, `30d9cd91`; letta alle `09:53`; scritto PRIMA di `anima_coppia.py`; sola lettura, nessuna corsa)*:
  - **IL PERCORSO:** il mandato dice `E:/soliton_simulator/controllo/M2034/d1`, ma quella cartella non esiste. **Gli stati sono in `M2034/coppia/d1`**, cioe' la `BASE` di `due_corpi_lettura_v3.py`, la stessa delle letture v3, v4 e v5. **Uso quella;**
  - **LE MIE SCELTE, dichiarate prima:**
    - **le coordinate:** `dxy` = `toro.scarti` rispetto a `centro_coppia`, come nella v5. **Il baricentro della coppia** al tick `k` e' la media, pesata con le masse, dei due baricentri della `serie.json` *(le colonne `1,2,3` e `4,5,6`)* in quel tick. **Il riquadro** e' `|x - x_b| <= 60` e `|y - y_b| <= 60` in unita' di lunghezza *(il lato del triangolo vale `1`)*;
    - **`d(k)`** e' la distanza fra i due baricentri della serie in quel tick. **`omega` di un corpo** e' la media della serie per tick sui `250` tick che precedono `k`, cioe' `[k-250, k)`; a `k 0` e' `[0, 250)`;
    - **le scale fisse:** `rho_psi` va da `0` al massimo su tutti i quadri dentro il riquadro; `chi` va dal minimo al massimo su tutti i quadri dentro il riquadro; le curve di livello di `chi` sono `12`, equispaziate, uguali in tutti i quadri;
    - **25 quadri senza interpolazione**, a `4 fps`; formato `1280x640` *(`figsize 16x8`, `dpi 80`)*, `libx264` `yuv420p`. **Se supera `5 MB`, rifaccio a `960x480`** *(`dpi 60`)*, nella stessa esecuzione;
  - **I CONTROLLI, PRIMA DEL VIDEO:**
    - **(il mandato) DEVE:** il quadro a `k 3250` ha `d` entro il `10%` di `6.795` *(il minimo, che cade a `k 3230`)*;
    - **(mio, il controllo positivo sul sistema di riferimento) DEVE:** a `k 0` il baricentro di `rho_psi` di ciascuna meta' *(`y < 0` e `y >= 0` in `dxy`)* coincide entro `0.5` col baricentro della serie. **Se le coordinate dei pannelli fossero in un altro riferimento, questo controllo fallirebbe;**
  - **LA PREVISIONE, mia:** i due controlli passano *(`90%`)*; il video sta sotto i `5 MB` gia' a `1280x640` *(`80%`: sono `25` quadri soli)*.
  - **LA v2** *(scritta dopo il v1 illeggibile, `593dea51`; PRIMA di `anima_coppia_v2.py`)*: **cambia solo come si disegna**. I campi si colorano con `tripcolor` in `gouraud` sulla triangolazione dei nodi del riquadro, cosi' il pannello e' pieno; le `12` curve di livello di `chi` sono bianche con spessore `0.9`; in entrambi i pannelli un `+` segna i due baricentri della serie. **Dati, scale, controlli e formato restano quelli del v1.** Il video sovrascrive `anima_coppia.mp4`; il referto e' `anima_coppia_v2.txt`. **Il controllo in piu', mio:** guardo i quadri a `k 0`, `k 3250` e `k 6000` prima del commit.

- **### [M1016] A0, LA CORSA LUNGA d1'' E IL VIDEO v3** *(DECISIONE DI LUCA, 2026-11-27 `10:16`, arrivata dalla posta, `0c25127e`; letta alle `10:18`; scritto PRIMA di `coppia_a0.py`)*:
  - **LA DOMANDA DI LUCA:** «nelle parti finali i due oggetti sembrano svanire, e non capisco se e' un artefatto».
  - **LE DUE IPOTESI E IL CRITERIO CHE LE SEPARA:**
    - **(a) e' un artefatto di scala:** la scala dei colori e' fissa sul massimo di tutta la serie. Se la materia si allarga, il suo massimo cala e il quadro sbiadisce;
    - **(b) la materia si disperde davvero.** Ma la norma di `psi` si conserva per costruzione: **se cala, e' un errore**;
    - **il criterio e' la norma.** Se la norma e' ferma e `max rho` cala, la materia si e' solo allargata: vale (a).
  - **S1, A0, a costo zero sui `25` stati di `M2034/coppia/d1`.** Per ogni stato:
    - **(i) la norma** `N = somma |psi_h|^2`. **DEVE:** `|N(k)/N(0) - 1| < 1e-9` per ogni `k` *(relativo: la mia lettura di «ferma a `1e-9`»)*. **Se fallisce, FERMO: e' un errore, e si dichiara prima di tutto il resto;**
    - **(ii)** `max rho_psi`, il suo nodo `(m1, m2)` e la sua posizione;
    - **(iii) il numero di massimi locali**, cosi':
      - la lisciatura: `s(i)` e' la media di `rho_psi` sul disco di raggio `2` attorno al nodo. Il disco ha `19` nodi *(gli offset di reticolo `(a, b)` con `|a A1 + b A2| <= 2`; il nodo e' `m1 L + m2`; periodico sul toro)*;
      - **un massimo locale** e' un nodo con `s(i) >= s(j)` per ogni `j` del suo disco e con **`s(i) > 0.30 max s`** *(la soglia del `30%` va sul massimo della lisciatura dello stato)*;
    - **(iv) il raggio della nube** `R = sqrt(somma rho r^2 / somma rho)`, con `r` misurato dal baricentro totale di `rho_psi`. Le coordinate sono `toro.scarti` dal `centro_coppia`, come nella v5 e nel video;
    - **IL VERDETTO PER STATO:** **DUE CORPI** se i massimi sono `2`, **UNO** se e' `1`, **ALTRO (n)** se sono di piu'. **Il tick della fusione** e' il primo stato con UNO dopo uno con DUE.
  - **I CASI NOTI:**
    - **(K1)** `stato_000000`: DEVE dare `2` massimi, a una distanza entro `1` da `41.57`. La distanza fra due nodi del reticolo non coincide coi baricentri: e' la mia tolleranza;
    - **(K2)** un oggetto solo, cioe' il giro 3. Uso `M0414/puntofisso_accoppiato/giro_3/stato_003000.npz`, l'ultimo stato del giro, centrato sul nodo del suo massimo. **DEVE dare `1` massimo.** Lo stato non e' nel mandato: la scelta e' mia.
  - **S2, LA CORSA LUNGA d1''** da `stato_006000.npz` *(sha1 `aca74f48`)* per altri `12000` tick, fino a `k 18000`, stati ogni `250`, **UN processo**. `chi` e `pi` si prendono dallo stato. **(K0)** i primi `250` tick devono riprodurre al bit `6000 -> 6250` della stessa via: **lo stato a `6250` non esiste** *(d1' finisce a `6000`)*, quindi la carta di quel pezzo dira' come si sostituisce. **Il pezzo ha la sua carta, scritta prima di `due_corpi_fondo_v7.py`.**
  - **S3, IL VIDEO v3** su `73` quadri a `6 fps`, con tre pannelli:
    - `rho_psi` a scala FISSA;
    - `rho_psi` a scala PER QUADRO;
    - `chi`.
    - In sovrimpressione: `k`, `d(k)` *(solo se A0 dice DUE CORPI, altrimenti «un corpo»)*, la norma, `max rho` e `R`.
  - **S4:** **nessun verdetto su rimbalzo o orbita finche' A0 non e' fatto.** Dopo, i minimi si leggono solo sui tratti con DUE CORPI.
  - **LE PREVISIONI, mie, prima:**
    - la norma e' ferma *(`95%`)*: vale (a);
    - A0 dice DUE fino a `k 2750` e UNO da `k 3000` o `3250` in poi *(`70%`)*. Ma a `k 6000` la nube allungata **potrebbe dare `2` massimi deboli sopra il `30%`** *(`30%`)*: in quel caso «DUE» non significa due corpi separati;
    - `R` cresce dopo la fusione *(`80%`)*.
  - **### LA CORSA LUNGA d1'' (S2), LA CARTA** *(scritta alle `10:26`, PRIMA di `due_corpi_fondo_v7.py`)*:
    - **LA VIA E' QUELLA DI d1'** *(`due_corpi_fondo_v6.py corsa --quale d1`)*:
      - `costruisci` della v6 e `D.parametri` danno `P` e `m0` **prima** che lo stato venga caricato, nello stesso ordine della corsa originale. **Si asserisce** che i parametri coincidano col `meta` di `serie.json` e che `centro_coppia` coincida con quello del meta;
      - poi si carica lo stato di partenza: tutte le chiavi di `st` *(`Lambda, h_int, phi_h, psi, psi_h, rho`)*, `campo_A` e `campo_E` in `C.campo`, e `chi, pi, theta_a` in `X`. **Tutto in place.**
      - **Il ciclo** e' il corpo di `due_corpi_fondo.ciclo` *(`tick_chi_v2` nella forma `L-1` del nucleo)*, ma **col tick ASSOLUTO** da `k_da + 1`. Siccome `OGNI_GAUSS` vale `250` e `6000` e' un suo multiplo, **`C.residuo` cade negli stessi tick della corsa originale.**
    - **(K0') AL POSTO DI K0:** lo stato a `6250` di d1' non esiste, quindi non si puo' riprodurre `6000 -> 6250`. **Si prova la stessa cosa un passo prima:**
      - si riparte da `stato_005750.npz` per `250` tick;
      - **DEVE:** lo stato finale e' **uguale AL BIT** a `stato_006000.npz` in ogni chiave *(`st`, `campo_A`, `campo_E`, `chi`, `pi`, `theta_a`)*;
      - **DEVE:** le righe della serie da `5760` a `6000` e `omega` dei tick da `5751` a `6000` sono uguali al bit a quelle di `serie.json`;
      - **(K0'-neg), il caso che DEVE FALLIRE:** la stessa ripresa **senza caricare `campo_E`** *(che resta quello di `costruisci`)*. **DEVE** dare uno stato finale **diverso** da `stato_006000`. Se fosse uguale, il confronto non vedrebbe il campo;
      - **la carica:** prima del ciclo, **DEVE:** la riga della serie misurata a `k_da` e' uguale al bit a quella di `serie.json`.
    - **Se K0' fallisce: FERMO, la corsa non va in coda.**
    - **LA CORSA:**
      - parte da `stato_006000.npz` *(sha1 `aca74f48`, controllato)* e fa `12000` tick, fino a `k 18000`;
      - salva gli stati ogni `250` col `k` ASSOLUTO *(`stato_006250` ... `stato_018000`)* e la serie ogni `10`, nella cartella **`M2034/coppia/d1L`**;
      - `serie.json` ha lo stesso formato della v4. **`omega[j][i]` e' il tick `6001 + i`**, e `k_da` sta nel meta;
      - **un processo solo, dalla coda** *(`coda_m1446.py`, il tetto `10`, il freno `4 GB`)*.
    - **IL TEMPO, stimato** dalla corsa d1' *(`6000` tick in `4896 s`)*: circa `9800 s`, cioe' **2.7 ore**.
    - **LA MIA PREVISIONE:** K0' passa al bit *(`85%`)*; K0'-neg fallisce come deve *(`95%`)*.
