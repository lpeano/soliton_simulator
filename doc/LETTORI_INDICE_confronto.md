# 🔄 **`_punto_della_situazione`: PRIMA / DOPO, e le differenze SPIEGATE** *(2026-09-26)*

*(**Generato** da `csv/_confronto_pds.py`. `PRIMA` = il parser su `STATO_RUN`, salvato prima
della conversione; `DOPO` = la vista su `doc/INDICE_ID.tsv`.)*

| gruppo | PRIMA | DOPO |
|---|--:|--:|
| (senza marcatore) | 23 | — |
| BLOCCATO | — | 5 |
| CON RISERVA | 3 | 43 |
| DIFETTI E SOSPETTI | 47 | 47 |
| FATTO | 17 | 31 |
| IN CODA | 13 | 9 |
| **task elencati** | **60** | **95** |

## LE TRE CLASSI DI DIFFERENZA

### ➕ **68 voci COMPARSE — e' un GUADAGNO**

Il vecchio leggeva **solo `STATO_RUN`**; l'indice copre **tutti i registri**. Percio' compaiono
voci che prima **non si vedevano affatto**: `CLI-1`, `E4-LAM`, `INERZIA-1(C)`, `LETTORI-INDICE`, `NODI-1`, `OKN-ASSERT`, `POTENZE-1`, `RAMPA-1`, `REPERTI-IMMUTABILI`, `RIPIEGO-1`, `RIPRESA-ARGV`, `S09`, `S10`, `S12`…

### ➖ **30 voci SPARITE perche' SENZA MARCATORE — e' il FILTRO, dichiarato**

Il vecchio prendeva il marcatore dalla **QUARTA cella**; l'indice lo prende dalla **prima e
dall'ultima**, che e' dove una riga dichiara il **proprio** stato. **Dove il marcatore sta in una
cella INTERMEDIA, l'indice non lo vede** — e non lo allargo: le celle di mezzo contengono **le
prove**, che citano i `✅` di ALTRE voci. *(E' lo stesso difetto che questo strumento aveva gia'
curato una volta: prendere un `✅` che non e' suo.)*

Sono: `A1-COSTANTI`, `A1-TREVIE`, `A2-ANELLO`, `A2-DXD`, `A3-CHIRALE`, `A4-METRICHE`, `A5-PANNELLO`, `A6-PERCCHI`, `B1`, `B10`, `B2`, `B3`, `B4`, `B5`, `B6`, `B7`, `B8`, `B9`, `D0`, `E3`, `G2`, `I1`, `I4`, `I5`, `PROVA-COMB`, `REG-A`, `REG-B`, `REG-C`, `REG-R`, `REG-V`.

### ➖ **3 voci SPARITE perche' NON SONO ID — e' un GUADAGNO** 

| voce | perche' non e' un ID |
|---|---|
| `S-MIT2` | lo **stem e' UNA lettera** prima del trattino: la forma degli ID ne chiede almeno due. **Serve una rinomina, non una regex piu' larga.** |
| `_verifica_registro.py` | **e' un nome di file**: il vecchio parser lo listava come un task |
| `doc/PATTERN_DI_PROVA.md` | **idem**: un percorso, non una voce |

> ### **Due delle tre classi sono migliorie:** l'indice **vede piu' registri** e **non inventa
> ### task dai nomi di file**. La terza e' un **costo dichiarato**, non un difetto nascosto.

## ⚠ COSA QUESTO CONFRONTO *NON* DICE

- **non dice che i due documenti siano equivalenti**: dicono cose diverse su popolazioni
  diverse, ed e' il punto del cambio di fonte.
- **l'elenco delle voci «non ID» e' un mio giudizio**, scritto in `NON_ID` dentro lo script:
  si corregge in un posto solo.
