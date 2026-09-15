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

## 6-sexies. MATURAZIONE (2026-09-15) — **CONCLUSO: ESITO (C)**

Documento: **`doc/MATURAZIONE_aliasing.md`**. Predizione scritta **prima** e committata prima
(`doc/PREDIZIONE_maturazione.md`, commit `a8a0360`). **Run CONCLUSO, 2000 passi.**
Relazione dovuta per §5-ter.

> ### VERDETTO: **ESITO (C).** L'aliasing e' **STRUTTURALE, non transitorio.**
> La maturazione **funziona** (`ramp` lineare, `rho` da 1.76e-11 a 5.5e-4, pavimento rilasciato dal
> 100% al 7%) **ma non toglie l'aliasing: la frazione aliasata e' 100% a OGNI campione, l'ultimo
> compreso.**

**La domanda:** il `1e-7` dell'inerzia e' ETA'. Se lo e', l'aliasing (112 giri/passo) potrebbe
sparire **da solo** per maturazione, e non ci sarebbe niente da riparare. Va accertato **prima** di
cablare qualunque cura, perche' cablare su un sistema aliasato darebbe un risultato inattribuibile.

**Sigillo PASS** (20 campi + RNG, `0.000e+00`, N confrontabile) e **flag confermati IN-RUN**:
`GAMMA_TURBO = 1`, `STEP2_OROLOGIO = False`, fork+MEM attivi. Comportamento **naturale**, non forzato.

**PRIMA META' DELLA PREDIZIONE: CONFERMATA.** La predizione diceva che `theta` non sarebbe sceso
subito, perche' l'inerzia e' bloccata sul **pavimento `1e-6`**, e che la densita' mediana lo avrebbe
attraversato **"poco dopo il passo 150-300"**. Misurato: attraversamento al passo **~245-250**,
`rho` mediana da **1.5e-8** (passo 25) a **5.07e-6** (passo 425), e il pavimento passa dal vincolare
il **100%** dei nodi al **14.7%**.

**SECONDA META': NON CONFERMATA (ancora), ed e' il riscontro che conta.** `rho` e' cresciuta **4.5x
oltre il pavimento** e **`theta` NON e' sceso**: piatto a **~4.6e4** gradi/passo, con la frazione
aliasata ancora al **100%**. Se `theta` seguisse `1/inerzia`, sarebbe gia' a ~1.0e4.

**COSA HO SBAGLIATO NELLA PREDIZIONE, dichiarato.** La catena `omega ∝ ramp^-4` tratta `omega` come
se fosse **istantaneamente** uguale a `coppia/inerzia`. **Non lo e':** `omega_s` e' una **memoria**
con rilassamento (riga 1918) e tempo caratteristico **gia' misurato**, `tau/DT ≈ 250 passi`. Dal
ginocchio (250) a ora (425) e' passato **meno di un tempo di rilassamento**: siamo **dentro** il
transitorio. **Il dato non falsifica ancora la predizione, ma non la conferma, e la predizione era
incompleta.**

**LA PREVISIONE CORRETTA, scritta ORA prima di vederla:** se `theta` insegue `1/rho` con ritardo
`tau ≈ 250`, la discesa deve diventare visibile **dal passo ~500-600**. **Se al passo 800 `theta` e'
ancora a 4.6e4, la lettura `omega ∝ 1/inerzia` e' sbagliata, non solo ritardata** — esito **(C)**.

**UNA PROIEZIONE SCOMODA, detta ora e non fra due ore:** con `theta ∝ n^-4`, la soglia di 30
gradi/passo sarebbe attraversata a **~2660 passi**, **oltre i 2000 del run**. E al passo 2000 `ramp`
mediano sara' **~0.31**: **nessuna popolazione matura (`ramp > 0.9`)**, quindi la **seconda misura**
prevista dal mandato (`chi` nella zona matura) **non sara' eseguibile su questo run**.
Due strade, **decisione di Luca**: prolungare a ~3000 passi (altre ~2-3 h), oppure fermarsi a 2000 e
riportare la **pendenza** di `theta(n)`, dichiarando l'attraversamento come **estrapolazione**.

**AGGIORNAMENTO AL PASSO 1200 — IL CRITERIO E' SCATTATO.** Avevo scritto prima di vederlo: *"se al
passo 800 theta e' ancora a 4.6e4, la lettura omega ∝ 1/inerzia e' SBAGLIATA, non solo ritardata"*.
**E' cosi'.** Regressione su 14 campioni, solo dopo il rilascio del pavimento (passi 425-1200):

```
d(log theta)/d(log n)    = -0.020      attesa dalla lettura: -4
d(log theta)/d(log rho)  = -0.006      attesa dalla lettura: -1
leva:  n x2.82   rho x16.9   theta x0.977
```

