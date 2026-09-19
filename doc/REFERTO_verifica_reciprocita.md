# REFERTO — **la verifica: un nodo che non pesa PUÒ essere scosso. E la coppia non è piccola**

**Blob `7c4dec1d`** · seme 42 · snapshot `_fin_B/scena_000192.pkl.gz` · **lettura del codice +
una misura sul nodo 2393**. **Nessuna modifica: il simulatore non è stato toccato.**

> **⚠ ORDINE REALE, dichiarato:** le tre letture del §1 **venivano dal mandato**, quindi erano
> fissate prima **per costruzione** — non le ho scritte io dopo aver guardato. **Ma la lettura del
> codice è avvenuta PRIMA che scrivessi un task history**, e lo dico invece di ricostruire un
> ordine che non c'è stato.

---

## 1. (a) LA COPPIA PASSA DAL PESO? — **UNO dei due termini sì, l'ALTRO no**

```python
:2424  correzione = np.cross(B, nb)                        # termine 1
:2426  if CAMPO_SPINORIALE:
:2431      correzione = correzione + np.cross(self._nb_grav(), nb)   # termine 2
```

### Termine 1 — `cross(B, nb)`: passa dai pesi, **ma è una MEDIA**

```python
:2252  contrib_j = nb_vic[jj] * wl[:, None]
:2256  np.add.at(B, ii, contrib_j * refl);  np.add.at(deg, ii, wl)
:2258  B = B / np.maximum(deg[:, None], 1e-9)
```

**`w` sta al numeratore E al denominatore**: `B` è una **media pesata di versori**, quindi
**l'ampiezza del peso si semplifica**. Per il neonato, però, i pesi sono **esattamente zero**,
quindi `deg = 0` e `B = 0 / 1e-9 = 0`: **il primo termine è NULLO.**

### Termine 2 — `cross(_nb_grav(), nb)`: **NON passa dai pesi, ed è un VERSORE**

```python
_nbn = [2Re(a*b), 2Im(a*b), |a|^2-|b|^2] / max(rho_spin, 1e-30)
```

**La norma di Bloch è `rho_spin` per identità, e viene divisa proprio per `rho_spin`.**

```
|_nb_grav| misurato:  p05 = 1.000000   p50 = 1.000000   p95 = 1.000000
```

> **È un versore ovunque: l'ampiezza del campo emesso NON entra.** Un nodo con
> `rho_spin = 5.7e-10` produce un `_nb_grav` di norma **1**, **identico a quello di un nodo
> maturo.**

## 2. (b) LA COPPIA È **NODALE** — e questo decide la forma della cura

`cross(B, nb)` e `cross(_nb_grav, nb)` sono **array `(n,3)` per NODO**, e il risultato entra in
`omega_new` che è **per nodo**. **Non c'è nessun indice d'arco nella coppia.**

> **Quindi il fattore giusto sarebbe `ramp[k]`, NON `ramp[i]*ramp[j]`.**

## 3. ⚠ LA TERZA LETTURA **CADE**: la coppia NON è piccola

**Il sospetto era:** *«`401 = coppia/1e-6` ⇒ coppia `≈ 4e-04`, minuscola: il problema è solo il
denominatore»*. **Misurato:**

```
nodo 2393 (neonato):   |cross(_nb_grav, nb)| = 0.380946
nodi MATURI (961, eta>mediana e deg>100):  p50 = 0.0776   p95 = 0.5968
RAPPORTO neonato / mediana matura:  x4.911
```

> **La coppia sul neonato è `0.38`: CINQUE VOLTE la mediana dei nodi maturi.** **Non è piccola, e
> non è proporzionata al peso.** **La terza lettura cade.**

**E il conto torna con l'osservato:**

```
coppia / inerzia = 0.3809 / 1e-6 = 3.81e+05
incremento in UN passo = dtn * (coppia/inerzia) ~ 0.0079 * 3.81e5 ~ 3009
omega misurato al passo 198: 401   (il rilassamento -omega/tau frena)
```

## 4. L'ASIMMETRIA, MISURATA

```
peso dei 2 archi del neonato:  [0. 0.]       ESATTAMENTE zero  (mediana globale 1.96e-04)
ramp del neonato: 0            ramp mediano: 0.0290

CONTRIBUISCE al campo:  NO   (peso esattamente zero -> A7b rispettata)
RICEVE coppia:          SI   0.3809, cioe' 4.9 volte un nodo maturo
```

> **`A7b` dice che un nodo appena nato NON PESA. NON dice cosa RICEVE.**
> **Il codice gli dà peso zero come sorgente e coppia PIENA come ricevente.**
> **La reciprocità è rotta, ed è misurata — non dedotta.**

**Scatta la SECONDA lettura: via libera al §2.**

## 5. ⚠ UN MIO ERRORE, e come si è denunciato da solo

La **prima** misura l'ho fatta importando il modulo con `sys.argv = ["x","--test","N-MASSE"]`,
cioè **senza applicare i flag del run**. Con `CAMPO_SPINORIALE = False`, `_nb_grav()` restituisce
`self._nb`, e `cross(nb, nb) = 0` **esattamente**.

**Risultato: coppia `0` su TUTTI i nodi, maturi compresi.** Un numero impossibile — **è così che
l'errore si è denunciato**. Rifatta col percorso ufficiale (`_cli` + `_applica_regime` +
`_applica_flag`), lo stesso del driver.

> **È la stessa famiglia del difetto già catalogato:** *«`--step2-orologio` è ON di default:
> l'assenza del flag non significa più OFF»*. **Un modulo importato senza `_applica_flag` NON è il
> sistema che gira.**

---

## 6. LA PROPOSTA PER IL §2.2 — **l'override del blob, e NON lo cablo senza via libera**

La modifica cambierà il blob, e **`carica_stato` rifiuterà lo snapshot 192**. Tre strade:

| # | strada | costo |
|---|---|---|
| **A** | **flag `--db-accetta-blob <sha>`** nel simulatore | tocca il simulatore, e resta nel codice |
| **B** | **override nello SCRIPT dell'esperimento**: si carica il `.pkl` a mano e si assegnano gli `attrs`, **saltando `carica_stato`** | non tocca il simulatore, **ma duplica la logica di caricamento** |
| **C** | **copia dello snapshot col blob RISCRITTO**, dichiarata e contata | non tocca nulla, **ma crea un file che mente sul proprio blob** |

> **PROPONGO `B`, con tre vincoli:** l'override vive **solo nello script dell'A/B**; **stampa una
> riga esplicita** *(«blob dello snapshot `X` ≠ blob corrente `Y`: override DICHIARATO per
> l'esperimento»)*; e **il confronto A/B non usa mai `carica_stato` per il ramo A**, così i due
> rami sono trattati allo stesso modo.
> **`C` la scarto**: un file che dichiara un blob che non è quello che l'ha prodotto è
> **esattamente** ciò che il presidio esiste per impedire.
> **`A` la scarto per ora**: indebolirebbe il presidio **in modo permanente**, e il mandato lo
> vieta.

**Non cablo niente finché non mi dici quale.**
