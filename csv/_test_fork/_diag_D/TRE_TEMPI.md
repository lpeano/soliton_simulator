# `phi` CONTRO L'AZIMUT · I TRE TEMPI · CHI LEGGE COSA

> Generato da `csv/_test_fork/_tre_tempi.py`. **Blob `3d91338e`.** **Nessun run:** 15 snapshot gia' scritti e il sorgente.

## ① `phi` È L'AZIMUT DEL VETTORE DI BLOCH?

> Il docstring di `_passo_spinoriale` dice *«il vettore di Bloch `n_i(phi, phi_s)`»*.
> **`_passo_spinoriale` GIRA:** chiamato a `:4620`, con `SPINORE_VIVO = True`. *(Il suo docstring si dichiara «ORFANO»: e' STALE, e `CLAUDE.md` lo dice gia'.)*
>
> **`R = |media(exp(i·Δ))|`** con `Δ = wrap(azimut − φ)`. **`R = 1`** → `φ` *è* l'azimut a meno di una costante · **`R = 0`** → nessuna relazione.
> **Il NULLO non è zero:** `√(π/4N)`, e sta nella tabella.

| braccio | passo | nodi | **`R` con `φ`** | **`R` con `phi_s`** | nullo | lettura |
|---|--:|--:|--:|--:|--:|---|
| ACCESO | 120 | 2647 | **0.1033** | 0.0948 | 0.0172 | parziale |
| ACCESO | 240 | 2694 | **0.0201** | 0.1459 | 0.0171 | **NESSUNA RELAZIONE** |
| ACCESO | 360 | 2761 | **0.1822** | 0.2466 | 0.0169 | parziale |
| ACCESO | 480 | 2836 | **0.1567** | 0.2443 | 0.0166 | parziale |
| ACCESO | 600 | 2959 | **0.0455** | 0.2075 | 0.0163 | **NESSUNA RELAZIONE** |
| SOLO-SCRITTURA | 120 | 2670 | **0.1693** | 0.1070 | 0.0172 | parziale |
| SOLO-SCRITTURA | 240 | 2703 | **0.1404** | 0.1655 | 0.0170 | parziale |
| SOLO-SCRITTURA | 360 | 2737 | **0.0849** | 0.1911 | 0.0169 | parziale |
| SOLO-SCRITTURA | 480 | 2799 | **0.1062** | 0.2049 | 0.0168 | parziale |
| SOLO-SCRITTURA | 600 | 2914 | **0.0576** | 0.1488 | 0.0164 | **NESSUNA RELAZIONE** |
| INTERO-BLOCCO | 120 | 2980 | **0.0466** | 0.0763 | 0.0162 | **NESSUNA RELAZIONE** |
| INTERO-BLOCCO | 240 | 3068 | **0.0508** | 0.0886 | 0.0160 | **NESSUNA RELAZIONE** |
| INTERO-BLOCCO | 360 | 3160 | **0.0622** | 0.0951 | 0.0158 | **NESSUNA RELAZIONE** |
| INTERO-BLOCCO | 480 | 3312 | **0.0582** | 0.0944 | 0.0154 | **NESSUNA RELAZIONE** |
| INTERO-BLOCCO | 600 | 3853 | **0.0382** | 0.0762 | 0.0143 | **NESSUNA RELAZIONE** |

## ② I TRE TEMPI, sugli stessi archi

> **`:1319` dichiara già che sono SCOLLEGATI**, e ne nomina **due** — *«il metrico `tau_p = d/cs` e l'orologio `dt_n = DT·r`»*. **Con `tau_pp` sono TRE.**
> `r` è per NODO: si proietta sugli archi con `r_arco = ½(r_i + r_j)`.
> **Il nullo della correlazione è `~1/√N`**, e sta nella tabella.

