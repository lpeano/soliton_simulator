# REFERTO — **il passo 198: né artefatto numerico, né fenomeno collettivo. È UN NODO NEONATO**

**Blob `7c4dec1d`** · seme **42** · 11 snapshot a **6 passi** (180-240), rigiocata **sigillata
3/3** · strumento `csv/_test_fork/_passo198.py` (`5267eaf0`), esito `_passo198.txt` · letture
fissate **PRIMA** in `doc/TASK_HISTORY/2026-09-19_passo198.md` (`8132be8`).

> **`--tau-luce` sigillo 6/7. UN SEME, UNA SCENA. Nessun run, nessuna cura.**

---

## 1. LA DISTRIBUZIONE NON SI MUOVE. **ANZI, SCENDE**

```
passo   p25     p50         p75       p95      p99      max     | n>1e1  n>1e2
192     0       5.04e-16    0.08953   0.1744   0.2266   0.3097  |   0      0
198     0       1.53e-15    0.08438   0.1646   0.2144   401     |   1      1
```

**Mentre il massimo fa `×1295`, `p75`, `p95` e `p99` CALANO.** E i nodi sopra `100` sono **UNO**.

> **Non è la popolazione che si sposta: è un singolo nodo su 2394.**

### ⚠ Il verdetto automatico dice «nessuna delle due», e il difetto è del MIO criterio `B`

```
quota della mediana sul salto (log/log): 0.1549   [A vuole >= 0.30]   -> A non scatta, giusto
nodi sopra 10*p99(192): 1                [B vuole <= 100]             -> ok
p50: 5.04e-16 -> 1.53e-15  (x3.03)       [B vuole < x2]               -> B NON scatta
```

**`B` non scatta per un rapporto fra due numeri che valgono entrambi `~10⁻¹⁵`: sono zero
macchina.** Il `×3.03` **non significa «la mediana si muove»**, significa che numeratore e
denominatore sono rumore di arrotondamento. **Avevo scritto un criterio su un rapporto senza
chiedermi se il denominatore fosse un numero.**

> **Non cambio il criterio a posteriori** — resta quello di `8132be8`. **Riporto che non scatta, e
> perché**: il dato è **un nodo su 2394**, e non ha bisogno del criterio per essere letto.

## 2. I TRE CANDIDATI NUMERICI — **cadono TUTTI E TRE, e sono DATATI**

| candidato | misura | esito |
|---|---|---|
| **① `_cs_lam_degenere`** | **`+0` in TUTTI e dieci gli intervalli**; il contatore vale già `2` al passo 180 | **CADE**: le due occorrenze sono **prima** del 180 |
| **② `_fatt_cs_ultimo`** | `p50` fermo a `1.48`, max oscilla `9.9-14.7`, **nessun attraversamento** | **CADE**: il `142.8` del passo 2700 arriva molto dopo |
| **③ `NaN`/`inf`/overflow** | **ZERO** su 8 campi × 11 istanti, e **zero** valori oltre `1e10` e `1e15` | **CADE** |

> **L'evento del passo 198 NON è un'eccezione numerica.** Nessun `NaN`, nessuna divisione
> degenere, nessun overflow — e i contatori lo dicono **con le date**, non per argomento.

## 3. CHI È IL NODO — **e la catena è completa**

```
indice 2393 su n = 2394        <- L'ULTIMO, cioe' il piu' recente
|omega_s|  0.1323 (passo 192)  ->  400.99 (passo 198)     x3031
(al 192 il massimo era il nodo 52: questo nodo NON era anomalo sei passi prima)

                 questo nodo      mediana popolazione
eta              0.0607           1.4968        <- NEONATO: ~8 passi di eta'
_deg             2                496           <- IL GRADO DI NASCITA
|psi|            2.82e-06         0.0470        <- 17 000 volte piu' piccolo
rho_spin         5.70e-10         0.0123        <- 20 MILIONI di volte piu' piccolo
peq (sui suoi archi)  1.09e-06    0.00129       <- 1200 volte piu' piccolo
```

