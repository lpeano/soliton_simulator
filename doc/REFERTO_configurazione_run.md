# REFERTO — **LA CONFIGURAZIONE CON CUI I RUN HANNO GIRATO**

> **Punto (1b) del prompt unico di Luca, 2026-09-24.** Le risposte vengono **dalla tabella generata**
> (`csv/_test_fork/_RICOSTRUZIONE_config.txt`), **non a memoria**.
> Strumenti: `csv/_configurazione.py` *(da ora in avanti)* e
> `csv/_test_fork/_ricostruisci_config.py` *(per i run già fatti)*.

---

## 1. I SETTE FLAG, PER OGNI RUN

**Il valore è lo stesso su tutte le campagne ricostruite.** Riporto il valore e **da dove
viene**, perché la fonte cambia il peso della risposta.

| flag | valore | **fonte** | campagne |
|---|:--:|---|---|
| `CAMPO_SPINORIALE` | **`True`** | **banner** *(stato effettivo dal modulo)* | 10 su 11 |
| `SPINORE_VIVO` | **`True`** | **banner**, e il **default è già `True`** | 10 su 11 |
| `SPINORE_CORRETTO` | **`True`** | **banner** | 10 su 11 |
| **`TEMPO_SEGNO`** | **`False`** | default del sorgente al commit **+ `--tempo-segno` ASSENTE da ogni lanciatore committato** | 9 su 11 |
| `SCALA_MIN` | **`False`** | **banner** | 8 su 11 |
| `SCALA_MIN_PASSO` | **`True`** | **banner** | 8 su 11 |
| **`TW_SPINORE`** | **`False`** | default del sorgente al commit **+ `--tw-spinore` ASSENTE da ogni lanciatore committato** | 9 su 11 |

> ### ⚠ **E `TW_SPINORE` è `False` IN OGNI RUN, il che chiude una domanda e ne apre un'altra.**
> **Chiude:** il fronte `W` del registro dice che `TW_SPINORE` ha un **commento falso**
> *(dichiara di pilotare il Bloch di `tw/2`, cioè un ANGOLO, mentre il codice somma
> `tw/(4π)` a una VELOCITÀ angolare — fattore `628.3 = 2π/DT`)*. **Nessuna misura di
> questo programma è stata contaminata da quella legge: non ha mai girato.**
> **Apre:** è il caso **INVERSA** della mappa del `4π` — *la torsione che pilota il
> Bloch*, cioè il `4π` **finto** che comanda il `4π` **vero**. È spento **oggi**, e
> l'architettura a un solo ponte deve dire **se può esistere affatto**.

**Le celle che mancano sono dichiarate, non dedotte:**

- **`G3 controllo` e `G4 controllo`** non lasciano snapshot *(il `G4 controllo` cancella i suoi
  `.pkl.gz` a ogni giro: è **scratch**)*, quindi non hanno un commit da cui leggere i default.
  Per loro valgono i **24 flag del banner** e nulla più → `TEMPO_SEGNO` **NON RICOSTRUITO**;
- **`validazione 600`** non ha banner nel suo log, e per i flag che un'opzione **può** cambiare
  il default del sorgente **non basta** → **NON RICOSTRUITO**, non «probabilmente come gli altri»;
- **`G1` e `G2`** hanno un banner di **15** flag, non 24: il banner è una **lista a mano** nel
  driver, ed è cresciuta nel tempo. `SCALA_MIN`/`SCALA_MIN_PASSO` **non esistevano** allora.

> ### ⚠ **`SPINORE_CORRETTO` È `True`, NON `False`.**
> Il **default nel sorgente è `False`**, ma il driver cabla **`--spinore-corretto`** in
> `sys.argv` (`csv/_test_fork/_scena_video.py:187`). **La lettura «`SPINORE_CORRETTO` spento»
> era sbagliata**, e l'errore è esattamente quello che il referto di configurazione esiste per
> impedire: **chi legge il sorgente conclude il contrario di chi legge il run.**

