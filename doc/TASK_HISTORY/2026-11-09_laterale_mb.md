# 2026-11-09 -- IL RAMO LATERALE `zero-nel-nucleo`: (m-b), I CONTI COL NUCLEO NUOVO CONTRO IL VECCHIO, DALLO STESSO STATO

> **Il ramo laterale** *(Luca `2026-11-08` `21:47`-`21:49`; `doc/NUCLEO_CONGELATO.md` sul principale)*: **il nucleo CON v2.** **Questo task history e i
> referti di questo ramo sono SUOI** *(la regola `2`)*: **sul principale va una riga che rimanda al commit di qui.** [[PIANO-2D-3D]] [[VUOTO-SUL-FONDO]]

## 1. LE PREMESSE DAL CODICE

- ### **La decisione** *(Luca `21:49`, (m-b))*: **«i conti per nodo e `E + E_ass` di un pezzo con il nucleo nuovo contro il vecchio, dallo stesso stato. Lettura scritta prima: UGUALI entro l'arrotondamento A MENO DELLA COSTANTE `pi` per norma.»** **Serve a preparare la riunione.**
- **Che cosa so** *(dal principale, `de46816d` e il task history di v2)*: **la DINAMICA e' identica al bit** *(il braccio 0, `6` chiavi)*; **`e_K` si sposta di `+pi` esatto** *(`-4.7122750003546425` -> `-1.5706823467648499`)*.
- **Dal codice** *(`csv/solitone/c0_cucitura.py` del principale, il ciclo della corsa: `AC.tick`, poi `BO.assorbi` con `c(t) F3`; `E_ass += e_pr - e_dopo` coi `conti_per_nodo` prima e dopo l'assorbimento)*: **`LC.conti_per_nodo(inc, mot, st, e_K, LAM_ZERO, par)` prende `e_K`: quindi lo spostamento di `e_K` entra nei conti, e se l'energia e `e_K` si spostano INSIEME la costante puo' cancellarsi in qualche termine.** ### **NON SO in quale termine sta la costante, ne' se si cancella.**
- **Il ramo laterale e' a `7c181cc4`** *(prima del merge)*: **`csv/solitone/corsa_accensione.py` identico al principale** *(controllato col `diff`)*; **`c0_cucitura.py` qui non c'e': il ciclo si ricopia nello script nuovo.**

## 2. LA MISURA E LE LETTURE, PRIMA DEI NUMERI

- ### **Lo script `csv/solitone/mb_costante.py`** *(su questo ramo)*: **lo stato completo di `TBS` a `100000`** *(la libreria, `E:`)*, **`N = 200` tick del ciclo della corsa** *(gli accumulatori del bordo dal pezzo prima)*; **a `t0` e alla fine: i conti per nodo per TERMINE, la norma `M`, `E + E_ass`, `e_K`, gli sha dello stato** *(in un `npz` fuori dal repo)*. **`--confronta A B`: i due `npz`.**
- **Si gira DUE volte, lo stesso blob:** **qui** *(il nucleo nuovo)* **e nel worktree del principale `wt_zero_padre`** *(il nucleo vecchio; il file copiato e tolto dopo, dichiarato)*.
- ### **LE LETTURE** *(Luca, e mie per i dettagli, dichiarate)*:
  - **(L0) la dinamica: gli sha dello stato alla fine UGUALI** *(se no, FERMO: il braccio 0 sarebbe smentito)*.
  - **(L1) `e_K` nuovo - vecchio = `pi` alla macchina** *(`|diff - pi| <= 4 eps pi`)*.
  - **(L2) per ogni termine dei conti, `(nuovo - vecchio)` sommato sui nodi, diviso `M`: o `0` o `pi`** *(entro `64 eps` relativi al termine: mia)* **-- cioe' la costante sta in UN termine, ed e' `pi` per norma; lo stampo per termine.**
  - **(L3) `E + E_ass` nuovo - vecchio, a `t0` e alla fine: la STESSA costante** *(`pi M0` o `0`, entro `64 eps` relativi)*, **cioe' costante NEL TEMPO: e' la condizione perche' la riunione possa dichiarare lo spostamento e confrontare le corse vecchie.**
  - **Se L2 o L3 non tornano: FERMO, e lo scrivo** *(la riunione non si prepara senza capire dove sta la costante)*.
- ### **IL DEVE FALLIRE:** **lo stesso confronto con `N` diverso nei due bracci** *(`200` contro `199`)*: **L0 DEVE fallire** *(il confronto sa dire «diverso»)*.

## 3. L'ESITO DI (m-b): **`9/14` -- LA DINAMICA AL BIT, `e_K` `+pi` ESATTO; LA COSTANTE NON E' SOLO `pi M`: IL TERMINE DEL VUOTO SI SPOSTA ANCHE LUI; FERMO** *(`doc/referti_l2/mb_costante.txt`; il codice a `c4208037`; dall'orologio `00:40`-`00:42`)*

- **Girato:** **qui** *(il nucleo nuovo, `flussi_parziali` `d43b1cf8`, `energia_pesata` `43bce8ad`)* **e nel worktree del principale a `aaf7e95b`** *(il vecchio, `1461182f`, `cfaff204`)*, **lo stesso blob dello script** *(`e5a270ef`, copiato e tolto dopo)*. **Il primo giro e' morto per un file di dati mancante nei worktree** *(`db/accensione_lenta/fase_F3.npz`, ignorato da git: copiato, lo sha1 `4beb01d9` uguale)*.
- ### **(L0) la dinamica AL BIT** *(`6` chiavi)*; **(L0-F) contro `N 199` fallisce come deve** *(`4` chiavi diverse)*; **(L1) `e_K` nuovo - vecchio `3.1415926535897927`** *(scarto `-4.4e-16`)*.
- ### **(L2), per termine** *(`(nuovo - vecchio) / M`, `M = 995049.70`)*: **`cin` `0`** *(`9e-16`)*, **`leg` `0`**, **`cost` `pi` esatto**; ### **`vuo` `+0.112929` per `M`: NE' `0` NE' `pi`** *(`+2792.41` contro `-109577.51`)*; **quindi `tot` `+3.254522`** *(= `pi + 0.112929`)*. **Alla fine** *(`200` tick)*: **`vuo` `+0.112924`: la costante del vuoto CAMBIA nel tempo** *(di `-4.9` in assoluto)*, **mentre `cost` resta `pi` per la norma del momento.**
- ### **(L3) `E + E_ass`:** **la differenza a `t0` `+3238410.737093371`, alla fine `+3238410.737093734`: la STESSA costante entro `3.6e-07`** *(relativa `4.4e-14`)*; **`E_ass` nuovo - vecchio `+8.85`: lo spostamento di `tot` dovuto a cio' che il bordo assorbe** *(`pi dM = -3.94` e il cambio del vuoto `-4.91`)* **finisce in `E_ass`, e la somma si conserva.** ### ⚠ **La soglia di L3 (`64 eps` di `E`, `1.18e-07`) FALLISCE di un fattore `3`: e' un ERRORE MIO di progetto** *(una soglia da UNA somma, applicata a un accumulatore di `400` differenze di somme da `~8e6`)*. **Non la cambio dopo i numeri: lo scrivo.**
- ### **LA LETTURA** *(la mia, da verificare)*: **lo zero simmetrico sposta l'energia di `pi` per unita' di norma della MATERIA** *(il termine `cost`, via `e_K`)* **E di una costante anche nel termine del VUOTO** *(`vuo`)*: **l'ipotesi piu' semplice e' `pi` per unita' di norma del VUOTO** *(la `V = sum Lambda` dei conti)*, **che cala mentre il bordo assorbe vuoto** *(`V_ass`)*: **cosi' `E + E_ass` resta spostato di `pi (M_0 + V_0)`, costante.** ### **NON MISURATO: lo script non registra `V`.**
- ### **LA LETTURA DI LUCA** *(«uguali entro l'arrotondamento a meno della costante `pi` per norma»)*: **VALE per la materia** *(`cin`, `leg` a `0`; `cost` `pi M`)* **e per la conservazione** *(`E + E_ass` costante a `4e-14`)*; **NON vale per il vuoto, che porta una costante sua.** ### **Per la riunione cambia una cosa:** **la costante da dichiarare nei referti non e' `pi M` ma `pi M` + quella del vuoto** *(se l'ipotesi regge: `pi (M + V)`)*.
- ### **FERMO** *(la regola della sez. `2`)*. **LA DOMANDA A LUCA:** **(mb-a) una misura in piu', corta: lo stesso script con `V` registrato** *(la somma di `Lambda` nei conti)*, **e la lettura «`Delta vuo = pi V` al bit di `64 eps`»; con L3 a una soglia da accumulatore** *(`64 eps E sqrt(2 N)`, fissata PRIMA di rigirare)*; **(mb-b) basta cosi': la costante del vuoto si dichiara come misurata, `0.1129 M` a `TBS 100000`.** ### **La mia proposta: (mb-a)** *(due minuti di calcolo, e la riunione ha una formula invece di un numero)*.

## 4. LA DECISIONE DI LUCA DELLE `01:31`: (mb-a) -- LA STESSA MISURA COL VUOTO `V` REGISTRATO; LE LETTURE, PRIMA

- ### **La lettura di Luca, scritta prima:** **«la costante di `V` e' proporzionale alla norma della materia** *(circa `+0.1129` per norma)* **e si scrive come effetto dello zero simmetrico sulla ripartizione fra materia e vuoto; `E + E_ass` resta lo stesso spostamento costante** *(`4e-14`)*».
- ### **La misura:** **`mb_costante.py` con `V = sum Lambda` dei conti** *(il campo `"V"` di `conti_per_nodo`)* **registrato a `t0` e alla fine; il resto identico.**
- ### **LE LETTURE, fissate ora:**
  - **(R-M) la lettura di Luca: `Delta vuo / M` lo STESSO a `t0` e alla fine** *(entro `64 eps` relativi: con `M` che cambia, una costante proporzionale a `M` segue `M`)*. **Gia' dal referto `c2ad5f0d`: `0.1129290` contro `0.1129242`, `4e-5` relativi mentre `M` cambia di `1.3e-6`: mi aspetto che (R-M) NON passi.** *(Detto prima, onestamente: la lettura di Luca si prova e si scrive l'esito.)*
  - **(R-V) la mia ipotesi: `Delta vuo = pi V`** *(entro `64 eps` relativi a `vuo`)*, **a `t0` e alla fine.**
  - **(R-V') se (R-V) non passa: `Delta vuo / V` stampato a `t0` e alla fine** *(e' costante? allora e' una costante per norma del vuoto diversa da `pi`)*.
  - **(L3) `E + E_ass` la stessa costante a `t0` e alla fine, con la soglia DA ACCUMULATORE `64 eps E sqrt(2 N)`** *(fissata ora, prima di rigirare: la cura del mio errore della sez. `3`)*.
  - **L0, L0-F, L1, L2 per `cin`, `leg`, `cost` come nella sez. `2`.**

## 5. L'ESITO DI (mb-a): **LA COSTANTE E' `pi` PER UNITA' DI NORMA TOTALE, MATERIA PIU' VUOTO: `Delta E = pi (M + V)` ESATTO; (R-M) CADE, (R-V) PASSA** *(`doc/referti_l2/mb_costante_v.txt`; il codice a `8bc67f84`; dall'orologio `02:10`-`02:12`)*

- ### **(R-V) PASSA a `t0` e alla fine:** **`Delta vuo = +1.123699224816906e+05 = pi V`** *(`V = 35768.45723562832`)*, **`Delta vuo / V = 3.141592653589793`; alla fine `3.141592653589794`.** ### **(R-M), la lettura di Luca, FALLISCE** *(`Delta vuo / M`: `0.11292896` e `0.11292416`, scarto relativo `-4.2e-05`)*, **come detto prima nella sez. `4`: la costante del vuoto segue la norma del VUOTO, non quella della materia** *(il `+0.1129` era `pi V / M` a questo stato: `V / M = 0.0359`)*.
- ### **IL CONTO TOTALE** *(una riga di python sui due `json` della misura, `mbv_nuovo.json` e `mbv_vecchio.json`, dichiarata: `a['c0']['tot'] - b['c0']['tot'] - pi (M0 + V0)`)*: **`Delta tot` a `t0` = `pi (M0 + V0)` con scarto `0.000e+00`** *(`3238410.737093`)*; **`E_ass` nuovo - vecchio `8.850464` = `pi` per la norma assorbita** *(materia piu' vuoto, `8.850463`)*. ### **Quindi `E + E_ass` resta spostato di `pi (M0 + V0)`, COSTANTE NEL TEMPO** *(L3 con la soglia da accumulatore: `3.6e-07` contro `2.35e-06`, PASSA)*.
- ### **LA FORMULA PER LA RIUNIONE** *(da dichiarare nei referti col nucleo nuovo, per il confronto con le corse vecchie)*: **`E_nuovo = E_vecchio + pi (M + V)`** *(`M` la norma della materia, `V` quella del vuoto, sommate sui nodi)*; **per norma: `cost` porta `pi M`** *(via `e_K + pi`)*, **`vuo` porta `pi V`, `cin` e `leg` nulla.** **Per la conservazione: `E + E_ass` nuovo = vecchio + `pi (M_0 + V_0)`.**
- **I controlli vecchi della sez. `2`** *(L2 per `vuo` e `tot`, L3 a `64 eps`)* **restano nel referto e falliscono come prima: sono le letture di prima, e non si tolgono.** **ESITO `12/18`.**

## 6. LA PRIMA FUSIONE DEL PRINCIPALE NEL LATERALE, COL REVERT DEL REVERT *(Luca `2026-11-09` `01:31`, la procedura della regola `3`)*: **LE LETTURE, PRIMA**

- ### **La procedura:** **(1) `git merge origin/primo-ordine` sul laterale** *(lo stato X: porta il revert `de46816d`, quindi SENZA v2)*; **(2) `git revert de46816d`** *(lo stato Y: v2 torna)*.
- ### ⚠ **UN LIMITE DEL CONTROLLO DI LUCA, detto prima:** **il braccio 0 di v2** *(`zero_nel_nucleo.py`: il nucleo contro il VECCHIO COL SUO AVVOLGIMENTO, al bit)* **NON distingue «con v2» da «senza v2»: v2 e' stato fatto apposta perche' la dinamica sia la stessa al bit.** **Sullo stato X** *(il nucleo vecchio con l'avvolgimento vero)* **il braccio 0 PASSA anche lui** *(e' il padre contro se stesso)*. **Quindi il DEVE FALLIRE non puo' essere il braccio 0.**
- ### **I CONTROLLI, quindi:**
  - **(F-0) il braccio 0 di v2 su Y: `4/4` al bit** *(il DEVE di Luca: v2 c'e' e la dinamica e' quella)*; **lo stampo anche su X** *(passa: e' il limite, scritto)*.
  - **(F-B) i blob dei file di v2** *(i `.py` sotto `primo_ordine/` e `csv/` che v2 ha cambiato, `git diff --name-only 995bafc4 7c181cc4`)* **= quelli di `7c181cc4`:** **su Y DEVE PASSARE; su X DEVE FALLIRE** *(il DEVE FALLIRE di Luca: senza il revert del revert il laterale NON ha v2)*.
  - **(F-K) `e_K` della scena di `C35-pi`** *(lo script di diagnosi di `de46816d`)*: **su Y `-1.5706823467648499`, su X `-4.7122750003546425`** *(il segno di v2 che il braccio 0 non vede)*.
  - **La suite sul laterale in Y.**
- ### **COSA MI FAREBBE FERMARE:** **un conflitto nel nucleo** *(i file di v2 toccati dal principale dopo `7c181cc4`: il nucleo del principale e' congelato, quindi non me lo aspetto)*; **F-B su Y che fallisce.**

## 7. L'ESITO DELLA FUSIONE COL REVERT DEL REVERT: **TUTTO COME DEVE -- X SENZA v2, Y CON v2, IL BRACCIO 0 `4/4` AL BIT SU Y** *(dall'orologio `02:50`-`03:27`)*

- ### **X** *(`ebe2f13c`, la sola fusione del principale `0bebbe94`)*: **F-B `0` file su `17` uguali a `16d2ebdb`, F-K `e_K` `-4.7122750003546425`: SENZA v2** *(i due DEVE FALLIRE di Luca falliscono come devono; `doc/referti_l2/fusione_v2_X.txt`, il codice a `61c173fb`)*.
- ### **Y** *(`8cfda2f1`, `git revert de46816d`)*: **F-B `17` su `17`, F-K `-1.5706823467648499`: CON v2** *(`doc/referti_l2/fusione_v2_Y.txt`)*; ### **il braccio 0 di v2: `4/4` AL BIT** *(`Z0-D` e `Z0-R` `6` chiavi uguali al padre, il nucleo vecchio col suo avvolgimento a `0bebbe94`; `Z0-F-D` e `Z0-F-R`, lo zero due volte, `4` chiavi diverse; `doc/referti_l2/zero_nel_nucleo_Y.txt`)*; **la suite su Y `67` su `67`** *(il pre-commit `521.8` s)*.
- ### **Due difetti miei, trovati e curati prima di Y:** **(1) l'elenco dei file di v2 della sez. `6`** *(da `995bafc4..7c181cc4`: prendeva i file del principale)* **sostituito da quello del revert; (2) `fusione_v2.py` trattava un file cancellato da v2 come «diverso»** *(`61c173fb`)*.
- ### **Il laterale ora ha la libreria di oggi del principale E v2: D0-D4 si possono fare qui.**

## 8. D0-D4, IL PUNTO FISSO DI `cs` COL SOLITONE, SUL LATERALE *(il progetto: `doc/TASK_HISTORY/2026-11-07_punto_fisso_cs_solitone.md`, sez. `1`-`3`, le letture `pf0`-`pf5` e i DEVE `PF-V`, `PF-E`, `PF-U`, `PF-F` LI'; Luca `2026-11-09` `01:31`: «poi D0-D4» sul laterale)* -- **I CAMBI RISPETTO AL PROGETTO, DICHIARATI PRIMA**

- ### **Il nucleo e' quello del laterale** *(con v2: lo zero simmetrico nel nucleo; il progetto del `2026-11-07` parlava di `BE.conv(DC.ZERO)`, che qui e' un contesto nullo: la dinamica e' la stessa al bit, il braccio 0)*.
- ### **La mappa** *(la riga di `tick.cs_al_centro`, ricopiata e NON modificata)*: **`F(x) = FP.cs(densita_vuoto(stato al centro avanzato con mot.cs = x), Lambda_c)`, mezzo palindromo con `percorri_tick` su una COPIA.** **D0 gira anche `tick.cs_al_centro` stesso** *(il controllo che la copia e' la mappa del nucleo: lo stesso numero di giri, o lo stesso «alza»)*.
- ### **`Lambda_c` DERIVATO nello script, non scritto:** **`Lambda_c = Lambda_vuoto (1 - s) / s`** *(la decisione (P): la continuita' col vuoto `F3`, `Lambda_vuoto` la media per nodo, `s = 0.15`)*, **atteso `34`.**
- ### ⚠ **CAMBIO 1, le scene:** **`TB3` non ha stati salvati, e lo stato a `t 0` ricostruito non ha uno sha registrato con cui confrontarlo** *(il primo jsonl ha solo `sha_vuoto`)*: **al posto del «tick `0` di `TB3`» uso lo STATO A `t 0` DI `TBS`** *(`E:\...\TBS_stato_000000.npz`, lo sha nel jsonl)*. **Le scene: `TBS` a `0`, `10000` (`t 1500`), `100000` (`t 15000`), `200000` (`t 30000`) tick**, **ogni stato contro il suo sha registrato.**
- ### ⚠ **CAMBIO 2, D4 su UNA scena:** **la continuazione in `Lambda_c = 34 x 2^k`, `k = 10 .. 0`, su `TBS` a `10000` tick** *(lo stato piu' vicino a dove `cs` si accenderebbe in `TCS`: la strada (r1))*; **le altre tre scene solo a `34`.**
- ### **D3: (i) Anderson** *(`scipy.optimize.anderson` su `G = F(x) - x`)*, **(ii) Newton-Krylov** *(`scipy.optimize.newton_krylov`)*, **`f_tol = 8 eps max|x|`** *(il criterio del nucleo)*; **il numero di valutazioni di `F` contato** *(il costo per tick: un `F` e' mezzo tick)*.
- ### **D2:** **`h = sqrt(eps) max|cs|`; (a) l'iterazione di potenza, `30` prodotti, il modulo e il segno** *(dal rapporto `<v, J v> / <v, v>`)*; **(b) la contrazione locale su dischi di raggio `2` nodi a `4` centri** *(il centro del solitone; `r = w`, `2 w`; il vuoto lontano)*.
- ### **D1:** **gli anelli dal centro del solitone** *(`r < w`, `w`-`2 w`, `2 w`-`4 w`, oltre)*, **`w` la larghezza della `rho`: la frazione di `|cs_{n+1} - cs_n|^2` per anello, e `Lambda`, `cs`, `rho` medi.**
- ### **Le letture e i DEVE sono quelli del progetto** *(`pf0`-`pf5`; `PF-V`, `PF-E`, `PF-U`, `PF-F`)*. **Il referto `doc/referti_l2/punto_fisso_cs.txt` sul laterale.** **FERMO sul rimedio** *(il progetto)*.

## 9. D0-D4, IL PRIMO GIRO: **INTERROTTO DA UN DIFETTO MIO ALLA SECONDA SCENA; LA PRIMA SCENA DICE GIA' MOLTO** *(`doc/referti_l2/punto_fisso_cs_interrotto.txt`; il codice a `ae1a2585`; `04:32`-`04:36`)*

- ### **`Lambda_c = 34.000000000000`** *(derivato)*; **PF-V passa coi tre metodi** *(`cs = 0.15` ovunque, `5.6e-17`)*.
- ### **`TBS` a `t 0`:** **D0: l'iterazione semplice NON converge in `120` giri** *(gli scarti fermi a `~3.6e-2`, senza calare)*; **`tick.cs_al_centro` ALZA allo stesso modo** *(D0-N passa: la copia e' la mappa del nucleo)*. **D1: lo scarto e' tutto entro `2 w`** *(`r < w` `30%`, `w`-`2 w` `70%`, oltre `0`)*. ### **D2: l'autovalore dominante `~ -15.2`** *(`|J v| / |v| = 15.22`, `<v, J v> / <v, v> = -15.22`)*: **NON una contrazione, e NEGATIVO** *(l'iterazione oscilla)*; **i dischi: il centro `1.56`, `r = w` `1.41`, `2 w` `0.096`, il vuoto `0.004`: la non-contrazione sta nel CUORE.**
- ### **D3: Anderson e' morto al secondo passo** *(il punto medio di `Omega` -- l'altro punto fisso, dentro il tick -- NON converge al `cs` di prova di Anderson: scarto `8.7e3`)* **e Newton-Krylov subito dopo, ma per il MIO difetto:** ### **un'eccezione dentro `percorri_tick` lascia il tick del motore APERTO** *(`mot.cresciute_nel_tick`)*, **e la valutazione dopo alza «un tick e' gia' aperto»: il NK di questa scena NON e' una misura, e la seconda scena e' morta li'.**
- ### **LA CURA** *(il commit dopo, a se')*: **in `Mappa.__call__`, se `percorri_tick` alza, il tick si richiude** *(`cresciute_nel_tick = -1`, senza contare un tick)* **e l'eccezione risale.** **Nessuna lettura cambia.**

## 10. L'ESITO DI D0-D4: **`8/8` -- A `Lambda_c = 34` NESSUN METODO TROVA IL PUNTO FISSO, SU NESSUNA DELLE QUATTRO SCENE; LA CONTINUAZIONE LO RITROVA SOLO SOPRA `Lambda_c` FRA `136` E `272`, DOVE `cs` NEL VUOTO E' GIA' `0.042`-`0.022` INVECE DI `s = 0.15`; FERMO SUL RIMEDIO** *(`doc/referti_l2/punto_fisso_cs.txt`; il codice a `3faa4858`, blob `9ea68434`; finito alle `06:03`, `4712` s)*

- **I DEVE:** **PF-V `3/3`** *(il vuoto F3 da solo: `cs = s` coi tre metodi, `5.6e-17`)*; **D0-N `4/4`** *(la copia della mappa = il nucleo: tutti e due non convergono, su ogni scena)*; **PF-F fallisce come deve** *(la scena del `27/10`: il nucleo alza, scarto `1.698e-01`)*.
- ### ⚠ **PF-E e PF-U NON HANNO AVUTO MATERIA a `34`:** **D3 non ha trovato nessun punto fisso, quindi non c'era niente da controllare** *(nessun verdetto stampato: lo dico, perche' `8/8` non li contiene)*. **Nella continuazione, dove converge, la distanza NK-semplice e' `1e-19`-`2e-17`** *(stampata, senza verdetto: il progetto la voleva solo a `34`)*.

| scena | D0, l'ultimo scarto dopo `120` giri | D2, `|Jv|/|v|` e `<v,Jv>/<v,v>` | D2, i dischi: centro, `w`, `2w`, vuoto | D3 Anderson | D3 Newton-Krylov |
|---|---|---|---|---|---|
| `TBS` `0` | `3.58e-02` | `15.22`, `-15.22` | `1.56`, `1.41`, `0.096`, `0.004` | il punto medio di `Omega` alza (`8.7e3`) | non converge (`8601` valutazioni) |
| `TBS` `10000` | `7.56e-02` | `13.50`, `+13.50` | `1.57`, `0.93`, `0.043`, `0.004` | `Omega` alza (`9.3e2`) | non converge (`8668`) |
| `TBS` `100000` | `5.93e-02` | `12.71`, `+12.71` | `1.75`, `0.97`, `0.014`, `0.004` | `Omega` alza (`1.2e7`) | arriva a un `s` NEGATIVO (`-0.0079`) e alza (`5817`) |
| `TBS` `200000` | `7.64e-02` | `11.46`, `+11.43` | `2.21`, `0.79`, `0.018`, `0.004` | `Omega` alza (`2.8e4`) | `s` negativo (`-0.051`) e alza (`2192`) |

- **D1, dove sta lo scarto:** **tutto entro `2 w`, e sempre `0` oltre**; **fra `w` e `2 w` la quota e' `0.70`, `0.71`, `0.41`, `0.22`** *(con `Lambda` medio dell'anello `6.0`, `4.63`, `3.01`, `2.61`: l'anello dove `Lambda` scende sotto il vuoto)*, **dentro `w` `0.30`, `0.29`, `0.59`, `0.78`.** **Col tempo lo scarto migra dall'anello al centro.**
- ### **D4 sulla scena a `10000`** *(`Lambda_c = 34 x 2^k`)*: **la semplice converge per `k >= 3`** *(`4`, `5`, `5`, `6`, `7`, `10`, `14`, `41` giri, da `k = 10` a `k = 3`)*, **e NK ridà lo stesso punto** *(entro `2e-17`)*; **a `k = 2` (`136`) non convergono ne' l'una ne' l'altro** *(`|Jv|/|v| = 1.31`)*. **`|Jv|/|v|` cresce con continuita':** `0.0001` ... `0.0999` (`544`), `0.478` (`272`), `1.31` (`136`), `4.86` (`68`), `13.41` (`34`). **Il segno cambia due volte** *(`+` fino a `544`, `-` a `272`, `136`, `68`, `+` a `34`)*.
- ### ⚠ **LA TRAPPOLA DI D4, scritta perche' cambia la lettura:** **alzare `Lambda_c` abbassa `cs` OVUNQUE, vuoto compreso** *(`cs` del vuoto `0.000172` a `k = 10`, `0.0216` a `272`, `0.0423` a `136`, `0.150` a `34`)*. **Quindi D4 NON separa «il cuore troppo forte» da «`cs` troppo forte dappertutto»:** ### **dice solo che la mappa contrae quando `cs` e' piccolo DAPPERTUTTO.** **E `Lambda_c = 34` non e' una scelta:** **e' quello che da' `cs = s` nel vuoto** *(la decisione (P))*. **Un `Lambda_c` piu' grande romperebbe `cs_vuoto = s`: NON E' UN RIMEDIO** *(`A1`)*, **e' solo una misura del margine.**

### **LE LETTURE** *(quelle del progetto, sez. `1`-`3` del task history del `2026-11-07`)*

- **(pf0) CADE:** **a `34` l'iterazione semplice non converge su nessuna delle quattro scene.**
- **(pf1) NON E' DIMOSTRATA:** **(pf1) chiede un punto fisso che ESISTE**, e **nessuno dei due metodi robusti lo trova.** ### **Anderson non e' mai arrivato al terzo passo:** **muore DENTRO `F`, nel punto medio di `Omega`** *(il punto fisso interno del tick)*, **su tutte e quattro le scene.** **NK fa migliaia di valutazioni senza convergere e, alle due scene tarde, porta un tempo proprio sotto zero.**
- **(pf2) E' COMPATIBILE con D4, ma non dimostrata:** **la convergenza torna solo sopra una soglia fra `136` e `272`**, **e per la trappola qui sopra quella soglia NON e' «il cuore che sta nel dominio»: e' «tutto il `cs` abbassato di `4`-`7` volte».**
- **(pf3)** **nessun indizio** *(nessun metodo ha trovato due punti)*. **(pf4)** **non si puo' escludere:** **a `34` non abbiamo trovato nessun punto fisso.**
- ### **(pf5), LA MIA, DAI NUMERI:** **`F` NON E' DEFINITA DAPPERTUTTO.** **Il tick ha DUE punti fissi annidati** *(`cs` fuori, il punto medio di `Omega` dentro)*, **e appena `cs` esce di poco dalla traiettoria del nucleo il punto interno non converge** *(gli scarti di `Omega` `9e2`-`1.2e7`)*, **oppure `s` va sotto zero.** ### **Allora «il punto fisso di `cs` esiste?» non e' ancora una domanda ben posta: prima va detto su che insieme `F` e' definita.**
- **Il controllo che mi doveva FERMARE c'e' stato:** **«l'inner di `Omega` che non converge (e' un altro punto fisso: lo riporto)»** *(sez. `1`)*: **lo riporto qui, su tutte le scene.**

### **IL COSTO PER TICK** *(dal referto)*

- **una valutazione di `F` = mezzo tick = `0.143`-`0.163` s** su `TBS`.
- **dove converge** *(D4, `k >= 3`)*: **la semplice `4`-`41` valutazioni** *(`41` a `272`)*, **NK `32`-`104`.**
- **a `34`: nessun metodo provato converge in `120` giri** *(la semplice)* **o in `2192`-`8668` valutazioni** *(NK)*. **Un rimedio di METODO oggi non ha un costo: non ha un metodo.**

### **FERMO SUL RIMEDIO: LA PROPOSTA E LE ALTERNATIVE** *(la scelta e' di Luca)*

1. ### **LA MIA RACCOMANDAZIONE: (r-D5), UN'ALTRA DIAGNOSI PRIMA DI UN RIMEDIO, senza toccare il nucleo.** **Rendere `F` definita** *(il punto medio di `Omega` risolto con un metodo robusto ANCHE lui, dentro la mappa di prova, oppure `F` ristretta a `s > 0`)* **e rifare D3 a `34`.** **Perche':** **(pf1), (pf2) e (pf4) si distinguono solo su una `F` definita**, e oggi D3 muore prima di poter rispondere. **Il costo:** **la diagnosi su una scena `~30`-`40` min** *(come una scena di oggi)*; **tocca solo `carta_punto_fisso.py`, sul laterale.**
2. **(pf2) DI FORMA, SUBITO:** **il minimo per `Lambda` della voce `35`** *(la (e) di Luca)*: **e' un NUMERO e un PAVIMENTO** *(`A1`, `A11`)*, ### **ammissibile solo DERIVATO** *(dal quanto di olonomia, la (g), che oggi non c'e')*. **D4 non da' un numero da usare:** **la sua soglia abbassa `cs` anche nel vuoto.**
3. **(pf4), LA LEGGE IMPLICITA RIPENSATA:** **`cs` esplicito** *(dal `Lambda` del tick precedente, non dello stesso)*: **niente punto fisso, niente costo**; **cambia la legge** *(una decisione di fisica)*, **e la simmetria del palindromo va riverificata.**
4. **(pf1) DI METODO A PRESCINDERE** *(NK con la ricerca sul tratto e `s > 0` imposto)*: **lo sconsiglio adesso:** ### **imporre `s > 0` dentro un risolutore e' un pavimento che protegge da un errore** *(`A11`)*, **e oggi non sappiamo se il punto fisso esiste.**

