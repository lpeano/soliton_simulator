# RELAZIONE — per Claude web · **aggiornata 2026-09-16** *(il giro del 16 e' il §9, in fondo)*

> **Scritta per Claude web**, che legge il repo e deve pronunciarsi su una decisione di merito.
> Branch `fork-su2`. **Blob sul disco `c57800c1`** *(oggi e' cambiato TRE volte: `08784685` ->
> `a467fd9a` taglio spettrale -> `57681b9e` correzione (1) -> `c57800c1` correzione (2))*,
> gate in `CLAUDE.md` §0 a `c0803713`
> (**non ri-timbrato di proposito**: i sigilli della FASE 2 non passano).
> Il documento e' **cumulativo**: i paragrafi 1-7 sono nell'ordine in cui i fatti sono nati, e
> l'ultimo lavoro sta in fondo. **Se leggi una cosa sola, leggi il §0-ante qui sotto** (il giro
> del **16**); il §0 che lo segue e' quello del **15**, tenuto perche' la sequenza conti.

---

## 0-ante. **L'ULTIMO GIRO (2026-09-16) — in dodici righe.** Il dettaglio e' il §9

> **Blob: `08784685` -> ... -> `c57800c1`.** `soliton_simulator.py` e' stato toccato **tre volte**
> oggi, tutte e tre committate **prima** di qualunque run.
>
> 1. **`S` e' CHIUSA: rumore.** 4 semi per braccio, IC95 con `t(3)`: OFF `[89.722, 90.022]`,
>    ON `[89.995, 90.103]` — **entrambi contengono 90**. E `OFF s3` vale **89.9999**, il null esatto.
>    *(Resta aperta una domanda DIVERSA: il contrasto ON-OFF `+0.177` esclude lo zero, ma i due
>    bracci differiscono anche di ~7x in RISOLUZIONE -> voce `S2`.)*
> 2. **`R` e' REFUTATA**, dal dato piu' pulito del lotto: `tau` cambia di **due ordini** (+1.708 ->
>    +0.020) e **`sigma` si muove di 0.0013**, contro una barra di sistema di 0.030.
> 3. **`ESITO (I)` confermato QUATTRO volte**: `-1.0498 / -1.0592 / -1.0562 / -1.0554` contro il
>    `-1.056` del tracing. Due bracci, due leggi di `tau`, l'esponente non si muove di 0.01.
> 4. **Il FDT rifatto sul sistema pulito: CENTO volte meglio, MILLECINQUECENTO volte insufficiente.**
>    `kT/Lam` da ~2e7 a **1.2e5**, ma il disordine resta **726-3081 volte** piu' veloce dello
>    smorzamento. **NON SI CABLA.**
> 5. **Lo spin e' ACCOPPIATO MA SENZA BILANCIO** (terzo esito, non previsto dal mandato): decide
>    dove la materia si divide e con che verso la gravita' tira, ma **nessun canale trasferisce una
>    grandezza conservata**. Il torque **non e' azione-reazione** (dimostrato dalla formula) e nel
>    file **non esiste un'energia totale**. **Quindi `lambda` NON SI DERIVA**: manca la grammatica.
> 6. **Il marchio dello STRATO 1 e' TOLTO: `tau` SEGUE `cs`, misurato per la prima volta.**
>    Sigillo **25/27 + 2 FAIL ATTESI** (previsti e committati prima). **`S8b`: rapporto `cs=8/cs=1`
>    = 7.660686976 = atteso** — se `cs` fosse ignorato varrebbe esattamente 1.000000000.
> 7. **I DUE `theta` sono chiusi** (`C19`): `theta_coord = |omega|*DT` e `theta_prop = |omega|*dt_n`
>    girano ora **insieme**, col controllo d'identita' a `4.6e-16`. **Differivano del 26 % sulla
>    mediana.** E ne e' uscita una correzione: la catena `sigma + tau/2` **assumeva `pend(r) = 0`**,
>    mai verificato.
> 8. **Taglio spettrale CABLATO** (`--rumore-colorato`, flag OFF). **`N7` VINTO**: la ricorsione usa
>    `dt_n = DT*r` **per nodo**, errore `0.000e+00`, contro `6.142e-01` col `DT` nudo. `N2` aperto.
> 9. **DUE CORREZIONI DI DIFETTO, SENZA FLAG** (decisione di Luca, §9.12):
>    **①** `_xi_rumore` **non si eredita** — `xi` e' l'AMBIENTE, non una proprieta' del nodo.
>    Correlazione padre-figlio **da `+1.0000` a `+0.0065`** su 258 coppie.
>    **②** `inerzia = max(rho*(CS_M/cs)^2, 1e-6)` — il fattore `cs^-2` che la derivazione impone e
>    che **mancava**. **`M2` (il decisivo) PASS: `max|A-B| = 0.000e+00`, nodi 3070 = 3070.**
>    **⚠ Ma l'effetto OGGI e' minuscolo — fattore mediano `1.0000048` — ed era scritto PRIMA.**
> 10. **La trappola CRLF e' chiusa alla radice** (`.gitattributes`, `eol=lf`). Aveva morso **due
>    volte**: la prima per un mio `git checkout`, la seconda **da sola**, fra due commit.
> 11. **⚠ QUATTRO SIGILLI SI SONO ROTTI OGGI, E NESSUNO LO HA DETTO**: `AttributeError` a S2
>    (metodo estratto assente dal guscio), `AttributeError` a N7 (`Generator.normal` read-only),
>    **loop infinito** a N2 (46 minuti al 68 % di CPU), e **due criteri SCADUTI** che hanno prodotto
>    FAIL falsi. **Una sola forma: un diagnostico che tocca i globali del simulatore, o ne elenca i
>    metodi a mano, si rompe appena il simulatore cambia forma — in SILENZIO.**
> 12. **⚠ E TUTTI I DATI DI OGGI PORTANO IL MARCHIO**: prodotti **prima** delle due correzioni,
>    cioe' su un **sistema diverso** da quello corrente. **La campagna va RIFATTA.**

---

## 0. L'ULTIMO GIRO (2026-09-15, sera) — in dodici righe

> 1. **Trovato e curato un difetto silenzioso:** la cache `_cs_nodo_prev` veniva **scartata a ogni
>    mitosi**, quindi nel **71.88 %** delle chiamate `tau = d/cs` calcolava `tau = d/CS_M`.
>    Colpiva anche **lo STRATO 1, gia' sigillato 23/23**. Sigillo della patch: **5/5 PASS**.
> 2. **La cura NON chiude la FASE 2.** La pendenza T3 va da **-0.4265** a **-0.4710** contro
>    l'attesa **-0.69**: **16.9 % del divario**, non la meta'. `theta` resta a **42.8 giri/passo**.
>    **⚠ IL "16.9 %" E' STATO RITIRATO — vedi il punto 4. Lo lascio scritto perche' la sequenza
>    conti: e' cosi' che un numero sopravvive mezza giornata prima di cadere.**
> 3. **Due predizioni opposte, entrambe sbagliate:** il mandato diceva ~50 %, **io dicevo zero**.
>    L'errore mio e' spiegato al §6-duodecies ed e' di tipo generale.
> 4. **Il controllo sui semi ha SMENTITO il punto 2** (§6-terdecies): su 3 semi il segno di `Delta`
>    **non è nemmeno concorde** (-0.0445 / **+0.0367** / -0.0635), `t = -0.77`. **Il "16.9 %" è
>    ritirato.** E la scoperta collaterale vale più della vicenda: **la barra d'errore usata in tutto
>    il programma è 3 volte troppo piccola** (dispersione fra semi **0.030** contro `SE` interna
>    **0.010**).
> 5. **SETTIMO difetto silenzioso, il più grosso** (§6-quaterdecies): `_psi_spin_prec` non era esteso
>    alla mitosi → la guardia **esatta** di `ritmo()` scartava il ramo a **4π** nel **95.33 %** dei
>    casi → **la FASE 5 (doppia copertura) non è MAI entrata in funzione.** Curato, **6/6 PASS**.
>    **Non** è "tempo proprio stale": è **l'orologio scalare storico invece di quello dichiarato.**
> 6. **`S4` di quella cura ha misurato la cosa sbagliata:** `median(r) = 1.0` **per costruzione**,
>    con qualunque orologio. Secondo caso del **punto fisso auto-normalizzante**.
> 7. **ESITO (A) sul braccio OFF della prima misura vera** (par.6-sexdecies): nessuna firma si
>    stacca dal casuale, su 2 semi. **Ma theta e' a 92.8-98.7 giri/passo, il DOPPIO di quanto avevo
>    scritto**: (A) e' l'esito che l'aliasing produrrebbe da solo.
> 8. **--cs-dinamico era SPENTO** (par.6-septdecies), dimostrato da TRE vie. Decisione di Luca:
>    **ci va SEMPRE**. E il sigillo 23/23 dello STRATO 1 **non ha mai esercitato la dipendenza da
>    cs** (par.6-octodecies): i quattro run in partenza sono **la prima volta che gira davvero**.
> 9. **Due REGOLE nuove** (par.6-vicies): la **promozione delle componenti** (par.10) e **un dato
>    deve portarsi dietro le proprie condizioni** (par.9). Dal primo e' uscito il reperto dei
>    **10 flag gia' accesi** che non sono mai passati per nessun criterio.
> 11. **I QUATTRO BRACCI, esito finale** (par.6-unvicies): **(A) NON conclusivo**. Nessuna firma
>    emerge **nemmeno a risoluzione 6.4x migliore** (theta 96.4 -> 15.1 giri/passo). Le obiezioni
>    "la FASE 5 non era attiva" e "cs era spento" sono **entrambe chiuse**: e' il negativo piu'
>    pulito della sessione. Ma theta resta **oltre il giro per passo**, quindi la frase "lo spin non
>    si organizza" resta **INDICIBILE**.
> 12. **Due presidi di metodo, entrambi correzioni a me** (par.6-duovicies): **due semi non bastano
>    per una barra fra semi** (t con 1 gdl = 12.7), e **una soglia su un sistema che cresce va
>    dichiarata con l'istante** (cs_std/cs: venti volte in 450 passi).
> 10. **E la domanda aperta più utile non cerca un bug** (§6-quindecies): l'attesa `-0.69` assume che
>    `sigma` sia indipendente da `tau`, ma c'è un **anello** che lo mette a valle. **Forse è il
>    BERSAGLIO a essere mal calcolato.** Da provare **per prima**; **non lanciata**, e il numero
>    **non è nei dati** come si credeva.

---

## 0-ter. **I SEI PATTERN COMPORTAMENTALI** (regole di Luca, 2026-09-16) — leggi questi prima di proporre qualsiasi cosa

> **Sono REGOLE, non suggerimenti**, e stanno anche in `CLAUDE.md` §0-ter. Sono qui perche' un
> Claude web nuovo le deve ricevere **leggendo questa relazione**, senza doverle far dare di nuovo.
> Nascono tutte da errori realmente commessi su questo repo, quasi tutti **nello stesso giorno**.

**P1 — NON USARE L'ASSOCIAZIONE SENZA VERIFICARE LO STORICO.**
Prima di proporre una diagnosi, una cura o un mandato, **rileggere dal DISCO** cio' che e' gia'
stabilito su quel punto (`doc/RAMIFICAZIONI.md`, questa relazione, i documenti di reperto) e
verificare di **non contraddire un fatto gia' misurato**. Se si contraddice: **o c'e' un dato nuovo
che lo supera — e lo si dichiara — o la proposta cade.**
L'associazione genera **candidati**, non conclusioni. Le frasi *«manca X»*, *«il problema e' Y»*,
*«basta fare Z»* sono il **segnale d'allarme**: li', prima di scrivere, si controlla.
Se rileggendo **non si trova nulla**, **dirlo**: *«non ho un fatto stabilito su questo, sto
proponendo per analogia»*.
*(Quattro precedenti, tutti del 2026-09-15: `--tau-luce` messo nella casella del turbo; `theta ~43`
trasportato fra due configurazioni; `--step2-orologio` fra gli esperimenti benche' derivato e
sigillato 10/10; **«universo in accelerazione senza freni» quando il freno `−omega/tau` era gia'
misurato** e anche il ginocchio — previsto `7.059e4`, misurato `7.271e4`, scarto x1.03.)*

**P2 — PRIMA DI ESCLUDERE UN FLAG: forza il sistema o lo CORREGGE?**
Escludere una **correzione** significa misurare un sistema che si sa difettoso.

**P3 — NESSUNA STATISTICA SENZA BARRA D'ERRORE**, e per confronti **fra bracci** si usa la
**dispersione FRA SEMI**, mai la `SE` interna a un singolo run (**C10**: la pendenza cambia di
**0.03 a codice invariato**, contro `SE` interna ~**0.010**). **Per una barra fra semi servono
>= 4 semi**: con 2, `t(0.025,1) = 12.706`.

**P4 — PRIMA DI MISURARE SE UNA GRANDEZZA CAMBIA, VERIFICARE CHE SIA LIBERA DI CAMBIARE.**
Una quantita' normalizzata sulla propria mediana non puo' muoversi: misurarla e' un test vuoto
(**C12**).

**P5 — OGNI RAMO `else` / fallback / `getattr(..., default)` su un percorso fisico VA CONTATO.**
Un fallback mai misurato e' un comportamento sconosciuto; uno che scatta l'80 % delle volte **non
e' un fallback: e' il comportamento principale** (**C7** 71.88 %, **C11** 95.33 %).

**P6 — OGNI CSV DI MISURA porta BLOB, SEME e TUTTI i flag** che distinguono quel run dagli altri
bracci. Un file che si distingue dagli altri **solo per il nome** non e' un dato: e' un ricordo.

> **Uso:** P1 e' un prerequisito di **scrittura**; P2 e P6 sono check di **preparazione** di un run;
> P3, P4, P5 sono check di **lettura** di un risultato. Un run che non soddisfa P6 in **ogni** campo
> **non si conta**.

---

## 1. IN UNA RIGA (2026-09-14 — storico, resta valido)

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

