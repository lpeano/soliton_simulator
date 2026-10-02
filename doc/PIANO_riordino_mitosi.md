# 🧭 **IL PIANO: IL RIORDINO DELLA MITOSI** *(`T3`, passo 2 — 2026-10-01)*

> ### ⚠ **QUESTO E' UN PIANO: NESSUNA RIGA DI CODICE DEL SIMULATORE.** Blob **`62d67675`**.
> **La base e' il REGISTRO DELLE GRANDEZZE**, e la storia e' in `doc/MITOSI_storia.md` *(`e97fc073`)*.
> ### **STOP dopo questo commit**, come da mandato.

**Il numero da cui parte tutto, misurato dall'AST:** `mitosi` e' **549 righe**, scrive **56
attributi** in **79 punti**, e delle **30** grandezze del registro ### **ne scrive 16 qui, 13 in due
funzioni di servizio, e 1 per mutazione in posto.**

---

# **(a) DECISIONE: chi decide la divisione, quando, e cosa legge**

## Com'e' oggi

| | |
|---|---|
| **dove** | dentro `mitosi`, nelle prime ~270 righe |
| **la soglia** | `soglia0 = PHI_CRIT + twist_max` = ### **`3π`** *(`2π` quanto + `π` twist dipolare massimo)*, **oppure `PHI_CRIT`** con `FASE_2PI` |
| **la modulazione** | `soglia = soglia0 * (1 − 0.3·tanh(grad_r))` — ### **il `0.3` e' SCELTO** |
| **cosa legge** | `tw` *(avvolgimento)* · `_r_nodo_mitosi()` *(tempo proprio)* · `_rho_sorgente()` *(densita')* · `peq` · `massa_critica_collasso()` · `_deg` · `pos` *(per lo Schwinger)* |
| **i filtri a valle** | ~~`MITOSI_2LAM` *(OFF)*~~ · `MITMAX` *(0)* · `MITOSI_DIR` *(0.0)* · la **campana** di criticita' ### ⛔ **ANNOTAZIONE DEL 2026-10-02 (`MITOSI-2LAM-ACCESO`): `MITOSI_2LAM` e' `OFF` solo come DEFAULT DI MODULO** *(`:441`)*. ### **Il DRIVER lo ACCENDE** -- l'argv contiene `--mitosi-2lam` -- e dal runtime vale ### **`True`**: e' ON nella configurazione su cui girano **tutti** i sigilli. ### **Lo stesso per `PLAST_DIN`** *(`--plast-din`, default di modulo `False`, runtime **`True`**)*. ### **La riga vecchia resta leggibile** *(par.8)* |

## Che cosa il riordino fa, e che cosa NON fa

| | |
|---|---|
| ### ✅ **SEPARA la decisione dall'esecuzione** | `decidi_divisione(net) -> (archi_da_dividere, perche')`: ### **legge e NON SCRIVE NIENTE.** Oggi decisione e scrittura sono **intrecciate** per 270 righe, e per questo *«chi decide»* non si puo' nemmeno leggere |
| ### ⛔ **NON cambia la soglia** | `3π` resta **identica**, e il piano lo dichiara: ### **byte-identico**. Ma ### **la soglia E' `D36`** *(acclarato per misura: con `phi` su `2π` gli archi sopra soglia passano da **7047 a ZERO**)*, e ### **un riordino che la tocca cambia la fisica** |
| ### ⛔ **NON cambia il `0.3`** | resta, ### **e si DICHIARA come numero non derivato** nel registro fisica. **Toglierlo e' una cura a se'** |

## ✅ **LE DECISIONI DI LUCA** *(2026-10-01)* — **tutte e cinque RISPOSTE**

| | la decisione |
|---|---|
| **1** | ### **la soglia `3π` resta INVARIATA nel riordino.** `D36` *(soglia adimensionale)* diventa ### **una voce a se', DOPO, con la sua misura** |
| **2** | ### **il `0.3` si DICHIARA** nel registro fisica **come numero NON derivato**. ### **Toglierlo e' una cura a se', dopo** |
| **3** | ### **i pavimenti `1e-6`/`1e-3` e `massa_critica_collasso`: FUORI dal riordino**, come voce a se' |
| **4** | ### **`MITOSI_DIR` si ARCHIVIA** *(vale `0.0`, il ramo non gira)*, e ### **il commento «ATTIVA» si corregge SUBITO** |
| **5** | ### **`MITMAX` diventa un ERRORE come `MAX_NODI`**, non un tetto che tronca |

### ⚠ **Sul «subito» di (4): NON l'ho fatto in questo commit, e dico perche'**
Il mandato di questo giro dice ### **«Nessun codice. STOP dopo»**. La correzione del commento e'
**byte-inerte**, ### **ma e' comunque una riga del simulatore** — e infilarla in un commit dichiarato
senza codice sarebbe ### **esattamente il tipo di scorciatoia che i presidi di questo repo esistono
per impedire.** ➜ **E' il COMMIT 0 dell'ordine qui sotto**, e si fa **per primo**.

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **deve restare IDENTICO AL BYTE** | **tutto**: quali archi si dividono, quanti, e in quale ordine. ### **La separazione decisione/esecuzione e' una RIORGANIZZAZIONE, non una cura** |
| cosa puo' cambiare | ### **niente.** Un solo bit diverso ⇒ **non e' una separazione, e' una cura non dichiarata** |
| ### **il caso che DEVE fallire** | ### ⛔ **CORRETTO: la prima stesura NON POTEVA fallire.** Dicevo *«si altera la soglia di `1e-12`»*, e ### **nessun arco sta a `1e-12` dalla soglia**: il sigillo sarebbe passato **per costruzione**, senza guardare niente. ### ➜ **Ora: si porta la soglia APPENA SOTTO il `\|tw\|` piu' alto fra gli archi che OGGI stanno sotto soglia**, cosi' ### **almeno UN arco NOTO deve passare** — e si confronta ### **la LISTA di `decidi_divisione` ARCO PER ARCO**, non il conteggio delle nascite *(un conteggio uguale puo' nascondere due archi scambiati)* |

---

# **(b) STRUTTURA: come nascono nodi e archi**

## Com'e' oggi

| | come |
|---|---|
| **il nodo** | `pos_figlio = 0.5·(pos[a] + pos[b])` → ### **il PUNTO MEDIO** |
| **gli archi** | l'arco `(a,b)` e' ### **SOSTITUITO** da `(a,m)` e `(m,b)`, lunghi `d/2` *(`keep` toglie lo spezzato)* |
| **`d` e `d0`** | `dh = d[sel]/2`, poi ### **`_nasce(...)` porta a `LAM` cio' che sta sotto** |
| **`tw` dei nuovi** | ### **`0`** *(`zz = zeros(len(sel))`)* |
| **lo Schwinger** | ### **AGGIUNGE** due archi verso `k` **senza togliere** `(aa,bb)`, e ### **`dd` viene da `pos`** |

## ⭐ **LA DOMANDA DI FISICA DI LUCA: «perche' per forza il punto medio?»** *(2026-10-01)*

> ### **Il punto medio NON E' DERIVATO: e' la toppa ③.**
> E' la scelta **simmetrica**, ### **ma ignora che i due estremi hanno STATI DIVERSI** — torsione,
> densita', `psi`, tempo proprio.

### ➜ **Per la STELLA POLARE** *(«le leggi sono simmetriche, gli stati scelgono»)* **la forma giusta
e' una FRAZIONE:**

```
t = f(stato_a, stato_b)        con        f(a, b) = 1 - f(b, a)
```

### **Scambiando gli estremi il figlio va nella posizione SPECULARE**, e ### **il punto medio e' solo
il caso in cui gli stati sono UGUALI.** ### ➜ **Non e' una legge che preferisce un lato: e' una legge
simmetrica che lascia scegliere allo stato** — esattamente la forma che la stella polare chiede, e
### **l'opposto di `MITOSI_DIR`**, che metteva un **coefficiente scelto** davanti a una `tanh`.

### ⚠ **E non si decide ORA quale grandezza scelga `t`:** e' una ### **decisione di fisica di Luca**,
in una ### **voce a se' (`DIVISIONE-AUTOCONSISTENTE`, nata come `FRAZIONE-DIVISIONE`)**. ### **Qui si prepara SOLO la STRUTTURA.**

## ✅ **Come la struttura si prepara** *(commit 6a)*

| | |
|---|---|
| **1** | il figlio sta a ### **`t·d` da `a`** e a ### **`(1−t)·d` da `b`** |
| ### **2** | ### **LO STESSO `t`** vale per **`pos_figlio`** *(dove nasce)* **e per `d`/`d0` dei due nuovi archi** *(quanto sono lunghi)*. ### **Oggi sono DUE formule indipendenti che per caso dicono entrambe «meta'»: domani devono dire LA STESSA COSA, o il figlio nasce in un posto e gli archi ne descrivono un altro** |
| **3** | per ora ### **`t = 0.5` per tutti, DICHIARATO IN UN SOLO POSTO.** ### **Il punto medio smette di essere una FORMULA SPARSA e diventa un VALORE DICHIARATO** |
| **4** | ### **lo stesso vale per lo SCHWINGER**, dove il figlio nasce **anche li'** nel punto medio |

> ### 📌 **Perche' questo e' un riordino e non una cura:** con `t = 0.5` ### **il valore non cambia di
> un bit.** Cambia **dove vive**: da **quattro formule** *(`pos` e `d` per la divisione, `pos` e `dd`
> per lo Schwinger)* a ### **una costante dichiarata** — e **da li'** una decisione di fisica potra'
> cambiarla ### **in un posto solo.**

## ⛔ **Il confine che NON tiene, e lo dico invece di assorbirlo**

> ### **`M2` ① e ②, `U2` e `MITOSI_2LAM` NON si possono separare da questa parte.**
> La parte (b) **e'** *«come nascono `pos`, `d`, `d0`»*, e ### **il punto medio e la fabbricazione di
> lunghezza SONO quella descrizione.** Non sono voci accanto al riordino: ### **sono il riordino.**

| il difetto | ### **la DECISIONE di Luca** |
|---|---|
| ### **`M2` ①** il figlio a `d/2` da ciascun genitore e' ### **sotto `LAM` se `d < 2·LAM`** → viola **`A13`** | ### ✅ **si RIFIUTA la divisione**: `MITOSI_2LAM` **ON**, come **legge** |
| ### **`M2` ②** due meta' portate a `LAM` danno `2·LAM` al posto di `d` | ### ✅ **il caso SMETTE DI ESISTERE**: niente sotto `2·LAM` si divide, quindi ### **`d/2 + d/2 = d` esattamente** e `_nasce` non ripara |

## ⛔ **UNA MIA AFFERMAZIONE ERA FALSA, e il guardiano l'ha smontata sul codice**

**Avevo scritto:** *«`A13` e la conservazione della lunghezza **non possono valere entrambe** alla
nascita — una delle due cede»*. ### **E' FALSO.**

**Con `MITOSI_2LAM` ON** *(il filtro sta a `:6956`)* un arco con `d < 2·LAM` ### **NON SI DIVIDE
AFFATTO**: `ok = ok & _conforme` lo **toglie dai candidati** prima dello spezzamento. Allora i figli
nascono a ### **`d/2 >= LAM`**, ### **`_nasce` non ripara niente**, e ### **`d/2 + d/2 = d`
ESATTAMENTE.** ### ➜ **Valgono TUTTE E DUE.**

> ### 📌 **L'incompatibilita' esiste SOLO se la divisione e' OBBLIGATORIA** — e non lo e'.
> ### **Il mio errore e' stato logico, non di lettura: ho trattato la divisione come un atto dovuto,
> e da li' ho dedotto un conflitto fra due leggi che non si toccano.**
> **E il codice lo sapeva gia':** il commento del filtro dice che la cura va messa dove *«si decide
> se questo candidato si divide o no»*, ### **«NON in `_nasce`: la' si RIPARA, e la cura e' proprio
> togliere la riparazione»**. **Avevo la risposta sotto gli occhi.**

### ✅ **E `MITOSI_2LAM` era GIA' «approvata da Luca»**, scritto nel commento a `:418`: era **OFF**
solo per *«un interruttore alla volta»*, ### **non perche' la legge fosse in dubbio.**

## ✅ **LA DECISIONE DI LUCA sulla parte (b)** *(2026-10-01)*

> ### **Si RIFIUTA la divisione sotto `2·LAM`: `MITOSI_2LAM` ON, come LEGGE e non come
> interruttore**, nel **commit 5**, con la misura di ### **quante divisioni vengono rifiutate** e
> ### **di quanto cala `n` al passo 72** — *«si riporta, non si giudica»*.

### ➜ **E il caso «fabbricazione di lunghezza» SMETTE DI ESISTERE, e lo dichiaro:**
`M2` ② descriveva due meta' portate a `LAM` che davano `2·LAM` al posto di `d`. ### **Con la
divisione rifiutata sotto `2·LAM`, quel caso non si presenta piu': `_nasce` non ha piu' niente da
riparare sui tronconi della mitosi.** ### **Il secondo motore di gonfiamento di `M2` e' CHIUSO dalla
decisione**, non mitigato.

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **6a: `t` esplicito, `t = 0.5`** | ### **BYTE-IDENTICO, contatori compresi.** E' una **riorganizzazione**: lo stesso numero, in un posto solo. ### **Caso che DEVE fallire: una copia con `t = 0.5 + 1e-9` deve cambiare `pos` E `d` dei nati, e il sigillo deve vederlo** *(se non lo vede, non sta guardando la struttura)* |
| ### **6b: la LEGGE, non un interruttore** | `MITOSI_2LAM` diventa **legge**: ### **il ramo `else` ESCE dal sorgente**, come in `CURA2-STRUTTURALE` — e ### **va ARCHIVIATO COPIATO**, non cancellato *(`RAMI-OFF-CURA2`)* |
| ### **6b: e la forma e' GENERALE** | ### **non `d >= 2·LAM`, ma `t·d >= LAM` E `(1−t)·d >= LAM`.** Con `t = 0.5` ### **e' la stessa cosa**, ma ### **resta vera quando `t` cambiera'** — ed e' la ragione per cui `6a` viene **prima** |
| ### **cosa deve restare IDENTICO** | ### **tutto cio' che NON riguarda gli archi rifiutati.** Gli archi con `d >= 2·LAM` si dividono **come prima**, ed e' su loro che il byte-identico vale |
| ### ⛔ **ANNOTAZIONE DEL 2026-10-02: QUESTO CRITERIO E' SCRITTO SU UNA PREMESSA FALSA** | `MITOSI_2LAM` ### **e' GIA' ACCESO nel driver** *(`MITOSI-2LAM-ACCESO`, misurato dal runtime)*. ### ➜ **Quindi far uscire il ramo `else` dal sorgente e' BYTE-IDENTICO IN QUELLA CONFIGURAZIONE**, non un cambio di fisica: lo sarebbe ### **solo con l'argv NUDO.** ### **Il criterio va riletto, e con lui le due misure che il piano chiede qui sotto.** ### ⚠ **E che il flag AGISCA non l'ho misurato:** lo direbbe il contatore `_g_m2l_negati` sulla finestra dei 72 passi, ### **e quella misura NON l'ho girata** -- la dichiaro invece di stimarla |
| ### **cosa CAMBIA, ed e' atteso** | gli archi che non passano ### **NON si dividono piu'**: si misura ### **quante divisioni sono RIFIUTATE** *(il contatore `_g_m2l_negati` esiste gia')* e ### **di quanto cala `n` al passo 72**. ### **Si riporta, non si giudica** |
| ### ⭐ **e si misura COSA SUCCEDE DOPO** *(richiesta di Luca)* | ### **gli archi rifiutati che fine fanno?** Tre esiti possibili, e sono **misurabili**: ### **① restano sopra soglia PER SEMPRE** *(un serbatoio di torsione che non si scarica)* · ### **② la torsione si scarica ALTROVE** *(e allora la mitosi si sposta, non si ferma)* · ### **③ la dinamica li ALLUNGA finche' si dividono** *(e allora e' solo un ritardo)*. ### **Si misura: per gli archi rifiutati, `\|tw\|` e `d` nel tempo fino al 72, e quanti finiscono per dividersi** |
| ### ✅ **e una cosa SMETTE di esistere** | ### **la fabbricazione di lunghezza di `M2` ②**: niente sotto `2·LAM` si divide ⇒ `d/2 >= LAM` ⇒ ### **`_nasce` non ripara, e `d/2 + d/2 = d` esattamente** |
| ### **il caso che DEVE fallire** | una copia in cui `pos_figlio` e' spostato di `1e-9`: il sigillo ### **deve vederlo**. E una in cui `tw` dei nuovi archi e' `1e-12` invece di `0`: ### **deve vederlo** |

---

# **(c) LA NASCITA COME EVENTO UNICO**

> ### **Tutte le grandezze del registro scritte in UN SOLO punto, con UNA regola dichiarata per
> ciascuna. Niente scritture sparse e niente sistemazioni a valle.**

## Il numero di oggi, e il bersaglio

| | oggi | dopo |
|---|---|---|
| posti che scrivono le grandezze della nascita | ### **3** *(`mitosi`, i due `_eredita_*`, piu' la mutazione di `conc_nodi`)* | ### **1** |
| grandezze del registro scritte in `mitosi` | **16 su 30** | ### **30 su 30, nel punto unico** |
| scritture che allungano | **38**, sparse | ### **una per grandezza, in tabella** |

## La forma proposta

```
nascita(net, evento, genitori, quante) -> None
    # per OGNI voce del registro, nell'ordine del registro:
    #   regola = REGOLA_DI_NASCITA[evento][nome]
    #   net.<nome> = regola(net, nome, genitori)
    # e NIENTE ALTRO scrive quelle grandezze.
```

| | |
|---|---|
| **la tabella** | ### **`REGOLE_nascita.tsv` (32 regole) e' il punto di partenza**, ed e' gia' **verificata per ancora** |
| ### **i QUATTRO eventi** | `semina` · `divisione` · `Schwinger` · `allaccio` — ### ✅ **APPROVATI DA LUCA il 2026-10-01**, e ### **questa riga E' la registrazione** *(vedi sotto)* |
| **le regole** | `eredita` · `media` · `zero` · `estrazione nuova` · ### **`eredita INVERTITA`** *(la carica alla Schwinger)* · ### **`derivata dalla definizione`** *(`perc_geom`)* |
| ### **il presidio** | ### **una grandezza del registro che NON compare nella tabella dell'evento ferma il run**: *«regola di nascita non dichiarata per `<nome>` all'evento `<evento>`»*. ### **E' lo stesso disegno del controllo unico, spostato alla nascita** |

### ✅ **I QUATTRO EVENTI SONO APPROVATI, e ORA la decisione E' NEL REPO** *(2026-10-01)*

> ### **DECISIONE DI LUCA, 2026-10-01: i quattro eventi di nascita — `semina`, `divisione`,
> `Schwinger`, `allaccio` — sono APPROVATI.**

### ⚠ **E la registrazione e' QUESTA RIGA, non la chat:** l'approvazione era arrivata il **2026-09-29**
e ### **io non l'avevo scritta nel repo**. Il paragrafo qui sotto resta ### **perche' il difetto non
si cancella: si annota** *(par.8)*.

### ⛔ **Com'era andata: ho scritto «decisi da Luca» e NEL REPO NON C'ERA**

Il guardiano ha chiesto di **citare il commit o la frase**. ### **L'ho cercata e non c'e'.**
Nel repo esiste ### **solo la mia PROPOSTA** — `doc/PIANO_controllo_unico.md:94` *(«Proposta: il
registro dichiara QUATTRO eventi»)* e `:192` *(fra le cose che **non** decido io)*, piu' il
paragrafo della relazione che la propone.

