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
# ### Ogni riga: `(nome del pezzo, il file che ESISTE quando il pezzo e' fatto)`.
PEZZI = (
    ("il pezzo 5 del simulatore: IL MOTORE (doppio contenitore, CSR, punto unico di "
     "scrittura, checkpoint)", "primo_ordine/motore.py"),
    ("il pezzo 6 del simulatore: IL CRITERIO DI PASSAGGIO (il generato riproduce il "
     "banco congelato al bit)", "primo_ordine/_collauda_passaggio.py"),
    ("la derivazione di SPAZIO-CHE-NASCE (solo task history, nessun codice)",
     "doc/TASK_HISTORY/2026-10-13_spazio_che_nasce.md"),
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


def pronti():
    """### I pezzi ### **PRONTI**: quelli il cui file ### **non esiste ancora.**

    ### ⭐ **E <<pronto>> vuol dire DUE cose, entrambe necessarie:** il pezzo
    ### **non e' fatto**, e ### **non aspetta una decisione di Luca** — e la seconda la
    dice l'indice, non io.
    """
    return [nome for nome, f in PEZZI if not os.path.exists(os.path.join(RADICE, f))]


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
        globals()["PEZZI"] = (("il pezzo finto", "non/esisto/affatto.py"),)
        b, m = decidi("aaaaaaaa", None)
        esito("### (1) c'e' lavoro PRONTO: BLOCCA, e NOMINA il pezzo",
              b and "il pezzo finto" in m, "### %r" % m[:60])
        # ### (2) NIENTE PRONTO -> LASCIA FERMARE
        globals()["PEZZI"] = (("un pezzo fatto", "CLAUDE.md"),)
        b2, m2 = decidi("aaaaaaaa", None)
        esito("### (2) la coda NON ha pezzi pronti: LASCIA FERMARE",
              not b2, "### %r" % m2[:60])
        # ### (3) GIA' BLOCCATO, NESSUN COMMIT NUOVO -> LASCIA FERMARE
        globals()["PEZZI"] = (("il pezzo finto", "non/esisto/affatto.py"),)
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
    male = [f for _n, f in PEZZI if os.path.isabs(f) or not _n.strip()]
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
