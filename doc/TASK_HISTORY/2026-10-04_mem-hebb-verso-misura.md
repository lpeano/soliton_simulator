# `MEM-HEBB-VERSO`, passo (1) — **DECISIONE REGISTRATA E MISURA**

## STATO: **INIZIATO il 2026-10-05** *(era `NON INIZIATO - in coda dopo TETTO-CAUSALE
## passo (1)`)*

> ### ✅ **PARTE ORA, su ordine di Luca del 2026-10-05**, dopo che `TETTO-CAUSALE`
> passo (1) *(`eeb54be`)* e `VELENO-ARCHI-KEEP` passi (1) e (2) *(`cb24b95`, `c4e9fd5`,
> approvato in `8bf9271`)* sono chiusi.
> ### ⛔ **E IL SIMULATORE DI PARTENZA NON E' PIU' `0f060670`: e' `e2940b3c`**, la
> cura di `VELENO-ARCHI-KEEP`. ### **Dove il mandato dice `0f060670` vale `e2940b3c`**
> *(decisione di Luca, 2026-10-05)*.

*(Messo al sicuro nel repo su ordine di Luca del 2026-10-04, fine serata. **Nessun lavoro e'
stato fatto su questo mandato.** Il passo (1) di `TETTO-CAUSALE` e' chiuso col referto
`doc/REFERTO_tetto_causale_tempo_2026-10-04.md`, in `eeb54be`.)*

> ### ⛔ **LA SEZIONE `LA STELLA POLARE` NON E' QUI, E NON PER DIMENTICANZA:** si scrive
> **quando il lavoro parte**, non ora. ### **Scritta adesso sarebbe una risposta data prima
> di aver letto il codice, cioe' esattamente la ricostruzione che il par.8 esiste per
> impedire.**

> ### ⚠ **E IL TESTO QUI SOTTO E' COPIATO PAROLA PER PAROLA dalla conversazione, come Luca
> ha chiesto: non e' riassunto ne' riformulato.** Se una riga sembra ambigua, l'ambiguita' e'
> **nell'originale** e va risolta con Luca, non da me.

---

## IL MANDATO, verbatim

MANDATO: MEM-HEBB-VERSO, PASSO (1): DECISIONE REGISTRATA E MISURA. Il simulatore 0f060670 NON si tocca. Congelamento dell'infrastruttura (decisione di Luca, 2026-10-04): niente presidi, riordini o censimenti di igiene, salvo un difetto che falsi QUESTA misura. Se il mandato TETTO-CAUSALE passo (1) e' in coda prima di questo, fallo prima: sono due commit separati, in ordine.

DECISIONI DI LUCA (2026-10-04), da registrare in doc/INDICE_ID.tsv e nel task history. Le decisioni sono sue: non reinterpretarle. doc/ASSIOMI.md non si tocca.
(1) d0 (memoria_hebbiana_moto, :9035-9037 su 0f060670). Oggi proj = media(m_i*I_i, m_j*I_j)/Imed . dir(i->j): cambia segno invertendo il verso dell'arco, e una traslazione rigida cambia d0. FORMA DECISA: moto relativo, con peso d'arco:
    proj = 0.5*(I_i+I_j)/Imed * (m_j - m_i) . dir(i->j)
  E' invariante per scambio i<->j, nulla per traslazione rigida (tutte le m uguali), positiva se i nodi si allontanano. Il peso e' sull'ARCO, non sul nodo: con il peso per nodo, la traslazione rigida di masse diverse NON da' zero.
(2) Fase (:9409-9434). Tre difetti: solo l'estremo ii riceve; phi[ii]=... con indici ripetuti tiene l'ULTIMA scrittura; dir_laterale = (-y, x, 0) privilegia l'asse z del laboratorio, mentre i nodi stanno in 3D (:4843). DECISIONE: il sito si SPEGNE con un flag proprio (MEM_MOTO_TUTTO e MEM_MOTO restano come sono). Si apre la voce nuova FASE-TRASCINAMENTO-3D (aperta, difetto): serve un asse fisico locale al posto di z. E' legge nuova, non riparazione.

