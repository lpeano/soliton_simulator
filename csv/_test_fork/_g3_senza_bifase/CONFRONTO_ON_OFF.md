# `G3` -- LA GRAVITA' ACCESA contro LA GRAVITA' SPENTA

> **GENERATA DA CODICE** (`P1-ter`). **SOLA LETTURA** su file gia' scritti.
> Stesso blob `9557a867`, stesso seme `42`, stessa scena, stessa configurazione:
> **l'unica differenza e' `GRAV_BIFASE`.** Non e' un confronto fra epoche.

## `med d0` e `d/d0`, snapshot per snapshot

| passo | `n` ON | `n` OFF | `med d0` ON | `med d0` OFF | `d/d0` ON | `d/d0` OFF |
|--:|--:|--:|--:|--:|--:|--:|
| 120 | 2647 | 2617 | `1.4150` | `1.6372` | `0.8442` | `0.8599` |
| 240 | 2694 | 2659 | `1.7450` | `2.0375` | `0.7875` | `0.7158` |
| 360 | 2761 | 2723 | `2.3706` | `2.6744` | `0.6938` | `0.6417` |
| 480 | 2836 | 2816 | `2.9180` | `3.2029` | `0.6922` | `0.6123` |
| 600 | 2959 | 3057 | `3.3180` | `3.5951` | `0.7489` | `0.6258` |

**Il criterio `4`, il RAPPORTO fra snapshot consecutivi di `med d0`**
*(costante `> 1` = crescita ESPONENZIALE)*:

| | rapporti | MEDIANO |
|---|---|--:|
| gravita' **ACCESA** | `1.2332`, `1.3585`, `1.2309`, `1.1371` | **`1.2321`** |
| gravita' **SPENTA** | `1.2445`, `1.3126`, `1.1976`, `1.1225` | **`1.2211`** |

> **Differenza relativa del rapporto mediano: `-0.9 %`.**

## `coer_l` e `dil` dal `prog.csv` dei due run

| frame | passo | `coer_l` ON | `coer_l` OFF | `dil` ON | `dil` OFF |
|--:|--:|--:|--:|--:|--:|
| 20 | 120 | `0.3551` | `0.3212` | `-0.169 %` | `-0.199 %` |
| 40 | 240 | `0.3935` | `0.4668` | `-0.269 %` | `-0.321 %` |
| 60 | 360 | `0.5607` | `0.4527` | `-0.360 %` | `-0.381 %` |
| 80 | 480 | `0.5302` | `0.3236` | `-0.337 %` | `-0.408 %` |
| 100 | 600 | `0.3638` | `0.4810` | `-0.241 %` | `-0.399 %` |

**`coer_l`** e' la coerenza locale *(quanto le masse restano insieme)*; **`dil`** e'
la dilatazione riportata dal driver. **Non li interpreto oltre il loro andamento:**
sono due grandezze del driver, e la loro definizione esatta non e' stata riletta qui.

## ⚠ COSA QUESTO CONFRONTO NON E'

**Non e' un confronto fra epoche.** I due run condividono blob, seme, scena e configurazione;
l'unica differenza e' il flag, e il sigillo `7/7` dimostra che quella differenza e'
**chirurgica** -- `T5`, strutturale: **una sola ramificazione** dipende da `GRAV_BIFASE`.

**Non e' una misura su piu' semi.** **UN seme, UNA scena.** Per una barra fra semi ne servono
**almeno quattro** (`P3`). **Cio' che qui e' grande** *(il rapporto di `d0` che non cambia,
lo stress che cala)* **andra' comunque riconfermato.**
