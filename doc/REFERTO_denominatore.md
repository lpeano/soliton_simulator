# REFERTO — **(A) o (B)? LA MISURA NON DISTINGUE. Ma (B) cade per DIMOSTRAZIONE**

**Data:** 2026-09-17 · **Branch:** `fork-su2` · **HEAD** `c440a5c` · **Blob** `5d61af08` (byte) /
`425e4aaa` (git — sono due spazi di hash diversi, il mandato cita il secondo)
**Strumento:** `csv/_test_fork/_misura_denominatore.py` · **Output:** `_misura_denominatore.txt`
**Mandato §5.2:** *«la misura che decide fra (A) e (B) → STOP e riporta»*. **Mi fermo qui.**

> **Nota su una citazione del mandato:** il referto precedente è `doc/REFERTO_2706.md`, non
> `doc/REFERTO_sonda_2706.md`.

---

## 0. IN UNA RIGA

**La misura NON distingue (A) da (B): entrambe ripristinano l'antisimmetria all'epsilon macchina, e
le differenze sulla conservazione sono dentro il rumore di tre traiettorie che divergono.**
**Ma (B) cade per un'altra strada: la sua premessa è falsa.**
**E l'«alternativa» suggerita dal mandato è algebricamente IDENTICA al codice attuale.**

---

## 1. LA PREMESSA DI (B) NON REGGE — verificato dal sorgente, non misurato

Il mandato fonda (B) su: *«C'è già una divisione per l'inerzia a valle:
`omega_new = omega_src + dt_n*(coppia/inerzia − omega_src/tau)` — quindi `/grado` è una SECONDA
normalizzazione»*.

**Dal disco:**

| punto | cosa c'è davvero |
|---|---|
| `:3113` | **unica** chiamata a `_feedback_spinoriale_archi` |
| `:3129` | `coppia += _fb` |
| `:3197` | `delta_phivel = dt_n_s * (coppia − G_PH*_phivel_t) / **M_PH**` |
| `:206` | **`M_PH = 1.0`** — una **costante globale**, non una massa per nodo |
| `:2283` | l'**unica** `/inerzia` del file: `omega_new = omega_src + dtn_c*(**correzione**/inerzia[:,None] − …)` — divide **`correzione`** (un 3-vettore), **non `coppia`** |

**Il feedback agisce su `phivel` — il settore della FASE. `omega_s` e `inerzia` — il settore dello
SPIN — non lo vedono mai.** Sono due catene separate.

> **Quindi non c'è nessuna doppia divisione da togliere: a valle c'è una COSTANTE.**
> **(B) è esclusa per DIMOSTRAZIONE, non per misura** — che è la distinzione che CLAUDE.md impone
> (*«si misura per promuovere, si dimostra per escludere»*).

**E una seconda ragione indipendente:** togliere `/grado` non rimuove *una* normalizzazione di
due — rimuove **l'unica**. Un nodo con cento archi accumulerebbe cento volte, e a valle non c'è
nessuna massa per nodo che lo assorba.

---

## 2. ⚠ E IL CRITERIO CAMBIA — **in questo settore `sum(out) = 0` È la legge di conservazione**

Il mandato avverte, giustamente: *«`sum(coppia)` non è una legge fisica; ciò che si conserva è
`sum(I·omega)`, e `I` è diversa per ogni nodo»*.

**Quell'avvertenza vale per il settore dello SPIN. Qui la massa è UNIFORME:**

```
d/dt sum(phivel) = sum(coppia) / M_PH        con M_PH costante
        =>        sum(out) = 0   <=>   sum(phivel) si conserva,  esattamente
```

**`G1` non è quindi un criterio di forma: è la conservazione stessa.** E `L_tot = sum(I·|omega|)`
non è lo strumento giusto per questo termine, perché misura un settore in cui il feedback non entra.

*(Non ho calcolato `L_tot`: il simulatore **non espone l'array dell'inerzia** — è una locale di
`_passo_spinoriale`, e `L_tot` nasce dalle colonne CSV della campagna. Metterci `I = 1` avrebbe dato
un `sum(|omega|)` **travestito da `L_tot`**: il fallback silenzioso che P5 vieta. Riporto
`sum(|omega_s|)` **col suo nome**, come secondario.)*

---

## 3. LA MISURA — tre varianti, stessa scena, `TAU_A = 2.0`, 60 passi, **un seme**

