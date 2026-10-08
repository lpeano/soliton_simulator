# `D1` e `D2` — **LA POTENZA DELLA COPPIA, e una coppia che LEGGE la fase** *(2026-10-08, mandato di Luca)*

> ### ⛔ **SOLO DIAGNOSI. Nessun file del simulatore si tocca** — resta ### **`b8c21049`** — e
> `doc/ASSIOMI.md` non si tocca. ### **Gli interventi stanno nello strumento e sono
> dichiarati.**

> ### 📌 **Committato e pushato PRIMA degli strumenti e PRIMA delle corse.**

---

## 0. ⛔ **LA VERIFICA SUL CODICE — e CORREGGE il guardiano su un punto**

Il mandato chiede: *«la coppia del ramo del driver dipende da `self.phi` oppure no? Segui il
percorso REALE delle chiamate, non i commenti né il docstring.»* ### **Fatto, con un
censimento `AST` più la lettura delle righe.**

### I FLAG A RUNTIME *(sondati, non assunti)*

`CAMPO_SPINORIALE = True`, `FORK_SU2 = True`, ### **`DEPARAM_OROLOGIO = True`**,
`SPINORE_CORRETTO = True`, `K_C = 2.0`.

### ✔ **`(a)` LA DIPENDENZA DIRETTA: il guardiano ha RAGIONE**

`_coppia_interferenza` *(`:7434`)*, nel ramo del driver, ritorna

```
K_C * Im[ conj(_a)*(_c00 + _c01) + conj(_b)*(_c10 + _c11) ]        (:7479-:7480)
```

### **Il censimento `AST` della funzione trova ZERO letture di `phi`, `phi0`, `phivel`.**
### ⭐ **E `z` — l'argomento che porta `e^{iφ}` — è PASSATO MA NON USATO in quel ramo:**
compare solo nel `return` finale *(`:7484`)*, quello scalare.
### **Dipende da `_psi_spinor` *(`_a`, `_b`)*, da `A` e da `N`.** ✔

### ⛔ **`(b)` MA LA DIPENDENZA INDIRETTA ESISTE, e «`φ` non entra mai in `ψ`» è TROPPO FORTE**

`_passo_spinoriale` *(`:5432`)* ### **legge `self.phi`** — e il censimento lo trova. La riga è

```
_cij = np.cos(self.phi[_ii] - self.phi[_jj])                        (:5986)
omega_clk = _num / max(_den, 1e-12)      # la COERENZA D'ARCO, in [-1, 1]
```

e con ### **`DEPARAM_OROLOGIO = True`** quell'`omega_clk` è applicato come
### **FASE GLOBALE `e^{−i·omega_clk·dt/2}`** sullo spinore *(il commento `:6000`-`:6001` lo
dice, e il codice lo conferma)*, che poi viene committato in ### **`self._psi_spinor`**
*(`:6111`)*.

### ➜ **QUINDI `φ` ENTRA IN `ψ`, ma SOLO come FASE COMUNE `α`** — ### **non tocca la direzione
di Bloch** *(«PURA FASE: l'orologio NON entra nell'asse di rotazione»)*.

> ### ⭐ **LA FORMULAZIONE CORRETTA, che sostituisce «`φ` non entra mai in `ψ`»:**
>
> | | |
> |---|---|
> | direttamente | ### **la coppia NON legge `φ`** ✔ |
> | tramite la direzione di Bloch | ### **NO**: `omega_clk` è pura fase |
> | tramite la ### **fase comune `α`** | ### ⛔ **SÌ**, con `α` che accumula `∫omega_clk·dt` e `omega_clk = media_w(cos(φ_i − φ_j))` |
> | il ritardo | ### **UN passo:** la coppia legge lo ### **SNAPSHOT** `_psi_spinor` di inizio passo, che `_passo_spinoriale` aggiorna ### **DOPO** *(causalità Jacobi, dichiarata nel docstring)* |

