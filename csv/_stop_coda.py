# -*- coding: utf-8 -*-
r"""IL PRESIDIO SULLO STOP — **un checkpoint non chiude il turno.**

> ### ⛔ **PERCHE' ESISTE:** la regola `L-NON-FERMARSI-AL-CHECKPOINT` e' **scritta**, e
> **due volte nello stesso giorno** mi sono fermato comunque dopo un commit. ### **Una
> regola scritta che non impedisce non e' un presidio** *(`A9`)* — e questo file e' il
> tentativo di farne un **impedimento**.

### ⭐ **CHE COSA FA, in una riga:** quando il turno sta per chiudersi, guarda se c'e'
**lavoro PRONTO** *(che non aspetta una decisione di Luca)* e, se c'e', **blocca lo stop
nominando il pezzo successivo**.

### ⛔ **E NON TOCCA IL REPO: LEGGE SOLTANTO.** Il promemoria contro i cicli vive **fuori
dal repo** *(nella cartella temporanea della sessione)*, e questa e' una scelta
dichiarata: ricordare «ho gia' bloccato» richiede uno stato, e **uno stato dentro il repo
sarebbe un file che il presidio scrive a ogni turno.**

## ⚠ CHE COSA HO VERIFICATO DAVVERO, E CHE COSA NO

Dai **file installati** di Claude Code *(l'estensione VS Code `2.1.295`)*:

* ✅ **la forma della configurazione** e l'elenco degli eventi — da
  `claude-code-settings.schema.json`: un evento *(fra cui `Stop`)* porta una lista di
  gruppi, ognuno con `hooks: [{type: "command", command, args}]`. ### **E `args` e' la
  forma `exec`: il comando NON passa da una shell**, quindi un percorso con spazi o `$`
  non viene reinterpretato.
* ✅ **il protocollo di uscita** `{"continue": bool, "hookSpecificOutput": {...}}` — letto
  **nel codice dell'estensione stessa**, che usa un suo hook `PostToolUse`.
* ✅ **che un hook `Stop` PUO' bloccare davvero**, e **il contratto obbligatorio** — dalle
  stringhe del binario `claude.exe`, **alla lettera**:

  > *«For Stop/SubagentStop hooks, **check `stop_hook_active` in the input and return
  > success while it's true**. Set `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` to raise this
  > limit.»*
  > *«A hook blocked the turn from ending … consecutive times … overriding and ending
  > turn.»*

  ### ⭐ **QUINDI CLAUDE CODE HA GIA' UNA SUA PROTEZIONE DAI CICLI** *(un tetto ai blocchi
  consecutivi)*, e **pretende che il hook ne abbia una sua**: `stop_hook_active`.
* ⛔ **NON ho trovato il NOME esatto del campo d'uscita che blocca uno `Stop`.** Le
  occorrenze di `stopReason` nel bundle JS sono **lo schema MCP di sampling**, non i hook.

### ⭐ **QUINDI LO SCRIPT FA TRE COSE**: ① rispetta `stop_hook_active` *(il contratto
scritto)*; ② tiene **la sua** protezione, legata al **commit** e non al turno — ed e'
quella che il mandato chiede, *«mai due volte senza un commit nuovo»*; ③ **emette le forme
note insieme** *(una chiave in piu' viene ignorata)* **e usa il codice d'uscita `2`**.
### ⚠ **E IL LIMITE RESTA DETTO: il collaudo prova che lo script DECIDE BENE**, non che
Claude Code onori **quel** campo.

Gira con:  python csv/_stop_coda.py            (legge il JSON dell'hook da stdin)
           python csv/_stop_coda.py --collaudo (i tre casi, senza stdin)
"""
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)

# ### ⛔ **IL PRESIDIO DELL'ENCODING C'E', MA NON PUO' ESSERE `_presidio.avvia()`** — e il
# ### motivo **non e' una dimenticanza**: `avvia()` ### **STAMPA il timbro su stdout**, e
# ### qui ### **stdout E' IL CANALE JSON del hook** — un timbro davanti alla graffa
# ### ### **romperebbe il JSON a ogni turno.**
# ### ⭐ **QUINDI: la RICONFIGURAZIONE si fa** *(e' la meta' che serve)*, **e il TIMBRO si
# ### stampa SOLO nel collaudo**, dove stdout e' di chi legge e non del hook.
# ### ⚠ **E l'output del hook resta ASCII PURO per costruzione:** le forme accentate
# ### *(`GIA'`, `perche'`)* sono scritte con l'apostrofo, e questo e' ### **un vincolo del
# ### file, non un caso.**
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:                                             # noqa: BLE001
    pass

