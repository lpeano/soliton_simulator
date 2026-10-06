# REFERTO — `M1`-`M4`: **IL VERSO E LE PLAQUETTE**, in sola lettura *(2026-10-06)*

*(Mandato di Luca del 2026-10-06 e sua integrazione. ### **Criteri e previsioni fissati PRIMA della corsa** in `doc/TASK_HISTORY/2026-10-06_misura-verso-e-plaquette.md`, committato **prima** in `76b18ef`.)*

> ### ⛔ **QUESTO REFERTO NON SCEGLIE NIENTE, e lo dice il mandato:** *«questa misura NON sceglie un'opzione. Riporta i numeri e l'unica affermazione permessa e' DESCRITTIVA.»* ### **Le raccomandazioni restano quelle di `doc/GEOM_SENZA_VERSO.md`: questo referto non ne aggiunge e non ne ritira nessuna.**

## LA CORSA

| | |
|---|---|
| simulatore | `b8c21049` *(atteso `b8c21049`: ### **coincide**)* |
| strumenti | `9a00080a` *(`M1`-`M3`)* · `9a00080a` *(`M4`)* |
| passi | ### **230**, un braccio, ### **SOLA LETTURA** |
| passi della misura | `1`, `50`, `150`, `230` |
| passi ### **PESANTI** | `0`, `1`, `49`, `50`, `149`, `150`, `229`, `230` — ### **i quattro della misura E I LORO PREDECESSORI**, perche' la stabilita' e' una differenza fra due passi |
| in configurazione del driver | ### **SI** |
| a valle | `n = 12813`, archi `471580` |
| durata | `753.1 s` |
| piattaforma | 3.13.2 · numpy 2.3.0 |

**LA GEOMETRIA, letta DALLA SCENA** *(nessun numero nuovo)*: `r_regione = 4.096438`, `R_CONN = 2.400000`, quindi `u_bordo = 1 + R_CONN/r_regione = 1.5859`; `sep = 6.1158`, coorti `[411, 413, 413]`.

> ### 📌 **`M4` E' GIRATO SULLA STESSA CORSA DI `M1`-`M3`, e lo dichiaro:** il mandato lo consente *«se lo strumento non e' ancora stato committato»*, e ### **non lo era** quando l'integrazione e' arrivata. ### **Un file separato, un json separato, UNA corsa sola** *(il json lo registra: `gira_sulla_stessa_corsa_di_M1_M3 = SI`)*.

> ### ⚠ **E IL PASSO `1` ERA GIA' VISTO:** il collaudo su `2` passi *(che il mandato chiede)* ha prodotto quei numeri ### **prima** della corsa. ### **Per il passo `1` le mie previsioni non erano previsioni**, e nel task history sono marcate come tali. ### **Le previsioni vere riguardano i passi `50`, `150` e `230`.**

---

## ✔ **CHE COSA HA SCRITTO OGNI CHIAMATA GUARDATA — MISURATO, non dichiarato**

Il presidio `sola_lettura` copia **tutto** `net.__dict__`, ### **misura quali attributi la chiamata ha scritto**, ripristina tutto e ### **riverifica.** ### **Questi non sono gli attributi che io CREDO che vengano scritti: sono quelli che il presidio ha VISTO cambiare.**

| la chiamata | quanti | quali |
|---|--:|---|
| `_base_cicli_topologici` | ### **1** | `_cicli_topologici` |
| `_pesi` | ### **11** | `_S`, `_cs_chiamate`, `_g_kernel_alpha_tot`, `_g_rampa_nodi`, `_g_rampa_prec`, `_g_rampa_prec_disallineata`, `_g_rampa_prec_shape`, `_g_rampa_sotto1`, `_g_rampa_tot`, `_g_scherm_ricorsione`, `_g_tempo_luce_tot` |
| `chiralita_core_locale` | ### **14** | `_S`, `_chi_geom_nodi`, `_cs_chiamate`, `_g_ccl_geom`, `_g_ccl_tot`, `_g_kernel_alpha_tot`, `_g_rampa_nodi`, `_g_rampa_prec`, `_g_rampa_prec_disallineata`, `_g_rampa_prec_shape`, `_g_rampa_sotto1`, `_g_rampa_tot`, `_g_scherm_ricorsione`, `_g_tempo_luce_tot` |
| `massa_critica_adattiva` | ### **11** | `_S`, `_cs_chiamate`, `_g_kernel_alpha_tot`, `_g_rampa_nodi`, `_g_rampa_prec`, `_g_rampa_prec_disallineata`, `_g_rampa_prec_shape`, `_g_rampa_sotto1`, `_g_rampa_tot`, `_g_scherm_ricorsione`, `_g_tempo_luce_tot` |

> ### ⛔ **E AVEVO SCRITTO CHE `lambda_nodi` ERA DI SOLA LETTURA, ED ERA FALSO.** Un elenco a mano avrebbe perso le scritture ### **TRANSITIVE** — e `_chi_geom_nodi` e' ### **la cache che `TORS_4PI` legge al passo dopo**, quindi lasciarla scritta avrebbe cambiato la dinamica della corsa che sto misurando.

---

## `M1` — **`--chi-core` AGISCE SUL DIPOLO?**

**IL CRITERIO, fissato prima:** ### **`(a) = 0` E `(c) = 0` a TUTTI E QUATTRO i passi significa `--chi-core` INERTE per il dipolo.** Altrimenti si riporta dove e quanto agisce. ### **E `(b)` si riporta SEMPRE:** un massimo a `0.98` e uno a `0.001` danno lo stesso `(a) = 0` e ### **dicono due cose opposte.**

| passo | `(a)` nodi con `rho0/rho_c > 1` | `(b)` ### **il MASSIMO del rapporto** | `(c)` diversi da `perc_geom` | `rho_c` | `max |psi|^2` | mediana del rapporto |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | **0** | ### **0.063858** | **0** | 291.276 | 18.6003 | 0.008676 |
| `50` | **0** | ### **0.093184** | **0** | 292.757 | 27.2804 | 0.023628 |
| `150` | **0** | ### **0.061975** | **0** | 292.200 | 18.1091 | 0.021020 |
| `230` | **0** | ### **0.048300** | **0** | 292.585 | 14.1319 | 0.028187 |

> ### ✔ **IL CRITERIO E' SODDISFATTO: `(a) = 0` e `(c) = 0` a tutti e `4` i passi**, quindi ### **`--chi-core` e' INERTE per il dipolo in questa scena.**
>
> ### ⚠ **E `(b)` DICE QUANTO MARGINE C'E', che e' la ragione per cui il mandato lo pretende anche con `(a) = 0`:** il massimo del rapporto arriva a ### **`0.093184`**, cioe' ### **`10.7` volte sotto la soglia.** ### **Non e' <<appena sotto>>: e' lontano.**

**IL CONTROLLO CHE LEGA I DUE CONTI INDIPENDENTI:** `(a)` e `(b)` li ### **ricalcolo io** *(vettorialmente, con la stessa definizione)*, `(c)` viene dalla ### **funzione vera** chiamata dentro il presidio. La funzione modifica `chi_core[k]` ### **solo dove `r > 0`**, cioe' solo dove `rapporto > 1`, quindi ### **`(c)` NON PUO' superare `(a)`.** ### **Esito:** ✔ **regge a tutti i passi**.

---

## `M2` — **`c_k`, LA COERENZA DEL CAMPO AL NODO, col denominatore SATURO**

**LA FORMA, e la correzione verificata sul codice:** `c_k = |satura(F_k)| / satura(amp * Somma_j |W_kj|)`. ### **Il denominatore e' SATURO**, e il motivo e' algebrico: `|satura(f)|` e' ### **monotona nel modulo**, quindi con questa forma ### **`c_k` sta in `[0,1]` e `c = 1` E' RAGGIUNGIBILE** — col denominatore ### **nudo** non lo sarebbe mai.

| passo | `c_k` mediana | MATERIA | BORDO | VUOTO | ### **`AUC` MAT/VUOTO** | fuori da `[0,1]` |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | 0.1841 | 0.7904 | 0.1925 | 0.1627 | ### **0.9992** | 0 |
| `50` | 0.3125 | 0.8293 | 0.3312 | 0.2795 | ### **0.9966** | 0 |
| `150` | 0.2747 | 0.6483 | 0.2974 | 0.2430 | ### **0.9861** | 0 |
| `230` | 0.3001 | 0.4847 | 0.3257 | 0.2665 | ### **0.9023** | 0 |

> ### **`AUC = 0.5` VUOL DIRE NESSUNA SEPARAZIONE.** Qui l'`AUC` e' la probabilita' che un nodo di MATERIA preso a caso abbia `c_k` ### **piu' alto** di un nodo di VUOTO preso a caso.

**E IL SECONDO ASSE CHIESTO DAL MANDATO, il NUMERO DI VICINI** *(secchi dichiarati prima: `0-20`, `21-40`, `41-60`, `61-80`, `81+`)*:

| passo | `0-20` | `21-40` | `41-60` | `61-80` | `81+` | grado medio |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | n/d | 0.1894 *(n=24)* | 0.1884 *(n=2485)* | 0.1747 *(n=4709)* | 0.1901 *(n=5584)* | 73.67 |
| `50` | n/d | 0.2594 *(n=24)* | 0.3050 *(n=2485)* | 0.3023 *(n=4709)* | 0.3263 *(n=5584)* | 73.67 |
| `150` | n/d | 0.2429 *(n=24)* | 0.2721 *(n=2485)* | 0.2693 *(n=4709)* | 0.2822 *(n=5584)* | 73.67 |
| `230` | 0.4635 *(n=11)* | 0.2409 *(n=24)* | 0.2813 *(n=2485)* | 0.2903 *(n=4709)* | 0.3189 *(n=5584)* | 73.61 |

> ### ⚠ **UNA DICHIARAZIONE, invece di un silenzio:** numeratore e denominatore vengono dallo ### **STESSO `w`**, ricalcolato dopo il passo, mentre `net.psi` e' stato calcolato ### **DENTRO** il passo. ### **Sono due istanti diversi**, e lo scarto massimo fra `|net.psi|` e il mio numeratore vale ### **`0.1690`** — si riporta invece di essere taciuto.

---

## `M3` — **QUANTO OSCILLA OGNI CANDIDATO AL <<VERSO>>**

> ### ⛔ **E' LA LETTURA CHE CONTA, perche' col dipolo che entra COME VARIAZIONE un verso GIUSTO ma che OSCILLA inietterebbe `±π` esattamente come adesso.** ### **Il riferimento e' `perc_geom`: il verso di OGGI.**

### `A` — **DUE letture, e il mandato ne nomina una sola**

`tw` e' orientata `i -> j` *(verificato dal codice)*. Quindi:

> ### ⛔ **E QUI AVEVO SCRITTO UNA PREMESSA FALSA: <<tutti gli archi hanno `i < j`>>.** Era misurata ai passi `0`, `1` e `2`, cioe' ### **prima della prima nascita**, e la corsa precedente si e' ### **FERMATA al passo `229`** su `9` archi fuori convenzione. ### **Ogni nascita ne produce ESATTAMENTE uno**: alla mitosi nascono `a-m` e `m-b` col nodo nuovo `m` di indice ### **piu' alto**, quindi `m-b` ha `i > j` ### **sempre.** ### ✔ **Adesso il conto NON si assume: si MISURA a ogni passo** -- `1`: 0, `50`: 0, `150`: 0, `230`: 11 -- e la chiave d'arco e' ### **canonica `(min, max)`**, col segno della circolazione ### **letto dall'arco** invece che dedotto.

| | |
|---|---|
| `A` ### **GREZZA** | `Σ tw` col segno ### **MEMORIZZATO** — ### ⛔ **dipende dalla NUMERAZIONE** |
| `A` ### **DIVERGENZA** | col segno ### **relativo al nodo**: il ### **flusso uscente**, ben definito — ### **e non e' una circolazione** |

| passo | nodi | `A` grezza: cambi | frazione | `A` divergenza: cambi | frazione | ### **`perc_geom`: cambi** | ### **frazione** | `A` grezza `= 0` |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 12802 | 0 | 0.00 % | 0 | 0.00 % | ### **6419** | ### **50.14 %** | 12802 |
| `50` | 12802 | 59 | 0.46 % | 45 | 0.35 % | ### **0** | ### **0.00 %** | 0 |
| `150` | 12802 | 35 | 0.27 % | 35 | 0.27 % | ### **0** | ### **0.00 %** | 0 |
| `230` | 12811 | 34 | 0.27 % | 30 | 0.23 % | ### **1** | ### **0.01 %** | 2 |

### `D` — **il segno di `tw` SULL'ARCO**, confrontato ### **per CHIAVE `(i,j)`**

> ### ⚠ **PER CHIAVE E NON PER INDICE**, perche' alla mitosi `i = concat([i[keep], a, m])` ### **rimescola gli indici**: un confronto per indice conterebbe cambi che non ci sono. ### **E gli archi non confrontabili si CONTANO.**

| passo | archi | ### **con `i > j`** | confrontabili | nuovi | cambi di `sign(tw)` | frazione |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | 471564 | ### **0** | 471564 | 0 | 0 | 0.00 % |
| `50` | 471564 | ### **0** | 471564 | 0 | 2180 | 0.46 % |
| `150` | 471564 | ### **0** | 471564 | 0 | 1144 | 0.24 % |
| `230` | 471580 | ### **11** | 471576 | 4 | 1211 | 0.26 % |

> ### ✔ **E IL SEGNO SI CONFRONTA RIDOTTO AL VERSO CANONICO `min -> max`:** `tw` e' una ### **1-forma orientata**, quindi confrontare `sign(tw)` fra due passi senza quella riduzione ### **conterebbe un cambio di segno dove e' cambiata solo la SCRITTURA dell'arco.**

**E `A` E `D` SI PRENDONO A OGNI PASSO, non solo ai quattro** *(costano poco)*, quindi si puo' dare ### **la media su tutta la corsa**:

| | passi | frazione media per passo |
|---|--:|--:|
| `A` grezza | 230 | ### **0.72 %** |
| `D` segno di `tw` | 230 | ### **0.82 %** |
| ### **`perc_geom`** *(il riferimento di oggi)* | 230 | ### **0.22 %** |

### `C` — **l'OLONOMIA DI FASE sulla base dei cicli**

> ### ⛔ **LA CONVENZIONE DEL `verso` L'HO MISURATA, NON DEDOTTA:** il cammino e' `u -> lca -> v -> u` e ### **la chiusura si percorre `v -> u` mentre il suo `verso` e' registrato `+1`**, cioe' opposto. ### **La via primaria e' `_vertici_ciclo`**, che chiude il ciclo per costruzione; quella sugli archi resta come ### **controllo indipendente.**

| passo | cicli | ### **olonomia non nulla** | frazione | `|k|` max | scarto dal multiplo di `4π` | ### **le due vie: modulo** | ### **segno discorde** | base cambiata |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 256 | ### **122** | 47.66 % | 2 | 5.33e-15 | 7.11e-15 | ### **122** | 0 su 256 (0.00 %) |
| `50` | 256 | ### **153** | 59.77 % | 3 | 8.88e-15 | 7.11e-15 | ### **153** | 0 su 256 (0.00 %) |
| `150` | 256 | ### **171** | 66.80 % | 3 | 7.11e-15 | 1.42e-14 | ### **171** | 0 su 256 (0.00 %) |
| `230` | 256 | ### **189** | 73.83 % | 4 | 1.42e-14 | 2.13e-14 | ### **189** | 0 su 256 (0.00 %) |

> ### ✔ **L'ALGEBRA DELL'OBIEZIONE `(b)` E' CONFERMATA DAL NUMERO, non assunta:** su un ciclo chiuso la somma di `(phi_i - phi_j)` telescopia a `0` esatto e `_wphi` avvolge sul periodo `4π`, quindi l'olonomia ### **deve** essere un multiplo intero di `4π`. ### **Scarto massimo misurato: `1.42e-14`.**
>
> ### ⛔ **E IL SEGNO DELL'OLONOMIA NON E' DETERMINATO DAL GRAFO:** le due vie concordano sul ### **MODULO** e ### **discordano sul SEGNO** su ### **TUTTI** i cicli con olonomia non nulla, a ### **ogni** passo misurato *(122, 153, 171, 189 su 122, 153, 171, 189)*. ### **Due routine DEL SIMULATORE scelgono versi opposti sullo STESSO ciclo** — ed e' precisamente l'arbitrarieta' che l'obiezione `(a)` attribuisce all'opzione `C`.

---

## `M4` — **LE PLAQUETTE** *(l'opzione `P` di Luca)*

**La plaquette:** un triangolo coi ### **tre archi presenti.** La circolazione sul cammino `u -> v -> w -> u` e' `tw[(u,v)] + tw[(v,w)] - tw[(u,w)]`, e ### **il meno c'e' perche' l'ultimo tratto va contro la convenzione `i < j`.**

> ### ✔ **E IL SEGNO DI UNA SINGOLA PLAQUETTE E' ARBITRARIO, IL PRODOTTO COL VERSORE NO:** scambiando due vertici la circolazione cambia segno ### **e la normale anche**, quindi il prodotto ### **`(Σ tw) · n̂` e' INVARIANTE mentre ciascun fattore da solo NON LO E'.** ### **Per questo `(b)` misura il MODULO e `(c)` il VETTORE** — e ### **`R_k` resta un ASSE: l'invarianza non regala il segno.**

### `(a)` **quante, e quanto costano**

| passo | ### **plaquette** | conto ### **indipendente** | degeneri | archi `i > j` | cappi esclusi | nodi senza plaquette | `s` enumerazione | `s` controllo | MATERIA | BORDO | VUOTO |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **5534011** | 5534011 | 0 | ### **0** | 0 | 0 | 4.91 | 0.33 | 1505 | 1495 | 1330 |
| `50` | ### **5534011** | 5534011 | 0 | ### **0** | 0 | 0 | 4.88 | 0.32 | 1505 | 1494 | 1330 |
| `150` | ### **5534011** | 5534011 | 0 | ### **0** | 0 | 0 | 4.86 | 0.31 | 1505 | 1496 | 1331 |
| `230` | ### **5533797** | 5533797 | 0 | ### **11** | 0 | 11 | 4.92 | 0.30 | 1502 | 1494 | 1333 |

*(Le tre colonne di classe sono la ### **MEDIANA delle plaquette per nodo**.)*

> ### ✔ **IL CONTO INDIPENDENTE:** coincide a tutti i passi. Per ogni arco il numero di ### **vicini comuni** e' il numero di triangoli che passano per quell'arco, e sommato sugli archi orientati ogni triangolo si conta ### **sei volte.** ### **Non passa da nessuna chiave**, quindi non condivide nessun difetto con l'enumerazione — e ### ⛔ **in costruzione ha trovato un traboccamento `int32` che faceva sparire il `97 %` dei triangoli IN SILENZIO.**

### `(b)` **`|Σ tw|` sulle plaquette**, per classe

| passo | campione | q05 | q25 | ### **q50** | q75 | q95 | max | MATERIA *(media per nodo)* | BORDO | VUOTO |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 190835 | 0.0000 | 0.0000 | ### **0.0000** | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `50` | 190835 | 0.0031 | 0.0280 | ### **0.0875** | 0.1997 | 0.4699 | 1.7625 | 0.0668 | 0.1303 | 0.1433 |
| `150` | 190835 | 0.0255 | 0.1530 | ### **0.3916** | 0.8488 | 1.9249 | 6.1652 | 0.2928 | 0.5196 | 0.6143 |
| `230` | 190826 | 0.0374 | 0.2168 | ### **0.5348** | 1.1089 | 2.4017 | 9.0680 | 0.3889 | 0.6832 | 0.8117 |

*(I quantili vengono da un sottocampione a ### **passo PRIMO fisso** `29`: ### **deterministico, nessun RNG, nessun seme da dichiarare.**)*

### `(c)` **LA COERENZA `|Σ v| / Σ |v|`** — `0` disordine, `1` stesso asse

| passo | MATERIA | BORDO | VUOTO | MATERIA q25-q75 | VUOTO q25-q75 | nodi senza `R` definito |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **n/d** | n/d | ### **n/d** | n/d - n/d | n/d - n/d | 0 |
| `50` | ### **0.0343** | 0.0292 | ### **0.0342** | 0.0227 - 0.0510 | 0.0219 - 0.0563 | 0 |
| `150` | ### **0.0313** | 0.0339 | ### **0.0360** | 0.0204 - 0.0475 | 0.0227 - 0.0579 | 0 |
| `230` | ### **0.0395** | 0.0448 | ### **0.0446** | 0.0252 - 0.0579 | 0.0297 - 0.0669 | 11 |

> ### ⚠ **E UN NODO SENZA NESSUNA PLAQUETTE NON DEGENERE HA COERENZA `NaN`, NON `0`:** un `0` li' vorrebbe dire *«disordine totale»* mentre la verita' e' *«non definita»*. ### **E' la famiglia di `CHI-TORS-ZERO-FALSO`, e il collaudo me l'ha trovato addosso.**

### `(d)` **il coseno fra `R_k` e l'asse di Bloch `_nb`** — *e `P2` dipende da qui*

**IL CASO NULLO E' ANALITICO, non simulato:** fra due assi indipendenti in `3D` il coseno e' ### **UNIFORME su `[-1,1]`**, quindi ### **media `0`** e ### **frazione con `|cos| > 0.5` pari a `0.5`.**

| passo | media MATERIA | media BORDO | media VUOTO | `|cos|>0.5` MATERIA | BORDO | VUOTO | ### **atteso dal caso** |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | n/d | n/d | n/d | n/d | n/d | n/d | media `0.0`, frazione `0.5` |
| `50` | 0.0072 | 0.0021 | 0.0113 | 0.4847 | 0.4788 | 0.5039 | media `0.0`, frazione `0.5` |
| `150` | 0.0022 | -0.0152 | 0.0013 | 0.5157 | 0.5051 | 0.4994 | media `0.0`, frazione `0.5` |
| `230` | -0.0338 | 0.0041 | -0.0078 | 0.5070 | 0.4932 | 0.4930 | media `0.0`, frazione `0.5` |

### `(e)` **LA STABILITA': di quanto ruota `R_k` fra due passi**

| passo | contro il passo | nodi | ### **angolo mediano (gradi)** MATERIA | BORDO | VUOTO | nodi senza `R` | ### **riferimento: `perc_geom` cambia** |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | `0` | 12802 | ### **n/d** | n/d | n/d | 12802 | ### **50.14 %** |
| `50` | `49` | 12802 | ### **0.88** | 1.28 | 1.50 | 0 | ### **0.00 %** |
| `150` | `149` | 12802 | ### **0.40** | 0.53 | 0.67 | 0 | ### **0.00 %** |
| `230` | `229` | 12811 | ### **0.56** | 0.64 | 0.82 | 9 | ### **0.01 %** |

> ### ⚠ **E I PASSI CAMPIONATI NON SONO PASSI MEDI, per il RIFERIMENTO:** su tutta la corsa `perc_geom` cambia ### **0.22 %** dei nodi per passo, mentre ai passi della misura cambia `50`: 0.00 %, `150`: 0.00 %, `230`: 0.01 %. ### **Il confronto di `(e)` va letto sapendo questo**: ai quattro passi scelti il riferimento e' ### **piu' QUIETO** della sua media.
>
> ### **L'ANGOLO E IL RIFERIMENTO MISURANO DUE COSE DIVERSE, e lo dico perche' non si confondano:** l'angolo e' ### **CONTINUO** *(di quanto ruota un asse)*, la frazione di `perc_geom` e' ### **DISCRETA** *(quanti nodi cambiano valore)*. ### **Non sono la stessa grandezza e non si sottraggono** — stanno accanto perche' il mandato chiede il confronto, e ### **il confronto e' fra due letture, non fra due numeri.**

---

## ⚠ **LE MIE PREVISIONI, CONTRO I NUMERI** — *e le stampa lo script*

Le previsioni sono fissate in `doc/TASK_HISTORY/2026-10-06_misura-verso-e-plaquette.md`, committato ### **prima della corsa** in `76b18ef`. ### **Qui le confronta il codice, non la mia buona volonta'** — e ### **il passo `1` non conta: era GIA' VISTO** *(il collaudo su `2` passi)*, quindi si guardano i passi ### **oltre il primo.**

| | la previsione | il numero | esito |
|---|---|---|---|
| `M1` | ### **`--chi-core` INERTE** per il dipolo | `(a)` e `(c)` valgono `0` su 3 passi su 3; il massimo del rapporto ### **SCENDE**: `0.093184`, `0.061975`, `0.048300` | ### ✔ **CONFERMATA** |
| `M2` | `c_k` ### **separa MATERIA da VUOTO** | `AUC` fra `0.9023` e `0.9966` *(`0.5` = nessuna separazione)* | ### ✔ **CONFERMATA** |
| `M3-A` | i cambi di segno ### **CALANO** coi passi | frazione per passo: `50` -> 0.46 %, `150` -> 0.27 %, `230` -> 0.27 % | ### ✔ **CONFERMATA** |
| `M3-C` | la base dei cicli ### **cambia molto** con le nascite | massimo cambiato: 0.00 %, con nascite | ### ⛔ **SMENTITA**: non cambia |
| `M4(c)` | la ### **COERENZA e' BASSA** | mediane per classe fra `0.0292` e `0.0448` *(soglia di <<bassa>>: `0.5`, il punto medio -- ### **e' una mia convenzione, DICHIARATA, non una misura**)* | ### ✔ **CONFERMATA** |
| `M4(d)` | `R_k` e `_nb` ### **SCORRELATI, come il caso** | scarto massimo dal caso nullo: la ### **media** del coseno a ### **2.04 sigma** dallo zero, la ### **frazione** `|cos| > 0.5` a ### **2.49 sigma** da `0.5`; tolleranza ### **2.99 sigma**, che e' ### **Bonferroni su 18 confronti** e non un numero scelto *(`sigma` e' ### **DERIVATO**: per un coseno uniforme su `[-1,1]` la varianza e' `1/3`, e per una frazione attorno a `0.5` e' `0.5/sqrt(n)`)* | ### ✔ **CONFERMATA** |
| `M4(e)` | `R_k` ### **ruota DI MOLTO** fra due passi, cioe' ### **NON e' stabile** | angolo mediano fra `0.40` e `1.50` gradi *(soglia di <<molto>>: `10` gradi -- ### **e' una mia convenzione, DICHIARATA**)* | ### ⛔ **SMENTITA** |

> ### **5 confermate, 2 SMENTITE, 0 non decidibili.** ### **Le smentite sono il pezzo che vale:** una misura che conferma tutto quello che credevo ### **non mi ha insegnato niente.**

> ### ⚠ **E DUE SOGLIE DI QUESTA TAVOLA SONO MIE, non misurate:** ### **<<bassa>> = `0.5`** per la coerenza e ### **<<di molto>> = `10` gradi** per la rotazione. ### **Le dichiaro perche' un esito che dipende da una soglia scelta da me DEVE dirlo** -- la tolleranza di `M4(d)`, invece, e' ### **DERIVATA** dalla varianza di una distribuzione uniforme.

---

## ⛔ **CHE COSA QUESTA MISURA NON DICE**

| | |
|---|---|
| ### **non sceglie un'opzione** | lo vieta il mandato, e ### **le raccomandazioni restano quelle di `doc/GEOM_SENZA_VERSO.md`** |
| ### **non misura `f'`** | la quota di conteggi *(un arco sta in una frazione delle plaquette del nodo)* ### **NON e' la derivata**: `f'` dipende anche dalla normalizzazione di `chi_k` e dalla coerenza delle normali |
| ### **non prova la prova dello specchio** | `B` della Stella Polare resta ### **NON FATTA**: il controllo che direbbe se il verso e' una chiralita' vera o un artefatto dell'orientamento del grafo |
| ### **non chiude `U1`** | `chiralita_core_locale` prende `rho_c` da `massa_critica_adattiva`, che chiama ### **la stessa** `massa_critica_collasso`: ### **il ramo adattivo non sfugge a `U1`** — e se aprire `U1` per questa funzione e' una decisione di Luca |
| ### **non e' un braccio contro un braccio** | e' ### **un braccio solo**: dice come si comportano i candidati ### **oggi**, non che cosa cambierebbe una cura |

**AVVISI DEGLI STRUMENTI:** ### ✔ **nessuno**

> ### ⛔ **LA SCELTA FRA `A`/`B`/`C`/`D`/`P`, FRA `P1`/`P2`/`P3` — cioe' se il verso e' un SEGNO o un ASSE — E SE APRIRE `U1` PER `chiralita_core_locale`, SONO DECISIONI DI LUCA.**

---

# ANNOTAZIONE DI CHIUSURA *(2026-10-06 sera — `par.8`: si ANNOTA, non si riscrive)*

*(Registrazione decisa da Luca alla chiusura della sessione. ### **Nessuna corsa, nessuna
patch al simulatore** — resta `b8c21049`. ### **`doc/ASSIOMI.md` non toccato.**)*

## `(a)` ⛔ **L'OBIEZIONE `(b)` DEL GUARDIANO E' SMENTITA; LA `(a)` E' RAFFORZATA**

**La previsione era:** *«l'olonomia e' zero sulla maggior parte dei cicli»*. **Misurato:**

| passo | `1` | `50` | `150` | `230` |
|---|--:|--:|--:|--:|
| cicli con olonomia ### **NON nulla** | `47.66 %` | `59.77 %` | `66.80 %` | ### **`73.83 %`** |

> ### ⛔ **SMENTITA, E SEMPRE DI PIU':** a `230` passi ### **tre quarti** dei cicli della
> base hanno olonomia diversa da zero, con `|k|` fino a ### **`4`**.
> ### **Il `0` che l'obiezione `(b)` temeva NON e' il caso tipico in questa scena.**

**LE OBIEZIONI `(a)` E `(c)` RESTANO**, e la `(a)` ### **si rafforza con un fatto nuovo:**
la base dei `256` cicli ### **non cambia MAI** — `0.00 %` a tutti e quattro i passi,
### **nemmeno al `230`, dove nascono nodi.**

> ### ⛔ **PERCHE' COPRE SOLO GLI ARCHI DI INDICE PIU' BASSO.** Il taglio
> `if len(cicli) >= massimo: break` tiene i primi `256` archi non-albero
> ### **in ordine di INDICE**, e cio' che succede altrove — ### **comprese le nascite** —
> ### **non li tocca.** ### **Una base che non reagisce alla rete non e' una descrizione
> della rete: e' una descrizione della NUMERAZIONE.**

## `(b)` ⛔ **UN ERRORE DEL GUARDIANO: LA FINESTRA `1`-`230` ERA SBAGLIATA PER LA STABILITA'**

| | |
|---|---|
| le nascite | cominciano al passo ### **`216`**: su `230` passi, ### **`14` passi su `230`** hanno dinamica di mitosi |
| la torsione | e' ### **quasi tutta sotto `2π`** in questa finestra |
| `perc_geom` | ### **quasi non cambia**: `0.00 %`, `0.00 %`, `0.01 %` ai passi `50`, `150`, `230` |

> ### ⛔ **E' IL REGIME IN CUI IL DIFETTO DA CURARE NON AGISCE.** Misurare la
> ### **stabilita' di un verso** dove il sistema e' quasi fermo ### **non dice quanto quel
> verso oscilli quando il sistema si muove.** ### **L'errore e' nella SCELTA DELLA
> FINESTRA, non nei numeri**, e i numeri restano veri ### **per quella finestra.**
>
> ### ✔ **LA CURA E' `A1` DI `doc/RIPRESA_2026-10-07.md`:** la misura si rifa' su
> ### **`1000` passi**, con i passi pesanti ### **oltre il `216`.**

## `(c)` ⛔ **IL TITOLO DEL REFERTO E' CORRETTO NEL MERITO: IL METRO ERA SBAGLIATO**

> ### ⛔ **<<`A` e `D` oscillano piu' di `perc_geom`>> CONFRONTA FRAZIONI DI SEGNI CHE
> CAMBIANO, E QUELLO NON E' IL METRO.**

| | perche' il conteggio dei segni non misura cio' che conta |
|---|---|
| **`D`** | il dipolo e' ### **CONTINUO**: un `tw` che passa per zero ### **non inietta niente** — il segno cambia e la spinta e' ### **infinitesima** |
| **`A`**, **`B`**, **`C`** | ogni cambio e' un ### **SALTO DI `π`**: un conteggio e una spinta ### **coincidono** solo qui |
| **`perc_geom`** | cambia ### **PER NODO**, e ogni nodo tocca ### **~`74` archi** *(il grado medio misurato)*: ### **un cambio non e' un cambio** |

> ### ✔ **LA GRANDEZZA DA CONFRONTARE, PER TUTTE LE OPZIONI, E' LA SPINTA INIETTATA:**
> ### **`Σ |Δdipolo|` per passo.** ### **E' l'unica che mette `A`, `B`, `C`, `D`, `P` e il
> riferimento sulla STESSA unita'** — e ### **`A1` la misura.**
>
> ### ⚠ **E IL NUMERO VECCHIO NON E' FALSO: e' di un'altra grandezza.** `0.72 %`, `0.82 %`
> e `0.22 %` restano ### **i cambi di segno per passo**, e vanno letti come tali.
> ### **E' il terzo caso in due giorni in cui prendo un numero vero e lo porto dove misura
> un'altra cosa.**

## `(d)` ⛔ **IL SEGNO DISCORDE HA UNA CAUSA NEL SIMULATORE: UN DIFETTO, ora REGISTRATO**

> ### ⛔ **VOCE NUOVA: `CICLO-CHIUSURA-SEGNO`** *(cercata prima nell'indice con sei
> termini — `base_cicli`, `circolazione`, `olonomia`, `ciclo`, `chiusura`, `verso` —
> ### **non esisteva**; `GEOM-SENZA-VERSO` riguarda `perc_geom`, che e' un'altra cosa)*.

**LA CAUSA, trovata durante il collaudo di `M3-C`:** in `_base_cicli_topologici` il ciclo
si percorre ### **`u -> lca -> v -> u`**, ma il segno dell'arco di ### **CHIUSURA** e'
registrato ### **`+1`** — cioe' ### **OPPOSTO al verso in cui il ciclo lo percorre.**

| la convenzione | scarto dell'olonomia dal multiplo di `4π` |
|---|--:|
| come ### **MEMORIZZATO** | ### ⛔ **`6.17`** |
| ### **solo la CHIUSURA ribaltata** | ### ✔ **`7.1e-15`** |

> ### ⛔ **DA QUI IL SEGNO DISCORDE: `189` cicli su `189`** al passo `230` — tutti quelli
> con olonomia non nulla — mentre il ### **MODULO** concorda a ### **`2.1e-14`.**
> ### **Due routine DEL SIMULATORE danno versi opposti sullo STESSO ciclo.**

### ✔ **CHI LO LEGGE — censito COL COMANDO (`AST` su `soliton_simulator.py`), non assunto**

| la catena | chi la chiama |
|---|---|
| `_base_cicli_topologici` | ### **SOLO** `circolazione_topologica` |
| `circolazione_topologica` | ### **SOLO** `_diag_completa` |
| `_diag_completa` | ### **SOLO** `batch_condensazione`, lo ### **scrittore dei CSV** — ### ⛔ **NON `step()`, NON `passo_pieno`** |

> ### ✔ **QUINDI OGGI IL SEGNO LO LEGGE SOLO LA DIAGNOSTICA, E NESSUNA LEGGE.** L'unica
> scrittura di `_diag_completa` su `net` e' ### **`_ang_asse_prec`**, una memoria
> diagnostica. Fuori dal simulatore lo leggono ### **solo strumenti di misura**
> *(`_diag_triangoli`, `_lettura_torsione_spinore`, `_letture_ab`, `_scansione_schemi`,
> `test_olonomia_chiralita`, e i due di `M1`-`M4`)*; ### **tutte le altre occorrenze sono
> COPIE** del simulatore nei sigilli e nei backup.
>
> ### ✔ **LA CURA E' QUINDI UNA CORREZIONE A SE', CON SIGILLO, e NON tocca la fisica.**
> ### ⛔ **MA VA FATTA PRIMA DI QUALUNQUE SCELTA CHE USI IL SEGNO DI UN CICLO:** le opzioni
> ### **`B`** e ### **`C`** leggerebbero ### **esattamente quel segno**, e oggi
> ### **non e' definito in modo univoco.** ### **E' il punto `A2` della ripresa.**

## `(e)` ⛔ **PER `P`, IL VALORE SUI NODI NATI E' INDEFINITO** *(`S-dominio`)*

Al passo `230` gli ### **`11` nodi nati** *(`12802` → `12813`)* hanno
### **ZERO plaquette**: un nato siede su un arco suddiviso, quindi ha
### **due vicini che non sono collegati fra loro** — ### **nessun triangolo.**

> ### ⛔ **QUINDI `R_k` NON ESISTE SUI NATI, e vale `NaN` — non `0`.** ### **Un `0` li'
> direbbe <<disordine totale>> dove la verita' e' <<non definito>>**, ed e' la famiglia di
> `CHI-TORS-ZERO-FALSO`. ### **Per `P` questo e' un `S-dominio` da dichiarare PRIMA della
> cura:** una legge che non ha valore sui nodi appena nati ### **deve dire che cosa fa
> li'**, e ### **non puo' scoprirlo a corsa in volo.**

## `(f)` **I RISULTATI, in forma breve**

### `M1` — ### ✔ **`--chi-core` e' INERTE per il dipolo**

`(a) = 0` e `(c) = 0` a ### **tutti e quattro** i passi; il massimo del rapporto
### **SCENDE** *(`0.0932`, `0.0620`, `0.0483`)* e il massimo assoluto e'
### **`10.7` volte sotto la soglia.** ### **E in CALO, quindi il margine cresce.**

### `M2` — ⚠ **`c_k` separa MATERIA da VUOTO, MA LA SEPARAZIONE CALA**

| | passo `1` | `50` | `150` | `230` |
|---|--:|--:|--:|--:|
| `AUC` MATERIA / VUOTO | `0.9992` | `0.9966` | `0.9861` | ### **`0.9023`** |
| mediana di `c_k` in MATERIA | `0.7904` | `0.8293` | `0.6483` | ### **`0.4847`** |

> ### ⛔ **LE MASSE PERDONO COERENZA, e questa e' una DOMANDA APERTA, non un risultato.**
> In `230` passi la mediana di MATERIA ### **quasi si dimezza** e l'`AUC` scende di
> ### **`~0.10`**. ### **Non so perche'**, e non lo deduco da qui: ### **sta in `B7` della
> ripresa.**

### `M4` — **la coerenza dell'asse e' quella del CASO, e non c'e' legame con lo spin**

**IL CONTO DEL CASO NULLO, scritto** *(e non e' una simulazione: e' algebra)*:

```
R_k = SOMMA sulle plaquette p di  c_p * n_cappello(p)
direzioni INDIPENDENTI  ->  E|R_k|^2 = SOMMA c_p^2   (i termini incrociati hanno media 0)
coerenza attesa = sqrt(SOMMA c^2) / SOMMA c
a MODULI UGUALI  ->  sqrt(N)/N = 1/sqrt(N)      <- il LIMITE INFERIORE
```

| al passo `230` | plaquette per nodo | `1/sqrt(N)` | ### **misurato** | rapporto |
|---|--:|--:|--:|--:|
| MATERIA | `1502` | `0.0258` | ### **`0.0395`** | `1.53` |
| BORDO | `1494` | `0.0259` | ### **`0.0448`** | `1.73` |
| VUOTO | `1333` | `0.0274` | ### **`0.0446`** | `1.63` |

> ### **LA COERENZA MISURATA E' DELL'ORDINE DEL CASO:** sta ### **`1.1`-`1.7` volte** sopra
> il limite inferiore, ### **ed e' UGUALE in tutte e tre le classi.**
>
> ### ⚠ **E NON SO SEPARARE DUE SPIEGAZIONI, quindi non scelgo:** l'eccesso sopra
> `1/sqrt(N)` e' ### **esattamente cio' che producono moduli ETEROGENEI** *(il fattore e'
> `sqrt(E[c²])/E[c]`, che vale `1` solo a moduli uguali, e i quantili di `|Σ tw|` al `230`
> vanno da `0.037` a `2.40`)*, ### **ma potrebbe anche essere un allineamento DEBOLE vero.**
> ### ⚠ **E il rapporto CRESCE** *(`1.1`-`1.3` al passo `50`, `1.5`-`1.7` al `230`)*:
> ### **anche quello puo' essere l'una o l'altra cosa.**
> ### ✔ **CHE COSA LE SEPARA:** un ### **nullo per PERMUTAZIONE** — si rimescolano le
> normali tenendo i moduli — oppure la distribuzione di `|Σ tw|` ### **per nodo**, che
> questo json ### **non porta.** ### **Va aggiunto in `A1`.**

**E le altre due voci:** il coseno fra `R_k` e l'asse di Bloch `_nb` sta ### **dentro il
caso nullo** *(`2.04 σ` e `2.49 σ` contro una soglia ### **Bonferroni** di `2.99 σ` su `18`
confronti)* — ### **nessun legame con lo spin in questa scena** — e `R_k` e'
### **STABILE**, con una rotazione mediana di ### **`0.40`-`1.50` gradi** per passo.
