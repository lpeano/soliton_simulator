# IL CONTRATTO DELL'ORDINE NELLA NASCITA

> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: `csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- misurato A UN ISTANTE** — ### **la CI NON lo rigenera**, e il presidio verifica ### **il suo BLOB**. ### **Per rimisurarlo si rigira il suo comando AL SUO COMMIT**, come un sigillo *(`CLAUDE.md` par. `6`)*.

> ### **GENERATO da `csv/_contratto_nascita.py` dal referto della misura. NON si modifica a mano** *(`L-NUMERI`)*.
> **Passo 2 del `COMMIT 3` del riordino** *(`doc/PIANO_riordino_mitosi.md`, parte (c))*.
> **Il referto:** `csv/_test_fork/_ordine_estrazioni/_ordine_estrazioni.json` *(strumento `a4c65607`, simulatore `3ddc56d9`)*.

**Perche' esiste:** il piano dichiara il rischio -- *spostare le scritture della nascita in un punto solo puo' cambiare l'ORDINE DELLE ESTRAZIONI e delle SOMME, e il generatore e' UNO: chi pesca prima cambia cio' che pescano tutti*. ### **Questo documento dice qual e' l'ordine da RISPETTARE**; non dice che il commit 3 lo rispettera'.

---

## 1. LA SEQUENZA DELLE ESTRAZIONI, per PASSO -- e questa e' la parte stretta del contratto

*(scena grande, seme 11, dal passo 40 al 72; la VOCE si ricava dalla composizione IN USO, non dal nome cablato.)*

### Un passo SENZA nascite -- **3 estrazioni** *(passo 41)*

| # | voce | metodo | elementi |
|--:|---|---|--:|
| 1 | `scuoti_vuoto` | `rng.normal` | 12802 |
| 2 | `step` | `rng.normal` | 38406 |
| 3 | `mitosi` | `rng.random` | 471564 |

### Un passo CON nascite -- **4 estrazioni** *(passo 42)*

| # | voce | metodo | elementi | che cos'e' |
|--:|---|---|--:|---|
| 1 | `scuoti_vuoto` | `rng.normal` | 12802 |  |
| 2 | `step` | `rng.normal` | 38406 |  |
| 3 | `mitosi` | `rng.random` | 471564 | ### **la DECISIONE** (`decidi_divisione`: `rng.random(len(avv))`), e pesca **a OGNI passo**, anche quando non nasce niente -- gli elementi sono **tutti gli archi** |
| 4 | `mitosi` | `rng.random` | 1 | ### **lo SCHWINGER** (`estratto = rng.random(len(sel))`), e c'e' **solo nei passi con nascite**: gli elementi sono gli archi SELEZIONATI |

### ⚠ **E UN RAMO CHE NON PESCA, dichiarato perche' la sua ASSENZA e' parte del contratto**
`ANTIFASE_ADD` pescherebbe (`flip = rng.random(len(sel))`) ed e' ### **spento nella configurazione di riferimento**: nella finestra misurata ### **quell'estrazione non compare.** ### ➜ **Se un giorno si accendesse, la sequenza avrebbe CINQUE estrazioni e questo contratto non la coprirebbe.**

## 2. LE ESTRAZIONI FUORI DAL PASSO -- **42**, e si contano a parte

| dove | metodo | chiamate | elementi |
|---|---|--:|--:|
| scena MASSE-COERENTI (avvia_test) | `rng.choice` | 16 | 573253 |
| scena MASSE-COERENTI (avvia_test) | `rng.normal` | 4 | 14039 |
| scena MASSE-COERENTI (avvia_test) | `rng.random` | 16 | 1694155 |
| vuoto (_applica_flag, dentro carica_dal_cli) | `rng.choice` | 1 | 900 |
| vuoto (_applica_flag, dentro carica_dal_cli) | `rng.normal` | 3 | 6300 |
| vuoto (_applica_flag, dentro carica_dal_cli) | `rng.random` | 2 | 1800 |

## 3. L'ORDINE DEGLI ADDENDI -- e la misura RESTRINGE il contratto invece di allargarlo

| la proprieta' | misurata |
|---|---|
| `a + b` contro `b + a` *(DUE addendi)* | ### **byte-identici: True** ⇒ l'ordine **NON** conta
| `(a+b)+c` contro `a+(b+c)` *(TRE addendi)* | ### **identici: False** -- differenze ### **48083 su 200000** ⇒ l'ordine **CONTA**

### ➜ **Quindi l'ordine degli addendi entra nel contratto DA TRE IN SU.** E nel perimetro della nascita:

| | |
|---|--:|
| somme `+` nelle 5 funzioni, ### **qualunque bersaglio, LOCALI COMPRESE** | **39** |
| con **2** addendi | 39 |
| ### **con TRE o piu'** | ### **0** |

### ✅ **ZERO con tre o piu' addendi, e questo CHIUDE un buco del mio strumento invece di nasconderlo:** il classificatore parte dalle scritture di `self.<nome>`, quindi ### **perde le somme che passano da una LOCALE** *(`pos_figlio = 0.5 * (pos[a] + pos[b])`)*. ### ➜ **Ma se NESSUNA somma del perimetro ha tre addendi, una somma persa in una locale NON PUO' CAMBIARE IL VERDETTO.** Il limite si chiude con una misura, non con una promessa.

## 4. LE RIDUZIONI -- **9**, e li' l'associativita' morde davvero

### ⚠ **NON sono solo `np.add.at` e `np.bincount`** *(rilievo del guardiano, 2026-10-02)*: ### **una `.mean()` in virgola mobile lo e' anche**, e la prima stesura del rilevatore ### **la perdeva.** Sono **accumulazioni su molti termini**, non somme scritte.

| riga | funzione | scrive | forma | gate |
|--:|---|---|---|---|
| `:3708` | `semina` | *(locale) u* | `np.linalg.norm` | `NOT (SEMINA_LAM)` |
| `:3919` | `_allaccia` | *(locale) rc* | `np.median` | - |
| `:7304` | `mitosi` | - | `np.add.at` | `MITOSI_DIR != 0.0` |
| `:7305` | `mitosi` | - | `np.add.at` | `MITOSI_DIR != 0.0` |
| `:7334` | `mitosi` | ### **`ultima_frac_antifase`** | `flip.mean` | `ANTIFASE_ADD` |
| `:7479` | `mitosi` | ### **`ultima_prob_coppia`** | `prob_coppia.mean` | `COPPIA_MIT > 0.0` |
| `:7501` | `mitosi` | *(locale) pmed* | `np.median` | `COPPIA_MIT > 0.0` AND `estratto.any()` |
| `:7505` | `mitosi` | ### **`_g_peqn_mediana`** | `np.median` | `COPPIA_MIT > 0.0` AND `estratto.any()` AND `PEQ_NASCITA_LOCALE` |
| `:7495` | `mitosi` | *(locale) dd* | `np.linalg.norm` | `COPPIA_MIT > 0.0` AND `estratto.any()` |

### **I FLAG dei gate, dal RUNTIME:** `MITOSI_DIR = 0.0`  ·  `ANTIFASE_ADD = False`  ·  `COPPIA_MIT = 1.0`  ·  `COPPIA_DENSITA = False`  ·  `PEQ_NASCITA_LOCALE = True`  ·  `PLAST_DIN = True`  ·  `PLAST_MIT = 0.0`  ·  `MITOSI_2LAM = True`  ·  `REGIME = 'deterministico'`  ·  `SEMINA_LAM = True`  ·  `CHI_COOP = True`

### ✅ **QUALI riduzioni dipendano dall'ordine e' MISURATO, non dichiarato a parole**

| | |
|---|---|
| MEDIA in virgola mobile | ### **dipende dall'ordine da `n = 3` IN SU** -- `200` vettori DIVERSI per taglia: `n=1`: 0, `n=2`: 0, `n=3`: 10, `n=4`: 25, `n=5`: 38, `n=8`: 61, `n=64`: 72, `n=4096`: 62 |
| MEDIA di **BOOLEANI** | **0** su 200 ⇒ ### **ESATTA**, l'ordine non conta *(e' il caso di `flip.mean()`)* |
| **MEDIANA** | **0** su 200 ⇒ l'ordine **non conta** |
| `norm(axis=1)` **per riga** | permutando le **RIGHE**, la norma di una riga cambia **0** volte su 50 ⇒ l'ordine delle righe **non entra** |

### ⛔ **E LA SOGLIA `n = 3` COINCIDE con la misura IEEE-754 del par. 3** *(due addendi commutativi al bit, TRE no)*: ### **le due misure si confermano a vicenda.**
### ⚠ **E una versione precedente di questo referto diceva «inerte fino a 4, ordine-dipendente da ~8»: era un FALSO ZERO** -- usava **UN SOLO vettore per taglia**, e per `n = 3` e `n = 4` quel vettore dava `0` **per caso**. ### **La riga vecchia resta nel repo** *(par.8)*, e questa e' la correzione.

### ⭐ **LA REGOLA DEL CONTRATTO SU `ultima_prob_coppia`, DERIVATA dai numeri**

> ### **`ultima_prob_coppia` e' inerte all'ordine SOLO SE `len(sel) <= 2`; da `3` in su DIPENDE dall'ordine degli archi.**

| | |
|---|---|
| la soglia **misurata** | `n = 3` |
| le taglie **vere** di `len(sel)` nella finestra | `1`, `1`, `1`, `1`, `1`, `1`, `1`, `2` |
| ### **l'esito** | ### **INERTE NELLA FINESTRA, con margine 1** |

### ⚠ **E NON E' INERTE PER LEGGE: lo e' perche' la scena divide POCO.** Il margine e' di ### **pochi archi**: ### **un passo con `3` divisioni la renderebbe ordine-dipendente SENZA che nessuna legge sia cambiata.** ### **E' la forma che `A8` chiama pericolosa:** *un'inerzia che dipende da un numero di oggi non e' un'inerzia, e' una coincidenza che vale finche' dura.*

## 4-bis. ⛔ **E IL SIGILLO NON CONFRONTA TRE DI QUESTE GRANDEZZE**

La regola del braccio `B` *(letta da `csv/_seal_fork/_sig_controllo_unico.py`, `_contatori`)* confronta ### **DUE insiemi**: le grandezze di `REGISTRO_NOMI`, e i **contatori** = ogni attributo che ### **comincia con `_` ED E' UN INTERO.**

| grandezza | nel registro? | contatore? | tipo a runtime | ### **confrontata?** |
|---|---|---|---|---|
| `_g_peqn_mediana` | False | False | `float` | ### **NO** |
| `ultima_frac_antifase` | False | False | `NoneType` | ### **NO** |
| `ultima_prob_coppia` | False | False | `float` | ### **NO** |

### ➜ **Quindi un cambio d'ordine su queste tre NON farebbe cadere il sigillo: ci passerebbe accanto IN SILENZIO.** ### **E' `A8` applicato al sigillo.**
### ⚠ **E `_g_peqn_mediana` e' il caso peggiore:** porta il prefisso `_g_` dei contatori, ### **quindi un lettore la crede coperta**, e non lo e' perche' e' un `float`.
### ✅ **REQUISITO PER IL SIGILLO DEL COMMIT 3, scritto QUI e PRIMA:** deve confrontare ### **anche queste tre**, non solo il registro e i contatori interi.

## 5. L'ORDINE DEI PEZZI DI OGNI CONCATENAZIONE -- **68**, e sta nella TABELLA

### **Per una CONCATENAZIONE l'ordine conta SEMPRE e per qualunque tipo**, perche' decide ### **quale valore va a quale INDICE**: non e' l'ultimo bit, e' il **significato**. *(Permutare `concatenate([i[keep], a, m])` non sposta un bit: cambia quali nodi sono collegati.)*

### ➜ **Riga per riga, l'ordine sta nella colonna `ordine_pezzi` di `doc/REGOLE_nascita.tsv`**, abbinato ### **PER ANCORA** *(la funzione `mitosi` copre DUE eventi, quindi `(funzione, grandezza)` non basta a scegliere la riga)*.

| | |
|---|--:|
| righe della tabella | **32** |
| abbinate a UNA concatenazione | **14** |
| senza concatenazione nel perimetro misurato | 17 |
| ### con ancora NON UNIVOCA *(dichiarate, non scelte)* | ### **1** |

### ⚠ **E le 17 senza concatenazione NON sono un buco:** sono le regole il cui valore nasce da una **scrittura diversa** *(una `np.full`, una mutazione in posto, una regola di `phi` che passa da una locale)*. ### **La colonna lo DICE invece di lasciare un campo vuoto**, perche' un campo vuoto si legge come *«non misurato»*.

---

## ⛔ CHE COSA QUESTO CONTRATTO **NON** DICE

| | |
|---|---|
| **non dice che il commit 3 lo rispettera'** | dice ### **qual e' l'ordine.** La verifica e' il **sigillo**, e il criterio e' **byte-identico fino al 72, contatori compresi** |
| ### **non copre un'altra CONFIGURAZIONE** | la sequenza delle estrazioni dipende dai flag: `ANTIFASE_ADD` spento, `COPPIA_MIT = 1.0`, `MITOSI_DIR = 0.0`, `REGIME` deterministico. ### **Con altri flag l'ordine cambia, e questo documento NON vale** |
| ### **non copre le riduzioni del ramo spento** | `MITOSI_DIR = 0.0`: le due `add.at` non girano, e ### **il contratto di oggi non le descrive** |

---

## 5. I VINCOLI D'ORDINE — **e sono QUATTRO**

### ⚠ **PRIMA DEL `COMMIT 5` QUESTO DOCUMENTO NON LI ELENCAVA.** I quattro vincoli erano nominati
### **solo nei commenti del codice** *(«vincolo 2 del contratto», «vincolo 3 del contratto»)*, e
chi leggeva **il contratto** non li trovava. ### **Un vincolo che vive solo nel codice che lo
rispetta non e' un contratto: e' un'abitudine.** Elencarli e' il minimo, e il `4` nasce qui.

| | il vincolo | dove vive nel codice | perche' |
|---|---|---|---|
| **1** | ### **`phi` PRIMA di `twp`** | `mitosi`, nella preparazione | `_rn_div_twp` legge `phi[a]`/`phi[b]` ### **DOPO il calcio**, che e' una scrittura indicizzata sui genitori |
| **2** | ### **`_peqn_idx` subito DOPO `peq`** | `_ordine_di_nascita()` | l'indice segue la grandezza che indicizza |
| **3** | ### **le regole NON leggono `self.n`** | `nascita()`, e il contesto porta `c["n0"]` | `self.n` e' una `@property` su `len(self.phi)`: leggerla ### **a META' della nascita** dava un valore che cambiava sotto i piedi |
| ### **4** | ### **`perc_geom` DOPO `tw`** *(`COMMIT 5`, 2026-10-03)* | `_ordine_di_nascita()`, coi ### **due presidi** | ### **la derivazione di `perc_geom` LEGGE `tw`**: nell'ordine del registro cadeva al posto **17** contro il **31** di `tw`, cioe' ### **prima che i nuovi archi avessero una torsione** |

### 📌 **E I VINCOLI `2` E `4` SONO LA STESSA FORMA:** una grandezza ### **si colloca** invece di
stare dove la mette il registro, ### **e il motivo e' DICHIARATO.** Il `3` e' di natura diversa —
non e' una collocazione, e' un ### **divieto di lettura**.

### ⚠ **IL `4` HA DUE PRESIDI, e il `2` no:** se `perc_geom` o `tw` uscissero dai registri, il
vincolo `4` romperebbe ### **in silenzio** e la derivazione tornerebbe a leggere un `tw` che non
c'e' ancora — cioe' ### **tornerebbe a essere la costante `-1` travestita.** I due
`raise RuntimeError` esistono per questo *(`A9`: un vincolo **scritto** non e' un presidio)*.
### ➜ **E il `2` ne e' SCOPERTO: e' un difetto di simmetria, non curato qui.**

### ✅ **E L'ORDINE RESTA DI `36` VOCI:** il vincolo `4` ### **SPOSTA**, non aggiunge ne' toglie —
verificato dal modulo, non assunto.
