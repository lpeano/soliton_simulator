# IL PUNTO MEDIO **PER PEZZO** — *il secondo ordine di `G`, e NON una legge nuova*

> ### 📌 **Decisione di Luca del `2026-10-18`, `12:07`:** ogni pezzo usa
> ### **il proprio peso al PROPRIO punto medio.** ### ✅ **Luca approva il cambio di
> schema che avevo indicato**, e ### **i criteri del mandato sono copiati qui PRIMA della
> misura.**

> ### ⛔ **E QUESTO FILE SI COMMITTA PRIMA DEL CODICE:** l'ordine e'
> ### **verificabile da `git`** *(questo commit e' ANTENATO dei commit del codice)*.

---

## 0. LA STELLA POLARE — *le cinque risposte, PRIMA del codice*

### ⛔⛔ **E PRIMA DI TUTTO, LA COSA CHE IL MANDATO CHIEDE DI DICHIARARE:
QUESTO E' UN CAMBIO DI SCHEMA, NON UNA LEGGE NUOVA.**
### **La legge dice CHE COSA fa un pezzo** *(`CAMM-SPOSTAMENTO-VUOTO` scambia le due
estremita' dell'arco)*; ### **lo schema dice QUANDO si valuta il peso** che quel pezzo
usa. ### ✅ **Il secondo e' mestiere dell'INTEGRATORE**, e `P-ES1` lo dice:
### **l'esecutore e' uno**, e i pezzi scritti a mano ### **si dichiarano.**

### ⭐⭐ **E L'IMPRONTA DELLA TABELLA NON CAMBIA, con il suo perche':**
### **`leggi.yaml` NON SI TOCCA** -- nessuna riga di legge, nessun campo, nessun ordine --
quindi l'impronta della composizione resta ### **`2e7f795d2a52fbe7`** e quelle delle
singole leggi restano le loro.
### ⚠ **E se avessi scritto lo schema nella SCHEDA della legge, l'impronta SAREBBE
cambiata** *(la scheda entra nell'impronta)*: ### **e sarebbe stato sbagliato**, perche'
direbbe che ### **la legge e' cambiata** mentre e' cambiato ### **il modo di integrarla.**
### ✅ **Lo schema si documenta dove vive: nel codice e nel registro della fisica.**

### **`1` — `A14`: questa legge conserva energia e carica LOCALMENTE?**

### ✅ **LE NORME SI', E PER LA STESSA RAGIONE DI PRIMA:** il punto medio
### **cambia l'ANGOLO** che il pezzo applica, ### **non la sua forma** -- e il pezzo
### **resta unitario per costruzione.** ### **Quindi `M` e `V` restano**, e il braccio
`(4)` di `D3` lo rimisura.
### ⭐⭐ **E L'ENERGIA E' L'OGGETTO DI QUESTO MANDATO:** `G` oggi deriva al
### **PRIMO ordine** *(`1.002`)*, e il criterio `C1` chiede ### **`>= 1.9`.**
### ⚠ **E se non ci arriva, NON si aggiusta: si misura la pendenza PEZZO PER PEZZO,
si localizza il prossimo ostacolo, si committa e si FERMA** *(il punto `4` del mandato)*.

### **`2` — a quale dei TRE GRADINI arriva il risultato?**

### ✅ **GRADINO `(a)`, robusto al rumore numerico:** pendenze su `>= 4`
dimezzamenti, bande dichiarate, ### **due casi che DEVONO fallire** *(i pesi bloccati, e
il segno di `Omega`)*, e ### **un controllo positivo che misura `O(dtau)`.**
### ✅ **E GRADINO `(b)`:** con la forma `cs` ### **SPENTA** i pesi
### **non dipendono dallo stato**, quindi ### **il punto medio COINCIDE col peso
bloccato** -- e il passo resta ### **AL BIT.** ### **Cioe' lo schema si puo' togliere, e
si vede cosa si perde.**
### ⛔ **GRADINO `(c)` NO:** nessun limite noto con cui confrontare `G`.

### **`3` — aggiunge un numero o una legge? Di che TIPO?**

### ✅ **NESSUNA LEGGE** *(e' un cambio di schema: vedi sopra)*, e
### **NESSUN NUMERO NUOVO DI FISICA.**
### ⚠ **MA DUE NUMERI DI METODO, e li dichiaro perche' esistono:** la
### **tolleranza del punto fisso** e il ### **tetto dei giri.**
### ✅ **E NON SONO NUOVI NEANCHE LORO:** la tolleranza e' ### **la stessa di `D2`**
*(`EPS_CS = 8 eps`, relativa)*, e il tetto e' ### **della stessa famiglia di
`GIRI_MAX`** -- cioe' ### **il numero oltre il quale si DICHIARA che non converge**, col
massimo misurato scritto accanto. ### ⛔ **Non sono manopole: nessuno dei due cambia
il risultato, uno lo CERTIFICA e l'altro FERMA.**

