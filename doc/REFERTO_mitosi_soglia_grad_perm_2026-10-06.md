# REFERTO -- `MITOSI-SOGLIA-GRAD`: **i morsi RIMESCOLATI**

*(Mandato di Luca del 2026-10-06. Previsioni, `P1`/`P2`/`P3`, i tre semi e i quattro controlli sono fissati in `doc/TASK_HISTORY/2026-10-06_mitosi-soglia-grad-permutato.md`, committato **prima** in `70b89c5` e annotato in `f922c20`.)*

| | |
|---|---|
| **simulatore** | `f7237563`, ### **NON toccato** |
| **strumento** | `b399adb2` |
| **semi della permutazione** | `101`, `202`, `303`, ### **fissati PRIMA** |
| **piattaforma** | Windows 11, python `3.13.2`, numpy `2.3.0` |
| **passi** | `150`, seme `11` |
| **`Bp`** | dal `soglia.json` **committato** *(`dd86933`)*: `18` divisioni, `7738` nella finestra |

## IL RISULTATO: **le nascite NON crollano. SALGONO.**

| braccio | divisioni | `Σg1∧g2∧g3` | div/`Bp` | finestra/`Bp` |
|---|--:|--:|--:|--:|
| `Bperm-s1` | **`27`** | `8722` | `1.5000` | `1.1272` |
| `Bperm-s2` | **`28`** | `8301` | `1.5556` | `1.0728` |
| `Bperm-s3` | **`30`** | `8534` | `1.6667` | `1.1029` |
| `Bperm-id` *(permutazione **IDENTICA**)* | `18` | `7738` | `1.0000` | `1.0000` |
| `Bp` *(riferimento)* | `18` | `7738` | `1.0000` | `1.0000` |

**MEDIA sui `3` semi:** divisioni `28.33` *(dispersione `1.25`)*, `Σg1∧g2∧g3` `8519.0` *(dispersione `172.2`)*.

### **RAPPORTI SULLA MEDIA: divisioni `1.5741` · finestra `1.1009`**

## `P1` / `P2` / `P3`, applicati **ALLA MEDIA**

| criterio su | rapporto | lettura |
|---|--:|---|
| **divisioni** *(`18` eventi)* | `1.5741` | ### **`P1`** -- il LEGAME col gradiente **NON** e' portante: il `0.3` agisce come **abbassamento** della soglia |
| **finestra** *(`7738` passi-arco)* | `1.1009` | ### **`P1`** -- il LEGAME col gradiente **NON** e' portante: il `0.3` agisce come **abbassamento** della soglia |

> ### ✔ **I TRE SEMI CADONO NELLA STESSA LETTURA**, su entrambi i criteri: `P1`. ### **Non c'e' nessuna incertezza da dichiarare fra i semi**, e la dispersione e' piccola *(`1.25` su `28.33` nelle divisioni, cioe' il `4.4 %`)*.

> ### ✔ **E I DUE CRITERI CONCORDANO**, nonostante `3` ordini di grandezza di statistica fra l'uno e l'altro *(`18` eventi contro `7738` passi-arco)*: ### **la lettura non dipende da quale dei due si guarda.**

## LE DUE PREVISIONI, scritte **PRIMA** *(`70b89c5`)*

