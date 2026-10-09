# INDICE `v3`: **i residui della verifica, e i presidi contro le mescolanze**

> **Mandato di Luca del 2026-10-09** *(relayed dal guardiano)*. Nessuna corsa, simulatore
> `b8c21049` intatto. Blocchi **`G`** *(tre residui, un commit)* e **`F`** *(sei presidi nel
> validatore)*, poi il referto `doc/REFERTO_indice_v3_presidi.md`.
>
> ### ⚠ **Questo file si committa e si pusha PRIMA del lavoro**, cosi' l'ordine e'
> **verificabile da git** invece che asserito da me *(par.8)*.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### **CHE COSA CREDO, E PUO' RIVELARSI FALSO**

**`a` I tre residui `G` sono correzioni di MIE applicazioni letterali di un prompt sbagliato,
non di mie letture.** `G1` dice che la regola *«altrimenti `APERTA`»* era un errore **del
prompt del guardiano**: le `5` voci verificano **flag dell'era `1`**, quindi vanno a
`METODO/1/SOSPESA` come `TS-*` e `TW-*`. Io l'avevo applicata **alla lettera**, e nel referto
`v3` avevo scritto che la distinzione fra le due regole di stato era *«presa prima di
applicare»*. ### ⛔ **Era vero per `DOCUMENTAZIONE`/`INFRASTRUTTURA` e FALSO per queste cinque:
li ho mandati ad `APERTA` perche' il prompt lo diceva, senza chiedermi se avesse senso per una
voce che verifica un flag dell'era `1`.** Lo annoto qui perche' **si annota, non si riscrive.**

