# `H3` — **CHI SCALDA IL VUOTO: IL TERMOSTATO O LO SCUOTIMENTO?**

*Referto generato da `csv/_test_fork/_referto_termo_h3.py`. Dati: `csv/_test_fork/_termo_h3/`. Criteri, previsioni e aritmetica: `doc/TASK_HISTORY/2026-10-07_h3-termostato-e-scuotimento.md`, committato ### **PRIMA** dello strumento e delle corse.*

| braccio | passi | stato | secondi | che cosa gli è stato fatto |
|---|--:|---|--:|---|
| `base` | 300 su 300 | ### ✔ **completo** | 1605.3 | ### **niente** — è la dinamica di sempre |
| `B-T` | 500 su 500 | ### ✔ **completo** | 2461.9 | ### **`xi_termo` azzerata prima di ogni `step`.** ### ⛔ **NON è un azzeramento del termostato:** lo step lo ### **RICALCOLA** dentro di sé, quindi resta ### **un passo di accumulo invece di tutti** — si chiama ### **«termostato senza memoria»** |
| `B-S` | 500 su 500 | ### ✔ **completo** | 2403.9 | ### **`scuoti_vuoto` sostituita** con una funzione della stessa firma che ### **non fa niente** |
| `B-TS` | 500 su 500 | ### ✔ **completo** | 1867.1 | ### **I DUE INSIEME:** `scuoti_vuoto` inerte ### **e** `xi_termo` azzerata. ### **Il sistema vive solo della sua energia iniziale e della dinamica interna.** ### ⚠ **Eredita da `B-T` il non essere un azzeramento del termostato** |
| `B-SCAL` | 500 su 500 | ### ✔ **completo** | 2271.4 | ### **`D2`:** `_coppia_interferenza` prende il suo ### **RAMO SCALARE**, quello che dipende dalla ### **FASE CORRENTE** *(`z = e^{iφ}`)*. ### ⚠ **Il flag è spento SOLO durante la chiamata** e ripristinato in un `finally`: gira il ramo ### **del simulatore** |
| `B-SCAL-TS` | 500 su 500 | ### ✔ **completo** | 3294.4 | ### **`D2-BIS`: I TRE INSIEME** — `scuoti_vuoto` inerte, `xi_termo` azzerata ### **e** la coppia sul suo ### **RAMO SCALARE**. ### ⭐ **Nessun codice di intervento nuovo:** sono i due interventi ### **già sigillati** composti, e il collaudo verifica che per i cinque bracci di prima le condizioni valutino ### **IDENTICO** |
| `B-SCAL-TS-NOSYNC` | 500 su 500 | ### ✔ **completo** | 3184.2 | ### **`D2-TER`: I QUATTRO INSIEME** — i tre di `B-SCAL-TS` ### **più `K_SYNC = 0`**, messo dallo strumento sul modulo e ripristinato in un `finally`. ### ⭐ **E che sia UN SOLO interruttore è MISURATO**, non argomentato *(la tavola di `calcola_psi` qui sotto)* |

### ✔ **I FLAG CHE RENDONO VALIDA LA RICOSTRUZIONE, letti a runtime e non assunti**

| | |
|---|---|
| `TEMPO_SEGNO` | `False` |
| `FORK_SU2_MEM` | `True` |
| `REGIME` | `'deterministico'` |
| `CS_DINAMICO` | `True` |
| `M_PH` | `1.0` |
| `DT` | `0.01` |
| `G_PH` | `0.003` |

> ### ⭐ **`TEMPO_SEGNO = False`** → `dt_n_s = dt_n` esattamente; ### **`FORK_SU2_MEM = True`** → lo step ### **salva `_r_corrente`**, quindi `dt_n = DT·r` è leggibile; ### **`REGIME = 'deterministico'`** → gira il ramo del termostato e ### **mai quello di `G_PH`** — ed è il controllo che il mandato chiede per `B-T`.

---

# `(1)` ⭐ **IL BILANCIO DI `<phivel²>`: CHI SCALDA, E DI QUANTO**

> ### ⛔ **È UN'IDENTITÀ, NON UNA STIMA:**
> `p2² − p0² = [2p₀·Δscuoti + Δscuoti²] + [2p₁·Δterm] + [2p₁·Δcoppia] + Δstep²`
> ### ⚠ **E `Δstep²` è un RESIDUO INCROCIATO fra termostato e coppia: non si può attribuire, e si riporta come tale.**

## la classe ### **VUOTO**

| passo | ### **scuoti** | termostato | coppia | residuo | TOTALE | quota dello scuoti |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **0.000000** | 0.000070 | -0.001197 | 0.034680 | 0.033554 | ### **0.00 %** |
| `10` | ### **0.110144** | 0.002176 | 0.000191 | 0.000011 | 0.112521 | ### **97.89 %** |
| `25` | ### **0.258174** | 0.017360 | 0.000582 | 0.000033 | 0.276149 | ### **93.49 %** |
| `50` | ### **0.353364** | -0.007619 | 0.001845 | 0.000014 | 0.347604 | ### **97.39 %** |
| `100` | ### **0.507635** | -0.497528 | 0.002462 | 0.003178 | 0.015748 | ### **50.22 %** |
| `200` | ### **0.291682** | -0.271847 | 0.003506 | 0.001468 | 0.024808 | ### **51.31 %** |
| `300` | ### **0.428746** | -0.359981 | 0.018606 | 0.001924 | 0.089295 | ### **52.98 %** |

**LA SOMMA SUI PRIMI `50` PASSI** *(è lì che il riscaldamento avviene)*:

| voce | somma | quota |
|---|--:|--:|
| ### **`scuoti**` | 11.52034 | ### **94.39 %** |
| `termostato` | 0.61447 | ### **5.03 %** |
| `coppia` | 0.03491 | ### **0.29 %** |
| `residuo_incrociato` | 0.03583 | ### **0.29 %** |

> ### ⭐ **IL TERMOSTATO CAMBIA SEGNO, e questo e' il fatto che la quota in valore assoluto NASCONDE:** aggiunge energia su ### **48** passi *(il primo: `1`)* e la ### **TOGLIE** su ### **252** *(dal `49` in poi)*. ### ⛔ **Da li' FRENA**, e il totale di `Delta<phivel^2>` crolla: lo scuotimento inietta e il termostato ### **quasi lo annulla.** ### **Quindi non e' il riscaldatore: e' il FRENO.**

> ### ⛔ **LA VOCE PRINCIPALE NEL VUOTO, sui primi `50` passi, è `scuoti`** — con il ### **94.39 %** del totale in valore assoluto.

## la classe ### **MASSE**

| passo | ### **scuoti** | termostato | coppia | residuo | TOTALE | quota dello scuoti |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | ### **0.000000** | 0.000078 | 0.002487 | 0.042575 | 0.045140 | ### **0.00 %** |
| `10` | ### **0.007647** | 0.000544 | 0.001367 | 0.000017 | 0.009576 | ### **79.86 %** |
| `25` | ### **0.014442** | 0.001699 | 0.004837 | 0.000041 | 0.021019 | ### **68.71 %** |
| `50` | ### **0.054163** | -0.000761 | 0.019037 | 0.000106 | 0.072544 | ### **73.13 %** |
| `100` | ### **-0.002092** | -0.072557 | 0.047354 | 0.000165 | -0.027130 | ### **1.71 %** |
| `200` | ### **0.076378** | -0.064311 | 0.016045 | 0.000214 | 0.028326 | ### **48.66 %** |
| `300` | ### **0.263750** | -0.179558 | 0.010363 | 0.000881 | 0.095437 | ### **58.02 %** |

**LA SOMMA SUI PRIMI `50` PASSI** *(è lì che il riscaldamento avviene)*:

| voce | somma | quota |
|---|--:|--:|
| ### **`scuoti**` | 0.96694 | ### **68.32 %** |
| `termostato` | 0.06446 | ### **4.55 %** |
| `coppia` | 0.33878 | ### **23.94 %** |
| `residuo_incrociato` | 0.04504 | ### **3.18 %** |

> ### ⭐ **IL TERMOSTATO CAMBIA SEGNO, e questo e' il fatto che la quota in valore assoluto NASCONDE:** aggiunge energia su ### **48** passi *(il primo: `1`)* e la ### **TOGLIE** su ### **252** *(dal `49` in poi)*. ### ⛔ **Da li' FRENA**, e il totale di `Delta<phivel^2>` crolla: lo scuotimento inietta e il termostato ### **quasi lo annulla.** ### **Quindi non e' il riscaldatore: e' il FRENO.**

> ### ⛔ **LA VOCE PRINCIPALE NEL MASSE, sui primi `50` passi, è `scuoti`** — con il ### **68.32 %** del totale in valore assoluto.

---

# `(2)` **LE GRANDEZZE DEL TERMOSTATO, e `E_cin` è MOLTO sotto l'obiettivo**

| passo | `E_cin` | ### **`T_target`** | `err_rel` | ### **`xi_termo`** | `P_eq` | `cs_rappr` | `Λ` | `r` mediana |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `1` | 0.15631 | ### **5.4327** | -0.9712 | ### **-0.02271** | 1.86393 | 1.7072 | 4.3131 | 1.0000 |
| `10` | 0.69416 | ### **5.2793** | -0.8685 | ### **-0.17048** | 1.86840 | 1.6809 | 2.6834 | 0.8419 |
| `25` | 3.29960 | ### **4.9252** | -0.3301 | ### **-0.28001** | 1.82131 | 1.6444 | 3.1045 | 0.8229 |
| `50` | 11.32267 | ### **4.7252** | 1.3962 | ### **0.03624** | 1.80218 | 1.6192 | 3.6083 | 0.8100 |
| `100` | 18.31058 | ### **5.2074** | 2.5163 | ### **1.51585** | 1.93162 | 1.6419 | 2.9798 | 0.8205 |
| `200` | 12.14502 | ### **5.9405** | 1.0444 | ### **1.28976** | 2.18932 | 1.6472 | 2.3096 | 0.8239 |
| `300` | 16.39289 | ### **7.0697** | 1.3187 | ### **1.27711** | 2.46773 | 1.6926 | 2.5764 | 0.8456 |

### ⭐ **`T_target` CRESCE? E QUANTO VIENE DA `median(d0)`?**

`T_target = cs_rappr² · P_eq`, quindi ### **in logaritmo i due contributi si SOMMANO**: `ln(T₁/T₀) = 2·ln(cs₁/cs₀) + ln(P₁/P₀)`. ### **Così la quota è DEFINITA, non un'impressione.**

