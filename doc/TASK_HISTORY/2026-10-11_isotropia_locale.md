# L'ISOTROPIA LOCALE — **si attenua con la distanza? e si riduce costruendo meglio?** *(mandato di Luca, `2026-10-11`)*

> ### ⛔ **QUESTO FILE SI COMMITTA E SI PUSHA *PRIMA* DELLE MISURE** *(par. `8`)*, cosi'
> l'ordine e' **verificabile da git**. ### **E' una task history NUOVA, non un'annotazione
> di quella del `LEGAME`**, e il mandato lo permette *(«annotazione della task history del
> `LEGAME` o una nuova, dichiarandolo»)*: ### **lo dichiaro qui.**

### ✅ **IL CONTROLLO DI IDEMPOTENZA, FATTO PER PRIMO**

| | che cosa ho cercato | c'era? |
|---|---|---|
| `a` | `doc/TASK_HISTORY/*isotropia_locale*` | ### **NO** |
| `b` | `proto_camminata/uscite/letture_isotropia_locale.json` | ### **NO** |
| `c` | le varianti `(ii)`, `(iii)`, `(iv)` in `scene3d.py` | ### **NESSUNA** — c'e' solo la `(i)` *(`geometrico3d`, punti uniformi, gradi `[2, 6]`)* |
| `d` | le voci che il mandato cita | `ISOTROPIA-LOCALE`, `GRAFO-PESATO-TUTTI-I-VICINI`, `DOMANDA-PESO-ARCO-COME-MEMORIA`, `DOMANDA-QUALE-SCENA-3D-PRINCIPALE` — ### **tutte e quattro CI SONO** |
| `e` | la misura dell'isotropia col **profilo medio** | ### **NO**: `scene3d.isotropia` media le dispersioni **per nodo**, ed e' il difetto che la correzione del guardiano ha trovato |

### ✅ **E SI RIUSA CIO' CHE REGGE** *(il mandato lo chiede)*: `scene3d.py` ha gia' il
**cubico periodico**, il **geometrico periodico con le posizioni scartate**, la
**dimensione spettrale** e i **due misurandi** *(grafo ed euclideo)* coi **due bracci sui
versori**. ### **Quello che manca e' il PROFILO MEDIO, il rumore atteso, le tre varianti e
la dipendenza da `t`.**

---

## 1. LA MATEMATICA DEL GROVER PESATO, **VERIFICATA PRIMA DI DERIVARLA**

> ### ⛔ **Un regalo non verificato e' un debito**, e qui il regalo e' la forma che Luca
> propone. ### **I numeri sono misurati sul codice, non ricopiati.**

`G_w = 2 |w⟩⟨w| / ⟨w|w⟩ − I` con `w_a = sqrt(peso dell'arco dell'uscita a)`, **a blocchi per
nodo**.

| | la proprieta' | misurato |
|---|---|---|
| `a` | **REALE** *(e quindi `C` regge)* | `max\|Im M\|` = **`0`** |
| `b` | **ERMITIANA** | `max\|M - M^dag\|` = **`0`** *(pesi uguali)*, **`1.11e-16`** *(casuali)* |
| `c` | **INVOLUZIONE** | `max\|M² - I\|` = **`2.22e-16`** .. **`4.44e-16`** |
| `d` | **UNITARIA** | `max\|M^dag M - I\|` = **`2.22e-16`** .. **`4.54e-16`** |
| `e` | **LOCALE** | elementi fra nodi diversi: ### **`0` ESATTO** |
| `f` | **a pesi UGUALI = il Grover del `v3`** | ### ⭐ **`0`, AL BIT** |
| `g` | **un peso NULLO stacca l'uscita** | la sua colonna ha ### **UN SOLO** elemento, e la diagonale e' ### **`−1`**: l'ampiezza **torna indietro**, e ### **nessun'altra uscita le manda niente** |
| `h` | **la `C`** | `max\|C G_w − G_w C\|` = **`0`** con pesi uguali ### **E** con pesi casuali |

### ⭐ **E IL PUNTO `(f)` E' MEGLIO DI QUANTO SPERASSI: `0` AL BIT, senza cortocircuito.**
### **La famiglia frazionaria del `v4` ne aveva bisogno** *(dava `2e-16`)*; qui
`(2/d)Σ − I` e `2(Σ w)/⟨w|w⟩ − I` con `w ≡ 1` ### **danno gli stessi byte**, perche'
`⟨w|w⟩ = d` e la divisione e' la stessa. ### ✅ **Quindi `W1` e' soddisfatto senza un ramo
speciale.**

### ⚠ **E NESSUNA COSTANTE NUOVA, e si dichiara DOVE:** i pesi entrano ### **solo come
rapporti dentro il nodo** *(`w/⟨w|w⟩`)*, quindi ### **moltiplicare tutti i pesi di un nodo
per la stessa costante non cambia niente** — e questo si misura *(un braccio del collaudo)*.

