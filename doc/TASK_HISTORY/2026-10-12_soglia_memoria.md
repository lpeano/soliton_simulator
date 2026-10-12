# LA SOGLIA DELLA MEMORIA A `5x`, E LO STATO DELLE ESTREMITA' NUOVE COME POSTO APERTO

> **Mandato di Luca, 2026-10-12:** *«La soglia di `m1` passa da `4x` a `5x` lo stato. Non
> e' "spostare la soglia per farla passare", per due motivi»* — e i due motivi sono suoi,
> non miei.

> ### ✅ **Questo file si committa PRIMA del codice**, e il marcatore del pezzo nel
> presidio sullo STOP **e' questo file**: finche' non c'e', **il pezzo non e' cominciato.**

---

## 1. PERCHE' NON E' <<SPOSTARE LA SOGLIA PER FARLA PASSARE>> — *e il motivo non e' mio*

### ⛔ **ERA LA MIA OBIEZIONE, e Luca la scioglie con due argomenti.**

| | l'argomento di Luca | perche' lo accetto |
|---|---|---|
| `1` | il `4` era **una stima mia**, fatta nel censimento *(`50a2d83`)*, **che non contava i buffer di lavoro** — cioe' **il termine piu' grande** *(`2.625x`)* | ### ✅ **E' quello che ho misurato io**: non e' una soglia sbagliata di poco, e' **derivata da un conto che OMETTEVA il termine dominante** |
| `2` | il **vincolo vero**, nato dalla caduta del run *(memoria che cresceva fino a **~`580x`** lo stato **durante** la scena)*, e' **`m3`** — la memoria **per tick piatta** — ### **e `m3` PASSA** | ### ✅ **E' la distinzione giusta: `m1` e' QUANTO COSTA una scena, `m3` e' SE CRESCE.** Il difetto che ha fatto cadere il run era **la crescita**, non il costo |

### ⭐ **E LA DIFFERENZA FRA I DUE SI VEDE NEI NUMERI:** `m1` sta fra `4` e `5`; il run
cadeva a **`580x`**. ### **Non e' lo stesso ordine di grandezza, e non e' lo stesso
difetto.**

---

## 2. CHE COSA FACCIO, E CHE COSA NON FACCIO

| | |
|---|---|
| ### ✅ **le tre riduzioni SICURE** | `(a)` `cos` e `sin` in **un solo** buffer; `(b)` lo spostamento salva **un lato solo**; `(c)` lo stesso per lo spostamento scalare. ### **Gia' CALCOLATE in `8a9c699`: `-0.4375x`** |
| ### ⛔ **cosa NON faccio** | **condividere i buffer fra operatori diversi**. Luca: *«il rischio di corruzione silenziosa non vale `-0.5x`»* — ### **e sono d'accordo: sarebbe il difetto che quel modulo esiste per impedire** |
| ### ⚠ **e la precisione NON si tocca** | e' il vincolo `(d)`: *«la precisione non si riduce mai per risparmiare memoria»*. ### **Le tre riduzioni sono riscritture, non approssimazioni** |

### 📌 **LA PREVISIONE, SCRITTA PRIMA DI RIMISURARE**

> **`5.000x − 0.4375x = 4.5625x`**, e **identico alle due taglie** *(il rapporto non
> dipende da `n`: ogni termine e' lineare in `n` o in `m`, e sull'anello `m = n`)*.
> ### ✅ **Quindi prevedo `4.56x` a `n=4096` E a `n=16384`, e un margine di `0.44x`
> sotto `5`.**
> ### ⚠ **E se NON venisse identico alle due taglie, sarebbe una cosa da guardare**:
> vorrebbe dire che **un termine non e' lineare**, e il conto voce per voce lo direbbe.

---

## 3. LA REGOLA PER I PEZZI FUTURI — *che Luca chiede di scrivere*

