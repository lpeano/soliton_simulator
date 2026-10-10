# IL PROTOTIPO DELLA CAMMINATA A MONETA — **il primo codice di fisica dell'era `2`**

> ### ⛔ **QUESTO FILE E' SCRITTO E COMMITTATO *PRIMA* DEL CODICE** *(par. `8`)*, e il rito
> serve a una cosa sola: **l'ordine e' verificabile da git** — il commit di questo documento
> e' **antenato** dei commit del banco — ### **invece che asserito da me.**

**Il mandato:** Luca, `2026-10-10`, *«IL PROTOTIPO DELLA CAMMINATA (`doc/PIANO_era2.md`, <<IL
PROTOTIPO DI CONFRONTO>>). E' il PRIMO codice di fisica dell'era `2`. Un solo mandato, commit +
push a ogni tappa»*. **Il punto `0`** *(la correzione del guardiano)* **e' gia' fatto**, nel
commit `10f7c94`.

---

## `1` RAGIONAMENTO PRELIMINARE — **che cosa credo PRIMA di guardare, e che cosa NON SO**

### ⭐ **CIO' CHE CREDO PER COSTRUZIONE, cioe' che mi aspetto di VERIFICARE e non di scoprire**

| | che cosa | perche' lo credo |
|---|---|---|
| `a` | **l'isotropia** | la moneta di Grover e' `(2/k)·Σ − I` sulle estremita' del nodo: e' **invariante per permutazione delle estremita'** per costruzione. ### ⚠ **Quindi se la misura dice di no, il difetto e' NELLA MIA IMPLEMENTAZIONE**, non nella fisica — e questo va detto prima, perche' altrimenti un rosso diventerebbe <<una scoperta>> |
| `b` | **il cono esatto** | lo spostamento scambia le due estremita' di **un** arco: dopo `T` tick l'ampiezza non puo' aver attraversato piu' di `T` archi. ### **E- un criterio AL BIT**, non statistico |
| `c` | **la norma conservata** | moneta di Grover **unitaria** + spostamento **permutazione** + le fasi non lineari **a modulo 1** ⟹ `Σρ` e' conservata **esattamente**, a meno dell'arrotondamento |
| `d` | **la simmetria `C` della camminata lineare** | con `C ψ = σ_x ψ*` *(la derivazione e' qui sotto)*: la moneta di Grover e' **reale** e agisce **identica sulle due componenti**; lo spostamento e' una **permutazione reale**; la moneta di banda e' `exp(-i θ σ_z)` e **commuta con `C`** perche' `σ_x σ_z = −σ_z σ_x` |
| `e` | **che `(A)` ROMPA `C`** | la fase `(A)` e' `exp(-i g ρ dτ)`, **scalare e `C`-PARI** — e un fattore scalare commuta con `C` **solo se e' `C`-DISPARI.** ### ⛔ **Quindi `(A)` deve fallire la lettura `5`: e- il BRACCIO CHE DEVE FALLIRE**, e lo prevedo **prima** |
| `f` | **che `(B)` sia `C`-simmetrica** | `(B)` e' la fase **proporzionale allo SBILANCIAMENTO DI BANDA** `s = ρ₊ − ρ₋`, che e' `C`-**dispari** — la derivazione e' qui sotto, ed e' **il motivo per cui l'ho scelta lei** |

### 📌 **LA DERIVAZIONE DI `C`, e perche' non e' una scelta ma l'unica che chiude**

Lo stato e' **un'ampiezza a due componenti per ogni estremita' d'arco**, e le due componenti
**sono le due bande**. La moneta di banda deve **separarle** con un angolo `∝ dτ` *(«è la
massa»)*, quindi e' **diagonale**: `M(θ) = exp(-i θ σ_z)`, `θ = dτ_k`.

Pongo **`C ψ = σ_x ψ*`** *(scambio delle bande + coniugazione)*. Allora:

| | il conto | l'esito |
|---|---|---|
| `M` | `C M ψ = σ_x (e^{-iθσ_z}ψ)* = σ_x e^{+iθσ_z} ψ* = e^{-iθσ_z} σ_x ψ*` | ### **`C M = M C`** |
| Grover | reale, e **la stessa matrice su entrambe le componenti** | **commuta** con `σ_x` e con `*` |
| spostamento | permutazione **reale** delle estremita' | **commuta** |
| fase scalare `e^{-iφ}` | `C e^{-iφ} ψ = e^{+iφ} Cψ`, mentre `e^{-iφ(Cψ)} Cψ` | ### ⛔ **commuta SOLO SE `φ(Cψ) = −φ(ψ)`** |

### ⭐ **E QUELLA RIGA E' TUTTO IL PUNTO:** una fase scalare e' `C`-simmetrica **solo se e'
`C`-DISPARI.** `ρ₊+ρ₋` e' `C`-pari ⟹ **`(A)` rompe `C`**; `ρ₊−ρ₋` e' `C`-dispari ⟹
**`(B)` la rispetta.**

### ✅ **E `(B)` NON E' UN TRUCCO ALGEBRICO, ha un senso fisico che si puo' dire:** su un
cluster **tutto nella banda `+`** vale `s = ρ`, quindi **`(B)` agisce esattamente come `(A)`**;
sul suo coniugato nella banda `−` vale `s = −ρ`, quindi la fase **cambia segno** — che e'
**esattamente cio' che serve perche' il coniugato evolva coniugato.** ### ⛔ **`(A)` invece da'
la STESSA fase alle due bande, e cosi' tiene una e disfa l'altra.**

### ⚠ **CHE COSA NON SO — e lo scrivo adesso, perche' dopo sembrerebbe una scusa**

| | non so | e come lo sapro' |
|---|---|---|
| `1` | **se esista una quantita' conservata usabile come ENERGIA** per le monete non lineari | e' **la lettura `3`**, ed e' la domanda `[[DOMANDA-QUANTITA-CONSERVATA]]`. ### ⛔ **Se non esiste per nessuna non linearita' ammissibile, e' il criterio di RIAPERTURA della decisione `10`** |
| `2` | **se un cluster in fase resti coerente, con QUALUNQUE moneta** | lettura `4`. ### ⚠ **Non ho nessuna ragione teorica per aspettarmelo:** la camminata lineare **disperde**, e la non linearita' deve **compensare la dispersione** — un bilancio che **non ho calcolato** |
| `3` | **se il grafo irregolare INTRAPPOLI** | lettura `4`, ultimo braccio. ### **La localizzazione su grafi disordinati e' un fenomeno noto, ma su QUESTO grafo e con QUESTA moneta non lo so** |
| `4` | **quanto cambia la fisica un fattore comune sugli `r_k`** | lettura `7` **rovesciata**: so **che** cambia *(punto `0`)*, ### **non QUANTO** |
| `5` | **se il confronto con l'integratore a strati converga come `dt²` su un grafo IRREGOLARE** | lettura `1`, secondo braccio. ### ⚠ **E- possibile che non converga affatto**, e sarebbe **un risultato**, non un fallimento |
| `6` | ### ⛔ **se la <<frequenza di un nodo>> sia una grandezza ben definita** | e' **il rischio piu' serio della lettura `4`**: misuro `ω_k` come **avanzamento di fase per tick**, e **l'argomento di un numero quasi nullo e' rumore.** ### ✅ **LA DIFESA, decisa ORA e non dopo:** la dispersione si misura **pesata con `ρ`**, e la fase si prende **sull'ampiezza TOTALE del cluster**, non nodo per nodo — cosi' **nessun pavimento, nessuna soglia a mano** *(`A11`)* |

---

## `2` PROGETTAZIONE DEL RAGIONAMENTO — **i passi, cosa decide ciascuno, cosa mi FERMA**

> ### ⛔ **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI** *(par. `8`, e
> `PATTERN_DI_PROVA`)*. ### **Una lettura decisa dopo i numeri non e' una lettura: e' una
> spiegazione.**

