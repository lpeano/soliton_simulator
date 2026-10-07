# `A-S1` — **IL TEST `H1`: LE MASSE SOPRAVVIVONO SE LE VELOCITÀ DI FASE PARTONO COERENTI?**

*Referto generato da `csv/_test_fork/_referto_massa_h1.py`. Dati: `csv/_test_fork/_massa_h1/h1.json`. Criteri e previsioni: `doc/TASK_HISTORY/2026-10-07_as1-test-h1-scioglimento.md`, committato ### **PRIMA** della corsa.*

| | |
|---|---|
| simulatore | `b8c21049` *(atteso `b8c21049`)* |
| strumento | `ccbe5ed8` |
| `_misura_verso` *(da cui si CHIAMA `m2`)* | `fcf75043` |
| passi | ### **500** |
| secondi | 2254.7 |
| in configurazione del driver | ### ✔ **sì** |
| avvisi | ### **0** |

## ⛔ **TRE COSE DA SAPERE PRIMA DEI NUMERI**

> ### ⭐ **`0` — IL BRACCIO DI CONTROLLO È STATO RIGIRATO, E LO DICO.** Il mandato lo prevede *(«se ti serve una grandezza che `A1` non ha registrato, rigira il controllo e dillo»)*, e ### **serviva: `A1` non ha la coerenza per massa, né la dispersione di `phivel`, né `tau_tw`.** Senza il controllo ### **l'esplosione della `phivel_std` del VUOTO non si potrebbe attribuire** — è un effetto dell'intervento, o succede comunque? ### ✔ **Stesso blob dello strumento** *(`ccbe5ed8`)*, stessa scena, stesso seme: i due bracci si distinguono ### **solo per `braccio_h1`**, e il generatore ### **si ferma** se i blob differiscono. ### ✔ **E dove `A1` ha l'`AUC`, il confronto con il braccio rigirato è una PROVA IN PIÙ, non una ripetizione.**

> ### ⛔ **`1` — `U1` È APERTA** *(da-decidere, blocca `SI`)*. Questa corsa ### **non dà valori assoluti:** confronta ### **DUE BRACCI DELLO STESSO SIMULATORE**, e la legge difettosa è ### **la stessa in entrambi**. ### **Quello che si legge è la DIFFERENZA, non il livello.**

> ### ⚠ **`2` — `P3` NON È SODDISFATTA: UN SEME SOLO** *(il `11`)*, perché il braccio di controllo è la corsa `A1` e il mandato dice di ### **non rigirarla**. *(`S1b`, nel task history del 2026-09-27, chiedeva ### **`4` semi**.)* Il confronto è ### **APPAIATO** — stessa scena, stesso seme, ### **UNA** condizione iniziale cambiata — che è la forma più forte di confronto appaiato, e ### **non dice NIENTE sulla variabilità fra semi.** ### **`A-S1` è una DIAGNOSI, non un sigillo: nessuna cura può appoggiarsi a questo numero.**

> ### ⚠ **`3` — TRE CONFONDENTI, dichiarati PRIMA della corsa** *(task history, aggiunta datata)*. ### **Uno di essi è MISURATO in questo referto**, e ### **il numero lo ridimensiona.** La tavola è sotto.

---

# `(0)` **L'INTERVENTO, E IL CONTROLLO CHE LO DELIMITA**

L'intervento: ### **`net.phivel[idx] = media(net.phivel[idx])` per ogni massa**, ### **dopo la costruzione e PRIMA del passo `1`**, ### **nello strumento.** ### ✔ **Toglie SOLO la dispersione, non cambia la velocità media, e non introduce nessun numero nuovo** *(`A1`)*.

| massa | nodi | media imposta | `std` PRIMA | intervallo PRIMA |
|---|--:|--:|--:|---|
| `massa_0` | 411 | ### **-0.016561** | 0.418805 | `[-1.2552, 1.1759]` |
| `massa_1` | 413 | ### **-0.014593** | 0.413630 | `[-1.3727, 1.3646]` |
| `massa_2` | 413 | ### **0.027931** | 0.405236 | `[-1.3068, 1.3936]` |

> ### ⭐ **E LE MEDIE SONO QUASI ZERO MENTRE LE `std` SONO `~0.41`:** ### **equalizzare alla media non «allinea» le velocità, le AZZERA.** ### **È il terzo confondente**, e il task history lo registra col conto dell'energia cinetica.