---

## 2. ⛔ **IL FATTO CHE CAMBIA IL QUADRO: LA DELAUNAY `3D` HA GRADO MEDIO `15.5`, NON `2..6`**

| `N` | archi | **gradi** | media | vicini comuni per arco *(min / mediana / max)* |
|---|---|---|---|---|
| `200` | `1556` | **`9..23`** | **`15.6`** | **`3`** / `6` / `11` |
| `1000` | `7750` | **`6..26`** | **`15.5`** | **`3`** / `6` / `13` |

### ⛔ **QUINDI LA VARIANTE `(iv)` NON AGGIUNGE SOLO PESI: TRIPLICA IL GRADO.** La scena
attuale ha gradi `2..6` *(media `5.8`)*; la Delaunay ne ha ### **`15.5`** — e
### **`m` passa da `~2.9 n` a `~7.8 n`**, cioe' lo spazio di stato ### **quasi triplica.**

### ⚠ **E IL MANDATO LO AVVERTE, ed e' esattamente questo:** *«cambiare l'intervallo dei
gradi CAMBIA LA FISICA LOCALE, perche' Grover dipende dal grado»*. ### **Quindi `(iv)` non
e' <<la stessa scena con dei pesi>>: e' una scena DIVERSA**, e il confronto con `(i)`,
`(ii)` e `(iii)` ### **va letto sapendolo.**

### ✅ **E UNA COSA BUONA, misurata:** i **vicini comuni** per arco sono ### **almeno `3`**
su entrambe le taglie, quindi il peso relazionale `w_ij = |N(i) ∩ N(j)|` ### **non e' mai
zero** — ### **nessun arco si stacca per caso.**

### **I TRE BRACCI DEI PESI, come il mandato li vuole**

| | il peso | legge le posizioni? |
|---|---|---|
| `iv-U` | **tutti `1`** — ### **il RIFERIMENTO** | ### ✅ **no** |
| `iv-R` | **RELAZIONALI**, due forme senza costanti: `w_ij = \|N(i) ∩ N(j)\|` *(i vicini comuni, cioe' i triangoli che contengono l'arco)* e `w_ij = \|N(i) ∩ N(j)\| / sqrt(d_i d_j)` *(lo stesso, normalizzato sui gradi)* | ### ✅ **no**, e ### **un braccio sul SORGENTE lo verifica** |
| `iv-V` | **VORONOI**, controllo dichiarato *«geometria a mano»*: area della faccia / distanza | ### ⛔ **SI'**, ed e' il motivo per cui ### **non puo' diventare il riferimento** |

### ⚠ **E UNA DIPENDENZA NUOVA, DICHIARATA: `scipy.spatial`.** Il repo ### **non usa `scipy`
in nessun file** *(verificato con un `grep` su `csv/`, `primo_ordine/` e
`proto_camminata/`)*, e la Delaunay periodica la vuole. ### ⛔ **Entra SOLO nel COSTRUTTORE
DI SCENA**, cioe' in una ### **condizione iniziale**, e ### **mai nel passo** — un braccio
del collaudo lo verifica sul sorgente.

---

## 3. RAGIONAMENTO PRELIMINARE — **cosa credo, e cosa NON SO**

| | quello che credo | perche' |
|---|---|---|
| `c1` | ### **l'irregolarita' locale CALA con `t`, e poi si APPIATTISCE su un pavimento** | il volume entro `r` cresce come `r³` in `3D`, quindi mediare su `~t³` nodi riduce la parte **statistica** come `t^(-3/2)`; ma ### **lo sbilanciamento del nodo di PARTENZA non si media**, e quello resta |
| `c2` | ### **il pavimento e' dell'ordine dello sbilanciamento misurato** *(`0.351`)*, diviso qualcosa | e' la parte che ### **non ha altri nodi su cui mediarsi** |
| `c3` | ### **sul cubico l'anisotropia del PROFILO MEDIO resta sopra il rumore a ogni `t`** | e' ### **sistematica**: le direzioni degli assi sono privilegiate dal reticolo, e mediare su molti nodi ### **non la cancella** perche' tutti i nodi hanno gli stessi assi |
| `c4` | ### **sul geometrico il profilo medio SCENDE al livello del rumore** | i vicinati sono ### **orientati a caso**, quindi mediando su molti nodi ### **nessuna direzione resta privilegiata** |
| `c5` | ### **`(iii)` gradi meno variabili aiuta piu' di `(ii)` punti piu' uniformi** | lo sbilanciamento viene da ### **quali vicini si collegano**, e il tetto di grado ne taglia il `20%` — mentre punti piu' uniformi ### **non cambiano il tetto** |

