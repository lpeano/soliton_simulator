# I TRE BRACCI DELLA MEMORIA DEL MOTO — **il confronto**

> Generato da `csv/_test_fork/_tre_bracci.py`. **Nessun run:** rilegge i 15 snapshot gia'
> scritti. Seme `42`, 600 passi, stessa scena. Blob `ab685eac` per i primi due, `21e3a3dc` per il terzo *(che aggiunge SOLO il flag, sigillato byte-inerte `10/10`)*.

COLLAUDO (`P1-sexies`), PRIMA di confrontare
--------------------------------------------------------------------------------------------
K1 legge `7/8` e IL NOME del criterio che non regge -> OK  (7/8, ['`d0` NON scappa'])
K2 IL CASO CHE DEVE FALLIRE: `LETTURE.txt` ASSENTE -> deve dare `None`, NON `0/8`
     *(un file che manca non e' "zero criteri": e' ASSENZA DI DATO, pattern 3)* -> OK
--------------------------------------------------------------------------------------------
  -> i criteri PASSANO

## L'ESITO CONTRO I CRITERI ASSOLUTI

| braccio | cosa spegne | **criteri** | quali NON reggono |
|---|---|--:|---|
| **ACCESO** | tutto attivo | **6/8** | ``d0` NON scappa`, ``d/d0` vicino a 1` |
| **SOLO-SCRITTURA** | `MEM_MOTO = False` | **7/8** | ``d0` NON scappa` |
| **INTERO-BLOCCO** | `MEM_MOTO_TUTTO = False` | **6/8** | ``d0` NON scappa`, ``d/d0` vicino a 1` |

## LE GRANDEZZE, snapshot per snapshot

### `med d0`

| passo | **ACCESO** | **SOLO-SCRITTURA** | **INTERO-BLOCCO** |
|--:|--:|--:|--:|
| 120 | 1.4150 | 1.2534 | 1.2327 |
| 240 | 1.7450 | 1.4566 | 1.4093 |
| 360 | 2.3706 | 1.7082 | 1.6486 |
| 480 | 2.9180 | 1.9804 | 2.2519 |
| 600 | 3.3180 | 2.2559 | 2.8995 |

### `med d`

| passo | **ACCESO** | **SOLO-SCRITTURA** | **INTERO-BLOCCO** |
|--:|--:|--:|--:|
| 120 | 1.0501 | 1.0358 | 1.0309 |
| 240 | 1.3632 | 1.2857 | 1.3724 |
| 360 | 1.4342 | 1.3895 | 1.3880 |
| 480 | 1.6040 | 1.5106 | 1.5511 |
| 600 | 1.8823 | 1.6382 | 1.7303 |

### **`med d/d0`**

| passo | **ACCESO** | **SOLO-SCRITTURA** | **INTERO-BLOCCO** |
|--:|--:|--:|--:|
| 120 | 0.8442 | 0.8750 | 0.9982 |
| 240 | 0.7875 | 0.9505 | 1.0005 |
| 360 | 0.6938 | 0.9739 | 0.9999 |
| 480 | 0.6922 | 0.9449 | 0.8625 |
| 600 | 0.7489 | 0.8546 | 0.7886 |

### `n`

| passo | **ACCESO** | **SOLO-SCRITTURA** | **INTERO-BLOCCO** |
|--:|--:|--:|--:|
| 120 | 2647 | 2670 | 2980 |
| 240 | 2694 | 2703 | 3068 |
| 360 | 2761 | 2737 | 3160 |
| 480 | 2836 | 2799 | 3312 |
| 600 | 2959 | 2914 | 3853 |

## IL RAPPORTO MEDIANO DI `med d0` FRA SNAPSHOT — **la fuga**

| braccio | rapporto mediano | `med d0` finale | lettura |
|---|--:|--:|---|
| **ACCESO** | **1.2320** | 3.3180 | costante `> 1` = **ESPONENZIALE** |
| **SOLO-SCRITTURA** | **1.1607** | 2.2559 | costante `> 1` = **ESPONENZIALE** |
| **INTERO-BLOCCO** | **1.2287** | 2.8995 | costante `> 1` = **ESPONENZIALE** |
