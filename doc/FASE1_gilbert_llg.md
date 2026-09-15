# FASE 1 — il termine di Gilbert/LLG: **analitico, nessun run, nessun codice**

**Data:** 2026-09-15 · **Branch:** `fork-su2` · **Blob:** `08784685` (dal disco)
**Esito: NON si cabla. Tre ragioni, in ordine di gravità — e la terza è una domanda per Luca.**

---

## 0. IL VERDETTO IN TRE RIGHE

1. **`lambda` SI DERIVA dal FDT, a zero parametri** — ed è **~10⁴ volte troppo debole**. Già fatto e
   committato stamattina (`doc/ANALISI_gilbert_fdt.md`). **Il mandato non lo sapeva.**
2. **La formula del mandato per `lambda` è dimensionalmente incompleta.**
3. **⚠ Il punto di cablaggio proposto NON produce allineamento** — e, verificando, è emerso che
   **la dinamica esistente orienta `n` verso `−B`, non verso `+B`.** *Questo va risolto prima di
   qualunque cablaggio, e la decisione non è mia.*

---

## 1. `lambda` si deriva — **ed è già stato fatto**, con lo stesso metodo che il mandato chiede

`doc/ANALISI_gilbert_fdt.md` §4 (blob di stamattina, commit già in storia):

```
rumore sul Bloch:   D = 2·amp²/dt
Langevin:           <theta²> = D/(2·lambda)
Boltzmann:          <theta²> = 2·kT/|B|
=>                  lambda = amp²·|B| / (2·dt·kT)
```

Con l'unica temperatura parameter-free del sistema (`kT = Lam`, l'energia del vuoto **da cui il
rumore stesso è costruito**), **`Lam` si cancella**:

> **`lambda = |B|/(2·dt) = 3.47/tempo` → tempo di allineamento **28.8 passi***
> *(115 passi con la stima di vuoto puro `amp² = Lam/4`: i due differiscono di 4× e non cambiano il
> verdetto.)*

**Contro un rimescolamento misurato di `0.0030` passi** → lo smorzamento FDT è **~10⁴ volte più lento
del disordine che dovrebbe combattere.**

### La lettura del mandato ha un ramo che non prevede

| il mandato dice | misurato |
|---|---|
| `lambda` si deriva → `\|omega\|_eq` sotto soglia → **cabla** | no |
| `lambda` si deriva → scende ma resta aliasato → **cabla, dillo** | **no: non scende in modo apprezzabile** |
| `lambda` **non** si deriva → **STOP** | no: **si deriva benissimo** |

> **C'è un quarto esito, ed è quello vero: `lambda` si deriva a zero parametri ED È QUANTITATIVAMENTE
> TRASCURABILE.** Non è «manca un ingrediente»: l'ingrediente c'è, ed è piccolo di quattro ordini.
> Per scendere sotto i 30°/passo servirebbe un `tau` **1.8·10⁶ volte** più piccolo — e il FDT non lo
> licenzia: per giustificarlo il rumore dovrebbe essere più forte dello stesso fattore, e non lo è.

---

## 2. La formula del mandato è dimensionalmente incompleta

Il mandato scrive `lambda = amp²/(2·kT)`. **Non è un tasso:** `amp²/kT` ha le dimensioni di
un'energia inversa per un'ampiezza al quadrato, non di `1/T`. Mancano **`|B|`** (che porta la scala
del campo) e **`/dt`** (che trasforma la varianza *per passo* in una *diffusione*).

La forma completa è quella del §1: `lambda = amp²·|B|/(2·dt·kT)`. **Non è un cavillo:** è proprio il
`1/dt` che fa cancellare `Lam` e rende il coefficiente parameter-free. Con la formula del mandato il
risultato dipenderebbe ancora dalla temperatura scelta — cioè sarebbe **una manopola travestita**.

---

## 3. ⚠ IL PUNTO DI CABLAGGIO NON PRODUCE ALLINEAMENTO

Il mandato propone:

```python
correzione = cross(B, nb) + cross(nb_grav, nb) - lambda * cross(nb, cross(nb, B))
```

**Ma `correzione` è una COPPIA, non una velocità.** Dal codice (verificato, righe 1984 e 2136-2142):

```python
omega_new = omega_src + dt_n·(correzione/inerzia - omega_src/_tau)      # omega e' uno STATO
nb_new    = Rodrigues(nb, omega_hat, |omega|·dt_n)                      # n e' RUOTATO da omega
```

