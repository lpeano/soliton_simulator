# REGISTRO DELLE COMPONENTI — promosse / candidate / esperimenti / correzioni

> Branch `fork-su2` · creato **2026-09-15** · blob al momento della creazione **`08784685`**
> (verificato dal disco). La regola che questo registro applica è **`CLAUDE.md` §10**.
> **In questo giro non è stata promossa nessuna componente.** La sezione **A è vuota di proposito.**
> Si aggiorna **nello stesso commit** del riscontro che lo cambia (§5-bis).

**I tre criteri (§10), in breve:** ① **derivata**, non tarata · ② **sigillata**, *con controllo
positivo* · ③ **la sua assenza è un DIFETTO, non un'alternativa**.
**Il ③ è quello che decide**, ed è quello che non si riempie per inerzia.

---

## ⚠ LA COSA DA LEGGERE PER PRIMA — **lo strato che ha saltato il processo**

Verificato dal disco: `soliton_simulator.py` ha **51 flag booleani di modulo, di cui 10 già a
`True`**. Nessuno dei dieci è mai passato per i tre criteri, **perché i tre criteri non esistevano
fino a oggi**.

| riga | componente | nota dal suo stesso commento |
|---|---|---|
| 258 | `SCHERMATURA` | «LEGGE INTRINSECA: portata ancorata alla densità critica adattiva» |
| 268 | `TAU_LOCALI` | costanti temporali come **rapporti adimensionali** |
| 270 | `CALORE_VETTORIALE` | «True = vettoriale+chirale DI DEFAULT» |
| **274** | **`TAU_A_LOCALE`** | **«IN VERIFICA»** — e vedi sotto |
| 544 | `REPULS_LEGGE` | repulsione emergente, «legge» |
| 597 | `TORS_4PI` | torsione a doppia copertura |
| 605 | `MEM_HEBB` | memoria hebbiana del moto |
| 678 | `FRAME_DRAG` | *(nessun commento)* |
| 680 | `GRAV_BIFASE` | legge gravitazionale bifase |
| 694 | `SPINORE` | «NB: l'EVOLUZIONE è orfana» |

### `TAU_A_LOCALE` — il caso che il registro esiste per rendere visibile

**È acceso di default, è marcato «IN VERIFICA» dal suo stesso commento, e NON ha un flag da riga di
comando** (tre sole occorrenze nel file, nessuna assegnata da argomenti). Quindi:

- **non è spegnibile per un A/B** → il criterio ② non è nemmeno *verificabile*: non esiste il ramo
  OFF su cui fare la byte-identità;
- è la branca che produce `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` con **`_dens_rif` = mediana**,
  cioè **il punto fisso auto-normalizzante** già registrato in `CLAUDE.md` §9 (`tau_mediano ≈ TAU_A`
  *sempre*, a qualunque maturazione);
- ed è **esattamente ciò che `--tau-luce` sostituirebbe**.

> **Una legge dichiarata «in verifica» dal proprio autore è la fisica di default da mesi, e la sua
> alternativa è dietro un flag OFF di cui i sigilli non passano.** È il rapporto rovesciato rispetto
> al problema che ha generato questa regola, e va guardato per quello che è.

*(Non lo classifico né in A né in B né in C: non è promosso — non ha i criteri — non è candidato —
è già acceso — e non è un esperimento. **È uno stato che la regola §10 non prevede, e il primo
compito della regola è stanarlo.**)*

---

# A. FISICA CERTIFICATA — ON di default

## A1. **`STEP2_OROLOGIO`** — aggancio OROLOGIO ↔ METRICA · `omega_clk *= (cs/CS_M)²`

> **PROMOSSA il 2026-09-16** (decisione di Luca, dopo la **FASE A**: `doc/REFERTO_faseA_sigilli.md`).
> Blob al momento della promozione: **`c57800c1`** (quello su cui il sigillo è stato eseguito).
> **È la PRIMA voce di questa sezione: fino a oggi nessuna componente era passata per i tre criteri.**

### ① DERIVATA, non tarata — **SÌ**

È l'**orologio di Compton**: `ω = m c²/ħ`, e nel modello `c` **è** `cs`. Quindi `ω ∝ cs²` non è una
scelta, è **la sola forma dimensionalmente possibile**. **Zero parametri, zero floor, zero
coefficienti.** Misurato dal sigillo: `omega_eff/omega_base = (cs/CS_M)²` a **`3.469e-18`** (`S3`),
e a `cs = CS_M` il fattore vale **`1.000000000000000` esatto** (`S3c`) — cioè la riduzione al limite
è **per costruzione**, non per taratura.

> **CONSISTENZA TROVATA, NON COSTRUITA — e va detta perché è il vero argomento:** lo **stesso
> esponente** `cs²` è stato derivato **per una strada indipendente** nel settore dell'inerzia
> (`inerzia ∝ cs⁻²`, da `inerzia = T² = (d/cs)²`, `doc/INERZIA_tempo_quadro.md`, cablata il
> 2026-09-16 come **correzione di difetto**). Due derivazioni che non si parlano, **stesso `cs²`**.

