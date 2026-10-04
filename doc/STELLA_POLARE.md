# LA STELLA POLARE — **le cinque domande di ogni commit di fisica**

*(decisione di Luca, 2026-10-04. **Tetto: 60 righe.**)*

> ### **Questo documento NON contiene decisioni di fisica. Le domande non decidono:
> ### OBBLIGANO A RISPONDERE.**

**Ogni mandato di fisica e ogni commit che cambia la fisica affronta queste cinque domande
PER ISCRITTO nel task history** — ### **anche solo con *«non si applica, perche' …»***.
### ⚠ **Una domanda saltata non e' una risposta; una risposta *«non si applica»* senza il
*«perche'»* non e' una risposta.**

| | la domanda | la voce |
|--:|---|---|
| **1** | **`A14`:** questa legge conserva **energia e carica LOCALMENTE**? Se no, e' **dichiarata** fra le violazioni note? | `A14` · `CONSERVAZIONE-LOCALE` |
| **2** | **a quale dei TRE GRADINI arriva** il risultato che si sta per affermare? *(a) robusto al rumore numerico · (b) regge togliendo la legge pratica · (c) coincide con un limite noto* | `ROBUSTEZZA-FISICA` |
| **3** | **aggiunge un numero o una legge?** Di che **tipo** — *costante di accoppiamento · toppa · proiezione/pavimento/clip*? **Compensa un difetto** invece di derivare da un principio? | `A1-COSTANTI` · `CLIP-INVENTARIO` · `AUDIT-CURE` |
| **4** | **tocca `rho`, `c_s` o il SEGNO?** Se si', **in quale VERSO** dell'accoppiamento agisce — *curvatura→EM* o *EM→curvatura*? | `EM-CURVATURA-BIDIREZIONALE` |
| **5** | **emergente o imposto:** il fenomeno **sopravvive** se si toglie la legge pratica che lo potrebbe produrre? | `ROBUSTEZZA-FISICA` *(gradino b)* |

### **PERCHE' CINQUE, e perche' queste**

Non sono un riassunto delle regole: sono i cinque modi in cui **un risultato puo' sembrare
fisica senza esserlo.** ### **①** una legge che conserva solo *in media* non conserva
*(`A14`)*. ### **②** un numero che viene da un run solo non e' una misura — e i conteggi
assoluti **dipendono dalla piattaforma**: sulla stessa scena, Linux/numpy 2.5.3 misura
`16/14/6/6` dove Windows/numpy 2.3.0 misura `14/12/4/4`, ### **mentre l'identita'
*prima/dopo* no.** ### **③** un fenomeno che vive in una finestra stretta di un numero a mano
e' **imposto** *(`A1`)*. ### **④** un accoppiamento a **un solo verso** non e' quello della
natura. ### **⑤** una legge pratica accesa puo' **produrre** il fenomeno che si crede di
osservare.

### ⚠ **E LA 3 HA UNA TRAPPOLA, che vale la pena scrivere qui:** i tre tipi **non sono tre
gradi dello stesso difetto.** Una *costante di accoppiamento* e' **legittima** e va solo
dichiarata; una *toppa* e' un **debito** e la cura e' una **derivazione**; una
*proiezione / pavimento / clip* ### **viola `A14` per costruzione QUALUNQUE SIA IL VALORE** —
quindi **non esiste una lagrangiana che la contenga: va TOLTA.**
### **Confonderli porta a TARARE un clip invece di TOGLIERLO.**

### **LE ALTRE DUE VOCI DELLA STELLA POLARE**, che non sono domande ma **vincoli di ordine**:

| voce | che cosa vincola |
|---|---|
| `MODELLO-MINIMO` | un modello semplice **DOPO** il simulatore completo, che resta il nucleo. ### **Scritto prima, sarebbe una semplificazione SUPPOSTA** |
| `TAGLIA-FINITA` | al limite continuo si va per **scaling di taglia finita** — reti diverse e si estrapola — non cercando una rete enorme. ### ⚠ **E due taglie non sono uno scaling: sono una retta per due punti** |
| `GEOMETRIA-DELLA-CRESCITA` | ### **SPECULATIVA.** Si guarda **solo** dopo l'energia e la legge di nascita, e **solo a partire da un'anomalia MISURATA** — mai scritta prima |

### ⛔ **QUESTO E' UNA REGOLA SCRITTA, NON UN PRESIDIO** *(`A9`)*. **Nessun hook controlla che
le cinque domande siano nel task history:** oggi lo controlla soltanto chi legge. ### **E una
regola scritta, in questo repo, e' stata violata tre volte prima di diventare una macchina.**

### 📌 **COME SI RISPONDE, in pratica:** una sezione **`LA STELLA POLARE`** nel task history,
cinque righe numerate, ciascuna col rimando alla sua voce. ### **Le risposte si scrivono
PRIMA del lavoro**, come il resto del task history *(par.8)*: una risposta scritta dopo aver
visto i numeri e' **una ricostruzione, non un impegno.**
