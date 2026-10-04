# -*- coding: utf-8 -*-
"""IL CENSIMENTO DI `MITOSI_2LAM` — ogni sito, e di che TIPO e'.

### **Serve a un cancello del commit `6b`:** il mandato elenca i siti attesi e dice *«se il
tuo censimento ne trova altri: FERMATI e dillo»*. ### **Quindi il confronto lo fa LA
MACCHINA**, non io a occhio — ed e' la lezione del censimento del `6a`, dove il conteggio
iniziale a memoria era sbagliato in entrambe le direzioni.

## LE TRE CLASSI, e distinguerle E' il lavoro

| | |
|---|---|
| ### **`CODICE`** | un riferimento che l'### **AST** vede: una lettura, un'assegnazione, un `global`. ### **Sono questi che cambiano il comportamento** |
| `COMMENTO` | il nome dentro un commento. ### **Non cambia niente a runtime, MA PUO' MENTIRE** -- e in questo repo i commenti sono stati scaduti piu' volte (`doc/FATTI_dal_codice.md`) |
| `STRINGA` | il nome dentro un letterale: il testo del CLI, un messaggio di stdout, una chiave |

### ⛔ **PERCHE' LE TRE CLASSI E NON SOLO IL CODICE:** il mandato chiede di fermarsi se
compaiono siti ### **non previsti**, e un commento che ### **asserisce la legge** e' un sito
che va curato come il codice. ### **Un censimento che guardasse solo l'AST direbbe
*<<nessun altro sito>>* mentre un commento continua a dire il contrario della legge** --
### **un `FALSO-ZERO` prodotto dallo strumento, non dal mondo.**

### ⚠ **E UN SITO PUO' ESSERE *ATTESO MA ASSENTE*:** il mandato elenca il blocco
`[flag-inerti]` fra i siti, ### **ma li' oggi il nome NON compare** -- e' il posto dove il
`6b` deve ### **aggiungerlo**. ### **Lo strumento lo riporta come `ATTESO-ASSENTE`, perche'
<<non trovato>> e <<non previsto>> sono due cose diverse.**

**COMANDO:** `python csv/_test_fork/_censimento_mitosi_2lam.py`
**USCITA:** `csv/_test_fork/_censimento_mitosi_2lam/`
"""
import ast
import hashlib
import io
import json
import os
import sys
import tokenize

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_censimento_mitosi_2lam")
NL = chr(10)
NOME = "MITOSI_2LAM"
CLI = "--mitosi-2lam"
ATTR = "mitosi_2lam"

# ### LA LISTA DEL MANDATO, scritta qui perche' il confronto lo faccia LA MACCHINA.
#   ### Le righe sono quelle del blob `c18c9bf6`: se il file in esame e' un altro blob, il
#   confronto PER RIGA non si rifa' -- e' la lezione di `208378b`, dove un artefatto di un
#   altro blob e' stato citato come se fosse quello in esame (`FALSO-UNO`).
BLOB_DEL_MANDATO = "c18c9bf6"
ATTESE_SIM = {
    457: "il DEFAULT del flag",
    8465: "IL CANCELLO -- e' il sito che il 6b rende INCONDIZIONATO",
    10636: "la `global` in `_applica_flag`",
    10731: "l'assegnazione dal CLI in `_applica_flag`",
    10732: "il `if MITOSI_2LAM:` che stampa l'avviso [cura5]",
    10733: "il testo dell'avviso [cura5]",
    11691: "il `p.add_argument` del CLI",
}
ATTESI_ALTROVE = (
    "csv/_test_fork/_scena_video.py",
    "csv/_cure_verificate.py",
    "csv/_presidio_commenti_flag.py",
)
# ### UN SITO ATTESO CHE OGGI NON ESISTE: il posto dove il `6b` deve METTERE la
#   dichiarazione di inerzia. ### Non trovarlo NON e' un difetto: e' il lavoro da fare.
ATTESI_ASSENTI = {
    "blocco [flag-inerti]": "il `6b` deve aggiungere `MITOSI_2LAM` fra i flag inerti, "
                            "come `PAV_COM`",
}


