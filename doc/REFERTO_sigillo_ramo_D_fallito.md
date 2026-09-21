# REFERTO — **il sigillo del ramo D NON passa: `7/9`, e i due fallimenti sono opposti**

> Mandato perentorio delle tre modifiche, §Z0-Z7. **Il mandato dice di fermarsi SOLO se fallisce un
> sigillo BLOCCANTE: ne sono falliti DUE, ed e' successo.** **Nessuna cura applicata, nessun run
> lanciato, nessun criterio allargato.**
> Simulatore **`43972024`** *(sha1 byte grezzi, non `git hash-object`: C18)*, sigillo **`f884eff0`**,
> confronto contro **`54623593`** *(il commit `0f4fc1e`, prima di `SCALA_MIN` e `COES_ADIM`)*.
> Output: `csv/_seal_fork/_sigillo_ramo_D_FALLITO_2026-09-21.txt`.
> **EPOCA 2** *(i tre flag esistono; qui sono esercitati uno per uno e tutti insieme)*.

---

## 1. L'ESITO

```
Z1   PASS   tutti i flag spenti -> 10 campi BYTE-IDENTICI
Z2   PASS   ogni flag DA SOLO cambia qualcosa (10/10 campi ciascuno: nessuno e' codice morto)
Z3   PASS   torsione su perc_geom 30, campo B su perc_chi 30,
            chi_basc -> perc_geom 30 volte e perc_chi ZERO,
            perc_chi == segno di doppia copertura in 30 passi su 30
Z4a  FAIL   max(dx_eff - dx) = +0.772        (il criterio diceva <= 0)
Z4b  FAIL   min(d) = 0.075760   min(d0) = 0.078622   LAM = 0.800000
Z4c  PASS   stress |d-d0|/d0 massimo 2.071926 -- FINITO
Z4d  PASS   casi patologici `dx <= -x`: 0    pavimenti vecchi SALTATI: 175
Z5   PASS   |delta d0| max 1.052725e-02 <= passo_causale 1.131371e-02
            archi saturi: 0 su 15 818 181 = 0.00 %
Z6   PASS   tutti accesi: nessun NaN, nessun inf, tutte le lunghezze = n
```

---

## 2. `Z4a` — **IL CRITERIO E' SBAGLIATO, NON IL CODICE. L'errore e' mio.**

Avevo scritto, nel task history e nel sigillo:

> *«`_g_sm_max_su = max(dx_eff - dx)` DEVE restare `<= 0`: il vincolo non AUMENTA mai un
> incremento, quindi non puo' produrre espansione da solo.»*

**E' FALSO, e lo e' per costruzione.** Per `dx < 0` la legge fa `dx_eff = dx * f` con `f ∈ [0, 1]`,
quindi:
```
dx_eff = dx*f  >=  dx        (perche' dx < 0 e 0 <= f <= 1)
->  dx_eff - dx  >=  0,  fino a |dx|
```
> **Attenuare una discesa rende l'incremento MENO NEGATIVO. Il numero `+0.772` non e' un difetto:
> e' LA DEFINIZIONE DELLO SMORZAMENTO.**

**E' esattamente l'errore che `CLAUDE.md` par.9 cataloga** — *«un criterio di sigillo si scrive da
una MISURA, non dal proprio modello mentale del codice»* — **e stavolta l'ho commesso sul criterio
che doveva dimostrare la proprieta' piu' importante della modifica.**
*(E' il quarto caso della stessa famiglia registrato su questo repo: `N3b`, `M1b`/`M3`, `M3c`, e
ora `Z4a`.)*

### La META' che conta HA PASSATO, e va detto
**`_g_sm_viol_id = 0`**: **nessun incremento `>= 0` e' mai stato toccato**, in **tutto** il run e su
**tutte** le scritture. **Le lunghezze che non scendono non cambiano di un bit** — che e' la
richiesta letterale di Luca.

### IL CRITERIO GIUSTO, e si STRINGE, non si allarga
La proprieta' vera e': **il nuovo valore sta sempre in `[x + dx, x]`**, cioe' il vincolo puo' solo
**ridurre la magnitudine di una discesa**, mai aggiungere moto verso l'alto:
```
dx >= 0   ->   dx_eff == dx        (identita' esatta)        [gia' misurato: 0 violazioni]
dx <  0   ->   dx <= dx_eff <= 0   (mai POSITIVO)            [DA MISURARE: e' il criterio nuovo]
```
**`max(dx_eff) su dx < 0` deve valere `<= 0`.** E' piu' STRETTO del precedente in un punto che il
precedente non guardava affatto, e non copre il fallimento: lo sposta dove la proprieta' vive.

---

## 3. ⚠ `Z4b` — ~~la sua causa NON E' TROVATA~~ **SUPERATO DAL §5, E LA SEZIONE RESTA**

