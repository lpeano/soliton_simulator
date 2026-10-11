# IL COMPLETAMENTO DEL LEGAME — **SCENE `3D` GRANDI, MISURA IN ARCHI ASSOLUTI, E `M2`**

> ### ⛔ **QUESTO FILE SI COMMITTA *PRIMA* DELLE MISURE** *(par.8)*: così l'ordine è
> **verificabile da git** invece che asserito da me. ### **Le soglie e le previsioni stanno
> qui, e non si riscrivono quando si rivelano sbagliate: si ANNOTANO.**

**Mandato:** `[[LEGAME-SCENE-GRANDI]]`, registrato in `53b2664`, voce ⑪ di
`doc/CODA_2026-10-09.md`. ### **Nasce dai TRE LIMITI che avevo dichiarato io** nel referto
del legame *(`3ef7c8e`)* — che è il modo in cui un limite dichiarato serve a qualcosa.

**Posizione in coda:** **DOPO** `[[ISOTROPIA-LOCALE]]` *(chiuso in `dae2892`)*, **PRIMA**
del simulatore.

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo prima di guardare*

### ⭐ **CHE COSA SO GIÀ, dai due referti che ho in casa**

| | il fatto misurato | da dove |
|---|---|---|
| `1` | il `+D` col segno diretto **lega in `1D`**, e l'effetto **CRESCE** con la taglia | `doc/REFERTO_legame.md` |
| `2` | in `3D` lo stesso effetto **cala con la taglia fino a sparire** | *idem* |
| `3` | sulle scene `3D` piccole il fronte **RIEMPIE il grafo** *(raggio finale `11` su diametro `18` a `L = 12`)* | *idem* |
| `4` | il misurando *«frazione entro un arco contro fondo uniforme»* dipende dalla taglia **attraverso il DENOMINATORE** | *idem* |
| `5` | il selettore prescritto da `M2` **OSCILLA a `O(1)`**, quello a massima sovrapposizione converge a `1.9e-13` | *idem* |
| `6` | la velocità del fronte è **`0.6193` archi/tick**, misurata | referto `v4` |
| `7` | a `n = 26000` **tutte e quattro** le famiglie di scena `3D` hanno `\|d_s - 3\| <= 0.109` | `doc/REFERTO_isotropia_locale.md` |
| `8` | i punti **respinti** hanno irregolarità `0.1584` contro `0.2719`, pavimento `0.0897` contro `0.1700`, e **meno archi** | *idem* |

### ⛔ **E QUINDI IL DUBBIO CENTRALE, detto prima di misurare:** il *«in `3D` l'effetto
cala con la taglia»* del referto del legame è stato misurato **su scene dove il fronte
riempiva il grafo**. ### **Quindi non so distinguere queste due spiegazioni:**

| | la spiegazione | che cosa predirebbe a taglia grande |
|---|---|---|
| `(a)` | **È LA DIMENSIONE**: in `3D` il segno non lega, e basta | l'effetto resta **nullo** anche con il fronte lontano dal bordo |
| `(b)` | **ERA TAGLIA FINITA**: il misurando era dominato dal grafo pieno | l'effetto **ricompare** quando il fronte non tocca il bordo |

### ⚠ **E HO GIÀ SBAGLIATO UNA VOLTA IN QUESTA STESSA DIREZIONE, quindi lo dico adesso:**
nel referto dell'isotropia ho presentato un compromesso che era **taglia finita**, e Luca
l'ha visto prima di me. ### **Non è una ragione per aspettarmi `(b)`: è una ragione per
NON escluderla come ho fatto l'altra volta.**

### **LA MIA PREVISIONE, e sono onesto sul perché è debole:** credo `(a)`, perché il
meccanismo del `+D` in `1D` è un'**interferenza fra due sole direzioni di uscita**, e in
`3D` con grado `6..34` le direzioni che non interferiscono sono molte di più. ### ⛔ **Ma
questo è un argomento di plausibilità, non un conto** — e non ho un conto.

### **CHE COSA NON SO**

1. **se `M2` converga su una scena `3D` grande**: il selettore a massima sovrapposizione
   converge sull'anello, e `202119` archi sono un'altra cosa;
