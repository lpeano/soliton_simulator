# RELAZIONE — per Claude web, 2026-09-14 (aggiornata: **scan K=300 CHIUSO, esito B**)

> **Scritta per Claude web**, che legge il repo e deve pronunciarsi su una decisione di merito.
> Branch `fork-su2`. Sostituisce la versione precedente, che si fermava a «scan in volo».

---

## 1. IN UNA RIGA

> **Lo scan del turbo è chiuso: ESITO B.** Con `cs` forzato fino al **5 % di `CS_M`**, lo Step 2
> **non muove lo spin**: i due bracci sono indistinguibili su tutte e tre le firme.
> È il **sesto lato** dello stesso fatto. **Lo scan ai K minori si ferma qui**, risparmiando
> ~40 ore di macchina.

Documento del verdetto: **`doc/ESITO_scan_turbo_K300.md`** — con i dati committati accanto.

---

## 2. IL VERDETTO — i numeri, contro la predizione scritta PRIMA

Due bracci, seme 1, 2000 passi, `exit = 0`, **un solo interruttore di differenza**
(`--step2-orologio`). Tutto il resto identico, verificato dal blocco `# RUN_PARAMS` dei CSV — non
dalla memoria.

**Il forcing ha morso, molto oltre il bersaglio:**

| | `cs_min / CS_M` finale |
|---|---|
| Step2 ON | **0.047** |
| Step2 OFF | **0.032** |

Il bersaglio era «almeno il dimezzamento». Siamo a **un ventesimo**. Traiettoria: 2.000 → 0.610
(passo 400) → 0.204 (1000) → 0.095 (2000).

**E le firme non si muovono lo stesso** (medie su 20 campioni, gradi):

| firma | ON | OFF | nullo casuale |
|---|---|---|---|
| `chi` materia | **89.9865** | **89.9941** | **90.000** |
| dispersione | 39.199 | 39.196 | **39.171** |
| `chi` **p90** (archi più densi) | **90.0309** | **89.9609** | 90.000 |
| \|⟨n⟩\| in unità di 1/√N | 0.83 | 1.00 | ~1 |

La differenza fra i bracci sulla firma principale è **0.008°** contro una dispersione di **39.2°**.

**Terza firma, quella che discrimina** — autocorrelazione spaziale su 14 bin
(`csv/_test_fork/_autocorr_k300.txt`):

| | vicino | lontano |
|---|---|---|
| ON | −0.0200 | 0.0032 |
| OFF | 0.0148 | 0.0014 |

**Piatta a zero ovunque, in entrambi.** Il segno del "calo" è addirittura **opposto** fra i due:
è rumore di campionamento, non struttura. **Nessuna scala di dominio.**

| esito predetto | misurato |
|---|---|
| **A** struttura (`chi` intermedio, autocorrelazione che decade) | no |
| **B** il chiuso regge | **SI** |
| **C** artefatto solo a K estremo | no — non c'è **nessun** effetto da estrapolare |

---

## 3. PERCHÉ LO SCAN SI CHIUDE (la logica dichiarata prima, non dopo)

> Se al forcing **massimo** le firme sono piatte, l'esito B è indicato e i K minori sono superflui:
> nessun effetto a K=300 implica nessuno a K minori.

Questa asimmetria era **scritta e approvata prima di partire**, ed è la ragione per cui ho iniziato
da K=300 invece che dal basso. Ha fatto il suo lavoro: **un quarto del costo**, stessa conclusione.

---

## 4. IL SESTO LATO

| # | misura | esito |
|---|---|---|
| 1 | teorema di inerzia (Strato 0) | la connessione è uno **specchio** della materia — 1.57e-15 |
| 2 | frozen-o-noise | ciò che rispecchia è **rumore** |
| 3 | Kuramoto | refutato — K-frozen **byte-identico** a OFF; K-noise = NO-rumore |
| 4 | FDT | `E[n'] - n = -a^2 n`, **dimostrato**, verificato a 1.28e-07 |
| 5 | shake-then-freeze | `chi` deriva di **−0.33°** in 600 passi da stato casuale |
| 6 | **Step 2 con `cs` vivo** | **nessuna differenza ON/OFF a `cs/CS_M = 0.047`** |

