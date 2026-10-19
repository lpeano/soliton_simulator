# `D4` — IL VERSO E IL PROFILO DI `cs`, COI TRE RAPPORTI

> **Il mandato:** il punto `D4` del task history `2026-10-17_D_cs_lambda_nel_motore.md`
> *(criteri GIA' fissati, che ### **non si cambiano**)*, piu' le protezioni del
> `2026-10-19` dal mandato di Luca. ### **Viene dopo la rimozione del ramo del punto medio**
> *(`3b467aa4`)*, quindi ### **misura il passo di oggi.**
> **LIVELLO CORRENTE:** `L2`. ### **`D4` MISURA, e non aggiunge leggi.**

## 0. LA STELLA POLARE — *le cinque risposte, PRIMA del codice*

1. **`A14`:** ### **non si applica come domanda su una legge nuova**, perche' `D4` non ne
   aggiunge: misura il passo di oggi. ### ⚠ **E la sorgente FOTOGRAFATA viola la
   conservazione PER COSTRUZIONE** *(la «massa di prova» di `statica_protocollo`: genera il
   campo e non lo subisce)* -- ### **e' uno strumento di misura, non una legge**, e non entra
   in nessuna tabella.
2. **Il gradino:** `(a)` le barre fra blocchi di tempo *(`>= 3`)*, a due `dtau`;
   `(b)` ### **il caso che DEVE fallire: senza sorgente `cs` resta uniforme AL BIT** -- il
   fenomeno sparisce togliendo cio' che lo produce; `(c)` ### **NON raggiunto**: non c'e' un
   limite noto di `cs(Lambda)` *(il confronto con la natura e' `alpha_G/alpha`, dopo `L4`)*.
3. **Aggiunge un numero o una legge?** ### **No.** `Lambda_c` c'e' gia' ed e' **scelto**
   *(`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`)*: `D4` lo fa variare su `{0.1, 1, 10}` volte il
   vuoto medio ### **per dare a Luca i numeri, non per sceglierlo.** La rampa e la
   fotografia sono **strumento**, non legge.
4. **Tocca `rho`, `c_s` o il segno?** ### **Misura `c_s`**, nel verso **vuoto ->
   propagazione** *(curvatura -> EM)*: `D4` chiede ### **se `cs` CALA dove la materia caccia
   il vuoto.** Il verso opposto e' `L4`, e qui non c'e'.
5. **Emergente o imposto?** ### **L'effetto e' imposto dalla forma** *(`cs` e' scelta,
   `Lambda_c` e' scelto)*; ### **cio' che `D4` misura e' COME si distribuisce** *(il profilo,
   l'alone)*, ed e' il caso che deve fallire a dire che ### **senza sorgente non c'e'.**

## 1. I CRITERI, COPIATI DAL TASK HISTORY DEL `2026-10-17` *(senza modifiche)*

- per `Lambda_c/Lambda_medio` in `{0.1, 1, 10}`, ### **sorgente FOTOGRAFATA**,
  ### **accensione DICHIARATA e UGUALE per i tre valori**;
- `cs` ### **CALA** vicino alla materia con ### **`>= 3` barre**, a `dtau` `0.5` e `0.25`;
- `delta cs` ### **LINEARE** in `delta Lambda` per `x` piccolo, confrontato con
  ### **`Lambda_c/(Lambda_medio + Lambda_c)^2`**;
- il profilo radiale ### **in tabella**;
- il caso che DEVE fallire: ### **senza sorgente `cs` resta uniforme AL BIT**.

## 2. LA CONFIGURAZIONE INTERA, e le mie LETTURE OPERATIVE *(fissate qui, prima dei numeri)*

- **Il passo:** quello di oggi, ### **la legge DEL MOTORE** *(`statica_protocollo.SOSTITUISCI
  = False`: `CAMM-MATERIA-VUOTO` e `CAMM-FASE-VUOTO` come girano)*, con `cs` dinamico
  *(`tick.tick_con_cs`)*; l'impronta della tabella `2e7f795d2a52fbe7`; ### **il referto
  stampa lo sha1 dei byte dei file del percorso del tick.**
- **La scena:** quella del protocollo statico *(toro `31x31`, `VUOTO = 1`, `SEME = 7`,
  `RAGGIO = 1`, un grumo al nodo `0`)*. ### **`Lambda_medio` si calcola UNA volta dalla
  scena, e `Lambda_c = rapporto * Lambda_medio` si stampa come NUMERO** *(mappa, sez.`20`)*.
- **L'accensione:** ### **`statica_protocollo.T_ACCENSIONE[1] = 100` tick** *(la stessa di
  `C4`)*, ### **UGUALE per i tre rapporti e i due `dtau`**; la finestra da `T + 200`, `10`
  blocchi.
- ### ⚠ **LETTURA 1 -- la SORGENTE FOTOGRAFATA con la legge del motore:** la «fotografia» di
  `statica_protocollo` vive **nel termine sostituito**, e con la legge del motore ###
  **non agisce.** ### **Lo stesso effetto -- `rho` ferma in OGNI istante, non solo ai confini
  dei tick -- si ottiene con `congela = "pezzo"`** *(`psi` ripristinata dopo ogni pezzo)*.
  ### **E' la scelta, e la dichiaro.**
- ### ⚠ **LETTURA 2 -- quale `cs`:** ### **`mot.cs` dopo ogni tick**, cioe' ### **il `cs` che
  il passo ha USATO** *(al centro del palindromo)*. ### **Non `cs(Lambda)` dello stato**:
  quello sarebbe una funzione algebrica di `Lambda`, e il confronto di linearita' sarebbe
  ### **algebra, non una misura.**
- ### ⚠ **LETTURA 3 -- «CALA vicino alla materia»:** la media dei blocchi di
  `delta cs = cs(sorgente) - cs(senza sorgente)` ### **sui nodi del grumo** *(`r <= RAGGIO`)*
  e' ### **NEGATIVA con `>= 3` barre**, per ### **ogni rapporto e ogni `dtau`** che converge.
- ### ⚠ **LETTURA 4 -- «LINEARE per `x` piccolo»:** a `dtau = 0.5`, sulla scansione
  `statica_protocollo.X_SCAN` *(`0.01`-`1`, `TICK_SCAN = 1200`, `T_SCAN = 100`)*:
  `S(x) = <delta cs> / <delta Lambda>` sui nodi del grumo, e `R(x) = S(x) / cs'(Lambda_medio)`
  con `cs' = Lambda_c/(Lambda_medio + Lambda_c)^2`. ### **LINEARE se `|R - 1|` NON CRESCE
  quando `x` cala, e al `x` piu' piccolo `|R - 1| <= |delta Lambda|/(Lambda_medio + Lambda_c)
  + 3 barre di `R`.** ### **Il primo termine non e' una tolleranza scelta: e' la CURVATURA
  della forma** *(lo scarto di `cs(Lambda_m + d) - cs(Lambda_m)` dal suo sviluppo lineare
  e' `d/(Lambda_m + Lambda_c + d)` relativo)*.
- ### ⚠ **LETTURA 5 -- il caso che DEVE fallire:** nella corsa SENZA sorgente,
  ### **`max - min` di `mot.cs` sui nodi e' `0` esatto a OGNI tick.**

## 3. LE PROTEZIONI DEL `2026-10-19` *(dal mandato)*

- `(a)` ### **NON CONVERGENZA:** se `cs_al_centro` alza, il punto si registra ### **«non
  converge»** col tick, `Lambda` minimo e `Lambda_c`, e si va avanti. ### **Niente cure,
  niente schemi diversi.**
- `(b)` ### **per ogni corsa, come INFORMAZIONE: il minimo di `Lambda/Lambda_c`** su rete e
  tick.
- `(c)` ### **ogni osservabile di `G` usa `energia_pesata.g_dello_stato`.** ### ⚠ **`D4` non
  misura `G`**: la protezione si applica ### **a vuoto**, e lo dico invece di ometterlo.
- **Il profilo, come INFORMAZIONE** *(mappa sez.`1`, il criterio di uscita di `L2`)*:
  `(1)` `Lambda` non piu' invariante sotto il tick; `(2)` ### **l'alone**: oltre quale raggio
  `|delta cs|` supera `3` barre; `(3)` gli orologi che rallentano ### **INTORNO** alla
  materia, non solo dentro. ### **Nessun verdetto su `L2`.**

## 4. CHE COSA HO GIA' VISTO, PRIMA DEL CODICE *(una prova di costo, non tenuta)*

### **Venti tick per braccio**, per sapere il budget: ### **`0.1`-`0.16` s per tick** *(quindi
`D4` intero e' circa un'ora e mezza, in background)*. ### ⛔ **E GIA' LI': a rapporto `0.1`,
`dtau = 0.5`, il punto fisso di `cs` NON CONVERGE** entro `20` tick; e il minimo di
`Lambda/Lambda_c` scende a ### **`0.02`-`0.16`** ai rapporti `1` e `10`. ### **Cioe' `D4`
entra nel regime del ciclo di stamattina** *(`Lambda` sotto `Lambda_c`)*, e la protezione
`(a)` ### **servira'.** ### **Lo scrivo PRIMA, perche' l'ho visto prima.**

## 5. TODO

1. `csv/_misura_d4.py`: un braccio per processo *(`STANDARD 1`)*, i risultati scritti
   ### **mentre corrono** in un `jsonl`; committato prima della corsa.
2. la corsa in background, dal blob pulito.
3. il referto e la relazione.
4. la voce `DOMANDA-IL-VALORE-DI-LAMBDA-C` coi numeri di `D4`, ### **senza scegliere**.
5. il commit di soli documenti: la mappa *(sez.`1`, riga `L2`, e sez.`4`)* e `CLAUDE.md`
   par.`13`.