LA MISURA, sulla scena del driver (nmasse e sep dall'argv), seme 11, 72 e 150 passi, sul blob di oggi. Calcola le grandezze nuove a lato, senza scriverle:
(a) d0, forma vecchia contro forma decisa, su ogni arco e a ogni passo: distribuzione di |proj| prima del taglio (min, mediana, p99, max); frazione di archi SATURI al taglio passo_max = 0.01*mediana(d0) (:9050), per ciascuna forma; frazione di archi in cui il segno cambia fra le due forme; somma con segno di Delta d0 per passo, per ciascuna forma.
(b) Fase: nodi con piu' di un arco come primo estremo; contributi scartati da "l'ultimo vince" (numero e somma dei moduli scartati contro quella applicata); distribuzione di |shift|; frazione saturata dal taglio pi/4.
(c) Dichiara, dall'AST, se nella configurazione del driver il sito (2) gira davvero (MEM_MOTO_TUTTO e i gate a :9391/:9393).
CONTROLLI CHE POSSONO FALLIRE, da fissare e committare PRIMA di girare:
 - la tua forma vecchia, ricalcolata a lato, coincide AL BIT con il proj del simulatore, dopo il taglio, su ogni arco. Se no, misuri un'altra cosa: FERMATI;
 - forma decisa con mem_mot sostituita da un vettore costante (traslazione rigida): proj = 0 esatto su ogni arco. La forma vecchia sullo stesso ingresso deve dare un proj NON nullo. Se la vecchia da' zero, il caso non discrimina: FERMATI;
 - scambio i<->j su tutti gli archi: la forma decisa e' identica al bit, la vecchia cambia segno.
Solo numeri, nessun PASSA/FALLISCE fuori dai controlli. Dichiara la piattaforma.

Prima di girare: task history con LA STELLA POLARE (le cinque risposte) per la cura decisa, scritta ORA e non dopo. Nel task history scrivi anche i criteri del sigillo della cura, per i commit successivi:
 - (1): braccio 0; caso che DEVE fallire = traslazione rigida (vecchia != 0, nuova == 0); scambio del verso degli archi: identita' al bit della nuova legge;
 - (2): con il flag nuovo ACCESO, identita' al byte con il blob di oggi; con il flag spento, le differenze devono stare solo in phi e a valle.
Commit: strumento prima di girare, referto dopo, con i blob citati.

NON CHIUDERE IL TURNO A META': ti fermi solo con "FERMO: <motivo>" su un controllo fallito o su una decisione di Luca. Chiudi con "PUSHATO: <hash>". STOP.

---

## CHE COSA MANCA, PRIMA CHE QUESTO LAVORO POSSA PARTIRE

*(Nessuna di queste righe interpreta il mandato: sono **cose da fare** che il mandato stesso
elenca, messe in ordine perche' alla ripresa non si debba ri-leggerlo per capire da dove
cominciare.)*

1. **`LA STELLA POLARE`**, le cinque risposte per la cura decisa — **prima** di girare;
2. i **criteri del sigillo** per i commit successivi, come il mandato li detta;
3. le **due decisioni di Luca** registrate in `doc/INDICE_ID.tsv` e nel task history;
4. la **voce nuova `FASE-TRASCINAMENTO-3D`** *(aperta, difetto)*;
5. il **flag proprio** per spegnere il sito (2) — *decisione di Luca: `MEM_MOTO_TUTTO` e
   `MEM_MOTO` restano come sono*;
6. i **tre controlli che possono fallire**, fissati e **committati PRIMA di girare**;
7. lo **strumento** prima di girare, il **referto** dopo, **coi blob citati**.

### ⚠ **E UNA COSA CHE IL MANDATO DICE E CHE VA LETTA DUE VOLTE:** *«Le decisioni sono sue:
non reinterpretarle»*, e *«`doc/ASSIOMI.md` non si tocca»*.
### **Quindi la forma di `proj` NON si discute: si registra e si misura.**

---

# IL LAVORO — **scritto il 2026-10-05, PRIMA di girare**

## LE RIGHE VERE SUL BLOB `e2940b3c`, misurate e non assunte

Il mandato cita righe di `0f060670`. Luca dice che il blob nuovo ha **97 righe in piu'**
prima di quei punti. ### **L'ho MISURATO invece di fidarmi del numero:** ho estratto
`0f060670` da `b17caec`, cercato **gli stessi ancoraggi per NOME** nei due blob e
confrontato le righe.

| ancoraggio | `0f060670` | `e2940b3c` | delta |
|---|--:|--:|--:|
| `def memoria_hebbiana_moto` | `8983` | **`9080`** | `+97` |
| `memedge = 0.5 * (...)` | `9035` | **`9132`** | `+97` |
| `proj = np.sum(memedge * dirarc, ...)` | `9037` | **`9134`** | `+97` |
| `passo_max = 0.01 * median(d0[mask])` | `9047` | **`9144`** | `+97` |
| `proj = np.clip(proj, -passo_max, passo_max)` | `9048` | **`9145`** | `+97` |
| il gate `if len(self.tw) and len(self.i) and self.n > 0:` | `9391` | **`9488`** | `+97` |
| il gate `if mask.any():` | `9393` | **`9490`** | `+97` |
| `dir_laterale = np.stack([-y, x, 0])` | `9409` | **`9506`** | `+97` |
| `proiezione_trasversale = np.sum(mem_mot[ii] * dir_laterale, ...)` | `9423` | **`9520`** | `+97` |
| `self.phi[ii] = (self.phi[ii] + shift) % self._dphi()` | `9434` | **`9531`** | `+97` |
| `u = self.rng.normal(size=(n, 3))` *(i nodi sono in 3D)* | `4843` | **`4940`** | `+97` |

> ### ✅ **IL DELTA E' `+97` SU OGNI SITO, e il numero di Luca e' giusto.** Le righe
> totali passano da `13 135` a `13 232`: ### **esattamente `+97`**, e la cura e' tutta
> **prima** di questi punti, quindi lo scostamento e' **costante** e non va interpolato.

### ⚠ **MA UNA CITAZIONE DEL MANDATO NON COINCIDE, e lo dico invece di aggiustarla
### in silenzio**

Il mandato scrive *<<il taglio `passo_max = 0.01*mediana(d0)` (`:9050`)>>*.
### **Su `0f060670` la riga `9050` e' un COMMENTO**; il taglio sta a **`:9047`** *(il
`passo_max`)* e **`:9048`** *(il `clip`)*, quindi su `e2940b3c` a ### **`:9144-9145`**.
### **Lo scostamento e' di 3 righe nel mandato stesso, non fra i due blob**, ed e'
esattamente cio' che il par.2 dice: ### **i numeri di riga nei documenti sono di blob
vecchi e SONO SHIFTATI — si cerca per NOME.**
### **Non e' un'ambiguita' da risolvere con Luca:** il mandato nomina la grandezza
*(`passo_max = 0.01*mediana(d0)`)*, e quella grandezza ha **un solo sito**.

