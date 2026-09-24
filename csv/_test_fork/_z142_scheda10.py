# -*- coding: utf-8 -*-
"""La scheda 10: GLI INVARIANTI DI DOMINIO (C5). Mancava, e REG-R l'ha preteso."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()
assert "nome=invarianti" not in t

SCHEDA = u"""

---

<!-- SCHEDA nome=invarianti funzioni=verifica_invarianti flag=INVARIANTI -->

# ⑩ GLI INVARIANTI DI DOMINIO — **`C5`**

> **Scheda aperta il 2026-09-24, e mancava.** `C5` è in `CURE VERIFICATE` con sigillo `3/3`,
> **è la sola cura ACCESA DI DEFAULT**, e **non aveva una scheda**: `REG-R` l'ha preteso quando
> `E4-LAM` ha toccato la legge. *(Un difetto di inventario, non di fisica — ma l'ordine giusto
> è questo: prima la scheda.)*

## LA FORMA

**`verifica_invarianti(dove, passo)`** scorre **`DOMINI`** — un dizionario
`nome → (forma, perché)` — e per ogni grandezza di stato presente controlla che stia **nel suo
dominio**. Alla prima violazione **solleva `DominioViolato`** con: **la grandezza**, **la regola
violata**, **il passo**, **gli INDICI**, **i valori**, **dove**, e **quale arco** *(`i`-`j`)*.

**DUE LIVELLI, e la distinzione è il punto:**

| livello | che cosa prende | come |
|---|---|---|
| **NUMERICO** | overflow, **divisione per zero**, valori non validi | `np.seterr(over='raise', divide='raise', invalid='raise', under='ignore')` a **`:7382`**. **L'UNDERFLOW non ferma niente**, perché densità come `1e-81` di un nodo neonato sono **legittime** |
| **FISICO** | ogni grandezza **dentro il suo dominio**, a fine passo | `DOMINI` + `verifica_invarianti` |

> **L'esplosione del 21/9 NON era un overflow** *(`1.8e6` è un numero normale)*: **l'avrebbe
> presa solo la regola FISICA `peq >= 0`.** È la ragione per cui i due livelli non si
> sostituiscono.

## LE FORME DI DOMINIO

| forma | regola | esempi |
|---|---|---|
| `'lam'` | **`>= LAM`** | `d`, `d0` |
| `'pos'` | `> 0` | `_dt_e_ultimo`, `_r_corrente`, `_cs_nodo_prev` |
| `'finito'` | finito, nessun vincolo di segno | `vd`, `_spinor_lift` |
| `'fase'` | in `[0, 4π)` | `phi`, `phi0` |
| `'unita'` | `|x| = 1` *(tolleranza `1e-6`)* | gli spinori |
| `'idx'` | `0 <= x < n` | `i`, `j` |

## ✅ `E4-LAM` — **LA LEGGE `d >= LAM` SI VERIFICA SEMPRE** *(decisione di Luca, 2026-09-24)*

> ### **«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema» è una
> ### LEGGE, non una garanzia che dipende da un flag.»**

**PRIMA** il controllo della forma `'lam'` era dentro `if _lam_attivo:`, con
`_lam_attivo = SCALA_MIN or SCALA_MIN_PASSO`, e **a flag spenti DEGRADAVA a `> 0`**:

```python
if _lam_attivo:  cattivo = ~fin | (vf < LAM * (1.0 - 1e-12))   # '>= LAM, con la scala minima accesa'
else:            cattivo = ~fin | (vf <= 0.0)                   # '> 0 (scala minima SPENTA)'
```

**DOPO**, incondizionato:

```python
cattivo = ~fin | (vf < LAM * (1.0 - 1e-12))
regola  = '>= LAM (= %.6f) -- LEGGE, non opzione' % LAM
```

**E `_lam_attivo` è stato TOLTO**: era il suo unico uso, e lasciarlo sarebbe stato codice morto
*(verificato dall'AST: `0` riferimenti di codice)*.

**Perché è giusto, in una riga:** **una legge verificata solo quando un flag è acceso non è una
legge, è un'opzione** — ed è `A9`: *un presidio che non impedisce non è un presidio.*

**La tolleranza `1e-12` non è un numero scelto:** è l'**arrotondamento** di `LAM`, cioè la
precisione con cui `LAM` stesso è rappresentabile.

### **IL SIGILLO** — `csv/_seal_fork/_sigillo_e4lam.py`

| | | |
|---|---|---|
| `T3` | **un arco sotto `LAM` a flag SPENTI FERMA il run** | quello che prima **non** faceva |
| `T4` | e con `d >= LAM` **non** si ferma | **il controllo che rende `T3` leggibile**: senza, `T3` passerebbe anche se il controllo si fermasse sempre |
| `T5` | **byte-inerte**: `206` campi identici, `0` diversi contro `_cura1_corto` | l'invariante **legge soltanto** |

**Il messaggio, verbatim:**

```
[INVARIANTE] `d` VIOLA `>= LAM (= 0.800000) -- LEGGE, non opzione` al passo 1
  indici (primi 8): 1     valori: 4.000000e-01     arco=1-2
```

## ❌ `D37` — **UNA CHIAVE DUPLICATA NEI `DOMINI`, ed è mia**

`'_cs_nodo_prev'` compariva **due volte**: `:226` *(la mia)* e `:257` *(preesistente)*.
**In un letterale di dict vince l'ULTIMA**, quindi la mia era **codice morto** — e **il sigillo
lo ha mostrato**, stampando una descrizione **che non era la mia**.

**La causa è `P1`:** avevo cercato la voce in una finestra di **28 righe** (`213-240`) e la voce
sta a **`:257`**. **Ho concluso un'ASSENZA da una ricerca PARZIALE.**
**Cura: si toglie la mia, si tiene la preesistente.** **E la derivazione resta valida:
`cs > 0` era GIÀ un invariante**, fatto da qualcun altro prima di me.

## ⚠ COSA QUESTA LEGGE **NON** FA, dichiarato

- **non corregge**: **legge soltanto**, e su un run sano **non cambia un bit**. Se scatta, il
  run **si ferma** — non si aggiusta;
- **non dice se la REALIZZAZIONE di una legge sia giusta.** Verifica che `d >= LAM`; **come** il
  sistema lo ottiene è il **freno a senso unico**, cioè **`D31`**. **La legge è giusta, la
  realizzazione no**, e sono due cose separate;
- **non copre le grandezze assenti**: `getattr(self, quale, None) -> continue`. Una grandezza
  che **non esiste** non viene controllata, e **questo non è contato**. *(Candidato per un
  contatore `A8`: quante voci di `DOMINI` vengono SALTATE per assenza. Non fatto.)*

## COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **se `'fase'` debba essere `[0, 4π)` o `[0, 2π)`.** È la domanda di `FASE_2PI`, e
   l'invariante **segue** la decisione invece di guidarla — oggi codifica il `4π`
   **dichiarato**, che la mappa del `4π` classifica come **convenzione**, non come misura;
2. **quante voci di `DOMINI` vengano saltate per assenza** in un run vero: non misurato.
"""
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + SCHEDA + "\n")
print("scheda 10 (invarianti) scritta")