| dal passo `1` al `300` | valore | variazione | contributo a `ln(T₁/T₀)` |
|---|--:|--:|--:|
| `T_target` | `5.4327` → ### **`7.0697`** | ### **30.13 %** | — |
| ### **`P_eq = median(d0)`** | `1.86393` → `2.46773` | ### **32.39 %** | ### **106.54 %** |
| `cs_rappr` *(entra al QUADRATO)* | `1.7072` → `1.6926` | -0.86 % | -6.54 % |

> ### ⛔ **SÌ: `T_target` cresce, e la crescita viene PRINCIPALMENTE da `median(d0)`** *(il ### **106.54 %** di `ln(T₁/T₀)`)* — ed è il cricchetto che `D31` descrive.

> ### ⚠ **E LA QUOTA SUPERA IL `100` PER CENTO PERCHE' L'ALTRO TERMINE E' NEGATIVO, non per un errore:** `cs_rappr` ### **CALA** *(contributo -6.54 %)*, quindi `median(d0)` deve ### **compensarlo E produrre la crescita.** ### **Le due quote sommano a `100` per cento per costruzione**, ed e' il senso della scomposizione in logaritmo.

### ⚠ **IL CONTROLLO POSITIVO DELLA RICOSTRUZIONE, e NON è esatto**

Lo step fa `xi += dt_scal·(err_rel − xi)/tau_termo` e poi `clip(−2, 2)`. ### **Ricostruirlo verifica in un colpo `E_cin`, `P_eq`, `cs_rappr`, `T_target`, `tau_termo` e `dt_scal`.**

| | |
|---|--:|
| residuo ASSOLUTO massimo su `300` passi | ### **2.34e-04** |
| residuo RELATIVO massimo | ### **0.326 %** |

> ### ⛔ **LA RICOSTRUZIONE NON È AL BIT, E LO SCRIVO:** la causa probabile è che `d0` o `psi` cambino fra il mio punto di lettura e la riga `:7735` dove la legge li usa. ### ✔ **A questo livello le conclusioni QUALITATIVE — chi domina — non cambiano**, perché le voci del bilancio differiscono di ### **ordini di grandezza**; ### ⚠ **ma `T_target` ed `E_cin` portano quell'incertezza**, e un confronto fine fra loro non si può fare su questi numeri.

### ✔ **IL CONTROLLO POSITIVO DI `ampiezza`: `rms(Δscuoti)` contro `rms(ampiezza)`**

| passo | classe | `rms(Δscuoti)` | `rms(ampiezza)` | scarto |
|--:|---|--:|--:|--:|
| `1` | vuoto | 0.00005 | 0.00005 | 0.42 % |
| `1` | masse | 0.00001 | 0.00001 | 1.33 % |
| `50` | vuoto | 0.62306 | 0.62444 | 0.22 % |
| `50` | masse | 0.18789 | 0.19288 | 2.59 % |
| `300` | vuoto | 0.60300 | 0.60306 | 0.01 % |
| `300` | masse | 0.48422 | 0.47726 | 1.46 % |

> ### ✔ **Coincidono entro il rumore di campione**: `Δscuoti = normal(0,1)·ampiezza`, quindi ### **la mia ricostruzione della legge dello scuotimento è giusta** — e ### **`calcio` NON si ricalcola**, perché userebbe `net.rng`.

---

# `(3)` ⭐ **`Λ` È GLOBALE, E AGISCE DUE VOLTE** *(il punto `1` dell'integrazione)*

`ampiezza = √(stress + 1e-9) · √Λ / (1 + I2/Λ)`, con ### **`Λ = mean(|psi|²)` GLOBALE**. ### ➜ **Un `Λ` che cresce ALZA il calcio ovunque *(`×√Λ`)* E INDEBOLISCE la soppressione dove `I2` è alto *(`/(1+I2/Λ)`)* — cioè scioglie la protezione delle masse.**

| passo | `Λ` | `amp` mediana ### **VUOTO** | `amp` mediana ### **MASSE** | ### **rapporto masse/vuoto** | `I2` mediana masse |
|--:|--:|--:|--:|--:|--:|
| `1` | 4.3131 | 0.00005 | 0.00001 | ### **0.1652** | 28.3300 |
| `10` | 2.6834 | 0.32623 | 0.06137 | ### **0.1881** | 16.3838 |
| `25` | 3.1045 | 0.48852 | 0.10947 | ### **0.2241** | 16.8088 |
| `50` | 3.6083 | 0.60684 | 0.16434 | ### **0.2708** | 16.9837 |
| `100` | 2.9798 | 0.60067 | 0.16620 | ### **0.2767** | 13.7721 |
| `200` | 2.3096 | 0.52996 | 0.23224 | ### **0.4382** | 6.0454 |
| `300` | 2.5764 | 0.56278 | 0.42026 | ### **0.7468** | 3.7376 |

> ### ⭐ **IL RAPPORTO `masse/vuoto` DELL'AMPIEZZA È LA MISURA DELLA PROTEZIONE:** se SALE verso `1`, la soppressione ### **si sta sciogliendo**, e le masse ricevono lo stesso calcio del vuoto.

---

# `(4)` ⛔ **I DUE BRACCI DIAGNOSTICI: CHI SCIOGLIE LE MASSE**

> ### ⛔ **I CRITERI, FISSATI PRIMA** *(mandato di Luca)*: ### **`IL TERMOSTATO SCIOGLIE LE MASSE`** se in `B-T` l'AUC al `400` è ### **`>= 0.85`**; ### **`LO SCUOTIMENTO SCIOGLIE LE MASSE`** se in `B-S` l'AUC al `400` è ### **`>= 0.85`**. ### **Il controllo è la corsa di controllo di `A-S1`, che non si rigira.**

| passo | AUC ### **`B-T`** | AUC ### **`B-S`** | AUC ### **`B-TS`** | AUC ### **`B-SCAL`** | AUC controllo *(`A-S1`)* |
|--:|--:|--:|--:|--:|--:|
| `1` | ### **0.9992** | ### **0.9991** | ### **0.9991** | ### **0.9992** | 0.9992 |
| `50` | ### **0.9967** | ### **0.9967** | ### **0.9967** | ### **0.9964** | 0.9966 |
| `150` | ### **0.9598** | ### **0.8102** | ### **0.9225** | ### **0.9958** | 0.9861 |
| `230` | ### **0.4973** | ### **0.1574** | ### **0.1638** | ### **0.9886** | 0.9023 |
| `300` | ### **0.4946** | ### **0.3551** | ### **0.2031** | ### **0.9604** | 0.7371 |
| `400` | ### **0.4316** | ### **0.3796** | ### **0.4848** | ### **0.9020** | 0.4679 |
| `500` | ### **0.4686** | ### **0.4458** | ### **0.3831** | ### **0.8243** | 0.4497 |

> ### ✔ **`B-T`: AUC al `400` = 0.4316 `< 0.85` → `IL TERMOSTATO SCIOGLIE LE MASSE` ### NON è soddisfatto** *(controllo: 0.4679)*.

> ### ✔ **`B-S`: AUC al `400` = 0.3796 `< 0.85` → `LO SCUOTIMENTO SCIOGLIE LE MASSE` ### NON è soddisfatto** *(controllo: 0.4679)*.

> ### ⛔ **NESSUNO DEI DUE SALVA LE MASSE: `H3` è SMENTITA COME CAUSA**, e si torna ad `A-S2` *(`H2`)*. ### **La decisione è di Luca.**

### ⚠ **E `B-T` HA FATTO QUELLO CHE DOVEVA? il `xi_termo` RESIDUO**

| | `\|xi\|` massimo | `\|xi\|` mediano |
|---|--:|--:|
| `base` | ### **1.75459** | 1.24031 |
| ### **`B-T`** | ### **0.43016** | 0.15525 |

> ### ✔ **LA SOPPRESSIONE MISURATA: `4.1 ×`** sul massimo. ### ⛔ **E NON È UN AZZERAMENTO**, come il task history dichiarava prima della corsa: `B-T` è ### **«termostato senza memoria»**, non «senza termostato».

---

---

# `(5)` ⭐ **`B-TS`: SENZA BAGNO, RESTA SOLO LA DINAMICA INTERNA**

> ### ⛔ **I CRITERI, FISSATI PRIMA** *(mandato di Luca)*: ### **`LA CAUSA È IL BAGNO GLOBALE`** se l'AUC al `400` è ### **`>= 0.85`** ### **E** la coerenza di fase delle masse al `230` è ### **`>= 0.6`**; ### **`LA CAUSA È DENTRO LE MASSE (H2)`** se l'AUC al `400` è ### **`< 0.6`** ### **E** il bilancio delle masse mostra che è la ### **COPPIA** a far crescere `<phivel²>`; fra i due ### **si riporta la curva e il termine dominante.**

### IL BILANCIO NELLE ### **MASSE**, somma su `500` passi

| voce | somma | quota |
|---|--:|--:|
| `scuoti` | 0.0000 | ### **0.00 %** |
| `termostato` | 0.6510 | ### **8.47 %** |
| ### **`coppia`** | 6.9437 | ### **90.35 %** |
| `residuo_incrociato` | 0.0902 | ### **1.17 %** |

> ### ⛔ **IL TERMINE DOMINANTE NELLE MASSE È `coppia`** — il ### **90.35 %** del totale in valore assoluto. ### ✔ **E `scuoti` vale ESATTAMENTE `0.00000000`: l'intervento è scattato.**

### ⭐ **L'ENERGIA TOTALE: resta finita, cresce o cala?** *(il mandato lo chiede comunque: senza sorgenti né freni, la sua evoluzione dice se la dinamica interna ### **conserva, scalda o dissipa**)*

| | |
|---|--:|
| `E_cin` al passo `1` | 0.15631 |
| `E_cin` al passo `500` | ### **3.95258** |
| massimo | 3.95258 |
| ### **passi con `phivel` NON FINITI** | ### **0** |

> ### ⛔ **CRESCE**: da `0.15631` a ### **`3.95258`** *(`×25.29`)*. ### **E resta FINITA: `0` passi con valori non finiti.** ### ➜ **Quindi la dinamica interna, da sola, SCALDA.**

### ⛔ **L'ESITO DEL CRITERIO**

