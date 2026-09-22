# IL FRENO: **le BANDE di `d0/LAM`** e **il TEST DEL CRICCHETTO**

> Punto 5 del mandato dei sospesi. Generato da `csv/_test_fork/_freno_bande_e_cricchetto.py`.
> **`LAM = 0.8`, letto dal sorgente.** Le bande sugli snapshot gia' scritti; il cricchetto e' **interamente sintetico**.

## (b) IL TEST DEL CRICCHETTO — **`_smorza` da solo, su rumore SIMMETRICO**

> **Nessun simulatore, nessuno snapshot.** Rumore a media **esattamente** nulla *(antitetico: ogni `+a` ha il suo `-a`)*, **lontano dal confine**.

| caso | `x0/LAM` | `LAM` | deriva MISURATA | attesa `E[LAM/x]` | scarto | `min(x)/LAM` | esito |
|---|--:|--:|--:|--:|--:|--:|---|
| b1 il freno VERO, `x0 = 10*LAM` | 10 | 0.8000 | **+1.582064e-03** | +1.582007e-03 | 0.0 % | 8.16 | PASS |
| b1 il freno VERO, `x0 = 100*LAM` | 100 | 0.8000 | **+1.595602e-03** | +1.596143e-03 | 0.0 % | 78.62 | PASS |
| **b2 IL CASO CHE DEVE FALLIRE: `LAM = 0`** | 10 | 0.0000 | **+0.000000e+00** | +0.000000e+00 | 0.0 % | 7.67 | PASS: nessuna deriva, come DEVE essere |
| **b3 IL CASO CHE DEVE FALLIRE: freno SIMMETRICO** | 10 | 0.8000 | **+5.927976e-09** | +0.000000e+00 | 0.0 % | 7.67 | PASS: nessuna deriva, come DEVE essere |

> **`b1` — l'attesa e' DERIVATA, non tarata:** per rumore gaussiano simmetrico
> `E[-dx | dx<0]*P(dx<0) = sigma/sqrt(2 pi)`, e ogni discesa perde la frazione `LAM/x`.
> **deriva per passo = `sigma/sqrt(2 pi) * LAM/x`.**
> **`b2` e `b3` sono i casi che DEVONO dare zero**, e sono il motivo per cui `b1` si puo'
> leggere: senza di loro una deriva potrebbe venire dal banco di prova o dalla semplice
> attenuazione, invece che dall'ASIMMETRIA.


## (a) LE BANDE DI `d0/LAM` — **dove il freno morde**

> La **frazione annullata** di una discesa e' `LAM/d0`: a `d0 = 1.1*LAM` il freno annulla il **`90.9 %`** di ogni discesa, a `d0 = 3*LAM` il **`33.3 %`**.
>
> **⚠ LA QUOTA DEL FRENO E' UNA STIMA, e lo dico prima di scriverla:** gli snapshot hanno `d0` ma **NON `dx`**. La quota vale **sotto l'ipotesi DICHIARATA** che le discese siano distribuite in modo uniforme fra le bande. **Popolazione e frazione annullata sono invece ESATTE.**

### G4 riferimento

| passo | banda `d0/LAM` | archi | quota archi | frazione annullata `LAM/d0` (mediana) | **quota STIMATA del freno** |
|--:|---|--:|--:|--:|--:|
| 120 | `[1.0, 1.1)` | 44059 | 8.37 % | 0.9722 | **13.43 %** |
| 120 | `[1.1, 1.5)` | 139100 | 26.43 % | 0.7671 | **33.96 %** |
| 120 | `[1.5, 2.0)` | 168716 | 32.06 % | 0.5615 | **30.37 %** |
| 120 | `[2.0, 3.0)` | 156176 | 29.68 % | 0.4129 | **20.43 %** |
| 120 | `>= 3.0` | 18231 | 3.46 % | 0.3181 | **1.80 %** |
| 240 | `[1.0, 1.1)` | 41504 | 7.89 % | 0.9763 | **15.35 %** |
| 240 | `[1.1, 1.5)` | 69923 | 13.28 % | 0.7694 | **20.70 %** |
| 240 | `[1.5, 2.0)` | 110542 | 21.00 % | 0.5659 | **24.10 %** |
| 240 | `[2.0, 3.0)` | 162936 | 30.96 % | 0.4200 | **25.98 %** |
| 240 | `>= 3.0` | 141431 | 26.87 % | 0.2573 | **13.88 %** |
| 360 | `[1.0, 1.1)` | 53361 | 10.14 % | 0.9918 | **23.52 %** |
| 360 | `[1.1, 1.5)` | 48854 | 9.28 % | 0.7755 | **17.18 %** |
| 360 | `[1.5, 2.0)` | 54249 | 10.31 % | 0.5747 | **14.11 %** |
| 360 | `[2.0, 3.0)` | 110427 | 20.98 % | 0.4025 | **20.24 %** |
| 360 | `>= 3.0` | 259527 | 49.30 % | 0.2080 | **24.94 %** |
| 480 | `[1.0, 1.1)` | 63903 | 12.14 % | 0.9984 | **30.63 %** |
| 480 | `[1.1, 1.5)` | 43182 | 8.20 % | 0.7878 | **16.55 %** |
| 480 | `[1.5, 2.0)` | 40273 | 7.65 % | 0.5741 | **11.32 %** |
| 480 | `[2.0, 3.0)` | 73916 | 14.04 % | 0.4021 | **14.64 %** |
| 480 | `>= 3.0` | 305238 | 57.97 % | 0.1742 | **26.86 %** |
| 600 | `[1.0, 1.1)` | 72373 | 13.74 % | 0.9996 | **35.80 %** |
| 600 | `[1.1, 1.5)` | 39205 | 7.44 % | 0.7821 | **15.42 %** |
| 600 | `[1.5, 2.0)` | 39027 | 7.41 % | 0.5772 | **11.33 %** |
| 600 | `[2.0, 3.0)` | 58391 | 11.09 % | 0.4065 | **12.00 %** |
| 600 | `>= 3.0` | 317676 | 60.32 % | 0.1506 | **25.45 %** |

