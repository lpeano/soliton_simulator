# `L2`, QUARTO PEZZO — **LA RISPOSTA DEL VUOTO A UNA SORGENTE FERMA**

*(mandato di Luca del `2026-10-15`. Ultimo commit verificato dal guardiano: `a9cb2ee`.
**Il motore NON si tocca, la tabella NON si tocca: tutto nello script.**)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE**, e il commit del codice ha questo
> come ### **antenato**: cosi' l'ordine e' verificabile da `git` invece che asserito da me.

---

## 0. PERCHE' QUESTO PEZZO ESISTE — *due errori, uno del guardiano e uno di protocollo*

### ⚠ **(a) L'ERRORE DEL GUARDIANO, come lui stesso lo scrive:** la richiesta di una
*«`beta` lineare»* presupponeva ### **un effetto sul vuoto proporzionale a `beta`.**
### ⛔ **Ma il secondo pezzo** *(`48fb22f`)* **aveva gia' mostrato che la parte netta e'
PARI in `beta`**, e il terzo *(`74ba200`)* lo ha confermato col numero:
### **esponente misurato = `2` x esponente di `beta`** *(`6.0` dove `beta ~ x^3`)*.

### ⛔⛔ **(b) IL DIFETTO DI PROTOCOLLO, E VALE PER TUTTI E TRE I PEZZI: LA SORGENTE NON
ERA FERMA.** Il grumo ### **si disperde** — larghezza da `0.894` a `~3.6`-`4.1` sul toro
`7x7`, misurato nel terzo pezzo. ### **Con una sorgente che si muove, la risposta di primo
ordine del vuoto e' un'onda che si media a zero, e resta solo il secondo ordine (`beta^2`).**

> ### ⭐⭐ **E LA GRAVITA' DI UNA MASSA E' IL SUO CAMPO STATICO.** La risposta statica a un
> potenziale fermo e' ### **di norma LINEARE.** ### **Questa misura la ISOLA.**

### 📌 **E lo dico come lo capisco io, per non ripetere a pappagallo:** nei tre pezzi
precedenti ho misurato ### **la scia di una sorgente che scappa**, non ### **il campo di
una massa che sta.** ### **Sono due cose diverse, e la seconda e' quella che il bersaglio
del progetto chiede** *(`doc/IPOTESI_gravita_a_spinta.md`, prove `②` e `③`)*.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐ **CREDO CHE LA RISPOSTA STATICA SIA LINEARE IN `beta`, e ho un motivo meccanico:**
il termine scrive su `phi` ### **una FASE**, e ### **una fase non cambia `|phi|^2`** —
quindi `Lambda` non cambia *per niente* finche' il hop non mescola. Il hop fa
`phi' = alpha phi + beta_hop S_U phi`, e il cambiamento di `|phi'|^2` contiene
### **il termine incrociato in `Re(phi^* S_U phi)`**, che dipende dalla ### **DIFFERENZA
di fase fra vicini.** Con la sorgente ferma quella differenza e' `~ beta dtau` ### **al
PRIMO ordine**, e non si media a zero perche' ### **non oscilla.**
### ⛔ **Quindi mi aspetto le pendenze `~3` (`S1`), `~1` (`S2`, `S3`), `~1.64` (`S4`).**

### ⚠ **MA NON LO SO, E DICO PERCHE' POTREI SBAGLIARMI:** lo stato stazionario potrebbe
cancellare il primo ordine. Su un toro ### **il vuoto totale e' conservato**, quindi
`somma_k dLambda_k = 0` ### **per identita'** — e un profilo a somma nulla ### **puo'
avere il termine di primo ordine che si annulla nell'integrale** e sopravvive solo nella
FORMA. ### **Se esce `2x`, il mio ragionamento meccanico e' sbagliato e lo scrivo.**

### ⚠⚠ **E IL SEGNO NON LO SO, ed e' il punto.** Il segno che ho misurato nei tre pezzi
*(il vuoto si ACCUMULA)* viene dal canale ### **`beta^2`.** ### **Il canale di primo
ordine puo' avere il segno OPPOSTO**, e sarebbe coerente: `beta` cambia segno, `beta^2` no.
### 📌 **Non ho una previsione, e non ne invento una dopo.**

