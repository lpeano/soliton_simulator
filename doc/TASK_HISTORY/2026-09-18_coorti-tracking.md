# TASK HISTORY — **le coorti: un pezzo su due esiste già, e il secondo va fatto DOPO il run**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `2808d8d`
**Blob:** `a1ae5090` · **NESSUN CODICE TOCCATO IN QUESTO GIRO** *(vedi §1.4)*

---

## 1. RAGIONAMENTO PRELIMINARE — *la verifica del §5.2, prima di scrivere codice*

### 1.1 ⚠ IL §1① NON SERVE: **l'ereditarietà alla mitosi È GIÀ CABLATA**

Il mandato dice *«alla mitosi il figlio nasce SENZA appartenenza: `:1858` estende con liste VUOTE»*.
**Dal disco, `:3951-3954`:**

```python
# TRACKING: i figli della mitosi ereditano la concorrenza del genitore a (nascono dalla sua
# divisione, concorrono alle stesse masse). conc_archi viene riallineato sotto (keep+nuovi).
if self.conc_nodi:
    for kk in a:
        eredita = [v[:] for v in self.conc_nodi[kk]] if kk < len(self.conc_nodi) else []
        self.conc_nodi.append(eredita)
```

**Il figlio eredita una COPIA PROFONDA delle voci del genitore `a`.** **E la scelta di `a` è già
fatta E MOTIVATA nel commento** — che è esattamente la domanda che il §1① pone.

**E non è l'unico punto:**
- **`:4076-4082`** — **il ramo Schwinger fa lo stesso** *(eredita dal genitore `gk`)*;
- **`:3997-4001`** — **`conc_archi` è RIALLINEATO**: gli archi mantenuti conservano la concorrenza,
  i nuovi ricevono `[]`.

> **`:1858` — l'`extend` con liste vuote che il mandato cita — è in `semina()`, NON in `mitosi()`.**
> **Ed è corretto lì: un nodo appena SEMINATO non ha lignaggio finché
> `_registra_concorrenza` non glielo assegna.**
> **La coorte NON si perde alla prima mitosi. Il §1① è già fatto.**

### 1.2 ✅ IL §2 È SODDISFATTO: **nessuna legge fisica legge `conc_nodi`**

**Enumerati dal disco tutti i lettori, e i loro chiamanti:**

| chi legge | chiamato da | è fisica? |
|---|---|---|
| `indici_massa_vivi` (`:1651`) | `_picchi_nuovi` (`:7180`) | **no — diagnostica** |
| `aggiorna_pesi_concorrenza` (`:1910`) | `batch_condensazione` (`:6305`), `_diag_completa` (`:6504`), `_classifica_tracking` (`:7039`) | **no — scena e diagnostica** |
| `tracking_masse` (`:1937`) | `_classifica_tracking` (`:7049`) | **no** |
| `_registra_concorrenza` (`:1876`) | `semina`/`nuova_massa` | scrittura, alla creazione |
| `_ripara_tracking` (`:1900`) | manutenzione dimensione | — |

> **Nessun metodo chiamato dentro `step()` / `mitosi()` / `scuoti_vuoto()` tocca `conc_nodi`.**
> **È una struttura di MISURA pura, e il vincolo del §2 regge.**

### 1.3 ✅ E PERCHÉ NON FINISCE NEL `.pkl` — **una riga, e la modifica è quella**

```python
:2865   if isinstance(v, (np.ndarray, int, float, bool, np.integer, np.floating, str)):
:2866       stato['attrs'][k] = v
```

**`conc_nodi` è una `list`: non matcha nessuno di quei tipi, e viene SCARTATA in silenzio.**
**Insieme a `conc_archi` e a `masse_info` (un `dict`).**
**È l'unico pezzo vero da fare, ed è il §1②.**

### 1.4 ⚠ E UN VINCOLO PRATICO CHE IMPONE DI ASPETTARE — due ragioni, non una

**Il run a DUE masse è ATTIVO** *(frame ~80/400, ~1h15 alla fine)*.

1. **`S5` misura il TEMPO PER PASSO.** **Misurarlo mentre un altro run satura la CPU darebbe un
   numero sbagliato**, e il §2 chiede esplicitamente di **misurare il costo** prima di cablare.
2. **`par.5-quinquies`:** il run è partito dal blob **`a1ae5090`**. **Modificare
   `soliton_simulator.py` adesso farebbe divergere il file su disco dal blob che quel run cita**, e
   la regola esiste apposta perché non accada.

> **Quindi: la verifica si riporta ADESSO** *(è il §5.2 del mandato, e non richiede di scrivere
> codice)*, **e la modifica si fa QUANDO IL RUN CHIUDE.** **Non è una rinuncia: è l'ordine giusto.**

### 1.5 Cosa resta da decidere, e le due domande del §1① **decadono entrambe**

