# PUNTO `B` — **I DUE BRACCI SCADUTI DI `_collauda_deriva.py`**

*(mandato unico di Luca del `2026-10-16`, punto `B`. Base: `9406545`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE**, come il punto `B` chiede alla
> lettera: *«PRIMA di toccare il codice scrivi nel task history, per ciascun braccio, che
> cosa la legge di OGGI garantisce e perche' (derivato dalla strada `B`); solo dopo
> riscrivi il braccio su quell'affermazione, con un caso che DEVE fallire»*.

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa la legge di OGGI garantisce*

### ⭐⭐ **IL BRACCIO `(4)`: `Lambda_k` SOTTO LA CAMMINATA DEL VUOTO**

**L'affermazione di ieri** — *«con `|phi|` UNIFORME `Lambda_k` e' esattamente
invariante»* — ### **era vera quando il Grover scalare era UN'INVOLUZIONE** *(`(2/d)Σ − I`,
cioe' `theta = pi`)*: la' Grover e spostamento erano ### **permutazioni di moduli tutti
uguali.** ### ⛔ **Dalla strada `(B)` sono flussi parziali a `theta = pi dtau frazione`**, e
a `dtau = 0.2` ### **mescolano.**

> ### ⛔⛔ **ANNOTAZIONE DEL `2026-10-16` (integrazione del guardiano, verifica fino a
> `2b72739`): LE DUE RIGHE QUI SOPRA SONO SBAGLIATE SU DUE PUNTI, e NON le riscrivo —
> ### **si ANNOTANO**, come il par.`8` pretende.**
> ### ① **<<il Grover a `dtau = 0.2` MESCOLA>> e' falso**, e lo smentisce
> ### **la mia stessa `(4a)`**: il Grover del vuoto agisce ### **dentro il nodo** ed e'
> ### **unitario** la', quindi ### **conserva `Lambda_k` a QUALUNQUE frazione**
> *(misurato: `8.882e-16`)*. ### ⛔ **Quindi il rosso del braccio `(4)` veniva SOLO
> dallo SPOSTAMENTO sugli archi**, e la spiegazione che avevo scritto in `7e0a7d0`
> — *«dalla strada `(B)` e' un flusso parziale, e a `dtau = 0.2` mescola»* —
> ### **la RITIRO.**
> ### ② **e a `theta = pi` il Grover NON e' una permutazione di moduli: e' una
> RIFLESSIONE** `2 P_u − I`. ### **La permutazione e' lo SPOSTAMENTO**, e la `(4c)`
> parla di quello.
> ### ✅ **E le TRE affermazioni derivate sotto NON cambiano:** erano gia' scritte
> ### **pezzo per pezzo**, ed e' esattamente cio' che ha fatto emergere l'errore.

### **E CIO' CHE LA LEGGE DI OGGI GARANTISCE SI DERIVA DAI DUE PEZZI, uno per volta:**

| | il pezzo | che cosa conserva, e PERCHE' |
|---|---|---|
| `a` | **`CAMM-GROVER-VUOTO`**, `G(theta) = P_u + e^{i theta}(I − P_u)` | agisce ### **DENTRO IL NODO** *(mescola le estremita' di uno stesso nodo)* ed e' ### **UNITARIO** su quello spazio ⟹ ### **conserva `Lambda_k` ESATTAMENTE, per nodo, a QUALUNQUE frazione e con QUALUNQUE `|phi|`** *(uniforme o no)*. ### **Non e' una proprieta' del vuoto uniforme: e' l'unitarieta' del pezzo.** |
| `b` | **`CAMM-SPOSTAMENTO-VUOTO`**, `hop(theta) = alpha I + beta S` | agisce ### **SULL'ARCO**, e le due estremita' di un arco stanno in ### **DUE NODI DIVERSI** ⟹ conserva ### **il TOTALE `V = somma_k Lambda_k`** *(unitario sull'arco)* ma ### **MUOVE vuoto fra i nodi**: `Lambda_k` ### **CAMBIA, e deve.** ### **E' il TRASPORTO.** |
| `c` | **lo spostamento a `theta = pi`** *(`alpha = 0`, `beta = 1`)* | e' ### **una permutazione pura**: scambia le due estremita'. ### **Con `|phi|` UNIFORME i moduli scambiati sono uguali ⟹ `Lambda_k` torna invariante** — ### **l'affermazione di ieri, con la sua CONDIZIONE scritta.** |