### ⛔ **COSA NON SO**

| | |
|---|---|
| `n1` | se il pavimento di `c1` sia ### **misurabile** entro `t <= 30` o se serva piu' tempo del bordo |
| `n2` | se `(iv-R)` si avvicini a `(iv-V)`: e' ### **la domanda chiave del mandato**, e non ho un'intuizione |
| `n3` | se il grado `15.5` della Delaunay ### **da solo** riduca l'irregolarita' *(piu' vicini = piu' media)*, indipendentemente dai pesi — ### **e il braccio `(iv-U)` lo isola** |

---

## 4. LE SOGLIE E LE PREVISIONI, **fissate ADESSO**

| | la domanda | la soglia | la previsione |
|---|---|---|---|
| `s1` | **l'ANISOTROPIA** *(dispersione del profilo MEDIO)* | significativa se ### **`> 3 ×` il rumore atteso**, con il rumore = *dispersione per nodo / sqrt(numero di nodi)* | ### **cubico: SOPRA** · ### **geometrico: AL LIVELLO** |
| `s2` | **l'IRREGOLARITA' si attenua?** | si adatta `log(irregolarita')` contro `log t` e si riporta `a` con la sua `sigma`: ### **<<si attenua>> se `a > 3 sigma_a`**, ### **<<resta piatta>> se `\|a\| <= 3 sigma_a`** | ### **cala, con `a` fra `0.5` e `1.5`**, e ### **poi si appiattisce** |
| `s3` | **c'e' un PAVIMENTO?** | gli ultimi due `t` differiscono di ### **meno di `3 sigma`** | ### **si'**, ed e' la parte strutturale |
| `s4` | **il fronte non fa il giro** | `t * v_fronte <= diametro/2`, con `v_fronte = 0.6193` **misurato** ⟹ `t_max = diametro/(2 × 0.6193)` | — |
| `s5` | **la dimensione resta `~3`?** | `\|d_s − 3\| <= 0.3` su ogni variante | ### **si'** per tutte |
| `s6` | **`(iv-U)` e `(iv-R)` si avvicinano a `(iv-V)`?** | si riporta ### **la frazione del guadagno** di `(iv-V)` che `(iv-U)` e `(iv-R)` ottengono: `(x − x_i) / (x_V − x_i)` con `x_i` la variante `(i)` | ### **non lo so** *(`n2`)* |
| `s7` | **la CORRELAZIONE fra sbilanciamento e irregolarita'** | il coefficiente di Pearson per nodo, con la sua `sigma`: ### **significativo se `> 3 sigma`** | ### **positiva e significativa**: e' l'ipotesi che lo sbilanciamento SIA la causa |

### ⛔ **E IL VINCOLO CHE NON SI TOCCA:** le posizioni servono ### **solo a costruire gli
archi e a LEGGERE** *(osservatore)*, ### **mai alla dinamica** — e il collaudo lo verifica
### **sul sorgente** *(`[[DOMANDA-D9-GEOMETRIA]]`, `A17`)*.

---

## 5. TODO DEL NEXT STEP

| | il passo | cosa decide |
|---|---|---|
| `1` | committare e pushare **questo file** | l'ordine verificabile da git |
| `2` | `scene3d.isotropia`: aggiungere il ### **PROFILO MEDIO** e il ### **RUMORE ATTESO**, e le ### **TRE grandezze** | la correzione del guardiano |
| `3` | le varianti `(ii)` *(Lloyd sul toro)* e `(iii)` *(gradi `[4, 6]`)* | `I2` |
| `4` | `delaunay4.py`: la Delaunay periodica, i ### **tre bracci dei pesi**, e il ### **Grover pesato** | la variante `(iv)` |
| `5` | `_letture_isotropia_locale.py` → `uscite/letture_isotropia_locale.json` | `I1` e `I2` |
| `6` | i bracci nel banco: cubico ### **sopra il rumore a ogni `t`**, pesi uguali ### **`= v3` al bit**, la `C` col Grover pesato, e ### **le posizioni non entrano** | il collaudo |
| `7` | la sezione nel referto, le voci, e `[[DOMANDA-QUALE-SCENA-3D-PRINCIPALE]]` aggiornata col confronto | la registrazione |

### ⛔ **E LA COSA CHE NON FARO': SCEGLIERE LA SCENA.** Il grado `15.5` della Delaunay
### **cambia la fisica locale**, e il mandato lo dice: ### **la scelta fra le varianti e' di
Luca.**

---

## ⭐ **ANNOTAZIONE: L'AGGIUNTA DI LUCA — IL COMPROMESSO POTREBBE ESSERE TAGLIA FINITA** *(`2026-10-11`, a `I1` e `I2` GIA' MISURATE: quindi si **ANNOTA**, e niente qui sopra si riscrive)*