2. **se la quasi-energia di uno stato autoconsistente cada FUORI dallo spettro lineare**:
   non l'ho mai misurato per nessuna scena;
3. **quale sia la soglia di <<cresce più lentamente del lineare>>** che non sia arbitraria
   — e questo è il punto dove rischio una manopola *(`A1`)*;
4. **se il raggio in archi assoluti smetta di crescere PRIMA del bordo**: è esattamente la
   cosa che la misura vecchia non poteva vedere.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — **le soglie si fissano QUI**

### ⛔ **LA REGOLA DI AMMISSIBILITÀ DI UNA SCENA** *(`C1`)*

> ### **Una taglia è ammissibile solo se `0.6193 · t_oss < diametro / 2`.** Il numero
> `0.6193` è **misurato**, non scelto, e il `/2` è la condizione del mandato
> *(«il fronte non arrivi a METÀ del diametro»)*.

| | la soglia | come si decide |
|---|---|---|
| `c1` | **la scena è ammissibile?** | `0.6193 · t_oss < diametro/2`, col **diametro dichiarato** e il campo che dice se è **esatto o campionato** |
| `c1-bis` | **e il costo si dichiara** | secondi per tick, misurati, per ogni scena — ### **una taglia che non si paga si DICHIARA e si ferma alla precedente**, senza ridurre la precisione |

### ⭐ **IL MISURANDO IN ARCHI ASSOLUTI** *(`C2`)* — **e le soglie**

| | la soglia | come si decide | la mia previsione |
|---|---|---|---|
| `c2` | **il raggio in archi SMETTE di crescere?** | il raggio che contiene il `90%` della norma, contro `t`, adattato a una retta: **pendenza compatibile con `0` entro `3 sigma`** | ### **NO**: cresce come il lineare |
| `c2-bis` | **oppure cresce PIÙ LENTAMENTE del lineare?** | il rapporto fra le due pendenze, **sotto `1` di più di `3 sigma`** — ### ⛔ **e NON metto una soglia numerica sul rapporto**, perché sarebbe una manopola *(`A1`)*: la soglia è ### **la significatività**, non un valore scelto | ### **NO**: rapporto compatibile con `1` |
| `c2-ter` | **la frazione entro pochi archi resta SOPRA il lineare?** | frazione entro `r = 1, 2, 3` archi, contro il lineare **alla STESSA taglia**, con l'effetto e il `sigma` **accanto** | ### **NO**, o un effetto sotto l'`1%` |
| `c2-quater` | **e su DUE taglie che non toccano il bordo** | il verdetto `RESTA CONCENTRATO` si dà **solo se `c2` o `c2-bis` E `c2-ter` passano su DUE taglie ammissibili** | ### **nessun segno lega in `3D`** |

### ⛔ **E LA MISURA VECCHIA SI TIENE ACCANTO**, come il mandato chiede: serve a vedere
**se le due misure si contraddicono**, e se si contraddicono ### **la vecchia era il
difetto**, perché il suo denominatore dipende dalla taglia.

### ⭐ **`M2`: GLI STATI AUTOCONSISTENTI** *(`C3`)* — **e le soglie**

> ### ⛔ **IL SELETTORE È DICHIARATO, E IL MOTIVO È MISURATO:** quello prescritto dal
> mandato *(«il più localizzato»)* ### **OSCILLA a `O(1)`**; quello a **massima
> sovrapposizione** converge a `1.9e-13` *(già nel referto del legame)*. ### **Si usa il
> secondo, e si dice perché.**

| | la soglia | come si decide | la mia previsione |
|---|---|---|---|
| `c3` | **l'iterazione CONVERGE?** | il residuo scende sotto `1e-10`, altrimenti ### **`FERMO`, non un verdetto** | ### **sì sull'anello**, ### **non lo so** sulle `3D` grandi |
| `c3-bis` | **la quasi-energia cade FUORI dallo spettro lineare?** | contro lo spettro di `M0` per ### **QUELLA scena e QUEL `eps`**, con le spigole di `±1` escluse | ### **DENTRO** — cioè ### **non è uno stato legato** |
| `c3-ter` | **il raggio dello stato smette di crescere?** | la **regola sul raggio** applicata allo **stato STAZIONARIO** *(non al grumo iniziale: lo dice la correzione di Luca)* | ### **cresce** |
| `c3-quater` | **la prova dinamica lo tiene?** | si fa evolvere col **passo vero** e si guarda se resta | ### **si disperde** |
| `c3-quinquies` | **la `C` sul coniugato** | residuo **relativo** sotto `64 eps` | ### **regge**, come per `+N` e `-N` |
| `c3-sexies` | **<<legato>> solo su DUE taglie** | un verdetto su una taglia sola è ### **una retta per un punto** *(`TAGLIA-FINITA`)* | ### **nessun legato** |

