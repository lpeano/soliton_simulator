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
| **`P1-sexies`** | **Un criterio si collauda su casi a risposta NOTA prima di puntarlo sul codice vero — e la SOGLIA non si calcola dai dati che giudica.** Due casi: **uno che DEVE passare e uno che DEVE fallire**; e il caso nullo *(che cosa varrebbe questo criterio **se non ci fosse niente**?)* fa parte del collaudo. | *decisione di Luca, 2026-09-21* · **`L-SOGLIA` fusa qui il 2026-09-26** | **CINQUE criteri sbagliati in un giorno**, e ogni volta il `FAIL` era **del criterio, non della cura**: `Q6` *(confronto dopo il rilassamento: assenza di CONTRASTO letta come assenza di effetto)* · `Q6` *(«>= 100 volte» una dispersione che a flag spento è **ZERO ESATTO**: `100*0 = 0`, passava con qualunque valore)* · `R3` *(pretendeva `== 0.0` esatto e falliva su **due ulp**)* · `R5` *(contava **25 aperture su 24 passi**: era l'iniezione del test ad aprire il freno)* · `U3` *(confrontava col mio **sviluppo** invece che col valore **esatto**)*. **E le soglie auto-referenziali:** una soglia `2*std(ON)` **si stringe proprio quando la cura funziona**; un criterio con `|x|` **falliva l'85.89 % su rumore puro**. | Due casi sintetici prima del codice vero, **e il caso che DEVE fallire è il più importante** *(quattro dei cinque errori sarebbero stati presi così)*. La soglia si **deriva dal valore sotto ipotesi nulla**, non si sceglie: `\|corr\| < 0.15` era inventato, il nullo della correlazione campionaria è `sigma ~ 1/sqrt(3N)` → `3 sigma = 0.165` su 110 coppie. |
| **`P3`** | **Un numero senza la sua BARRA D'ERRORE, il suo SEME, i suoi FLAG e la sua EPOCA non è un dato.** ① fra bracci si usa la **dispersione FRA SEMI**, mai la `SE` interna a un run, **e per una barra fra semi servono ALMENO 4 SEMI**; ② ogni CSV porta **blob, seme e TUTTI i flag** che distinguono quel braccio; ③ ogni numero porta la sua **EPOCA**, e un numero dell'epoca 1 non è una premessa per l'epoca 2. *(fonde `P3` + `P6` + `par.9-bis`)* | *regole di Luca, 2026-09-15 / 2026-09-21* | ① la pendenza trasversale cambia di **0.0302** da seme a seme **a codice INVARIATO**, contro una `SE` interna di **~0.010**: `Δ = -0.0445 ± 0.0141`, `z = 3.16` su **un** seme sembrava un effetto a 3 sigma, e su tre semi **il segno non era nemmeno concorde**. ② il braccio OFF della prima misura spinoriale aveva **sette** colonne di flag e **non** `TAU_LUCE`, che era **l'unica** variabile del confronto: i due bracci erano distinguibili **solo dal nome del file**. ③ il vuoto nasceva **prima** dei flag, e **otto** grandezze sono state inerti in ogni run di epoca 1, in silenzio. | **Con 2 semi la `std` ha UN grado di libertà** e `t(0.025,1) = 12.706`: l'IC95 è inutilizzabile — con 4, `t(3) = 3.18`. Il CSV si controlla **campo per campo**, non dal log *(il log si perde, il CSV resta)*, e **i dati già scritti non acquisiscono una colonna aggiunta dopo**. L'epoca si cita **col blob e con la configurazione**, che sono **due cose insieme**. |
| **`P4`** | **Prima di misurare se una grandezza cambia, verifica che sia LIBERA di cambiare.** Se `x = f/median(f)` e la mappa è monotona, `median(y)` vale **una costante ESATTA**: su quel punto fisso **non si misura nulla**. | *regola di Luca, 2026-09-15* | `ritmo()`: `median(r) = 1.0 ESATTAMENTE` con **qualunque** orologio — il sigillo `S4` diede `z = 0.00`, che **non** è «nessun effetto» ma **«nessuna misura»**. *(E il caso gemello mostra che la verifica va fatta **sull'espressione effettiva**: `_tau` sembrava avere lo stesso punto fisso e **non ce l'ha**, perché `_dens_rif` è la mediana di un **SOTTOINSIEME**.)* | Prima di confrontare una statistica riassuntiva fra due rami, **si controlla se il codice la ancora a se stessa** — e si guarda l'espressione che gira, non la sua forma ricordata. |
| **`P5`** | **Ogni ramo `else` / fallback / `getattr(..., default)` su un percorso fisico va CONTATO.** Un fallback mai misurato è un comportamento **sconosciuto**; uno che scatta l'80 % delle volte **non è un fallback: è il comportamento principale**. | *regola di Luca, 2026-09-15* | Il ramo `else` di `_tempo_luce_nodo` scattava nel **71.88 %** delle chiamate senza che **nessun** sigillo se ne accorgesse — perché il ramo **non è un errore**: niente `NaN`, niente runaway, nessuna byte-identità violata. E la guardia di `ritmo()` scartava il 4pi nel **95.33 %**. | Un **contatore per sito**, e quattro numeri non uno: **invocazioni, salti, la FORMA al fallimento, e QUANDO** *(`rapporto_guardie(net)`, quindici siti)*. **`20 %` di salti nelle prime 11 invocazioni e `20 %` sparsi danno lo stesso conteggio e sono due diagnosi opposte** (`A8`). |

### Le regole che valgono qui e stanno già altrove — **richiamo, non copia**

- **Una cura non aumenta il numero delle leggi; a parita' di effetto si preferisce togliere un'eccezione** *(era `STANDARD 10`)* → **`CLAUDE.md` par.9-ter**. **Decisione di Luca, 2026-09-26:** e' il criterio con cui si scegle fra **CURE**, non il metodo di una **MISURA** — e con la sua uscita **il posto 2 torna a 10, senza alzare il tetto**.
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

## ✅ IL CONTO TORNA: **DIECI REGOLE PER UN TETTO DI DIECI** *(2026-09-26)*

**Per un giorno sono state ELEVEN, e lo avevo dichiarato invece di arrotondarlo.**
**Ha deciso Luca, e non alzando il tetto:** `STANDARD 10` **esce dal posto 2** e va in
`CLAUDE.md` par.9-ter, *perche' e' il criterio per scegliere fra **CURE**, non un metodo di
misura*. **Il tetto resta 10.**

| | |
|---|--:|
| righe della tabella `STANDARD` al 2026-09-26 sera | **10** |
| tetto | **10** |

**LE DUE CANDIDATE NON SCELTE, e restano scritte perche' la strada scartata informa:**
**`P5` dentro `STANDARD 3`** *(ma `P5` conta **rami** e `STANDARD 3` confronta **istanti**:
fonderle mescola due presidi)* e **`P4` dentro `P1-sexies`** *(la fusione che Luca aveva
**rifiutato** lo stesso giorno)*.

> **E IL MODO IN CUI E' STATA DECISA E' IL PUNTO:** il conto sbagliato era **nella proposta**
> *(annunciava 10 e ne dava 12)*, e a trovarlo e' stato **un controllo che legge l'inventario
> invece di ricopiarlo**. **Un tetto che si alza quando non ci si sta dentro non e' un tetto.**

---

## LE CORSE DELLA FORZA: I CRITERI *(decisione di Luca, `2026-10-23`, dopo `cbcb99c7`)*

> ### **NON e' una riga della tabella `STANDARD`** *(il tetto e' `10`, deciso da Luca il `2026-09-26`)*: ### **e' un criterio di un TIPO di misura** *(un pacchetto in un gradiente di `cs`)*, ### **non un
> metodo di ogni sigillo.**

- ### **LO SPECCHIO SI FISSA PRIMA SUL DIFFERENZIALE:** ### **`(a(+eta) - a(-eta))/2`, con `a(+-eta)` letti da `x(+-eta) - x(0)` dalla stessa partenza, entro il `5%`**; ### **lo specchio GREZZO
  si stampa come LETTURA, non come controllo;** ### **e insieme si riporta SEMPRE la SEMISOMMA `(a(+eta) + a(-eta))/2` confrontata con `a(eta 0)`** *(la correzione
  del guardiano: e' la misura della deriva propria del pacchetto)*.
- ### **Il perche':** ### **in `cbcb99c7` lo specchio grezzo a `eta 1e-3` falliva in `4` casi su `128`** *(fino al `10.74%`)* ### **per la deriva a `eta 0`, sotto il rumore, che pesa su un segnale dieci
  volte piu' piccolo; il differenziale teneva entro lo `0.13%`.** ### **Quei `4` casi restano FALLITI** *(il criterio di quella corsa non e' cambiato a posteriori)*; ### **la causa, misurata: la semisomma coincide con `a(eta 0)`, un'accelerazione propria del
  pacchetto** *(`doc/TASK_HISTORY/2026-10-23_triangoli_forza.md`, sezione `10`)*.

