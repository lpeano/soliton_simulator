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

## 6-ter. GILBERT / FDT (2026-09-15) — **ipotesi NON confermata, nessun cablaggio**

Documento: **`doc/ANALISI_gilbert_fdt.md`**. Mandato: *il termine mancante e' lo smorzamento di
Gilbert, e il FDT ne fissa il coefficiente?* **Testato. Cade — e cade prima della derivazione.**

**Due premesse del mandato sono COMMENTI STALE.** E' il caso d'uso di §0:
- *"`omega_s` e' conservativo: si conserva, non rilassa"* (righe **868** e **1803**) -> **FALSO**.
  L'unico aggiornamento per passo e' la riga **1918**, che contiene `- omega_src/_tau`:
  **la dissipazione c'e' gia'.**
- *"il calcio termico alimenta `omega_s`"* (riga ~1590) -> **FALSO**: e' dentro `semina()`, quindi e'
  il punto zero **alla nascita del nodo**, non una sorgente per passo.

Quindi lo schema *"accumulatore conservativo + rumore che lo alimenta = crescita illimitata"*
**non descrive questo codice**: mancano entrambi i pezzi.

**E la crescita non e' quella che avevo dedotto nemmeno io.** Da un solo campione avevo inferito
crescita *balistica*; ho misurato la traiettoria **prima** di scrivere il verdetto (150 passi, 15
punti) ed e' **DIFFUSIVA**: `omega/sqrt(n)` costante entro il **4.6%**, `omega/n` varia di 3.5x.

**E c'e' un PLATEAU.** Random walk smorzato, `omega_eq = sigma*sqrt(tau/(2 dt))`:

| | |
|---|---|
| previsto | **7.06e4** |
| misurato al passo 150 | **7.27e4** (scarto x1.03) |
| theta al plateau | **112 giri per passo** |

> **La dissipazione non manca: c'e', funziona, e un equilibrio finito lo produce gia'.**
> Il problema e' *dove* sta quel plateau — e dipende dall'**ingresso** (coppia/inerzia), non
> dall'uscita. **La diagnosi corretta resta l'inerzia a 1e-7.**

**Il coefficiente si deriva davvero, e a zero parametri.** Dal rumore sul Bloch: `D = 2 amp^2/dt`;
imponendo che l'equilibrio di Langevin coincida con quello di Boltzmann,
`lambda = amp^2 |B| / (2 dt kT)`. Con l'unica temperatura parameter-free (`kT = Lam`, l'energia del
vuoto da cui il rumore stesso e' costruito) **`Lam` si cancella**: `lambda = |B|/(2 dt)`.

| tempo | valore |
|---|---|
| `tau_smorzamento` (allineamento FDT **derivato**) | **28.8 passi** |
| `tau_disordine` (rimescolamento **misurato**) | **0.0030 passi** |

> **Terzo ramo della regola scritta prima: lo smorzamento FDT e' ~10^4 volte troppo lento.
> REPERTO, non fallimento.** La FASE 2 **non e' partita**.

**Controllo di consistenza:** l'equipartizione darebbe `kT = 800` contro `Lam = 4.4e-5` — rapporto
~2e7. **Non e' equilibrio termico ma dinamico pilotato**, ed e' la ragione strutturale: il FDT
accoppia una dissipazione a una **fluttuazione**, e qui il termine dominante non lo e'.

**Non e' un fallimento dell'idea di Gilbert:** il termine LLG resta l'**unico** che allinea. Cade il
fatto che il suo coefficiente FDT basti *a questa scala*. Metterne uno piu' grande sarebbe
**sceglierlo** (§3) e mettere dissipazione senza fluttuazione: lo stesso errore, ribaltato.

**Una correzione a un fatto MIO.** `CLAUDE.md` §9 diceva (scritto da me ieri)
`omega_eq = tau * coppia/inerzia`, proporzionale a `tau`: e' il punto fisso **deterministico**, e
sovrastima di ~20x. **Corretto in §9**: `omega_eq ~ sqrt(tau)`. La conclusione operativa resta
(piu' memoria = piu' rotazione), ma l'esponente era sbagliato e la diagnosi *"manca la
dissipazione"* era **falsa**.

