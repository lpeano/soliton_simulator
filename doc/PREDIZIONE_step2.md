# PREDIZIONE — STEP 2: agganciare l'OROLOGIO alla METRICA (`omega_clk *= (cs/CS_M)^2`)

> **Scritta e committata PRIMA di toccare il codice.** Branch `fork-su2`, blob **2277e9a0**.
> Data: 2026-09-14. Un solo interruttore nuovo, OFF di default.

---

## 0. PERCHE' NON E' UNA MANOPOLA

Verificato dal disco: la metrica legge solo `|psi|^2` (`cs = _cs_nodo(...)`, `:2762`) e l'orologio
**non legge `cs`**. I due tempi propri — metrico `tau_p = d/cs` e orologio `dt_n = DT*r` — sono
**scollegati**. Lo Step 2 progettato (`omega_clk *= (cs/CS_M)^2`) non e' mai stato cablato.

L'aggancio e' l'**orologio di Compton**: `omega = m c^2 / hbar`. La frequenza propria di una massa
va come `c^2`; nel modello `c` e' `cs`. Quindi `omega ∝ cs^2` e' **fisica necessaria, derivata**,
zero parametri: e' l'unico aggancio orologio↔metrica lecito. A `cs = CS_M` il fattore vale
**esattamente 1** — la riduzione al limite e' esatta per costruzione, non per taratura.

---

## 1. LOCALIZZAZIONE (fatta prima di cablare, dal sorgente)

| grandezza | dove | cosa fa |
|---|---|---|
| `omega_clk` | `:1926` (ramo deparam) `= (coerenza d'arco) * r_node`; `:1931` (legacy) `= (rho/rho_c) * r_node` | entra in `:1960` `_phc = exp(-0.5j * s_k * omega_clk * dt)`, applicata come **fase globale** allo spinore (`:1961`) |
| `r = ritmo()` -> `dt_n = DT*r` | `:2476` | e' il **tic del tempo proprio** che tutta la fisica integra |

**Il punto d'aggancio e' `omega_clk`**, non `r`: e' l'orologio de Broglie/Compton.

**Ordinamento:** `_passo_spinoriale` gira a `:2691`, `cs_nodo = self._cs_nodo(I, w)` a `:2762`.
**L'orologio viene PRIMA della metrica** — stessa situazione della coppia nello Strato 1. Quindi si
usa `self._cs_nodo_prev` (il `cs` del passo precedente), che **esiste gia'** (`:839` init, `:2767`
scrittura) ma e' scritto **solo sotto `FORK_SU2_MEM`**: il plumbing e' estendere quella condizione
al flag nuovo, e **nient'altro**.

---

## 2. LE TRE PROTEZIONI DI LETTURA (il cuore di questa predizione)

Scritte prima perche' i risultati non vengano letti al contrario.

### 2.1 — Il VERDETTO del cablaggio e' **S3**, il rapporto diretto

`omega_eff / omega_base = (cs/CS_M)^2`, adimensionale, verificabile a **~1e-15**. Questo, e solo
questo, dice se lo Step 2 e' cablato bene.

### 2.2 — Il profilo di `dt_n` e' un effetto **INDIRETTO**, atteso piccolo, **NON e' il criterio**

Moltiplicare `omega_clk` **non tocca `dt_n`**: tocca `_phc`, cioe' la **fase** dello spinore. La via
verso `dt_n` esiste ma passa per **quattro anelli**:

```
omega_clk  ->  _phc  ->  psi_spin  ->  ritmo()  ->  dt_n
```

(`ritmo()` sotto `--campo-spinoriale` legge `angle(psi_spin) - angle(_psi_spin_prec)`, e `psi_spin`
porta `_phc`.) Con in piu' il fatto che alle densita' attuali **`cs` e' quasi-costante**
(`I~0.05` contro la soglia `~400`), quindi `(cs/CS_M)^2 ~ 1`.

> **S3 PASS + profilo di `dt_n` piccolo = Step 2 cablato BENE.** L'effetto e' smorzato dalla catena
> e da `cs` quasi-costante: **non e' un bug**. Leggere "dt_n piccolo = fallimento" sarebbe l'errore.

