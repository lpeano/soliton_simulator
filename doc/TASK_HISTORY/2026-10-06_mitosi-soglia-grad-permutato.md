# `MITOSI-SOGLIA-GRAD` — **i morsi RIMESCOLATI**: il `0.3` porta per DOVE, o solo per QUANTO?

*(Mandato di Luca del 2026-10-06, **dopo** il referto di `MITOSI-SOGLIA-GRAD` (`d97317a`) e
il suo aggiornamento col predittore causale. Il simulatore **NON si tocca**: si misura con
una patch, **sola lettura** sulla fisica.)*

> ### ⛔ **DOPO IL REFERTO, FERMO E SI ASPETTA LUCA:** che fare del `0.3` — *tenerlo*,
> *derivarlo su* `|r_i·phivel_i − r_j·phivel_j|`, o *ripensare la soglia* `3π` — ### **è una
> decisione sua.**

## 1. RAGIONAMENTO PRELIMINARE

### LA DOMANDA, e nasce da un risultato già misurato

Il referto `d97317a` ha mostrato che il `0.3` è **PORTANTE**: senza di lui, **`2` divisioni
in entrambe le leggi del tempo** *(`Ap0 = 2`, `Bp0 = 2`, contro `1219` e `18`)*.
### **Resta da capire PERCHÉ porta**, e ci sono **due** spiegazioni che danno lo stesso
conteggio:

| | la spiegazione | che cosa implicherebbe |
|---|---|---|
| **(1)** | la modulazione **abbassa la soglia DOVE il gradiente di `r` è grande** | ### **il gradiente porta FISICA**, e il `0.3` è un'ampiezza da derivare |
| **(2)** | la modulazione **la ABBASSA, e basta** — in qualunque punto | ### **è una soglia ridotta a mano MASCHERATA**, e il `3π` è il numero vero da discutere |

### ✔ **E IL BRACCIO `Bperm` SEPARA LE DUE, perché distrugge il LEGAME lasciando la
### DISTRIBUZIONE**

A ogni passo si calcola `bite = 0.3 * tanh(grad_modula)` **come oggi**, poi lo si
### **PERMUTA a caso fra gli archi**, e si usa `soglia = soglia0 * (1 - bite_permutato)`.

* ### **la distribuzione delle soglie per passo resta IDENTICA** *(è la stessa array
  riordinata: il multiinsieme è conservato **per costruzione**)*;
* ### **il legame arco–gradiente è DISTRUTTO.**

### ➜ **Quindi se le nascite restano, il `0.3` agiva come ABBASSAMENTO; se crollano, il
### LEGAME col gradiente è portante.**

### ⚠ **LA PERMUTAZIONE USA UN GENERATORE SEPARATO, e non è un dettaglio**

`np.random.default_rng` con **seme fisso**, ### **MAI `self.rng`** *(`:3922`)*. Se usasse
quello del simulatore, ogni permutazione **consumerebbe estrazioni** e le `rng.random(len(avv))`
della mitosi si sposterebbero: ### **il confronto non sarebbe più a parità di dado**, e la
differenza misurata conterrebbe anche il dado diverso.

### CHE COSA MI ASPETTO IO, scritto **ORA**

**Mi aspetto che le nascite CROLLINO**, cioè che il legame sia portante — e il motivo viene
dal referto `d97317a`: in `Ap` gli archi che entrano nella finestra hanno `soglia` q05 a
`6.9900` contro un pavimento di `6.9129`, ### **praticamente al minimo.** Se il morso grande
finisse su archi **a caso**, quasi nessuno di quelli con `|tw|` alto lo riceverebbe.

### ⛔ **MA QUESTO RAGIONAMENTO HA UN BUCO, E LO DICHIARO:** quel `6.99` è un effetto di
### **SELEZIONE** *(l'insieme è definito da `avv > soglia`)*, e dal referto `12e2ca7` so che
**non posso dedurne la causalità.** ### **Se potessi, questa misura non servirebbe.**
### **La mia aspettativa è un'aspettativa, non una deduzione.**

### ⚠ **E UNA COSA CHE IL BRACCIO *NON* PUÒ DIRE**

`Bperm` distrugge il legame **arco–gradiente**, ma ### **conserva la distribuzione dei morsi
nel TEMPO**: un passo con morsi grandi resta un passo con morsi grandi. ### **Quindi non
separa <<il DOVE spaziale>> da <<il QUANDO temporale>>.** Se le nascite restassero, la
lettura corretta sarebbe *«non conta QUALE arco»*, ### **non** *«non conta il gradiente»* —
perché il gradiente decide ancora **quanti** morsi grandi ci sono a ogni passo.

## 2. PROGETTAZIONE

