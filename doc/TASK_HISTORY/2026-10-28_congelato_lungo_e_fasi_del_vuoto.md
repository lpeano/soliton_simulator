# 2026-10-28 — IL CONGELATO LUNGO E LE FASI DEL VUOTO *([[VUOTO-SUL-FONDO]], [[PROGETTO-MASSA-COLLETTIVA]]; la risposta di Luca delle `15:49` a `f2c646e3` e `83daa823`)*

> ### **LIVELLO: una lettura del codice** *(punto `3`)*; ### **una corsa LUNGA del solo congelato a `s 0.3`, a pezzi** *(punto `2`)*; ### **nessun file del nucleo.**

## 0. LA RISPOSTA DELLE `15:49`, PER INTERO

```
RISPOSTA DI LUCA (2026-10-28 15:49) A f2c646e3 E 83daa823, sulla raccomandazione del guardiano

1. IL FILTRO PROPOSTO: NO per ora. Lo stato del risolutore e' gia' lo stazionario del passo entro 3e-6 (83daa823): il
   filtro aggiungerebbe una tolleranza da scegliere (A1) senza un problema da risolvere. Resta descritto nel task history
   come opzione.
2. LA DERIVA DEL CONGELATO: si classifica con una corsa LUNGA del solo congelato, a s 0.3 (costa meno), la taglia grande
   (N 1e6 L 81) e una seconda (L 120), fino a 3000 di tempo fisico, a pezzi. Ogni 3 di tempo fisico: la larghezza, la
   frazione entro la larghezza iniziale, il picco. LA LETTURA, scritta PRIMA: (i) si stabilizza (un plateau) -- il
   solitone esiste; (ii) OSCILLA (un periodo e un'ampiezza che restano) -- il solitone esiste e respira; (iii) SCAPPA (la
   crescita accelera, o il picco crolla) -- l'instabilita' del 2D (S1 "sopra-critica in 2D"), e allora la prova di S4 in
   2D e poi il 3D. Il guardiano non sa quale; la non monotonia gia' vista (f2c646e3) fa pensare a (ii).
3. LE FASI DEL VUOTO (c0 di f2c646e3): leggi nel codice quale pezzo del passo fa arrivare alla materia le FASI del vuoto,
   e non solo Lambda (il moto, la moneta, il Grover, la fase del vuoto, dtau_nodo): file, righe, e il meccanismo.
   Correggi la frase "psi vede il vuoto solo attraverso Lambda" ovunque sia scritta. Nessuna corsa nuova se il codice
   basta.
4. LA MAPPA: la riga 4 (il solitone con la sua buca) con la rilettura (la vita relativa al congelato col fondo 1584-2867
   per T_r 25 e 100) e la deriva intrinseca, non dello stato di partenza.
```

## 1. RAGIONAMENTO PRELIMINARE

### **PUNTO `3`: CHE COSA HO LETTO DAL CODICE** *(il risultato e' questa lettura: nessuna corsa)*

- ### **L'ORDINE DEL PASSO** *(`composizione.ORDINE`, `14` pezzi, palindromo)*: ### **`CAMM-MATERIA-VUOTO` in posizione `0` e `13`;** ### **i pezzi del vuoto `CAMM-GROVER-VUOTO` e `CAMM-SPOSTAMENTO-VUOTO` in `5`-`8`, IN MEZZO.**
- ### **I PEZZI DELLA MATERIA NON LEGGONO `phi`:** ### **`motore._grover`** *(`FP.grover` su `st["psi_h"]`)*, ### **`motore._moneta_spin`** *(`psi = st["psi_h"]`)*, ### **`motore._spostamento_trasporto`** *(`FP.hop_psi` su `st["psi_h"]`)*. ### **`CAMM-FASE-VUOTO`** *(`energia_pesata.applica`, `primo_ordine/energia_pesata.py:375`)*: ### **con `mot.lambda_c is None` esce subito,** ### **e agisce comunque solo su `phi`.** ### **`flussi_parziali.dtau_nodo` legge `mot.dtau`, non lo stato.**
- ### **I PEZZI DEL VUOTO MUOVONO SOLO `phi`:** ### **`motore._grover_scalare`** *(`primo_ordine/motore.py:459`, `phi = st["phi_h"]`)* ### **e `motore._spostamento_scalare`** *(`primo_ordine/motore.py:688`, `FP.hop_phi`)*: ### **un Grover e un salto sugli archi, cioe' un'INTERFERENZA:** ### **`|phi|^2` per nodo DOPO dipende dalle FASI di `phi` PRIMA.**
- ### **L'UNICO PONTE e' `materia_vuoto.applica`** *(`primo_ordine/materia_vuoto.py:132`-`133`)*: ### **`lam = mot.densita_vuoto(st)` e `al, be = pezzi(rho, lam)` si calcolano AL MOMENTO DELLA CHIAMATA,** ### **e `alpha` ruota `psi`;** ### **e alla riga `146` la fase `beta(rho, Lambda)` ruota `phi`.**
- ### ⭐ **IL MECCANISMO, DENTRO UN TICK DEL CONGELATO** *(`phi` torna a `phi0` solo A FINE tick)*: ### **`(1)` in posizione `0` `Lambda` e' quello di `phi0` -- uguale al bit nelle due scene;** ### **la fase `beta` imprime su `phi` una fase che dipende da `rho`;** ### **`(2)` in `5`-`8` il Grover e il salto del vuoto fanno interferire le fasi di `phi`** *(quelle iniziali, diverse fra fondo e uniforme, piu' quella di `beta`)* ### **e cambiano `|phi|^2` per nodo;** ### **`(3)` in posizione `13` `materia_vuoto.applica` legge QUEL `Lambda`, e `alpha` lo porta su `psi`.** ### **Quindi `psi` sente le fasi del vuoto attraverso `Lambda` A META' TICK, non attraverso `Lambda` all'inizio del tick.**
- ### **LA CORREZIONE:** ### **la frase sbagliata e' solo nel mio task history** `doc/TASK_HISTORY/2026-10-28_rilettura_buca_e_deriva.md` *(sezione `1`, «col vuoto congelato `psi` vede `phi` solo attraverso `Lambda`»)*; ### **il task history non si riscrive: si ANNOTA** *(par.8)*, ### **e lo annoto li'.** ### **Il testo del `2026-10-13`** *(`2026-10-13_pe_hamilton.md`: «`E` dipende da `phi` solo attraverso `Lambda_k`»)* ### **e' un'altra affermazione, sul funzionale d'energia, e resta.**
- ### **Una conseguenza che il congelato non vede:** ### **«il vuoto congelato» non e' «il vuoto fermo»:** ### **dentro il tick si muove;** ### **e la corsa a `r = 0`** *(i pezzi del vuoto saltati)* ### **e' la sola con `phi` davvero fermo** *(la differenza `2.38e-03` di `(d2)` alla grande)*.