### ✔ **IL CONTROLLO DEL PASSO `0`** *(`python csv/_test_fork/_massa_h1.py --passo0`)*

| | |
|---|--:|
| attributi firmati | 63 |
| attributi ### **DIVERSI** | ### **1** — `phivel` |
| nodi delle masse | 1237 |
| nodi FUORI con `phivel` ### **identica AL BIT** | ### **11565** |
| esito | ### ✔ **PASSA** |

> ### ⛔ **E LA VERIFICA NON È «`phivel` DIFFERISCE»:** un nodo la cui `phivel` era ### **già** la media ### **non differisce**, e pretenderlo darebbe un falso allarme. ### **Le due affermazioni VERE sono «fuori dalle masse identica al bit» e «dentro vale ESATTAMENTE la media dichiarata».**

## ⭐ **LE DUE VALIDAZIONI, e si chiudono a vicenda**

| | che cosa pretende | il numero | esito |
|---|---|--:|---|
| `(a)` ### **il controllo RIGIRATO è il controllo** | `n` identica a quella di ### **`A1`** su tutti i passi in comune *(stesso seme, stessa scena, nessun intervento)* | ### **0** differenze su 501 passi | ### ✔ **SÌ** |
| `(b)` ### **l'intervento NON è inerte** | `n` del braccio `H1` ### **DIVERSA** da quella del controllo, almeno a un passo | ### **277** differenze su 501 passi | ### ✔ **SÌ**, e la prima è al passo `221` *(controllo 12811, `H1` 12809)* |

> ### ⭐ **ENTRAMBE PASSANO, e insieme dicono una cosa che nessuna delle due dice da sola:** il controllo è ### **esattamente** la corsa `A1` *(quindi i numeri del 2026-10-07 valgono come riferimento)*, e l'intervento ### **ha spostato la dinamica** a partire dal passo `221` *(il `216` è la prima nascita: la prima differenza arriva subito dopo)*. ### **Quindi la differenza che si legge sotto è REALE, e il riferimento è SOLIDO.**

---

# `(1)` ⭐ **L'AUC DI `c_k` MATERIA/VUOTO — IL NUMERO CHE DECIDE**

> ### ⛔ **I CRITERI, FISSATI PRIMA** *(mandato di Luca)*: ### **`H1 BASTA`** se AUC al `400` ### **`>= 0.90`** ### **E** al `500` ### **`>= 0.85`**; ### **`H1 NON BASTA`** se AUC al `400` ### **`< 0.60`**; fra i due ### **`H1 AIUTA MA NON BASTA`**, e si riporta la curva e il passo in cui l'AUC scende sotto ### **`0.60`** nei due bracci.

| passo | ### **AUC `H1`** | AUC controllo | differenza | `c_k` MAT `H1` | MAT contr. | `c_k` VUO `H1` | VUO contr. |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **0.9992** | 0.9992 | ### **-0.0000** | 0.7903 | 0.7904 | 0.1627 | 0.1627 |
| `50` | ### **0.9968** | 0.9966 | ### **+0.0002** | 0.8326 | 0.8293 | 0.2795 | 0.2795 |
| `150` | ### **0.9906** | 0.9861 | ### **+0.0045** | 0.6897 | 0.6483 | 0.2416 | 0.2430 |
| `230` | ### **0.9351** | 0.9023 | ### **+0.0329** | 0.5319 | 0.4847 | 0.2632 | 0.2665 |
| `300` | ### **0.7535** | 0.7371 | ### **+0.0163** | 0.3971 | 0.3870 | 0.2707 | 0.2744 |
| `400` | ### **0.5536** | 0.4679 | ### **+0.0857** | 0.3128 | 0.2882 | 0.2857 | 0.2972 |
| `500` | ### **0.4627** | 0.4497 | ### **+0.0130** | 0.2923 | 0.2761 | 0.3074 | 0.3019 |

| | primo passo MISURATO con AUC `< 0.60` |
|---|---|
| ### **braccio `H1`** | ### **`400`** |
| controllo *(`A1`)* | ### **`400`** |

> ### ⛔ **L'ESITO DEL CRITERIO: `H1 NON BASTA`.** AUC `0.5536` al `400`, sotto la soglia `0.60`: ### **le masse si sciolgono anche con le velocità coerenti**.