- **Che cosa blocca:** **[[PUNTO-FISSO-CS-SOLITONE]] blocca ancora `TCS`, la coppia con `cs` e la mitosi «dove gli orologi differiscono».** **Non blocca niente del principale** *(`cs` e' spento in tutte le corse)*.

## 11. LE DECISIONI DI LUCA DEL `2026-11-09` `08:56` SU D0-D4: **IL FATTO, (r-D5) SI', E UN'IDEA PER DOPO**

- ### **IL FATTO, registrato:** **a `Lambda_c 34` il punto fisso di `cs` col solitone NON si trova con nessun metodo su nessuna scena** *(`|Jv|/|v|` `11.5`-`15.2`; l'autovalore dominante negativo a `t 0`: un'oscillazione divergente, localizzata nel cuore)*. **Converge solo a `Lambda_c` `136`-`272`, abbassando `cs` anche nel vuoto: con `s` fisica cambierebbe la fisica dappertutto.** ### **Nessun rimedio si applica prima di (r-D5).**
- ### **(r-D5) SI', qui, senza toccare il nucleo:** **`F` resa definita** *(il punto medio di `Omega` risolto con un metodo robusto dentro la mappa di prova, oppure `F` ristretta a `s > 0`, dichiarato quale)*, **e D3 rifatto a `Lambda_c 34`, per distinguere (pf1), (pf2), (pf4).** **Le letture scritte prima** *(la sezione dopo, prima del codice)*.
- ### **PER DOPO, SOLO COME IDEA** *(Luca; nessun lavoro ora)*: **se il punto fisso non esiste, `cs` come MEMORIA** *(`A15`: dinamica, locale, col tempo di memoria ricavato dalla dinamica locale)* **che RILASSA verso `cs(Lambda)` invece di essere risolto a ogni tick.** **Da valutare dopo (r-D5), con le sue conseguenze sul palindromo e sulla reversibilita'** *(una legge con memoria non e' piu' un punto fisso del tick: il palindromo va ripensato, e il rovescio del tempo deve portare la memoria con se')*.

## 12. (r-D5): **`F` RESA DEFINITA, D3 RIFATTO A `34` -- LE PREMESSE, IL PROGETTO, LE LETTURE, PRIMA DEL CODICE** *(Luca `2026-11-09` `08:56`)*

- ### **LE PREMESSE DAL CODICE** *(LETTE)*:
  - **`F` e' `Mappa.__call__` di `carta_punto_fisso.py`:** **una copia dello stato, `mot.cs = x`, `TK.percorri_tick` col mezzo palindromo, poi `FP.cs` della densita' del vuoto.**
  - **Dentro il tick, `CAMM-FASE-VUOTO` e' `motore._fase_vuoto`, che chiama `energia_pesata.applica`** *(per nome del modulo: `import energia_pesata as EP; EP.applica(...)`)*.
  - **`applica` risolve il punto medio di `Omega` con l'iterazione semplice:** **`GIRI_MAX_OMEGA = 200` giri, il criterio `entro_tolleranza`** *(`EPS_OMEGA` per il massimo del tetto)*, **i controlli del tetto all'inizio e alla fine; se non converge ALZA.**
  - **E' questo che uccide Anderson su tutte le scene** *(gli scarti `9e2`-`1.2e7`)*.
  - **L'altra causa: `flussi_parziali` alza con un `s <= 0`** *(«un tempo proprio nullo o negativo»)* *(NK alle scene a `100000` e `200000`)*.
  - **D4 ha gia' fatto una continuazione** *(NK partito dal punto del `k` prima)*, **ma a passi di un fattore `2`: perso fra `272` e `136`.**
- ### **LA SCELTA DICHIARATA** *(Luca: «dichiarato quale»)*: **il punto medio di `Omega` risolto con un metodo ROBUSTO dentro la mappa di prova.**
  - **Prima l'iterazione semplice del nucleo, IDENTICA** *(le stesse righe: dove converge, `F` e' quella del nucleo AL BIT)*.
  - **Se non converge in `GIRI_MAX_OMEGA`, Newton-Krylov su `omega(fase a meta' con w) - w`**, partendo dall'`Omega` di partenza, con lo stesso criterio *(`EPS_OMEGA` per la scala)* **e gli stessi controlli del tetto.**
  - **Se anche quello non converge, `F` NON E' DEFINITA in quel `x`:** **si alza un'eccezione SUA** *(«il punto medio di `Omega` non esiste qui»)*, **contata.**
  - ### **`s > 0` NON si impone:** **un `x` che porta un `s <= 0` resta fuori dal dominio, contato, e il metodo esterno muore li'.** **Imporlo sarebbe il pavimento di `A11`** *(la sez. `10`)*.
  - **Il nucleo non si tocca:** **`EP.applica` sostituita SOLO dentro la mappa di prova** *(un `with`, rimessa all'uscita)*.
- ### **LA MISURA:**
  - **D3-R:** **Anderson e NK esterni, con `F` definita**, **a `Lambda_c 34`, sulle quattro scene di `TBS`** *(`0`, `10000`, `100000`, `200000` tick; `maxiter 200` come D3)*.
  - **D4-R, la continuazione FINE sulla scena a `10000`:** **NK da `Lambda_c 272`** *(dove D4 converge)* **giu' fino a `34` a passi di `2^{-1/4}`** *(`12` passi)*, **ogni passo partito dal punto del passo prima.**
  - **Per ogni passo:** **converge? `|Jv|/|v|` col metodo della potenza** *(D2)*, **e il minimo di `s`.**
  - **Il costo:** **le valutazioni di `F`, quante col NK interno, il tempo.**
- ### **I DEVE, fissati ora:**
  - **(R-B) DEVE:** **`F` con l'`Omega` robusto = `F` del nucleo, AL BIT, dove il nucleo converge** *(sul vuoto F3 e sul punto di D4 a `272`)*;
  - **(R-V) DEVE:** **PF-V coi tre metodi, con `F` definita**;
  - **(PF-E) DEVE, per ogni punto trovato:** **`|F(x) - x| <= 8 eps |x|_inf`**;
  - **(R-E-F) DEVE FALLIRE:** **PF-E applicato al punto di PARTENZA `x0` a `34`** *(che non e' un punto fisso: il controllo che PF-E sa dire di no)*;
  - **(PF-F) DEVE FALLIRE, come prima:** **la scena del `27/10`.**
- ### **LE LETTURE, scritte prima:**
  - **(d1) D3-R converge a `34`** *(PF-E passa)*, **o D4-R arriva a `34`:** ### **il punto fisso ESISTE, la mappa non contrae: (pf1), si cura col METODO.** **Il costo per tick del metodo dal referto**, e **se i due metodi danno lo stesso punto, PF-U.**
  - **(d2) D4-R perde il ramo a un `Lambda_c*` fra `34` e `272`, con `|Jv|/|v|` o il passo di Newton che esplode li'** *(un punto di svolta)*, **e D3-R non converge:** ### **il punto fisso esiste solo sopra `Lambda_c*`: (pf2)**, **col numero `Lambda_c*`.**
  - **(d3) D4-R e D3-R muoiono per «`Omega` non esiste qui» o per `s <= 0`, PRIMA di un punto di svolta:** ### **(pf5) confermata: la legge interna cede prima di quella esterna**, **e il punto fisso di `cs` non e' una domanda ben posta finche' `Omega` non lo e'.**
  - **(d4) tutti i metodi girano dentro il dominio senza convergere e senza un punto di svolta:** **(pf4) resta possibile.**
  - **(d5) altro.**
- **COSA MI FAREBBE FERMARE:** **R-B o R-V che falliscono** *(la mappa di prova non e' piu' quella del nucleo)*.
- ### **Il costo previsto:** **`~1`-`2` ore** *(D3 erano `~22` minuti per scena a `0.15` s per valutazione; il NK interno costa di piu' dove serve)*. **La prova corta della regola `4`, mentre gira `C35-pi`.**
- **Lo script:** **`csv/solitone/carta_punto_fisso_r.py`** *(nuovo; importa `carta_punto_fisso.py`, che non si tocca)*; **il referto `doc/referti_l2/punto_fisso_cs_r.txt`.**

## 13. L'INTEGRAZIONE DI LUCA DELLE `09:59` A (r-D5): **LA ZONA SENSIBILE E' UN GUSCIO SUL BORDO DEL SOLITONE, NON IL CENTRO** -- R1-R4, LE LETTURE PRIMA DEL CODICE

- ### **IL FATTO NUOVO** *(dal guardiano, DA VERIFICARE)*:
  - **la mappa di `cs(Lambda)/s = Lambda / (Lambda + 34) / s`, calcolata dalle mappe leggere di `TB3`** *(`doc/referti_l2/campo_TB3/mappe_leggere.npz`, `Lambda = 6 + dLambda`)*: **l'orologio senza la sua reazione, non una corsa con `cs` acceso.**
  - **Al centro `cs/s` e' `~1`, fino a `~2`.** **Il rallentamento e' un GUSCIO sul bordo dell'esagono, a `~17`-`20` nodi dal centro** *(`cs/s` minimo `0.063` a `t 3000`, `0.030` a `t 30000`)*. **Oltre il guscio `cs/s` torna a `1`.**
  - **Gli errori n.`123` e n.`124` del guardiano** *(l'autovalore negativo solo a `t 0`; il «cuore»)*.
  - ### **E UN ERRORE MIO, nella sez. `10` e nel rimando del principale:** **«localizzata nel CUORE» viene dai dischi di D2** *(il centro `1.56`-`2.21`)*, **ma D1 diceva gia' che lo scarto sta per il `70%` fra `w` e `2 w`.** **Ho letto i dischi e non D1.**
- ### **R1, CHE COSA SONO I DISCHI DI D2** *(dal codice, `carta_punto_fisso.main` e `dischi`)*:
  - **il centro e' quello periodico della densita' di materia `rho`** *(`toro.centro`)*, **e `r` la distanza di ogni nodo da li'** *(`toro.scarti`, l'immagine piu' vicina, in unita' del lato)*;
  - **`w = sqrt(somma rho r^2 / somma rho)`** *(`6.65`, `8.25`, `9.29`, `9.64` alle quattro scene)*;
  - **i quattro centri dei dischi sono il nodo piu' vicino a `r = 0`, a `r = w`, a `r = 2 w`, e il nodo piu' lontano** *(«il vuoto»)*;
  - **ogni disco ha raggio `R_DISCO = 2` intorno al suo nodo** *(`17`-`19` nodi)*, **e la perturbazione e' uniforme sul disco.**
  - ### **Quindi nessun disco stava sul guscio di Luca** *(`17`-`20` nodi)*: **`2 w` e' `13`-`19`, e un disco di raggio `2` attorno a UN nodo non e' un anello.**
  - **Il profilo radiale di `Lambda` e di `cs/s` lo stampa il codice a ogni scena:** **anelli di `1` nodo, la media per anello**, **e il raggio del minimo di `Lambda`, `r_min`.**
- ### **R2, LA FORMA DELLA DIREZIONE INSTABILE:**
  - **l'autovettore dominante di D2** *(la stessa potenza: `30` prodotti, lo stesso seme, dallo stesso `x` di D2)*;
  - **il suo profilo radiale: la media di `v^2` per nodo, per anello**;
  - **e la quota di `|v|^2` nel guscio `[r_min - 2, r_min + 2]`, dentro (`r < r_min - 2`) e fuori.**
  - ### **LE LETTURE** *(di Luca, scritte prima; il criterio e' mio, dichiarato)*:
    - **(g1) il massimo del profilo di `v^2` per nodo cade nel guscio `[r_min - 2, r_min + 2]`:** **la non-contrazione nasce dove `cs` e' minimo e varia piu' in fretta**;
    - **(g2) il massimo cade dentro, `r < r_min - 2`:** **la mappa del guardiano non spiega l'instabilita': lo scrivo**;
    - **(g-a) altrove** *(fuori dal guscio)*: **lo scrivo coi numeri.**
- ### **R3:** **il fattore `|J v|_anello / |v|`, con `v` uniforme sull'ANELLO `[r_min - 2, r_min + 2]`**, **accanto ai dischi di oggi.**
- ### **R4** *(solo se (g1))*: **le cure candidate** *(la memoria `A15`, una legge di `cs` meno sensibile a `Lambda` piccolo, `cs` dal tick precedente)* **si valutano sapendo che la zona critica e' un guscio sottile dove `Lambda` scende fino a `~0.1`-`0.2` e `cs/s` fino a `~0.03`.** **Nel referto, R4 e' una stampa** *(`Lambda` e `cs/s` minimi sul guscio, a ogni scena)*, **non una cura.**
- **Il resto di (r-D5) non cambia** *(la sez. `12`)*. **R1-R3 entrano in `carta_punto_fisso_r.py` PRIMA del suo commit** *(non era ancora committato)*, **e si fanno su ognuna delle quattro scene, prima di D3-R.**

## 14. L'ESITO DI (r-D5): **`7/7` -- IL GUSCIO C'E' (R1), MA LA DIREZIONE INSTABILE STA AL CENTRO (R2: (g2) SU TUTTE LE SCENE MATURE); IL GUSCIO CONTRAE (R3); LA LEGGE INTERNA E IL DOMINIO `s > 0` CEDONO PRIMA DEL PUNTO FISSO: (d3); FERMO SUL RIMEDIO** *(`doc/referti_l2/punto_fisso_cs_r.txt`; il codice a `1fcc9e9b`, blob `f13be46a`; `13:09`-`14:25`, `4622` s)*

- **I DEVE:** **R-V `3/3`**, **R-B `2/2`** *(al bit sul vuoto e a `Lambda_c 272`)*, **R-E-F fallisce come deve** *(`2.578e-02` sul punto di partenza)*, **PF-F fallisce come deve.**
- ### **R1, IL GUSCIO, CONFERMATO** *(il fatto del guardiano)*:

| scena | `w` | `r_min` di `Lambda` | sul guscio `[r_min - 2, r_min + 2]`: `Lambda` min, `cs/s` min | al centro (`r < 1`): `Lambda`, `cs/s` |
|---|---|---|---|---|
| `TBS` `0` | `6.65` | *(nessun guscio: `Lambda = 6` ovunque)* | `6.0`, `1.00` | `6.0`, `1.00` |
| `TBS` `10000` | `8.25` | `16` | `0.444`, `0.086` | `6.60`, `1.08` |
| `TBS` `100000` | `9.29` | `18` | `0.147`, `0.029` | `8.51`, `1.33` |
| `TBS` `200000` | `9.64` | `18` | `0.121`, `0.024` | `9.53`, `1.46` |

  - **A `t 0` il vuoto non e' ancora disturbato: `r_min = 0` e la lettura R2 (g-a) e' degenere** *(un difetto della mia definizione di `r_min` su un profilo costante: la scena a `0` non ha un guscio)*.
- ### **R2, DOVE STA LA DIREZIONE INSTABILE: AL CENTRO** *((g2) a `10000`, `100000`, `200000`)*:
  - **il massimo del profilo di `v^2` a `r` `2`, `0`, `0`**;
  - **la quota di `|v|^2` dentro (`r < r_min - 2`) `1.000`, sul guscio `0.000`**;
  - **il profilo cade di `10` ordini fra `r 0` e `r 10`.**
  - ### **La lettura di Luca (g2): «la mappa del guardiano non spiega l'instabilita'».** **Il rallentamento sta sul guscio, ma la non-contrazione nasce al CENTRO**, **dove `cs/s` e' `1.1`-`1.5`** *(il tempo un po' piu' veloce)* **e `Lambda` e' il piu' alto** *(`6.6`-`9.5`)*.
- ### **R3: il guscio CONTRAE FORTE:** **`|Jv|_anello / |v|` `0.058`, `0.026`, `0.030`** *(contro `11.5`-`13.5` della direzione dominante)*.
- ### **D4-R, LA CONTINUAZIONE FINE A `10000`:**
  - **NK segue il ramo a `228.7` e `192.3`** *(`|Jv|/|v|` `0.554`, `0.641`, negativi; `cs` min `0.0019`-`0.0023`)*;
  - **a `161.7` muore per un `s <= 0`**, **con `|Jv|/|v| = 0.92` al passo prima: SOTTO `1`.**
  - ### **Il ramo esce dal DOMINIO prima di un punto di svolta:** **(d3), non (d2).**
- ### **D3-R A `34`, CON `F` DEFINITA:**
  - **Anderson muore a ogni scena alla seconda valutazione: «il punto medio di `Omega` non esiste qui»** *(anche l'NK interno non converge: `Omega robusto` `0` volte, `non esiste` `4` volte)*;
  - **NK esterno: non converge** *(`8452`, `8514` valutazioni)* **o porta un `s` sotto zero** *(`100000`, `200000`)*.
- ### **LE LETTURE** *(sez. `12`)*: **(d3): la legge interna** *(`Omega`)* **e il dominio** *(`s > 0`)* **cedono PRIMA del punto fisso di `cs`.** **(pf5) confermata.** **(pf1), (pf2), (pf4) restano NON distinguibili:** **il punto fisso a `34`, se c'e', sta fuori da dove `F` e' definita lungo ogni strada provata.**
- ### **FERMO SUL RIMEDIO** *(la regola del progetto)*: **le letture per Luca:**
  - **il guscio NON e' la causa** *(contrae)*; **la causa sta al CENTRO** *(coerente col revisore, P4: «il modo al centro», a densita' alte)*;
  - **i candidati delle `09:59`** *(R4: la memoria `A15`, una legge di `cs` meno sensibile a `Lambda` piccolo, `cs` dal tick precedente)* **vanno riletti cosi':** **una legge «meno sensibile a `Lambda` PICCOLO» cura il guscio, che gia' contrae: NON e' la cura.**
  - ### **La mia proposta** *(la scelta e' di Luca)*: **P4 del revisore come prova successiva** *(il pacchetto senza guscio alla stessa massa: se la mappa NON contrae neanche li', la causa e' la densita' al centro, non il guscio)*; **e la memoria `A15`** *(`cs` che RILASSA verso `cs(Lambda)`)* **come il candidato che toglie il punto fisso del tick** *(e con esso il dominio che cede)*, **da valutare dopo P4.**

## 15. IL RIMANDO ALLE NOTE SULLA GRAVITA' *(Luca `2026-11-09` `10:17`, X2)*

- **Le note di progetto «la gravita' nel modello»** *(G1-G8: il guscio di `cs`, perche' una `cs` locale non da' portata, la `U(1)`, le strade, il limite delle `2+1` dimensioni, il piano 2D poi 3D)* **stanno SUL PRINCIPALE:** `doc/TASK_HISTORY/2026-11-09_gravita_note_di_progetto.md` *(`5f4b5216`, `93254ada`)*.
- **Il legame con questo task history:** **G1 e' il guscio di R1** *(confermato qui, sez. `14`)*; **G5.3** *(una `cs` che si diffonde)* **e' uno dei candidati della cura.**

## 16. LA CURA DI `cs`: QUATTRO FORME A CONFRONTO, CON LE PREVISIONI SCRITTE PRIMA *(Luca `2026-11-09` `14:53`-`15:01`; SOLO PROGETTO: nessun codice, nessuna corsa, nessuna legge cambiata)*

### 16.1 IL FATTO DI PARTENZA E UNA PRECISAZIONE DAL REFERTO

- **(r-D5)** *(`0f639f12`, `7/7`)*:
  - **il guscio** di `Lambda` svuotato c'e' *(`r` `16`-`18`, `cs/s` minimo da `0.086` a `0.024`)*, **ma CONTRAE** *(`0.03`-`0.06`)*;
  - **la direzione instabile sta al CENTRO in tutte le scene mature** *(g2; lo conferma il revisore, con un pacchetto senza guscio, a densita' `3`-`10` volte maggiori)*;
  - **il meccanismo e' (d3):** **scendendo da `Lambda_c 272`, a `161.7` la mappa esce dal dominio** *(`s <= 0`)* **dove ancora contrarrebbe** *(`|Jv| 0.92`)*; **e il punto medio di `Omega` non esiste.**
- **La legge di oggi `cs = Lambda / (Lambda + Lambda_c)` sta in `[0, 1)` per costruzione** *(`Lambda >= 0`)*: **`s <= 0` non e' una previsione della legge, e' il segno che dentro la legge non c'e' un `cs` coerente** *(Luca)*.
- ### ⚠ **LA PRECISAZIONE, dal referto:**
  - **gli `s <= 0` nascono nei punti di PROVA dei metodi** *(NK propone un `x` libero in `R^n`, anche negativo, e il tick alza)*;
  - **`F(x)`, cioe' la legge applicata, e' SEMPRE in `[0, 1)`.**
  - **Quindi il muro (d3) e' un muro del DOMINIO DI `F`, non dei valori della legge:** **la mappa non sa dove portarsi senza uscire.** **Conta per F3** *(che allarga il dominio)* **e per F1** *(che non cerca punti di prova)*.

### 16.2 LE QUATTRO FORME

#### F1. LA MEMORIA (`A15`)

- **La formula:** **`cs_nuovo = cs_vecchio + (cs_legge(Lambda) - cs_vecchio) r`**, **`r` in `(0, 1]`.**
- **Da che cosa si ricava `r`** *(`A15`: non un numero scelto; le proposte, la scelta e' di Luca)*:
  - **(r-a) dal battito locale del vuoto:** **`r = 1 - e^{-omega_v dtau}`** *(`omega_v` la frequenza del vuoto locale, IS2: `0.471` per tick a `s 0.15`; `r ~ 0.38`)*;
  - **(r-b) dal tempo di risposta di `Lambda`:** **`r = dtau / tau_Lambda`**, **con `tau_Lambda` misurato** *(il tempo di rilassamento di `Lambda` dopo un disturbo: una misura da fare)*;
  - **(r-c) `r = s`** *(il quanto di tempo stesso)*: **il piu' semplice, ma e' una coincidenza dichiarata, non una derivazione.**
- **Cura:**
  - **nessun punto fisso da cercare, quindi nessuna divergenza;**
  - **`cs` resta positivo per costruzione** *(una media pesata di due numeri positivi, con `r` in `(0, 1]`)*.
- ### **NON cura, o da progettare:**
  - ### **C1, LA REVERSIBILITA':** **un rilassamento del primo ordine NON e' reversibile** *(dimentica: e' dissipativo)*. **Due strade, da scrivere prima del codice:**
    - **(m1)** **l'aggiornamento SIMMETRICO a meta' tick** *(`cs` letto da `Lambda` del punto medio, come fa oggi il punto fisso, ma ESPLICITO dal tick prima)*, **con l'inversa scritta: tornare indietro vuol dire riapplicare la stessa formula col segno di `dtau` cambiato** *(va verificato che la composizione sia l'identita': in generale NON lo e' per un rilassamento)*;
    - **(m2)** **`cs` come variabile dinamica col suo coniugato** *(un oscillatore smorzato: il secondo ordine e' reversibile se lo smorzamento e' uno scambio con il vuoto e non una perdita)*: **piu' stati, ma il palindromo resta.**
  - ### **C4, L'ENERGIA:** **cio' che la memoria dimentica diventa CALORE DEL VUOTO LOCALE** *(`A15`)*: **un termine nuovo nel bilancio, da scrivere nella forma.**
- **Le previsioni, scritte prima:**
  - **la corsa col solitone e `cs` acceso arriva fino in fondo** *(niente punto fisso, niente dominio)*;
  - **vicino al solitone `cs` segue `Lambda` con un ritardo di circa `1/r` tick**;
  - **la direzione instabile al centro DIVENTA un modo smorzato** *(un fattore `(1 - r) + r J`: con `|J| ~ 13` e `r` `~0.4` il fattore e' `~5`: NON contrae per forza)*. ### ⚠ **Quindi F1 da sola NON garantisce la stabilita' della dinamica:** **toglie il punto fisso, ma l'amplificazione al centro puo' tornare come instabilita' NEL TEMPO.** **Da misurare.**

#### F2. LO SMUSSAMENTO NELLO SPAZIO

- **La formula:** **`cs` dalla media di `Lambda` sul primo anello** *(i `6` vicini piu' il nodo, la localita' minima)*: **`cs = cs_legge(<Lambda>_1)`**; **il secondo anello solo come variante dichiarata.**
- **Cura:** **attenua le variazioni rapide da nodo a nodo**, **di cui e' fatta la direzione instabile al centro** *(R2: il profilo di `v^2` cade di `10` ordini in `10` nodi)*.
- **NON cura:** **resta un punto fisso da risolvere, e il bordo del dominio resta.**
- **La previsione da misurare:** **di quanto scende `|Jv|/|v|` al centro con la media a `6`** *(D2)*. **La mia stima, scritta prima:** **una media su `7` nodi abbassa il modo piu' corto di un fattore fino a `~7`** *(da `~13` a `~2`: ancora sopra `1`)*: **da sola probabilmente NON basta.**
- **Il legame con la gravita'** *(G5 delle note)*: **un orologio che sente un INTORNO, non un punto.**
- **C2:** **nel vuoto uniforme la media e' il valore stesso: `cs = s` al bit** *(se la media si calcola nello stesso ordine: da verificare)*.

#### F3. LA RAMPA SIMMETRICA RISPETTO ALLO ZERO *(Luca `14:58`)*

- **Le forme:**
  - **la razionale simmetrica:** **`cs = (Lambda - Lambda*) / (|Lambda - Lambda*| + Lambda_c)`**, **in `(-1, 1)`**;
  - **la tangente iperbolica:** **`cs = c_max tanh((Lambda - Lambda*) / Lambda_c)`.**
- ### **IL VINCOLO DEL VUOTO** *(C2: `cs(Lambda_v = 6) = s = 0.15`)*, **scritto:**
  - **per la razionale:** **`Lambda_c = (6 - Lambda*) (1 - s) / s = 5.667 (6 - Lambda*)`**: **ogni `Lambda*` in `[0, 6)` lo soddisfa, con `Lambda_c` aggiustato.** ### **Il vincolo del vuoto NON fissa `Lambda*`: lascia una famiglia a un parametro.**
  - ### **E UN FATTO DELLA FORMA:** **a `Lambda* = 0` la razionale simmetrica E' la legge di oggi** *(per `Lambda >= 0`, `|Lambda| = Lambda`)*: **non cambia niente.** **F3 cambia qualcosa SOLO con `Lambda* > 0`.**
  - **Con `Lambda*` sopra il minimo del guscio** *(`0.12`-`0.44`)*, **il guscio avrebbe il tempo NEGATIVO.**
- **Da che cosa derivare `Lambda*`** *(le proposte; la scelta e' di Luca)*:
  - **(l-a) dal vuoto:** **il `Lambda` sotto cui il vuoto F3 non e' piu' un vuoto** *(da misurare: la densita' minima di un vuoto stabile)*;
  - **(l-b) da un rapporto delle leggi:** **il `Lambda` dove `cs` e la sua derivata danno lo stesso ritmo** *(da scrivere)*;
  - **(l-c) dal quanto di olonomia** *(la (g) della voce `35`)*, **che oggi non c'e'.**
- **Cura:** **toglie il bordo del dominio** *(il muro di (d3))*: **il tick con `s < 0` e' il tick INVERSO, che esiste ed e' reversibile** *(il palindromo con `dtau` negativo)*. ### ⚠ **Ma il nucleo oggi ALZA con `s <= 0`** *(`flussi_parziali`)*: **F3 chiede di togliere quell'assert, nel nucleo: un cambio del nucleo, sul laterale.**
- **NON cura da sola:** **l'amplificazione al centro** *(`|J| > 1`)*.
- ### **LE CONSEGUENZE, SCRITTE COME PREVISIONI, NON COME SCOPERTE:**
  - **dove `cs = 0` il tempo si ferma:** **una SUPERFICIE dove niente evolve, fra una regione a tempo in avanti e una a tempo all'indietro** *(un muro, simile a un orizzonte)*;
  - **la materia nella regione a tempo negativo, letta con Feynman-Stueckelberg, come ANTIMATERIA**;
  - **la causalita':** **un segnale non attraversa la superficie a `cs = 0`** *(la velocita' locale va a zero)*; **ai due lati le frecce del tempo sono opposte**;
  - **l'energia:** **col tempo che cambia segno, l'energia locale `H dtau` cambia segno**: **da scrivere se il bilancio si chiude attraverso il muro** *(C4)*.

#### F4. LA COMBINAZIONE: F3 COME LEGGE, F1 COME MODO DI ARRIVARCI

- **`cs_nuovo = cs_vecchio + (cs_F3(Lambda) - cs_vecchio) r`.**
- **F3 toglie il muro del dominio, F1 toglie la divergenza del punto fisso.**
- **Le proprieta' buone di tutte e due:**
  - **il dominio: si'** *(con F3 `cs` puo' passare per zero senza uscire)*;
  - ### ⚠ **la positivita' di F1 si PERDE** *(con F3 la legge e' negativa sotto `Lambda*`)*: **non serve piu', perche' il tempo negativo e' ammesso;**
  - **la reversibilita': quella di F1 (C1), da risolvere comunque;**
  - **l'amplificazione al centro: non curata da nessuna delle due** *(vedi F1: un fattore `~5` nel tempo)*.

### 16.3 I CRITERI DI SCELTA *(C1-C6, per la decisione di Luca)*

| | **F1 la memoria** | **F2 lo smussamento** | **F3 la rampa simmetrica** | **F4 F3 + F1** |
|---|---|---|---|---|
| **C1 il tick reversibile e unitario** | ### **no, se del primo ordine**; (m1) da verificare, (m2) si' | si' *(e' ancora il punto fisso di oggi)* | si', **col tick inverso a `s < 0`** *(e l'assert del nucleo tolto)* | come F1 |
| **C2 il vuoto `cs = s` al bit** | si' *(`cs_legge(6) = s`: il rilassamento resta fermo)* | si', da verificare l'ordine della media | si', **col vincolo su `Lambda_c`** | si' |
| **C3 il solitone maturo fino in fondo** | **probabile, non garantito** *(l'amplificazione nel tempo)* | **improbabile** *(resta il punto fisso, `|J|` `~2`)* | **no da sola** *(resta il punto fisso con `|J| ~13`)* | probabile, non garantito |
| **C4 il bilancio dell'energia** | **un termine nuovo: il calore della memoria** | chiuso come oggi | **da scrivere attraverso il muro** | tutti e due |
| **C5 i parametri nuovi** | **`r`, da derivare** | **nessuno** *(il primo anello)* | **`Lambda*`, da derivare** | `r` e `Lambda*` |
| **C6 il legame con la gravita'** | un punto, con memoria | **un intorno** | un punto | un punto, con memoria |

### 16.4 LA PROVA CHE DECIDERA' *(da progettare, NON da fare)*

- **La scena:** **quella di (r-D5)** *(`TBS` maturo dalla libreria, `Lambda_c 34`)*.
- **Per ciascuna forma:**
  - **D2:** **`|Jv|/|v|` al centro, al guscio, nel vuoto** *(per F1 e F4: il fattore del rilassamento `(1 - r) + r J`, non `J`)*;
  - **una corsa corta con `cs` acceso:** **`1000` tick** *(`150` unita')*, **la norma, l'energia e il minimo di `cs` stampati a ogni `10` tick.**
- **Le letture, scritte prima:**
  - **(k1) la forma arriva in fondo, col vuoto al bit:** **candidata**;
  - **(k2) esce dal dominio o alza:** **scartata, col tick in cui succede**;
  - **(k3) arriva in fondo, ma una grandezza cresce senza limite** *(l'amplificazione nel tempo)*: **instabile, con il ritmo di crescita.**
- **Il costo stimato** *(dal referto di (r-D5): `0.15` s per mezzo tick sulla scena di `TBS`)*:
  - **D2: `~1` minuto per forma;**
  - **la corsa corta: `1000` tick x `~0.3` s = `~5` minuti per forma** *(F2 e F3 col punto fisso: fino a `120` giri per tick, quindi fino a `~10` ore se non converge; si ferma al primo tick che non converge)*;
  - **in tutto, le quattro forme: `~1` ora, se F2 e F3 si fermano presto.**

### 16.5 LE DOMANDE A LUCA *(il criterio di chiusura: la sua risposta, registrata qui)*

1. **Quale forma, o quale combinazione, provare per PRIMA?** *(la mia raccomandazione: F1 con (m2), o F4, perche' sono le sole che tolgono il punto fisso; F2 come misura accessoria, a costo nullo di parametri)*
2. **Da che cosa ricavare `r`** *(F1: (r-a) il battito del vuoto, (r-b) il tempo di risposta di `Lambda`, (r-c) `s`)*?
3. **Da che cosa ricavare `Lambda*`** *(F3: (l-a), (l-b), (l-c))*, **sapendo che il vincolo del vuoto lascia una famiglia e che a `Lambda* = 0` F3 e' la legge di oggi?**
4. **C1:** **la memoria del primo ordine NON e' reversibile:** **e' accettabile un termine dissipativo dichiarato** *(il calore del vuoto)*, **o si vuole (m2)** *(`cs` col suo coniugato)*?

## 17. LA DECISIONE DI LUCA DELLE `16:18` SULLA CURA DI `cs`: **SI PROVA PER PRIMA F1, LA MEMORIA (`A15`)**

- **Da proporre e scrivere PRIMA del codice:**
  - **da che cosa si ricava `r`** *(il tempo di memoria: non un numero scelto)*;
  - **dove si aggiorna `cs` nel palindromo, e come si inverte**;
  - **il bilancio locale.**
- **F3** *(la rampa simmetrica)* **dopo, o dentro F4, quando F1 avra' detto qualcosa**; **`Lambda*` da derivare.**
- **L'ordine:** **il progetto dettagliato di F1 nella sezione dopo, poi il codice, poi la prova sulla scena di (r-D5).**

## 18. F1, LA MEMORIA (`A15`): IL PROGETTO DETTAGLIATO, PRIMA DEL CODICE *(Luca `16:18`)*

### 18.1 LE PREMESSE DAL CODICE

- **Oggi `cs` del tick e' il PUNTO FISSO di `tick.cs_al_centro`:** **`cs = FP.cs(Lambda(x), Lambda_c)` con `Lambda` del vuoto al CENTRO del palindromo, avanzato di mezzo tick con `mot.cs = x`.** **E' quello che non si trova** *(r-D5)*.
- **Dentro il tick `cs` e' costante** *(un array per nodo)*: **il palindromo usa lo stesso `cs` in tutte e due le meta'.**
- ### **NON SO, e va letto prima del codice:** **che cosa usa `CAMM-FASE-VUOTO` oltre a `mot.cs`** *(`energia_pesata.applica` legge anche `mot.lambda_c` e `cs_primo`: la derivata `dcs/dLambda` della legge)*. **Con F1 `cs` non e' piu' una funzione istantanea di `Lambda`:** **che cosa diventa `cs'`?** **Due possibilita':** **(q1) `cs'` resta la derivata della LEGGE** *(il valore a cui `cs` tende)*; **(q2) `cs'` e' zero** *(`cs` e' una variabile di stato, non una funzione)*. **La scelta e' di fisica: la porto a Luca coi numeri della prova, misurata nei due modi.**

### 18.2 LA FORMA PROPOSTA

- ### **DOVE: al CONFINE fra due tick, non dentro.**
  - **Nel tick `n + 1` `cs` e' COSTANTE** *(il palindromo resta intatto: niente punto fisso dentro il tick)*;
  - **al confine, dallo stato del confine** *(che e' lo stesso andando avanti e tornando indietro)*, **si aggiorna `cs`.**
- ### **COME: la regola del TRAPEZIO** *(Crank-Nicolson)*, **che e' simmetrica nel tempo:**
  - **`cs_{n+1} = cs_n + r (L - (cs_n + cs_{n+1}) / 2)`**, **cioe' `cs_{n+1} = [cs_n (1 - r/2) + r L] / (1 + r/2)`**, **con `L = FP.cs(Lambda_confine, Lambda_c)`.**
  - ### **L'INVERSA, scritta:** **`cs_n = [cs_{n+1} (1 + r/2) - r L] / (1 - r/2)`**, **con lo STESSO `L`** *(lo stato del confine)*. **Esiste per `r < 2`.**
  - **Il tick all'indietro:** **il tick inverso con `cs_{n+1}`, poi l'inversa al confine.** **Esatta in aritmetica esatta; in virgola mobile entro l'arrotondamento** *(NON al bit: lo dico prima)*.
- ### **`cs` resta positivo:** **con `cs_n > 0`, `L > 0` e `r < 2`, `cs_{n+1}` e' una combinazione a pesi positivi** *(`(1 - r/2)/(1 + r/2)` e `r/(1 + r/2)`)*.

### 18.3 DA CHE COSA SI RICAVA `r` *(`A15`: non un numero scelto)*

- ### **La proposta: dal BATTITO LOCALE DEL VUOTO:** **`r = omega_v dtau`**, **con `omega_v` la rotazione di fase del vuoto per tick, misurata PER NODO dallo stato** *(nel vuoto F3 a `s 0.15`: `0.471` per tick, IS2)*. **E' il tempo di risposta piu' naturale del vuoto locale: un giro di fase per `1/omega_v` tick.**
- **Le alternative, scritte:** **`r` dal tempo di risposta di `Lambda`** *(da misurare)*; **`r = s`** *(una coincidenza, non una derivazione)*.

### 18.4 IL BILANCIO LOCALE *(`A15`: cio' che la memoria dimentica diventa calore del vuoto)*

- **Al confine lo stato non cambia, cambia `cs`:** **l'energia pesata cambia di `Delta E = H(stato, cs_{n+1}) - H(stato, cs_n)`.**
- ### **Quel `Delta E` e' il CALORE DELLA MEMORIA:** **un termine nuovo del bilancio, contato per nodo e sommato** *(un accumulatore, come quelli del bordo)*. **La prova lo stampa.**

### 18.5 LE PREVISIONI, SCRITTE PRIMA *(incluse quelle scomode)*

- **C2, il vuoto:** **nel vuoto F3 `L = s` ovunque, e con `cs_n = s` il trapezio da' `cs_{n+1} = s`** *(in aritmetica esatta)*. **In virgola mobile entro `8 eps`, NON al bit garantito.**
- ### **C3, LA STABILITA' NEL TEMPO, LA PREVISIONE SCOMODA:**
  - **una perturbazione `delta cs` cresce, da un tick all'altro, di un fattore `~ (1 - r/2 + r J_t) / (1 + r/2)`**, **con `J_t` la risposta di `L` a `cs` in UN tick** *(dell'ordine del `|J| ~ 11`-`15` di D2, che e' su mezzo tick: forse il doppio)*;
  - **con `r ~ 0.47` e `J_t ~ 13`-`26` il fattore e' `~5`-`10` per tick:** **la memoria CRESCEREBBE in poche decine di tick** *(la lettura (k3))*;
  - ### **la condizione di stabilita' e' circa `r |J_t| < 2`, cioe' `r < ~0.1`:** **piu' piccolo del battito del vuoto.** **Se la prova lo conferma, F1 col `r` derivato NON basta da sola**, **e la scelta e' di Luca:** **un `r` piu' piccolo ha bisogno di un'altra derivazione** *(non di una scelta)*, **oppure F1 va con F2** *(lo smussamento abbassa `J`)*.
- **Vicino al solitone, se stabile:** **`cs` segue `L` con un ritardo di `~1/r` tick.**

### 18.6 LA PROVA *(il codice dopo questa sezione, poi la corsa)*

- **La scena:** **`TBS` a `10000` tick dalla libreria** *(lo stato di (r-D5))*, **`Lambda_c 34`, `cs` iniziale = `L` dello stato.**
- **`200` tick con F1** *(due modi di `cs'`: (q1) e (q2))*, **stampando ogni tick:** **`max|cs - L|`, `min cs`, la norma, l'energia, il calore della memoria.**
- **E il fattore di crescita MISURATO:** **due corse con `cs` iniziale diverso di `1e-8` sul centro:** **la differenza tick per tick.**
- **I DEVE:**
  - **(F1-V)** **il vuoto F3 da solo, `50` tick: `cs = s` entro `8 eps`** *(C2)*;
  - **(F1-I)** **l'inversa al confine: `5` tick avanti e `5` indietro ridanno lo stato e `cs` entro `1e-10`** *(C1)*;
  - **(F1-F) DEVE FALLIRE:** **lo stesso F1-I con la regola esplicita** *(`cs_{n+1} = cs_n + r (L - cs_n)`, senza il trapezio)* **e l'inversa del trapezio** *(l'inversa sbagliata: deve dare uno scarto oltre `1e-10`)*.
- **Le letture** *(le `k1`-`k3` della sez. `16.4`)*: **(k1) arriva in fondo coi DEVE: candidata; (k2) esce dal dominio o alza; (k3) arriva ma cresce: col fattore misurato.**
- **Il costo:** **`~0.3` s per tick: `200` tick x `2` modi x `2` corse `~4` minuti; i DEVE `~1` minuto.**

### 18.7 ANNOTAZIONE PRIMA DEL CODICE *(`csv/solitone/carta_f1.py`)*

- ### **F1-I si STRINGE:** **non «`5` tick avanti e `5` indietro»**, **ma l'inversa del trapezio al confine** *(`1000` terne a caso di `cs`, `L`, `r`: entro `1e-14` relativo)*.
  - **Perche':** **dentro il tick `cs` e' costante, e la reversibilita' del tick a `cs` costante e' quella del NUCLEO** *(collaudata dalla suite)*;
  - **il pezzo NUOVO di F1 e' solo l'aggiornamento al confine:** **e' quello che va provato.**
  - **F1-F diventa:** **la regola esplicita invertita col trapezio** *(deve sbagliare)*.
- **`r = omega_v`** *(la rotazione di fase del vuoto nel tick appena fatto, per nodo)* **puo' superare `2`** *(fino a `pi`)*: **li' il trapezio non e' piu' una media a pesi positivi.** **Il referto stampa `r` minimo e massimo.**
- **Il calore della memoria = `g_pesata(cs nuovo) - g_pesata(cs vecchio)` sullo stesso stato, sommato.**
- **Il fattore di crescita:** **due corse, con `cs` iniziale perturbato di `1e-8` sui nodi del centro** *(`r < 1`)*, **la differenza tick per tick e il rapporto mediano sui primi `20`.**

## 19. F1, IL PRIMO GIRO: **INTERROTTO DA UN DIFETTO MIO** *(`doc/referti_l2/carta_f1_interrotto.txt`; il codice a `f406890d`, blob `3a488d55`; `17:50`)*

- **F1-I passa** *(l'inversa del trapezio `2.41e-15`)*; **F1-F fallisce come deve** *(`3.71e+01`)*.
- ### **IL DIFETTO MIO:** **`omega_v` somma `conj(phi0) phi1` sull'asse `1`, ma `phi_h` ha UNA dimensione** *(una fase per estremita' d'arco, non un vettore come `psi_h`)*: **`AxisError` al primo tick del vuoto.** **Nessuna corsa di F1 e' avvenuta.**
- **La cura** *(un commit a se')*: **`np.add.at(z, nodo, conj(phi0) phi1)` senza la somma.** **Nessuna lettura cambia.**

## 20. L'ESITO DI F1: **`2/3` -- F1-V FALLISCE (IL VUOTO SI SPOSTA DI `1.7e-15` IN `50` TICK); LA SCENA ARRIVA A `200` TICK NEI DUE MODI; (q1) E' SENSIBILISSIMO (`1e-8` -> `3e-2` IN `5` TICK) E `r` ARRIVA A `3.14`; (q2) CRESCE PIANO (`1e-8` -> `7e-6` IN `200` TICK); FERMO** *(`doc/referti_l2/carta_f1.txt`; il codice a `f5f0c47c`, blob `6040448a`; `18:23`-`18:27`)*

- **I DEVE:** **F1-I passa** *(`2.41e-15`)*; **F1-F fallisce come deve** *(`37.1`)*.
- ### **F1-V FALLISCE:** **nel vuoto F3, in `50` tick, `cs` si sposta da `s` di `1.721e-15`, contro la soglia `8 eps s = 2.7e-16`** *(una soglia mia, scritta prima: `8 eps` RELATIVO)*.
  - **Lo scarto e' `~60` ulp di `s`:** **l'arrotondamento del trapezio e del ciclo `cs -> tick -> L` si ACCUMULA nei `50` tick.**
  - ### **Lo scrivo come fallimento, e non lo rileggo:** **C2 chiedeva il vuoto «al bit con oggi»; F1 lo tiene a `1e-15`, non al bit.** **Una soglia per tick, o la deriva in funzione del numero di tick, sono una decisione di Luca, non mia.**
- ### **LA SCENA** *(`TBS` a `10000` tick)*, **`200` tick, la norma conservata a `1e-15` relativo nei due modi:**

| | **(q1) `cs'` della legge** | **(q2) `cs' = 0`** |
|---|---|---|
| **arriva a `200` tick** | **si'** | **si'** |
| **`max|cs - L|`** *(tick `1`, `200`)* | `4.5e-2`, `3.8e-2` | `2.3e-2`, `2.2e-2` |
| **`cs` min, max** *(tick `200`)* | `0.0041`, `0.454` | `0.0013`, `0.475` |
| **`r` max** *(il battito del vuoto)* | ### **`3.14`: oltre `2`, il trapezio NON e' piu' una media a pesi positivi** | **`1.70`** |
| **la perturbazione `1e-8` sul centro, la differenza ai tick `1`, `5`, `20`, `200`** | ### **`9.7e-8`, `3.1e-2`, `1.8e-1`, `3.3e-1`: satura a `O(1)` in pochi tick** | **`5.6e-9`, `4.5e-9`, `6.1e-8`, `6.9e-6`** |
| **il calore della memoria** *(la somma, `200` tick)* | `-2.62e5` | `-3.60e4` |

- ### **LE LETTURE** *(sez. `16.4`, `k1`-`k3`)*:
  - **(q1): (k3), arriva ma e' INSTABILE:** **una perturbazione di `1e-8` diventa di ordine `1` in meno di `10` tick.** **La previsione scomoda della sez. `18.5` e' confermata in (q1).** **E `r` oltre `2` rompe la positivita' del trapezio** *(il battito del vuoto con `cs` acceso arriva quasi a `pi` per tick)*.
  - ### **(q2): quasi (k1):** **arriva, e la perturbazione cresce di un fattore `~1000` in `200` tick** *(dopo i primi `20` quasi ferma)*: **una crescita lenta, molto sotto la previsione.** **Ma F1-V fallisce, quindi NON la chiamo candidata.**
  - **Il calore della memoria e' grande e NEGATIVO in tutti e due** *(l'energia pesata cala a ogni aggiornamento)*: **da confrontare con l'energia della scena** *(non stampata: un difetto dello strumento)*.
- ### **FERMO** *(un DEVE che fallisce)*. **Le domande a Luca:**
  1. **F1-V:** **una deriva di `~1e-15` in `50` tick nel vuoto e' accettabile** *(una soglia per tick, dichiarata)*, **o il vuoto deve restare al bit** *(e allora il trapezio va scritto in modo che con `L = cs` dia `cs` esatto: per esempio `cs + r (L - cs) / (1 + r/2)`, che a `L = cs` da' `cs` al bit)*?
  2. ### **(q1) contro (q2):** **che cosa e' `cs'` quando `cs` e' una memoria?** **I numeri dicono: con `cs'` della legge e' instabile, con `cs' = 0` no.** **E' una scelta di fisica.**
  3. **`r` oltre `2`** *(in (q1))*: **il battito del vuoto come tempo di memoria va limitato, o ricavato diversamente?**

## 21. LE DECISIONI DI LUCA DELLE `18:46` SU F1, E LA FORMA CHE NE SEGUE *(prima del codice)*

- **REGISTRATO** *(Luca)*:
  - **(4) il vuoto resta AL BIT;**
  - **(5) `cs'` dentro il tick: (q2), `cs' = 0`**; **la memoria si aggiorna solo al confine** *(`A15`)*;
  - **(6) `r` NON si limita a mano: si DERIVA dal rilassamento ESATTO su un passo** *(`dcs/dt = omega (L - cs)` integrato su `dtau`: `cs_nuovo = L + (cs - L) e^{-omega dtau}`, cioe' `r = 1 - e^{-omega dtau}`, sempre in `(0, 1)`)*; **`omega` il battito locale del vuoto.**
- ### **LA FORMA, la mia lettura di (4) e (6) insieme** *(dichiarata)*: **`cs_nuovo = cs + r (L - cs)`, `r = 1 - e^{-omega}`** *(`omega` la rotazione del vuoto nel tick: gia' «per tick»)*.
  - **E' il rilassamento esatto di (6)**, **e a `L = cs` da' `cs` AL BIT** *(`r x 0 = 0`: (4))*. **La forma del trapezio esatta di (4)** *(`cs + r (L - cs) / (1 + r/2)`)* **e' del trapezio, non del rilassamento esatto: con (6) non serve.**
  - **L'inversa:** **`cs = (cs_nuovo - r L) / (1 - r)`** *(esiste: `r < 1`)*.
- ### **I DEVE:** **F1-V al BIT** *(il vuoto F3, `50` tick: `cs == s`, ogni nodo, ogni tick)*; **F1-I** *(l'inversa nuova, `1e-14` relativo)*; **F1-F** *(DEVE FALLIRE: la regola invertita col trapezio)*.
- ### **LA PREVISIONE, scritta prima** *(di Luca)*: **dove `r` valeva `~0.47`, ora `~0.37`** *(`1 - e^{-0.471} = 0.376`)*; **la crescita di (q2) scende**; **ma la stabilita' vuole `r < ~0.1`** *(la mia stima, sez. `18.5`)*: ### **se la perturbazione cresce ancora: FERMO, con la proposta di un tempo di memoria piu' lento** *(per esempio la risposta di `Lambda`)* **e le sue letture.**
- **La prova:** **(q2) solo; `200` tick; se la differenza a `200` resta sotto `1e-4`, si va a `1000`** *(«e oltre, se stabile»: la soglia `1e-4` e' mia, dichiarata)*.

## 22. L'ESITO DI F1 COL RILASSAMENTO ESATTO: **`2/3` -- F1-V FALLISCE ANCORA (`7.8e-16`: E' `Lambda` DEL VUOTO CHE CAMBIA AGLI ULTIMI BIT); `r` MAX `0.81`; LA PERTURBAZIONE CRESCE ANCORA (`1e-8` -> `6.3e-5` A `200`, `5.4e-2` A `1000` TICK): FERMO, LA PROPOSTA DI UN TEMPO DI MEMORIA PIU' LENTO** *(`doc/referti_l2/carta_f1.txt`; il codice a `d2689b81`, blob `b0b5deb1`; `19:43`-`19:49`)*

- **I DEVE:** **F1-I passa** *(l'inversa del rilassamento `6.1e-15`)*; **F1-F fallisce come deve** *(`5.2`)*.
- ### **F1-V FALLISCE:** **nel vuoto F3, in `50` tick, `cs` si sposta dal suo valore iniziale di `7.772e-16`** *(`~5` ulp di `s`; prima, col trapezio e (q2) assente, `1.7e-15`)*.
  - **La forma `cs + r (L - cs)` da' `cs` al bit SOLO se `L = cs` al bit:** **ma `L` si ricalcola a ogni tick da `Lambda` del vuoto DOPO il tick**, **e `Lambda` del vuoto F3 cambia agli ultimi bit da un tick all'altro** *(l'arrotondamento del tick stesso)*.
  - ### **Quindi il vuoto «al bit» con F1 chiede che `Lambda` del vuoto sia costante al bit lungo i tick:** **una proprieta' del tick, non di F1.** **Da misurare a parte** *(la deriva di `Lambda` del vuoto F3 tick per tick, a `cs` spento)*.
- ### **LA SCENA, (q2), `r = 1 - e^{-omega}`:**
  - **`r` va da `0` a `0.81`** *(prima `1.70`)*: **la previsione «`0.47` -> `0.37`» vale per il vuoto; vicino al solitone il battito e' piu' alto;**
  - **arriva a `200` tick, la norma conservata a `2e-15` relativo;** **`cs` min `0.0012` a `200` tick, `0.0003` a `1000`;**
  - ### **la perturbazione `1e-8` sul centro: `5.7e-9`, `4.5e-9`, `8.7e-9`, `6.4e-8`, `5.1e-8`, `4.4e-6`, `6.3e-5`** *(i tick `1`, `5`, `10`, `20`, `50`, `100`, `200`)*; **poi `4.3e-3`, `7.3e-3`, `5.0e-2`, `5.4e-2`** *(`400`, `600`, `800`, `1000`)*.
  - ### **CRESCE ANCORA:** **un fattore `~5e6` in `1000` tick** *(lento: in media `~1.016` per tick)*. **La previsione della sez. `18.5` era un fattore `~5` per tick: SBAGLIATA in eccesso** *(la stima lineare da `|J|` di D2 non vale per la memoria)*; **ma la crescita c'e'.**
  - **Il calore della memoria:** **`-5.2e4` in `200` tick.**
- ### **LA LETTURA:** **(k3), arriva ma cresce** *(lentamente)*. **La regola di Luca delle `18:46`: «se la perturbazione cresce ancora, FERMO, con la proposta di un tempo di memoria piu' lento».**
- ### **LA PROPOSTA: il tempo di memoria dalla RISPOSTA DI `Lambda`** *(la scelta e' di Luca)*:
  - **`r = 1 - e^{-dtau / tau_Lambda}`**, **`tau_Lambda` il tempo con cui `Lambda` del vuoto risponde a un disturbo, PER NODO**;
  - **da dove: la `tau_int` di Sokal della serie di `Lambda` al nodo** *(dalle mappe leggere di `TB3`/`TBS`, o da una corsa corta)*, **oppure il tempo di rilassamento di `Lambda` dopo un disturbo imposto** *(una misura)*;
  - ### **LE LETTURE, scritte prima:** **(t1) `tau_Lambda` molto piu' lungo di `1/omega`** *(`r < ~0.1` vicino al solitone)*: **F1 con quel `r`, e la crescita va rimisurata**; **(t2) `tau_Lambda ~ 1/omega`:** **il tempo di memoria lento non c'e' nella dinamica, e F1 da sola non basta: F2 o F4.**
- ### **E LA DOMANDA SU F1-V:** **«il vuoto al bit» con F1 e' possibile solo se `Lambda` del vuoto e' costante al bit:** **la misuro** *(una prova di un minuto)* **prima di qualunque altra cosa su F1?**

## 23. LE DECISIONI DI LUCA DELLE `20:13` SU F1, E T1: LA DERIVA DI `Lambda` DEL VUOTO A `cs` SPENTO -- **LE LETTURE PRIMA DELLA MISURA**

- **REGISTRATO** *(Luca)*:
  - **tre test brevi sul laterale, uno alla volta: T1** *(la deriva di `Lambda` del vuoto)*, **T2** *(F1 allungata)*, **T3** *(`tau_Lambda`)*; **poi FERMO: niente F2, F3, F4 senza la sua decisione;**
  - **il fattore `/(1 + r/2)` del mandato delle `18:46` era ridondante con `r = 1 - e^{-omega dtau}`:** **la forma `cs + r (L - cs)` resta quella giusta** *(l'errore e' del guardiano)*;
  - **se una lettura chiede di cambiare una regola (F1-V compreso): FERMO e la proposta.**
- ### **T1, LA MISURA:**
  - **il vuoto F3 da solo, il nucleo del laterale, `cs` SPENTO** *(`mot.lambda_c = None`)*, **`1000` tick** *(`tick.tick`)*;
  - **a ogni tick, per nodo: `Delta Lambda = Lambda(t+1) - Lambda(t)`, in valore e in ulp di `Lambda`** *(`np.spacing`)*;
  - **il max e la media di `|Delta Lambda|`; la deriva cumulata `Lambda(t) - Lambda(0)`** *(max, media, rms)* **ai tick `1`, `10`, `100`, `1000`;**
  - **la forma: la pendenza in log-log della rms della deriva fra `t 10` e `t 1000`.**
- ### **IL DEVE FALLIRE** *(Luca)*: **a meta' corsa** *(tick `500`)* **un `Lambda` di un nodo spostato di `1e-12`** *(la fase del vuoto di quel nodo scalata di `sqrt(1 + 1e-12 / Lambda)`: `Lambda` e' una densita', quadratica nelle fasi)*, **in una seconda corsa**: **T1-F: «la misura NON vede lo spostamento»** *(`max|Lambda_iniettata - Lambda| < 0.5e-12` dopo il tick `500`)* **DEVE FALLIRE.**
- ### **LE LETTURE, scritte prima** *(di Luca; i criteri numerici sono miei, dichiarati)*:
  - **(v1) `Lambda` costante AL BIT** *(`Delta Lambda = 0` a ogni tick, ogni nodo)*: **F1-V fallisce per colpa di F1: cerco la causa nella formula e mi fermo con la proposta.**
  - **(v2) `Lambda` oscilla di pochi ulp, limitata o `~sqrt(t)`** *(la pendenza della rms `< 0.75`)*: **F1-V va riformulato come «`cs` non deriva piu' di quanto deriva `Lambda`»: propongo il criterio, la decisione e' di Luca;** **intanto T2 e T3, con F1-V come lettura e non come cancello.**
  - **(v3) `Lambda` deriva in modo SISTEMATICO** *(la pendenza `>= 0.75`: lineare)*: **un fatto del tick, non di F1: una nota separata, e FERMO.**
  - **I due sotto-casi di (v2), per scriverli:** **limitata** *(pendenza `< 0.25`)*, **passeggiata casuale** *(fra `0.25` e `0.75`)*.
- **Lo script: `csv/solitone/lambda_vuoto_deriva.py`** *(nuovo)*; **il referto `doc/referti_l2/lambda_vuoto_deriva.txt`.**

- ### **IL RIMANDO, U1** *(Luca `2026-11-09` `20:16`)*: **l'unificazione dei due rami solo a lavori chiusi** *(`S162` e (r-b), `C50-0`, F1 con la decisione di Luca)*; **fino ad allora nessun merge, rebase, cherry-pick o porting.** **Il dettaglio sul principale:** `doc/TASK_HISTORY/2026-11-08_zero_simmetrico_nel_nucleo.md`, **sez. `10`** *(`e103636f`)*.

### 23.1 L'ESITO DI T1: **(v3) -- `Lambda` DEL VUOTO F3 A `cs` SPENTO DERIVA IN MODO SISTEMATICO E UNIFORME: `+2.2e-15` PER TICK, LA PENDENZA DELLA rms `0.985`; UN FATTO DEL TICK, NON DI F1: FERMO** *(`doc/referti_l2/lambda_vuoto_deriva.txt`; il codice a `141711d3`, blob `b4610021`; `20:51`-`20:53`)*

- **La scena:** **`6561` nodi** *(il toro `81 x 81` di `TBS`)*, **`mot.cs` = `0.15` ovunque, `mot.lambda_c = None`, `Lambda = 6` all'inizio.**
- **`|Delta Lambda|` per tick:** **max `1.066e-14`** *(`12` ulp)*, **media `2.499e-15`** *(`2.8` ulp)*; **i tick in cui NESSUN nodo cambia: `273` su `1000`.**
- ### **LA DERIVA CUMULATA `Lambda(t) - Lambda(0)`:**

| tick | max | media | rms |
|---|---|---|---|
| `1` | `1.776e-15` *(`2` ulp)* | `+1.776e-15` | `1.776e-15` |
| `10` | `2.487e-14` *(`28` ulp)* | `+2.400e-14` | `2.400e-14` |
| `100` | `2.256e-13` *(`254` ulp)* | `+2.256e-13` | `2.256e-13` |
| `1000` | `2.228e-12` *(`2508` ulp)* | `+2.228e-12` | `2.228e-12` |

- ### **La pendenza in log-log della rms fra `t 10` e `1000`: `0.985`: LINEARE.** **E max = media = rms: la deriva e' UGUALE su tutti i nodi e sempre POSITIVA** *(il vuoto cresce di `~2.2e-15` per tick: `3.7e-16` relativo, `~1.7` ulp relativi per tick)*.
- **T1-F fallisce come deve:** **lo spostamento di `1e-12` al tick `500` si vede** *(`9.4e-13`)*.
- ### **LA LETTURA: (v3), una deriva SISTEMATICA di `Lambda` del vuoto, a `cs` SPENTO, nel nucleo del laterale.** **E' un fatto del TICK, non di F1** *(F1-V falliva con `7.8e-16` in `50` tick: `~1e-13` di deriva di `Lambda` in `50` tick, coerente)*.
- ### **FERMO** *(la regola del mandato delle `20:13`)*. **T2 e T3 NON partono.** **Le cose per Luca:**
  - **una deriva lineare e uniforme di `Lambda` del vuoto, `+3.7e-16` relativo per tick:** **non e' una passeggiata casuale; e' un arrotondamento con un SEGNO** *(per esempio una norma che non si conserva al bit in un pezzo del tick, sempre per eccesso)*;
  - **da cercare: in quale pezzo del tick nasce** *(il tick pezzo per pezzo, la norma del vuoto dopo ciascuno)*: **una diagnosi, se Luca la vuole**;
  - **e se c'e' anche sul PRINCIPALE** *(senza v2)*: **la stessa misura col nucleo del principale** *(il principale e' congelato: si misura, non si tocca)*.

## 24. D2, IN QUALE PEZZO DEL TICK NASCE LA DERIVA DI `Lambda` *(Luca `2026-11-09` `23:02`)*: IL PROGETTO, PRIMA DEL CODICE

### 24.0 DA DOVE PARTE

- **D1 del principale e' su origin** *(`b34f6836`, poi la correzione `115a288d`)*. ### ⚠ **L'esito (w1) NON vale come «senza v2»:** **lo script girava il tick dentro `BE.conv(DC.ZERO)`, che SUL PRINCIPALE avvolge in memoria `grover`/`hop_psi`/`hop_phi` con lo zero simmetrico** *(le stesse operazioni del v2 di qui)*. **Quindi la frase del mandato «se D1 ha dato (w1), la causa e' nel tick condiviso» NON si puo' dichiarare oggi.** **D1-bis** *(`2bb5ee52`: i tick senza l'avvolgimento, la scena identica)* **ha dato (w3): il nucleo del principale deriva ANCHE LUI, sistematico e uniforme, ma col SEGNO OPPOSTO** *(`-2.313e-12` in `1000` tick, la pendenza `1.004`; qui `+2.228e-12`)*. **Questa misura separa la fase `conj(z)` del v2 dai due mezzi pezzi.**
- **La lettura del guardiano, da verificare:** **in un vuoto uniforme ogni nodo fa gli stessi conti, quindi l'errore e' uguale ovunque** *(T1: max = media = rms al tick `1000`: coerente)*; **un pezzo in virgola mobile non esattamente unitario allunga la norma.** **I sospetti:** **un coefficiente non esatto** *(`1/d` del Grover)*; **la fase `e^{-i theta/2}` del v2.**

### 24.1 I PEZZI DEL TICK, DAL CODICE, NELL'ORDINE *(D2.1)*

**`tick.tick` = `percorri_tick(st, mot, par, (), None, 14)`:** **`mot.apri_tick()`, i `14` pezzi di `composizione.ORDINE` ciascuno con `frazione 0.5`, `mot.chiudi_tick()`** *(apri e chiudi contano le crescite: non toccano lo stato)*.

| pos | id | operatore | su che cosa, **nel vuoto F3 con `psi = 0` e `lambda_c = None`** |
|---|---|---|---|
| `1` | `CAMM-MATERIA-VUOTO` | `materia_vuoto.applica` | `psi *= e^{-i alpha dtau f}`, `phi *= e^{-i beta dtau f}` con `alpha`, `beta` da `pezzi(rho, Lambda)`; **a `rho = 0` mi aspetto `beta = 0` e il fattore `exp(0) = 1` esatto** *(da misurare)* |
| `2` | `CAMM-FASE-VUOTO` | `energia_pesata.applica` | **ritorna subito:** `mot.lambda_c is None` *(riga «`if mot.cs is None or mot.lambda_c is None`»)* |
| `3` | `CAMM-MONETA-SPIN` | `_moneta_spin` | **solo `psi`** |
| `4` | `CAMM-GROVER` | `FP.grover` su `psi` | **solo `psi`** |
| `5` | `CAMM-SPOSTAMENTO` | `FP.hop_psi` | **solo `psi`** |
| `6` | `CAMM-GROVER-VUOTO` | `FP.grover` su `phi.reshape(-1, 1)` | **(6a)** `_grover_mezzo(h)`, **(6b)** `_grover_mezzo(h)`, **(6c)** `phi *= conj(z_nodo(h))`, con `h = f/2 = 0.25` |
| `7` | `CAMM-SPOSTAMENTO-VUOTO` | `FP.hop_phi` | **(7a)** `_hop_phi_mezzo(h)`, **(7b)** `_hop_phi_mezzo(h)`, **(7c)** `phi *= conj(z_arco(h))` sulle due estremita' |
| `8` | `CAMM-SPOSTAMENTO-VUOTO` | come `7` | **(8a)**, **(8b)**, **(8c)** |
| `9` | `CAMM-GROVER-VUOTO` | come `6` | **(9a)**, **(9b)**, **(9c)** |
| `10` | `CAMM-SPOSTAMENTO` | `FP.hop_psi` | solo `psi` |
| `11` | `CAMM-GROVER` | `FP.grover` su `psi` | solo `psi` |
| `12` | `CAMM-MONETA-SPIN` | `_moneta_spin` | solo `psi` |
| `13` | `CAMM-FASE-VUOTO` | `energia_pesata.applica` | ritorna subito |
| `14` | `CAMM-MATERIA-VUOTO` | `materia_vuoto.applica` | come `1` |

- **I coefficienti, dal codice** *(`primo_ordine/flussi_parziali.py`)*:
  - **`z = e^{i pi s h}`** da `espi` *(`cos` di `pi s`, `sin` di `pi min(s, 1 - s)`)*, **per nodo** *(`z_nodo`)* **o per arco** *(`z_arco`, `s` la media armonica)*;
  - **il mezzo Grover:** `nuovo_i = w · Somma_j v_j + z · v_i`, **`w = (1 - z)/d`** *(`d` il grado; la divisione e' in virgola mobile)*: **la matrice `z I + w J`, normale: valori propri `z + d w` e `z`;**
  - **il mezzo spostamento:** `[[alpha, beta], [beta, alpha]]`, **`alpha = (1 + z)/2`, `beta = (1 - z)/2`:** **valori propri `alpha + beta` e `alpha - beta`;**
  - **la fase del v2:** `conj(z)`, **modulo `|z|`.**
- ### **NON SO:** **se i pezzi di `psi` toccano `phi`** *(dal codice no; la misura lo dice: devono dare zero)*; **se il coefficiente `beta` di `materia_vuoto` a `rho = 0` e' zero esatto.**

### 24.2 LA MISURA *(D2.2-D2.5)*

- **La scena di T1, identica** *(il codice di `lambda_vuoto_deriva.py`: vuoto F3 di TBS, `81 x 81`, `mot.cs 0.15`, `lambda_c = None`, `1000` tick, dentro `SF.forma` e `BE.conv(DC.ZERO)`, che QUI non avvolge niente)*.
- **Gli strumenti, in memoria e solo per la corsa:** **ogni operatore di `mot.operatori` avvolto** *(il numero della posizione `1`-`14` nel tick)*; **dentro le posizioni `6`-`9` anche `FP._grover_mezzo` e `FP._hop_phi_mezzo`** *(i sotto-pezzi `a`, `b`; il `c` e' la differenza fra la fine dell'operatore e la fine di `b`)*.
- ### **CHE COSA SI MISURA, e perche' ESATTO:** **la deriva per tick e' `~2.2e-15` su `Lambda 6`, cioe' `~2.5` ulp: una misura in virgola mobile di `Lambda` dopo ogni pezzo avrebbe un errore dello stesso ordine, E UGUALE su tutti i nodi** *(il vuoto e' uniforme: l'errore di misura non si media)*. **Quindi:**
  - **`Lambda` ESATTO** *(somma di `re^2 + im^2` in `fractions.Fraction`, dai float di `phi`)* **su un campione di `9` nodi** *(gli indici `0`-`8`: una scelta dichiarata, non tarata; il periodo di F3 e' `3`, e la deriva di T1 e' uguale su tutti i nodi)*, **dopo ogni pezzo e sotto-pezzo;**
  - **accanto, la norma totale in virgola mobile** *(`np.sum(|phi|^2)` su tutti i nodi: solo stampata)*.
- **Per ogni pezzo** *(D2.2)*: **la variazione relativa media per tick** `<Delta Lambda / Lambda>` *(media sui `1000` tick e sui `9` nodi)*, **il segno, la frazione dei tick con variazione positiva;** **la dispersione fra i `9` nodi.**
- **D2.3, i coefficienti in virgola mobile, ESATTI:** **per ogni valore distinto di `z` nella scena** *(per nodo a `h`, per arco a `h`)*, **in `Fraction`:** **`|lambda|^2 - 1` per ogni valore proprio** *(la matrice e' normale: `||U^dagger U - I|| = max ||lambda|^2 - 1|`, `sigma_max - 1 = max |lambda| - 1`)*, **e `| |conj z| - 1 |`;** **e il fattore di `materia_vuoto`.**
- **D2.4 DEVE FALLIRE:** **una seconda corsa con `phi *= fl(1 + 1e-15)` subito dopo il pezzo in posizione `1`** *(`CAMM-MATERIA-VUOTO`, scelto PRIMA di vedere i numeri)*: **il controllo «la diagnosi NON indica la posizione `1` come la piu' pesante, con l'aumento atteso `|fl(1 + 1e-15)|^2 - 1` entro il `10%`» DEVE FALLIRE.**
- **D2.5, la chiusura:** **la somma dei contributi medi per tick** *(esatti, sul campione)* **contro la deriva di T1 per tick** *(letta dal referto a `81c690a8`: `2.228e-12 / 1000`)* **entro il `10%`;** **e accanto la deriva in virgola mobile di `densita_vuoto` di questa corsa.** ### ⚠ **Che cosa NON dice:** **la somma dei pezzi esatti e' telescopica sulla `Lambda` esatta** *(chiude per costruzione)*: **il confronto vero e' fra la `Lambda` ESATTA e quella di `densita_vuoto` di T1.**

### 24.3 LE LETTURE, SCRITTE PRIMA *(quelle di Luca, rese operative)*

- **Il peso di un pezzo = il suo contributo medio diviso la somma dei contributi.**
- **(p1)** **un pezzo pesa oltre il `90%` E il suo `sigma_max - 1 > 0` in D2.3:** **causa trovata;** **la proposta di correzione scritta, NON applicata.**
- **(p2)** **nessun pezzo oltre il `90%`:** **tutti quelli col peso, in ordine.**
- **(p3)** **un pezzo oltre il `90%` ma coi coefficienti non espansivi** *(`sigma_max - 1 <= 0`)*, **oppure D2.5 non chiude:** **la deriva sta nell'ARITMETICA dell'applicazione** *(l'ordine delle operazioni, le somme)*, **non nei coefficienti:** **lo scrivo e mi fermo con una proposta di diagnosi piu' fine.**
- ### **Ogni lettura dice anche:** **se il pezzo pesante e' la fase `conj(z)` del v2** *(i sotto-pezzi `c`)* **o un mezzo pezzo** *(`a`, `b`: comuni al principale, che li fa a `f` intera e non a `f/2`)*.
- **Il costo** *(stima)*: **`~3` minuti per corsa, due corse:** **`~6`-`8` minuti accanto a S162.**

### 24.4 TODO

1. **Questa sezione: commit e push** *(dopo D1-bis sul principale: un test breve alla volta)*.
2. **Lo script `csv/solitone/lambda_deriva_pezzi.py`; la suite in `wt_zero`; commit e push.**
3. **La corsa; il referto `doc/referti_l2/lambda_deriva_pezzi.txt`; l'esito in `24.5`; il rimando nella RELAZIONE del principale.**
4. **Poi FERMO:** **niente T2, T3, ne' correzioni senza la decisione di Luca.**

### 24.5 L'ESITO *(la corsa dalle `00:38:14` alle `00:42:10` del `2026-11-10`, a `cd10786c`, blob dello script `a6201067`; il referto `doc/referti_l2/lambda_deriva_pezzi.txt`)*

- **La scena di T1** *(`6561` nodi, `cs 0.15`, `Lambda 6`; i `9` nodi del campione di grado `6`)*; **il controllo positivo: `FP.grover` e `FP.hop_phi` sono quelli del modulo** *(nessun avvolgimento)*.
- **D2.2, per pezzo** *(`Delta Lambda / Lambda` esatto, media su `1000` tick e `9` nodi; i nodi tutti uguali, min = max)*:
  - **posizioni `1`, `2`, `3`, `4`, `5`, `10`-`14`: ZERO ESATTO in ogni tick e nodo** *(le due premesse NON SO della sez. `24.1`: i pezzi di `psi` non toccano `phi`; `beta` di `materia_vuoto` a `rho = 0` vale `0` e il fattore e' `1` esatto)*;
  - ### **i quattro MEZZI SPOSTAMENTI del vuoto:** **`7a` `+1.0420e-16`, `7b` `+1.0391e-16`, `8a` `+1.0166e-16`, `8b` `+1.0247e-16`** *(positivi nell'`88`-`90%` dei tick; i pesi `0.2807`, `0.2799`, `0.2738`, `0.2760`)*;
  - **i mezzi Grover** *(`6a` `-6.15e-18`, `6b` `-2.15e-18`, `9a` `-2.19e-18`, `9b` `-5.91e-18`)* **e le fasi `conj(z)` del v2** *(`6c` `-3.01e-18`, `7c` `-8.55e-18`, `8c` `-6.62e-18`, `9c` `-6.41e-18`)*: **piccoli, negativi, positivi in circa meta' dei tick** *(`0.46`-`0.50`)*.
- **D2.3, i coefficienti esatti** *(`h = 0.25`, un solo `z` per nodo e per arco: `0.993068 + 0.117537j`; grado `6`)*:
  - **mezzo Grover:** `|lambda|^2 - 1` = `-1.735e-18`, `-5.123e-18`; `sigma_max - 1 = -8.674e-19`;
  - ### **mezzo spostamento:** **`|alpha + beta|^2 - 1 = +1.110e-16`**, `|alpha - beta|^2 - 1 = +1.051e-16`; **`sigma_max - 1 = +5.551e-17`: ESPANSIVO;**
  - **le fasi `conj(z_arco)`, `conj(z_nodo)`:** `-5.123e-18`; **`materia_vuoto`:** il fattore `1` esatto.
- **D2.4** *(`fl(1 + 1e-15)` dopo la posizione `1`)* **FALLISCE COME DEVE:** **la piu' pesante e' la `1`, l'aumento `2.2453e-15` contro l'atteso `|fl(1+1e-15)|^2 - 1`** *(il rapporto `1.0112`)*.
- **D2.5 PASSA:** **la somma dei contributi esatti, per tick, `+2.2276e-15`** *(relativa `+3.7126e-16`, per `Lambda 6`)* **contro T1 `+2.2280e-15`** *(il rapporto `0.999799`: l'arrotondamento del referto di T1)*; **la deriva in float di `densita_vuoto` di questa corsa: `+2.2276e-15`.**
- ### **LA LETTURA, COME SCRITTA PRIMA (per etichetta): (p2)** — **nessuna etichetta oltre il `90%`:** **`7a` `0.2807`, `7b` `0.2799`, `8b` `0.2760`, `8a` `0.2738`;** **poi `7c` `-0.0230`, `8c` `-0.0178`, `9c` `-0.0173`, `6a` `-0.0166`, `9b` `-0.0159`.**
- ### **PER TIPO** *(informazione, non decide: dichiarato prima nella docstring)*: **le quattro etichette pesanti sono LO STESSO COEFFICIENTE, il mezzo spostamento del vuoto: peso `1.1104`, `sigma_max - 1 = +5.551e-17 > 0`.** **Se il pezzo si conta per tipo, e' la forma di (p1).** **Gli altri tipi pesano meno di zero** *(`-0.044` il Grover, `-0.041` e `-0.025` le due fasi del v2)*.
- ### **La sospettata del guardiano NON e' lei:** **la fase `e^{-i theta/2}` del v2 ha `|z|^2 - 1 = -5.1e-18` e pesa meno di zero;** **il `1/d` del Grover ha `sigma_max - 1 < 0`.** **La deriva e' nel mezzo spostamento, che non e' del v2** *(il principale lo fa a `f` intera, una volta per pezzo)*.

### 24.6 LA LETTURA DEL MECCANISMO *(dal codice; un'ipotesi da verificare, NON una misura)*

- **`_alfa_beta`:** **`beta = fl((1 - z)/2)`, `alpha = fl((1 + z)/2)`.** **`1 - z_re` e' ESATTO** *(Sterbenz: `z_re` in `[0.5, 2]`)*; **`1 + z_re` NO** *(in `[1, 2)` l'ulp e' `2^-52`)*. **Quindi `alpha + beta = 1 + delta` con `delta` l'arrotondamento di `1 + z_re`, e la parte immaginaria si cancella esatta:** **`|alpha + beta|^2 - 1 ~ 2 delta`.**
- **Il vuoto F3, sui due lati di un arco, e' quasi tutto nella combinazione SIMMETRICA** *(da verificare)*: **ogni mezzo spostamento lo allunga di `~|alpha + beta|^2 - 1 = 1.110e-16`** *(misurato `~1.04e-16`: compatibile con una piccola parte antisimmetrica)*.
- ### **IL SEGNO DIPENDE DA `z`:** **cioe' da come si arrotonda `1 + cos(pi s f)`.** **Sul principale lo spostamento gira a `f` intera** *(un altro `z`)*, **e D1-bis ha dato il segno OPPOSTO:** **COMPATIBILE con questo meccanismo, NON verificato.**
- **E l'avvolgimento in memoria del principale** *(D1)* **fa gli stessi mezzi pezzi del laterale:** **per questo la deriva e' la stessa.**

### 24.7 LE PROPOSTE, A LUCA *(NON applicate: il nucleo e' condiviso, e quello del principale e' congelato)*

1. **(D2-bis, una verifica di poco costo)** **D2.3 sul `z` del principale** *(`f` intera)*: **se `|alpha + beta|^2 - 1 < 0` li', il segno di D1-bis e' spiegato; e la stessa misura per pezzi sul principale senza avvolgimento.**
2. **(la correzione possibile, una scelta di Luca)** **lo spostamento scritto come `I - beta (I - S)`:** `nuovo_0 = v0 - beta (v0 - v1)`, `nuovo_1 = v1 - beta (v1 - v0)`. **Sulla combinazione simmetrica `v0 - v1 = 0` esatto, quindi il valore proprio `1` e' ESATTO** *(e' la forma `I + (e^{i theta} - 1) P-` del commento di `_alfa_beta`)*. ### ⚠ **Il prezzo, scritto:** **a `theta = pi` (`beta = 1`) `v0 - (v0 - v1)` NON e' `v1` al bit**, **e `M-B1`** *(l'identita' al bit col vecchio spostamento)* **cadrebbe.** **Le alternative ne hanno altri** *(`alpha = 1 - beta`: il commento di `_alfa_beta` lo vieta, col suo motivo)*. **La scelta della forma e' di Luca;** **qualunque forma tocca `primo_ordine/flussi_parziali.py` su tutti e due i rami.**
- ### **FERMO** *(il mandato)*: **ne' T2, ne' T3, ne' correzioni senza la decisione di Luca.**

## 25. T2, LA CARTA F1 ALLUNGATA *(Luca `2026-11-09` `20:13`, ripartito `2026-11-10` `01:22`)*: **IL PROGETTO, PRIMA DEL CODICE**

### 25.0 DA DOVE PARTE

- **La deriva di `Lambda` del vuoto e' spiegata** *(D2, sez. `24.5`: i quattro mezzi spostamenti, `+3.7e-16` relativo per tick)*: **un arrotondamento del tick, non di F1.** **La correzione dello spostamento e' RIMANDATA all'unificazione** *(Luca)*: **non si anticipa.**
- ### **F1-V NON E' PIU' UN CANCELLO: E' UNA LETTURA** *(il criterio di Luca)*: **«`cs` nel vuoto non deriva piu' di quanto il rilassamento esatto gli impone dalla deriva di `Lambda`».**
  - **La deriva attesa:** **`dcs/dLambda = Lambda_c/(Lambda + Lambda_c)^2`** *(`34/(Lambda + 34)^2`)* **per la deriva MISURATA di `Lambda` nella stessa corsa;**
  - **F1-V passa se la deriva media di `cs` sta entro un fattore `2` da quella attesa;** **ai tick `50`, `1000` e alla fine.**
- **D2-bis del principale e' su origin** *(`126eb630`)*.

### 25.1 LE PREMESSE DAL CODICE

- **Lo script nuovo `csv/solitone/carta_f1_lunga.py`, dalla `carta_f1.py`** *(blob `b0b5deb1`: il rilassamento esatto `cs + r (L - cs)`, `r = 1 - e^{-omega_v}`, (q2))*. **`carta_f1.py` resta com'e'** *(si rigira al suo commit)*.
- **Le modifiche, dichiarate:**
  1. **`5000` tick** *(il mandato)*; **il tetto dei `60` minuti:** **dopo i primi `100` tick della prima corsa, i secondi per tick per `4` corse da `5000`** *(il vuoto, la base, `1e-8`, `1e-10`)*: **se la proiezione supera `3600` s, TUTTE le corse a `3000`, dichiarato nel referto;**
  2. **due ampiezze sul centro, `1e-8` e `1e-10`, in corse separate, contro la stessa corsa base** *(la base tiene `cs` di ogni tick in memoria: `5000 x 6561` float, `~262` MB, stima)*;
  3. **ogni `100` tick:** **la differenza `max|cs_pert - cs_base|`; `cs` min e il RAGGIO del suo nodo** *(dal centro di `rho` dello stato di partenza, `toro.centro`)*; **`r` max; la norma; il calore della memoria;**
  4. **il tasso di crescita** *(stima di Lyapunov)*: **la pendenza di `ln(differenza)` sui tick, dal tick `1` al primo con la differenza oltre `1e-4`** *(la soglia di «e oltre, se stabile» della sez. `21`: la stessa, non scelta ora)*, **per ciascuna ampiezza;**
  5. **F1-V: il vuoto F3 da solo, (q2), fino alla fine;** **la lettura col criterio di Luca ai tick `50`, `1000` e alla fine;**
  6. **F1-I e F1-F restano** *(l'aritmetica dell'inversa)*; **il vecchio F1-V «AL BIT» non c'e' piu'.**

### 25.2 LE LETTURE, SCRITTE PRIMA *(di Luca; i criteri numerici miei, dichiarati)*

- **«l'ultimo terzo» = i campioni ogni `100` tick nell'ultimo terzo della corsa.**
- **(s1)** **la differenza si STABILIZZA:** **la pendenza di `log10(differenza)` nell'ultimo terzo sotto `0.1` decadi per `1000` tick in valore assoluto, E i livelli delle due ampiezze** *(la media geometrica dell'ultimo terzo)* **entro un fattore `2`:** **caotica ma limitata.**
- **(s2)** **la differenza continua a CRESCERE:** **la pendenza `>= 0.1` decadi per `1000` tick:** **instabilita' vera.**
  - **Se la pendenza e' sotto `0.1` ma i livelli differiscono oltre un fattore `2`:** **lo scrivo cosi', fra (s1) e (s2).**
- **(s3)** **`cs` min `<= 0`, oppure il dominio o `Omega` cedono** *(un'eccezione: `s <= 0`)*: **FERMO SUBITO;** **il tick, il raggio, `Lambda` locale:** **il muro `cs = 0`.**
- **(s4)** **la discesa di `cs` min** *(`0.0012` a `200`, `0.0003` a `1000`)*: **si ARRESTA se la pendenza di `ln(cs min)` nell'ultimo terzo e' sotto `0.05` per `1000` tick in valore assoluto;** **allora il tick in cui `cs` min entra per la prima volta entro il `5%` del suo minimo;** **altrimenti la pendenza.**
- **F1-V, come lettura:** **«entro un fattore `2`» o «fuori», ai tre tick.**

### 25.3 TODO

1. **Questa sezione, commit e push.**
2. **Lo script; la suite in `wt_zero`; commit e push.**
3. **La corsa** *(stima `~48` minuti, in background)*; **il referto `doc/referti_l2/carta_f1_lunga.txt`; l'esito in `25.4`; il rimando nella RELAZIONE del principale.**
4. **Poi T3** *(sez. `26`)*; **dopo T3 FERMO.**

## 26. T3, IL TEMPO DI MEMORIA `tau_Lambda` *(Luca `2026-11-09` `20:13`, ripartito `2026-11-10` `01:22`)*: **IL PROGETTO, PRIMA DEL CODICE**

### 26.1 IL PASSO DELLE MAPPE, CONTROLLATO PRIMA *(il mandato)*

- **`csv/solitone/mappe.py`: `OGNI = 100`** *(un'istantanea ogni `100` tick, `15` unita')*.
- **`1/omega` del vuoto F3 a `s 0.15`:** **`omega_v = 0.471` per tick** *(IS2)*, **cioe' `1/omega ~ 2` tick.**
- ### **Il passo delle mappe e' ~`50` volte `1/omega`: la `tau_int` di Sokal dalle mappe NON VALE** *(lo dichiaro, come chiede il mandato)*. **Al posto suo: il rilassamento di `Lambda` dopo un disturbo imposto.**
  - **Vicino al solitone `omega` cambia** *(in F1 `r` va da `~1e-4` a `0.81`)*: **la misura lo stampa per nodo.**

### 26.2 LA MISURA *(una corsa corta, il nucleo del laterale, `cs` SPENTO)*

- **Lo stato: `TBS` a `10000` tick dalla libreria** *(lo stesso di F1 e di (r-D5))*; **`mot.lambda_c = None`, `mot.cs` quello dello stato.**
- **Il centro: `toro.centro` di `rho`** *(come in F1)*. **Tre nodi, scelti PRIMA:** **il nodo piu' vicino al raggio `0` (centro), `17` (il guscio di (r-D5), `16`-`18`), `25` (il vuoto, dentro il bordo di `TBS`, `R_A 28`)**, **lungo la direzione `+x` dal centro.**
- **Il disturbo:** **`Lambda` del nodo scalato di `1 + 1e-6`** *(la `phi` delle sue estremita' per `sqrt(1 + 1e-6)`: `Lambda` e' quadratica nelle fasi)*, **al tick `0`.** **Quattro corse:** **la base, e una per nodo disturbato.** **`1000` tick ciascuna** *(stima `~10` minuti in tutto)*.
- **Per ogni nodo disturbato:**
  - **`DeltaLambda(t)` sul nodo** *(disturbata meno base)*, **relativo al disturbo iniziale;**
  - ### **`tau_Lambda` = il primo tick con `|DeltaLambda(t)| <= e^{-1} |DeltaLambda(0)|`** *(se non arriva entro `1000`: «oltre `1000`»)*;
  - **`omega_v` del nodo** *(dal primo tick della base, la funzione di `carta_f1`)* **e `1/omega`;** **il rapporto `tau_Lambda / (1/omega)`.**
- ### **IL CONTROLLO DI SCALA:** **(T3-P) DEVE PASSARE:** **la base contro se stessa da' `DeltaLambda = 0` esatto** *(la misura non inventa un rilassamento)*; **(T3-F) DEVE FALLIRE:** **«il disturbo NON si vede»** *(`|DeltaLambda(0)| / Lambda` del nodo sotto `1e-9`, per ognuno dei tre nodi)*.

### 26.3 LE LETTURE *(le mie della sez. `22`, gia' scritte)*

- **(t1)** **`tau_Lambda` molto piu' lungo di `1/omega`** *(il rapporto oltre `10`, mio, dichiarato)*: **un tempo di memoria lento esiste: F1 con quel `r`** *(NON applicata: la scelta e' di Luca)*.
- **(t2)** **`tau_Lambda ~ 1/omega`** *(il rapporto entro `10`)*: **il tempo di memoria lento non c'e' nella dinamica: F1 da sola non basta** *(F2 o F4: la scelta e' di Luca)*.
- **La lettura per ognuno dei tre nodi** *(il profilo radiale)*.

### 26.4 TODO

1. **Questa sezione, commit e push** *(durante T2: non tocca il suo percorso)*.
2. **Lo script `csv/solitone/tau_lambda.py`; la suite in `wt_zero` DOPO T2; commit e push.**
3. **La corsa; il referto `doc/referti_l2/tau_lambda.txt`; l'esito in `26.5`; il rimando nella RELAZIONE.**
4. **Poi FERMO** *(il mandato)*: **niente F2, F3, F4, niente `tau_Lambda` dentro F1.**

### 25.4 L'ESITO DI T2 *(la corsa dalle `02:33:59` alle `03:29:22` del `2026-11-10`, a `2d996ae0`, blob `f77f58f5`; il referto `doc/referti_l2/carta_f1_lunga.txt`)*

- **Il costo:** **`0.1541` s per tick sui primi `100` del vuoto; la proiezione `3083` s: sotto il tetto, `5000` tick.** **Le tre corse: `824`, `818`, `815` s; `3321` s in tutto.**
- **F1-I passa** *(`6.08e-15`)*; **F1-F fallisce come deve** *(`5.20e+00`)*.
- ### **F1-V, LA LETTURA COL CRITERIO DI LUCA** *(`dcs/dLambda = 2.125e-02`)*: **ENTRO UN FATTORE `2` a tutti e tre i tick:**
  - **tick `50`:** la deriva di `Lambda` `+2.8422e-14`; di `cs` misurata `+6.6613e-16`, attesa `+6.0396e-16`; il rapporto `1.1029`;
  - **tick `1000`:** `+4.1744e-14`; `+7.4940e-16` contro `+8.8707e-16`; `0.8448`;
  - **tick `5000`:** `+2.2204e-14`; `+6.6613e-16` contro `+4.7184e-16`; `1.4118`.
  - ### **Un fatto da notare, non una lettura:** **con F1 acceso la deriva di `Lambda` del vuoto NON e' lineare e resta `~1e-14`** *(`+4.2e-14` a `1000`, `+2.2e-14` a `5000`)*; **a `cs` spento T1 dava `+2.228e-12` a `1000`.**
- **La base** *(`TBS` a `10000`, (q2))*, **ai tick `100`, `200`, `500`, `1000`, `2000`, `3000`, `4000`, `5000`:**
  - **`cs` min:** `0.001942`, `0.001212`, `0.000485`, `0.000301`, `0.000141`, `0.000109`, `0.000094`, `0.000065` *(il minimo su tutti i campioni `0.000060`)*;
  - **il raggio del nodo di `cs` min:** `26.28`, `26.13`, `37.71`, `39.04`, `29.19`, `35.77`, `35.77`, `38.91` ### *(vicino o OLTRE il bordo di `TBS`, `R_A 28`: non al centro)*;
  - **`r` max:** da `0.7771` a `0.8618`; **la norma:** da `996944.862393052084` a `996944.862393003423`; **il calore della memoria:** da `-3.098200e+04` a `-7.271386e+03`.
- **La differenza perturbata/base** *(`max|cs_pert - cs_base|`)*:
  - **`1e-8`:** `4.444e-06` (100), `6.302e-05` (200), `3.008e-02` (500), `5.369e-02` (1000), `2.372e-01` (2000), `2.631e-01` (3000), `2.689e-01` (4000), `2.716e-01` (5000);
  - **`1e-10`:** `4.444e-08`, `6.300e-07`, `6.862e-04`, `3.303e-02`, `2.424e-02`, `5.620e-02`, `2.233e-01`, `2.399e-01`.
- **Il tasso di crescita** *(stima di Lyapunov, fino alla differenza `1e-4`)*: **`1e-8`: `0.04554` per tick** *(il fattore `1.04659`, dal tick `1` al `204`)*; **`1e-10`: `0.04711`** *(`1.04823`, dal `1` al `279`)*.
- **L'ultimo terzo:** **`1e-8`: il livello `2.699e-01`, la pendenza `+0.0055` decadi per `1000` tick;** **`1e-10`: `2.157e-01`, `+0.0982`.**
- ### **LA LETTURA: (s1)** — **si stabilizza sullo stesso livello per le due ampiezze** *(il rapporto `1.251`)*: **caotica ma limitata.** ### ⚠ **AL MARGINE:** **la pendenza di `1e-10` (`0.0982`) sta appena sotto la soglia `0.1`** *(la sua differenza sale ancora fra `3000` e `4000`)*.
- ### **LA LETTURA: (s4)** — **la discesa di `cs` min CONTINUA:** **la pendenza di `ln(cs min)` nell'ultimo terzo `-0.3998` per `1000` tick** *(il minimo `0.000060`)*. **Nessun muro (s3) in `5000` tick.**

### 26.5 L'ESITO DI T3 *(la corsa dalle `04:02:58` alle `04:09:27` del `2026-11-10`, a `46e4ba95`, blob `7102b17c`; il referto `doc/referti_l2/tau_lambda.txt`)*

- **Il passo delle mappe:** **`OGNI = 100` tick; `omega_v` del vuoto** *(la mediana oltre il raggio `30`)* **`0.471235` per tick, `1/omega` `2.122` tick: il passo e' `47.1` volte `1/omega`.** **La `tau_int` dalle mappe non vale** *(come dichiarato nella sez. `26.1`)*.
- **T3-P passa** *(la base contro se stessa: `0` esatto)*; **T3-F fallisce come deve sui tre nodi** *(il disturbo si vede: `1.000e-06`)*.
- **I tre nodi** *(lungo `+x` dal centro di `rho`)*:

| raggio | nodo | `Lambda` | `omega_v` per tick | `1/omega` | `DeltaLambda / DeltaLambda(0)` ai tick `1`, `2`, `5`, `10`, `50`, `100`, `1000` | `tau_Lambda` | il rapporto |
|---|---|---|---|---|---|---|---|
| `0` | `3362` | `5.425885` | `0.739647` | `1.352` | `+0.947` `+0.811` `+0.256` `+0.407` `+0.442` `+0.009` `+0.807` | `5` | `3.698` |
| `17` | `4739` | `2.061094` | `0.310652` | `3.219` | `+0.950` `+0.808` `+0.269` `+0.406` `+0.488` `+1.089` `+0.875` | `5` | `1.553` |
| `25` | `5387` | `6.040594` | `0.470457` | `2.126` | `+0.945` `+0.797` `+0.218` `+0.388` `+0.421` `+0.012` `+0.788` | `5` | `2.352` |

- ### **LA LETTURA COL CRITERIO SCRITTO: (t2) sui tre nodi** *(`tau_Lambda` entro `10` volte `1/omega`)*.
- ### ⚠ **MA LA PREMESSA DEL RILASSAMENTO CADE** *(i numeri della tabella)*: **`DeltaLambda` sul nodo NON DECADE.** **Scende sotto `e^{-1}` al tick `5`, risale a `~0.4` al tick `10`, passa vicino a `0` al tick `100` e torna a `0.79`-`0.88` al tick `1000`** *(al raggio `17` e' `1.089` al tick `100`)*. **Il tick e' unitario, e il disturbo di `Lambda` non si dissipa: si allontana e torna** *(un'onda sul toro: stima, non misurata)*. ### **Quindi `tau_Lambda = 5` e' il primo passaggio sotto `e^{-1}`, NON un tempo di memoria:** **un tempo di rilassamento di `Lambda`, in questa dinamica, non c'e'.**
- **Cio' va nella stessa direzione di (t2)** *(«il tempo di memoria lento non c'e' nella dinamica»)*, **ma per un motivo diverso da quello scritto: non «veloce», bensi' «assente».**
- ### **FERMO** *(il mandato: dopo T3)*. **Niente F2, F3, F4, niente `tau_Lambda` dentro F1.** **Le domande a Luca:**
  1. **con (t2) e la premessa caduta:** **F1 resta col `r` del battito** *(T2: (s1) al margine, (s4) `cs` min che scende ancora)*, **oppure F2 o F4?**
  2. **(s4):** **`cs` min scende ai raggi `26`-`39`, vicino o oltre il bordo di `TBS`:** **guardare li' prima di scegliere?**


## 27. B1, LA DISCESA DI `cs` MIN E' DEL BORDO? *(Luca `2026-11-10` `08:42`)*: **B1.0, LE PREMESSE DAL CODICE, PRIMA DELLA MISURA**

### 27.1 COME AGISCE IL BORDO DI `TBS` *(letto dal codice, `wt_zero` a `05f77182`)*

- **E' un'operazione FUORI dal nucleo, DOPO ogni tick** *(`csv/solitone/bordo.py`, la docstring; chiamata da `corsa_accensione.corsa`: `AC.tick(z, t, K)`, poi `BO.assorbi(z["st"], gfa[0], rif)`)*.
- **Dove:** i nodi a distanza periodica `R >= R_A` dal centro `bor["c0"]` *(`campo.anelli`: la distanza in indici, `|a A1 + b A2|`, l'immagine piu' vicina fra le `9`)*. **Per `TBS`:** `R_A = 28` *(`BO.R_A`; `TBS` non e' in `BORDO_CORSA`)*, `g_max = 0.03` *(`BORDO["TBS"] = BORDO["TB3"]`)*, `R_B = 40.5` *(la meta' del periodo, `TO.meta_periodo(81)`)*.
- **Il profilo:** `g(R) = g_max sin^2(pi/2 (R - R_A)/(R_B - R_A))` fra `R_A` e `R_B`, `g_max` oltre *(i nodi negli angoli del rombo, fino a `L/sqrt 3 ~ 46.8`)*. **`g` per estremita' e' quello del suo nodo.**
- **Che cosa toglie:** `psi -> psi (1 - g)`; `phi -> phi0 + (phi - phi0)(1 - g)` con `phi0 = c(t) F3` *(il vuoto di riferimento che gira, `c_di(t, tab_c, K, omega)`, `omega = 3 pi/20`)*. **Toglie le onde del vuoto attorno a `phi0`, non il vuoto:** se `phi = phi0` sulla fascia, il bordo non fa niente su `phi`.
- **`cs` ne dipende?** **Solo per la via di `phi`:** `cs` di F1 rilassa verso `L = FP.cs(Lambda, Lambda_c)`, e `Lambda = mot.densita_vuoto(st)` si legge da `phi`. **Il bordo non tocca `cs` direttamente.**
- **Il centro del bordo rispetto al centro di `rho`:** `bor["c0"] = (40.5, 40.5)` *(il centro periodico del campione `0` di `TBS`)*; **a `10000` tick il centro di `rho` e' `(40.50359, 40.50231)`, lo spostamento `X = (0.00243, 0.00200)`** *(dal jsonl di `TBS`, pezzo `0`-`10000`, letto con `CA.serie("TBS")`)*. **I raggi di T2** *(dal centro di `rho` a `10000`, `TO.scarti` + `hypot`, la stessa metrica)* **coincidono con quelli del bordo entro ~`0.004`.**
- **Fino a `10000` il bordo di `TBS` ha tolto `M 3.055e+03`, `V 1.456e+03`** *(lo stesso jsonl)*.

### 27.2 ⚠ **LA PREMESSA DEL MANDATO CADE: T2 GIRAVA COL BORDO SPENTO**

- **`carta_f1_lunga.corsa`** *(e `carta_f1.corsa`, e `tau_lambda.py`)* **chiamano SOLO `TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))`.** **Nessuno dei tre chiama `BO.assorbi`, ne' importa `bordo`** *(grep di `assorbi`, `bordo`, `BO.`, `g_estremita` nei quattro file: zero righe)*. **Il referto di T2 non nomina il bordo.**
- ### **Quindi la base di T2 e' gia' il toro `81 x 81` PURO:** **lo stato di `TBS` a `10000`** *(nato COL bordo, `10000` tick di assorbimento)* **lasciato andare SENZA il bordo, `5000` tick.** **E' la corsa che il mandato chiama (b1), non (b0).**
- **E la discesa di `cs` min c'e' col bordo spento:** **T2 base** *(il referto, la tabella della base)*: **tick `50` `0.004596` al raggio `19.22`; `100` `0.001942` a `26.28`; `1000` `0.000301` a `39.04`; `3000` `0.000109` a `35.77`; `5000` `0.000065` a `38.91`;** **la pendenza di `ln(cs min)` nell'ultimo terzo `-0.3998` per `1000` tick.**
- **Cosa NON si puo' piu' leggere com'era scritto:**
  - **B1.1 (b0)** *(«lo script nuovo, col bordo ACCESO, ridà al bit `cs` min di T2»)*: **fallirebbe per costruzione**, perche' T2 non aveva il bordo.
  - **(c1)/(c2)** sono formulate su (b1) = bordo spento, **cioe' su T2 stessa**: **(c1) e' gia' esclusa da T2** *(`cs` min `6.0e-5`, sotto `1e-3`; pendenza `-0.40`)*, **ma (c2) chiede la discesa DENTRO `r < R_A`, e T2 non separa le zone.**
- **Cosa resta aperto, ed e' l'ipotesi del bordo in un'altra forma:** **la STORIA del bordo.** **Lo stato a `10000` porta `10000` tick di assorbimento sulla fascia `R >= 28`:** **togliendo il bordo, la fascia puo' rilassare da quello stato, e la discesa puo' essere quel rilassamento** *(ipotesi mia, non misurata)*.

### 27.3 **FERMO SU B1: IL DISEGNO E' DI LUCA** *(nessuna corsa, nessuno script)*

**Le mie proposte, con la raccomandazione** *(la scelta e' di Luca)*:

1. **(raccomandata) Rovesciare i ruoli, senza cambiare la domanda:** **(b0) = T2 com'e'** *(bordo spento; il controllo positivo: lo script nuovo ridà al bit `cs` min e il raggio di T2 ai tick `100` e `1000`)*; **(b1) = la stessa corsa col bordo ACCESO** *(`BO.assorbi` dopo ogni tick, `c0 (40.5, 40.5)`, `R_A 28`, `g_max 0.03`, `phi0 = c(10000 + k) F3`)*, **5000 tick, il tetto di 60 minuti;** **B1.4 per entrambe** *(rifacendo (b0), che costa ~`824` s)*. **Le letture andrebbero riscritte per Luca:** il criterio di (c1) diventerebbe *«col bordo acceso la discesa e' piu' rapida, e il nodo di `cs` min sta in `R >= R_A`»*. ### ⚠ **Un controllo in piu' che serve:** **con F1 acceso, `phi0 = c(t) F3` e' ancora il vuoto giusto sulla fascia?** **F1-V di T2 dice che il vuoto F3 sotto F1 deriva in `Lambda` di `~1e-14`, ma la FASE `c(t)` non e' stata controllata sotto F1:** **un C0 breve sotto F1 prima di (b1)** *(come `CA.c0_breve`)*.
2. **(complementare) La storia senza bordo:** **`TS`** *(la stessa partenza, MAI assorbita: `STIMA["TBS"] = "TS"`)* **NON ha stati su disco** *(`CA.serie("TS")`: nessuno; `STATI` non ha `TS`)*. **`TBS` ha lo stato a `t 0`** *(`TBS_stato_000000.npz`, PRIMA di ogni assorbimento)*: **sotto F1 col bordo spento, `5000` tick, e' una partenza mai assorbita**, ma **non e' lo stesso istante** *(la materia a `t 0` non ha i `10000` tick di dinamica)*. **Lo stato di `TS` a `10000` vorrebbe una corsa di `TS` da rifare** *(costo non stimato)*. **Se la discesa c'e' anche partendo da `t 0`, la storia del bordo non basta a spiegarla.**
3. **b2** *(`L 162`)*: **resta com'e' scritta**, ma **col bordo acceso o spento va detto**: con la premessa caduta, **non e' piu' «un'altra via per (c1)»**.

**Il criterio di chiusura della domanda:** **la decisione di Luca su 1-3** *(o un disegno suo)*.


### 27.4 B1.0-bis *(Luca `2026-11-10` `13:42`)*: **B1 RIDISEGNATO, PRIMA DEL CODICE**

**La decisione di Luca:** **la corsa col bordo acceso (la proposta 1 della sez. `27.3`) NON si fa.** **Tre ipotesi, una per corsa:** **H1** la storia del bordo; **H2** il toro finito *(l'antipodo a `40.5`)*; **H3** il colpo dell'accensione di F1. **L'ordine: (i), (iv), (ii), (iii).** **F1 come in T2** *(il rilassamento esatto, (q2); F1-V come lettura)*; **nessuna modifica al nucleo; vuoto F3.**

#### 27.4.1 LE VELOCITA' CON CUI CONFRONTARE UN FRONTE *(in nodi per tick, con la provenienza)*

| | la velocita' | la provenienza |
|---|---|---|
| **il cono del tick** | **`1` nodo per tick** *(dal codice; MISURATO dallo script (i): il supporto della risposta a un impulso dopo un tick)* | **`composizione.ORDINE`, 14 posizioni:** **`psi` salta in `4` e `9`** *(`hop_psi`: `alpha I + beta S_U` sull'arco, due mezzi sugli STESSI archi)* **e fra `4` e `9` nessun pezzo rimescola `psi` sul nodo** *(`5`-`8` sono del vuoto)*: **netto, un arco;** **`phi` salta in `6` e `7`, consecutivi, sugli stessi archi:** un arco; **materia e vuoto si scambiano solo in `0` e `13`** *(i flussi, sul posto)*: **nessun cammino fa due archi in un tick.** |
| **`v_max` della materia** | **`0.08819` nodi per tick** *(`0.58795` per unita' di tempo `x` `s 0.15`)* | **`doc/referti_l2/bordo_riflessione.txt`** *(`carta_bordo.py`, la scena di `TB3`, `cs` SPENTO, il tick congelato di `DV.matrice`)*: **`|v_g|` piu' grande della banda `B`, `0.58795`.** *(Coincide con `v_max/s` di P1/T5, `0.588137` a `s 0.15`, `eps 0.5`, sul principale.)* ### ⚠ **E' a `cs` spento e sulle sole bande `B`:** **la materia sotto F1 nel vuoto** *(dove `cs = s` al bit, F1-V)* **la MISURA lo script (i)** *(sotto)*. |
| **la velocita' di gruppo piu' grande del vuoto F3** | **non c'e' nel repo:** **la MISURA lo script (i)** | **Il metodo, fissato qui:** **la risposta lineare del tick INTERO** *(F1, (q2), `cs` = quello del vuoto)* **attorno a `psi = 0`, `phi = F3`:** **`R_c(x) = (tick(stato + a e_c) - tick(stato)) / a`** per ognuna delle `18` componenti del nodo `0` *(`12` di `psi`, `6` di `phi`)*, `a = 1e-6`; **`A(k) = sum_x R(x) e^{-i k.d(x)}`** *(`d(x)` lo scarto cartesiano dal nodo `0`, l'immagine piu' vicina)*; **`omega_n(k) = -arg lambda_n`**, **`v_n = d omega_n / dk` per Hellmann-Feynman** *(`dlambda = <u_n| dA |v_n> / <u_n|v_n>`, coi vettori sinistri e destri: niente differenze finite, niente salti fra bande)*. **Il massimo di `|v_n|`, separato per le bande di `psi` e di `phi`.** **I controlli:** **la linearita'** *(`R(2a)/2` e `R(i a)/i` contro `R(a)`, stampati)*; **il cono** *(la distanza piu' grande con `R != 0`)*; **`A(k)` unitaria** *(`|lambda| = 1`, stampato)*. **Se la risposta NON e' lineare in senso complesso** *(oltre `1e-6` relativo)*: **la velocita' del vuoto non si legge da `A(k)`, lo si scrive, e il confronto (f1) si fa con le altre due.** |

#### 27.4.2 IL PROFILO E IL FRONTE *(per le quattro corse; le mie scelte, dichiarate)*

- **Gli anelli:** **`campo.anelli` dal centro di `rho` allo stato di partenza** *(`TO.centro`, come T2; il centro resta fisso nella corsa)*; **l'anello `k = floor(r)`.** **Ogni `50` tick, per ogni anello:** **`cs` min, `cs` medio, `Lambda` medio** *(stampati per intero)*; **e `cs` min col suo raggio** *(il raggio di T2: `hypot` di `TO.scarti`; lo script stampa lo scarto massimo fra le due metriche)*.
- ### **IL RAGGIO DEL FRONTE `r_f(t)`:** **l'anello col `cs` MEDIO piu' basso** *(il profilo medio: il minimo globale salta fra nodi, T2 lo mostra; stampato accanto anche l'anello del minimo globale)*.
- ### **IL TRATTO IN MOTO:** **dal primo campione** *(tick `50`)* **al primo campione in cui `r_f` tocca il suo massimo della corsa;** **un fit lineare `r_f(t)`** sul tratto: **`v_f`**, **l'errore** *(l'errore standard della pendenza, dai residui)*, **il RMS dei residui**, **il passo all'indietro piu' grande** *(in anelli)*.
- ### **LE LETTURE (f1)/(f2)** *(Luca; le soglie in anelli sono mie: `1` anello e' la risoluzione del profilo)*:
  - **(f1) c'e' un fronte:** **il tratto ha almeno `3` campioni, il RMS dei residui `<= 1` anello, nessun passo all'indietro `> 1` anello, e `v_f` entro il `20%` di una delle velocita' di 27.4.1** *(si dice di quale)*;
  - **(f2) niente fronte:** **il tratto ha meno di `3` campioni** *(il minimo non viaggia)*, **oppure il RMS `> 2` anelli, oppure un passo all'indietro `> 2` anelli** *(salti)*;
  - **in mezzo** *(continuo ma `v_f` lontana da tutte, o RMS fra `1` e `2`)*: **caso intermedio, scritto cosi'.**
- **La pendenza di `ln(cs min)` nell'ultimo terzo:** **la definizione di T2** *(`carta_f1_lunga.pendenza` sui campioni ai multipli di `100` oltre i due terzi)*.

#### 27.4.3 LE QUATTRO CORSE *(un solo script, `csv/solitone/b1_profilo.py --corsa i|iv|ii`; (iii) dopo, col suo controllo del raccordo)*

- **(i) b0, T2 rifatto col profilo:** **lo stato di `TBS` a `10000`, F1, `5000` tick** *(il tetto di 60 minuti come in T2)*; **prima, il vuoto F3 da solo `5000` tick per F1-V** *(come T2)*.
  - **DEVE PASSARE (i-B):** **il ciclo nuovo ridà AL BIT, ai tick `100` e `1000`, l'array `cs` INTERO di `carta_f1_lunga.corsa`** *(il codice di T2, importato, girato `1000` tick sulla stessa partenza)*, **e le stringhe di `cs` min e del raggio uguali a quelle del referto di T2** *(`%.6f`, `%.2f`)*.
  - **DEVE FALLIRE (i-F):** **`cs` disturbato di `1e-12` sul nodo del centro al tick `0`:** **lo stesso controllo al tick `1000` deve dire di no.**
  - **Il fronte, (f1)/(f2).**
- **(iv) F1 acceso piano (H3):** **il valore verso cui F1 rilassa, `L~_k = s + lambda_k (L - s)`, `lambda_k = sin^2(pi k / (2K))`, `K = 1000`;** **per `k >= K` si usa `L` STESSO** *(F1 pieno: non `s + 1·(L - s)`, che puo' differire di un ulp)*. **`cs` al tick `1` e' `L~_1` dello stato di partenza; dopo il tick `k`, `cs <- cs + r (L~_{k+1} - cs)`.** `5000` tick, lo stesso profilo.
  - ### ⚠ **IL DEVE DI LUCA «con `K = 1` ridà (i)» sarebbe un FALSO-UNO** se confrontato con (i): **a `K = 1` il ciclo E' quello di (i), lo stesso codice.** **Quindi (iv-B) confronta `K = 1` col codice di T2** *(`carta_f1_lunga.corsa`, `1000` tick, AL BIT ai tick `100` e `1000`)*: **e' il controllo indipendente.** **E un controllo che la rampa agisca:** **a `K = 1000`, `max|cs - s|` al tick `1` stampato** *(deve essere `lambda_1 = sin^2(pi / 2000)` volte quello di (i), entro l'arrotondamento: stampato)*.
  - **Le letture (q1)/(q2) di Luca** *(la pendenza di (i) letta dal referto di (i))*.
- **(ii) la partenza mai assorbita (H1):** **`TBS_stato_000000.npz`, F1 acceso tutto insieme come in T2, bordo spento, `5000` tick.**
  - **Il limite di Luca:** **non e' lo stesso istante.**
  - ### ⚠ **UN SECONDO LIMITE, DAL CODICE** *(`accensione.tick`)*: **a `t 0` `TBS` e' all'INIZIO della rampa del vuoto:** **`K = T_acc / s = 1000 / 0.15 = 6667` tick in cui i pezzi di `VC.VUOTO`** *(`CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`, `CAMM-FASE-VUOTO`)* **girano con la frazione `x lam_k`.** **Con `TK.percorri_tick`** *(«come in T2»)* **il vuoto si accende TUTTO INSIEME insieme a F1:** **un secondo colpo.** **La corsa si fa come scritta** *(e' il mandato)*; **se la discesa c'e', (h1) e' scritta con questo limite accanto** *(la discesa puo' venire dal colpo del vuoto)*. **La variante con la rampa del vuoto** *(`AC.tick` fino a `6667`, piu' F1)* **e' una proposta a Luca, non si fa.**
  - **Le letture (h1)/(h2) di Luca.**
- **(iii) il toro `L 162`** *(H2)*: **dopo (ii), con la sua sezione** *(27.7)*. **Prima del codice, dal codice:** **il periodo di F3 sulla griglia** *(se lo spostamento del blocco `81 x 81` non e' un multiplo del periodo, il raccordo salta per costruzione)*; **la fase `c(10000)`** *(`bordo.c_di`, la tabella `fase_F3.npz`)*; **il salto di `phi` al confine** *(e di `psi`, stampato)*. **Oltre `1e-12`: dichiarato, e (iii) si salta** *(Luca)*. ### ⚠ **Una stima che dico ORA** *(non misurata)*: **sul bordo del blocco** *(`R ~ 40`, nella fascia dove il bordo di `TBS` toglieva le onde)* **`phi` e' `c(t) F3` piu' le onde attenuate da `g_max 0.03`: e' probabile che il salto superi `1e-12`.**

#### 27.4.4 IL COSTO *(stima, dai tempi di T2: `824` s per `5000` tick)*

**(i): ~`30` minuti** *(il vuoto `5000`, il riferimento di T2 `1000`, il disturbato `1000`, la base `5000`)*; **(iv): ~`20`** *(`K = 1` e T2 `1000` ciascuno, la rampa `5000`)*; **(ii): ~`14`.**

#### 27.4.5 TODO

1. **Questa sezione, committata.**
2. **`csv/solitone/b1_profilo.py`** *(modi `i`, `iv`, `ii`)* **e l'inventario; la suite in `wt_zero`; il commit.**
3. **(i) → referto `doc/referti_l2/b1_i_profilo.txt`, sez. `27.5`;** **(iv) → `b1_iv_rampa.txt`, `27.6`;** **(ii) → `b1_ii_t0.txt`, `27.7`;** **(iii) → il suo progetto e `b1_iii_l162.txt`, `27.8`.**
4. **La tabella H1/H2/H3, e FERMO.**

#### 27.4.6 ANNOTAZIONE, PRIMA DELLE CORSE: **LA DEFINIZIONE DEL FRONTE CORRETTA** *(dopo una PROVA dello script a `200` tick, nello scratchpad, NON una corsa del mandato)*

- ### **IL MIO ERRORE nella 27.4.2:** **«l'anello col `cs` MEDIO piu' basso» misura il GUSCIO, non il fronte.** **Nella prova** *(lo stato di `TBS` a `10000`, (i))* **e' l'anello `16` a ogni campione** *(il `Lambda` medio dell'anello `16` e' `~1.6`, il vuoto svuotato attorno alla materia)*, **mentre il minimo globale va da `19` a `26`:** **con la mia scelta (f2) usciva per costruzione** *(un FALSO-ZERO del fronte)*.
- ### **LA DEFINIZIONE, QUELLA DI LUCA** *(«il raggio del minimo del profilo di `cs`»; il suo indizio di H3 e' il raggio di `cs` min)*: **`r_f` = l'anello del minimo del profilo di `cs` MIN** *(cioe' l'anello del nodo di `cs` min)*. **L'anello col `cs` medio piu' basso resta stampato accanto** *(`r_med`)*. **Il resto della 27.4.2** *(il tratto, il fit, le soglie, le letture)* **non cambia.**
- **Cosa ha detto la prova, oltre a questo** *(numeri della prova, non letture)*: **il cono `1.000000` nodi per tick** *(misurato)*; **la linearita' `2.4e-10` e quella complessa `2.9e-10`** *(sotto `1e-6`: le velocita' si leggono da `A(k)`)*; **`|v_g|` massimo `0.088272` nodi per tick per le bande di `psi`, `0.090371` per quelle di `phi`;** **(i-B) passa al bit al tick `100`, (i-F) fallisce come deve** *(`8.9e-11`)*. **Le corse vere ristampano tutto.**
- **E la struttura delle estremita'** *(un'altra premessa caduta, nella prova)*: **non sono in ordine di nodo ma di ARCO, `3` archi per nodo** *(gli archi che partono da `x`, con un'estremita' in `x` e una in un vicino)*: **la cella di `12 + 6` componenti e' quella di `DV.matrice`;** **il cono si misura sui nodi VERI delle estremita'.**

### 27.5 L'ESITO DI (i), T2 RIFATTO COL PROFILO *(la corsa dalle `14:37:18` alle `15:11:42` del `2026-11-10`, a `534db2e3`, blob `6b575a6b`; il referto `doc/referti_l2/b1_i_profilo.txt`)*

- **I controlli: `3/3` come devono.** **(i-B) AL BIT** contro il codice di T2 ai tick `100` e `1000` *(`max|diff| 0`)*, **e le stringhe uguali al referto di T2** *(`0.001942` a `26.28`; `0.000301` a `39.04`)*. **(i-F) fallisce come deve** *(al tick `1000` `max|diff| 2.373e-05`)*.
- **Le velocita'** *(27.4.1, misurate)*: **il cono `1.000000` nodi per tick** *(`23` nodi nel supporto)*; **la risposta lineare in senso complesso** *(`2.90e-10`)*, **`A(k)` unitaria entro `1.47e-09`;** **`|v_g|` massimo: `psi` `0.088272`, `phi` `0.090371` nodi per tick** *(e `0.08819` a `cs` spento, `bordo_riflessione`)*.
- **F1-V, la lettura:** **entro un fattore `2` ai tick `50`, `1000`, `5000`** *(i rapporti `1.1029`, `0.8448`, `1.4118`, come T2)*.
- ### **IL FRONTE: (f2), NIENTE FRONTE.** **`r_f`** *(l'anello del minimo di `cs` min)* **ai tick `50`, `100`, `200`, `500`, `1000`, `2000`, `5000`: `19`, `26`, `26`, `37`, `39`, `29`, `38`; il massimo `45` al tick `1450`.** **Sul tratto `50`-`1450`** *(`29` campioni)*: **`v_f 0.00432 +- 0.00285` nodi per tick, il RMS dei residui `6.199` anelli, un passo all'indietro di `17` anelli.** **`v_f` e' `~1/20` delle velocita' di gruppo** *(i rapporti `0.0489`, `0.0478`)*. **L'anello col `cs` MEDIO piu' basso resta il `16` a ogni campione** *(il guscio)*.
- ### **E IL PROFILO DICE PERCHE': LA DISCESA E' DI TUTTO IL DOMINIO, NON DI UNA ZONA** *(le righe del profilo di `cs` MIN nel referto)*: **dal tick `50` al `5000` `cs` min scende in OGNI anello:** **dentro `r < 20` da `4.60e-03` a `2.33e-04`; nella corona `20`-`27` da `5.23e-03` a `1.11e-04`; oltre `28` da `7.12e-03` a `6.55e-05`.** **Al tick `1000` i tre minimi sono `3.23e-04`, `3.12e-04`, `3.01e-04`: quasi uguali.** ### **Il minimo GLOBALE sta fuori per un margine piccolo, e per questo salta fra anelli lontani:** **«il raggio di `cs` min» era il posto dove un abbassamento GENERALE tocca per primo il fondo, non un luogo speciale.**
- **La pendenza di `ln(cs min)` nell'ultimo terzo: `-0.3998` per `1000` tick** *(come T2)*; **il minimo `5.979e-05` al tick `4800`, il raggio `38.91`.**
- ### **Per H3, l'indizio cade cosi' com'era:** **il raggio di `cs` min «da `19.2` a `26.3` a `39.0`» non e' un fronte** *(i primi `50` tick vanno da `19` a `26`, poi il minimo salta)*. **(iv) mette alla prova H3 per l'altra via** *(la rampa)*. **Per H2:** **la discesa anche a `r < 20`** *(lontano dall'antipodo)* **e' gia' un'indicazione contro l'antipodo come causa** *(una lettura mia, non quella di (iii))*.

### 27.6 L'ESITO DI (iv), F1 ACCESO PIANO *(la corsa dalle `15:16:54` alle `15:38:17` del `2026-11-10`, a `e340476c`, blob `6b575a6b`; il referto `doc/referti_l2/b1_iv_rampa.txt`)*

- **I controlli:** **(iv-B) AL BIT** *(`K = 1` contro il codice di T2, ai tick `100` e `1000`: `max|diff| 0`)*. **La rampa agisce:** **al tick `1` il rapporto `max|cs - s| / max|L - s|` e' `2.467399e-06` = `lambda_1 = sin^2(pi / 2000)`.**
- ### **LA LETTURA COL CRITERIO SCRITTO: CASO INTERMEDIO.** **(q1) no:** **`cs` min scende a `5.078e-05`** *(al tick `3950`, il raggio `33.57`)*, **sotto `1e-3`.** **(q2) no:** **la pendenza nell'ultimo terzo e' `+0.0347` per `1000` tick contro `-0.3998` di (i)** *(fuori dal `30%`)*.
- ### **E I NUMERI DICONO PERCHE'** *(le righe di `cs` min nei due referti)*:

| tick | (i) `cs` min @ raggio | (iv) `cs` min @ raggio |
|---|---|---|
| `50` | `0.004596` @ `19.22` | `0.149197` @ `15.74` |
| `500` | `0.000485` @ `37.71` | `0.078431` @ `10.12` |
| `1000` | `0.000301` @ `39.04` | `0.000407` @ `41.30` |
| `1500` | `0.000216` @ `35.77` | `0.000089` @ `41.30` |
| `3000` | `0.000109` @ `35.77` | `0.000063` @ `41.30` |
| `5000` | `0.000065` @ `38.91` | `0.000052` @ `32.54` |

  - **Durante la rampa `cs` min resta alto** *(`0.149` -> `0.078`)*; **a `K = 1000`, quando F1 e' pieno, cade a `4.1e-4`** *(come (i) allo stesso tick)*, **e a `1500` e' gia' SOTTO (i).** **Poi si ferma su un piano attorno a `5e-5`** *(`5.4e-5` a `3500`, `5.2e-5` a `5000`)*.
  - **(i) a `5000` e' a `6.5e-5` e scende ancora:** **le due corse vanno verso LO STESSO FONDO**, **(iv) ci arriva prima e si ferma.**
- ### **LA MIA LETTURA, da confermare** *(non quella di Luca)*: **il colpo dell'accensione NON spiega la discesa:** **acceso piano, F1 porta `cs` min allo stesso livello** *(`~5e-5`)*; **cambia solo QUANDO.** **La pendenza diversa nell'ultimo terzo viene dal fatto che (iv) ha gia' raggiunto il fondo e (i) no.** **H3, cosi' com'era, non regge.**
- **Il fronte:** **(f2) anche qui** *(RMS `9.351` anelli, un passo all'indietro di `10`)*.

### 27.7 L'ESITO DI (ii), LA PARTENZA MAI ASSORBITA *(la corsa dalle `15:43:58` alle `15:57:29` del `2026-11-10`, a `a1708087`, blob `6b575a6b`; il referto `doc/referti_l2/b1_ii_t0.txt`)*

- **La partenza:** `TBS_stato_000000.npz` *(t `0`)*, **il centro di `rho` `(40.5, 40.5)`.** **I due limiti** *(27.4.3)*: **non e' lo stesso istante; e il vuoto si accende TUTTO INSIEME con F1** *(a `t 0` `TBS` era all'inizio della rampa del vuoto)*.
- ### **LA LETTURA COL CRITERIO SCRITTO: CASO INTERMEDIO** *(la pendenza di `ln(cs min)` nell'ultimo terzo `-0.1387` per `1000` tick, fra `-0.2` e `-0.05`)*.
- ### **MA `cs` MIN SCENDE ALLO STESSO LIVELLO DI (i)** *(le righe del referto)*: **`0.005623` @ `12.62` al tick `50`; `0.000852` @ `16.90` a `250`; `0.000231` @ `31.78` a `1000`; `0.000121` a `3000`; `0.000093` @ `31.78` a `5000`** *(il minimo `9.005e-05` al tick `4900`)*. **(i) a `5000`: `6.5e-5`.**
- ### **E IL PROFILO MOSTRA DA DOVE PARTE** *(i minimi per zona, dalle righe del profilo di `cs` MIN)*: **al tick `50` e' scesa solo la zona della materia** *(`r < 20`: `5.62e-03`; `20`-`27`: `1.06e-01`; oltre `28`: `1.50e-01`, cioe' ancora `s`)*; **al `1000` tutte** *(`5.50e-04`, `4.32e-04`, `2.31e-04`)*; **al `5000` tutte attorno a `1e-4`** *(`1.07e-04`, `1.23e-04`, `9.34e-05`)*. **La discesa NASCE dove c'e' la materia e si allarga a tutto il dominio.**
- **Il fronte: (f2)** *(il RMS `4.378` anelli, un passo all'indietro di `12`; sul tratto `50`-`750` `v_f 0.0382 +- 0.0056` nodi per tick, il `~43%` di `v_g`, non entro il `20%`)*.
- ### **LA MIA LETTURA, da confermare:** **la storia del bordo NON serve a spiegare la discesa** *(da uno stato MAI assorbito `cs` min arriva a `~1e-4` come da quello a `10000`)*, **con il limite del vuoto acceso tutto insieme** *(un colpo in piu', che non posso separare con questa corsa)*. **H1, cosi' com'era, non regge.**

### 27.8 (iii) IL TORO `L 162`: **IL RACCORDO NON REGGE, (iii) SI SALTA** *(il controllo dalle `16:03:17` alle `16:03:34` del `2026-11-10`, a `4052a546`, `csv/solitone/b1_raccordo.py` blob `f1c70287`; il referto `doc/referti_l2/b1_iii_l162.txt`)*

- **Il blocco `81 x 81` dello stato di `TBS` spostato di `40` nel toro `162`, riempito con `c(t) F3`:** **`19360` archi portati, `952` toccano l'orlo.**
- **Il controllo positivo PASSA:** **a `t 0` il salto sull'orlo e' `1.110e-16`** *(lo stato mai assorbito e' `F3` esatto sull'orlo)*.
- ### **A `t 10000` IL SALTO E' `3.853e-02`** *(`max|phi - c F3|` sull'orlo)*, **e `max|psi|` sull'orlo `4.989e-02`**: **oltre `1e-12` di Luca: (iii) SI SALTA, dichiarato.** **Il motivo e' fisico:** **sull'orlo del blocco** *(la fascia assorbente di `TBS`, `R >= 28`)* **ci sono le onde del vuoto e la materia emessa** *(non assorbite del tutto)*: **un raccordo esatto con `c(t) F3` non c'e'.**

### 27.9 LA TABELLA H1/H2/H3, E IL FERMO *(il mandato: «dopo le quattro corse: fermo»)*

| | l'ipotesi | la corsa | che cosa dice | regge? |
|---|---|---|---|---|
| **H1** | **la storia del bordo** | **(ii)** `TBS` a `t 0`, mai assorbita | **`cs` min scende a `9.0e-5`** *(al `4900`)*, **come in (i)** *(`6.5e-5` al `5000`)*; **la discesa nasce nella zona della materia e si allarga a tutto il dominio** | ### **NON REGGE** *(lettura mia; col criterio scritto: caso intermedio, la pendenza `-0.139`)*. **Il limite: il vuoto si accende tutto insieme a `t 0`** |
| **H2** | **il toro finito, l'antipodo** | **(iii)** `L 162` | **NON FATTA:** il raccordo salta di `3.85e-2` | ### **NON MISURATA.** **Gli indizi contro** *(non una misura di H2)*: **in (i) `cs` min scende in OGNI anello, anche a `r < 20`** *(da `4.6e-3` a `2.3e-4`)*; **in (ii) parte dalla materia, non dall'antipodo** |
| **H3** | **il colpo dell'accensione** | **(iv)** la rampa `K 1000` | **acceso piano, F1 porta `cs` min allo STESSO FONDO** *(`~5e-5`)*, **prima, e li' si ferma** | ### **NON REGGE** *(lettura mia; col criterio scritto: caso intermedio)* |

- **Il fronte:** **(f2) in tutte e tre le corse** *(il minimo salta fra anelli lontani; le velocita' di confronto misurate: il cono `1`, `|v_g|` `0.0883` e `0.0904` nodi per tick)*.
- ### **CHE COSA RESTA, DETTO COME IPOTESI E NON COME MISURA:** **la discesa sembra della DINAMICA con F1, in tutto il dominio, verso un fondo `~5e-5`-`1e-4`.** **Una stima** *(non misurata)*: **col `cs` di F1 che rilassa verso `L = FP.cs(Lambda)`, `cs ~ 6e-5` vorrebbe `Lambda` dell'ordine di `1e-3` in quel nodo:** **il vuoto quasi VUOTO in nodi isolati.** **Il profilo stampa `Lambda` MEDIO per anello, non il minimo:** **la coda bassa di `Lambda` non e' misurata.** **Se interessa, la misura naturale e' la distribuzione di `Lambda` per nodo** *(il minimo e i quantili bassi nel tempo)* **sulle stesse corse:** **una proposta, non la faccio.**
- ### **FERMO** *(il mandato)*: **la scena di F4 e il passo dopo li decide Luca.** **F4 resta in coda dietro questa decisione** *(il mandato delle `08:48`: con (c1)/(c2) di B1 vecchio; il caso di oggi e' piu' vicino a «della dinamica», ma la scelta della scena e' sua)*.

### 27.10 H4, IL VUOTO COL TEMPO LOCALE REGGE I DISTURBI? *(Luca `2026-11-10` `16:06`)*: **H4.0, PRIMA DEL CODICE**

*(Il mandato chiama questa sezione «27.9»: la `27.9` c'e' gia', ed e' la tabella H1/H2/H3 di B1 (`93579fe7`). **H4.0 e' la `27.10`, l'esito la `27.11`**: dichiarato.)*

#### 27.10.1 LA SCENA DEL SOLO VUOTO *(dal codice)*

- **Il motore ammette `psi = 0`:** **F1-V di T2 e di (i) gira cosi'** *(`st["psi_h"][...] = 0`, `st["phi_h"][...] = phi_v`, il tick intero)*. **Il vuoto: `c(10000) F3`** *(`bordo.c_di(10000, tab, K, omega)`, la tabella `fase_F3.npz`, `K 6667`; `F3` = `CA.vuoto_della_corsa`)*. **`Lambda_c` quello di T2** *(dalla media di `Lambda` del vuoto)*.
- **`cs` SPENTO** *(per (v2))*: **`mot.cs = None` e `mot.lambda_c = None` a ogni tick** *(T3, `tau_lambda.corsa`, spegne con `lambda_c = None`; la scena nuova ha `mot.cs = None`)*. **Per (v2) la «distribuzione di `cs`» e' quella di `L = FP.cs(Lambda, Lambda_c)`, il `cs` che la legge DAREBBE** *(dichiarato: a `cs` spento non c'e' un `cs`)*.

#### 27.10.2 L'AMPIEZZA DELL'ALONE `A_h` E LO SPETTRO *(misurati dallo script, PRIMA delle corse; stampati nel referto)*

- **Lo stato di `TBS` a `10000`:** **il residuo `r = phi - c(10000) F3` sulle estremita' il cui nodo sta a `r > 20` dal centro di `rho`** *(il centro come in (i))*. **`A_h` = la rms di `|r|` su quelle estremita'.** **Accanto, stampata: la proiezione `a = <F3, phi> / |F3|^2` sulla stessa zona** *(se `a` non e' `c`, una parte del residuo e' di fase o di ampiezza del vuoto stesso)*.
- **Lo spettro:** **il residuo con la zona `r <= 20` messa a zero, nella cella** *(`phi` come `(L, L, 6)`: i `3` archi del nodo, 27.4.6)*, **`fft2` per componente, la potenza sommata sulle `6` e mediata per anelli di `|k|`** *(la larghezza del passo della griglia in `k`)*. **La maschera altera lo spettro** *(dichiarato)*: **e' «quello che si ricava facilmente».**

#### 27.10.3 IL DISTURBO *(seme fisso `2026`, `CPF.SEME`)*

- **Per ognuna delle `6` componenti della cella:** **un rumore gaussiano complesso in `k` per la radice dello spettro radiale di 27.10.2, `ifft2`;** **`delta` reso ORTOGONALE a `F3`** *(tolta la proiezione)* **e riscalato a rms `A` sulle estremita'** *(`A = A_h` per (v1), (v2); `A_h / 10` per (v3))*.
- ### **`phi = c (alpha F3 + delta)`, `alpha = sqrt(1 - |delta|^2 / |F3|^2)`:** **la NORMA di `phi` e' quella del vuoto** *(entro l'arrotondamento: stampata)*, **quindi `Lambda` MEDIO e' conservato** *(`= norma / n`)* **e `Lambda_c` non cambia;** **la proiezione su `F3` scende da `c` a `c alpha`** *(stampato `1 - alpha`)*: **conservare insieme la norma e la proiezione non si puo'** *(dichiarato)*.

#### 27.10.4 LE CORSE E LE MISURE *(un solo script, `csv/solitone/h4_vuoto.py`)*

- **(v0)** il vuoto SENZA disturbo, F1; **(v1)** con `A_h`, F1; **(v2)** con `A_h`, `cs` spento; **(v3)** con `A_h / 10`, F1: **`5000` tick ciascuna, in un solo processo, il referto `doc/referti_l2/h4_vuoto_disturbato.txt`.**
- **(i-q):** ### **gli stati e le mappe di (i) NON bastano** *(lo script di (i) non ne ha salvati: la corsa si RIFA' con lo strumento della distribuzione)*; **il referto `doc/referti_l2/h4_distribuzione.txt`** *(`--corsa iq`)*.
- **Ogni `50` tick:** **`cs` min; i quantili di `cs` `0.1%`, `1%`, `10%`, `50%`; la frazione dei nodi con `cs < 1e-3` e `< 1e-2`; `Lambda` min e la rms di `Lambda - Lambda` medio; la norma di `phi` e di `psi`.**
- **Il gemello di (v1) e (v2)** *(la stima di Lyapunov, come T2)*: **`phi` delle `6` estremita' della cella del nodo `0` per `(1 + 1e-10)`;** **la differenza `max|Lambda - Lambda_gemello|` a ogni tick** *(la base tiene `Lambda` di ogni tick)*; **il tasso: la pendenza di `ln` della differenza dal tick `1` al primo tick sopra `1e-4`** *(la soglia di T2)*. **Disturbare `phi` e non `cs` e' una mia scelta** *(a `cs` spento non c'e' `cs` da disturbare; la stessa per le due corse)*.
- **I DEVE:**
  - **(v0) F1-V:** **la deriva di `cs` medio entro un fattore `2` da `dcs/dLambda` per la deriva di `Lambda` medio, ai tick `50`, `1000`, `5000`** *(il criterio di Luca, come in T2)*;
  - **lo strumento della distribuzione su uno stato di prova** *(il vuoto `F3` con `10` nodi a `Lambda = 0.002`: `phi` di quei nodi riscalato)*: **DEVE PASSARE la frazione sotto `1e-3` = `10/6561` esatta;** **DEVE FALLIRE «la frazione sotto `1e-3` e' zero (il vuoto calmo)»** *(lo strumento sa dire di no)*.

#### 27.10.5 LE LETTURE *(di Luca; i dettagli miei, dichiarati)*

- **(u1)** **in (v1) `cs` min scende sotto `1e-3` E la frazione sotto `1e-3` cresce nel tempo** *(mio: la media dell'ultimo terzo oltre quella del primo)*, **mentre in (v2) la rms di `Lambda` resta entro il `10%` della sua iniziale** *(a ogni campione)*: **H4 regge.**
- **(u2)** **(v1) resta calmo** *(`cs` min sopra `0.7 s` per tutti i `5000` tick)*: **H4 cade.**
- **(u3)** **(v1) turbolento e (v3) calmo:** **una soglia, fra `A_h / 10` e `A_h`.**
- **(e1)** **in (i-q) la frazione sotto `1e-3` resta sotto `1e-3` per tutta la corsa:** **pochi nodi, valori estremi;** **(e2)** **cresce oltre `1e-2`:** **e' il vuoto intero che si svuota.** **Fra le soglie: caso intermedio.**

#### 27.10.6 IL COSTO E L'ORDINE *(stima: `~0.16` s per tick, da (i))*

**(v0) ~`14` min, (v1) e (v2) col gemello ~`27` ciascuna, (v3) ~`14`: ~`80` minuti in un processo; (i-q) ~`14`.** **Sul principale gira la carta (r-b): due processi, e una suite pre-commit aspetta che uno finisca** *(Luca)*.

### 27.11 L'ESITO DI H4, IL VUOTO DISTURBATO *(la corsa dalle `16:44:08` alle `17:40:27` del `2026-11-10`, a `a54a3ee4`, blob `7f9ffb9b`; il referto `doc/referti_l2/h4_vuoto_disturbato.txt`; exit `1`)*: **(u1) H4 REGGE -- E IL DEVE DI (v0) FALLISCE: IL VUOTO UNIFORME CON F1 E' INSTABILE DA SOLO. FERMO.**

- **Lo strumento:** **la frazione sotto `1e-3` sullo stato di prova `1.524158e-03` = `10/6561`** *(DEVE PASSA)*; **«zero» fallisce come deve.**
- **`A_h = 3.308833e-02`** *(la rms di `|phi - c F3|` su `30654` estremita' a `r > 20` di `TBS` a `10000`; `|F3|` per estremita' `1`)*; **la proiezione sulla zona `a = 0.98762 + 0.15668 i` contro `c = 0.98769 + 0.15643 i`** *(il residuo e' quasi tutto onde, non fase)*. **Lo spettro: il picco al bin `3`** *(`|k| 0.2687`)*.
- ### **(v1)** *(`A_h`, F1)*: **`cs` min `4.274e-05`; la frazione sotto `1e-3` dal primo terzo `3.559e-02` all'ultimo `2.137e-01`;** **il gemello: Lyapunov `0.02475` per tick** *(dal tick `1` al `387`)*, **la differenza di `Lambda` a `2.630` alla fine.**
- ### **(v2)** *(`A_h`, `cs` SPENTO)*: **CALMO:** **la rms di `Lambda` `1.164e-01`, lo scarto massimo `0.0069` relativo;** **il gemello NON cresce** *(la differenza `~5e-10` per tutti i `5000` tick: Lyapunov `0.00000`)*.
- **(v3)** *(`A_h / 10`, F1)*: **turbolento come (v1)** *(`cs` min `6.966e-05`; la frazione sotto `1e-3` da `3.506e-02` a `2.176e-01`)*.
- ### **LA LETTURA COL CRITERIO SCRITTO: (u1) H4 REGGE** *(«il vuoto col tempo locale non regge i disturbi, e il solitone non serve»)*. **(u3) non c'e'** *(anche `A_h / 10` e' turbolento: nessuna soglia fra `A_h / 10` e `A_h`)*.
- ### ⛔ **IL DEVE DI (v0) FALLISCE** *(F1-V: ai tick `1000` e `5000` la deriva di `cs` medio e' `-3.07e-02` e `-3.21e-02` contro `-3.5e-15` e `-4.1e-15` attese)*. **(v0) e' il vuoto `c(10000) F3` SENZA disturbo, con F1:** **la rms di `Lambda` cresce da sola:**

| tick | rms di `Lambda` | `cs` min | la frazione sotto `1e-2` |
|---|---|---|---|
| `100` | `5.037e-15` | `0.150` | `0` |
| `150` | `5.527e-13` | `0.150` | `0` |
| `200` | `1.467e-09` | `0.150` | `0` |
| `250` | `4.136e-06` | `0.150` | `0` |
| `300` | `1.190e-02` | `0.148` | `0` |
| `400` | `7.313` | `2.600e-03` | `3.88e-01` |
| `1000` | `7.986` | `3.030e-04` | `5.58e-01` |
| `5000` | `8.203` | `8.432e-05` | `6.05e-01` |

  - **Il tasso di crescita** *(dalle righe del referto, `python -c`)*: **`0.1577` per tick fra `150` e `200`, `0.1589` fra `200` e `250`:** **un'instabilita' LINEARE del vuoto uniforme con F1, un fattore `e` ogni ~`6` tick, seminata dall'arrotondamento** *(`~5e-15`)*.
  - **Al tick `5000` la mediana di `cs` e' `4.875e-03`** *(`s = 0.15`)* **e il `60%` dei nodi sta sotto `1e-2`:** **e' il vuoto INTERO che si svuota.**
- ### **PERCHE' T2 E (i) NON LO VEDEVANO** *(un'ipotesi mia, NON misurata)*: **il loro F1-V partiva da `F3` a fase `1`** *(componenti reali, `+-1`)*: **il vuoto resta uniforme AL BIT e l'instabilita' non ha un seme** *(in (i) la rms non era stampata; la deriva di `Lambda` `~1e-14` per `5000` tick)*. **Con `c(10000) F3`** *(una fase complessa)* **l'arrotondamento rompe l'uniformita' a `~5e-15`, e dopo ~`300` tick il vuoto e' turbolento.** ### **Quindi «F1-V regge» di T2 era un FALSO-UNO** *(un controllo che passava perche' il seme era zero, non perche' il vuoto fosse stabile)*: **da confermare** *(per esempio: (v0) con `F3` a fase `1` piu' un disturbo `1e-14`)*.
- ### **CHE COSA VUOL DIRE PER B1** *(lettura mia)*: **la discesa di `cs` min di T2, (i), (iv), (ii) e' questa instabilita' del vuoto con F1, seminata dalle onde del solitone:** **il solitone non serve** *(u1)*; **e il fondo comune `~5e-5`-`1e-4` e' quello del vuoto turbolento** *(in (v0) a `5000`: `8.4e-5`)*.
- ### ⛔ **FERMO** *(la regola: un DEVE che fallisce si committa, e ci si ferma)*. **(i-q) NON e' girata.** **Le domande a Luca:**
  1. **(i-q) serve ancora** *(la distribuzione della scena del solitone)*, **o il risultato di (v0) basta?**
  2. **Confermare il FALSO-UNO di F1-V:** **(v0) con `F3` a fase `1`, con e senza un seme `1e-14`?**
  3. **F4 e la sua scena:** **con un vuoto F1 instabile da solo, la rampa di F4 ha ancora senso, o serve prima capire l'instabilita'** *(il suo tasso `~0.16` per tick contro le scale del tick)*?
- ### **LA TABELLA H1-H4** *(provvisoria: (i-q) manca)*: **H1 non regge; H2 non misurata; H3 non regge; H4 REGGE** *(u1)*, **e piu' forte di come era scritta: non servono nemmeno i disturbi, basta l'arrotondamento.**

## 28. IL VUOTO COL TEMPO LOCALE E' INSTABILE: PERCHE'? *(Luca `2026-11-10` `19:37`, dopo H4 `2389b8e2`)*: **S0, E S1/S2 PRIMA DEL CODICE**

### 28.0 S0: LE RISPOSTE DI LUCA ALLE TRE DOMANDE DI 27.11, E LA TABELLA H1-H4 DEFINITIVA

- **Le risposte di Luca** *(`19:37`)*:
  1. ### **(i-q) NON si fa: (v0) basta.**
  2. ### **Il FALSO-UNO di F1-V si conferma: S1.**
  3. ### **F4 ASPETTA: prima si capisce l'instabilita' (S2).**
- ### **E una lettura mia che NON era giustificata, scritta da Luca:** **«e1» (pochi nodi, dalla media lontana di `cs` in (i))** **non si usa:** **la media di una distribuzione cosi' storta la tirano su i nodi con `Lambda` alto.** *(Il mio errore: una media letta come un indizio sulla forma della distribuzione.)*
- **I vincoli del mandato:** **nessuna modifica al nucleo, nessuna TARATURA;** **le scansioni di S2 su `Lambda_c`, `s`, `Lambda` sono una MAPPA: non si sceglie nessun valore;** **il vuoto F3;** **un test breve alla volta** *(sul principale gira `C50-0`)*; **le suite aspettano se girano gia' due processi.**
- ### **LA TABELLA H1-H4, DEFINITIVA:**

| | l'ipotesi | l'esito | dove |
|---|---|---|---|
| **H1** | la storia del bordo | **NON REGGE** | 27.5-27.7, 27.9 |
| **H2** | l'antipodo | **NON MISURATA, SUPERATA** *(H4 spiega la discesa senza il bordo)* | 27.8, 27.9 |
| **H3** | lo shock dell'accensione | **NON REGGE** | 27.6, 27.9 |
| **H4** | il vuoto col tempo locale non regge i disturbi | ### **REGGE, e piu' forte di come era scritta:** **basta l'arrotondamento, senza disturbo** | 27.11 |

### 28.1 S1, IL FALSO-UNO DI F1-V: **LE PREMESSE DAL CODICE, IL PROGETTO, LE LETTURE** *(prima del codice)*

- **Dal codice** *(`csv/solitone/corsa_accensione.py` `vuoto_della_corsa` -> `_solitone_dal_fondo.fondo_con_fasi`)*: **F3 e' un flusso costante PER DIREZIONE** *(la coda `+e^{i theta_d}`, la testa `-e^{i theta_d}`)*: **lo stesso valore in ogni cella, a meno della direzione** *(quindi un vuoto invariante per traslazione di un nodo)*. **«A fase `1`» = `phi_v` com'e', «`c(10000) F3`» = `phi_v` per la fase globale `c` della tabella `fase_F3.npz`.** **Se le componenti di F3 a fase `1` siano reali, lo stampa lo script** *(`max |Im phi_v|`)*: **in 27.11 l'ho scritto senza stamparlo.**
- **Le corse** *(un solo script, `csv/solitone/s1_falso_uno.py`; F1 come T2 e H4: il rilassamento esatto, (q2), il bordo spento, `Lambda_c` = quello di T2)*:
  - **(v0a)** **F3 a fase `1`, senza seme, `1000` tick;**
  - **(v0b)** **lo stesso piu' un seme `1e-14`:** **un rumore gaussiano complesso BIANCO** *(per estremita', seme fisso `CPF.SEME`)*, **reso ortogonale a F3 e riscalato a rms `1e-14` per estremita'; la norma conservata come in H4** *(`phi = alpha F3 + delta`, `alpha = sqrt(1 - |delta|^2/|F3|^2)`)*; **`1000` tick;**
  - **(v0c)** **`c(10000) F3` senza seme, `400` tick:** ### **DEVE ridare (v0) di H4 AL BIT:** **(1) lo stato `phi` ai tick `200` e `400` uguale al bit a quello di `h4_vuoto.corsa`** *(il codice che ha prodotto (v0), importato e rigirato a `200` e a `400` tick)*; **(2) le righe ai tick `200` e `400`, nel formato di `h4_vuoto.stampa`, uguali AL CARATTERE a quelle di `doc/referti_l2/h4_vuoto_disturbato.txt`.**
- **Ogni `10` tick:** **la rms di `Lambda`, `cs` min, la frazione dei nodi sotto `1e-2`** *(e accanto, `cs` medio e `Lambda` medio)*.
- **Il tasso** *(fissato qui)*: **la pendenza di `ln` della rms di `Lambda` contro il tick, sui campioni con la rms fra `1e-12` e `1e-4`** *(la crescita lineare: sopra il seme, sotto la saturazione)*; **il tasso di (v0) e' quello di (v0c) con la stessa finestra** *(e accanto il `0.158` di 27.11, che era a passo `50`)*.
- ### **LE LETTURE (di Luca):**
  - **(z1)** **(v0a) resta uniforme** *(la rms di `Lambda` sotto `1e-13` per `1000` tick)* **E (v0b) cresce col tasso di (v0) entro il `5%`:** ### **il falso-uno e' confermato; l'instabilita' c'era anche in T2, senza seme.**
  - **(z2)** **altrimenti: si scrive senza interpretare.**
- **Le conseguenze, da elencare nell'esito** *(dal codice, gia' letto)*: **F1-V di T2** *(`carta_f1_lunga.py`: `st["phi_h"][...] = phi_v`, fase `1`)*; **F1-V di (i)** *(`b1_profilo.py`: lo stesso)*; **F1-V di `d2689b81`** *(`carta_f1.py` a quel commit: `phi_v`, «`cs = s` al bit» -- e FALLIVA, sez. 22)*; **T1** *(`lambda_vuoto_deriva.py`: `phi_v`, ma a `cs` FISSO `0.15` e `lambda_c = None`: senza la legge di `cs` l'instabilita' non c'e' per costruzione)*.

### 28.2 S2.0: LO SPETTRO DI STABILITA' LINEARE DEL VUOTO CON LA LEGGE DI `cs` -- **LE PREMESSE DAL CODICE** *(prima del codice)*

- **(a) Le variabili.** **`phi`: `6` complessi per cella** *(le `6` estremita' dei `3` archi del nodo, arc-major: 27.4.6)*, **cioe' `12` reali;** **`cs`: `1` reale per nodo** *(con F1 `cs` ha memoria: e' una variabile; con la legge istantanea e' una funzione di `Lambda`, ma la tengo nel vettore -- vedi (L-ist))*. **`psi`: `12` complessi per cella** *(`6` estremita' x `2` spin)*. ### **`psi` a `psi = 0`: NON lo so dal codice** *(i flussi materia-vuoto, posizioni `0` e `13`, `CAMM-MATERIA-VUOTO`, non li ho letti per intero)*: **lo MISURO** -- **la risposta di `phi`, `cs` a un `delta psi` e di `psi` a `delta phi`, `delta cs`, con le differenze simmetriche** *(un termine quadratico in `psi` si cancella esattamente nella differenza simmetrica)*. **Se le due risposte incrociate sono zero** *(sotto `1e-12` relativo)*, **`psi` si stacca al primo ordine e si toglie** *(dichiarato, con lo spettro del suo blocco stampato accanto)*; **altrimenti resta nel vettore** *(`37` reali per cella)*.
- **(b) Il riferimento che gira.** **`c F3` e' un autostato del tick a meno della fase `e^{-i omega}`** *(C0 di `C50-0`: lo scarto da `c(t) F3` `3.968e-14` a `200` tick)*. **La mappa linearizzata e' quella di un tick seguito dalla rotazione `e^{+i omega}` di `phi`;** **`e^{-i omega}` si misura sulla base** *(`<phi_0, phi_1> / |<phi_0, phi_1>|`, un tick)*. **Il residuo della base** *(`|e^{i omega} phi_1 - phi_0|`, `|cs_1 - cs_0|`)* **si stampa per ogni punto:** ### **se un punto della mappa NON e' un punto fisso** *(il residuo oltre `1e-10` relativo)*, **la linearizzazione li' non vale, e lo dico** *(non lo correggo)*.
- **(c) La rappresentazione reale:** **`cs` dipende da `|phi|^2`, quindi la mappa NON e' lineare in senso complesso;** **il vettore della cella: `Re phi` (`6`), `Im phi` (`6`), `cs` (`1`) = `13` reali** *(piu' `psi` se (a) lo tiene)*.
- **(d) L'invarianza per traslazione:** **la risposta `R(x)` a un impulso in ognuna delle `13` direzioni della cella del nodo `0`, con differenze simmetriche** *(`a = 1e-6` relativo alla scala della componente: `|phi|` per estremita', `cs` della base)*; **`A(k) = somma_x R(x) e^{-i k x}`** *(`fft2` sulla griglia `L x L`)*, **`13 x 13` per ognuno dei `6561` `k`.** **I controlli:** **la linearita' `|R(2a) - R(a)| / max|R|` sotto `1e-6`** *(per ogni punto)*; **l'invarianza: la risposta a un impulso in un altro nodo, traslata, uguale a quella del nodo `0`** *(sotto `1e-9` relativo)*.
- **I casi** *(S2.1)*:
  - **(L-F1)** **F1 come nelle corse:** **`cs' = cs + r (L(Lambda') - cs)`, `r = 1 - e^{-omega_v}`, (q2)** *(`cs_primo_zero`)*;
  - **(L-ist)** **la legge istantanea:** ### **la stessa mappa con `r = 1`** *(`cs' = L(Lambda')`: il `cs` del tick dopo e' quello di `Lambda` all'inizio di quel tick, senza memoria)*, **e (q2) come (L-F1)**: ### **una SCELTA MIA, dichiarata:** **cosi' (L-ist) e (L-F1) differiscono SOLO per la memoria.** **La legge istantanea DEL NUCLEO** *(`tick.tick_con_cs`: `cs` al centro del palindromo a punto fisso, col termine `CAMM-FASE-VUOTO` acceso)* **e' un ALTRO oggetto, e qui NON si misura** *(lo segnalo a Luca)*.
  - **Il caso di oggi:** **`Lambda = 6`, `Lambda_c` di T2** *(`34`, dalla media di `Lambda`)*, **`s = 0.15`.**
- **La mappa** *(S2.2, senza scegliere niente)*: **`Lambda_c` in `{8.5, 17, 34, 68, 136, 340}` a `Lambda = 6`** *(`cs` del vuoto `6/(6 + Lambda_c)`, stampato)*; **`s` in `{0.05, 0.15, 0.3}` con `Lambda_c = (6 - 0)(1 - s)/s`** *(`114`, `34`, `14`)*; **`Lambda` del vuoto in `{6, 3, 1, 0.5, 0.1}` a `Lambda_c = 34`** *(`phi = c F3 sqrt(Lambda/6)`)*. **I punti ripetuti si contano una volta:** **`12` punti, per (L-F1) e (L-ist).**
- **Per ogni punto:** **`|lambda|_max` e `ln |lambda|_max` per tick; il `k` dove sta** *(`|k|` con l'immagine minima, la direzione in gradi, e quanti `k` equivalenti)*; **l'autovettore:** **la frazione in `cs` e in `phi`;** **la banda di `phi`:** **i pesi della parte `phi` sugli autovettori del blocco `phi -> phi`** *(il tick a `cs` congelato, unitario)*, **coi due pesi piu' grandi e la loro `omega`;** **`k = 0` o `k` finito.**
- **Il meccanismo, dalla matrice al `k` piu' instabile** *(una LETTURA della matrice)*: **per l'autovalore `lambda` vale `lambda - A_cc = g(lambda)`, `g = A_cphi (lambda - A_phiphi)^{-1} A_phic`;** **`g` si scompone per bande:** **`g = somma_b (A_cphi e_b)(e_b^H A_phic) / (lambda - lambda_b)`;** **stampo `A_cc` (`= 1 - r` atteso), le norme di `A_cphi` e `A_phic`, e i contributi di bande piu' grandi con `lambda - lambda_b`.**
- **I DEVE:**
  - **a `cs` spento lo spettro e' unitario:** **`max ||lambda| - 1|` sotto `1e-9`** *(`12` reali per cella, `mot.cs = None`, `mot.lambda_c = None`)*;
  - **nel caso di oggi (L-F1) il tasso piu' grande riproduce `0.158` per tick entro il `5%`** *(il `0.158` di 27.11)*;
  - **un'onda piana seminata nella simulazione sul `k` piu' instabile** *(la parte reale dell'autovettore per `e^{i k x}`, ampiezza massima `1e-11`; la simulazione di F1 vera, `100` tick, contro un gemello senza onda)* **cresce col tasso dello spettro entro il `5%`** *(la pendenza di `ln` della differenza fra il tick `20` e il `100`)*;
  - ### **DEVE FALLIRE:** **a `cs` spento, un fattore `(1 + 1e-3)` su `phi` dopo il tick** *(il «pezzo» e' l'ultimo: lo applico a TUTTA `phi`, quindi il modo giusto sono TUTTI -- una scelta mia, dichiarata)*: **deve comparire `|lambda| = 1.001` entro `1e-9`, su ogni `k`;** **e il DEVE dell'unitarieta' su quella mappa DEVE FALLIRE.**
- ### **LE LETTURE (di Luca):**
  - **(w1)** **(L-ist) e' gia' instabile nel caso di oggi:** **la colpa e' della LEGGE, non della memoria;**
  - **(w2)** **(L-ist) stabile e (L-F1) instabile:** **la colpa e' della MEMORIA di F1;**
  - **(w3)** **nella mappa esistono zone stabili:** **le riporto come mappa** *(`Lambda_c`, `s`, `Lambda`)*, **coi confini. NESSUNA scelta;**
  - **(w4)** **instabile in tutta la mappa:** **il vuoto con questa legge del tempo locale e' instabile per costruzione.** ### **FERMO: la decisione e' di Luca.**
  - **«Stabile»** *(il mio dettaglio, dichiarato)*: **`|lambda|_max - 1` sotto `1e-9`** *(la soglia del DEVE unitario)*.
- **Il costo** *(stima: `~0.16` s per tick)*: **`53` tick per punto e caso** *(la base e `13 x 4` differenze)*, **`24` linearizzazioni, piu' `psi`, i controlli, l'onda piana:** **~`2000` tick, ~`6` minuti.** **Il referto `doc/referti_l2/s2_spettro_vuoto_cs.txt`; lo script `csv/solitone/s2_spettro.py`.**
- ### **DOPO S2: FERMO.** **F4, la forma della legge, e qualunque cambio di `Lambda_c` o di `s` sono di Luca.**

## 29. LA LEGGE COMANDATA DALLA MATERIA *(Luca `2026-11-10` `19:47`, aggiunta al mandato delle `19:37`)*: **UN'OPZIONE, SOLO SCRITTURA** *(nessun codice, nessuna corsa, nessuna scelta; nessuna voce dell'indice cambia stato)*

### 29.1 L'OSSERVAZIONE *(di LUCA, `19:44`)*

> ### **«Nello spazio vuoto il tempo dovrebbe essere libero di fluire, non fermarsi e rallentare. Dovrebbe rallentare nello spazio vicino alla materia.»**

- **La legge di oggi** *(`FP.cs`: `cs = Lambda / (Lambda + Lambda_c)`)* **lega l'orologio alla densita' del VUOTO:** **anche il vuoto da solo fa da orologio,** **e l'instabilita' di H4 (v0) nasce da li'.** ### **E' un'IPOTESI (di Luca), da confermare con S2, non un fatto** *(S2 dice SE il vuoto con la legge di oggi e' instabile e per quale meccanismo; non dice che una legge senza `Lambda` sarebbe stabile)*.
- **Il riferimento fisico** *(Luca)*: **in relativita', lontano da ogni massa gli orologi vanno al ritmo pieno; rallentano vicino alla materia, e anche INTORNO, con una portata, attraverso un POTENZIALE e non attraverso la densita' locale.**
- **Un fatto gia' scritto che va nella stessa direzione** *(G1 delle note sulla gravita', `doc/TASK_HISTORY/2026-11-09_gravita_note_di_progetto.md` sul principale)*: **con la legge di oggi, al centro del solitone `cs/s` e' `~1` (fino a `~2`)** *(il tempo un po' piu' VELOCE)* **e il rallentamento e' un guscio sul bordo:** **il contrario di un orologio comandato dalla materia.**
- ### ⚠ **Una correzione della citazione del mandato:** **«un `cs` locale non ha portata» non sta in G1** *(G1 e' il fatto del guscio)*: **sta in G3** *(«una legge puramente locale cosi' non puo' dare un effetto che sente tutta la materia intorno»)* **e in G5.3** *(«la mancanza di portata»)*.

### 29.2 IL PRINCIPIO, E LE DUE FORME *(PROPOSTE DEL GUARDIANO; nessuna e' decisa)*

- ### **IL PRINCIPIO** *(dall'osservazione di Luca)*: **nel vuoto puro (`psi = 0`) `cs = s` ESATTAMENTE, per costruzione.** **Il vuoto non fa da orologio, e non puo' destabilizzare il tempo: il rallentamento lo comanda la materia.**
- ### **PROPOSTA (M-rho), la forma LOCALE:** **`cs = s / (1 + rho / rho_c)`**, **`rho` la densita' di materia del nodo** *(`somma |psi|^2` sulle sue estremita')*. **Semplice; a `psi = 0` da' `s` al bit.** ### **Il suo limite:** **rallenta solo DENTRO la materia, non intorno** *(il limite di G3: un `cs` locale non ha portata)*.
- ### **PROPOSTA (M-Phi), la forma CON PORTATA:** **`cs = s (1 + Phi)`**, **`Phi` un potenziale SCALARE che si PROPAGA, con sorgente `rho`** *(un'equazione d'onda sul reticolo)*. **Il rallentamento si estende intorno al solitone e cala con la distanza;** **in 2D ci si aspetta un andamento LOGARITMICO** *(il potenziale di una sorgente puntiforme in due dimensioni; un'attesa, non una misura)*. ### **E' la «gravita' scalare che si propaga» del piano 2D -> 3D** *(G5.1, la gravita' di Nordstrom)*: **tempo locale e gravita' diventerebbero LA STESSA COSA.**

### 29.3 LE DOMANDE APERTE *(senza risposte)*

| | (M-rho) | (M-Phi) |
|---|---|---|
| **il segno e la scala** *(da RICAVARE, non da tarare: `A1`)* | **`rho_c`: da che cosa?** *(una scala del solitone? del vuoto?)* | **l'accoppiamento della sorgente in `Phi`, e la velocita' dell'onda di `Phi`** *(il cono di `1` nodo per tick? `cs` stesso?)*; **il segno: `Phi <= 0` vicino alla materia** |
| **il bilancio dell'energia con `cs` variabile** *(C4: `H dtau`)* | **`cs` dipende da `psi`: il generatore pesato `G` acquista un termine in `psi`** *(come `CAMM-FASE-VUOTO` per `Lambda`)* | **`Phi` e' un campo con la sua energia: entra in `G`?** |
| **il limite `cs >= 0`** | **`cs > 0` per costruzione** *(`rho >= 0`)* | ### **`Phi` puo' portare `cs` a zero? Allora c'e' un ORIZZONTE** *(come nella rampa F3)*: **e' fisica o e' un difetto?** |
| **il rapporto con F1** *(serve ancora una memoria?)* **e con F3/F4** *(la rampa simmetrica ha ancora senso?)* | **senza `Lambda` nella legge, la memoria di F1 serve ancora?** | **`Phi` E' gia' una memoria che si propaga** *(G5.3)*: **F1 si scioglie dentro `Phi`?**; **la rampa di F4 lega `cs` a `Lambda`: con queste forme non c'e' piu' `Lambda` nella legge** |
| **come verificarla per PRIMA** | ### **il vuoto puro deve restare STABILE PER COSTRUZIONE** *(il contrario di (v0)): `cs = s` al bit, nessuna variabile `cs` da linearizzare* | **lo stesso; e poi il profilo di `Phi` attorno a un solitone fermo** *(il logaritmo atteso in 2D)* |

### 29.4 IL LEGAME CON S2

- **Se S2 da' (w4)** *(instabile in tutta la mappa)*: **questa opzione e' la candidata naturale.**
- **Se S2 da' (w3)** *(zone stabili)*: **resta un'alternativa da CONFRONTARE.**
- ### **In ogni caso la scelta e' di LUCA.**

### 28.3 L'ESITO DI S1 *(la corsa dalle `20:10:44` alle `20:18:29` del `2026-11-10`, a `00dedc5b`; il referto `doc/referti_l2/s1_falso_uno.txt`; `5/5`)*: **(z1) IL FALSO-UNO DI F1-V E' CONFERMATO**

- ### **(v0c) ridà (v0) di H4 AL BIT:** **`sha(phi)` di S1 = quello di `h4_vuoto.corsa` rigirato ai tick `200` e `400`** *(`2cd09149fc766d1c`, `2377b9f3cbb34336`)*; **le righe = quelle del referto di H4 al carattere** *(al tick `200` la rms di `Lambda` `1.467e-09`, al `400` `7.313e+00`)*; **il controllo che deve fallire fallisce.**
- ### **(v0a)** *(F3 a fase `1`, senza seme)*: **la rms di `Lambda` resta fra `0` e `1.776e-15` per `1000` tick** *(un ulp di `6` e' `8.88e-16`)*, **senza crescere; `cs` min `0.15` per tutta la corsa.**
- ### **(v0b)** *(lo stesso, seme bianco `1e-14`)*: **cresce col tasso `0.15497` per tick** *(`12` campioni, dal tick `40` al `150`)* **contro `0.15868` di (v0c)** *(dal `160` al `270`)*: **il rapporto `0.97666`, lo scarto `2.3%` (sotto il `5%`).** **(v0c) contro il `0.158` di 27.11: `1.0043`.** **Turbolento dal tick ~`210`; al tick `430` il `59%` dei nodi sotto `cs 1e-2`, come (v0).**
- ### **LA LETTURA COL CRITERIO SCRITTO: (z1).** **Senza seme il vuoto F3 a fase `1` resta uniforme; con un seme di `1e-14` cresce col tasso di (v0): l'instabilita' c'era anche in T2, senza seme.**
- ### ⚠ **DUE CORREZIONI A 27.11, dall'uscita:**
  1. **F3 «a fase `1`» NON ha componenti reali al bit:** **`max |Im phi_v| = 1.225e-16`** *(`e^{i theta_d}` in virgola mobile)*. **Avevo scritto «componenti reali, `+-1`» senza stamparlo.**
  2. **(v0a) NON e' uniforme al bit:** **la rms di `Lambda` e' `0`-`1.8e-15`, cioe' non-uniformita' di un ulp, che NON cresce.** ### **Quindi «senza seme» non vuol dire «non-uniformita' zero»: vuol dire che l'arrotondamento di F3 a fase `1` non ha componente sul modo instabile** *(un'IPOTESI mia, non misurata: S2 dice dove sta il modo; la proiezione dell'arrotondamento su quel modo non l'ho misurata)*, **mentre quello di `c(10000) F3` ce l'ha** *(cresce da ~`5e-15`)*.
- ### **LE CONSEGUENZE DEL FALSO-UNO** *(dal codice, gia' letto in 28.1)*:

| il controllo | la partenza | che cosa diceva | che cosa dice davvero |
|---|---|---|---|
| **F1-V di T2** *(`carta_f1_lunga.py`)* | **`phi_v`, fase `1`, senza seme** | **«F1-V regge»** *(la deriva di `cs` entro un fattore `2`)* | ### **solo che il vuoto SENZA SEME resta uniforme: NON la stabilita'.** **Un FALSO-UNO.** |
| **F1-V di (i)** *(`b1_profilo.py`)* | **lo stesso** | **lo stesso** | ### **lo stesso FALSO-UNO** |
| **F1-V di `d2689b81`** *(`carta_f1.py`, sez. `22`)* | **`phi_v`, fase `1`** | **FALLIVA** *(`cs = s` al bit: `7.8e-16`, la deriva di `Lambda` agli ultimi bit)* | **il suo fallimento era la deriva di un ulp, uniforme: NON l'instabilita'** *(da quella partenza non poteva vederla)* |
| **T1** *(`lambda_vuoto_deriva.py`)* | **`phi_v`, fase `1`, ma `cs` FISSO `0.15` e `lambda_c = None`** | **la deriva di `Lambda` a `cs` spento, `+2.2e-15` per tick** | ### **NON e' toccato:** **senza la legge di `cs` l'instabilita' non c'e' per costruzione** *(H4 (v2) e lo spettro a `cs` spento di S2)*; **il suo risultato resta.** |

  **E una cosa da guardare, non una conclusione:** **la crescita della perturbazione nella scena col solitone delle sez. `20` e `22`** *(`1e-8` -> `6.3e-5` in `200` tick, `5.4e-2` a `1000`)* **potrebbe essere la stessa instabilita'** *(non misurato)*.
- **Il passo successivo: S2** *(lo script, provato dallo scratchpad, si committa dopo la sua suite)*.

### 28.4 S2, DUE ANNOTAZIONI AL PROGETTO PRIMA DELLA CORSA *(28.2 non si riscrive: si annota)*

- ### **(d) L'impulso: `a = 1e-4` relativo, e `R = (4 R(a) - R(2a)) / 3`** *(l'estrapolazione di Richardson, che toglie il termine in `a^2`)*, **invece di `a = 1e-6` con la sola differenza simmetrica.** **Perche':** **una prova breve dallo scratchpad** *(non un referto)* **con `a = 1e-6` dava a `cs` spento `max ||lambda| - 1| = 2.753e-09`, sopra la soglia di Luca `1e-9`, per l'arrotondamento** *(~`1e-16 / 1e-6` per elemento)* **e non per la fisica** *(a `cs` spento la mappa e' lineare: la differenza simmetrica e' esatta a meno dell'arrotondamento)*; **con `1e-4` e Richardson: `2.892e-11`.** **Il controllo di linearita' resta `|R(2a) - R(a)| / max|R|` sotto `1e-6`** *(nella prova: `2.4e-09`-`2.6e-09` coi punti accesi, `3.75e-12` a `cs` spento)*. **E la traslazione si controlla con lo stesso `R` di Richardson.**
- ### ⚠ **LA PROVA BREVE MI HA GIA' MOSTRATO NUMERI** *(il caso di oggi, `Lambda_c 340` e `Lambda 0.1`; l'onda a `60` tick)*: **lo dichiaro.** **Le letture (w1)-(w4) e le soglie sono quelle scritte in 28.2 PRIMA della prova, e non cambiano.** **Il referto e' la corsa al commit dello script, non la prova.**

### 28.5 L'ESITO DI S2 *(la corsa dalle `08:50:31` alle `08:52:51` del `2026-11-11`, a `015f5ee2`; il referto `doc/referti_l2/s2_spettro_vuoto_cs.txt`; `20/20`)*: **(w1) E (w4) -- IL VUOTO CON LA LEGGE DI `cs` E' INSTABILE PER COSTRUZIONE, IN TUTTA LA MAPPA; LA COLPA E' DELLA LEGGE, NON DELLA MEMORIA. FERMO.**

- ### **I DEVE, tutti come devono:**
  - **a `cs` spento lo spettro e' unitario** *(`max ||lambda| - 1| 2.892e-11`)*;
  - **il fattore `1 + 1e-3` compare come `|lambda| = 1.001` su ogni `k`** *(entro `3.0e-11`)*, **e l'unitarieta' su quella mappa FALLISCE come deve;**
  - **`psi` si stacca** *(le risposte incrociate `0` esatto; il blocco `psi -> psi` unitario)*;
  - **la traslazione `5.334e-12`; la linearita' `2.1e-09`-`4.1e-09` su tutti i punti;**
  - **oggi (L-F1) `ln |lambda|_max = 0.160987` contro `0.158`** *(il rapporto `1.0189`)*;
  - ### **l'onda piana nella simulazione F1 vera cresce a `0.16099` per tick** *(dal tick `20` al `100`; il rapporto con lo spettro `1.0000`)*.
  - **I residui delle basi sono `<= 4.9e-15`: tutti i punti sono punti fissi.**
- ### **IL MODO:** **in TUTTI i `24` casi il `k` piu' instabile e' `(m1, m2) = (27, 27)`, `|k| = 4.18879 = 4 pi / 3`, con il suo opposto** *(`2` `k` equivalenti)*.
  - **E' l'angolo della zona di Brillouin del reticolo triangolare** *(il modulo `4 pi / 3` e' quello del punto `K`; la lettura «punto `K`» e' mia)*.
  - **L'autovalore e' REALE** *(`arg 0`)*: **nel riferimento che gira, il modo cresce senza oscillare.**
- ### **LA MAPPA** *(`ln |lambda|_max` per tick; (L-F1) e (L-ist))*:

| il punto | `Lambda` | `Lambda_c` | `cs` del vuoto | (L-F1) | (L-ist) |
|---|---|---|---|---|---|
| `Lambda_c 8.5` | `6` | `8.5` | `0.4138` | `0.139276` | `0.181390` |
| `Lambda_c 17` | `6` | `17` | `0.2609` | `0.218835` | `0.276258` |
| **oggi** | `6` | `34` | `0.1500` | **`0.160987`** | **`0.211198`** |
| `Lambda_c 68` | `6` | `68` | `0.0811` | `0.096343` | `0.131230` |
| `Lambda_c 136` | `6` | `136` | `0.0423` | `0.052583` | `0.073490` |
| `Lambda_c 340` | `6` | `340` | `0.0173` | `0.022153` | `0.031535` |
| `s 0.05` | `6` | `114` | `0.0500` | `0.061685` | `0.085748` |
| `s 0.3` | `6` | `14` | `0.3000` | `0.221038` | `0.277441` |
| `Lambda 3` | `3` | `34` | `0.0811` | `0.096343` | `0.131230` |
| `Lambda 1` | `1` | `34` | `0.0286` | `0.036083` | `0.050931` |
| `Lambda 0.5` | `0.5` | `34` | `0.0145` | `0.018567` | `0.026488` |
| `Lambda 0.1` | `0.1` | `34` | `0.0029` | `0.003799` | `0.005470` |

  - **Instabili `24` su `24`** *(la soglia `1e-9`)*. **Nessuna zona stabile: NON (w3).**
  - ### **Un fatto della tabella** *(non una lettura)*:
    - **`Lambda_c 68` e `Lambda 3` hanno lo STESSO `cs` del vuoto** *(`0.0811`)* **e lo stesso tasso fino alla `12`ma cifra** *(`0.096343` per tutti e due i casi)*: **in questi punti il tasso dipende da `Lambda / Lambda_c`, non dai due separati.**
    - **Il tasso cresce con `cs` del vuoto fino a `0.26`-`0.30`** *(`0.2188`, `0.2210`)* **e scende a `0.41`** *(`0.1393`)*.
    - **Verso `cs -> 0` va a zero** *(`0.0038` a `cs 0.0029`)*, **ma non diventa mai stabile.**
  - ### **Una cosa da segnalare, non da interpretare:** **a `k = 0` `|lambda|` e' sopra `1` in quattro punti:**
    - `1.0000019` a `Lambda_c 17`;
    - `1.0000010` a `s 0.05`;
    - `1.0000008` a `Lambda 3`;
    - `1.0000006` a `Lambda 0.5`.

    **Negli altri punti e' `1 + O(1e-11)`.** **Questi valori stanno sopra la precisione dello strumento a `cs` spento** *(`2.9e-11`)*, **ma molto sotto il modo a `K`.** **Non so se sia un modo vero o l'arrotondamento del modo neutro a `k = 0`.**
- ### **IL MECCANISMO, letto dalla matrice nel caso di oggi:**
  - **L'autovettore e' quasi tutto `phi`** *(`99.61%`; `cs` `0.39%`)*, **diviso a meta' fra le due bande di `phi` a `omega_b = +-0.237260`** *(`0.4976` e `0.4976`)*. **E' una sovrapposizione delle due onde a `+K` e `-K` che modula `|phi|^2`, cioe' `Lambda`, sul passo del reticolo** *(lettura mia della composizione)*.
  - **`lambda - A_cc = g(lambda)` regge** *(lo scarto `3.2e-15`)*: **(L-F1) `A_cc = 0.6499`, `g = 0.5248`; (L-ist) `A_cc = 0.0682`, `g = 1.1670`.**
  - **`g` e' REALE e POSITIVO, e il `96%` viene dalle due bande `+-0.237260`** *(`0.2527 + 0.2527` su `0.5248`)*: **l'anello `phi -> Lambda -> cs -> phi` si chiude IN FASE, una retroazione positiva.**
  - **Le due braccia dell'anello:** **`|A_phi,c| = 5.03`** *(quanto un `delta cs` sposta `phi`)*, **contro `|A_c,phi| = 0.039`** *(F1)* **e `0.104`** *(ist)*.
  - ### **Perche' la memoria non salva:** **la memoria di F1 abbassa `A_c,phi`** *(da `0.104` a `0.039`)* **ma porta `A_cc` a `0.65`, vicino a `1`:** **il guadagno dell'anello resta sopra la soglia** *(il tasso scende da `0.211` a `0.161`, non a zero)*. **In tutta la mappa (L-F1) e' piu' lento di (L-ist), mai stabile.**
- ### **LE LETTURE COL CRITERIO SCRITTO:**
  - ### **(w1): (L-ist) e' gia' instabile nel caso di oggi** *(`0.211198` per tick)*: **la colpa e' della LEGGE, non della memoria;**
  - ### **(w4): instabile in tutta la mappa** *(`24` su `24`)*: **il vuoto con questa legge del tempo locale e' instabile per costruzione.**
- ### ⛔ **FERMO** *(il mandato: «dopo S2: fermo»)*.
  - **F4, la forma della legge, e qualunque cambio di `Lambda_c` o di `s` sono di Luca.**
  - **Per la ROTTA** *(`doc/ROTTA.md`, passo `1`)*: **S2 chiude la diagnosi; (w3) non c'e', quindi F1-F4 si archiviano.**
  - **La sez. `29`** *(M-rho, M-Phi)* **e' la candidata naturale per (w4), come scritto li': la scelta e' di Luca.**

### 28.6 IL RIMANDO ALLA ROTTA *(la regola `2`)*

- **La rotta del tempo locale e dell'unificazione** *(Luca `2026-11-10` `20:08`)* **e' `doc/ROTTA.md` sul principale** *(`4f8bb34b`)*.
- **Su questo ramo:** **dopo S2 nessuna nuova cura della legge sul vuoto, e F1-F4 sono archiviate** *(S2 non ha trovato zone stabili)*.

## 30. S4, LA LEGGE M-rho HA UN'INSTABILITA' NELLA MATERIA? *(Luca `2026-11-11` `09:17`)*: **S4.0, PRIMA DEL CODICE**

**SOLO uno studio di stabilita' lineare:** **nessuna modifica al nucleo, nessuna corsa lunga, nessuna scelta di `rho_c`** *(la scansione e' una MAPPA)*. **M-rho e' ISTANTANEA** *(F1-F4 archiviate)*. **Lo strumento e' quello di S2, esteso a `psi`.** **Il codice si committa PRIMA di qualunque esecuzione, senza prove fuori dal repo** *(il criterio di Luca, e il mio errore di S2)*.

### 30.1 (a) IL FONDO DI MATERIA UNIFORME *(dal codice)*

- ### **LA BANDA DEI SOLITONI, dal codice:** **`_consolida_B.coppia` prende `A[0, 0]`, cioe' il blocco del tick di `psi` a `k = 0` (`Gamma`), e ne tiene le DUE bande piu' alte** *(`E = -arg lambda / S`, gli ultimi due dopo l'ordinamento)*, **ortonormalizzate (`q1`, `q2`).** **Il solitone BG e' l'inviluppo di `q = cos theta q1 + e^{i phi} sin theta q2`, con `theta`, `phi` dal minimo di `griglia.json` a `eps 0.5`** *(`theta = pi/4`, `phi = 5 pi / 4`)*. **La coppia e' degenere entro `~1e-15`** *(`degenere` nei referti: `8.9e-16`-`5.3e-15`)*, **quindi `q` e' un autovettore.**
- ### **IL FONDO:** **`psi_0` = `sqrt(rho_0) q` in OGNI cella, con `|q| = 1`.** **Ogni nodo riceve un'estremita' di ciascuno dei `6` posti della cella** *(i tre archi in uscita e i tre in entrata)*: **quindi `rho` per nodo = `rho_0 |q|^2 = rho_0` esatto** *(stampato: il min e il max di `rho`)*. **`phi_0` = `c F3`, il vuoto di S2** *(`Lambda = 6`)*. **`rho_0` e' in unita' della norma per nodo, la stessa di `Lambda`.**
- ### **`q1`, `q2` si RICALCOLANO in ogni punto:** **il blocco `M` di `psi` a `Gamma` cambia col `cs` del punto** *(`cs = cs(rho_0)` uniforme moltiplica i tempi dei pezzi)*: **`M` dalle colonne `tick(sqrt(rho_0) e_c) / sqrt(rho_0)`** *(un `psi` uniforme con una sola componente ha ancora `rho = rho_0` per nodo, quindi il `cs` e la fase della materia sono quelli del fondo)*, **le due bande piu' alte come in `coppia`, la stessa combinazione `theta`, `phi`.**
- ### **DUE FASI:** **`CAMM-MATERIA-VUOTO`** *(la forma `S1` della scena: `alpha = x^2/(1+x^2)` su `psi`, `beta = x - arctan x - x^3/(1+x^2)` su `phi`, `x = rho / Lambda`)* **mette fasi DIVERSE su `psi` e su `phi`, e i pezzi di `psi` e di `phi` girano con frequenze diverse:** **il riferimento che gira ha DUE fasi, `u_psi` e `u_phi`, misurate sulla base** *(`<psi_0, psi_1>` e `<phi_0, phi_1>`, un tick)*. ### **Il residuo della base** *(`|u_psi^* psi_1 - psi_0| / max|psi_0|`, e lo stesso per `phi`)* **DEVE stare sotto `1e-12`** *(Luca)*: **se non ci sta, (m4): FERMO prima dello spettro.**
- **I flussi materia-vuoto sono FASI esatte** *(la scheda: «una fase NON CAMBIA ne' `rho` ne' `Lambda`»)*: **non spostano norma, quindi un fondo uniforme PUO' essere un punto fisso.** **Lo dice il residuo, non io.**

### 30.2 (b) LE VARIABILI, E LA LEGGE M-rho NELLA MAPPA

- **`psi`: `24` reali per cella; `phi`: `12`. `36` in tutto.** **`cs` NON e' una variabile.**
- ### **M-rho, come la scrivo nella mappa** *(scelte MIE, dichiarate)*:
  - **`cs_k = s / (1 + rho_k / rho_c)`, con `rho_k` dallo stato all'INIZIO del tick** *(la legge istantanea, come (L-ist) di S2)*;
  - **`mot.cs` = quel vettore, `mot.lambda_c = None`:** **cosi' `CAMM-FASE-VUOTO` non c'e'** *(e' la derivata della legge su `Lambda`, che qui non esiste)*. ### **Il termine analogo per M-rho** *(il gradiente di `G` attraverso `cs(rho)`, una fase su `psi`)* **NON ESISTE nel codice, e qui non lo scrivo:** **e' una mancanza dichiarata** *(come (q2) per F1)*.
- **«La legge spenta» del mandato:** **`mot.cs = s` ovunque, `mot.lambda_c = None`** *(come T1)*.
- **«Il `cs` congelato»** *(mio, per il meccanismo)*: **`mot.cs = cs(rho_0)` uniforme e costante.** **E' la mappa M-rho SENZA l'anello:** **la differenza fra le due e' il pezzo che passa per `cs`.**

### 30.3 (c) LA MAPPA

- **`rho_0 / rho_c` in `{1e-3, 1e-2, 1e-1, 1, 10}`; `rho_0` in `{1e-4, 1e-2, 1}`; `s` in `{0.05, 0.15, 0.3}`: `45` punti.** **Tutte le combinazioni hanno senso col codice** *(`rho_c = rho_0 / rapporto > 0`)*. **Per ogni punto: M-rho e il `cs` congelato** *(`90` linearizzazioni)*; **per ogni (`rho_0`, `s`): la legge spenta** *(`9`)*; **`rho_0 = 0` con M-rho per ogni `s`** *(`3`)*.

### 30.4 S4.1, LO SPETTRO, I DEVE, IL MECCANISMO

- **Come S2:** **la risposta a un impulso nella cella del nodo `0` per ognuna delle `36` direzioni, differenze simmetriche con Richardson, `a = 1e-4` per la scala del blocco** *(`psi`: la rms delle componenti di `psi_0` della cella; `phi`: `|phi|` per estremita'; a `rho_0 = 0` per `psi` la scala di `phi`)*; **`A(k)` con `fft2`, `36 x 36` per ogni `k`.** **Per ogni punto: `|lambda|_max`, `ln |lambda|_max`, il `k`** *(`|k|`, la direzione, quanti equivalenti)*, **la frazione dell'autovettore in `psi` e in `phi`, la banda** *(i pesi sugli autovettori del blocco del `cs` congelato allo stesso `k`)*.
- ### **IL MECCANISMO** *(l'anello `rho -> cs -> (psi, phi) -> rho`)*: **il `cs` entra solo come un numero per nodo, quindi `A(k) = F(k) + P(k) Q(k)`:** **`F` il `cs` congelato; `P` (`36 x 1`) la risposta a un impulso di `cs` nel nodo `0`** *(misurata, Richardson)*; **`Q` (`1 x 36`) la risposta di `cs` del nodo a un impulso dello stato** *(dalla legge, con differenze simmetriche)*. **Un controllo:** **`|A - F - P Q| / |A|` al `k` piu' instabile sotto `1e-6`.** **L'autovalore soddisfa `Q (lambda - F)^{-1} P = 1`; il guadagno `g(lambda) = Q (lambda - F)^{-1} P` si scompone per bande di `F`, come in S2.**
- **I DEVE** *(Luca)*:
  - **`rho_0 = 0` con M-rho: lo spettro e' unitario entro la precisione di S2** *(`max ||lambda| - 1| < 1e-10`; S2 dava `2.9e-11`)*: **il vuoto stabile per costruzione;**
  - **la legge spenta (`cs = s`), `rho_0 > 0`: lo spettro e' unitario** *(la stessa soglia)*: **la materia senza orologio e' stabile;**
  - **un'onda piana seminata nella simulazione sul `k` piu' instabile** *(se c'e')*: **cresce col tasso dello spettro entro il `5%`** *(`100` tick, M-rho vera, un gemello; la pendenza dal tick `20`; al punto piu' instabile della mappa)*;
  - **DEVE FALLIRE:** **il fattore `1 + 1e-3` su `psi` e `phi` dopo il tick** *(a `rho_0 = 0`, M-rho)* **compare come `|lambda| = 1.001`** *(entro `1e-9`)*, **e l'unitarieta' su quella mappa fallisce.**
  - **I controlli di S2:** **la linearita' `|R(2a) - R(a)| / max|R| < 1e-6` per ogni linearizzazione;** **l'invarianza per traslazione** *(un impulso in un altro nodo, al punto di mezzo della mappa)*.
- ### ⚠ **UNA COSA CHE MI ASPETTO, scritta prima** *(un'ATTESA, non una misura)*: **il fondo di materia ha gia' una fase che dipende da `rho`** *(`alpha = x^2/(1+x^2)`, una auto-fase)*. **Se e' FOCALIZZANTE** *(e i solitoni brillanti esistono: e' il caso tipico)*, **un fondo uniforme e' instabile per MODULAZIONE anche senza orologio** *(l'instabilita' di Benjamin-Feir, nell'equazione di Schrodinger non lineare)*. ### **Allora il DEVE «la legge spenta e' unitaria» FALLIREBBE.** **Se fallisce:** **lo committo, riporto lo spettro di tutti e tre i casi** *(spenta, congelato, M-rho)* **e la differenza M-rho meno congelato, e mi FERMO senza leggere (m1)-(m3)** *(che presuppongono un riferimento stabile)*.
- ### **LE LETTURE** *(di Luca; «stabile» = `|lambda|_max - 1 < 1e-9`)*:
  - **(m1)** **stabile in tutta la mappa:** **M-rho passa la prova lineare nella materia;**
  - **(m2)** **instabile solo oltre una soglia di `rho_0 / rho_c`** *(per ogni `rho_0`, `s`: stabile sotto, instabile sopra)*: **la soglia, il `k`, la banda;**
  - **(m3)** **instabile in tutta la mappa:** **anche l'anello nella materia si chiude in fase. FERMO: la decisione e' di Luca;**
  - **(m4)** **il fondo uniforme non e' un punto fisso:** **FERMO prima dello spettro.**
- **Il costo** *(stima, `~0.14` s per tick da S2)*: **`~160` tick per linearizzazione, `~103` linearizzazioni: ~`40` minuti, un processo.** **Il referto `doc/referti_l2/s4_spettro_materia_mrho.txt`; lo script `csv/solitone/s4_materia_mrho.py`.**
- ### **DOPO S4: FERMO.** **La scelta di `rho_c` e il passo dopo sono di Luca.**

### 30.5 L'ESITO DI S4 *(la corsa dalle `09:54:51` alle `10:28:39` del `2026-11-11`, a `e51dd24c`; il referto `doc/referti_l2/s4_spettro_materia_mrho.txt`; `102/116`, exit `1`)*: **LA LEGGE SPENTA NON E' UNITARIA (L'INSTABILITA' DI MODULAZIONE ATTESA, A `rho_0 = 1`): (m1)-(m3) NON SI LEGGONO. M-rho INSTABILE IN `45` PUNTI SU `45`. E UN DIFETTO MIO NEL CONTROLLO `A = F + P Q`. FERMO.**

- ### **Che cosa passa:**
  - **ogni base e' un punto fisso** *(il residuo piu' grande `7.6e-15`)*: **NON (m4);**
  - ### **il vuoto con M-rho e' unitario** *(`rho_0 = 0`: `1.8e-11`, `1.9e-11`, `1.2e-11` a `s` `0.05`, `0.15`, `0.3`)*: **il vuoto stabile per costruzione, alla prova lineare;**
  - **il fattore `1.001`** *(entro `1.7e-11`)* **e il DEVE FALLIRE;**
  - **la linearita' e la traslazione;**
  - ### **l'onda piana:** **al punto piu' instabile della mappa** *(`rho_0 1`, `rho_0/rho_c 1e-3`, `s 0.3`, `k (4, 2)`)* **cresce a `1.467927e-02` per tick contro lo spettro `1.467819e-02`** *(il rapporto `1.0001`)*.
- ### **Che cosa fallisce, `14`:**
  - ### **LA LEGGE SPENTA, `6` su `9`:**
    - **a `rho_0 = 1`, nettamente:** **`ln |lambda|_max` `2.601e-03`, `7.808e-03`, `1.562e-02` per tick a `s` `0.05`, `0.15`, `0.3`;** **a `|k| 0.4987`** *(`12` `k` equivalenti)*, **l'autovettore per il `77%` in `psi`.** ### **E' l'instabilita' di MODULAZIONE del fondo di materia, SENZA orologio, che avevo scritto come attesa in 30.4:** **la materia del solitone ha un'auto-fase focalizzante.**
    - **a `rho_0 = 0.01`** *(`s 0.15`, `0.3`)*: **`2.4e-09` e `2.3e-09`, a `k = 0`** *(un solo `k`; il `96%`-`99%` in `psi`)*; **a `rho_0 = 1e-4`, `s 0.3`: `1.03e-10`, appena sopra la soglia.** **Non so se siano modi veri o il modo neutro di `k = 0` arrotondato** *(come i `1.000001` di S2 a `k = 0`)*.
  - ### **`A = F + P Q`, `8` su `45`:** **tutti a `rho_0 = 1`, `s 0.15` e `0.3`** *(fino a `8.5e-03`)*; **gli altri `37` passano** *(fino a `3e-10`)*. ### **UN DIFETTO MIO, probabilmente** *(un'ipotesi, NON verificata)*: **`q` e' una combinazione della COPPIA DEGENERE, e la base della coppia viene da `np.linalg.eig`, che dentro un autospazio degenere non e' unica.** **La base di M-rho e quella del `cs` congelato possono avere un `q` DIVERSO** *(lo stesso autospazio, un altro vettore)*: **dove la non linearita' conta** *(`rho_0 = 1`)*, **`F` e' linearizzata attorno a un altro fondo.** ### **Quindi a `rho_0 = 1` la colonna «M-rho - congelato» e la scomposizione per bande NON valgono;** **lo spettro di ciascuna mappa vale per il SUO fondo.** **La cura** *(da decidere)*: **fissare `q` in modo univoco dentro la coppia** *(per esempio con gli autostati di `sigma_z`, come il ritratto di `griglia.json`)*.
- ### **LA MAPPA** *(`ln |lambda|_max` per tick, il referto)*: **M-rho e' instabile in `45` punti su `45`.** **Dove la legge spenta e il congelato sono unitari** *(`rho_0` `1e-4` e `1e-2`)*, **l'instabilita' viene dall'anello di `cs`:**

| `rho_0 / rho_c` | `s 0.05` | `s 0.15` | `s 0.3` |
|---|---|---|---|
| `1e-3` | `3.49e-06` | `3.11e-05` | `1.20e-04` |
| `1e-2` | `3.39e-05` | `3.02e-04` | `1.17e-03` |
| `1e-1` | `2.59e-04` | `2.31e-03` | `8.95e-03` |
| `1` | `3.92e-04` | `3.52e-03` | `1.39e-02` |
| `10` | `2.10e-05` | `1.89e-04` | `7.56e-04` |

  - ### **Un fatto della tabella:** **a `rho_0 = 1e-4` e a `rho_0 = 1e-2` il tasso e' lo STESSO alla terza cifra** *(per esempio `3.49006e-06` e `3.48964e-06`; `3.51812e-03` e `3.51813e-03`)*: **dipende da `rho_0 / rho_c` e da `s`, NON dalla quantita' di materia.** **Anche una materia rarissima destabilizza, se il rallentamento che comanda e' forte.**
  - **Il modo:** **`|k|` fra `3.18` e `4.19`** *(vicino all'angolo `4 pi / 3` di S2, non sempre su di esso)*; **l'autovalore COMPLESSO** *(il modo oscilla)*; ### **l'autovettore e' quasi tutto `phi`** *(la frazione in `psi` `0.000`-`0.01`; `0.41`-`0.50` solo a `rho_0/rho_c = 1e-3`, `rho_0 = 1e-2`)*.
  - ### **Il meccanismo, dove `A = F + P Q` regge** *(`rho_0 1e-2`, `rho_0/rho_c 1`, `s 0.05`: lo scarto `3.1e-10`; `g(lambda) = 1.0000`)*: **il `96%` dell'autovettore sta in UNA banda di `phi`** *(`omega_b -0.0392`)*, **e quella banda da' il contributo maggiore a `g`** *(`+1.29`, contro `-0.24` della banda opposta)*: **il `cs` comandato da `rho` muove la fase di `phi`** *(`|P| = 5.1`)*, **e `phi` torna su `rho` attraverso la fase della materia** *(`CAMM-MATERIA-VUOTO`)*. **Una lettura mia della matrice, non una dimostrazione.**
  - **A `rho_0 = 1` la tabella e' dominata dall'instabilita' di modulazione** *(la legge spenta: `2.6e-3`-`1.56e-2`)*; **M-rho la ABBASSA in `14` punti su `15`** *(sale solo a `rho_0/rho_c 1`, `s 0.3`: `+6.2e-03`)* *(la differenza M-rho meno congelato e' negativa, ma vedi il difetto sopra)*.
- ### **LE LETTURE COL CRITERIO SCRITTO (30.4):** **la legge spenta non e' unitaria, quindi (m1)-(m3) NON si leggono.** **Fuori dal criterio, i fatti:** **M-rho e' instabile in tutta la mappa, anche dove la materia senza orologio e' stabile;** **il tasso va col rapporto `rho_0/rho_c` e con `s`, ed e' massimo a `rho_0/rho_c ~ 1`.**
- ### ⛔ **FERMO** *(il mandato: «dopo S4: fermo»; e i DEVE falliti si committano e ci si ferma)*. **Le domande a Luca:**
  1. **la cura del mio difetto** *(`q` univoco dentro la coppia)* **e il rifacimento dei punti a `rho_0 = 1`?**
  2. **la legge spenta a `rho_0 = 1` e' instabile per modulazione:** **il riferimento giusto per M-rho e' il `cs` congelato allo stesso `cs`, non la legge spenta?** *(la sez. 30 l'ha gia' misurato accanto)*
  3. **M-rho istantanea ha un anello in fase attraverso la fase della materia:** **la scelta di `rho_c` e il passo dopo sono suoi.**

### 30.6 S4.6: LE DUE INSTABILITA' DI S4, SEPARATE *(Luca `2026-11-11` `11:33`)*

| | (I-mod) | (I-cs) |
|---|---|---|
| **che cos'e'** | **la modulazione della materia SENZA orologio** | **l'anello dell'orologio M-rho** |
| **dove** | **`rho_0 = 1`** *(la legge spenta e il congelato)* | **anche dove (I-mod) non c'e'** *(`rho_0` `1e-4`, `1e-2`)* |
| **il `k`** | **`|k| 0.4987`** *(`12` equivalenti)* | **vicino a `K`** *(`|k|` `3.2`-`4.2`)* |
| **l'autovettore** | **il `77%` in `psi`** | **quasi tutto in `phi`** |
| **il tasso** | **cresce con `s`** *(`2.6e-3`, `7.8e-3`, `1.56e-2`)* | **dipende da `rho_0 / rho_c` e `s`, NON da `rho_0`** |
| ### **il giudizio** *(Luca)* | ### **CORRETTA: e' l'origine dei solitoni** | ### **NON fisica** |

- ### **IL CRITERIO PER IL FUTURO** *(Luca: la firma di un'instabilita' fisica accettabile, tipo Jeans)*: **su scale LUNGHE** *(`k` piccolo)*; **piu' rapida dove c'e' PIU' materia; l'autovettore nella MATERIA.** **(I-cs) li viola tutti e tre.**
- ### **L'ERRORE DEL GUARDIANO (n.`135`)** *(scritto da Luca)*: **il DEVE «la legge spenta e' unitaria» era SBAGLIATO:** **la materia senza orologio ha (I-mod), che e' fisica.** ### **Il riferimento giusto e' il `cs` CONGELATO.** **L'attesa l'avevo scritta io stesso in 30.4, e il DEVE l'ho tenuto lo stesso:** **un DEVE contro la propria premessa.**
- ### **LE RISPOSTE DI LUCA alle tre domande di 30.5:**
  1. **lo strumento si cura** *(S4.7)*;
  2. **il riferimento e' il congelato;**
  3. **`rho_c` NON si sceglie** *(si scansiona come mappa)*.
- ### **LA DIAGNOSI DEL GUARDIANO, accolta da Luca** *(`11:33`)*: **l'orologio di oggi agisce A SENSO UNICO:** **la materia rallenta il tempo del vuoto senza nessuna reazione su di se', quindi la dinamica non viene da un'energia conservata, e l'anello fa da POMPA** *(una risonanza parametrica: l'autovalore complesso)*. **La decisione di Luca: l'orologio che CONSERVA L'ENERGIA PER COSTRUZIONE** *(S5, sez. `31`)*.

### 30.7 S4.7: LA CURA DELLO STRUMENTO *(prima di S5)*: **IL PROGETTO, PRIMA DEL CODICE**

- ### **`q` UNICO:** **in ogni punto (`rho_0`, `rho_0/rho_c`, `s`) `q` si calcola UNA volta** *(sulla mappa M-rho, come in 30.1)* **e il fondo `psi_0` si passa IDENTICO al `cs` congelato** *(lo stesso array)*: **lo scarto fra le due basi e' `0`** *(stampato; il DEVE: sotto `1e-14`)*. **Il residuo della base del congelato si ricontrolla col SUO tick** *(sotto `1e-12`)*.
- **Lo script `csv/solitone/s4_materia_mrho.py` si cambia** *(il referto di 30.5 resta rigirabile a `e51dd24c`)*: **un argomento `--v2`** *(il fondo unico; niente legge spenta, che non e' il riferimento)*; **il referto NUOVO `doc/referti_l2/s4_spettro_materia_mrho_v2.txt`, accanto al primo.**
- **Si rifanno TUTTI i `45` punti** *(anche `1e-4` e `1e-2`, per il DEVE)*, **con la colonna «M-rho meno congelato».**
- **I DEVE:**
  - **`A = F + P Q` sotto `1e-6` in TUTTI i `45` punti;**
  - **lo scarto fra le basi di M-rho e del congelato sotto `1e-14`** *(per costruzione `0`)*;
  - ### **i punti a `rho_0` `1e-4` e `1e-2` ridanno 30.5 alla terza cifra:** **`ln |lambda|_max` di M-rho, letto dalla tabella del referto di 30.5, entro `1e-3` relativo** *(il mio modo di dire «alla terza cifra»)*;
  - **DEVE FALLIRE:** **lo stesso confronto contro la riga di un altro punto** *(lo strumento sa dire di no)*;
  - **restano: le basi, il vuoto con M-rho unitario, il fattore `1.001`, la linearita', la traslazione.**
- **Non c'e' una lettura nuova:** **S4.7 cura uno strumento; i numeri a `rho_0 = 1` si riportano, e la colonna «M-rho meno congelato» dice quanto (I-cs) aggiunge sopra (I-mod).**

## 31. S5, L'OROLOGIO CHE CONSERVA L'ENERGIA *(Luca `2026-11-11` `11:33`; l'aggiunta (e) delle `11:46`)*: **S5.0, IL PROGETTO SU CARTA, PRIMA DEL CODICE**

**Il banco e' FUORI dal nucleo; il nucleo non si tocca; nessuna taratura** *(`rho_c` come mappa)*. **Le fermate:** **se (a) fallisce; se (e) trova un'energia non limitata dal basso; se una lettura lo dice; comunque dopo S5.2.**

### 31.1 (a) L'ENERGIA DEL TICK DI OGGI, PEZZO PER PEZZO *(dal codice: `primo_ordine/energia_pesata.py`, `termini_di_h`; `flussi_parziali.py`)*

| il pezzo (`composizione.ORDINE`) | il generatore locale | il peso (il «lapse» di oggi) |
|---|---|---|
| **`CAMM-GROVER`** *(`psi`, nodo)* | **`-pi (N_k/2 - P_k)`** *(lo zero simmetrico O1: `0.5 nrm_psi - |somma_h psi_h|^2 / d`)* | **`cs_k`** *(`z_nodo`)* |
| **`CAMM-GROVER-VUOTO`** *(`phi`, nodo)* | **lo stesso su `phi`** | **`cs_k`** |
| **`CAMM-MONETA-SPIN`** *(`psi`, nodo)* | **`eps * elicita_k`** *(`eps` dal `par`)* | **`cs_k`** *(`dtau_nodo`)* |
| **`CAMM-MATERIA-VUOTO`** *(nodo)* | **`N_k = Lambda_k (x - arctan x)`, `x = rho_k / Lambda_k`** *(la forma `S1`)* | **`cs_k`** |
| **`CAMM-SPOSTAMENTO`** *(`psi`, arco)* | **`pi Re <psi_0 | U | psi_1>`** | **`w_a`, la media ARMONICA dei due `cs`** *(`s_arco`, `B-3`)* |
| **`CAMM-SPOSTAMENTO-VUOTO`** *(`phi`, arco)* | **`pi Re (conj phi_0 phi_1)`** | **`w_a`** |
| **`CAMM-FASE-VUOTO`** *(`phi`, nodo)* | ### **NON e' un addendo di `H`: e' la parte del gradiente di `G` che passa per i PESI** *(`Omega_k phi_h`, quando `cs = cs(Lambda)`)* | **assente a `mot.lambda_c = None`** |

- ### **(a) REGGE: ogni pezzo ha un generatore LOCALE** *(di nodo o di arco)*, **e l'energia del tick e' gia' scritta nel nucleo come**
  **`G = somma_k cs_k H_k(nodo) + somma_a w_a H_a(arco)`** *(la decisione di Luca del `2026-10-18` `00:07`; il modulo e' «l'unica fonte dei termini di `H`»)*. **Il controllo esiste gia':** **`hw_energia_pesata.txt` (0): a forma spenta `H_w = h_tot` entro `0.7` ulp.**
- ### ⭐ **UNA SCOPERTA DAL CODICE, da dire a Luca:** **il nucleo ha GIA' l'orologio che conserva l'energia per la legge su `Lambda`:** **`tick.tick_con_cs`** *(`cs` al centro del palindromo, a punto fisso)* **piu' `CAMM-FASE-VUOTO`** *(la reazione `dG/dphi*` attraverso `cs(Lambda)`)*. ### **S2, H4 e F1 hanno girato con (q2), cioe' con `cs_primo = 0`: la reazione SPENTA.** **L'orologio a senso unico misurato in S2 NON e' la legge del nucleo:** **la legge del nucleo, con la sua reazione, sul vuoto non e' mai stata provata** *(in 28.2 l'avevo scritto: «un ALTRO oggetto, qui NON si misura»)*.

### 31.2 (b) LA FORMA COL LAPSE

- **`E_N = somma_k s N_k H_k(nodo) + somma_a w_a(s N) H_a(arco)`, cioe' `cs_k = s N_k`.** **`N(rho) = 1 / (1 + rho / rho_c)`** *(la forma di M-rho)*, **`N = 1` esatto dove `psi = 0`.**
- ### **L'ARCO: il mandato propone la media aritmetica o la geometrica. I pezzi del nucleo usano la media ARMONICA** *(`FP.s_arco`, scritta `S/2 - D^2/(2S)` perche' dia `d` al bit quando i due capi sono uguali)*. **Tutte e tre mantengono l'hermiticita'** *(`w_a` e' un numero reale, simmetrico nei due capi, che moltiplica un `H_a` hermitiano)*. ### **Ma usare l'aritmetica o la geometrica vorrebbe dire cambiare `FP.s_arco` (il nucleo: VIETATO) o riscrivere il peso fuori dal nucleo (una SECONDA FONTE della legge: `STRUMENTO-LEGGE-DALLA-TABELLA`).** **La proposta: l'ARMONICA del nucleo** *(e la sua derivata c'e' gia': `energia_pesata.d_peso_arco`, verificata a `1.3e-07`)*. **Una decisione di Luca.**

### 31.3 (c) LE EQUAZIONI DA `E_N` *(per esteso, nel discreto)*

- **Il vuoto:** **`i d phi_h / d tau = dE_N / d phi*_h`:** **i pezzi del vuoto coi pesi `s N`** *(Grover-vuoto `cs_k`, spostamento-vuoto `w_a`, la fase `beta` di `CAMM-MATERIA-VUOTO` pesata `cs_k`)*; **nessuna reazione, perche' `N` non dipende da `Lambda`.**
- **La materia:** **`i d psi_h / d tau = (i pezzi della materia coi pesi `s N`) + Omega^psi_k psi_h`**, **con**
  **`Omega^psi_k = s N'(rho_k) [ H_k(nodo) + somma_{a in k} (dw_a / dcs_k) H_a(arco) ]`, `N'(rho) = -(1/rho_c) / (1 + rho/rho_c)^2`.**
  - ### **E' il termine di reazione** *(`dN/drho` `h`)*: **una FASE uguale per tutte le estremita' del nodo, la stessa forma di `CAMM-FASE-VUOTO` con `rho` al posto di `Lambda` e `psi` al posto di `phi`.** **Non cambia `rho`** *(e' una fase)*; **la forza nasce dalla fase che dipende dal posto:** **un pacchetto sente `Omega^psi` come un potenziale `V_k = s N'(rho) h_k`.**
  - ### ⚠ **IL VERSO DELLA FORZA DIPENDE DAL SEGNO DI `h_k`, quindi dallo ZERO dell'energia** *(O1 o O4)*: **con `h_k > 0` la materia scende verso `N` piu' basso; con `h_k < 0`, verso `N` piu' alto.** **E' la domanda (1) di (e).**

### 31.4 (d) LO SCHEMA CHE CONSERVA `E_N`

| | il palindromo con `N` a meta' passo *(come `tick_con_cs`, punto fisso a `8` ulp)* + la reazione col punto medio implicito *(come `CAMM-FASE-VUOTO`)* | un gradiente discreto *(per esempio il campo vettoriale medio)* |
|---|---|---|
| **la norma** | **esatta all'arrotondamento** *(pezzi unitari e fasi pure)* | **NON esatta in generale** |
| **reversibile** | **si'** *(palindromo, punto medio simmetrico)* | **si'** *(se simmetrico)* |
| **`E_N`** | ### **NON al bit: l'errore e' `O(dtau^2)`, limitato, senza deriva** | **al bit** *(a meno dell'arrotondamento)* |
| **dai pezzi del nucleo** | **si'** | ### **NO:** **una soluzione implicita globale; il nucleo non ha i pezzi per farlo** |

- ### ⛔ **IL PUNTO DA DIRE A LUCA PRIMA DEL CODICE** *(un DEVE contro la sua premessa)*: **gia' OGGI, a `cs` uniforme e costante** *(`N = 1`)*, **il tick NON conserva `H` al bit:** **`hw_energia_pesata.txt` (b), `cs` uniforme `0.450304`: l'escursione di `H_w` e' `8.71e-01` a `dtau 0.5`, `2.19e-01` a `0.25`, ... `3.44e-03` a `0.03125`, la pendenza `1.996`** *(il secondo ordine dello spezzamento)*. ### **Quindi la soglia di T-L2** *(`|Delta E_N / E_N| < 1e-11` alla fine)* **NON si puo' raggiungere col palindromo, nemmeno a `N = 1`.** **Le strade:** **(d1) il palindromo, e T-L2 diventa «nessuna deriva secolare; l'escursione dello stesso ordine di `N = 1`; la pendenza `2` nel dimezzamento di `dtau`»** *(il criterio di `hw_energia_pesata`)*; **(d2) un gradiente discreto, fuori dai pezzi del nucleo, con la norma non esatta.** ### **La scelta e' di Luca: FERMO prima del banco** *(S5.1)*.

### 31.5 (e) QUANTA ENERGIA PUO' CONTENERE UN TRIANGOLO *(Luca `11:46`)*: **IL PROGETTO DELLA MISURA**

- **Lo script `csv/solitone/s5_triangolo.py`** *(la scena di `TBS` a `L 81`, il vuoto `c F3`, `cs = s = 0.15` uniforme: `N = 1`)*; **l'energia SI LEGGE da `energia_pesata.termini_di_h`** *(la fonte unica: nessuna formula ricopiata)*, **come `somma per_nodo + somma per_arco` e come energia per nodo** *(il nodo piu' meta' dei suoi archi)*.
- ### **IL LIMITE DEL TEMPO:**
  - **la finestra delle quasi-energie del tick:** **`(-pi/dtau, +pi/dtau)` per unita' di norma, `dtau = 1` tick;** **le bande dal tick lineare** *(`psi` e `phi`, `A(k)` come in S2, gli autovalori `e^{-i eps}`)*: **il minimo e il massimo di `eps`, e quanto la finestra e' piena;**
  - **l'energia LINEARE** *(le parti quadratiche di `H`: i Grover, la moneta, gli spostamenti)* **come forma quadratica: i suoi autovalori estremi per unita' di norma, ristretta a UN nodo** *(le sue `6` estremita')* **e a UN triangolo** *(le estremita' dei suoi `3` nodi)*; **la matrice per polarizzazione** *(`E(u + v) - E(u - v)`, esatta per una forma quadratica)*.
- ### **IL LIMITE DELLO SPAZIO:**
  - **la parte NON lineare** *(`N = Lambda (x - arctan x)`)* **in funzione di `rho`** *(a `Lambda = 6`)*: **una tabella;**
  - ### **il minimo e il massimo dell'energia di UN triangolo a norma fissata:** **`psi` sulle estremita' dei `3` nodi del triangolo, la norma per nodo FISSATA** *(`nu / 3` ciascuno)*, **`phi = c F3` dappertutto, fisso;** **`nu` da `1e-3`** *(il limite lineare)* **a `18`** *(la norma del vuoto di un triangolo, `3 x 6`)* **fino a TUTTA la norma di materia della scena** *(letta dalla scena)*: **`6` valori geometrici;** **l'ottimizzazione vincolata** *(`scipy`, il vincolo per costruzione: i blocchi di nodo rinormalizzati)*, **`8` partenze casuali** *(seme fisso)*; **il minimo e il massimo trovati, e lo stato che li realizza** *(la norma per spin e per estremita')*.
  - **Con DUE zeri:** **O1** *(lo zero simmetrico di oggi: quello che `termini_di_h` gia' usa)* **e O4** *(lo zero locale: per nodo `e_k - media_{j in N1(k)} e_j`, il primo anello di `6`; sommato sui `3` nodi del triangolo)*.
  - **Il costo:** **ogni energia e' un `termini_di_h` sul toro intero** *(~ms)*; ### **un tetto di `60` minuti: se la stima dopo la prima ottimizzazione lo supera, le partenze scendono a `4`** *(dichiarato nel referto)*.
- ### **LE DOMANDE, senza scegliere:**
  1. **`E_N` e' limitata dal basso e dall'alto a norma conservata? Con quale zero?** *(Su un toro finito ogni forma quadratica e' limitata e `0 <= N <= rho`: mi aspetto «si'» con tutti e due gli zeri; la misura dice QUANTO.)*
  2. **`rho_max` per triangolo, e il minimo di `N = 1/(1 + rho_max/rho_c)`:** **`N` puo' arrivare a `0`?** *(A norma finita `rho <= M`, quindi `N >= 1/(1 + M/rho_c) > 0`: `N = 0` solo nel limite `rho_c -> 0`.)*
  3. **Le scale naturali per `rho_c`, elencate:** **`rho_max`; `Lambda = 6`** *(dove `x = 1`)*; **`rho` al quale l'energia del triangolo tocca il tetto `pi/dtau` per unita' di norma; `rho` al quale la parte non lineare uguaglia la larghezza della banda.** ### **NESSUNA scelta.**
- **Se l'energia NON e' limitata dal basso con nessuno zero: FERMO prima del banco.**

### 31.6 LA CODA DOPO S5.0

**(1) S4.7** *(in corsa)*; **(2) lo script di (e), la suite, il commit, la corsa;** ### **(3) FERMO: la scelta dello schema (31.4) e della media d'arco (31.2) e' di Luca;** **il banco** *(S5.1)* **e le prove** *(S5.2)* **dopo.**

### 30.8 L'ESITO DI S4.7 *(la corsa dalle `12:06:21` alle `12:34:17` del `2026-11-11`, a `59c562f0`; il referto `doc/referti_l2/s4_spettro_materia_mrho_v2.txt`, ACCANTO al primo; `101/101`)*: **LO STRUMENTO E' CURATO; IL DIFETTO ERA QUELLO DI 30.5**

- ### **Il fondo passato IDENTICO al congelato** *(lo scarto `0.000e+00`)*: **`A = F + P Q` PASSA in TUTTI i `45` punti** *(fino a `5.0e-09`; a `rho_0 = 1` fino a `7.0e-11`, contro `8.5e-03` di 30.5)*. ### **L'ipotesi di 30.5 era giusta: `q` non era unico dentro la coppia degenere, e il congelato era linearizzato attorno a un altro fondo.**
- **I punti a `rho_0` `1e-4` e `1e-2` ridanno 30.5:** **lo scarto relativo piu' grande di `ln |lambda|_max` e' `3.6e-06`** *(la soglia `1e-3`)*; **il controllo incrociato fallisce come deve** *(`0.897`)*.
- **Restano:** **le basi** *(`7.6e-15`)*, **il vuoto con M-rho unitario, il fattore `1.001`, la traslazione** *(`2.0e-12`)*, **l'onda piana** *(il rapporto `1.0001`)*.
- ### **A `rho_0 = 1` gli spettri sono gli STESSI di 30.5** *(M-rho e congelato, alle `6` cifre stampate)*: **era sbagliato il CONTROLLO, non gli spettri.** **La colonna «M-rho meno congelato» ora vale:**

| `rho_0/rho_c` | `s 0.05` | `s 0.15` | `s 0.3` |
|---|---|---|---|
| `1e-3` | `-1.49e-04` | `-4.52e-04` | `-9.31e-04` |
| `1e-2` | `-1.54e-03` | `-4.61e-03` | `-9.14e-03` |
| `1e-1` | `-2.12e-03` | `-4.89e-03` | `-5.72e-03` |
| `1` | `-9.06e-04` | `-3.65e-04` | **`+6.20e-03`** |
| `10` | `-2.16e-04` | `-5.23e-04` | `-6.72e-04` |

  **Negativa in `14` punti su `15`:** **a `rho_0 = 1` l'orologio M-rho ABBASSA il tasso di (I-mod);** **solo a `rho_0/rho_c = 1`, `s 0.3` lo alza** *(`1.40e-02` contro `7.81e-03`, al `|k| 4.11`, l'autovettore al `14%` in `psi`: la firma di (I-cs), non di (I-mod))*. **A `rho_0` `1e-4` e `1e-2`, dove il congelato e' unitario, (I-cs) e' l'unica instabilita'** *(la tabella di 30.5)*.
- **Nessuna lettura nuova** *(sez. 30.7)*.

### 31.7 S5.0-bis: LE DECISIONI DI LUCA DELLE `13:22`, GLI ERRORI n.136 E n.137, CHE COSA E' STATO PROVATO *(il mandato la chiama «31.6»: la `31.6` c'e' gia', ed e' la coda di S5.0; dichiarato)*

- ### **LE DECISIONI DI LUCA:**
  - **(a) LO SCHEMA:** **il PALINDROMO con `N` a meta' passo** *(come `tick_con_cs`)* **e la reazione col punto medio implicito; NON il gradiente discreto;**
  - **(b) L'ARCO:** **la media ARMONICA del nucleo** *(`FP.s_arco`)*; **nessuna seconda fonte della legge;**
  - **(c) LA PROVA DEL VUOTO CON LA REAZIONE ACCESA:** **si fa, come nota di completezza DENTRO S5** *(V-R)*, **non come ramo nuovo.**
- ### **GLI ERRORI DEL GUARDIANO** *(scritti da Luca)*:
  - **n.136:** **«q2» (`cs' = 0`) l'ha messo il guardiano nel mandato F1; ha spento la reazione.** **T2, B1, H4 e S2 hanno quindi provato un orologio A SENSO UNICO, non la legge del nucleo.**
  - **n.137:** **la soglia di T-L2** *(`|Delta E_N / E_N| < 1e-11`)* **era impossibile:** **il palindromo non conserva `H` al bit nemmeno a `N = 1`** *(l'errore e' `O(dtau^2)`, limitato, senza deriva)*.
- ### **CHE COSA E' STATO PROVATO, com'e':**

| | col solitone | sul vuoto da solo |
|---|---|---|
| **la legge del nucleo CON la reazione** *(`CAMM-FASE-VUOTO`)* | **provata:** **D0-D5, nessun punto fisso; r-D5, il guscio si contrae, il centro instabile, il dominio cede a `Lambda_c ~ 162`** | ### **MAI** |
| **l'orologio a senso unico (q2)** | **T2, B1: instabile** | **H4, S2: instabile** |

  ### **La conclusione «la colpa e' della LEGGE» di S2 (w1) vale SOLO per il senso unico.**

### 31.8 V-R, IL VUOTO CON LA REAZIONE ACCESA: **IL PROGETTO, PRIMA DEL CODICE**

- **Lo strumento di S2** *(`csv/solitone/s2_spettro.py`)*, **con un argomento `--reazione`:** **la mappa di S2** *(i `12` punti)*, **coi casi (L-ist) e (L-F1), DUE volte:** **(q2)** *(`cs_primo_zero`, come S2)* **e (q1)** *(la reazione del nucleo ACCESA: `cs_primo` della legge; `CAMM-FASE-VUOTO` gira col suo punto medio implicito)*. **Il referto `doc/referti_l2/s5_vuoto_reazione.txt`.**
- ### **ACCANTO, un terzo caso MIO, dichiarato: (L-nuc), la legge del nucleo COM'E'** *(`tick.tick_con_cs`: `cs` al centro del palindromo a punto fisso, con la reazione)*. **Perche':** **(L-ist) con (q1) prende `cs` dallo stato all'inizio del tick, e non e' ancora la legge del nucleo;** **e la tabella qui sopra dice che la legge del nucleo sul vuoto non e' MAI stata provata.** **(L-nuc) ha solo `phi` come variabile** *(`12` reali per cella)*. **Le letture si leggono su (L-ist) e (L-F1), come il mandato; (L-nuc) e' accanto.** **Se il punto fisso di `tick_con_cs` alza** *(non converge)*, **lo scrivo e vado avanti.**
- **I DEVE:**
  - **con (q2) i numeri di S2 alla terza cifra:** **`ln |lambda|_max` contro la tabella del referto di S2, entro `1e-3` relativo;** **DEVE FALLIRE: lo stesso contro la riga di un altro punto;**
  - **a `cs` spento lo spettro unitario** *(come in S2)*; **il fattore `1.001`; la linearita'; le basi punti fissi.**
- ### **LE LETTURE** *(di Luca; su (L-ist) e (L-F1) con (q1))*:
  - **(r1)** **stabile in tutta la mappa** *(`|lambda|_max - 1 < 1e-9`)*: **l'instabilita' di S2 era tutta del senso unico; il vuoto che comanda l'orologio, se paga la sua reazione, regge;**
  - **(r2)** **instabile, ma piu' lento di S2 in OGNI punto: la reazione aiuta e non basta;**
  - **(r3)** **instabile come S2** *(entro il `10%` in ogni punto)*: **la reazione non conta, e il problema e' che sia il vuoto a comandare;**
  - **altrimenti: caso intermedio, coi numeri.**
- **Se (r1): lo scrivo IN CIMA al referto e proseguo** *(Luca)*. ### **Il risultato NON riapre F1-F4 e NON cambia la ROTTA: e' un'informazione per Luca.**

### 31.9 (e)-bis: IL SEGNO DI `h_k` NEL SOLITONE, PER CIASCUNO ZERO *(Luca `13:22`)*: **IL PROGETTO**

- **Lo script `s5_triangolo.py` e' gia' committato** *(`a2137e0d`)* **e in corsa:** **il segno di `h_k` va in uno script PICCOLO a parte, `csv/solitone/s5_segno_h.py`, committato prima di girarlo.**
- **`h_k` e' l'energia del nodo** *(`per_nodo` piu' meta' dei suoi archi, da `termini_di_h`)*: **con `cs` uniforme e' esattamente il coefficiente della reazione** *(`H_k(nodo) + somma (dw/dcs_k) H_a`, con `dw/dcs_k = 1/2`)*. **Con O1 e con O4** *(il nodo meno la media dei `6` vicini)*.
- **Lo stato: `TBS` a `10000`** *(il file e lo sha come in H4)*. **Le zone, dal centro di `rho`** *(come in (i))*: **il centro `r < w_in`; il guscio `w_in <= r < 3 w_in`; l'alone `3 w_in <= r < R_ZONA`; e il vuoto lontano `r >= R_ZONA`** *(`w_in` dal jsonl di `TBS`; `R_ZONA = 20` come H4; le soglie sono quelle gia' in uso, dichiarate)*. **Per zona: la media, il min, il max di `h_k`, la frazione dei nodi con `h_k > 0`, e `h_k` meno il valore del vuoto `c F3`.**
- **Accanto, il verso della forza atteso** *(31.3: `V_k = s N'(rho) h_k`, `N' < 0`)*: **`h_k > 0` spinge verso `N` piu' basso, `h_k < 0` verso `N` piu' alto.** ### **Nessuna scelta dello zero: e' di Luca.**

### 31.10 L'ESITO DI S5.0 (e), IL TRIANGOLO *(la corsa dalle `12:59:33` alle `14:55:09` del `2026-11-11`, a `a2137e0d`; il referto `doc/referti_l2/s5_triangolo.txt`; `3/3`)*: **L'ENERGIA E' LIMITATA DAL BASSO E DALL'ALTO, CON TUTTI E DUE GLI ZERI**

- **La scena:** **`TBS` a `L 81`, il triangolo dei nodi `0, 1, 82`** *(`18` estremita', i `3` archi interni)*; **la norma di materia della scena `996944.86`;** **un'energia costa `0.019` s.** **Le energie sono in unita' di `H`** *(`termini_di_h` non pesa: a `N = 1` `G = s H`)*. **Il vuoto `c F3`: `-18.8496` per nodo** *(`-6 pi`, con O1)*.
- ### **IL LIMITE DEL TEMPO:** **le quasi-energie del tick lineare:**
  - **`psi`: `eps` fra `-0.4827` e `+0.4767` per tick** *(il `15.3%` della finestra `(-pi, pi]`; `|lambda| = 1` alla dodicesima cifra)*;
  - **`phi`: `+-0.4712`** *(`+-0.15 pi`; il `15.0%`)*.
  - **La forma quadratica** *(senza `N`)* **per unita' di norma:** **un nodo `[-2.0708, +1.6485]`; un triangolo `[-3.2192, +2.3430]`** *(la polarizzazione riproduce la forma a `3.4e-12`)*.
- **IL LIMITE DELLO SPAZIO:** **`N / rho` a `Lambda = 6` cresce da `~1e-8`** *(`rho = 0.001`)* **a `0.215`** *(`rho = 6`)* **e a `0.984`** *(`rho = 600`)*: ### **`0 <= N <= rho`.**
- ### **IL TRIANGOLO a norma per nodo fissata** *(`phi` fisso; `8` partenze; tutte le ottimizzazioni convergono)*, **per unita' di norma, tolto il vuoto:**

| `nu` | O1 min | O1 max | O4 min | O4 max |
|---|---|---|---|---|
| `0.001` | `-3.1275` | `+2.3280` | `-2.0444` | `+1.4860` |
| `0.0631` | `-3.2192` | `+2.3428` | `-2.1460` | `+1.5619` |
| `3.976` | `-3.2034` | `+2.3588` | `-2.1356` | `+1.5725` |
| `18` | `-3.0046` | `+2.5576` | `-2.0031` | `+1.7051` |
| `250.7` | `-2.3268` | `+3.2354` | `-1.5512` | `+2.1569` |
| `1.58e4` | `-2.2210` | `+3.3412` | `-1.4806` | `+2.2275` |
| `9.97e5` | `-2.2192` | `+3.3430` | `-1.4795` | `+2.2287` |

  - **Lo stato del MINIMO: la norma tutta sulle `6` estremita' dei `3` archi INTERNI del triangolo** *(`0.167` ciascuna)*; **del MASSIMO: sparsa su tutte le `18`.**
  - **Il minimo e il massimo SALGONO tutti e due di `~+1.0` per unita' di norma dalle norme piccole alle grandi** *(O1: da `-3.22` a `-2.22` e da `+2.34` a `+3.34`)*, **perche' la parte `N` cresce come `rho`** *(`N/rho -> 1`)*: **la forma ottima non cambia** *(lo stesso stato)*.
  - ### **A `nu = 0.001` il minimo di O1** *(`-3.1275`)* **e' sopra quello di `nu = 0.063`** *(`-3.2192`, il valore della forma quadratica)*: **l'ottimizzazione a `nu` piccolo si e' fermata prima** *(`7` giri)*: **un limite del metodo, dichiarato** *(i giri sono pochi perche' il gradiente e' `~nu`)*.
- ### **LE DOMANDE, senza scegliere:**
  1. ### **Si': `E_N` e' limitata dal basso e dall'alto a norma conservata, con O1 e con O4.** **Per unita' di norma `[-3.22, +3.34]` con O1, `[-2.15, +2.23]` con O4** *(su `nu` da `1e-3` a `1e6`)*. **Con O1 il vuoto ha `-6 pi` per nodo; con O4 il vuoto ha `0`** *(e la somma di O4 sul toro e' zero per costruzione)*.
  2. **`rho_max` per nodo del triangolo = `M / 3 = 332314.95`** *(tutta la materia della scena nei `3` nodi)*: **`N_min = 1 / (1 + rho_max / rho_c) > 0` per ogni `rho_c > 0`: `N` NON arriva a `0` a norma finita.**
  3. **Le scale per `rho_c`** *(NESSUNA scelta)*:
     - **`rho_max = 332315`;**
     - **`Lambda = 6`** *(dove `x = 1`, `N/rho = 0.215`)*;
     - **il tetto del tick:** **l'energia per unita' di norma resta sotto `3.4`, mentre il tetto `pi / dtau` in unita' di `H` e' `pi / s = 20.9` a `s 0.15`:** **il triangolo lo toccherebbe solo a `s >= ~0.94`.**
- **Nessuna fermata:** **l'energia e' limitata con tutti e due gli zeri.** **Il passo dopo: il segno di `h_k`** *(31.9)*.

### 31.11 L'ESITO DI V-R, IL VUOTO CON LA REAZIONE ACCESA *(la corsa dalle `15:24:20` alle `15:39:14` del `2026-11-11`, a `e6798e4a`; il referto `doc/referti_l2/s5_vuoto_reazione.txt`; `34/34`)*: **CASO INTERMEDIO -- CON LA REAZIONE IL VUOTO RESTA INSTABILE IN TUTTA LA MAPPA; LA REAZIONE RALLENTA MOLTO DOVE `cs` E' ALTO, E ACCELERA F1 DOVE E' BASSO**

- **I DEVE:** **(q2) ridà S2 alla terza cifra** *(`7.8e-05` relativo, `24` righe)*, **il controllo incrociato fallisce come deve** *(`0.156`)*; **`cs` spento unitario, il fattore `1.001`, la linearita', le basi, l'onda piana: come S2.**
- ### **LA MAPPA** *(`ln |lambda|_max` per tick; sempre a `|k| = 4 pi / 3`)*:

| il punto | `cs` del vuoto | (L-F1) q2 | (L-F1) q1 | (L-ist) q2 | (L-ist) q1 | (L-nuc) |
|---|---|---|---|---|---|---|
| `Lambda_c 8.5` | `0.414` | `0.1393` | `0.0357` | `0.1814` | `0.0402` | `2.13e-05` |
| `s 0.3` | `0.300` | `0.2210` | `0.0308` | `0.2774` | `0.0314` | `2.18e-05` |
| `Lambda_c 17` | `0.261` | `0.2188` | `0.0286` | `0.2763` | `0.0273` | `1.48e-05` |
| **oggi** | **`0.150`** | **`0.1610`** | **`0.1452`** | **`0.2112`** | **`0.1495`** | **`0.1540`** |
| `Lambda_c 68`, `Lambda 3` | `0.081` | `0.0963` | `0.1120` | `0.1312` | `0.1133` | `0.1138` |
| `Lambda_c 136` | `0.042` | `0.0526` | `0.0672` | `0.0735` | `0.0674` | `0.0674` |
| `s 0.05` | `0.050` | `0.0617` | `0.0775` | `0.0857` | `0.0778` | `0.0779` |
| `Lambda 1` | `0.029` | `0.0361` | `0.0475` | `0.0509` | `0.0474` | `0.0474` |
| `Lambda_c 340` | `0.017` | `0.0222` | `0.0298` | `0.0315` | `0.0297` | `0.0297` |
| `Lambda 0.5` | `0.014` | `0.0186` | `0.0251` | `0.0265` | `0.0250` | `0.0250` |
| `Lambda 0.1` | `0.003` | `0.0038` | `0.0053` | `0.0055` | `0.0052` | `0.0052` |

- ### **LA LETTURA COL CRITERIO SCRITTO: CASO INTERMEDIO** *(stabili `0` su `24`; `q1/q2` fra `0.099` e `1.385`)*: **ne' (r1)** *(nessun punto stabile)*, **ne' (r2)** *(in `8` casi (L-F1) q1 e' piu' VELOCE di q2)*, **ne' (r3)** *(lo scarto supera il `10%`)*.
- ### **I fatti, senza interpretare:**
  - **con la reazione, dove `cs` del vuoto e' ALTO** *(`0.26`-`0.41`)* **il tasso scende di un fattore `4`-`10`;** **la legge del nucleo com'e' (L-nuc) li' e' QUASI marginale** *(`1.5e-05`-`2.2e-05` per tick)*;
  - **dove `cs` e' BASSO** *(`< 0.15`)* **(L-ist) q1 e (L-nuc) coincidono quasi alla terza cifra** *(oggi differiscono del `3%`)*, e (L-F1) q1 e' piu' veloce di (L-F1) q2:** **la memoria di F1 aiutava, la reazione la toglie;**
  - ### **oggi** *(`cs 0.15`)*: **(L-nuc) `0.154` per tick, quasi come S2.**
- ### **NON (r1): niente da scrivere in cima al referto.** **V-R non riapre F1-F4 e non cambia la ROTTA** *(Luca: il passo `5` si costruisce sul lapse della materia qualunque sia l'esito)*.

### 31.12 L'ESITO DEL SEGNO DI `h_k` *(la corsa dalle `15:39` alle `15:39:46` del `2026-11-11`, a `5aaaa97b`; il referto `doc/referti_l2/s5_segno_h.txt`; `2/2`)*

- **Lo stato: `TBS` a `10000`** *(`rho` totale `996944.86`; il centro `(40.504, 40.502)`; `w_in 6.644`)*; **il vuoto `c F3`: O1 `-18.8496` per nodo** *(`-6 pi`)*, **O4 `3.6e-15`.** **I controlli:** **la somma di `h_k` = il totale** *(`0.0`)*; **O4 somma a zero sul toro** *(`8.9e-12`)*.

| la zona | nodi | `rho` medio | O1 media | O1 `f(h>0)` | O4 media | O4 `f(h>0)` |
|---|---|---|---|---|---|---|
| **il centro** *(`r < w_in`)* | `162` | `2655` | **`+1.106e+04`** | **`1.00`** | **`+85.7`** | `0.65` |
| **il guscio** *(`< 3 w_in`)* | `1278` | `443` | **`+1.833e+03`** | `0.73` | **`-10.9`** | `0.30` |
| **l'alone** *(`< 20`)* | `12` | `0.012` | `-19.08` | `0.00` | `+0.009` | `0.67` |
| **il vuoto lontano** | `5109` | `0.005` | `-18.85` | `0.00` | `+0.002` | `0.50` |

- ### **Il verso atteso della forza** *(31.3: `h_k > 0` verso `N` piu' basso)*:
  - **con O1: nel centro e nel guscio verso `N` piu' basso** *(verso la materia)*; **fuori, `h_k < 0` e la forza va verso `N` piu' alto** *(ma li' `rho ~ 0`, `N' ~ -1/rho_c` e `N ~ 1`)*;
  - **con O4: nel centro verso `N` piu' basso, nel guscio verso `N` piu' alto** *(in media; i segni sono misti)*.
- ⚠ **L'alone fra `3 w_in = 19.9` e `20` ha solo `12` nodi:** **una zona sottile** *(le soglie erano gia' in uso: dichiarato)*.
- ### **Nessuna scelta dello zero: e' di Luca** *(e per la decisione delle `13:29` lo zero diventa fisico prima del passo `5`)*.

### 31.13 S5.1, IL BANCO DEL LAPSE: **IL PROGETTO, PRIMA DEL CODICE** *(le scelte di Luca delle `13:22`: il palindromo, la media armonica)*

- **Il modulo `csv/solitone/tick_lapse.py`, FUORI dal nucleo:** **usa `tick.percorri_tick`, `tick.meta_del_palindromo`, `tick.EPS_CS`, `tick.GIRI_MAX`, `energia_pesata.termini_di_h`, `energia_pesata.d_peso_arco`, `energia_pesata.pesi`, `flussi_parziali.s_arco`** *(attraverso `mot.cs`)* **senza modificarli.**
- ### **IL TICK COL LAPSE** *(lo schema (a))*:
  1. **`N` a meta' passo:** **`cs = s N(rho)` dallo stato al CENTRO del palindromo, a punto fisso** *(la stessa iterazione di `tick.cs_al_centro`: mezzo palindromo su una COPIA, `rho` della copia, fino a `EPS_CS` relativo; se non converge entro `GIRI_MAX`, ALZA)*;
  2. **la reazione sulla materia, MEZZO passo prima e MEZZO dopo il palindromo** *(Strang; il palindromo resta simmetrico, quindi il tick resta reversibile)*: **`psi_h -> e^{-i Omega^psi_k dtau/2} psi_h`, con `Omega^psi_k = s N'(rho_k) [ H_k(nodo) + somma_{a in k} (dw_a/dcs_k) H_a(arco) ]`** *(31.3; `termini_di_h` e `d_peso_arco` del nucleo)*, **col PUNTO MEDIO IMPLICITO a punto fisso** *(`Omega` dallo stato a meta' del mezzo passo; `rho` non cambia, perche' e' una fase; fino a `1e-14` relativo, o ALZA)*;
  3. **il palindromo intero di oggi con `mot.cs` = quel `cs`, `mot.lambda_c = None`** *(niente `CAMM-FASE-VUOTO`: `N` non dipende da `Lambda`)*.
  - ### **Il POSTO della reazione e' una scelta MIA, dichiarata:** **fuori dal palindromo** *(agli estremi)*, **non dentro come `CAMM-FASE-VUOTO`** *(posizioni `1` e `12`)*, **perche' il banco non puo' cambiare `composizione.ORDINE` senza toccare il nucleo.** **Lo schema resta simmetrico e del secondo ordine.**
- **`N(rho) = 1 / (1 + rho / rho_c)`, `N'(rho) = -(1/rho_c) / (1 + rho/rho_c)^2`.** **`rho_c` si passa sempre** *(nessun valore predefinito)*; **`N = 1` esatto dove `psi = 0`** *(`rho = 0` da' `1.0` al bit)*.
- ### **`E_N`, l'osservabile:** **`somma_k w_k H_k(nodo) + somma_a w_a H_a(arco)`, coi pesi DELLO STATO** *(`mot.cs = s N(rho di adesso)` per il tempo della lettura, poi `energia_pesata.pesi`)*: **lo stesso principio di `energia_pesata.g_dello_stato`** *(errore n.12: i pesi dello stato, non quelli del passo)*. **A `N = 1` e' `s H`.**
- ### **IL DEVE DI S5.1:** **con `N = 1` ovunque il banco ridà il tick di oggi AL BIT per `1000` tick, sulla scena di `TBS` a `10000`.**
  - **«Il tick di oggi»:** **`tick.percorri_tick` con `mot.cs = s` uniforme e `mot.lambda_c = None`** *(come T1, H4 (v2), S4 «la legge spenta»)*.
  - **«`N = 1` ovunque»:** **`N` costante `1`** *(un `N` che non dipende da `rho`, quindi `N' = 0`, e la reazione e' `e^{0} = 1` esatto)*.
  - **Il confronto:** **lo `sha1` di `psi_h` e `phi_h` ai tick `1`, `10`, `100`, `1000`, fra le due corse.**
  - ### **DEVE FALLIRE:** **lo stesso con `rho_c = 1e6`** *(`N` vicino a `1` ma NON uguale)*: **lo `sha1` deve DIFFERIRE gia' al tick `1`** *(lo strumento vede una differenza piccola)*.
- **Lo script del DEVE: `csv/solitone/s5_banco.py`** *(il referto `doc/referti_l2/s5_banco.txt`)*. **Poi il progetto di S5.2 per esteso** *(le prove, le letture, PRIMA del codice)*.

### 31.14 L'ESITO DI S5.1 *(la corsa dalle `16:22:12` alle `16:26:42` del `2026-11-11`, a `9344cc65`; il referto `doc/referti_l2/s5_banco.txt`; `2/2`)*: **IL BANCO CON `N = 1` E' IL TICK DI OGGI AL BIT**

- ### **DEVE PASSA:** **lo `sha1` di `psi_h` e `phi_h` del banco con `N = 1` = quello del tick di oggi ai tick `1`, `10`, `100`, `1000`** *(per esempio al `1000`: `psi 04e053354db5fcda`, `phi d706b57deb94b48b`)*. **Il punto fisso di `cs` converge in `1` giro a ogni tick.**
- **DEVE FALLIRE fallisce come deve:** **con `rho_c = 1e6` lo stato al tick `1` e' diverso** *(i giri: `cs` `4`, la reazione `3` e `3`)*.
- **`E_N` sullo stato di `TBS` a `10000`:** **`6.0570146942e+05` a `N = 1`** *(`= s H`)*, **`6.0455115762e+05` a `rho_c = 1e6`.**
- **Il costo:** **il tick di oggi `102` s per `1000` tick; il banco a `N = 1` `154` s** *(il mezzo palindromo del punto fisso in piu')*.

### 31.15 S5.2, LE PROVE DEL LAPSE: **IL PROGETTO, PRIMA DEL CODICE** *(il mandato delle `11:33` con le modifiche delle `13:22`)*

- ### **DUE PREMESSE CHE NON REGGONO, dal codice** *(da dire a Luca)*:
  1. ### **T-L5** *(«avanti `1000` tick e indietro `1000`»)* **NON si puo' fare coi pezzi del nucleo:** **`flussi_parziali._nel_cono` asserisce `0 < s <= 1`** *(«un tempo proprio negativo e' un orologio che va indietro, e NON si corregge»)* **e `_frazione_valida` vieta una frazione negativa.** **Un tick all'indietro vorrebbe una modifica del nucleo** *(vietata)* **o un pezzo inverso scritto fuori** *(una seconda fonte della legge)*. ### **T-L5 resta FUORI finche' Luca non decide** *(la reversibilita' dello schema e' per costruzione: il palindromo e la reazione simmetrica; ma non la misuro)*.
  2. ### **T-L4 con lo zero O4 NON si puo' SIMULARE:** **lo zero dell'energia sta DENTRO i pezzi del tick** *(lo zero simmetrico O1, Luca `2026-11-08`)*: **un tick con O4 sarebbe un altro generatore** *(un'altra legge)*. ### **T-L4 si simula con O1; per O4 riporto il verso PREVISTO dalla forza di (c) coi valori di `h_k` di 31.12, accanto, non una simulazione.**
- **La scena comune:** **`TBS` a `10000`** *(`L 81`, il bordo spento)*; **`rho_0` = la `rho` media del centro del solitone** *(`r < w_in`, `2655` in 31.12; lo script la ricalcola)*; **`rho_c = rho_0 / r`.**
- ### **T-L1, IL VUOTO:** **`c(10000) F3`, `psi = 0`, `1000` tick, `rho_c = rho_0 / 1e-2`:** **DEVE: il banco = il tick di oggi al bit** *(gli sha ai tick `1`, `10`, `100`, `1000`)*; **DEVE: calmo** *(la rms di `Lambda` sotto `1e-13` alla fine, il criterio di (v0a))*.
- ### **T-L2, L'ENERGIA** *(il criterio nuovo: NESSUNA DERIVA)*: **`5000` tick per `r` in `{1e-3, 1e-2, 1e-1}`; `E_N` ogni `10` tick** *(coi pesi dello stato)*:
  - **DEVE: la pendenza di una retta su `E_N` entro `3` errori di Sokal** *(l'errore gonfiato di `sqrt(2 tau_int)` dei residui, come U2)*;
  - **DEVE: la norma di `psi` e di `phi` entro `1e-13` relativo, a ogni campione;**
  - **DEVE: l'escursione scende come `dtau^2`:** **la stessa scena a `s` e a `s/2`, per lo STESSO tempo fisico** *(`1000` tick a `s`, `2000` a `s/2`; `r = 1e-2`: una scelta mia per il costo, dichiarata)*: **il rapporto delle escursioni fra `3.2` e `4.8`;**
  - **accanto: l'escursione a `N = 1`** *(lo stesso ordine di grandezza)* **e M-rho istantanea** *(`cs` dallo stato di inizio tick, niente reazione: la sua pendenza, attesa diversa da zero)*, **`5000` tick a `r = 1e-2`.**
  - ### **DEVE FALLIRE:** **il banco SENZA la reazione** *(`r = 1e-2`, `5000` tick)*: **la pendenza oltre `3` errori.**
- ### **T-L3, LO SPETTRO:** **lo strumento di S4.7** *(`s4_materia_mrho.py`, un argomento `--lapse`)*: **i `45` punti di S4, la mappa del banco** *(`tick_lapse.tick`, `rho_c = rho_0 / r`)* **contro il `cs` congelato** *(il riferimento)*; **DEVE FALLIRE: senza la reazione (I-cs) ricompare** *(il tasso del banco senza reazione supera il congelato oltre `1e-9` in almeno un punto vicino a `K`)*. **Le letture di Luca:**
  - **(l1)** **vicino a `K` il tasso del lapse non supera il congelato oltre `1e-9` in tutta la mappa: (I-cs) sparisce;**
  - **(l2)** **resta un'instabilita' con la firma di Jeans** *(`|k|` piccolo, sotto `1` -- mio; il tasso che cresce con `rho_0`; l'autovettore per piu' della meta' in `psi` -- mio)*: **CANDIDATA GRAVITA', col tasso in funzione di `rho_0` e di `k`;**
  - **(l3)** **resta un'instabilita' alla scala del reticolo** *(`|k| > 2`, mio)*: **FERMO.**
- ### **T-L4, LA CADUTA** *(con O1)*: **un pacchetto gaussiano della banda dei solitoni** *(`q` della coppia a `Gamma`, la larghezza `8` nodi -- mia)*, **ampiezza piccola** *(`rho` massima `1e-3` -- mia)*, **nel vuoto `c F3` SENZA il solitone** *(«lontano»)*, **in un `N` ESTERNO statico `N(x) = 1 + gamma sin(2 pi x / L)`** *(il pacchetto dove la pendenza e' massima; `gamma` in `{0.01, 0.02}`: due valori per vedere che l'accelerazione va come `gamma`, invece di sceglierne uno)*; **`N` NON comandato dalla materia** *(quindi niente reazione)*.
  - **La previsione dalla forza di (c), in forma di raggio:** **`omega(x, k) = s N(x) E(k)`, quindi `dk/dt = -s E(k) dN/dx`, `v = s N dE/dk`, e al fondo della banda `a = -s^2 N E_0 (d^2 E / dk^2) dN/dx`** *(`E_0` e la curvatura dalla banda del tick lineare a `Gamma`, misurate dallo script)*.
  - **DEVE: l'accelerazione del baricentro** *(una parabola su `200` tick -- mio)* **= la previsione entro il `5%`;** **DEVE: col gradiente rovesciato** *(`gamma -> -gamma`)* **il verso si rovescia;** **e il verso, scritto: verso `N` piu' basso o piu' alto.**
- **Il costo** *(il banco ~`0.15`-`0.6` s per tick)*: **T-L1 ~`10` min; T-L2 ~`4` ore; T-L3 ~`2` ore; T-L4 ~`30` min.** **Un test alla volta, coi suoi script:** **`s5_prove.py --prova L1|L2|L4`** *(i referti `s5_lapse_energia.txt` per L1 e L2, `s5_lapse_caduta.txt` per L4)*, **e `s4_materia_mrho.py --lapse`** *(`s5_lapse_spettro.txt`)*.
- ### **DOPO S5.2: FERMO, con la tabella delle prove.** **Lo zero, la forma di `N`, la scala e l'ingresso nel nucleo sono di Luca.**

### 31.16 S5.0 (f), LA SORGENTE MISTA DELL'OROLOGIO *(Luca `2026-11-11` `16:44`)*: **f.0, PRIMA DEL CODICE** *(il mandato la chiama «31.14»: la `31.14` e la `31.15` ci sono gia' -- l'esito di S5.1 e il progetto di S5.2 --, quindi f.0 e' la `31.16`, l'esito la `31.17`, f.2 la `31.18`; dichiarato)*

- ### **LA DECISIONE DI LUCA:** **`S` = l'energia della MATERIA con lo zero di O1** *(comprende `pi M`, l'analogo dell'energia di riposo)* **+ l'energia del VUOTO con lo zero LOCALE di O4** *(la media dei `6` vicini tolta nodo per nodo)*. **Il vuoto calmo e uniforme non pesa; le sue FLUTTUAZIONI pesano col loro segno** *(come nell'effetto Casimir)*; **la materia pesa con tutta la sua energia.**
- ### ⛔ **E LE PROVE DEL BANCO (S5.2) ASPETTANO la decisione di Luca sulla forma di `N`** *(`rho` o `S`)*: **lo script `s5_prove.py` e' committato, NON si gira** *(la precedenza: il mandato delle `16:44` viene dopo quello delle `13:22`)*.

#### (a) LA SCOMPOSIZIONE DI `h_k` *(dal codice: `energia_pesata.termini_di_h`; per nodo, il nodo piu' meta' dei suoi archi)*

| il termine | la parte |
|---|---|
| **il Grover di `psi`:** `-pi (nrm_psi/2 - |somma psi|^2 / d)` | **MATERIA** |
| **la moneta:** `eps * elicita` *(di `psi`)* | **MATERIA** |
| **lo spostamento di `psi`:** `pi Re <psi_0 | U | psi_1>` *(meta' a ciascun capo)* | **MATERIA** |
| **il Grover di `phi`:** `-pi (nrm_phi/2 - |somma phi|^2 / d)` | **VUOTO** |
| **lo spostamento di `phi`:** `pi Re (conj phi_0 phi_1)` *(meta' a ciascun capo)* | **VUOTO** |
| **l'accoppiamento `N(rho, Lambda) = Lambda (x - arctan x)`** *(`CAMM-MATERIA-VUOTO`)* | ### **il codice NON lo impone:** **tre attribuzioni, misurate tutte e tre accanto: (A-m) alla materia; (A-v) al vuoto; (A-mv) meta' e meta'** |

- **Che cosa dice il codice sull'accoppiamento** *(un fatto, non una scelta)*: **`N` dipende da `rho` E da `Lambda`; e' `0` dove `rho = 0`** *(il vuoto puro non lo vede)*; **le sue derivate mettono una fase su `psi` (`alpha`) e una su `phi` (`beta`).**

#### (b) GLI ZERI

- **La materia con O1:** **i termini di `psi` come li da' `termini_di_h`, che usa GIA' lo zero simmetrico O1** *(Luca `2026-11-08`)*. ### **Come leggo «lo spostamento `pi rho` del nodo (O1)»:** **e' la differenza fra lo zero di prima e O1** *(`-pi s (X - 1/2)` contro `-pi s X`: `pi/2` per unita' di norma e per pezzo)*; **`termini_di_h` lo contiene gia', quindi NON lo aggiungo** *(dichiarato: se Luca intende un `+ pi rho` in piu', e' una riga)*.
- **Il vuoto con O4:** **`e_k^vuoto - media_{j in N1(k)} e_j^vuoto`, i `6` vicini** *(`doc/TASK_HISTORY/2026-11-08_zero_del_vuoto.md`, sez. `2`)*.

#### (c) LE PROPRIETA' ATTESE, E UNA PREMESSA DA DIRE

- **`S = 0` esatto dove `psi = 0` e il vuoto e' uniforme:** **la materia e' `0`** *(i termini di `psi` sono `0`, e `N(0, Lambda) = 0` in tutte e tre le attribuzioni)*; **il vuoto uniforme con O4 e' `0`.** **DEVE: entro `1e-12` per nodo.**
- ### ⚠ **«`S` non cambia se si sposta lo zero GLOBALE»: dipende da QUALE spostamento.**
  - **Una costante PER NODO** *(`E_k -> E_k + C`)*: **la materia, riportata a O1, non cambia; il vuoto con O4 la toglie ESATTAMENTE.** **DEVE: `S` identica entro `1e-12`.**
  - **La conversione fra le convenzioni del nucleo e' invece una costante PER UNITA' DI NORMA** *(`c` per pezzo: `E_k -> E_k + c (norma del pezzo)`)*: **la materia, riportata a O1, non cambia; ma il vuoto con O4 cambia di `c (Lambda_k - media_j Lambda_j)`, che e' zero solo dove `Lambda` e' uniforme o lineare.** ### **Quindi in quel caso `S` NON e' identica nel solitone** *(un DEVE contro la sua premessa)*: **misuro lo scarto e DEVE: lo scarto = `c (Lambda_k - media_j Lambda_j)` entro `1e-12`** *(l'identita' prevista)*, **con `c = -pi/2`** *(il passaggio dallo zero di prima a O1, per Grover e arco)*.
- **DEVE FALLIRE** *(Luca)*: **il vuoto con lo zero di O1 invece di O4, sul vuoto uniforme: `S = -6 pi` per nodo.**

#### f.1, LA MISURA *(lo script `csv/solitone/s5_sorgente.py`, il referto `doc/referti_l2/s5_sorgente_mista.txt`)*

- **`TBS` a `10000`**, **le zone dal centro di `rho`:** **il centro `r < w_in`; l'interno `w_in <= r < 16`** *(mio: la corona fra il centro e il guscio di Luca, perche' nessun nodo resti fuori)*; **il guscio `16 <= r < 18`** *(Luca)*; **l'alone `18 <= r <= 30`** *(mio)*; **il vuoto lontano `r > 30`** *(Luca)*.
  - **Per zona e per attribuzione: la media di `S`, il minimo, la frazione dei nodi con `S < 0` PESATA con `rho`** *(`somma_{S<0} rho / somma rho`)*; **il totale di `S` e il rapporto con `M`** *(la norma di materia)*.
- **Il vuoto uniforme** *(`c(10000) F3`, `psi = 0`: la scena di H4 (v0) a `t 0`)*: **`S` per nodo.**
- **Il vuoto con onde** *(la scena di H4 (v1): il disturbo `A_h` costruito come in `h4_vuoto.py`, lo stesso seme)*: **`S` per nodo, la media, la rms, la frazione negativa.** **DEVE: `A_h` = quello del referto di H4** *(`3.308833e-02`, alla settima cifra)*.
- ### **LE LETTURE** *(di Luca; per ciascuna attribuzione)*:
  - **(g1)** **`S >= 0` nel centro, nel guscio e nell'alone** *(la frazione negativa pesata sotto l'`1%`)* **e il totale positivo, circa proporzionale a `M`: la sorgente e' sana;**
  - **(g2)** **restano zone negative nel guscio, ma il totale e' positivo:** **la lettura dell'energia di LEGAME** *(negativa localmente)*; **quanto pesa rispetto al totale;**
  - **(g3)** **il totale e' negativo, o il vuoto uniforme non da' zero: FERMO;**
  - **sul vuoto con onde, nessuna lettura: i numeri.**
- **Poi f.2 su carta** *(la coerenza con la conservazione)*, **e FERMO.**

### 31.17 LE RISPOSTE DI LUCA DELLE `17:22`, E L'ESITO DI f.1 *(la corsa dalle `17:36:34` alle `17:36:50` del `2026-11-11`, a `e81c5081`; il referto `doc/referti_l2/s5_sorgente_mista.txt`; `11/11`)*

- ### **LE RISPOSTE DI LUCA** *(`17:22`, ai punti di 31.15 e 31.16)*:
  1. **nessun «`+ pi rho`» in piu':** **la materia con lo zero O1 e' quella dei pezzi del nucleo, come l'ho letta;**
  2. **lo zero globale: la correzione va bene;** **si misura lo scarto previsto `c (Lambda_k - media_j Lambda_j)` e si verifica l'identita' entro `1e-12`;**
  3. ### **T-L5 resta FUORI, come voce aperta:** **niente modifiche al nucleo, niente tick inverso scritto fuori;**
  4. **T-L4: simulata con O1; per O4 solo il verso previsto, accanto.**
- ### **f.1, I DEVE:**
  - **il vuoto uniforme: `S = 0`** *(`max |S| = 3.6e-15`, tutte e tre le attribuzioni)*;
  - **il vuoto contato con O1 invece di O4 FALLISCE come deve** *(`S = -18.849556 = -6 pi` per nodo)*;
  - **lo zero globale PER NODO** *(`-6 pi`)*: **`S` identica, lo scarto `3.6e-12`;**
  - **lo zero PER UNITA' DI NORMA** *(`c = -pi/2`)*: **`S` cambia fino a `11.21` nel solitone, ESATTAMENTE di `c (Lambda_k - media_j Lambda_j)`** *(l'identita' entro `4.4e-12`-`5.3e-12`)*.
    - ⚠ **In ASSOLUTO l'identita' e' a `~5e-12`, non sotto `1e-12`:** **`S` arriva a `1.4e4` nel centro, e l'arrotondamento di numeri cosi' e' gia' `~2e-12`.** **In RELATIVO e' `~4e-16`.** **Il DEVE e' relativo alla scala di `S`** *(dichiarato nel commit dello script)*: **lo dico a Luca, che aveva scritto «entro `1e-12`».**
  - **`A_h` = quello di H4** *(`3.308833e-02`)*.
- ### **f.1, `TBS` a `10000`** *(`M = 996944.86`)*:
  - **le parti per nodo, sommate:** **la materia `3.1655e+06`** *(`3.175 M`: circa `pi M`, che sarebbe `3.1320e+06`)*; **il vuoto con O1 `-1.1619e+05`; l'accoppiamento `9.887`.**

| la zona | nodi | `rho` medio | (A-m) `S` medio | (A-v) `S` medio | (A-mv) `S` medio | `f(S<0)` pesata, (A-m)/(A-v)/(A-mv) |
|---|---|---|---|---|---|---|
| **il centro** *(`r < w_in`)* | `162` | `2655` | `+1.108e+04` | `+8.456e+03` | `+9.768e+03` | `0` / `0` / `0` |
| **l'interno** *(`w_in`-`16`)* | `760` | `741` | `+3.083e+03` | `+2.349e+03` | `+2.716e+03` | `0` / `0` / `0` |
| **il guscio** *(`16`-`18`)* | `254` | `15.3` | `+62.8` | `+42.6` | `+52.7` | `0.0013` / `0.0115` / `0.0047` |
| **l'alone** *(`18`-`30`)* | `2090` | `0.0186` | `-0.082` | `-0.099` | `-0.090` | `0.40` / `0.47` / `0.44` |
| **il vuoto lontano** *(`> 30`)* | `3295` | `0.0017` | `+0.0044` | `+0.0044` | `+0.0044` | `0.43` / `0.43` / `0.43` |

  - **Il totale di `S`:** **(A-m) `+4.154e+06`** *(`S/M = 4.167`)*; **(A-v) `+3.166e+06`** *(`3.175`)*; **(A-mv) `+3.660e+06`** *(`3.671`)*. **Le parti negative valgono `0.0002`-`0.0003` del totale positivo.**
  - ### **LA LETTURA COL CRITERIO SCRITTO: (g2) con tutte e tre le attribuzioni.**
    - **Nel centro e nell'interno `S > 0` dappertutto; nel guscio la frazione negativa pesata e' `0.13%`-`1.2%`.**
    - **Nell'alone `40%`-`47%` e' negativo:** **li' `rho` e' `0.019` e `S` e' quasi tutto il VUOTO con O4** *(le onde emesse, col loro segno)*.
    - **Il totale e' positivo e circa proporzionale a `M`:** **con (A-v) `S/M = 3.175`, quasi `pi`** *(l'energia «di riposo» `pi M`)*.
- **f.1, il vuoto con le onde di H4 (v1)** *(nessuna lettura)*: **`S` per nodo con la media `+6e-18`** *(O4 somma a zero per costruzione)*, **la rms `0.206`, il min `-0.765`, il max `+0.820`, la frazione negativa `0.498`;** **accanto, il vuoto con O1: la media `-18.836`, la rms `0.325`.**

### 31.18 f.2, LA COERENZA CON LA CONSERVAZIONE *(su carta)*: **LE SCELTE CHE IL CODICE NON IMPONE -- FERMO**

- ### **Se l'orologio e' comandato da `S`, `E_N` e la sua reazione si scrivono con la STESSA scomposizione.**
  - **I pezzi del tick pesano i loro generatori col `cs` del nodo** *(e con la media armonica sugli archi)*. **Quindi `E_N = somma_k s N_k H_k(nodo) + somma_a w_a H_a(arco)`, con lo zero O1 DENTRO i pezzi** *(31.1)*.
  - **La reazione e' `i d/dt = dE_N / d(campo)^*`.**
  - **Con `N = N(S)`, `S` dipende da TUTTO lo stato della cella** *(i Grover, la moneta, gli spostamenti; per il vuoto con O4, anche da `phi` dei `6` vicini)*. **Quindi:**
    - **la reazione sulla MATERIA non e' piu' una fase per nodo** *(come con `N(rho)`)*: **e' `somma_k s N'(S_k) h_k dS_k / d psi*`, un operatore che mescola le estremita' e i nodi vicini;**
    - ### **ora anche il VUOTO sente la reazione** *(`dS_k / d phi*` non e' zero: le fluttuazioni pesano, quindi rispondono)*, **e a raggio del primo anello** *(O4)*;
    - **la reazione non e' una fase, quindi non conserva da sola la norma per costruzione:** **il punto medio implicito resta reversibile, ma la norma esatta va dimostrata** *(con un `E_N` reale e invariante sotto la fase globale, il flusso esatto conserva la norma; lo schema, da verificare)*.
- ### **LE SCELTE CHE IL CODICE NON IMPONE** *(di Luca)*:
  1. **la forma di `N(S)`:** **`S` puo' essere NEGATIVO** *(l'alone, il guscio, le fluttuazioni)*: **`1/(1 + S/S_c)` diverge a `S = -S_c` e supera `1` per `S < 0`, e allora `cs = s N` puo' uscire dal cono** *(`s N <= 1`)*. **Serve una forma definita anche per `S < 0`.**
  2. **che cosa moltiplica `N` in `E_N`:** **l'energia dei pezzi** *(zero O1: allora il vuoto con `N != 1` porta il suo `-6 pi` per nodo come potenziale)* **o `S` stessa** *(`E_N = somma N(S) S`: ma il tick pesa i pezzi, non `S`)*;
  3. **l'attribuzione dell'accoppiamento** *(A-m, A-v, A-mv)*: **cambia `S` del `24%` nel centro;**
  4. **lo schema della reazione non locale** *(sulla materia E sul vuoto, al primo anello)*: **il punto medio implicito sull'intera cella, o un altro;**
  5. ### **o `S` entra solo al passo `5`** *(come sorgente di `Phi`, M-Phi)*, **e il banco tiene `N(rho)`** *(la reazione una fase, gia' provata in S5.1)*.
- ### ⛔ **FERMO** *(Luca: «poi fermo per la decisione su `N(rho)` o `N(S)`»)*. **Le prove del banco** *(S5.2: `s5_prove.py` committato, non girato; T-L3 e T-L4 da scrivere)* **partono con la sua decisione.**

### 31.19 LA DECISIONE DI LUCA DELLE `18:17`: **LA SCELTA 5 -- IL BANCO TIENE `N(rho)`; `S` ENTRA AL PASSO `5` COME SORGENTE DI `Phi`** *(M-Phi)*

- **Le prove del banco S5.2 partono:** **T-L1, T-L2, T-L3, T-L4 con O1, e il DEVE FALLIRE senza la reazione; T-L5 fuori** *(la voce aperta delle `17:22`)*.
- **L'ordine** *(un test alla volta dove serve la suite; le suite non partono con due processi gia' in corsa)*:
  1. **il codice che manca, committato prima:** **T-L3** *(l'argomento `--lapse` di `s4_materia_mrho.py`, il progetto in 31.15)*; **T-L4** *(uno script NUOVO, `csv/solitone/s5_caduta.py`, perche' `s5_prove.py` sara' in uso da T-L2)*;
  2. **la suite;**
  3. **le corse: T-L1, poi T-L2, T-L3 e T-L4.**
- ### **T-L4, i dettagli che 31.15 non fissava** *(miei, dichiarati prima del codice)*:
  - **`N(x) = 1 + gamma sin(2 pi i1 / L)`** *(`i1` l'indice lungo `A1`)*: **il gradiente sta lungo il vettore reciproco `B_0`** *(perpendicolare ad `A2`)*, **`|grad N| = gamma (2 pi / L)(2/sqrt 3)` dove il seno passa per zero;** **lo spostamento si misura lungo `B_0`.**
  - **Il pacchetto:** **`q` = la prima colonna della coppia piu' alta a `Gamma`** *(come `_consolida_B.coppia`)*, **l'inviluppo gaussiano di larghezza `8` nodi, `rho` massima `1e-3`, centrato su un nodo con `i1 = 0`** *(`N = 1`, la pendenza massima)*.
  - ### **La previsione, in forma di raggio e SENZA supporre `epsilon` lineare in `cs`:** **`Omega(x, k) = epsilon(k; s N(x))`, quindi `dk/dt = -(d epsilon / d cs) s dN/dx` e `a = (d^2 epsilon / dk^2) dk/dt = -(d^2 epsilon / dk^2)(d epsilon / d cs) s dN/dx`** *(per tick al quadrato)*. **`epsilon = -arg lambda` della banda del pacchetto** *(quella con la sovrapposizione piu' grande con `q`)*; **le derivate con differenze centrali dal tick lineare di `psi`** *(`A(k)` per `k` lungo `B_0`, `dk = 0.02`; `cs` a `s (1 +- 1e-4)`)*.
  - **La misura:** **`200` tick; il baricentro lungo `B_0` pesato con `rho`; una parabola** *(l'accelerazione)*. **`gamma` in `{+0.01, -0.01, +0.02, -0.02}`.**
  - **I DEVE:** **l'accelerazione = la previsione entro il `5%`, per ogni `gamma`;** **col gradiente rovesciato il verso si rovescia;** **e il verso, scritto: verso `N` piu' basso o piu' alto.**
  - **O4, solo previsto:** **con lo zero locale una pendenza COSTANTE di `N` non da' potenziale** *(il nodo sta sulla media dei vicini: la tabella di `2026-11-08_zero_del_vuoto`, O4)*: **la forza lineare sparisce; resta un termine `~ (a^2/4) lapl(cs)`, a cortissimo raggio.**

### 31.20 LA CONFERMA DI LUCA DELLE `18:25`, E LA DECISIONE DELLE `18:24`

- **`18:25`: la scelta 5 di 31.18, ripetuta:** **il banco tiene `N(rho)`** *(la reazione una fase per nodo, gia' provata in S5.1)*; **`S` entra al passo `5` come sorgente di `Phi`** *(M-Phi)*. ### **Le prove S5.2 UNA ALLA VOLTA:** **T-L1, T-L2** *(il criterio senza deriva)*, **T-L3** *(col `cs` congelato)*, **T-L4** *(con O1; per O4 il verso previsto, accanto)*, **il DEVE FALLIRE senza reazione; T-L5 fuori.** **Dopo S5.2: FERMO, con la tabella delle prove.**
- ### **Il codice di T-L3 e T-L4: `a82ca3d0`** *(la suite `67` su `67`, dalle `18:25:58` alle `18:44:47`)*. **Le corse in SEQUENZA in un solo processo:** **T-L1, T-L2, T-L3, T-L4** *(gli orari in `orari_prove`, letti dall'uscita)*.
- **`18:24`** *(sul principale)*: **l'unificazione** *(il passo `3`)* **parte DOPO la chiusura di S5.**
- ### **T-L1: `2/2`** *(dalle `18:49:47` alle `18:55:45`, a `a82ca3d0`; `doc/referti_l2/s5_lapse_vuoto.txt`)*: **sul vuoto il banco = il tick di oggi AL BIT ai tick `1`, `10`, `100`, `1000`; calmo** *(la rms di `Lambda` `1.776e-15`)*. **Il commit arriva tardi: sono rimasto in attesa invece di committare la prova chiusa** *(un errore mio)*.
- ### **T-L2: `6/8`, exit `1`** *(dalle `18:55:45` alle `21:54:18`, a `a82ca3d0`; `doc/referti_l2/s5_lapse_energia.txt`)*:
  - **NESSUNA DERIVA col lapse ai tre rapporti** *(la pendenza a `1.89`, `0.48`, `1.01` errori; l'escursione relativa `6.1e-05`, `9.6e-05`, `8.4e-04` per `r` `1e-3`, `1e-2`, `1e-1`)*; **le norme entro `3.6e-14`.**
  - ### **FALLISCE: l'escursione NON scende come `dtau^2`:** **il rapporto `s` contro `s/2` e' `1.82`** *(atteso fra `3.2` e `4.8`)*. **Un fatto, non interpretato:** **va piu' come `dtau` che come `dtau^2`.**
  - **Accanto: `N = 1`, l'escursione `2.77e+02`** *(il lapse a `r = 1e-2` `1.39` volte tanto)*; **M-rho istantanea: l'escursione `1.00e+04`** *(`26` volte il lapse)*, **ma la pendenza a `0.31` errori.**
  - ### **FALLISCE IL DEVE FALLIRE:** **senza la reazione la pendenza e' a `0.69` errori** *(il criterio «nessuna deriva» non la vede)*, **MA l'escursione e' `1.06e+04`, `27` volte quella col lapse, e l'energia finisce `+0.26%` sopra l'inizio.** ### **Il criterio della pendenza con l'errore di Sokal e' troppo debole per questa differenza** *(`tau_int` `25`: le oscillazioni lente gonfiano l'errore)*: **lo dico, non lo cambio.**
