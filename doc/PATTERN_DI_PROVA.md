# PATTERN DI PROVA — la lista di controllo di **ogni** sigillo, prova o confronto

> **Si legge PRIMA di scrivere.** Ogni voce nasce da un errore reale e porta il suo commit.
> **Tre sezioni: `STANDARD` · `IN PROVA` · `RESPINTE`.**
>
> **COME SI AGGIUNGE UNA VOCE (regola di Luca, 2026-09-22).** Non promuovo niente a `STANDARD`
> da solo. Un pattern nuovo — nato da un **fallimento di metodo** *oppure* da una **soluzione che
> ha funzionato** — entra in **`IN PROVA`** con quattro cose: **la regola in una riga**, **il
> commit**, **il difetto che previene o ha scoperto**, **come si verifica** che uno strumento lo
> rispetti. **Lo uso subito**, e lo segnalo a Luca con la riga `PROPOSTA IN PROVA: <regola>`.
> **Diventa `STANDARD` solo col sì esplicito di Luca**, anche in blocco al checkpoint; **il
> silenzio lo lascia in prova**. **Se Luca lo respinge** va in **`RESPINTE`** **col motivo**, così
> non si ripropone. **Ammissione solo se:** caso reale col suo commit · una riga · verificabile.
> **Ogni 10 voci `STANDARD`, propongo anche cosa togliere o fondere.**

---

## STANDARD

