# `L1` — SECONDA PARTE: **il passo PALINDROMO, e lo spettro**

> **Decisioni di Luca del 2026-10-15, 12:43–12:44.** Ultimo commit verificato dal
> guardiano: `0ce59ba`.
>
> ### ⛔ **E SI SCRIVE PRIMA DEL CODICE**, come il paragrafo 8 pretende: il commit di questo
> file e' **antenato** di quelli del lavoro.

---

## 0. ⛔ **DUE ERRORI MIEI, PRIMA DI TUTTO IL RESTO**

### ⚠ **① I DUE CRITERI NON POTEVANO VALERE INSIEME, E LI AVEVO RIPORTATI SENZA
CONTROLLARLI.** `M-B1` *(il passo intero al bit come `717bb60`)* e `M-B2` *(errore
`O(dtau^2)`)* **si escludono**, e io me ne sono accorto **solo dopo averli misurati
entrambi**. ### **Li avevo presi dalla mappa e riportati come se fossero compatibili**:
e' esattamente cio' che `L-NUMERI` vieta per i numeri, applicato a dei **criteri**.
### ✅ **Luca li ha riformulati** *(punto 2)*, e la riformulazione e' sua, non mia.

### ⛔⛔ **② <<IL PRESIDIO FA FALLIRE IL `pre-commit`>> ERA FALSO NEL SENSO CHE CONTA, e il
guardiano l'ha trovato.** ### **L'ho riletto dal disco** *(`P1`)*, e confermo:
`.githooks/pre-commit` lancia **`28` comandi** e fra questi ### **NON c'e'
`_collauda_tempo_proprio.py`**, ne' `_collauda_deriva.py`, ne' `_collauda_memoria.py`.

> ### **Quindi <<`pre-commit`>> in `collauda.py` e' UNA ETICHETTA, non un fatto.** Io ho
> misurato che **lo script torna `1`** — vero — e ho scritto che **ferma un commit** —
> ### **falso.** ### ⚠ **E' esattamente la forma di errore che `A9` descrive: ho chiamato
> PRESIDIO una cosa che non impedisce niente.**

### 📌 **E la stessa frase era sbagliata anche in `717bb60`**, dove avevo scritto che i due
collaudi *«restano nel `pre-commit`»*: **non ci erano.**
### ✅ **Il punto 4 del mandato lo cabla per davvero**, e la prova non e' che lo script
torni `1`: e' che ### **un commit VERO si fermi.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### ⭐ **PERCHE' IL PALINDROMO RIPARA LA `C` DEL PASSO INTERO — la derivazione, in tre righe**

Dal punto `3` di `1eeb73f` *(misurato, `16`/`16`)*: `C Op_i C^-1 = Op_i(-theta) = Op_i^-1`
**per ogni pezzo**. Allora, con `W = Op_1 Op_2 ... Op_n`:

```
C W C^-1  =  Op_1^-1 Op_2^-1 ... Op_n^-1        <- NELLO STESSO ORDINE
W^-1      =  Op_n^-1 ... Op_2^-1 Op_1^-1        <- IN ORDINE ROVESCIO
```

### ⭐⭐ **E LE DUE COINCIDONO SE E SOLO SE LA SEQUENZA E' IL SUO PROPRIO ROVESCIO**, cioe'
### **se e solo se e' PALINDROMA.** ### ✅ **Quindi `C W C^-1 = W^-1` non e' un effetto
sperato del palindromo: e' la sua DEFINIZIONE, vista da un'altra parte.**
### ⛔ **E da qui viene anche il caso che DEVE fallire del punto 3:** col passo **non**
palindromo quell'uguaglianza **deve rompersi**, e se non si rompesse vorrebbe dire che i
pezzi commutano — cosa che **non si assume, si misura.**

### ⭐ **E PERCHE' IL PALINDROMO DA' IL FATTORE `4`:** una composizione simmetrica e' di
**secondo** ordine *(Strang)*, una asimmetrica di **primo** *(Lie-Trotter)*.
### 📌 **E non lo credo: l'ho GIA' MISURATO** in `1eeb73f` come **diagnosi** — `5.342`,
`3.691`, `4.291` col solo ordine rispecchiato, contro `2.540`, `2.204`, `2.111`.
### ⚠ **Ma la diagnosi usava un palindromo di `14` pezzi** *(il vecchio `ORDINE` dimezzato
e specchiato, con la saturazione a `0.25` **quattro** volte)*, e quello che entra in tabella
ne ha **`12`**: ### **i numeri NON saranno gli stessi, e li rimisuro.**

### ⛔ **CIO' CHE NON SO**

1. **se la fusione dei due mezzi centrali e' lecita.** ### ✅ **E NON LA FACCIO:** scrivo il
   palindromo **puro**, `12` pezzi, col pezzo centrale **in due mezzi**. ### ⭐ **Cosi' non
   c'e' niente da dimostrare** — la fusione sarebbe *coperta* dalla misura <<due mezzi fanno
   l'intero>> *(`0.7`–`1.4` ulp)*, ma **un'equivalenza entro l'ulp non e' un'identita'**, e
   il palindromo **si definisce coi mezzi.**
2. **se i pezzi di `psi` e di `phi` commutano** *(per raggrupparli)*. ### ⛔ **NON LI
   RAGGRUPPO:** il mandato dice che se lo faccio **devo misurarlo**, e ### **non mi serve** —
   quindi non introduco una cosa da dimostrare per un vantaggio che non mi serve.
3. **se lo spettro e' appaiato.** ### **Non lo so, e non lo devo decidere:** il punto 3 e'
   **una misura, nessuna decisione.**
