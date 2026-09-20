# TASK HISTORY — tre guardie silenziose: prima i contatori. E la provenienza era sbagliata

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `dc9d4a3` · **blob** `0a488348`
(**sha1 dei BYTE GREZZI**; il blob git dello stesso file è `775ceab7`) · albero **pulito** ·
**nessun processo in esecuzione**.

> **Nessun run finché non è sigillato. NIENTE NUMERI SCELTI. Una correzione, un sigillo.**
> **In questo giro NON si toccano:** `:2378` *(già misurata)*, `:3974`, le **19 di ESTENSIONE**,
> `scala_p` *(ha il suo mandato)*, `L_CONSERVA`.

---

## 1. ⚠ LA PROVENIENZA DEL MANDATO NON REGGE — **verificato dal disco, come ordinato**

**Il mandato dice: *«si curano SOLO i siti che vengono da `ca02af0` (13 settembre, il primo commit
del branch)»*. Due affermazioni, ed entrambe sono false.**

**① `ca02af0` NON è il primo commit.** Il primo è **`0ebaa4a`, 2026-08-28, «first commit»**.
`ca02af0` è del **2026-09-13** ed è *«PEZZO 2 (peso sin chi)»*.

**② NESSUNO dei siti viene da `ca02af0`.** Con `git log -S` *(che trova l'INTRODUZIONE della
stringa, non l'ultimo tocco come `git blame`)*:

| sito | introdotto da | data | messaggio |
|---|---|---|---|
| **`:2704`** `KERNEL_ALPHA` | **`670310f`** | 2026-08-28 | *«Implement code changes to enhance functionality and improve performance»* |
| **`:3865`** `TORS_4PI` | **`670310f`** | 2026-08-28 | *(lo stesso)* |
| **`:3678`** `ZETA_VIR` | **`53f885b`** | 2026-08-31 | *«TestAperti»* |
| **`:3715`** `ZETA_VIR` | **`7946c46`** | 2026-09-03 | *«Aggiungi integratore metrico Velocity-Verlet»* |
| **`:3182`** tempo-luce | **`94c2609`** | 2026-09-14 | *«PEZZO 4 / STRATO 1 … Sigillo 23/23 PASS»* |

> **Quattro commit diversi, dal 28 agosto al 14 settembre. Nessuno è `ca02af0`.**
> **⚠ E `git blame` avrebbe mentito:** dava `f7051c3` per `:3182` e `53f885b`/`7946c46` per le
> `ZETA_VIR` — **blame attribuisce l'ULTIMO tocco, non l'introduzione.** *(Per `:3182` la
> differenza è di un commit intero: `94c2609` contro `f7051c3`.)*

**⚠ MA LA SOSTANZA DEL CRITERIO DI LUCA REGGE, ed esce RAFFORZATA.** Il criterio vero è *«nessuna
ragione dichiarata nella storia»*, e **i messaggi dei commit d'origine lo confermano**:
*«Implement code changes to enhance functionality and improve performance»* e *«TestAperti»* **non
dichiarano nulla**; il terzo è il commit di Verlet, che **ha DUPLICATO la guardia** nel nuovo ramo
`beta_new` senza dirne la ragione.
> **Quindi i tre si curano lo stesso — ma per il motivo giusto, non per una provenienza che non
> hanno.**

**Una sola eccezione da dichiarare:** **`:3182` viene da un commit SIGILLATO 23/23**, quindi ha un
contesto dichiarato *(anche se non una ragione per la guardia)*. **È coerente col mandato, che per
`:3182` chiede solo il contatore.**

## 2. I SITI, verificati riga per riga dal disco

```python
:2704   _pesi    if KERNEL_ALPHA != 0.0 and len(self.tw) == len(self.d):
:3182   _tempo_luce_nodo   if len(ii) and len(dd) == len(ii):
:3678   step     if ZETA_VIR and self._sin2_vir is not None and len(self._sin2_vir) == len(beta):
:3715   step     if ZETA_VIR and self._sin2_vir is not None and len(self._sin2_vir) == len(beta_new):
:3865   mitosi   if TORS_4PI and len(self.i) == len(avv):
```

**Nessuno ha un `else`. Nessuno ha un contatore.** *(`:3182` ha il fallback esplicito e derivato
`d_nodo = np.full(n, LAM)`: gli manca solo il conteggio.)*

**⚠ E UNA PRECISAZIONE SUI FLAG, perché il mandato dice «tutti attivi»:**

```
KERNEL_ALPHA = 1.0      (:586, commento «SEMPRE ATTIVO»)      -> attivo per DEFAULT
TORS_4PI     = True     (:597)                                 -> attivo per DEFAULT
ZETA_VIR     = False    (:645)                                 -> attivo SOLO col flag --zeta-vir
```

> **`ZETA_VIR` è `False` di default.** È `True` **nel run** (`P6`: `"zeta_vir": true`), perché il
> driver passa `--zeta-vir`. **Entrambe le cose sono vere e vanno dette separate:** la guardia gira
> **in quella configurazione**, non sempre.

## 3. `:2378` — **NON si tocca: l'esito è già misurato, e lo si DICHIARA**

**Verificato nel messaggio di `4f2a6b7` (2026-09-17, indagine `Y5`), dal disco:**

```
PORTA A  (len(peq) != len(i))   :  0        MAI
«PORTA A NON SCATTA MAI: le lunghezze combaciano sempre. Nessun difetto di LUNGHEZZA, e A8b …»
```

**La lettura *«sembra strumentato e non lo è»* era sbagliata: è strumentato, è stato misurato, ed è
inerte.** **Va nel registro come esito dichiarato, col riferimento a `4f2a6b7`.**

## 4. IL PASSO 1 — **i contatori, e basta. Byte-inerti.**

**Il modello è già nel codice, `:3970-3973`, e si imita quello:**

```python
self._rep_guardia_tot   = getattr(self, "_rep_guardia_tot", 0) + 1     # le INVOCAZIONI
if len(self.d0) != len(avv):
    self._rep_guardia_salti = getattr(self, "_rep_guardia_salti", 0) + 1
    self._rep_guardia_shape = (len(self.d0), len(avv))                  # LA FORMA
```

**Per ciascuno dei quattro siti, col SUO nome** *(non un contatore globale: serve sapere QUALE
salta)*, e **con quattro numeri**:
1. **le invocazioni totali** — per la frazione;
2. **i salti**;
3. **la FORMA al fallimento** — le due lunghezze;
4. **QUANDO** — **l'indice dell'ULTIMA invocazione in cui è saltata**, perché `A8` dice che *non
   basta quante volte*: **un fallback confinato alle prime invocazioni è un transitorio, uno sparso
   è il comportamento principale, e i due casi danno lo STESSO conteggio.**

> **⚠ NEL PASSO 1 NON CAMBIA NIENTE: si conta e basta.** Nessuna guardia solleva, nessun `else`
> nuovo. **Far sollevare una guardia prima di sapere quante volte scatta romperebbe i run.**

## 5. I SIGILLI
- **V0** riferimento **`0a488348`** *(byte grezzi)*;
- **V1 — BYTE-IDENTITÀ, BLOCCANTE:** la sola contabilità **non deve cambiare un bit** di `psi`,
  `d`, `phi`, `eta`, `n`. **Se cambia, FERMATI;**
- **V2 — I CONTATORI SI LEGGONO** a fine run: per sito, col nome, la forma, e l'ultima invocazione;
- **V3 — E POSSONO SCATTARE: su CIASCUNO**, forzando una lunghezza sbagliata. **Senza questa prova
  ho aggiunto codice morto** *(par.10.2: un sigillo di sola byte-identità passa anche su codice
  morto)*;
- **V4** — dopo il PASSO 2: riduzione al limite, byte-identica al comportamento vecchio;
- **V5** — stabilità + **si rigirano tutti i sigilli del giro. Se uno si muove, è un reperto.**

## 6. COSA MI FA FERMARE
- **`V1` che non è byte-identico** → la contabilità sta toccando la fisica: **STOP**;
- **`V3` che non riesce a far scattare un contatore** → **quel contatore è codice morto**, e va
  detto invece di lasciarlo;
- **una guardia che salta spesso** → **è un difetto ATTIVO**: la causa si trova **a monte**, non si
  tappa.

## 7. TODO DEL NEXT STEP
1. [fatto] blob/branch, i cinque siti e **lo storico**, verificati dal disco;
2. **PASSO 1: i contatori**, committati prima, poi `V1` `V2` `V3`;
3. **riporto le frazioni e il QUANDO** → **STOP.**