# ### ⛔ **I PEZZI, DICHIARATI UNO A UNO — e NON si scoprono con un `glob`.**
# ### ⭐ **E' la stessa scelta di `primo_ordine/collauda.py` per i collaudi**, e la ragione
# ### e' la stessa: ### **un elenco dichiarato si legge**, e un pezzo che spariva da un
# ### `glob` ### **spariva in silenzio.**
# ### Ogni riga: `(nome, il file che ESISTE quando e' fatto, le voci che lo BLOCCANO)`.
# ### \u26d4 **LA TERZA COLONNA E- UNA CORREZIONE DEL `2026-10-12`, e sanava una
# ### ### **AFFERMAZIONE FALSA NEL MIO CODICE:** il docstring di `pronti()` diceva che
# ### <<pronto>> vuol dire ### **non e- fatto E non aspetta una decisione di Luca**, e che
# ### ### **la seconda la dice l-indice**. ### **Ma il codice NON interrogava l-indice
# ### affatto.** ### \u26a0 **Quindi il presidio avrebbe bloccato il turno su un pezzo che
# ### aspetta una risposta di Luca** -- cioe- ### **avrebbe girato a vuoto proprio nel
# ### caso in cui fermarsi e- GIUSTO.**
# ### ⛔ **E IL MARCATORE E- IL COLLAUDO DI ACCETTAZIONE, NON IL PRIMO FILE** --
# ### correzione del `2026-10-12`, trovata progettando il pezzo `5`. ### Prima il pezzo
# ### `5` era segnato FATTO quando esisteva `primo_ordine/motore.py`: ma quello e- il
# ### sotto-pezzo `5b`, e dopo vengono il checkpoint e i collaudi della memoria.
# ### ### **Cioe- il presidio lasciava chiudere il turno col pezzo a META-**, che e-
# ### ### **la forma del difetto che esiste per impedire.**
# ### ⭐ **E VALE IN GENERALE: un pezzo e- fatto quando il suo COLLAUDO esiste**, non
# ### quando esiste il suo codice.
PEZZI = (
    ("il pezzo 5 del simulatore: IL MOTORE (doppio contenitore, CSR, punto unico di "
     "scrittura, checkpoint) -- il suo collaudo di accettazione e- la MEMORIA",
     "primo_ordine/_collauda_memoria.py", ()),
    # ### ⛔ **E QUESTO IL PRESIDIO ME L-HA DETTO DAL VIVO, non in collaudo:** ha
    # ### bloccato il mio stop nominando ### **il pezzo `6`** -- ma la coda dice che
    # ### ### **il CONFRONTO viene PRIMA**, e la sua lista ### **non lo conteneva.**
    # ### ⭐ **Un elenco dichiarato si legge, ma va anche TENUTO:** un presidio che
    # ### nomina il pezzo sbagliato ### **manda a lavorare fuori ordine**, che e- la
    # ### cosa che il paragrafo `13` chiama <<lavorare fuori ordine>>.
    ("il CONFRONTO COMPLETO fra la tabella delle leggi e il banco congelato -- PRIMA "
     "del flusso di saturazione e PRIMA del criterio di passaggio, per mandato",
     "doc/CONFRONTO_tabella_banco.md", ()),
    # ### \u26d4 **IL PEZZO `6` ASPETTA DUE RISPOSTE, e sono di fisica:** il criterio di
    # ### passaggio pretende che il generato ### **riproduca il banco congelato**, e per
    # ### farlo serve sapere ### **di che tipo e- il vuoto** *(la tabella lo dice reale, il
    # ### banco lo tiene complesso)* e ### **da dove nasce la geometria** nell-era `2`.
    # ### ⚠ **TERZA VOLTA CHE QUESTA LISTA INVECCHIA, e lo scrivo invece di
    # ### aggiustarla in silenzio.** La prima: non conteneva il confronto. La seconda: il
    # ### marcatore del pezzo `5` era il suo PRIMO FILE invece del suo COLLAUDO. La
    # ### terza: il bloccante del pezzo `6` era ### **la domanda su `phi`, che Luca ha
    # ### CHIUSO** -- e appena chiusa il presidio ha ricominciato a nominare il pezzo
    # ### `6`, che invece aspetta ### **un-ALTRA risposta** *(le condizioni iniziali,
    # ### l-unico `CONFLITTO` del confronto)*.
    # ### ⛔ **E LA LEZIONE NON E- <<derivare la lista>>:** derivarla la farebbe
    # ### ### **coincidere sempre**, cioe- il presidio ### **non direbbe piu- niente.**
    # ### ⭐ **La lezione e- che IL BLOCCANTE DI UN PEZZO CAMBIA quando una
    # ### domanda si chiude**, e va riguardato ### **a ogni risposta di Luca.**
    ("la SOGLIA DELLA MEMORIA a 5x con le tre riduzioni sicure, e lo stato iniziale "
     "delle estremita- nuove come POSTO APERTO (mandato di Luca: decide `m1`)",
     "doc/TASK_HISTORY/2026-10-12_soglia_memoria.md", ()),
    ("il pezzo 6 del simulatore: IL CRITERIO DI PASSAGGIO (il generato riproduce il "
     "banco congelato al bit)", "primo_ordine/_collauda_passaggio.py",
     ("DOMANDA-CONDIZIONI-INIZIALI-IN-TABELLA",)),
    # ### ⛔ **QUARTA VOLTA CHE QUESTA LISTA INVECCHIA -- E LA PRIMA NEL VERSO
    # ### PEGGIORE.** Le prime tre nominavano ### **il pezzo sbagliato**; questa
    # ### ### **mi ha lasciato FERMARE mentre c-era da fare**, dicendo *<<la coda e-
    # ### BLOCCATA>>* quando il mandato su energia e mitosi aveva ### **lavoro pronto.**
    # ### ⭐ **E il verso conta: un presidio troppo severo si fa notare, uno
    # ### troppo permissivo NO** -- e questo esiste proprio per impedire che io mi fermi
    # ### quando c-e- da fare.
    # ### ⚠ **La causa e- sempre la stessa:** un mandato nuovo porta pezzi
    # ### nuovi, e ### **la lista non si aggiorna da sola.** ### La lezione non e-
    # ### <<derivarla>> *(coinciderebbe sempre)*: e- che ### **un mandato nuovo si
    # ### registra QUI nello stesso giro in cui si registra nella coda.**
    ("il mandato ENERGIA E MITOSI, parte 0: REGISTRARE le decisioni (energia promossa "
     "provvisoria, e chi paga la nascita) -- nessuna dipendenza",
     "doc/TASK_HISTORY/2026-10-12_energia_e_mitosi.md", ()),
    # ### ✅ **E IL FLUSSO DI SATURAZIONE E- SBLOCCATO:** era fermo ### **solo
    # ### sul tipo di `phi`**, e Luca ha deciso che e- complesso.
    ("il flusso di SATURAZIONE nel motore (`P1` del mandato energia e mitosi), che era "
     "bloccato SOLO dal tipo di phi", "primo_ordine/_collauda_saturazione.py", ()),
    # ### ⚠ **QUINTA VOLTA, e questa e- un MARCATORE CHE PUNTAVA A UN FILE
    # ### CHE NON AVREI MAI SCRITTO:** il pezzo si chiamava
    # ### `2026-10-13_spazio_che_nasce.md`, e la derivazione l-ho scritta in
    # ### `2026-10-12_mitosi.md`. ### **Un marcatore cosi- non e- <<sbagliato una volta>>:
    # ### sbaglia PER SEMPRE**, perche- il file atteso non arrivera- mai.
    # ### ⛔ **E LA LEZIONE, dopo cinque volte, NON e- ancora <<derivare la
    # ### lista>>** *(coinciderebbe sempre)*: ### **e- che il marcatore di un pezzo e- un
    # ### FILE, e un file lo decide chi lo scrive** -- quindi il marcatore si fissa
    # ### ### **quando il pezzo si apre**, non quando si progetta.
    # ### ✅ **Il pezzo e- FATTO: la derivazione della mitosi e- `P5`**, e il suo
    # ### file esiste.
    ("la derivazione di SPAZIO-CHE-NASCE, cioe- la MITOSI (`P5`): solo task history",
     "doc/TASK_HISTORY/2026-10-12_mitosi.md",
     ("DOMANDA-QUALE-SEGNO",)),
)