### **PUNTO `2`: CHE COSA CREDO PRIMA DI GUARDARE**

- ### **Come Luca, piu' la `(ii)`:** ### **la crescita non monotona, il salto al tick `20` e il ritorno al `40`.** ### **Circa `45%` `(ii)`, `30%` `(i)`, `25%` `(iii)`.**
- ### **Che la taglia `L 120` finisca piu' larga della `81`** *(in `74f99039`: `7.576` contro `7.344` a `600`)*: ### **la scatola conta, e questo sarebbe un segno di code.**

### **CHE COSA NON SO**

- ### **Quale scena usare:** ### **`74f99039` aveva il vuoto UNIFORME, le corse della buca il FONDO,** ### **e `(c0)` dice che non sono la stessa dinamica.** ### **Faccio le due** *(il costo e' piccolo)*: ### **l'uniforme ha il controllo al bit contro `74f99039`;** ### **il fondo e' quello della buca.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### **LO SCRIPT: `csv/_congelato_lungo.py`** *(N `1e6`, `s 0.3`, lo zero simmetrico, `S1`, `cs` spento come nelle corse)*

| | la scelta | il perche' |
|---|---|---|
| 1 | ### **`L 81` e `L 120`; il vuoto uniforme e il fondo: `4` corse** | ### **il mandato; sezione `1`** |
| 2 | ### **`10000` tick** *(`3000` di tempo fisico)*, ### **un punto ogni `10` tick** *(`3`)* | ### **il mandato** |
| 3 | ### **A PEZZI di `2000` tick:** ### **lo stato a fine pezzo in `db/congelato_lungo/*.npz`** *(ignorato da git, come i `.pkl`: il dato e' il comando)*, ### **i punti in un file per pezzo in `doc/referti_l2/congelato_lungo/`, mai riscritto** | ### **il riavvio notturno** |
| 4 | ### **i punti: la larghezza, la frazione entro `w_in` assoluta e relativa, entro `3 w0`, il picco, `M`** | ### **il mandato; e la frazione relativa come in `f2c646e3`** |

### **I CONTROLLI**

1. ### **`(kp)` DEVE: un pezzo spezzato in due col file di ripresa = lo stesso pezzo di fila, AL BIT** *(`40` tick: `20` + `20` contro `40`)*.
2. ### **`(k74)` DEVE: col vuoto uniforme le larghezze ogni `20` tick fino a `2000` = la corsa `simm` congelata di `74f99039` AL BIT, a `L 81` e a `L 120`.**
3. ### **`(n)` DEVE: `M` entro `1e-10` relativo in ogni corsa.**

### **LA LETTURA, SENZA SOGLIE MIE** *(le soglie sarebbero numeri da scegliere: `A1`)*: ### **il referto stampa, per finestre di `500` di tempo fisico, la pendenza media di `w/w_in`, l'ampiezza** *(massimo meno minimo)* ### **di `w/w_in` tolta la retta della finestra, il picco relativo medio;** ### **e il periodo dominante delle oscillazioni nella seconda meta'** *(la trasformata della serie tolta la retta)*. ### **La classificazione `(i)`/`(ii)`/`(iii)` la scrivo io come LETTURA, coi numeri accanto.**

### **COSA MI FAREBBE FERMARE**

- ### **`(kp)` fallito: i pezzi non sono una corsa sola; FERMO.**
- ### **`(k74)` fallito: lo stato non e' quello di `74f99039`; FERMO sull'uniforme** *(il fondo non ha quel riferimento)*.

## 3. TODO DEL NEXT STEP

1. ### **questo task history, committato da solo, PRIMA dello script;**
2. ### **lo script e la voce d'inventario, committati prima della corsa;** ### **l'annotazione nel task history della rilettura** *(la frase corretta)*;
3. ### **le `4` corse a pezzi; il referto; la RELAZIONE; la MAPPA** *(la riga `4`: la rilettura e la deriva intrinseca)*.
