# TASK HISTORY — **`CHI_COOP`: il ramo C a COOPERAZIONE** (2026-09-21)

> **Scritto e committato PRIMA del lavoro** (par.5-septies). L'ordine e' verificabile da git: questo
> commit dev'essere **antenato** dei commit del codice e dei sigilli.
> Simulatore di partenza: **`b46835bd`** *(sha1 byte grezzi)*. Driver: **`9aee4fc2`**.
> Decisioni: **la CORREZIONE del ramo C**, la sua **AGGIUNTA**, e il mandato **DECISIONI**.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### Cosa e' gia' stabilito e NON va ri-derivato
- **`Z85`**: la catena della torsione tocca `perc_chi` in **un solo punto raggiungibile**,
  `:1574` dentro `chiralita_core_locale()`, perche' con `CHI_CORE=True` i tre siti passano tutti
  di li'. **Accolto da Luca.**
- **`Z70` corretta**: `CHI_DA_SPINORE` **non rompe** l'anello, lo **inverte di verso**.
- **Il difetto vero** non era l'anello: era **un CAMPO (`tw`) che decideva la CARICA**.

### La premessa che il censimento ha fatto cadere, e che l'AGGIUNTA non poteva sapere
**`chiralita_core_locale()` e' chiamata da DUE padroni**: la torsione (`:3763`, e la cache letta da
`:3894`) **e** il campo `B` dello spinore (`:2388`). Dirottare `:1574` su `perc_geom` avrebbe portato
**anche il campo dello spinore sulla geometria**, contro la decisione dell'AGGIUNTA.
**Non e' un dettaglio implementativo: era la premessa del disegno.**

