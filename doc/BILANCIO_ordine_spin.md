# IL BILANCIO DEI TASSI — l'ordine di spin **nasce** e viene **distrutto**

> **Scritto per Claude web.** Branch `fork-su2`, 2026-09-15. Blob sul disco **`f5887254`**
> (gate in `CLAUDE.md` §0 su `c0803713`: disallineamento voluto, ramo turbo diagnostico).
> **Nessuna modifica alla fisica.** Stato: **FASI A, B e C chiuse.**

---

## 0. LA RIFORMULAZIONE — perché questo lavoro non è «un settimo lato»

Sei misure convergenti dicono che lo spin è *frozen-o-noise*. Ma dal codice emerge un fatto che
**cambia la domanda**: alla mitosi il figlio eredita il padre per **copia esatta**. Quindi

> **ogni nascita crea una coppia perfettamente correlata (chi = 0).**

E la misura dice **chi = 90° ovunque**. Segue che **l'ordine non manca: nasce di continuo e viene
distrutto.** Il problema non è «serve un meccanismo ordinante» — sarebbe la strada che porta a
*imporre* un Kuramoto, già refutata — ma **un bilancio fra due tassi già presenti nel sistema**:

| | chi lo produce |
|---|---|
| **creazione** di correlazione | la mitosi (eredità esatta) |
| **distruzione** | rumore del vuoto + precessione mutua (misurata come **attivamente disordinante**: 60° → 104° a rumore spento) |

Questo documento **misura i due tassi**. Non aggiunge meccanismi.

---

## 1. FASE A — IL FATTO, VERIFICATO

### 1.1 L'eredità è una copia esatta, senza perturbazione

