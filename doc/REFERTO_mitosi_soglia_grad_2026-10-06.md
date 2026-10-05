# REFERTO -- `MITOSI-SOGLIA-GRAD` **a ampiezza zero**: il `0.3` serve o no?

*(Mandato di Luca del 2026-10-05. Previsioni, `K1`/`K2`/`K2b` e i cinque controlli fissati in `doc/TASK_HISTORY/2026-10-05_mitosi-soglia-grad-ampiezza-zero.md`, committato **prima** in `bb1fece`, annotato in `1362672` e `99782e1`.)*

| | |
|---|---|
| **simulatore** | `f7237563`, ### **NON toccato** *(la patch e' su copie)* |
| **braccio `A`** | `062172d3`, dal tag `pre-z43-cura2-r-da-cs` |
| **strumento** | `6b26f173` |
| **piattaforma** | Windows 11, python `3.13.2`, numpy `2.3.0`, `AMD64` |
| **passi** | `150`, seme `11`, scena del driver |
| **configurazione dichiarata INTERA** | `True` *(braccio `Bg`)* |
| **predittore della misura `(2)`** | ### **CAUSALE** *(letto al passo `t-1`)* |

## IL RISULTATO: **togliere il `0.3` ANNIENTA le nascite, in ENTRAMBI i bracci**

| braccio | divisioni | Schwinger | `nati` | `n` finale |
|---|--:|--:|--:|--:|
| `Ap0` | **`2`** | `0` | `2` | `12804` |
| `Bp0` | **`2`** | `1` | `3` | `12805` |
| `B03` | **`18`** | `7` | `25` | `12827` |
| `Bg` | **`18`** | `7` | `25` | `12827` |
| `Ap` *(riferimento, `12e2ca7`)* | `1219` | `307` | `1526` | `14328` |
| `Bp` *(riferimento, `12e2ca7`)* | `18` | `7` | `25` | `12827` |

### **`Ap0/Ap` = `0.001641`  ·  `Bp0/Bp` = `0.111111`**

> ### ✔ **E IL FATTO PIU' NETTO DI TUTTA LA MISURA: SENZA LA MODULAZIONE I DUE BRACCI DANNO LO STESSO NUMERO DI DIVISIONI** — `2` e `2`. ### **Le due leggi del tempo proprio, private del `0.3`, producono la STESSA mitosi.**
>
> ### ⛔ **Quindi il fattore `67.7` fra `Ap` e `Bp` del referto `12e2ca7` passava TUTTO per la MODULAZIONE.** Non per `_ft`, non per la scarica: ### **per il `0.3`.**
>
> ### ⚠ **E VA DETTO CHE COSA QUESTO *NON* DIMOSTRA:** che la modulazione sia *giusta*. Dimostra che e' ### **PORTANTE** — che senza di lei la mitosi quasi non accade, in nessuna delle due leggi del tempo. ### **<<Portante>> e <<corretta>> sono due cose diverse, e la seconda non la decide una misura di conteggi.**

## `K1` — **l'ipotesi NON e' refutata**, e di molto

| | |
|---|---|
| `Ap0/Ap` | **`0.001641`** |
| soglia `K1` | `0.8` |
| esito | **### l'ipotesi NON e' refutata: togliere il `0.3` **ABBATTE** le nascite di `A`** |

**Togliere il `0.3` porta le divisioni di `A` da `1219` a `2`: un fattore `610`.**

### LE PREVISIONI DEL GUARDIANO, scritte **prima** *(`bb1fece`)*

| previsione | esito |
|---|---|
| `Ap0` perde la maggior parte: **`< 0.5x`** di `Ap` | ### **CONFERMATA** -- e **molto oltre**: `0.001641` |
| `Bp0` cambia poco: fra **`0.5x`** e **`1.0x`** di `Bp` | ### ⛔ **NON CONFERMATA**: `0.111111`, cioe' **sotto** la banda |

