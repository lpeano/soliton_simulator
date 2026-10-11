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
