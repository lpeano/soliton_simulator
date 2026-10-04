# dettaglio di `CLAUDE.md` par.11 — **le regole di lavoro**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col loro numero o id. Non rimanda ad altri file di `doc/REGOLE/`.)*

## `P1` — non usare l'associazione senza verificare lo storico

Prima di proporre una diagnosi o una cura, **rileggi dal DISCO** cio' che e' gia'
stabilito su quel punto, e verifica di **non contraddire un fatto gia' misurato**.
### **Le frasi *«manca X»*, *«il problema e' Y»*, *«basta fare Z»* sono IL SEGNALE
D'ALLARME.** Se non trovi nulla sul punto, **dillo**: *«sto proponendo per analogia»*.

### \u26d4 **IL CASO PIU' COSTOSO E' MIO, del 2026-10-04:** nel commit `6a` avevo misurato
il primo evento di divisione al passo **`42`**; nel `6b` ho scritto **`74`**,
### **stessa scena nominale e stesso seme**, e l'ho messo in tre documenti come *«un numero
misurato che corregge il piano»*. ### **Due misure incompatibili sullo stesso oggetto, e
non ho fatto la domanda.** La causa era un attributo scritto a mano che faceva girare il
sigillo su un'altra scena — ### **ma la spia era nel mio referto del giorno prima.**

## `P2` — forza il sistema o lo corregge?

Escludere un **forzante** *(turbo)* **protegge** la misura; escludere una **correzione**
significa **misurare un sistema che si sa difettoso**. Lo stato di ogni componente sta in
`doc/COMPONENTI_PROMOSSE.md`.

## `P1-quater` — ogni sostituzione si asserisce per se'

Si usa un helper che **conta l'ancora e fallisce se non e' unica**, **una sostituzione alla
volta**. ### \u26d4 **Un `assert` globale del tipo `t != originale` e' soddisfatto dalle
ALTRE sostituzioni**, e lascia passare in silenzio quella che non ha attaccato.

### **E nei patch script NIENTE ESCAPE:** si usa **`chr()` o `replace`**. ### **Le ancore
si tengono ASCII**, perche' un carattere accentato o un simbolo scritto come escape
**non combacia** col file vero.

### **Le patch si lanciano IN PRIMO PIANO.**

## `L-PATCH` e `H-STASH` — perche' lo stash non serviva mai

`L-PATCH` *(regola di Luca, 2026-09-26)*: **non si fa `git stash` con una patch in corso**.
### \u26d4 **L'ho violata TRE VOLTE IN DUE GIORNI**, sempre per committare **un
sottoinsieme di file**, sempre dichiarandolo **dopo**, e ogni volta scrivendo che
*«scriverlo non basta»* — che e' `A9`.

### \u2705 **LA STRADA GIUSTA, e non serviva lo stash nemmeno una volta:**
`git add <i file>` e `git commit`. **Git committa SOLO L'INDICE:** il resto **resta sul
disco, intatto**. ### **Nelle tre violazioni lo stash era un giro in piu' che introduceva
un rischio** — una patch a meta' messa via, e poi ripresa — **per ottenere una cosa che
git fa da se'.**

### **Dal 2026-10-03 e' `H-STASH`: BLOCCATO, non sconsigliato.**

## `L-NUMERI` — ogni numero esce da uno script

Ricopiare a mano e' un'operazione **senza presidio**: ### **un numero ricopiato non ha
provenienza, uno generato ce l'ha.** *(Assorbe `P1-ter`, che lo diceva per le sole
tabelle.)*

## `L-UN-PROMPT` e `L-DOPO-STOP`

**Un prompt alla volta:** i rilievi che arrivano durante un lavoro **vanno in CODA**, non
lo interrompono — ### **un lavoro interrotto a meta' lascia il repo in uno stato che
nessuno ha dichiarato.**

**Dopo uno `STOP`, se Luca non risponde, si lavora SOLO la coda:** nessuna cura fisica,
nessun run lungo, **nessuna decisione presa al suo posto**.

## `L-STELLA` — le cinque domande

Si rispondono **per iscritto** nel task history di ogni commit che cambia la fisica,
**anche solo con *«non si applica, perche' …»*** — e ### **il «perche'» e' parte della
risposta.**

| | la domanda |
|--:|---|
| 1 | `A14`: conserva energia e carica **localmente**? |
| 2 | a quale dei **tre gradini** di `ROBUSTEZZA-FISICA` arriva il risultato? |
| 3 | aggiunge un numero o una legge, e di che **tipo**? Compensa un difetto? |
| 4 | tocca `rho`, `c_s` o il **segno**, e in quale **verso** dell'accoppiamento? |
| 5 | **emergente o imposto**: sopravvive se si toglie la legge pratica? |

### \u26d4 **E' una REGOLA SCRITTA, NON un presidio: nessun hook la controlla** *(`A9`)*.
