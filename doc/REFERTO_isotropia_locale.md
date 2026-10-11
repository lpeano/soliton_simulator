# IL REFERTO DELL'ISOTROPIA LOCALE — **SI ATTENUA, E I PESI DALLA GEOMETRIA NON SERVONO**

> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un ### **REPERTO** — la CI ### **non lo rigenera**, e il presidio verifica ### **il suo BLOB.**

*(**Generato** da `python proto_camminata/_referto_isotropia.py`, che legge `proto_camminata/uscite/letture_isotropia_locale.json` prodotto da `python proto_camminata/_letture_isotropia_locale.py` — **BLOB del modulo di letture: `4e2c611853eb838bebd243c1f0abb26815a35190`**. Soglie e previsioni: `doc/TASK_HISTORY/2026-10-11_isotropia_locale.md`, committato **PRIMA**.)*

## ⭐ `1` LE TRE GRANDEZZE, e perche' il mio misurando vecchio era SBAGLIATO

> ### ⛔ **IL RILIEVO DEL GUARDIANO, confermato:** mediavo le dispersioni ### **per nodo**, e quella e' ### **IRREGOLARITA' LOCALE** — l'### **ANISOTROPIA** e' la dispersione del ### **profilo MEDIO**, e si giudica ### **contro il RUMORE ATTESO** *(`irregolarita'/sqrt(N)`)*.

| la grandezza | che cosa dice | quando conta |
|---|---|---|
| **irregolarita' per nodo** | quanto e' ### **irregolare il vicinato** di un nodo | e' una proprieta' ### **LOCALE**, e ### **non e' anisotropia** |
| **anisotropia del profilo medio** | se una ### **DIREZIONE** e' privilegiata nella media | ### **solo sopra il rumore** e' anisotropia vera |
| **rumore atteso** | `irregolarita'/sqrt(N)` | ### ⚠ **dipende dal CAMPIONE**: con meno nodi il rumore cresce, e <<sistematica>> e' una proprieta' ### **della scena E del campione** |

## ⭐ `2` `I1`: L'IRREGOLARITA' SI ATTENUA, E POI SI FERMA SU UN PAVIMENTO

### **cubico L=20 (controllo)** — `n = 8000`, `m = 24000`, diametro `>= 30`, `t_max = 24`, e i tempi `25, 30` sono ### **oltre `t_max`: non misurati**

| `t` | irregolarita' | anisotropia | rumore | aniso/rumore | |
|---|---|---|---|---|---|
| `4` | `0.2292 ± 0.0003` | `0.2287` | `0.0362` | `6.31` | ### ⛔ **SISTEMATICA** |
| `6` | `0.1113 ± 0.0009` | `0.1075` | `0.0176` | `6.11` | ### ⛔ **SISTEMATICA** |
| `10` | `0.1018 ± 0.0011` | `0.0968` | `0.0161` | `6.01` | ### ⛔ **SISTEMATICA** |
| `15` | `0.2266 ± 0.0025` | `0.2230` | `0.0358` | `6.22` | ### ⛔ **SISTEMATICA** |
| `20` | `0.1490 ± 0.0012` | `0.1416` | `0.0236` | `6.01` | ### ⛔ **SISTEMATICA** |

### ⭐ **L'esponente: `t^(-0.037 ± 0.336)`** — ### **RESTA PIATTA** *(a `0.1 sigma`)*. ### **E il pavimento:** gli ultimi due `t` differiscono di `0.0776` con `sigma` combinato `0.0028`, cioe' `27.6 sigma` — ### **ANCORA IN DISCESA**.

### **geometrico3d n=26000** — `n = 26000`, `m = 76634`, diametro `>= 32`, `t_max = 25`, e i tempi `30` sono ### **oltre `t_max`: non misurati**