def che_cos_e(percorso):
    """### UN REPERTO O UNO STRUMENTO? ### **La domanda che il primo perimetro non si
    poneva**, e che gli ha fatto dichiarare ### **142 siti nuovi** dove non ce n'era
    nessuno.

    ### \u26d4 IL DIFETTO MISURATO: `os.walk` su `csv/` raccoglie anche le
    ### **COPIE DEL SIMULATORE** salvate accanto ai sigilli *(par.7, stato 2)* e gli
    ### **STUB generati** sotto `_tmp/`. Quelle copie contengono il flag ### **per
    costruzione**: sono fotografie del simulatore, non posti dove qualcuno lo usa.
    ### **Contarle come <<siti non previsti>> trasforma un archivio in un allarme.**

    | classe | come si riconosce | che cos'e' |
    |---|---|---|
    | `COPIA-SIMULATORE` | definisce ### **a livello di modulo** il default `MITOSI_2LAM`
      ### **E** contiene il sito del CLI `--mitosi-2lam` | un ### **REPERTO** |
    | `STUB-DI-RUN` | sta sotto una cartella `_tmp/` | un ### **REPERTO** |
    | `STRUMENTO` | tutto il resto | ### **un SITO, e va guardato** |

    ### \u2705 **IL MARCATORE E' STRUTTURALE E LEGATO ALLA COSA CENSITA: solo il
    simulatore definisce SIA il default SIA il CLI.** ### \u26a0 Il primo marcatore che
    avevo provato -- *<<definisce `decidi_divisione`>>* -- ne riconosceva ### **30 su
    46**, perche' nei blob piu' vecchi quella funzione ha un ### **altro nome**: un
    marcatore che dipende da un nome di funzione ### **non e' stabile fra blob**, e qui si
    confrontano blob di settimane diverse.
    """
    if (chr(47) + "_tmp" + chr(47)) in percorso.replace(chr(92), chr(47)):
        return "STUB-DI-RUN"
    try:
        a = ast.parse(io.open(percorso, encoding="utf-8").read())
    except (SyntaxError, OSError, UnicodeDecodeError):
        return "STRUMENTO"
    default = any(isinstance(n, ast.Assign)
                  and any(isinstance(x, ast.Name) and x.id == NOME
                          for x in n.targets)
                  for n in a.body)
    cli = any(isinstance(n, ast.Constant) and n.value == CLI for n in ast.walk(a))
    return "COPIA-SIMULATORE" if (default and cli) else "STRUMENTO"


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def siti_di_codice(sorgente):
    """### I riferimenti che l'AST VEDE: `Name`, `global`, e l'attributo del CLI."""
    a = ast.parse(sorgente)
    fuori = []
    for n in ast.walk(a):
        if isinstance(n, ast.Name) and n.id == NOME:
            come = ("assegnazione" if isinstance(n.ctx, ast.Store) else
                    "cancellazione" if isinstance(n.ctx, ast.Del) else "lettura")
            fuori.append({"riga": n.lineno, "classe": "CODICE", "come": come})
        elif isinstance(n, ast.Global) and NOME in n.names:
            fuori.append({"riga": n.lineno, "classe": "CODICE", "come": "global"})
        elif isinstance(n, ast.Attribute) and n.attr == ATTR:
            fuori.append({"riga": n.lineno, "classe": "CODICE",
                          "come": "attributo `%s`" % ATTR})
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            if n.value == ATTR or n.value == CLI:
                fuori.append({"riga": n.lineno, "classe": "CODICE",
                              "come": "stringa-chiave `%s`" % n.value})
    return fuori


def siti_di_testo(percorso):
    """### I COMMENTI e le STRINGHE che nominano il flag, via `tokenize`.

    ### L'AST ### **non vede i commenti**: un censimento fatto col solo AST direbbe
    *<<nessun altro sito>>* mentre un commento continua ad asserire il contrario della legge.
    """
    fuori = []
    with io.open(percorso, "rb") as f:
        try:
            for tok in tokenize.tokenize(f.readline):
                if tok.type == tokenize.COMMENT and (NOME in tok.string
                                                     or CLI in tok.string):
                    fuori.append({"riga": tok.start[0], "classe": "COMMENTO",
                                  "come": "commento"})
                elif tok.type == tokenize.STRING and (NOME in tok.string
                                                      or CLI in tok.string):
                    fuori.append({"riga": tok.start[0], "classe": "STRINGA",
                                  "come": "letterale o docstring"})
        except (tokenize.TokenError, IndentationError, SyntaxError) as e:
            fuori.append({"riga": 0, "classe": "STRINGA",
                          "come": "NON TOKENIZZABILE: %s" % e})
    return fuori


def raccogli(percorso, righe_sorgente):
    s = io.open(percorso, encoding="utf-8").read()
    v = []
    try:
        v += siti_di_codice(s)
    except SyntaxError as e:
        v.append({"riga": 0, "classe": "CODICE", "come": "NON PARSABILE: %s" % e})
    v += siti_di_testo(percorso)
    # ### UNA RIGA PUO' AVERE PIU' RIFERIMENTI: non si deduplica per riga, si deduplica
    #   per (riga, classe, come) -- altrimenti `:10733` *(stringa dentro un print)* e il
    #   `if` che la precede si confonderebbero.
    visti = set()
    fuori = []
    for x in sorted(v, key=lambda y: (y["riga"], y["classe"], y["come"])):
        k = (x["riga"], x["classe"], x["come"])
        if k in visti:
            continue
        visti.add(k)
        x["testo"] = (righe_sorgente[x["riga"] - 1].strip()[:120]
                      if 0 < x["riga"] <= len(righe_sorgente) else "?")
        fuori.append(x)
    return fuori