### ② SIGILLATA **con controllo positivo** — **SÌ**, `csv/_seal_fork/_sigillo_step2.py`

| test | cosa dimostra | misura |
|---|---|---|
| **`S3.0`** | **IL CONTROLLO POSITIVO**: il test **VEDE** l'effetto | **39/40 nodi** con `\|f(1)−f(0)\| > 1e-13` |
| `S3` | la legge è quella dichiarata | `max\|mis − atteso\| = 3.469e-18` |
| `S3b` | l'orologio **rallenta** dove `cs` è basso | `0.0100` volte a `cs = 0.1·CS_M` |
| `S3c` | a `cs = CS_M` il fattore è 1 **esatto** | `1.000000000000000` |
| **`S2`** | **riduzione al limite sul blob ATTUALE**: ON (`cs=CS_M`) vs OFF **byte-identico** | `0.000e+00` con **nodi 2924 = 2924** |
| `S4a/b/c` | stabilità | `\|psi\|=1` a `4.441e-16`, nessun NaN, `max\|x\| = 9.254` |
| **`S1`** | **FAIL ATTESO** — vs blob `2277e9a0`, di **quattro cambiamenti fa** | nodi **3164 contro 2924**, 32 shape |

> **Si cita «9/10 + 1 FAIL ATTESO», MAI «10/10».** Il `S1` che fallisce è un
> `max\|A−B\| = 0.000e+00` con **shape diverse** = **mancanza di confronto**, non identità
> (`CLAUDE.md` §9). **Il confronto che conta è `S2`, ed esiste davvero: 2924 = 2924.**
>
> **E senza `S3.0` questo sigillo non basterebbe:** un sigillo di sola byte-identità a OFF
> **passerebbe anche su codice morto** (§10 ②). `S3.0` è la ragione per cui questa voce è qui e le
> altre tredici no.

### ③ LA SUA ASSENZA È UN **DIFETTO**, non un'alternativa — **SÌ** (motivazione di Luca)

> ### «**Un sistema in cui l'EM non risponde alla metrica è un sistema SBAGLIATO, non diverso.**»

La fase U(1) **evolveva già** senza lo Step 2: ciò che mancava non era il moto dell'orologio, era che
**rispondesse alla curvatura**. Un orologio che non rallenta nel pozzo non è un modello alternativo
di gravità: è un modello **senza** redshift gravitazionale, cioè privo di un accoppiamento che in
fisica **c'è sempre**. È il caso puro del criterio ③: *«il sistema senza X è SBAGLIATO»*.

**E non è promossa per inerzia** (§10 lo vieta esplicitamente): fino a ieri era **OFF di default** e
**non è mai stata accesa in una misura committata**. Il suo argomento è il ③, non l'abitudine.

### COME è promossa, nel codice

- `STEP2_OROLOGIO = True` di modulo (`:793`), col riscontro dei tre criteri **nel commento**;
- resta **`--senza-step2-orologio`**, marcato **«DIAGNOSTICO, non fisica alternativa»**;
- `--step2-orologio` **resta accettato come NO-OP** (avvisa e non fa nulla): non rompe gli script,
  e chi lo passa lo legge a video;
- il prerequisito (`--campo-spinoriale` + `--deparam-orologio`) **non è un no-op silenzioso**:
  stampa un **AVVISO GRAVE** che dichiara che il run gira su **fisica amputata rispetto al default**;
- la colonna CSV **`STEP2`** dell'osservatore scrive il valore **EFFETTIVO** (dopo il controllo del
  prerequisito), non quello richiesto.

> **⚠ DUE ADEGUAMENTI OBBLIGATI, e sarebbero stati errori gravi se dimenticati.**
> Dal 2026-09-16 **l'assenza del flag significa ON**. Quindi:
> - `_sigillo_step2.py` prende il braccio OFF con `--senza-step2-orologio` — **senza, `S2` avrebbe
>   confrontato ON contro ON e sarebbe PASSATO SEMPRE**: un falso PASS della classe già catalogata
>   in `CLAUDE.md` §9 (*«`0.000e+00` per mancanza di confronto»*);
> - `_osserva_vuoto.py` ha ora **`--senza-step2`**, e il vecchio `--step2` è un no-op dichiarato.
>
> **Ogni altro braccio "OFF" ottenuto per OMISSIONE del flag, in qualunque script, da oggi è ON.**

### RETROCESSIONE — il criterio, scritto **ORA** (§10)

> **Torna a flag** se un riscontro **committato** mostra che `_phc` **non è una fase globale** —
> cioè se una firma di **SPIN** (Bloch, `chi`, `spin_overlap`, olonomia) si muovesse per effetto
> dello Step 2 **oltre la dispersione fra semi** (P3: **0.03** sulle pendenze, mai la `SE` interna).