## 6-novies. `tau` deve essere il TEMPO-LUCE `d/cs`? (2026-09-15) — **criterio scritto, misura IN VOLO**

Documento: **`doc/TAU_tempo_luce.md`**. Contiene **solo il criterio e il setup**, committati
**prima** dei dati. **I numeri non ci sono ancora.**

**La domanda nasce dal verdetto del tracing:** il `-1` della coppia e' cancellato dal `+0.91` di
`sqrt(tau)`. L'aliasing viene dall'**interazione di DUE leggi**: `omega = coppia/inerzia`
(riga 1918) e `tau = TAU_A*max(dens/dens_rif, 0.05)` (riga 1913).

**Le due righe non sono pari, e la seconda ha gia' due fatti MISURATI contro:**
1. **non fa quello che dichiara**: e' scritta come `tau ∝ dens` ma misurata da' **`rho^1.81`**
   (via indiretta `+1.867`: due strade indipendenti, stesso scarto dall'unita');
2. **il perche' e' strutturale**: `dens_rif` e' la **MEDIANA**, quindi per il nodo mediano
   `dens/dens_rif ~ 1` **sempre** — `tau` del nodo tipico e' **ancorato a `TAU_A` per costruzione**
   (rilievo di Luca, gia' in `CLAUDE.md` §9). **Punto fisso auto-normalizzante, non transitorio.**
Una riga che non fa quello che dichiara e' la categoria che questo repo ha gia' pagato **tre volte**.

**L'incoerenza da sanare:** se `inerzia = T² = (d/cs)²`, allora **il tempo che COSTRUISCE l'inerzia
e quello che la RILASSA devono essere lo stesso**. Oggi sono **due diversi nella stessa equazione**.
Il candidato `tau = d/cs` e' **imposto** (causalita': non si puo' ricordare piu' a lungo di quanto si
impieghi a sapere di se'), **gia' cablato** (e' il `tau` dello Strato 1, messo li' per la stessa
ragione) e a **zero manopole**.

**Nota di metodo:** il tracer misura `tau_luce` con la **STESSA formula gia' nel file**
(`_bloch_ritardato`: `d_nodo` = media degli archi incidenti con fallback `LAM`, `cs_nodo` dalla cache
`_cs_nodo_prev`), non con una nuova. Misurare la proposta con una formula diversa da quella cablata
sarebbe stato incoerente col suo stesso argomento.

**IL CRITERIO, fissato prima:** `pendenza(theta) = -1.056 + pendenza(d/cs)/2`.
`|pendenza(d/cs)| <= 0.3` -> `theta` torna a **~ -1.0**, la cancellazione si rompe;
`pendenza(d/cs) ~ +1.8` -> **non cambia nulla**, la sostituzione resta piu' coerente ma **non
risolve**, e va detto cosi'.

**IL CAVEAT DI AMPIEZZA, da dire comunque:** `tau` passa da ~44 unita' di tempo a ~0.25, e poiche'
`|omega|_eq ∝ sqrt(tau)` il fattore e' **~1/13**: da **112 giri/passo a ~9**.
**Un ordine di grandezza nella direzione giusta, NON la soluzione dell'aliasing.**

**ESITO DELLA FASE 1 — e prima una CORREZIONE A ME STESSO.**

La formula del criterio (`pendenza(theta) = sigma + tau/2`) **va verificata sul caso attuale prima di
usarla per estrapolare**, e **non regge**:

| | `sigma` | `tau` | attesa | misurata | scarto |
|---|---|---|---|---|---|
| run 400 passi, `tau` su **20 nodi** | -1.056 | **+1.812** | -0.150 | -0.113 | **0.037** |
| run 300 passi, `tau` su **2195 nodi** | -1.078 | **+1.176** | -0.490 | -0.152 | **0.338** |

> **Correzione a `doc/TRACING_omega.md` §6.3 e al commit `9713ddb`:** lì avevo scritto che la catena
> «si chiude» con scarto **0.037**. Quel numero usava `pendenza(tau)` su **20 nodi**. Su **2195**
> (`r = +0.796`) lo scarto è **0.338**: **la catena NON si chiude.** Il meccanismo qualitativo regge
> (√`tau` cancella **parte** del −1) ma il conto quantitativo no, e **resta un residuo di ~0.34
> nell'esponente che non so spiegare.**

**LA MISURA CHE IL CRITERIO CHIEDEVA:**
```
pendenza tau_ATTUALE  = +1.176   (r = +0.796, 2195 nodi)
pendenza tau_LUCE     = +0.097   (r = +0.351, 2195 nodi)     <- PIATTO
sigma = coppia/inerzia = -1.078
```
**`d/cs` è piatto (+0.097)**: prima banda del criterio, fissata prima di misurare. Un `tau` piatto
**non può cancellare niente**.

| stima per `theta` con `tau_luce` | |
|---|---|
| naive (solo formula) | **-1.030** |
| **corretta, se il residuo 0.338 resta** | **-0.692** |
| oggi, misurato | **-0.152** |

> **La stima onesta è −0.69, non −1.03.** Ma in entrambe: **la cancellazione SI ROMPE**, un fattore
> **4.5-7** sull'esponente.

**L'AMPIEZZA, coi numeri misurati:** `tau/DT` da **6500** a **66.5** passi (rapporto 0.0102);
`|omega|_eq ∝ √tau` → fattore **0.101** → `theta` da **126.7 a 12.8 GIRI per passo**.
**Un ordine di grandezza nella direzione giusta, e il settore resta ALIASATO. Non è una cura.**

**Restano aperti:** il **residuo di 0.338** (da stanare prima di fidarsi di qualunque predizione
quantitativa su questa catena) e l'**aliasing** (13 giri/passo).

**Cosa NON tocca:** la riga 1918, `inerzia`, e la **forma** del termine dissipativo — in particolare
**non** apre la questione se `-omega/tau` debba essere un allineamento LLG `-lambda n x (n x B)`:
e' **separata e aperta**, e mescolarla renderebbe inattribuibile qualunque risultato.

---

## 6-decies. BARRE D'ERRORE (2026-09-15) — **il residuo e' REALE ma TRANSITORIO. E ho corretto due volte, sbagliando la prima correzione.**

Documento: **`doc/BARRE_ERRORE_pendenze.md`**. **Nessun run**, solo statistica sui CSV su disco.

**1. La premessa da verificare non reggeva, ma la verifica era giusta da chiedere.**
L'ipotesi era: *"`r = 0.35` -> pendenza fragile, `SE ~ 0.3`"*. **`SE` non dipende quasi da `r`:
dipende da `sqrt(n)`.** Stessa pendenza, stesso `r`: `SE` = **0.108** con 20 punti, **0.0097** con
2195. `r^2` basso dice che la relazione **spiega poca varianza**, non che la pendenza sia incerta.

| grandezza | pendenza | SE | r^2 | IC 95% |
|---|---|---|---|---|
| `sigma` | -1.0780 | 0.0073 | 0.908 | [-1.0923, -1.0637] |
| `tau` attuale | +1.1760 | 0.0191 | 0.634 | [+1.1386, +1.2134] |
| `tau` luce (`d/cs`) | +0.0970 | 0.0055 | 0.123 | [+0.0862, +0.1078] |
| `theta` | -0.1520 | 0.0097 | 0.100 | [-0.1711, -0.1329] |

**2. Propagazione: `z = 21.8`.** Lo scarto al passo 300 **non e' rumore**. Si passa al secondo check.

**3. Il secondo check: e' TRANSITORIO, e si chiude.** Lo scarto cala di **due ordini**:

```
passo   50  100  150  200  250  300  350  400
scarto 0.979 0.660 0.448 0.427 0.194 0.337 0.230 0.010
pendenza su log(passo): -0.412
```

> **Al passo 400 la catena CHIUDE (scarto 0.010).** `tau ~ 4425-6500 passi` contro un run di 400: il
> sistema ha vissuto **meno di un decimo** di un rilassamento, e la formula vale **all'equilibrio**.
> **VERDETTO: TRANSITORIO, NON UN TERMINE MANCANTE. La ricerca non e' giustificata.**

**4. E la mia correzione di stamattina aveva la CAUSA SBAGLIATA.** Avevo attribuito la differenza
`0.037` vs `0.338` al campione (20 contro 2195 nodi), e l'avevo messo in `CLAUDE.md` §9 come fatto.
**A parita' di passo le due strade CONCORDANO:** passo 300 -> +1.176 contro +1.178 (scarto **0.002**);
passo 400 -> +1.812 contro +1.867 (scarto **0.055**). **La differenza e' il PASSO, non il campione.**

> **Quindi il numero ORIGINALE — "la catena si chiude, scarto 0.037" — era GIUSTO**, e col conto
> rifatto lo e' ancora di piu' (0.010). **Ho corretto una cosa giusta con una spiegazione sbagliata,
> e me ne sono accorto solo facendo il check che Luca ha chiesto.**

**Cosa resta e cosa no:** resta il presidio *"una pendenza si riporta col suo `SE`"* — ed e' proprio
applicandolo che si e' visto che `SE = 0.0097`. **Non resta** *"una pendenza su 20 nodi non e' una
pendenza"* **come spiegazione di questo caso**: qui i 20 nodi davano il numero giusto. Corretto in
`CLAUDE.md` §9, in `doc/TRACING_omega.md` e in `doc/TAU_tempo_luce.md`, **in loco**, lasciando le
righe originali visibili.

---

## 6-undecies. FASE 2 `--tau-luce` (2026-09-15) — **SIGILLO FALLITO. Ci si ferma.**

Documento: **`doc/SIGILLO_tau_luce_FALLITO.md`**. Blob `f5887254` -> **`7d484580`**.
**Gate NON ri-timbrato.** Flag **OFF di default**, e **T1 dimostra la byte-identita'**: il
comportamento di default del repo e' **invariato**.

```
T1=PASS   T2=FAIL   T3=FAIL   T4=FAIL   T5=PASS      ->   SIGILLO COMPLESSIVO: FAIL
```

**T1 PASS**, ed e' quello che copre di piu': confronto contro il file **prima** della modifica, 21
campi + RNG a `0.000e+00` con N confrontabile. Certifica insieme il flag OFF **e** che l'estrazione
di `_tempo_luce_nodo` da `_bloch_ritardato` non ha cambiato una virgola.

**T2 FAIL — ma e' un difetto del TEST.** Il monkeypatch agisce sul metodo **condiviso**, quindi
cambia **anche la ritardazione dello Strato 1** (`--fork-su2-mem` e' attivo): due meccanismi insieme,
traiettoria diversa, `N` 1718 contro 1647. E' il rovescio della scelta - giusta - di avere **una
sola** formula: un test naive che la sostituisce colpisce entrambi gli utilizzatori. Il presidio ha
funzionato: la riga dei conteggi per prima ha impedito di leggere uno zero come identita'.

**T3 FAIL — l'effetto e' REALE ma la META' di quello predetto.**

| | pendenza | SE | r^2 | n |
|---|---|---|---|---|
| OFF | -0.1685 | 0.0090 | 0.126 | 2417 |
| **ON** | **-0.4265** | **0.0091** | 0.464 | 2534 |

Spostamento **0.258**, cioe' **~28 sigma**: indiscutibile. **Ma l'attesa era -1.03** (naive) **o
-0.69** (stima onesta): misurata **-0.43**. Il criterio chiedeva almeno 0.3: **non ci arriva**.
**Non ho una spiegazione della meta' mancante e non ne invento una.**

**T4 FAIL a meta', ED E' UN REPERTO CHE TOCCA ANCHE LO STRATO 1.**
`d -> 2d` da' **2.000000 esatto**: sulla geometria e' una legge. `cs -> 2cs` da' **1.000000**: non
segue. La causa **non e' il cablaggio nuovo**: `_cs_nodo_prev` e' scritta in `step()` con l'`n` di
quel momento, poi `mitosi()` fa crescere `n`, e al passo dopo `len(csp) >= n` e' **falso** -> la
guardia ricade su `cs_nodo = CS_M`. **Misurato: cache usabile in 6 passi su 30 = 20%.**

> **Nell'80% dei passi il `cs` locale non viene usato affatto** — e vale **anche per lo STRATO 1**,
> sigillato 23/23, che usa la stessa funzione: il suo `tau = d/cs` e' in realta' **`d/CS_M`** quasi
> sempre. Il ritardo esiste, ma **la parte che porta la curvatura e' inerte.**
> **Ereditato, non introdotto oggi, e non era stato notato.**

**T5 PASS** sulla stabilita' (`|nb|-1 = 2.2e-16`, zero NaN) ma con un numero da leggere: `theta` da
**129.5 a 43.6 GIRI per passo**, fattore **0.336** contro lo 0.077 atteso. **L'ampiezza cala di 3x,
non di 13x, e 43.6 giri/passo restano un settore massicciamente aliasato. Non e' una cura, e ora
c'e' il numero misurato a dirlo.**

**Tre cose da fare, NESSUNA "al volo" in questo commit** (§2): riscrivere T2; decidere sul reperto
`_cs_nodo_prev` (**questione a se'**, tocca un meccanismo gia' sigillato); capire la meta' mancante
di T3 **con un criterio scritto prima**.

---

## 6-duodecies. LA CACHE `_cs_nodo_prev` (2026-09-15) — **difetto REALE, curato, sigillo 5/5. Ma NON spiega la meta' mancante di T3, e lo dico PRIMA di ri-misurare**

**IL DIFETTO.** `_cs_nodo_prev` e' scritta a **fine passo** con l'`n` di quel passo (riga ~2918). La
**mitosi aggiunge nodi**, quindi al passo dopo la guardia `len(csp) >= n` di `_tempo_luce_nodo`
fallisce e si cade nel ramo `else` -> **`cs_nodo = CS_M` costante**.

**Misurato sul file PRIMA della patch** (seme 1, scena 3 masse, 30 passi):

| | |
|---|---|
| passi con cache **inusabile** | **24 su 30** |
| chiamate finite nel **fallback** | **23 su 32 = 71.88 %** |

**Ne risentivano DUE chiamanti**, non uno: `_bloch_ritardato` (riga 2462, **lo STRATO 1, gia'
sigillato 23/23**) e il rilassamento sotto `--tau-luce` (riga 1947).

**PERCHE' NESSUN SIGILLO L'AVEVA VISTO.** Il ramo `else` **non e' un errore**: e' il fallback
legittimo per `--cs-dinamico` OFF e per il primo passo. Il codice fa quello che dice. E' la
**condizione** a essere sbagliata in presenza di mitosi. Niente NaN, niente runaway, nessuna
byte-identita' violata. **Un difetto silenzioso non si trova guardando se il codice sbaglia: si
trova contando quale strada prende.** Da qui il presidio nuovo in `CLAUDE.md` par.9:

> **Ogni ramo `else` / fallback / `getattr(..., default)` su un percorso FISICO va strumentato con un
> contatore.** Un fallback che scatta il 72 % delle volte **non e' un fallback: e' il comportamento
> principale.** E' il gemello del presidio del *valore sotto ipotesi nulla*.

**LA CURA.** Il figlio **eredita `cs` dal padre** in `_eredita_spinore_figli`: **sesta voce della
stessa convenzione** gia' usata per `_nb`, `_nb_prec`, `_nb_ret`, `omega_s`, `_psi_spinor`,
`_psi_prec`. Zero parametri, zero floor, zero valori nuovi. **Non toccati** la guardia, il ramo
`else`, la scrittura a fine passo.

**SIGILLO `csv/_seal_fork/_sigillo_fix_cache.py` — 5/5 PASS**

| | esito | numeri |
|---|---|---|
| **P1** flag OFF byte-identico | PASS | `n_A = n_B = 1692` (**confrontabili**), 21 campi, `max\|A-B\| = 0.000e+00`, RNG identico |
| **P1b** col flag ON devono DIFFERIRE | PASS | `n` 1821 contro 1771 |
| **P2** il contatore | PASS | **71.88 % -> 0.00 %** |
| **P3** `len(cache) == n` a ogni passo | PASS | **24/30 -> 0/30** |
| **P4** stabilita' | PASS | `\|nb\|-1 = 2.2e-16`, NaN/inf **0** |

**P1b non era nel mandato: l'ho aggiunto.** Senza, una patch che non fa **nulla** passerebbe P1, P3 e
P4. Il controllo necessario e' che il risultato **fisico** cambi.

### E QUI LA COSA CHE CONTA PER TE — **una premessa del mandato non regge**

P4 misura anche la dispersione di `cs` **riparato**:

```
cs cache: min 1.99954   max 2.0   (CS_M = 2)      max/min = 1.000230
```

> **`cs` varia dello 0.023 %.**

Il mandato argomentava: *«l'effetto di `tau = d/cs` puo' esistere solo quando `cs` varia, cioe' in un
quinto dei passi; con la cache attiva 1/5 del tempo, un effetto dimezzato e' quello che deve
succedere»* — e ne concludeva che la meta' mancante di T3 (misurato **-0.43** contro **-0.69**
onesto / **-1.03** naive) era **questo bug**.

**Non segue.** Il fallback **non disattivava** `tau = d/cs`: lo calcolava come **`tau = d/CS_M`**, e
**il fattore `d` era vivo nel 100 % dei passi.** Cio' che la FASE 2 sostituisce e'
`TAU_A*max(dens/dens_rif, 0.05)` con `d/cs`, e **quasi tutto quel cambiamento sta in `d`**, non in
`cs`. Il difetto congelava **solo** il fattore `cs` — che ha **2.3e-4** di escursione totale.
Attribuirgli uno spostamento di pendenza di ordine **0.3** significa chiedere a una grandezza che
varia di 2e-4 di produrre un effetto tre ordini di grandezza piu' grande.

**PREDIZIONE, scritta e committata PRIMA della ri-misura** (`doc/FIX_cache_cs.md` par.5, commit
`43e9a47`): la pendenza T3 col flag ON **non si muovera' in modo misurabile**, `|Delta|` sotto il
proprio `SE` (~0.01). Se e' cosi', vale la lettura gia' fissata dal mandato stesso: **«il bug non era
la causa: resta un residuo vero da capire. Non inventare una spiegazione: riporta e fermati.»**

**LA CURA RESTA GIUSTA COMUNQUE**, per una ragione indipendente dal residuo: `cs` e' quasi-costante
**oggi**, alle densita' attuali (`CLAUDE.md` par.6, *«a densita' reali cs e' MORTO»*). Il giorno in cui
`cs` sara' vivo, una cache scartata a ogni mitosi sarebbe un difetto **grande** — e lo sarebbe **in
silenzio**. Si ripara adesso, mentre e' innocuo e dimostrabile.

**COSA RESTA SCOPERTO.** Le vie di crescita dei nodi sono **tre**: mitosi (`:3192`), Schwinger
(`:3309`) e **`semina()` (`:1600`)**. La terza **non** passa da `_eredita_spinore_figli`. In batch e'
inerte (`semina_cont=False` di default, si accende **solo** dalla GUI), quindi **non tocca nessuna
misura committata** — ma e' sul percorso GUI, lo stesso della voce **H** di `doc/RAMIFICAZIONI.md`,
e li' e' registrata.

### ESITO DELLA RI-MISURA — **la mia predizione e' SMENTITA, e la scrivo per prima**

Quattro bracci, 300 passi, seme 1 (`csv/_test_fork/_rimisura_t3.txt`; codice committato **prima** del
run, `22a7c41`).

| braccio | pendenza | SE | r^2 | n | theta mediana |
|---|---|---|---|---|---|
| PRE  OFF | -0.1685 | 0.0090 | 0.126 | 2417 | 129.51 giri/passo |
| **PRE  ON** | **-0.4265** | 0.0091 | 0.464 | 2534 | 43.55 giri/passo |
| POST OFF | -0.1491 | 0.0085 | 0.109 | 2517 | 131.27 giri/passo |
| **POST ON** | **-0.4710** | 0.0107 | 0.417 | 2690 | 42.81 giri/passo |

> **`Delta` = -0.0445 +- 0.0141, `z` = 3.16.** Avevo predetto `|Delta|` **sotto il proprio SE**.
> **Ho predetto zero e ho misurato 3 sigma.**

**Le DUE previsioni opposte erano entrambe sbagliate.** Il mandato diceva **~50 %** (*«un effetto
dimezzato e' quello che deve succedere»*); io dicevo **zero**. **Misurato: 16.9 %** del divario verso
l'attesa onesta `-0.69`. **Restano aperti `-0.219`, e `theta` resta a 42.8 giri/passo: la FASE 2 non
si chiude.** E' il caso *«valori intermedi»* previsto dal mandato: si riporta il numero e la
frazione, **senza forzare**.

*(Controllo di validita' superato: `PRE ON = -0.4265` riproduce il `-0.43` gia' in
`doc/SIGILLO_tau_luce_FALLITO.md`. Stessa scena, confronto col numero storico valido.)*

**IL MIO ERRORE, perche' e' il tipo che si ripete.** Avevo argomentato: *«`cs` varia dello 0.023 %,
quindi non puo' spostare la pendenza»*. **Ho confrontato l'AMPIEZZA di una variazione con l'ampiezza
di una pendenza.** Una pendenza trasversale non misura **quanto** una grandezza varia, misura
**quanto la sua variazione e' CORRELATA con l'ascissa**: un fattore che cambia dello 0.02 % ma
**sistematicamente nella stessa direzione** lungo l'asse dell'inerzia **sposta la pendenza**; uno che
cambia del 50 % a caso non la sposta. **Argomento di ampiezza su una domanda di correlazione.**
Resta vero il resto — `d` era vivo nel 100 % dei passi, e i **6/7** di divario ancora aperto lo
confermano — ma *«non puo' muoverla affatto»* era falso.

### ⚠ E UN DUBBIO SUL METRO, che ti segnalo perche' vale CONTRO di me

`z = 3.16` usa le `SE` **interne a un singolo run**. Ma i due bracci ON sono **due traiettorie di un
sistema caotico** (`N` 3999 contro 4100): **il valore sotto ipotesi nulla non e' zero**, e' la
dispersione della pendenza fra run che differiscono per una perturbazione irrilevante — **mai
misurata su questa osservabile**. Per `CLAUDE.md` par.2.7 (*mai su un solo seme*) va **misurata**:
**controllo in volo**, tre semi x due bracci, `csv/_test_fork/_controllo_semi.py`, con la lettura
scritta **dentro lo script prima dei dati**. Se il segno non e' concorde sui tre semi, **il
`16.9 %` non e' un numero riportabile** e vanno corretti tutti i documenti che l'hanno gia' scritto,
questo compreso.

---

## 6-terdecies. IL CONTROLLO SUI SEMI (2026-09-15) — **ritiro il "16.9 %". Era dispersione di run.**

`csv/_test_fork/_controllo_semi.py`, 3 semi x 2 bracci, 300 passi.

| seme | ON **pre** | ON **post** | `Delta` |
|---|---|---|---|
| 1 | -0.4265 ± 0.0091 | -0.4710 ± 0.0107 | **-0.0445** |
| 2 | -0.4846 ± 0.0099 | -0.4479 ± 0.0082 | **+0.0367** ← **segno opposto** |
| 3 | -0.4412 ± 0.0080 | -0.5047 ± 0.0116 | **-0.0635** |

> `media = -0.0238`, `SE della media = 0.0307`, **`t = -0.77`**.
> **`IC95 = [-0.156, +0.108]`**: contiene lo **zero** *e* il **-0.120** dell'ipotesi «~metà».
> **Tre semi non decidono. Nessuna delle due ipotesi è esclusa.**

**IL NULLO CHE NESSUNO AVEVA MISURATO**, ed è la parte che vale per tutto il programma:

| | |
|---|---|
| `SE` **interna** a un singolo run | **~0.010** |
| dispersione **FRA SEMI, a codice INVARIATO** | **0.0302** / **0.0286** |

> **La barra giusta è TRE VOLTE quella usata.** Su questo sistema caotico la pendenza trasversale
> cambia da run a run di **0.03 senza che il codice cambi**. **Tutte** le pendenze committate in
> questo programma portano la barra piccola: le conclusioni sembrano reggere perché gli effetti sono
> grandi (il **-1.056** del tracing, il **+0.097** di `d/cs` contro `-1`, il contrasto ON-OFF
> **-0.32** = 11 volte la dispersione) **ma vanno ricontrollate una per una contro 0.03.**

**REGGE:** la **FASE 2 non si chiude** — ON post medio **-0.4745** contro l'attesa `-0.69`, divario
**-0.2155**, `SE` della media **0.0165** → **`z = 13.1`**; `theta` **30.7-44.9 giri/passo** su sei run.

---

## 6-quaterdecies. **`_psi_spin_prec`: la FASE 5 non è MAI entrata in funzione** — e questo tocca tutto ciò che è stato misurato

Cercando altri casi del pattern *«snapshot cross-passo non esteso alla mitosi»* ne è emerso un
**settimo**, e in un punto che non è diagnostico.

**FASE A** (`doc/REPERTO_psi_spin_prec.md`, 150 passi): la guardia di `ritmo()` è un'uguaglianza
**ESATTA**, quindi **un solo nodo di mitosi** la fa scartare.

| esito di `ritmo()` | | |
|---|---|---|
| guardia 4π **FALLISCE** → ricade sul **ritmo scalare a 2π** | **143/150** | **95.33 %** |
| guardia 4π passa | 6/150 | 4.00 % |
| `return` anticipato su `_psi_prec` (`r = 1`) | 1/150 | 0.67 % |

**La condizione che fallisce è una sola, in 143 casi su 143: `len(_psi_spin_prec) != n`.**
`psi_spin`, che `calcola_psi` ricostruisce **dentro** il passo, era sempre lungo `n`. Il 4π girava
**solo ai passi 2 e 3**, prima della prima mitosi.

### ⚠ LA FORMULAZIONE CONTA, e quella corrente è sbagliata

Circola già la frase *«la fisica ha integrato con un tempo proprio stale»*. **Non è vero, e l'ho
verificato.** `signed` era **già calcolato** nella versione **scalare a 2π** poche righe sopra; la
guardia decide solo se **sovrascriverlo**. `r` era **ricalcolato a ogni passo ed era valido** — il
contatore registra `len(_psi_prec) == n` in **149 chiamate su 150**.

> **La frase vera:** la fisica ha integrato con **l'orologio SCALARE STORICO**, e la doppia copertura
> **non è mai entrata in funzione.** *"Integrate male"* implicherebbe **errore numerico**;
> *"orologio diverso da quello dichiarato"* implica **modello diverso** — **e solo la seconda è vera.**
> Le misure sono **valide per il sistema che è girato davvero**, e **non valide** come misure del
> sistema col settore 4π attivo.

**Marchio registrato** in `doc/RAMIFICAZIONI.md` (secondo marchio, in testa): *«misurate col ritmo
scalare a 2π; la doppia copertura non era attiva. Da riverificare col settore 4π in funzione»* —
**T3 e i suoi quattro bracci inclusi**, cioè il divario stesso che stiamo inseguendo.

### FASE B — curato, **sigillo 6/6 PASS**

Settima voce della stessa convenzione (`vstack`, perché `psi_spin` è `n × 2` **complesso**).
Blob **`b298677a` → `08784685`**.

| | | |
|---|---|---|
| **S1** OFF byte-identico | **PASS** | `n_A = n_B = 2501`, `max\|A-B\| = 0.000e+00`, RNG identico |
| **S1b** con ON devono differire | **PASS** | `n` 2392 contro 2200 |
| **S2** contatore | **PASS** | **88.33 % → 0.00 %** |
| **S3** `len == n` | **PASS** | **54/60 → 0/60** |
| **S5** stabilità | **PASS** | `\|nb\|-1 = 2.2e-16`, NaN/inf 0 |

### ⚠⚠ E S4 HA MISURATO LA COSA SBAGLIATA — lo dice il codice, non il numero

```
PRIMA   r: mediana 1.000000    DOPO   r: mediana 0.999999    z = 0.00
```

**Quel `z = 0.00` non significa «la cura non cambia `r`»: significa che la mediana di `r` NON PUÒ
cambiare.** In coda a `ritmo()`, `x = f / median(|f|)` e `r_normalized = r / r_unit` con `r_unit` il
valore a `x = 1`: il nodo mediano ha `x = 1` **per definizione**, la mappa è **monotona**, quindi
**`median(r) = 1.0` ESATTAMENTE, con qualunque orologio.**

> **È il SECONDO caso dello stesso trabocchetto strutturale.** Il primo è `_tau = TAU_A *
> max(_dens/_dens_rif, 0.05)` con `_dens_rif = median(_dens)`. **Una grandezza normalizzata sulla
> propria mediana ha un punto fisso, e su quel punto non si misura nulla.** Presidio in `CLAUDE.md` §9.

L'unico numero informativo è la **dispersione**: `0.4421 → 0.4257` (**−3.7 %**) — **un seme, nullo
non misurato**. Per il presidio del paragrafo precedente, **non basta**.

**Quindi l'attesa «`r` cambierà in modo significativo» non è confermata, e non è nemmeno smentita:
`S4`, com'è costruito, NON PUÒ rispondere.** E **non dico che questo chiuda T3**: non è stato
misurato, e un difetto grande non implica un effetto grande — la cache `cs` lo ha appena dimostrato.

---

## 6-quindecies. **L'ANELLO DI RETROAZIONE: e se il BERSAGLIO fosse mal calcolato?** (rilievo di Luca, 2026-09-15)

È l'osservazione più utile della giornata, e **non propone un colpevole nuovo.**

### Il rilievo

L'attesa contro cui misuriamo da due giorni nasce da:

```
pendenza(theta) = pendenza(sigma) + pendenza(tau)/2
                = -1.078          + 0.097/2          ~ -1.03   (naive)
                -> -0.69 con la correzione del transitorio
```

**e assume che `sigma = coppia/inerzia` resti `-1.078` anche col nuovo `tau`.** Ma c'è un **anello**:

```
  tau  ->  omega  ->  fasi (phi)  ->  psi  ->  inerzia = |psi|^2  ->  sigma = coppia/inerzia
   ^________________________________________________________________________|
```

Cambiando `tau` cambia `omega`; `omega` fa evolvere le fasi; le fasi costruiscono `psi`; **`psi` E'
l'inerzia**. Quindi **`sigma` non è una costante indipendente: è A VALLE di `tau`.** Usare il `sigma`
misurato nel braccio **vecchio** per predire il braccio **nuovo** presuppone che l'anello non ci sia.

| | |
|---|---|
| se `sigma` nel braccio ON **non è più** `-1.078` | l'attesa **non era** `-0.69` → il "divario" è in parte **un artefatto della predizione**, non un bug da cercare |
| se `sigma` è ancora `≈ -1.078` | l'anello è debole, **l'attesa regge e il divario è reale** |

**Ciò che la rende seria:** non dice *«c'è un altro bug»*, dice *«il bersaglio contro cui misuriamo
potrebbe essere mal calcolato»*. **È l'unica ipotesi sul tavolo che non richiede di trovare qualcosa
di rotto**, e per questo va provata **per prima** fra le spiegazioni del residuo.

### La mia correzione: **il numero NON è nei dati, e non costa zero**

Il rilievo dice *«è un numero solo, già nei dati dei quattro bracci: costa zero»*. **Verificato, ed è
falso.** `csv/_test_fork/_rimisura_t3.py` calcola **solo** la pendenza di `theta` contro l'inerzia:
**zero occorrenze** di `coppia` o `sigma` in tutto lo script, e le reti non sono persistite.
**`sigma` non è mai stato calcolato né salvato. Serve un run.**

*(Lo scrivo perché è la stessa regola del registro: **un numero entra solo se è già nel repo.**
Qui non c'è.)*

### E un secondo motivo per non rifarlo com'era

Quel `sigma` andrebbe misurato su un sistema che **è appena cambiato due volte** — e la seconda ha
**acceso la FASE 5**, che sta **a monte di tutto l'anello**: `dt_n = DT*r` è il tic con cui `omega`
si rilassa (§6-quaterdecies). Misurarlo sul sistema a 2π risponderebbe alla domanda di **ieri**.

### La proposta, con il presidio di Luca incorporato **per costruzione**

Un solo script, **3 semi × 2 bracci** (~50 min), che **nello stesso run** misura `sigma`, `tau`,
`theta`, e **ricalcola l'attesa `sigma + tau/2` col `sigma` misurato IN QUEL BRACCIO**.

Così il presidio — *«se `sigma` risultasse cambiato non basta dire «ecco perché»: va RICALCOLATA
l'attesa e verificato che il divario si chiuda QUANTITATIVAMENTE, con le barre d'errore»* — **è
soddisfatto per costruzione**, non a posteriori: l'attesa ricalcolata si confronta col misurato
**contro la barra giusta (0.03, non 0.01 — §6-terdecies)**. Se non si avvicina, **l'anello non era
la causa**, e lo dirà il numero.

**Criterio scritto prima, come sempre. Registrato come fronte R** in `doc/RAMIFICAZIONI.md`.
**Non lanciato**: aspetta il via libera.

---

## 6-sexdecies. **PRIMA MISURA DEL SETTORE SPINORIALE, braccio OFF: ESITO (A)** — e l'aliasing è il doppio di quanto avevo scritto

Predizione committata **prima** del run (`c547294`), soglie in **codice** committate prima di girare
(`c8cd9d1`). 2 semi, 500 passi, blob `08784685`, osservatore **sigillato 6/6 PASS**.

| | seme 1 | seme 2 |
|---|---|---|
| `chi` **materia** | 89.9682° · `SE 0.0854` → **`z = −0.37`** | 90.0639° · `SE 0.0857` → **`z = +0.75`** |
| `chi` **p90** | 90.0210° → `z = +0.14` | 90.1174° → `z = +0.70` |
| autocorrelazione, **10 bin** (0.57–15.0) | `max\|z\| = 1.80` | `max\|z\| = 1.09` |
| frazioni `<10°` / `>170°` | 0.00745 / 0.00744 | 0.00763 / 0.00773 |

Le frazioni ai poli **coincidono entro il terzo decimale** su entrambi i semi: distribuzione
**simmetrica attorno a 90°**. Un ordinamento darebbe eccesso sotto i 10°, un'antiallineazione sopra
i 170°. **Nessuno dei due.**

**Una cosa pende e non la annuncio:** `|<n>|` è sopra il casuale su **entrambi** i semi (1.741 e
1.374). **Ma il nullo che l'osservatore stampa (`1/√N`) è la SCALA, non l'ATTESA.** Misurato con
4000 estrazioni di `N` versori casuali: **`|<n>|·√N = 0.915 ± 0.383`**, `p95 ≈ 1.59`. Contro quello:
`z = +2.11` (seme 1, **sopra** il p95) e `z = +1.16`. **Media 1.64. Va riguardata, non annunciata.**

**⚠ CORREZIONE A UN MIO NUMERO:** la predizione diceva *«`theta` resta a ~43 giri/passo»*.
**Misurato 98.65 e 92.81.** Il `43` è il valore del braccio **ON**, con `--tau-luce`; questi run
sono il sistema naturale. **Il 98–99 % dei nodi compie più di un giro intero per passo.**

**Ciò che (A) toglie di mezzo** è l'obiezione *«ma la FASE 5 non era attiva»*, che rendeva i sei lati
precedenti **non conclusivi**. **Ciò che non toglie:** (A) è l'esito che l'aliasing produrrebbe **da
solo**. Il negativo è **più pulito**, non **conclusivo**.

---

## 6-septdecies. **`--cs-dinamico` era SPENTO** — e la decisione di Luca: **ci va SEMPRE**

Rilievo di Luca, e la verifica ha dato **tre vie indipendenti concordi**.

**1) Dai dati, e non è `0` ma `nan`:** `cs_std = cs_min = cs_max = **nan**` su tutti gli 11 campioni
di entrambi i semi. **`nan` è una prova di ASSENZA, non di costanza**: uno `0` direbbe *«cs c'era e
non variava»*, il `nan` dice che **la cache `_cs_nodo_prev` non esiste.**
**2) Dal codice:** la cache è scritta **solo** dentro `if CS_DINAMICO:` — e `FORK_SU2_MEM` valeva
**1**, letto dal CSV. **Resta solo `CS_DINAMICO`.**
**3) Dal log in-run:** `CS_DIN=False` su entrambi i semi, letto dai **globali vivi** durante il ciclo.