| | valore | la soglia |
|---|--:|---|
| AUC al `400` | ### **0.4848** | `>= 0.85` per il bagno, `< 0.60` per `H2` |
| coerenza di fase delle masse al `230` | ### **0.2178** | `>= 0.6` per il bagno |
| il termine dominante nelle masse | ### **`coppia`** | `coppia` per `H2` |

> ### ⛔ **`LA CAUSA È DENTRO LE MASSE (H2)`.** Senza bagno le masse si sciolgono comunque *(AUC `0.4848`)*, e ### **il termine che le scalda è la COPPIA** — cioè ### **la loro dinamica interna.** ### ⛔ **NON comincio la cura: la decisione è di Luca.**

> ### ⚠ **E `B-TS` EREDITA DA `B-T` IL NON ESSERE UN AZZERAMENTO:** `|xi|` massimo ### **0.02274** contro ### **1.75459** della base, cioè una soppressione di ### **77.1 ×**. ### **Il residuo è misurato, non assunto.**

---

---

# `D1` ⭐ **LA POTENZA DELLA COPPIA: pompa o ridistribuisce?**

> ### ⛔ **IL CRITERIO, FISSATO PRIMA** *(mandato di Luca)*: ### **`LA COPPIA POMPA`** se `P_coppia` nelle masse è ### **positiva in almeno l'`80 %`** dei passi `1..230` ### **E** la sua ### **somma** su quei passi è positiva; ### **`NON POMPA`** se quella somma è ### **`<= 0`**; fra i due ### **la curva.**

Le tre potenze, nella ### **stessa unità** *(lavoro per unità di tempo proprio)*: ### **`P_coppia = Σ coppia_k·p1_k`** *(forza × velocità: la potenza vera)*, `P_termo = −xi·Σ p1²`, e ### ⚠ **`P_scuoti = Σ p0·Δscuoti/dt_n`, che è un ANALOGO DICHIARATO** — lo scuotimento è un ### **calcio additivo**, non una forza.

## la classe ### **MASSE**

| passo | ### **`P_coppia`** | `P_termo` | `P_scuoti` *(analogo)* | `\|coppia_k\|` mediana |
|--:|--:|--:|--:|--:|
| `1` | ### **153.81** | 4.79 | 0.02 | 20.5304 |
| `10` | ### **142.93** | 53.95 | 83.78 | 0.4401 |
| `25` | ### **491.29** | 163.60 | -285.51 | 0.5860 |
| `50` | ### **1895.71** | -70.26 | 1244.39 | 1.0625 |
| `100` | ### **4802.54** | -6987.01 | -3232.74 | 1.8329 |
| `200` | ### **1563.14** | -5850.26 | 1186.17 | 0.8895 |
| `300` | ### **890.30** | -14542.15 | 3857.27 | 0.7174 |

| sui passi `1..230` | |
|---|--:|
| passi con `P_coppia` ### **positiva** | ### **230 su 230** *(100.00 %)* |
| ### **somma di `P_coppia`** | ### **564721.69** |

## la classe ### **VUOTO**

| passo | ### **`P_coppia`** | `P_termo` | `P_scuoti` *(analogo)* | `\|coppia_k\|` mediana |
|--:|--:|--:|--:|--:|
| `1` | ### **-692.18** | 40.65 | 0.06 | 18.8240 |
| `10` | ### **128.44** | 1461.04 | 1498.86 | 0.1727 |
| `25` | ### **403.93** | 11664.39 | 11372.59 | 0.1948 |
| `50` | ### **1319.94** | -5182.41 | -22231.67 | 0.2362 |
| `100` | ### **1924.41** | -348347.42 | 77849.06 | 0.2410 |
| `200` | ### **2721.08** | -194683.08 | -15157.70 | 0.3762 |
| `300` | ### **12341.87** | -254480.24 | 46382.38 | 0.5145 |

| sui passi `1..230` | |
|---|--:|
| passi con `P_coppia` ### **positiva** | ### **229 su 230** *(99.57 %)* |
| ### **somma di `P_coppia`** | ### **455660.71** |

> ### ⛔ **`LA COPPIA POMPA`.** `P_coppia` nelle masse è positiva nel ### **100.00 %** dei passi `1..230` *(soglia `80 %`)* ### **e la somma è 564721.69 `> 0`.**

> ### ⚠ **E LO AVEVO DICHIARATO GIÀ NOTO PRIMA DI GIRARE:** la voce `coppia` del bilancio di `H3` è un ### **multiplo POSITIVO** di `P_coppia` *(`voce = (2/M_PH)·media(dt_n·coppia·p1)`, con `dt_n > 0`)*, ed era positiva in ### **`230` passi su `230`** nelle masse. ### **La corsa non lo SCOPRE: lo misura nell'unità giusta e lo mette accanto alle altre due potenze.**

## ⭐ **E LO SCUOTIMENTO NON FA LAVORO: INIETTA VARIANZA**

La voce `scuoti` del bilancio e' `media(2·p0·Δs + Δs²)`: il primo addendo e' il ### **lavoro LINEARE** *(cioe' `2·dt_n·P_scuoti`)*, il secondo e' la ### **VARIANZA iniettata.** ### ⛔ **E per un calcio CASUALE il lavoro lineare media a ZERO**, perche' il calcio ### **non e' correlato con la velocita' corrente.**

| classe | somma `1..230` del ### **QUADRATICO** | del ### **LINEARE** | quota del quadratico |
|---|--:|--:|--:|
| VUOTO | ### **73.1294** | -0.4067 | ### **99.45 %** |
| MASSE | ### **9.6478** | 0.0568 | ### **99.42 %** |

> ### ⭐ **QUESTO RISOLVE L'APPARENTE CONTRADDIZIONE CON `H3`:** li' lo scuotimento faceva il ### **`94 %`** del riscaldamento; qui `P_scuoti` oscilla attorno a ### **zero**. ### **Non e' un disaccordo: sono DUE GRANDEZZE DIVERSE.** La coppia e' la ### **POTENZA** dominante *(fa lavoro SISTEMATICO)*, lo scuotimento la ### **SORGENTE DI VARIANZA** dominante *(scalda senza fare lavoro netto, come un bagno termico)*.

> ### ⛔ **E CONFRONTARE `P_coppia` CON `P_scuoti` COME SE FOSSERO LA STESSA COSA INGANNEREBBE:** `P_scuoti` ### **sottostima sistematicamente** lo scuotimento, perche' una potenza ### **non vede il termine quadratico.** ### **Lo scrivo qui perche' chi legge la tavola delle potenze lo deve sapere PRIMA di confrontare le colonne.**

> ### ⭐ **E `P_termo` CAMBIA SEGNO, come in `H3`:** positiva *(rifornisce)* su ### **48** passi, negativa *(frena)* su ### **252**, e il primo passo negativo è il ### **`49`**.

---

# `D2` ⭐ **UNA COPPIA CHE LEGGE LA FASE: il ramo SCALARE**

> ### ⛔ **DA DICHIARARE, e il mandato lo impone:** il ramo scalare usa ### **`cos(φ_k − φ_j)`**, ### **NON `cos((φ_k − φ_j)/2)`** come nella direzione candidata di Luca. ### **È un test sul PRINCIPIO** *(una coppia che dipende dalla fase che muove)*, ### **NON sulla forma finale: un esito positivo NON decide la cura.**

> ### ⛔ **I CRITERI, FISSATI PRIMA:** ### **`UNA COPPIA CHE LEGGE LA FASE TIENE LE MASSE`** se l'AUC al `400` è ### **`>= 0.85`** ### **E** l'energia totale al `500` è ### **minore** che nel controllo; ### **`NON BASTA`** se l'AUC al `400` è ### **`< 0.6`**; fra i due la curva ### **e il confronto al passo `230`.**

### ✔ **LA VERIFICA DELL'INTERVENTO — MISURATA, non promessa**

| | |
|---|--:|
| chiamate a `_coppia_interferenza` | ### **500** |
| ripristini del flag | ### **500** |
| ### **firme del settore spinoriale DIVERSE** *(prima/dopo)* | ### **0** |
| flag NON ripristinato | ### **0** |

> ### ✔ **`chiamate == ripristini`, ZERO firme diverse, ZERO flag non ripristinati.** ### ⭐ **Quindi `_coppia_interferenza` è PURA, e spegnere un flag intorno a lei NON PUÒ toccare nient'altro che il valore restituito** — ### **ed è la misura che il mandato chiede al posto delle parole.**

| | `B-SCAL` | controllo |
|---|--:|--:|
| AUC al `230` | ### **0.9886** | 0.9023 |
| ### **AUC al `400`** | ### **0.9020** | 0.4679 |
| `E_cin` al `1` | 0.15631 | — |
| ### **`E_cin` al `500`** | ### **25.40616** | ### ⛔ **ASSENTE** *(il controllo di `A-S1` non registra `E_cin`)* |
| ### **`E_cin` al `300`** *(il massimo passo comune col braccio `base`)* | ### **19.02911** | ### **16.39289** |

| | valore | il controllo |
|---|--:|--:|
| ### **coerenza di fase delle masse al `230`** | ### **0.8622** | 0.4565 |

> ### ⭐ **AUC al `400` = 0.9020, cioe' `>= 0.85`: LA PRIMA CLAUSOLA E' SODDISFATTA, e con un margine grande** *(il controllo sta a 0.4679)*.

> ### ⛔ **MA LA SECONDA NON LO E': l'energia GLOBALE non e' minore.** Al passo `300` vale ### **19.0291** contro ### **16.3929** del braccio `base`.

> ### ⚠ **QUINDI IL CRITERIO, CHE E' UNA CONGIUNZIONE, NON E' SODDISFATTO** -- e lo dico invece di fermarmi alla clausola che mi conviene.

> ### ⛔ **MA QUELLA CLAUSOLA MISURAVA LA GRANDEZZA SBAGLIATA, e lo dico perche' cambia la lettura:** l'energia ### **GLOBALE** e' dominata dal ### **VUOTO**, che e' il ### **90.34 %** dei nodi. ### ⚠ **E' un errore del guardiano, che ha scritto la clausola, e MIO, che l'ho letta come se dicesse qualcosa sulle MASSE.** ### ✔ **Il verdetto FORMALE resta quello che e'** -- un criterio fissato prima non si riscrive dopo -- ### **ma la tavola per classe qui sotto dice che cosa succede DAVVERO.**

