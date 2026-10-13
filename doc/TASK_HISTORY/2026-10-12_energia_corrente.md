# `P3` — **L'ENERGIA COME SOMMA DI DENSITA' LOCALI, E LA CORRENTE SUGLI ARCHI**

> **Mandato di Luca, `P3`:** *«`E` calcolata come **SOMMA DI DENSITA' LOCALI** (per
> estremita' e per nodo), **mai come prodotto globale**; la **DERIVAZIONE** della
> **CORRENTE SUGLI ARCHI `J`**, tale che per ogni nodo la variazione della sua energia in
> un tick sia la somma di cio' che entra ed esce dai suoi archi. Prima la parte lineare
> (identita' esatta), poi con il flusso `N`. ### **Se con `N` la corrente locale NON
> esiste in forma chiusa, lo scrivi, e va a Luca come limite della promozione.»**

> ### ✅ **Questo file si committa PRIMA del codice.**

---

## 1. `E` COME SOMMA DI DENSITA' LOCALI — *e viene gratis*

**`E = Re <psi | W psi> + somma_k Lambda_k G(h_k / Lambda_k)`**

| | la densita' | dove vive |
|---|---|---|
| la parte **lineare** | **`e_h = Re[ conj(psi_h) . (W psi)_h ]`** *(prodotto scalare in `C^2`)* | **per ESTREMITA'** |
| la parte del **vuoto** | **`e_k = Lambda_k G(h_k / Lambda_k)`** | **per NODO** |

### ⭐ **E LA SOMMA DELLE DENSITA' E' `E`, ESATTAMENTE:** `Re<psi|W psi>` **e'** per
definizione `Re somma_h conj(psi_h).(W psi)_h`, e il termine del vuoto **e' gia' una somma
sui nodi**. ### ⛔ **Non c'e' nessun prodotto globale da cui partire:** il prodotto
globale **E'** la somma delle densita', non il contrario.

### ⚠ **E l'energia DI UN NODO si scrive attribuendogli le sue estremita':**

> **`E_k = somma_{h su k} e_h + Lambda_k G(h_k / Lambda_k)`**

### ⛔ **E QUESTA ATTRIBUZIONE E' UNA SCELTA, non un fatto** — e la dichiaro: `e_h` vive
**sull'estremita'**, e ogni estremita' **appartiene a un nodo solo**, quindi
l'attribuzione e' **l'unica possibile senza spezzare un'estremita'**.
### ✅ **Non c'e' arbitrio**, ma va detto che e' un passo.

---

## 2. LA CORRENTE DELLA PARTE LINEARE — **e la risposta e' UN CAMPO DELLA TABELLA**

### ⭐ **LA DOMANDA:** in un tick lineare, **che cosa attraversa fra due nodi?**

### ✅ **E LA TABELLA LO DICHIARA, nel campo `azione`.** Non e' una mia lettura del
codice: e' **un campo**, ed e' esattamente cio' che la regola *«una decisione che serve a
un programma vuole un CAMPO»* pretende.

| la legge | `azione` | che cosa attraversa |
|---|---|---|
| `CAMM-MONETA-SPIN` | **`estremita`** | ### **NIENTE**: agisce su **una** estremita' per volta, e **non legge il vicino** |
| `CAMM-GROVER` | **`nodo`** | ### **niente fra NODI**: mescola le estremita' **di uno stesso nodo** |
| `CAMM-SPOSTAMENTO` | **`arco`** | ### ⭐ **E' IL SOLO che attraversa**: `psi'[compagna(h)] = U[h] psi[h]` |
| `CAMM-GROVER-VUOTO` | **`nodo`** | niente fra nodi |
| `CAMM-SPOSTAMENTO-VUOTO` | **`arco`** | ### **attraversa** *(ma e' `phi`, e `phi` non entra nella parte lineare di `E`)* |

### ⛔ **QUINDI LA CORRENTE DELLA PARTE LINEARE E' UNICA E IN FORMA CHIUSA**, e l'unicita'
**non e' una scelta mia**: tutto il trasferimento fra nodi di un tick lineare
**passa per lo spostamento**, perche' **gli altri due pezzi non attraversano**.
### ⭐ **E sulla medesima linea: la corrente di un arco e' CIO' CHE LO SPOSTAMENTO PORTA
SU QUELL'ARCO** — un numero per arco, calcolabile.

### ⚠ **E IL SEGNO: la corrente ha un VERSO**, e il verso e' quello della numerazione
*(dall'estremita' `2k` a `2k+1`, cioe' da `ii[k]` a `jj[k]`)*. ### **Scambiare `ii` e `jj`
cambia il segno di `J`, e NON cambia il bilancio** — ed e' il caso che il collaudo
**deve far fallire**, perche' il mandato lo chiede: *«una corrente sbagliata, per esempio
con il verso di un arco invertito»*.

---

## 3. CON `N`: **LA CORRENTE LOCALE NON ESISTE IN FORMA CHIUSA** — *e il perche' e' preciso*

### ⛔ **PRIMA UN FATTO SULLO SCHEMA, e non e' un dettaglio: UN FLUSSO NON HA `azione`.**
Le chiavi di un `flusso` sono `generatore`, `ambito`, `parametri`, `esatto`, `simmetrie`,
`conserva` — ### **`azione` NON c'e'**. ### ⚠ **Quindi la tabella NON DICHIARA dove un
flusso agisce**, e per la corrente **quella e' proprio l'informazione che serve.**
### 📌 **Lo scrivo come buco dello schema**, e non lo riempio da solo.

### ✅ **DAL GENERATORE si vede comunque:** `Lambda*(h_int/Lambda - atan(h_int/Lambda))`
dipende **solo da grandezze DI NODO** *(`Lambda_k`, `h_k`)*, e il flusso le applica
**alle estremita' di quel nodo**. ### ⛔ **Quindi `N` NON ATTRAVERSA fra nodi: la sua
corrente e' ZERO.**

### ⛔ **MA `N` CAMBIA `E_k`.** Ed e' qui che si rompe:

| | |
|---|---|
| **il termine del vuoto NON cambia** | `P1` lo ha **misurato**: il flusso **conserva `h` e `Lambda`** *(`1.9` ulp)*, quindi `Lambda_k G(h_k/Lambda_k)` e' **invariato** |
| ### ⛔ **la parte lineare INVECE cambia** | `N` cambia `psi`, e `e_h = Re[conj(psi_h).(W psi)_h]` **dipende da `psi`**. ### E `N` **non commuta con `W`**: commuta con la **moneta** *(stesso asse `n`)*, ### **ma non col Grover ne' con lo spostamento** |

### ⛔ **E ALLORA IL BILANCIO LOCALE NON PUO' CHIUDERSI.** Se `N` **non trasferisce
niente** fra nodi *(corrente zero)* e **cambia `E_k`**, allora

> **`Delta E_k` da `N`** `= 0 + (qualcosa diverso da zero)` ### ⟹ **`Delta E_k` NON e' la
> somma di cio' che entra ed esce dai suoi archi.**

### ⚠ **E LA CONSEGUENZA E' PIU' GROSSA DI UNA FORMULA CHE MANCA:** il banco ha misurato
`E` conservata **GLOBALMENTE** sul tick intero. Globalmente conservata **piu'** nessun
trasferimento locale **piu'** cambiamenti locali non nulli ### ⟹ **i cambiamenti locali
si CANCELLANO FRA NODI LONTANI.**

### ⛔ **E UNA CANCELLAZIONE FRA NODI LONTANI E' ESATTAMENTE CIO' CHE `A14` CHIEDE DI
DICHIARARE** *(«conserva energia e carica LOCALMENTE? Se no, e' dichiarata fra le
violazioni note?»)* **e cio' che la carta vieta come MECCANISMO** *(nessuna scorciatoia
globale)*.

### 📌 **QUINDI, COME IL MANDATO PREVEDE: VA A LUCA COME LIMITE DELLA PROMOZIONE.**
### ⚠ **E lo scrivo come DERIVAZIONE, non come misura:** la misura e' **`M2`**, e
**questa derivazione e' la sua PREVISIONE.**

---

## 4. LE PREVISIONI PER `M2`, SCRITTE PRIMA DEI NUMERI

| | la previsione | che cosa vorrebbe dire se fosse falsa |
|---|---|---|
| `1` | **la parte lineare chiude il bilancio locale ESATTAMENTE** *(arrotondamento)*: `Delta E_k = somma dei flussi J` | che **lo spostamento non e' il solo pezzo che attraversa** — cioe' che **il campo `azione` dice il falso** |
| `2` | **con `N` acceso il residuo NON e' arrotondamento**, ed e' **dell'ordine di `dtau^2`** per nodo | che `N` **commuta** con `W` piu' di quanto credo, e allora il limite **non c'e'** |
| `3` | **i residui per nodo SOMMANO a (quasi) zero** sul grafo intero | che `E` **non e' conservata nemmeno globalmente**, e allora **la promozione cade del tutto** e non e' un limite: e' un errore |

### ⛔ **E IL CASO CHE DEVE FALLIRE, che il mandato chiede:** una corrente **col verso di un
arco invertito** ### **deve rompere il bilancio della parte lineare.** ### ⚠ **Se non lo
rompesse, vorrebbe dire che il bilancio passa anche con una corrente sbagliata** — cioe'
che **non sto misurando il bilancio.**

---

## 5. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **energia e carica LOCALMENTE**? | ### ⛔ **E' LA DOMANDA DI QUESTO PEZZO, e la risposta e' DIVISA:** **si'** per la parte lineare *(un'identita', e il bilancio chiude per costruzione)*; ### **NO per `N`**, e ### **lo dichiaro fra le violazioni note** invece di curarlo |
| **2** | **quale dei tre gradini**? | ### **(a) robusto al rumore numerico** per la parte lineare *(e' un'identita')*. ### ⚠ **Per `N` NON arrivo a nessun gradino: ho una derivazione e NON ancora una misura** — e' `M2` |
| **3** | **aggiunge un numero o una legge**? | ### ✅ **Nessuno dei due.** `J` **non e' una legge**: e' **un osservatore** calcolato dallo stato e dallo spostamento. ### **E non porta costanti** |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### ⚠ **IL SEGNO SI':** `J` **ha un verso**, e il verso e' quello della numerazione degli archi. ### **Non e' il segno dell'accoppiamento della carta** *(non c'e' nessun `EM <-> curvatura` qui)*, ma e' **un segno**, e sbagliarlo **invertirebbe il bilancio** |
| **5** | **emergente o imposto**? | ### ⭐ **EMERGENTE, e questo e' il punto piu' bello del pezzo:** l'unicita' della corrente **non la impongo io** — ### **viene dal campo `azione` della tabella**, che dice quali pezzi attraversano. ### **Se un giorno una legge nuova avesse `azione: arco`, la corrente cambierebbe DA SOLA** |

---

## 6. TODO DEL NEXT STEP

1. **`E` come somma di densita' locali** in `primo_ordine/energia.py`, con le **due**
   densita' *(estremita' e nodo)* e **la somma per nodo**.