## LE DUE DECISIONI DI LUCA, REGISTRATE — e non reinterpretate

### **DECISIONE (1): LA FORMA DI `proj`**

> ### **`proj = 0.5*(I_i+I_j)/Imed * (m_j - m_i) . dir(i->j)`**

dove `m` e' `mem_mot`. **La forma di oggi** *(`:9132-9134`)* e'
`proj = sum(0.5*(m_i*I_i + m_j*I_j)/Imed . dir(i->j))`.

### ✅ **LE QUATTRO AFFERMAZIONI DEL MANDATO, VERIFICATE NUMERICAMENTE PRIMA DI
### SCRIVERE QUESTO** *(dati sintetici, 40 nodi, ~118 archi, seme 7)*

| | la forma vecchia | la forma decisa |
|---|--:|--:|
| scambio `i<->j`: `max abs(p(i,j) - p(j,i))` | `5.943e+00` | ### **`0.000e+00`** |
| scambio `i<->j`: `max abs(p(i,j) + p(j,i))` | ### **`0.000e+00`** *(cambia segno)* | — |
| traslazione rigida *(`m` costante)*: `max abs(proj)` | `5.645e+00` | ### **`0.000e+00`** |

### **E ANCHE LA QUARTA, che e' la ragione per cui il peso sta sull'ARCO:** con il peso
**per nodo** — `0.5*(m_j*I_j - m_i*I_i)/Imed . dir` — la traslazione rigida da'
`3.724e+00`, ### **NON zero**, perche' resta `0.5*m*(I_j - I_i)/Imed . dir` e le `I` sono
diverse. ### **Il mandato lo dice, e il numero lo conferma: il peso DEVE stare
sull'arco.**

