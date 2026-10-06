# `TORS-W8-AVVOLGIMENTO` — **LA MISURA LUNGA: 1000 passi**

*(Decisione di Luca del 2026-10-06. ### ⛔ **SOSTITUISCE la «misura sola» del prompt della
cura**, e il motivo e' un numero del mio stesso task history.)*

---

## 0. IL PERCHE', e viene da un numero che avevo misurato io

Il task history della cura *(`5c46856`)* ha mostrato che il **tempo di scarica**
`τ_tw/dt_e` vale ### **`1491` passi** al passo `1`, ### **`309`** al passo `50` e
### **`250`** al passo `140`.

> ### ⛔ **QUINDI IN `150` PASSI LA RETE ERA ANCORA NEL TRANSITORIO.** Con la legge vecchia
> era il transitorio ### **del calcio di nascita**; con la legge curata la torsione
> ### **parte da zero**, e per vedere dove si stabilizza servono ### **almeno due o tre
> tempi di scarica.** ### **`150` passi non bastano, e `1000` sono `~3.3` tempi.**

### ✔ **I NUMERI DEL SIGILLO `c17e518` COME PUNTO DI PARTENZA**

| | legge **vecchia** *(`f7237563`)* | legge **curata** *(`cf2a1ac8`)* |
|---|--:|--:|
| `|tw|` mediano al passo `140` | `2.11` | ### **`2.2223`** *(`1.0532x`)* |
| archi con `|tw| >= 4π` | mediana `108`, massimo `109` | ### **`0` A OGNI PASSO dei `150`** |
| calci di modulo `~4π` | `142114` | ### **`0`** |
| `|tw|` prodotto dal passo `1` | `3.0950` mediano, `9.4248` massimo | ### **`0.0000`** |

### ➜ **Quindi la torsione NON e' crollata togliendo il calcio: e' dello STESSO ORDINE,
### per una ragione DIVERSA.** ### **E' la domanda della misura lunga: dove si fermera'.**

---

## LA STELLA POLARE — le cinque domande

| | risposta |
|--:|---|
| **1 `A14`** | ### **NON SI APPLICA, e il perche':** la misura ### **non introduce nessuna legge** e non muta nessuno stato. Un braccio, il blob `cf2a1ac8` **come e'**, con un gancio di **sola lettura**. ### **Nessuna patch sulla fisica** |
| **2 i tre gradini** | ### **(a) e (b), e il (b) e' il punto.** **(a)** `1000` passi e distribuzioni, non singoli valori. ### ✔ **(b) E' ESATTAMENTE QUESTA MISURA:** la legge pratica *(il calcio di nascita e l'avvolgimento spurio)* ### **e' stata TOLTA**, e qui si guarda **che cosa resta**. ### ⛔ **Non arriva al (c):** nessun limite noto. ### ⚠ **E i conteggi assoluti dipendono dalla piattaforma** *(`STELLA_POLARE`)*: si legge il **rapporto alla curva**, non il valore |
| **3 un numero o una legge?** | ### **NESSUNO DEI DUE: non si aggiunge niente, si MISURA.** La curva `2π·(1 − e^(−t/300))` e' un **termine di paragone**, non una legge del sistema, e le tre soglie `0.5`/`1.5` sono un **criterio di lettura** fissato prima. ### ⚠ **E il `τ = 300` della curva non e' scelto: e' il tempo di scarica MISURATO** *(`309` al passo `50`)* |
| **4 `rho`, `c_s`, il segno?** | ### **NON SI APPLICA a `rho` e `c_s`.** ### ⚠ **MA IL SEGNO E' LA DOMANDA:** la curva assume che la spinta sia ### **coerente in segno** arco per arco. Se non lo e', `|tw|` non cresce come `δ·T` ma come `δ·sqrt(T/2)`. ### **E' per questo che il criterio e' un RAPPORTO e non un valore** |
| **5 emergente o imposto?** | ### ⛔ **E' LA DOMANDA DELLA MISURA.** Con la legge vecchia la torsione era ### **imposta** *(il calcio di nascita, misurato: `3.0950` mediano al passo `1`, e il `61.5 %` sopravviveva a `150` passi)*. ### **Ora parte da zero: se a `1000` passi c'e' una torsione, quella e' EMERGENTE** -- e il rapporto alla curva dice ### **da quale meccanismo** |

---

## 1. RAGIONAMENTO PRELIMINARE

### LA PREVISIONE DEL GUARDIANO

| | |
|---|---|
| la curva | `|tw|` mediano `≈ 2π·(1 − e^(−t/300))` |
| i valori | `0.9646` al passo `50` · `2.4722` al `150` · `3.9717` al `300` · `5.4328` al `600` · ### **`6.0590`** al `1000` |
| e che cosa si aspetta | ### ⛔ **che la curva misurata stia SENSIBILMENTE SOTTO**, perche' la `Spearman` `0.02` di `eebe24f` dice che la spinta ### **non e' coerente in segno arco per arco** |
| sulle nascite | ### **NESSUNA PREVISIONE, e lo scrivo cosi'** |

### ✔ **E LE DUE IPOTESI SONO A UN FATTORE `24.5`: il criterio discrimina NETTO**

Con la spinta per passo misurata `δ = 0.0247` *(`|avanzamento|` mediano, `M7` al passo `140`)*
e il tempo di scarica `T = 300` passi:

| ipotesi | ampiezza di equilibrio | il conto |
|---|--:|---|
| **COERENTE** *(la spinta ha sempre lo stesso segno)* | `δ·T` = ### **`7.4100`** | e `2π` = `6.2832`: lo stesso ordine, ed e' la curva del guardiano |
| **INCOERENTE** *(segno casuale: cammino aleatorio)* | `δ·sqrt(T/2)` = ### **`0.3025`** | la varianza si accumula, non il valore |

### ➜ ⛔ **UN FATTORE `24.5` FRA LE DUE**, quindi al passo `1000` il rapporto
misurato/curva vale ### **`~1.0` se coerente** e ### **`~0.05` se incoerente.**
### **Non e' una sfumatura: sono due risposte che non si possono confondere.**

### ⛔ **IL LIMITE DI QUELLA CURVA, scritto PRIMA della corsa**

La curva assume ### **`τ = 300` FISSO.** Il `τ_tw/dt_e` **vero** parte da ### **`~1491`** al
passo `1` e scende a ### **`~250`** al `140`. ### ⛔ **Nei primi passi la scarica e' molto
piu' debole di quella che la curva assume, quindi il rapporto misurato/curva e' GONFIATO.**

| passo | `|tw|` mediano *(dal sigillo)* | la curva | rapporto |
|--:|--:|--:|--:|
| `25` | `1.0120` | `0.5024` | ### **`2.0145`** |
| `50` | `1.3967` | `0.9646` | `1.4479` |
| `100` | `1.8743` | `1.7811` | `1.0523` |
| `150` | `2.2829` | `2.4722` | ### **`0.9234`** |

### ➜ ⚠ **IL RAPPORTO SCENDE MONOTONO, e l'eccesso iniziale NON e' <<una spinta
### misteriosa>>: e' `τ` che vale cinque volte tanto.** ### **Dirlo prima della corsa e'
l'unico modo di non scambiarlo per un risultato.**

### ⛔ **IL CRITERIO, FISSATO PRIMA — e dice ANCHE DOVE NON si legge**

| | |
|---|---|
| ### **si LEGGE ai passi `300`, `600`, `1000`** | ### **dove `τ` e' vicino a `300`** e la curva ha il suo termine di paragone |
| ### **ai passi `50` e `150` si RIPORTA ma NON decide** | li' `τ` vale `309`-`1491`, e il rapporto e' gonfiato ### **per costruzione** |

| il rapporto | la lettura |
|---|---|
| **sotto `0.5`** | ### **«la deriva non e' coerente: la torsione non accumula»** |
| fra **`0.5`** e **`1.5`** | ### **«accumula come previsto»** |
| **sopra `1.5`** | ### **«c'e' una spinta che il conto non vede»** |

### ⛔ **E SE I TRE PASSI DANNO LETTURE DIVERSE, SI DICE COSI' E NON SI SCEGLIE.**
### **Tre letture diverse sono un risultato: dicono che il regime CAMBIA, e scegliere la
piu' comoda lo nasconderebbe.**

### LA MIA PREVISIONE, e per la prima volta ho un dato

Il giro minimo della cura *(3 passi, blob `cf2a1ac8`)* ha dato `|tw|` mediano:

| passo | misurato | la curva | rapporto | il cammino aleatorio darebbe |
|--:|--:|--:|--:|--:|
| `2` | `0.036102` | `0.041749` | **`0.8647`** | `0.0349` |
| `3` | `0.067253` | `0.062519` | **`1.0757`** | `0.0428` |

> ### ⚠ **TRE PASSI NON SONO UNA MISURA, e lo dico prima di appoggiarmi a loro.** Ma il
> rapporto e' ### **`0.86`-`1.08`**, e il cammino aleatorio al passo `3` darebbe `0.0428`
> contro `0.0673` misurato: ### **il dato che ho favorisce il COERENTE.**

| | la mia previsione |
|---|---|
| al passo `300` *(il primo che DECIDE)* | ### **rapporto fra `0.6` e `1.0`.** Il sigillo da' `0.9234` al `150` e la tendenza e' **in discesa**: prevedo che continui, ma **piano** |
| al passo `600` | ### **fra `0.4` e `0.9`** |
| al passo `1000` | ### ⚠ **PREVEDO CHE SCENDA SOTTO `0.5`**, cioe' *«la deriva non e' coerente»* -- e ### **mi separo dalla mia previsione di `5c46856`**, dove avevo scritto *«resti sopra `0.3`»*: il sigillo ha mostrato una discesa monotona, e `0.5` e' la soglia che il criterio usa |
| le nascite | ### **MENO di `18` divisioni a `150` passi**, e a `1000` passi ### **PIU' di `18`** -- prevedo fra `30` e `150`, perche' la torsione ha tempo di arrivare alla coda e `g1` cresceva gia' *(`109` -> `151` -> `280` ai passi `50`/`100`/`140` di `eebe24f`)* |
| gli archi oltre `4π` | ### **ZERO a ogni passo, anche a `1000`**: non c'e' piu' nessun meccanismo che li porti la' in un passo solo. ### ⚠ **E se ne comparisse UNO, sarebbe una scoperta, non un difetto della cura** |

> ### ⛔ **E LE MIE PREVISIONI SONO SBAGLIATE DUE SU DUE** *(`Bperm`, `Bperm-fisso`)*.
> ### **Chi legge pesi queste per quello che valgono.**
>
> ### ⚠ **E DICHIARO LA COSA CHE NON SO, perche' e' la piu' importante:** il rapporto
> misurato/curva puo' **scendere nel tempo** anche se la spinta e' coerente, perche' la curva
> assume `δ` **costante** e `δ` dipende da `phivel`, che evolve. ### **Se il rapporto
> scendesse, non saprei distinguere <<la deriva non e' coerente>> da <<`δ` e' calato>>** --
> e per questo la misura registra `τ_tw/dt_e` **e** i quantili di `|tw|` ai cinque passi,
> non solo il rapporto.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### LA SCENA

Quella di sempre: `--nmasse 3 --sep 6.1158`, ### **seme `11`**, blob ### **`cf2a1ac8`**,
### **UN braccio**, ### **`1000` passi**. Strumento committato e collaudato **prima** della
corsa, salvataggio ### **ogni `10` passi e a OGNI caduta.**

### CHE COSA SI REGISTRA, a **OGNI** passo

`n` · `archi` · **divisioni** · **Schwinger** · ### **archi oltre `4π`** ·
### **calci di modulo `~4π`** *(devono essere ZERO)* · ### **il contatore della guardia di
`TAU_TW`** *(rilievo `E4`)* · e i quantili di `|tw|`: `q25`, `q50`, `q75`, `q95`, `q99`.

### E AI PASSI `50`, `150`, `300`, `600`, `1000`

| | |
|---|---|
| i quantili di `τ_tw/dt_e` | ### **il tempo di scarica in PASSI**, che e' la scala della curva |
| la `Spearman` fra il tetto calcolato e `|tw|` | il criterio ### **`M2` di `eebe24f`**, coi valori ### **CAUSALI** *(la lezione di `99782e1`)* |
| la frazione sopra la **soglia modulata** e sopra `3π` | il canale della mitosi |
| la distribuzione di `twist_dip` | *(a `0`, `π/2`, `π`)*: in `eebe24f` era ### **`0` sul `100 %`** degli archi |

### E LE NASCITE PER FINESTRE DI `50` PASSI

### **Non il totale:** con `1000` passi un totale nasconderebbe **quando** la rete cresce, e
*«quando»* e' la domanda.

### ⛔ **IL CRITERIO, FISSATO PRIMA**

Si riporta il ### **rapporto misurato/curva** ai cinque passi, e si legge cosi':

| il rapporto | la lettura |
|---|---|
| **sotto `0.5`** | ### **«la deriva non e' coerente: la torsione non accumula»** |
| fra **`0.5`** e **`1.5`** | ### **«accumula come previsto»** |
| **sopra `1.5`** | ### **«c'e' una spinta che il conto non vede»** |

### IL CONFRONTO, coi numeri di `f7237563` **gia' committati**

| | `f7237563` a `150` passi | `cf2a1ac8` |
|---|---|---|
| nascite | ### **`18` divisioni + `7` Schwinger** | ? |
| `|tw|` mediano al passo `140` | ### **`2.11`** | ? |
| archi oltre `4π` per passo | ### **`~108`** *(mediana `108`, massimo `109`)* | ### **atteso `0`** |
| calci di modulo `~4π` | ### **`142114`** in `150` passi | ### **atteso `0`** |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

I **calci** diversi da zero ⟹ ### **la cura non ha curato**, e la misura non si legge: si
ferma e si scrive. ### **E un `nan` in `twp_dip` che sopravvive a un passo** ⟹ lo stesso.

---

## 3. TODO DEL NEXT STEP

1. **commit di questo task history**, ### **DA SOLO**;
2. lo **strumento** della misura lunga, col **collaudo**, ### **commit a se'**;
3. il **giro corto** *(`STANDARD 7`)*, poi la **corsa** da `1000` passi;
4. le **uscite** col verdetto, poi il **referto generato** col rapporto alla curva ai cinque
   passi e il confronto con `f7237563`;
5. ### ⛔ **poi FERMO:** la soglia, il `0.3` e `κ` si decidono su quei numeri, e
   ### **sono decisioni di Luca.**

---

## ANNOTAZIONE *(2026-10-06, a corsa CADUTA -- `par.8`: si ANNOTA, non si riscrive)*

> ### ⛔ **LA CORSA DA `1000` PASSI E' CADUTA AL PASSO `1`, PRIMA DI OGNI SALVATAGGIO:**
> `KeyError: 'calci_oltre_pi'` alla riga del *«battito»* per-passo
> *(`csv/_test_fork/_tors_w8_lunga.py:669`)*. ### **Zero passi girati, zero dati.**
> La prova sta in `csv/_test_fork/_tors_w8_lunga/caduta_passo1.txt`, committata col
> fallimento; la voce e' ### **`LUNGA-BATTITO-CADUTA`**.

**E IL PUNTO `3` DI QUESTO TODO PRESCRIVEVA ESATTAMENTE LA COSA CHE HO SALTATO.** C'e'
scritto *«il **giro corto** (`STANDARD 7`), **poi** la corsa»*. Il giro corto l'ho fatto --
### **ma PRIMA di curare l'etichetta dei calci**, e dopo la cura ho rigirato ### **il
COLLAUDO e non il GIRO CORTO.** La sequenza vera e' stata:

1. giro corto a `4` passi → ### **trova** il difetto dell'etichetta *(il contatore
   `calci_oltre_pi` misurava un controfattuale)*;
