# IL REFERTO DEL LEGAME — **PERCHE' NESSUN GRUMO STA INSIEME**

> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un ### **REPERTO** — la CI ### **non lo rigenera**, e il presidio verifica ### **il suo BLOB.**

*(**Generato** da `python proto_camminata/_referto_legame.py`, che legge `proto_camminata/uscite/letture_legame.json` prodotto da `python proto_camminata/_letture_legame.py`. Soglie e previsioni: `doc/TASK_HISTORY/2026-10-11_legame.md`, **committato PRIMA del codice** (`11b8927`).)*

> ## ⭐ **IL VERDETTO, IN UNA RIGA: LA FORMA `(D)` COL SEGNO DIRETTO **LEGA IN `1D`**, e in `3D` l'effetto **CALA CON LA TAGLIA** fino a sparire.**

> ### ⛔ **E si scrive <<LEGA IN `1D`>>, non <<lega>>**, perche' l'anello ha ### **dimensione spettrale `1.001`** — ed e' la distinzione che il mandato aveva ### **preregistrato.**

## LA CONFIGURAZIONE, INTERA *(`H-P5`)*

| | |
|---|---|
| i semi | ``11`, `23`, `37`, `53`` |
| `eps` del passo | **`0.5`** |
| la velocita' del fronte, **misurata** | **`0.6193`** archi/tick *(referto `v4`)*, e da lei viene `T_max = 2 * diametro / v` |
| la griglia di `eps` di `M0` | ``0`, `0.125`, `0.25`, `0.375`, `0.5`, `0.75`, `1``, **ridotta a `0, 0.5, 1`** dove `dim > 4500` *(il costo di `eig` e' **cubico**)* |
| la soglia di un buco | larghezza **`> 3`** spaziature *(degli stati USATI, non di `dim`)* |
| la griglia di `x0` di `M1` | ``0.125`, `0.25`, `0.5`, `1`, `2`, `4`, `8`` |
| la geometria | `scena_identita` *(e `scena_curva` nei bracci del banco)* |
| le candidate | `+N`, `-N`, `+D`, `-D`, **accendibili e mai di default**; e il **lineare** come controllo |

## ⭐ **LE DIMENSIONI E L'ISOTROPIA, MISURATE — e decidono come si legge tutto il resto**

| la scena | famiglia | `n` | diametro | **`d_s`** | `r²` | legge di potenza? |
|---|---|---|---|---|---|---|
| `cubico L=5` | 3D, da misurare | `125` | `6` | **3.039** | `0.9996` | si |
| `cubico L=8` | 3D, da misurare | `512` | `12` | **3.125** | `0.9999` | si |
| `cubico L=12` | 3D, da misurare | `1728` | `>= 18` | **3.090** | `0.9999` | si |
| `cubico L=20` | 3D, da misurare | `8000` | `>= 30` | **3.048** | `0.9999` | si |
| `geometrico3d n=512` | 3D, da misurare | `512` | `10` | **2.126** | `0.9845` | si |
| `geometrico3d n=4000` | 3D, da misurare | `4000` | `>= 19` | **2.923** | `0.9867` | si |
| `irregolare n=120` | casuale | `120` | `8` | **2.363** | `0.9935` | si |
| `irregolare n=2000` | casuale | `2000` | `>= 11` | **3.927** | `0.9831` | si |
| `regolare n=120` | 1D | `120` | `30` | **1.006** | `0.9998` | si |
| `regolare n=2000` | 1D | `2000` | `>= 500` | **1.001** | `1.0000` | si |

### ⛔ **E LE DUE SCENE DEL BANCO NON HANNO DIMENSIONE `3`:** l'anello e' ### **`1D` esatto** *(`d_s = 1.001`, `r² = 1.0000`)* e il casuale ha `d_s` che ### **CRESCE con `n`** *(`2.36` → `3.93`)*, cioe' ### **non ha una dimensione fissa.** ### **Un verdetto su quelle due non dice che cosa succede in uno spazio a tre dimensioni**, ed e' la ragione per cui le famiglie `3D` esistono.

## `M0` — **IL BUCO NELLO SPETTRO: C'E' SULL'ANELLO E SUL GEOMETRICO `3D`, NON SUL CUBICO**

| la famiglia | il verdetto | `eps` col buco | `eps` senza |
|---|---|---|---|
| **regolare (1D)** | ### ⭐ **BUCO PRESENTE E STABILE a `eps = 0.5`** | `0, 0.125, 0.25, 0.375, 0.5, 0.75, 1` | `nessuno` |
| **cubico (3D)** | ### ⛔ **NESSUN BUCO ai `eps` della fisica (solo a `eps = 0`, che e- degenere)** | `0` | `0.5, 1` |
| **geometrico3d (3D irregolare)** | ### ⭐ **BUCO PRESENTE E STABILE a `eps = 0.5`** | `0, 0.5` | `1` |
| **irregolare (casuale)** | ### ⛔ **BUCO solo a `eps` = 0, 0.125, 0.25, 0.375** | `0, 0.125, 0.25, 0.375` | `0.5, 0.75, 1` |

### ⛔ **E IL MIO PRIMO VERDETTO ERA UN FALSO-UNO MIO:** collassavo gli `eps` con un ### **OR**, e tutte e quattro le famiglie dicevano *«BUCO PRESENTE E STABILE»*. ### ⭐ **Ma il buco veniva TUTTO da `eps = 0`**, dove ### **non c'e' moneta di spin** e ### **il `43%` degli stati sta a `±1`**: un buco la' e' la ### **struttura a BANDE PIATTE di Grover**, non un gap in cui uno stato legato possa vivere. ### **Trovato leggendo i numeri, non rileggendo il codice.**

### **E il cubico lo mostra in tre righe** *(larghezze su `L = 5` e `L = 8`)*:

| `eps` | larghezza | in spaziature | rapporto `L=8 / L=5` | buco? |
|---|---|---|---|---|
| `0` | 1.385 → 0.8911 | 330.6 → 871.4 | **0.643** | ### ⭐ **si'** |
| `0.5` | 0.1139 → 0.03259 | 27.2 → 31.9 | **0.286** | ### ⛔ **no** |
| `1` | 0.02544 → 0.007925 | 6.1 → 7.7 | **0.311** | ### ⛔ **no** |

### ⛔ **A `eps = 0.5` e `eps = 1` la larghezza CALA del `71%` e del `69%` crescendo la taglia** — cioe' scala come ### **la spaziatura della griglia di momenti**, e ### **una spaziatura non e' un gap.** ### ✅ **E la soglia che l'ha preso era scritta PRIMA** *(`s2`: la larghezza non cala piu' del `50%`)*.

## ⭐ **`M1` — IL SEGNO: `(D)` DIRETTO LEGA IN `1D`, E IN `3D` L'EFFETTO CALA CON LA TAGLIA**

| la scena | famiglia | diametro | `t_oss` | **RESTA** | **DISPERDE** | non decidibili |
|---|---|---|---|---|---|---|
| `cubico L=5` | cubico (3D) | `6` | `19` | **5** | 23 | `0` |
| `cubico L=8` | cubico (3D) | `12` | `38` | **1** | 27 | `0` |
| `cubico L=12` | cubico (3D) | `>= 18` | `40` | **3** | 25 | `0` |
| `geometrico3d n=512` | geometrico3d (3D irregolare) | `10` | `32` | **6** | 22 | `0` |
| `geometrico3d n=1728` | geometrico3d (3D irregolare) | `>= 15` | `40` | **0** | 28 | `0` |
| `irregolare n=120` | irregolare (casuale) | `8` | `25` | **10** | 18 | `0` |
| `irregolare n=2000` | irregolare (casuale) | `>= 11` | `35` | **8** | 20 | `0` |
| `regolare n=120` | regolare (1D) | `30` | `40` | **2** | 26 | `0` |
| `regolare n=2000` | regolare (1D) | `>= 500` | `40` | **4** | 24 | `0` |

### ✅ **E <<NON DECIDIBILE>> E' SPARITO DEL TUTTO, perche' la regola era applicata allo stato sbagliato:** prima dava `0` casi decidibili su ### **otto scene su nove.** ### **Adesso la taglia si giudica sul grumo INIZIALE e il raggio finale e' una MISURA** — e *«si disperde»* e' ### **un risultato, non un'assenza di risultato.**

### ⛔ **E I CASI SI ORDINANO PER *EFFETTO*, NON PER `sigma` — e il motivo e' un falso-uno che i numeri mi hanno messo davanti**

### **Dei `39` casi <<RESTA CONCENTRATO>>, `4` hanno un effetto SOTTO l'`1%`** — e il peggiore e' ### **`+0.699%` a `7.76 sigma`** *(`geometrico3d n=512`, `+D`, `x0 = 0.125`)*: il rapporto e' **11.406** contro **11.327** del lineare, cioe' ### **uguale a tre decimali.** ### ⭐ **E' SIGNIFICATIVITA' SENZA EFFETTO**, il rovescio esatto dell'errore che avevo fatto in `G2(b)` del `v4` — e la soglia `3 sigma`, scritta prima, ### **non basta da sola: serve anche l'ampiezza dell'effetto.**

| **effetto** | `sigma` | la scena | famiglia | var | `x0` | raggio finale / diametro |
|---|---|---|---|---|---|---|
| **+24.61%** | `9.11` | `regolare n=2000` | regolare | **`+D`** | `1` | 26 / 500 |
| **+24.08%** | `4.16` | `cubico L=8` | cubico | **`+D`** | `2` | 9 / 12 |
| **+23.74%** | `4.42` | `irregolare n=120` | irregolare | **`+N`** | `8` | 4 / 8 |
| **+23.03%** | `8.03` | `irregolare n=2000` | irregolare | **`+N`** | `4` | 7 / 11 |
| **+22.51%** | `6.46` | `regolare n=2000` | regolare | **`+D`** | `0.5` | 26 / 500 |
| **+22.36%** | `4.82` | `geometrico3d n=512` | geometrico3d | **`+N`** | `8` | 7 / 10 |
| **+19.84%** | `4.25` | `irregolare n=120` | irregolare | **`+D`** | `4` | 4 / 8 |
| **+18.51%** | `3.03` | `irregolare n=120` | irregolare | **`-D`** | `2` | 4 / 8 |
| **+18.44%** | `3.28` | `regolare n=120` | regolare | **`+D`** | `1` | 26 / 30 ### ⛔ **il fronte ha RIEMPITO il grafo** |
| **+17.74%** | `6.08` | `irregolare n=120` | irregolare | **`-D`** | `4` | 4 / 8 |
| **+16.89%** | `6.02` | `irregolare n=120` | irregolare | **`-D`** | `8` | 4 / 8 |
| **+16.40%** | `4.46` | `cubico L=12` | cubico | **`-D`** | `2` | 11 / 18 |
| **+15.03%** | `18.75` | `irregolare n=2000` | irregolare | **`+D`** | `0.5` | 7 / 11 |
| **+12.67%** | `4.72` | `irregolare n=2000` | irregolare | **`+D`** | `1` | 7 / 11 |

### ⭐ **E LA PROVA CHE DECIDE E' LA TAGLIA, perche' il mandato lo chiede: <<solido solo se regge su almeno DUE taglie>>**

| famiglia | il caso | taglia piccola | taglia grande | che cosa fa |
|---|---|---|---|---|
| **regolare (1D)** | `+D` a `x0 = 1` | **+18.44%** | **+24.61%** | ### ⭐ **CRESCE** |
| **cubico (3D)** | `+D` a `x0 = 2` | **+24.08%** | **+8.55%** | ### ⛔ **CALA** |
| **geometrico3d (3D irregolare)** | `+D` a `x0 = 1` | **+11.86%** | ### **NIENTE** | ### ⛔ **SPARISCE** |
| **irregolare (casuale)** | `+N` a `x0 = 2` | **+8.94%** | **+12.44%** | ### ⭐ **CRESCE** |

### ⭐ **QUINDI: in `1D` l'effetto CRESCE con la taglia** *(`+18.4%` a `n=120`, `+24.6%` a `n=2000`)*, e in ### **`3D` CALA o SPARISCE** — sul cubico da `+24.1%` a `L=8` a `+8.6%` a `L=12`, e sul geometrico ### **da `+11.9%` a `n=512` a NIENTE a `n=1728`** *(`0` casi concentrati su `28`)*.

### ⚠ **E UNA COSA CHE NON LASCIO AMBIGUA: anche il CASUALE cresce** *(`+8.9%` → `+12.4%`)*. ### **Le due famiglie che CRESCONO sono `1D` e l'ESPANSORE; le due che CALANO sono le `3D`.** ### ⛔ **Ma sull'espansore il misurando stesso e' sospetto**, e lo dichiaro: il *«fondo uniforme»* su un grafo dove il volume cresce ### **esponenzialmente** con la distanza e' ### **minuscolo**, quindi il rapporto *«frazione entro un arco / fondo»* puo' crescere ### **per la geometria del denominatore**, non perche' il grumo stia insieme. ### **Non concludo <<lega anche nell-espansore>>: dico che il misurando non lo distingue.**

### ⛔ **E IL GEOMETRICO `3D` HA UN BUCO NELLO SPETTRO *E NON LEGA*:** un buco e' ### **necessario ma non sufficiente**, ed e' il risultato piu' informativo di tutto il mandato.

## ⚠ **I LIMITI, dichiarati**

| | il limite |
|---|---|
| `1` | ### **`M2` NON E' GIRATA su queste famiglie**: gli stati stazionari autoconsistenti restano da misurare, e la sonda sul `n=120` irregolare dice che il selettore prescritto dal mandato *(«il piu' localizzato»)* ### **oscilla a `O(1)`**, mentre quello a ### **massima sovrapposizione** converge a `1.9e-13` |
| `2` | ### **DUE taglie non sono uno scaling** *(`TAGLIA-FINITA`)*: la soglia `s2` confronta la piu' piccola con la piu' grande, e con due punti e' ### **una retta per due punti.** `M0` ha due taglie per famiglia |
| `3` | ### **Sulle scene `3D` piccole il fronte RIEMPIE il grafo**: il raggio finale arriva a `5/6` sul cubico `L=5` e a `11/18` su `L=12`. ### **La regola sul raggio INIZIALE passa, ma il confronto <<frazione entro un arco contro fondo uniforme>> e' allora dominato dalla taglia finita** — e questo ### **non e' nella regola del mandato** |
| `4` | ### **La soglia `3 sigma` non basta da sola**: `4` casi su `39` hanno un effetto sotto l'`1%`, e uno e' `+0.016%` a `3.55 sigma`. ### **L'effetto si riporta accanto al `sigma`**, sempre |
| `5` | ### **L'anisotropia delle scene `3D` non e' risolta**: nessuna delle due provate e' isotropa sul misurando di grafo, e il mandato `[[ISOTROPIA-LOCALE]]` e' in coda proprio per questo |
| `6` | ### **La grandezza conservata di `-N` e' `-N`**, e ### **NON la chiamo energia** *(`[[PROMOZIONE-CONSERVAZIONE-MODIFICATA]]` e' una decisione di Luca aperta)* |

## ⛔ **IL MANDATO SI CHIUDE PARZIALE** *(decisione di Luca, `2026-10-12`: `[[BASTA-PROTOTIPI]]`)*

> ### ⭐ **CIO' CHE E' MISURATO E SALVATO RESTA, con la sua provenienza; cio' che manca diventa LE PRIME MISURE DEL SIMULATORE** dopo il criterio di passaggio *(`[[BANCO-CONGELATO]]`)*. ### ⛔ **E il banco non gira piu': nessuna corsa, ne' leggera' ne' pesante.**

### ✅ **`1` CIO' CHE E' SALVATO SU DISCO, e da dove viene**

*(`proto_camminata/uscite/letture_legame_grandi.json`, prodotto da `python proto_camminata/_letture_legame_grandi.py` al blob `70720dfc`, scritto alle `23:57:01` del `2026-10-11` e **committato con questa sezione**.)*

| la scena | `n` | `m` | diametro | `t` usati | griglia `x0` | costo/tick |
|---|---|---|---|---|---|---|
| regolare n=2000 (limite noto 1D) | `2000` | `4000` | `>=500` | `4, 11, 18, 26, 33, 40` | `0.125, 0.25, 0.5, 1, 2, 4, 8` | `0.0019` s |
| geometrico3d n=4000 respinti (PRINCIPALE) | `4000` | `9307` | `>=20` | `4, 6, 9, 11, 14, 16` | `0.125, 0.25, 0.5, 1, 2, 4, 8` | `0.0045` s |
| geometrico3d n=26000 respinti (PRINCIPALE) | `26000` | `69700` | `>=33` | `4, 8, 13, 17, 22, 26` | `1, 4, 8` | `0.0576` s |

### ⭐ **`geometrico3d n=26000 respinti (PRINCIPALE)`** — ### **SI DISPERDE: **12****

| variante | `x0` | verdetto | effetto rel. | differenza | `sigma` | rapp. pendenze | `sigma` da `1` | raggio fermo? |
|---|---|---|---|---|---|---|---|---|
| `+N` | `8` | SI DISPERDE | `+0.2780` | `+0.0173` | `6.5` | `0.918` | `0.7` | no |
| `-N` | `8` | SI DISPERDE | `-0.2406` | `-0.0149` | `8.3` | `1.129` | `0.8` | no |
| `+D` | `8` | SI DISPERDE | `-0.2156` | `-0.0134` | `6.5` | `0.918` | `0.7` | no |
| `+N` | `4` | SI DISPERDE | `+0.1270` | `+0.0079` | `1.9` | `0.906` | `0.8` | no |
| `-D` | `4` | SI DISPERDE | `-0.0987` | `-0.0061` | `1.2` | `0.932` | `0.6` | no |
| `-N` | `4` | SI DISPERDE | `-0.0646` | `-0.0040` | `1.8` | `1.097` | `0.6` | no |
| `-D` | `1` | SI DISPERDE | `-0.0525` | `-0.0033` | `2.5` | `1.129` | `0.8` | no |
| `+D` | `4` | SI DISPERDE | `-0.0314` | `-0.0020` | `1.5` | `0.918` | `0.7` | no |
| `-D` | `8` | SI DISPERDE | `+0.0256` | `+0.0016` | `0.2` | `0.918` | `0.7` | no |
| `+N` | `1` | SI DISPERDE | `-0.0256` | `-0.0016` | `2.5` | `1.000` | `0.0` | no |
| `-N` | `1` | SI DISPERDE | `+0.0145` | `+0.0009` | `3.9` | `1.000` | `0.0` | no |
| `+D` | `1` | SI DISPERDE | `+0.0107` | `+0.0007` | `0.4` | `0.953` | `0.3` | no |

### ⭐ **`geometrico3d n=4000 respinti (PRINCIPALE)`** — ### **SI DISPERDE: **28****

| variante | `x0` | verdetto | effetto rel. | differenza | `sigma` | rapp. pendenze | `sigma` da `1` | raggio fermo? |
|---|---|---|---|---|---|---|---|---|
| `+D` | `4` | SI DISPERDE | `-0.2402` | `-0.0206` | `3.4` | `0.959` | `0.3` | no |
| `+D` | `8` | SI DISPERDE | `-0.1370` | `-0.0118` | `2.1` | `0.946` | `0.5` | no |
| `+D` | `1` | SI DISPERDE | `+0.1151` | `+0.0099` | `1.5` | `1.000` | `0.0` | no |
| `+N` | `8` | SI DISPERDE | `-0.1084` | `-0.0093` | `2.8` | `0.946` | `0.5` | no |
| `+D` | `0.5` | SI DISPERDE | `+0.0876` | `+0.0075` | `1.9` | `1.000` | `0.0` | no |
| `-N` | `4` | SI DISPERDE | `+0.0872` | `+0.0075` | `2.4` | `1.000` | `0.0` | no |
| `-D` | `2` | SI DISPERDE | `-0.0826` | `-0.0071` | `3.4` | `1.000` | `0.0` | no |
| `-D` | `1` | SI DISPERDE | `-0.0784` | `-0.0067` | `15.8` | `1.000` | `0.0` | no |
| `-D` | `8` | SI DISPERDE | `-0.0705` | `-0.0061` | `2.1` | `0.919` | `0.7` | no |
| `-D` | `0.5` | SI DISPERDE | `-0.0568` | `-0.0049` | `7.0` | `1.000` | `0.0` | no |
| `-N` | `2` | SI DISPERDE | `+0.0493` | `+0.0042` | `6.1` | `1.000` | `0.0` | no |
| `+N` | `4` | SI DISPERDE | `-0.0437` | `-0.0038` | `0.9` | `0.973` | `0.2` | no |
| `-N` | `8` | SI DISPERDE | `-0.0371` | `-0.0032` | `1.1` | `1.000` | `0.0` | no |
| `+D` | `0.25` | SI DISPERDE | `+0.0346` | `+0.0030` | `2.2` | `1.000` | `0.0` | no |
| `-D` | `4` | SI DISPERDE | `+0.0288` | `+0.0025` | `0.6` | `0.973` | `0.2` | no |
| `+D` | `2` | SI DISPERDE | `-0.0265` | `-0.0023` | `0.7` | `1.000` | `0.0` | no |
| `-D` | `0.25` | SI DISPERDE | `-0.0261` | `-0.0022` | `3.9` | `1.000` | `0.0` | no |
| `+N` | `2` | SI DISPERDE | `-0.0163` | `-0.0014` | `0.4` | `1.000` | `0.0` | no |
| `-N` | `1` | SI DISPERDE | `+0.0128` | `+0.0011` | `1.6` | `1.000` | `0.0` | no |
| `+D` | `0.125` | SI DISPERDE | `+0.0098` | `+0.0008` | `2.7` | `1.000` | `0.0` | no |
| `-D` | `0.125` | SI DISPERDE | `-0.0088` | `-0.0008` | `3.2` | `1.000` | `0.0` | no |
| `+N` | `0.5` | SI DISPERDE | `+0.0061` | `+0.0005` | `0.5` | `1.000` | `0.0` | no |
| `+N` | `1` | SI DISPERDE | `+0.0059` | `+0.0005` | `0.2` | `1.000` | `0.0` | no |
| `+N` | `0.25` | SI DISPERDE | `+0.0020` | `+0.0002` | `0.5` | `1.000` | `0.0` | no |
| `-N` | `0.5` | SI DISPERDE | `-0.0015` | `-0.0001` | `0.2` | `1.000` | `0.0` | no |
| `-N` | `0.25` | SI DISPERDE | `-0.0015` | `-0.0001` | `0.5` | `1.000` | `0.0` | no |
| `+N` | `0.125` | SI DISPERDE | `+0.0005` | `+0.0000` | `0.6` | `1.000` | `0.0` | no |
| `-N` | `0.125` | SI DISPERDE | `-0.0005` | `-0.0000` | `0.5` | `1.000` | `0.0` | no |

### ⭐ **`regolare n=2000 (limite noto 1D)`** — ### **RESTA CONCENTRATO: **1**  SI DISPERDE: **27****

| variante | `x0` | verdetto | effetto rel. | differenza | `sigma` | rapp. pendenze | `sigma` da `1` | raggio fermo? |
|---|---|---|---|---|---|---|---|---|
| `-D` | `4` | SI DISPERDE | `-0.2988` | `-0.0462` | `8.4` | `0.938` | `2.9` | no |
| `-N` | `8` | SI DISPERDE | `-0.2667` | `-0.0413` | `4.8` | `0.973` | `0.9` | no |
| `-D` | `8` | SI DISPERDE | `-0.2510` | `-0.0388` | `2.5` | `0.853` | `6.5` | no |
| `+D` | `1` | SI DISPERDE | `+0.2461` | `+0.0381` | `9.1` | `1.012` | `0.4` | no |
| `+N` | `8` | SI DISPERDE | `-0.2315` | `-0.0358` | `10.5` | `0.872` | `3.1` | no |
| `+D` | `0.5` | SI DISPERDE | `+0.2251` | `+0.0348` | `6.5` | `1.012` | `0.4` | no |
| `+D` | `4` | SI DISPERDE | `-0.2185` | `-0.0338` | `3.7` | `0.939` | `2.3` | no |
| `-N` | `4` | SI DISPERDE | `-0.2088` | `-0.0323` | `2.9` | `1.007` | `0.3` | no |
| `-D` | `2` | SI DISPERDE | `-0.1831` | `-0.0283` | `2.3` | `0.994` | `0.2` | no |
| `-N` | `2` | SI DISPERDE | `-0.1830` | `-0.0283` | `7.5` | `1.016` | `0.5` | no |
| `-D` | `1` | SI DISPERDE | `-0.1545` | `-0.0239` | `1.6` | `1.008` | `0.3` | no |
| `+N` | `4` | SI DISPERDE | `-0.1007` | `-0.0156` | `1.2` | `0.956` | `1.2` | no |
| `-N` | `1` | SI DISPERDE | `-0.0726` | `-0.0112` | `7.5` | `1.032` | `1.0` | no |
| `+N` | `1` | SI DISPERDE | `+0.0702` | `+0.0109` | `2.2` | `1.005` | `0.2` | no |
| `+D` | `0.25` | SI DISPERDE | `+0.0620` | `+0.0096` | `8.0` | `1.000` | `0.0` | no |
| `+D` | `8` | ### ⭐ **RESTA CONCENTRATO** | `+0.0542` | `+0.0084` | `0.5` | `0.772` | `5.9` | no |
| `-D` | `0.5` | SI DISPERDE | `-0.0470` | `-0.0073` | `1.2` | `1.034` | `1.1` | no |
| `+N` | `0.5` | SI DISPERDE | `+0.0215` | `+0.0033` | `2.1` | `1.000` | `0.0` | no |
| `-N` | `0.5` | SI DISPERDE | `-0.0194` | `-0.0030` | `2.8` | `1.032` | `1.0` | no |
| `+N` | `2` | SI DISPERDE | `+0.0178` | `+0.0028` | `0.4` | `1.007` | `0.2` | no |
| `-D` | `0.25` | SI DISPERDE | `-0.0134` | `-0.0021` | `1.2` | `1.032` | `1.0` | no |
| `+D` | `0.125` | SI DISPERDE | `+0.0113` | `+0.0018` | `6.5` | `1.000` | `0.0` | no |
| `-D` | `0.125` | SI DISPERDE | `-0.0062` | `-0.0010` | `2.3` | `1.032` | `1.0` | no |
| `+N` | `0.25` | SI DISPERDE | `+0.0049` | `+0.0008` | `1.8` | `1.000` | `0.0` | no |
| `-N` | `0.25` | SI DISPERDE | `-0.0046` | `-0.0007` | `1.9` | `1.032` | `1.0` | no |
| `+D` | `2` | SI DISPERDE | `+0.0029` | `+0.0004` | `0.0` | `0.972` | `0.7` | no |
| `+N` | `0.125` | SI DISPERDE | `+0.0011` | `+0.0002` | `1.6` | `1.000` | `0.0` | no |
| `-N` | `0.125` | SI DISPERDE | `-0.0011` | `-0.0002` | `1.6` | `1.008` | `0.3` | no |

### ⛔ **`2` IL FATTO CHE DECIDE, sulla scena PRINCIPALE a `n = 26000`: `12` CASI SU `12` SI DISPERDONO.** E dentro quel `12 su 12` ci sono due cose che il verdetto da solo non dice.

| | il fatto | il numero |
|---|---|---|
| `1` | ### **`+N` CONCENTRA IL NUCLEO**, e la gamba della frazione PASSA | `+27.8%` della frazione entro un arco, a `6.5 sigma` |
| `2` | ### **ma il FRONTE si allarga come nel lineare**, e la gamba del raggio FALLISCE | rapporto fra le pendenze `0.918`, a `0.7 sigma` da `1` |
| `3` | ### ⛔ **e `+D`, il segno che LEGA in `1D`, in `3D` e' PEGGIO del lineare** | `-21.6%` a `6.5 sigma` — ### **non e' neutro: e' sfavorevole** |

### ⭐ **E IL MISURANDO IN ARCHI HA FATTO ESATTAMENTE CIO' PER CUI E' STATO SCRITTO:** il misurando vecchio *(frazione entro un arco contro fondo uniforme)* avrebbe visto ### **solo la prima riga** e avrebbe detto *«`+N` lega»*. ### ⛔ **Il misurando nuovo vede che il NUCLEO si concentra mentre l'ESTENSIONE no** — cioe' ### **un picco che sopravvive sopra un fronte che si allarga alla velocita' della luce del grafo**, non uno stato legato.

### ⚠ **`3` CIO' CHE MANCA, e diventa le PRIME MISURE DEL SIMULATORE**

| | che cosa | perche' manca |
|---|---|---|
| `1` | il ### **geometrico uniformi** a `n = 4000` e `26000` *(la colonna di confronto col referto vecchio)* | era la scena ### **in corso** quando il run e' stato fermato |
| `2` | il ### **cubico di controllo** `L = 20` e `L = 30` | ### **vengono DOPO** nell'ordine delle scene, e il run non ci e' arrivato |
| `3` | ### **`M2`**, gli stati autoconsistenti col selettore a massima sovrapposizione | ### **non e' mai girata**, ed era il terzo limite che avevo dichiarato io |
| `4` | il ### **cubico `L = 40`** | ### **dichiarato NON PAGABILE**: `MemoryError` a `n = 64000`, e ### **~`11` ore** estrapolando il salto `L = 20` → `L = 30` *(`4.98` volte)* |
| `5` | l'### **aggregazione PER FAMIGLIA** *(la regola delle due taglie)* | si calcola ### **alla fine** della misura, e il processo e' stato fermato prima: ### **il `json` ha il dato per scena, non quello per famiglia** |

### ⛔ **E LE DUE DOMANDE RESTANO APERTE, con i numeri che ci sono:** `[[DOMANDA-QUALE-SEGNO]]` *(quale segno, se quello che lega in `1D` in `3D` peggiora)* e `[[DOMANDA-VIA-DEL-CAMPO]]`. ### ⭐ **E la seconda e' quella che questi numeri spingono:** se ### **nessun termine LOCALE lega in `3D`**, la via che resta e' ### **il CAMPO.**

