# RISCRIVERE IL SIMULATORE IN **Go**: ne trarremmo vantaggio?

> **Domanda di Luca, 2026-09-27.** Risposta breve: **no, non oggi — e il motivo non e' la
> velocita': e' che la riscrittura azzererebbe i SIGILLI e i PRESIDI, che sono l'unica ragione per
> cui i numeri di questo repo si possono credere.**
>
> **⚠ E LA PARTE SULLA VELOCITA' E' UN'INFERENZA, NON UNA MISURA:** **non esiste un profilo del
> simulatore**, e non l'ho fatto. Chiunque dica *«in Go andrebbe N volte piu' veloce»* — me
> compreso — sta stimando. **Quello che segue e' misurato dove lo dico, e inferito dove lo dico.**

## 1. CHE COSA C'E' DA RISCRIVERE — **misurato**

```
soliton_simulator.py ............ 10 592 righe, 164 funzioni, 3 classi
  chiamate `np.` ................  1 754        <- il lavoro vero e' TUTTO vettoriale
  `np.add.at` ...................     54        <- scatter-add: in Go si scrive a mano
  indicizzazione con maschere ...     67
  scipy (cKDTree, csgraph) ......     22        <- KD-tree e grafi sparsi: da riscrivere
strumenti sotto `csv/` .......... 361 script
  che dipendono dall'INTROSPEZIONE di Python ... 122  (34 %)
```

**I `122` non sono un dettaglio: sono i presidi e i sigilli.** Dipendono da cose che **in Go non
esistono**:

| che cosa fanno oggi | dove | in Go |
|---|---|---|
| **importano il simulatore DUE VOLTE nello stesso processo**, con nomi diversi, per confrontare due versioni | `_cli_flag.carica_dal_cli` *(`spec_from_file_location`)* | **non esiste**: un binario e' uno |
| **eseguono il TESTO del driver fino a un'ancora** e catturano l'argv che ha costruito | `_cli_flag.argv_del_driver` *(`exec(compile(...))`)* | **non esiste** |
| **elencano i flag leggendo i globali del modulo** *(`vars(S)`)*, cosi' una cura nuova entra da se' | `_cli_flag.scarto_dal_driver` → `H-P5` | si riscrive come registro esplicito, **e perde la proprieta' che lo rende un presidio** |
| **sostituiscono un metodo a runtime** per contare quante volte gira | il sigillo di `D32` *(`S.Rete.mitosi = spia`)* | si riscrive con un'iniezione dichiarata, cioe' **modificando il codice sorvegliato** |
| **leggono l'AST del proprio sorgente** per dire dove sta una legge | `H-P3`, `H-P8`, `N3` di `D32`, `RAMPA-1` | esiste `go/ast`, **ma va riscritto tutto** |

## 2. DOVE Go VINCEREBBE DAVVERO — e quanto vale qui

**Vincerebbe** su: il **GIL** *(vero parallelismo su lavoro per-nodo e per-arco)*, il **costo di
avvio** *(misurato oggi: `~1.2 s` di import per processo, e i sigilli ne lanciano 2-4 per giro)*, e
l'**allocazione** *(oggi ogni passo crea array temporanei)*.

**Ma i costi che ho misurato oggi non sono costi dell'interprete:**

```
costruzione della scena (ii)(a), 12 814 nodi ....... 25.8 s   <- KD-tree + saturazione: C
una misura di OSSERVABILE-P1 (Dijkstra, 471k archi)   9.1 s   <- scipy csgraph: C
import del simulatore ..............................  1.2 s
```

**Il tempo sta in kernel che sono GIA' compilati.** Riscriverli in Go significa **ri-implementare
numpy e scipy per la parte che serve**, e il guadagno atteso e' *«pari o meglio, se scritti bene»* —
**non un ordine di grandezza gratuito**.

## 3. IL COSTO CHE NON SI VEDE NEL CONTO DELLE RIGHE

