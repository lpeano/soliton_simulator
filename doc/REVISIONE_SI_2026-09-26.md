# 🔬 **LA REVISIONE STORICA DEGLI OTTO `SI`** — *guardiano, 2026-09-26*

> **A CHI SERVE:** a chi prende in mano uno degli otto `SI` della lista chiusa **senza avere la
> conversazione in cui sono stati decisi**. Ogni voce dell'indice che compare qui porta l'**ancora**
> della sua sezione nella colonna `revisione` di `doc/INDICE_ID.tsv`.

## ⚠ **DUE LIVELLI DI EVIDENZA, e non si mescolano**

| marchio | che cosa significa |
|---|---|
| ✅ **VERIFICATO** | **l'ho aperto io e la riga dice quello**: file, riga, e la frase che la riga contiene. Si ricontrolla in dieci secondi. |
| 🟨 **DI LUCA, non verificato da me** | una **misura o un numero** che viene dalla revisione di Luca. **Non l'ho rifatto.** Sta qui perché è il motivo della decisione, non perché lo confermo. |
| 🧠 **INFERENZA** | un **ragionamento**: una derivazione, un principio, una conseguenza. **Non è una misura**, e si giudica dalla sua forma, non da un numero. |

**Perché la distinzione è la prima cosa del documento:** nel corso di questa stessa giornata ho
**chiuso una voce su un numero che non esisteva nei file** *(`D09`, e la smentita era in un
messaggio di commit)* e ho **creduto buono un campo vuoto** *(`avanzamento` su 740 voci su 740)*.
**Un documento che non dice quale riga ha aperto chi lo ha scritto è una voce di corridoio.**

---

## DRIVER-SCENA-II — *il primo da fare* {#driver-scena-ii}

**Senza un driver che faccia la scena `(ii)`(a) non esiste il RUN BASE, e senza run base non
esistono le tre prove.** Sono **quattro cose insieme**, non una.

✅ **VERIFICATO — le quattro righe dicono quello:**

| dove | che cosa c'è |
|---|---|
| `csv/_test_fork/_scena_video.py:223` | `sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", NMASSE, "--sep", SEP, …]` — **il driver FISSA `N-MASSE`** |
| `csv/_test_fork/_scena_video.py:328` | `S.avvia_test("N-MASSE")()` — *«il costruttore UFFICIALE della scena»*, e anche qui è `N-MASSE` |
| `soliton_simulator.py:7187` | `raise SystemExit(` dentro `_massa` *(la funzione comincia a `:7169`)* |
| `soliton_simulator.py:8681` | `net.semina(-1 if SEMINA_LAM else a.nodi)` — **`_applica_flag` semina il vuoto**, e con `SEMINA_LAM` chiede la **saturazione** |
| `soliton_simulator.py:7290`-`7295` | il commento della scena `(ii)`: *«UN SOLO VUOTO, e lo si VERIFICA invece di sperarlo. Se la rete ha già dei nodi, il vuoto dell'`import`/di `--nodi` si SOMMEREBBE a questo: due vuoti, non uno… NON lo aggiusto in silenzio (`A9`): lo DICO»* |

🟨 **DI LUCA, non verificato da me:** che `N-MASSE` **con `SEMINA_LAM`** finisca *proprio* in quel
`SystemExit` *(ho verificato che il `raise` esiste a `:7187` dentro `_massa`, **non** che sia quel
ramo a scattare con quella combinazione di flag)*; e che **manchi un `--seme` reale** *(nel driver la
parola `seme` compare 5 volte: non ho stabilito che nessuna di esse sia un seme vero)*.

🧠 **INFERENZA:** le quattro cose **si compongono in un vicolo cieco** — il driver fissa `N-MASSE`,
`N-MASSE` con `SEMINA_LAM` si ferma, e senza `SEMINA_LAM` il vuoto nasce comunque da `_applica_flag`
mentre la scena `(ii)` **rifiuta una rete non vuota**. **Non l'ho eseguito**: è il ragionamento sulle
quattro righe, e la prova sarà il driver che gira.

**CRITERIO DI CHIUSURA:** un comando solo che produce la scena `(ii)`(a) in configurazione del
driver, con un seme dichiarato, **e un collaudo nei due versi**.

---

## OSSERVABILE-P1 {#osservabile-p1}

**La `PROVA 1` chiede *«due masse si avvicinano?»*, e la distanza del sistema è lungo il GRAFO
pesato con `d`** — non su `pos` *(`A13`: la distanza sta sugli archi)*.