> **Con `rho` cresciuta quasi 17 volte, `theta` e' variato del -2%. Non e' un ritardo: e' ASSENZA DI
> DIPENDENZA. VERDETTO INDICATO: ESITO (C), l'aliasing e' STRUTTURALE, non transitorio.**
> E lo si sa **al passo 1200, non a 20.000** — che era lo scopo di misurare la pendenza.

**Meccanismo candidato (IPOTESI, non ancora misurata):** riga 1913,
`_tau = TAU_A * max(dens/dens_rif, 0.05)`. Prima della maturazione quasi tutti i nodi sono sotto
`1e-6`, scatta il **pavimento 0.05** e `tau/DT = 250`. Dopo, per il nodo mediano `dens/dens_rif ≈ 1`
e `tau = TAU_A`, cioe' **`tau/DT = 5000`**. **La memoria si e' allungata di ~20x esattamente mentre
il sistema maturava.** Con `omega_eq = |F|·sqrt(dt·tau/2)`, se `|F| ∝ 1/rho` **e** `tau ∝ rho`,
allora `omega_eq ∝ rho^(-1/2)` e anche quella discesa arriverebbe su 5000 passi. Da verificare
aggiungendo la colonna `tau` alla sonda, senza toccare la fisica.

**I NUMERI FINALI.** `theta` **non e' piatto** — ha un picco a 4.978e4 (passo 600) e cala a
**3.243e4** (passo 2000), **-35%**. Ma la domanda era *"cala COME PREVISTO?"*, e la risposta e' no,
di due ordini:

| finestra | leva su `rho` | `d(log theta)/d(log rho)` | atteso |
|---|---|---|---|
| tutto post-pavimento (22 campioni) | **x309** | **-0.061** | -1 (o -0.5 raffinata) |
| ultima parte (1300-2000) | x8.7 | -0.131 | idem |

Dal picco di `theta` alla fine, con `rho` cresciuta **x43.3**: se seguisse `1/rho` sarebbe **1149**;
se `rho^(-1/2)` sarebbe **7564**; **misurato 3.243e4** — **28x e 4.3x sopra**. La pendenza `-0.061`
con leva `x309` cade nella banda `-0.2..+0.2`: **il criterio temporale posto da Luca e' soddisfatto,
la lettura e' SBAGLIATA, non ritardata.**

**Il limite dichiarato in anticipo si e' avverato:** `ramp` mediano finale **0.2585** (proiezione
fatta al passo 425: ~0.31). **Nessuna popolazione matura**, quindi la seconda misura (`chi` nella
zona matura) **non era eseguibile** — come avevo detto prima, non dopo.

**E UN INDIZIO TRASVERSALE CHE PUNTA DALLA PARTE SBAGLIATA.** Alla stessa istantanea, negli ultimi
campioni: nodi **giovani** (`ramp<0.1`) `theta = 3.485e4`; nodi **maturi** (`ramp>0.5`)
`theta = 4.088e4`. **I maturi ruotano PIU' VELOCEMENTE.** Se `omega = coppia/inerzia` e l'inerzia
cresce con la maturita', dovrebbe essere il contrario. **E' a un solo istante, quindi il ritardo non
puo' spiegarlo** — ma e' grezzo (due classi, campione piccolo sui maturi): lo riporto come
**indizio**, non come misura. Il test vero e' la regressione trasversale del
`doc/CRITERIO_omega_rho.md` §4.1, **in corso**.

**Costo misurato:** 425 passi in 9.0 min (~1.3 s/passo a N≈4100); stima **2-3 h** per i 2000.

---

## 6-septies. IL TEST TRASVERSALE (2026-09-15) — **la lettura `omega = coppia/inerzia` e' FALSIFICATA**

Documenti: **`doc/CRITERIO_omega_rho.md`** (criterio scritto PRIMA + esito) e
`doc/MATURAZIONE_aliasing.md`. Sonda **ri-sigillata PASS** prima dell'uso. **Nessun run in volo.**

**Perche' serviva un test senza tempo.** Luca ha rilevato che la mia ipotesi **rigenerava la propria
scusa**: ogni volta che l'effetto non si vedeva, il ritardo era cresciuto (pavimento -> `tau=250` ->
`tau=5000`). Con `tau` proporzionale a `rho` e `rho` crescente, **aspettare non converge mai**.
Il presidio, ora in `CLAUDE.md` §9: **quando la spiegazione e' temporale, il test che la decide non
deve contenere il tempo.**

**RISULTATO 1 — il meccanismo `tau` e' CONFERMATO PER MISURA**, non piu' ipotesi:

| passo | `tau/DT` | % col pavimento 0.05 attivo |
|---|---|---|
| 1-200 | **250** | 100% -> 69% |
| 400 | 2884 | 10.7% |
| **700** | **4425** | **8.9%** |