### **LA SCENA, dichiarata** *(e ogni scelta e' una riga, non un'abitudine)*

| | che cosa | il valore | perche' |
|---|---|---|---|
| grafo irregolare | nodi · gradi | **`120` nodi, gradi fra `2` e `6`** | *«decine-centinaia di nodi, gradi diversi»*. ### ⛔ **Costruito SENZA `pos`**: solo liste di adiacenza |
| grafo regolare | il controllo | **`120` nodi, `4`-regolare** *(circolante)* | il controllo dice **che cosa e' colpa dell'irregolarita'** e che cosa no |
| stato | per estremita' d'arco | **un'ampiezza `C²`** | le due componenti **sono le due bande** |
| seme | esplicito | **`11`** | e' il seme che questo repo usa da sempre; ### **dichiarato, non nascosto** |
| `r_k` | il ritmo locale | **dato**, estratto con il seme in `[1/2, 1]` | il mandato lo dice: *«nel prototipo `r_k` e' dato (non derivato)»*. ### ⚠ **La derivazione e' la domanda aperta**, non un pezzo di questo lavoro |
| `cs_k` | la velocita' locale | **`1` ovunque**, dichiarato | ### ⛔ **QUESTO PROTOTIPO NON PROVA LA `cs` LOCALE**, e lo dico invece di lasciarlo credere: i punti `3`-`6` di `[[TEMPO-PROPRIO-LOCALE]]` restano **da provare altrove** |
| `g` | la forza della non linearita' | ### **SCANSIONATA** su `{0, 1/4, 1/2, 1, 2}` | ### ⛔ **`A1`: non si tara un numero.** Un fenomeno che vive **in una finestra stretta di `g`** e' **imposto**, e la scansione e' il modo di vederlo |
| `c` | il fattore della lettura `7` | ### **`1/2` e `2`**, e **solo potenze di due** | ### ⭐ **PERCHE' `c·r` DEVE ESSERE ESATTO AL BIT:** con un `c` qualunque misurerei **il mio arrotondamento** invece della fisica |
| passi | le corse | **`60`** tick per i bracci strutturali, **`400`** per cluster e conservazione, **`4` semi** | *«corse brevi (minuti, non ore)»* |