### **`4` — tocca `rho`, `c_s` o il SEGNO? In quale VERSO?**

### ✅ **TOCCA `c_s`**, cioe' ### **il peso che ogni pezzo usa** -- e
### **non `rho`, e non il segno.**
### ⛔⛔ **E NON E' UN ACCOPPIAMENTO NUOVO: e' LO STESSO, valutato in modo
coerente nel TEMPO.** ### **Quindi non mi aspetto nessun cambio di VERSO**, e
### **`C4` lo misura** *(oggi: `-3.145` con la forma accesa contro `-3.919` spenta)*.
### ⚠⚠ **E SE IL VERSO CAMBIASSE SAREBBE UN RISULTATO GRAVE**, non un
dettaglio: vorrebbe dire che ### **i due schemi NON sono due approssimazioni della stessa
dinamica** -- e allora si ferma.

### **`5` — emergente o imposto? Il fenomeno sopravvive togliendo la legge pratica?**

### ✅ **LO SCHEMA E' UNA SCELTA NUMERICA, non un pezzo di fisica**, e si vede:
### **a forma spenta SPARISCE** *(il punto medio coincide col peso bloccato, AL BIT)*.
### ⭐ **La fisica e' `G`**, e lo schema serve ### **a integrarla senza inventare
niente.**
### ⚠ **E `Lambda_c` resta IMPOSTO** *(`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`)*: questo
mandato ### **non lo tocca.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo, e cosa NON so*

### ⭐ **IL FATTO DA CUI PARTO, ED E' MIO E MISURATO** *(referto
`strada_d_c1_c2_c5.txt`, blob `092a4056`)*: ### **`CAMM-SPOSTAMENTO-VUOTO` muove `Lambda`
di `O(dtau)` DENTRO la propria applicazione** *(`4.02`, `1.99`, `1.03`, `0.52`, `0.26` al
dimezzare)*, mentre ### **`CAMM-GROVER-VUOTO` e `CAMM-SPOSTAMENTO` la conservano**
*(`5e-15` e `0.0`)*.

### ⛔⛔ **MA QUEI NUMERI SONO SU TRE PEZZI, E IL MANDATO NE CHIEDE QUATTORDICI
-- e ha ragione:** ### **un elenco ATTESO non e' una misura.** ### ✅ **Quindi il
primo passo e' MISURARE TUTTI E `14`**, e ### **scrivere i numeri che ho VISTO.**
### ⚠ **E se un pezzo che NON mi aspetto muove `Lambda`, il mandato dice che
### **si segnala PRIMA, con un commit, come osservazione** -- e lo faro'.

### ⭐ **CHE COSA CREDO, PRIMA DI GUARDARE** *(e lo scrivo per poterlo sbagliare)*:

| il pezzo | muove `Lambda`? | il motivo che credo |
|---|---|---|
| `CAMM-MATERIA-VUOTO` | ### **NO** | da' ### **una FASE** a `phi`, e una fase non cambia `|phi|` |
| `CAMM-FASE-VUOTO` | ### **NO** | idem: e' ### **una fase**, uniforme nel nodo |
| `CAMM-MONETA-SPIN` | ### **NO** | tocca ### **solo `psi`** |
| `CAMM-GROVER` | ### **NO** | solo `psi` |
| `CAMM-SPOSTAMENTO` | ### **NO** | solo `psi` |
| `CAMM-GROVER-VUOTO` | ### **NO** | e' unitario ### **DENTRO il nodo**, e `Lambda_k` e' la somma del nodo: la somma resta |
| `CAMM-SPOSTAMENTO-VUOTO` | ### **SI'** | mescola `phi` ### **FRA due nodi**, e la somma di ciascuno ### **cambia** |

### ⚠ **E LA COSA CHE NON SO E' PIU' FINE:** `Lambda` ### **non si muove solo per
il pezzo che la muove.** Il peso d'arco e' ### **la media armonica dei DUE capi**, quindi
dipende da `Lambda` di ### **due nodi** -- e il punto medio del pezzo d'arco
### **li legge entrambi.** ### **Se il punto fisso non convergesse**, il mandato dice di
### **relazionare, non di cambiare schema.**

