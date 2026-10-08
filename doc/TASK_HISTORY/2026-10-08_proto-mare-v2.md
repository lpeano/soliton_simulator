# MARE `v2` — **il test PULITO dell'idea di Luca: si parte da uno stato FERMO**

> **Mandato di Luca, 2026-10-08.** ### ⛔ **Il simulatore NON si tocca *(`b8c21049`)*,
> `ASSIOMI.md` NON si tocca, e il prototipo NON importa il simulatore.**
> Il `v1` è committato in `a0892c9`: verdetto ### **NON DECIDIBILE**.

## 1. PERCHÉ IL `v1` NON DECIDEVA, E CHE COSA CAMBIA

| il difetto del `v1` | come il `v2` lo toglie |
|---|---|
| ### **lo stato uniforme NON era stazionario**: `Σ_j w_kj` varia fino a un fattore `39.8` | si parte dallo ### **stato stazionario di `H` COMPLETA a quel `g`**, trovato con Newton |
| il controllo a `g = 0` ### **non era un controllo** *(`ρ_max/media` fra `7.7` e `12.7`)* | a `g = 0` lo stato di partenza è ### **un autostato esatto**: una perturbazione piccola ### **non può crescere**, e il controllo diventa pulito |
| il caso `ε = 0` dava ### **gli stessi grumi** del caso disturbato | i grumi si definiscono ### **RISPETTO allo stato di partenza** *(`ρ_k(t)/ρ_k(0) > 3`)*, non rispetto alla media |
| l'orologio era ### **aliasato** | `dφ/dt` si calcola ### **dalla legge**, non da una differenza fra campioni |
| il tetto era ### **mal posto** *(il blocco `ε = 0` fuori dal controllo)* | il controllo sta attorno a ### **TUTTE** le corse |

## 2. LO STATO DI PARTENZA — **e la stima del tempo, PRIMA di girare**

### **L'EQUAZIONE STAZIONARIA.** Con `U = I` e una sola componente, `ψ` reale positiva:

```
-(W psi)_k  +  g psi_k^3  -  mu psi_k  =  0        con il vincolo   somma_k psi_k^2 = n
```

`W` è l'adiacenza pesata. ### **`n + 1` incognite `(psi, mu)` e `n + 1` equazioni**, e Newton
sul sistema aumentato. ### **La jacobiana:** `-W + diag(3 g psi^2 - mu)`, la colonna di `mu` è
`-psi`, la riga del vincolo è `2 psi^T`.

### **LA CONTINUAZIONE.** Si parte dall'### **autovettore di Perron** della parte lineare a
`g = 0` *(il più basso di `-W` è il più alto di `W`, e per Perron-Frobenius è ### **positivo**:
è il ramo ESTESO)* e si scende in `g` a passi di `Δg = -0.25`, ripartendo ogni volta dalla
soluzione precedente. ### ⛔ **Se Newton non converge, il ramo esteso FINISCE, e il `g` in cui
finisce è UN RISULTATO** *(auto-intrappolamento: lo stato più basso diventa localizzato da
solo)*.

### ✔ **E IL RESIDUO SI VERIFICA** *(`< 1e-12`)*, invece di fidarsi di Newton.

### 📌 **LA STIMA DEL TEMPO, dalle corse del `v1`** *(mediane del braccio `U-UNO`)*:

| | |
|---|--:|
| `g = 0` · `g = -5` · `g = -10` | `22.8` · `40.7` · `44.5` s |
| per seme e braccio | `108.0` s |
| le `18` corse *(`3 g × 3 semi × 2 bracci`)* | `648.0` s |
| le `6` corse a `ε = 0` *(`g = -10`)* | `267.0` s |
| ### **STIMA TOTALE** | ### **`915.0` s = `15.25` minuti** |
| il tetto | `20` minuti |

### ➜ **STA SOTTO, quindi `g = -10` RESTA.** ### ⚠ **E il controllo dei `20` minuti sta
attorno a TUTTE le corse, comprese quelle a `ε = 0`** — nel `v1` era fuori, e per quello non
prese il superamento.

