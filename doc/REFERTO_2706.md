# REFERTO — **IL 2.706 NON È UN FATTO SUL FEEDBACK.** E il sigillo `F3` fallisce già adesso

**Data:** 2026-09-17 · **Branch:** `fork-su2` · **Blob** `5d61af08` (byte) / `425e4aaa` (git)
**Sonda:** `csv/_test_fork/_sonda_2706.py` · **Output:** `_sonda_2706.txt`, `_sonda_2706_tau2.txt`
**Mandato:** §1 — *«non si certifica un componente di cui non si sa cosa sia»*. **Nessun sigillo,
nessun run di misura, nessuna promozione.**

---

## 0. IN UNA RIGA

**Il rapporto `|feedback|/|coppia|` non è una costante: decade di ~5 ordini di grandezza lungo il
run, e negli ultimi 10 passi vale `0.75` — cioè il feedback è più PICCOLO della coppia.** Il
`2.706` era una **media su una popolazione non stazionaria**, dominata dal transitorio.
**E strada facendo è caduta una cosa più grossa: `sum(out) ≠ 0`. Il termine NON è antisimmetrico.**

---

## 1.1 — È UN ARTEFATTO DI CONFRONTO (A3c)? **Sull'asse che il mandato indicava, NO. Su un altro, SÌ.**

**Quello che è PULITO, verificato e non assunto:**

| controllo | esito |
|---|---|
| stessa **popolazione**? | `len(feedback) = len(coppia) = n = 484`, **entrambe per-nodo** ✓ |
| stesso **statistico**? | `median(abs(·))` contro `median(abs(·))` ✓ |
| stesso **istante**? | entrambe dentro la stessa invocazione, `coppia` catturata da `_coppia_interferenza` nello stesso passo ✓ |
| nodi con feedback **esattamente zero** | **0 su 484** — e se ce ne fossero, abbasserebbero la mediana del feedback, cioè **sottostimerebbero** il rapporto, non lo gonfierebbero |
| **`_spinor_lift` è normalizzato?** *(il mandato lo assume)* | **`norma ∈ [1.000000, 1.000000]` su 64 invocazioni.** L'assunzione **regge**, e `imag(ov)` è davvero in `[−1, 1]` |

**Quello che NON è pulito, ed è il mio errore:**

> **La MEDIA dei rapporti per-passo è lo statistico sbagliato, perché la popolazione NON è
> stazionaria.**

```
distribuzione del rapporto su 64 invocazioni (TAU_A = 2.0, la configurazione dell'esperimento)
   MEDIA        2086.2       <- dominata dai primi passi
   MEDIANA         1.834
   p25 / p75       1.113 / 9.507
   min / max       0.698 / 54844      ->  4.9 ORDINI di escursione
   ultimi 10 passi (il regime)  mediana   0.748
   passi col rapporto < 1                 14 su 64  (21.9 %)
```

**È l'UNDICESIMO caso di A3c, e cade sul mio stesso rimedio.** Avevo sostituito *«due massimi presi
in passi diversi»* con *«media dei rapporti per-passo»* — stessa popolazione, stesso istante,
**stessa unità**. Ma A3c dice *«stessa POPOLAZIONE»*, e **una popolazione che si muove di cinque
ordini non è una popolazione**: la media ne descrive i primi campioni e **nessun passo reale**.
La forma dell'errore è la stessa di sempre, spostata di un asse: dallo **spazio** al **tempo**.

---

## 1.2 — DA COSA VIENE L'AMPIEZZA? **Dalla coppia, non dal feedback.**

| passo | `\|imag(ov)\|` med | `w/grado` med | `\|feedback\|` med | `\|coppia\|` med | rapporto |
|---|---|---|---|---|---|
| 0 | 0.00163 | 0.0506 | 0.00114 | **2.09e-08** | 54844 |
| 16 | 0.01598 | 0.00743 | 0.01149 | 1.27e-03 | 9.05 |
| 32 | 0.03548 | 0.00737 | 0.02300 | 1.31e-02 | 1.75 |
| 63 | 0.06838 | 0.00712 | 0.04229 | **6.02e-02** | **0.70** |

**Il conto è diretto:** da 0 a 63 passi, **`\|coppia\|` cresce di un fattore ~2.9 MILIONI**
(`2.1e-8 → 6.0e-2`), mentre **`\|feedback\|` cresce di un fattore ~37** (`0.0011 → 0.042`).
**Il rapporto non misura il feedback: misura quanto è piccola la coppia all'inizio.**

E le sotto-grandezze dicono che il feedback è **ordinario**, non grande:
- `|imag(ov)|` mediana **0.035**, max 0.852 — **ben dentro `[0,1]`**, e molto sotto lo 0.5 di
  spinori scorrelati: gli spinori adiacenti sono **quasi in fase**, come ci si aspetta dopo una
  mitosi che copia esattamente;