| # | la regola | commit | il difetto che previene | come si verifica |
|--:|---|---|---|---|
| **1** | **Un processo per braccio.** Mai due bracci di un confronto nello stesso processo. | `b6f3c83`, `96c7f22` | La rete e lo stato delle scene **sopravvivono**: `avvia_test` è una **levetta**, la seconda chiamata *ferma* la scena e il braccio nasce **senza masse** (`n=900` invece di `2480`). | Il braccio si lancia con `subprocess`, e un criterio di **riproducibilità** confronta **due bracci identici** prima di leggere gli altri. **⚠ E SI VERIFICA ANCHE DALLA FORMA DEL CRITERIO** *(`Z145`, 2026-09-24)*: **un criterio di IDENTITÀ fallisce rumorosamente col banco rotto; uno di DIFFERENZA passa più facilmente PROPRIO col banco rotto.** Quindi, ogni volta che un test chiede *«i due DEVONO differire»*, **prima vanno confrontati due bracci identici** — è la stessa riga, letta al contrario. *(Il collaudo `P1-sexies` non lo prende: collauda le FORMULE, non il BANCO.)* |
| **2** | **Firme dei byte, non `max\|Δ\|`.** `sha1` + forma + `dtype` + somme + min/max + non-finiti. | `96c7f22` | `max\|Δ\| = 0` **non vede** due `NaN` nello stesso posto né **`+0.0` contro `-0.0`** — e quest'ultimo caso è collaudato (`K5`). | Il confronto di **identità** usa `sha1` dei byte; i cinque scalari restano per dire **di quanto**, non solo **che**. |
| **3** | **Assenza strutturale ≠ dato mancante.** Un sito che cambia lunghezza **non ha** un delta: si registra come tale, non come `None`. | `40f79dc`, `691eeba` | Due assenze **attese** venivano dichiarate «diverse» e facevano fallire il criterio; e **le lunghezze da sole** non vedono **stessa crescita con valori diversi**. | Per chi concatena: **lunghezze + firma della coda + firma dell'intero** *(la parte conservata **non** è un prefisso: `concatenate([d0[keep], d0new])`)*. **Due `None` non sono un'identità.** |
| **4** | **Snapshot contro snapshot, allo stesso istante.** Mai la rete viva contro un file. | `abc5b49` | I **contatori diagnostici** continuano a salire dopo la scrittura: `_g_kernel_alpha_tot` dava «1 campo diverso» fra **due istanti**, non fra due run *(1523 e 1523, identici)*. | I due termini del confronto sono **due file**, allo **stesso passo**. **E niente `astype(float)` sui complessi**: scarta la parte immaginaria. |
| **5** | **Il controllo dell'involucro, prima di ogni prova.** Lo strumento di lancio *(runpy, monkeypatch, tracce)* deve riprodurre il riferimento **campo per campo a flag invariato**. | `b812f92`, `c901456` | Il sigillo dimostra che **il flag** è chirurgico; **non** che **l'involucro** sia inerte. Sono due affermazioni diverse, e senza la seconda una differenza è attribuibile allo strumento. | Un giro corto a **flag invariato** contro il riferimento: **`0` campi diversi**. **Dimostra anche che le tracce sono di sola lettura.** |
| **6** | **Ogni difetto ACCLARATO si registra SUBITO nella CODA UNICA**, nello stesso commit in cui diventa acclarato. | *decisione di Luca, 2026-09-22* | **Due cure sicure (`SPINTA_LOCALE`, `POZZO_D`) esistevano solo nella relazione e nei mandati: dopo una compattazione si sarebbero PERSE.** | La riga `DIFETTO ACCLARATO: Dxx` nel messaggio, e l'ID esiste nella sezione **DIFETTI APERTI**. Un **sospetto** va in **SOSPETTI** e si promuove solo con la prova. |
| **7** | **Un giro CORTO prima del giro vero.** Prima di un run che costa più di qualche minuto, lo stesso strumento gira **end-to-end** coi parametri minimi. | `438da39`, `53e08f3` · *ammessa da Luca il 2026-09-22* | **I collaudi passano e il run muore lo stesso**: collaudano i **criteri**, non l'**impianto** che li alimenta. ① un `UnboundLocalError` ha ucciso un run di **400 s al passo 1**, con dodici collaudi tutti `OK`; ② il **bilancio di `G4` non chiudeva** *(`8.0e-05`)*, e il giro corto lo ha preso **in 43 s invece che in mezz'ora**, su un run che sarebbe stato **inutilizzabile**. | Lo strumento accetta un modo ridotto *(`--frame=3`, `--passi=2`)*, **ed e' stato ESEGUITO** prima del giro vero. |
| **8** | **Un difetto DIMOSTRATO si cura: misurare non è curare.** Se la cura è **derivabile**, si scrive — le correlazioni si capiscono **dopo**, con un difetto in meno. | *decisione di Luca, 2026-09-22* · `A12` | **Quattro misure chiuse e ZERO cure in un giorno**, con **`D31` dimostrato sulla formula dal mattino** *(`Z113`, `4/4`, scarto `0.0 %`)*: il motore della crescita di `d0` era dimostrato alle undici ed era ancora lì alle nove di sera. | **La frase-spia:** *«prima però bisogna capire se…»*. Se ciò che segue è una **correlazione con un altro difetto** e quello in mano è già dimostrato, **si sta rimandando**. **Una cura alla volta**, per **grandezza dell'effetto misurato**; le misure nuove **in coda**. |

| **9** | **Un'ASSENZA si dichiara solo da una ricerca sull'INTERO FILE o dall'AST.** Mai da una finestra di righe, mai da un `in` sul testo. | *decisione di Luca, 2026-09-24* · `2070aab` | **TRE casi in un giorno, e sbagliano nei DUE versi opposti:** `S10` *(dedotto da un contatore, senza verificare né dove stesse né il valore del flag — **ritirato**)* · `T1` di `E4-LAM` *(`"_lam_attivo" not in sorg` trova le sue occorrenze nei **COMMENTI** → **`FAIL` falso su codice corretto**)* · `D37` *(cercato in una finestra di **28 righe**, la voce stava a `:257` → **chiave duplicata**, codice morto in silenzio)*. | ogni affermazione di assenza porta **il comando che l'ha prodotta**, e quel comando **non ha un intervallo di righe**. Per una domanda su un riferimento di **codice**: **l'AST**, non un `in`. |
### Le regole che valgono qui e stanno già altrove — **richiamo, non copia**

