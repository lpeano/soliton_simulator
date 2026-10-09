# IL REFERTO DELLA VERIFICA COMPLETA DEL GUARDIANO

> ### ⭐ **LE `165` RIGHE, UNA PER UNA.** Il mandato chiede ### **quante applicate, quante non applicate e quante lasciate** — e un conteggio ### **per CAMPO** non risponde a quella domanda: una riga che cambia due campi puo- averne ### **uno applicato e uno lasciato.** ### ⛔ **Quindi il verdetto e- PER RIGA, e la somma DEVE fare `165`: e- un `assert`, non una stampa.**

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_verifica_completa.md`, ### **committato PRIMA del lavoro** *(`bfb1596`)* |
| **il file del guardiano** | `doc/indice/_lotti/correzioni_guardiano_2026-10-09.txt`, `165` righe, ### **committato da solo** *(`67c12fa`)* |
| **i commit** | `ba8c359` *(il difetto «IL FATTO»)* · `ed10b34` *(i punti `3`, `4`, `5` e l'accensione di `F9`/`F10`)*, piu' questo |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |
| **i controlli** | ### **6 su 6** · collaudo dei presidi ### **59 su 59** · collaudo dell'indice ### **26 su 26** · le sei attese del difetto ### **6 su 6** |

---

## ① L'ORDINE DEL PUNTO `1`: **impossibile, non rischioso** — e Luca lo ha riconosciuto

> *«E l'ordine del punto `1` era sbagliato, ERRORE DEL GUARDIANO: hai ragione tu (`bfb1596`). `F9` e `F10` si accendono NELLO STESSO COMMIT delle correzioni che li rendono veri, mai prima.»*

`indice.py valida` gira ### **nel `pre-commit`** *(`csv/_hook_presidi.py`, blocco `[INDICE v2]`: lancia `csv/indice.py valida` e fa `return 1` se esce diverso da `0`)*. ### ⛔ **Quindi un presidio bloccante acceso prima della cura blocca OGNI COMMIT DEL REPO**, e il commit che lo accende ### **sarebbe bloccato dal suo stesso hook**: l'hook gira il codice ### **dell'albero di lavoro.**

### ⭐ **E- LA TERZA VOLTA IN TRE GIRI, E LA PRIMA CHE ARRIVA PRIMA DEL DANNO.** `F5` e `F7` hanno dato la stessa lezione ### **sbattendoci**; questa volta il task history l'ha ### **dedotta dal codice dell'hook** e si e- fermato. ### **La lezione nuova: il costo non e- l'indice, e- il REPO INTERO.**

### ✔ **E `F10` SI POTEVA ACCENDERE SUBITO, `F9` NO**, e la differenza e- ### **misurata, non di gusto:** `F10` violava su ### **ZERO** voci, `F9` su ### **CINQUE** — e sono esattamente le cinque che il mandato nomina. ### **Due presidi che il mandato chiede INSIEME si separano, perche- uno si puo- e l'altro no.**

---

## ② IL DIFETTO «IL FATTO»: **il criterio di chiusura CITAVA la prova che la chiusura era sbagliata**

| id | la regola corretta | chi decide | la frase che il MIO criterio citava |
|---|---|---|---|
| `M3` | `CHIUSA` → ### **`None`** | ### ⚠ **segnaposto**: il punto `1` la saltava gia- | *## ① IL FATTO, **trovato durante il collaudo di `M3-C`** In `_base_cicli_topologici` il ciclo si percorre ### **`u -> lca -> v -> u`**, ma il segno de* |
| `SOGLIA-MITOSI-3PI` | `CHIUSA` → ### **`None`** | ### **il FILE** del guardiano | *## `SOGLIA-MITOSI-3PI` — **la soglia porta un `π` di dipolo che quasi nessun arco ha** *(Aperta il 2026-10-06 sera, ### **su decisione di Luca.** ### * |
| `X1` | `CHIUSA` → ### **`SOSPESA`** | ### **il FILE** del guardiano | */ **X1** 🟩`VALE SEMPRE` ⏳`[EPOCA 1 · MISURA]` / **`TEMPO_PROPRIO_ORIENTATO`: il principio e' giusto, ma `dt_n < 0` rompe TRE consumatori** / Con `f = * |
| `Z23` | `CHIUSA` → ### **`None`** | ### **questo giro** | */ **Z23** 🟨`VALE PER QUELLA SCENA` ⏳`[EPOCA 1 · MISURA]` / **`SPIN_FEEDBACK` NON E' ANTISIMMETRICO: `sum(out) != 0`, e la causa e' la divisione per il* |
| `Z46` | `CHIUSA` → ### **`None`** | ### **questo giro** | */ **Z46** 🟨`VALE PER QUELLA SCENA` ⏳`[EPOCA 1 · MISURA]` / **⚠ IL 93 % DEI NODI NON INVECCHIA, SONO SEMPRE GLI STESSI, E SONO LE TRE MASSE. E IL GAUGE* |
| `Z56` | `CHIUSA` → ### **`SOSPESA`** | ### **questo giro** | */ **Z56** 🟨`VALE PER QUELLA SCENA` ⏳`[EPOCA 1 · MISURA]` / **⚠ `chi_basc`: NON E' UNA MONOCOLTURA CHE SI RIBALTA — e la premessa opposta veniva da UN * |
| `Z66` | `CHIUSA` → ### **`None`** | ### **questo giro** | */ **Z66** 🟨`VALE PER QUELLA SCENA` ⏳`[EPOCA 1 · MISURA]` / **`median(lambda_nodi())` SI CONGELA: `0.6092` IDENTICO A QUATTRO DECIMALI PER 270 PASSI, M* |
| `Z74` | `CHIUSA` → ### **`SOSPESA`** | ### **questo giro** | */ **Z74** 🟨`VALE PER QUELLA SCENA` ⏳`[EPOCA 1 · MISURA]` / **il ramo B rallenta `x11`: `nsub` esplode, e lo tira `\/vd\/.max()` su POCHISSIMI archi** * |

### ⛔ **IL DIFETTO ERA MIO, e sta scritto nei miei stessi motivi:** il lotto del punto `1` ha chiuso ### **sei voci** col criterio *«la riga dice **FATTO**»*, e la frase citata era *«**IL FATTO**: `soglia0` = …»*, *«(c) **IL FATTO** PIU' GROSSO»*, *«**IL FATTO**: `median(lambda_nodi())` vale `0.8000`»*. ### ⭐ **Guardavo se la parola c'era, non se era un VERBO** — ed e- ### **lo stesso errore della NEGAZIONE, un livello piu- su.**

### ✔ **La differenza si ISOLA spegnendo il filtro**, non riscrivendo la regola: `_scarta` si sostituisce con `lambda: False`, cioe- ### **il comportamento di prima della cura.** ### **Cosi- l'elenco e- esattamente cio- che il difetto ha causato**, non cio- che credo abbia causato — e le ### **sei attese sono un `assert`**: ### **`6` su `6`.**

### ⭐ **E LO STATO TORNA DOV'ERA, dove la regola corretta non decide:** per `Z23`, `Z46` e `Z66` la regola corretta ### **non decide niente**, e la `CHIUSA` di oggi ### **l'aveva scritta il mio lotto col difetto** — ### **una scrittura sbagliata si disfa.** E la `chiusura` ### **si svuota**: una voce `SOSPESA` che porta *«chiusa dal commit X»* ### **mente.**