| `phivel^2` al passo `300` | braccio `base` | ### **`B-SCAL`** | rapporto |
|---|--:|--:|--:|
| ### **MASSE** | 9.0368 | ### **2.4715** | ### **0.273** |
| ### **VUOTO** | 16.8191 | ### **20.2505** | ### **1.204** |

| `P_coppia` in `B-SCAL` | passi | ### **segno** | somma |
|---|--:|---|--:|
| ### **MASSE** | 500 | ### **NEGATIVA in 499 su 500** | ### **-575956.7** |
| MASSE, ### **dopo il `230`** | 270 | positiva in **0 su 270** | -417741.1 |
| ### **VUOTO** | 500 | ### **POSITIVA in 364 su 500** | ### **562890.3** |
| VUOTO, ### **dopo il `230`** | 270 | positiva in **270 su 270** | 3596164.3 |

> ### ⭐ **LA LETTURA GIUSTA, e corregge quella che avevo scritto:** con la coppia scalare ### **le MASSE sono PIU' FREDDE** *(e non piu' calde)*, ### **e la coppia TOGLIE loro energia** -- `P_coppia` nelle masse e' ### **NEGATIVA quasi sempre**, contro i ### **`230` su `230` POSITIVI** del braccio `base`. ### **Il piu' caldo e' il VUOTO**, dove la coppia immette energia.

> ### ⛔ **QUINDI LA FRASE <<LA COERENZA NON E' UNA QUESTIONE DI TEMPERATURA>> CHE AVEVO SCRITTO E' SBAGLIATA**, e la cancello: era basata sulla temperatura ### **GLOBALE**, cioe' su quella del vuoto. ### ✔ **Per le MASSE coerenza e temperatura vanno INSIEME, come ci si aspetta:** la coppia scalare le raffredda ### **e** le tiene coerenti.

> ### ⛔ **E NON DECIDE LA CURA, per la ragione dichiarata in testa alla sezione:** il ramo scalare usa `cos(phi_k - phi_j)`, ### **non `cos((phi_k - phi_j)/2)`** della direzione candidata di Luca. ### **E' un test sul PRINCIPIO. La decisione e' di Luca.**

---

# `D2-BIS` ⭐ **`B-SCAL-TS`: LA COPPIA SCALARE SENZA BAGNO, E L ENERGIA**

> *Criteri e previsioni: `doc/TASK_HISTORY/2026-10-08_bscalts-energia-e-potenziale.md`, committato ### **prima** in `d69214d`.*

## ⛔ **IL FATTO DA DIRE PRIMA DI TUTTO: IN QUESTO BRACCIO NON NASCE NIENTE**

| braccio | passi | `n` iniziale → finale | archi iniziali → finali | ### **nodi nati** |
|---|--:|--:|--:|--:|
| `base` | 300 | 12802 → 12850 | 471564 → 471630 | ### **48** |
| `B-SCAL` | 500 | 12802 → 12966 | 471564 → 471773 | ### **164** |
| `B-TS` | 500 | 12802 → 12811 | 471564 → 471576 | ### **9** |
| `B-SCAL-TS` | 500 | 12802 → 12802 | 471564 → 471564 | ### ⛔ **0** |

> ### ⛔ **ZERO NASCITE SU 500 PASSI: `n` e gli archi NON SI MUOVONO.** ### **Non l avevo previsto**, e cambia la lettura di tre cose: ### **(1)** la previsione `PE-5` è smentita ### **non perché le nascite non dominino, ma perché non ce ne sono**; ### **(2)** la finestra `216..500` in questo braccio ### **non separa le nascite da niente** — si riporta comunque, perché il mandato la chiede, ma ### **qui divide solo il tempo**; ### **(3)** `dU_A` è ### **tutto e solo `w` che cambia**, quindi il lavoro di `A` qui misura ### **la plasticità dei pesi**, non la crescita della rete.

> ### ⛔ **E L ATTRIBUZIONE NON È ALLA COPPIA: È AL BAGNO TOLTO.** ### ⚠ **Qui avevo scritto che è «la coppia scalare» a fermare la divisione, e i numeri dicono che NO:** `B-SCAL` ha la ### **STESSA** coppia scalare e, ### **col bagno**, fa ### **164** nascite in `500` passi — ### **più del `base`**, che ne fa `48` in `300`. E con la coppia ### **spinoriale** e il bagno ### **spento** *(`B-TS`)* ne fa `9`. ### ➜ **Le nascite crollano TOGLIENDO IL BAGNO, non cambiando la coppia:** `base 48` → `B-SCAL 164` → `B-TS 9` → `B-SCAL-TS 0`.

> ### ⭐ **E RESTA UN RISULTATO, ma di un ALTRO fatto:** togliere i due forzanti globali ### **azzera** la divisione, e la coppia scalare ### **non la ripristina**. ### **Il bagno è ciò che porta il sistema alla soglia di mitosi**, e il costo è del ### **togliere il bagno**, ### **non della forma della coppia.** ### ⚠ **Resta sul tavolo della decisione, con l etichetta giusta.**

## ⭐ **LE DUE ENERGIE SONO DERIVATE DAL CODICE, NON SCELTE**

| | |
|---|---|
| ### **CINETICA** | da `:7760` e `:7830`, diviso per `dt_n_s`, si legge ### **Newton sulla coordinata `φ`** con inerzia `M_PH`: ### **`T = ½·M_PH·Σ phivel²`** |
| il ruolo di `dt_n` | ### ⛔ **NON entra in `T`.** È il passo d integrazione, ed è ### **PER NODO** *(`dt_n = DT·r`, `:7498`)*: entra solo nei LAVORI, via `Δφ = dt_n·phivel(t+1)` *(`:7831`)* |
| ### ⚠ **e NON è l `E_cin` del codice** | `:7711` calcola `mean(phivel²)`: una ### **MEDIA**, senza `½` e senza `M_PH` — un analogo di ### **TEMPERATURA** per il confronto con `T_target`. ### **Due cose diverse con lo stesso nome, e qui sotto ci sono entrambe** |
| ### **POTENZIALE** | `U = −K_C·Σ_archi A_ij·cos(φ_i − φ_j)` con la `A` ### **EFFETTIVAMENTE USATA** — catturata dall involucro, perché è il ### **primo argomento** di `_coppia_interferenza`: non si ricostruisce |

> ### ✔ **E CHE IL RAMO SCALARE SIA `−∂U/∂φ` È MISURATO SULLA FUNZIONE VERA**, non argomentato: `--collaudo-potenziale` dà ### **`1.49e-15`** sulla `A` e le `φ` vere, e la ### **differenza finita** *(che non passa dalla mia derivata)* dà ### **`3.32e-09`**. ### ⛔ **E il caso che DEVE fallire fallisce:** la coppia ### **spinoriale** dà `1.01e+00`, con lo spinore ### **lontano** dal limite in cui i due rami coinciderebbero *(`max|b| = 1.0000`)*.

## ⛔ **IL CRITERIO `LA COPPIA SCALARE CONSERVA A A FISSO`**

> ### **Il criterio di Luca:** in almeno il ### **`95 %`** dei passi, `P_coppia` più il `dU/dt` dovuto alle ### **sole `φ`** ha residuo relativo ### **`< 1e-2`**. ### **Valutato nella forma del LAVORO** *(`Σ coppia·Δφ`)*, perché ### **`dt_n` è PER NODO** e una potenza per un `dt` unico sarebbe sbagliata.

| finestra | passi | ### **quota con residuo `< 1e-2`** | residuo mediano | `Δφ` massimo mediano | ### **residuo / `Δφ`** *(decile `10` — mediana — decile `90`)* | max | `W_interf` quasi nullo |
|---|--:|--:|--:|--:|--:|--:|--:|
| 1..215 | 215 | ### **2.79 %** | 0.02884 | 0.03455 | 0.3771 / 0.9004 / 3.5680 | 102.2762 | 10 |
| 216..500 *(e qui NON nasce niente: divide solo il tempo)* | 285 | ### **22.46 %** | 0.02299 | 0.05822 | 0.1549 / 0.3931 / 2.8465 | 112.6053 | 10 |

> ### ⛔ **IL CRITERIO NON È SODDISFATTO:** solo ### **14.00 %** dei passi sta sotto `1e-2` *(soglia `95 %`)*.

### ⭐ **E QUEL RESIDUO NON MISURA LA CONSERVAZIONE: MISURA IL PASSO.**

Il residuo è `dU_φ + Σ coppia·Δφ`, e ### **`Δφ` è l incremento VERO** *(quello che contiene anche `delta_sync_phi`)*: la sincronizzazione entra ### **sia in `dU_φ` sia nel lavoro**, quindi ### **si cancella NEL RESIDUO DI QUELLA IDENTITÀ** — ### ⛔ **e SOLO lì: NON nel bilancio di `H`, dove lo spostamento di sincronizzazione FA LAVORO, e molto** *(la sezione qui sotto)*. E siccome il collaudo ### **MISURA** che la coppia è `−∂U/∂φ` *(`1.49e-15`)*, l identità `dU_φ = −Σ coppia·Δφ + O(Δφ²)` è ### **ALGEBRA**: il residuo ### **È** quel resto del secondo ordine. ### ⛔ **Non è una congettura, e non dipende da questa corsa.**

> ### ⚠ **LA BANDA QUI SOTTO ERA PENSATA COME CONFERMA INDIPENDENTE, E LO È SOLO IN PARTE:** il coefficiente del secondo ordine va come `cos(φ_i − φ_j)` e quindi ### **VARIA DA PASSO A PASSO**, perciò il rapporto ### **non deve** restare costante quanto avevo creduto scrivendo la previsione. ### **Era un attesa mia troppo forte, e la correggo qui invece di leggere la larghezza della banda come un problema del codice.**

> ### **LA PROVA, dai dati:** se il residuo è del secondo ordine, allora `residuo / Δφ` deve restare in una banda ### **stretta** mentre il residuo assoluto cambia. ### **MISURATO:** fra i decili `10` e `90` sta fra `0.3771` e `3.5680`, un fattore ### **9.463** — ma il ### **massimo è `102.2762`**.

> ### ⛔ **E LA CODA NON LA NASCONDO: SU 215 PASSI, `10` HANNO `abs(W_interf)` SOTTO IL `10 %` DELLA SUA MEDIANA** — cioè un ### **denominatore quasi nullo**, dove un rapporto relativo esplode ### **per aritmetica, non per fisica.**