> ### 📌 **L'approvazione e' arrivata, ma SOLO IN CHAT — e io non l'ho scritta nel repo.**
> ### **E' esattamente il difetto del par.4: «un riscontro non relazionato e' un riscontro perso»**
> — e qui il perso e' **una decisione**, non una misura. ### **Peggio: l'ho poi CITATA come se il
> repo la registrasse**, dandole un'autorita' che nel repo non ha.

### ➜ **Quindi la tratto come il mandato dice: PROPOSTA DA APPROVARE.**
I quattro eventi **restano la base del piano** *(senza di loro le sei «incoerenze» di `REGOLE_nascita`
tornano a essere difetti)*, ### **ma la riga che li dichiara decisi non la scrivo finche' non c'e' un
commit che la porti.**

### ⚠ **Che cosa questo richiede, e non e' gratis**

| | |
|---|---|
| ### **i due `_eredita_*` SPARISCONO** | le loro 13 grandezze entrano nella tabella. ### **Sono le funzioni nate dalle cure di `C7`/`C11`/`PSI-FLASH`**: il riordino **non le butta**, le **assorbe** — e la storia dice **perche' esistono** |
| ### **`conc_nodi` deve smettere di crescere per MUTAZIONE** | e' l'unica che cresce con `.append`, ### **invisibile all'AST e alla sorveglianza**. ➜ **O entra nel registro con una scrittura vera, o esce dal registro e la sua riparazione si motiva** |
| ### **la riallocazione di `_rep` deve sparire** | `_rep = zeros(...)` quando le lunghezze non tornano ### **butta la memoria in silenzio**, e sta ### **nell'unica finestra che il controllo unico non vede**. Con la nascita in un punto solo ### **quel ramo non ha piu' ragione di esistere** |

