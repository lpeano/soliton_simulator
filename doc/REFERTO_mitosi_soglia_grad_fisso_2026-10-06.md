# REFERTO -- `MITOSI-SOGLIA-GRAD`: **`Bperm` e `Bperm-fisso`, i DUE bracci**

*(Mandato: l'annotazione `f922c20`, che ha fissato `Bperm-fisso` ### **prima di vedere i numeri di `Bperm`**. Previsioni, criteri e tavola della lotteria in `doc/TASK_HISTORY/2026-10-06_bperm-fisso.md` *(`1bf6fe2`)*, con le ### **bande corrette** in `0b8999c`.)*

| | |
|---|---|
| **simulatore** | `f7237563`, ### **NON toccato** |
| **strumento** | `43cf63c8` *(`Bperm-fisso`)* · `b399adb2` *(`Bperm`)* |
| **semi** | `101`, `202`, `303`, ### **gli STESSI dei due bracci** |
| **piattaforma** | Windows 11, python `3.13.2`, numpy `2.3.0` |
| **`Bp`** | dal `crescita.json` **committato** *(`dd86933`)*: `18` divisioni, `7738` nella finestra |

## ⛔ LA PRIMA COSA: **lo strumento ha stampato BANDE SBAGLIATE, e questo referto no**

Lo strumento `43cf63c8` calcola la banda come `1/sqrt(N)`. ### **E' sbagliata in due modi** *(correzione del guardiano, `0b8999c`, fissata **prima** della corsa)*:

| | la banda dello strumento | perche' e' sbagliata | ### **quella che VALE** |
|---|--:|---|--:|
| **divisioni** | `± 0.2357` | e' ### **`1 sigma`**: anche con la previsione **giusta** un conteggio cade fuori il `~31.7 %` delle volte, cioe' ### **una volta su tre** | `± 0.4714` ⟹ **`[0.5286, 1.4714]`** |
| **finestra** | `± 0.0114` | tratta ogni **passo-arco** come indipendente, e ### **non lo e': lo stesso arco resta nella finestra per molti passi** | `± 0.0233` ⟹ **`[0.9767, 1.0233]`** |

### ✔ **E IL RUMORE DELLA FINESTRA NON E' STIMATO: E' MISURATO in `Bperm`** -- i tre semi danno `8722`, `8301`, `8534`, media `8519.0`, dispersione `172.1995` = ### **`2.0214 %`**, errore della media `1.1670 %`, e `2x` da' la banda qui sopra.

> ### ⚠ **E NEL CONTO DEL GUARDIANO C'E' UN ERRORE, che il mandato chiedeva di dire:** il `2.0214 %` e' **`pstdev`**, la deviazione standard di **POPOLAZIONE** *(divide per `N`)* -- quella che lo strumento stampa. ### **Per STIMARE la dispersione da tre campioni l'estimatore non distorto e' quello di CAMPIONE**, e vale `sqrt(3/2)` = `1.2247` volte tanto: `2.4756 %` ⟹ banda **`[0.9714, 1.0286]`**.
>
> ### 📌 **VALE LA BANDA DEL GUARDIANO**, perche' e' lui che l'ha fissata e la sua formula dice *«la dispersione misurata»*. ### **L'altra e' RIPORTATA, non applicata**, e se un risultato cadesse **fra le due** il referto lo direbbe invece di scegliere.
>
> ### ⛔ **E UN LIMITE PIU' GRANDE DI ENTRAMBE: `2x` l'errore della media e' una regola a `2 sigma`, e con TRE semi ci sono DUE gradi di liberta'.** L'`IC95` vero vuole `t(0.025, 2)` = `4.3027`, non `2`: la banda sarebbe `± 5.0214 %` ⟹ `[0.9498, 1.0502]`. ### **Una banda a `2 sigma` su tre semi e' OTTIMISTICA di un fattore `2.15`, e `P3` chiede ALMENO QUATTRO SEMI. La cura e' un quarto seme, non una banda piu' larga.**

## I DUE BRACCI

| braccio | divisioni | `Σg1∧g2∧g3` | div/`Bp` | finestra/`Bp` | lotterie |
|---|--:|--:|--:|--:|--:|
| `Bperm-s1` | **`27`** | `8722` | `1.5000` | `1.1272` | `150` *(a ogni passo)* |
| `Bperm-s2` | **`28`** | `8301` | `1.5556` | `1.0728` | `150` *(a ogni passo)* |
| `Bperm-s3` | **`30`** | `8534` | `1.6667` | `1.1029` | `150` *(a ogni passo)* |
| `Bperm-id` *(permutazione **IDENTICA**)* | `18` | `7738` | `1.0000` | `1.0000` | -- |
| `Bpf-s1` | **`26`** | `8664` | `1.4444` | `1.1197` | `20` |
| `Bpf-s2` | **`33`** | `8477` | `1.8333` | `1.0955` | `26` |
| `Bpf-s3` | **`22`** | `8755` | `1.2222` | `1.1314` | `16` |
| `Bpf-id` *(permutazione **IDENTICA**)* | `18` | `7738` | `1.0000` | `1.0000` | -- |
| `Bp` *(riferimento)* | `18` | `7738` | `1.0000` | `1.0000` | -- |

| | `Bperm` | `Bperm-fisso` |
|---|--:|--:|
| media divisioni | `28.33` | `27.00` |
| dispersione *(`pstdev`)* | `1.2472` *(`4.40 %`)* | `4.5461` *(`16.84 %`)* |
| media finestra | `8519.0` | `8632.0` |
| dispersione *(`pstdev`)* | `172.1995` *(`2.02 %`)* | `115.7267` *(`1.34 %`)* |
| ### **rapporto divisioni** | ### **`1.5741`** | ### **`1.5000`** |
| ### **rapporto finestra** | ### **`1.1009`** | ### **`1.1155`** |

> ### ⚠ **E LA DISPERSIONE FRA SEMI DI `Bperm-fisso` E' PIU' CHE DOPPIA di quella di `Bperm`** *(`16.84 %` contro `4.40 %`)*. ### **L'avevo scritto come cosa che non sapevo** *(`1bf6fe2`, punto `2`)*: con **una** permutazione per corsa invece di `150` ### **non c'e' niente che medi**, e un seme sfortunato pesa. ### ⛔ **Con tre semi e questa dispersione la media e' FRAGILE, e `P3` chiede almeno quattro semi.**

## `P1` / `P2` / `P3`, applicati **ALLA MEDIA** di ciascun braccio

| braccio | su | rapporto | lettura |
|---|---|--:|---|
| `Bperm` | **divisioni** | `1.5741` | ### **`P1`** -- il LEGAME col gradiente **NON** e' portante |
| `Bperm` | **finestra** | `1.1009` | ### **`P1`** -- il LEGAME col gradiente **NON** e' portante |
| `Bperm-fisso` | **divisioni** | `1.5000` | ### **`P1`** -- il LEGAME col gradiente **NON** e' portante |
| `Bperm-fisso` | **finestra** | `1.1155` | ### **`P1`** -- il LEGAME col gradiente **NON** e' portante |

- `Bperm`: ### ✔ **i tre semi cadono nella STESSA lettura** su entrambi i criteri *(`P1`)*.
- `Bperm-fisso`: ### ✔ **i tre semi cadono nella STESSA lettura** su entrambi i criteri *(`P1`)*.

## ⛔ LA TAVOLA DELLA LOTTERIA, **fissata PRIMA dei numeri** *(`1bf6fe2`)*

| su | `fisso` | `perm` | banda | ### **lettura** |
|---|--:|--:|--:|---|
| **divisioni** | `1.5000` | `1.5741` | `[0.5286, 1.4714]` | ### **`L-B`** -- **LA LOTTERIA NON C'ENTRA** |
| **finestra** | `1.1155` | `1.1009` | `[0.9767, 1.0233]` | ### **`L-B`** -- **LA LOTTERIA NON C'ENTRA** |

- **divisioni** ⟹ `L-B`: la salita viene dalla **permutazione in se'**, e ### **va capita: nessuna delle due spiegazioni basta**.
- **finestra** ⟹ `L-B`: la salita viene dalla **permutazione in se'**, e ### **va capita: nessuna delle due spiegazioni basta**.

> ### ✔ **LE DUE METRICHE CONCORDANO**, nonostante `3` ordini di grandezza di statistica fra l'una e l'altra.

### LA REGOLA DELL'ERRORE COMBINATO *(fissata in `0b8999c`)*

`|media_fisso - media_perm| > 2*sqrt(se_fisso^2 + se_perm^2)`, con ogni `se` = dispersione fra i suoi tre semi `/sqrt(3)` *(estimatore di **campione**)*:

| | valore |
|---|--:|
| `se` di `Bperm-fisso` *(finestra)* | `0.9480 %` |
| `se` di `Bperm` *(finestra)* | `1.4293 %` |
| errore **combinato** | `1.7151 %` · `2x` = **`3.4302 %`** |
| differenza fra le due medie | **`1.3264 %`** *(`8632.0` contro `8519.0`)* |

> ### ⛔ **LE DUE FINESTRE NON SONO DISTINGUIBILI:** `1.3264 %` **non supera** `3.4302 %`. ### **Togliere la lotteria non sposta la finestra in modo misurabile**, e questo e' un risultato, non un'assenza di risultato.

## LE PREVISIONI

| chi | la previsione | esito |
|---|---|---|
| **io** *(`1bf6fe2`)* | `Bperm-fisso` **torna verso `Bp`**: rapporto delle divisioni dentro la banda | ### **⛔ REFUTATA** |
| **io**, sulla dispersione | *«con una permutazione sola i tre semi potrebbero separarsi MOLTO di piu'»* | `16.84 %` contro `4.40 %` di `Bperm`: ### **si separano** |

> ### ⛔ **LA MIA PREVISIONE E' SBAGLIATA DI NUOVO, e lo scrivo per primo: due su due.** Il rapporto e' `1.5000`, fuori da `[0.5286, 1.4714]` di `0.0286` *(il `2.86 %`)*.
>
> ### ⚠ **E NON MI APPIGLIO AL MARGINE:** e' fuori di poco, ma con la ### **dispersione MISURATA** fra i tre semi *(`16.84 %`, errore della media `9.72 %`)* l'intervallo a `2 sigma` del rapporto e' **`[1.2084, 1.7916]`**, che ### **ESCLUDE `1.0`**. ### **La previsione e' sbagliata per il MERITO, non per un pelo di banda.**

## I CONTROLLI

| | | esito |
|---|---|---|
| **`C-perm-0`** *(deve passare)* | `Bpf-id`: divisioni `18`/`18`, finestra `7738`/`7738`, `n` `12827`/`12827` | **PASSA** |
| **`C-distr`** | `Bpf-s1`: multiinsieme dei morsi identico su `150`/`150` passi | **PASSA** |
| **`C-distr`** | `Bpf-s2`: multiinsieme dei morsi identico su `150`/`150` passi | **PASSA** |
| **`C-distr`** | `Bpf-s3`: multiinsieme dei morsi identico su `150`/`150` passi | **PASSA** |
| **`C-distr`** | `Bpf-id`: multiinsieme dei morsi identico su `150`/`150` passi | **PASSA** |
| **`C1`** | `Bpf-s1`: `26` + `9` = `35` contro `nati = 35` | **COINCIDE** |
| **`C1`** | `Bpf-s2`: `33` + `13` = `46` contro `nati = 46` | **COINCIDE** |
| **`C1`** | `Bpf-s3`: `22` + `9` = `31` contro `nati = 31` | **COINCIDE** |
| **`C1`** | `Bpf-id`: `18` + `7` = `25` contro `nati = 25` | **COINCIDE** |
| **`C-ident`** *(riporta, non ferma)* | `Bpf-s1`: coppie a lunghezza **uguale** `130`, di cui con **nascite al passo prima** `0`, archi **diversi** `0` | **### POTERE NULLO: nessun caso pericoloso** |
| **`C-ident`** *(riporta, non ferma)* | `Bpf-s2`: coppie a lunghezza **uguale** `124`, di cui con **nascite al passo prima** `0`, archi **diversi** `0` | **### POTERE NULLO: nessun caso pericoloso** |
| **`C-ident`** *(riporta, non ferma)* | `Bpf-s3`: coppie a lunghezza **uguale** `134`, di cui con **nascite al passo prima** `0`, archi **diversi** `0` | **### POTERE NULLO: nessun caso pericoloso** |
| **`C-ident`** *(riporta, non ferma)* | `Bpf-id`: coppie a lunghezza **uguale** `137`, di cui con **nascite al passo prima** `0`, archi **diversi** `0` | **### POTERE NULLO: nessun caso pericoloso** |
| **`C-lotterie`** | `Bpf-s1`: estratte `20`, cambi di `len(avv)` `19`, atteso `20` | **COINCIDE** |
| **`C-lotterie`** | `Bpf-s2`: estratte `26`, cambi di `len(avv)` `25`, atteso `26` | **COINCIDE** |
| **`C-lotterie`** | `Bpf-s3`: estratte `16`, cambi di `len(avv)` `15`, atteso `16` | **COINCIDE** |

> ### ✔ **E `C-lotterie` E' LA PROVA CHE IL BRACCIO FA CIO' CHE DICE:** la permutazione si ripesca ### **solo quando `len(avv)` cambia**, e il conteggio lo verifica contro i cambi veri invece di fidarsi del codice.

> ### ⛔ **MA `C-ident` HA POTERE NULLO SU QUESTA CORSA, e la domanda che doveva chiudere RESTA APERTA.** I casi pericolosi sono ### **ZERO su tutti e quattro i bracci**: in ogni coppia a lunghezza uguale ### **non era nato nessuno al passo prima**, quindi l'insieme degli archi era identico ### **per costruzione** e l'impronta non poteva differire.
>
> ### ⛔ **QUINDI LA FRASE <<ora e' MISURATO invece che sperato>> ERA SBAGLIATA, e la correggo:** le `525` coppie guardate non sono `525` prove -- sono `525` casi in cui non c'era niente da vedere. ### **Il rischio che un passo tolga `k` archi e ne aggiunga `k` NON e' escluso da questa corsa: e' solo non capitato.**
>
> ### ✔ **E L'IMPRONTA E' SENSIBILE, questo si':** due insiemi che differiscono per **un** arco danno `sha1` diversi. ### **Il controllo e' VALIDO e il suo POTERE e' nullo: sono due cose diverse, e prima le avevo confuse.**

## ⚠ IL LIMITE, **dichiarato PRIMA dei numeri** *(`f922c20`)*

> ### ⛔ **`Bperm-fisso` NON E' <<`Bperm` SENZA IL DIFETTO>>.** Ripescare solo alla crescita ### **lega la permutazione alla TOPOLOGIA** *(i morsi cambiano **quando** nasce un nodo)*. ### **Riduce la lotteria, non la toglie, e cambia una cosa per un'altra. NESSUNO DEI DUE E' IL BRACCIO <<PULITO>>.**
>
> ### ✔ **E C'E' UN FATTO CHE LO RENDE MENO GRAVE DI QUANTO SEMBRI:** nel `Bp` committato `len(avv)` cambia `12` volte su `150`, e la **prima** e' ### **AL passo `100`** -- quindi per i primi ### **99** passi la permutazione e' ### **UNA SOLA**, e il legame con la topologia non ha ancora modo di agire. ### ⚠ **E <<tutte DOPO il passo 100>> era sbagliato: il primo cambio e' *AL* passo 100** *(rilievo del guardiano)*.

## IL VERDETTO

> ### **I CONTROLLI PASSANO su entrambi i bracci.**
>
> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** che fare del `0.3` -- tenerlo, derivarlo su `|r_i*phivel_i - r_j*phivel_j|`, o ripensare la soglia `3π` -- ### **e' UNA DECISIONE DI LUCA.**

## CHE COSA QUESTA MISURA AGGIUNGE, e che cosa LASCIA APERTO

| | |
|---|---|
| `0af53a5` aveva mostrato | il `0.3` e' ### **PORTANTE**: senza di lui `2` divisioni invece di `18` |
| `d97317a` aveva mostrato | la modulazione ### **legge la grandezza sbagliata** *(Spearman `~0.04` col gradiente nudo, `~0.86` con `|r_i*w_i - r_j*w_j|`)* |
| `d97ac64` *(`Bperm`)* aveva mostrato | rimescolando i morsi le nascite ### **non calano, SALGONO** -- e la lettura era **AMBIGUA** fra *«non conta quale arco»* e *«lotteria»* |
| ### **questo mostra** | ### ⛔ **NON ERA LA LOTTERIA.** Con `20`/`26`/`16` estrazioni invece di `150` il risultato ### **non si muove** |

> ### ⛔ **E L'AMBIGUITA' SI CHIUDE DA UN LATO SOLO.** Cade la *«lotteria»*; ### **ma non resta <<non conta quale arco>>**, perche' se non contasse il rapporto sarebbe `1`, ### **e invece e' `1.5000`.** Permutare i morsi ### **FA SALIRE** le nascite, e questo e' un fatto che nessuna delle due spiegazioni copriva.

### ⚠ **L'IPOTESI PER LA PROSSIMA MISURA -- e' UN'IPOTESI, non un risultato**

Se randomizzare **aiuta**, allora l'assegnazione vera mette le soglie basse sugli archi ### **che servono meno**: il legame col gradiente non sarebbe soltanto **non informativo** ma ### **ANTI-informativo**. ### ✔ **Sarebbe coerente con `d97317a`** *(la modulazione legge `|r_i - r_j|`, che correla `~0.04` con la spinta, mentre la forma esatta correla `~0.86`)*: una grandezza quasi scorrelata ### **puo' essere leggermente anti-correlata**, e `11.55 %` di finestra in piu' e' esattamente l'ordine di grandezza che ci si aspetterebbe.

> ### ⛔ **NON LA MISURO QUI, E NON LA DICHIARO DIMOSTRATA.** La misura che la deciderebbe e' la **correlazione fra il morso e la DISTANZA DALLA SOGLIA** -- e ### **che fare del `0.3` resta UNA DECISIONE DI LUCA.**

---

*Referto **generato** da `csv/_test_fork/_referto_fisso.py` dai `json` di **tre** corse -- `crescita.json` *(`dd86933`)*, `soglia_perm.json` *(`e32b9e7`)* e `soglia_fisso.json` -- e ### **ogni numero dice da quale viene** (`L-NUMERI`).*
