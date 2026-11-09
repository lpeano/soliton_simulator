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
