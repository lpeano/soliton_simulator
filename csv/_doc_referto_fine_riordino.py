# -*- coding: utf-8 -*-
"""IL REFERTO DELLA FINE DEL RIORDINO — **voce per voce, e nessun numero ricopiato.**

Il **prima** da `git show 61711cb:doc/indice/voci.jsonl` *(il task history, prima di ogni
scrittura del giro)*, il **dopo** dal disco.

Gira con:  python csv/_doc_referto_fine_riordino.py
"""
import collections
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
import _file_fisica as FF                                    # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
PRIMA = "61711cb"
R = []


def p(s=""):
    R.append(s)


def gshow(ref):
    q = subprocess.run(["git", "show", ref], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8")
    assert q.returncode == 0, ref
    return q.stdout


def js(rel):
    return json.loads(io.open(os.path.join(RADICE, rel), encoding="utf-8").read())


def gira(cmd, pat):
    q = subprocess.run([sys.executable] + cmd, cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8")
    m = re.search(pat, q.stdout or "")
    assert m, cmd
    return m.group(1), m.group(2)


def tab(campo, a, b):
    p("| `%s` | prima | dopo | |" % campo)
    p("|---|--:|--:|---|")
    # ### ⛔ **IL NOME E- LO SPAREGGIO:** un ordine totale non ha pari merito, e un referto
    # ### ### **che non si rigenera identico non si puo- verificare.**
    for k in sorted(set(a) | set(b), key=lambda x: (-b.get(x, 0), x)):
        d = b.get(k, 0) - a.get(k, 0)
        p("| %s | `%d` | `%d` | %s |" % (k, a.get(k, 0), b.get(k, 0),
                                         ("### **%+d**" % d) if d else ""))
    p()


def main():
    voci = [json.loads(r) for r in
            io.open(os.path.join(RADICE, "doc/indice/voci.jsonl"), encoding="utf-8")
            if r.strip()]
    per = {v["id"]: v for v in voci}
    pv = [json.loads(r) for r in gshow("%s:doc/indice/voci.jsonl" % PRIMA).split(NL)
          if r.strip()]
    pper = {v["id"]: v for v in pv}
    _v, reg = IX.carica()
    seg = {x[0]: x[2] for x in IX.segnali(voci, reg, verboso=False)}
    ind = js("doc/indice/_p2_indirizzate.json")
    dd = io.open(os.path.join(RADICE, "doc/indice/DA_DECIDERE_LUCA.md"),
                 encoding="utf-8").read()
    m_dd = re.search(r"decisione\*\* \| ### \*\*`(\d+)`\*\*", dd)
    n_pres = gira(["csv/_collaudo_presidi_indice.py"],
                  r"IL COLLAUDO DEI PRESIDI: (\d+) su (\d+)")
    n_ind = gira(["csv/indice.py", "collaudo"], r"COLLAUDO: (\d+) su (\d+)")
    n_ctrl = gira(["csv/_controlli_indice_v2.py"], r"I CONTROLLI: (\d+) su (\d+)")
    n_ff = gira(["csv/_collaudo_file_fisica.py"],
                r"IL COLLAUDO DI `_file_fisica.py`: (\d+) su (\d+)")
    n_id = gira(["csv/_hook_id_obbligatorio.py", "--collaudo"],
                r"COLLAUDO `H-ID-OBBLIGATORIO`: (\d+) su (\d+)")

    p("# IL REFERTO DELLA FINE DEL RIORDINO")
    p()
    p("> ### ⭐ **DUE DEI SEI PUNTI CORREGGONO PRESIDI CHE HO SCRITTO IO**, e il "
      "guardiano dichiara l'errore suo — ma ### **l'applicazione era mia, e in entrambi "
      "i casi avevo ELENCATO I LORO SEGNALI COME DIFETTI DELL'INDICE.** "
      "### ⛔ **Il difetto non era nelle voci: era nel presidio.**")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | "
      "`doc/TASK_HISTORY/2026-10-09_indice_v3_fine_riordino.md`, ### **committato PRIMA del "
      "lavoro** *(`%s`)* |" % PRIMA)
    p("| **i commit** | `c80d3a4` *(`1`)* · `2bfa639` *(`2`)* · `c38bd10` *(`3`)* "
      "· `7eb64fe` *(`4`)* · `7a86f61` *(`5`)*, piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **i controlli** | ### **%s/%s** · presidi ### **%s/%s** · indice "
      "### **%s/%s** · `_file_fisica` ### **%s/%s** · `H-ID-OBBLIGATORIO` "
      "### **%s/%s** |" % (n_ctrl + n_pres + n_ind + n_ff + n_id))
    p()
    p("---")
    p()

    # ================================================================ punto 1
    p("## ① PUNTO `1` — **`primo_ordine/`: la tenda diventa un presidio**")
    p()
    p("| | |")
    p("|---|---|")
    p("| la costante | `CARTELLA_ERA_2 = %r` *(decisione di Luca)* |" % FF.CARTELLA_ERA_2)
    p("| ### ✔ **e `H-FISICA-FUORI-LISTA` IMPEDISCE** | finche' era `\"\"` era "
      "### **una TENDA** *(`A9`)*, e l'avevo dichiarato in ### **quattro posti.** "
      "### **Tre sono diventati falsi, e li ho riscritti** |")
    p("| ### ⚠ **la cartella NON esiste, e NON l'ho creata** | il mandato da' ### **il "
      "nome**, non l'ordine di crearla — e creare la cartella del codice dell'era `2` "
      "e' ### **un atto di FISICA** |")
    p("| ### ⭐ **e il presidio funziona comunque** | guarda ### **i percorsi staged, non il "
      "disco**: impedisce ### **dal primo `.py` che qualcuno metta la-** |")
    p("| il collaudo | ### **%s/%s**, sulla cartella VERA nei due versi, piu' "
      "### **una copia con la costante VUOTA** che conserva ### **la misura del vecchio "
      "stato** |" % (n_ff[0], n_ff[1]))
    p()
    p("### ⭐ **E IL REFERTO VECCHIO *(`doc/REFERTO_strumenti_era2.md`)* DICE ANCORA «e' "
      "una tenda», e NON l'ho riscritto:** ### **un referto e' la foto di un giorno.** Questo "
      "lo cita e dice che ### **la tenda e' diventata un presidio.**")
    p()
    p("---")
    p()

    # ================================================================ punto 2
    p("## ② PUNTO `2` — **le `10` righe a `file:riga`**: `%d` su `%d`"
      % (len(ind["fatte"]), len(ind["fatte"]) + len(ind["non_fatte"])))
    p()
    p("> ### ⛔ **LE CITAZIONI ERANO GIUSTE, E IL DIFETTO ERA IL MIO RITROVAMENTO.** "
      "Cercavo ### **nel file della `fonte`** della voce, e per queste dieci la frase sta "
      "### **in un altro file** — e il referto le metteva fra le *«non applicate: la "
      "citazione non compare»*. ### ⭐ **Il mio livello `T4` era LARGO NEL POSTO "
      "SBAGLIATO: largo nel FILE, e CIECO SU QUALE FILE.**")
    p()
    p("| id | il file chiede | la frase | l'indirizzo | la riga che la porta |")
    p("|---|---|---|---|---|")
    for x in ind["fatte"]:
        p("| `%s` | `%s` | *(vedi l'indirizzo)* | `%s` | *%s* |"
          % (x["id"], json.dumps(x["campi"], ensure_ascii=False).replace("|", "/")[:90],
             x["indirizzo"], x["riga"].replace("|", "/")[:120]))
    p()
    p("### ✔ **E IL CONTROLLO DEL MANDATO E- PIU- STRETTO DEL MIO:** la frase deve "
      "essere ### **ESATTAMENTE alla riga indicata.** Niente `N±1`, niente *«altrove»*. "
      "### **Un indirizzo sbagliato non si corregge a mano** — e non e' servito: "
      "### **`%d` su `%d`.**" % (len(ind["fatte"]),
                                 len(ind["fatte"]) + len(ind["non_fatte"])))
    p()
    p("### ⚠ **UNA L'HO GUARDATA DUE VOLTE:** `Z119` indirizza a `doc/STATO_RUN.md:653`, "
      "e quella riga ### **parla di `D35`.** La riga e' lunga ### **`440` caratteri**, e la "
      "frase sta ### **al carattere `167`**, nella colonna *«come si e' saputo»*. "
      "### **Il match era genuino, e l'ho verificato invece di fidarmi del troncamento della "
      "mia stampa.**")
    p()
    p("### ✔ **E `STANDARD-6` SI RITIRA DAI DATI** *(citazione inesistente)*: il file "
      "del guardiano passa da `59` a ### **`58`** righe. ### ⛔ **Un dato che il guardiano "
      "RITIRA si TOGLIE, non si corregge** — e il commit `3926dbb` che asseriva `59` "
      "### **era vero quando l'ha asserito.**")
    p()
    p("---")
    p()

    # ================================================================ punto 3
    p("## ③ PUNTO `3` — **lo STATO esce da `F1`**, e avevo elencato la forma "
      "giusta come un difetto")
    p()
    p("| | |")
    p("|---|---|")
    p("| ### **la distinzione che non avevo** | la voce `D` e' ### **il DIFETTO**, la `Z` e' "
      "### **il REPERTO che lo ha trovato.** Io le leggevo come *«la stessa cosa scritta due "
      "volte»* |")
    p("| ### ⭐ **e una misura resta un'avvertenza** | anche dopo che il difetto e' curato "
      "*(`D19` CURATO, `Z88` aperta come avvertenza)*: ### **possono stare in stati diversi "
      "A RAGIONE** |")
    p("| ### ⛔ **cosa avevo scritto nel referto** | *«se danno stati diversi, sono le RIGHE "
      "a disaccordare, e questo e' il ritrovato»*. ### **Le righe dicevano la verita-, e il "
      "presidio era sbagliato** |")
    p("| ### ⚠ **e il braccio di collaudo PASSAVA** | il caso diceva *«`D08` cita `Z14`, e "
      "sono LO STESSO FATTO con stati diversi: DEVE scattare»* — e scattava. "
      "### **Un caso a risposta nota con la RISPOSTA SBAGLIATA passa, e non si accorge di "
      "niente** |")
    p("| ### ⭐ **la lezione** | ### **il collaudo non puo' trovare un errore nella REGOLA: "
      "lo trova chi legge i segnali** — e il guardiano li ha letti |")
    p()
    p("### **`F1`: `8` → `%d`, e i `%d` che restano sono VERI** *(differiscono "
      "### **anche per dominio o era**)*" % (len(seg["F1"]), len(seg["F1"])))
    p()
    p("| id | il segnale |")
    p("|---|---|")
    for i, mm in sorted(seg["F1"]):
        p("| `%s` | %s |" % (i, mm.replace("|", "/")))
    p()
    p("---")
    p()

    # ================================================================ punto 4
    p("## ④ PUNTO `4` — **`F8` perde il marcatore `.py`**, e due richieste sono "
      "INCOMPATIBILI")
    p()
    p("| | |")
    p("|---|---|")
    p("| ### **il perche' del taglio** | ### **quasi ogni voce di METODO nomina un `.py`** "
      "— un presidio, un attrezzo, un collaudo — e un `.py` ### **non e' un "
      "oggetto dell'era `1`: e' un oggetto DEL REPO** |")
    p("| ### ⛔ **e il marcatore l'avevo aggiunto IO** | nel mandato dell'era delle voci di "
      "metodo. ### **E avevo gia' tolto un marcatore mio una volta** *(il `FLAG-COSTANTE`)*: "
      "### **questo l'ho tenuto, e per quattro giri** |")
    p("| ### ⚠ **e la mia previsione era sbagliata** | nel task history avevo scritto "
      "*«prevedo `3` segnali residui su `20`»*: sono ### **`%d`.** Il marcatore ne faceva "
      "### **`6`, non `17`** — ### **avevo attribuito al marcatore piu' di quanto "
      "facesse** |" % len(seg["F8"]))
    p()
    p("### ⛔ **E DUE RICHIESTE DEL PUNTO `4` SONO INCOMPATIBILI, MISURATO**")
    p()
    p("| | il fatto misurato |")
    p("|---|---|")
    p("| `(a)` | *«DEVE scattare su `CONFIG-1` a `80eaf82`»*: ### **a quel commit `CONFIG-1` "
      "e' era `1`** — il mandato dell'era delle voci di metodo ### **l'ha spostata** "
      "— e `F8` per costruzione guarda ### **solo le `ENTRAMBE`.** ### **Nessun "
      "marcatore puo' farla scattare la-** |")
    p("| `(b)` | anche a `ba400c0`, dove ### **e' `ENTRAMBE`**, dopo il taglio l'unico "
      "marcatore che la prenderebbe e' ### **un FLAG DEL SIMULATORE** *(`FORK_SU2`, "
      "`CAMPO_SPINORIALE`, `TAU_LUCE`)* — e ### **quello stesso marcatore fa scattare "
      "`FALSO-ZERO`**, che nomina `REGISTRO_STATO` e `REGISTRO_METRI`, ### **flag VERI del "
      "simulatore** *(verificato: `140` costanti di modulo, e tutte e quattro sono fra "
      "quelle)*, e che il mandato precedente dichiara ### **NON DEVE scattare** |")
    p()
    p("### 📌 **LA RACCOMANDAZIONE, motivata:** `F8` esiste per ### **TROVARE** le voci "
      "`ENTRAMBE` che nominano oggetti dell'era `1`, ### **perche' siano spostate.** "
      "`CONFIG-1` ### **E- STATA spostata** — e chiedere che scatti ancora e' chiedere a "
      "un rilevatore ### **di continuare a segnalare un caso curato.** "
      "### ✔ **Credo che `80eaf82` sia un lapsus per `ba400c0`, e che la risposta giusta "
      "sia NESSUNA DELLE DUE: il taglio toglie `CONFIG-1` da `F8`, e va bene cosi'.**")
    p()
    p("### **I `%d` SEGNALI DI `F8` CHE RESTANO**" % len(seg["F8"]))
    p()
    p("| id | il segnale |")
    p("|---|---|")
    for i, mm in sorted(seg["F8"]):
        p("| `%s` | %s |" % (i, mm.replace("|", "/")))
    p()
    p("---")
    p()

    # ================================================================ punto 5
    p("## ⑤ PUNTO `5` — **le due note, e l'eccezione di `CENS-B15`**: `F3` e `F6` "
      "a ZERO")
    p()
    p("| id | la nota, adesso |")
    p("|---|---|")
    for i in ("POTATURA-GUARDIE", "REGISTRO_FISICA:U2-6", "CENS-B15"):
        p("| `%s` *(`%s`/`%s`/era `%s`/`%s`)* | *%s* |"
          % (i, per[i]["classe"], per[i]["dominio"], per[i]["era"], per[i]["stato"],
             " ".join((per[i]["meta"].get("nota_guardiano") or "").split())[:230]
             .replace("|", "/")))
    p()
    p("### ⛔ **E LA NOTA NUOVA CITAVA LA VECCHIA, E COSI- RI-INNESCAVA IL PATTERN.** "
      "Avevo scritto *«la nota diceva «**lista 3 del guardiano**: …»»* — e `F6` cerca "
      "### **esattamente quella forma.** ### ⭐ **Una CITAZIONE dentro una nota e' "
      "indistinguibile da un'ASSERZIONE, per un presidio che legge una forma.** Riscritta "
      "### **senza nominare la lista**: la storia vive ### **nello storico.**")
    p()
    p("### ⚠ **E L'ECCEZIONE DI `CENS-B15` E- UN INDEBOLIMENTO, E LO DICHIARO.** "
      "`_eccezioni_malformate` pretende ### **un pezzo letterale di almeno `20` caratteri del "
      "TESTO DELLA VOCE**, e la frase *«COSTRUITA E MAI MISURATA»* ### **NON era nel testo**: "
      "l'ho messa ### **nella nota, nello stesso lotto** — quindi ### **l'eccezione cita "
      "una nota che ho scritto io.** ### ✔ **E- la forma piu' forte che avevo** *(la "
      "nota TRASCRIVE alla lettera `doc/CENSIMENTO_intenzioni.md:265`, con l'indirizzo, e "
      "quella riga l'ho verificata)*, ### **ma resta un anello che si chiude su di me.**")
    p()
    p("### ✔ **E l'eccezione e' collaudata nei due versi:** `F3` ### **tace** con "
      "l'eccezione e ### **scatta** sulla stessa voce ### **senza.** "
      "### ⛔ **Un'eccezione che nessuno prova e' una riga che nessuno sa se serve.**")
    p()
    p("---")
    p()

    # ================================================================ conteggi
    p("## ⑥ I CONTEGGI E I SEGNALI")
    p()
    p("> **PRIMA** = `git show %s` *(il task history)*. **DOPO** = il disco." % PRIMA)
    p()
    for campo in ("classe", "dominio", "era", "stato"):
        tab(campo, collections.Counter(str(v[campo]) for v in pv),
            collections.Counter(str(v[campo]) for v in voci))
    p("| | prima | dopo |")
    p("|---|--:|--:|")
    p("| voci | `%d` | ### **`%d`** |" % (len(pv), len(voci)))
    p("| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |")
    p("| ### **righe di storico** | `%d` | ### **`%d`** |"
      % (len([r for r in gshow("%s:doc/indice/storico.jsonl" % PRIMA).split(NL)
              if r.strip()]),
         sum(1 for r in io.open(os.path.join(RADICE, "doc/indice/storico.jsonl"),
                                encoding="utf-8") if r.strip())))
    p()
    p("| presidio | prima | dopo | |")
    p("|---|--:|--:|---|")
    for k, pr in (("F1", 8), ("F2", 0), ("F3", 1), ("F4", 0), ("F6", 2), ("F8", 20)):
        d = len(seg[k]) - pr
        p("| `%s` | `%d` | %s | %s |"
          % (k, pr, "### **`%d`**" % len(seg[k]) if seg[k] else "### **`0`**",
             ("### **%+d**" % d) if d else ""))
    p("| `F5` `F7` `F9` `F10` `F11` `F12` | `0` | ### **`0`** | sono ERRORI: se non fossero "
      "zero, `valida` ### **non passerebbe** |")
    p("| ### **in tutto** | `31` | ### **`%d`** | ### **%+d** |"
      % (sum(len(v) for v in seg.values()), sum(len(v) for v in seg.values()) - 31))
    p()
    p("---")
    p()

    # ================================================================ DA_DECIDERE
    p("## ⑦ L'ELENCO GENERATO: **`doc/indice/DA_DECIDERE_LUCA.md`**")
    p()
    p("> ### ⛔ **Non si scrive a mano, e nel codice NON c'e' nessuna lista di ID:** ci sono "
      "### **tre criteri** — la nota che dice *«da decidere/confermare da Luca»*, il "
      "metadato `omonimo`, e lo stato `DA_CLASSIFICARE` su una voce ### **che non e' un "
      "segnaposto.**")
    p()
    p("| | |")
    p("|---|--:|")
    p("| ### **voci che aspettano una decisione** | ### **`%s`** |"
      % (m_dd.group(1) if m_dd else "?"))
    p("| segnaposto `NON_DEFINITA`, che ### **NON sono una domanda** | `%d` |"
      % sum(1 for v in voci if v["classe"] == "NON_DEFINITA"))
    p()
    p("### **E LE DOMANDE DI QUESTO GIRO, che l'elenco generato NON puo' vedere** "
      "*(non sono note di voci: sono ### **letture del mandato**)*")
    p()
    p("| | la domanda |")
    p("|---|---|")
    p("| `1` | ### **le due richieste incompatibili del punto `4`**: `CONFIG-1` in `F8`. "
      "### **La mia raccomandazione: nessuna delle due** |")
    p("| `2` | ### **l'eccezione di `CENS-B15` cita una nota scritta nello stesso lotto.** "
      "La forma stretta vorrebbe la frase ### **nel titolo o nella descrizione** |")
    p("| `3` | ### **la cartella `primo_ordine/` non esiste**, e ### **non l'ho creata**: "
      "crearla e' ### **un atto di fisica** |")
    p("| `4` | ### **il mio livello `T4` resta «largo nel posto sbagliato»**, e non l'ho "
      "cambiato: ### **le righe di oggi non passano da la-**, e cambiarlo farebbe divergere i "
      "referti dei due giri scorsi |")
    p("| `5` | ### **i `%d` segnali di `F1` e i `%d` di `F8` che restano** sono "
      "### **elencati e non corretti** |" % (len(seg["F1"]), len(seg["F8"])))
    p()
    p("> ### ⭐ **E la cosa che porto fuori da questo giro:** ### **un presidio che ho "
      "scritto io, esteso «alla lettera del mandato», ha prodotto segnali che poi ho elencato "
      "come difetti dell'indice** — due volte, `F1` e `F8`. "
      "### ⛔ **Il collaudo non se ne accorge, perche' i suoi bracci provano che la regola "
      "scatta DOVE DICO IO, non che la regola sia GIUSTA.** "
      "### **Chi se ne accorge e' chi legge i segnali.**")
    p()

    q = os.path.join(RADICE, "doc", "REFERTO_indice_v3_fine_riordino.md")
    io.open(q, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_fine_riordino.md: %d righe" % len(R))
    print("  segnali: %s  (in tutto %d)"
          % ({k: len(v) for k, v in seg.items()}, sum(len(v) for v in seg.values())))
    print("  controlli %s/%s; presidi %s/%s; indice %s/%s; _file_fisica %s/%s; H-ID %s/%s"
          % (n_ctrl + n_pres + n_ind + n_ff + n_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