> ### ⚠ **`SPINORE_VIVO` È `True` PER DEFAULT, non per l'argv.**
> Il driver passa **anche** `--spinore-vivo`, ma il default di modulo è **già** `True`. Chi lo
> spegnesse togliendo il flag dal driver **non otterrebbe nulla**: servirebbe
> `--senza-spinore-vivo`. È la stessa trappola di `STEP2_OROLOGIO` *(par.9: «un default
> ribaltato converte i rami di controllo in duplicati del ramo di prova»)*.

---

## 2. `--scala-min=off` IN `COMUNE`: **IL FRENO ERA ATTIVO**

**Sì, il freno girava** — e non tramite `SCALA_MIN`, ma tramite **`SCALA_MIN_PASSO`**, che è
`--scala-min-passo=on` nello stesso `COMUNE`.

### LE CONDIZIONI DEL SORGENTE, citate

| riga | condizione | cosa decide |
|---|---|---|
| **`:3657`** | `_lam_attivo = SCALA_MIN or SCALA_MIN_PASSO` | la **guardia degli invarianti** considera attiva la scala minima |
| **`:3800-3805`** | `if SCALA_MIN_PASSO: return dx` · poi `if not SCALA_MIN: return dx` | la **singola scrittura NON si frena**: è **passante** |
| **`:3781-3790`** | `if not SCALA_MIN_PASSO: return` · poi `self.d0 = v + self._smorza(v, dx, 'd0_passo')` | **il freno si applica UNA VOLTA per passo**, sulla variazione **totale** |
| **`:3811`** | `if SCALA_MIN or SCALA_MIN_PASSO: return v` | **il pavimento `_floor_d0()` SPARISCE** |
| **`:3821`** | `if not (SCALA_MIN or SCALA_MIN_PASSO): return v` | alla **nascita** il troncone si porta **a `LAM`** |

**È un `or` in quattro punti su cinque:** con `SCALA_MIN = False` e `SCALA_MIN_PASSO = True` la
scala minima è **attiva in tutto**, e l'unica cosa che `SCALA_MIN` da solo governa è **il
frenare scrittura per scrittura** — che `C3` ha sostituito **di proposito**, perché frenare a
ogni scrittura fa dipendere il risultato **dall'ORDINE** delle leggi.

### I CONTATORI, dal riferimento a 600 passi

| contatore | valore | cosa dice |
|---|--:|---|
| `_g_smp_chiusure` | **`600`** | il freno si è chiuso **una volta per passo**, 600 passi |
| `_g_sm_d0_passo` | **`600`** | `_smorza` chiamato con `'d0_passo'` 600 volte |
| `_g_smp_passanti` | **`3596`** | scritture **non frenate** singolarmente: la cura `C3` funziona |
| `_g_sm_pav_saltati` | **`3596`** | il pavimento `_floor_d0()` **salta**, come `:3811` prescrive |
| `_g_sm_nascite` | **`604`** | il troncone a `LAM` alla nascita **si applica** |
| `_g_smp_discese` / `salite` | `154 197 389` / `161 637 017` | il freno morde **solo** le discese |
| `_g_smp_nulli` | **`0`** | `dx == 0` **non capita mai** su 526 mila archi: il ramo «somma nulla» del docstring **è teorico** |

### IL TERMINE DEL FRENO NEI BILANCI, e **il segno è il punto**

| run | `freno` | quota di `Δ(Σd0)` |
|---|--:|--:|
| `G4` riferimento | **`+2.032480e+06`** | **`+117.41 %`** |
| `G4` spegni *(`MEM_MOTO=False`)* | `+1.419938e+06` | **`+218.33 %`** |
| `G4-bis` *(blocco intero)* | `+1.634679e+06` | **`+178.09 %`** |
| `D34` ritmo-wrap | `+2.068902e+06` | **`+105.60 %`** |
| `FASE_2PI` corto | `+3.226687e+05` | **`+186.77 %`** |

**Il termine è POSITIVO in tutti e cinque, e vale più del `Δ` totale.** Un *freno* che
**aggiunge** lunghezza non è un freno: è un **motore**. **È `D31`**, e il bilancio lo misura
in ogni braccio.

---

## 3. COSA SIGNIFICA PER `D31`

**`D31` si applica a tutti i run, e non era in dubbio: ora è documentato.**

