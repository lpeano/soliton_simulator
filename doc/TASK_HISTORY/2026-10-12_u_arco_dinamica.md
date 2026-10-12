# `P4` — **LA `U` D'ARCO DINAMICA: la derivazione, e il suo TERMINE IN `E`**

> **Mandato di Luca, `P4`:** *«la derivazione, cioe' **la coppia coniugata sull'arco**, la
> parte `U(1)` e la parte `SU(2)`, **cio' che la muove**. E **SOPRATTUTTO IL SUO TERMINE
> IN `E`**: se `U` diventa dinamica, la sua energia entra nel bilancio, altrimenti `E`
> smette di conservarsi. ### **Le forme vanno a Luca; il codice dopo la sua risposta.»**

> ### ✅ **E I VINCOLI DI FORMA NON LI INVENTO: stanno GIA' in `[[U-ARCO-DINAMICA]]`** —
> hamiltoniana, locale, covariante di gauge, `C`, reversibile; ### ⛔ **e la scala
> dell'accoppiamento SOLO RELAZIONALE rispetto al vuoto locale, MAI un numero.**
> ### 📌 **Quel vincolo risolve in anticipo la tensione che stavo per sollevare**, e lo
> dico: un termine cinetico per `U` **vorrebbe** una costante d'accoppiamento, e `A1` la
> vieta. ### **Luca aveva gia' deciso DOVE prenderla.**

---

## 1. LA COPPIA CONIUGATA SULL'ARCO — *e il conto dei gradi di liberta' torna*

### ⭐ **`U(2) = U(1) x SU(2)` diviso `Z_2`**, quindi **quattro** generatori. ### Si scrive
`U_k = exp(i theta_k) . V_k`, con `V_k` in `SU(2)`.

| | la coordinata | il momento coniugato | quante |
|---|---|---|---|
| **parte `U(1)`** | `theta_k` *(una fase per arco)* | **`p_k`** *(reale)* | `1 + 1` |
| **parte `SU(2)`** | `V_k` *(in `SU(2)`)* | **`L_k^a`**, `a = 1,2,3` *(i momenti invarianti a sinistra)* | `3 + 3` |

### ✅ **TOTALE: `4` coordinate e `4` momenti per arco**, e coincide coi **quattro
generatori** di `U(2)`. ### ⚠ **Il conto torna, e questo e' il primo controllo:** se non
tornasse, la parametrizzazione **starebbe perdendo o inventando gradi di liberta'.**

### ⛔ **E I MOMENTI VIVONO SULL'ARCO, non sull'estremita'.** E' una differenza che conta:
lo spinore vive **sulle estremita'** *(e' `2m`)*, `U` e i suoi momenti vivono
**sull'arco** *(e' `m`)*. ### **Confonderli raddoppierebbe lo stato di `U`.**

---

## 2. IL SUO TERMINE IN `E` — *e la scala viene dal VUOTO, non da una costante*

### ⭐ **La parte dai MOMENTI** *(il pezzo <<elettrico>>)*:

> **`E_mom = somma_k [ p_k^2 + |L_k|^2 ] / (2 sigma_k)`**

| | |
|---|---|
| ### ⛔ **e `sigma_k` NON e' una costante: e' il VUOTO SULL'ARCO** | `sigma_k = |phi_{2k}|^2 + |phi_{2k+1}|^2`, cioe' **il vuoto delle due estremita' dell'arco** |
| ### ✅ **perche' questo rispetta `A1`** | la scala e' **presa dal sistema**, come `Lambda_k` per la saturazione: ### **non c'e' nessun numero da tarare** |
| ### ⭐ **e perche' e' il VUOTO e non altro** | sull'arco **non c'e' nient'altro di relazionale**: lo spinore vive sulle estremita' ed e' **materia** *(e usarlo renderebbe l'energia di `U` dipendente dalla materia che la sorgente)*; il grado e' **del nodo**, non dell'arco |
| ### ⚠ **E IL CASO `sigma_k = 0` VA DICHIARATO** | dove il vuoto e' **assente**, `E_mom` **diverge**. ### ⛔ **E NON si mette un pavimento** *(`A11`)*: la lettura giusta e' che **senza vuoto l'arco non puo' avere momento** — cioe' `p_k = L_k = 0` **e' l'unico stato ammesso la'**, e il limite e' `0/0 -> 0`. ### **Ma e' una FORMA, e va a Luca** |