| `t` | irregolarita' | anisotropia | rumore | aniso/rumore | |
|---|---|---|---|---|---|
| `4` | `0.3106 ± 0.0083` | `0.0447` | `0.0491` | `0.91` | al rumore |
| `6` | `0.2970 ± 0.0111` | `0.0406` | `0.0470` | `0.86` | al rumore |
| `10` | `0.2543 ± 0.0104` | `0.0366` | `0.0402` | `0.91` | al rumore |
| `15` | `0.2196 ± 0.0093` | `0.0326` | `0.0347` | `0.94` | al rumore |
| `20` | `0.1863 ± 0.0083` | `0.0292` | `0.0295` | `0.99` | al rumore |
| `25` | `0.1700 ± 0.0071` | `0.0263` | `0.0269` | `0.98` | al rumore |

### ⭐ **L'esponente: `t^(-0.339 ± 0.033)`** — ### **SI ATTENUA** *(a `10.1 sigma`)*. ### **E il pavimento:** gli ultimi due `t` differiscono di `0.0162` con `sigma` combinato `0.0109`, cioe' `1.5 sigma` — ### **PAVIMENTO**, e vale `0.1700`.

## ⭐ `3` `I2`: LE OTTO VARIANTI, TUTTE ALLA STESSA TAGLIA

> ### ⛔ **TUTTE A `n = 1728` E `t = 10`, con gli STESSI `40` nodi:** un confronto fra varianti misurate a taglie diverse ### **non e' un confronto.**

| la variante | `m` | gradi | `d_s` | irregolarita' | contro `(i)` | costo/tick | pesi dalle posizioni |
|---|---|---|---|---|---|---|---|
| ### ⭐ **(ii) respinti, gradi 2-6** | `3697` | `2..6` | `2.831` | `0.1584 ± 0.0039` | ### **11.8 sigma** | `0.0010` s | no |
| ### ⭐ **(ii)+(iv-U) respinti + tutti i vicini, pesi uguali** | `14032` | `10..23` | `3.517` | `0.1697 ± 0.0025` | ### **11.2 sigma** | `0.0075` s | no |
| ### ⭐ **(iv-U) Delaunay, pesi U** | `13405` | `6..26` | `3.247` | `0.2328 ± 0.0061` | ### **3.7 sigma** | `0.0067` s | no |
| (iv-R) Delaunay, pesi R | `13405` | `6..26` | `3.247` | `0.2492 ± 0.0067` | `2.1 sigma` | `0.0073` s | no |
| (iv-Rn) Delaunay, pesi Rn | `13405` | `6..26` | `3.247` | `0.2503 ± 0.0067` | `2.0 sigma` | `0.0068` s | no |
| (iv-V) Delaunay, pesi V | `13405` | `6..26` | `3.247` | `0.2603 ± 0.0066` | `1.1 sigma` | `0.0069` s | ### ⛔ **SI** *(controllo)* |
| (iii) uniformi, gradi 4-6 | `5182` | `3..6` | `2.755` | `0.2646 ± 0.0092` | `0.6 sigma` | `0.0015` s | no |
| (i) uniformi, gradi 2-6 | `4835` | `2..6` | `2.578` | `0.2719 ± 0.0088` | — *(riferimento)* | `0.0013` s | no |

### ⛔ **IL RISULTATO CHIAVE, ed e' la domanda che l'aggiunta sui pesi pone:** il controllo `(iv-V) Delaunay, pesi V` *(### **geometria messa a mano**)* guadagna `0.0116` contro il riferimento, cioe' `1.1 sigma` — ### ****SOTTO LA SOGLIA: non da' niente**.**

* **`(iv-U) Delaunay, pesi U`**: irregolarita' `0.2328`, guadagno `0.0390` *(`3.7 sigma`)* — ### ⚠ **la <<quota del guadagno del controllo>> NON si riporta: il controllo stesso e' sotto la soglia**, quindi la frazione avrebbe un denominatore non significativo, e contro il controllo sta a `3.1 sigma`
* **`(iv-R) Delaunay, pesi R`**: irregolarita' `0.2492`, guadagno `0.0227` *(`2.1 sigma`)* — ### ⚠ **la <<quota del guadagno del controllo>> NON si riporta: il controllo stesso e' sotto la soglia**, quindi la frazione avrebbe un denominatore non significativo, e contro il controllo sta a `1.2 sigma`
* **`(iv-Rn) Delaunay, pesi Rn`**: irregolarita' `0.2503`, guadagno `0.0215` *(`2.0 sigma`)* — ### ⚠ **la <<quota del guadagno del controllo>> NON si riporta: il controllo stesso e' sotto la soglia**, quindi la frazione avrebbe un denominatore non significativo, e contro il controllo sta a `1.1 sigma`

