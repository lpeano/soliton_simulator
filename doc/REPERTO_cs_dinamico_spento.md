# REPERTO — `--cs-dinamico` era **SPENTO** nel braccio OFF. E accenderlo **non basterebbe**.

**Data:** 2026-09-15 · **Branch:** `fork-su2` · **Blob:** `08784685` (dal disco)
**Rilievo di Luca. Il braccio ON NON è stato lanciato.**

---

## 1. LA PROVA DAI DATI — e non è `0`, è `nan`

`cs_std`, `cs_min`, `cs_max` nei CSV del braccio OFF, **tutti gli 11 campioni di entrambi i semi**:

```
_vuoto_pulito1_s1.vuoto.csv   cs_std / cs_min / cs_max  =  nan  (valore unico su 11 campioni)
_vuoto_pulito2_s2.vuoto.csv   cs_std / cs_min / cs_max  =  nan  (valore unico su 11 campioni)
```

> **`nan` è una prova PIÙ FORTE di `0`.** Uno `0` direbbe *«`cs` c'era, e non variava»*. Il `nan`
> dice che **la cache `_cs_nodo_prev` non esiste affatto.**

**La catena causale, letta dal codice e non dedotta:**

| passo | evidenza |
|---|---|
| l'osservatore scrive `nan` **solo** se `_cs_nodo_prev is None` | `_osserva_vuoto.py:266-270`, ramo `else` |
| la cache è scritta **solo** dentro `if CS_DINAMICO:` | `soliton_simulator.py:2924` → `:2930` |
| …e dentro `if FORK_SU2_MEM or STEP2_OROLOGIO:` | `:2926` |
| `FORK_SU2_MEM` valeva **1**, letto dal CSV | colonna `FORK_SU2_MEM` |

⇒ **l'unica condizione che poteva mancare è `CS_DINAMICO`. Era `False`.**

## 2. LA SECONDA PROVA, INDIPENDENTE — il log in-run

```
[osserva-flag] tag=pulito1 seed=1  … STEP2=False CS_DIN=False GAMMA_TURBO=1  (letti DURANTE il run)
[osserva-flag] tag=pulito2 seed=2  … STEP2=False CS_DIN=False GAMMA_TURBO=1  (letti DURANTE il run)
```

Letti **dai globali vivi durante il ciclo**, non da prima del run. Due strade indipendenti, stessa
risposta.

**⚠ E un difetto di certificabilità nel difetto:** quei log **non erano committati**. Erano l'unica
traccia del comando eseguito, e vivevano solo sul disco. **Committati con questo documento.**

---

## 3. ⚠ IL NUMERO CHE CAMBIA LA DECISIONE: accendere il flag **NON** risolve

Il rilievo propone la config corretta con `--cs-dinamico` acceso in entrambi i bracci. **La proposta
è giusta come principio, ma non otterrebbe ciò che si vuole**, e va detto **prima** di spendere
tempo macchina.

**Dove `--cs-dinamico` ERA acceso** (sigillo della cura della cache, `_sigillo_fix_cache.txt` P4):

```
cs cache: min 1.99954   max 2.0   (CS_M = 2)     ->  max/min = 1.000230
tau = d/cs: min 0.0271257   max 1.05089          ->  max/min = 38.74
```

| | escursione | in log |
|---|---|---|
| `tau = d/cs` | **×38.74** | 3.6569 |
| di cui dovuta a **`cs`** | **×1.000230** | **0.000230** |

> **La quota di `cs` sulla dispersione di `tau` è `0.00629 %` — UNA PARTE SU 15 898.**
> La soglia posta dal rilievo stesso è **1 %**. Siamo **160 volte sotto**.

**Quindi `tau = d/cs` è `tau ∝ d` a due parti su diecimila, ANCHE col flag acceso.** Non è un
artefatto della config: è il fatto già in `CLAUDE.md` §6 — *«a densità reali `cs` è MORTO, `I ~ 0.05`
contro soglia `~400`»* — visto dal lato di `tau`.