def _testa():
    """### Lo `HEAD` di adesso. ### **E' la chiave del promemoria contro i cicli.**"""
    try:
        q = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RADICE,
                           capture_output=True, text=True)
        return (q.stdout or "").strip() or "?"
    except Exception:                                         # noqa: BLE001
        return "?"


def _promemoria():
    """### Il file del promemoria, ### **FUORI dal repo.**

    ### ⛔ **E il percorso NON e' una scelta di comodo:** dentro il repo sarebbe
    ### **un file che il presidio scrive a ogni turno**, e il mandato dice
    ### **<<legge soltanto>>.**
    """
    base = (os.environ.get("CLAUDE_STOP_MEMO")
            or os.path.join(os.environ.get("TEMP") or os.path.expanduser("~"),
                            "_stop_coda_memo.json"))
    return base


def aspettano_luca():
    """### Gli `id` delle voci su cui ### **l'indice aspetta Luca**, dal file GENERATO.

    ### ⛔ **Si leggono dal file e non si indovinano:** `DA_DECIDERE_LUCA.md` lo
    ### **genera** `indice.py da-decidere`, col suo criterio *(priorita' non vuota e stato
    aperto)*. ### **Un elenco mio accanto a quello sarebbe la seconda verita' che
    divergerebbe.**
    """
    p = os.path.join(RADICE, "doc", "indice", "DA_DECIDERE_LUCA.md")
    if not os.path.exists(p):
        return set()
    t = io.open(p, encoding="utf-8").read()
    # ### ⛔ **LO SCHEMA DI UN ID, e non <<tutto cio- che e- maiuscolo>>:** al primo
    # ### giro prendevo anche il GRASSETTO del markdown -- il collaudo ha nominato
    # ### ### **`**DUE`** come se fosse una voce. ### ⚠ **Un estrattore troppo largo
    # ### non e- generoso: DICE IL FALSO**, e un pezzo si sarebbe potuto bloccare su una
    # ### voce che non esiste.
    import re as _re
    return set(_re.findall(r"\b[A-Z][A-Z0-9]{2,}(?:-[A-Z0-9]+)+\b", t))


