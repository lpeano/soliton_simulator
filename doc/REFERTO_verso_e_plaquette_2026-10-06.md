# REFERTO — `M1`-`M4`: **IL VERSO E LE PLAQUETTE**, in sola lettura *(2026-10-06)*

*(Mandato di Luca del 2026-10-06 e sua integrazione. ### **Criteri e previsioni fissati PRIMA della corsa** in `doc/TASK_HISTORY/2026-10-06_misura-verso-e-plaquette.md`, committato **prima** in `76b18ef`.)*

> ### ⛔ **QUESTO REFERTO NON SCEGLIE NIENTE, e lo dice il mandato:** *«questa misura NON sceglie un'opzione. Riporta i numeri e l'unica affermazione permessa e' DESCRITTIVA.»* ### **Le raccomandazioni restano quelle di `doc/GEOM_SENZA_VERSO.md`: questo referto non ne aggiunge e non ne ritira nessuna.**

> ### ⛔ **E QUESTA E' UNA CORSA LUNGA CON `U1` APERTA, e lo dichiaro in testa:** `U1` dice *<<URGENTE, PRIMA DI QUALUNQUE GIRO LUNGO>>*. ### **La misura SERVE A SCEGLIERE LA CURA, non a dare valori assoluti** -- e l'argomento sta nel task history di `A1`: ### **le opzioni non sono bracci diversi del simulatore, sono CINQUE LETTURE DELLA STESSA CORSA**, quindi la legge difettosa che `U1` denuncia e' ### **la stessa in tutti i termini del confronto**, e un difetto comune a tutti i termini ### **non ne cambia l'ordine.** ### ✔ **E per questa scena `U1` e' ancora piu' lontana, ed e' MISURATO:** `M1` trova `--chi-core` ### **INERTE per il dipolo.**

## LA CORSA

| | |
|---|---|
| simulatore | `b8c21049` *(atteso `b8c21049`: ### **coincide**)* |
| strumenti | `670c4d75` *(`M1`-`M3`)* · `670c4d75` *(`M4`)* |
| passi | ### **1000**, un braccio, ### **SOLA LETTURA** |
| passi della misura | `1`, `150`, `230`, `300`, `400`, `500`, `700`, `1000` |
| passi ### **PESANTI** | `0`, `1`, `149`, `150`, `229`, `230`, `299`, `300`, `399`, `400`, `499`, `500`, `699`, `700`, `999`, `1000` — ### **i quattro della misura E I LORO PREDECESSORI**, perche' la stabilita' e' una differenza fra due passi |
| in configurazione del driver | ### **SI** |
| a valle | `n = 13629`, archi `472653` |
| durata | `7039.8 s` |
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
| `_pesi` | ### **12** | `_S`, `_cs_chiamate`, `_g_kernel_alpha_tot`, `_g_rampa_cali`, `_g_rampa_calo_quando`, `_g_rampa_calo_somma`, `_g_rampa_nodi`, `_g_rampa_prec`, `_g_rampa_sotto1`, `_g_rampa_tot`, `_g_scherm_ricorsione`, `_g_tempo_luce_tot` |
| `_tau_tw_locale` | ### **1** | `_g_tautw_tot` |
| `_wphi` | ### **0** | ### **nessuno** |
| `chiralita_core_locale` | ### **15** | `_S`, `_chi_geom_nodi`, `_cs_chiamate`, `_g_ccl_geom`, `_g_ccl_tot`, `_g_kernel_alpha_tot`, `_g_rampa_cali`, `_g_rampa_calo_quando`, `_g_rampa_calo_somma`, `_g_rampa_nodi`, `_g_rampa_prec`, `_g_rampa_sotto1`, `_g_rampa_tot`, `_g_scherm_ricorsione`, `_g_tempo_luce_tot` |
| `massa_critica_adattiva` | ### **12** | `_S`, `_cs_chiamate`, `_g_kernel_alpha_tot`, `_g_rampa_cali`, `_g_rampa_calo_quando`, `_g_rampa_calo_somma`, `_g_rampa_nodi`, `_g_rampa_prec`, `_g_rampa_sotto1`, `_g_rampa_tot`, `_g_scherm_ricorsione`, `_g_tempo_luce_tot` |

> ### ⛔ **E AVEVO SCRITTO CHE `lambda_nodi` ERA DI SOLA LETTURA, ED ERA FALSO.** Un elenco a mano avrebbe perso le scritture ### **TRANSITIVE** — e `_chi_geom_nodi` e' ### **la cache che `TORS_4PI` legge al passo dopo**, quindi lasciarla scritta avrebbe cambiato la dinamica della corsa che sto misurando.

---

## `M1` — **`--chi-core` AGISCE SUL DIPOLO?**

**IL CRITERIO, fissato prima:** ### **`(a) = 0` E `(c) = 0` a TUTTI E QUATTRO i passi significa `--chi-core` INERTE per il dipolo.** Altrimenti si riporta dove e quanto agisce. ### **E `(b)` si riporta SEMPRE:** un massimo a `0.98` e uno a `0.001` danno lo stesso `(a) = 0` e ### **dicono due cose opposte.**

| passo | `(a)` nodi con `rho0/rho_c > 1` | `(b)` ### **il MASSIMO del rapporto** | `(c)` diversi da `perc_geom` | `rho_c` | `max |psi|^2` | mediana del rapporto |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | **0** | ### **0.063858** | **0** | 291.276 | 18.6003 | 0.008676 |
| `150` | **0** | ### **0.061975** | **0** | 292.200 | 18.1091 | 0.021020 |
| `230` | **0** | ### **0.048300** | **0** | 292.585 | 14.1319 | 0.028187 |
| `300` | **0** | ### **0.074282** | **0** | 292.692 | 21.7417 | 0.035334 |
| `400` | **0** | ### **0.120083** | **0** | 292.786 | 35.1585 | 0.047251 |
| `500` | **0** | ### **0.129733** | **0** | 292.811 | 37.9872 | 0.055350 |
| `700` | **0** | ### **0.149377** | **0** | 292.734 | 43.7277 | 0.061345 |
| `1000` | **0** | ### **0.130483** | **0** | 292.815 | 38.2073 | 0.065440 |

> ### ✔ **IL CRITERIO E' SODDISFATTO: `(a) = 0` e `(c) = 0` a tutti e `8` i passi**, quindi ### **`--chi-core` e' INERTE per il dipolo in questa scena.**
>
> ### ⚠ **E `(b)` DICE QUANTO MARGINE C'E', che e' la ragione per cui il mandato lo pretende anche con `(a) = 0`:** il massimo del rapporto arriva a ### **`0.149377`**, cioe' ### **`6.7` volte sotto la soglia.** ### **Non e' <<appena sotto>>: e' lontano.**

**IL CONTROLLO CHE LEGA I DUE CONTI INDIPENDENTI:** `(a)` e `(b)` li ### **ricalcolo io** *(vettorialmente, con la stessa definizione)*, `(c)` viene dalla ### **funzione vera** chiamata dentro il presidio. La funzione modifica `chi_core[k]` ### **solo dove `r > 0`**, cioe' solo dove `rapporto > 1`, quindi ### **`(c)` NON PUO' superare `(a)`.** ### **Esito:** ✔ **regge a tutti i passi**.

---

## `M2` — **`c_k`, LA COERENZA DEL CAMPO AL NODO, col denominatore SATURO**

**LA FORMA, e la correzione verificata sul codice:** `c_k = |satura(F_k)| / satura(amp * Somma_j |W_kj|)`. ### **Il denominatore e' SATURO**, e il motivo e' algebrico: `|satura(f)|` e' ### **monotona nel modulo**, quindi con questa forma ### **`c_k` sta in `[0,1]` e `c = 1` E' RAGGIUNGIBILE** — col denominatore ### **nudo** non lo sarebbe mai.

| passo | `c_k` mediana | MATERIA | BORDO | VUOTO | ### **`AUC` MAT/VUOTO** | fuori da `[0,1]` |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | 0.1841 | 0.7904 | 0.1925 | 0.1627 | ### **0.9992** | 0 |
| `150` | 0.2747 | 0.6483 | 0.2974 | 0.2430 | ### **0.9861** | 0 |
| `230` | 0.3001 | 0.4847 | 0.3257 | 0.2665 | ### **0.9023** | 0 |
| `300` | 0.2925 | 0.3870 | 0.3050 | 0.2744 | ### **0.7371** | 0 |
| `400` | 0.2930 | 0.2882 | 0.2856 | 0.2972 | ### **0.4679** | 0 |
| `500` | 0.2967 | 0.2761 | 0.2916 | 0.3019 | ### **0.4497** | 0 |
| `700` | 0.2972 | 0.2889 | 0.2912 | 0.3034 | ### **0.4638** | 0 |
| `1000` | 0.2990 | 0.2875 | 0.2844 | 0.3123 | ### **0.4415** | 0 |

> ### **`AUC = 0.5` VUOL DIRE NESSUNA SEPARAZIONE.** Qui l'`AUC` e' la probabilita' che un nodo di MATERIA preso a caso abbia `c_k` ### **piu' alto** di un nodo di VUOTO preso a caso.

**E IL SECONDO ASSE CHIESTO DAL MANDATO, il NUMERO DI VICINI** *(secchi dichiarati prima: `0-20`, `21-40`, `41-60`, `61-80`, `81+`)*:

| passo | `0-20` | `21-40` | `41-60` | `61-80` | `81+` | grado medio |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | n/d | 0.1894 *(n=24)* | 0.1884 *(n=2485)* | 0.1747 *(n=4709)* | 0.1901 *(n=5584)* | 73.67 |
| `150` | n/d | 0.2429 *(n=24)* | 0.2721 *(n=2485)* | 0.2693 *(n=4709)* | 0.2822 *(n=5584)* | 73.67 |
| `230` | 0.4635 *(n=11)* | 0.2409 *(n=24)* | 0.2813 *(n=2485)* | 0.2903 *(n=4709)* | 0.3189 *(n=5584)* | 73.61 |
| `300` | 0.7005 *(n=48)* | 0.2704 *(n=24)* | 0.2797 *(n=2484)* | 0.2854 *(n=4705)* | 0.3030 *(n=5589)* | 73.41 |
| `400` | 0.8075 *(n=103)* | 0.2986 *(n=24)* | 0.3088 *(n=2484)* | 0.2891 *(n=4702)* | 0.2875 *(n=5592)* | 73.10 |
| `500` | 0.8328 *(n=207)* | 0.2867 *(n=24)* | 0.3108 *(n=2484)* | 0.2936 *(n=4697)* | 0.2886 *(n=5597)* | 72.54 |
| `700` | 0.9550 *(n=451)* | 0.2957 *(n=23)* | 0.3095 *(n=2485)* | 0.2920 *(n=4689)* | 0.2845 *(n=5605)* | 71.25 |
| `1000` | 0.9959 *(n=827)* | 0.3096 *(n=23)* | 0.3016 *(n=2481)* | 0.2869 *(n=4679)* | 0.2830 *(n=5619)* | 69.36 |

> ### ⚠ **UNA DICHIARAZIONE, invece di un silenzio:** numeratore e denominatore vengono dallo ### **STESSO `w`**, ricalcolato dopo il passo, mentre `net.psi` e' stato calcolato ### **DENTRO** il passo. ### **Sono due istanti diversi**, e lo scarto massimo fra `|net.psi|` e il mio numeratore vale ### **`0.6780`** — si riporta invece di essere taciuto.

---

## `M3` — **QUANTO OSCILLA OGNI CANDIDATO AL <<VERSO>>**

> ### ⛔ **E' LA LETTURA CHE CONTA, perche' col dipolo che entra COME VARIAZIONE un verso GIUSTO ma che OSCILLA inietterebbe `±π` esattamente come adesso.** ### **Il riferimento e' `perc_geom`: il verso di OGGI.**

### `A` — **DUE letture, e il mandato ne nomina una sola**

`tw` e' orientata `i -> j` *(verificato dal codice)*. Quindi:

> ### ⛔ **E QUI AVEVO SCRITTO UNA PREMESSA FALSA: <<tutti gli archi hanno `i < j`>>.** Era misurata ai passi `0`, `1` e `2`, cioe' ### **prima della prima nascita**, e la corsa precedente si e' ### **FERMATA al passo `229`** su `9` archi fuori convenzione. ### **Ogni nascita ne produce ESATTAMENTE uno**: alla mitosi nascono `a-m` e `m-b` col nodo nuovo `m` di indice ### **piu' alto**, quindi `m-b` ha `i > j` ### **sempre.** ### ✔ **Adesso il conto NON si assume: si MISURA a ogni passo** -- `1`: 0, `150`: 0, `230`: 11, `300`: 48, `400`: 103, `500`: 207, `700`: 451, `1000`: 826 -- e la chiave d'arco e' ### **canonica `(min, max)`**, col segno della circolazione ### **letto dall'arco** invece che dedotto.

| | |
|---|---|
| `A` ### **GREZZA** | `Σ tw` col segno ### **MEMORIZZATO** — ### ⛔ **dipende dalla NUMERAZIONE** |
| `A` ### **DIVERGENZA** | col segno ### **relativo al nodo**: il ### **flusso uscente**, ben definito — ### **e non e' una circolazione** |

| passo | nodi | `A` grezza: cambi | frazione | `A` divergenza: cambi | frazione | ### **`perc_geom`: cambi** | ### **frazione** | `A` grezza `= 0` |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 12802 | 0 | 0.00 % | 0 | 0.00 % | ### **6419** | ### **50.14 %** | 12802 |
| `150` | 12802 | 35 | 0.27 % | 35 | 0.27 % | ### **0** | ### **0.00 %** | 0 |
| `230` | 12811 | 34 | 0.27 % | 30 | 0.23 % | ### **1** | ### **0.01 %** | 2 |
| `300` | 12850 | 42 | 0.33 % | 29 | 0.23 % | ### **2** | ### **0.02 %** | 0 |
| `400` | 12905 | 41 | 0.32 % | 36 | 0.28 % | ### **5** | ### **0.04 %** | 2 |
| `500` | 13009 | 60 | 0.46 % | 50 | 0.38 % | ### **9** | ### **0.07 %** | 2 |
| `700` | 13253 | 35 | 0.26 % | 51 | 0.38 % | ### **21** | ### **0.16 %** | 0 |
| `1000` | 13629 | 81 | 0.59 % | 64 | 0.47 % | ### **72** | ### **0.53 %** | 2 |

### ⭐ **LA SPINTA INIETTATA -- IL METRO GIUSTO**

> ### ⛔ **CONTARE QUANTI SEGNI CAMBIANO NON E' IL METRO**, e il referto `d60b987` l'aveva sbagliato: per ### **`D`** e ### **`MEM`** il dipolo e' ### **continuo** *(un valore che passa per zero non inietta niente)*, per ### **`A`** ogni cambio e' un ### **salto di `pi`**, e ### **`perc_geom`** cambia ### **per NODO** dove ogni nodo tocca ### **~`74` archi.** ### ✔ **La somma di `|Delta dipolo|` e' l'unica grandezza che le mette tutte nella STESSA unita'.**

**LE QUATTRO FORME, dichiarate:** `perc_geom` = `pi*0.5*(chi_i - chi_j)` con `chi = _chi_geom_nodi` *(la legge di OGGI)* - `A` = il segno della somma GREZZA sul nodo - `D` = `pi*tanh(tw/PHI_CRIT)` *(per arco, continua)* - ### **`MEM`** = `pi*tanh(delta/PHI_CRIT)` con `delta = twp - tw` *(### **la stessa forma di `D` con la MEMORIA al posto dell'istante**)*.

| l'opzione | ### **totale sulla corsa** | ### **MEDIANA per passo** | passi |
|---|--:|--:|--:|
| ### **`perc_geom`** *(la legge di oggi)* | 3.02e+06 | ### **1457.70** | 999 |
| `A` | 1.10e+07 | ### **10122.21** | 999 |
| `D` | 5.86e+06 | ### **5609.09** | 999 |
| `MEM` | 1.05e+07 | ### **10450.79** | 999 |

> ### ⚠ **LA MEDIANA CONTA PIU' DEL TOTALE, e il motivo e' misurato:** nei primi passi le spinte sono ### **ordini di grandezza** sopra il regime *(il transitorio in cui `tw` diventa non nullo)*. ### **Un totale dominato da un transitorio dice del transitorio.**

**E PER PASSO, ai passi della misura:**

| passo | `perc_geom` | `A` | `D` | ### **`MEM`** | archi maturi |
|--:|--:|--:|--:|--:|--:|
| `1` | n/d | n/d | n/d | ### **n/d** | 0 |
| `150` | 0.00 | 8117.88 | 3954.68 | ### **6838.96** | 471564 |
| `230` | 144.51 | 8205.84 | 4216.16 | ### **7086.91** | 471576 |
| `300` | 144.51 | 9245.71 | 4473.22 | ### **7971.87** | 471630 |
| `400` | 512.08 | 8017.34 | 4991.04 | ### **9135.40** | 471698 |
| `500` | 1950.93 | 11162.08 | 5530.19 | ### **10538.55** | 471836 |
| `700` | 1809.56 | 7564.96 | 5779.25 | ### **12083.22** | 472156 |
| `1000` | 9534.73 | 15667.12 | 7890.37 | ### **15435.65** | 472649 |

> ### ⚠ **E GLI ARCHI AL LORO PRIMO PASSO SONO ESCLUSI, per TUTTE e quattro le opzioni:** al primo passo di un arco `twp` e `twp_dip` ### **non sono ancora stati scritti dalla dinamica**, quindi una differenza fra il primo e il secondo passo ### **misura l'inizializzazione, non la dinamica.** ### **E' la stessa ragione per cui il simulatore mette `NaN` in `twp_dip`.**

### `MEM` -- **la stabilita' del segno di `delta`, e la frazione sopra `2pi`**

| passo | archi confrontabili | cambi di `sign(delta)` | frazione | ### **`|tw| > 2pi`** |
|--:|--:|--:|--:|--:|
| `1` | 471564 | 471564 | 100.00 % | ### **0.00 %** |
| `150` | 471564 | 1661 | 0.35 % | ### **0.11 %** |
| `230` | 471576 | 1712 | 0.36 % | ### **0.72 %** |
| `300` | 471630 | 1930 | 0.41 % | ### **1.39 %** |
| `400` | 471702 | 2181 | 0.46 % | ### **2.59 %** |
| `500` | 471840 | 2381 | 0.50 % | ### **3.77 %** |
| `700` | 472156 | 2688 | 0.57 % | ### **5.56 %** |
| `1000` | 472653 | 3308 | 0.70 % | ### **7.64 %** |

### `D` — **il segno di `tw` SULL'ARCO**, confrontato ### **per CHIAVE `(i,j)`**

> ### ⚠ **PER CHIAVE E NON PER INDICE**, perche' alla mitosi `i = concat([i[keep], a, m])` ### **rimescola gli indici**: un confronto per indice conterebbe cambi che non ci sono. ### **E gli archi non confrontabili si CONTANO.**

| passo | archi | ### **con `i > j`** | confrontabili | nuovi | cambi di `sign(tw)` | frazione |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | 471564 | ### **0** | 471564 | 0 | 0 | 0.00 % |
| `150` | 471564 | ### **0** | 471564 | 0 | 1144 | 0.24 % |
| `230` | 471580 | ### **11** | 471576 | 4 | 1211 | 0.26 % |
| `300` | 471630 | ### **48** | 471630 | 0 | 1216 | 0.26 % |
| `400` | 471702 | ### **103** | 471702 | 0 | 1251 | 0.27 % |
| `500` | 471840 | ### **207** | 471840 | 0 | 1313 | 0.28 % |
| `700` | 472156 | ### **451** | 472156 | 0 | 1298 | 0.27 % |
| `1000` | 472653 | ### **826** | 472653 | 0 | 1321 | 0.28 % |

> ### ✔ **E IL SEGNO SI CONFRONTA RIDOTTO AL VERSO CANONICO `min -> max`:** `tw` e' una ### **1-forma orientata**, quindi confrontare `sign(tw)` fra due passi senza quella riduzione ### **conterebbe un cambio di segno dove e' cambiata solo la SCRITTURA dell'arco.**

**E `A` E `D` SI PRENDONO A OGNI PASSO, non solo ai quattro** *(costano poco)*, quindi si puo' dare ### **la media su tutta la corsa**:

| | passi | frazione media per passo |
|---|--:|--:|
| `A` grezza | 1000 | ### **0.47 %** |
| `D` segno di `tw` | 1000 | ### **0.40 %** |
| ### **`perc_geom`** *(il riferimento di oggi)* | 1000 | ### **0.18 %** |

### `C` — **l'OLONOMIA DI FASE sulla base dei cicli**

> ### ⛔ **LA CONVENZIONE DEL `verso` L'HO MISURATA, NON DEDOTTA:** il cammino e' `u -> lca -> v -> u` e ### **la chiusura si percorre `v -> u` mentre il suo `verso` e' registrato `+1`**, cioe' opposto. ### **La via primaria e' `_vertici_ciclo`**, che chiude il ciclo per costruzione; quella sugli archi resta come ### **controllo indipendente.**

| passo | cicli | ### **olonomia non nulla** | frazione | `|k|` max | scarto dal multiplo di `4π` | ### **le due vie: modulo** | ### **segno discorde** | base cambiata |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 256 | ### **122** | 47.66 % | 2 | 5.33e-15 | 7.11e-15 | ### **122** | 0 su 256 (0.00 %) |
| `150` | 256 | ### **171** | 66.80 % | 3 | 7.11e-15 | 1.42e-14 | ### **171** | 0 su 256 (0.00 %) |
| `230` | 256 | ### **189** | 73.83 % | 4 | 1.42e-14 | 2.13e-14 | ### **189** | 0 su 256 (0.00 %) |
| `300` | 256 | ### **143** | 55.86 % | 2 | 3.55e-15 | 7.11e-15 | ### **143** | 0 su 256 (0.00 %) |
| `400` | 256 | ### **65** | 25.39 % | 1 | 4.44e-15 | 3.55e-15 | ### **65** | 0 su 256 (0.00 %) |
| `500` | 256 | ### **167** | 65.23 % | 2 | 7.11e-15 | 7.11e-15 | ### **167** | 0 su 256 (0.00 %) |
| `700` | 256 | ### **112** | 43.75 % | 3 | 7.11e-15 | 1.42e-14 | ### **112** | 0 su 256 (0.00 %) |
| `1000` | 256 | ### **106** | 41.41 % | 3 | 1.42e-14 | 1.07e-14 | ### **106** | 0 su 256 (0.00 %) |

> ### ✔ **L'ALGEBRA DELL'OBIEZIONE `(b)` E' CONFERMATA DAL NUMERO, non assunta:** su un ciclo chiuso la somma di `(phi_i - phi_j)` telescopia a `0` esatto e `_wphi` avvolge sul periodo `4π`, quindi l'olonomia ### **deve** essere un multiplo intero di `4π`. ### **Scarto massimo misurato: `1.42e-14`.**
>
> ### ⛔ **E IL SEGNO DELL'OLONOMIA NON E' DETERMINATO DAL GRAFO:** le due vie concordano sul ### **MODULO** e ### **discordano sul SEGNO** su ### **TUTTI** i cicli con olonomia non nulla, a ### **ogni** passo misurato *(122, 171, 189, 143, 65, 167, 112, 106 su 122, 171, 189, 143, 65, 167, 112, 106)*. ### **Due routine DEL SIMULATORE scelgono versi opposti sullo STESSO ciclo** — ed e' precisamente l'arbitrarieta' che l'obiezione `(a)` attribuisce all'opzione `C`.

---

## `M4` — **LE PLAQUETTE** *(l'opzione `P` di Luca)*

**La plaquette:** un triangolo coi ### **tre archi presenti.** La circolazione sul cammino `u -> v -> w -> u` e' `tw[(u,v)] + tw[(v,w)] - tw[(u,w)]`, e ### **il meno c'e' perche' l'ultimo tratto va contro la convenzione `i < j`.**

> ### ✔ **E IL SEGNO DI UNA SINGOLA PLAQUETTE E' ARBITRARIO, IL PRODOTTO COL VERSORE NO:** scambiando due vertici la circolazione cambia segno ### **e la normale anche**, quindi il prodotto ### **`(Σ tw) · n̂` e' INVARIANTE mentre ciascun fattore da solo NON LO E'.** ### **Per questo `(b)` misura il MODULO e `(c)` il VETTORE** — e ### **`R_k` resta un ASSE: l'invarianza non regala il segno.**

### `(a)` **quante, e quanto costano**

| passo | ### **plaquette** | conto ### **indipendente** | degeneri | archi `i > j` | cappi esclusi | nodi senza plaquette | `s` enumerazione | `s` controllo | MATERIA | BORDO | VUOTO |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **5534011** | 5534011 | 0 | ### **0** | 0 | 0 | 6.16 | 0.36 | 1505 | 1495 | 1330 |
| `150` | ### **5534011** | 5534011 | 0 | ### **0** | 0 | 0 | 5.50 | 0.35 | 1505 | 1496 | 1331 |
| `230` | ### **5533797** | 5533797 | 0 | ### **11** | 0 | 11 | 5.67 | 0.45 | 1502 | 1494 | 1333 |
| `300` | ### **5532866** | 5532866 | 0 | ### **48** | 0 | 48 | 5.81 | 0.40 | 1498 | 1490 | 1338 |
| `400` | ### **5531576** | 5531576 | 0 | ### **103** | 0 | 103 | 5.52 | 0.48 | 1495 | 1484 | 1341 |
| `500` | ### **5529206** | 5529206 | 0 | ### **207** | 0 | 207 | 5.87 | 0.38 | 1488 | 1479 | 1338 |
| `700` | ### **5523385** | 5523385 | 0 | ### **451** | 0 | 451 | 6.53 | 0.42 | 1482 | 1460 | 1330 |
| `1000` | ### **5514828** | 5514828 | 0 | ### **826** | 0 | 827 | 7.97 | 0.59 | 1459 | 1435 | 1341 |

*(Le tre colonne di classe sono la ### **MEDIANA delle plaquette per nodo**.)*

> ### ✔ **IL CONTO INDIPENDENTE:** coincide a tutti i passi. Per ogni arco il numero di ### **vicini comuni** e' il numero di triangoli che passano per quell'arco, e sommato sugli archi orientati ogni triangolo si conta ### **sei volte.** ### **Non passa da nessuna chiave**, quindi non condivide nessun difetto con l'enumerazione — e ### ⛔ **in costruzione ha trovato un traboccamento `int32` che faceva sparire il `97 %` dei triangoli IN SILENZIO.**

### `(b)` **`|Σ tw|` sulle plaquette**, per classe

| passo | campione | q05 | q25 | ### **q50** | q75 | q95 | max | MATERIA *(media per nodo)* | BORDO | VUOTO |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 190835 | 0.0000 | 0.0000 | ### **0.0000** | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `150` | 190835 | 0.0255 | 0.1530 | ### **0.3916** | 0.8488 | 1.9249 | 6.1652 | 0.2928 | 0.5196 | 0.6143 |
| `230` | 190826 | 0.0374 | 0.2168 | ### **0.5348** | 1.1089 | 2.4017 | 9.0680 | 0.3889 | 0.6832 | 0.8117 |
| `300` | 190795 | 0.0483 | 0.2709 | ### **0.6563** | 1.3129 | 2.7518 | 9.6969 | 0.4658 | 0.8030 | 0.9611 |
| `400` | 190750 | 0.0642 | 0.3452 | ### **0.8093** | 1.5758 | 3.1930 | 9.8711 | 0.6768 | 0.9813 | 1.1298 |
| `500` | 190668 | 0.0805 | 0.4208 | ### **0.9477** | 1.7966 | 3.5429 | 12.2582 | 0.9934 | 1.1558 | 1.2437 |
| `700` | 190467 | 0.1025 | 0.5305 | ### **1.1750** | 2.1649 | 4.1121 | 10.2323 | 1.3637 | 1.4177 | 1.4325 |
| `1000` | 190174 | 0.1207 | 0.6231 | ### **1.3873** | 2.5452 | 4.6387 | 11.0423 | 1.6341 | 1.6479 | 1.6609 |

*(I quantili vengono da un sottocampione a ### **passo PRIMO fisso** `29`: ### **deterministico, nessun RNG, nessun seme da dichiarare.**)*

### `(c)` **LA COERENZA `|Σ v| / Σ |v|`** — `0` disordine, `1` stesso asse

| passo | MATERIA | BORDO | VUOTO | MATERIA q25-q75 | VUOTO q25-q75 | nodi senza `R` definito |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **n/d** | n/d | ### **n/d** | n/d - n/d | n/d - n/d | 0 |
| `150` | ### **0.0313** | 0.0339 | ### **0.0360** | 0.0204 - 0.0475 | 0.0227 - 0.0579 | 0 |
| `230` | ### **0.0395** | 0.0448 | ### **0.0446** | 0.0252 - 0.0579 | 0.0297 - 0.0669 | 11 |
| `300` | ### **0.0510** | 0.0551 | ### **0.0543** | 0.0343 - 0.0745 | 0.0365 - 0.0798 | 48 |
| `400` | ### **0.0564** | 0.0572 | ### **0.0613** | 0.0375 - 0.0802 | 0.0405 - 0.0911 | 103 |
| `500` | ### **0.0618** | 0.0568 | ### **0.0643** | 0.0407 - 0.0885 | 0.0423 - 0.0986 | 207 |
| `700` | ### **0.0645** | 0.0594 | ### **0.0710** | 0.0403 - 0.0976 | 0.0450 - 0.1091 | 451 |
| `1000` | ### **0.0612** | 0.0616 | ### **0.0817** | 0.0380 - 0.0960 | 0.0504 - 0.1247 | 827 |

> ### ⚠ **E UN NODO SENZA NESSUNA PLAQUETTE NON DEGENERE HA COERENZA `NaN`, NON `0`:** un `0` li' vorrebbe dire *«disordine totale»* mentre la verita' e' *«non definita»*. ### **E' la famiglia di `CHI-TORS-ZERO-FALSO`, e il collaudo me l'ha trovato addosso.**

### `(d)` **il coseno fra `R_k` e l'asse di Bloch `_nb`** — *e `P2` dipende da qui*

**IL CASO NULLO E' ANALITICO, non simulato:** fra due assi indipendenti in `3D` il coseno e' ### **UNIFORME su `[-1,1]`**, quindi ### **media `0`** e ### **frazione con `|cos| > 0.5` pari a `0.5`.**

| passo | media MATERIA | media BORDO | media VUOTO | `|cos|>0.5` MATERIA | BORDO | VUOTO | ### **atteso dal caso** |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | n/d | n/d | n/d | n/d | n/d | n/d | media `0.0`, frazione `0.5` |
| `150` | 0.0022 | -0.0152 | 0.0013 | 0.5157 | 0.5051 | 0.4994 | media `0.0`, frazione `0.5` |
| `230` | -0.0338 | 0.0041 | -0.0078 | 0.5070 | 0.4932 | 0.4930 | media `0.0`, frazione `0.5` |
| `300` | -0.0128 | -0.0019 | -0.0115 | 0.4969 | 0.5017 | 0.4985 | media `0.0`, frazione `0.5` |
| `400` | -0.0145 | -0.0039 | -0.0023 | 0.4987 | 0.4948 | 0.4966 | media `0.0`, frazione `0.5` |
| `500` | -0.0018 | 0.0016 | 0.0036 | 0.5165 | 0.4817 | 0.5083 | media `0.0`, frazione `0.5` |
| `700` | -0.0116 | 0.0119 | -0.0090 | 0.4962 | 0.5016 | 0.5078 | media `0.0`, frazione `0.5` |
| `1000` | 0.0034 | -0.0118 | -0.0089 | 0.5061 | 0.5069 | 0.5017 | media `0.0`, frazione `0.5` |

### `(e)` **LA STABILITA': di quanto ruota `R_k` fra due passi**

| passo | contro il passo | nodi | ### **angolo mediano (gradi)** MATERIA | BORDO | VUOTO | nodi senza `R` | ### **riferimento: `perc_geom` cambia** |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | `0` | 12802 | ### **n/d** | n/d | n/d | 12802 | ### **50.14 %** |
| `150` | `149` | 12802 | ### **0.40** | 0.53 | 0.67 | 0 | ### **0.00 %** |
| `230` | `229` | 12811 | ### **0.56** | 0.64 | 0.82 | 9 | ### **0.01 %** |
| `300` | `299` | 12850 | ### **0.64** | 0.67 | 0.72 | 48 | ### **0.02 %** |
| `400` | `399` | 12905 | ### **0.81** | 0.71 | 0.70 | 103 | ### **0.04 %** |
| `500` | `499` | 13009 | ### **0.69** | 0.73 | 0.70 | 207 | ### **0.07 %** |
| `700` | `699` | 13253 | ### **0.67** | 0.72 | 0.69 | 451 | ### **0.16 %** |
| `1000` | `999` | 13629 | ### **0.69** | 0.70 | 0.63 | 827 | ### **0.53 %** |

> ### ⚠ **E I PASSI CAMPIONATI NON SONO PASSI MEDI, per il RIFERIMENTO:** su tutta la corsa `perc_geom` cambia ### **0.18 %** dei nodi per passo, mentre ai passi della misura cambia `150`: 0.00 %, `230`: 0.01 %, `300`: 0.02 %, `400`: 0.04 %, `500`: 0.07 %, `700`: 0.16 %, `1000`: 0.53 %. ### **Il confronto di `(e)` va letto sapendo questo**: ai quattro passi scelti il riferimento e' ### **piu' QUIETO** della sua media.
>
> ### **L'ANGOLO E IL RIFERIMENTO MISURANO DUE COSE DIVERSE, e lo dico perche' non si confondano:** l'angolo e' ### **CONTINUO** *(di quanto ruota un asse)*, la frazione di `perc_geom` e' ### **DISCRETA** *(quanti nodi cambiano valore)*. ### **Non sono la stessa grandezza e non si sottraggono** — stanno accanto perche' il mandato chiede il confronto, e ### **il confronto e' fra due letture, non fra due numeri.**

---

# ⭐ **L'INERZIA DEGLI OSSERVATORI ATTRAVERSO LE NASCITE** *(il controllo di Luca, senza una corsa in piu')*

Il riferimento e' ### **`amp0.json`** *(blob `cf2a1ac8`)*, il braccio `_AMP = 0` su ### **`1000` passi in comune**, confrontato con la corsa osservata *(blob `b8c21049`)*.

> ### ⛔ **IL CRITERIO E' DI LUCA, fissato prima di guardare:** ### **zero differenze su tutti i `1000` passi** = gli osservatori, involucri compresi, ### **non cambiano la dinamica**; ### **una differenza** = il primo passo diverso e il campo vanno qui, e ### **i numeri di `A1` dopo quel passo NON VALGONO.**

| campo | allineamento | differenze | era quello previsto dalla derivazione? |
|---|--:|--:|---|
| `n` | ### **`rif[k] = oss[k+0]`** | ### **0** | ### ⭐ **SI** *(`+0`)* |
| `archi` | ### **`rif[k] = oss[k-1]`** | ### **0** | ### ⭐ **SI** *(`-1`)* |
| la ### **forbice** su `q_tw` | `dec = -1` | ### **0 fuori forbice su 1000** | *(e' una FORBICE, non un'uguaglianza)* |

**E GLI ALTRI ALLINEAMENTI, per dire che lo zero NON e' un caso:**

| | differenze |
|---|--:|
| `archi@+0` | 391 |
| `archi@+1` | 574 |
| `archi@-1` | 0 |
| `n@+0` | 0 |
| `n@+1` | 391 |
| `n@-1` | 391 |

> ### ✔ **IL CRITERIO DI LUCA E' SODDISFATTO: ZERO differenze su `1000` passi.** ### **Gli osservatori, INVOLUCRI DI NASCITA COMPRESI, non cambiano la dinamica** -- e ### **i numeri di `A1` qui sotto valgono per tutti i `1000` passi.**

> ### ⚠ **E I CAMPI CHE `A1` NON REGISTRA SONO DICHIARATI:** `nati_tot`, `schwinger_tot`, `q_tw`. ### **Si confrontano `n` e `archi`, e non sono poco:** `n` e' ### **il conto delle nascite integrato** e `archi` risente ### **sia della mitosi** *(`-1 +2`)* ### **sia dello Schwinger** *(`+2`)* -- ### **uno spostamento di UNA nascita di UN passo si vedrebbe in entrambi.**

---

# `M5` -- **LE MEMORIE**

## `(a)` **`c0` CONGELATO contro `c_delta` VIVO**

`c0 = cos(phi0_i - phi0_j)` e' la ### **memoria CONGELATA dei legami** *(`phi0` ha `5` scritture, tutte alla nascita)*; `c_delta = cos(dph - tw)` e' la ### **memoria VIVA** dentro `tw`.

> ### ⛔ **IL CRITERIO, fissato PRIMA:** *<<`phi0` e' memoria MORTA>>* se `Spearman(c0, c_delta) < 0.3` sugli archi ### **VUOTO di eta' > 2 tau_tw**; *<<`phi0` come `delta`>>* se ### **`> 0.8`**; fra i due ### **AMBIGUO.**

| passo | ### **Spearman del CRITERIO** | archi | esito |
|--:|--:|--:|---|
| `1` | ### **n/d** | 0 | n/d: ### **nessun arco** |
| `150` | ### **-0.0435** | 17174 | ### ✔ **MORTA** |
| `230` | ### **0.0076** | 62636 | ### ✔ **MORTA** |
| `300` | ### **0.0102** | 103878 | ### ✔ **MORTA** |
| `400` | ### **6.50e-04** | 138781 | ### ✔ **MORTA** |
| `500` | ### **1.09e-04** | 161099 | ### ✔ **MORTA** |
| `700` | ### **-3.35e-04** | 178043 | ### ✔ **MORTA** |
| `1000` | ### **0.0022** | 183067 | ### ✔ **MORTA** |

**LE ORIGINI REGISTRATE**, e ### **si dichiarano PRIMA della tavola per origine**, perche' una riga <<per origine>> con zero archi di quell'origine ### **non e' una misura:**

| origine | archi |
|---|--:|
| `seminato` | ### **471564** |
| `divisione` | ### **1130** |
| `schwinger` | ### **524** |
| ### **da NASCITA, in tutto** | ### **1654** |

> ### ✔ **L'INVOLUCRO HA LAVORATO: `1654` archi etichettati da una NASCITA.** ### **La riga per origine si puo' leggere.**

> ### ✔ **E NESSUN ARCO SENZA ORIGINE, a nessun passo:** ogni arco e' ### **o seminato o nato da un evento avvolto.** ### ⚠ **E questo numero PUO' essere diverso da zero** -- e' il conteggio che ha preso il posto dell'involucro MORTO di `_allaccia`, non un posto vuoto.

**E PER CLASSE, PER ORIGINE E PER ETA'** *(la dipendenza dall'eta' si riporta perche' il taglio `> 2 tau_tw` e' UNO, e un taglio solo non si puo' rileggere)*:

*(all'ultimo passo misurato: `1000`)*

| | Spearman | archi |
|---|--:|--:|
| classe ### **MATERIA** | 0.0024 | 97722 |
| classe ### **BORDO** | -0.0033 | 158639 |
| classe ### **VUOTO** | 0.0025 | 216292 |
| origine `seminato` | 8.92e-04 | 471003 |
| origine `divisione` | -0.0553 | 1127 |
| origine `schwinger` | 0.0180 | 523 |
| origine `?` | n/d | 0 |
| eta' `0.0-0.5` x `tau_tw` | -0.0023 | 19406 |
| eta' `0.5-1.0` x `tau_tw` | 0.0059 | 19367 |
| eta' `1.0-2.0` x `tau_tw` | 2.86e-04 | 38272 |
| eta' `2.0-5.0` x `tau_tw` | 0.0044 | 105612 |
| eta' `5.0-inf` x `tau_tw` | -6.20e-04 | 289996 |

## `(b)` **QUANTA PARTE DI `tw` VIENE DAL DIPOLO**

> ### ⛔ **IL CRITERIO, fissato PRIMA:** *<<il dipolo DOMINA `delta`>>* se la ### **mediana** di `|tw_dip|/|tw|` ### **supera `0.5`.** ### ⚠ **E se dominasse, `MEM-VERSO` leggerebbe SE STESSA: non sarebbe una cura, sarebbe un anello.**

| passo | mediana | q05-q95 | con un salto nei `50` passi prima | archi | esito |
|--:|--:|--:|--:|--:|---|
| `1` | ### **0.0000** | 0.0000 - 3.14e+12 | n/d | 0 | ### ✔ **non domina** |
| `150` | ### **0.0000** | 0.0000 - 0.0026 | n/d | 0 | ### ✔ **non domina** |
| `230` | ### **0.0000** | 0.0000 - 0.0020 | 0.2751 | 285 | ### ✔ **non domina** |
| `300` | ### **2.25e-07** | 0.0000 - 0.0014 | 0.2622 | 633 | ### ✔ **non domina** |
| `400` | ### **4.76e-07** | 0.0000 - 9.10e-04 | 0.2497 | 1708 | ### ✔ **non domina** |
| `500` | ### **4.30e-07** | 0.0000 - 5.69e-04 | 0.2780 | 2255 | ### ✔ **non domina** |
| `700` | ### **1.47e-07** | 0.0000 - 2.09e-04 | 0.2478 | 3426 | ### ✔ **non domina** |
| `1000` | ### **2.25e-08** | 0.0000 - 0.0032 | 0.2289 | 9105 | ### ✔ **non domina** |

## `(c)` **IL DISORDINE CONGELATO**

| passo | quota di archi con `c0 < 0` | MATERIA | BORDO | VUOTO |
|--:|--:|--:|--:|--:|
| `1` | ### **46.53 %** | 0.0000 | 1.0000 | 1.0000 |
| `150` | ### **46.53 %** | 0.0000 | 0.0000 | 1.0000 |
| `230` | ### **46.53 %** | 0.0000 | 0.0000 | 1.0000 |
| `300` | ### **46.53 %** | 0.0000 | 0.0000 | 1.0000 |
| `400` | ### **46.53 %** | 0.0000 | 0.0000 | 1.0000 |
| `500` | ### **46.54 %** | 0.0000 | 0.0000 | 0.0000 |
| `700` | ### **46.54 %** | 0.0000 | 0.0000 | 0.0000 |
| `1000` | ### **46.54 %** | 0.0000 | 0.0000 | 0.0000 |

**E LE PLAQUETTE FRUSTRATE** *(il prodotto dei tre `c0` negativo: ### **non esiste un assegnamento di fasi che soddisfi i tre legami**, e ### **`c0` e' congelato, quindi quella frustrazione non si scioglie mai**)*:

| passo | frustrate | su | frazione | MATERIA | BORDO | VUOTO |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **1242840** | 5534011 | ### **22.46 %** | 0.0464 | 0.2415 | 0.2500 |
| `150` | ### **1242840** | 5534011 | ### **22.46 %** | 0.0466 | 0.2418 | 0.2500 |
| `230` | ### **1242787** | 5533797 | ### **22.46 %** | 0.0449 | 0.2406 | 0.2500 |
| `300` | ### **1242519** | 5532866 | ### **22.46 %** | 0.0507 | 0.2377 | 0.2500 |
| `400` | ### **1242125** | 5531576 | ### **22.46 %** | 0.0658 | 0.2381 | 0.2496 |
| `500` | ### **1241561** | 5529206 | ### **22.45 %** | 0.0815 | 0.2408 | 0.2491 |
| `700` | ### **1240235** | 5523385 | ### **22.45 %** | 0.1465 | 0.2431 | 0.2483 |
| `1000` | ### **1238366** | 5514828 | ### **22.46 %** | 0.2255 | 0.2437 | 0.2458 |

## `(d)` **IL BILANCIO DELLA TORSIONE: dove si dissipa**

La potenza persa nel rilassamento, ### **`somma di tw^2*dt_e/tau_tw` per passo**, per classe e ### **per NODO** *(meta' a ciascun estremo, che e' la proposta di `P-DECADIMENTO` e ### **una proposta, non una legge**)*.

> ### ⛔ **IL CRITERIO, fissato PRIMA:** *<<la dissipazione sta nel VUOTO>>* se la potenza ### **per nodo MEDIANA** in MATERIA e' ### **meno di UN QUARTO** di quella in VUOTO, ### **a TUTTI i passi pesanti dopo il `300`.** ### ⭐ **E' l'osservazione di Luca:** una memoria che dimentica dissipa ### **solo quando ha qualcosa da dimenticare.**

| passo | potenza totale | per nodo MATERIA | BORDO | VUOTO | MATERIA sotto 1/4? |
|--:|--:|--:|--:|--:|---|
| `1` | 0.00 | ### **0.0000** | 0.0000 | ### **0.0000** | n/d *(la potenza nel VUOTO e' zero: niente da dimenticare)* |
| `150` | 23775.34 | ### **0.3841** | 1.2225 | ### **1.5414** | ### ✔ **SI** |
| `230` | n/d | ### **0.5008** | 1.4395 | ### **n/d** | n/d *(una mediana e' `NaN`, e un `NaN` non e' un falso)* |
| `300` | 34831.61 | ### **0.8397** | 1.8012 | ### **2.2450** | ### ⛔ **NO** |
| `400` | 43794.84 | ### **1.8843** | 2.4877 | ### **2.6261** | ### ⛔ **NO** |
| `500` | 54634.17 | ### **3.1820** | 3.1740 | ### **3.0533** | ### ⛔ **NO** |
| `700` | 72062.46 | ### **4.2104** | 4.1207 | ### **4.0334** | ### ⛔ **NO** |
| `1000` | 91703.97 | ### **5.2288** | 5.1874 | ### **5.1395** | ### ⛔ **NO** |

> ### ⚠ **IL CRITERIO SUI PASSI DOPO IL `300` E' NON DECIDIBILE** *(decisione di Luca, 2026-10-07 sera)*, e ### **non perche' manchi un numero:** l'`AUC` MATERIA/VUOTO sta SOTTO `0.5` a 4 dei 4 passi che decidono *(il minimo: 0.4415 al passo `1000`)*, quindi le classi ### **non identificano struttura** e il confronto parla di ### **dove la materia ERA**.

> ### ⛔ **LA CONDIZIONE DEL TEST NON C'ERA.** L'osservazione di Luca dice che ### **la memoria non dissipa dove la struttura e' STABILE**, e le classi MATERIA/BORDO/VUOTO sono ### **GEOMETRICHE: dicono dove le masse sono state SEMINATE.** ### **I numeri della tavola restano e valgono; il VERDETTO aspetta masse che durano** *(`A-S1`)*.

> ### ⚠ **E UN NUMERO CHE IL CAMBIO DI ETICHETTA NON DEVE FAR PERDERE:** al passo `150` -- dove le masse ### **c'erano ancora** -- il criterio era soddisfatto ### **per un PELO.** ### **Quando `A-S1` dara' masse che durano, il numero da guardare e' se quel rapporto SCENDE o SALE.**

> ### ⚠ **E SE NON FOSSE SODDISFATTO NON SAREBBE UN DETTAGLIO:** vorrebbe dire che la torsione dissipa ### **dove la materia sta**, cioe' che il termine di rilassamento ### **non e' il costo di una memoria che rincorre** ma qualcos'altro.

---

## ⚠ **LE MIE PREVISIONI, CONTRO I NUMERI** — *e le stampa lo script*

Le previsioni sono fissate in `doc/TASK_HISTORY/2026-10-06_misura-verso-e-plaquette.md`, committato ### **prima della corsa** in `76b18ef`. ### **Qui le confronta il codice, non la mia buona volonta'** — e ### **il passo `1` non conta: era GIA' VISTO** *(il collaudo su `2` passi)*, quindi si guardano i passi ### **oltre il primo.**

| | la previsione | il numero | esito |
|---|---|---|---|
| `M1` | ### **`--chi-core` INERTE** per il dipolo | `(a)` e `(c)` valgono `0` su 7 passi su 7; il massimo del rapporto ### **SALE**: `0.061975`, `0.048300`, `0.074282`, `0.120083`, `0.129733`, `0.149377`, `0.130483` | ### ✔ **CONFERMATA** |
| `M2` | `c_k` ### **separa MATERIA da VUOTO** | `AUC` fra `0.4415` e `0.9861` *(`0.5` = nessuna separazione)* | ### ⛔ **SMENTITA** |
| `M3-A` | i cambi di segno ### **CALANO** coi passi | frazione per passo: `150` -> 0.27 %, `230` -> 0.27 %, `300` -> 0.33 %, `400` -> 0.32 %, `500` -> 0.46 %, `700` -> 0.26 %, `1000` -> 0.59 % | ### ⛔ **SMENTITA**: non e' monotona |
| `M3-C` | la base dei cicli ### **cambia molto** con le nascite | massimo cambiato: 0.00 %, con nascite | ### ⛔ **SMENTITA**: non cambia |
| `M4(c)` | la ### **COERENZA e' BASSA** | mediane per classe fra `0.0313` e `0.0817` *(soglia di <<bassa>>: `0.5`, il punto medio -- ### **e' una mia convenzione, DICHIARATA, non una misura**)* | ### ✔ **CONFERMATA** |
| `M4(d)` | `R_k` e `_nb` ### **SCORRELATI, come il caso** | scarto massimo dal caso nullo: la ### **media** del coseno a ### **2.04 sigma** dallo zero, la ### **frazione** `|cos| > 0.5` a ### **2.29 sigma** da `0.5`; tolleranza ### **3.24 sigma**, che e' ### **Bonferroni su 42 confronti** e non un numero scelto *(`sigma` e' ### **DERIVATO**: per un coseno uniforme su `[-1,1]` la varianza e' `1/3`, e per una frazione attorno a `0.5` e' `0.5/sqrt(n)`)* | ### ✔ **CONFERMATA** |
| `M4(e)` | `R_k` ### **ruota DI MOLTO** fra due passi, cioe' ### **NON e' stabile** | angolo mediano fra `0.40` e `0.82` gradi *(soglia di <<molto>>: `10` gradi -- ### **e' una mia convenzione, DICHIARATA**)* | ### ⛔ **SMENTITA** |
| `P1` | ### **`D` inietta la spinta MINORE** di tutte | mediane ai passi oltre il `216`: `perc_geom` 1160.82, `A` 8725.77, `D` 5260.62, `MEM` 9836.97 | ### ⛔ **SMENTITA**: la minore e' `perc_geom` |
| `P2` | ### **`MEM` inietta MENO di `A`** | `MEM` 9836.97 contro `A` 8725.77 | ### ⛔ **SMENTITA** |
| `P3` | ### ⚠ **NON SAPEVO l'ordine fra `A` e `perc_geom`**, e l'avevo scritto | l'ordine misurato, dal minore al maggiore: `perc_geom` < `D` < `A` < `MEM` | ### ✔ **ERA GIUSTO NON SAPERLO**: il numero decide, e lo scrivo |
| `P4` | la frazione con `|tw| > 2pi` ### **CRESCE** e all'ultimo passo sta fra ### **`15 %`** e ### **`25 %`** *(era una STIMA da interpolazione, non una misura)* | all'ultimo passo 7.64 %; monotona: SI | ### ⛔ **SMENTITA** |
| `P5` | le nascite per `100` passi stanno fra ### **`48`** e ### **`150`** | `827` nodi nuovi in `1000` passi, cioe' ### **82.7 per `100` passi** | ### ✔ **CONFERMATA** |
| `P6` | ### ⭐ **la base dei cicli NON CAMBIA** *(`~0 %`)* anche a `1000` passi e con migliaia di nascite | massimo cambiato: 0.00 % su 8 passi misurati | ### ✔ **CONFERMATA** |
| `M5a` | ### **`phi0` e' memoria MORTA** *(Spearman `< 0.3` su VUOTO con eta' `> 2 tau_tw`)* | il massimo sui passi oltre il `216`: 0.0102 *(su 6 passi)* | ### ✔ **CONFERMATA** |
| `M5b` | ### **il dipolo NON domina `delta`** *(mediana `< 0.5`)* | la mediana massima oltre il `216`: 4.76e-07 | ### ✔ **CONFERMATA** |
| `M5d` | ### ⭐ **l'osservazione di LUCA regge**: la dissipazione sta nel VUOTO *(MATERIA sotto un quarto di VUOTO, a TUTTI i passi dopo il `300`)* | 4 passi valutati, 0 soddisfatti | ### ⚠ **NON DECIDIBILE** *(decisione di Luca, 2026-10-07)*: l'`AUC` MATERIA/VUOTO sta SOTTO `0.5` a 4 dei 4 passi che decidono *(il minimo: 0.4415 al passo `1000`)*, quindi le classi ### **non identificano struttura** e il confronto parla di ### **dove la materia ERA**. ### **Il numero resta, il verdetto aspetta masse che durano.** |

> ### **7 confermate, 7 SMENTITE, 2 non decidibili.** ### **Le smentite sono il pezzo che vale:** una misura che conferma tutto quello che credevo ### **non mi ha insegnato niente.**

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