### La decisione, e la ragione è più forte di quella numerica che avevo misurato io

Avevo argomentato sull'**ampiezza**: dove `cs` era acceso, `cs ∈ [1.99954, 2.0]` (**0.023 %**) contro
`tau = d/cs ∈ [0.0271, 1.0509]` (**×38.74**) → **`cs` pesa `0.00629 %` della dispersione di `tau`,
una parte su 15 898**. Il numero resta vero, **ma non è quello che decide**, e il mio «propongo di
lanciare com'è» era sbagliato.

> **Senza `--cs-dinamico` la cache non viene MAI scritta, quindi cade anche il `tau = d/cs` dello
> STRATO 1** (`_bloch_ritardato`), non solo quello di `--tau-luce`: **tutta la memoria del fork
> girava su una legge amputata.**
> **Un `cs` costante non è un `cs` piccolo: è un `cs` ASSENTE**, e rende `tau = d/cs` un
> `tau ∝ d` travestito. **Il punto non è l'ampiezza: è che la legge dev'essere CABLATA.**

**Correzione al rilievo:** diceva che ciò *«spiegherebbe il 16.9 % di T3»*. **No:**
`_rimisura_t3.py` riga 24 **contiene `--cs-dinamico`** — T3 girava col `cs` dinamico. E il **16.9 %
era già stato ritirato** (segno non concorde su 3 semi, `t = −0.77`). **Non c'è un 16.9 % da
spiegare.**