### ⛔ **La parte dalle OLONOMIE** *(il pezzo <<magnetico>>)* — **E QUI C'E' UN PROBLEMA
STRUTTURALE, lo stesso di `P3`:**

> **`E_hol = somma_{cicli} sigma_ciclo . (1 - Re tr Hol / 2)`**

### ⚠ **PERCHE' SUI CICLI E NON SUGLI ARCHI:** l'olonomia di **un arco solo** non e'
invariante di gauge *(una trasformazione sui nodi la cambia)*; ### **l'olonomia su un
CICLO CHIUSO lo e'.** ### **E' la stessa ragione per cui il criterio della mitosi e' su un
ciclo** *(`P5(a)`)*.

### ⛔ **MA <<QUALI CICLI>> E' UNA SCELTA, e una base di cicli NON E' UNICA.** ### **E' lo
stesso difetto strutturale che `P3` ha trovato per la corrente:** una somma su una base non
unica **non e' un osservabile.** ### 📌 **E il banco ha un candidato gia' scritto:**
`geometria.cicli_corti` — **i cicli piu' corti**, che su un grafo sono **determinati**
*(a meno di pareggi)*. ### ⚠ **Ma e' una FORMA, e la decide Luca.**

---

## 3. CHE COSA LA MUOVE — *la corrente della camminata, e viene da una variazione*

Il termine di materia che contiene `U` e' quello dello **spostamento con trasporto**:

> **`T = Re somma_k conj(psi_{2k+1}) . U_k . psi_{2k}`**

### ⭐ **E LA SORGENTE E' LA SUA VARIAZIONE:**

| | la derivata | che cosa muove |
|---|---|---|
| `dT / d theta_k` | **`-Im[ conj(psi_{2k+1}) . U_k . psi_{2k} ]`** | ### la **corrente di carica** sull'arco: muove `p_k` |
| `dT / dV_k` *(nelle tre direzioni `su(2)`)* | **`Re[ conj(psi_{2k+1}) . (i sigma^a U_k) . psi_{2k} ]`** | ### la **corrente di SPIN** sull'arco: muove `L_k^a` |

### ✅ **E QUESTO E' <<una connessione mossa dalla sua sorgente>>**, che e' esattamente la
frase della voce. ### ⛔ **E non e' un innesto: la sorgente E' la derivata del termine che
`U` ha gia'** — non si aggiunge niente.

---

## 4. LA `C`, E CHE COSA IMPONE A `U`

La `C` decisa e' `psi -> i sigma_y psi*`, `phi -> phi*`. ### **Perche' `T` sia invariante**,
`U` deve trasformarsi come **`U -> sigma_y U* sigma_y`**.

| | che cosa vuol dire | e la conseguenza sull'energia |
|---|---|---|
| parte **`U(1)`** | ### **`theta -> -theta`**: ### **la fase e' DISPARI sotto `C`** | allora `p -> -p`, e **`p^2` e' PARI**: ### ✅ **l'energia e' invariante** |
| parte **`SU(2)`** | **`V -> sigma_y V* sigma_y`** | i momenti vanno in se' col segno che segue, e **`|L|^2` e' PARI**: ### ✅ **invariante** |

### ⭐ **E QUESTO NON E' UN CONTROLLO A POSTERIORI: e' un VINCOLO che sceglie la forma.**
Un termine lineare nei momenti **sarebbe dispari** e ### **romperebbe `C`** — quindi
**l'energia dev'essere quadratica**, e **non e' una scelta mia.**

---

## 5. IL RUOLO DEL VUOTO — *la cosa che la voce chiede di DICHIARARE*

> ### 📌 **La voce dice:** *«una cosa da dichiarare: il ruolo del vuoto `phi`, che oggi e'
> NEUTRO -- se e come entra nella dinamica di `U`.»*

### ✅ **LA RISPOSTA, e ha due meta' distinte:**

