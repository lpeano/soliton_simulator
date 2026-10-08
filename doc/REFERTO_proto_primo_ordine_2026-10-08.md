# IL PROTOTIPO AL PRIMO ORDINE — **il collaudo chiude, e il criterio del mare NON è decidibile come è scritto**

*Referto generato da `proto_primo_ordine/referto.py`. Dati: `proto_primo_ordine/uscite/`. Criteri, previsioni e DUE annotazioni scritte ### **prima** di girare: `doc/TASK_HISTORY/2026-10-08_proto-primo-ordine.md`.*

> ### ⛔ **IL SIMULATORE NON È TOCCATO** *(`b8c21049`)*, **e il prototipo NON lo importa** — e lo ### **asserisce** guardando `sys.modules`, non lo promette. L'assioma è `A16` *(`e17a334`)*, il piano `doc/RISCRITTURA_PRIMO_ORDINE.md`.

---

# ⛔ `①` **IL TETTO DEI `20` MINUTI È STATO SUPERATO, E LO DICO PRIMA DEI RISULTATI**

| | |
|---|--:|
| i secondi della corsa del mare | ### **1274.2** |
| in minuti | ### **21.24** |
| il tetto del mandato | `20` minuti |

> ### ⛔ **IL MANDATO DICE: «se una supera i `20` minuti FERMATI e scrivilo». La corsa li ha superati, quindi mi FERMO e lo scrivo** — e ### **NON lancio l'esperimento del pacchetto**, che era l'altro in programma.

> ### ⚠ **E IL MIO CONTROLLO DEL TETTO NON L'HA PRESO, per come l'avevo messo:** la verifica è ### **dentro** il ciclo dei `g` e dei semi, e il blocco `ε = 0` sta ### **dopo** quel ciclo. ### **Quindi gli ultimi `6` giri sono passati senza controllo.** I dati sono completi, ma il presidio era mal posto, ed è un difetto mio.

---

# ✔ `②` **IL COLLAUDO: `14` SU `14`, E `(b)` PROVA CIÒ CHE DICE**

| controllo | il numero | la soglia |
|---|--:|--:|
| ### **la NORMA si conserva** su `10⁴` passi | ### **`3.706e-13`** | `1e-8` |
| ### **l'ENERGIA si conserva** su `10⁴` passi | ### **`4.364e-13`** | `1e-8` |
| il solitone discreto è ### **STAZIONARIO**, verificato | ### **`9.714e-17`** | `1e-12` |
| ### **e si propaga INTATTO** dopo `10` tempi caratteristici | ### **`9.027e-11`** | `1e-3` |
| ⛔ il caso che ### **DEVE fallire**: a `g = 0` il profilo si disperde | ### **`5.558e-01`** | `> 1e-2` |
| la ### **doppia copertura**: `φ+4π` riporta `H` identica | ### **`0.000e+00`** | `0` |

## ⭐ **E L'ATTRIBUZIONE DEL RESIDUO È DIMOSTRATA, NON RACCONTATA**

Il `sech` è il solitone del limite ### **CONTINUO**; sul reticolo l'equazione stazionaria è `−(u_{k−1}+u_{k+1}−2u_k) + g|u|²u = μu`, e la sua soluzione è ### **un'altra**. Lo scarto fra le due sul profilo iniziale è ### **`3.239e-02`**.

| | |
|---|--:|
| col `sech` ### **continuo** | `1.903e-03` *(e ### **non calava** né con `dt` né con la larghezza)* |
| col solitone ### **dell'equazione che integro** | ### **`9.027e-11`** |

> ### ⛔ **TRE GIRI SBAGLIATI, MIEI, PRIMA DI ARRIVARE QUI** — e il terzo ha smontato la mia stessa spiegazione: `(1)` avevo ### **normalizzato** il `sech`, distruggendo la relazione ampiezza-larghezza che ### **fa** di quel profilo un solitone *(`3.373e-01`)*; `(2)` avevo chiamato il residuo «discretizzazione spaziale» con un test sulla ### **larghezza** che ### **non discriminava**, perché scalavo `dt ∝ LARG²` e l'errore temporale restava fisso ### **per costruzione**; `(3)` il test sul `dt` ha dato ### **lo stesso numero a quattro cifre** *(fattore `1.00`)*, e ### **una quantità che non si muove dimezzando il passo non è un errore di integrazione.**

