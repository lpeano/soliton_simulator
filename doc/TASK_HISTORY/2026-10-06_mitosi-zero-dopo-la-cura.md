# TASK HISTORY — **il `0.3` a ZERO dopo la cura, DOVE cresce la rete, e il CIRCOLO del dipolo**

*(Mandato di Luca del 2026-10-06, che **sostituisce** quelli precedenti sul test del `0.3` a
zero.)*

> ### ⛔ **NESSUNA CORSA ERA PARTITA su quel test, quindi non c'era niente da preservare**, e
> lo scrivo perche' il mandato chiedeva di non fermare una corsa in volo. ### **E questo file
> non era ancora committato quando il mandato e' stato sostituito:** l'ho ### **riscritto**,
> non annotato, e il `par.8` *(«non si riscrive quando si rivela sbagliato»)* parla di un
> ragionamento ### **smentito dai fatti**, non di una bozza su disco che nessun commit ha
> ancora visto. ### **La versione precedente non esiste in git, e dirlo e' la cosa onesta.**

> ### ⛔ **QUESTO FILE SI COMMITTA DA SOLO E PRIMA DELLO STRUMENTO**, cosi' l'ordine e'
> ### **verificabile da git** *(il suo commit e' ANTENATO di quelli del lavoro)* invece che
> asserito da me.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare, e cosa NON so*

### LE TRE DOMANDE, come le ha poste Luca

1. **Con la legge della torsione curata, la crescita e' del MODELLO o dipende ancora dal
   `0.3`?**
2. **DOVE cresce la rete** — nella materia, nel vuoto, o sul ### **bordo** delle masse? La
   misura lunga ### **non lo registra**, e la risposta decide se l'accelerazione *(`267`,
   `333`, `362`, `398` nascite per finestra)* e' ### **lo spazio che si espande** o
   ### **la materia che prolifera.**
3. **Perche' accelera** — l'ipotesi del ### **basculamento chirale.**

Nella misura lunga *(`b544d5a`)* il `0.3` di `MITOSI-SOGLIA-GRAD` e' ### **acceso**, e le
`3496` divisioni possono dipendere da lui. Con la legge ### **vecchia** togliere il `0.3`
portava le divisioni a ### **`2`** *(`d97317a`)* — ma quella legge aveva ### **il calcio di
nascita**, che e' precisamente cio' che la cura ha tolto.

### I FATTI DAL CODICE, **letti adesso e non assunti** *(`CLAUDE.md` par.2: dal sorgente, non dai commenti)*

| il fatto | dove, e che cosa dice |
|---|---|
| la soglia modulata | `soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))`. ### **`_AMP = 0` la rende `soglia0` su ogni arco**, e `soglia0` e' `3π` |
| `twist_dip` | `np.pi * 0.5 * (chi_torsione[i] - chi_torsione[j])` *(`:7864`, ramo `POLO_MATURO = False`)*. Con `chi ∈ {-1,+1}` sta in ### **`{-π, 0, +π}`** |
| `chi_torsione` | con `CHI_CORE = False` e `CHI_COOP = False` e' ### **`perc_chi`** *(`:7855`)* |
| il basculamento | `perc_chi[:n] = np.where(twn > PHI_CRIT, 1, -1)` *(`:7908`)*, con `twn` la ### **media di `|tw|` sugli archi del nodo** e `PHI_CRIT = 2π` *(`:567`)* |
| ### ⚠ **e NON e' un <<ribaltamento>>** | `perc_chi` e' ### **RICALCOLATO DA ZERO a ogni passo.** Un nodo *«cambia»* quando ### **attraversa** la soglia, ### **in un verso o nell'altro** |
| ### ⚠ **l'ordine dentro il passo** | la torsione sta a `:7884`, il basculamento a `:7897`: la torsione usa il `perc_chi` del ### **passo prima**, e il basculamento legge `_tw_t`, il `tw` di ### **INIZIO passo** *(`:7502`)*. ### **Sfasamento di un passo, e va dichiarato nel referto** |
| il calcio ai genitori | `calcio_a = comune + 0.5*KICK_TW*sciolta*chi_a*mod`, con `sciolta = |tw[sel]|/2π`, `mod = tau/(1+tau) ∈ (0.5, 1)` *(`:8839`)* |
| ### ⛔ **`KICK_TW = 0.35`, NON `~0.5`** | `:617`. ### **Il mandato dice <<~0.5 rad dal codice>>; il codice dice `0.35`**, e con `sciolta ~ 0.6` il calcio atteso e' dell'ordine di ### **`0.2` rad.** ### **Lo misuro invece di assumerlo**, e correggo il numero qui perche' chi legge non lo riprenda |
| ### ⛔ **`rho_spin` NON e' `|ψ|²`** | `:1057` registra come ### **DIFETTO** un `_rho_sorgente` che restituiva `|ψ|²` ### **invece di** `rho_spin`. ### **Il mandato chiede <<la densita' `|ψ|²`>>: REGISTRO ENTRAMBE**, perche' sceglierne una in silenzio rifarebbe quel difetto |
| il tempo proprio | `ritmo()` = `cs_nodo / CS_M`, ### **in `(0, 1]`** *(`:5355`)*. La mitosi legge `_r_nodo_mitosi()`, che e' ### **la stessa grandezza** messa in cache, con fallback `1` e ### **quattro contatori `A8`** |

