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

## 6-bis. IL BILANCIO DEI TASSI (2026-09-15) — **FASI A, B, C CHIUSE**, e un REPERTO

Documento: **`doc/BILANCIO_ordine_spin.md`**. Nessuna modifica al simulatore (blob `f5887254`).

**La riformulazione.** Alla mitosi il figlio eredita il padre per **copia esatta** e nasce
**adiacente**: ogni nascita crea una coppia con `chi = 0` (misurato, `0.0000` esatto). Ma `chi = 90`
ovunque. Quindi **l'ordine non manca: nasce di continuo e viene distrutto.** Non serve un meccanismo
ordinante — serve misurare il **bilancio**.

**FASE B — i due tassi** (osservatore **sigillato PASS**: 19 campi + stato RNG a `0.000e+00`, con N
confrontabile). Scena reale, 250 passi, **due semi**, 4163 coppie padre-figlio:

| | seme 1 | seme 2 |
|---|---|---|
| `tau_dec` (decorrelazione della coppia) | **0.63 passi** | **0.63 passi** |
| `tau_mit` locale (una mitosi nel vicinato) | 187 passi | 210 passi |
| rapporto | **295** | **335** |

> **`tau_dec` << `tau_mit` di quasi TRE ORDINI. Dominio della distruzione.**

**E il confondente e' ESCLUSO, non stimato.** All'eta' 1, quando `chi` e' gia' 89.7 (nullo:
90.000 +- 39.171), la **distanza e' invariata** (0.540 contro 0.539) e l'**arco diretto e' vivo al
100%**. Decorrelano **da adiacenti e connessi**: e' disordine, non disaccoppiamento geometrico.

**FASE C — l'ipotesi «dare memoria combatte il disordine» e' REFUTATA, e c'e' un reperto.**
Leggendo `omega_s` **direttamente dal simulatore**:

> **il Bloch fa ~67 GIRI COMPLETI per passo** (2.4e4 gradi/passo; 99.3% dei nodi oltre il giro
> intero). **Il settore di spin NON e' risolto nel tempo dal passo DT.**

Perche': `omega = coppia/inerzia`, la coppia e' **ordinaria** (0.06) ma l'inerzia e' la **densita'**,
che vale **1.2e-7** — sette ordini sotto l'unita'. Il pavimento `1e-6` **non e' la causa: la
mitiga** (senza, `omega` sarebbe otto volte piu' grande).

**E' la stessa radice del problema noto su `cs`**, con segno opposto: la densita' e' minuscola alle
scale simulabili, quindi **congela la metrica** (`cs` fermo a `CS_M`) **e fa esplodere lo spin**
(`omega` divisa per quella densita').

**Perche' piu' memoria peggiorerebbe:** il punto fisso del rilassamento e' `omega_eq = tau · F`,
cioe' **omega e' proporzionale alla memoria**. Il canale ha gia' la memoria piu' lunga del sistema
(2470 passi) e ruota di 67 giri per tick. La memoria vive sulla **velocita' angolare**: conserva la
rotazione, non la direzione. **Nessun canale merita piu' memoria**, e ognuno e' escluso col suo
numero (la densita': il 99.7% dei nodi e' sotto il pavimento; `cs`: fase globale, `nb` invariante a
3.3e-16, piu' l'esito B; i pesi: il campo e' al valore casuale entro il 7%).

**Cosa cambia per i sei lati.** Restano **validi** — nessuno e' invalidato. Cambia
l'**interpretazione**: non dicono «non esiste una fisica ordinante», dicono «**in questo regime
numerico nessun ordine puo' sopravvivere a un tick**». Due strade aperte, entrambe decisione di
Luca: un **sotto-passo per lo spin** (lo stesso principio di `nsub` per la metrica), oppure
**rileggere tutto dove la densita' e' O(1)**.

**Caveat:** i 67 giri/passo sono misurati a **passo 60, un seme, una scena** — vanno rifatti prima
di trattarli come stabili. `tau_dec` invece e' su due semi e 4163 coppie.

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

**Il quadro e' cambiato di natura, non di segno.**

Fino a ieri: sei misure convergenti, *"il settore di spin non ha una forza organizzante emergente"*,
e la conclusione implicita che **mancasse un meccanismo**. Da oggi sappiamo che **non manca**:
l'ordine **nasce a ogni mitosi** (chi = 0 esatto) e viene **distrutto ~300 volte piu' in fretta di
quanto nasca**. E sappiamo **perche'**: il Bloch fa **~67 giri per tick**, perche' la coppia e'
ordinaria ma l'inerzia e' una densita' di **1.2e-7**.

> **I sei lati restano validi. Cambia cio' che si puo' concludere da essi:** non *"non esiste una
> fisica ordinante"*, ma *"in questo regime numerico nessun ordine sopravvive a un tick"*.

E' la **stessa radice** del fatto gia' noto in `CLAUDE.md` §6 (*a densita' reali cs e' MORTO*): la
densita' minuscola alle scale simulabili **congela** un settore e **fa esplodere** l'altro. Un solo
problema di scala, due sintomi opposti.

**Nessun run in volo. Quattro cose aspettano te:**
1. **sotto-passo per lo spin** (lo stesso principio di `nsub` per la metrica) **oppure** rileggere
   tutto dove la densita' e' O(1);
2. il **test decisivo su `TAU_A`** che non ho fatto (cambia la fisica): verificare
   `omega_eq` proporzionale a `tau`. **`--regime` non serve**, muove quattro interruttori insieme;
3. **`_pesi()`**: FASE B non eseguita, la premessa del mandato e' falsa (`doc/REPERTO_pesi_ricorsione.md`);
4. **`:5318`**: il diaglog re-implementa `cs` inline — sotto turbo quella colonna mente.

Il **gate** e' a `c0803713` in `CLAUDE.md` §0, il blob sul disco e' **`f5887254`** (cablaggio turbo
+ i due fix). **Non ri-timbrato di proposito:** il turbo e' un ramo diagnostico, e si timbra a pezzo
compiuto. `soliton_simulator.py` **non e' stato toccato** in tutto il lavoro del bilancio.

Dettagli: `doc/ESITO_scan_turbo_K300.md`, `doc/REPERTO_pesi_ricorsione.md`,
`doc/PROFILAZIONE_costo_run.md`, `doc/REPERTO_gamma_condiviso.md`, `doc/PREDIZIONE_*.md`,
`doc/AUDIT_misurato_vs_asserito.md`, `STATO_CLAUDE_fork-su2.md`, `CLAUDECONNECT.md`.
