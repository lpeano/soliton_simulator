# `CURA 4` — L'ACCENSIONE DEL CAMPO *(decisione di Luca, 2026-09-25)*

> **Committato PRIMA del lavoro** *(par.5-septies: l'ordine deve essere verificabile da git, non
> asserito da me)*. **Il giro di 120 passi resta sospeso; la torsione NON si scrive.**

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### LE PREMESSE, che sono già misurate e non da rifare

- `ramp = min(1, eta/TAU_A)` in `_pesi`, ed **entra come `ramp[i]*ramp[j]`**: il peso d'arco va
  come **`ramp²`**. Al passo `120`, `5.76e-04` del valore maturo.
- **Tutti** i nodi nascono con `eta = 0`: `semina` *(`:2645`)*, `mitosi` *(`:5831`)*, Schwinger
  *(`:5987`)*. **La distinzione «nodo dato» / «nodo creato» NON ESISTE nel codice**: è il pezzo
  nuovo che questa cura deve introdurre.
- `_tempo_luce_nodo` è **già cablato**, è **per nodo** *(shape misurata `= n`)*, e vale
  **`p50 = 0.8978`**, cioè **`89.8` passi** con `p05 86.6` / `p95 92.2`.
- `TAU_A = 50` viene dal regime `deterministico` e **fu scelto per la vita media della memoria
  spinoriale**, non per la rampa.

### COSA MI ASPETTO

1. **Il flag spento sarà byte-identico** senza sorprese: la cura tocca `eta` alla nascita e il
   denominatore della rampa, e **entrambi sono dentro un `if`**.
2. **Al passo `1` il contrasto massa/vuoto salirà**, perché oggi è misurato a `ramp = 0.0002` e
   il campo è costruito da `ramp²`. **Non so di quanto**, e non lo indovino.
3. **`Λ = mean(I)` salirà di ordini di grandezza**: oggi vale `7.2e-15`, e `ramp² = 4e-08`.
   **Se `Λ` non salisse, la cura non sta agendo** — è il controllo positivo naturale.

### ⚠ COSA **NON** SO

- **Se il sistema resti stabile con il campo acceso dal passo zero.** Oggi il campo cresce
  lentamente e il sistema si assesta *con* lui. Accenderlo tutto insieme **è un cambio di
  condizione iniziale grosso**, e `G_PH = 3e-3` è dichiarato *«vicino al limite di divergenza»*.
  **Se diverge, è un RISULTATO**, non un fallimento della cura.
- **Se `|dx|/d` cresca abbastanza da far mordere la saturazione di `tanh`.** È ciò che la
  rimisura deve dire, e **non ho un'aspettativa quantitativa**: so solo che `0.0531` era misurato
  a campo spento.
- **Quale sia il valore giusto di `eta` per un nodo «maturo».** Basta `ramp = 1`, cioè
  `eta >= tempo`; ma **con quale tempo**, se la rampa dei nati in dinamica usa
  `_tempo_luce_nodo` e quella iniziale non esiste più? *(Sotto, nella progettazione.)*

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

### LA DISTINZIONE «SEMINA INIZIALE» / «IN VOLO», dichiarata

**Non esiste una proprietà del nodo che lo dica**, quindi va introdotta. **La scelta che faccio, e
la dichiaro come scelta:**

> **`semina(..., maturi=None)`**: un parametro **esplicito del chiamante**, non un'euristica sul
> tempo o sul numero di passi.
> **`maturi=None` significa «decidi dal flag»**, e la regola è: **matura se la rete è VUOTA**
> *(`self.n == 0` prima della semina)*, cioè **se questa semina È l'universo**.
> **Ogni altra semina è «in volo»**, GUI compresa.

**PERCHÉ COSÌ e non con un contatore di passi:** un criterio temporale *(«prima del passo 1»)*
sarebbe **una soglia nuova**, e `A11`/par.3 la vietano. **`n == 0` non è una soglia: è un fatto
topologico** — prima non c'era niente.
**⚠ E IL LIMITE, che va detto:** la scena `(ii)` semina **una sola volta** su rete vuota, quindi
`n == 0` la copre; ma una scena che seminasse **due masse in due chiamate** avrebbe la **seconda**
trattata come «in volo». **Per questo il parametro esplicito esiste**: chi vuole due semine
iniziali passa `maturi=True` e **lo dichiara nel codice della scena**.

### IL TEMPO DELLA RAMPA PER I NATI IN DINAMICA

