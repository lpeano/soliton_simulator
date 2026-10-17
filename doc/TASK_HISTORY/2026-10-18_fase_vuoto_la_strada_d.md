# `CAMM-FASE-VUOTO` — **LA FASE SUL VUOTO CHE NASCE DA `G`** *(la strada `(d)`)*

> ### 📌 **Decisione di Luca del `2026-10-18`, `00:07`** *(la strada `(d)`,
> l'accoppiamento hamiltoniano)*, ### **mandato del guardiano dello stesso giro.**
> ### ⛔ **I criteri `C1`-`C5` sono COPIATI QUI dal mandato, PRIMA della misura**, e
> ### **qui non se ne cambia nessuno.**

> ### ⛔ **E QUESTO FILE SI COMMITTA PRIMA DEL CODICE**: l'ordine e'
> ### **verificabile da `git`** *(questo commit e' ANTENATO dei commit del codice)*.

---

## 0. LA STELLA POLARE — *le cinque risposte, PRIMA del codice*

### **`1` — `A14`: questa legge conserva energia e carica LOCALMENTE?**

### ✅ **LE NORME SI', ESATTAMENTE E PER COSTRUZIONE:** il pezzo e'
### **una FASE su `phi`**, e una fase ### **non cambia nessun modulo** -- quindi
### **`M` e `V` restano**, non *«entro una banda»* ma ### **al bit, componente per
componente.**
### ⭐⭐ **E L'ENERGIA: QUESTA LEGGE ESISTE PER CONSERVARLA.** E' il termine che
### **mancava** perche' il passo fosse ### **il flusso di `G`**: senza di lui la pendenza
di `G` con `cs` dinamico e' ### **`-0.001`** *(misurato)*. ### **Quindi la risposta non e'
<<conserva>>: e' <<e' il pezzo che rende vera la conservazione>>** -- e
### **il criterio `C1` e' esattamente questo**, con la sua banda `1.9`.
### ⚠ **E LA VIOLAZIONE NOTA RESTA DICHIARATA:** `G` si conserva
### **al SECONDO ORDINE**, non esattamente -- come la decisione `QC` dice del suo
oggetto, ora esteso a `G`.

### **`2` — a quale dei TRE GRADINI arriva il risultato?**

### ✅ **GRADINO `(a)`, robusto al rumore numerico:** le pendenze su `>= 4`
dimezzamenti, le bande in ulp, i casi che DEVONO fallire.
### ✅ **E GRADINO `(b)`, <<regge togliendo la legge pratica>>, in un senso preciso:**
### **a forma `cs` SPENTA questa legge NON ESISTE** *(`cs'` non c'e')*, e il passo
### **resta AL BIT** -- cioe' ### **si puo' togliere, e si vede cosa si perde.**
### ⛔ **GRADINO `(c)` NO, e lo dico:** ### **non c'e' nessun limite noto** con cui
confrontare `G` -- e inventarne uno sarebbe peggio che non averlo.

### **`3` — aggiunge un numero o una legge? Di che TIPO?**