## IL SIGILLO DI GAUGE DEL CAMPO: IL CRITERIO *(decisione di Luca, `2026-10-25`, dopo `64bb2328`)*

> ### **NON e' una riga della tabella `STANDARD`:** ### **e' il criterio di un TIPO di misura** *(l'invarianza di gauge di un campo sugli archi)*.

- ### **`E` SI GIUDICA CONTRO LA STIMA DELL'ARROTONDAMENTO, fissata prima:** ### **`|dE| <= N 6 eps max|A'|/A_p`** *(`N` i tick, `A'` il potenziale trasformato)*; ### **`rho` ed `e B` restano a `1e-12` relativo.**
- ### **Il perche':** ### **in `0b6bfde8` e `64bb2328` lo scarto su `E` andava come `max|A'|`, lineare fino al pavimento `~2e-14`, sempre SOTTO la stima** *(al piu' `0.44` di essa)*: ### **un `1e-12` relativo fisso chiedeva `max|A'| ~ 1e-2`, cioe' di non provare la gauge.** ### **I sigilli `(b)`, `(b1)`, `(b2)` RESTANO FALLITI** *(il criterio di quelle corse non cambia a posteriori)*.

---

## UN NUMERO E' FISICO SOLO SE CONVERGE RAFFINANDO *(decisione di Luca, `2026-10-22`, `19:57`; portata qui il `2026-10-25`)*

