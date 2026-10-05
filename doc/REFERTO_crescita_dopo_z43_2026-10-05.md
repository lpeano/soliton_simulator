# REFERTO -- `CRESCITA-DOPO-Z43`: **perche' la rete quasi non cresce piu'**

*(Mandato di Luca del 2026-10-05, piu' le **quattro verifiche del guardiano**, **rifatte sui dati di questa corsa** e non ricopiate. Cancelli, controlli e `STELLA POLARE` in `doc/TASK_HISTORY/2026-10-05_crescita-dopo-z43-misura.md`, committato **prima** dello strumento in `9a11cda`.)*

| | |
|---|---|
| **`Ap`** | la `PARTE A`, blob `062172d3` *(dal tag `pre-z43-cura2-r-da-cs`)* |
| **`Bp`** | la `PARTE B`, blob `f7237563` |
| **`Bc`** | il **CONTROFATTUALE**, ### **dichiarato FINTO** *(`r` per `1/mediana(r)`)* |
| **strumento** | `a3db21b2` |
| **piattaforma** | Windows 11, python `3.13.2`, numpy `2.3.0`, `AMD64` |
| **passi** | `150`, seme `11`, scena del driver |
| **configurazione dichiarata INTERA** | `True` *(braccio `Bp`)* |

## IL RISULTATO IN UNA RIGA

| | `Ap` | `Bp` | `Bc` |
|---|--:|--:|--:|
| **divisioni** | `1219` | `18` | `70` |
| nascite **Schwinger** | `307` | `7` | `19` |
| `nati` *(dal simulatore)* | `1526` | `25` | `89` |
| `n` finale | `14328` | `12827` | `12891` |

### **Il fattore sulle divisioni `Ap/Bp` = `67.722222`.**

## LA SCOMPOSIZIONE DEL FATTORE -- **tre fattori, e il prodotto deve tornare**

*(Verifica `2` del guardiano.)* ### **E' una scomposizione ESATTA, non una stima:** ogni fattore e' un rapporto fra due conteggi, e il loro prodotto ### **e' il fattore sulle divisioni per costruzione algebrica** -- i denominatori si cancellano a due a due. ### **Il suo valore non e' <<tornare>>: e' DOVE sta il fattore.**

| finestra | **(a)** popolazione nella finestra | **(b)** tasso di estrazione per arco | **(c)** cancello `2LAM` | **prodotto** | divisioni `Ap` | divisioni `Bp` | rapporto |
|---|--:|--:|--:|--:|--:|--:|--:|
| `1`-`150` | `16.790` | `3.327` | `1.213` | **`67.722`** | `1219` | `18` | `67.722` |
| `60`-`100` | `42.140` | `2.460` | `2.527` | **`262.000`** | `262` | `1` | `262.000` |
| `100`-`150` | `14.024` | `3.545` | `1.129` | **`56.118`** | `954` | `17` | `56.118` |

**Che cosa sono i tre fattori:**
* **(a)** quanti **passi-arco** entrano nella finestra `soglia < |tw| < 4pi` col segno di creazione *(`Sum g1^g2^g3`)*;
* **(b)** la **probabilita' per arco** di essere estratto, una volta dentro la finestra *(`Sum g4 / Sum g1^g2^g3`)*: ### **e' qui che vive `_ft = dt_e/DT`**, cioe' il rallentamento;
* **(c)** la frazione dei candidati che supera `A13`/`2LAM`.

> ### **SU TUTTA LA CORSA IL FATTORE DOMINANTE E' (a) la POPOLAZIONE nella finestra, con `x16.79` su `x67.72` totale.**
>
> ### ⚠ **E LA FINESTRA `60`-`100` NON VA LETTA COME LE ALTRE: `Bp` ha `1` divisioni in tutto.** ### **Un rapporto costruito su `1` evento non ha peso statistico**, e lo dico invece di riportare il numero come se ne avesse.

## L'ARTEFATTO SUL CANCELLO `2` -- **una popolazione FISSA oltre il tetto**

*(Verifica `1` del guardiano.)* Gli archi che passano il cancello `1` e **non** il `2` sono ### **esattamente quelli con `|tw| >= 4pi`** -- e' un'**identita'**, perche' il cancello `2` e' `avv < 4pi`.

| braccio | passi-arco oltre `4pi` | su `Sum g1` | per passo: min | mediana | max | al passo `1` | al passo `2` | all'ultimo |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| `Ap` | `14981` | `10.2 %` | `0` | `104.5` | `110` | `0` | `109` | `81` |
| `Bp` | `14338` | `61.8 %` | `0` | `105.5` | `109` | `0` | `109` | `57` |
| `Bc` | `14153` | `44.9 %` | `0` | `105.5` | `109` | `0` | `109` | `57` |

### I SALTI **SENZA** quella popolazione

| braccio | `Sum g1` grezzo | oltre `4pi` | `Sum g1` NETTO | `Sum g1^g2` | salto del cancello `2` | **NETTO** |
|---|--:|--:|--:|--:|--:|--:|
| `Ap` | `146907` | `14981` | `131926` | `131926` | `0.8980` | **`1.0000`** |
| `Bp` | `23190` | `14338` | `8852` | `8852` | `0.3817` | **`1.0000`** |
| `Bc` | `31534` | `14153` | `17381` | `17381` | `0.5512` | **`1.0000`** |

> ### ✔ **E IL SALTO NETTO DEL CANCELLO `2` E' `1.0000` IN ENTRAMBI I BRACCI: una volta tolta quella popolazione, IL CANCELLO `2` NON PERDE NIENTE.** ### **Non e' un canale: e' la DILUIZIONE di una popolazione fissa** che e' oltre il tetto **dal passo `2`** e non torna piu' indietro.
>
> **Il rapporto `Bp/Ap` su `g1`:** `0.1579` **grezzo**, `0.0671` sul **netto**. ### **La differenza fra i due E' l'artefatto**, e nella `PARTE B` quella popolazione e' una frazione molto piu' grande di `g1` che nella `PARTE A` -- ### **non perche' sia piu' numerosa, ma perche' `g1` e' piu' piccolo.**
>
> ### ⛔ **E QUESTO CORREGGE IL MIO RAPPORTO PRECEDENTE** *(`92da889`)*, dove avevo scritto che **<<la separazione cade su TRE cancelli>>** contando il `2` fra i tre. ### **Il cancello `2` non e' un canale**, e i canali veri sono i tre fattori della scomposizione qui sopra.

## LA SOGLIA **DEGLI ARCHI CHE PASSANO**, non quella mediana della rete

*(Verifica `3` del guardiano.)* `soglia_su_g1` e' la soglia **sugli archi che superano il cancello `1`**, ed e' registrata **a ogni passo**.

| passo | | `Ap` q05 | `Ap` **q50** | `Ap` q95 | `Bp` q05 | `Bp` **q50** | `Bp` q95 | `Bc` q05 | `Bc` **q50** | `Bc` q95 |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `50` | | `7.1415` | **`8.2921`** | `9.3426` | `8.3281` | **`8.9827`** | `9.3821` | `8.0890` | **`8.8730`** | `9.3713` |
| `70` | | `7.0060` | **`7.3694`** | `9.2231` | `8.3657` | **`9.0277`** | `9.4029` | `8.0119` | **`8.8202`** | `9.3937` |
| `100` | | `6.9900` | **`7.3891`** | `8.5327` | `8.2038` | **`8.7710`** | `9.3512` | `7.9594` | **`8.4215`** | `9.3499` |
| `140` | | `7.0000` | **`7.4327`** | `8.7284` | `8.0790` | **`8.5111`** | `9.3276` | `7.8610` | **`8.2711`** | `9.2514` |

**La soglia non modulata e' `soglia0` = `9.424778`** *(`= 3pi`)*, e **il minimo possibile** e' `soglia0 * (1 - 0.3*tanh(sqrt(2)))` = ### **`6.9129`** -- il `sqrt(2)` e' il gradiente massimo possibile quando `r` sta in `(0, sqrt(2)]`.

**Il `q05` piu' basso osservato su questi quattro passi e' `6.9900`**, cioe' `0.0771` sopra il pavimento.

> ### LO STATO DELL'IPOTESI DEL GUARDIANO, scritto come lui chiede:
> ### **<<FALSA al mediano della rete** *(l'errore e' del guardiano e lui lo dichiara)*, ### **SOSTENUTA sugli archi che entrano nella finestra.>>**
>
> ### ⛔ **ED E' UNA CORRELAZIONE, NON UNA CAUSA -- e il meccanismo per cui lo e' si puo' nominare:** l'insieme `g1` e' definito da `avv > soglia`, cioe' ### **si seleziona condizionando su `soglia` BASSA.** Un insieme scelto perche' la sua soglia e' stata superata ### **ha per costruzione soglie piu' basse della rete**, in QUALUNQUE braccio e con qualunque meccanismo. ### **Quindi <<la soglia e' bassa dove nascono>> non dimostra <<nascono perche' la soglia e' bassa>>:** e' un effetto di SELEZIONE, e separare le due cose vuole un intervento sulla soglia, non un'osservazione.

## (a) LA CATENA DEI CANCELLI -- totali sui `150` passi

| il cancello | `Ap` | `Bp` | `Bc` | `Bp/Ap` |
|---|--:|--:|--:|--:|
| archi totali | `70794938` | `70735095` | `70737183` | `0.999155` |
| `1` sopra soglia | `146907` | `23190` | `31534` | `0.157855` |
| `1`+`2` dentro la finestra `soglia`-`4pi` | `131926` | `8852` | `17381` | `0.067098` |
| `1`+`2`+`3` segno di CREAZIONE | `129918` | `7738` | `16162` | `0.059561` |
| `4` l'estrazione | `1508` | `27` | `83` | `0.017905` |
| `5` dopo `MITMAX` | `1508` | `27` | `83` | `0.017905` |
| rifiutati **solo per densita'** | `0` | `0` | `0` | `n/d` |
| rifiutati **solo per `2LAM`** | `289` | `9` | `13` | `0.031142` |
| rifiutati **per entrambi** | `0` | `0` | `0` | `n/d` |
| **-> divisioni** | `1219` | `18` | `70` | `0.014766` |

> ### ✔ **I RIFIUTATI PER DENSITA' SONO `0` IN TOTALE SUI TRE BRACCI:** il cancello `6` ### **non chiude niente**, ed era ### **dichiarato quasi-inerte PRIMA di misurarlo** *(`QMIN_M = 0.0`, quindi la condizione e' `0.5*(I[a]+I[b]) >= 0`)*. ### **Dichiararlo prima e' l'unico motivo per cui questo non e' una scoperta.**

## (b) LE GRANDEZZE CHE I CANCELLI LEGGONO

> ### ⛔ **UNA CORREZIONE A CIO' CHE AVEVO SCRITTO IO** *(verifica `4` del guardiano)*: avevo chiamato *<<lacuna della misura>>* l'assenza delle distribuzioni tardive. ### **I QUANTILI C'ERANO GIA', A OGNI PASSO** -- `avv`, `soglia`, `soglia_su_g1`, `ft`, `segno`, `rapporto_avv_soglia`, `prob_su_g123` -- e la tabella della soglia qui sopra ne e' la prova. ### **La lacuna riguardava le DISTRIBUZIONI PIENE** *(il blocco `mod` col gradiente e il morso)*, **non i quantili**, e la frase larga era mia.

**Le distribuzioni piene di questa corsa sono ai passi:** `10`, `50`, `100`, `140`.

### al passo `10`

| braccio | | `r` q50 | **`grad` q50** | `grad` q99 | **`morso` q50** | `morso` q99 | `soglia` q50 | `ft` q50 | `ft` q01 | `ft` q99 |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `Ap` | | `2.1092e-02` | **`1.8696e-02`** | `1.1583e+00` | **`5.6080e-03`** | `2.4614e-01` | `9.3719` | `2.5311e-02` | `1.4978e-03` | `1.4089e+00` |
| `Bp` | | `8.2080e-01` | **`1.2523e-01`** | `4.8780e-01` | **`3.7374e-02`** | `1.3574e-01` | `9.0725` | `7.9330e-01` | `5.2189e-01` | `9.7353e-01` |
| `Bc` | | `1.0000e+00` | **`1.5257e-01`** | `5.9431e-01` | **`4.5420e-02`** | `1.5990e-01` | `8.9967` | `7.9330e-01` | `5.2189e-01` | `9.7353e-01` |

### al passo `50`

| braccio | | `r` q50 | **`grad` q50** | `grad` q99 | **`morso` q50** | `morso` q99 | `soglia` q50 | `ft` q50 | `ft` q01 | `ft` q99 |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `Ap` | | `9.6228e-01` | **`1.6272e-01`** | `1.1263e+00` | **`4.8389e-02`** | `2.4292e-01` | `8.9687` | `9.2364e-01` | `1.9283e-02` | `1.4060e+00` |
| `Bp` | | `7.9750e-01` | **`1.1726e-01`** | `4.6017e-01` | **`3.5017e-02`** | `1.2907e-01` | `9.0948` | `7.7936e-01` | `5.3850e-01` | `9.6696e-01` |
| `Bc` | | `1.0000e+00` | **`1.4703e-01`** | `5.7701e-01` | **`4.3793e-02`** | `1.5615e-01` | `9.0120` | `7.7936e-01` | `5.3851e-01` | `9.6696e-01` |

### al passo `100`

| braccio | | `r` q50 | **`grad` q50** | `grad` q99 | **`morso` q50** | `morso` q99 | `soglia` q50 | `ft` q50 | `ft` q01 | `ft` q99 |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `Ap` | | `1.0122e+00` | **`2.5423e-01`** | `1.2588e+00` | **`7.4668e-02`** | `2.5522e-01` | `8.7210` | `9.1636e-01` | `5.9695e-02` | `1.4004e+00` |
| `Bp` | | `8.1030e-01` | **`1.1234e-01`** | `4.6009e-01` | **`3.3561e-02`** | `1.2905e-01` | `9.1085` | `7.8903e-01` | `5.3700e-01` | `9.6926e-01` |
| `Bc` | | `1.0000e+00` | **`1.3896e-01`** | `5.6475e-01` | **`4.1422e-02`** | `1.5345e-01` | `9.0344` | `7.8912e-01` | `5.3629e-01` | `9.7177e-01` |

### al passo `140`

| braccio | | `r` q50 | **`grad` q50** | `grad` q99 | **`morso` q50** | `morso` q99 | `soglia` q50 | `ft` q50 | `ft` q01 | `ft` q99 |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `Ap` | | `1.0319e+00` | **`2.3533e-01`** | `1.2777e+00` | **`6.9325e-02`** | `2.5676e-01` | `8.7714` | `8.9474e-01` | `2.5786e-02` | `1.4129e+00` |
| `Bp` | | `8.1447e-01` | **`1.1684e-01`** | `4.8149e-01` | **`3.4894e-02`** | `1.3423e-01` | `9.0959` | `7.9046e-01` | `5.2151e-01` | `9.7173e-01` |
| `Bc` | | `1.0000e+00` | **`1.4255e-01`** | `5.8511e-01` | **`4.2479e-02`** | `1.5791e-01` | `9.0244` | `7.8978e-01` | `5.2366e-01` | `9.6990e-01` |

## (d) IL CONTROFATTUALE

**divisioni: `Ap` = `1219`, `Bp` = `18`, `Bc` = `70`.** `Bc/Bp` = `3.888889`, `Bc/Ap` = `0.057424`.

Il fattore `1/mediana(r)` applicato: da `1.000000` a `1.254784`, mediano `1.233014`.

> ### ⚠ **<<GRADIENTI INTATTI>> NON E' LETTERALMENTE VERO:** il riscalamento moltiplica **anche** `|r_i - r_j|` per lo stesso fattore, quindi il gradiente di `Bc` e' **maggiorato**. ### ✔ **L'errore va nella direzione GIUSTA** -- un gradiente maggiorato **abbassa** la soglia, cioe' spinge le nascite **verso l'alto**.
>
> ### ✔ **E C'E' UN'INFERENZA, che scrivo COME inferenza:** togliere il rallentamento uniforme dovrebbe dare **al massimo `x1.233`** sugli eventi attesi *(entra una volta sola, in `(b)`)*. Le divisioni fanno ### **`x3.89`**. ### **Quindi la parte del leone NON viene dal rallentamento: viene dall'altro effetto del riscalamento, cioe' DAL GRADIENTE.** ### ⛔ **E' un'inferenza su DUE punti, non una misura:** con un solo valore del fattore non si separa una dipendenza lineare da una ripida.

### ⚠ **LETTURA: INTERMEDIA** -- le nascite risalgono *(`x3.89`)* ma **non** tornano a `Ap` *(restano a `5.7 %` di `Ap`)*. ### **Il controfattuale NON separa le due cause**, e il gradiente maggiorato e' una **causa confondente dichiarata**. ### **Era la lettura prevista dal criterio fissato PRIMA.**

## I CONTROLLI

| | braccio | che cosa | esito |
|---|---|---|---|
| **`C1`** | `Ap` | `1219` divisioni + `307` schwinger = `1526` contro `nati = 1526` | **COINCIDE** |
| | `Ap` | e `n_fin - n_0 = 1526` | uguale a `nati`: **nessun nodo muore** |
| **`C1`** | `Bp` | `18` divisioni + `7` schwinger = `25` contro `nati = 25` | **COINCIDE** |
| | `Bp` | e `n_fin - n_0 = 25` | uguale a `nati`: **nessun nodo muore** |
| **`C1`** | `Bc` | `70` divisioni + `19` schwinger = `89` contro `nati = 89` | **COINCIDE** |
| | `Bc` | e `n_fin - n_0 = 89` | uguale a `nati`: **nessun nodo muore** |
| **`C2`** | `Ap` | candidati: `1508` | ok |
| **`C2`** | `Bp` | candidati: `27` | ok |
| **`C2`** | `Bc` | candidati: `83` | ok |
| **`C3`** | | `n` di `Ap`: `14328` contro il **sigillo committato** `14328` | **COINCIDE** |
| **`C3`** | | archi di `Ap`: `473397` contro il **sigillo committato** `473397` | **COINCIDE** |
| **`C3`** | | `n` di `Bp`: `12827` contro il **sigillo committato** `12827` | **COINCIDE** |
| **`C3`** | | archi di `Bp`: `471596` contro il **sigillo committato** `471596` | **COINCIDE** |

> ### ✔ **`C3` E' UN CONFRONTO FRA DUE CORSE DIVERSE**, quindi piu' forte di un auto-confronto: se i ganci cambiassero la fisica, questi numeri non coinciderebbero.

## IL VERDETTO

> ### **I CONTROLLI CHE FERMANO (`C1`, `C3`) PASSANO.**
>
> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO: non c'e' niente da promuovere.** ### **Il peso `0.3` della modulazione e se le nascite della `PARTE A` fossero un artefatto sono DECISIONI DI LUCA.**

## CHE COSA RESTA APERTO

1. ### **IL PESO `0.3` della modulazione** -- un numero **scelto**, che `A1` condanna, e che questa misura ### **NON cambia**: e' una decisione di Luca *(`MITOSI-SOGLIA-GRAD`)*;
2. ### **SE LE NASCITE DELLA `PARTE A` FOSSERO UN ARTEFATTO** -- questa misura dice **dove** sta il fattore, **non** se la crescita di prima fosse fisica. ### **Decisione di Luca.**
3. **`ARCHI-OLTRE-4PI`** *(voce nuova, non indagata)*: i ~`109` archi che sono **oltre il tetto `4pi` dal passo `2`** e ### **non rilassano**;
4. **la MISURA CON `DT` DIMEZZATO**, decisa da Luca: ### **NON si avvia finche' Luca non lo dice**;
5. **`GRAVITA-POTENZIALE`**: due potenziali nel codice e Poisson come **vincolo di scala**, oggi inerte *(`SCALA_B = 1.0`)*;
6. ### **LA DOMANDA DI `A14`:** se la crescita era alimentata dal gradiente dell'orologio, ### **quella massa da dove veniva?** Nominata, non risolta.

---

*Referto **generato** da `csv/_test_fork/_referto_crescita.py` dal `crescita.json` della corsa: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`). Le **quattro verifiche del guardiano** sono **ricalcolate qui sui dati di questa corsa**.*