### ⛔ **E IL CUORE DEL MECCANISMO SOPRAVVIVE ALLA CORREZIONE, per tre ragioni che si
leggono dal codice:**

1. ### **`A = w·cos(φ0_i − φ0_j)` usa `φ0`, la fase INIZIALE CONGELATA** *(`PHI0-CONGELATA`)*,
   non `φ`;
2. la dipendenza da `φ` è su una ### **STORIA INTEGRATA** *(`α = ∫omega_clk dt`)*, non sul `φ`
   istantaneo, e ### **ritardata di un passo**;
3. ### **`omega_clk` è una coerenza d'arco MEDIATA SUL NODO**, cioè una grandezza
   ### **scalare per nodo**, non il gradiente di un'energia rispetto a `φ_k`.

> ### ➜ **Quindi `∂(coppia_k)/∂φ_k` NON è zero, ma la coppia NON è `−∂E/∂φ` di nessuna
> energia** — ed è ### **questa** la proprietà che permette di pompare, non lo zero esatto.
> ### ⚠ **Lo scrivo come correzione, non come conferma: il guardiano diceva «no» in assoluto,
> e in assoluto non regge.**

---

## 1. ⭐ **`D1` È IN GRAN PARTE GIÀ MISURATO, e lo dico PRIMA di girare**

### **La relazione fra il bilancio di `H3` e `P_coppia` è algebrica, non approssimata:**

```
Delta_coppia_k   = dt_n_k * coppia_k / M_PH                 (dalla decomposizione di H3)
voce "coppia"    = media_classe( 2 * p1_k * Delta_coppia_k )
                 = (2/M_PH) * media_classe( dt_n_k * coppia_k * p1_k )
```

### ➜ **Con `dt_n > 0` il SEGNO della voce `coppia` del bilancio È il segno di
`Σ coppia_k·p1_k`**, cioè di ### **`P_coppia`**.

### ✔ **E sui dati di `H3` già committati** *(`h3_base.json`, `d90a547`)*, nei passi `1..230`:

| classe | passi con la voce `coppia` ### **positiva** | somma |
|---|--:|--:|
| ### **MASSE** | ### **`230 / 230` = `100.0 %`** | ### **`+5.6186`** |
| VUOTO | `229 / 230` = `99.6 %` *(l'unico negativo è il passo `1`, `−0.0012`)* | `+0.6035` |

### ⛔ **Il criterio di `D1` — «positiva in almeno l'`80 %` dei passi `1..230` E somma
positiva» — È GIÀ SODDISFATTO CON LARGO MARGINE.**

### ⭐ **ALLORA A CHE SERVE LA CORSA?** A tre cose che i dati di `H3` ### **non** hanno:

1. ### **`P_coppia` nella sua UNITÀ** *(un lavoro per unità di tempo proprio)*, non come
   contributo a `Δ<phivel²>`;
2. ### **le potenze del TERMOSTATO e dello SCUOTIMENTO**, per confrontarle con quella della
   coppia ### **nella stessa unità**;
3. ### ⭐ **un CONTROLLO POSITIVO dell'identità qui sopra:** lo strumento calcola
   ### **entrambi** i membri e verifica che coincidano. ### ⛔ **Se non coincidessero, la mia
   ri-espressione sarebbe sbagliata e lo saprei.**

### LE TRE POTENZE, e la terza è un ANALOGO DICHIARATO

| | definizione | |
|---|---|---|
| ### **`P_coppia`** | `Σ_k coppia_k · p1_k` | ### **forza × velocità: è la potenza vera** |
| ### **`P_termo`** | `Σ_k (−xi·p1_k) · p1_k = −xi·Σ p1²` | stessa forma: un attrito |
| ### ⚠ **`P_scuoti`** | `Σ_k p0_k · Δscuoti_k / dt_n_k` | ### ⛔ **ANALOGO DICHIARATO:** lo scuotimento è un ### **calcio additivo**, non una forza. È il lavoro per unità di tempo proprio, e si scrive così invece di fingere che sia una potenza |

---

## 2. ⭐ **`D2` — COME FORZO IL RAMO SCALARE, E PERCHÉ COSÌ**

### ⛔ **NON riscrivo la formula.** `_coppia_interferenza` sceglie il ramo con
`if CAMPO_SPINORIALE:` *(`:7444`)*, e il ramo scalare è ### **l'ultimo `return` della funzione
stessa.**

### ✔ **L'INTERVENTO: un involucro che spegne `CAMPO_SPINORIALE` SOLO DURANTE LA CHIAMATA**

```
def _inv(A, z, _o=originale):
    vecchio = S.CAMPO_SPINORIALE
    S.CAMPO_SPINORIALE = False
    try:    return _o(A, z)
    finally: S.CAMPO_SPINORIALE = vecchio
```

### ⭐ **Così gira il ramo scalare DEL SIMULATORE, non una mia copia** *(`9-ter`: nessuna
seconda formula)*, e il flag è ### **ripristinato prima che qualunque altra legge lo legga.**

