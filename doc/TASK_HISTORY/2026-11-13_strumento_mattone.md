# 2026-11-13 — LO STRUMENTO «MATTONE»: LA SECONDA NAVE *(Luca `18:47`; le scelte di dettaglio DELEGATE AL GUARDIANO, `18:44`)*

> **Il ramo `strumento-mattone`, nel worktree `C:\Users\lpeano\soliton_simulator_mattone`.** **SOLO FILE NUOVI** *(in `csv/solitone/` e `doc/`)*: **nessun file del nucleo, nessuno script esistente modificato** *(si IMPORTANO)*.

## 0. IL MANDATO, COME ARRIVATO *(le regole e le scelte sono del guardiano, su delega di Luca; qui RIPRESE alla lettera nel senso)*

- **Il perche':** **il (G) brusco non e' leggibile** *(la risposta all'accensione)*; **la rampa di `500` tick e' piu' corta del respiro del solitone** *(il video triplo, (B): periodi di circa `1000` e `2000` tick)*, **quindi fa ancora onde.**
- **L'idea di Luca** *(`18:31`-`18:42`)*: **preparare UNA volta il solitone adattato ai campi, con un'accensione lunga `4000` tick, su un toro piccolo** *(`L 81`; `162 = 2 x 81`)*, **salvarlo e incollarne copie su `L 162`** *(«il mattone»)*; **per i tre casi di P6: G, U, G + U; utilizzabile anche con le leggi di `cs`** *(il lapse e' gia' una legge per `cs`: `cs = s N`)*. **Sul principale si va avanti col piano gia' mandato** *((Grampa), (GUrampa), (Uzero)), **che fara' da confronto.**
- ### **LE REGOLE R1-R6:**
  - **R1** il ramo parte dall'HEAD di `primo-ordine`, SOLO file nuovi; **R2** un worktree, la cartella del principale non cambia mai ramo; **R3** il registro `doc/REGISTRO_CORSE_mattone.md` *(stesso modulo, stesse regole)*, le tappe col prefisso `mattone-`, alla riunione in coda a quello del principale;
  - ### **R4 UNA MACCHINA SOLA:** **le corse COL LAPSE dei due rami non girano mai insieme;** **prima di aprirne una si controlla l'altro registro; il principale ha la precedenza;**
  - **R5** la riunione quando il controllo del metodo passa per i tre mattoni: un merge senza conflitti, con la suite, poi una riga nella ROTTA; **nessun braccio di P6 si rifa' coi mattoni senza un mandato nuovo;** **R6** commit e push dopo ogni pezzo su tutti e due i rami, nessuna riscrittura.
- ### **LE SCELTE S1-S8:**
  - **S1** il solitone di base *(sotto, sez. `1`)*; **S2** la rampa `r(k) = sin^2(pi k / (2 K))`, `K = 4000`, poi `1000` tick a campi pieni *(`5000` per mattone, a pezzi da `1000` con lo stato salvato)*; **S3** il lapse `N = 1/(1 + rho/rho_c)` col `rho_c` ASSOLUTO dei bracci di P6, `N_eff = 1 + r (N - 1)` nel tick vero e nelle copie;
  - **S4** la U(1) accesa piano: `e(k) = r(k) e*`, `e* = 6.315414e-05`; **a ogni tick `E` riscalato per `e(k+1)/e(k)`** *(cosi' `div E = e(k)(rho - media rho)` resta vera; all'inizio `E = A = 0`, `e = 0`)*; il residuo di Gauss ogni `250` tick; (MGU) le due rampe con l'adattatore di (G+U);
  - **S5 «calmo»:** l'ampiezza del respiro *(`rho max` / la densita' media del corpo, picco-picco)* **sugli ultimi `1000` tick sotto `0.30`** *(meta' di (B) del video triplo, `0.594`)* **e il centro fermo entro `0.2` nodi;**
  - **S6 il francobollo:** `R_t` = il raggio oltre il quale il `|dphi|` medio per anello resta sotto il `2%` di quello sull'anello del vuoto, non meno di `25`; il raccordo `cos^2` largo `4` nodi; le chiavi `psi` e `phi`; **la fase globale del vuoto allineata a quella di F3 fresco di `L 162` allo stesso tick**; per (MU), (MGU) **il campo NON si ritaglia: si RICALCOLA con Gauss sparso** *(`A = 0`)*;
  - **S7 il controllo del metodo:** un francobollo su `L 162`, `1000` tick coi suoi campi: il centro fermo entro `0.2` nodi; il respiro entro il `25%` di quello del mattone negli ultimi `1000` tick; **il salto di energia all'incollatura misurato** *(nessuna soglia)*;
  - **S8 l'ordine:** (MG); se calmo (MU) e (MGU); i tre controlli; la riunione.
- ### **I DEVE:** **la rampa spenta: i primi `20` tick = il tick col lapse di oggi AL BIT; `e = 0` (MU) = il tick senza campo AL BIT;** **un francobollo ritagliato e incollato SENZA spostarlo nel suo toro ridà lo stato dentro `R_t` entro `1e-12`;** **Gauss in (MU), (MGU) sotto `1e-10` a ogni controllo;** **DEVE FALLIRE: senza allineare la fase del vuoto il salto di energia e' maggiore.**
- ### **FERMO SOLO SE:** **un DEVE non va come deve; (MG) NON e' calmo** *(prima di (MU), (MGU))*; **un controllo del metodo fallisce; un conflitto alla riunione.**

- ### **IL MANDATO DELLE `18:58` CAMBIA DUE REGOLE** *(Luca `18:57`)*: **R4 SOSPESA** *(le corse col lapse dei due rami POSSONO girare insieme; sospesa anche la regola delle `17:22`)*; **il tetto delle corse col lapse `18000` s su tutti e due i rami;** **la PROTEZIONE** *(del guardiano)*: **a ogni tappa il tempo per tick e la memoria libera; sotto `2` GB si ferma la corsa del MATTONE** *(il principale ha la precedenza)*; **il riavvio: le corse interrotte si chiudono come INTERROTTE DAL RIAVVIO e si rifanno da capo.** **Il CALENDARIO della sez. `2` si legge con R4 sospesa.**

## 1. IL CONTROLLO S1: IL SOLITONE DI BASE *(dal codice, cercato per nome)*

- **`csv/solitone/corsa_accensione.py`:** **tutte le corse partono dalla stessa scena** *(`NOME = "BG-F-0.15"`: `_vuoto_vivo_B.CORSE` -> il solitone `BG`, il vuoto `fondo`, `s 0.15`; `V.EPS` `0.5`; lo zero `DC.ZERO`; la forma `VC.FORMA`)*; **TBS e S162/C35-*:** **il vuoto `F3`, il bordo di TB3** *(`BORDO[...] = BORDO["TB3"]`)*.
- ### **LE DIFFERENZE:** **il lato** *(TBS: `V.L = 81`; le coppie: `LCORSA = 162`)*; ### **la PARTENZA:** **TBS = la partenza SIMMETRIZZATA di TS** *(`partenza_ts`, `SIMMETRIZZATE`)*; **S162/C35 = la partenza di `V.partenza`, NON simmetrizzata** *(piu' la copia traslata di `d` lungo `A1` per le coppie)*.
- ### **LA SCELTA S1:** **la moneta e lo zero sono gli STESSI** *(lo stesso `V.CORSE[CA.NOME]`, `V.EPS`, `DC.ZERO`)*: **il mattone si prepara dal TBS di `L 81`**, **lo stato a `10000`** *(lo stato di partenza delle G1, integro nell'inventario di E: `ae69c52d`)*. ### **Dichiarato:** **il solitone del mattone e' quello SIMMETRIZZATO, non lo stesso di C35-pi:** **il controllo del metodo** *(S7)* **lo misura su `L 162` da solo, e il confronto coi bracci del principale lo deve tenere presente.**

## 2. IL PROGETTO DEL CODICE *(`csv/solitone/mattone.py`; solo file nuovi)*

- **`prepara(caso)`** *(caso in `MG`, `MU`, `MGU`)*: **la scena di TBS a `L 81`** *(come `s5_caduta_solitone`/`s5_g1_lunga`: lo stato a `10000`, il bordo di TB3)*; **`5000` tick a pezzi da `1000`** *(lo stato salvato su E: `E:\soliton_simulator\mattone\<caso>_<tick>.npz` con lo sha e i parametri accanto)*; **ogni `50` tick il centro, `rho max`, la densita' media del corpo, l'energia; ogni `250` il residuo di Gauss** *((MU), (MGU))*;
  - **il tick:** **(MG) `tick_lapse.tick` dentro `con_rampa(r(k))`** *(la stessa idea dell'adattatore del principale, `p6_bracci.con_rampa`, IMPORTATO)*; **(MU) `_u1_oggi.tick` con `e(k)`** *(il campo `Campo` col suo `e` aggiornato a ogni tick, `E` riscalato)*; **(MGU) `p6_bracci.tick_GU` dentro `con_rampa(r(k))` col campo a `e(k)`.**
- **`ritaglia(stato, centro)`**, **`incolla(stato_162, francobollo, posizione)`**: **S6.**
- **`controllo(caso)`:** **S7.**
- **Il collaudo `csv/solitone/test_mattone.py`:** **i DEVE di sopra che non vogliono una preparazione intera** *(la rampa spenta `20` tick; `e = 0`; il francobollo senza spostamento entro `1e-12`; il DEVE FALLIRE della fase su un francobollo incollato)*.
- ### **IL CALENDARIO** *(R4 e la decisione di Luca delle `17:22`: niente accanto a una corsa col lapse)*: **il codice si scrive mentre il principale corre; le suite e le preparazioni (MG), (MGU) SOLO quando il principale non ha una corsa col lapse aperta** *(il principale: `0L`, `UL` senza lapse; poi `Grampa`, `GUrampa` col lapse; poi `Uzero`)*; **(MU) non ha lapse: puo' girare accanto a un braccio SENZA lapse.**

## 3. IL COLLAUDO: `4/4` *(il codice a `f8e289fb`; dalle `20:21:02` alle `20:22:31`, accanto a `p6-Grampa` del principale)*

- **(MG) la rampa spenta = `tick_lapse.tick` AL BIT per `20` tick; (MU) `e = 0` = `accensione.tick` AL BIT** *(col bordo)*.
- **Il francobollo di TBS a `10000`:** **`R_t = 28`** *(l'anello del vuoto, il `|dphi|` medio massimo, e' il primo: `11.7`; il `|dphi|` resta fra `6` e `9` fino all'anello `17`, poi `3.3`, `0.80`, `0.35` e scende sotto il `2%` oltre il `25`)*; **`3697` nodi; incollato nello stesso stato: dentro `R_t` `psi` uguale, `phi` entro `8.9e-20`** *(il DEVE `1e-12`)*.
- **La fase del vuoto su `L 162`** *(incollato a `[80, 80]`, tick `60000`)*: **il salto di energia allineato `-52.54778`, NON allineato `-52.54783`: il DEVE FALLIRE fallisce come deve,**
  - ### ⚠ **MA E' DEBOLE:** **`Delta = 7.4e-05` rad soltanto:** **la fase del vuoto `c(t)` gira di `3 pi / 20` per tick, e fra il tick `10000` di TBS e il `60000` passano `50000` tick = `3750` giri INTERI: le due fasi coincidono gia'.** **Lo stesso nel controllo S7** *(dal mattone a `15000` al `60000`: `45000` tick, `3375` giri)*. ### **Il controllo non distingue a questi tick; per uno sensibile: incollare a un tick NON congruente** *(per esempio `60001`)*. **Un'osservazione, non un cambio del codice ora.**

## 4. (MG): CALMO *(il codice a `f8e289fb`; dalle `20:29:06` alle `21:17:02`, IN COPPIA con `p6-Grampa` del principale)*

- **`5000` tick in `2875` s** *(`0.55`-`0.57` s per tick in coppia; la memoria libera sempre sopra `8.2` GB nelle tappe del mattone)*; **gli stati su `E:\soliton_simulator\mattone\MG_01000` ... `MG_05000.npz`** *(lo sha di `psi_h` a `5000`: `15faeeb4`)*.
- ### **GLI ULTIMI `1000` TICK: il respiro `0.0711`** *(la soglia `0.30`)*, **il centro si sposta al piu' di `0.0680` nodi** *(la soglia `0.2`)*: ### **CALMO** *(S5)*.
- **Sotto il lapse il solitone si allarga:** **`rho max` da `3083` a `1388`;** **il rapporto del respiro scende da circa `1.71` a circa `1.43` durante la rampa;** **il centro scivola di circa `0.2` nodi lungo la seconda coordinata durante la rampa** *(da `40.503` a `40.698`)*; **`M` cala di `3.5e-4` relativo** *(il bordo)*.
- ### **IN COPPIA** *(la misura del parallelo, Luca `18:58`)*: **`Grampa` del principale nelle stesse ore `2.67`-`3.43` s per tick** *(le sue tappe)* **contro i `2.25`-`2.4` da solo; il mattone `0.55`-`0.57`.**
- **Poi (MU) e (MGU)** *(S8)*.

## 5. LA TRAPPOLA CRLF: IL COLLAUDO, (MG) E (MU) HANNO GIRATO CON `mattone.py` A BYTE NON COMMITTATI *(Luca, la segnalazione dopo `7d42ad11`; ERRORE MIO)*

- **Il timbro di `_presidio`** *(nelle uscite del collaudo, di (MG), di (MU))*: **`mattone.py sha1-BYTE e0ea8957 !! MODIFICATO rispetto a HEAD`** *(il blob committato: `sha1-BYTE c2107885`)*. ### **Non l'ho letto prima di lanciare.**
- ### **LA CAUSA:** **sul disco `mattone.py` ha le righe CRLF; nel commit `f8e289fb` git l'ha salvato LF** *(`.gitattributes`: `text eol=lf`, la decisione di Luca del `2026-09-16`)*. **Avevo ritoccato il file nello scratchpad con un `open(p, "w")` in modo testo su Windows, che scrive CRLF, e l'ho copiato cosi' nel worktree.** **`git status` era PULITO** *(git normalizza le newline nel confronto)*: **e' lo stato «stesso CONTENUTO, byte DIVERSI» di CLAUDE.md sez. `7`.**
- ### **IL DIFF, spiegato:** **SOLO le newline:** **`tr -d '\r' < mattone.py` e il blob di `f8e289fb` sono IDENTICI** *(`diff` vuoto)*; **nessuna istruzione diversa.** **`test_mattone.py` e `doc/INVENTARIO_mattone.md` hanno i byte uguali al commit** *(`c64c1058`, `b7f77fec`)*.
- ### **I BYTE CHE HANNO GIRATO, COMMITTATI** *(CLAUDE.md sez. `7`, lo stato 2: una COPIA ESATTA accanto ai dati)*: **`doc/referti_l2/mattone/mattone_girato_e0ea8957.py.gz`** *(gzip con `mtime 0`: un file di TESTO non puo' tenere i CR nel repo, per `.gitattributes`; i byte scompattati del blob nell'indice danno `sha1-BYTE e0ea8957`, verificato)*.
- **(MU)** *(dalle `21:17`, in corsa)* **gira con gli STESSI byte `e0ea8957`** *(il suo timbro)*.
- ### **LA REGOLA, da qui** *(Luca)*: **nessuna corsa del ramo mattone si apre con file modificati:** **prima di `apri` lo `sha1-BYTE` dal disco di ogni file del ramo contro il blob committato** *(non `git status`)*. **A (MU) finito, `mattone.py` si riscrive in LF dal blob** *(`git cat-file -p HEAD:csv/solitone/mattone.py`, in binario)* **e si ricontrolla il timbro prima di (MGU).**

## 6. (MU): CALMO *(i byte di `mattone.py` `e0ea8957`, la copia in `d83cb363`; dalle `21:22:55` alle `21:37:20`, accanto a `p6-Grampa`)*

- **`5000` tick in `864` s;** **gli ultimi `1000` tick: il respiro `0.0918`** *(la soglia `0.30`)*, **il centro al piu' `0.0232` nodi** *(`0.2`)*: ### **CALMO.**
- ### **Gauss: il residuo massimo sui controlli ogni `250` tick `2.703e-12`** *(il DEVE: sotto `1e-10`)*; **`K + V` a `5000` `5.89`; il residuo a `5000` `2.67e-12`.**
- **Dopo (MU):** **`mattone.py` riscritto coi byte del blob** *(`git cat-file -p HEAD:...`, in binario)*: **sul disco `sha1-BYTE c2107885` = il commit; `test_mattone.py` `c64c1058`, `doc/INVENTARIO_mattone.md` `b7f77fec` uguali;** **l'indice rinfrescato** *(`git add` del file identico)*. ### **(MGU) si apre coi byte committati.**

## 7. (MGU): CALMO; I TRE MATTONI CALMI *(i byte di `mattone.py` `c2107885` = il commit; dalle `21:43:51` alle `22:34:50`, in coppia con `p6-Grampa` poi `p6-GUrampa`)*

- **`5000` tick in `3059` s;** **gli ultimi `1000` tick: il respiro `0.0738`, il centro al piu' `0.0739` nodi:** ### **CALMO;** **Gauss: il massimo `5.684e-12`** *(sotto `1e-10`)*; **`K + V` a `4000` `4.19`.**
- ### **I TRE MATTONI** *(gli ultimi `1000` tick)*: **(MG) il respiro `0.0711`, il centro `0.0680`; (MU) `0.0918`, `0.0232`; (MGU) `0.0738`, `0.0739`** *(la soglia `0.30` e `0.2`)*. **Poi i controlli del metodo** *(S7)*, **uno alla volta.**
- **Un'annotazione al punto `5`** *(Luca, dopo `0818afe1`)*: ### **la segnalazione sui byte di `mattone.py` era un FALSO ALLARME del guardiano** *(errore n.149)*: **il contenuto che ha girato = quello committato** *(CRLF contro LF)*; **la copia `.gz` di `d83cb363` era quindi superflua** *(resta: nessuna riscrittura)*. **La regola resta, ma «modificato» si intende DOPO aver normalizzato i fine riga: il timbro si cambia sul principale** *(una funzione nuova in `csv/_presidio.py`, col suo DEVE)*, **quando le corse che lo usano sono chiuse.**

## 8. LA COPPIA DI MATTONI *(Luca `2026-11-13` `22:54`; dopo i tre controlli S7, PRIMA della riunione; le scelte del guardiano su delega)*: IL PROGETTO, PRIMA DEL CODICE

- **La decisione:** **due mattoni (MGU) UGUALI** *(fase `0`, spin su: lo stesso francobollo)* **sul vuoto di `L 162`; il mondo G+U** *(`rho_c` ASSOLUTO `227058.574864`, `e* = 6.3154140e-05`)*, **campi PIENI dal tick `0`, NESSUNA rampa; i centri come C35-pi a `60000`** *(`d0 = 37.569220`, la stessa direzione)*; **`2000` tick, il tetto `18000` s, lo stato ogni `500`; ogni `50` i centri, la distanza, il picco e la massa di ogni solitone.**
- **Le scelte** *(del guardiano)*: **la materia per SOMMA dei `psi` ritagliati; il vuoto per PRODOTTO delle deformazioni** *(`phi = phi_F3 x prodotto_i (phi_i / phi_F3)`, la fase allineata come in S6)*; **la massa di ogni francobollo oltre `18.8` nodi scritta; U ricalcolata con Gauss** *(`A = 0`)*.
- ### **LE MIE LETTURE** *(dichiarate)*:
  - **il prodotto si costruisce PARTENDO dalla prima incollatura** *(`phi_1` = il francobollo `1` incollato sul vuoto fresco, come S6)* **e moltiplicando per `phi_i / phi_F3` dei successivi:** **con UN francobollo e' l'incollatura di S6 AL BIT** *(`phi_F3 x (phi_1 / phi_F3)` non lo sarebbe: `(a / b) b` non e' `a` al bit)*;
  - **«poi `|phi_j|^2 = 1`»: lo leggo come un CONTROLLO sul vuoto lontano dai due solitoni** *(lontano il prodotto torna a `phi_F3`)*, **NON come una rinormalizzazione** *(che cancellerebbe i buchi del vuoto)*: **si stampa `|phi_j|^2` mediano fuori da `R_t + 4` dai due centri;**
  - **i centri:** **quelli di C35-pi a `60000`** *(i semipiani, come P6)*, **arrotondati al nodo PIU' VICINO con lo spostamento multiplo di `3`** *(il disegno di fase di F3)*: **la `d0` effettiva si stampa;**
  - **la scena:** **quella di C35-pi** *(il suo bordo)*, **il vuoto fresco al tick `60000`;** **il mattone: (MGU) a `5000`** *(`E:\soliton_simulator\mattone\MGU_05000.npz`)*.
- ### **I DEVE:** **con UN solo francobollo, la somma e il prodotto = l'incollatura di S6 AL BIT** *(`psi` e `phi`)*; **il residuo di Gauss sotto `1e-10` a ogni controllo** *(ogni `250` tick)*.
- **Il referto:** **l'accelerazione relativa in quattro finestre** *(`0-500`, `500-1000`, `1000-1500`, `1500-2000`: la parabola di `d` in ciascuna; forza costante o colpetto?)*; **il picco dei due solitoni contro quello del mattone** *(gli ultimi `1000` tick di (MGU))*.
- **Il codice:** **un file NUOVO, `csv/solitone/mattone_coppia.py`** *(importa `mattone.py`, che in quel momento serve al controllo S7 in corsa: non si tocca)*. **Poi la riunione** *(R5)* **e FERMO su tutti e due i rami.**

## 9. IL CONTROLLO DEL METODO DI (MG): FALLISCE -- FERMO DELLA CATENA DEL MATTONE *(il codice a `f8e289fb`, i byte `c2107885`; dalle `22:39:41` alle `23:21:27`, in coppia con `p6-GUrampa`)*

- **Il francobollo di `MG_05000.npz`:** **`R_t = 32`** *(l'anello del vuoto il `5`; quello di TBS a `10000` era `28`: il solitone sotto il lapse e' piu' largo)*, **`4693` nodi; incollato a `[80, 80]` nella scena di S162** *(il suo solitone a `(81.58, 81.34)`)*.
- **Il salto di energia all'incollatura:** **`+11.18239` allineato** *(`Delta = 1.39e-04`)*, **`+11.18238` non allineato** *(la fase quasi nulla: i tick congruenti, sez. `3`)*.
- ### **`1000` tick in `2471` s:** **il centro si sposta al piu' di `0.0785` nodi** *(la soglia `0.2`: PASSA)*; ### **il respiro `0.1068` contro quello del mattone `0.0711`: il rapporto `1.502`, la tolleranza `25%`: FALLISCE.**
- ### **FERMO** *(il mandato delle `18:47`: «FERMO SOLO SE un controllo del metodo S7 fallisce»)*: **NON si fanno i controlli di (MU) e (MGU), NON la coppia di mattoni** *(anche la decisione delle `22:54` si ferma su un S7 fallito)*, **NON la riunione.** **Nessuna correzione.**
- **Una lettura possibile, NON verificata** *(guardiano, per Luca)*: **su `L 162` il mattone si trova in una scena diversa** *(il bordo di S162, piu' largo; il vuoto di `L 162`; il francobollo tagliato a `R_t + 4` con la coda raccordata)*; **un respiro piu' ampio del `50%` dice che l'incollatura lo scuote: il «mattone calmo» non resta calmo trapiantato.** **Quanto pesino il taglio, il raccordo o la scena, non lo so.**
- **Continuano, perche' non dipendono da S7:** **il mandato delle `23:22`** *(perche' il lapse allarga il solitone: `mattone_rhoc.py`, (MGx2), (MG/2))* **e il ramo principale.**

## 10. PERCHE' IL LAPSE ALLARGA IL SOLITONE: DUE MATTONI (MG) CON `rho_c` DIVERSO *(Luca `2026-11-13` `23:22`; le scelte L1-L5 del guardiano su delega)*: IL PROGETTO, PRIMA DEL CODICE

- **I fatti** *(dai referti)*: **col lapse il picco cala di circa il `57%` a massa ferma, nello stesso modo in (MG) `3300 -> 1388`, (MGU) `3300 -> 1396` e `Grampa` `2787 -> ~1200`; senza lapse (MU) resta `3100`-`3300`.** **Al centro `N` circa `0.987`: l'`1.3%` di orologio piu' lento DIMEZZA il picco.**
- ### **L'IPOTESI** *(del guardiano)*: **in `2D` il solitone potrebbe stare «in bilico»** *(come la Schrodinger non lineare cubica, per cui `2D` e' la dimensione critica)*: **la risposta al lapse a SOGLIA, non proporzionale; l'alternativa: un equilibrio normale, risposta graduale.**
- **L1-L5** *(del guardiano)*: **(MG/2) `rho_c = 113529.287432`, (MGx2) `rho_c = 454117.149728`, IDENTICI a (MG) per il resto; un file NUOVO `csv/solitone/mattone_rhoc.py` che cambia SOLO `rho_c`; ogni `50` tick il RAGGIO e `N` al centro; il raggio di (MG) dagli stati salvati; la lettura `A(f) = 1 - picco finale / iniziale`: `A(MGx2) >= 0.75 A(MG)` SOGLIA, `<= 0.6 A(MG)` GRADUALE, fra le due INDECISO; (MG/2) oltre `2` volte il picco iniziale: COLLASSO** *(un risultato, non un errore)*; **al piu' due corse col lapse alla volta fra i due rami.**
- ### **LE MIE SCELTE** *(dichiarate)*: **i nomi: (MGx2) = `MGdoppio`, (MG/2) = `MGmezzo`** *(`/` non sta in un nome di file o del registro)*; **il raggio dentro `R_t = 28` FISSO** *(il `R_t` di TBS a `10000`; il `R_t` cambia sotto il lapse, `32` per `MG_05000`: fisso e' confrontabile)*; **`N` al centro = `mot.cs / s` del tick vero al nodo del centro arrotondato;** **per (MG) `N` dalla legge sul picco** *((MG) non salvava `cs`)*; **il ciclo di `mattone.prepara` COPIATO in `mattone_rhoc.corsa`** *(`prepara` non e' parametrica in `rho_c`; `mattone.py` non si tocca)*.
- ### **I DEVE:** **col `rho_c` di (MG) i primi `20` tick del ciclo = (MG) AL BIT;** **`N` al centro a piena rampa coerente con la legge entro `1e-3`** *(mio, dichiarato)* **e vicino ai valori di Luca** *((MG/2) `0.974`, (MGx2) `0.993`, entro `0.005`, mio)*.
- **L'ordine:** **il collaudo, la suite, il commit; il raggio di (MG) dagli stati; (MGx2) poi (MG/2) quando c'e' un posto col lapse** *(il principale: `GUrampa` in corsa)*; **il referto unico; FERMO solo per questa voce.**
- **La catena del mattone resta FERMA** *(sez. `9`: il controllo S7 di (MG) fallito)*: **questa voce non dipende da S7.**

## 11. `rho_c`: IL COLLAUDO `3/3` E IL RAGGIO DI (MG) *(il codice a `9aa5ed96`; alle `00:04`-`00:05`)*

- **Il collaudo:** **col `rho_c` di (MG) i primi `20` tick del ciclo di `mattone_rhoc` = (MG) AL BIT;** **`N` al centro a piena rampa** *(la legge sul nodo del centro di TBS a `10000`, `rho` `3338.45`)*: **`MGdoppio` `0.992703` contro la legge `0.992702`** *(Luca: circa `0.993`)*; **`MGmezzo` `0.971435` contro `0.971434`** *(Luca: circa `0.974`; il centro ha `rho 3338`, non `3000`)*.
- ### **IL RAGGIO DI (MG)** *(dagli stati salvati, dentro `R 28`)*: **`8.249` (`k 0`), `8.569`, `9.724`, `10.607`, `10.851`, `11.268` (`k 5000`)** *(1.37 volte)*; **il picco `3350 -> 2909 -> 1897 -> 1544 -> 1510 -> 1388`; `N_eff` al centro dalla legge `1.000 -> 0.9939`.**
- **Poi `MGdoppio`, poi `MGmezzo`** *(quando c'e' un posto col lapse)*.

## 12. LA GIORNATA (Luca `2026-11-14` `00:53`): IL FERMO SCIOLTO; S7' RIVISTO DOPO IL FALLIMENTO; IL BIVIO

- **Il FERMO della catena** *(sez. `9`, `dbfbaf31`)* **e' SCIOLTO dal mandato delle `00:53`, nei modi scritti li'.**
- ### **ERRORE DEL GUARDIANO n.154:** **S7 confrontava i `1000` tick SUBITO dopo l'incollatura** *(con l'assestamento dentro)* **con gli ultimi `1000` tick gia' calmi del mattone: due misure NON omogenee.**
- ### **LA REVISIONE S7'** *(decisa dal guardiano su delega di Luca alle `00:53`, DOPO aver visto il fallimento; scritta esattamente cosi')*: **il francobollo incollato su `L 162`, `1250` tick; i primi `250` sono l'ASSESTAMENTO** *(misurati e scritti, non giudicati)*; **il giudizio sui tick `250`-`1250`: il respiro entro il `25%` di quello del mattone negli ultimi `1000` tick della preparazione, il centro fermo entro `0.2` nodi.**
- **A1:** **la serie del respiro di `ctrl_MG` NON e' salvata** *(`mattone.controllo` la teneva in memoria e stampava solo il finale)*: **si RIFA' il controllo di (MG) con S7' in un file NUOVO, `csv/solitone/mattone_ctrl2.py`** *(il ciclo di `mattone.controllo` COPIATO; `mattone.py` non si tocca: e' in uso da `mattone_rhoc`)*, **`1250` tick, la serie del respiro e del centro ogni `50` in `doc/referti_l2/mattone/ctrl2_<caso>_serie.npz`;** **il respiro in quattro finestre da `250` tick** *(cinque: `0`-`1250`)*.
  - ### **DEVE** *(la riproducibilita')*: **i primi `1000` tick = il controllo S7 di prima** *(il respiro `0.1068`, lo spostamento `0.0785`, a tutte le cifre stampate)*.
- ### **A2, IL BIVIO:** **se (MG) PASSA S7': S7' per (MU) e (MGU); poi la coppia di mattoni** *(i primi `250` tick dichiarati come assestamento nella tabella delle forze)*; **poi la riunione** *(R5, con la suite)*; **poi FERMO.** **Se NON passa: il referto col respiro per finestre e FERMO della catena** *(nessun rodaggio, nessun mattone nuovo senza Luca)*.
- **A3:** **i mattoni con `rho_c` diverso continuano** *(`MGdoppio` in corsa dalle `00:43`, poi `MGmezzo`)*.
- **C1:** **al piu' DUE corse col lapse alla volta fra i due rami; il principale ha la precedenza** *(il bilancio di `Grampa` prima di S7')*.

## 13. PERCHE' IL LAPSE ALLARGA IL SOLITONE: IL REFERTO UNICO *(`doc/referti_l2/mattone/rhoc.txt`; `MGmezzo` dalle `01:34:46` alle `02:18:59`, in coppia con `bilancio-Grampa`)*

| il caso | `rho_c` | il picco `k 0` -> `5000` | il raggio | `N` al centro alla fine | `A(f)` | il respiro |
|---|---|---|---|---|---|---|
| (MG) | `227058.575` | `3350 -> 1388` | `8.249 -> 11.268` | `0.9939` | `0.5856` | `0.0711` |
| (MGx2) `MGdoppio` | `454117.150` | `3350 -> 1840` | `8.249 -> 10.136` | `0.9961` | `0.4506` | `0.0765` |
| (MG/2) `MGmezzo` | `113529.287` | `3350 -> 1035` | `8.249 -> 13.080` | `0.9919` | `0.6910` | `0.0813` |

- **La massa quasi ferma in tutti e tre** *(da `9.9694e+05` a `9.9625`-`9.9643e+05`: il bordo)*.
- ### **LA LETTURA L4** *(le soglie del guardiano `0.75` e `0.6`, dichiarate)*: **`A(MGx2) / A(MG) = 0.7695`: RISPOSTA A SOGLIA** *(compatibile col bilico)*; ### ⚠ **a `0.02` dal limite** *(`0.75`)*: **una lettura al confine, non netta.**
- **(MG/2): NESSUN collasso** *(il picco non cresce: si allarga di piu', `A = 0.691`)*.
- **Un fatto, non una lettura:** **raddoppiando `rho_c` il lapse al centro alla fine si dimezza circa** *(`1 - N`: `0.0061`, `0.0039`, `0.0081`)* **mentre `A` cambia meno** *(`0.586`, `0.451`, `0.691`)*: **l'allargamento riduce `rho` e quindi il lapse che il solitone sente.**
- ### **FERMO per questa voce** *(il mandato delle `23:22`)*. **Il resto del ramo continua:** **S7' di (MG).**

## 14. S7' DI (MG): NON PASSA -- FERMO DELLA CATENA (A2) *(il codice a `24c6dfd2`; dalle `02:23:54` alle `03:07:21`, in coppia con `bilancio-Grampa`)*

- **S7' dichiarato come revisione decisa DOPO il fallimento di S7** *(Luca `00:53`; sez. `12`)*.
- **Il francobollo come in S7** *(`R_t 32`, `4693` nodi, incollato a `[80, 80]`; il salto di energia `+11.18`)*; **`1250` tick in `2573` s.**
- ### **DEVE, la riproducibilita': PASSA** *(i primi `1000` tick: il respiro `0.1068`, il centro `0.0785`, come S7 a `4` cifre)*.
- ### **IL RESPIRO PER FINESTRE DI `250` TICK:** **`0`-`250` `0.0749`** *(l'assestamento, non giudicato)*; **`250`-`500` `0.0677`; `500`-`750` `0.0792`; `750`-`1000` `0.0635`; `1000`-`1250` `0.0425`;** **il centro sempre entro `0.024` nodi per finestra.**
- ### **IL GIUDIZIO S7'** *(tick `250`-`1250`)*: **il respiro `0.1193` contro il mattone `0.0711`: il rapporto `1.677`, la tolleranza `25%`: NON PASSA;** **il centro `0.0839`** *(passa)*.
- ### **UN'OSSERVAZIONE, che NON cambia il verdetto** *(guardiano, per Luca)*: **finestra per finestra il respiro e' simile o PIU' PICCOLO di quello del mattone, e cala nell'ultima** *(`0.0425`)*; **sui `1000` tick e' grande perche' il LIVELLO MEDIO del rapporto si sposta piano** *(`1.42` -> `1.51`, ogni `250` tick)*: **un'oscillazione lenta, piu' lunga di `250` tick. Il mattone su `L 81` misurava il picco-picco degli ultimi `1000` tick: le due misure contano la stessa cosa solo se l'oscillazione lenta e' uguale nei due tori.**
- ### **FERMO DELLA CATENA** *(il bivio A2: «se (MG) NON PASSA S7': referto col respiro per finestre e FERMO; nessun rodaggio, nessun mattone nuovo senza Luca»)*: **NON si fanno S7' per (MU) e (MGU), NON la coppia, NON la riunione.**

## 15. IL MATTONE BEN COTTO, LE DUE COPPIE, LA RIUNIONE (Luca `2026-11-14` `09:34`): LE PREMESSE E IL PROGETTO, PRIMA DEL CODICE

- **Il FERMO della catena** *(sez. `14`, `94259b8f`)* **e' SCIOLTO dal mandato delle `09:34`, nei modi scritti li'.** **Le scelte di dettaglio sono del guardiano** *(Luca)*; **quelle che restano a me sono scritte qui sotto come MIE.**
- ### **GLI ERRORI DEL GUARDIANO, come scritti nel mandato:** **n.155** *(il respiro «da picco a picco su `1000` tick» mescola l'oscillazione con la deriva lenta)*; **n.156** *(la lettura L4 costruita su `A`, che satura a `1`, invece che sul raggio)*; **n.157** *(la tolleranza della massa `1e-12`: e' del principale)*. **Le correzioni sono decise DOPO aver visto i risultati, e si scrivono cosi'.**

### 15.1 LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- **Gli stati di (MG) e (MGU) a `4000` e `5000` ci sono su E:** *(`MG_04000.npz` ... `MGU_05000.npz`; `campo_A`, `campo_E` per (MGU))*. **A `k >= 4000` `r_di(k) = 1`:** **i tick `4001`-`5000` di `mattone.prepara` sono gia' a campi pieni**, **quindi la ripartenza da `04000` deve ridare `05000` AL BIT** *(il DEVE del mandato)*.
- ### **COSA NON SO:** **se il tick col lapse tiene uno stato che NON sta nel npz** *(`mot.cs`: il bilancio lo salvava a parte, «il cs del tick»)*. **Se `tick_lapse` lo ricalcola a ogni tick dallo stato, la ripartenza e' esatta; se no, il DEVE fallisce, e allora: referto e FERMO.** **Per (MGU): `campo.e` e `e_prec` si rimettono a `e*`** *(cosi' `E *= e / e_prec` moltiplica per `1.0` esatto, come in `prepara`)*.
- **Il respiro:** **la serie e' `rho max x (somma rho) / somma rho^2`** *(`mattone.respiro`: il picco diviso la densita' media pesata del corpo)*, **quella del mandato.**
- **Il raggio:** **`mattone_rhoc.raggio`** *(la radice del secondo momento di `rho` entro `28` nodi dal centro, come R-CONTI-3)*, **ripreso, non riscritto.**
- **`conti.py` sta SOLO sul principale** *(`db57e4df`)*: **R-CONTI vuole le tabelle dei conti nelle corse nuove** *(la cottura, S7'', le coppie)*. ### **MIA SCELTA: lo COPIO identico sul ramo** *(lo stesso blob `sha1-BYTE d57ce3d4`)*: **alla riunione due file uguali non fanno conflitto.**

### 15.2 IL PROGETTO *(le scelte MIE sono marcate)*

- **A1, `csv/solitone/mattone_cottura.py`** *(nuovo; importa `mattone.py`, che NON si tocca)*: **`cuoci --caso MG|MGU`:**
  1. ### **IL DEVE della ripartenza, PRIMA della cottura e nella stessa corsa:** **da `<caso>_04000` `1000` tick = `<caso>_05000` AL BIT** *(tutte le chiavi dello stato, e `campo_A`, `campo_E` per (MGU))*. **Se fallisce: la corsa si ferma, referto e FERMO.**
  2. **da `<caso>_05000`, a pezzi di `1000` tick, lo stato a fine pezzo su E:** *(`<caso>_06000.npz`, ...; il meta dice il codice)*; **«COTTO» quando, fra due pezzi CONSECUTIVI DELLA COTTURA, la media del picco cambia meno del `2%` E la media del raggio meno dell'`1%`;** **al piu' `10` pezzi** *(`10000` tick)*. ### **MIA SCELTA: i pezzi confrontati sono SOLO quelli della cottura** *(il pezzo `4000`-`5000` di `prepara` non ha la serie del raggio per (MGU))*: **il primo giudizio dopo `2000` tick.**
  3. ### **MIA SCELTA: il respiro, il picco, il raggio, il centro ogni `10` tick** *(non `50`: una finestra di `250` tick con `6` punti da' un picco-picco grezzo)*; **S5' si scrive ANCHE sulla serie presa ogni `50`, per il confronto coi mattoni vecchi.**
  4. **le tabelle R-CONTI** *(un solitone: la deriva del centro, il picco, il raggio ogni `500` tick; i conti all'inizio, ogni `500` e alla fine: la materia del solitone e fuori, il vuoto del solitone e lontano, `K + V`, `tot`, l'energia uscita dal bordo, il residuo `tot(t) - tot(0) + bordo`)*; ### **l'energia come MEDIA sugli ultimi `100` tick** *(C5; a `k 0` il valore del tick, dichiarato)*: **`tot` e i pezzi per nodo a OGNI tick** *(serve comunque per il bordo)*.
  5. **lo stato cotto si scrive in `doc/referti_l2/mattone/cottura_<caso>.json`** *(il file, `k`, la serie)* **e lo leggono S7'' e le coppie.**
- **A2, S5':** **la serie del respiro; in ogni finestra di `250` tick** *(gli estremi COMPRESI, come `mattone_ctrl2`)* **si toglie la RETTA dei minimi quadrati di QUELLA finestra** ### *(MIA LETTURA di «la tendenza lineare tolta»: la retta per finestra, non una sola su tutta la serie)*, **poi il picco-picco; il respiro e' il MASSIMO delle ultime quattro finestre.** **`mattone_cottura.py letture`: S5' dalle serie salvate** *((MG), (MU), (MGU), `MGdoppio`, `MGmezzo`, e `ctrl2_MG` sui tick `250`-`1250`)*, **accanto ai vecchi numeri; nessuna corsa.**
  - ### **DEVE:** **S5' di (MG) a `5000` ricalcolato dalla serie salvata, scritto accanto al vecchio `0.0711`.**
  - **C6 (sul ramo, perche' il referto e' qui):** **le stesse `letture` stampano il paragrafo del raggio** *(n.156)*: **gli aumenti del raggio di `MGdoppio`, (MG), `MGmezzo` dalle serie, i rapporti per raddoppio di `rho_c`, la potenza** *(`log2` del rapporto)*. ### **MIA SCELTA: il paragrafo sta in un file ACCANTO** *(`doc/referti_l2/mattone/rhoc_raggio.txt`)* **e `rhoc.txt` resta l'uscita del suo comando** *(un referto si rigenera con un comando: un paragrafo a mano dentro non avrebbe provenienza)*.
- **A3, S7'', `csv/solitone/mattone_ctrl3.py`** *(nuovo; come `mattone_ctrl2`)*: **il francobollo del mattone COTTO su `L 162`, `1250` tick, i primi `250` l'assestamento; il giudizio sui `250`-`1250`: S5' entro il `25%` di S5' del mattone cotto** *(le ultime quattro finestre della cottura)*; **il centro fermo entro `0.2` nodi; la media del picco fra `250`-`750` e `750`-`1250` cambia meno del `2%`.** **(MG) e (MGU) in parallelo. (MU) si salta** *(non serve alle coppie)*. **Le tabelle R-CONTI come nella cottura.**
- **B, le due coppie, `csv/solitone/mattone_coppia.py`** *(c1740faa, MAI girato: si modifica, dichiarato)*: **`--mondo G|GU`:** **G = due (MG) cotti, `Campi` col caso `MG` a `r = 1`; GU = due (MGU) cotti, il caso `MGU`.** **I centri di C35-pi a `60000`, il nodo piu' vicino multiplo di `3`; `d0` vera stampata; la materia per somma, il vuoto per prodotto; `2000` tick; `d` e i centri ogni `10` tick** ### *(MIA SCELTA, come sopra)*.
  - ### **LA TABELLA DELLE FORZE in finestre di `250` tick** *(il mandato; R-CONTI-2 diceva `500`: per queste corse vale il mandato, dichiarato)*, **la prima l'assestamento.**
  - ### **B3, LA LETTURA** *(le soglie del guardiano, dichiarate nel mandato)*: **`d''` dalla parabola di `d` sui tick `250`-`2000`** *(`carta_coppia.curvatura`, come i bracci)*; **«G E' UNA FORZA» se positiva oltre `3` errori E almeno il `30%` di `Grampa`; «ERA IL COLPETTO DELL'ALLARGAMENTO» se in valore assoluto sotto il `10%`; in mezzo «INDECISO».** **I riferimenti `Grampa` e `U_2000` si LEGGONO dal referto dei bracci del principale** *(`git show 8ca61a34:doc/referti_l2/p6_bracci.txt`, non ricopiati)*. ### ⚠ **I due numeri non sono omogenei:** **`Grampa` e' `d_G - d_0` (tolta la coppia senza campi); la coppia di mattoni e' `d''` CRUDO** *(non c'e' la coppia di mattoni senza campi)*: **il confronto vale per il SEGNO e l'ORDINE di grandezza** *(come dice il mandato per il TBS)*.
  - **In GU: la stessa lettura, e l'additivita': `d''(GU) - d''(G)` contro `(U) = U_2000 - 0_2000`, scritta.**
  - **DEVE: un solo francobollo, la somma e il prodotto = l'incollatura di S6 AL BIT, nei due mondi; il residuo di Gauss sotto `1e-10` in GU.**
- **D, la riunione:** **quando S7'' e' passato per (MG) e (MGU) e B1, B2 hanno il referto: il merge del ramo in `primo-ordine`, la suite, una riga nella ROTTA; poi FERMO.**

### 15.3 COSA MI FAREBBE FERMARE

- **il DEVE della ripartenza fallisce; un mattone non e' cotto dopo `10000` tick; S7'' fallisce per (MG) o (MGU); un DEVE delle coppie fallisce; un conflitto alla riunione.** **In ognuno: il referto, senza correggere, e FERMO.**

### 15.4 TODO

1. questo task history, commit e push;
2. il codice: `conti.py` copiato, `mattone_cottura.py`, `mattone_ctrl3.py`, `mattone_coppia.py` modificato, l'inventario; la suite; commit e push;
3. `letture` *(A2, C6)*; le corse `cottura-MG` e `cottura-MGU` insieme, col registro;
4. S7'' di (MG) e (MGU) insieme; poi B1 e B2 insieme;
5. i referti; la riunione; FERMO.

### 15.5 LA DECISIONE DI LUCA DELLE `09:38`: SOLO IL MONDO G+U *(arrivata durante la prima suite del codice, che ho FERMATO: girava sul codice di prima)*

- **Si tolgono: la cottura di (MG), S7'' di (MG), la coppia B1.** **Resta: la cottura di (MGU) (A1), S5' (A2, anche per i mattoni gia' fatti), S7'' di (MGU) (A3), la coppia B2.**
- ### **B3 applicata a B2** *(Luca)*: **`d''` sui tick `250`-`2000`: «G E' UNA FORZA» se positiva oltre `3` errori E almeno il `30%` di `GUrampa` *(`+6.89e-07`)*; «ERA IL COLPETTO DELL'ALLARGAMENTO» se entro `3` errori da `U_2000` *(`-2.55e-08`)*; altrimenti «INDECISO».**
  - ### **MIA SCELTA: «entro `3` errori da `U_2000`» con l'errore della differenza IN QUADRATURA** *(quello della coppia e quello di `U_2000`; il secondo e' `3.4e-10`, trascurabile)*. **I riferimenti `GUrampa`, `U_2000` letti col `git show` dal referto dei bracci a `8ca61a34`.**
  - **L'additivita' con B1 cade** *(B1 non c'e')*: **il comando `--mondo additivita` tolto.**
- **La riunione D1: quando S7'' di (MGU) e' passato e B2 ha il referto. C ed E invariati.** **Una sola corsa col lapse sul ramo alla volta, quindi niente `--forza` sul registro.**

### 15.6 LA COTTURA DI (MGU): IL DEVE DELLA RIPARTENZA FALLISCE -- FERMO DELLA CATENA *(il codice a `cef29e39`; dalle `10:11:02` alle `10:18:56`; il referto `doc/referti_l2/mattone/cottura_MGU.txt`)*

- ### **DEVE: da `MGU_04000` `1000` tick = `MGU_05000` AL BIT: FALLISCE** *(in `465` s)*: **diverse `Lambda`, `phi_h`, `psi_h`, `rho`, `campo_A`, `campo_E`.** **La cottura NON e' partita** *(nessuno stato nuovo, nessuna serie)*.
- ### **LA PREMESSA CHE CADE** *(sez. `15.1`, «cosa NON so»)*: **lo stato del mondo G+U NON sta tutto nel npz.**
- ### **UNA LETTURA DAL CODICE, NON VERIFICATA** *(guardiano, per Luca)*: **`_u1_prototipo.avvolto` riscrive `mot.geo.U` dal campo** *(`scrivi_U`, dopo il primo `CAMM-SPOSTAMENTO-VUOTO` del tick)* **e all'uscita rimette SOLO `mot.operatori`, non `U`:** **il tick dopo parte con l'`U` lasciato dal tick prima** *(in `cs_al_centro`, le copie del punto fisso girano SENZA `avvolto`, e la prima parte del tick vero prima della riscrittura)*. **Alla ripartenza `mattone.scena.metti` rimette l'`U` della SCENA** *(senza campo)*: **il tick `4001` rifatto parte da un `U` diverso da quello di `prepara`.** **Il nucleo stesso tratta `geo.U` come stato** *(`primo_ordine/_collauda_checkpoint.py` lo confronta nella ripresa)*.
  - **Se e' cosi', la cura sarebbe salvare `mot.geo.U` nel npz** *(o rifarlo dal campo alla ripartenza)*: ### **NON la faccio** *(il mandato: un DEVE che fallisce = referto senza correggere, e FERMO)*. **E vale anche per (MG)?** **No per questa via:** **in (MG) non c'e' `avvolto`; non e' provato** *((MG) e' tolto dalle `09:38`)*.
  - ### ⚠ **Una conseguenza da guardare:** **anche S7', la coppia di `c1740faa` e ogni incollatura in G+U partono con l'`U` della scena** *(col campo rifatto con Gauss e `A = 0`: se l'`U` della scena coincide con quello di `A = 0` NON l'ho verificato; il caso che rompe di sicuro e' la ripartenza da uno stato con `A != 0`)*.
- ### **FERMO DELLA CATENA** *(il mandato: «FERMO SOLO SE un DEVE non va come deve»)*: **NON si fanno la cottura, S7'' di (MGU), la coppia B2, la riunione.** **Il resto che NON dipende dalla cottura continua:** **C** *(la chiusura della voce `15`, sul principale)* **e A2/C6** *(le letture dalle serie salvate)*.

### 15.7 A2 E C6: LE LETTURE DALLE SERIE SALVATE *(il codice a `cef29e39`; alle `10:42`; `doc/referti_l2/mattone/s5p_letture.txt`, `rhoc_raggio.txt`)*

| il mattone | S5' a `5000` | il vecchio *(picco-picco su `1000` tick)* |
|---|---|---|
| (MG) | `0.0481` | `0.0711` |
| (MU) | `0.0572` | `0.0918` |
| (MGU) | `0.0646` | `0.0738` |
| `MGdoppio` | `0.0419` | `0.0765` |
| `MGmezzo` | `0.0522` | `0.0813` |
| S7' di (MG), tick `250`-`1250` | `0.0615` | `0.1193` |

- ### **DEVE: S5' di (MG) a `5000` accanto al vecchio `0.0711` (riletto dalla stessa serie): PASSA** *(`1/1`)*.
- **Con S5' il controllo S7' di (MG) darebbe il rapporto `1.278`** *(descrittivo: oltre il `25%` anche cosi'; S7' e' chiuso, e (MG) e' tolto dalle `09:38`)*.
- ### ⚠ **Le serie vecchie sono prese ogni `50` tick: una finestra di `250` ha `6` punti, e il picco-picco senza la retta e' GROSSOLANO** *(le finestre di (MGU) vanno da `0.0173` a `0.0646`)*. **Le corse nuove le prendono ogni `10`** *(sez. `15.2`)*.
- **C6, il raggio** *(n.156)*: **gli aumenti `+1.887` (MGx2), `+3.019` (MG), `+4.831` (MG/2); il rapporto per ogni dimezzamento di `rho_c` `1.600` e `1.600`, la potenza `0.678`:** **la risposta e' GRADUALE; l'ipotesi «in bilico» NON e' confermata.** **Il file accanto a `rhoc.txt`, che resta l'uscita del suo comando.**

## 16. LA GEOMETRIA NASCOSTA: PERDITA VERA O SOLO RIPARTENZA? (Luca `2026-11-14` `11:26`) -- LA CARTA G1, DAL CODICE, PRIMA DELLE PROVE

- **Il FERMO della catena** *(`60940fc4`)* **e' SCIOLTO SOLO per questo mandato.** **Le scelte di dettaglio sono del guardiano; le mie sono marcate.**

### 16.1 LE PREMESSE DAL CODICE *(cercate per nome di funzione)*

- **CHE COSA E' `mot.geo.U`:** **il trasporto `2 x 2` di ogni ARCO** *(`primo_ordine/motore.py`, `Geometria`)*. **Nelle scene di C35-pi e di TBS e' l'IDENTITA'** *(`p6_bracci.braccio` lo asserisce: «la scena NON ha `U = I`»)*.
- **DOVE LO SCRIVE `avvolto`** *(`csv/_u1_prototipo.py`)*: **nel `spostamento_scalare` avvolto, alla PRIMA chiamata del tick e poi a ogni chiamata dispari** *(`conta % 2 == 1`)*: **`campo.deriva(0.5)` due volte** *(`A += w E`)* **e `scrivi_U(mot, campo)`: `U[a, 0, 0] = U[a, 1, 1] = exp(i e A_a)`** *(la diagonale; i fuori diagonale restano `0`)*. ### **All'uscita `avvolto` rimette SOLO `mot.operatori`; il docstring del prototipo dice «`mot.geo.U` rimesso a FINE CORSA»: la persistenza fra i tick e' di PROGETTO nel prototipo.**
- **CHI LO LEGGE:** **`flussi_parziali.hop_psi`** *(lo `spostamento_trasporto`: TUTTI i passi di trasporto della materia)*; **`energia.py` ed `energia_pesata.py`** *(l'energia: quindi anche i conti e `mattone.energia`)*. **`bordo.assorbi` no** *(non lo nomina)*.
- **QUANDO, DENTRO UN TICK DI `p6_bracci.tick_GU`:**
  1. **`campo.spinta(0.5)`; `fase_a`;**
  2. ### **`tick_lapse.cs_al_centro`: le COPIE del punto fisso girano `TK.percorri_tick` SENZA `avvolto`, con l'`U` LASCIATO DAL TICK PRIMA** *(`exp(i e A)` di allora, non `I`)*;
  3. **la reazione; il tick vero avvolto: i passi PRIMA del primo `spostamento_scalare` usano ANCHE LORO l'`U` del tick prima; poi `U` rifatto dal campo;**
  4. **la reazione, `fase_a`, `campo.spinta(0.5)`.**
  - **L'ordine dei passi** *(`composizione.ORDINE`, letto)*: **`14` posizioni; `CAMM-SPOSTAMENTO` alla `5` e alla `10`, `CAMM-SPOSTAMENTO-VUOTO` alla `7` e alla `8`:** ### **il PRIMO trasporto della materia di ogni tick usa l'`U` del tick prima, il SECONDO quello nuovo** *(la `7` riscrive, la `8` no: `conta` pari)*.
- ### **LA MIA LETTURA, PRIMA DELLE PROVE:** **la possibilita' (2) del guardiano, «le copie del punto fisso vedono l'`U` del campo», e' VERA PER COSTRUZIONE dal secondo tick in poi** *(lo dice il punto 2: niente rimette `I` prima di `cs_al_centro`)*. **Il contatore G3 lo deve mostrare: zero solo al primo tick dopo un caricamento.**
- ### ⚠ **UN PUNTO DEL BIVIO CHE SEGNALO AL GUARDIANO** *(non lo cambio: lo scrivo)*: **anche nel mondo SOLO U** *(`_u1_oggi.tick`: `avvolto` attorno al tick intero)* **i passi prima del primo `spostamento_scalare` leggono l'`U` del tick prima:** ### **la ripartenza di (MU) PERDE `U` ANCHE LEI, e io prevedo che FALLISCA per la stessa causa.** **Allora il ramo (c) «lo stato nascosto non e' (solo) `U`» sarebbe una conclusione sbagliata.** **Per distinguere:** ### **MIA SCELTA: G4 si fa ANCHE con `U` RICOSTRUITO dal campo salvato al caricamento** *(`scrivi_U(mot, campo)`: dopo l'ultimo `spostamento_scalare` dispari il tick non tocca piu' `A`, solo `E` con la spinta: l'`U` lasciato e' `exp(i e A_finale)`, ESATTO)*: **(MU) e (MGU).** **Se con `U` ricostruito passano, lo stato nascosto e' SOLO `U`.**
- **E (MG)?** **Nessun `avvolto`, `U` resta `I`; `cs_al_centro` riparte da `cs_di(stato)`:** **prevedo che la ripartenza di (MG) PASSI.**
- ### **COSA NON SO:** **quanto pesa** *(l'additivita' dice: poco)*; **se il primo segmento del tick vero col vecchio `U` sia voluto** *(un integratore a salti: `U` di `A` a meta' del tick prima)* **o un difetto: e' una domanda di fisica, per Luca.**

### 16.2 IL PROGETTO *(`csv/solitone/geometria_nascosta.py`, NUOVO; nessun file esistente cambia)*

- **`perdita`** *(G3)*: **da `MGU_05000` su `L 81`, G+U a campi pieni, `20` tick, quattro bracci dallo STESSO stato:**
  - **(oggi)** **`mattone.Campi.tick` cosi' com'e';**
  - **(oggi+contatore)** **lo stesso, con `tick_lapse.cs_al_centro` avvolto da un CONTATORE** *(chiamate e giri in cui `U != I`; il contatore NON cambia i conti)*;
  - **(R)** **dopo OGNI tick vero `U` rimesso al valore di prima del tick** *(il mandato; da un caricamento e' `I`)*;
  - **(C)** ### **MIA SCELTA, in piu': SOLO le copie del punto fisso con `U = I`** *(attorno a `cs_al_centro`; il tick vero com'e')*: **«il campo solo sul tick vero» del progetto `914c1248`.**
  - ### **DEVE** *(il mandato: «senza variante = il codice di oggi»)*: **(oggi+contatore) = (oggi) AL BIT su tutte le chiavi e il campo.** ### ⚠ **LA MIA LETTURA DEL DEVE, dichiarata:** **«gli stessi byte della corsa MGU originale fra `4000` e `4020`» NON si puo' fare cosi': gli stati sono ogni `1000` tick, e la ripartenza da `04000` inciampa proprio nel difetto in esame.** **Il senso del DEVE** *(lo strumento senza variante E' il codice di oggi)* **lo dice il confronto con `mattone.Campi.tick` stesso.**
  - **Il controllo che PUO' fallire:** **il contatore in (R) DEVE dare zero** *(se no il contatore non conta quello che dice)*.
  - **IL BIVIO del guardiano:** **(R) = (oggi) al bit E contatore zero: (a); se no: (b).** **(C) e' scritto accanto.**
- **`ripartenza --caso MG|MU|MGU [--ricostruisci]`** *(G4 e la mia aggiunta)*: **da `<caso>_04000` `1000` tick col tick di `mattone.Campi`, contro `<caso>_05000` chiave per chiave; con `--ricostruisci` `U` rifatto dal campo salvato al caricamento** *(solo MU, MGU)*.
- **`peso --variante oggi|C`** *(il ramo (b))*: **`200` tick di `GUrampa` dallo stato iniziale** *(la scena di C35-pi a `60000`, `U = I`, Gauss, la rampa del lapse `min(1, k/500)`, `p6_bracci.tick_GU`)*; **`d` e `rho max` a `50`, `100`, `150`, `200`.** ### **DEVE** *(il controllo positivo)*: **(oggi) = `GUrampa.npz`** *(`git show 8ca61a34`)* **AL BIT a quei tick.** ### **MIA SCELTA: «la variante corretta» e' (C)** *(il progetto: il campo solo sul tick vero)*; **(R) butta via il campo anche nel primo segmento del tick vero.**

### 16.3 COSA MI FAREBBE FERMARE

- **il DEVE della `perdita` o del `peso` che fallisce; il contatore di (R) diverso da zero; il ramo (b) o (c) del bivio** *(referto, FERMO)*.

### 16.4 TODO

1. questa carta, commit e push;
2. `geometria_nascosta.py`, l'inventario, la suite, commit;
3. il registro; `perdita` e `ripartenza` (MG, MU, MU ricostruita) insieme *(due col lapse al piu')*; poi MGU ricostruita;
4. il bivio: (a) la cottura col caricamento che ricostruisce `U`; (b) il `peso`, il referto, FERMO.