> ### ⭐ **E QUESTO È IL RAMO CHE I CONFONDENTI NON TOCCANO**, ed era scritto ### **prima** della corsa: un intervento che ha dato alle masse ### **le velocità coerenti** *(e, per gli effetti collaterali, anche una torsione che rilassa meno e un vuoto scaldato dal termostato)* ### **non le ha salvate comunque.** ### **La conclusione è SOLIDA.**

> ### ⛔ **E NON SI PASSA AD `A-S2`: LA DECISIONE È DI LUCA.**

---

# `(2)` **LA COERENZA DI FASE DI OGNI MASSA, COL SUO NULLO**

> ### ⛔ **IL NULLO NON È ZERO: è il VUOTO.** Una coerenza che scende va letta contro ### **quella del vuoto**, non contro `0`.

> ### ⚠ **E SONO DUE LETTURE, non una.** `phi` vive su ### **`4π`**, quindi `e^{iφ}` identifica `φ` con `φ + 2π`. ### **Il campo del simulatore usa `exp(1j*φ)`** *(`:5195`)*, quindi `|<e^{iφ}>|` è ### **quella che il codice VEDE**; `|<e^{iφ/2}>|` è ### **quella fedele al dominio.** Si riportano entrambe.

| passo | ### **`massa_0`** | ### **`massa_1`** | ### **`massa_2`** | ### **VUOTO** | ### **controllo** *(media)* |
|--:|--:|--:|--:|--:|--:|
| `1` | 0.9986 | 0.9988 | 0.9988 | 0.0051 | 0.9988 |
| `50` | 0.9895 | 0.9876 | 0.9886 | 0.0176 | 0.9798 |
| `150` | 0.7540 | 0.7226 | 0.7362 | 0.0257 | 0.6790 |
| `230` | 0.5480 | 0.4891 | 0.4861 | 0.0508 | 0.4565 |
| `300` | 0.3404 | 0.3268 | 0.3175 | 0.0453 | 0.3054 |
| `400` | 0.1834 | 0.1880 | 0.2392 | 0.0359 | 0.1585 |
| `500` | 0.1707 | 0.0490 | 0.1026 | 0.0069 | 0.0858 |

> ### ⭐ **L'ULTIMA COLONNA E' IL BRACCIO DI CONTROLLO RIGIRATO** *(la MEDIA sulle tre masse)*, e ### **senza di lei la colonna <<VUOTO>> non basterebbe:** dice se la coerenza che cade nel braccio `H1` cade ### **di meno** di quanto cadrebbe comunque.

*(la stessa, letta su `4π`)*

| passo | `massa_0` | `massa_1` | `massa_2` | ### **VUOTO** |
|--:|--:|--:|--:|--:|
| `1` | 0.9997 | 0.9997 | 0.9997 | 0.0091 |
| `50` | 0.9974 | 0.9969 | 0.9971 | 0.0084 |
| `150` | 0.9262 | 0.9222 | 0.9199 | 0.0102 |
| `230` | 0.8581 | 0.8429 | 0.8203 | 0.0013 |
| `300` | 0.7440 | 0.7448 | 0.6883 | 0.0070 |
| `400` | 0.4189 | 0.3985 | 0.4258 | 0.0082 |
| `500` | 0.1724 | 0.1448 | 0.1567 | 0.0047 |

---

# `(3)` ⭐ **LA DISPERSIONE DI `phivel`: QUANTO DURA L'INTERVENTO**

> ### ⭐ **QUESTA È LA MISURA CHE DICE SE L'INTERVENTO È SOPRAVVISSUTO.** `scuoti_vuoto` sta nella `PASSO_COMPOSIZIONE` a ### **ogni** passo e ### **scrive `phivel` e nient'altro**: l'equalizzazione è una ### **condizione iniziale**, non uno stato mantenuto.

