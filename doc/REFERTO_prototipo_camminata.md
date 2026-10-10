# 🔬 **IL PROTOTIPO DELLA CAMMINATA A MONETA — LE SETTE LETTURE**

> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: `csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- misurato A UN ISTANTE** — la CI ### **non lo rigenera**, e il presidio verifica ### **il suo BLOB.**

*(**Generato** da `python proto_camminata/_referto.py`, che legge `proto_camminata/uscite/letture.json` prodotto da `python proto_camminata/_letture.py`. Criteri, previsioni e soglie: `doc/TASK_HISTORY/2026-10-10_prototipo_camminata.md`, **committato PRIMA del codice**.)*

**LA SCENA:** `irregolare(n=120,gmin=2,gmax=6,seme=11)` — **120** nodi, **208** archi, **416** estremita-, gradi **[2, 3, 4, 5, 6]**; controllo `regolare(n=120,salti=(1, 2))`; semi **[11, 23, 37, 53]**.

## ⭐ **I SETTE VERDETTI, in una tabella**

| | la lettura | la PREVISIONE *(scritta prima)* | il verdetto |
|---|---|---|---|
| `1a` | **ISOTROPIA della camminata** | isotropia **esatta** per costruzione | ### ✅ **CONFERMA** |
| `1b` | **ANISOTROPIA dell-integratore** | l-anisotropia dell-integratore **scende come `dt^2`** | ### ⛔ **SMENTITA** |
| `2` | **CONO** | oltre il cono, **zero al bit** | ### ✅ **CONFERMA** |
| `3` | **QUANTITA- CONSERVATA** | **non lo so**, ed e- la domanda aperta — ### **nessuna previsione da smentire** | ### ⛔ **NESSUNA TROVATA** *(criterio di RIAPERTURA)* |
| `4` | **CLUSTER** | **non ho ragioni** per aspettarmi che il cluster tenga | ### ⛔ **LA NON LINEARITA- NON BASTA** |
| `5` | **MATERIA / ANTIMATERIA** | `(A)` **DEVE** rompere la simmetria, `(B)` **no** | ### ✅ **CONFERMA** |
| `6` | **`r=1`** | `r=1` coincide col `dt` globale **al bit** | ### ✅ **CONFERMA** |
| `7` | **GAUGE, ROVESCIATO** | un fattore comune **CAMBIA** la fisica *(per costruzione)* | ### ✅ **CONFERMA** |

## 📌 **I NUMERI, lettura per lettura**

### `1a` **ISOTROPIA della camminata** — ### ✅ **CONFERMA**

`fsum` = **0** *(zero al bit)*; `numpy` = **1.07e-16** su soglia **7.99e-14**

### `1b` **ANISOTROPIA dell-integratore** — ### ⛔ **SMENTITA**

pendenza misurata **2.885 +/- 0.051** su `4` valori di `dt` e `7` strati; il criterio era **`|pendenza - 2| <= 3 sigma`**, cioe- **0.885 <= 0.152**

### `2` **CONO** — ### ✅ **CONFERMA**

oltre **3** archi: `max|differenza|` = **0** su **178** estremita-, con **57** nodi fuori dal cono *(eccentricita- **6**)*

### `3` **QUANTITA- CONSERVATA** — ### ⛔ **NESSUNA TROVATA** *(criterio di RIAPERTURA)*

per la camminata **LINEARE** le **quattro** candidate sono **tutte CONSERVATE** *(ed e- il controllo positivo: senza di lui il test non direbbe niente)*; per le **8** varianti non lineari la **norma** e- conservata **sempre**, e delle **tre** candidate oltre la norma ****NESSUNA si conserva****

### `4` **CLUSTER** — ### ⛔ **LA NON LINEARITA- NON BASTA**

la dispersione **CRESCE** in ogni variante: **+0.237** con la lineare, e da **+0.212** a **+0.052** sulla scansione di `g`; la frazione **intrappolata** resta **0.043**..**0.093**. ### ⭐ **E la crescita SCENDE con `g`, in modo MONOTONO** su `4` valori

### `5` **MATERIA / ANTIMATERIA** — ### ✅ **CONFERMA**

**`(A)` ROMPE la coniugazione in 4 varianti su 4** *(differenza fino a **0.229**, asimmetria dell-intrappolamento fino a **0.0763**)* — ### ed e- **IL BRACCIO CHE DEVE FALLIRE**; **`(B)` la rispetta AL BIT in 4 su 4** *(differenza **esattamente 0**, asimmetria **esattamente 0**)*

### `6` **`r=1`** — ### ✅ **CONFERMA**

`max|differenza|` = **0**, e sono **due strade di codice diverse** *(la moneta per nodo e quella a `dt` scalare)*

### `7` **GAUGE, ROVESCIATO** — ### ✅ **CONFERMA**

un fattore comune **CAMBIA** lo stato: `c=0.5` -> **0.204**, `c=2` -> **0.159**, contro una soglia di arrotondamento di **7.99e-14** — cioe- **12 ordini di grandezza sopra**

## ⛔ **LE TRE COSE CHE QUESTO REFERTO DICE E CHE NON ERANO NEL PIANO**

### `1` **`(A)` E `(B)` SONO INDISTINGUIBILI SULLA LETTURA `4`, E NON E- UN DIFETTO: E- LA DERIVAZIONE.** Su un cluster **tutto nella banda `+`** vale `s = rho`, quindi la fase **dispari** e quella **pari** sono **la stessa fase** — e i numeri della lettura `4` coincidono **cifra per cifra**. ### ⭐ **Solo la lettura `5`, che costruisce il CONIUGATO, le separa** — e le separa **al bit.**

### `2` **LA CRESCITA DELLA DISPERSIONE SCENDE CON `g`, IN MODO MONOTONO.** Il cluster **non tiene** con nessun `g` provato *(la coerenza si perde sempre)*, ### ⚠ **ma la perdita e- sempre piu- lenta**, e su `4` valori la tendenza e- **monotona** — quindi ### **non e- una finestra stretta** *(la terza domanda della stella polare)*. ### ⛔ **Che cosa farne e- una decisione di Luca**, e sta in una voce.

### `3` **LA SOGLIA `dt^2` DEL PIANO E- SMENTITA, E IL MOTIVO E- CHE L-INTEGRATORE E- MIGLIORE DI COSI-.** La composizione a strati e- **SIMMETRICA alla Strang**, quindi ### **l-errore di ordine PARI si annulla** e l-anisotropia va come **`dt^3`**. ### ✅ **Il criterio scritto prima FALLISCE**, e lo scrivo invece di aggiustarlo: ### **la previsione era PESSIMISTA.**

## ✅ **CHE COSA SBLOCCA O RIAPRE NELL-ALBERO** *(e nessuna decisione e- mia)*

| il nodo | che cosa dicono i numeri | che cosa NON dicono |
|---|---|---|
| **[[DOMANDA-QUANTITA-CONSERVATA]]** *(la prossima)* | la **norma** si conserva **sempre**, anche con le non lineari; delle **tre** candidate oltre la norma **nessuna** si conserva per nessuna delle **8** varianti provate | ### ⛔ **NON dicono che non esista:** dicono che **non l-ho trovata fra le candidate DICHIARATE** — ed e- la forma giusta di un **criterio di RIAPERTURA**, non una dimostrazione di assenza |
| **[[MATERIA-ANTIMATERIA-SPAZIO]]**, condizione `(b)` | la fase **dispari sotto `C`** la soddisfa ### **AL BIT**, su `8` varianti e `2` semi: materia e antimateria si comportano **identicamente** | non dicono che `(B)` sia **la** forza di coesione: dicono che e- **ammissibile**, mentre `(A)` **non lo e-** |
| **la forza di COESIONE** *(il nodo `FC`)* | la fase dispari e- **una candidata ammissibile**, e la crescita della dispersione **scende con `g`** | non dicono **quale** forma, ne- **da dove** viene `g` — che e- `A1` |
| **[[TEMPO-PROPRIO-LOCALE]]** | la lettura `7` **conferma la correzione del punto `0`**: un fattore comune sugli `r_k` cambia lo stato di **`0.16`-`0.20`**, contro un arrotondamento di **`8e-14`** | non dicono **da dove viene `r_k`**: resta la domanda aperta, e adesso ### **con il vincolo in piu- della SCALA ASSOLUTA** |
| **[[DOMANDA-FORME-VUOTO]]** e la divisione del lavoro | ### ⛔ **NIENTE: questo prototipo non le ha toccate**, e dirlo e- parte del referto | il vuoto locale non e- implementato: ### **`cs_k = 1` ovunque**, dichiarato |

## ⚠ **I LIMITI, dichiarati**

| | il limite |
|---|---|
| `1` | ### **`cs_k = 1` ovunque:** questo prototipo **non prova la `cs` locale**, e i punti `3`-`6` di [[TEMPO-PROPRIO-LOCALE]] restano **da provare altrove** |
| `2` | ### **`r_k` e- DATO, non derivato** *(il mandato lo dice)*: la derivazione e' la domanda aperta |
| `3` | ### **un solo grafo irregolare** e un solo regolare: **non e- uno scaling di taglia finita** *([[TAGLIA-FINITA]])*, e due taglie **non sarebbero uno scaling** |
| `4` | la lettura `4` guarda **un cluster costruito da me**: se la coerenza dipendesse dalla **forma** del cluster, questo referto **non lo vedrebbe** |

