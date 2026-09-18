# TASK HISTORY — **`Z33`: il gauge degenere. Cosa collassa, quando, e cosa succede a `r`**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `e342ae8`
**Blob:** `72acd6aa` (git) / `aa84755b` (byte) · **Nessuna cura in questo giro.**
**Task:** le tre misure del §2, per decidere se `Z33` sia un difetto vero o un transitorio.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### Cosa ho già in mano, dal giro precedente

`median(|f|) = 0` **esatto** in **4 invocazioni su 126 (3.2 %)** sul ramo 4π. E nel campione che
avevo stampato, le degeneri avevano **`median = p05 = p95 = max = 0`**: non «metà a zero», ma
**`f` IDENTICAMENTE NULLO**.

**Questo è già un'informazione che il mandato non ha:** la 2.1 offre tre alternative, e **la terza
(*«mediana nulla con valori non nulli»*) sembra esclusa dai dati che ho già.** Ma **il campione era
di 5 invocazioni su 126**, quindi **va verificato su tutte**, non dedotto.

### ⚠ E ho trovato una causa candidata leggendo `step()`, prima di misurare

```
:3093   r = self.ritmo()
:3099   self._psi_prec = self.psi.copy()
:3101   self._psi_spin_prec = self.psi_spin.copy()      # lo SNAPSHOT si aggiorna DOPO
```

E dentro `ritmo()` (`:2039`): `a = angle(psi_spin[:,0]) − angle(_psi_spin_prec[:,0])`.

> **Se `ritmo()` viene chiamata di nuovo PRIMA che `psi_spin` cambi, `a = 0` per OGNI nodo, quindi
> `f` è identicamente nullo.** Non è una degenerazione fisica: è **un confronto di uno snapshot con
> sé stesso.**

**Candidati per una seconda chiamata:** i due diagnostici a `:6232` e `:6890` (`tau = net.ritmo()`),
oppure `stato_crossover`. **Se le degeneri vengono da lì, `eta` non le vede mai** — perché solo la
chiamata a `:3093` alimenta `dt_n` — **e `Z33` non sarebbe un difetto della fisica ma un artefatto
della mia sonda, che conta tutte le chiamate.**

**Ma c'è un dato che gioca contro questa ipotesi:** **126 invocazioni per 126 passi**, cioè **una
per passo**. Se ci fossero chiamate diagnostiche in più, ne conterei di più. **Quindi probabilmente
sono tutte da `step()`, e allora il difetto è nel percorso fisico.**

**Non risolvo questa tensione a tavolino: è la prima cosa che misuro.**

### Una seconda causa candidata, indipendente

`:3100` aggiorna lo snapshot **solo se `len(psi_spin) == self.n`**. **La mitosi fa crescere `n`**:
se `psi_spin` ha ancora la lunghezza vecchia, **lo snapshot NON si aggiorna**. È la stessa famiglia
di `C11` (`_psi_spin_prec` non esteso alla mitosi, inerte nel 95.33 % per mesi) e di `C7` (la cache
`_cs_nodo_prev` scartata a ogni mitosi). **È il candidato che il mandato suggerisce con «coincidono
con le mitosi?», e ha un precedente preciso nel repo.**

### Il sospetto del §1 del mandato, e perché credo sia **parzialmente** sbagliato

> *«`med = 1e-9` → `x` enorme → `r → ±1` per tutti → la dilatazione sparisce»*

**Se `f` è identicamente nullo, `x = 0/1e-9 = 0` per tutti, quindi `r = 0 + 1e-6`, e il ritorno è
`1 + (1e-6/r_unit − 1) ≈ 1.414e-06` — NON `±1`.** **Il collasso è verso il BASSO, non verso l'alto.**

**L'effetto però è lo stesso e forse peggiore:** `dt_n = DT · 1.414e-06`, cioè **il tempo si ferma
per tutti** in quel passo. **La dilatazione sparisce lo stesso** — ma per la ragione opposta a
quella del mandato. **Va misurato, non assunto**, e se ho ragione va detto che il mandato aveva il
segno sbagliato.

*(Il caso `x → ∞` esiste ed è il duale: si verifica quando `median(|f|) = 0` **ma qualche `f` non è
zero**. Allora quelli esplodono e saturano a `√2`. **Sono due regimi diversi, e la 2.1 serve
esattamente a distinguerli.**)*

### Cosa NON so

- **non so da quale chiamante vengano le degeneri** — è la prima misura;
- **non so se coincidano con le mitosi** — è la 2.2;
- **non so se `eta` le veda davvero.** **Se non le vede, `Z33` non è un difetto di `Z9`**, e tutto
  il §4 del mandato cade.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi ferma*

**Passo A — IL CHIAMANTE.** Per ogni invocazione: `sys._getframe(1).f_code.co_name`, l'indice del
passo, e se è **dentro `step()`**. *Decide:* se `Z33` è nel percorso fisico o è un artefatto della
sonda. **È la domanda che viene prima di tutte le altre**, e se la risposta è «diagnostico» il giro
finisce lì.

**Passo B (2.1) — COSA collassa.** Per ogni invocazione degenere: **`f` è identicamente nullo**,
oppure **≥ metà esattamente zero con altri non nulli**, oppure **`median(|f|)` è piccola ma non
zero**? **Tre casi, tre cure.** E la distribuzione di `|f|` lì: `median`, `p05`, `p95`, **frazione a
zero esatto**, `n`.