### ⛔ **E LE DUE COSE CHE MI FERMANO**

1. ### **`c3` che non converge su nessuna scena `3D`**: allora `M2` in `3D` è **`FERMO`**,
   e lo scrivo — ### **non riporto un verdetto da un'iterazione che oscilla**;
2. ### **una contraddizione fra la misura in archi e quella vecchia che NON si spiega con
   la taglia**: allora una delle due è sbagliata e ### **mi fermo a capire quale**, invece
   di scegliere quella che mi piace.

### ⭐ **LE REGOLE DI FORMA, che vengono dai miei errori e che il mandato ripete**

* **effetto e `sigma` SEMPRE accanto** — perché ho già riportato `8` casi su `39` con
  significatività e **senza effetto** *(il peggiore `+0.016%` a `3.55 sigma`)*;
* **i casi si ordinano per EFFETTO**, non per `sigma`;
* **ogni soglia relativa alla scala della grandezza**, non assoluta — è successo **tre
  volte**;
* **nessuna soglia nuova tarata a mano**: dove serve un numero, la soglia è la
  **significatività** *(`A1`)*.

---

---

## 3. LA STELLA POLARE — **le cinque risposte, PRIMA delle misure** *(`L-STELLA`)*

| | la domanda | la risposta |
|---|---|---|
| `1` | **`A14`: conserva energia e carica LOCALMENTE?** | ### **Non cambia nulla di cio' che si conserva**, perche' ### **questo mandato non accende niente**: `C1` e `C2` sono ### **MISURANDI** *(il raggio in archi, la frazione entro `r`)*, e `C3` cerca ### **stati di una dinamica che c'e' gia'**. ### ⚠ **L'unica cosa che potrebbe rompersi e' la `C` sul coniugato di uno stato di `M2`**, e ### **e' una soglia** *(`c3-quinquies`)* |
| `2` | **a quale dei TRE GRADINI arriva?** | ### **`(a)` robusto: SI'** *(ogni verdetto chiede ### **due taglie**, e le soglie sono significativita' e non valori)*. ### **`(b)` regge togliendo la legge pratica: E' IL CONTROLLO LINEARE** *(ogni misura ha il lineare ### **alla STESSA taglia** accanto)*. ### ⛔ **`(c)` coincide con un limite noto: SI', e il limite e' il mio `1D`** — il `+D` lega in `1D` con effetto che CRESCE, quindi ### **se il misurando nuovo non ritrovasse quello, il misurando sarebbe rotto** |
| `3` | **aggiunge un numero o una legge?** | ### ⭐ **NESSUNO DEI DUE.** Il misurando in archi assoluti ### **toglie un denominatore che dipendeva dalla taglia** *(il <<fondo uniforme>>)* e lo sostituisce con ### **un conteggio di archi**, che non ha parametri. ### ⛔ **E dove servirebbe un numero** *(<<quanto piu' lentamente del lineare?>>)* ### **non lo metto: la soglia e' la SIGNIFICATIVITA'** *(`A1`)* |
| `4` | **tocca `rho`, `c_s` o il SEGNO?** | ### **Nessuno dei tre:** le quattro candidate `+N`, `-N`, `+D`, `-D` sono ### **quelle di `M1`, gia' misurate**, e qui si cambia ### **soltanto la SCENA e il MISURANDO.** ### ⭐ **Ed e' il punto del mandato:** se un verdetto cambia cambiando ### **solo la taglia**, allora il verdetto vecchio ### **parlava della taglia** |
| `5` | **emergente o imposto?** | ### ⛔ **E' LA DOMANDA INTERA DI `C3`.** Uno stato autoconsistente che ### **cade DENTRO lo spettro lineare** non e' uno stato legato: e' ### **una sovrapposizione di onde che si disperdera'**, e la ### **prova dinamica col passo vero** e' la guardia. ### ✅ **E il controllo che PUO' fallire e' il LINEARE alla stessa taglia:** se il lineare desse lo stesso raggio e la stessa frazione, ### **la candidata non starebbe facendo niente** |