### ⛔⛔ **E UNA COSA CHE POTREBBE NON BASTARE, e la dico adesso:** il punto medio
### **PER PEZZO** rende ogni pezzo ### **del secondo ordine nel proprio peso**, ma
### **la composizione resta quella** -- e se restasse un'asimmetria
### **fra i due mezzi del palindromo**, la pendenza ### **non arriverebbe a `1.9`.**
### ✅ **E in quel caso il punto `4` del mandato dice cosa fare: pendenza PEZZO PER
PEZZO, localizzare, committare, FERMARSI.**

---

## 2. PROGETTAZIONE — *i passi, le dichiarazioni, e i criteri FISSATI QUI*

### ⭐⭐ **A QUALE PUNTO MEDIO, e perche': SULLO STATO, non sulla media di `cs`**

### ✅ **Il peso si valuta sullo STATO A META' DEL PEZZO** *(la regola del
### **PUNTO MEDIO IMPLICITO**)*, e non come ### **media dei due `cs`** agli estremi.
### ⛔ **I DUE NON SONO LA STESSA COSA, e il motivo e' che `cs` e' NON LINEARE in
`Lambda`:** ### **`media(cs(Lambda)) != cs(media(Lambda))`.**
### ✅ **E lo STATO e' l'oggetto primitivo:** la regola del punto medio implicito e'
### **del secondo ordine E simmetrica nel tempo** *(cioe' REVERSIBILE)*, ed e'
### **la proprieta' che serve a non rompere il palindromo.**
### 📌 **E la differenza fra le due letture SI MISURA**, e va nel referto come
informazione: ### **cosi' la scelta non e' un'opinione.**

### ⛔ **LA TOLLERANZA E IL TETTO, dichiarati:** ### **la stessa di `D2`**
*(`EPS_CS = 8 eps`, RELATIVA al valore)*, e il tetto ### **della famiglia di `GIRI_MAX`**
-- e il mandato chiede ### **medio e massimo dei giri**, sulla scena di `D3` e sulle
### **quattro `Lambda_c` gia' usate.**
### ✅ **E le quattro sono DICHIARATE, non scelte adesso:** i rapporti
### **`0.1`, `1`, `10`** *(i tre di `D4`, dal mandato del `2026-10-16`)* e
### **`0.3`** *(il massimo MISURATO del punto fisso di `cs`)*.

| | il passo | cosa DECIDE | cosa mi FERMA |
|---|---|---|---|
| `1` | ### **i `14` pezzi**: quanto muove `Lambda` ciascuno | ### **DOVE** va il punto medio | un pezzo ### **inatteso** -> si segnala con un commit, PRIMA del codice |
| `2` | il peso al punto medio ### **nei pezzi che lo chiedono** | lo schema | il punto fisso ### **non converge** -> si relaziona |
| `3` | braccio `0`: forma spenta ### **AL BIT** | che lo schema sia ### **inerte a default** | un bit che si muove -> ### **STOP** |
| `4` | `C1`, e i suoi due casi che DEVONO fallire | se lo schema ### **porta `G` al secondo ordine** | `C1 < 1.9` -> ### **pendenza pezzo per pezzo, commit, STOP** |
| `5` | `C2`, `C4`, `C5`, i quattro di `D3` | che ### **niente altro si rompa** | il ### **VERSO** di `C4` che si inverte -> ### **STOP** |

### ⛔ **I CRITERI, COPIATI DAL MANDATO PRIMA DELLA MISURA:**
### **`C1`** pendenza di `G` ### **`>= 1.9`** *(fissato ora)*;
### **il caso che DEVE fallire:** lo ### **STESSO codice coi pesi BLOCCATI** deve ridare
### **`1.002 +- 0.01`**, e ### **si verifica che fallisca per la CHIAVE GIUSTA**;
### **il controllo positivo:** il peso usato dal pezzo deve differire da quello bloccato
di ### **`O(dtau)`**, coi numeri ### **al dimezzare**;
### **la reversibilita':** `+h` poi `-h` ### **torna all'inizio** entro la tolleranza
dichiarata;
### **il braccio `0`:** `M-B1` ### **al bit** e distanza del passo intero
### **esattamente `0`**, su ### **entrambe** le scene;
### **e si rifanno** `C2`, `C5`, i ### **quattro criteri di `D3`** e ### **`C4`**, con la
variazione rispetto a oggi *(`D3(2) = 1.254`, `C4` `-3.145` contro `-3.919`)*, e il
### **costo** contro ### **`3.7`-`9.7`.**

---

## 3. TODO DEL NEXT STEP

