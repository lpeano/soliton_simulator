# REFERTO — TEMPO 1 di `calcola_psi(w=None)`: **Q1 e Q2 passano. Ma «sedici violazioni» sono DUE — e il resto era già stato misurato tre giorni fa.**

**Blob:** `69ee5403` → `8f9...` (contatori aggiunti, **byte-identico**). Byte grezzi del riferimento
`ee0c2a60`. **Nessuna legge toccata.** `Z9` **non toccata**, come da mandato.

---

## 1. I SIGILLI DEL TEMPO 1

```
[PASS] Q1a c'e' CONFRONTO (stesso N, shape uguali)   38 array, nodi PRE 1669 = POST 1669
[PASS] Q1b BYTE-IDENTICO: max|A-B| = 0.000e+00       [BLOCCANTE]
[PASS] Q2  il contatore legge > 0                    _calcpsi_w_none = 134 su 134  (100.00 %)
```

**Q2 è netto: TUTTE le chiamate a `calcola_psi` passano dal ramo `w is None`.** Nessun chiamante,
nel file, passa `w`. **La diagnosi del mandato su QUESTO punto è giusta.**

---

## 2. ⚠ LA TABELLA — e **ridimensiona la premessa del mandato**

```
chiamante:riga                     volte     per passo   posizione
step:3006                            20        1.00      DENTRO il passo
step:3118                            20        1.00      DENTRO il passo
_registra_concorrenza:1768            3        (setup)   fuori
-------------------------------------------------------------------
DENTRO il passo (violano :2959)      40        2.00
fuori (setup/diagnostica)             3
```

> **Il mandato dice: *«Le "sedici volte" sono sedici violazioni di un intento già dichiarato»*.**
> **NON LO SONO. Le chiamate a `calcola_psi` dentro il passo sono DUE, non sedici.**

**Da dove vengono davvero le sedici chiamate a `_pesi()`:**

```
stato_crossover:424     260 totali   13.00 per passo   <-  l'80.5 %
calcola_psi:2498         43 totali    2.00 per passo   <-  il 13.3 %
step:2979                20 totali    1.00 per passo
                                     16.00 per passo
```

**`_pesi()` chiama INDIRETTAMENTE sé stesso** — profondità di annidamento misurata: **2**:

```
_pesi()  ->  _lam_archi()  ->  lambda_nodi()  ->  massa_critica_adattiva()  ->  stato_crossover()  ->  _pesi()
```

### ⚠ E QUESTO NON È UN REPERTO NUOVO: ERA GIÀ COMMITTATO IL 2026-09-14

**`doc/REPERTO_pesi_ricorsione.md`**, voce **M** del registro. E i numeri coincidono:

| | allora (14 set) | oggi (17 set) |
|---|---|---|
| da `calcola_psi` | **12.8 %** | **13.3 %** |
| da `stato_crossover` | **80.9 %** | **80.5 %** |

**E quel referto fermò un mandato per la STESSA ragione:**
> *«Il mandato della FASE B assume che le 16 chiamate per passo di `_pesi()` siano ricalcoli
> ridondanti dello stesso valore da parte di `calcola_psi()`… **La misura dice che la premessa è
> falsa.**»*

**La premessa di oggi è la stessa, e la misura la smentisce di nuovo, con gli stessi numeri.**
*(Lo scrivo così invece di presentarlo come una scoperta: P1 — prima di proporre una diagnosi si
rilegge dal disco ciò che è già stabilito. Qui il fatto c'era, e non l'avevo riletto prima di
misurare.)*

---

## 3. MA IL DIFETTO ESISTE, ED È FLAGRANTE — **su DUE punti, non sedici**

La domanda del 14 settembre era l'**ottimizzazione** (il costo). **Quella di oggi è la
CORRETTEZZA** — le letture miste `t`/`t+1` — ed è **diversa e legittima**. Guardiamo i due punti:

```python
:3005   if REPULS_LEGGE:
:3006       psi_forces = psi_t if SYNC_UPDATE else self.calcola_psi()
:3007       MtPsi = self._mat(w) @ psi_forces
```

> **Nella STESSA espressione:** `psi_forces` viene da `calcola_psi()`, che **ricalcola i pesi al suo
> interno**, e `self._mat(w)` usa **il `w` calcolato da `step` a `:2979`**.
> **Due insiemi di pesi diversi, moltiplicati insieme.**
> **È esattamente la «lettura mista t/t+1» che il commento a `:2960` vieta**, e sta **una riga
> sotto** quella che sarebbe la cura.

Stessa struttura a `:3118` (`psi_sync = psi_t if SYNC_UPDATE else self.calcola_psi()`).

**Entrambi i rami sono presi perché `SYNC_UPDATE` è FALSE** — spento in tutti i run del fork. **Con
`SYNC_UPDATE` acceso il difetto non esiste**: si userebbe `psi_t`, calcolato una volta da `w`.

---

