# `H3` — **CHI SCALDA IL VUOTO: IL TERMOSTATO O LO SCUOTIMENTO?**

*Referto generato da `csv/_test_fork/_referto_termo_h3.py`. Dati: `csv/_test_fork/_termo_h3/`. Criteri, previsioni e aritmetica: `doc/TASK_HISTORY/2026-10-07_h3-termostato-e-scuotimento.md`, committato ### **PRIMA** dello strumento e delle corse.*

| braccio | passi | stato | secondi | che cosa gli è stato fatto |
|---|--:|---|--:|---|
| `base` | 300 su 300 | ### ✔ **completo** | 1539.8 | ### **niente** — è la dinamica di sempre |
| `B-T` | 500 su 500 | ### ✔ **completo** | 2461.9 | ### **`xi_termo` azzerata prima di ogni `step`.** ### ⛔ **NON è un azzeramento del termostato:** lo step lo ### **RICALCOLA** dentro di sé, quindi resta ### **un passo di accumulo invece di tutti** — si chiama ### **«termostato senza memoria»** |
| `B-S` | 500 su 500 | ### ✔ **completo** | 2403.9 | ### **`scuoti_vuoto` sostituita** con una funzione della stessa firma che ### **non fa niente** |

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

| passo | AUC ### **`B-T`** | AUC ### **`B-S`** | AUC controllo *(`A-S1`)* |
|--:|--:|--:|--:|
| `1` | ### **0.9992** | ### **0.9991** | 0.9992 |
| `50` | ### **0.9967** | ### **0.9967** | 0.9966 |
| `150` | ### **0.9598** | ### **0.8102** | 0.9861 |
| `230` | ### **0.4973** | ### **0.1574** | 0.9023 |
| `300` | ### **0.4946** | ### **0.3551** | 0.7371 |
| `400` | ### **0.4316** | ### **0.3796** | 0.4679 |
| `500` | ### **0.4686** | ### **0.4458** | 0.4497 |

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

# ⭐ **LE MIE PREVISIONI, CONTRO I NUMERI**

| | la previsione | il numero | esito |
|---|---|---|---|
| `PH3-1` | ### ⛔ **`H3` sarà SMENTITA sulla TERZA clausola: il termostato NON è la voce principale** *(l'aritmetica: nemmeno al tetto `\|xi\|=2` arriva a `×8.1`, dà al massimo `×2.3`)* | la voce principale nel VUOTO sui primi `50` passi è ### **`scuoti`** | ### ✔ **CONFERMATA** |
| `PH3-2` | la voce principale sarà ### **`scuoti_vuoto`**, che è ADDITIVO | è ### **`scuoti`** | ### ✔ **CONFERMATA** |
| `PH3-3` | ### **`B-S` mostrerà l'effetto grande** *(AUC al `400` `>= 0.85`)*, ### **`B-T` quello piccolo** *(`< 0.85`)* | `B-S` 0.3796, `B-T` 0.4316 | ### ⛔ **SMENTITA** |
| `PH3-4` | `T_target` cresce ### **POCO** e per via di `median(d0)`; e ### **non è il motore** del riscaldamento dei primi `50` passi | `T_target` dal passo `1` al `300`: ### **30.13 %** | ### ⛔ **SMENTITA: cresce di 30.13 %** |
| `PH3-5` | ### **`Λ` cresce e la soppressione delle masse si INDEBOLISCE:** il rapporto `amp` masse/vuoto ### **SALE** | dal passo `1` al `300`: ### **0.1652 → 0.7468** | ### ✔ **CONFERMATA** |

> ### **3 confermate, 2 SMENTITE** su 5.

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE, E NON PROPONE**

| | |
|---|---|
| una ### **CURA** | ### ⛔ **NESSUNA.** La scelta fra anticipare il vuoto locale *(`B1`)*, curare prima `D31`, o entrambe, ### **è di Luca** |
| la variabilità fra semi | ### **UN seme** *(il `11`)*: `P3` non soddisfatta |
| i valori ASSOLUTI | ### **`U1` è aperta:** si leggono le ### **differenze fra bracci** |
| `B-T` come ### **«senza termostato»** | ### ⛔ **NON lo è:** è «senza MEMORIA del termostato», e il residuo è misurato qui sopra |
| la ricostruzione come ### **esatta** | ### ⛔ **NON lo è:** predice `xi` allo `0.1 %`, e il residuo è riportato |