| chi | la previsione | esito |
|---|---|---|
| **il guardiano** | divisioni fra `0.5x` e `2x` di `Bp` *(fra `9` e `36`)* | ### **CONFERMATA** |
| **io** | le nascite **CROLLANO** *(il legame e' portante)* | ### ⛔ **REFUTATA** |

> ### ⛔ **LA MIA PREVISIONE E' SBAGLIATA, e lo scrivo per primo.** Mi aspettavo un crollo e le divisioni ### **SALGONO** a `1.5741` di `Bp`. ### **Il ragionamento che mi aveva portato li' era quello che avevo DICHIARATO come bucato:** poggiava sul `q05` della soglia a `6.9900`, ### **che il referto `12e2ca7` aveva stabilito essere un effetto di SELEZIONE** -- e da un effetto di selezione **non si deduce la causalita'**. ### **Avevo scritto che era un'aspettativa e non una deduzione: era un'aspettativa SBAGLIATA.**

## COME SI LEGGE — e la regola era **fissata PRIMA** *(`f922c20`)*

### ⛔ **L'EFFETTO LOTTERIA**: `_PRNG.permutation` e' chiamata **a ogni passo**, quindi la soglia di ogni arco e' **ripescata** `150` volte. In `Bp` la soglia di un arco e' **PERSISTENTE** *(il gradiente di `r` varia lentamente)*. ### **La probabilita' che un arco non veda MAI un morso del decile alto in `150` estrazioni e' `0.9^150` = `1.37e-07`:** praticamente **ogni** arco riceve almeno una volta una soglia fra le piu' basse.

> ### ⛔ **QUINDI IL RISULTATO E' AMBIGUO, e la regola lo diceva PRIMA:** vale `P1`, e fra le due spiegazioni ### **<<non conta QUALE arco>>** e ### **<<LOTTERIA>>** ### **questo braccio non distingue.**
>
> ### ✔ **E L'AMBIGUITA' NON E' SIMMETRICA:** le nascite non sono rimaste, sono ### **SALITE** *(`1.5741`)*, e ### **la lotteria spinge ESATTAMENTE in quella direzione.** Quindi la salita e' **compatibile** con la lotteria, e ### **l'ipotesi <<non conta quale arco>> non e' l'unica lettura.**
>
> ### ➜ **IL PASSO SUCCESSIVO E' FISSATO:** il braccio **`Bperm-fisso`** *(permutazione ripescata **solo quando `len(avv)` cambia**, stessi tre semi, stessi controlli, stessi criteri)*. ### **Nel `Bp` committato `len(avv)` cambia `12` volte su `150`, quindi `Bperm-fisso` ripeschera' `13` volte invece di `150`** -- un fattore `11.5` di lotterie in meno, e `p(mai il decile alto)` da `1.37e-07` a `0.254`.
>
> ### ⚠ **MA `Bperm-fisso` NON E' <<`Bperm` SENZA IL DIFETTO>>:** ripescare solo alla crescita ### **lega la permutazione alla TOPOLOGIA** *(i morsi cambiano **quando** nasce un nodo)*. ### **Riduce la lotteria, non la toglie, e cambia una cosa per un'altra. Nessuno dei due e' il braccio <<pulito>>.**

### ✔ **E LA LETTURA VA DETTA NELLA FORMA GIUSTA**, come il task history pretende

`Bperm` distrugge il legame **arco-gradiente** ma ### **conserva la distribuzione dei morsi NEL TEMPO**: un passo con morsi grandi resta un passo con morsi grandi. ### ⛔ **Quindi <<`P1`>> si legge <<NON CONTA QUALE ARCO>>, NON <<IL GRADIENTE NON CONTA>>:** il gradiente decide ancora **quanti** morsi grandi ci sono a ogni passo.

## I QUATTRO CONTROLLI

| | | esito |
|---|---|---|
| **`C-perm-0`** *(deve passare)* | `Bperm-id` con la permutazione **IDENTICA**: divisioni `18`/`18`, finestra `7738`/`7738`, `n` `12827`/`12827` | **PASSA** |
| **`C-distr`** *(deve passare)* | `Bperm-s1`: il **multiinsieme dei morsi** prima/dopo identico su `150` passi su `150` | **PASSA** |
| **`C-distr`** *(deve passare)* | `Bperm-s2`: il **multiinsieme dei morsi** prima/dopo identico su `150` passi su `150` | **PASSA** |
| **`C-distr`** *(deve passare)* | `Bperm-s3`: il **multiinsieme dei morsi** prima/dopo identico su `150` passi su `150` | **PASSA** |
| **`C-distr`** *(deve passare)* | `Bperm-id`: il **multiinsieme dei morsi** prima/dopo identico su `150` passi su `150` | **PASSA** |
| **`C1`** | `Bperm-s1`: `27` + `16` = `43` contro `nati = 43` | **COINCIDE** |
| **`C1`** | `Bperm-s2`: `28` + `8` = `36` contro `nati = 36` | **COINCIDE** |
| **`C1`** | `Bperm-s3`: `30` + `14` = `44` contro `nati = 44` | **COINCIDE** |
| **`C1`** | `Bperm-id`: `18` + `7` = `25` contro `nati = 25` | **COINCIDE** |

> ### ✔ **`C-perm-0` E' LA PROVA CHE LA PATCH E' PULITA:** la permutazione identica e' un **no-op aritmetico** *(`b[arange(len(b))]` **e'** `b`)*, e il braccio riproduce `Bp` ### **esattamente** -- divisioni, finestra e `n` finale.
>
> ### ✔ **E `C-distr` E' ESATTO, non statistico:** per ogni passo si confronta il **multiinsieme** dei morsi prima e dopo la permutazione con `array_equal` sugli ordinati. ### **`150` passi su `150`, su tutti i bracci.**
>
> ### ⚠ **E UN PEZZO DI `C-distr` E' <<n/d>>, come avevo PREVISTO nel commit dello strumento** *(`472b0e6`, <<cosa ricontrollare>> punto `2`)*: il confronto dell'**impronta delle soglie contro `Bp`** non si puo' fare, perche' `Bp` *(`dd86933`)* e' stato prodotto da uno strumento che ### **non registrava l'impronta.** ### **La prova che conta resta il multiinsieme prima/dopo, che si calcola DENTRO la corsa.**

**`C-rng`** -- il primo passo in cui `len(avv)` differisce da `Bp`: `Bperm-s1`: 79, `Bperm-s2`: 83, `Bperm-s3`: 84, `Bperm-id`: **nessuno**.

> ### ✔ **E `Bperm-id` non diverge MAI**, che e' l'altra faccia di `C-perm-0`. I tre semi divergono quando la topologia si separa, e ### **il passo in cui succede E' il numero qui sopra** -- `C-rng` non dice <<stesso dado per sempre>>, dice <<stesso dado finche' la topologia e' la stessa>>.

## IL VERDETTO

> ### **I QUATTRO CONTROLLI PASSANO.**
>
> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** che fare del `0.3` -- tenerlo, derivarlo su `|r_i*phivel_i - r_j*phivel_j|`, o ripensare la soglia `3π` -- ### **e' UNA DECISIONE DI LUCA.**

## CHE COSA QUESTA MISURA AGGIUNGE, in una riga

Il referto `0af53a5` aveva mostrato che il `0.3` e' **PORTANTE** *(senza di lui `2` divisioni)*. ### **Questo mostra che NON porta per DOVE mette il morso:** rimescolando i morsi fra gli archi le nascite ### **non calano, salgono** *(`1.5741`)*. ### ⛔ **Ma fra <<non conta quale arco>> e <<lotteria>> questo braccio non distingue**, e `Bperm-fisso` e' il passo successivo.

---

*Referto **generato** da `csv/_test_fork/_referto_perm.py` dal `soglia_perm.json`: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`).*