## 3-bis. ⚠ TRE PUNTI NEL SORGENTE, DUE A RUNTIME — la discrepanza, sciolta

**Rilievo del guardiano:** *«io trovo TRE punti dentro `step`, lui ne dichiara DUE»*. **Ha ragione
sui punti sorgente, e non e' un disaccordo: contavamo unita' diverse.** Dal codice:

```python
:3005   if REPULS_LEGGE:                      # <- True di DEFAULT (:544)
:3006       psi_forces = psi_t if SYNC_UPDATE else self.calcola_psi()     GIRA
:3007       MtPsi = self._mat(w) @ psi_forces
        [...]
:3036   elif MU_PSI != 0.0:                   # <- elif: ESCLUSO da REPULS_LEGGE = True
:3037       psi_forces = psi_t if SYNC_UPDATE else self.calcola_psi()     NON GIRA
:3038       MtPsi = self._mat(w) @ psi_forces
        [...]
:3118   psi_sync   = psi_t if SYNC_UPDATE else self.calcola_psi()         GIRA (se K_SYNC != 0)
```

> **`:3006` e `:3037` sono i due rami di un `if`/`elif` MUTUAMENTE ESCLUSIVI.** Il commento a
> `:3039` chiama il secondo *«vecchia repulsione a parametro, fallback»*: con `REPULS_LEGGE = True`
> **non viene mai preso**, e infatti il contatore non lo registra.

**Il contatore misura CIO' CHE GIRA; il grep misura CIO' CHE E' SCRITTO. Entrambe le misure sono
giuste, e servono a cose diverse:** *«due da correggere»* e' azionabile, *«tre punti»* e' la mappa
completa.

**E il terzo punto ha lo STESSO difetto flagrante:** `:3038` fa `self._mat(w) @ psi_forces`,
identico a `:3007`.

### Cosa cambia per il TEMPO 2

**I punti da toccare sono TRE, non due**, e vanno trattati diversamente:

| punto | gira? | cosa fare |
|---|---|---|
| `:3006` | **SI'** (`REPULS_LEGGE = True`) | passare `w`. **Q4 lo esercita.** |
| `:3118` | **SI'** (se `K_SYNC != 0`) | passare `w`. **Q4 lo esercita.** |
| `:3037` | **NO** (`elif` escluso) | passare `w` **per coerenza**, ma **NESSUN SIGILLO PUO' TESTARLO** in questa configurazione. **Va dichiarato**, non spacciato per verificato. |

> **`:3037` NON e' un chiamante «fuori dal passo»** — quelli il mandato dice di non toccare per
> simmetria. **E' dentro il passo, su un ramo spento da un flag.** Correggerlo e' legittimo (stesso
> difetto, stesso blocco), **ma il suo esito resta non esercitato**, e il referto del TEMPO 2 dovra'
> dirlo invece di contarlo fra i successi. *(E' la classe di `VERSO_CHI`: cablato ma muto.)*

## 4. VERIFICHE PRELIMINARI DEL TEMPO 2 — **la strada è aperta, su due punti**

1. **`w` è ancora valido lì?** **SÌ**: `:3007` **lo sta già usando** (`self._mat(w)`). Se non fosse
   valido, quella riga sarebbe già rotta. **La topologia non cambia fra `:2979` e `:3006`/`:3118`.**
2. **Qualche chiamante si aspetta pesi RICALCOLATI?** Nei due punti interni **no**: entrambi
   vogliono `psi` *della snapshot*, ed è quello che `psi_t` fornisce nel ramo `SYNC_UPDATE`. **Il
   ramo `else` è il fallback, e deve dare la stessa cosa.**
3. **`calcola_psi` SCRIVE `self.psi`.** **Confermato**, e passare `w` **non lo cambia**: resta una
   scrittura di stato dentro il passo. *(I chiamanti fuori dal passo — `:388`, `:446`, `:5952`,
   `:6688` — scrivono `self.psi` in contesti di diagnostica: è il fronte **H**, già registrato, e
   NON lo tocco.)*

---

## 5. COSA CHIEDO — **il via libera al TEMPO 2, ridimensionato**

**Il TEMPO 2 riguarda TRE righe** — `:3006`, `:3118` (che girano) e `:3037` (ramo `elif` **spento**, vedi §3-bis): passare `w`, che e' gia' li'.

**Ma la sua portata non è quella che il mandato prevedeva:**
- **non elimina 16 ricalcoli**, ne elimina **2** (il **13 %**);
- **gli altri 13** vengono da `stato_crossover` attraverso `massa_critica_adattiva`, e **quello è un
  fronte diverso** (voce **M**, *«resta il costo, non la cura»*), che questo mandato **non tocca**;
- **e sull'EFFETTO non ho una previsione**: i pesi ricalcolati potrebbero coincidere con quelli di
  `step` — nel qual caso il difetto è **teorico** e Q4 lo dirà. **È una misura, non un'attesa.**

**Mi fermo qui, come il mandato ordina** (*«STOP e riporta la tabella»*).