- **Il criterio si collauda su casi a risposta nota, con uno che DEVE fallire** → `CLAUDE.md` `P1-sexies`.
- **Controllo positivo: un sigillo deve dimostrare che il flag FA qualcosa** → `CLAUDE.md` par.10, criterio 2.
- **Le tabelle si generano da codice, mai si ricopiano** → `P1-ter`.
- **Ogni sostituzione di testo si asserisce per sé, mai in blocco** → `P1-quater`.
- **Il fallimento si committa come reperto; la correzione è un commit a sé, PRIMA del nuovo giro** → par.5.
- **Nessun numero a Luca prima del commit** → `P1-bis`, `P1-bis-bis`.
- **Lo strumento non si tocca dopo il giro**: il blob che accompagna un output dev'essere quello che l'ha prodotto → par.5-quinquies.

---

## IN PROVA

*(nessuna)*

> **La riga `10` proposta il 2026-09-24 — *«un collaudo dei criteri non collauda il banco»* — È
> STATA FUSA NELLA RIGA `1`, per decisione di Luca, il giorno stesso.** **Non era una regola
> nuova: era il «come si verifica» della `1`**, che già diceva *«un criterio di riproducibilità
> confronta due bracci identici prima di leggere gli altri»*. **Io non l'avevo applicata e ne
> avevo dedotto che mancasse una regola. Mancava l'applicazione.**
>
> **È il caso da ricordare quando si propone una riga nuova:** `Z145` non è successo perché lo
> standard non c'era — **c'era, con il numero esatto scritto dentro** *(`n=900`; io ho misurato
> `901`)*. **Aggiungere una riga dove ce n'era già una è il modo in cui un elenco di standard
> diventa illeggibile, e un elenco illeggibile non impedisce nulla** *(`A9`)*.
>
> **La regola sull'ASSENZA è stata PROMOSSA a `STANDARD` il 2026-09-24**, col **sì esplicito di Luca** — **riga `9`**. È rimasta `IN PROVA` meno di un'ora, e non perché fosse ovvia: perché aveva **tre casi reali già misurati** nel giorno stesso.
>
> **⚠ E IL SUO LIMITE RESTA QUELLO DICHIARATO QUANDO ERA `IN PROVA`, la promozione non lo cancella:** **non è un presidio** *(`A9`)*. Non impedisce nulla: è un **obbligo di forma verificabile dal destinatario**. **Cosa la renderebbe un presidio:** un controllo che rifiuti, nei referti generati, le parole *«non esiste» / «manca» / «assente»* se non accompagnate da un comando **senza intervallo di righe**. **NON è scritto**, e la regola non va chiamata presidio finché non lo è.

## RESPINTE

*(nessuna)*

---

## `STANDARD 10` — **UNA CURA NON AUMENTA IL NUMERO DELLE LEGGI** *(criterio di Luca, 2026-09-25)*

> ### **«Una cura non aumenta il numero delle leggi; a parità di effetto si preferisce togliere
> ### un'eccezione.»**

**IL CASO CHE L'HA GENERATO, ed è di oggi:** `NODI-1` proponeva di far allacciare i nodi nati in
dinamica **con la stessa regola della semina** *(`R_CONN`)*. Sembrava *togliere* un'eccezione
— «nessun nodo di seconda classe» — e invece **ne aggiungeva una di fisica**: avrebbe
trasformato la mitosi da **creazione di spazio** *(il figlio non accorcia niente: la relazione fra
i genitori passa da `1` a `2` passi)* in **addensamento** *(`~77` scorciatoie per figlio)*.

> **La forma dell'errore:** una regola che rende **uniforme il CODICE** può rendere **non uniforme
> la FISICA**. «Togliere un'eccezione» va misurato **sulle leggi**, non sui rami del programma.

**COME SI APPLICA, operativamente:**

1. **si conta:** quante leggi c'erano prima, quante dopo. Una cura che ne aggiunge una **deve
   dire perché non si poteva togliere niente**;
2. **a parità di effetto misurato, vince la variante con MENO leggi** — e «parità» significa
   *entro la barra d'errore*, non a occhio;
3. **un'eccezione che si toglie va verificata SULLA FISICA:** *che cosa cambia nel sistema*, non
   *quante righe in meno ha il file*.

**⚠ E NON È UN INVITO A NON CURARE:** `A12` resta — *un difetto dimostrato si cura*. Questo dice
**come** si scegle fra due cure, non **se** curare.