### LE PREVISIONI DEL GUARDIANO, **scritte PRIMA**

> **le divisioni di `Bperm` stanno fra `0.5x` e `2x` di `Bp`** *(cioè fra `9` e `36`)*.

### ⚠ **E LA MIA ASPETTATIVA È L'OPPOSTA** *(crollo)*: ### **una delle due sarà
### smentita**, e questo è il punto di scriverle entrambe prima.

### I CRITERI, **fissati PRIMA e non negoziabili dopo**

| | se | allora |
|---|---|---|
| **`P1`** | `Bperm/Bp >= 0.5` | ### **il LEGAME col gradiente NON è portante**, e il `0.3` agisce come **abbassamento della soglia** |
| **`P2`** | `Bperm/Bp <= 0.2` | ### **il legame È portante**, e il gradiente **porta fisica** |
| **`P3`** | fra `0.2` e `0.5` | ### **lettura INTERMEDIA, e si dice così** |

### ✔ **E `18` DIVISIONI SONO POCHE: SI RIPORTA ANCHE `Σg1∧g2∧g3`**

Il conteggio degli archi **nella finestra** ha ### **molta più statistica** *(decine di
migliaia di passi-arco contro `18` eventi)*, e ### **lo stesso criterio si applica al suo
rapporto.**
### ⚠ **E SE I DUE CRITERI DISCORDASSERO** — divisioni e popolazione nella finestra —
### **vale quello con più statistica, e la discordanza si RIPORTA come risultato**, non si
risolve scegliendo il più comodo.

### ✔ TRE SEMI DI PERMUTAZIONE, **fissati PRIMA** — *aggiunta di Luca, 2026-10-06*

| braccio | seme |
|---|--:|
| `Bperm-s1` | `101` |
| `Bperm-s2` | `202` |
| `Bperm-s3` | `303` |

### ⛔ **E IL PERCHE' DI TRE E NON UNO E' UN LIMITE CHE AVEVO DICHIARATO IO:** *<<un seme
solo e' UNA realizzazione; se le nascite di `Bperm` fossero poche, la loro varianza su semi
diversi sarebbe grande, e con un seme solo non la conosco>>*. ### **Con `18` divisioni di
riferimento, la varianza di Poisson da sola e' `~sqrt(18) ~ 4.2`, cioe' il `24 %`:** un
rapporto misurato su un seme solo ### **non distingue `0.5x` da `0.8x`.**