1. **UNA RISCRITTURA NON PUO' ESSERE BYTE-IDENTICA.** Il punto 1 di ogni sigillo (`par.2`) e'
   *«flag OFF = byte-identico»*, e le firme sono **`sha1` dei byte degli array**. Fra due
   linguaggi l'ordine delle somme cambia, e **cambia l'ultimo bit**. Quindi **ogni sigillo andrebbe
   ristabilito da zero**, non ri-girato: non *«passa ancora»*, ma *«che cosa vuol dire adesso»*.
2. **TUTTI I NUMERI DIVENTANO DI UN'ALTRA EPOCA** (`par.9-bis`). I `12 814` nodi, i `471 143`
   archi, la `sd` fra semi di `OSSERVABILE-P1`, le `214` firme di `D32`: **nessuno di questi si
   confronta** con la versione Go. **Si riparte dal termine di paragone.**
3. **I NOVE HOOK andrebbero riscritti**, e sono la cosa che questa settimana ha preso quasi ogni
   difetto: `H-RIGHE` ha rifiutato un mio commit, `H-INDICE` due, `H-P5` uno, e `N5` — un criterio
   nato da un hook mancante — ha scoperto che **`net.step()` non e' un passo** e che un sigillo
   misurava codice mai eseguito. **Durante la riscrittura quei presidi non ci sono**, ed e' la
   finestra in cui i difetti entrano.

## 4. E IL PUNTO CHE DECIDE: **la velocita' non e' il collo di bottiglia**

**Il bersaglio del progetto sono le tre prove di `doc/IPOTESI_gravita_a_spinta.md`**, e oggi non
sono eseguibili. Cio' che le blocca sta in `doc/SMISTAMENTO_run_base.md`: **`6` voci `SI`**, e
**nessuna di esse e' «il simulatore e' lento»**. Sono difetti di **legge** e di **misura**.

> **Una riscrittura consumerebbe mesi e azzererebbe i sigilli, senza spostare nessuno dei sei.**
> `STANDARD 10` applicato al progetto invece che a una cura: **non aumenta il numero delle leggi,
> aumenta il numero delle cose da ri-dimostrare.**

## 5. CHE COSA FAREI INVECE — in ordine di costo

1. **UN PROFILO. Non ce l'abbiamo, e senza quello ogni scelta e' un'opinione** *(`A9`: una
   decisione senza misura non e' una decisione)*. Costo: un pomeriggio.
2. **Se il profilo indica pochi punti caldi:** kernel nativi mirati *(Cython, `numba`, o una
   libreria in Go/Rust chiamata dal Python)* **lasciando lo scheletro e TUTTI i presidi dove sono**.
   Questo **non** rompe la byte-identita' se il kernel e' deterministico, e si sigilla come
   qualunque cura.
3. **Se il costo e' il numero di PROCESSI** *(i sigilli a 2-4 bracci)*: riusare lo stesso processo
   dove `STANDARD 1` lo permette, o tenere una scena costruita in cache.
4. **Se un giorno servisse Go**, il momento giusto e' **dopo** che le tre prove sono eseguibili e i
   difetti bloccanti sono chiusi: allora la riscrittura avrebbe **un termine di paragone vero** —
   *«la versione Go riproduce questi risultati»* — invece di essere il termine di paragone di se stessa.

## ⚠ COSA QUESTA VALUTAZIONE **NON** DICE

- **non dice che Go sia peggio di Python** per questo problema: dice che **il guadagno e' sui punti
  caldi, che non abbiamo misurato**, e che **il costo e' sui presidi, che abbiamo contato** *(`122`
  script su `361`)*;
- **non dice che il simulatore sia veloce.** Dice che **non so dove sia lento**, e che il numero
  che deciderebbe — un profilo — **non esiste**;
- **non e' una decisione:** decide Luca. **La voce nell'indice e' `RISCRITTURA-GO`**, col criterio
  di chiusura: **un profilo che mostri il tempo concentrato in codice Python** *(non in kernel C)*
  **per una frazione che giustifichi la riscrittura.**