> ### ⚠ **E PRIMA ANCORA, DUE DIFETTI CHE IL COLLAUDO HA PRESO:** l'### **encoding** di `stdout` *(la NONA volta in questo repo: `# -*- coding -*-` riguarda il SORGENTE, non lo STDOUT)*, e `energia` che calcolava `Σ|ψ_kc|⁴` ### **per componente** mentre `forza` usa la ### **norma spinoriale** del nodo — ### **due `H` diverse**, e la deriva dell'energia non si muoveva *(`2.408e-03` identico prima e dopo un'altra cura)* perché la causa era quella.

---

# ⭐ `③` **L'ESPERIMENTO DEL MARE** *(idea di Luca: i campi, per interferenza, generano le masse)*

| | |
|---|--:|
| nodi | ### **400** |
| `ρ_0` *(uguale su tutti i nodi)* | ### **1.0000** |
| `ε` *(il disturbo di fase, rad)* | ### **0.0100** |
| `dt` | ### **0.0020** |
| passi | ### **5000** |
| campione ogni | ### **50** |
| soglia del grumo *(× la media)* | ### **3.0000** |
| `g` | `0.0, -2.0, -5.0, -10.0, -20.0` |
| semi | `11, 12, 13` |

> ### ⚠ **`ρ_0 = 1` E NON la norma `1`, e il perché conta:** con norma totale `1` si avrebbe `ρ_0 = 0.0025`, quindi `g·ρ_0 = 0.05` a `g = −20` contro una scala di salto `~5`: ### **la non linearità sarebbe NEGLIGIBILE per costruzione**, e non succederebbe niente. ### **È un numero di banco, ed è dichiarato.**

## il braccio ### **`U-CASO`** — `U_ij` **casuale ma FISSA**

| `g` | seme | ### **grumi max** | vita max *(`t_c`)* | ### **`ρ_max/media`** | `PR` iniziale → finale | deriva norma | deriva `H` |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `0.0` | 11 | ### **11** | 11.00 | ### **6.04** | 400.00 → 272.59 | 8.5e-16 | 0.0e+00 |
| `0.0` | 12 | ### **9** | 13.50 | ### **6.22** | 400.00 → 257.17 | 1.3e-13 | 4.1e-13 |
| `0.0` | 13 | ### **8** | 15.00 | ### **6.57** | 400.00 → 276.52 | 4.4e-14 | 5.0e-13 |
| `-2.0` | 11 | ### **4** | 2.00 | ### **3.96** | 400.00 → 302.10 | 3.0e-14 | 1.6e-13 |
| `-2.0` | 12 | ### **2** | 1.60 | ### **3.41** | 400.00 → 312.55 | 2.4e-14 | 1.3e-13 |
| `-2.0` | 13 | ### **3** | 1.80 | ### **3.88** | 400.00 → 307.28 | 3.2e-14 | 1.8e-13 |
| `-5.0` | 11 | ### **0** | 0.00 | ### **2.79** | 400.00 → 339.25 | 1.3e-14 | 4.0e-14 |
| `-5.0` | 12 | ### **0** | 0.00 | ### **2.83** | 400.00 → 347.65 | 1.1e-14 | 3.7e-14 |
| `-5.0` | 13 | ### **0** | 0.00 | ### **2.80** | 400.00 → 340.09 | 1.1e-14 | 3.6e-14 |
| `-10.0` | 11 | ### **0** | 0.00 | ### **2.27** | 400.00 → 366.03 | 2.4e-13 | 7.9e-13 |
| `-10.0` | 12 | ### **0** | 0.00 | ### **2.28** | 400.00 → 367.26 | 1.8e-13 | 6.0e-13 |
| `-10.0` | 13 | ### **0** | 0.00 | ### **2.49** | 400.00 → 364.56 | 9.5e-14 | 3.1e-13 |
| `-20.0` | 11 | ### **0** | 0.00 | ### **2.21** | 400.00 → 380.72 | 1.9e-13 | 5.6e-13 |
| `-20.0` | 12 | ### **0** | 0.00 | ### **1.83** | 400.00 → 379.74 | 2.1e-13 | 5.9e-13 |
| `-20.0` | 13 | ### **0** | 0.00 | ### **2.00** | 400.00 → 382.01 | 2.4e-13 | 7.0e-13 |