---

## ③ LE `165` RIGHE, RIGA PER RIGA

| verdetto | quante | che cosa vuol dire |
|---|--:|---|
| ### **`APPLICATA`** | ### **`79`** | tutti i campi che la riga chiede sono stati scritti |
| ### **`APPLICATA_IN_PARTE`** | ### **`23`** | ### **almeno uno scritto e almeno uno lasciato** — ed e- il caso che un conteggio per campo nasconde |
| ### **`LASCIATA`** | ### **`44`** | citazione trovata, ### **nessun campo applicato** |
| ### **`NON_APPLICATA`** | ### **`19`** | ### **citazione non trovata** |
| ### **in tutto** | ### **`165`** | ### **e DEVE fare `165`** |

| dove si e- trovata la citazione | quante | chi lo dice |
|---|--:|---|
| `T0` | `49` | il `titolo` + `descrizione` della voce — ### **MIO**, e il motivo e- che ### **quello E- il testo della voce** |
| `T1` | `36` | la ### **riga d'origine** — ### **del mandato** |
| `T2` | `5` | il ### **blocco** *(intestazione + sezione)* — ### **del mandato** |
| `T3` | `22` | la ### **sezione** che contiene la riga — ### **del mandato** |
| `T4` | `33` | ### **altrove nel file** che la `fonte` nomina — ### **MIO, e SOLO quando la riga NON si ritrova**: la- il luogo del mandato ### **non esiste** |
| `T-STRUTTURALE` | `1` | ### **non e- una citazione**: il guardiano dichiara fra parentesi un ### **motivo strutturale** *(`A2`, cioe- `F9`)* |

### ⛔ **E IL LIMITE ERA IL MIO RITROVAMENTO, NON IL GUARDIANO.** La prima stesura dichiarava ### **`65` citazioni introvabili su `165`.** Ho misurato ### **perche-**: ### **`15`** stavano nel testo della voce, ### **`37`** altrove nel file di origine, e solo ### **`13`** erano davvero introvabili. ### ⭐ **Dichiarare `65` «non trovate» avrebbe buttato `52` correzioni VERE del guardiano per un difetto MIO.**

### ⚠ **I DUE LIVELLI CHE AGGIUNGO IO SONO UNA DECISIONE, e la dichiaro:** se Luca li ritiene troppo larghi, ### **`49` righe trovate in `T0` e `33` in `T4`** vanno riviste. ### **Ogni riga qui sotto porta il suo livello**, cosi- la revisione non deve rifare il lavoro.

### **LE `79` APPLICATE**

| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |
|---|---|---|---|---|---|
| `SOGLIA-MITOSI-3PI` | `classe=DIFETTO stato=SOSPESA` | *MA NON SI ADOTTA ADESSO* | `alta` | `MISURA/FISICA/era 1/CHIUSA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ['classe', 'stato'] in `T0` (alta) — `T0` |
| `X1` | `stato=SOSPESA` | *Si chiude quando (a), (b) e (c) sono trattati esplicitamente* | `alta` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['stato'] in `T1` (alta) — `T1` |
| `A1-TREVIE` | `stato=SOSPESA` | *né applicata né scartata* | `alta` | `DIFETTO/FISICA/era 1/CHIUSA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ['stato'] in `T1` (alta) — `T1` |
| `B3` | `classe=FRONTE stato=SOSPESA` | *Quanti siano su un percorso fisico non è misurato* | `alta` | `DIFETTO/FISICA/era 1/CHIUSA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe', 'stato'] in `T4` (alta) — `T4` |
| `B4` | `classe=FRONTE stato=SOSPESA` | *quel conto non esiste ancora* | `alta` | `DIFETTO/FISICA/era 1/CHIUSA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe', 'stato'] in `T1` (alta) — `T1` |
| `C20` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'stato'] in `T3` (alta) — `T3` |
| `Z127` | `classe=MISURA stato=CHIUSA` | *E1 NON PASSA* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T0` (alta) — `T0` |
| `Z26` | `classe=MISURA stato=CHIUSA` | *CONTIENE LO ZERO* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T1` (alta) — `T1` |
| `A2` | `stato=APERTA` | *(combinazione impossibile: ENTRAMBE+SOSPESA)* | `alta` | `STANDARD/FISICA/era ENTRAMBE/SOSPESA` → ### **`STANDARD/FISICA/era ENTRAMBE/APERTA`** | ['stato'] in `T-STRUTTURALE` (alta) — `T-STRUTTURALE` |
| `REPERTI-IMMUTABILI` | `stato=APERTA` | *APERTA il 2026-09-26* | `alta` | `DIFETTO/METODO/era ENTRAMBE/SOSPESA` → ### **`DIFETTO/METODO/era ENTRAMBE/APERTA`** | ['stato'] in `T0` (alta) — `T0` |
| `PRESTAZIONI-CORSE` | `classe=FRONTE stato=APERTA` | *IN CODA, NON ADESSO* | `alta` | `FRONTE/INFRASTRUTTURA/era ENTRAMBE/SOSPESA` → ### **`FRONTE/INFRASTRUTTURA/era ENTRAMBE/APERTA`** | ['stato'] in `T2` (alta) — `T2` |
| `RIPRESA-ARGV` | `stato=APERTA` | *LA RIPRESA SI FIDA DEL BLOB* | `media` | `DIFETTO/INFRASTRUTTURA/era ENTRAMBE/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era ENTRAMBE/APERTA`** | ['stato'] in `T0` (media) — `T0` |
| `LUNGA-BATTITO-CADUTA` | `era=1` | *_tors_w8_lunga* | `media` | `DIFETTO/INFRASTRUTTURA/era ENTRAMBE/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ['era'] in `T0` (media) — `T0` |
| `B10` | `stato=SOSPESA` | *APERTE DA PRIMA* | `alta` | `DIFETTO/INFRASTRUTTURA/era 1/CHIUSA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ['stato'] in `T3` (alta) — `T3` |
| `B8` | `stato=SOSPESA` | *APERTE DA PRIMA* | `alta` | `DIFETTO/INFRASTRUTTURA/era 1/CHIUSA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ['stato'] in `T3` (alta) — `T3` |
| `Z35` | `classe=CURA stato=CHIUSA` | *BYTE-INERTE* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T1` (alta) — `T1` |
| `Z87` | `classe=DIFETTO stato=CHIUSA` | *CAUSA TROVATA* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T1` (alta) — `T1` |
| `Z31` | `classe=DIFETTO stato=SOSPESA` | *NON RIPARATI IN QUESTO GIRO* | `alta` | `MISURA/METODO/era 1/CHIUSA` → ### **`DIFETTO/METODO/era 1/SOSPESA`** | ['classe', 'stato'] in `T1` (alta) — `T1` |
| `Z25` | `classe=CURA` | *CURAT* | `alta` | `MISURA/FISICA/era 1/CHIUSA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T3` (alta) — `T3` |
| `Z42` | `classe=CURA` | *CURAT* | `alta` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (alta) — `T0` |
| `Z67` | `classe=CURA` | *CURAT* | `alta` | `MISURA/FISICA/era 1/CHIUSA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (alta) — `T0` |
| `X3` | `classe=MISURA` | *e' uno stato* | `alta` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T1` (alta) — `T1` |
| `Z110` | `classe=MISURA` | *CHIUSA PER MISURA* | `alta` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (alta) — `T0` |
| `Z111` | `classe=MISURA` | *CHIUSA PER MISURA* | `alta` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (alta) — `T0` |
| `Z62` | `classe=MISURA` | *CHIUSA PER MISURA* | `alta` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T3` (alta) — `T3` |
| `U2` | `classe=DIFETTO` | *VA MISURATA, non assunta* | `alta` | `MISURA/FISICA/era 1/CHIUSA` → ### **`DIFETTO/FISICA/era 1/CHIUSA`** | ['classe'] in `T1` (alta) — `T1` |
| `CHK3-D` | `classe=MISURA` | *Solo misure e letture del sorgente* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/SOSPESA`** | ['classe'] in `T1` (alta) — `T1` |
| `SCALE-TW` | `classe=FRONTE` | *NON* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T1` (alta) — `T1` |
| `PROBLEMI-CHK3` | `classe=FRONTE` | *NON* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T1` (alta) — `T1` |
| `E3` | `classe=FRONTE` | *NON* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T3` (alta) — `T3` |
| `Z10` | `classe=DIFETTO` | *difetto di suo* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ['classe'] in `T0` (alta) — `T0` |
| `X2` | `classe=DIFETTO` | *Due difetti distinti* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ['classe'] in `T1` (alta) — `T1` |
| `PAT-1` | `classe=DIFETTO` | *non rispetta il pattern* | `alta` | `CURA/METODO/era 1/SOSPESA` → ### **`DIFETTO/METODO/era 1/SOSPESA`** | ['classe'] in `T0` (alta) — `T0` |
| `PAT-2` | `classe=DIFETTO` | *non rispetta il pattern* | `alta` | `CURA/METODO/era 1/SOSPESA` → ### **`DIFETTO/METODO/era 1/SOSPESA`** | ['classe'] in `T0` (alta) — `T0` |
| `EM-CURVATURA-BIDIREZIONALE` | `classe=FRONTE` | *DA VERIFICARE* | `alta` | `MISURA/FISICA/era 2/AGENDA` → ### **`FRONTE/FISICA/era 2/AGENDA`** | ['classe'] in `T0` (alta) — `T0` |
| `LORENTZ-MATERIA-INTERFERENZA` | `classe=FRONTE` | *DA VERIFICARE* | `alta` | `MISURA/FISICA/era 2/AGENDA` → ### **`FRONTE/FISICA/era 2/AGENDA`** | ['classe'] in `T0` (alta) — `T0` |
| `SIGILLO-CURA2-RIPARATO` | `classe=MISURA` | *FINITO 5/5* | `alta` | `DIFETTO/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T2` (alta) — `T2` |
| `POTENZE-1` | `classe=CURA` | *sigillo* | `alta` | `MISURA/FISICA/era 1/CHIUSA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (alta) — `T0` |
| `RAMPA-1` | `classe=CURA` | *sigillo* | `alta` | `MISURA/FISICA/era 1/CHIUSA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (alta) — `T0` |
| `POTATURA-GUARDIE` | `dominio=INFRASTRUTTURA` | *i 57 rami MORTI* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`FRONTE/INFRASTRUTTURA/era 1/SOSPESA`** | ['dominio'] in `T4` (alta) — `T4` |
| `D37` | `dominio=INFRASTRUTTURA` | *CHIAVE DUPLICATA NEI DOMINI* | `alta` | `DIFETTO/FISICA/era 1/CHIUSA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/CHIUSA`** | ['dominio'] in `T0` (alta) — `T0` |
| `Z14` | `da_dividere=DIFETTO/FISICA/1 + STANDARD/METODO/ENTRAMBE` | *REGOLA GENERALE* | `alta` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`FRONTE/FISICA/era 1/CHIUSA`** | ['da_dividere', 'da_dividere_parti'] in `T1` (alta) — `T1` |
| `Z22` | `classe=STANDARD dominio=METODO era=ENTRAMBE stato=APERTA` | *Una regola che non impedisce* | `alta` | `MISURA/FISICA/era 1/CHIUSA` → ### **`STANDARD/METODO/era ENTRAMBE/CHIUSA`** | ['classe', 'dominio', 'era', 'stato'] in `T1` (alta) — `T1` |
| `Z68` | `classe=CURA` | *sigillo 3/3* | `media` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T4` (media) — `T4` |
| `Z73` | `classe=MISURA` | *RITIRATA* | `media` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (media) — `T0` |
| `Z70` | `classe=MISURA` | *C'E', MA NON E' ISTANTANEO* | `media` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (media) — `T0` |
| `Z8` | `stato=SOSPESA` | *NON e' caratterizzato* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/SOSPESA`** | ['stato'] in `T0` (media) — `T0` |
| `Z19` | `stato=SOSPESA` | *non e' mai stata fatta* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/SOSPESA`** | ['stato'] in `T1` (media) — `T1` |
| `CHK3` | `classe=FRONTE` | *QUI CI SI FERMA* | `media` | `CURA/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T1` (media) — `T1` |
| `PROVA-COMB` | `classe=FRONTE` | *l'insieme no* | `media` | `CURA/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T1` (media) — `T1` |
| `Z1` | `classe=DIFETTO` | *NON e' stata cablata* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ['classe'] in `T0` (media) — `T0` |
| `Z101` | `classe=MISURA` | *6 criteri su 8 REGGONO* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/SOSPESA`** | ['classe'] in `T0` (media) — `T0` |
| `Z148` | `classe=MISURA` | *ACCLARATO* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/SOSPESA`** | ['classe'] in `T4` (media) — `T4` |
| `S13` | `classe=FRONTE` | *proposta per TUTTO il sistema* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T0` (media) — `T0` |
| `MASSA-MIGRA` | `classe=FRONTE` | *NON VA CORRETTO* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T4` (media) — `T4` |
| `GUSCIO-ANTIFASE-EMERGENTE` | `classe=FRONTE` | *IPOTESI DI LUCA* | `media` | `MISURA/FISICA/era 1/SOSPESA` → ### **`FRONTE/FISICA/era 1/SOSPESA`** | ['classe'] in `T0` (media) — `T0` |
| `REGISTRO_FISICA:D33` | `classe=DIFETTO` | *la repulsione si spegne* | `media` | `MISURA/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ['classe'] in `T0` (media) — `T0` |
| `Z32` | `classe=MISURA stato=CHIUSA` | *INTATTA* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T0` (media) — `T0` |
| `Z33` | `classe=MISURA stato=CHIUSA` | *VERDETTO* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T1` (media) — `T1` |
| `Z34` | `classe=MISURA stato=CHIUSA` | *VERDETTO* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T1` (media) — `T1` |
| `Z37` | `classe=MISURA stato=CHIUSA` | *FALLISCE SU ENTRAMBI I FRONTI* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['chiusura', 'classe', 'stato'] in `T0` (media) — `T0` |
| `Z88` | `dominio=METODO` | *SERVE A CHI RILEGGE* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`FRONTE/METODO/era 1/SOSPESA`** | ['dominio'] in `T1` (media) — `T1` |
| `MASSA-ID` | `classe=FRONTE` | *messo IN CODA* | `media` | `DIFETTO/METODO/era 1/SOSPESA` → ### **`FRONTE/METODO/era 1/SOSPESA`** | ['classe'] in `T4` (media) — `T4` |
| `W5` | `classe=CRITERIO` | *A/B nel driver* | `media` | `DIFETTO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/SOSPESA`** | ['classe'] in `T0` (media) — `T0` |
| `Z125` | `classe=DIFETTO` | *DIFETTO DI METODO, MIO* | `media` | `FRONTE/METODO/era ENTRAMBE/APERTA` → ### **`DIFETTO/METODO/era ENTRAMBE/APERTA`** | ['classe'] in `T0` (media) — `T0` |
| `Z15` | `classe=DIFETTO` | *e' un DEBITO* | `media` | `FRONTE/METODO/era 1/SOSPESA` → ### **`DIFETTO/METODO/era 1/SOSPESA`** | ['classe'] in `T4` (media) — `T4` |
| `LOSCHMIDT-ECO` | `classe=FRONTE` | *NON da fare oggi* | `media` | `MISURA/METODO/era ENTRAMBE/APERTA` → ### **`FRONTE/METODO/era ENTRAMBE/APERTA`** | ['classe'] in `T4` (media) — `T4` |
| `C19` | `dominio=METODO` | *Controllo di identita' cablato* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/METODO/era 1/CHIUSA`** | ['dominio'] in `T1` (media) — `T1` |
| `D10` | `dominio=INFRASTRUTTURA` | *INVISIBILE* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ['dominio'] in `T0` (media) — `T0` |
| `A4-METRICHE` | `classe=FRONTE dominio=METODO` | *il pannello fedele viene prima* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`FRONTE/METODO/era 1/SOSPESA`** | ['classe', 'dominio'] in `T1` (media) — `T1` |
| `Z130` | `dominio=METODO` | *Conta le invocazioni* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/METODO/era 1/CHIUSA`** | ['dominio'] in `T1` (media) — `T1` |
| `Z136` | `classe=MISURA` | *CHIUSA PER DIMOSTRAZIONE* | `media` | `FRONTE/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ['classe'] in `T0` (media) — `T0` |
| `REG-R` | `classe=PRESIDIO` | *l'hook che RIFIUTA* | `media` | `DIFETTO/INFRASTRUTTURA/era ENTRAMBE/APERTA` → ### **`PRESIDIO/METODO/era ENTRAMBE/APERTA`** | ['classe'] in `T1` (media) — `T1` |
| `SIGILLO-COMPARATORE-DUPLICATO` | `classe=DIFETTO` | *PERCHE E UN DIFETTO* | `media` | `FRONTE/INFRASTRUTTURA/era 1/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ['classe'] in `T0` (media) — `T0` |
| `SIGILLO-REGISTRO-NON-CONFRONTABILE` | `classe=DIFETTO` | *il difetto va in coda* | `media` | `FRONTE/INFRASTRUTTURA/era 1/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ['classe'] in `T4` (media) — `T4` |
| `SIGILLO-SENZA-CONFIGURAZIONE` | `classe=DIFETTO` | *il difetto va in coda* | `media` | `FRONTE/INFRASTRUTTURA/era 1/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ['classe'] in `T4` (media) — `T4` |
| `C25` | `era=ENTRAMBE` | *git lo NORMALIZZA* | `media` | `MISURA/INFRASTRUTTURA/era 1/CHIUSA` → ### **`MISURA/INFRASTRUTTURA/era ENTRAMBE/CHIUSA`** | ['era'] in `T1` (media) — `T1` |
| `D05` | `classe=FRONTE dominio=INFRASTRUTTURA` | *I4 scatola nera* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`FRONTE/INFRASTRUTTURA/era 1/SOSPESA`** | ['classe', 'dominio'] in `T0` (media) — `T0` |
| `CLI-1` | `classe=DIFETTO dominio=METODO da_dividere=DIFETTO/METODO/1 + STANDARD/METODO/ENTRAMBE` | *vale come regola generale* | `media` | `CURA/INFRASTRUTTURA/era 1/SOSPESA` → ### **`DIFETTO/METODO/era 1/SOSPESA`** | ['classe', 'da_dividere', 'da_dividere_parti', 'dominio'] in `T1` (media) — `T1` |

### **LE `23` APPLICATE IN PARTE**

### ⭐ **Queste sono la ragione per cui il verdetto e- PER RIGA:** un conteggio per campo le metterebbe ### **due volte**, fra le applicate e fra le lasciate.

| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |
|---|---|---|---|---|---|
| `D0` | `classe=MISURA stato=CHIUSA` | *MISURATO: e' IL FRENO* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `G2` | `classe=MISURA stato=CHIUSA` | *FATTO. Il saldo vive sul CONFINE* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `G3` | `classe=MISURA stato=CHIUSA` | *sigillo 7/7* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `G4` | `classe=MISURA stato=CHIUSA` | *FATTO (finito 14:39:27)* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `S03` | `classe=MISURA stato=CHIUSA` | *DECISO da Z109* | `alta` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `S04` | `classe=MISURA stato=CHIUSA` | *CADE con Z108* | `alta` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z13` | `classe=CURA stato=CHIUSA` | *CHIUSA il 2026-09-17* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z29` | `classe=CURA stato=CHIUSA` | *Sigillo 8/8* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z30` | `classe=MISURA stato=CHIUSA` | *CHIUSA il 2026-09-18* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z53` | `classe=CURA stato=CHIUSA` | *CURATO, SIGILLO 9/9 PASS* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z5` | `classe=MISURA stato=CHIUSA` | *chiusa per DIMOSTRAZIONE* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z28` | `classe=CRITERIO dominio=METODO stato=CHIUSA` | *CHIUSA PRIMA DI NASCERE* | `alta` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z2` | `classe=DIFETTO stato=SOSPESA` | *A1 resta violato* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/SOSPESA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): 9-17) / La correzione (2) ha sostituito 0.02median(self.d0)re) |
| `Z6` | `classe=DIFETTO stato=SOSPESA` | *BLOCCO STRUTTURALE* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/SOSPESA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): al posto di NaN) e ① inerzia (rho/peq = 0/0 = NaN in omega_s)) |
| `Z21` | `classe=MISURA stato=SUPERATA` | *era UN SEME* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/SUPERATA`** | ### **`stato`=`SUPERATA`**: ### `SUPERATA` SENZA DIRE DA CHE COSA: lo schema pretende `superata_da`, e il file non lo porta. <<Superata>> vuol dire CHE QUALCUNO HA DECISO ALTRO, e chi ha deciso NON SI INVENTA |
| `Z27` | `classe=MISURA stato=CHIUSA` | *Z24 MISURATA* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z91` | `classe=DIFETTO stato=CHIUSA` | *CRICCHETTO E' CURATO* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### **`stato`=`CHIUSA`**: ### LA REGOLA DELLO STATO DA- `SOSPESA`, NON `CHIUSA`: la riga CONTRADDICE il cambio (la riga dice <<APERTA>> (la PRIMA parola di stato): / Z91 APERTA [EPOCA 2 · LETTURA DEL CODICE] / SCALA_) |
| `Z92` | `classe=DIFETTO stato=CHIUSA` | *CURATA* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### **`stato`=`CHIUSA`**: ### LA REGOLA DELLO STATO DA- `SOSPESA`, NON `CHIUSA`: la riga CONTRADDICE il cambio (la riga dice <<APERTA>> (la PRIMA parola di stato): freno che cresceva insieme alla fuga. / APERTA come LIMITE, non come) |
| `Z7` | `classe=DIFETTO dominio=INFRASTRUTTURA` | *SCRITTO e MAI LETTO* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/CHIUSA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `FRONTE`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<una domanda o un programma, e la voce e- aperta>> (la PRIMA che compare): be cs^-4) non rompe nessun cons) |
| `Y2` | `classe=DIFETTO stato=SOSPESA` | *resta muta* | `media` | `MISURA/METODO/era 1/CHIUSA` → ### **`MISURA/METODO/era 1/SOSPESA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): V / (a) u1_segno_ov_nullo scrive 2/pi = 0.6366, ma canon vien) |
| `REGISTRO_FISICA:E4-LAM` | `classe=CURA stato=CHIUSA` | *SI VERIFICA SEMPRE* | `media` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CURA/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `COMPONENTI:A1` | `classe=CURA dominio=FISICA stato=CHIUSA` | *PROMOSSA il 2026-09-16* | `media` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CURA/METODO/era 1/CHIUSA`** | ### **`dominio`=`FISICA`**: ### la citazione si trova in `T4` -- la SEZIONE, o il FILE -- non nella voce ne- nella sua riga, e per `dominio` la regola del punto 1 non ha una lettura: una sezione contiene anche le voci vicine · ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Y1` | `classe=DIFETTO dominio=METODO` | *zero fisica* | `media` | `FRONTE/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### **`dominio`=`METODO`**: ### la citazione si trova in `T4` -- la SEZIONE, o il FILE -- non nella voce ne- nella sua riga, e per `dominio` la regola del punto 1 non ha una lettura: una sezione contiene anche le voci vicine |

### **LE `44` LASCIATE**

### ⛔ **«Lasciata» NON vuol dire «ignorata»:** vuol dire che la riga intera ### **NON sostiene il cambio**, e il motivo e- scritto. ### **La regola del mandato dice «altrimenti elenca con una riga di motivo».**

| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |
|---|---|---|---|---|---|
| `C13` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C17` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C18` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C22` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C23` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C24` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C1-PEQ-ESATTO` | `stato=CHIUSA` | *✅* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C1BIS-ANOM-SIMM` | `stato=CHIUSA` | *✅* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C2-PEQ-NASCITA` | `stato=CHIUSA` | *✅* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C3-SCALA-MIN-PASSO` | `stato=CHIUSA` | *✅* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C4-COES-CAUSALE` | `stato=CHIUSA` | *✅* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `CHK2` | `stato=CHIUSA` | *raggiunto e riferito a Luca* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `COMPONENTI:S3b` | `stato=CHIUSA` | *SIGILLATA con controllo positivo* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `COMPONENTI:S3c` | `stato=CHIUSA` | *SIGILLATA con controllo positivo* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `D34` | `stato=CHIUSA` | *CURATO IN CODICE* | `alta` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `S02` | `stato=SUPERATA superata_da=D31` | *PROMOSSO* | `alta` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SUPERATA`** | ### **`stato+superata_da`=`D31`**: ### `D31` NON E- UNA DECISIONE NE- UN ASSIOMA, e lo schema la rifiuta: una voce superata deve essere superata DA UNA DECISIONE, e un difetto non decide niente |
| `REGISTRO_FISICA:P2` | `stato=CHIUSA` | *P2 È FALLITA* | `alta` | `MISURA/FISICA/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `REGISTRO_FISICA:T3` | `stato=CHIUSA` | *PASS* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `REGISTRO_FISICA:T4` | `stato=CHIUSA` | *PASS* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `REGISTRO_FISICA:T5` | `stato=CHIUSA` | *PASS* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `REGISTRO_FISICA:U2-5` | `stato=CHIUSA` | *PASS* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `REGISTRO_FISICA:U2-6` | `stato=CHIUSA` | *PASS* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `T3a` | `stato=CHIUSA` | *PASS* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `T3b` | `stato=CHIUSA` | *PASS* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z142` | `stato=CHIUSA` | *E4-LAM PASSA* | `alta` | `DIFETTO/METODO/era 1/SOSPESA` → ### **`DIFETTO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `C5` | `stato=CHIUSA` | *C. DIAGNOSI CHIUSE* | `media` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `H1` | `stato=CHIUSA` | *H1 NON BASTA* | `media` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `H3` | `stato=CHIUSA` | *500 su 500* | `media` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `DE-ACCOPPIABILITA` | `stato=CHIUSA` | *superata dai fatti* | `media` | `MISURA/FISICA/era 1/SOSPESA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `REGISTRO_FISICA:P3` | `stato=CHIUSA` | *TIENE* | `media` | `MISURA/FISICA/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `Z50` | `classe=MISURA` | *NON E' UNA Y* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### **`classe`=`MISURA`**: ### LA REGOLA DELLA CLASSE DA- `DIFETTO`, NON `MISURA`: la riga CONTRADDICE il cambio (la riga dice <<DIFETTO MIO>> (la PRIMA che compare): O, un seme) / E PRIMA DEL RISULTATO, UN DIFETTO MIO, trovato perche) |
| `Z54` | `classe=CURA` | *Sigillo 12/12* | `media` | `MISURA/INFRASTRUTTURA/era 1/CHIUSA` → ### **`MISURA/INFRASTRUTTURA/era 1/CHIUSA`** | ### **`classe`=`CURA`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `CURA`: la riga CONTRADDICE il cambio (la riga dice <<CHIUSA PER MISURA>> (la PRIMA che compare): ampi: l'archivio non tocca la fisica. / CHIUSA per MISURA. To) |
| `Z86` | `classe=DIFETTO` | *ERA SBAGLIATO* | `media` | `MISURA/METODO/era 1/CHIUSA` → ### **`MISURA/METODO/era 1/CHIUSA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): f884eff0 sul simulatore 43972024, esito 7/9; doc/REFERTO_sigi) |
| `Z145` | `classe=DIFETTO` | *era invalido* | `media` | `MISURA/METODO/era 1/CHIUSA` → ### **`MISURA/METODO/era 1/CHIUSA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): ubprocess, ingresso --braccio. Collaudo 8/8, con K7/K8 che pr) |
| `L-SOGLIA` | `stato=CHIUSA` | *fusa dentro* | `media` | `STANDARD/METODO/era ENTRAMBE/APERTA` → ### **`STANDARD/METODO/era ENTRAMBE/SUPERATA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `STANDARD-4` | `stato=CHIUSA` | *fusa dentro* | `media` | `STANDARD/METODO/era ENTRAMBE/APERTA` → ### **`STANDARD/METODO/era ENTRAMBE/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |
| `SCHED-T3-REGOLE` | `dominio=FISICA` | *Le eccezioni sono ZERO* | `media` | `MISURA/DOCUMENTAZIONE/era ENTRAMBE/APERTA` → ### **`MISURA/DOCUMENTAZIONE/era ENTRAMBE/APERTA`** | ### **`dominio`=`FISICA`**: ### la citazione si trova in `T4` -- la SEZIONE, o il FILE -- non nella voce ne- nella sua riga, e per `dominio` la regola del punto 1 non ha una lettura: una sezione contiene anche le voci vicine |
| `D11` | `classe=DIFETTO` | *CURATO* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): i sotto LAM sono ZERO, con min(d)/LAM = 1.000000 esatto (Z148) |
| `D17` | `classe=DIFETTO` | *CURATO* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`classe`=`DIFETTO`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `DIFETTO`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): x(peq, 1e-9) NE RIBALTAVA IL SEGNO (da -3.72 a +1.8e+06) / Z9) |
| `C7` | `classe=CURA` | *Curata* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`classe`=`CURA`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `CURA`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): rev veniva scartata a ogni mitosi ⇒ nel 72 % delle chiamate t) |
| `C11` | `classe=CURA` | *CURATO* | `media` | `MISURA/FISICA/era 1/CHIUSA` → ### **`MISURA/FISICA/era 1/CHIUSA`** | ### **`classe`=`CURA`**: ### LA REGOLA DELLA CLASSE DA- `MISURA`, NON `CURA`: la riga CONTRADDICE il cambio (la riga dice <<un esito misurato>> (la PRIMA che compare): sa convenzione / guardia 4π fallita nel 95.33 % (143/150), co) |
| `D04` | `dominio=INFRASTRUTTURA` | *invisibile alla traccia* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### **`dominio`=`INFRASTRUTTURA`**: ### la citazione si trova in `T4` -- la SEZIONE, o il FILE -- non nella voce ne- nella sua riga, e per `dominio` la regola del punto 1 non ha una lettura: una sezione contiene anche le voci vicine |
| `CENS-A1` | `dominio=DOCUMENTAZIONE` | *dichiarata e FALSA* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### **`dominio`=`DOCUMENTAZIONE`**: ### la citazione si trova in `T4` -- la SEZIONE, o il FILE -- non nella voce ne- nella sua riga, e per `dominio` la regola del punto 1 non ha una lettura: una sezione contiene anche le voci vicine |
| `MITOSI-2LAM-ACCESO` | `stato=CHIUSA` | *ANNOTAZIONE DEL 2026-10-02* | `media` | `DIFETTO/DOCUMENTAZIONE/era 1/SOSPESA` → ### **`DIFETTO/DOCUMENTAZIONE/era 1/CHIUSA`** | ### **`stato`=`CHIUSA`**: ### la riga NON PORTA UN COMMIT, e chiudere pretende `chiusura.commit`: un commit NON SI INVENTA (la stessa regola del punto 1) |