| passo | `std massa_0` | `std massa_1` | `std massa_2` | ### **VUOTO** *(il NULLO)* | ### **massa_0 / VUOTO** | ### **massa_1 / VUOTO** | ### **massa_2 / VUOTO** | ### **`std` masse CONTROLLO** | ### **`std` VUOTO contr.** |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 0.20445 | 0.20509 | 0.20932 | 0.43391 | ### **0.4712** | ### **0.4727** | ### **0.4824** | 0.46412 | 0.43391 |
| `50` | 1.06832 | 1.08198 | 1.12856 | 3.51765 | ### **0.3037** | ### **0.3076** | ### **0.3208** | 1.25643 | 3.51571 |
| `150` | 1.69527 | 1.73174 | 1.79053 | 3.71977 | ### **0.4557** | ### **0.4656** | ### **0.4814** | 1.80821 | 3.66221 |
| `230` | 1.95979 | 1.94999 | 2.13793 | 3.82449 | ### **0.5124** | ### **0.5099** | ### **0.5590** | 2.13150 | 3.77187 |
| `300` | 2.79815 | 2.58330 | 2.75117 | 4.12619 | ### **0.6781** | ### **0.6261** | ### **0.6668** | 2.99213 | 4.09224 |
| `400` | 4.02014 | 4.01252 | 3.49195 | 4.43234 | ### **0.9070** | ### **0.9053** | ### **0.7878** | 4.22138 | 4.39037 |
| `500` | 4.83261 | 4.77658 | 4.44759 | 4.91821 | ### **0.9826** | ### **0.9712** | ### **0.9043** | 5.18325 | 4.81880 |

> ### ⛔ **AL PASSO `1` LA DISPERSIONE È GIÀ AL 47.54 % DEL VUOTO.** ### **L'intervento azzera la dispersione al passo `0`, e UN SOLO PASSO la riporta a circa metà.** ### ⭐ **Non è una previsione: è il numero**, e dice che ### **`scuoti_vuoto` cancella l'intervento quasi subito.**

---

# `(4)` ⛔ **IL CONFONDENTE `tau_tw`, MISURATO — e il numero lo RIDIMENSIONA**

Il task history dichiarava, ### **prima della corsa**, che azzerare la dispersione porterebbe `tau_tw` degli archi intra-massa a ### **`2π/1e-3 = 6283.2`**, cioè ### **~`2600 ×`** la mediana misurata. ### ✔ **Si misura, non si assume:**

| passo | `tau_tw` mediana ### **intra-massa** | su ### **TUTTI** gli archi | ### **rapporto** | ### **rapporto CONTROLLO** | archi intra-massa |
|--:|--:|--:|--:|--:|--:|
| `1` | 18.779 | 15.656 | ### **1.200** | 0.953 | 34120 |
| `50` | 7.068 | 2.234 | ### **3.164** | 2.614 | 34120 |
| `150` | 3.594 | 2.008 | ### **1.790** | 1.709 | 34120 |
| `230` | 3.243 | 1.920 | ### **1.690** | 1.585 | 34120 |
| `300` | 2.523 | 1.755 | ### **1.438** | 1.311 | 34120 |
| `400` | 1.810 | 1.587 | ### **1.141** | 1.022 | 34120 |
| `500` | 1.463 | 1.452 | ### **1.007** | 0.906 | 34117 |

> ### ⭐ **IL CONFONDENTE È PICCOLO, E IL MOTIVO È IL NUMERO DI PRIMA:** già al passo `1` il rapporto è ### **1.200**, non `~2600`, ### **perché la dispersione è tornata entro UN passo** e `dom` non sta più al pavimento. ### ✔ **L'avevo dichiarato come rischio e misurato come piccolo: è il modo in cui un confondente si tratta.**

---

# `(5)` **LE NASCITE E LA TORSIONE**

| passo | `n` `H1` | `n` controllo | nati `H1` | nati contr. | `\|tw\| > 2π` `H1` | contr. |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | 12802 | 12802 | ### **0** | 0 | 0.00 % | 0.00 % |
| `50` | 12802 | 12802 | ### **0** | 0 | 0.00 % | 0.00 % |
| `150` | 12802 | 12802 | ### **0** | 0 | 0.11 % | 0.11 % |
| `230` | 12816 | 12813 | ### **14** | 11 | 0.71 % | 0.72 % |
| `300` | 12841 | 12850 | ### **39** | 48 | 1.37 % | 1.39 % |
| `400` | 12899 | 12905 | ### **97** | 103 | 2.42 % | 2.59 % |
| `500` | 13006 | 13009 | ### **204** | 207 | 3.68 % | 3.77 % |

---

# ⭐ **LE MIE PREVISIONI, CONTRO I NUMERI**

