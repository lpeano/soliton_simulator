# PATTERN DI PROVA — il metodo di **ogni** sigillo, prova o confronto

> **Si legge PRIMA di scrivere.** Ogni voce nasce da un errore reale e porta il suo commit.
>
> ### ⚠ **IL TETTO E' DIECI. SE NE ENTRA UNA, NE ESCE UNA.**
> *(`STANDARD 10` applicato alle regole stesse: **una cura non aumenta il numero delle leggi**.)*
> **Oggi le regole sono ELEVEN, non dieci, e lo dico invece di nasconderlo: vedi la nota in coda.**
>
> **COME SI AGGIUNGE UNA VOCE (regola di Luca, 2026-09-22).** Non promuovo niente a `STANDARD`
> da solo. Un pattern nuovo — nato da un **fallimento di metodo** *oppure* da una **soluzione che
> ha funzionato** — entra in **`IN PROVA`** con quattro cose: **la regola in una riga**, **il
> commit**, **il difetto che previene o ha scoperto**, **come si verifica** che uno strumento lo
> rispetti. **Lo uso subito**, e lo segnalo a Luca con la riga `PROPOSTA IN PROVA: <regola>`.
> **Diventa `STANDARD` solo col sì esplicito di Luca**, anche in blocco al checkpoint; **il
> silenzio lo lascia in prova**. **Se Luca lo respinge** va in **`RESPINTE`** **col motivo**, così
> non si ripropone. **Ammissione solo se:** caso reale col suo commit · una riga · verificabile.

---

## LA LISTA DI CONTROLLO DI UN SIGILLO — **il rito, in ordine** *(ex `CLAUDE.md` par.2)*

1. **Flag OFF = byte-identico** al comportamento precedente: `max|A-B| = 0.000e+00`.
   **Se fallisce → STOP.** *(E si legge insieme a `STANDARD 2` e `STANDARD 3`: uno zero può
   essere **mancanza di confronto**.)*
2. **Riduzione al limite:** ogni strato torna a quello sotto nel limite *(allineato / `tau→0` /
   Hebb-off)*. Ridurre al VECCHIO scalare è opzionale; ridurre **allo strato sotto** no.