**Si riportano, per ciascun seme e poi in MEDIA:**
* le **divisioni**;
* **`Σg1∧g2∧g3`** *(la popolazione nella finestra, che ha molta piu' statistica)*;
* la **dispersione** fra i tre semi.

### ✔ **E I CRITERI SI APPLICANO ALLA MEDIA**, non a un seme scelto dopo.
### ⚠ **MA SE I TRE SEMI CADESSERO IN LETTURE DIVERSE** — uno in `P1`, uno in `P3`, per
dire — ### **VA DICHIARATO**, e la media va letta **con quella riserva accanto**: una media
che sta fra due letture ### **non e' una terza lettura, e' un'incertezza.**

### ⚠ **E TRE SEMI RESTANO POCHI, e lo dico ORA:** la dispersione su tre punti e' essa
stessa rumorosa. ### **Tre bastano a dire se le letture DIVERGONO, non a stimare bene la
varianza** — e se divergessero, la cosa da fare sarebbe **piu' semi**, non scegliere.

### I CONTROLLI

| | | se fallisce |
|---|---|---|
| **`C-perm-0`** *(deve **passare**)* | con la permutazione **IDENTICA**, `Bperm` è byte-identico a `Bp` su **tutti i conteggi e tutti i passi** | ### ⛔ **la patch fa più che permutare: FERMO** |
| **`C-distr`** *(deve **passare**)* | a ogni passo il **multiinsieme** delle soglie di `Bperm` è identico a quello di `Bp`, verificato con un **ordinamento e un confronto esatto** | ### ⛔ **la permutazione non conserva la distribuzione: FERMO** |
| **`C-rng`** | `len(avv)` uguale a `Bp` finché la topologia è la stessa, e **da quale passo diverge** | si **riporta** |
| **`C1`** | `divisioni + schwinger == nati`, dal contatore del simulatore | ### ⛔ **FERMO** |

> ### 📌 **`C-perm-0` È IL CONTROLLO CHE CONTA, e il perché è che la permutazione identica
> ### è un NO-OP ARITMETICO:** `b[np.arange(len(b))]` **è** `b`, quindi il braccio deve
> riprodurre `Bp` **esattamente**. ### **Se non lo facesse, la patch starebbe cambiando
> qualcos'altro** — e il confronto con `Bp` non misurerebbe la permutazione.

> ### 📌 **E `C-distr` NON È RIDONDANTE:** `C-perm-0` prova la patch **con la permutazione
> spenta**, `C-distr` prova che **con la permutazione accesa** la distribuzione non si
> muove. ### **Sono due cose diverse, e servono entrambe.**

## LA STELLA POLARE

**1 — `A14`.** **Non si applica alla misura**, che legge. ### ⚠ **Ma si applica a ciò che
potrebbe far decidere:** se il `0.3` fosse un abbassamento mascherato, ### **la materia nata
grazie a lui sarebbe nata per un numero a mano** — e *«quella massa da dove viene»* è `A14`.
### **Nominata, non risolta.**

**2 — i tre gradini.** Gradino **(a)**: stessa scena, stesso seme, e ### **il dado resta lo
stesso** *(generatore separato)*. ### ✔ **Gradino (b) È IL PUNTO:** *«regge togliendo la
legge pratica?»* — qui la legge pratica non si toglie, ### **si RANDOMIZZA**, che è più
informativo: ### **separa la FORMA dall'AMPIEZZA.** ### ⛔ **Gradino (c): NO**, nessun
limite noto per un conteggio di nascite su questa scena.

**3 — numeri e leggi.** ### **ZERO aggiunti.** La misura introduce **un seme** per la
permutazione, che è ### **un parametro dello STRUMENTO e non della fisica** — e si dichiara.
### ⚠ **E un seme solo è UNA realizzazione:** se le nascite di `Bperm` fossero poche, la
loro varianza su semi diversi sarebbe grande, e ### **con un seme solo non la conosco.**
### **Lo dichiaro invece di scoprirlo dopo.**

**4 — `rho`, `c_s`, il SEGNO.** La misura non li tocca. Legge `r` *(che viene da `cs`)*; il
**SEGNO** resta il cancello `3`, non modificato.

**5 — emergente o imposto.** ### **È LA DOMANDA, nella sua forma più nitida:** una legge che
porta **per la sua FORMA** è diversa da una che porta **per la sua AMPIEZZA**.
### **`Bperm` tiene l'ampiezza e distrugge la forma.** ### ⛔ **E se le nascite restassero,
la risposta sarebbe <<IMPOSTO>>** — cioè il `3π` sarebbe il numero da discutere, non il
`0.3`.

## ⛔ ANNOTAZIONE DEL 2026-10-06 — **L'EFFETTO LOTTERIA**: la permutazione si ripesca
## A OGNI PASSO, e spinge le nascite VERSO L'ALTO

*(Osservazione del guardiano sul blob `7eae0618`/`b399adb2`, ### **scritta mentre la corsa e'
IN VOLO e PRIMA di vederne i numeri.** La verifica l'ho fatta **io** sul codice dello
strumento.)*

### LA VERIFICA — **il guardiano ha ragione**

| | |
|---|---|
| la patch | `_p = _PRNG.permutation(len(_bite))` sta **dentro** il blocco che sostituisce la riga della soglia |
| dove vive | in `decidi_divisione`, chiamata a `:8658` **da `mitosi()`** |
| quante volte | `mitosi` gira **una volta per passo** *(terza legge di `_passo.ordine()`)* |

### ➜ **QUINDI LA PERMUTAZIONE SI RIPESCA A OGNI PASSO: `150` lotterie per arco.**

### ⛔ **E IN `Bp` LA SOGLIA DI UN ARCO E' PERSISTENTE**

Il morso di un arco e' `0.3*tanh(|r_i - r_j|)`, e il gradiente di `r` **varia lentamente**:
### **un arco con gradiente piccolo ha una soglia alta SEMPRE.** In `Bperm` lo stesso arco
riceve ### **una lotteria nuova a ogni passo**, e prima o poi pesca un morso grande.

### ✔ **E L'EFFETTO SI PUO' QUANTIFICARE PRIMA DI VEDERE I NUMERI, cosa che lo rende una
### previsione e non una scusa**

La probabilita' che un arco **non veda MAI** un morso del **decile alto** in `150` estrazioni
indipendenti e' `0.9^150` = ### **`1.37e-07`.** Cioe' ### **praticamente OGNI arco, nel corso
della corsa, riceve almeno una volta una soglia fra le piu' basse** — mentre in `Bp` solo
gli archi ad alto gradiente la vedono, e **sempre quelli**.

### ⚠ **QUINDI L'EFFETTO LOTTERIA SPINGE LE NASCITE DI `Bperm` VERSO L'ALTO, cioe' NELLA
### DIREZIONE DELLA PREVISIONE DEL GUARDIANO** *(`0.5x`-`2x`)* **e CONTRO la mia**
*(crollo)*. ### **Lo scrivo adesso, prima dei numeri: se la mia previsione risultasse giusta,
sarebbe giusta NONOSTANTE un effetto che la ostacola.**

### COME SI LEGGE, **fissato ORA**

| se | il risultato e' |
|---|---|
| vale **`P2`** *(crollo)* | ### **ROBUSTO: crolla NONOSTANTE la lotteria** |
| vale **`P1`** o **`P3`** | ### **AMBIGUO** fra *<<non conta quale arco>>* e *<<lotteria>>* |

### ✔ **E NEL CASO AMBIGUO, DOPO IL REFERTO, SI AGGIUNGE `Bperm-fisso`**

Permutazione ripescata ### **SOLO quando `len(avv)` CAMBIA**, stessi tre semi, stessi
controlli, stessi criteri. ### **Il referto finale li riporta ENTRAMBI.**

### ✔ **E IL FATTORE E' MISURATO, non stimato:** nel braccio `Bp` committato *(`dd86933`)*
`len(avv)` cambia ### **`12` volte su `150` passi**, quindi `Bperm-fisso` ripescherebbe
**`13`** volte invece di `150` — ### **un fattore `11.5` di lotterie in meno.** E la
probabilita' di non vedere mai il decile alto passa da `1.37e-07` a ### **`0.254`**: con
`13` estrazioni ### **un quarto degli archi non vede mai una soglia bassa**, che e' molto
piu' vicino al comportamento persistente di `Bp`.

> ### ⚠ **MA `Bperm-fisso` NON E' <<`Bperm` SENZA IL DIFETTO>>, e va detto:** ripescare solo
> alla crescita ### **lega la permutazione alla TOPOLOGIA**, cioe' introduce una
> correlazione nuova *(i morsi cambiano **quando** nasce un nodo)*. ### **Riduce la lotteria,
> non la toglie, e cambia una cosa per un'altra.** Il confronto fra i due bracci dice
> **quanto** pesa la lotteria; ### **nessuno dei due e' il braccio <<pulito>>.**

## ⛔ ANNOTAZIONE DEL 2026-10-06 — **L'ESITO: la mia previsione e' REFUTATA**

*(Scritta **dopo** i numeri, e ### **il ragionamento preliminare qui sopra NON si riscrive**:
resta com'era, sbagliato, come il par.8 pretende.)*

| | la previsione | esito |
|---|---|---|
| **il guardiano** | divisioni fra `0.5x` e `2x` *(fra `9` e `36`)* | ### **CONFERMATA** |
| **io** | le nascite **CROLLANO** | ### ⛔ **REFUTATA** |

Misurato: divisioni `27`/`28`/`30` sui tre semi, media `28.33` *(dispersione `1.25`)*,
### **rapporto `1.5741` sulle divisioni e `1.1009` sulla finestra: `P1` su entrambi, e i tre
semi nella STESSA lettura.** I quattro controlli passano.

### ⛔ **DOVE HO SBAGLIATO:** il mio ragionamento poggiava sul `q05` della soglia a `6.9900`,
che il referto `12e2ca7` aveva **gia' stabilito** essere un effetto di **SELEZIONE**. ### **Da
un effetto di selezione non si deduce la causalita'** -- l'avevo scritto, e poi ci ho
ragionato sopra come se fosse una deduzione.

### ✔ **E LA REGOLA DELLA LOTTERIA SCATTA:** `P1` ⟹ ### **AMBIGUO**, quindi
### **`Bperm-fisso` non e' una scelta fatta dopo i numeri: era fissata in `f922c20`, prima.**

## 3. TODO DEL NEXT STEP

1. **commit di questo task history**, prima dello strumento, ### **DA SOLO**;
2. lo **strumento**: il braccio `Bperm` *(patch sulla **sola** riga della soglia, generatore
   separato)*, il modo **permutazione identica** per `C-perm-0`, la verifica `C-distr`, e il
   **collaudo**;
3. **commit dello strumento**, prima della corsa;
4. la **corsa** *(`Bperm-s1`, `Bperm-s2`, `Bperm-s3` e `Bperm-id`, in **lockstep**; `Bp` viene dal `soglia.json` committato)*;
5. i **controlli**, e `FERMO` se `C-perm-0`, `C-distr` o `C1` falliscono;
6. il **referto**, **generato**, con `P1`/`P2`/`P3` applicati ### **alla MEDIA dei tre semi**, il confronto fra **divisioni** e **popolazione nella finestra**, e ### **la dichiarazione se i tre semi cadono in letture diverse**;
7. ### ⛔ **poi FERMO, e si aspetta Luca.**
