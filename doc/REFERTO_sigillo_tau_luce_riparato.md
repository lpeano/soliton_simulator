# REFERTO — **Il sigillo di `--tau-luce` è riparato: `6/7 PASS`. E il `FAIL` che resta è un RISULTATO, non un difetto**

**Data:** 2026-09-19 · **Blob `b9e07c73` INVARIATO — e il sigillo stesso lo DIMOSTRA (`T0`)**
**Fallimento committato PRIMA:** `38bd0a7` · **Riparazione committata PRIMA della corsa:** `54c9730`
**Task history con la diagnosi:** `47b7804` · **Output:** `csv/_seal_fork/_sigillo_tau_luce_RIPARATO_2026-09-19.txt`

> **⚠ SI È RIPARATO IL SIGILLO. LA LEGGE `--tau-luce` NON È STATA TOCCATA**, e non lo asserisco io:
> **`T0` misura il blob della fisica PRIMA e DOPO la corsa, e sono identici.**

```
ESITO: T0=PASS  T1a=PASS  T1b=PASS  T2=PASS  T3=FAIL  T4=PASS  T5=PASS
TEMPI: T1a=93s  T1b=35s  T2=68s  T3=2975s  T4=66s  T5=66s     TOTALE 3305 s
```

---

## 0. LE TRE LETTURE DEL MANDATO — **quale è scattata**

| lettura fissata in `§1.2` | esito |
|---|---|
| **il criterio è SCADUTO** → si riscrive, e dev'essere ancora capace di fallire | **✓ È QUESTA, per `T1` e per `T3`** |
| il sigillo cerca un RIFERIMENTO che non c'è (famiglia `Z31`) | **NO** — il riferimento era committato e col blob giusto |
| **la LEGGE è sbagliata → FERMARSI** | **NO**, e la ragione è `T4`: `tau` segue `d` e `cs` in modo ESATTO |

**Più un difetto del TEST (`T2`), che è la stessa famiglia della prima lettura.**

---

## 1. ⚠ `T1a` — **il cablaggio NON cambiò il ramo OFF.** Era la condizione BLOCCANTE

```
f5887254 (PRE, senza TAU_LUCE)  contro  7d484580 (POST, TAU_LUCE presente ma OFF)
  n_A = 1718   n_B = 1718   ->  CONFRONTABILI
  21 campi confrontati, PEGGIOR max|A-B| = 0.000e+00   stato RNG identico
T1a: PASS
```

**Il criterio vecchio dava `n_A = 1718` contro `n_B = 1484`: NESSUN CONFRONTO.** Non perché il flag
avesse rotto qualcosa, ma perché **confrontava il disco di OGGI con un blob di tre giorni fa**, e in
mezzo ci sono **sette correzioni di legge sigillate**.

> **`T1` asseriva «il flag OFF è byte-identico al comportamento PRIMA della modifica» ed ESEGUIVA
> «oggi è uguale a tre giorni fa».** **La riparazione ancora il confronto alla COPPIA DI BLOB CHE
> RACCHIUDE IL CAMBIAMENTO**, entrambi PINNATI come costanti dichiarate ed estratti con
> `git cat-file -p` **in BINARIO** *(mai `git checkout`: trappola CRLF `C18`)*, **col blob
> RICALCOLATO e verificato.**
> **È la lezione di `c818208` rovesciata:** là era il lato **NUOVO** ad andare alla deriva perché
> ancorato a `HEAD`; qui è il lato nuovo a **non dover essere `HEAD`**.

**E se un blob non è estraibile, il sigillo ESCE CON ERRORE.** **Non degrada in un confronto contro
il vuoto** — è il difetto `pre_src = "" if not os.path.exists(PRE)` che il mandato nomina, e che
**in questo sigillo non c'era, ma nella riparazione è escluso per costruzione.**

## 2. `T1b` — **la verifica di OGGI, e può fallire sul blob corrente**

```
chiamate a `_tempo_luce_nodo`, PER RIGA DEL CHIAMANTE (flag OFF):
  riga 2337    31 chiamate        <- l'INERZIA
  riga 3027    27 chiamate        <- lo STRATO 1
sito tau-luce (2442): 0 chiamate   altri siti: 58
T1b: PASS
```

**A flag spento il ramo tau-luce non viene preso nemmeno una volta** (P5/A8).
**E il criterio richiede ANCHE che gli altri siti siano `> 0`**: senza quella condizione, un
contatore rotto darebbe `0` ovunque e **il PASS sarebbe VUOTO**.

## 3. ⚠ `T2` — **riparato, e la diagnosi esistente era INCOMPLETA**