### ⛔ **E IL RILIEVO E' GIUSTO, E L'ARGOMENTO STA NEI MIEI NUMERI:** ho confrontato ### **tutte le varianti a `n = 1728`**, e ### **la stessa `(i)` passa da `d_s = 2.578` a `n = 1728` a `d_s = 2.92` a `n = 4000`.** ### ⭐ **Quindi <<`(ii)` ha `d_s = 2.83`>> non dice che `(ii)` NON e' tridimensionale: dice che ### **a `n = 1728` NESSUNA scena geometrica lo e' ancora.** ### ⚠ **E questo e' il mio errore di presentazione:** ho messo in tabella un compromesso ### **confrontando una grandezza che SO dipendere dalla taglia**, senza la colonna della taglia che varia — ed e' lo stesso difetto che il mandato del legame chiama ### **`TAGLIA-FINITA`.**

### **E LE TRE MISURE CHE CHIEDE:**

| | che cosa | perche'|
|---|---|---|
| `M-A` | `d_s` di `(i)`, `(ii)` e `(iv-U)` a ### **`n = 4000`, `10000`, `26000`** | ### **`(ii)` tende a `3` crescendo la taglia?** |
| `M-B` | ### **LA COMBINAZIONE `(ii)+(iv-U)`** *(punti respinti **+** Delaunay **+** pesi uguali)*, con ### **tutte** le misure delle altre varianti | i due effetti ### **si SOMMANO** o ### **si SOVRAPPONGONO**? |
| `M-C` | il ### **PAVIMENTO di `(ii)`** a taglia grande, come per `(i)` a `n = 26000` | il pavimento scende sotto lo ### **`0.17`** di `(i)`? |

### ⭐ **LE SOGLIE, SCRITTE PRIMA DI GUARDARE** *(e il numero continua la serie di sopra)*

| | che cosa decide | la soglia, FISSATA ORA | la mia previsione |
|---|---|---|---|
| `s8` | **`(ii)` tende a `3`?** | `d_s` ### **cresce in modo monotono** con `n` ### **E** a `n = 26000` vale `|d_s - 3| <= 0.3` | ### **si'** — a parita' di taglia `(ii)` sta ### **sopra** `(i)` *(`2.83` contro `2.58`)*, quindi se `(i)` arriva a `3` ### **`(ii)` ci arriva prima** |
| `s9` | **chi e' la piu' tridimensionale a taglia grande** | si confronta ### **`|d_s - 3|` a `n = 26000`**, non `d_s` — ### **perche' SOPRA `3` e' un difetto come sotto** | ### **`(iv-U)` PEGGIORA**: a `1728` sta ### **gia' a `3.25`**, e se `d_s` cresce con `n` va ### **oltre** — e ### **un grafo con `d_s > 3` non e' uno spazio `3D`** |
| `s10` | **i due effetti si SOMMANO?** | il guadagno di `(ii)+(iv-U)` contro `(i)` confrontato con la ### **SOMMA dei due guadagni separati**, entro `3 sigma` | ### **NO, si sovrappongono:** entrambi riducono ### **la stessa cosa** *(l'irregolarita' del vicinato)*, quindi prevedo il guadagno ### **fra il massimo dei due e la loro somma** |
| `s11` | **il pavimento di `(ii)` scende?** | il pavimento di `(ii)` sotto quello di `(i)` *(`0.1700 ± 0.0071`)* di ### **piu' di `3 sigma`** | ### **si'** — a `t = 10` `(ii)` sta ### **`42%` sotto**, e non vedo perche' il pavimento sia comune |
| `s12` | **e' la STESSA legge di attenuazione?** | l'esponente di `(ii)` contro quello di `(i)` *(`-0.339 ± 0.033`)*, entro `3 sigma` | ### **si'** — prevedo che cambi ### **solo il prefattore**, perche' l'attenuazione viene dalla ### **media su piu' archi**, che e' geometria del fronte e ### **non della scena** |

### ⛔ **E UNA COSA CHE NON CAMBIA: NESSUNA VARIANTE DIVENTA LA SCENA DI DEFAULT.** La combinazione `(ii)+(iv-U)` e' ### **una variante in piu' da misurare**, non una promozione — e il grado della Delaunay ### **cambia la fisica locale** *(Grover dipende dal grado)*: ### **la scelta resta di Luca.**

### ⚠ **E IL LIMITE DI COSTO, dichiarato ORA:** la Delaunay periodica a `n = 26000` costruisce ### **`27 n` punti** *(le copie del toro)*, e il `d_s` a `n = 26000` costa ### **una camminata classica fino al diametro.** ### **Se una taglia sfora, si DICHIARA e si ferma alla precedente** — ### **senza ridurre la precisione**, come il mandato del legame ha gia' stabilito.

