# LA TRADUZIONE DELLE LEGGI DEL SIMULATORE IN TERMINI DI `H` — **e il freno che manca alla sonda**

> **Mandato di Luca, 2026-10-08.** ### ⛔ **Lavoro di LETTURA e di CARTA:** nessuna corsa
> lunga, ### **nessuna modifica al simulatore** *(resta `b8c21049`)*, `ASSIOMI.md` non si tocca.
> ### ✔ **Verificato all'avvio:** `git pull` già allineato, blob
> `b8c21049b85ba36a828f49dfa225d42419f3baf5`, `12` voci bloccanti su `953` — ### **nessuna
> tocca un lavoro di lettura** *(bloccano le corse base)*.

## 1. RAGIONAMENTO PRELIMINARE — **cosa credo PRIMA di guardare, e cosa NON so**

### ⭐ **LA COSA CHE IL MANDATO MI INSEGNA, E CHE NON AVEVO:** la sonda del prototipo
*(`hopping + (g/2)|ψ|⁴`)* ### **è una scelta MIA, non una traduzione delle leggi di Luca.**
L'ho scritta come se fosse «la forma al primo ordine», e invece è ### **una forma da manuale**
*(Schrödinger non lineare discreta)* ### **presa in prestito.** ### ➜ **Il collasso su un nodo
del `v2` è quindi un fatto SULLA SONDA, non sul modello** — e la precisazione di Luca dice
### **quale pezzo del modello manca alla sonda: il freno.**

| | cosa credo prima di guardare |
|---|---|
| ### **il censimento** | i censimenti che esistono *(`MEMORIE_MANCANTI` con le `34` variabili di stato, `FRECCE-IMPOSTE`, le quattro leggi in più di `D2-BIS`)* ### **coprono la maggior parte** delle leggi, ma ### **non tutte**: credo che manchino le leggi della ### **topologia** *(archi che nascono e muoiono)*, che nessun censimento di *variabili* vede, perché cambiano la ### **forma** dello stato, non il suo valore |
| ### **la classe più grossa** | ### **TRADUCIBILE CON UNA MEMORIA.** Il simulatore è pieno di gradi di libertà lenti *(`tw`, `d0`, `peq`, `omega_s`, `mem_mot`)* che ### **inseguono** un bersaglio: un inseguimento è un ### **rilassamento**, e un rilassamento è la derivata di un'energia ### **solo se** il grado lento sta ### **dentro** `H` *(`A16.3`)* |
| ### **il caso che deve fallire** | la coppia spinoriale del driver ### **NON è traducibile così com'è**, e il numero è ### **già misurato**: `1.054` di scarto contro la forma `U(2)`, e `1.18e-01` contro `-∂U/∂φ`. ### ✔ **Non è una previsione: è un fatto che riuso come controllo** |
| ### ⛔ **cosa NON so** | ### **se la nascita dello spazio, scritta coi due vincoli di Luca, basti davvero a impedire il collasso.** La divisione `ψ_p → ψ_p/√2` conserva `Σρ` ma ### **DIMEZZA `Σρ²`** — che è esattamente la quantità che il collasso massimizza. ### **Credo che sia il freno, ma il conto va fatto, non asserito** |
| ### ⛔ **e cosa NON so, 2** | ### **da dove viene l'energia dello spazio nuovo.** Oggi è il ### **bagno globale**, ed è misurato *(`B-SCAL` `164` nascite col bagno, `B-SCAL-TS` `0` senza)*. ### **Quale termine di `H` la paghi nel vuoto LOCALE non lo so**, e non lo invento |

### ⚠ **E UN'ABITUDINE MIA DA CUI MI GUARDO, scritta prima:** quando una legge «quasi» deriva
da un'energia, la tentazione è ### **chiamarla traducibile e aggiungere l'eccezione in nota.**
### ⛔ **`9-ter` dice il contrario:** se serve un'eccezione, la legge ### **non è** quel
gradiente, e va nella classe che le spetta.

## 2. PROGETTAZIONE DEL RAGIONAMENTO — **i passi, cosa decide ciascuno, cosa mi FERMA**

| passo | che cosa decide | che cosa mi farebbe fermare |
|---|---|---|
| `0` **i documenti** | che la sonda sia dichiarata ### **mia**, e che la precisazione di Luca sullo spazio entri ### **prima** del censimento, così la classificazione la può usare | — *(è carta)* |
| `1` **il censimento** | ### **l'elenco delle leggi**, cercate ### **PER FORMA e non per nome** | se il censimento trova una legge che ### **nessun documento** nomina ### **e** che cambia la fisica, lo dico prima di classificarla |
| `2` **la classificazione** | la classe di ogni legge, e per le traducibili ### **il termine `E_x` scritto per intero** | una legge che ### **non so** scrivere: va in ### **aperto**, non in traducibile |
| `3` **la verifica** | ### **se `E_x` è davvero l'energia di quella legge**: identità algebrica ### **più** differenza finita locale col pavimento calcolato | una traducibile che ### **non passa**: ### **cambia classe**, e lo scrivo |
| `4` **il documento** | la `H` candidata, la regola di crescita ### **a parte**, e ### **l'elenco delle decisioni di Luca** | — |

### ⛔ **LE LETTURE SI FISSANO QUI, prima di vedere i numeri:**