## il braccio ### **`U-UNO`** — `U_ij` ### **= IDENTITÀ**

| `g` | seme | ### **grumi max** | vita max *(`t_c`)* | ### **`ρ_max/media`** | `PR` iniziale → finale | deriva norma | deriva `H` |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `0.0` | 11 | ### **6** | 43.00 | ### **12.68** | 400.00 → 176.02 | 3.8e-15 | 5.4e-15 |
| `0.0` | 12 | ### **7** | 45.50 | ### **7.74** | 400.00 → 172.78 | 2.1e-15 | 2.5e-15 |
| `0.0` | 13 | ### **5** | 47.50 | ### **11.51** | 400.00 → 142.89 | 2.3e-15 | 2.9e-15 |
| `-2.0` | 11 | ### **18** | 19.00 | ### **12.70** | 400.00 → 96.94 | 4.1e-15 | 4.6e-14 |
| `-2.0` | 12 | ### **21** | 19.00 | ### **11.62** | 400.00 → 99.43 | 2.2e-14 | 1.1e-13 |
| `-2.0` | 13 | ### **15** | 18.40 | ### **14.06** | 400.00 → 95.41 | 1.1e-14 | 8.3e-14 |
| `-5.0` | 11 | ### **22** | 44.00 | ### **7.64** | 400.00 → 169.42 | 1.0e-13 | 5.2e-13 |
| `-5.0` | 12 | ### **18** | 48.00 | ### **7.07** | 400.00 → 174.61 | 7.3e-14 | 3.9e-13 |
| `-5.0` | 13 | ### **17** | 39.00 | ### **6.82** | 400.00 → 169.16 | 3.1e-14 | 1.6e-13 |
| `-10.0` | 11 | ### **14** | 63.00 | ### **5.04** | 400.00 → 235.13 | 5.9e-14 | 3.0e-13 |
| `-10.0` | 12 | ### **11** | 97.00 | ### **4.71** | 400.00 → 242.43 | 7.6e-14 | 3.9e-13 |
| `-10.0` | 13 | ### **14** | 53.00 | ### **4.55** | 400.00 → 235.13 | 4.2e-14 | 2.1e-13 |
| `-20.0` | 11 | ### **3** | 18.00 | ### **3.61** | 400.00 → 295.43 | 1.5e-13 | 6.4e-13 |
| `-20.0` | 12 | ### **3** | 88.00 | ### **3.49** | 400.00 → 301.70 | 1.5e-13 | 6.5e-13 |
| `-20.0` | 13 | ### **3** | 14.00 | ### **3.49** | 400.00 → 295.16 | 1.3e-13 | 5.6e-13 |

# ⛔ `④` **IL CRITERIO NON È DECIDIBILE COME È SCRITTO, E IL PERCHÉ È MISURATO**

Il criterio di Luca ha ### **due clausole**: grumi che durano oltre `10 t_c` per almeno un `g`, ### **MENTRE** a `g = 0` il mare resta uniforme ### **entro un fattore `2`** della densità media. ### ➜ **La seconda clausola NON si verifica in NESSUNO dei due bracci:**

| braccio | `ρ_max/media` a `g = 0` *(i tre semi)* | la clausola chiede |
|---|--:|--:|
| `U-CASO` | ### **6.04, 6.22, 6.57** | `< 2` |
| `U-UNO` | ### **12.68, 7.74, 11.51** | `< 2` |

