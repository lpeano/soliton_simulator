# REFERTO -- **il `0.3` a ZERO dopo la cura, il DOVE, e il CIRCOLO del dipolo**

*(Mandato di Luca del 2026-10-06. Le tre domande, la classe `MATERIA`/`BORDO`/`VUOTO` e i **tre criteri** sono fissati in `doc/TASK_HISTORY/2026-10-06_mitosi-zero-dopo-la-cura.md`, committato ### **prima** in `b56141c`.)*

| | |
|---|---|
| **simulatore** | `cf2a1ac8` -- ### **verificato all'avvio** contro `cf2a1ac8` |
| **strumento** | `16dced88` *(piu' `_tors_w8_lunga` `bc62bcaa`, che IMPORTA)* |
| **copie patchate** | `4d9f5e8c` *(zero)*, `86ae2f80` *(acceso)*, **10** ancore |
| **passi** | `1000` per braccio, ### **processi SEPARATI**, seme `11` |
| **la geometria, DALLA SCENA** | `r_regione` `4.096438`, `R_CONN` `2.400000`, ### **`u_bordo` `1.5859`** |
| **configurazione del driver** | dichiarata INTERA: `True` *(zero)*, `True` *(acceso)* |

## ⛔ DOMANDA `1`: **la crescita e' del MODELLO o dipende dal `0.3`?**

| | `_AMP = 0` | `_AMP = 0.3` | ### **`R`** | la lettura |
|---|--:|--:|--:|---|
| divisioni | `565` | `3496` | ### **`0.1616`** | ### **INTERMEDIA** |
| popolazione nella finestra `Σ (g1∧g2∧g3)` | `253334` | `741333` | ### **`0.3417`** | ### **INTERMEDIA** |
| Schwinger | `262` | `1265` | *(non nel criterio)* | |

> ### ⛔ **LE DUE LETTURE DI `R` CONCORDANO: <<INTERMEDIA>>.**

| `R` | la lettura, fissata PRIMA |
|---|---|
| ### **`>= 0.5`** | la crescita e' del MODELLO; il `0.3` la anticipa o la accelera, ma **non la crea** |
| ### **`<= 0.1`** | la crescita **dipende ancora** dal `0.3` |
| fra `0.1` e `0.5` | intermedia |

### IL PASSO DELLA PRIMA NASCITA, **nei due bracci**

| | `_AMP = 0` | `_AMP = 0.3` |
|---|--:|--:|
| prima **divisione** | `216` | `214` |
| primo **Schwinger** | `216` | `215` |
| primo arco oltre `4π` | `218` | `218` |

### ➜ **Il `0.3` sposta la prima divisione di `2` passi** *(da `214` a `216`)*.

### LE NASCITE PER FINESTRE DI `50` PASSI

| finestra | divisioni `_AMP = 0` | divisioni `_AMP = 0.3` | Schwinger `0` | Schwinger `0.3` |
|---|--:|--:|--:|--:|
| `1`-`50` | `0` | `0` | `0` | `0` |
| `51`-`100` | `0` | `0` | `0` | `0` |
| `101`-`150` | `0` | `0` | `0` | `0` |
| `151`-`200` | `0` | `0` | `0` | `0` |
| `201`-`250` | `17` | `25` | `12` | `8` |
| `251`-`300` | `13` | `75` | `6` | `35` |
| `301`-`350` | `15` | `99` | `7` | `30` |
| `351`-`400` | `23` | `127` | `10` | `42` |
| `401`-`450` | `36` | `119` | `17` | `39` |
| `451`-`500` | `34` | `152` | `17` | `64` |
| `501`-`550` | `51` | `224` | `19` | `86` |
| `551`-`600` | `54` | `252` | `26` | `87` |
| `601`-`650` | `32` | `207` | `15` | `56` |
| `651`-`700` | `35` | `273` | `12` | `92` |
| `701`-`750` | `32` | `286` | `13` | `109` |
| `751`-`800` | `49` | `297` | `26` | `97` |
| `801`-`850` | `48` | `267` | `25` | `108` |
| `851`-`900` | `44` | `333` | `21` | `128` |
| `901`-`950` | `42` | `362` | `22` | `135` |
| `951`-`1000` | `40` | `398` | `14` | `149` |

### ⚠ **E IL BRACCIO ACCESO CRESCE ACCELERANDO FINO AL PASSO `1000`**, come il criterio chiede di dichiarare accanto a `R`: le ultime quattro finestre danno ### **`267`, `333`, `362`, `398`** divisioni.

## ⛔ DOMANDA `3`: **perche' accelera -- l'ipotesi del DIPOLO**

| | `_AMP = 0` | `_AMP = 0.3` |
|---|--:|--:|
| archi con spinta oltre `π`, **totale** | `455773` | `817694` |
| di cui dalla **FASE** sola | `2958` | `24231` |
| di cui dal **DIPOLO** solo | `452466` | `789654` |
| di cui da **ENTRAMBE** | `349` | `3809` |
| ### **la frazione CON la componente di dipolo** | `0.9935` | `0.9704` |
| `Σ |Δdipolo|` | `3024458.3715` | `5141995.4926` |
| cambi di `chi_torsione` *(### **cio' che ENTRA nel dipolo**)* | `13786` | `6592` |
| cambi di `perc_geom` *(il basculamento)* | `23363` | `74685` |
| cambi di `perc_chi` *(### **cio' che il mandato NOMINA**)* | `91552` | `7358` |
| `Σ |calcio|` ai genitori *(`KICK_TW`)* | `231.2877` | `1363.8543` |
| quanti calci | `1130` | `6992` |
| ### **`Spearman`**(cambi di `chi_torsione`, archi oltre `4π`) | `0.9090` *(n=608)* | `0.6961` *(n=269)* |
| ### ⛔ **passi ESCLUSI dalla correlazione** *(`chi_torsione` non confrontabile)* | `392` su `1000` | `731` su `1000` |
| ### ⚠ **spinta ESATTAMENTE `π`** *(che `> π` NON conta)* | `0` | `0` |

> ### ✔ **`_AMP = 0`: l'ipotesi del dipolo e' ### CONFERMATA** -- frazione col dipolo `0.9935`, correlazione `0.9090`.
> ### ✔ **`_AMP = 0.3`: l'ipotesi del dipolo e' ### CONFERMATA** -- frazione col dipolo `0.9704`, correlazione `0.6961`.
>
> ### ⛔ **E LA CORRELAZIONE E' CALCOLATA SU UNA SERIE BUCATA:** il gancio `chi_tors` ### **non puo' confrontare quando nascono nodi** *(la lunghezza cambia)*, e in quei passi lasciava uno ### **ZERO FALSO.** Sono ### **il 39 %** dei passi nel braccio zero e ### **il 73 %** nell'acceso. ### **Quei passi sono ESCLUSI qui**, invece di entrare come zeri -- ### **ma la correlazione resta una misura su una serie BUCATA**, e una lettura <<REFUTATA>> che si appoggiasse su di essa ### **andrebbe pesata per questo.**
>
> ### ⛔ **E LA CONGIUNZIONE E' UNA <<E>>, NON UNA <<O>>:** `CONFERMATA` vuole ### **frazione `>= 70 %` E correlazione `>= 0.5`**, e basta che una manchi perche' non lo sia. `REFUTATA` vuole la frazione ### **sotto il 30 %.**

## ⛔ DOMANDA `2`: **DOVE cresce la rete**

La classe e' ### **derivata dalla scena**, non scelta: `MATERIA` e' `u <= 1` *(il test di appartenenza ### **della scena**)*, `BORDO` e' `u <= 1 + R_CONN/r_regione = 1.5859` *(`R_CONN` e' ### **il varco** della scena)*, `VUOTO` il resto.

### ⛔ **E LA FRAZIONE DI NASCITE SI CONFRONTA CON QUELLA DI NODI, non col volume:** altrimenti *«nascono nel vuoto»* direbbe soltanto *«il vuoto e' piu' grande»*. Lo dice il mandato.

#### `_AMP = 0`

| finestra | nascite | ### **MATERIA**: nascite / nodi = ### **rapporto** | ### **BORDO**: nascite / nodi = ### **rapporto** | ### **VUOTO**: nascite / nodi = ### **rapporto** |
|---|--:|---|---|---|
| `1`-`100` | `0` | `n/d` / `0.0967` = ### **`n/d`** | `n/d` / `0.2713` = ### **`n/d`** | `n/d` / `0.6319` = ### **`n/d`** |
| `101`-`200` | `0` | `n/d` / `0.0969` = ### **`n/d`** | `n/d` / `0.2688` = ### **`n/d`** | `n/d` / `0.6343` = ### **`n/d`** |
| `201`-`300` | `48` | `0.0000` / `0.0936` = ### **`0.0000`** | `0.1667` / `0.2722` = ### **`0.6122`** | `0.8333` / `0.6342` = ### **`1.3140`** |
| `301`-`400` | `55` | `0.0000` / `0.0894` = ### **`0.0000`** | `0.2000` / `0.2877` = ### **`0.6952`** | `0.8000` / `0.6229` = ### **`1.2844`** |
| `401`-`500` | `104` | `0.0673` / `0.0980` = ### **`0.6867`** | `0.4231` / `0.2965` = ### **`1.4267`** | `0.5096` / `0.6054` = ### **`0.8417`** |
| `501`-`600` | `150` | `0.0267` / `0.1099` = ### **`0.2427`** | `0.4467` / `0.3120` = ### **`1.4318`** | `0.5267` / `0.5782` = ### **`0.9109`** |
| `601`-`700` | `94` | `0.0745` / `0.1235` = ### **`0.6030`** | `0.2766` / `0.3255` = ### **`0.8496`** | `0.6489` / `0.5510` = ### **`1.1778`** |
| `701`-`800` | `120` | `0.1583` / `0.1405` = ### **`1.1271`** | `0.3583` / `0.3384` = ### **`1.0590`** | `0.4833` / `0.5212` = ### **`0.9274`** |
| `801`-`900` | `138` | `0.1522` / `0.1559` = ### **`0.9759`** | `0.2174` / `0.3457` = ### **`0.6288`** | `0.6304` / `0.4984` = ### **`1.2650`** |
| `901`-`1000` | `118` | `0.1102` / `0.1669` = ### **`0.6603`** | `0.3136` / `0.3394` = ### **`0.9237`** | `0.5763` / `0.4937` = ### **`1.1673`** |

> ### ⚠ **NESSUNA CLASSE E' SOVRARAPPRESENTATA** col criterio fissato *(`>= 2` volte, in `>= 2` finestre su `3`)*: ### **le nascite seguono i nodi**, cioe' ### **la rete cresce dove c'e' rete**, senza preferire un luogo.

#### `_AMP = 0.3`

| finestra | nascite | ### **MATERIA**: nascite / nodi = ### **rapporto** | ### **BORDO**: nascite / nodi = ### **rapporto** | ### **VUOTO**: nascite / nodi = ### **rapporto** |
|---|--:|---|---|---|
| `1`-`100` | `0` | `n/d` / `0.0967` = ### **`n/d`** | `n/d` / `0.2713` = ### **`n/d`** | `n/d` / `0.6319` = ### **`n/d`** |
| `101`-`200` | `0` | `n/d` / `0.0969` = ### **`n/d`** | `n/d` / `0.2688` = ### **`n/d`** | `n/d` / `0.6343` = ### **`n/d`** |
| `201`-`300` | `143` | `0.0350` / `0.0934` = ### **`0.3742`** | `0.1888` / `0.2722` = ### **`0.6937`** | `0.7762` / `0.6344` = ### **`1.2236`** |
| `301`-`400` | `298` | `0.1040` / `0.0890` = ### **`1.1682`** | `0.2416` / `0.2878` = ### **`0.8395`** | `0.6544` / `0.6232` = ### **`1.0501`** |
| `401`-`500` | `374` | `0.1364` / `0.0996` = ### **`1.3685`** | `0.3075` / `0.2947` = ### **`1.0434`** | `0.5561` / `0.6057` = ### **`0.9182`** |
| `501`-`600` | `649` | `0.1032` / `0.1130` = ### **`0.9133`** | `0.3313` / `0.3062` = ### **`1.0819`** | `0.5655` / `0.5808` = ### **`0.9737`** |
| `601`-`700` | `628` | `0.0876` / `0.1274` = ### **`0.6875`** | `0.3965` / `0.3190` = ### **`1.2431`** | `0.5159` / `0.5536` = ### **`0.9319`** |
| `701`-`800` | `789` | `0.1318` / `0.1399` = ### **`0.9421`** | `0.3181` / `0.3287` = ### **`0.9679`** | `0.5501` / `0.5314` = ### **`1.0351`** |
| `801`-`900` | `836` | `0.1758` / `0.1464` = ### **`1.2013`** | `0.3266` / `0.3338` = ### **`0.9783`** | `0.4976` / `0.5198` = ### **`0.9573`** |
| `901`-`1000` | `1044` | `0.1025` / `0.1489` = ### **`0.6883`** | `0.3065` / `0.3191` = ### **`0.9605`** | `0.5910` / `0.5320` = ### **`1.1109`** |

> ### ⚠ **NESSUNA CLASSE E' SOVRARAPPRESENTATA** col criterio fissato *(`>= 2` volte, in `>= 2` finestre su `3`)*: ### **le nascite seguono i nodi**, cioe' ### **la rete cresce dove c'e' rete**, senza preferire un luogo.

### DIVISIONI e SCHWINGER, **separate** *(lo chiede il mandato)*

| braccio | finestra | divisioni per classe | Schwinger per classe |
|---|---|---|---|
| `0` | `701`-`800` | 14 / 31 / 36 | 5 / 12 / 22 |
| `0` | `801`-`900` | 15 / 20 / 57 | 6 / 10 / 30 |
| `0` | `901`-`1000` | 10 / 26 / 46 | 3 / 11 / 22 |
| `0.3` | `701`-`800` | 79 / 182 / 322 | 25 / 69 / 112 |
| `0.3` | `801`-`900` | 100 / 197 / 303 | 47 / 76 / 113 |
| `0.3` | `901`-`1000` | 80 / 227 / 453 | 27 / 93 / 164 |

*(l'ordine e' `MATERIA / BORDO / VUOTO`.)*

### GLI ARCHI OLTRE `4π`, **come POPOLAZIONE** *(ai passi pieni)*

### ⛔ **MAI gli indici:** `ARCHI-OLTRE-4PI` e' ### **<<da non indagare>> per decisione di Luca**, e il mandato lo ripete. ### **Si contano le popolazioni, non gli individui.**

| braccio | passo | archi | nodi | per classe | `u` mediano | `rho_spin` rel. mediana |
|---|--:|--:|--:|---|--:|--:|
| `0` | `50` | `0` | `None` |  | `n/d` | `n/d` |
| `0` | `150` | `0` | `None` |  | `n/d` | `n/d` |
| `0` | `300` | `0` | `None` |  | `n/d` | `n/d` |
| `0` | `600` | `3` | `6` | 1 / 2 / 3 | `1.3823` | `1.3869` |
| `0` | `1000` | `47` | `79` | 12 / 13 / 54 | `2.2972` | `0.3785` |
| `0.3` | `50` | `0` | `None` |  | `n/d` | `n/d` |
| `0.3` | `150` | `0` | `None` |  | `n/d` | `n/d` |
| `0.3` | `300` | `6` | `7` | 0 / 0 / 7 | `1.9745` | `3.2914` |
| `0.3` | `600` | `7` | `11` | 1 / 2 / 8 | `2.3349` | `1.3473` |
| `0.3` | `1000` | `364` | `529` | 44 / 85 / 400 | `2.6106` | `0.3044` |

## IL VERDETTO

| la domanda | l'esito |
|---|---|
| `1` la crescita e' del modello? | ### **INTERMEDIA** |
| `3` l'ipotesi del dipolo | zero: ### **CONFERMATA** · acceso: ### **CONFERMATA** |
| `2` dove cresce la rete | zero: ### **NESSUNA** · acceso: ### **NESSUNA** |

> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** ### **il `0.3`, la soglia `3π`, `κ` e la legge del basculamento chirale si decidono su questi numeri, e sono DECISIONI DI LUCA.**

> ### ⚠ **E UN LIMITE CHE VALE PER TUTTO IL REFERTO:** ### **un seme solo.** Nessuna barra d'errore fra semi, e `P3` ne chiederebbe ### **almeno quattro.** ### **Il gradino raggiunto e' `(b)`** *(«regge togliendo la legge pratica»)*, ### **non `(a)` ne' `(c)`.**

---

*Referto **generato** da `csv/_test_fork/_referto_mzd.py` dai due `json`: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`), e i criteri sono letti **dalle soglie fissate nel task history**.*