### **LE `19` NON APPLICATE**

### ⛔ **La citazione NON COMPARE**, e il mandato dice ### **«NON applicare, elenca».** ### **Non ho cercato una frase simile:** una citazione che non si trova ### **non si avvicina a mano.**

| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |
|---|---|---|---|---|---|
| `CENS-A4` | `stato=CHIUSA` | *Questo commit corregge SOLO il commento* | `alta` | `DIFETTO/DOCUMENTAZIONE/era 1/SOSPESA` → ### **`DIFETTO/DOCUMENTAZIONE/era 1/SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/CENSIMENTO_intenzioni.md` |
| `REGISTRO_FISICA:D37` | `stato=CHIUSA` | *È CURATO* | `alta` | `DIFETTO/INFRASTRUTTURA/era 1/SOSPESA` → ### **`DIFETTO/INFRASTRUTTURA/era 1/SOSPESA`** | ### COMPARE NEL FILE `doc/REGISTRO_FISICA.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `CHI-TORS-ZERO-FALSO` | `classe=DIFETTO stato=SOSPESA` | *la voce resta aperta* | `alta` | `MISURA/METODO/era 1/CHIUSA` → ### **`MISURA/METODO/era 1/CHIUSA`** | ### COMPARE NEL FILE `doc/STATO_RUN.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `B2` | `classe=DIFETTO stato=SOSPESA` | *NON RIPARATI IN QUESTO GIRO* | `alta` | `MISURA/METODO/era 1/CHIUSA` → ### **`MISURA/METODO/era 1/CHIUSA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/STATO_RUN.md` |
| `REGISTRO_FISICA:SCENA-1` | `classe=CURA dominio=FISICA stato=CHIUSA` | *CHIUSA il 2026-09-25* | `alta` | `CRITERIO/METODO/era 1/SOSPESA` → ### **`CRITERIO/METODO/era 1/SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/REGISTRO_FISICA.md` |
| `Q6` | `classe=DIFETTO stato=CHIUSA` | *il FAIL era del criterio* | `alta` | `PRESIDIO/METODO/era 1/SOSPESA` → ### **`PRESIDIO/METODO/era 1/SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `CLAUDE.md` |
| `R3` | `classe=DIFETTO stato=CHIUSA` | *il FAIL era del criterio* | `alta` | `PRESIDIO/METODO/era 1/SOSPESA` → ### **`PRESIDIO/METODO/era 1/SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `CLAUDE.md` |
| `R5` | `classe=DIFETTO stato=CHIUSA` | *il FAIL era del criterio* | `alta` | `PRESIDIO/METODO/era 1/SOSPESA` → ### **`PRESIDIO/METODO/era 1/SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `CLAUDE.md` |
| `U3` | `classe=DIFETTO stato=CHIUSA` | *il FAIL era del criterio* | `alta` | `PRESIDIO/METODO/era 1/SOSPESA` → ### **`PRESIDIO/METODO/era 1/SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `CLAUDE.md` |
| `FASCE-TAU` | `classe=FRONTE` | *DA VERIFICARE* | `alta` | `CURA/FISICA/era 2/AGENDA` → ### **`CURA/FISICA/era 2/AGENDA`** | ### COMPARE NEL FILE `doc/STATO_RUN.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `L-STELLA` | `classe=STANDARD` | *Regola scritta, NON un presidio* | `alta` | `PRESIDIO/METODO/era ENTRAMBE/APERTA` → ### **`STANDARD/METODO/era ENTRAMBE/APERTA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `CLAUDE.md par.11` |
| `CICLO-CHIUSURA-SEGNO` | `dominio=METODO` | *NON tocca la fisica* | `alta` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### COMPARE NEL FILE `doc/STATO_RUN.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `D27` | `stato=CHIUSA` | *NON E' UN DIFETTO NEL SISTEMA ATTUALE* | `media` | `DIFETTO/FISICA/era 1/SOSPESA` → ### **`DIFETTO/FISICA/era 1/SOSPESA`** | ### COMPARE NEL FILE `doc/STATO_RUN.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `SCHED-PASSO` | `dominio=INFRASTRUTTURA` | *architettura del passo, non fisica* | `media` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/SOSPESA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/PIANO_schedulatore_passo.md` |
| `D26` | `stato=CHIUSA` | *La cura in se' resta valida* | `media` | `DIFETTO/METODO/era 1/SOSPESA` → ### **`DIFETTO/METODO/era 1/SOSPESA`** | ### COMPARE NEL FILE `doc/STATO_RUN.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |
| `REG-A` | `classe=MISURA stato=CHIUSA` | *FATTA (1214283)* | `media` | `DIFETTO/FISICA/era 1/CHIUSA` → ### **`DIFETTO/FISICA/era 1/CHIUSA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/STATO_RUN.md` |
| `TW-DIVISIONE-INCOGNITA` | `classe=MISURA dominio=METODO` | *una soglia misurata nel posto sbagliato* | `media` | `DIFETTO/FISICA/era 1/CHIUSA` → ### **`DIFETTO/FISICA/era 1/CHIUSA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `csv/_test_fork/_misure_calore/` |
| `ESENTE-P3` | `classe=PRESIDIO` | *ESENTE-H-P3* | `media` | `DIFETTO/METODO/era ENTRAMBE/APERTA` → ### **`DIFETTO/METODO/era ENTRAMBE/APERTA`** | NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel file `doc/STATO_RUN.md` |
| `C5RES-INVARIANTI` | `classe=FRONTE dominio=INFRASTRUTTURA` | *I4 scatola nera* | `media` | `CURA/FISICA/era 1/SOSPESA` → ### **`CURA/FISICA/era 1/SOSPESA`** | ### COMPARE NEL FILE `doc/STATO_RUN.md` MA FUORI DALLA SEZIONE della voce, e la regola chiede la riga o la sezione che la contiene |

