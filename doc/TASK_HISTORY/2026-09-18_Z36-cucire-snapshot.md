# TASK HISTORY — **`Z36`: cucire lo snapshot. E un'obiezione che viene PRIMA della cura**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `343fb40`
**Blob:** `f8f46683` (git) / `94b6cc29` (byte) · **Nessuna cura cablata finché §2 non è chiuso.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### ⚠ L'OBIEZIONE CHE VIENE PRIMA DI TUTTO: **il modello non trasferisce**

Il mandato dice: *«la forma è identica a quella che `_spinor_lift` usa già, misurata a `0.35 %`.
Non stai inventando una cura: stai applicando una che funziona, allo stesso tipo di oggetto.»*

**Ho letto la cucitura vera** (`:1180-1191`, **non** `:1146-1150` che è `_vertici_ciclo`), **e i due
oggetti NON sono lo stesso tipo:**

```python
# _spinor_lift  (:1180)
candidato = np.stack([cos(th/2), sin(th/2)*exp(i*ph)], axis=1)     # COSTRUITO da nb
...        candidato = candidato * fase                             # si ruota il NUOVO
# docstring :1170-1171: «cosi' l'overlap consecutivo e' reale positivo […] il Bloch resta la
#                        variabile fisica»
```

**Il lift è una PARAMETRIZZAZIONE del Bloch, definita a meno di una fase globale: quella fase è
GAUGE, e ruotarla non perde niente.** È esattamente perché `G6` ha dato `0.35 %`.

```python
# psi_spin  (:2693)
self.psi_spin = _Fs / (1.0 + GAMMA*_norm)[:, None]                 # CAMPO CALCOLATO
```

**`psi_spin` NON è un lift: è un campo con una fase DEFINITA, e quella fase è l'OROLOGIO.**
`f = Δangle(psi_spin[:,0])/DT` **è** il tasso di avanzamento della fase — **il segnale.**

### E il conto che mi preoccupa, scritto per esteso

La cura proposta è `_psp ← _psp · exp(−i·angle(overlap))`, poi
`a = angle(_ps[:,0]) − angle(_psp_ruotato[:,0])`. Ma:

```
angle(_psp_ruotato[:,0]) = angle(_psp[:,0]) + angle(overlap)
=>  a_curato = [angle(_ps[:,0]) − angle(_psp[:,0])]  −  angle(overlap)
             =            a_originale               −  angle(overlap)
```

**E se lo spinore ruota RIGIDAMENTE di una fase `φ`** — il caso che l'orologio deve misurare —
allora `angle(overlap) = φ` **e** `a_originale = φ`, quindi:

> **`a_curato = φ − φ = 0`. L'OROLOGIO SI FERMEREBBE ESATTAMENTE NEL CASO CHE DEVE MISURARE.**

**Questo non è un dubbio di stile: è un conto.** E se è giusto, la cura **non riduce il rumore: toglie
il segnale**, e il `64.7 %` scenderebbe **per la ragione sbagliata**.

**Non lo do per certo** — potrebbe essere che la rotazione rigida non sia il caso dominante, e che
`angle(overlap)` e `a_originale` differiscano abbastanza da lasciare segnale. **Ma va MISURATO prima
di cablare, non dopo**, e la misura è cheap: **calcolare `a_curato` senza cablarlo.**

### Il secondo candidato del mandato (§2) — **e lo trovo forte**

```python
a = angle(_ps[:, 0]) - angle(_psp[:, 0])      # SOLO la prima componente
```

`angle(z)` è mal definito per `|z| → 0`, e **uno spinore ruota fra le due componenti**: la prima
passa per zero regolarmente. **Potrebbe essere quello il `64.7 %`.**

**E se è quello, la diagnosi cambia anche se la cura restasse la stessa** — il referto deve dirlo
giusto, come il mandato stesso chiede.

### Cosa NON so

- **non so quale dei due domini** — è il §2;
- **non so se `a_curato` conservi il segnale** — è la mia obiezione, e **è la misura che decide se
  cablare**;
- **non so se esista una terza via** che tolga il rumore della componente **senza** toccare la fase
  globale. *(Un candidato: usare `angle` dell'**overlap** al posto della differenza delle
  componenti — ma **quello cambia la definizione di `f`**, ed è la via (b) che Luca ha scartato.)*

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO

**Passo A — `|psi_spin[:,0]|` è piccola?** Distribuzione, e **quale frazione di nodi** sta sotto
soglie crescenti (`1e-3`, `1e-6`, `1e-9`) **rispetto a `|psi_spin|` totale** *(il rapporto, non il
valore assoluto: A3c)*. *Decide:* se il candidato del mandato è plausibile.

**Passo B — i salti di `f` sono CORRELATI con `|psi_spin[:,0]|` piccola?** Correlazione fra
`|Δf|/|f|` per nodo e `|psi_spin[:,0]|/|psi_spin|`. *Decide:* **quale dei due candidati domina.**

**Passo C — `|<psi_prec|psi>|` quanto vale dove `f` salta?** Se è **vicino a 1**, gli stati erano
**vicini** e il salto è un artefatto della parametrizzazione. *Decide:* conferma indipendente di B.

**Passo D — ⚠ LA MIA OBIEZIONE: `a_curato` conserva il segnale?** Si calcola `a_curato` **senza
cablarlo** e si confrontano, sulla stessa popolazione e nello stesso istante (A3c):
- il **salto** `|Δa|/|a|` — deve **scendere** (è lo scopo);
- **e il LIVELLO `median|a|`** — **se crolla verso zero, la cura ha tolto il segnale, non il rumore.**

> **È la distinzione che decide, e nessuno dei due numeri da solo la fa: serve la coppia.**

**LE LETTURE, FISSATE ADESSO:**
- **il salto scende E il livello resta** → **la cura funziona: si cabla.**
- **il salto scende MA il livello crolla** → **la cura toglie il segnale. NON si cabla, e si riporta
  il conto di §1.** **È la lettura che mi aspetto, e spero di sbagliarmi.**
- **domina la componente che si annulla** → **la diagnosi cambia**: `Z36` non è deriva di gauge ma
  **parametrizzazione**, e la cura giusta potrebbe essere un'altra. **Il referto deve dirlo.**
- **il salto NON scende** → la cucitura non è il meccanismo: **reperto, e si ferma.**

**COSA MI FA FERMARE:**
- se `median|a_curato|` crolla → **si riporta e NON si cabla**, anche se `L1` passerebbe. **`L1` da
  solo sarebbe un falso PASS**, e va detto;
- se domina la componente → **si riporta prima di cablare**, come il mandato chiede.

**E una cosa che NON farò:** non cambio la definizione di `f`, non ruoto `psi_spin`, non tocco il
gauge.

---

## 3. TODO DEL NEXT STEP

- [ ] **A** — `|psi_spin[:,0]| / |psi_spin|`: distribuzione e frazioni sotto soglia
- [ ] **B** — i salti di `f` correlano con la componente piccola?
- [ ] **C** — `|<psi_prec|psi>|` dove `f` salta
- [ ] **D** — ⚠ `a_curato`: il salto scende **e il livello resta**? *(la coppia, non un numero solo)*
- [ ] **STOP e riporta** col verdetto contro le quattro letture
- [ ] *(solo se D è verde)* previsioni → cura → sigilli `L0-L10` → `Z9` rimisurata
- [ ] **⚠ NON toccare:** `psi_spin`, la definizione di `f`, `median(|f|)`, `max(...,1e-9)`, `+1e-6`
