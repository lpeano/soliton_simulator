# `Z43`, passo (1) — **LA DEFINIZIONE DEL TEMPO PROPRIO `r`: LA MISURA**

*(mandato di Luca del 2026-10-05. **Scritto PRIMA di girare**, e committato prima: cosi'
l'ordine e' **verificabile da git** invece che asserito da me — par.8.)*

> ### ⛔ **E' UNA MISURA, NON UNA CURA.** Il simulatore `e2940b3c` **non si tocca**, e
> ### **nessuna legge nuova si scrive: la forma la decide Luca dopo il referto.**

**LA VOCE E' `Z43`** *(aperta dal 2026-09-18, `da-decidere`, famiglia `B`: «**è una
decisione sulla definizione del tempo**»)*. ### **Nessun ID nuovo.** Collega `Z33`, `Z41`,
`Z37`, `Z42`, `D25`, `D32`, `RITMO-PAVIMENTO`, `TEMPO-LUCE`,
`TETTO-CAUSALE-TEMPO-COORDINATO`.

**PERCHE' VIENE ADESSO, e rientra nell'eccezione al congelamento:** `r` e' la base del
**passo (2)** di `TETTO-CAUSALE-TEMPO-COORDINATO`, che ### **ora BLOCCA su `Z43`**.
*(La cura di `MEM-HEBB-VERSO` aspetta la verifica del guardiano sul referto `2717308`.)*

## LE DECISIONI GIA' PRESE, che questo mandato RISPETTA e NON riapre

| | |
|---|---|
| **`D32`** *(2026-09-27, Luca)* | il tempo proprio del sistema **E' `r`** *(`dt_e` sull'arco)*; `d/cs` e' il **tempo-luce**, grandezza **diversa e legittima**. ### ⛔ **Questo mandato NON riapre `D32`: cerca la DEFINIZIONE di `r`.** |
| **`CURA2-STRUTTURALE`** / `TEMPO_UNICO_MITOSI` | la mitosi usa **quel** tempo. ### **Verificato dal codice:** `step()` scrive `_r_corrente` *(`:7469`)* e `_r_nodo_mitosi` lo **legge** *(`:7235-7241`)*; `_dt_e_ultimo` *(`:7462`)* e' letto da `_fattore_tempo_arco` *(`:7251`)*, che **dichiara di non ricalcolarlo** per non avere due leggi. |
| **`Z42` / `A6`** | `r` **non puo'** dipendere da `f` dello **stesso istante**. ### **Ogni via proposta lo dichiara, una per una.** |
| **`STEP2`** *(fisica di default dal 2026-09-16, Luca; `COMPONENTI:A1`, `COMPONENTI:B9`)* | `omega_clk *= (cs/CS_M)^2`, l'**orologio di Compton** con `c -> cs`. **Verificato a `:5970`.** |

### ⛔ **LE DUE STRADE CHIUSE DA MISURE, che NON ripropongo senza un fatto nuovo**

| | perche' e' chiusa | e in che cosa differisce la via di questa misura |
|---|---|---|
| **`Z41`** riferimento **assoluto** | ### **l'orologio si ferma** | ### **`C6` SOMIGLIA, e lo dico subito:** `f = delta_angolo/dt_n` e' *la via nominata da `Z41` e mai decisa*. ### **Differisce in questo:** `Z41` proponeva un riferimento **assoluto al posto del gauge**; `C6` ### **non toglie il gauge**, misura `f` in **tempo proprio** invece che in tempo di coordinata. ### ⚠ **Ma il rischio e' lo stesso** — `dt_n = DT*r`, quindi `f = delta/(DT*r)` ### **rimette `r` nel denominatore di cio' che definisce `r`**, e il referto deve dire se e' `A6`. |
| **`Z37`** **cucitura** | ### **toglie il 98% del segnale** | ### **`V1` SOMIGLIA, e lo dico subito:** il riferimento ai **vicini** e' una normalizzazione **locale**, come la cucitura. ### **Differisce in questo:** `Z37` **cuciva le FASI** *(toccava lo stato)*; `V1` ### **normalizza una FREQUENZA GIA' MISURATA** e non riscrive niente. ### ⚠ **Il rischio da misurare e' l'altro:** se i vicini hanno `C1` quasi uguale, ### **`V1 ~ 1` per tutti e il segnale sparisce — che e' esattamente il 98% di `Z37`.** Il referto deve riportare la **dispersione di `C1` fra vicini**, non solo la mediana di `V1`. |