Sei misure indipendenti, **un solo fatto**: il settore di spin non ha una forza organizzante
emergente, e **non ne acquisisce una** agganciando l'orologio alla metrica.

---

## 5. I DUE CAVEAT, INTERI — quello che il verdetto **non** dice

**1. Un solo seme.** `CLAUDE.md` §2.7: nessuna conclusione su un solo seme. Questo è **screening**,
legittimo come tale, **non** un fatto pubblicabile. Un secondo seme costa ~1.7 h per braccio.

**2. Il turbo ristretto è un ISOLAMENTO DIAGNOSTICO, non il regime reale.** `GAMMA` è **condiviso**
fra `cs`, `satura()` e la saturazione del campo spinoriale. Restringerlo a `_cs_nodo` **rompe di
proposito** quella condivisione; nel regime reale ad alta densità cambierebbero **entrambi**.

> La formula onesta: **«il gradiente di cs, IN ISOLAMENTO e fino al 5 % di CS_M, non retroagisce
> sullo spin»** — un **condizionale**.

E vale in entrambe le direzioni: **un negativo in isolamento è più debole, non più forte**, di un
negativo nel regime vero. Non prova che nel regime reale non succeda nulla; prova che **questo
canale, da solo, non basta**.

**3. Una correzione a me stesso.** Nella versione precedente di questa relazione avevo scritto che
nel braccio OFF le colonne `cs_*` sarebbero state `NaN`. **Falso:** entrambi i bracci hanno
`--fork-su2-mem`, che scrive `_cs_nodo_prev`, quindi `cs_*` è popolato in tutti e due — ed è
proprio da lì che vengono i numeri del §2.

---

## 6. DUE COSE CHE ASPETTANO UNA TUA DECISIONE

### 6.1 `_pesi()` — la premessa del mandato di ottimizzazione è falsa

FASE A fatta, **FASE B non eseguita**, come prescrive il mandato (se la premessa non regge,
fermati). Documento: **`doc/REPERTO_pesi_ricorsione.md`**.

Le 16 chiamate per passo **non** sono ricalcoli ridondanti di `calcola_psi()` (quello è il
**12.8 %**). L'**80.9 %** passa da `stato_crossover()` via `massa_critica_adattiva()`, e il
**43.6 %** è **`_pesi()` che chiama se stessa** un livello più sotto:

```
_pesi -> _lam_archi -> lambda_nodi -> massa_critica_adattiva -> stato_crossover -> _pesi
```

Il ciclo non è infinito perché `lambda_nodi` ha già la guardia `_calcolo_schermatura`, che nel ramo
rientrante restituisce **LAM costante** invece della schermatura vera. **Quindi le due `_pesi()`
calcolano cose diverse**, e cachearne una per l'altra non romperebbe l'ultimo bit: **cambierebbe la
schermatura**. Tre strade nel documento, §5. **Non ho scelto e non ho toccato niente.**

### 6.2 `:5318` — un diagnostico che non segue la fisica

Il diaglog **re-implementa `cs` inline** e non chiama `_cs_nodo`: **sotto turbo quella colonna
mente**. Dichiarato e non risolto (la tua indicazione era «applicazione UNICA»). I numeri di questa
relazione **non** vengono da lì: vengono dall'osservatore, che legge `_cs_nodo_prev`, il `cs` vero.

---

## 6-bis. APERTO DA OGGI (2026-09-15) — la riformulazione: **un bilancio, non un meccanismo mancante**

Documento: **`doc/BILANCIO_ordine_spin.md`**. **FASE A chiusa, B e C da fare.**

Dal codice e' emerso un fatto che **cambia la domanda**: alla mitosi il figlio eredita il padre per
**copia esatta** (`_nb`, `_psi_spinor`, `omega_s`, `_nb_ret`, `_psi_prec` — nessun jitter), e nasce
**adiacente** nello spazio e nella topologia. Quindi **ogni nascita crea una coppia con chi = 0**
(misurato: `0.0000` esatto). Ma la misura dice `chi = 90` ovunque.