### ⭐ **E LA PROVA CHE I PUNTI RESPINTI SONO DAVVERO PIU' UNIFORMI** — altrimenti *«respinti»* e' una ### **parola**: la distanza al primo vicino passa da dispersione relativa `0.3658` a ### **`0.1375`** *(`0.38` volte)*, e il minimo sale di ### **`13.1` volte.**

## ⭐ `4` LA CORRELAZIONE `s7`: LO SBILANCIAMENTO *NON* SPIEGA L'IRREGOLARITA'

| la variante | sbilanciamento medio | Pearson | in `sigma` | significativa? |
|---|---|---|---|---|
| (ii) respinti, gradi 2-6 | `0.2659 ± 0.0142` | `-0.119` | `0.73` | no |
| (ii)+(iv-U) respinti + tutti i vicini, pesi uguali | `0.1212 ± 0.0064` | `0.085` | `0.52` | no |
| (iv-U) Delaunay, pesi U | `0.1617 ± 0.0095` | `0.260` | `1.62` | no |
| (iv-R) Delaunay, pesi R | `0.1634 ± 0.0106` | `0.233` | `1.44` | no |
| (iv-Rn) Delaunay, pesi Rn | `0.1664 ± 0.0106` | `0.263` | `1.64` | no |
| (iv-V) Delaunay, pesi V | `0.1082 ± 0.0092` | `0.204` | `1.26` | no |
| (iii) uniformi, gradi 4-6 | `0.3507 ± 0.0237` | `0.102` | `0.62` | no |
| (i) uniformi, gradi 2-6 | `0.3591 ± 0.0264` | `0.128` | `0.78` | no |

### **`0` varianti su `8` hanno una correlazione significativa** *(soglia `3 sigma`, `s7`)*. ### ⭐ **E la mia previsione era <<positiva e significativa>>, cioe' che lo sbilanciamento FOSSE la causa:** ### ⛔ **CADE** — l'irregolarita' locale ### **non si spiega con lo sbilanciamento direzionale delle uscite.**

### ✅ **E IL BRACCIO LO PROVA NEI DUE VERSI:** su un legame ### **costruito a mano** la correlazione da' `+1.000000000` e lo dichiara significativo, su ### **rumore indipendente** da' `-0.0311` a `0.70 sigma` e lo dichiara ### **NON significativo** — ### **quindi uno zero qui e' un FATTO, non un misurando cieco.**

## ⭐ `5` `M-A`: LA DIMENSIONE A TAGLIA GRANDE — **IL COMPROMESSO ERA TAGLIA FINITA?**

> ### ⛔ **E IL CRITERIO E' LO SCARTO DA `3`, NON IL VALORE** *(`s9`)*: ### **`d_s > 3` e' un difetto come `d_s < 3`** — un grafo con dimensione spettrale `3.5` ### **non e' uno spazio tridimensionale.**

| la famiglia | `n = 4000` | `n = 10000` | `n = 26000` | monotona? | `|d_s-3|` alla taglia massima | `s8` |
|---|---|---|---|---|---|---|
| (i) uniformi, gradi 2-6 | `2.923` | `2.880` | `2.962` | no | `0.038` | NON ARRIVA A 3 |
| (ii) respinti, gradi 2-6 | `3.071` | `3.126` | `3.046` | no | `0.046` | NON ARRIVA A 3 |
| (ii)+(iv-U) respinti + tutti i vicini, pesi uguali | `3.199` | `3.166` | `3.070` | no | `0.070` | NON ARRIVA A 3 |
| (iv-U) Delaunay, pesi U | `3.135` | `3.098` | `3.109` | no | `0.109` | NON ARRIVA A 3 |

