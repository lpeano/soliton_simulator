# IL REFERTO DEL PIANO E DELL'ALBERO — **il mandato `3` di `6`**

> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: `csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- misurato A UN ISTANTE** — ### **la CI NON lo rigenera**, e il presidio verifica ### **il suo BLOB**. ### **Per rimisurarlo si rigira il suo comando AL SUO COMMIT**, come un sigillo *(`CLAUDE.md` par. `6`)*.

> ### ⛔ **Questo file e' GENERATO da `python csv/_referto_piano_era2.py`: non si scrive a mano, e NESSUN numero e' ricopiato** *(`L-NUMERI`)*.
> **Il simulatore:** `b8c21049`, ### **non toccato** *(sha1 dei byte grezzi, ASSERITO da questo script)*.
> **Il mandato dice:** *<<solo scrittura del piano: nessun codice di fisica, nessuna corsa>>* e *<<nessuna scelta di fisica in questo mandato>>*.

---

## `1.` I QUATTRO PUNTI, e che cosa e' stato fatto

| | il punto | l'esito |
|---|---|---|
| `1` | `doc/PIANO_era2.md`, le fasi con ingresso e uscita | ### **FATTO**: `F0`-`F4`, piu' un ### **tabellone di controllo** coi comandi |
| `2` | l'albero, nel piano ### **e** come nodi in `decisioni.jsonl` | ### **FATTO**: `10` nodi, e `decisioni.jsonl` passa da `25` a `35` record |
| `3` | ### **il presidio dell'albero**, nei due versi | ### **FATTO**: `P-ALB`, dentro `indice.py valida` |
| `4` | questo referto | ### **FATTO** |

### ⭐ **E LA REGOLA CHE HO MESSO IN TESTA AL PIANO, perche' vale per tutte le fasi: un criterio di uscita che NON ESCE DA UN COMANDO non e' un criterio.** ### **Se una fase si dichiara chiusa, si dice CON QUALE COMANDO** — e il piano porta i sei comandi che rispondono.

---

## `2.` CHE COSA HO TROVATO PRIMA DI COMINCIARE — ### **quattro difetti, e il peggiore era un presidio che TACEVA**

### ⛔ **Il task history ordinava come PRIMO PASSO:** *<<leggere ### **dal codice** chi valida `decisioni.jsonl`>>*. ### ⭐ **Quella lettura — fatta PRIMA di scrivere una riga del piano — ha trovato questo:**

| | l'ID | che cosa era |
|---|---|---|
| `1` | `REPLAY-CIECO-ALLE-CANCELLAZIONI` *(`APERTA`)* | il REPLAY di P-T2 non vedeva una cancellazione: 13 su 13 con 4 record tolti |
| `2` | `DUE-VIE-SU-LEGGI-JSONL` *(`CHIUSA`)* | due vie di scrittura si contendono leggi.jsonl e variabili.jsonl, e vince chi gira per ultimo |
| `3` | `H-INDICE-IGNORA-I-VOCABOLARI` *(`CHIUSA`)* | H-INDICE legge solo le voci: un ID di legge, variabile, assioma o decisione risulta IGNOTO |
| `4` | `FORMA-SPEZZA-ID` *(`CHIUSA`)* | la regex FORMA di H-INDICE spezzava 122 ID su 887, e verificava il PREFISSO |

### ⭐ **IL PEGGIORE E' IL PRIMO, e il perche' e' una frase che sembra la stessa e non lo e':** *<<ogni record coincide col `dopo` della sua ultima riga di storico>>* ### **NON E'** *<<lo storico si rigioca in questo file>>*. ### **La prima e' vera anche su un file META' VUOTO**, e per questo `P-T2` passava ### **`13` su `13` con QUATTRO record cancellati.**

### ⚠ **E IL SECONDO SPIEGA PERCHE' IL PRIMO CONTAVA:** un giro del generatore dell'era `1` ### **cancellava i quattro record dell'era `2`**, e ### **il conto delle leggi di `timbro.py` esce dalla TABELLA** — quindi quel giro avrebbe portato il conto a ### **zero senza toccare un file di codice.**

### 📌 **E IL QUARTO L'HA TROVATO IL PRESIDIO STESSO, rifiutandomi un commit:** `H-INDICE` verificava ### **il PREFISSO invece dell'ID** per ### **`122` ID su `887`**, e il difetto era ### **MUTO** perche' le code degli altri `122` non hanno un trattino.

---

## `3.` L'ALBERO, come il mandato lo scrive

| il nodo | l'etichetta di Luca | `presa` | dipende da | argomento noto |
|---|---|---|---|---|
| `DEC-D9-GEOMETRIA` | `D9` | no | ### *radice* | si' |
| `DEC-D13-MEMORIE` | `D13` | no | `DEC-D9-GEOMETRIA` | si' |
| `DEC-D6-VUOTO` | `D6` | no | `DEC-D13-MEMORIE` | si' |
| `DEC-D7-DIVISIONE` | `D7` | no | `DEC-D6-VUOTO` | si' |
| `DEC-INT-INTEGRATORE` | `INT` | no | ### *radice* | si' |
| `DEC-D2-DA-CHIEDERE` | `D2` | no | ### *radice* | ### ⛔ **NO** |
| `DEC-D4-DA-CHIEDERE` | `D4` | no | ### *radice* | ### ⛔ **NO** |
| `DEC-D11-DA-CHIEDERE` | `D11` | no | ### *radice* | ### ⛔ **NO** |
| `DEC-D12-DA-CHIEDERE` | `D12` | no | ### *radice* | ### ⛔ **NO** |
| `DEC-T4-DA-CHIEDERE` | `T4` | no | ### *radice* | ### ⛔ **NO** |

| | |
|---|--:|
| nodi | `10` |
| archi | `3` |
| radici gia' prese | `2` — `DEC-A16`, `DEC-A17` |
| ### **nodi `presa`** | ### **`0`** |
| ### **nodi senza argomento noto** | ### **`5`** |

### ✅ **E `0` NODI `presa` E' IL FATTO DEL MANDATO**, non una mancanza: *<<nessuna scelta di fisica in questo mandato>>*. ### **Le due radici prese sono `A16` e `A17`, che sono ASSIOMI** — decisioni di Luca del `2026-10-08`, non scelte di oggi.

### ⛔ **E SU `D9` LUCA HA DICHIARATO UNA DIREZIONE** *(<<lo spazio emerge grazie alla mitosi>>)*, ### **e il mandato dice NELLA STESSA FRASE che la direzione NON E' UNA DECISIONE PRESA.** ### ⭐ **Tenere separate quelle due cose e' esattamente il lavoro di `P-ALB`**, ed e' il motivo per cui la direzione sta nel `yaml` ### **come NOTA e non come STATO.**

---

## `4.` I CONTROLLI

| il controllo | l'esito |
|---|---|
| `python csv/indice.py valida` ### **(con `P-ALB` dentro)** | ### **FALLISCE** |
| i segnali *(non bloccano, `A9`)* | `19` |
| `P-ALB` l-albero delle scelte | ### ⛔ **`13`/`14`** *(codice `1`)* |
| `P-T2` il replay, col buco chiuso | ### ✅ **`27`/`27`** |
| l-ARBITRO fra le due vie | ### ✅ **`6`/`6`** |
| i presidi dell-indice, coi vocabolari | ### ✅ **`16`/`16`** |
| il simulatore | `b8c21049`, ASSERITO |

### ⛔ **E IL BRACCIO CHE CONTA DI `P-ALB` E' QUELLO END-TO-END:** provare `controlla()` ### **non prova `valida`**, perche' fra le due c'e' ### **un `import` dentro un `try`** — ed e' ### **il posto dove un presidio si spegne in silenzio.** ### **Misurato: `indice.py valida` ESCE `1`** col nodo marcato `presa` ### **nel file**, e la fonte torna ### **identica al byte.**

### ⭐ **E IL SECONDO CHE CONTA:** se si marca `presa` ### **anche il padre**, il presidio ### **TACE.** ### **Senza quel braccio, il <<deve scattare>> potrebbe passare perche' il presidio RIFIUTA SEMPRE** — e un presidio che rifiuta sempre non prova niente.

---

## `5.` LO STATO DELLE CINQUE FASI, misurato oggi

| | la fase | lo stato |
|---|---|---|
| `F0` | chiusura | ### ⚠ **NON CHIUSA**: restano la ### **terza parte** dell'infrastruttura e le ### **regole di gestione** *(i mandati `4` e `5`)* |
| `F1` | regole di forma | ### **non cominciata.** ### ⭐ **E la regola `(a)` e' GIA' VERA senza essere una regola:** il termine di prova ha ### **esattamente** la forma bilineare, ### **ma il generatore NON LA PRETENDE** — e finche' non la pretende ### **e' un'abitudine, non una regola** |
| `F2` | le decisioni | ### ⛔ **NON PUO' COMINCIARE**: aspetta Luca su `DEC-ALBERO-CINQUE-SENZA-ARGOMENTO` |
| `F3` | le leggi | ### **non cominciata**: la tabella ha `3` leggi, ### **TUTTE `prova: true`** → ### ⛔ **ZERO LEGGI VERE** |
| `F4` | le prime misure | ### **non cominciata** |

### ✅ **E <<ZERO LEGGI VERE>> NON E' UN DIFETTO: e' il punto di partenza DICHIARATO.** L'infrastruttura e' stata costruita su leggi finte ### **proprio perche' una legge finta non puo' far sembrare vero un risultato.**

---

## `6.` CIO' CHE RESTA APERTO — ### **scritto, non taciuto**

| | |
|---|---|
| `DEC-ALBERO-CINQUE-SENZA-ARGOMENTO` | di CINQUE nodi dell-albero il repo non dice l-argomento, e delle decisioni 1, 3, 10 nemmeno |
| `DEC-NASCITA-PSI` | con che stato nasce un nodo? il punto 3 chiede UNA REGOLA DICHIARATA per ogni grandezza |
| `DEC-REGOLA-FORMA` | che CODICE genera una `regola`? il punto 11(a) chiede che crescita e vuoto si generino |
| `DEC-Z47-TRANSIZIONE` | Z47 non si puo- portare ad AGENDA: CHIUSA -> AGENDA e- una transizione VIETATA |
| `Z47` | Z47 VALE SEMPRE ⏳[EPOCA 1 · MISURA] | PROGETTO DI LUNGO PERIODO — NON INIZIATO. GEOMETRIA... |
| `DEC-ALBERO-CINQUE-SENZA-ARGOMENTO` | di `D4`, `D2`, `D11`, `D12`, `T4` il repo ### **non dice l'argomento**, e nemmeno quali siano *<<le decisioni `1`, `3`, `10`>>*. ### ⛔ **Non l'ho inventato** |
| `H-FISICA-FUORI-LISTA` | legge la lista ### **dal DISCO**: una modifica non committata ### **autorizza un commit.** ### **In `F3` conta piu' che in `F0`** |
| le etichette `D2`, `D4`, `D6`, `D11`, `D12`, `D13`, `T4` | ### **esistono nell'indice come voci dell'era `1`**, e `H-INDICE` le risolve ### **su quelle**, in silenzio. ### **E' il motivo per cui l'etichetta e' un CAMPO e non un id** |
| `metadati.jsonl` | resta un ### **`REPERTO` per NECESSITA'** *(ha una via di scrittura e ### **zero** righe di storico)*: il quarto stato `GENERATO` ### **non lo copre** |

---

## `7.` L'ORDINE E' VERIFICABILE DA GIT, non asserito da me

Il task history di questo mandato e' il commit ### **`ccafeca`**, e per il rito del par. `8` e' ### **antenato di ogni commit del lavoro.** ### ⭐ **Quindi <<il ragionamento l'ho scritto prima>> non e' una mia affermazione: e' una proprieta' del grafo dei commit**, e si verifica con `git merge-base --is-ancestor ccafeca HEAD`.

### ✅ **Verificato adesso: `ccafeca` E' antenato di `HEAD`.**

