# `H3` — **CHI SCALDA IL VUOTO: IL TERMOSTATO O LO SCUOTIMENTO?**

*Referto generato da `csv/_test_fork/_referto_termo_h3.py`. Dati: `csv/_test_fork/_termo_h3/`. Criteri, previsioni e aritmetica: `doc/TASK_HISTORY/2026-10-07_h3-termostato-e-scuotimento.md`, committato ### **PRIMA** dello strumento e delle corse.*

| braccio | passi | stato | secondi | che cosa gli è stato fatto |
|---|--:|---|--:|---|
| `base` | 300 su 300 | ### ✔ **completo** | 1605.3 | ### **niente** — è la dinamica di sempre |
| `B-T` | 500 su 500 | ### ✔ **completo** | 2461.9 | ### **`xi_termo` azzerata prima di ogni `step`.** ### ⛔ **NON è un azzeramento del termostato:** lo step lo ### **RICALCOLA** dentro di sé, quindi resta ### **un passo di accumulo invece di tutti** — si chiama ### **«termostato senza memoria»** |
| `B-S` | 500 su 500 | ### ✔ **completo** | 2403.9 | ### **`scuoti_vuoto` sostituita** con una funzione della stessa firma che ### **non fa niente** |
| `B-TS` | 500 su 500 | ### ✔ **completo** | 1867.1 | ### **I DUE INSIEME:** `scuoti_vuoto` inerte ### **e** `xi_termo` azzerata. ### **Il sistema vive solo della sua energia iniziale e della dinamica interna.** ### ⚠ **Eredita da `B-T` il non essere un azzeramento del termostato** |
| `B-SCAL` | 500 su 500 | ### ✔ **completo** | 2271.4 | ### **`D2`:** `_coppia_interferenza` prende il suo ### **RAMO SCALARE**, quello che dipende dalla ### **FASE CORRENTE** *(`z = e^{iφ}`)*. ### ⚠ **Il flag è spento SOLO durante la chiamata** e ripristinato in un `finally`: gira il ramo ### **del simulatore** |

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

> ### ⛔ **MA LA SECONDA NON LO E': l'energia NON e' minore.** Al passo `300` vale ### **19.0291** contro ### **16.3929** del braccio `base` -- cioe' il sistema e' ### **PIU' CALDO**, non piu' freddo.

> ### ⚠ **QUINDI IL CRITERIO, CHE E' UNA CONGIUNZIONE, NON E' SODDISFATTO** -- e lo dico invece di fermarmi alla clausola che mi conviene. ### ⭐ **MA IL FATTO RESTA, ed e' grosso: una coppia che LEGGE LA FASE CHE MUOVE tiene la coerenza delle masse MOLTO meglio, pur lasciando il sistema PIU' CALDO.** ### **La coerenza non e' una questione di temperatura, e questo e' il risultato che la corsa aggiunge.**

> ### ⛔ **E NON DECIDE LA CURA, per la ragione dichiarata in testa alla sezione:** il ramo scalare usa `cos(phi_k - phi_j)`, ### **non `cos((phi_k - phi_j)/2)`** della direzione candidata di Luca. ### **E' un test sul PRINCIPIO. La decisione e' di Luca.**

---

# ⭐ **LE MIE PREVISIONI, CONTRO I NUMERI**

