# FISICA — **`perc_geom` e `perc_chi`: due grandezze, due lavori**

> **La legge, la derivazione e il perché** (par.5-novies ③). Il registro dice *«questo era rotto»*;
> questo documento dice *«questa è la legge»*, e le due cose non si sostituiscono.
> Flag: **`--chi-coop`**, **OFF di default**, byte-inerte a default. Simulatore **`54623593`**.

---

## 1. IL PROBLEMA — **una sola grandezza portava due significati** (`A10` al contrario)

`perc_chi` è nato come *«verso di percorrenza / antichiralità (+1/-1)»* e ha finito per portare
**due cose diverse**:

| significato | chi lo scrive | chi lo legge |
|---|---|---|
| **GEOMETRIA** — *il giro è compiuto o no* | `chi_basc`, dalla torsione locale contro `PHI_CRIT` | la catena `CHI_CORE` (chiralità di core, `FRAME_DRAG`, `TORS_4PI`) |
| **CARICA** — *materia o antimateria* | la nascita (semina / mitosi / Schwinger), e il segno di doppia copertura di `_psi_spinor` | il campo `B` del passo spinoriale, il Bloch ribaltato, `TEMPO_SEGNO`, `OROLOGIO_SEGNO` |

> **`A10` dice che UNA grandezza può legare due domini. Non dice che debba portarne due
> SIGNIFICATI.** Qui non c'era un legame: c'era una **collisione**.

**E la collisione aveva un verso sbagliato, ed è il difetto di `Z70`:** `chi_basc` scrive
`perc_chi` **dalla torsione `tw`**, cioè **un CAMPO decideva la CARICA**. Il par.8 dice che lo
spinore è l'oggetto fondamentale e il campo è ciò che l'oggetto **genera**: la freccia era invertita.

---

## 2. LA LEGGE — **separare le due grandezze, non spegnerne una**

```
chi_basc  ->  perc_geom     GEOMETRIA: sign(twn - PHI_CRIT), il giro compiuto o no
spinore   ->  perc_chi      CARICA:    sign(Re <canon(nb) | psi_spinor>), doppia copertura
```

**Perché non basta spegnere `chi_basc`** *(che è ciò che fa `--chi-da-spinore`)*: la geometria
alimenta la catena della torsione, ed è **da lì che probabilmente passa l'espansione**. Spegnendola
per accendere la carica si cambiano **due variabili insieme**, e un confronto con due variabili
cambiate insieme **non si legge** (par.1, un interruttore alla volta).

### Zero coefficienti nuovi
`perc_geom` usa **la stessa soglia** `PHI_CRIT` (il quanto di olonomia, `2π`) e **la stessa
formula** che `chi_basc` usava già. **Non nasce nessun numero** (par.3).

---

## 3. GLI ANELLI — **due, e non sono la stessa cosa**

### (a) `perc_geom ↔ tw` — **geometria, periodo 2, sfasato**
`chi_basc` legge `tw` e scrive `perc_geom`; la catena della torsione legge `perc_geom` e concorre a
`tw`. **L'anello resta**, ma è **una coerenza geometrica**: un campo che decide la propria
geometria, non la carica di qualcosa.

### (b) `perc_chi → B → _psi_spinor → perc_chi` — **l'anello NORMALE della fisica**
```
perc_chi  ->  chi_nodi (campo B del passo spinoriale)  ->  omega_s
          ->  _psi_spinor  (il commit)
          ->  perc_chi     (segno di doppia copertura)
```
**Le cariche generano campi, e i campi muovono le cariche.** È l'anello di ogni teoria di gauge.
**È SFASATO DI UN PASSO** e va dichiarato così: dentro `step()` la chiamata al passo spinoriale
precede la riscrittura di `perc_chi`, quindi
`perc_chi(t+1) = f(g(perc_chi(t)))` — **`A6` nella lettera non è violato** *(nessuna auto-referenza
istantanea)*, **ma l'anello c'è, ed è più stretto del periodo 2 di oggi.**

> **IL GUADAGNO NON È LA ROTTURA DELL'ANELLO: È IL VERSO.** Oggi è `tw`, un campo, a riscrivere la
> carica; con la cooperazione è lo **spinore** — l'oggetto fondamentale del par.8.

---

## 4. LA STRUTTURA — **una fonte, due padroni**

`chiralita_core_locale()` è chiamata **sia** dalla catena della torsione **sia** dal campo `B` del
passo spinoriale. Dirottarla sarebbe bastato a portare **anche il campo** sulla geometria, contro
la legge del §2. **Quindi l'array arriva come argomento**, e:

- **la cache la scrive il ramo che la possiede**: `_chi_geom_nodi` per la torsione,
  `_chi_core_nodi` per la carica;
- **il perché non è estetico:** l'ordine dentro `step()` è `FRAME_DRAG → _passo_spinoriale →
  TORS_4PI`, quindi **`TORS_4PI` legge la cache scritta PER ULTIMA**, cioè quella del passo
  spinoriale. Con una cache sola avrebbe ricevuto **la carica in silenzio** — nessun errore,
  nessun `NaN`, solo l'array sbagliato;
- **i tre diagnostici** `_chi_core_rho0` / `_chi_core_rhoc` / `_chi_core_raggio` **non dipendono
  dall'array**: sono calcolati da `I2` e da `lam_loc`. **Verificato dal codice**, e per questo il
  ramo della geometria non li riscrive.

---

## 5. LA NASCITA — **la carica si coniuga, la geometria no**

| via di crescita | `perc_chi` (carica) | `perc_geom` (geometria) |
|---|---|---|
| **semina** | `rng.choice([-1, +1])` | **copia** della carica *(al passo 0 sono la stessa cosa)* |
| **mitosi** | copia del genitore *(rompe `N(+1)−N(−1)`)* | **copia** del genitore |
| **Schwinger** | **`−`** del genitore *(antimateria; conserva)* | **copia** del genitore |

> **La geometria NON è coniugata**: *«il giro è compiuto»* non ha un'antiparticella.
> **È una scelta dichiarata, non ovvia** — e `chi_basc` riscrive `perc_geom` al passo dopo comunque.

**Le tre vie vanno coperte tutte**: se ne manca una, `len(perc_geom)` diverge da `n`
**in silenzio**. Per questo `Z4` verifica l'invariante a ogni passo **invece di assumerla**.

---

## 6. COSA QUESTO DOCUMENTO **NON** DICE

- **NON dice che la cooperazione migliori l'espansione.** È la domanda del ramo C, non una
  previsione;
- **NON dice che `A6` sia soddisfatto in spirito:** dice che è soddisfatto **nella lettera**, e che
  l'anello resta, **sfasato di un passo**;
- **NON dice che `:4493` sia neutro.** Il calcio alla nascita nel ramo A leggeva l'uscita di
  `chi_basc`; ora legge la carica. **Cambia la NASCITA dei nodi**, ed è un effetto atteso da tenere
  presente nel confronto A/C.