---

## ④ LE DUE CONVENZIONI, **lette da `CLAUDE.md`**

> ### ⛔ **«In vigore» = «citato in `CLAUDE.md` OGGI»**, non *«mi pare in uso»*. Gli ID ### **si leggono dalle due tabelle**, e se un ID sparisse da la- lo strumento ### **smetterebbe di dichiararlo in vigore DA SE-.**

| | gli ID |
|---|---|
| §`11`, ### **le regole di lavoro** *(`8`)* | `P1` · `P2` · `P1-quater` · `L-PATCH` · `L-NUMERI` · `L-UN-PROMPT` · `L-STELLA` · `L-DOPO-STOP` |
| §`12`, ### **i cablati** *(`14`)* | `H-P3` · `H-P5` · `H-P7` · `H-P8` · `H-VALIDATORE` · `H-RIGHE` · `H-P1-bis` · `H-REG-R` · `H-INDICE` · `H-FILE` · `H-NON-TRACCIATI` · `H-FISICA-FUORI-LISTA` · `H-ID-OBBLIGATORIO` · `H-STASH` |

| id | prima | dopo | perche' |
|---|---|---|---|

### ✔ **E `22` erano GIA- a posto:** `P1` · `P2` · `P1-quater` · `L-PATCH` · `L-NUMERI` · `L-UN-PROMPT` · `L-STELLA` · `L-DOPO-STOP` · `H-P3` · `H-P5` · `H-P7` · `H-P8` · `H-VALIDATORE` · `H-RIGHE` · `H-P1-bis` · `H-REG-R` · `H-INDICE` · `H-FILE` · `H-NON-TRACCIATI` · `H-FISICA-FUORI-LISTA` · `H-ID-OBBLIGATORIO` · `H-STASH`.