### ⛔ **E LA VERIFICA CHE IL MANDATO CHIEDE — «con una misura, non a parole»**

| | come si misura |
|---|---|
| `(1)` ### **`_coppia_interferenza` è PURA** *(non scrive niente)* | si avvolge la chiamata in ### **`sola_lettura`** e si pretende ### **`toccati == []`**. ### **Se è pura, spegnere un flag intorno a lei NON PUÒ toccare nient'altro che il valore restituito** |
| `(2)` il flag è ### **sempre ripristinato** | un ### **contatore**: `installazioni`, `chiamate`, `ripristini` — e ### **`chiamate == ripristini`**, altrimenti FERMO |
| `(3)` il resto del passo spinoriale ### **non cambia** | `_psi_spinor`, `_nb`, `omega_s`, `phi_s` ### **firmati prima e dopo la chiamata** con la `_firma` del presidio: ### **devono coincidere** |

### ⚠ **E UNA COSA DA DICHIARARE NEL REFERTO** *(il mandato la impone, e ha ragione)*: il ramo
scalare usa ### **`cos(φ_k − φ_j)`**, ### **non `cos((φ_k − φ_j)/2)`** come nella direzione
candidata di Luca. ### ⛔ **È un test sul PRINCIPIO** *(una coppia che dipende dalla fase che
muove)*, ### **NON sulla forma finale. Un esito positivo NON decide la cura.**

---

## 3. ⛔ **I CRITERI, FISSATI ADESSO** *(mandato di Luca)*

### `D1`

| esito | condizione |
|---|---|
| ### **`LA COPPIA POMPA`** | `P_coppia` nelle masse ### **positiva in almeno l'`80 %`** dei passi `1..230` ### **E** la sua ### **somma** su quei passi positiva |
| ### **`NON POMPA`** | quella somma è ### **`<= 0`** |
| fra i due | ### **la curva** |

### `D2`

| esito | condizione |
|---|---|
| ### **`UNA COPPIA CHE LEGGE LA FASE TIENE LE MASSE`** | AUC al `400` ### **`>= 0.85`** ### **E** l'energia totale al `500` ### **minore** che nel controllo |
| ### **`NON BASTA`** | AUC al `400` ### **`< 0.6`** |
| fra i due | la curva, e ### **il confronto al passo `230` col controllo** *(`B-TS` crollava già lì: `0.1638` contro `0.9023`)* |

### ⛔ **IL CONTROLLO È QUELLO DI `A-S1`** *(`55a7edc`)*: ### **non si rigira.**

---

## 4. ⭐ **LE PREVISIONI, PRIMA DELLE CORSE**