## 3. I DUE BRACCI D'INTERFERENZA — **misura, NON decisione**

| braccio | l'hopping |
|---|---|
| ### **`NON-NORM`** | `w_ij` come oggi: ### **il grado conta come energia** |
| ### **`NORM`** | `w_ij / sqrt(s_i · s_j)` con `s_k = Σ_j w_kj` — ### **hermitiano** per costruzione |

### ⛔ **E QUESTA NORMALIZZAZIONE TOCCA `A3`, e lo dichiaro con la precisione che serve.**
`A3` dice: *«non si normalizza una grandezza su una ### **statistica di POSIZIONE** del proprio
insieme (mediana, media dei primi vicini): il centro diventa `1` per identità»*.

| | |
|---|---|
| ### **che cosa tocca** | `s_k` è una grandezza ### **del proprio intorno**: lo spirito di `A3` c'è ### **tutto** — il vicinato del nodo diventa il metro |
| ### ⚠ **che cosa NON è** | `s_k` è una ### **SOMMA**, non una mediana né una media: ### **il meccanismo che `A3` nomina — «il centro diventa `1` per identità» — NON scatta.** ### **MISURATO:** dopo la normalizzazione `s̃_k` ha media `0.98` e deviazione relativa ancora ### **`12 %`** *(contro il `38 %` di prima)*, e `max/min` passa da `39.8` a ### **`3.7`** |
| ### **perché la si prova** | ### **per sapere CHE COSA CAMBIA**, non per adottarla. ### ⛔ **La scelta fra le due forme è una DECISIONE DI LUCA**, e va nell'elenco delle decisioni della traduzione in `H` |

## 4. L'OROLOGIO SENZA ALIASING — **dalla legge, non da una differenza fra campioni**

Da `i dψ/dt = F` con `ψ = R e^{iφ/2}` *(la convenzione di `A16.1`)*:

```
psi* dpsi/dt = R dR/dt + i (R^2/2) dphi/dt        e        psi* dpsi/dt = -i psi* F
=> Im(-i psi* F) = -Re(psi* F) = (R^2/2) dphi/dt
=> dphi/dt = -2 Re(psi* F) / |psi|^2
```

### ✔ **Il `2` viene dalla convenzione `φ/2`**, ed è ### **esattamente** la formula del
mandato. ### ⛔ **E NON LA DO PER BUONA: il collaudo `(b)` la confronta con una differenza
finita a passo FINE.**

## 5. IL COLLAUDO, PRIMA DELLE CORSE

| | che cosa deve venire |
|---|---|
| ### **(a)** | lo stato stazionario ### **senza disturbo resta FERMO** a ogni `g`: deriva della densità ### **`< 1e-8`** sul tempo della corsa, in ### **entrambi** i bracci |
| ### **(b)** | la formula dell'orologio ### **coincide** con la differenza finita a passo fine |
| ### **(c)** | norma ed energia conservate come nel `v1` |
| ### ⛔ **(d)** | ### **il caso che DEVE fallire:** a `ε = 0` ### **nessun grumo nuovo** a ogni `g` — `max_k ρ_k(t)/ρ_k(0) < 1 + 1e-6` |

## 6. I CRITERI, FISSATI ADESSO *(quelli di Luca, per braccio)*

| | il criterio |
|---|---|
| ### **`LE MASSE NASCONO DALL'INTERFERENZA`** | se per ### **almeno un `g < 0`**, in ### **tutti e `3`** i semi nascono grumi che durano ### **oltre `10 t_c`**, ### **MENTRE** a `g = 0` ### **non ne nasce nessuno** e il caso `(d)` ### **passa** |
| ### **`NON NASCONO`** | se ### **nessun `g < 0`** produce grumi duraturi a partire dallo stato fermo |
| ### **`LO STATO PIÙ BASSO È GIÀ UNA MASSA`** | se il ramo esteso ### **finisce** prima di `g = -10`: esito ### **a sé**, col `g` in cui finisce |

