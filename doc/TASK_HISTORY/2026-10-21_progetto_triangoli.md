# IL PROGETTO DELLA GRIGLIA A TRIANGOLI SUL TORO, PENSATO PER LA FCC IN 3D *(su carta)*

> **Il mandato:** decisione di Luca del `2026-10-21` alle `14:08`, con l'aggiunta delle `14:14`.
> ### **Un PROGETTO: nessun codice di fisica, nessuna corsa.** Impronta `2e7f795d2a52fbe7` e
> `leggi.yaml` intatti. ### **Le scelte di fisica sono di Luca.**

**LIVELLO CORRENTE:** `L2`.

## 0. LA MOTIVAZIONE DI LUCA, alla lettera

> ### **«I triangoli si scelgono come LA FISICA PIU' PULITA (nessun numero da tarare, geometria
> dalle sole connessioni), NON come cura dell'instabilita'. Stella Polare, domanda 5: una
> geometria scelta per ragioni sue; se poi stabilizza, e' un RISULTATO, non un rimedio.»**

## 1. LA STELLA POLARE

1. **`A14`:** ### **non si applica al progetto** *(nessuna legge cambia oggi)*; ### **si
   applichera' a ogni legge riscritta** sulla griglia nuova: il progetto dice per ognuna se la
   sua conservazione locale va rifatta *(sez. `f` del documento)*.
2. **Il gradino:** ### **non si applica:** e' un progetto. ### **Ogni gradino del piano**
   *(2D, poi FCC)* ### **ha i suoi criteri di STOP** *(sez. `k`)*.
3. **Aggiunge un numero o una legge?** ### **Il progetto deve dirlo:** ### **la griglia non
   aggiunge numeri** *(e' topologia)*; ### **la moneta ha GIA' un numero** *(`eps`, oggi `0.5`,
   «il valore del banco», origine aperta)*: ### **la domanda dei sottogruppi finiti e' se la
   simmetria lo FISSA.**
4. **Tocca `rho`, `c_s` o il segno?** ### **Tocca come si contano** `rho` e `Lambda` per nodo
   *(`6` o `12` estremita' invece di `4`)*: ### **il progetto dice come si confrontano.**
5. **Emergente o imposto?** ### **E' la motivazione di Luca:** ### **una geometria scelta per
   ragioni sue**; ### **se stabilizza, e' un risultato.**

## 2. RAGIONAMENTO PRELIMINARE — che cosa credo PRIMA di progettare

- **Dove credo che stia la difficolta' VERA:**
  - ### **NON nel grafo ne' nei pezzi senza parametri:** il Grover *(il `2/d` viene dal grado)* e lo spostamento *(per arco)* ### **sono gia' scritti per un grado qualunque** *(letto in `leggi.yaml`: «NON HA PARAMETRI ... il `2/d` viene dal GRADO del nodo»)*;
  - ### **nella MONETA:** e' l'unico pezzo con un numero *(`eps`)* e con le direzioni `n_h` *(«geometriche»: oggi vengono da `scena_l2.versori_geometrici`, cioe' dall'asse dell'arco del toro quadrato)*. ### **Senza posizioni, le direzioni devono essere un DATO DEL GRAFO REGOLARE.**
  - ### **nella REGOLA DI SCALA FRA GEOMETRIE:** con `6` estremita' per nodo, ### **a vuoto per estremita' uguale `Lambda` per nodo passa da `4` a `6`**; e `S3` e `cs` leggono ### **rapporti** *(la precisazione di Luca delle `11:45` del `2026-10-20`)*. ### **Quale grandezza tenere fissa nel confronto 4 contro 6 vicini e' una scelta di Luca.**
  - ### **in `M-B1`**: e' il raccordo AL BIT col motore vecchio, ### **che e' quadrato**: ### **sulla griglia a triangoli non ha un termine di confronto**, e va sostituito con un altro raccordo.
- **Sui sottogruppi finiti, che cosa credo PRIMA del conto:** ### **le `n_h` sono assi DOPPI** del gruppo di simmetria della griglia *(nel piano per il diedrale; le diagonali delle facce per l'ottaedrico)*, e ### **un elemento di `SU(2)` di rotazione attorno a un asse doppio, dentro il doppio ricoprimento, e' solo la rotazione di `pi`**: ### **credo che il sottogruppo finito fissi `eps dtau = pi/2`** *(mod `pi`)*, ### **la stessa risposta su quadrato, triangoli e FCC.** ### **Da verificare nel documento, non da assumere.**
- **Cosa NON so:** se la camminata coi triangoli ha ancora la `C`-simmetria e `PTheta` *(dipendono dalla moneta e dall'ordine)*; ### **quanto costa la FCC** *(`72` reali per cella)*.

## 3. PROGETTAZIONE

- ### **Il documento `doc/PROGETTO_TRIANGOLI.md`**, con le sezioni `a`-`k` del mandato, ### **e per OGNI voce la sua forma FCC** *(e se una scelta 2D non si generalizza, la proposta che si generalizza)*.
- ### **I numeri del documento:** dalle formule *(gli angoli diedri, gli ordini dei gruppi)* o ### **da comandi scritti accanto** *(i conti dei collaudi e dei referti)*: ### **nessun numero ricopiato.**
- ### **Le domande per Luca, UNA alla volta**: la prima, ### **i gradi di liberta' che la derivazione della moneta lascia liberi, e se un sottogruppo finito di `SU(2)` li fissa.**
- ### **La voce `[[GRIGLIA-A-TRIANGOLI]]`** aggiornata con la procedura dell'indice: la motivazione, il progetto, la FCC. ### **Resta `AGENDA`.** ### **Nessuna voce nuova.**

## 4. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `doc/PROGETTO_TRIANGOLI.md`, la voce, la relazione: un commit, `PUSHATO`, `FERMO` *(la domanda e' di Luca)*.
