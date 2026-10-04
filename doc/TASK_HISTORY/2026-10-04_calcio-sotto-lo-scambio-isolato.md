# IL CALCIO SOTTO LO SCAMBIO `a<->b`, **ISOLATO** — *mandato di Luca, 2026-10-04*

**Punto 2 del mandato.** *Solo misure: il simulatore `0f060670` **non si tocca**.*
**Scritto e committato PRIMA del codice** *(par.8)*.

---

## LA STELLA POLARE — **le cinque risposte, scritte PRIMA del lavoro** *(`L-STELLA`)*

> ### ⚠ **Questo e' un mandato di MISURA, non di fisica nuova. Le cinque domande si
> ### rispondono comunque**, perche' `L-STELLA` non fa l'eccezione *«tanto non cambio
> ### niente»* — e perche' una misura progettata male **afferma** fisica anche senza
> ### scriverla.

**① `A14` — questa legge conserva energia e carica LOCALMENTE?**
### **NON SI APPLICA, e il perche' e' che non introduco nessuna legge:** questo lavoro
**misura una simmetria** di leggi che esistono gia'. ### ⚠ **Ma c'e' un <<ma>>, e va scritto
PRIMA:** il calcio della mitosi **somma a `phi` dei genitori** una quantita' che **non e'
antisimmetrica** fra `a` e `b` *(vedi la ③)*, e `phi` e' la grandezza in cui vive la materia.
### **Se la misura confermera' l'asimmetria, il materiale e' per `A14`:** un termine
`comune` che **non si media a zero** fra i due genitori e' precisamente *«una sorgente»*.
**Lo registro come materia per `DIVISIONE-AUTOCONSISTENTE`, non come un difetto da curare
qui** *(punto 3 del mandato)*.

**② A quale dei TRE GRADINI arriva il risultato?**
### **Al gradino `(a)`, e solo a quello: robusto al rumore numerico.** La misura e'
un'**identita' fra due esecuzioni della stessa funzione sullo stesso stato**, quindi non ha
barra d'errore statistica: uno scarto e' `0` o non lo e'. ### ⛔ **NON arriva al `(b)`**
*(non tolgo nessuna legge pratica)* ### **ne' al `(c)`** *(non c'e' un limite noto con cui
confrontare un'asimmetria di scambio)*. ### **E un gradino dichiarato basso e' un risultato,
non una scusa.**

**③ Aggiunge un numero o una legge? Di che tipo?**
### **NESSUN numero nuovo nel simulatore.** Lo strumento usa `FRAZ_NASCITA = 0.4` **solo nel
controllo che deve fallire**, su una **COPIA** — e `0.4` **non e' una taratura**: e' un valore
**qualunque diverso da `0.5`**, scelto perche' il mandato lo nomina. ### **Se il controllo
funzionasse solo a `0.4` sarebbe un difetto dello strumento**, e il collaudo lo prova con un
secondo valore.
### 📌 **E LA DOMANDA VERA DELLA ③ CADE SU CIO' CHE MISURO:** il calcio contiene
`comune = KICK_TW * sciolta * (mod - 0.5)`, dove `0.5` **non e' `FRAZ_NASCITA`**: e' il
**centro della saturazione** `mod = tau/(1+tau)`. ### **Sono due `0.5` con due ruoli, e il
file lo dichiara gia'.** `KICK_TW` e' una **costante di accoppiamento** *(legittima, va
dichiarata)*; `mod - 0.5` e' un **ricentramento**, non un clip. ### **Nessun
pavimento/tetto/clip entra in questo lavoro.**