### 📌 **DUE PREVISIONI PIU' PICCOLE, scritte qui per poterle sbagliare:**
### **(i) la SOVRAPPOSIZIONE regge a `x` piccolo e si rompe a `x = 1`**, con lo scarto
relativo che ### **cresce con `x`** *(la correzione e' quadratica)*;
### **(ii) il PROFILO cambia SEGNO a una certa distanza**, perche' la somma su tutti i
nodi e' nulla per identita' — come l'anello `3` negativo del secondo pezzo.
### ⛔ **E NON adatto il profilo a `log r` prima di guardarlo**, come il mandato dice: il
toro e' `2D`, e `log r` e' ### **cio' che si verifica DOPO, non cio' che si assume.**

### ⚠ **CIO' CHE NON SO E CHE NON PROVO A INDOVINARE:** quanto tempo serve allo stato
stazionario; se l'accensione di colpo lasci un transitorio che non si spegne; e se le forme
con `alpha` divergente *(`S2`, `S3`)* siano leggibili qui — ### **nel terzo pezzo non lo
erano.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### ⛔⛔ **LA SCELTA CHE IL MANDATO MI CHIEDE DI DICHIARARE: COME SI CONGELA LA MATERIA**

> ### ⭐ **SCELGO: `psi` SI RIPRISTINA A OGNI TICK** *(copia salvata prima del tick,
> riscritta dopo)*, e ### **NON <<i pezzi su `psi` non si applicano>>.**

**I tre motivi, e il terzo e' quello che decide:**

1. ### **non mi obbliga a CLASSIFICARE i pezzi** in *«su `psi`»* e *«sul vuoto»* — una
   classificazione sarebbe ### **una decisione di fisica mia**, e non ne prendo;
2. ### **e' UNA RIGA**, quindi non c'e' un secondo posto da tenere d'accordo col primo;
3. ### ⭐ **`rho_k` risulta ESATTAMENTE costante ai confini dei tick, e lo MISURO** —
   `max |rho(t) - rho(0)|` ### **su tutta la corsa.**

### ⚠ **E IL PREZZO, che dichiaro:** ### **dentro il tick** i pezzi del vuoto vedono una
`psi` che si e' mossa di un passo. ### **Quindi la sorgente e' ferma AI CONFINI DEI TICK,
non dentro il tick** — un errore `O(dtau)` per tick, ### **e lo dico invece di nasconderlo.**

### ⛔⛔ **E LA SORGENTE CONGELATA E' UNO STRUMENTO DI MISURA, NON UNA LEGGE:** e' ### **la
<<massa di prova>> della fisica** — un corpo che genera il campo e non lo subisce.
### ⚠ **Viola la conservazione PER COSTRUZIONE** *(il ripristino rimette dentro cio' che la
dinamica aveva tolto)*, e ### **per questo non puo' stare in nessuna tabella: vive nello
script, e il referto lo dice in testa.**

### ⭐ **UNA COSA CHE PREVEDO E CHE SI MISURA AL BIT:** con la sorgente congelata
### **`alpha` NON PUO' CONTARE NIENTE.** `alpha` scrive una fase su `psi`, il ripristino la
cancella, e ### **tutto cio' che il vuoto legge da `psi` e' `rho` o `h`, che sono
invarianti di fase.** ### ✅ **Quindi: `alpha = 0` forzato deve dare lo STESSO RISULTATO AL
BIT**, e se non lo da' ho capito male qualcosa. ### **E' un braccio.**

### **LA CONFIGURAZIONE, fissata QUI e stampata dal referto**

| | |
|---|---|
| **il toro** | ### **`31x31`** = `961` nodi, `1922` archi, distanza toroidale massima ### **`30`** |
| **perche' `31` e non `15`** | il **budget MISURATO**: `0.760` ms/tick su `7x7`, `1.224` su `15x15`, `1.813` su `21x21`, ### **`2.998` su `31x31`** — e un profilo in distanza vuole ### **un decennio di `r`**, non tre anelli |
| **la scena** | `n` **geometrici**, `U = I`, `phi` **uniforme**, grumo a elicita' `+1` di raggio `1` sul nodo `0`, seme `7` |
| **`dtau`** | `0.5` e `0.25` |
| **l'accensione** | **(a) di colpo** *(`T = 0`)* e **(b) rampa liscia** `s(t) = (1 - cos(pi t/T))/2` su ### **`T = 100` e `T = 800`** tick |
| **la finestra di misura** | ### **DOPO la rampa**: dal tick `T` alla fine, in `10` blocchi |
| **i tick** | `2000` per il verso e il profilo; `1200` per la scansione in `x` e la sovrapposizione |
| **l'intensita'** | `x = 0.01, 0.03, 0.1, 0.3, 1` *(ampiezza `sqrt(x)`, come nei tre pezzi: `x = rho/Lambda`)* |
| **le forme** | `S1`, `S2`, `S3`, `S4` — ### **nessuna in tabella** |