---

## 6-octodecies. ⚠ **IL SIGILLO 23/23 DELLO STRATO 1 NON HA MAI ESERCITATO LA DIPENDENZA DA `cs`**

Rilievo di Luca, **verificato dal disco** — e vale **due volte**, non una.

L'argv di `csv/_seal_fork/_sigillo_strato1.py` (righe **380-386**) **non contiene `--cs-dinamico`**.
E quel sigillo è del blob **`2277e9a0`**, **precedente alla cura della cache**: anche col flag
acceso, la cache sarebbe stata **scartata a ogni mitosi**.

| | |
|---|---|
| **resta valido** | il **meccanismo** del ritardo (slerp geodetico, `alpha = 1−exp(−dt_n/tau)`) e **S7**, che misura `r=2 / r=1 = **1.9753**` — dipende da **`r`**, non da `cs`: il presidio sul tempo proprio **tiene** |
| **mai testato** | che **`tau` SEGUA `cs`** — ed è *proprio* la ragione per cui `tau = d/cs` sarebbe più principiato di `tau ∝ rho` |

> **I quattro run in partenza sono la PRIMA VOLTA che quella dipendenza gira davvero.**
> **Non è «rifare la misura meglio»: è misurare per la prima volta.** *(Scritto prima che partano.)*

---

## 6-novodecies. **T3 sul sistema pulito** — il numero, e perché **non** riporto l'«11 %»

4 bracci, 300 passi, seme **1**, **con `--cs-dinamico`**, blob `08784685`.

| braccio | pendenza | SE | r² | n | `theta` | fallback |
|---|---|---|---|---|---|---|
| PRE OFF | −0.1685 | 0.0090 | 0.126 | 2417 | 129.51 giri/passo | n/d |
| PRE ON | −0.4265 | 0.0091 | 0.464 | 2534 | 43.55 | n/d |
| **POST OFF** | **−0.1024** | 0.0071 | 0.088 | 2146 | 128.88 | **0/302** |
| **POST ON** | **−0.4555** | 0.0082 | 0.567 | 2364 | **38.99** | **2/608** |

Lo script stampa `Delta = −0.0290 ± 0.0122`, `z = 2.37`, «11.0 % recuperato».
**Non lo riporto.** Quella `SE` è **interna a un singolo run**; la dispersione **fra semi** vale
**~0.030** (**C10**). Con `Delta = 0.029` e barra `0.030`, **non c'è un effetto: c'è un seme.**
**È il 16.9 % di stamattina con un'altra cifra**, e quello fu ritirato quando tre semi diedero segno
**non concorde**.

**Regge invece, contro la barra giusta:** **la FASE 2 non si chiude** (divario **−0.2345** verso
`−0.69`, `z ≈ 7.8`) · `--tau-luce` ha un effetto **grande** (ON−OFF **−0.3531**, ~12× la
dispersione) · **`theta` resta ALIASATO a 38.99 giri/passo** nel braccio migliore.

---

## 6-vicies. DUE REGOLE NUOVE, e un reperto che ne è uscito

**§10 — PROMOZIONE DELLE COMPONENTI.** Una componente sotto flag diventa fisica di default **solo**
se: ① **derivata** non tarata · ② **sigillata con CONTROLLO POSITIVO** («con ON DEVONO differire»:
un sigillo che verifica solo la byte-identità a OFF passerebbe anche su **codice morto**) ·
③ **la sua assenza è un DIFETTO, non un'alternativa**. Si promuove il **default**, non si cancella
il ramo. Registro: `doc/COMPONENTI_PROMOSSE.md`, **sezione A VUOTA**.

> **IL REPERTO:** il file ha **51 flag booleani, 10 già a `True`**. Nessuno è passato per quei
> criteri, **perché non esistevano**. Il peggiore: **`TAU_A_LOCALE`** — acceso di default, marcato
> **«IN VERIFICA» dal suo stesso commento**, e **senza flag da riga di comando**, quindi **non
> spegnibile per un A/B**: il criterio ② non è nemmeno *verificabile*. Ed è la branca che produce
> il **punto fisso auto-normalizzante** (`tau_mediano ≈ TAU_A` sempre), cioè **esattamente ciò che
> `--tau-luce` sostituirebbe**. *Una legge «in verifica» è la fisica di default da mesi, mentre la
> sua alternativa è dietro un flag i cui sigilli non passano.*