> ### 📌 **Scritte nel task history `840a98d`, committato PRIMA dello strumento e PRIMA della corsa.**

| | la previsione | il numero | esito |
|---|---|---|---|
| `PH1-1` | ### ⚠ **`H1 AIUTA MA NON BASTA`**: AUC al `400` ### **sopra** quella del controllo ### **ma sotto `0.90`** | AUC `H1` 0.5536 contro controllo 0.4679 *(differenza +0.0857)*; e la soglia del criterio è ### **`0.60`** | ### ⚠ **MAL POSTA, e il difetto è MIO:** le due condizioni numeriche ### **REGGONO** *(l'AUC è sopra il controllo e sotto `0.90`)*, ### **ma l'intervallo che avevo dichiarato ATTRAVERSA la soglia `0.60`**, quindi ### **la previsione non poteva scegliere un verdetto.** Il numero è caduto nella parte che il criterio chiama ### **`H1 NON BASTA`**. ### ⛔ **Non la conto come confermata.** |
| `PH1-2` | la dispersione di `phivel` intra-massa ### **TORNA**: al passo `150` è già ### **più di METÀ** di quella del `vuoto` | al `150` la media sulle tre masse è ### **46.76 %** del vuoto; al passo `1` era già 47.54 %; e in ASSOLUTO la `std` intra-massa va da 0.2063 al passo `1` a ### **1.7392** al `150`, cioe' ### **8.43 volte** | ### ⛔ **SMENTITA SUL RAPPORTO** — ### ⚠ **ma il difetto è nel METRO che ho scelto io:** avevo normalizzato sul VUOTO, e ### **il vuoto si scalda**, quindi il rapporto scende anche se la dispersione delle masse ### **CRESCE**. ### **In assoluto la dispersione torna, e di molto.** |
| `PH1-3` | `tau_tw` intra-massa al passo `1` è ### **almeno `100 ×`** la mediana su tutti gli archi, e ### **CALA** | il rapporto MASSIMO sui passi misurati è ### **3.164**, non `>= 100` | ### ⛔ **SMENTITA** — ### ⭐ **e per la ragione giusta: la dispersione torna entro UN passo, quindi `dom` non sta al pavimento. Il confondente che avevo dichiarato È PICCOLO** |
| `PH1-4` | ### ⚠ **il passo `1` NON è un discriminante:** la coerenza per massa è ### **`>= 0.99`** | il minimo sulle tre masse al passo `1`: ### **0.9986**; e l'AUC al `1` è 0.9992 contro 0.9992 del controllo | ### ✔ **CONFERMATA** |
| `PH1-5` | le nascite a `500` passi stanno ### **entro il `±25 %`** di quelle del controllo | `H1` ### **204** contro controllo ### **207** *(scarto 1.45 %)* | ### ✔ **CONFERMATA** |

> ### **2 confermate, 2 SMENTITE, 1 ### **MAL POSTA**** su 5. ### ⚠ **E la MAL POSTA è un difetto di come ho SCRITTO la previsione, non del numero:** l'intervallo che avevo dichiarato ### **attraversava la soglia del criterio**, quindi qualunque numero dentro quell'intervallo avrebbe potuto dare DUE verdetti opposti. ### **Una previsione così non si può verificare, e contarla come confermata sarebbe stato comodo e falso.** ### **E la smentita che vale è `PH1-3`:** ### ⭐ **avevo dichiarato un confondente grande e l'ho misurato PICCOLO** — ### **dichiararlo prima è ciò che ha reso possibile ridimensionarlo dopo.**

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE**

| | |
|---|---|
| la variabilità fra semi | ### **UN seme solo** *(`P3` non soddisfatta)* |
| i valori ASSOLUTI | ### **`U1` è aperta:** si legge la ### **differenza**, non il livello |
| ### **perché** le masse si sciolgono | ### **`H2` non è stata misurata** *(`A-S2`)*: qui si misura ### **se `H1` basta**, non quale sia la causa |
| la causa di una eventuale RISALITA | ### **ambigua fra quattro cause**, e per questo il referto la dichiarerebbe `CONFONDUTA` |

> ### ⛔ **E LA DECISIONE SU `A-S2` È DI LUCA.** ### **Questo referto riporta i numeri e l'esito del criterio. Non prosegue.**