## ⛔ **UN RISCHIO CHE NON AVEVO DICHIARATO** *(correzione del guardiano)*

> ### **Spostare le scritture della nascita in un punto solo puo' cambiare L'ORDINE DELLE ESTRAZIONI
> CASUALI** *(`_xi_rumore` e le altre)* ### **e l'ordine delle SOMME IN VIRGOLA MOBILE.**

**E il generatore e' `net.rng`, uno solo**: ### **chi pesca prima cambia cio' che pescano tutti gli
altri.** Un riordino che sembra una pura riorganizzazione ### **puo' cambiare il mondo per il solo
fatto di aver cambiato l'ORDINE.**

### ➜ **Quindi, PRIMA di scrivere il commit 3:**

| | |
|---|---|
| **1** | ### **si MISURA quali estrazioni casuali avvengono nella nascita e in che ORDINE** — con la sorveglianza su `net.rng`, come quella che ha gia' intercettato **1 887 282** accessi per passo |
| **2** | ### **l'ordine diventa PARTE DEL CONTRATTO**: va scritto nella tabella delle regole di nascita, accanto alle regole |
| **3** | ### **e la SOMMA conta quanto l'estrazione**: dove un valore nasce da una somma di contributi, ### **l'ordine degli addendi e' parte del risultato** in virgola mobile |

