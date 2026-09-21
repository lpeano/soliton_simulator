# ESTRATTO GREZZO DEL RAMO D — **per rifare i conti da soli**

> **Ramo `dati-grezzi`, separato da `fork-su2`** per non appesantire il branch di lavoro.
> Prodotto da **`csv/_estratto_grezzo_D.py`** *(che vive su `fork-su2`, con la sua voce
> d'inventario)*.
> **EPOCA 2:** `CHI_COOP` + `SCALA_MIN` + `COES_ADIM` accesi, piu' la cura del mondo-dopo-i-flag.
> Simulatore **`4954fe5b`** *(sha1 dei BYTE GREZZI, non `git hash-object`: sono due numeri
> diversi)*.

## Perche' esiste
Il 2026-09-21 una tabella **ricopiata a mano** ha rovesciato una conclusione su `peq`, e se n'e'
accorto **chi aveva letto il file grezzo invece del commit**. **Questo estratto rende quell'errore
visibile a chiunque, subito.**

## I file
| file | passo | nodi | archi | MB |
|---|---:|---:|---:|---:|
| `ramoD_passo_000600.npz` | 600 | 2986 | 526709 | 9.37 |
| `ramoD_passo_001080.npz` | 1080 | 4261 | 528331 | 9.31 |
| `ramoD_passo_001200.npz` | 1200 | 4499 | 528638 | 9.29 |

**`600` e' lo snapshot SANO, `1080` e `1200` quelli in cui `peq` crolla.**
**Il run e' stato FERMATO al passo 1230** *(`nsub = 22591`)*: **nessuno snapshot copre
l'esplosione**, che avviene nei ~30 passi dopo il 1200.

## I campi

### Per ARCO (lunghezza = `meta_archi`)
| campo | significato |
|---|---|
| `arco_i`, `arco_j` | gli indici dei due NODI che l'arco collega |
| `arco_d` | la lunghezza VERA |
| `arco_d0` | la lunghezza di RIPOSO |
| `arco_vd` | la velocita' di `d` |
| `arco_peq` | la pressione di equilibrio |
| `arco_tw` | la torsione |

### Per NODO (lunghezza = `meta_n`)
| campo | significato |
|---|---|
| `nodo_I` | **`|psi|**2`** — e' la densita' PER NODO |
| `nodo_eta` | `eta` |
| `nodo_origine` | **`0` = vuoto** *(indice < 900, la semina)*, **`1` = massa**, **`2` = NATO** |
| `nodo_perc_chi` | la CARICA (segno di doppia copertura, scritta dallo spinore) |
| `nodo_perc_geom` | la GEOMETRIA (scritta da `chi_basc` dalla torsione) |

## ⚠ COME SI RICOSTRUISCE `src` E `n1` — **esattamente come il codice**

**`rho` E' PER ARCO, NON PER NODO.** E' il punto in cui ci si sbaglia:
```python
rho   = 0.5 * (nodo_I[arco_i] + nodo_I[arco_j])          # :4167
anom  = (rho - arco_peq) / np.maximum(arco_peq, 1e-9)    # :4215  <- PAVIMENTO 1e-9, NON zero
src   = cost_ALPHA_M * anom                              # :4218  (perche' ALPHA_NAT == 0)
n1    = np.ceil(np.abs(src).max() * cost_DT / (0.02 * cs_max))   # :4264, ramo VERLET
```
**Il pavimento `1e-9` conta:** con `peq ~ 1e-14` il denominatore vero e' **`1e-9`**, non `1e-14`.
*(Nella prima analisi avevo usato `1e-300`: e' un'altra cosa, ed e' un errore da non ripetere.)*

**`cs_max`** e' `max(cs_arco)` col ramo dinamico, e `cs_arco` **non e' in questo estratto**: serve
`_cs_nodo_prev`, che dipende dallo stato completo. **Come limite superiore si puo' usare
`cost_CS_M = 2.0`**, e va **dichiarato** quando lo si fa.

## Le costanti
- `cost_ALPHA_M` = `0.05`
- `cost_ALPHA_NAT` = `0.0`
- `cost_CFL_n1_coef` = `0.02`
- `cost_CFL_n3_coef` = `0.05`
- `cost_CS_M` = `2.0`
- `cost_DT` = `0.01`
- `cost_HAM_SRC` = `0.0`
- `cost_K_C` = `2.0`
- `cost_LAM` = `0.8`
- `cost_PAVIMENTO_PEQ` = `1e-09`
- `cost_VERLET` = `1`

## ⚠ COSA QUESTO ESTRATTO NON E'
- **NON e' un'analisi.** Nessun numero e' interpretato;
- **NON contiene lo stato completo:** mancano gli spinori, le fasi, `pos`, le cache. **Non si puo'
  far ripartire un run da qui** — per quello servono i `.pkl` interi;
- **NON copre l'esplosione:** il `nsub = 22591` e' **dopo** il passo 1200.
