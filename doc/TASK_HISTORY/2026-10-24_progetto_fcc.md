# IL PROGETTO DEGLI STRUMENTI DELLA FCC, SULLA CARTA

> **Il mandato:** di Luca, «chiudere il capitolo dei triangoli e progettare gli strumenti della FCC», parte `2` *([[PIANO-2D-3D]]; [[DECISIONE-SOLO-TRIANGOLI]]; il dossier `doc/DOSSIER_S1_S4.md`)*.
> ### **NESSUN CODICE, NESSUNA DECISIONE DI LUCA PRESA.** ### **Il documento e' `doc/PROGETTO_FCC.md`.**

### ⛔ **UN MIO ERRORE, DICHIARATO:** ### **questo task history doveva entrare PRIMA del documento** *(`365012e5`, poi questo, poi il progetto)*; ### **il mio comando di copia ha fallito in silenzio** *(un percorso
`/c/...` dentro una stringa di Python su Windows)* ### **e il progetto `doc/PROGETTO_FCC.md` e' entrato in `bb7619f0` SENZA il task history prima, il cui messaggio dice il falso** *(«il task history nel commit
prima»)*. ### **L'ordine che git mostra e' dunque: il progetto, POI il task history. Il contenuto qui e' quello scritto prima del progetto** *(negli appunti)*, ### **non riscritto.**

### ⚠ **L'ORDINE DEI COMMIT:** ### **il mandato dice «due commit, nell'ordine delle parti»; `CLAUDE.md` par.`8` vuole il task history PRIMA del lavoro, e prevale:** ### **parte `1`; questo task history; il progetto.**

**LIVELLO:** un progetto sulla carta.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica.** 2. **Il gradino:** ### **il progetto degli strumenti, non la misura.** 3. **Aggiunge un numero o una legge?** ### **No: ogni scelta di Luca resta un PARAMETRO.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Il reticolo FCC e' imposto** *(un gradino tecnico verso lo spazio che emerge, `D9`: `doc/PIANO_2D_3D.md`)*.

## 1. IL RAGIONAMENTO PRELIMINARE

- ### **DAL CODICE** *(letto, non dai commenti)*: ### **`_triangoli.toro_spostamenti` e `scena_toro` sono GIA' generali in dimensione** *(`nn = prod(lati)`, gli spostamenti come tuple)*: ### **la scena FCC e' una COSTANTE e un `lati` di
  tre elementi.** ### ⚠ **La trappola: `zip(c, s, lati)` TRONCA in silenzio: un `lati` di due elementi con spostamenti a tre perde la `z`.**
- ### **NON sono generali:** ### **`matrice_tick`** *(`fft2`, `lato x lato`)*, ### **`ruota60` e `scarto_c6`** *(la rotazione di `60` gradi del piano)*, ### **i blocchi `A(k)` e la curvatura** *(due fasi `theta_1`, `theta_2`)*, ### **la coppia a `K`**
  *(un punto dei triangoli)*.
- ### **IL VUOTO:** ### **`VUOTO = 1.0` per estremita'** *(`_triangoli.VUOTO`)*: ### **`Lambda0 = 2d = 12` per nodo.** ### ⚠ **La regola di scala FRA geometrie e' una domanda aperta di Luca** *(`doc/PROGETTO_TRIANGOLI.md`: si tiene fisso il vuoto per
  estremita', o `Lambda` per nodo?)*: ### **il progetto la lascia parametrica.**
- ### **NON SO:** ### **dove sta il salto minimo sulla FCC** *(sui triangoli era `K`, che non ha un analogo diretto)*; ### **il costo esatto** *(le stime sono da tempi misurati in 2D)*.

## 2. LA PROGETTAZIONE

### **Per ogni punto del mandato: che cosa serve, che cosa si riusa, che cosa si scrive, il controllo di servizio** *(nel documento)*. ### **Le stime di costo dai tempi MISURATI nel repo** *(`stato_finale_R2T.txt`:
la camminata sui triangoli `3.9`-`4.9 us` per nodo e tick)*, ### **scalate col numero degli archi** *(`d 3 -> 6`)*: ### **dichiarato come stima, non come misura.**

## 3. TODO DEL NEXT STEP

1. questo task history, da solo; 2. `doc/PROGETTO_FCC.md` e la relazione.