### G4 senza memoria del moto

| passo | banda `d0/LAM` | archi | quota archi | frazione annullata `LAM/d0` (mediana) | **quota STIMATA del freno** |
|--:|---|--:|--:|--:|--:|
| 120 | `[1.0, 1.1)` | 35576 | 6.76 % | 0.9728 | **10.19 %** |
| 120 | `[1.1, 1.5)` | 193451 | 36.76 % | 0.7427 | **43.47 %** |
| 120 | `[1.5, 2.0)` | 173641 | 32.99 % | 0.5830 | **30.02 %** |
| 120 | `[2.0, 3.0)` | 119202 | 22.65 % | 0.4615 | **15.90 %** |
| 120 | `>= 3.0` | 4448 | 0.85 % | 0.3189 | **0.42 %** |
| 240 | `[1.0, 1.1)` | 54144 | 10.29 % | 0.9545 | **16.53 %** |
| 240 | `[1.1, 1.5)` | 136818 | 25.99 % | 0.8028 | **34.82 %** |
| 240 | `[1.5, 2.0)` | 105556 | 20.05 % | 0.5793 | **19.58 %** |
| 240 | `[2.0, 3.0)` | 203251 | 38.61 % | 0.4002 | **26.44 %** |
| 240 | `>= 3.0` | 26588 | 5.05 % | 0.3157 | **2.63 %** |
| 360 | `[1.0, 1.1)` | 71731 | 13.63 % | 0.9716 | **24.28 %** |
| 360 | `[1.1, 1.5)` | 87170 | 16.56 % | 0.7846 | **24.01 %** |
| 360 | `[1.5, 2.0)` | 84542 | 16.06 % | 0.5768 | **17.15 %** |
| 360 | `[2.0, 3.0)` | 161495 | 30.68 % | 0.3926 | **22.75 %** |
| 360 | `>= 3.0` | 121460 | 23.07 % | 0.2760 | **11.81 %** |
| 480 | `[1.0, 1.1)` | 66076 | 12.55 % | 0.9805 | **24.45 %** |
| 480 | `[1.1, 1.5)` | 74152 | 14.08 % | 0.7902 | **22.29 %** |
| 480 | `[1.5, 2.0)` | 67711 | 12.86 % | 0.5743 | **14.89 %** |
| 480 | `[2.0, 3.0)` | 125490 | 23.84 % | 0.3939 | **19.19 %** |
| 480 | `>= 3.0` | 193047 | 36.67 % | 0.2611 | **19.19 %** |
| 600 | `[1.0, 1.1)` | 48159 | 9.14 % | 0.9808 | **20.06 %** |
| 600 | `[1.1, 1.5)` | 56827 | 10.79 % | 0.7800 | **19.07 %** |
| 600 | `[1.5, 2.0)` | 60208 | 11.43 % | 0.5728 | **14.87 %** |
| 600 | `[2.0, 3.0)` | 118895 | 22.58 % | 0.4007 | **20.69 %** |
| 600 | `>= 3.0` | 242530 | 46.05 % | 0.2473 | **25.32 %** |


## GLI ESITI, contro i criteri scritti PRIMA

- **(b) il cricchetto: **CONFERMATO** — il freno crea deriva su rumore a media nulla, e i due casi che devono dare zero la danno.**
- **(a) le bande:** popolazione e frazione annullata sono **esatte**; la quota del freno e' una **stima sotto ipotesi dichiarata**.

**LIMITI:** le bande vengono da UN seme, UNA scena, archivi delle cure. Il cricchetto e' **sintetico e non dipende da nessun run**: e' una proprieta' della FORMULA, e vale per qualunque seme.
