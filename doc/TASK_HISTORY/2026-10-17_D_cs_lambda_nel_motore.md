# PUNTO `D` — **LA FORMA DI `cs(Lambda)`: L'ATTUAZIONE, senza scegliere `Lambda_c`**

*(mandato unico del guardiano del `2026-10-16`, punto `D`, piu' le integrazioni del
`2026-10-17`. Base: `e38a2831`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE** *(`CLAUDE.md` §8)*, e contiene
> **LA STELLA POLARE** perche' **questo commit cambia la fisica** *(`[[L-STELLA]]`)*.

---

## 0. LA STELLA POLARE — *le cinque risposte, PRIMA del codice*

### **`1` — `A14`: questa legge conserva energia e carica LOCALMENTE?**

### ✅ **LA NORMA SI': ESATTAMENTE, e non per fortuna.** `cs` non aggiunge un termine a
`H`: ### **scala il tempo proprio del nodo** *(`dtau_k = cs_k * dt`)*, e ### **ogni pezzo
del passo e' unitario per QUALUNQUE `dtau`** — quindi `somma|psi|^2` e `V` restano
conservate ### **al bit**, come oggi.
### ⚠ **L'ENERGIA NO, e la violazione e' GIA' DICHIARATA:** `[[DEC-QC-CONSERVATA]]` dice
che ### **l'energia e' conservata solo al SECONDO ORDINE**, e `cs` ### **non aggiunge una
violazione nuova:** rende il passo ### **disomogeneo fra nodi**, che e' ### **la fisica
dichiarata del tempo proprio locale** *(`TEMPO-PROPRIO-LOCALE`)*.
### ⛔ **E C'E' UNA COSA DA MISURARE, non da assumere:** con `cs` ### **dinamico** il
secondo ordine di `M-B2` ### **potrebbe degradare.** ### **E' il criterio `D3`**, e se
degrada ### **lo riferisco invece di spiegarlo.**

### **`2` — a quale dei TRE GRADINI arriva il risultato?**

| | il gradino | dove arriva questo pezzo |
|---|---|---|
| `(a)` robusto al rumore numerico | ### ✅ **SUPERATO, e piu' che superato:** `D0` chiede ### **AL BIT** *(distanza del passo intero `= 0` ESATTO)*, e `D1` l'invarianza di scala ### **entro `8` ulp** |
| `(b)` regge togliendo la legge pratica | ### ✅ **E' il caso che DEVE fallire di `D4`:** ### **senza sorgente `cs` resta uniforme AL BIT** — cioe' il fenomeno ### **sparisce** quando si toglie cio' che lo produce |
| `(c)` coincide con un limite noto | ### ⛔ **NON RAGGIUNTO, e lo dico:** ### **non esiste un limite noto di `cs(Lambda)`** con cui confrontare. ### **Il confronto con la natura e' il rapporto `alpha_G/alpha`, e arriva dopo `L4`** *(`[[DOMANDA-LA-GERARCHIA-GRAVITA-EM]]`)* |

### **`3` — aggiunge un numero o una legge? Di che TIPO?**

> ### ⛔⛔ **AGGIUNGE UN NUMERO, ED E' IL PRIMO DEL MODELLO: `Lambda_c`.**
> ### **E' LA PRIMA SCALA ASSOLUTA** *(errore `n.2` del guardiano, registrato)*: tutte le
> leggi di oggi sono ### **RELAZIONALI** — `x = rho/Lambda` e' un rapporto, e
> `parametri: {}` in tabella. ### **`Lambda_c` rompe quella proprieta'.**

| | |
|---|---|
| **il tipo** | ### **COSTANTE DI ACCOPPIAMENTO** — non una toppa, non un clip. ### **E un accoppiamento e' LEGITTIMO e va solo DICHIARATO** *(`STELLA_POLARE`, la trappola della domanda `3`)* |
| ### ⛔ **compensa un difetto?** | ### **NO.** Non c'e' nessun errore che `Lambda_c` ripara: ### **introduce un effetto** *(la luce rallenta dove il vuoto e' tolto)*, e lo introduce ### **da zero** |
| ### ⛔ **e' emergente?** | ### **NO, OGGI E' SCELTO.** ### **Lo scrivo come il mandato chiede**, e la voce `[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]` lo tiene aperto |
| ### ✅ **nessun pavimento, nessun tetto** | `cs < 1` viene ### **dalla forma stessa** *(`cs = Lambda/(Lambda + Lambda_c)` sta in `[0, 1)` per costruzione)*: ### **non c'e' niente da tagliare** *(`A11`)* |
| ### ⚠ **e `Lambda = 0` da' `cs = 0`** | ### **non e' un pavimento: e' il valore della forma.** ### **E va VERIFICATO che i pezzi lo accettino** *(il nodo resta fermo)* ### **senza aggirare l'assert del cono** — e se un assert lo rifiuta, ### **relaziono invece di cambiarlo** |

### **`4` — tocca `rho`, `c_s` o il SEGNO? In quale VERSO?**

### ✅ **TOCCA `c_s`, ed e' il suo oggetto.** Il verso dell'accoppiamento e'
### **VUOTO → PROPAGAZIONE**, cioe' nel linguaggio di `[[EM-CURVATURA-BIDIREZIONALE]]`
### **curvatura → EM**: ### **la metrica** *(il vuoto locale)* ### **decide come si
propaga tutto il resto.**
### ⛔ **IL VERSO OPPOSTO — `EM → curvatura` — NON E' IN QUESTO PEZZO**, e non va
spacciato: ### **e' `L4`**, dove la `U` d'arco diventa dinamica. ### ⚠ **E un
accoppiamento a un solo verso NON e' quello della natura** *(e' il motivo per cui la
domanda `4` esiste)*: ### **questo pezzo fa META- del lavoro, e lo dichiara.**