### ⚠ **`T`, i tick e la taglia sono PARAMETRI DI PROTOCOLLO, non costanti di
accoppiamento** *(`A1`)*: ### **non li taro per far uscire un risultato**, e di `T` ne
porto ### **due** proprio perche' il risultato ### **non deve dipendere da `T`.**

### **I PASSI, e cosa decide ciascuno**

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| `1` | **il vuoto di riferimento su `31x31`**, senza sorgente, `2000` tick | che la base sia **stazionaria**, altrimenti `dLambda` misura la deriva | se la deriva non e' a livello di ulp: **mi fermo e la riporto** |
| `2` | **il CONGELAMENTO fa qualcosa?** larghezza di `rho` con e senza ripristino | che lo strumento **non sia un FALSO-ZERO** *(`rho` costante e' banale se lo impongo: devo mostrare che SENZA l'imposizione cambia)* | se `rho` cambia anche col ripristino: **lo strumento e' rotto** |
| `3` | **`alpha = 0` forzato** contro il termine intero | che con la sorgente ferma **`alpha` non conti**, AL BIT | se conta: **ho capito male il meccanismo, e lo scrivo** |
| `4` | **il controllo nullo** `beta = 0` | che `dLambda` sia **`0` esatto** | se non e' esatto: **mi fermo** |
| `5` | **(a) il SEGNO** di `dLambda` sulla sorgente, `>= 3` barre | *il vuoto si ritira o si accumula?* | nessun verdetto sotto `3` barre: **allungo la corsa, non abbasso la soglia** |
| `6` | **(b) la LINEARITA'**: pendenza `log`-`log` di `|dLambda|` in `x` | se la risposta statica e' **lineare in `beta`** *(atteso `3`, `1`, `1`, `1.64`)* o **`2x`** | niente: e' una misura, e il numero che esce **e' il risultato** |
| `7` | **(c) la SOVRAPPOSIZIONE**: `dLambda(A+B)` contro `dLambda(A) + dLambda(B)` | se vale **la linearita' di Newton**, nodo per nodo | niente da fermare: **lo scarto relativo con la sua barra E' la risposta** |
| `8` | **(d) il PROFILO** in distanza | **come decade**, e **dove cambia segno** | ### ⛔ **non adatto a `log r` prima di guardare** |
| `9` | **la somma di `|phi|^2` conservata** in ogni corsa | che il vuoto **si sposti e non nasca** | se non e' conservata: **mi fermo** |

### ⛔ **E SE UN CRITERIO FALLISCE NON AGGIUSTO NIENTE:** committo la misura, spiego, e mi
fermo. ### **La scelta della forma e' di Luca, e si prende coi numeri di questa misura.**

---

## 3. LA STELLA POLARE — *le cinque domande, PRIMA del codice*

### **`1` — `A14`: conserva energia e carica LOCALMENTE?**
### ⛔ **NO, E LO VIOLA PER COSTRUZIONE — ma non e' una legge, e' lo STRUMENTO.** Il
termine candidato da solo conserva la somma di `|phi|^2` *(scrive una FASE)*; ### **il
CONGELAMENTO della sorgente no:** il ripristino di `psi` a ogni tick ### **rimette dentro
cio' che la dinamica aveva tolto**, cioe' e' una ### **condizione al contorno non
conservativa.** ### ✅ **E' esattamente la <<massa di prova>>**: un corpo che genera il
campo e non lo subisce. ### **Dichiarato qui, nel referto e nella voce — e non entra in
nessuna tabella.** *(`A14`, `CONSERVAZIONE-LOCALE`)*

