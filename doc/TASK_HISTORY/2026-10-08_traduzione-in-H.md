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

## 5-bis. **IL CRITERIO DEL «NO»** — *integrazione di Luca, ricevuta PRIMA di classificare*

> ### ⭐ **IL RILIEVO, ed è giusto:** il metodo del punto `3` *(scrivere `E` e verificare
> `F = −∂E/∂x`)* ### **dimostra il SÌ ma non il NO.** ### ⛔ **Non trovare `E` NON prova che `E`
> non esista** — prova solo che io non l'ho trovata. ### **Senza questo, metà della mia tavola
> sarebbe stata «non ci sono riuscito» scritto come «non si può».**

### **(1) IL TEST DI INTEGRABILITÀ** — *non richiede di indovinare `E`*

Per ### **ogni** legge che muove una variabile ### **continua**, sullo snapshot della scena:

```
J_ij = dF_i / dx_j          (differenze finite, su un campione di nodi E DEI LORO VICINI)
asimmetria = || J - J^T || / || J ||        col PAVIMENTO NUMERICO CALCOLATO
```

| esito | che cosa significa |
|---|---|
| ### **simmetrica** entro il pavimento | ### ✔ **una `E` ESISTE**, anche se non è ancora scritta |
| ### **asimmetrica** | ### ⛔ **NON ESISTE in quelle variabili**, ed è un ### **«no» DIMOSTRATO** |

| | |
|---|---|
| ### **controllo positivo** | la ### **coppia scalare** *(gradiente noto, già verificato a `1.49e-15`)* deve risultare ### **simmetrica** |
| ### ⛔ **caso che DEVE fallire** | la ### **coppia spinoriale del driver** deve risultare ### **asimmetrica** |

### ⚠ **E DUE LIMITI DEL TEST, che dichiaro PRIMA di usarlo, perché non lo sopravvaluti:**

| | |
|---|---|
| ### **è la condizione di Poincaré** | `J` simmetrica ⇒ la forma è ### **chiusa** ⇒ `E` esiste ### **LOCALMENTE** *(su un dominio semplicemente connesso)*. ### **Sullo snapshot questo basta**, ma «esiste `E`» va letto ### **in un intorno dello stato misurato**, non globalmente |
| ### **vale nelle variabili scelte** | ed è esattamente ciò che Luca scrive: ### **«non esiste IN QUELLE VARIABILI»**. Una legge asimmetrica in `φ` può diventare il gradiente di qualcosa ### **in variabili diverse** *(è il caso della coppia spinoriale, che la forma `U(2)` riscrive in `ψ`)*, e la tavola lo dirà invece di nasconderlo |
| ### **le variabili reali** | il test, così com'è scritto, è quello delle variabili ### **REALI** *(`φ`, `d`, `tw`, `d0`, `peq`…)*, che sono la quasi totalità. Per uno stato ### **complesso** la condizione che corrisponde è l'### **hermitianità**, non la simmetria, e dove serve lo scrivo |

### **(2) LA RISCRITTURA SI MISURA** — *e c'è una soglia*

Se una legge diventa traducibile ### **solo dopo una riscrittura**, si riporta ### **quanto la
legge riscritta differisce dall'originale sullo snapshot**: scarto relativo, ### **per classe
`MASSE` e `VUOTO`**.

> ### ⛔ **OLTRE IL `10 %` NON È UNA TRADUZIONE: È UNA LEGGE NUOVA**, e va ### **nell'elenco
> delle decisioni di Luca**, ### **non** nella `H` candidata.