> ### ⛔ **QUINDI IL CONTROLLO A `g = 0` NON È UN CONTROLLO: il mare NON resta uniforme nemmeno senza non linearità**, e il criterio ### **non si può soddisfare come è scritto** — in nessuno dei due bracci. ### **Lo dico invece di scegliere la lettura che darebbe un verdetto.**

## ⭐ **E LA CAUSA È MISURATA, non ipotizzata: IL GRAFO È GIÀ UN CAMPO DISORDINATO**

Con `ψ` uniforme la forza è `F_k = −(Σ_j w_kj)·ψ + g·ρ·ψ`. ### **Se `Σ_j w_kj` varia da nodo a nodo, `F` NON è proporzionale a `ψ`**, e lo stato uniforme ### **non è stazionario.** Misurato sui tre grafi:

| seme | `Σ_j w_kj` media | min | max | ### **deviazione relativa** | ### **max/min** |
|--:|--:|--:|--:|--:|--:|
| 11 | 3.4841 | 0.4705 | 7.8404 | ### **0.3856** | ### **16.66** |
| 12 | 3.2113 | 0.4361 | 6.9591 | ### **0.3732** | ### **15.96** |
| 13 | 3.4752 | 0.1742 | 6.9379 | ### **0.3846** | ### **39.83** |

> ### ➜ **UN RAPPORTO `max/min` DI `16` E UNA DEVIAZIONE DEL `38 %` SONO UN CAMPO DISORDINATO FORTE.** ### **Il «mare uniforme» lo è solo in modulo: in energia di sito non lo è per niente**, e la localizzazione che si vede a `g = 0` è ### **localizzazione di Anderson del GRAFO** — esattamente il falso positivo che il task history dichiarava, ### **ma di una sorgente che NON avevo nominato.**

# ⛔ `⑤` **IL CASO CHE DEVE FALLIRE È SMENTITO IN UN BRACCIO, E LA PREMESSA ERA FALSA**

| braccio | seme | grumi max con ### **`ε = 0`** | `ρ_max/media` |
|---|--:|--:|--:|
| `U-CASO` | 11 | ### **0** | ### **2.2679** |
| `U-CASO` | 12 | ### **0** | ### **2.1852** |
| `U-CASO` | 13 | ### **0** | ### **2.4789** |
| `U-UNO` | 11 | ### **12** | ### **5.2801** |
| `U-UNO` | 12 | ### **14** | ### **4.5493** |
| `U-UNO` | 13 | ### **12** | ### **4.6375** |

> ### ⛔ **CON `ε = 0` IN `U-UNO` NASCONO `12`-`14` GRUMI.** Il criterio diceva che non deve nascere niente ### **«perché la simmetria non si rompe da sola»**. ### ➜ **E la premessa è FALSA: la simmetria non c'era.** Un `|ψ|` uniforme su questo grafo ### **non è uno stato simmetrico**, perché `Σ_j w_kj` varia di un fattore `16`: ### **il grafo stesso è il campo che rompe la simmetria.**

> ### ⚠ **E IL TEST ERA MAL POSTO, ED È UN DIFETTO MIO:** lo stato che ### **sarebbe** simmetrico non è il costante, ma ### **uno stato stazionario** dell'equazione. ### **Il test giusto parte da quello** — come ho fatto per il solitone discreto nel collaudo `(b)` — e ### **non l'ho fatto qui.**

# ⛔ `⑥` **L'OROLOGIO DI DE BROGLIE: LA MISURA È ALIASATA, E NON LA USO**

| | |
|---|--:|
| il campione è ogni | `0.1000` di tempo |
| quindi `dφ/dt` è risolvibile solo fino a | ### **`± 62.83`** |
| `U-CASO`: `dφ/dt` misurato, min e max | ### **`-61.23` / `62.42`** |
| `U-UNO`: `dφ/dt` misurato, min e max | ### **`-62.82` / `62.82`** |

> ### ⛔ **GLI ESTREMI STANNO ESATTAMENTE AL LIMITE `±2π/Δt`: la fase avanza di più di `2π` fra due campioni, e la differenza avvolta NON è più `dφ/dt`.** ### **La misura è ALIASATA, e non la riporto come se significasse qualcosa** — le correlazioni che ne escono hanno perfino ### **segno opposto** nei due bracci, che è il sintomo. ### ➜ **La cura è campionare la fase A OGNI PASSO, e non ogni `50`: è una misura MANCANTE, non un risultato.**