```
contatori del discriminatore: sito tau-luce 31   altri siti 58
  n_A = 1484   n_B = 1484   ->  CONFRONTABILI
  21 campi confrontati, PEGGIOR max|A-B| = 0.000e+00   stato RNG identico
T2: PASS
```

**Il documento del fallimento diceva che `_tempo_luce_nodo` è chiamato «anche da
`_bloch_ritardato`». VERIFICATO DAL DISCO: I CHIAMANTI SONO TRE, NON DUE.**

```
:2337  _passo_spinoriale   L'INERZIA (_T2 = T^2)   -- NON gated su TAU_LUCE
:2442  _passo_spinoriale   il rilassamento tau-luce, dentro `if TAU_LUCE:`
:3027  _bloch_ritardato    lo STRATO 1
```

> **E i primi due stanno NELLA STESSA FUNZIONE: `co_name` non basta a distinguerli.**
> **Il monkeypatch vecchio cambiava TRE meccanismi, non due** — e uno dei tre è **l'inerzia, che è
> legge promossa e non ha niente a che fare con questo flag.**

**Il wrapper nuovo discrimina per riga del chiamante, MA LA RIGA NON È PINNATA:** si trova a runtime
**cercando il FLAG** — il blocco *indentato* `if TAU_LUCE:` e la chiamata `self._tempo_luce_nodo(`
dentro quel blocco, **coi commenti scartati**. **È par.0 alla lettera** *(«cerca per NOME di
funzione/flag, non per riga»)*: se il blocco si sposta, la ricerca lo segue.
**E se i siti trovati non sono ESATTAMENTE UNO, il sigillo RIFIUTA DI GIRARE.**

**Il risultato è `0.000e+00` ESATTO con shape uguali e RNG identico** — dove prima c'erano residui
`fino a 6.063e-07` **sui campi dello Strato 1** (`_nb_ret`, `_nb`, `_psi_spinor`, `omega_s`), che
erano **la firma del difetto.**

---

## 4. ⚠ `T3` — **FALLISCE, e questa volta il FAIL È UN RISULTATO**

**Il criterio vecchio** chiedeva che la pendenza si **allontanasse** da zero di almeno `0.3`.
**Soglia e DIREZIONE venivano da un'attesa (`-1.03`) calcolata quando `cs` era MORTO**
(`cs_std/cs = 0.0079 %`). **Oggi `cs` è VIVO (`17.6 %`)** e la baseline `OFF` ha dato `-0.17`, poi
`-1.73`, poi `+0.34` **su tre blob**: quella soglia non ha più niente a cui appoggiarsi.

**Il criterio nuovo non prescrive una direzione e non sceglie una soglia:** chiede che l'effetto
superi **il NULLO MISURATO DENTRO IL SIGILLO**, come dispersione **FRA SEMI** — `P3`: **quattro semi
appaiati**, perché con due `t(0.025,1) = 12.706` e l'IC95 è inutilizzabile.

```
seme |  OFF pendenza +- SE (r2, n)      |  ON pendenza +- SE (r2, n)       | DIFF ON-OFF
1    | +0.3370 +- 0.0884 (0.031,  452)  | +0.5218 +- 0.1366 (0.031,  462)  |   +0.1849
2    | -0.9501 +- 0.2581 (0.142,   84)  | -1.0036 +- 0.1475 (0.372,   80)  |   -0.0535
3    | +0.0049 +- 0.0553 (0.000,  817)  | +1.0337 +- 0.1015 (0.114,  811)  |   +1.0288
4    | -1.0592 +- 0.0499 (0.344,  862)  | -0.1673 +- 0.0604 (0.009,  831)  |   +0.8919

NULLO MISURATO: std(OFF fra semi) = 0.6936     SE INTERNA tipica = 0.1129
EFFETTO APPAIATO: media = +0.5130  std = 0.5286  SE = 0.2643  IC95 = [-0.3280, +1.3540]
T3: FAIL
```

> **L'IC95 dell'effetto appaiato CONTIENE LO ZERO. Il flag non produce un effetto distinguibile dal
> rumore fra semi, su quattro semi.**

### 4.1 ⚠ E come va LETTO questo nullo — **par.9: mai «nessun effetto», sempre un LIMITE**

**Si scrive così: *«l'effetto di `--tau-luce` sulla pendenza non è distinguibile da zero, e la
risoluzione di questo test è `±0.84`»*** — la semi-ampiezza dell'IC95.
**La stima puntuale è `+0.51`, cioè MENO della risoluzione: è «NON MISURATO», non «nessun effetto».**