def principale():
    out = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        out.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    b = blob(SIM)
    stampa("=" * 100)
    stampa("IL CENSIMENTO DI `%s` -- ogni sito, e di che TIPO e'" % NOME)
    stampa("=" * 100)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % b[:8])
    stampa("  strumento ... %s" % blob(os.path.abspath(__file__))[:8])
    stampa("  il setaccio: l'AST per il CODICE, `tokenize` per COMMENTI e STRINGHE.")
    stampa("  ### L'AST NON VEDE I COMMENTI: con il solo AST questo censimento direbbe")
    stampa("  ###   <<nessun altro sito>> mentre un commento continua ad asserire il")
    stampa("  ###   contrario della legge. ### Sarebbe un FALSO-ZERO dello STRUMENTO.")
    stampa("")

    righe = io.open(SIM, encoding="utf-8").read().split(NL)
    nel_sim = raccogli(SIM, righe)
    stampa("-" * 100)
    stampa("NEL SIMULATORE: %d riferimenti" % len(nel_sim))
    stampa("    %-7s %-9s %-24s %s" % ("riga", "classe", "come", "testo"))
    for x in nel_sim:
        stampa("    :%-6d %-9s %-24s %s"
               % (x["riga"], x["classe"], x["come"][:24], x["testo"][:60]))
    stampa("")

    # ---- il confronto con la lista del mandato, FATTO DALLA MACCHINA
    stampa("-" * 100)
    stampa("IL CONFRONTO CON LA LISTA DEL MANDATO (il guardiano, blob %s)"
           % BLOB_DEL_MANDATO)
    if not b.startswith(BLOB_DEL_MANDATO):
        stampa("  ### IL CONFRONTO PER RIGA NON SI RIFA', ED E' UN LIMITE DICHIARATO.")
        stampa("  ###   la lista si riferisce al blob .. %s" % BLOB_DEL_MANDATO)
        stampa("  ###   il file in esame e' ............ %s" % b[:8])
        stampa("  ###   Confrontare righe fra due blob diversi produce rumore, non una")
        stampa("  ###   misura: e' il difetto FALSO-UNO, caso 1.")
        esito_confronto = {"rifatto": False}
    else:
        mie_cod = sorted(set(x["riga"] for x in nel_sim if x["classe"] == "CODICE"))
        sue = sorted(ATTESE_SIM)
        solo_mie = [r for r in mie_cod if r not in sue]
        solo_sue = [r for r in sue if r not in mie_cod]
        stampa("  righe di CODICE nella MIA lista .. %d  %s" % (len(mie_cod), mie_cod))
        stampa("  righe nella SUA lista ............ %d  %s" % (len(sue), sue))
        stampa("")
        stampa("  SOLO NELLA MIA (codice NON previsto): %d" % len(solo_mie))
        for r in solo_mie:
            x = [y for y in nel_sim if y["riga"] == r and y["classe"] == "CODICE"][0]
            stampa("      :%-6d %-24s %s" % (r, x["come"][:24], x["testo"][:60]))
        stampa("  SOLO NELLA SUA (previsto e NON trovato): %d" % len(solo_sue))
        for r in solo_sue:
            stampa("      :%-6d %s" % (r, ATTESE_SIM[r]))
        stampa("")
        # ### I COMMENTI E LE STRINGHE, separati: non sono codice, ma POSSONO MENTIRE.
        testo = [x for x in nel_sim if x["classe"] != "CODICE"]
        fuori_lista = [x for x in testo if x["riga"] not in ATTESE_SIM]
        stampa("  COMMENTI e STRINGHE fuori dalla lista del mandato: %d"
               % len(fuori_lista))
        for x in fuori_lista:
            stampa("      :%-6d %-9s %s" % (x["riga"], x["classe"], x["testo"][:70]))
        stampa("  ### NON sono CODICE, quindi NON fanno scattare lo STOP del mandato.")
        stampa("  ### MA VANNO GUARDATI UNO PER UNO: un commento che ASSERISCE la legge")
        stampa("  ###   sotto condizione del flag diventa FALSO il giorno della cura.")
        esito_confronto = {"rifatto": True, "solo_mie_codice": solo_mie,
                           "solo_sue": solo_sue,
                           "testo_fuori_lista": [x["riga"] for x in fuori_lista]}
        if solo_mie:
            stampa("")
            stampa("### *** %d SITI DI CODICE NON PREVISTI: IL CENSIMENTO SI FERMA. ***"
                   % len(solo_mie))
            stampa("###   Il mandato dice: <<se il tuo censimento ne trova altri, FERMATI")
            stampa("###   e dillo>>. Non si prosegue col codice.")
    stampa("")

    # ---- fuori dal simulatore
    stampa("-" * 100)
    stampa("FUORI DAL SIMULATORE: solo gli STRUMENTI, non i REPERTI")
    stampa("  ### Le COPIE DEL SIMULATORE salvate accanto ai sigilli e gli STUB")
    stampa("  ###   sotto `_tmp/` contengono il flag PER COSTRUZIONE: sono")
    stampa("  ###   fotografie, non posti dove qualcuno lo usa. Si CONTANO e si")
    stampa("  ###   DICHIARANO, ma non sono siti.")
    altrove = {}
    reperti = {}
    for base, _d, files in os.walk(os.path.join(RADICE, "csv")):
        if "_archivio" in base or "__pycache__" in base:
            continue
        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            pf = os.path.join(base, f)
            try:
                s = io.open(pf, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            if NOME not in s and CLI not in s:
                continue
            rel = os.path.relpath(pf, RADICE).replace(chr(92), "/")
            # ### SI CLASSIFICA PRIMA DI CONTARE: un reperto non e' un sito.
            tipo = che_cos_e(pf)
            reperti.setdefault(tipo, []).append(rel)
            if tipo != "STRUMENTO":
                continue
            v = raccogli(pf, s.split(NL))
            altrove[rel] = v
            stampa("  %s -- %d riferimenti (%s)"
                   % (rel, len(v),
                      ", ".join(sorted(set(x["classe"] for x in v)))))
            for x in v:
                stampa("      :%-6d %-9s %s" % (x["riga"], x["classe"], x["testo"][:70]))
    stampa("")
    stampa("  I REPERTI, contati e non confusi coi siti:")
    for _k in sorted(reperti):
        stampa("    %-18s %d file" % (_k, len(reperti[_k])))
    non_previsti = sorted(k for k in altrove if k not in ATTESI_ALTROVE)
    previsti_assenti = sorted(k for k in ATTESI_ALTROVE if k not in altrove)
    stampa("")
    stampa("  file ATTESI dal mandato ......... %d  %s"
           % (len(ATTESI_ALTROVE), list(ATTESI_ALTROVE)))
    stampa("  file NON PREVISTI che lo nominano %d  %s" % (len(non_previsti),
                                                           non_previsti or "nessuno"))
    stampa("  file previsti e NON trovati ..... %d  %s" % (len(previsti_assenti),
                                                           previsti_assenti or "nessuno"))
    stampa("")

    # ---- i siti ATTESI MA ASSENTI
    stampa("-" * 100)
    stampa("I SITI `ATTESO-ASSENTE` -- previsti dal mandato e oggi INESISTENTI")
    stampa("  ### <<non trovato>> e <<non previsto>> sono DUE COSE DIVERSE, e confonderle")
    stampa("  ###   farebbe sembrare un lavoro da fare un difetto del censimento.")
    for k, v in sorted(ATTESI_ASSENTI.items()):
        stampa("  %-24s %s" % (k, v))
    stampa("")

    esito = {"blob_sim": b, "blob_strumento": blob(os.path.abspath(__file__)),
             "nel_simulatore": nel_sim, "altrove": altrove,
             "confronto": esito_confronto,
             "attesi_altrove": list(ATTESI_ALTROVE),
             "altrove_non_previsti": non_previsti,
             "altrove_previsti_assenti": previsti_assenti,
             "attesi_assenti": ATTESI_ASSENTI,
             "reperti": {k: sorted(v) for k, v in reperti.items()},
             "codice": len([x for x in nel_sim if x["classe"] == "CODICE"]),
             "commenti": len([x for x in nel_sim if x["classe"] == "COMMENTO"]),
             "stringhe": len([x for x in nel_sim if x["classe"] == "STRINGA"])}
    stampa("=" * 100)
    stampa("### IL RIEPILOGO")
    stampa("###   nel simulatore: %d CODICE, %d COMMENTO, %d STRINGA"
           % (esito["codice"], esito["commenti"], esito["stringhe"]))
    stampa("###   file di csv/ che lo nominano: %d" % len(altrove))
    _stop = bool(esito_confronto.get("solo_mie_codice")) or bool(non_previsti)
    stampa("###   %s" % ("*** SI FERMA: ci sono siti non previsti. ***" if _stop
                         else "nessun sito di CODICE non previsto: si prosegue."))
    stampa("=" * 100)
    esito["si_ferma"] = _stop

    io.open(os.path.join(FUORI, "_censimento.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(out) + NL)
    print("  referto .. %s" % FUORI)
    return 1 if _stop else 0


if __name__ == "__main__":
    sys.exit(principale())