> ### ✔ **IL MECCANISMO DELL'IPOTESI DEL GUARDIANO E' ESATTO NEL CODICE**, e questo si puo'
> dire ### **prima** di misurare: un nodo che attraversa `2π` cambia `perc_chi[i]`, quindi
> `twist_dip` di ### **TUTTI i suoi archi** cambia di `±π` in un colpo, e la legge
> ### **CURATA** somma il dipolo ### **come VARIAZIONE** `(twist_dip - _dp)` — quindi quel
> `±π` ### **entra in `tw` interamente, in un passo solo.**
>
> ### ⛔ **MA <<IL MECCANISMO ESISTE>> NON E' <<IL MECCANISMO DOMINA>>**, e la differenza e'
> tutto il contenuto di questa misura.

### LA GEOMETRIA DELLA SCENA, **letta da `_semina_masse_coerenti` e non assunta** *(`:9928`)*

| | |
|---|--:|
| `LAM` | `0.800000` |
| `R_CONN = 3·LAM` | `2.400000` |
| `sep` *(dall'argv del driver)* | `6.115800` |
| ### **`r_regione = 0.5·(sep·√3 − R_CONN)`** | ### **`4.096438`** |
| `raggio_vuoto = sep + r + R_CONN` | `12.612238` |

**E le tre regioni la scena le definisce come COORTI DI INDICI:** i nodi con
`|pos − c_k| <= r_regione`, con `c_k = sep·(cos 2πk/3, sin 2πk/3, 0)`, registrati in
`test["dati"]["coorti"]["massa_k"]`. ### **Non sono masse SEMINATE** — il codice lo dice
esplicitamente e non tocca `conc_nodi`.

### ⛔ LA CLASSE A TRE VALORI, **fissata QUI e DERIVATA, non scelta** *(`A1`: la legge, non il numero)*

Sia `u = min_k |pos − centro_k(t)| / r_regione`, dove ### **`centro_k(t)` e' il BARICENTRO
della coorte `k` al passo corrente** *(la scena definisce la regione come la sua coorte, e
### **le masse possono muoversi** — e' la prima delle tre prove di Luca)* e `r_regione` resta
### **quello della scena.**

| classe | la regola | il perche' e' DERIVATA |
|---|---|---|
| **MATERIA** | `u <= 1` | ### **e' il test di appartenenza DELLA SCENA**, verbatim |
| **BORDO** | `1 < u <= 1 + R_CONN/r_regione = `### **`1.5859`** | ### **`R_CONN` e' il VARCO della scena**: la lunghezza con cui garantisce che le superfici non si tocchino. ### **Un raggio di connessione oltre la superficie e' <<il bordo>>** |
| **VUOTO** | `u > 1.5859` | il resto |

> ### ✔ **ZERO NUMERI NUOVI:** `r_regione` e `R_CONN` sono ### **gia' nella scena**, e il
> rapporto fra i due non e' una manopola.
>
> ### ⚠ **E DICHIARO UN LIMITE DELLA GEOMETRIA, prima di misurare:** i ### **gusci** del
> bordo ### **SI SOVRAPPONGONO** *(raggio esterno `1.5859·r = 6.497` dai centri, che distano
> `sep·√3 = 10.595`: `2 × 6.497 > 10.595`)*. Le ### **palle** della materia no *(`2r = 8.19 <
> 10.595`)*. Quindi una stima a volume uniforme ### **sovrastimerebbe il BORDO**
> *(`0.1028` / `0.3072` / `0.5900` per materia/bordo/vuoto, ### **non additiva**)*.
> ### **Per questo le frazioni di NODI si MISURANO e non si assumono** — ed e' anche la
> ragione per cui il criterio confronta la frazione di ### **nascite** con quella di
> ### **nodi**, non con una frazione di volume.

### QUELLO CHE HO GIA' IN MANO, dal `lunga.json` *(e che uso per prevedere, invece di andare a sentimento)*

| passo | `g1_sopra_soglia` | `g1 ∧ g2` | `g1∧g2∧g3` | `g4_nasce` |
|--:|--:|--:|--:|--:|
| `100` | `0` | `0` | `0` | `0` |
| `200` | `2` | `2` | `2` | `0` |
| `214` | `106` | `106` | `93` | `1` |
| `500` | `906` | `903` | `793` | `3` |
| `1000` | ### **`2397`** | `2033` | `1776` | `13` |

Quantili di `|tw|` all'ultimo passo: `q25 = 2.0701`, `q50 = 3.9151`, `q75 = 5.3748`,
`q95 = 6.5578`, `q99 = 7.9269`, ### **massimo `75.9216`.** E `spinta_oltre_pi = 2960`
all'ultimo passo, con la spinta per passo a `q95 = 0.1521` e `q99 = 2.9811`.

> ### ✔ **DUE CONTI CHE ORIENTANO LA PREVISIONE:**
>
> 1. **la soglia NON modulata e' `3π = 9.4248`**, e `q99 = 7.9269` sta ### **sotto**: con
>    `_AMP = 0` passa il cancello `1` ### **meno dell'`1 %`** degli archi;
> 2. **ma non ZERO:** `2397 − 2033 = 364` archi falliscono il cancello `2` *(`avv < 4π`)*, e
>    gli archi sopra `4π` sono `368`. ### **Fra `3π` e l'infinito c'e' una popolazione VERA**,
>    e con la soglia piatta ### **qualcosa passa.**
>
> ### ⛔ **E QUESTO E' DIVERSO DALLA LEGGE VECCHIA:** li' il `|tw|` mediano era `2.11` con
> `~108` archi ### **incollati** sopra `4π` e nulla in mezzo — il serbatoio fra `3π` e `4π`
> era ### **vuoto**, ### **ecco perche' toglierlo portava le divisioni a `2`.** Con la legge
> curata la distribuzione e' ### **larga**, e il serbatoio ### **non e' vuoto.**

### COSA NON SO, **e lo scrivo prima**

1. ### ⛔ **I DUE BRACCI NON SONO <<LO STESSO SISTEMA MENO UN EFFETTO>>:** togliere la
   modulazione cambia la traiettoria dal primo passo in cui un arco sfiora la soglia, e da li'
   le due reti ### **divergono.** `R` confronta ### **due traiettorie diverse.**
2. **non so separare <<il dipolo CAUSA le nascite>> da <<le nascite causano il dipolo>>:** il
   basculamento dipende da `|tw|`, che le nascite alterano col calcio e con gli archi nuovi.
   ### **Una correlazione per passo NON e' un verso**, e il mandato ne chiede una.
   ### **La riportero' dichiarando che il verso non lo decide.**
3. **non so se `1000` passi bastino:** nella misura lunga gli archi oltre `4π` crescono
   ### **fino all'ultimo passo.** Se col `0.3` a zero la rete partisse piu' tardi, `1000`
   passi la coglierebbero ### **ancora nel transitorio**, e un `R` piccolo direbbe
   ### **<<piu' tardi>> invece di <<meno>>.**
4. **sul DOVE non so quasi niente**, e questa e' la domanda ### **nuova**: la misura lunga non
   registra posizioni, quindi ### **non ho un solo dato** su cui appoggiarmi. ### **E' l'unica
   delle tre domande su cui non posso prevedere con un conto.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi farebbe FERMARE*

### I DUE BRACCI, **in processi SEPARATI** *(lo chiede il mandato)*

| braccio | `_AMP` | passi | perche' |
|---|--:|--:|---|
| **A** | `0.0` | `1000` | la domanda `1` |
| **B** | `0.3` | `1000` | ### **le registrazioni dei punti `D` ed `E` NON esistono nella misura lunga**, quindi il confronto le vuole in un braccio ### **acceso che le abbia** |

> ### ⚠ **E IL BRACCIO `B` NON SOSTITUISCE LA MISURA LUNGA: deve RIPRODURLA**, ed e' `C0`.
> Se non la riproducesse, ### **il confronto fra i bracci non varrebbe niente**, perche' non
> saprei se la differenza viene da `_AMP` o dal mio strumento.

### LE REGISTRAZIONI, a OGNI passo

**PUNTO `D` — perche' accelera:**

1. **nodi che cambiano `perc_chi`** — gancio ### **di sola lettura** al basculamento: il
   gancio ricalcola `where(twn > 2π, 1, -1)` e lo confronta col `perc_chi` corrente.
   ### **La riga del simulatore non si tocca.**
2. **archi con `|spinta| > π`, divisi per SORGENTE** — la legge curata somma
   `_w4(dph − _fp) + (twist_dip − _dp)`, quindi le due parti ### **sono separate per
   costruzione**: fase `|_w4(dph − _fp)| > π`, dipolo `|twist_dip − _dp| > 0`, ### **ed
   entrambe.**
3. **`Σ |Δdipolo|`** su tutti gli archi.
4. **nascite e `Σ |calcio|` ai genitori** — gancio al sito di `KICK_TW`.

**PUNTO `E` — dove:** per ### **ogni nascita** *(divisione e Schwinger ### **separate**)*, per
### **ogni nodo che cambia chiralita'**, e ai passi `300`, `600`, `1000` per gli archi con
`|tw| >= 4π` ### **come POPOLAZIONE** *(distribuzioni, mai indici)*:

- `|ψ|²` ### **e** `rho_spin` del nodo, ### **divisi per la mediana della rete**;
- il tempo proprio `ritmo()` del nodo;
- `u`, la distanza dal baricentro della coorte piu' vicina ### **in unita' di `r_regione`**;
- la ### **classe** `MATERIA` / `BORDO` / `VUOTO`.

E per finestre di `100` passi: la frazione di nascite in ciascuna classe ### **contro la
frazione di NODI della rete in quella classe** — ### **altrimenti <<nascono nel vuoto>>
direbbe solo <<il vuoto e' piu' grande>>**, e il mandato lo dice esplicitamente.

> ### ⛔ **E GLI INDICI DEGLI ARCHI OLTRE `4π` NON SI GUARDANO:** `ARCHI-OLTRE-4PI` e'
> ### **<<da non indagare>> per decisione di Luca.** ### **Conto le popolazioni, non gli
> individui.**

### I CONTROLLI, e che cosa decide ciascuno

| id | che cosa pretende | che cosa decide |
|---|---|---|
| **`C0`** | `_AMP = 0.3` riproduce ### **ESATTAMENTE** i conteggi per passo della misura lunga *(`n`, archi, divisioni, Schwinger, quantili di `|tw|`)* ### **su TUTTI i passi registrati da entrambi** | che il mio strumento ### **non abbia cambiato il sistema.** Se fallisce, ### **MI FERMO** |
| **`C-fallisce`** | il braccio `_AMP = 0` ### **DEVE DIFFERIRE**, e il referto riporta ### **il primo passo in cui succede** | che la patch ### **faccia qualcosa.** Se non differisse, `_AMP` sarebbe ### **inerte** e la misura un falso-zero |
| **`C1`** | `divisioni + Schwinger == nati`, e `n` cresce ### **esattamente** di quanto dicono i nati | che i conteggi siano ### **la grandezza del simulatore** e non una mia ricostruzione |
| **`C-letture`** | ### **i ganci sono di SOLA LETTURA:** la copia ### **con** i ganci riproduce ### **AL BIT** i conteggi della copia ### **senza** ganci sui primi `150` passi | che le registrazioni nuove ### **non abbiano cambiato la misura.** ### **E' il controllo che `C0` da solo non da'**, perche' `C0` confronta col `json` di uno strumento che ### **aveva gia' due ganci** |

> ### ⛔ **COSA MI FA FERMARE, deciso adesso:** `C0` che fallisce · `C-letture` che fallisce ·
> un blob del simulatore diverso da `cf2a1ac8` · `C1` che non torna · una caduta che non salva
> i dati. ### **In tutti i casi committo il fallimento e mi fermo, e la correzione e' un
> commit a se'.**

### ⛔ I CRITERI, **fissati QUI, prima della corsa** *(dettati da Luca)*

**① SU `R = divisioni(_AMP = 0) / divisioni(_AMP = 0.3)`** a `1000` passi, letto ### **anche**
su `Σ (g1 ∧ g2 ∧ g3)`:

| `R` | la lettura |
|---|---|
| ### **`>= 0.5`** | *«la crescita e' del MODELLO; il `0.3` la anticipa o la accelera, ma ### **non la crea**»* |
| ### **`<= 0.1`** | *«la crescita ### **dipende ancora** dal `0.3`»* |
| fra `0.1` e `0.5` | ### **intermedia** |

Accanto a `R`: ### **il passo della prima nascita nei due bracci**, le nascite per finestre di
`50` passi, e ### **il fatto che il braccio acceso cresce ACCELERANDO** *(misurato: `267`,
`333`, `362`, `398` nelle ultime quattro finestre)*.

**② SULL'IPOTESI DEL DIPOLO:**

| | |
|---|---|
| ### **CONFERMATA** | almeno il ### **`70 %`** degli archi con spinta oltre `π` ha la componente di dipolo ### **non nulla**, ### **E** la correlazione per passo fra cambi di chiralita' e archi oltre `4π` e' ### **`>= 0.5`** |
| ### **REFUTATA** | quella frazione e' ### **sotto il `30 %`** |
| intermedia | il resto |

> ### ⚠ **LA CONGIUNZIONE DELLA PRIMA RIGA E' UNA <<E>>, NON UNA <<O>>:** basta che una delle
> due manchi perche' non sia confermata. ### **Lo scrivo perche' a corsa finita sarebbe comodo
> leggerla come una <<o>>.**

**③ SUL DOVE:** una classe si dice ### **SOVRARAPPRESENTATA** se la sua frazione di
### **nascite** supera di almeno ### **`2` volte** la sua frazione di ### **nodi**, in almeno
### **due finestre su tre** fra i passi `700` e `1000`.

> ### ✔ **E <<due su tre>> e' la parte che conta:** una finestra sola sarebbe
> ### **un'oscillazione**, e il criterio chiede che ### **persista.**

---

## 3. LE PREVISIONI, **scritte PRIMA**

### DEL GUARDIANO *(riportata come l'ha data Luca)*

> Con il `0.3` a zero le nascite sono ### **molte meno** e la prima arriva ### **piu' tardi
> del passo `214`**, forse ### **mai entro `1000`.** Nei bracci con nascite la spinta oltre
> `π` viene ### **soprattutto dal DIPOLO.** ### **Sul DOVE il guardiano NON fa previsioni
> sulle divisioni**; le ### **Schwinger** dovrebbero stare soprattutto nel ### **VUOTO**, per
> costruzione.

### LA MIA, **e la motivo coi conti del par.1**

| | la mia previsione | il perche' |
|---|---|---|
| **`R`** | ### **fra `0.2` e `0.6`**, quindi ### **NON `<= 0.1`** | il serbatoio fra `3π` e `4π` ### **non e' vuoto** come con la legge vecchia: `364` archi falliscono il cancello `2`, `q95 = 6.56`, massimo `76` |
| **prima nascita, braccio `A`** | ### **fra il `250` e il `450`**, e ### **PRIMA del `1000`** | col `0.3` il cancello `1` si apre fra il `200` e il `214`; con la soglia piatta serve `|tw| >= 9.42` invece di `~6.6`-`9.4`, e il `|tw|` mediano cresce di circa `1.2` ogni `300` passi |
| **la sorgente della spinta oltre `π`** | ### **soprattutto il DIPOLO**, come il guardiano | un cambio di chiralita' inietta ### **`π` esatto** in un passo; la variazione di fase per passo ha `q95 = 0.1521`, quindi passare `π` ### **per fase sola e' raro** |
| **la correlazione `>= 0.5`** | ### **NON mi impegno** | mescola ### **causa ed effetto**, e con `1000` punti `0.5` e' facile ### **per tendenza comune** |
| ### **il DOVE** | ### **BORDO sovrarappresentato** per le ### **divisioni**; ### **VUOTO** per le Schwinger | la mitosi scatta dove `|tw|` e' alto, e `tw` nasce dalla ### **differenza di fase sull'arco**: dentro una regione la fase e' ### **coerente** *(dispersione `0.05`)* quindi `dph ≈ 0`, e nel vuoto profondo i nodi sono ### **poco connessi.** ### **Il gradiente sta sulla SUPERFICIE**, ed e' li' che `dph` e' grande |
| ### **e la cosa che il DOVE deciderebbe** | se vince il ### **BORDO**, l'accelerazione e' ### **superficie che cresce**, cioe' ### **geometria**; se vince la ### **MATERIA**, e' ### **materia che prolifera** | ### **Non lo prevedo come esito**: lo scrivo perche' ### **la lettura sia fissata prima**, e non scelta dopo |

> ### ⛔ **E LE MIE PREVISIONI SULLA MISURA LUNGA ERANO SBAGLIATE TRE SU QUATTRO** *(le
> divisioni di `23` volte, il rapporto, e gli archi oltre `4π`)*. ### **Chi legge pesi queste
> per quello che valgono**, e il conto resta scritto.
>
> ### ⚠ **E DICHIARO LA COSA CHE PIU' FACILMENTE MI FAREBBE SBAGLIARE:** sto prevedendo il
> braccio `A` con i numeri del braccio ### **B**. ### **Le due traiettorie divergono**, e il
> serbatoio fra `3π` e `4π` del braccio `A` ### **potrebbe non formarsi affatto** se sono le
> nascite — che alterano `|tw|` col calcio — ### **a riempirlo.** In quel caso `R` sarebbe
> ### **molto piu' piccolo** di quanto prevedo, ### **e il circolo del guardiano sarebbe la
> spiegazione di ENTRAMBE le cose.**

---

## 4. LA STELLA POLARE — **le cinque risposte** *(`L-STELLA`)*

| | la risposta |
|--:|---|
| **1** *(`A14`, conservazione locale)* | ### **NON SI APPLICA, e il perche':** questo lavoro ### **non introduce nessuna legge.** `_AMP` e' un'ampiezza ### **gia' nel codice** *(il `0.3` di `:8376`)*, e la patch la rende iniettabile ### **in una COPIA** per poterla azzerare. I ganci sono ### **di sola lettura**, e `C-letture` lo ### **misura al bit.** Il simulatore ### **non si tocca:** resta `cf2a1ac8` |
| **2** *(a quale dei tre gradini)* | ### **gradino `(b)`: <<regge togliendo la legge pratica>>** — ed e' ### **esattamente** la domanda `1`. Il `0.3` e' la legge pratica; `R` misura se la crescita regge senza. ### **NON arriva ai gradini `(a)` e `(c)`:** un seme solo *(quindi ### **nessuna barra d'errore fra semi**, e `P3` chiederebbe `>= 4`)*, e nessun limite noto con cui confrontare |
| **3** *(aggiunge un numero o una legge?)* | ### **NO, ne TOGLIE uno:** `_AMP = 0` ### **annulla** una modulazione. ### **E il `0.3` e' del tipo <<toppa>>**, non costante di accoppiamento: modula una soglia ### **per far accadere la mitosi.** `9-ter` dice che a parita' di effetto si preferisce ### **togliere un'eccezione** — e questa misura dice ### **se si puo'** |
| **4** *(tocca `rho`, `c_s` o il SEGNO?)* | ### **NO, non li tocca.** ### **Ma li MISURA tutti e tre:** il punto `E` registra `rho_spin` e `|ψ|²` *(densita')* e `ritmo() = cs/CS_M` *(la velocita' metrica)*; e `perc_chi` ### **e' il segno di doppia copertura.** ### **Il verso che la misura guarda e' `curvatura → chiralita' → torsione`**, cioe' ### **curvatura → EM** |
| **5** *(emergente o imposto)* | ### **E' LA DOMANDA DEL MANDATO, e la risposta e' il risultato:** `R >= 0.5` → ### **emergente**; `R <= 0.1` → ### **imposta dal `0.3`.** ### **Non la rispondo adesso:** rispondere prima di misurare sarebbe ### **decidere il risultato.** ### **E il DOVE e' la seconda meta' della stessa domanda:** una crescita che si concentra ### **sul bordo** e' geometria, una che si concentra ### **nella materia** e' proliferazione |

---

## 5. TODO DEL NEXT STEP

1. **commit di questo task history**, ### **DA SOLO**;
2. lo **strumento**: quello della misura lunga ### **piu'** la patch di `_AMP` ### **adattata
   al blob nuovo**, ### **piu'** i ganci dei punti `D` ed `E`, col **collaudo** — ### **commit
   a se', PRIMA della corsa**;
3. ### ⛔ **il giro corto SI RIGIRA DOPO OGNI CURA, non una volta sola:** e' la lezione di
   `LUNGA-BATTITO-CADUTA`, e saltarla e' costata una corsa;
4. **`C-letture`** *(ganci contro nessun gancio, al bit, `150` passi)* e **`C0`**: ### **se
   uno dei due fallisce, FERMO**;
5. le **due corse** da `1000` passi, in ### **processi separati** e in ### **background**,
   controllate periodicamente;
6. le **uscite col verdetto**, poi il **referto generato**;
7. ### ⛔ **poi FERMO:** il `0.3`, la soglia `3π`, `κ` e ### **la legge del basculamento
   chirale** si decidono su questi numeri, e ### **sono decisioni di Luca.**

---

## ANNOTAZIONE *(2026-10-06, dopo il giro corto -- `par.8`: si ANNOTA, non si riscrive)*

> ### ⛔ **UN <<FATTO DAL CODICE>> DEL PAR.1 E' SBAGLIATO, E LO HA TROVATO IL GIRO
> CORTO.** Avevo scritto che `chi_torsione` e' ### **`perc_chi`** *«con `CHI_CORE = False` e
> `CHI_COOP = False`»*. ### **Quelli sono i DEFAULT DI MODULO, non la SCENA:** l'argv del
> driver ha ### **`--chi-coop` E `--chi-core`**, e li ho verificati ### **adesso**, da
> `_cli_flag.argv_del_driver()`.

**COSA CAMBIA, e non e' poco:**

| | prima credevo | il fatto |
|---|---|---|
| chi scrive il basculamento | `perc_chi` | ### **`perc_geom`** *(il ramo `CHI_COOP`, `:7905`)* |
| cos'e' `chi_torsione` | `perc_chi` | ### **`_chi_geom_nodi`**: la chiralita' core-locale calcolata da `perc_geom` |
| il ramo che hookavo | quello giusto | ### **quello `else`, che in questa scena NON GIRA MAI** |

**E IL SINTOMO ERA VISIBILE SUBITO:** il giro corto dava ### **`chi = 0` a ogni passo**
mentre il dipolo cambiava su ### **`90854` archi.** ### **Un contatore a zero accanto a un
effetto grande: la stessa forma del falso-zero che mi e' tornata addosso tutta la
settimana.**

### ✔ COME L'HO CURATO, e non e' <<cambiare `perc_chi` in `perc_geom`>>

Il gancio che conta e' ### **su `chi_torsione` stesso**, dove il dipolo lo legge:
### **si misura la grandezza che ENTRA, non si indovina chi l'ha scritta.** Cosi' il conto
### **vale qualunque sia il flag** che governa la cache, e ### **non va rifatto** se un
giorno cambiasse. E accanto restano gli altri due, ### **dichiarati per quello che sono:**

| contatore | che cos'e' |
|---|---|
| ### **`cambi_chi_tors`** | ### **la grandezza che ENTRA nel dipolo.** E' questa che il criterio usa |
| `cambi_geom` | i cambi che il basculamento scrive *(`perc_geom`)* |
| `cambi_perc_chi` | ### **cio' che il mandato NOMINA**, e che in questa scena ### **non entra nel dipolo**: misurato `0` in `4` passi |

> ### ⚠ **L'IPOTESI DEL GUARDIANO NON CADE, SI PRECISA:** il meccanismo e' quello che
> aveva descritto, ### **ma la grandezza che cambia e' la GEOMETRIA e non la CARICA**, e
> ### **la carica non cambia affatto.** ### **Il criterio del par.2 NON si tocca:** era
> fissato prima, e si legge sul contatore che ### **misura il dipolo**, come dice.

**E UN SECONDO RILIEVO, registrato come `CHI-BASC-DESCRIZIONE`:** la riga che `--chi-basc`
stampa all'avvio dice *«`perc_chi` vira»* ### **mentre scrive `perc_geom`** — cioe'
### **nomina l'array sbagliato nel dump della configurazione**, che e' uno dei posti dove
chi legge si fida di piu'. ### **NON la correggo qui: sta nel simulatore, e in questo
mandato il simulatore non si tocca.**

### ⛔ **E UNA COSA CHE LA MIA PREVISIONE ORA DEVE DIRE:** avevo previsto *«la spinta
oltre `π` viene soprattutto dal DIPOLO»* ragionando su un ribaltamento che inietta
### **`π` esatto.** ### **Il collaudo ha mostrato che `> π` NON conta un `π`
esatto**, quindi un ribaltamento su ### **un solo estremo** con fase nulla
### **sfuggirebbe al criterio.** ### **Il criterio resta `> π`** — era fissato prima
— e accanto c'e' ora `spinta_pi_esatto`, che rende ### **visibile** l'accumulo al bordo
invece di lasciarlo cadere in silenzio. ### **Se quel contatore fosse grande e
`spinta_pi_dip` piccolo, la lettura <<refutata>> sarebbe un ARTEFATTO DELLA SOGLIA**, e il
referto deve dirlo.

---

## ANNOTAZIONE *(2026-10-06, a controlli girati -- `par.8`: si ANNOTA)*

### ✔ `C0` PASSA, e con molta materia

`150` passi, ### **`41` campi per passo** piu' ### **`2691` quantili** = ### **`8841`
valori**, e ### **ZERO differenze** contro il `lunga.json`. ### **Lo strumento riproduce la
misura lunga esattamente**, quindi il confronto fra i due bracci avra' un fondamento.

### ⛔ `C-letture` FALLISCE, **e il difetto e' NEL CONTROLLO**

`3` differenze su `8841` valori, e sono ### **tutte e tre in contatori che esistono SOLO
perche' i ganci ci sono:**

| il campo | con i ganci | senza |
|---|--:|--:|
| `cambi_geom` *(passo `1`)* | `6419` | `0` |
| `chi_tors_non_confrontabile` *(passo `1`)* | `1` | `0` |
| `cambi_chi_tors` *(passo `2`)* | `6419` | `0` |

> ### ✔ **E L'HO VERIFICATO IN MODO INDIPENDENTE, non a occhio:** ho confrontato l'insieme dei
> campi che differiscono con ### **l'insieme dei contatori che la classe `Misura` dichiara in
> `_azzera_passo`**, letto ### **dalla classe stessa.** ### **Le differenze FUORI da quei
> contatori sono ZERO.**

**Quindi la sostanza di `C-letture` e' stabilita:** ### **`8838` valori su `8841` sono
identici AL BIT su `150` passi**, e i tre scarti sono ### **in grandezze che il braccio senza
ganci non puo' produrre.**

> ### ⛔ **MA IL CONTROLLO E' FALLITO, E IO LO STO CAMBIANDO DOPO CHE E' FALLITO.** Lo scrivo
> cosi' perche' e' ### **la forma esatta del muovere i pali della porta**, e la differenza
> sta in due cose ### **verificabili**, non nella mia parola:
>
> 1. ### **la ragione era scritta PRIMA.** Il docstring di `c_letture`, committato in
>    `2893907`, dice gia': *«i campi ### **nuovi non si pretendono** dal braccio senza ganci:
>    pretenderli sarebbe ### **un falso fallimento**»*. ### **L'avevo scritto e NON
>    l'avevo implementato**, ed e' un difetto di esecuzione, non un criterio che cambia.
> 2. ### **l'esclusione e' DERIVATA, non elencata a mano:** si legge
>    `set(Misura(dt, amp).p)` ### **dalla classe**, quindi ### **qualunque contatore futuro
>    e' escluso automaticamente e NESSUN campo del simulatore puo' finirci dentro di
>    nascosto.**
>
> ### ⚠ **E il fallimento resta committato prima della correzione**, cosi' ### **si vede da
> git che non ho aggiustato il controllo finche' non passava.**

### `C1` PASSA, **ma con poca materia, e va detto**

`150` passi, `0` divisioni, `0` Schwinger, `0` nati. ### **Il controllo e' vero e non ha
nulla da controllare:** a `150` passi col `0.3` acceso la rete ### **non ha ancora partorito**
*(la prima nascita della misura lunga e' al passo `214`)*. ### **`C1` diventera' informativo
solo sulle corse da `1000` passi**, e li' va riletto.

### `C1 (zero)` e `C-fallisce`: **NON FATTI**, e non e' un `PASSA`

Manca il `json` del braccio `_AMP = 0`, che ### **non e' ancora stato girato.** Lo strumento
dice ### **«NON FATTO»** e torna `1`: ### **un controllo che non si e' potuto fare non deve
poter passare per uno che e' passato.**
