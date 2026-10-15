# `L2` — SECONDO PEZZO: **il verso sulla PARTE PARI, e l'esponente**

> **Mandato di Luca del 2026-10-15.** Ultimo commit verificato dal guardiano: `38853a9`.
> ### ⛔ **Nessuna legge nuova, la saturazione non si tocca.**
>
> ### **E si scrive prima del codice** *(§8)*.

---

## 0. ⛔⛔ **DUE ERRORI NEL PROTOCOLLO DEL PRIMO PEZZO, e sono del guardiano**

### ⚠ **Li registro con la stessa cura con cui registro i miei**, perche' il risultato del
primo pezzo *(«nessun verdetto»)* **dipendeva da entrambi.**

### ⛔ **(a) IL CASO CHE DOVEVA FALLIRE PRESUPPONEVA UNA RISPOSTA LINEARE IN `beta`.**
Il criterio diceva: *«`beta` rovesciato deve rovesciare `dLambda`»*. ### **Ma quello vale
solo se la risposta e' LINEARE.** La risposta misurata e' ### **PARI** *(`520bfbc`:
`dispari/pari = 1.6e-13` a `dtau = 1`)*, e

> ### ⭐⭐ **UNA RISPOSTA PARI HA UN VERSO.** Non e' ambigua: e' **la stessa** per le due
> elicita', cioe' ### **indipendente dall'orientamento dello spin** — ed e' **proprio
> cio' che il principio di equivalenza richiede.**

### ✅ **Quindi il precondizionamento <<canale dispari presente>> SI TOGLIE come criterio
del verso.** ### ⚠ **E la conseguenza su di me e' che il mio <<nessun verdetto>> era
TROPPO PRUDENTE su quel punto:** avevo trattato la parita' come **un'assenza di verso**,
mentre e' ### **un verso che non dipende dall'elicita'.**

### ⛔ **(b) IL GRUMO ISOTROPO NON E' UN CONTROLLO NULLO** — e questo l'ho misurato io
*(`3dccfc5`: `h(0) = 0` ma `max|h(t)| = 2.1617`, **l'elicita' nasce**)*.
### ✅ **Il controllo nullo e' `beta = 0`, che da' `dLambda = 0` ESATTO: resta, ed e'
l'UNICO.**

### 📌 **E RILETTI COSI', I NUMERI DI `38853a9` A `dtau = 1` DICONO UNA COSA PRECISA:**
parte pari **POSITIVA** sul grumo e **crescente** *(anello `0` da `+0.043` a `+0.105`)*,
**negativa all'anello `3`**, e **uguale per le due elicita'** *(rapporto `1.10`–`1.24`)*.

> ### ⛔ **Cioe': IL VUOTO SI ACCUMULA SULLA MATERIA — verso OPPOSTO alla decisione di
> Luca.**

### ⚠ **MA `dtau = 1` E' UN CASO SPECIALE** *(il hop del vuoto e' una **permutazione
pura**)*, quindi ### **quella lettura NON si puo' usare come conclusione:** serve il
punto 1, a `dtau` piu' piccoli e con le barre d'errore.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### ⭐ **CIO' CHE CREDO, e viene da misure gia' fatte**

1. **`E` sul grumo sara' POSITIVA anche a `dtau < 1`.** Il motivo non e' un'intuizione: a
   `dtau = 1` e' positiva e crescente, e il meccanismo *(il modulo di `beta`, non il suo
   segno)* ### **non cambia natura abbassando `dtau`** — cambia solo l'angolo degli
   operatori.
2. **`O` sara' compatibile con zero come MEDIA**, pur essendo grande come **ampiezza** a
   `dtau = 0.5` *(dove `dispari/pari = 2.99`)*: i segni alternavano fra le finestre.
   ### **Se e' cosi', la parte dispari e' OSCILLAZIONE SENZA SPOSTAMENTO NETTO.**
3. **L'esponente sara' `~6` per `x` piccolo.** `beta ~ -(2/3)x^3` e `E` e' quadratica in
   `beta` ⟹ `E ~ x^6`.

### ⛔ **E QUESTA TERZA COSA, SE SI CONFERMA, E' LA PIU' PESANTE DEL PEZZO**

> ### ⚠⚠ **Una <<gravita'>> che va come `x^6` NON ESISTE PER POCA MATERIA.** La gravita'
> newtoniana e' **lineare nella massa**; `x^6` vuol dire che ### **dimezzare la materia
> divide l'effetto per `64`.**

### 📌 **E lo scrivo PRIMA di misurare, perche' se esce `6` non voglio poterlo chiamare
<<previsto>> senza averlo scritto, e se esce `1` devo accorgermi che la mia derivazione di
`beta` era sbagliata.**

### ⛔ **CIO' CHE NON SO**