def pronti():
    """### I pezzi ### **PRONTI**, e <<pronto>> vuol dire ### **DUE cose.**

    ### ⭐ **Entrambe necessarie:** il pezzo ### **non e' fatto**, e ### **non aspetta
    una decisione di Luca** -- e la seconda ### **la dice l'indice**, non io.

    ### ⚠ **E fino al `2026-10-12` la seconda NON ERA CONTROLLATA:** il docstring la
    diceva e il codice ### **non interrogava l'indice affatto**. ### **Era
    un'affermazione falsa nel mio codice**, e avrebbe fatto bloccare il turno
    ### **proprio quando fermarsi e' giusto.**
    """
    attesa = aspettano_luca()
    fuori = []
    for nome, f, blocchi in PEZZI:
        if os.path.exists(os.path.join(RADICE, f)):
            # ### il ramo FATTO: il suo collaudo di accettazione ESISTE
            continue
        fermi = [b for b in blocchi if b in attesa]
        if fermi:
            # ### il ramo ASPETTA LUCA: ### **non e' pronto, ed e' una cosa DIVERSA da
            # ### <<fatto>>** -- per questo il motivo lo NOMINA.
            continue
        fuori.append(nome)
    return fuori


def fermi_su_luca():
    """### I pezzi che ### **aspettano Luca**, col nome della voce. ### **Per DIRLO.**

    ### ⛔ **Un pezzo che aspetta e un pezzo che non c'e' non sono la stessa cosa**, e
    un presidio che li confondesse direbbe *<<la coda e' vuota>>* ### **quando invece e'
    BLOCCATA.**
    """
    attesa = aspettano_luca()
    return [(nome, [b for b in blocchi if b in attesa])
            for nome, f, blocchi in PEZZI
            if not os.path.exists(os.path.join(RADICE, f))
            and any(b in attesa for b in blocchi)]