`tau/DT` da **250 a 4425** (**x17.7**), e tende a `TAU_A/DT = 5000` — l'ancoraggio del nodo mediano
che Luca aveva dedotto dalla riga 1913. **La memoria si allunga di quasi 18x mentre il sistema
matura.** Ma non salva la lettura, perche' il test qui sotto non contiene il tempo.

**RISULTATO 2 — il test trasversale: la lettura CADE.** 4374 nodi, **leva sull'inerzia x10 080**
(quattro decadi), a **un solo istante**:

```
correlazione r = -0.395
theta per decile di inerzia:  basso 6.663e4 -> medio 5.073e4 -> ALTO 3.464e4
PENDENZA  d(log theta)/d(log inerzia) = -0.106
```

| esponente | `theta` cadrebbe di |
|---|---|
| -1.000 (lettura originale) | **x10 080** |
| -0.500 (lettura raffinata) | **x100.4** |
| **-0.106 (misurato)** | x2.66 — osservato per decili **x1.92** |

> **VERDETTO: `omega = coppia/inerzia` come LEGGE DI SCALA e' FALSIFICATA.** L'esponente misurato e'
> **-0.106**, non -1 ne' -0.5, su quattro decadi e **senza scappatoia temporale**.

**CORREZIONE AL MIO STESSO CRITERIO, dichiarata.** La banda che avevo scritto (-0.2..+0.2) diceva
*"omega NON dipende da inerzia PER NESSUNA VIA"*. **Quella formulazione e' troppo forte e i dati la
smentiscono:** `r = -0.395` e l'andamento per decili e' **monotono**, `theta` cala di **x1.92**. Una
dipendenza **c'e'**. La formulazione corretta: **`omega` dipende da `inerzia` con esponente -0.106,
circa UN DECIMO di quello richiesto.** La conclusione non cambia, la motivazione si': non e'
"nessuna dipendenza", e' **una dipendenza dieci volte troppo debole** — e nessun ritardo, per quanto
lungo (ora sappiamo: 4425 passi), spiega un **esponente** sbagliato di un fattore 10.
Sto correggendo un mio criterio **dopo** aver visto i dati, ed e' la mossa che il presidio §9 vieta:
lo dichiaro. La differenza e' che **non sto salvando l'ipotesi, la seppellisco lo stesso** — la
correzione rende il verdetto **piu' preciso, non piu' clemente**.