**Passo C (2.2) — QUANDO.** Posizione degli eventi nel run, e **coincidenza con le mitosi**
(nodi nati in quel passo). *Decide:* transitorio contro regime — **la distinzione che decide se vale
la pena curare.**

**Passo D (2.3) — COSA SUCCEDE a `r` e a `dt_n`.** Distribuzione di `r` nei passi degeneri contro i
sani: **mediana, dispersione, frazione vicino a `±1` E frazione vicino a `1.4e-06`** *(entrambe le
code, perché il mandato ne prevede una sola e io sospetto l'altra)*. E **`std(dt_n)`**: se collassa,
la dilatazione è sparita.

**LE LETTURE, FISSATE ADESSO** *(le quattro del mandato, più una che aggiungo)*:
- **transitorio, `r` non degenera** → non è un difetto: **si chiude `Z33`**;
- **transitorio, `r → ±1` (o `→ 1.4e-06`)** → difetto **confinato**, cura opzionale;
- **a regime, con `r` degenere** → **difetto GRAVE**, si cura e `Z9` va rimisurata dopo;
- **`f` ha mediana nulla per costruzione** (metà esatta a zero) → **A3 in forma nuova: una mediana
  che vale zero non normalizza, SELEZIONA.** Reperto grosso;
- **⊕ le degeneri NON sono nel percorso fisico** *(chiamate diagnostiche, o `eta` non le vede)* →
  **`Z33` non è un difetto di `Z9`**, e **il §4 del mandato cade**. **Va detto, ed è un esito
  valido.**

**COSA MI FA FERMARE:**
- se il passo A dice «diagnostico» → **si riporta quello e si chiude**, senza fare B, C, D come se
  fossero fisica;
- se `f` è identicamente nullo **e** la causa è lo snapshot non aggiornato → **è un difetto di
  ORDINE, non di gauge**, e la cura non c'entra con la mediana. **Cambierebbe tutto il quadro.**

**E una cosa che NON farò:** **non cablo niente**, e **non tocco il gauge**: il §3 del mandato dice
che qualunque sostituzione è una decisione di Luca, e il mio stesso verdetto di ieri (A4) lo impone.

---

## 3. TODO DEL NEXT STEP

- [x] **A** — il CHIAMANTE delle invocazioni degeneri *(la domanda che viene prima di tutte)*
- [x] **B (2.1)** — cosa collassa: `f` tutto nullo / metà zero / mediana piccola
- [x] **C (2.2)** — quando: transitorio o regime, e coincidenza con le mitosi
- [x] **D (2.3)** — `r` e `std(dt_n)` nei degeneri contro i sani, **entrambe le code**
- [x] **STOP e riporta** col verdetto contro le **cinque** letture
- [ ] **⚠ NON toccare:** il gauge, il `+1e-6`, `ramp`, `TAU_A`. **Nessuna cura.**
- [x] ~~*(dopo)* `Z9` rimisurata~~ — **NON SERVE**: impatto <= ~2 %, calcolato — **ma solo se `Z33` risulta nel percorso fisico**

---

## 4. ESITO — *cosa il ragionamento preliminare aveva preso, e cosa no*

**PRESO, ed erano le tre cose che contavano:**

1. **la causa (1)** — lo snapshot confrontato con sé stesso — trovata **leggendo `step()` prima di
   misurare**: confermata **3 su 4**;
2. **la causa (2)** — le lunghezze disallineate dopo una crescita di `n` — confermata **sul passo 6**
   (`440/80`), ed è il **terzo membro** della famiglia `C11`/`C7`;
3. **il segno del collasso.** Avevo scritto che il sospetto del mandato era *«probabilmente
   sbagliato»*, perché con `f` identicamente nullo `x = 0` e non `∞`. **Misurato: `fraz r>1.4 =
   0.0000`, `fraz r<1e-5 = 0.49`.** **Il mandato aveva il segno sbagliato, e averlo scritto prima è
   ciò che rende la correzione credibile.**

**E la quinta lettura che avevo aggiunto ha funzionato a metà, nella metà giusta:** la prima parte
(*«è un artefatto della sonda»*) è **falsa** — tutte le chiamate vengono da `step()`. La seconda
(*«se `f` è identicamente nullo la causa è l'ORDINE, non il gauge, e cambierebbe tutto il quadro»*)
è **esatta**, ed è il risultato del giro.

**NON PRESO:** **non avevo previsto che i quattro eventi si dividessero in DUE regimi opposti** —
`r = 1.0` (ramo di sicurezza) e `r = 1.4e-06` (`f` nullo). Avevo pensato a un solo modo di
degenerare. **Sono due, con cause diverse, e uno dei due è il ramo di sicurezza che fa il suo
mestiere.**

## 5. TODO DEL PROSSIMO PASSO

- [ ] **decisione di Luca:** `Z33` è **transitorio e confinato**, la cura è **opzionale** e **non
      tocca il gauge**. Curare o registrare e chiudere?
- [ ] se si cura: **è la cura di `C7`/`C11`** (estendere lo snapshot con la popolazione) **più una
      guardia A8** che dichiari `psi_spin == _psi_spin_prec`. **Nessuna delle due è una decisione di
      gauge.**
- [ ] **`Z9` NON va rimisurata**: impatto ≤ ~2 %, calcolato, dentro il rumore già misurato
- [ ] **⚠ NON toccare:** il gauge, il `+1e-6`, `ramp`, `TAU_A`