- `w/grado` mediana **0.0073** — piccolo, non grande;
- `|feedback|` mediana **0.0228**, **sotto** il valore sotto ipotesi nulla stimato prima della
  misura (`~0.5/grado ≈ 0.1`).

> **La TERZA lettura del mandato è quella giusta, con una precisazione:** il fatto non è
> *«la coppia è piccola»* in assoluto — **a regime coppia e feedback sono dello stesso ordine**
> (0.060 contro 0.042). Il fatto è che **la coppia parte sei ordini sotto il suo valore di regime**,
> e il rapporto eredita quel transitorio.
>
> **Quindi la frase del referto precedente — *«non è una correzione, è il motore»* — NON REGGE.**
> Era vera del transitorio e falsa del regime, e io l'avevo scritta del componente.

---

## 1.3 — DOVE È APPLICATO? **Nella stessa somma, prima della stessa divisione — e la divisione è per una COSTANTE**

```
:3041   coppia = self._coppia_interferenza(A, z)      la coppia PRINCIPALE
:3094   coppia = coppia - fattore * dHdphi            repulsione (ramo REPULS_LEGGE)
:3109   coppia = coppia + MU_PSI * dHdphi             vecchia repulsione (ramo elif, MORTO)
:3117   _cm = median(|coppia|)                        <-- QUI si MISURA
:3129   coppia += _fb                                 <-- QUI si APPLICA
:3154   coppia = coppia + twist_nodo                  twist TW/Hall (DOPO la misura; TW off)
:3195   delta_phivel = dt_n_s * (coppia - ...) / M_PH
```

**`coppia` e `_fb` sono commensurabili: stessa somma, stessa divisione.** E il divisore è
**`M_PH = 1.0`**, una **costante** — la divisione è letteralmente un no-op.

### ⚠ UNA PREMESSA DEL MANDATO VA CORRETTA

Il mandato dice: *«l'inerzia è stata appena corretta di sei ordini. Se `coppia/inerzia` è cambiata
di scala, il confronto con un termine che NON è passato per l'inerzia è cambiato con lei»*.

**Non si applica qui.** Questa catena è il **settore della FASE** (`phivel`, diviso per `M_PH`); la
correzione dell'inerzia vive in **`_passo_spinoriale`**, nel **settore dello SPIN** (`omega_s`).
**Sono due catene separate**, e il feedback non passa per la seconda. La preoccupazione era
legittima e la risposta è: **nessun effetto di quella correzione su questo rapporto.**

**E `_cm` misura la coppia ACCUMULATA FIN LÌ**, non la totale: il twist di `:3154` viene dopo. In
questi run `TW_SPINORE` è **spento**, quindi non manca nulla — **ma il criterio è fragile**: se
qualcuno accendesse `TW_SPINORE`, `_cm` misurerebbe una coppia **parziale** senza che nulla lo
segnali. Va annotato nel codice.

---

## 2. ⚠ LA COSA CHE NON ERA FRA LE DOMANDE — **`F3` FALLISCE GIÀ ADESSO**

Ho anticipato il criterio `F3` del mandato (`sum(out) == 0`) dentro la sonda, per sapere se valesse
la pena scriverlo. **Non passa:**

```
|sum(out)| / max|out| :   mediana 1.112     MAX 8.441     su 64 invocazioni
                          (l'errore macchina sarebbe ~1e-14)
```

**Non è rumore numerico: è ORDINE UNITÀ.** La somma del "feedback" è dello stesso ordine del suo
valore massimo.

### La causa, dimostrata algebricamente e verificata sul numero esatto

```python
np.add.at(out, ii, -flusso / np.maximum(grado[ii], 1e-9))
np.add.at(out, jj,  flusso / np.maximum(grado[jj], 1e-9))
```

Per ogni arco `(a,b)` con flusso `f`: `out[a] -= f/g_a`, `out[b] += f/g_b`.
Contributo alla somma: **`f · (1/g_b − 1/g_a)`** — **zero solo se `g_a == g_b`**.

**I due denominatori sono DIVERSI. La divisione per il grado ROMPE l'antisimmetria che il nome
della funzione dichiara.**

Verifica su un caso minimo costruito a mano (stella: centro grado 3, tre foglie grado 1, `f = 1`):

| caso | `sum(out)` | atteso a mano |
|---|---|---|
| **B** — stella, gradi `[3,1,1,1]` | **2.000000** | `3·(1/1 − 1/3) =` **2.000000** ✓ |
| **C** — controprova, stesso grafo ma denominatore **simmetrico** sull'arco | **−2.22e-16** | antisimmetria **recuperata** |