| | la previsione | il perché |
|---|---|---|
| ### **`PD-1`** | ### ⛔ **`LA COPPIA POMPA`**, e con margine larghissimo: ### **`100 %`** dei passi e somma ### **positiva** | ### **è già nei dati di `H3`**, e la corsa lo conferma nell'unità giusta. ### ⚠ **Non la conto come una previsione difficile: la dichiaro GIÀ NOTA** |
| ### **`PD-2`** | `P_coppia` nelle masse sarà ### **dello stesso ordine** di `P_scuoti` nelle masse, e ### **molto più piccola** di `P_scuoti` nel vuoto | nel bilancio di `H3`, masse: `coppia +5.619` contro `scuoti +9.705`; vuoto: `coppia +0.604` contro `scuoti ~+11.5` |
| ### **`PD-3`** | ### **`P_termo` cambierà SEGNO** attorno al passo `49` | misurato in `H3`: aggiunge su `48` passi, toglie su `252` |
| ### **`PD-4`** | ### ⚠ **`D2` darà `NON BASTA`: AUC al `400` `< 0.6`** | ### **il ramo scalare cambia la COPPIA, non la scena**: le masse partono comunque con velocità di fase casuali *(`H1`, già misurato insufficiente)*, e `A` resta ### **`w·cos(φ0_i − φ0_j)` con `φ0` CONGELATA.** ### **Una coppia che legge `φ` ma pesa con una memoria morta non basta** |
| ### **`PD-5`** | ### ⭐ **ma l'energia totale in `D2` sarà MINORE che nel controllo** | se la coppia diventa `−∂E/∂φ` di qualcosa, smette di pompare liberamente. ### **Se `PD-4` e `PD-5` fossero entrambe vere, l'esito è «fra i due» e la curva è il risultato** |

> ### ⭐ **E SE `PD-4` SI SBAGLIASSE — se l'AUC al `400` fosse `>= 0.85` — sarebbe il
> risultato più importante:** vorrebbe dire che ### **far dipendere la coppia dalla fase che
> muove, DA SOLO, salva le masse.** ### ⛔ **E non deciderebbe comunque la cura**, perché la
> forma non è quella candidata da Luca.

---

## 5. ⭐ **LA STELLA POLARE** *(`L-STELLA`)*

| | |
|---|---|
| `A14` | ### **NON SI APPLICA:** nessun termine di nessuna legge è aggiunto, tolto o cambiato nel simulatore. ### ⚠ **`D2` fa girare un ramo CHE C'È GIÀ**, scegliendolo dall'esterno |
| `ROBUSTEZZA-FISICA` | ### **NON SI APPLICA.** ### ⚠ **Il gradino di robustezza della MISURA è dichiarato:** il ramo scalare ha una forma `2π`, non `4π` |
| numeri o leggi aggiunti | ### **ZERO** |
| verso EM-curvatura | ### **NON SI APPLICA** |
| ### **emergente o imposto** | ### ⛔ **IMPOSTO e dichiarato:** `D2` è un ### **test di principio**, non un modello. ### **La cura è decisione di Luca, e non si comincia** |

---

## 6. TODO

- [ ] **(a)** questo task history, ### **committato PRIMA**;
- [ ] **(b)** le tre potenze e il braccio `B-SCAL` in `csv/_test_fork/_termo_h3.py`, col
      collaudo e col caso che ### **DEVE fallire** *(una coppia finta scritta come `−∂E/∂φ` di
      un'energia nota deve ### **chiudere il bilancio**, e lo strumento deve accorgersi se non
      chiude)*;
- [ ] **(c)** la ### **BYTE-INERZIA dell'osservatore `TermoH3`** su una finestra ### **oltre
      il `216`**, perché l'osservatore avvolge ### **`step` stesso** — ed è il wrapper più
      invasivo finora;
- [ ] **(d)** `D1` *(`300` passi)* e `D2` *(`500` passi)*, in background;
- [ ] **(e)** ### **UN SOLO referto** per `D1` e `D2`, coi numeri ### **generati dai json**;
- [ ] **(f)** `SPINORE-SENZA-FASE` aggiornata col verdetto, e ### **collegata ad `A14`, `A7` e
      `ENERGIA-NON-DEFINITA` se il pompaggio è confermato**;
- [ ] **(g)** poi ### **FERMO. La cura è una DECISIONE DI LUCA: non si comincia.**