**E il pavimento dell'inerzia è `1e-6`** (`CLAUDE.md` §9: `inerzia = max(rho_sorgente, 1e-6)`).
**Questo nodo ha `rho ≈ 5.7e-10`: MILLE VOLTE SOTTO IL PAVIMENTO.**

### E vale per TUTTI i nodi che schizzano, a ogni istante

```
passo   n<1e-6   nodi con om>1e2   eta mediana   deg mediano   rho mediana
198       3            1             0.0607          2          5.7e-10
216       9            4             0.0384          2          7.0e-10
240      26           12             0.148           2          5.9e-09
```

> **Sono SEMPRE neonati** (`eta` `0.04-0.16` contro `1.5` della popolazione), **sempre a grado 2**
> — il grado di nascita — **e sempre con `rho ~10⁻⁹`, mille volte sotto il pavimento.**

**E il contatore `_sfondo_ko_rho` scatta per la PRIMA volta esattamente al passo 198** (`+0, +0,
+0` ai passi 186/192, poi **`+1` al 198**, poi `+1, +2, +3, +0, +4, +9, +4`): **è il contatore dei
nodi che cadono nel fallback dello sfondo PER `rho`.**

### Il Jaccard dice che è un CONTAGIO, non un evento isolato

```
192 -> 198   |A|=0  |B|=1   J = 0.0000    <- nasce il primo
198 -> 204   |A|=1  |B|=1   J = 1.0000    <- resta SOLO lui
204 -> 210   |A|=1  |B|=1   J = 1.0000
210 -> 216   |A|=1  |B|=4   J = 0.2500    <- se ne aggiungono tre
216 -> 222   |A|=4  |B|=5   J = 0.8000
...
234 -> 240   |A|=10 |B|=12  J = 0.8333
```

**Uno parte, resta solo per 12 passi, poi la popolazione anomala cresce senza che i vecchi
escano** *(Jaccard alto = sono sempre gli stessi più i nuovi)*.

## 4. COSA QUESTO È, E COSA NON È

**NON è un quarto candidato inventato.** È **il meccanismo che `CLAUDE.md` §9 descrive già**:

> *«`inerzia = np.maximum(_rho_sorgente(), 1e-6)` … il pavimento è attivo sul 99.7 % dei nodi, e
> `omega = coppia/inerzia ~ 6e4` mentre la coppia è ORDINARIA»*

**Ma con una differenza che cambia la natura del fenomeno.** Là il pavimento era attivo **sul
99.7 % dei nodi**, perché la densità mediana valeva `1.21e-07`. **Qui la densità mediana è `~1e-2`:
il pavimento NON è attivo sulla popolazione, ed è attivo SOLO sui neonati.**

> **Quindi non è più una proprietà globale del regime: è un difetto DEI NODI APPENA NATI**, che
> nascono con `rho` mille volte sotto il pavimento e il cui `omega = coppia/inerzia` esplode di
> conseguenza.

**Cosa NON ho misurato, e non invento:** **la coppia**. La catena
*«`rho` sotto il pavimento → `inerzia` al pavimento → `omega` esplode»* è **coerente con tutti i
numeri raccolti**, ma l'ultimo anello — che la coppia su quel nodo sia **ordinaria** — **non l'ho
misurato qui**. *(Lo era nel caso di `CLAUDE.md`: `0.06`.)*

## 5. COSA RESTA APERTO

- **la coppia su quei nodi**: se fosse anch'essa anomala, la lettura cambierebbe;
- **perché un neonato nasca con `rho ≈ 5.7e-10`** quando la mediana è `10⁻²`;
- **perché il contagio**: i nodi anomali passano da 1 a 12 in 42 passi, e il Jaccard dice che
  **nessuno guarisce**.