| | la soglia |
|---|---|
| **traducibile** | identità algebrica `max\|legge − ∂E/∂x\|` ### **sotto il pavimento di macchina calcolato** sui termini di quella somma, ### **non** contro una costante |
| **la differenza finita** | scarto relativo ### **sotto `1e-6`** su almeno `3` nodi scelti ### **dove la grandezza è grande** *(dove è zero non discrimina)* |
| ### ⛔ **il caso che DEVE fallire** | la coppia spinoriale del driver deve dare uno scarto ### **ben sopra** il pavimento. ### **Se PASSA, il mio banco è rotto** e mi fermo |

## 3. LE PREVISIONI, PRIMA DI CONTARE *(quante leggi per classe)*

| id | la previsione |
|---|---|
| **`PT-1`** | il censimento trova ### **fra `24` e `32`** leggi che muovono lo stato |
| **`PT-2`** | ### **TRADUCIBILE: `7`** — la coppia scalare, la repulsione, il legame elastico, l'inerzia della fase, il termine di Schwinger, e due che non so nominare prima |
| **`PT-3`** | ### **TRADUCIBILE CON UNA MEMORIA: `6`** — `tw`, `d0`, `peq`, `omega_s`, `mem_mot`, e la dinamica dei pesi `w` |
| **`PT-4`** | ### **CRESCITA DELLO SPAZIO: `4`** — mitosi, Schwinger, la creazione di archi, la scomparsa di archi. ### ⚠ **E la SCOMPARSA mi mette in difficoltà: `A14.2` dice che la crescita è l'unica freccia ammessa, quindi un arco che muore è GIÀ una violazione**, non una legge da tradurre |
| **`PT-5`** | ### **NON TRADUCIBILE: `5`** — il termostato, `scuoti_vuoto`, `_smorza` *(`D31`)*, lo smorzamento `beta·vd`, e `K_SYNC` |
| **`PT-6`** | ### **DIAGNOSTICA: `3`** |
| **`PT-7`** | ### ⭐ **LA PREVISIONE CHE CONTA, e che posso perdere:** la divisione `ψ_p → ψ_p/√2` ### **impedisce il collasso**, perché conserva `Σρ` ma ### **dimezza il contributo `ρ²` del nodo che divide** — cioè toglie ### **esattamente** ciò che il collasso guadagna. ### ⛔ **Se invece il conto dà che il nodo diviso ri-collassa sui due figli, la nascita NON è il freno, e lo dico** |
| **`PT-8`** | ### **la massa critica e la repulsione, insieme, fanno già oggi da freno nel simulatore** — e credo che il prototipo collassi ### **proprio perché non ha né l'una né l'altra** |

### ⚠ **`PT-4` E `PT-7` SONO SCRITTE PER POTER PERDERE**, ed è il punto: se la nascita non frena,
l'ipotesi del guardiano del punto `0(c)` ### **cade**, e il freno va cercato altrove.

## 4. LA STELLA POLARE — *le cinque risposte*

| | la risposta |
|---|---|
| **1 `A14`** | ### **non si applica al codice di questo giro** *(non gira fisica nuova)*, ### **ma è IL TEMA:** la classe ### **NON TRADUCIBILE** è l'elenco delle violazioni di `A14`, e la classe ### **CRESCITA** chiede per la prima volta ### **che forma avrebbe la nascita se conservasse** |
| **2 i tre gradini** | ### **(c) coincide con un limite noto:** ogni traducibile si verifica contro il gradiente del suo `E_x`, e il collaudo del potenziale di `D2-BIS` *(`1.49e-15`)* è ### **il precedente che dice che il banco funziona**. ### ⛔ **(a) e (b) non si applicano: non c'è una corsa** |
| **3 numeri o leggi** | ### ⛔ **NESSUNA legge nuova e NESSUN numero nuovo entrano nel simulatore.** Il documento ### **propone** forme e le marca ### **candidate**; `H` candidata e regola di crescita sono ### **decisioni di Luca** |
| **4 `rho`, `c_s`, il SEGNO** | ### **toccato di striscio:** `peq` insegue `rho` ed è un candidato a termine di pressione. ### **Il segno non lo decido io in questo giro** |
| **5 emergente o imposto** | ### ⭐ **È LA DOMANDA DEL MANDATO.** Una legge ### **TRADUCIBILE** è emergente *(viene da un'energia)*; una ### **NON TRADUCIBILE** è ### **imposta**, e il documento la nomina tale invece di lasciarla implicita |

## 5. TODO DEL NEXT STEP — **la lista operativa**

1. `0(a)` la sonda dichiarata ### **del guardiano** in `RISCRITTURA_PRIMO_ORDINE` e nei ### **due** referti del prototipo *(`v1` e `v2`)*; il grafo fisso dichiarato ### **impalcatura**.
2. `0(b)` la sezione ### **«LO SPAZIO NASCE DALLA MATERIA»**, coi cinque punti e ciascuno marcato ### **deciso / candidato / aperto**.
3. `0(c)` il risultato del ### **MARE `v2`** letto come ### **assenza di freno nella sonda**, con l'ipotesi del guardiano marcata ### **come tale**, e il `PR` del Perron *(`24.6` contro `348.2`)*.
4. ### **Commit `0` DA SOLO.**
5. Il censimento ### **per forma**, col metodo dichiarato, e i flag presi da ### **`csv/_configurazione.py`**, non dai default del modulo.
6. La classificazione nelle cinque classi, con `E_x` scritto per intero dove la classe lo chiede.
7. La verifica sullo snapshot ### **solo per le traducibili**, col caso che deve fallire.
8. `doc/TRADUZIONE_IN_H.md` con la tavola, la `H` candidata, il confronto con la sonda e ### **l'elenco delle decisioni di Luca**.
9. ### ⛔ **Poi FERMARSI.**
