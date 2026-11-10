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