### **LE SOGLIE, FISSATE ADESSO — e OGNUNA E' DERIVATA, nessuna scelta a mano**

> ### ⛔ **`A1` vale anche per le soglie:** una soglia scelta a occhio e' **una manopola**, e
> una misura con una manopola **non decide niente.** ### ✅ **Qui ogni soglia esce da un
> CONTEGGIO DI OPERAZIONI o dall'errore della propria stima.**

| | la soglia | la forma | da dove viene |
|---|---|---|---|
| `S1` | **isotropia** | `tol = T · g_max · ε · ‖ψ‖`, con `ε = 2.22e-16` | ### **il conteggio delle operazioni**: ogni tick somma `≤ g_max` termini per nodo, e gli errori si sommano al piu' linearmente nei tick |
| `S2` | **cono** | ### **`0.0` ESATTO** *(al bit)* | non e' una tolleranza: ### **oltre il cono l'ampiezza non e' MAI STATA TOCCATA.** ### ⚠ **Un effetto piccolo ma non nullo e' una VIOLAZIONE** |
| `S3` | **norma** | `|Σρ − 1| ≤ passi · n_est · ε` | lo stesso conteggio: `n_est` ampiezze toccate per tick |
| `S4` | **pendenza nulla** | `|pendenza| ≤ 3·σ_pendenza` | ### ⭐ **la soglia e' l'errore della stima stessa**: niente numero esterno |
| `S5` | **`dt²`** | `|pendenza − 2| ≤ 3·σ_pendenza` su `≥ 4` valori di `dt` | ### ⚠ **Due punti sono una retta, non uno scaling** *(`TAGLIA-FINITA`)* |
| `S6` | **coniugazione di `(B)`** | ### **`0.0` ESATTO** fra il run `+` e il coniugato del run `−` | se `C` e' una simmetria **esatta** del passo, i due run sono **coniugati AL BIT**; ### ⭐ **e se non lo sono, la mia implementazione ha un'asimmetria in virgola mobile, che e' un difetto MIO e va detto** |