4. **quanto dura il `pre-commit` VERO.** ### ⚠ **I `294` s che ho citato sono di
   `collauda.py`, NON del hook** — cioe' ### **non sono il numero che il budget di `500` s
   governa.** Lo misuro.

---

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, cosa mi FERMA*

| | il passo | **che cosa decide** | **cosa mi FERMA** |
|---|---|---|---|
| `0` | **le decisioni in indice**: `DECISIONE-COMPOSIZIONE-SIMMETRICA` **CHIUSA**, la `C` **APERTA**, la soglia a `6x` registrata | che il codice nasca **dopo** la decisione | — |
| `1` | **l'`ordine` palindromo in `leggi.yaml`**, `12` pezzi; **l'IMPRONTA si dichiara prima e dopo** | il passo | la somma delle frazioni di una legge **diversa da `1` esatto** → il generatore rifiuta, ed e' giusto |
| `2` | **`M-B1` NUOVO: PEZZO PER PEZZO** al bit contro `717bb60`, a `theta = pi` | se il raccordo vale **dove ha senso** | un pezzo che **non** coincide → **FERMO** |
| `2-bis` | **la distanza del passo intero** su `250` tick, **come INFORMAZIONE** | niente: e' un numero da riportare | — |
| `3` | **`M-B2`** con lo stesso script e la stessa scena | il secondo ordine | un rapporto lontano da `4` → **FERMO e riporto** |
| `4` | **lo SPETTRO** *(script nuovo)*: `eps <-> -eps`, le degeneranze doppie, `C W C^-1 = W^-1`, **col caso che DEVE fallire** | niente di fisica: **solo numeri** | il caso che deve fallire **che non fallisce** → il braccio e' **un FALSO-UNO** |
| `5` | **il hook VERO**: `_collauda_tempo_proprio.py` dentro `.githooks/pre-commit`, col **tempo** | che il presidio **impedisca** *(`A9`)* | il totale oltre **`500` s** → **FERMO e riporto** |
| `5-bis` | **la prova su un ramo usa-e-getta**: un pezzo a tick fisso **FERMA UN COMMIT VERO** | che la parola <<presidio>> sia vera | il commit che **passa** → **non e' un presidio** |
| `6` | **la soglia della memoria**: misuro col palindromo, **POI** porto a `6x`, e un caso oltre `6x` **deve** fallire | il budget di calcolo | la misura **oltre `6x`** → **NON alzo**, riporto e mi fermo |

### ⛔ **L'ORDINE DEI DUE E' OBBLIGATO, e lo scrivo per non invertirlo:** ### **prima si
MISURA col palindromo, poi si cambia la soglia.** Cambiarla prima vorrebbe dire
**scegliere la soglia sapendo che fa passare** — che e' la cosa che il mandato vieta.

---

## 3. LA STELLA POLARE — **le cinque risposte, PRIMA del codice**

| | la risposta |
|---|---|
| **1. `A14`, conserva localmente?** | **La carica si'**: ogni pezzo resta unitario, e il palindromo e' **un prodotto di unitari**. ### ⭐ **E l'energia MIGLIORA, ed e' il punto:** l'errore passa da `O(dtau)` a `O(dtau^2)` — ### **la violazione resta, ma la sua SCALA cambia**, e `M-B2` la misura. |
| **2. a quale GRADINO arriva?** | **`(a)`**, e per `M-B1` **al bit sui singoli pezzi**. ### ⛔ **NON `(c)`:** nessun limite noto e' stato toccato. |
| **3. aggiunge un numero o una legge?** | ### ✅ **NIENTE.** `0` leggi nuove *(restano `7`)*, `0` parametri nuovi: cambia **l'ORDINE**, che e' **un dato della tabella**, e le frazioni sono `0.5` — ### **meta' di `1`, non un numero tarato.** ### ⚠ **E la soglia della memoria si ALZA, ma e' UN BUDGET DI CALCOLO e lo dice Luca:** non entra in nessuna legge. |
| **4. tocca `rho`, `c_s` o il SEGNO?** | **Tocca il SEGNO per via dello spettro**, e **solo per MISURARLO**: il punto 3 guarda se `eps <-> -eps`, che e' cio' su cui materia/antimateria si appoggia. ### ⛔ **Nessuna decisione**, e nessun verso EM↔curvatura. |
| **5. emergente o imposto?** | ### ⭐ **IMPOSTA e' la REVERSIBILITA'** *(la scelta `(b)` di Luca: il passo rovesciato e' il passo rifatto all'indietro)*, ### **e l'IRREVERSIBILITA' deve EMERGERE** — e' `A15.3`, e il palindromo e' cio' che rende la domanda **ben posta**. ### ⚠ **E l'APPAIAMENTO dello spettro, se c'e', e' EMERGENTE:** non lo impone nessuna riga, e il punto 3 **potrebbe smentirlo.** |

---

## 4. TODO DEL NEXT STEP

1. **punto 0**: le tre registrazioni *(chiusura, apertura, soglia)*, e **la correzione dei
   miei due errori** nella relazione e nelle voci.
2. **punto 1**: `ordine` palindromo a `12` pezzi, rigenerazione, **impronta prima e dopo**.
3. **punto 2**: `_misura_mb1.py` riscritto **pezzo per pezzo**, piu' la distanza del passo
   intero come informazione; `M-B2`; `_collauda_tempo_proprio.py` ancora `0`/`7`.
4. **punto 3**: `primo_ordine/_misura_spettro_l1.py`, **col caso che deve fallire.**
5. **punto 4**: il hook, la prova sul ramo usa-e-getta, la soglia a `6x` **dopo** la misura,
   e **la CI dichiarata ROSSA** con l'elenco esatto.
6. **punto 5**: `RIPRESA` e mappa. Poi **STOP**: la `C` e' di Luca.
