# TASK HISTORY — **la reciprocità: il neonato riceve quanto contribuisce**

**Data** 2026-09-19 · **branch** `fork-su2` · **HEAD** `c891d22` · **blob PRIMA della modifica**
`7c4dec1d` · albero **pulito**.

> **Via libera dal §1:** l'asimmetria è **misurata** — peso `[0. 0.]` esatto, coppia `0.3809` pari a
> **4.9×** la mediana dei maturi, `|_nb_grav| = 1.000000` ovunque. **La terza lettura è caduta.**

---

## 1. LA MODIFICA — **una riga, un fattore che già esiste**

### Dove, e perché SOLO lì

```python
:2424  correzione = np.cross(B, nb)                              # TERMINE 1: gia' ZERO
:2431  correzione = correzione + np.cross(self._nb_grav(), nb)   # TERMINE 2: <- QUI
```

**Il termine 1 non si tocca:** per il neonato `B = 0` **da solo**, perché `deg = Σw = 0` e
`B = 0/max(0, 1e-9)`. **È già reciproco.** **Il termine 2 è l'unico che non passa dai pesi.**

### La forma: **moltiplicazione, MAI un `if`**

```python
_ramp = np.minimum(1.0, self.eta[:n] / TAU_A)      # LA STESSA riga di _pesi() (:2649)
correzione = correzione + np.cross(self._nb_grav(), nb) * _ramp[:, None]
```

- **NESSUN numero nuovo:** `ramp` è **già** la legge del peso, e la riga è **identica** a quella
  di `_pesi()`. *(A1: se servisse un coefficiente, la legge sarebbe sbagliata.)*
- **NESSUNA soglia, NESSUNA discontinuità:** `ramp` cresce con `eta`, quindi il neonato **entra
  gradualmente** — come sorgente **e** come ricevente. **Non è escluso: è pesato.**
- **È `ramp[k]`, NODALE**, perché la coppia è nodale — **deciso dal codice nel §1(b)**, non scelto.

### Cosa NON si tocca
**il pavimento `1e-6`** *(se la coppia va a zero col peso, il pavimento smette di mordere DA SOLO)*
· **`A7b`** · **il peso zero alla nascita** · **il termine 1**.

## 2. ⚠ IL FLAG — e perché lo metto, anche se il mandato non lo chiede

**`COPPIA_RECIPROCA`, OFF di default, `--coppia-reciproca`.**

> **Il §1 di `CLAUDE.md` è esplicito: un interruttore alla volta, flag nuovi OFF, byte-identico a
> OFF.** Senza flag, l'A/B confronterebbe **due blob diversi** e la differenza sarebbe attribuibile
> al blob. **Col flag i due rami hanno lo STESSO blob e differiscono per UNA variabile.**

**E il flag dà gratis il sigillo di byte-identità:** **il ramo A (flag OFF, blob NUOVO) deve
riprodurre BYTE-IDENTICO lo snapshot 240 dell'archivio, prodotto dal blob VECCHIO.** Se lo fa, la
modifica **è inerte a flag spento** — **provato, non argomentato**.

## 3. L'OVERRIDE DEL BLOB — **strada B, decisa da Luca**

`carica_stato` rifiuterà lo snapshot 192 (blob diverso). **L'override vive SOLO nello script
dell'A/B**: si legge il `.pkl` e si assegnano gli `attrs` **senza passare da `carica_stato`**.

> **⚠ E I DUE RAMI LO USANO ALLO STESSO MODO.** È il pezzo che rende l'A/B valido: **se solo il
> ramo B saltasse `carica_stato`, la differenza potrebbe venire da lì.**
> **L'override STAMPA una riga esplicita** *(blob dello snapshot ≠ blob corrente, override
> DICHIARATO per questo esperimento)*, **non tocca il simulatore, e sparisce con lo script.**

## 4. L'A/B, variabile singola

```
ramo A:  snapshot 192 -> 240,  blob NUOVO, flag OFF     (deve riprodurre l'archivio)
ramo B:  snapshot 192 -> 240,  blob NUOVO, flag ON      (la cura)
stessa cadenza, stesso seme, stesso driver, stesso override
```

**Confronto:** `omega_s` *(percentili e max; il ramo A deve dare `0.31 → 401`)* ·
`_inerzia_al_pavimento` *(la frazione scende?)* · `r`, `d0`, `_fatt_cs_ultimo`, `_deg` · **e IL
NODO 2393**: `ramp`, grado, `psi`, `rho`, `omega` — **fa ancora `×1300`?**

## 5. LE LETTURE, FISSATE PRIMA

| # | esito | conclusione |
|---|---|---|
| **α** | il ramo A **non** riproduce lo snapshot 240 | **la modifica NON è inerte a flag OFF: STOP**, e non si guarda nemmeno il ramo B |
| **β** | ramo B: `omega_s` max **resta** dell'ordine di `10²`-`10³` | **la cura non morde**: l'asimmetria non era la causa |
| **γ** | ramo B: `omega_s` max **scende di ordini** e `_inerzia_al_pavimento` **cala** | **la cura morde**, e si riporta a Luca per la decisione del §3 |
| **δ** | `omega_s` scende **ma** compare un'altra degenerazione | **si riporta COSÌ**: una cura che sposta il problema non è una cura |

> **⚠ E NESSUN NUMERO DEL RAMO B ENTRA IN UN REFERTO COME RISULTATO DI FISICA.** È un
> **esperimento su metà run**, e il mandato lo vieta esplicitamente. **Serve a decidere se rifare
> il run da capo, non a misurare il sistema.**

## 6. COSA MI FA FERMARE
- **il ramo A che non riproduce** → lettura **α**: STOP;
- **il flag che non è byte-identico a OFF** → ho toccato la fisica dove non dovevo;
- **la tentazione di leggere il ramo B come misura** → non è una misura, è un test di una cura.