`_eredita_spinore_figli` ([`soliton_simulator.py:1133-1170`](../soliton_simulator.py#L1133-L1170)),
chiamata da `mitosi` a [`:3125`](../soliton_simulator.py#L3125):

| campo ereditato | riga | come |
|---|---|---|
| `_nb` (Bloch) | `:1147` | `vstack([_nb, _nb[src]])` — **esatta** |
| `_nb_prec` | `:1149` | esatta |
| `_nb_ret` (ritardato, Strato 1) | `:1155` | esatta |
| `omega_s` (memoria hebbiana) | `:1157` | esatta |
| `_psi_spinor` (primario complesso) | `:1159-1161` | `.copy()`, con `−` per gli antinodi |
| `_spinor_lift` | `:1164` | idem |
| `_psi_prec` | `:1169` | esatta |

**Nessun jitter, nessuna perturbazione, nessun gating** oltre al flag
(`SPINORE_CORRETTO or CAMPO_SPINORIALE`, entrambi attivi nei run del fork).

> **Conseguenza non ovvia, da tenere:** l'antinodo Schwinger ([`:3242`](../soliton_simulator.py#L3242),
> `segno=-1`) eredita `−ψ`. Ma `nb = ψ†σψ` è **invariante per fase globale**, e `−1 = e^{iπ}` lo è:
> `conj(−a)(−b) = conj(a)b`. **Anche l'antinodo nasce con chi = 0 in Bloch.** «Antichirale» riguarda
> il segno di doppia copertura, **non** la direzione. Il tasso di creazione di coppie correlate
> include quindi *anche* le Schwinger, non solo le mitosi.

### 1.2 Il figlio nasce adiacente — nello spazio **e** nella topologia

- **spazio:** [`:3094`](../soliton_simulator.py#L3094) `pos_figlio = 0.5*(pos[a] + pos[b])`, il punto
  medio dell'arco. Il kernel `e^{−d/λ}` li accoppia **per costruzione**, non per caso.
- **topologia:** [`:3172-3173`](../soliton_simulator.py#L3172-L3173) l'arco del padre viene
  **rimosso** e sostituito da `(a,m)` e `(m,b)`. Il figlio nasce con **esattamente due archi**,
  verso entrambi i genitori.

### 1.3 La parentela **non è registrata**, ma è **ricostruibile in volo**

Nessun array di lignaggio esiste. Gli unici `parent` del file
([`:949-982`](../soliton_simulator.py#L949-L982)) sono lo spanning-tree di
`_base_cicli_topologici`: **topologia di grafo, non genealogia**. `conc_nodi` eredita l'**ID di
massa**, non l'indice del padre.

**Ma un osservatore per passo la ricostruisce**, e il padre `a` — quello da cui si eredita — è
distinguibile da `b`: nell'arco `(a,m)` il padre sta nel lato `i`, il figlio nel lato `j`.
Verificato, non dedotto (`csv/_test_fork/_parentela_bloch.py`):

```
nuovi nodi osservati             : 7
  con ESATTAMENTE 2 genitori     : 7  (100.0%)
  con il padre `a` identificabile: 7  (100.0%)
```

> **Quindi la FASE B può fare la misura VERA** (coppie padre-figlio seguite nel tempo), **non un
> proxy.** Era questo a essere in dubbio.

---

## 2. IL FATTO È CONFERMATO — ma il numero accanto è quello che conta

```
chi PADRE-FIGLIO alla nascita (gradi), n=7:
   media 0.0000  mediana 0.0000  min 0.0000  max 0.0000
   VALORE-NULL (direzioni casuali): 90.000 +- 39.171
```

Correlazione **perfetta ed esatta**, come prevede la copia. Ma nello **stesso passo**:

```
spostamento del PADRE nel passo della nascita (gradi), n=7:
   media 85.6452  mediana 95.8363  min 36.6732  max 108.7353
```

> **Il Bloch di un nodo si sposta di ~90° in UN passo: decorrela da sé stesso in un tick.**

Cioè si colloca già sul valore-null della decorrelazione completa. Se regge sulla statistica,
`tau_dec ≲ 1 passo` e il verdetto della FASE B è **già indicato**: `tau_dec << tau_mit`, sistema
**dominato dalla distruzione**, coerente con `chi = 90` ovunque.

**Ma sette campioni non sono una misura,** ed è esattamente il genere di numero a cui si crede
troppo presto. La FASE B lo rifà sulla scena reale con centinaia di nascite. Finché non è rifatto,
questo è un **indizio**, non un risultato.

---

## 3. IL CANALE DEL RUMORE NON È QUELLO CHE SI PRESUME (pesa sulla FASE C)

Sotto `--spinore-corretto` con `SYNC_UPDATE = False` — cioè **la configurazione di tutti i run del
fork**:

- il rumore a [`:1847`](../soliton_simulator.py#L1847) colpisce `self._nb`…
- …ma il `_nb` **committato** è **derivato** da `_psi_spinor`
  ([`:2066-2069`](../soliton_simulator.py#L2066-L2069), [`:2088`](../soliton_simulator.py#L2088));
- il rumore additivo **diretto** sul Bloch ([`:2060`](../soliton_simulator.py#L2060),
  [`:2085`](../soliton_simulator.py#L2085)) è gated su `SYNC_UPDATE` ed è **spento**.

> Il rumore entra **solo** via `correzione = cross(B, nb)` → `omega_new` → rotazione.
> **È rumore di COPPIA, non di posizione sulla sfera.**

Non è un dettaglio di implementazione: cambia la legge attesa di decorrelazione (diffusione
sull'**angolo di rotazione**, non sulla posizione) e tocca direttamente l'ipotesi della FASE C,
perché `omega_s` **ha già memoria** (`TAU_A`, e `TAU_A_LOCALE` la rende locale). Un canale a cui
«dare memoria» ce l'ha già, e resta comunque disordinato: è un vincolo forte sulla classifica.

---

## 4. LA PRECISAZIONE DA NON PERDERE — la memoria **non ordina**

Un rilassamento `dx/dt = (x_eq − x)/tau` **rallenta** i cambiamenti, non li **orienta**.
La prova è già nel repo: lo **Strato 1 è memoria pura**, ed è passato 23/23 **senza ordinare i
Bloch**. La memoria agisce **sui tassi** — filtro passa-basso sul rumore veloce, vita più lunga
della correlazione ereditata — quindi la domanda giusta per ogni canale è **un confronto di tempi**,
non «aiuta o no».

---

---

## 5. FASE B — I DUE TASSI

### 5.0 Il sigillo, PRIMA della misura (§2.3)

L'osservatore legge **solo** array di stato (`i`, `j`, `_nb`, `pos`, `d`, `n`): mai `calcola_psi()`,
`ritmo()`, `_pesi()`, `_lam_archi()`, che mutano cache di continuità lette dalla dinamica. Il
sigillo lo **dimostra**, confrontando due run identici con e senza osservatore:

```
n senza osservatore = 1636   n con osservatore = 1636   ->  CONFRONTABILI
19 campi su 19 (pos phi phi0 phivel eta d d0 vd peq tw twp i j perc_chi perc_tw
                _nb _psi_spinor omega_s psi)      ->  max|A-B| = 0.000e+00
stato RNG                                          ->  identico
SIGILLO: PASS
```

> **Presidio applicato** (`CLAUDE.md` §9): la riga dei conteggi è stampata **per prima**. Uno zero
> con `N` diverso sarebbe **mancanza di confronto**, non identità.

### 5.1 B1 — il tasso di CREAZIONE

Scena reale (3 masse, `sep 8`), **250 passi**, **due semi**.

| | seme 1 | seme 2 |
|---|---|---|
| coppie padre-figlio registrate | **2402** | **1761** |
| nascite per passo | media 9.61, mediana 8 | media 7.04, mediana 5 |
| N finale / archi / grado medio | 3598 / 210530 / 117.0 | 2957 / 209677 / 141.8 |
| **`tau_mit` LOCALE** | **187.2 passi** | **209.9 passi** |
| `tau_mit` globale (raddoppio) | 374.5 passi | 419.8 passi |

`tau_mit` locale `= 1/(grado_medio · nascite_per_arco_per_passo)`: è il tasso che compete col
disordine **locale**, non quello globale, come richiesto dal mandato.

### 5.2 B2 — il tasso di DISTRUZIONE, e il confondente **escluso**

**Valore-null sempre accanto:** `chi` casuale = **90.000 ± 39.171**; bersaglio 1−1/e = **56.891**.

**Seme 1** (2402 coppie):

| età | `<chi>` gradi | n | distanza | d/LAM | arco diretto vivo |
|---|---|---|---|---|---|
| 0 | **0.000** | 2402 | 0.539 | 0.67 | **100.0%** |
| **1** | **89.739** | 2401 | **0.540** | 0.68 | **100.0%** |
| 2 | 90.362 | 2396 | 0.542 | 0.68 | 100.0% |
| 10 | 90.659 | 2376 | 0.556 | 0.70 | 99.7% |
| 40 | 90.622 | 2253 | 0.629 | 0.79 | 98.6% |
| 80 | 89.641 | 2075 | 0.727 | 0.91 | 97.8% |

**Seme 2** (1761 coppie): identico nella sostanza — età 1 → `chi` **90.715**, distanza **0.486**
contro 0.485 alla nascita, arco vivo **100.0%**; età 80 → `chi` 89.462, distanza 0.664, arco 97.2%.

> **`tau_dec` = 0.63 passi.** Identico sui due semi.

**Il confondente è ESCLUSO, non stimato.** Alla prima età in cui `chi` è già al valore-null:
- la **distanza è invariata** (0.540 contro 0.539; 0.486 contro 0.485) — i due non si sono mossi;
- l'**arco diretto è vivo al 100.0%** — sono ancora accoppiati dal kernel.

**Decorrelano da ADIACENTI e CONNESSI.** Non è disaccoppiamento geometrico: è **disordine**.
Lo conferma la coda: a età 80 la distanza è cresciuta solo da 0.54 a 0.73 (`d/LAM` da 0.67 a 0.91)
e l'arco è ancora vivo al 97.8%, mentre `chi` sta a 90 da **ottanta passi**. L'allontanamento è
lentissimo, la decorrelazione istantanea: **due ordini di grandezza di separazione fra i due
effetti.**

### 5.3 B3 — IL VERDETTO DEL BILANCIO

| | seme 1 | seme 2 |
|---|---|---|
| `tau_dec` | **0.63 passi** | **0.63 passi** |
| `tau_mit` locale | 187.2 passi | 209.9 passi |
| **rapporto `tau_mit`/`tau_dec`** | **295** | **335** |

> **`tau_dec` ≪ `tau_mit`, di quasi TRE ORDINI DI GRANDEZZA. DOMINIO DELLA DISTRUZIONE.**
> L'ordine muore ~300 volte più in fretta di quanto ne nasca.

È la prima delle tre letture scritte **prima** di misurare, e spiega `chi = 90` ovunque **senza
bisogno di un meccanismo mancante**: l'ordine c'è, nasce a ogni mitosi, e non sopravvive a un
singolo tick.

---

## 6. FASE C — QUALI CANALI MERITANO MEMORIA

### 6.0 Il numero che decide tutto

Sonda pure-read su stato evoluto (`csv/_test_fork/_canali_disordine.py`, passo 60, seme 1,
n=2123, archi 208708). **`omega_s` letto DIRETTAMENTE dal simulatore**, non ricostruito:

```
|omega_s| (memoria hebbiana)   mediana  4.90e+04 rad/tempo   [5%..95%] 1.36e+04 .. 1.21e+05
theta_vero = |omega_s| * dt_n  mediana  2.40e+04 GRADI per passo
giri interi per passo (mediana)                : 66.7
frazione di nodi con theta > 360 gradi         : 99.3%
```

> **Il Bloch non «diffonde»: fa ~67 GIRI COMPLETI per tick.**

Non c'è alcun clamp su `theta` ([`:2033-2037`](../soliton_simulator.py#L2033)): la rotazione SU(2)
viene applicata così com'è. Dopo 67 giri la direzione finale dipende dalla parte frazionaria di un
numero enorme — una variazione di `omega` di una parte su 10^4 cambia del tutto il risultato.
**Non è errore numerico** (in doppia precisione `cos` a ~400 rad è accurato): è **sensibilità
amplificata di 67 giri per passo**. Il settore di spin **non è risolto nel tempo** dal passo `DT`.

Questo spiega *meccanicamente* le sei misure negative: `chi = 90` non è «assenza di una forza
ordinante», è **rimescolamento per sotto-risoluzione**. E si salda con la FASE B: `tau_dec = 0.63`
passi non è un dato misterioso — è quello che si ottiene ruotando di 67 giri per tick.

### 6.1 Da dove viene: l'inerzia è **sette ordini** sotto l'unità

```
|cross(B,nb)| (coppia nuda)   mediana  6.05e-02        <- ordinaria
rho sorgente                  mediana  1.21e-07        <- SETTE ordini sotto 1
inerzia = max(rho, 1e-6)      mediana  1.00e-06
frazione di nodi col pavimento 1e-6 attivo : 99.7%
|omega| = coppia/inerzia      mediana  6.02e+04
```

`omega = coppia / inerzia`, con l'inerzia posta uguale alla densità
([`:1891`](../soliton_simulator.py#L1891)). La coppia è **ordinaria**; è **l'inerzia a essere
minuscola**, e il rapporto esplode.

> **ONESTÀ — il pavimento `1e-6` NON è la causa: la MITIGA.** Senza, l'inerzia sarebbe `1.21e-07`
> e `omega` sarebbe **otto volte più grande**. La causa è che la densità vale ~1e-7 alle scale
> simulabili.

Ed è **la stessa famiglia** del problema già noto su `cs` (`CLAUDE.md` §6: *a densità reali cs è
MORTO, I~0.05 contro soglia ~400*), con il segno opposto:

| settore | grandezza | alle scale simulabili | effetto |
|---|---|---|---|
| metrica | `cs = CS_M/(1+GAMMA·sqrt(I))` | `I` troppo **bassa** | `cs` **congelato** a `CS_M` |
| spin | `omega = coppia/densità` | densità troppo **bassa** | `omega` **esplosa** |

**Una sola radice: la densità è minuscola alle scale simulabili.** Congela un settore e fa esplodere
l'altro. Non è una congettura: sono i due numeri misurati, messi accanto.

### 6.2 Il punto che ROVESCIA l'ipotesi

Dalla riga [`:1918`](../soliton_simulator.py#L1918):

```
omega_new = omega_src + dt_n * (coppia/inerzia - omega_src/tau)
```

è un rilassamento del **primo ordine**, il cui **punto fisso** è

> **omega_eq = tau · coppia / inerzia**

cioè **omega è PROPORZIONALE alla memoria**. Misurato:

```
tau (TAU_A locale) / DT                        mediana  2.47e+03 PASSI   [5%..95%] 250 .. 8.7e+03
tau_disordine (passi per ruotare di 90 gradi)  :        0.0030 PASSI
```

> `tau_memoria / tau_disordine` è circa **8·10^5**. Il canale che «dovrebbe essere filtrato dalla
> memoria» **ha già la memoria più lunga del sistema — 2470 passi — e ruota di 67 giri per passo.**

**L'ipotesi «dare memoria combatte il disordine» è REFUTATA su questo canale, e per un motivo
strutturale, non accidentale:** la memoria vive sulla **velocità angolare**, non sulla direzione.
Un rilassamento su `omega` **conserva la rotazione**, non la posizione — e per giunta ne **alza il
punto fisso**. Dare *più* memoria qui farebbe girare il Bloch **più in fretta**.

È coerente con la precisazione di partenza (la memoria non ordina, sposta il bilancio) e con lo
Strato 1, memoria pura passata 23/23 **senza** ordinare i Bloch. Qui si vede il caso in cui la
memoria sposta il bilancio **dalla parte sbagliata**.

### 6.3 Il canale dei pesi: non è il collo

```
|B| MISURATO                  mediana  0.0694
1/sqrt(k_eff) atteso casuale  mediana  0.0649        <- rapporto 1.07
k_eff = (sum w)^2/sum w^2     mediana  237 vicini efficaci
|B| NULL (vicini permutati)   mediana  0.124
```

Il campo misurato coincide col valore di **direzioni indipendenti casuali** entro il **7%**: quello
che pilota la coppia è la media di ~237 vicini **scorrelati**. I pesi non producono coerenza —
non c'è coerenza da pesare.

> **Onestà sul null:** il null per **permutazione** (0.124) **non è pulito** e va letto con cautela.
> Permutando i Bloch si rompe anche l'accoppiamento con il segno chirale (che **non** viene
> permutato), quindi quel null misura due cose insieme. Il riferimento pulito è `1/sqrt(k_eff)`, ed
> è quello che combacia. Lo riporto lo stesso perché l'ho misurato: non si nasconde un null che non
> ha funzionato come previsto.

### 6.4 LA CLASSIFICA — ogni voce col numero che la sostiene

| canale | è porta d'ingresso del disordine per lo SPIN? | verdetto |
|---|---|---|
| **`omega_s`** | **SÌ, è LA porta.** Il rumore entra **solo** via `cross(B,nb)` e poi `omega` ([`:1895`](../soliton_simulator.py#L1895), [`:1918`](../soliton_simulator.py#L1918)) | **ha GIÀ memoria** `tau ≈ 2470` passi, e la memoria **PEGGIORA**: `omega_eq = tau·F`. Più memoria, più rotazione. **Da NON aumentare.** |
| **densità** (`rho`) | entra come **divisore**, ma il **99.7%** dei nodi è **sotto il pavimento** | **escluso col numero**: darle memoria non cambia il divisore per il 99.7% dei nodi |
| **`cs`** | **no**: raggiunge lo spin **solo** via `omega_clk`, che è una **fase globale**, quindi `nb` resta invariante (**3.3e-16**) | **escluso col numero**, e confermato dall'**esito B** a K=300 |
| **pesi** (`w`) | entrano nel campo, ma il campo è al valore casuale entro il **7%** | **non è il collo**: il disordine è nei **vicini**, non nei pesi |
| **`_psi_spinor`** | è lo **stato** disordinato, non la porta; evolve per rotazione unitaria, senza rilassamento | **non è il canale** |
| **`_nb`** (Bloch) | è un **VINCOLO**, derivato dallo spinore ([`:2066-2069`](../soliton_simulator.py#L2066)) | **escluso per principio** |

**Vincoli, esclusi per principio** — darebbero memoria a una **definizione**, non a una dinamica, e
la romperebbero: la densità come modulo quadro del campo, il Bloch come proiezione dello spinore, la
norma unitaria.

> **Nessun canale merita più memoria.** Il solo che è davvero la porta del disordine ne ha già la
> quantità massima del sistema, e aumentarla peggiorerebbe. L'ipotesi è **refutata con i numeri**,
> non accantonata.

---

## 7. IL REPERTO, e la domanda che apre

Il mandato prevedeva che `tau_dec >> tau_mit` sarebbe stato un reperto. Il reperto è arrivato
dall'**altro estremo**, e non era previsto da nessuna delle tre letture:

> **il settore di spin non è risolto nel tempo.** La rotazione per passo vale **~67 giri**, perché
> `omega = coppia/densità` con una densità di ~1e-7.

Le sei misure negative **restano valide** — nessuna è invalidata, e il disordine è reale nel sistema
come gira oggi. Ma la loro **interpretazione cambia**: non dicono «non esiste una fisica ordinante»,
dicono «**in questo regime numerico nessun ordine può sopravvivere a un tick**».

**Due strade, entrambe decisioni di Luca — non le ho prese e non ho toccato nulla:**
1. **risolvere il tempo dello spin:** un sotto-passo per il settore spinoriale, come già esiste
   `nsub` per la metrica (il CFL delle onde). Sarebbe **lo stesso principio già nel sistema**, non
   un meccanismo nuovo;
2. **guardare la scala:** una densità di ~1e-7 è la stessa radice per cui `cs` è morto. Se è un
   problema di scala, il settore di spin va provato dove la densità è O(1) — e allora **l'esito B
   su `cs` e i sei lati andrebbero riletti in quel regime**, non in questo.

**Il test decisivo che NON ho fatto** (richiederebbe di cambiare la fisica, quindi la tua
autorizzazione): fissare `TAU_A` a due valori diversi a parità di tutto il resto, e verificare la
predizione `omega_eq` proporzionale a `tau`. Se confermata, chiude il §6.2 per misura e non per
derivazione. **Attenzione:** `--regime` **non** serve a questo — cambia `TAU_A` *insieme* a `G_PH`,
`_CALORE_INIT` e `SCUOTIMENTO`: quattro interruttori insieme, contro §1.

---

## 8. STATO

| fase | stato |
|---|---|
| **A** — il fatto, l'adiacenza, la parentela ricostruibile | **chiusa** |
| **B** — i due tassi, confondente separato, verdetto | **chiusa** — dominio della distruzione, 2 semi |
| **C** — classifica dei canali col confronto dei tempi | **chiusa** — nessun canale merita più memoria |

**Caveat, interi:**
1. La FASE C è misurata a **passo 60, un seme, una scena**. `tau_dec` è confermato su **due semi** e
   4163 coppie; i **67 giri per passo no**: vanno rifatti su più semi e a tempi diversi prima di
   trattarli come stabili.
2. Il null per permutazione del campo **non ha funzionato come previsto** (§6.3): riportato con il
   suo difetto, non scartato.
3. **Nessuna implementazione**, come da mandato: nessun flag, nessuna memoria aggiunta, nessuna
   costante di tempo nuova.

---

## 9. COSA NON È STATO TOCCATO

`soliton_simulator.py` **non è stato modificato**: blob sul disco `f5887254`, lo stesso di prima di
questo lavoro, `git status` pulito. I due diagnostici (`_parentela_bloch.py`, `_tassi_coppie.py`)
leggono solo array di stato, e il secondo è **sigillato PASS** su 19 campi più lo stato dell'RNG.
`_canali_disordine.py` lavora su una **copia profonda** della rete, così anche le mutazioni di cache
delle funzioni del simulatore che usa restano confinate lì.
