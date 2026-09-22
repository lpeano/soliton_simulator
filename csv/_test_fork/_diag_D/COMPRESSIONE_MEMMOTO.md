# L'IPOTESI DELLA COMPRESSIONE — **`S08_proj` alza `d0` senza che `d` segua?**

> Ipotesi di Luca, 2026-09-22. Generato da `csv/_test_fork/_compressione_memmoto.py`.
> **Nessun run:** i due bracci di `G4`, blob `ab685eac`, seme `42`, UN seme, UNA scena.

## PROVA 1 — **fra i DUE BRACCI, allo stesso passo**

> Se `S08_proj` alza `d0` **senza che `d` segua**, spegnendolo **`d0` deve scendere molto
> piu' di `d`**. Il numero che decide e' il **rapporto fra le due sensibilita'**.

| passo | `med d0` acceso | spento | **`Δd0/d0`** | `med d` acceso | spento | **`Δd/d`** | **rapporto** | `med d/d0` acceso | spento |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 120 | 1.4150 | 1.2534 | **-11.42 %** | 1.0501 | 1.0358 | **-1.37 %** | **8.35** | 0.8442 | 0.8750 |
| 240 | 1.7450 | 1.4566 | **-16.53 %** | 1.3632 | 1.2857 | **-5.69 %** | **2.91** | 0.7875 | 0.9505 |
| 360 | 2.3706 | 1.7082 | **-27.94 %** | 1.4342 | 1.3895 | **-3.11 %** | **8.97** | 0.6938 | 0.9739 |
| 480 | 2.9180 | 1.9804 | **-32.13 %** | 1.6040 | 1.5106 | **-5.83 %** | **5.52** | 0.6922 | 0.9449 |
| 600 | 3.3180 | 2.2559 | **-32.01 %** | 1.8823 | 1.6382 | **-12.97 %** | **2.47** | 0.7489 | 0.8546 |

**IL RAPPORTO va da `2.47` a `8.97` — **REGGE**: `d0` e' almeno `2x` piu' sensibile di `d` su TUTTI gli snapshot.**

## PROVA 2 — **TRASVERSALE, a UN SOLO ISTANTE, nel braccio ACCESO**

> `proj` ricostruito **esattamente come il codice** (`:5657-5669`), col clip `0.01*median(d0)`.
> **Nessun tempo nel test** *(par.9: una spiegazione temporale si decide su un istante)*.

| passo | archi | **`proj > 0`** | `med proj` | `somma proj` | al clip | **corr(`proj`, `d/d0`)** | nullo `1/√N` |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 120 | 526282 | **57.66 %** | +1.4150e-02 | +1.1401e+03 | 0.8679 | **-0.1948** | `1.4e-03` |
| 240 | 526336 | **64.34 %** | +1.7450e-02 | +2.6236e+03 | 0.8931 | **-0.3258** | `1.4e-03` |
| 360 | 526418 | **58.63 %** | +1.5588e-02 | +2.0941e+03 | 0.7836 | **-0.4441** | `1.4e-03` |
| 480 | 526512 | **51.43 %** | +3.3713e-04 | +3.9249e+02 | 0.7947 | **-0.4238** | `1.4e-03` |
| 600 | 526672 | **47.36 %** | -4.4150e-03 | -8.3946e+02 | 0.844 | **-0.3607** | `1.4e-03` |

## LE LETTURE, fissate PRIMA

1. **PROVA 1:** REGGE se `|Δd0/d0| / |Δd/d| >= 2` ovunque · CADE se sta fra `0.8` e `1.25` · altrimenti **NON DECISO**.
2. **PROVA 2:** REGGE se `proj > 0` in piu' del `60 %` degli archi **e** la correlazione con `d/d0` e' **negativa** e **sopra il suo nullo `1/√N`**.

**⚠ IL LIMITE DELLA PROVA 2, dichiarato PRIMA di vedere i numeri:** `proj` e' l'incremento **ISTANTANEO**, `d/d0` e' una **STORIA**. Un nullo qui **non refuta**: dice che l'istantaneo non predice la storia. **La PROVA 1 e' quella che decide.**

**LIMITI: UN seme, UNA scena, 600 passi, archivi delle cure (blob `ab685eac`).**