---

## 6-quater. `inerzia`: MASSA o FRAZIONE? (2026-09-15) — **FASE A chiusa: nessuna delle due**

Documento: **`doc/INERZIA_massa_o_frazione.md`**. Prima relazione scritta sotto la regola nuova
**§5-ter** (a ogni riscontro, una relazione, subito).

Il mandato chiedeva di scegliere fra due ipotesi su `inerzia = |Psi|^2`: **frazione normalizzata**
(scala come 1/N) o **massa vera**. **Dal codice non e' ne' l'una ne' l'altra.**

- **Non e' normalizzata.** `F = mat(w) @ (1.0 * e^{i phi})` e' una **somma pesata sui vicini**: non
  c'e' divisione per `N`, non esiste alcun vincolo `sum|psi|^2 = cost` in tutto il file, e `satura`
  e' un **tetto morbido** (asintoto `1/GAMMA = 20`), non una normalizzazione. Il codice prevede il
  **contrario** della firma (1): `|psi|` dovrebbe **crescere** col numero di vicini.
- **Non e' una massa.** `inerzia = max(_rho_sorgente(), 1e-6)` (riga **1891**) e' **letteralmente**
  il modulo quadro del campo: nessuna massa, nessun volume, nessun fattore. Solo il floor.

**E allora perche' vale 1e-7? L'ETA', non la normalizzazione.** In `_pesi()`:
`ramp = min(1, eta/TAU_A)`, con `eta += dt_n` (~0.01) per passo e **`TAU_A = 50`** nel regime
deterministico, quindi un nodo raggiunge **peso pieno solo dopo ~5000 passi**. Al passo 150
`ramp ~ 0.03`, e `w` va come `ramp_i*ramp_j ~ 9e-4`. **E i figli della mitosi nascono con `eta = 0`**,
quindi una frazione stabile della popolazione resta **permanentemente immatura**. Coerente con la
crescita gia' misurata di `Lam`: **7.45e-14 al passo 1 -> 1.32e-4 al passo 150**, nove ordini in 150
passi. Il campo **si sta accendendo**, non e' a regime.

**IL REPERTO — l'analisi dimensionale.** `w`, `F`, `psi`, `|psi|^2`, `B`, `nb`, `cross(B,nb)` sono
**tutti adimensionali**, quindi **`correzione/inerzia` e' adimensionale**. Ma la riga **1918** e'
`omega += dt_n*(correzione/inerzia - omega/tau)` e `theta = |omega|*dt_n` deve essere un **angolo**:
servirebbe **`[correzione/inerzia] = 1/T^2`**. In un corpo rigido `dw/dt = tau/I` lo da' **da se'**,
perche' coppia e momento d'inerzia portano entrambi `M L^2`. Qui il numeratore e' un puro prodotto
vettoriale geometrico e il denominatore una pura intensita' di campo.

> **Onestamente:** `CLAUDE.md` dice che `DT` e' un **contatore di tick**, quindi il modello potrebbe
> lavorare di proposito in unita' adimensionali, e allora non c'e' un "errore" da dichiarare. Ma
> resta la conseguenza: **non c'e' protezione dimensionale, e il valore di `omega` e' libero.**
> Nulla lo lega a una frequenza propria del modello (`cs/LAM`). Il "4000x il tetto di Planck" non e'
> un'affermazione fisica: **nel rapporto non c'e' alcuna scala di frequenza.** Ed e' anche il motivo
> per cui **riparametrizzare non puo' aiutare**: non ci sono unita' da riscalare.

**Per la FASE B cambia la variabile.** Il mandato chiede l'istogramma contro `N`; la lettura dice che
la variabile giusta e' **`|Psi|^2` contro `eta`** (l'eta' del nodo). Se i piccoli sono i **giovani**,
il `1e-7` e' **maturazione**, non normalizzazione — transitoria, se non fosse che la mitosi la
rigenera. Faro' entrambe, dichiarando la stratificazione per `eta` come **quarta firma**, aggiunta.

