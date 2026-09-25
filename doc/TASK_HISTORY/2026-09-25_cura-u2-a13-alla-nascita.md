# `CURA 5` — **`U2` = `A13` ALLA NASCITA** *(approvata da Luca, 2026-09-25)*

> **Committato PRIMA del codice** *(par.5-septies: l'ordine dev'essere verificabile da git, non
> asserito da me)*.

> ### **Un arco si divide SOLO se `d_arco >= 2 LAM`.**
> **Un interruttore, OFF di default. Lo Schwinger NON è toccato** *(resta `A3`)*.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### LE PREMESSE, tutte già misurate

- **`A13` alla nascita ≡ `d_arco >= 2 LAM`**, perché il figlio nasce a `d/2` dai genitori e **la
  distanza del sistema è quella lungo gli archi**, non su `pos` *(correzione di Luca)*.
- **Il `77.23 %` delle divisioni è GIÀ conforme**, il `22.77 %` no *(`7086031`, `279` eventi,
  2 semi)*.
- **`U2` e `A13`-alla-nascita sono la stessa voce**, e i contatori di `U2` **la misuravano già**:
  `_sm_trd_mitosi / _sm_visd_mitosi = 20/82` e `22/104`, che coincidono **cifra per cifra** con
  l'involucro indipendente.
- **La mitosi non divide a caso:** `0.2277` contro `0.2998` di archi corti nel grafo — **evita un
  po'** gli archi corti *(indizio: `2.3` volte lo spread fra due semi)*.

### PERCHÉ NON È UNA LEGGE NUOVA — `STANDARD 10`, e il conto va fatto

```
PRIMA   la mitosi divide senza guardare `d`;  `_nasce` INTERVIENE sui figli e FABBRICA lunghezza
        (misurato: `_sm_lund_mitosi` = 0.8 LAM per evento a risposta nota)
DOPO    la mitosi guarda `d >= 2 LAM`;        `_nasce` NON HA PIÙ NIENTE DA FARE su quel sito
```

> ### **LE LEGGI NON AUMENTANO: `A13` c'era già, e si TOGLIE l'intervento di `_nasce` sui figli
> ### della mitosi**, cioè **la lunghezza fabbricata su quel sito**.
> **È il caso che `STANDARD 10` descrive:** *a parità di effetto si preferisce togliere
> un'eccezione* — e qui l'eccezione era **«la mitosi è il solo sito che può creare una distanza
> sotto la scala di Planck, e un presidio la ripara dopo»**.

### COSA MI ASPETTO

1. **il flag spento sarà byte-identico**: la condizione è un `and` in più su una maschera;
2. **gli eventi di mitosi caleranno al `~77 %`**, perché è la frazione conforme misurata;
3. **`_sm_trd_mitosi` e `_sm_lund_mitosi` andranno a ZERO ESATTO** — è la cura stessa.

### ⚠ COSA **NON** SO

- **se il `23 %` di divisioni tolte cambi la dinamica oltre il conteggio.** Quelle divisioni
  avvenivano su archi **corti**, cioè in regioni **diverse** dalle altre: toglierle non è un
  campionamento uniforme. **Non lo indovino.**
- **se la mitosi si spenga col tempo.** Se il grafo si contrae *(e si contrae: `med d0` cala del
  `36 %`)*, **gli archi scendono sotto `2 LAM`** e la condizione diventa via via più difficile.
  **La frazione `77 %` è misurata su `300` passi; a `1000` potrebbe essere molto più bassa.**
  **Questo è il rischio principale della cura, e il criterio `C3` lo guarda.**
- **se `d/2 >= LAM` basti.** Il figlio è a `d/2` dai **genitori**; dagli **altri** nodi la distanza
  lungo gli archi è **almeno** `d/2` *(passa per un genitore)*, quindi sì — **ma solo se il grafo
  non ha un cammino più corto**, e un cammino più corto per un nodo appena nato **non esiste**,
  perché ha **solo** i due archi verso i genitori. **È un argomento, e va verificato: `C5`.**

---

## ② PROGETTAZIONE — *come intendo arrivarci*

### DOVE VA LA CONDIZIONE, e perché lì

La selezione finale è in `mitosi`:

```python
c = np.where(nasce)[0]                      # i candidati (campana di torsione + probabilità)
I = self._rho_sorgente()
ok = 0.5 * (I[a] + I[b]) >= QMIN_M * median(self.peq)     # la soglia di densità
sel = c[ok]
```

**La condizione va nella maschera `ok`**, accanto alla soglia di densità: è **lo stesso punto**
dove il codice già decide *«questo candidato si divide o no»*. **Non in `nasce`** *(là si decide la
probabilità, e `A13` non è una probabilità)*, **non in `_nasce`** *(là si ripara, e la cura è
proprio togliere la riparazione)*.

### IL FLAG

`MITOSI_2LAM`, **`False` di default**, con `--mitosi-2lam` e il `global` in `_applica_flag`.
**Nessun numero nuovo:** `2 LAM` viene da `A13` + *«il figlio nasce a `d/2`»*, entrambi già nel
sistema.

### I CRITERI, fissati QUI — quelli di Luca, più due miei

| | criterio | cosa decide |
|---|---|---|
| **`C1`** | **flag SPENTO = byte-identico**, firma dei byte, un processo per braccio | par.2.1 · `STANDARD 1` · `STANDARD 2`. **Se fallisce, STOP** |
| **`C2`** | flag ACCESO: **`_sm_trd_mitosi == 0` E `_sm_lund_mitosi == 0`** su `300` passi, `2` semi | **è la cura stessa**, e in forma ESATTA |
| **`C3`** | **eventi di mitosi `~77 %`** di quelli a flag spento, **entro lo spread** | il numero viene dalla misura `7086031`. **Se è molto più basso, la cura non regola: strozza** |
| **`C4`** | **nessun figlio con `d/2 < LAM`** | la verifica diretta di `A13` alla nascita |
| **`C5`** | *(mio)* **il figlio è a `>= LAM` da TUTTI lungo gli archi**, non solo dai genitori | l'argomento del punto ① va **verificato**: se il figlio avesse un terzo arco, cadrebbe |
| **`C6`** | *(mio)* **lo SCHWINGER è INVARIATO**: `_sm_trd_schwinger` e `_sm_lund_schwinger` **uguali** fra i due bracci | Luca dice *«lo Schwinger NON è toccato»*, e **una cosa che non si tocca va MISURATA invariata**, non assunta |
| **`C7`** | *(mio)* **CONTROLLO POSITIVO**: i due bracci **DEVONO** differire | par.10.2: un sigillo di sola byte-identità **passerebbe su codice morto** |
| **`C8`** | *(mio)* **CASO CHE DEVE FALLIRE** *(`P1-sexies`)*: col flag ON e la soglia forzata a `0`, **`C2` deve dare FAIL** | se `C2` passa anche senza la condizione, non sta guardando la cura |

**COSA MI FAREBBE FERMARE:** `C1` che fallisce; `C3` molto sotto il `77 %` *(la cura strozza
invece di regolare)*; `C5` che fallisce *(l'argomento è sbagliato e `A13` non è soddisfatto)*.

---

## ③ TODO DEL NEXT STEP

1. il flag `MITOSI_2LAM` e la condizione nella maschera `ok`;
2. il sigillo `C1`-`C8`, un processo per braccio;
3. la scheda della legge *(`REG-R`)*;
4. **poi** `INERZIA-1`: `I3` col taglio opposto, la scalatura di coppia e inerzia, e la scala di
   `(C)`. **Nessuna corsa lunga prima della cura dell'inerzia** *(`CONTAGIO`)*.
