# -*- coding: utf-8 -*-
"""ESTRATTO GREZZO DEL RAMO D per Claude web -- perche' possa RIFARE I CONTI da solo.

⚠ PERCHE' ESISTE: il 2026-09-21 una tabella **ricopiata a mano** ha rovesciato una conclusione su
  `peq`, e se n'e' accorto **chi aveva letto il file grezzo invece del commit**. **Un estratto che
  permette di ricalcolare tutto rende quell'errore visibile a chiunque, subito.**

COSA PRODUCE: un `.npz` COMPRESSO per snapshot, con **tutto il necessario per ricostruire `src` e
`n1` ESATTAMENTE come fa il codice**, piu' un `README` che dice cosa significa ogni campo.

⚠ `rho` E' PER ARCO, NON PER NODO, e va detto perche' e' il punto in cui ci si sbaglia:
  il codice fa `I = |psi|**2` (per NODO) e poi **`rho = 0.5*(I[i] + I[j])`** (per ARCO), `:4167`.
  Qui si esporta `I` per nodo, e il `README` dice come si ricompone. Cosi' chi rifa' il conto usa
  la stessa definizione invece di indovinarla.

⚠ E IL PAVIMENTO DI `peq` E' `1e-9`, NON ZERO: `anom = (rho - peq)/max(peq, 1e-9)` (`:4215`).
  **Nella mia prima analisi avevo usato `1e-300`**, che e' un'altra cosa: con `peq ~ 1e-14` il
  denominatore vero e' `1e-9`, non `1e-14`. **E' esportato fra le costanti.**
ASCII PURO.
"""
import glob
import gzip
import io
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
ARCH = os.path.join(RADICE, "csv", "_test_fork", "_ab_D")
DEST = os.path.join(RADICE, "estratto_grezzo")
PASSI = (600, 1080, 1200)
N_VUOTO = 900
# ⚠ CORRETTO IL 2026-09-21 -- ERRORE TROVATO DA CLAUDE WEB rifacendo i conti sull'estratto.
#   `N0` era preso dal PRIMO SNAPSHOT ESPORTATO (passo 600, n = 2986) invece che dallo STATO
#   INIZIALE: cosi' i 595 nodi con indice 2391-2985 -- che sono NATI prima del passo 600 --
#   risultavano MASSA, e le masse contavano 2086 invece di 1491. Al passo 600 NESSUN nodo
#   risultava nato, mentre 595 lo erano.
#   E' la STESSA famiglia dell'errore della tabella ricopiata: un valore dedotto da cio' che
#   avevo sotto mano invece che dalla sua definizione.
#   MISURATO DAL DISCO, non ricordato: `avvia_test('N-MASSE')` con nmasse=3, sep=4.0 da
#   n = 2391 alla semina, e `SEME_INIZIALE = 900`.
N0_SEMINA = 2391       # vuoto = [0,900)   masse = [900,2391)   nati = >= 2391
COST = dict(ALPHA_M=0.05, ALPHA_NAT=0.0, DT=0.01, CS_M=2.0, K_C=2.0, LAM=0.8,
            PAVIMENTO_PEQ=1e-9, HAM_SRC=0.0, VERLET=1, CFL_n1_coef=0.02, CFL_n3_coef=0.05)