> ### ✅ **QUINDI IL BRACCIO SI RISCRIVE SU TRE AFFERMAZIONI DERIVATE**, e nessuna di loro
> dipende da un accidente:
> ### **`(4a)` il Grover del vuoto conserva `Lambda_k` agli ulp, a ogni frazione e con
> `|phi|` NON uniforme** · ### **`(4b)` lo spostamento conserva `V` agli ulp e CAMBIA
> `Lambda_k`** · ### **`(4c)` a `theta = pi` e `|phi|` uniforme `Lambda_k` torna
> invariante.**
> ### ⛔ **E IL CASO CHE DEVE FALLIRE: `theta = pi` con `|phi|` NON uniforme** — la
> permutazione scambia moduli ### **diversi**, quindi `Lambda_k` ### **deve cambiare.**
> ### **Senza di lui `(4c)` passerebbe per vacuita'.**

### ⭐⭐ **IL BRACCIO `(6)`: L'ORDINE IN `dtau` DELLA SORGENTE**

**L'affermazione di ieri** — *«la sorgente per nodo e' `O(1)` in `dtau`, non `O(dtau^2)`»* —
### **non e' cio' che la misura dice:** il rapporto su un fattore `4` di `dtau` vale
### **`4.625`** *(legge vecchia)* e ### **`3.220`** *(legge nuova)*, cioe' ### **circa
`4`** — e `O(1)` darebbe ### **`1`.**

### **E CIO' CHE LA LEGGE DI OGGI GARANTISCE SI DERIVA:** la sorgente `s_k` e'
### **cio' che il termine `N` inietta nel nodo `k` IN UN TICK**, e il termine agisce con
### **una fase `beta dtau frazione`** — quindi al primo ordine
### **l'energia scambiata per tick e' proporzionale a `dtau`**:

```
s_k = O(dtau)   PER PASSO        (e NON O(1), e NON O(dtau^2))
```

### ✅ **E' esattamente cio' che un FLUSSO PARZIALE deve dare**, ed e' il motivo per cui il
mandato lo chiama *«cio' che un flusso parziale deve dare»*.

> ### ⛔ **IL CRITERIO, FISSATO QUI PRIMA DI MISURARE:** si misura a ### **TRE `dtau`**
> *(`0.2`, `0.05`, `0.0125`: due fattori `4`)*, e ### **l'ESPONENTE** si legge come
> `log(rapporto)/log(4)`. ### **Criterio: l'esponente sta in `[0.75, 1.25]` su ENTRAMBI i
> rapporti.**
> ### ⛔ **E i due casi che DEVONO fallire sono le due alternative:** ### **`O(1)`**
> *(esponente `0`)* e ### **`O(dtau^2)`** *(esponente `2`)* — e il braccio li esclude
> ### **con lo stesso numero**, non con due misure diverse.
> ### ⚠ **La banda `[0.75, 1.25]` e' MIA e la dichiaro:** e' larga perche' `s_k` e' un
> ### **massimo su nodi** *(non una media)*, e un massimo su `16` nodi ha una dispersione
> che non e' una barra d'errore. ### **Non la allargo dopo.**

---

## 2. PROGETTAZIONE — *i passi, e cosa mi FERMA*

| | il passo | cosa mi FERMA |
|---|---|---|
| `1` | `(4a)`: il **Grover del vuoto** conserva `Lambda_k` agli ulp, con `|phi|` NON uniforme e a due frazioni | se NON conserva: ### **l'unitarieta' del pezzo e' rotta**, e non e' un difetto del braccio — ### **mi fermo e lo riporto** |
| `2` | `(4b)`: lo **spostamento** conserva `V` e CAMBIA `Lambda_k` | se `V` non si conserva: ### **mi fermo** |
| `3` | `(4c)` + il caso che deve fallire | se il caso che deve fallire ### **passa**, il braccio e' vacuo e lo dico |
| `4` | `(6)`: l'esponente a tre `dtau` | se l'esponente non sta in `[0.75, 1.25]`: ### **l'affermazione derivata e' sbagliata**, e allora ### **il braccio si RITIRA col motivo**, come il mandato ammette |
| `5` | la suite intera | ### **esito atteso: `53` ok, `0` rossi** |

### ⛔ **E NON TOCCO IL CODICE DELLA FISICA:** i due bracci stanno in
`primo_ordine/_collauda_deriva.py`, e la funzione `lambda_sotto_vuoto` di `deriva.py`
### **va estesa** *(serve il pezzo SINGOLO e la frazione)*, non cambiata nel suo
significato. ### **Se mi trovassi a cambiare un numero della fisica per far passare un
braccio, mi fermerei.**

---

## 3. TODO

1. `deriva.lambda_sotto_vuoto`: il **pezzo** e la **frazione** come argomenti *(senza
   valori di comodo: e' una misura)*.
2. i due bracci riscritti, con i **casi che devono fallire**.
3. la suite: **`53` ok, `0` rossi**, e il tempo nel budget.
4. relazione, RIPRESA, e il referto se i numeri cambiano.