2. cura: ### **un contatore diventa TRE** *(`calci_evitati`, `calci_spuri_curata`,
   `spinta_senza_causa`)*, e la chiave `calci_oltre_pi` ### **non esiste piu'**;
3. collaudo `40/40` → ### **PASSA**, perche' il collaudo ### **non esercita la riga del
   battito**;
4. commit `7d68c6d`, corsa lanciata → ### **cade al primo battito.**

> ### ⛔ **HO RITIRATO L'UNICO CONTROLLO CHE AVEVA IL POTERE DI PRENDERLO.** Il giro corto
> aveva ### **appena dimostrato** quel potere -- e' lui che aveva trovato il difetto
> precedente ### **sulla stessa riga** -- e invece di rigirarlo mi sono fidato di un collaudo
> che quella riga ### **non la guarda.** ### **Un collaudo che prova le formule non prova il
> RAPPORTO che le stampa**, ed e' la terza volta in questa misura che il difetto sta
> ### **nel rapporto e non nella grandezza.**

**E IL SECONDO DIFETTO, PIU' GRAVE DEL PRIMO:** lo strumento ### **promette** *«i dati dei
passi prima sono salvati»* a ogni caduta, ma il suo `try` avvolge ### **SOLO**
`passo_pieno` e `m.chiudi`. La stampa del battito e il salvataggio ### **stanno FUORI**,
quindi una caduta li' ### **non salva niente** -- ed e' esattamente quello che e' successo.
### **La promessa valeva per una caduta del SIMULATORE, non per una caduta dello
STRUMENTO**, e la differenza non era dichiarata da nessuna parte.

**COSA NON CAMBIA:** le previsioni dei paragrafi `1` e `2` ### **restano quelle scritte
prima**, e il criterio *(`300`, `600`, `1000`; `0.5` e `1.5`)* ### **non si tocca**: la
corsa non ha prodotto un solo numero, quindi ### **non c'e' nulla da cui una previsione
potrebbe essere stata ritoccata.**