| | |
|---|---|
| ### ⛔ **`phi` NON e' una sorgente di `U`** | perche' e' **neutro**, cioe' **non e' trasportato da `U`** — quindi **non compare nel termine `T`**, quindi **la sua variazione rispetto a `U` e' ZERO** |
| ### ⭐ **ma `phi` E' LA SCALA di `U`** | `sigma_k` **e' il vuoto dell'arco**: il vuoto **non spinge** `U`, ### **ne decide l'INERZIA** |

### ⭐ **E questa divisione e' pulita e verificabile:** *<<neutro>>* vuol dire **senza
`U`**, e qui vuol dire **esattamente** *«non sorgente»*. ### **Ma puo' comunque essere
scala, perche' una scala non e' un accoppiamento al campo: e' un fattore davanti
all'energia.**

---

## 6. IL BRACCIO DI REGRESSIONE — **obbligatorio, e esatto PER COSTRUZIONE**

> La voce lo pretende: *«spenta (momenti nulli e `U` fisse) deve dare il `v3` AL BIT.»*

### ✅ **E con questa forma e' esatto per costruzione:** l'evoluzione di `U` e' mossa
**solo dai momenti**; con `p = 0` e `L = 0` ### **`U` non si muove**, e il passo si riduce
**esattamente** a quello di oggi. ### ⚠ **E va comunque MISURATO**, perche' *«esatto per
costruzione»* e' un'affermazione sul codice **che non ho ancora scritto.**

---

## 7. CHE COSA VA A LUCA — *le forme, separate dalla raccomandazione*

| | la forma | la mia raccomandazione |
|---|---|---|
| `1` | **la scala `sigma_k`** | ### **il vuoto delle due estremita' dell'arco**: e' **l'unica grandezza relazionale che vive sull'arco** senza essere materia |
| `2` | **il caso `sigma_k = 0`** | ### **nessun pavimento**: `p = L = 0` e' **l'unico stato ammesso** dove il vuoto e' assente, e il limite e' `0`. ### **Ma e' una forma** |
| `3` | **il termine delle OLONOMIE** | ### ⛔ **NON raccomando una base di cicli arbitraria.** Candidato: **i cicli piu' corti** *(`geometria.cicli_corti`)*, che sono **determinati**. ### ⚠ **E se nemmeno quelli bastano, il termine magnetico NON e' un osservabile** — ed e' lo **stesso difetto strutturale di `P3`** |
| `4` | **l'esponente dell'energia** | ### ✅ **quadratica, e NON e' una scelta mia: la `C` la impone** |

---

## 8. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **localmente**? | ### ⚠ **NON LO SO ANCORA, e dopo `P3` e' una domanda aperta per `E` stessa.** La parte dai momenti e' **una somma per arco** *(locale per costruzione)*; ### ⛔ **il termine delle olonomie e' una somma SUI CICLI, e un ciclo non e' locale** — e' il **suo** problema, oltre a quello di `P3` |
| **2** | **quale gradino**? | ### **NESSUNO: questa e' una DERIVAZIONE, non un risultato.** Non ho misurato niente, e **non lo dichiaro come se l'avessi fatto** |
| **3** | **aggiunge un numero o una legge**? | ### ✅ **NESSUN NUMERO**, ed e' il vincolo di Luca: la scala e' **relazionale**. ### ⚠ **Aggiunge LEGGI: due** *(l'energia di `U`, e la sua evoluzione)* — e `9-ter` chiede di dirlo: ### **non si poteva togliere niente in cambio** |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### ⚠ **IL SEGNO SI':** il segno della sorgente decide **se il campo attrae o respinge**, ed e' ### **`[[DOMANDA-QUALE-SEGNO]]`, che resta APERTA** |
| **5** | **emergente o imposto**? | ### ⭐ **La SORGENTE e' emergente** *(e' la derivata del termine che `U` ha gia')*; ### ⛔ **la FORMA DELL'ENERGIA e' imposta** — la scelgo fra quelle che `C` e `A1` ammettono, e **le ammesse sono poche, ma piu' di una.** |

---

## 9. TODO DEL NEXT STEP

1. le **quattro forme** del paragrafo `7` in `DA_DECIDERE_LUCA.md`, **una voce**, con la
   raccomandazione **separata**.
2. ### ⛔ **NESSUN CODICE finche' Luca non risponde**, e il mandato lo dice.
3. e il **braccio di regressione** si scrive **insieme** al codice, non dopo.