1. **se a `dtau = 0.25` il segno resta POSITIVO.** A `dtau = 0.5` nel primo pezzo tutto
   oscillava: ### **la media con la barra d'errore e' una misura che non ho ancora fatto.**
2. **quanto costano `2000` tick.** Lo misuro e lo **dichiaro**; se il budget non ci sta,
   ### **dichiaro il massimo che ci sta** invece di tagliare in silenzio.
3. **se l'esponente e' lo stesso ai due `dtau`.** Se non lo e', ### **l'esponente non e'
   una proprieta' della legge** ma della scena, e va detto.

---

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, cosa mi FERMA*

| | il passo | **che cosa decide** | **cosa mi FERMA** |
|---|---|---|---|
| `1` | **`primo_ordine/_misura_pari_l2.py`**, file NUOVO *(il vecchio tiene il suo referto)*: `E` e `O` per finestre, sul grumo e per anelli | il verso | — |
| `2` | **il controllo nullo `beta = 0`**, che resta **l'unico** | che la misura non guardi rumore | `dLambda != 0` con `beta = 0` → la misura e' rotta |
| `3` | **corse LUNGHE** *(`>= 2000` tick, `>= 10` finestre)*, e il costo **dichiarato** | la barra d'errore | il budget che non ci sta → **dichiaro il massimo**, non taglio in silenzio |
| `4` | **il VERDETTO**: segno della media di `E` sul grumo, con `|media| > 3` barre | il verso | `E > 0` → **verso OPPOSTO alla decisione: STOP e riporto.** ### **Nessuna legge per raddrizzarlo** |
| `5` | **la media di `O`** con la sua barra | se la parte dispari e' **solo oscillazione** | — |
| `6` | **l'esponente** in `x = 0.1 .. 2`, pendenza in log–log con l'incertezza | **se la gravita' esiste per poca materia** | un esponente che **cambia col `dtau`** → non e' della legge, e lo dico |

### ⛔ **LE TRE COSE CHE NON FACCIO**
1. **non tocco la saturazione** *(il mandato lo dice, e la strada `A` e' derivata)*;
2. **non aggiungo nessuna legge** se il verso esce opposto: **riporto e mi fermo**;
3. **non metto le corse lunghe nel `pre-commit`**: sono **misure dichiarate**, e il budget
   di `500` s resta.

---

## 3. LA STELLA POLARE — **cinque risposte, PRIMA del codice**

| | la risposta |
|---|---|
| **1. `A14`, conserva localmente?** | **Il vuoto TOTALE si conserva** *(misurato `1.5e-13`)*, e **localmente no, ed e' il punto**: `Lambda_k` cambia. ### ⭐ **E la somma di `E` su TUTTI i nodi deve essere ZERO** se il vuoto si sposta e non nasce: ### **lo misuro, ed e' un controllo che nel primo pezzo non c'era.** |
| **2. a quale GRADINO arriva?** | **`(a)`**, e per la prima volta con **una barra d'errore** sul numero che conta. ### ⛔ **NON `(c)`:** e l'esponente serve **proprio** a dire **quanto lontano** si e' da un limite noto *(la gravita' newtoniana e' lineare nella massa, `x^6` non lo e')*. |
| **3. aggiunge un numero o una legge?** | ### ✅ **NIENTE.** `0` leggi, `0` parametri: `E` e `O` sono **due combinazioni** di misure, e la soglia `3` barre d'errore e' **il criterio di Luca**, scritto nel mandato. |
| **4. tocca `rho`, `c_s` o il SEGNO?** | **Tocca `Lambda`** *(e quindi `cs` indirettamente)*, e **il SEGNO e' esattamente l'oggetto della misura.** ### ⛔ **`cs` NON e' ancora accoppiato a `Lambda`.** |
| **5. emergente o imposto?** | ### ⭐⭐ **Il verso deve EMERGERE, e qui c'e' la cosa nuova: la PARITA' in `beta` e' essa stessa un fatto emergente, e porta con se' l'INDIPENDENZA DALL'ELICITA'** — cioe' **un pezzo del principio di equivalenza** *(lo stesso effetto per spin opposti)*, ### **che nessuna riga ha imposto.** ### ⚠ **E l'esponente e' il rovescio della medaglia: se e' `6`, la stessa legge che rispetta l'equivalenza sullo SPIN la viola sulla MASSA**, perche' non e' lineare. |

---

## 4. TODO DEL NEXT STEP

1. `primo_ordine/_misura_pari_l2.py`: `E` e `O` per finestre, corse lunghe col costo
   **dichiarato**, il controllo `beta = 0`, la somma di `E` su tutti i nodi, il verdetto a
   `3` barre, e **l'esponente** con la sua incertezza.
2. Il referto **nuovo** in `doc/referti_l2/`, **accanto** al vecchio.
3. `RIPRESA` e mappa: la correzione dei due errori del protocollo, il verso, l'esponente.
   Poi **STOP**: il verso e l'esponente vanno a Luca.