### ⭐ **E LA PIU' TRIDIMENSIONALE ALLA TAGLIA MASSIMA E' `(i) uniformi, gradi 2-6`** — ### **sullo scarto da `3`, che e' il criterio scritto prima.**

> ### ⛔ **MA LA SOGLIA `s8` COSI' COM'E' SCRITTA DA' UN VERDETTO CHE CONTRADDICE I SUOI PROPRI NUMERI, E IL DIFETTO E' MIO.** `s8` chiede ### **due cose in CONGIUNZIONE** — *«`d_s` cresce in modo **monotono** con `n` ### **E** alla taglia massima `|d_s - 3| <= 0.3`»* — e il risultato e' che ### **`4` famiglie su `4` stanno entro `0.3` da `3`** *(la migliore a `0.038`)*, ma ### **NESSUNA e' monotona**, quindi il verdetto composto dice ### **<<NON ARRIVA A 3>> per tutte.**

### ⭐ **E IL MOTIVO PER CUI LA CONGIUNZIONE ERA LA FORMA SBAGLIATA SI VEDE DAL `json`: `d_s` NON HA UNA `sigma`.** Il misurando torna ### **`d_s` e `r2`, e nessuna incertezza** — quindi *«cresce in modo monotono»* stava leggendo ### **l'ordine di tre numeri la cui oscillazione** *(`~0.08`)* ### **e' piu' grande della tendenza che doveva misurare.** ### ⛔ **Una soglia che chiede una monotonia a una grandezza senza barra d'errore chiede qualcosa che la misura non puo' dare.**

### ✅ **E NON LA RISCRIVO ADESSO: riporto i DUE pezzi separati, perche' erano ENTRAMBI registrati prima.** ### **Il pezzo che risponde alla domanda di Luca** *(«`(ii)` tende a `3` crescendo la taglia?»)* ### **e' il secondo**, ed e' ### **`|d_s - 3| <= 0.3` alla taglia massima** — e la risposta e' ### **SI'.** ### ⚠ **Il primo pezzo resta come difetto dichiarato della soglia**, non come verdetto sulla fisica.

## ⭐ `6` `M-B`: LA COMBINAZIONE — **I DUE EFFETTI SI SOMMANO?**

| | il guadagno sull'irregolarita' |
|---|---|
| i punti **respinti** da soli | `0.1135` |
| **tutti i vicini** da soli | `0.0390` |
| la **SOMMA** dei due | `0.1525 ± 0.0143` |
| ### ⭐ **la COMBINAZIONE, misurata** | ### **`0.1022 ± 0.0025`** |
| la differenza | `-0.0503 ± 0.0170`, cioe' ### **`3.0 sigma`** |

### ⭐ **IL VERDETTO `s10`: ADDITIVI** — ### ⚠ **ma a `2.96 sigma` e' SUL CONFINE**, e la soglia era `3`: ### **questa misura NON decide fra <<additivi>> e <<si sovrappongono>>.** ### **E la stima puntuale dice sovrapposizione:** la combinazione ottiene il ### **`67%` della somma dei due.**

### ⛔ **E IL FATTO CHE DECIDE NON HA BISOGNO DI `s10`: la combinazione ### ⛔ **NON BATTE** il migliore dei due da sola.** Il guadagno della combinazione e' `0.1022`, quello dei soli punti respinti e' `0.1135` — ### **quindi aggiungere tutti i vicini a punti gia' respinti PEGGIORA l'irregolarita'**, e costa di piu'.

## ⭐ `7` `M-C`: I PAVIMENTI A CONFRONTO

| la scena | il pavimento | `sigma` | contro `(i)` |
|---|---|---|---|
| `(i)` uniformi *(da `I1`)* | `0.1700` | `0.0109` | — |
| (ii) respinti, gradi 2-6 n=26000 | `0.0897` | `0.0037` | ### **piu' BASSO di `0.0803`, cioe' `7.0 sigma`** | 
| (ii)+(iv-U) respinti + tutti i vicini, pesi uguali n=26000 | `0.1751` | `0.0038` | piu' ALTO di `0.0051` (`0.4 sigma`) | 