---

## ⑤ IL PUNTO `5`: **`F6` trova `G1`**, e la via grossolana dava `69` segnali

| | |
|---|---|
| la nota di `G1` | *«»* |
| la voce oggi | `MISURA`/`FISICA`/era `1`/### **`CHIUSA`** |
| perche' `F6` NON la trovava | ### **due ragioni**: la nota non nomina *«la lista `N` del guardiano»*, e dice *«correzione»* — che era escluso come ### **informativo** |
| l'estensione | una nota che scrive ### **la forma esatta `DOMINIO/era N/STATO`** fa ### **un'ASSERZIONE**, e se la voce si e- mossa ### **la nota e- SCADUTA** |
| quante note hanno quella forma | ### **`6`** su `846` voci, e ### **una sola e- incoerente: `G1`** |
| ### ⛔ **la via grossolana** | *«la nota nomina uno stato diverso da quello della voce»* dava ### **`69` SEGNALI**, perche' la maggior parte delle note parla ### **di un'altra era** o ### **fa una DOMANDA** *(«superata da `A16`?»)*. ### **Era la condizione di FERMO scritta nel task history, e mi sono fermato** |

### ✔ **E IL COLLAUDO MISURA I `69`**, invece di dire *«era troppo grossa»*: ### **una scelta scartata senza numero e- un'opinione.** Piu' ### **il braccio negativo** che prova che `F6` ### **non scatta per la PAROLA**: con la stessa nota e la tripla ### **allineata**, ### **tace.**

