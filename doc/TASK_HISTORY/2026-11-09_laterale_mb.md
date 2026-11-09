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