> ### **UN FATTORE `9.463` SULL `80 %` CENTRALE: la banda è più larga di quanto avessi previsto**, e la ragione è scritta qui sopra *(il coefficiente del secondo ordine varia come `cos(φ_i − φ_j)`)*. ### ⛔ **QUESTO NON INDEBOLISCE LA CONCLUSIONE, perché la conclusione poggia sul COLLAUDO e sull ALGEBRA, non sulla banda:** la coppia scalare ### **È** `−∂U/∂φ`, misurato a `1.49e-15` su tre casi, con la differenza finita a conferma. ### ➜ **Quindi il `NON SODDISFATTO` del criterio NON dice che la coppia non conserva: dice che `dt` non è abbastanza piccolo perché il lavoro di PRIMO ordine approssimi `ΔU` all `1 %`.** ### ⚠ **E LA MISURA CHE SEPAREREBBE il secondo ordine dalla coda dei denominatori piccoli è il lavoro col TRAPEZIO** *(la coppia valutata ANCHE a `φ` nuove)*: ### **questa corsa non la registra, e lo scrivo come misura MANCANTE, non come dettaglio.**

## ⭐ **LA NON-CONSERVAZIONE VERA, A `A` FISSO: `dT + dU_φ`** *(esatta, nessuna approssimazione)*

| finestra | `dT` sommato | `dU_φ` sommato | ### **`dT + dU_φ`** | in quota di `dU_φ` |
|---|--:|--:|--:|--:|
| 1..215 | 9739.9869 | 14042.6525 | ### **23782.6394** | 169.36 % |
| 216..500 *(e qui NON nasce niente: divide solo il tempo)* | 14026.8312 | 17911.5443 | ### **31938.3755** | 178.31 % |

> ### ⛔ **A `A` FISSO L ENERGIA NON SI CONSERVA. E LA CAUSA NON LA SCELGO IO: LA SCELGONO I NUMERI**, perché `dT` si DECOMPONE dal bilancio. ### **In unità di energia:** la voce del bilancio è una media di `Δ(phivel²)` per nodo, quindi il suo contributo a `T` è ### **`½·M_PH·(voce_masse·n_masse + voce_vuoto·n_vuoto)`**.

| finestra | ### **termostato** | ### **coppia** | `scuoti` | residuo incrociato | ### **somma** | `dT` misurato |
|---|--:|--:|--:|--:|--:|--:|
| 1..215 | ### **394.5614** | ### **8804.8634** | 0.0000 | 540.5622 | ### **9739.9869** | 9739.9869 |
| 216..500 *(e qui NON nasce niente: divide solo il tempo)* | ### **1333.7052** | ### **11951.6986** | 0.0000 | 741.4274 | ### **14026.8312** | 14026.8312 |


| finestra | `W` dell ### **interferenza** | `W` della coppia ### **totale** | ### **`W_extra`** *(i tre non-gradiente)* | ### **in quota** |
|---|--:|--:|--:|--:|
| 1..215 | -13637.4544 | -12365.2351 | ### **1272.2193** | 9.33 % |
| 216..500 *(e qui NON nasce niente: divide solo il tempo)* | -17368.8981 | -13516.3246 | ### **3852.5735** | 22.18 % |

## ⭐ **L IPOTESI DEL GUARDIANO: LA SINCRONIZZAZIONE È LA SORGENTE** *(`D2-TER`, e qui è UN IPOTESI, non un fatto)*

L algebra, scritta: `W_tot = Σ c_tot·Δφ` con `Δφ = dt_n·phivel(t+1) + delta_sync_phi`, mentre la voce `coppia` del bilancio cinetico, in unità di energia, è `Σ p1·d_cop = Σ dt_n·c_tot·p1/M_PH`. ### ➜ **La loro differenza contiene DUE cose, non una:**

```
W_tot - voce_coppia  =  Σ dt_n·c_tot·(p2 - p1)  +  Σ c_tot·delta_sync_phi
                        ^^^^^^^^^^^^^^^^^^^^^^
                        il SECONDO ORDINE, e si LIMITA dal bilancio:
                        dt_n·c_tot = M_PH·d_t + dt_n·xi·p1, quindi
                        Σ dt_n·c_tot·d_t = M_PH·Σ(d_t²) + (un termine in xi)
                        e `residuo_incrociato` in energia E' (1/2)·Σ(d_t²)
```

| finestra | `W_tot` | voce ### **`coppia`** | ### **differenza** | di cui ### **secondo ordine** | ### **`W_sync` STIMATO** | `ΔH` | ### **`−W_sync` su `ΔH`** |
|---|--:|--:|--:|--:|--:|--:|--:|
| 1..215 | -12365.2351 | 8804.8634 | ### **-21170.0985** | 1081.1243 | ### **-22251.2229** | 23782.6394 | ### **93.56 %** |
| 216..500 *(e qui NON nasce niente: divide solo il tempo)* | -13516.3246 | 11951.6986 | ### **-25468.0232** | 1482.8547 | ### **-26950.8780** | 31938.3755 | ### **84.38 %** |

> ### ⭐ **L ARITMETICA DEL GUARDIANO REGGE, E L HO RIFATTA IO:** la differenza è ### **-21170.0985**, e il secondo ordine — ### **che il guardiano non aveva messo** — ne spiega ### **1081.1243**, quindi `W_sync` stimato è ### **-22251.2229**. ### ➜ **Cioè lo spostamento di sincronizzazione spiega il 93.56 % della crescita di `H` nella prima finestra.** ### **Con il secondo ordine dentro, l ipotesi è PIÙ forte di come era scritta, non meno.**

> ### ⛔ **E RESTA UN IPOTESI, per DUE ragioni che dico io:** ### **(1)** `W_sync` qui è ### **DEDOTTO da una differenza**, non misurato — `delta_sync_phi` non è registrato in questa corsa; ### **(2)** la differenza è costruita sulla coppia ### **TOTALE**, mentre `W_interferenza` *(la sola che sia `−∂U/∂φ`)* è un altro numero. ### ➜ **La misura DIRETTA è `D2-TER` punto `1`, e il controllo positivo è che `W_sync + W_newton` ricomponga `W_interferenza`.**

## ⭐ **QUANTA PARTE DI `ΔH` VIENE DA `A` CHE CAMBIA, E QUANTA DALLE `φ`**

> ### ⚠ **IL PASSO DI RITARDO È DICHIARATO:** `dU_A` si può calcolare solo alla chiamata ### **successiva** *(la `A` nuova nasce lì)*, quindi la voce del passo `k` ### **chiude il passo `k−1`** e si somma col suo `dU_φ`.

| finestra | `dU_φ` | ### **`dU_A`** | di cui ### **`w`** *(archi comuni)* | di cui ### **nascite** | archi ### **spariti** | ### **quota di `A`** |
|---|--:|--:|--:|--:|--:|--:|
| 1..215 | 14042.6525 | ### **23885.7223** | 23885.7223 | 0.0000 | 0.0000 | ### **62.98 %** |
| 216..500 *(e qui NON nasce niente: divide solo il tempo)* | 17911.5443 | ### **357.7607** | 357.7607 | 0.0000 | 0.0000 | ### **1.96 %** |

## **`T`, `U` e `H` AI PASSI DI MISURA, PER CLASSE**

> ### ⚠ **`U` SI SPARTISCE IN TRE CLASSI, NON DUE:** un arco fra una massa e il vuoto ### **non appartiene a nessuna delle due**, e metterlo d autorità in una falserebbe il bilancio. Le masse sono ### **1237** nodi su ### **12802**.

| passo | `T` masse | `T` vuoto | `U` masse | `U` misti | `U` vuoto | ### **`H`** | `E_cin` del codice |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 105.5464 | 895.0033 | -8839.0863 | -3485.1636 | -50540.2957 | ### **-61863.9959** | 0.15631 |
| 50 | 130.8362 | 1868.7825 | -5900.3623 | -2149.9669 | -30696.3316 | ### **-36747.0422** | 0.31239 |
| 150 | 226.9550 | 14930.9178 | -5275.7555 | -2272.0265 | -26270.8412 | ### **-18660.7504** | 2.36805 |
| 215 | 178.2809 | 10659.9563 | -5146.4170 | -1951.0136 | -18060.5877 | ### **-14319.7810** | 1.69321 |
| 216 | 179.6856 | 10560.8510 | -5148.0491 | -1947.8160 | -17870.5562 | ### **-14225.8847** | 1.67795 |
| 230 | 212.2868 | 9449.9087 | -5188.4585 | -1924.6106 | -15362.6384 | ### **-12813.5120** | 1.50948 |
| 300 | 560.5278 | 14827.9308 | -5537.3728 | -2153.1032 | -11060.4128 | ### **-3362.4302** | 2.40407 |
| 400 | 693.6064 | 22465.5642 | -5302.6153 | -1140.5028 | -7900.7910 | ### **8815.2615** | 3.61806 |
| 500 | 1068.1588 | 23625.6698 | -4305.8254 | -642.5263 | -1724.9947 | ### **18020.4822** | 3.85781 |

| il controllo positivo | su 500 passi |
|---|--:|
| le tre classi di `U` ### **ricompongono `U`** | scarto relativo massimo ### **0.000** |
| gli archi delle tre classi ### **fanno gli archi del passo** | scarto massimo ### **0.0000** |

> ### ✔ **LA SPARTIZIONE PER CLASSE È VERIFICATA, non presunta:** le tre classi ricompongono `U` e gli archi. ### **Senza questo controllo una colonna per classe potrebbe essere sbagliata senza che si veda.**

## ⛔ **IL CRITERIO `SENZA BAGNO NON ESPLODE`**

| | |
|---|--:|
| `T` al passo `1` | 1222.9194 |
| `T` al passo `500` | 24767.3678 |
| ### **la crescita** | ### **×20.2527** |
| il confronto: `B-TS` *(coppia SPINORIALE, stesso bagno spento)* | ### **×25.29** |

| classe | `T` al `1` | `T` al `500` | ### **la crescita** |
|---|--:|--:|--:|
| ### **MASSE** | 133.4341 | 1067.8214 | ### **×8.0026** |
| ### **VUOTO** | 1089.4853 | 23699.5464 | ### **×21.7530** |
| ### **TOTALE** *(dominato dal VUOTO: 11565 nodi su 12802)* | 1222.9194 | 24767.3678 | ### **×20.2527** |