def main():
    os.makedirs(DEST, exist_ok=True)
    fatti = []
    for k in PASSI:
        p = os.path.join(ARCH, "scena_%06d.pkl.gz" % k)
        if not os.path.exists(p):
            print("  MANCA %s" % p); continue
        with gzip.open(p, "rb") as f:
            s = pickle.load(f)
        a = s["attrs"]
        i = np.asarray(a["i"], np.int32); j = np.asarray(a["j"], np.int32)
        psi = np.asarray(a["psi"])
        I = (np.abs(psi) ** 2).astype(np.float32)
        n = len(I)
        orig = np.where(np.arange(n) < N_VUOTO, 0,
                        np.where(np.arange(n) < N0_SEMINA, 1, 2)).astype(np.int8)
        d = dict(
            # --- per ARCO
            arco_i=i, arco_j=j,
            arco_d=np.asarray(a["d"], np.float32),
            arco_d0=np.asarray(a["d0"], np.float32),
            arco_vd=np.asarray(a["vd"], np.float32),
            arco_peq=np.asarray(a["peq"], np.float32),
            arco_tw=np.asarray(a["tw"], np.float32),
            # --- per NODO
            nodo_I=I,
            nodo_eta=np.asarray(a["eta"], np.float32),
            nodo_origine=orig,
            nodo_perc_chi=np.asarray(a["perc_chi"], np.int8),
            nodo_perc_geom=np.asarray(a.get("perc_geom", np.zeros(n)), np.int8),
            # --- identita'
            meta_passo=np.int32(k), meta_n=np.int32(n), meta_archi=np.int32(len(i)),
        )
        for c, v in COST.items():
            d["cost_" + c] = np.float64(v)
        out = os.path.join(DEST, "ramoD_passo_%06d.npz" % k)
        np.savez_compressed(out, **d)
        mb = os.path.getsize(out) / 2 ** 20
        fatti.append((k, n, len(i), mb, s.get("blob")))
        print("  passo %6d  n=%5d  archi=%7d  ->  %.2f MB" % (k, n, len(i), mb))

    tot = sum(x[3] for x in fatti)
    R = io.open(os.path.join(DEST, "README.md"), "w", encoding="utf-8", newline="\n")
    R.write("""# ESTRATTO GREZZO DEL RAMO D — **per rifare i conti da soli**

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
""")
    for k, n, na, mb, _ in fatti:
        R.write("| `ramoD_passo_%06d.npz` | %d | %d | %d | %.2f |\n" % (k, k, n, na, mb))
    R.write("""
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
""")
    for c in sorted(COST):
        R.write("- `cost_%s` = `%s`\n" % (c, COST[c]))
    R.write("""
## ⚠⚠ CORREZIONE DEL 2026-09-21 — **la prima pubblicazione aveva `nodo_origine` SBAGLIATO**

**Trovato da Claude web rifacendo i conti su questo stesso estratto** — che e' esattamente il
motivo per cui esiste.

**Cosa era sbagliato:** `N0`, il confine fra masse e nati, era preso dal **primo snapshot
esportato** (passo 600, `n = 2986`) invece che dallo **stato iniziale**. Cosi' i **595 nodi con
indice 2391-2985** — che sono **NATI** prima del passo 600 — risultavano **MASSA**:
```
             PRIMA (sbagliato)        ORA (corretto)
passo  600   vuoto 900  masse 2086  nati    0   |  vuoto 900  masse 1491  nati  595
passo 1080   vuoto 900  masse 2986  nati 1275   |  vuoto 900  masse 1491  nati 1870
passo 1200   vuoto 900  masse 2986  nati 1513   |  vuoto 900  masse 1491  nati 2108
```
**Al passo 600 nessun nodo risultava nato, mentre 595 lo erano.**

**Il valore giusto e' MISURATO dal disco, non ricordato:** `avvia_test('N-MASSE')` con `nmasse=3`,
`sep=4.0` da **`n = 2391`** alla semina, e `SEME_INIZIALE = 900`.
**Quindi: vuoto `[0,900)`, masse `[900,2391)`, nati `>= 2391`.**

> **E' la stessa famiglia dell'errore della tabella ricopiata a mano:** un valore **dedotto da cio'
> che avevo sotto mano** invece che **dalla sua definizione**. Due volte nello stesso giorno.

**La stessa correzione e' stata applicata a `csv/_analisi_ramoD.py`**, dove il difetto rendeva
sbagliate le percentuali per regione di `T3` *(e due archi erano etichettati «massa-nato» mentre
sono «nato-nato»)*.

## ⚠ COSA QUESTO ESTRATTO NON E'
- **NON e' un'analisi.** Nessun numero e' interpretato;
- **NON contiene lo stato completo:** mancano gli spinori, le fasi, `pos`, le cache. **Non si puo'
  far ripartire un run da qui** — per quello servono i `.pkl` interi;
- **NON copre l'esplosione:** il `nsub = 22591` e' **dopo** il passo 1200.
""")
    R.close()
    print("\nTOTALE %.2f MB in %s" % (tot, os.path.relpath(DEST, RADICE)))
    if tot > 50:
        print("*** SUPERA I 50 MB: fermarsi e riportare, come da mandato. ***")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