**④ Tocca `rho`, `c_s` o il SEGNO? In quale verso dell'accoppiamento?**
### **IL SEGNO: SI', ED E' IL CUORE DELLA MISURA.** Lo scambio inverte `(i,j)` **e il segno di
`tw`**. Il calcio legge `sciolta = |tw|/PHI_CRIT` e `tau = 1+|tw|/PHI_CRIT`: ### **entrambi in
VALORE ASSOLUTO, quindi il segno di `tw` NON entra nel calcio.** Ci entra invece
`perc_chi[a]` e `perc_chi[b]`, cioe' la **chiralita'**. ### **Il verso e' <<curvatura -> EM>>:**
la torsione dell'arco *(geometria)* decide la **forza** del calcio, la chiralita' decide il
**verso**, e il calcio muove `phi` *(fase, cioe' EM)*. ### ⚠ **Il verso inverso --
`EM -> curvatura` -- NON e' in questa misura**, e lo dichiaro: non guardo se il calcio
retroagisce sulla metrica.

**⑤ Emergente o imposto: sopravvive se si toglie la legge pratica?**
### **LA DOMANDA SI RIBALTA, e vale la pena dirlo invece di rispondere di riflesso.** Qui non
osservo un *fenomeno* che una legge pratica potrebbe produrre: osservo una **proprieta' di
simmetria del codice**. ### **La <<legge pratica>> sospetta e' `MITOSI_DIR`**, che sposta la
fase del figlio verso il genitore piu' teso ed e' **per costruzione asimmetrica in `a`/`b`**.
### ✅ **Per questo la misura gira con `MITOSI_DIR = 0`** *(il default)*: ### **se
l'asimmetria comparisse solo con `MITOSI_DIR != 0` sarebbe IMPOSTA; se compare a
`MITOSI_DIR = 0` e' nel calcio stesso.** E `ANTIFASE_ADD` va guardato per la stessa ragione:
estrae dal generatore e puo' ribaltare `fm`.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare*

### **PERCHE' LA MISURA ESISTE: due buchi, entrambi DICHIARATI dai referti stessi**

| | il buco | dove e' scritto |
|---|---|---|
| **①** | `_verso_archi` gira su **1 passo** e in quel passo le nascite sono **ZERO** | il suo referto: *«se in questi passi NON ci sono nascite, il calcio della mitosi NON HA AGITO»* |
| **②** | invertire **TUTTI** gli archi mescola `memoria_hebbiana_moto` **con la mitosi** | `_misure_calore`: `memoria_hebbiana_moto` ha `sum d_Q2 = +3.8423e+05`, ### **l'unica voce che muove `Q2` oltre a `step` e `chiudi`** |

### ⛔ **Quindi la misura di oggi non e' <<la stessa, meglio>>: e' la PRIMA che puo'
### attribuire qualcosa al calcio.** Arriva al passo in cui la divisione **avviene**, e
inverte **solo** gli archi che si dividono.

### **CIO' CHE HO LETTO DAL CODICE** *(e non dai commenti: par.2)*

Il calcio, in `mitosi`, ramo `REGIME == "deterministico"` *(l'unico che gira)*:

```
sciolta  = |tw[sel]| / PHI_CRIT
tau_a    = 1 + |tw[sel]| / PHI_CRIT
mod      = tau_a / (1 + tau_a)
chi_a    = perc_chi[a]        chi_b = perc_chi[b]
comune   = KICK_TW * sciolta * (mod - 0.5)
calcio_a = comune + 0.5 * KICK_TW * sciolta * chi_a * mod
calcio_b = comune - 0.5 * KICK_TW * sciolta * chi_b * mod
```

E le due grandezze del figlio:

```
D          = _wphi(phi[a] - phi[b])
fm         = (phi[a] - FRAZ_NASCITA * D) % dphi            # con MITOSI_DIR = 0
pos_figlio = (1 - FRAZ_NASCITA) * pos[a] + FRAZ_NASCITA * pos[b]
```

## 2. LE ATTESE, **dichiarate PRIMA** e col conto che le produce

### ✅ **`pos_figlio` a `t = 0.5`: SIMMETRICO.**
`0.5*pos[a] + 0.5*pos[b]` e' invariante allo scambio. ### **E il file dichiara gia' che la
forma convessa a `t=0.5` e' identica al bit a `0.5*(x+y)`: `0` differenze su `2 000 000`.**

### ✅ **`fm` a `t = 0.5`: SIMMETRICO**, e il conto non e' ovvio, quindi lo scrivo:
sotto lo scambio `D -> _wphi(phi[b]-phi[a]) = -D`, quindi
`fm' = (phi[b] + 0.5*D) % dphi`. E poiche' `phi[b] = phi[a] - D` *(modulo `dphi`)*:
`fm' = phi[a] - D + 0.5*D = phi[a] - 0.5*D = fm`. ### **Simmetrico.**
### ⚠ **E UN CASO LIMITE CHE DICHIARO ORA:** `_wphi` e' **dispari** *(`_wphi(-x) = -_wphi(x)`)*
**tranne esattamente sul taglio** *(`|D| = pi` su `2pi`)*, dove `+pi` e `-pi` sono lo stesso
punto ma **un solo rappresentante** esce dalla funzione. ### **Se un arco cadesse sul taglio,
`fm` potrebbe differire di `dphi` e NON sarebbe un'asimmetria fisica.** Lo strumento deve
**contare** quanti archi stanno sul taglio e dirlo, invece di attribuirmi un'asimmetria che e'
una convenzione di wrap.

### ⛔ **IL CALCIO: ASIMMETRICO, e il conto dice ANCHE DI QUANTO.**
Il nodo che in BASE sta nello slot `a` riceve `comune + c*chi_a` con
`c = 0.5*KICK_TW*sciolta*mod`. Nello SCAMBIO **lo stesso nodo fisico** sta nello slot `b`, e
riceve `comune - c*chi_a` — ### **perche' lo slot `b` legge `perc_chi` del nodo che ci sta,
e quel nodo e' sempre lo stesso.** Quindi:

> ### 📌 **ATTESA QUANTITATIVA:**
> ### **`delta_phi(nodo a) = 2*c*chi_a = KICK_TW * sciolta * chi_a * mod`**, e lo stesso per
> ### `b` con `chi_b`. ### **Zero se e solo se `chi = 0`.**

### **E L'ASIMMETRIA HA DUE SORGENTI DISTINTE, che la misura deve separare:**

| | sorgente | sparisce se |
|---|---|---|
| **①** | il **SEGNO**: `+0.5` su `a`, `-0.5` su `b` | mai: e' nella forma |
| **②** | la **CHIRALITA' LETTA**: `chi_a` per `a`, `chi_b` per `b` | `chi_a == chi_b` |

### ⚠ **E SE RISULTASSE `chi_a == chi_b` SU TUTTI GLI ARCHI SELEZIONATI, l'asimmetria
### misurata sarebbe solo la ①, e io avrei <<confermato>> meno di quel che credo.**
### **Lo strumento deve riportare `chi_a` e `chi_b` arco per arco**, altrimenti non so quale
delle due sorgenti sto vedendo.

### **COSA NON SO, e non voglio indovinare**

1. ### **Se la selezione degli archi sia invariante allo scambio.** `decidi_divisione` usa
   `avv = |tw|` *(invariante al segno)* e un criterio di densita' `0.5*(I[a]+I[b])`
   *(simmetrico in `a`,`b`)*, e **estrae dal generatore**. ### ⛔ **Credo che sia invariante,
   e se NON lo fosse il confronto sarebbe fra DUE EVENTI DIVERSI, cioe' senza senso.**
   ### **Va VERIFICATO dallo strumento, non assunto** — ed e' una condizione di validita',
   non un risultato.
2. **Quanti archi si dividono al passo 42**, e se `ANTIFASE_ADD` scatta su qualcuno di loro
   *(ribaltando `fm` di mezzo dominio e rendendo il confronto di `fm` un confronto fra due
   rami diversi)*.
3. **Se al passo 70 lo Schwinger estragga la stessa coppia** nei due rami.
4. ### **Se `perc_chi` dei genitori sia diversa da zero.** Se fosse zero su tutti, l'attesa
   quantitativa darebbe `0` e **il calcio risulterebbe simmetrico per un motivo che non e' la
   simmetria della legge.** ### **E' un FALSO-ZERO, e va escluso misurando `chi`, non
   supponendolo.**

## 3. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa decide ciascuno*

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| **1** | scena dal **driver**: `nmasse` e `sep` **dall'argv**, seme `11` | che sia la scena del mandato | se `nmasse`/`sep` finissero scritti a mano: e' `H-P3`, ed e' **lo stesso difetto del `6b`** |
| **2** | si arriva al passo **41** *(quello PRIMA della prima divisione, il 42)* | lo stato di partenza | se al 42 non ci fosse nessun candidato: la scena non e' quella misurata |
| **3** | si **sonda** `decidi_divisione` su una copia **usa-e-getta** per sapere `sel` | quali archi invertire | se `sel` fosse vuoto |
| **4** | due copie profonde: **BASE** e **SCAMBIO** *(solo su `sel`: `(i,j)` invertiti e `tw` di segno opposto)* | il confronto | — |
| **5** | **lo stesso stato del generatore** in entrambe | che la differenza sia solo lo scambio | se il generatore divergesse, ogni scarto sarebbe rumore |
| **6** | **solo `mitosi()`**, su ciascuna | — | — |
| **7** | ### **si VERIFICA che le due abbiano selezionato gli STESSI archi** | la **validita'** del confronto | ### ⛔ **se la selezione differisce: FERMO.** Non e' un risultato: e' un confronto fra due eventi diversi |
| **8** | confronto con **rinumerazione**: nodi per indice, **archi nuovi per INSIEME degli estremi** | il verdetto per grandezza | — |

### ⛔ **PERCHE' GLI ARCHI NUOVI NON SI CONFRONTANO PER POSIZIONE.** La nascita scrive
`i = [i[keep], a, m]` e `j = [j[keep], m, b]`: i due archi nuovi sono **`a-m`** e **`m-b`**.
### **Sotto lo scambio diventano `b-m` e `m-a`: i due archi si scambiano di ruolo E di
orientamento.** Confrontare *«il primo arco nuovo col primo arco nuovo»* misurerebbe **lo
scambio che ho fatto io**, non la fisica. ### **Si accoppiano per INSIEME degli estremi
`{estremo, m}`, e si riporta anche l'orientamento.**

### **IL CONTROLLO CHE PUO' FALLIRE, come il mandato lo fissa**

Una copia con **`FRAZ_NASCITA = 0.4`**. Li':
`pos_figlio = 0.6*pos[a] + 0.4*pos[b]` contro `0.6*pos[b] + 0.4*pos[a]`,
### **differenza `0.2*(pos[a]-pos[b])`, cioe' NON NULLA** *(salvo `pos[a] == pos[b]`)*.
### ⛔ **Lo strumento DEVE trovarla. Se non la trova e' CIECO, e il mandato dice: FERMATI.**
### ✅ **E a `0.4` anche `fm` diventa asimmetrico** *(`phi[a]-0.4D` contro `phi[a]-0.6D`,
differenza `0.2*D`)*: ### **due grandezze indipendenti che il controllo deve scoprire, non
una.**

### ⚠ **E IL CONTROLLO VA FATTO CON DUE VALORI, non solo `0.4`.** Un controllo che passa a
`0.4` e **solo** a `0.4` non prova che lo strumento vede le asimmetrie: prova che vede
`0.4`. **Secondo valore: `0.3`.**

## 4. TODO DEL NEXT STEP

1. **lo strumento**, in `csv/_test_fork/`, con `_presidio.avvia`, `nmasse`/`sep` **dall'argv**,
   e il **collaudo** coi due valori di `FRAZ_NASCITA`;
2. **la voce d'inventario nello stesso commit** *(par.6 ①)*, col blob;
3. **commit dello strumento PRIMA di girarlo** *(par.5)*;
4. **il run**, staccato e non bufferizzato;
5. **il referto**: per ogni grandezza **simmetrica / asimmetrica / con quale scarto**, e per
   le asimmetriche **la riga di codice che la produce**;
6. **la ripetizione per lo Schwinger** al passo `70`, con `aa` e `bb`;
7. ### **NIENTE CURE** *(punto 3 del mandato)*: le asimmetrie vanno in
   `DIVISIONE-AUTOCONSISTENTE` come **materia per la LEGGE**, che viene **dopo l'energia**.
   ### **La forma della cura la decide Luca.**

### ⚠ **E UNA COSA CHE NON FARO', per non ripetere il `6b`:** non scrivero' `nmasse` e `sep`
**a mano** nello strumento. ### **Il `6b` ha sigillato una scena da `2208` nodi credendola
quella del driver da `~12800`, e il numero sbagliato (`74` invece di `42`) e' arrivato fino a
`FATTI_dal_codice.md`.** ### **La scena si legge dall'argv, e lo strumento STAMPA `n` perche'
chi legge possa riconoscere la scena sbagliata.**