> ### 🛑 **E SE IL BYTE-IDENTICO CADE SOLO PER QUESTO: MI FERMO E LO DICO.**
> ### **NON allento il criterio.** *(E' la regola di Luca, ed e' quella giusta: un criterio allentato
> per far passare un commit non e' un criterio, e' una formalita'.)*

### ✅ **IL CONTRATTO DELL'ORDINE, MISURATO PRIMA DI SCRIVERE IL CODICE** *(2026-10-02, `csv/_test_fork/_ordine_registro.py`)*

> ### **Il par.(c) chiede <<nell'ordine del REGISTRO>>. QUESTO E' MISURATO, non assunto: l'ordine
> del registro e' un ordine TOPOLOGICO VALIDO, e i vincoli sono QUATTRO in due forme.**

| | il vincolo | perche' |
|---|---|---|
| **1** | ### **`phi` prima di `twp`** | `twp` legge `phi[a,b]` ### **DOPO il calcio**, che e' una scrittura **indicizzata** sui genitori, non un'estensione ⇒ **genuino**. ### ✅ **Rispettato**: `phi` sta in `METRI`, cioe' prima di tutto `STATO` |
| **2** | ### **`peq` prima di `_peqn_idx`** | `_peqn_idx` legge `peq` ### **INTERA**, ed e' cio' che il commento al `:7588` **dichiara**. `_peqn_idx` non sta in nessun registro ⇒ ### **va dichiarato DOPO `peq`** nella tabella |
| **3** | ### **`n0` va nel CONTESTO** | **4 locali interposte**, tutte `n0` *(i due `_eredita_*`, i due eventi)*: `n0 = self.n - k` legge ### **`self.n`, cioe' `len(self.phi)`, DOPO l'estensione.** ⇒ ### **la regola NON deve leggere `self.n`**: riceve `n0` calcolato nella fase di **PREPARAZIONE** |
| **4** | ### **6 chiamate con EFFETTO** | `_smp_chirurgia`, `_traccia_d0`, `_grado` — ### **tre per evento.** ### **NON sono regole di nascita** e non vanno in tabella: si collocano **a mano** e si **dichiarano** una per una |

### 📌 **E DUE CASI SONO STATI SCARTATI COME INERTI, ed e' importante quanto trovarli:**
`chi_a`/`chi_b` al `:7405` leggono `perc_chi` ### **gia' estesa** al `:7372` — ma la leggono ### **sui GENITORI** *(indici `< n0`)* e la scrittura precedente e' una ### **PURA ESTENSIONE**, che non tocca i primi `n0` elementi. ### ➜ **Il valore non cambia, e contarli per ostacoli avrebbe gonfiato la cura** (`9-ter`).

### ⚠ **E LO STRUMENTO HA AVUTO TRE BUCHI PRIMA DI DARE QUESTO NUMERO**, tutti della forma `FALSO-ZERO`: l'insieme sul solo `REGISTRO_STATO` *(escludeva `phi`/`i`/`j`/`_peqn_idx`)*, le letture mediate da una ### **`@property`** *(`self.n`)*, e le ### **locali interposte**. ### **Il primo numero era ZERO, e lo zero era falso.**

---

per far passare un commit non e' un criterio, e' una formalita'.)*

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **byte-identico, scena grande fino al 72, CON nascite** | **grandezze E contatori**, contro il blob di prima. ### **La nascita come evento unico e' una RIORGANIZZAZIONE: non deve cambiare un bit** |
| ### **e l'ORDINE delle estrazioni e' nel contratto** | ### **misurato PRIMA**, scritto nella tabella, e ### **verificato dal sigillo** |
| ### **e il CONTATORE e' il controllo piu' fine** | i rami della nascita **si contano** *(`_rep_realloc`, `_g_eredpsi_*`, `_ritmo_sicurezza`…)*: ### **un contatore che cambia di uno e' un difetto che le grandezze non vedrebbero** — misurato in questa sessione |
| ### **il caso che DEVE fallire** | **tre**, e sono quelli che dimostrano che il sigillo vede un difetto **della nascita**: ### **① si TOGLIE una grandezza dalla tabella** ⇒ deve fermarsi con *«regola non dichiarata»* · ### **② si cambia la regola di UNA grandezza** *(`psi` da `media` a `eredita`)* ⇒ il sigillo **deve vedere la differenza** · ### **③ si lascia una scrittura SPARSA a valle** ⇒ deve essere **impossibile**, cioe' il presidio deve nominarla |

---

# **(d) DERIVATE — generalizzazione 4: le derivate SPORCHE alla nascita**

> ### **Quando nasce un nodo, le derivate sono segnate DA RICALCOLARE; leggerne una sporca e' un
> ERRORE; tornano pulite quando la loro legge le riscrive.**
> ### **E' la regola «letta fra nascita e riscrittura» resa LEGGE DEL SISTEMA** invece di un
> accertamento fatto una volta con una misura.

## Quello che la misura ha gia' detto *(`bd9262f`)*

Nella finestra della nascita, delle **10** derivate *(8 per nodo, 2 per arco)*:

| | |
|---|---|
| **4** | ### **nessuna legge le legge** — `_chi_core_nodi` `_chi_core_rho0` `_chi_core_raggio` `_fatt_cs_ultimo` *(e per l'ultima il codice dichiara «nessun lettore, Z7»)* |
| **4** | la legge le trova ### **GIA' RISCRITTE** — `_chi_geom_nodi` `_r_corrente` `_dt_e_ultimo` `_sin2_vir` |
| ### **2** | ### **AUTO-RINFRESCO**: `_xi_rumore` *(ed **E'** la regola di nascita: il figlio non eredita l'ambiente)* e `_g_rampa_prec` *(diagnostica, disallineamento gia' contato)* |
| ### **BUCHI** | ### **ZERO** |

### ➜ **Quindi oggi la regola e' VERA. Ma e' vera per MISURA, su UNA scena e UNA configurazione** —
ed e' ### **il terzo limite che ho scritto nella scheda.** La generalizzazione 4 la rende **vera per
costruzione**.

## La forma proposta

| | |
|---|---|
| **la marca** | alla nascita, **ogni** voce di `REGISTRO_DERIVATE` entra in `net._sporche` |
| **la pulizia** | la **legge che la riscrive** la **toglie** da `_sporche` — ### **e non lo fa un'altra** |
| ### **la lettura** | leggere una derivata **sporca** ⇒ ### **`DerivataSporca`**, col **nome**, **chi** la legge e **quale legge** dovrebbe pulirla |
| ### ⚠ **il costo, e va detto** | intercettare **la lettura** costa: la sorveglianza di questa sessione ha misurato ### **1 887 282 accessi per passo** sulle sole 43 grandezze. ### **Un controllo su OGNI lettura non e' gratis come uno sui CONFINI delle voci** |