**Perché è questo il punto debole giusto da sorvegliare:** tutta la legittimità dello Step 2 come
fisica *dell'orologio* poggia sul fatto che `_phc` moltiplichi `a1` e `b1` per lo **stesso** fattore
(`:2212-2213`, **uniche occorrenze nel file**), lasciando `nb = ψ†σψ` invariante — misurato
**`3.3e-16`**. Se quella proprietà cadesse, lo Step 2 starebbe **organizzando lo spin**, cosa che il
suo stesso messaggio dichiara di non fare (*«NON muove il Bloch e quindi NON organizza lo spin»*).
**Non retrocede per ripensamento, né perché un run "va peggio".**

**COSA QUESTA PROMOZIONE NON DICE:** non dice che lo Step 2 **migliori** alcuna osservabile. Dice
che la sua **assenza è un difetto**. Le sue conseguenze misurabili sul settore U(1) sono ancora da
misurare — **è esattamente a quello che serve la MISURA U**, cablata nello stesso giro.

---

> **Il resto della sezione era VUOTO fino al 2026-09-16.**
>
> **⚠ MA C'È UNA DECISIONE OPERATIVA IN VIGORE, presa da Luca il 2026-09-15:**
> **`--cs-dinamico` va acceso in OGNI misura, sempre.** Non è (ancora) una promozione del default
> nel codice — il criterio ② non è completo, manca un sigillo con controllo positivo — ma
> **è vincolante per come si lanciano i run**, ed è scritta in `CLAUDE.md` §4.
> *Distinzione che conta: una regola d'uso non è una promozione. La promozione si fa nel codice,
> col suo sigillo e col suo criterio di retrocessione.*

---

# B. CANDIDATE — da valutare, **NON promosse**

Per ciascuna: i tre criteri col riscontro che li sostiene, e **il verdetto sul ③, che è quello che
decide**.

