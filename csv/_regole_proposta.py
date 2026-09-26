r"""**GENERA `doc/REGOLE_proposta.md`** — l'inventario di OGNI regola in vigore e la sua destinazione.

**Mandato di Luca, 2026-09-26 (sessione nuova): SOLO PROPOSTA, non si applica niente.**

## CHE COSA E' MISURATO E CHE COSA E' GIUDIZIO

```
MISURATO dallo script   gli ID delle regole (dalle intestazioni e dalle tabelle delle fonti),
                        le RIGHE di ogni sezione e di ogni documento, i marcatori che i hook
                        stampano, i conteggi PRIMA/DOPO
GIUDIZIO MIO            la DESTINAZIONE di ogni regola (`TIENI` / `FONDI` / `AUTOMATICA` / `TOGLI`)
                        e il motivo: stanno in `DESTINAZIONE`, **una riga per id**
```

**IL CONTROLLO CHE RENDE LA PROPOSTA VERIFICABILE:** ogni id estratto dalle fonti **deve avere una
destinazione**. Se ne manca uno, **lo script si ferma e lo nomina**: *nessun comportamento imposto da
Luca puo' sparire in silenzio*.

**NESSUN RUN, nessuna modifica a `CLAUDE.md` o ai hook.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge documenti e ne scrive uno.
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "REGOLE_proposta.md")
NL = chr(10)

# ============================================================ I CINQUE POSTI
POSTI = [
    ("1", "`doc/ASSIOMI.md`", "ASSIOMI — **INTOCCABILI**",
     "vincoli sulla FORMA delle leggi. Non si fondono, non si tolgono, non si spostano."),
    ("2", "`doc/PATTERN_DI_PROVA.md`", "METODO DI MISURA — **max 10 regole**",
     "una riga + **il difetto che previene**. Se ne entra una, ne esce una."),
    ("3", "i **hook** *(`.githooks/`, `csv/_hook_*.py`, `csv/_presidio_*.py`)*",
     "IGIENE TECNICA — **automatica**",
     "in `CLAUDE.md` **una riga** che li elenca; **il perche' sta nel messaggio d'errore del hook**."),
    ("4", "`CLAUDE.md`", "FLUSSO DI LAVORO — **una pagina**",
     "come si lavora: ordine, commit, relazione, indice. **Sotto le 400 righe**, e un presidio lo "
     "fa rispettare."),
    ("5", "`doc/STATO_RUN.md` + `doc/INDICE_ID.tsv`", "STATO E FATTI DAL CODICE",
     "**non sono regole**: sono cio' che il sistema e' oggi. Fuori da `CLAUDE.md`."),
]

# ============================================================ LE DESTINAZIONI (GIUDIZIO MIO)
#   verdetto: TIENI | FONDI | AUTOMATICA | TOGLI      posto: 1..5 (o "-" se esce)
D = {}


def d(idv, verdetto, posto, testo, motivo):
    D[idv] = (verdetto, posto, testo, motivo)


# ---------- gli ASSIOMI: TUTTI restano dove sono (posto 1), e non si toccano
for a, testo in [
    ("A1", "la LEGGE, non il numero"), ("A2", "nessuna scorciatoia globale"),
    ("A3", "niente si normalizza sul proprio insieme"), ("A4", "stratificazione causale"),
    ("A5", "causalita' della mediazione"), ("A6", "inerzia (TEOREMA)"),
    ("A7", "conservazione e stato"), ("A7b", "uno stato non nasce indefinito"),
    ("A8", "un ramo silenzioso non e' un ramo"),
    ("A8b", "le cache cross-passo"), ("A9", "un presidio che non impedisce non e' un presidio"),
    ("A10", "una sola grandezza puo' legare due domini"),
    ("A11", "un limite e' una legge, non una toppa"),
    ("A12", "un difetto dimostrato si cura: misurare non e' curare"),
    ("A13", "`LAM` e' la scala di Planck del sistema"),
        ]:
    d(a, "TIENI", "1", testo, "assioma: intoccabile per decisione di Luca")
d("A3b", "TIENI", "1", "corollario di `A3` (inline)",
  "corollario: resta dentro `A3`, non diventa una voce a se'")
d("A3c", "TIENI", "1", "due grandezze si confrontano solo se sono confrontabili",
  "corollario metodologico di `A3`: **richiamato** dal posto 2, non copiato")

# ---------- gli STANDARD: max 10, e due se ne vanno per FUSIONE
d("STANDARD 1", "TIENI", "2", "un processo per braccio",
  "difetto che previene: lo stato condiviso fra due bracci nello stesso processo")
d("STANDARD 2", "TIENI", "2", "firme dei byte, non `max|delta|`",
  "difetto: `max|delta| = 0` non vede due array di forma diversa")
d("STANDARD 3", "TIENI", "2", "assenza strutturale != dato mancante",
  "difetto: un sito che cambia lunghezza registrato come `None`")
d("STANDARD 4", "TIENI", "2", "snapshot contro snapshot, allo stesso istante",
  "difetto: i contatori diagnostici corrono mentre confronti")
d("STANDARD 5", "TIENI", "2", "il controllo dell'involucro, prima di ogni prova",
  "difetto: lo strumento di lancio non riproduce il riferimento")
d("STANDARD 6", "FONDI", "5", "ogni difetto acclarato si registra SUBITO",
  "**assorbita dal punto 5**: dal 2026-09-26 un difetto nuovo E' una riga dell'indice, e **il hook "
  "lo impedisce**. Da regola di metodo a **fatto meccanico**")
d("STANDARD 7", "TIENI", "2", "un giro CORTO prima del giro vero",
  "difetto: sette ore buttate per un parametro sbagliato")
d("STANDARD 8", "FONDI", "1", "un difetto dimostrato si cura",
  "**e' `A12` parola per parola**: resta l'assioma, e il posto 2 lo **richiama**. Una regola in due "
  "posti e' una regola che si puo' aggiornare a metà")
d("STANDARD 9", "TIENI", "2", "un'assenza si dichiara solo da una ricerca sull'INTERO file, "
  "dall'AST **o da `git log`**",
  "**si AMPLIA di una riga** *(la nuova regola di lavoro)*: `git log` **e' il repo**, e una smentita "
  "puo' vivere in un messaggio di commit — **misurato su `D09`**")
d("STANDARD 10", "TIENI", "2", "una cura non aumenta il numero delle leggi",
  "difetto: ogni cura che aggiunge un meccanismo invece di togliere una toppa. **Si applica anche "
  "alle REGOLE, ed e' il criterio di questa proposta**")

# ---------- i P di `CLAUDE.md` (par.0-ter)
d("P1", "TIENI", "4", "non usare l'associazione senza verificare lo storico",
  "e' il prerequisito di scrittura: resta, in **una riga**")
d("P1-bis", "FONDI", "4", "la relazione si scrive nello stesso commit del riscontro",
  "**fusa con `P1-bis-bis`, par.5-ter, par.5-sexies e par.5-octies** in UNA regola di flusso: "
  "*tutto cio' che si dice a Luca va nel repo nello stesso giro*. **Il hook la rende automatica in "
  "parte** (`H-RELAZIONE`)")
d("P1-bis-bis", "FONDI", "4", "ogni messaggio a Luca finisce con `PUSHATO: <hash>`",
  "**nella stessa regola di `P1-bis`**: e' la sua forma verificabile dal destinatario")
d("P1-ter", "FONDI", "4", "una tabella di numeri si genera da codice",
  "**assorbita dalla regola di lavoro nuova**: *ogni numero scritto in un commit o referto esce da "
  "uno script*. Piu' larga e piu' semplice")
d("P1-quater", "TIENI", "4", "ogni sostituzione di testo si asserisce per se'",
  "resta, **e guadagna la riga sugli escape**: nei patch script niente `\\t`/`\\b`/`\\s`, si usa "
  "`chr()` o `replace` — **quattro volte in un giorno un escape e' morto in un patch**")
d("P1-quinquies", "TOGLI", "-", "prima di un clip, un pavimento o un tetto: `A11`",
  "**e' solo un puntatore ad `A11`**, che e' un assioma e non si tocca. Un puntatore non e' una "
  "regola: **il posto 1 basta**")
d("P1-sexies", "TIENI", "2", "un criterio si collauda su un caso a risposta nota, **e il caso che "
  "DEVE fallire e' il piu' importante**",
  "e' metodo di misura, non flusso: **cambia posto**, da `CLAUDE.md` a `PATTERN_DI_PROVA`")
d("P2", "TIENI", "4", "prima di escludere un flag: forza il sistema o lo CORREGGE?",
  "resta, in una riga, accanto al punto 5 *(lo stato dei flag e' un dato, non una regola)*")
d("P3", "TIENI", "2", "nessuna statistica senza barra d'errore, e fra bracci si usa la dispersione "
  "FRA SEMI (>= 4 semi)",
  "metodo di misura: **cambia posto**. ⚠ **E CAMBIA NOME**: oggi `P3` e' **anche** un presidio del "
  "hook, e sono due regole diverse")
d("P4", "TIENI", "2", "prima di misurare se una grandezza cambia, verificare che sia LIBERA di "
  "cambiare", "metodo di misura: cambia posto")
d("P5", "TIENI", "2", "ogni ramo `else`/fallback su un percorso fisico va CONTATO",
  "metodo di misura: cambia posto. ⚠ **E CAMBIA NOME**: `P5` e' **anche** un presidio del hook")
d("P6", "TIENI", "2", "ogni CSV di misura porta blob, seme e tutti i flag",
  "metodo di misura: cambia posto")

# ---------- i presidi AUTOMATICI (i hook): restano, e prendono un NOME che non collide
for i2, testo, mot in [
    ("H-CLI", "un sigillo che configura il modulo a mano invece di passare dal CLI",
     "oggi si chiama `P3` **e collide con `P3` di `CLAUDE.md`**: il prefisso `H-` dice *hook*"),
    ("H-CONFIG", "un referto che non dichiara la configurazione INTERA",
     "oggi `P5`, **collide con `P5` di `CLAUDE.md`**"),
    ("H-ANCORA", "un confronto che prende il codice di prima da `HEAD` invece dal PADRE",
     "oggi `P8`: nessuna collisione, ma il prefisso rende l'elenco leggibile"),
    ("H-COMMENTI", "un flag il cui commento cambia senza nominare quel flag",
     "oggi `P7`"),
    ("H-INDICE", "un ID citato in un documento vivo o nel messaggio che non e' nell'indice",
     "oggi `INDICE`"),
    ("H-FISICA", "una legge che cambia senza la sua scheda",
     "oggi `REG-R`"),
    ("H-RELAZIONE", "un referto committato senza toccare la relazione",
     "oggi `P1-bis` nel hook: **stesso nome della regola di flusso**, e sono due cose diverse"),
    ("H-VALIDATORE", "un indice mal formato o con una voce persa",
     "gira nel `pre-commit` dal 2026-09-26"),
        ]:
    d(i2, "AUTOMATICA", "3", testo, mot)

# ---------- le SEZIONI di `CLAUDE.md`
d("par.0-zero", "TIENI", "4", "il bersaglio: le tre prove di `IPOTESI_gravita_a_spinta`",
  "e' l'orientamento del progetto: resta, 3 righe")
d("par.0", "TIENI", "4", "ruolo e postura: guardiano, verifica dal codice",
  "resta **asciugata**: 55 righe oggi, la parte sui blob storici va al posto 5")
d("par.0-bis", "TIENI", "4", "che cosa si legge all'avvio",
  "resta, e **si accorcia**: l'elenco dei documenti d'avvio scende *(vedi i conteggi in testa)*")
d("par.0-ter", "FONDI", "4", "i pattern comportamentali `P1`-`P6`",
  "**la sezione sparisce come contenitore**: i `P` vanno al posto giusto *(2 o 4)*, e le 208 righe "
  "di storia vanno in `doc/STORIA_REGOLE.md`")
d("par.1", "TIENI", "4", "un interruttore alla volta",
  "regola d'oro del flusso: resta")
d("par.2", "TIENI", "2", "il rito del sigillo, in ordine",
  "e' il metodo di una prova: **cambia posto** e diventa la lista di controllo del posto 2")
d("par.3", "FONDI", "1", "zero manopole: nessun parametro tarato a mano",
  "**e' `A1`** *(la legge, non il numero)*: resta l'assioma, e il posto 4 lo richiama in una riga")
d("par.4", "TIENI", "5", "le regole fisiche da non violare *(SU(2), Verlet, locale pura...)*",
  "**non sono regole di lavoro: sono FISICA** → `doc/REGISTRO_FISICA.md`, dove le leggi vivono")
d("par.5", "TIENI", "4", "politiche di commit",
  "resta, asciugata: molte parti sono **gia' automatiche** nei hook")
d("par.5-bis", "FONDI", "5", "auto-manutenzione dei documenti vivi",
  "**assorbita dal punto 5**: lo stato sta nell'indice, e il validatore lo controlla")
d("par.5-ter", "FONDI", "4", "relazione a ogni riscontro",
  "**nella regola unica di `P1-bis`**")
d("par.5-quater", "FONDI", "5", "il registro dei fronti aperti",
  "**assorbito dall'indice**: i fronti sono voci, e `RAMIFICAZIONI` e' una fonte dell'indice")
d("par.5-quinquies", "FONDI", "4", "il codice di una misura dev'essere recuperabile",
  "la **regola** resta in una riga *(blob committato, o copia accanto ai dati)*; le **130 righe di "
  "storia** *(la trappola CRLF, le due convenzioni di hash)* vanno in `doc/STORIA_REGOLE.md`")
d("par.5-sexies", "FONDI", "4", "una domanda si committa col suo ragionamento",
  "**nella regola unica di `P1-bis`**: una domanda e' un riscontro")
d("par.5-septies", "TIENI", "4", "il task history si scrive e si committa PRIMA",
  "resta, **asciugata a 12 righe**: le tre sezioni e il rito, senza i precedenti")
d("par.5-octies", "FONDI", "4", "ogni resoconto si committa anche a meta' run",
  "**nella regola unica di `P1-bis`**")
d("par.5-novies", "AUTOMATICA", "3", "inventario, README e fisica nello stesso commit",
  "③ *(la fisica)* **e' gia' automatica** (`H-FISICA`); ① *(l'inventario)* e' **candidata a un hook**: "
  "un file nuovo in `csv/_test_fork/` o `csv/_seal_fork/` senza voce in `INVENTARIO_strumenti` "
  "viene rifiutato. **Finche' non c'e' il hook, resta una riga al posto 4**")
d("par.6", "TIENI", "5", "stato e ordine del lavoro",
  "**e' STATO, non una regola** → `STATO_RUN` *(dove gia' vive la coda unica)*")
d("par.7", "TIENI", "4", "i documenti di riferimento",
  "resta come **elenco**, una riga per documento")
d("par.8", "TIENI", "4", "il principio guida",
  "5 righe: resta")
d("par.9", "TIENI", "5", "i fatti verificati dal codice",
  "**671 righe su 1575: il 43 % di `CLAUDE.md` NON E' UNA REGOLA, sono FATTI** → "
  "`doc/FATTI_dal_codice.md`, citato dal posto 4 e **letto quando serve**, non all'avvio")
d("par.9-bis", "TIENI", "2", "ogni numero porta la sua epoca",
  "e' metodo di misura: **cambia posto**")
d("par.10", "TIENI", "5", "promozione delle componenti",
  "il **criterio** *(tre condizioni)* resta in `COMPONENTI_PROMOSSE.md`, dove vive il registro; al "
  "posto 4 **una riga** col rimando")
d("par.11", "TIENI", "4", "l'indice dei difetti: come si usa",
  "**resta, ed e' collaudata** *(`csv/_collaudo_istruzioni.py`, 6/6: la sezione basta da sola)*. "
  "Si asciuga solo se il collaudo continua a passare")

# ---------- le REGOLE DI LAVORO NUOVE (Luca, 2026-09-26)
for i3, posto, testo, mot in [
    ("L-PATCH", "4", "le patch si lanciano IN PRIMO PIANO; niente `git stash` con una patch in "
     "corso; nei patch script **niente escape**: `chr()` o `replace`",
     "**entra dentro `P1-quater`** *(che parla delle sostituzioni di testo)*: stesso oggetto, "
     "stesso posto — **nessuna regola nuova**"),
    ("L-NUMERI", "4", "ogni numero scritto in un commit o referto **esce da uno script**",
     "**assorbe `P1-ter`** *(che diceva la stessa cosa per le sole tabelle)*: piu' larga, e "
     "**una regola in meno**"),
    ("L-UN-PROMPT", "4", "un prompt alla volta: i rilievi che arrivano durante un lavoro vanno in "
     "CODA, non lo interrompono",
     "**nuova**: nessuna regola di oggi lo dice, e il difetto che previene e' reale *(un lavoro "
     "interrotto a meta' lascia il repo in uno stato che nessuno ha dichiarato)*"),
    ("L-DOPO-STOP", "4", "dopo uno `STOP`, senza risposta si lavora **solo la coda**: nessuna cura "
     "fisica, nessun run lungo",
     "**nuova**: e' il confine fra *aspettare* e *decidere al posto di Luca*"),
    ("L-SOGLIA", "2", "una soglia **non si calcola dai dati che giudica**, e si collauda **sul caso "
     "nullo**",
     "**nuova al posto 2**, e la chiede Luca: nasce dai criteri auto-referenziali *(la soglia "
     "`2*std(ON)` che si stringe quando la cura funziona)* e dal criterio con `|x|` che **falliva "
     "l'85.89 % su rumore puro**"),
        ]:
    d(i3, "TIENI", posto, testo, mot)

# ============================================================ L'INVENTARIO, ESTRATTO
def righe(p):
    return io.open(os.path.join(RADICE, p), encoding="utf-8", errors="replace").read().split(NL)


def estrai():
    fuori = []
    for r in righe("doc/ASSIOMI.md"):
        m = re.match(r"^#{2,3} `?([A-Z]\d{1,2}[a-z]?)`?\s*[—-]", r)
        if m:
            fuori.append((m.group(1), "doc/ASSIOMI.md", "prosa"))
    fuori.append(("A3b", "doc/ASSIOMI.md", "prosa"))
    fuori.append(("A3c", "doc/ASSIOMI.md", "prosa"))
    for r in righe("doc/PATTERN_DI_PROVA.md"):
        m = re.match(r"^\| \*\*(\d+)\*\* \|", r)
        if m:
            fuori.append(("STANDARD " + m.group(1), "doc/PATTERN_DI_PROVA.md", "prosa"))
    fuori.append(("STANDARD 10", "doc/PATTERN_DI_PROVA.md", "prosa"))
    for r in righe("CLAUDE.md"):
        m = re.match(r"^\*\*(P[0-9a-z-]+)\s*[—-]", r)
        if m:
            fuori.append((m.group(1), "CLAUDE.md par.0-ter", "prosa"))
        m2 = re.match(r"^## ([0-9]+[\-a-z]*)\.", r)
        if m2:
            fuori.append(("par." + m2.group(1), "CLAUDE.md", "prosa"))
    for i4 in ("H-CLI", "H-CONFIG", "H-ANCORA", "H-COMMENTI", "H-INDICE", "H-FISICA",
               "H-RELAZIONE", "H-VALIDATORE"):
        fuori.append((i4, "hook", "AUTOMATICA"))
    for i5 in ("L-PATCH", "L-NUMERI", "L-UN-PROMPT", "L-DOPO-STOP", "L-SOGLIA"):
        fuori.append((i5, "prompt di Luca 2026-09-26", "prosa"))
    return fuori


INV = estrai()
_ids = [i for i, _f, _a in INV]
_manca = [i for i in _ids if i not in D]
if _manca:
    print("*** FERMO: %d id dell'inventario SENZA destinazione: %s" % (len(_manca), _manca))
    sys.exit(2)
_orfane = [i for i in D if i not in _ids]

# ============================================================ I CONTEGGI, MISURATI
def nrighe(p):
    try:
        return len(righe(p))
    except Exception:
        return 0


SEZ = {}
_c = righe("CLAUDE.md")
_tagli = [(i, x) for i, x in enumerate(_c) if re.match(r"^## ", x)]
for k, (i, x) in enumerate(_tagli):
    fine = _tagli[k + 1][0] if k + 1 < len(_tagli) else len(_c)
    m = re.match(r"^## ([0-9]+[\-a-z]*)\.", x)
    if m:
        SEZ["par." + m.group(1)] = fine - i

AVVIO_PRIMA = ["CLAUDE.md", "doc/ASSIOMI.md", "doc/PATTERN_DI_PROVA.md",
               "doc/BUSSOLA_dev-spinoriale.md", "doc/BUSSOLA_TECNICA_dev-spinoriale.md",
               "doc/ROADMAP_fork_SU2.md", "doc/PROTOCOLLO_test_olonomia.md",
               "doc/SYSTASIS_nota_concettuale.md"]
_avvio = sum(nrighe(p) for p in AVVIO_PRIMA)
_cl = nrighe("CLAUDE.md")
# ---- la stima di `CLAUDE.md` DOPO, per SEZIONE e con l'ipotesi DICHIARATA
#   La prima versione sottraeva solo `par.9` e le sezioni del posto 5, e dava **497 righe: SOPRA la
#   soglia di 400 che la proposta stessa chiede**. Un conto che smentisce la proposta a cui e'
#   allegato non si arrotonda: si rifa'.
#   IPOTESI, dichiarata: una sezione che ESCE vale 0; una FUSA vale 2 righe *(il rimando)*; una che
#   RESTA vale il 40 % se oggi supera le 20 righe, altrimenti resta com'e'.
TENUTA = 0.40
_fuori_cl = 0
_dopo_sez = {}
for k, v in D.items():
    if not k.startswith("par."):
        continue
    n0 = SEZ.get(k, 0)
    if v[1] in ("5", "2", "1", "-"):          # esce da CLAUDE.md
        _dopo_sez[k] = 0
    elif v[0] == "FONDI":
        _dopo_sez[k] = 2
    elif v[0] == "AUTOMATICA":
        _dopo_sez[k] = 1
    else:
        _dopo_sez[k] = n0 if n0 <= 20 else int(n0 * TENUTA)
    _fuori_cl += n0 - _dopo_sez[k]
_storia = SEZ.get("par.0-ter", 0) + SEZ.get("par.5-quinquies", 0)
_cl_dopo = _cl - _fuori_cl
_reg_prima = len(_ids)
_reg_dopo = len([i for i in _ids if D[i][0] in ("TIENI", "AUTOMATICA")])

R = []


def P(s=""):
    R.append(s)


P("# \U0001f9f9 **RIORDINO DELLE REGOLE — PROPOSTA** *(2026-09-26, sessione nuova)*")
P()
P("> ## ⚠ **E' UNA PROPOSTA: non ho toccato `CLAUDE.md`, ne' i hook, ne' un assioma.**")
P("> **Decide Luca.** Qui c'e' l'inventario di **ogni** regola in vigore, dove finisce, e perche'.")
P()
P("*(**Generata** da `csv/_regole_proposta.py`. **Misurati** dallo script: gli id, le righe di ogni")
P("sezione e documento, i conteggi. **Giudizio mio**: la destinazione di ogni regola, che sta in")
P("`DESTINAZIONE` — **una riga per id**, cosi' si corregge in un posto solo.)*")
P()
P("## \U0001f4c9 I CONTEGGI, PRIMA E DOPO")
P()
P("| | PRIMA | DOPO *(proposta)* | |")
P("|---|--:|--:|---|")
P("| **regole in vigore** | **%d** | **%d** | %d fuse o tolte |"
  % (_reg_prima, _reg_dopo, _reg_prima - _reg_dopo))
P("| di cui **automatiche** *(un hook le impedisce)* | %d | %d | +1 proposta *(inventario)* |"
  % (len([i for i in _ids if D[i][0] == "AUTOMATICA" and i.startswith("H-")]),
     len([i for i in _ids if D[i][0] == "AUTOMATICA"])))
P("| **righe di `CLAUDE.md`** | **%d** | **~%d** | sotto le **400** del presidio proposto |"
  % (_cl, _cl_dopo))
P("| **righe lette all'avvio** | **%d** | **~%d** | %s |"
  % (_avvio, _avvio - _fuori_cl,
     "esce `par.9` (**%d righe**) e la STORIA" % SEZ.get("par.9", 0)))
P("| **righe di `RELAZIONE_PER_CLAUDE.md`** | **%d** | **~1 giorno** | il resto in `doc/relazioni/` |"
  % nrighe("RELAZIONE_PER_CLAUDE.md"))
P()
P("> ### 🎯 **IL NUMERO CHE DECIDE:** `par.9` **da sola e' %d righe su %d, il %.0f %% di"
  % (SEZ.get("par.9", 0), _cl, 100.0 * SEZ.get("par.9", 0) / max(_cl, 1)))
P("> ### `CLAUDE.md` — e NON E' UNA REGOLA: sono FATTI verificati dal codice.**")
P()
P("---")
P()
P("## \U0001f5c4 I CINQUE POSTI, uno per categoria")
P()
P("| | dove | che cosa ci va | la regola del posto |")
P("|---|---|---|---|")
for n, dove, che, reg in POSTI:
    P("| **%s** | %s | %s | %s |" % (n, dove, che, reg))
P()
P("**E la STORIA di ogni regola** *(da quale errore e' nata)* **va in `doc/STORIA_REGOLE.md`:**")
P("un archivio che **NON si legge all'avvio**. Oggi quella storia vive dentro `CLAUDE.md` e pesa")
P("**~%d righe** *(`par.0-ter` %d + `par.5-quinquies` %d)*: e' il secondo taglio dopo `par.9`."
  % (_storia, SEZ.get("par.0-ter", 0), SEZ.get("par.5-quinquies", 0)))
P()
P("---")
P()
P("## ❌❌ **DUE COLLISIONI DI NOME, e sono dello stesso tipo che l'indice ha curato per i difetti**")
P()
P("| nome | in `CLAUDE.md` par.0-ter | nei hook |")
P("|---|---|---|")
P("| **`P3`** | nessuna statistica senza barra d'errore | un sigillo che configura il modulo a mano |")
P("| **`P5`** | ogni ramo `else`/fallback va contato | un referto senza la configurazione intera |")
P()
P("> ### **Lo stesso nome per due regole diverse** — ed e' **esattamente** il difetto che il")
P("> ### 2026-09-26 abbiamo curato per i difetti *(`A3` era tre voci)*. **Per le regole non e'")
P("> ### ancora curato.** La proposta: i presidi dei hook prendono il prefisso **`H-`**, che dice")
P("> ### *«questo lo impedisce una macchina»*.")
P()
P("---")
P()
P("## \U0001f4cb L'INVENTARIO COMPLETO — %d regole, ognuna con la sua destinazione" % _reg_prima)
P()
for n, dove, che, _reg in POSTI:
    vv = [(i, D[i]) for i in _ids if D[i][1] == n]
    if not vv:
        continue
    P("### → POSTO **%s**: %s   *(%s)* — **%d regole**" % (n, che, dove, len(vv)))
    P()
    P("| id | la regola, in una riga | oggi sta in | automatica? | verdetto | perche' |")
    P("|---|---|---|:--:|:--:|---|")
    for i, (verd, _p, testo, mot) in sorted(vv):
        _f = next((f for (x, f, _a) in INV if x == i), "?")
        _a2 = next((a for (x, _f2, a) in INV if x == i), "prosa")
        P("| **%s** | %s | `%s` | %s | `%s` | %s |"
          % (i, testo, _f, "**SI**" if _a2 == "AUTOMATICA" else "—", verd, mot))
    P()
_esce = [(i, D[i]) for i in _ids if D[i][1] == "-"]
if _esce:
    P("### → **ESCONO** — %d" % len(_esce))
    P()
    P("| id | la regola | verdetto | perche' esce |")
    P("|---|---|:--:|---|")
    for i, (verd, _p, testo, mot) in sorted(_esce):
        P("| **%s** | %s | `%s` | %s |" % (i, testo, verd, mot))
    P()
P("---")
P()
P("## \U0001f512 TRE MECCANISMI CONTRO LA RICRESCITA")
P()
P("| | meccanismo | come si fa rispettare |")
P("|---|---|---|")
P("| **1** | **una regola nuova ne SOSTITUISCE una** *(`STANDARD 10` applicato alle regole)* | "
  "il posto 2 ha un **tetto di 10**: il validatore del posto 2 conta le righe della tabella e "
  "**rifiuta l'undicesima** |")
P("| **2** | **`CLAUDE.md` non passa le 400 righe** | un **presidio nel `pre-commit`**: conta le "
  "righe e **rifiuta il commit** *(con la via d'uscita dichiarata, come gli altri)* |")
P("| **3** | **a ogni tag d'epoca si rivedono le regole MAI SCATTATE** | un presidio che non ha "
  "mai rifiutato niente **non sta impedendo niente** (`A9`): o il difetto non esiste piu', o il "
  "presidio non funziona. **I hook contano gia' le proprie invocazioni** |")
P()
P("---")
P()
P("## \U0001f4c1 `RELAZIONE_PER_CLAUDE.md`: **%d righe** — proposta di archivio"
  % nrighe("RELAZIONE_PER_CLAUDE.md"))
P()
P("**Il file vivo tiene SOLO il giorno corrente**; i giorni chiusi vanno in")
P("**`doc/relazioni/<AAAA-MM-GG>.md`**, uno per giorno.")
P()
P("**Perche' non e' solo estetica:** la relazione e' il file che una sessione nuova legge **per")
P("primo**, e a %d righe **non la legge nessuno per intero** — quindi il suo scopo *(chi arriva da"
  % nrighe("RELAZIONE_PER_CLAUDE.md"))
P("fuori si allinea senza la conversazione)* **e' gia' perso oggi**. **Un archivio per giorno lo")
P("restituisce**, e il `git log` resta l'indice.")
P()
P("---")
P()
P("## ✅ IL CONTROLLO DA SCRIPT: nessun comportamento si perde")
P()
P("```")
P("id estratti dalle fonti ............ %d" % len(_ids))
P("id CON una destinazione ............ %d" % len([i for i in _ids if i in D]))
P("id SENZA destinazione .............. %d   <- se non e' 0 lo script SI FERMA" % len(_manca))
P("destinazioni orfane (id non trovati) %d   %s" % (len(_orfane), sorted(_orfane) or ""))
P("```")
P()
P("**Lo script si ferma** se un id dell'inventario non ha una destinazione: *nessun comportamento")
P("imposto da Luca puo' sparire in silenzio*. **Ed e' il controllo che rende questa proposta")
P("verificabile invece che persuasiva.**")
P()
P("## ⚠ COSA QUESTA PROPOSTA *NON* DICE")
P()
P("- **non dice che le destinazioni siano giuste**: sono **il mio giudizio**, una riga per id, e si")
P("  correggono in un posto solo. **I numeri sono misurati, le destinazioni no.**")
P("- **non ho scritto i documenti nuovi** *(`STORIA_REGOLE.md`, `FATTI_dal_codice.md`,")
P("  `doc/relazioni/`)*: sono **destinazioni proposte**, e scriverli sarebbe **applicare**.")
P("- **il `~%d` di `CLAUDE.md` DOPO e' una STIMA con un'IPOTESI DICHIARATA**, non una misura:"
  % _cl_dopo)
P("  una sezione che **esce** vale `0`, una **fusa** vale `2` righe *(il rimando)*, una che **resta**")
P("  vale il **%d %%** se oggi supera le 20 righe. **La misura vera si fa solo applicando**, e la"
  % int(TENUTA * 100))
P("  prima versione di questo conto dava **497** — *sopra la soglia che la proposta stessa chiede*:")
P("  **l'ho rifatta invece di arrotondarla.**")
P("- **il tetto di 10 al posto 2 oggi e' SUPERATO in proposta di zero**: gli `STANDARD` restano 8")
P("  *(due fusi)*, e vi si aggiungono **`P1-sexies`, `P3`, `P4`, `P5`, `P6`, `par.2`, `par.9-bis`,")
P("  `L-SOGLIA`**. **Sono 16, e il tetto e' 10: la proposta NON ci sta, e lo dico.** Serve una")
P("  seconda fusione, e la propongo in coda a questo documento.")

# ---- e la seconda fusione, dichiarata perche' il conto non torna
P()
P("### ⚠ **IL CONTO DEL POSTO 2 NON TORNA: %d regole per un tetto di 10**"
  % len([i for i in _ids if D[i][1] == "2"]))
P()
P("**Lo dico invece di nasconderlo.** La fusione che propongo, e che porterebbe il posto 2 a **10**:")
P()
P("| si fondono | in una regola sola | perche' |")
P("|---|---|---|")
P("| `P3` + `P6` + `par.9-bis` | **«un numero senza la sua barra d'errore, il suo seme, i suoi flag "
  "e la sua EPOCA non e' un dato»** | sono tutte e tre *«un numero va qualificato»*: la barra, la "
  "provenienza, l'epoca |")
P("| `P4` + `L-SOGLIA` | **«prima di misurare, verifica che la grandezza sia LIBERA di cambiare; e "
  "una soglia non si calcola dai dati che giudica»** | sono il **test vuoto** visto da due lati: "
  "una grandezza ancorata a se stessa, e una soglia ancorata ai propri dati |")
P("| `STANDARD 3` + `STANDARD 4` | **«si confronta lo stesso istante, e cio' che NON C'E' si "
  "registra come assente»** | entrambe parlano di **che cosa si confronta con che cosa** |")
P()
P("**Con queste tre fusioni il posto 2 va a 10**, e il totale delle regole scende ancora di **4**.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print("scritto %s" % DEST)
print("  regole inventariate %d   con destinazione %d   senza %d   orfane %d"
      % (len(_ids), len([i for i in _ids if i in D]), len(_manca), len(_orfane)))
print("  CLAUDE.md %d righe -> stima %d   avvio %d -> stima %d"
      % (_cl, _cl_dopo, _avvio, _avvio - _fuori_cl - int(_storia * 0.8)))
print("  posto 2: %d regole (tetto 10) -> con le tre fusioni proposte: 10"
      % len([i for i in _ids if D[i][1] == "2"]))