**§9 — UN DATO DEVE PORTARSI DIETRO LE PROPRIE CONDIZIONI.** Ogni CSV deve portare **blob, seme e
tutti i flag che distinguono quel run dagli altri bracci**. *Un file che si distingue dagli altri
solo per il NOME non è un dato: è un ricordo.* Caso reale: il braccio OFF aveva **136 colonne e
sette flag corretti**, ma **non `TAU_LUCE`** — l'unica variabile che distingue i due bracci — né
`CS_DINAMICO`, né blob, né seme. **Il run non era sbagliato: era non certificabile dai dati.**
Diagnosi **dal disco**: i CSV scritti alle `19:18:46`, la colonna aggiunta alle `19:23:32`,
**cinque minuti dopo**. Sanato: ora il CSV porta `TAU_LUCE`, `CS_DINAMICO`, **blob** (calcolato come
lo calcola git, senza subprocess) e **seme**.

---

## 6-unvicies. **I QUATTRO BRACCI — ESITO (A), non conclusivo. Gradiente di risoluzione 6.4×.**

4 run · 2 bracci × 2 semi · 500 passi · blob `08784685` **scritto dentro ogni CSV**.
Predizione e soglie committate **prima** (`c547294`, `b934445`). Referto: `doc/REFERTO_4bracci_4pi.md`.

**Conformità: PASS su tutti e quattro, ogni campo, letto dal CSV** — `CS_DINAMICO = 1` ovunque,
`TAU_LUCE = 0/0/1/1`, `seed = 1/2/1/2`, tutto il resto identico. **Un solo interruttore di
differenza, e stavolta è nei dati e non nel nome del file.**

### Il gradiente — il valore vero di questi run

| braccio | `theta` s1 | s2 | media |
|---|---|---|---|
| **OFF** | 101.22 | 91.53 | **96.37 giri/passo** |
| **ON** | 16.46 | 13.71 | **15.08 giri/passo** |

> **Fattore 6.39.** Atteso dal T3 (`129 → 39`): **3.3**. Al passo 300: **4.3**. **Finale: 6.39.**
> Il gradiente **cresce col tempo**, ed è il **doppio** di quanto la lettura T3 suggerisse.

### Le firme, tutte al casuale

| | `OFF_s1` | `OFF_s2` | `ON_s1` | `ON_s2` |
|---|---|---|---|---|
| `chi` **materia** | 89.7779 (`z −2.12`) | 89.8756 (`z −1.45`) | 90.0481 (`z +0.56`) | 90.0845 (`z +0.99`) |
| `\|<n>\|·√N` | 1.2373 | 0.7596 | 0.1467 | 0.8130 |
| autocorr. `max\|z\|` | 1.81 | 2.04 | 2.36 | 2.20 |

**Autocorrelazione: `max|z|` fra 1.81 e 2.36 su QUARANTA bin.** Sotto ipotesi nulla il massimo di 40
gaussiane vale ~2.2–2.5. **È esattamente il rumore.** E le **frazioni ai poli** (`<10°` e `>170°`)
coincidono **entro il terzo decimale** in tutti e quattro: distribuzione simmetrica attorno a 90°,
ed è il controllo che **non dipende dalle barre d'errore**.

### ⚠ L'unico `z` grande NON si riproduce

`OFF_s2` dà `chi_p90` con `z = −4.17` → lo script lo marca **INDETERMINATO**. Ma sull'**altro seme
dello stesso braccio** vale **−0.07**: i due differiscono di **0.63°, quattro volte la `SE` interna**.
**È dispersione di run** — la **terza volta oggi** che la `SE` interna produce un falso segnale, dopo
il `16.9 %` e l'`11.0 %`.

### Una domanda aperta si CHIUDE

`|<n>|` **non pende più**. Stamattina 1.741 e 1.374 (`z +2.11`, `+1.16`), *sempre dallo stesso lato*,
lasciata dichiaratamente aperta. Ora su quattro run: **1.237 / 0.760 / 0.147 / 0.813** — **due sotto
e due sopra** il null empirico. **Non si riproduce: era rumore.** Chiusa **con più dati, non con una
rilettura.**

---

## 6-duovicies. DUE PRESIDI DI METODO che questo run ha prodotto — e sono entrambi correzioni a me

**① DUE SEMI NON BASTANO PER UNA BARRA FRA SEMI.** Con 2 semi la deviazione standard ha **un grado di
libertà**, e `t(0.025, 1) = 12.706`: l'IC95 è **12.7 volte** la `SE` della media.

E c'è un caso reale che **sembra un segnale**: `chi` materia è **sotto 90 su entrambi i semi OFF**
(89.778, 89.876) e **sopra 90 su entrambi gli ON** (90.048, 90.084) — **segno concorde**, `z ≈ 3.5`
preso ingenuamente. **Ma l'IC95 con 1 gdl è largo 1.2° e contiene lo zero.**

> **Il segno concorde su due semi non è una prova: è un'ipotesi da rifare con quattro.**
> Registrato come **fronte S**, non come risultato, con la sua soglia: **≥ 4 semi** (`t(3) = 3.18`).
> Se reggesse, sarebbe **la prima firma non nulla del settore**.

**② UNA SOGLIA SU UN SISTEMA CHE CRESCE VA DICHIARATA CON L'ISTANTE IN CUI SI MISURA.**

```
passo  50  (n ~ 80)     cs_std/cs = 0.0086 %     margine sotto l'1 % :  116x
passo 300  (n ~ 3000)   cs_std/cs = 0.096  %                         :   10x
passo 500  (n ~ 3200)   cs_std/cs = 0.19-0.24 %                      :  ~4x
```

**Venti volte in 450 passi.** Avevo registrato il primo valore in **C13** come se fosse una proprietà
del sistema: era **un'istantanea su 80 nodi appena seminati**. **C13 regge** (siamo sotto l'1 %:
`tau = d/cs` è `tau ∝ d`) **ma la sua forza è un quarantesimo di come l'avevo scritta** — e la
traiettoria è **monotòna crescente**.

> **Conseguenza nuova:** il tempo-luce non è *«non testabile mai»*, è **«non testabile a 500 passi»**.
> A maturazione sufficiente `cs` potrebbe uscire dal regime degenere **senza turbo**.

---

## 6-tervicies. IL VERDETTO, e cosa rende dicibile

> *«Con la doppia copertura a 4π attiva, `cs` dinamico cablato per la prima volta, e il settore
> campionato a 13.7–16.5 giri per passo — **6.4 volte** meglio del braccio di riferimento — nessuna
> delle firme misurabili si stacca dal valore casuale: `chi` in materia e nel p90, le frazioni ai
> poli, `|<n>|` contro il null empirico, l'autocorrelazione su 40 bin. **Resta indeciso** se ciò
> dipenda dall'assenza di ordine o dall'impossibilità di vederlo a questa risoluzione.»*

**Ciò che (A) TOGLIE di mezzo:** le obiezioni *«ma la FASE 5 non era attiva»* e *«ma `cs` era
spento»*. **Entrambe chiuse.** È **il negativo più pulito della sessione** — non perché le barre
siano grandi, ma **perché sono piccole** (`SE ≈ 0.09°` su ~210 000 archi): un segnale **sarebbe
visibile**.

**Ciò che NON toglie:** `theta` è ancora **oltre il giro per passo**, col **96–98 %** dei nodi sopra
i 30°/passo *(prima: 99.9 %)*. **La frase «lo spin non si organizza» resta INDICIBILE** finché
`theta` non scende sotto il tetto `2π·cs/λ`.

**E il braccio ON non ha testato il tempo-luce**: con `cs_std/cs = 0.19–0.24 %` ha confrontato
**distanza contro densità** (C13), non tempo-luce contro densità.

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

### ⚠ AGGIORNAMENTO 2026-09-15 sera — **tre affermazioni di questo paragrafo erano diventate FALSE**

Le lascio visibili invece di cancellarle, perche' e' utile sapere **come** invecchia un documento:

| diceva | oggi |
|---|---|
| *"Nessun run in volo"* | **falso:** `csv/_test_fork/_controllo_semi.py` sta girando |
| *"il blob sul disco e' `f5887254`"* | **falso:** e' **`b298677a`** — era stale di **tre** blob |
| *"`soliton_simulator.py` **non e' stato toccato**"* | **falso:** e' stato toccato due volte, `TAU_LUCE` e il fix della cache |

**E TUTTI I NUMERI DI RIGA di questo repo sono shiftati.** La tabella di conversione verificata dal
disco e' in `CLAUDE.md` §9, in testa (il rilassamento di `omega_s` **1918 -> 1972**, i due commenti
stale **868 -> 901** e **1803 -> 1852**, e altri 14).

**IL CONTROLLO IN VOLO, e perche' e' contro di me.** La ri-misura T3 dice `Delta = -0.0445 +- 0.0141`,
`z = 3.16`. Quelle `SE` sono l'errore della retta **DENTRO un singolo run**, ma i due bracci sono
**due traiettorie di un sistema caotico** (`N` 3999 contro 4100): **il valore sotto ipotesi nulla non
e' zero**, ed e' la dispersione fra run — **mai misurata su questa osservabile**.
`_controllo_semi.py` la misura su **3 semi x 2 bracci**, con la lettura scritta **dentro lo script
prima dei dati**:

- segno concorde **e** `|media| > 2*SE(media)` -> **sistematico**, il 16.9 % resta;
- segno concorde ma non separato dal rumore -> **plausibile, NON dimostrato**, e il `z = 3.16` cade;
- **segno non concorde** -> era **dispersione di run**, e **"16.9 %" non e' un numero riportabile**:
  vanno corretti `doc/FIX_cache_cs.md` §6, `doc/RAMIFICAZIONI.md` C8/C8-bis, `CLAUDE.md` §9 e
  **questa relazione**.

**Cinque cose aspettano te** *(stato aggiornato al 2026-09-15 sera)*:
1. **alzare l'inerzia**, cioe' rileggere tutto dove la densita' e' O(1): toglie la causa, non il
   sintomo. E' la leva che il lavoro di oggi indica come la sola non-cosmetica;
2. **sotto-passo per lo spin** (lo stesso principio di `nsub`): presidio numerico onesto, non una
   cura. NB: con la crescita **diffusiva con plateau** misurata oggi il numero di sotto-passi
   **non diverge** — ne servirebbero ~112, non "sempre di piu'";
3. **correggere i due commenti stale**, oggi alle righe **901** e **1852** (un commit suo):
   **ANCORA NON FATTO**, e sono loro ad aver fatto partire un mandato da una diagnosi sbagliata;
4. **`_pesi()`**: FASE B non eseguita, la premessa del mandato e' falsa (`doc/REPERTO_pesi_ricorsione.md`);
5. **`:5318`**: il diaglog re-implementa `cs` inline — sotto turbo quella colonna mente.

Il **gate** e' a `c0803713` in `CLAUDE.md` §0, il blob sul disco e' **`b298677a`**. **Non
ri-timbrato di proposito**, e oggi a maggior ragione: i sigilli della FASE 2 **non passano**.
*(La frase precedente diceva `f5887254` e «il `.py` non e' stato toccato»: vera il 15 mattina,
falsa dal cablaggio di `TAU_LUCE` in poi. Storia dei blob: `f5887254` -> `968c903` (estrazione di
`_tempo_luce_nodo`) -> `7d484580` (`TAU_LUCE`) -> **`b298677a`** (fix cache + contatore).)*

Dettagli: `doc/ESITO_scan_turbo_K300.md`, `doc/REPERTO_pesi_ricorsione.md`,
`doc/PROFILAZIONE_costo_run.md`, `doc/REPERTO_gamma_condiviso.md`, `doc/PREDIZIONE_*.md`,
`doc/AUDIT_misurato_vs_asserito.md`, `STATO_CLAUDE_fork-su2.md`, `CLAUDECONNECT.md`.

---

# 9. IL GIRO DEL **2026-09-16** — blob `08784685`, invariato

> **Nessuna riga di `soliton_simulator.py` e' stata toccata oggi.** Tutto quello che segue e'
> lettura di codice, documentazione, strumenti diagnostici e sigilli. I quattro run della voce **S**
> sono **in volo** mentre questo paragrafo viene scritto (passo ~100/500): **i loro numeri NON sono
> qui**, e chi legge non deve aspettarseli.

## 9.1 — I SEI PATTERN COMPORTAMENTALI sono ora nel repo (§0-ter)

`P1..P6` stanno in **`CLAUDE.md` §0-ter** e, identici, in **§0-ter di questa relazione**.
Prima vivevano solo nella conversazione: un Claude web nuovo doveva **farseli dare di nuovo** ogni
volta. **Vanno letti prima di proporre qualsiasi cosa**, e in particolare **P1**: *l'associazione
genera candidati, non conclusioni; prima di scrivere «manca X» si rilegge dal disco.*
*(Precedenti che l'hanno generata: quattro errori dello stesso tipo in un solo giorno, elencati li'.)*

## 9.2 — **A COSA SI ACCOPPIA LO SPIN: e' uscito un TERZO esito, che il mandato non prevedeva**

`doc/MAPPA_accoppiamenti_spin.md`. Il mandato prevedeva due uscite — *«c'e' un accoppiamento,
quindi `lambda` si deriva da li'»* oppure *«non c'e', lo spin e' isolato»*. **Nessuna delle due.**

> ### **ACCOPPIATO MA SENZA BILANCIO. Lo spin parla con tutti e non deve niente a nessuno.**