### 2.3 — Le firme di SPIN devono restare invariate: e' **conferma**, non fallimento

`_phc` e' una fase **globale per nodo**, e il Bloch `nb = psi^dag sigma psi` e' **invariante** per
fase globale — verificato numericamente: `max|bloch(psi) - bloch(psi e^{i phi})| = 3.3e-16`.
Quindi lo Step 2 vive nel canale **U(1)/orologio** e **non puo'** muovere la direzione SU(2).

> Firme di spin (`chi`, `<n>`, autocorrelazione) statisticamente invariate = **lo Step 2 fa il suo
> mestiere**. Non e' "non funziona": e' orologio↔metrica, non spin.

**MA ATTENZIONE A UN TERZO ERRORE, speculare:** `omega_clk` e' **diverso da nodo a nodo**, quindi le
**fasi RELATIVE fra nodi** cambiano — e `_coppia_interferenza` calcola `Im<psi_i|psi_j>`, che dalle
fasi relative **dipende**. Quindi la forza cambia, la traiettoria diverge, le mitosi cambiano, `N`
cambia. L'attesa corretta non e' *"chi e <n> identici"* ma:

> **`chi` e `<n>` statisticamente invariati (90 gradi / 39), ma NON bit-identici.** Una piccola
> deriva delle firme di spin e' **caos via fasi relative**, **non** un'azione sullo spin. Leggerla
> come "lo Step 2 tocca lo spin" sarebbe l'errore speculare a quello del §2.2.

---

## 3. LA FIRMA ATTESA (verso e scaling, non grandezza)

- **cs < CS_M** (pozzo, alta densita') -> `omega_clk` **cala** come `cs^2` -> l'orologio proprio
  **RALLENTA** dove la densita' e' alta = **redshift gravitazionale**.
- **Conferma:** rapporto `omega_eff/omega_base` che segue `(cs/CS_M)^2` **esatto**; e, se
  osservabile, `dt_n`/fase piu' lenti nel nucleo che nel vuoto.
- **Falsificazione:** rapporto che **non** segue `(cs/CS_M)^2` (potenza sbagliata), oppure **segno
  invertito** (orologio piu' VELOCE nel pozzo). Quello sarebbe un reperto, e ci si ferma.

**Conta il VERSO e lo SCALING, non la grandezza.** A `cs` quasi-costante l'effetto e' piccolo **per
costruzione**.

---

## 4. I SIGILLI (definiti prima)

| | cosa verifica | criterio |
|---|---|---|
| **S1** | flag OFF byte-identico al codice pre-modifica | `max\\|A-B\\| = 0.000e+00` (con il conteggio nodi accanto: uno zero senza confronto non vale) |
| **S2** | riduzione al limite: ON con `cs = CS_M` ovunque | byte-identico a OFF, **0 esatto** |
| **S3** | **IL DECISIVO**: verso e scaling | `omega_eff/omega_base = (cs/CS_M)^2` a ~1e-15, su `cs/CS_M = 1.0, 0.5, 0.1`; e l'orologio **rallenta** dove `cs` cala |
| **S4** | stabilita' | ON su run breve: nessun NaN/inf, nessun runaway |

S3 deve esercitare il **percorso reale** del codice, non ricalcolare la formula inline — stesso
monito del sigillo N e di S7 (Strato 1).

---

## 5. COSA QUESTO NON FARA'

Non "risolvera'" lo spin: aggancia l'orologio alla metrica, **non organizza i Bloch** — e per il
§2.3 non **puo'** farlo. Non aggiunge floor ne' coefficienti: solo `(cs/CS_M)^2`. Non accende altro.
Non conclude sulla fisica (par.2.7: nessuna conclusione sotto ~2000 passi, mai su un solo seme).
E a `cs` quasi-costante, **qualunque** effetto dinamico sara' piccolo per costruzione: il test e'
che il **meccanismo risponda nel verso giusto e scali come `cs^2`**.
