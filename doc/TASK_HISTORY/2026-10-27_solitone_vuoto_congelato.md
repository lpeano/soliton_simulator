# IL SOLITONE COL VUOTO CONGELATO: E' LA RISPOSTA DEL VUOTO A DISFARLO? *(la parte 1 del mandato del 2026-10-27, con i due zeri)*

> **Il mandato:** di Luca, `2026-10-27` *([[SOLITONI-TRIANGOLI]], [[PROGETTO-MASSA-COLLETTIVA]], [[INDIRIZZO-MASSA-COLLETTIVA]])*: ### **la lettura da provare** *(`bcbd1f40`, mia)*: ### **«il risolutore tiene il vuoto FISSO; nel tick il vuoto risponde e il legame che teneva il solitone non tiene piu'».**
> ### **In memoria; nessun file del nucleo; nessuna scelta fra `S1` e `S4`, ne' fra i due zeri.** ### **Lo script `csv/_solitone_vuoto_congelato.py`, il referto `doc/referti_l2/solitone_vuoto_congelato.{txt,jsonl}`.**

**LIVELLO:** una misura dinamica con due controlli.

## 0. LA STELLA POLARE

1. **`A14`:** ### **le norme si conservano** *(si controllano)*. 2. **Il gradino:** ### **chi disfa il solitone.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Il vuoto sotto la materia.** 5. **Emergente o imposto?** ### **La causa del disfarsi e' cio' che si misura.**

## 1. LA SCENA *(quella di `bcbd1f40`, `csv/_solitoni_triangoli.py`, importato)*

- ### **`S1`, `s 0.3`, `LAM0 6`; `N 1e6` a `L 81` e `120`, `N 1e5` a `L 48` e `69`** *(gli `L` di `dinamica`: `3 ceil(f w0/3)`, `f = 12, 18`)*; ### **lo stato di partenza del risolutore; `T_MAX 2000`, le misure ogni `20` tick; la rotazione al centro a ogni tick; la vita col criterio di allora** *(la larghezza entro `+-20%`, la frazione entro `3 w0` `>= 0.8`)*.

## 2. LE TRE CORSE E I DUE ZERI *(dichiarati qui)*

| | la corsa | che cosa gira |
|---|---|---|
| `(a)` | ### **il tick INTERO** | ### **`tick.percorri_tick` con `salta` vuoto** *(= `tick.tick`)* |
| `(b)` | ### **il VUOTO CONGELATO** | ### **saltati `CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`, `CAMM-FASE-VUOTO`;** ### **e `phi` RIMESSO al suo valore dell'istante zero dopo ogni tick** *(il legame `CAMM-MATERIA-VUOTO` gira e mette la sua fase anche su `phi`: rimettendolo, il vuoto che il legame legge e' ESATTAMENTE quello dell'istante zero)*; ### **la materia avanza col resto del tick.** ### **Il controllo: `Lambda` per nodo uguale AL BIT all'istante zero, a ogni misura** |
| `(c)` | ### **la materia SENZA legame** | ### **saltato `CAMM-MATERIA-VUOTO`** *(la materia sola, lineare; il vuoto gira ma non tocca la materia)* |

- ### **I DUE ZERI:** ### **OGGI = il nucleo** *(nessun cambiamento)*; ### **SIMMETRICO = `_zero_simmetrico.convenzione_simmetrica()`** *(attraverso `_triangoli_bassa_energia.conv("simm")`: in memoria `flussi_parziali.grover`, `hop_psi`, `hop_phi` sono composti col pezzo di oggi a `f/2` e quello dell'alternativa a `f/2`; e' il modo delle misure di gravita' sui triangoli)*.
- ### **IL CONTROLLO DELLO ZERO** *(vuoto e legame spenti: saltati i quattro pezzi del vuoto e il legame; `s` uniforme; uno stato casuale su un toro `12 x 12`, `50` tick)*: ### **la densita' per nodo con i due zeri.** ### ⚠ **NON «AL BIT», ed e' gia' misurato** *(una prova di costruzione: lo scarto massimo `1.75e-12` su `43.6`, cioe' `4e-14` relativo)*: ### **la composizione dei mezzi pezzi arrotonda in modo diverso da un pezzo intero; lo zero e' una fase globale in aritmetica esatta, non nei bit.** ### **Il criterio: entro `1e-12` relativo** *(la previsione del guardiano diceva «al bit»: lo dico)*.
- ### **LA RISPOSTA DEL VUOTO in `(a)`:** ### **`Lambda` per estremita' al nodo centrale e a un nodo lontano** *(l'angolo del toro)* ### **a ogni misura, e la velocita' del cambiamento** *(la pendenza nei primi `200` tick)*.

## 3. I CRITERI *(del mandato, con la soglia dello zero dichiarata sopra)*

| | il criterio | il tipo |
|---|---|---|
| `1` | ### **`(a)` con lo zero di oggi ridà la vita di `bcbd1f40` entro il `20%`** *(`320` e `140` tick)* ### **e la rotazione `-1.101` entro `1e-2`, a ogni taglia** | DEVE |
| `2` | ### **`M` e `V` conservati entro `1e-10` relativo in ogni corsa; in `(b)` `Lambda` per nodo AL BIT** | DEVE |
| `3` | ### **il controllo dello zero: la densita' fra i due zeri entro `1e-12` relativo** | DEVE |
| `4` | ### **`(b)` vive almeno `4` volte piu' di `(a)`, e la larghezza resta entro il `20%` fino a `T_MAX`** *(lo zero di oggi, le due taglie)* | PUO' FALLIRE |
| `5` | ### **`(c)` si disperde piu' in fretta di `(a)`** *(la vita di `(c)` minore, lo zero di oggi, le due taglie)* | PUO' FALLIRE |

### **LA LETTURA, nessuna soglia:** ### **lo zero simmetrico contro quello di oggi, in `(a)` e in `(b)`.** ### **LA CONVERGENZA:** ### **un verdetto vale se le due taglie danno lo stesso verdetto e la vita entro il `20%`.** ### **Mi FERMO** ### **se `1`, `2` o `3` fallisce.** ### **LA PARTE `2`** *(la scomposizione)* ### **SOLO se `(b)` trova un oggetto stabile.**

## 3-bis. ANNOTAZIONE, PRIMA DEL COMMIT DELLO SCRIPT *(una prova di costruzione da una cartella pulita, NON il referto)*

- ### **IL CONTROLLO DELLO ZERO:** ### **`4.0e-14` relativo, non al bit** *(come gia' scritto sopra)*.
- ### **`N 1e5`, `L 48`, zero di oggi, `200` tick:** ### **`(a)` vita `140`** *(come `bcbd1f40`)*, ### **e `Lambda` per estremita' al centro sale da `1.000` a `1.530`: il vuoto sotto il solitone SI RIEMPIE;** ### **`(b)` STABILE fino a `200`** *(la larghezza `3.81 -> 4.03`; `Lambda` al bit)*; ### **`(c)` vita `80`** *(`Lambda` resta `1.000` al bit: senza legame il vuoto uniforme non risponde)*; ### **`M` e `V` a `3e-14`.** ### **Le soglie restano.**

## 4. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice.