### **IN PIÙ:** quanti grumi, la loro ### **norma** e la loro ### **energia**, ### **dove**
nascono rispetto allo stato di partenza *(nelle zone già dense o ovunque)*, e l'### **orologio
contro l'energia** locale per unità di norma.

## 7. LE PREVISIONI, PRIMA DI VEDERE I NUMERI

| id | la previsione |
|---|---|
| **`PV-1`** | la continuazione ### **arriva a `g = -10`** in entrambi i bracci, con residuo `< 1e-12`: ### **il ramo esteso NON finisce**, ma lo stato ### **si localizza** — il `PR` cala e `max/media` cresce al crescere di `\|g\|` |
| **`PV-2`** | l'### **autovettore di Perron** concentra già da solo: `max/media` ### **oltre `2`** a `g = 0`, e il `PR` ### **ben sotto** `400` |
| **`PV-3`** | la formula dell'orologio coincide con la differenza finita a passo fine ### **entro `1e-6`** relativo |
| **`PV-4`** | `(a)` passa: lo stato fermo ### **resta fermo**, deriva `< 1e-10` *(meglio della soglia)* |
| **`PV-5`** | `(d)` passa: a `ε = 0` ### **nessun grumo nuovo** a nessun `g`. ### ⛔ **Se fallisce, il difetto è nel mio stato stazionario, non nella fisica** |
| **`PV-6`** | ### ⭐ **`LE MASSE NASCONO DALL'INTERFERENZA` è soddisfatto in almeno un braccio:** a `g = 0` lo stato è un ### **autostato esatto** e una perturbazione piccola ### **non può crescere** *(spettro reale)*, mentre a `g < 0` l'### **instabilità modulazionale** amplifica. ### **È la prima volta che il controllo è pulito** |
| **`PV-7`** | i grumi nascono in ### **ENTRAMBI** i bracci, ma in `NORM` servirà ### **più `\|g\|`**, perché il campo di sito è più piatto e aiuta meno |
| **`PV-8`** | i grumi nascono ### **dove lo stato di partenza è GIÀ DENSO**, perché il tasso di crescita va come `\|g\|·ρ`. ### **Scritta per poter PERDERE: se nascono ovunque, l'instabilità non segue la densità** |

### **COSA MI FAREBBE FERMARE:** il residuo di Newton ### **sopra `1e-12`**; `(a)` o `(b)` che
non chiudono; `(d)` che ### **produce grumi** *(sarebbe un difetto del mio stato stazionario)*;
la stima del tempo ### **oltre i `20` minuti** *(è `15.25`, e il controllo è attorno a tutte le
corse)*.

## 8. LA STELLA POLARE — *le cinque risposte*

| | la risposta |
|---|---|
| **1 `A14`** | conserva ### **per costruzione** *(una `H`, un integratore unitario)*, e il collaudo `(c)` lo misura. ### ⭐ **E il `v2` aggiunge una cosa: lo stato di partenza è un AUTOSTATO, quindi anche la DENSITÀ è conservata — e `(a)` la misura** |
| **2 i tre gradini** | ### **(a) robusto al rumore** e ### **(c) coincide con un limite noto** *(a `g = 0` l'autostato di Perron è esatto, e il collaudo lo verifica)*. ### ⛔ **Il (b) non è raggiunto:** `3` semi, `P3` non soddisfatta |
| **3 numeri o leggi** | ### **nessun numero nuovo di fisica.** `Δg = -0.25` *(il passo della continuazione)*, le tolleranze di Newton e la soglia `3` dei grumi sono ### **numeri di banco**, dichiarati. ### ⛔ **E il braccio `NORM` AGGIUNGE UNA FORMA, non un numero: tocca `A3`, è dichiarato, e la scelta è di Luca** |
| **4 `rho`, `c_s`, il SEGNO** | ### **nessuno:** nel prototipo non c'è metrica |
| **5 emergente o imposto** | ### ⭐ **È LA DOMANDA, e per la prima volta il controllo è PULITO:** si parte da uno stato ### **fermo dell'equazione completa**, quindi ogni grumo che nasce viene ### **dall'amplificazione del disturbo** — non dal grafo, non dall'assestamento |