| # | componente | ① derivata? | ② sigillata + controllo positivo? | ③ **assenza = difetto o alternativa?** |
|---|---|---|---|---|
| **B1** | **`--deparam-orologio`** | **SÌ** — «zero parametri» nel suo commento | byte-identità a OFF dichiarata; **controllo positivo: non risulta** | **DIFETTO — ed è l'unica con una base documentata.** Senza, `omega_clk` viene da `\|Psi\|²` **estensiva** / `rho_c` **GLOBALE**. `CLAUDE.md` §4 vieta la non-località: *«la media globale introduce NON-LOCALITÀ, una scorciatoia che il sistema relazionale non deve avere»*. **Il sistema senza non è diverso: viola una regola del progetto.** |
| **B2** | **`--spinore-corretto`** | sì per costruzione (evaluate-then-commit, `\|psi\|=1`) | «Default off = byte-identico»; controllo positivo **non risulta** | **PLAUSIBILE, non dimostrato.** Il nome dice «gestione CORRETTA», e senza non c'è commit atomico né normalizzazione. Ma *nessun riscontro committato* mostra che il ramo OFF produca uno stato **sbagliato** — solo diverso. **Serve la misura, non l'aggettivo nel nome.** |
| **B3** | **`--verlet`** | è una scelta di **integratore**, non una legge | «attivare per il confronto A/B» | **PLAUSIBILE, e c'è una TENSIONE da risolvere.** Il suo commento dice «INTEGRATORE METRICO **SPERIMENTALE**»; `CLAUDE.md` §4 **prescrive** Verlet per il second'ordine con inerzia. Le due frasi non possono essere entrambe vere. E **nessuno ha mai misurato la deriva di energia** del ramo Eulero: senza quel numero, ③ è un'opinione. |
| **B4** | **`--spinore-vivo`** | sì (reinnesto nell'ordine ETC, zero parametri) | «Reversibile, per A/B; **richiede rimisura di Berry**» | **NON STABILITO.** Senza, lo spinore è **congelato**. §4 dice che spinori **passivi** sono un bug — ma quella clausola parla del caso in cui *il link li comanda*, che è un'altra situazione. **Non la uso per inerzia.** |
| **B5** | **`--chi-core`** | «nessun segno selezionato a priori» | «default off per A/B» | **NON STABILITO.** Il suo commento lo presenta come un **A/B**, non come una correzione. |
| **B6** | **`--campo-spinoriale`** | sì (FASE 1, riduzione al limite esatta) | «Default off = byte-identico»; **il FASE-5 ci si appoggia** | **ALTERNATIVA, non difetto.** Il suo stesso commento dice «**non ancora agganciato** a gravità/forze/mitosi». Un sistema senza il campo emesso spinoriale **non è rotto: è un modello diverso**. ⚠ **Ma senza, la FASE 5 non gira affatto** — quindi è un *prerequisito* di altre candidate, non una candidata forte per sé. |
| **B7** | **`--fork-su2`** | sì (Berry non normalizzato, il peso `cos(chi/2)` **è ciò che resta non normalizzando**) | sigillato (Strato 0) | **ALTERNATIVA — e c'è di più: da solo è INERTE PER TEOREMA** (`<psi_i\|N\|psi_j> = 2<psi_i\|psi_j>`, misurato **1.57e-15** su 200 000 coppie). **Promuoverlo da solo non cambierebbe un bit.** Promuoverlo avrebbe senso solo insieme a B8. |
| **B8** | **`--fork-su2-mem`** | sì — `tau = d/cs`, «nessun numero nuovo, `d` e `cs` esistono già» | **23/23 PASS**, S7 incluso — **⚠ MA con `cs` COSTANTE:** l'argv del sigillo non ha `--cs-dinamico`, quindi il ritardo girava su `tau = d/CS_M`. Il **meccanismo** e' sigillato, **la dipendenza da `cs` no**. Il ② e' **parziale** | **ALTERNATIVA, oggi.** È il pezzo che **accende** il fork. Ma dire «senza è sbagliato» presuppone che il non-abeliano sia **stabilito**, e non lo è: la sua resa non è ancora dimostrata (le firme sono a valore casuale, `doc/ESITO_prima_misura_4pi.md`). **③ si potrà riempire quando il fork avrà prodotto qualcosa di misurabile, non prima.** |
| **B9** | **`--step2-orologio`** | **SÌ** — orologio di Compton `omega ∝ cs²`; «fisica NECESSARIA e derivata: zero parametri nuovi, nessun floor, nessun coefficiente» | **10/10 PASS**, e include **S3.0**, il controllo che il test *veda* (`\|f(1)−f(0)\| > 1e-13` su 39/40 nodi) — **è un controllo positivo vero** | **PLAUSIBILE, ma BLOCCATO da ③ per una ragione fisica:** §6 dice che **a densità reali `cs` è MORTO** (`I ~ 0.05` contro soglia `~400`), quindi il fattore vale ~1 e **la sua assenza oggi non è misurabilmente un difetto**. Dimostrarlo richiederebbe il **turbo**, cioè un forzante. |
| **B10** | **`--tau-luce`** | **SÌ** — `d/cs`, lo stesso `tau` già cablato nello Strato 1, coefficiente **1** | **NO — criterio ② NON SODDISFATTO.** I sigilli della FASE 2 **non sono passati** (T2 difetto del test, T3/T4). `doc/SIGILLO_tau_luce_FALLITO.md` | **NON VALUTABILE finché ② non passa.** ⚠ **Ma è la componente che ha generato la regola**: escluderla da una misura come se fosse il turbo è l'errore di categoria del §10. E **abbassa `theta` da ~96 a ~43 giri/passo**: è l'unica leva di risoluzione esistente. |
| **B11** | **`--cs-dinamico`** | sì (`cs = CS_M/(1+GAMMA√I)`, **stesso `GAMMA`** di `G(rho)`) | A/B storico; **nessun controllo positivo** | **⭐ DIFETTO — decisione di Luca, 2026-09-15: «CS DINAMICO SERVE E DEVE ESSERCI SEMPRE».** Senza, `_cs_nodo_prev` non viene **mai** scritta, quindi cade il `tau = d/cs` **dello STRATO 1**, non solo quello di `--tau-luce`: la memoria del fork gira su una legge amputata. **È la prima voce con il ③ pieno insieme a B1.** ⚠ Il ② resta da completare (serve un sigillo con controllo positivo) prima di poterla promuovere |

---

## B-bis. **`TW_SPINORE` — CANDIDATA SOSPESA: la legge codificata non e' quella dichiarata**

> **Aggiunta il 2026-09-16, nello stesso commit del riscontro** (§5-bis). Era **la prima candidata
> indicata da Luca** per l'accensione dopo lo Step 2. **Non e' stata accesa, e non e' stato scritto
> il suo sigillo.** -> `doc/REFERTO_tw_spinore.md`, voce **W** di `doc/RAMIFICAZIONI.md`.

| criterio §10 | stato |
|---|---|
| ① **derivata, non tarata** | **SI', in linea di principio** — `tw/2` e' spin-1/2 geometrico, `PHI_CRIT` e' gia' nel sistema, nessun coefficiente nuovo. **Ma cio' che il codice implementa non e' quella formula** (sotto) |
| ② **sigillata con controllo positivo** | **NO, e non si puo' scrivere adesso.** Il criterio naturale (*«ruota il Bloch di `tw/2`»*) **fallirebbe di 628** — non per un difetto del codice, ma perche' verrebbe **dalla descrizione invece che dal codice**. Sarebbe il **quarto** criterio stale in due giorni |
| ③ **assenza = difetto?** | **NON VALUTABILE** finche' ① non e' chiuso: non si giudica l'indispensabilita' di una legge di cui non si sa quale sia |

**IL RISCONTRO, in tre numeri** *(209 852 archi, 150 passi, seme 1, `--cs-dinamico` acceso)*:

| | | valore |
|---|---|---|
| **(a)** | **DICHIARATO** dal commento: angolo/passo `= tw/2` | **9.827e-01 rad** |
| **(b)** | **CODIFICATO** (`:2149`): `tw/(4π)` sommato a `omega_new` | **1.564e-01** |
| **(c)** | l'angolo che (b) produce davvero `= (b)·dt_n` | **1.564e-03 rad** |
| | **(a)/(c) `= 2π/DT`** | **628.3** |

**E dove finisce:** in `self.omega_s` (`:2313`), la **memoria persistente** — mentre il commento di
`SYNC_SPINORE` (`:724`), **dello stesso blocco**, dice che metterci un torque *«darebbe
accumulo/divergenza»*. E, **unico fra i termini del blocco**, `_otw` **non e' diviso per l'inerzia**.

> **COSA QUESTO NON DICE: che sia trascurabile.** Il peso in **ampiezza** e' **0.054 %**, ma la
> domanda e' **direzionale** — l'asse TW e' **fisso e persistente**, `omega` e' un **random walk**.
> Confondere le due cose e' l'errore **ampiezza-contro-correlazione** gia' commesso su `cs` allo
> 0.023 % (§9): **non si rifa' al contrario.** *(Ed e' proprio la proprieta' per cui Luca l'aveva
> scelta per prima: «l'unico meccanismo il cui asse non svanisce all'allineamento».)*