- **da quale genitore?** → **già deciso nel codice: `a`, col perché scritto.** Non tocco.
- **il peso: ereditato o ricalcolato?** → **ereditato** (`v[:]` copia la voce intera), **e
  `aggiorna_pesi_concorrenza` lo RICALCOLA dopo** (`:1927-1935`: `voce[2] = w` corrente).
  **Quindi il sistema fa già entrambe le cose, nell'ordine giusto: eredita la STORIA e aggiorna il
  CONTRIBUTO.** **Non c'è niente da scegliere.**

**Cosa NON so:** **quanto costi** `conc_nodi` nel `.pkl` con `n = 8000` e mitosi attiva. **È il §2, e
va misurato, non stimato.**

---

## 2. PROGETTAZIONE — *quando il run chiude*

**La modifica è UNA:** far entrare `conc_nodi`, `conc_archi` e `masse_info` nello snapshot.
**Forma minima:** aggiungerli **esplicitamente** dopo il ciclo su `__dict__`, **senza toccare il
filtro** *(cambiare il filtro farebbe entrare anche altro, e non so cosa)*.

**I SIGILLI, e `S1` è il decisivo:**
`S0` blob byte grezzi · **`S1` BYTE-IDENTITÀ della fisica su un run breve (`psi`, `d`, `phi`, `eta`,
`n`)** · `S2` frazione di nodi con `conc_nodi` non vuoto dopo `k` mitosi · `S3` round-trip
salva→ricarica identico e `len == n` · `S4` quante volte scatta `_ripara_tracking` · **`S5` costo:
dimensione `.pkl` e tempo/passo, PRIMA e DOPO, a CPU libera** · `S6` rigiro dei sigilli del giro.

**LE LETTURE, FISSATE ADESSO:**
- **`S1` non byte-identico** → **la modifica è sbagliata: si ferma e si riporta;**
- **`S5` costo che esplode** → **si propone la forma compatta invece di cablare;**
- **`S4` che scatta spesso** → **la dimensione non è mantenuta dove dovrebbe: è un difetto, non la
  cura;**
- **`S2` già ~100 % prima della modifica** → **conferma il §1.1: l'ereditarietà c'era già, e lo si
  scrive.**

---

## 3. TODO DEL NEXT STEP

- [x] **§5.2 verificato e riportato PRIMA di scrivere codice**
- [x] attendere la chiusura del run a due masse *(par.5-quinquies + `S5` a CPU libera)*
- [x] **§1②** la persistenza + **`S0-S6`** → **9/9 PASS**
- [x] referto + registro + relazione **nello stesso commit** *(`Z53`, `doc/REFERTO_coorti_snapshot.md`, §9.67)*
- [x] **⚠ NON toccato:** nessuna legge, `TAU_A`, `ramp`, `Z9`, **né il filtro di `salva_stato`**

### ⚠ ESITO — **le quattro letture fissate in §2, e come sono andate**

| lettura fissata | esito |
|---|---|
| **`S1` non byte-identico → la modifica è sbagliata: si ferma** | **NON è scattata: `0.000e+00` su 9 campi su 9, shape uguali** |
| **`S5` costo che esplode → si propone la forma compatta** | **NON è scattata: `+25.6 %` sul `.pkl` a `n = 454`** |
| **`S4` che scatta spesso → è un difetto, non la cura** | **NON è scattata: `0` chiamate in entrambi i bracci** |
| **`S2` già ~100 % prima della modifica → l'ereditarietà c'era già, e lo si scrive** | **✓ È SCATTATA — ma vale `0.8238`, non `~100 %`, e il numero si riporta com'è** |

**⚠ E una previsione mia che NON avevo scritto, quindi non conta come previsione ma come rilievo:**
**le previsioni qualitative NON sono state committate per questo giro.** Era un punto del TODO
*(«previsioni qualitative → commit»)*, **e l'ho saltato.** Le quattro letture di §2 facevano già il
lavoro — sono criteri con una soglia, scritti prima e committati in `695ced0` — **ma il punto era
nella lista e non l'ho spuntato: lo dichiaro invece di cancellarlo dalla lista.**

### ⚠ IL FAIL INTERMEDIO, e perché sta qui

**Il primo giro ha dato `8/9`, e il FAIL era `S6` — cioè IL MIO CRITERIO, non il codice.** Committato
com'era in `a872383` **prima** di correggerlo (par.5: *«se il sigillo FALLISCE, committa comunque lo
stato + il fallimento e FERMATI: non aggiustare al volo dentro lo stesso commit»*).
**Il criterio cercava `"FAIL"` e lo trovava nel testo esplicativo di una riga che PASSA.**
**È il quarto caso in questo repo della famiglia par.9** *(`N3b`, `M1b`/`M3`, `M3c`)*.

### TODO — il passo successivo

- [ ] **il costo a `n = 8000`**: `S5` misura `n = 454`. **Non estrapolato, e va misurato prima di
      rigirare una scena lunga con le coorti dentro.**
- [ ] **i contatori DURANTE il run** per separare «coorte assegnata dalla MITOSI» da «riscritta da
      `chi_basc`» — **non è ricavabile dai `.pkl` neanche adesso** *(limite già dichiarato in `Z49`)*
- [ ] **≥ 4 semi per braccio** se `Z52` deve diventare un fatto e non un rapporto senza barra
