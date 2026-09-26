# `DRIVER-SCENA-II` — il driver deve poter fare la scena `(ii)`(a)

> **Il primo `SI` dello smistamento** *(`doc/SMISTAMENTO_run_base.md`, `doc/REVISIONE_SI_2026-09-26.md`)*.
> **Mandato di Luca, 2026-09-26.** *«Senza un driver che faccia la scena `(ii)`(a) non esiste il RUN
> BASE, e senza run base non esistono le tre prove.»*
>
> **COMMITTATO PRIMA DEL CODICE** (`CLAUDE.md` par.8): il commit di questo file dev'essere
> **antenato** dei commit del lavoro che descrive, cosi' l'ordine e' **verificabile da git**
> invece di essere asserito da me.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di scrivere una riga di codice*

### 1.1 ⚠ LA PRIMA COSA DA DIRE: **una delle due fonti che il mandato indica NON ESISTE**

Il mandato dice *«leggi i fatti di `_applica_flag` e `_massa` in `doc/FATTI_dal_codice.md`»`.*
**Li' non ci sono, e non e' una svista di ricerca:**

| cercato | occorrenze in `doc/FATTI_dal_codice.md` |
|---|--:|
| `_applica_flag` | **0** |
| `_massa` | **1**, ed e' `nuova_massa()` in un'altra voce |
| `avvia_test` | **0** |
| `N-MASSE` | **0** |

**E non e' colpa del riordino: `par.9` non ne parlava neanche prima** — `git show
regole-pre-riordino:CLAUDE.md | grep -c '_applica_flag'` da' **`0`**. *(Assenza dichiarata da una
ricerca sull'INTERO file, non da una finestra: `STANDARD 9`.)*

> **CONSEGUENZA DI METODO, e vale oltre questo task:** `doc/FATTI_dal_codice.md` copre **11
> funzioni**, e sono quelle su cui il fork ha misurato qualcosa. **La catena di avvio** —
> `_applica_flag`, `avvia_test`, `_massa`, `semina` — **non ha un solo fatto scritto**, benche' sia
> il pezzo che decide **con che mondo parte ogni run**. **Ho letto il codice** *(e quello che ho
> letto sta qui sotto)*, ed e' un vuoto da colmare: **va in coda**, non in questo task.

### 1.2 Che cosa credo, prima di toccare niente

Credo che **il vicolo cieco sia reale e che stia in `_applica_flag`, non nella scena**. Le quattro
righe della revisione lo dicono separatamente; la riga che le compone, e che nella revisione era
**🧠 INFERENZA**, e' questa:

```python
# soliton_simulator.py :8681, ultima riga utile di `_applica_flag`
net.semina(-1 if SEMINA_LAM else a.nodi)
```

**Con `SEMINA_LAM` acceso il ternario NON GUARDA `a.nodi`.** Quindi `--nodi 0` **non e' rispettato**:
il vuoto nasce **a saturazione**, `net.n > 0`, e la scena `(ii)` — che pretende una rete vuota —
**rifiuta**. E `SEMINA_LAM` e' nell'argv del driver **in ogni run**.

**Mi aspetto** che la cura sia **una sola riga di condizione** su quel `semina`, e **non** un ramo
nuovo nella scena: la scena fa la cosa giusta *(rifiuta invece di sommare due vuoti, e lo DICE)*.
**`STANDARD 10`:** si toglie un'eccezione al vuoto di default, **non si aggiunge una legge**.

### 1.3 Che cosa ho VERIFICATO dal codice, e che nella revisione era **🟨 di Luca**

**Le due cose che Luca aveva marcato come non verificate da lui: le ho verificate, ed erano vere.**

| affermazione | com'era | ora |
|---|---|---|
| `N-MASSE` **con `SEMINA_LAM`** finisce *proprio* in quel `SystemExit` | 🟨 | ✅ **il `raise` a `:7187` e' la PRIMA istruzione di `_massa` sotto `if SEMINA_LAM:`, senza altre condizioni**: qualunque scena che passa da `_massa` si ferma. `N-MASSE` passa da `_massa`. |
| **manca un `--seme` reale** nel driver | 🟨 | ✅ **`--seed` non compare nell'argv del driver**: `grep -c '\-\-seed' csv/_test_fork/_scena_video.py` = **0**. Ogni run del driver gira col **seme 42** *(`_applica_flag`: `Rete(a.seed if a.seed is not None else 42)`, e `Rete.__init__(seed=42)`)*. |

**E una cosa buona, che va detta perche' evita una cura inutile:** il driver **riporta** il seme
giusto. `SEME_EFFETTIVO` legge il default di `Rete.__init__` *(42)*, che **coincide** con quello
che `_applica_flag` usa quando `--seed` e' `None`. **Il difetto non e' che il driver mente sul
seme: e' che non puo' cambiarlo.**

### 1.4 Che cosa **NON** so

- **se `--nodi 0` basti**, o se serva un'opzione `--scena` anche per **non** far partire i 300 passi
  di pre-rilassamento: `if a.seed is not None or a.nodi != SEME_INIZIALE:` → con `--nodi 0` quel
  ramo **scatta**, e farebbe `300` `step()` + `rilassa_disegno(30)` **su una rete vuota**. Credo sia
  un no-op *(`semina(0)` ritorna subito, e `step()` su `n = 0`)* ma **non l'ho eseguito**.
- **se `MASSE-COERENTI` sia completa** come scena del driver: e' registrata in `TESTS` a `:7476`, e
  il driver chiama `S.avvia_test("N-MASSE")()` a `:328` — **due punti** da cambiare, non uno.
- **quanto vuoto** faccia la saturazione con l'argv del driver: e' il numero che la scena `(ii)`
  vedrebbe, e non l'ho misurato.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — i cinque criteri, **scritti prima di vedere i numeri**

**Sono i criteri che Luca ha dettato.** Per ognuno: **che cosa decide**, e **che cosa mi fa
FERMARE**. Il sigillo si chiama `csv/_seal_fork/_sigillo_scena_ii.py` e gira **via CLI**, **un
processo per braccio** (`STANDARD 1`, `H-P3`).

| # | criterio | che cosa decide | che cosa mi fa FERMARE |
|--:|---|---|---|
| **1** | il driver lancia la scena `(ii)`(a) con un'opzione **`--scena`**, e **il default resta invariato** *(dichiarato)* | che la scena sia **raggiungibile da un comando solo**, e che **nessun comando gia' scritto cambi comportamento** | se il braccio **senza** `--scena` non e' **byte-identico** al driver di prima: allora non e' un'opzione, e' una cura travestita |
| **2** | con la scena `(ii)`, **`_applica_flag` NON semina il vuoto prima della scena** *(`--nodi 0` rispettato)*, **e la scena costruisce il suo vuoto** | che il vicolo cieco sia **chiuso alla radice**: un vuoto solo, fatto dalla scena | se per farlo devo toccare `_semina_masse_coerenti`: la scena e' giusta, il difetto e' a monte. **Toccare la scena sarebbe curare il sintomo** |
| **3** | **un'opzione `--seme` REALE**: due semi diversi → **reti diverse**; lo **stesso seme due volte** → **byte identici** *(firme, `STANDARD 2`)* | che il seme sia **una variabile del run** e non una costante nascosta — prerequisito di `P3` *(≥ 4 semi per una barra)* | se lo stesso seme da' due reti diverse: c'e' uno stato **fuori dall'RNG**, e va trovato **prima** di qualunque misura |
| **4** | **configurazione: `0` differenze sui booleani** contro l'argv del driver *(`H-P5`)* | che il referto dichiari **la configurazione INTERA**, non i flag che ricordo io | qualunque differenza: e' `CONFIG-1` che si ripete, e quel difetto e' costato **sei misure con 28 leggi su 31 spente** |
| **5** | **caso che DEVE fallire:** la scena **`N-MASSE` con `SEMINA_LAM`** continua a rifiutare, **con lo stesso messaggio** | che la cura **non apra una porta** alle scene di epoca pre-`A13` | se `N-MASSE` parte: ho rotto un presidio invece di aggiungere una scena. **E' il criterio piu' importante** (`P1-sexies`) |

### 2.1 Come intendo arrivarci, in ordine

1. **misurare prima**: che cosa fa **oggi** il driver con la scena `(ii)` *(mi aspetto il
   `SystemExit` della rete non vuota)*. **Un `FAIL` atteso, prima della cura, e' il termine di
   paragone del criterio 2.**
2. **la cura in `_applica_flag`**, una condizione sola, e **la scena non si tocca**;
3. **`--scena` e `--seme` nel driver**, col default dichiarato;
4. **il sigillo**, cinque criteri, **un processo per braccio**, e il **giro corto prima**
   (`STANDARD 7`);
5. **STOP dopo il sigillo: nessun run lungo.**

### 2.2 Le letture si fissano QUI

- **criterio 1** passa **solo** con `0` campi diversi fra il braccio senza `--scena` e il
  riferimento *(non «pochi», non «trascurabili»)*;
- **criterio 3** passa **solo** con **firme `sha1` identiche** sullo stesso seme e **almeno una
  firma diversa** su semi diversi. *`max|Δ| = 0` non e' ammesso come prova di identita'*
  (`STANDARD 2`), e **due `None` non sono un'identita'** (`STANDARD 3`);
- **criterio 5** passa **solo** se il messaggio e' **lo stesso** *(confronto sul testo, non «ha
  dato errore»)*.

### 2.3 Che cosa questo task **NON** fa

**Non fa il run base.** Fa **il driver che lo potrebbe fare**, e si ferma al sigillo. Nessuna
misura di fisica, nessuna conclusione su `PROVA 1`.

---

## 3. TODO DEL NEXT STEP — *operativo*

- [ ] **misura 0**: lanciare il driver con la scena `(ii)` **com'e' oggi** e committare
      l'errore che da', come termine di paragone del criterio 2;
- [ ] `--scena` nel driver: **due** punti da cambiare *(l'argv a `:223` e `avvia_test` a `:328`)*,
      default `N-MASSE` **dichiarato invariato**;
- [ ] `--seme` nel driver → `--seed` del simulatore, e **`SEME_EFFETTIVO` deve leggerlo da li'**,
      non dalla firma di `Rete.__init__`;
- [ ] la cura di `_applica_flag`: `--nodi 0` rispettato **anche** con `SEMINA_LAM`;
- [ ] `csv/_seal_fork/_sigillo_scena_ii.py`, cinque criteri, **via CLI**, **un processo per
      braccio**, **giro corto prima**;
- [ ] inventario + README + relazione **nello stesso commit** del codice (`CLAUDE.md` par.6);
- [ ] **STOP.**

### In coda (non in questo task)

- **`FATTI-AVVIO`** — la catena di avvio *(`_applica_flag`, `avvia_test`, `_massa`, `semina`)* **non
  ha un solo fatto** in `doc/FATTI_dal_codice.md`, benche' decida **con che mondo parte ogni run**.
  **Criterio di chiusura:** una sezione per ciascuna delle quattro funzioni, coi fatti **letti dal
  codice** e la riga misurata dall'AST.
