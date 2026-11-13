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