3. **Purezza pure-read:** i diagnostici non mutano stato né RNG. Snapshot/restore **COMPLETO**
   *(incluso lo stato dell'RNG)* prima e dopo ogni misura.
4. **Norma `|psi| = 1`**, niente `NaN`/`inf`. **Stabilità:** niente runaway; per Hebb `g <= G(rho)`
   **sempre**.
5. **Unitarietà SU(2):** `U_ij^dag U_ij = I` preservata **anche DURANTE** l'evoluzione, non solo
   all'init.
6. **Gate ancorato al git-BLOB** *(un commit può «mentire», un blob no)*. Verifica **dal DISCO**.
7. **Controllo positivo:** un sigillo deve dimostrare che il flag **FA QUALCOSA**. Uno che
   verifica solo la byte-identità a OFF **passerebbe anche su codice morto**.
8. **Statistica:** nessuna conclusione sotto ~2000 passi, **MAI su un solo seme**. Un risultato su
   un seme è baseline interna, **non un fatto** — e per una **barra** vedi `P3`.

---

## STANDARD

| id | la regola | commit | il difetto che previene | come si verifica |
|--:|---|---|---|---|
| **STANDARD 1** | **Un processo per braccio.** Mai due bracci di un confronto nello stesso processo. | `b6f3c83`, `96c7f22` | La rete e lo stato delle scene **sopravvivono**: `avvia_test` è una **levetta**, la seconda chiamata *ferma* la scena e il braccio nasce **senza masse** (`n=900` invece di `2480`). | Il braccio si lancia con `subprocess`, e un criterio di **riproducibilità** confronta **due bracci identici** prima di leggere gli altri. **⚠ E SI VERIFICA ANCHE DALLA FORMA DEL CRITERIO** *(`Z145`, 2026-09-24)*: **un criterio di IDENTITÀ fallisce rumorosamente col banco rotto; uno di DIFFERENZA passa più facilmente PROPRIO col banco rotto.** Quindi, ogni volta che un test chiede *«i due DEVONO differire»*, **prima vanno confrontati due bracci identici** — è la stessa riga, letta al contrario. *(Il collaudo `P1-sexies` non lo prende: collauda le FORMULE, non il BANCO.)* |
| **STANDARD 2** | **Firme dei byte, non `max\|Δ\|`.** `sha1` + forma + `dtype` + somme + min/max + non-finiti. | `96c7f22` | `max\|Δ\| = 0` **non vede** due `NaN` nello stesso posto né **`+0.0` contro `-0.0`** — e quest'ultimo caso è collaudato (`K5`). **E può voler dire «NESSUN CONFRONTO»:** se due run divergono al punto di cambiare il **numero di nodi**, nessun array ha più la stessa forma e il massimo di un insieme vuoto è `0` *(misurato: 3209 nodi contro 3073, 32 forme su 32 divergenti)*. | Il confronto di **identità** usa `sha1` dei byte; i cinque scalari restano per dire **di quanto**, non solo **che**. **Si guarda SEMPRE prima la riga delle forme / del conteggio nodi.** |
| **STANDARD 3** | **Si confronta lo stesso istante, e ciò che NON C'È si registra come assente.** ① **Snapshot contro snapshot, allo stesso passo** — mai la rete viva contro un file. ② **Assenza strutturale ≠ dato mancante:** un sito che cambia lunghezza **non ha** un delta, e si registra come tale, non come `None`. *(fonde la vecchia `STANDARD 4` nella `3`: entrambe dicono **che cosa si confronta con che cosa**)* | `40f79dc`, `691eeba`, `abc5b49` | ① I **contatori diagnostici** continuano a salire dopo la scrittura: `_g_kernel_alpha_tot` dava «1 campo diverso» fra **due istanti**, non fra due run *(1523 e 1523, identici)*. ② Due assenze **attese** venivano dichiarate «diverse» e facevano fallire il criterio; e **le lunghezze da sole** non vedono **stessa crescita con valori diversi**. | I due termini sono **due file**, allo **stesso passo**, e **niente `astype(float)` sui complessi** *(scarta la parte immaginaria)*. Per chi concatena: **lunghezze + firma della coda + firma dell'intero** *(la parte conservata **non** è un prefisso)*. **Due `None` non sono un'identità.** |
| **STANDARD 5** | **Il controllo dell'involucro, prima di ogni prova.** Lo strumento di lancio *(runpy, monkeypatch, tracce)* deve riprodurre il riferimento **campo per campo a flag invariato**. | `b812f92`, `c901456` | Il sigillo dimostra che **il flag** è chirurgico; **non** che **l'involucro** sia inerte. Sono due affermazioni diverse, e senza la seconda una differenza è attribuibile allo strumento. | Un giro corto a **flag invariato** contro il riferimento: **`0` campi diversi**. **Dimostra anche che le tracce sono di sola lettura.** |
| **STANDARD 7** | **Un giro CORTO prima del giro vero.** Prima di un run che costa più di qualche minuto, lo stesso strumento gira **end-to-end** coi parametri minimi. | `438da39`, `53e08f3` · *ammessa da Luca il 2026-09-22* | **I collaudi passano e il run muore lo stesso**: collaudano i **criteri**, non l'**impianto** che li alimenta. ① un `UnboundLocalError` ha ucciso un run di **400 s al passo 1**, con dodici collaudi tutti `OK`; ② il **bilancio di `G4` non chiudeva** *(`8.0e-05`)*, e il giro corto lo ha preso **in 43 s invece che in mezz'ora**. | Lo strumento accetta un modo ridotto *(`--frame=3`, `--passi=2`)*, **ed è stato ESEGUITO** prima del giro vero. |
| **STANDARD 9** | **Un'ASSENZA si dichiara solo da una ricerca sull'INTERO FILE, dall'AST o da `git log`.** Mai da una finestra di righe, mai da un `in` sul testo. | *decisione di Luca, 2026-09-24* · `2070aab` · **ampliata il 2026-09-26** | **TRE casi in un giorno, e sbagliano nei DUE versi opposti:** `S10` *(dedotto da un contatore — **ritirato**)* · `T1` di `E4-LAM` *(`"_lam_attivo" not in sorg` trova le sue occorrenze nei **COMMENTI** → **`FAIL` falso su codice corretto**)* · `D37` *(cercato in una finestra di **28 righe**, la voce stava a `:257` → **chiave duplicata**, codice morto in silenzio)*. **E il quarto è del `git log`:** una smentita può vivere **in un messaggio di commit** e non nei file — **misurato su `D09`**. | Ogni affermazione di assenza porta **il comando che l'ha prodotta**, e quel comando **non ha un intervallo di righe**. Per una domanda su un riferimento di **codice**: **l'AST**, non un `in`. **`git log` è il repo**, e va cercato anche lui. |
| **STANDARD 10** | **Una cura non aumenta il numero delle leggi**; a parità di effetto si preferisce **togliere un'eccezione**. *(la sezione lunga è in fondo a questo documento)* | *criterio di Luca, 2026-09-25* | `NODI-1` sembrava *togliere* un'eccezione e ne **aggiungeva una di fisica**: avrebbe trasformato la mitosi da **creazione di spazio** in **addensamento** *(~77 scorciatoie per figlio)*. | ① si **conta** quante leggi prima e quante dopo; ② a parità **entro la barra d'errore**, vince la variante con **meno leggi**; ③ l'eccezione tolta si verifica **SULLA FISICA**, non sulle righe in meno. |
| **`P1-sexies`** | **Un criterio si collauda su casi a risposta NOTA prima di puntarlo sul codice vero — e la SOGLIA non si calcola dai dati che giudica.** Due casi: **uno che DEVE passare e uno che DEVE fallire**; e il caso nullo *(che cosa varrebbe questo criterio **se non ci fosse niente**?)* fa parte del collaudo. | *decisione di Luca, 2026-09-21* · **`L-SOGLIA` fusa qui il 2026-09-26** | **CINQUE criteri sbagliati in un giorno**, e ogni volta il `FAIL` era **del criterio, non della cura**: `Q6` *(confronto dopo il rilassamento: assenza di CONTRASTO letta come assenza di effetto)* · `Q6` *(«>= 100 volte» una dispersione che a flag spento è **ZERO ESATTO**: `100*0 = 0`, passava con qualunque valore)* · `R3` *(pretendeva `== 0.0` esatto e falliva su **due ulp**)* · `R5` *(contava **25 aperture su 24 passi**: era l'iniezione del test ad aprire il freno)* · `U3` *(confrontava col mio **sviluppo** invece che col valore **esatto**)*. **E le soglie auto-referenziali:** una soglia `2*std(ON)` **si stringe proprio quando la cura funziona**; un criterio con `|x|` **falliva l'85.89 % su rumore puro**. | Due casi sintetici prima del codice vero, **e il caso che DEVE fallire è il più importante** *(quattro dei cinque errori sarebbero stati presi così)*. La soglia si **deriva dal valore sotto ipotesi nulla**, non si sceglie: `\|corr\| < 0.15` era inventato, il nullo della correlazione campionaria è `sigma ~ 1/sqrt(3N)` → `3 sigma = 0.165` su 110 coppie. |
| **`P3`** | **Un numero senza la sua BARRA D'ERRORE, il suo SEME, i suoi FLAG e la sua EPOCA non è un dato.** ① fra bracci si usa la **dispersione FRA SEMI**, mai la `SE` interna a un run, **e per una barra fra semi servono ALMENO 4 SEMI**; ② ogni CSV porta **blob, seme e TUTTI i flag** che distinguono quel braccio; ③ ogni numero porta la sua **EPOCA**, e un numero dell'epoca 1 non è una premessa per l'epoca 2. *(fonde `P3` + `P6` + `par.9-bis`)* | *regole di Luca, 2026-09-15 / 2026-09-21* | ① la pendenza trasversale cambia di **0.0302** da seme a seme **a codice INVARIATO**, contro una `SE` interna di **~0.010**: `Δ = -0.0445 ± 0.0141`, `z = 3.16` su **un** seme sembrava un effetto a 3 sigma, e su tre semi **il segno non era nemmeno concorde**. ② il braccio OFF della prima misura spinoriale aveva **sette** colonne di flag e **non** `TAU_LUCE`, che era **l'unica** variabile del confronto: i due bracci erano distinguibili **solo dal nome del file**. ③ il vuoto nasceva **prima** dei flag, e **otto** grandezze sono state inerti in ogni run di epoca 1, in silenzio. | **Con 2 semi la `std` ha UN grado di libertà** e `t(0.025,1) = 12.706`: l'IC95 è inutilizzabile — con 4, `t(3) = 3.18`. Il CSV si controlla **campo per campo**, non dal log *(il log si perde, il CSV resta)*, e **i dati già scritti non acquisiscono una colonna aggiunta dopo**. L'epoca si cita **col blob e con la configurazione**, che sono **due cose insieme**. |
| **`P4`** | **Prima di misurare se una grandezza cambia, verifica che sia LIBERA di cambiare.** Se `x = f/median(f)` e la mappa è monotona, `median(y)` vale **una costante ESATTA**: su quel punto fisso **non si misura nulla**. | *regola di Luca, 2026-09-15* | `ritmo()`: `median(r) = 1.0 ESATTAMENTE` con **qualunque** orologio — il sigillo `S4` diede `z = 0.00`, che **non** è «nessun effetto» ma **«nessuna misura»**. *(E il caso gemello mostra che la verifica va fatta **sull'espressione effettiva**: `_tau` sembrava avere lo stesso punto fisso e **non ce l'ha**, perché `_dens_rif` è la mediana di un **SOTTOINSIEME**.)* | Prima di confrontare una statistica riassuntiva fra due rami, **si controlla se il codice la ancora a se stessa** — e si guarda l'espressione che gira, non la sua forma ricordata. |
| **`P5`** | **Ogni ramo `else` / fallback / `getattr(..., default)` su un percorso fisico va CONTATO.** Un fallback mai misurato è un comportamento **sconosciuto**; uno che scatta l'80 % delle volte **non è un fallback: è il comportamento principale**. | *regola di Luca, 2026-09-15* | Il ramo `else` di `_tempo_luce_nodo` scattava nel **71.88 %** delle chiamate senza che **nessun** sigillo se ne accorgesse — perché il ramo **non è un errore**: niente `NaN`, niente runaway, nessuna byte-identità violata. E la guardia di `ritmo()` scartava il 4pi nel **95.33 %**. | Un **contatore per sito**, e quattro numeri non uno: **invocazioni, salti, la FORMA al fallimento, e QUANDO** *(`rapporto_guardie(net)`, quindici siti)*. **`20 %` di salti nelle prime 11 invocazioni e `20 %` sparsi danno lo stesso conteggio e sono due diagnosi opposte** (`A8`). |

### Le regole che valgono qui e stanno già altrove — **richiamo, non copia**

- **Un difetto DIMOSTRATO si cura: misurare non è curare** → `doc/ASSIOMI.md` **`A12`**
  *(era `STANDARD 8`, ed era `A12` parola per parola: **una regola in due posti è una regola che si
  può aggiornare a metà**)*.
- **Zero manopole: la LEGGE, non il numero** → `doc/ASSIOMI.md` **`A1`**.
- **Un limite è una legge, non una toppa** → `doc/ASSIOMI.md` **`A11`**.
- **Due grandezze si confrontano solo se sono confrontabili** → `doc/ASSIOMI.md` **`A3c`**.
- **Ogni difetto acclarato si registra SUBITO** *(era `STANDARD 6`)* → **non è più una regola di
  metodo: è un fatto meccanico.** Un difetto nuovo **È** una riga di `doc/INDICE_ID.tsv`, e il hook
  **`H-INDICE`** lo impedisce.
- **Ogni numero esce da uno script; ogni sostituzione di testo si asserisce per sé** →
  `CLAUDE.md` par.11 (**`L-NUMERI`**, **`P1-quater`**).
- **Il fallimento si committa come reperto; la correzione è un commit a sé, PRIMA del nuovo giro**
  → `CLAUDE.md` par.5.
- **Nessun numero a Luca prima del commit** → `CLAUDE.md` par.4 (`PUSHATO: <hash>`).
- **Lo strumento non si tocca dopo il giro**: il blob che accompagna un output dev'essere quello
  che l'ha prodotto → `CLAUDE.md` par.7.
- **I FATTI già verificati su una funzione** → `doc/FATTI_dal_codice.md`, **prima di toccarla**.

---

## ⚠ IL CONTO NON TORNA: **ELEVEN REGOLE PER UN TETTO DI DIECI** *(2026-09-26)*

**Lo dico invece di arrotondarlo.** La proposta approvata prevedeva **tre** fusioni e annunciava
**10**; con le modifiche di Luca *(`P4` resta sola, `L-SOGLIA` va dentro `P1-sexies`)* il conto
misurato è **11**, e **anche la proposta originale ne dava 12, non 10: quel «10» era sbagliato in
aritmetica.** *(16 righe − 2 per `P3`+`P6`+`par.9-bis` − 1 per la coppia di `L-SOGLIA` − 1 per
`STANDARD 3`+`4` = 12, e `par.2` non è una riga ma **la lista di controllo**, quindi 11.)*

> **NON ho scelto io l'undicesima da fondere: sarebbe decidere al posto di Luca**, e la fusione
> che lui ha **esplicitamente rifiutato** era proprio una di queste. **La decisione è in coda.**

**Le tre candidate, con quello che si perderebbe:**

| candidata | a favore | contro |
|---|---|---|
| **`STANDARD 10` → `CLAUDE.md` par.11** | è un **criterio di scelta fra due cure**, non il metodo di una misura | è il criterio con cui questo stesso riordino è stato giudicato |
| **`P5` dentro `STANDARD 3`** | entrambe dicono *«ciò che non si vede va registrato»* | `P5` conta **rami**, `STANDARD 3` confronta **istanti**: fonderle mescola due presidi |
| **`P4` dentro `P1-sexies`** | è la fusione che la proposta chiedeva | **Luca l'ha rifiutata il 2026-09-26** |

---

## IN PROVA

*(nessuna)*

> **La riga `10` proposta il 2026-09-24 — *«un collaudo dei criteri non collauda il banco»* — È
> STATA FUSA NELLA RIGA `1`, per decisione di Luca, il giorno stesso.** **Non era una regola
> nuova: era il «come si verifica» della `1`.** **Io non l'avevo applicata e ne avevo dedotto che
> mancasse una regola. Mancava l'applicazione.**
>
> **È il caso da ricordare quando si propone una riga nuova:** `Z145` non è successo perché lo
> standard non c'era — **c'era, con il numero esatto scritto dentro** *(`n=900`; io ho misurato
> `901`)*. **Aggiungere una riga dove ce n'era già una è il modo in cui un elenco di standard
> diventa illeggibile, e un elenco illeggibile non impedisce nulla** *(`A9`)*.
>
> **La regola sull'ASSENZA è stata PROMOSSA a `STANDARD` il 2026-09-24**, col **sì esplicito di
> Luca** — **riga `9`**. È rimasta `IN PROVA` meno di un'ora, e non perché fosse ovvia: perché
> aveva **tre casi reali già misurati** nel giorno stesso.
>
> **⚠ E IL SUO LIMITE RESTA QUELLO DICHIARATO QUANDO ERA `IN PROVA`, la promozione non lo
> cancella:** **non è un presidio** *(`A9`)*. Non impedisce nulla: è un **obbligo di forma
> verificabile dal destinatario**. **Cosa la renderebbe un presidio:** un controllo che rifiuti,
> nei referti generati, le parole *«non esiste» / «manca» / «assente»* se non accompagnate da un
> comando **senza intervallo di righe**. **NON è scritto**, e la regola non va chiamata presidio
> finché non lo è.

## RESPINTE

*(nessuna)*

---

## `STANDARD 10` — **UNA CURA NON AUMENTA IL NUMERO DELLE LEGGI** *(criterio di Luca, 2026-09-25)*

> ### **«Una cura non aumenta il numero delle leggi; a parità di effetto si preferisce togliere
> ### un'eccezione.»**

**IL CASO CHE L'HA GENERATO:** `NODI-1` proponeva di far allacciare i nodi nati in
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
**come** si sceglie fra due cure, non **se** curare.

---

## ⚠ I NOMI CHE SONO CAMBIATI IL 2026-09-26, e perché **i reperti non si riscrivono**

| nome di allora | oggi | dove |
|---|---|---|
| `STANDARD 4` | **fusa dentro `STANDARD 3`** | questo documento |
| `STANDARD 6` | **assorbita dall'indice** e dal hook `H-INDICE` | `doc/INDICE_ID.tsv` |
| `STANDARD 8` | **è `A12`**, e non si duplica | `doc/ASSIOMI.md` |
| `P6`, `par.9-bis` | **fuse dentro `P3`** | questo documento |
| `L-SOGLIA` | **fusa dentro `P1-sexies`** | questo documento |
| `P3`, `P5`, `P7`, `P8` **del hook** | **`H-P3`, `H-P5`, `H-P7`, `H-P8`** | `CLAUDE.md` par.12 |

**Nei task history, nei referti, nei `json` e nel codice il nome vecchio RESTA**, e si risolve
con l'`alias` in `doc/INDICE_ID.tsv`: **un ID è una chiave, e una chiave non si riscrive a
posteriori.**