### 4.2 ⚠ E `C10` di par.9 è confermata, con un numero PEGGIORE di quello che dice

```
dispersione FRA SEMI delle pendenze OFF, a codice INVARIATO : 0.6936
SE INTERNA tipica a un singolo run                          : 0.1129
rapporto                                                    : 6.1
```

**`CLAUDE.md` par.9 dice *«la barra d'errore di una pendenza è ~3 volte la `SE` interna»*. Qui è
`6.1` volte.** **Il vecchio `T3` usava la `SE` interna e dichiarava effetti a `28 sigma`: con la
barra giusta, su quattro semi, l'effetto NON si vede.**

### 4.3 `T3-bis` — **il rovesciamento del segno: RIPORTATO, non spiegato, non incorporato**

```
2026-09-15  blob 7d484580   OFF -0.1685   ON -0.4265   ON piu' LONTANO da zero (-0.258)
2026-09-17  blob 08784685+  OFF -1.7311   ON -1.2749   ON piu' VICINO  da zero (+0.456)
2026-09-19  blob b9e07c73   OFF +0.3370   ON +0.5218   segno POSITIVO, r2 = 0.031
```

**Tre blob, tre letture incommensurabili.** **Non ho una misura che lo spieghi, e non la invento.**
**E i quattro semi di oggi mostrano che parte di quella storia può essere DISPERSIONE FRA SEMI, non
evoluzione del codice:** a codice invariato le pendenze `OFF` valgono
`+0.337 / -0.950 / +0.005 / -1.059`. **Un singolo seme non poteva dirlo, e i tre numeri storici sono
tutti su UN seme.**

> **Riscrivere il criterio finché `T3` passa sarebbe aggiustare il criterio, non ripararlo.**
> **`T3` resta FAIL, e il FAIL è informativo.**

---

## 5. `T4` e `T5` — **non toccati, e passano**

```
T4   d -> 2d : 2.000000   cs -> 2cs : 0.500000   legge VECCHIA con d -> 2d : 1.000000 (resta ferma)
     PASS - tau SEGUE lo stato da solo: e' una LEGGE
T5   |nb| max scostamento da 1: 1.110e-16    NaN/inf: 0    PASS
```

**`T4` è precisamente il test «è una LEGGE o un numero travestito?», e passa in modo esatto.**
**È la ragione per cui la terza lettura del mandato NON scatta.**

---

## 6. I SIGILLI DELLA RIPARAZIONE (mandato `§1.4`)

| | esito |
|---|---|
| **`T1` byte-identità della FISICA [BLOCCANTE]** | **PASS** — `T0` misura il blob PRIMA e DOPO: `b9e07c73` / `2a7207a4` **identici**. E `git` conferma: il commit della riparazione tocca **solo** `_sigillo_tau_luce.py` |
| **`T2` il sigillo gira e dà un verdetto leggibile** | **PASS** — nessun crash, nessun FAIL falso, `exit 1` con sette verdetti espliciti |
| **`T3` e PUÒ FALLIRE: dimostralo** | **DIMOSTRATO SUL CAMPO: `T3` è FALLITO su dati veri.** Più due rifiuti cablati: sito ambiguo → `SystemExit`; contatore del discriminatore a zero → `T2` FAIL |
| **`T4` rigira i sigilli del giro** | vedi `§8` |

---

## 7. ⚠ IL COSTO — **misurato, e NON è un costo pulito**

```
TOTALE 3305 s (55 min).   T3 da solo: 2975 s (90 %).
```

**⚠ I primi ~22 minuti hanno CONDIVISO LA CPU con un rendering video** (`PID 31048`, avviato alle
`19:08:50`, fermato alle `23:45` su richiesta di Luca). **`T3` è proprio il tratto che ha subito la
concorrenza**, quindi **il `2975 s` è un limite SUPERIORE, non una misura a macchina libera.**
**Lo dico invece di spacciarlo per il costo vero.**

**E il costo è quasi tutto nel numero di semi:** `T3` fa **otto** corse da 300 passi (4 semi × 2
bracci) dove prima ne faceva **due**. **È il prezzo di `P3`, e non è negoziabile senza tornare a una
barra d'errore sbagliata.**

---

## 8. COSA QUESTO DICE, E COSA NO