### ⛔ **E QUESTO NON E' UN CONTROLLO DELLA MISURA, E' UN CONTROLLO DELLA MIA LETTURA
### DELLA DECISIONE:** l'ho fatto a lato, su dati finti, **prima** di scrivere una riga
di strumento, ### **perche' se avessi letto male la formula misurerei un'altra legge.**
I controlli del mandato restano, e girano sul simulatore vero.

### **DECISIONE (2): IL SITO DELLA FASE SI SPEGNE CON UN FLAG PROPRIO**

I **tre difetti** del sito *(`:9506-9531`)*, come il mandato li elenca:

1. ### **solo l'estremo `ii` riceve**: `proiezione_trasversale` legge `mem_mot[ii]` e
   `self.phi[ii] = ...` scrive su `ii`. ### **Due volte `ii` e mai `jj`.**
2. ### **`phi[ii] = ...` con indici RIPETUTI tiene l'ULTIMA scrittura**: un nodo e'
   primo estremo di **molti** archi, e in numpy l'indicizzazione fancy **in scrittura**
   fa **vincere l'ultimo**. ### **Tutti gli altri contributi sono scartati IN SILENZIO**
   — e non e' una somma mancata, e' ### **una scelta implicita fatta dall'ORDINE
   DELL'ARRAY** *(il file usa `np.add.at` altrove, p.es. a `:9115`)*.
3. ### **`dir_laterale = (-y, x, 0)` privilegia l'asse `z` del LABORATORIO**, mentre i
   nodi stanno in **3D** *(`:4940`: `u = rng.normal(size=(n, 3))`)*.

> ### **LA DECISIONE: il sito SI SPEGNE con un flag proprio.** `MEM_MOTO_TUTTO` e
> `MEM_MOTO` ### **restano come sono.**
> ### **E si apre la voce nuova `FASE-TRASCINAMENTO-3D`** *(aperta, difetto)*: serve
> ### **un asse fisico locale al posto di `z`**. ### ⛔ **E' LEGGE NUOVA, NON UNA
> ### RIPARAZIONE** — e per questo **non** si scrive adesso.

## LA STELLA POLARE — **le cinque risposte, PRIMA del codice** *(`L-STELLA`)*