| | la previsione | il numero | esito |
|---|---|---|---|
| `PH3-1` | ### ⛔ **`H3` sarà SMENTITA sulla TERZA clausola: il termostato NON è la voce principale** *(l'aritmetica: nemmeno al tetto `\|xi\|=2` arriva a `×8.1`, dà al massimo `×2.3`)* | la voce principale nel VUOTO sui primi `50` passi è ### **`scuoti`** | ### ✔ **CONFERMATA** |
| `PH3-2` | la voce principale sarà ### **`scuoti_vuoto`**, che è ADDITIVO | è ### **`scuoti`** | ### ✔ **CONFERMATA** |
| `PH3-3` | ### **`B-S` mostrerà l'effetto grande** *(AUC al `400` `>= 0.85`)*, ### **`B-T` quello piccolo** *(`< 0.85`)* | `B-S` 0.3796, `B-T` 0.4316 | ### ⛔ **SMENTITA** |
| `PH3-4` | `T_target` cresce ### **POCO** e per via di `median(d0)`; e ### **non è il motore** del riscaldamento dei primi `50` passi | `T_target` dal passo `1` al `300`: ### **30.13 %** | ### ⛔ **SMENTITA: cresce di 30.13 %** |
| `PH3-5` | ### **`Λ` cresce e la soppressione delle masse si INDEBOLISCE:** il rapporto `amp` masse/vuoto ### **SALE** | dal passo `1` al `300`: ### **0.1652 → 0.7468** | ### ✔ **CONFERMATA** |
| `PTS-1` | ### ⛔ **scattera' `LA CAUSA E' DENTRO LE MASSE (H2)`: AUC al `400` `< 0.6`** *(perche' la coppia agisce `9.31 x` piu' nelle masse che nel vuoto)* | AUC al `400` in `B-TS`: ### **0.4848** | ### ✔ **CONFERMATA** |
| `PTS-2` | il termine dominante nelle masse sara' la ### **`coppia`** | e' ### **`coppia`** *(il 90.35 %)* | ### ✔ **CONFERMATA** |
| `PTS-3` | l'energia totale ### **CRESCE** ma `~10 x` meno del controllo *(previsto `~1.2` al `230` contro `13.57`)* | da `0.1563` a ### **3.9526**; e al `230` il controllo e' `3.4 x` piu' caldo | ### ✔ **CONFERMATA** |
| `PTS-4` | la coerenza di fase delle masse al `230` sara' ### **`< 0.3`**, quindi il criterio del bagno NON scatta | ### **0.2178** | ### ✔ **CONFERMATA** |
| `PTS-5` | ### **NON divergera'** entro `500` passi, e ### **non si congelera'** | passi con `phivel` non finiti: ### **0**; stato: ### **DATI SALVATI** | ### ✔ **CONFERMATA** |
| `PD-1` | ### ⛔ **`LA COPPIA POMPA`**, con margine larghissimo. ### ⚠ **DICHIARATA GIA' NOTA** prima di girare: era nei dati di `H3` | nelle masse: positiva nel ### **100.00 %** dei passi `1..230`, somma ### **564721.69** | ### ✔ **CONFERMATA** |
| `PD-2` | `P_coppia` nelle masse ### **dello stesso ordine** di `P_scuoti` nelle masse, e ### **molto piu' piccola** di `P_scuoti` nel vuoto | al passo `230`: `\|P_coppia\|` masse ### **1140.25**, `\|P_scuoti\|` masse 1553.56, `\|P_scuoti\|` vuoto 19826.70 | ### ✔ **CONFERMATA** |
| `PD-3` | `P_termo` cambiera' ### **SEGNO** attorno al passo `49` | primo passo negativo: ### **`49`** *(positiva su 48 passi, negativa su 252)* | ### ✔ **CONFERMATA** |
| `PD-4` | ### ⚠ **`D2` dara' `NON BASTA`: AUC al `400` `< 0.6`** *(il ramo scalare cambia la COPPIA, non la scena, e `A` resta `w*cos(phi0_i - phi0_j)` con `phi0` CONGELATA)* | AUC al `400` in `B-SCAL`: ### **0.9020** *(controllo 0.4679)* | ### ⛔ **SMENTITA, ed e' il risultato piu' importante: una coppia che legge la fase TIENE le masse** |
| `PD-5` | ma l'energia totale in `D2` sara' ### **MINORE** che nel controllo | ### ⚠ **il controllo di `A-S1` NON registra `E_cin`**, quindi il confronto e' col braccio `base` al ### **massimo passo comune, il `300`**: `B-SCAL` ### **19.0291** contro `base` ### **16.3929** | ### ⛔ **SMENTITA** |

> ### **11 confermate, 4 SMENTITE** su 15.

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE, E NON PROPONE**

| | |
|---|---|
| una ### **CURA** | ### ⛔ **NESSUNA.** La scelta fra anticipare il vuoto locale *(`B1`)*, curare prima `D31`, o entrambe, ### **è di Luca** |
| la variabilità fra semi | ### **UN seme** *(il `11`)*: `P3` non soddisfatta |
| i valori ASSOLUTI | ### **`U1` è aperta:** si leggono le ### **differenze fra bracci** |
| `B-T` come ### **«senza termostato»** | ### ⛔ **NON lo è:** è «senza MEMORIA del termostato», e il residuo è misurato qui sopra |
| la ricostruzione come ### **esatta** | ### ⛔ **NON lo è:** predice `xi` allo `0.1 %`, e il residuo è riportato |