### Cosa mi aspetto
1. **`Z1` (byte-identita' a `CHI_COOP` spento) passa**: tutte le modifiche sono argomenti con
   default che riproducono il comportamento di oggi. **Se fallisce, ho toccato un percorso che
   credevo inerte;**
2. **`Z2` sui contatori passa**, ed e' il sigillo che porta davvero informazione: dice **quale array
   riceve ogni chiamata**;
3. **`Z2` sul primo passo passa** — `perc_geom(C, t=1) == perc_chi(A, t=1)` — **ma e' DEBOLE**, e lo
   dichiaro: al passo 1 i due array sono ancora identici, quindi un lettore assegnato male
   **passerebbe comunque**. **La forza sta nei contatori, non nel confronto con A;**
4. **il ramo C DIVERGE da A quasi subito**, e questo **non e' un fallimento**: lo spinore sente la
   carica vera dal passo 2, e `:4493` cambia la NASCITA dei nodi.

### Cosa NON so, e lo scrivo prima
- **non so se il ramo C si espande come A.** E' la domanda del run, non una previsione;
- **non so quanto pesi `:4493`.** Nel ramo A il calcio alla nascita leggeva l'uscita di `chi_basc`;
  ora legge la carica dello spinore. **Se l'espansione passa dalla nascita dei nodi, questo sito
  puo' contare piu' della torsione** — e non ho modo di dirlo prima di misurare;
- **non so se `_chi_core_rho0`/`_chi_core_rhoc`/`_chi_core_raggio`** *(diagnostici scritti dalla
  stessa funzione)* **abbiano letture che si aspettano la carica o la geometria.** Verifico prima
  di scrivere;
- **non so se il costo raddoppia.** Oggi la funzione gira **due volte per passo** (`:3763` e
  `:2388`); con la cooperazione dovrebbe girare **ancora due volte** (una per array), ma
  **e' da verificare, non da assumere.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *come ci arrivo, e cosa mi ferma*

### La forma della modifica, decisa PRIMA di scriverla
```
chiralita_core_locale(sorgente=None, geom=False)
    sorgente is None  ->  self.perc_chi        (LEGACY: byte-identico)
    geom=False        ->  scrive _chi_core_nodi + i tre diagnostici   (LEGACY)
    geom=True         ->  scrive _chi_geom_nodi                        (solo con CHI_COOP)
```
**DICHIARAZIONE, come il mandato chiede:** **la cache la scrive il ramo che la possiede.** Con
`CHI_COOP` acceso, `_chi_geom_nodi` e' scritta **solo** dalle chiamate della torsione, e
`_chi_core_nodi` **solo** da quella del campo `B`. **A `CHI_COOP` spento il ramo `geom` non gira
mai**, quindi la byte-identita' non dipende dalla mia parola: dipende dal fatto che il ramo sia
**irraggiungibile**.

### Le assegnazioni che cablero' (dalla tabella §2 del mandato)
| sito | array |
|---|---|
| `:1574` chiamato dalla torsione (`:3763` `FRAME_DRAG`, `:3894` `TORS_4PI`) | **`perc_geom`** |
| `:2388`/`:2395` campo `B` dello spinore — **compreso il suo `else`** | **`perc_chi`** *(invariato)* |
| `:3771` `VERSO_CHI`, `:3898` fallback della torsione | **`perc_geom`** |
| `:4493` mitosi, `:622`, `:2099`, `:2731`, `:1878`, Schwinger, `TEMPO_SEGNO` | **`perc_chi`** *(invariati)* |

**UNA SCELTA DI PRUDENZA CHE DICHIARO PRIMA:** **le GUARDIE di lunghezza restano su `perc_chi`.**
Sono `len(self.perc_chi) >= self.n`, e i due array hanno la stessa lunghezza **per costruzione**
(le tre vie di crescita estendono entrambi). **Cambiarle non aggiungerebbe protezione e
aggiungerebbe superficie.** **`Z4` verifica l'invariante invece di assumerla.**

### I passi, e cosa decide ciascuno
1. **verifica dal disco** dei tre diagnostici della cache e del costo per passo → **se un lettore
   si aspetta la carica dove metto la geometria, FERMO e riporto;**
2. **`perc_geom`**: init + **tre** vie di crescita (semina / mitosi / Schwinger) + snapshot.
   *(`salva_stato` lo prende **automaticamente**: il filtro `:3203` accetta `np.ndarray` scorrendo
   `__dict__` — **verificato dal disco, non assunto**.)*
3. **i contatori di `Z2`**, byte-inerti;
4. **`:3917`** — `chi_basc` gira anche con lo spinore, e scrive `perc_geom`;
5. **`:3941`** — lo spinore scrive `perc_chi` anche sotto `CHI_COOP`;
6. **il driver** `--chi-coop=on|off`, default off;
7. **commit**, poi i **sigilli**.

### COSA MI FA FERMARE — fissato ORA, prima dei numeri
- **`Z1` FALLISCE** *(byte-identita' a flag spento, simulatore o driver)* → **STOP.** Non allargo il
  criterio: cerco cosa ho toccato;
- **`Z2` FALLISCE** *(una chiamata della torsione su `perc_chi`, o quella del campo su `perc_geom`)*
  → **STOP: un lettore e' sull'array sbagliato;**
- **`Z3` FALLISCE** *(`chi_basc` scrive `perc_chi` anche una sola volta, o `perc_chi` non e' il segno
  di doppia copertura)* → **STOP;**
- **`Z4` FALLISCE** *(`len(perc_geom) != n` a un qualunque passo)* → **STOP: una via di crescita mi
  e' sfuggita, ed e' esattamente il difetto silenzioso che il mandato teme;**
- **un `NaN`** → STOP.

### E UN CONTROLLO POSITIVO OBBLIGATORIO, senza il quale `Z2` e' vuoto
Se `perc_geom` e `perc_chi` **non differiscono mai** durante il sigillo, il test *«la torsione legge
la geometria»* **non ha distinto niente**: due array uguali passano qualunque assegnazione.
**Il sigillo deve VERIFICARE che i due array abbiano differito**, e dichiarare **`FAIL` se non
differiscono** — non `PASS`. *(E' la stessa famiglia del `max|A-B| = 0.000e+00` per mancanza di
confronto, par.9.)*

---

## 3. TODO DEL NEXT STEP

- [ ] verifica dal disco: i tre diagnostici della cache, il costo per passo, le guardie
- [ ] `perc_geom`: init, tre vie di crescita, snapshot
- [ ] contatori `Z2` (byte-inerti)
- [ ] `chiralita_core_locale(sorgente, geom)` + i chiamanti della torsione
- [ ] `:3917` / `:3941` / `SystemExit` su `--spinore-corretto`
- [ ] driver `--chi-coop=on|off` + sigillo di byte-identita' dell'argv
- [ ] **INVENTARIO / README / FISICA nello stesso commit** (par.5-novies)
- [ ] **commit + push PRIMA dei sigilli**
- [ ] `Z0`-`Z6`; se `Z1`/`Z2`/`Z3`/`Z4` falliscono → **STOP e riporta**
- [ ] ramo C: seme di A, `sep = 4.0`, 3000 passi, `--db-ogni 120`, archivio `_ab_C`
      *(non temporaneo, non in un `finally`)*
- [ ] confronto A/B/C → **CHECKPOINT a Luca**