> ### ⛔ **E LA SECONDA PREVISIONE SBAGLIA PER LA RAGIONE CHE LA MOTIVAVA:** era *<<in `B` la modulazione morde solo il `5`-`10 per cento` sugli archi che passano>>*. ### **Il morso sulla SOGLIA e' davvero piccolo, ma l'effetto sulle NASCITE non lo e':** `0.111111`. ### **Un morso piccolo su una soglia non da' un effetto piccolo sulle nascite, se la popolazione sopra soglia e' ripida.**

## `K2` *(ESISTENZA)* e `K2b` *(ENTITA')* — la misura `(2)` sul braccio `Bg`

> ### ✔ **IL PREDITTORE E' CAUSALE**: `r` e `phivel` sono letti al passo **`t-1`**, cioe' quello che ha prodotto la `SPINTA` *(`:7772` legge la fotografia `_phi_t`)*. Le correlazioni vengono dalla corsa di **solo `Bg`** *(`--solo-bg`)*, e ### **`K1` e i cinque controlli restano della corsa a quattro bracci** -- il referto dice quale numero viene da quale corsa.

**Archi usati** *(quelli i cui due estremi esistevano al passo `t-1`)*: passo `50`: `471564`, passo `100`: `471563`, passo `140`: `471575`. ### ✔ **Gli archi NATI, esclusi e contati: `0`, `2`, `2`** -- su `~471` mila, quindi il predittore causale descrive **praticamente tutta** la popolazione.

### LE SPEARMAN — `3` predittori x `3` bersagli

| predittore | bersaglio | passo `50` | passo `100` | passo `140` |
|---|---|--:|--:|--:|
| `|r_i - r_j|`  *(il gradiente **nudo**: quello che la soglia legge)* | incremento **TOTALE** | `0.071002` | `0.045910` | `0.027752` |
| `|r_i - r_j|`  *(il gradiente **nudo**: quello che la soglia legge)* | ### **SPINTA** | `0.068427` | `0.033277` | `0.011997` |
| `|r_i - r_j|`  *(il gradiente **nudo**: quello che la soglia legge)* | **SCARICA** | `0.081700` | `0.042904` | `0.024617` |
| `|r_i - r_j| * |phivel|` medio  *(la **proxy** del mandato)* | incremento **TOTALE** | `0.351520` | `0.336760` | `0.288001` |
| `|r_i - r_j| * |phivel|` medio  *(la **proxy** del mandato)* | ### **SPINTA** | `0.402846` | `0.369878` | `0.318859` |
| `|r_i - r_j| * |phivel|` medio  *(la **proxy** del mandato)* | **SCARICA** | `0.339056` | `0.292211` | `0.261092` |
| `|r_i*phivel_i - r_j*phivel_j|`  *(la **forma esatta**: quella che il codice produce)* | incremento **TOTALE** | `0.732879` | `0.792027` | `0.754567` |
| `|r_i*phivel_i - r_j*phivel_j|`  *(la **forma esatta**: quella che il codice produce)* | ### **SPINTA** | `0.869942` | `0.915141` | `0.887105` |
| `|r_i*phivel_i - r_j*phivel_j|`  *(la **forma esatta**: quella che il codice produce)* | **SCARICA** | `0.687912` | `0.698127` | `0.699019` |