**DICE:**
- **il sigillo è RIPARATO**: `T1a`, `T1b`, `T2` passano dove prima davano «nessun confronto»;
- **il cablaggio di `--tau-luce` NON cambiò il ramo OFF** — la condizione bloccante regge;
- **la riduzione al limite ORA FUNZIONA**: `0.000e+00` esatto, e prima non c'era nemmeno il confronto;
- **`--tau-luce` È una legge** (`T4`), stabile (`T5`), inerte a flag spento (`T1b`);
- **e il suo effetto sulla pendenza NON è distinguibile dal rumore fra semi su 4 semi**, con
  risoluzione `±0.84`.

**NON DICE:**
- **che `--tau-luce` sia certificato.** **Il SIGILLO COMPLESSIVO resta FAIL**, e **il gate resta a
  `c0803713`** (par.0). **Ogni referto che usa quella scena continua a ereditare il limite.**
- **che l'effetto non ci sia.** **`T3` è un NON MISURATO**, non un «nessun effetto» — la potenza del
  test con 4 semi e `std = 0.69` è bassa.
- **niente sul rovesciamento del segno.** **Riportato, non spiegato.**
- **⚠ E il costo NON è pulito**, per il rendering concorrente: va rimisurato a macchina libera se
  qualcuno vuole citarlo.


---

## 9. APPENDICE — **la voce `A` del registro PRIMA di questa riscrittura, VERBATIM**

**par.5-quater: il registro e' uno STATO, non una cronaca -- quindi la voce si RISCRIVE. Ma il testo
vecchio diceva com'era e a quale blob, ed e' un'informazione.**

```
| **A** | `--tau-luce` cablato, **SIGILLO ANCORA FALLITO**. T2 resta da riscrivere (il monkeypatch colpiva il metodo **condiviso**). T3 **rifatto oggi** dopo la cura della cache (C7), e poi **su 3 semi**: ON post medio **-0.4745** contro l'attesa **-0.69**, divario **-0.2155** a **z = 13.1**, e `theta` resta a **30.7-44.9 giri/passo**. *(La lettura intermedia «un sesto recuperato» e' stata **RITIRATA**: era dispersione di run — C10.)* `doc/SIGILLO_tau_luce_FALLITO.md`, `doc/FIX_cache_cs.md` §6 | T1-T5 tutti PASS, **e** `theta` sotto il tetto `2π·cs/λ` | **⚠ MARCATA IL 2026-09-17 — VERDETTO DA RIGIRARE PRIMA DI ESSERE CITATO:** il FAIL è del blob `7d484580` (15 set); da allora **14 commit** e **sette correzioni di legge sigillate**, e `cs_std/cs` è passato da **0.0079 %** a **11 %** — cioè il sigillo fu preso quando `d/cs` era di fatto `∝ d`. **Ma i tre FAIL non hanno la stessa natura: T2 è un difetto del TEST** (monkeypatch sul metodo condiviso) **e il rigiro non può cambiarlo**; T4 dipendeva dalla cache `_cs_nodo_prev`, **poi CURATA** (C7). → `doc/SIGILLO_tau_luce_FALLITO.md` **✅ RIGIRATO il 2026-09-17** (`doc/REFERTO_rigiro_tau_luce.md`): **T4 da FAIL a PASS** (`cs→2cs` ora **`0.500000`** esatto: la cura C7 ha funzionato, `tau = d/cs` **e' una LEGGE**); **T2 FAIL per la STESSA ragione** (difetto del test, non del codice); **T1 da PASS a FAIL** perche' il suo **riferimento e' di 15 commit fa** — **criterio SCADUTO, non regressione**; **T3 FAIL per una RAGIONE DIVERSA: l'effetto ha CAMBIATO SEGNO** (allora ON si allontanava da zero di 0.258, oggi si **avvicina** di 0.456). **L'ostacolo non cade, ma non regge piu' per le ragioni di allora.**
```

**Cosa di quel testo RESTA VERO:** che `T2` era un **difetto del TEST**; che `T4` dipendeva dalla
cache `_cs_nodo_prev` **poi curata**; che il FAIL originale era del blob `7d484580`; e il criterio di
chiusura *«T1-T5 tutti PASS»*.
**Cosa NON regge piu':** *«T2 resta da riscrivere ... e il rigiro non puo' cambiarlo»* -- **e' stato
riscritto, e ora PASSA a `0.000e+00` esatto**; e i numeri di `T3` su **3 semi** (`-0.4745` contro
l'attesa `-0.69`, `z = 13.1`) **usavano una barra d'errore sbagliata**: con la dispersione FRA SEMI
misurata qui (`0.6936`) quegli `z` non reggono.
**E il `theta` a «30.7-44.9 giri/passo» NON e' piu' vero su questo blob:** `T5` misura
`1.675e-05 gradi/passo`. **E' un riscontro separato, ed e' nel task history.**
