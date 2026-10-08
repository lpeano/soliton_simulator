# REGISTRO DELLA FISICA — **un documento unico, su tutto il modello, passato e futuro**

> **Mandato di Luca, 2026-09-22.** Il registro dei difetti dice *«questo era rotto»*; **questo
> documento dice «questa è la legge»**, e le due cose non si sostituiscono.
>
> **⚠ IL VINCOLO CHE GOVERNA IL `CHK3`:** **le cure non partono finché la scheda della componente
> da curare non esiste.** Una cura deve **nascere dalla scheda** — dalla formula, dalle dimensioni,
> da cosa legge e cosa scrive, dai limiti classificati con `A11`. **Se la scheda non c'è, si cura
> di nuovo alla cieca**, ed è il modo in cui sono nati `D01`–`D33`.

## COSA CONTIENE UNA SCHEDA, e perché ciascuna voce

| voce | perché c'è |
|---|---|
| **LA FORMA** | la formula **copiata dal codice che gira**, non dal commento *(par.0)* |
| **DA DOVE VIENE** | derivazione o origine. **Se non si ricostruisce, si scrive `NON RICOSTRUITO`** |
| **LE DIMENSIONI** | `A3c`: due grandezze si confrontano solo se sono **confrontabili** |
| **COSA LEGGE / COSA SCRIVE** | i siti dell'inventario *(`REG-A`)*, col nome di traccia |
| **I LIMITI, classificati con `A11`** | ogni `clip`, pavimento o tetto, **col corollario che rispetta o viola** |
| **LO STATO** | `SANA` · `DA VERIFICARE` · **`DIFETTOSA`** *(col numero del difetto)* |
| **LE DOMANDE APERTE** | **domande, non scelte.** Una scheda non decide: prepara la decisione |
| **L'EPOCA DI OGNI NUMERO** | `par.9-bis`: un numero dell'epoca 1 non è una premessa per l'epoca 3 |

**REG-R, la regola mantenuta** *(da cablare quando le schede coprono le leggi attive)*: **nessuna
legge fisica entra, cambia o esce dal simulatore senza passare da questo documento**, con un hook
che rifiuta un commit a `soliton_simulator.py` che non tocchi il registro, salvo
`[SENZA-FISICA: <motivo>]`.
**✅ CABLATA il 2026-09-22 — e nella forma che la rende un presidio invece di una formalità.**
`csv/_hook_fisica.py`, dentro il `commit-msg` già esistente *(un hook solo: due che se lo contendono è il modo in cui un presidio sparisce in silenzio)*. **Non chiede di «toccare il registro»** — lo soddisferebbe una riga qualsiasi in fondo al file. **Chiede che la modifica cada DENTRO la sezione della legge toccata**, e se quella legge **non ha una scheda**, dice *«prima si crea la scheda»*.

> ### ⚠ **UN INDEBOLIMENTO DI `REG-R`, dichiarato il 2026-09-24**
>
> **`_applica_flag` e `_cli` NON sono leggi**: sono il cablaggio dei flag. Ma è **lì** che un
> flag viene collegato alla sua legge, quindi `REG-R` li vede cambiare e chiede una scheda.
> **Li ho aggiunti alle `funzioni=` delle due schede che governano i flag cablati in quel
> commit** — `tempo-proprio` per `RITMO_WRAP_2PI`, `torsione-spinore` per `TW_SPINORE` —
> perché è vero che la cura *sta* lì.
>
> **L'INDEBOLIMENTO: da ora un commit che tocca `_applica_flag` per un flag QUALUNQUE
> soddisfa `REG-R` toccando una di queste due schede.** È meno stretto di prima, e va detto
> invece di scoprirlo dopo. **Non l'ho risolto**: la via pulita sarebbe che `REG-R` mappasse
> il flag, non la funzione, e quella è una modifica al presidio che **non decido da solo**.

**COME SA QUALE SCHEDA:** ogni scheda porta un marcatore leggibile da codice — `<!-- SCHEDA nome=… funzioni=… flag=… -->` — e la sezione va da un marcatore al successivo.
**COME SA COSA È CAMBIATO:** dalla diff in cache di `soliton_simulator.py`, le righe toccate risalgono alla **funzione** che le contiene *(per NOME, via AST della versione in cache — par.0)* o al **flag** di modulo assegnato su quella riga.

**⚠ IL LIMITE, dichiarato invece che nascosto:** **non distingue una modifica di LEGGE da una di COMMENTO.** Distinguerle richiederebbe un confronto di AST fra le due versioni, e **un commento che descrive una legge è parte della legge** *(i commenti stale sono un difetto documentato di questo repo)*. **Quindi è più severo del necessario**, e le modifiche davvero non fisiche passano per `[SENZA-FISICA: <motivo>]`.

## ⛔ **LA DECISIONE DEL 2026-10-08: `A16`, E LA RISCRITTURA AL PRIMO ORDINE**

> ### **Decisione di Luca.** L'assioma sta in `doc/ASSIOMI.md` *(`A16`, in testa)*, il piano in
> **`doc/RISCRITTURA_PRIMO_ORDINE.md`**, il banco in `proto_primo_ordine/`.
> ### ⛔ **E IL SIMULATORE NON È TOCCATO: resta `b8c21049`.**

### **CHE COSA CAMBIA NELLA FISICA DEL MODELLO.** `A16` fissa che ### **lo stato di nodo è uno
solo** *(`ψ_k ∈ C²`, e `φ` si LEGGE da `ψ`)* e che ### **ogni legge che fa evolvere uno stato è
del primo ordine e deriva dalla stessa `H`** *(`i·dψ/dt = ∂H/∂ψ*`)*. ### ➜ **Non è una legge
nuova: è un VINCOLO SULLA FORMA di tutte le leggi**, come gli altri assiomi.

### ⛔ **E NASCE GIÀ VIOLATO, dal cuore del simulatore di oggi**, con i numeri misurati:

| che cosa viola `A16` | il numero |
|---|---|
| `phivel` con l'inerzia `M_PH` — ### **secondo ordine** *(`:7760`, `:7830`)* | — *(è la forma stessa della legge)* |
| la coppia come ### **forza che non deriva da `H`** | il collaudo di `D3` dà scarto ### **`1.054`** contro la forma `U(2)`; il collaudo del gradiente dà ### **`1.18e-01`** per una coppia non di gradiente contro `2.55e-06` per una che lo è |
| ### **DUE orologi** per nodo: `φ/2` e la fase comune `α` dello spinore | ### **`rms(wrap(α − φ/2)) = 1.9716`** radianti *(mediana `1.7377`)* |
| il termostato sulle ### **velocità** | nella decomposizione di `dT` vale `+394.5614` contro `+8804.8634` della coppia |
| la sincronizzazione che sposta `φ` ### **fuori** dalla dinamica *(`:7805`)* | toglierla costa il ### **`93.44 %`** della crescita di `H` a `A` fissa, e ### **non costa coerenza** *(`AUC` al `400` da `0.9394` a `0.9333`)* |
| lo scuotimento come ### **calcio additivo** | ### **non fa lavoro: inietta varianza** — quota quadratica `99.45 %` nel vuoto, `99.42 %` nelle masse |

### ⭐ **IL FATTO CHE HA DECISO:** ciò che tiene le masse coerenti è ### **la forma della
coppia** *(un gradiente di un'energia che legge la fase che muove)*; ciò che pompa energia sono
### **i forzanti e la sincronizzazione**, che ### **non ordinano**. ### ➜ **Quindi non manca una
legge in più: ne mancano di MENO, e scritte da una sola `H`** — ed è esattamente `9-ter`
*(«una cura non aumenta il numero delle leggi»)* portato alla sua conclusione.

### **LE VOCI CHE `A16` RENDE DA RILEGGERE, e che NON si chiudono qui** *(si chiudono con
misure, e il collegamento è nella colonna `nota` dell'indice)*:
`SPINORE-SENZA-FASE` · `ENERGIA-NON-DEFINITA` · `CENS-A1` · `PHI0-CONGELATA` · `M-LEGAMI` ·
`FRECCE-IMPOSTE`, più ### **le memorie provvisorie** *(`A15.1`: nessuna memoria congelata; e nel
prototipo `w` e `U` sono ### **fissi**, dichiarato come violazione provvisoria di `A16.3`)*.

### ⚠ **E COSA QUESTA SCHEDA NON DICE:** non fissa la ### **forma di `H`** *(il termine non
lineare, le matrici d'arco, i pesi: `A16` dice che si decidono ### **con misure**)*; non dice
che il prototipo sostituisca il simulatore *(è un ### **banco**, fuori e senza importarlo)*; e
non dice che la simulazione sia meccanica quantistica — su un grafo di migliaia di nodi è
### **un campo con la FORMA della dinamica quantistica**, non uno stato a molti corpi.

---

## COSA C'È DA COPRIRE — **dalla `FASE A`, misurato, non stimato**

**`164` scritture di stato su `27` grandezze, di cui `65` CONCATENAZIONI**, più `313` scritture su
attributi **non dichiarati fisici** *(`csv/_seal_fork/_inventario_scrittori.py`, blob `2c70e4ad`,
voce `Z…` della `FASE A`, commit `9a82bfb`)*.
**Ogni scrittore dei 164 deve finire in una scheda.**

**L'ORDINE, fissato da Luca il 2026-09-22 e rivisto dopo `Z109`:**
① **il freno di `SCALA_MIN`** · ② **la memoria del moto** · ③ **la gravità bifase** ·
④ **la coesione** · poi mitosi, Schwinger, rilassamento di `peq`; poi le altre attive, poi le
**dormienti**.

---

<!-- SCHEDA nome=freno-della-coesione funzioni=massa_critica_adattiva,massa_critica_collasso flag=K_C,COES_ADIM,COES_CAUSALE,LAM -->

## ⭐ **LA DECISIONE DEL 2026-10-08 `(C)`: IL FRENO DELLA COESIONE E' LA `(c)` — ENTRAMBI**

> ### **Decisione di Luca, PRESA.** L'elenco di `doc/TRADUZIONE_IN_H.md` dava tre alternative
> *(`(a)` un termine che satura dentro `H`; `(b)` la nascita dello spazio; `(c)` entrambi)*:
> ### **e' la `(c)`.**
> ### ⛔ **E NEL SIMULATORE ATTUALE NON SI TOCCA NIENTE: resta `b8c21049`.**

| il freno | che cos'e' | la portata |
|---|---|---|
| ### **FRENO VERO** | la ### **NASCITA DELLO SPAZIO**, pagata dal ### **calore** *(decisione `(A)`)* | ### **alleggerisce** la materia, e si ferma quando il calore finisce *(livello `4`, `16` nodi)* |
| ### **FRENO A CORTO RAGGIO** | la ### **PRESSIONE DI DEGENERAZIONE** — parole di Luca: *«la pressione di degenerazione, ### **che in natura esiste**»* | ### **tiene SEMPRE**, anche quando il calore e' finito |

### ⭐ **PERCHE' SERVONO ENTRAMBI, ed e' un argomento di coerenza, non di gusto.** Se il freno
fosse ### **solo** «capacita' + nascite», quando il calore si esaurisce — e si esaurisce, al
livello ### **`4`** — ### **le nascite si fermano e NON RESTA NESSUN FRENO.** Con la barriera
dentro `H`:

| | |
|---|---|
| la ### **degenerazione** | ### **tiene SEMPRE** |
| la ### **nascita** | ### **ALLEGGERISCE quando il calore la paga** |
| se il calore ### **non basta** | la materia ### **resta compressa al limite SENZA COLLASSARE** |

### **DA DOVE EMERGE LA DEGENERAZIONE — due regole RELAZIONALI, e nessun volume** *(`A17`)*:

| | la regola | perche' e' relazionale |
|---|---|---|
| ### **`1`** | la ### **CAPACITA' DEL NODO**: `ψ_k ∈ C²` ha ### **due componenti**, quindi ### **al piu' DUE STATI per nodo** *(immagine di Pauli; lo spin `½` viene dalla ### **doppia copertura** a `4π`)* | e' una proprieta' ### **dello stato**, non dello spazio |
| ### **`2`** | la ### **LUNGHEZZA MINIMA SUGLI ARCHI**: `d_ij ≥ LAM` *(`A13`)*, o `2·LAM` in certi casi — ### ⛔ **sulla `d` RELAZIONALE, MAI su `\|pos_i − pos_j\|`** | `d` e' una ### **relazione d'arco** |

### ⛔ **E NIENTE VOLUME, NIENTE DIMENSIONE** *(`A17` punto `3`)*: ### **niente `2/LAM³`, niente
`ρ^(5/3)`.** La forma di Chandrasekhar presuppone ### **uno spazio di dimensione `3`**, che qui
### **non c'e'**.

### ⚠ **UNA CAUTELA DICHIARATA, e non la nascondo:** ### **Pauli NON emerge da solo in un campo
come questo.** La ### **doppia copertura** e' ### **necessaria ma NON sufficiente** per la
statistica di Fermi. ### ➜ **La barriera e' derivata dalla STRUTTURA** *(due componenti, `LAM`)*,
### **NON dalla statistica** — e chiamarla «Pauli» e' un'### **analogia**, non una derivazione.

### ⛔ **IL PUNTO APERTO, da NON inventare:** «due stati» richiede ### **l'UNITA' DI STATO**,
cioe' ### **quanta `ρ` vale UNO stato.** Le candidate stanno in `doc/TRADUZIONE_IN_H.md`
*(`⑧`)*, tutte relazionali, ### **e la decisione e' di Luca.**

### ⛔ **IL CRITERIO CHE LA RIAPRE:** se, scritta la barriera, ### **il collasso su un nodo
resta lo stato piu' basso** *(cioe' la barriera non cambia il minimo)*, la `(c)` ### **non ha
ottenuto il suo scopo** e si riapre.

### 📌 **E UNA DIPENDENZA, dichiarata:** la degenerazione ### **richiede la geometria DINAMICA
dentro `H`** — cioe' la decisione `9 (a)` — perche' `d_ij ≥ LAM` come ### **barriera d'energia**
ha senso solo se `d` ha una dinamica che ### **sente** quella barriera.

---

<!-- SCHEDA nome=chi-paga-la-nascita funzioni=mitosi,decidi_divisione,massa_critica_adattiva,massa_critica_collasso flag=COPPIA_MIT,MITOSI_2LAM,TEMPO_UNICO_MITOSI -->

## ⭐ **LA DECISIONE DEL 2026-10-08 `(A)`: CHI PAGA LA NASCITA E' IL CALORE SUL VUOTO LOCALE**

> ### **Decisione di Luca, PRESA.** *(Era ### **candidata** in `b6cba2f`; oggi e' ### **presa**.)*
> ### ⛔ **E NEL SIMULATORE ATTUALE NON SI TOCCA NIENTE: resta `b8c21049`.**

> ### **LE PAROLE DI LUCA:** *«chi paga la nascita e' ### **il calore che si scarica sul vuoto
> locale**»*.

### **IL BILANCIO, CON I NUMERI** *(`N = 400`, `g = -5`, braccio `NON-NORM`, seme `11`; dal
`csv/_test_fork/_bilancio_nascita`)*:

| | |
|---|--:|
| la ### **CONCENTRAZIONE libera**: `H`(mare esteso) → `H`(un nodo) | `-18533.8` → `-400000.0` |
| energia liberata | ### **`381466.2`** |
| in una dinamica conservativa diventa ### **CALORE NEL VUOTO LOCALE** *(`A15.3`)* | — |
| la ### **NASCITA costa** *(la prima divisione)* | ### **`+199600.0`** |
| e lo ### **PRELEVA da lì** | il ### **`52.32 %`** della liberata |

### ⭐ **E LA CASCATA SI FERMA DA SOLA.** Il costo va come `N²`, quindi ogni livello costa
### **un quarto** del precedente: il calore si esaurisce al livello ### **`4`**, cioe' a
### **`16` nodi**. ### **La scala d'arresto ESCE DAL BILANCIO: non e' una manopola** *(`A1`)*.

### ⭐ **E LA SOGLIA DIVENTA IL BILANCIO STESSO** — non un numero *(`A1`)*: un nodo si divide
### **quando il calore disponibile nel suo vuoto locale ≥ `ΔH` della divisione**.
### ➜ **Sostituisce `massa_critica_adattiva` e `massa_critica_collasso` coi suoi `21` usi dentro
le leggi, cioe' CHIUDE la voce bloccante `U1`.**

### ⛔ **CHE COSA RESTA APERTO, e va scritto come APERTO:**

| | che cosa manca | ### **e deve essere RELAZIONALE** *(`A17`)* |
|---|---|---|
| ### **`(i)`** | che cos'e' il ### **vuoto locale come grandezza CONTABILE** | candidato: le ### **oscillazioni irradiate**, cioe' `H` ristretta all'intorno ### **meno** il profilo stazionario lì. ### ⛔ **La sottrazione NON e' scritta**, e ### **«intorno» va definito sul GRAFO, non nel disegno** |
| ### **`(ii)`** | la sua ### **ESTENSIONE** | i ### **vicini diretti** *(relazionale per costruzione)*, oppure una ### **scala legata alla massa** — candidata la lunghezza di guarigione `ξ = 1/√(\|g\|ρ)`, ### **derivata** *(`A1`)*. ### ⚠ **Ma `ξ` e' una LUNGHEZZA: in forma relazionale va espressa in NUMERO DI ARCHI, non in distanza** |

### ⚠ **E LA COSA CHE IL BILANCIO DICE E CHE LA FRASE NON DICEVA: IL MARGINE E' ZERO PER
COSTRUZIONE.** In una dinamica conservativa, disfare il collasso costa ### **esattamente** cio'
che il collasso ha liberato. ### ✔ **La forza: nessun bagno esterno.** ### ⛔ **Il limite: il
conto che torna NON prova che il processo avvenga — prova che NON E' VIETATO.** E i due termini
`N²` ### **si cancellano** *(la serie fa `400000.0`, il liberato `381466.2`, la differenza
### **`18533.8`** e' esattamente l'### **hopping**)*: ### ➜ **decidono i termini
SOTTODOMINANTI.**

### ⛔ **IL CRITERIO CHE LA RIAPRE:**

> **Se, scritto il vuoto locale, il calore ### NON resta disponibile vicino alla massa** — si
> ### **disperde prima di poter pagare** — ### **la decisione si riapre.**

### 📌 **E IL LEGAME CON LE ALTRE DUE:** lo ### **stesso** calore serve all'### **aggancio degli
orologi** *(decisione `(B)`, `sincronizzazione-si-toglie`)* e alimenta il ### **freno vero**
della decisione `(C)` *(`freno-della-coesione`)*. ### ⚠ **Un serbatoio, TRE usi.**

---

<!-- SCHEDA nome=sincronizzazione-si-toglie funzioni= flag=K_SYNC,SYNC_SPINORE,SYNC_FASE_OROLOGIO,KURAMOTO_SU2 -->

## ⛔ **LA DECISIONE DEL 2026-10-08: SI TOGLIE LA SINCRONIZZAZIONE, PERCHE' EMERGERA'**

> ### **Decisione di Luca, PRESA** *(non una proposta)*.
> ### ⛔ **E NEL SIMULATORE ATTUALE NON SI TOCCA NIENTE: resta `b8c21049`.** La rimozione di
> `K_SYNC` avviene ### **nella riscrittura**, sotto il flag del primo ordine.
>
> ### 📌 **E IL RIMANDO ALLE ALTRE DUE DECISIONI DEL 2026-10-08** *(aggiunto, la scheda
> ### **non si riscrive**)*: l'aggancio degli orologi si paga cedendo l'eccesso al
> ### **vuoto locale**, che e' ### **LO STESSO CALORE** con cui la decisione `(A)`
> *(`chi-paga-la-nascita`)* paga la ### **nascita dello spazio** e con cui la `(C)`
> *(`freno-della-coesione`)* alimenta il ### **freno vero**. ### ⚠ **Un serbatoio, TRE usi — e
> se manca a uno, manca agli altri.**

### **LA LEGGE CHE SI TOGLIE.** `delta_sync_phi = dt_n_s · forza · sin(media − φ)` con
`media = angle(Σ_j w_kj e^{iφ_j})` e `forza = (2/π)·prof_rel·rinforzo_shear` — un Kuramoto
locale che ### **sposta `φ` fuori dalla dinamica**.

### **I TRE MOTIVI, CON I NUMERI:**

| | il motivo | il numero |
|---|---|--:|
| **`(i)`** | ### **nessuna `E(φ)` esiste** di cui `K_SYNC` sia il gradiente | asimmetria della jacobiana ### **`1.0641`** contro un pavimento ### **calcolato** di `1.438e-10` — ### **nove ordini sopra**, e identica ai tre passi `h` |
| **`(ii)`** | ### **anche un Kuramoto SIMMETRICO e' un flusso di gradiente**, cioe' ### **dissipativo**: e' la forma che `A16.3` ### **non ammette come legge** | `φ̇ = −∂E/∂φ` ⇒ `dE/dt = −\|∂E/∂φ\|² ≤ 0` |
| **`(iii)`** | ### **toglierla NON costa coerenza**, e toglie il pompaggio | `AUC` al `400`: `0.9394` → ### **`0.9333`**; e toglie il ### **`93.44 %`** della crescita di `H` a `A` fissa |

### ⭐ **E UNA DISTINZIONE CHE IL `(ii)` RENDE NECESSARIA, perche' senza di essa sembra una
contraddizione.** La ### **stessa** energia `E = −K_C Σ A_ij cos(φ_i − φ_j)` da' ### **due
leggi diverse**, e ### **una conserva e l'altra dissipa**:

```
Kuramoto  (gradiente):   phi'_i = -dE/dphi_i                  ->  dE/dt <= 0   DISSIPA
primo ordine (A16):      i dpsi/dt = dH/dpsi*                 ->  dH/dt  = 0   CONSERVA
                         cioe'  phi'_k = +dH/drho_k ,  rho'_k = -dH/dphi_k
```

### ➜ **Non conta QUALE energia: conta A QUALE EQUAZIONE la si dia.** La coppia scalare e il
Kuramoto nascono dalla ### **stessa** `E`; la prima e' hamiltoniana perche' `φ` e `ρ` sono
### **coniugati**, il secondo e' una discesa. ### ⛔ **Per questo «scrivere la `E` della
sincronizzazione» non l'avrebbe salvata: l'avrebbe resa un Kuramoto simmetrico, che dissipa
comunque.**

### ⭐ **PERCHE' DEVE EMERGERE, e non e' una speranza.** Al primo ordine uno stato stazionario
ha ### **la stessa frequenza su tutti i nodi**:

```
psi_k(t) = psi_k(0) e^{-i mu t}     =>     dphi_k/dt = mu    PER OGNI k
```

### ➜ **L'aggancio degli orologi NON e' una legge da aggiungere: e' una PROPRIETA' dello stato
stazionario.** E il sistema ci arriva ### **cedendo l'energia in eccesso al vuoto locale**
*(`A15.3`)* — ### **lo stesso calore che paga la nascita dello spazio** *(la proposta di Luca
del `2026-10-08`, `doc/TRADUZIONE_IN_H.md` `⑥.2`)*.

### ⛔ **IL CRITERIO DA MISURARE, NON DA ASSUMERE** *(e la decisione si RIAPRE se non passa)*:

> **Quando il vuoto locale sara' scritto, si misura se gli orologi di una massa si agganciano
> ### SENZA nessuna legge di sincronizzazione:** la ### **dispersione di `dφ/dt` dentro la
> massa** deve ### **calare nel tempo**, con il ### **calore ceduto al vuoto CONTABILIZZATO**.
> ### ⛔ **Se non succede, la decisione si riapre.**

### ⚠ **E COSA QUESTA SCHEDA NON DICE:** non dice che l'aggancio ### **avvenga** — dice che
### **al primo ordine e' una proprieta' dello stato stazionario**, e che ### **se il sistema
raggiunga quello stato e' DA MISURARE.** Non tocca il simulatore di oggi: ### **`K_SYNC` resta
`1.0` in `b8c21049`**, e il flag non si muove.

---

<!-- SCHEDA nome=freno-scala-min funzioni=_smorza,_smp_apri,_smp_chiudi,_smp_snap,_sd0,_nasce flag=SCALA_MIN,SCALA_MIN_PASSO,PAV_COM -->
# ① IL FRENO DI `SCALA_MIN` — **`SCALA_MIN_PASSO` / `_smorza` / `_smp_chiudi`**

## ⭐ **E DAL `COMMIT 6a` `_nasce` SA SOMMARE PER META': `meta=`**

*(decisione di Luca del 2026-10-03, e il motivo e' che ### **un contatore e' un FLOAT**.)*

`_nasce(v, dove, md, md0, meta=None)`. Con `meta` dato — il numero di voci della ### **prima
meta'** — il contatore `_fab` *(la lunghezza fabbricata, `sum(LAM - v)` sui troncati)* si calcola
### **per meta' e poi si somma**, invece che con un `np.sum` sull'array intero.

### **PERCHE' SERVE:** col `6a` la frazione della nascita e' esplicita, e i due tronconi diventano
`t*d` e `(1-t)*d` — ### **due blocchi** invece di un valore usato due volte. Quindi `dh` passa da
`_nasce` come array di ### **`2n`** con `md = 1`, dov'era `n` con `md = 2`.
### ⛔ **E UNA SOLA CHIAMATA, di proposito:** `_g_sm_nascite` conta le ### **INVOCAZIONI**, e
spezzarla in due lo farebbe salire di `2` invece di `1`.

### ⛔ **MA `np.sum` SU `2n` NON E' IDENTICA AL BIT A `2 * np.sum` SU `n`, ed e' MISURATO:**
### **4043 differenze su 14000** *(`csv/_test_fork/_somma_meta/`, 2000 prove per sette taglie)*.
### ✅ **La somma per META' a `t = 0.5` e' `s + s`, e `s + s == 2*s` e' ESATTO** — il
raddoppio e' uno scalamento per una potenza di due.

### ⚠ **E UN DETTAGLIO CHE VALE DA SE': a `n = 128` la forma concatenata NON diverge** *(la
somma a coppie di numpy allinea i blocchi)*. ### **Un test su UNA SOLA taglia avrebbe dato un falso
*<<identica>>***: e' la lezione di `FALSO-ZERO`.

### 📌 **E VALE SU DUE PERCORSI, non uno:** `dh` *(`mitosi`, `md` `2,0` → `1,0`)*
### **e** `dd` *(`schwinger`, `2,2` → `1,1`)*. ### **`d0new` RESTA com'e'** *(`0,1`)*: e' gia'
l'array dei due figli, e la sua somma e' gia' sull'array intero. ### **Il secondo percorso era
sfuggito al rilievo del guardiano, che l'ha dichiarato.**

### ✅ **VERIFICATO PRIMA DI SCRIVERE IL CODICE:** a `t = 0.5` tutti e ### **quattro** i
contatori *(`_g_sm_nascite`, `_sm_lun`, `_sm_tr`, `_sm_vis`)*, per tutti e ### **tre** i siti,
### **identici al bit** — zero differenze su 2000 prove per sito, con valori che
### **includono lunghezze sotto `LAM`**, altrimenti `_ntr` e `_fab` sarebbero zero
### **per costruzione** e la verifica sarebbe essa stessa un `FALSO-ZERO`.

### ⚠ **E con `meta=None` il comportamento e' IDENTICO a prima:** gli altri siti di `_nasce`
*(`semina`, `_allaccia`, `d0new`)* ### **non si accorgono di niente.**

> ### 🔓 **(c)1, 2026-09-27: IL CONFINE DELLA FOTOGRAFIA SI SPOSTA A INIZIO PASSO**
 > **`(c)1` di `ETC-PASSO`, 2026-09-27: `_smp_apri()` e' IDEMPOTENTE e la chiamano TUTTE
> e CINQUE le leggi**, in testa. **La prima che gira apre**, le altre quattro escono subito, e
> cosi' il confine della transazione e' a **inizio passo pieno qualunque sia l'ORDINE** -- che e'
> cio' che `H-ETC-2` permuta. **I chiamanti delle cinque leggi sono SEI**, e una divergenza fra
> due di loro sarebbe invisibile: l'idempotenza mette il confine **dentro** la cosa che deve
> rispettarlo. Contatore `A8`: **`_g_smp_gia_aperta`** = quante leggi l'hanno trovata gia' aperta
> *(4 per passo con le cinque canoniche)*.
>
> ### **E un difetto curato di passaggio:** in `step()` l'apertura stava **DOPO** la guardia
> `if self.n < 2 or not len(self.i): return`. **Un passo con meno di 2 nodi NON APRIVA la
> fotografia, e il freno del passo non chiudeva.** Ora sta **prima**.
> ### ⚠ **LA CHIUSURA NON E' TOCCATA, ed e' una decisione:** `_smp_chiudi()` sta in fondo a
> `memoria_hebbiana_moto` e **subito dopo c'e' `verifica_invarianti()`**. Spostarla fuori dalla
> legge farebbe girare il controllo degli invarianti su **`d0` non ancora frenata**: cambierebbe
> **quando** il controllo guarda, non solo dove sta il freno. **Secondo meccanismo, secondo
> commit** (regola d'oro). *(Verificato dal codice che `verifica_invarianti` **legge soltanto**:
> lo stato non cambierebbe, cambierebbe su quali valori il controllo scatta.)*


> ### 🗄 **I DUE PAVIMENTI VECCHI SONO USCITI DALLA LEGGE** *(2026-09-27, `(b)1`
> ### di `ETC-PASSO`)*
>
> **`_pav_d0` e `_floor_d0` non stanno piu' nel simulatore**, e la scheda non li elenca piu' fra
> le sue funzioni. Sono in **`csv/_archivio/_pavimenti_morti.py`**, col tag
> **`pre-archivio-pavimenti`**; con loro sono usciti i **due rami `else`** con
> `np.maximum(..., 0.05)` su `d` *(Verlet e Eulero)*.
>
> ### **LA FORMA DELLA LEGGE, dopo:** il vincolo sulle lunghezze e' **UNO SOLO**, ed e' `LAM`.
> Prima erano **DUE sovrapposti** -- il freno di `SCALA_MIN`/`SCALA_MIN_PASSO` **e** il pavimento
> comovente -- e il docstring di `_pav_d0` lo diceva: *<<lasciare anche il pavimento comovente
> vorrebbe dire DUE leggi sovrapposte, con la vecchia che continua a mordere>>*. **Quella
> sovrapposizione era gia' risolta a RUNTIME con un `return v`; ora e' risolta nella FORMA.**
>
> **`9-ter`: il numero delle leggi SCENDE.** I due sottocicli metrici passano da **tre rami a
> due**: il freno di `SCALA_MIN`, e l'aggiornamento nudo che `SCALA_MIN_PASSO` frena **una volta
> sola** a fine passo (`C3`).
>
> **DERIVAZIONE, e perche' non e' una perdita:** il pavimento vecchio era `0.05` assoluto, oppure
> `f*median(d0)` con `f = 0.05/LAM_BASE` se `PAV_COM`. **Misurato sui 16 stati del pilota:**
> `min(d) = 0.800000 = LAM` **esattamente**, in ogni stato e ogni checkpoint, **0 archi sotto
> `LAM`** -- e `0.05` sta **16 volte piu' in basso** del minimo osservato. **Il pavimento vecchio
> non definiva il vincolo: lo seguiva da sedici volte piu' giu'.**
>
> **DIMENSIONI:** invariate. `LAM` e' una lunghezza (`A13`: la scala di Planck del modello), e il
> vincolo `d >= LAM` resta quello di prima.
>
> **LIMITI, e `A11`:** il limite che RESTA e' `LAM`, e la scheda lo classifica gia' *(corollario
> 2: `LAM` e' costante e non insegue `d0`, a differenza del pavimento comovente di `Z91`)*.
> **Il limite che ESCE era proprio quello che il corollario 2 accusava.**
>
> **⚠ E COSA CAMBIA, dichiarato:** con **entrambi** `SCALA_MIN` e `SCALA_MIN_PASSO` **spenti**
> *(configurazione che il driver NON usa)* prima `d0` aveva un pavimento e **ora non l'ha piu'**.
> **`PAV_COM` diventa INERTE** in entrambi i suoi stati, e lo dichiara all'avvio.
>
> ### ⚠ **CORREZIONE del 2026-09-27 (Luca, su `7840039`): LA PRECEDENZA**
>
> Togliendo il pavimento avevo collassato la catena
> `if SCALA_MIN_PASSO: nudo / elif SCALA_MIN: freno / else: 0.05` in
> `if SCALA_MIN: freno / else: nudo`, **e questo ROVESCIA LA PRECEDENZA.**
> **Col driver e' identico** *(`SCALA_MIN` e' spento)*, **ma con ENTRAMBI i flag accesi si
> frenerebbe DUE VOLTE** -- per scrittura **e** a fine passo -- mentre **deve vincere il freno
> PER PASSO** (`C3`), che e' l'intero punto della cura: frenare scrittura per scrittura fa
> dipendere il risultato dall'**ORDINE**.
>
> **LA FORMA GIUSTA, ora esplicita in entrambi i sottocicli:**
> `if SCALA_MIN and not SCALA_MIN_PASSO: freno` / `else: nudo`.
>
> ### **E la precedenza sulle scritture di `d0` era GIA' intatta:** `_sd0` controlla
> `SCALA_MIN_PASSO` **per primo** e **ritorna**, quindi non l'ho toccata -- verificato dal
> codice, non assunto.
>
> **La lezione, e vale oltre questo caso:** un `elif` che diventa `else` **non e' una
> semplificazione, e' un cambio di ordine fra due condizioni**. Il sigillo byte-identico col
> driver **non poteva vederlo**, perche' col driver una delle due e' spenta: **un sigillo su UNA
> configurazione non certifica una PRECEDENZA fra due flag.**

> **`D31` NON E' TOCCATA:** *il freno e' solo in discesa* resta il difetto aperto di questa
> scheda, ed e' della cura **(d)**.


> **STATO: `DIFETTOSA`.** Difetto **`D31`**. **Viola `A11` corollario 4 e corollario 7(b).**
> **È IL MOTORE DELLA CRESCITA DI `d0`**, misurato due volte con un bilancio che chiude.
>
> ### ➜ **`_nasce` ORA MISURA LA LUNGHEZZA CHE FABBRICA** *(2026-09-25, `U2`)*
>
> Tre contatori `A8`, **byte-inerti**: `_sm_visti`, `_sm_troncati`, **`_sm_lunghezza`**.
> **`_g_sm_nascite` contava le INVOCAZIONI, non i troncamenti** — quindi *«quanto `_nasce`
> ha fabbricato»* **non era leggibile**. Ora `_sm_lunghezza = sum(LAM - d)` sui troncati è
> **il contributo DIRETTO di questa funzione al gonfiamento di `d0`, nelle stesse unita'
> del bilancio** — cioè nelle stesse unita' in cui `D31` accusa il freno.
> **Serve a `U2`**, e la legge sta in scheda ⑫.
>
> ### ➜ **`_nasce` HA PERSO IL SUO GATE** *(2026-09-24, `D38`)*
>
> `_nasce` — *il troncone sotto `LAM` si porta A `LAM`* — era `if not (SCALA_MIN or
> SCALA_MIN_PASSO): return v`. **Il gate è TOLTO: il presidio agisce SEMPRE.**
> **Coi default del SORGENTE la legge `d >= LAM` era VIOLATA AL PASSO ZERO su `223 380`
> archi**, ed è **lo stesso schema che `E4-LAM` ha tolto al CONTROLLO e che era rimasto
> all'ESECUZIONE**: *il controllo era legge, chi la faceva rispettare era un'opzione.*
>
> **⚠ E NON È UNA CURA, È UN PRESIDIO** *(decisione di Luca)*: con `SEMINA_LAM` acceso **non
> deve scattare mai**, e **`_g_sm_nascite` è la sua misura**. **La legge sta in scheda ⑫.**
>
> ### ✅ **LA FORMA DELLA CURA DI `D31` È DECISA** *(Luca, 2026-09-24)*
>
> ```
> (d − LAM)  ←  (d − LAM) · (1 + tanh(dx / d))
> ```
>
> **LA MISURA CHE L'HA DECISA:** `V8`/`V9` dal giro corto di `CURA 2` — **`max |dx|/d = 0.0531`
> su `125 731 076` campioni, ZERO oltre `0.5`** su entrambi i versi. **Il solo difetto
> dichiarato di `tanh`, la saturazione a `2`, non si presenta mai:** conta a `x ~ 1`, e il
> massimo misurato è **`19` volte** più piccolo.
>
> **⚠ E IL CONFRONTO NON È SIMMETRICO:** la deriva di `piana` vale `exp(N·E[x²]/2)`, e **`E[x²]`
> NON è stato registrato** — a `6000` passi l'intervallo va da **`+1.7 %` a `+471 %`**.
> **Si sceglie la forma il cui prezzo si CONOSCE.**
>
> **CRITERIO CHE LA RIAPRE, scritto ORA** *(par.10: la condizione si scrive al momento della
> decisione, non dopo)*: **una quota NON NULLA di `|dx|/d > 0.5`.**
>
> **⚠ NESSUN CODICE: la forma è decisa, la scrittura no.** Sta in **scheda ⑩ par.4-quinquies**,
> e **l'ordine — se il freno-legge venga prima o dopo `CURA 3` — è un CHECKPOINT di Luca.**

## LA FORMA — copiata dal codice, non dal commento

**Il nucleo, `_smorza` (`:3526`):**
```
eff(prima, dx) =  dx                                se  dx >= 0     <- IDENTITÀ ESATTA
                  dx * max(0, 1 - LAM/prima)        se  dx <  0     <- solo la DISCESA è frenata
```
**L'applicazione, `_smp_chiudi` (`:3698`), UNA VOLTA per passo:**
```
v  = d0 a INIZIO passo                   (fotografia di `_smp_apri`, :3666)
dx = d0 a FINE passo - v                 (la variazione TOTALE del passo)
d0 <- v + eff(v, dx)
```

**L'INVARIANTE, dichiarato nel docstring e verificato algebricamente qui:**
```
nuovo - LAM = (prima - LAM) * (1 + dx/prima)
```
*(sviluppo: `nuovo = prima + dx - dx·LAM/prima`, e `(prima-LAM)(1+dx/prima) = prima + dx - LAM -
LAM·dx/prima`. Coincidono.)*

> **COSA DICE DAVVERO QUESTO INVARIANTE, ed è il contenuto fisico della legge:** per `prima > LAM`
> e `dx > -prima`, il fattore `(1 + dx/prima)` è **positivo**, quindi **`nuovo > LAM` sempre**.
> **`LAM` è una BARRIERA ASSORBENTE DALL'ALTO: non si tocca e non si attraversa, la si avvicina
> asintoticamente.**

## DA DOVE VIENE

**`LAM` è la scala del sistema** — la stessa che fissa `R_CONN = 3·LAM`, il filtro di portata
`1 − tanh(d/LAM)` e l'ancora elastica. **Non è un numero scelto per questa legge:** esisteva prima.
**Il vincolo dichiarato è: nessuna lunghezza sotto `LAM`** *(`:979`)*.
**La FORMA `1 − LAM/x` invece NON è derivata: è stata scelta fra tre**, e le altre due sono cadute
*(`A11` cor.7, `doc/TASK_HISTORY/2026-09-21_ramo_D_tre_modifiche.md`)*. **`NON RICOSTRUITO`: perché
proprio questa forma e non un'altra che rispetti l'obbligo (b).**

## LE DIMENSIONI

| simbolo | dimensione |
|---|---|
| `prima`, `dx`, `eff`, `LAM` | **lunghezza** `[L]` |
| `LAM/prima` | **adimensionale** |
| `eff = dx · (1 − LAM/prima)` | `[L]` ✔ |

**Coerente.** *(Il difetto non è dimensionale: è di simmetria.)*

## COSA LEGGE / COSA SCRIVE

- **legge:** `d0` a inizio passo *(`_smp_apri`)*, `d0` corrente, `LAM`.
- **scrive:** **tutto `d0`**, a fine passo, dentro `_smp_chiudi` *(`:3719`)*.
- **⚠ E NON HA NESSUN SITO DI TRACCIA** — è il difetto **`D04`**: la scrittura è **invisibile** a
  `_traccia_d0`, ed è il termine che in `Z107` lasciava il bilancio aperto. Nel bilancio di `G4` è
  aggirato **avvolgendo `_smorza` dall'esterno**; **nel simulatore il sito manca ancora.**
- **il chiamante `d0_passo`** è quello del bilancio; esiste anche `d_passo`, **dentro un sito già
  tracciato**, che non va sommato o si conta due volte.

## I LIMITI, CLASSIFICATI CON `A11`

| corollario | esito |
|---|---|
| **1 — origine fisica** | ✅ `LAM` è la scala del sistema, non una difesa dalla divisione |
| **2 — non dipende da ciò che limita** | ✅ `LAM` è costante; **non** insegue `d0` *(a differenza del pavimento comovente `f·median(d0)` di `Z91`)* |
| **3 — non ribalta segni** | ✅ `fatt ∈ [0,1]`, quindi `eff` ha il segno di `dx`; e `_g_sm_max_giu ≤ 0` lo misura a ogni scrittura |
| **4 — SIMMETRICO** | ❌ **VIOLATO, e DIMOSTRATO sulla formula** *(`Z113`, `4/4`)*: su rumore a media **zero esatta**, lontano dal confine, la deriva è **`+1.582064e-03`** contro l'attesa derivata **`+1.582007e-03`** — **scarto `0.0 %`**. **E con `LAM = 0` la deriva è `0.000000e+00` ESATTO**, con un freno **simmetrico** `5.9e-09`: **viene dall'ASIMMETRIA** |
| **5 — si ripara all'origine** | ⚠ **DA DECIDERE:** il freno sta nel punto d'uso. **Dove nasce la discesa che va frenata?** |
| **6 — se satura è un allarme** | ❌ **VIOLATO, e ora è MISURATO** *(`Z113`)*: al passo 600 il **`13.74 %`** degli archi sta in `[1.0, 1.1)·LAM`, dove il freno annulla il **`99.96 %`** di ogni discesa, e porta il **`35.80 %`** del freno. **La popolazione si è POLARIZZATA:** `13.74 %` incollato al muro, **`60.32 %` oltre `3·LAM`**, le bande intermedie svuotate |
| **7(a) — lontano è identità** | ✅ per `x ≫ LAM`, `1 − LAM/x → 1` |
| **7(b) — nessuna deriva su spinte simmetriche** | ❌ **VIOLATO, ed è il punto.** |
| **7(c) — larghezza dalla fisica** | ✅ la larghezza **è** `LAM` |

## ⭐ **LA CURA (2): IL SITO DELLA FASE SI SPEGNE** *(`MEM_FASE`, decisione di Luca
## del 2026-10-04, sigillata il 2026-10-05)*

> ### ⛔ **IL NUMERO CHE L'HA DECISA: il sito SCARTAVA IL `97.3%` DEI CONTRIBUTI CHE
> ### CALCOLAVA.**

**IL DIFETTO, misurato e non letto** *(`doc/REFERTO_mem_hebb_verso_2026-10-05.md`,
commit `2717308`)*: `phi[ii] = (phi[ii] + shift) % _dphi()` con `ii` che
### **contiene ripetizioni** — un nodo e' primo estremo di **fino a `90`** archi — e in
numpy l'indicizzazione **fancy in scrittura** fa ### **VINCERE L'ULTIMO.**

| | |
|---|--:|
| contributi **applicati** | `1 925 336` |
| contributi ### **SCARTATI** | ### **`68 847 776`** |
| frazione scartati | ### **`0.9728`** |
| somma dei **moduli** applicati | `3.4531e+04` |
| somma dei **moduli** scartati | ### **`1.2514e+06`** |
| ### **rapporto scartati/applicati** | ### **`36.24`** |

### ⛔ **E NON E' UNA SOMMA MANCATA: E' UNA SCELTA FATTA DALL'ORDINE DELL'ARRAY.** Se
la legge volesse **sommare** servirebbe `np.add.at`, che il file ### **usa altrove**, a
`:9115`, ### **nella stessa funzione.**
### **Un fenomeno che cambia se riordini un array NON e' un fenomeno del sistema**, ed e'
la risposta alla **domanda 5** della stella polare.

### ✅ **E IL TAGLIO `pi/4` NON C'ENTRA, e questo chiude una domanda aperta di questa
### scheda:** morde sullo ### **`0.0011`**. ### **Due distorsori possibili, e il
colpevole e' l'altro.**

**LA FORMA DELLA CURA:** un `if MEM_FASE:` attorno a ### **quella riga e basta.**
`mem_mot` continua ad aggiornarsi, `proiezione_trasversale` e `shift_fase_dinamico`
restano **calcolati**, e il taglio `pi/4` resta **applicato**: ### **si toglie SOLO il
contributo a `phi`**, com'e' per `MEM_MOTO` sul contributo a `d0`.

### ⛔ **IL DEFAULT E' `False`, E NON E' UN FLAG BYTE-INERTE:** spento,
### **LA FISICA CAMBIA.** E' la fisica **decisa**. ### **E' il PRIMO flag di questo repo
il cui default cambia la fisica** — tutti gli altri nascono *OFF e inerti* oppure *ON*.

### ⚠ **E TOGLIE ANCHE IL `% _dphi()`, non solo la somma:** il commento del codice
dichiara che `(phi + 0) % (4 pi)` e' un NO-OP ### **solo se `phi` sta gia' nel dominio.**

### ⛔ **GLI ALTRI DUE DIFETTI DEL SITO NON SONO CURATI, e spegnere NON E' CURARE**

| difetto | dove vive |
|---|---|
| solo l'estremo `ii` riceve | `MEM-HEBB-VERSO` |
| `phi[ii] = ...` con indici ripetuti: vince l'**ultimo** | ### **curato QUI, spegnendo** |
| `dir_laterale = (-y, x, 0)` privilegia l'asse `z` del **laboratorio** | ### **`FASE-TRASCINAMENTO-3D`, che RESTA APERTA** |

### **La legge in 3D NON si scrive ora** *(decisione di Luca)*, e la voce ### **non si
chiude.**

**IL SIGILLO:** `csv/_seal_fork/_sigillo_mem_fase.py` *(`a5cb4c60`)*; la patch del
braccio 0 e' `csv/_seal_fork/_mem_fase_patch.py` *(`8b9c0c1a`)*.
**Simulatore curato: `1feb9b0a`** *(da `e2940b3c`)*.

## LO STATO: `DIFETTOSA` — **e quanto pesa, misurato**

| | `Z108` *(braccio acceso, 600 passi)* | `Z109` *(senza memoria del moto)* |
|---|--:|--:|
| **FRENO** | **`+117.41 %`** del `Δ(Σd0)` | **`+218.33 %`** |
| scritture fisiche | `−17.43 %` | `−118.38 %` |
| nascite − morti | `0.01 %` | `0.05 %` |
| residuo del bilancio | `1.138e-13` | `1.170e-13` |

> **Gli scrittori fisici tirano `d0` GIÙ. È il VINCOLO a gonfiarlo.**
> **E la sua quota CRESCE quando si spegne un'altra legge**, perché il `Δ` si rimpicciolisce e il
> freno no. **Epoca: archivi delle cure**, blob `ab685eac`, UN seme, UNA scena, 600 passi.

## LE DOMANDE APERTE — **tre candidati per il limite fisico. DOMANDE, non scelte.**

> **Poste da Luca, 2026-09-22.** **Nessuna è stata scelta, e questa scheda non sceglie.**

### (A) **La barriera da POTENZIALE, con un integratore che non la scavalca**

**L'idea:** invece di frenare la variazione *a posteriori*, mettere `LAM` in un **potenziale** che
diverge al confine, e integrarlo con uno schema che **non può** scavalcarlo — come `PEQ_ESATTO` ha
fatto per `peq` *(`A11` cor.5: la positività **dimostrata** da una combinazione convessa invece che
**imposta** da un pavimento)*.

**LE DOMANDE:**
1. **Qual è il potenziale, e da dove viene?** Se va scelto, è una manopola *(par.3)*.
2. **Rispetta l'obbligo (b)?** Un potenziale repulsivo è **simmetrico per costruzione** — ma
   aggiunge **energia**: da dove la prende?
3. **`A6`:** il potenziale dipenderebbe da `d0` e agirebbe su `d0` nello **stesso istante**. Serve
   uno sfasamento, come la cura dell'anello di `ritmo()`?

### (B) **La repulsione a `4π` che ESISTE GIÀ** *(→ `D33`, misurato oggi)*

**L'idea:** il sistema **ha già** una repulsione per la materia super-compressa — il ramo negativo
di `mitosi()` *(`:5153`)*. **Non serve inventarla: serve farla arrivare dove serve.**

**MA `D33` DICE CHE OGGI NON CI ARRIVA**, e i numeri sono di **oggi**, archivi delle cure:
- il **segno** si inverte oltre `~3.5π`, **ma `discesa = clip(1 − |tw|/4π, 0, 1)` è ZERO ESATTO da
  `4π`**: la finestra utile è larga **mezzo `π`**;
- **dal `75.3 %` al `95.8 %`** degli archi oltre l'inversione riceve **repulsione esattamente zero**;
- il saldo di `S05_spinta_locale` su 600 passi vale **`+3.57`** contro **`−2.6e+05`** di `S09`:
  **un fattore `~1e-5`**.

**⚠ E IL NUMERO CHE CIRCOLAVA ERA DI UN'ALTRA EPOCA:** il commento `:64-66` dice che la torsione
**satura a `~2.5π`** — **`PRE-FORK`**. **Oggi `max|tw|` sta fra `9.5π` e `13.0π`.**

**LE DOMANDE:**
1. **`discesa` deve annullarsi a `4π`?** Nasce come *«spegnimento della MITOSI al tetto»* — ma
   moltiplica **anche** il ramo repulsivo. **Sono due leggi in un prodotto solo.**
2. **Se si separassero, la repulsione oltre `4π` sarebbe la barriera cercata?** E con quale
   ampiezza, visto che il `0.02` di `:5230` è **un numero scelto** *(`A1` violato, già dichiarato)*?
3. **La repulsione agisce su `d0`, il freno agisce su `d0`. Sono lo stesso vincolo scritto due
   volte?** Se sì, **una delle due va tolta**, non affiancata.

### (C) **Un'esclusione alla Pauli sugli spinori, DA DERIVARE**

**L'idea:** la scala minima non sarebbe un vincolo **sulla lunghezza**, ma la **conseguenza** di
un'antisimmetria degli spinori: due nodi nello stesso stato non possono coincidere. **Sarebbe
l'unico dei tre candidati a rendere `LAM` un RISULTATO invece che un'ipotesi.**

**LE DOMANDE:**
1. **`A6` (teorema):** il trasporto oggi è **scalare** *(`:2207-2208`, abeliano per struttura)*.
   **Un'esclusione richiede l'antisimmetria dello stato a due corpi: il sistema ce l'ha?**
2. **Da dove verrebbe la scala?** Un'esclusione dà una **densità** massima, non una lunghezza:
   il passaggio `densità → LAM` **va derivato, non postulato** *(par.3)*.
3. **È verificabile oggi?** `spin_ovl = 0.5` = **direzioni di Bloch CASUALI** *(par.9)*: su un
   substrato senza struttura di spin, **un'esclusione non ha su cosa agire.** **La domanda
   precedente a tutte è se il substrato esista.**

## LAVORO RESIDUO DI QUESTA SCHEDA

- ✅ **FATTO** *(`Z113`)*: le bande di `d0/LAM` e il test del cricchetto. **Restano i CONTATORI del simulatore** *(`_g_sm_discese`, `_g_sm_patol`, `_g_sm_viol_*`)*, **mai letti in un referto**: la misura di `Z113` è fatta sugli snapshot e su una formula, **non su quei contatori**;
- ⚠ **`_smorza` HA DUE CRICCHETTI, non uno** *(trovato sbagliando, reperto `7203ae3`)*: oltre a `LAM`, la guardia **`pos = prima > 0`** azzera le discese e lascia passare le salite. **Non è raggiungibile oggi** — `d0 >= LAM` per costruzione — **ma è una proprietà della formula, e una cura che tocchi il pavimento la incontrerà**;
- **`A11` cor.5:** dove nasce la discesa che il freno trattiene? **Non è stato cercato.**

---


### ❌❌ `_nasce` — **I CONTATORI MESCOLAVANO `d` CON `d0`. CORRETTO** *(rilievo di Luca, 2026-09-25)*

**`_nasce` è una legge di questa scheda**, e i suoi contatori appartengono qui.

`_nasce(v, dove="?", md=1, md0=1)`. **`md`/`md0` dicono quanti ARCHI VERI di `d` e di `d0`
diventa ogni voce di `v` nel sito che chiama** — e **sono diversi in ognuno dei quattro siti**:

| sito | `md` | `md0` | dal codice |
|---|--:|--:|---|
| `semina` — `_allaccia`, `dd` | `1` | `1` | `d = concat([d, dd])` **e** `d0 = concat([d0, dd])`: **UNA chiamata, DUE grandezze** |
| `mitosi` — `dh` | **`2`** | `0` | `d = concat([d[keep], dh, dh])`: **due archi per voce** |
| `mitosi` — `d0new` | `0` | `1` | `d0new` è **già** `concat([d0h, d0h])` |
| `schwinger` — `dd` | **`2`** | **`2`** | `[d, dd, dd]` **e** `[d0, dd, dd]` |

**Contatori: `_sm_{lun,tr,vis}{d,d0}_{sito}`.** Byte-inerti *(si somma, non si cambia)*.

> ### **Solo `_sm_lund0_*` è nelle unità del bilancio di `d0`, quindi solo quello entra in `P-GONFIA`.**

**COSA C'ERA PRIMA, e perché era sbagliato:** un contatore solo, `_sm_lunghezza`, che
① **sommava `d` e `d0` nello stesso numero** — quindi **non era nelle unità di nessuna delle
due**, che era l'unica ragione per cui l'avevo scritto; ② **sottocontava di `2`** il sito `dh`;
③ contava le **voci**, non gli **archi**, anche nel denominatore.

**SIGILLO: `csv/_seal_fork/_sigillo_u2_contatori.py`** — **una MITOSI VERA** con un solo arco a
`1.2 LAM` *(`dh = 0.6 LAM`, entrambi i figli troncati)*; atteso per costruzione
`trd = trd0 = 2`, `lund = lund0 = 0.8 LAM`. **`U2-6` è il caso che DEVE fallire** *(`P1-sexies`)*:
la formula vecchia, sullo stesso evento, dava `0.4 LAM` su `d` e una somma mescolata di `1.2 LAM`.

**⚠ `_g_sm_nascite` RESTA, e misura un'altra cosa:** le **INVOCAZIONI**. Una chiamata che non
tronca nulla lo fa salire ugualmente — è il presidio di `D38`, non una misura del troncamento.

<!-- SCHEDA nome=memoria-del-moto funzioni=memoria_hebbiana_moto flag=MEM_HEBB,MEM_MOTO,MEM_FASE,MEM_MOTO_TUTTO,SCALA_P_MEDIANA,ZETA_VIR -->
# ② LA MEMORIA DEL MOTO — **`memoria_hebbiana_moto` / `S08_proj` / `mem_mot`**

> ### 🏗 **T1: escono da questa legge l'apertura, LE DUE CHIUSURE e il controllo degli invarianti**
> **`T1`, 2026-09-28: l'apertura del passo NON sta piu' qui.** La fa lo **SCHEDULATORE**
> (`esegui_passo`), in testa alla composizione, e **l'idempotenza di `(c)1` non serve piu'** --
> il compositore **sa** di essere il primo. **Misurato:** `_g_smp_gia_aperta` passa da **4 per
> passo** a ### **0**. *(Scheda `schedulatore-del-passo`; tag `pre-schedulatore-t1`.)*
>
> **Questa legge portava il confine del passo per tutti:** chiudeva il freno **in coda** e **anche
> sul ritorno anticipato** *(`if not MEM_HEBB or self.n < 2 ...`)*, e chiamava
> `verifica_invarianti(dove='memoria_hebbiana_moto')`. ### **Tutto questo e' dello schedulatore.**
> ### 📌 **E il ritorno anticipato e' il caso che dice perche' l'architettura batte la regola:** il
> suo commento spiegava con cura che *<<anche sul ritorno anticipato il freno va chiuso, senno' lo
> snapshot resterebbe aperto e il passo DOPO confronterebbe `d0` con quello del passo PRIMA>>*.
> **Era una regola scritta e rispettata a mano in un punto solo.** Ora il confine **non dipende
> piu' da quale uscita la legge prende.**
> **La fisica della memoria del moto non e' toccata:** il sigillo di `T1` e' **byte-identico**.


> ### 🔓 **(c)1, 2026-09-27: anche questa legge APRE il passo**
 > **`(c)1` di `ETC-PASSO`, 2026-09-27: `_smp_apri()` e' IDEMPOTENTE e la chiamano TUTTE
> e CINQUE le leggi**, in testa. **La prima che gira apre**, le altre quattro escono subito, e
> cosi' il confine della transazione e' a **inizio passo pieno qualunque sia l'ORDINE** -- che e'
> cio' che `H-ETC-2` permuta. **I chiamanti delle cinque leggi sono SEI**, e una divergenza fra
> due di loro sarebbe invisibile: l'idempotenza mette il confine **dentro** la cosa che deve
> rispettarlo. Contatore `A8`: **`_g_smp_gia_aperta`** = quante leggi l'hanno trovata gia' aperta
> *(4 per passo con le cinque canoniche)*.
>
> **Qui la chiamata e' inserita dopo il docstring**, e nell'ordine canonico **trova sempre la
> fotografia gia' aperta**: e' l'ultima delle cinque. **Serve per le PERMUTAZIONI** -- se
> `H-ETC-2` la mette prima, deve poter aprire lei.


> ### 🗄 **(b)1, 2026-09-27: le CINQUE chiamate al pavimento vecchio sono uscite**
>
> `memoria_hebbiana_moto` chiamava **cinque volte** `self.d0 = self._pav_d0(self.d0)`, dopo
> `S08_proj`, dopo la gravita', dopo il flusso, dopo la coesione e dopo `:7042`. **Col driver
> erano cinque NO-OP** *(`_pav_d0` usciva dal ramo inerte: `_g_sm_pav_saltati = 15` su 15
> chiamate totali, riga del pavimento **0 esecuzioni**)*, e ora **non ci sono piu'**.
> **La forma della legge non cambia:** questa scheda scrive `d0` con `_sd0`, e il freno di
> `SCALA_MIN_PASSO` chiude **una volta sola** a fine passo (`_smp_chiudi`, chiamata proprio da
> qui). **Quello che esce e' il secondo vincolo, quello sovrapposto.**
> Anche i cinque `pavimento=self._floor_d0()` delle tracce `TRACCIA_D0` sono usciti:
> l'argomento era **`None` per difetto** e la firma di `_traccia_d0` **resta**.


> **STATO: `DIFETTOSA`.** Difetti **`D03`** *(direzioni dal disegno, `Imed` globale, tetto
> `0.01·median(d0)`)* e **`D02`** *(il pozzo usa `pos`)*.
> **Cura derivata e NON scritta: `MEM_ARCO`.** **Spegnerla toglie il `62 %` della crescita di `d0`
> e FA SPARIRE LA COMPRESSIONE** *(`Z109`)*.

## LA FORMA — copiata dal codice (`:5644-5676`), non dal commento

```
twn[nodo]   = SUM |tw| sugli archi incidenti / deg            [rad]
dtw[arco]   = twn[jj] - twn[ii]                               [rad]
dirarc      = (pos[jj] - pos[ii]) / |pos[jj] - pos[ii]|       <- DAL DISEGNO (D02/D03)
grad_tw[n]  = SUM_archi dtw * dirarc / deg                    [rad]   <- NON diviso per una lunghezza
plast       = tanh(|grad_tw|)                                 in [0,1)
mem_mot     = (1 - plast)*mem_mot + plast*grad_tw             <- LA MEMORIA: rilassamento
memedge     = 0.5*(mem_mot[ii]*I[ii]/Imed + mem_mot[jj]*I[jj]/Imed)    <- Imed GLOBALE
proj        = SUM(memedge * dirarc)
proj        = clip(proj, -0.01*median(d0), +0.01*median(d0))  <- TETTO GLOBALE
d0[mask]   += _sd0(proj, mask)                                <- il sito `S08_proj`
```
**E IL QUARTO PUNTO, che non scrive su `d0` e che `MEM_MOTO` non copriva** (`:6033`):
```
proiezione_trasversale = SUM(mem_mot[ii] * dir_laterale)
shift_fase_dinamico    = accoppiamento_dinamico * proiezione_trasversale * (d_archi/d0_archi)
if MEM_FASE:                             # <- IL GATE, dal 2026-10-05 (default SPENTO)
    phi[ii] = (phi[ii] + clip(shift_fase_dinamico, -pi/4, +pi/4)) % 4pi
```
### ⛔ **E DAL 2026-10-05 QUESTO PUNTO E' SPENTO DI DEFAULT** *(`MEM_FASE = False`,
decisione di Luca del 2026-10-04)*: la riga **non gira**. Il **perche'** sta sotto,
### **ed e' un numero.**

## DA DOVE VIENE

**Legge del momento:** `mem(t+1) = mem(t) + correzione_dal_campo`. La **plasticità** non è scelta:
è `|grad_tw|` stesso, saturato da `tanh`. **Questo è derivato.**
**`NON RICOSTRUITO`:** perché la correzione sia `grad_tw` *(differenza di torsione per nodo)* e
non un'altra forma; e perché il tetto sia `0.01`.

## LE DIMENSIONI — **e qui c'è un problema**

| simbolo | dimensione |
|---|---|
| `tw`, `twn`, `dtw`, `grad_tw`, `mem_mot` | **angolo** — adimensionale |
| `dirarc`, `I/Imed`, `plast` | adimensionale |
| **`proj`** | **adimensionale** |
| **`d0`** | **lunghezza `[L]`** |

> **⚠ `proj` È UN NUMERO PURO, E VIENE SOMMATO A UNA LUNGHEZZA.**
> **L'unica cosa che gli dà unità di lunghezza è IL CLIP `0.01·median(d0)`.**
> **Quindi il clip non è un limite: è la SCALA della legge** — ed è esattamente ciò che il
> `78 %`–`89 %` di saturazione misurato dice *(`Z112`)*.
>
> **E `grad_tw` è chiamato GRADIENTE ma non è diviso per una lunghezza:** un gradiente vero
> sarebbe `dtw/L`. **`A3c`.**

## COSA LEGGE / COSA SCRIVE

- **legge:** `tw`, `pos` *(il DISEGNO — `D02`)*, `psi` → `I` e `Imed` *(media **globale** —
  `A2`, `D03`)*, `_deg`, `d0`.
- **scrive:** `mem_mot` *(stato per nodo)* · `d0` al sito **`S08_proj`** · **`phi`** al
  punto `:6033`.
- **flag:** **`MEM_MOTO`** recinta la **sola** scrittura su `d0`; ### **`MEM_FASE`**
  *(dal 2026-10-05)* recinta la **sola** scrittura su **`phi`**, ed e'
  ### **SPENTO di default**; **`MEM_MOTO_TUTTO`** recinta **tutti e quattro** i punti
  *(sigillo `10/10`, blob `21e3a3dc`)*.

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `clip(proj, ±0.01·median(d0))` | **1** | ❌ il `0.01` è **scelto** *(`A1`)* |
| | **2** | ❌ **cresce con `d0`**: più `d0` scappa, più il tetto glielo consente |
| | **6** | ❌ **saturo nel `78 %`–`89 %`**: *«non è un limite, è la legge»* |
| `max(median(I), 1e-9)` | **1** | ⚠ difesa dalla divisione, non vincolo fisico |
| `max(|v|, 1e-9)` su `L` | **1** | ⚠ idem |
| `clip(shift_fase, ±π/4)` | **1** | ### ✅ **MISURATO il 2026-10-05: satura sullo `0.0011`** *(`doc/REFERTO_mem_hebb_verso_2026-10-05.md`)*. ### **NON e' lui il distorsore del sito:** il distorsore e' ### **<<l'ultimo vince>>**, che morde sullo `0.973` |

## LO STATO: `DIFETTOSA` — **e quanto pesa, misurato**

| | acceso | spento *(`MEM_MOTO=False`)* |
|---|--:|--:|
| `Δ(Σd0)` su 600 passi | `+1.731e+06` | **`+6.504e+05`** — **−62 %** |
| `S08_proj`, saldo | `+7.151e+05` | assente |
| `med d/d0` finale | `0.7489` **`NON REGGE`** | **`0.8546` `REGGE`** |
| criteri | `6/8` | **`7/8`** |

## L'IPOTESI DELLA COMPRESSIONE — **misurata, e si divide in due**

> *«`S08_proj` scrive `d0` verso l'ALTO senza che `d` segua, e questo abbassa `d/d0`»*
> *(Luca, 2026-09-22 · `csv/_test_fork/_compressione_memmoto.py` blob `f5e55310`, `Z112`)*

**✅ LA PARTE «`d` NON SEGUE» REGGE, e nettamente.** Fra i due bracci allo **stesso** passo,
spegnendo `S08_proj`:

| passo | `Δd0/d0` | `Δd/d` | **rapporto** |
|--:|--:|--:|--:|
| 120 | `−11.42 %` | `−1.37 %` | **`8.35`** |
| 360 | `−27.94 %` | `−3.11 %` | **`8.97`** |
| 600 | `−32.01 %` | `−12.97 %` | **`2.47`** |

**`d0` è da `2.5` a `9` volte più sensibile di `d`.** Il criterio chiedeva `>= 2` ovunque: **c'è.**

**⚠ LA PARTE «VERSO L'ALTO» NON REGGE COME SCRITTA, e va detto.** La frazione di archi con
`proj > 0` è **`57.7 %` · `64.3 %` · `58.6 %` · `51.4 %` · `47.4 %`**: **decresce**, e **al
passo 600 è SOTTO metà** con **somma NEGATIVA** *(`−8.4e+02`)*.
**Ma la correlazione trasversale è forte e sempre dello stesso segno: `−0.19` … `−0.44`**,
contro un nullo di `1.4e-03` — **da `140` a `310` volte il suo valore sotto ipotesi nulla**.
**Gli archi che ricevono più `proj` HANNO `d/d0` più basso, nello stesso istante.**

> **COME SI LEGGONO INSIEME, ed è il limite che avevo dichiarato PRIMA:** `proj` è l'incremento
> **istantaneo**, `d/d0` è una **storia**. **Al passo 600 l'istantaneo è già girato in negativo
> mentre `d0` resta alto: è l'ACCUMULO che comprime, non il segno del momento.**
> **L'ipotesi regge nella sostanza — `S08_proj` è la causa della compressione — ma il
> meccanismo NON è «spinge sempre in su»: è «ha spinto in su, e `d0` non torna».**
> **E questo è esattamente il cricchetto del freno** *(scheda ①, `A11` cor.4)*: `d0` sale e non
> può scendere. **Le due schede si toccano qui.**

## ⚠ `FASE_2PI` TOCCA UN SITO ANCHE QUI

**`:6105`**, l'avvolgimento di `phi` dopo lo spostamento di fase, passa da `% (4π)` a **`% self._dphi()`**. **È l'unico punto di questa scheda che la cura del dominio attraversa**, e la legge della memoria del moto **non cambia**: cambia **il periodo su cui `phi` si richiude** dopo che questa legge l'ha spostata.

## LE DOMANDE APERTE

1. **`proj` è adimensionale e viene sommato a una lunghezza.** **Quale lunghezza fisica lo
   converte?** Oggi lo fa il clip, che è un numero scelto. **`MEM_ARCO` deve rispondere a questa
   prima di essere scritta.**
2. **`grad_tw` è un gradiente senza divisione per la lunghezza dell'arco.** Dividerlo cambia la
   legge o la ripara?
3. **Il `62 %` di `Z109` non è il peso della sola scrittura su `d0`:** `shift_fase_dinamico` legge
   `d_archi/d0_archi`, quindi il punto (4) è **accoppiato** al punto (3) attraverso `d0`
   *(sigillo di `G4-bis`, `T6`)*. **`G4-bis` è il braccio che separa le due cose.**
4. **Se `d0` è `2.5`–`9` volte più sensibile di `d`, che cosa lega `d` a `d0`?** La compressione
   è un difetto **di `d0`** o un'**assenza di accoppiamento** verso `d`?

---

<!-- SCHEDA nome=gravita-bifase funzioni=pozzo_grafo,_nb_grav flag=GRAV_BIFASE,VIRIALE,LS_AZIM,PHI_CRIT,K_FRANGE,POZZO_D -->

### **AGGIORNAMENTO del 2026-10-04, commit `6b`** *(questa scheda possiede
`pozzo_grafo`)*: **il commento sul pavimento `1e-9` e' stato corretto.** Diceva che
`d >= LAM` vale *«con `SEMINA_LAM`/`MITOSI_2LAM`»*, cioe' ### **sotto condizione di un
flag**; dal `6b` alla divisione vale **sempre** e `MITOSI_2LAM` e' **inerte**.
### ⚠ **NIENTE CAMBIA NELLA LEGGE DI QUESTA SCHEDA:** cambia solo una frase che
### **asseriva la legge di un'altra** — e un commento che resta condizionale dopo la cura
### **sarebbe scaduto il giorno stesso.** ### ✅ **E resta vero cio' che il pavimento
proteggeva:** `d <= 0` si **CONTA** *(`_pozzo_d_nonpos`, `A8`)* invece di assumerlo
impossibile *(`A11`)*.


> ### ⛔ **NOTA DEL 2026-09-28 (`PSI-FLASH`): `_nb_grav` NON RIPIEGA PIU' IN SILENZIO.**
> Quando `psi_spin` era piu' corta di `n` restituiva **`self._nb`** invece del Bloch **nativo**
> del campo emesso: ### **un'ALTRA DIREZIONE, e la direzione entra nella GRAVITA'**.
> ⚠ **MISURATO: su questa scena NON SCATTA MAI** nella finestra della nascita, quindi la riga
> e' **byte-inerte** qui -- **il sigillo non potra' dimostrare che serve, solo che non rompe.**
> **Ora solleva `CacheCorta`**, e la cache va **estesa alla nascita** (`_eredita_psi_figli`), non
> allungata dove la si legge. *(La legge sta nella scheda `schermatura-nucleo-nudo`.)*
# ③ LA GRAVITA' BIFASE — **`GRAV_BIFASE` / `S09_spinta_med` / `S10_grav_med`**

> **STATO: `DIFETTOSA`.** Difetti **`D01`** e **`D02`**. **Viola `A2`, `A5` e `A11` cor. 6.**
> ### ⚠ **`D02`: IL DISEGNO ENTRA NELLA GRAVITA', e la cura e' `POZZO_D`** *(2026-09-27)*.
> **`pozzo_grafo` calcolava `L` da `self.pos`** — *il DISEGNO* — **e il risultato entra nella
> spinta `S09`.** E **il docstring della funzione dichiara l'opposto**: *«diviso per la
> DISTANZA REALE DELL'ARCO»*. **La distanza reale dell'arco e' `self.d`.**
> ### ❗ **CORREZIONE DI ETICHETTA, 2026-09-27 (rilievo di Luca): la regola e' `A3-DISEGNO`, NON `A13`.**
> **Avevo citato `A13`, che e' *«`LAM` e' la scala di Planck del sistema»*.** La regola che
> dice **«il disegno esce dalla dinamica: `pos` non entra nella fisica»** e' **`A3-DISEGNO`**.
> **Non e' un dettaglio:** un'etichetta sbagliata **manda chi legge a cercare la regola nel
> posto sbagliato**, e in un repo dove le regole si citano per nome quella e' la forma piu'
> facile di errore silenzioso. **L'etichetta vecchia resta leggibile, con cio' che l'ha
> corretta** *(stessa convenzione dei marchi storici: si legge com'era e cosa l'ha cambiata)*.
> ### ✅ **ACCESA NEL DRIVER DAL 2026-09-27** *(decisione di Luca, dopo `W5`)*.
> **E' una scelta DI PRINCIPIO, non sostenuta da un effetto misurato, e la decisione lo dice:**
> **`W4` DIMOSTRA** che `pos` non entra piu' *(muovendo **solo** `pos` il pozzo non cambia
> di un bit: `0.000000e+00` esatto; a flag spento cambia di `5.38e+02`)*; **`W5` dice che a
> 120 passi l'effetto sulla distanza fra le masse e' SOTTO l'`1.3`-`2.7 %`**, cioe' **NON MISURATO**
> *(IC95 che contengono lo zero su tutte e tre le coppie, segni non concordi)*.
> **`A3-DISEGNO` basta da sola:** si misura per PROMUOVERE, **si DIMOSTRA per ESCLUDERE**.
> **NON e' byte-inerte**, e i numeri di prima non si confrontano con questi *(par.9-bis)*.
>
> **LA CURA, derivata e senza coefficienti:** `L = self.d[mask]`, dietro **`POZZO_D`**
> *(`--pozzo-d`, **spento di default**)*. **`STANDARD 10`: si TOGLIE una dipendenza (`pos`),
> non si aggiunge una legge.**
> **E IL PAVIMENTO `1e-9` ESCE dal ramo acceso**, perche' `d >= LAM` con
> `SEMINA_LAM`/`MITOSI_2LAM` — **⚠ ma quella e' una MISURA (`D11`), non un'invariante del
> codice**, quindi i casi `d <= 0` **si CONTANO** *(`_pozzo_d_nonpos`, `A8`)* invece di
> assumerli impossibili *(`A11`)*. **Il contatore nasce SOLO nel ramo acceso**, cosi' la
> byte-identita' a flag spento resta vera.
> **⚠ E TOCCA SOLO `pozzo_grafo`:** le altre due letture di `pos` in `memoria_hebbiana_moto`
> *(`:6590`, `:6978`)* sono **DIREZIONI**, non lunghezze, e sono **`D03`** — un altro fronte.
> **Un flag che le cambiasse insieme misurerebbe due cose** *(par.1)*.
> **Criteri e sigillo:** `doc/TASK_HISTORY/2026-09-27_d02-pozzo-d.md`,
> `csv/_seal_fork/_sigillo_pozzo_d.py`. **`W5`** *(A/B a 4 semi)* **decide se accenderla.**
> **NON è il motore della fuga di `d0`** *(`Z107`: spegnendola il rapporto passa da `1.2321` a
> `1.2211`, lo `0.9 %`)*, **ma è il maggior scrittore in ampiezza**: `±2.5e+06`–`3.7e+06`
> per 600 passi.

## LA FORMA — copiata dal codice (`:5766-5850`)

```
grav      = -tanh(s) * ampiezza                       s = |tw|/PHI_CRIT - 1, FIRMATA
                                                      -s = il VERSO (attrae / respinge)
se SPINORE:  grav = grav * (nb_g[ii]·nb_g[jj]) * sign(dpozzo)     <- proiezione spinoriale

c_sistema      = LAM * sqrt(K_C)                      velocità del cono, da LAM e K_C
passo_causale  = c_sistema * DT                       IL TETTO

se VIRIALE:  radiale  = grav * cos2
             tangenz  = |grav| * sin2 * sign(circ_arc)      (o `_azim` se LS_AZIM)
             spinta   = radiale + tangenz
             spinta   = clip(spinta, ±passo_causale)
             d0[mask] += _sd0(spinta * median(d0[mask]), mask)        <- `S09_spinta_med`
altrimenti:  grav     = clip(grav, ±passo_causale)
             d0[mask] += _sd0(grav * median(d0[mask]), mask)          <- `S10_grav_med`
```

## DA DOVE VIENE

**Il verso è DERIVATO:** `s = |tw|/PHI_CRIT - 1` è lo scarto dal **quanto di olonomia**, e il
segno di `-tanh(s)` dice se l'arco è sotto o sopra il giro completo. **Bifase: attrae da una
parte, respinge dall'altra, e la soglia è `PHI_CRIT`, che esisteva già.**
**`NON RICOSTRUITO`:** perché `tanh` e non un'altra saturazione; perché la scomposizione
radiale/tangenziale usi `cos2`/`sin2` di quell'angolo.

## LE DIMENSIONI — **e qui c'è il difetto**

| simbolo | dimensione |
|---|---|
| `s`, `tanh(s)`, `ampiezza`, `cos2`, `sin2`, `proiez` | adimensionale |
| **`grav`, `spinta`** | **adimensionale** |
| `c_sistema = LAM·√K_C` | `[L/T]` |
| **`passo_causale = c_sistema·DT`** | **`[L]`** |
| `spinta * median(d0)` | `[L]` |

> **⚠ `spinta` VIENE CLIPPATA A UNA LUNGHEZZA E POI MOLTIPLICATA PER UN'ALTRA LUNGHEZZA.**
> Dopo il clip `spinta` ha unità `[L]`; moltiplicarla per `median(d0)` dà **`[L²]`**, che viene
> sommato a `d0` — **`[L]`**. **È `D01`, e la scheda lo rende esplicito:** *«clippa al passo
> causale — quindi è già una LUNGHEZZA — e poi moltiplica per `median(d0)`: statistica GLOBALE
> e lunghezza AL QUADRATO»*.

## COSA LEGGE / COSA SCRIVE

- **legge:** `tw`, `pozzo_grafo` → `dpozzo` *(che usa `pos`, il **DISEGNO** — `D02`)*,
  `_nb_grav()`, `median(d0[mask])` *(**globale** — `A2`)*, `LAM`, `K_C`, `DT`.
- **scrive:** `d0` a **`S09_spinta_med`** *(ramo `VIRIALE`)* oppure **`S10_grav_med`**.
  **I due rami sono esclusivi:** in tutti i run del fork gira `S09`, e **`S10` è inerte**
  *(`Z102`)*.
- **flag:** `GRAV_BIFASE` *(sigillo `7/7`, `G3`)*.

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `clip(spinta, ±passo_causale)` | **1** | ✅ **causalità**: `c_sistema` viene da `LAM` e `K_C`, non è scelto |
| | **2** | ✅ costante, non insegue `d0` |
| | **6** | ❌ **VIOLATO: `85.05 %` degli archi-passo INCOLLATO AL TETTO**, e il **`99.69 %`** del saldo viene da incrementi **saturi** *(`Z106`)*. **Non è un limite: è la legge**, e nessuno l'ha scelta |
| | **5 (A5)** | ⚠ `c_sistema` è costruito su **costanti di modulo** e **non conosce il cono del LUOGO** — lo stesso difetto che `COES_CAUSALE` ha curato per la coesione |

## LO STATO: `DIFETTOSA` — **e dove spinge, misurato**

- **il saldo netto vive SUL CONFINE vuoto-massa e TIRA GIÙ:** `-1.4150` per arco, il **`107 %`**
  del totale *(`Z105`)*;
- i **20 archi** col `|saldo|` maggiore sono **`20/20` nel VUOTO**, e il confine è **DIFFUSO** su
  **`96 429`** archi all'**`85 %`** del plateau;
- saldo su 600 passi: **`-1.901e+05`** *(braccio acceso)*, **`-2.598e+05`** *(senza memoria del
  moto)* — **il maggior scrittore in ampiezza, e tira GIÙ.**

## LE DOMANDE APERTE

1. **Se il `99.69 %` del saldo viene da incrementi saturi, che legge sta girando davvero?**
   Quella scritta, o **`spinta = passo_causale · sign(...)`**? *(`A11` cor.6.)*
2. **Il tetto è GLOBALE mentre `COES_CAUSALE` ha reso locale quello della coesione.**
   Perché non qui? È la stessa `A5`.
3. **`median(d0[mask])` è una statistica globale dentro una legge che si dichiara locale.**
   `SPINTA_LOCALE` è la cura derivata — **e deve risolvere anche il `[L²]`.**

---

<!-- SCHEDA nome=coesione funzioni= flag=COES_ADIM,COES_CAUSALE,K_C -->
# ④ LA COESIONE — **`COES_ADIM` / `COES_CAUSALE` / `S12_coesione`**

> **STATO: `DA VERIFICARE`.** Il difetto **`D18`** *(istanti misti e tetto globale)* è
> **`CURATO`** da `COES_CAUSALE` *(`C4`, sigillo `5/5`)*, e la forma adimensionale da `COES_ADIM`.
> **È l'unica delle quattro che arriva alla scheda già curata.**

## LA FORMA — copiata dal codice (`:5939-6032`)

```
coesione_relazionale = scala_statale * (forza_campo + richiamo_elastico)
                       * filtro_portata * d0[mask]**2 * (I_arco/I_med)
tasso_dinamico       = tanh(stress_metrico) * d0[mask]

se COES_ADIM:   _delta_coes = _passo_causale * _F_adim          |_F_adim| <= 1 PER COSTRUZIONE
                d0[mask] += _sd0(_delta_coes, mask)
altrimenti:     d0[mask] += _sd0(clip(coesione_relazionale, ±tasso_dinamico), mask)
                                                                 <- il ramo STORICO
se COES_CAUSALE: _passo_causale = cs_arco * DT      <- il cono LOCALE, col `cs` del nodo PIÙ LENTO
altrimenti:      _passo_causale = LAM*sqrt(K_C)*DT  <- costanti di MODULO
```
**⚠ I due rami di `COES_ADIM` sono MUTUAMENTE ESCLUSIVI e condividono UN solo sito di traccia**
— ed è la coppia che ha prodotto il falso positivo di `Z114`.

## LE DIMENSIONI — **coerenti, ed è la cura che le ha rese tali**

| simbolo | dimensione |
|---|---|
| `_F_adim` | **adimensionale**, e `|_F_adim| <= 1` **per costruzione** |
| `_passo_causale = cs_arco·DT` | **`[L]`** |
| `_delta_coes` | **`[L]`** ✅ |

> **È l'unica delle quattro leggi in cui l'incremento ha le unità giuste SENZA che un clip
> gliele dia.** *(Confronta: `proj` della memoria del moto — adimensionale; `spinta` della
> gravità — `[L²]`.)*

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `_passo_causale = cs_arco·DT` | **1** | ✅ **causalità LOCALE**: `cs` del nodo più lento, zero parametri |
| | **2** | ✅ non insegue `d0` |
| | **6** | ⚠ **i contatori ESISTONO** *(`_g_cct_stringe`, `_g_cct_allarga`, `_g_cct_archi`, `_g_cct_min`)* **ma la frazione non è in nessun referto**. **Lavoro residuo.** Il massimo misurato è `0.2384`, **e un MASSIMO non dice QUANTO SPESSO** |
| | **7(a)** | ✅ `|_F_adim| <= 1` per costruzione: non è un clip, è un **dominio** |

> **E il tetto locale NON è sempre più stretto:** dove il cono è veloce **ALLARGA**. **È
> causalità, non prudenza** — e va detto, perché la lettura sbagliata *(«una cura che
> restringe»)* circola facile.

## LO STATO: `DA VERIFICARE` — **e quanto pesa**

saldo su 600 passi: **`-1.025e+05`** *(braccio acceso)*, **`-1.064e+05`** *(senza memoria del
moto)*. **Tira GIÙ, come tutti gli scrittori fisici.**

## LE DOMANDE APERTE

1. **Quante volte il tetto causale morde?** ### ✅ **MISURATO il 2026-10-04**,
   `doc/REFERTO_tetto_causale_tempo_2026-10-04.md`: il clip di `spinta` limita
   **`26 666 143`** archi-passo su **`30 651 762`**, e il tetto locale della coesione
   **allarga** su `24 476 351` e **stringe** su `6 175 411` rispetto al globale.
   ### ⚠ **Ma su `83` passi su `150` quella misura e' INVALIDA**, e la causa e'
   `VELENO-ARCHI-KEEP` — ### **curata il 2026-10-05**.
   ### 📌 **E DOPO LA CURA GLI ARCHI NATI NEL PASSO HANNO `dt_e = NaN`:** il passo (2)
   del tetto, che vuole far leggere `dt_e` a `memoria_hebbiana_moto` *(voce 5, DOPO la
   nascita)*, ### **avra' bisogno di una REGOLA per loro — DECISIONE DI LUCA, da
   prendere ALLORA e non adesso.**
2. **`scala_statale`, `forza_campo`, `richiamo_elastico`: da dove vengono?** **`NON RICOSTRUITO`**
   in questa scheda — vanno lette dal codice che le costruisce, e non l'ho fatto.
3. **Il ramo storico** *(`COES_ADIM = False`)* **è ancora raggiungibile.** Se non serve più,
   è codice morto che complica l'appaiamento delle tracce *(`Z114`)*; se serve, **cosa lo
   giustifica?**

---

<!-- SCHEDA nome=tempo-proprio funzioni=ritmo,_cli,_applica_flag flag=TAU_LOC,TEMPO_SEGNO,TEMPO_PROPRIO_ORIENTATO,RITMO_WRAP_2PI -->

> ### ⚠ **ANNOTAZIONE DEL 2026-10-06: IL MESSAGGIO DI `--chi-basc` NOMINAVA L'ARRAY
> SBAGLIATO** *(`CHI-BASC-DESCRIZIONE`, decisione di Luca)*. Diceva *«`perc_chi` vira
> secondo la torsione locale»*, e ### **col driver** — che ha `--chi-coop` —
> ### **e' `perc_geom` che viene scritta** *(`:7905`)*. ### **MISURATO: `6419` cambi di
> `perc_geom` e ZERO di `perc_chi` in `4` passi.**
>
> Ora il messaggio dice ### **entrambi i casi**: la media di `|tw|` sugli archi del nodo
> contro `PHI_CRIT`, e ### **scrive `perc_geom` (la GEOMETRIA) con `--chi-coop`, `perc_chi`
> (la CARICA) senza.**
>
> ### ⛔ **E' SOLO UNA STRINGA: il codice compilato e' IDENTICO**, e il sigillo `K0` lo
> verifica confrontando i ### **code object di tutto il modulo, ricorsivamente.**


### **AGGIORNAMENTO del 2026-10-04, commit `6b`** *(questa scheda possiede
`_applica_flag`)*: **l'avviso `[cura5]` e' stato TOLTO da `_applica_flag`.** Annunciava
*«`MITOSI_2LAM` ON: un arco si divide SOLO se `d >= 2 LAM`»* ### **come se fosse il flag a
deciderlo**; dal `6b` la legge vale **sempre** e il flag e' **inerte**, quindi quell'avviso
### **direbbe il falso.** L'annuncio lo da' ora il blocco `[flag-inerti]`
*(scheda `leggi-in-uso`)*. ### **La legge e' nella scheda `mitosi-schwinger`.**


> **→ NOTA DEL 2026-09-29, e sta qui perche' questa scheda POSSIEDE `_cli` e `_applica_flag`:**
> un flag nuovo, ### **`CONTROLLO_REGISTRO`** *(`--senza-controllo-registro`)*, si parsa in
> `_cli` e si applica in `_applica_flag`, ### **con la `global` dichiarata nella stessa
> funzione** — senza, nascerebbe **morto**, ed e' come `--tau-a`, `--semina-matura` e
> `--mitosi-2lam` sono stati inerti per un giorno intero **coi loro sigilli che passavano**.
> ### ⚠ **E il suo DEFAULT e' ACCESO, al contrario di tutti gli altri:** il flag **SPEGNE**.
> **Il TEMPO PROPRIO non cambia:** quel flag riguarda **il registro delle grandezze**, e la
> sua legge sta nella scheda **`registro-grandezze`**. Qui sta solo il passaggio dal CLI.

> **-> NOTA DEL 2026-09-28, e sta qui perche' questa scheda POSSIEDE `_cli`: NESSUNA
> LEGGE E' CAMBIATA.** Il commit di `MAX-NODI-FERMA` tocca **il solo testo di `help`** di
> `--maxnodi`, per dire che ora **ferma il run** invece di troncare. **Il default resta
> `4000000`.** *(La legge sta nella scheda `guardia-max-nodi`.)*

> **→ NOTA DEL 2026-09-25, e sta qui perche' questa scheda POSSIEDE `_cli` e `_applica_flag`:**
> un flag nuovo, **`CONTRASTO_INTENSIVO`** (`--contrasto-intensivo`), si parsa in `_cli` e si
> applica in `_applica_flag`, **con la `global` dichiarata nella stessa funzione** — senza,
> nascerebbe **morto**, ed e' come `--semina-matura` e `--mitosi-2lam` sono stati inerti per un
> giorno intero coi loro sigilli che passavano.
> **Il TEMPO PROPRIO non cambia**: quel flag riguarda **l'inerzia**, e la sua legge sta nella
> scheda **`inerzia-spinoriale`**. Qui sta solo il passaggio dal CLI.

> ### ➜ **`CURA 2` PASSA DI QUI, e questa scheda deve dirlo** *(2026-09-24, blob `b881db89`)*
>
> `_cli` e `_applica_flag` acquisiscono **`--tempo-unico-mitosi`** *(con `TEMPO_UNICO_MITOSI`
> nel `global`, come `RITMO_WRAP_2PI`: senza, l'assegnamento creerebbe una locale e il flag
> sarebbe **silenziosamente inerte** — il difetto documentato di `--tau-a`)*. **La legge sta in
> scheda ⑨**; qui resta il rimando, perché `REG-R` mappa **per funzione**.
>
> **➤ E `SEMINA_LAM` passa di qui allo stesso modo** *(2026-09-24)*: `--semina-lam` in `_cli`,
> la riga in `_applica_flag`, e **`SEMINA_LAM` nel `global`** — senza il quale l'assegnamento
> creerebbe una locale e il flag sarebbe **silenziosamente inerte**. **La legge sta in scheda
> ⑫.**
>
> **⚠ E C'È UN LEGAME DI SOSTANZA, non solo di funzione: `CURA 2` prende il suo orologio da
> QUI.** `_r_nodo_mitosi` legge `_r_corrente`, cioè l'`r` che **`ritmo()` di questa scheda
> produce**; e il `tau_nodo` che la cura **sostituisce** è **identico al ramo `TEMPO_SEGNO`**
> — un ramo di **questa** scheda **che non gira** *(`Z130`)*. **La mitosi usava come «tempo
> proprio» la definizione di tempo che il resto del sistema ha SCARTATO.**

> ## ✅ **`RITMO_WRAP_2PI` È APPROVATA — decisione di Luca, 2026-09-24**
>
> **Da oggi il driver la accende in OGNI run** *(`--ritmo-wrap-2pi`, cablato in
> `csv/_test_fork/_scena_video.py`)*. `D34` passa da **difetto aperto** a **CURA IN CODICE**.
>
> **Che cosa è stato aggiunto**, perché fino a oggi la cura era accendibile **solo
> in-process**: l'opzione **`--ritmo-wrap-2pi`** nel simulatore e la riga corrispondente in
> `_applica_flag` *(con `RITMO_WRAP_2PI` nel `global`: senza, l'assegnamento creerebbe una
> **locale** e il flag resterebbe **inerte in silenzio** — è il difetto già catalogato di
> `--tau-a`)*.
>
> **⚠ E NON È BYTE-INERTE, ed è il punto:** è una **cura**, non un'opzione. **I numeri presi
> prima di oggi non si confrontano con quelli di dopo senza dirlo** *(par.9-bis)*, e lo stato
> effettivo di ogni run sta in `CONFIGURAZIONE.txt`.
>
> **Il default nel sorgente resta `False`**, come per tutte le cure non ancora in epoca 3: chi
> vuole il braccio di confronto **omette il flag**, e il referto lo mostra.
# ⑤ IL TEMPO PROPRIO — **`ritmo()` / `r` / `dt_n = DT·r`**, e il surrogato **`tau_pp`**

> ## ✔ **LA LEGGE DI OGGI, dal 2026-10-05:** `r = cs_nodo / CS_M`
>
> ### **LA FORMA**
> ```
> r_i(t) = cs_i(t-1) / CS_M                  esponente p = 1
> ```
> dove `cs_i` e' la **velocita' delle onde metriche** nel nodo, quella che `_cs_nodo` gia'
> calcola come **unica fonte** della legge `cs_eff(rho)`, letta dalla **cache del passo
> PRECEDENTE** *(`_cs_nodo_prev`)*.
>
> ### **LA DERIVAZIONE** *(non una taratura: `A1`)*
> **Un tic e' il TEMPO DI ATTRAVERSAMENTO.** Il modello ha gia' un tempo costruito cosi' --
> il **tempo-luce** `tau = d/cs` -- e il tempo proprio e' **la stessa cosa adimensionata**:
> il rapporto fra la velocita' di propagazione nel luogo e quella nel vuoto.
> ### **L'esponente `p = 1` NON E' SCELTO: e' quello che rende `r` e `tau` LA STESSA
> ### GRANDEZZA.** Con `p != 1` sarebbero due tempi diversi costruiti da due leggi diverse,
> ed e' esattamente l'eccezione che questa cura **toglie** *(`9-ter`)*.
>
> ### **IL PERCHE'** *(e il perche' la legge di prima era sbagliata)*
> La legge di prima prendeva `r` dalla **frequenza d'interferenza della fase**, normalizzata
> sulla **MEDIANA GLOBALE** di `|f|`. Tre cose non tornavano:
> 1. ### **un gauge GLOBALE in un modello RELAZIONALE:** la mediana su tutta la rete decideva
>    il ritmo di ogni nodo;
> 2. ### **la fase non e' un orologio:** `Delta(angle psi)/DT` e' una frequenza
>    d'**interferenza**, e il campo che la porta e' quello **EMESSO** dai vicini;
> 3. ### **un ANELLO:** `f -> r -> f`. Curato nel 2026-09-18 **sfasandolo di un passo**, ma
>    ### **lo sfasamento non ha eliminato l'altalena: l'ha SMORZATA** *(referto `3edb7dd`,
>    corretto in `b337ec1`: il rapporto per coppia resta sopra `1.2` fino al passo `42`)*.
>
> ### **I LIMITI, che la forma garantisce**
> * `r ∈ (0, 1]`, e **non per un clip**: `_cs_nodo` restituisce
>   `cs_floor + (CS_M - cs_floor)*transizione` con `transizione = 0.5*(1 + tanh(1 - u))` e
>   `u = I/media_vicini >= 0`, quindi ### **`transizione <= 0.880797` e NON PUO' ARRIVARE A 1**;
> * da cui `cs = CS_M`, cioe' **`r = 1` ESATTO**, ### **SOLO dove `I = 0`** -- in una rete di
>   materia **non esistono nodi con `r = 1`**, e il tempo proprio e' **piu' lento** di quello
>   coordinato **ovunque ci sia qualcosa**. ### **E' il verso giusto.**
>
> ### **CHE COSA QUESTA LEGGE TOGLIE** *(il conto di `9-ter`: scende)*
> **QUATTRO leggi pratiche:** la saturazione `x/sqrt(1+x^2)`, il tetto `1.414212977`, il
> pavimento `1.414e-06`, il pavimento `1e-9` sul gauge. **UNA manopola:** `TAU_LOC` come
> **ampiezza** *(a `1.0` era un **passante**: `1 + 1.0*(x-1) = x`)*. **UN gauge globale.**
> **E UN'ECCEZIONE:** `r` e `tau` non sono piu' due tempi costruiti in due modi.
>
> ### ⚠ **MA NE APRE UNA CHE VA DETTA, ed e' il punto scomodo:** `cs` porta
> `_Lam = mean(|psi|^2)` su **TUTTA la rete** *(`CS-LAMBDA-GLOBALE`)*. ### **Quindi da questa
> cura IL TEMPO DI OGNI LEGGE LOCALE LEGGE UNA MEDIA GLOBALE** -- non piu' una **mediana**
> di fasi, ma ancora una media. ### **Il criterio di LOCALITA' del sigillo lo MISURA invece di
> presumerlo**, con atteso `~1/n` e **non zero**.
>
> ### **L'ANELLO, che resta e si sposta**
> `cs -> r -> dt_e -> cs`: `cs` dipende da `r` attraverso i sotto-passi della metrica, e ora
> `r` dipende da `cs`. ### **Passa per la cache del passo PRECEDENTE**, quindi e' sfasato di
> uno e **non viola `A6`** -- ed e' **la stessa forma che produceva l'altalena**. Per questo il
> sigillo misura l'**autocorrelazione a ritardo 1** della mediana di `r`: se quell'anello
> oscilla, ### **si ferma e si riporta.**
>
> **DOVE:** `ritmo()` del simulatore. **IL RAMO DI PRIMA:**
> `csv/_archivio/_rami_off_z43_cura2.py`, tag `pre-z43-cura2-r-da-cs`, blob `062172d3`.
> **IL SIGILLO:** `csv/_seal_fork/_sigillo_z43_cura2.py`, **sette criteri**.
> **LA DECISIONE:** di Luca, 2026-10-05, in
> `doc/TASK_HISTORY/2026-10-05_z43-cura2-r-da-cs.md`.
>
> ### ⚠ **E DUE FLAG PERDONO QUI IL LORO UNICO CONSUMATORE FISICO**, e **non sono stati
> ### tolti**, perche' toglierli sarebbe estendere la cura da soli:
> * **`RITMO_WRAP_2PI`** -- la cura `D34`, che avvolgeva su `2pi` la differenza di `np.angle`.
>   ### **Era una cura SIGILLATA** *(`_sigillo_ritmo_wrap.py`, 4/4)*, e **la sua misura resta
>   vera**: diceva che il wrap su `4pi` era l'identita'. ### **Ma la legge che curava non c'e'
>   piu'.**
> * **`TEMPO_PROPRIO_ORIENTATO`** -- il segno di `f`.
>
> **Dopo questa cura `r` NON LEGGE LA FASE**, quindi non c'e' piu' niente da avvolgere ne' da
> orientare: restano **accettati dal CLI** e **INERTI nella fisica**. ### **La loro sorte e'
> una decisione di Luca, non mia.**
>
> ### ⚠ **E UN SIGILLO DIVENTA STORICO:** `csv/_seal_fork/_sigillo_anello.py` **asserisce
> ### che `step()` PROMUOVA il gauge**. Da questo commit **FALLISCE a `HEAD`, e DEVE** --
> sigilla una legge che non esiste piu'. **Si rigira AL SUO COMMIT** *(par.6)*.


> ### 🗄 **(b)2, 2026-09-27: `--sync` si dichiara no-op, e un avviso cade**
>
> **`SYNC_UPDATE` e' un NO-OP ACCETTATO dal 2026-09-27** *(passo `(b)2` di `ETC-PASSO`)*: i
> suoi rami sono in **`csv/_archivio/_sync_update.py`**, tag **`pre-archivio-sync`**, e `--sync`
> si accetta senza fare niente. **Il suo raggio era UNA legge su cinque** -- `7` usi in
> `_passo_spinoriale`, `6` in `step`, **ZERO** nelle altre quattro -- e **tutte e 56 le letture
> miste `t`/`t+1` misurate nella FASE 0 stavano FUORI da quel raggio.**
>
> `_applica_flag` stampava *<<aggiornamento sincrono attivo: dph legge la fase dallo snapshot
> t-1 (Jacobi)>>*. **Ora dichiara di non fare niente.**
> **E un secondo avviso e' caduto col ramo:** quello di `--rumore-colorato`, che diceva di
> agire <<solo sul percorso VIVO (`not SYNC_UPDATE`)>> e di essere quindi **inerte sotto**
> `--sync`. **Ora il percorso vivo e' l'UNICO**, quindi il rumore colorato agisce **sempre** e
> quell'avviso **non ha piu' oggetto**. *(Sostituito da un commento che dice perche'.)*


> ### 🗄 **(b)1, 2026-09-27: `_applica_flag` non annuncia piu' una legge che non applica**
>
> Il messaggio d'avvio di `PAV_COM` diceva *<<pavimento comovente attivo: d0 >=
> median(d0)-MAD(d0) invece di 0.05 assoluto>>*. **Quel pavimento e' ARCHIVIATO**
> (`csv/_archivio/_pavimenti_morti.py`), quindi il flag **e' INERTE in entrambi i suoi stati**
> e ora lo **dichiara**. **`PAV_COM` non e' stato TOLTO** *(decisione 3: si conserva tutto)*, e
> il driver lo passa ancora. **Nessuna legge del tempo proprio e' toccata:** cambia solo cio'
> che `_applica_flag` **dice** di se stesso, ed e' `A8` -- un ramo che annuncia un effetto che
> non produce e' un ramo silenzioso al contrario.


> **STATO: `DIFETTOSA`.** Difetto **`D34`** *(il wrap «a `4π`» non avvolge)*.
> **→ NOTA DEL 2026-09-27 (`D02`): `_applica_flag` e `_cli` hanno UN FLAG IN PIU', `POZZO_D`,
> e NON tocca il tempo proprio.** E' la cura di `D02` *(la lunghezza del pozzo dal grafo e
> non dal disegno)*, e la sua scheda e' **③ `gravita-bifase`**, dove vive `pozzo_grafo`.
> *(Questa nota esiste perche' `H-REG-R` ha chiesto questa scheda: `_applica_flag` e `_cli`
> sono elencate qui, e **ogni** flag nuovo le tocca. **Ha fatto bene a chiederla** — dal diff
> non si vede a quale legge appartenga una riga di `argparse`.)*
>
> **✅ E DAL 2026-09-27 `_applica_flag` NON ASSEGNA PIU' `TEMPO_UNICO_MITOSI`:** la `CURA 2`
> e' **strutturale** *(scheda ⑨)*, quindi qui non c'e' piu' un interruttore da applicare.
> **Il `global` resta**, e non fa danno: nessuno assegna piu'.
> **✅ `D32` E' RISOLTO — decisione di Luca del 2026-09-27:** **il tempo proprio del sistema e' `r`**
> *(e `dt_e = DT·0.5·(r_i + r_j)` sull'arco)*; **`d/cs` e' il TEMPO-LUCE**, una grandezza **diversa
> e legittima**, non un secondo tempo proprio; e cio' che si chiamava **`tau_pp` non e' un tempo
> affatto**: e' una **POSIZIONE sull'asse della torsione**, `1 + avv/PHI_CRIT`, un numero puro.
> **Rinominata `pos_torsione`** *(sigillo byte-identico: i nomi non cambiano un bit)*.
> **I TRE «TEMPI PROPRI» ERANO TRE GRANDEZZE, e ora hanno tre nomi:** `r` il tempo proprio,
> `d/cs` il tempo-luce, `pos_torsione` una posizione. **Il difetto non era che fossero diverse:
> era che si chiamassero allo stesso modo.** *(`Z117`, il pavimento del ritmo, resta APERTA a parte.)*
> **È la grandezza da cui dipende il tic di OGNI processo locale** *(par.9: `dt_n = DT·r`, e
> `DT` nudo dentro un rilassamento locale impone un frame preferito, cioè un etere)*.

## LA FORMA — copiata dal codice (`:2536-2646`)

```
se TEMPO_SEGNO:                                 <- OGGI `False`: questo ramo NON gira
    r = 1 + mean(|tw| sugli archi incidenti)/PHI_CRIT
altrimenti, il ramo DE BROGLIE, che e' quello che gira:
    a      = angle(psi) - angle(psi_prec)
    signed = ((a + pi) % (2 pi) - pi) / DT                    <- ramo SCALARE: periodo 2pi
    se CAMPO_SPINORIALE e psi_spin e' allineato:
        a      = angle(psi_spin[:,0]) - angle(psi_spin_prec[:,0])
        signed = ((a + 2 pi) % (4 pi) - 2 pi) / DT            <- ramo SPINORIALE: `D34`
    f    = signed  (o |signed| se non TEMPO_PROPRIO_ORIENTATO)
    med  = median(|f|) del passo PRECEDENTE                   <- gauge SFASATO (cura dell'anello)
    x    = f / med
    r    = x/sqrt(1 + x^2) + 1e-6                             <- SATURA a ~1
    r_n  = r / (1/sqrt(2) + 1e-6)                             <- x=1 -> 1
    ritorna 1 + TAU_LOC*(r_n - 1)
```
**E IL SURROGATO, che e' un'ALTRA legge (`:5160`):** `tau_pp = 1 + |tw|/PHI_CRIT`, **per ARCO**,
usato da **mitosi**, **repulsione** e dalla memoria `_rep`.

## ⚠ IL CODICE CONTIENE IL PROPRIO CONTROESEMPIO

**Il ramo SCALARE avvolge su `2π`. Il ramo SPINORIALE, OTTO RIGHE DOPO, su `4π`.**
**Stessa grandezza, stesso significato, due periodi diversi, nella stessa funzione.**
E il commento di `:2566-2568` dichiara l'equivalenza **con la sua condizione**:
*«nel limite `psi_spin[:,0] = psi` e **`|dphi| < pi`** → ritmo IDENTICO»*.
**`|dphi| < pi` e' ESATTAMENTE la condizione in cui il taglio non si attraversa.**
**Il commento sapeva già dove sta il difetto, e nessuno ha letto la condizione come un
avvertimento.**

## LE DIMENSIONI

| simbolo | dimensione |
|---|---|
| `a`, `signed·DT` | **angolo** — adimensionale |
| `signed`, `f`, `med` | `[1/T]` |
| `x = f/med`, `r`, `r_n` | **adimensionale** ✅ |
| `dt_n = DT·r` | `[T]` ✅ |
| **`tau_pp`** | **adimensionale** — *si chiama «tempo proprio» ma NON ha dimensione di tempo* |

> **`A3c`: `r` e `tau_pp` sono ENTRAMBI adimensionali, quindi CONFRONTABILI** — ed è
> precisamente per questo che `D32` è un difetto e non un equivoco di notazione: **due numeri
> puri con lo stesso nome fisico e correlazione `~0`.**

## COSA LEGGE / COSA SCRIVE

- **legge:** `psi`, `_psi_prec`, `psi_spin`, `_psi_spin_prec`, `_med_f_prec`, `tw` *(solo nel ramo
  `TEMPO_SEGNO`, che non gira)*.
- **scrive:** `_med_f_ultimo` *(registro, promosso da `step()`)*, e **`_r_corrente`** — che
  **`step()`** salva. **`ritmo()` non scrive nessuno snapshot**, di proposito: ha **tre**
  chiamanti e **due sono DIAGNOSTICI**; se avanzasse lo stato qui, ogni chiamata diagnostica
  muoverebbe la fisica *(par.2.3)*.
- **a valle:** `dt_n = DT·r` — **il tic di ogni processo locale**.

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `+1e-6` in `r = x/√(1+x²) + 1e-6` | **1** | ❌ **numero SCELTO**, non un vincolo fisico |
| | **2** | ✅ costante |
| | **6** | ⚠ **e' un PAVIMENTO che MORDE:** `min(r) = 1.414212e-06` **misurato**, cioè **esattamente il pavimento** *(`Z117`)*. **Quando `f ≈ 0` il tempo proprio del nodo NON si ferma: si ferma AL PAVIMENTO** |
| `max(median(|f|), 1e-9)` | **1** | ⚠ difesa dalla divisione |
| la saturazione `x/√(1+x²)` | **7(a)** | ✅ identità per `x ≪ 1`; **e non è un `clip`: è liscia ovunque**, derivata continua |

> **⚠ E IL «RAPPORTO `max/min` = `1.000e+06`» NON È UNA MISURA:** è `1.4142 / 1.4142e-6`,
> cioè **`1/1e-6`, l'inverso della regolarizzazione**. **Correzione a una mia frase di `Z110`**,
> che lo chiamava *«il clip»*.

## LO STATO: `DIFETTOSA`

- **`D34`** — il wrap del ramo spinoriale. **Dimostrato:** `max|w4(a) − a| = 0.000e+00` su
  `100 001` punti. **Misurato raro:** `4.45e-05` dei nodi, `12` chiamate su `119`; **ma
  arricchimento `728.94 x` al tetto** e **gauge invariato** *(`1.000000`)*.
  **✅ CURA `RITMO_WRAP_2PI`, IN CODICE dal 2026-09-22** *(blob `21e3a3dc` → `3d91338e`)*,
  **spenta di default**. **Tocca UNA SOLA riga e SOLO il ramo spinoriale:**
  `signed = ((a + π) % 2π − π)/DT`, **la stessa forma del ramo scalare otto righe sopra**.
  **Il default NON si cambia qui:** è una decisione di Luca dopo la prova a 600 passi *(`E3`)*.
- **✅ `D32` — CHIUSO il 2026-09-27** *(decisione di Luca)*. La correlazione misurata fra `r`
  e `tau_pp` — **`-0.13`…`+0.29`, segno non concorde** — **non era un difetto di `r`: era la
  prova che le due grandezze non sono la stessa cosa**, e che chiamarle entrambe «tempo
  proprio» era il difetto. **`r` e' il tempo proprio; `pos_torsione` e' una posizione.**
  **VERIFICATO DAL SORGENTE:** con `TEMPO_UNICO_MITOSI` **acceso** *(il driver lo accende in
  ogni run)* i due usi come TEMPO — `1/tau_pp` come ritmo e `tau_pp` come costante di tempo
  di `_rep` — stanno **entrambi nel ramo `else`, che non gira**. Nel ramo attivo resta
  **solo** `segno = -tanh(3·(pos_torsione − centro))`: **il SEGNO, cioe' la posizione**.
  **⚠ I DUE USI NEL RAMO SPENTO CI SONO ANCORA, e sono PROPOSTI per la rimozione**
  *(`STANDARD 10`: si toglierebbe una legge, il ritmo finto `1/pos_torsione`, senza
  aggiungerne)* — **non tolti**, perche' quel ramo e' anche **il braccio OFF che rende
  misurabile la cura**, e toglierlo perderebbe la byte-identita' a flag spento *(par.2,
  punto 1)*. **Decide Luca.**

## LE DOMANDE APERTE

1. **✅ RISPOSTA, 2026-09-27: il tempo proprio NON si unifica, perche' non erano tre tempi.**
   Le righe sono state elencate una per una *(`csv/_patch_d32_nomi.py`, 24 sostituzioni
   asserite)*, e il risultato e' che **nel ramo attivo nessuna usa `pos_torsione` come
   tempo**. **Resta aperto SOLO che fare dei due usi nel ramo spento** — proposta sopra.
2. **Il pavimento `1e-6` è un vincolo o una difesa?** Oggi **morde**: `min(r)` è esattamente
   lui. **Un nodo con `f = 0` che tempo proprio ha?** *(Zero è una risposta fisica; `1.414e-6`
   è un numero scelto.)*
3. **⚠ L'ANELLO CHE `A6` TIENE D'OCCHIO, posto da Luca il 2026-09-22:** **l'orologio dello spinore si calcola dalla VARIAZIONE della fase dello spinore, e poi FA AVANZARE quella stessa fase.** `r` viene da `angle(psi_spin) − angle(psi_spin_prec)`; `dt_n = DT·r` entra nell'integrazione che **muove `psi_spin`**; al passo dopo `r` si rimisura da lì. **È un anello CHIUSO.**
   **NON è retroazione ISTANTANEA** — lo snapshot è **ritardato** *(`_psi_spin_prec` è del passo precedente, promosso da `step()`)*, **e questo lo mette fuori dalla lettera di `A6`**. **Ma è esattamente la forma che `A6` sorveglia**, e va scritto invece di essere dedotto ogni volta da capo.
   **NON DA CHIUDERE ORA.** La domanda è: *un orologio che misura sé stesso può derivare senza che nulla lo riporti indietro?* — e il candidato per deciderlo è la **dispersione di `r` a codice invariato fra semi**, che oggi **non è misurata**.
4. **Il gauge è `median(|f|)` del passo PRECEDENTE** — cura dell'anello istantaneo *(`A6`)*.
   **Ma resta una statistica GLOBALE dentro una legge per nodo** *(`A2`)*. **È accettabile
   perché è un GAUGE, o è lo stesso difetto di `D01`?** **NON DECISO.**

---


### ➕ DUE FLAG NUOVI IN `_cli`, PER LA SCENA `(ii)` *(2026-09-25)*

| flag | default | cosa fa | byte-inerte a default? |
|---|---|---|---|
| **`--mc-nodi N`** | **`0`** | nodi del vuoto della scena `(ii)`. **`0` = FINO A SATURAZIONE**: il numero lo decide la **geometria**, non una scelta. | **sì**: letto **solo** da `_semina_masse_coerenti`, che gira **solo** nella scena `MASSE-COERENTI` |
| **`--mc-fasi-casuali`** | **`False`** | **BRACCIO DI CONTROLLO DI `S10`**: fasi casuali **anche dentro** le regioni. **DIAGNOSTICO, non fisica alternativa.** | **sì**, stessa ragione |

> **Perché `--mc-nodi` esiste invece di lasciare sempre la saturazione:** il **braccio di
> controllo di `P-GONFIA`** gira con `SEMINA_LAM` **spenta**, e **senza distanza minima la
> saturazione non esiste**. Quel braccio deve ricevere **il numero MISURATO dal braccio acceso**,
> per avere **lo stesso `n`** — che è la condizione che rende il confronto attribuibile alla
> **sola** distanza minima.
> **Non è una manopola di fisica** *(par.10, categoria infrastruttura)*: non entra in nessuna legge.


### ➕ `CURA 4` AGGIUNGE `--semina-matura` in `_cli` / `_applica_flag` *(2026-09-25)*

| flag | default | byte-inerte a default? |
|---|---|---|
| **`--semina-matura`** | **OFF** | **sì**: `_tempo_rampa()` restituisce `TAU_A` e `semina` scrive `eta = 0`, cioè **le righe di prima**. Lo prova `A1` |

**La legge sta nella scheda `accensione-campo`.**

### ❌❌ `--semina-matura` E `--mitosi-2lam` ERANO MORTI: assegnati in una funzione, `global` in un'altra *(2026-09-25)*

Il `global SEMINA_MATURA` e il `global MITOSI_2LAM` sono in **`_applica_flag`**, ma **le
assegnazioni erano in `esegui_headless`**: due funzioni diverse, quindi là erano **variabili
LOCALI** e il flag di modulo restava `False`.

> ### ⛔ **I DUE FLAG NON FUNZIONAVANO DA RIGA DI COMANDO.**
> ### ⚠ **E I DUE SIGILLI PASSAVANO UGUALMENTE**, perché impostavano `S.SEMINA_MATURA = True`
> ### **direttamente sul modulo: non hanno mai provato il percorso CLI.**
> **`7/7` e `8/8` restano validi per la LEGGE, ma non dicevano niente sul FLAG.**
>
> **L'ha trovato il SIGILLO DEL DRIVER** *(`MITOSI_2LAM False/False` in NUDA e CAMPAGNA)*: senza
> il mandato di aggiungerli al driver, **il difetto sarebbe restato invisibile fino alla prima
> campagna.**
>
> **E il commento accanto al `global` diceva esattamente questo rischio** — *«senza questo
> l'assegnazione sarebbe una LOCALE, cioè INERTE IN SILENZIO»*. **Scritto, e poi fatto.**
> **È la famiglia di `VERSO_CHI` e `TW_SPINORE`: un flag che non fa ciò che dichiara è peggio di
> un flag assente.**

**✅ CURA: le tre assegnazioni** *(`SEMINA_MATURA`, `MITOSI_2LAM`, `SEMINA_LAM`)* **stanno ora in
`_applica_flag`**, verificato dall'AST. **Sigillo del driver: `15/15`.**

**⛔ E RESTA IN CODA:** i sigilli di `CURA 4` e `CURA 5` **vanno rifatti passando dal CLI**,
altrimenti quel percorso resta non provato.

### ➕ `SEMINA_LAM` IN `_applica_flag`: il vuoto di default diventa la SATURAZIONE *(SCENA-1, 2026-09-25)*

```
net.semina(-1 if SEMINA_LAM else a.nodi)
```

**`-1` non è un numero: è il sentinella della SATURAZIONE**, e il numero di nodi lo decide la
**geometria**. **A flag spento il comportamento è quello di prima** *(`a.nodi`)*, perché senza
distanza minima **la saturazione non esiste** — e `semina` lo dice da sé rifiutando `n < 0`.

### ➕ `--mitosi-2lam` in `_cli` / `_applica_flag` *(CURA 5, 2026-09-25)*

| flag | default | byte-inerte a default? |
|---|---|---|
| **`--mitosi-2lam`** | **OFF** | **sì**: la condizione è un `and` in più su una maschera, e a flag spento non si valuta. Lo prova `C1` |

**La legge sta nella scheda `mitosi-schwinger`.**

<!-- SCHEDA nome=fase-phi funzioni=_w4,_w8,_wphi,_dphi,circolazione_topologica,semina,step flag=FASE_2PI,TORS_4PI -->

> ## ⚠ **2026-10-05, `Z43` CURA (2): `step()` NON PROMUOVE PIU' IL GAUGE DI `ritmo()`**
>
> **Era, dentro `step()`:** `_med_f_prec = _med_f_ultimo`, con il ramo che **non** promuoveva
> un `med` finito sul pavimento `1e-9`.
> ### **ESCE** perche' quel gauge **era la MEDIANA GLOBALE DELLA FASE**, e la legge nuova
> `r = cs_nodo/CS_M` ### **non legge piu' la fase:** non c'e' piu' niente da promuovere.
> **La scheda della legge e' `tempo-proprio`** *(sezione ⑤)*; qui si registra **l'effetto su
> `step()`**, che e' dove la promozione viveva.
>
> ### ✔ **E QUELLA PROMOZIONE ERA UN PRESIDIO, non un dettaglio -- va detto perche' chi
> ### legge non creda che fosse codice di servizio:** stava in `step()` e **non** in
> `ritmo()` proprio perche' `ritmo()` ha **TRE call-site e DUE sono DIAGNOSTICI**. Se lo
> snapshot fosse avanzato dentro `ritmo()`, ogni chiamata diagnostica avrebbe fatto avanzare
> lo **stato fisico**. ### **Quel presidio esce INSIEME alla cosa che proteggeva**, e il
> ragionamento resta in `csv/_archivio/_rami_off_z43_cura2.py`.
>
> **E `_med_f_prec`/`_med_f_ultimo` restano DICHIARATI a `None`** *(`A7b`)* **e da oggi
> nessuno li scrive:** due registri morti, non tolti perche' **due strumenti di misura li
> leggono** *(`_f_e_median.py`, `_z43_tempo_proprio.py`)*. Voce `RITMO-FLAG-SENZA-OGGETTO`.


> ### ⚠ **COMMIT 0-bis — L'IMPULSO INIZIALE DI FASE DELLA SEMINA: quale ramo gira** *(2026-10-01)*
>
> Il commento diceva *«zero in regime stocastico **(canonico)**, calcio termico di punto zero in
> regime deterministico»*, e ### **l'etichetta «canonico» stava sul ramo che NON GIRA.**
>
> | | |
> |---|---|
> | ### **cio' che gira** | `REGIME = "deterministico"`, quindi `_CALORE_INIT = 0.4`: ### **`phivel` nasce con un calcio termico di punto zero**, e quel calcio ### **SOSTITUISCE il vuoto come energia iniziale** |
> | **cio' che non gira** | il ramo stocastico, dove `_CALORE_INIT = 0.0` e `phivel` ### **nasce a zero** *(valore dell'**epoca 1**)* |
> | ### **e la forma del calcio dipende da un ALTRO flag** | `CALORE_VETTORIALE`: se acceso il calcio e' ### **FIRMATO dalla chiralita'** *(`chi_nuovi · normal(...)`)* e ### **non si media a zero**; se spento e' un ### **rumore isotropo** |
>
> ### ➜ **Va detto nella scheda perche' tocca `phivel` ALLA NASCITE:** l'energia iniziale della
> fase ### **non e' un dettaglio di configurazione**, e ### **l'etichetta «canonico» puntava al
> ramo sbagliato.**

> ### 📌 **NOTA DEL 2026-09-29 — `P_eq` dentro `step`: IL CONFRONTO ERA FRA DUE METRI DIVERSI**
> *(`RIPIEGHI-ZERO`, rilevato da Luca)*
>
> `P_eq` e' la **rigidita' del mezzo** *(la relazione di dispersione, `v^2`)*, e il codice dice che
> viene da *«`d0`, la scala di frequenza mediana del ritmo»*. La guardia era
> **`len(self.d0) >= self.n`**: ### ⚠ **`d0` e' PER ARCO e `self.n` conta i NODI.**
> `471564 >= 12802` e' **sempre vero**, quindi ### **il ramo di scorta (`1.0`) non scattava mai** --
> era un ripiego **solo in apparenza**.
>
> **Ora il confronto e' `len(self.d0) >= len(self.i)`**, archi contro archi, e resta sempre vero:
> ### ✅ **BYTE-INERTE, e MISURATO** — 8 passi, 23 grandezze, **zero differenze** contro il blob
> `9cf6fb07`.
>
> ### ⛔ **E LA FETTA NON E' IL CONFRONTO, e NON e' curata qui**
> `float(np.median(self.d0[:self.n]))` prende la mediana dei ### **PRIMI `n` ARCHI su `m`** --
> **12802 su 471564** sulla scena grande -- cioe' un **sottoinsieme arbitrario**, ordinato per
> **creazione**. ### **Una mediana su un sottoinsieme arbitrario non e' «la scala mediana del
> ritmo».**
> **Registrata come `P-EQ-MEDIANA-ARCHI`** e lasciata **IN CODA**: correggerla ### **cambia il
> VALORE di `P_eq`**, quindi e' un cambio di fisica e vuole il suo commit e il suo sigillo.
>
> ### ⚠ **E la guardia e' ora RIDONDANTE:** il **controllo unico** *(scheda `registro-grandezze`)*
> garantisce `len(d0) == m` ai due punti del passo. **Va tolta col resto delle guardie di
> sostituzione**, nel commit separato che il mandato prevede.

> ### ✅ **FATTO IL 2026-09-29 — la guardia di `P_eq` E' TOLTA, e `_sin2_vir` e' SEPARATA**
> *(punto 3 di Luca, primo pezzo; entrambe dentro `step`)*
>
> | | |
> |---|---|
> | **`P_eq`** | via `and len(self.d0) >= len(self.i)`: ### **era sempre vera per costruzione** — una guardia che non guarda niente *(`A9`)*. ### **`self.n > 0` RESTA**, e non e' la stessa cosa: su una rete vuota `median([])` da' `nan` e `np.seterr(invalid='raise')` **solleva**. ### **La FETTA non e' toccata** *(`P-EQ-MEDIANA-ARCHI`, in coda)* |
> | ### **`_sin2_vir`** | la **condizione fusa** del **freno anisotropo** e' separata **nei due rami** *(non-Verlet e gemello Verlet, coi loro due contatori)*: `None` ### **resta legittimo e contato** *(`A1`)*, **lunghezza sbagliata SOLLEVA** |
>
> ### ✅ **AGGIORNATO IL 2026-09-29 (generalizzazione 1):** i due siti di `_sin2_vir` passano
> ora a `_ferma_registro` la ### **FORMA** *(`_forma_di(self._sin2_vir)` contro `(len(beta),)`)*
> invece di due interi. ### **Cambia solo il MESSAGGIO** — la condizione e' la stessa — e la
> ragione e' che il controllo ora verifica **tutti gli assi**, quindi il messaggio deve poter
> dire una forma e non una lunghezza. **La legge sta nella scheda `registro-grandezze`.**
>
> ### **Byte-inerte, e MISURATO: 12 passi, 23 grandezze, zero differenze — E I CONTATORI IDENTICI**
> *(`_g_zeta_vir_a_salti` **1**, `_g_zeta_vir_b_salti` **4**, in entrambi i blob: scatta **solo** la
> causa `None`)*. ### **Il confronto sui CONTATORI e' piu' fine di quello sulle grandezze**, e qui
> serve: un contatore che cambiasse di uno sarebbe un difetto che la byte-identita' **non vedrebbe**.

> **-> NOTA DEL 2026-09-28 (`MAX-NODI-FERMA`), e riguarda `semina`: LA LEGGE DELLA SEMINA NON
> E' CAMBIATA, e' cambiato CIO' CHE FA QUANDO NON CI STA.** Prima **troncava**
> (`min(n, MAX_NODI - self.n)`): si chiedevano `n` nodi, ne nascevano meno, **e dai dati non
> si vedeva**. Ora **ferma il run**. ### **Byte-inerte finche' la guardia non morde**, cioe
> sempre nelle corse reali. ### 🟨 **E IL RAMO SENZA `SEMINA_LAM` E' COPERTO: misura di Luca del
> 2026-09-28** -- `MAX_NODI = 100` con `semina(200)`, **il vecchio tronca a 100 in silenzio, il nuovo
> solleva `LimiteNodiSuperato`**.
> ### **E IL CONTROLLO E' UNO, DOPO LA GEOMETRIA, PER ENTRAMBI I RAMI**
> *(prescrizione del guardiano, 2026-09-28)*: nel ramo `_sat` il numero lo decide **la geometria**
> (`n = len(p)`) e il valore calcolato con `MAX_NODI` **non viene usato**, quindi **prima la
> saturazione non era controllata affatto**; e un controllo dentro il solo ramo `SEMINA_LAM`
> **lascerebbe scoperto l'altro ramo**.
> *(La legge della guardia sta nella scheda `guardia-max-nodi`.)*
# ⑥ LA FASE `φ` E IL SUO DOMINIO — **`semina` / `_w4` / `_w8` / `step`**

> ### 🏗 **T1, 2026-09-28: `step` non apre piu' il passo, e non e' piu' il proprietario di niente**
>
> In `(c)1` l'apertura era **passata prima della guardia** `if self.n < 2 ...`; ### **ora e' uscita
> del tutto**: la fa lo schedulatore, in testa alla composizione. **Il commento storico che diceva
> *<<il passo, per il freno, e' il ciclo INTERO del driver>>* e' finalmente vero nel codice e non
> solo nel testo** -- e sta scritto in `PASSO_COMPOSIZIONE`, non in un commento.
> **La legge sulla FASE non e' toccata:** `_dphi`, `_wphi`, il dominio a `4 pi` e il cuore
> simplettico `phivel -> phi` restano come erano. *(Scheda `schedulatore-del-passo`.)*


> ### 🔓 **(c)1, 2026-09-27: `step` non e' piu' il proprietario della fotografia**
>
> `_smp_apri()` era chiamata **qui**, e il suo commento diceva che <<il passo, per il freno, e' il
> ciclo INTERO del driver>>: **lo diceva e non lo faceva** -- la fotografia si apriva all'inizio di
> `step`, cioe' **dopo** `scuoti_vuoto`. Ora la aprono **tutte e cinque le leggi**, idempotente, e
> la prima che gira apre. **Il commento e il codice ora dicono la stessa cosa.**
> ### **E l'apertura e' passata PRIMA della guardia `if self.n < 2 or not len(self.i): return`:**
> con meno di 2 nodi il passo **non apriva** la fotografia, e il freno del passo **non chiudeva**.
> **La legge sulla FASE non e' toccata:** `_dphi`, `_wphi`, il dominio a `4 pi`, il cuore
> simplettico `phivel -> phi` restano come erano. Qui cambia **soltanto** dove nasce la
> transazione del freno.


> ### 🗄 **(b)2, 2026-09-27: `step` perde il campo `psi_t` della snapshot**
>
> **`SYNC_UPDATE` e' un NO-OP ACCETTATO dal 2026-09-27** *(passo `(b)2` di `ETC-PASSO`)*: i
> suoi rami sono in **`csv/_archivio/_sync_update.py`**, tag **`pre-archivio-sync`**, e `--sync`
> si accetta senza fare niente. **Il suo raggio era UNA legge su cinque** -- `7` usi in
> `_passo_spinoriale`, `6` in `step`, **ZERO** nelle altre quattro -- e **tutte e 56 le letture
> miste `t`/`t+1` misurate nella FASE 0 stavano FUORI da quel raggio.**
>
> **Che cosa e' uscito da `step`:** il calcolo di `psi_t` dalla snapshot; le **tre** letture
> `psi_forces`/`psi_sync` che lo preferivano a `calcola_psi`; il ramo della **materia della
> metrica** (`self.psi = psi_t.copy()`), di cui resta il percorso storico `F = Mw @ exp(i phi)`;
> la fotografia `_peq_t`, che dopo la rimozione **non aveva piu' lettori**.
> ### **`_phi_t` RESTA, e va detto perche' non e' una dimenticanza:** la fotografia della FASE
> la legge **il percorso vivo** (`z = np.exp(1j * _phi_t)`), non il ramo sincrono. **Non era
> parte di `SYNC_UPDATE`.**
> **Il dominio a `4 pi` e `_dphi`/`_wphi` non sono toccati.**


> ### 🗄 **(b)1, 2026-09-27: `step` perde il pavimento su `d` e una chiamata su `d0`**
>
> Nei **due** sottocicli metrici di `step` il ramo `else` faceva
> `np.maximum(self.d + dts*vd, 0.05)`. **Col driver non girava mai** *(0 esecuzioni; e quello di
> Eulero era doppiamente morto, perche' il driver passa `--verlet`)*, ed e' **uscito**: restano
> **DUE rami invece di tre** -- il freno di `SCALA_MIN`, e l'aggiornamento nudo che
> `SCALA_MIN_PASSO` frena **una volta sola** dopo il ciclo. **`9-ter`: il numero delle leggi
> scende.** Via anche una chiamata `self.d0 = self._pav_d0(self.d0)`, che era un no-op.
> **La legge sulla FASE non e' toccata:** `_dphi`, `_wphi` e il dominio a `4 pi` restano come
> erano. Qui cambia solo il settore METRICO di `step`.

> ### ⚠ **E UNA CORREZIONE, il 2026-09-27 (Luca, su `7840039`): LA PRECEDENZA**
>
> Nel collassare i tre rami in due avevo scritto `if SCALA_MIN: freno / else: nudo`, che
> **ROVESCIA la precedenza**: prima `SCALA_MIN_PASSO` era la **prima** condizione della catena e
> **vinceva**. Con entrambi i flag accesi si sarebbe frenato **due volte**, per scrittura e a
> fine passo. **Ora la forma e' esplicita:** `if SCALA_MIN and not SCALA_MIN_PASSO`.
> **Il sigillo byte-identico col driver non poteva vederlo**, perche' col driver `SCALA_MIN` e'
> spento: **un sigillo su UNA configurazione non certifica una PRECEDENZA fra due flag.**



> **STATO: `DIFETTOSA`.** Difetti **`D34`** *(il wrap del ritmo)*, **`D35`** *(l'antifase di
> Schwinger)*, e i sospetti **`S07`**, **`S08`**.
> **⚠ QUESTA SCHEDA RIVENDICA `step` IN VIA PROVVISORIA:** `step` fa **tutto**, e attribuirlo
> alla fase è improprio. Lo tiene perché `REG-R` mappa **per funzione** e i due siti di `φ`
> vivono lì. **Quando `step` avrà la sua scheda, il marcatore si divide.**
>
> ### ➜ **E `semina()` HA UN RAMO NUOVO: `SEMINA_LAM`** *(2026-09-24)*
>
> Questa scheda rivendica `semina` **per la FASE** *(`φ` nasce su `[0, 4π)`)*. Il ramo nuovo
> **non tocca la fase**: tocca **le POSIZIONI** — ogni nodo a distanza `>= LAM` da qualunque
> altro, con `RSA` — e **la sua legge sta in scheda ⑫**.
> **⚠ Ma è nella STESSA funzione**, quindi una modifica futura alla fase della semina e una alla
> geometria **si incontrano qui**. *(Stessa ragione per cui questa scheda rivendica `step` «in
> via provvisoria»: quando `semina` avrà la sua scheda, il marcatore si divide.)*
>
> ### ➜ **E `CURA 2` HA TOCCATO `step`, con una modifica SENZA FLAG** *(2026-09-24)*
>
> La media **armonica** d'arco di `:4791` — `cs_arco = 2·cs_i·cs_j/(cs_i+cs_j)`, il *«collo di
> bottiglia causale»* — è stata **ESTRATTA nel metodo `_cs_arco_da_nodo`** e `step()` ora lo
> **chiama**, **senza che l'espressione cambi di una virgola**. Motivo: `mitosi()` ne ha
> bisogno per `tau_arco = d/cs_arco`, e **duplicarla avrebbe dato due leggi che possono
> divergere**.
>
> **⚠ NON È GATED DA NESSUN FLAG**, quindi nessun sigillo di byte-inerzia del *flag* la copre:
> **la copre solo `T4`**, che confronta il run a flag SPENTO col riferimento `_cura1_corto`.
> **Se `T4` fallisce, il primo sospetto è questa estrazione, non la cura.**
>
> *(E conferma ciò che questa scheda dice già: `step` fa troppe cose perché una sola scheda lo
> rivendichi. La divisione del marcatore resta in coda.)*

## LA REGOLA DI FONDO *(decisione di Luca, 2026-09-22)*

> **Lo spinore ha periodo `4π`; tutto ciò che si OSSERVA da lui ha periodo `2π`; un ACCUMULO
> non ha periodo.**
> `np.angle`, `|ψ|²`, `exp(iφ)`, `cos`, `sin` hanno **periodo `2π`**: **non vedono il segno
> dello spinore.** **Un avvolgimento su `4π` applicato a una grandezza a periodo `2π` non
> avvolge niente. Un «`+2π` = antifase» letto attraverso `exp(iφ)` è un'identità.**
> **Per ogni `π` del codice la domanda è: questa grandezza è lo SPINORE, un'OSSERVABILE o un
> ACCUMULO?**

## LA FORMA OGGI — copiata dal codice

```
semina  (:2349-2350)   phi, phi0 <- ph % (4 pi)                    <- il dominio DICHIARATO
step    (:4625)        phi <- (phi_t + dt_n_s*phivel + dsync) % (4 pi)
mitosi  (:5289-5357)   fm, phi[a], phi[b], phi[g]  % (4 pi)
mem_mot (:6105)        phi[ii] <- (phi[ii] + shift) % (4 pi)
_w4     (:3423)        (a + 2 pi) % (4 pi) - 2 pi                  <- differenze di fase
_w8     (:3426)        (a + 4 pi) % (8 pi) - 4 pi                  <- la TORSIONE accumulata
```

## ⚠ IL FATTO MISURATO, ed è il cuore della scheda

**In `31` righe su `31` il campo legge `φ` attraverso `exp`, `cos`, `sin` o `angle`** *(`Z118`,
censimento da AST)*. **In tutte e 31 la doppia copertura di `φ` è INVISIBILE alla fisica**,
perché `exp(i(φ + 2π)) = exp(iφ)`. **Non è un'interpretazione: è un conto.**

**E la verifica che Luca ha chiesto è stata fatta** *(`Z120`)*: **nessuna riga della FISICA
distingue `φ` da `φ + 2π`**, fuori dalla torsione *(`_w4`/`_w8`)* e dall'antifase.
`31` candidati letti uno per uno: `13` assegnamenti, `7` torsione, `2` antifase, `6` diagnostici.

> **⚠ E UNA PREMESSA CHE È CADUTA, scritta qui perché non si riusi:** il docstring di
> `_passo_spinoriale` dice che `φ` è **l'azimut del vettore di Bloch**. **MISURATO: FALSO**
> *(`Z121`, `R ≤ 0.18` contro un criterio di `0.90` e un nullo di `0.016`)*.
> **Se `φ` non è l'azimut, che cos'è? → `S08`, aperto.** **Refutare non è spiegare.**

## LE DIMENSIONI

`φ`, `_w4(Δφ)`, `_w8(…)`, `twist_dip` sono **angoli**, cioè adimensionali. **Coerente.**
*(Il difetto non è dimensionale: è di PERIODO.)*

## I LIMITI, CLASSIFICATI CON `A11` e con le classi `T/L/E`

| punto | classe | esito |
|---|:--:|---|
| `% (2π)`, `% (4π)`, `_w4`, `_w8` | **`T`** | **NON si levigano.** Il salto da `2π` a `0` è un artefatto della **coordinata**: levigarlo **inventerebbe valori che non esistono**. **La cura è il PERIODO GIUSTO** |
| la soglia della mitosi, `discesa`, il punto di inversione | **`L`** | **si levigano**, coi tre obblighi del cor.7 e la **larghezza DERIVATA** — **ma appartengono a `SCALE-TW`, non a qui** |
| la nascita di un nodo | **`E`** | **evento discreto**: resta discreto, **ma il suo TASSO dev'essere liscio** |

## LA CURA DECISA — **`FASE_2PI`**, spenta di default — ✅ **IN CODICE** *(blob `3d91338e` → `445e2896`)*

**I DUE AIUTANTI, e sono il punto della forma:** **`_dphi()`** *(il periodo)* e **`_wphi()`** *(l'avvolgimento di una differenza)*. **UN SOLO POSTO da cui tutti prendono il periodo**, così non si possono sfasare fra loro — **che è esattamente il difetto che `D34` ha mostrato costare caro**: due rami della stessa funzione con due periodi diversi, a otto righe di distanza.

> **Decisione di Luca, presa dopo la verifica di `Z120`.** **Regge su TRE argomenti invece dei
> quattro iniziali**, perché il quarto *(l'azimut)* è caduto con `Z121` — **e l'argomento
> caduto non argomenta per `4π`: dice solo che `φ` non è ciò che il commento dichiarava.**

**`φ` è una FASE ORDINARIA su `[0, 2π)`. L'antifase è `+π`.**
**La doppia copertura resta dove è già vera: nel SEGNO esplicito** *(`_spinor_lift`,
`s_k = sign(perc_chi)`)* **e nei MEZZI ANGOLI** *(`exp(-0.5i…)`)* — **un solo ponte** *(`A10`)*.

**COSA TOCCA, e nient'altro:**

| | sito | oggi | con `FASE_2PI` |
|---|---|---|---|
| (a) | `:2349`, `:2350`, `:4625`, `:5289`, `:5291`, `:5353`, `:5354`, `:5357`, `:6105` | `% (4π)` | **`% (2π)`** |
| (b) | `:2218`, `:4628`, `:5273`, `:5403`, `:5404`, `:5508`, `:5509` | `_w4(Δφ)` | **`_w2(Δφ)`** *(via `_wphi`)* |
| (c) | `:5311` *(dormiente)*, **`:5443`** *(`D35`, attivo)* | `+2π` | **`+π`** |
| (d) | `:5104` | `soglia0 = 2π + π = 3π` | **`soglia0 = 2π`** |

**⚠ COSA NON TOCCA, ed è una scelta di confine:** **`:4651-4655`**, dove `_w8`/`_w4` avvolgono
la **TORSIONE ACCUMULATA** *(`tw`, `twp`)*. **`tw` è un ACCUMULO: non ha periodo**, e il suo
dominio appartiene a **`SCALE-TW`**. **Toccarlo qui mescolerebbe due decisioni.**
*(La conseguenza — `dph` passa da `(-2π, 2π]` a `(-π, π]`, quindi `twp` cambia intervallo
— **non è una modifica: è un effetto, ed è il test `E1`.**)*

**⚠ E IL PUNTO (e) DEL §D È GIÀ IN CODICE:** *«la coppia nasce con lo spinore di segno
opposto»* — `:5477` fa già `_eredita_spinore_figli(aa, segno=-1)`. **Verificato dal sorgente:
non c'è niente da cambiare lì.**

## LE DOMANDE APERTE

1. **`S08`: se `φ` non è l'azimut del Bloch, che cos'è?** **Non si risolve con un'altra
   misura adesso** *(decisione di Luca)*.
2. **`S07`:** `:5894` collassa a `2π` una differenza a `4π` — **dormiente** *(`K_FRANGE = 0`)*.
   **Con `φ` su `2π` quella riga diventa corretta per costruzione:** la cura la sana senza
   toccarla.
3. **Il dominio di `tw` resta a `4π`/`8π`.** **Con `φ` su `2π` è ancora il dominio giusto,
   o `_w8` diventa l'identità come lo era il wrap del ritmo?** → **`SCALE-TW`**.

---

### ⛔ **LA CURA DI `TORS-W8-AVVOLGIMENTO`** *(decisione di Luca, 2026-10-06)* — **e risponde
### alla domanda aperta `3` qui sopra, per un verso che non avevo considerato**

**La domanda `3` chiedeva se `_w8` diventi l'identità.** ### **La risposta e' un'altra: `_w8`
non era il periodo SBAGLIATO per eccesso, era il periodo sbagliato PER IL LAVORO CHE FACEVA.**

| | |
|---|---|
| la legge **di prima** | `tw += _w8(dph + twist_dip − twp)`, con `twp = _w8(dph + twist_dip)` |
| il difetto | `dph = _wphi(…)` vive su un periodo di **`4π`**; `_w8` ha periodo **`8π`**. ### **Un salto di `4π` NON e' un multiplo del periodo di `_w8`, quindi NON viene riparato** |
| **misurato** | ### **`142114` calci di modulo `4π` ESATTI** in `150` passi *(`64.6` milioni di coppie `(passo, arco)`)*, e il ramo non-`4π` — che usa `_w4`, periodo `4π` — ### **ripara entro `1.9e-15`** |
| la legge **di oggi** | ### **`tw += _w4(dph − twp) + (twist_dip − twp_dip)`** |

### ✔ **E LA CURA NON E' SCEGLIERE FRA `_w4` E `_w8`: si possono avere entrambe le cose.**
La **fase** si avvolge col **suo** periodo *(`_w4`, `4π`, lo stesso di `_wphi`)*; il
**dipolo** vale fra `−π` e `π`, cambia al massimo di `2π` e ### **non ha periodo, quindi non
si avvolge.** ### **Due stati separati al posto della somma.**

### ✔ **E IL CONTO DELLE LEGGI SCENDE** *(par.9-ter)*

Prima `twp` significava ### **due cose diverse nei due rami**: `_w8(dph + twist_dip)` nel ramo
`TORS_4PI` e `dph` nel ramo non-`4π`. ### **Oggi significa <<la fase precedente d'arco>> in
ENTRAMBI.** Un nome, un significato: ### **un'eccezione TOLTA.** Il costo e' **un** campo
d'arco, `twp_dip`.

### ⛔ **E LA RIGA <<COSA NON TOCCA>> QUI SOPRA NON ERA SBAGLIATA: ERA UN CONFINE, e Luca
### l'ha spostato**

Diceva *«`tw` e' un ACCUMULO: non ha periodo, e il suo dominio appartiene a `SCALE-TW`»*.
### ✔ **E' ancora vero: `tw` NON ha periodo, e la cura non gliene da' uno.** Quello che la
cura cambia non e' il dominio di `tw`: e' ### **il modo di calcolare il suo INCREMENTO**, che
e' una cosa diversa — e il difetto stava li'.

### ⛔ **I DUE CALCI DI NASCITA, della stessa famiglia**

| | dove | che cosa faceva |
|---|---|---|
| **(i)** | `_rn_div_twp` *(`:2219`)*, `_rn_sch_twp` *(`:2568`)* | inizializzavano `twp` alla **sola** differenza di fase, **senza `twist_dip`**: al primo passo l'arco nuovo riceveva ### **un calcio pari al suo dipolo** |
| **(ii)** | `_allaccia` *(`:5228`)*, chiamata da `semina` | `twp = 0`: al primo passo ### **tutta la differenza di fase piu' il dipolo diventava torsione** |

### ⛔ **E (ii) ERA LA SORGENTE PRINCIPALE DELLA TORSIONE DELLA RETE, misurato:** al passo `1`
la spinta mediana era ### **`3.0950`** e la massima ### **`9.4248` = `3π` ESATTO** *(il
massimo possibile di `|dph + twist_dip|`: il calcio saturava il suo limite teorico)*. Il tempo
di scarica e' `τ_tw/dt_e` ≈ **`309` passi**, quindi in `150` passi la rete conserva il
`61.5 %` del calcio: `3.0950 × 0.6151` = `1.9037`, contro il `|tw|` mediano ### **misurato
`2.1105`** al passo `140`.

> ### ⛔ **LA TORSIONE CHE LA RETE AVEVA A `150` PASSI ERA QUASI TUTTA IL CALCIO DI NASCITA,
> non l'accumulo della deriva.** ### **E un calcio che viene da un'inizializzazione non viene
> da nessuna legge.**

### ✔ **LA CURA: SPINTA ZERO AL PRIMO PASSO, per QUALUNQUE via di nascita**

Il marcatore e' ### **`nan` su `twp_dip`**, consumato dal primo passo di torsione, con
l'invariante ### **PRECISATO e non allargato** *(la lezione di `peq`)*: *«finito, e `nan` SOLO
su un arco con `tw == 0` esatto, cioe' mai passato dalla torsione»*. ### ✔ **E il <<mai oltre
un passo>> e' STRUTTURALE:** il passo di torsione scrive `twp_dip` **incondizionatamente su
ogni arco**.

### ⚠ **PERCHE' UN MARCATORE E NON IL VALORE ALLA NASCITA:** per la **fase** il valore alla
nascita funziona esattamente *(dopo `mitosi()` nessuno scrive `phi`)*; ### **per il DIPOLO no**
— con `CHI_CORE` o `CHI_COOP` accesi `chi_torsione` viene da una **cache scritta nel passo
della torsione**, quindi il valore letto alla mitosi non e' quello che l'arco vedra'.
### **Il marcatore non dipende da nessun flag.**

### ⛔ **E NON SI TOCCA IL RAMO NON-`4π`**, che non ha il difetto: `_w4` con `twp = dph` era
### **gia' giusto**, e ora i due rami ### **scrivono la stessa cosa in `twp`.**

---


### ❗ UNA FASE A `0` STA **SUL TAGLIO DEL WRAP**, E OGNI STATISTICA LINEARE LA LEGGE COME MASSIMO DISORDINE *(2026-09-25)*

**Misurato nella prova di fumo della scena `(ii)`**, e preso **prima** di usarlo come criterio:

```
fase della regione = 2 pi k/3       ->  massa_0 (k=0, fase ZERO):  std(phi) = 6.0798
                                        massa_1:                   std(phi) = 0.0518
                                        massa_2:                   std(phi) = 0.0468
                                        ... A FASE IDENTICAMENTE COERENTE
```

**`phi % _dphi()` manda la coda gaussiana negativa a `~4 pi`:** la fase resta **coerente SUL
CERCHIO**, ma `std` la legge a cavallo del taglio e dà **il valore del disordine massimo**.

> ### **NON È UN DIFETTO DI `phi`: È UN DIFETTO DELLA STATISTICA.** La coerenza di una fase si
> ### misura **CIRCOLARMENTE**, `|<e^{i phi}>|`, non con una deviazione standard.

### ❌❌ LA MIA PRIMA CURA DEL TAGLIO ERA UNA SCELTA DI FISICA NON DICHIARATA *(Luca, 2026-09-25)*

**Avevo messo ogni regione al centro di un TERZO diverso del dominio**, `_dphi()*(k+0.5)/3`.
Evitava il taglio — ed era vero — **ma dava alle tre masse fasi SFASATE DI 120 GRADI in
`exp(i phi)`**.

> ### **MASSE SFASATE INTERFERISCONO IN PARTE IN MODO DISTRUTTIVO:** fra loro nascono
> ### **repulsione o cancellazione DALLA CONDIZIONE INIZIALE, non dalla dinamica.**
>
> E la **prima delle tre prove** chiede esattamente *«due masse si avvicinano?»*: sarebbe
> stato **un effetto messo dentro da me**, e indistinguibile da quello cercato.
>
> **La scena vecchia usava la STESSA fase per tutte, e il codice diceva perché:**
> *«fase compatibile: le masse devono coesistere, non annichilarsi»*. **Non l'ho letto.**

**DECISIONE DI LUCA: la STESSA fase per tutte e tre, `_dphi()/2`.**
Sta **lontana dal taglio da entrambi i lati**, e poiché il campo usa **`exp(1j*phi)`
direttamente** (`:3635`), `phi = 2 pi` dà `exp(i 2 pi) = 1`: **è la fase ZERO di prima,
esattamente.** **Nessun numero nuovo:** il centro di un intervallo non è una manopola.

**⚠ E LA PROVA DI FUMO NON SE NE ACCORGEVA, perché non misurava la grandezza in questione:**
guardava la coerenza **DENTRO** ciascuna regione — **perfetta in entrambi i casi** — e non
**FRA** le regioni. **Un criterio che non guarda la grandezza di cui si discute non è un
criterio.** Ora la misura c'è, e **il suo nullo si sa in anticipo**: tre gruppi uguali a
`120°` **si cancellano**, quindi la versione sfasata darebbe `|<e^{i phi}>| ~ 0`.

| | coerenza FRA le regioni | fasi nel campo `exp(1j*phi)` |
|---|--:|---|
| **scena `(a)`, fase unica** | **`0.999681`** | `359.965 / 0.085 / 359.939` — **fase ZERO, la stessa** |
| **scena `(b)`, fase unica** | **`0.999666`** | `0.248 / 359.969 / 359.222` — **fase ZERO, la stessa** |
| **controllo a fasi casuali** | `0.029367` | `322.890 / 3.935 / 335.848` |

> **⚠ LA VERSIONE SFASATA È ESISTITA SOLO NEL COMMIT `3a67512` E NON HA PRODOTTO NESSUNA
> MISURA** *(registrato su richiesta di Luca)*. I numeri della prova di fumo di quel commit
> — taglia, archi, `QUOTA`, distanza minima — **non dipendono dalla fase** e restano validi.

**E la convenzione si dichiara, sennò il numero si legge male:** le fasi «normalizzate a
`4 pi`» valgono `~180°` perché `_dphi()/2` è metà del periodo di `phi`; **nel CAMPO sono
`0°`**. Due convenzioni, due numeri, **lo stesso stato**.

**Il valore dopo la cura del taglio:**

```
COERENZA CIRCOLARE |<e^{i phi}>|      dentro le regioni   0.999631 / 0.999665 / 0.999726
                                      nel vuoto           0.008019   (nullo ~ 1/sqrt(n) = 0.0157)
BRACCIO DI CONTROLLO di `S10`         dentro le regioni   0.071 / 0.035 / 0.032  -> AL NULLO
```

**È la stessa famiglia di `RITMO_WRAP_2PI`**, e la stessa del presidio del par.9 *«quanto
varrebbe se non ci fosse niente?»*: `std(phi) ≈ D/sqrt(12) = 3.63` **è** il valore di fasi
casuali, e `6.08` è **peggio del caso**, cioè il segno che la statistica è sbagliata e non il dato.


### ➕ `CURA 4` TOCCA `semina`: il parametro `maturi` *(2026-09-25)*

`semina(..., maturi=None)` decide se i nodi nuovi nascono **maturi** *(`ramp = 1`)* o con la rampa. **Default: maturi se la rete era VUOTA** *(`base == 0`)*, cioè se questa semina **è** l'universo. **La legge sta nella scheda `accensione-campo`.**

> **✅ AGGIORNATO il 2026-09-25 (`RAMPA-1`, strada (3)):** i nodi maturi ricevono
> **`eta = +inf`**, non `eta = _tempo_rampa()`. **La rampa non puo' piu' SCENDERE** — prima
> scendeva, misurato: `ramp` da `1.000000000` a `0.845601758` in **un** passo, perche' il
> denominatore cresce `x1.196` contro `x1.011` del numeratore.
> **La derivazione e i numeri stanno nella scheda `accensione-campo`**: qui sta solo il
> rimando, perche' `semina` compare in entrambi i marcatori e **un lettore che arriva da
> `fase-phi` non deve poter credere che la legge sia ancora quella.**

<!-- SCHEDA nome=tau-tw-locale funzioni=_tau_tw_locale flag=TAU_LOCALI,TAU_TW -->

# ⑦-bis IL TEMPO DI SCARICA DELLA TORSIONE — **`τ_tw` LOCALE**

> ### ✔ **DECISIONE DI LUCA, 2026-10-06 sera: `κ = 1` E' LA LEGGE.**
>
> La legge e' ### **`τ_tw = 2π / |Δω_locale|`**, con ### **`κ = 1`.**
>
> ### ⛔ **IL DOCSTRING DICEVA `κ_tw = TAU_TW/(2π)`, cioe' `3.1831`, E IL
> CODICE HA SEMPRE USATO `1`.** E non e' la svista di un giorno: e' ### **cosi' dal PRIMO
> COMMIT del file** *(`670310f`)*, e la ### **stessa scelta `κ = 1`** vale per `TAU_BG`
> e `TAU_P` — ### **e' una scelta SISTEMATICA**, e il docstring era ### **il pezzo
> vecchio.**
>
> ### ⚠ **E LA DIFFERENZA NON ERA PICCOLA:** con `κ = 3.1831` il tetto di
> equilibrio della torsione sarebbe stato ### **TRE VOLTE piu' alto**, e ### **per mesi il
> registro ha detto quel numero mentre il sistema ne usava un altro.**
>
> **Il blob passa da `30e18cdd` a `b8c21049`**, e il sigillo `K0` verifica che i
> ### **code object sono IDENTICI**: `12` differenze, ### **tutte dichiarate** — `2`
> stringhe *(il docstring e il messaggio di `--chi-basc`)* e ### **`10` numeri di riga**
> spostati del delta ### **MISURATO**.

*(Scheda **aperta il 2026-10-06**, dalla cura di `TORS-W8-AVVOLGIMENTO`. ### ⛔ **Non
esisteva, e il presidio `H-REG-R` l'ha preteso: una legge che cambia vuole una scheda, e
`_tau_tw_locale` ne era senza.** ### **`KAPPA-TW-COMMENTO` non aveva casa: ora ce l'ha.**)*

## LA FORMA, dal codice e non dal commento

```
def _tau_tw_locale(net):
    i, j = net.i, net.j
    if len(net.phivel) < net.n or len(i) == 0:
        return TAU_TW                                   # <- LA GUARDIA
    dom = |phivel[i] - phivel[j]| + 1e-3
    return maximum(2*pi / dom, 1e-3)                    # <- kappa = 1
```

| | |
|---|---|
| **che cos'e'** | il tempo di **scarica** della torsione: `tw` perde `dt_e·tw/τ_tw` a ogni passo |
| **la legge** | `τ_tw = κ·2π/(|Δω| + 1e-3)`, con `Δω` = differenza di `phivel` fra i due nodi |
| **dimensioni** | `[τ] = T`. `ω` e' una frequenza, `2π/ω` un tempo: ### **coerente** |
| **il verso** | la torsione decade **tanto piu' in fretta** quanto piu' i due nodi sono **fuori fase** |
| **chi la legge** | **solo** il blocco della torsione in `step()`, nei **due** rami *(`:7795` e `:7799`)* |
| **l'interruttore** | `TAU_LOCALI = True` *(`:451`)*: se `False`, `τ_tw = TAU_TW = 20.0`, **costante** |

## ⛔ **I TRE NUMERI SCRITTI A MANO** *(`A1`, `A11`)*

| | valore | che cos'e' | classificato |
|---|--:|---|---|
| **`κ`** | ### **`1`** | il rapporto `O(1)` della legge | ### ⛔ **UN NUMERO SCRITTO A MANO**, e il docstring ne dice **un altro** |
| il pavimento **dentro** `dom` | `1e-3` | impedisce la divisione per zero quando `Δω = 0` | ### ⚠ **una GUARDIA NUMERICA** *(`A11`)*: protegge da un **infinito**, e un infinito non e' un errore — e' il caso `Δω = 0`, in cui la torsione **non decade**. ### **Classificato: PROIEZIONE, da derivare** |
| il pavimento **esterno** | `1e-3` | tetto inferiore su `τ_tw` | ### ⚠ **MISURATO INERTE:** scatta se `Δω > 6283`, e il massimo misurato e' `3.236` — ### **`0` archi su `64.6` milioni di coppie** *(`eebe24f`)*. ### **Inerte NON vuol dire giusto: vuol dire non ancora in gioco** |

### ⛔ **`KAPPA-TW-COMMENTO`: il commento dice `3.1831`, il codice restituisce `1`**

Il **docstring** dice *«`kappa_tw = TAU_TW/(2π)` resta come rapporto `O(1)`»* e il commento
nel corpo lo ripete; ### **la riga che gira non ha nessun fattore `TAU_TW`.** Con
`TAU_TW = 20.0` il commento implica `κ = 3.1831`, il codice da' `κ = 1`.

| con | il tetto di equilibrio | e la soglia di mitosi `3π` |
|---|--:|---|
| `κ = 1` *(il codice)* | **`2π`** | ### **irraggiungibile in equilibrio**: la mitosi e' **marginale** |
| `κ = 3.1831` *(il commento)* | **`20`** | **tre volte** la soglia: la mitosi sarebbe **generica** |

### ➜ ⛔ **DUE LETTURE, DUE FISICHE OPPOSTE.** ### **Non si decide dal commento** — in questo
repo i commenti **sono stati** scaduti — ### **si decide da `git log` sulla riga del
`return`.** ### **Che fare di `κ` e' UNA DECISIONE DI LUCA**, e la voce resta **aperta**.

## ✔ **LA GUARDIA SI CONTA, dal 2026-10-06** *(rilievo `E4` del guardiano)*

`_tau_tw_locale` fa `return TAU_TW` nel **proprio** ramo di guardia, quando
`len(net.phivel) < net.n` **oppure** non ci sono archi. ### ⛔ **Quindi `TAU_TW` entra in gioco
per TRE vie, non due** -- il ramo non locale, il docstring, e **questa guardia** -- e
### **nessuno la contava.**

| se scattasse | `τ_tw` passerebbe da | a |
|---|--:|--:|
| *(misurato in `eebe24f`)* | **`2.4055`** al passo `50`, **`1.9738`** al passo `140` | ### **`20`** |

### ➜ **un fattore `3`-`10` sul tetto di equilibrio, in silenzio.** ### **Un ramo silenzioso
non e' un ramo** *(`A8`)*. Ora porta i quattro contatori di `A8` — ### **invocazioni, salti,
forma al fallimento, QUANDO** — ### **ed e' BYTE-INERTE:** nessun valore restituito cambia.

### ✔ **E IL PRIMO NUMERO C'E' GIA':** sul giro minimo della cura, ### **`0` salti su `3`
invocazioni** — la guardia **non scatta** in questa scena. ### ⚠ **E <<non scatta in questa
scena>> non e' <<non scatta mai>>:** il numero vero lo da' la misura finale della cura, su
`150` passi.

## LE DOMANDE APERTE

1. ### **`κ` va DERIVATO, non scelto** *(`A1`)*. ### **Decisione di Luca.**
2. il pavimento **dentro** `dom` e' una **proiezione**: che cosa dice la fisica del caso
   `Δω = 0`? ### **Due nodi in fase perfetta hanno una torsione che non decade mai?**
3. il pavimento **esterno** e' inerte oggi: ### **va TOLTO o DERIVATO?** *(`A11`: se protegge
   da un errore, si cerca l'errore.)*

---

<!-- SCHEDA nome=mitosi-schwinger funzioni=mitosi,decidi_divisione flag=MITOSI_DIR,ANTIFASE_ADD,COPPIA_MIT,PLAST_MIT,KICK_TW,REGIME,MITOSI_2LAM -->

### ⛔ **AGGIORNAMENTO del 2026-10-06: LA MODULAZIONE DELLA SOGLIA DI MITOSI E'
USCITA** *(`MITOSI-SOGLIA-GRAD`, decisione di Luca sul referto `27c10bd`)*.

**La legge era** `soglia = soglia0 · (1 − 0.3·tanh|r_i − r_j|)` — la
soglia di `decidi_divisione` modulata dal gradiente del tempo proprio lungo l'arco.
### **Ora e' `soglia = soglia0` su OGNI arco.**

| | |
|---|--:|
| `R` sulle divisioni *(senza / con)* | ### **`0.1616`** |
| `R` sulla popolazione nella finestra | ### **`0.3417`** |
| nascite per `100` passi ### **senza** la modulazione | `48`-`150`, ### **stabili** |
| nascite per `100` passi ### **con** | fino a ### **`1044`**, ### **in accelerazione** |

> ### ✔ **LA CRESCITA NON ERA CREATA DALLA MODULAZIONE** *(`R` non e' zero: senza di
> lei la rete partorisce comunque)*, ### **ma CAMBIA FORMA: da accelerante a stabile.**
> ### **Si sceglie la forma senza**, ed e' `9-ter`: ### **a parita' di effetto si preferisce
> togliere un'eccezione** — e qui l'effetto ### **non e' nemmeno pari.**

**COSA ESCE DAL CODICE:** il blocco della modulazione; ### **`_r_nodo_mitosi`**, che resta
### **senza chiamanti**; e con lei i quattro contatori `A8` ### **`_tum_r_*`**.
### **ZERO righe di codice nuovo:** `soglia` era ### **gia'** `np.full(len(avv), soglia0)`,
e la modulazione ### **la sovrascriveva.**

> ### ⚠ **E LA SOGLIA `3π` NON E' TOCCATA:** `soglia0 = PHI_CRIT + twist_max`
> resta. ### **Il `π` di dipolo che in questa scena non esiste e' una DECISIONE
> SEPARATA di Luca**, col principio *«solo valori ricavati»*
> — ### **`2π + |twist_dip dell'arco|`** — da decidere ### **dopo la cura di
> `GEOM-SENZA-VERSO`**, su una misura a tre bracci.

**Il ramo che esce e' archiviato** in `csv/_archivio/_rami_off_mitosi_soglia_grad.py`, e si
rilancia dal tag ### **`pre-mitosi-soglia-grad-via`**.

---
### ⛔ **AGGIORNAMENTO del 2026-10-04, commit `6b`: IL CANCELLO DI `A13` ALLA NASCITA E'
DIVENTATO LEGGE INCONDIZIONATA, e `MITOSI_2LAM` E' UN FLAG INERTE.**

## `A13-NASCITA-LEGGE` — **un arco non nasce piu' corto della lunghezza d'onda**

*(commit `6b`, 2026-10-04. **Era `CURA 5` dietro il flag `MITOSI_2LAM`; ora e' LEGGE.**)*

### **LA FORMA**

```
un arco si divide  <=>  FRAZ_NASCITA * d >= LAM   AND   (1 - FRAZ_NASCITA) * d >= LAM
```

**senza condizione sul flag**, dentro `decidi_divisione`, accanto alla soglia di densita'.

### **LA DERIVAZIONE, e non e' una scelta**

Il figlio nasce a **`FRAZ_NASCITA * d`** dal genitore `a` e a **`(1 - FRAZ_NASCITA) * d`**
da `b`. ### **Quindi i tronconi sono DUE, e ciascuno deve rispettare `A13`**: un arco non
nasce piu' corto della lunghezza d'onda. ### **Due tronconi, due disuguaglianze.** Non c'e'
un numero da scegliere: `LAM` e' la scala della teoria e `FRAZ_NASCITA` esiste dal `6a`.

### **PERCHE' SOSTITUISCE `d >= 2*LAM`, e perche' a `t = 0.5` non cambia NIENTE**

A `FRAZ_NASCITA = 0.5` i due rami **coincidono** e la congiunzione si riduce a
`0.5*d >= LAM`, che e' `d >= 2*LAM` ### **al bit** — moltiplicare per `0.5` e per `2.0` e'
### **esatto in IEEE-754** *(potenze di due: la mantissa non cambia, cambia l'esponente)*.
### ⚠ **Limite dichiarato:** vale per `d` **finito e normale**; `d` ha un pavimento a
`0.05`, quindi il caso subnormale non si presenta — **ma e' una premessa sul dominio.**

### ⛔ **E CON UNA FRAZIONE DIVERSA DA META' IL CANCELLO VECCHIO GUARDA LA GRANDEZZA
SBAGLIATA:** a `t = 0.4` il troncone corto e' `0.4*d`, e `d >= 2*LAM` lo ammette anche
quando `0.4*d < LAM`. ### **Era corretto solo perche' la frazione era implicita.**

### **CHE COSA TOGLIE, ed e' il punto `A14`**

Senza il cancello gli archi sotto `LAM` **nascono comunque** e **`_nasce` li ALZA** —
cioe' **modifica una lunghezza dopo averla creata**. ### **Quella e' una PROIEZIONE, e
viola `A14` per costruzione QUALUNQUE SIA IL VALORE del pavimento.** Un cancello invece
**non modifica lo stato: rifiuta un evento.** ### **Non e' un taglio, e' un
NON-ACCADIMENTO.**

### ⚠ **E NON LO TOGLIE DOVE NON GUARDA: lo SCHWINGER resta scoperto**
*(`SCHW-SOTTO-LAM`, `46` troncamenti nel referto `1927b45`)*. La lunghezza dei suoi due
archi viene da **`pos`**, non da `d`, e il solo limite e' `np.maximum(..., 0.05)` — un
pavimento assoluto, non `LAM`. ### **`A11` applicato, `A13` no. La cura la decide Luca.**

### **IL CONTO DELLE LEGGI VA IN DIMINUZIONE** *(`9-ter`)*: prima **due** comportamenti
*(col flag e senza)*, ora **uno**. Il ramo <<senza>> e' **archiviato** in
`csv/_archivio/_rami_off_cura2.py`, e il flag resta **inerte come `PAV_COM`**
*(decisione 3 di Luca: si conserva tutto)*.

### **I CONTATORI, e perche' sono TRE invece di uno**

`negate` **mescolava** i rifiuti: un candidato scartato per densita' e uno scartato per
`LAM` erano **indistinguibili**. Ora: `_g_m2l_rif_solo_dens`, `_g_m2l_rif_solo_lam`,
`_g_m2l_rif_entrambi`, e la **somma dei tre** e' il totale dei rifiutati.
### ➕ **Piu' `_g_m2l_tw_rif`**, la lista di `|tw|` degli archi rifiutati per `LAM`: una
**diagnostica per il `6c`**, non una legge — e si tiene la **lista** e non la somma perche'
una **mediana** non si ricostruisce da una somma.

### ⛔ **RITIRATO il 2026-10-04: IL NUMERO QUI SOTTO VIENE DA UNA SCENA SBAGLIATA.**
Il sigillo del `6b` costruiva la scena con `nmasse = 2` e `sep = 3.0` **scritti a
mano** *(`H-P3`)*, mentre il driver passa **`--nmasse 3`** e **`--sep 6.1158`**:
`2208` nodi al passo 150 invece di `~12800`. ### **Sulla scena del driver il primo
candidato e' al passo `42`** — ### **come avevo misurato IO nel `6a`.**
### ⚠ **E la frase *«le scene da 72 passi non portano statistica del cancello»* e'
FALSA per la scena del driver.** ### **Il paragrafo resta visibile perche' il
reperto non si riscrive, ma NON si cita come misura.**

> ### 📌 **UN NUMERO MISURATO CHE CORREGGE IL PIANO:** su questa piattaforma
*(Windows, numpy 2.3.0, seme 11, con il flag)* il **primo candidato** alla divisione
arriva al passo **`74`**, non al 42 — e al passo `100` i candidati sono `7`, con `1`
rifiutato per `LAM` e `_g_m2l_dmin = 0.973`. ### ⚠ **Quindi le scene da 72 passi NON
portano statistica del cancello**, e i numeri del braccio `B3` vengono da `lunga` *(150
passi)*. ### **Il guardiano, su Linux/numpy 2.5.3, misurava `11` candidati a 72 passi: e'
la stessa differenza di piattaforma di `ROBUSTEZZA-FISICA`.**

### 📌 **E LA SCHEDA NUOVA STA QUI, non in coda al file, per una ragione di presidio:**
`H-REG-R` mappa le sezioni **da un marcatore al successivo**, quindi una scheda appesa in
fondo cadrebbe dentro la sezione dell'**ultima** scheda — e si leggerebbe come un
aggiornamento a `registro-grandezze`, che non ha niente a che vedere.
### ⚠ **E non le ho dato un marcatore PROPRIO**, perche' dichiarare
`funzioni=decidi_divisione` creerebbe **due schede proprietarie della stessa funzione** e
la mappa del hook diventerebbe ambigua. ### **Una legge nuova su una funzione che ha gia'
la sua scheda si scrive DENTRO quella scheda.**


## ⭐ **E DAL `COMMIT 6a` CINQUE PUNTI DI `mitosi` LEGGONO `FRAZ_NASCITA`**

*(decisione di Luca del 2026-10-03. La frazione e' dichiarata in un solo posto, accanto a
`PHI_CRIT`; la scheda del punto unico ne porta il quadro intero.)*

| dove, in `mitosi` | che cosa decide | come e' scritto ora |
|---|---|---|
| preparazione | ### **DOVE** nasce il figlio | `pos_figlio = (1-t)*pos[a] + t*pos[b]` |
| preparazione | ### **QUANTO** sono lunghi i due tronconi | `dh_a = t*d[sel]` · `dh_b = (1-t)*d[sel]` |
| ramo `MITOSI_DIR` | la ### **FASE** del figlio | `fm = phi[a] - (t + bias)*D` |
| ramo senza `MITOSI_DIR` | la ### **FASE** del figlio | `fm = phi[a] - t*D` |
| ramo ### **Schwinger** | ### **QUANTO** sono lunghi i due archi nuovi | `max(t*L, 0.05)` · `max((1-t)*L, 0.05)` |

### ⚠ **E IL `bias` DI `MITOSI_DIR` RESTA UNO SCOSTAMENTO *SOPRA* `t`:** il suo `0.5` e'
### **l'AMPIEZZA** *(lo tiene in `[-0.5, 0.5]`)*, non la frazione. ### **Due `0.5` con due ruoli
diversi sulla stessa legge, e distinguerli e' il punto.**

### 📌 **E L'ORDINE DEI DUE BLOCCHI NON E' ARBITRARIO:** segue `i = [keep, a, m]`, quindi
### **il PRIMO blocco e' `a`-`m` e vale `t*d`**, il secondo e' `m`-`b` e vale `(1-t)*d`. Lo stesso
nello Schwinger, dove `i = [.., aa, k]`. ### **A `t = 0.5` i due blocchi sono IDENTICI, ed e' per
questo che prima UNA sola `dh` bastava per entrambi.**

### ⛔ **E NON ERANO TRE, ERANO QUATTRO: la quarta l'ha trovata IL PRESIDIO.**
`_smp_chirurgia(nuovi=np.concatenate([dd, dd]))` nel ramo Schwinger faceva crescere lo
snapshot `_smp_d0` del ### **DOPPIO**, e `RIPIEGHI-ZERO` ha fermato il run al
### **primo passo con uno Schwinger**. ### 📌 **E il mio collaudo non poteva
vederla: 45 passi, scelti perche' la prima MITOSI e' al 42 — ma il primo SCHWINGER e'
al 70.** ### **Un collaudo tarato sul primo evento di UN tipo non dice niente
sull'altro**, ed e' `FALSO-ZERO` sull'asse temporale. ### ✅ **Curata, e il censimento
sistematico di OGNI uso di `dh`/`dd` nel perimetro dice che non ce ne sono altre.**

### ⚠ **E TRE REGOLE DELLA TABELLA SONO CAMBIATE DI CONSEGUENZA:** `_rn_div_d`, `_rn_sch_d`
e `_rn_sch_d0` consumavano `dh`/`dd` ### **due volte** *(`concatenate([d[keep], dh, dh])`)*. Ora
che sono ### **gia'** i due blocchi, le consumano ### **una volta sola** — con `dh, dh`
darebbero ### **`4n` archi.**

### ⚠ **`MITOSI_2LAM` e l'antifase NON sono toccati** *(e' il `6b`)*, e ### **`SCHW-CORTI` si
DICHIARA e non si risolve**: nella divisione la lunghezza viene da ### **`d`**, nello Schwinger da
### **`pos`**. Il `6a` mette `t` in entrambe ### **senza cambiare la sorgente**, e il pavimento
`0.05` resta com'e' *(e' un `A11`)*.


> ### ✅ **`NASCITA-PUNTO-UNICO` — LE REGOLE DI NASCITA SONO UNA TABELLA, E LA TABELLA E' IL CODICE** *(`COMMIT 3` del riordino, 2026-10-02)*
>
> ### **Non e' una legge nuova: e' il posto dove le leggi di nascita ABITANO.** E sta qui perche' ### **dove una legge si scrive e' un fatto di fisica**, non di programmazione: finche' le regole erano sparse in tre posti, ### **nessuno poteva elencarle** — e una legge che non si puo' elencare non si puo' nemmeno discutere.
>
> | | prima | ora |
> |---|---|---|
> | i **posti** che scrivono | ### **3** *(`mitosi`, i due `_eredita_*`, piu' la MUTAZIONE di `conc_nodi`)* | ### **1** *(`nascita()`)* |
> | le **regole** | sparse, e due in funzioni separate | ### **72 righe** in `REGOLE_NASCITA` *(36 grandezze x 2 eventi)* |
> | una grandezza **dimenticata** | passa in silenzio | ### **FERMA IL RUN** |
>
> ### 📌 **E LA TABELLA DICE COSE DI FISICA che prima erano sparpagliate.** Si legge in `doc/TABELLA_nascita.md` *(generato, non scritto a mano)*, e mette una accanto all'altra le regole che ### **differiscono fra i due eventi**:
>
> | grandezza | `divisione` | `schwinger` |
> |---|---|---|
> | `perc_chi` | **eredita** ⇒ sposta `N(+1)-N(-1)` di ### **`+segno`** per figlio | ### **eredita INVERTITA** ⇒ lo sposta di ### **`-segno`** |
> | `perc_geom` | eredita | ### **eredita NON invertita** — *la geometria non e' una carica e non si coniuga* |
> | `mem_mot` | **eredita** dal genitore | ### **zero** — *non continua un moto, comincia* |
> | `phi_s` | **eredita** dal genitore | ### **zero** |
> | `_rep`, `vd` | **eredita** dall'arco che si spezza | ### **zero** — *l'arco che si spezza non NASCE, CONTINUA* |
> | `peq` | **eredita** | ### **`nan`** = *da calibrare sul PROPRIO arco* |
> | `psi` | ### **MEDIA** *(come `phi`)* | ### **MEDIA** |
> | `psi_spin` | ### **EREDITA** *(come `phi_s`)* | ### **EREDITA**, ma qui `phi_s` e' **zero**: ### **asimmetria di OGGI, dichiarata** |
>
> ### ⚠ **L'ULTIMA RIGA E' UN RILIEVO, non una conferma:** la coppia `psi`/`psi_spin` segue *«la regola del proprio compagno»* — e nello Schwinger ### **il compagno di `psi_spin` non c'e' piu'**, perche' `phi_s` dell'antinodo e' zero. ### **Il commit 3 SPOSTA e non cura, quindi la lascia tale** — ma ora e' ### **VISIBILE in tabella** invece di essere sepolta in due funzioni diverse.
>
### ⛔ **E DAL 2026-10-06 LE GRANDEZZE SONO UNA DI PIU': `twp_dip`**
*(cura di `TORS-W8-AVVOLGIMENTO`, decisione di Luca)*

Il **dipolo precedente d'arco**, con regola di nascita ### **`nan`** per **entrambi** gli
eventi convertiti *(`_rn_div_twp_dip`, `_rn_sch_twp_dip`)* e una scrittura diretta in
`_allaccia` per la **semina**. ### ✔ **E IL PRESIDIO D'IMPORT L'HA PRETESA:**
`_nascita_collaudo_della_tabella()` alza un `RuntimeError` se una grandezza del registro non
ha una regola per ogni evento convertito — ### **aggiungere il campo senza le regole non
sarebbe compilato.**

### ✔ **E IL VINCOLO 4 REGGE, verificato:** `twp_dip` sta al posto **`33`**, `twp` al `32`,
### **`perc_geom` al `31` e `tw` al `30`** — cioe' `perc_geom` e' **ancora** subito dopo `tw`,
e i due `raise` di `:1467` lo confermano all'import.

> ### ✅ **E L'ORDINE E' MISURATO, non assunto** *(`csv/_test_fork/_ordine_registro.py`)*: l'ordine del **registro** e' un ordine ### **topologico valido** — **4 vincoli genuini, 0 violazioni**. `phi` prima di `twp` · `peq` prima di `_peqn_idx` · `n0` nel **contesto** · le **6 chiamate con effetto** collocate a mano.
>
> ### ⛔ **CORREZIONE DEL 2026-10-03, su rilievo del guardiano: CINQUE DERIVAZIONI DI
> ### QUESTA TABELLA AFFERMAVANO UN BILANCIO CHE NESSUNO HA MISURATO** — e la riga
> ### `perc_chi` qui sopra era una di esse.
>
> | | diceva | dice ORA, e perche' |
> |---|---|---|
> | `tw` | *<<la torsione e' stata ### **SCIOLTA** dalla divisione, ed e' cio' che il calcio
> ha ### **SPESO**>>* | ### **FALSA.** Il calcio ### **USA `|tw|` come MISURA** di quanto
> colpire, e ### **NON trasferisce l'avvolgimento**: `DIVISIONE-AUTOCONSISTENTE:M1` ha
> misurato ### **~1.2 giri persi per arco diviso, SENZA BILANCIO**. ### **Se debba
> conservarsi e' una domanda APERTA** |
> | `perc_chi`, ### **entrambi gli eventi** | *<<e' il ramo che ### **CONSERVA**: la coppia
> e' NEUTRA e `N(+1)-N(-1)` NON cambia>>* | ### **VERA DELLA COPPIA, FALSA DEL RAMO.**
> L'antinodo ### **da solo** sposta la carica di `-segno(perc_chi[aa])`; i due rami si
> cancellano ### **SOLO sugli archi dove scattano ENTRAMBI**, e lo Schwinger scatta su un
> ### **sottoinsieme** (`pick`) |
> | `schwinger`/`conc_nodi` | *<<la Schwinger ### **DRENA** tensione di una massa
> esistente>>* | ### **un trasferimento non misurato.** Quella regola ### **copia una lista
> e le mette una marca** — che la coppia dreni la massa e' una lettura ### **plausibile**,
> non una misura |
> | `d0` | *<<proporzionale alla torsione ### **sciolta**>>* | la frase e' esatta, ma
> ### **il NOME `sciolta` presuppone il bilancio**: e' solo `|tw|/PHI_CRIT`. ### **Il nome
> non si cambia in un commit di commenti:** e' in coda |
>
> ### 📌 **E IL NUMERO CHE SMONTA LA CONSERVAZIONE ERA GIA' COMMITTATO:** 72 passi,
> seme 11 — ### **`_g_nati_mitosi = 9` contro `_g_nati_schwinger = 1`**, cioe'
> `N(+1)-N(-1)` si e' spostato di ### **+8** in quel run
> *(`csv/_test_fork/_sonda_commit3/_sonda_commit3.json`, `nati_dopo`)*.
> ### ⛔ **I DUE CONTATORI ESISTONO PROPRIO PER DISTINGUERE LE DUE COSE, e la frase era
> ### scritta come se non esistessero.**
>
> ### ✅ **E LE FRASI VECCHIE RESTANO CITATE, nelle derivazioni e qui: un errore non si
> ### cancella, si ANNOTA** (par.8). ### **Trovate col setaccio** *(`csv/_test_fork/_setaccio_derivazioni.py`: 9 segnalate su 72, e il giudizio e' 5 da
> riscrivere e 4 non-fisica)*.

<!-- SCHEDA nome=veleno-derivate funzioni=_avvelena_derivate,_riallinea_derivate_arco flag=NASCITA_DERIVATA,REGISTRO_DERIVATE -->

# **`veleno-derivate` — IL VELENO: le derivate dei nati nascono `NaN`**

> ### **Quando nasce un nodo, le sue derivate sono SPORCHE; leggerne una e' un ERRORE;
> tornano pulite quando la loro legge le riscrive.**
> ### **E il VELENO e' il modo in cui quella regola diventa una LEGGE DEL SISTEMA** invece
> di un accertamento fatto una volta con una misura.

*(`COMMIT 4` del riordino. Terza via del par.(d), **approvata da Luca il 2026-10-01** nella
forma raffinata; **VIA A** scelta il 2026-10-03 dopo la misura della copertura.)*

## **LA FORMA**

```
_avvelena_derivate(net)      # alla FINE di nascita(), per EVENTO
    per ogni voce di REGISTRO_DERIVATE:
        se la CLASSE DI NASCITA e' `auto-rinfresco`  ->  SI SALTA (esente)
        altrimenti, se e' CORTA  ->  si estende con `NaN` fino a `n` (o `m`)
```

| | |
|---|---|
| **dimensioni** | ### **nessuna**: `NaN` non ha unita'. Il veleno non introduce una formula |
| **cosa LEGGE** | `len(net.phi)`, `len(net.i)`, e la ### **CLASSE** dal registro |
| **cosa SCRIVE** | le voci di `REGISTRO_DERIVATE` di classe `avvelena`, ### **solo in coda** |
| **limiti** (`A11`) | ### **nessun clip, nessun pavimento.** I quattro rami che NON avvelenano *(esente, assente, multiasse, non-float, gia'-lunga)* sono ### **CONTATI, non taciuti** |

## ### ✅ **PERCHE' IL VELENO E NON UNA MARCA LETTA A OGNI ACCESSO**

Intercettare **la lettura** costa: la sorveglianza ha misurato ### **1 887 282 accessi per
passo.** Il veleno non costa niente a chi legge: ### **una lettura sporca PROPAGA il `NaN`
nello stato, e il controllo lo prende al confine successivo** — e un controllo di
finitezza su tutte e 30 le voci di stato costa `0.002085 s`, lo ### **0.073 %** di un passo.

### 📌 **E NON E UNA CONVENZIONE NUOVA: IL SISTEMA LO FA GIA IN DUE PUNTI.** `peq`
nasce `nan` in `_allaccia` *(`# da calibrare`)* e nello Schwinger con `PEQ_NASCITA_LOCALE`,
e `step` la ### **CALIBRA**. ### **<<derivata sporca>> e <<`peq` da calibrare>> sono LA
STESSA COSA**, e per `9-ter` questo conta: il commit 4 ### **da' un NOME a cio' che il
sistema fa gia'.**

## ### ⚠ **LE DUE ESENTI, e l'esenzione LA DICHIARA IL REGISTRO**

| | la guardia | con il veleno, se NON fosse esente |
|---|---|---|
| `_xi_rumore` `:5031` | `if _xi is None or len(_xi) < n:` | estendere la rende ### **FALSA** ⇒ ### **l'estrazione fresca NON avviene** ⇒ i nati prendono `NaN`. E il commento dichiara che quello e' ### **<<IL PERCORSO NORMALE della mitosi>>** |
| `_g_rampa_prec` `:5704` | `if ... len(_prec) == len(ramp):` | estendere la rende ### **VERA** ⇒ `ramp < _prec` confronta con `NaN` ⇒ ### **False in silenzio**, e il ramo che conta il disallineamento ### **smette di scattare** |

### ➜ **IL DISALLINEAMENTO DI LUNGHEZZA *E* IL SEGNALE con cui quelle due si
ripuliscono**, e riempirle di `NaN` lo distruggerebbe. ### **MISURATO: 99 letture sporche
ciascuna, su tre scene** *(`csv/_test_fork/_copertura_derivate/`)*.

### ✅ **E L'ESENZIONE E NEL REGISTRO, NON NEL CODICE DEL VELENO:** `REGISTRO_DERIVATE`
ha una colonna ### **CLASSE DI NASCITA** col vocabolario `NASCITA_DERIVATA`, e
`_avvelena_derivate` ### **la legge da la'.** ### **Un elenco scritto nel veleno sarebbe
una seconda fonte, e divergerebbe.**

## ### ⚠ **E NON HA UN FLAG, ED E UNA SCELTA**

Un flag renderebbe il presidio ### **un'opzione** — ed e' il difetto che `E4-LAM` ha
curato *(<<il controllo era legge, chi la faceva rispettare era un'opzione>>)* e che
`_nasce` dichiara di aver tolto *(<<IL GATE E' TOLTO: il presidio agisce SEMPRE>>)*.

## ✅ **L'ESENZIONE PER CELLA, ANCORATA AL VELENO** *(via (a), decisione di Luca, 2026-10-03)*

### **E' IL TERZO CASO DELLA STESSA ESENZIONE**, e per `9-ter` questo e' il punto: non e'
una legge nuova, e' la ### **terza volta che si usa la stessa.**

| | la forma | l'ancora |
|---|---|---|
| `eta` | esenzione sull'### **INTERO DOMINIO** | la **forma** `nonneg_inf` |
| `peq` | esenzione ### **PER CELLA** | la **marca** `_peqn_idx` |
| ### **le derivate avvelenate** | esenzione ### **PER CELLA** | il ### **registro del veleno** `_veleno_registro` |

### **COME FUNZIONA**

| | |
|---|---|
| **1** | `_avvelena_derivate` registra, per ogni derivata avvelenata, le ### **celle** `[inizio:fine]` e ### **il RIFERIMENTO all'array** che ha scritto |
| **2** | se il registro e' ### **VIVO** *(stesso oggetto)*: nelle celle avvelenate il valore ### **DEVE essere `nan`** — ### **stretto nei DUE versi** — e ### **fuori** da quelle celle vale il dominio dichiarato, come prima |
| **3** | se l'oggetto e' ### **CAMBIATO** *(la legge ha riscritto la derivata)*: il registro e' ### **SCADUTO**, si cancella, e il dominio si applica ### **PIENO** |

### ⛔ **IL SECONDO VERSO E' IL PUNTO, e senza di lui l'esenzione sarebbe `A9`:** un
### **NUMERO** in una cella avvelenata vuol dire che qualcuno ha scritto ### **UNA CELLA
senza riscrivere la derivata** — e quello e' un ### **DIFETTO DA NOMINARE**, non
un'esenzione. ### **Un'esenzione che ammettesse anche i numeri non impedirebbe niente.**

### ✅ **E SI TIENE IL RIFERIMENTO, NON `id()`, ED E' PIU' FORTE:** un `id` si puo'
### **RIUSARE** dopo che l'oggetto e' stato liberato, e allora un registro ### **scaduto
sembrerebbe VIVO.** Tenendo il riferimento l'oggetto non puo' essere liberato, quindi `is`
e' ### **esatto.** Il prezzo e' ### **una copia stantia per derivata**, che vive al massimo
fino al prossimo `verifica_invarianti`.

### ⚠ **IL LIMITE, DICHIARATO:** una modifica ### **IN POSTO** conserverebbe
l'identita', quindi il registro sembrerebbe ### **vivo** mentre la derivata e' stata
ricalcolata — e le celle, ora piene di numeri veri, verrebbero ### **nominate come
difetto.** ### ✅ **MISURATO: ZERO modifiche in posto sulle dieci derivate**, e il
rilevatore ha il suo ### **controllo positivo cablato**
*(`csv/_test_fork/_copertura_derivate/`; il blob del referto e' citato dal braccio `D` del
sigillo)*.

### 📌 **E IL COLLAUDO DICE CHE FUNZIONA** *(72 passi, seme 11)*: il run ### **arriva
in fondo**, ### **71** celle `nan` esentate, ### **29 registri SCADUTI** cancellati *(cioe'
la rilevazione dell'oggetto riscritto gira davvero)*, e le due esenti restano ### **corte**
*(12811 contro 12812)* con ### **zero `nan`**.

---

## ⛔ **E UNA MEZZA VERITA' DI QUESTA SCHEDA, CORRETTA DAL SIGILLO** *(2026-10-03)*

La tabella delle due esenti diceva che l'esenzione protegge `_xi_rumore` dal veleno.
### ⚠ **Oggi NON e' lei a proteggerla:** `_xi_rumore` ha shape ### **`(12802, 3)`** — ### **DUE ASSI** — quindi il ramo `multiasse` di `_avvelena_derivate` ### **la salterebbe COMUNQUE.**

### ✅ **E L'HA MISURATO IL BRACCIO `B` DEL SIGILLO**, al primo giro: togliendole l'esenzione ### **non cambiava niente**, e il contatore ### **`_g_veleno_multiasse`** e' comparso. ### **Un ramo CONTATO invece di taciuto e' la ragione per cui questo si e' visto** — e l'avevo scritto *<<per prudenza, con ZERO casi oggi>>*: ### **ne aveva uno.**

### 📌 **L'esenzione resta GIUSTA come DICHIARAZIONE D'INTENTO** *(morderebbe se un domani `_xi_rumore` diventasse 1-D)*, ### **ma dire che e' lei a proteggerla oggi era falso.** ### ➜ **E per questo il braccio `B` e' ancorato a `_g_rampa_prec`**, che e' `(12802,)` 1-D e quindi ### **davvero avvelenabile.**

### ⚠ **E LA MIA DICHIARAZIONE <<tutte e dieci sono 1-D>> ERA SBAGLIATA:** il piano diceva *<<tutte e 10 sono `float64`>>*, e io ho letto ### **1-D.** ### **Nove su dieci lo sono.**

---

## ### ⛔ **IL LIMITE CHE IL PRIMO COLLAUDO HA TROVATO: `VELENO-DOMINI`**

Il veleno ### **fa cadere il run al passo 42**, alla ### **prima mitosi**:
`DominioViolato` — `_dt_e_ultimo` viola `> 0`, 1 elemento, indice `471564`, valore `nan`,
arco `12802-1583`.

### **LA CAUSA:** `DOMINI` ha 42 voci e ### **NOVE sono derivate**; `verifica_invarianti`
le controlla ### **come se fossero STATO**, quindi una derivata avvelenata ### **viola il
suo dominio PER COSTRUZIONE.**

### 📌 **E NON E UN DIFETTO SCOPERTO NEL SIMULATORE: E IL VELENO CHE HA TROVATO SE
STESSO.** Nessuna ### **LEGGE** ha letto la derivata sporca — l'ha vista il
### **PRESIDIO**, ed e' il suo lavoro.

### ✅ **IL PEZZO CHE MANCA, e il piano lo prevedeva:** *<<il controllo di finitezza e'
PER GRANDEZZA, con l'esenzione DICHIARATA NEL REGISTRO>>*. La forma esiste ### **due
volte**: `DOMINI['peq'] = ('peq', …)` ammette `nan` sugli archi,
`DOMINI['eta'] = ('nonneg_inf', …)` ammette `+inf`. ### **Serve la TERZA: una forma di
dominio per le derivate AVVELENATE**, che ammetta `nan` ### **dove il veleno l'ha messo e
solo la'.** ### ⛔ **NON implementata: tocca il presidio centrale, e la forma e' una
scelta di Luca.**

## ⭐ **LA CURA DI `VELENO-ARCHI-KEEP`: `keep` SI APPLICA ANCHE ALLE DERIVATE D'ARCO**
*(decisione di Luca del 2026-10-05, **VIA (i)**; misura del passo (1) in
`doc/REFERTO_veleno_archi_keep_2026-10-05.md`)*

> ### **IL VELENO ERA MEZZO-CIECO, e il numero che lo dice e' `0.5000`.**

**IL DIFETTO, misurato e non letto.** La nascita ricostruisce le colonne d'arco con
`concat(x[keep], ...)`: **toglie** archi e ne **aggiunge** in coda. `_avvelena_derivate`
allungava **solo in coda** con `NaN`, e ### **non applicava `keep`** — la parola non
compariva **mai** in quella funzione. ### **Quindi dal primo arco tolto in poi ogni arco
leggeva il valore di UN ALTRO arco: un valore FINITO, che il veleno non segnala.**

**IL CONTO, e il numero:** con `s` archi divisi, tolti `s` e aggiunti `2s`, il veleno
appendeva `(m+s) - m = s` celle su `2s` archi nuovi.

| | copertura del veleno | misurata |
|---|--:|---|
| eventi di **divisione** *(usano `keep`)* | ### **`0.5000`** | `min = max` su 166 confronti |
| eventi **Schwinger** *(non lo usano)* | **`1.0000`** | `min = max` |

### ⛔ **E L'UNICA DIFFERENZA FRA I DUE CASI ERA `keep`.** La prima posizione diversa
coincideva col **primo arco tolto** in **`166` confronti su `166`** — non in media, in
tutti. E la frazione di archi conservati che leggeva il valore di un altro arco aveva
**mediana `0.9306`**: ### **nella meta' degli eventi, piu' del 93%.**

**LA FORMA DELLA CURA:** `_riallinea_derivate_arco(net, evento, c)`, chiamata
**immediatamente prima** di `_avvelena_derivate`. ### **Il veleno resta dov'e': la cura
sta PRIMA di lui.**

### **PERCHE' PRIMA, e non dentro il veleno:** il veleno allunga fino alla lunghezza
**NUOVA** *(e il suo commento lo dichiara)*; il riallineamento vuole quella **VECCHIA**,
cioe' `len(keep)`. ### **Sono due istanti diversi, e metterli nella stessa funzione
vorrebbe dire darle due bersagli.**

### **E DOPO LA CURA:** `len(v) = sum(keep) = m - s`, quindi il veleno appende
`(m+s) - (m-s) = `**`2s`** celle — ### **copertura `1.0000` in ENTRAMBI i casi.**
### **La cura non aggiunge un comportamento: estende al caso che gli sfuggiva quello che
il veleno faceva GIA' nell'altro** — e per `9-ter` ### **toglie un'eccezione**, perche'
oggi le colonne d'arco si riallineano e le derivate d'arco **no**.

**I VINCOLI, come la decisione di Luca li fissa:** `keep` dal **contesto** `c['keep']`
e ### **mai ricostruito**; solo le derivate d'**arco** con classe **`avvelena`**, lette
dal **`REGISTRO_DERIVATE`** e ### **non da un elenco a mano**; solo gli eventi che
**hanno** `keep`; e se la lunghezza non e' quella degli archi di **prima**,
### **`_ferma_registro`** — ### **non si indovina** *(`RIPIEGHI-ZERO`, `A9`)*.
**Nessun flag:** *«il veleno agisce sempre»*, e ### **questa e' la riparazione di un
difetto, non un esperimento.**

### ⚠ **LA VIA SCARTATA, e il perche':** la via `(ii)` — far **ricalcolare** `dt_e` a
chi lo legge — curava ### **un lettore solo**, lasciava `_sin2_vir` col difetto, e
### **aggiungeva una SECONDA SCRITTURA** della legge di `dt_e`. *(Decisione di Luca.)*

### 📌 **E UNA CONSEGUENZA CHE IL PASSO (2) DI `TETTO-CAUSALE-TEMPO-COORDINATO` DEVE
### AFFRONTARE, e NON si decide adesso**

> ### ⛔ **Dopo questa cura, gli archi NATI nel passo hanno `dt_e = NaN`** — prima
> avevano un valore **finito preso da un altro arco**, che e' peggio ma **non si
> vedeva**.
> ### **Quindi il passo (2) del tetto causale — che vuole far leggere `dt_e` a
> `memoria_hebbiana_moto`, cioe' alla voce 5, DOPO la nascita — avra' bisogno di una
> REGOLA per gli archi nati in quel passo.**
> ### ⚠ **E' una DECISIONE DI LUCA, da prendere ALLORA e non adesso.** Qui si registra
> **che serve**, non **quale**.

**IL SIGILLO:** `csv/_seal_fork/_sigillo_veleno_keep.py`; la patch del braccio 0 e'
`csv/_seal_fork/_veleno_keep_patch.py`. **Simulatore curato: `e2940b3c`**
*(da `0f060670`)*.

## **Criteri, fissati PRIMA dei numeri** *(il sigillo e' `csv/_seal_fork/_sigillo_veleno.py`)*

| | |
|---|---|
| ### **`A`** | lo ### **STATO** byte-identico sulle ### **tre scene**, e le ### **DERIVATE NO** — il prezzo ### **dichiarato e ACCETTATO**. E `A` ### **verifica che le derivate DIFFERISCANO**: se fossero identiche il veleno ### **non avrebbe fatto niente** |
| ### **`B`** | il ### **caso che DEVE fallire**: si ### **toglie l'esenzione** a `_xi_rumore` ⇒ il run deve ### **ROMPERSI, con voce e riga** |
| **`C`** | le ### **due esenti NON avvelenate**: restano ### **CORTE**, senza `NaN` |
| **`D`** | il verdetto della ### **COPERTURA**, ### **CITATO** dal referto committato col suo blob *(`L-NUMERI`)* |

---

<!-- SCHEDA nome=nascita-punto-unico funzioni=_derivazione_perc_geom,_nascita_collaudo_della_tabella,_nascita_collocata,_nascita_non_si_tocca,_nascita_regola,_ordine_di_nascita,_registra_regola,_rn_div_conc_nodi,_rn_div_cs_nodo_prev,_rn_div_d,_rn_div_d0,_rn_div_eta,_rn_div_i,_rn_div_j,_rn_div_mem_mot,_rn_div_nb,_rn_div_nb_prec,_rn_div_nb_ret,_rn_div_omega_s,_rn_div_peq,_rn_div_perc_chi,_rn_div_perc_geom,_rn_div_perc_tw,_rn_div_phi,_rn_div_phi0,_rn_div_phi_s,_rn_div_phivel,_rn_div_pos,_rn_div_psi,_rn_div_psi_prec,_rn_div_psi_spin,_rn_div_psi_spin_prec,_rn_div_psi_spinor,_rn_div_rep,_rn_div_rho_spin,_rn_div_spinor_lift,_rn_div_tw,_rn_div_twp,_rn_div_twp_dip,_rn_div_vd,_rn_sch_conc_nodi,_rn_sch_cs_nodo_prev,_rn_sch_d,_rn_sch_d0,_rn_sch_eta,_rn_sch_i,_rn_sch_j,_rn_sch_mem_mot,_rn_sch_nb,_rn_sch_nb_prec,_rn_sch_nb_ret,_rn_sch_omega_s,_rn_sch_peq,_rn_sch_peqn_idx,_rn_sch_perc_chi,_rn_sch_perc_geom,_rn_sch_perc_tw,_rn_sch_phi,_rn_sch_phi0,_rn_sch_phi_s,_rn_sch_phivel,_rn_sch_pos,_rn_sch_psi,_rn_sch_psi_prec,_rn_sch_psi_spin,_rn_sch_psi_spin_prec,_rn_sch_psi_spinor,_rn_sch_rep,_rn_sch_rho_spin,_rn_sch_spinor_lift,_rn_sch_tw,_rn_sch_twp,_rn_sch_twp_dip,_rn_sch_vd,nascita flag=FRAZ_NASCITA,REGOLE_NASCITA,ORDINE_DI_NASCITA,EVENTI_DI_NASCITA,EVENTI_CONVERTITI -->


## ⭐ **E DAL 2026-10-05 `nascita` HA UNA CHIAMATA IN PIU', PRIMA DEL VELENO**
*(cura di `VELENO-ARCHI-KEEP`, **VIA (i)**, decisione di Luca)*

L'ordine dentro `nascita` e' ora: **le regole** -> **`_riallinea_derivate_arco`** ->
**`_avvelena_derivate`**.

### **PERCHE' LA NUOVA CHIAMATA STA FRA LE DUE, e non altrove:** le **regole** lasciano
le colonne d'arco alla lunghezza **NUOVA** *(`concat(x[keep], ...)`)* e le **derivate**
d'arco a quella **VECCHIA**; il **veleno** allunga fino alla nuova.
### ⛔ **In quella finestra le derivate d'arco sono DISALLINEATE, e fino al 2026-10-05
ci restavano:** il veleno appendeva `NaN` in coda **senza applicare `keep`**, quindi
ogni arco dopo il primo tolto leggeva il valore di **un altro arco** — un valore
**finito**, che il veleno non segnala.
### ✅ **La chiamata nuova chiude quella finestra**, e la misura del passo (1) dice di
quanto: copertura del veleno da **`0.5000`** a **`1.0000`** negli eventi di divisione.
### **Il dettaglio della cura vive nella scheda `veleno-derivate`**, che e' la sua casa.

### ⚠ **E LA TABELLA DELLE REGOLE NON CAMBIA:** la cura **non e'** una regola di
nascita, e non compare in `REGOLE_NASCITA`. ### **Agisce su una CACHE, non su una
grandezza del registro** — ed e' per questo che non vuole una riga nella tabella e non
fa scattare il presidio delle grandezze non dichiarate.
# **`nascita-punto-unico` — IL PUNTO UNICO DI NASCITA, e le sue 72 regole**

## ⭐ **E DAL `COMMIT 6a` LA FRAZIONE DELLA NASCITA E' UN VALORE DICHIARATO: `FRAZ_NASCITA`**

### ✅ **E IL NOME E' `FRAZ_NASCITA`, NON `t`, per decisione di Luca** *(2026-10-03)*:
e' una ### **FRAZIONE dell'arco**, un numero puro in `[0,1]` misurato dal genitore
`a`/`aa` — e nel simulatore ### **`t` e `dt` sono TEMPI** *(`dt_e`, il tempo proprio
dell'arco)*. ### **Chiamarla `t` avrebbe messo una lunghezza adimensionale nello stesso
alfabeto dei tempi.**

*(decisione di Luca del 2026-10-03.)*

> ### **Il figlio sta a `FRAZ_NASCITA * d` dal genitore `a` e a `(1 - FRAZ_NASCITA) * d` da `b`, e lo
> ### STESSO valore vale per DOVE nasce, per QUANTO sono lunghi i suoi archi, e per la sua FASE.**

### **I SEI SITI che lo leggono** *(prima erano sei formule indipendenti che per caso dicevano
tutte *<<meta'>>*)*:

| dove | che cosa decide | la forma |
|---|---|---|
| `mitosi`, preparazione | ### **DOVE** nasce il figlio | `pos_figlio = (1-t)*pos[a] + t*pos[b]` |
| `mitosi`, preparazione | ### **QUANTO** sono lunghi i due tronconi | `dh_a = t*d[sel]` · `dh_b = (1-t)*d[sel]` |
| `mitosi`, ramo `MITOSI_DIR` | la ### **FASE** del figlio | `fm = phi[a] - (t + bias)*D` |
| `mitosi`, ramo senza | la ### **FASE** del figlio | `fm = phi[a] - t*D` |
| `_rn_sch_pos` | ### **DOVE** nasce l'antinodo | `(1-t)*pos[aa] + t*pos[bb]` |
| `mitosi`, ramo Schwinger | ### **QUANTO** sono lunghi i due archi nuovi | `max(t*L, 0.05)` · `max((1-t)*L, 0.05)` |

### ⛔ **NON E' UN FLAG, ed e' una scelta:** un flag renderebbe la frazione ### **un'opzione**,
e ### **dove nasce un figlio non e' un'opzione: e' la legge.** E' il difetto `E4-LAM`, pagato una
volta.

### ⚠ **E LE EREDITA' DI STATO NON LA LEGGONO** *(decisione di Luca)*: `psi` e `phivel`
restano ### **medie**, la famiglia dello ### **spinore** resta una ### **copia** *(col segno `-1`
nello Schwinger)*, `rho_sel` del cancello resta com'e'. ### **Si decidono nella LEGGE di
`DIVISIONE-AUTOCONSISTENTE`, che viene DOPO la definizione dell'energia perche' deve rispettare
`A14`.**

### ✅ **LA FORMA E' CONVESSA, E NON E' COSMETICA:** `(1-t)*x + t*y` e' ### **identica al
bit** a `0.5*(x+y)` a `t = 0.5` *(0 differenze su 2 000 000)*, mentre la lerp `x + t*(y-x)`
### **NO** *(576 135 su 2 000 000)*. ### **Misurato prima di scrivere**
*(`csv/_test_fork/_somma_meta/`)*.

### ⚠ **E `SCHW-CORTI` SI DICHIARA, non si risolve:** nella divisione la lunghezza viene da
### **`d`**, nello Schwinger da ### **`pos`** *(`norm(pos[aa]-pos[bb])`)*. ### **Il `6a` mette `t`
in entrambe SENZA cambiare la sorgente.** E il pavimento `0.05` dello Schwinger resta com'e': e'
un `A11`, non del `6a`.

## ⭐ **E `_nasce` IMPARA A SOMMARE PER META', perche' un contatore e' un FLOAT**

`_nasce(v, dove, md, md0, meta=None)`. Con `meta` dato, `_fab` *(la lunghezza fabbricata,
`sum(LAM - v)` sui troncati)* si calcola ### **per meta' e poi si somma.**

### **PERCHE', e il motivo e' MISURATO:** `dh` passava da `_nasce` con ### **`md = 2` su `n`
voci**; col `6a` e' un array di ### **`2n`** e passa con ### **`md = 1`** — e ### **una sola
chiamata**, perche' `_g_sm_nascite` conta le ### **INVOCAZIONI** e spezzarla la farebbe salire di
`2` invece di `1`.
### ⛔ **Ma `np.sum` su `2n` NON e' identica al bit a `2 * np.sum` su `n`:** ### **4043
differenze su 14000** *(misurato)*. ### ✅ **La somma per META' a `t = 0.5` e' `s + s`, e
`s + s == 2*s` e' ESATTO** — il raddoppio e' uno scalamento per una potenza di due.

### 📌 **E VALE SU DUE PERCORSI, non uno:** `dh` *(`mitosi`, `2,0` → `1,0`)* **e**
`dd` *(`schwinger`, `2,2` → `1,1`)*. ### **`d0new` RESTA com'e'** *(`0,1`)*: e' gia' l'array
dei due figli, e la sua somma e' gia' sull'array intero.
### ✅ **VERIFICATO PRIMA DI SCRIVERE: a `t = 0.5` tutti e QUATTRO i contatori, per tutti e
TRE i siti, identici al bit** — zero differenze su 2000 prove per sito, con valori che
### **includono lunghezze sotto `LAM`** *(altrimenti `_ntr` e `_fab` sarebbero zero per
costruzione, e la verifica sarebbe essa stessa un `FALSO-ZERO`)*.

### ⚠ **E TRE REGOLE DELLA TABELLA SONO CAMBIATE, e non era nel mandato:** `_rn_div_d`,
`_rn_sch_d` e `_rn_sch_d0` consumavano `dh`/`dd` ### **DUE volte**
*(`concatenate([d[keep], dh, dh])`)*. Ora che `dh`/`dd` sono ### **gia'** i due blocchi, le
consumano ### **una volta sola** — con `dh, dh` darebbero ### **`4n` archi.** Le loro
### **ancore dichiarate** sono aggiornate insieme al corpo.

### ⛔ **E NON ERANO TRE: ERANO QUATTRO.** La quarta e' la ### **chiamata con effetto**
`_smp_chirurgia(nuovi=np.concatenate([dd, dd]))` del ramo Schwinger, che faceva crescere
lo snapshot `_smp_d0` del ### **doppio**. ### **L'ha trovata il presidio `RIPIEGHI-ZERO`**,
non il mio collaudo — che era di ### **45 passi**, scelti perche' la prima **mitosi** e'
al 42, ### **mentre il primo SCHWINGER e' al 70.**
### 📌 **Un collaudo tarato sul primo evento di UN tipo non dice niente sull'altro:**
e' `FALSO-ZERO` sull'asse temporale, la stessa forma che il commit 4 ha gia' pagato.

### ⚠ **E CINQUE DERIVAZIONI DICHIARATE ERANO SCADUTE, scritte dalla patch stessa:**
`_rn_div_d` diceva ancora `dh = d[sel]/2` e `_nasce('mitosi', 2, 0)`; `_rn_div_d0` citava
`[d0h, d0h]`, e ### **`d0h` non esiste piu'**; `_rn_sch_d` diceva ancora
`dd = max(0.5 * norm(...), 0.05)`. ### **Un'ancora dichiarata e' PARTE della regola, non un
commento:** lasciarla scaduta e' il difetto che `H-P7` esiste per impedire.
### ✅ **Corrette, e il censimento di OGNI uso di `dh`/`dd` nel perimetro dice che non ce
ne sono altre.**

## ✅ **E DAL `COMMIT 5` UNA REGOLA NON EREDITA PIU': `perc_geom` SI DERIVA**

*(decisione di Luca del 2026-09-29, `doc/relazioni/2026-09-29.md` e `doc/MITOSI_storia.md`.)*

### **LA LEGGE, ed e' la STESSA di `chi_basc`:** `perc_geom` del nato vale ### **`+1` se la media
di `|tw|` sugli archi del nodo supera `PHI_CRIT`, altrimenti `-1`.** La scrive
`_derivazione_perc_geom`, chiamata dalle due regole `_rn_div_perc_geom` e `_rn_sch_perc_geom`.

### ⛔ **PRIMA EREDITAVA, E L'EREDITA' POTEVA CONTRADDIRE LA DEFINIZIONE.** Il nato prendeva il
valore del genitore *(`a` per la divisione, `aa` per lo Schwinger, **non** coniugato)*, mentre i
suoi archi nascono con `tw = 0` ### **⇒ la definizione dice `-1`.** E ### **quel valore entra
nella dinamica per UN passo:** `PASSO_COMPOSIZIONE` mette `step` **prima** di `mitosi`, quindi al
passo dopo il ### **frame-drag legge `perc_geom`** *(`:7368`, `chiralita_core_locale(…, geom=True)`)*
### **PRIMA** che `chi_basc` *(`:7560`)* lo riporti alla definizione.

### 📌 **PERCHE' UNA DERIVAZIONE E NON LA COSTANTE `-1`** *(ed e' il cuore della decisione)*:
oggi i due numeri **coincidono**. ### **Ma `DIVISIONE-AUTOCONSISTENTE`, se dara' ai figli una
torsione diversa da zero, cambierebbe la risposta** — e una costante resterebbe `-1`
### **sbagliata in silenzio.**

### ⚠ **E IL VINCOLO 4 DEL CONTRATTO NASCE DA QUI, e NON e' un riordino di comodo**

| | |
|---|---|
| nell'ordine del registro | `perc_geom` cadeva al posto ### **17**, `tw` al ### **31** |
| cioe' | ### **la derivazione avrebbe letto il `tw` dei nuovi archi PRIMA che esistesse** |
| e avrebbe dato | `-1` ### **per il motivo sbagliato: la costante travestita da derivazione** |

### ➜ **`perc_geom` si colloca DOPO `tw`** *(ora posto `31`, `tw` al `30`; l'ordine resta di
**36** voci: ### **sposta, non aggiunge ne' toglie**)*, con la stessa forma del vincolo `2`
*(`_peqn_idx` dopo `peq`)*. ### **E' una DIPENDENZA DI LETTURA**, e ha ### **due presidi** che
sollevano se `perc_geom` o `tw` uscissero dai registri — perche' `A9`: **un vincolo scritto non e'
un presidio.**

### ⚠ **LE DUE DIFFERENZE DA `chi_basc`, DICHIARATE e non nascoste:**

| | `chi_basc` | la derivazione alla nascita |
|---|---|---|
| il grado | `self._deg` | ### **RICALCOLATO da `i`/`j`** — `_grado()` e' `collocata` e gira **DOPO** `nascita()`, quindi dentro la nascita `_deg` e' **STANTIO** |
| la torsione | `_tw_t`, uno ### **SNAPSHOT** preso prima nel passo | ### **`net.tw`** — alla nascita non esiste nessuno snapshot |

### 📌 **E DUE CONTATORI, `_g_pgeom_der_m1` e `_g_pgeom_der_p1`:** dicono ### **quante volte la
derivazione ha davvero DECISO** `-1` e `+1`. Esistono perche' un *«sempre `-1`»*
### **non distingue una derivazione da una costante.**

### ⛔ **E OGGI LA CURA E' BYTE-INERTE SULLE TRE SCENE DEL SIGILLO, ed e' MISURATO:** il
censimento *(`csv/_test_fork/_censimento_perc_geom/`)* ha trovato ### **`1225` nati con eredita'
`-1` E derivazione `-1`** ⇒ zero differenze. ### ⚠ **Ma e' una proprieta' DELLE SCENE, non della
legge:** nella scena da **150** passi fino a ### **`103` nodi** stanno a `+1`, quindi un nato da un
genitore a `+1` e' ### **possibile** — e la' le due regole ### **divergerebbero.**

## ✅ **E DAL `COMMIT 4` IL PUNTO UNICO FA UN'ULTIMA COSA: IL VELENO**

Dopo che ### **tutte le regole hanno scritto**, `nascita()` chiama
### **`_avvelena_derivate(net)`** — e sta ### **qui** perche' ### **qui e' il punto unico
della nascita.**

| | |
|---|---|
| ### **perche' DOPO e non prima** | il veleno estende fino a `len(net.phi)` e `len(net.i)`, cioe' alle lunghezze ### **NUOVE** — e quelle le stabiliscono le regole di `phi` e di `i`. ### **Prima del blocco non esisterebbero ancora** |
| ### **perche' PER EVENTO** | ogni chiamata a `nascita` aggiunge nodi o archi, quindi ### **ogni chiamata avvelena cio' che ha appena allungato** |
| la scheda del veleno | ### **`veleno-derivate`**, qui sopra |

### 📌 **E questo e' il primo pezzo di fisica che il punto unico ha reso POSSIBILE:**
prima della riorganizzazione le scritture della nascita stavano in ### **tre posti**, e
*<<dopo che tutte le regole hanno scritto>>* ### **non era un istante nominabile.**

---

## ⛔ **CORREZIONE DEL 2026-10-03: CINQUE DERIVAZIONI AFFERMAVANO UN BILANCIO NON MISURATO**

> ### **Rilievo del guardiano. Una derivazione di questa tabella SI LEGGE COME UN FATTO** —
> ### e cinque su 72 davano per risolte domande APERTE.

| la regola | diceva | dice ORA, e perche' |
|---|---|---|
| ### **`divisione`/`tw`** | *<<la torsione dell'arco e' stata ### **SCIOLTA** dalla divisione, ed e' cio' che il calcio ha ### **SPESO**>>* | ### **FALSA.** Il calcio ### **USA `|tw|` come MISURA** di quanto colpire e ### **NON trasferisce l'avvolgimento**: `DIVISIONE-AUTOCONSISTENTE:M1` ha misurato ### **~1.2 giri persi per arco diviso, SENZA BILANCIO.** ### **Se debba conservarsi e' APERTA** |
| ### **`perc_chi`**, su ### **ENTRAMBI** gli eventi | *<<e' il ramo che ### **CONSERVA**: la coppia e' NEUTRA e `N(+1)-N(-1)` NON cambia>>* | ### **VERA DELLA COPPIA, FALSA DEL RAMO.** L'antinodo ### **da solo** sposta la carica di `-segno(perc_chi[aa])`; i due rami si cancellano ### **SOLO sugli archi dove scattano ENTRAMBI**, e lo Schwinger scatta su un ### **sottoinsieme** (`pick`) |
| ### **`schwinger`/`conc_nodi`** | *<<la Schwinger ### **DRENA** tensione di una massa esistente>>* | ### **un trasferimento che nessuno ha misurato.** Quella regola ### **copia una lista e le mette una marca**: che la coppia dreni la massa e' una lettura ### **plausibile**, non una misura |
| ### **`divisione`/`d0`** | *<<proporzionale alla torsione ### **sciolta**>>* | la frase e' ### **esatta**, ma ### **il NOME `sciolta` presuppone il bilancio**: e' solo `|tw|/PHI_CRIT`. ### **Il nome non si cambia in un commit di commenti** — in coda |

### 📌 **E IL NUMERO CHE SMONTA LA CONSERVAZIONE ERA GIA' COMMITTATO:** 72 passi, seme 11 — ### **`_g_nati_mitosi = 9` contro `_g_nati_schwinger = 1`**, cioe' `N(+1)-N(-1)` si e' spostato di ### **+8** in quel run *(`csv/_test_fork/_sonda_commit3/_sonda_commit3.json`, `nati_dopo`)*.
### ⛔ **I DUE CONTATORI ESISTONO PROPRIO PER DISTINGUERE LE DUE COSE, e la frase era scritta come se non esistessero.**

### ✅ **E LE FRASI VECCHIE RESTANO CITATE nelle derivazioni: un errore non si cancella, si ANNOTA** *(par.8)*. Trovate col ### **setaccio** *(`csv/_test_fork/_setaccio_derivazioni.py`: ### **9 segnalate su 72**, e il giudizio e' ### **5 da riscrivere, 4 non-fisica** — li' *<<conserva>>* parla del ### **CODICE**)*.

### ⚠ **E NESSUNA DI QUESTE CINQUE RISCRITTURE TOCCA UNA RIGA DI LOGICA:** sono stringhe di documentazione, e che il cambio sia ### **inerte si PROVA** — `csv/_seal_fork/_sigillo_inerzia_commenti.py` confronta gli ### **alberi sintattici** normalizzando solo la documentazione.

> ### **Questa scheda esiste perche' `H-REG-R` ha RIFIUTATO il commit, e aveva ragione:**
> ### **76 nomi nuovi nel simulatore senza una scheda che li nominasse.** Il presidio non
> ### sapeva che sono una RIORGANIZZAZIONE e non una legge nuova — e ### **non deve
> ### saperlo**: deve chiedere che qualcuno lo DICHIARI. Questa e' la dichiarazione.

### 📌 **E IL RIFIUTO HA PRODOTTO UNA COSA UTILE, non solo un adempimento:** il
marcatore qui sopra ### **ELENCA tutte e 72 le regole di nascita, una per una** — e
### **elencarle era IL PUNTO del par.(c)**: *finche' le regole erano sparse in tre posti,
nessuno poteva elencarle, e una legge che non si puo' elencare non si puo' discutere.*
### ✅ **I nomi sono DERIVATI dall'AST**, non battuti a mano *(`L-NUMERI`)*.

## **LA FORMA, e non e' una legge: e' il POSTO dove le leggi di nascita abitano**

```
nascita(net, evento, c)
    per OGNI grandezza in ORDINE_DI_NASCITA (= l'ordine del REGISTRO):
        voce = REGOLE_NASCITA[(evento, grandezza)]
        se non c'e'  ->  RuntimeError: regola di nascita non dichiarata
        se c'e' una regola  ->  la esegue
    e NIENTE ALTRO scrive quelle grandezze.
```

| | |
|---|---|
| **dimensioni** | ### **nessuna**: non c'e' una formula nuova. Ogni regola e'
l'espressione di prima, ### **verbatim** — le dimensioni sono quelle della grandezza
che scrive, e stanno nella sua voce di registro |
| **cosa LEGGE** | `net.<grandezza>` e il ### **CONTESTO** `c`: i genitori, i figli,
`n0`, i valori preparati. ### ⚠ **Non legge `self.n`**, e questo e' un vincolo
MISURATO — vedi sotto |
| **cosa SCRIVE** | ### **le 36 grandezze** di `ORDINE_DI_NASCITA`, e **solo** da qui |
| **limiti** (`A11`) | ### **nessun clip, nessun pavimento, nessun tetto introdotto.**
Le **guardie di lunghezza** che c'erano *(`len(cur) >= n0`, `hasattr`, `is not None`)*
sono ### **SPOSTATE verbatim** nei corpi delle regole: ### **non potate** — una
potatura e' una CURA, e `POTATURA-GUARDIE` resta APERTA |

## ### ⚠ **I QUATTRO VINCOLI D'ORDINE, MISURATI PRIMA DI SCRIVERE IL CODICE**

*(`csv/_test_fork/_ordine_registro.py`; referto in `csv/_test_fork/_ordine_registro/`)*

| | il vincolo | perche' |
|---|---|---|
| **1** | ### **`phi` prima di `twp`** | `twp` legge `phi[a,b]` ### **DOPO il calcio**,
che e' una scrittura **indicizzata** sui genitori, non una pura estensione |
| **2** | ### **`peq` prima di `_peqn_idx`** | lo legge ### **INTERO**. `_peqn_idx` non
sta in nessun registro, quindi e' ### **DICHIARATO** subito dopo `peq` |
| **3** | ### **`n0` nel CONTESTO** | `self.n` e' una ### **`@property`** su
`len(self.phi)`, e i due `_eredita_*` facevano `n0 = self.n - k` ### **A META' della
nascita** |
| **4** | ### **6 chiamate con EFFETTO** | `_smp_chirurgia`, `_traccia_d0`, `_grado`:
### **NON sono regole**, e si collocano a mano con `_nascita_collocata` |

### ✅ **E l'ordine del REGISTRO li rispetta TUTTI: 0 violazioni su 4 vincoli.**

## **IL PRESIDIO, e non e' un avviso**

Una grandezza del registro che non compare nella tabella dell'evento ### **ferma il
run**: *«regola di nascita non dichiarata per `<nome>` all'evento `<evento>`»*.
### ✅ **E il collaudo a secco gira ALL'IMPORT**, quindi ferma il processo ### **prima
che un run cominci** invece di farlo cadere a meta'.
### 📌 **E il silenzio NON e' una terza possibilita':** ogni grandezza ha una
### **REGOLA**, oppure ### **`collocata`** *(la scrive una chiamata con effetto)*,
oppure ### **`non si tocca`** *(l'evento non la scrive, e lo DICE)*.

### ⚠ **E DUE EVENTI SU QUATTRO NON SONO CONVERTITI:** `semina` e `allaccio` vivono
nelle loro funzioni, e ### **`nascita()` si RIFIUTA di girare per loro** invece di far
finta che la tabella li descriva. ### **Una tabella incompleta che tace e' peggio di una
che si ferma.**

> ### 📌 **`PEQ-MEDIANA-ISTANTE` — IL DIAGNOSTICO `_g_peqn_mediana` HA UN ISTANTE DICHIARATO** *(decisione di Luca, 2026-10-02)*
>
> ### **Non e' una legge: e' un DIAGNOSTICO**, e sta qui perche' ### **la sua POSIZIONE era un fatto di fisica mascherato.**
>
> | | |
> |---|---|
> | **che cos'e'** | *«cio' che si EVITA»*: la ### **mediana GLOBALE** di `peq` che `PEQ_NASCITA_LOCALE` esiste per ### **NON usare** |
> | ### **dov'era** | ### **FRA le due scritture di `peq`** — la riscrittura della mitosi *(`concatenate([peq[keep], peq[sel], peq[sel]])`)* e l'estensione dello Schwinger. ### **Una mediana sull'INTERO array, presa fra due riscritture di quell'array** |
> | ### **perche' contava** | ### **era l'UNICO ostacolo genuino al PUNTO UNICO di nascita** *(misurato: `csv/_test_fork/_punto_unico_fattibile.py`)*. Non si poteva spostare ### **ne' prima** *(leggerebbe il `peq` pre-mitosi)* ### **ne' dopo** *(quello post-Schwinger)* |
> | ### **l'ISTANTE, ora** | ### **LO STATO DA CUI LA NASCITA DEL PASSO PARTE.** Il valore si **cattura** in una locale in testa a `mitosi`; ### **l'assegnazione resta dov'era**, sotto le sue tre condizioni ⇒ ### **il GATE non cambia, cambia SOLO il numero** |
> | ### **perche' QUESTO istante** | e' ### **l'unico NON AMBIGUO**: *«dopo la nascita completa»* dipenderebbe da ### **quali rami sono scattati** dentro `mitosi` *(Schwinger si'/no, quanti archi)*, e due passi darebbero mediane prese su stati diversi ### **per ragioni diverse** |
> | ### **il NUMERO cambia, e si dichiara** | prima era la mediana ### **DOPO** la riscrittura della mitosi, ora e' quella ### **PRIMA**, e la differenza e' ### **esattamente l'effetto di quella riscrittura.** ### **NON e' byte-identico, e lo e' DI PROPOSITO su QUELLA SOLA grandezza** |
> | **il COSTO, misurato** | `np.median` su 471564 float: ### **`0.0053 s`**, cioe' lo ### **`0.187 %`** di un passo da `2.849 s`. Il gate della cattura e' **cheap**, quindi si paga ### **solo nei passi in cui una divisione c'e' davvero** |
>
> ### ⚠ **E LA RAGIONE PER CUI IL SIGILLO E' VENUTO PRIMA:** la regola di confronto di ieri *(registro piu' `_`-e-intero)* ### **NON guardava `_g_peqn_mediana`** — comincia con `_` **ma e' un `float`**. ### **Quindi questa cura sarebbe passata IN SILENZIO**, e ### **il difetto non sarebbe stato il cambiamento: sarebbe stato il non vederlo** (`A8`). La regola estesa e' `csv/_confronto_nascita.py`, e il suo sigillo `csv/_seal_fork/_sigillo_confronto_esteso.py`.

> ### 📌 **COMMIT 2 DEL RIORDINO — LA DECISIONE E' USCITA, E NON E' UNA LEGGE NUOVA** *(2026-10-01)*
>
> ### **`decidi_divisione` entra in QUESTA scheda, non in una sua:** e' ### **la stessa legge di
> `mitosi`**, separata da chi la esegue. ### **Byte-identico, zero bit** — soglia e `0.3`
> ### **invariati**, come decide il piano *(la soglia **E'** `D36`, e toccarla cambia la fisica)*.
>
> | | |
> |---|---|
> | ### **che cosa si LEGGE adesso** | `decidi_divisione(net) -> (sel, perche)`: ### **il criterio dall'inizio alla fine**, senza le 274 righe di esecuzione in mezzo |
> | ### **l'interfaccia, MISURATA** | su **25** nomi candidati, l'esecuzione legge della decisione ### **UNO SOLO: `I`** *(la densita' sorgente)*. Verificato dallo strumento di patch, ### **saltando i commenti e gli argomenti omonimi** |
> | ### **e il `perche'` si consegna ANCHE quando non nasce niente** | ### **il caso piu' frequente**: una decisione leggibile deve esserlo ### **soprattutto quando dice NO** |
>
> ### ⛔ **E NON «LEGGE E NON SCRIVE NIENTE», come il piano prometteva: LO DICHIARO QUI**
> Tre scritture restano **dentro**, e ciascuna ha un motivo di **fisica**:
>
> | la scrittura | perche' non puo' uscire |
> |---|---|
> | ### **l'estrazione casuale** | il generatore **avanza**: spostarla cambia ### **l'ORDINE delle estrazioni**, e il run non sarebbe piu' byte-identico |
> | ### **`self._rep`** | e' una grandezza di **STATO** col suo rilassamento esatto: ### **e' la MEMORIA della decisione**, non un effetto dell'esecuzione |
> | **i contatori** | contano ### **cio' che la decisione ha fatto** (`A8`) |
>
> ### ➜ **La promessa onesta e': «NON TOCCA LA FISICA DEI NODI E DEGLI ARCHI».** Non crea, non
> distrugge, non muove `phi`, `d`, `d0`, `pos`, `tw`. ### **Dichiararla pura sarebbe stato FALSO, e
> un sigillo su una promessa falsa non prova niente.**
>
> ### 🧪 **E UN'OSSERVAZIONE NON SPIEGATA, registrata e non inseguita:** sulla scena **piccola**
> ### **26 archi stanno SOPRA la soglia locale e `prob` vale ZERO ESATTO per tutti.** Spiega
> *«zero nascite in 40 passi»* con qualcosa ### **piu' forte di una probabilita' bassa**, e
> ### **va misurato a se'.**

> ### ⚠ **COMMIT 0-bis — DENTRO `mitosi` CI SONO DUE RAMI, E UNO NON GIRA MAI** *(2026-10-01)*
>
> | ramo | che cosa fa | gira? |
> |---|---|---|
> | ### **deterministico** | il calcio ai genitori e' ### **modulato dal TEMPO PROPRIO LOCALE**: `tau = 1+|tw|/PHI_CRIT`, `mod = tau/(1+tau)`, una **parte comune** `KICK_TW·sciolta·(mod−0.5)` e una **parte chirale** `±½·KICK_TW·sciolta·chi·mod` | ### **SI', ED E' L'UNICO SIGILLATO** |
> | ### **stocastico** | **rinculo di fase CASUALE**: `rng.normal(0,1)·KICK_TW·sciolta` | ### **MAI** |
>
> ### ⛔ **E il commento del ramo stocastico diceva *«canonico, validato ... DEFAULT»*: falso su
> tutti e tre i punti.** `REGIME = "deterministico"` ### **dal 2026-08-28** (`670310f`), **nessuno
> strumento** seleziona lo stocastico, e ### **nessun sigillo copre quel ramo.**
>
> ### 📌 **E IL CONFRONTO FRA I DUE RAMI DICE UNA COSA DI FISICA, non di manutenzione**
> ### **Il ramo che gira HA GIA' UN'AUTOINTERAZIONE, e deterministica:** ### **la torsione
> dell'arco decide QUANTO FORTE e' il calcio**, e ### **la chiralita' di ciascun genitore ne
> decide IL VERSO.** L'altro ramo ha un **rinculo casuale**.
> ### ➜ **Quindi alla domanda di Luca *«non dovrebbe esserci una parte di autointerazione?»* la
> risposta e' «C'E' GIA'», non «manca»** — e il lavoro e' ### **renderla autoconsistente**:
> la voce e' **`DIVISIONE-AUTOCONSISTENTE`**, e il suo difetto piu' grave e' che ### **i figli
> ripartono da `tw = 0`, cioe' la torsione SPARISCE senza un bilancio.**

> ### 📌 **COMMIT 0 DEL RIORDINO, 2026-10-01 — `MITOSI_DIR` SI ARCHIVIA, e il commento diceva il
> contrario** *(decisione di Luca; `CENS-A4`)*
>
> | | |
> |---|---|
> | il fatto | `MITOSI_DIR = 0.0`, quindi ### **il ramo a `:6975`-`:6981` NON GIRA MAI** — e il commento diceva ### **«MITOSI DIREZIONALE ATTIVA»**. ### **Sono DUE difetti e non uno:** un ramo **morto**, **e** un commento che dice **il contrario** |
> | ### **che cosa cambia questo commit** | ### **SOLO IL COMMENTO.** Il valore non si tocca, il ramo resta dov'e'. ### ✅ **E la byte-inerzia e' PROVATA DALLA STRUTTURA, non da un run: l'AST del file e' IDENTICO** *(1 525 008 caratteri di dump, uguali)* — ### **quindi cambiano per costruzione solo i commenti** |
> | ### ✅ **l'IDEA non si butta** | *«il figlio nasce decentrato verso il gradiente di torsione»* ### **E' `t = f(stato_a, stato_b)`** con la torsione come grandezza: e' il ### **PRIMO TENTATIVO** della voce **`FRAZIONE-DIVISIONE`**, e il commento ora lo **cita** |
> | ### ⛔ **la FORMA si archivia** | `bias = 0.5 * np.tanh(MITOSI_DIR * (twn[a] - twn[b]))` *(`:6981`)* = ### **TRE numeri a mano** — il coefficiente, la `tanh`, e lo `0.5`. ### **`A1`: la legge, non il numero** |
>
> ### ⚠ **Perche' il ramo NON esce in questo commit:** il par.3 dice **un interruttore alla volta**,
> e ### **togliere il ramo e' una modifica dell'AST**, cioe' una cosa **diversa** dal correggere una
> frase falsa. ### **L'archiviazione del ramo e' una voce a se'** *(il `(7)` del piano)*, e
> `RAMI-OFF-CURA2` dice **come**: ### **archiviato COPIATO dal sorgente, non cancellato.**

> ### 🆕 **NOTA DEL 2026-09-28 (`PSI-FLASH`): la mitosi ora ESTENDE `psi` e `psi_spin` ai nati.**
> **La legge della mitosi non cambia**: cambia che ### **i nati ricevono un `psi` invece di lasciare
> `len(psi) < n`**, che spegneva la schermatura per tutta la rete. `psi` prende la **media dei
> genitori** *(il compagno di `phi`, che alla nascita prende `fm`)*, `psi_spin` **eredita da `a`**
> *(il compagno di `phi_s`)*. **Ai DUE canali**: mitosi (`a`,`b`) e Schwinger (`aa`,`bb`).
> *(La legge della schermatura sta nella scheda `schermatura-nucleo-nudo`.)*

> **-> NOTA DEL 2026-09-28 (`MAX-NODI-FERMA`): LA LEGGE DELLA MITOSI NON E' CAMBIATA -- LE E'
> STATA TOLTA UNA COSA CHE NON ERA SUA.** Due rami leggevano `MAX_NODI`:
> `if self.n >= MAX_NODI or not len(self.tw): return 0` (### **zero nascite in silenzio**) e
> `if COPPIA_MIT > 0.0 and self.n < MAX_NODI` (### **canale di Schwinger spento in
> silenzio**). ### **Una guardia di MEMORIA diventava una LEGGE.** Ora la mitosi non legge
> piu' `MAX_NODI`: ferma lo **schedulatore**. **`not len(self.tw)` RESTA**, perche' quella e'
> una rete senza archi -- *non c'e' niente da dividere* -- e non ha nulla a che vedere con
> la memoria. *(La legge della guardia sta nella scheda `guardia-max-nodi`.)*

> **→ NOTA DEL 2026-09-25: la LEGGE DELLA MITOSI NON E' CAMBIATA.** Il commit di
> `INERZIA-1(C)` tocca **la riga accanto** alla `global MITOSI_2LAM` in `_applica_flag`, per
> dichiarare `global CONTRASTO_INTENSIVO` — **niente di piu'**. `MITOSI_2LAM` e la soglia
> `d >= 2 LAM` restano **identici**.
> *(Questa nota esiste perche' `REG-R` ha rifiutato il commit chiedendo la scheda di
> `MITOSI_2LAM`, e **ha fatto bene a chiederla**: dal diff non si vede se la riga toccata sia
> un commento o una legge. **La risposta va scritta, non assunta.**)*
# ⑦ LA MITOSI E SCHWINGER — **`mitosi()`**

> ### 🏗 **T1: la mitosi non apre piu' il passo**
> **`T1`, 2026-09-28: l'apertura del passo NON sta piu' qui.** La fa lo **SCHEDULATORE**
> (`esegui_passo`), in testa alla composizione, e **l'idempotenza di `(c)1` non serve piu'** --
> il compositore **sa** di essere il primo. **Misurato:** `_g_smp_gia_aperta` passa da **4 per
> passo** a ### **0**. *(Scheda `schedulatore-del-passo`; tag `pre-schedulatore-t1`.)*
>
> **Le regole di nascita non sono toccate**, e `_smp_chirurgia` continua a far seguire la
> fotografia alla ristrutturazione: ### **e ora la fotografia e' garantita aperta dallo
> schedulatore**, invece di dipendere dal fatto che una delle cinque leggi ci si fosse ricordata.
> ⚠ **E la mitosi resta l'unica legge `AMBIGUA`** *(scrive STRUTTURA e STATO: 30 scritture di
> stato)*. **Si spezza in `T2`**, mentre tutto il resto e' ancora byte-identico -- correzione (b)
> del piano, approvata da Luca.


> ### 🔓 **(c)1, 2026-09-27: anche la mitosi APRE il passo**
 > **`(c)1` di `ETC-PASSO`, 2026-09-27: `_smp_apri()` e' IDEMPOTENTE e la chiamano TUTTE
> e CINQUE le leggi**, in testa. **La prima che gira apre**, le altre quattro escono subito, e
> cosi' il confine della transazione e' a **inizio passo pieno qualunque sia l'ORDINE** -- che e'
> cio' che `H-ETC-2` permuta. **I chiamanti delle cinque leggi sono SEI**, e una divergenza fra
> due di loro sarebbe invisibile: l'idempotenza mette il confine **dentro** la cosa che deve
> rispettarlo. Contatore `A8`: **`_g_smp_gia_aperta`** = quante leggi l'hanno trovata gia' aperta
> *(4 per passo con le cinque canoniche)*.
>
> **Le regole di nascita non sono toccate.** Cambia solo **chi puo' aprire la transazione**, e
> per la mitosi conta doppio: e' **lei** che chiama `_smp_chirurgia`, cioe' che fa subire alla
> fotografia le stesse operazioni di `d0`. **Una fotografia non aperta non potrebbe seguirla.**


> ### 🗄 **(b)1, 2026-09-27: via la chiamata al pavimento vecchio dopo la spinta**
>
> `mitosi` faceva `self.d0 = self._pav_d0(self.d0)` subito dopo la spinta locale, col commento
> *<<PAVIMENTO: la spinta non deve>>*. **Col driver era un no-op** e ora non c'e' piu'.
> ### **E le REGOLE DI NASCITA non sono toccate:** `_nasce` resta, e con lui la garanzia che un
> troncone sotto `LAM` **parta da `LAM`** -- che e' il vincolo vero, ed e' `MITOSI_2LAM` +
> `SEMINA_LAM`. **Quello che esce e' il pavimento VECCHIO su `d0`, non la scala minima.**
> *(Misurato: `min(d) = LAM` esatto in 16/16 stati del pilota, 0 archi sotto `LAM`.)*


> **→ NOTA DEL 2026-09-27 (seconda): DENTRO `mitosi()` SONO USCITI QUATTRO RAMI `else`.**
> La `CURA 2` e' **strutturale** *(scheda ⑨, decisione di Luca)*: i quattro `if
> TEMPO_UNICO_MITOSI:` **non ci sono piu'** e il corpo del ramo **acceso** resta, de-indentato.
> **LA LEGGE DELLA MITOSI NON CAMBIA:** e' quella che girava gia' in ogni run, perche' il
> driver accendeva il flag **sempre**. **Cio' che cambia e' che non si puo' piu' spegnere.**
> **Il taglio e' stato fatto per AST**, non a stringhe, perche' togliere un `if` vuol dire
> **de-indentare il suo corpo di 4** su quattro blocchi da 2 a 19 righe, e il controllo e'
> che **il corpo sia lo stesso testo de-indentato e nient'altro**.
> **I rami tolti:** `csv/_archivio/rami_off_cura2.py`, tag **`pre-cura2-strutturale`**.
>
> **→ NOTA DEL 2026-09-27: LA LEGGE DELLA MITOSI NON E' CAMBIATA, SONO CAMBIATI I NOMI.**
> La chiusura di **`D32`** rinomina, **dentro `mitosi()`**, `tau_pp` → **`pos_torsione`**,
> `tau_soglia`/`tau_tetto` → **`pos_soglia`/`pos_tetto`**, `tau_nodo` → **`tors_nodo`**,
> `grad_tau` → **`grad_modula`**, e corregge i **sette commenti** che chiamavano `tau_pp`
> *«tempo proprio»*. **Nessuna formula cambia**, e un sigillo byte-identico lo prova
> *(`csv/_seal_fork/_sigillo_d32_nomi.py`)*.
> **⚠ E UNA RINOMINA CHIESTA NON SI POTEVA FARE COM'ERA:** `grad_tau → grad_torsione`
> **mentirebbe sul ramo che gira**. Con `TEMPO_UNICO_MITOSI` **acceso** quel gradiente e'
> **`|r_nodo[i] − r_nodo[j]|`: il gradiente di `r`, il tempo proprio VERO**; e' della
> **torsione solo a flag spento**. Il nome al punto d'uso dice quindi il **RUOLO**
> *(`grad_modula`: modula la soglia)*, e **ogni ramo dichiara il suo contenuto**.
> *(Questa nota esiste perche' `H-REG-R` ha rifiutato il commit chiedendo la scheda di
> `mitosi`, e **ha fatto bene**: dal diff non si vede se una riga toccata sia un nome o una
> legge. **La risposta va scritta, non assunta.**)*

> **STATO: `DIFETTOSA`.** Difetti **`D35`** *(l'antifase della coppia)* e **`D33`** *(la
> repulsione che si spegne al tetto)*. Piu' **`D03`** per la parte di `_rep`.
>
> ### ➜ **`CURA 2` MODIFICA `mitosi()`, e la legge sta in scheda ⑨** *(2026-09-24)*
>
> Quattro rami gated su **`TEMPO_UNICO_MITOSI`** *(spento di default)*: `grad_tau`, il fattore
> di tempo di `ampiezza`, la forma di `prob`, il bersaglio e il rilassamento di `_rep`.
> **I quattro usi di `tau_pp` come POSIZIONE sull'asse della torsione** — `tau_soglia`,
> `tau_tetto`, `centro`, `segno`, cioè **la forma riportata qui sotto** — **NON sono toccati**,
> e il sigillo lo verifica **dall'AST** *(`T3`)*, non a parola.
>
> **➜ E `mitosi()` HA UN CONTATORE IN PIÙ, incondizionato** *(2026-09-24, `_tum_clip0_prob`)*:
> `np.clip(resp, 0, 1)` taglia **in alto E IN BASSO**, e finora contavo **solo il lato alto**.
> **Il lato basso morde su tutto il regime repulsivo** — cioè sulla metà di questa scheda che
> riguarda `_rep`. **Byte-inerte per costruzione, non misurata.**
>
> **⚠ E IL CLIP SU `rep` HA LO STESSO DOPPIO LATO E IL CONTATORE DEL LATO BASSO NON C'È ANCORA.**
>
> **⚠ E `D33` È DENTRO IL PERIMETRO DELLA CURA:** *«la repulsione che si spegne al tetto»* vive
> su `_rep`, che `CURA 2` cambia in **due** punti — il bersaglio *(ora senza il fattore di
> tempo)* e l'integratore *(ora esatto invece che Eulero)*. **La cura NON dichiara di curare
> `D33`**, e il criterio `R` misura proprio **quanto `d0` si allarga**: la previsione di Luca è
> **×2.5-×3** sul bersaglio. **Se `D33` si muovesse, sarebbe un effetto collaterale da
> RIPORTARE, non un merito da rivendicare.**

## LA FORMA — copiata dal codice

> ### ⛔ **LA MODULAZIONE DELLA SOGLIA E' USCITA il 2026-10-06, su decisione di Luca.**
> La legge era `soglia = soglia0 · (1 − 0.3·tanh|r_i − r_j|)`; ora e'
> ### **`soglia = soglia0` su OGNI arco.**
>
> ### **IL PERCHE', MISURATO** *(referto `27c10bd`, `1000` passi, due bracci)*:
>
> | | |
> |---|--:|
> | `R` sulle divisioni | `0.1616` |
> | `R` sulla popolazione nella finestra | `0.3417` |
> | nascite per `100` passi ### **senza** | `48`-`150`, ### **stabili** |
> | nascite per `100` passi ### **con** | fino a ### **`1044`**, ### **in accelerazione** |
>
> ### ✔ **La crescita NON era creata dalla modulazione** *(`R` non e' zero)*, e
> ### **senza di lei CAMBIA FORMA: da accelerante a stabile.** ### **La si sceglie senza.**
>
> ### ⚠ **E LA SOGLIA `3π` NON E' TOCCATA:** `soglia0 = PHI_CRIT + twist_max`
> resta. ### **Il `π` di dipolo che in questa scena non esiste e' una DECISIONE
> SEPARATA di Luca**, e il principio scelto e' *«solo valori ricavati»*:
> ### **`2π + |twist_dip dell'arco|`**, da decidere ### **dopo la cura di
> `GEOM-SENZA-VERSO`**, su una misura a tre bracci.
>
> **Il ramo che esce e' archiviato** in `csv/_archivio/_rami_off_mitosi_soglia_grad.py`, e
> si rilancia dal tag ### **`pre-mitosi-soglia-grad-via`**.

```
soglia0 = PHI_CRIT + twist_max = 2pi + pi = 3pi          (TORS_4PI acceso)
soglia  = soglia0                                        su OGNI arco
          # [VIA IL 0.3, 2026-10-06] prima era:
          #   soglia = soglia0 * (1 - 0.3*tanh(grad_modula))   modulazione LOCALE
ecc     = max(|tw|/soglia - 1, 0)
salita  = satura(ecc)                                     zero sotto soglia
discesa = clip(1 - |tw|/TW_TETTO, 0, 1)                   ZERO da 4pi
tau_pp  = 1 + |tw|/PHI_CRIT                               <- il "tempo proprio surrogato"
centro  = 0.5*(tau_soglia + tau_tetto)
segno   = -tanh(3.0*(tau_pp - centro))                    + crea, - respinge
resp    = salita * discesa * (1/tau_pp) * segno
prob    = clip(resp, 0, 1)        ->  nasce = rng < prob             (CREAZIONE)
rep     = clip(-resp, 0, 1)       ->  _rep rilassa con tau_pp        (REPULSIONE)
```
**LA COPPIA (Schwinger):** `prob_coppia = 1 - exp(-COPPIA_MIT * eccesso)`, e il partner nasce
con **`anti = (fm + 2π) % 4π`** *(`:5443`)* **e lo spinore di segno opposto** *(`:5477`)*.

## ⚠ I DUE DIFETTI, MISURATI

**`D35` — l'antifase non è un'antifase.** Il campo è `F = Σ K·exp(iφ)`, e
`exp(i(φ + 2π)) = exp(iφ)`: **nel campo l'antiparticella è IDENTICA alla particella.**
**Il commento dice `+π`, il codice fa `+2π`: fa fede il codice.**
**E il ramo È ATTIVO:** `COPPIA_MIT = 1.0`, e `S07_schwinger` scatta **`102` · `90` · `172`**
volte su 600 passi nei tre bracci *(`Z119`)*.

**`D33` — la repulsione si spegne dove servirebbe.** Il `segno` si inverte oltre `~3.5π`, **ma
`discesa` è ZERO ESATTO da `4π`**: la finestra utile è larga **mezzo `π`**, e **dal `75 %`
al `96 %` degli archi oltre l'inversione riceve repulsione esattamente zero** *(`Z111`)*.

## I LIMITI, CLASSIFICATI

| limite | classe | `A11` |
|---|:--:|---|
| `soglia0 = 3π` | **`L`** | ⚠ **derivazione A POSTERIORI**: `2π + π` è stato giustificato dopo, e **cade con `FASE_2PI`** *(`§D` punto 2)*. **È il punto più incerto, e lo decide `E1`** |
| `0.3 * tanh(grad_tau)` | **`L`** | ❌ il `0.3` è **scelto** *(`A1`)* → `SCALE-TW` |
| `clip(1 - \|tw\|/4π, 0, 1)` | **`L`** | ❌ **`D33`**: azzera il ramo repulsivo oltre `4π`. **Due leggi in un prodotto solo** |
| `tanh(3.0 * …)` | **`L`** | ❌ il `3.0` è **scelto** → `SCALE-TW` |
| `0.02 * d0 * _rep` | **`L`** | ❌ il `0.02` è **scelto**, già dichiarato in `D03` |
| la nascita di un nodo | **`E`** | ✅ **evento discreto con TASSO liscio** — la campana **è** già liscia; **ma `salita` ha un `max(…, 0)` e `discesa` un `clip`: due spigoli DENTRO il tasso**, da verificare |

## COSA CAMBIA CON `FASE_2PI` — ✅ **IN CODICE** *(blob `445e2896`)*, spenta di default

- **`anti = (fm + π) % 2π`** — cura `D35`;
- **`soglia0 = 2π`** — *«un arco porta una differenza fino a `π`; quando porta un quanto
  intero (`2π`) si divide, e ciascuna metà ne porta `π`»* *(Luca)*;
- **e il punto di inversione SI SPOSTA come conseguenza:** `tau_soglia` passa da `2.5` a `2`,
  quindi `centro` da `2.75` a **`2.5`**, cioè **l'inversione da `3.5π` a `3π`**. **La finestra
  di `D33` si allarga da mezzo `π` a un `π` intero** — **non è una cura di `D33`, è un
  effetto, e va misurato.**

## LE DOMANDE APERTE

1. **`E1`: la mitosi a `2π` funziona senza tarature?** Né zero mitosi né esplosione. **Se
   fallisce, cade il punto 2 del `§D`**, e con esso la soglia a `2π`.
2. **`E2`: le coppie annichilano?** Oggi la frazione è `~0`. **Se resta `~0` con `+π`, cade il
   punto 5**, e `S06` *(il «muro dell'1 %»)* **non** ha la spiegazione che sembra avere.
3. **L'argomento della soglia vale per una differenza ISTANTANEA, ma `tw` è un ACCUMULO che
   decade.** **È la crepa dichiarata da Luca stesso**, e `E1` è il suo giudice.

## I CRITERI DEI TEST, **fissati PRIMA di girare** *(par.5-septies)*

> **⚠ CHI HA SCRITTO QUALE TEST, e va detto perché due sono MIEI — è `Z125`.**
> Nel repo esistevano **solo `E1` ed `E2`**, e ho citato *«i quattro test `E1`-`E4`»* **undici
> volte** senza che `E3` ed `E4` fossero scritti da nessuna parte. **`E1` ed `E2` sono di Luca
> e non si toccano; `E3` ed `E4` li DERIVO, e Luca può sostituirli.**
> Lo strumento è **`csv/_test_fork/_f2p_test_E.py`**, e i criteri stanno **nel suo codice**,
> non solo qui *(`P1-ter`)*.

| test | di chi | criterio | **origine della soglia** |
|---|:--:|---|---|
| **`E1a`** la mitosi non muore | **Luca** | `_g_nati_mitosi > 0` e `n` cresce | il nullo: se la cura rompesse `fm`, le nascite sarebbero `0` |
| **`E1b`** la mitosi non esplode | **Luca** | `n` finale **< 10×** il riferimento, e il run **arriva** a 600 passi | **MISURATA: `178` archi per nodo** *(`526672 / 2959`)*. `10× n` = `~5.3M` archi = `10×` memoria e tempo: **oltre, il sistema non è simulabile, e QUELLA è l'esplosione**. **`MAX_NODI = 4000000` non serve: è una guardia di memoria, non di fisica** |
| **`E1c`** il **fattore** | *mio* | le nascite salgono di un fattore **fra `5×` e `100×`** | **DERIVATA dagli archi GIÀ SUL DISCO**: la campana ha il picco a `|tw| = soglia`, e la finestra **nuova** *(`tau` `2.0`-`2.5`)* contiene **`17113`** archi contro i **`346`** della vecchia *(`tau` `2.5`-`3.0`)* al passo 600 — **`49.46×`**. La banda è **un ordine per lato** perché la **larghezza** della campana non entra nel conto e **la mitosi CONSUMA la torsione** *(retroazione che smorza)*. **Questo test giudica ME, non la cura** |
| **`E2`** le coppie annichilano | **Luca** | **NON MISURABILE**, e si dichiara | vedi il blocco qui sotto |
| **`E3`** la finestra di `D33` | *mio* | si riporta la **popolazione** delle due finestre nei due bracci | il §E **stesso** dice *«non è una cura di `D33`, è un effetto, e va misurato»*. **Si RIPORTA, non si giudica** |
| **`E4`** i diagnostici di fase | *mio* | `max(φ) < 2π` nel braccio della cura | la **riserva ② di `Z120`**. **Il nullo è il sigillo:** a flag spento `max(φ) = 12.565546` |

### ❌ **`E2` NON È MISURABILE IN QUESTO RUN, e lo dichiaro invece di riportare uno zero**

**L'ANNICHILAZIONE VIVE SOLO DENTRO `ANTIFASE_ADD` (`:5351`), CHE È `False`.**
Il ramo che la cura tocca — **`:5499`** — è la **creazione di coppia alla Schwinger**, e lì
l'antifase decide se l'antiparticella è **DISTINGUIBILE** dalla particella nel campo: che è la
**precondizione** dell'annichilazione, **non l'annichilazione**.

**Riportare uno zero sarebbe leggere un'ASSENZA DI MECCANISMO come un'assenza di effetto** —
lo stesso errore del `max|A-B| = 0.000e+00` per **mancanza di confronto**.

**COSA SI MISURA AL SUO POSTO**, e il valore atteso **non è scelto**, è `|exp(i s) − 1|`:

| | `max|exp(i·anti) − exp(i·part)|` |
|---|--:|
| **spenta** — `+2π` su dominio `4π` | **`2.156e-15`** → **identica**: è `D35` |
| **accesa** — `+π` su dominio `2π` | **`2.000000`** → **opposta** |

> ### ⚠ **E LA CONSEGUENZA PER `S06` È PIÙ FORTE DELLA DOMANDA DI PARTENZA**
> Il «muro dell'1 %» **non si spiega con `D35` da solo**: il meccanismo che annichilerebbe
> **non gira**. **`S06` non si chiude con questa cura**, e per misurarlo servirebbe accendere
> `ANTIFASE_ADD` — che è un **ESPERIMENTO** *(par.10)*, **non fisica**, e va **chiesto a Luca**
> invece che deciso qui.

### ✅ **IL CONTROLLO DELL'INVOLUCRO È STATO FATTO PRIMA** *(`STANDARD ⑤`)*

Lo strumento puntato sul **riferimento CONTRO SE STESSO** dà **`2/4`**: `E1a` e `E1b`
**passano**, **`E1c` e `E4` NON passano** — perché il braccio della «cura» *è* il riferimento.
**I criteri non sono vuoti.** → `csv/_test_fork/_f2p_CONTROLLO_involucro.txt`

**E il controllo ha trovato un difetto prima del run:** `n` **non è una chiave** dello snapshot
*(si legge da `len(phi)`)*, e lo strumento si schiantava con `KeyError: 'n'`. **Su un run vero
lo schianto sarebbe arrivato dopo quaranta minuti.**

---


### ❗ LA MITOSI CHIAMA `_nasce` DUE VOLTE, E LE DUE CHIAMATE NON HANNO LA STESSA MOLTEPLICITÀ *(2026-09-25)*

**Fatto di questa scheda, e ci si sbaglia facile** *(mi ci sono sbagliato io)*:

```python
dh    = self._nasce(dh,    'mitosi', 2, 0)   # `len(sel)` voci -> concat([d[keep], dh, dh])
d0new = self._nasce(d0new, 'mitosi', 0, 1)   # d0new e' GIA' concat([d0h, d0h])
```

> **`dh` ha una voce per arco che si divide, ma diventa DUE archi di `d`.**
> **`d0new` ha già le due voci dei figli.**
> **Chi conta le voci invece degli archi sbaglia di `2` sul primo e di niente sul secondo** —
> cioè in modo **asimmetrico fra le due grandezze**, che è il difetto peggiore da leggere.

**E IL RAMO SCHWINGER È UN TERZO CASO:** `dd` finisce in `concat([d, dd, dd])` **e** in
`concat([d0, dd, dd])`, quindi è `×2` su **entrambe** le grandezze — e **la sua lunghezza viene
da `pos`, non da `d`** *(voce `A3` della coda)*.

**La legge dei contatori sta nella scheda `freno-scala-min`, con `_nasce`.**


### ➕➕ `CURA 5` — **`A13` ALLA NASCITA: un arco si divide SOLO se `d >= 2 LAM`** *(Luca, 2026-09-25)*

**Flag `MITOSI_2LAM`, `--mitosi-2lam`, OFF di default.** La condizione sta **nella maschera `ok`**
di `mitosi`, accanto alla soglia di densità: **lo stesso punto dove il codice decide se un
candidato si divide.**

> ### **NON È UNA LEGGE NUOVA, ed è `STANDARD 10` applicato:**
> ```
> PRIMA   la mitosi divide senza guardare `d`;  `_nasce` INTERVIENE e FABBRICA lunghezza
> DOPO    la mitosi guarda `d >= 2 LAM`;        `_nasce` non ha piu' niente da fare li'
> ```
> **Le leggi non aumentano: si TOGLIE l'eccezione per cui la mitosi era il solo sito capace di
> creare una distanza sotto la scala di Planck, con un presidio che la riparava dopo.**

**PERCHÉ `2 LAM` E NON UN ALTRO NUMERO:** il figlio nasce a **`d/2`** dai genitori, e **la distanza
del sistema è quella LUNGO GLI ARCHI**, non su `pos` *(correzione di Luca)*. Quindi `A13`
— *«sotto `LAM` non esiste una distanza»* — alla nascita **È** `d/2 >= LAM`. **Nessun numero nuovo.**

**MISURATO PRIMA DELLA CURA** *(`7086031`, `279` eventi, `2` semi, `300` passi)*: il **`77.23 %`**
delle divisioni è **già conforme**. E la mitosi **non divide a caso**: `0.2277` contro `0.2998` di
archi corti nel grafo.

**⚠ LO SCHWINGER NON È TOCCATO** *(decisione di Luca)*: la `d` dei suoi archi nuovi viene da
`0.5·|pos[aa] − pos[bb]|`, cioè **dal DISEGNO** — **la voce `A3`**. Toccarlo qui vorrebbe dire
curare `A3` di nascosto.

**I CRITERI** *(task history `832653e`, **antenato** del commit del codice)*: `C1` byte-identità ·
`C2` `_sm_trd_mitosi == 0` **e** `_sm_lund_mitosi == 0` · `C3` eventi `~77 %` entro lo spread ·
`C4` nessun figlio con `d/2 < LAM` · `C5` il figlio è a `>= LAM` da **tutti** lungo gli archi ·
`C6` Schwinger invariato · `C7` controllo positivo · `C8` **caso che deve fallire**.

**⛔ IL RISCHIO DICHIARATO PRIMA:** il grafo **si contrae** *(`med d0` `−36 %`)*, quindi gli archi
scendono sotto `2 LAM` e **la condizione diventa via via più difficile**. **Il `77 %` è misurato su
`300` passi; a `1000` potrebbe essere molto più basso** — cioè **la cura potrebbe SPEGNERE la
mitosi col tempo invece di regolarla.** `C3` guarda questo, e `300` passi **non lo escludono.**

<!-- SCHEDA nome=inerzia-spinoriale funzioni=_passo_spinoriale,_rho_sorgente,_applica_flag,_cli flag=CONTRASTO_INTENSIVO,CAMPO_SPINORIALE,TAU_A -->

> ### ⛔ **NOTA DEL 2026-09-28 (`PSI-FLASH`): `_rho_sorgente` NON RIPIEGA PIU' IN SILENZIO.**
> Quando `rho_spin` era piu' corta di `n` restituiva **`abs(psi)^2`** invece di `rho_spin`: con
> `CAMPO_SPINORIALE` acceso la densita' sorgente **E'** `rho_spin`, quindi quello non era un
> ripiego, era ### **UN'ALTRA GRANDEZZA data a TUTTA LA RETE**. **MISURATO: 2 volte su 15 al
> passo DOPO la nascita** *(len 12802, n 12803)*, ed era **il gradino del +11 % sul pozzo**.
> **Ora solleva `CacheCorta`**, e la cache va **estesa alla nascita** (`_eredita_psi_figli`), non
> allungata dove la si legge. *(La legge sta nella scheda `schermatura-nucleo-nudo`.)*
# Ⓐ `inerzia-spinoriale` — **QUANTO COSTA GIRARE A UNO SPINORE**

> ### 🗄 **(b)2, 2026-09-27: il settore spinoriale ha UN SOLO percorso**
>
> **`SYNC_UPDATE` e' un NO-OP ACCETTATO dal 2026-09-27** *(passo `(b)2` di `ETC-PASSO`)*: i
> suoi rami sono in **`csv/_archivio/_sync_update.py`**, tag **`pre-archivio-sync`**, e `--sync`
> si accetta senza fare niente. **Il suo raggio era UNA legge su cinque** -- `7` usi in
> `_passo_spinoriale`, `6` in `step`, **ZERO** nelle altre quattro -- e **tutte e 56 le letture
> miste `t`/`t+1` misurate nella FASE 0 stavano FUORI da quel raggio.**
>
> **Che cosa e' uscito da `_passo_spinoriale`:** le copie `nb_t` / `nb_prec_t` / `omega_t`
> della <<snapshot immutabile dello stato t>>, e i **due** rami `SYNC_UPDATE and SCUOTIMENTO`
> del rumore sul primario complesso e sul Bloch ruotato.
> **E UNO SCUOTIMENTO CHE ORA AGISCE SEMPRE:** `if SCUOTIMENTO and not SYNC_UPDATE` diventa
> `if SCUOTIMENTO`. **Non e' una legge nuova: e' la stessa legge senza l'eccezione**, e il suo
> commento diceva gia' che le due forme <<devono essere identiche -- il vuoto e' lo stesso
> vuoto>>.
> **`omega_src` e `nb` leggono ora `self.omega_s` e `self._nb` e basta:** la forma della legge
> non cambia, sparisce la scelta fra due sorgenti.
> **`9-ter`: il numero delle leggi SCENDE.** Sette blocchi condizionali in meno, zero aggiunti.


> **QUESTA SCHEDA NASCE IL 2026-09-25, E IL FATTO CHE NON CI FOSSE E' PARTE DEL DIFETTO.**
> La legge che divide la coppia — **`omega = coppia/inerzia`** — governa il settore di spin da
> sempre, ed era descritta **solo nei commenti del codice e nei registri dei difetti**. Il
> registro dice *«questo era rotto»*; **la scheda dice «questa e' la legge»**, e le due cose
> non si sostituiscono (par.5-novies ③).

## LA FORMA

```
inerzia    = max(_contrasto * _T2, 1e-6)
_contrasto = rho_c / peq_nodo          rho_c = rho_s / max(_cn, 1)  se CONTRASTO_INTENSIVO
                                       rho_c = rho_s                altrimenti
_T2        = (d_nodo / cs_nodo)^2
_peq_nodo  = _sp / max(_cn, 1)         (somma dei `peq` d'arco / numero di archi VALIDI)
omega_new  = omega_src + dt_n * (correzione/inerzia - omega_src/_tau)
```

**`_cn` conta gli archi VALIDI** (`peq` finito e positivo), **non tutti**: e' il medesimo
insieme su cui `_peq_nodo` fa la media. **Un conteggio diverso sarebbe l'errore di POPOLAZIONE
di `A3`** — numeratore e denominatore su insiemi diversi.

## DIMENSIONI

`_T2` e' un **tempo al quadrato** (`[T²]`). `_contrasto` e' **adimensionale** *(una densita'
diviso una densita')*, e con la cura resta adimensionale: `rho_s/vicini` diviso
`peq_somma/vicini` — **i due `vicini` si semplificano nel rapporto**, ed e' proprio questo che
rende la cura una **rimozione di incoerenza** e non un fattore di scala nuovo.
`omega = coppia/inerzia` ha quindi le dimensioni di `[coppia]/[T²]`.

## ✅ LA CURA DEL 2026-09-25 — `INERZIA-1(C)`, **LOCALE** (decisione di Luca)

> ### ⚠ **DUE VARIANTI PROVATE, E UNA TERZA IPOTESI CHE POTREBBE RITIRARLE ENTRAMBE**
> **VARIANTE 1 — per CONTEGGIO dei vicini** (`rho_s / max(_cn, 1)`). **Sigillo `3/6`.**
> Toglieva **esattamente `-1.0000`** di pendenza in **4 bracci su 4** *(`1.5200 -> 0.5199`,
> `2.3389 -> 1.3387`, `1.4858 -> 0.4865`, `2.3642 -> 1.3641`)* — **una** potenza di `k`, cioe'
> quello che il conteggio puo' togliere. **Residuo `+0.49` (via i lunghi), `+1.34` (via i
> corti).** `C3` PASS *(LOCALE: 121 campi, 0 diversi)*, `C5` PASS *(pavimento non morde, min
> `0.0655`)*, `C6` scala `x0.0149 ~ 1/77`. **Non e' nel codice: resta come TENTATIVO MISURATO.**
>
> **VARIANTE 2 — per SOMMA DEI PESI** (`rho_s / Σ w_ij`), decisione di Luca: `w` e' **gia'** un
> parametro di `_passo_spinoriale`, lo **stesso** che `calcola_psi` passa a `_mat(w)`.
> **⚠ VARIANTE 2 MISURATA E INSUFFICIENTE:** dimezzava il divario di pendenza (`1.25 -> 0.62`,
> `2.78 -> 1.44`) **senza chiuderlo**, perche' toglieva **una sola** potenza.
>
> ## ✅ **LA FORMA IN VIGORE — CURA A, `rho_s / W^2`** *(decisione di Luca, 2026-09-26)*
> **`_rho_c = rho_s / W^2`**, con `W = Σ w_ij` per nodo, **dentro `_contrasto` e SOLO li'**.
>
> ### PERCHE' L'ESPONENTE E' `2`, E NON E' UNA SCELTA
> **MISURATO sui figli della mitosi** *(2 semi, `K1` PASS su **4300** campioni, collaudo `4/4`)*:
> ```
> rho ~ ramp^2.74      W ~ ramp^1.37      ->   rho ~ W^(2.74/1.37) = W^2.00     (R2 0.95-0.96)
> ```
> **`2.00` esatto.** `rho_s` e' il **modulo quadro** di una somma pesata, e il dato lo dice
> **senza passare dalla lettura del codice**.
>
> ### E LA SCOMPOSIZIONE DEL DIVARIO DEI FIGLI LO CONFERMA DALL'ALTRO LATO
> `log(c_f/c_m) = T1 + T2 + T3`, con `T2 = 2 log(W_f/W_m)`:
> ```
>            %T2 (il termine W^2)   %T3 (peq EREDITATO)   %T1 (resto)
> eta' 2        107.2 - 107.8            -3.3 / -2.8         -4.5 / -4.4
> eta' 14       114.0 - 114.4            -6.0 / -6.4         -8.0 / -8.0
> ```
> **Il divario dei figli e' TUTTO nel peso di vicinato, al quadrato.** Il `peq` **ereditato** va
> nella direzione **OPPOSTA** *(`T3 < 0`: il `peq` del figlio e' **piu' piccolo** di quello dei
> maturi, rapporto `~0.68`)*, quindi **NON e' la causa** — e questo **ritira** la lettura
> precedente, che l'attribuiva a `peq`.
>
> ### ⚠ COSA QUESTA CURA **NON** CHIUDE
> ~~L'asimmetria e' `0` contro `2.8`, e `W^2` ne toglie `2`: resta `0.8`.~~
> **❌ ERRORE DI UNITA' MIO, corretto il 2026-09-26** *(rilievo di Luca; la versione vecchia resta
> leggibile sopra)*: **2 potenze di `W` non sono 2 potenze di `ramp`.**
> **IL CONTO GIUSTO:** `W ~ ramp^1.37` -> `W^2 ~ ramp^2.74`, e `inerzia/W^2 ~ ramp^0.06`; la
> coppia va come `ramp^0.10`, quindi **il residuo e' `-0.04`: ZERO entro il rumore.**
> **E IL DATO LO DICEVA GIA':** `exp(T1+T3)` **piatto** (`x1.00`-`x1.08`) mentre `ramp` cresce
> `x5.20` — con `0.8` potenze varierebbe di **`x3.74`**. **La piattezza esclude `0.8`.**
> ⇒ **`W^2` CHIUDE L'ESPONENTE**, e il sigillo lo conferma: `F1` e `F2` PASS.
> *(Resta fuori una domanda diversa: **perche' la coppia non porta `ramp`** — riguarda il termine
> `_tq*ramp`, non l'inerzia.)*
> **E il rischio vero e' il PAVIMENTO:** dividere due volte abbassa l'inerzia due volte. Con `/W`
> non mordeva (`min 0.0655`, quattro ordini sopra `1e-6`); con `/W^2` **va misurato** (`C5`).
> **❌❌ E IL SUO PRIMO RIPIEGO ERA UN DIFETTO, rilevato da Luca prima che il sigillo girasse:**
> `if ... or np.any(_wn <= 0.0)` — **una condizione GLOBALE su una grandezza LOCALE**. Un solo
> nodo con somma dei pesi zero **spegneva la cura per tutto il sistema in quel passo**, e **non
> era un caso raro: era IL CASO**, perche' i figli della mitosi nascono con `ramp = 0`, quindi i
> loro archi hanno `w = 0`. **Ogni nascita spegneva la cura** — e i figli sono **esattamente cio'
> che la cura doveva sistemare.** ✅ **Ora il ripiego e' PER NODO** (`np.where`), e i contatori
> sono **per NODO**: `_g_ci_nodi_senza_peso` su `_g_ci_nodi_tot`, piu' **quanti di quei nodi sono
> NATI IN DINAMICA** *(discriminante: `eta` finito contro `+inf` di `RAMPA-1`; senza
> `SEMINA_MATURA` il contatore vale `-1`, **dichiarato invece che finto**)*.
> **⚠ `rho_spin` e' il MODULO QUADRO di `psi_spin`**, che e' a sua volta una somma pesata ->
> **`rho_s ~ W^2`**: dividere per `W` **una volta** toglie **una** potenza, quindi se la
> dipendenza e' quadratica **il residuo non si azzera**.
>
> ### ❗ **IPOTESI DI LUCA (2026-09-25): E SE FOSSE UN RITARDO DI `peq`, NON UN'ESTENSIVITA'?**
> `_peq_nodo` e' una **MEMORIA** che rilassa verso `rho` con `tau_bg`. **All'equilibrio i due
> seguono lo STESSO vicinato, e il loro rapporto potrebbe essere GIA' intensivo.** Due fatti:
> * nella prova di limite gli archi si tagliano **DI COLPO**: `rho` reagisce subito, **`peq` no**;
> * **i figli della mitosi EREDITANO `peq` dall'arco del genitore** *(vicinato ~77)*, mentre il
>   loro `rho` viene da **2** vicini.
>
> **Se e' un ritardo, la cura NON e' normalizzare** — cambierebbe l'inerzia di **TUTTI** i nodi
> di `~1/77` — **ma il `peq` alla nascita dei nuovi archi.** **La misura decide, e la decisione
> e' di Luca.** *(Criteri nel task history, scritti prima.)*

**IL DIFETTO, MISURATO** *(`CONFIG-1/a`, configurazione del driver, 2 semi × 2 versi del
taglio, 20 bersagli per seme; `csv/_test_fork/_limite_accoppiamento2.py`)* — pendenze su
`log k`, dove `k` e' il numero di relazioni del nodo:

| grandezza | pendenza | lettura |
|---|---|---|
| **COPPIA** | `-0.19 … -0.30` | **INTENSIVA**: non cresce col numero di vicini |
| **`_contrasto`** | **`+1.06 … +2.47`** | **ESTENSIVO** |
| `_T2` | `-0.15 … +0.44` | fa cio' che la geometria impone |

```
da k = 77 a k = 2:   INERZIA x2e-4 ... x4.6e-3     coppia/inerzia x427 ... x1.5e4
                     |omega|  x4.4  ... x176        <- IL DIFETTO ARRIVA ALLA DINAMICA
```

> ### **DUE FATTORI DELLA STESSA EQUAZIONE SCALAVANO IN VERSO OPPOSTO NEL NUMERO DI VICINI.**
> **LA CAUSA E' DI STRUTTURA, non numerica:** `rho_s` e' una **SOMMA pesata sui vicini**
> (`psi = _mat(w) @ …`), `_peq_nodo` e' **esplicitamente una MEDIA**. **Un rapporto
> somma/media scala col grado per costruzione.**

**PERCHE' LA CURA E' *LOCALE*, e perche' la localita' era la parte da decidere:** `rho_s`
entra anche in **`lambda_nodi`**, nella **soglia della mitosi**, nella **densita' della coppia
Schwinger** e nella **tabella degli invarianti**. Normalizzarlo **alla fonte** avrebbe
cambiato **il campo**; normalizzarlo **dentro `_contrasto`** cambia **l'inerzia**.
**Le sette letture fuori da `_passo_spinoriale` sono elencate in `doc/LETTURE_rho_s.md`**, e
**nessuna vede la normalizzazione** — quattro di esse si trovano **solo cercando le
STRINGHE**, ed e' la lezione che l'audit di `eta` ha pagato lo stesso giorno.

## ⭐ **LA CURA DEL 2026-10-05 — `Z43` CURA (1): `r` VA UNA VOLTA SOLA**
*(decisione di Luca; sigillo `csv/_seal_fork/_sigillo_z43_cura1.py`)*

> ### ⛔ **L'OROLOGIO DI COMPTON CONTAVA `r` DUE VOLTE.**

**LA FORMA, PRIMA** *(e le righe sono di `1feb9b0a`)*:

```
r_node    = dtn/DT                      = r                        :5939
omega_clk = coerenza_arco * r_node                                 :5970
omega_clk = omega_clk * (cs_prec/CS_M)^2                           :5994
_phc      = exp(-0.5j * s_k * omega_clk * _dts)   _dts = DT*r      :5995
```

### ⛔ **L'incremento di fase era `-0.5*coerenza*(cs/CS_M)^2*DT*r^2`: `r` AL QUADRATO**
— una volta nella **frequenza**, una volta nel **tempo**.

**LA FORMA, DOPO:** `omega_clk = coerenza_arco` *(e poi `* (cs/CS_M)^2`)*, e `r` resta
### **solo in `_dts`.**

### **PERCHE' E' UN DIFETTO E NON UNA SCELTA: e' ANALISI DIMENSIONALE.** L'incremento
di fase e' **frequenza x tempo**. ### **Una frequenza PROPRIA non contiene il ritmo del
proprio tempo:** contenerlo e' ### **contare lo stesso fattore due volte.**

### ✅ **E IL MOTIVO E' MISURATO, non argomentato:** il `BRACCIO A` del referto
`66a798d` ha tolto ### **proprio questo fattore** su una copia, e l'altalena e'
### **crollata:**

| | prima | col fattore tolto |
|---|--:|--:|
| rapporto dispari/pari di `abs(f)` | `5.283` | ### **`1.034`** |
| rapporto dispari/pari di `C0` *(il `r` di oggi)* | `7.185` | ### **`1.031`** |

### **LA CURA TOCCA DUE RIGHE, e il censimento dall'AST dice che sono tutte:**
`:5970` *(il ramo `DEPARAM_OROLOGIO`, **che gira**)* e `:5982` *(il ramo **legacy**,
che ### **non gira** — `DEPARAM_OROLOGIO = True`)*.
### ⚠ **Il legacy si cura perche' e' LA STESSA LEGGE, ma NESSUN SIGILLO PUO'
MISURARLO GIRANDO:** la sua cura e' verificabile ### **solo dall'AST e dalla
lettura.**

### 📌 **E `r_node` NON E' PIU' LETTO DA NESSUNO** *(verificato dall'AST: scritture
`[5939]`, letture `[]`)*. ### **L'assegnazione RESTA, col suo commento:** la decisione
era *«si toglie `r_node` DALLA FREQUENZA»*, non *«si toglie `r_node»*, e
### **chi la togliesse domani non starebbe pulendo: starebbe cancellando la traccia di
una legge che c'era.**

### **`9-ter`: il conto delle leggi NON cambia** — una legge ### **perde un fattore**,
e nessuna entra. ### ✅ **E toglie un'ECCEZIONE alla regola <<frequenza propria per
tempo proprio>>**, che il resto del simulatore rispetta.

### ⚠ **E IL SEGNO NON CAMBIA, e va detto perche' e' facile sbagliarsi:** `r_node` e'
`dtn/DT`, cioe' ### **non negativo** *(`r` sta in `[1.414e-06, 1.414212977]`)*.
### **Togliere un fattore positivo non cambia il segno di `omega_clk`.**

## `A11` — IL PAVIMENTO `1e-6`

**Resta, e deve diventare INERTE.** Misurato **prima** della cura: `0/20` — **non morde mai**,
quindi non stava nascondendo il crollo. **Con la cura va RI-misurato**: se comincia a mordere,
la cura abbassa l'inerzia **in assoluto** e non solo la sua pendenza, e `A11` chiede di
guardare **l'errore che il pavimento nasconde**, non il pavimento.

## COSA LEGGE E COSA SCRIVE

**legge** `rho_s` *(via `_rho_sorgente()`)*, `peq` d'arco *(per `_peq_nodo`)*, `d_nodo` e
`cs_nodo` *(per `_T2`)*, `omega_s`, `_tau`. **scrive** `omega_s`, e i contatori `A8`
`_g_ci_tot` / `_g_ci_senza_cn` / `_g_ci_vic_p50` / `_g_ci_vic_min`.

**⚠ `_cn = None`** *(nessun arco valido)* **non si aggira con un `1`:** in quel caso `_ok_n` e'
falso e `_contrasto` vale **1** per la convenzione del primo passo, **la stessa di
`_cs_nodo_prev`**. Il ramo e' **CONTATO** (`_g_ci_senza_cn`), non assunto impossibile (`P5`).

## STATO

**`CONTRASTO_INTENSIVO` e' OFF di default**, e **non e' nel driver**, finche' il sigillo non
passa (decisione di Luca). **`STANDARD 10`: nessuna legge nuova, nessuna grandezza nuova** —
`_cn` esiste tre righe sopra, e la cura **toglie** un'incoerenza invece di aggiungere un
termine.

<!-- SCHEDA nome=torsione-spinore funzioni=_passo_spinoriale,_applica_flag flag=TW_SPINORE,SYNC_SPINORE,SPIN_LARMOR,SPIN_FEEDBACK -->

# ⑧ TORSIONE → SPINORE — **il ponte INVERSO**

> ### 🗄 **(b)2, 2026-09-27: `nb_vic` non ha piu' il ramo sincrono**
>
> **`SYNC_UPDATE` e' un NO-OP ACCETTATO dal 2026-09-27** *(passo `(b)2` di `ETC-PASSO`)*: i
> suoi rami sono in **`csv/_archivio/_sync_update.py`**, tag **`pre-archivio-sync`**, e `--sync`
> si accetta senza fare niente. **Il suo raggio era UNA legge su cinque** -- `7` usi in
> `_passo_spinoriale`, `6` in `step`, **ZERO** nelle altre quattro -- e **tutte e 56 le letture
> miste `t`/`t+1` misurate nella FASE 0 stavano FUORI da quel raggio.**
>
> Il campo dai vicini leggeva `nb_prec_t` sotto `SYNC_UPDATE` e `self._nb_prec` altrimenti.
> **Ora resta solo la causalita' vera** -- il Bloch **ritardato** del passo precedente -- con
> il suo fallback `A8` gia' contato (`_g_nb_prec_tot`, `_g_nb_prec_quando`), **che non e'
> toccato**.
> ⚠ **`SYNC_SPINORE` NON e' `SYNC_UPDATE`:** `_forza_sync`, `_wI_sync`, `_uno_sync` sono gli
> ingredienti del torque `SU(2)` e **restano**. Due flag con `SYNC` nel nome, due cose diverse.


> **→ LA LEGGE DELL'INERZIA (`omega = coppia/inerzia`) HA UNA SCHEDA SUA dal 2026-09-25:**
> **`inerzia-spinoriale`**. Sta qui il rimando perche' `_passo_spinoriale` compare in
> entrambi i marcatori, e **un lettore che arriva da `torsione-spinore` non deve credere che
> l'inerzia sia descritta qui.** *(La cura `INERZIA-1(C)` del 2026-09-25 — il contrasto «per
> vicino» — e' descritta li', coi numeri che l'hanno motivata.)*

> **Scheda aperta il 2026-09-24 per `CURA 1b`.** È l'unica legge del registro che esiste
> **per essere bloccata**, non per essere applicata.

## LA FORMA, dal codice

```
:3095   _twh = self.tw[mask] / (2.0 * max(PHI_CRIT, 1e-9))
:3097   _otw = np.zeros((n, 3));  _degt = np.zeros(n)
:3098   np.add.at(_otw, ii, _axis * _twh[:, None])          # mutazione IN PLACE
:3099   np.add.at(_otw, jj, _axis * _twh[:, None])
:3100   omega_new = omega_new + _otw / np.maximum(_degt[:, None], 1.0)
```

**Il verso è: `tw` → `omega_s` → `_psi_spinor`.** La **torsione**, che prende la sua scala da
`phi`, **scrive lo SPINORE**.

## PERCHÉ È IL VERSO SBAGLIATO

**È la classe `INVERSA` della mappa del `4pi`** *(`csv/_test_fork/_diag_D/MAPPA_4PI.md`:
`:3100` e la sua conseguenza `:3264`, le **uniche due** su 139 punti)*.

| | |
|---|---|
| il `4pi` di `_psi_spinor` | **`VERA`**: un oggetto di spin 1/2 torna in sé dopo `4pi`. È fisica |
| il `4pi` di `phi` | **`DICHIARATA`**: una **convenzione del codice** |
| `tw` | **`EREDITATA`**: prende la scala da `phi` |

**Quindi `TW_SPINORE` fa scrivere il `4pi` VERO dal `4pi` FINTO.** E la freccia causale del
par.4 di `CLAUDE.md` dice l'opposto: *«i nodi guidano, gli archi ricordano»* — **se in un test
gli spinori diventano passivi (il link li comanda) → BUG, da rilevare, non l'obiettivo.**

## E IL COMMENTO È FALSO, che è una ragione in più

Il commento (`:705-709`, `:2146-2148`) dice che la torsione *«pilota il Bloch di `tw/2`»*, cioè
un **ANGOLO**. **Il codice somma `tw/(2·PHI_CRIT)` a `omega_new`, che è una VELOCITÀ
ANGOLARE**: l'angolo effettivo è **`1.564e-03` rad/passo** contro i **`9.827e-01`** dichiarati,
**fattore `628.3 = 2π/DT`** — *un'unità di misura mancante, non un'approssimazione*.
E il termine finisce in **`self.omega_s`**, la **memoria persistente**, mentre il commento di
`SYNC_SPINORE` dice, **dello stesso blocco**, che metterci un torque *«darebbe
accumulo/divergenza»*. **Unico fra i termini del blocco, `_otw` NON è diviso per l'inerzia.**
→ `doc/REFERTO_tw_spinore.md`, fronte `W`.

## ✅ NON HA MAI GIRATO — **misurato, non supposto**

**`TW_SPINORE = False` in 9 run su 11 ricostruibili**, e **`--tw-spinore` non compare in
nessun lanciatore committato** a nessuno di quei commit
*(`csv/_test_fork/_RICOSTRUZIONE_config.txt`, `Z128`)*. I due non ricostruiti sono i due
`controllo`, che non lasciano snapshot.

> **Nessuna misura di questo programma è contaminata da questa legge.** È il motivo per cui
> bloccarla **non ritira nulla**.

## LA CURA — `CURA 1b`: **il simulatore RIFIUTA DI PARTIRE**

**Decisione di Luca, 2026-09-24.** `TW_SPINORE` resta **nel codice, spento, e BLOCCATO**: se
qualcuno lo accende, il simulatore **si ferma con la ragione**.

**Perché un blocco e non la cancellazione:** par.10 — *«il codice di una legge esclusa non si
cancella mai: resta spento, ed è l'evidenza che spiega perché esiste il suo sostituto»*.
`TW_SPINORE` esiste **perché** `SPIN_LARMOR` fallisce: cancellarlo farebbe perdere il
**perché**.

**Perché un blocco e non un semplice default spento:** il default è già spento, e **non ha
impedito nulla** — `A9`: *un presidio che non impedisce non è un presidio*. Un flag che
introduce il **verso sbagliato del ponte** non deve poter essere acceso **per sbaglio**, e
oggi basterebbe `--tw-spinore`.

**Che cosa NON è:** non è una cura di un difetto misurato, perché **la legge non ha mai
girato e quindi non ha prodotto nulla da curare**. È un **presidio strutturale**, e va detto
così invece di contarlo fra le cure.

## COSA NON SI SA DERIVARE — **dichiarato** *(`A12` regola 4)*

**Se un ponte torsione → spinore possa esistere AFFATTO, in qualche forma.**
L'architettura a un solo ponte dice che la torsione va **ricavata dal trasporto degli
spinori** *(olonomia SU(2))*, non dalle differenze di `phi`. **In quell'architettura la
domanda cambia**: la torsione sarebbe già una proprietà degli spinori trasportati, e una
retroazione su `omega_s` **non sarebbe più un ponte inverso** — sarebbe dinamica interna.
**Non lo so derivare oggi, e non lo decido: è la domanda che il `CHECKPOINT` mette a Luca.**

## ✅ LA CURA È IN CODICE — 2026-09-24

**`_applica_flag`, subito dopo `TW_SPINORE = bool(getattr(a, "tw_spinore", False))`:**

```python
if TW_SPINORE:
    raise SystemExit("[tw-spinore] RIFIUTO DI PARTIRE: e' il ponte inverso. ...")
```

**Il messaggio nomina la ragione** *(il ponte inverso, le righe `:3090-3100`, la scheda, il
referto col commento falso)* **e dice come riaprirlo**: *«una decisione di Luca, non la
rimozione di questa riga»*.

**Perché in `_applica_flag` e non nel punto d'uso:** lì il rifiuto arriva **prima che la scena
nasca**, quindi non c'è nessun run a metà da interpretare. Un rifiuto dentro `step()` lascerebbe
uno stato parziale sul disco.

---


### ➕ `CURA 4` TOCCA `_passo_spinoriale` a `:3382` *(2026-09-25)*

Quella riga **deve seguire `_pesi`**: il suo commento dice *«la STESSA riga di `_pesi()`»*, e se una usasse `TAU_A` e l'altra il tempo-luce sarebbero **due leggi che possono divergere** — la ragione per cui `_tempo_luce_nodo` fu **estratto in un metodo solo**. Ora entrambe passano da `_tempo_rampa()`. **`:3334` NON cambia: lì `TAU_A` resta, ed è il suo unico ruolo superstite.**

<!-- SCHEDA nome=tempo-nella-mitosi funzioni=mitosi,_cs_arco_da_nodo,_r_nodo_mitosi,_fattore_tempo_arco,_tau_arco_causale flag=TEMPO_UNICO_MITOSI,MITOSI_DIR -->

# ⑨ IL TEMPO NELLA MITOSI — **`CURA 2`**

> ### ✅ **STRUTTURALE DAL 2026-09-27** *(decisione di Luca)*. **NON E' PIU' UN FLAG: E' UNA LEGGE.**
> I **quattro** rami `else` di `TEMPO_UNICO_MITOSI` **sono usciti dal simulatore**; la
> costante e' **`True`** e **l'assegnazione e' stata tolta da `_applica_flag`**: **nessun
> percorso puo' piu' spegnerla.** `--tempo-unico-mitosi` resta **accettata come NO-OP
> dichiarato** *(il driver la passa in ogni run)*, **e avvisa**.
> **NON c'e' un `--senza-tempo-unico-mitosi`, e va detto:** `par.10` lo chiede per una
> **promozione**, dove il ramo OFF resta nel codice. **Qui i rami ESCONO**, e il braccio
> OFF vive **al tag**, non in un flag.
> **DOVE SI RITROVANO:** tag **`pre-cura2-strutturale`** *(blob del simulatore al tag:
> **`dd4f5ccf`**, sha1 byte grezzi)*, e archivio **`csv/_archivio/rami_off_cura2.py`**
> — **quattro** rami, **13 righe**, **copiate dal sorgente da uno script**, ciascuna con
> funzione, righe al tag, cosa faceva e perche' e' uscita.
> **SI RILANCIA CON:** `git cat-file -p pre-cura2-strutturale:soliton_simulator.py`,
> **in BINARIO** *(par.5-quinquies: `git checkout` riscriverebbe le newline)*.
>
> **Mandato di Luca, 2026-09-24.** Flag: **`TEMPO_UNICO_MITOSI`**, spento di default
> *(storico: e' cosi' che e' nato)*.
> **Riscritta** dopo il mandato: la prima stesura aveva **due errori**, segnati con ❌.

## 0. IL PRINCIPIO, ed è di Luca

> ### **«Si applicano le cose CORRETTE e COERENTI. Dove intenzione e implementazione
> ### divergono, si realizza l'INTENZIONE. Ogni grandezza con le sue UNITÀ giuste.»**

**Operativamente: si cura dove intenzione e implementazione DIVERGONO; dove sono coerenti non
si tocca.** L'intenzione si legge **dal commento e dal nome**, che sono ciò che la legge
*dichiara di essere*.

| riga | l'INTENZIONE, dal commento | l'IMPLEMENTAZIONE | coerenti? |
|---|---|---|:--:|
| `:5240` | *«ritmo»* | `1/(1 + |tw|/PHI_CRIT)`: reciproco di una **torsione** | **NO** |
| `:5244` | una **probabilità** | `clip(resp, 0, 1)`: un **clip** `A11` | **NO** |
| `:5280` | *«rilassa con tempo `tau_pp` — **un tempo locale dello stesso arco**»* e *«`A5` livello 1, **rilassamento esponenziale**»* | una **torsione** come costante di tempo, **e un EULERO esplicito** | **NO, due volte** |
| `:5189-5196` | *«gradiente di **tempo proprio** lungo l'arco»* | gradiente di `mean(|tw|)` | **NO** |
| `:5234-5239` | soglia, tetto, centro, **inversione**: posizioni sull'asse di `tw` | esattamente quello | **SÌ → NON SI TOCCA** |

---

## 1. UN SOLO TEMPO D'ARCO: **`dt_e`, che il sistema definisce già**

**`:4352`: `dt_e = DT * 0.5 * (r[i] + r[j])`.** È **il** tempo proprio d'arco del sistema, e la
mitosi usa **quello**, cioe' il fattore adimensionale **`dt_e/DT = 0.5(r_i + r_j)`**.

### ❌ **IL MIO PRIMO ERRORE: avevo proposto `min(r_i, r_j)`**

**Era sbagliato per la ragione più semplice: creava un SECONDO orologio d'arco**, accanto a
quello che il sistema ha già. *«Un solo tempo»* è il nome di questa cura, e la mia proposta ne
aggiungeva uno.

**E l'argomento con cui l'avevo scartata la media era anch'esso sbagliato:** avevo scritto che
una media *«viola `A2`, è una statistica in una legge locale»*. **`A2` riguarda le statistiche
GLOBALI** — una mediana su tutta la rete, una media su tutti i nodi. **La media dei DUE nodi di
un arco è locale per costruzione**, ed è la definizione che il sistema usa già.

> **L'argomento causale per `min(r)` non è privo di senso, ma se vale, vale per TUTTO il
> sistema, non per la mitosi da sola.** → va **in coda** come proposta generale, `S13`.

### ⚠ **E la media ARMONICA esisteva già, per il `cs`**

`:4774`: `cs_arco = 2·cs_i·cs_j / (cs_i + cs_j)`, col commento *«**collo di bottiglia causale:
media armonica, non media aritmetica**»*. **La mia tabella delle alternative la liquidava con
«vale per rate in serie, e l'arco non lo è»: era sbagliato**, perché il sistema la usa
esattamente per questo e la chiama col suo nome.
**Il sistema ha quindi DUE medie d'arco, ciascuna col suo dominio:** **aritmetica** per il
**tempo** (`dt_e`), **armonica** per la **velocità** (`cs_arco`). **Non se ne inventa una terza.**

---

## 2. IL GRADIENTE DI TEMPO PROPRIO — **su `r`, e la ragione è derivata**

**Oggi** (`:5189-5196`): `tau_nodo = 1 + mean(|tw|)/PHI_CRIT` per nodo, poi
`grad_tau = |tau_i − tau_j|`, poi `soglia = soglia0·(1 − 0.3·tanh(grad_tau))`.

**`tau_nodo` è IDENTICO al ramo `TEMPO_SEGNO` di `ritmo()` — quello che NON GIRA** *(`Z130`)*.
**La mitosi usa come «tempo proprio» la definizione di tempo che il resto del sistema ha
SCARTATO.** Sono **due orologi nello stesso passo**.

**Con la cura: `grad_r = |r_i − r_j|`.**

### **`r` o `1/r`? Si prende `r`, e NON è una preferenza**

`tau_nodo` oggi è una **lentezza** *(«tau_nodo alto = tempo lento», lo dice il commento)*, e
l'analogo diretto della lentezza è **`1/r`**. **Ma `1/r` È ILLIMITATO**, e il conto lo mostra:

| | intervallo | `tanh` del gradiente | la modulazione `1 − 0.3·tanh` |
|---|---|---|---|
| **`r`** | `[1.4142e-6, 1.4142]` | `tanh(grad) ≤ tanh(1.4142) = 0.8884` | **`[0.7335, 1]·soglia0` — MODULA** |
| `1/r` | `[0.707, 707107]` | `grad` fino a `~7e5` → **`tanh = 1` ESATTO** | **`0.7·soglia0` COSTANTE** |

> **Con `1/r` la modulazione diventa un RISCALAMENTO COSTANTE della soglia**, cioè **un
> parametro nascosto** *(`A1`)*, non una legge. **Con `r` resta una modulazione.**
> **`A11` cor.6: un limite che satura è un allarme** — e `1/r` lo farebbe saturare **sempre**.

---

## 3. IL RILASSAMENTO DI `_rep` — **`S12` APPROVATO DA LUCA**

**Oggi** (`:5280`): `self._rep += _dte * (rep − self._rep) / max(tau_pp, 1e-12)`.

**Tre difetti nella stessa riga, e il commento ne dichiara due:**

| | |
|---|---|
| **① la DILATAZIONE È CONTATA DUE VOLTE** | `_dte` **è già** `DT·0.5(r_i+r_j)`, cioè contiene già il tempo proprio; dividere **anche** per `tau_pp` la conta una seconda volta |
| **② `tau_pp` non è una durata** | è un numero puro *(un fattore di dilatazione)*. Una costante di tempo **deve avere le unità di un tempo** |
| **③ l'integratore è un EULERO ESPLICITO** | il commento dichiara *«`A5` livello 1, **rilassamento esponenziale**»*, e `par.4` impone la **forma esatta** |

### **LA DURATA, DERIVATA: `tau_arco = d / cs_arco`**

**È il ritardo causale dell'arco**, e **le due grandezze esistono già**:

| | | unità |
|---|---|---|
| `d` | la **lunghezza dell'arco**, `self.d` | `[LAM]` |
| `cs_arco` | la velocità d'onda d'arco, **media armonica** *(`:4774`)* | `[LAM/DT]` |
| **`tau_arco = d / cs_arco`** | **una DURATA** | **`[DT]`** ✅ |

**È la stessa legge che `FORK_SU2_MEM` usa per il ritardo dei Bloch** *(`tau = d/cs`,
`_tempo_luce_nodo`)*, **al livello dell'ARCO invece che del nodo** — e al livello dell'arco `d` e
`cs_arco` sono **direttamente disponibili**, senza la media sul grado che la versione nodale deve
fare. **Zero parametri nuovi, zero coefficienti.**

### **LA FORMA ESATTA**

```
_rep  <-  rep + (_rep - rep) * exp(-dt_e / tau_arco)
```

**L'esponente è `[DT]/[DT]` = numero puro.** È la stessa forma che `PEQ_ESATTO` (`C1`) ha imposto
a `peq` e che `par.4` impone a ogni rilassamento di primo ordine. **È una combinazione convessa**,
quindi `_rep` resta **fra `rep` e il suo valore precedente per QUALUNQUE passo**: non può
scavalcare, e il difetto che l'Eulero aveva su `peq` *(`dt/tau > 1` misurato `1.2018`)* **non può
ripresentarsi**.

### ⚠ **PRECISAZIONE 1 del guardiano: `cs_arco` NON È DISPONIBILE in `mitosi()`**

**È una LOCALE di `step()`** (`:4774`), **non un attributo.** Quindi `tau_arco = d/cs_arco` va
**ricostruito** dentro `mitosi()` da **`self._cs_nodo_prev`** — che è **classe `A8b`**, la stessa
di `_cs_nodo_prev` quando era **stale al `71.88 %`**.

**TRE conseguenze, tutte obbligatorie:**

#### ① **UNA SOLA FORMULA, non due copie**

Si **estrae una funzione** per la media armonica d'arco, e la chiamano **entrambi**: `step()`
(`:4774`) **e** `mitosi()`.

```
_cs_arco_da_nodo(cs_nodo, i, j)  =  2·cs_i·cs_j / max(cs_i + cs_j, 1e-12)
```

**È lo stesso argomento del docstring di `_tempo_luce_nodo`:** *«UNICO punto del file in cui
questa relazione è scritta … duplicarla avrebbe significato avere **due leggi che possono
divergere**»*. **Due copie della media armonica sarebbero due leggi.**

#### ② **LA GUARDIA SU `_cs_nodo_prev` SI CONTA** *(`A8`, quattro numeri)*

invocazioni · salti · **la forma** al fallimento *(le due lunghezze; `-1` = assente)* ·
**quando** *(l'indice dell'ultima saltata)*.

**Il fallback è `CS_M`**, e **non è una convenzione nuova**: è esattamente ciò che `step()` fa
già a `:4778` quando `CS_DINAMICO` è spento — `cs_arco = np.full(len(i), CS_M)`.

#### ③ **IL SIGILLO DEVE PROVARE CHE L'ESTRAZIONE NON CAMBIA `step()`**

**A flag SPENTO, `step()` deve restare byte-identico dopo l'estrazione della funzione.**
È la stessa prova che l'estrazione di `_tempo_luce_nodo` ha dovuto dare *(«senza cambiarne una
virgola»)*, e **non è ovvia**: un'estrazione può cambiare l'ordine delle operazioni in
virgola mobile.

### ⚠ **I CLAMP: uno SPARISCE, uno NASCE** *(`A11`)*

### ✅ **DECISIONE DI LUCA, 2026-09-24: NON SI SCRIVE NESSUN CLAMP. È UNA LEGGE.**

> ### **«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema» è una
> ### LEGGE, non una garanzia che dipende da un flag.**

**Quindi in `CURA 2` `tau_arco = d / cs_arco` si scrive COSÌ, senza `np.maximum`.** Se uno dei
due fosse zero, **il livello NUMERICO di `C5` alza un'eccezione con la riga esatta**:
`np.seterr(over='raise', divide='raise', invalid='raise')` a **`:7382`**. **È `A11` fatto bene:
un limite che protegge da un errore si sostituisce con il RILEVAMENTO dell'errore.**

#### ① **`d ≥ LAM`: L'INVARIANTE ESISTE — MA È GATED SU UN FLAG, ed è il difetto**

`DOMINI['d'] = ('lam', …)` e `DOMINI['d0'] = ('lam', …)` **ci sono** (`:215-216`). Ma il
controllo, a **`:3702`**, è:

```python
_lam_attivo = SCALA_MIN or SCALA_MIN_PASSO        # :3657
…
if _lam_attivo:
    cattivo = ~fin | (vf < LAM * (1.0 - 1e-12));  regola = '>= LAM, con la scala minima accesa'
else:
    cattivo = ~fin | (vf <= 0.0);                 regola = '> 0 (scala minima SPENTA)'
```

> **Una LEGGE verificata solo quando un flag è acceso non è una legge: è un'opzione.**
> **→ va reso INCONDIZIONATO**, ed è la voce `E4-LAM` della coda: **non lo faccio in `CURA 2`**,
> perché cambierebbe il comportamento di una configurazione diversa da quella dei run *(a flag
> spenti, un `d < LAM` oggi passa e domani fermerebbe il run)*, **e quella è una decisione di
> Luca su `C5`, non un pezzo di questa cura.**
>
> **Per `CURA 2` non serve:** nei run `SCALA_MIN_PASSO` è **acceso**, quindi l'invariante
> controlla `d ≥ LAM` **davvero**, e **misurato**: `min(d) = 0.800000 = LAM` esatto, `0` archi
> sotto su `526302`.

#### ② **`cs` NON PUÒ ESSERE ZERO — derivato dal codice, non misurato**

```python
_scala      = max(_Lam, 1e-30) / GAMMA_TURBO**2
cs_floor    = CS_M / (1.0 + sqrt(_I) * sqrt(1.0/_scala))      # > 0: il denominatore e' >= 1
cs_floor    = min(cs_floor, CS_M)                             # quindi 0 < cs_floor <= CS_M
transizione = 0.5 * (1.0 + tanh(1.0 - u_nodo))                # in (0, 1) STRETTO
return        cs_floor + (CS_M - cs_floor) * transizione      # >= cs_floor > 0
```

**`cs ∈ (0, CS_M]` PER COSTRUZIONE**, e `cs_arco` è la **media armonica di due numeri
positivi**, dunque **positiva**. *(La misura concorda e non serve alla dimostrazione:
`min(cs) = 4.3465e-01`, **`0` zeri esatti** su `2660` nodi.)*

> **Quindi è un INVARIANTE, non un caso da contare** — e si aggiunge a `DOMINI`:
> `'_cs_nodo_prev': ('pos', …)`. **Legge soltanto: su un run sano non cambia un bit.**
> **Nel ramo `CS_DINAMICO` spento `cs_arco = CS_M` costante**, quindi positivo anche lì.

### ❌ **E RESTA LA MIA CORREZIONE SUL CONTO DEI CLAMP, perché il primo pezzo era giusto**

**Avevo scritto** che *«due clamp spariscono per costruzione»*. **Il secondo era falso**, e l'ho
visto controllando invece di assumere.

| clamp | prima | dopo | verdetto |
|---|---|---|---|
| `max(tau_pp, 1e-12)` | **È CODICE MORTO**: `tau_pp = 1 + |tw|/PHI_CRIT` con `|tw| ≥ 0`, quindi **`tau_pp ≥ 1` SEMPRE** e il clamp è **irraggiungibile** | esce dalla formula | **sparisce, e non proteggeva nulla** |
| `max(tau_arco, 1e-12)` | — | **NON SI SCRIVE** *(decisione di Luca)* | **`d ≥ LAM` è una legge e `cs > 0` è derivato: al posto del clamp c'è l'INVARIANTE** |

**Il primo pezzo resta vero e utile:** `max(tau_pp, 1e-12)` era **codice morto**, e accorgersene è il tipo di cosa che `A11` chiede. **Il secondo pezzo è caduto**: non nasce nessun clamp, perché `d ≥ LAM` è una **legge** e `cs > 0` è **derivato**.

**MISURATO nel giro di `CURA 1`** *(`SCALA_MIN = False`, **`SCALA_MIN_PASSO = True`**)*:

| | |
|---|--:|
| `LAM` | **`0.8`** |
| `min(d)` | **`0.800000`** — **esattamente `LAM`** |
| `min(d)/LAM` | **`1.0000`** |
| archi con `d < LAM` | **`0` su `526302`** |

> **Quindi nella configurazione dei run il clamp non morde — ma NON per costruzione: per via di
> un FLAG.** Si scrive il clamp, **si CONTA**, e si dichiara che la garanzia viene da
> `SCALA_MIN_PASSO`. **`A11`: un limite ammesso solo se esprime un vincolo dichiarato** — qui il
> vincolo è *«nessuna lunghezza sotto `LAM`»*, che è una legge del sistema, **non una
> protezione da un errore.** È legittimo **a condizione di dirlo.**
>
> **⚠ E IL CONTO DI PRIMA ERA SBAGLIATO PURE NEL NUMERO:** avevo scritto `min(d)/LAM = 2.0000`
> perché il mio script aveva `LAM = 0.4` cablato a mano invece di leggerlo. **`LAM` è `0.8`**, e
> il rapporto è **`1.0000`**. *(`P1-ter`: un numero ricopiato a mano non ha provenienza.)*

---

## 4. LA PROBABILITÀ DI MITOSI — **la forma di Poisson, e il clip sparisce**

**Oggi** (`:5244`): `prob = np.clip(resp, 0.0, 1.0)`. **Un clip `A11` su una probabilità.**

**Con la cura:**

```
prob = 1 - exp(-max(resp, 0))
```

**Perché è DERIVATA e non scelta:** `resp` è il **numero atteso di eventi** nel passo proprio
locale *(un tasso per unità di tempo di coordinata, moltiplicato per `dt_e/DT`)*, e la
probabilità di **almeno un evento** di un processo di Poisson con quel numero atteso è
`1 − e^{−λ}`. **Sta in `[0, 1)` per costruzione: il clip non ha più niente da tagliare.**

**E per ampiezze piccole coincide con la vecchia forma:** `1 − e^{−λ} = λ − λ²/2 + …`, quindi
**l'errore relativo è `λ/2`**: sotto `λ = 0.02` le due forme differiscono di meno dell'`1 %`.

### ⚠ **IL FATTORE DI TEMPO VA CONTATO UNA VOLTA SOLA**

`tau_locale` **non si sostituisce con `dt_e/DT` lasciando poi un secondo `dt_e/DT`
nell'esponente**: sarebbe **la dilatazione contata due volte**, lo stesso difetto del par.3 ①.
**Il fattore compare UNA volta**, dentro `ampiezza`:

```
ampiezza = salita * discesa * (dt_e / DT)        # numero atteso di eventi
resp     = ampiezza * segno
prob     = 1 - exp(-max(resp, 0))
```

### ✅ **E LA SOSTITUZIONE TOGLIE UN DOPPIO CONTO DELLA TORSIONE**

`tau_locale = 1/(1 + |tw|/PHI_CRIT)` **decresce con la torsione**. Ma `discesa =
clip(1 − |tw|/TW_TETTO, 0, 1)` **fa già esattamente questo**, e va a zero al tetto.
**Quindi oggi la soppressione ad alta torsione è contata DUE VOLTE**, una in `discesa` e una in
`tau_locale`. **Con `dt_e/DT` resta contata una volta**, in `discesa`, dove la legge la
dichiara — e il fattore di tempo fa il mestiere del tempo.

---

## 5. ✅ **PRECISAZIONE 2 del guardiano: SÌ, È UN DOPPIO CONTEGGIO. LO CORREGGO.**

**La domanda:** con la cura, il ritmo `dt_e/DT` entrerebbe **due volte** nel ramo repulsivo —
nel **bersaglio** `rep` *(via `ampiezza`)* e nella **velocità del rilassamento** *(via `dt_e`
nell'esponente)*.

### **LA RAGIONE, in una riga, e dice CORREGGI**

> **Un'INTENSITÀ D'EQUILIBRIO non può dipendere dalla DURATA del passo: se dipendesse, la
> stessa condizione fisica darebbe un equilibrio diverso a seconda di quanto batte l'orologio
> locale. Una PROBABILITÀ PER PASSO, invece, DEVE dipenderne.**

**`rep` è il BERSAGLIO di un rilassamento**, cioè il valore verso cui `_rep` tende: è un
**equilibrio**. **`prob` è una probabilità nel passo**: è un **conteggio**. Sono due tipi
diversi, e il tempo entra **solo nel secondo**.

### **LA CAMPANA SI LEGGE DUE VOLTE, e ciascuna lettura ha le SUE unità**

```
ampiezza_int = salita * discesa                    # INTENSITA'   [numero puro]
ampiezza_ev  = ampiezza_int * (dt_e / DT)          # EVENTI ATTESI [numero puro]

resp_int = ampiezza_int * segno                    # -> il BERSAGLIO
resp_ev  = ampiezza_ev  * segno                    # -> la PROBABILITA'

rep   = clip(-resp_int, 0, 1)                      # equilibrio: SENZA tempo
prob  = 1 - exp(-max(resp_ev, 0))                  # per passo:  CON il tempo
_rep <- rep + (_rep - rep) * exp(-dt_e / tau_arco) # il tempo entra QUI, nella VELOCITA'
```

**Il tempo compare UNA volta per ciascuna grandezza, e mai due nella stessa.**

> ### ✅ **E COSÌ LA CURA CHIUDE UN DIFETTO CHE NÉ IO NÉ IL MANDATO AVEVAMO NOMINATO**
> **Oggi** `ampiezza = salita·discesa·(1/tau_pp)` **e `rep = clip(−ampiezza·segno, 0, 1)`**:
> quindi **l'equilibrio della repulsione dipende GIÀ da un fattore che il commento chiama
> «ritmo»**. Ed è la **terza** dipendenza da `|tw|` nello stesso bersaglio, dopo `salita` e
> `discesa`. **Togliendo il fattore di tempo restano le due che sono la legge** — attivazione
> sopra soglia, spegnimento al tetto — **e l'equilibrio smette di dipendere dall'orologio.**

### ⚠ **E IL CLIP SU `rep` RESTA, perché È RAGGIUNGIBILE — VERIFICATO, non assunto**

Avevo pensato di sostituirlo con `tanh` *(la normalizzazione che `COES_ADIM` usa per una
magnitudine)*, o di dichiararlo inerte perché il suo lato superiore è inarrivabile.
**Ho controllato, e NON è inarrivabile:**

| | |
|---|---|
| `satura(f) = f/(1 + GAMMA·|f|)` | → **`1/GAMMA`** per `f → ∞` |
| **`GAMMA = 0.05`** *(letto dal sorgente e dal referto di configurazione)* | → **`salita < 20`** |
| quindi `|resp_int| < 20` | **il clip a `1` MORDE**, e non di poco |

> **Quindi il clip resta in questa cura, e la sua sostituzione si DECIDE SU UNA MISURA, non su
> un'opinione:** `tanh` e il clip **coincidono dove il clip non morde** e differiscono solo dove
> mordeva. **Si conta quante volte morde** — è il criterio `K`, esteso da `prob` anche a `rep`.
> **Se non morde mai, la sostituzione è sicura; se morde, cambia la fisica e la decisione è di
> Luca.** *(`A12` regola 4: dichiarato, non deciso.)*

## 6. LA TABELLA DELLE UNITÀ

| grandezza | **prima** | **dopo** | nota |
|---|---|---|---|
| `DT` | tempo di coordinata | — | l'unità di tempo |
| `r` | numero puro | — | `dt_n = DT·r` |
| `dt_e` | `[DT]` | — | `DT·0.5(r_i+r_j)`, `:4352` |
| `dt_e/DT` | — | **numero puro** | il fattore di tempo proprio d'arco |
| `avv = |tw|` | `[rad]` | — | torsione |
| `soglia` | `[rad]` | `[rad]` | modulata da `grad_r`, non da `grad_tau` |
| `ecc = avv/soglia − 1` | numero puro | — | rapporto di due angoli |
| `salita`, `discesa` | numero puro | — | |
| `tau_locale` | numero puro *(ma **era** un reciproco di torsione)* | **`dt_e/DT`** | **ora è un tempo, come il nome dice** |
| `ampiezza` | numero puro **(con un fattore di tempo travestito)** | **si SDOPPIA** | vedi le due righe sotto |
| **`ampiezza_int`** | — | **numero puro** | `salita·discesa`: **INTENSITÀ**, senza tempo. Va al **bersaglio** `rep` |
| **`ampiezza_ev`** | — | **numero puro** | `ampiezza_int·(dt_e/DT)`: **eventi attesi**, col tempo. Va a `prob` |
| `segno` | numero puro `(−1, 1)` | — | resta |
| `resp` | numero puro | **si SDOPPIA in `resp_int` e `resp_ev`** | uno per il bersaglio, uno per la probabilita' |
| `rep` | numero puro **con clip**, e **col fattore di tempo** | numero puro **con clip**, **SENZA** il fattore di tempo | e' un **equilibrio**: non deve dipendere dalla durata del passo |
| `prob` | numero puro **con clip** | numero puro **in `[0,1)` per costruzione** | il clip sparisce |
| `tau_pp` | numero puro, **usato come TEMPO** | **esce dagli usi TEMPO** | resta solo come coordinata di torsione |
| **`tau_arco`** | — | **`[DT]`** | `d/cs_arco`: **una durata vera** |
| `_rep` | numero puro | — | rilassa in forma **esatta** |
| `grad_tau` → `grad_r` | `[rad]`/PHI_CRIT | **numero puro** | gradiente di un **ritmo** |

**Nessuna grandezza con unità diverse viene sommata o confrontata**: gli unici confronti sono
`avv` con `soglia` *(entrambi `[rad]`)* e `tau_pp` con `centro` *(entrambi numeri puri sull'asse
di torsione)*.

---

## 7. LA PROVENIENZA DI `r` DENTRO `mitosi()`, e la guardia

`r` per nodo è in `self._r_corrente`, scritto in `step()` a `:4397` **ma solo
`if FORK_SU2_MEM`**.

| questione | risposta, **dal codice** |
|---|---|
| è disponibile? | **sì**: il ciclo è `step(); mitosi(); …`, quindi `mitosi()` segue **immediatamente** |
| la lunghezza è giusta? | **sì in quel punto** — `n` non è ancora cresciuto. Ma è un array **per-nodo attraversato da un punto di crescita**: la classe `A8b` di `_cs_nodo_prev` *(`71.88 %`)* e `_psi_spin_prec` *(`95.33 %`)* |
| se `FORK_SU2_MEM` è spento? | `_r_corrente` è `None`. **Dipendenza DICHIARATA**: nei run del fork è acceso |
| indici d'arco `≥ n`? | il codice si guarda già *(`self.i[self.i < self.n]`, `:5190-5192`)*: si fa lo stesso, **e si conta** |

**LA GUARDIA SI CONTA, NON SI TACE** *(`A8`)*: **quattro** numeri — invocazioni, salti, **la
forma** al fallimento *(le due lunghezze)*, e **quando** *(l'indice dell'ultima saltata)*.
Il fallback è **`dt_e/DT = 1`**, cioè *«nessuna dilatazione»*: la stessa convenzione che
`ritmo()` usa quando non c'è un passato *(`np.ones`)*, **non una convenzione nuova**.

---

## 8. COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **se il clip su `rep` si possa sostituire con `tanh`** *(par.5)*: **non è una questione di principio ma di MISURA** — le due forme coincidono dove il clip non morde, e `GAMMA = 0.05` dice che **può mordere** *(`salita < 20`)*. **Il criterio `K` lo conta**, e poi decide Luca;
2. **il `0.3`** della modulazione della soglia: era un numero scelto **prima** della cura, e la
   cura non lo migliora né lo peggiora — **ne cambia la scala dell'argomento**, e il conto del
   par.2 dice di quanto *(`tanh ≤ 0.8884` invece di `→ 1`)*;
3. **il `3.0`** dentro `tanh(3.0·(tau_pp − centro))`: resta `TORSIONE`, resta com'è, **è un
   numero scelto** e la scheda lo deve dire;
4. **che il tasso di mitosi resti dello stesso ordine.** `1/tau_pp ∈ (0,1]` con mediana vicina a
   `1`; `dt_e/DT` ha **mediana misurata `≈ 0.68`** *(`Z135`)*. **Il tasso può calare di ~`1/3`**,
   e **`E1a` è il suo giudice**. *(Non metto un fattore di normalizzazione: sarebbe un numero
   scelto.)*

---

## 9. I CRITERI DELLA PROVA, fissati qui

| | criterio | origine |
|---|---|---|
| **`E1a`** | la mitosi **non muore**: nascite `> 0` e eventi **dello stesso ordine** del riferimento | di Luca. `FASE_2PI` è caduta qui *(`62` → `1` evento)* |
| **`E1b`** | **non esplode**: `n` finale `< 10×` il riferimento | **misurata**: `178` archi per nodo |
| **`B`** | il **bilancio di `d0` CHIUDE** | il criterio di `G4` |
| **`K`** | **quante volte il clip avrebbe morso**, su `prob` **E su `rep`** | richiesta di Luca, **estesa a `rep`**: dice **quanto la forma nuova differisce dalla vecchia**. Se su `prob` è `0`, la cura di `:5244` è **formale**. **Su `rep` decide se il clip si può sostituire con `tanh`**, e quella decisione è di Luca |
| **`H`** | **la guardia di `_cs_nodo_prev`**: invocazioni, salti, forma, quando | `A8`. Era **stale al `71.88 %`** in passato: se salta, `tau_arco` cade su `CS_M` e **il rilassamento non è quello dichiarato** |
| **`G`** | **dove nasce la materia rispetto al gradiente di `r`** | richiesta di Luca. **Si RIPORTA**, non si giudica |
| **`R`** | **`d0` e `d/d0` con i QUANTILI (`p10`, mediana, `p90`) e la divisione VUOTO / CONFINE / MASSA**, più il **TERMINE DELLA REPULSIONE nel bilancio**, contro `_cura1_corto` | **richiesta di Luca, 2026-09-24**, e la previsione è **sua e derivata**: togliere il fattore di tempo dal bersaglio di `rep` **ALZA l'equilibrio della repulsione**, che **allarga `d0`**. **Quanto:** il bersaglio viene moltiplicato per `tau_pp = 1 + |tw|/PHI_CRIT`, e nel regime repulsivo `tau_pp > centro = 2.5`, quindi **circa ×2.5-×3**. **Si RIPORTA il verso e l'ampiezza**, e se `d0` si allarga **non è una sorpresa: è la previsione**. **⚠ E LA MEDIANA DA SOLA NON BASTA — rilievo di Luca, 2026-09-24:** *«la mediana è un riassunto GLOBALE di un rapporto LOCALE: può nascondere compressione e stiramento che si COMPENSANO»*. Quindi **`p10`, mediana, `p90`** e la **divisione per classe d'arco**, con la **stessa convenzione di `G1`-`G2`** *(`csv/_test_fork/_dove_spinge_la_gravita.py:72-78`: nodo `< 900` = **VUOTO**, `< 2391` = **MASSA seminata**, oltre = **NATO**; l'arco prende la coppia delle due classi)* — **non una convenzione nuova**. **E `A2` vale: statistiche globali SOLO nel referto, MAI nella legge.** La legge tocca `ampiezza_int`, `ampiezza_ev`, `rep`, `prob`, `_rep`, `grad_r`: **nessuna di queste legge una statistica globale.** |
| **`C`** | la **guardia** di `_r_corrente`: quante volte salta, e **quando** | `A8`. Se salta **fuori dal transitorio**, il referto **non si legge** |
| **`V8`/`V9`** | **la distribuzione di `\|dx\|/d`** — `p50`/`p90`/`p99`/`p99.9`, `max`, e la quota `> 0.5`, `> 1`, `> 2` — **separata per SALITE e DISCESE** | **decisione di Luca, 2026-09-24: SENZA UN RUN IN PIÙ.** L'involucro del bilancio avvolge già `_smorza` e vede ogni `(dx, prima)`: il numero che sceglie fra `piana` e `tanh` *(scheda ⑪)* **si raccoglie qui dentro**. Criterio committato **prima** in `2c4da47` |

**Riferimento: `csv/_test_fork/_cura1_corto`** — stessa configurazione, `CURA 1` accesa, questo
flag **spento**. **Differisce per UN interruttore.**

---

## 10. IL CODICE, COM'È STATO SCRITTO — *2026-09-24, blob `b881db89`*

### 10.1 QUATTRO METODI NUOVI, e ciascuno esiste per non avere DUE leggi

| metodo | cosa fa | perché è un metodo e non una riga |
|---|---|---|
| **`_cs_arco_da_nodo`** | media **armonica** del `cs` sui due estremi | **ESTRATTA da `step()` `:4791` senza cambiarne una virgola.** `mitosi()` ne ha bisogno per `tau_arco = d/cs_arco`; **duplicarla avrebbe significato due leggi che possono divergere** — lo stesso argomento del docstring di `_tempo_luce_nodo`. **`T4` prova che l'estrazione non ha cambiato un bit** |
| **`_r_nodo_mitosi`** | l'orologio **per nodo**, per il gradiente | guardia **contata `A8`**: invocazioni, salti, **forma** al fallimento, **quando** |
| **`_fattore_tempo_arco`** | `dt_e/DT` per arco | **LETTO da `_dt_e_ultimo`, NON ricalcolato.** Ricalcolarlo sarebbe **una seconda formula per lo stesso tempo** |
| **`_tau_arco_causale`** | `d / cs_arco`, e **ha le unità di un TEMPO** | `[LAM]/[LAM/DT] = [DT]`. **NESSUN CLAMP**, ed è una decisione di Luca: `d ≥ LAM` è una **LEGGE** *(`E4-LAM`)* e `cs > 0` è **derivato** |

### 10.2 LE QUATTRO MODIFICHE GATED, tutte dentro `mitosi()`

```
:5297   grad_tau   da |tw| per nodo  ->  da r per nodo  (_r_nodo_mitosi)
:5370   ampiezza   * 1/tau_pp        ->  * dt_e/DT      (_fattore_tempo_arco)
        prob       clip(resp,0,1)    ->  1 - exp(-max(resp,0))     [Poisson]
:5387   rep        bersaglio da resp ->  da resp_int (SENZA il tempo)
:5438   _rep       Eulero con tau_pp ->  forma ESATTA con tau_arco  [S12]
```

> **⚠ E IL FATTORE DI TEMPO ENTRA UNA VOLTA SOLA, non due — è il rilievo di Luca del `e11602d`.**
> `rep` è il **BERSAGLIO di un rilassamento**, cioè un **EQUILIBRIO**: non può dipendere dalla
> **durata** del passo, senno' la stessa condizione fisica darebbe un equilibrio diverso a
> seconda di quanto batte l'orologio locale. `prob` è una **probabilità NEL passo**, cioè un
> **conteggio**: **deve** dipenderne. Per questo esistono `ampiezza_int` *(senza tempo)* e
> `ampiezza` *(con)*, e il bersaglio legge la prima.

### 10.2-bis ⚠ **I QUATTRO METODI SONO LEGGI, E `REG-R` LO HA PRETESO**

Il primo tentativo di commit è stato **RIFIUTATO**: *«queste leggi non hanno una scheda»*, e
le elencava tutte e quattro. **Aveva ragione, e non era una formalità** — sono quattro
relazioni fisiche *(una media d'arco, un orologio per nodo, un fattore di tempo, un ritardo
causale)*, e senza scheda si curerebbe alla cieca. **Sono entrate nel marcatore di questa
scheda**, che è dove la loro legge è scritta.

> **⚠ E UNA TENSIONE VA DICHIARATA, non nascosta: `_cs_arco_da_nodo` NON È SOLO DI QUESTA
> SCHEDA.** La chiama anche `step()`, che appartiene alla ⑥, e la relazione vive in `step()`
> **da prima della cura**. Sta qui perché **qui è stata scritta la sua derivazione**
> *(armonica perché è un collo di bottiglia; aritmetica per il tempo, armonica per la
> velocità)*. **È lo stesso caso della ⑥ che rivendica `step` «in via provvisoria», con lo
> stesso rimedio: quando `step` avrà la sua scheda, il marcatore si divide.** Finché non
> succede, **una modifica a questa media obbliga a toccare la ⑨ e non la ⑥**, e chi la cerca
> partendo da `step()` deve passare dal rimando che la ⑥ ora porta.

### 10.2-ter ⚠ **IL CLIP HA DUE LATI, E NE CONTAVO UNO SOLO** — *rilievo di Luca, 2026-09-24*

`np.clip(resp, 0, 1)` taglia **in alto** *(contato: `_tum_clip_prob` = **`0` su `63 148 047`**)*
**e in basso**. **Il lato basso morde ogni volta che `resp <= 0`, cioè su TUTTO il regime
repulsivo** — e dire *«il clip non morde»* con in mano solo il lato alto **sarebbe falso**.

Aggiunto **`_tum_clip0_prob`**, incondizionato come gli altri.

> **E dice una cosa precisa sulla cura: la forma di Poisson `1 − exp(−max(resp, 0))` CONSERVA il
> taglio in basso.** È il taglio **in alto** che sparisce. Quindi `_tum_clip0_prob` misura
> **quanto è grande il pezzo di dominio su cui le due forme COINCIDONO ESATTAMENTE** *(entrambe
> danno `0`)*. **Più è grande, più la cura di `:5244` è formale.**

### 10.3 I CONTATORI `A8`, e girano **ANCHE A FLAG SPENTO**

`_tum_clip_prob*`, `_tum_clip_rep*`, `_tum_eulero_gt1`/`_tot` sono **fuori dal gate**, di
proposito: così **il «prima» del criterio `K` arriva dal giro di byte-inerzia del sigillo,
senza un run in più**. Sono l'unica ragione per cui `T4` riporta dei campi *«non confrontati»*
invece di zero.

---

<!-- SCHEDA nome=nascita-archi funzioni=_allaccia,_nasce,semina,_semina_lam,_celle_vive flag=SEMINA_LAM,NASCITA_LAM,SCALA_MIN,SCALA_MIN_PASSO,LAM -->

### ⛔ **AGGIORNAMENTO del 2026-10-06 — `_allaccia` DAVA UN CALCIO DI TORSIONE A TUTTA LA
### SCENA** *(cura di `TORS-W8-AVVOLGIMENTO`)*

`_allaccia` metteva `tw = 0` **e `twp = 0`** sugli archi nuovi. ### ⛔ **E `twp = 0` non e'
<<nessuna storia>>: e' <<fase precedente ZERO>>**, quindi al primo passo la spinta valeva
`dph + twist_dip − 0`, cioe' ### **TUTTA la differenza di fase dell'arco piu' il suo dipolo
diventava torsione.**

| al passo `1`, misurato su `f7237563` *(`eebe24f`)* | |
|---|--:|
| `|tw|` in **ingresso** *(archi appena seminati)* | `0.0000` |
| `|dph|` mediano | `2.8971` |
| ### **`|spinta|` mediana** | ### **`3.0950`** |
| ### **`|spinta|` MASSIMA** | ### **`9.4248` = `3π` ESATTO** |
| e al passo `2`, `|tw|` in ingresso mediano | ### **`3.0950`** |

### ⛔ **IL MASSIMO SATURAVA IL LIMITE TEORICO** *(`|dph + twist_dip| <= 3π`)*, e il tempo di
scarica e' `τ_tw/dt_e` ≈ **`309` passi**: in `150` passi la rete conservava il **`61.5 %`**
del calcio. ### **`3.0950 × 0.6151` = `1.9037`, contro il `|tw|` mediano misurato `2.1105` al
passo `140`.** ### ➜ **LA TORSIONE DELLA RETE ERA QUASI TUTTA IL CALCIO DI NASCITA.**

### ✔ **LA CURA:** `_allaccia` scrive ### **`twp_dip = nan`**, il marcatore di arco nuovo, e il
primo passo di torsione da' ### **spinta ZERO.** ### **Misurato sul giro minimo: al passo `1`
`|tw|` mediano E massimo valgono `0.000000`.**

### ⚠ **E `twp = 0` RESTA**, perche' col marcatore ### **non viene piu' letto** dal ramo `4π`
e il ramo non-`4π` lo usa com'e' sempre stato. ### **Togliere una riga che non fa piu' danno
non e' una cura: e' un ritocco, e andrebbe in un commit suo.**

# ⑫ LA NASCITA DEGLI ARCHI — **la cura della semina** *(`D38`, decisione `D-b` di Luca)*

> **Decisione di Luca, 2026-09-24:** *«Non deve nascere un arco sotto `LAM`. Il troncone
> `_nasce` resta come PRESIDIO.»*
> **NESSUN CODICE in questa scheda.** Difetto e criteri **prima**, cura **dopo**.
>
> ## ❌ **`NASCITA_LAM` È RITIRATA — decisione di Luca, 2026-09-24**
>
> **La prima cura che avevo proposto era `keep &= (dd >= LAM)`: FILTRARE GLI ARCHI.**
> **È ritirata**, e il motivo è **il criterio che avevo scritto io stesso** nel par.2 di questa
> scheda: *«se la mediana della distanza al primo vicino è sotto `LAM`, il difetto è nelle
> POSIZIONI, e nessun aggiustamento sugli ARCHI può curarlo»*.
>
> ### **Filtrare gli archi lascia i NODI a `0.135·LAM` l'uno dall'altro.** Toglie il sintomo
> ### *(`d < LAM`)* e lascia la violazione *(`|pos_i − pos_j| < LAM`)*. **Con `A13` non è
> ### nemmeno una mezza cura: è la cura di un'altra cosa.**
>
> **NON si cancella** *(par.10: il codice di una legge esclusa non si cancella mai)*: resta qui,
> **come il perché esiste `SEMINA_LAM`.**

## 1. IL DIFETTO — **`D38`**

`_allaccia` prende la lunghezza dell'arco dal `cKDTree`:

```python
M = Tn.sparse_distance_matrix(T, rc, output_type="coo_matrix")
a, b, dd = M.row + base, M.col, M.data          # dd = la distanza EUCLIDEA VERA fra `pos`
...
dd = self._nasce(dd)                            # [SCALA_MIN] il troncone parte da LAM
```

e `_nasce` *(`:3845-3853`)* è:

```python
if not (SCALA_MIN or SCALA_MIN_PASSO):
    return v
return np.maximum(v, LAM)
```

> ### ❗ **LA LEGGE `d >= LAM` È VERIFICATA SEMPRE (`E4-LAM`) MA FATTA RISPETTARE ALLA NASCITA
> ### DA UN'OPZIONE.** È **lo schema che `E4-LAM` ha tolto al CONTROLLO e che è rimasto
> ### all'ESECUZIONE.** Coi **default del sorgente** la legge è **violata al passo zero**.

## 2. LA CAUSA — **non è negli ARCHI: è nelle POSIZIONI**

*(`csv/_test_fork/_geometria_semina.py`, blob `49fc54d2`, passo ZERO, `--scala-min-passo=off`
per avere la `d` GREZZA — col ramo acceso la domanda risponderebbe sempre zero.)*

**Distanza al PRIMO VICINO di ogni nodo** *(la più corta che quel nodo può avere)*:

```
n=2391  LAM=0.800000  R_CONN=2.400000
p01=0.022187  p10=0.049003  p50=0.107721  p90=0.473825  p99=0.676303
min=0.009679  max=0.814763
sotto_LAM = 2390 su 2391 (99.96 %)   mediana/LAM = 0.134651   min/LAM = 0.012098
```

> ### ❗ **IL `99.96 %` DEI NODI HA IL PRIMO VICINO SOTTO `LAM`, e la mediana è `0.135·LAM`:
> ### LA SEMINA METTE I NODI ~`7.4` VOLTE PIÙ FITTI DELLA LUNGHEZZA TIPICA DEL SISTEMA.**
>
> **Quindi `_nasce` non «corregge» `d`: LA SCOLLEGA DA `pos`.** Per il `42.47 %` degli archi,
> dopo il troncone **`d ≠ |pos_i − pos_j|`**. **È `D02` FATTO A MANO** — la distanza e il
> disegno divergono **per costruzione**, e divergono **al passo zero**.

**Sugli archi:** `223 380` su `525 973` — il **`42.47 %`** — nascono sotto `LAM`.

## 3. ❗ IL NUMERO CHE RENDE LA CURA POSSIBILE

```
SE_TAGLIASSI  archi_rimasti = 302593 su 525973 (57.53 %)
SE_TAGLIASSI  nodi_isolati  = 0 su 2391 (0.00 %)
```

> ### **NON CREARE gli archi sotto `LAM` costa il `42.47 %` degli archi e ZERO NODI ISOLATI.**
> **Era la domanda che poteva uccidere la cura, ed è misurata prima di proporla:** un nodo
> isolato **non è un nodo più semplice, è un nodo che esce dalla fisica**. **Non ce n'è
> nessuno**, perché `R_CONN = 3·LAM` lascia un anello `[LAM, 3·LAM]` pieno di vicini.

## 4. LA CURA — **`SEMINA_LAM`, spenta di default. UN INTERRUTTORE SOLO.**

**`A13` dice che sotto `LAM` non esiste niente, nemmeno una distanza fra nodi.** Quindi la cura
non sta sugli archi: **sta dove i nodi vengono messi.**

```
in `semina()`:  ogni nodo nuovo a distanza >= LAM da QUALUNQUE nodo GIA' PRESENTE
                -- della stessa massa, delle altre masse, del VUOTO DI FONDO --
                con semina casuale e SCARTO (RSA, random sequential adsorption)
```

**E il vuoto di fondo segue la stessa regola:** *non ci sono nodi di seconda classe.*

> ### PERCHÉ È DERIVATA E NON SCELTA *(par.3, zero manopole)*
> **`LAM` c'è già** ed è l'assioma; **`R_CONN = 3·LAM` c'è già**. **La cura non introduce
> nessun numero.** L'`RSA` non ha parametri: propone un punto, lo accetta se rispetta `LAM`,
> altrimenti lo scarta.

### ❗ E SE `n` NON ENTRA NEL RAGGIO, **LA SEMINA RIFIUTA** *(`A9`)*

> **NIENTE RIDUZIONI SILENZIOSE.** Se in quel raggio non stanno `n` nodi a distanza `LAM`, la
> semina **si ferma** con un messaggio che **nomina `n`, il raggio e il massimo possibile**.
> **È la ragione per cui questo è un presidio e non una nota:** una semina che «fa del suo
> meglio» consegnerebbe **una massa più piccola di quella chiesta, in silenzio**, e ogni
> misura successiva sarebbe su una taglia diversa da quella scritta nel comando.
>
> **La SCENA calcola il raggio da `n`** *(decisione di Luca)*: è la scena a sapere quanto spazio
> serve, non la semina a stringersi.

### E `_nasce` RESTA — **come PRESIDIO, e ora agisce SEMPRE**

`D38` *(il troncone sotto flag)* **si cura qui**: il presidio **non è più gated**.
Dopo la cura **non deve scattare mai**, e **`_g_sm_nascite` è la sua misura**: se sale, un arco
è nato sotto `LAM` **da un'altra strada**.

> **⚠ E LE ALTRE STRADE ESISTONO:** la **mitosi** crea nodi vicino al genitore, e questa scheda
> **non la copre**. **`S4` lo RILEVEREBBE al passo zero, non nei passi dopo.** → in coda.

## 5. I CRITERI DELLA PROVA, **fissati QUI, PRIMA DEL CODICE** *(mandato di Luca)*

| | criterio | origine |
|---|---|---|
| **`S1`** | **flag SPENTO = byte-identico**: **firma dei byte** su tutti i campi, **un processo per braccio** | par.2.1 · `STANDARD 1` · `STANDARD 2` |
| **`S2`** | **passo ZERO: `min` distanza fra POSIZIONI `>= LAM`** *(`cKDTree`, `k=2`)* | ❗ **è `A13` misurato direttamente**, e **è il criterio che `NASCITA_LAM` non poteva soddisfare** |
| **`S3`** | **passo ZERO: `sum(d < LAM) == 0` E `sum(d == LAM) == 0`** | **i due INSIEME**: il primo da solo lo darebbe anche `_nasce`. **Lo zero sul secondo distingue «non c'è bisogno di troncare» da «troncato»** |
| **`S4`** | **`_g_sm_nascite == 0`** al passo zero | il presidio **non deve scattare**. **Rileva solo il passo zero**, non i passi dopo |
| **`S5`** | **nodi isolati `== 0`** | un nodo isolato **non è un nodo più semplice: è un nodo che esce dalla fisica** |
| **`S6`** | **`d == |pos_i − pos_j|` per OGNI arco al passo zero** | ❗ dice se la cura ha curato **`D02` a questo sito**: oggi diverge sul `42.47 %` |
| **`S7`** | **giro corto di 120 passi**: la mitosi **viva**, il **bilancio di `d0` CHIUDE** | `E1a` e `B`, gli stessi di `CURA 1` e `CURA 2`. ❗ **è il solo che può BOCCIARE la cura** |

### ✅ **LA STRADA è `(ii)`: MASSA = REGIONE A FASE COERENTE NEL VUOTO** *(Luca, 2026-09-25)*

```
un vuoto UNICO seminato con SEMINA_LAM (saturazione esatta) su una palla che
contiene le tre regioni.
LE MASSE NON AGGIUNGONO NODI: sono i nodi del vuoto DENTRO TRE SFERE, a cui si
assegna la STESSA FASE (fase della scena + il rumore che `semina()` usa gia').
Fuori: fasi casuali, come oggi. Coorti registrate come oggi (`massa_k`).
```

> ### **ZERO NUMERI NUOVI, e per una ragione che vale più dell'economia:** la materia **era
> ### già** uno **STATO del nodo** nel codice — `I > Λ`, *«sotto `Λ` sei vuoto, sopra sei
> ### materia»* *(voce `M1` della coda)*. **La strada `(ii)` non aggiunge un'ontologia: rende
> ### la SCENA coerente con quella che il simulatore ha già.**
>
> **E risolve il vincolo che uccideva `(i)`:** con `A13` una massa **non può essere più densa
> del vuoto** — stessa distanza minima per tutti — quindi *«aggiungere nodi»* dentro un vuoto
> saturo **è impossibile per costruzione**. Se la massa non aggiunge nodi, il problema non
> esiste.

### LA GEOMETRIA, e cosa è SCELTO

```
tre regioni su un cerchio di raggio `sep` -> distanza fra i CENTRI = sep*sqrt(3) (corda 120')
intervallo fra i BORDI = sep*sqrt(3) - 2*r      ** = R_CONN e' una SCELTA di Luca **
raggio del VUOTO = sep + r + R_CONN            <- il minimo che contiene le tre regioni
                                                  PIU' un guscio di R_CONN
```

**I numeri si calcolano con la semina VERA** *(`csv/_test_fork/_scene_coerenti.py`)*, **non si
stimano**, e si committano **prima** della misura.

### I DUE CRITERI IN PIÙ — **`S9` e `S10`**, fissati PRIMA *(Luca, 2026-09-25)*

| | criterio | perché |
|---|---|---|
| **`S9`** | **al passo ZERO: intensità media DENTRO le regioni / quella del vuoto, `> 1`** — e **si riporta il valore** | ❗ **È IL CRITERIO CHE DECIDE SE LA STRADA `(ii)` ESISTE.** Se le regioni non sono **materia per il codice**, allora «massa = fase coerente» è una parola, non una scena. **E non basta «esiste un effetto»: il valore va detto**, perché `1.01` e `10` sono due fisiche diverse |
| **`S10`** | **le regioni restano coerenti**: frazione di nodi della coorte con `I > Λ`, ai passi `0`, `30`, `60`, `120` | ❗ **SE CROLLA È UN RISULTATO, NON UN DIFETTO** *(Luca)*: direbbe che **la coerenza da sola non tiene la materia**. **Reperto e stop.** È il solo criterio di questa scheda che può dire qualcosa sulla FISICA invece che sul codice |

> **⚠ E `S10` HA UN NULLO CHE VA DETTO ORA** *(presidio del valore sotto ipotesi nulla)*:
> **fuori dalle regioni le fasi sono casuali**, quindi la frazione con `I > Λ` nel VUOTO non è
> zero — `Λ` è la **media** di `I`, quindi per costruzione **circa metà dei nodi** ci sta
> sopra. **Il numero che conta è il CONTRASTO fra coorte e vuoto, non il valore assoluto**, e
> il referto deve riportare **entrambi**.

### ✅ **LA SCENA `(a)` SI CHIAMA «STESSO RAGGIO», NON «STESSA MATERIA»** *(Luca, 2026-09-25)*

**Si tiene il RAGGIO `4.0964`**, cioe' **`~411` nodi per regione**, non `497`.

> ### **E LA RAGIONE È PIÙ FORTE DELLA SCELTA: i `497` per massa di `CURA 2` ERANO SOTTO LA
> ### SCALA DI PLANCK.** Stavano in un raggio `0.7 = 0.875·LAM`, dove ci stanno **`5`** nodi
> *(rapporto `104`)*. **Non c'è una «stessa materia» da conservare: quella materia non
> esisteva.** Conservare `497` sarebbe **portare avanti un numero nato in un regime che `A13`
> ha dichiarato inesistente.**
>
> **Il nome cambia perche' il nome era una PROMESSA sbagliata**, ed è lo stesso difetto dei
> commenti scaduti: *«stessa materia»* avrebbe fatto leggere il confronto come se una
> grandezza fosse tenuta fissa, mentre quella grandezza **non ha un valore precedente valido**.

**La scena `(b)` resta com'è:** `sep = 4.0`, `r_regione = 2.2641`, `~70` nodi per regione.

### ❗ `P-GONFIA` — **IL RIFERIMENTO CAMBIA, E VA DICHIARATO** *(Luca, 2026-09-25)*

**Il confronto con `CURA 2` è fra SCENE DIVERSE e non attribuisce niente alla semina.**
*(Scena diversa, `n` diverso, raggio diverso, `QUOTA` diversa: qualunque differenza di `d0`
potrebbe venire da lì.)*

```
BRACCIO DI CONTROLLO DI `P-GONFIA`:
  la STESSA scena (ii) -- stesso raggio del vuoto, stesso `n`, stesse regioni,
  stesso seme -- con `SEMINA_LAM` **SPENTA**.
  UNICA DIFFERENZA: la distanza minima.
```

> **La soglia resta «MENO DELLA METÀ»**, ma **applicata a QUESTO confronto**.
> **Il confronto con `CURA 2` resta nel referto come riferimento DI UN'ALTRA SCENA**, e va
> letto così: dice **dove siamo**, non **cosa ha fatto la semina**.

### ❗ `S10` — **TRE PRECISAZIONI PRIMA DELLA MISURA** *(Luca, 2026-09-25)*

1. **BRACCIO DI CONTROLLO:** la stessa scena, **stesso seme**, con **fasi CASUALI anche dentro
   le tre regioni**. **`S10` si legge come CONTRASTO fra la coorte coerente e questo controllo,
   non in assoluto.** *(Senza, il `~50 %` che `Λ` dà per costruzione si leggerebbe come mezzo
   successo.)*
2. **PROFILO PER GUSCI**, contati **in ARCHI dal nucleo della regione** *(non da `pos`)*:
   frazione con `I > Λ` ai passi `0`, `30`, `60`, `120`.
   **Distingue l'EROSIONE DAL BORDO dallo SFASAMENTO GLOBALE** — due esiti che un numero unico
   confonderebbe.
3. **PREVISIONE, scritta prima:** la scena **`(b)` perde coerenza PRIMA della `(a)`**.
   `r = 2.26 < R_CONN = 2.4`, quindi **nessun nodo della regione `(b)` ha tutti i vicini
   dentro**; in `(a)` *(`r = 4.10`)* il nucleo interno di raggio `~1.70` **ce li ha tutti**.
   **Se accade il contrario, va spiegato.**

> ### ⛔ **E SE LA COERENZA CROLLA: REPERTO E STOP. NESSUNA LEGGE NUOVA PER TENERLA** *(Luca)*.
> **La diagnosi si fa DOPO, spegnendo UNA legge alla volta** — dispersione delle frequenze,
> calci di fase della mitosi, torsione.
> **È `A12` applicato al contrario:** una misura che fallisce **non autorizza una legge**, e
> aggiungere un meccanismo per salvare un risultato è il modo in cui una teoria smette di
> poter essere smentita.

### ❗ LE PREVISIONI ANALITICHE, **committate PRIMA del giro** *(punto 4 del mandato)*

| | grandezza | `CURA 2` | scena `(ii)` | `×` |
|---|---|--:|--:|--:|
| **`P1`** | somma dei pesi per nodo | `~50` | `~9` | `0.18` |
| **`P2`** | contrasto `I_massa / I_vuoto` | `~13` | `~27` | `2.1` |
| **`P3`** | `Λ` | `~140` | `~5` | `0.036` |
| **`P3b`** | ampiezza dello scuotimento | — | **`~5×` più bassa** | `0.2` |
| **`P4`** | `cs_floor` dentro le masse | `~0.9` | `~0.55` | `0.61` |
| **`P5`** | `lambda_nodi` | — | **quasi COSTANTE, `0.74`-`0.76 LAM` ovunque** | — |

**LE ASSUNZIONI, dichiarate:** `SCALA_AMP = 1` · pesi `exp(-d/LAM)` · **nessuna correlazione
`RSA`**.

### ❌❌ **`P2` È FALLITA DI `×4`** — registrata così da Luca, **non come «da spiegare»** *(2026-09-25)*

**Misurato a campo MATURO** *(`CURA 4` ON, sigillo `A4`)*:

| | previsto | misurato | |
|---|--:|--:|---|
| **contrasto `I_massa / I_vuoto`** | `27` | **`6.79`** | **`×0.25`: FALLITA di `×4`** |
| `I_vuoto` | `1.42` | **`1.69`** | **stimato BENE** |
| `I_massa` | `≈38` *(implicito)* | **`11.45`** | **SOVRASTIMATO di `~×3.3`** |
| **`P3` (`Lam`)** | `5` | **`2.16`** | `×0.43`: **dentro il fattore `2`, TIENE** |

> ### **LA CAUSA, ed è di Luca, non mia:** *«ho sovrastimato `I_massa` assumendo NODI INTERNI;
> ### le regioni sono QUASI SOLO BORDO.»*
>
> **E il dato che lo conferma era già nel referto del passo zero, nel PROFILO PER GUSCI:**
> con `1` nodo al centro e `~80` al primo guscio su `~411` totali, **quasi tutta la regione sta
> a distanza `2` dal nucleo** — `3`-`4` gusci in `(a)`, `2`-`3` in `(b)`.
> **Un nodo di bordo ha meno vicini coerenti, quindi meno interferenza costruttiva.**
>
> ### **IL RISULTATO FISICO, detto come va detto: le masse sono `~7` volte più luminose del
> ### vuoto. SI DISTINGUONO, MA NON DI MOLTO.**
> **Non è «da spiegare»: è spiegato, e la previsione è sbagliata di un fattore `4`.**

**⚠ E LA PROVENIENZA RESTA QUELLA DICHIARATA:** queste previsioni vengono **dal mandato**, non le
ho derivate io. **Ma la CAUSA del fallimento è un'assunzione geometrica**, e quell'assunzione
— *«nodi interni»* — **era falsificabile dal profilo per gusci, che avevo già misurato**.

> **⚠ E UNA DICHIARAZIONE DI PROVENIENZA, perche' conta per come si legge un errore:
> QUESTE PREVISIONI VENGONO DAL MANDATO, NON LE HO DERIVATE IO.** Le committo come sono, con le
> loro assunzioni, **e le verifico al passo zero**. Se sbagliassi a rivendicarle come mie, un
> loro fallimento non direbbe piu' se è sbagliata l'assunzione o il conto.
>
> **CRITERIO: se una previsione sbaglia di più di un FATTORE 2, va spiegato perche'** — *o
> l'assunzione è falsa, o la legge fa altro da ciò che dice* *(Luca)*. **E `P5` è la piu'
> interessante**: se `lambda_nodi` è quasi costante, **la legge di schermatura è di fatto
> SPENTA dalla soglia irraggiungibile** — cioè lo stesso difetto di `massa_critica_collasso`,
> visto da un'altra legge.

### ⚠ `U2` È ATTIVA IN ENTRAMBI I BRACCI DI `P-GONFIA` E FABBRICA LUNGHEZZA *(Luca, 2026-09-25)*

**Non cambia il criterio**, e va dichiarata come tale: serve a **leggere quanto del gonfiamento
viene dalla MITOSI** invece che dalla semina.

> **Il problema è che `U2` agisce in ENTRAMBI i bracci, e probabilmente PIÙ nel controllo**,
> dove `SEMINA_LAM` è spenta e **quasi tutti gli archi sono corti**. **Il confronto di
> `P-GONFIA` mescola quindi due effetti**, e senza contarli il suo esito — passi o fallisca —
> non si attribuisce.

**NEL REFERTO, PER OGNI BRACCIO:**

| | cosa | quando |
|---|---|---|
| **`U2a`** | **la LUNGHEZZA FABBRICATA da `_nasce`**, `sum(LAM - v)` sugli archi troncati, **SEPARATA per grandezza (`d`, `d0`) e per sito (`semina`, `mitosi`, `schwinger`)** e contata sugli **ARCHI VERI**. **Nel confronto con la crescita di `d0` entra SOLO `_sm_lund0_*`** | cumulativa, e **al netto del passo zero** |
| **`U2b`** | quanti archi sono stati **troncati**, e su quanti visti — **stessa separazione** | idem |
| **`U2c`** | **frazione di archi sotto `2 LAM`** | ai passi `0` e `120` |

### ❗ E IL CONTATORE CHE LUCA CITAVA NON MISURAVA QUESTO — rilievo mio, verificato dal codice

**`_g_sm_nascite` CONTA LE INVOCAZIONI di `_nasce`, non i troncamenti:**

```python
self._g_sm_nascite = getattr(self, '_g_sm_nascite', 0) + 1
return np.maximum(v, LAM)
```

**Una chiamata che non tronca nulla lo fa salire ugualmente.** Quindi *«quante volte `_nasce` ha
troncato un figlio della mitosi»* **non era leggibile**: il numero non c'era.

> **Tre contatori nuovi, tutti BYTE-INERTI** *(si somma, non si cambia)*: `_sm_visti`,
> `_sm_troncati`, **`_sm_lunghezza`**.
> ### **E `_sm_lunghezza` è quello che conta: `sum(LAM - d)` è il contributo DIRETTO di `_nasce`
> ### al gonfiamento di `d0`, NELLE STESSE UNITÀ DEL BILANCIO.**
> Così `P-GONFIA` non dice solo *«quanto è cresciuto»*: dice **quanta di quella crescita è
> lunghezza FABBRICATA alla nascita**, e quanto resta da spiegare.

### ❌❌ `U2` ERA SBAGLIATA: **UN CONTATORE SOLO, E MESCOLAVA `d` CON `d0`** *(rilievo di Luca, 2026-09-25)*

**Cio' che avevo scritto ieri:** *«`_sm_lunghezza` è il contributo DIRETTO di `_nasce` al
gonfiamento di `d0`, NELLE STESSE UNITÀ DEL BILANCIO»*. **Non lo era**, e la ragione è nel
codice che avevo letto io stesso per scrivere la riga.

> ### **`_nasce` è chiamata in QUATTRO siti, e la MOLTEPLICITÀ degli archi veri è DIVERSA in ognuno.**

| sito | chiamata | archi veri di `d` | archi veri di `d0` | dal codice |
|---|---|--:|--:|---|
| **`semina`** | `_allaccia`: `dd` | `1` | `1` | `d = concat([d, dd])` **e** `d0 = concat([d0, dd])` — **UNA chiamata vale per DUE grandezze** |
| **`mitosi`** | `dh` | **`2`** | `0` | `d = concat([d[keep], dh, dh])` — **`dh` ha `len(sel)` voci ma diventa DUE archi per voce** |
| **`mitosi`** | `d0new` | `0` | `1` | `d0new` è **già** `concat([d0h, d0h])`: i due figli ci sono già |
| **`schwinger`** | `dd` | **`2`** | **`2`** | `concat([d, dd, dd])` **e** `concat([d0, dd, dd])` |

**TRE DIFETTI IN UNO, e il primo distrugge proprio la ragione per cui il contatore esisteva:**

1. **la somma MESCOLAVA `d` e `d0`** — quindi **non era «nelle unità del bilancio di `d0`»**,
   che era l'unica cosa che le dava senso in `P-GONFIA`;
2. **il sito `dh` era SOTTOCONTATO DI `2`**: contava le voci di `dh`, non gli archi che ne nascono;
3. **`_sm_visti` contava le VOCI**, non gli archi, con lo stesso errore nel denominatore.

**LA CORREZIONE:** `_nasce(v, dove, md, md0)`. Contatori `_sm_{lun,tr,vis}{d,d0}_{sito}`,
**separati per grandezza e per sito, sugli ARCHI VERI**.

> ### **Solo `_sm_lund0_*` entra nel confronto con la crescita di `d0` in `P-GONFIA`.**

**⚠ E LO SCHWINGER È UN QUARTO SITO, NON NEI TRE DEL RILIEVO:** è `×2` su **entrambe** le
grandezze. Lo segnalo perché cambia il conto, e perché la sua lunghezza viene da **`pos`, non da
`d`** — cioè è anche la voce **`A3`** della coda.

### ✅ IL SIGILLO: `csv/_seal_fork/_sigillo_u2_contatori.py`

**Il caso a risposta nota, come chiesto da Luca:** **una MITOSI VERA** con **un solo arco a
`1.2 LAM`** — `dh = 0.6 LAM < LAM`, **entrambi i figli troncati**.

```
ATTESO PER COSTRUZIONE:
  _sm_trd_mitosi   = 2                       (DUE archi di `d`, non uno)
  _sm_trd0_mitosi  = 2
  _sm_lund_mitosi  = 2 * (LAM - 0.6 LAM)     = 0.8 LAM
  _sm_lund0_mitosi = 2 * (LAM - 0.6 LAM)     = 0.8 LAM
```

**`U2-6` È IL CASO CHE DEVE FALLIRE** *(`P1-sexies`, ed è il criterio più importante)*: la
formula VECCHIA, **sullo stesso evento**, dava `0.4 LAM` sul lato `d` e una somma mescolata di
`1.2 LAM`, **che non è in nessuna delle due unità**. Il criterio applicato a quella **deve dare
FAIL**: se passasse, non discriminerebbe la cura dal difetto.

**`U2-5` è MODEL-FREE:** non confronta col mio conto, **legge `d` e `d0` e conta gli archi che
nell'ARRAY stanno a `LAM`**. **`U2-8` è la BYTE-IDENTITÀ** al codice di `HEAD`, col suo controllo
positivo *(un caso diverso DEVE risultare diverso, sennò «identico» è un confronto cieco)*.

**COSA IL SIGILLO NON DICE, dichiarato nel referto:** **il sito `schwinger` NON è collaudato**
— quel ramo non è stato fatto scattare, e la sua molteplicità è **letta dal codice, non
misurata**.

### ❗ IL COSTO SI MISURA DAGLI **ARCHI**, non dai nodi *(punto 5)*

**Al passo ZERO si conta il numero di ARCHI di entrambe le scene, PRIMA di stimare i tempi.**
**Stima da verificare:** `(a)` `~500k` archi *(simile a `CURA 2`)*, `(b)` `~150k`.

> **E il mio avviso di costo di ieri era sbagliato nella grandezza guardata:** avevo detto
> *«il vuoto di `A` ha `5.4×` i nodi, quindi costera' molto di piu'»*. **Il costo dipende dagli
> ARCHI**, e con `A13` i nodi sono **piu' distanti**, quindi **meno connessi**: `5.4×` i nodi
> **non significa `5.4×` gli archi**. **Si misura, non si stima.**

### ❗ `P-GONFIA` — **LA PREVISIONE, CON LA SUA SOGLIA NUMERICA FISSATA ORA**

**La previsione di Luca:** *la crescita della mediana di `d0` nei 120 passi **CALA NETTAMENTE**
rispetto al giro di `CURA 2`.*

**Il riferimento, LETTO dal bilancio di `CURA 2`** *(`csv/_test_fork/_cura2_corto/BILANCIO_d0.txt`,
colonna `med vivi`)*:

```
med vivi:  passo 8 -> 0.938570      passo 120 -> 1.382321
CRESCITA CURA 2 = +47.2795 %
```

> ### **SOGLIA: la crescita deve essere `< +23.64 %`, cioè MENO DELLA METÀ.**
>
> **⚠ E «metà» È UNA SCELTA, non una derivazione — lo dico invece di farla passare per un
> conto.** Non so derivare quanto debba calare: so che il freno agisce **sugli archi al muro**,
> e quegli archi **non esisteranno più**. **Un fattore 2 è la soglia più grossolana che possa
> ancora distinguere «cala nettamente» da «cala un po'»**, ed è grossolana **di proposito**:
> il riferimento è **UN SEME SOLO**, la dispersione fra semi **non è misurata** *(`P3`)*, e una
> soglia fine su un riferimento senza barra sarebbe finta precisione.
>
> ### **SE NON CALA → IL MOTORE È IL FRENO, e il freno-legge va in coda** *(decisione di Luca)*.
> **È una previsione che può FALLIRE e indirizzare il lavoro**, non una che conferma comunque.

> ### ⚠ LE ALTRE PREVISIONI, scritte PRIMA
> **NON sarà byte-inerte e cambierà TUTTO**: `n`, la densità, il bilancio, la mitosi.
> **Mi aspetto numeri diversi, non numeri uguali.**
>
> **⚠ E DUE INCOGNITE, dichiarate invece che nascoste:**
> 1. **quanti nodi entreranno davvero.** Con distanza minima `LAM` la densità massima è fissata
>    dalla geometria: la semina **potrebbe RIFIUTARE** le taglie di oggi. **Se rifiuta, non è un
>    difetto della cura: è `A13` che dice che quella taglia non esiste.**
> 2. **la coesione.** Il grafo sarà molto più rado e `R_CONN = 3·LAM` resta invariato.
>    **Non l'ho misurato, e `S7` è dove si vedrà.**

## 5-bis. ❗ **IL RIFIUTO HA GIÀ PARLATO, AL PRIMO GIRO DEL FLAG** *(2026-09-24, blob `ba9054ce`)*

**Non era una prova: stavo solo verificando che il flag arrivasse.** `--semina-lam` da solo, e
la *cura del mondo* ricostruisce il vuoto di fondo dopo i flag:

```
[semina-lam] RIFIUTO DI SEMINARE: non ci stanno 900 nodi a distanza >= LAM
  chiesti      n = 900
  raggio       r = 4.000000   (= 5.000 LAM)
  LAM            = 0.800000
  collocati      = 352   <- il MASSIMO RAGGIUNTO, misurato adesso
  stima RSA      = 384   <- frazione di impacchettamento ~0.384 (STIMA di letteratura)
  nodi gia' presenti = 0
```

> ### **IL VUOTO DI FONDO DI DEFAULT — `900` NODI IN RAGGIO `4.0` — NON ENTRA: NE STANNO `352`.**
>
> **E' la prima incognita che avevo dichiarato, e si è materializzata subito.** **Non è un
> difetto della cura: è `A13` che dice che quella taglia non esiste.** Prima di oggi il sistema
> la otteneva **sovrapponendo i nodi sotto la scala di Planck.**
>
> **E il RIFIUTO ha fatto il suo mestiere al primo colpo:** senza di lui la semina avrebbe
> consegnato **`352` nodi invece di `900`, in silenzio**, e ogni misura successiva sarebbe stata
> su una taglia diversa da quella scritta nel comando *(`A9`)*.

### ⚠⚠ **IL LIMITE DEL RIFIUTO, e va letto PRIMA di credergli** *(rilievo di Luca, 2026-09-24)*

`_semina_lam` si arrende quando **un lotto di `n` proposte non accetta nessun punto**, e **il
lotto ha la taglia CHIESTA**. Da qui tre conseguenze, e nessuna è innocua:

1. **`collocati` DIPENDE DA `n`.** Più se ne chiedono, più tentativi si fanno, più se ne
   piazzano. **MISURATO a `r = 4.0`, stesso seme:**
   ```
   n=900 -> 372 | n=2000 -> 371 | n=4000 -> 399 | n=8000 -> 411 | n=16000 -> 398 | n=32000 -> 418
   ```
   **`+12 %` su un intervallo di richieste di `35x`.** **Non è «il massimo che ci sta»: è un
   LIMITE INFERIORE che cresce con la richiesta.**
2. **CON `n` PICCOLO IL RIFIUTO PUÒ ESSERE FALSO:** bastano `n` mancati di fila mentre c'è
   ancora posto. **È il silenzio al contrario che `A9` vuole evitare** — non nasconde una
   riduzione, ma **può negare una taglia che in realtà entrerebbe.**
3. **la bisezione del raggio poggia su un sì/no RUMOROSO**, quindi il raggio per `n` **si dà
   con la sua dispersione fra semi, mai come un numero secco.**

> **IL CRITERIO DI ARRESTO NON È STATO CAMBIATO** *(decisione di Luca: prima si misura quanto
> pesa)*. Cambiarlo introdurrebbe **un NUMERO** — la taglia del lotto — che è ciò che si voleva
> evitare *(par.3)*. **Il limite è scritto DENTRO il messaggio di rifiuto**, così chi lo legge
> lo legge lì e non qui.

**⚠ E IL `352` DEL PRIMO GIRO VA RILETTO COSÌ:** veniva da `ask = 900`. **Non era sbagliato,
ma non era «la capienza»: era la capienza A QUELLA DOMANDA.**

**LA STIMA `RSA` REGGE:** `384` previsti contro `352` misurati, **scarto `8.3 %`** — e la stima
è un **limite superiore** *(ignora il bordo)*, quindi il verso è quello giusto.

### ➤ COSA NE DISCENDE PER LA TAGLIA, e è una DECISIONE DI LUCA

`n` scala come `r³`, quindi il raggio che serve è `r = 4 · (n/352)^(1/3)`:

| `n` chiesti | raggio necessario | in `LAM` |
|--:|--:|--:|
| `352` | `4.00` | `5.0` |
| `500` | `4.50` | `5.6` |
| `900` | `5.48` | `6.8` |
| `2391` *(la scena di oggi)* | `7.60` | `9.5` |

> **Il punto di partenza che Luca ipotizzava — `~500` nodi, raggio `~4` — è a un soffio: con
> raggio `4` ne stanno `352`, e per `500` serve `4.5`.** **La taglia la sceglie Luca** *(mandato)*.

---

## 5-ter. ✅ **L'ARRESTO SI DERIVA DA `LAM`** — decisione di Luca, 2026-09-24

> **Nessuna taglia di lotto. Saturazione ESATTA.**

**IL METODO — Zhang & Torquato (2013), suddivisione di celle:**

```
celle di lato LAM/sqrt(3)  ->  diagonale = LAM  ->  AL PIU' UN NODO PER CELLA
  cella COPERTA da un nodo (distanza dal nodo allo spigolo PIU' LONTANO <= LAM)  -> MORTA
  cella fuori dalla regione                                                      -> MORTA
  cella LIBERA (nessun nodo entro LAM dal suo punto PIU' VICINO)  -> ci si puo' seminare
  cella PARZIALMENTE coperta                                      -> SI SUDDIVIDE in 8
si propone SOLO nelle celle vive; si finisce quando non ne resta NESSUNA
```

> ### **IL RIFIUTO SCATTA SOLO SE `n` SUPERA LA SATURAZIONE VERA.**
> Non più «un lotto senza accettazioni»: **non c'è più posto, e lo si sa per costruzione.**
> **Cade con lui il difetto che Luca aveva trovato:** il rifiuto **non può più essere falso.**

### ⚠⚠ E QUI DEVO DIRE UNA COSA SU «ZERO NUMERI NUOVI»

**Il metodo è parameter-free nella FISICA: l'unica lunghezza è `LAM`, e `LAM/sqrt(3)` ne
discende** *(la diagonale del cubo di lato `a` è `a·sqrt(3)`, quindi `a = LAM/sqrt(3)` dà
diagonale `LAM`)*.

**MA LA SUDDIVISIONE NON TERMINA IN MODO ESATTO AL BORDO DELLA REGIONE**, e va detto:

- una cella tutta dentro la palla si risolve *(coperta o libera)* in un numero finito di
  suddivisioni, perché i nodi sono finiti;
- **una cella che ATTRAVERSA la superficie della sfera non è né dentro né fuori**, quindi si
  suddividerebbe **all'infinito**: il guscio ha volume che tende a zero ma **non diventa mai
  vuoto**.

> ### ✅ **LA RISOLUZIONE NON SI SCEGLIE — precisazione di Luca, 2026-09-24**
>
> ```
> si ferma la suddivisione quando il lato della cella e' piu' piccolo di cio' che
> `float64` distingue RISPETTO A LAM:        lato < LAM * eps_macchina
> ```
>
> **`eps` è una proprietà DEL CALCOLATORE, non un numero scelto** — `np.finfo(float).eps`,
> `2.22e-16`. **Sotto quella soglia due posizioni non sono più posizioni diverse: sono lo
> stesso `float`.** Suddividere ancora non aggiungerebbe informazione, **ne toglierebbe**.
>
> **Avevo scritto «non è zero numeri, è zero numeri fisici più una risoluzione»: con `eps` la
> frase cade**, perché `eps` non è un numero del modello né una mia scelta. **Resta UN
> NUMERO SOLO: `LAM`.**
>
> **IL CONTATORE `A8` RESTA** *(Luca)*, e va detto perché: `eps` rende la risoluzione non
> arbitraria, **non la rende innocua**. Se celle vengono abbandonate lì, la saturazione
> dichiarata **non è esatta**, ed è esattamente ciò che il contatore deve rendere visibile.
> **Un presidio che non conta non è un presidio.**

## 5-ter-bis. ✅ **IL CODICE DELL'ARRESTO DERIVATO** — *2026-09-24*

**Due metodi:** `_celle_vive` *(la classificazione)* e `_semina_lam` *(il ciclo)*.

```
celle di lato LAM/sqrt(3), OGNI cella col SUO lato (le libere restano grandi)
  MORTA        tutta fuori dalla palla, OPPURE coperta da un nodo
  LIBERA       tutta dentro, e il nodo PIU' VICINO AL CENTRO dista >= LAM
               ⚠ NON "ogni suo punto va bene": il test guarda UN SOLO nodo, e un
                 ALTRO nodo puo' stare entro LAM da un angolo (rilievo di Luca)
  DA DIVIDERE  in parte coperta, o a cavallo del bordo -> si spezza in 8
la cella si sorteggia con peso `lato^3`; si finisce quando non resta nessuna cella
```

### ⚠ DUE LIMITI DEL CODICE, dichiarati invece che taciuti

1. **il test guarda UN SOLO nodo — il più vicino al CENTRO della cella — e questo ha DUE
   conseguenze, non una:** una cella coperta dall'**unione** di più nodi non è riconosciuta e
   **si suddivide** *(costa lavoro, non correttezza)*; **e una cella detta «LIBERA» può avere un
   altro nodo entro `LAM` da un angolo**, quindi **«LIBERA» non garantisce che ogni suo punto
   vada bene** *(rilievo di Luca)*.
   **LA CORRETTEZZA NON DIPENDE DA QUESTO TEST:** dipende dal fatto che **ogni proposta è
   verificata contro TUTTI i nodi** prima di essere accettata. Il test delle celle serve a
   sapere **dove proporre** e **quando fermarsi**, non a garantire i punti;
2. **la risoluzione `LAM · eps`** ferma la suddivisione, e le celle abbandonate lì si **contano**
   *(`_sl_abbandonate`)*. **Se il contatore sale, la saturazione dichiarata non è esatta.**

### ❌ E UNA DIAGNOSI MIA, SBAGLIATA, che resta scritta

Avevo scritto che **`C3` aveva preso un difetto del codice** *(frazione `0.536` contro `0.384`)*.
**Era la frazione GLOBALE, che il mandato di Luca aveva già dichiarato inadatta.**
**La prova che la diagnosi era sbagliata: dopo la «correzione» la globale è SALITA** *(`0.536`
→ `0.568`)*. **Ho letto un numero dichiarato inadatto e ne ho tratto una conclusione.**

**Il cambiamento resta comunque giusto, per un'altra ragione:** proponevo **un punto per cella**,
quindi gli interstizi pesavano come le regioni grandi e **le proposte non erano uniformi nel
volume libero** — e l'`RSA` è *esattamente* «uniforme nella regione, condizionato
all'accettazione». **La cura era giusta; il motivo che avevo scritto no.**

## 5-quater. I CRITERI DELL'ARRESTO DERIVATO — **fissati PRIMA del codice** *(Luca)*

| | criterio | perché |
|---|---|---|
| **`C1`** | **flag spento: byte-identico** | par.2.1. L'arresto vive dentro `SEMINA_LAM`: a flag spento non esiste |
| **`C2`** | **la capienza è INDIPENDENTE da `n` chiesto** *(prova del raddoppio)* | ❗ **È IL CRITERIO CHE OGGI FALLISCE:** misurato `+0.61 %`, `+4.11 %`, `+2.77 %` a tre raggi. **Con l'arresto derivato deve dare `0` esatto**, perché la saturazione non dipende dalla domanda |
| **`C3`** | **frazione di impacchettamento `0.384` NELLA SFERA INTERNA** — i nodi a distanza `>= R_CONN` dal bordo, **entro la dispersione fra QUATTRO semi** | ❗ **È IL CONTROLLO CONTRO UN VALORE ESTERNO AL PROGETTO**: se si discosta, **il codice è sbagliato**, non il sistema. **RIDEFINITO da Luca, 2026-09-24:** si misura **dentro**, dove il bordo non arriva, **e li' vale `0.384` senza sconti** |
| **`C4`** | **nessun rifiuto falso**: con `n` sotto la capienza misurata la semina riesce **sempre**, su **quattro semi** | è il difetto che Luca ha trovato, e questo criterio **lo mette alla prova invece di fidarsi** |

> ### ⚠ `C3` È IL CRITERIO PIÙ FORTE DEI QUATTRO, e va detto perché
> `C1`, `C2` e `C4` verificano che il codice sia **coerente con se stesso**. **`C3` lo confronta
> con un numero che nessuno in questo progetto ha scelto** — la frazione di saturazione
> dell'`RSA` in 3D, `~0.384`, misurata in letteratura su un problema che è lo **stesso**.
> **È il solo dei quattro che possa dire «il codice è sbagliato» invece di «il codice non fa
> quello che credevo».**
>
> ### ✅ **E IL SUO LIMITE È TOLTO, NON GIRATO — precisazione di Luca**
>
> **Avevo scritto «`C3` si legge sui raggi GRANDI, e sui piccoli si aspetta di meno».**
> **È un criterio che si adatta al risultato**, cioè il difetto che `P1-sexies` insegue: una
> soglia che si allarga dove il dato non torna **non può più fallire**.
>
> **LA FORMA GIUSTA È RESTRINGERE IL DOMINIO, NON LA SOGLIA:** si misura la frazione **solo
> sui nodi a distanza `>= R_CONN` dal bordo**. **Lì il bordo non arriva, e `0.384` vale senza
> sconti**, entro la dispersione fra **quattro semi**.
> **La soglia resta dura; è il dominio a essere onesto.**

**⚠ I NUMERI DI PRIMA RESTANO NEL REGISTRO COME STORIA** *(decisione di Luca)*: sono
misurati col criterio a lotti, e **vanno rifatti**. Il par.5-bis e questa sezione dicono con
quale criterio ciascuno è stato preso.

## 6. `massa_critica_collasso` — **MARCATA, NON TOCCATA** *(decisione di Luca)*

> ### **«Tarata sotto la scala di Planck, da non usare.»**

**Il conto, derivato** *(`csv/_test_fork/_usi_massa_critica.py`)*:

```
massa_critica_collasso() = 621.4858 nodi, in una sfera di raggio LAM = 0.8
quanti PUNTI stanno in una palla di raggio LAM con distanze mutue >= LAM?
  uno al centro + al piu' 12 sulla sfera (separazione >= 60 gradi = NUMERO DI BACIO, K(3)=12)
  -> al piu' 13
RAPPORTO CHIESTO / POSSIBILE = 47.81
```

**La costante chiede ~`48` volte più nodi di quanti ne stiano.**

**`36` usi nel simulatore, elencati dall'AST: `21` nel codice della FISICA** *(dove essere tarata
sotto la scala di Planck **entra nelle leggi**)* **e `15` nelle SCENE** *(dove decide **quanti**
nodi seminare)*. **Non si tocca niente:** l'elenco è **il perimetro della marcatura**, perché
una costante marcata senza l'elenco di chi la usa è un'avvertenza generica, **e un'avvertenza
generica non impedisce nulla** *(`A9`)*.

> **⚠ E IL MIO PRIMO CONTO ERA SBAGLIATO:** avevo usato l'impacchettamento di **Kepler** —
> palline di raggio `LAM/2` **interamente dentro** una sfera di raggio `LAM`, `8·0.7405 = 5.92`.
> **Kepler impone una condizione più stretta di quella vera**: qui il vincolo è **solo sui
> centri**. **Il numero di Luca — «circa una dozzina» — era esatto, e il mio troppo piccolo di
> ~2.2 volte.** Il conto sbagliato **resta stampato nel referto**, col perché.

## 7. COSA QUESTA SCHEDA **NON** COPRE

- **la MITOSI**, che crea nodi vicino al genitore: **rispetta `LAM`?** `S4` lo rileverebbe **al
  passo zero**, non ai passi dopo. **→ in coda, misurarlo;**
- **`Λ = media GLOBALE di `I` dentro la legge locale di `cs`** — più materia nel sistema, meno
  rallentamento: **sospetto famiglia `D01`/`D03`. → in coda;**
- **la scelta alternativa: FILTRARE GLI ARCHI** *(`NASCITA_LAM`)*, **ritirata** — vedi il
  cappello di questa scheda. **Esclusa per DIMOSTRAZIONE**, non per misura: lascia i nodi sotto
  `LAM`, quindi **viola `A13` per costruzione**.

---


### ✅ LA SCENA `(ii)` È IN CODICE: **`semina(n < 0)` = FINO A SATURAZIONE** *(2026-09-25)*

**`_semina_lam` accetta `n < 0`: nessun bersaglio, si semina finché non resta una cella viva.**
**Non è una manopola nuova** *(par.3)*: l'arresto era **già** derivato da `LAM`
*(Zhang-Torquato)*; questo modo si limita a **non imporre un `n`**.

> ### **PERCHÉ SERVE, ed è un errore che Luca ha già preso:** la capienza **DIPENDE DAL SEME**
> — misurata `12807 / 12783 / 12812 / 12790`. **Chiedere la MEDIA fa RIFIUTARE i semi sotto
> media**, e il rifiuto aveva ragione: era la richiesta a essere sbagliata.

**DUE PRESIDI, entrambi `A9`:**
- **il tetto dell'array è GEOMETRICO**, non scelto *(al più un nodo per cella di diagonale
  `LAM`)*, e **se venisse raggiunto il codice si FERMA e lo DICE**: l'array sarebbe stato il
  vincolo invece della geometria;
- **`n < 0` senza `SEMINA_LAM` è un RIFIUTO**: senza distanza minima **la saturazione non
  esiste**, e ridurre a un numero qualunque sarebbe una riduzione silenziosa. **Il braccio di
  controllo di `P-GONFIA` passa il numero MISURATO dal braccio acceso**, non un numero a caso.

### ✅ LA GEOMETRIA DELLA SCENA `(ii)` SI DERIVA DA UN SOLO INGRESSO, `--sep`

```
centri sul cerchio di raggio `sep`  ->  distanza fra centri adiacenti = sep*sqrt(3)
raggio della regione                ->  r  = (sep*sqrt(3) - R_CONN)/2
                                        cioè IL VARCO FRA LE SUPERFICI È `R_CONN`
raggio del vuoto                    ->  Rv = sep + r + R_CONN
                                        un guscio di `R_CONN` oltre la regione più esterna
```

**E riproduce ESATTI i numeri misurati il 2026-09-25**, che erano stati ottenuti per altra via:

| scena | `--sep` | `r_regione` | `raggio_vuoto` | `n` *(saturazione)* | nodi/regione | **ARCHI** |
|---|--:|--:|--:|--:|--:|--:|
| **`(a)` «stesso raggio»** | `6.1158` | `4.096438` | `12.612238` | `12 802` | `411 / 413 / 413` | **`471 564`** |
| **`(b)`** | `4.0` | `2.264102` | `8.664102` | `4 252` | `67 / 75 / 64` | **`148 237`** |

**LE MASSE NON AGGIUNGONO NODI:** `QUOTA` *(dentro/totale)* vale **`0.0966`** in `(a)` e
**`0.0484`** in `(b)`, contro i `0.0961` e `0.0492` previsti.
**E la distanza minima regge:** `min(d_nodi) = 0.800005` e `0.800000` contro `LAM = 0.8`.

**IL COSTO, misurato dagli ARCHI come imposto:** `471 564` contro `148 237`, cioè **`3.2×`** —
**non `5.4×` come i nodi.** La mia stima *«`~500k` e `~150k`»* regge entro il `6 %`.

**⚠ `conc_nodi` NON viene toccato, di proposito:** le regioni **non sono masse SEMINATE**, e
marcarle come tali direbbe che il lignaggio viene da una semina che non c'è stata.

**⚠ E LA SCENA RIFIUTA SE LA RETE NON È VUOTA:** il vuoto dell'`import`/di `--nodi` si
**sommerebbe** a quello della scena — **due vuoti, non uno**. Si lancia con **`--nodi 0`**, e la
rete **non si svuota da sola** *(`A9`: svuotarla butterebbe via ciò che un altro flag ha
chiesto, senza dirlo)*.


### ➕ `CURA 4` E LA SCENA `(ii)`: la semina della scena è **INIZIALE** *(2026-09-25)*

`_semina_masse_coerenti` chiama `net.semina` **una sola volta, su rete vuota** *(la scena RIFIUTA se `net.n` non è zero)*, quindi il default `maturi=None` la classifica **iniziale** e i suoi nodi nascono **maturi**. **È la condizione che rende misurabile `S9` al passo zero**, che oggi non lo è.

### ✅✅ `SCENA-1`, STRADA (1): **IL VUOTO DI DEFAULT E' LA SATURAZIONE, E `SEMINA_LAM` E' OBBLIGATORIA** *(Luca, 2026-09-25)*

```
PRIMA   net.semina(a.nodi)          con `a.nodi = SEME_INIZIALE = 900` in raggio 4.0
        -> con `SEMINA_LAM` RIFIUTA: la saturazione vera e' 455
DOPO    net.semina(-1 if SEMINA_LAM else a.nodi)
        -> LA SATURAZIONE, senza un numero: **il numero lo decide la GEOMETRIA**
```

> ### **E NON SI POTEVA AGGIRARE CON UN NUMERO**, perché **la capienza DIPENDE DAL SEME**
> *(misurato: `12807/12783/12812/12790`)*. **Scegliere `455` avrebbe fatto rifiutare i semi più
> poveri** — l'errore già preso il 2026-09-25.

**⚠ SOLO a flag ACCESO:** a flag spento **la saturazione non esiste** *(senza distanza minima non
c'è un limite)*, e `semina` **lo dice da sé rifiutando `n < 0`**.

**⚠ E IL VUOTO DELL'`import` RESTA A `SEME_INIZIALE`:** lì `SEMINA_LAM` è ancora `False` *(i flag
si applicano DOPO, in `_applica_flag`)*, e **la cura del mondo del 2026-09-21 ha già stabilito che
quel vuoto viene RICOSTRUITO quando i flag sono noti.** Cambiarlo lì significherebbe **deciderlo
prima di sapere con quali flag si gira.**

### ⛔ LE SCENE CHE SEMINANO MASSE SOPRA IL VUOTO SONO **DI EPOCA PRE-`A13`**

**`_massa` RIFIUTA con `SEMINA_LAM` acceso, e lo DICE** *(`A9`)*: **non si adatta in silenzio.**

> **PERCHÉ, misurato:** `_massa` chiede `n` nodi in un raggio **scelto per la scena**, e quei
> raggi vengono dall'epoca in cui **una distanza sotto `LAM` era ammessa**. Il caso più chiaro:
> `_semina_n_masse` chiede **`497` nodi in raggio `0.7 = 0.875 LAM`, dove ce ne stanno `5`** —
> **rapporto `104`**.
> **Non è una scena da adattare: è una scena di un'altra fisica.**

**La scena `MASSE-COERENTI` — la scena `(ii)` — NON passa da `_massa`:** le sue masse sono
**regioni a fase coerente di un vuoto solo**, e **non aggiungono nodi**. **È la scena dell'epoca
`A13`.**

**✅ `SEMINA_LAM` È USCITA DALLE `ESCLUSE`** del sigillo del driver, ed è **obbligatoria**:
`NUDA = CAMPAGNA`. **Il criterio `S5` verifica la compatibilità a ogni corsa**, quindi se un
giorno tornasse incompatibile **lo direbbe da sé.**

<!-- SCHEDA nome=invarianti funzioni=verifica_invarianti flag=INVARIANTI,DOMINI -->

### ⛔ **AGGIORNAMENTO del 2026-10-06 — LA FORMA `dip`, e l'invariante si PRECISA**
*(cura di `TORS-W8-AVVOLGIMENTO`)*

`twp_dip`, il **dipolo precedente d'arco**, nasce ### **`nan`**: e' il marcatore di *«arco
che non ha ancora visto un passo di torsione»*, e il primo passo di torsione lo **consuma**
dando spinta **zero**.

| | |
|---|---|
| la **regola** | ### **finito, oppure `nan` SOLO su un arco con `tw == 0` ESATTO** |
| perche' `tw == 0` identifica l'arco nuovo | ### **tutte e tre** le vie di nascita azzerano `tw` *(`_rn_div_tw`, `_rn_sch_tw`, `_allaccia`)*, e ### **solo il passo di torsione lo muove** |
| il contatore | `_g_inv_dip_nan_ok`: quanti `nan` **ammessi** il controllo vede |

### ⛔ **SI PRECISA, NON SI ALLARGA — ed e' la lezione di `peq`, scritta in questa stessa
### scheda:** *«la risposta giusta non e' allargare la regola ma PRECISARLA»*.
### **Un `nan` su un arco con `tw != 0` resta UNA VIOLAZIONE.**

### ✔ **E IL <<MAI OLTRE UN PASSO>> E' STRUTTURALE, non vigilato:** il passo di torsione
scrive `twp_dip` ### **incondizionatamente su OGNI arco**, quindi dopo **qualunque** passo di
torsione ### **nessun arco ha `nan`.** Il `nan` puo' esistere **solo** fra una nascita e il
passo dopo. ### **Lo DIMOSTRA il sigillo `S1`, non lo spera un contatore.**

### ⚠ **E IL PRIMO NUMERO:** sul giro minimo, `471564` archi nascono `nan` alla costruzione e
### **`0` ne restano dopo il primo passo di torsione.**

> ### ✅ **COMMIT 4 — IL CONTROLLO DI DOMINIO HA UN'ESENZIONE PER CELLA, ANCORATA AL VELENO** *(2026-10-03)*
>
> ### **E LA CADUTA CHE L'HA RICHIESTA DICE UNA COSA CHE NESSUNO SAPEVA, e va scritta qui:**
> ### **PRIMA del veleno, dopo ogni nascita, QUESTO STESSO CONTROLLO verificava il dominio
> ### di derivate che portavano VALORI VECCHI** *(copiati, o semplicemente lasciati li')*,
> ### **e che passavano PERCHE' ERANO POSITIVI PER CASO.**
>
> ### ➜ **Il controllo sulle derivate dopo una nascita verificava valori NON VALIDI** — e
> ### nessuno lo sapeva, perche' un valore vecchio ma positivo supera `> 0` come un valore
> ### giusto. ### **Il veleno non ha introdotto il problema: lo ha reso VISIBILE**, mettendo
> ### `nan` dove c'era un numero che non significava niente.
>
> **COME FUNZIONA l'esenzione**: per una derivata con un registro di veleno ### **VIVO**
> *(stesso oggetto)*, nelle celle avvelenate il valore ### **DEVE essere `nan`** — e un
> ### **NUMERO** li' e' un ### **DIFETTO DA NOMINARE**, perche' vuol dire che qualcuno ha
> scritto ### **una cella senza riscrivere la derivata**. Fuori da quelle celle vale il
> dominio dichiarato, come prima. Se l'oggetto e' ### **cambiato**, il registro e' ### **scaduto**:
> si cancella e il dominio si applica ### **pieno**.
>
> ### 📌 **E' IL TERZO CASO DELLA STESSA ESENZIONE** *(dopo `eta` sull'intero dominio e
> `peq` per cella con la marca `_peqn_idx`)*, quindi per `9-ter` ### **non e' una legge in piu'.**
> ### **E non c'e' nessun elenco a mano:** il registro del veleno lo scrive `_avvelena_derivate`
> leggendo la ### **CLASSE DI NASCITA** da `REGISTRO_DERIVATE`.
>
> *(La scheda del veleno e' `veleno-derivate`.)*


> ## ✅ **AGGIORNATA il 2026-09-25 — `nonneg_inf`, e l'invariante HA FERMATO UNA CURA**
> **Il dominio di `eta` e' cambiato** (`RAMPA-1`: il vuoto dato ha `eta = +inf`), quindi la sua
> **forma** passa da `nonneg` a **`nonneg_inf`**:
>
> ```
> nonneg       ~isfinite | (v < 0)        -> `inf` e' un DIFETTO
> nonneg_inf   isnan     | (v < 0)        -> `+inf` AMMESSO, `nan` e `-inf` NO
> ```
>
> ### ❌ E L'INVARIANTE HA FERMATO LA CURA AL PRIMO GIRO
> ```
> [INVARIANTE] `eta` VIOLA `>= 0` al passo 1, in `memoria_hebbiana_moto`.
>   quanti: 4252   valori: inf, inf, inf, ...   quanti=4252 su=4252
> ```
> **Ha funzionato**: una legge nuova ha incontrato il dominio dichiarato e **si e' fermata**,
> invece di girare per 120 passi con un valore che nessuno aveva ammesso.
>
> ### ⚠ **NON SI ALLARGA `nonneg`**, e il perche' e' `A9`
> `nonneg` copre `rho_spin`, `_deg`, `_chi_core_raggio` e altre: **per loro un `inf` resta un
> difetto**. **Una forma nuova per UNA grandezza costa meno di un controllo indebolito per
> dodici** — un presidio che ammette tutto non impedisce niente.
>
> ### ❌ E UN LIMITE DEL MIO AUDIT, che va scritto qui perche' si ripetera'
> `csv/_letture_eta.py` cerca `eta` **per AST**, come **attributo** o **nome**. Qui `eta` e' una
> **CHIAVE DI TABELLA**, cioe' una **STRINGA** (`'eta': ('nonneg', ...)`), e l'audit **non
> poteva vederlo**. **In un codice guidato da tabelle, un audit su chi LEGGE una grandezza deve
> cercare anche le stringhe.** *(Il limite dichiarato prima era un altro — «la riduzione si
> cerca sulla stessa riga» — e questo si e' aggiunto: due limiti, e il secondo l'ha trovato il
> codice, non io.)*


# ⑩ GLI INVARIANTI DI DOMINIO — **`C5`**

> **Scheda aperta il 2026-09-24, e mancava.** `C5` è in `CURE VERIFICATE` con sigillo `3/3`,
> **è la sola cura ACCESA DI DEFAULT**, e **non aveva una scheda**: `REG-R` l'ha preteso quando
> `E4-LAM` ha toccato la legge. *(Un difetto di inventario, non di fisica — ma l'ordine giusto
> è questo: prima la scheda.)*

## LA FORMA

**`verifica_invarianti(dove, passo)`** scorre **`DOMINI`** — un dizionario
`nome → (forma, perché)` — e per ogni grandezza di stato presente controlla che stia **nel suo
dominio**. Alla prima violazione **solleva `DominioViolato`** con: **la grandezza**, **la regola
violata**, **il passo**, **gli INDICI**, **i valori**, **dove**, e **quale arco** *(`i`-`j`)*.

**DUE LIVELLI, e la distinzione è il punto:**

| livello | che cosa prende | come |
|---|---|---|
| **NUMERICO** | overflow, **divisione per zero**, valori non validi | `np.seterr(over='raise', divide='raise', invalid='raise', under='ignore')` a **`:7382`**. **L'UNDERFLOW non ferma niente**, perché densità come `1e-81` di un nodo neonato sono **legittime** |
| **FISICO** | ogni grandezza **dentro il suo dominio**, a fine passo | `DOMINI` + `verifica_invarianti` |

> **L'esplosione del 21/9 NON era un overflow** *(`1.8e6` è un numero normale)*: **l'avrebbe
> presa solo la regola FISICA `peq >= 0`.** È la ragione per cui i due livelli non si
> sostituiscono.

## LE FORME DI DOMINIO

| forma | regola | esempi |
|---|---|---|
| `'lam'` | **`>= LAM`** | `d`, `d0` |
| `'pos'` | `> 0` | `_dt_e_ultimo`, `_r_corrente`, `_cs_nodo_prev` |
| `'finito'` | finito, nessun vincolo di segno | `vd`, `_spinor_lift` |
| `'fase'` | in `[0, 4π)` | `phi`, `phi0` |
| `'unita'` | `|x| = 1` *(tolleranza `1e-6`)* | gli spinori |
| `'idx'` | `0 <= x < n` | `i`, `j` |

## ✅ `E4-LAM` — **LA LEGGE `d >= LAM` SI VERIFICA SEMPRE** *(decisione di Luca, 2026-09-24)*

> ### **«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema» è una
> ### LEGGE, non una garanzia che dipende da un flag.»**

**PRIMA** il controllo della forma `'lam'` era dentro `if _lam_attivo:`, con
`_lam_attivo = SCALA_MIN or SCALA_MIN_PASSO`, e **a flag spenti DEGRADAVA a `> 0`**:

```python
if _lam_attivo:  cattivo = ~fin | (vf < LAM * (1.0 - 1e-12))   # '>= LAM, con la scala minima accesa'
else:            cattivo = ~fin | (vf <= 0.0)                   # '> 0 (scala minima SPENTA)'
```

**DOPO**, incondizionato:

```python
cattivo = ~fin | (vf < LAM * (1.0 - 1e-12))
regola  = '>= LAM (= %.6f) -- LEGGE, non opzione' % LAM
```

**E `_lam_attivo` è stato TOLTO**: era il suo unico uso, e lasciarlo sarebbe stato codice morto
*(verificato dall'AST: `0` riferimenti di codice)*.

**Perché è giusto, in una riga:** **una legge verificata solo quando un flag è acceso non è una
legge, è un'opzione** — ed è `A9`: *un presidio che non impedisce non è un presidio.*

**La tolleranza `1e-12` non è un numero scelto:** è l'**arrotondamento** di `LAM`, cioè la
precisione con cui `LAM` stesso è rappresentabile.

### **IL SIGILLO** — `csv/_seal_fork/_sigillo_e4lam.py`

| | | |
|---|---|---|
| `T3` | **un arco sotto `LAM` a flag SPENTI FERMA il run** | quello che prima **non** faceva |
| `T4` | e con `d >= LAM` **non** si ferma | **il controllo che rende `T3` leggibile**: senza, `T3` passerebbe anche se il controllo si fermasse sempre |
| `T5` | **byte-inerte**: `206` campi identici, `0` diversi contro `_cura1_corto` | l'invariante **legge soltanto** |

**Il messaggio, verbatim:**

```
[INVARIANTE] `d` VIOLA `>= LAM (= 0.800000) -- LEGGE, non opzione` al passo 1
  indici (primi 8): 1     valori: 4.000000e-01     arco=1-2
```

## ❌ `D37` — **UNA CHIAVE DUPLICATA NEI `DOMINI`, ed è mia**

`'_cs_nodo_prev'` compariva **due volte**: `:226` *(la mia)* e `:257` *(preesistente)*.
**In un letterale di dict vince l'ULTIMA**, quindi la mia era **codice morto** — e **il sigillo
lo ha mostrato**, stampando una descrizione **che non era la mia**.

**La causa è `P1`:** avevo cercato la voce in una finestra di **28 righe** (`213-240`) e la voce
sta a **`:257`**. **Ho concluso un'ASSENZA da una ricerca PARZIALE.**
**Cura: si toglie la mia, si tiene la preesistente.** **E la derivazione resta valida:
`cs > 0` era GIÀ un invariante**, fatto da qualcun altro prima di me.

### ✅ **`D37` È CURATO** — 2026-09-24, lo stesso giorno in cui è nato

La voce duplicata è **via**, e **la derivazione di `cs > 0` è stata SPOSTATA sulla voce
preesistente** invece di essere buttata — col motivo per cui era nata **e col perché era
un duplicato**, così chi la legge fra un mese sa entrambe le cose.

**E c'è un TEST PERMANENTE:** **`T1b`** del sigillo `E4-LAM` verifica **dall'AST** che il
letterale `DOMINI` **non abbia chiavi duplicate** — oggi **`42` chiavi, `0` duplicate** —
col suo collaudo `K7` *(un `DOMINI` con `'a'` due volte → `['a']`)* e `K8` *(uno pulito non
dà falsi allarmi)*.

> **⚠ IL LIMITE DI `T1b`, dichiarato:** guarda il **letterale**. Voci aggiunte con
> `DOMINI[...] = ...` **non le vedrebbe**. Oggi non ce ne sono, e se ce ne fossero il test
> **non lo direbbe**.

## ⚠ COSA QUESTA LEGGE **NON** FA, dichiarato

- **non corregge**: **legge soltanto**, e su un run sano **non cambia un bit**. Se scatta, il
  run **si ferma** — non si aggiusta;
- **non dice se la REALIZZAZIONE di una legge sia giusta.** Verifica che `d >= LAM`; **come** il
  sistema lo ottiene è il **freno a senso unico**, cioè **`D31`**. **La legge è giusta, la
  realizzazione no**, e sono due cose separate;
- **non copre le grandezze assenti**: `getattr(self, quale, None) -> continue`. Una grandezza
  che **non esiste** non viene controllata, e **questo non è contato**. *(Candidato per un
  contatore `A8`: quante voci di `DOMINI` vengono SALTATE per assenza. Non fatto.)*

## COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **se `'fase'` debba essere `[0, 4π)` o `[0, 2π)`.** È la domanda di `FASE_2PI`, e
   l'invariante **segue** la decisione invece di guidarla — oggi codifica il `4π`
   **dichiarato**, che la mappa del `4π` classifica come **convenzione**, non come misura;
2. **quante voci di `DOMINI` vengano saltate per assenza** in un run vero: non misurato.

---

<!-- SCHEDA nome=freno-legge funzioni=_smorza flag=SCALA_MIN,SCALA_MIN_PASSO,LAM -->

# ⑪ IL FRENO DIVENTA LA LEGGE — **la cura proposta di `D31`**

> **Decisione di Luca, 2026-09-24: SCHEDA ORA, CODICE SOLO DOPO LA PROVA DI `CURA 2`.**
> **Qui non si tocca una riga di codice.**

## 0. LA LEGGE, nelle parole di Luca

> ### **«Nessun arco sotto `LAM`, e l'avvicinamento al minimo è ASINTOTICO: rallenta sempre
> ### di più, senza mai toccarlo.»**

**Che cosa vuol dire, in una riga:** più l'arco è vicino al minimo, più **ogni suo movimento**
viene rallentato. **Al confine la mobilità va a zero**: l'arco si avvicina a `LAM` per sempre
senza toccarlo, come una curva che si avvicina al suo asintoto. **Lontano dal confine la
mobilità torna quasi piena.**

**✅ LA LEGGE È GIUSTA. ❌ LA REALIZZAZIONE NO.**

## 1. IL FRENO DI OGGI — `_smorza`, `:3607-3618`

```python
scende = dx < 0.0
fatt   = max(0.0, 1.0 - LAM / prima)          # = (d - LAM)/d  =  LA MOBILITA'
eff    = np.where(scende, dx * fatt, dx)      # <-- SOLO la discesa
```

Con **`u = d − LAM`** *(la distanza dal minimo)* e **`m = u/d`** *(la mobilità)*:

| verso | oggi | è asintotico? |
|---|---|:--:|
| **discesa** `dx < 0` | `u ← u·(1 + dx/d)`, cioè incremento `dx·m` | **SÌ** — `m → 0` al confine |
| **salita** `dx > 0` | `u ← u + dx` — **identità esatta, nessun rallentamento** | **NO** |

> **È tutta qui l'asimmetria, ed è il cricchetto di `D31`.**

## 2. LA DERIVA DI OGGI — **primo ordine, e MASSIMA AL CONFINE**

Rumore simmetrico: `dx = +a` e `dx = −a` con probabilità `1/2`.

```
E[Δu]  =  ½·(+a)  +  ½·(−a·m)  =  (a/2)·(1 − m)  =  (a/2)·(LAM/d)
```

| | |
|---|---|
| **ordine nel rumore** | **PRIMO** — lineare in `a` |
| **al confine** *(`d → LAM`)* | `LAM/d → 1` ⇒ **`E[Δu] → a/2`: la deriva è MASSIMA proprio dove il vincolo morde** |
| **lontano** *(`d ≫ LAM`)* | `LAM/d → 0` ⇒ la deriva svanisce |

> **Il cricchetto spinge gli archi LONTANO dal muro, e spinge di più quanto più sono vicini.**
> È la forma esatta di ciò che `Z113` ha dimostrato *(deriva `+1.582064e-03` contro l'attesa
> derivata `+1.582007e-03`, scarto `0.0 %`)* e che i bilanci misurano: il termine **FRENO** vale
> **`+117 %`** di `Δ(Σd0)` nel riferimento di `G4`. **Un freno che AGGIUNGE lunghezza è un
> motore.**

## 3. LA FORMA PROPOSTA — **la stessa mobilità nei DUE versi, in forma esatta**

```
(d − LAM)  ←  (d − LAM) · exp(dx / d)
```

cioè, tenendo l'interfaccia di `_smorza` *(che ritorna un INCREMENTO)*:

```
eff  =  u · (exp(dx / d) − 1)              # e il chiamante fa d += eff, come oggi
```

### **LE TRE PROPRIETÀ, verificate sulla formula**

| | | |
|---|---|:--:|
| **(a) SIMMETRICA** | lo stesso fattore per `dx > 0` e `dx < 0`. **Un arco vicino al minimo è «viscoso»: si muove poco in entrambi i versi** | ✅ |
| **(b) MAI SOTTO `LAM`, per QUALUNQUE passo** | `exp(·) > 0` sempre ⇒ `u_new > 0` **strettamente**, anche per `dx → −∞`. **L'arco si avvicina a `LAM` per sempre senza toccarlo** | ✅ |
| **(c) LOCALE** | lontano da `LAM`: `u ≈ d` ⇒ `u_new ≈ d·exp(dx/d) ≈ d + dx` — **tende all'identità** | ✅ |

### **E AL PRIMO ORDINE È ESATTAMENTE LA MOBILITÀ DI OGGI**

```
u·(exp(dx/d) − 1)  =  u·(dx/d)  +  O(dx²)  =  dx·m  +  O(dx²)
```

**Cioè: il fattore non cambia, cambia il VERSO IN CUI SI APPLICA.** Non è una legge nuova: è
**la stessa legge, resa simmetrica**.

### ⚠ **E UN GUADAGNO CHE OGGI NON C'È: il vincolo vale anche A METÀ PASSO**

Oggi `u ← u(1 + dx/d)` diventa **negativo** se `dx < −d`, e il conto è immediato. Il
`max(0, …)` protegge il **fattore**, non il **risultato**. Oggi quel caso è solo **contato**
*(`_g_sm_patol`)*. **Con l'esponenziale non può succedere**, e il vincolo vale **a ogni
scrittura**, non solo al controllo di fine passo.

## 4. LA DERIVA RESIDUA — **secondo ordine, nulla al confine, decade lontano**

Stesso rumore simmetrico `dx = ±a`:

```
E[u_new]  =  u · ½·(e^{a/d} + e^{−a/d})  =  u · cosh(a/d)

E[Δu]     =  u · (cosh(a/d) − 1)  =  u · a²/(2d²)  +  O(a⁴)
```

| | oggi | proposta |
|---|---|---|
| **ordine nel rumore** | **primo**: `(a/2)·(LAM/d)` | **SECONDO**: `u·a²/(2d²)` |
| **al confine** `d → LAM` | **`→ a/2`, MASSIMA** | **`→ 0`** *(perché `u → 0`)* |
| **lontano** `d ≫ LAM` | `→ 0` | `→ a²/(2d)`, decade come `1/d`; **in termini RELATIVI `a²/(2d²)`** |

### **IL RAPPORTO FRA LE DUE, e da' una CONDIZIONE**

```
  nuova / oggi  =  [u·a²/(2d²)] / [(a/2)·(LAM/d)]  =  a·u / (d·LAM)  =  a·(d−LAM) / (d·LAM)
```

* **al confine** `d → LAM`: il rapporto **→ 0**. La proposta è **incomparabilmente migliore
  proprio dove oggi la deriva è massima**;
* **lontano** `d ≫ LAM`: il rapporto **→ `a / LAM`**.

> ### ❗ **QUINDI LA PROPOSTA È MIGLIORE OVUNQUE SE E SOLO SE `a < LAM`**
> cioè **se il passo tipico di rumore è più piccolo della scala minima**.
> **`LAM = 0.8`. Il valore di `a` NON È MISURATO**, e va misurato prima di cablare: è la
> prima cosa che la verifica deve dire. *(`A12` regola 4: dichiarato, non assunto.)*

## 4-bis. ❓ **LA CORREZIONE DI ITÔ** — *proposta del guardiano, e la scelta è di Luca*

> **La deriva residua viene dalla CONVESSITÀ di `exp`.** La correzione derivata la toglie:
>
> ```
> (d − LAM)  ←  (d − LAM) · exp(dx/d − (dx/d)²/2)
> ```

**Verificato numericamente, non solo algebricamente** *(`csv/_test_fork/_z147_ito.py`)*. Con
`s = a/d`:

| `s` | **piana** `E[f]−1` | attesa `s²/2` | **Itô** `E[f]−1` | attesa `−s⁴/12` | `\|Itô\|/\|piana\|` |
|--:|--:|--:|--:|--:|--:|
| `0.250` | `+3.141310e-02` | `3.125e-02` | **`−3.201451e-04`** | `−3.255e-04` | `1.019e-02` |
| `0.125` | `+7.822678e-03` | `7.813e-03` | **`−2.026048e-05`** | `−2.035e-05` | `2.590e-03` |
| `0.0625` | `+1.953761e-03` | `1.953e-03` | **`−1.270242e-06`** | `−1.272e-06` | `6.502e-04` |

**E l'ORDINE si legge raddoppiando `s`:**

| | piana | Itô |
|---|--:|--:|
| `s: 0.0625 → 0.125` | **`×4.004`** *(atteso `2² = 4`)* | **`×15.950`** *(atteso `2⁴ = 16`)* |
| `s: 0.125 → 0.25` | **`×4.016`** | **`×15.801`** |

> **La deriva scende dal SECONDO al QUARTO ordine**, e **cambia SEGNO: diventa NEGATIVA**,
> cioè **verso il confine** invece che lontano da esso.

### ✅ **E c'è un secondo guadagno che la sola deriva non mostra: la FEDELTÀ**

Entrambe le forme tendono alla legge **`u ← u(1 + x)`**, con `x = dx/d`. **Quanto le si
avvicinano:**

| `x` | `u(1+x)` | **piana** | eccesso | **Itô** | eccesso |
|--:|--:|--:|--:|--:|--:|
| `0.1` | `1.10000` | `1.10517` | **`+5.17e-03`** | `1.09966` | **`−3.41e-04`** |
| `0.3` | `1.30000` | `1.34986` | **`+4.99e-02`** | `1.29046` | **`−9.54e-03`** |

**`exp(x − x²/2) = 1 + x + O(x³)`: i termini in `x²` si cancellano ESATTAMENTE.**
Quindi, **su una spinta DETERMINISTICA**, la correzione **non è un bias: toglie l'eccesso di
convessità della piana**, ed è **più fedele** alla legge voluta, non meno.

> **⚠ Il «bias verso il basso di ordine `dx²`» è vero RELATIVAMENTE ALLA PIANA, non
> relativamente alla LEGGE.** Va detto così, perché le due letture portano a decisioni opposte.

### ❌ **MA C'È UN COSTO, e non è nella deriva: la forma NON È MONOTONA**

`f(x) = exp(x − x²/2)` ha **massimo in `x = 1`**, dove vale `√e = 1.64872`. **E poi scende:**

| `x` | piana `exp(x)` | **Itô** | |
|--:|--:|--:|---|
| `0.5` | `1.64872` | `1.45499` | |
| **`1.0`** | `2.71828` | **`1.64872`** | **← il MASSIMO** |
| `1.5` | `4.48169` | `1.45499` | |
| `2.0` | `7.38906` | `1.00000` | **← una salita non muove nulla** |
| `2.5` | `12.18249` | **`0.53526`** | **← UNA SALITA FA SCENDERE** |
| `3.0` | `20.08554` | **`0.22313`** | |

> ### ❗ **Per `dx > 2d` la forma di Itô TRASFORMA UNA SALITA IN UNA DISCESA.**
> **La piana è monotona sempre.** E qualunque salita, con Itô, **non può far crescere `u` di
> più di `√e ≈ 1.6487`** in una scrittura.
>
> **È esattamente la firma che `A11` cerca:** *una spinta più grande che produce un effetto
> più piccolo.* **Non è un difetto se `\|dx\|/d` resta piccolo — ma «resta piccolo» è una
> MISURA, non un'assunzione.**

### **IL CONFRONTO, in una tabella sola**

| | **piana** `exp(x)` | **Itô** `exp(x − x²/2)` |
|---|---|---|
| deriva, rumore simmetrico | `+u·s²/2` — **2° ordine, POSITIVA** *(lontano dal muro)* | **`−u·s⁴/12` — 4° ordine, NEGATIVA** *(verso il muro)* |
| fedeltà a `u(1+x)` | eccesso `+x²/2` | **esatta a `O(x³)`** |
| mai sotto `LAM` | ✅ | ✅ |
| **monotona in `dx`** | **✅ sempre** | **❌ massimo a `x=1`; per `x>2` una salita fa SCENDERE** |
| tetto per scrittura | nessuno | `u·√e ≈ 1.6487·u` |

### ⚠ **E UNA CONSEGUENZA CHE TOCCA UN ALTRO FRONTE**

**La deriva di Itô è NEGATIVA: spinge gli archi PIANO VERSO il muro**, mentre quella di oggi
li spinge **lontano**. **È debolissima** *(`4°` ordine)*, ma il verso è opposto — e la domanda
**«chi spinge gli archi contro il muro»** è già aperta come **`D33` / `S05`**. **Aggiungere una
spinta verso il muro, per quanto piccola, va detto a chi indaga quel fronte.**

> ### **LA SCELTA È DI LUCA, e non la prendo io.** Il criterio che la decide è **misurabile**:
> **la distribuzione di `\|dx\|/d`.** Se resta ben sotto `1`, **Itô è migliore su tutto** e la
> non-monotonia non si manifesta mai. Se arriva vicino a `1`, il tetto `√e` comincia a mordere,
> e **a `2` inverte**. → punti `V8` e `V9` della verifica.

## 4-ter. ✅ **LA TERZA FORMA: `1 + tanh(x)`** — *proposta di Luca, e domina la seconda*

```
(d − LAM)  ←  (d − LAM) · (1 + tanh(dx/d))
```

**Le quattro proprietà, verificate con lo STESSO strumento** *(`csv/_test_fork/_z147_ito.py`)*:

### ✅ **(1) DERIVA ESATTAMENTE NULLA, a TUTTI gli ordini**

`(1 + tanh(x)) + (1 + tanh(−x)) = 2` **per disparità di `tanh`**. Non è un'approssimazione: è
un'identità.

| `s` | `E[f] − 1` |
|--:|--:|
| `0.500` | **`0.000000000000000e+00`** |
| `0.125` | **`0.000000000000000e+00`** |
| `0.001` | **`0.000000000000000e+00`** |

> **Zero ESATTO in macchina, a ogni `s` provato.** La piana dà `+s²/2`, Itô `−s⁴/12`;
> **questa dà zero e basta.**

### ✅ **(2) MONOTONA** — la derivata è `sech²(x) > 0` sempre

Su `[−3, 3]`: **`0` incrementi negativi su `6000`**. *(Itô ne ha `2000` su `3000`.)*

### ✅ **(3) MAI SOTTO `LAM`** — `1 + tanh(x) ∈ (0, 2)`

`x = −50 →` fattore `0.000000e+00` *(numericamente, ma matematicamente `> 0`: `~2e^{2x}`)* ·
`x = +50 →` fattore `2.000000`.

### ✅ **(4) FEDELTÀ `O(x³)`, come Itô** — `1 + tanh(x) = 1 + x − x³/3 + …`, **nessun termine in `x²`**

| `x` | `u(1+x)` | piana | eccesso | Itô | eccesso | **tanh** | **eccesso** |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `0.30` | `1.30000` | `1.34986` | `+4.986e-02` | `1.29046` | `−9.538e-03` | `1.29131` | **`−8.687e-03`** |
| `1.00` | `2.00000` | `2.71828` | `+7.183e-01` | `1.64872` | `−3.513e-01` | `1.76159` | **`−2.384e-01`** |

**È anche un po' PIÙ fedele di Itô** a `x` moderati.

### ⚠ **(5) IL LIMITE, dichiarato: UNA SALITA AL PIÙ RADDOPPIA `(d − LAM)`**

`1 + tanh(x) < 2` **per costruzione**. È una **saturazione**, e `A11` cor.6 dice che *un limite
che satura è un allarme*. **Va giudicato con la distribuzione di `|dx|/d`, esattamente come il
tetto `√e` di Itô** — punti `V8`/`V9`.

> **Ed è MENO restrittivo del tetto di Itô** *(`2` contro `1.6487`)*, **e senza la
> non-monotonia.**

## 4-quater. ❗ **LE TRE FORME A CONFRONTO**

| | **deriva simmetrica** | **monotona** | **fedeltà a `u(1+x)`** | **tetto per una SALITA** |
|---|---|:--:|---|---|
| **piana** `exp(x)` | `+s²/2` — **2° ord., POSITIVA** *(lontano dal muro)* | **✅** | eccesso `+x²/2` | **nessuno** |
| **Itô** `exp(x−x²/2)` | `−s⁴/12` — 4° ord., NEGATIVA | **❌** *(max a `x=1`)* | `O(x³)` | `√e = 1.6487` |
| **tanh** `1+tanh(x)` | **`0` ESATTO** | **✅** | `O(x³)` | `2` *(raddoppia)* |

> ### ❗ **`tanh` DOMINA `Itô` SU OGNI ASSE**
> deriva **più piccola** *(zero contro quarto ordine)* · **monotona**, e Itô no · **stessa**
> fedeltà, anzi un po' migliore · tetto **meno restrittivo** *(`2` contro `1.6487`)*.
> **Quindi Itô esce dal confronto**: non c'è nessun asse su cui sia preferibile.

> ### **LA SCELTA VERA È FRA `piana` E `tanh`, e si riduce a UNA domanda:**
> **`piana` non ha tetto ma HA deriva. `tanh` non ha deriva ma SATURA a `2`.**
> **La decide la DISTRIBUZIONE di `|dx|/d`** — punti `V8`/`V9` — **e la decide Luca DOPO quella
> misura.** *(Non prima: senza quel numero non c'è una base derivata.)*

## 4-quinquies. ✅ **LA FORMA È DECISA — `1 + tanh(x)`** *(decisione di Luca, 2026-09-24)*

```
(d − LAM)  ←  (d − LAM) · (1 + tanh(dx / d))
```

### LA MISURA CHE L'HA DECISA — `V8`/`V9`, dal giro corto di `CURA 2`

*(`csv/_test_fork/_cura2_corto/BILANCIO_d0.txt`, blob `49fc54d2`, `120` passi, seme `42`)*

```
  verso                n        p50      p90      p99    p99.9      max   >0.5   >1   >2
  discese       60538734     0.0019   0.0239   0.0310   0.0344   0.0385    0.0  0.0  0.0
  salite        65192342     0.0024   0.0124   0.0241   0.0307   0.0531    0.0  0.0  0.0
```

> ### ❗ **IL SOLO DIFETTO DICHIARATO DI `tanh` — LA SATURAZIONE A `2` — NON SI PRESENTA MAI.**
> Il **massimo** su **`125 731 076`** campioni è **`0.0531`**: la saturazione conta a `x` di
> ordine `1`, e il massimo misurato è **`19` volte più piccolo**. **Zero campioni oltre `0.5`,
> su entrambi i versi.** Al massimo misurato le due forme differiscono di **`1.4e-03`
> relativo**.
>
> **Quindi `tanh` paga il suo unico prezzo ZERO VOLTE, e in cambio dà deriva ESATTAMENTE nulla.**

### ⚠ E IL CONFRONTO NON È SIMMETRICO, PERCHÉ SULL'ALTRO PIATTO IL NUMERO MANCA

La deriva di `piana` vale `exp(N·E[x²]/2)`, e **`E[x²]` NON È STATO REGISTRATO** — l'involucro
ha salvato **quantili**, `max` e quote, **e i quantili non bastano a stimare una media di
quadrati** *(`csv/_test_fork/_z146_scelta_freno.py`)*:

| ipotesi su `sqrt(E[x²])` | 120 passi | 1200 passi | 6000 passi |
|---|--:|--:|--:|
| `= p50 (0.0024)` | `+0.03 %` | `+0.35 %` | `+1.74 %` |
| `= p90 (0.0124)` | `+0.93 %` | `+9.66 %` | `+58.61 %` |
| `= p99 (0.0241)` | `+3.55 %` | `+41.69 %` | `+471.12 %` |

> **A `120` passi la scelta è indifferente in ogni ipotesi. A `6000` l'intervallo va da
> `+1.7 %` a `+471 %`: TROPPO LARGO per decidere.**
>
> ### **E LA DECISIONE NON NE È INDEBOLITA — È ANZI IL SUO ARGOMENTO PIÙ FORTE:**
> **il costo di `tanh` è MISURATO e vale zero; il costo di `piana` è NON MISURATO e il suo
> intervallo arriva a un fattore.** **Si sceglie la forma il cui prezzo si conosce.**

### ⚠ COSA RESTEREBBE DA MISURARE, e costa **ZERO run in più**

Registrare **`mean((dx/d)²)`** nello stesso involucro che già registra i quantili: **è una somma
in più, sugli stessi campioni.** **Non cambia la decisione** — servirebbe a sapere **di quanto**
`piana` sarebbe stata peggiore, non **se**. **→ in coda.**

### ⚠ E LA DECISIONE PORTA IL SUO REGIME, come ogni numero di questo repo *(`9-bis`)*

`|dx|/d ≤ 0.053` è misurato a **`120` passi**, su **un seme**, con `--sep 4.0`. **Se un giorno
`|dx|/d` si avvicinasse a `1`, la saturazione di `tanh` comincerebbe a mordere e questa
decisione andrebbe RIFATTA, non difesa.**
**IL CRITERIO CHE LA RIAPRE, scritto ORA e non dopo** *(`par.10`: la condizione di retrocessione
si scrive al momento della promozione)*:
### **una quota NON NULLA di `|dx|/d > 0.5`.**

## 5. ❌ **PERCHÉ NON `exp(dx/u)`** — la variabile `log(d − LAM)`

La scelta «naturale» sarebbe far evolvere **liberamente** `log u`, cioè `u ← u·exp(dx/u)`.
**È SBAGLIATA, e il motivo è un conto:** vicino al confine `u → 0`, quindi **una spinta in su
piccola diventa un salto enorme** — `exp(a/u) → ∞`. **Una spinta LIMITATA produrrebbe uno
spostamento ILLIMITATO**, che è la firma di `A11`.

**Con `exp(dx/d)` non succede**, perché `d ≥ LAM > 0` **per legge**, quindi l'esponente è
**limitato da `|dx|/LAM`**.

> **Era una mia proposta, e Luca l'ha corretta prima che diventasse codice.** Sta qui perché
> **il codice di una via scartata non si cancella: e' l'evidenza che spiega perché esiste
> quella scelta** *(par.10)*.

## 6. I LIMITI, CLASSIFICATI CON `A11`

| limite | oggi | con la proposta |
|---|---|---|
| `max(0.0, 1.0 - LAM/base)` | **protegge il FATTORE** dal diventare negativo quando `d < LAM` — cioè **da uno stato che `E4-LAM` ora VIETA** | **SPARISCE**: `d ≥ LAM` è un invariante verificato **sempre**, quindi `1 − LAM/d ≥ 0` è **derivato** |
| `pos = prima > 0` | protegge da `d = 0` | **SPARISCE per la stessa ragione**: `d ≥ LAM > 0` |
| *(nuovo)* overflow di `exp` | — | **NESSUN CLAMP.** `|dx|/d ≤ |dx|/LAM`, e se mai superasse `709` è **`np.seterr(over='raise')`** a fermarsi **con la riga** — la stessa scelta di `E4-LAM` |

> **Due limiti spariscono e nessuno nasce**, e questa volta **l'ho verificato** invece di
> dirlo *(è l'errore di `Z142`)*: entrambi proteggevano da `d < LAM`, che **ora è un
> invariante**.

## 7. LA VERIFICA, **sulla FORMULA, col test di `Z113`**

**Non un run: un conto**, come `Z113`. Lo strumento deve mostrare:

| | che cosa | criterio |
|---|---|---|
| **`V1`** | **quanto vale `a`**, il passo tipico di rumore, **misurato** | è il numero che decide la condizione `a < LAM` del par.4 |
| **`V2`** | la deriva di **oggi** sotto rumore simmetrico | deve **riprodurre `Z113`**: `≈ +1.582e-03` con i suoi parametri |
| **`V3`** | la deriva della **proposta**, stessa `a`, stessi `d` | deve essere **del secondo ordine**: raddoppiando `a` deve **quadruplicare**, non raddoppiare |
| **`V4`** | la deriva della proposta **al confine** *(`d → LAM`)* | **→ 0**, mentre quella di oggi **→ `a/2`** |
| **`V5`** | la deriva della proposta **lontano** | decade come `1/d` in assoluto, `1/d²` in relativo |
| **`V6`** | **il caso che DEVE fallire**: la forma `exp(dx/u)` | deve **esplodere** vicino al confine, e il test lo deve **mostrare** |
| **`V7`** | **mai sotto `LAM`**: una discesa enorme, `dx = −100·d` | oggi **attraversa**; la proposta **no**, per qualunque passo |
| **`V8`** | **la DISTRIBUZIONE di `\|dx\|/d`**, non solo il suo tipico | è **il numero che decide fra piana e Itô**: `p50`, `p99`, `max`. Se `max ≪ 1` la non-monotonia di Itô **non si manifesta mai** |
| **`V9`** | **quante scritture hanno `\|dx\|/d > 1`, e quante `> 2`** | `> 1`: Itô **comprime**; `> 2`: Itô **inverte il verso**. **Se sono zero, la scelta è libera; se non lo sono, la piana è l'unica monotona** |

## 8. COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **che la deriva residua di secondo ordine sia TRASCURABILE.** So che è di second'ordine,
   nulla al confine e decrescente lontano. **Non so derivare che su `600` passi e `526` mila
   archi non si accumuli**: è una misura, non un teorema;
2. **il valore di `a`**, il passo tipico di rumore. **Senza, la condizione `a < LAM` non si può
   dichiarare vera** — ed è il punto `V1`;
3. **se la stessa forma vada applicata a `d0` come a `d`.** `_smorza` è chiamata per **entrambi**
   *(`quale` ∈ `{d, d0, d0_passo, …}`)*, e `d0` è una lunghezza di **riposo**: che debba obbedire
   alla stessa legge è **plausibile, non derivato**;
4. **chi spinge gli archi contro il muro.** La proposta toglie **il cricchetto del freno**, non
   la **causa** per cui gli archi ci arrivano. **Resta aperta e SEPARATA:** `D33` e `S05`.
5. ~~**se la SATURAZIONE di `tanh` a `2` si manifesti davvero**~~ — **RISOLTO il 2026-09-24**: **non si manifesta**, `max |dx|/d = 0.0531` su `125 731 076` campioni, **zero oltre `0.5`** *(par.4-quinquies)*. **Resta aperto `E[x²]`**, che non ho registrato e che direbbe **di quanto** `piana` sarebbe stata peggiore. Dipende da `\|dx\|/d`, che **non è
   misurato** — punti `V8`/`V9`. **Senza quel numero la scelta fra le due forme non ha una
   base derivata**, e resta di Luca;
6. **se una deriva NEGATIVA di quarto ordine sia preferibile a una POSITIVA di secondo.** È
   più piccola di ordini di grandezza, **ma va verso il muro** — e la domanda «chi spinge gli
   archi contro il muro» è un fronte aperto. **Più piccolo non è automaticamente meglio quando
   il SEGNO cambia.**

> **E la cosa più importante, che non va persa:** **questa cura NON elimina la deriva. La
> abbassa di un ordine e la annulla dove oggi è massima.** Dire *«il cricchetto sparisce»*
> sarebbe falso: `cosh(x) ≥ 1` sempre, quindi `E[Δu] ≥ 0` **sempre**. **Cambia l'ORDINE, non il
> segno.**

<!-- SCHEDA nome=scena-masse-coerenti funzioni=_semina_masse_coerenti,esegui_headless,_massa flag=_MC_VIDEO,TESTS,MASSE-COERENTI,SEMINA_LAM -->

> **→ NOTA DEL 2026-09-29, e sta qui perche' questa scheda POSSIEDE `esegui_headless`:**
> l'ultima riga del run headless ora stampa anche ### **l'elenco delle grandezze di STATO MAI
> APPARSE** *(`registro_mai_apparse`)*. ### **La scena non cambia, e non cambia un bit:** e' un
> **rendiconto** a run finito. **La legge sta nella scheda `registro-grandezze`**; qui sta solo
> il punto in cui viene stampato, perche' `REG-R` mappa **per funzione**.

# ③ `scena-masse-coerenti` — **LA SCENA `(ii)`: UN VUOTO SOLO, E LE MASSE SONO REGIONI**

**Decisione di Luca, 2026-09-25.** È una **SCENA**, non una legge: non entra in nessuna equazione
del passo. Sta nel registro perché **decide che cosa viene misurato**, e una scena sbagliata
produce numeri irreprensibili su un sistema che non è quello che si crede.

## LA FORMA

> ### **MASSA = REGIONE A FASE COERENTE IN UN VUOTO SOLO. LE MASSE NON AGGIUNGONO NODI.**

È la differenza con la scena di `CURA 2`, dove **ogni massa era una semina a sé** e il vuoto
**non c'era**.

## LA GEOMETRIA È DERIVATA DA UN SOLO INGRESSO, `--sep`

```
centri sul cerchio di raggio `sep`   ->  distanza fra centri adiacenti = sep*sqrt(3)
r  = (sep*sqrt(3) - R_CONN)/2        ->  IL VARCO FRA LE SUPERFICI È `R_CONN`:
                                         le regioni non si toccano e non si allacciano
                                         direttamente, ma il vuoto fra loro sì
Rv = sep + r + R_CONN                ->  un guscio di `R_CONN` oltre la regione più esterna,
                                         così nessuna regione tocca il bordo
fase, LA STESSA PER TUTTE E TRE = _dphi()/2  ->  il CENTRO del dominio.
                                                 Nel campo (`exp(1j*phi)`) e' la FASE ZERO.
                                                 ⚠ NON una fase per regione: masse sfasate
                                                   INTERFERISCONO, e sarebbe un effetto
                                                   messo dalla CONDIZIONE INIZIALE.
```

**Nessun numero scelto.** `R_CONN = 3*LAM` e `_dphi()` esistono già; il *«centro del terzo»* viene
da *«tre regioni, spaziate uguali»*.

## ⚠ LE DUE SCENE SONO LO STESSO CODICE CON `--sep` DIVERSO

| scena | `--sep` | `r_regione` | `raggio_vuoto` | `n` *(saturazione)* | nodi/regione | **ARCHI** | `QUOTA` |
|---|--:|--:|--:|--:|--:|--:|--:|
| **`(a)` «STESSO RAGGIO»** | `6.1158` | `4.096438` | `12.612238` | `12 802` | `411/413/413` | **`471 564`** | `0.0966` |
| **`(b)`** | `4.0` | `2.264102` | `8.664102` | `4 252` | `67/75/64` | **`148 237`** | `0.0484` |

*(un seme, `11`; `csv/_test_fork/_fumo_scena_ii.py`)*

**⚠ `(a)` SI CHIAMA «STESSO RAGGIO», NON «STESSA MATERIA»:** i `497` nodi per massa di `CURA 2`
stavano in un raggio `0.7 = 0.875 LAM`, dove ce ne stanno **`5`**. **Non c'è una materia da
conservare**, perché quella materia era **sotto la scala di Planck** (`A13`).

## I DUE BRACCI DI CONTROLLO, e senza di loro i criteri non si leggono

| criterio | braccio di controllo | perché |
|---|---|---|
| **`S10`** *(le regioni restano coerenti?)* | **`--mc-fasi-casuali`**: stessa scena, stesso seme, **fasi casuali anche dentro le regioni** | senza, il `~50 %` che `Lam` dà **per costruzione** si leggerebbe come mezzo successo. **Misurato: il controllo sta AL NULLO**, `0.071 / 0.035 / 0.032` |
| **`P-GONFIA`** *(quanto gonfia `d0`?)* | **la STESSA scena con `SEMINA_LAM` SPENTA**, **stesso `n` MISURATO** dal braccio acceso | il confronto con `CURA 2` è fra **scene diverse** e non attribuisce niente alla semina |

**⚠ `--mc-nodi` ESISTE PER QUESTO:** con `SEMINA_LAM` spenta **la saturazione non esiste**, quindi
il braccio di controllo **non può leggersi `n` da solo** e lo riceve.

## COSA LA SCENA RIFIUTA DI FARE *(`A9`)*

- **se la rete ha già nodi**: il vuoto dell'`import`/di `--nodi` **si sommerebbe** — **due vuoti,
  non uno**. Si lancia con **`--nodi 0`**, e **la rete non si svuota da sola**: svuotarla
  butterebbe via ciò che un altro flag ha chiesto, **senza dirlo**;
- **`conc_nodi` non viene toccato**: le regioni **non sono masse SEMINATE**, e marcarle come tali
  direbbe che il lignaggio viene da una semina che non c'è stata.

## ⛔ LO STATO: **IL GIRO DI 120 PASSI È SOSPESO** *(Luca, 2026-09-25)*

**La parte al PASSO ZERO si fa subito** *(`S1`-`S9`, previsioni `P1`-`P5`, numero di archi,
frazione di archi sotto `2 LAM`)*: **non dipende dalla mitosi.**
**Il giro resta sospeso** finché la **soglia della mitosi** non è una **legge derivata**: `3π` è
**un numero tarato a posteriori nell'epoca 1** — vedi la scheda `mitosi-schwinger` e `SCALE-TW`.

### ➕ `esegui_headless` NON assegna più i flag di cura *(2026-09-25)*

Le assegnazioni di `SEMINA_MATURA` e `MITOSI_2LAM` **erano qui**, e con il `global` in
`_applica_flag` erano **variabili locali inerti**. Ora `esegui_headless` tiene **solo** ciò che
è suo: `_MC_VIDEO` e `_NMASSE_VIDEO`, che sono **dizionari** e non hanno bisogno di `global`.
**La regola che ne esce: un flag di modulo si assegna DOVE sta il suo `global`, e mai altrove.**

### ➕ `CURA 5` E LA SCENA `(ii)`: la cura si accende dal driver *(2026-09-25)*

`--mitosi-2lam` passa da `esegui_headless` come tutti gli altri. **Nella scena `(ii)` il `77.23 %`
delle divisioni è già conforme**, quindi la cura **toglie il `22.77 %`** — e quelle divisioni
avvenivano **su archi corti**, cioè in regioni **diverse** dalle altre: **non è un campionamento
uniforme**, e va tenuto presente leggendo qualunque confronto fra i due bracci.

<!-- SCHEDA nome=accensione-campo funzioni=_pesi,_tempo_rampa,semina flag=SEMINA_MATURA,TAU_A,TAU_A_LOCALE -->

> ## ✅ **AGGIORNATA il 2026-09-25 — `RAMPA-1`, strada (3): IL VUOTO DATO HA ETA' INFINITA.**
> **LA LEGGE ORA E':** i nodi della semina iniziale (`maturi=True`) ricevono **`eta = +inf`**.
> **`ramp = min(1, eta/_tempo_rampa()) = 1` per sempre, qualunque `cs`.**
>
> ### PERCHE' LA FORMA PRECEDENTE ERA SBAGLIATA, e non e' un'opinione
> `eta = _tempo_rampa()` dava `ramp = 1` **esatto IN QUELL'ISTANTE**, e `ramp` e' un **rapporto
> fra due quantita' che si muovono entrambe**. **MISURATO** in configurazione del driver
> *(`csv/_test_fork/_perche_ramp_cala.py`)*:
>
> | grandezza | passo 0 (p50) | passo 1 (p50) | rapporto |
> |---|---|---|---|
> | `eta` — numeratore | `0.897802954` | `0.907802954` | **x1.011** |
> | `_tempo_rampa` — denominatore | `0.897802954` | `1.071554877` | **x1.196** |
> | `ramp` | `1.000000000` | `0.845601758` | **x0.846** |
>
> **Il denominatore corre 18 volte piu' del numeratore**, e al passo 1 solo **54 nodi su
> 4252** sono ancora a `1` (`_g_rampa_cali = 4198`).
> **CAUSA:** al passo 0 la cache `_cs_nodo_prev` **non esiste**, quindi il tempo-luce si
> calcola con `cs = CS_M = 2`; al passo 1 il `cs` vero e' **`p50 1.672`**, `cs_std/cs = 19.07 %`.
> **La maturita' era assegnata con un `cs` che il nodo non ha.** *(-> `RAMPA-2`, in coda: al
> passo 1 TUTTE le leggi che usano il tempo-luce o `cs` hanno lo stesso problema.)*
>
> ### DIMENSIONI E DOMINIO
> `eta` e' un **tempo** (`[T]`), e `+inf` e' un tempo **infinito**: dimensionalmente coerente.
> `ramp` resta in `[0, 1]` per costruzione (`min(1, ...)`); `inf/tr` con `tr > 0` finito da'
> `inf`, e `min(1, inf) = 1`. **`tr = 0` darebbe `nan`**, ma `tr = d_nodo/cs_nodo > 0` sempre
> *(`d >= LAM` per `A13`, `cs > 0` per `cs_floor`)*.
>
> ### `A11` — NESSUN LIMITE NUOVO, E UNO IN MENO
> **`+inf` NON e' un tetto ne' un pavimento:** e' l'assenza di una scala. E **spariscono** la
> chiamata a `_tempo_rampa()` alla semina **e le sue due diramazioni** (array / scalare), che
> esistevano solo per ricopiare il denominatore nel numeratore (`STANDARD 10`).
>
> ### COSA LEGGE E COSA SCRIVE
> **scrive** `self.eta[_a:_b] = np.inf` (i soli nodi del vuoto dato, l'intervallo
> `_cura4_maturi` fissato da `semina`). **Non legge niente**: e' proprio il punto — prima
> leggeva `_tempo_rampa()`, cioe' `d` e `cs` di quell'istante.
> **I nati in dinamica NON sono toccati**: `eta = 0` a `:2720`, `:2723`, `:6022`, `:6178`, e
> salgono con la rampa del tempo-luce. **La maturita' e' del VUOTO DATO, non si eredita.**
>
> ### `+inf` E' UN VALORE SPECIALE: LE SUE LETTURE SONO VERIFICATE **PER AST**
> `csv/_letture_eta.py` -> `doc/LETTURE_eta.md`: **17 occorrenze** nel simulatore, e le uniche
> **due** letture dentro una legge sono **`:3419`** *(il torque pesato)* e **`:3684`** *(`_pesi`)*,
> **nessuna delle due e' una riduzione**. L'unica riduzione e' **diagnostica** (`_stat` delle
> colonne `eta_*` in `_diag_completa`), adattata a parte.


# ④ `accensione-campo` — **QUANDO UN NODO DIVENTA SORGENTE DI CAMPO**

**`CURA 4`, decisione di Luca, 2026-09-25. Flag `SEMINA_MATURA`, OFF di default.**

## LA LEGGE

```python
_pesi:   ramp = min(1, eta / _tempo_rampa())
         base = exp(-d/lam_archi) * ramp[i] * ramp[j]
```

> ### ❗ **`ramp` ENTRA COME PRODOTTO DI DUE NODI: IL PESO D'ARCO VA COME `ramp²`.**

`_tempo_rampa()`: **`TAU_A` a flag spento** *(byte-identico)*, **`_tempo_luce_nodo` a flag acceso**.

## IL DIFETTO CURATO, misurato

| | |
|---|---|
| **tutti** i nodi nascono con `eta = 0` | `semina` `:2645`, `mitosi` `:5831`, Schwinger `:5987` — **lo stesso zero** |
| al passo zero la somma dei pesi è | **`0.000000e+00` ESATTO** |
| passi perché `ramp = 1` | **`TAU_A/DT = 5000`** |
| al passo `120`, `ramp` | `0.024` — e il **peso d'arco `5.76e-04`**, **una parte su `1736`** |

**TUTTI i giri corti fatti finora hanno girato in quel regime**, `CURA 2` compresa.

## LA CURA, in due metà

1. **i nodi della SEMINA INIZIALE nascono MATURI:** `eta = _tempo_rampa()`, che dà
   `ramp = min(1, eta/tempo) = 1` **ESATTO**. **Nessun numero nuovo:** il valore è *la grandezza
   stessa che sta al denominatore*.
2. **la rampa resta per i nati in dinamica**, col tempo **`_tempo_luce_nodo`** invece di `TAU_A`.
   Misurato: **`89.8` passi** *(`p05 86.6` / `p95 92.2`, cioè `±3 %`)* contro `5000`.

> ### ✅ **E COSÌ I DUE RUOLI DI `TAU_A` SI SEPARANO.**
> Oggi `TAU_A` è **insieme** la **vita media della memoria spinoriale** *(`:3334`, ed è per
> **quello** che il `50` fu scelto: *«alta persistenza memoria spinoriale»*, *«per non far
> divergere `omega`»*)* **e** il **tempo di accensione di una sorgente** *(`_pesi`)*.
> **Nessuna ragione, scritta da nessuna parte, perché coincidano.**
> **Col flag ON `TAU_A` resta SOLO il primo**, e `A7` lo verifica **dall'AST**.

## ❗ LA DISTINZIONE «INIZIALE» / «IN VOLO» — **il codice non l'aveva, e va dichiarata**

```
semina(..., maturi=True/False)   -> lo dice il CHIAMANTE, esplicitamente
semina(..., maturi=None)         -> DEFAULT: matura SE LA RETE ERA VUOTA (`base == 0`)
```

> **`base == 0` NON È UNA SOGLIA: è un fatto topologico** — prima non c'era niente.
> Un criterio temporale *(«prima del passo 1»)* sarebbe **un numero nuovo** *(par.3, `A11`)*.
>
> **⚠ IL LIMITE:** una scena che seminasse **due volte** avrebbe la **seconda** trattata come
> «in volo». **Per questo il parametro esplicito esiste**: chi vuole due semine iniziali passa
> `maturi=True` **e lo dichiara nella scena**.

## ✅ `eta` È IL MARCATORE, E NON SERVE UN ARRAY NUOVO

**nato in dinamica → `eta = 0`; nato come vuoto DATO → `eta` tale che `ramp = 1`.**
`eta` **esiste già**, è **già estesa a ogni sito di nascita** ed è **già nello snapshot**.
**Così non si crea il settimo array da estendere a mano** — la famiglia di difetti di
`_cs_nodo_prev` *(`71.88 %`)* e `_psi_spin_prec` *(`95.33 %`)*.

**E LA MATURITÀ SI SCRIVE DOPO `_allaccia`**, non prima: `_tempo_luce_nodo` ha bisogno degli
**archi** per costruire `d_nodo`.

## ➕ IL CONTATORE DEI **CALI** DI `ramp` *(rilievo di Luca, 2026-09-25)*

❌ **`_g_rampa_sotto1` NON misura ciò che serve:** conta quanti nodi hanno `ramp < 1`, **che
include un nodo GIOVANE non ancora arrivato a `1`**. **Un CALO è un'altra cosa.**

```
_g_rampa_cali         quante volte un `ramp` per nodo e' SCESO rispetto al passo prima
_g_rampa_calo_somma   la somma dei cali ("di quanto", cumulativo)
_g_rampa_calo_max     il calo singolo PIU' GRANDE
_g_rampa_calo_quando  l'indice dell'ULTIMA invocazione in cui e' calato
```

**Serve un array `_g_rampa_prec`, e lo dichiaro DIAGNOSTICO:** il suo disallineamento **si conta e
si riparte** *(`_g_rampa_prec_disallineata`)* invece di essere esteso a mano a ogni sito di
nascita. **NON è la famiglia di `_cs_nodo_prev`**, che stava su un percorso **fisico**: qui se il
confronto salta **si perde una MISURA, non una legge**.

## ⚠ `A11` — **NON È MONOTONO, E SI MISURA INVECE DI NASCONDERLO**

`_tempo_luce_nodo` dipende da `d` e da `cs`, quindi **cambia a ogni passo**: se gli archi di un
nodo si allungano, `ramp` **può SCENDERE**.
**È voluto:** è una legge locale che segue lo stato locale, come `_ttw = 2π/|Δω|`.
**L'alternativa — congelare il tempo-luce alla nascita — richiederebbe un array di stato nuovo**
per nodo, con la sua estensione alla mitosi, allo Schwinger e allo snapshot: **esattamente il
difetto che si vuole evitare.**
**Contatore: `_g_rampa_sotto1` / `_g_rampa_nodi`.** E i rami di fallback *(nessun arco, forma non
combaciante)* sono **dichiarati e contati** *(`A8`)*.

## I CRITERI, fissati nel TASK HISTORY **prima** del codice

*(`doc/TASK_HISTORY/2026-09-25_cura-accensione-campo.md`, commit `30db901`, **antenato** del
commit del codice — par.5-septies: l'ordine è verificabile da git)*

| | criterio |
|---|---|
| **`A1`** | **flag SPENTO = BYTE-IDENTICO** al codice precedente, firma dei byte, un processo per braccio |
| **`A2`** | al passo `1`, **`ramp == 1` su TUTTI** i nodi della semina iniziale, **ESATTO** |
| **`A3`** | un nodo nato da **MITOSI** parte da `ramp = 0` e arriva a `1` **nel suo tempo-luce** |
| **`A4`** | contrasto massa/vuoto e `Lam` al passo `1`, contro **`P2 = 27`** e **`P3 = 5`** |
| **`A5`** | **CONTROLLO POSITIVO:** ON e OFF **DEVONO** differire |
| **`A6`** | **CASO CHE DEVE FALLIRE:** con `maturi=False` forzato, **`A2` deve dare FAIL** |
| **`A7`** | **`TAU_A` non è più letto da `_pesi`** — dall'**AST**, non da un `grep` |

**⚠ `A3` FORZA LA MITOSI**, perché la soglia `3π` è **irraggiungibile** *(`SCALE-TW`:
`max|tw| = 2.8991 π`)*: **senza forzarla `A3` non avrebbe nulla da misurare**, e va detto invece
di far sembrare che scatti da sé.

## ⛔ COSA RESTA APERTO

- **la stabilità col campo acceso dal passo zero.** `G_PH = 3e-3` è dichiarato *«vicino al limite
  di divergenza»* *(`1e-4` e `0` divergono)*. **Se diverge è un RISULTATO**, da committare e
  fermarsi.
- **la rimisura di `|dx|/d` a campo maturo:** la forma del freno-legge `(1+tanh)` fu decisa su
  `max |dx|/d = 0.0531` **a campo spento**. **È il passo dopo il sigillo.**

---

<!-- DA-CLAUDE-MD-2026-09-26:par.4 -->

> *(Era **`CLAUDE.md` par.4** fino al riordino del 2026-09-26. **Verbatim**, dal tag `regole-pre-riordino`. La storia di quella sezione sta in `doc/STORIA_REGOLE.md`.)*

## 4. REGOLE FISICHE DA NON VIOLARE
- **U_ij resta in SU(2):** costruiscilo/evolvilo NELL'ALGEBRA di Lie (exp, slerp/geodetica), MAI
  come blend lineare di matrici (uscirebbe da SU(2)). Questo protegge unitarieta' **E**
  elettromagnetismo (la fase globale U(1)/segno vive separata: SU(2) ha det=1, non la tocca).
- **Freccia causale spinore -> link:** i nodi guidano, gli archi ricordano. Se in un test gli
  spinori diventano passivi (il link li comanda) -> BUG, da rilevare, non l'obiettivo.
- **Integratore:** VERLET (leapfrog) solo per il SECOND'ordine con inerzia (xddot: fasi, spinori,
  metrica). Per il RILASSAMENTO di primo ordine (xdot: memoria del gauge Strato 1/2) usa il passo
  ESATTO `U(t+dt) = U_target + (U-U_target) e^{-dt/tau}`, NON Verlet. Se ti chiedo Verlet su un
  rilassamento, segnalalo invece di eseguire.
- **`--cs-dinamico` CI VA SEMPRE (decisione di Luca, 2026-09-15).** Non e' un'opzione di scenario:
  **senza, `cs = CS_M` costante e `_cs_nodo_prev` non viene MAI scritta**, quindi cade anche il
  `tau = d/cs` dello **STRATO 1** (`_bloch_ritardato`), non solo quello di `--tau-luce`: **tutta la
  memoria del fork gira su una legge amputata.** Una misura senza `--cs-dinamico` **non misura il
  sistema che si crede di misurare**, ed e' successo (`doc/REPERTO_cs_dinamico_spento.md`).
  **NB, e non cambia la regola:** alle densita' simulabili `cs` varia pochissimo — misurato
  `cs \in [1.99954, 2.0]`, cioe' **0.023%**, che pesa **0.00629%** della dispersione di `tau = d/cs`
  (una parte su **15 898**). **Il punto non e' l'ampiezza: e' che la legge dev'essere CABLATA.**
  Un `cs` costante non e' un `cs` piccolo: e' un `cs` **assente**, e rende `tau = d/cs` un
  `tau ∝ d` travestito.
- **Dipendenza di flag:** `--cs-dinamico` implica `--chi-core` e `--spinore-vivo` (senza, e' inerte/incoerente).
- **Mai confronti a PASSO FISSO su un sistema che si espande/dilata:** genera ALIASING (una struttura
  che trasla o si dilata, campionata a intervalli costanti, sembra ferma o va a velocita' falsa).
  Campiona in modo adattivo o normalizza sulla scala (comovente), non su intervalli assoluti.
- **LOCALE PURA — niente sottrazione della media:** mai togliere la media globale (spinta.mean(),
  flusso.mean(), ...). La media globale introduce NON-LOCALITA' (una scorciatoia che il sistema
  relazionale non deve avere). Tutto agisce per arco/vicinato. La media NON va qui.

<!-- DA-CLAUDE-MD-2026-09-26:par.4 FINE -->


---

<!-- SCHEDA nome=aggiornamento-sincrono funzioni=step,_passo_spinoriale,_applica_flag flag=SYNC_UPDATE -->
# ㉕ L'AGGIORNAMENTO SINCRONO — **`SYNC_UPDATE` / `--sync`**, e perché è **archiviato**

> ### **STATO: `ARCHIVIATA`** *(2026-09-27, passo `(b)2` di `ETC-PASSO`)*.
> **`--sync` resta ACCETTATO come no-op che si dichiara.** I rami sono in
> `csv/_archivio/_sync_update.py`, tag **`pre-archivio-sync`**, blob `f845d30d`.
>
> ### ⚠ **E LA SCHEDA NASCE ADESSO, che è tardi.** `SYNC_UPDATE` è vissuto nel simulatore senza
> una scheda propria: `H-REG-R` l'ha imposta **nel commit che lo archivia**. **Una legge senza
> scheda è una legge che nessuno ha dovuto scrivere in forma chiusa** — ed è esattamente il modo
> in cui, dice il presidio, sono nati `D01`-`D33`.

## LA FORMA che dichiarava

Il commento del flag diceva: *«`dph` (il ponte fase→twist/metrica) legge la fase dallo **SNAPSHOT**
di inizio passo, non da quella appena aggiornata. Così pesi materia e `dph` vedono la **STESSA**
fase (`t-1`): il passo diventa coerente e **indipendente dall'ordine di aggiornamento (Jacobi
invece di Gauss-Seidel)**. Il cuore simplettico (`phivel→phi`) resta sequenziale.»*

**In formula:** dato lo stato `S(t)`, ogni legge `L_k` calcola `L_k(S(t))` — non `L_k(S'(t))` con
`S'` già mosso dalle leggi precedenti — e le scritture si applicano insieme.
**Dimensioni:** nessuna grandezza nuova; è una regola sull'**ordine di lettura**, non sui valori.
**Limiti (`A11`):** non introduceva né `clip` né pavimenti.

## ✅ PERCHÉ È ARCHIVIATA, e non è un ripudio della forma

### **La forma era giusta. Il RAGGIO era un quinto del passo.**

| dove | usi di `SYNC_UPDATE` |
|---|---|
| `_passo_spinoriale` | **7** |
| `step` | **6** |
| `_applica_flag`, modulo, `batch_condensazione` | 4 + 1 + 1 |
| ### `scuoti_vuoto` · `mitosi` · `rilassa_disegno` · `memoria_hebbiana_moto` | ### **0** |

**E il numero che decide:** delle **56** letture miste `t`/`t+1` misurate dall'AST nella FASE 0 di
`ETC-PASSO`, ### **tutte e 56 stavano FUORI dal suo raggio** — compresa l'unica di `step`, che viene
da `scuoti_vuoto`.

> ### **Quindi `--sync` non era una cura parziale di un difetto: era una cura di un difetto
> DIVERSO.** Rendeva Jacobi l'**interno** di `step`, mentre le letture miste stanno **fra le
> leggi**. **`ETC-PASSO` non lo estende: lo sostituisce sul passo intero**, ed è per questo che
> archiviarlo **non lascia scoperta** nessuna proprietà.

## MISURATO, prima di toccarlo

**`--sync` AGIVA** — non era già inerte, e questo va detto perché è ciò che rende l'archiviazione
una **decisione** e non una pulizia: su scena `(ii)(a)`, seme `11`, 3 passi,
### **19 grandezze su 23 differivano** fra `--sync` acceso e spento.

**Conseguenza per chi legge numeri vecchi:** ### i run fatti con `--sync` **non si confrontano** con
quelli di oggi **senza dirlo**.

## ⚠ DUE CONFUSIONI DA NON FARE

| | |
|---|---|
| ### **`SYNC_SPINORE` NON è `SYNC_UPDATE`** | `_forza_sync`, `_wI_sync`, `_uno_sync` sono gli ingredienti del **torque `SU(2)`** e **restano vivi**. Due flag con `SYNC` nel nome, **due leggi diverse** *(scheda `torsione-spinore`)* |
| **`_phi_t` NON era suo** | la fotografia della **fase** la legge **il percorso vivo** — `z = np.exp(1j*_phi_t)` — e **resta** |

## E UNA LEGGE CHE PERDE UN'ECCEZIONE

`if SCUOTIMENTO and not SYNC_UPDATE` → ### `if SCUOTIMENTO`.
**Lo scuotimento del vuoto sullo spinore ora agisce SEMPRE**, e **non è una legge nuova: è la
stessa senza l'eccezione**. Il suo commento lo chiedeva già: *«le due leggi devono essere identiche
— il vuoto è lo stesso vuoto»*.
**`9-ter`: il numero delle leggi SCENDE** — 7 blocchi condizionali e 9 ternari in meno, **zero
aggiunti**.

---

<!-- SCHEDA nome=scuotimento-vuoto funzioni=scuoti_vuoto,lambda_vuoto flag=SCUOTIMENTO,CALORE_VETTORIALE,RUMORE_COLORATO -->

> ### ⚠ **COMMIT 0-bis — `SCUOTIMENTO` *NON* SEGUE IL REGIME, e il commento diceva che lo segue**
> *(2026-10-01, `REGIME-COMMENTI`. E' un fatto di FISICA, non una svista di testo.)*
>
> **Il commento diceva:** *«legge dello scuotimento (segue `REGIME`; `True` in stocastico)»*.
>
> | dove | che cosa fa davvero |
> |---|---|
> | il **ramo di modulo** *(sempre eseguito)* | mette `_SCUOTIMENTO_REGIME = True` ### **in ENTRAMBI i rami** — deterministico **e** stocastico. ### **Quindi da qui `SCUOTIMENTO` vale SEMPRE `True`, qualunque sia `REGIME`.** |
> | `_applica_regime` *(solo se `--regime` e' passato)* | mette ### **`SCUOTIMENTO = False`** per il deterministico |
>
> ### ➜ **LO STESSO NOME DI REGIME DA' DUE SISTEMI DIVERSI, a seconda che il flag sia stato
> passato o no.** ### **E il vuoto acceso o spento non e' un dettaglio: e' il termostato e la
> sorgente di asimmetria.**
> **E' la trappola `--regime`, gia' repertata**, e ### **i due strumenti che passano
> `--regime deterministico`** *(`_osserva_vuoto.py`, `_sigillo_osservatore.py`)* ### **lo fanno
> PROPRIO per questo**: `O2` e' un A/B a **variabile singola** che cambia **solo**
> `SCUOTIMENTO`.
> ### ⚠ **Quindi <<il run di default>> e <<il run con `--regime deterministico`>> NON sono lo
> stesso sistema**, e un confronto fra misure prese nei due modi ### **non e' un confronto a
> variabile singola.**
# ㉖ LO SCUOTIMENTO DEL VUOTO — **`scuoti_vuoto`**, la **prima** legge del passo

> ### 🏗 **T1, 2026-09-28: l'apertura del passo non sta piu' qui**
>
> In `(c)1` **questa legge apriva il passo**, perche' e' la prima dell'ordine canonico, e
> l'apertura stava **prima della guardia** `if not SCUOTIMENTO ... return`. ### **Ora la fa lo
> SCHEDULATORE**, e la domanda *<<e se la prima legge esce subito?>>* **non esiste piu'**: il
> passo comincia prima che una legge possa uscire.
> **La legge dello scuotimento non e' toccata**, e resta vero il fatto che rendeva `(c)1`
> byte-identico: ### **`scuoti_vuoto` scrive `phivel` e nient'altro.** *(Scheda
> `schedulatore-del-passo`.)*


> ### ⚠ **LA SCHEDA NASCE IL 2026-09-27, E NASCE TARDI.** `scuoti_vuoto` è **la prima delle cinque
> leggi del passo pieno** e **non aveva una scheda**: `H-REG-R` l'ha imposta nel commit `(c)1` di
> `ETC-PASSO`. **Una legge senza scheda è una legge la cui forma nessuno ha dovuto scrivere
> chiusa**, ed è il modo in cui — dice il presidio — sono nati `D01`-`D33`.

## LA FORMA, letta dal codice

Per **arco** lo stress metrico, per **nodo** la sua media sui vicini, e da lì l'ampiezza:

```
stress_arco(e) = |d(e) - d0(e)| / max(d0(e), 1e-6)
stress_nodo(k) = ( SUM_{e: k in e} stress_arco(e) ) / max(grado(k), 1)
ampiezza(k)    = sqrt( stress_nodo(k) + 1e-9 ) * sqrt(Lam) / ( 1 + I2(k)/Lam )
calcio(k)      = N(0,1) * ampiezza(k)            [ * perc_chi(k) se CALORE_VETTORIALE ]
phivel(k)      += calcio(k)
```

con `Lam = lambda_vuoto(net)` *(l'energia del vuoto, dinamica)* e `I2 = |psi|²`.

## CHE COSA LEGGE E CHE COSA SCRIVE

| | |
|---|---|
| **legge** | `d`, `d0` *(per arco)*, `psi` → `I2`, `perc_chi`, `rng`, `n`, `i`, `j`, `_deg` implicito nel grado ricalcolato |
| ### **scrive** | ### **`phivel` e NIENT'ALTRO** |

### **È il fatto che rende `(c)1` byte-identico:** fra `scuoti_vuoto` e `step` **non c'è nessuna
scrittura di `d` o `d0`**, quindi spostare la fotografia da `step` a `scuoti_vuoto` **non cambia la
fotografia**. *(E il sigillo di `(c)1` lo verifica invece di fidarsi di questa riga.)*

## DIMENSIONI

`stress` è **adimensionale** *(un rapporto di lunghezze)*; `Lam` ha le dimensioni di `|psi|²`,
quindi `sqrt(Lam)` quelle di `|psi|`; `ampiezza` esce in unità di `phivel`, cioè **fase su tempo**.
**Nessuna costante con dimensioni scelte a mano.**

## LIMITI, classificati con `A11`

| sito | forma | natura |
|---|---|---|
| `max(d0, 1e-6)` | denominatore | **anti-zero** |
| `max(grado, 1.0)` | denominatore | **anti-zero** *(un nodo isolato)* |
| `sqrt(stress + 1e-9)` | dominio di `sqrt` | **condizione di esistenza** |
| `1/(1 + I2/Lam)` | soppressione | ### **non è un limite: è la LEGGE** — dove c'è materia coerente il vuoto non scuote |

### **Nessun `clip`, nessun pavimento, nessun tetto.** *(Verificato con `CLIP-INVENTARIO`.)*

## LA COSA CHE VA DETTA, e non è una critica alla legge

> **`SCUOTIMENTO` è il flag che la accende, e la guardia `if not SCUOTIMENTO ... return` sta
> DOPO l'apertura del passo** *(cura `(c)1`)*: **se la prima legge esce subito, il passo deve
> cominciare comunque.** Prima di `(c)1` la fotografia si apriva in `step`, e questa domanda non
> esisteva.

**E `RUMORE_COLORATO`** *(taglio spettrale, `tau_c = LAM/CS_M`)* **agisce sul `calcio`**: da `(b)2`
**agisce sempre**, perché il percorso `not SYNC_UPDATE` è diventato l'unico *(scheda
`aggiornamento-sincrono`)*.

---

<!-- SCHEDA nome=rilassamento-disegno funzioni=rilassa_disegno flag=L_CONSERVA,EMB_IT,EMB_ETA -->
# ㉗ IL RILASSAMENTO DEL DISEGNO — **`rilassa_disegno`**, e **`A3-DISEGNO`**

> ### 🗄 **`L_CONSERVA` E' ARCHIVIATO** *(2026-09-28, strada (b) scelta da Luca)*
>
> `_togli_rotazione_rigida` e il ramo che lo chiamava sono in **`csv/_archivio/_l_conserva.py`**
> *(tag `pre-archivio-lconserva`)*, e con loro la variabile `pos0`, che non aveva piu' lettori.
> **Il codice stesso lo marcava <<ERRATA, NON usare>>:** azzerava **tutta** la rotazione rigida a
> ogni passo e **distruggeva la PRECESSIONE FISICA REALE** *(`L_z ~ -0.9`, verso coerente
> all'84 %)*. ### **Conservare `L` non e' annullare la rotazione.**
> ### ➜ **E LA RAGIONE CHE L'HA FATTO USCIRE ADESSO E' IL TIPO.** La catena
> `rilassa_disegno -> _togli_rotazione_rigida -> calcola_psi` faceva scrivere `psi` e `psi_spin`
> a una legge di tipo **`disegno`**, che dice *<<scrive solo `pos`>>*. **La verifica statica dei
> tipi l'ha trovato, e Luca ha scelto di archiviare invece di cambiare il tipo:**
> ### **ora il tipo e' VERO PER COSTRUZIONE invece che scusato.** La verifica passa **8/8**.
> **⚠ E IL RAMO AGIVA, misurato PRIMA di toglierlo:** acceso contro spento, ### **17 grandezze su
> 23 DIVERSE**. **Non e' una pulizia: e' una decisione.**
> **`L_CONSERVA` non e' stato tolto** *(decisione 3)*: e' un **no-op accettato**, e **non ha
> nemmeno un flag CLI** -- per accenderlo si modificava il sorgente.
> **E porta con se' `H-ETC-1`:** quel ramo conteneva la `calcola_psi()` di `:6529`, **l'unica degli
> 8 siti in un ramo morto**. Ora sono **7, tutte vive**, e il conto dice **una cosa sola invece di
> due**.


> ### 🏗 **T1: il disegno non apre piu' il passo**
> **`T1`, 2026-09-28: l'apertura del passo NON sta piu' qui.** La fa lo **SCHEDULATORE**
> (`esegui_passo`), in testa alla composizione, e **l'idempotenza di `(c)1` non serve piu'** --
> il compositore **sa** di essere il primo. **Misurato:** `_g_smp_gia_aperta` passa da **4 per
> passo** a ### **0**. *(Scheda `schedulatore-del-passo`; tag `pre-schedulatore-t1`.)*
>
> **E' la legge che meno c'entra col confine del freno** -- scrive `pos` e **zero stato fisico** --
> e in `(c)1` doveva comunque chiamare l'apertura, perche' **una permutazione poteva metterla per
> prima**. ### **Con lo schedulatore quel dovere sparisce**, e resta solo il fatto che conta:
> **questa non e' una legge del passo fisico**, ed **esce dalla sequenza in `T4`**.


> ### ⚠ **ANCHE QUESTA SCHEDA NASCE IL 2026-09-27**, imposta da `H-REG-R` nel commit `(c)1`.
> **È la quarta delle cinque leggi del passo, e non aveva forma scritta.**

## LA FORMA

Le coordinate **inseguono** le distanze relazionali. Per `it = EMB_IT` iterazioni:

```
v(e)    = pos(j) - pos(i)                   L(e) = max(|v(e)|, 1e-9)
corr(e) = ((L(e) - d(e)) / L(e)) * v(e) * 0.5
acc(k)  = ( SUM_{e: i=k} corr(e) - SUM_{e: j=k} corr(e) ) / deg(k)
pos     += EMB_ETA * clip(acc, -0.5, +0.5)
pos     -= mean(pos)                        # il baricentro resta nell'origine
```

## ⛔ CHE COSA **NON** È

### **NON è fisica: è il DISEGNO.** `pos` non è una grandezza del sistema relazionale — è la
**proiezione** che rende visibile `d`. Il sistema vive su `(i, j, d)`.

> ### 📌 **E qui sta `A3-DISEGNO`, che è un difetto APERTO e non di questa scheda:**
> `pos`, scritto qui, **è riletto dalla FISICA** — `memoria_hebbiana_moto:6622` **senza nessuna
> guardia** *(→ `grad_tw` → `mem_mot` → il blocco `GRAV_BIFASE`)* e `:7010` *(→ `dir_radiale` → con
> `MEM_MOTO_TUTTO` **scrive `self.phi`**)*.
> **La cura `ETC-PASSO` NON lo chiude**, e non deve fingere di farlo: congelare `pos` nella
> fotografia rende la dipendenza **sincrona**, **non la toglie**. **Un difetto reso ordinato resta
> un difetto**, ed è la cura **(c)** dell'elenco *(voce `A3-DISEGNO`)*.

## CHE COSA LEGGE E CHE COSA SCRIVE

| | |
|---|---|
| **legge** | `pos`, `i`, `j`, `d`, `_deg`, `n` |
| **scrive** | ### **`pos` e nient'altro** *(più `psi` e `psi_spin` se qualcosa a valle le ricalcola: vedi `PSI-FLASH`)* |

## LIMITI, classificati con `A11`

| sito | forma | natura |
|---|---|---|
| `max(|v|, 1e-9)` | denominatore | **anti-zero** |
| `clip(acc, ±0.5)` | ### **TETTO FISICO** | ### **è un limite su quanto il disegno può muoversi in un'iterazione** |
| `nan_to_num(pos)` | difesa | **non è un limite: è una toppa su un `NaN`** — e `A11` dice di **cercare l'errore** |

> ### ⚠ **I due ultimi sono in `CLIP-INVENTARIO` come TETTI FISICI del disegno**, ed è il posto
> giusto: **stanno fuori dalla fisica**, quindi toccarli **non cambia il sistema** — cambia solo
> come lo si vede. **Per questo NON sono nella famiglia da archiviare.**

## `L_CONSERVA`

Il ramo che sottrarrebbe la **rotazione rigida spuria** *(conservazione del momento angolare del
disegno)*. ### **`L_CONSERVA = False` a runtime, e il codice lo marca «ERRATA, NON usare»:** il
ramo è **morto**, e con lui la chiamata `calcola_psi()` di `:6529` che `H-ETC-1` conta fra le 8.
**È l'unico degli 8 siti senza `w` che sta in un ramo morto**, e la scheda lo dice **perché il conto
di `H-ETC-1` non vada letto come «8 problemi vivi»**.

---

<!-- SCHEDA nome=leggi-in-uso funzioni=_applica_regime,_avvisa_leggi_in_uso flag=VERLET,REGIME -->

### **AGGIORNAMENTO del 2026-10-04, commit `6b`** *(questa scheda possiede
`_avvisa_leggi_in_uso`)*: **`MITOSI_2LAM` entra fra i `[flag-inerti]`**, come `PAV_COM`,
`L_CONSERVA` e `SYNC_UPDATE`. La voce dice **dove e' finito il suo ramo**
*(`csv/_archivio/_rami_off_cura2.py`)*, perche' ### **un flag che non fa niente e che
qualcuno accende e' un'ASPETTATIVA TRADITA**, non un dettaglio.
### ⚠ **E il flag RESTA, non si toglie** *(decisione 3 di Luca: si conserva tutto)*: il
driver continua a passarlo. ### **La legge e' nella scheda `mitosi-schwinger`.**

# ㉘ LE LEGGI IN USO — **`VERLET` e il `REGIME` deterministico**, e l'avviso che le sorveglia

> ### 🚩 **E ORA AVVISA ANCHE SUI FLAG INERTI ACCESI** *(2026-09-28)*
>
> `[flag-inerti]`: se un flag **inerte** e' **acceso**, lo dice e **nomina l'archivio** --
> `L_CONSERVA`, `PAV_COM`, `SYNC_UPDATE`. ### **Un flag che non fa niente e che qualcuno accende
> e' un'ASPETTATIVA TRADITA, non un dettaglio.**
> **⚠ E' un AVVISO, non un presidio** (`A9`), come l'altro che vive in questa funzione.
> **⚠ E il suo limite, dichiarato:** legge le costanti **al momento della configurazione**. Chi le
> imposta **dopo** *(per esempio `--flag=` di `csv/_test_fork/_hashseed_prova.py`)* **non lo fa
> scattare** -- e in quel caso e' chi lancia che sa cosa sta facendo.


> ### **DECISIONE DI LUCA, 2026-09-27:** *«`VERLET` e `REGIME` deterministico si TENGONO COME SONO.
> Nessuna archiviazione, nessun cambiamento. **L'importante è che siano USATI.**»*

## CHE COSA SONO, e la forma

| | |
|---|---|
| **`VERLET`** | il sottociclo metrico integra `d`/`vd` con **Velocity-Verlet (secondo ordine)** invece di Eulero esplicito. `vd_half = vd + ½·dts·acc(t)`, poi `d_new`, poi `acc(t+dt)`, poi `vd = vd_half + ½·dts·acc_next`. **È il percorso vivo**, e `REGISTRO_FISICA` impone già *Verlet solo sul second'ordine* |
| **`REGIME`** | **non è un flag: è un INTERRUTTORE COMPOSTO.** `"deterministico"` fissa **quattro** cose insieme — `SCUOTIMENTO`, `G_PH = 3e-3`, `TAU_A = 50.0`, `_CALORE_INIT = 0.4` — contro `"stocastico"` che dà `0.15`, `2.0`, `0.0` |

> ### ⚠ **E qui c'è una cosa che va detta sulla PROMOZIONE.** Il par.10 chiede **tre** criteri per
> promuovere una componente a fisica di default: **derivata e non tarata**, **sigillata col
> controllo positivo**, e **la sua assenza è un difetto**. ### **Qui il criterio è LA DECISIONE DI
> LUCA**, e va scritto in chiaro: sono leggi in uso **per decisione**, non perché una misura le
> abbia mostrate migliori.
> **`CENS-B8` resta aperta e dice proprio questo:** la **deriva d'energia del ramo Eulero non è MAI
> stata misurata**. La decisione di tenere Verlet **non la misura**: la rende una legge in uso.
> **E `COMPONENTI:C3` dice che `--regime` cambia quattro interruttori insieme**, cioè che non è
> isolabile: un A/B sul regime **non è un A/B su un meccanismo**.

## L'AVVISO — `_avvisa_leggi_in_uso()`

Se il run **non** usa `VERLET`, oppure **non** è in regime `deterministico`, **lo dice in chiaro**
all'avvio, nominando la voce d'indice *(`CENS-B8`, `COMPONENTI:C3`)*.

### ⚠⚠ **È UN AVVISO, NON UN PRESIDIO** (`A9`): **non impedisce niente.**
Luca l'ha chiesto così — *«avviso, non blocco»* — e **chi conta i presidi non lo deve contare fra
loro**: vale quanto l'attenzione di chi legge lo stdout. **Un avviso presentato come presidio
sarebbe esattamente il difetto che `A9` esiste per intercettare.**

## DOVE STA, e perché non in `_applica_flag`

`--regime` si applica in **`_applica_regime`**, che gira **DOPO** `_applica_flag`. Un controllo
messo là leggerebbe il `REGIME` **di testa al file** e non quello del run: ### **direbbe la cosa
sbagliata proprio quando conta.**
**E sta su ENTRAMBI i rami** di `_applica_regime`: il ramo senza override faceva un `return` secco
che l'avrebbe **saltato nel caso più comune** *(nessun `--regime` sulla riga di comando)*.

## COLLAUDO, girato a tre casi

| caso | esito |
|---|---|
| argv del driver | *«VERLET attivo e REGIME deterministico: le leggi in uso ci sono»* |
| `VERLET` spento | avvisa **1**, e nomina `CENS-B8` |
| `VERLET` spento **e** `--regime stocastico` | avvisa **2**, e nomina i **quattro** interruttori |

## LIMITI, `A11`

**Nessuno:** la funzione **stampa** e non scrive stato. Il costo è una stampa per run.

---

<!-- SCHEDA nome=schedulatore-del-passo funzioni=esegui_passo,valida_composizione,update,_passo,batch_condensazione,_dbg_init flag=PASSO_COMPOSIZIONE,_PASSO_FASI,_PASSO_MODULO,_PASSO_REGISTRO,_PASSO_CODA,_PASSO_TIPI,_PASSO_FUNZIONE -->

> ### 📌 **COMMIT 1 DEL RIORDINO — LA VOCE PASSA AL CONTROLLO COME *DATO*** *(2026-10-01)*
>
> `esegui_passo` ora chiama il controllo con ### **`voce=_nome` e `comp=comp`**, e la ragione e'
> precisa: le grandezze **a finestra** *(`REGISTRO_FINESTRA`, scheda `registro-grandezze`)*
> esistono **solo dentro** il passo, e per sapere se il punto di controllo e' **dentro o fuori**
> la finestra serve ### **QUALE voce ha appena girato.**
>
> | | |
> |---|---|
> | ### **non si legge dalla stringa `dove`** | `dove` e' una **frase per chi legge l'errore**; ricavarne il nome della voce sarebbe ### **una regola che parte dalla SINTASSI** — l'errore che in questa sessione ho fatto **sei** volte |
> | ### **la finestra si DERIVA, non si elenca** | `_finestra_aperta` usa la composizione ### **IN USO**, non quella canonica: `H-ETC-2` **permuta** l'ordine, e un elenco di voci scritto a mano ### **direbbe il falso appena l'ordine cambia** |
> | ### **e la derivazione e' sicura per COSTRUZIONE** | la garanzia viene da `valida_composizione`, che **impone** `apri` come **prima** voce e la **coda** `('chiudi', 'verifica_invarianti')`: ### **quindi `chiudi` esiste SEMPRE e viene SEMPRE dopo `apri`** |
>
> ### ⚠ **E LO SCHEDULATORE NON CONTIENE PIU' FISICA DI PRIMA:** `voce` e `comp` sono **cio' che
> lo schedulatore GIA' SA** *(quale voce sta girando, in quale composizione)*, passato invece che
> ri-dedotto. ### **Nessun `if` su un nome di voce e' entrato in `esegui_passo`** — la
> composizione resta un **DATO**.

> ### 📌 **GENERALIZZAZIONE 2 DEL 2026-09-29 — IL CONTROLLO DOPO *OGNI* VOCE** *(decisione di Luca)*
>
> Prima il controllo del registro girava in **due** punti: la **precondizione** e **dopo `mitosi`**.
> ### ⚠ **E restava un limite che avevo DICHIARATO:** `calcola_psi` riscrive `psi_spin` e
> `_estendi_psi_spinor` allunga `_psi_spinor` ### **a META' PASSO** — una grandezza che andasse fuori
> forma **fra** i due punti ### **non veniva vista**.
>
> ### ➜ **Ora il controllo gira DOPO OGNI VOCE della composizione.**
>
> | | |
> |---|---|
> | **il costo** | ~**30** confronti di forma per voce: con **8** voci, **9** controlli per passo *(la precondizione piu' una per voce)*. ### **E' la ragione per cui si puo' fare** |
> | ### **e TOGLIE un `if` sul nome di una voce** | lo schedulatore ### **non cabla piu' `'mitosi'`**: la composizione resta un **DATO** ancora piu' di prima, e il docstring di `esegui_passo` diventa vero **senza eccezioni** |
> | ### ⚠ **due CONTATORI cambiano per costruzione** | `_g_registro_controlli` e `_g_registro_assenti` contano ### **i controlli, non la fisica**: con piu' punti **devono** crescere. Il sigillo li **separa per NOME** e li ### **RIPORTA invece di farli sparire** — un contatore escluso in silenzio e' un buco, uno escluso per nome e stampato e' una **dichiarazione** |
>
> **Misurato sulla scena piccola:** 10 passi sani, ### **90 controlli** *(era 20)*, **42** assenze
> contate *(erano 14)*, **zero errori**.

> ### 📌 **AGGIUNTA DEL 2026-09-29 — `esegui_passo` ACQUISISCE IL SECONDO PRESIDIO DELLO SCHEDULATORE** *(`RIPIEGHI-ZERO`, decisione di Luca)*
>
> Accanto a `_ferma_se_oltre_max_nodi` *(che resta)* lo schedulatore chiama ora
> **`_ferma_se_registro_incoerente`** in **due** punti, e **la legge sta nella scheda
> `registro-grandezze`**: qui si dichiara **soltanto il PASSAGGIO**, perche' `REG-R` mappa
> **per funzione**.
>
> | punto | dove, e ### **perche' li'** |
> |---|---|
> | **l'`apri`** | ### **prima del ciclo**, accanto a `MAX_NODI` — e **non** dentro
>   `_smp_apri`: e' una **PRECONDIZIONE**, e una precondizione ### **non deve muoversi con
>   una voce.** `H-ETC-2` **permuta** la composizione, e *«il passo comincia con le lunghezze
>   giuste»* vale in **qualunque** ordine |
> | **dopo `mitosi`** | ### **dentro il ciclo**, subito dopo che la voce ha girato: `mitosi`
>   e' ### **il solo posto del passo in cui `n` cresce** |
>
> ### ⚠ **E il docstring di `esegui_passo` resta VERO:** l'`if` guarda ### **il NOME DI UNA
> VOCE**, che e' un **dato** della composizione — **non un flag**. La composizione resta un
> DATO, ed e' la ragione per cui **non** ho scelto la variante con **due voci nuove**
> *(`valida_composizione` vieta i duplicati, quindi servirebbero due nomi: ### **due leggi in
> piu', e `9-ter` dice di non moltiplicarle**)*.

> ### 🆕 **2026-09-28 (`MAX-NODI-FERMA`): lo schedulatore ha una PRECONDIZIONE.**
> Prima di validare la composizione, `esegui_passo` chiama
> `_ferma_se_oltre_max_nodi(net.n, 0, ...)`: ### **un passo che non si puo' fare NON COMINCIA.**
> **Sta all'inizio e non alla fine** perche' all'inizio e' una *precondizione*, alla fine
> sarebbe una *constatazione* con lo stato gia' oltre il limite. ### ⚠ **E il limite,
> dichiarato e NON MISURATO:** `mitosi` crea nodi **dentro** il passo, quindi un passo che
> sfora **finisce** e l'errore arriva **al passo dopo**. ### **QUANTO sia lo sforo NON LO SO:**
> sulla scena dei sigilli `(ii)(a)` sono **misurati 40 passi con ZERO nascite**, quindi `n` non
> cresce e lo sforo **non si osserva**. Serve una scena **che cresce**: e' una misura a se'.
> *(La legge della guardia sta nella scheda `guardia-max-nodi`.)*

> ### 🗄 **2026-09-28: `_passo.passo_pieno` ha un FALLBACK per i blob PRE-`T1`, e non indebolisce
> `H-P9`.** Un blob storico estratto **non ha `esegui_passo`**, quindi dopo `T1` ### **nessun sigillo
> poteva piu' confrontarsi con il codice di prima** -- ed e' esattamente cio' che `H-P8` esiste per
> proteggere. Il fallback itera `ordine()` *(le CINQUE LEGGI, che sono le stesse prima e dopo `T1`:
> `T1` ha aggiunto le FASI, che un blob pre-`T1` non ha)* e ### **scatta SOLO quando l'esecutore NON
> ESISTE**, cosa che per il simulatore sul disco non puo' succedere: **per il codice di oggi il ramo
> e' MORTO**. Contato da `_g_passo_pieno_pre_t1`.
# ㉙ LO SCHEDULATORE DEL PASSO — **`esegui_passo` / `PASSO_COMPOSIZIONE`**

> ### **`T1` del piano `SCHED-PASSO`** *(2026-09-28, decisione di Luca)*: **lo schedulatore possiede
> il passo.** Le regole del passo — sincronia, scala minima, `4π`, ordine — **non sono più intenzioni
> dentro le leggi controllate a posteriori dai presidi: sono l'ARCHITETTURA.**

## LA FORMA

```
PASSO_COMPOSIZIONE = ('apri', 'scuoti_vuoto', 'step', 'mitosi',
                      'rilassa_disegno', 'memoria_hebbiana_moto', 'chiudi',
                      'verifica_invarianti')
```

**Otto fasi, con apertura e chiusura FISSE in testa e in coda.** `esegui_passo(net, composizione=None)`
le esegue in ordine; `_PASSO_FASI` mappa `apri`/`chiudi` su `_smp_apri`/`_smp_chiudi`, `_PASSO_MODULO`
dice quali leggi sono **funzioni di modulo** *(oggi solo `scuoti_vuoto`)*.

### ⚠ **`PASSO_COMPOSIZIONE` NON È UN FLAG: è la COMPOSIZIONE, cioè un DATO.**
`H-REG-R` l'ha classificata come flag e ha imposto questa scheda — **e ha fatto bene**: una lista che
decide **quali leggi girano e in che ordine** è **fisica**, non configurazione. **Ma va detto che non
ha due stati:** non si «accende», si **compone**.

## CHE COSA FA `T1`, E CHE COSA NON FA

| | |
|---|---|
| **fa** | l'ordine e le fasi diventano **espliciti** e passano per **un punto solo** |
| ### **non fa** | ### **la fisica NON cambia.** Fotografia, variazioni e vincoli-una-volta sono `T3` |
| il criterio | ### **sigillo BYTE-IDENTICO** |

## PERCHÉ È BYTE-IDENTICO ANCHE SPOSTANDO LA CHIUSURA

**In `(c)1` avevo dichiarato un timore:** spostare `_smp_chiudi` fuori da `memoria_hebbiana_moto`
avrebbe fatto girare `verifica_invarianti` su **`d0` non ancora frenata**.
### **Il timore era giusto per lo spostamento della SOLA chiusura. La lista di Luca li sposta
INSIEME**, e fra i due non c'era nient'altro: ### **l'ordine relativo `chiudi → verifica_invarianti`
è preservato**, quindi il controllo guarda `d0` **già frenata**, esattamente come prima.

## COSA È USCITO DALLE LEGGI

le **cinque** aperture idempotenti di `(c)1` · la chiusura del **ritorno anticipato** di
`memoria_hebbiana_moto` · la chiusura **in coda** alla legge · la chiamata a
`verifica_invarianti(dove='memoria_hebbiana_moto')`.

> **E il ritorno anticipato è il caso che dice perché l'architettura è meglio di una regola:** il suo
> commento spiegava, con cura, che *«anche sul ritorno anticipato il freno va chiuso, sennò lo
> snapshot resterebbe aperto»*. ### **Era una regola scritta e rispettata a mano in un punto solo.
> Ora il confine non dipende più da quale uscita la legge prende.**

## TRE COSE CHE CAMBIANO E **NON SONO STATO**

**①** `verifica_invarianti` riceve `dove='esegui_passo'`: cambia **la stringa** in un referto
d'eccezione.
**②** ### **il benchmark perde il dettaglio per legge**: prima cronometrava le cinque chiamate una
per una, ora misura **il passo intero**. **Tornerà strumentando lo SCHEDULATORE (strato 5), non
ricopiando l'ordine.**
**③** il ritorno anticipato non chiude più il freno da sé.

## DIMENSIONI E LIMITI

**Nessuna grandezza nuova, nessun `clip`.** `esegui_passo` **non contiene fisica**: se un giorno ci
finisse un `if` su un flag, ### **la composizione smetterebbe di essere un DATO e tornerebbe a
essere codice** — ed è la cosa da non fare.

## 🏷 I TIPI DELLE VOCI *(`T2` (i tipi), 2026-09-28)* — **DICHIARATI, non fatti rispettare**

| voce | tipo | coerente col codice? |
|---|---|---|
| `apri` | **`fase`** | ✅ scrive solo lo snapshot |
| `scuoti_vuoto` · `step` · `memoria_hebbiana_moto` | `dinamica` | ✅ |
| `mitosi` | `AMBIGUA` | ✅ *(struttura **e** stato: l'ambiguita' dichiarata)* |
| ### `rilassa_disegno` | `disegno` | ### ❌ **scrive anche `psi`, `psi_spin`** |
| `chiudi` | `vincolo` | ✅ |
| `verifica_invarianti` | `osservatore` | ✅ |

**In `T2` (i tipi) nessun comportamento cambia** *(sigillo byte-identico)*: sara' **`T3`** a dare a ogni
tipo il suo **contratto**.

### ⚠⚠ **`fase` NON e' uno dei cinque tipi, e l'ho aggiunto io.**
`apri` **non e' una legge**: e' la **fotografia**, e non scrive stato fisico. **`osservatore` sarebbe
falso** *(scrive)*, **`vincolo` sarebbe falso** *(non corregge)*, **`dinamica` sarebbe il peggiore**
*(non fa fisica)*. **Dichiarato come mio invece di forzato in una casella che non gli appartiene.**

### 🛑 **E LA VOCE NON COERENTE, per cui ci si e' FERMATI** *(mandato di Luca)*

```
rilassa_disegno -> :6666 self._togli_rotazione_rigida(pos0) -> calcola_psi() -> psi, psi_spin
```

Il sito e' dentro `if L_CONSERVA and pos0 is not None:`, e ### **`L_CONSERVA` e' `False` col
driver** -- e' **uno dei 121 rami morti** di `(b)3`, e il codice lo marca **<<ERRATA, NON usare>>**.
### **Staticamente `rilassa_disegno` puo' scrivere `psi`; a runtime col driver non puo'.**

**Tre strade, e la decisione e' di Luca:** **(a)** il tipo e' sbagliato e la voce e' `AMBIGUA` anche
lei; ### **(b)** il ramo morto si ARCHIVIA e il tipo diventa coerente **per costruzione**;
**(c)** il controllo ignora i rami morti -- **e sarebbe la terza volta che la granularita' dei rami
inganna**. **Raccomandazione: (b)**, e porta con se' la `calcola_psi()` di `:6529`, l'unico degli 8
siti di `H-ETC-1` in un ramo morto.

**Il controllo:** `csv/_seal_fork/_sig_sched_tipi.py` -- **statico e per nome (`A9`)**: certifica la
**coerenza della dichiarazione**, non il comportamento.

## 🔒 LA VALIDAZIONE DELLA COMPOSIZIONE *(T2, 2026-09-28, su richiesta di Luca)*

**`esegui_passo` valida prima di eseguire**, e `valida_composizione` solleva
`ComposizioneNonValida`. **Quattro regole, e ognuna dice che cosa romperebbe:**

| regola | che cosa romperebbe |
|---|---|
| **`apri` e' il PRIMO** | una legge girerebbe **prima che la fotografia esista** |
| ### **`chiudi` e `verifica_invarianti` sono gli ULTIMI, in quest'ordine** | `chiudi` in mezzo: il freno gira su una variazione **PARZIALE** e le leggi dopo scrivono **fuori transazione**. Controllo prima del commit: guarda **`d0` non ancora frenata** |
| **ogni nome sta in `_PASSO_REGISTRO`** | `AttributeError` **a meta' passo**, dopo che alcune leggi hanno scritto |
| **nessun duplicato** | due volte la stessa variazione |

### ➜ **E' QUI CHE IL TIMORE DI `(c)1` DIVENTA IMPOSSIBILE invece che EVITATO.**
In `(c)1` avevo dichiarato che spostare la chiusura avrebbe fatto controllare gli invarianti su `d0`
non frenata; `T1` l'ha evitato **tenendoli insieme**; ### **`T2` lo rende irrappresentabile**: una
composizione che li separa **non gira**.

**SOLLEVA, NON AVVISA**, e **non e' un presidio di `git`: e' un controllo a RUNTIME** che nessun
commit puo' aggirare. **E si valida prima di toccare `net`**: una composizione rotta fallisce **col
passo ancora da cominciare**.

**⚠ `_PASSO_REGISTRO` e' LA PRIMA FORMA del registro di `T2`:** oggi elenca **i nomi**, e i **tipi**
sono il pezzo successivo.

**COLLAUDO, 8 casi con la risposta NOTA, 8 su 8** *(referto `csv/_seal_fork/_sig_sched_t2a.json`)*.
Il caso che deve fallire e' **`chiudi` in mezzo**. ### **E c'e' il simmetrico: una PERMUTAZIONE
### LECITA resta VALIDA** -- senza quel caso il validatore potrebbe rifiutare tutto e sembrare
corretto, e `H-ETC-2`, che **permuta**, non potrebbe piu' girare. **Un validatore che dice sempre no
non valida: blocca.**

## ⚠ PERCHE' I CHIAMANTI STANNO IN QUESTA SCHEDA, e non in una loro

`update` · `_passo` · `batch_condensazione` · `_dbg_init` sono **INTERFACCE** *(strato 6 della mappa
degli strati)*: **non hanno fisica propria**. `H-REG-R` ha chiesto una scheda per ognuna, e **creare
quattro schede di fisica per quattro chiamanti sarebbe stato peggio che non crearne nessuna** -- le
avrei riempite di niente.

### **Ma il presidio ha ragione sul fatto che conta: la loro modifica E' la modifica dello
### schedulatore.** Prima ognuna **ricopiava l'ordine**; ora **chiama la composizione**. Quindi
stanno qui, nella scheda della legge che le governa, **come SITI DI CHIAMATA** -- ed e' anche il
posto dove si vede che sono **sei** *(i quattro qui piu' i due di*
`csv/_test_fork/_scena_video.py`*)*, cioe' quanti punti dovevano restare d'accordo **prima** di `T1`.

## I CONTATORI (`A8`)

`_g_passi_eseguiti` · `_g_passi_composizione_altra` *(quante volte si è girato con una composizione
**non** standard: serve agli innesti di `T5` e a `H-ETC-2`, che **permuta**)*.

> ### 📌 **E una misura che conferma il progetto:** dopo `T1`, `_g_smp_gia_aperta = 0` — mentre in
> `(c)1` valeva `4` per passo. ### **L'idempotenza non serve più: il compositore SA di essere il
> primo.** `(c)1` era il primo abbozzo di questo confine, e il tag `pre-schedulatore-t1` lo conserva.

## LE REGOLE DI COMPOSIZIONE, dichiarate il 2026-09-28 (`T3`)

**La forma della sovrapposizione non e' un dettaglio di implementazione: e' un vincolo sulla FORMA
delle leggi**, e quindi sta qui. **Le cinque forme di Luca** — `1 variazione` · `2 rilassamento` ·
`3 derivata` · `4 vincolo` · `5 struttura` — **piu' due accettate e una esenzione:**

| forma | la legge |
|---|---|
| **6 · `gruppo`** | le grandezze che vivono in un **GRUPPO** *(il versore `_nb` e la sua coordinata polare `phi_s`)* **non compongono per somma dei valori**: due rotazioni compongono per **moltiplicazione**. ### **E' la fisica di `SU(2)`, che questo registro impone gia'.** ⚠ `omega_s` **NON** e' fra queste: `omega_new = omega_src + dtn_c*(...)` e' un'**addizione nell'algebra**, e l'algebra E' uno spazio vettoriale |
| **7 · `nascita`** | i **valori di partenza dei soli nuovi indici**, dopo la struttura e **fuori dalla somma**. La maschera e' `isnan` sulla grandezza di stato, che **significa** <<gli indici che non hanno ancora un valore>> |
| **0 · `segno`** | ### **NON e' una forma: e' un'ESENZIONE.** Le grandezze categoriali in `{+1,-1}` *(`perc_chi`, `perc_geom`)* non si compongono affatto: **sommare due decisioni darebbe `+2`, `0` o `-2`**, che non sono valori ammessi. **UNA SOLA legge scrive ogni grandezza-segno** |

> ### 📌 **L'esenzione `0 segno` REGGE SU UNA CONDIZIONE, e la condizione E' GIA' VERA PER
> COSTRUZIONE:** e' la cura di `A6-PERCCHI`. **Verificata a RUNTIME** (`_sig_segni_una_legge.py`,
> 3 passi sulla scena `(ii)(a)`, seme 11): `perc_geom` solo da `:5639` **3 su 3**, `perc_chi` solo
> da `:5666` **3 su 3**, e `:5642` **ZERO** — perche' `:5639` e `:5642` sono l'`if` e l'`else` della
> **stessa** condizione. ### **Si DICHIARA, non si cura.**
> **⚠ E un'analisi statica non puo' vederlo:** vede **le scritture** e non **le condizioni che le
> escludono**. Per questo il verdetto viene dalla **copertura di riga**.

**LA NASCITA E' UN EVENTO ATOMICO** *(decisione di Luca, 2026-09-28)*: la transazione comprende **il
RINCULO DEI GENITORI**, non solo i valori del figlio. ### **Se il rinculo sta fuori dall'evento, una
legge successiva vede uno stato in cui la materia e' comparsa dal nulla.** **Come** si distribuisce
il rinculo **non e' deciso: va DERIVATO** (`A1`), e misurato in `T3`.

*(Documento: `doc/REGOLE_composizione_T3.md`; tabelle generate in
`doc/REGOLE_composizione_T3_tabelle.md`. Strumento `csv/_test_fork/_etc_sovrapposizione.py`.
**94 scritture, e le eccezioni sono ZERO.**)*

<!-- SCHEDA nome=guardia-max-nodi funzioni=_ferma_se_oltre_max_nodi flag=MAX_NODI -->
# ㉚ `MAX_NODI`: UNA GUARDIA DI MEMORIA NON E' UNA LEGGE *(`MAX-NODI-FERMA`, 2026-09-28)*

**Questa scheda esiste per dire che qui NON c'e' fisica**, ed e' il punto: `MAX_NODI` **non e' un
tetto fisico** (`A11`) e **non protegge da un errore di fisica**. Protegge la RAM.

**Fino al 2026-09-28 pero' LA FISICA LA CAMBIAVA**, perche' i tre siti che la leggevano **non
fermavano il run**: `mitosi` restituiva **zero nascite**, `semina` **troncava**, il canale di
**Schwinger** si **spegneva**. ### **Tre leggi silenziose nate da una guardia di memoria** -- la
forma di `A8`.

| | |
|---|---|
| **la forma, ora** | **UN** controllo, `_ferma_se_oltre_max_nodi(n_attuale, quanti, dove)`, e **un'eccezione dedicata**, `LimiteNodiSuperato`. ### **DUE soli siti di chiamata**: lo schedulatore *(inizio del passo)* e `semina` *(**dopo la geometria**, sul numero VERO, per **entrambi** i rami)* -- e i due rami di `mitosi` che **non leggono piu' `MAX_NODI`** |
| **perche' UNA funzione e non tre `raise`** | tre copie sarebbero **tre leggi**, e `9-ter`: *a parita' di effetto si preferisce togliere un'eccezione* |
| **dove sta il controllo dello schedulatore** | ### **all'INIZIO del passo**, perche' e' una **precondizione**: un passo che non si puo' fare **non comincia**. Alla fine sarebbe una constatazione, con lo stato gia' oltre il limite |
| ⚠ **il limite, dichiarato e NON MISURATO** | `mitosi` crea nodi **dentro** il passo: un passo che sfora **finisce**, e l'errore arriva **al passo dopo**. ### **Quanto sia lo sforo NON LO SO:** sulla scena dei sigilli sono **misurati 40 passi con ZERO nascite**, quindi `n` non cresce e lo sforo non si osserva. Serve una scena **che cresce** |
| **la dimensione** | `4000000` contro i **~12800** nodi del pilota: **byte-inerte, e sigillato 23 su 23** |
| **il futuro** | ### **va ELIMINATO** *(decisione di Luca)*. Una guardia che non serve e' una riga in meno, non una legge |

## ✅ **PRESCRIZIONE DEL GUARDIANO** *(Luca, 2026-09-28)*: **un solo controllo, sul numero VERO**

Il ramo `_sat` di `semina` **passa `-1` a `_semina_lam`**, e il numero lo decide **la geometria**
(`n = len(p)`): ### **il valore calcolato con `MAX_NODI` NON VIENE USATO**, serve solo alla
scorciatoia `semina(0)`. ### **Quindi prima di questa cura la saturazione non era controllata
affatto.**

**E la prima stesura della cura metteva DUE controlli** -- uno prima, sul numero *chiesto*, e uno
**dentro il solo ramo `SEMINA_LAM`**. ### **Due controlli sono due leggi** *(`9-ter`)*, **e quello
dentro il ramo lasciava scoperto l'altro ramo.** Ora e' **uno**, dopo l'`if`/`else`, dove `n` e' il
numero di punti che **esistono** in `p`.

> ### 🟨 **MISURA DI LUCA, 2026-09-28: il ramo senza `SEMINA_LAM` E' COPERTO.** Con `MAX_NODI = 100`
> e `semina(200)`: ### **il blob VECCHIO tronca a 100 in silenzio, il NUOVO solleva
> `LimiteNodiSuperato`.** *(Il sigillo non ci arriva -- la scena dei sigilli chiede la saturazione --
> e il suo braccio `E` verifica solo la FORMA. **Questa e' la misura, e non e' mia: e' di Luca.**)*

> ### ⚠ **LA CONSEGUENZA, DICHIARATA:** controllando **dopo**, i punti `p` sono ### **gia' allocati**
> quando il run si ferma. Sono `n x 3` float, e **non sono la memoria che `MAX_NODI` protegge
> davvero** -- quella e' lo **stato del grafo**, archi compresi, che **non e' ancora stato toccato**.
> **Ma e' un'allocazione che prima, col troncamento, non avveniva.**

<!-- SCHEDA nome=conservazione-locale-dissipazione-globale funzioni=nascita,_rn_div_phivel,_rn_sch_phivel,scuoti_vuoto flag=A14 -->
# ⭐ **`conservazione-locale-dissipazione-globale` — `A14`**

*(assioma deciso da Luca il 2026-10-03; il testo intero sta in `doc/ASSIOMI.md`, `A14`.
Questa scheda lo COLLEGA alla fisica del modello.)*

> ### **Le grandezze si conservano LOCALMENTE e si dissipano GLOBALMENTE.** L'energia cambia
> globalmente ### **solo attraverso la crescita**; la ### **carica si conserva anche
> globalmente, nascita compresa.**

## ✅ **IL LEGAME CON LA VISIONE DEL 2026-10-01**

La revisione della visione dice gia' ### **«energia globale non conservata in espansione;
bilancio locale»**. ### ➜ **`A14` ne fa un CRITERIO invece di una descrizione**: non
*«cosi' va il modello»*, ma ### **«ogni legge si giudica su tre domande»** — `(a)` energia
locale, `(b)` carica locale, `(c)` se cambia un totale, solo per nascita.

## ✅ **IL LEGAME CON `REVERSIBILITA-LOCALE`: LA CRESCITA E' L'UNICA FRECCIA**

`A14` dice ### **dove sta la freccia del tempo**: nel punto `(2)`, e ### **solo li'**. Il nucleo
locale e' ### **conservativo e reversibile** *(una lagrangiana del second'ordine: `XY` /
sine-Gordon, non Kuramoto)*; ### **l'irreversibilita' entra con la NASCITA DEI NODI**, che cambia
il numero dei gradi di liberta'.
### 📌 **E la tabella di nascita del riordino e' esattamente il posto dove quella freccia
si legge**: `nascita()` e' ### **il punto unico** in cui il numero dei gradi di liberta' cambia.

## ⛔ **E LA CARICA ALLA NASCITA E' GIA' VIOLATA, MISURATA SUL CODICE**

```
_rn_div_phivel:  net.phivel = np.concatenate([net.phivel, 0.5 * (net.phivel[a] + net.phivel[b])])
_rn_sch_phivel:  net.phivel = np.concatenate([net.phivel, 0.5 * (net.phivel[aa] + net.phivel[bb])])
```

### ➜ **Il nato riceve la MEDIA dei genitori e ai genitori non si toglie niente:** la somma
### **CRESCE**. ### **Contro il punto `(3)`, che non ammette eccezioni.**

### ⚠ **E LA CURA OVVIA NON BASTA:** la grandezza conservata e'
### **`Q = somma |psi|^2 w (omega - omega_0)`** *(par.②-bis)*, ### **non `somma omega`**. Quindi
*«prendere dai genitori cio' che si riceve»* conserva `somma phivel` ### **ma non `Q`**, perche' i
pesi `|psi|^2 w` del nato e dei genitori ### **sono diversi** — e ### **il peso del nato non e'
noto prima che `psi` sia ricalcolato.
### 📌 **E' un vincolo di ORDINE, della stessa famiglia del `vincolo 4`** del contratto di
nascita *(`perc_geom` dopo `tw`, perche' la sua derivazione legge `tw`)*. ### **La voce che lo
tiene e' `CARICA-PERCORSO`.**

## ⚠ **IL PUNTO `(4)` E' UNA FORMA, NON UNA FORMULA: e dirlo e' il punto**

La geometria di contatto dice ### **in che linguaggio** si scrive la dissipazione indotta dalla
crescita — ### **non quale sia la legge.** Il teorema di Noether di contatto da' quantita'
### **dissipate** che decadono allo stesso ritmo e i cui ### **RAPPORTI si conservano**: cioe'
l'invariante non e' la quantita', ### **e' il rapporto.**
### ➜ **Ed e' un criterio MISURABILE:** se due grandezze del modello decadono con lo stesso
ritmo durante la crescita, il loro rapporto e' ### **una costante del moto** — e ### **si
cerca**, non si assume.

## ⛔ **IL PUNTO APERTO, che `A14` non chiude:** la crescita cambia ### **il numero dei gradi di
liberta'**, e una lagrangiana con un numero variabile di coordinate ### **non e' il caso di
scuola.** ### **`A14` dice che il nucleo locale deve restare conservativo e che la carica deve
sopravvivere alla nascita; NON dice come si scrive l'azione di un sistema che cresce.**
### **E' li' che il modello deve inventare** *(`ENERGIA-NON-DEFINITA`)*.

---

<!-- SCHEDA nome=schermatura-nucleo-nudo funzioni=lambda_nodi,_lam_archi,_eredita_psi_figli,massa_critica_adattiva,_ferma_se_cache_corta,_rho_sorgente,_nb_grav flag=SCHERMATURA,LAM -->
# ㉛ LA SCHERMATURA, E PERCHE' LA MASSA CRITICA SI CALCOLA SUL NUCLEO NUDO

**La legge:** `lambda_nodi` da' a ogni nodo una **portata** che SCENDE dove la densita' sale --
`u = rho/rho_c`, `fattore = 1/(1 + softplus(u-1))`, `lambda = max(LAM*fattore, LAM*0.15)`. Sugli
archi si simmetrizza: `_lam_archi = max(0.5*(lam_i + lam_j), 1e-6)`. Entra nei pesi come
`exp(-d/lam)`, quindi ### **lambda piu' grande = accoppiamento piu' esteso = campo piu' forte.**

## ⛔ **E LA LEGGE NON RESTITUISCE MAI `LAM`: LO SBAGLIO E' DEL PRIMO GIORNO**

*(fatto trovato dal guardiano sulla storia, 2026-10-03; voce `SCHERMATURA-LEGGE-REVISIONE`.*
*La decisione di che farne e' di Luca, e la correzione proposta e' in quella voce.)*

### **`softplus(-1) = ln(1 + e^-1) = 0.3132616875182229`**, quindi **a densita' NULLA**
### **`f(0) = 0.7614628596146600`** e la portata nel vuoto e' **`LAM * 0.76 = 0.609170`**,
### **non `LAM`.** La legge non e' *«accorcia la portata dove e' denso»*: e'
### **«accorcia SEMPRE del 23.85 %, e di piu' dove e' denso».**

### ⚠ **E L'INTENZIONE SCRITTA ERA L'OPPOSTO, dal commit di nascita `670310f`
*(2026-08-28)*, con la STESSA formula di oggi:**

| dove | la frase del commento originale | vera? |
|---|---|---|
| `:902` | *«fattore in (0,1], **= 1 sotto soglia**»* | ### **NO** |
| `:904` | *«`f = 1/(1 + softplus(u-1))` **-> 1 se rho < rho_c**»* | ### **NO** |
| `:906` | *«dolce, >= 0, **~0 sotto soglia**»* | ### **NO:** `0.3133` a `u = 0` |
| `:883` | *«dove `rho << rho_c` **resta `LAM`** (interferenza piena)»* | ### **NO** |

### ➜ **L'INTENZIONE ERA <<NESSUNA SCHERMATURA SOTTO SOGLIA>>. IL CODICE NON L'HA MAI
FATTO**, e sono passate **cinque settimane** — perche' nelle scene di allora le regioni
**sopra** soglia erano comuni e il taglio nel vuoto si confondeva col resto.
### **Oggi la scena e' TUTTA sotto soglia** *(`u` max **`0.113102`**, cioe' l'**`11.31 %`**
di `rho_c`; referto `csv/_test_fork/_schermatura_rami/`)* e il **taglio costante e' l'UNICA
cosa che la legge fa.**

### 📌 **E IL REPO L'AVEVA GIA' PREVISTO:** `REGISTRO_FISICA:P5` diceva
*«`lambda_nodi` quasi **COSTANTE, `0.74`-`0.76 LAM` ovunque**»* e ne traeva la conclusione
— *«la legge di schermatura e' di fatto **SPENTA dalla soglia irraggiungibile**»*.
### **Misurato: `0.743517`-`0.761463`. La previsione era giusta a QUATTRO CIFRE**, e la
soglia non e' solo irraggiungibile: ### **e' lontana un fattore ~9.**

### ⚠ **E IL PAVIMENTO `LAM*0.15` NON C'ERA:** `670310f` finiva con
`return LAM * fattore`, e il suo commento *(`:883`)* si vantava proprio di questo —
### **«Nessun LAM_MIN scelto.»** *(la legge vecchia aveva `P_LAM` e `LAM_MIN` come due
parametri liberi, con una taglia **non monotona**: `LAM_MIN` `0.1`/`0.3` -> `2369`/`9669`)*.
### **`portata_minima = LAM * 0.15` e' entrata SEI GIORNI DOPO** *(`5198938`, 2026-09-03)*:
### ➜ **e' il ritorno della manopola che questa legge esisteva per eliminare.**

### ⛔ **E C'E' UN SECONDO PAVIMENTO, NASCOSTO NEL CLIP, oggi INERTE:**
`np.clip(u-1, -30, 30)` satura il fattore a **`1/31 = 0.032258`** *(`lambda = 0.025806`)*,
che sta **SOTTO** `portata_minima = 0.12` — quindi il lato **`+30`** del clip **non puo' mai
influenzare il valore restituito** *(il pavimento esplicito morde da `u ~ 6.65`)*, e il lato
**`-30`** vorrebbe `u < -29`, impossibile per `rho >= 0`. ### **Il clip e' interamente morto
dietro il pavimento.** ### ⚠ **Ma diventa VIVO se il pavimento si toglie:** sopra
`u = 31` la legge smetterebbe di andare come `1/u` e tornerebbe **costante a `LAM/31`**.
### ➜ **I due punti si decidono INSIEME:** derivare il pavimento senza guardare il clip
### **sposta** il difetto invece di curarlo — ed e' `A11` *(un tetto che protegge da un
errore: si cerca l'errore)*.

## ✅ **DEFINIZIONE, decisa da Luca il 2026-09-28: la massa critica si calcola SUL NUCLEO NUDO**

Dentro `massa_critica_adattiva` la schermatura vale **`LAM`**, non il suo valore schermato, e
### **non e' un ripiego: e' la definizione.**

> ### 📌 **La soglia che ACCENDE la schermatura non puo' dipendere dalla schermatura stessa.**
> Il codice la implementa con `_calcolo_schermatura`, che esiste anche per **rompere la ricorsione**
> fra `lambda_nodi` e `massa_critica_adattiva` -- ma la ragione VERA e' la prima.

**⚠ E IL NUMERO, che mancava** (`A8`, contatore `_g_scherm_ricorsione`): **MISURATO `308` volte su
`44` passi, cioe' SETTE PER PASSO.** Su `530` chiamate di `_lam_archi`, ### **`310` restituiscono
`LAM`: il `58.5 %`.**

## ⛔ **IL DIFETTO CHE C'ERA ACCANTO, e non era la stessa cosa** *(`PSI-FLASH`)*

```
PRIMA:  if not hasattr(self, "psi") or len(self.psi) < self.n: return np.full(self.n, LAM)
```

### **Due condizioni in un `or`, e sono cose diverse:**

| | |
|---|---|
| ### `len(psi) == 0` | ### **inizializzazione**, e ### **NON e' `not hasattr`**: `Rete.__init__` fa `self.psi = np.zeros(0, complex)`, quindi l'attributo ESISTE SEMPRE. **RESTA**, e si conta (`_g_scherm_init`). ⚠ **La mia prima stesura splittava su `not hasattr` e l'errore scattava alla COSTRUZIONE DELLA SCENA**: la sonda contava le due condizioni insieme, e ho attribuito alla prima l'occorrenza del passo 1 che era della seconda |
| ### `len(psi) < n` | ### **IL DIFETTO**: al passo di nascita `mitosi` fa crescere `n`, e ### **la schermatura si spegneva PER TUTTA LA RETE** -- `lambda` da `~0.60` a `0.80`, `exp(-d/lam)` da `0.0655` a `0.1223`, `|psi|` su di `1.62x` **per TUTTI, non per il nato**, e il pozzo da `130` a `366`. **ORA SOLLEVA `SchermaturaSpenta`** |

> ### 📌 **Il `2.6x` sul pozzo NON ERA FISICA: era l'assenza della schermatura.** E scioglie il
> paradosso: **una nascita su 12802 nodi non muove il campo di tutti** -- lo muove **una guardia che
> si spegne.** *(Causa trovata dal guardiano; verificata da `csv/_test_fork/_lambda_al_flash.py`.)*

## ✅ **LA CURA: `psi` si EREDITA alla nascita** *(`_eredita_psi_figli`, forma 7)*

| grandezza | regola | il compagno che la usa gia' |
|---|---|---|
| `psi` | ### **media dei genitori** `0.5*(psi[a] + psi[b])` | `phi` del figlio e' `fm`, la fase **MEDIA** |
| `psi_spin` | ### **eredita' da `a`** | `phi_s` alla nascita **eredita da `a`** |

**Dare a ciascuno la regola del PROPRIO compagno e' l'unica scelta che non aggiunge una convenzione
nuova** (`9-ter`). **E NON un ricalcolo:** un ricalcolo a meta' passo leggerebbe il grafo **dopo** la
mitosi, cioe' **un'altra lettura mista**. **Il valore vero arriva al passo dopo, da `step`.**

**Chiamata ai DUE canali di nascita:** la mitosi *(genitori `a`, `b`)* e lo Schwinger *(`aa`, `bb`)*.
**Il segno dell'antinodo non si tocca:** `psi` e' **complesso** e l'antinodo nasce a `anti = fm + pi`,
quindi ### **il segno e' GIA' nella sua fase.**

## ⛔ **IL SECONDO GIRO: il GRADINO al passo DOPO la nascita** *(2026-09-28)*

**Il flash grande era curato, il gradino no:** `140.0` -> `138.6` -> ### **`146.2` (+11 % sulla
base)** -> `137.6`. ### **Il livello sotto la base non era sparito: era COPERTO da un difetto di
segno opposto.** *(Rilievo del guardiano su una mia lettura sbagliata: avevo letto <<non piu' sotto>>
come <<a posto>>.)*

| sito | il valore di scorta, e perche' non va |
|---|---|
| ### `_rho_sorgente` | restituiva **`abs(psi)^2`** invece di **`rho_spin`**: ### **un'ALTRA DENSITA' per tutta la rete** -- e la densita' entra in `lambda_nodi`, quindi nella schermatura, quindi nel campo. **MISURATO: 2 volte su 15 al passo dopo la nascita** *(len 12802, n 12803)* |
| `_nb_grav` | restituiva **`self._nb`** invece del Bloch **nativo** del campo emesso: **un'ALTRA DIREZIONE**, e la direzione entra nella **gravita'**. ⚠ **MISURATO: non scatta mai in questa finestra**, quindi la sua cura e' **byte-inerte** qui |

### ➜ **La cura: `_eredita_psi_figli` estende ANCHE `rho_spin`** *(il nato prende `rho_spin[a]`,
coerente con `psi_spin[a]`: sono la stessa grandezza vista in due modi,
`rho_spin = psi_spin^dag psi_spin`)*, **e i due ripieghi sollevano `CacheCorta`.**

**⚠ E NON si "ripara" allungando la cache a valle:** allungarla dove la si legge **e' proprio il
ripiego** che l'eccezione esiste per rendere impossibile.

*(`⚠` La somma di `psi` e' complessa: due genitori in antifase danno un figlio con `|psi| ~ 0`.
**E' interferenza distruttiva, cioe' fisica, non un errore.**)*

---

<!-- SCHEDA nome=registro-grandezze funzioni=__init__,_ferma_se_registro_incoerente,_ferma_registro,registro_mai_apparse,_forma_di,_scrivi_forma,_controlla_forma_e_tipo,_finestra_aperta flag=REGISTRO_STATO,REGISTRO_DERIVATE,REGISTRO_METRI,REGISTRO_FINESTRA,REGISTRO_NOMI,CONTROLLO_REGISTRO,CacheLunga,FormaSbagliata,TipoSbagliato,GrandezzaNonDichiarata,FinestraRestataAperta -->

### ⛔ **AGGIORNAMENTO del 2026-10-06 — UNA GRANDEZZA D'ARCO IN PIU': `twp_dip`**
*(cura di `TORS-W8-AVVOLGIMENTO`)*

| | |
|---|---|
| **che cos'e'** | il **dipolo precedente d'arco**, `("twp_dip", ("m",), "float64")` |
| **dove** | in `REGISTRO_STATO`, ### **subito dopo `twp`** |
| **la nascita** | ### **`nan`** per entrambi gli eventi convertiti *(`_rn_div_twp_dip`, `_rn_sch_twp_dip`)*, e una scrittura diretta in `_allaccia` per la **semina** |
| **l'invariante** | nella scheda `invarianti`: ### **forma `dip`** |

### ✔ **E `__init__` ENTRA IN QUESTA SCHEDA, e il perche' va detto:** `__init__` crea
### **tutte** le grandezze del registro vuote *(`self.twp_dip = np.zeros(0)`)*, quindi la sua
riga ### **e' parte del contratto del registro**, non di un'altra legge.
### ⛔ **Non e' un modo di passare `H-REG-R`:** `__init__` non aveva scheda, e il posto giusto
e' quello che parla delle grandezze che lui dichiara. ### **Se qualcuno trovasse un posto
migliore, lo sposti: la riga resta vera.**

### ✔ **E IL PRESIDIO D'IMPORT HA PRETESO LE REGOLE:**
`_nascita_collaudo_della_tabella()` alza un `RuntimeError` se una grandezza del registro non
ha una regola per **ogni** evento convertito. ### **Aggiungere il campo senza le due regole
NON sarebbe compilato**, e non e' una gentilezza: e' il presidio che fa il suo lavoro.

### ✔ **E IL VINCOLO 4 REGGE, verificato all'import:** `twp_dip` al posto **`33`**, `twp` al
`32`, ### **`perc_geom` al `31` e `tw` al `30`** — `perc_geom` e' **ancora** subito dopo `tw`,
e i due `raise` di `:1467` lo confermano.

> ### ✅ **COMMIT 4 — IL REGISTRO DICHIARA ANCHE LA CLASSE DI NASCITA DI UNA DERIVATA** *(2026-10-03)*
>
> ### **`REGISTRO_DERIVATE` ha una colonna in piu': `avvelena` oppure `auto-rinfresco`**, col
> vocabolario `NASCITA_DERIVATA` e un ### **`assert` ALL'IMPORT** che rifiuta una classe fuori
> vocabolario — *<<una derivata senza classe non si puo' ne' avvelenare ne' esentare, e il
> silenzio NON e' una terza possibilita'>>*.
>
> ### 📌 **E' LA STESSA FORMA DELLE ESENZIONI GIA' APPROVATE**, e per `9-ter` questo
> conta: `DOMINI['eta'] = ('nonneg_inf', …)` dichiara che `+inf` e' legittimo,
> `DOMINI['peq'] = ('peq', …)` che `nan` lo e' sugli archi, e ora la ### **classe di nascita**
> dichiara quali derivate ### **non si avvelenano.** ### **Tre casi della STESSA esenzione, non
> tre leggi.**
>
> ### ⚠ **E IL REGISTRO LO DICEVA GIA', A PAROLE:** la colonna del motivo di `_g_rampa_prec`
> e di `_xi_rumore` conteneva *<<AUTO-RINFRESCO>>* dal 2026-10-01. ### **Il commit 4 non
> aggiunge una convenzione: la rende LEGGIBILE DA UNA MACCHINA** — e
> `_avvelena_derivate` la legge da la', ### **senza nessun elenco a mano.**
>
> *(La scheda del veleno e' `veleno-derivate`.)*
>
> ### ⚠ **E UN CONSUMATORE ESTERNO SI E' ROTTO, e si aggiusta nello stesso commit** (par.6):
> `csv/_test_fork/_sonda_veleno.py` faceva un unpack a ### **TRE** campi. Ora e' a quattro.

> ### 📌 **COMMIT 1 DEL RIORDINO — IL REGISTRO E' DICHIARATO, NON MISURATO** *(2026-10-01)*
>
> > ### **Il controllo non parte piu' da un ELENCO: parte da CIO' CHE LA RETE HA.**
>
> **Era il TERZO limite che avevo dichiarato in questa scheda**, e ora non c'e' piu': il registro
> era stato costruito **misurando UNA scena e UNA configurazione**, quindi ### **con altri flag
> una grandezza nuova poteva comparire e restare FUORI dal controllo in silenzio, per sempre.**
> **Ora** `_ferma_se_registro_incoerente` scorre `vars(net)`, prende cio' che e' array o lista col
> **primo asse** `== n` oppure `== m`, e ### **se il nome non e' nel registro FERMA IL RUN**
> (`GrandezzaNonDichiarata`).
>
> ### ⚠ **LA REGOLA NON PARTE DAL NOME NE' DALLA SINTASSI, ed e' deliberato**
> In questa sessione ### **SEI volte** una mia regola basata sul **nome** o sulla **sintassi** ha
> nascosto cio' che cercava. ### **Qui una grandezza si qualifica PER LA SUA FORMA**, che e' un
> **fatto misurato a runtime**: nessun nome, nessun alias, nessuna sintassi.
>
> ### ✅ **E AL PRIMO GIRO IL PRESIDIO HA TROVATO UN BUCO VERO: `_smp_d0` e `_smp_d`**
> Sono **per arco**, `float64`, e il registro ### **non le dichiarava.** Il motivo e' preciso:
> ### **il registro era stato costruito misurando `vars(net)` alla FINE di un passo**
> *(`csv/_test_fork/_registro_grandezze.py`, fine del passo 30)*, e queste ### **a fine passo NON
> ESISTONO** — le azzera `_smp_chiudi`. ### **Una misura presa a UN SOLO ISTANTE non puo' vedere
> cio' che vive FRA DUE ISTANTI**, ed e' esattamente il buco che il **controllo dopo ogni voce**
> esisteva per trovare.
>
> ### 🧪 **LA FINESTRA, MISURATA voce per voce** *(scena piccola, seme 11, 3 passi, 27 controlli)*
>
> | dove | `_smp_d0` e `_smp_d` |
> |---|---|
> | `prima delle leggi` | ### **NON ESISTONO** |
> | da `apri` a `memoria_hebbiana_moto` *(sei voci)* | ### **lunghe `m` = 70199** |
> | dopo `chiudi`, dopo `verifica_invarianti` | ### **NON ESISTONO** |
>
> **Zero casi ambigui, zero disallineamenti, e le due SEMPRE INSIEME.**
>
> ### ➜ **ALLORA NON SONO DERIVATE, E NEMMENO DI STATO: SONO UNA TERZA COSA, E SI DICHIARA**
> **Di STATO no:** una grandezza di stato ha una **regola di nascita** e la sua lunghezza e' un
> invariante ai punti di controllo — queste a quei punti ### **devono NON esserci.**
> **Derivate no:** per il criterio di Luca *(letta fra la nascita e la sua riscrittura)* ### **sono
> LETTE dentro la finestra** — le scrive `_smp_apri`, le riallinea `_smp_chirurgia`, le legge e le
> chiude `_smp_chiudi`. ### **Chiamarle derivate sarebbe FALSO**, e la terza colonna delle derivate
> chiede un **motivo misurato** che qui non esiste.
> ### **Si dichiarano per cio' che SONO:** `REGISTRO_FINESTRA`, con la **forma**, il **tipo**, la
> **voce che apre**, la **voce che chiude** e il **motivo misurato**.
>
> ### ⛔ **E IL CONTROLLO DIVENTA PIU' FORTE, NON PIU' DEBOLE**
> ### **Fuori dalla finestra la grandezza DEVE NON ESISTERE** (`FinestraRestataAperta`), ed e'
> ### **il difetto che `_smp_chiudi` TEME nel suo stesso commento**: *«la fotografia si CHIUDE
> sempre, senno' resterebbe aperta e ### il passo dopo leggerebbe quella del passo prima»*.
> ### **Era un timore scritto in un commento; ora e' un presidio** (`A9`).
> **Il verso molle SI CONTA e non ferma** (`A8`): `_smp_apri` fotografa **solo se**
> `SCALA_MIN_PASSO or COES_CAUSALE`, quindi a flag spenti la finestra ### **non si apre mai**, e
> *«non si e' aperta»* deve essere **leggibile** (`_g_finestra_chiusa_dentro`), non supposto.
>
> ### 📐 **E LA FINESTRA SI DERIVA DALLA COMPOSIZIONE IN USO, non da un elenco di voci**
> `H-ETC-2` **permuta** l'ordine, e un elenco scritto a mano direbbe il falso appena l'ordine
> cambia. `valida_composizione` **impone** che `apri` sia la prima voce e che la coda sia
> `('chiudi', 'verifica_invarianti')`: ### **quindi `chiudi` esiste SEMPRE e viene SEMPRE dopo
> `apri`**, e `_finestra_aperta` puo' derivare l'intervallo invece di cablarlo.
> ### **E la voce passa al controllo come DATO** (`voce=`, `comp=`), ### **non si legge dal testo
> della stringa `dove`**: leggerla da una frase sarebbe di nuovo una regola basata sulla SINTASSI.
>
> ### 🧹 **UNA SOLA LEGGE, non due** (`9-ter`)
> La cascata **forma -> tipo** e' uscita in `_controlla_forma_e_tipo` e la chiamano **entrambi** i
> cicli *(STATO e FINESTRA)*: ### **la tabella nuova aggiunge una DICHIARAZIONE, non una legge** —
> 30 righe diventate 5 nel ciclo, e il conto delle leggi **non cresce**.
>
> ### ⚠ **IL LIMITE CHE RESTA, dichiarato**
> Una grandezza con `len` **diverso** da `n` e da `m` ### **non viene vista** *(per esempio una per
> faccia o per ciclo)*: il presidio copre ### **i DUE METRI che il registro conosce, non tutti i
> metri possibili.** E se `n == m` i due metri sono **indistinguibili** — oggi `12802` contro
> `471564`, e lo strumento del registro **lo controlla e lo dichiara.**

> ### 📌 **GENERALIZZAZIONE 3 DEL 2026-09-29 — IL TIPO** *(decisione di Luca)*
>
> > ### **Un COMPLESSO diventato REALE perde META' DELL'INFORMAZIONE senza cambiare forma.**
>
> E le **sei** grandezze `complex128` del registro — `psi` `_psi_prec` `_psi_spinor`
> `_psi_spin_prec` `_spinor_lift` `psi_spin` — sono ### **esattamente quelle su cui e' nato il
> flash di `PSI-FLASH`**: la **fase** vive nella parte immaginaria, e un `np.real` di troppo la
> butterebbe via ### **senza che ne' la LUNGHEZZA ne' la FORMA se ne accorgano.**
>
> | | |
> |---|---|
> | il terzo campo | **21** `float64` · **6** `complex128` · **3** `int64` · **1** esente |
> | ### **`None` = ESENTE, e c'e' UNA sola** | `conc_nodi`: e' una **LISTA**, e il suo
>   `float64` misurato e' un ### **ARTEFATTO di `np.asarray` su liste vuote** |
> | **quando si guarda** | ### **solo se la FORMA e' giusta**: se la forma e' sbagliata il
>   difetto e' quello, e ### **due errori insieme non aiutano chi legge** |
> | **`TipoSbagliato`** | il **quarto** nome per il **quarto** difetto distinto — corta,
>   lunga, forma, tipo — e ### **non una legge in piu': la legge e' UNA** |
>
> ### ⛔ **IL BUCO CURATO LO STESSO GIORNO, e l'ha visto il guardiano**
> La prima stesura diceva `if suo is not None and str(suo) != tipo`, e quel **`is not None`**
> era ### **UNA SECONDA ESENZIONE IMPLICITA** — mentre il registro ne dichiara ### **una
> sola** *(`conc_nodi`)*. ### **E' la stessa famiglia dei ripieghi appena chiusi: una
> condizione di ESISTENZA che copre un difetto.**
>
> **MISURATO PRIMA della cura**, su sei grandezze trasformate in **lista** con la forma giusta:
> ### **`psi` e `eta` SALTATE IN SILENZIO** *(e `psi` e' una delle sei complesse)*, `phi0` e
> `perc_chi` **rotte rumorosamente** *(`TypeError`, `AttributeError`)*, `pos` e `_psi_spinor`
> ### **gia' prese da `FormaSbagliata`** — perche' ### **una lista PERDE IL SECONDO ASSE.**
> ### ➜ **Il buco viveva SOLO sulle grandezze a UN asse**, dove la forma resta giusta.
>
> **DOPO la cura** *(`dtype` assente e tipo dichiarato → `TipoSbagliato`, col tipo vero
> `"(nessun dtype: <classe>)"`)*: ### **sei su sei PROTETTE — zero silenziose, zero
> rumorose** — e i due che prima **rompevano** alzano ora ### **l'errore DICHIARATO**.
> ### **L'unica esenzione resta quella scritta nel registro.**
>
> ### ⚠ **LA RISERVA, DICHIARATA: i tre `int64` dipendono dalla PIATTAFORMA.**
> `_deg` `perc_chi` `perc_geom` sono `int64` **su questa macchina**, ma la larghezza
> dell'intero predefinito di numpy **cambia fra piattaforme**. ### **Se l'errore scatta su uno
> di quei tre, la cosa da aggiornare e' IL REGISTRO, non il codice** — e ### **il messaggio
> d'errore lo DICE**, invece di lasciarlo capire.
>
> ### ✅ **IL CASO CHE DEVE FALLIRE, misurato — SETTE su sette:** `psi`, `_psi_spinor`,
> `psi_spin` ### **da complesso a reale** *(`float64` invece di `complex128`)*; `_nb` e `pos`
> a `float32`; `perc_chi` e `_deg` a `float64`. ### **Tutti e sette alzano `TipoSbagliato`, e
> la FORMA in tutti e sette era GIUSTA** — quindi nessuno di essi veniva visto prima.

> ### 📌 **GENERALIZZAZIONE 1 DEL 2026-09-29 — LA FORMA COMPLETA** *(decisione di Luca)*
>
> ### ⚠ **Il controllo guardava UN SOLO ASSE, e io l'avevo dichiarato come LIMITE:** `len` e'
> il primo asse, e ### **dieci grandezze del registro hanno DUE assi** — `pos` `_nb` `_nb_prec`
> `_nb_ret` `mem_mot` `omega_s` sono `(n, 3)`, `_psi_spinor` `_psi_spin_prec` `_spinor_lift`
> `psi_spin` sono `(n, 2)`. ### **Un secondo asse sbagliato PASSAVA.**
>
> ### ➜ **Ora il registro dichiara la FORMA e il controllo la verifica TUTTA.**
>
> | | |
> |---|---|
> | la dichiarazione | `("n",)` · `("n", 3)` · `("n", 2)` · `("m",)`, e il primo asse si
>   **risolve** in `n` o `m` al momento del controllo |
> | ### **le forme sono MISURATE** | vengono dalla colonna `forma` di
>   `doc/REGISTRO_grandezze.md`, che `_registro_grandezze.py` genera **dal runtime**:
>   ### **non le ho scritte a mano** |
> | **`FormaSbagliata`** | classe **nuova**: primo asse **giusto**, un altro **no**.
>   ### **Non e' ne' corta ne' lunga: e' UN'ALTRA GRANDEZZA**, e merita il suo nome |
> | ### ⚠ `conc_nodi` | e' una **lista di liste** e il suo secondo asse vale `0` e **cambia**
>   *(le voci si aggiungono)*: si dichiara ### **solo il primo asse**, perche' dichiarare `0`
>   sarebbe **dichiarare il falso** |
>
> ### ✅ **IL CASO CHE DEVE FALLIRE, misurato:** un **secondo asse** sbagliato su `pos`
> *(`n×2` invece di `n×3`)*, `_nb` *(`n×4`)* e `_psi_spinor` *(`n×3` invece di `n×2`)* alza
> ### **`FormaSbagliata` tre volte su tre**, con **entrambe le forme** nel messaggio.
> **Prima nessuno dei tre veniva visto.**

> ### 📌 **AGGIUNTA DEL 2026-09-29 — `_ferma_registro` CHIAMATA DAI SITI: la condizione fusa di
> `_sin2_vir`** *(punto 3 di Luca, primo pezzo)*
>
> Il **freno anisotropo** *(`ZETA_VIR`)* leggeva `_sin2_vir` con una **condizione fusa**:
> `is None` **or** `len != len(beta)`. ### **Il codice STESSO dichiarava che le due cause «sono cose
> diverse e vanno distinte, non sommate»** — e le distingueva **nel contatore** *(`shape[0] = -1`)*,
> ### ⚠ **ma NON nel comportamento: entrambe portavano a «nessun freno».**
>
> | | |
> |---|---|
> | `None` | ### **LEGITTIMO E DERIVATO, e resta**: `memoria_hebbiana_moto` gira **dopo** `step`, quindi al primo giro non esiste; e inventare un valore iniziale sarebbe ### **un numero SCELTO** (`A1`) — *«al primo giro NON C'E' FRENO ANISOTROPO, ed e' corretto che sia cosi'»* |
> | **lunghezza sbagliata** | ### **SOLLEVA** *(`CacheCorta`/`CacheLunga` via `_ferma_registro`)*: faceva **sparire una legge in silenzio, per TUTTA LA RETE** — ed era ### **l'ultimo ripiego silenzioso che la prova a guasto vedeva** |
>
> **Due rami, due contatori**, come prima: `_a` *(non-Verlet)* e `_b` *(gemello Verlet, a sottopassi
> CFL)*. ### **E la separazione e' BYTE-INERTE, MISURATA: 12 passi, 23 grandezze, zero differenze —
> E I CONTATORI SONO IDENTICI** *(`salti` 1 e 4, cioe' solo la causa `None`)*.
>
> ### ⚠ **E la guardia di `P_eq` e' TOLTA** *(`len(d0) >= len(i)`, sempre vera per costruzione ora:
> una guardia che non guarda niente, `A9`)*.

> ---
>
> ### ⭐ **LA REGOLA DI CONFINE, e vale anche per la potatura futura** *(Luca, 2026-09-29)*
>
> > # **IL CONTROLLO UNICO POSSIEDE LE LUNGHEZZE.**
> > # **I SITI POSSIEDONO SOLO «ESISTE ANCORA?».**
>
> | forma del sito | che cosa se ne fa |
> |---|---|
> | **condizione FUSA** *(`is None` / `not hasattr` **e** un test di lunghezza)* | si **tiene** il test di **esistenza** — ### **e' un'inizializzazione VERA, e resta** — e ### **la LUNGHEZZA SOLLEVA** |
> | **sola LUNGHEZZA** | ### **si TOGLIE**: il controllo la garantisce, e ### **una guardia che non guarda niente e' `A9`** |
>
> ### ⚠ **E si confrontano ANCHE I CONTATORI, non solo le grandezze.** Questi rami **si contano**
> *(`A8`)*: `_ritmo_sicurezza`, `_ritmo_guard4pi_ko`, `_ritmo_snap_identico`, `_g_zeta_vir_*`,
> `_cs_in_fallback`… ### **Un contatore che cambia di UNO e' un difetto, e le 23 grandezze del
> sigillo NON lo vedrebbero**: lo stato puo' restare identico mentre il **percorso** e' cambiato.
>
> ### 🛑 **E la POTATURA dei 57 rami morti e' RIMANDATA** *(decisione di Luca)*: **dopo lo
> schedulatore**, perche' ### **il riordino della mitosi tocchera' molte di quelle righe** e potarle
> adesso vorrebbe dire farlo **due volte**. La lista e' in **`doc/POTATURA_guardie.md`**, **generata**
> — **57 siti in 13 funzioni: 12 condizioni FUSE e 45 di sola lunghezza** — e la voce e'
> **`POTATURA-GUARDIE`**. ### **`self.n > 0` RESTA**, e non e' la stessa cosa: su
> una rete vuota la mediana di un array vuoto da' `nan`, e `np.seterr(invalid='raise')` solleva.
> ### **E la FETTA non e' toccata** — e' `P-EQ-MEDIANA-ARCHI`, **in coda**.

> ### 📌 **AGGIUNTA DEL 2026-09-29 — `registro_mai_apparse`: IL RENDICONTO DELLA TOLLERANZA**
> *(punto 2 di Luca, che chiude un varco che avevo aperto io)*
>
> La tolleranza dell'assenza e' **per grandezza, fino alla prima apparizione** — necessaria,
> perche' `_nb_ret` e' il Bloch **ritardato** e al primo passo ### **non esiste un passato**.
> ### ⚠ **Ma una tolleranza SENZA RENDICONTO e' un VARCO:** una grandezza che non appare **mai**
> resterebbe ### **fuori dal controllo per sempre, in silenzio.**
>
> ### ➜ **Quindi a fine run, e IN OGNI SIGILLO, si ELENCA cio' che non e' mai apparso**, e se la
> lista non e' vuota ### **non e' una curiosita': e' un ESITO** — o la grandezza **non esiste**
> in questa configurazione *(e va dichiarata **DERIVATA** col suo motivo misurato)*, o qualcosa
> ### **non la crea mai, e allora il registro dice il falso.**
>
> **Non e' fisica e non tocca un bit:** legge `_g_registro_apparse` e stampa. **E' un
> RENDICONTO**, cioe' la forma che `A8` chiede: *un comportamento che non si conta e' un
> comportamento sconosciuto.*

# 📒 **IL REGISTRO DELLE GRANDEZZE, E IL CONTROLLO UNICO** *(`RIPIEGHI-ZERO`, 2026-09-29)*

## La forma

> ### **Ai due punti dello schedulatore, ogni grandezza di STATO ha lunghezza ESATTAMENTE il suo
> ### bersaglio: `n` per i nodi, `m` per gli archi. Altrimenti il run SI FERMA, col NOME.**

`len(x) == n` *(nodi)* · `len(x) == m` *(archi)* · piu' corta → **`CacheCorta`** · piu' lunga →
**`CacheLunga`**. ### **Non c'e' un valore di scorta, non c'e' un troncamento, non c'e' un
allungamento: c'e' un errore.**

## La derivazione: **perche' UNICO e non quaranta guardie**

**Non e' una preferenza di stile: e' misurato.** La **prova a guasto** del 2026-09-28
*(`f173050`)* ha mostrato col **comportamento** che una guardia **dentro** una legge non tiene:

| | |
|---|---|
| `:4462`, la guardia su `psi_spin` | ### **ESEGUE e non spara**, perche' `calcola_psi` ha gia' riscritto `psi_spin` a piena lunghezza: ### **sta A VALLE della riscrittura** |
| `_estendi_psi_spinor` | **allunga la coda** con una riga **inventata**, quindi ogni guardia a valle trova un array **giusto**: ### **un estensore a monte la DISARMA** |
| la classe `(b)` *(«estende i soli nuovi»)* | ### **non e' sicura**: `mem_mot` estende **davvero** la coda e il guasto cambia **12611 nodi**, perche' l'elemento inventato appartiene a un nodo ### **CHE ESISTEVA GIA'** |

### ➜ **Curare sito per sito aveva lasciato 29 grandezze su 31 scoperte: `0` su `31` erano «a posto».**

## Le due classi, e ### **il criterio NON e' «stato o derivata»**

**Il mio piano diceva «stato o derivata», e Luca l'ha corretto:** `psi` **E'** derivata *(la scrive
`calcola_psi`)* e ha avuto bisogno di una regola di nascita ### **perche' una legge la leggeva fra
la mitosi e il ricalcolo** — ed e' li' che nasceva il flash di `PSI-FLASH`.

> ### 📌 **IL CRITERIO E': «una legge la legge CORTA fra la nascita e la sua riscrittura?»**

| classe | quante | che cosa vuol dire |
|---|---|---|
| ### **`REGISTRO_STATO`** | **30** | sono **GIA' PIENE** quando `mitosi` ritorna: ### **nessuno puo' vederle corte.** Si controllano |
| ### **`REGISTRO_DERIVATE`** | **10** | sono **corte** a quell'istante, e per ognuna la **terza colonna dice il MOTIVO MISURATO** per cui va bene: **4** nessuna legge le legge · **4** la legge le trova **gia' riscritte** · **2** sono **AUTO-RINFRESCHI** |
| `REGISTRO_METRI` | **3** | `phi` `i` `j`: ### **non sono voci, sono il RIFERIMENTO** *(`n` E' `len(phi)`, `m` E' `len(i)`)* |

**I due auto-rinfreschi erano GIA' dichiarati e contati nel codice**, e la misura lo conferma:
`_xi_rumore` *(«NON e' un fallback: e' il percorso normale della mitosi; `xi` e' l'AMBIENTE …
il figlio NON lo eredita»)* e `_g_rampa_prec` *(«e' un array DIAGNOSTICO … il suo disallineamento
SI CONTA … si perde una MISURA, non una legge»)*. ### ➜ **`A8` era gia' rispettato in entrambi.**

## ⚠ **«ASSENTE» non e' «DI LUNGHEZZA SBAGLIATA», e la tolleranza e' PER GRANDEZZA**

E' la distinzione che Luca ha imposto in `lambda_nodi`. **Due cose l'hanno allargata, e entrambe
sono MISURATE, non supposte:**

1. ### **«assente» comprende «esiste ma e' VUOTA»**: `Rete.__init__` crea diverse cache come
   `np.zeros(0)`. La prima stesura guardava solo `is None` e ### **si e' fermata all'`apri` del
   PRIMO passo** su `_psi_spinor`.
2. ### **la tolleranza e' PER GRANDEZZA, fino alla sua PRIMA APPARIZIONE** — e non *«prima del
   primo passo»*, che ### **ferma un run sano all'`apri` del passo 2** su **`_nb_ret`**.

| dall'`apri` del passo | quante diventano piene |
|---|---|
| **0** *(subito dopo la semina)* | **18** |
| **1** | **11** |
| ### **2** | ### **1: `_nb_ret`** |
| mai, in 12 passi | **0** |

### ➜ **E la ragione di `_nb_ret` e' FISICA, non pigrizia: e' il Bloch RITARDATO** `n(t-tau)`
*(`FORK_SU2_MEM`)*, ### **e al primo passo NON ESISTE UN PASSATO.**
**La forma «tollera fino al passo 2» sarebbe stata una MANOPOLA** (`A1`): *«fino alla prima
apparizione»* non contiene nessun numero scelto. ### **E una grandezza che SPARISCE dopo essersi
vista piena e' un ERRORE** — che e' il caso che la regola di Luca vuole impedire.

## I limiti, dichiarati

| | |
|---|---|
| ### **il controllo guarda UN SOLO ASSE** | `len` e' il **primo** asse. `pos` `_nb` `_nb_prec` `_nb_ret` `mem_mot` `omega_s` sono `(n,3)`, `_psi_spinor` `_psi_spin_prec` `_spinor_lift` sono `(n,2)`: ### **un secondo asse sbagliato passerebbe** |
| ### **due punti potrebbero non bastare** | `calcola_psi` riscrive `psi_spin` a `:4421` e `_estendi_psi_spinor` allunga a `:2264`, ### **entrambi a META' PASSO**: una cache che va corta **fra** i due punti non viene vista |
| **il registro viene da UNA configurazione** | `nmasse 3`, `sep 6.1158`, seme `11`, **zero differenze su 80 booleani** dal driver. ### **Con altri flag una voce di STATO potrebbe non esistere mai** — e allora il controllo si ferma **nominandola**, che e' informazione, non un difetto: va dichiarata **DERIVATA col suo motivo misurato**, mai togliere in silenzio |
| ### **e le LISTE hanno un punto cieco** | `conc_nodi` cresce con `.append`, non con un assegnamento: l'AST e la sorveglianza **non la vedevano**. ### **La sua regola di nascita esiste** *(`:6669`, `:6839`)*, e l'ho trovata solo verificando a mano |

---

# ⭐⭐ **LA VISIONE DI LUCA SULLA NASCITA E SULLA CONSERVAZIONE** *(Luca, 2026-10-01)*

> ### **(a) LA NASCITA DI UN NODO HA TRE ESITI: SPAZIO · MATERIA · MATERIA E ANTIMATERIA.**
> ### **`peq` — la densita' di equilibrio del vuoto — E' IL RIFERIMENTO CHE LI SEPARA.**
>
> ### **(b) SI CONSERVA ESATTAMENTE SOLO LA CARICA**, cioe' materia contro antimateria.
>
> ### **(c) L'ENERGIA GLOBALE NON SI CONSERVA.** Il modello deve poter simulare uno spaziotempo
> ### **che si espande** — e in relativita' generale, in espansione, ### **non c'e' conservazione
> ### globale dell'energia.** ### **Resta il bilancio LOCALE: ogni variazione ha una CAUSA
> ### DICHIARATA.**

### 📌 **PERCHE' QUESTE TRE RIGHE CAMBIANO IL PIANO DEL CALORE**
Il piano era costruito su **due bilanci paralleli** — avvolgimento **ed** energia — ### **e li
trattava come due conservazioni.** La visione dice che ### **non sono simmetrici:**

| | |
|---|---|
| ### **la CARICA** | ### **si conserva ESATTAMENTE.** E' l'unica legge di conservazione **stretta** del modello |
| ### **l'AVVOLGIMENTO `tw`** | ### **NON e' la carica e NON si conserva.** La sua perdita alla divisione ### **non e' un difetto da curare: e' una LEGGE da scrivere** |
| ### **l'ENERGIA** | ### **non si conserva globalmente, e non DEVE.** Il bilancio che si chiede e' ### **locale**: *«ogni variazione ha una causa dichiarata»* |

> ### ⚠ **E QUESTO RIBALTA UNA MIA CONCLUSIONE, non la raffina.** Avevo scritto che
> `DIVISIONE-AUTOCONSISTENTE:M1` mostrava ### **«una carica che svanisce, evento per evento»** —
> e ### **`tw` NON E' UNA CARICA.** La misura resta *(`1.17` avvolgimenti per arco diviso, con
> `PHI_CRIT = 2π` esatto)*, ### **ma la sua LETTURA era sbagliata: non e' una violazione, e' un
> PREZZO NON SCRITTO.**

---

## ⭐ **DECISIONE 1 DI LUCA: «LA TORSIONE PAGA LO SPAZIO»** *(2026-10-01)*

> ### **L'avvolgimento che sparisce alla divisione E' IL PREZZO DEL NODO NUOVO.**
> ### **Si riscrive come LEGGE DICHIARATA, col bilancio scritto — quanto avvolgimento per quanto
> ### spazio — invece di restare una perdita nascosta.**

| | |
|---|---|
| **che cosa NON e'** | ### **non e' una carica che svanisce** *(era la mia lettura, ed era sbagliata)* |
| **che cosa e'** | ### **una CONVERSIONE**: avvolgimento -> spazio. E una conversione ### **si scrive**, con il suo tasso |
| ### **cosa la rende una legge e non una toppa** | ### **il bilancio DEVE essere scritto:** quanto `tw` per quanto spazio. ### **Senza il tasso non e' una legge, e' ancora una perdita** |
| **il numero misurato da cui parte** | `1.17` avvolgimenti per arco diviso *(min `0.60`, max `1.33`)*, ### **e sono il dato di partenza del tasso, non il tasso** |

## ⭐ **CRITERIO 8 DI LUCA: LA DIVISIONE CREA SOLO SPAZIO NEUTRO** *(2026-10-01)*

> ### **La divisione da sola crea SOLO SPAZIO NEUTRO. La materia CARICA nasce solo A COPPIE:
> ### due nodi nuovi, uno `+1` e uno `−1`, LOCALMENTE — cosi' la carica totale NON CAMBIA.**

### ⚠ **E OGGI IL CODICE NON FA COSI', ed e' misurato** *(`:G4`)*: lo **Schwinger** crea ### **UN
SOLO nodo** *(l'antinodo, accanto a un genitore **che c'era gia'**)*, quindi ### **la somma della
carica cambia di `±1`** — e il commento del codice dice l'opposto *(«la coppia e' NEUTRA e
`N(+1) − N(−1)` NON cambia»)*. ### **Il criterio 8 e' la forma che quel pezzo deve prendere.**

## ⭐ **DECISIONE 5 DI LUCA: `MEM-HEBB-VERSO` BLOCCA IL RUN BASE** *(2026-10-01)*

| | |
|---|---|
| ### **blocca** | ### **SI'.** Finche' non e' curato, ### **ogni misura nuova nasce su un sistema che dipende dall'ordine di memorizzazione degli archi** |
| **quando** | ### **la prossima modifica di FISICA dopo i commit 2 e 3 del riordino**, col suo piano e il suo sigillo |
| ### **come** | ### **UNA funzione chiamata per i DUE estremi** *(coi ruoli scambiati)*, e ### **`np.add.at` al posto dell'assegnazione con indici ripetuti** |
| **e il piano `xy`** | `MEM-HEBB-PIANO-XY` ### **si MISURA prima di curarlo** |

## 🕐 **LE DECISIONI 2, 3 E 4 RESTANO APERTE** *(e aspettano una misura, non una mia proposta)*

| | aspetta |
|---|---|
| **2** — il Nose-Hoover si sostituisce o si affianca | ### **`:M7`** *(la potenza del solo `−xi·phivel`)* |
| **3** — quale grandezza decide `t` | le misure del passo 2 |
| **4** — il ruolo dello scuotimento | ### **`:M7`**, e `SCUOT-INNESCO` ha gia' ristretto il campo: ### **se il vuoto e' l'INNESCO, il calore non puo' sostituirlo** |

---

## ✅ **E IL 2026-10-02 `:M7` E' ARRIVATA: le decisioni 2 e 4 HANNO il loro numero**

**La riga «aspetta `:M7`» non aspetta piu'**, e la risposta e' ### **girata dalla parte sbagliata**
rispetto a come l'avevo posta. Sta in **`TERMOSTATO-E-FRENO`** e nel par. **(C-ter)** di
`doc/PIANO_divisione_e_calore.md`:

| | |
|---|---|
| ### **il ruolo DOMINANTE del termostato non e' rifornire: e' FRENARE** | rifornisce **`+3.678e+03`** in 55 passi e ### **toglie `−1.1691e+05`** in 94 ⇒ netto ### **`−1.1323e+05`** su 150 passi *(149 misurati)*. ### **Il prelievo e' `31.8` volte il rifornimento** |
| **il vuoto copre il termostato** | ### **SI', con un margine di `48.2`** *(`+1.775e+05` dallo scuotimento contro `+3.678e+03`)*, e lo copre **da solo** in **149 passi su 149** |
| ### **e il PICCO separa due regimi** | fino al passo 88: `W = −1.4102e+04`, rifornisce **55** e frena 32. ### **Dopo il passo 88: `W = −9.9126e+04`, rifornisce ZERO volte e frena in TUTTI e 62 i passi** |

### ⛔ **QUINDI IL RISCHIO CHE AVEVO SCRITTO NEL PIANO ERA ROVESCIATO, e lo annoto invece di riscriverlo**
Avevo scritto, come **il rischio vero** della temperatura per nodo: *«senza un «fuori» il sistema
puo' SOLO PERDERE»*. ### **Misurato: il pericolo e' l'opposto — senza il termostato il sistema puo'
solo CRESCERE**, con un vuoto che immette `+1.775e+05` e **nessuno che lo contrasti.**
### ➜ **E la (c) di Luca resta giusta** *(l'energia globale non si conserva)*: ### **ma non si
conserva VERSO L'ALTO.**

### 📌 **Precisazione di un numero del 2026-10-01**, e la faccio perche' esce dallo stesso `json`:
avevo scritto *«`xi` cambia segno UNA volta, al passo 56»*. ### **Il passo 56 e' l'ULTIMO con
`xi < 0`** *(`−7.480e-03`)* **e il 57 e' il PRIMO con `xi > 0`** *(`+2.871e-02`)*: il cambio sta
**fra i due**. *(Una volta sola: e' confermato.)*

---

# ⭐⭐ **REVISIONE DELLA VISIONE: LA MATERIA E' UNO STATO COLLETTIVO, LA CARICA E' UN VERSO DI ROTAZIONE** *(decisione di Luca, 2026-10-01 sera)*

> ### ⚠ **QUESTA DECISIONE RIVEDE TRE RIGHE DELLA VISIONE REGISTRATA QUI SOPRA.**
> **Le righe vecchie RESTANO leggibili** *(par.8: un ragionamento non si riscrive, si ANNOTA)*, e
> qui sotto ciascuna porta accanto ### **che cosa la sostituisce.**

## ⭐ **① LA MATERIA E' L'INTERFERENZA COSTRUTTIVA DI TANTI SOLITONI**

> ### **I NODI sono i solitoni. LA MATERIA e' uno STATO COLLETTIVO — una «massa» — NON un nodo.**

### ✅ **E il codice lo dice gia', in due punti** *(cercati per nome di funzione, non per riga)*:

| dove | la frase |
|---|---|
| `mitosi` | *«il **baricentro dell'interferenza (=la materia)** trasla in quella [direzione]»* |
| `classifica_topologia` | *«**baricentro dell'interferenza (dove sta davvero la massa)**, non il centro nominale»* |

### ➜ **Quindi la revisione non introduce un concetto nuovo: dichiara come LEGGE cio' che il codice
usava gia' come descrizione.** E per `9-ter` questo conta: ### **nessuna legge in piu'.**

## ⭐ **② LA CARICA E' IL VERSO DI ROTAZIONE COLLETTIVO DELLA FASE**

> ### **densita' di carica `∝ |ψ|² · ω` con `ω = phivel`; la carica di una MASSA e' la somma sui
> ### solitoni che la compongono.**

| | |
|---|---|
| ### **perche' NON dipende da una convenzione** | spostare **tutte** le fasi di una costante ### **non cambia il verso di rotazione**: `phivel` e' una **derivata**, e una traslazione rigida di `φ` la lascia identica |
| ### **che cos'e', in una riga** | e' la ### **carica di Noether della simmetria di fase globale** `φ → φ + c`. ### ➜ **Si conserva PER SIMMETRIA — non per una regola di nascita — SE il nucleo e' conservativo** |
| ### ⛔ **e oggi DUE leggi la violano** | ### **scrivono `phivel`**: il **termostato** *(dentro `step`: `self.phivel = _phivel_t + delta_phivel`)* e lo **scuotimento** *(`scuoti_vuoto`: `net.phivel[:net.n] += calcio`, l'**unica** scrittura di stato di quella voce — verificato dal sorgente)*. ### **E' un motivo IN PIU' per il nucleo reversibile**, non un difetto a se' |
| ### ✅ **e `phivel` E' la velocita' di fase**, non una mia lettura | il registro lo dichiara: `'phivel': ('finito', 'velocita di fase: entrambi i segni')` |

### 📌 **E `ω = phivel` chiude un cerchio col PRINCIPIO GUIDA** *(par.10 di `CLAUDE.md`)*:
*«lo spinore E' il tempo proprio della massa»*. ### **Un verso di rotazione della fase e' un
orologio con un senso di marcia** — ed e' la forma in cui *«materia contro antimateria»* diventa
**una proprieta' dello STATO COLLETTIVO** invece di un'etichetta per nodo.

## ⭐ **②-bis LA CARICA DI UNA MASSA: LA DEFINIZIONE** *(decisione di Luca, 2026-10-03)*

> ### **La carica di una massa e' il SEGNO PESATO COLLETTIVO che emerge dalla velocita' di fase
> ### di tutti i solitoni che la compongono.** Il ### **SEGNO** distingue materia da antimateria,
> il ### **VALORE** dice quanta carica.

### ⛔ **E' EMERGENTE e COLLETTIVA: nessun solitone *<<ha>>* una carica, ce l'ha la MASSA.**
Un nodo debole che ruota al contrario dentro una massa forte ### **non la rende antimateria.**

## ⚠ **LE DUE FASI, e quindi DUE CANDIDATE — e non sono la stessa cosa**

Ogni nodo ha ### **due** fasi, e il codice le tiene separate:

| | | |
|---|---|---|
| `phi_k` | la fase ### **PROPRIA** del nodo | `REGISTRO_METRI`, dominio `[0, 4pi)` |
| `theta_k = arg psi_k` | la fase del ### **CAMPO** nel nodo | e `psi_k = somma_j W_kj * amp * e^{i phi_j}` — ### **verificato dal codice**: `F = self._mat(w) @ (amp * np.exp(1j * self.phi))` |

```
Q_A = somma_k |psi_k|^2 * w_k * (phidot_k   - omega_vuoto)      intensita' del campo x rotazione PROPRIA
Q_B = somma_k |psi_k|^2 * w_k * (thetadot_k - omega_vuoto)      intensita' del campo x rotazione del CAMPO
```

### ⭐ **E `Q_B` COMPONE LE DUE COSE** *(conto del guardiano, prima della saturazione e con `W` simmetrica)*

```
Q_B = somma_j phidot_j * c_j     con   c_j = Re( e^{i phi_j} * conj( somma_k W_jk psi_k ) )
                                       c_j ~ intensita' del campo intorno a j  x  cos(phi_j - theta)
```

### ➜ **Cioe' la rotazione di ogni solitone PESATA PER QUANTO E' IN FASE COL CAMPO CHE LO
CIRCONDA: il nucleo in fase conta A FAVORE, il GUSCIO IN ANTIFASE conta CONTRO.**

### 📌 **Ed e' la STESSA FORMA dei pesi di `aggiorna_pesi_concorrenza`** *(`cos(phi_nodo -
phi_massa)`)*: ### **risponde da se' alla domanda sui PESI NEGATIVI di
`MASSE-PESI-SOVRAPPOSTE`** — il segno del guscio ### **non si decide, esce dalla formula.**

### ✅ **LA VERIFICA CHIESTA DAL GUARDIANO, FATTA: `satura()` cambia SOLO IL MODULO**

```
satura(f) = f / (1.0 + GAMMA * np.sqrt(np.abs(f)**2 + 1e-9))
```

Il denominatore e' ### **reale e positivo**, quindi ### **`arg(satura(f)) = arg(f)` esattamente**
*(in aritmetica esatta; nei float a meno dell'arrotondamento)*.

| | |
|---|---|
| ### ➜ **la struttura del conto REGGE** | `theta = arg psi = arg F`: ### **`thetadot` NON e' toccato dalla saturazione** |
| ### ➜ **cambiano SOLO i pesi `c_j`** | che prendono il `\|psi\|` ### **saturato** invece di `\|F\|`, come il guardiano prevedeva |

### ⭐ **`Q_B` E' LA CANDIDATA PREFERITA**, perche' e' la carica del ### **campo complesso** —
### **ma la scelta definitiva la da' la LAGRANGIANA** *(il par. qui sotto)* ### **oppure la misura
di quale delle due si conserva** *(`CARICA-SIMMETRIA-FASE`, misura `(c)`)*.

### ✅ **E LA PARTIZIONE DELL'UNITA' DA' UNA CONSERVAZIONE PER COSTRUZIONE**

```
somma_m Q_m = somma_k |psi_k|^2 (omega_k - omega_0) * (somma_m w_k^(m)) = somma_k |psi_k|^2 (omega_k - omega_0)
```

### ➜ **Non e' una proprieta' da verificare: e' un'IDENTITA'** — e vale per `Q_A` come per
`Q_B`, perche' il peso `w_k` e' fuori dalla parentesi. Ed e' una delle ragioni per cui la decisione
sui pesi viene ### **PRIMA** di `CARICA-ROTAZIONE`.

### ⚠ **MA VALE SOLO SUI NODI CHE APPARTENGONO A UNA MASSA, e lo aggiungo perche' cambia come
si legge il numero.** I nodi del ### **vuoto** hanno `w = 0` per ogni massa, quindi la loro carica
### **non entra** nella somma: l'identita' e' *somma delle masse = carica della ### **PARTE
MATERIA***, e il resto e' ### **il residuo del vuoto.**

| | |
|---|---|
| quel residuo | ha media ### **~zero per costruzione** *(e' proprio `omega - omega_vuoto` sul vuoto)*, ### **ma non e' zero: FLUTTUA** |
| ### ➜ **e' IL PAVIMENTO DI RUMORE della misura** | una `Q_massa` piccola ### **non si distingue dal residuo** finche' il residuo non e' misurato ### **accanto** |
| ### ✅ **e la definizione lo sopprime da se'** | il peso `\|psi_k\|^2` ### **schiaccia i nodi di vuoto**, dove il campo e' debole — ### **un pregio della formula, non un caso**. Ma ### **quanto** lo sopprima e' un numero, e va misurato |

### ✔ **E' DISTINTA DALLA CHIRALITA' SPINORIALE `perc_chi`, e la ragione e' FISICA:** in
fisica la carica elettrica ### **non dipende dallo spin**; l'unico punto in cui *<<mano>>* e carica
si toccano e' l'### **interazione debole** *(solo la chiralita' sinistra sente il `W`)*.
### **Il codice di oggi usa `perc_chi` come carica: e' LA COSA DA SOSTITUIRE.**

### ⛔ **E UNA FRASE DI QUESTA SCHEDA VA QUALIFICATA** *(la qualifico qui invece di lasciarla
come sta)*

La tabella del par.② dice: *«spostare tutte le fasi di una costante ### **non cambia il verso di
rotazione**: `phivel` e' una derivata, e una traslazione rigida di `φ` la lascia identica»*.
### **E' vero per `phivel` come derivata MATEMATICA, e non basta:**

| | |
|---|---|
| **1** | la fase ### **ASSOLUTA e' AVVOLTA**: `self.phi = (…) % self._dphi()` *(`:7607`)*, e la semina avvolge *(`:4825-4826`)*. ### ➜ **Una traslazione rigida e' esattamente una traslazione SOLO se `c` e' un multiplo di `_dphi()`** — e quindi ### **`c = _dphi()` e' il CONTROLLO POSITIVO** del test, che deve dare ### **byte-identico** |
| **2** | ### **`phivel` viene RISCRITTA ogni passo** come `_phivel_t + delta_phivel`, e `delta_phivel` lo calcolano leggi che leggono `phi`. ### ➜ **Se una usa la fase ASSOLUTA, dopo un passo `phivel` NON e' invariante** — e questa scheda dichiara gia' che ### **due leggi la scrivono** *(termostato e scuotimento)* |

### ➜ **La frase conflonde l'invarianza CINEMATICA di `phivel` sotto uno spostamento rigido**
*(vera nel continuo)* ### **con l'invarianza delle LEGGI che la aggiornano** *(non misurata)* —
ed e' la seconda che `CARICA-SIMMETRIA-FASE` misura.

### ⚠ **I LIMITI, DICHIARATI E ACCETTATI DA LUCA:** `Q` ### **non e' quantizzata** *(servirebbe
un meccanismo topologico o quantistico)*; e una carica ### **GLOBALE non produce da sola una
forza** *(servirebbe un campo di gauge ### **LOCALE** sugli archi; ### **se `tw` possa esserlo e'
una DOMANDA APERTA, non una risposta**)*.

## ⭐ **LA FORMA DELL'ENERGIA: UNA SOLA LAGRANGIANA** *(decisione di Luca, 2026-10-03)*

> ### **Non *<<aggiungere un'energia al codice che c'e'>>*, ma RIFORMULARE il modello come UNA
> ### SOLA LAGRANGIANA da cui escono TUTTE le leggi.**

```
L = somma_j  1/2 * I_j * phidot_j^2   -   V(phi, struttura della rete)
```

### **CON L'INTERFERENZA DENTRO `V`**, e il punto e' l'autoconsistenza: il campo collettivo
`psi_k = somma_j W_kj e^{i phi_j}` e' ### **CALCOLATO dalle fasi** — ### **non e' un secondo
campo indipendente** — ### **e agisce sulle fasi.** Un ### **CAMPO AUTOCONSISTENTE.**

### **LA FAMIGLIA, e la scelta e' fra due:**

| | | |
|---|---|---|
| ### **Kuramoto** | ### **DISSIPATIVO, primo ordine** | ### ⛔ **irreversibile PER COSTRUZIONE: NON e' la forma voluta** |
| ### **XY / sine-Gordon su reticolo** | ### **SECONDO ordine, CON INERZIA** | ### ✅ **conservativo**: energia conservata, carica di Noether, ### **reversibile** |

### ✅ **E IL SIMULATORE HA GIA' L'INERZIA — verificato: `phivel` E' IN `REGISTRO_STATO`.**
### **Quindi PUO' stare nella seconda famiglia.** Oggi ne e' fuori per cose ### **elencate, non
genericamente *<<dissipative>>***:

| | che cosa rompe la forma conservativa | dove |
|---|---|---|
| **1** | ### **termostato e scuotimento SCRIVONO `phivel`** | `step` *(`self.phivel = _phivel_t + delta_phivel`)* e `scuoti_vuoto` |
| **2** | ### **`beta * vd`** — uno smorzamento del primo ordine nell'accelerazione dell'arco | `:7896` `acc_t = cs_arco**2 * lap + src - beta * self.vd` e `:7967` |
| **3** | ### **i rilassamenti**: `_rep`, `peq`, `mem_mot` | — |
| **4** | ### **la memoria dove VINCE L'ULTIMO** | `MEM-HEBB-VERSO` |
| **5** | ### **le soglie scritte a mano** | — |

### ⭐ **E DA `L` ESCONO INSIEME, che e' il punto di farne UNA:**

| | |
|---|---|
| le ### **equazioni del moto** | per variazione |
| l'### **ENERGIA** | dalla traslazione nel tempo |
| la ### **CARICA DI NOETHER** | dalla simmetria di fase — ### **e dice QUALE fra `Q_A` e `Q_B`** *(il par.②-bis)* |
| la ### **REVERSIBILITA'** | ### **controllabile con `LOSCHMIDT-ECO`** |

### **E il campo SPINORIALE sarebbe un SECONDO campo VERO**, accoppiato nella ### **stessa `L`** —
non un'aggiunta a parte.

### ⛔ **IL PUNTO APERTO, DICHIARATO DA LUCA: LA CRESCITA DELLA RETE.** La nascita dei nodi
### **cambia il NUMERO dei gradi di liberta'**, e per questo ### **non c'e' una ricetta
standard**: una lagrangiana con un numero variabile di coordinate non e' il caso di scuola.
### ➜ **E' li' che il modello deve INVENTARE**, e dirlo e' meglio che nasconderlo dentro una
formula che vale solo a rete fissa.

### ⚠ **E UNA TENSIONE DA MISURARE, che aggiungo io:** nella lagrangiana `psi` e' ### **una
FUNZIONE delle `phi`**; nel codice e' una ### **CACHE** — `self.psi = self.satura(F)` la
ricalcola, ma ### **altre leggi la LEGGONO prima del ricalcolo** *(fra cui `lambda_nodi`)*.
### ➜ **Le due cose coincidono SOLO SE nessuna legge legge una `psi` stantia**, e
### **`PSI-FLASH` e' il caso MISURATO in cui una `psi` di lunghezza sbagliata cambiava la fisica**
*(`lambda` da `~0.60` a `0.80`, `|psi|` ### **x1.62 per TUTTI**)*. ### **E' un vincolo
VERIFICABILE della riformulazione, non una nota.**
### ⚠ **E `psi` e' in `REGISTRO_STATO`:** per la lagrangiana e' ### **derivata**, per il codice
e' ### **una cache letta come stato**. ### **Quale delle due classificazioni valga e' esattamente
la domanda che `L` risolve** — e finche' non e' risolta, ### **le due letture convivono.**

## ⛔ **③ `perc_chi` NON E' QUESTA CARICA, e lo DICHIARO**

| | |
|---|---|
| `perc_chi` | il **segno del foglio della doppia copertura** dello spinore *(`CARICA-DI-GAUGE`)* |
| ### **e il suo segno e' una CONVENZIONE al 100 %** | misurato su **tre** run: cambiando il rappresentante canonico si ribaltano ### **12812/12812, 12782/12782, 14000/14000** cariche — **frazione `1.000000`** |
| ### ➜ **la carica della revisione e' un'ALTRA grandezza** | viene da `|ψ|²·phivel`, ### **non dal foglio dello spinore.** Chiamarle entrambe *«carica»* sarebbe ### **la collisione di nomi che l'indice esiste per curare** *(`A3` era tre cose)* |

### ⚠ **E questo NON dice che `CARICA-DI-GAUGE` sia risolta:** dice che ### **quel difetto riguarda
`perc_chi`, non la carica della visione.** La voce resta **aperta**, e la sua misura resta valida.

## ⭐ **④ LA CHIRALITA' SPINORIALE COLLETTIVA E' UNA GRANDEZZA DISTINTA**

> ### **Somiglia a un'ELICITA'. NON va identificata con la carica senza un argomento.**

### ➜ **E' la terza colonna della tabella di `GEOM-SENZA-VERSO`, letta sullo stato COLLETTIVO
invece che sul nodo:** li' le tre grandezze con tre mestieri sono `perc_geom` *(«avvolto si'/no»)*,
il **verso di rotazione**, e `perc_chi` *(il foglio)*. ### **La revisione aggiunge che il «verso di
rotazione» e la «chiralita' spinoriale» sono DUE cose anche loro**, e che la **carica** e' il primo.

## 🔁 **LE TRE RIGHE RIVISTE, una per una**

| la riga vecchia | ### **cio' che la sostituisce** |
|---|---|
| **(a)** *«la nascita di un nodo ha TRE ESITI: spazio · materia · materia e antimateria»* | ### **UN SOLO TIPO DI NASCITA DI NODO, in TRE REGIMI**: ① **vuoto → spazio** · ② **interferenza costruttiva → RAFFORZA una massa** · ③ **regime di coppie**. ### **Non sono tre eventi diversi: e' un evento in tre regimi**, e `peq` resta il riferimento che li separa |
| ### **criterio 8** *«la materia carica nasce a coppie: DUE NODI NUOVI, uno `+1` e uno `−1`»* | ### **una coppia di PATTERN (masse) con VERSO DI ROTAZIONE OPPOSTO**, che nascono e si annichilano **insieme** e **in modo reversibile**. ### ⛔ **NON «due nodi nuovi»:** la nascita di nodi e' ### **SOLO SPAZIO**, e resta ### **l'UNICA FRECCIA del tempo** |
| ### **decisione 1** *«`tw` e' qualcosa di simile a una CARICA»* | ### **`tw` e' una TENSIONE che PAGA LO SPAZIO, NON una carica.** La carica e' il verso di rotazione. ### ➜ **E ne segue una verifica, non una legge: che le DIVISIONI non cambino la carica delle masse** |

### 📌 **Che cosa cambia in pratica, e vale la pena dirlo in una riga**
La revisione **sposta la conservazione** da *«un conteggio di nodi `±1`»* a ### **«una somma su uno
stato collettivo»** — e con lei ### **sposta anche il posto in cui si verifica:** non piu' il
`d_somma` di un evento di nascita *(`:G4`)*, ma ### **la carica di ogni MASSA nel tempo**
*(`CARICA-ROTAZIONE`)*.

## 🗣 **NOTA DI LINGUAGGIO, per chi legge il repo da fuori** *(e va dichiarata, non assorbita)*

| la parola | che cosa significa **in fisica** | che cosa significa **in questo repo** |
|---|---|---|
| ### **«solitone»** | lo **stato collettivo LOCALIZZATO** | ### **la MASSA** *(l'interferenza costruttiva di tanti nodi)* |
| ### **i «nodi» di questo modello** | — | ### **somigliano a QUANTI DI SPAZIO**, non a solitoni |

### ➜ **Il repo MANTIENE i suoi nomi** *(par.9: un reperto non si riscrive, e «nodo» vive in
centinaia di referti e di `json`)*, ### **ma la corrispondenza va DICHIARATA**, senno' chi legge da
fuori legge *«solitone»* e pensa alla massa mentre il codice intende il nodo.

## 📐 **LA MISURA IN CODA: `CARICA-ROTAZIONE`** *(NON oggi)*

| | |
|---|---|
| **che cosa misura** | per **ogni massa**, la somma di ### **`|ψ|² · phivel`** nel tempo |
| **le tre domande** | ① **esistono masse di segno opposto?** · ② **quanto varia per PASSO?** · ③ **quanto varia per VOCE** *(scuotimento, termostato, `step`, `mitosi`)* |
| ### **come si misura il «per voce»** | con la **spia sui confini di voce** — il controllo del **commit 1**, che gira dopo **ogni** voce. ### **E' la stessa imbragatura di `:M1`, `:M4`, `:M6`** |
| ### **da cosa dipende** | ### **da `MASSA-ID`**: *«per ogni massa»* richiede di sapere **quali nodi** sono una massa, e `MASSA-ID` e' **BLOCCATA** *(due blocchi, verificati dal disco il 2026-09-27)*. ### **Lo dico invece di scoprirlo girando** |

## 🛑 **E LE VOCI SULLA CARICA E SULLE COPPIE NON SI IMPLEMENTANO**

> ### **Finche' Luca non ha CHIUSO questa revisione, `CARICA-DI-GAUGE`, `SCHWINGER-UN-NODO` e il
> ### criterio 8 NON si curano.**

### ➜ **La ragione e' precisa:** la revisione ### **cambia che cosa sia la carica**, quindi
cambierebbe ### **l'obiettivo** delle loro cure. Curarle adesso vorrebbe dire ### **far nascere le
coppie neutre in una grandezza che fra una settimana non e' piu' quella che si conserva.**
### ⚠ **E nel frattempo le loro MISURE restano valide:** `:G1` e `:G4` misurano `perc_chi`, e
`perc_chi` **continua a essere quello che e'.**

---

# 🔄 **LA DIREZIONE DI LUCA SULLA REVERSIBILITA': `REVERSIBILITA-LOCALE`** *(2026-10-02, **IN VALUTAZIONE**)*

> ### ⚠ **E' REGISTRATA COME «IN VALUTAZIONE», NON COME DECISIONE.** Lo scrivo cosi' perche' Luca
> l'ha data cosi': ### **una direzione da valutare, non una legge da applicare.** `stato = teoria`
> nell'indice.

> ### **REVERSIBILITA' LOCALE, IRREVERSIBILITA' GLOBALE.**
> L'irreversibilita' globale ### **EMERGE dal caos delle leggi locali reversibili** *(Boltzmann)*.
> ### **La SOLA freccia fondamentale ammessa e' la CRESCITA DELLO SPAZIO** — la nascita dei nodi.

## 📐 **IL CRITERIO MISURABILE, e questo e' cio' che la rende valutabile e non un desiderio**

> ### **«L'eco di Loschmidt FALLISCE SOLO nella voce della NASCITA.»**

### ➜ **Che cosa lo deciderebbe:** `LOSCHMIDT-ECO`. ### **Se l'eco fallisse anche in `step`, in
`chiudi` o nel termostato, la direzione NON sarebbe soddisfatta dal codice di oggi** — e allora si
saprebbe **dove** e **di quanto**, invece di saperlo in generale.

## ⚠ **TRE COSE CHE QUESTA DIREZIONE CHIEDE, e che oggi non ci sono**

| | |
|---|---|
| **1** | ### **il termostato NON e' reversibile**: il richiamo `−ξ` e il `clip(±2)` sono un attrito, e `:M7` misura che ### **frena in 94 passi su 149** |
| **2** | ### **le ESTRAZIONI CASUALI non sono reversibili** come sono scritte: scuotimento, nascite, Schwinger pescano da `net.rng`, e ### **tornare indietro vorrebbe dire ri-pescare gli stessi numeri in ordine inverso** |
| ### **3** | ### **`phi[ii] = (...)` con `ii` RIPETUTO fa vincere l'ultimo**, e ### **una scelta implicita fatta dall'ordine di un array non ha un'inversa** *(`MEM-HEBB-VERSO`, criterio 7 del piano del calore)* |

### ➜ **Nessuna delle tre e' un argomento CONTRO la direzione:** sono ### **l'elenco di cio' che la
direzione implicherebbe di cambiare**, e serve averlo scritto **prima** di chiamarla una decisione.

---

# ⭐ **STELLA POLARE: LE LEGGI SONO SIMMETRICHE, GLI STATI SCELGONO** *(Luca, 2026-09-29)*

> ### ✅ **E IL 2026-10-01 LA STELLA POLARE HA LA SUA PRIMA APPLICAZIONE: `FRAZIONE-DIVISIONE`.**
> **Domanda di fisica di Luca:** *«perche' per forza il punto medio?»* — e ### **il punto medio NON
> E' DERIVATO**: e' la scelta simmetrica, ### **ma ignora che i due estremi hanno STATI DIVERSI.**
> ### ➜ **La forma giusta e' `t = f(stato_a, stato_b)` con `f(a,b) = 1 − f(b,a)`:** scambiando gli
> estremi il figlio va nella posizione **speculare**, e ### **il punto medio e' solo il caso in cui
> gli stati sono UGUALI.** ### **La legge resta simmetrica; sceglie lo STATO.**
> **La voce e' `FRAZIONE-DIVISIONE`**, i criteri sono in `doc/PIANO_riordino_mitosi.md`, e
> ### **quale grandezza decide `t` lo decide Luca.**

> ### ✅ **DUE DECISIONI DI LUCA DEL 2026-10-01, e questa e' la loro REGISTRAZIONE**
> *(par.4: un'approvazione in chat non basta — e la prima volta non l'avevo scritta)*
>
> | | |
> |---|---|
> | ### **i QUATTRO EVENTI di nascita** | `semina` · `divisione` · `Schwinger` · `allaccio`: ### **APPROVATI.** Sono la base del registro delle regole di nascita *(`doc/REGOLE_nascita.tsv`)*, e senza di loro le sei *«incoerenze»* di quel registro ### **tornerebbero a essere difetti** |
> | ### **la TERZA VIA, il VELENO** | ### **APPROVATA nella forma RAFFINATA**: controllo di finitezza ### **PER GRANDEZZA**, con le esenzioni ### **dichiarate nel registro** *(`eta`: `inf` per il vuoto DATO)* — ### **lo stesso schema del TIPO.** ### **«Derivata sporca» e «`peq` da calibrare» diventano UN SOLO meccanismo con UN SOLO nome** *(`peq` nasce `NaN` «da calibrare» a `:3693` e a `:7165`, e `step` la calibra: il sistema lo fa **gia'**)*. ### **Prezzo ACCETTATO:** al passo della nascita il sigillo confronta al byte ### **lo STATO, non le derivate** |

> ### ⚠ **E' un PRINCIPIO, non ancora una legge del codice:** non porta un marcatore `SCHEDA`,
> perche' oggi **non governa nessuna funzione modificata**. ### **Il marcatore arriva col codice**,
> quando la strada **(ii)** si cabla. La voce e' **`GEOM-SENZA-VERSO`**, il documento e'
> `doc/GEOM_SENZA_VERSO.md`.

## **A. Nessuna legge deve preferire un verso di rotazione**

### **Se un verso prevale, deve EMERGERE dall'evoluzione — rottura SPONTANEA — non essere scritto
nella legge.**

## **B. Una rottura ESPLICITA e' ammessa solo come POSTULATO DICHIARATO**

**un solo termine · nominato · col suo peso · accendibile e spegnibile · confrontabile.**
### ⛔ **Mai come effetto collaterale di un valore assoluto.**

## **C. Tre grandezze, tre mestieri, mai mescolati**

| grandezza | mestiere | da dove viene |
|---|---|---|
| `perc_geom` | ### **«avvolto si' o no»**: **DOVE** c'e' materia avvolta | l'**intensita'** `\|tw\|` |
| *(oggi non esiste)* | ### **VERSO DI ROTAZIONE**: orario / antiorario | il ### **SEGNO della circolazione** della torsione |
| `perc_chi` | ### **CARICA**: materia / antimateria | il **foglio della doppia copertura** dello spinore |

> ### 📌 **E' la stessa forma dell'errore che `CHI_COOP` ha GIA' corretto il 2026-09-21:** allora
> **una sola variabile** *(`perc_chi`)* faceva **due lavori** — la **carica** e la **geometria** — e
> fu **divisa**. ### **Rimettere il verso dentro `perc_geom` ripeterebbe quell'errore**, ed e' la
> ragione per cui la strada **(i)** e' **scartata**.

## ⛔ **IL SOSPETTO, e motiva `A`**

> **Specchiando il sistema** *(fasi invertite)* **`tw` cambia segno, `|tw|` NO — quindi `perc_geom`
> no — quindi `twist_dip = pi/2 (chi_i - chi_j)` *(`:6061`)* NON cambia segno.**

### ➜ **La legge aggiunge alla torsione LO STESSO contributo nel mondo specchiato: una rottura
ESPLICITA della simmetria, probabilmente INVOLONTARIA.** E se i nuclei risultassero tutti dello
stesso verso, ### **potrebbe essere questo termine e non fisica emergente.**

**L'anello:** `tw` → `|tw|` → `perc_geom` → `twist_dip` → `tw`. **E l'ordine nel passo conta:** i
lettori della catena stanno a `:5908` e `:5917`, ### **PRIMA** della riscrittura di `perc_geom` a
`:6083` — quindi il frame-drag legge **il valore del passo precedente**.

## La direzione scelta, e come si prova

**Strada (ii):** `perc_geom` resta *si'/no*; la catena della rotazione ### **legge il verso dalla
circolazione con segno**. **La (iii)** *(lasciare tutto)* resta **solo se la misura mostra che il
problema non esiste** — e allora ### **va scritto qui PERCHE' un'intensita' vale come chiralita'**.

### 🪞 **LA PROVA DELLO SPECCHIO** *(criterio fissato prima dei numeri)*
Copia **A** normale e copia **B** **specchiata** dallo stesso stato: se le leggi sono simmetriche,
### **B deve restare lo specchio di A entro l'errore numerico**, e si riporta ### **la prima
grandezza e il primo passo in cui lo specchio si rompe, con la riga che lo produce**.
### ⛔ **E la trasformazione di specchio la DEFINISCE LUCA prima del giro: dire quali grandezze
cambiano segno e quali no e' una scelta di FISICA, non una convenzione di misura.**
**Il caso che deve fallire:** con `twist_dip` com'e', lo specchio ### **deve rompersi**; se non si
rompe, ### **il sospetto cade, e si dice.**

---

# ⭐ **I DUE PRINCIPI DI LUCA: IL DECADIMENTO È UNA TRASFORMAZIONE, LA MEMORIA DÀ UN VERSO** *(decisione di Luca, 2026-10-07)*

> ### 📌 **Sono i due principi che `A15` rende VINCOLANTI.** Senza `A15` sarebbero due
> frasi; con `A15` sono ### **una forma che ogni legge nuova deve avere.**

## `P-decadimento` — **ogni decadimento è una trasformazione**

> **«Ogni decadimento è una trasformazione: ciò che una grandezza perde rilassando diventa
> calore del vuoto locale. Nessun termine fa sparire energia. Le strutture decadono,
> l'energia si trasforma.»**

### **CHE COSA VINCOLA, in pratica**

Ogni termine della forma ### **`− dt · X / τ`** deve avere ### **una destinazione.**
### ⛔ **Oggi NESSUNO ce l'ha**, e l'inventario completo sta in
`doc/MEMORIE_MANCANTI.md` §`3`.

| | |
|---|---|
| la legge | *«le strutture decadono»* — ### **il decadimento NON si vieta** |
| il vincolo | *«l'energia si trasforma»* — ### **il termine deve CEDERE a qualcuno**, non annullarsi |
| la destinazione | ### **il calore del VUOTO LOCALE** *(`A15.3`, corollario di `A14`)* |
| per un ARCO | ### ⚠ **a chi?** La proposta e' ### **metà a ciascun estremo** — ### **ed è una PROPOSTA, non una legge**: una regola diversa *(per esempio pesata su `\|psi\|²`)* e' altrettanto scrivibile, e ### **la scelta è di Luca** |

> ### ⛔ **E MANCA IL NUMERO, non la regola:** per dire ### **quanta** energia cede un
> termine serve ### **l'energia dell'arco**, che oggi ### **non è definita** —
> `ENERGIA-NON-DEFINITA`. ### **Quindi `P-decadimento` oggi si può SCRIVERE come forma e
> NON si può BILANCIARE come numero**, e dirlo è parte del principio.

## `P-memoria` — **uno scalare con memoria acquista un verso**

> **«Uno scalare con memoria acquista un verso: la memoria dà la direzione.»**

### **PERCHE' NON E' UNA METAFORA, e si vede sull'esempio che il sistema HA GIA'**

`tw` è ### **uno scalare d'arco**, e ### **porta memoria**: la legge curata lo aggiorna con
`tw += _w4(dph − twp) + (twist_dip − twp_dip) − dt_e·tw/τ_tw`.
### ➜ **La differenza `δ = dph − tw` è una MEDIA MOBILE della differenza di fase**
*(l'algebra è nel §`4b` del rapporto)*, e ### **una media mobile ha un verso che il valore
istantaneo non ha:** dice ### **da che parte si stava andando.**

> ### ⚠ **E IL VERSO NON E' GRATIS: `P-memoria` dice che la memoria LO DA', non che sia il
> verso GIUSTO.** ### **Quale verso serva — e se serva un segno o un asse — resta la
> decisione `A3` della ripresa**, e ### **`A1` la misura.**

## ⚠ **L'OSSERVAZIONE DI LUCA, DA MISURARE — e diventa `M5d`**

> **«Una memoria che dimentica dissipa SOLO quando ha qualcosa da dimenticare. Dove la
> struttura è stabile la memoria raggiunge il presente e non dissipa; nel vuoto rincorre e
> dissipa.»**

### ✔ **E' UNA PREVISIONE FALSIFICABILE, non un'intuizione**, perche' dice ### **dove** la
dissipazione deve stare:

| | |
|---|---|
| in ### **MATERIA** | la struttura e' stabile → la memoria ### **ha raggiunto il presente** → ### **dissipa POCO** |
| nel ### **VUOTO** | la struttura cambia → la memoria ### **rincorre** → ### **dissipa MOLTO** |

**LA MISURA, ed è `M5d` di `A1`:** la potenza persa nel rilassamento della torsione,
### **`Σ tw² · dt_e / τ_tw` per passo**, ### **per classe** e ### **per nodo** *(metà a
ciascun estremo, che è la proposta di `P-decadimento`)*.

> ### ⛔ **IL CRITERIO, fissato PRIMA dei numeri** *(e sta nel task history di `A1`)*:
> ### **«la dissipazione sta nel vuoto» se la potenza per nodo MEDIANA in MATERIA è meno di
> UN QUARTO di quella in VUOTO, a TUTTI i passi pesanti dopo il `300`.**
>
> ### ⚠ **E SE NON FOSSE COSI', NON SAREBBE UN DETTAGLIO:** vorrebbe dire che la torsione
> dissipa ### **dove la materia sta**, cioè che il termine di rilassamento ### **non è il
> costo di una memoria che rincorre** ma qualcos'altro. ### **La previsione è di Luca, il
> numero no.**

## 📌 **DOVE SI AGGANCIANO**

| | |
|---|---|
| `A15` | li rende ### **vincolanti**: `A15.3` È `P-decadimento`, la ### **conseguenza** di `A15` È `P-memoria` |
| `A14` | `P-decadimento` è ### **il suo corollario locale**: *«nessun termine fa sparire energia»* |
| `CONSERVAZIONE-LOCALE` | la voce che tiene ### **l'elenco delle violazioni** |
| `ENERGIA-NON-DEFINITA` | ### ⛔ **il prerequisito**: senza l'energia dell'arco il bilancio non si scrive |
| `VUOTO-LOCALE-DETERMINISTICO` | ### **la destinazione** del calore |