- il freno **girava** in ogni campagna `G3`/`G4`/`D34`/`FASE_2PI`, via `SCALA_MIN_PASSO`;
- `Z113` lo **dimostra sulla formula** *(`4/4`, deriva `+1.582064e-03` contro l'attesa derivata
  `+1.582007e-03`, scarto `0.0 %`)*, quindi non dipende dalla configurazione;
- **la configurazione conferma che la dimostrazione è PERTINENTE**: il cricchetto non era una
  proprietà di un ramo spento.

> **⚠ E UNA COSA CHE QUESTO REFERTO *NON* DICE:** che `C3` *(il freno una volta per passo)* sia
> la causa del cricchetto di **verso**. **Non lo è:** `C3` cura il cricchetto **d'ORDINE**
> (`Z91`), e `Z113` dimostra che quello **di VERSO** sopravvive. **Sono due difetti diversi
> nello stesso punto**, e `SCALA_MIN_PASSO` acceso cura il primo lasciando il secondo.

## 4. COSA SIGNIFICA PER IL BILANCIO DI `Z108` / `Z113`

**Il bilancio misura il freno GIUSTO, e si verifica dal sorgente.**

`_freno_passo` chiama **`self._smorza(v, dx, 'd0_passo')`** (`:3790`), e l'involucro di
`_g4_prova.py` conta **solo `d0_passo`** — *«le altre chiamate stanno dentro siti già tracciati
e si conterebbero due volte»*. Quindi:

- il termine `freno` del bilancio **è** il freno di `SCALA_MIN_PASSO`, **non** quello
  per-scrittura di `SCALA_MIN` (che era **spento** e comunque **passante**);
- `_g_sm_d0_passo = 600` = `_g_smp_chiusure = 600`: **una chiamata per passo, nessuna
  doppia contabilizzazione**;
- **il bilancio chiude** in tutti i bracci *(`9.595e-14` in `D34`, `4.041e-14` in `FASE_2PI`
  corto)*, e chiudere con un termine misurato al posto sbagliato sarebbe stato improbabile,
  ma **ora non è più un argomento di plausibilità: è una lettura del sorgente.**

> **Conclusione per `Z108`/`Z113`: reggono, e la configurazione è quella che credevano.**
> **Non era verificato prima di adesso**, ed è l'unica cosa che cambia.

---

## 5. COSA RESTA NON RICOSTRUITO, e perché

> **⚠ E UNA PRECISAZIONE DI NOMENCLATURA, chiesta da Luca:** dove il referto generato dice **«default del sorgente AL COMMIT `<hash>`»**, quell'hash è un **COMMIT**, non un blob. `git cat-file -t` su un timbro del presidio risponde **`Not a valid object name`**, perché quel numero **non è un oggetto git**. Accanto, per leggibilità, c'è lo `sha1` del simulatore — **e il referto dice QUALE delle due convenzioni è**: `sha1 byte GREZZI, dal log` *(quello che i CSV citano, l'unico che vede la trappola CRLF)*, oppure `sha1 del CONTENUTO git, forma LF`, che **non è il byte-grezzo se il disco era CRLF**.

| cosa | perché |
|---|---|
| `TEMPO_SEGNO`, `SCALA_MIN`, `SCALA_MIN_PASSO`, `OROLOGIO_SEGNO` per **`G3 controllo`** e **`G4 controllo`** | **nessuno snapshot** → nessun commit da cui leggere i default. Il `G4 controllo` è scratch **per progetto** |
| i flag argv-dipendenti per **`validazione 600`** | **il suo log non porta il banner**, e il default del blob non basta per un flag che un'opzione può cambiare |
| **99 flag su 123** per ogni run vecchio | il banner ne stampa **24**. Per gli altri la fonte è il **default del blob**, e vale **solo** dove l'opzione è assente dai lanciatori — verificato caso per caso, ma **più debole** |

**Da ora in avanti niente di tutto questo serve:** ogni run scrive
**`CONFIGURAZIONE.txt`/`.json`** con **tutti i 123**, letti **dal modulo**, e **il driver
rifiuta di partire** se non riesce a scriverli.