### ⭐ **E QUESTA SOGLIA PRENDE GIÀ UN CASO CHE CONOSCO:** la coppia spinoriale contro la forma
`U(2)` sta a ### **`1.054`** di scarto — cioè ### **il `105 %`**, dieci volte sopra. ### ➜ **La
forma `U(2) NON è una traduzione della coppia del driver: è una legge nuova**, e con questo
criterio va ### **fra le decisioni di Luca**. ### ⚠ **Senza questa regola l'avrei messa nella
`H` candidata**, e avrei chiamato «traduzione» un cambio di fisica del `105 %`.

### **(3) DUE INSTRADAMENTI AUTOMATICI** — *che tolgono il test dove non serve*

| se la legge… | va in… | e il test… |
|---|---|---|
| dipende da una ### **velocità** o dalla ### **storia** | ### **TRADUCIBILE CON UNA MEMORIA** | si fa ### **sul sistema esteso**, non sulla legge sola |
| è ### **a senso unico** — `np.where` su un segno, `clip` ### **da un lato** | ### **fra le FRECCE** *(non traducibile)* | ### ⛔ **non si fa**: una legge a senso unico non ha gradiente, e misurarne la jacobiana sarebbe un ### **FALSO-ZERO** *(nel ramo dove non agisce, `J = 0` è simmetrica)* |

### 📌 **E LE PREVISIONI SU QUESTO CRITERIO, scritte prima di applicarlo:**

| id | la previsione |
|---|---|
| **`PT-9`** | il test ### **sposta di classe almeno `2`** leggi che avevo previsto traducibili — e il motivo che mi aspetto è ### **la dipendenza dai vicini dei vicini**: una legge che legge `rho` del vicino e scrive sul nodo ### **non è simmetrica** a meno che la stessa quantità torni indietro |
| **`PT-10`** | il controllo positivo ### **passa** e il caso che deve fallire ### **fallisce**. ### ⛔ **Se il caso che deve fallire PASSA, il banco è rotto e mi fermo** |
| **`PT-11`** | ### **almeno una** legge che avrei scartato risulta ### **simmetrica** senza che io sappia scriverne la `E` — e allora va in ### **TRADUCIBILE, con `E` APERTA**, che è una casella che prima non avevo |

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

## 6. L'ANNOTAZIONE — **gli esiti delle undici previsioni**

*(Scritta dopo, come vuole il par.8: ### **sopra non si riscrive niente.** I numeri:
`doc/TRADUZIONE_IN_H.md`, generato dai quattro json.)*

| id | esito |
|---|---|
| **`PT-1`** | ### ⛔ **MANCATA, E DAL BASSO:** `21` righe contro un minimo di `24`. Il motivo e' ### **mio**, non del sistema: ho ### **raggruppato piu' grosso** di quanto avessi previsto — `419` scritture in `21` righe, perche' *«il rilassamento di `d0`»* e' ### **una** riga e ### **dieci** scritture |
| **`PT-2`** | ### ⛔ **MANCATA: `3` traducibili, non `7`** — ed e' `PT-9` che l'ha mangiata |
| **`PT-3`** | ### ✔ **PRESA ESATTA: `6`** |
| **`PT-4`** | ### ✔ **PRESA ESATTA: `4`.** E la difficolta' che dichiaravo si e' rivelata giusta: ### **la scomparsa di un arco e' GIA' una violazione di `A14.2`**, non una legge da tradurre, e sta nell'elenco di Luca come ### **difetto da decidere** |
| **`PT-5`** | ### **MANCATA per `+2`: `7` non traducibili, non `5`** — le due in piu' sono quelle che `PT-9` ha spostato |
| **`PT-6`** | ### **MANCATA, e NON la aggiusto:** `1` riga, non `3`. Ma quella riga copre ### **`231` nomi**: ### **`PT-6` contava le LEGGI, la tavola conta le RIGHE**, e le due cose non sono la stessa |
| **`PT-7`** | ### ⭐ **VINTA A META', E LA META' CHE PERDE E' QUELLA CHE CONTA.** La diluizione c'e' ed e' ### **esatta** *(`Σρ` al bit, `ρ²` del nodo dimezzato)*; ### ⛔ **ma la divisione ALZA `H` di `+199600`**, quindi ### **non avviene da sola.** ### ➜ **La nascita e' un freno SOLO SE il vuoto locale paga, e `S5` e' APERTO** |
| **`PT-8`** | ### **CONFERMATA come lettura, NON come misura:** la tavola nomina ### **tre** freni nel simulatore *(repulsione, massa critica, nascita)* e ### **zero** nella sonda. ### ⚠ **Che siano loro a impedire il collasso NON e' misurato**, e non lo scrivo come se lo fosse |
| **`PT-9`** | ### ⭐ **VINTA, E DI PIU':** dicevo ### **almeno `2`** spostamenti, ### **ne ha fatti `4`** — sincronizzazione, coppia del driver, `_smorza`, massa critica |
| **`PT-10`** | ### ✔ **PRESA:** il controllo positivo passa *(`4.39e-13`)* e il caso che deve fallire fallisce. ### **Il banco e' SANO**, e i verdetti si leggono |
| **`PT-11`** | ### **NON VERIFICATA:** nessuna legge e' risultata ### **simmetrica senza che io sappia scriverne la `E`**, quindi la casella *«TRADUCIBILE con `E` APERTA»* ### **e' rimasta vuota.** ### **Non la riempio per non lasciarla vuota** |

### ⭐ **E DUE COSE CHE IL MANDATO NON PREVEDEVA, e che sono emerse facendo:**

| | |
|---|---|
| ### **il test `(A)` viene PRIMA del `(B)`** | una legge che scrive `x` ma ### **non legge `x`** ha `J = 0`, che e' ### **simmetrica**: il `(B)` la promuoverebbe a traducibile. ### ⛔ **E' un FALSO-ZERO, ed e' esattamente il caso della coppia del driver** — senza il `(A)` l'avrei messa in `H` |
| ### **il terzo controllo del banco** | serviva una legge che ### **DEVE** risultare asimmetrica, perche' ### **un banco che approva tutto e un banco che funziona danno lo STESSO referto sul controllo positivo.** L'ho costruita *(la coppia col prefattore di nodo)*, e ### **non e' una legge del simulatore**: e' dichiarata come controllo |

### ⚠ **E UNO SCARTO DI PROCESSO, dichiarato nel commit:** i quattro strumenti di questo
mandato ### **hanno girato prima di essere committati**, contro il par.5. Il timbro di
`_presidio` lo ha scritto a ogni giro, e io l'ho letto e sono andato avanti. ### **I blob sono
nell'inventario e il comando rigira verbatim, quindi l'output e' riproducibile AL COMMIT — ma
l'ordine non e' stato rispettato, e l'ordine E' il punto della regola.**
