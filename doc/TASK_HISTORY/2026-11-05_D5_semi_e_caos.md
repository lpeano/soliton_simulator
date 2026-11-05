# 2026-11-05 — `D5`: I SEMI DI RUMORE E LA CRESCITA DEL CAOS *(Luca; l'aggiunta del `2026-11-03` `20:23`; la voce `6` della coda)* -- **COL BORDO O SENZA: LA PROPOSTA, FERMO PRIMA DI PARTIRE**

> **`D5` come sta nel repo** *(la relazione, `2026-11-03`, «L'ORDINE DELLE SOMME E IL CAOS»)*: la partenza di `TP1000` piu' un rumore relativo `1e-10`, `1e-8`, `1e-6`, semi dichiarati prima, su `F0`; per ogni seme la distanza dalla corsa di riferimento, **il tempo di `e`-folding contro i `~25` di `D0R`**, la direzione; le letture (o1), (o2) di Luca; **il tempo letto sul tratto di CRESCITA** *(in `D0R` da `~577` a `~1400`)*, la finestra dichiarata prima dei numeri. **Il mandato del `2026-11-04` `18:31`:** FERMO prima di partire; nel task history la proposta motivata, col bordo o senza.

## 1. LE PREMESSE *(dal repo)*
- ### **IL BORDO NON CAMBIA LA CRESCITA DEL CAOS NELLA SUA FINESTRA:** `TBS` *(la partenza di `TS` col bordo)* **rompe la simmetria negli stessi tempi di `TS` senza bordo** *(psi sopra `1e-12` a `528` contro `565.5`, `1e-6` a `1081.5` contro `1092`, `1e-2` a `1441.5` contro `1381.5`: `diag_tbs_volo.txt`)*. **La finestra della crescita** *(`~577 .. 1400`)* **finisce prima che il bordo conti:** al bordo la materia arriva piu' tardi *(in `TB3` l'alone a `t 1500` era `~0.00002`)*.
- ### **MA IL BORDO TOGLIE LA CORSA:** `TB3` non parte entro `30000` *(la velocita' massima `0.8` per `1000`)*. **La direzione della corsa** *(una delle tre misure di `D5`: «la direzione la sceglie il rumore», la lettura di `D0R`)* **col bordo NON si puo' misurare**, perche' la corsa non c'e'.
- **Il vuoto:** `D5` e' scritto su `F0`; **`F3` e' il vuoto predefinito delle prove nuove** *(Luca, dopo `eaa5e3ec`)*. **Su `F0` la freccia di fondo anticipa la partenza** *(la lettura (f1))*: per la direzione scelta dal rumore, **`F3` e' piu' pulito** *(nessun asse imposto dal vuoto)*.
- ### **UNA SOVRAPPOSIZIONE CON `TL120`:** il pilota proposto per `TL120` *(`doc/TASK_HISTORY/2026-11-05_TL120_densita_o_rientro.md`)* e' **la partenza di `TF3` piu' il rumore `1e-10`, `4` semi, `F3`, senza bordo, fino a `30000`**: ### **sono semi della famiglia di `D5`.** Le stesse corse darebbero lo sparpaglio delle partenze *(`TL120`)* **e** l'`e`-folding e la direzione *(`D5`)*.

## 2. LA PROPOSTA *(FERMO: decide Luca)*
- ### **`D5` SENZA bordo, su `F3`, con la partenza di `TF3`:** l'`e`-folding si misura uguale *(il bordo non conta nella finestra, `TBS`)*, **e la direzione della corsa si puo' misurare solo senza bordo.** **I semi:** `1e-10` *(`4` semi, quelli del pilota di `TL120`)*, piu' `1e-8` e `1e-6` *(`1` seme l'uno, per la dipendenza dall'ampiezza)*.
- ### **IL RIFERIMENTO e' `TF3`** *(la stessa partenza senza rumore: i suoi jsonl ci sono, `0 .. 16000`, e `TF3C` fino a `30000`)*: la distanza di ogni seme da `TF3` campione per campione.
- **Il costo:** `6` corse *(`4 + 1 + 1`)*, **`~3.01` ore l'una fino a `30000`** *(`diag_tl120_costo.txt`)*: **`~18` ore**; **se `D5` si ferma alla fine della finestra della crescita** *(`~1500` piu' la direzione, che vuole la corsa: almeno fino alla partenza)*, meno. **Con il pilota di `TL120` in comune, le `4` corse a `1e-10` contano una volta sola.**
- **Le finestre, dichiarate prima** *(come chiede `D5`)*: **la crescita** fra la distanza `1e-8` e `1e-2` *(sopra il pavimento, sotto la saturazione)*; **la direzione:** il primo blocco sopra `5` per `1000` *(la partenza di `TL120`)*, la direzione di quel blocco.

## 3. LE DOMANDE A LUCA
1. **Senza bordo, su `F3`, con la partenza di `TF3`** *(invece di `F0` e `TP1000`)*?
2. **I semi e le ampiezze** *(`4` a `1e-10`, `1` a `1e-8`, `1` a `1e-6`)*, e **la comunione col pilota di `TL120`**.
3. **Le finestre** *(la crescita fra `1e-8` e `1e-2`; la direzione al primo blocco sopra `5` per `1000`)*.
