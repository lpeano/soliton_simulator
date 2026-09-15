# BARRE D'ERRORE sulle pendenze — **il residuo è REALE ma TRANSITORIO**, e non c'è nulla da cercare

> **Scritto per Claude web** (§5-ter). Branch `fork-su2`, 2026-09-15. Blob **`f5887254`**.
> **Nessun run, nessun cablaggio, nessuna modifica al `.py`.** Solo statistica sui CSV su disco.

---

## 0. I DUE RISULTATI, E UNA CORREZIONE A UNA MIA CORREZIONE

1. **`z = 21.8`** — lo scarto **non è rumore**. La premessa del mandato («`r = 0.35` ⇒ `SE ~ 0.3`»)
   **è sbagliata di un fattore 30**: `SE(theta) = 0.0097`, non 0.3.
2. **Ma lo scarto è TRANSITORIO**: cala da **0.979** (passo 50) a **0.010** (passo 400).
   **Non c'è nessun termine mancante da cercare.**
3. **E la mia correzione di stamattina aveva la causa sbagliata.** Avevo attribuito la differenza
   `0.037` vs `0.338` al campione (20 contro 2195 nodi). **Falso:** è `passo 400` contro `passo 300`.

---

## 1. LE BARRE D'ERRORE (n = 2195, passo 300)

`SE_b = |b/r|·√((1−r²)/(n−2))` — identità esatta per la regressione lineare semplice, quindi
ricavabile da `b`, `r`, `n` **senza** i dati grezzi di tutti i nodi.

| grandezza | pendenza | **SE** | r² | IC 95 % |
|---|---|---|---|---|
| `sigma = coppia/inerzia` | −1.0780 | **0.0073** | 0.908 | [−1.0923, −1.0637] |
| `tau` ATTUALE | +1.1760 | **0.0191** | 0.634 | [+1.1386, +1.2134] |
| `tau` LUCE (`d/cs`) | +0.0970 | **0.0055** | 0.123 | [+0.0862, +0.1078] |
| `theta` | −0.1520 | **0.0097** | 0.100 | [−0.1711, −0.1329] |

### 1.1 ⚠ La premessa del mandato non regge — e vale la pena capire perché

> *«una pendenza con `r = 0.35` è un numero fragile; se il suo `SE` è dell'ordine di 0.3, lo scarto
> non è significativo»*.

**`SE` non dipende quasi da `r`: dipende da `√n`.** Stessa pendenza, stesso `r`, campioni diversi:

| n | SE(theta) |
|---|---|
| 20 | 0.108 |
| 100 | 0.046 |
| **2195** | **0.0097** |

> **`r²` basso significa che la relazione spiega poca varianza, NON che la pendenza sia incerta.**
> Con 2195 punti la pendenza è determinata a **±0.01**, non ±0.3. Il sospetto era ragionevole e la
> verifica era giusta da chiedere — ma la risposta è no.

## 2. LA PROPAGAZIONE

```
attesa   = sigma + tau/2 = -0.4900  +-  0.0120
misurata = theta         = -0.1520  +-  0.0097
scarto = 0.3380      errore combinato = 0.0155

>>> z = 21.83
```

> **`z > 3`: lo scarto al passo 300 NON è un artefatto statistico.** Per il criterio, si passa al
> secondo check.

---

## 3. IL SECONDO CHECK — **transitorio**, e si chiude

`slope(tau)` non è stampata per campione, ma si ricava: `slope(tau) = slope(theta) − slope(diss)`.
**Validata** al passo 300: indiretta **+1.178** contro diretta **+1.176** — scarto **0.002**.

| passo | `sigma` | `diss` | `theta` | `tau` (ind.) | attesa | **scarto** |
|---|---|---|---|---|---|---|
| 50 | −1.110 | −0.392 | +0.129 | +0.521 | −0.850 | **0.979** |
| 100 | −1.013 | −0.638 | −0.067 | +0.571 | −0.727 | 0.660 |
| 150 | −1.079 | −1.155 | −0.108 | +1.047 | −0.555 | 0.448 |
| 200 | −1.073 | −1.175 | −0.117 | +1.058 | −0.544 | 0.427 |
| 250 | −1.093 | −1.623 | −0.174 | +1.449 | −0.368 | 0.194 |
| 300 | −1.078 | −1.330 | −0.152 | +1.178 | −0.489 | 0.337 |
| 350 | −1.085 | −2.472 | −0.158 | +2.314 | +0.072 | 0.230 |
| **400** | −1.056 | −1.980 | −0.113 | +1.867 | −0.123 | **0.010** |

> **Lo scarto CALA di due ordini: 0.979 → 0.010.** Pendenza su `log(passo)`: **−0.412**.
> **Al passo 400 la catena CHIUDE** (scarto 0.010).

**E il perché era già nel mandato:** `tau ≈ 4425-6500 passi`, il run ne ha 300-400. Il sistema ha
vissuto **meno di un decimo** di un tempo di rilassamento, e la formula
`omega_eq = sigma·√(tau/(2·dt))` vale **all'EQUILIBRIO**.

> ### **VERDETTO: TRANSITORIO, NON UN TERMINE MANCANTE.** La ricerca non è giustificata.

---

## 4. ⚠ CORREZIONE A UNA MIA CORREZIONE (commit `8447f47`, `996b2c4`)

Stamattina avevo scritto: *«lo scarto passa da 0.037 a 0.338 perché `pendenza(tau)` era misurata su
20 nodi invece che 2195»*, e l'avevo messo in `CLAUDE.md` §9 come fatto.

**È sbagliato.** A parità di passo le due strade danno **lo stesso numero**:

| passo | diretta | indiretta | scarto |
|---|---|---|---|
| 300 | +1.176 (2195 nodi) | +1.178 (dalle stesse 2195) | **0.002** |
| 400 | +1.812 (20 nodi) | +1.867 (dalle 2781) | **0.055** |

> **La differenza fra +1.176 e +1.812 non è 20-vs-2195: è 300-vs-400. È il TEMPO.**
> `tau(t)` evolve, e con esso lo scarto — che è il **transitorio**, non un difetto di campionamento.

**Cosa resta valido e cosa no:**
- **resta valido** il presidio generale *«una pendenza si riporta col suo errore standard»* — ed è
  proprio applicandolo che si è visto che `SE = 0.0097`, non 0.3;
- **NON resta valido** *«una pendenza su 20 nodi non è una pendenza»* **come spiegazione di questo
  caso**: qui i 20 nodi davano il numero giusto. Resta una buona regola di prudenza, ma **non era la
  causa**, e in `CLAUDE.md` §9 era scritta come se lo fosse.

**Ho corretto la causa sbagliata con un'altra causa sbagliata, e me ne sono accorto solo facendo il
check che Luca ha chiesto.** È il secondo errore della stessa giornata sulla stessa catena, e va
scritto così.