def quante_aspettano_luca():
    """### Quante domande aspettano Luca, ### **dall'indice e non da me.**

    ### ⛔ **NON serve a bloccare, serve a NON bloccare:** se l'unico lavoro che resta
    e' ### **una decisione di Luca**, il turno ### **deve poter finire.**
    """
    p = os.path.join(RADICE, "doc", "indice", "DA_DECIDERE_LUCA.md")
    if not os.path.exists(p):
        return 0
    t = io.open(p, encoding="utf-8").read()
    # ### la riga di intestazione dell'elenco porta il conto, e si legge da la'
    for riga in t.split(chr(10)):
        if "domande" in riga and "voci" in riga:
            for pezzo in riga.replace(",", " ").split():
                if pezzo.isdigit():
                    return int(pezzo)
    return t.count("[[DOMANDA-")


def decidi(testa, memo_letto, attivo=False):
    """### `(blocca, motivo)`. ### **PURA: nessun disco, nessun `git`.**

    ### ⭐ **Cosi' il collaudo la prova sui tre casi in memoria**, invece di costruire
    tre repository.

    ### ⛔ **`attivo` E' `stop_hook_active`, E NON E' UNA CORTESIA:** il binario di Claude
    Code dice ### **<<return success while it's true>>** -- e un hook che blocca mentre
    quel campo e' vero ### **sta girando dentro un ciclo che ha gia' cominciato.**
    ### ⚠ **E' il PRIMO controllo**, prima ancora di guardare la coda: se il ciclo e' in
    corso, ### **che ci sia lavoro pronto non cambia la risposta.**
    """
    if attivo:
        return (False, "`stop_hook_active` e' VERO: Claude Code dice di tornare successo"
                       " finche' lo e', e un blocco qui girerebbe dentro un ciclo gia'"
                       " cominciato")
    p = pronti()
    if not p:
        # ### \u2b50 **E SI DICE PERCHE-: <<vuota>> e <<BLOCCATA>> non sono la stessa
        # ### cosa.** Se la coda e- ferma su una decisione di Luca, il motivo
        # ### ### **NOMINA la voce** -- cosi- chi legge sa ### **che cosa sbloccherebbe il
        # ### lavoro**, invece di credere che non ci sia niente da fare.
        fermi = fermi_su_luca()
        if fermi:
            return (False, "la coda e' BLOCCATA, non vuota: %s"
                    % "; ".join("%s aspetta %s" % (n[:60], ",".join(v))
                                for n, v in fermi))
        return (False, "la coda non ha pezzi pronti: il turno puo' finire")
    if memo_letto == testa:
        # ### ⛔ **LA PROTEZIONE DAI CICLI, e la sua condizione e' `HEAD`:** se ho gia'
        # ### bloccato ### **a questo stesso commit**, bloccare di nuovo vorrebbe dire
        # ### ### **girare a vuoto** -- e un presidio che impedisce di finire senza far
        # ### avanzare niente ### **e' peggio della regola scritta.**
        return (False, "ho GIA' bloccato lo stop a questo commit (%s) e NON c'e' un "
                       "commit nuovo: lascio finire, e il motivo e' che bloccare di "
                       "nuovo girerebbe a vuoto. ### Il pezzo pronto resta: %s"
                % (testa[:8], p[0]))
    return (True, "continua con: %s" % p[0])


def main(argv):
    if "--collaudo" in argv:
        return collaudo()
    # ### ⚠ **IL JSON DELL'HOOK SI LEGGE E NON SI PRETENDE:** se stdin e' vuoto o
    # ### malformato il presidio ### **non deve rompere il turno** -- un presidio che
    # ### rompe quando il suo ingresso cambia forma ### **si spegne il primo giorno.**
    try:
        _dati = json.loads(sys.stdin.read() or "{}")
    except Exception:                                         # noqa: BLE001
        _dati = {}
    testa = _testa()
    memo = _promemoria()
    letto = None
    try:
        letto = json.loads(io.open(memo, encoding="utf-8").read()).get("testa")
    except Exception:                                         # noqa: BLE001
        letto = None
    blocca, motivo = decidi(testa, letto, bool(_dati.get("stop_hook_active")))
    if blocca:
        try:
            io.open(memo, "w", encoding="utf-8").write(
                json.dumps({"testa": testa}, ensure_ascii=False))
        except Exception:                                     # noqa: BLE001
            pass
        # ### ⛔ **LE FORME NOTE, INSIEME:** una chiave in piu' viene ignorata, e
        # ### ### **non ho potuto verificare QUALE blocchi uno `Stop`** nei file
        # ### installati. ### ⭐ **E il codice d'uscita `2`** e' il segnale di blocco
        # ### uniforme fra i tipi di hook.
        print(json.dumps({
            "continue": False,
            "stopReason": motivo,
            "decision": "block",
            "reason": motivo,
            "systemMessage": motivo,
            "hookSpecificOutput": {"hookEventName": "Stop",
                                   "additionalContext": motivo},
        }, ensure_ascii=False))
        sys.stderr.write(motivo + chr(10))
        return 2
    print(json.dumps({"continue": True,
                      "hookSpecificOutput": {"hookEventName": "Stop",
                                             "additionalContext": motivo}},
                     ensure_ascii=False))
    return 0