2. **`J` sugli archi**, dalla sola parte dello **spostamento**.
3. il **collaudo**: il bilancio **chiude al bit** per la parte lineare, col **caso che
   deve fallire** *(verso invertito)*; e **misura** il residuo con `N` acceso.
4. la **domanda per Luca** sul **limite della promozione**, e il **buco dello schema**
   *(un flusso non dichiara dove agisce)*.

---

## ⛔ ANNOTAZIONE DEL `2026-10-12`, DOPO LA MISURA — **la previsione `1` E' FALSA**

> ### ⚠ **Il par.`8` dice che un ragionamento che si rivela sbagliato NON SI
> RISCRIVE: si ANNOTA.** ### **Quindi quello che sta sopra resta**, e qui c'e' che cosa
> la misura ha detto.

### ✅ **CHE COSA REGGE, e regge esattamente:**

| | il fatto | la misura |
|---|---|---|
| `a` | **`E` e' la somma delle densita' locali**, e non un'approssimazione della forma globale | scarto **`1.8e-15`** |
| `b` | **il PRIMO termine e' conservato dal tick lineare**, per l'identita' `W^dag W W = W` | **`0.6` ulp** |
| `c` | **i cambiamenti per nodo sommano a zero**, quindi ### **UNA corrente ESISTE** | `0.6` ulp |

