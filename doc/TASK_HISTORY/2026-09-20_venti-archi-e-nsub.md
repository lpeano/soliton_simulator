# 2026-09-20 — **I VENTI ARCHI PEGGIORI, e `nsub` letto DAL VIVO**

Mandato: diagnosi da **snapshot** e **stack**, run **VIVI e non toccati**, **niente analisi pesanti**.
Simulatore `edb8f844` (blob git `b44f50ce`), **non si tocca**. HEAD all'avvio `967fd6c`.

> **⚠ ORDINE DICHIARATO, e non e' quello del rito.** La **PARTE ①** (`py-spy --locals`) e' stata
> eseguita **PRIMA** di scrivere questo file, perche' il mandato la ordina per prima *(«riporta
> `nsub` SUBITO: costa secondi»)* **e perche' non ha letture da fissare**: e' la lettura di una
> variabile, non un confronto che si possa leggere come conviene.
> **Le parti ② e ③ SI', e i loro criteri sono fissati qui sotto, prima dei numeri.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Cio' che la PARTE ① ha gia' stabilito (non piu' un'ipotesi)

```
ramo A   n1=1  n2=1  n3=1    -> nsub =   4     (il PAVIMENTO di max(4, ...))
ramo B   n1=1  n2=3  n3=206  -> nsub = 206     n3 VINCE DA SOLO
```
**`n3` e' il vincolo su `|vd|`.** `n1` *(sorgente)* e `n2` *(`beta`)* sono **inerti**: valgono `1` e
`3`. **Quindi la fuga e' governata da `|vd|` e da nient'altro**, e non c'e' piu' bisogno di dedurlo.

**E `n3` era `52` allo snapshot del passo 360: adesso e' `206`. E' quadruplicato da allora.**

**Una differenza QUALITATIVA, non solo di numero:** in A **6 campioni su 8 cadono FUORI** dal blocco
CFL *(`_pesi`, `chiralita_core_locale`, `_passo_spinoriale`)*; in B **tutti** i campioni cadono
**dentro** il ciclo dei sottopassi.

### 1.2 Il sospetto di Luca, e cosa lo renderebbe vero o falso

> *«Il `p99` SCENDE mentre il massimo esplode. In un collasso fisico la coda INTERA si alza: qui il
> resto RALLENTA — cioe' l'energia non viene da nessuna parte: APPARE.»*

**E' l'argomento piu' forte del mandato, e non l'avevo formulato cosi'.** Il mio referto aveva
misurato il `p99` che scende, ma l'aveva letto come *«il grosso gela»*; **la lettura di Luca e' piu'
stringente: un sistema conservativo non fa accelerare pochi rallentando tutti gli altri SENZA un
canale che trasferisca.**

### 1.3 Cosa NON so

- **non so da dove venga `vd`, e non lo deduco: il mandato dice di LEGGERLO.** Se nella sua catena
  c'e' una divisione per una grandezza che puo' andare a zero *(come `inerzia` nel caso del passo
  198, `rho = 5.7e-10` mille volte sotto il pavimento)*, quello e' l'innesco;
- **non so se gli archi peggiori siano gli STESSI a tre istanti.** Al `par.2.2` del giro precedente
  il Jaccard sui primi **100** dava `0.04` in B — **ma dava lo stesso in A**, quindi **non
  discriminava**. **Sui primi VENTI potrebbe discriminare, o potrebbe non farlo: e' da misurare;**
- **non so se i nati abbiano davvero grado ~2.** Il conto `n x2.4 / archi +0.9 %` lo **suggerisce
  fortissimo**, ma e' un'aritmetica su totali, **non una distribuzione misurata**.

### 1.4 Cosa mi aspetto (**non si riscrive se sbagliato**)

- mi aspetto che i venti archi peggiori condividano **pochi nodi**, cioe' un **nucleo**;
- mi aspetto che gli indici **NON coincidano del tutto** e che la lettura giusta sia quella che il
  mandato prevede: **un nucleo fisso che RECLUTA**;
- mi aspetto che `_deg` dei nati sia **basso ma non 2**: `2` era il valore del run a `sep = 8`, e
  questa scena e' **connessa**.

---

## 2. PROGETTAZIONE — i criteri, **fissati prima dei numeri**

### 2.1 PARTE ②③ — l'identita' dei venti peggiori, e il NULLO si calcola

