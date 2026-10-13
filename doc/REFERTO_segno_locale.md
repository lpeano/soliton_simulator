# `(D1)` LO STRUMENTO LOCALE `q` — **validato, e una mia previsione CADE**

> ### ⛔ **LA PREVISIONE `+0.9438` ERA SBAGLIATA, e l'errore e' preciso:** quel numero viene
> da `B3`, misurato su un **ANELLO DI 16 NODI**, e io l'ho previsto per un **TORO `10x10`**.
> ### ⚠ **La correlazione dipende dai pesi `sin(omega_k)`, cioe' DALLO SPETTRO, cioe'
> DALLA SCENA.** ### ✅ **E la previsione era giusta PER LA SUA SCENA: sull'anello-16 fa
> `+0.9345`, dentro `0.01`.**

Lo rigira:  `python primo_ordine/segno.py --scrivi`

## 1. LE DUE SCENE, E LA CONFIGURAZIONE INTERA

| la voce | il valore |
|---|---|
| scene | `anello-16` *(quella di `B3`)* e `toro 2D 10x10` |
| ### ⚠ **NON** la scena del banco | il banco e' **irregolare** e **congelato** |
| tick / `dtau` / seme | `400` / `0.25` / `7` |
| `U` per arco | `SU(2)` casuale |
| piattaforma | `Windows`, numpy `2.3.0` |

## 2. I BRACCI, SU ENTRAMBE LE SCENE

| scena | `dim` | memoria | `x0` | `corr` **variazioni** | `corr` **valori** | `C`: `q -> -q` | localita' |
|---|--:|--:|--:|--:|--:|--:|--:|
| `(16,)` | 64 | `0.06` MB | `0.9700` | **`+0.9345`** *(prevista `+0.9438`)* | `+0.6340` | `0.0e+00` | `0.0e+00` |
| `(10, 10)` | 800 | `9.77` MB | `0.9055` | **`+0.7543`** | `+0.6946` | `0.0e+00` | `0.0e+00` |

### ⭐ **I DUE BRACCI CHE TORNANO ESATTAMENTE, e sono i piu' importanti:**

| | il braccio | il numero |
|---|---|--:|
| `d1c` | sotto la `C` completa, `q_k -> -q_k` | ### ✅ **`0.000e+00`, ESATTO** |
| `d1d` | perturbando `psi` a distanza `>= 3`, `q_k` non cambia | ### ✅ **`0.000e+00`, ESATTO** |
| `d1d` | e ### ⛔ **DEVE cambiare** perturbando **sul nodo** | ### ✅ **`2.0`** |

### ⚠ **E `d1c` E' UN CONTROLLO DELLO STRUMENTO, NON UNA PROVA:** la
`C`-disparita' di `q_h` e' **DERIVATA** estremita' per estremita' in
`doc/TASK_HISTORY/2026-10-13_pb_ordinamento.md`. ### **Che venga `0.000e+00` ESATTO
dice che il codice fa cio' che il conto dice.**

## 3. ⛔ CHE COSA CADE, E CHE COSA RESTA

| | |
|---|---|
| ### ⛔ **cade** | la mia previsione **`+0.9438` sul toro**: ho trasferito un numero da una scena a un'altra **senza dirlo** |
| ### ✅ **resta** | lo **strumento funziona**: `C` e localita' tornano **esattamente**, e `q` segue `Q` in modo **sostanziale e positivo** su entrambe le scene |
| ### ⚠ **e si impara** | `q` segue le **VARIAZIONI** di `Q` meglio del suo **LIVELLO** *(`+0.75` contro `+0.69` sul toro; `+0.93` contro `+0.63` sull'anello)*: come proxy della **dinamica** dello squilibrio e' buono, come proxy del suo **valore assoluto** e' piu' debole |

### ⭐ **E LA CAUSA E' STRUTTURALE, non un difetto:** `q` e' un `Q` **PESATO con**
**`sin(omega_k)`**, e i pesi dipendono dallo **spettro**. ### ⛔ **Se la correlazione fosse
`+1.000` esatta sarebbe LO STRUMENTO a essere sbagliato.**