### ✅ DECISIONE DI LUCA, 2026-09-16: **STRADA 3 — RESTA SPENTO.**

> **La componente NON si accende e il cablaggio NON si tocca in questo giro.** Resta **candidata
> SOSPESA**: non e' respinta (① e' plausibile in linea di principio), non e' promossa (② non e'
> scrivibile finche' il codice e la descrizione dicono cose diverse).
> **Cosa la riaprirebbe:** una decisione di fisica su quale delle due leggi sia quella voluta.
> **Fino ad allora il flag resta OFF e il suo commento resta FALSO** — presidio in `CLAUDE.md` §9,
> perche' il rischio vero non e' dimenticarla: e' **riaccenderla credendo di aggiungere `tw/2`**.

**LE TRE STRADE, per il verbale** *(la 3 e' quella scelta)*:
1. **correggere** il cablaggio -> allora e' una **CORREZIONE DI DIFETTO** (§10: *nessun flag*), e la
   legge corretta si sigilla e si valuta da capo;
2. **tenerlo com'e'** e sigillarlo **per quello che fa davvero**, riscrivendo il commento;
3. **lasciarlo spento** e passare a un altro dei tredici.

**Finche' non decide, resta OFF.**

---

# C. ESPERIMENTI — OFF **per sempre**

| # | componente | perché è qui |
|---|---|---|
| **C1** | `--gamma-turbo` | **dichiarato dal codice stesso**: «[DIAGNOSTICO, **NON PERCORSO CERTIFICATO**] amplificatore della SENSIBILITÀ di `cs` alla densità». **Amplifica un parametro**: è la definizione di forzante. |
| **C2** | `--kuramoto-su2` | meccanismo di allineamento **aggiunto a mano**, non derivato. E **refutato per misura**: K-frozen **byte-identico** a OFF, K-noise = NO-rumore (`doc/RAMIFICAZIONI.md` **B5**). |
| **C3** | `--regime` (deterministico, ecc.) | cambia **quattro interruttori insieme** (`TAU_A`, `G_PH`, `_CALORE_INIT`, `SCUOTIMENTO`) — contro §1, *un interruttore alla volta*. Utile come **A/B a variabile singola solo** dove è stato verificato che ne cambi uno (sigillo O2). |

> **Correzione dichiarata al mandato:** il mandato metteva **`--step2-orologio`** in questa sezione
> «finché non validato». **L'ho spostato in B9.** La proprietà che definisce **C** è, per il mandato
> stesso, *«meccanismo **aggiunto a mano** invece che derivato»* — e lo Step 2 è **derivato**
> (orologio di Compton, zero parametri, riduzione al limite esatta per costruzione) **e sigillato
> 10/10 con controllo positivo**. Metterlo fra gli esperimenti sarebbe **lo stesso errore di
> categoria** che la regola §10 esiste per impedire, commesso nel documento che la applica.
> Il suo blocco è **③**, ed è scritto in B9.

---

# E. ESCLUSE PER DIMOSTRAZIONE — **spente, e non si riaprono con una misura**

> **Creata il 2026-09-16** dall'audit di lettura chiesto da Luca (*«quali leggi hanno senso fisico,
> quali no, quali vanno integrate meglio»*). **Verificate riga per riga dal blob `a44adc31`.**
>
> ### LA REGOLA CHE QUESTA SEZIONE APPLICA
> **Si MISURA per PROMUOVERE, si DIMOSTRA per ESCLUDERE.** Una misura dice *«questa legge produce
> un effetto»*; **non dice se ha senso**. `SPIN_LARMOR` produceva un effetto ed era **sbagliata**;
> il fattore `cs^-2` non ne produce quasi e **e' necessario**.
> **Quindi:** per escludere una legge non basta *«non produce effetto»* — **si deve dire QUALE
> PROPRIETA' ROMPE**, e la proprieta' va citata col suo punto nel codice.
> **E per questo non si riaprono con una misura:** una voce chiusa qui torna in gioco solo se cade
> la **dimostrazione**, cioe' se quella proprieta' non e' piu' richiesta o se il codice cambia.
>
> ### IL CODICE DELLE ESCLUSE NON SI CANCELLA
> Resta spento, ed e' **l'evidenza che spiega perche' esistono i loro sostituti**: `TW_SPINORE`
> esiste **perche'** `SPIN_LARMOR` fallisce. Cancellare il secondo farebbe perdere il **perche'**
> del primo. *(Stessa ragione per cui si promuove il default invece di cancellare il ramo, §10.)*