### ⛔ **CHE COSA E' FALSO: la previsione `1`.** Avevo scritto *«la parte lineare
chiude il bilancio locale ESATTAMENTE»*. ### **NON CHIUDE**, e non chiude **di tanto**:

| | |
|---|---|
| il residuo con la corrente derivata | **`1.342e+01`** su scala `4.93` |
| il cambiamento **senza nessuna corrente** | `7.768e+00` |
| ### ⛔ **quindi** | ### **la corrente NON TOGLIE niente: AGGIUNGE.** E' **peggio** di non averla |

### ⭐ **E L'ERRORE DELLA DERIVAZIONE E' PRECISO, e non e' un conto sbagliato:**
l'argomento del campo `azione` *(solo `arco` attraversa)* e' **vero**, ma dice
**dove si muove `psi`**. ### ⛔ **E `e_h = Re[conj(psi_h) . (W psi)_h]` NON E' UNA
FUNZIONE DI `psi` A UN TEMPO: e' una CORRELAZIONE FRA DUE TEMPI** — `psi` e `W psi`.
### **Quindi non e' una carica che si trasporta, e l'argomento non si trasferisce.**

### ✅ **E LA PROVA E' DIRETTA, non dedotta:** `e_h` cambia su **TUTTI** i nodi
*(`16` su `16`)*, anche su quelli i cui archi **non portano niente**. ### **Una carica
trasportata non si comporta cosi'.**

