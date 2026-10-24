# IL PROGETTO DEL CAMPO U(1) SUGLI ARCHI: LA LUCE DEL MODELLO *(sulla carta: nessun codice, nessuna decisione)*

> ### **Il mandato:** di Luca, «il progetto del campo `U(1)` sugli archi» *(il piano di Luca del `2026-10-24` alle `19:07`: il progetto, il prototipo sui triangoli, poi la FCC)*; ### **il task history
> `doc/TASK_HISTORY/2026-10-24_progetto_u1.md`** *(`f8f55b9d`, entrato PRIMA, controllato)*; ### **la voce [[PROGETTO-U1]]** *(collegata a [[LUCE-VINCOLO-LAMPI-GAMMA]], [[SPAZIOTEMPO-3PIU1]], [[PIANO-2D-3D]],
> [[LORENTZ-MATERIA-INTERFERENZA]], [[U-ARCO-DINAMICA]], [[DOMANDA-U-DINAMICA-LE-FORME]])*.
> ### **Ogni affermazione sul codice di oggi e' letta dal sorgente, con file e riga.** ### **Per ogni scelta: le alternative, i pro e i contro, e la MIA RACCOMANDAZIONE, marcata `[RACCOMANDAZIONE]`: la scelta e' di Luca.**

## 1. LO SCOPO E IL CRITERIO DI SUCCESSO

- ### **LO SCOPO:** ### **un campo con gradi di liberta' PROPRI sugli archi** *(non «schiavo» della materia)*, ### **le cui onde si propaghino SENZA SMORZARSI** *(un passo reversibile)*.
- ### **LA MISURA CHE DECIDE:** ### **la velocita' delle onde del campo per tempo proprio, `c_U/s`, contro `v_b/s = 0.785` della particella a `K` e `v_max/s = 0.60` dei segnali della materia** *(sui triangoli, `7daa8840`,
  `77f9f850`; e' una proprieta' LOCALE del passo: si misura gia' in 2D, l'errore del guardiano `n.61`)*.
- ### **I TRE ESITI:**

| l'esito | che cosa vorrebbe dire |
|---|---|
| `c_U = v_b` | ### **la particella vede la `c` del campo: la relazione di Einstein del modo a `K` usa la velocita' della luce; la gravita' di `7daa8840` e' quella della relativita' generale con la `c` giusta.** ### **Restano i segnali della materia piu' lenti** *(`v_max < c`)*: come una particella massiva che non raggiunge la luce |
| `c_U = v_max` | ### **la luce va come il limite dei segnali della materia: un solo limite di causalita'; ma la particella a `K` ha una relazione di Einstein con una `c` PIU' GRANDE** *(`v_b > c`)*: ### **un problema di Lorentz nella dispersione della materia** |
| diversa da tutte e due | ### **tre velocita' diverse: il problema di relativita' ristretta resta, e il campo non lo risolve** *(e' la mia previsione sulla carta, sezione `5`: `c_U/s = 1`)* |

## 2. CHE COSA C'E' OGGI NEL CODICE