```
(0) ATTUALE   out[i] -= f/g_i ; out[j] += f/g_j        denominatori DIVERSI
(1) SENZA     out[i] -= f     ; out[j] += f            nessun denominatore   <- lettura (B)
(2) SIMM      out[i] -= f/g_ij; out[j] += f/g_ij       g_ij = sqrt(g_i·g_j)  <- lettura (A)
```
*(`sqrt(g_i·g_j)` è **una scelta (A1)**, messa solo per isolare l'effetto della **simmetrizzazione
in sé**. **Non è la cura proposta.**)*

### `G1` — l'antisimmetria. **Verifica ALGEBRICA, non statistica**

| variante | mediana | MAX |
|---|---|---|
| **attuale** | **1.112e+00** | **8.441e+00** |
| **senza** | **6.475e-16** | 2.752e-15 |
| **simm** | **8.540e-16** | 3.641e-15 |

**Quindici ordini di grandezza fra `attuale` e le altre due.** Confermato il difetto, e confermato
che **è il denominatore**: entrambe le cure lo tolgono, **esattamente**.

**Ma proprio per questo `G1` NON discrimina fra (A) e (B): entrambe lo passano.**

### Il criterio fisico del settore — deriva di `sum(phivel)`

| variante | `sum\|d_step\|` | `sum\|d_mit\|` | deriva TOT | `\|deriva\|/scala` | n finale |
|---|---|---|---|---|---|
| attuale | 298.14 | 16.54 | −70.41 | 1.0658 | **548** |
| senza | 293.51 | 25.67 | −118.14 | 1.0382 | **564** |
| simm | **243.16** | **14.04** | +53.17 | **0.92442** | **554** |

`simm` è il migliore su tutte e tre le colonne. **E non lo uso per decidere, per una ragione che si
legge nell'ultima colonna: `n finale` è 548 / 564 / 554 — le tre traiettorie DIVERGONO.**

Sto confrontando **tre sistemi diversi**, non tre misure dello stesso. Le differenze sono del ~18 %
su `sum|d_step|`, **su un seme, senza nullo misurato**, e il nullo caotico noto sul conteggio nodi
vale già ~1.4 % mentre qui `n` differisce del **2.9 %**.

> **La misura NON distingue (A) da (B).** Lo dico invece di sceglierne una, come §4 ordina.

### Secondario — `sum(|omega_s|)`, **e non è `L_tot`**

| variante | passo 0 | finale | rapporto |
|---|---|---|---|
| attuale | 236.2 | 61638 | 260.96 |
| senza | 236.2 | 70899 | 300.16 |
| simm | 236.2 | 30423 | **128.8** |

`simm` dimezza la crescita del settore di spin. **Non lo interpreto**: è il settore aliasato, un
seme, e il feedback non ci entra direttamente — l'effetto è indiretto via le fasi.

### Stabilità — nessuna variante esplode

`NaN/inf = 0` su `phivel` e `omega_s` in tutte e tre. `max|phivel|` 14.3 / 16.6 / 18.4.

---

## 4. ⚠ L'«ALTERNATIVA» DEL MANDATO È IL CODICE ATTUALE

Il mandato propone: *«accumulare `+flusso`/`−flusso` SENZA denominatore, e dividere per il grado
DOPO, sul totale del nodo — così lo scambio resta esatto e la normalizzazione agisce dove deve»*.

**È algebricamente identica alla versione attuale**, perché **`grado[k]` è lo stesso per tutti gli
archi di `k` e si raccoglie fuori dalla somma**:

```
out[k] = Σ_{archi di k} (±f / grado[k])  =  ( Σ_{archi di k} ±f ) / grado[k]
```

Verificato numericamente: **`max|ATTUALE − ALTERNATIVA| = 5.551e-17`** — zero macchina. E il
rapporto `|sum|/max|·|` è **7.119e-01 in entrambe**, contro **2.365e-16** della forma simmetrica.

> **Non è un'alternativa: è la stessa cosa riscritta.** Lo scambio *sembra* esatto perché si guarda
> la fase di accumulo, ma la normalizzazione successiva lo rompe di nuovo.
> **L'unico modo di avere `sum(out) = 0` è un denominatore SIMMETRICO SULL'ARCO — o nessuno.**

---

## 5. ⚠ E IL DIFETTO ERA **GIÀ DIMOSTRATO NEL REPO** — su un termine gemello

`doc/MAPPA_accoppiamenti_spin.md` (righe 88-96) contiene, **già committato**:

> *«**La normalizzazione.** Il contributo della coppia `(i,j)` al torque su `i` è
> `(w_ij/deg_i)·cross(nb_j, nb_i)`; quello su `j` è `(w_ij/deg_j)·cross(nb_i, nb_j)`. Sono opposti
> **solo se `deg_i == deg_j`**. Su un grafo di grado disomogeneo — cioè **questo** — **non lo
> sono.** […] **Quindi `SOMMA_i L_i` non è conservata**, e non per errore numerico: **per
> costruzione**. […] **NB ONESTO:** che non sia conservata si **dimostra** dalla formula;
> **quanto** non lo sia [non è misurato].»*

**Stesso difetto, stessa causa, su un altro termine** (`B`, `:2080-2082`, il torque di spin).
**La mia misura `|sum(out)|/max|out| = 1.112` è la prima misura di AMPIEZZA di un difetto che nel
repo era già dimostrato in forma.**

**È P1, e l'ho mancato:** avrei dovuto rileggere quel documento **prima** di trattare il difetto
come nuovo. Il presidio *«quando si apre una domanda nuova, ri-interroga le misure vecchie»* esiste
esattamente per questo.

**E la conseguenza è più grande del termine in esame.** Lo stesso schema «dividi per il grado del
nodo che riceve» compare in **almeno quattro punti**:

| punto | forma |
|---|---|
| `:1367-1368` | **`SPIN_FEEDBACK`** — divisione **dentro** l'accumulo, `grado[ii]` vs `grado[jj]` |
| `:2082` | `B = B / np.maximum(deg[:,None], 1e-9)` — divisione **dopo**, per nodo |
| `:2294` | `omega_new += _otw / np.maximum(_degt[:,None], 1.0)` |
| `:3154` | `coppia = coppia + twist_nodo / np.maximum(grado, 1.0)` |

**E per il §4 di questo referto, «dentro» e «dopo» sono la STESSA cosa.** Quindi **la domanda «il
denominatore per grado rompe l'antisimmetria» non riguarda solo `SPIN_FEEDBACK`.**
**Non l'ho misurata sugli altri tre: è un fronte nuovo, e non lo apro dentro questo mandato.**

---

## 6. DOVE VA CORRETTO IL PREGIO SMENTITO

Il mandato chiede di correggere *«ovunque sia stato affermato»* che il termine è conservativo.
**Cercato in tutto il repo: l'affermazione sta in UN posto, il docstring del metodo**
(`:1336-1341`):

> *«Trasforma l'overlap spinoriale locale in una **coppia antisimmetrica** ai nodi. […] La divisione
> per il grado pesato **resta locale e non introduce una manopola**.»*

**La seconda frase è VERA ed è la RAGIONE per cui la prima è FALSA.** Va riscritto — ed è `G9`, cioè
**parte della cura, non di questa misura**: non lo tocco adesso.

*(Nei documenti non ho trovato l'affermazione «è conservativo per costruzione, A7 soddisfatta»
riferita a `SPIN_FEEDBACK`. Se è stata fatta, è stata fatta **nei mandati**, non nel repo — e allora
la correzione è questo referto.)*

---

## 7. COSA RESTA DA DECIDERE — **la decisione è di Luca**

1. **La misura non distingue (A) da (B), e lo dico invece di scegliere** (§4 del mandato).
   **Ma §1 del mandato pre-registra cosa fare nel caso indifferente:** *«si sceglie (A) per il
   motivo più debole ma valido: è la modifica minima che ripristina l'antisimmetria»*. **A questo si
   aggiunge che (B) è esclusa per dimostrazione (§1 di questo referto).** Se accetti entrambe,
   **(A) è quello che resta** — e serve il tuo via libera, perché §5.2 dice STOP.
2. **Il denominatore simmetrico va DERIVATO, e oggi non ho una derivazione.** Il mandato indica `w`
   come candidato «già nella formula e simmetrico per costruzione». **Ma `flusso = w·imag(ov)`:
   dividere per `w` lo CANCELLA**, e resta `out[i] −= imag(ov)` — il peso dell'arco sparirebbe dalla
   legge. **Va valutato, non dato per buono.** `(g_i+g_j)/2`, `min`, `max`, `sqrt(g_i·g_j)` sono
   **quattro scelte arbitrarie (A1)**.
3. **Il fronte nuovo di §5:** lo stesso schema in `:2082`, `:2294`, `:3154`. **Non misurato.**

**`SPIN_FEEDBACK` resta OFF. Nessuna cura cablata, nessun sigillo, nessun test a semi.**