> **⚠ QUESTA SEZIONE E' STORICA: la causa E' stata trovata poche ore dopo, ed e' nel §5.**
> **Non la cancello**, per la stessa convenzione dei marchi storici di `CLAUDE.md`: si legge per
> sapere **cosa era stato escluso e con quale ragionamento** — e soprattutto perche'
> **l'ipotesi che avevo lasciato in piedi era QUELLA SBAGLIATA.**
> **Avevo concluso *«esiste uno scrittore fuori dai DODICI di `Z78`»*. E' FALSO: il censimento
> era giusto. A sbagliare non era il DOVE, era il QUANDO.**
> **L'errore di ragionamento e' identificabile: avevo elencato le ipotesi sul MECCANISMO della
> scrittura e nessuna sul MOMENTO in cui il mondo viene costruito.** Il dato che lo diceva era
> gia' nei numeri — `min(d) = min(d0)` a nove cifre — **e non l'ho letto.**


**`min(d) = 0.0758` con `LAM = 0.8`: DIECI VOLTE SOTTO.** E `min(d0) = 0.0786`.

### Cosa ho ESCLUSO dal disco, non per congettura
| ipotesi | esito |
|---|---|
| un arco NASCE sotto `LAM` | **ESCLUSO**: le **tre** vie di creazione — `_allaccia` (`:2216`), mitosi (`dh`, `d0new`), Schwinger (`dd`) — passano **tutte** per `_nasce` = `max(·, LAM)` |
| una discesa scavalca l'invariante | **ESCLUSO**: `_g_sm_patol = 0`. Il caso `dx <= -x`, l'unico in cui `nuovo - LAM = (x-LAM)(1+dx/x)` cade, **non e' mai scattato** |
| il pavimento comovente li tiene giu' | **ESCLUSO**: i sette pavimenti sono **saltati 175 volte**, quindi non agiscono piu' |
| uno scrittore di `d`/`d0` non passa dalla legge | **⚠ NON ESCLUSO — ed e' l'unica ipotesi rimasta** |

### La conseguenza, e vale AL DI LA' di `SCALA_MIN`
> **Se ogni arco nasce `>= LAM` e nessuna discesa puo' portarlo sotto, allora esiste una TERZA VIA
> che non ho trovato.**
> **Cioe': o c'e' uno scrittore di `d`/`d0` FUORI dai DODICI censiti in `Z78`, oppure uno dei dodici
> non passa da dove credo.**

**E' un riscontro sul CENSIMENTO, non solo sulla modifica.** `Z78` fu gia' corretta in loco una
volta — avevo scritto «DIECI scrittori» e la rilettura dal disco ne diede **DODICI**. **Questo
numero potrebbe essere ancora incompleto.**

### Come si chiude, e NON si chiude a ragionamento
**Strumentare la caduta:** al primo passo in cui `min(d) < LAM`, registrare **quale sito** ha
scritto quel valore. La strumentazione `TRACCIA_D0` esiste gia' e copre i dodici siti di `d0`;
**per `d` non c'e' un equivalente**, e va aggiunto — **byte-inerte, gated, come le altre**.

---

## 4. COSA QUESTO REFERTO **NON** DICE

- **NON dice che `SCALA_MIN` sia sbagliato.** Le quattro proprieta' della legge sono state
  verificate numericamente *(identita' esatta `0.0`, invariante a `2.2e-15`, 200 dimezzamenti che
  convergono a `LAM` restando sopra, discesa nulla sotto `LAM`)*. Dice che **il vincolo non copre
  una via di scrittura che non conosco**;
- **NON dice niente sul ramo D**: non e' stato lanciato, e **non si lancia finche' i due bloccanti
  non sono risolti** *(voce `3` della coda unica in `doc/STATO_RUN.md`)*;
- **NON confronta con A, B o C** — epoca 1, e il mandato lo vieta;
- **LIMITI: un seme, una scena, 30 passi.** In 30 passi la coppia di **Schwinger** puo' non essere
  mai scattata, quindi **la terza via di nascita puo' essere NON ESERCITATA**, e la riga «esclusa»
  della tabella sopra vale per `_allaccia` e per la mitosi con certezza, **per Schwinger solo se e'
  scattata**. **Si legge da `_g_nati_schwinger`, e in questo giro non l'ho letto.**

---

## 5. ✅ **`Z4b`: LA CAUSA E' TROVATA — ed e' un problema di ORDINE, non una via di scrittura mancante**

> **L'indizio che ha aperto la diagnosi e' di Luca**, e non lo avevo sfruttato: `min(d)` e `min(d0)`
> erano **identici a nove cifre** (`0.075759598` entrambi). **Una discesa dinamica li
> SEPAREREBBE**, perche' `d` e `d0` sono mossi da leggi diverse. **Due valori identici sono la
> firma di un arco NATO cosi'.**