| flag | **quale proprieta' ROMPE** | riga | **cosa la RIAPRIREBBE** (scritto ora) |
|---|---|---|---|
| **`SPIN_LARMOR`** | **Si autoannulla dove servirebbe.** L'asse e' `cross_ij = np.cross(nb_vic[ii], nb_vic[jj])`: **si annulla esattamente all'allineamento**, cioe' quando l'ordine comincia. Non e' debole: e' **nullo per costruzione** proprio nel regime che dovrebbe sostenere | **`:2065`** | un asse che **non** sia il prodotto vettore dei due Bloch — cioe' una legge diversa, non una taratura di questa |
| **`TW_SPINORE`** | **L'implementazione non e' la legge dichiarata.** Commento `tw/2` (un ANGOLO), codice `tw/(4π)` sommato a una **VELOCITA'**: **628.3 = 2π/DT** volte piu' debole. E finisce in `self.omega_s` (memoria persistente) contro il divieto scritto **nello stesso blocco** per `SYNC_SPINORE` (*«darebbe accumulo/divergenza»*). **Unico del blocco, non e' diviso per l'inerzia** | **`:2149-2154`**, `:2313`, divieto a `:724` | **PRINCIPIO BUONO, implementazione rotta:** riaprirebbe una **correzione del cablaggio** (e allora e' §10-D, *senza flag*). -> `doc/REFERTO_tw_spinore.md` |
| **`POLO_MATURO`** | **Rende SIMMETRICO un termine che dev'essere ANTISIMMETRICO.** Sostituisce `chi[i] - chi[j]` con `np.where(_twn[i] >= _twn[j], chi[i], chi[j])`: il secondo seleziona il nodo a torsione maggiore, quindi **non cambia segno invertendo l'arco**, mentre `tw` e' una torsione su arco **ORIENTATO** e l'altro addendo (`dph`) e' antisimmetrico. La somma perde parita' definita. **Il commento ammette lo scopo:** *«rompe il bilanciamento»* -> **tattica, non legge** | **`:3032`** contro `:3034` | una costruzione **antisimmetrica** che selezioni comunque il polo maturo (p.es. `sign(twn[i]-twn[j]) * (chi[i]-chi[j])/2`): sarebbe **un'altra legge**, da sigillare |
| **`VERSO_CHI`** | **No-op silenzioso.** `if CHI_CORE …` arriva **prima** di `elif VERSO_CHI …`, e `--chi-core` e' nella config di **ogni** run: il ramo **non e' mai raggiunto**. Accenderlo fa credere di aver aggiunto una legge senza aggiungere nulla | **`:2881`** / **`:2884`** | solo un run **senza** `--chi-core` — ma §4 lo richiede sempre. **Di fatto irraggiungibile** |
| **`L_CONSERVA`** | **Distrugge una proprieta' MISURATA.** Non conserva `L`: **azzera tutta la rotazione rigida a ogni passo**, quindi cancella la **precessione fisica reale** (`L_z ~ -0.9`, verso coerente all'**84 %**). *«Conservare L != annullare la rotazione»*, e la fisica di base **conserva gia' `L` da sola** | **`:549-553`**, `:3611` | una rimozione della sola rotazione **spuria** del rilassamento che lasci intatta quella **fisica**: e' un problema aperto, non un flag da accendere |
| **`SYNC_SPINORE`** | **Allineamento IMPOSTO, non derivato** (§3, zero manopole): e' un Kuramoto sugli spinori, `omega_sync = forza * cross(nb, nb_media)`. **E `nb_media` e' una media di VICINATO**, quindi introduce un termine che *decide* l'ordine invece di farlo emergere | **`:2161-2163`** | una derivazione da un principio (non da analogia col Kuramoto) che produca la **stessa** forma |
| **`ANTIFASE_ADD`** · **`COPPIA_DENSITA`** | **Marcate dal codice stesso** *«LEGGE DI STABILITA' (esplorativa)»* e *«ESPLORATIVO»*. Sono **interventi sulla stabilita'**, non leggi derivate | `:554`, `:557` | una derivazione. Finche' il commento dice «esplorativa», l'autore stesso non le classifica come fisica |
| **`TEMPO_SEGNO`** | **NO-GO gia' registrato** (MOD 5.3a / 5.3c) | `:2829-2833` | il NO-GO, se cade con un riscontro committato |
| **`GAMMA_TURBO`** | **Non e' una legge: e' un AMPLIFICATORE diagnostico.** §10-C: si usa per **VEDERE**, mai per **CONCLUDERE** | `--gamma-turbo` | nulla: la sua categoria e' corretta e resta |