### **`2` — a quale dei TRE GRADINI arriva il risultato?**
### **(a) robusto al rumore numerico: SI'**, ed e' cio' a cui mi fermo — barre a blocchi,
due `dtau`, ### **due `T` di rampa**, controllo nullo `beta = 0` esatto, e il vuoto di
riferimento verificato stazionario.
### **(b) regge togliendo la legge pratica: NON SI APPLICA, e il perche' e' che qui la
legge sotto esame E' il termine** — non c'e' una legge pratica accesa che potrebbe
produrre il fenomeno; ### **cio' che e' IMPOSTO e' l'immobilita' della sorgente**, e il
confronto col terzo pezzo *(sorgente libera)* e' il «togliere».
### **(c) coincide con un limite noto: NON ANCORA.** Il limite candidato e' il potenziale
statico newtoniano in `2D`, che va come `log r` — ### ⛔ **e il mandato vieta di adattarlo
prima di guardare il profilo.** *(`ROBUSTEZZA-FISICA`)*

### **`3` — aggiunge un numero o una legge?**
### ⛔ **ZERO leggi in tabella e ZERO costanti di accoppiamento.** Cio' che aggiungo sono
### **parametri di PROTOCOLLO**: la taglia del toro, i tick, `T` della rampa, i valori di
`x`, il seme. ### ✅ **Nessun clip, nessun pavimento, nessun tetto.** ### 📌 **L'unica cosa
che somiglia a una toppa e' `alpha = 0` dove `rho = 0`, ed e' gia' dichiarata nel terzo
pezzo come SINGOLARITA' ELIMINABILE** *(dove `psi = 0` la fase di `psi` non vuol dire
niente)* — e ### **qui conta ancora meno, perche' il braccio `3` misura che `alpha` non
conta per niente.** *(`A1-COSTANTI`, `CLIP-INVENTARIO`)*

### **`4` — tocca `rho`, `c_s` o il SEGNO? In quale VERSO?**
### **Tocca `rho` LEGGENDOLA**, e la congela: `rho` e' la ### **sorgente**, non
l'incognita. ### **E il SEGNO di `dLambda` sulla sorgente e' LA DOMANDA `(a)`.**
### ⛔⛔ **E IL VERSO E' UNO SOLO, PER COSTRUZIONE: `materia -> vuoto`.** La retroazione
`vuoto -> materia` e' ### **ESCLUSA dal congelamento**, quindi ### **questa misura non dice
NIENTE sul verso `EM -> curvatura`** — e un risultato di qui ### **non si puo' usare per
affermare la bidirezionalita'.** *(`EM-CURVATURA-BIDIREZIONALE`)*

### **`5` — emergente o imposto?**
### ✅ **EMERGENTE, e c'e' un motivo meccanico oltre al controllo:** il termine scrive
### **una FASE su `phi`**, e ### **una fase non cambia `|phi|^2`** — quindi
### **nessuna riga del termine puo' scrivere un profilo di `Lambda`.** Il profilo nasce
### **dall'interferenza del hop**, cioe' dalla dinamica. ### ✅ **E il controllo `beta = 0`
deve dare `0` ESATTO**, non «piccolo».
### ⛔ **Cio' che e' IMPOSTO, e lo ripeto perche' e' la cosa che un lettore deve sapere, e'
l'IMMOBILITA' DELLA SORGENTE.** *(`ROBUSTEZZA-FISICA`, gradino `b`)*

---

## 4. TODO DEL NEXT STEP — *la lista operativa*

1. ### **`primo_ordine/_misura_statica_l2.py`** — nuovo, e ### **il motore non si tocca**:
   sostituzione di `mot.operatori["CAMM-SATURAZIONE"]` a runtime, come nel terzo pezzo,
   ### **piu' la rampa e il ripristino di `psi`.**
2. le ### **quattro domande** `(a)` `(b)` `(c)` `(d)` e i ### **cinque controlli**
   *(base stazionaria, il congelamento fa qualcosa, `alpha` non conta AL BIT, `beta = 0`
   esatto, la somma di `|phi|^2` conservata)*.
3. ### **dichiarare il modulo** in `primo_ordine/_mappa.yaml` e in `csv/_file_fisica.py`,
   e ### **le funzioni che scrivono il passo a mano** in `csv/_un_solo_esecutore.py`
   *(`P-ES1`: me lo ricordo da `74ba200`, e il dizionario giusto e' ### **`SCRITTI_A_MANO`**,
   non `ECCEZIONI`)*.
4. ### **la riga nell'inventario** con file, comando verbatim, cosa misura, ### **BLOB**.
5. ### **il referto DAL CODICE COMMITTATO** in `doc/referti_l2/`, accanto ai tre vecchi.
6. ### **la RIPRESA, la mappa, la relazione**, e la voce
   `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]` con l'esito.
7. ### **STOP.**