> ### ⛔ **LA CLAUSOLA È SCRITTA SULL ENERGIA TOTALE, CHE È LA GRANDEZZA DOMINATA DAL VUOTO** — ed è ### **lo stesso difetto** che il punto `1` di questo mandato ha dichiarato per `D2`. ### **Il verdetto formale resta quello che è** *(un criterio fissato prima non si riscrive dopo)*, ### **ma i numeri per classe dicono un altra cosa:** le MASSE crescono ### **×8.0026**, il VUOTO ### **×21.7530** — un fattore ### **2.72** fra le due. ### ➜ **Quello che esplode è il VUOTO, e le masse restano l oggetto freddo e coerente.**

> ### ⛔ **IL CRITERIO NON È SODDISFATTO: ×20.2527**, oltre la soglia ×3 *(`B-TS` dava ×25.29)*.

## **L `AUC` E LA COERENZA, COME IN `D2`**

| | `B-SCAL-TS` | `B-SCAL` *(col bagno)* | controllo |
|---|--:|--:|--:|
| AUC al `230` | ### **0.9377** | 0.9886 | 0.9023 |
| ### **AUC al `400`** | ### **0.9394** | 0.9020 | 0.4679 |

| massa | coerenza di fase al `230` | `std(phivel)` |
|---|--:|--:|
| `massa_0` | ### **0.9495** | 0.5263 |
| `massa_1` | ### **0.9024** | 0.6009 |
| `massa_2` | ### **0.9264** | 0.6172 |
| il ### **VUOTO** | 0.0274 | 1.2746 |

---

# `D2-TER` ⭐ **LA SINCRONIZZAZIONE È LA SORGENTE?**

> *Criteri e previsioni: `doc/TASK_HISTORY/2026-10-08_d2ter-sincronizzazione-sorgente.md`, committato ### **prima** in `74d1305`.*

## ⭐ **`K_SYNC = 0` È UN SOLO INTERRUTTORE? MISURATO, NON ARGOMENTATO**

Dal codice: `K_SYNC` apre il blocco di `:7767`, la cui ### **unica** uscita è `delta_sync_phi` *(`:7805`)*, perché `_forza_sync` si popola ### **solo se** uno fra `SYNC_SPINORE`, `SYNC_FASE_OROLOGIO` e `KURAMOTO_SU2` è acceso — e le tre leggi che lo leggono stanno a `:5946`, `:6053`, `:6067`. ### ⚠ **E `--sync` NON è `K_SYNC`:** quello è un flag CLI a sé *(`:11600`)*, e ### **`K_SYNC` non ha affatto un flag CLI** — è una costante di modulo.

| flag | in `B-SCAL-TS` | in ### **`B-SCAL-TS-NOSYNC`** |
|---|--:|--:|
| `K_SYNC` | 1.0 | ### **0.0** |
| `SYNC_SPINORE` | False | ### **False** |
| `SYNC_FASE_OROLOGIO` | False | ### **False** |
| `KURAMOTO_SU2` | False | ### **False** |

### ⛔ **MA IL BLOCCO CONTIENE `calcola_psi(w)`** *(`:7771`)*, che ### **SCRIVE** `self.psi`, `psi_spin` e `rho_spin`: saltarlo salta quella scrittura. ### **«Dovrebbe essere byte-inerte» non è una misura**, quindi un involucro firma `psi` ### **prima e dopo OGNI chiamata** e conta per ### **CHIAMANTE**.

| braccio | chiamante | chiamate | ### **che hanno CAMBIATO `psi`** |
|---|--:|--:|--:|
| `B-SCAL-TS` | ### **`:876`** | 1 | ### ⛔ **1** |
| `B-SCAL-TS` | ### **`:7592`** | 500 | ### ⛔ **500** |
| `B-SCAL-TS` | ### **`:7771`** | 500 | ### ✔ **0** |
| `B-SCAL-TS-NOSYNC` | ### **`:876`** | 1 | ### ⛔ **1** |
| `B-SCAL-TS-NOSYNC` | ### **`:7592`** | 500 | ### ⛔ **500** |

> ### ✔ **`K_SYNC = 0` È UN SOLO INTERRUTTORE:** la `calcola_psi` di `:7771` è stata chiamata ### **500** volte e ha cambiato `psi` ### **ZERO** volte. ### ⭐ **E il rivelatore PUÒ fallire:** `:7592` cambia `psi` ### **a ogni chiamata**, quindi non è un controllo che passa a vuoto. ### ➜ **La regola d oro del par.3 è rispettata: fra i due bracci cambia UNA cosa.**

## ⭐ **`delta_sync_phi` DERIVATO DALLA LEGGE, E IL CONTROLLO CHE LO VALIDA**

Dal commit atomico *(`:7831`)* `phi(t+1) = (phi_t + dt_n·phivel(t+1) + delta_sync_phi) mod _dphi()`, quindi ### **`delta_sync_phi = Δφ − dt_n·phivel(t+1)`** — ### **esatto dalla legge, non stimato** *(e `dt_n_s = dt_n` perché `TEMPO_SEGNO = False`, che lo strumento verifica e altrimenti FERMA)*.

| braccio | `rms` mediano | ### **massimo** | nodi con valore non nullo *(mediano)* |
|---|--:|--:|--:|
| `B-SCAL-TS` | ### **6.7817e-03** | 3.5039e-02 | 12802 |
| `B-SCAL-TS-NOSYNC` | ### **3.7311e-16** | 3.2561e-15 | 12796 |

> ### ⚠ **E LA MIA PREVISIONE `PS-1` ERA TROPPO FORTE:** avevo scritto ### **«esattamente `0`»**, e in `NOSYNC` il residuo è `3.7311e-16`. ### **Non è un termine: è il PAVIMENTO DI ARROTONDAMENTO**, perché l avvolgimento `mod 4π` ### **non è esatto** e `eps_macchina · |φ|` è di quell ordine. ### ➜ **Ma il controllo DISCRIMINA comunque: `6.7817e-03` contro `3.7311e-16`, cioè un fattore `1.818e+13`.** ### **La previsione era sbagliata nella FORMA e giusta nella SOSTANZA, e la annoto invece di riscriverla** *(par.8)*.

## ⭐ **LA SPARTIZIONE DEL LAVORO: `W_newton` CONTRO `W_sync`**

> ### ⚠ **LA RICOMPOSIZIONE `W_sync + W_newton = W_interferenza` È TAUTOLOGICA**, perché i due addendi partizionano `Δφ` ### **per definizione**. Il mandato la chiede e si riporta, ### **ma il controllo vero è il pavimento in `NOSYNC` qui sopra.**

| braccio | finestra | ### **`W_sync`** | `W_newton` | `W_interferenza` | ### **quota di `W_sync`** | residuo della ricomposizione |
|---|---|--:|--:|--:|--:|--:|
| `B-SCAL-TS` | `1..215` | ### **-19993.5289** | 6356.0745 | -13637.4544 | ### **146.61 %** | 2.67e-14 |
| `B-SCAL-TS` | `216..500` | ### **-17704.8616** | 335.9635 | -17368.8981 | ### **101.93 %** | 3.03e-14 |
| `B-SCAL-TS-NOSYNC` | `1..215` | ### **-0.0000** | -1078.8467 | -1078.8467 | ### **0.00 %** | 1.92e-15 |
| `B-SCAL-TS-NOSYNC` | `216..500` | ### **-0.0000** | -1274.2057 | -1274.2057 | ### **0.00 %** | 5.19e-15 |

| braccio | finestra | `W_sync` sulla coppia ### **TOTALE** | il confronto con la ### **STIMA** del punto `0` |
|---|---|--:|--:|
| `B-SCAL-TS` | `1..215` | ### **-22250.2756** | la stima era `-22251.2229` → rapporto ### **1.000** |
| `B-SCAL-TS` | `216..500` | ### **-26949.4294** | la stima era `-26950.8780` → rapporto ### **1.000** |

## ⛔ **IL CRITERIO: `LA SINCRONIZZAZIONE È LA SORGENTE`?**

| la lettura di ### **«crescita di `H`»** | in `B-SCAL-TS` | ### **in `NOSYNC`** | il rapporto | soglia ### **SORGENTE** *(un quarto)* | soglia ### **NON È LEI** *(la metà)* | ### **il verdetto** |
|---|--:|--:|--:|--:|--:|---|
| `H(215) − H(1)`, ### **LETTERALE** | 47544.2149 | ### **22988.5679** | ### **48.35 %** | 11886.0537 | 23772.1075 | ### ⚠ **`FRA I DUE`** |
| `Σ(dT + dU_φ)`, a ### **`A` FISSA** | 23782.6394 | ### **1559.4201** | ### **6.56 %** | 5945.6598 | 11891.3197 | ### ⛔ **`LA SINCRONIZZAZIONE È LA SORGENTE`** |

| il ### **lavoro di `A` che cambia** su `1..215` | `B-SCAL-TS` | ### **`NOSYNC`** | il rapporto |
|---|--:|--:|--:|
| ### **`Σ(dU_A)`** | 23885.7223 | ### **21435.8389** | 89.74 % |

> ### ⛔ **I DUE VERDETTI SONO DIVERSI, E LO DICO INVECE DI SCEGLIERE.** Sulla lettura ### **letterale** il criterio dà ### ⚠ **`FRA I DUE`** *(48.35 %)*; sulla lettura ### **a `A` fissa** dà ### ⛔ **`LA SINCRONIZZAZIONE È LA SORGENTE`** *(6.56 %)*. ### ➜ **E la ragione è nella tavola qui sopra:** `H` cresce ANCHE per il ### **lavoro di `A` che cambia**, e quel lavoro è ### **quasi lo stesso nei due bracci** *(23885.7223 contro 21435.8389, cioè il 89.74 %)* — ### **la sincronizzazione non lo tocca.**

> ### ⭐ **QUELLO CHE I NUMERI DICONO SENZA AMBIGUITÀ:** togliere `K_SYNC` toglie ### **93.44 %** della crescita di `H` ### **a `A` fissa** *(da 23782.6394 a 1559.4201)*, e ### **51.65 %** della crescita TOTALE. ### **La sincronizzazione è la sorgente DELLA PARTE IN `φ`, non di tutta la crescita** — e il criterio, come è scritto, non distingueva le due cose.