**FASE B e C non fatte.** Nessun run lanciato per la FASE A: e' sola lettura del sorgente.

---

## 6-quinquies. `inerzia` e' un **TEMPO^2** (2026-09-15) — la lettura di Luca chiude il buco

Documento: **`doc/INERZIA_tempo_quadro.md`**. Relazione dovuta per **§5-ter**.

Avevo riportato un buco dimensionale: `correzione/inerzia` e' adimensionale, ma la riga 1918
richiede `1/T^2`. **La lettura di Luca lo chiude esattamente**, e discende dal principio fondativo
(§8: *"lo spinore E' il tempo proprio della massa"*): se `Psi` porta **tempo**, allora
`[inerzia] = [|Psi|^2] = T^2` e `[correzione/inerzia] = 1/T^2`. **La massa e' il modulo quadro di un
tempo proprio.** Non e' una toppa: chiude al primo colpo, senza coefficienti.

**QUALE tempo — e il codice lo decide.** NON l'orologio `dt_n = DT*r`, perche' `r` e' **derivato da
`Psi`** (`ritmo()`: `a = angle(psi) - angle(psi_prec)`): sarebbe **circolare**. Resta il tempo
**metrico**, l'unico definito indipendentemente da `Psi`.

**DA DOVE entrerebbe — un solo slot.** In `F = mat(w) @ (amp * e^{i phi})`: `w = exp(-d/lam)*ramp*ramp`
e' l'esponenziale di **rapporti**, `e^{i phi}` e' una fase. **L'unico slot e' `amp`** (riga 2176),
oggi la costante `1.0`.

**L'ESPONENTE, derivato.** Il solitone ha lunghezza d'onda ~`LAM` e le onde viaggiano a `cs`, quindi
il suo periodo proprio e' `T_j = LAM/cs_j` — grandezze **gia' nel sistema**. Se l'ampiezza di
emissione e' il tempo proprio dell'emettitore:

> **inerzia ∝ cs^(-2)   <=>   omega = coppia/inerzia ∝ cs^2**

**IL TEST DEL VERSO PASSA, e non per costruzione.** Nei pozzi `cs` e' piccolo -> inerzia grande ->
omega piccola -> **la materia densa ruota piu' lentamente**. E' il verso del redshift
gravitazionale, ed e' **lo STESSO esponente dello Step 2** gia' cablato e **sigillato 10/10**
(`omega_clk *= (cs/CS_M)^2`), che fu derivato **prima** e **indipendentemente** dall'orologio di
Compton. Due canali indipendenti — la **massa** e l'**orologio** — danno lo stesso `omega ∝ cs^2`.
**Non e' una coincidenza costruita: e' una consistenza trovata.**

