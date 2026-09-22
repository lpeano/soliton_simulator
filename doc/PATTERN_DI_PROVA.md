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
| **1** | **Un processo per braccio.** Mai due bracci di un confronto nello stesso processo. | `b6f3c83`, `96c7f22` | La rete e lo stato delle scene **sopravvivono**: `avvia_test` è una **levetta**, la seconda chiamata *ferma* la scena e il braccio nasce **senza masse** (`n=900` invece di `2480`). | Il braccio si lancia con `subprocess`, e un criterio di **riproducibilità** confronta **due bracci identici** prima di leggere gli altri. |
| **2** | **Firme dei byte, non `max\|Δ\|`.** `sha1` + forma + `dtype` + somme + min/max + non-finiti. | `96c7f22` | `max\|Δ\| = 0` **non vede** due `NaN` nello stesso posto né **`+0.0` contro `-0.0`** — e quest'ultimo caso è collaudato (`K5`). | Il confronto di **identità** usa `sha1` dei byte; i cinque scalari restano per dire **di quanto**, non solo **che**. |
| **3** | **Assenza strutturale ≠ dato mancante.** Un sito che cambia lunghezza **non ha** un delta: si registra come tale, non come `None`. | `40f79dc`, `691eeba` | Due assenze **attese** venivano dichiarate «diverse» e facevano fallire il criterio; e **le lunghezze da sole** non vedono **stessa crescita con valori diversi**. | Per chi concatena: **lunghezze + firma della coda + firma dell'intero** *(la parte conservata **non** è un prefisso: `concatenate([d0[keep], d0new])`)*. **Due `None` non sono un'identità.** |
| **4** | **Snapshot contro snapshot, allo stesso istante.** Mai la rete viva contro un file. | `abc5b49` | I **contatori diagnostici** continuano a salire dopo la scrittura: `_g_kernel_alpha_tot` dava «1 campo diverso» fra **due istanti**, non fra due run *(1523 e 1523, identici)*. | I due termini del confronto sono **due file**, allo **stesso passo**. **E niente `astype(float)` sui complessi**: scarta la parte immaginaria. |
| **5** | **Il controllo dell'involucro, prima di ogni prova.** Lo strumento di lancio *(runpy, monkeypatch, tracce)* deve riprodurre il riferimento **campo per campo a flag invariato**. | `b812f92`, `c901456` | Il sigillo dimostra che **il flag** è chirurgico; **non** che **l'involucro** sia inerte. Sono due affermazioni diverse, e senza la seconda una differenza è attribuibile allo strumento. | Un giro corto a **flag invariato** contro il riferimento: **`0` campi diversi**. **Dimostra anche che le tracce sono di sola lettura.** |

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

| la regola | commit | il difetto che ha scoperto | come si verifica |
|---|---|---|---|
| **Un giro CORTO prima del giro vero.** Prima di un run che costa più di qualche minuto, lo stesso strumento gira **end-to-end** coi parametri minimi. | `438da39`, `b6f3c83` | **I collaudi passano e il run muore lo stesso**: collaudano i **criteri**, non l'**impianto** che li alimenta. Un `UnboundLocalError` ha ucciso un run di 400 s **al passo 1**, con dodici collaudi tutti `OK`. | Lo strumento accetta un modo ridotto *(`--passi=2`, `--prova`)*, ed è stato **eseguito** prima del giro vero. |

## RESPINTE

*(nessuna)*