## ⛔ **L'opzione «AI CONFINI» NON FUNZIONA, e il guardiano ha ragione**

**Avevo proposto di verificare la marca ai confini delle voci.** ### **Non regge:** dopo `mitosi`
una derivata e' sporca ### **LEGITTIMAMENTE** fino alla voce che la riscrive — quindi un controllo al
confine ### **o la segnala per sbaglio, o non controlla nessuna lettura.** **Era una terza via solo
in apparenza: in realta' e' la prima che non guarda niente.**

## 🧪 **LA TERZA VIA VERA: il VELENO. E l'ho MISURATA** *(sonda `csv/_test_fork/_sonda_veleno.py`)*

> ### **Alla nascita le derivate dei nuovi nodi si riempiono con un valore AVVELENATO** *(`NaN` per i
> float)*, **e il controllo unico verifica che nessuna grandezza di STATO contenga valori non
> finiti.** ### **Una lettura sporca PROPAGA il veleno nello stato, e viene presa al confine
> successivo.**

### ✅ **E non e' un'invenzione: il sistema LO FA GIA', in due punti**

| | |
|---|---|
| `:3693` in `_allaccia` | `self.peq = np.concatenate([self.peq, np.full(len(dd), np.nan)])` ### **` # da calibrare`** |
| `:7165` nella mitosi/Schwinger | `pmed = np.nan if PEQ_NASCITA_LOCALE else float(np.median(self.peq))` |

### ➜ **`peq` — una grandezza di STATO — nasce `NaN` PER DISEGNO, e `step` la CALIBRA.**
Il flag lo dichiara: *«gli archi della creazione di coppia alla Schwinger nascono con `nan` e vengono
**CALIBRATI** da `step()`»*. ### **Cioe' `peq` E' GIA' una grandezza «sporca alla nascita, con un
veleno e un pulitore dichiarato»: la generalizzazione 4 non introduce una convenzione nuova — ESTENDE
QUELLA CHE IL SISTEMA HA GIA'.**

### 📊 **Le tre misure che il mandato chiede** *(scena GRANDE, `n = 12802`, `m = 471564`)*

| | |
|---|---|
| ### **① il COSTO** | un controllo di finitezza su **tutte e 30** le voci di STATO: ### **`0.002085 s`**. Un **passo** costa ### **`2.849 s`** ⇒ ### **lo `0.073 %`**. Con **9** controlli per passo *(generalizzazione 2)*: ### **lo `0.659 %`.** ### **E' trascurabile** |
| ### **② le derivate INTERE** | ### **ZERO.** Tutte e **10** le derivate sono `float64` ⇒ ### **il veleno `NaN` esiste per TUTTE**, e la domanda *«cosa si fa dove `NaN` non esiste»* ### **non ha casi** |
| ### **③ `seterr(invalid='raise')`** | ### **il `NaN` PROPAGA**: somma, prodotto, ### **confronto `>`**, `isfinite`, `sum` — **nessuna eccezione**. Solleva **solo** su `astype(int64)` e su `inf - inf` ⇒ ### **il veleno funziona: arriva allo stato invece di far crashare la lettura** |

### ⛔ **E una QUARTA misura che NON era nel mandato, e RAFFINA la proposta**

**Censimento dei non finiti su un run SANO:** ### **UNA grandezza di STATO ne ha gia'** —
### **`eta`, `inf` su TUTTI i 12802 nodi** — ed e' ### **LEGITTIMO E DICHIARATO** *(dominio
`nonneg_inf`: «`+inf` per il vuoto DATO»)*.
### ➜ **Quindi un controllo GLOBALE di finitezza SPARA AL PRIMO PASSO**, e il veleno ### **non si
distingue da cio' che e' legittimo.**

### ✅ **LA PROPOSTA, raffinata dalle misure** *(e decide Luca)*

| | |
|---|---|
| **la forma** | il controllo di finitezza e' ### **PER GRANDEZZA, con l'esenzione DICHIARATA NEL REGISTRO** — ### **lo stesso schema gia' in piedi per il TIPO** *(`None` = esente, e c'e' **una** sola esenzione)* |
| le esenzioni | ### **`eta`**, permanente e dichiarata *(`+inf` e' nel suo dominio)*; ### **`peq`**, **temporanea** — `NaN` dalla nascita fino alla calibrazione di `step` ### **che e' ESATTAMENTE la semantica «sporca»** |
| ### ➜ **la convergenza** | ### **«derivata sporca» e «`peq` da calibrare» sono LA STESSA COSA.** La generalizzazione 4 non aggiunge una legge: ### **da un NOME a cio' che il sistema fa gia' in due punti** — e per `9-ter` questo conta |
| ### ⚠ **il prezzo, dichiarato** | il veleno ### **rende NON BYTE-IDENTICO** il passo della nascita, perche' una derivata che prima conteneva un valore vecchio ora contiene `NaN`. ### **Non e' una riorganizzazione: e' un cambio di stato** — e il suo sigillo **non puo'** chiedere byte-identico sulle derivate |

## ✅ **LA DECISIONE DI LUCA su (d): il VELENO e' APPROVATO** *(2026-10-01)*

> ### **DECISIONE DI LUCA, 2026-10-01: la terza via — il VELENO — e' APPROVATA nella FORMA
> RAFFINATA.**

| | |
|---|---|
| **la forma** | controllo di finitezza ### **PER GRANDEZZA**, con le esenzioni ### **DICHIARATE NEL REGISTRO** *(`eta`: `inf` per il vuoto)* — ### **lo stesso schema del TIPO** |
| ### **e un solo MECCANISMO, un solo NOME** | ### **«derivata sporca» e «`peq` da calibrare» diventano LA STESSA COSA.** Non due convenzioni che si assomigliano: **una** |
| ### **il prezzo, ACCETTATO** | al passo della nascita il sigillo del **commit 4** confronta al byte ### **lo STATO, NON le derivate**. ### **E' il solo criterio del piano che si restringe, ed e' una DECISIONE, non un allentamento mio** |

### ➜ **E questa riga e' la REGISTRAZIONE della decisione** *(par.4: un'approvazione in chat non
basta)*.

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **byte-identico** | la marca **legge e scrive un insieme di nomi**: ### **non tocca una grandezza di fisica** |
| i contatori | ### **i contatori della MARCA sono «del presidio»** e cambiano per costruzione: si **separano per nome e si RIPORTANO**, come gia' fatto per `_g_registro_*` |
| ### **il caso che DEVE fallire** | ### ⛔ **CORRETTO: usavo `_deg`, che NON e' una derivata.** `_deg` e' in ### **`REGISTRO_STATO`** *(`:1095`)*, non in `REGISTRO_DERIVATE` — quindi il caso **non provava niente della marca**. ### ➜ **Ora: si rinvia la riscrittura di `_chi_geom_nodi`** *(o di `_r_corrente`)*, che sono ### **derivate VERE**, e il sigillo deve ### **nominare quella grandezza**. **Se non lo fa, la marca non guarda niente** |

---

# **(3-bis) IL REGISTRO DICHIARATO, non misurato**