**ESITO (b): IL FATTORE MANCA.** Ricerca esaustiva: **zero** occorrenze di `cs` in `calcola_psi`,
`_pesi`, `_lam_archi`, `lambda_nodi`, `_rho_sorgente`, `satura`. La dipendenza **implicita** via `d`
esiste (l'onda metrica muove `d`) ma **non puo' essere quella derivata, per costruzione**:
`exp(-d/lam)` e' adimensionale **qualunque cosa faccia `d`**. **Esito (c) escluso rigorosamente.**
**Non l'ho cablato:** sarebbe un pezzo, con flag e sigilli, e la decisione e' di Luca.

**DA SAPERE PRIMA DI DECIDERE:** a densita' attuali `cs ~ CS_M`, quindi il fattore varrebbe una
**costante** (`LAM/CS_M = 0.4`, inerzia x0.16). **NON risolverebbe il `1e-7`**, che resta **ETA'**.
Due cose separate, tenute separate.

**IL COSTO DELLA LETTURA, dichiarato.** Chiude il buco a 1918 ma **ne apre due** altrove: riga
**1847** somma `amp ~ T` a un **versore adimensionale**; `scuoti_vuoto` (riga **534**) somma `T` a
`phivel ~ 1/T`. E una che c'era gia' sotto **entrambe** le letture: `lambda_nodi` confronta `|psi|^2`
con un **conteggio per volume**. **Il modello non e' dimensionalmente chiuso in nessuna delle due
letture.** La lettura di Luca chiude quello che conta di piu' — il buco che produce i 112 giri — ma
non e' globalmente consistente com'e' il codice oggi.
**A favore**, pero': sotto la lettura `GAMMA ~ 1/T` **coerentemente in tutti e tre** i suoi usi
(`satura`, `cs`, `psi_spin`), coerente col fatto gia' registrato che sia **condiviso**.

**PISTA REGISTRATA, NON APERTA:** se il fattore c'e', **`cs` entra nello spin ATTRAVERSO LA MASSA**,
non attraverso l'orologio — e **nessuna delle sei misure lo esclude**, perche' tutte riguardavano lo
Step 2 (fase globale, Bloch invariante a 3.3e-16). Mai testato.

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

**Il quadro e' cambiato di natura, non di segno — e ora sappiamo anche cosa NON e'.**

L'ordine di spin **non manca**: nasce a ogni mitosi (chi = 0 esatto) e viene distrutto ~300 volte
piu' in fretta di quanto nasca. Il meccanismo e' che il Bloch fa **~67-112 giri per tick**, perche'
la coppia e' ordinaria ma l'inerzia e' una densita' di **1.2e-7**.

E oggi si e' chiusa anche la prima ipotesi di cura: **non e' dissipazione mancante.** La
dissipazione c'e' (riga 1918), e' efficace, produce gia' un plateau — e il plateau e' comunque
aliasato. Il coefficiente di Gilbert derivato dal FDT e' **10^4 volte troppo lento**.

> **I sei lati restano validi. Cambia cio' che si puo' concludere da essi:** non *"non esiste una
> fisica ordinante"*, ma *"in questo regime numerico nessun ordine sopravvive a un tick"*.
> E ora sappiamo che **non si aggiusta aggiungendo attrito**: si aggiusta sulla **scala**.

E' la **stessa radice** del fatto gia' noto in `CLAUDE.md` §6 (*a densita' reali cs e' MORTO*): la
densita' minuscola alle scale simulabili **congela** un settore e **fa esplodere** l'altro. Un solo
problema di scala, due sintomi opposti — e ora anche una cura esclusa.

**Nessun run in volo. Cinque cose aspettano te:**
1. **alzare l'inerzia**, cioe' rileggere tutto dove la densita' e' O(1): toglie la causa, non il
   sintomo. E' la leva che il lavoro di oggi indica come la sola non-cosmetica;
2. **sotto-passo per lo spin** (lo stesso principio di `nsub`): presidio numerico onesto, non una
   cura. NB: con la crescita **diffusiva con plateau** misurata oggi il numero di sotto-passi
   **non diverge** — ne servirebbero ~112, non "sempre di piu'";
3. **correggere i due commenti stale** alle righe **868** e **1803** (un commit suo): sono loro ad
   aver fatto partire il mandato di oggi da una diagnosi sbagliata;
4. **`_pesi()`**: FASE B non eseguita, la premessa del mandato e' falsa (`doc/REPERTO_pesi_ricorsione.md`);
5. **`:5318`**: il diaglog re-implementa `cs` inline — sotto turbo quella colonna mente.

Il **gate** e' a `c0803713` in `CLAUDE.md` §0, il blob sul disco e' **`f5887254`**. **Non
ri-timbrato di proposito.** `soliton_simulator.py` **non e' stato toccato** in nessuno dei lavori
del 14 e 15 settembre: bilancio, Gilbert/FDT, `_pesi`, profilazione.

Dettagli: `doc/ESITO_scan_turbo_K300.md`, `doc/REPERTO_pesi_ricorsione.md`,
`doc/PROFILAZIONE_costo_run.md`, `doc/REPERTO_gamma_condiviso.md`, `doc/PREDIZIONE_*.md`,
`doc/AUDIT_misurato_vs_asserito.md`, `STATO_CLAUDE_fork-su2.md`, `CLAUDECONNECT.md`.