**Conseguenza per la decisione:** rifare il braccio OFF con `--cs-dinamico` acceso costerebbe
**~2 minuti a seme** e produrrebbe **la stessa interpretazione**: `tau ∝ d`. Comprerebbe la
*correttezza formale della config*, non un contenuto diverso.

---

## 4. UNA CORREZIONE AL RILIEVO — verificata dallo script committato

Il rilievo dice: *«il fix della cache non ha alcun effetto in quei run — il che spiegherebbe anche
perché il suo contributo a T3 è stato solo 16.9 %»*.

**La prima metà è vera, la seconda no.** `csv/_test_fork/_rimisura_t3.py`, riga 24, committato:

```python
"--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
```

**T3 girava CON `--cs-dinamico`.** Il fix della cache era **pienamente esercitato** lì. Il 16.9 % non
si spiega con «non c'era niente da riparare».

*(E c'è dell'altro: il 16.9 % è **già stato ritirato** — `doc/FIX_cache_cs.md` §7. Su 3 semi il
segno di `Delta` non è nemmeno concorde: **−0.0445 / +0.0367 / −0.0635**, `t = −0.77`. Era
**dispersione di run**. Non c'è un 16.9 % da spiegare.)*

---

## 5. COSA RESTA VALIDO, E COSA VA RI-ETICHETTATO

**Il braccio OFF non si butta: si marca.** È una misura valida **di ciò che è girato davvero** —
un sistema con `cs = CS_M` costante. Le firme (`chi` a `z = −0.37 / +0.75`, autocorrelazione piatta,
frazioni ai poli simmetriche) **non dipendono da `cs`**: restano.

**Il braccio ON resta interessante — ma per un'altra ragione di quella dichiarata.**
Non misurerebbe *«densità contro tempo-luce»*: misurerebbe **densità contro distanza**
(`tau ∝ d`). **Ma il suo valore vero è un altro e non cambia:** è l'unica leva che porta `theta` da
**~96 a ~43 giri/passo**, cioè **il gradiente di risoluzione**, che è il motivo per cui il mandato a
due bracci esiste.

> **La sostanza del test sopravvive; il nome della variabile no.** Il referto dovrà dire
> **`tau ∝ d`**, non *«tempo-luce»* — e dovrà dirlo **nella stessa riga** in cui dà il numero, non
> in nota.

---

## 6. LE TRE CONSEGUENZE DEL RILIEVO, quantificate

| # | conseguenza | verdetto |
|---|---|---|
| 1 | *«`tau = d/cs` con `cs` costante è `tau ∝ d`»* | **VERA** — e **vera anche col flag acceso**: `cs` pesa `0.00629 %` |
| 2 | *«il fix della cache non ha effetto in quei run»* | **VERA per l'osservatore**, **FALSA per T3** (che aveva `--cs-dinamico`). E il 16.9 % era già ritirato |
| 3 | *«la sostituzione perde la giustificazione principale»* | **VERA oggi, e non per la config:** `inerzia = T² = (d/cs)²` vive sul `cs` locale, e il `cs` locale è morto alle densità simulabili (§6). Non è riparabile con un flag |

---

## 7. STOP — e cosa propongo (senza eseguire)

**Il braccio ON non è partito.** Tre opzioni, e la scelta è di Luca:

| | cosa | costo | cosa compra |
|---|---|---|---|
| **a** | lanciare il braccio ON **così com'è**, ri-etichettando il referto `tau ∝ d` | ~2 min/seme | il **gradiente di risoluzione** (96 → 43 giri/passo), che è lo scopo dichiarato |
| **b** | rifare **entrambi** i bracci con `--cs-dinamico` acceso | ~8 min (4 run) | la **correttezza formale** della config. **Non** un contenuto diverso: `cs` pesa 1/15 898 |
| **c** | fermarsi e portare prima `theta` sotto il tetto | — | evita di misurare ancora un settore aliasato |

**Propongo (a)**, per una ragione sola: **il gradiente di risoluzione non dipende da `cs`.** Il
braccio ON serve a vedere se una firma emerge quando l'aliasing scende di un fattore ~2.2, e quella
domanda resta intatta anche se `tau` si chiama `d` invece che `d/cs`.

**Non eseguo nulla senza il via.**