## 4. TODO DEL NEXT STEP

| | il passo | cosa decide |
|---|---|---|
| `1` | committare e pushare **questo file** | l'ordine verificabile da git |
| `2` | `_letture_legame_grandi.py`: le **scene ammissibili** e il loro costo | `C1`, e quali taglie esistono |
| `3` | il misurando **in archi assoluti** *(raggio al `50%` e al `90%`, frazione entro `1, 2, 3`)*, col **lineare alla stessa taglia** | `C2` |
| `4` | `M2` col selettore a **massima sovrapposizione** sulle tre famiglie, per i **quattro segni** | `C3` |
| `5` | i **bracci** nel banco del legame: la regola di ammissibilità **scatta**, e un caso che **DEVE** fallire | il collaudo |
| `6` | la **sezione nuova** in `doc/REFERTO_legame.md` *(il resto NON si tocca)*, le voci, e le **due domande** aggiornate **per famiglia e per taglia** | la registrazione |

### ⛔ **E LA COSA CHE NON FARÒ: SCEGLIERE LA SCENA PRINCIPALE.** Le misure dell'isotropia
indicano i **punti respinti** su ogni asse tranne uno, ma ### **la scelta è di Luca**
*(`[[DOMANDA-QUALE-SCENA-3D-PRINCIPALE]]`)*. ### **Quindi `C1` gira su ENTRAMBE le
varianti geometriche**, uniformi e respinti, e la decisione **resta aperta**.

---

## ⭐ **ANNOTAZIONE: LA SCENA `3D` PRINCIPALE E' DECISA, ED E' LA `(ii)`** *(decisione di Luca, `2026-10-11`, arrivata a CORSA IN VOLO — quindi si **ANNOTA**)*

### ✅ **E LA CORSA IN VOLO NON SI TOCCA, NE' HA BISOGNO DI ESSERE RIFATTA:** `C1` era gia' scritto per girare su ### **ENTRAMBE le varianti geometriche** *(uniformi e respinti, a `n = 4000`, `10000`, `26000`)* piu' il ### **cubico `L = 20, 30, 40`** e l'### **anello come limite noto `1D`**. ### **Quindi la scena decisa e' GIA' DENTRO la corsa**, e la decisione ### **non obbliga a rifare niente** — cambia soltanto ### **quale colonna del referto e' la PRINCIPALE e quale il CONTROLLO.**

### ⭐ **E IL MOTIVO PER CUI `C1` girava su due varianti era PROPRIO QUESTO:** nel paragrafo `2` di questo file avevo scritto *<<la scelta e' di Luca, quindi `C1` gira su ENTRAMBE le varianti geometriche e la decisione resta aperta>>*. ### **Non decidere al posto suo e' costato una colonna in piu' e ha risparmiato una corsa intera.**

| | che cosa cambia nel referto |
|---|---|
| `1` | la ### **`(ii)` e' la scena `3D` PRINCIPALE** alle taglie grandi |
| `2` | il ### **cubico periodico** resta il ### **CONTROLLO dichiarato** *(e' `3D` ma **non isotropo**: l'anisotropia del profilo medio e' sistematica a ogni `t`, `~6` volte il rumore)* |
| `3` | l'### **anello** e il ### **grafo casuale** restano controlli di ### **DIMENSIONE** |
| `4` | la ### **`(i)` uniformi resta come colonna**, perche' e' la scena su cui il referto vecchio ha misurato — ### **togliere la colonna renderebbe il confronto col referto vecchio impossibile** |

### 📌 **E LA VOCE DELLA DECISIONE E' `[[SCENA-3D-PRINCIPALE]]`**, con i numeri e ### **la taglia accanto a ciascuno.**

