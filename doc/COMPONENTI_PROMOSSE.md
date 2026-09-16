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