1. ### **La misura dei `14` pezzi**, e il commit dell'osservazione se c'e' una sorpresa.
2. `flussi_parziali`: il peso ### **dato** al pezzo *(`hop_phi` con `s` esplicita)*, e il
   ### **punto fisso** nel solo pezzo che lo chiede.
3. Il braccio `0`, poi `C1` coi suoi due casi, il controllo positivo e la reversibilita'.
4. `C2`, `C5`, `D3`, `C4`, e il costo.
5. I referti ### **dal blob committato**, la `RIPRESA`, la relazione.
6. La mappa: ### **l'alternativa di Luca** *(la memoria invece del punto fisso)*,
   ### **solo la voce, senza codice.**


---

## 4. ⭐⭐ LE PRECISAZIONI DEL `2026-10-18` — *quale punto medio, e che cosa accoppia*

> ### 📌 **Precisazioni al mandato**, e ### **stanno QUI perche' vengono PRIMA
> del codice del punto fisso.**

### `A1)` ⛔⛔ **QUALE REGOLA SIMMETRICA USO: LA `(ii)`, LA MEDIA DEI DUE `Lambda`**

```
Lambda_medio = (Lambda_0 + Lambda_1)/2        e il peso si legge LA' DENTRO
```

### ⚠ **E la `(i)` -- `Lambda` calcolato sul `phi` medio `(phi_0 + phi_1)/2` -- NON la
uso, per un motivo che si CONTROLLA:** ### **`(phi_0 + phi_1)/2` NON E' UNO STATO DEL
FLUSSO.** Il pezzo e' ### **una rotazione**, e la media fra il punto di partenza e quello
d'arrivo di una rotazione di angolo `theta` ha norma ### **`cos(theta/2)`** volte quella
di partenza -- quindi `Lambda` letta la' e' ### **sistematicamente PIU' PICCOLA**, di un
fattore ### **`cos^2(theta/2)`.**
### ⛔ **E' un errore `O(h^2)`**, cioe' ### **non rompe il secondo ordine** -- ma e'
### **un BIAS con un segno**, e fra due regole che costano uguale ### **si prende quella
che non ce l'ha.**
### ✅ **La `(ii)` non ha quel difetto:** e' ### **la media di DUE `Lambda` VERI**, cioe'
di due stati che il flusso attraversa davvero.
### 📌 **E LA `(i)` LA MISURO COMUNQUE, come informazione:** ### **`C1` per tutte e
due**, nel referto. ### ⛔ **Non e' un criterio nuovo:** il criterio e' `C1 >= 1.9`, e
quello resta uno.

### ⚠ **E UNA TERZA REGOLA ESISTE, e la scarto DICENDOLO:** il peso allo stato
### **a META' del pezzo** *(`Phi(h/2)`)*, che e' ### **la piu' fedele alla frase
<<il proprio punto medio>>** e ### **non ha il difetto di norma.**
### ⛔ **Non la uso perche' il mandato chiede di scegliere fra le DUE**, e perche'
costerebbe ### **un'applicazione in piu' per giro** *(mezzo pezzo per il punto medio, poi
il pezzo intero)*. ### **Sta scritta perche' la scelta sia leggibile, non per nasconderla.**

### `A2)` ⛔⛔ **IL PUNTO FISSO NON E' PER ARCO: ACCOPPIA LA RETE INTERA**

### **`hop_phi` applica TUTTI gli archi insieme**, e ### **`Lambda_k` somma i semiarchi di
PIU' archi** -- quindi il peso di un arco dipende da `Lambda` dei suoi due nodi, che
dipendono da ### **tutti gli archi che li toccano.**
### ✅ **Quindi il punto fisso e' UNO, su tutta la rete**, e ### **non `m` punti fissi
indipendenti.** ### **Lo dichiaro perche' cambia cio' che il numero dei giri misura:**
non *«quanto e' difficile un arco»* ma ### **quanto e' accoppiata la rete.**
### 📌 **E IL MANDATO CHIEDE LA DIPENDENZA DALLA TAGLIA, e ha ragione:** se il punto
fisso accoppia la rete, ### **i giri possono crescere con la taglia** -- e questo
### **si misura**, su ### **almeno DUE taglie** oltre alle ### **quattro `Lambda_c`**
gia' dichiarate *(i rapporti `0.1`, `0.3`, `1`, `10`)*.
### ⚠ **E se i giri crescessero con la taglia sarebbe una cosa da dire a Luca**, perche'
vorrebbe dire che ### **il costo per tick non e' una costante del modello** ma
### **una funzione della rete.**
