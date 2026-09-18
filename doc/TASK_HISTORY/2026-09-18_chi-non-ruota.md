# TASK HISTORY — **chi non ruota, e perché.** Cinque misure, nessuna cura

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `5422126`
**Blob:** `a1ae5090` — **e non cambierà: solo strumentazione byte-inerte, nessuna cura.**

---

## 1. RAGIONAMENTO PRELIMINARE — *verificato dal disco prima di accettare il §1*

### 1.1 ⚠ PRIMO — **le convenzioni di `perc_chi` sono TRE, non due, e la terza è quella che domina**

Il mandato ne cita due. **Dal disco ce n'è una terza, ed è la principale in questa scena:**

```python
:1835   chi_nuovi = self.rng.choice([-1, 1], n)                       # NASCITA: ~50/50 A CASO
:1850   self.perc_chi = np.concatenate([self.perc_chi, chi_nuovi])
:3945   self.perc_chi = np.concatenate([self.perc_chi,  self.perc_chi[a]])    # mitosi: UGUALE
:4066   self.perc_chi = np.concatenate([self.perc_chi, -self.perc_chi[aa]])   # Schwinger: OPPOSTO
```

**E questo CAMBIA l'indizio del §5b.** Il mandato dice: *«una delle due mitosi eredita l'opposto —
quindi le due popolazioni potrebbero essere bilanciate a metà»*.
**Il bilanciamento NON viene da lì: viene da `rng.choice([-1,1])` alla nascita.** La mitosi
`:3945` **conserva** il segno, quindi **propaga** il 50/50 iniziale invece di generarlo.

> **La coincidenza numerica resta** *(due popolazioni ~50/50, e «metà non ruota»)* **ma il
> meccanismo che il mandato le attribuisce non è quello. Va detto prima di misurare, non dopo.**

### 1.2 ⚠ SECONDO — **DUE flag possono RISCRIVERE `perc_chi` in blocco, e sono OFF**

```python
:3486   self.perc_chi[:n] = np.where(twn > soglia, 1, -1)     # CHI_BASC   = False  (:669)
:3496   self.perc_chi[:n] = np.where(real(_ov) >= 0, 1, -1)   # CHI_DA_SPINORE = False (:739)
```

**Sono spenti di default, quindi in questa scena `perc_chi` è un'ETICHETTA DI LIGNAGGIO**, fissata
alla nascita e propagata. **Va verificato che restino spenti nel run, non assunto** (P2/A8).

### 1.3 ⚠ TERZO — **«metà dei nodi» non è il caso che ho misurato**

Il §0 dice *«in quei passi metà dei nodi ha `f = 0`»*, da `median(|f|) = 0`. **Ma i contatori del
blob curato dicono che sono DUE REGIMI DIVERSI**, e uno non è «metà»:

```
_ritmo_f_tutto_nullo      1     <- TUTTI i nodi, non meta'
_ritmo_med_sul_pavimento  2
_ritmo_med_non_promosso   2
_ritmo_sicurezza          2     <- non esiste un prima (avvio + iniezione)
_ritmo_med_assente        2
```

**`f` TUTTO nullo e `f` MEDIANO nullo sono cose diverse e hanno cause diverse.**
**Il «4 su 126» del mandato è il conteggio di `Z33` sul blob VECCHIO, e sommava quattro contatori
distinti.** **Misurerò la frazione VERA di nodi con `f = 0`, passo per passo — che è quello che il
§4 stesso chiede.**

### 1.4 Cosa mi aspetto, e cosa NON so

**Mi aspetto che ③ sia la spiegazione:** `psi_spin` nasce dal campo `_Fs/(1+GAMMA·norm)`, e i nodi
appena iniettati da `nuova_massa` **non hanno ancora peso**. `angle(0) = 0` per convenzione numpy,
quindi `f = 0` **senza che nulla sia fermo**. **E ④ la spiegherebbe a monte** (`ramp ≈ 0` ⟹ pesi a
zero ⟹ `psi ≈ 0`).