> **La dinamica è del SECOND'ordine:** `omega` ha inerzia ed è una variabile di stato; `n` è ruotato
> da `omega`. **LLG è del PRIM'ordine:** `dn/dt = −lambda·n×(n×B)`.

Mettere un termine di `dn/dt` dentro `domega/dt` **non dà LLG**: dà un'**accelerazione angolare**
lungo `B_perp`, cioè una rotazione *attorno* a `B_perp`, non un moto *verso* `B`. È un errore di
ordine dell'equazione, non di segno.

**E c'è una conseguenza che il registro non aveva colto.** Il registro dice: *«`−ω/τ` frena ma non
orienta; manca il "tira verso"»*. **È incompleto:** frenare **da solo** non orienta, ma
**frenare + coppia di richiamo = pendolo sferico smorzato, che orienta.** Il meccanismo orientante
**c'è già**; è solo del second'ordine (approccio oscillante) invece che del primo (sovrasmorzato).

---

## 4. ⚠⚠ E VERIFICANDO QUEL PUNTO È EMERSA UNA DOMANDA SUL SEGNO

Riproducendo **esattamente** lo schema del codice (`correzione = np.cross(B, nb)`, riga 1956;
integrazione riga 1984; Rodrigues righe 2140-2142), con `B` fisso e rumore spento:

```
passo     0   n·B = +0.825   angolo =  34.4 gradi
passo  2000   n·B = -0.938   angolo = 159.8 gradi
passo  8000   n·B = -0.772   angolo = 140.6 gradi
passo 19999   n·B = -0.994   angolo = 173.9 gradi
```

> **`n` si allontana da `B` e si stabilizza verso `−B`.** Il punto stabile della dinamica esistente è
> **ANTIPARALLELO** al campo dei vicini.

**Perché:** la coppia standard di un momento in un campo è `n × B`; il codice usa `B × n`, che è
`−(n × B)`. In una dinamica del second'ordine con attrito, il segno decide **quale dei due poli è
stabile**.

### Non lo chiamo un bug, e dico perché

**Potrebbe essere voluto.** `B` non è il campo dei vicini nudo: è costruito con una **riflessione**
per i legami fra uguali (`refl` inverte `z`, righe 1932-1934), e i commenti parlano di strutture
**staggered / antiferromagnetiche**. Una convenzione antiferro coerente è una scelta fisica
legittima, non un errore.

**Ma va deciso prima di cablare LLG**, perché il termine che il mandato vuole aggiungere orienta
verso **`+B`**: se la coppia esistente orienta verso **`−B`**, i due termini **si oppongono**, e il
risultato non sarebbe «più allineamento» ma una competizione fra due leggi con punti fissi opposti.

**La domanda per Luca, secca:**
> **Il punto fisso del settore di spin deve essere `n ∥ B` (ferro) o `n ∥ −B` (antiferro)?**
> Oggi il codice fa **antiferro**. Il termine LLG proposto fa **ferro**. **Non possono convivere
> senza una decisione.**

*(Nota: nulla di ciò contraddice le misure. `chi ≈ 90°` significa **nessun** ordine, né ferro né
antiferro, perché il rumore rimescola 10⁴ volte più in fretta di quanto la dinamica orienti — §1.
Il segno determina **dove** andrebbe il sistema se l'orientamento funzionasse, non dove sta oggi.)*

---

## 5. COSA PROPONGO — e non eseguo

1. **Non cablare LLG.** Motivo primario: `lambda` derivato è **10⁴ volte troppo debole** — cablarlo
   aggiungerebbe un termine che non muove nulla, e la stessa cosa varrebbe per il segno.
2. **Rispondere prima alla domanda del §4.** È a costo zero (una decisione), e **cambia il segno di
   un termine già in produzione**: vale più di qualunque cablaggio nuovo.
3. **Se si vuole comunque un test:** l'esperimento onesto non è aggiungere LLG, è **misurare dove va
   `n` a rumore spento** — cioè verificare *nel simulatore* ciò che il §4 mostra *nello schema*.
   È un run breve, pure-read sul verso, **e deciderebbe la domanda senza toccare la fisica.**

**Ciò che NON propongo:** mettere un `lambda` più grande di quello derivato. Sarebbe **sceglierlo**
(§3, zero manopole) e mettere **dissipazione senza fluttuazione** — lo stesso errore del FDT,
ribaltato. È già scritto in `CLAUDE.md` §9 e resta valido.