### 5.1 La misura al passo 0
```
subito dopo la semina:  n = 2391   archi = 527 088   LAM = 0.8000
    archi con d  < LAM:  2848  (0.54 %)      min(d)  = 0.075759598
    archi con d0 < LAM:  2848  (0.54 %)      min(d0) = 0.075759598
    su quegli archi:  max|d - d0| = 0.000e+00  ESATTO      <- NATI uguali
    i loro indici: da 3 a 59 729
    percentili di d: p01 = 0.8000   p50 = 0.8801   p99 = 2.3720
```
**`p01 = 0.8000` esatto: `_nasce` ha davvero sollevato a `LAM` una parte della popolazione.**

### 5.2 `_allaccia` FUNZIONA — tracciato per chiamata
```
_nasce      156 768 archi   min PRIMA 0.014273  ->  min DOPO 0.800000
_allaccia   156 768 archi aggiunti   min 0.800000   sotto LAM: 0
_nasce      154 373 archi   min PRIMA 0.016586  ->  min DOPO 0.800000
_allaccia   154 373 archi aggiunti   min 0.800000   sotto LAM: 0
_nasce      156 217 archi   min PRIMA 0.015176  ->  min DOPO 0.800000
_allaccia   156 217 archi aggiunti   min 0.800000   sotto LAM: 0
                                    TOTALE AGGIUNTI: 467 358
```
> **Tre invocazioni, `467 358` archi, ZERO sotto `LAM`.** **Ma al passo 0 gli archi sono
> `527 088`: ne mancano `59 730` — ESATTAMENTE l'intervallo `3..59729` in cui vivono tutti quelli
> sotto `LAM`.**

### 5.3 ⚠ DOVE NASCONO: **`:5379-5380`, a livello di MODULO**
```python
net = Rete()                    # :5379   <- gira all' `import`
net.semina(SEME_INIZIALE)       # :5380
```
**Il vuoto — `59 730` archi — e' costruito quando `import soliton_simulator` viene eseguito**,
cioe' **PRIMA di `_cli()` e di `_applica_flag()`**, quando **ogni flag da riga di comando e'
ancora al suo default di modulo** e `SCALA_MIN` vale `False`.

`_applica_flag` accende `SCALA_MIN` a **`:6492`**, ma la ricostruzione della rete a **`:6713`** e'
**CONDIZIONALE**:
```python
if a.seed is not None or a.nodi != SEME_INIZIALE:
    net = Rete(...); net.semina(a.nodi); ...
```
**e in questa configurazione NON SCATTA.** **Il vuoto costruito all'import SOPRAVVIVE.**

**Verificato direttamente: dopo `_applica_flag` e PRIMA di `avvia_test`, la rete ha gia'
`59 730` archi.**

### 5.4 Il sospetto DI METODO e' ESCLUSO dal disco
| controllo | esito |
|---|---|
| scritture `out=` su `d`/`d0` | **ZERO occorrenze** |
| alias che scrivono | **nessuno**: i quattro trovati (`:3144 dopo`, `:3634 dd`, `:4332`/`:4334` `d_arco`) sono **tutti in sola lettura** |
| siti dove `self.i` cresce | **TRE soli**: `:2214` `_allaccia`, `:4722` mitosi, `:4824` Schwinger — **tutti coperti** |

> **Quindi `Z78` NON e' incompleta: il censimento degli scrittori era GIUSTO.**
> **RITIRO l'ipotesi che avevo scritto** — *«uno scrittore fuori dai dodici»* — **era il candidato
> sbagliato. A sbagliare non era il DOVE, era il QUANDO.**

### 5.5 ⚠ E LA CONSEGUENZA E' PIU' GRANDE DI `SCALA_MIN`

> **Il VUOTO — il substrato di tutto — e' costruito PRIMA che la fisica sia configurata.**
> **Qualunque flag che dovrebbe agire al momento della semina e' INERTE per il vuoto**, e lo e'
> **in silenzio**: nessun errore, nessun avviso, solo un mondo nato con leggi diverse da quelle
> che il comando chiedeva.

**E il sistema parte SOTTO la propria scala minima fin dal primo istante:** `0.54 %` degli archi,
il minimo **dieci volte** sotto `LAM`, la mediana della popolazione sotto-`LAM` a `0.63 LAM`.
**`SCALA_MIN` poi funziona correttamente — li CONGELA, non li fa scendere oltre — ma non puo'
sollevarli**, perche' sollevarli sarebbe l'inflazione che la forma e' fatta apposta per evitare.

### 5.6 COSA **NON** FACCIO
**NON applico la cura.** Cambiare **quando** il mondo viene costruito e' una decisione di
struttura, non un ritocco: tocca **ogni** flag, non solo i tre del ramo D. **Si riporta e si
aspetta Luca** *(voce `3` della coda unica)*.