**Non e' isolato — e' uno dei settori piu' connessi del file.** Decide **dove la materia si divide**
(`rho_spin` -> soglia di mitosi, `:3173`, e coppie di Schwinger, `:3316`), **quanto pesa**
(sorgente di gravita', `:1787`), **quanta inerzia ha lui stesso** (`:1952`), e — l'accoppiamento
piu' forte e il meno citato — **con che verso la gravita' tira**: in `memoria_hebbiana_moto`, che
gira a **ogni passo**, la spinta di ogni arco e' **moltiplicata per `<nb_i . nb_j>`** (`:3583-3586`),
dietro il solo `SPINORE`, che vale `True`. *Due nodi con spin antipodali si respingono invece di
attrarsi; due ortogonali non si vedono.*

**Ma nessuno di questi canali TRASFERISCE una grandezza conservata: sono MODULAZIONI.** E il punto
che decide **si dimostra dalla formula, non si misura**:

> **il torque `cross(B_i, nb_i)` NON e' azione-reazione.** Il contributo della coppia `(i,j)` vale
> `(w_ij/deg_i)*cross(nb_j,nb_i)` su `i` e `(w_ij/deg_j)*cross(nb_i,nb_j)` su `j`: **opposti solo
> se `deg_i == deg_j`** — e questo grafo non e' regolare. In piu', sui legami fra chiralita'
> **uguali** il vicino entra **RIFLESSO** (`z -> -z`), e li' l'antisimmetria non e' rotta da una
> normalizzazione: e' **rotta nella struttura**.

E **nel file non esiste nessuna funzione di energia totale**: `grep -i energ` da' solo commenti,
`lambda_vuoto` (una densita' locale) e il termostato Nose-Hoover (`:2767-2806`) — che e' gated su
`REGIME == "deterministico"`, quindi **spento in tutti i run di questo programma**, e che comunque
agirebbe su `phivel`, **non** su `omega_s`. Lo spinore poi e' normalizzato **`|psi| = 1` in modo
atomico a ogni passo** (`:2128-2129`): **non ha ampiezza, quindi non ha energia** da scambiare.

**Conseguenza diretta, ed e' la terza ragione indipendente dopo il FDT e la FASE 1:**
**`lambda` NON SI DERIVA.** Non perche' manchi un canale: perche' **manca la grammatica**. Cablare
Gilbert resterebbe una **manopola** (§3). La voce **B** del registro passa da *«non aperto»* a
**CHIUSA COME NON DERIVABILE**.

**`TW_SPINORE` non e' «un canale aperto in un verso solo»: e' CHIUSO IN ENTRAMBI.** `tw -> nb`
esiste (`:1990-1996`) ma e' gated su `TW_SPINORE = False`, come `SPIN_LARMOR`; e **`nb -> tw` non
esiste**: la dinamica di `tw` (`:2878-2883`) e' guidata da **`dph`**, la differenza di fase, e non
contiene ne' `nb` ne' `omega_s`.
**⚠ DA NON CONFONDERE CON C11:** li' era la **FASE 5**, l'**orologio** a 4pi in `ritmo()`, cablato e
curato; qui e' `TW_SPINORE`, il **torque** a 4pi, **spento di proposito**. Due cose diverse con lo
stesso «4pi» nel nome.

**COSA QUESTO NON DICE (dichiarato):** che il torque non conservi si **dimostra**; **quanto** non
conservi **non e' misurato**. La misura che lo chiuderebbe costa dieci righe e **zero run nuovi**:
`|SOMMA_i cross(B_i,nb_i)| / SOMMA_i |cross(B_i,nb_i)|` — `~1/sqrt(n)` sarebbe rumore di somma,
`O(1)` violazione grande. **Non fatta oggi.**

## 9.3 — MISURA F e G nell'osservatore, e il **SIGILLO 6/6 PASS**

Per rispondere alla voce **R** servivano `sigma`, `tau` e `theta` **nello stesso run**: sono state
aggiunte all'osservatore come **MISURA F** (le tre pendenze trasversali, con `SE`, `r^2`, `n`, piu'
`t3_attesa = b_sigma + b_tau/2` e `t3_divario`) e **MISURA G** (gli ingredienti del conto FDT).

**La scelta di metodo che conta:** MISURA F **non ricostruisce** la catena di `omega`, **riusa**
`_tracing_omega.ingredienti`. Riscriverla avrebbe riesposto all'errore del 15 — il termine
`cross(_nb_grav(), nb)` omesso, che valeva **~2.8 volte** il deterministico. E poiche' quella
ricostruzione **non contiene** `Bg` ne' `_otw`, e' valida **solo con `SPIN_LARMOR` e `TW_SPINORE`
spenti**: per questo sono **colonne del CSV** (P6) e la conformita' li controlla.

**Sigillo dell'osservatore rigirato, ora con `--cs-dinamico` anche nei suoi run: 6/6 PASS.**
`O1.0` nodi **3020 = 3020** (il confronto **esiste**, prima di leggere lo zero) e `O1`
**`max|A-B| = 0.000e+00`**. Contava davvero: MISURA F chiama `ritmo()`, `_pesi()`, `calcola_psi()` e
`_nb_grav()` — **tutte funzioni che MUTANO cache lette dalla dinamica** — su una copia profonda.

## 9.4 — IL GATE: **resta indietro, e ora c'e' scritto perche'**

Blob sul disco **`08784685`**, gate **`c0803713`**. Fra i due ci sono **tre** cambiamenti e **non
hanno lo stesso stato**: il cablaggio di **`--tau-luce`** ha il **sigillo FALLITO**, mentre le cure
**C7** (5/5) e **C11** (6/6) sono sigillate. **Basta il primo a bloccare il timbro**: il gate
certifica **un blob**, non un sottoinsieme dei suoi cambiamenti.
**Lettura operativa, perche' «gate indietro» non vuol dire «codice non fidato»:** un run **senza**
`--tau-luce` gira su un file il cui unico delta non sigillato e' **inerte**; un run **con**
`--tau-luce` gira su un ramo **esplicitamente non certificato**, e va detto nel documento che lo usa.

## 9.5 — DUE CORREZIONI AL MANDATO, ENTRAMBE SCRITTE **PRIMA** DI ESEGUIRE

`doc/PREDIZIONE_risigillo_strato1.md`. Il §6.2 chiedeva di rilanciare il sigillo dello Strato 1
*«con `--cs-dinamico`, resto identico»*.

1. **«Resto identico» non e' possibile, e S1a/S1b FALLIRANNO — legittimamente.** Fra il blob di
   riferimento (`968fba34`, pre-Strato 1) e `08784685` c'e' **C11**, che **non e' gated su
   `FORK_SU2_MEM`**: gira in ogni run `--campo-spinoriale`. Nel codice nuovo la guardia esatta di
   `ritmo()` passa, nel vecchio falliva nel **95.33 %** delle chiamate. Due orologi diversi -> due
   `r` -> due `dt_n` -> **traiettorie diverse**. **Byte-identita' con un blob che ha un orologio
   diverso sarebbe una CONTRADDIZIONE, non un successo.** *(C7 invece e' un no-op esatto con MEM
   OFF: la cache non esiste.)* Va detto prima, o domani si legge «da 23/23 a N/23» e si conclude una
   **regressione** dove c'e' una **cura che ha fatto il suo mestiere**.
2. **Aggiungere `--cs-dinamico` all'argv NON BASTA a esercitare la dipendenza da `cs`.** Verificato
   dal disco: nei sigilli **in-process** `_cs_nodo_prev` e' `None` (`:330`) oppure
   `np.full(nodi, cs)` (`:224`) — **COSTANTE**. Un `cs` costante non esercita `tau = d/cs`: lo rende
   indistinguibile da `tau ∝ d`. `--cs-dinamico` cambia solo i **tre run veri**; **S7**, il presidio
   piu' fine del lotto, misura la dipendenza da **`r`**, non da **`cs`**.
   **Rilanciare il sigillo com'era avrebbe lasciato il marchio esattamente dov'era.**

**Percio' e' stato scritto il SIGILLO 8**, l'unico del lotto che fallirebbe se `cs` fosse ignorato:
quattro nodi con **`cs = 1, 2, 4, 8`**, stessa `d`, **`r = 1` su tutti** — l'opposto esatto di S7,
che varia `r` e tiene `cs` fisso — e si verifica `alpha = 1 - exp(-dt_n*cs/d)` **nodo per nodo**.
Con `S8b` (il rapporto `cs=8 / cs=1`: se `cs` fosse ignorato varrebbe **esattamente 1.000000000**)
e `S8d`, la controprova con `cs` costante, perche' S8 non possa passare per un artefatto dello slerp.
**In volo mentre scrivo: l'esito non e' qui.**

## 9.6 — IL MERGE IN `main`: piano scritto, **niente eseguito**

`doc/PIANO_merge_main.md`. **Il fatto che cambia il quadro:**

> ### **`main` NON HA MAI TOCCATO `soliton_simulator.py`.**
> `blob: merge-base 194a9456 | main 194a9456 | fork-su2 08784685`

I 20 commit che `main` ha in piu' sono **tutta documentazione** (`CLAUDECONNECT.md` +479 righe,
`Checkpoint.md` +212, `CLAUDE.md` +26, e la cancellazione di 4 file spazzatura).
**Non e' un merge di codice, e' un merge di RACCONTO**, e i conflitti reali — da prova a secco con
`git merge-tree`, che non tocca il working tree — sono **due soli file**: `CLAUDE.md` e
`CLAUDECONNECT.md`.

**Due dei tre presidi del registro non erano dove si credeva:** il **rename dello STATO** e' **gia'
risolto** (`main` non ha **nessun** file di STATO; quello a rischio e' di `dev-spinoriale`, e solo
se si cancella quel branch), l'**AVVISO** e' **chiuso** oggi, e il **ri-timbro del gate** e' il vero
blocco. **E c'e' una trappola operativa che nel registro non c'era:** `main` e' estratto in un
**worktree separato** (`C:/Users/lpeano/st_main`), quindi un `git checkout main` dalla cartella
principale **fallisce** finche' quel worktree esiste.

**RACCOMANDAZIONE: non adesso.** `main` e' oggi **l'unico branch il cui codice coincide con un blob
certificato**; portarci `08784685` significherebbe **perdere l'ultimo punto fermo** mentre la voce
**A** e' aperta. Il pericolo vero non e' il merge mancante: e' che qualcuno **legga `main` e creda
che sia lo stato del progetto**. Una riga in testa a `CLAUDE.md` **di `main`** — *«branch FERMO al
2026-09-10, il lavoro vivo e' su `fork-su2`»* — toglie il 90 % del danno con lo 0 % del rischio.

## 9.7 — UNA DISCREPANZA FRA IL MANDATO E IL DISCO

Il TODO di oggi dice che `AVVISO_LAVORO_IN_CORSO.md` *«NON esiste piu': e' stato chiuso. Non
cercarlo»*. **Esiste**: 8042 byte, ultimo commit `8447f47`, e il contenuto era **stale** (blob
`f5887254`, gate `c0803713`, «nessun run in volo» al 15 a mezzogiorno).
**L'ho SVUOTATO e marcato CHIUSO, non cancellato**, con la tabella di dove sta ora ciascuna cosa che
conteneva: il contenuto era gia' tutto altrove, e cancellarlo avrebbe lasciato la **discrepanza**
senza traccia. **Se Luca lo vuole rimosso e' una sua decisione, non mia.**
*(L'unica cosa non replicata altrove e' stata conservata: le fonti auditate — `ROADMAP:46`/`:42`,
`PROTOCOLLO:41-44`, `STATO:112`/`:433` — **non sono state corrette**, ed e' una decisione di Luca.)*

## 9.8 — COSA E' ANCORA IN VOLO (e quindi cosa NON e' in questa relazione)

| | stato |
|---|---|
| **voce S** — `chi` materia, 4 semi per braccio | **4 run in volo**, 500 passi, passo ~100 al momento della scrittura |
| **voce R** — attesa `sigma + tau/2` ricalcolata | **negli stessi run** (MISURA F). Nessun numero ancora |
| **dispersione di `r`** | idem. Su 2 semi era ~10 % piu' alta nell'ON; **serve la barra fra semi** |
| **conto FDT rifatto** | idem (MISURA G). I tre numeri — `lambda`, `tau_smorz` vs `tau_disordine`, `kT/Lam` — **non ci sono ancora** |
| **ri-sigillo Strato 1 + S8** | **in volo** |

> **Quindi: oggi nessun numero fisico nuovo.** Quello che c'e' e' **una diagnosi strutturale
> (`lambda` non si deriva)**, **due correzioni a un mandato fatte prima di eseguirlo**, **un sigillo
> di purezza 6/6**, e **tre decisioni di igiene scritte invece che rimandate**.

## 9.9 — **I DUE `theta` SONO CHIUSI** (C19): ora girano insieme, e ne e' uscita una correzione alla catena

`theta` non era un'osservabile sola. `_rimisura_t3.py` `:73` usa `theta = |omega|*DT` (tempo di
**COORDINATA** — la convenzione di **C8** e dell'attesa **`-0.69`**); MISURA F usa
`theta = |omega|*dt_n` (tempo **PROPRIO**, quello giusto per §9). **Finche' ne girava una sola, un
numero che si muoveva poteva essere fisica oppure l'unita' di misura che cambia** — ed era gia'
successo.

**Ora l'osservatore scrive ENTRAMBE, fianco a fianco, nello stesso campione:** `theta_coord_*`,
`theta_prop_*` e **`r_ratio_*`**, il loro rapporto, che **e' `r`** (la FASE 5 agisce proprio li').
In MISURA F: `t3_b_theta_coord`, `t3_b_theta_prop`, **`t3_b_r`**.
**Nessuna delle due e' stata dismessa** — la giusta e' `prop`, ma tutto lo storico e' in `coord` e
serve per rileggerlo. **`theta_*` senza suffisso resta come LEGACY ed E' `theta_prop`**: gli 8 CSV
gia' committati e i due script di verdetto la leggono con quel nome, e rinominarla li avrebbe resi
illeggibili. *(Deviazione dichiarata rispetto al mandato, che chiedeva «mai `theta` nudo».)*

**E quanto conta? Al primo campione di prova, 120 passi: `theta_coord = 107.7` contro
`theta_prop = 85.3` giri/passo — il 26 % di differenza sulla mediana.** Non e' un dettaglio.

**Controllo di identita' cablato:** poiche' `theta_prop = theta_coord * r` sullo stesso campione,
deve valere `pend(prop) - pend(coord) - pend(r) = 0` **esattamente**. La colonna `t3_identita`
misura **`4.6e-16`**. Se un giorno non fosse ~`1e-12`, l'errore e' **nel codice, non nella fisica**.