def collaudo():
    """### I TRE CASI del mandato, ### **e il terzo e' quello che evita il ciclo.**"""
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    # ### ⭐ **IL TIMBRO QUI SI', nel hook NO:** nel collaudo stdout e' di chi legge.
    try:
        sys.path.insert(0, _QUI)
        import _presidio                                      # noqa: PLC0415
        print(_presidio.timbro(os.path.abspath(__file__)))
    except Exception as _e:                                   # noqa: BLE001
        print("### il timbro non si e' potuto leggere: %s" % _e)
    print("=" * 100)
    print("IL PRESIDIO SULLO STOP -- i tre casi")
    print("=" * 100)
    veri = PEZZI
    try:
        # ### (1) LAVORO PRONTO -> BLOCCA
        globals()["PEZZI"] = (("il pezzo finto", "non/esisto/affatto.py", ()),)
        b, m = decidi("aaaaaaaa", None)
        esito("### (1) c'e' lavoro PRONTO: BLOCCA, e NOMINA il pezzo",
              b and "il pezzo finto" in m, "### %r" % m[:60])
        # ### (2) NIENTE PRONTO -> LASCIA FERMARE
        globals()["PEZZI"] = (("un pezzo fatto", "CLAUDE.md", ()),)
        b2, m2 = decidi("aaaaaaaa", None)
        esito("### (2) la coda NON ha pezzi pronti: LASCIA FERMARE",
              not b2, "### %r" % m2[:60])
        # ### (3) GIA' BLOCCATO, NESSUN COMMIT NUOVO -> LASCIA FERMARE
        globals()["PEZZI"] = (("il pezzo finto", "non/esisto/affatto.py", ()),)
        b3, m3 = decidi("aaaaaaaa", "aaaaaaaa")
        esito("### (3) GIA' bloccato a questo commit: LASCIA FERMARE, e dice perche'",
              (not b3) and "GIA'" in m3 and "il pezzo finto" in m3,
              "### e il pezzo pronto resta NOMINATO")
        # ### (3-bis) e con un COMMIT NUOVO blocca di nuovo
        b4, _m4 = decidi("bbbbbbbb", "aaaaaaaa")
        esito("### (3-bis) ma con un COMMIT NUOVO blocca di nuovo",
              b4, "### altrimenti il presidio si spegnerebbe per sempre")
        # ### ⛔ **(3-ter) IL CONTRATTO DI CLAUDE CODE VINCE SU TUTTO:** c'e- lavoro
        # ### pronto, il commit e- nuovo, e ### **nonostante questo NON si blocca** --
        # ### perche- ### **<<return success while it's true>>.** ### ⭐ **E questo
        # ### braccio POTEVA fallire:** fino a poco fa lo script ### **ignorava quel
        # ### campo**, e qui sarebbe stato rosso.
        b5, m5 = decidi("bbbbbbbb", "aaaaaaaa", True)
        esito("### (3-ter) `stop_hook_active` VERO: NON blocca, col lavoro pronto",
              (not b5) and "stop_hook_active" in m5,
              "### e il contratto e- CITATO nel motivo")
        # ### \u26d4 **(3-quater) UN PEZZO CHE ASPETTA LUCA NON E- PRONTO**, e il
        # ### motivo ### **NOMINA la voce**: <<vuota>> e <<BLOCCATA>> non sono la stessa
        # ### cosa. ### \u2b50 **E questo braccio POTEVA fallire:** fino a poco fa
        # ### `pronti()` ### **non guardava l-indice affatto.**
        attesa = sorted(aspettano_luca())
        if attesa:
            globals()["PEZZI"] = (("un pezzo che aspetta Luca",
                                   "non/esisto/affatto.py", (attesa[0],)),)
            b6, m6 = decidi("cccccccc", None)
            esito("### (3-quater) un pezzo che ASPETTA LUCA: NON blocca, e lo DICE",
                  (not b6) and "BLOCCATA" in m6 and attesa[0] in m6,
                  "### la voce nominata e- `%s`" % attesa[0])
            # ### \u2705 **E IL VERSO OPPOSTO: una voce che NON aspetta non lo ferma.**
            globals()["PEZZI"] = (("un pezzo libero", "non/esisto/affatto.py",
                                   ("UNA-VOCE-CHE-NON-ESISTE",)),)
            b7, _m7 = decidi("cccccccc", None)
            esito("### e una voce che NON aspetta Luca NON ferma il pezzo",
                  b7, "### altrimenti ogni pezzo con una voce sarebbe bloccato")
        else:
            esito("### (3-quater) il braccio su <<aspetta Luca>> NON HA MATERIA",
                  False, "### `DA_DECIDERE_LUCA.md` non elenca nessuna voce: il braccio"
                         " passerebbe PER VACUITA-, e questo e- un FALLIMENTO")
    finally:
        globals()["PEZZI"] = veri
    # ### ⭐ **E un braccio sul VERO elenco**, per non provare solo i casi finti.
    esito("### (4) e sull'elenco VERO la decisione non alza",
          isinstance(decidi(_testa(), None), tuple),
          "### %d pezzi pronti oggi, %d domande aspettano Luca"
          % (len(pronti()), quante_aspettano_luca()))
    # ### ⛔ **(5) LA PUREZZA ASCII DELL'USCITA, PROVATA E NON DICHIARATA:** il hook non
    # ### puo' chiamare `_presidio.avvia()`, quindi il vincolo ### **che i suoi messaggi
    # ### siano ASCII** e' l'unica difesa che resta -- e ### **un vincolo che nessuno
    # ### verifica e' una testimonianza** *(`A9`)*. ### Si provano ### **i messaggi veri
    # ### di `decidi`**, non il file.
    msg = [decidi("aaaaaaaa", None)[1], decidi("aaaaaaaa", "aaaaaaaa")[1],
           decidi(_testa(), None)[1]]
    sporchi = [m for m in msg if any(ord(c) > 127 for c in m)]
    esito("### (5) i messaggi del hook sono ASCII PURO (stdout e' il canale JSON)",
          not sporchi, "### %d messaggi provati, %d fuori da ASCII"
                       % (len(msg), len(sporchi)))
    # ### ⚠ **(6) E IL NOME DEI PEZZI SI LEGGE:** un elenco dichiarato serve a chi legge,
    # ### e un nome vuoto o un percorso assoluto ### **lo renderebbero inutile.**
    male = [f for _n, f, _b in PEZZI if os.path.isabs(f) or not _n.strip()]
    esito("### (6) l'elenco dei pezzi e' relativo e nominato",
          not male, "### %d pezzi dichiarati" % len(PEZZI))
    # ### ⛔ **(7) LA REGISTRAZIONE PUNTA A UN FILE CHE ESISTE.** ### ⭐ **E questo
    # ### braccio esiste per un motivo preciso:** un presidio registrato con un percorso
    # ### sbagliato ### **non impedisce niente e non lo dice** -- fallirebbe a vuoto a
    # ### ogni turno, ### **che e- esattamente la forma di `A9`** che sto cercando di
    # ### togliere. Qui si legge ### **la configurazione vera**, non una copia.
    reg, nota = [], ""
    try:
        cfg = json.loads(io.open(os.path.join(RADICE, ".claude", "settings.json"),
                                 encoding="utf-8").read())
        for gruppo in (cfg.get("hooks") or {}).get("Stop") or []:
            for h in gruppo.get("hooks") or []:
                for a in h.get("args") or []:
                    reg.append(a)
        manca = [a for a in reg
                 if not os.path.exists(os.path.join(RADICE, a.replace("/", os.sep)))]
        nota = "### %d argomenti registrati, %d non esistono" % (len(reg), len(manca))
        passa = bool(reg) and not manca
    except Exception as e:                                    # noqa: BLE001
        passa, nota = False, "### la configurazione non si e' letta: %s" % e
    esito("### (7) `.claude/settings.json` registra `Stop` su un file che ESISTE",
          passa, nota)
    print("=" * 100)
    print("IL PRESIDIO SULLO STOP: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