> ### ✔ **IL RISULTATO PIU' INFORMATIVO DELLA MISURA, e non e' `K2`:** la correlazione della `SPINTA` col ### **gradiente NUDO e' `0.012`-`0.068`**, con la **proxy** `0.319`-`0.403`, e con la ### **FORMA ESATTA `0.870`-`0.915`.**
>
> ### ⛔ **QUINDI LA MODULAZIONE LEGGE LA GRANDEZZA SBAGLIATA.** La torsione e' guidata da `|r_i*phivel_i - r_j*phivel_j|` *(`rho ~ 0.89`)*, e la soglia si modula su `|r_i - r_j|` *(`rho ~ 0.04`)*. ### **Sono la stessa cosa solo se `phivel` e' uniforme sull'arco, e NON lo e'.**
>
> ### ✔ **ED E' IL LIMITE CHE IL GUARDIANO AVEVA DICHIARATO**, qui con un numero: *<<lo sfasamento e' proporzionale anche a `phivel`; dove `phivel ~ 0` il gradiente non produce torsione>>*. ### **La forma esatta era una mia aggiunta alla proxy chiesta: senza di lei questo confronto non ci sarebbe.**

### IL CONFRONTO FRA I DUE ALLINEAMENTI del predittore

| predittore | versione | passo `50` | passo `100` | passo `140` |
|---|---|--:|--:|--:|
| `|r_i - r_j|`  *(il gradiente **nudo**: quello che la soglia legge)* | ### **CAUSALE** *(`t-1`)* | `0.068427` | `0.033277` | `0.011997` |
| `|r_i - r_j|`  *(il gradiente **nudo**: quello che la soglia legge)* | stesso passo *(`t`)* | `0.068092` | `0.032211` | `0.011504` |
| `|r_i - r_j| * |phivel|` medio  *(la **proxy** del mandato)* | ### **CAUSALE** *(`t-1`)* | `0.402846` | `0.369878` | `0.318859` |
| `|r_i - r_j| * |phivel|` medio  *(la **proxy** del mandato)* | stesso passo *(`t`)* | `0.390527` | `0.359655` | `0.311442` |
| `|r_i*phivel_i - r_j*phivel_j|`  *(la **forma esatta**: quella che il codice produce)* | ### **CAUSALE** *(`t-1`)* | `0.869942` | `0.915141` | `0.887105` |
| `|r_i*phivel_i - r_j*phivel_j|`  *(la **forma esatta**: quella che il codice produce)* | stesso passo *(`t`)* | `0.826367` | `0.884193` | `0.856539` |

> ### ✔ **LE DUE VERSIONI DANNO LO STESSO VERDETTO su `K2` e `K2b`:** il difetto era ### **innocuo in questo caso, ma restava un difetto.** ### ✔ **E l'allineamento causale RAFFORZA la forma esatta** *(da `~0.86` a `~0.89` di media)*, ### **che e' quello che si aspetta se e' davvero lei a guidare la torsione:** correlare col passo giusto non puo' che migliorare il predittore vero.

### `K2`: la `SPINTA` contro il **gradiente nudo** — il predittore che la soglia legge

`|rho|` ai tre passi: `0.068427`, `0.033277`, `0.011997`. Soglia `K2`: `<= 0.05` **a tutti e tre**.

### **`K2`: l'ipotesi **NON** e' refutata: la correlazione **ESISTE****

> ### ⚠ **E PASSA PER UN PELO, SU UN PASSO SOLO:** `1` dei tre passi supera la soglia *(`0.068427`)*, gli altri due stanno **sotto** *(`0.033277`, `0.011997`)*. ### **Un criterio <<a tutti e tre>> deciso da un passo e' fragile, e lo dico invece di presentarlo come netto.**

### `K2b`: gli incrementi mediani della `SPINTA` per **quintile del gradiente nudo**

| passo | `q1` | `q2` | `q3` | `q4` | `q5` | **`q5/q1`** |
|--:|--:|--:|--:|--:|--:|--:|
| `50` | `1.7490e-02` | `1.9037e-02` | `2.0101e-02` | `2.0775e-02` | `2.3177e-02` | **`1.3251`** |
| `100` | `2.4333e-02` | `2.4743e-02` | `2.5964e-02` | `2.6512e-02` | `2.7933e-02` | **`1.1480`** |
| `140` | `2.2729e-02` | `2.1582e-02` | `2.1838e-02` | `2.2687e-02` | `2.3911e-02` | **`1.0520`** |