---

## ⚠ E.bis — **DUE VOCI DELLA TABELLA PROPOSTA NON REGGONO, e vanno corrette**

*(P1: la tabella era una prima passata di Claude web sui corpi del codice. Verificata dal disco,
due motivazioni sono sbagliate. Le correzioni **non** salvano i flag — li **riclassificano**.)*

### E.bis.1 — **`SYNC_UPDATE`: la motivazione e' FALSA. Non accende lo scuotimento.**

La tabella diceva: *«Cambia l'integratore **e accende lo scuotimento**: due variabili in un flag»*.
**Verificato dal codice: e' il contrario.**

```python
:1980   if SCUOTIMENTO and not SYNC_UPDATE:      # il rumore pre-passo e' DISATTIVATO da SYNC_UPDATE
:2279   if SYNC_UPDATE and SCUOTIMENTO:          # e RIAPPLICATO dopo la rotazione
:2302   if SYNC_UPDATE and SCUOTIMENTO:
```

**`SYNC_UPDATE` non accende niente: SPOSTA il punto di iniezione del rumore.** `SCUOTIMENTO` e' un
flag **indipendente**, e resta ON o OFF per conto suo.

**E non sono «due variabili in un flag»:** tutti i suoi effetti — `dph` dalla snapshot (`:1969`),
`nb_t` invece di `self._nb` (`:2031`), `omega_t` invece di `self.omega_s` (`:2142`), `psi_t`
(`:2861`), e la rilocazione del rumore — sono **UNA sola scelta coerente**: *ogni legge del passo
legge lo stato a `t-1`*. E' **Gauss-Seidel -> Jacobi**.

> **RICLASSIFICATA: `SYNC_UPDATE` NON e' una legge, e' uno SCHEMA DI INTEGRAZIONE** — stessa
> categoria di `VERLET`. Non appartiene a questa sezione: **non rompe una proprieta' fisica**, sceglie
> un ordine di aggiornamento. Resta **OFF in tutti i run del fork** (fatto gia' in §9, ed e' la
> ragione per cui sotto `--spinore-corretto` il rumore non tocca il Bloch direttamente).
> **Cosa servirebbe per deciderlo:** una misura della **deriva** fra i due schemi — che **non
> esiste**, esattamente come per `VERLET` (voce **B3**).

### E.bis.2 — **`LS_AZIM`: `z` NON e' un asse di laboratorio arbitrario. Ma la voce resta esclusa, per una ragione PIU' FORTE.**

La tabella chiedeva di accertarlo, e aveva ragione a dubitare. **Verificato:**

```python
:5666-5667   ang = 2*np.pi*k/nmasse ;  cx, cy = sep*np.cos(ang), sep*np.sin(ang)
:5668        net.nuova_massa(..., centro=(cx, cy, 0.0), ...)      # <- le masse stanno sul piano z = 0
```

**I centri delle masse giacciono su un cerchio nel piano `z = 0`**, quindi `z` e' la **normale
geometrica della configurazione iniziale**, non un asse arbitrario. **La motivazione originale era
imprecisa.**

**Ma l'esclusione regge, e per due ragioni piu' nette:**

1. **⚠ USA IL BARICENTRO GLOBALE.** `_cen = self.pos[:self.n].mean(0)` (**`:3773`**) e' una **media
   su TUTTO il sistema**, ed e' precisamente cio' che `CLAUDE.md` §4 vieta: *«LOCALE PURA — mai
   togliere la media globale: introduce NON-LOCALITA', una scorciatoia che il sistema relazionale
   non deve avere»*. **E l'ironia sta dieci righe sotto**, `:3783`:
   `# --- LOCALE PURA: rimossa la sottrazione di spinta.mean() ---`
   **E non e' un caso isolato: nello stesso metodo ci sono QUATTRO annotazioni identiche**
   (`:3721` `proj.mean()`, `:3747` `grav.mean()`, `:3783` `spinta.mean()`, `:3799` `flusso.mean()`).
   **Quattro medie globali sono state tolte da qui per questa ragione. `LS_AZIM` ne reintroduce una
   quinta, per una via diversa: non una sottrazione, ma un CENTRO.** *(Questa e' la ragione decisiva, e non dipende da come e' fatta la scena.)*
2. **L'asse e' CABLATO, non DERIVATO.** `np.cross(_rhat, _spin)[:, 2]` (**`:3777`**) prende l'indice
   **2** e basta. Anche dove `z` e' la normale giusta, **il codice non la CALCOLA: la assume.** I
   nodi sono seminati in **palle 3D isotrope** (`u = rng.normal(size=(n,3))`), il sistema evolve in
   3D e puo' inclinarsi; una scena disposta altrimenti renderebbe la legge semplicemente **falsa**.
   §3: *«nessun numero scelto»* vale anche per un **indice** scelto.