🟨 **DI LUCA:** l'osservabile **esiste solo in tre script di analisi**, e **nessuno è ufficiale**
*(non l'ho contato io)*.

🧠 **INFERENZA:** finché la grandezza della prova non ha **un nome e un collaudo**, la `PROVA 1` non
ha un numero — e un numero prodotto da uno script di analisi *ad hoc* non è confrontabile fra run.

**CRITERIO DI CHIUSURA:** un osservabile inventariato che, dati due insiemi di nodi, dia la distanza
**sul grafo pesato con `d`**, col collaudo su **due masse a distanza nota**.

---

## D02 — *il disegno entra nella gravità* {#d02}

✅ **VERIFICATO:** `pozzo_grafo` comincia a `soliton_simulator.py:6525`, e a **`:6541`** contiene
`v = self.pos[jj] - self.pos[ii]`. **La lunghezza `L` viene da `pos`, cioè dal DISEGNO.**

🟨 **DI LUCA:** il risultato **entra nella spinta `S09`** *(`d0 += spinta*median(d0)`)*, e `L/d`
arriva a **×8 fra le masse** *(`Z103`)*. **Non ho rifatto la misura.**

🧠 **INFERENZA / CURA DERIVATA:** se la distanza del sistema è `d` *(`A13`)*, la lunghezza nel pozzo
**deve essere `self.d`**, non `pos`. La cura è **`L = self.d`**, con **flag, sigillo e A/B** — e va
fatta **prima delle misure**, perché misurare con il disegno dentro la gravità significa misurare un
sistema che si sa difettoso *(`P2`)*.

---

## D31 — *il freno, e la forma da scegliere* {#d31}

✅ **VERIFICATO:** `_smorza` è a `soliton_simulator.py:4186`, il docstring dice *«smorzando solo la
DISCESA»*, e il corpo è `eff = np.where(scende, dx * fatt, dx)`: **il freno è a SENSO UNICO**, e
`scende = dx < 0.0`. ✅ **`Z91` è curato e `SCALA_MIN_PASSO` è acceso** *(sta in `CURE VERIFICATE`)*.

🧠 **INFERENZA, e decide il confronto fra le due forme:**
**`tanh` conserva la MEDIA di `u = d − LAM`; l'esponenziale conserva la MEDIANA.**
**La distanza fra le masse è una SOMMA lungo un cammino, quindi segue la MEDIA** → **`tanh` è
favorito per PRINCIPIO**, non per il numero.

❌ **UN CONTO SBAGLIATO, ritirato qui:** `exp(8.97e4)` su `4239163` **non ha senso** —
**l'esponente è PER ARCO** *(ordine `~0.3` a 120 passi)*, non la somma su tutte le scritture.
**Sommare gli esponenti di archi diversi tratta un prodotto di fattori indipendenti come un unico
fattore.**

⚠ **E UN PRECEDENTE DI METODO, che pesa più del conto:** la rimisura del **25** *(`454418` campioni
sopra `0.5`)* **soddisfaceva il criterio di riapertura**, e fu comunque dichiarata *«regge»* — **in
configurazione sbagliata**. 🟨 *(numeri di Luca.)*

🧠 **E UNA COSA DA GUARDARE, non un verdetto:** **le due forme simmetriche congelano gli archi a
`LAM` esatto** *(`u → 0` ⇒ nessun movimento in nessuno dei due versi)*. **Non è un difetto
dimostrato: è una conseguenza della forma, e va guardata sui dati.**

**LA MISURA, come l'ha fissata Luca:** `|dx|/d` **per sito e per verso**; `sum_t x²` **per arco**,
per **classe** *(masse / vuoto / fascia del muro)*; la **quota a `d = LAM`**.
**CRITERIO:** `tanh` se `exp(sum x²/2) − 1` **<** l'errore fra semi della distanza fra masse **e** la
quota `> 0.5` è nulla; **altrimenti decide Luca.**

---

## U1 — *`massa_critica_collasso` dentro le leggi* {#u1}

✅ **VERIFICATO:** `massa_critica_collasso` è definita a `:580` *(forma adattiva
`N_c = C·λ⁻³·(1+s)^θ`)*; `lambda_nodi` *(`:2954`-`:2961`)* ritorna **`np.full(self.n, LAM)`** in più
rami, cioè **una costante uniforme**; e a **`:5212`** la **repulsione di coerenza** dentro `step`
calcola `riempimento = n_vic_coer / max(Ncrit_ad, 1e-9)` e `u = riempimento * coerenza`, con
**`massa_critica_collasso()` come fallback** di `massa_critica_adattiva`.

> ### 🧠 **La conseguenza è il motivo del `SI`:** quella repulsione **agisce sulle regioni coerenti**,
> ### e le regioni coerenti **sono le masse**. Una soglia sbagliata non fa rumore di fondo: **agisce
> ### dove si misura la `PROVA 1`.**

🟨 **DI LUCA:** delle **21** occorrenze attive nel driver **ne mordono due** *(`lambda_nodi` e la
repulsione)*; `lambda_nodi` vale **`0.7615·LAM`** *(non ho verificato il valore, solo che è
uniforme — e `0.7615 = tanh(1)`, che vale la pena guardare)*; la capacità **`621`** *(nel file il
numero compare una volta sola)*.

**LA MISURA:** `u` **mediana** e **`p99`**, e `riempimento × coerenza`. **CRITERIO:** se
**`p99 < 0.05` non blocca**; altrimenti **A/B `REPULS_LEGGE`** sulla distanza fra le masse.
**CURA DERIVATA EVENTUALE:** una **capacità di saturazione `RSA`** al posto di `621`.

---

## CLI-1 — *la cura 5 dal CLI* {#cli-1}

🟨 **DI LUCA:** la cura **funziona nel driver** *(nati `218`/`216`)*; il **sigillo** però gira in
**configurazione DI MODULO**. **Non l'ho rifatto.**

🧠 **INFERENZA:** un sigillo in configurazione di modulo **certifica un percorso che nessun run
usa** — è la stessa classe del *default ribaltato* del par.9: il braccio di controllo diventa un
duplicato del braccio di prova.

**COME SI RIFÀ:** `argv_del_driver()` **+** `senza(argv, "--mitosi-2lam")`.
**CRITERI:** `0` archi sotto `2·LAM` nella mitosi a **ON**; **negati > 0 e nati > 0** *(senza questo
un ON che non fa niente passerebbe)*; braccio **OFF con archi corti**; `0 DominioViolato`.

---

## SCALE-TW — *e `3π` non è un quanto* {#scale-tw}

🧠 **INFERENZA, ed è la parte che cambia la lettura:**
**`3π` NON è un quanto: è il MASSIMO DELL'INGRESSO ISTANTANEO** — `2π` di fase **più** `π` di
torsione dipolare. **Per questo solo la CODA della distribuzione lo raggiunge**, e una soglia posta
sul massimo dell'ingresso non è una soglia fisica.

❌ **«`4π` sulle facce» NON REGGE:** per un **triangolo** l'angolo solido è **< `2π`**, quindi la fase
di Berry è **< `π`**. **La premessa geometrica cade**, e con essa la lettura che ne discendeva.

🧠 **L'UNICA LEGGE DERIVABILE, dichiarata come proposta:** l'**olonomia di Berry per FACCIA**,
seguita nel tempo; gli **eventi** sono gli **attraversamenti di `−1`**; il **tasso** è
`|dΩ/dτ| / 4π` — e **darebbe anche il tasso della creazione di faccia**, che è una seconda cosa che
oggi non si sa misurare.

**PRIMA LA MISURA `M1`: quanta mitosi e DOVE** *(masse / varco / vuoto)*, scena `(ii)`(a),
configurazione del driver, **300 passi**.
> **E il criterio di rilevanza è già scritto:** **se nel VARCO la mitosi è trascurabile, `3π` non
> tocca la `PROVA 1`** — e la voce scende di priorità senza bisogno di deciderla.

---

## D03 — *la memoria del moto* {#d03}

🟨 **DI LUCA:** prende le **direzioni da `pos`**, normalizza su **`I_med` GLOBALE**, ed è **satura
sul 78-89 % degli archi** *(`Z112`)*. **Non ho rifatto la misura.**

🧠 **INFERENZA:** scrive `d0` **con un meccanismo estraneo alla gravità** — e `d0` è la scala su cui
la gravità agisce. Due violazioni dichiarate: `A1` *(direzioni dal disegno)* e `A2` *(statistica
globale in una legge locale)*.

**DUE STRADE, e DECIDE LUCA:** **spegnerla nel run base dichiarandolo**, oppure **completare
`MEM_ARCO`**.

---

# ⬇ **LE VOCI CHE NON BLOCCANO, col motivo** {#non-bloccano}

| voce | perché non blocca | evidenza |
|---|---|---|
| **RAMPA-2** | è il **transitorio di UN SOLO passo** *(al passo 0 tutti leggono `cs = CS_M`)*. **Si cura comunque** | 🧠 e la cura proposta — valutare **`_cs_nodo` sullo stato iniziale** — è **legittima**: 🧠 **nessuna circolarità con `eta = inf`**, perché `eta` entra nella rampa e non in `cs` |
| **D09** e **Z73** | **smentiti**: `chi_basc` **non** blocca la mitosi | ✅ il messaggio di **`48a3555`** *(**2026-09-20**)*: *«da 2672 a 7323 nodi, 4651 nati in 1560 passi»*. **La misura di partenza era su 60 passi e un seme: CORTA, non sbagliata** |
| **D11** | curato | ✅ `01eda44` è la cura di `Z87` *(il mondo si costruisce dopo i flag)*; 🟨 `0` archi sotto `LAM` in scena `(ii)` coi flag del driver |
| **D14** | la **scala globale è uguale ovunque**: non introduce una differenza fra nodi | 🟨 di Luca |
| **D15** | la **premessa è superata da `CHI_COOP`** | 🟨 di Luca |

---

# ⚠ **COSA QUESTA REVISIONE *NON* È**

- **non è una misura**: le uniche cose che ho **aperto e letto** sono le righe marcate ✅. Tutti i
  **numeri** — `L/d` ×8, `454418`, `78-89 %`, `218/216`, `0.7615`, `621`, le 21 occorrenze — sono
  **di Luca**, e li ho lasciati **marcati come tali** invece di assorbirli nel testo;
- **non decide niente**: `D31`, `SCALE-TW` e `D03` restano **decisioni di Luca**, e le misure che le
  precedono sono elencate con i loro criteri;
- **non sostituisce i registri**: ogni voce vive nell'indice, e questa è **la sua storia**, non il
  suo stato. Lo stato sta in `doc/INDICE_ID.tsv`, e l'ordine di lavoro in
  `doc/SMISTAMENTO_run_base.md`.