> ### **Una grandezza per nodo o per arco NON DICHIARATA ferma il run.**
> E' il ### **terzo limite** della scheda — *«una scena, una configurazione»* — e questo lo toglie.

## Come la trovo

| | |
|---|---|
| **il criterio** | ### **al controllo, si scorrono TUTTI gli attributi della rete** *(`vars(net)`)* e si cercano quelli che sono **array o liste** con ### **primo asse `== n` oppure `== m`** |
| **l'esito** | se il nome ### **non e' nel registro** *(ne' `STATO`, ne' `DERIVATE`, ne' `METRI`)* ⇒ ### **`GrandezzaNonDichiarata`**, col **nome**, la **forma** e il **tipo** trovati |
| ### **perche' vale con QUALUNQUE flag** | non parte da un elenco: ### **parte da cio' che la rete HA.** Un flag che crea una grandezza nuova la fa **comparire**, e il controllo la **nomina** |

## ⚠ **E come EVITO che la regola dipenda dai NOMI o dalla SINTASSI**

### **Questa e' la domanda piu' importante del paragrafo, perche' l'errore l'ho fatto SEI VOLTE in questa sessione:**

| volta | la regola sbagliata | che cosa ha nascosto |
|---|---|---|
| 1 | `full(n,…)` contato come *«estende»* | i siti che sostituivano |
| 2 | la condizione fusa chiamata *«inizializzazione»* | il difetto dentro l'`or` |
| 3 | `==`/`!=` messi *«fuori dal mandato»* | **sette** siti |
| 4 | il ramo degli `IfExp` **invertito** | una *«famiglia»* intera **inesistente** |
| 5 | il filtro per **NOME** che perde gli **alias locali** | 4 siti su 10 senza riga |
| 6 | la lista di **nomi** `semina`/`mitosi`/`_allaccia` al posto del **grafo** | **falsi BUCHI** nel registro |

> ### 📌 **La forma dell'errore e' SEMPRE la stessa: una regola che parte dal NOME o dalla SINTASSI
> invece che da CIO' CHE FA.** E la cura, provata tre volte in questa sessione, e' sempre la stessa:
> ### **non leggere il codice — GUARDARE LA RETE.**

**Quindi il presidio del registro dichiarato:**

| | |
|---|---|
| ### ✅ **parte dal RUNTIME, non dall'AST** | `vars(net)` e il **primo asse**: ### **nessun nome, nessuna sintassi, nessun alias.** Una grandezza si qualifica **per la sua FORMA**, che e' un **fatto**, non una convenzione |
| ### ✅ **e il suo CASO CHE DEVE FALLIRE e' banale e decisivo** | si aggiunge `net.pippo = np.zeros(net.n)` ⇒ ### **deve fermarsi nominando `pippo`.** ### **Se non lo fa, il presidio non guarda la rete** |
| ### ⚠ **il limite che RESTA, e lo dichiaro** | una grandezza con `len` **diverso** da `n` e da `m` ### **non viene vista** *(per esempio una per-faccia o per-ciclo)*. ### **Il presidio copre i due metri che il registro conosce, non tutti i metri possibili** |
| ### ⚠ **e le coincidenze** | se `n == m` i due metri sono **indistinguibili**. Oggi `12802` contro `471564`, ### **e lo strumento lo CONTROLLA e lo dichiara** — ma su una rete piccola potrebbe succedere |

### **Criteri, fissati PRIMA dei numeri**

| | |
|---|---|
| ### **byte-identico** | il presidio **legge** `vars(net)` e **solleva**: ### **non tocca niente** |
| **e il run sano non deve fermarsi** | ⇒ ### **tutte le grandezze per nodo/arco della configurazione del driver devono essere GIA' nel registro.** **Le 43 misurate ci sono**; ### **se ne compare una, e' informazione, non un difetto del presidio** |
| ### **il caso che DEVE fallire** | `net.pippo = zeros(n)` ⇒ **`GrandezzaNonDichiarata: pippo`**. ### **Piu' un secondo: `net.pluto = zeros(m)`** ⇒ deve nominare **`pluto`** e dire **per arco** |

---

# 📋 **L'ORDINE DEI COMMIT: piccoli, uno per cambiamento, ognuno col suo sigillo**

| # | commit | che cosa cambia | sigillo |
|---|---|---|---|
| ### **0** | ### **il commento di `MITOSI_DIR`** | dice **«ATTIVA»** e il valore e' **`0.0`**: ### **una riga, byte-inerte, e Luca la vuole «subito»** | ### **nessun sigillo**: e' un **commento**. *(E `H-P7` lo guarda: un flag il cui commento cambia deve nominare quel flag)* |
| **1** | ### **registro DICHIARATO** *(3-bis)* | `GrandezzaNonDichiarata`, e il controllo scorre `vars(net)` | byte-identico 72 + ### **`pippo` e `pluto`** |
| **2** | ### **decisione SEPARATA** *(a)* | `decidi_divisione` legge e non scrive. ### **Soglia e `0.3` INVARIATI** | ### **byte-identico, zero bit** + la soglia portata **appena sotto il `|tw|` piu' alto fra gli archi oggi sotto soglia** ⇒ ### **almeno un arco NOTO deve passare**, e si confronta ### **la LISTA arco per arco** |
| **3** | ### **nascita come EVENTO UNICO** *(c)* | i due `_eredita_*` **assorbiti**, la tabella delle 32 regole, il presidio della **regola non dichiarata** | byte-identico 72, **contatori compresi** + i **tre** casi che devono fallire |
| **4** | ### **derivate SPORCHE** *(d, generalizzazione 4)* | la marca, e `DerivataSporca` | byte-identico + **riscrittura rinviata** ⇒ deve nominare la derivata |
| **5** | ### **`perc_geom` del nato `= −1`** | ### **FUORI dal riordino, gia' deciso.** Dipende **solo** dal punto unico di nascita *(commit 3)*, ### **non dalla struttura** | byte-identico **tranne** `perc_geom` dei nati, e il **frame-drag** misurato |
| ### **6a** | ### **STRUTTURA: la FRAZIONE `t` esplicita, `t = 0.5`** | ### **RIORGANIZZAZIONE**: da **quattro formule** a ### **un valore dichiarato in un posto solo**. Lo stesso `t` per `pos` e per `d`/`d0`, ### **Schwinger compreso** | ### **BYTE-IDENTICO, contatori compresi** + ### **`t = 0.5 + 1e-9` deve cambiare `pos` E `d` dei nati** |
| ### **6b** | ### **`MITOSI_2LAM` come LEGGE, in forma GENERALE** | `t·d >= LAM` **e** `(1−t)·d >= LAM`. Il ramo `else` **esce** e si **archivia copiato** | ### **NON byte-identico, ATTESO**: divisioni **rifiutate**, calo di `n` al 72, ### **e che fine fanno gli archi rifiutati** |
| **(7)** | *(fuori dal riordino, in coda)* | `D36` · il **`0.3`** · i **pavimenti** e `massa_critica_collasso` · `MITMAX` **errore** · ### **`DIVISIONE-AUTOCONSISTENTE`** *(e `MITOSI_DIR` e' **archiviato** al commit 0)* | ognuna ### **voce a se', con la sua misura** |

### ⚠ **Perche' `1` viene PRIMA di tutto**
Il **registro dichiarato** e' l'unico pezzo che ### **rende impossibile dimenticare una grandezza
mentre si sposta la nascita.** Farlo **dopo** vorrebbe dire riordinare ### **senza la rete di
sicurezza**, ed e' esattamente l'errore che la storia racconta **sette volte**.

### ⚠ **Perche' la STRUTTURA e' DIVISA in `6a` e `6b`** *(correzione del guardiano)*
Il vecchio commit 6 ### **mescolava una RIORGANIZZAZIONE byte-identica** *(`t` esplicito)*
### **con un CAMBIAMENTO DI FISICA** *(`MITOSI_2LAM` legge)*. ### **Mescolati, un fallimento non si
sa a chi attribuirlo** — ed e' il difetto che il par.3 chiama *«un interruttore alla volta»*.
### ➜ **`6a` byte-identico, `6b` misurato: se `6b` sposta un numero, si sa che e' la LEGGE.**

### ⚠ **E perche' `6b` e' scritta in forma GENERALE**
`t·d >= LAM` **e** `(1−t)·d >= LAM` ### **con `t = 0.5` e' identica a `d >= 2·LAM`**, quindi **non
cambia niente oggi**. ### **Ma resta VERA quando `t` cambiera'**, e scriverla in forma speciale
vorrebbe dire ### **dover ricordare di generalizzarla il giorno della decisione su `t`** — cioe'
**fidarsi della memoria** invece della forma.

### ✅ **E perche' `perc_geom` e' SALITO al 5** *(correzione del guardiano)*
Avevo messo `perc_geom` **in fondo**, dopo la struttura. ### **E' sbagliato: dipende solo dal PUNTO
UNICO di nascita** *(commit 3)* — serve che il registro sia **l'unico posto** che scrive una regola
di nascita, ### **e non serve affatto che la struttura sia riordinata.** ➜ **Cosi' non aspetta una
decisione che non lo riguarda.**

---

# 🛑 **I CONFINI, dichiarati**

| voce | dove sta |
|---|---|
| **`perc_geom` del nato** | ### **commit 6**, dopo il riordino: commit e sigillo **separati**, come deciso |
| `GEOM-SENZA-VERSO` | **dopo**. ### **Il suo primo passo e' una decisione di Luca** *(lo specchio)* |
| `P-EQ-MEDIANA-ARCHI` | **dopo**: e' in `step`, non nella nascita |
| `POTATURA-GUARDIE` | ### **dopo**, per decisione di Luca: il riordino **tocchera' molte di quelle 57 righe** |
| `SCHW-CORTI` | ### **dopo, e SOSPESA** per priorita'. ⚠ **Ma il commit 5 tocca `dd`**: se la struttura si riordina, ### **la domanda «`dd` da `d` o da `pos`» diventa inevitabile** — e allora **si fermera' e si dira'**, non si assorbira' |

### ⛔ **E i DUE confini che NON tengono, ripetuti qui perche' contano**

| | |
|---|---|
| ### **`M2`/`U2`/`MITOSI_2LAM`** | ### **sono la parte (b)**, non una voce accanto. **Il commit 5 non si puo' scrivere senza la decisione di Luca** |
| ### **`D36`/la soglia `3π`** | ### **e' la parte (a)**. Il piano la lascia **invariata** e lo **dichiara**, ### **ma la decisione (a)-1 resta aperta e va risposta** |

---

# ⭐ **LA VOCE: `DIVISIONE-AUTOCONSISTENTE`** *(fuori dal riordino, in coda)*

> ### 🔁 **RINOMINATA il 2026-10-01**, e la ragione e' **di fisica, non di nome**: nata come
> `FRAZIONE-DIVISIONE` *(«dove si rompe l'arco»)*, ### **la voce ha dovuto allargarsi** quando la
> seconda domanda di Luca — *«non dovrebbe esserci una parte di autointerazione?»* — ha portato il
> guardiano a **rileggere il ramo che gira**. ### **Il nome vecchio resta come `alias`:** vive nei
> reperti, nei task history e nel commento di `MITOSI_DIR`, e ### **i reperti non si riscrivono**
> *(par.9)*.

> ### 🔎 **CHE COSA FA OGGI IL RAMO CHE GIRA** *(deterministico, `mitosi`)*
> ```
> tau      = 1 + |tw|/PHI_CRIT ;  mod = tau/(1+tau) ;  sciolta = |tw|/PHI_CRIT
> comune   = KICK_TW * sciolta * (mod - 0.5)
> calcio_a = comune + 0.5 * KICK_TW * sciolta * chi_a * mod
> calcio_b = comune - 0.5 * KICK_TW * sciolta * chi_b * mod
> ```
> e i **due archi nuovi nascono con `tw = 0`**.
> ### ➜ **QUINDI L'AUTOINTERAZIONE C'E' GIA', ED E' DETERMINISTICA:** la **torsione dell'arco**
> decide **quanto forte** e' il calcio ai genitori, e la **chiralita' di ciascun genitore** ne
> decide **il verso**. ### **La risposta alla domanda di Luca e' «c'e'», non «manca»** — e il
> lavoro non e' aggiungerla, e' ### **renderla autoconsistente.**

## ⛔ **I TRE DIFETTI, e il primo e' il piu' grave**

| | il difetto |
|---|---|
| ### **(i) LA TORSIONE SPARISCE** | i due archi figli ripartono da ### **`tw = 0`**, e ### **non c'e' una legge che dica quanta torsione va al calcio e quanta si perde.** Il paragone e' ### **un nastro attorcigliato tagliato in due: ogni pezzo tiene la sua torsione, la torsione non evapora.** `tw` e' un **avvolgimento** *(contato su `±4π`)*, cioe' qualcosa di simile a una ### **carica**: ### **che sparisca alla nascita va giustificato o curato** |
| **(ii) IL PUNTO MEDIO** | non e' derivato — e' la **toppa ③**. E' la domanda che ha aperto la voce |
| ### **(iii) IL CALCIO NON E' SIMMETRICO NELLO SCAMBIO `a <-> b`** | il genitore `a` riceve `+chi_a`, il genitore `b` riceve ### **`−chi_b`**: scambiando le etichette ### **si inverte il verso del calcio del nodo che era `b`.** Ma ### **«`a`» e «`b`» dipendono SOLO dall'ordine di memorizzazione dell'arco `(i, j)`** — e se l'arco non ha un **verso fisico dichiarato**, ### **e' un'orientazione ARBITRARIA che entra nella FISICA.** ### **Stessa famiglia di `GEOM-SENZA-VERSO`** |

## ➜ **LA FORMA: UNA legge sola, guidata dalla torsione dell'arco stesso**

> ### **Al posto di tre pezzi separati** *(dove si rompe · cosa ereditano i figli · il calcio)*,
> ### **UNA legge**, e la sua **forma la decide Luca**.

| | |
|---|---|
| ### **DOVE si rompe l'arco** | la frazione `t`, con ### **`f(a,b) = 1 − f(b,a)`** |
| ### **COSA ereditano i figli** | ### **la loro parte di `tw`**, invece di **zero** |
| ### **IL CALCIO ai genitori** | ### **solo cio' che NON va ai figli**, con il **verso deciso dallo STATO** |

## ✅ **I CRITERI, fissati ORA** *(prima di qualunque legge e di qualunque numero)*

| | il criterio |
|---|---|
| ### **1 — simmetria** | ### **`f(a,b) = 1 − f(b,a)`** nello scambio `a <-> b`. ### **E' la stella polare applicata: la legge e' simmetrica, lo STATO scegle** |
| ### **2 — entrambi i pezzi `>= LAM`** | `t·d >= LAM` **e** `(1−t)·d >= LAM`. ### **Senza questo, una `t` vicina a `0` o a `1` rimetterebbe `M2` ① dalla finestra** |
| ### **3 — nessun coefficiente scelto a mano** | ### **`A1`, e stavolta COMPRENDE `KICK_TW`:** ### **va dichiarato o derivato**, non lasciato dov'e'. E' il criterio che **archivia `MITOSI_DIR` nella FORMA** |
| ### **4 — un BILANCIO ESPLICITO della torsione** | ### **quanta ce n'era prima = quanta ne hanno i figli + quanta ne prende il calcio + quanta si perde** — e ### **ogni perdita va DICHIARATA.** E' la forma di `A8` applicata a una **carica**: ### **una torsione che sparisce senza una riga che lo dica e' un ripiego silenzioso di fisica** |
| **5 — quale grandezza decide `t`** | ### **decide Luca.** I candidati che lo stato offre: `tw` *(torsione)*, la **densita'**, `psi`, il **tempo proprio** — ### **e non ne propongo uno: la misura viene prima** |

## 🧪 **LE PRIME DUE MISURE, prima di qualsiasi legge** *(scena grande, fino al 72)*

| | la misura | che cosa decide |
|---|---|---|
| ### **`M1`** | ### **quanta `|tw|` sparisce per passo con le divisioni** — la somma di `|tw[sel]|`, ### **come FRAZIONE della `|tw|` totale della rete** | ### **se e' trascurabile LO SI DICE** *(e (i) e' un difetto formale)*; ### **se no, e' un POZZO che va curato** |
| ### **`M2`** | ### **il ruolo del VERSO dell'arco:** si invertono `(i,j) -> (j,i)` per ### **TUTTI** gli archi allo stato **BASE** *(e `tw` cambia segno **coerentemente**, se e' definito orientato)*, poi ### **un passo pieno** | se la simulazione cambia ### **oltre la rinumerazione**, ### **il verso dell'arco ENTRA NELLA FISICA** — e si dice ### **DOVE** *(il calcio della mitosi e' il primo sospetto, **non l'unico**)* |

### ⚠ **`M2` APPARTIENE ANCHE A `GEOM-SENZA-VERSO`, e si collega**
Le due voci chiedono ### **la stessa cosa da due lati**: *«un'orientazione arbitraria entra nella
fisica?»*. ### **Si misura UNA volta e si riporta a entrambe.**

### 📐 **E LA MISURA `pos` CONTRO `d` ORA FA PARTE DI QUESTA VOCE**
*(era un passo a se' di `FRAZIONE-DIVISIONE`, e ci resta dentro)*

> ### **Quali leggi leggono `pos` e quali solo `d`?** Cioe': ### **la posizione del figlio e' FISICA
> o solo DISEGNO?**

| | |
|---|---|
| **perche' conta** | se `pos` fosse ### **solo disegno**, `t` conterebbe **solo** per `d`/`d0` — e la decisione su `t` sarebbe ### **una decisione sulla LUNGHEZZA, non sulla posizione** |
| ### **e c'e' un indizio MISURATO** | `SCHW-CORTI`: lo Schwinger prende `dd` ### **da `pos`**, e il **39.06 %** delle coppie accorcia il grafo. ### **Quindi `pos` entra NELLA METRICA almeno in un punto** — ed e' il residuo `A3-DISEGNO` |
| **come si misura** | lo **stesso strumento** della sorveglianza: si intercetta la **lettura** di `pos` e si elenca ### **quali funzioni la leggono**, separando `osservatore`/`disegno` dalle **leggi** *(da `_PASSO_TIPI`, come gia' fatto)* |

### ⚠ **E un collegamento da non perdere:** questa misura ### **risponde anche a `SCHW-CORTI`**
*(«`dd` da `d` o da `pos`?»)*. ### **Le due voci guardano LO STESSO fatto da due lati.**

---

# 🗄 **IL MATERIALE EREDITATO DA `FRAZIONE-DIVISIONE`** *(invariato, e resta valido)*

> ### **Quale grandezza decide `t`? LO DECIDE LUCA.** Qui stanno **solo i criteri**, ### **fissati
> ORA, prima di qualunque numero.**

| | il criterio |
|---|---|
| ### **1 — simmetria** | ### **`f(a,b) = 1 − f(b,a)`.** Scambiando gli estremi il figlio va nella posizione **speculare**. ### **E' la stella polare applicata: la legge e' simmetrica, lo STATO scegle** |
| ### **2 — entrambi i pezzi `>= LAM`** | `t·d >= LAM` **e** `(1−t)·d >= LAM`. ### **Senza questo, una `t` vicina a `0` o a `1` rimetterebbe `M2` ① dalla finestra** |
| ### **3 — nessun coefficiente scelto a mano** | ### **`A1`.** E' il criterio che **archivia `MITOSI_DIR` nella FORMA** |
| **4 — quale grandezza** | ### **decide Luca.** I candidati che lo stato offre: `tw` *(torsione)*, la **densita'**, `psi`, il **tempo proprio** — ### **e non ne propongo uno: la misura viene prima** |

### ⚠ **`MITOSI_DIR` si archivia nella FORMA, ma la sua IDEA e' il primo tentativo di questa voce**

```
bias = 0.5 * np.tanh(MITOSI_DIR * (twn[a] - twn[b]))        # :6981
```

### ➜ **L'IDEA e' giusta e va citata qui:** *«il figlio nasce spostato verso l'estremo con piu'
torsione»* ### **e' esattamente `t = f(stato_a, stato_b)` con la torsione come grandezza.**
### ⛔ **La FORMA no:** un ### **coefficiente scelto** *(`MITOSI_DIR`)* davanti a una `tanh`
### **scelta**, e per di piu' con `0.5 *` davanti — ### **tre numeri a mano**.
### **Si archivia la forma, si conserva l'idea.** *(Ed e' la ragione per cui `MITOSI_DIR` esce al
commit 0 ma la sua riga **vive qui**.)*

### ⚠ **E LA MISURA `pos`/`d` E' SALITA IN TESTA ALLA VOCE** *(qui sopra)*: non e' piu' «il primo
passo di `FRAZIONE-DIVISIONE`», e' ### **una delle misure di `DIVISIONE-AUTOCONSISTENTE`** — perche'
`t` non decide piu' **soltanto** una posizione, decide anche ### **come si spartisce una carica.**

---

# ✅ **Che cosa questo piano NON promette**

| | |
|---|---|
| **non promette meno codice** | promette ### **UN POSTO SOLO**. Le 549 righe possono restare 549: ### **il numero che conta e' «3 posti → 1»** |
| **non cura le 12 toppe** | ne ### **DICHIARA** cinque *(la soglia, il `0.3`, i pavimenti, `MITOSI_DIR`, `MITMAX`)* e ne **toglie** due per costruzione *(la riallocazione di `_rep`, la mutazione di `conc_nodi`)*. ### **Le altre restano, con la loro domanda** |
| ### **non toglie la finestra DENTRO una voce** | il controllo unico guarda **i confini**. ### **Dentro `mitosi` la finestra resta** — e il riordino la **riduce** *(un posto solo invece di tre)* **senza chiuderla** |
| ### **e non e' una misura** | e' un **piano**. ### **Ogni numero che contiene e' gia' stato misurato e committato**, e ogni numero che non c'e' ### **e' un criterio, non una previsione** |