### **`5` — emergente o imposto? Il fenomeno sopravvive togliendo la legge pratica?**

### ⛔ **`Lambda_c` E' IMPOSTO**, e il pezzo e' costruito perche' si veda:
### **con la forma SPENTA** *(`cs = 1`)* ### **non succede NIENTE, al bit** — il passo di
oggi, identico. ### **L'effetto compare SOLO con la forma accesa**, e ### **la sua
intensita' e' `Lambda_c/Lambda_medio`**, cioe' ### **un numero scelto a mano.**
### 📌 **E la nota di mappa che il mandato chiede** *(«strada quantistica per `Lambda_c`»,
sotto `L6`)* ### **e' esattamente il registro di questo:** la' `Lambda_c` potrebbe
### **smettere di essere scelta** e diventare ### **<<un quanto>>**. ### **Oggi il
simulatore e' il campo medio, e quella scala NON C'E'.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo, e cosa NON so*

### ⭐ **IL POSTO DOVE LA FORMA ENTRA, ed e' GIA' CABLATO**

`flussi_parziali.dtau_nodo(mot)` e' ### **l'unico posto da cui si legge il tempo proprio
per nodo** *(lo dice il suo docstring)*. ### ✅ **Quindi `cs` entra LA'**, e ### **non in
sette posti.**

### ⭐ **CHE COSA CREDO, PRIMA DI GUARDARE**

| | credo che… | e ### **NON LO SO** |
|---|---|---|
| `a` | con `cs = 1` il passo sia ### **identico AL BIT**: `1.0 * x` e' ### **esatto** in IEEE-754 | ### ⚠ **non so se la forma spenta sia davvero `1.0`**: se la scrivessi come `Lambda/(Lambda + 0)` avrei ### **`0/0` dove `Lambda = 0`** — quindi la forma spenta dev'essere ### **un ramo**, non `Lambda_c = 0` |
| `b` | l'invarianza di scala di `D1` ### **regga a `cs = 1`**: le leggi di oggi sono ### **rapporti** | ### ⛔ **se NON regge, c'e' una SCALA NASCOSTA in una legge di oggi** — e il mandato dice ### **STOP del punto `D`**, relazionando quale |
| `c` | il punto fisso di `D2` ### **converga in pochi giri** *(`cs` dipende da `Lambda`, e `Lambda` cambia poco in un passo)* | ### ⚠ **non so in SATURAZIONE PROFONDA**, e il mandato dice: se non converge, ### **relaziona coi numeri e NON scegliere un altro schema** |
| `d` | `Lambda = 0` ⟹ `cs = 0` ⟹ ### **il nodo resta fermo**, e i pezzi lo accettino | ### ⛔ **non so se l'assert del cono lo rifiuti:** `flussi_parziali._frazione_valida` pretende `0 < f <= 1`, e con `cs = 0` la frazione effettiva e' ### **`0`.** ### **Se lo rifiuta, RELAZIONO invece di cambiarlo** |

### ⛔⛔ **E LA COSA PIU' PROBABILE CHE MI FERMI E' `(d)`:** l'assert del cono e'
### **un presidio che ho rispettato finora**, e `cs = 0` ### **lo viola per costruzione.**
### ⚠ **Non lo cambio:** se succede, ### **il punto `D` si ferma la' e lo scrivo.**

---

## 2. PROGETTAZIONE — *i cinque passi, e i criteri FISSATI QUI*

