# 2026-09-20 — **LA FUGA DI `|vd|` NEL RAMO B: struttura o divergenza?**

Mandato: diagnosi **dagli snapshot gia' scritti**, a run **VIVI**, senza fermarli e **senza analisi
pesanti**. Simulatore `edb8f844` (blob git `b44f50ce`), **non si tocca**. HEAD all'avvio `b60047c`.

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Cosa so gia' (dal mio referto `dcb210b`, non da una congettura)

```
|vd|.max  B:  2.923 -> 79.15 -> 531.6   ai passi 120/240/360     n3: 1 -> 9 -> 52
|vd|.max  A:  fra 2.62 e 4.03 per 1200 passi                     n3: 1 SEMPRE
p99 di |vd| in B: 1.176 -> 0.823 -> 0.493   (SCENDE mentre il max esplode)
```

### 1.2 ⚠ Un numero che ho GIA' in mano e che non ho ancora letto come rapporto

`79.15/2.923 = 27.1`, poi `531.6/79.15 = 6.7`. **Il rapporto fra snapshot consecutivi e' gia'
sceso da `27` a `6.7`.** **Sono DUE rapporti: non decidono nulla**, ma sono la ragione per cui il
criterio va fissato **adesso**, prima di vedere il terzo — altrimenti lo leggerei come mi conviene.

### 1.3 Cosa NON so, e lo dico prima

- **non so se gli archi veloci siano sempre gli stessi.** E' la misura che separa *collasso
  localizzato* da *contagio*, e non l'ho mai fatta;
- **non so se il ramo A sia stabile perche' sano o perche' MORTO.** A ha `N(+1) = 55` su `2672`, il
  **2 %**: monocoltura. **La stabilita' di A non e' automaticamente un punto a favore di `chi_basc`**,
  ed e' il rilievo del mandato che prendo piu' sul serio;
- **non so se `d` e `d0` di quegli archi si stiano accorciando**, e quindi se sia un collasso
  geometrico o una fuga di velocita' a geometria ferma.

### 1.4 Cosa mi aspetto (e NON si riscrive se sbagliato)

**Mi aspetto la ③ mista alla ①:** `chi_basc` spento toglie una saturazione, e cio' che emerge si
concentra in pochi archi. **Mi aspetto che gli archi veloci siano in buona parte GLI STESSI** e che
`d` si stia accorciando. **Se invece sono archi sempre diversi, la mia aspettativa cade** e la
lettura diventa contagio.

---

## 2. PROGETTAZIONE — **i criteri, fissati PRIMA dei numeri**

### 2.1 STRUTTURA contro DIVERGENZA — **il rapporto fra snapshot consecutivi**

`r_k = |vd|.max(t_{k+1}) / |vd|.max(t_k)`

```
r_k -> 1        (o comunque < 1.5 all'ultimo intervallo)   -> SI STABILIZZA  -> STRUTTURA
r_k resta > 3                                              -> CONTINUA A MOLTIPLICARSI -> DIVERGENZA
1.5 <= r_k <= 3                                            -> NON DECIDE: si dichiara indeciso
```
**Le soglie sono SCELTE e vanno dichiarate come tali** *(par.3: niente numeri scelti travestiti da
derivati)*. **Non sono derivate da un principio: sono un confine di lettura**, e la loro unica
virtu' e' di essere scritte **prima**.
**Il numero che conta davvero non e' la soglia: e' l'ANDAMENTO di `r_k`** — monotono in discesa,
piatto, o in risalita.

### 2.2 IDENTITA' degli archi veloci — **e qui il nullo si calcola, non si sceglie**

Si prendono i **primi `K` archi per `|vd|`** a due istanti e si misura la **sovrapposizione di
Jaccard**.

> **VALORE SOTTO IPOTESI NULLA:** se i due insiemi fossero indipendenti, su `M ~ 528 000` archi la
> sovrapposizione attesa e' `~K/M`. **Per `K = 100` vale `1.9e-4`.**
> **Quindi QUALUNQUE sovrapposizione apprezzabile e' un segnale**, e non serve una soglia inventata:
> `J > 0.5` = **gli stessi archi**; `J < 0.05` = **archi diversi**, cioe' **contagio**.

**⚠ E L'IDENTITA' DI UN ARCO NON E' IL SUO INDICE:** gli archi si aggiungono *(528031 -> 528158)*,
quindi **la posizione `k` negli array non e' stabile**. **Si identifica un arco con la COPPIA DI
NODI `(i[k], j[k])`**, ordinata, e **si dichiara l'assunzione**: vale finche' i nodi non vengono
rimossi, e **questo va verificato** confrontando il numero di nodi fra snapshot.

### 2.3 Il conteggio a PIU' soglie, per non dipendere dalla scelta
`#{|vd| > 1, 3, 10, 30, 100}` a ogni istante. **Piu' soglie = la forma della coda, non un numero.**

### 2.4 Costo — **il vincolo esplicito del mandato**

**Uno snapshot alla volta, e solo operazioni `numpy` su array per-arco.** Percentili e `argpartition`
su `528k` float sono millisecondi. **NIENTE scipy sul grafo, NIENTE `git log`.**
**Il costo reale e' l'I/O: ~36 MB compressi per snapshot.** Con ~13 snapshot in A e 3 in B sono
**~600 MB di lettura**, sequenziale, **una volta sola** — e i risultati si tengono in memoria invece
di rileggere.
> **Se un conto si rivelasse costoso, il mandato dice di DIRLO invece di girarlo.**

### 2.5 Cosa mi FERMA
- **il numero di nodi che CALA fra due snapshot** -> l'identita' `(i,j)` non regge, e la misura
  `2.2` va rifatta o dichiarata non valida;
- **un run che smette di avanzare** -> `py-spy` **prima di ogni altra cosa**, e **non si uccide**.

---

## 3. TODO
1. [ ] **§2① la serie nel tempo** su TUTTI gli snapshot dei due rami -> **riportare SUBITO**
2. [ ] §2② identita' (Jaccard) + conteggio a piu' soglie
3. [ ] §2③ dove stanno: `d`, `d0`, `perc_chi`, e se i nodi sono dentro una massa o nel vuoto
4. [ ] §2④ la controprova su A — **«la coda non esiste affatto» e' diverso da «e' piu' bassa»**
5. [ ] §3 la voce `nsub` nel registro, **senza cablare** (il simulatore e' in uso)
6. [ ] CHECKPOINT, e sorveglianza dei run
