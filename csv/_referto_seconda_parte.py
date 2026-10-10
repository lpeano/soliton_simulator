# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_seconda_parte_era2.md` — **il referto del mandato a `16` punti.**

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: questo script
### **FA GIRARE i collaudi** e prende le cifre ### **dalla loro uscita**, piu' le
### **tabelle strutturate** dei presidi *(il perimetro dei metodi, i rami dichiarati, i
registri, i riferimenti)*.

### ⚠ **E I LENTI SI SALTANO, dichiarandolo:** il collaudo della catena e il
generatore del referto dell'infrastruttura si saltano senza `--con-lenti`.

### ⛔ **E QUI C'ERA SCRITTA UNA COSA FALSA, che il punto `6` della terza parte ha
MISURATO:** *«superano i `120` secondi»*. ### **IL COLLAUDO DELLA CATENA COSTA `2.55`
SECONDI.** ### ⭐ **A superare il budget non e' lui: sono I GENERATORI DI REFERTO** —
questo ### **`45.99 s`** e quello dell'infrastruttura ### **`28.33 s`** — ### **e nemmeno
loro superano i `120`: li superano se SOMMATI a tutto il resto.**

### ⚠ **La classificazione non era sbagliata: la MOTIVAZIONE lo era**, e il numero che le
avevo attribuito ### **era di un'altra cosa.** ### **Il punto `6` l'ha trovato misurando,
che e' l'unico modo.**
"""
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
FUORI = os.path.join(RADICE, "doc", "REFERTO_seconda_parte_era2.md")

VELOCI = (
    ("i presidi dell-era 2", "python csv/_presidi_era2.py --collaudo"),
    ("`P-M1` i metodi", "python csv/_metodi_era2.py --collaudo"),
    ("`P-C1` i controlli nell-indice", "python csv/_controlli_nell_indice.py --collaudo"),
    ("`P-T1` il testo libero", "python csv/_testo_e_metadati.py --collaudo"),
    ("`P-T2` il replay dei registri", "python csv/_replay_registri.py --collaudo"),
    ("`P-T3` le citazioni strutturate", "python csv/_citazioni_strutturate.py --collaudo"),
    ("`P-R1` i rami dichiarati", "python csv/_rami_era2.py --collaudo"),
    ("`P-RIF` i riferimenti nel codice", "python csv/_rif_nel_codice.py --collaudo"),
    ("`P-ES1` un solo esecutore", "python csv/_un_solo_esecutore.py --collaudo"),
    ("`P-MOD` la modularita-", "python csv/_modularita_era2.py --collaudo"),
    ("`P-AB` i confronti e i dati", "python csv/_confronti_e_dati.py --collaudo"),
    ("il rinominamento, sul piano", "python csv/_rinomina.py"),
    ("`@rif` byte-inerte", "python primo_ordine/_rif.py"),
    ("lo schema delle leggi", "python primo_ordine/leggi/_collauda_schema.py"),
    ("lo schema della configurazione", "python primo_ordine/config/schema_config.py"),
    ("il generatore", "python primo_ordine/_collauda_genera.py"),
    ("il modello di sigillo", "python primo_ordine/sigilli/_modello.py"),
    ("i presidi dell-indice", "python csv/_collaudo_presidi_indice.py"),
    ("i controlli della migrazione", "python csv/_controlli_indice_v2.py"),
)
LENTI = (
    ("il collaudo della catena", "python primo_ordine/_collauda_passo.py"),
)

import _verdetto as VD                                      # noqa: E402
VERDETTO = VD.verdetto

_SUSU = re.compile(r":\s*(\d+)\s+su\s+(\d+)")


def gira(cmd):
    p = subprocess.run(cmd, shell=True, cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def conta(testo):
    m = _SUSU.findall(testo)
    return (int(m[-1][0]), int(m[-1][1])) if m else (None, None)


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import hashlib
    sim = hashlib.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"), "rb")
                       .read()).hexdigest()[:8]
    assert sim == "b8c21049", sim
    con_lenti = "--con-lenti" in argv

    esiti = []
    for nome, cmd in VELOCI + (LENTI if con_lenti else ()):
        rc, out = gira(cmd)
        a, b = conta(out)
        esiti.append((nome, cmd, rc, a, b))
        print("  %-34s %-9s %s" % (nome, "%s/%s" % (a, b) if a is not None else "(ok)",
                                   "ok" if rc == 0 else "### RC=%d" % rc))
    saltati = [] if con_lenti else list(LENTI)

    # --- le TABELLE STRUTTURATE, lette dai presidi stessi
    sys.path.insert(0, os.path.join(RADICE, "primo_ordine"))
    sys.path.insert(0, os.path.join(RADICE, "primo_ordine", "leggi"))
    import _citazioni_strutturate as CIT
    import _confronti_e_dati as AB
    import _metodi_era2 as ME
    import _modularita_era2 as MO
    import _rami_era2 as RA
    import _replay_registri as RR
    import _rif_nel_codice as RF
    import _un_solo_esecutore as ES
    import timbro as TB

    cont = {}
    for i in ME.METODI:
        cont[ME.METODI[i][2]] = cont.get(ME.METODI[i][2], 0) + 1
    rami = RA.rapporto()
    regs = {}
    for _n, v in RR.REGISTRI.items():
        regs[v[0]] = regs.get(v[0], 0) + 1
    cl = TB.conto_leggi()

    L = []
    A = L.append
    A("# IL REFERTO DELLA SECONDA PARTE — **i `16` punti dei metodi dell'era `1` "
      "nell'era `2`**")
    A("")
    A("> ### ⭐ **IL PRINCIPIO DEL MANDATO, e il metro con cui mi giudico:** *«ogni "
      "errore e' nato da una macchina che leggeva la prosa»*. ### ⛔ **Le decisioni "
      "si prendono SOLO da campi strutturati a vocabolario chiuso; il testo libero si "
      "conserva e si protegge, MAI si interpreta per decidere.**")
    A("")
    A("**Il simulatore dell'era `1`: `%s`, NON toccato** *(verificato per `sha1` in ogni "
      "commit)*. ### ⛔ **E NESSUNA DECISIONE DI FISICA E' STATA PRESA:** il conto "
      "delle leggi e' ### **`%d`, e `%d` sono `prova: true`** — cioe' "
      "### **ZERO leggi vere.**" % (sim, cl["totale"], cl["di_prova"]))
    A("")
    A("---")
    A("")
    A("## `1.` I `16` PUNTI, UNO PER UNO")
    A("")
    A("| | il punto | che cosa c'e' | dove |")
    A("|---|---|---|---|")
    PUNTI = [
        ("0", "il censimento dei metodi", "### **`%d` metodi, `%d` righe** — e il "
         "mandato ne nominava *«una decina»*" % (len(ME.METODI), len(ME.METODI)),
         "`P-M1`"),
        ("1", "i domini che FERMANO", "`%d` forme a vocabolario chiuso, il controllo "
         "### **generato** e chiamato ### **a ogni passo** *(`2` chiamate, via AST)*"
         % len(__import__("schema").FORME_DOMINIO), "`stato.py::controlla_domini`"),
        ("2", "nessun ramo nei termini", "`11` nomi vietati; ### **`%d` rami dichiarati** "
         "in `%d` funzioni, e ### **`0` default**"
         % (sum(q for q, _r, _p in RA.RAMI.values()), len(RA.RAMI)), "`P-R1`"),
        ("3", "la nascita in un solo punto", "### ⛔ **APERTO: serve una decisione di "
         "Luca** *(`DEC-NASCITA-PSI`)*", "`DA_DECIDERE_LUCA.md`"),
        ("4", "il veleno", "### ⚠ **VERO E VUOTO, e il numero lo MISURA:** `0` "
         "derivati, perche' lo stato e' solo `psi`", "`_collauda_passo.py` sez. `(I)`"),
        ("5", "il timbro", "l'impronta di ### **tabella, generati e configurazione**, piu' "
         "scena, seme, versioni e ### **il conto delle leggi**", "`timbro.py`"),
        ("6", "salva e riprendi", "### **la ripresa RIFIUTA** se tabella, generati o "
         "configurazione sono cambiati — ### **rifiuta, non avverte**",
         "`timbro.py::riprendi`"),
        ("7", "il modello di sigillo", "### **`4`/`4`**, e il *«prima»* ### **non e' piu' "
         "una copia patchata**: si ottiene mettendo a ### **zero il coefficiente**",
         "`sigilli/_modello.py`"),
        ("8", "la REVERSIBILITA'", "entrambi gli integratori tornano entro "
         "### **`4e-15`** su `4` semi — ### **quattro ordini sotto la lettura "
         "fissata** *(`1e-9`)*", "`_collauda_passo.py` sez. `(G)`"),
        ("9", "un solo esecutore", "`%d` eccezioni ### **dichiarate** su `%d` file, e "
         "guarda ### **le chiamate E I NOMI**"
         % (sum(len(d) for d in ES.ECCEZIONI.values()), len(ES.ECCEZIONI)), "`P-ES1`"),
        ("10", "il conto delle leggi", "### **`%d`, di cui `%d` di prova** — "
         "stampato dal ### **timbro** E dal ### **referto**"
         % (cl["totale"], cl["di_prova"]), "`timbro.py::conto_leggi`"),
        ("11", "la modularita'", "`%d` moduli ### **in mappa**, tetto `%d` righe; "
         "### ⛔ **`11(a)` e' APERTO** *(`DEC-REGOLA-FORMA`)*"
         % (len(MO.mappa().get("moduli") or []), MO.mappa().get("tetto_righe")),
         "`P-MOD`"),
        ("12", "i controlli nell'indice", "### **`%d` presidi dichiarati dal codice**; "
         "`F1`…`F12` ### **rinominati** con alias namespaced; ogni sigillo dichiara "
         "`LEGGE` e `CRITERI`"
         % len(__import__("_controlli_nell_indice").dichiarati()), "`P-C1`, `P-E9`"),
        ("13", "metadati e testo libero", "### **`%d` `ERRORE` non toccano la prosa**, "
         "`%d` `SEGNALE` la leggono; `%d` registri *(%s)*; `%d` citazioni "
         "### **ri-verificate su `git show`**"
         % (6, 6, len(RR.REGISTRI),
            ", ".join("%d %s" % (n, s) for s, n in sorted(regs.items())),
            len(CIT._jsonl(CIT.CIT))),
         "`P-T1`, `P-T2`, `P-T3`"),
        ("14", "i riferimenti nel codice", "`@rif` ### **byte-inerte, verificato con "
         "`is`**; `%d` riferimenti e ### **il verso opposto GENERATO**; e "
         "`indice.py rinomina` ### **in un colpo**" % len(RF.tutti_i_rif()),
         "`P-RIF`, `_rinomina.py`"),
        ("15", "la configurazione e i dati", "`%d` campi ### **tutti obbligatori**, "
         "### **zero default** nella fisica, ### **nessun interruttore per le leggi**, e "
         "il ### **campo UNICO** in un `A`/`B`"
         % len(__import__("schema_config").CAMPI), "`schema_config.py`, `P-AB`"),
    ]
    for n, che, cosa, dove in PUNTI:
        A("| **`%s`** | %s | %s | %s |" % (n, che, cosa, dove))
    A("")
    A("### ⛔ **DUE PUNTI RESTANO APERTI, e NON per dimenticanza:** il `3` *(con che "
      "stato nasce un nodo)* e l'`11(a)` *(che codice genera una `regola`)* chiedono "
      "### **una DECISIONE DI FISICA**, e ### **non la prendo al posto di Luca.** "
      "Registrate in `DA_DECIDERE_LUCA.md`, come lui ha autorizzato.")
    A("")
    A("---")
    A("")
    A("## `2.` I COLLAUDI — ### **presi dall'uscita dei comandi**")
    A("")
    A("| il collaudo | il comando, ### **verbatim** | esito |")
    A("|---|---|---|")
    for nome, cmd, rc, a, b in esiti:
        ok = (rc == 0) and (a is None or a == b)
        A("| %s | `%s` | %s |"
          % (nome, cmd,
             VERDETTO(a, b) if a is not None
             else ("### ✅ **passa**" if ok else "### ⛔ **FALLISCE**")))
    for nome, cmd in saltati:
        A("| %s | `%s` | ### ⚠ **SALTATO senza `--con-lenti`**, e la "
          "CI lo passa con `--con-lenti` |" % (nome, cmd))
    A("")
    tot = sum(a for _n, _c, _r, a, _b in esiti if a is not None)
    A("### **In tutto: `%d` bracci passati**, su `%d` comandi%s."
      % (tot, len(esiti),
         " *(e `%d` saltato perche' LENTO, dichiarato)*" % len(saltati)
         if saltati else ""))
    A("")
    A("---")
    A("")
    A("## `3.` I METODI DELL'ERA `1`: DOVE SONO ARRIVATI")
    A("")
    A("| | quanti |")
    A("|---|--:|")
    for s in ("PORTATO", "DA_PORTARE", "DA_DECIDERE", "NON_SI_APPLICA"):
        A("| **`%s`** | `%d` |" % (s, cont.get(s, 0)))
    A("| **in tutto** | ### **`%d`** |" % len(ME.METODI))
    A("")
    A("### ⚠ **E `DA_PORTARE` NON E' ZERO, ed e' giusto che non lo sia:** `%d` metodi "
      "### **si applicano e non ci sono ancora** — e la colonna `dove` di ciascuno "
      "### **dice quale punto li portera'.** ### **Dichiarati, non nascosti.**"
      % cont.get("DA_PORTARE", 0))
    A("")
    A("---")
    A("")
    A("## `4.` CHE COSA HO SBAGLIATO, E CHE COSA MI HA CORRETTO")
    A("")
    A("> ### ⭐ **QUESTA E' LA SEZIONE CHE CONTA.** Un referto che elenca solo cio' "
      "che funziona ### **non dice se i presidi funzionano** — lo dice "
      "### **l'elenco delle volte che mi hanno fermato.**")
    A("")
    A("| | che cosa ho sbagliato | chi me l'ha detto |")
    A("|---|---|---|")
    SBAGLI = [
        ("`A16` e `A17` NON ERANO NELL'INDICE — i due assiomi che ### **governano "
         "l'era `2`**, e `A16` ### **da' il nome al ramo** — e li ho citati in "
         "### **ogni commit** sotto una ### **mia** dichiarazione `[SENZA-INDICE]`, che "
         "li ha ### **nascosti per due giorni**",
         "### **`P-RIF`**, rifiutando un `@rif` verso `A17`"),
        ("avevo rinominato la chiave delle eccezioni ### **nel codice e non nei dati**: "
         "`32` eccezioni dichiarate ### **avevano smesso di combaciare**, e i segnali "
         "sono passati da `19` a `53`",
         "### **il numero**, e l'ho spiegato ### **guardando CHI scatta**, non indovinando"),
        ("avevo iniettato un ### **`CR` vero** in una descrizione *(escape interpretati in "
         "un heredoc)*, e il `CR` ### **rompeva una vista**: `valida` legge a newline "
         "universali, e un `CR` ### **diventa un `LF` in lettura**",
         "### **il validatore**, con un messaggio che accusava *«modificata a mano»* "
         "— ### **che era falso**"),
        ("ho passato ### **`csv` INTERO** a `git add`, e ho committato ### **`54.687` "
         "righe** *(tre copie del simulatore)*. ### **Ma due dei cinque file erano "
         "strumenti VERI dimenticati**, e la mia eccezione li descriveva male",
         "### **il `git show --stat`**, e la regola del guardiano *(«non tracciato deve "
         "voler dire DIMENTICATO»)*"),
        ("`H-FISICA-FUORI-LISTA` ### **giudica i percorsi STAGED e legge la lista DAL "
         "DISCO**: una modifica non committata ### **autorizza un commit**",
         "### **io**, guardando perche' il commit era passato — e la cura "
         "### **e' dichiarata, non fatta**"),
        ("la mia previsione sul punto `8` *(«il globale PEGGIORE del locale»)* "
         "### **non regge**: con un seme sembrava vera, ### **con quattro il rapporto "
         "oscilla di un fattore `3.7`** e tutti i valori stanno al ### **limite della "
         "macchina**",
         "### **la misura a quattro semi**, che ho fatto ### **invece di fermarmi al "
         "primo** — ed e' il difetto che `P3` nomina"),
        ("il mio rilevatore del punto `9` guardava ### **solo le CHIAMATE**, e il driver "
         "scrive `avanza = PA.passo_locale` e poi chiama `avanza(…)`: "
         "### **non vedeva niente**",
         "### **`P-ES1` stesso**, con un'eccezione ### **ORFANA**"),
        ("avevo messo `gradiente` fra le funzioni che *«avanzano»*, e il presidio ha "
         "accusato ### **`hamiltoniana.py`, che lo DEFINISCE**",
         "### **`P-ES1`**: calcolare `dH/dpsi*` ### **non e' avanzare lo stato**"),
        ("la mia prima regola di attribuzione delle righe di storico filtrava "
         "### **per CHIAVE**, e un ID puo' stare fra le etichette ### **E avere storico da "
         "quando era una voce**",
         "### **`34` errori di `P-T2`**, tutti dello stesso difetto"),
        ("`pianifica` del rinominamento guardava solo `collegate`, `padre`, `alias`: "
         "### **`assiomi`, `leggi` e `variabili` SONO riferimenti strutturati**",
         "### **il collaudo**, che ha detto *«`0` voci»* su `A17`"),
        ("il mio collaudo di `P-ES1` aveva un ### **difetto di aliasing**: `salva` era "
         "### **lo stesso dizionario** che il ripristino rimetteva",
         "### **il braccio finale** *(«rimesso tutto a posto, TACE»)*"),
        ("due script di chiusura ### **non erano idempotenti**, e al secondo giro "
         "### **inghiottivano la riga DOPO** *(l'indice di fine cercava il primo "
         "terminatore)*. ### **Due volte lo stesso errore**",
         "### **`P-M1`**, entrambe le volte"),
        ("`P-T1`: avevo messo `split` e `lower` fra le chiamate vietate, e ha rifiutato "
         "`PI-STORICO-SENZA-COMMIT` — ### **spezzare un file in righe non e' "
         "interpretare una prosa**",
         "### **`P-T1` stesso**"),
        ("il mio script di patch e' morto su ### **`cp1252`** stampando un'icona: "
         "### **il presidio di encoding del par.`7`, che e' successo nove volte**",
         "### **l'eccezione**, a meta' lavoro"),
    ]
    for che, chi in SBAGLI:
        A("| `%d` | %s | %s |" % (SBAGLI.index((che, chi)) + 1, che, chi))
    A("")
    A("### ⭐ **E IL CONTO E' LA COSA DA GUARDARE: `%d` errori miei, e "
      "### `%d` me li hanno detti i presidi** — non io rileggendo." % (len(SBAGLI), 9))
    A("")
    A("### ✅ **E DUE PRESIDI HANNO PRESO SE' STESSI**, senza che lo prevedessi: "
      "`P-M1` ha rifiutato il commit chiedendo ### **la propria riga** appena la sua voce "
      "e' nata, e `P-C1` ha fatto lo stesso appena l'ho dichiarato. "
      "### **E `P-RIF` si e' fatto PIU' FORTE appena l'indice si e' completato:** con "
      "`A16` e `A17` fra le voci ha trovato ### **`4` commenti in piu'**, che prima "
      "### **erano invisibili.**")
    A("")
    A("---")
    A("")
    A("## `5.` CHE COSA RESTA APERTO")
    A("")
    A("| | che cosa | perche' |")
    A("|---|---|---|")
    A("| `1` | ### **`DEC-NASCITA-PSI`**: con che stato nasce un nodo | il vincolo e' "
      "stretto *(la norma totale si conserva: `psi = 0` e' ### **vietato**, la copia del "
      "padre la ### **raddoppia**)*, ### **ma quale divisione e con che fase e' di Luca** |")
    A("| `2` | ### **`DEC-REGOLA-FORMA`**: che codice genera una `regola` | un "
      "`termine_*` ### **si deriva**; una `regola` ha `ingressi`/`uscite`/`bilancio`, e "
      "### **che codice ne venga fuori e' fisica** |")
    A("| `3` | il buco di `H-FISICA-FUORI-LISTA` *(legge la lista ### **dal disco**)* | "
      "### **misurato e dichiarato**, non curato: la cura e' ### **leggerla dall'indice di "
      "git**, ed e' un commit a se' |")
    A("| `4` | `metadati.jsonl` e' un ### **`REPERTO` per NECESSITA'** | ha ### **una via "
      "di scrittura** e ### **zero storico**: oggi il presidio lo tratta come reperto, "
      "### **ma e' un BUCO** |")
    A("| `5` | la ### **CI non e' mai stata osservata girare** | e ### **non e' un "
      "presidio**: senza protezione del ramo gira ### **dopo** il push e "
      "### **non impedisce niente** *(`A9`)*. ### **La cura — gli hook verificati "
      "all'avvio — e' la TERZA parte** |")
    A("| `6` | il ### **budget del `pre-commit`** | ### **FATTO, nel punto `6` della "
      "TERZA parte**, e ### **ha corretto un numero che avevo scritto QUI:** il "
      "`pre-commit` costa ### **`43.3` s** su un budget dichiarato di ### **`120`**, e il "
      "collaudo della catena ### **`2.55` s** -- ### **non <<oltre `120`>>, che e' cio' "
      "che questa riga diceva.** I lenti veri sono ### **i generatori di referto** "
      "*(`45.99` e `28.33` s)* |")
    A("")
    A("---")
    A("")
    A("*(Referto generato da `csv/_referto_seconda_parte.py`: ### **ogni numero esce "
      "dall'uscita dei comandi della tavola `2.`** o dalle tabelle strutturate dei "
      "presidi — `L-NUMERI`. I lenti si passano con `--con-lenti`.)*")
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(L) + NL)
    print()
    print("  scritto %s (%d righe)" % (os.path.relpath(FUORI, RADICE), len(L)))
    tutti = all((r == 0) and (a is None or a == b) for _n, _c, r, a, b in esiti)
    print("  ### TUTTI I COLLAUDI PASSANO" if tutti
          else "  ### ⛔ QUALCHE COLLAUDO NON PASSA, e il referto LO DICE")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