### ⛔⛔ **AGGIUNGE UNA LEGGE: da `6` a `7`**, e ### **`9-ter` chiede di dire
perche' non si poteva togliere niente.** ### ✅ **LA RISPOSTA:** non e'
### **un'aggiunta**, e' ### **un pezzo della derivazione che mancava.** `G` dipende da
`phi` ### **anche attraverso `cs(Lambda)`**, e ### **quel pezzo del gradiente non era
implementato**: il passo di oggi e' il flusso di `G` ### **a `cs` CONGELATO**, non a `cs`
funzione dello stato.
### ✅ **NESSUN NUMERO NUOVO** *(`A1`)*: `cs'(Lambda) = Lambda_c/(Lambda +
Lambda_c)^2` e' ### **la derivata della forma GIA' scelta**, e `d w_a/d cs_k` e'
### **la derivata del peso che il passo GIA' usa.** ### **Zero manopole, zero clip, zero
pavimenti.**
### ⚠ **E NON COMPENSA UN DIFETTO:** il difetto *(la pendenza `-0.001`)* e'
### **il sintomo di una derivazione incompleta**, non un errore numerico da tamponare.

### **`4` — tocca `rho`, `c_s` o il SEGNO? In quale VERSO?**

### ✅ **TOCCA `phi`, cioe' IL VUOTO, e la sorgente e' `H` -- L'ENERGIA.** Nel
linguaggio di `[[EM-CURVATURA-BIDIREZIONALE]]` questo e'
### **il verso OPPOSTO a quello di `D0`-`D2`:** la' era ### **vuoto -> propagazione**
*(`curvatura -> EM`)*, ### **qui e' `EM -> curvatura`** -- l'energia della materia
### **muove il vuoto.**
### ⭐⭐ **E QUESTO E' IL PUNTO FISICO DELLA STRADA `(d)`, con le parole del
guardiano:** ### **<<il vuoto sente l'ENERGIA della materia, non solo la sua
DENSITA'>>** -- cioe' ### **l'energia gravita.**
### ⚠ **IL SEGNO NON LO SCELGO: esce dalla derivazione**, e
### **il caso che DEVE fallire `C2` e' proprio il segno invertito.**

### **`5` — emergente o imposto? Il fenomeno sopravvive togliendo la legge pratica?**

### ✅ **EMERGENTE DA `G`, e si vede togliendola:** con `cs` spento il termine
### **non c'e'** e il passo e' quello di prima ### **al bit**; con `cs` acceso
### **nasce da solo** dalla derivata, ### **senza che nessuno scelga niente.**
### ⚠ **MA `Lambda_c` RESTA IMPOSTO** *(`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`)*, e
questa legge ### **non lo tocca:** ### **eredita quella domanda, non la chiude.**

---

## 1. RAGIONAMENTO PRELIMINARE — *la derivazione, e cosa ho GIA' misurato*

### ⭐⭐ **LA DERIVAZIONE DI `Omega`, passo per passo**

`G = somma_k cs_k H_k^nodo + somma_a w_a H_a^arco`, con `cs_k = cs(Lambda_k)` e
`w_a = armonica(cs_i, cs_j)` -- ### **il peso che il passo usa.**

Il campo del vuoto entra in `G` ### **in due modi**: dentro gli `H` *(come `phi`)* e
dentro i pesi *(attraverso `Lambda_k = somma_{h in k} |phi_h|^2`)*. Il secondo
### **non era implementato**, e il gradiente che ne viene e'

```
(dG/dphi*_h)_peso  =  (dG/dcs_k) * (dcs_k/dLambda_k) * (dLambda_k/dphi*_h)
                   =  [ H_k^nodo + somma_{a in k} (dw_a/dcs_k) H_a^arco ] * cs'(Lambda_k) * phi_h
                   =  Omega_k * phi_h                        (h nel nodo k)