> ### **Le parole di Luca** *(`doc/MAPPA_DIPENDENZE.md`, «LA DECISIONE SU `L1`»; la voce [[DECISIONE-L1-NATURA-A-SIMULATORE-B]])*: ### **«LA NATURA E' (A), IL SIMULATORE E' (B)** *(...)* ### **la sua griglia e' un CAMPIONAMENTO GROSSOLANO di quell'automa. Quindi una scala che resta FISSA IN ARCHI raffinando e' un ARTEFATTO; e' fisico solo cio' che CONVERGE raffinando.»**
> ### **NON e' una riga della tabella `STANDARD`** *(il tetto `10`)*: ### **e' il criterio di un TIPO di misura, quella che si legge come fisica.**

- ### **LA REGOLA:** ### **un numero e' fisico solo se CONVERGE raffinando** ### **la griglia** *(il lato, la risoluzione in `k`)*, ### **il passo `s`** *(il limite `s -> 0`, o la dipendenza dichiarata)*, ### **e la taglia** *(il toro, il pacchetto)*.
- ### **IL REFERTO:** ### **ogni referto che usa un numero COME FISICA dichiara la sua convergenza** *(i valori a due o tre raffinamenti, e lo scarto)*, ### **oppure scrive che NON e' misurata.** ### **Un numero senza la sua convergenza e' una lettura dello strumento, non della fisica.**
- ### **IL CASO CHE L'HA RESA CONCRETA** *([[V-MAX-DIREZIONI]], `afba052b`)*: ### **`v_max/s` a `r 1`: `0.598622` sulla griglia `48`, `0.599163` a `96`, `0.599237` a `192`, `0.5992864` con l'ottimizzatore:** ### **il valore «noto» `0.598467`, usato come riferimento in molti referti dei triangoli, era la griglia `48` piu' la scansione su `61` direzioni;** ### **nessuno l'aveva raffinato.**