### ⚠ **E C'E' UNA SECONDA COSA CHE NON AVEVO VISTO:** `E` **non e' conservata
dal tick LINEARE**. Il primo termine si', ma ### **il termine del vuoto cambia di
`2.633`**, perche' il tick lineare **cambia `h_k`** e `Lambda_k G(h_k/Lambda_k)` dipende
da `h_k`. ### ⛔ **Quindi la conservazione di `E` e' una proprieta' della
COMPOSIZIONE INTERA**, non della somma di due pezzi conservati.

### 📌 **E sul tick intero la deriva c'e' e scende:** a tempo totale fisso
`T = 20`, l'ultimo dimezzamento di `dtau` *(da `0.1` a `0.05`)* da' **rapporto `4.20`**
— ### **la firma dell'esponente `2`, cioe' dello splitting di Strang.** ### ⚠ **E
ai passi grandi il rapporto e' erratico** *(`0.39`, `2.48`)*: ### **fuori dal regime
asintotico**, e va detto invece di citare solo il numero buono.

---

## 9. ⭐ ANNOTAZIONE DEL 2026-10-13 — **LA CONCLUSIONE DI QUESTO PEZZO ERA TROPPO LARGA**

> **Mandato di Luca, 2026-10-13, punto `1`:** *«Cio' che hai dimostrato e' piu' stretto:
> **NON FUNZIONA LA TUA CANDIDATA**. L'esistenza di una corrente LOCALE e' un'altra cosa,
> ed e' **VERA** per la parte lineare.»*

### ⛔ **NON RISCRIVO NIENTE DI SOPRA:** il paragrafo `8` di `CLAUDE.md` dice che un
ragionamento rivelato sbagliato ### **si ANNOTA, non si riscrive** — e il motivo e' che
### **la riscrittura cancella la prova di come ci sono arrivato.**

| | che cosa avevo misurato *(e resta VERO)* | che cosa avevo concluso |
|---|---|---|
| ✅ | la candidata da' residuo **`1.342e+01`** su scala `4.93`, peggio che senza corrente | — |
| ✅ | `e_h` e' una **correlazione fra due tempi**, e cambia su `16` nodi su `16` | — |
| ### ⛔ **FALSO** | — | *«la corrente locale non esiste nemmeno per la parte lineare»* |
| ### ⛔ **FALSO** | — | *«la corrente e' UNICA, e l'unicita' viene da un campo della tabella»* |

### ⚠ **E IL SECONDO FATTO NON IMPLICA LA TERZA RIGA:** che `e_h` sia una correlazione fra
due tempi e' vero, ma ### **non impedisce la localita'.**

### ⛔ **E LA NON UNICITA' NON E' UN DIFETTO**, e qui avevo sbagliato una seconda volta,
nel verso opposto: prima avevo **rivendicato** l'unicita' *(`af8db57`)*, poi l'avevo
trattata come **un ostacolo**. ### ✅ **E' la stessa liberta' della corrente d'energia nel
continuo, definita a meno di un rotore:** una corrente e' fisicamente locale se e'
**funzione LOCALE dello stato** e **chiude la continuita'**. ### **L'unicita' non serve.**

### ⭐ **CHE COSA C'E' ADESSO, misurato** *(`doc/REFERTO_corrente_locale.md`)*:

| | il fatto | il numero |
|---|---|---|
| `a` | la variazione d'energia di una regione e' **un termine di bordo** | perturbando **dentro** `R` a distanza `>= 2`: `somma_R Delta e` cambia di **`2.665e-15`**, mentre `Delta e` **per nodo** cambia fino a **`6.183`** |
| `a-bis` | il **controllo positivo** | perturbando **al bordo**: **`7.144e-01`**, cioe' `O(1)` |
| `b` | una corrente locale **esiste, ed e' costruita** | la continuita' chiude a **`2.9`–`70.4` ulp** su `6` scene |
| `b-bis` | la **portata**, MISURATA | **`3` archi**, e **non cresce col grafo**: a grado `4` i diametri `4`, `5`, `6` danno **tutti `3`** |

### ⚠ **E LA MIA PREVISIONE SULLA PORTATA ERA `<= 4`:** il numero vero e' **`3`**.
### **La previsione era una stima, e l'ho scritta come tale** — questo e' il caso in cui
l'avere dichiarato *«non la so»* ha fatto la differenza fra una stima e una pretesa.

### ⛔ **E RITIRO LA RACCOMANDAZIONE** che avevo scritto in questo file: *«cambiare la
grandezza promossa a una densita' funzione dello stato a un tempo»*. ### **Non era
motivata**, e il mandato me la fa ritirare. ### ✅ **La ritiro.**

### 📌 **La costruzione, il collaudo e il referto:** `primo_ordine/corrente.py`,
`primo_ordine/_collauda_corrente.py`, `doc/REFERTO_corrente_locale.md`; e il ragionamento
preliminare sta in `doc/TASK_HISTORY/2026-10-13_corrente_locale_esiste.md`.