### ⚠ **E LA NOTA DI `G1` NON LA RISCRIVO.** Il mandato dice *«`F6` deve trovarla»*, ### **non «correggila»** — e un segnale ### **si elenca, non si spegne cambiando la voce.** ### 📌 **LA DOMANDA A LUCA: la nota di `G1` va riscritta o TOLTA?** La sua storia vive ### **in `storico.jsonl`**, quindi togliere la nota ### **non perde niente** — ma e' ### **una decisione, non una pulizia.**

---

## ⑥ DUE AFFERMAZIONI DEL GUARDIANO SI CONTRADDICONO, **e non scelgo io**

`C3` *(«le liste del guardiano: classificazione come indicata»)* ### **e- FALLITO**, e non l'ho zittito.

| id | la lista vecchia | il file nuovo | la citazione del file |
|---|---|---|---|
| `CLI-1` | lista `1` | `classe=DIFETTO dominio=METODO da_dividere=DIFETTO/METODO/1 + STANDARD/METODO/ENTRAMBE` | *vale come regola generale* |
| `POTATURA-GUARDIE` | lista `3` | `dominio=INFRASTRUTTURA` | *i 57 rami MORTI* |

### ✔ **La riconciliazione e- TEMPORALE e CITATA:** la verifica completa e- la parola ### **piu' recente** del guardiano, e ### **porta una frase del repo**; le liste ### **non citavano niente.** Sta in `csv/_controlli_indice_v2.py`, nel posto ### **dichiarato** dove *«il controllo dice che cosa si aspetta OGGI»*, e ### **va per ultima** perche' ### **l'ultima assegnazione vince** *(un blocco piu' sopra riscriveva `CLI-1`, e la prima stesura della riconciliazione ### **veniva sovrascritta**)*.

### ⛔ **MA E- IL GUARDIANO CHE HA CAMBIATO IDEA, E LUCA DEVE SAPERLO.** La regola del guardiano stesso dice: *«due misure incompatibili sullo stesso oggetto ### **si riconciliano, non si sceglie**»*. ### **Io ho scelto la FORMA della riconciliazione** *(il piu' recente vince, ### **se cita**)*, ### **non il merito.**

---

## ⑦ I CONTEGGI E I CONTROLLI