Si confrontano gli insiemi dei **20 archi peggiori** *(identificati per **coppia di nodi ordinata**,
non per indice: gli archi si aggiungono, l'indice non e' stabile — verificato al giro precedente)*
ai passi **240, 360** e a ogni snapshot successivo disponibile.

> **NULLO:** due insiemi indipendenti di `20` su `~528 000` archi si sovrappongono con
> **`20/528000 = 3.8e-05`**. **Quindi qualunque intersezione non nulla e' segnale**, e la domanda
> non e' *«c'e' sovrapposizione?»* ma *«quanta?*».

```
intersezione >= 15/20   -> NUCLEO FISSO: instabilita' numerica su archi determinati
intersezione <= 3/20    -> RICAMBIO: la fuga si SPOSTA, e la diagnosi e' un'altra
in mezzo                -> NUCLEO CHE RECLUTA -- si DICHIARA, non si forza
```
**Le tre fasce sono SCELTE e lo dichiaro** (par.3). **E la terza NON e' un ripiego: e' la lettura
che il mandato stesso prevede**, e con `n3` che va `1 -> 9 -> 52 -> 206` **e' quella che mi aspetto**.

**⚠ E IL CONTROLLO CHE RENDE LEGGIBILE IL NUMERO: la stessa misura sul ramo A.** Al giro precedente
il Jaccard sui primi 100 sembrava dire «contagio» in B, finche' **A non ha mostrato lo stesso
ricambio**. **Senza il controllo, l'intersezione dei venti non si puo' leggere.**

### 2.2 PARTE ②② — la catena di `vd`, **letta dal codice e non dedotta**

Si cerca **dove `vd` viene scritto** e si **legge la formula**, dichiarando:
- se contiene una **divisione** per una grandezza che puo' avvicinarsi a zero;
- **quale pavimento** la protegge, e **se quel pavimento e' attivo** su quei nodi.

**Cio' che si riporta dei venti archi:** `d`, `d0`, `psi`, `omega_s`, `_deg`, `perc_chi`, `eta`, e
la densita'/inerzia **se e solo se ricostruibile dallo snapshot** — *e se non lo e', si dice che non
lo e' invece di stimarla.*

### 2.3 PARTE ③ — il grado dei nati, e **come si distinguono dai nati**

**Il criterio di separazione dev'essere dichiarato**, perche' lo snapshot non ha un campo
«originale/nato». **Due candidati, e si usa quello verificabile:**
- **per INDICE**: i nodi `< 2391` *(l'`n` alla semina, misurato)* sono gli originali — **i nodi si
  APPENDONO, quindi l'indice e' un'eta' di nascita**, ed e' verificabile confrontando `n` fra
  snapshot;
- per `eta`: **piu' fragile**, perche' `eta` e' un tempo proprio che cresce e non un contatore.

**Si usa l'INDICE, e si dichiara l'assunzione** *(i nodi non vengono rimossi — gia' verificato al
giro precedente: `n` non cala mai)*.

### 2.4 Costo — **il vincolo esplicito**
**Uno snapshot alla volta, solo `numpy` per-arco/per-nodo.** Niente scipy sul grafo, niente `git log`.
**Gli snapshot da leggere sono pochi e mirati**: B ai passi `240`/`360` (+ i nuovi se ci sono), A a
due istanti. **Se servisse rileggere tutto A, lo dico invece di farlo.**

### 2.5 Cosa mi FERMA
- **`n` che cala fra due snapshot** -> cade l'identita' per coppia **e** il criterio per indice;
- **un run che smette di avanzare** -> `py-spy` **prima di tutto**, e **non si uccide**;
- **disco sotto 3 GB** -> si riporta **subito** (oggi: `13 GB`).

---

## 3. TODO
1. [x] **PARTE ①** `py-spy --locals` -> **`nsub`: A `4`, B `206`; `n3` vince da solo**
2. [ ] PARTE ②① e ②② — le venti righe di B + **la formula di `vd` letta dal codice**
3. [ ] **PARTE ②③ i tre istanti — l'intersezione dei venti: e' la misura che decide**
4. [ ] PARTE ②④ la controprova su A
5. [ ] PARTE ③ il grado dei nati, su A e B, a due istanti -> **voce nel registro**
6. [ ] **`Z73` aggiornata IN LOCO: `chi_basc` NON blocca la mitosi** *(A: `2672 -> 6481` con
       `chi_basc` ACCESO)* — **il ritiro dell'A/B corto, la SECONDA volta e dai fatti del run lungo**
7. [ ] CHECKPOINT