# ⭐ `⑦` **LE MIE PREVISIONI, CONTRO I NUMERI**

| id | la previsione | il numero | l'esito |
|---|---|---|---|
| `PM-1` | i grumi ### **NASCONO** per i `g` più negativi | `U-UNO`: `22` grumi a `g = -5`, `14` a `-10`, `3` a `-20`; ### **`U-CASO`: `0`, `0`, `0`** | ### ⚠ **MEZZA**: nascono in `U-UNO`, e in `U-CASO` ### **SPARISCONO** al crescere di `\|g\|` |
| `PM-2` | il caso ### **`ε = 0` NON produce niente** | `U-CASO`: `0` grumi; ### **`U-UNO`: `12`-`14`** | ### ⛔ **SMENTITA**, e la premessa era ### **falsa**: la simmetria non c'era |
| `PM-3` | i grumi nascono in ### **ENTRAMBI** i bracci | a `g = -10`: `U-UNO` `14`, ### **`U-CASO` `0`** | ### ⛔ **SMENTITA**: in `U-CASO` la non linearità ### **DISTRUGGE** la localizzazione invece di crearla |
| `PM-4` | a `g = 0` il mare resta uniforme entro `2` in ### **`U-UNO`** ma non in `U-CASO` | `U-UNO`: ### **12.68, 7.74, 11.51**; `U-CASO`: 6.04, 6.22, 6.57 | ### ⛔ **SMENTITA, E AL CONTRARIO**: `U-UNO` localizza ### **PIÙ** di `U-CASO` |
| `PM-5` | l'orologio di de Broglie ### **si vede** | ### **la misura è ALIASATA** *(estremi al limite `±2π/Δt`)* | ### ⛔ **NON VALUTABILE**: non la uso, ed è una misura ### **mancante** |
| `PM-6` | la ### **vita** è lunga per i `g` grandi e corta per `g = -2` | `U-UNO`, vita max in `t_c`: `-2` → 19.0, `-5` → 48.0, `-10` → ### **97.0**, `-20` → 88.0 | ### ⛔ **SMENTITA**: non è monotona — il massimo è a `g = -10`, e a `-20` ### **cala** |

> ### ⛔ **4 previsioni su 6 SMENTITE, e due di quelle erano scritte per poter perdere.** ### **Il pezzo che vale è `PM-4`: avevo previsto che il disordine venisse dal GAUGE, e viene dal GRAFO — al contrario.**

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE**

| | |
|---|---|
| che ### **le masse nascono** | ### ⛔ **NO.** Il criterio ### **non è decidibile come è scritto**, perché il controllo a `g = 0` non è un controllo |
| che ### **non nascono** | ### ⛔ **neanche questo:** in `U-UNO` a `g = -10` ci sono `14` grumi con vita fino a `97.0 t_c`. ### **Ma a `g = 0` ce ne sono `6` con vita `43`**: senza un controllo pulito ### **non si attribuisce** |
| che i grumi siano ### **masse** | ### **sono grumi di `\|ψ\|²` che durano.** Che si attraggano, con che legge, e se cadano tutti allo stesso modo sono ### **le tre prove** di `doc/IPOTESI_gravita_a_spinta.md`, e restano ### **fuori** |
| la ### **variabilità** | `3` semi: ### **`P3` NON è soddisfatta** |
| che `w` e `U` siano ### **memorie** | ### ⛔ **sono FISSI**, ed è una violazione ### **dichiarata** di `A16.3`. La memoria dinamica dentro `H` è il passo successivo, e ### **è una decisione di Luca** |
| l'### **orologio** | ### ⛔ **aliasato, quindi NON misurato** |
| l'esperimento del ### **pacchetto** | ### ⛔ **NON girato:** il tetto dei `20` minuti era già superato, e il mandato dice di fermarsi |