> **PRIMA** = `git show bfb1596` *(il task history, ### **prima di ogni scrittura del giro**)*. **DOPO** = il disco.

| `classe` | prima | dopo | |
|---|--:|--:|---|
| DIFETTO | `200` | `187` | ### **-13** |
| NON_DEFINITA | `187` | `187` |  |
| MISURA | `141` | `146` | ### **+5** |
| FRONTE | `109` | `109` |  |
| CRITERIO | `90` | `96` | ### **+6** |
| CURA | `56` | `56` |  |
| STANDARD | `29` | `42` | ### **+13** |
| PRESIDIO | `34` | `25` | ### **-9** |

| `dominio` | prima | dopo | |
|---|--:|--:|---|
| FISICA | `383` | `377` | ### **-6** |
| METODO | `198` | `216` | ### **+18** |
| DA_CLASSIFICARE | `187` | `187` |  |
| INFRASTRUTTURA | `49` | `52` | ### **+3** |
| DOCUMENTAZIONE | `29` | `16` | ### **-13** |

| `era` | prima | dopo | |
|---|--:|--:|---|
| 1 | `538` | `539` | ### **+1** |
| DA_CLASSIFICARE | `188` | `188` |  |
| ENTRAMBE | `96` | `97` | ### **+1** |
| 2 | `24` | `24` |  |

| `stato` | prima | dopo | |
|---|--:|--:|---|
| SOSPESA | `369` | `325` | ### **-44** |
| CHIUSA | `182` | `221` | ### **+39** |
| DA_CLASSIFICARE | `188` | `188` |  |
| APERTA | `82` | `86` | ### **+4** |
| AGENDA | `24` | `24` |  |
| SUPERATA | `1` | `4` | ### **+3** |

| | prima | dopo |
|---|--:|--:|
| voci | `846` | ### **`848`** |
| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |
| ### **righe di storico** | `1628` | ### **`1903`** |

| presidio | segnali | |
|---|--:|---|
| `F1` | ### **`8`** |  |
| `F2` | `0` |  |
| `F3` | ### **`1`** |  |
| `F4` | `0` |  |
| `F6` | ### **`2`** | ### **`G1`** e `POTATURA-GUARDIE` |
| `F8` | ### **`20`** |  |
| `F7` `F9` `F10` | ### **`0`** | ### **sono ERRORI: se non fossero zero, `valida` non passerebbe** |
| ### **in tutto** | ### **`31`** | ### **si elencano, non si correggono** |

### **I SEGNALI CHE RESTANO, voce per voce**

| `F1` | il segnale |
|---|---|
| `D05` | il titolo cita `C5`, che e- `FISICA`/era `1`, mentre questa e- `INFRASTRUTTURA`/era `1` |
| `D06` | il titolo cita `Z7`, che e- `INFRASTRUTTURA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `D08` | il titolo cita `Z14`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `D14` | il titolo cita `Z41`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `D18` | il titolo cita `Z92`, che e- `FISICA`/era `1`/`SOSPESA`, mentre questa e- `FISICA`/era `1`/`CHIUSA` |
| `D19` | il titolo cita `Z88`, che e- `METODO`/era `1`/`SOSPESA`, mentre questa e- `FISICA`/era `1`/`CHIUSA` |
| `D27` | il titolo cita `Z65`, che e- `FISICA`/era `1`/`CHIUSA`, mentre questa e- `FISICA`/era `1`/`SOSPESA` |
| `Z130` | il titolo cita `S10`, che e- `FISICA`/era `1`, mentre questa e- `METODO`/era `1` |

| `F6` | il segnale |
|---|---|
| `POTATURA-GUARDIE` | la nota nomina la lista `3` del guardiano e la voce NON e- piu- cio- che quella lista diceva: la lista diceva `FISICA`, la voce e- `INFRASTRUTTURA` |
| `REGISTRO_FISICA:U2-6` | la nota DICHIARA una tripla `dominio/era/stato` e la voce non e- piu- quella: la nota dichiara `SOSPESA`, la voce e- `CHIUSA` |

| `F8` | il segnale |
|---|---|
| `A7b` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<calcola_psi>>) |
| `A8` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<mitosi>>) |
| `A8b` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>) |
| `A9` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_presidio.py>>) |
| `CONTA-RIGHE` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_struttura_regole.py>>) |
| `FINESTRA-PRE-NASCITA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<perc_geom>>) |
| `H-FILE` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un flag `--...` (<<--cached>>); un file `.py` del repo (<<_hook_file_cambiati.py>>) |
| `H-FISICA-FUORI-LISTA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<_file_fisica.py>>) |
| `H-ID-OBBLIGATORIO` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un flag `--...` (<<--collaudo>>); un file `.py` del repo (<<_file_fisica.py>>) |
| `H-P9` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<net.step>>) |
| `INDICE-COLLAUDO-SCRITTURA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<indice.py>>) |
| `NON-TRACCIATI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un `.pkl` (<<.pkl>>); un file `.py` del repo (<<_censimento_non_tracciati.py>>) |
| `PASSO-PIENO` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<net.step>>); un file `.py` del repo (<<_passo.py>>) |
| `PIATTAFORMA-NON-TIMBRATA` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>); un file `.py` del repo (<<_confronto_blob_misure.py>>) |
| `PRESIDIO-RIFIUTO-SOLO-SIGILLI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_test_fork>>); un file `.py` del repo (<<_presidio.py>>) |
| `REG-R` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<soliton_simulator.py>>) |
| `REG-V` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: un file `.py` del repo (<<verificaregistro.py>>) |
| `REPERTI-IMMUTABILI` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: uno script di csv/_test_fork o csv/_seal_fork (<<csv/_seal_fork>>); un file `.py` del repo (<<_sim_A.py>>) |
| `RIPRESA-ARGV` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: il sigillo di una cura (<<sigillo della cura>>) |
| `Z125` | era `ENTRAMBE` ma nomina un oggetto dell-era 1: una funzione o una variabile del simulatore (<<mitosi>>) |

---

## ⑧ CHE COSA RESTA A LUCA

| | quante | che cosa |
|---|--:|---|
| ### **i due livelli `T0` e `T4`** | `49` + `33` | ### **li aggiungo IO**, e il mandato ne nomina tre: se sono troppo larghi, quelle righe vanno riviste |
| ### **le `19` non applicate** | `19` | ### **la citazione non compare**: o la frase non e' nel repo, o la `fonte` della voce ### **non punta dove dovrebbe** |
| ### **le chiusure senza commit** | `47` | righe che chiedono `CHIUSA` e ### **la riga non porta il commit**: ### **un commit non si inventa** |
| ### **le contraddizioni della riga** | `14` | la riga ### **dice il contrario** di cio' che il file chiede — e sono `media`, dove il mandato dice *«applica se la frase sostiene il cambio»* |
| ### **`CLI-1` e `POTATURA-GUARDIE`** | `2` | ### **il guardiano contraddice se stesso**: ho scelto la forma, non il merito |
| ### **`S02` e `Z21`** | `2` | lo schema le rifiuta: ### **una voce superata deve dire DA CHE COSA, e deve essere una DECISIONE** |
| ### **la nota di `G1`** | `1` | riscriverla o ### **toglierla**? |
| ### **i segnali di `F8`** | `20` | ### **sul confine fra le due frasi dell'era** |
| ### ⛔ **un mandato che non ho** | `1` | `doc/CODA_2026-10-09.md`: l'integrazione *«gli strumenti diventano obbligatori anche per l'era `2`»* e' arrivata, ### **il suo testo base NO** |

> ### ⭐ **Il criterio, lo stesso di tutto il lavoro:** dove il file ### **cita una frase del repo** l'ho applicato; dove ### **la riga dice il contrario**, ### **ho lasciato e ho scritto il motivo**; dove ### **due parole del guardiano si contraddicono**, ### **ho scelto la FORMA della riconciliazione e non il merito.** ### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un difetto.**