> **VERDETTO: esclusa** — non per «asse di laboratorio», ma per **media globale (§4)** piu' **asse
> cablato invece che derivato (§3)**.
> **COSA LA RIAPRIREBBE:** una versione che (a) usi un centro **locale** (baricentro del vicinato,
> non del sistema) e (b) **calcoli** la normale del piano dalla configurazione — p.es. dal momento
> angolare locale — invece di prendere `[:, 2]`. **Sarebbe un'altra legge, e andrebbe sigillata.**

---

## E.ter — Le voci §3 **CONFERMATE sane**, con la riga che le sostiene

| flag | perche' regge | riga |
|---|---|---|
| **`PAV_COM`** | sostituisce il **muro `0.05`** con `median(d0) - MAD(d0)`: **la legge al posto del numero**, e scala col sistema (§3) | `:621-623`, `:5165` |
| **`GUSCIO_MORBIDO`** | `D = c_locale * spaziatura` — **forma standard** di una diffusione, *«nessun coeff. nuovo»*, con **clamp causale CFL** `|delta d0| <= cs*dt_e` | **`:3211-3216`** |
| **`ZETA_VIR`** | `beta *= cos2`: dissipa il **radiale**, libera il **tangenziale**. E `cos2 + sin2 = 1` **esattamente** perche' `H = hypot(r_rad, t_tan)`: e' una **decomposizione ortogonale**, non una pesatura scelta | `:3765-3770` |
| **`CHI_BASC`** | soglia = **`PHI_CRIT`**, il quanto di olonomia **gia' nel sistema** — e **non** una mediana globale | **`:3045-3050`** |
| **`PLAST_DIN`** | plasticita' dallo **stress metrico** `\|d-d0\|/d0` per l'eccesso di torsione, **saturata** con `tanh` | **`:3423-3427`** |
| **`VIRIALE`** | `circ_nodo` costruito **ANTISIMMETRICAMENTE**: `np.add.at(circ_nodo, ii, twn_a)` e `np.add.at(circ_nodo, jj, -twn_a)` — l'opposto esatto del difetto di `POLO_MATURO` | **`:3755`** |
| **`OLON_PART`** | `hypot(\|circ_arc\|, \|twn_a\|)` = somma in quadratura di due contributi ortogonali, **la stessa regola usata due righe sotto** per `H = hypot(r_rad, t_tan)`: **derivata, non scelta** | **`:3761`** vs **`:3764`** |
| **`STEP2_OROLOGIO`** | **gia' promosso**, sezione **A1** | `:793` |

*(Sane **come costruzione**. Nessuna di esse ha un sigillo: restano spente, e la FASE A resta valida.)*

---

# D. CORREZIONI DI DIFETTO — **nessun flag, e non devono averne**

> **Un bug curato non ha un interruttore.** Sono qui **per memoria**, non come candidate.

| # | correzione | riscontro | sigillo |
|---|---|---|---|
| **D1** | **`_cs_nodo_prev` esteso alla mitosi** — il figlio eredita `cs` dal padre, come le altre sei cache | fallback **71.88 % → 0.00 %**; passi con cache inusabile **24/30 → 0/30** | **5/5 PASS**, con **P1b** (controllo positivo: «col flag ON DEVONO differire», `n` 1821 ≠ 1771) |
| **D2** | **`_psi_spin_prec` esteso alla mitosi** — settima voce della stessa convenzione | guardia 4π fallita nel **95.33 %** (143/150), condizione `len != n` in **143/143**; dopo: **0.00 %** | **6/6 PASS**, con **S1b** (controllo positivo, `n` 2392 ≠ 2200) |

**Perché non possono diventare flag:** un flag dichiara *«questa fisica è opzionale»*. Qui non c'è
fisica alternativa — c'è un array della lunghezza sbagliata. Un `--senza-fix-cache` significherebbe
*«esegui con il bug»*, che non è un braccio di un A/B: è un difetto con un nome gentile.

---

# REGOLE DI MANUTENZIONE

1. **Una componente entra in A solo con i TRE criteri documentati, ciascuno col suo riscontro
   committato**, e **col criterio di RETROCESSIONE scritto nello stesso momento**.
2. **Il ③ non si riempie per inerzia.** *«È sempre stato acceso»* non è *«senza è sbagliato»*.
3. **Promuovere = cambiare il DEFAULT.** Il ramo vecchio resta, marcato **diagnostico**: senza,
   si perde la capacità di misurare cosa fa quella legge.
4. **Le correzioni di difetto non entrano mai in B.**
5. **Un numero entra qui solo se è già nel repo** (stessa regola di `doc/RAMIFICAZIONI.md`).
6. **Lo strato dei 10 già-`True`** va riesaminato voce per voce: oggi è **fisica di default non
   certificata**, ed è la parte di questo registro con più lavoro davanti.