- ### **LO SPOSTAMENTO COL TRASPORTO** *(`primo_ordine/termini/camm_spostamento.py:6`, generato da `primo_ordine/leggi/leggi.yaml:393-421`)*: ### **`hop(theta) = alpha I + beta S_U`, `S_U = [[0, U^dagger], [U, 0]]`, `alpha = (1 + e^{i
  theta})/2`, `beta = (1 - e^{i theta})/2`, `theta = pi dtau_arco/dtau_rif`.** ### **E alla riga `418` di `leggi.yaml`: «la parte `U(1)` di `U` e' l'elettromagnetismo, la parte `SU(2)` la geometria».** *(Lo stesso nella
  CARTA, punto `F2`, e in `proto_camminata/geometria.py:3-6`: `U_kj = e^{i theta_kj} V_kj`.)*
- ### **IL CODICE CHE LO FA:** ### **`primo_ordine/flussi_parziali.py:378-408`, `hop_psi`:** ### **il lato `0` diventa `alpha v0 + beta U^dagger v1`, il lato `1` `alpha v1 + beta U v0`** *(`np.einsum` sulle `U = mot.geo.U`)*; ### **`z_arco`
  (`305-314`) e' `e^{i pi s_arco frazione}`; `s_arco` (`184-223`) la media armonica dei due nodi** *(`B-3`, calcolata come `S/2 - D^2/(2S)`)*; ### **`_nel_cono` (`226-243`) ASSERISCE `0 < s <= 1`** *(`B-5`)*.
- ### **DOVE `U` E' COSTRUITO, E PERCHE' OGGI E' `I`:** ### **`primo_ordine/scena_l2.py:197-199`** *(`U[:,0,0] = U[:,1,1] = 1`)* ### **e `csv/_triangoli.py` `scena_toro`** *(`U = I`)*. ### **`primo_ordine/motore.py:102-131`,
  `Geometria`, asserisce SOLO l'unitarieta'** *(`U^dagger U = I` entro `1e-12`; il determinante NON e' controllato: `U(2)` e' ammessa)*. ### **IL PERCHE', scritto:** ### **`leggi.yaml:325-330`: «`U` e' FERMA finche' la
  `U` dinamica non si deriva (posto `A2`)»; `doc/MAPPA_DIPENDENZE.md:136`: «prima di `L4` il campo di gauge `U` e' FERMO»** *(e `L4` aspetta `L3`)*. ### **`U` NON e' nello stato** *(`primo_ordine/stato.py:18-25`:
  `psi`, `psi_h`, `phi_h`, `Lambda`, `rho`, `h_int`)*.
- ### **LA CARICA DI NOETHER:** ### **la grandezza conservata ESATTAMENTE e' la NORMA DELLA MATERIA `M = somma_h |psi_h|^2`** *(`DEC-QC-CONSERVATA`, `doc/ALBERO_era2.yaml:66-107`, presa il `2026-10-16`)*; ### **`leggi.yaml:243`: «LA NORMA SI
  CONSERVA PER NOETHER, dalla U(1)»; `doc/ASSIOMI.md` `A16.4`: «la norma totale, che e' la carica di Noether della fase».** ### ⚠ **LA DOMANDA APERTA:** ### **`doc/ASSIOMI.md:276`** *(`A14` punto `3`)* ### **dice «il verso di rotazione
  collettivo, la carica di Noether della fase»** *(una carica di ROTAZIONE, non `|psi|^2`)*; ### **e la carica che distinguerebbe le DUE BANDE della coppia** *(particella e antiparticella)*, ### **`Q = N+ - N-`, e' MISURATA
  NON conservata** *(`doc/REFERTO_bande.md:137-139`)*. ### **Con la norma come carica, LE DUE BANDE HANNO LA STESSA CARICA** *(`|psi|^2 >= 0`)*: ### **un'antiparticella di carica opposta NON c'e' a questo livello.** ### **E' da
  decidere** *(sezione `8`)*.
- ### **LA CORRENTE SULL'ARCO:** ### **nel codice NON c'e' una corrente di carica** *(`primo_ordine/corrente.py` e `energia.py:141-181` sono correnti dell'ENERGIA, e allo spostamento intero, frazione `1`)*; ### **la formula sulla carta di
  `doc/TASK_HISTORY/2026-10-12_u_arco_dinamica.md:74-79` e' per la permutazione intera.** ### **PER IL FLUSSO PARZIALE DI OGGI, dal codice di `hop_psi`** *(il conto, mio, sulla carta)*: ### **la norma che passa dal lato `1` al lato
  `0` in un pezzo e' `J = sin^2(theta/2) (|v1|^2 - |v0|^2) + sin(theta) Im(v0^dagger U^dagger v1)`** *(da `|alpha|^2 = cos^2(theta/2)`, `|beta|^2 = sin^2(theta/2)`, `conj(alpha) beta = -i sin(theta)/2`)*; ### **a `theta = pi`
  torna `|v1|^2 - |v0|^2`** *(lo scambio)*. ### **E' ESATTA: la carica si muove SOLO nello spostamento** *(il Grover e la moneta agiscono sulle estremita' DELLO STESSO nodo; il legame mette solo fasi)*.

## 3. CHE COSA VIENE DALL'ERA 1 E CHE COSA NO *(`doc/BUSSOLA_TECNICA_dev-spinoriale.md` `4.0`-`4.5`; `doc/PROTOCOLLO_test_olonomia.md`)*

| | che cosa | perche' |
|---|---|---|
| **SI'** | ### **la placchetta triangolare come campo magnetico** *(`4.2`: `W = Tr(U_ij U_jk U_ki)`)* | ### **e' il rotore discreto: gauge invariante, locale** |
| **SI'** | ### **il protocollo dell'olonomia come strumento di misura** *(`PROTOCOLLO_test_olonomia.md` `§2`-`§3`: i triangoli dai vicini comuni, la convenzione di verso fissa, `W(r)`)* | ### **misura `B` senza toccare la dinamica** |
| **SI'** | ### **il tempo relazionale `tau = d/cs` e «zero manopole»** *(`4.3`, `4.5`)* | ### **il campo usa il tempo dell'arco del passo di oggi** *(`B-3`)* |
| **SI'** | ### **il campo che LEGGE la materia; la catena delle riduzioni al limite con un sigillo per anello** *(`4.5`)* | ### **il controllo `(a)`: tutto spento = il passo di oggi al bit** |
| **NO** | ### **lo STRATO 1** *(`4.3`: `dU/dt = (U^Berry - U)/tau`)* | ### **e' del PRIMO ordine e SMORZA verso un valore fissato: non propaga onde** *(e, nei fatti, fu realizzato come ritardo dei Bloch, `doc/STATO_RUN.md`)* |
| **NO** | ### **lo STRATO 2** *(la forza hebbiana saturata)* | ### **IRREVERSIBILE: contro la conservazione locale dell'era `2`** *(`DEC-QC-CONSERVATA`)* |
| **NO** | ### **la connessione di Berry come campo** *(`4.0`)* | ### **«schiava» dei Bloch, senza gradi di liberta' propri: niente fotoni liberi** *(e per la regola `F2` Berry fisserebbe al piu' la parte `SU(2)`)* |

## 4. LE VARIABILI

- ### **`A_a` la fase `U(1)` sull'arco `a`** *(`U_a = e^{i A_a} V_a`, `V_a` la parte `SU(2)`, oggi `I`)*, ### **orientata** *(`A_ji = -A_ij`: un arco del codice e' orientato dal nodo proprio al vicino, `U_jk = U_kj^dagger`, `motore.py:520-541`)*;
  ### **`E_a` il coniugato** *(il campo elettrico sull'arco)*.
- ### **IL CAMPO MAGNETICO dalle placchette TRIANGOLARI:** ### **`B_p = somma_{a in bordo di p} +-A_a`** *(sui triangoli: due placchette per cella, «su» e «giu'»; sulla FCC i triangoli delle facce dei tetraedri e degli ottaedri)*.
- ### **COMPATTO O NO:**

| | pro | contro |
|---|---|---|
| **compatto** *(`e^{i A}`, energia di placchetta `1 - cos B_p`)* | ### **e' cio' che `U` gia' e'** *(una fase)*; ### **la carica e' quantizzata per costruzione; l'invarianza di gauge e' esatta su `U`** | ### **i MONOPOLI; in `2+1` il `U(1)` compatto CONFINA a ogni accoppiamento** *(Polyakov: il fotone prende una massa esponenzialmente piccola)*; ### **in `3+1` ha una fase di Coulomb ad accoppiamento debole** |
| **non compatto** *(`A` reale, energia `B_p^2/2`)* | ### **e' l'elettromagnetismo libero, lineare: la dispersione si calcola esatta** | ### **la carica non e' quantizzata; `A` non e' piu' una fase di `U` ma un numero reale da cui si fa `e^{iA}`** |

  ### **`[RACCOMANDAZIONE]` COMPATTO**, ### **perche' `U` e' gia' una fase e la FCC** *(`3+1`)* ### **ha la fase di Coulomb**; ### **col prototipo sui triangoli ad accoppiamento debole, dove i due coincidono a meno dei monopoli; e il
  confinamento di Polyakov in `2+1` va DICHIARATO come un effetto atteso, non un difetto.**

## 5. IL PASSO DEL CAMPO

- ### **DUE MEZZI PEZZI REVERSIBILI** *(il leapfrog, simplettico)*: ### **la SPINTA MAGNETICA** *(`E_a <- E_a - dt w_a somma_{p contiene a} +-(1/A_p) sin B_p`, la forza delle placchette che toccano l'arco)* ### **e la DERIVA ELETTRICA** *(`A_a <- A_a +
  dt (l_a/l*_a) E_a`)*; ### **i pesi** *(la lunghezza dell'arco `l`, l'arco duale `l*`, l'area della placchetta `A_p`)* ### **sono quelli del calcolo esterno discreto: FISSATI dalla geometria, nessuna manopola.**
- ### **NEL PALINDROMO:** ### **la spinta a frazione `0.5` ai due estremi e la deriva a frazione `0.5` due volte al centro** *(fra i due `SPOSTAMENTO-VUOTO`)*, ### **cosi' l'ordine resta palindromo** *(`leggi.yaml:202-209`)*: ### **`18` pezzi, l'impronta
  CAMBIA** *(`2e7f795d2a52fbe7` di `composizione.py:13` non vale piu')*. ### **E LA SORGENTE** *(sezione `6`)* ### **entra NELLO spostamento della materia** *(lo stesso pezzo che muove la carica)*.
- ### **IL TEMPO:** ### **`dtau_arco`, la media armonica dei due nodi** *(`B-3`, `flussi_parziali.s_arco`)*: ### **dove `cs` e' basso la luce rallenta: il RITARDO DI SHAPIRO viene da se'.**
- ### **LA DISPERSIONE ATTESA SUI TRIANGOLI** *(un conto in memoria, sulla carta: la matrice `C^dagger diag(1/A) C (l/l*)` coi pesi del triangolo `l = 1`, `A = sqrt3/4`, `l* = 1/sqrt3`)*: ### **TRE bande:** ### **una di GAUGE a
  frequenza nulla** *(i gradienti)*, ### **il FOTONE con `omega = k` a `k` piccolo** *(`1.000000` a `k 1e-3` in quattro direzioni: ISOTROPO, `c = 1` arco per unita' di tempo proprio)*, ### **e una banda «ottica» a `sqrt(24) = 4.899` a `Gamma`.**
  ### **Per tick `c_U = s`: `c_U/s = 1`** *(la PREVISIONE: diversa da `v_b/s = 0.785` e da `v_max/s = 0.60`)*.
- ### ⚠ **LA CONDIZIONE DI STABILITA'** *(di Courant per il leapfrog: `dt omega_max <= 2`)*: ### **`omega_max = sqrt(24)` sui triangoli, quindi `s <= 2/sqrt(24) = 0.408`: PIU' STRETTA del limite `s <= 1` di `B-5`.**

| | pro | contro |
|---|---|---|
| **il regime `s <= 0.408`** | ### **nessun numero nuovo: e' la geometria** | ### **il regime `s -> 1` e' escluso per il campo** *(e la' nasce l'unico modo senza massa della camminata, `92c63912`)* |
| **sotto-passi del campo** *(`n` per tick)* | ### **qualunque `s <= 1`** | ### **`n` e' un NUMERO** *(`A1`)*, ### **a meno di derivarlo** *(`n = ceil(s/0.408)`, che cambia con `s`)* |
| **pesi diversi** *(che abbassino `omega_max`)* | ### **`s <= 1`** | ### **cambia `c`: e' una manopola travestita** |

  ### **`[RACCOMANDAZIONE]` IL REGIME `s <= 0.408`, DICHIARATO** *(compatibile col regime di lavoro `s <= 0.3` proposto dal guardiano; il limite del campo e' una conseguenza, non un tetto)*. ### **Sulla FCC `omega_max` va calcolato.**

## 6. L'ACCOPPIAMENTO CON LA MATERIA

- ### **LA MATERIA SENTE `A`:** ### **gia' oggi, attraverso `U` nello spostamento** *(`hop_psi`)*. ### **IL CAMPO SENTE LA MATERIA:** ### **nello spostamento la norma `J_a` passa da un lato all'altro dell'arco** *(sezione `2`)*, ### **e lo
  stesso pezzo aggiorna `E_a <- E_a - e J_a`** *(la legge di Ampere discreta)*.
- ### **LA LEGGE DI GAUSS ESATTA a ogni tick:** ### **`div E = e rho`** *(la divergenza discreta sui nodi)*: ### **(i) la spinta magnetica e' a divergenza nulla PER COSTRUZIONE** *(`div rot = 0` esatto sul reticolo)*; ### **(ii) la carica cambia SOLO nello
  spostamento, e dello stesso `J_a` che entra in `E_a`.** ### **Quindi se vale al tick `0` vale sempre, a meno dell'arrotondamento** *(il controllo `(c)`)*.
- ### **L'INVARIANZA DI GAUGE del passo intero:** ### **`psi_i -> e^{i chi_i} psi_i`** *(su TUTTE le estremita' al nodo `i`)*, ### **`A_ij -> A_ij + chi_i - chi_j`** *(il verso secondo `U_jk = U_kj^dagger`)*: ### **il Grover e la moneta mescolano
  estremita' dello stesso nodo** *(la stessa fase)*, ### **il legame vede solo `|psi|^2`, il vuoto e' neutro** *(`flussi_parziali.py:414`)*, ### **lo spostamento e' covariante con `U`, `B_p` ed `E_a` sono invarianti.**
- ### **L'ENERGIA DI MATERIA PIU' CAMPO:** ### **`H_tot + somma_a E_a^2 w_a/2 + somma_p (1 - cos B_p)/A_p`** *(il passo e' una composizione di pezzi esatti o simplettici: l'energia si conserva al secondo ordine, come `H_tot` oggi, `DEC-QC-CONSERVATA` (b))*.

## 7. LA COSTANTE DI ACCOPPIAMENTO

### **LA DECISIONE PIU' PROFONDA DEL PROGETTO.** ### **In natura `alpha = e^2/(4 pi hbar c) ~ 1/137`**; ### **la regola `A1`: nessun numero da tarare.**

| l'alternativa | pro | contro |
|---|---|---|
| **un numero dichiarato come POSTULATO** | ### **onesto e semplice** | ### **e' una manopola** *(`A1`)* |
| **un numero che EMERGE dalla geometria o dalla densita'** | ### **zero manopole** | ### **va derivato; oggi non c'e'** *(`MAPPA_DIPENDENZE.md:809`: «oggi NON esiste una costante che faccia da `alpha`, nascera' in `L4`»)* |
| **fissato da un'altra legge: il VUOTO come scala** *(la derivazione di `2026-10-12_u_arco_dinamica.md`: `E_mom = somma p_k^2/(2 sigma_k)`, `sigma_k` il vuoto sull'arco)* | ### **gia' scritta nell'era `2`; il vuoto non spinge `U`, ne decide l'INERZIA** | ### **dove il vuoto manca `E_mom` diverge** *(dichiarato la')*; ### **la costante diventa `~ 1/Lambda`: un rapporto del modello, non un numero** |

### **`[RACCOMANDAZIONE]` LA TERZA, da derivare:** ### **e' l'unica gia' in linea con `A1` e con una derivazione dell'era `2`; il prototipo la puo' provare accanto a un `e` dichiarato** *(come controllo)*. ### **La scelta e' di Luca.**

## 8. LE SCELTE DI LUCA

| la scelta | le alternative | `[RACCOMANDAZIONE]` |
|---|---|---|
| compatto o no | `1 - cos B` / `B^2/2` | **compatto** *(sezione `4`)* |
| `U(1)` separato da `SU(2)` o insieme in `U(2)` | `A` dinamico con `V` fermo / tutto `U(2)` dinamico *(`U-ARCO-DINAMICA`: `4` coordinate e `4` momenti per arco)* | **separato**: `A` dinamico, `V = I` fermo *(un interruttore alla volta, `CLAUDE.md` par.`3`)* |
| dove nel palindromo | al centro / agli estremi / dentro lo spostamento | **la spinta agli estremi, la deriva al centro, la sorgente DENTRO lo spostamento** *(Gauss esatto)* |
| quale carica | la norma `|psi|^2` *(Noether, `DEC-QC`)* / la carica di rotazione *(`A14.3`)* / `N+ - N-` *(non conservata)* | **la norma**, dichiarando che le due bande hanno la stessa carica |
| la costante | postulato / emergente / il vuoto come scala | **il vuoto come scala, da derivare** *(sezione `7`)* |
| il tempo del campo | dell'arco *(`B-3`)* / globale | **dell'arco**: il ritardo di Shapiro e il «zero manopole» |

## 9. LA CATENA DEI SIGILLI E LE MISURE DEL PROTOTIPO SUI TRIANGOLI *(in memoria, in `csv/`, come gli strumenti dei triangoli)*

| | la misura | DEVE passare | DEVE fallire *(la chiave giusta)* | PUO' fallire |
|---|---|---|---|---|
| `(a)` | `A = 0`, `E = 0`, accoppiamento acceso | **il passo uguale a quello di oggi AL BIT** | col campo `A != 0` costante su un ciclo *(un'olonomia)* lo spettro CAMBIA | -- |
| `(b)` | l'invarianza di gauge del passo intero *(una `chi` casuale)* | **le osservabili invarianti** *(`|psi|^2` per nodo, `B_p`, `E_a`)* **uguali entro `1e-12`** | trasformare SOLO `psi` *(non `A`)*: le osservabili cambiano | -- |
| `(c)` | la legge di Gauss a ogni tick, una corsa con materia | **`div E - e rho` entro `1e-12` a ogni tick** | togliere la sorgente dallo spostamento: Gauss si rompe | -- |
| `(d)` | la reversibilita' | **avanti `N` tick e indietro: lo stato di partenza entro `1e-12`** | -- | -- |
| `(e)` | l'energia di materia piu' campo | **costante al secondo ordine in `s`** *(la pendenza `~2`, come `M-B2`)* | -- | -- |
| `(f)` | **LA MISURA DECISIVA:** la dispersione delle onde libere e la loro velocita' per tempo proprio | **la banda di gauge a frequenza nulla; `c_U` isotropo entro `1e-3`** | -- | **`c_U = v_b` entro il `5%`** *(la previsione dice di no: `c_U/s = 1`)*; **`c_U = v_max` entro il `5%`** |
| `(g)` | il ritardo di Shapiro: un'onda in un gradiente di `cs` | **il ritardo segue `int ds/cs`** *(entro il `5%`)* | `cs` uniforme: nessun ritardo | -- |

## 10. IL PASSAGGIO ALLA FCC

- ### **CHE COSA CAMBIA:** ### **le placchette sono i triangoli delle facce del reticolo tetraedri-ottaedri** *(i cui vertici sono la FCC, `doc/PROGETTO_TRIANGOLI.md`)*: ### **ogni arco sta in `4` triangoli**; ### **i pesi dal complesso duale**
  *(i dodecaedri rombici)*; ### **DUE polarizzazioni del fotone**; ### **la legge di Coulomb `1/r^2` fra due cariche ferme, da MISURARE** *(con la dimensione del grafo, `doc/IPOTESI_gravita_a_spinta.md`)*; ### **`omega_max` e la condizione di
  Courant da ricalcolare.**
- ### **CHE COSA SI RIUSA:** ### **il passo del campo, la sorgente, i sigilli `(a)`-`(g)`, gli strumenti di `doc/PROGETTO_FCC.md`** *(la scena, la zona, la dispersione)*.

## 11. IL COSTO E L'ORDINE DEI MANDATI *(uno alla volta)*

### **IL METODO DELLA STIMA:** ### **i tempi della camminata misurati sui triangoli** *(`3.9`-`4.9 us` per nodo e tick, `stato_finale_R2T.txt`)*; ### **il campo aggiunge per tick `~3` archi e `2` placchette per nodo** *(qualche operazione ciascuno:
`~+30%`)*.

| il mandato | il costo stimato |
|---|---|
| `1.` il prototipo del campo LIBERO sui triangoli *(le variabili in memoria, il passo, la dispersione: `(d)`, `(f)`)* | **minuti** *(la dispersione e' lineare: per `k`, in secondi)* |
| `2.` l'accoppiamento con la materia: `(a)`, `(b)`, `(c)`, `(e)` | **minuti** |
| `3.` il ritardo di Shapiro `(g)` | **`~10` minuti** *(una striscia, `~400` tick)* |
| `4.` sulla FCC: la dispersione, le due polarizzazioni, Coulomb | **ore** *(dopo gli strumenti della FCC, `doc/PROGETTO_FCC.md`)* |

### ⚠ **E PRIMA DEL NUCLEO** *(`doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`, il passo `1`)*: ### **una legge nella tabella vuole la sua DECISIONE `presa`** *(il posto `A2`, `L4`; `DOMANDA-U-DINAMICA-LE-FORME` e' `AGENDA`)*: ### **il prototipo resta IN MEMORIA finche' Luca non decide.**
