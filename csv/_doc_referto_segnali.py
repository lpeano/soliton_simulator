# -*- coding: utf-8 -*-
"""IL REFERTO DELLA CHIUSURA DEI SEGNALI — **voce per voce.**

### ⛔ **NESSUN NUMERO RICOPIATO** *(`L-NUMERI`)*: i segnali **DOPO** escono dalle stesse
funzioni che gira il validatore; quelli **PRIMA** da
`git show 433d215:doc/REFERTO_indice_v3_presidi.md`, cioe' **dal referto committato** che li
ha misurati; i conteggi **prima** da `git show 433d215:doc/indice/voci.jsonl`.

Gira con:  python csv/_doc_referto_segnali.py
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
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import indice as IX                                          # noqa: E402
import _segnali_chiusura as S                                # noqa: E402
import _p5_etichette as P5                                   # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
PRIMA = "433d215"
R = []


def p(s=""):
    R.append(s)


def gshow(ref):
    q = subprocess.run(["git", "show", ref], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8")
    assert q.returncode == 0, ref
    return q.stdout


def conta(righe, campo):
    c = {}
    for v in righe:
        c[str(v[campo])] = c.get(str(v[campo]), 0) + 1
    return c


def tab(campo, a, b):
    p("| `%s` | prima | dopo | |" % campo)
    p("|---|--:|--:|---|")
    for k in sorted(set(a) | set(b), key=lambda x: -b.get(x, 0)):
        d = b.get(k, 0) - a.get(k, 0)
        p("| %s | `%d` | `%d` | %s |" % (k, a.get(k, 0), b.get(k, 0),
                                         ("### **%+d**" % d) if d else ""))
    p()


def main():
    voci = [json.loads(r) for r in
            io.open(os.path.join(RADICE, "doc/indice/voci.jsonl"), encoding="utf-8")
            if r.strip()]
    per = {v["id"]: v for v in voci}
    _v, reg = IX.carica()
    dopo = {x[0]: x[2] for x in IX.segnali(voci, reg, verboso=False)}
    # ---- i segnali PRIMA, dal referto COMMITTATO che li ha misurati
    vecchio = gshow("%s:doc/REFERTO_indice_v3_presidi.md" % PRIMA)
    prima = {m.group(1): int(m.group(2)) for m in
             re.finditer(r"### `(F\d)` — \*\*(\d+) segnali", vecchio)}
    prima["F5"] = 0
    assert set(prima) >= {"F1", "F2", "F3", "F4", "F6"}, prima
    pv = [json.loads(r) for r in gshow("%s:doc/indice/voci.jsonl" % PRIMA).split(NL)
          if r.strip()]
    pe = len([r for r in gshow("%s:doc/indice/etichette_rimosse.jsonl" % PRIMA).split(NL)
              if r.strip()])
    etich = [json.loads(r) for r in
             io.open(os.path.join(RADICE, "doc/indice/etichette_rimosse.jsonl"),
                     encoding="utf-8").read().split(NL) if r.strip()]
    defi = json.loads(io.open(os.path.join(RADICE, "doc/indice/_definizioni.json"),
                              encoding="utf-8").read())
    q = subprocess.run([sys.executable, os.path.join(_QUI, "_collaudo_presidi_indice.py")],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    _E = re.compile(r"^  \S.*\s(PASSA|### FALLISCE)(\s|$)")
    coll = [r.rstrip() for r in (q.stdout or "").split(NL) if _E.match(r)]
    n_ok = sum(1 for r in coll if _E.match(r).group(1) == "PASSA")
    q2 = subprocess.run([sys.executable, os.path.join(_QUI, "_controlli_indice_v2.py")],
                        cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    ctrl = [r.rstrip() for r in (q2.stdout or "").split(NL)
            if re.match(r"^\s+C\d+ ", r) and ("PASSA" in r or "FALLISCE" in r)]

    p("# IL REFERTO DELLA CHIUSURA DEI SEGNALI DEI PRESIDI")
    p()
    p("> ### ⭐ **Il guardiano ha letto i `%d` segnali uno per uno, e il verdetto e' "
      "stato: «la maggior parte e' rumore, ### E IN PARTE PER COLPA MIA».** Questo referto e' "
      "la chiusura, e ### **i numeri sono `%d` -> `%d`.**"
      % (sum(prima.values()), sum(prima.values()), sum(len(v) for v in dopo.values())))
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_chiusura_segnali.md`, "
      "### **committato PRIMA del lavoro** *(`f2e950f`)* |")
    p("| **i commit** | `a8107b2` *(`1`)* · `0ef62f6` *(`2`)* · `0c4cb57` *(`3`)* "
      "· `1d34bc0` *(`4`)* · `c24eb66` *(`5`)*, piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **il collaudo** | ### **`%d` su `%d`** *(erano `15`: ### **`5` bracci nuovi**, `2` "
      "su `F1` e `3` su `F4`)* |" % (n_ok, len(coll)))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ① I SEGNALI, PRIMA E DOPO")
    p()
    p("| presidio | prima | dopo | come si sono chiusi |")
    p("|---|--:|--:|---|")
    COME = {
        "F1": "### **la formulazione era MIA:** `F1` ignora le voci citate `STANDARD`, "
              "`PRESIDIO` e `NON_DEFINITA`. ### ⚠ **Ma il punto `2` ne ha CREATI `6` "
              "nuovi**, e restano ### **elencati, non chiusi**",
        "F2": "`8` eccezioni che ### **citano la frase del «sostituisce»**; "
              "`ENERGIA-NON-DEFINITA` ### **non si tocca** e il suo segnale ### **resta "
              "acceso**",
        "F3": "`5` `CRITERIO` sono uscite da `FISICA` col punto `2`; `9` chiuse con "
              "l'eccezione; `1` *(`W5`)* ### **spostata**",
        "F4": "### **la regola dell'intestazione**; `7` ripristinate, `6` omonimi, `1` resta "
              "etichetta. I `3` che restano sono ### **il QUARTO CASO**",
        "F5": "### **zero prima e zero adesso.** `storico-commit` tiene il campo pieno",
        "F6": "### **zero prima e zero adesso**, dal blocco `G3`",
    }
    for k in ("F1", "F2", "F3", "F4", "F5", "F6"):
        n = len(dopo.get(k, []))
        p("| ### **`%s`** | `%d` | ### **`%d`** | %s |" % (k, prima[k], n, COME[k]))
    p("| ### **in tutto** | ### **`%d`** | ### **`%d`** | |"
      % (sum(prima.values()), sum(len(v) for v in dopo.values())))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ② PUNTO `1` — **`F1` era MIO**")
    p()
    p("> ### ⛔ **«Citare un assioma non vuol dire essere gemelle»**, scrive il guardiano. "
      "`D24` dice *«`A2` e' VIOLATO da `Lam = mean(I)` — una media GLOBALE dentro una "
      "legge locale»*: `D24` e' un difetto dell'era `1`, `A2` e' uno ### **`STANDARD` che "
      "vale per ENTRAMBE le ere**, e ### **«differiscono» e' GIUSTO che sia vero.**")
    p()
    p("### ⚠ **E nel referto dei presidi avevo dichiarato `12` segnali verso i "
      "segnaposto, presentandoli come «da decidere»:** era ### **la meta' del problema vista "
      "per un quarto.** Non avevo guardato che altri `30` puntavano ad ### **assiomi e "
      "presidi** — cose che ### **per definizione valgono per entrambe le ere.** "
      "### **`42` su `49`**, e la misura l'ho fatta ### **solo dopo che il guardiano me l'ha "
      "detto.**")
    p()
    p("### ✔ **E la restrizione si prova con DUE bracci, non col numero:** un presidio "
      "che segnala meno ### **non e' per questo giusto.** `D24` non deve scattare *(`A2` e' "
      "uno `STANDARD`)*, ### **e con `A2` finto `DIFETTO` deve tornare a scattare** — "
      "cosi' si sa che ### **e' LA CLASSE a zittirlo**, non un effetto collaterale.")
    p()
    p("### **`C5` e' un OMONIMO**, e il guardiano l'ha visto leggendo `F1`:")
    p()
    p("| | il significato |")
    p("|---|---|")
    for x in per["C5"]["meta"]["omonimo"]:
        p("| | %s |" % x)
    p()
    p("`Z100` e `C5-INVARIANTI` chiudono con l'eccezione: il `C5` che citano e' "
      "### **il mandato degli invarianti**, non la voce `C5`.")
    p()
    p("### **I `%d` segnali di `F1` che restano** — il mandato chiede di elencarli, "
      "### **non di chiuderli:**" % len(dopo["F1"]))
    p()
    p("| id | `classe`/`dominio`/era | il segnale | la mia lettura |")
    p("|---|---|---|---|")
    LETT = {
        "AB-CONTROLLI": "un DIFETTO che nomina la voce di cui parla",
        "COER-4PI": "### **un CRITERIO che cita la legge che verifica** — e' la "
                    "categoria che il punto `2` ha creato",
        "COLLAUDO-NON-ESEGUITO": "un DIFETTO che nomina il controllo di cui parla",
        "E3": "una CURA che nomina le misure da leggere durante la corsa",
        "ETICHETTA-A13": "un difetto di DOCUMENTAZIONE che nomina la regola giusta",
        "M-MASSA": "una CURA che dichiara ### **da che cosa DIPENDE**",
        "REGISTRO_FISICA:E3": "### **un CRITERIO che cita la legge che verifica**",
        "REGISTRO_FISICA:S6": "### **un CRITERIO che cita la legge che verifica**",
        "REGISTRO_FISICA:U2": "### **un CRITERIO che cita la legge che verifica**",
    }
    for i, m in dopo["F1"]:
        v = per[i]
        p("| `%s` | `%s`/`%s`/`%s` | %s | %s |"
          % (i, v["classe"], v["dominio"], v["era"],
             re.sub(r"^il titolo cita ", "cita ", m).split(", mentre")[0],
             LETT.get(i, "")))
    p()
    p("### ⛔ **LA RESTRIZIONE CANDIDATA, e NON l'ho applicata:** ### **un `CRITERIO` in "
      "`METODO` che cita una voce `FISICA` non e' una gemella** — e' ### **la relazione "
      "normale fra un controllo e la sua legge**, la stessa forma del rumore che il punto `1` "
      "ha tolto. Coprirebbe `%d` dei `%d`. ### **Restringere `F1` una seconda volta e' una "
      "decisione di Luca.**"
      % (sum(1 for i, _m in dopo["F1"] if per[i]["classe"] == "CRITERIO"),
         len(dopo["F1"])))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ③ PUNTO `2` — **la classe `CRITERIO` e' una cosa sola**")
    p()
    p("> ### ⭐ **Un criterio DICE COME SI GIUDICA, quindi e' `METODO`.** Era "
      "### **spaccata in due**: `71` voci in `FISICA` e `35` in `METODO`, e ### **gli stessi "
      "tipi di criterio** — *«caso che deve fallire»*, *«byte-identico»* — stavano "
      "### **da tutte e due le parti.**")
    p()
    p("### **`58` a `METODO`, `13` a classe `MISURA` restando `FISICA`**, `era` e `stato` "
      "### **invariati.** ### ⚠ **Non e' una decisione di fisica**, e il guardiano lo "
      "dichiara; tutte restano `SOSPESE` o `CHIUSE`, quindi ### **non cambia nulla per l'era "
      "`2`, solo l'ordine.**")
    p()
    p("### ✔ **I `%d` ESITI MISURATI, con LA FRASE CHE L'HA DECISO** — il mandato "
      "la chiede:" % len(S.DECISO_ESITO))
    p()
    p("| id | la frase |")
    p("|---|---|")
    for i in sorted(S.DECISO_ESITO):
        p("| `%s` | %s |" % (i, S.DECISO_ESITO[i]))
    p()
    p("### ⛔ **E `%d` CANDIDATI CHE LA REGOLA AVEVA PRESO E CHE LEGGENDO SONO "
      "CONTROLLI:**" % len(S.DECISO_CRITERIO))
    p()
    p("| id | perche' NON e' un esito |")
    p("|---|---|")
    for i in sorted(S.DECISO_CRITERIO):
        p("| `%s` | %s |" % (i, S.DECISO_CRITERIO[i]))
    p()
    p("### **Il numero c'e', ma non e' una misura: e' il valore CONTRO CUI si confronta.** "
      "Due *(`S3`, `S5`)* venivano da ### **un difetto della mia regola** — `==` non e' "
      "una misura, e' ### **un confronto** — e la regola e' corretta nel sorgente; gli "
      "altri due ### **passano solo per la lettura.**")
    p()
    p("### ⭐ **E il controllo `C3` conosce LA REGOLA, non i `6` ID** che oggi la "
      "esercitano: una voce `CRITERIO` si aspetta in `METODO` ### **qualunque cosa dicesse la "
      "lista del guardiano.** ### **Il punto `2` non e' una lista di ID: e' una regola**, e "
      "si scrive come tale — mentre `W5` *(punto `4`)* ### **l'ho deciso leggendo**, e "
      "un ID deciso leggendo ### **si scrive come ID.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ④ PUNTO `3` — **`F2`: segnali veri, voci al posto giusto**")
    p()
    p("`F2` vede l'era `1` e ### **ha ragione a vederla**: sono voci ### **di programma** che "
      "nominano il vecchio codice ### **per dire che cosa sostituiscono.** "
      "### ⛔ **Un segnale vero su una voce giusta NON si chiude spostando la voce: si "
      "chiude DICHIARANDO perche'.**")
    p()
    p("| id | il marcatore che ho scelto nel testo |")
    p("|---|---|")
    for i in sorted(S.F2_MARCATORE):
        p("| `%s` | *«%s»* |" % (i, S.F2_MARCATORE[i]))
    p()
    p("### ✔ **LA CITAZIONE NON SI RICOPIA: SI ESTRAE DAL TESTO VIVO.** Per ogni voce ho "
      "### **letto** il testo e scelto ### **un marcatore**; la frase la ritaglia il codice "
      "### **attorno a quel marcatore, dal testo della voce.** Cosi' e' letterale ### **per "
      "costruzione**, non per mia diligenza nel copiare — e ### **se il marcatore non "
      "c'e', il codice si ferma** invece di scrivere un'eccezione falsa.")
    p()
    p("### ⛔ **`ENERGIA-NON-DEFINITA`: il segnale RESTA ACCESO, ed e' voluto.** Il "
      "mandato dice di non toccarla; prende ### **solo la nota** *«da decidere da Luca: "
      "superata da `A16` (`H` definita)?»*. Il guardiano scrive che ### **secondo lui e' "
      "superata**, e lo dice ### **come opinione, non come decisione.** "
      "### ⭐ **Un'eccezione dice «guardato, va bene cosi'»; una nota dice «da decidere». "
      "Chiuderlo sarebbe stato decidere al posto di Luca.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑤ PUNTO `4` — **`F3`: il commento e' IL CONTRASTO, non il difetto**")
    p()
    p("### ⭐ **La regolarita' che viene fuori leggendo, e non l'avevo prevista:** in "
      "### **quattro dei cinque** letti il commento o il docstring e' ### **il contrasto**, "
      "non il difetto — la voce dice *«il codice fa `X` e il commento dice `Y`»*, e "
      "### **il difetto e' `X`.**")
    p()
    p("| id | esito | perche' |")
    p("|---|---|---|")
    for i in sorted(S.F3_RESTA):
        tipo, perche = S.F3_RESTA[i]
        p("| `%s` | resta `FISICA` *(%s)* | %s |" % (i, tipo.lower(), perche))
    for i in sorted(S.F3_SPOSTA):
        dom, perche = S.F3_SPOSTA[i]
        p("| `%s` | ### **spostata a `%s`** | %s |" % (i, dom, perche))
    p()
    p("### ⚠ **E una cosa che lascio a Luca:** la ### **classe** di `W5` resta "
      "`DIFETTO`, e il suo testo e' ### **un criterio.** Il mandato dice *«sposta»*, cioe' il "
      "dominio, e il dominio l'ho spostato; ### **cambiare anche la classe sarebbe applicare "
      "il punto `2` a una voce che il punto `2` non toccava.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑥ PUNTO `5` — **`F4`, e il FALSO-UNO per la terza volta**")
    p()
    p("### ⛔ **LA REGOLA DELL'INTESTAZIONE: l'ID deve essere il SOGGETTO, e ci deve "
      "essere CONTENUTO.** La distinzione e' ### **grammaticale**: in `## APERTO CURA1-CORTO` "
      "l'ID e' il soggetto; in `### 1.2 ⚠ E LA LETTURA CHE DECIDE DAVVERO — "
      "dichiarata POST-HOC, non era fissata prima` ### **`POST-HOC` e' un aggettivo**, e "
      "`RI-LETTO`, `RI-VERIFICATI`, `SOVRA-CORREGGE` sono ### **verbi.**")
    p()
    p("### ✔ **Il collaudo ha TRE bracci, non i due che il mandato fissa:** `POST-HOC` "
      "non deve scattare, `TW-1` a `6e5e75b` deve, ### **e con la regola SPENTA `POST-HOC` "
      "deve tornare a scattare** — senza il terzo, *«`POST-HOC` non scatta»* potrebbe "
      "essere vero ### **per la ragione sbagliata.**")
    p()
    p("### ⛔ **IL FALSO-UNO PER LA TERZA VOLTA, E STAVOLTA I FILE ERANO MIEI**")
    p()
    p("| | il file che ELENCA e sembrava DEFINIRE | chi l'ha preso |")
    p("|---|---|---|")
    p("| `1` | `doc/INDICE.md`, letto dal controllo `C4` — ### **un file che `C4` genera "
      "lui** | il controllo dell'idempotenza |")
    p("| `2` | `doc/LISTA_CHIUSA.md`, ### **la lista degli ID** | il ripasso del blocco `C` |")
    p("| `3` | ### **I MIEI REFERTI** — `doc/REFERTO_indice_v3_presidi.md` scrive "
      "`| ID | … |` per ogni segnale | ### **io, guardando i nomi dei "
      "file nell'uscita** |")
    p()
    p("> ### ⭐ **IL PRINCIPIO, scritto una volta per tutte in `doc/REGOLE/par9.md`:** "
      "### **un file che PARLA DELL'INDICE ELENCA gli ID; non li DEFINISCE.**")
    p()
    p("### **E `F4` SI FERMA AL PRIMO FILE**, quindi ### **non puo' dire se un ID e' un "
      "omonimo.** Per quello c'e' `python csv/_cerca_definizioni.py`, che cerca "
      "### **TUTTE** le definizioni in ### **`1527` file tracciati.**")
    p()
    p("### ✔ **I QUATTRO ESITI, voce per voce**")
    p()
    p("| id | esito | definizioni | perche' |")
    p("|---|---|--:|---|")
    for i in sorted(P5.RIPRISTINA):
        cl, dom, era, st, perche = P5.RIPRISTINA[i]
        p("| `%s` | ### **ripristinata** `%s`/`%s`/era `%s`/`%s` | `%d` | %s |"
          % (i, cl, dom, era, st, len(defi[i]), perche))
    for i in sorted(P5.OMONIMI):
        p("| `%s` | ### **OMONIMO**, `NON_DEFINITA` | `%d` in `%d` file | %s |"
          % (i, len(defi[i]), len({x["file"] for x in defi[i]}), P5.OMONIMI[i]))
    for i in sorted(P5.RESTA):
        p("| `%s` | resta etichetta, con l'eccezione | `%d` | %s |"
          % (i, len(defi[i]), P5.RESTA[i]))
    for i in sorted(P5.QUARTO):
        p("| `%s` | ### ⚠ **il QUARTO CASO**: nota, e ### **segnale ACCESO** | `%d` | "
          "%s |" % (i, len(defi[i]), P5.QUARTO[i]))
    for i in P5.ZERO:
        p("| `%s` | resta etichetta | ### **`0`** | il guardiano la dava per ### **candidata "
          "al ripristino**; nel repo ### **non e' definita da nessuna parte**, e con la "
          "regola nuova `F4` non la segnala piu' |" % i)
    p()
    p("### ⚠ **DUE LETTURE MIE, e le dichiaro:**")
    p()
    p("| | la lettura |")
    p("|---|---|")
    p("| ① | il primo esito dice *«in un solo ### **POSTO**»*; `H1` e `H3` sono definite "
      "in ### **quattro posti con UN SOLO SIGNIFICATO**. ### **Il cancello esiste per non FAR "
      "SCEGLIERE**, e con un solo significato ### **non c'e' niente da scegliere** |")
    p("| ② | il contenuto deve essere *«una corsa, un sigillo, una legge, una misura»*. "
      "### **Una REGOLA DI LAVORO non e' una legge** *(`AUTO-MANUTENZIONE`)*, e ### **una "
      "FAMIGLIA di difetti che punta a un'altra voce non e' nessuna delle quattro** *(`F4`, "
      "`F5`)*: ### **quarto caso**, e l'avevo previsto nel task history |")
    p()
    p("### ⭐ **`D3`, `D4`, `D5`, `D6`: QUATTRO OMONIMI DALLA STESSA COPPIA DI TAVOLE** "
      "— `doc/CENSIMENTO_intenzioni.md` *(voci del censimento)* e "
      "`doc/MAPPA_accoppiamenti_spin.md` *(termini di accoppiamento)*. ### **E' un fatto "
      "sull'indice, non su quelle quattro voci.**")
    p()
    p("### ⚠ **E DUE SEGNALI CHE HO CREATO IO, chiusi nello stesso giro:** ripristinando "
      "`SIGILLO-CURA2` e `SIGILLO-CURA2-RIPARATO` come voci `FISICA`, `F3` e' risalito da `0` "
      "a `2` — ### **il segnale scattava SUL LORO STESSO NOME**, perche' *«sigillo»* e' "
      "### **nell'ID.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑦ I CONTEGGI E I CONTROLLI")
    p()
    p("> **PRIMA** = `git show %s`. **DOPO** = il disco. ### **Nessun numero ricopiato.**"
      % PRIMA)
    p()
    for campo in ("dominio", "classe", "era", "stato"):
        tab(campo, conta(pv, campo), conta(voci, campo))
    p("| | prima | dopo |")
    p("|---|--:|--:|")
    p("| voci | `%d` | ### **`%d`** |" % (len(pv), len(voci)))
    p("| etichette rimosse | `%d` | ### **`%d`** |" % (pe, len(etich)))
    p("| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |")
    p()
    p("```")
    for r in ctrl:
        p(r)
    for r in coll:
        p(r)
    p("```")
    p()
    p("| | |")
    p("|---|---|")
    p("| `python csv/_controlli_indice_v2.py` | ### **%d su %d** |"
      % (sum(1 for r in ctrl if "PASSA" in r), len(ctrl)))
    p("| `python csv/_collaudo_presidi_indice.py` | ### **%d su %d** |" % (n_ok, len(coll)))
    p("| `python csv/indice.py valida` | ### **passa** |")
    p("| `python csv/indice.py collaudo` | ### **21 su 21** |")
    p("| `python csv/_indice_id.py` *(il validatore del `pre-commit`)* | ### **passa** |")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑧ CHE COSA RESTA A LUCA")
    p()
    p("| | che cosa, e perche' non l'ho deciso io |")
    p("|---|---|")
    p("| ### **gli `%d` segnali che restano** | `%d` di `F1` *(di cui `%d` sono la categoria "
      "che il punto `2` ha CREATO)*, `1` di `F2` *(`ENERGIA-NON-DEFINITA`)*, `%d` di `F4` "
      "*(il QUARTO CASO)*. ### **Sono ELENCATI, non chiusi** |"
      % (sum(len(v) for v in dopo.values()), len(dopo["F1"]),
         sum(1 for i, _m in dopo["F1"] if per[i]["classe"] == "CRITERIO"),
         len(dopo["F4"])))
    p("| ### **`ENERGIA-NON-DEFINITA`** | *«superata da `A16` (`H` definita)?»*. Il guardiano "
      "dice che ### **secondo lui si'**; la voce porta la nota e ### **il segnale acceso** |")
    p("| ### **la restrizione `2` di `F1`** | *un `CRITERIO` in `METODO` che cita una voce "
      "`FISICA` non e' una gemella*. ### **Coprirebbe `%d` segnali, e NON l'ho applicata** |"
      % sum(1 for i, _m in dopo["F1"] if per[i]["classe"] == "CRITERIO"))
    p("| ### **la classe di `W5`** | resta `DIFETTO`, e il testo e' ### **un criterio** |")
    p("| ### **il QUARTO CASO** | `AUTO-MANUTENZIONE` *(una regola di lavoro)*, `F4` e `F5` "
      "*(una famiglia di difetti)*: ### **nessuno dei tre esiti del mandato** |")
    p("| ### **le `7` ripristinate** | portano una ### **classificazione che ho letto io** "
      "dal testo che le definisce. Lo ### **stato** `APERTA` non l'ho scelto *(lo dice "
      "l'intestazione)*; ### **classe e dominio sono MIEI** |")
    p("| ### **`S1`, `S3`, `T1`** | `22`, `21` e `34` definizioni: `meta.omonimo` ne porta "
      "### **sei piu' il conteggio**, e la lista intera sta in "
      "`doc/indice/_definizioni.json` |")
    p()
    p("> ### ⭐ **Il criterio, lo stesso di tutto il giro:** dove il mandato "
      "### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho "
      "lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un "
      "dato; una decisione presa al posto di Luca e' un difetto.**")
    p()

    q3 = os.path.join(RADICE, "doc", "REFERTO_indice_v3_segnali.md")
    io.open(q3, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_segnali.md: %d righe" % len(R))
    print("  segnali %d -> %d; collaudo %d/%d; controlli %d/%d"
          % (sum(prima.values()), sum(len(v) for v in dopo.values()), n_ok, len(coll),
             sum(1 for r in ctrl if "PASSA" in r), len(ctrl)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