## IL QUADRO, **VERIFICATO DALL'AST** — e tre precisazioni

### ✅ **CIO' CHE IL GUARDIANO HA LETTO BENE** *(tutto, tranne quanto nelle tre note)*

`ritmo()` sta a **`:5260`**. Nella configurazione del driver:

```
a      = angle(psi_spin[:,0]) - angle(_psi_spin_prec[:,0])        :5308
signed = ((a + pi) % (2pi) - pi) / DT                             :5313   (RITMO_WRAP_2PI = True)
f      = |signed|                                                 :5318   (TEMPO_PROPRIO_ORIENTATO = False)
med    = _med_f_prec                                              :5358 / :5366
x      = f / med                                                  :5371
r      = x/sqrt(1+x^2) + 1e-6                                     :5372
r_unit = 1/sqrt(2) + 1e-6                                          :5373
return   1 + TAU_LOC*(r/r_unit - 1)                               :5375   (TAU_LOC = 1.0)
```

**I TRE DIFETTI DI DEFINIZIONE, come il mandato li nomina:** `(D1)` frequenza usata come
tempo **senza una frequenza propria del nodo**; `(D2)` riferimento **NON locale** *(mediana
su tutti i nodi)*; `(D3)` dipende dalla **BASE** dello spinore *(componente `0`)* e
**contiene la fase globale**.

### ⚠ **PRECISAZIONE 1 — il gauge si LEGGE a `:5358`, non a `:5356`**

Il mandato cita `:5356` per la mediana. ### **A `:5356` si calcola la mediana CORRENTE e la
si REGISTRA in `_med_f_ultimo`**; il `med` **usato** e' `_med_f_prec`, letto a **`:5358`** e
applicato a **`:5366-5371`**, e lo **promuove `step()`** a **`:7451-7456`** — ### **e solo se
sta sopra `1e-9`**, perche' *«non si promuove un `med` che sta sul pavimento: quel valore non
e' una misura, e' la protezione da divisione per zero»*.
### **Il gauge E' la mediana del passo precedente, come il mandato dice: cambia solo QUALE
RIGA la nomina.**

### ⚠ **PRECISAZIONE 2 — il tetto NON e' `sqrt(2)`: e' `sqrt(2)` meno `5.85e-07`**

Calcolato, non stimato *(`TAU_LOC = 1.0`)*:

| | `r` |
|---|--:|
| `x -> 0` *(`f` nullo)* | **`0.000001414`** |
| `x = 1` *(al gauge)* | **`1.000000000`** |
| `x -> inf` *(saturazione)* | **`1.414212977`** |
| `sqrt(2)`, per confronto | `1.414213562` |

### **La differenza e' `5.85e-07`, e viene dal `+1e-6` del regolarizzatore**, che entra **due
volte** *(al numeratore e in `r_unit`)*. ### **Non e' un dettaglio di stile: `1.414212977`
e' il valore che una misura trova, e chiamarlo `sqrt(2)` renderebbe invisibile il
regolarizzatore.** *(E il pavimento `1.414e-06` e' la firma che il codice stesso dichiara a
`:5319`: **il tempo proprio si FERMA per tutti**.)*

### ⚠ **PRECISAZIONE 3 — il nome `r` nel file E' SOVRACCARICO, e un censimento per nome MENTE**

Il censimento dall'AST trova `r` in **14 funzioni** in lettura. ### ⛔ **Ma in
`_semina_lam`, `semina`, `_celle_vive`, `_massa`, `_accresci`, `_gusci_esterni`,
`chiralita_core_locale` e `_git` `r` e' un RAGGIO, e in `batch_condensazione` e' una RIGA DI
CSV.** ### **Nessuno di questi e' un consumatore del ritmo.**
### **Quindi lo strumento non censisce per NOME: censisce per PROVENIENZA** — da che cosa il
nome e' assegnato — e **dichiara** i casi che scarta. ### **Un censimento che contasse 14
funzioni sarebbe un numero gonfiato di 9.**

### **I CONSUMATORI VERI, dall'AST e per provenienza**

