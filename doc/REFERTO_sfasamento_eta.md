# REFERTO — **IPOTESI CONFERMATA: il TEMPO 2 non ha creato un difetto, ha TOLTO UNO SFASAMENTO.**

**Blob:** `a8f1b2f4` (byte grezzi `cf6722ff`). **Nessuna riparazione, nessun revert, nessun
pavimento.** `Z9` non toccata, `Y5` non riscritto.

---

## 1. LA CATENA, MISURATA PUNTO PER PUNTO

```
:3018   w = self._pesi(); self.eta += dt_n
        ^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^
        usa eta VECCHIA   POI la incrementa
```

### ① IL TEST DIRETTO — **confermato, 100 %**

```
su 31 nodi-passo appena nati (grado 2, eta = 0):
  ramp PRIMA dell'incremento ESATTAMENTE 0 :  31 / 31   (100.00 %)
  ramp DOPO  l'incremento    ESATTAMENTE 0 :   0 / 31   (  0.00 %)
  ramp DOPO, valore minimo osservato       :  0.0002
```

**`ramp` è zero esatto prima dell'incremento e non lo è mai dopo.**

### ③ IL CONTO DEI PESI — **confermato, 100 %**

```
archi incidenti ai neonati       : 62
di cui con peso ESATTAMENTE ZERO : 62   (100.00 %)
peso massimo su un arco di neonato: 0
```

**Entrambi gli archi del figlio hanno peso zero** — come dev'essere, perché `ramp[figlio]` compare
come **fattore** in ogni suo arco (`base = exp(-d/lam) · ramp[i] · ramp[j]`). Quindi `psi = 0`, e
`rho_sorgente = 0`.

### ② LA CONTROPROVA SUL BLOB VECCHIO — **risolta dalla LETTURA del codice**

```
VECCHIO 9dfd91c4 :  :2979  w = self._pesi(); self.eta += dt_n
                    :3006  psi_forces = ... self.calcola_psi()    <- RICALCOLA _pesi()
                    :3118  psi_sync   = ... self.calcola_psi()    <- RICALCOLA _pesi()

ATTUALE a8f1b2f4 :  :3018  w = self._pesi(); self.eta += dt_n
                    :3052  psi_forces = ... self.calcola_psi(w)   <- usa `w`, eta VECCHIA
                    :3177  psi_sync   = ... self.calcola_psi(w)   <- idem
```

**Nel blob vecchio i due ricalcoli avvenivano DOPO l'incremento di `eta`**: `ramp` non era più zero,
e il neonato riceveva un peso **minuscolo ma non nullo**.

**E la conferma diretta è già in cassa** (`doc/REFERTO_rho_zero_tempo2.md`): sul blob vecchio i nodi
con `rho_sorgente ≤ 0` erano **ZERO su 66 invocazioni**. **I neonati avevano campo.**

---

## 2. IL VERDETTO — **la prima lettura, e ribalta il quadro**

> **Il TEMPO 2 non ha introdotto un difetto: ha TOLTO UNO SFASAMENTO.**
>
> **E il peso zero per un neonato è L'INTENTO DICHIARATO.** CLAUDE.md §9 e `doc/ASSIOMI.md` (A7b,
> caso speculare) dicono la stessa cosa: *«un nodo appena nato non pesa ancora»*, e **zero è il
> valore corretto di `ramp = min(1, eta/TAU_A)` con `eta = 0`.**
>
> **Prima, il neonato riceveva `~2e-4` per CASO** — perché `calcola_psi()` ricalcolava i pesi
> guardando `eta` **dopo** l'incremento. **Non era una scelta di legge: era una perdita di
> sincronia.**

**`Y5` era scritto su quel comportamento sfasato.** È **l'ottavo criterio scaduto** di questo giro.

---

## 3. ⚠ IL FATTO CHE VA REGISTRATO, e non è piccolo

> **Per tutto il tempo in cui quel codice è girato, il nodo appena nato ha pesato `~2e-4` invece di
> `0`, e nessuno lo sapeva.**

**È la quarta volta che uno sfasamento temporale silenzioso viene alla luce**, e le prime tre sono
già nel registro:

| | difetto | come si manifestava |
|---|---|---|
| `_cs_nodo_prev` | cache scartata a ogni mitosi | fallback **71.88 %**, `cs = CS_M` costante |
| `_psi_spin_prec` | cache non estesa alla mitosi | **95.33 %**, la FASE 5 inerte per mesi |
| i due `theta` | due convenzioni per lo stesso nome | C19, numeri incomparabili |
| **questo** | **`_pesi()` valutato a un `eta` diverso da quello del passo** | **il neonato pesava `2e-4` invece di 0** |

**La famiglia è sempre la stessa: una grandezza letta in un momento del passo diverso da quello che
il codice dichiara.** *(Ed è esattamente ciò che A6 chiede di escludere — qui col segno opposto: non
uno stato troppo nuovo, ma **due letture della stessa grandezza a istanti diversi**.)*

---

## 4. COSA NON HO FATTO, e perché

- **Non ho riscritto `Y5`:** il mandato dice di sapere prima il *perché*. **Ora si sa**, e `Y5` può
  essere riscritto — **ma con un mandato proprio**, perché riscrivere un criterio è la cosa su cui
  questo repo ha già sbagliato **otto volte**.
- **Non ho messo alcun pavimento** su `ramp`, `rho_sorgente` o `psi`: **se il neonato non deve
  pesare, zero è la risposta giusta**, non un problema da tamponare.
- **Non ho spostato `eta += dt_n` prima di `_pesi()`:** cambierebbe la legge, e non è questo il
  mandato.
- **`Z9` resta aperta e resta smentita come causa di questo.**

---

## 5. UNA PRECISAZIONE SULLA MISURA

Il `ramp` "dopo l'incremento" è calcolato con **`DT` nudo** (`0.01/50 = 2e-4`), non con
`dt_n = DT·r`. **È un limite inferiore dichiarato:** l'incremento vero è `dt_n`, e se anche col
valore più piccolo `ramp` non è zero, **a maggior ragione non lo è col ritmo locale**. *(Usare `DT`
per stimare e dichiararlo è diverso dall'usarlo nella fisica — dove sarebbe il difetto di §9.)*