---

## OGNI MISURA D'ENERGIA USA IL LIBRO DEI CONTI *(il mandato di Luca delle `12:54` del `2026-10-27`; lo strumento `02954bc4`, il referto `4f6a4bd7`)*

> ### **NON e' una riga della tabella `STANDARD`** *(il tetto `10`)*: ### **e' il criterio di un TIPO di misura, quella che conta l'energia** *([[LIBRO-DEI-CONTI]]; `doc/LIBRO_DEI_CONTI.md`)*.

- ### **LA REGOLA:** ### **una misura d'energia per conto o per regione usa `csv/_libro_dei_conti.py`** *(`conti_per_nodo`, `per_regione` con `math.fsum`, `dischi`, `guadagni_A`, `pezzi_B`)*, ### **non una sua copia:** ### **i conti sono UNA definizione** *(i costituenti, la cinetica, il legame dichiarato, il vuoto, `H_tot`, `M`, `V`; lo zero e il suo `2 pi lambda`)*. ### **Il dare e l'avere sul confine si legge con la strada `A`** *(dischi annidati, i tick in entrata e in uscita separati)*; ### **la `B`** *(pezzo per pezzo)* ### **e' una diagnosi del va-e-vieni del passo, non un flusso.**
- ### **IL REFERTO DICHIARA:** ### **il legame attivo** *(`S1` o `S3`)*, ### **`cs`** *(acceso o spento)*, ### **lo zero** *(per NOME: `conv("simm")`; con un numero la convenzione e' quella di oggi, l'errore del `2026-10-27`)*, ### **e l'unita' `N |e_K(0)|`.**
- ### ⚠ **LA CAUTELA, MISURATA** *(il sigillo `(iv)`, `4f6a4bd7`)*: ### **col legame `S1` la deviazione di `H_tot` NON va come `s^2`** *(il rapporto `0.62` fra `s 0.3` e `0.15`, non `4`)*: ### **i residui di `A` non sono solo l'errore del passo, e un flusso di `A` piu' piccolo della deviazione di `H_tot` sullo stesso tempo non si legge come fisica.**

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

## ⚠ I NOMI CHE SONO CAMBIATI IL 2026-09-26, e perché **i reperti non si riscrivono**

| nome di allora | oggi | dove |
|---|---|---|
| `STANDARD 4` | **fusa dentro `STANDARD 3`** | questo documento |
| `STANDARD 10` | **uscita dal posto 2**, per decisione di Luca | `CLAUDE.md` par.9-ter |
| `STANDARD 6` | **assorbita dall'indice** e dal hook `H-INDICE` | `doc/INDICE_ID.tsv` |
| `STANDARD 8` | **è `A12`**, e non si duplica | `doc/ASSIOMI.md` |
| `P6`, `par.9-bis` | **fuse dentro `P3`** | questo documento |
| `L-SOGLIA` | **fusa dentro `P1-sexies`** | questo documento |
| `P3`, `P5`, `P7`, `P8` **del hook** | **`H-P3`, `H-P5`, `H-P7`, `H-P8`** | `CLAUDE.md` par.12 |

**Nei task history, nei referti, nei `json` e nel codice il nome vecchio RESTA**, e si risolve
con l'`alias` in `doc/INDICE_ID.tsv`: **un ID è una chiave, e una chiave non si riscrive a
posteriori.**