**E RITIRO UN INDIZIO PRECEDENTE.** Avevo riportato che i nodi "maturi" ruotavano **piu'
velocemente** (segno opposto all'atteso). Il test per **decili di inerzia** lo **smentisce**:
l'andamento e' monotono **nel verso giusto**. "Maturo" e "inerzia alta" non sono la stessa
popolazione, e vale il test per decili, non il confronto a due classi. **Indizio ritirato.**

---

## 6-octies. TRACING di `omega` (2026-09-15) — **il controllo ha stanato un termine mancante, ed era MIO**

Documenti: `doc/PREDIZIONE_tracing_omega.md` (criterio, committato **prima**: `075a09f` + esito (IV)
in `457abe4`) e **`doc/TRACING_omega.md`**. **CONCLUSO: ESITO (I)**, col meccanismo identificato.

**Il riscontro.** `correzione` ha **DUE** termini (righe 1895-1901) e io ne avevo ricostruito **uno**:
```
correzione = cross(B, nb)
if CAMPO_SPINORIALE:  correzione += cross(_nb_grav(), nb)      <- ATTIVO nei run del fork
```
Il secondo e' il torque verso il Bloch del **campo emesso spinoriale**. La mia catena lo ignorava.

**Come e' stato stanato: dal controllo, non dall'occhio.** Nel criterio (§IV.4, scritto **prima**)
avevo messo un controllo sulla **direzione** del residuo, perche' un `R_stoc` alto ha due cause:
rumore genuino **oppure un mio errore**. Regola: `cos(stoc, det)` ~ 0 = rumore isotropo; ~ ±1 =
**errore sistematico mio**, e allora **(IV) non si dichiara**.
**Misurato `cos = +0.643`**, oltre la soglia 0.5, e **stabile su tutti e otto i campioni**
(+0.348 … +0.643). Un residuo **allineato e persistente non e' rumore: e' formula che manca.**
E l'ampiezza torna: con `R_stoc ~ 2.8` e `cos ~ 0.64`, il deterministico vero e' ~`1+R·cos` = **2.8x**
quello ricostruito — **mancava un termine dello stesso ordine del primo**.

> **Senza quel controllo avrei dichiarato l'ESITO (IV)** — *"e' il rumore che guida omega"* — con
> `R_stoc` fra 13 e 2.8 a sostenerlo. **Sarebbe stato un falso positivo:** avrei attribuito al
> rumore un effetto che e' **una riga di codice**.

**Tre esiti che il termine mancante NON cambia** (perche' non dipendono da esso):
1. **Il dissipativo NON domina:** rapporto coppia/dissipazione = **73.88**. L'ipotesi *"omega e'
   governato dal rilassamento"* e' **esclusa**, non rinviata.
2. **L'angolo (B,nb) e' PIATTO:** pendenza **-0.006** (`r = -0.025`), mediana **59.4 gradi**.
   Nessun allineamento crescente con la densita' -> **(II-b) escluso**, e in modo robusto, perche'
   `B` e' ricostruito **esatto** (il codice lo costruisce da `_nb_prec`, non dal `nb` rumoroso).
3. **`|B|` DECRESCE** con l'inerzia (**-0.534**), non cresce -> **(II-a) escluso**.

E una conferma incrociata: il `theta` misurato qui, **-0.113**, coincide col **-0.106** del test
trasversale di ieri, misurato in modo indipendente. **Le due misure si confermano a vicenda.**

**Cosa NON dichiaro.** Il run incompleto stampava **(I)**, colpevole a valle. **Non lo dichiaro:**
era calcolato con `coppia/inerzia` dimezzata. Il run corretto e' in volo, tracer **ri-sigillato PASS**
dopo la modifica e **prima** dell'uso. Il run incompleto e' conservato come evidenza in
`csv/_test_fork/_tracing_omega_INCOMPLETO.txt`.

**IL RUN CORRETTO — ESITO (I), E IL COLPEVOLE HA UN NOME.**

Con il secondo termine al suo posto, la ricostruzione spiega il **96%** dell'incremento:
`R_stoc = 0.041`, **sotto** l'errore che la mia stessa approssimazione prevedeva (**0.097**).
**(IV) ESCLUSO** — e questo **valida a posteriori** la diagnosi: l'`R_stoc ~ 2.8` di prima **era** il
termine mancante, non il rumore.

| pendenza su `log inerzia` (passo 400, 2781 nodi) | valore | r |
|---|---|---|
| `coppia` (completa) | **-0.056** | -0.260 |
| **`coppia/inerzia`** | **-1.056** | **-0.981** |
| **`theta`** | **-0.113** | -0.353 |

La coppia e' **piatta**: tutto il `-1` viene dalla divisione per l'inerzia, ed esce **-1.056 con
r = -0.981**, praticamente esatto. **La formula d'ingresso e' giusta; l'esponente si perde DOPO.**

**DOVE si perde: nel rilassamento, attraverso `sqrt(tau)`.** `omega` e' un random walk smorzato, il
cui equilibrio e' `|omega|_eq = sigma * sqrt(tau/(2 dt))`. Le due pendenze, **misurate**:

```
sigma = |coppia|/inerzia   pendenza  -1.056     (2781 nodi, r = -0.981)
tau                        pendenza  +1.812     (20 nodi; via indiretta: +1.867)
attesa per |omega|:  -1.056 + 1.812/2 = -0.150
theta MISURATO                        = -0.113        scarto 0.037
```

> **Il `-1` della coppia e' cancellato dal `+0.91` di `sqrt(tau)`.** `tau = TAU_A*max(dens/dens_rif,
> 0.05)` cresce con la densita', e il suo peso entra nel plateau come **radice**. Coppia e memoria si
> annullano a vicenda e resta `-0.11`.
> **NON C'E' NESSUN BUG:** non c'e' una riga che fa qualcosa di diverso da quel che si crede. C'e' un
> **rilassamento la cui costante di tempo dipende dalla stessa grandezza** che sta al denominatore
> della coppia. **E' il sistema che si cancella da se'.**

**UNA COLONNA DA BUTTARE, dichiarata.** Nel run corretto la colonna `angolo` e' **invalida**: la
calcolo come `arcsin(|correzione|/|B|)`, che e' un seno **solo** se `correzione = cross(B,nb)`; col
secondo termine satura e stampa 90.00 per tutti. **Va ignorata.** L'esclusione di **(II-b) regge
lo stesso** e viene dal run *incompleto*, dove l'angolo era esattamente quello fra `B` e `nb`:
**-0.006, r = -0.025, mediana 59.4 gradi**. I dati "difettosi" misuravano bene proprio cio' che al
run corretto sfugge.

**Verdetto contro il criterio scritto prima:** **(I) confermato**; (II-a) escluso (`|B|` **decresce**,
-0.534); (II-b) escluso (angolo piatto); (III) non si applica; (IV) escluso (`R_stoc` 0.041).

**L'errore era nella MIA ricostruzione, non nel simulatore:** `soliton_simulator.py` non e' stato
toccato, blob `f5887254`.

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