| braccio | passo | archi | `med r_arco` | `med tau_pp` | `med d/cs` | **corr(r,tau_pp)** | **corr(r,d/cs)** | **corr(tau_pp,d/cs)** | nullo |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ACCESO | 120 | 526282 | 0.8874 | 1.2840 | 0.6941 | **-0.0074** | **+0.4176** | **+0.2163** | `1.4e-03` |
| ACCESO | 240 | 526336 | 0.5065 | 1.2597 | 0.8391 | **-0.2411** | **+0.5137** | **-0.0750** | `1.4e-03` |
| ACCESO | 360 | 526416 | 0.6970 | 1.2323 | 1.0684 | **-0.2516** | **+0.2949** | **-0.0662** | `1.4e-03` |
| ACCESO | 480 | 526512 | 0.3396 | 1.2426 | 1.2783 | **-0.0543** | **+0.0731** | **-0.0677** | `1.4e-03` |
| ACCESO | 600 | 526658 | 1.4036 | 1.2918 | 1.5363 | **-0.0391** | **+0.0518** | **-0.0385** | `1.4e-03` |
| SOLO-SCRITTURA | 120 | 526314 | 1.1837 | 1.3360 | 0.7576 | **-0.0575** | **+0.2830** | **+0.1488** | `1.4e-03` |
| SOLO-SCRITTURA | 240 | 526357 | 0.6598 | 1.4164 | 0.9392 | **+0.0489** | **+0.5440** | **+0.0340** | `1.4e-03` |
| SOLO-SCRITTURA | 360 | 526396 | 0.7391 | 1.4064 | 1.0426 | **+0.0085** | **+0.5131** | **+0.0092** | `1.4e-03` |
| SOLO-SCRITTURA | 480 | 526474 | 0.9664 | 1.3711 | 1.1452 | **-0.0275** | **+0.4777** | **+0.0005** | `1.4e-03` |
| SOLO-SCRITTURA | 600 | 526617 | 0.9916 | 1.3547 | 1.2254 | **-0.0503** | **+0.3147** | **-0.0258** | `1.4e-03` |
| INTERO-BLOCCO | 120 | 526688 | 0.9391 | 1.1410 | 0.7648 | **+0.1983** | **+0.2651** | **+0.4799** | `1.4e-03` |
| INTERO-BLOCCO | 240 | 526796 | 0.4453 | 1.1002 | 0.9570 | **+0.0039** | **+0.0920** | **+0.2344** | `1.4e-03` |
| INTERO-BLOCCO | 360 | 526906 | 0.3841 | 1.1003 | 1.0993 | **+0.2614** | **+0.1561** | **+0.1723** | `1.4e-03` |
| INTERO-BLOCCO | 480 | 527094 | 1.3602 | 1.1181 | 1.2336 | **+0.0142** | **+0.0748** | **+0.1290** | `1.4e-03` |
| INTERO-BLOCCO | 600 | 527745 | 0.7868 | 1.1525 | 1.4223 | **+0.0670** | **+0.0909** | **+0.1018** | `1.4e-03` |

## ③ CHI LEGGE COSA — dall'AST

**Funzioni che toccano almeno uno dei tre tempi: 10.**

| funzione | `r` / `dt_n` | `tau_pp` | `d/cs` |
|---|---|---|---|
| `__init__` | `_r_corrente` | — | `_cs_nodo_prev` |
| `_bloch_ritardato` | `dt_n`, `r_loc` | — | `_tempo_luce_nodo` |
| `_diag_completa` | `ritmo` | — | — |
| `_eredita_spinore_figli` | — | — | `_cs_nodo_prev` |
| `_gusci_esterni` | `ritmo` | — | — |
| `_passo_spinoriale` | `dt_n` | — | `_tempo_luce_nodo` |
| `_tempo_luce_nodo` | — | — | `cs_nodo` |
| `batch_condensazione` | `ritmo` | — | — |
| `mitosi` | — | `tau_a`, `tau_locale`, `tau_nodo`, `tau_pp`, `tau_soglia`, `tau_tetto` | — |
| `step` | `_r_corrente`, `dt_n`, `ritmo` | — | `_cs_nodo_prev`, `cs_nodo` |

**Combinazioni:**

| quali tempi | quante funzioni |
|---|--:|
| `d/cs (tempo-luce)` + `r (dt_n)` | 4 |
| `r (dt_n)` | 3 |
| `d/cs (tempo-luce)` | 2 |
| `tau_pp` | 1 |

**LIMITI: UN seme, UNA scena, 15 snapshot. NESSUNA unificazione, nessuna proposta: si misura, si registra, e decide Luca al `CHK3`.**