**Il rapporto `q5/q1` e' `>= 2.0` in `0` passi su `3`.** Soglia `K2b`: **almeno due su tre**.

### **`K2b`: il doppio conteggio **NON** e' rilevante**

### LA LETTURA COMBINATA, **dalla tavola fissata PRIMA** *(`1362672`)*

> ### **`K2` passa, `K2b` NON passa → <<IL DOPPIO CONTEGGIO ESISTE MA E' PICCOLO>>**, e ### **la decisione sul `0.3` si legge da `K1` e dalle nascite di `Bp0`.**
>
> ### ✔ **E `K1` e `Bp0` dicono la stessa cosa, forte:** togliere il `0.3` porta le divisioni da `1219` a `2` in `A` e da `18` a `2` in `B`. ### **La modulazione non e' una ridondanza da togliere: e' PORTANTE.**

## I CINQUE CONTROLLI

| | | esito |
|---|---|---|
| **`C0`** *(deve passare)* | `B03` riproduce `Bp`: `n` `12827`/`12827`, archi `471596`/`471596`, divisioni `18`/`18` | **PASSA** |
| **`C0-tw`** *(deve passare)* | `Bg` riproduce `Bp`: `n` `12827`/`12827`, archi `471596`/`471596`, divisioni `18`/`18` | **PASSA** |
| **`C-fallisce`** *(deve fallire)* | `Bp0` differisce da `Bp`: `n` `12805` contro `12827`, divisioni `2` contro `18` | **DIFFERISCE (giusto)** |
| **`C1`** | `Ap0`: `2` + `0` = `2` contro `nati = 2` | **COINCIDE** |
| **`C1`** | `Bp0`: `2` + `1` = `3` contro `nati = 3` | **COINCIDE** |
| **`C1`** | `B03`: `18` + `7` = `25` contro `nati = 25` | **COINCIDE** |
| **`C1`** | `Bg`: `18` + `7` = `25` contro `nati = 25` | **COINCIDE** |

> ### ✔ **`C0` E `C0-tw` SONO LA PROVA CHE LA PATCH E' PULITA**, e non su un numero solo: `B03` *(ampiezza `0.3`)* e `Bg` *(i due termini di `tw` con un nome)* riproducono `Bp` ### **su TUTTI i conteggi dei cancelli, a tutti e `150` i passi** — `0` differenze. ### **Quindi `_AMP = 0.3` E' l'espressione originale, e la separazione SPINTA/SCARICA non ha cambiato l'aritmetica.**

## IL VERDETTO

> ### **I CINQUE CONTROLLI PASSANO.**
>
> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO.** La rimozione del `0.3` dal simulatore — archivio col tag, censimento degli strumenti che usano `_r_nodo_mitosi`, sigillo, chiusura della voce — ### **e' UNA DECISIONE DI LUCA, e sara' un prompt a parte.**

## CHE COSA RESTA APERTO

1. **il `0.3`**: un numero **scelto**, che `A1` condanna e che `REGOLE_composizione_T3.md` §6.3 dice **<<va derivata>>**, legandolo al **principio di equivalenza**. ### **Questa misura dice che e' PORTANTE, non che e' giusto.**
2. ### **E la domanda che la misura APRE:** la modulazione si modula su `|r_i - r_j|`, ma la torsione e' guidata da `|r_i*phivel_i - r_j*phivel_j|`. ### **Una modulazione DERIVATA leggerebbe la seconda, non la prima** — ma sarebbe una legge nuova, e ### **non la propongo: la nomino.**
3. **`ARCHI-OLTRE-4PI`**, **`GRAVITA-POTENZIALE`**, e la **misura con `DT` dimezzato**, ### **che NON si avvia finche' Luca non lo dice.**

---

*Referto **generato** da `csv/_test_fork/_referto_soglia.py` dal `soglia.json`: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`).*