**`b` I presidi `F` troveranno pochi segnali.** ### **Credo di sbagliarmi**, e la ragione e'
`F1`: *«una voce che cita nel titolo l'ID di un'altra»* — gli ID corti *(`G1`, `E3`, `B7`,
`O4`, `D5`, `C25`)* compaiono come **sottostringhe nella prosa**, e un rilevatore su `830`
voci × `830` ID puo' produrre **decine di falsi**. ### **Previsione scritta: `F1` fra `10` e
`60` segnali; `F2` pochi** *(`26` voci sono era `2`)*; **`F3` molti** *(`439` voci `FISICA`, e
il vocabolario di `F3` contiene `criterio`, che e' una parola comune)*; **`F4` fra `10` e
`28`** *(il ripasso del blocco `C` ne aveva trovate `28` definite, `16` ripristinate ⇒ almeno
le `12` lasciate a Luca)*; **`F5` zero** *(`storico-commit` ha riempito tutte e `1079`)*;
**`F6` circa `8`** *(le note di `G3`, che pero' `G` corregge PRIMA)*.

**`c` «Lo stesso fatto» NON e' rilevabile in modo deterministico.** `F1` chiede *«se una voce
cita l'ID di un'altra **come lo stesso fatto**»*. ### ⛔ **Un programma non legge l'intenzione.**
Credo che l'unica forma onesta sia: **cita l'ID come token intero** ⇒ segnale, e che
l'*«stesso fatto»* lo decida **chi legge il segnale**. ### **E' esattamente il motivo per cui
il mandato dice che i presidi SEGNALANO e non decidono**, e lo scrivo qui perche' non sembri
una scorciatoia trovata dopo.

### ⛔ **CHE COSA NON SO, E NON INVENTO**

1. ### **`F5` come ERRORE, cosi' com'e' scritto, BLOCCA OGNI COMMIT DI UN LOTTO.** Non so se
   il mandato se ne renda conto. La catena e': `aggiorna-lotto` scrive righe con `commit = ""`
   *(il commit che le conterra' **non esiste ancora** — e' il ritardo dichiarato nel blocco
   `D`)* ⇒ il `pre-commit` gira `indice.py valida` ⇒ `F5` trova righe senza commit ⇒
   ### **BLOCCA, e il lotto non si puo' committare mai.** ### ✔ **La forma che credo giusta,
   e la scrivo PRIMA di provarla:** `F5` e' un errore **solo per le righe GIA' COMMITTATE**,
   cioe' quelle presenti in `HEAD:doc/indice/storico.jsonl`; le righe aggiunte dopo `HEAD`
   sono **esattamente il ritardo**, e sono esenti. ### **Questo rende `F5` utile invece che
   fatale:** obbliga a girare `storico-commit` **prima del commit successivo.**
   ### ⚠ **E' una MIA derivazione, non una scelta di Luca: va nel referto come tale.**
2. **Se `F3` vada guardato sul `titolo` o anche sulla `descrizione`.** Il mandato dice
   *«il cui **titolo** parla di…»* ⇒ **titolo**, e niente altro. Lo prendo alla lettera, e se
   risulta troppo stretto **lo scrivo invece di allargarlo da solo.**
3. **Quanti segnali siano «troppi».** Non lo so, e per non deciderlo a posteriori lo fisso
   adesso: ### **se un presidio segnala su piu' del `10%` delle voci che esamina, nel referto
   lo dichiaro TROPPO GROSSO** e dico che la sua lista **non e' azionabile com'e'**, invece di
   presentarla come un elenco di difetti.
4. **Se `F4` sia abbastanza rapido per il `pre-commit`.** Apre i `file_citanti` di `122`
   etichette. Se supera **`5` secondi** lo dico e propongo di tenerlo **fuori** dal
   `pre-commit`, in un comando a parte.

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### **I PASSI**

| | il passo | che cosa DECIDE |
|---|---|---|
| `1` | **`G1`+`G2`+`G3` in un lotto solo**, con `aggiorna-lotto` e un motivo che cita il testo | niente di nuovo: **applica una correzione chiesta** |
| `2` | il controllo `C3` deve conoscere anche queste *(come `CORRETTE_V3`)* | se `C3` grida *«fuori posto»* su una correzione **chiesta**, il controllo e' sbagliato, non la voce |
| `3` | **i sei presidi**, in `csv/indice.py`, come funzione `segnali()` **separata da `valida()`** | ### **`F1`–`F4` e `F6` NON toccano il codice d'uscita**; ### **`F5` SI'**, perche' il mandato dice *«errore, non segnale»* |
| `4` | **il collaudo**, su una **COPIA** dell'indice con le voci riportate allo stato di prima | ### **ogni presidio DEVE scattare** sul suo caso a risposta nota *(`P1-sexies`)*; **e NON deve scattare** sulla voce corretta |
| `5` | i segnali sull'indice **vero**: si **contano** e si **elencano** | ### **NON si correggono**, lo dice il mandato |
| `6` | il referto `doc/REFERTO_indice_v3_presidi.md` | i segnali residui **voce per voce**, e quanti sono |

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura |
|---|---|
| **il collaudo** | ### **`6` presidi × `2` bracci** *(il caso che DEVE scattare, e la voce corretta che NON deve)* = ### **`12` esiti**. Meno di `12` su `12` ⇒ ### **FERMO** |
| **`F1` troppo grosso** | piu' di `83` segnali *(`10%` di `830`)* ⇒ **dichiarato tale nel referto** |
| **`F3` troppo grosso** | piu' di `44` segnali *(`10%` delle `439` voci `FISICA`)* ⇒ **idem** |
| **`F4`** | i segnali attesi sono **almeno le `12` lasciate a Luca**: ### **se `F4` ne trova MENO di `12`, il rilevatore e' ROTTO**, non l'indice |
| **`F5`** | ### **zero.** Se ne trova uno, vedi *«cosa mi ferma»* |
| **`F6`** | ### **zero dopo `G3`.** Se `G3` e' applicato e `F6` segnala ancora, **`G3` e' incompleto** |

### ⛔ **CHE COSA MI FA FERMARE**

1. **`F5` segnala sull'indice vero** ⇒ una riga **committata** senza commit: lo storico non e'
   piu' ricostruibile ⇒ ### **FERMO**, commit dello stato e del fallimento.
2. **Un presidio NON scatta sul suo caso a risposta nota** ⇒ e' un presidio che non protegge
   niente (`A9`) ⇒ ### **FERMO**: non si committa un presidio che non si e' visto scattare.
3. **Un presidio scatta sulla voce CORRETTA** *(il braccio negativo)* ⇒ e' un **falso-uno** ⇒
   ### **FERMO**.
4. **Il collaudo tocca l'indice vero** anche solo in lettura-scrittura temporanea ⇒
   ### **FERMO e ripristino**: il mandato dice *«in una COPIA di prova, mai nell'indice
   vero»*, ed e' **lo stesso difetto che nel giro scorso mi ha cancellato `867`
   classificazioni** *(`C4` che rilanciava la migrazione)*.
5. **`valida` cambia codice d'uscita per un segnale** ⇒ un segnale che blocca **non e' un
   segnale** ⇒ **FERMO**.

### **`L-STELLA`: le cinque domande di `doc/STELLA_POLARE.md`**

### ⛔ **NON SI APPLICA, e il perche' e' parte della risposta:** questo giro **non cambia la
fisica** — non tocca `soliton_simulator.py` *(resta `b8c21049`)*, non aggiunge ne' toglie una
legge, non accende ne' spegne un flag, e non fa girare nulla. Tocca **l'indice dei difetti** e
**il suo validatore**. ### **Le cinque domande chiedono di un gradino di robustezza fisica, di
numeri o leggi aggiunti, del verso EM-curvatura e di emergente-contro-imposto:** su un
cambiamento che non entra nel simulatore **non hanno un soggetto**, e rispondere per forma
sarebbe **riempire un modulo**, non un controllo.

---

## ③ TODO DEL NEXT STEP — *operativo*

- [ ] **`G`** — lotto `v3_G.jsonl`: `G1` *(5 voci → `METODO/1/SOSPESA`)*, `G2` *(`G1` →
      `FISICA/1/SOSPESA`)*, `G3` *(8 note sostituite)*. `C3` aggiornato. Commit + push +
      `_avanzamento.md`.
- [ ] **`F`** — `segnali()` in `csv/indice.py`, sei presidi, `F5` **errore** e gli altri
      **segnali**. Nuova chiave meta **`eccezione_presidio`** *(testo che CITA alla lettera)*.
- [ ] **collaudo** — `csv/_collaudo_presidi_indice.py`: copia di prova, `6` casi che **devono
      scattare** *(`Z31`/`B2`, `D35`, `C28`, `TW-1`, `CENS-A6`, e una riga di storico
      committata senza commit)* + `6` bracci negativi. ### **Mai sull'indice vero.**
- [ ] **i segnali veri** — contati ed elencati, ### **non corretti.**
- [ ] **referto** — `doc/REFERTO_indice_v3_presidi.md`, voce per voce, con i conteggi.
- [ ] **`storico-commit`** come ultimo passo di ogni blocco, perche' `F5` lo pretende al
      commit dopo.
- [ ] **par.6** nello stesso commit: **inventario** *(gli strumenti nuovi, col blob)* e
      **README/par9** *(il comando `segnali` e la chiave meta nuova)*. ### **FISICA: non si
      applica, nessuna legge cambia.**