| passo | `H` in `B-SCAL-TS` | ### **`H` in `NOSYNC`** | `T` masse `NOSYNC` | `T` vuoto `NOSYNC` | `U` totale `NOSYNC` |
|--:|--:|--:|--:|--:|--:|
| 1 | -61863.9959 | ### **-61863.9959** | 105.5464 | 895.0033 | -62864.5456 |
| 50 | -36747.0422 | ### **-40157.8739** | 109.4471 | 772.5282 | -41039.8492 |
| 150 | -18660.7504 | ### **-35908.3326** | 122.4502 | 1164.9406 | -37195.7233 |
| 215 | -14319.7810 | ### **-38875.4280** | 152.8112 | 1227.7992 | -40256.0385 |
| 216 | -14225.8847 | ### **-38934.3650** | 153.6951 | 1234.5551 | -40322.6152 |
| 230 | -12813.5120 | ### **-39751.2141** | 166.2905 | 1341.7954 | -41259.3000 |
| 300 | -3362.4302 | ### **-42702.4686** | 239.9990 | 1754.8711 | -44697.3387 |
| 400 | 8815.2615 | ### **-42699.7152** | 327.9550 | 1983.9474 | -45011.6176 |
| 500 | 18020.4822 | ### **-40521.9759** | 400.2383 | 2087.3224 | -43009.5366 |

| | `B-SCAL-TS` | ### **`B-SCAL-TS-NOSYNC`** | controllo |
|---|--:|--:|--:|
| AUC al `230` | 0.9377 | ### **0.9891** | 0.9023 |
| ### **AUC al `400`** | 0.9394 | ### **0.9333** | 0.4679 |
| ### **nascite** | 0 | ### **0** | — |

| massa | coerenza al `230` in `B-SCAL-TS` | ### **in `NOSYNC`** |
|---|--:|--:|
| `massa_0` | 0.9495 | ### **0.9372** |
| `massa_1` | 0.9024 | ### **0.9197** |
| `massa_2` | 0.9264 | ### **0.9352** |
| il ### **VUOTO** | 0.0274 | ### **0.0078** |

> ### ✔ **LE MASSE NON SI SCIOLGONO** *(AUC al `400` = `0.9333`)*: la coerenza ### **sopravvive** al togliere la sincronizzazione, quindi viene dalla ### **coppia**, che è `−∂U/∂φ` e ordina le fasi. ### ➜ **E allora la sincronizzazione POMPAVA senza ordinare.**

## ⛔ **IL SIGILLO DI BYTE-INERZIA È FALLITO, POI CURATO — E LO SCRIVO IN QUEST ORDINE**

| | |
|---|---|
| ### **che cos è fallito** | ### **UN** attributo su `291`: `_calcpsi_origini`, con `n` e gli archi a valle ### **identici** nei due bracci. L esito `FALLISCE` è committato ### **così com è** in `3ef2dd4`, ### **prima** della cura *(par.5)* |
| ### **la causa, dal codice** | quel dizionario è ### **diagnostico** e le sue chiavi sono `nome_del_chiamante:riga_del_chiamante` *(`:6295`-`:6297`)*; l involucro su `calcola_psi` ### **diventa il chiamante**, quindi le chiavi cambiano ### **per costruzione** |
| ### ⚠ **e aggregare per FUNZIONE non basta** | cambia ### **anche il nome** della funzione *(`_inv_psi` invece di `step`)*, quindi l aggregazione — la pratica abituale per questa voce — ### **non riconcilia niente** |
| ### ✔ **e nessuna legge lo legge** | nel simulatore compare ### **solo** a `:6295` e `:6297`, ### **entrambe SCRITTURE**: censito, non supposto |
| ### **la cura** *(`0572907`, un commit a sé)* | l attributo entra in `ESCLUSI` ### **con la ragione scritta nel codice**, e al suo posto va un ### **TERZO controllo positivo che PUÒ fallire**: la ### **somma** dei conteggi e `_calcpsi_chiamate` devono coincidere fra i due bracci. ### **Le CHIAVI cambiano, i NUMERI no** |

| il sigillo, dopo la cura | |
|---|--:|
| ### **esito** | ### **PASSA** |
| attributi confrontati | 290 |
| ### **attributi DIVERSI** | ### **0** |
| esclusi, ### **dichiarati** | `_calcpsi_origini` |
| `n` e archi a valle | nudo `[12809, 471574]` · osservato `[12809, 471574]` |
| ### **il controllo che rimpiazza l escluso** | somma dei conteggi `1` / `1`; `_calcpsi_w_none` `1` / `1`; ### **`_calcpsi_chiamate` TOTALI `441` / `441`**; chiavi `1` / `1` *(e POSSONO differire)* |
| ### **i numeri coincidono** | ### **✔ SÌ** |

> ### ⭐ **E IL CONTROLLO PIÙ FORTE SULLA FISICA NON È IL SIGILLO: È LA RI-ESECUZIONE.** `B-SCAL-TS` rigirato col blob nuovo contro il file ### **già committato** dà ### **ZERO DIFFERENZE su 44498 coppie di valori** su ### **501** passi in comune, confrontando ogni contatore e ogni voce del bilancio in entrambe le classi. ### **Le voci che `D2-TER` ha aggiunto sono dichiarate ESCLUSE nel file del confronto**, perché nel vecchio non esistono.

## ⭐ **E SOTTO `A16`: LA CLAUSOLA «SENZA BAGNO NON ESPLODE» QUI PASSA** *(annotazione del 2026-10-08, dai json già committati)*

| la lettura della cinetica | al passo `1` | al passo `500` | ### **la crescita** | la soglia | ### **l esito** |
|---|--:|--:|--:|--:|---|
| `T_PRE` *(PRIMA del passo)* | 1000.5497 | 2487.5607 | ### **×2.4862** | `×3` | ### ✔ **PASSA** |
| `T_POST` *(DOPO il passo)* | 1222.9194 | 2491.8632 | ### **×2.0376** | `×3` | ### ✔ **PASSA** |

> ### ⚠ **DUE LETTURE DELLO STESSO DATO, RICONCILIATE invece di scelte.** Il guardiano ha scritto `1000.5497 → 2487.5607` *(`×2.4862`)*, cioè la cinetica ### **PRIMA** del passo; io avevo riportato `1222.9194 → 2491.8632` *(`×2.0376`)*, cioè ### **DOPO**. ### **Le due differiscono perché il PRIMO passo inietta `222.3697` nella cinetica**, e lo stato iniziale non è in equilibrio. ### ➜ **La clausola `< ×3` PASSA in entrambe le letture**, e i criteri di `D2-BIS` usavano `T_POST`: lo dico perché i due numeri non si leggano come un disaccordo.

| finestra | ### **`Σ(dU_A)`** | `Σ(dT + dU_φ)` | `H` alla fine − `H` all inizio |
|---|--:|--:|--:|
| `1..215` | ### **21435.8389** | 1559.4201 | 22988.5679 |
| `216..500` | ### **-4284.3679** | 2640.0422 | -1587.6109 |

> ### ⭐ **IPOTESI DEL GUARDIANO, E LA SCRIVO COME TALE:** la crescita residua di `H` viene ### **quasi tutta dal lavoro di `A` che cambia**, e quel lavoro ### **cambia SEGNO fra le due finestre** — `21435.8389` su `1..215` e ### **-4284.3679** su `216..500`. ### ➜ **Letto così è un ASSESTAMENTO INIZIALE DEI PESI, non una pompa continua.**

> ### ⚠ **E RESTA UN IPOTESI, per due ragioni che dico io:** ### **(1)** un cambio di segno su DUE finestre non è un assestamento ### **misurato**: servirebbe la curva di `dU_A` nel tempo, e il criterio su quando si esaurisce; ### **(2)** in questo braccio ### **non nasce niente**, quindi `dU_A` è ### **tutto e solo `w` che cambia** — su una corsa con nascite il numero mescolerebbe due cose. ### **La misura che la chiuderebbe non c è, e non la spaccio per fatta.**

> ### ⛔ **E SOTTO `A16` QUESTO BRACCIO RESTA UNA DIAGNOSI, non un modello:** `phivel` e `M_PH` sono ### **secondo ordine** e l assioma non li ammette; la coppia del simulatore ### **non deriva da `H`**. ### **Il piano è in `doc/RISCRITTURA_PRIMO_ORDINE.md`, e il simulatore NON è toccato.**

---

# ⭐ **LE MIE PREVISIONI, CONTRO I NUMERI**

| | la previsione | il numero | esito |
|---|---|---|---|
> ### ✔ **I numeri del collaudo del potenziale sono LETTI dal suo file** *(`csv/_test_fork/_termo_h3/collaudo_potenziale.txt`, ### **8 su 8**)*, non ricopiati.