`ramp = min(1, eta / tempo_rampa)` con **`tempo_rampa = _tempo_luce_nodo(i, j)`** per nodo,
**non `TAU_A`**.
**`TAU_A` resta SOLO a `:3334`** *(la vita media della memoria spinoriale)*. **`:3316` segue la
rampa** — il suo commento dice *«la STESSA riga di `_pesi()`»*, quindi deve restare la stessa.

**⚠ UN PROBLEMA CHE DEVO RISOLVERE E CHE IL MANDATO NON NOMINA:** `_tempo_luce_nodo` **cambia a
ogni passo** *(dipende da `d` e `cs`)*. Se il denominatore della rampa cambia, **`ramp` non è
monotona**: un nodo può «tornare immaturo» se i suoi archi si allungano.
**LA SCELTA, e la dichiaro:** si confronta `eta` col tempo-luce **corrente**, senza memorizzarlo.
`ramp` **può** scendere, e **va bene**: è una legge locale che segue lo stato locale, come
`_ttw = 2π/|Δω|`. **L'alternativa** *(congelare il tempo-luce alla nascita)* **richiederebbe un
array di stato nuovo per nodo**, con la sua estensione alla mitosi e allo snapshot — cioè
**esattamente la famiglia di difetti `_cs_nodo_prev` / `_psi_spin_prec`**. **Non lo faccio.**

### I CRITERI, fissati QUI e prima di vedere i numeri

| | criterio | cosa decide |
|---|---|---|
| **`A1`** | **flag SPENTO = byte-identico**: firma dei byte su tutti i campi, **un processo per braccio** | par.2.1 · `STANDARD 1` · `STANDARD 2`. **Se fallisce, STOP** |
| **`A2`** | **al passo `1`, `ramp == 1` su TUTTI i nodi della semina iniziale** | è la cura stessa. **Esatto, non approssimato** |
| **`A3`** | **un nodo nato da MITOSI parte da `ramp = 0` e arriva a `1` nel suo tempo-luce** | è la seconda metà: la rampa **resta** per i nati in dinamica |
| **`A4`** | **contrasto massa/vuoto e `Λ` al passo `1`**, confrontati con `P2 = 27` e `P3 = 5` | il mandato lo chiede. **`Λ` deve salire di ordini**: se non sale, la cura non agisce |
| **`A5`** | **CONTROLLO POSITIVO**: ON e OFF **DEVONO differire** al passo `1` | par.10.2: un sigillo che verifica solo la byte-identità a OFF **passerebbe su codice morto** |
| **`A6`** | **caso che DEVE fallire** *(`P1-sexies`)*: con il flag ON e `maturi=False` forzato, `A2` **deve dare FAIL** | se passa, `A2` non sta guardando la maturità |
| **`A7`** | **`TAU_A` non è più letto da `_pesi`**: verifica dall'**AST**, non da un `grep` | la separazione dei due ruoli è **il punto** della cura |

**COSA MI FAREBBE FERMARE:** `A1` che fallisce *(il flag non è inerte)*; una divergenza numerica
con il flag ON *(che è un **risultato**, da committare e fermarsi)*; `A4` con `Λ` che **non** sale
*(la cura non agisce e la diagnosi è sbagliata)*.

### E DOPO: LA RIMISURA DI `|dx|/d`

**Solo dopo che `A1`-`A7` passano**, e **con il flag ON**: si rigira la misura di `V8`/`V9` a campo
maturo. **Il criterio è già scritto in `V8`:** la saturazione di `tanh` conta a `x` di ordine `1`;
oggi il massimo è `0.0531`. **Se a campo maturo resta sotto `0.5`, la forma `1+tanh` regge; se lo
supera, la decisione va riaperta.**

---

## ③ TODO DEL NEXT STEP

1. **[fatto in questo commit]** la dichiarazione di **`2a`**: i cicli di
   `circolazione_topologica` sono **fondamentali di un albero**, **tappati a `256`**, e
   l'olonomia `> 4π` **non dice nulla sulla curvatura locale**.
2. il flag `SEMINA_MATURA` *(nome provvisorio)*, **OFF di default**, e la distinzione
   `maturi` in `semina`.
3. il sigillo `A1`-`A7`, **un processo per braccio**.
4. la rimisura di `|dx|/d` a campo maturo.
5. **poi** la corsa diagnostica `2b` sui **triangoli**, e la valutazione di `2c`.
