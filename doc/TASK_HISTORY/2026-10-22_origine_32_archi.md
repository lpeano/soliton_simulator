# DA DOVE NASCE LA LUNGHEZZA DI `32` ARCHI DELL'INSTABILITA' DI `S1` *(su carta, nessuna corsa nuova, nessuna scelta)*

> **Il mandato:** decisione di Luca del `2026-10-22` alle `17:42`, ### **dopo le parti «materia» e «cs»** *(`b16e58ba`, `974d411a`)*.
> ### **Un DOCUMENTO: solo i dati gia' committati; `leggi.yaml` e l'impronta intatti. Le scelte sono di Luca.**

**LIVELLO:** `L2`, un documento.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica al documento**; ogni strada ha la sua risposta nella scheda.
2. **Il gradino:** ### **non si applica** *(letture e strade, nessun risultato nuovo affermato)*.
3. **Aggiunge un numero o una legge?** ### **Il documento no**; ### **le strade che lo farebbero lo DICONO.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No.**
5. **Emergente o imposto?** ### **E' la domanda del documento:** la scala di `32` archi e' della dinamica o del reticolo.

## 1. CHE COSA CREDO PRIMA *(e una dichiarazione onesta sull'ordine)*

- ### ⚠ **L'ORDINE, DICHIARATO:** ### **prima di scrivere questo task history ho GIA' letto i dati committati** *(le velocita' di gruppo
  `v_gruppo_m0` di `d0_risonanza_bis.jsonl` e `d0_risonanza_64.jsonl`)* ### **e ho GIA' fatto il conto a mano che segue.** ### **Non e'
  una previsione scritta prima dei numeri: e' una LETTURA**, e lo scrivo qui invece di presentarla come previsione.
- ### **LA LETTURA:**
  - ### **la dispersione dei rami dispersivi della camminata a onde lunghe e' QUADRATICA** *(`v_g` lineare in `k`: `0.0765`, `0.153` a
    `m = 1, 2`, lato `32`)*: ### **`omega ~ (1/2) c k^2`**, ### **`c = 0.390`** *(archi^2 per unita' di tempo proprio)* ### **a lato `32`, e
    `0.393` a lato `64`**: ### **la stessa in unita' d'arco a tutte e due le taglie.**
  - ### **A `k = 0.0625 pi` la camminata e' nel suo regime di CONTINUO** *(lo scarto dalla parabola e' sotto l'`1%`)*: ### **i `32` archi
    NON sono un errore di discretizzazione della dispersione.**
  - ### **IL MODELLO MINIMO** *(l'instabilita' modulazionale di una parabola: il massimo dove `(1/2) c k^2 = gamma`)* ### **mette il
    massimo a `k = sqrt(2 gamma / c)`**: ### **per `S1` a `x 0.1`** *(`gamma` `0.0057`)* ### **`0.0545 pi`**, ### **fra i punti della griglia,
    piu' vicino a `0.0625 pi` a tutte e due le taglie.**
  - ### **QUINDI** *(il criterio del mandato)*: ### **`L = 2 pi / k = 2 pi sqrt(c / (2 gamma))` e' un rapporto fra `c` e `gamma`, tutte e due
    INVARIANTI in unita' d'arco e di tempo proprio sotto la regola di scala** *(`c` misurata alle due taglie, `gamma` misurato alle due
    taglie, `cb846b2a`)*: ### **e' NECESSARIAMENTE fissa in archi.**
- ### **CHE COSA NON SO:** ### **se il modello minimo regge su tutta la tabella** *(lo dira' lo script sui dati committati: `k` previsto
  contro `k` misurato, per `S1`, `S4`, `S3` e ogni `x`)*; ### **la `c` sui triangoli** *(non e' nei dati committati)*.
- ### **E COSA CREDO DELLE STRADE:** ### **un miglioramento alla Symanzik NON tocca i `32` archi** *(la dispersione e' gia' nel continuo
  li')*; ### **un taglio ultravioletto NON li tocca** *(e' un'onda LUNGA)*; ### **la scala e' nella REGOLA DI SCALA** *(come `c` e il tempo
  si trasformano raffinando)*, ### **che e' di Luca.**

### ⚠ **ANNOTAZIONE DOPO LO SCRIPT** *(`doc/referti_l2/origine_32_archi.txt`)*: ### **lo scarto dalla parabola a lato `32` e' `1.25%`**
*(`v_g(2)/v_g(1) = 1.975`)*, ### **non «sotto l'`1%`» come avevo scritto sopra**; a lato `64` `0.3%`. ### **`c` `0.3894` e `0.3882`** *(non `0.390` e
`0.393`: il conto a mano usava un ramo solo)*. ### **La lettura non cambia.**

## 2. LA PROGETTAZIONE

1. ### **`csv/_origine_32_archi.py`**: ### **legge SOLO i `jsonl` committati** *(`d0_risonanza_bis`, `d0_risonanza_64`, `lineare_s1_s4_*`,
   `screening_forme_s3`, `s3_diluita`)*, ### **stampa `c` alle due taglie e la tabella del `k` previsto contro il misurato**: ### **nessuna
   corsa del simulatore** *(`L-NUMERI`: ogni numero del documento esce da uno script)*.
2. ### **`doc/ORIGINE_32_ARCHI.md`**: il contesto *(con le due letture di Luca alla lettera)*, il meccanismo, le strade *(Symanzik, il
   taglio dall'olonomia, le mie)*, ### **la sezione onesta** *(un argomento per cui l'artefatto non si elimina)*.
3. ### **La relazione: la sintesi e UNA domanda.** ### **NESSUNA SCELTA.**

### ⛔ **COSA MI FA FERMARE:** ### **un numero che servirebbe e non e' nei dati committati** *(lo si dice, non si corre)*.