**⚠ E su ⑤b sono SCETTICO, e lo dichiaro prima:** `perc_chi` è fissato **alla nascita per sorteggio**
e non entra in `psi_spin` *(che è costruito da `_Fs`, non da `perc_chi`)*. **Perché `f` dipenda dal
segno servirebbe un canale, e i due che esistono — `OROLOGIO_SEGNO` e `TEMPO_SEGNO` — vanno
verificati come spenti.** **Se `⑤b` dicesse SÌ con quei flag spenti, sarebbe un reperto enorme
proprio perché non c'è un meccanismo noto: e allora andrebbe cercato, non celebrato.**

**Cosa NON so:** se il ramo Schwinger `:4066` **giri mai** in questa scena. **Va contato, non
dedotto** (il mandato lo chiede, ed è giusto).

---

## 2. PROGETTAZIONE

**Una sola sonda, nell'ordine del mandato** *(⑤a è la più economica e cambia il contesto)*.

**⑤a** — distribuzione di `perc_chi` nel tempo (`+1` / `−1` / frazione), **e i CONTATORI dei tre
rami** (`semina`/`nuova_massa`, mitosi `:3945`, Schwinger `:4066`), **più lo stato dei flag che
potrebbero riscriverlo**.

**⑤b** — `perc_chi` dei nodi con `f = 0`: **frazione `+1`**, contro **la frazione `+1` della
popolazione nello stesso istante** (A3c: stessa popolazione, stesso istante). **Il valore sotto
ipotesi nulla è la frazione della popolazione, NON `0.5`.**

**③** — `|psi_spin[:,0]|` e `|psi_spin|` dei nodi fermi contro tutti.

**④** — `ramp = min(1, eta/TAU_A)` ed `eta` dei nodi fermi contro tutti.

**②** — `|psi_spin(t) − psi_spin(t−1)|` per i nodi fermi: lo stato evolve mentre `f = 0`?

**①** — identità: gli indici si ripetono fra passi? **Frazione di sovrapposizione.**

**LE LETTURE, FISSATE ADESSO** *(sono quelle del §2 del mandato, più una mia)*:
- **⑤b SÌ** *(tutti lo stesso segno, contro un nullo che NON è 0.5 ma la frazione della
  popolazione)* → **si riporta e ci si FERMA;**
- **④ regge** → `Z33`/`Z43` **sintomi di `Z9`**;
- **③ `|psi| ≈ 0`** → **`f = 0` è convenzione di numpy, non fisica;**
- **② evolve ma `angle` non lo vede** → **difetto dell'OSSERVABILE;**
- **① sempre gli stessi** → **congelamento;**
- **nessuna regge** → **lo dico, e NON invento la sesta.**

**⚠ E UNA LETTURA MIA, che il mandato non ha:** ③ e ④ **possono reggere ENTRAMBE senza contraddirsi**
— sarebbero **lo stesso fatto a due livelli** (`ramp ≈ 0` ⟹ `psi ≈ 0` ⟹ `angle` indefinita).
**Se reggono entrambe NON è un conflitto, ed è l'esito che mi aspetto.** Il referto deve saperlo
dire, altrimenti sembrerà che due spiegazioni competano.

**COSA MI FA FERMARE:** ⑤b positivo. **E in ogni caso: NESSUNA CURA, nessun cablaggio, nessun cambio
di default.**

---

## 3. TODO DEL NEXT STEP

- [ ] **⑤a** — `perc_chi` nel tempo + i contatori dei tre rami + lo stato dei flag
- [ ] **⑤b** — `perc_chi` dei nodi fermi contro il nullo VERO (la frazione della popolazione)
- [ ] **③** — `|psi_spin|` dei nodi fermi
- [ ] **④** — `ramp`/`eta` dei nodi fermi *(il collegamento con `Z9`)*
- [ ] **②** — lo stato evolve mentre `f = 0`?
- [ ] **①** — sono sempre gli stessi?
- [ ] **verdetto contro le sei letture**, **senza curare**
- [ ] registro *(voci nuove + `Z43` qualificata come DECISIONE SULLA DEFINIZIONE DEL TEMPO)* +
      relazione + **CHECKPOINT**
- [ ] **⚠ NON toccare:** il gauge, il `+1e-6`, il `max(...,1e-9)`, la regolarizzazione appena cablata