| | il passo | il criterio, e cosa mi FERMA |
|---|---|---|
| `D0` | `cs` nel motore, ### **`Lambda_c` SENZA valore predefinito**; forma ### **SPENTA** di default | ### ⛔ **braccio `0`: `M-B1` `12`/`12` AL BIT** contro il commit prima di `D`, ### **PIU' la distanza del passo intero `= 0` ESATTO su ENTRAMBE le scene** *(l'integrazione del `2026-10-17`: e' ### **un CRITERIO**)*. ### **E il caso che DEVE fallire: con la forma ACCESA la distanza `> 0` su entrambe** |
| `D1` | l'invarianza di scala, ### **collaudo nuovo nella suite** | `lambda` in `{2, 0.5}` ### **al bit**, `3` entro ### **`8` ulp**; il caso che DEVE fallire ### **con la forma accesa**; la controprova ### **con `Lambda_c` scalata per `lambda^2`** |
| `D2` | `cs` dallo stato ### **al CENTRO del palindromo**, a ### **punto fisso fino agli ulp** | si ### **riportano** le iterazioni e il loro massimo; il caso che DEVE fallire: ### **<<`cs` a inizio passo>> perde il secondo ordine in `M-B2` e la simmetria `PTheta`** |
| `D3` | ### **`L1` RESTA CHIUSO** con `cs` dinamico | `0` violatori del tempo proprio · `M-B2` pendenza ### **`>= 1.9`** su ### **`>= 4`** dimezzamenti · `W A W A^-1 = 1` a ### **`<= 8` ulp** su ### **`>= 8`** stati · norme `M` e `V` conservate |
| `D4` | il verso e il profilo, ### **sorgente FOTOGRAFATA**, per `Lambda_c/Lambda_medio` in `{0.1, 1, 10}` | `cs` ### **CALA** vicino alla materia con ### **`>= 3` barre**, a `dtau` `0.5` e `0.25`; `delta cs` ### **LINEARE** in `delta Lambda` per `x` piccolo, confrontato con ### **`Lambda_c/(Lambda_medio + Lambda_c)^2`**; il profilo radiale ### **in tabella**; il caso che DEVE fallire: ### **senza sorgente `cs` resta uniforme AL BIT** |

### ⛔ **E L'ACCENSIONE DI `D4` SI DICHIARA, E SI USA UGUALE PER I TRE `Lambda_c`**
*(integrazione del `2026-10-16`, errore `n.3`)*: ### **la rampa agiva solo da una parte**, e
un confronto fra tre valori ### **con accensioni diverse non e' un confronto.**

### ⛔⛔ **CIO' CHE NON SI FA IN QUESTO MANDATO**, e il mandato lo dice: ### **la
deflessione della luce**, ### **due masse che si avvicinano**, ### **l'auto-legame.**
### **Sono le misure che CHIUDONO `L2`, e vengono DOPO la scelta di `Lambda_c`.**

---

## 3. TODO

1. **`D0`**: `cs` in `flussi_parziali`, `Lambda_c` nel motore ### **senza default**, la
   ### **scheda** di `Lambda_c` *(generata, non scritta a mano)*, e il ### **braccio `0`**
   coi due criteri.
2. **`D1`**: `primo_ordine/_collauda_scala.py`, nella suite.
3. **`D2`**: il punto fisso al centro del palindromo, ### **coi giri riportati.**
4. **`D3`**: i quattro criteri di `L1`.
5. **`D4`**: il verso e il profilo, ### **accensione dichiarata e uguale.**
6. le ### **due note di mappa** *(la strada quantistica sotto `L6`; l'alternativa
   `Lambda_c = Lambda_medio` ### **considerata e NON presa**, con i due motivi)*.
7. ### **LA DOMANDA PER LUCA** sul valore di `Lambda_c/Lambda_medio` — ### **la `G` del
   modello** — coi numeri di `D4`, ### **registrata come voce** e committata.
   ### ⛔ **Non scelgo.**
### ✅ **ANNOTAZIONE DEL `2026-10-17`, a cose fatte** *(e NON riscrivo niente di sopra)*

La meta' ### **`PTheta`** del caso che DEVE fallire di `D2` e' ### **FATTA**, e sta in
`_misura_theta_nonlineare.py` *(bracci `(5)`, `(6)`, `(7)`; `36` su `36`)*:
### **`cs` al CENTRO `2`-`6` ulp, `cs` a INIZIO PASSO `3e14`-`2.5e15` ulp**, banda
`4096`.
### ⚠ **E una cosa che qui non avevo previsto:** per farla ho dovuto curare
### **la scena**, perche' il divieto del vuoto nullo ### **aveva rotto tre strumenti** --
e ### **la suite non li girava.** Sta nella `40` della RIPRESA.