> ### E LA CORREZIONE CHE NE E' USCITA, che non era nel mandato
> Da `|omega|_eq = |F|*sqrt(dt_n*tau/2)` con `dt_n = DT*r`:
> ```
> pend(theta_coord) = sigma + tau/2 +   r/2
> pend(theta_prop)  = sigma + tau/2 + 3*r/2
> ```
> **La formula usata finora, `sigma + tau/2`, ASSUMEVA `pend(r) = 0` — in ENTRAMBE le convenzioni,
> e non era mai stato verificato.** Ora `t3_b_r` lo misura.
> *(Il **divario** resta pero' **indipendente dalla convenzione**: `divario_prop − divario_coord =
> pend(r) − pend(r) = 0`, verificato nei dati. Quindi il residuo non spiegato della voce **R2**
> non era un artefatto di convenzione.)*

---

## 9.10 — **TAGLIO SPETTRALE: predizione scritta, cablaggio NON fatto.** Tre premesse del mandato non reggono

`doc/PREDIZIONE_taglio_spettrale.md`. Il mandato metteva **P1 in vigore** e chiedeva di segnalare,
non eseguire, ogni affermazione in contrasto con un fatto misurato. **Ce ne sono tre.**

**① LA RICORSIONE DATA NON RIDUCE L'AMPIEZZA: PRESERVA LA VARIANZA, esattamente.**
Per `x' = a x + b g` la varianza stazionaria e' `b^2/(1-a^2)`; con `b^2 = 1-a^2` vale **1**, cioe'
quella del rumore bianco. Verificato: **analitico `1.000000`, simulato `0.997330`** su 400 000
passi, `tau_c = 0.400` = 40 passi. **Cambia solo la STRUTTURA TEMPORALE, non l'ampiezza.**
La stima «varianza /20 -> ampiezza /4.47» descrive un oggetto **diverso** (banda limitata a densita'
spettrale costante) e per ottenerlo servirebbe **moltiplicare per `sqrt(2 dt/tau_c)`**, cioe'
**toccare `amp`** — che il mandato vieta e che sarebbe **un coefficiente scelto** (§3).
**Le due prescrizioni del mandato sono incompatibili fra loro.**

**② IL RUMORE NON MUOVE IL BLOCH. Lo muove `omega`, di tre ordini di grandezza.**
Misurato sui quattro run di oggi:

| run | calcio del rumore | moto del Bloch | rapporto |
|---|---|---|---|
| OFF s3 / s4 | **7.68 / 8.44** gradi/passo | 37 874 / 37 866 | **0.020 % / 0.022 %** |
| ON s3 / s4 | **7.23 / 9.42** | 5 705 / 4 274 | **0.127 % / 0.220 %** |

Il «kick da ~90 gradi» **non esiste**: vale **7-9 gradi**. Il `85.6` citato e' reale ma e' lo
spostamento del **padre nel passo della nascita su n = 7** (`doc/BILANCIO_ordine_spin.md:97`, che
scrive esso stesso *«se regge sulla statistica»*) — **non una misura del rumore**.
E dal codice: sotto `--spinore-corretto` il `_nb` committato e' **derivato da `_psi_spinor`**, quindi
il calcio del rumore viene **sovrascritto**: il rumore entra **solo nella COPPIA**, via
`cross(B, nb)`.

**③ E QUELLA COPPIA E' GIA' MISURATA MARGINALE: `R_stoc = 0.041` contro l'errore atteso `0.097`
(C6).** Il taglio agisce su un canale che vale il **4 %** dell'ingresso di `omega`, **senza
cambiarne l'ampiezza**. Non c'e' via per cui `theta` scenda di 4.5x.

> **PREDIZIONE CORRETTA: `theta` NON SCENDE. Se si muove, SALE** (≲ 5 %). Una forzante **correlata**
> su 40 passi fa crescere `omega` stocastico come **`n`** invece che `sqrt(n)` — fino a `sqrt(40)
> ~ 6.3` **sulla sola componente stocastica**, che pero' vale il 4 %.
> **E l'ipotesi qualitativa del mandato non puo' verificarsi:** richiede che il rumore domini la
> decorrelazione del Bloch, e la domina allo **0.02-0.22 %**. `B` e' costruito da `_nb_prec`, il
> Bloch committato, il cui moto e' `omega`. **Colorare il rumore non puo' stabilizzare `B`.**

**COSA RESTA IN PIEDI, ed e' la parte che conta:** *«si fa perche' il rumore bianco e' fisicamente
SBAGLIATO»*. **Questa giustificazione regge intatta** e non dipende da nessuna delle tre
correzioni: `tau_c = LAM/CS_M` e' **derivato**, la ricorsione **non introduce coefficienti**.
**Il cablaggio ha senso — ma per correggere una legge sbagliata, aspettandosi che NON cambi i
numeri.**

**E una correzione da fare comunque, se si cabla:** **il `dt` della ricorsione dev'essere
`dt_n = DT*r`, non `DT`**. Il mandato non lo dice; §9 e' esplicito che `DT` nudo dentro un processo
locale impone **un frame preferito**. **E' l'errore gia' preso nello Strato 1**, che S1..S6
passavano identici e solo **S7** ha stanato: **serve un sigillo tipo S7 fra N1 e N6**, o passerebbe
invisibile come allora.

**Serve il via di Luca su una cosa sola: quale delle due prescrizioni incompatibili vale.**

---

## 9.11 — **IL TAGLIO SPETTRALE E' CABLATO** (flag OFF), e il sigillo e' a meta': N1/N1b PASS, poi SI E' SCHIANTATO

> **Via libera di Luca, 2026-09-16**, dopo aver letto e accettato le tre correzioni del §9.10:
> *«il cablaggio resta legittimo, ma per la sola ragione onesta — e senza aspettarsi niente su
> `theta`»*. **Risolve l'incompatibilita' del mandato in favore di `amp` INTOCCATA: rumore
> DIVERSO, non rumore MINORE.**
>
> **Blob: `08784685` -> `c5e5088c` -> `a467fd9a`.** Due commit di codice, entrambi **prima** di
> qualsiasi run (§5). **Il flag nasce OFF.**

### 9.11.1 — Come e' cablato

```
tau_c = LAM / CS_M = 0.400  = 40 passi        # tempo-luce del solitone: DERIVATO
a = exp(-|dt_n| / tau_c)      b = sqrt(1 - a^2)
xi = xi*a + b*g                               # g = la STESSA rng.normal(0,1,(n,3)) del ramo bianco
_nb += xi * amp                               # amp INVARIATA
```

Il ramo OFF e' **letteralmente invariato** (`_calcio = _g`), e **`g` e' estratto PRIMA del ramo**,
nella stessa posizione di prima: cosi' il braccio spento consuma l'RNG **esattamente** come faceva.
E' la condizione che rende possibile N1.

**Tre scelte di costruzione, dichiarate:**
1. **`dt_n = DT*r`, non `DT`** — il rumore e' un processo **locale** del nodo; `DT` nudo
   imporrebbe la foliazione sincrona globale, cioe' **un frame preferito** (§9).
2. **`xi` inizializzato da `N(0,1)`, cioe' dalla distribuzione STAZIONARIA.** Partire da zero
   darebbe un primo calcio attenuato di `b = 0.22` per ~40 passi: **un artefatto all'accensione**.
   Costo dichiarato: **un'estrazione RNG in piu'**, che rende impossibile una byte-identita' di
   run intero per N2 — per questo N2 e' scritto come **controllo mirato**.
3. **Eredita' di `_xi_rumore` alla mitosi**, stessa convenzione di `_nb`/`_nb_prec`/`_nb_ret`/
   `omega_s`/`_psi_spinor`/`_psi_prec`/`_cs_nodo_prev`/`_psi_spin_prec`. **E' la terza volta**
   (C7, C11): **stavolta scritta PRIMA di misurarla, non dopo.**

### 9.11.2 — ⚠ UN DIFETTO TROVATO LEGGENDO IL CHIAMANTE, non aspettando che esplodesse

> **`_passo_spinoriale` NON riceve `dt_n`: riceve `dt_n_s`** (`:2931`).

E `dt_n_s` (`:2747-2751`), sotto **`--tempo-segno`** (MOD 5.3a, Feynman-Stuckelberg), vale
`(1 + (perc_chi-1)*m_coer) * dt_n`, che per l'**antimateria coerente e' NEGATIVO**.
Con `dt_n < 0` verrebbe `a = exp(+|dt|/tau_c) > 1` e la ricorsione **sarebbe divergita IN
SILENZIO**: nessun NaN subito, solo `xi` che cresce di passo in passo finche' il Bloch smette di
avere senso. Da qui **`|dt_n|`**: il tempo di correlazione e' una **durata**, dipende dal modulo
del tic, non dal verso. **Nessun numero nuovo** — e' la stessa classe di guardia dei
`np.maximum(..., 1e-9)` gia' nel file.

**Oggi `TEMPO_SEGNO = False` e non cambia un bit.** Lo scrivo lo stesso perche' **un difetto che
esiste solo in una combinazione di flag e' esattamente quello che salta fuori fra sei mesi**,
quando nessuno ricorda che le due cose interagiscono.

### 9.11.3 — ⚠⚠ LA TRAPPOLA CRLF HA MORSO **DA SOLA**

Fra il commit `7f2af6c` e il cablaggio, `soliton_simulator.py` era tornato **CRLF** (442240 byte,
6510 CRLF, sha1 grezzo `37c31630`) **senza che io avessi lanciato nessun `git checkout`**.
L'ha fermata l'`assert '\r\n' not in s` che avevo messo in testa allo script di patch: **senza,
avrei scritto un file misto.**

> **E' la seconda volta in una giornata.** La prima l'avevo causata io con `git checkout`; questa
> e' arrivata da sola. **Il `.gitattributes` con `soliton_simulator.py text eol=lf` non e'
> cosmesi: e' l'unica cosa che toglie la trappola alla radice.** Resta una decisione di Luca.

### 9.11.4 — IL SIGILLO: due PASS, poi uno SCHIANTO

```
[PASS] N1.0   il riferimento e' il blob PRE-cablaggio      blob = 08784685 (atteso 08784685)
[PASS] N1.0b  stesso numero di nodi (il confronto ESISTE)  PRE = 3020, POST(OFF) = 3020
[PASS] N1     flag OFF vs codice pre-cablaggio             max|A-B| = 0.000e+00
[PASS] N1b    ON != OFF (il flag FA qualcosa)              35 array divergenti
```

**Il ramo OFF e' intatto e il flag non e' codice morto. Questo e' stabilito.**

> **⚠ E N1b NON VA LETTO COME MISURA DI UN EFFETTO.** I nodi finali sono **3020 (OFF) contro 2449
> (ON)**, ma il ramo ON consuma **un'estrazione RNG in piu'** all'inizializzazione, quindi le due
> traiettorie divergono **completamente dal primo passo**: e' **caos con semi diversi**, non
> l'ampiezza di un effetto fisico. N1b prova **solo** che il flag fa qualcosa.

**POI LO SCHIANTO:**
```
AttributeError: 'numpy.random._generator.Generator' object attribute 'normal' is read-only
```
La spia di N7 monkeypatchava `net.rng.normal`, che in numpy e' **read-only**. **N2, N3, N6 e N7
non sono girati.**

> **E' lo stesso modo di fallire del sigillo dello STRATO 1 di stamattina: NON FALLISCE, SI
> SCHIANTA** — la modalita' piu' facile da non notare. Due volte in un giorno, su due sigilli
> diversi, per la stessa ragione strutturale: **un guscio in-process che tocca il simulatore
> pezzo per pezzo si rompe appena il simulatore cambia forma.**
> **Corretto:** la spia ora avvolge l'**oggetto** `rng` con un proxy che inoltra tutto e registra
> solo `normal` (`net.rng` e' un attributo normale, quindi sostituibile). Resta pure-read: non
> cambia ne' l'ordine ne' il numero delle estrazioni.

### 9.11.5 — E IL CRITERIO SBAGLIATO ERA MIO — il contatore lo ha detto prima di schiantarsi

`_xi_fallback = 2` su 36 chiamate nella costruzione della scena. **Non e' un difetto**, e il
perche' conta: il ramo di estensione scatta quando i nodi crescono **senza passare da
`_eredita_spinore_figli`**, cioe' su **`semina()` e `nuova_massa()` — LA TERZA VIA DI CRESCITA,
la voce H del registro**. Li' l'estensione e' **corretta**: i nodi esistenti **conservano** il
loro `xi` (vstack sulla testa) e **solo i nuovi** ricevono un'estrazione stazionaria, perche' un
nodo appena nato non ha passato.

> **Quindi il criterio di N3b che avevo scritto era SBAGLIATO:** *«fallback <= 1»* **in assoluto**
> avrebbe fatto **fallire il sigillo per una ragione legittima**.
> **Corretto in DELTA:** sui 25 passi di sola mitosi l'estensione **non deve scattare affatto**,
> perche' li' l'eredita' deve bastare. **E' il criterio che misura la cosa giusta**, e la
> differenza fra i due non e' stilistica: uno avrebbe prodotto un FAIL falso, e un FAIL falso
> costa piu' di un sigillo mancante, perche' si porta dietro una diagnosi.

### 9.11.6 — COSA E' ANCORA IGNOTO

| | stato |
|---|---|
| **N2** — `tau_c -> 0` collassa sul rumore bianco | **non girato** |
| **N3 / N3b** — `_xi_rumore` esteso alla mitosi | **non girato** |
| **N6** — stabilita', `\|nb\| = 1`, no NaN/runaway | **non girato** |
| **N7 / N7b / N7c** — **la ricorsione usa `dt_n = DT*r` per nodo, e col `DT` nudo NON tornerebbe** | **non girato — ED E' QUELLO CHE DECIDE** |
| campagna `{OFF, ON} x >= 2 semi` | **non lanciata** |

> **N7 e' il sigillo che conta, e la ragione non e' ovvia:** N1..N6 provano la **struttura** — ramo
> OFF intatto, il flag fa qualcosa, lo stato si eredita, nulla esplode — e **passerebbero IDENTICI
> anche se la ricorsione usasse `DT` nudo**, cioe' col tic di **coordinata** al posto del tempo
> proprio del nodo. **E' esattamente il bug gia' preso nello Strato 1, dove S1..S6 passavano
> identici e solo S7 lo ha stanato.**

**E la predizione resta quella del §9.10, invariata:** `theta` **non scende**, e se si muove
**sale** (<= 5 %). **Si e' cablato perche' il rumore bianco e' fisicamente sbagliato, non perche'
risolva l'aliasing.** Se il verdetto dovesse mostrare un calo significativo, **il reperto sarebbe
a mio carico**: vorrebbe dire che uno fra C6, il rapporto 0.02-0.22 % e la conservazione della
varianza non regge.

---

## 9.12 — **STOP AI TEST. DUE CORREZIONI DI DIFETTO, SENZA FLAG.** E `M2`, il sigillo decisivo, **PASSA**

> **Decisione di Luca, 2026-09-16:** i test in corso si interrompono, e due difetti entrano nel
> codice **senza flag**, come **correzioni di difetto** (categoria **D** del registro: *un bug
> curato non ha un interruttore*).
> **Blob: `a467fd9a` -> `57681b9e` -> `c57800c1`.** Due commit di codice, uno per correzione,
> **entrambi prima di qualunque run** (§5).
>
> ### ⚠ MARCHIO SU TUTTI I DATI PRECEDENTI
> **Ogni misura di questo repo prodotta prima del blob `c57800c1` e' «prodotta con `_xi_rumore`
> EREDITATO alla mitosi e SENZA il fattore `cs^-2` nell'inerzia: misura di un sistema DIVERSO da
> quello corrente».** Vale per gli 8 CSV della campagna, per i sigilli di oggi, e per tutto cio'
> che sta in §9.1-9.11.

### 9.12.1 — La trappola CRLF e' chiusa alla radice

`.gitattributes` con `*.py|*.md|*.csv|*.txt|*.json text eol=lf` e i binari marcati `binary`.
**Provato con lo stesso comando che aveva causato il danno stamattina:**
```
git checkout -- soliton_simulator.py  ->  444654 byte, 0 CRLF, sha1 a467fd9a   INVARIATO
```
*(La regola non riscrive nulla: fissa cio' che gia' c'e'. Verificato prima e dopo
`git add --renormalize .`: byte identici.)*

### 9.12.2 — CORREZIONE ① : `_xi_rumore` NON si eredita — **e l'analogia sbagliata era MIA**

Stamattina avevo aggiunto l'eredita' di `_xi_rumore` alla mitosi, scrivendo che era *«la stessa
convenzione di `_nb`/`_nb_prec`/`_nb_ret`/`omega_s`/`_psi_spinor`/`_psi_prec`/`_cs_nodo_prev`/
`_psi_spin_prec`»* e **vantandomi di averla scritta PRIMA di misurarla** invece che dopo (C7, C11).

> **L'analogia era FALSA, e averla applicata in anticipo non la rende giusta.**
> Quegli otto sono **proprieta' del NODO**: e' corretto che il figlio le erediti.
> **`xi` no: e' un campione dell'AMBIENTE che spintona il nodo, un processo ESTERNO.**
> **Due nodi distinti non ricevono lo stesso identico spintone.**

**Cosa produceva:** padre e figlio con rumore **correlato al 100 %** per ~40 passi
(`tau_c = LAM/CS_M`) — una correlazione **spuria** fra oggetti che devono essere indipendenti, e
**proprio nella grandezza che serve a decorrelare**.

**La correzione e' una CANCELLAZIONE**: si toglie il blocco, e il figlio riceve un `xi` **fresco**
dal ramo di estensione gia' presente, che estrae dalla **stazionaria** (`N(0,1)`, coerente con
`b = sqrt(1-a^2)`) — non da zero, che sarebbe un transitorio artificiale. **Nessun feedback sul
padre:** il rumore non e' una quantita' che si ripartisce.

**E i contatori cambiano nome, perche' cambia il loro significato:** `_xi_fallback` ->
`_xi_esteso` + `_xi_nuovi`. **L'estensione non e' piu' un fallback: e' IL PERCORSO NORMALE della
mitosi.** Chiamarla «fallback» avrebbe fatto leggere come difetto il comportamento **corretto** —
ed e' esattamente l'errore che avevo gia' fatto scrivendo il criterio di N3b, che avrebbe prodotto
un **FAIL falso**.

### 9.12.3 — CORREZIONE ② : il fattore `cs^-2` nell'inerzia

`inerzia = max(rho, 1e-6)` **non aveva alcuna dipendenza da `cs`**. La derivazione la impone
(`doc/INERZIA_tempo_quadro.md`, esito **(b)**): `correzione` e' adimensionale e `omega` e' `1/T`,
quindi `correzione/inerzia` deve dare `1/T^2` -> **`inerzia` e' un TEMPO AL QUADRATO**, e il tempo
proprio del nodo e' `d/cs` -> **`inerzia ∝ (d/cs)^2 ∝ cs^-2`**.
**Esponente DERIVATO, verso CONFERMATO** (Compton con `c -> cs`), e **lo stesso esponente dello
Step 2** (`omega_clk *= (cs/CS_M)^2`), derivato **prima e indipendentemente**: consistenza
**trovata**, non costruita.

**Forma:** `inerzia = max(rho * (CS_M/cs_nodo)^2, 1e-6)`. Adimensionale, **esattamente 1** dove
`cs = CS_M`. Nessun coefficiente nuovo, nessun floor nuovo; `cs_nodo` dalla cache
`_cs_nodo_prev` col fallback **contato** (P5).

**Perche' e' una correzione di CONSERVAZIONE:** alla mitosi il figlio riceve un'inerzia nuova e il
padre non ne perde, quindi **`L_tot = somma(I*omega)` cresce a ogni divisione**. `omega` e'
intensiva — un corpo rigido che si spezza mantiene `omega` in ogni frammento — quindi **e'
l'inerzia che deve ripartirsi, e non lo fa**. Con `inerzia ∝ cs^-2` la nascita di un figlio alza
la densita' locale, abbassa `cs` locale, e **l'inerzia di padre e figlio aumenta insieme**: un
feedback **mediato dal campo**, che non richiede di sottrarre nulla al padre — cosa peraltro
impossibile, perche' `|psi|^2` e' **ricalcolata dalle fasi**, non e' una variabile di stato.

**Una scelta di struttura, dichiarata:** la lettura di `_cs_nodo_prev` e' scritta **inline** e non
estratta in un metodo, benche' gemella di quella in `_tempo_luce_nodo`. **Duplicazione
consapevole:** oggi **tre sigilli si sono rotti** perche' un metodo estratto non era nei gusci
in-process. Il commento marca i due punti come da tenere allineati.

### 9.12.4 — ✅ `M2`, IL SIGILLO DECISIVO: **PASS**

> `(CS_M/cs_nodo)^2` vale **esattamente 1** dove `cs = CS_M`, e **`rho * 1.0 == rho` bit per bit**
> in IEEE. Quindi **senza `--cs-dinamico`** (cache mai scritta -> fallback a `CS_M`) il codice
> NUOVO **deve** essere byte-identico al riferimento. Se non lo fosse, **la FORMA del fattore
> sarebbe sbagliata**, e ci si ferma li'.

```
M2   nodi PRE = 3070, POST = 3070      <- il confronto ESISTE (le shape PRIMA dello zero)
     34 array numerici confrontati
     max|A-B| = 0.000e+00              array divergenti: 0          PASS
M2b  con --cs-dinamico: 3020 contro 3101 nodi, 35 array divergenti  PASS (il fattore MORDE)
```

**`M2b` e' il controllo opposto e serve tanto quanto `M2`:** senza, `M2` passerebbe anche su un
fattore **inerte**, cioe' su codice morto.

### 9.12.5 — E IL NUMERO CHE IL MANDATO CHIEDEVA DI DICHIARARE PRIMA

| | |
|---|---|
| `cs` | `[1.994899, 2.000000]` |
| `cs_std / cs` | **0.0333 %** |
| fattore `(CS_M/cs)^2`, **mediana** | **1.000004812** |
| scarto **massimo** da 1 | **5.1e-03** |

> **L'attesa scritta prima e' confermata:** il fattore vale **1.0000048** sul nodo mediano.
> **L'effetto quantitativo OGGI e' minuscolo**, esattamente come dichiarato nel commit **prima** di
> guardare i dati. **La correzione si e' fatta perche' senza la legge e' SBAGLIATA**, non per un
> effetto misurabile a questa densita'.

**E una precisazione che va fatta, perche' il numero non e' nessuno dei due gia' citati:** il
`cs_std/cs` misurato qui e' **0.033 %**, mentre C13 riporta **0.0086 %** al passo 50 e **0.24 %**
al passo 500. Questi run sono a **150 passi**, e la traiettoria di quel rapporto e' **monotona
crescente**: il valore sta **dentro** la forbice, ma **non e' nessuno dei due estremi**, e citarlo
come se lo fosse sarebbe stato sbagliato.

### 9.12.6 — IL SIGILLO E' ATTERRATO: **11/13 PASS, due FAIL — ed entrambi sono CRITERI MIEI SCADUTI**

```
[PASS] M0   riferimento = blob a467fd9a         444654 byte, 0 CRLF (sha1 dei BYTE GREZZI)
[PASS] M0b  il codice corrente e' DIVERSO       c57800c1, 448943 byte, 0 CRLF
[PASS] M0c  nessuno dei due ha CRLF             .gitattributes in vigore
[PASS] M2.0 il confronto ESISTE                 nodi PRE 3070 = POST 3070
[PASS] M2   cs = CS_M -> BYTE-IDENTICO          max|A-B| = 0.000e+00        <- IL DECISIVO
[PASS] M2b  con cs VIVO il fattore MORDE        3020 contro 3101, 35 array divergenti
[PASS] M1   PRIMA il rumore era CORRELATO       corr = +1.0000
[FAIL] M1b  DOPO dev'essere INDIPENDENTE        corr = nan su 0 coppie
[FAIL] M3   len(_xi_rumore) == n a ogni passo   estensioni 24, nodi con xi fresco 1734
[PASS] M4   la conservazione e' calcolabile     (misura, non timbro)
[PASS] M5a  |nb| = 1                            max||nb|-1| = 2.220e-16 su 3101 nodi
[PASS] M5b  nessun NaN/inf                      tutti finiti
[PASS] M5c  nessun runaway                      max|x| = 9.355
                                                SIGILLO CORREZIONI: 11/13 -> FAIL
```

**`M1` da' `corr = +1.0000`, non il `+0.951` che avevo previsto**, e il motivo e' che misuro al
**momento dell'eredita'**, prima che il passo successivo li faccia divergere: il difetto era
**massimo**, non attenuato. **Meglio cosi' per il sigillo:** un controllo positivo piu' netto.

**I DUE FAIL: VERIFICATI, non spiegati via.** Ho misurato invece di argomentare:

| | |
|---|---|
| `len(xi)` **dopo `step()`** | **allineato**: 1608=1608, 1652=1652, 1703=1703, 1750=1750 |
| `len(xi)` **dopo `mitosi()`** | **corto**: 1608 contro 1652, 1652 contro 1703, 1703 contro 1750 |

**`M3` controllava a FINE passo, cioe' DOPO `mitosi()`** — dove l'array e' legittimamente corto,
**perche' con la correzione ① l'estensione avviene dentro `_passo_spinoriale`**, che e' la **prima**
cosa del passo dopo. **L'array non e' mai stale quando viene USATO**: chi lo usa lo estende prima.
**Il criterio giusto e' «allineato dopo `step()`», e il mio era scritto per la versione EREDITATA.**

**`M1b` dava `0 coppie` per la stessa ragione**: subito dopo la mitosi i figli **non hanno ancora**
un `xi`, quindi non c'era niente da correlare. Misurato **uno step dopo**, su una scena vera:

> ### **corr(xi_padre, xi_figlio) = +0.0065 su 258 coppie** — contro **+1.0000** prima della correzione.
> **La correzione ① funziona.** Il rumore di padre e figlio e' indipendente.

**Ma il sigillo resta FAIL finche' non lo rigiro con i criteri giusti**, e il fallimento e'
committato com'e' (§5). **Un criterio scaduto che produce un FAIL falso costa piu' di un sigillo
mancante**, perche' si porta dietro una diagnosi — ed e' la **seconda volta oggi** che scrivo un
criterio per una versione del codice che nel frattempo e' cambiata (la prima fu `N3b`,
«fallback <= 1»).