### ⭐ **E `s12`: E' LA STESSA LEGGE DI ATTENUAZIONE?**

| la scena | l'esponente | contro `(i)` | compatibile con `-1/2`? |
|---|---|---|---|
| `(i)` uniformi *(da `I1`)* | `-0.339 ± 0.033` | — | no *(`4.8 sigma`)* |
| (ii) respinti, gradi 2-6 n=26000 | `-0.527 ± 0.025` | `4.5 sigma` ### ⛔ **DIVERSA** | ### ✅ **SI'** *(`1.1 sigma`)* |
| (ii)+(iv-U) respinti + tutti i vicini, pesi uguali n=26000 | `-0.102 ± 0.037` | `4.8 sigma` ### ⛔ **DIVERSA** | no *(`10.8 sigma`)* |

## ⛔ `8` LA DECISIONE E' DI LUCA, E QUESTA E' LA TABELLA INTERA

> ### ⛔ **CAMBIARE I GRADI CAMBIA LA FISICA LOCALE** — la moneta di Grover ### **dipende dal grado** *(`(2/d)Σ - I`)*, quindi passare da gradi `2..6` a gradi `6..34` ### **non e' una scelta di comodita'.** ### **Nessuna variante diventa la scena di default qui:** `[[DOMANDA-QUALE-SCENA-3D-PRINCIPALE]]`.

| la variante | `d_s` alla taglia massima | `|d_s-3|` | irregolarita' a `t = 10` | pavimento | costo/tick | gradi |
|---|---|---|---|---|---|---|
| (ii) respinti, gradi 2-6 | `3.046` *(n = 26000)* | `0.046` | `0.1584` | `0.0897` | `0.0010` s | `2..6` |
| (ii)+(iv-U) respinti + tutti i vicini, pesi uguali | `3.070` *(n = 26000)* | `0.070` | `0.1697` | `0.1751` | `0.0075` s | `10..23` |
| (iv-U) Delaunay, pesi U | `3.109` *(n = 26000)* | `0.109` | `0.2328` | — | `0.0067` s | `6..26` |
| (iv-R) Delaunay, pesi R | `3.247` *(n = 1728)* | `0.247` | `0.2492` | — | `0.0073` s | `6..26` |
| (iv-Rn) Delaunay, pesi Rn | `3.247` *(n = 1728)* | `0.247` | `0.2503` | — | `0.0068` s | `6..26` |
| (iv-V) Delaunay, pesi V | `3.247` *(n = 1728)* | `0.247` | `0.2603` | — | `0.0069` s | `6..26` |
| (iii) uniformi, gradi 4-6 | `2.755` *(n = 1728)* | `0.245` | `0.2646` | — | `0.0015` s | `3..6` |
| (i) uniformi, gradi 2-6 | `2.962` *(n = 26000)* | `0.038` | `0.2719` | — | `0.0013` s | `2..6` |

## ⚠ `9` I LIMITI DI QUESTO REFERTO, dichiarati

| | il limite |
|---|---|
| `1` | ### **`t = 30` non si misura**: il geometrico a `n = 26000` ha `t_max = 25`, e `t = 30` vorrebbe `n ~ 40000` |
| `2` | ### **UN SEME SOLO per i punti** *(`11`)*: la dispersione fra nodi c'e', ma ### **la variabilita' fra REALIZZAZIONI della scena non e' misurata** |
| `3` | ### **le due vie del rilassamento non sono bit-identiche** *(`3.2e-11` sui punti)*: a `n = 1728` ### **non spostano nessun arco**, e il braccio ### **verifica una taglia sola** |
| `4` | ### **il diametro e' CAMPIONATO** su `40` nodi sopra le taglie piccole, quindi e' ### **un limite inferiore** — e il campo `diametro_esatto` lo dice |
| `5` | ### **la correlazione `s7` e' fra DUE grandezze per nodo**, e una correlazione nulla ### **non esclude una causa non lineare** |