| dove | che cosa |
|---|---|
| `step` `:7419` | `r = self.ritmo()` — ### **l'UNICO call-site FISICO** *(gli altri due, `:12072` e `:12742`, assegnano a `tau` e sono **diagnostici**)* |
| `step` `:7423-7424` | `dt_n = DT*r` *(nodo)* e `dt_e = DT*0.5*(r[i]+r[j])` *(arco)* |
| `step` `:7462` / `:7469` | `_dt_e_ultimo = dt_e` e `_r_corrente = r` *(sotto `FORK_SU2_MEM`)* |
| `step` `:7488` | `self.eta += dt_n` |
| `_passo_spinoriale` `:5904`, `:5926`, `:5939` | `r_node = dtn/DT`, `omega_clk = coerenza * r_node`, `_dts = dtn` |
| `_bloch_ritardato` `:7173-7176` | `alpha = 1 - exp(-dt_n/tau)`, `tau = d/cs` — ### **lo Strato 1** |
| `_peq_esatto` `:6848-6860` | `peq` in forma esatta, con `dte` |
| `_fattore_tempo_arco` `:7251-7258` | `dt_e/DT` per arco, ### **LETTO da `_dt_e_ultimo` e non ricalcolato** |
| `_r_nodo_mitosi` `:7235-7241` | legge `_r_corrente` — ### **e' il tempo della MITOSI** |
| `step`, 17 letture di `dt_e` | fra cui `:7912-7922` e `:8032` *(l'integrazione delle fasi e i sotto-passi)* |

## ⛔ L'ANELLO: **E' NEL CODICE, e l'ho VERIFICATO invece di assumerlo**

> L'ipotesi del mandato: `r -> omega_clk -> fase dello spinore ~ r^2 -> psi_spin -> f -> r`.

**LE QUATTRO RIGHE CHE LO CHIUDONO** *(configurazione del driver: `SPINORE_CORRETTO`,
`DEPARAM_OROLOGIO`, `STEP2_OROLOGIO` tutti `True`, `OROLOGIO_SEGNO` `False` -> `_sk = 1`)*:

```
:5904   r_node     = dtn/DT                         = r
:5926   omega_clk  = coerenza_arco * r_node          [-1,1] * r
:5970   omega_clk  = omega_clk * (cs_prec/CS_M)^2
:5971   _phc       = exp(-0.5j * _sk * omega_clk * _dts)      _dts = dtn = DT*r
```

### ⛔ **L'INCREMENTO DI FASE DELL'OROLOGIO E' `-0.5 * coerenza * (cs/CS_M)^2 * DT * r^2`.**
### **Il quadrato c'e', ed e' esplicito: `r` entra UNA volta in `omega_clk` e UNA volta in
`_dts`.**
Poi `_phc` moltiplica `a1, b1`, cioe' **`_psi_spinor`**; `calcola_psi` emette
`psi_spin = W@(amp*_psi_spinor)/(1+GAMMA*norm)` *(`:6240-6242`)*; e `ritmo()` legge la fase
della **componente 0 di `psi_spin`**. ### **L'anello si chiude.**

### ✅ **E `A6` NON E' VIOLATO DALL'ANELLO, e va detto:** il giro passa per `_psi_spin_prec`
e `_med_f_prec`, che sono **snapshot del passo precedente** — `step()` li promuove **dopo**
il consumo *(`:7438`, `:7454`)*. ### **E' un anello SFASATO DI UN PASSO, non istantaneo.**
### **Per questo e' un candidato all'ALTALENA e non a un punto fisso:** un'andata e ritorno
in due passi e' esattamente cio' che produce un periodo 2.

## IL FATTO DEL GUARDIANO, **da rifare io** *(non e' nel repo)*

Linux, `e2940b3c`, seme 11, 150 passi. Passi 1-2: `r = 1` **per costruzione**
*(`_ritmo_sicurezza`, poi `_ritmo_med_assente`)*. Dal passo 3 la mediana di `|f|`
**ALTERNA** alta/bassa a ogni passo, rapporto `~1.5e4` ai passi 3-4, `~18` al 20, `~10` al
60, `~3` al 100, `~1` al 140. Passi **dispari** `r ~ 1.41` per quasi tutti; passi **pari**
`r` mediano da `1e-4` *(passo 4)* a `0.4` *(passo 100)*. Nei passi pari la **materia** *(5%
di `|psi|^2` piu' alto)* ha `r ~1.3-1.4` fra i passi 16 e 64 contro `0.03-0.1` del
**vuoto**; dopo il 100 la differenza si spegne. I nodi **nel loro primo passo** hanno
`r ~1.2-1.4` *(`_psi_spin_prec` **ereditato dal genitore**)*.

### ⚠ **LO RIFACCIO SU WINDOWS, e se i numeri non coincidessero NON sarebbe una smentita:**
sarebbe ### **una differenza di piattaforma da dichiarare** *(`PIATTAFORMA-NON-TIMBRATA`)*.
### **Scrivo ORA che il confronto che conta e' il RAPPORTO pari/dispari e il suo
ANDAMENTO**, non la terza cifra.

## LE QUATTRO GRANDEZZE DI «TEMPO LOCALE», e come si legano

| | che cos'e' | da dove viene |
|---|---|---|
| **`r`** | il **ritmo del tempo proprio** *(`D32`: **E'** il tempo proprio del sistema)* | `ritmo()`, dalla **fase della componente 0 di `psi_spin`**, su gauge **globale sfasato** |
| **`tau = d/cs`** | il **tempo-luce** *(`D32`: grandezza **diversa e legittima**)* | `_tempo_luce_nodo` `:7285`, ### **unico punto del file** |
| **`omega_clk`** | l'**orologio di Compton** | `:5926` *(coerenza d'arco `*r`)* `* (cs/CS_M)^2` a `:5970`; applicato come **fase globale** `_phc` a `:5971` |
| **`cs`** | la **velocita' metrica locale** | `_cs_nodo` `:7072`, chiamata a `:7847` con ### **`I = |psi|^2` del campo SCALARE** *(`:7839`)* |

### ⛔ **ED ECCO LA DISSONANZA CHE QUESTA MISURA DEVE PESARE:** `cs` si calcola da
**`|psi|^2` scalare**, mentre `mitosi` *(`:8552`)*, la **densita' di coppia** *(`:8871`)* e
`_rho_sorgente` usano ### **`rho_spin`**. ### **Due densita' nella stessa fisica**, e
`omega_clk` — che vive **sullo spinore** — e' pilotato da un `cs` che viene dallo
**scalare**. ### **Per questo il mandato chiede `C4` e `C4s`: la STESSA legge `_cs_nodo`,
con le DUE densita'.**

### **L'ALLINEAMENTO DI `cs`, dichiarato:** `_cs_nodo_prev` e' scritto a **`:7852`**
*(settore metrico, sotto `FORK_SU2_MEM or STEP2_OROLOGIO`)* e letto a **`:5965`**
*(`_passo_spinoriale`)*, che gira **PRIMA**. ### **Quindi l'orologio usa il `cs` di UN PASSO
FA, e il codice lo dichiara** *(`:5961-5962`, `:7849-7851`)*.

## LA STELLA POLARE — **le cinque risposte, PRIMA del codice** *(`L-STELLA`)*

> ### ⚠ **Qui si risponde per la MISURA, non per una cura: nessuna cura e' proposta.** Dove
> una domanda riguarda **la forma futura**, la risposta dice ### **che cosa la misura dovra'
> produrre perche' quella domanda sia rispondibile** — e non la risponde al posto di Luca.

### **1. `A14`: conserva energia e carica LOCALMENTE?**

### **NON SI APPLICA: questa misura non scrive niente.** Calcola grandezze **a lato**, su una
**copia patchata**, e il simulatore ### **non e' toccato**.
### ⚠ **E per le VIE: la domanda non e' rispondibile oggi, e il perche' e' un fatto del
repo** — `ENERGIA-NON-DEFINITA`: ### **il modello non ha un'energia totale.**
### 📌 **Ma una cosa la misura la produce, ed e' il materiale per rispondere domani:** `r`
moltiplica **il tic di tutte le leggi** *(`dt_n`, `dt_e`)*, quindi una definizione di `r`
che **non sia locale** rende ### **non locale il TEMPO di ogni legge locale** — ed e'
esattamente `(D2)`. ### **Il numero che lo pesa e' il rapporto fra `S1`/`V1` e `C0`.**

### **2. A quale dei TRE GRADINI arriva il risultato?**

| gradino | risposta |
|---|---|
| **(a)** robusto al rumore numerico | ### **DA MISURARE**, e `FEDELTA'` lo pretende: il mio `C0` deve coincidere **AL BIT** col `r` di `ritmo()`. ### **Se non coincide, nessun altro numero vale.** |
| **(b)** regge togliendo la legge pratica | ### ⛔ **LE LEGGI PRATICHE QUI SONO DUE, e vanno nominate entrambe:** la **saturazione** `x/sqrt(1+x^2)` *(tetto `1.414212977`)* e il **pavimento** `1e-9` sul gauge. ### **Il referto deve dire quante volte MORDONO** — e se l'altalena vive **dentro la saturazione**, allora cio' che si osserva e' ### **il tetto, non la legge.** |
| **(c)** coincide con un limite noto | ### **SI', E SU TRE CONTROLLI ESATTI:** `POSITIVO` *(angolo noto -> `C1` all'arrotondamento)*, `BASE` *(una rotazione `SU(2)` comune lascia `C1` invariato)*, `FASE GLOBALE` *(lo stesso `e^{i alpha}` lascia `C1` e `C2` invariati)*. ### **Sono i limiti di INVARIANZA, e sono il senso di `C1`.** |

### **3. Aggiunge un numero o una legge?**

### **QUESTA MISURA: ZERO.** Non aggiunge niente — ### **conta**, e conta **a lato**.

### ⛔ **E IL CONTO DELLE LEGGI PER LE SEI VIE, scritto ORA perche' `9-ter` si applica alla
### SCELTA e non alla cura** *(«una cura non aumenta il numero delle leggi; a parita' di
effetto si preferisce togliere un'eccezione»)*:

| via | aggiunge una legge? | aggiunge un numero? |
|---|---|---|
| **(a)** `S1`, riferimento a **se stesso** | **no**: cambia **chi** e' il gauge | ### ⚠ **SI', uno NUOVO: la FINESTRA** *(«sui passi precedenti» — quanti?)*. **Va dichiarato come manopola.** |
| **(b)** `V1`, riferimento ai **vicini** | **no**: cambia **chi** e' il gauge | **no**: i vicini sono il grafo |
| **(c)** `f0` dalla **massa** | ### **SI', una legge nuova** `f0(massa)` | dipende dalla forma |
| **(d)** da `cs` con `|psi|^2` | ### **no, ne TOGLIE una:** `r` **deriva** da `cs`, che e' gia' legge | **no** |
| **(d')** da `cs` con `rho_spin` | ### **no, e TOGLIE ANCHE UN'ECCEZIONE:** le due densita' diventano una | **no** |
| **(e)** da **`omega_clk`** *(Compton)* | ### **no, ne TOGLIE una** — e ### **ELIMINA L'ANELLO per costruzione** | ### ⚠ **SI': L'ESPONENTE** *(`2` di `STEP2` o `0.5` della relativita' generale in coordinate isotrope)*. ### **DECISIONE DI LUCA: il referto riporta ENTRAMBI e NON scegliE.** |
| **(f)** `C6`, la via di `Z41` | **no** | **no** |

### **4. Tocca `rho`, `c_s` o il SEGNO?**

### **LA MISURA: NO.** Legge, non scrive.
### ⛔ **MA LE VIE `(d)`, `(d')` ed `(e)` FANNO DIPENDERE `r` DA `cs`, E VA DETTO FORTE:**
oggi `cs` **dipende da `r`** attraverso `dt_e` nei sotto-passi della metrica. ### **Quindi
quelle tre vie CHIUDONO UN ANELLO NUOVO `r <-> cs`, e il referto deve dire con quale
sfasamento** — ### **`A6` si gioca li'.** *(`(e)` lo chiude **esplicitamente**:
`omega_clk` contiene **gia'** `(cs/CS_M)^2`, e derivarne `r` lo renderebbe la definizione.)*
**Il SEGNO:** oggi `r >= 0` perche' `TEMPO_PROPRIO_ORIENTATO = False` *(`f = |signed|`)*;
### **nessuna via qui proposta cambia quel flag**, e `C2` misura la fase **con segno** per
dire **quanto segnale c'e'** in cio' che `f = |.|` butta.

### **5. Emergente o imposto: il fenomeno sopravvive se si toglie la legge pratica?**

### **IL <<FENOMENO>> QUI E' L'ALTALENA, ed e' proprio cio' che si misura.**
### 📌 **`BRACCIO A` e' la risposta operativa a questa domanda**, e la scrivo sotto con
### **l'esito che la SMENTIREBBE, PRIMA di girare.**

## ⛔ `BRACCIO A` — **che cosa SMENTIREBBE l'ipotesi dell'anello**, scritto PRIMA

**CHE COSA FA:** una **seconda copia**, in cui `:5926` diventa
`omega_clk = (_num/max(_den,1e-12)) * 1` — ### **`r_node` sostituito da `1`, tutto il resto
identico al byte.**

### ⚠ **E CHE COSA *NON* FA, dichiarato subito perche' e' il limite del braccio:** `r`
### **resta** in `_dts = dtn` *(`:5939`, `:5971`)*. ### **Quindi il braccio non spezza
l'anello: ne toglie UNA POTENZA**, da `r^2` a `r^1`.
### **Non lo chiamo <<anello spezzato>>**: toccare anche `_dts` cambierebbe `theta` della
rotazione `SU(2)` a `:5941`, che e' ### **un'altra legge**, e sarebbe **due interruttori in
una volta** *(par.3)*.

| esito di `BRACCIO A` | che cosa concludo |
|---|---|
| il rapporto **pari/dispari** della mediana di `|f|` **crolla verso `1`** | ### ✅ l'anello **contribuisce** all'altalena |
| il rapporto **resta dello stesso ordine** *(`~1e4` ai passi 3-4)* | ### ⛔ **L'IPOTESI DELL'ANELLO E' SMENTITA come causa dominante**, e la causa sta altrove — ### **il candidato successivo e' il GAUGE SFASATO** *(`med` del passo precedente diviso una `f` del passo corrente: un ritardo di uno in una retroazione **e' di per se' un generatore di periodo 2**, anche senza `omega_clk`)* |
| il rapporto **cala ma resta `>> 1`** | ### **l'anello e' UNA delle cause, non LA causa**, e il referto dice **quanto** ne spiega |

### ⛔ **SCRIVO ORA LA MIA ASPETTATIVA, perche' detta dopo non valga come previsione:**
### **mi aspetto che il rapporto CALI MA NON CROLLI**, cioe' il terzo caso.
### **Il perche':** il gauge sfasato basta da solo a produrre periodo 2 — se `f` e' alta, il
`med` del passo dopo e' alto, quindi `x = f/med` del passo dopo e' **basso**. ### **Quello e'
un oscillatore a due passi che NON passa da `omega_clk`.** ### **Se mi sbaglio, lo scrivo.**

## ⛔ COERENZA DI COMPTON — **il valore sotto IPOTESI NULLA, scritto PRIMA**

**L'IPOTESI:** se la **rotazione** dello spinore e la sua **densita'** raccontano la stessa
storia, allora `C1 / C4s` e' ### **COSTANTE nel tempo per ogni nodo**, e quella costante
sarebbe ### **la frequenza propria `f0`**.

**LA MISURA:** per ogni nodo, il **coefficiente di variazione** *(`CV = sigma/|media|`)* del
rapporto `C1/C4s` nel tempo, **contro** quello di `C1` da solo.

> ### **SOTTO IPOTESI NULLA — `C1` e `C4s` indipendenti — il rapporto e' PIU' RUMOROSO di
> ### `C1`, non meno:** al primo ordine
> ### **`CV(C1/C4s)^2 ~ CV(C1)^2 + CV(C4s)^2`**, quindi
> ### **`CV(rapporto) >= CV(C1)`**, e il rapporto delle due `CV` e' **`>= 1`**.
>
> | esito | che cosa concludo |
> |---|---|
> | `CV(rapporto)/CV(C1)` ### **`>= 1`** | ### **IPOTESI NULLA: dividere per `C4s` AGGIUNGE rumore. Nessuna `f0`.** |
> | `CV(rapporto)/CV(C1)` ### **`<< 1`** | ### ✅ **la divisione CANCELLA varianza: le due grandezze raccontano la stessa storia, e la costante e' un candidato `f0`** |
> | `~1` | ### **indeciso**, e si dice **indeciso** |

### ⚠ **E DICHIARO UN MODO IN CUI QUESTO TEST PUO' MENTIRE:** se `C1` e `C4s` **saturassero
entrambi** *(p.es. `C1` al tetto e `cs` al suo `floor`)*, il rapporto sarebbe costante
### **perche' sono due costanti, non perche' si cancellano.** ### **Il referto deve
riportare la frazione di nodi in saturazione** accanto alla `CV`, altrimenti ### **una `CV`
bassa sarebbe un FALSO-UNO a favore dell'ipotesi.**

## LA MISURA, come il mandato la detta

Scena del driver *(`nmasse` e `sep` dall'argv)*, **seme 11**, **150 passi**, patch su una
**COPIA**. Si registra con ### **gli STESSI snapshot di `ritmo()`** *(`psi_spin` e
`_psi_spin_prec`, piu' `_med_f_prec`)*. Per ogni **nodo** e ogni **passo**, a lato:

| | |
|---|---|
| **`C0`** | `r` di oggi |
| **`C1`** | angolo **invariante**: `theta = 2*arccos(min(1, abs(<psi_prec|psi>)/(abs(psi_prec)*abs(psi))))/DT` |
| **`C2`** | **fase globale**: `arg(<psi_prec|psi>)/DT` |
| **`C3`** | fase della componente **0** e della componente **1**, **separate** |
| **`S1`** | `C1` / media di `C1` **dello stesso nodo** sui passi precedenti |
| **`V1`** | `C1` / mediana di `C1` sui soli **VICINI** |
| **`C4`** | `cs/CS_M` e `cs/`mediana di `cs` sui vicini, con `cs` da `|psi|^2` *(la cache `_cs_nodo_prev`)* |
| **`C4s`** | lo stesso con `cs` dalla **STESSA legge `_cs_nodo`** ma con `I = rho_spin` |
| **`C5`** | `(cs/CS_M)^2` *(l'esponente di `STEP2`)* **e** `(cs/CS_M)^0.5` *(l'esponente della relativita' generale in coordinate isotrope)*. ### **L'esponente e' una DECISIONE DI LUCA: riporto ENTRAMBI.** |
| **`C6`** | la via di `Z41`: `f = delta_angolo/dt_n` |

Per ciascuno: **mediana, `p5`, `p95` per passo**; **rapporto pari/dispari** delle mediane;
**materia contro vuoto**; **nodi nel loro primo passo separati**.

**PIU':** l'**autocorrelazione a ritardo 1** degli incrementi di fase per nodo, in quali
orologi compare, e se **`psi_spin` stesso alterna** fra passi consecutivi; la **pendenza
log-log** di `C1` e `C2` contro `|psi|^2` e `rho_spin`.

### **UNA COSA CHE NON FARO', e il perche'**

`_cs_nodo` **incrementa un contatore** *(`_cs_lam_degenere`, `:7120`)* se `mean(I) <= 1e-30`.
### **Quindi per `C4s` verifico `mean(rho_spin) > 1e-30` PRIMA di chiamarla**, e se non lo
fosse ### **registro e salto invece di chiamare.** ### **Una misura non muove cio' che
misura, nemmeno un contatore** — e' la stessa ragione per cui ieri non ho chiamato `_sd0`.

## I CONTROLLI CHE POSSONO FALLIRE — **fissati e committati PRIMA di girare**

| | che cosa pretende | e se fallisce |
|---|---|---|
| **`POSITIVO`** | uno spinore **sintetico** ruotato di un angolo **noto** *(`SU(2)`, piu' taglie)* restituisce **quell'angolo** in `C1`, all'arrotondamento | ### **`C1` non misura un angolo: FERMO** |
| **`BASE`** | una stessa rotazione `SU(2)` **casuale** applicata a **tutti** gli spinori *(entrambi gli snapshot)* lascia `C1` **invariato**. ### **CASO CHE DEVE FALLIRE: `C3` CAMBIA** | ### ⛔ **se `C3` NON cambia, il test NON DISCRIMINA: FERMO** |
| **`FASE GLOBALE`** | lo stesso `e^{i alpha}` su **entrambi** gli snapshot lascia `C1` **e** `C2` invariati | ### **FERMO** |
| **`FEDELTA'`** | il mio `C0` ricalcolato a lato coincide ### **AL BIT** col `r` di `ritmo()` su **ogni nodo**, nei passi **senza rami di sicurezza** | ### ⛔ **misuro un'altra cosa: FERMO** |
| **`CONTEGGIO`** | ### **zero nodi confrontati NON e' un'identita'** | si dichiara su quanti |

### ⚠ **`FEDELTA'` E' IL PIU' ESPOSTO, e lo dico PRIMA:** devo riprodurre `np.median`,
`np.angle` e l'ordine esatto delle operazioni di `:5371-5375`. ### **Il mandato dice <<AL
BIT>> e non lo ammorbidisco:** se fallisce per `1e-16`, porto **il numero e la causa** a
Luca. ### **E i passi 1-2 sono ESCLUSI per costruzione** *(`_ritmo_sicurezza` e
`_ritmo_med_assente` restituiscono `np.ones` senza passare dalla formula)*: il controllo li
**riconosce dai contatori**, non dal numero del passo.

## LE SEI VIE — **da riportare, NON da scegliere**

> ### ⛔ **NESSUNA LEGGE NUOVA: la forma la decide Luca dopo il referto.**

Per ciascuna il referto dira': **l'altalena sparisce si'/no**, **rispetta `A6` si'/no**,
**e' locale si'/no**, **segno materia/vuoto**, **somiglianza con le strade chiuse**.

| | la via | `A6`, dichiarato ORA |
|---|---|---|
| **(a)** | `S1`, riferimento a **se stesso** | ✅ **si'**, se la finestra e' sui passi **precedenti** *(mai il corrente)* |
| **(b)** | `V1`, riferimento ai **vicini** | ### ⚠ **DIPENDE:** i vicini dello **stesso istante** sono `f` dello stesso istante -> ### **violerebbe `A6`**, come il `med` istantaneo curato nel 2026-09-18. ### **Serve lo snapshot dei vicini al passo precedente**, e il referto lo deve dire |
| **(c)** | `f0` dalla **massa** | ✅ **si'**, se la massa e' quella dello snapshot |
| **(d)** | da `cs` con `|psi|^2` | ✅ **si'** per `cs`, che e' **del passo precedente** *(`_cs_nodo_prev`)*; ### ⚠ **ma apre l'anello `r <-> cs`** |
| **(d')** | da `cs` con `rho_spin` | come `(d)`, ### **e toglie l'eccezione delle due densita'** |
| **(e)** | da **`omega_clk`** | ✅ **si'**, e ### **elimina l'anello di `r` PER COSTRUZIONE**; ### ⚠ **l'esponente e' una DECISIONE DI LUCA** |
| **(f)** | `C6`, la via di `Z41` | ### ⛔ **NO, e lo dichiaro subito:** `f = delta/(DT*r)` ### **mette `r` nel denominatore di cio' che definisce `r`** — e il referto deve dire se e' lo stesso istante *(violazione)* o il precedente *(ammissibile)* |

## L'ORDINE DEI COMMIT

1. ### **questo task history**, pushato **PRIMA** del lavoro *(par.8)*;
2. ### **lo strumento, PRIMA di girare**, coi **cinque controlli** dentro e il **collaudo**;
3. ### **il referto, dopo**, **coi blob citati** e la **piattaforma dichiarata**.

## TODO DEL NEXT STEP — **operativo**

1. **commit di questo task history**;
2. `csv/_test_fork/_z43_tempo_proprio.py`: **due copie** patchate *(la misura e `BRACCIO A`)*,
   ancore **contate**, **battito per passo**, i **cinque controlli**, il **collaudo** su dati
   sintetici, e la **configurazione INTERA dichiarata** *(`H-P5`)*;
3. **commit dello strumento**, col blob nell'**inventario** *(par.6)*;
4. **la corsa**: 150 passi, seme 11, **piu' `BRACCIO A`**;
5. **il referto** `doc/REFERTO_z43_tempo_proprio_2026-10-05.md`, con le **sei vie** riportate
   e ### **nessuna scelta**;
6. **relazione** e **voce d'indice** nello stesso giro *(par.4)*.

### ⛔ **CIO' CHE NON SI FA:** ### **nessuna cura, nessun flag nuovo, nessuna legge.**
### **`doc/ASSIOMI.md` non si tocca**, e `D32` ### **non si riapre.**
