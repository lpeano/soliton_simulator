# -*- coding: utf-8 -*-
"""La regola IN PROVA di Luca: un'ASSENZA si dichiara solo dall'intero file o dall'AST."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

P = "doc/PATTERN_DI_PROVA.md"
t = io.open(P, encoding="utf-8", newline="").read()
A = "## IN PROVA\n\n*(nessuna)*"
B = u"""## IN PROVA

### ① **UN'ASSENZA SI DICHIARA SOLO DA UNA RICERCA SULL'INTERO FILE O DALL'AST** — mai da una finestra di righe, mai da un `in` sul testo

> **Proposta di Luca, 2026-09-24.** *(`PROPOSTA IN PROVA`)*

| | |
|---|---|
| **la regola, in una riga** | **Dire *«non c'è»* richiede una ricerca sull'**intero file** o sull'**AST**. Una finestra di righe e un `in` sul testo possono dire *«non c'è»* quando c'è, e *«c'è»* quando è solo un commento.** |
| **il difetto reale da cui nasce** | **TRE casi, tutti dello stesso giorno** — vedi sotto |
| **come la userei** | prima di scrivere *«non esiste»*, *«manca»*, *«non è in `DOMINI`»*, *«non ha un flag CLI»*: **`grep` su tutto il file**, oppure **l'AST** se la domanda è su un riferimento di **codice**. |
| **come si vede se la rispetto** | ogni affermazione di assenza porta **il comando che l'ha prodotta**, e quel comando **non ha un intervallo di righe** |

### I TRE CASI, e sono di oggi

| | il caso | l'errore |
|---|---|---|
| **`S10`** | *«il ramo `TEMPO_SEGNO` di `ritmo()` gira 600 volte»* | dedotto **da un contatore** senza verificare **dove stesse** rispetto al controllo del flag *(stava PRIMA)*, **né il valore del flag** *(era `False`)*. **Due verifiche omesse nella stessa frase**, e il sospetto è stato **ritirato** *(`Z130`)* |
| **`T1` di `E4-LAM`** | *«`_lam_attivo` non esiste più»*, cercato con `"_lam_attivo" not in sorg` | **trova le sue DUE occorrenze nei COMMENTI** che spiegano che il gate è stato tolto → **`FAIL` falso su codice corretto**. Dall'AST i riferimenti di codice sono **`[]`** *(`Z142`)* |
| **`D37`** | *«`_cs_nodo_prev` non è nei `DOMINI`»*, cercato con `sed -n '213,240p' \| grep cs` | **la voce sta a `:257`, fuori dalla finestra.** Ho aggiunto un **duplicato**, che in un dict è **codice morto in silenzio** *(`Z142`, `D37`)* |

> **I tre errori hanno lo stesso verso opposto a coppie, e per questo la regola serve in
> entrambe le direzioni:** `T1` diceva **«c'è»** e non c'era *(un commento letto come codice)*;
> `D37` e `S10` dicevano **«non c'è»** e c'era. **Una ricerca parziale sbaglia in entrambi i
> sensi.**

### ⚠ **PERCHÉ NON È GIÀ COPERTA DA `P1`**

`P1` dice *«non usare l'associazione senza verificare lo storico»*, e riguarda i **fatti già
stabiliti nei documenti**. **Questa riguarda il CODICE**, ed è più stretta: dice **quale
strumento** rende valida un'affermazione di assenza. `P1` dice *«rileggi»*; questa dice
**«rileggi TUTTO, o guarda l'AST»**.

### ⚠ **E IL LIMITE, dichiarato: NON È UN PRESIDIO** *(`A9`)*

**Non impedisce nulla.** È un **obbligo di forma verificabile dal destinatario**: se
un'affermazione di assenza non porta il comando che l'ha prodotta, **si vede**.
**Cosa la renderebbe un presidio:** un controllo che, nei referti generati, rifiuti le parole
*«non esiste» / «manca» / «assente»* se non accompagnate da un comando senza intervallo di
righe. **Non l'ho scritto**, e va detto invece di chiamarla presidio.

*(nessun'altra)*"""
assert t.count(A) == 1
io.open(P, "w", encoding="utf-8", newline="\n").write(t.replace(A, B))
print("regola IN PROVA scritta")