### ⚠ **E CHE COSA I GRUMI NON SONO ANCORA, dichiarato prima:** ### **masse nel senso del
bersaglio.** Che si ### **attraggano**, con che ### **legge**, e se ### **cadano tutti allo
stesso modo** sono le ### **tre prove** di `doc/IPOTESI_gravita_a_spinta.md`, e
### **restano FUORI.**

## 9. L'ANNOTAZIONE — **LA PREMESSA DEL MANDATO NON STA IN PIEDI, E IL CONTO LO DICE**

*(Scritta dopo, come vuole il par.8: ### **sopra non si riscrive niente.** I numeri:
`proto_primo_ordine/diagnosi_v2.py` → `doc/REFERTO_proto_mare_v2_2026-10-08.md`.)*

### ⛔ **Il mandato chiede «lo stato stazionario di `H` completa sul ramo ESTESO, con densità
media `ρ_0 = 1`». Quello stato ESISTE, ma NON è lo stato più basso: è una SELLA.**

| | |
|---|---|
| il conto | a norma fissa `Σψ² = N`, ### **un solo nodo** dà `H = (g/2)N²` *(va come `N²`)*, l'esteso `H ≈ −λN + (g/2)N²/n_eff` *(va come `N`)* |
| ### ➜ | per ### **ogni** `g < 0` vince un nodo: a `g = -5`, ### **`-400000` contro `-18534`** *(`NON-NORM`)* e ### **`-1549`** *(`NORM`)* |
| la misura | la continuazione collassa a ### **`PR = 1.00`** già al ### **primo** passo sotto `g = 0`, in ### **entrambi** i bracci e per ### **entrambi** i `Δg` |
| ### ⛔ **e nessun `ρ_0` salva** | sotto la soglia il mare resta il più basso, ma lì `\|g\|ρ_0` vale ### **`0.029`** e ### **`0.005`** contro `λ_max` `5.65` e `1.00`: ### **la non linearità SPARISCE** |

| previsione | esito |
|---|---|
| **`PV-1`** | ### ⛔ **SMENTITA.** Dicevo *«il ramo esteso NON finisce, ma si localizza»*: finisce ### **subito**, e la discesa ne cade fuori al primo passo |
| **`PV-2`** | ### **MEZZA, e la metà che vale è misurata.** `NON-NORM`: `max/media` ### **29.38** e `PR` ### **24.6** su `400` — ### **confermata in pieno**. `NORM`: `max/media` `2.25` *(appena sopra il `2` che avevo scritto)* e `PR` ### **348**, cioè ### **NON «ben sotto 400»** |
| **`PV-3`..`PV-8`** | ### **NON VALUTATE:** l'esperimento ha bisogno di uno stato di partenza ### **fermo ed esteso**, e quello ### **non c'è**. ### **Non le converto in verdetti** |

### ⚠ **E IL DIFETTO CHE HO PRESO NEL REFERTO STESSO, prima di committarlo:** la riga *«dopo la
normalizzazione»* ripeteva il `s_k` ### **di prima**, perché `pesi_v2` restituisce sempre quello;
era un ### **FALSO-UNO**. Ricalcolato dai pesi veri: `0.3856 → ` ### **`0.1160`** e
`16.66 → ` ### **`2.82`** — coerente col `0.12` e `3.7` che avevo misurato ### **prima** della
corsa, nel §3.

### ⛔ **CHE COSA NON DECIDO:** la forma di `H`. Le strade che il conto lascia aperte — un termine
che ### **penalizza** la concentrazione, oppure il ramo esteso studiato ### **come sella**
*(dichiarando che si misura un decadimento)*, oppure `g > 0` — sono ### **DECISIONI DI LUCA**, e
sono ### **più a monte** della scelta `NON-NORM`/`NORM` su cui il mandato mi chiedeva di fermarmi.
