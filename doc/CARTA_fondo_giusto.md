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