> **L'ordine non manca: nasce di continuo e viene DISTRUTTO.** Non serve cercare un meccanismo
> ordinante (la strada che porterebbe a *imporre* un Kuramoto, gia' refutato): serve misurare il
> **bilancio fra due tassi gia' presenti** — la mitosi che crea, il rumore + la precessione mutua
> che distruggono.

**Il numero che mi ha sorpreso**, e che va rifatto prima di crederci: nello **stesso passo** in cui
nasce il figlio, il **padre** si sposta di **85.6 gradi in media** (mediana 95.8). Il Bloch
decorrela **da se' stesso in un tick**, cioe' e' gia' sul valore-null. Se regge sulla statistica,
`tau_dec` e' inferiore al passo e il bilancio e' dominato dalla distruzione. **Ma sono 7 campioni:
un indizio, non un risultato.**

**Due cose gia' utili per chi legge:**
- l'**antinodo** Schwinger eredita `-psi`, ma `nb = psi^dag sigma psi` e' invariante per fase
  globale: **anche l'antinodo nasce con chi = 0 in Bloch.** «Antichirale» riguarda il segno di
  doppia copertura, non la direzione.
- sotto `--spinore-corretto` il rumore **non** perturba il Bloch direttamente (quel ramo e' gated su
  `SYNC_UPDATE`, spento): entra **solo** via `cross(B, nb) -> omega`. E' **rumore di COPPIA**, e
  `omega_s` **ha gia' memoria** (`TAU_A`). Un canale che la memoria ce l'ha, e resta disordinato.

---

## 7. IL LAVORO DI CONTORNO, in breve

- **Profilazione** (`doc/PROFILAZIONE_costo_run.md`): il collo **non** è il loop CFL. I due hoist
  autorizzati non valgono la pena, e **non sono stati applicati**. La leva vera è `nsub`, cioè la
  **scala**, non il codice. Corollario da tenere: **il costo È il segnale** — forzare `cs` basso è
  caro *perché* è lontano dal regime naturale.
- **Fix critico** (`cda0931`): il guard di `--gamma-turbo` leggeva `CS_DINAMICO` **prima** che
  fosse assegnato, quindi **turbo sempre spento**, con un avviso che **diceva il falso**. Bug mio,
  e il **terzo** della stessa famiglia (leggere un flag prima dell'assegnazione, come il falso O3c).
  **L'ha visto Luca, non io.** Il primo run K=300 girava a K=1: **buttato**, non riciclato. Il
  presidio non è «ricordarsi l'ordine» ma **non dipendere dall'ordine**: leggere dagli argomenti.
- **Osservatore incrementale** (`ee21618` + `646116f`): senza scrittura incrementale un run lungo
  non è troncabile sull'evidenza. Il primo tentativo scriveva **prima** che la riga fosse completa:
  CSV troncato. Bug mio, corretto.

---

## 8. DOVE SIAMO

**Chiuso come negativo pulito, sei lati.** Lo scan del turbo era l'ultimo punto aperto e ora è
chiuso. **Non c'è un run in volo.**

Il **gate** è a `c0803713` in `CLAUDE.md` §0, mentre sul disco il blob è **`f5887254`**: la
differenza sono il cablaggio del turbo e i due fix. **Non ri-timbrato di proposito**, per non
timbrare a metà; da ri-timbrare a pezzo compiuto.

Dettagli: `doc/ESITO_scan_turbo_K300.md`, `doc/REPERTO_pesi_ricorsione.md`,
`doc/PROFILAZIONE_costo_run.md`, `doc/REPERTO_gamma_condiviso.md`, `doc/PREDIZIONE_*.md`,
`doc/AUDIT_misurato_vs_asserito.md`, `STATO_CLAUDE_fork-su2.md`, `CLAUDECONNECT.md`.