*(Si rispondono sulla **cura decisa**, cioe' la forma di `proj` della decisione (1), e
sullo **spegnimento** della decisione (2). ### **Anche solo con <<non si applica,
perche' ...>>, e il <<perche'>> e' parte della risposta.**)*

### **1. `A14`: conserva energia e carica LOCALMENTE?**

### **NON SI APPLICA ALLA CARICA**, perche' `d0` e' una **lunghezza di riposo** e non
trasporta carica: il sito non tocca `perc_chi` ne' `psi`.
### ⚠ **E SULL'ENERGIA LA RISPOSTA ONESTA E' CHE IL MODELLO NON HA UN'ENERGIA
### TOTALE**, ed e' **dichiarato**: `ENERGIA-NON-DEFINITA`. ### **Quindi non posso dire
<<conserva>>, e non lo dico.**

> ### ✅ **MA UNA COSA LA FORMA DECISA LA GUADAGNA, ed e' misurabile:** la forma
> vecchia inietta una variazione di `d0` ### **anche quando il sistema si muove TUTTO
> INSIEME** *(traslazione rigida: `5.645e+00`)*. ### **La forma decisa da' `0` esatto.**
> Un moto d'insieme non deforma le lunghezze di riposo: ### **questo e' un passo VERSO
> `A14`, non una dimostrazione di `A14`.**

### **2. A quale dei TRE GRADINI arriva il risultato?**

| gradino | risposta |
|---|---|
| **(a)** robusto al rumore numerico | ### **DA MISURARE**, ed e' il punto (a) del mandato: la distribuzione di `abs(proj)` e la frazione di archi **saturi** al taglio |
| **(b)** regge togliendo la legge pratica | ### ⛔ **E' LA DOMANDA PIU' PERICOLOSA DI QUESTA MISURA**, e la misura la affronta di petto — vedi sotto |
| **(c)** coincide con un limite noto | ### ✅ **SI', E SU DUE LIMITI ESATTI:** traslazione rigida -> `0` esatto, scambio `i<->j` -> **identita' al bit**. ### **La forma vecchia non arriva a nessuno dei due.** |

> ### ⛔ **IL GRADINO (b), ED E' PERCHE' IL MANDATO CHIEDE LA FRAZIONE DI SATURI:**
> la **legge pratica** qui e' il `clip` a `passo_max = 0.01*mediana(d0)` *(`:9144-9145`)*.
> ### **Se quasi tutti gli archi SATURANO, allora cio' che si osserva non e' la legge:
> ### e' IL TAGLIO**, e cambiare la forma di `proj` cambierebbe **solo il segno** di una
> quantita' che vale comunque `+/- passo_max`.
> ### ⚠ **Lo scrivo ADESSO, prima di vedere il numero, perche' detto DOPO sarebbe una
> ### scusa.** Se la frazione di saturi e' alta, il referto deve dirlo come **risultato
> principale**, non come nota.

### **3. Aggiunge un numero o una legge?**

### **NESSUN NUMERO NUOVO: ZERO.** `I`, `Imed`, `mem_mot`, `dir` esistono tutti; la
forma decisa li **ricombina**.

**E IL CONTO DELLE LEGGI** *(`9-ter`)*: la decisione (1) ### **non aggiunge una legge:
ne CAMBIA LA FORMA**, e il numero di leggi resta lo stesso. La decisione (2)
### **ne TOGLIE una dal percorso** *(il sito si spegne)* e ### **ne annuncia una nuova,
`FASE-TRASCINAMENTO-3D`, che NON si scrive adesso** — quindi oggi il conto
### **scende di uno**.

### ⚠ **E IL `clip` NON SI TOCCA, e va detto che E' un clip:** `passo_max =
0.01*mediana(d0)` e' ### **una proiezione/pavimento nel senso della domanda 3**, e
contiene ### **un numero scelto: `0.01`**. ### ⛔ **Non e' parte di questa decisione,
e non lo rimuovo di mia iniziativa** *(`A11` chiederebbe: da quale ERRORE protegge?)*.
### **Ma la misura lo PESA**, e se mordesse quasi sempre sarebbe ### **un candidato per
`A11` e per `CLIP-INVENTARIO`**, da portare a Luca col numero.

### ✅ **E NON COMPENSA UN DIFETTO: NE RIPARA UNO.** La forma vecchia e'
**asimmetrica per costruzione** — `MEM-HEBB-VERSO` lo ha **misurato** il 2026-10-01
*(da `1e-15` a `1e-1` in una voce, fattore `1e14`)*. ### **Qui non si tara niente: si
sostituisce una forma che dipende dall'ordine di memorizzazione dell'arco con una che
non ci dipende.**

### **4. Tocca `rho`, `c_s` o il SEGNO?**

> ### ⛔ **IL SEGNO: SI', ED E' ESATTAMENTE IL BERSAGLIO.**

La forma vecchia ### **cambia segno invertendo il verso dell'arco** — verificato
sopra: `max abs(p(i,j) + p(j,i)) = 0.000e+00`, cioe' ### **p(j,i) = -p(i,j)**, un'identita'
e non un'approssimazione. ### **`d0` e' una lunghezza di riposo e NON HA VERSO: il segno
della sua variazione non puo' dipendere da come l'arco e' stato memorizzato.**

**`rho` e `c_s`: NON direttamente.** Il sito scrive `d0`, che entra nella **metrica** e
quindi in `cs_eff(rho)` ### **a valle, nel passo dopo**. Lo dichiaro come effetto
**indiretto** e non come <<non lo tocca>>.

**IL VERSO DELL'ACCOPPIAMENTO:** ### **non e' l'asse EM<->curvatura** della domanda 4.
`mem_mot` nasce da `grad_tw` *(torsione)*, e scrive su `d0` *(geometria)*: e'
### **curvatura -> curvatura**, per il tramite della torsione. ### **La voce
`EM-CURVATURA-BIDIREZIONALE` non si applica, e il perche' e' questo.**

### **5. Emergente o imposto: il fenomeno sopravvive se si toglie la legge pratica?**

### **DA MISURARE, e la misura e' proprio quella del punto (a).** Il <<fenomeno>> e' lo
spostamento di `d0` dovuto alla memoria del moto; la <<legge pratica>> e' il `clip`.
### ⛔ **Se la frazione di saturi fosse ~1, il fenomeno sarebbe IMPOSTO dal taglio e
### non emergente**, e questo varrebbe ### **per ENTRAMBE le forme**, vecchia e decisa.

### ⚠ **E SULLA DECISIONE (2) LA RISPOSTA E' DIVERSA, e piu' netta:** spegnere un
sito **non fa emergere** niente. ### **La domanda 5 li' diventa: cio' che oggi si vede
DIPENDE da quel sito?** E il mandato chiede di misurarlo — punto (b), i contributi
scartati da <<l'ultimo vince>>: ### **se la somma dei moduli scartati e' molto piu'
grande di quella applicata, allora cio' che il sito fa oggi NON E' la legge che il
commento descrive, ed e' un ARTEFATTO DELL'ORDINE.**

## LA MISURA, come il mandato la detta

**Sulla scena del driver** *(`nmasse` e `sep` dall'argv)*, **seme 11**, **72 e 150
passi**, sul blob ### **`e2940b3c`**. ### **Le grandezze nuove si calcolano A LATO,
senza scriverle:** il simulatore non si tocca, la patch sta su una **copia**.

### **(a) `d0`: forma vecchia contro forma decisa, su ogni arco e a ogni passo**

1. distribuzione di `abs(proj)` ### **PRIMA del taglio**: `min`, **mediana**, `p99`,
   `max`, per ciascuna forma;
2. frazione di archi ### **SATURI** al taglio `passo_max = 0.01*mediana(d0)`
   *(`:9144`)*, ### **per ciascuna forma**;
3. frazione di archi in cui ### **il SEGNO cambia** fra le due forme;
4. ### **somma CON SEGNO** di `Delta d0` per passo, per ciascuna forma.

### **(b) La fase**

1. nodi con ### **piu' di un arco come primo estremo**;
2. contributi ### **scartati da <<l'ultimo vince>>**: **numero** e **somma dei moduli
   scartati contro quella applicata**;
3. distribuzione di `abs(shift)`;
4. frazione ### **saturata dal taglio `pi/4`** *(`:9528`)*.

### **(c) Dall'AST: il sito (2) gira DAVVERO nella configurazione del driver?**

`MEM_MOTO_TUTTO` e i gate a ### **`:9488` e `:9490`** *(erano `:9391`/`:9393`)*.

> ### ⛔ **SOLO NUMERI, nessun `PASSA`/`FALLISCE` fuori dai controlli.** E la
> **piattaforma** si dichiara.

## I TRE CONTROLLI CHE POSSONO FALLIRE — **fissati e committati PRIMA di girare**

| | che cosa pretende | e se fallisce |
|---|---|---|
| **C1** | la mia **forma vecchia**, ricalcolata a lato, coincide ### **AL BIT** col `proj` del simulatore, ### **dopo il taglio**, su ogni arco | ### ⛔ **misuro un'altra cosa: FERMO** |
| **C2** | forma decisa con `mem_mot` sostituita da un ### **vettore costante** *(traslazione rigida)*: `proj = 0` ### **esatto** su ogni arco — ### **e la forma VECCHIA sullo stesso ingresso deve dare un `proj` NON nullo** | ### ⛔ **se la vecchia da' zero, il caso NON DISCRIMINA: FERMO** |
| **C3** | ### **scambio `i<->j` su TUTTI gli archi**: la forma decisa e' ### **identica al bit**, la vecchia ### **cambia segno** | ### **il controllo non discrimina: FERMO** |

### ✅ **E `C2` HA DENTRO IL SUO CONTROLLO POSITIVO, che e' la parte che conta:** non
basta che la forma decisa dia zero — ### **uno zero puo' venire da uno strumento che non
calcola niente.** Serve che la vecchia, ### **sullo STESSO ingresso**, dia **non zero**.
### **Senza quella meta', `C2` sarebbe un FALSO-ZERO.**

### ⚠ **E `C1` E' IL PIU' ESPOSTO, perche' pretende l'identita' AL BIT:** `proj` passa
da `np.sum` su un prodotto, e ### **l'ordine delle somme cambia gli ultimi bit**. Se
`C1` fallisse per `1e-16`, ### **la causa sarebbe l'aritmetica e non la legge** — ma
### ⛔ **il mandato dice <<AL BIT>>, e non lo ammorbidisco di mia iniziativa:** se
fallisce, mi **FERMO** e porto a Luca il numero e la causa. ### **Ammorbidire un
controllo perche' ha fallito e' il modo di non avere controlli.**

## I CRITERI DEL SIGILLO DELLA CURA — **per i commit successivi**

*(Il mandato li detta; qui si fissano, come per `VELENO-ARCHI-KEEP` in `b17caec`.)*

### **Per la decisione (1), la forma di `proj`:**

1. ### **BRACCIO 0**: la patch applicata al blob di **prima** ridA' il blob di **oggi**
   al byte, col *prima* preso dal ### **PADRE DEL COMMIT CHE HA CAMBIATO IL
   SIMULATORE** — ### ⛔ **non `HEAD~1`, che SLITTA** *(lo ha trovato il sigillo di
   `VELENO-ARCHI-KEEP` rifiutandosi di proseguire, `c7f2eb3`)*;
2. ### **IL CASO CHE DEVE FALLIRE: traslazione rigida** — la forma vecchia `!= 0`, la
   nuova `== 0`;
3. ### **scambio del verso degli archi: identita' AL BIT della legge nuova.**

### **Per la decisione (2), lo spegnimento:**

1. con il flag nuovo ### **ACCESO**: ### **identita' AL BYTE col blob di oggi**
   *(`e2940b3c`)* — ### **e' il controllo che il flag e' byte-inerte a default)*;
2. con il flag ### **SPENTO**: ### **le differenze devono stare SOLO in `phi` e a
   valle.** ### ⚠ **Se una differenza comparisse altrove, lo spegnimento non e'
   recintato dove credo.**

## L'ORDINE DEI COMMIT, come il mandato lo fissa

1. ### **questo task history** — e **si pusha PRIMA del lavoro**, cosi' l'ordine e'
   ### **verificabile da git** *(questo commit e' ANTENATO dei commit del lavoro)*
   ### **invece che asserito da me** *(par.8)*; insieme: le **due decisioni** in
   `doc/INDICE_ID.tsv` e la **voce nuova `FASE-TRASCINAMENTO-3D`**;
2. ### **lo strumento, PRIMA di girare** — coi tre controlli dentro;
3. ### **il referto, dopo** — **coi blob citati**.

### ⛔ **E IN QUESTO PASSO NON SI CURA NIENTE:** il simulatore `e2940b3c`
### **non si tocca.** Le forme nuove si calcolano ### **a lato**, su una **copia**
patchata.

## TODO DEL NEXT STEP — **operativo**

1. **commit di questo task history** + le due decisioni nell'indice +
   `FASE-TRASCINAMENTO-3D`;
2. **lo strumento** `csv/_test_fork/_mem_hebb_verso.py`: patch su una **copia** con
   ancore **contate**, che registri **a ogni passo** le grandezze (a), (b) e il censimento
   (c) dall'**AST**; ### **i tre controlli dentro, piu' il collaudo su dati sintetici**;
   ### **un battito per passo** *(debito gia' pagato una volta: senza, una richiesta di
   stato deve STIMARE il passo invece di leggerlo)*;
3. **commit dello strumento**, col suo blob nell'inventario *(par.6)*;
4. **le due corse**: `72` e `150` passi, seme `11`;
5. **il referto** `doc/REFERTO_mem_hebb_verso_2026-10-05.md`, coi blob citati e la
   **piattaforma**; la **frazione di saturi** come ### **risultato principale se e' alta**;
6. **la relazione** e la voce d'indice aggiornate ### **nello stesso giro** *(par.4)*.

### ⛔ **E CIO' CHE NON SI FA IN QUESTO PASSO:** ### **la cura.** Ne' la forma di
`proj`, ne' il flag nuovo, ne' `FASE-TRASCINAMENTO-3D`. ### **Il passo (1) MISURA.**

## TODO ALLA RIPRESA — **IL PROGRAMMA, deciso da Luca il 2026-10-05**

> ### ⛔ **E' L'ORDINE DEI LAVORI, e non lo decido io.** Ogni voce ha il suo task
> ### history, il suo sigillo coi criteri committati **prima**, e i suoi commit.

| | il lavoro | dove vive |
|--:|---|---|
| **1** | ### ✅ **`Z43` passo (1), la misura del tempo proprio `r`** | ### **FATTA** — `doc/REFERTO_z43_tempo_proprio_2026-10-05.md` *(`66a798d`)* e `doc/REFERTO_z43_compton_C2_2026-10-05.md` *(`9cec5d8`)* |
| **2** | **`MEM-HEBB-VERSO` passo (2):** lo **spegnimento** del sito della fase | `doc/TASK_HISTORY/2026-10-05_mem-hebb-verso-cura2-fase.md` |
| **3** | la **decisione di Luca sulla definizione di `r`**, dopo il referto di `Z43`; poi **la cura di `r`** col suo sigillo | ### ✅ **DECISA** il 2026-10-05 — `doc/TASK_HISTORY/2026-10-05_z43-due-cure-tempo-proprio.md` |
| **4** | **`TETTO-CAUSALE-TEMPO-COORDINATO` passo (2)** *(il mandato lo abbrevia in `TETTO-CAUSALE`; ### **la chiave intera e' questa** — par.9: **un ID non e' un nome, e' una CHIAVE**)* e la **cura (1) di `MEM-HEBB-VERSO`** *(la forma di `proj`)*, ### **PENSATI INSIEME** perche' toccano la stessa funzione, ### **ma in commit separati, ciascuno col suo sigillo** | da aprire |

### **L'IDEA DA VALUTARE AL PUNTO 4, e la decisione e' di Luca ALLORA**

> Il taglio `passo_max = 0.01*mediana(d0)` — ### **numero a mano, mediana globale, e
> comanda sul `40-55%` degli archi** *(misurato in `2717308`)* — ### **sostituito dal
> limite causale `c_s*dt_e` dell'arco.**
> ### ⛔ **DECISIONE DI LUCA, da prendere ALLORA.**

## ⛔ IN SOSPESO: **la decisione (1) va RICONFERMATA da Luca prima della sua cura**

*(Scritto tale e quale come Luca lo ha dato.)*

> La decisione (1) — `proj = 0.5*(I_i+I_j)/Imed*(m_j-m_i).dir` — va **RICONFERMATA**
> da Luca prima della sua cura, ### **alla luce di DUE FATTI EMERSI DOPO:**

1. ### ⛔ **`mem_mot` NON e' una velocita':** rilassa verso `grad_tw` *(`:9130` su
   `e2940b3c`)*, quindi ### **`(m_j - m_i).dir` e' circa la CURVATURA DELLA TORSIONE
   lungo l'arco, non un moto relativo.** *(Le **simmetrie restano valide**.)*
2. ### ⛔ **la forma decisa satura al taglio sul `55%` degli archi** e ### **cambia la
   somma di `Delta d0` da `+6.7e3` a `-9.2e4`** *(referto `2717308`)*.

### 📌 **IL PRIMO FATTO E' UNA LETTURA DEL GUARDIANO, e lo registro come SUA:** non era
nel mio referto. ### **Io avevo misurato le SIMMETRIE della forma decisa e le avevo
trovate; non mi ero chiesto CHE COSA `mem_mot` SIA.** ### **E' una domanda che il mio
referto non ha posto.**

## L'OSSERVAZIONE DEL GUARDIANO sul tempo proprio dentro `memoria_hebbiana_moto`

> ### **Dentro `memoria_hebbiana_moto` NESSUN PASSO USA IL TEMPO PROPRIO:** `mem_mot`
> si aggiorna **per passo senza `dt`**, il taglio su `d0` ### **non ha tempo**, e i
> tetti usano ### **`DT`**.

### **Va nella voce `TETTO-CAUSALE-TEMPO-COORDINATO`**, ed e' li' che l'ho registrata.