### 9.12.7 — Dove eravamo rimasti coi test, e cosa resta

**Il sigillo del rumore colorato era a 12/13 prima dello STOP:**
> **`N7` E' VINTO** — `max|xi_mis - xi_atteso(dt_n)| = **0.000e+00**` nodo per nodo, contro
> **`6.142e-01`** col `DT` nudo, `std(a)` fra i nodi `1.133e-02`. **Il tic della ricorsione E' il
> tempo proprio del nodo.**

L'unico FAIL era **`N2`**, e la causa era **mia, tre volte diverse**: alzare `CS_M` piantava il
**CFL** (46 minuti al 68 % di CPU: *non falliva, si piantava*); abbassare `LAM` **spegneva il
campo** (`Lam = 0` -> la guardia saltava l'intero blocco del rumore -> `n/d`); la via giusta —
alzare `CS_M` **solo dentro `_passo_spinoriale`** — e' scritta ma non ancora eseguita.

| | stato |
|---|---|
| `M1b` e `M3` coi criteri corretti | **da rigirare** (il difetto e' nel criterio, ed e' misurato) |
| metriche §3 nell'osservatore (`L_tot`, `r` per eta', corr `xi`, fattore `cs`) | **da fare** |
| campagna `{OFF, ON} x >= 2 semi` sul sistema corretto | **da rifare** |
| `N2` del rumore colorato | **da rigirare** sul nuovo riferimento |