*(Il caso A — grafo regolare — dà `sum = 0` ma anche `max|out| = 0`: è **degenere** e non prova
nulla. Lo dico perché l'avevo messo come controllo ed è inutile.)*

**Il caso C NON è una proposta di cura** — è la controprova che isola la causa. Cambiare il
denominatore è una **legge nuova** e non si fa qui.

### Perché questo conta più del 2.706

Il docstring dice: *«Trasforma l'overlap spinoriale locale in una **coppia antisimmetrica** ai
nodi»*, e *«La divisione per il grado pesato resta locale e **non introduce una manopola**»*.

**La seconda frase è vera. La prima è falsa, e la seconda è la ragione per cui la prima è falsa.**
La normalizzazione per grado — messa per non introdurre un parametro — **distrugge la proprietà che
dà senso al termine**.

> **Con `sum(out) ≠ 0` il termine inietta coppia NETTA nel sistema: è esattamente il «cricchetto»
> che A7 esclude.** E il segno dell'iniezione dipende dalla **disomogeneità dei gradi**, cioè da una
> proprietà della **topologia**, non della fisica dello spin.

**È il QUINTO membro della famiglia «un flag che non fa ciò che dichiara»**, dopo
`_passo_spinoriale` («ORFANO» ma vivo), `VERSO_CHI` (cablato ma muto), `spin_locale` (mai chiamata),
`TW_SPINORE` (un'unità di misura mancante). **Qui non è il commento a essere stale: è la
PROPRIETÀ dichiarata a non esserci.**

---

## 3. IL LIMITE DI QUESTA MISURA, e non lo nascondo

**La sonda NON riproduce il `2.706`.** Gira **in-process**, 60 passi, con i flag impostati
direttamente: le manca `--verlet`, `--calore-scal`, `--deparam-orologio`, e l'esperimento faceva
126 passi. A `TAU_A = 2.0` la sonda dà **media 2086**, mediana **1.83**.

**Non so attribuire per intero la differenza fra 2086 e 2.706**, e non la spiego con un'ipotesi.
**Quello che questa misura stabilisce è STRUTTURALE e non dipende dalla configurazione:**
1. la **popolazione non è stazionaria** → la media è lo statistico sbagliato, **comunque**;
2. il rapporto **scende sotto 1** a maturazione → *«tre volte la coppia»* non descrive il regime;
3. `sum(out) ≠ 0` → **l'antisimmetria non c'è**, e la causa è **algebrica**, quindi vale in ogni
   configurazione con gradi disomogenei.

**Il punto 3 non ha bisogno di nessuna delle due misure per reggere: si dimostra sulla riga.**

---

## 4. VERDETTO CONTRO LE TRE LETTURE FISSATE PRIMA

| lettura del mandato | esito |
|---|---|
| **è un artefatto di confronto (A3c)** → si corregge la MISURA | **SÌ, in parte** — non su popolazione/statistico/istante, che sono puliti, ma sulla **non-stazionarietà**. **Undicesimo caso A3c, ed è mio.** `E4b` va riscritto. |
| **è vero e viene dal FEEDBACK** → è un termine dominante, legge nuova | **NO.** `\|imag(ov)\|` è 0.035, `w/grado` è 0.0073, `\|feedback\|` è **sotto** il suo nullo stimato. |
| **è vero e viene da `coppia` PICCOLA** → il fatto è sulla coppia | **SÌ**, con precisazione: non *«la coppia è piccola»*, ma **«la coppia parte 6 ordini sotto il suo regime»**. A regime i due termini sono dello stesso ordine. |

**E una quarta cosa, che non era fra le letture perché nessuno l'aveva ancora misurata:
`F3` fallisce. Il termine non è antisimmetrico, e la causa è nella riga.**

---

## 5. COSA RACCOMANDO — **e la decisione è di Luca**

**Non propongo di curare niente.** Tre cose da decidere, in ordine:

1. **`E4b` è scaduto e va riscritto** — su una statistica che rispetti la non-stazionarietà
   (mediana + ultimi N passi, o il rapporto **a regime**), non sulla media. È l'**undicesimo A3c**
   e il **decimo-primo criterio scaduto**.
2. **`F3` ha già risposto prima di essere scritto, e ha risposto NO.** Il mandato diceva:
   *«Se non è zero, la premessa cade»*. **È zero? No.** Quindi — se si accetta quel criterio —
   **il sigillo di `SPIN_FEEDBACK` fallisce sul punto che ne definisce la forma**, e gli altri
   criteri (F1, F2, F4-F7) misurerebbero un termine di cui già sappiamo che **non è ciò che
   dichiara**.
3. **La domanda vera diventa un'altra:** se il termine deve essere antisimmetrico, **il divisore
   per grado va ripensato** — e quella è una **legge nuova**, par.10, non una riparazione.
   Se invece **non** deve esserlo, allora **il docstring va corretto** e il termine va descritto
   per quello che è: **una sorgente netta di coppia pilotata dalla disomogeneità dei gradi.**

**`SPIN_FEEDBACK` resta OFF. Nessuna promozione, nessun cablaggio, nessun cambio di default.**
**Mi fermo qui, come il mandato ordina.**