| `PH3-1` | ### ⛔ **`H3` sarà SMENTITA sulla TERZA clausola: il termostato NON è la voce principale** *(l'aritmetica: nemmeno al tetto `\|xi\|=2` arriva a `×8.1`, dà al massimo `×2.3`)* | la voce principale nel VUOTO sui primi `50` passi è ### **`scuoti`** | ### ✔ **CONFERMATA** |
| `PH3-2` | la voce principale sarà ### **`scuoti_vuoto`**, che è ADDITIVO | è ### **`scuoti`** | ### ✔ **CONFERMATA** |
| `PH3-3` | ### **`B-S` mostrerà l'effetto grande** *(AUC al `400` `>= 0.85`)*, ### **`B-T` quello piccolo** *(`< 0.85`)* | `B-S` 0.3796, `B-T` 0.4316 | ### ⛔ **SMENTITA** |
| `PH3-4` | `T_target` cresce ### **POCO** e per via di `median(d0)`; e ### **non è il motore** del riscaldamento dei primi `50` passi | `T_target` dal passo `1` al `300`: ### **30.13 %** | ### ⛔ **SMENTITA: cresce di 30.13 %** |
| `PH3-5` | ### **`Λ` cresce e la soppressione delle masse si INDEBOLISCE:** il rapporto `amp` masse/vuoto ### **SALE** | dal passo `1` al `300`: ### **0.1652 → 0.7468** | ### ✔ **CONFERMATA** |
| `PTS-1` | ### ⛔ **scattera' `LA CAUSA E' DENTRO LE MASSE (H2)`: AUC al `400` `< 0.6`** *(perche' la coppia agisce `9.31 x` piu' nelle masse che nel vuoto)* | AUC al `400` in `B-TS`: ### **0.9394** | ### ⛔ **SMENTITA, ed e' il risultato piu' importante: le masse SOPRAVVIVONO senza il bagno** |
| `PTS-2` | il termine dominante nelle masse sara' la ### **`coppia`** | e' ### **`coppia`** *(il 89.16 %)* | ### ✔ **CONFERMATA** |
| `PTS-3` | l'energia totale ### **CRESCE** ma `~10 x` meno del controllo *(previsto `~1.2` al `230` contro `13.57`)* | da `0.1563` a ### **3.8578**; e al `230` il controllo e' `3.5 x` piu' caldo | ### ✔ **CONFERMATA** |
| `PTS-4` | la coerenza di fase delle masse al `230` sara' ### **`< 0.3`**, quindi il criterio del bagno NON scatta | ### **0.9261** | ### ⛔ **SMENTITA** |
| `PTS-5` | ### **NON divergera'** entro `500` passi, e ### **non si congelera'** | passi con `phivel` non finiti: ### **0**; stato: ### **DATI SALVATI** | ### ✔ **CONFERMATA** |
| `PD-1` | ### ⛔ **`LA COPPIA POMPA`**, con margine larghissimo. ### ⚠ **DICHIARATA GIA' NOTA** prima di girare: era nei dati di `H3` | nelle masse: positiva nel ### **100.00 %** dei passi `1..230`, somma ### **564721.69** | ### ✔ **CONFERMATA** |
| `PD-2` | `P_coppia` nelle masse ### **dello stesso ordine** di `P_scuoti` nelle masse, e ### **molto piu' piccola** di `P_scuoti` nel vuoto | al passo `230`: `\|P_coppia\|` masse ### **1140.25**, `\|P_scuoti\|` masse 1553.56, `\|P_scuoti\|` vuoto 19826.70 | ### ✔ **CONFERMATA** |
| `PD-3` | `P_termo` cambiera' ### **SEGNO** attorno al passo `49` | primo passo negativo: ### **`49`** *(positiva su 48 passi, negativa su 252)* | ### ✔ **CONFERMATA** |
| `PD-4` | ### ⚠ **`D2` dara' `NON BASTA`: AUC al `400` `< 0.6`** *(il ramo scalare cambia la COPPIA, non la scena, e `A` resta `w*cos(phi0_i - phi0_j)` con `phi0` CONGELATA)* | AUC al `400` in `B-SCAL`: ### **0.9020** *(controllo 0.4679)* | ### ⛔ **SMENTITA, ed e' il risultato piu' importante: una coppia che legge la fase TIENE le masse** |
| `PD-5` | ma l'energia totale in `D2` sara' ### **MINORE** che nel controllo | ### ⚠ **il controllo di `A-S1` NON registra `E_cin`**, quindi il confronto e' col braccio `base` al ### **massimo passo comune, il `300`**: `B-SCAL` ### **19.0291** contro `base` ### **16.3929** | ### ⛔ **SMENTITA** |
| `PE-1` | il collaudo del potenziale ### **CHIUDE** sulla funzione vera, con residuo relativo ### **`< 1e-10`** | ### **1.490e-15** | ### ✔ **CONFERMATA** |
| `PE-2` | ### **il caso che DEVE fallire fallisce:** la coppia ### **spinoriale** non chiude, con residuo ### **`> 1e-2`** | ### **1.012e+00** *(e la differenza finita, che non passa dalla mia derivata, dà `3.316e-09`)* | ### ✔ **CONFERMATA** |
| `PE-4` | ### **`SENZA BAGNO NON ESPLODE` è soddisfatto:** l energia cinetica ### **non cresce ×3** | ### **×20.2527** *(`B-TS`, con la coppia spinoriale, dava ×25.29)* | ### ⛔ **SMENTITA** |
| `PE-5` | il ### **lavoro di `A` che cambia** è la parte ### **dominante** della variazione di `H` dopo il `216`, ### **perché le nascite aggiungono archi** | la quota di `A` è ### **1.96 %**, gli archi nuovi sono ### **0** e il loro lavoro ### **0.0000** | ### ⛔ **SMENTITA, E PER UN MOTIVO CHE NON AVEVO PREVISTO:** in questo braccio ### **non nasce NIENTE**, quindi la premessa della previsione *(«le nascite aggiungono archi»)* ### **non si verifica mai**. ### **Non è che le nascite non dominino: non ci sono.** |
| `PE-6` | l `AUC` al `400` resta ### **`>= 0.85`** anche senza bagno | ### **0.9394** | ### ✔ **CONFERMATA** |
| `PE-7` | ### **`W_extra` NON è trascurabile** *(almeno il `10 %` di `W_interf` in modulo)*. ### **Scritta così per poter PERDERE:** se fosse trascurabile, il criterio chiuderebbe anche sulla coppia totale e il mio censimento sarebbe stato pessimismo | ### **16.53 %** di `W_interf` su tutta la corsa — e ### ⚠ **il rapporto CAMBIA con la finestra:** `9.33 %` su `1..215`, `n/d` su `216..500`. ### **Riporto entrambe invece di scegliere quella che mi conviene** | ### ✔ **CONFERMATA sul TOTALE** |
| `PS-1` | in `NOSYNC` `delta_sync_phi` è ### **esattamente `0`** su tutti i passi e tutti i nodi | il residuo è ### **3.7311e-16**, contro `6.7817e-03` in `B-SCAL-TS` *(un fattore `1.818e+13`)* | ### ⛔ **SMENTITA NELLA FORMA, confermata nella SOSTANZA:** l avvolgimento `mod 4π` ### **non è esatto**, quindi il pavimento è `eps_macchina·|φ|` e NON lo zero. ### **Era un attesa mia troppo forte, e la annoto** *(par.8)* |
| `PS-2` | in `B-SCAL-TS` `W_sync` è la parte ### **dominante** di `W_interferenza` *(oltre il `50 %`)* | ### **146.61 %** | ### ✔ **CONFERMATA** |
| `PS-3` | `W_sync` sulla coppia ### **TOTALE** sta ### **entro un fattore `2`** dalla stima dedotta nel punto `0` | misurato `-22250.2756`, stima `-22251.2229` → rapporto ### **1.0000** | ### ✔ **CONFERMATA** |
| `PS-4` | ### **`LA SINCRONIZZAZIONE È LA SORGENTE` è soddisfatto:** la crescita di `H` in `NOSYNC` sta ### **sotto un quarto** di quella di `B-SCAL-TS` | a ### **`A` FISSA**: ### **6.56 %** *(`1559.4201` contro `23782.6394`, soglia `5945.6598`)*; ### ⚠ **sulla lettura LETTERALE `H(215) − H(1)`: 48.35 %**, cioè ### **`FRA I DUE`** | ### ✔ **CONFERMATA sulla lettura a `A` FISSA**, ### ⚠ **e NON su quella letterale:** il criterio non distingueva le due, e ### **riporto entrambe invece di scegliere** |
| `PS-5` | ### **le masse NON si sciolgono** senza sincronizzazione: `AUC` al `400` ### **`>= 0.85`**. ### **Scritta per poter PERDERE:** se crolla, la sincronizzazione le teneva insieme ### **pompando** | ### **0.9333** | ### ✔ **CONFERMATA** |
| `PS-6` | ### **zero nascite anche in `NOSYNC`**: il bagno resta spento, ed è lui che porta alla soglia *(il punto `0`)* | ### **0** nascite | ### ✔ **CONFERMATA** |
| `PS-7` | la `calcola_psi` di `:7771` è ### **byte-inerte**, quindi `K_SYNC = 0` è ### **UN SOLO interruttore** | ### **500** chiamate, ### **0** cambiate *(e `:7592` ne cambia tutte, quindi il rivelatore PUÒ fallire)* | ### ✔ **CONFERMATA** |
| `PS-8` | la ri-esecuzione di `B-SCAL-TS` dal blob nuovo dà ### **zero differenze** sui contatori già committati | ### **44498** coppie di valori confrontate, e l esito è ### **ZERO DIFFERENZE** | ### ✔ **CONFERMATA** |

> ### **20 confermate, 9 SMENTITE** su 29.

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE, E NON PROPONE**

| | |
|---|---|
| una ### **CURA** | ### ⛔ **NESSUNA.** La scelta fra anticipare il vuoto locale *(`B1`)*, curare prima `D31`, o entrambe, ### **è di Luca** |
| la variabilità fra semi | ### **UN seme** *(il `11`)*: `P3` non soddisfatta |
| i valori ASSOLUTI | ### **`U1` è aperta:** si leggono le ### **differenze fra bracci** |
| `B-T` come ### **«senza termostato»** | ### ⛔ **NON lo è:** è «senza MEMORIA del termostato», e il residuo è misurato qui sopra |
| ### **`K_SYNC = 0` come «senza sincronizzazione» nel modello finale** | ### ⚠ **è una DIAGNOSI, non una proposta:** `K_SYNC` è una costante di modulo, e portarla a zero ### **toglie una legge** — ### **non dice con che cosa sostituirla** |
| ### **la ri-esecuzione** | ### **copre i contatori COMUNI:** le voci che `D2-TER` ha aggiunto ### **non esistono** nel file vecchio, e sono ### **dichiarate escluse** nel file del confronto |
| ### **`B-SCAL-TS` come prova della DIREZIONE di Luca** | ### ⛔ **NON lo è:** il ramo scalare usa `cos(φ_k − φ_j)`, ### **non `cos((φ_k − φ_j)/2)`**. È un test sul ### **PRINCIPIO**, e un esito positivo ### **non decide la cura** |
| ### **la conservazione lungo la CORSA** | ### ⛔ **non è misurata, e non può esserlo con questi dati:** servirebbe il lavoro col ### **TRAPEZIO** *(la coppia valutata anche a `φ` nuove)*, che la corsa ### **non registra**. ### **Quello che è misurato è che la coppia È `−∂U/∂φ`** *(collaudo, `1.49e-15`)* |
| ### **«senza bagno»** | ### ⚠ **il bagno è SOPPRESSO, non spento:** `xi_termo` è azzerata ### **prima** di ogni passo, ma lo step lo ### **RICALCOLA** — e il residuo resta, ### **misurato** nella decomposizione di `dT` |
| ### **la finestra** | ### ⚠ **in questo braccio la frontiera del `216` NON separa le nascite da niente**, perché nascite ### **non ce ne sono**: divide ### **solo il tempo**. Le due finestre si riportano comunque *(il mandato le chiede)*, e `FINESTRA-PRE-NASCITA` resta la ragione per cui si riportano SEPARATE |
| la ricostruzione come ### **esatta** | ### ⛔ **NON lo è:** predice `xi` allo `0.1 %`, e il residuo è riportato |