```

### ✅ **Quindi il pezzo e' `i dphi_h/dt = Omega_k phi_h`**, cioe'
### **`phi_h -> phi_h exp(-i Omega_k tau)`** -- ### **una FASE, uguale per tutte le
estremita' dello stesso nodo**, e ### **`psi` non si tocca.**

### ⛔ **E IL TEMPO E' `dtau`, NON `dtau_nodo`**, e questo va derivato invece di
copiarlo: i pezzi di oggi applicano `exp(-i H_k dtau_nodo)` con
`dtau_nodo = dtau * cs_k`, che e' ### **`exp(-i (cs_k H_k) dtau)`** -- cioe'
### **il parametro di flusso della composizione e' `dtau`**, e il generatore e'
### **`cs_k H_k`.** ### **Il pezzo nuovo e' un altro addendo dello STESSO generatore**,
quindi ### **va integrato per `dtau * frazione`**, con `dtau` ### **il tick**.
### ⚠ **Se usasse `dtau_nodo` sarebbe `cs_k Omega_k`, cioe' UN'ALTRA legge** -- e il
collaudo del tempo proprio ### **non lo vedrebbe**, perche' anche quella dipende da
`dtau`.

### ⭐ **`dw_a/dcs_k`, DERIVATA E VERIFICATA** *(e non si riscrive la media armonica:
si deriva la stessa funzione)*: con `w = 2xy/(x+y)`,
### **`dw/dx = 2y^2/(x+y)^2`.**
### ✅ **VERIFICATO CONTRO IL CODICE, prima di scriverlo:** la differenza finita di
`flussi_parziali.s_arco` *(la funzione che il passo chiama)* e la derivata analitica
coincidono entro ### **`1.3e-07`** con `h = 1e-7`, su `16` nodi -- e l'omogeneita' di
grado `1` *(`x w_x + y w_y = w`)* regge a ### **`2.2e-16`**, cioe' ### **al bit.**
### 📌 **E l'omogeneita' serve a due cose:** dice che il rapporto
`s_arco(con cs)/s_arco(senza cs)` ### **E'** `armonica(cs_i, cs_j)`, e da' il caso del
### **cappio** *(entrambi i capi nello stesso nodo)* ### **senza un ramo apposta**:
la' `dw/dx + dw/dy = 1`.

### ⭐⭐ **QUALI TERMINI DI `H` MUOVE LA FASE -- e quindi rendono `Omega` NON
COSTANTE** *(la correzione `n.10` del guardiano, e l'ho MISURATA)*:

| il termine | lo muove una fase uniforme nel nodo? | il numero |
|---|---|---|
| ### **`H^nodo`** *(i due Grover, la moneta, l'accoppiamento `N`)* | ### **NO** | `1.4e-14` su scala `5.8e+01` |
| ### **`H^arco`** *(i due spostamenti)* | ### **SI'** | ### **`1.5e+01`** su scala `4.8e+01` |

### ✅ **E IL PERCHE' DEL <<NO>> E' ESATTO, non numerico:** nel nodo la fase e'
### **la STESSA per tutte le estremita'**, quindi `|phi_h|` non cambia *(e con lui
`Lambda` e `N`)* e ### **`|somma_h phi_h|^2` nemmeno** -- la fase ### **esce dalla
somma.** ### ⛔ **Sull'arco NO:** i due capi stanno in ### **nodi diversi**, quindi
### **la fase RELATIVA cambia**, e con lei `Re(conj(f0) f1)`.
### 📌 **Quindi `Omega` si muove SOLO attraverso il termine d'arco del vuoto**, ed
e' ### **una cosa precisa da collaudare**, non una vaghezza.

### ⛔⛔ **COSA NON SO, e lo scrivo adesso**
### `a)` ### **se basta un punto fisso o serve altro.** Il pezzo e'
### **implicito** *(`Omega` dipende dallo stato che il pezzo cambia)*, e la scelta
### **simmetrica** -- `Omega` valutato ### **a metA' del pezzo**, a punto fisso -- e'
### **del secondo ordine e reversibile**, cioe' ### **non rompe il palindromo.**
### ⚠ **Ma se non convergesse, il mandato dice di RELAZIONARE, non di scegliere un
altro schema** *(la stessa regola di `D2`)*.
### `b)` ### **quanto costa.** Due punti fissi per tick *(`cs` e `Omega`)*, e il primo
costa gia' ### **da `7` a `74` giri** *(misurato)*.
### `c)` ### **se `C4` tiene il verso.** La risposta statica e'
### **la misura che puo' dire NO alla strada `(d)`**, e ### **se il verso si inverte si
ferma: e' fisica, e la legge Luca.**

---

## 2. PROGETTAZIONE — *i passi, e i criteri FISSATI QUI*

### ⛔⛔ **IL POSTO NEL PALINDROMO, DERIVATO**

### `1)` **Il vincolo e' UNO: la sequenza deve restare PALINDROMA**, perche' e' da li'
che viene il secondo ordine *(`M-B2`: `1.965` col palindromo, `0.837` con l'ordine di
prima)*. ### **Quindi il pezzo nuovo compare DUE VOLTE a frazione `0.5`, in posizioni
simmetriche** -- e l'ordine passa da `12` a `14` voci, ### **che resta PARI**, quindi
### **il centro continua a esistere** *(`meta_del_palindromo` ALZA se e' dispari)*.
### `2)` **Fra le posizioni simmetriche l'ordine di convergenza NON cambia** *(cambia la
costante)*: ### **la scelta non e' determinata dall'accuratezza**, e dirlo e' parte della
derivazione.
### `3)` ### **E ALLORA LA DECIDE UN ALTRO VINCOLO, che e' verificabile:**
`percorri_tick` chiama `al_primo(st)` ### **dopo il PRIMO pezzo**, e `deriva.fotografo` lo
usa. ### **Mettere il pezzo nuovo in posizione `1` cambierebbe il significato di quella
fotografia** *(e i numeri di chi la usa)*. ### ✅ **Quindi va in posizione `2` e
`13`** -- ### **appena DENTRO `CAMM-MATERIA-VUOTO`**, che resta il primo pezzo.
### ✅ **E la posizione `1`/`14` si MISURA come informazione**, per far vedere che
### **la pendenza e' la stessa**: cosi' la scelta ### **non e' un'opinione.**

| | il passo | cosa DECIDE | cosa mi FERMA |
|---|---|---|---|
| `1` | `Omega` in un modulo di fisica, e `pezzi_di_h` che ne diventa il LETTORE | che i termini di `H` abbiano ### **UNA fonte**, non due | -- |
| `2` | la legge in tabella *(riga, scheda, impronta, registro)* e il suo operatore | il pezzo esiste e ### **gira dall'ordine** | il generatore ### **RIFIUTA** *(e la cura e' la tabella, non il controllo)* |
| `3` | il punto fisso di `Omega`, e il suo tetto | l'errore `n.10`: ### **il flusso NON e' esatto** | ### **non converge** -> si relaziona |
| `4` | `cs` SPENTO: ### **il passo AL BIT** | che la legge sia ### **inerte a default** | un bit che si muove -> ### **STOP** |
| `5` | `C1`..`C5` | la strada `(d)` ### **regge o no** | un criterio che cade -> ### **si relaziona, e la scelta torna a Luca** |

### ⛔ **I CRITERI, COPIATI DAL MANDATO PRIMA DELLA MISURA:**
### **`C1`** con `cs` DINAMICO la pendenza di `G` su `>= 4` dimezzamenti e'
### **`>= 1.9`** *(oggi, senza il termine: `-0.001` -- ed e' il caso che DEVE fallire,
### **gia' misurato**)*;
### **`C2`** caso che DEVE fallire: ### **col SEGNO di `Omega` invertito la pendenza di
`G` cade**;
### **`C3`** `D0`, `D1` *(invarianza di scala: ### **`Omega` deve risultare invariante per
`lambda`**, perche' `cs'` scala come `1/lambda^2` e `H` come `lambda^2` -- ### **va
verificato**)*, `D2` *(secondo ordine sullo stato)* e `D3` *(tempo proprio, `PTheta` su
`8` stati entro `8` ulp, norme `M` e `V`)* ### **rigirati col termine ACCESO**, e
### **il criterio `(2)` di `D3` si legge su `G`**;
### **`C4`** la risposta ### **STATICA** *(il protocollo di `371731f`, accensione
dichiarata e uguale)*: ### **il vuoto si ritira ancora vicino alla sorgente?** Verso,
pendenza e sovrapposizione ### **accanto ai numeri di oggi.** ### ⛔ **Se il verso si
inverte: STOP e si relaziona.**
### **`C5`** il costo: ### **giri dei punti fissi per tick** *(`cs` e, se serve,
`Omega`)*, sui ### **sette rapporti** della spazzata di `402a4d5`.

### ⛔ **E SE UN CRITERIO CADE: non si allarga NESSUNA banda e non si aggiunge
NIENTE.** Si relaziona coi numeri, e ### **la scelta torna a Luca.**

---

## 3. TODO DEL NEXT STEP

1. `primo_ordine/energia_pesata.py`: `termini_di_h` *(i pezzi di `H`, UNA fonte)*,
   `pesi_dal_cs`, `d_peso_arco`, `omega`. ### **E `_misura_mb2.pezzi_di_h` diventa il suo
   LETTORE.**
2. La legge in `leggi.yaml` *(riga + ordine a `0.5` in posizione `2` e `13`)*, la scheda
   ### **generata**, l'impronta nuova, la riga del registro dell'era `2`
   *(`P-E6`)*, e la scheda in `REGISTRO_FISICA` *(`H-REG-R`)*.
3. L'operatore: ### **la fase a punto fisso**, col tetto dichiarato e il motivo.
4. Il braccio `0`: ### **`cs` spento -> `M-B1` al bit e distanza del passo intero `0`.**
5. `C1`..`C5`, e ### **l'informazione sulla posizione `1`/`14`.**
6. I referti ### **dal blob committato**, la `RIPRESA`, la relazione, lo stato di `D` in
   coda.