> ### ⛔ **Quando un pezzo nuovo aggiunge buffer** *(la saturazione, la mitosi)*, **la
> soglia NON si alza a mano.** Si rifa' **il conto voce per voce**, si **dichiara la voce
> nuova**, e **la soglia nuova la decide Luca.**

### ⭐ **E IL MOTIVO E' QUELLO CHE MI E' SUCCESSO:** il `4` non era sbagliato perche' era
basso, era sbagliato perche' **mancava una voce dal conto**. ### **Una soglia alzata a
mano nasconderebbe la voce nuova esattamente come il `4` nascondeva i buffer.**
### ⚠ **Va scritta in `[[MEMORIA-PER-TICK]]` e nel task history del motore**, non solo
qui.

---

## 4. LA SCELTA DI FISICA NASCOSTA NEL MOTORE — *trovata dalla verifica esterna*

### ⛔ **`cresci()` fa nascere le estremita' nuove con `psi_h = 0` e `phi_h = 0`**
*(`np.zeros`)*. ### **E' una decisione su come nasce lo stato, e l'ho presa io senza
accorgermene.**

| | contro che cosa va | perche' e' una decisione e non un dettaglio |
|---|---|---|
| `1` | *«seme piu' vuoto di fondo»* | un arco nuovo con `phi = 0` **nasce SENZA vuoto** |
| `2` | *«la natura del nato non si assegna»* | **zero e' un valore assegnato**, non un valore derivato |
| `3` | **`P-V4`** *(mandato del `2026-10-12` sera)* | *«le estremita' nuove nascono con un `phi` **DERIVATO** dal `phi` dei genitori, mai assegnato, **mai zero per default**, mai preso da uno sfondo»* |

### ✅ **CHE COSA FACCIO, e Luca lo dice esplicitamente: NON decido io il valore giusto.**

| | |
|---|---|
| **il motore** | `cresci()` **riceve** i valori iniziali delle estremita' nuove **da chi la chiama**, cioe' **dalla legge**; e se non li riceve ### **SI BLOCCA** |
| ### ⛔ **lo zero resta ammesso SOLO nei collaudi** | e **scritto esplicitamente dal collaudo**, non per omissione. ### **La differenza e' tutta qui: un default e' una decisione invisibile, un argomento esplicito e' una decisione dichiarata** |
| **il braccio che DEVE fallire** | `cresci()` **con estremita' nuove e senza valori iniziali** |
| **la domanda** | *«con che `psi` e che `phi` nascono le estremita' di un arco nuovo?»* — **NON critica**, legata alla derivazione di `[[SPAZIO-CHE-NASCE]]`, con **le prove** *(la riga di `np.zeros`)* e la raccomandazione **separata dalla decisione** |

---

## 5. LA STELLA POLARE

> ### ⚠ **SI APPLICA, e per una ragione sola: il punto `4`.** Togliere un default di
> fisica dal motore **cambia che cosa il simulatore puo' fare senza una legge** — e le
> cinque risposte vanno **nel commit che lo fa**.
> ### ✅ **Il punto `1`..`3` invece non tocca la fisica:** sono **riscritture di buffer** e
> **una soglia di misura**.

---

## 6. TODO DEL NEXT STEP

1. le **tre riduzioni** in `primo_ordine/motore.py`, e **rimisurare `m1`** alle due taglie.
2. la **soglia a `5x`** in `_collauda_memoria.py`, con **la scomposizione voce per voce**
   stampata e **il margine rimasto**.
3. la **regola per i pezzi futuri** in `[[MEMORIA-PER-TICK]]` e nel task history del motore.
4. `cresci()` **senza default di fisica**, col suo braccio che **deve fallire**.
5. la **domanda** in `DA_DECIDERE_LUCA.md`.
6. chiudere **`[[MOTORE-MEMORIA-M1-ROSSO]]`** come **decisa da Luca** — ### ✅ **e adesso
   si puo', perche' `PI-ERA-STATO` e' ristretto.**