### **I PASSI, e cosa decide ciascuno**

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| `0` | **l'operatore `C`, e la prova che la camminata lineare e' `C`-simmetrica** | se la lettura `5` **si puo' formulare** | ### ⛔ **se la camminata lineare NON e' `C`-simmetrica: STOP e lo scrivo.** Senza `C` esatta, *«materia e antimateria si comportano uguale»* **non ha un significato misurabile** |
| `1` | **il banco: scena, stato, determinismo** | se le misure sono **ripetibili** | ### **se due processi non danno byte identici: STOP.** Una misura non riproducibile non e' una misura |
| `2` | **letture `1`, `2`, `6`** *(isotropia, cono, `r=1`)* | se **l'implementazione** e' quella che credo | un rosso qui e' **un difetto mio**, non un risultato: si cura e si ripete |
| `3` | **lettura `3`** *(la quantita' conservata)* | se la decisione `10` **regge o si riapre** | niente mi ferma: ### **anche <<non esiste>> e' un risultato**, ed e' il criterio di riapertura |
| `4` | **letture `4` e `5`** *(cluster, materia/antimateria)* | se `(A)` e `(B)` **servono** | ### ⚠ **se `(A)` NON fallisce la lettura `5`, si ferma tutto:** vorrebbe dire che **non ho capito la simmetria**, perche' la derivazione dice che **deve** fallire |
| `5` | **lettura `7`** *(il gauge, rovesciato)* | **quanto** la scala assoluta di `r` e' fisica | — |
| `6` | **il referto** | che cosa **sblocca** o **riapre** nell'albero | — |

---

## `3` LA STELLA POLARE — **le cinque risposte, per iscritto** *(`[[L-STELLA]]`)*

| | la domanda | la risposta, per questo lavoro |
|--:|---|---|
| `1` | **`A14`: conserva energia e carica LOCALMENTE?** | ### ✅ **LA NORMA SI': LOCALMENTE E PER COSTRUZIONE.** La moneta mescola **solo dentro un nodo**, lo spostamento **solo lungo un arco**, le fasi non lineari **non cambiano i moduli**: c'e' **un'equazione di continuita' per `ρ`** e il flusso e' **sull'arco**. ### ⛔ **L'ENERGIA: NON LO SO, ED E' LA LETTURA `3`** — e il non saperlo e' **dichiarato**, non nascosto |
| `2` | **a quale dei TRE GRADINI arriva?** | ### **(a) ROBUSTO AL RUMORE NUMERICO: SI'** — bracci **al bit** e `4` semi. ### **(c) COINCIDE CON UN LIMITE NOTO: SI', in due punti** — `r=1` coincide **al bit** con la moneta a `dt` globale *(lettura `6`)*, e il confronto con l'integratore a strati **deve scendere come `dt²`** *(lettura `1`)*. ### ⛔ **(b) REGGE TOGLIENDO LA LEGGE PRATICA: NO, e non puo'** — qui **la legge pratica E' l'oggetto in prova** |
| `3` | **aggiunge un numero o una legge?** | ### ⛔ **NESSUNA LEGGE: il banco NON entra in `leggi.yaml`** *(e un braccio lo assicura)*. ### **I numeri sono TRE, e sono SONDE DI MISURA, non costanti di una legge:** `g` **scansionata** su potenze di due, `r_k` **dato col seme** *(la derivazione e' la domanda aperta)*, `c` **potenza di due per essere esatta al bit**. ### ✅ **NESSUN clip, NESSUN pavimento, NESSUNA proiezione** — e lo verifica un braccio, perche' un clip **violerebbe `A14` per costruzione** |
| `4` | **tocca `rho`, `c_s` o il SEGNO?** | ### **IL SEGNO SI', ed e' il centro:** le due componenti **sono le due bande**, e `C` scambia il segno della banda. ### ⛔ **`c_s` NO, e lo dichiaro:** `cs_k = 1` ovunque, quindi **questo prototipo non prova la `cs` locale.** ### **IL VERSO curvatura↔EM: NON SI APPLICA**, e il perche' e' che **in questo banco non esistono ne' campo elettromagnetico ne' metrica** |
| `5` | **emergente o imposto?** | ### ✅ **IL CONTROLLO E' LA MONETA LINEARE**, ed e' esattamente *«togliere la legge pratica»*: se la coerenza del cluster **si perde con la lineare** e **tiene con `(B)`**, la coerenza e' **dovuta a `(B)`**. ### ⚠ **E se tenesse ANCHE con la lineare, il fenomeno sarebbe della CONDIZIONE INIZIALE**, non della non linearita' — e la lettura `4` lo dice |

---

## `4` TODO DEL NEXT STEP — **operativo**

| | che cosa | dove |
|---|---|---|
| `1` | il banco, con `_presidio.avvia`, seme esplicito, **nessun import del simulatore** | `proto_camminata/` |
| `2` | la scena: irregolare `120`/gradi `2`-`6` **senza `pos`**, piu' il `4`-regolare di controllo | `proto_camminata/scena.py` |
| `3` | la camminata: Grover sulle estremita', moneta di banda `exp(-i dτ_k σ_z)`, spostamento **tutti gli archi insieme** | `proto_camminata/camminata.py` |
| `4` | `C`, e **il braccio `0`** che prova la simmetria **al bit** | `proto_camminata/_collauda_banco.py` |
| `5` | le due non linearita': `(A)` `C`-pari *(deve fallire)*, `(B)` `∝ (ρ₊−ρ₋)` `C`-dispari | `proto_camminata/nonlineare.py` |
| `6` | le sette letture, **ognuna con la sua soglia da questo documento** | `proto_camminata/_letture.py` |
| `7` | la dichiarazione **BANCO** nella lista dei file di fisica, e i collaudi **nella suite** | `csv/_file_fisica.py`, `primo_ordine/collauda.py` |
| `8` | il referto **GENERATO** dalle uscite, con previsione · numero · verdetto · cosa sblocca | `doc/REFERTO_prototipo_camminata.md` |
| `9` | le proposte per Luca **come VOCI** *(`DA_DECIDERE_LUCA.md` e' GENERATO)* | `csv/indice.py crea-lotto` |

### ⛔ **E DUE COSE CHE NON FARO', scritte qui perche' non diventino una sorpresa:** non
tocchero' **`leggi.yaml`** *(il banco non e' una legge)*, e non derivero' `r_k` — ### **il
mandato dice <<dato>>**, e derivarlo sarebbe **prendere al posto di Luca la decisione che
l'albero chiama `DOMANDA-LAMBDA-GRANDEZZA`.**

---

## ⛔ **ANNOTAZIONI — che cosa la MISURA ha precisato** *(par. `8`: ### **non si riscrive, si ANNOTA**)*

### 📌 **`(a)` IL `T` DEL CONO NON PUO' ESSERE `60`, E IL MOTIVO E' UNA MISURA.** Il grafo irregolare costruito come dichiarato ha ### **eccentricita' `6` archi** *(misurata con una `BFS`, `python proto_camminata/scena.py`)* — quindi a `60` tick ### **tutto il grafo e' DENTRO il cono**, e il braccio ### **passerebbe per VACUITA'.**

### ✅ **LA CURA E' UNA REGOLA, NON UN NUMERO:** `T_cono = eccentricita' // 2`, ### **cosi' i nodi oltre il cono ESISTONO SEMPRE** — e il collaudo ### **lo dichiara nella nota del braccio** *(`T=3`, `57` nodi oltre, `178` estremita' confrontate)*. ### ⚠ **I `60` tick restano** per norma e isotropia, dove non c'entra la distanza.

### 📌 **`(b)` L'ISOTROPIA HA DUE MODI, e la differenza e' MISURATA.** La somma sulle estremita' di un nodo e' ### **l'unico pezzo che dipende dall'ORDINE**: con `numpy` cambia gli ultimi bit, con **`math.fsum`** e' ### **esatta.** ### ✅ **Misurato:** con `fsum` la differenza fra la scena e la sua rinumerazione e' ### **`0.0` AL BIT**; con `numpy` e' ### **`1.07e-16`** contro una soglia di ### **`7.99e-14`.**

### ⭐ **E QUESTO E' UN RISULTATO PER L'ERA `2`, non un dettaglio di implementazione:** ### **l'isotropia della camminata e' ESATTA**, e cio' che si vede con `numpy` e' ### **solo arrotondamento** — quindi ### **se si vuole l'isotropia AL BIT basta sommare con `fsum`**, esattamente come fa gia' `primo_ordine/hamiltoniana.py`.

### 📌 **`(c)` LA LETTURA `1b` SI PRECISA, e senza la precisazione non misurerebbe niente.** *«Il confronto con l'integratore a strati, con la differenza che scende come `dt²`»* ### ⛔ **non puo' essere <<la camminata contro l'integratore>>:** sono ### **due dinamiche diverse** — la camminata ha un tick ### **fisso** *(un arco)*, l'integratore un passo ### **che si rimpicciolisce** — e una differenza fra due dinamiche diverse ### **non tende a zero.**

### ✅ **CIO' CHE SI MISURA, e che e' il confronto che conta:** ### **l'ANISOTROPIA dell'integratore a strati** — la differenza fra ### **due decomposizioni in strati** della stessa scena — deve scendere come ### **`dt²`**, mentre la camminata ### **non ha strati** e la sua anisotropia e' ### **`0.0` al bit.** ### ⭐ **Cosi' il confronto dice una cosa di FISICA:** l'anisotropia dell'integratore e' ### **un artefatto che si paga in `dt²`**, quella della camminata ### **non esiste.**
