# TASK HISTORY — **i tre cricchetti, misurati sui 45 snapshot**

**Data** 2026-09-19 · **branch** `fork-su2` · **HEAD** `acd9dc5` · **blob** `7c4dec1d` · albero
**pulito**. **Archivio:** `csv/_test_fork/_g6000`, **45 snapshot** dal passo 60 al 2700, cadenza 60,
**nessun buco** *(verificato dopo l'arresto)*.

> **NESSUN RUN NUOVO. NESSUNA CURA. Il simulatore non si tocca.**
> Il run è chiuso al passo 2700: **l'archivio è il dato.**

---

## 1. VERIFICHE DAL CODICE — **prima di misurare, e una cambia il mandato**

### 1.1 `chi_basc` — il meccanismo è RICOSTRUIBILE, e questo rende la misura ① forte

```python
:3527  if CHI_BASC and not CHI_DA_SPINORE and len(self.perc_chi) >= self.n and len(self.tw):
:3529      twabs = np.abs(_tw_src)
:3530      twn = np.zeros(self.n); np.add.at(twn, i, twabs); np.add.at(twn, j, twabs)
:3532      twn = twn / np.maximum(self._deg, 1)
:3533      soglia = PHI_CRIT                       # = 2*pi
:3534      self.perc_chi[:self.n] = np.where(twn > soglia, 1, -1)
```

**Tre fatti che ne discendono, tutti dal sorgente:**

1. **`perc_chi` è riscritto INTERAMENTE a ogni passo** — `[:self.n]`, non un sottoinsieme;
2. il criterio è la **media di `|tw|` sugli archi incidenti**, contro `PHI_CRIT = 2π`;
3. **è ricostruibile dagli snapshot**: `tw`, `i`, `j`, `_deg` ci sono tutti.

> **⚠ E LA SEPARAZIONE CHE IL MANDATO CHIEDE È GIÀ RISPOSTA DAL CODICE, non da una misura:**
> l'eredità della mitosi (`:1850`, `perc_chi = concatenate([perc_chi, chi_nuovi])`) **vive al
> massimo UN PASSO**, perché al passo successivo `chi_basc` riscrive **tutti** i nodi.
> **Quindi: l'antimateria può nascere, ma viene cancellata entro un passo.** Questo è un fatto di
> **struttura**; quello che la misura può aggiungere è **quando** e **quanto in fretta** la
> popolazione si ribalta.
> **La cadenza di 60 passi NON permette di contare i singoli eventi**, solo il netto fra due
> snapshot. Va dichiarato, non aggirato.

### 1.2 ⚠ `_tau` — **IL MANDATO NOMINA UN RAMO CHE IN QUESTO RUN NON GIRA**

Il mandato chiede: *«`_tau` effettivo: la sua mediana resta incollata a `TAU_A = 50`? Se sì, A3
morde qui»*, citando `_tau = TAU_A * max(dens/dens_rif, 0.05)`. **Dal codice:**

```python
:2438  if TAU_LUCE:
:2442      _tau = self._tempo_luce_nodo(i, j)[:, None]      <- QUESTO, nel run a 6000
:2443  elif TAU_A_LOCALE:
:2446      _tau = TAU_A * np.maximum(_dens / _dens_rif, 0.05)   <- il ramo del mandato
```

**`--tau-luce` è ATTIVO in questo run** *(`TAU_LUCE=1` nell'intestazione P6 del CSV)*, quindi
**`_tau = d/cs`, il tempo-luce — non `TAU_A * …`.** **La domanda «resta incollata a `TAU_A`?» non
si applica**, e misurare il ramo sbagliato darebbe un numero vero di una cosa che non gira.

> **Cosa misuro al suo posto, e lo dichiaro:** `_tau` **effettivo**, cioè
> `_tempo_luce_nodo(i, j)`, **chiamando il codice vero** su una `Rete` che ha ricaricato lo
> snapshot. **E il confronto con `TAU_A` resta interessante**, ma come *rapporto fra due scale
> diverse*, non come verifica del punto fisso di `A3`.

### 1.3 `lambda_nodi` — l'ipotesi ③ ha un pavimento, e si misura chiamando il codice

```python
portata_minima = LAM * 0.15          # LAM = 0.8  ->  PAVIMENTO = 0.12
return np.maximum(LAM * fattore, portata_minima)
:1959  rc = 3.0 * float(np.median(self.lambda_nodi()))    # in _allaccia
```

**Il pavimento è `0.12` e `rc` al pavimento vale `0.36`.** Con `d` mediano `1.325` al passo 2700,
**`rc/d ≈ 0.27`**. *(Numero di orientamento, non la misura: va fatto a ogni istante.)*

> **⚠ NON RICOSTRUISCO `lambda_nodi` FUORI DAL SIMULATORE.** È una catena **ricorsiva**
> (`lambda_nodi` → `massa_critica_adattiva` → `_pesi` → `lambda_nodi`, con una guardia di
> rientranza), ed è **esattamente l'errore già fatto su `correzione`** *(«chi ricostruisce la
> catena fuori dal simulatore e ne dimentica un pezzo calcola metà coppia»)*.
> **Si ricarica lo snapshot in una `Rete` e si chiama il metodo VERO.**

### 1.4 I contatori sono CUMULATIVI

`_inerzia_al_pavimento` e `_inerzia_tot` **contano dall'inizio del run**. Il `6.2 %` del mandato è
un **cumulato**. **Il tasso istantaneo è la DIFFERENZA fra snapshot consecutivi**, ed è quello che
dice se il sistema *sta* degenerando adesso o se porta il peso del passato.

---

## 2. LE LETTURE, FISSATE PRIMA

### ① `chi_basc`
- **`frac(perc_chi == +1)` a ogni snapshot.** *Ribaltamento NETTO* = passa da ~0 a ~1 in **pochi**
  snapshot; *transizione* = sale gradualmente su molti.
- **CONTROLLO DI CONSISTENZA:** `frac(twn > PHI_CRIT)` ricostruito **deve coincidere** con
  `frac(perc_chi == +1)`. **Se non coincide, ho ricostruito male e la misura non vale** — è la
  voce che impedisce di raccontare una storia su un `twn` sbagliato.
- **`twn / PHI_CRIT`** (percentili) nel tempo: **di quanto** si supera la soglia.
- **nodi che cambiano segno** fra snapshot consecutivi, sui **comuni** (primi `min(n1,n2)` indici).

### ② `omega_s`
- **percentili di `|omega_s|`** sui 45 snapshot.
  **MONOTONO ⇒ cricchetto (A7), e va detto. PLATEAU ⇒ non lo è.**
- **`_tau` effettivo** = `_tempo_luce_nodo(i, j)` dal codice vero, percentili, e il rapporto con
  `TAU_A` **dichiarato come rapporto fra scale diverse** (§1.2).

### ③ la portata
- **`median(lambda_nodi())` → `rc = 3·median`**, contro **`median(d)`**, a ogni istante.
- **grado: `p25`, `mediana`, `p75`** nel tempo.
- **L'IPOTESI REGGE** se `rc/d` scende sotto 1 **e** il grado si separa **nello stesso intervallo**.
  **CADE** altrimenti — **ed è un'ipotesi di Claude web, non un fatto: se cade, si scrive che cade.**

### ④ l'inerzia al pavimento
- **frazione per INTERVALLO** (differenze dei cumulati), non il cumulato.

---

## 3. I PRESIDI DI QUESTA MISURA

- **la memoria:** 45 snapshot × ~50 MB decompressi = **~2 GB**. **Non si tengono in RAM**: si
  legge uno alla volta e si trattengono solo i numeri. *(È il difetto che ho già trovato e corretto
  in `_misure_run6000.py` prima che facesse danno.)*
- **`_deg` è BIMODALE ESTREMA** al 2700 *(mediana 2, p75 501)*: **la mediana non descrive niente**,
  si riportano i percentili (A3c).
- **`--tau-luce` ha sigillo 6/7** *(`T3` è un risultato dichiarato)*: in testa al referto.
- **UN SEME, UNA SCENA.** Nessuna identificazione, nessun verdetto di fisica.
- **`Z9` NON si dichiara chiusa né risolta:** si **RIQUALIFICA** — *il kernel maturava
  (`ramp = 0.73`) e il sistema è degenerato mentre maturava*.

## 4. COSA MI FA FERMARE
- **il controllo di consistenza di ① che non torna** → ho ricostruito male `twn`: **STOP**, e si
  riporta senza raccontare il ribaltamento;
- **`carica_stato` che rifiuta uno snapshot** → il blob non è quello che credo: **STOP**;
- **un'ipotesi che cade** → **si scrive che cade**, non si cerca una misura sostitutiva.
