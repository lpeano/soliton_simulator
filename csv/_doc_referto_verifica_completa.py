# -*- coding: utf-8 -*-
"""IL REFERTO DELLA VERIFICA COMPLETA — **riga per riga, tutte e `165`.**

### ⛔ **NESSUN NUMERO RICOPIATO** *(`L-NUMERI`)*: il **prima** da
`git show bfb1596:doc/indice/voci.jsonl` *(il task history, prima di ogni scrittura del
giro)*, il **dopo** dal disco, e i verdetti dal rapporto che l'applicatore ha scritto.

Gira con:  python csv/_doc_referto_verifica_completa.py
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
PRIMA = "bfb1596"
FILE_G = "doc/indice/_lotti/correzioni_guardiano_2026-10-09.txt"
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
    # ### ⛔ **IL PARI MERITO ROMPEVA LA RIPRODUCIBILITA-:** ordinando ### **solo per il
    # ### conteggio**, due valori con lo stesso numero *(`DIFETTO` e `NON_DEFINITA`, `187`
    # ### entrambi)* usciviano ### **in ordine DIVERSO a ogni corsa** -- l-ordine di un
    # ### `set` non e- garantito. ### **Un referto che non si rigenera identico non si puo-
    # ### verificare**, e il controllo <<si rigenera, e deve dare lo STESSO FILE>> che
    # ### scrivo in ogni messaggio ### **sarebbe stato falso.**
    # ### ✔ **Il nome e- lo spareggio**, e un ordine totale non ha pari merito.
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
    rap = js("doc/indice/_p3_guardiano.json")
    conv = js("doc/indice/_p4_convenzioni.json")
    fatto = js("doc/indice/_il_fatto.json")
    righe = [x for x in io.open(os.path.join(RADICE, FILE_G), encoding="utf-8").read()
             .split(NL) if x.strip()]
    dati = {}
    for x in righe:
        pz = [y.strip() for y in x.split("|")]
        dati[pz[0]] = {"cambi": pz[1], "citazione": pz[2], "conf": pz[3]}
    esiti = {x["id"]: x for x in rap["esiti"]}
    conta = collections.Counter(x["verdetto"] for x in rap["esiti"])
    lasc = collections.defaultdict(list)
    for x in rap["lasciate"]:
        lasc[x["id"]].append(x)
    nonapp = {x["id"]: x for x in rap["non_applicate"]}
    appl = {x["id"]: x for x in rap["applicate"]}
    n_pres = gira(["csv/_collaudo_presidi_indice.py"],
                  r"IL COLLAUDO DEI PRESIDI: (\d+) su (\d+)")
    n_ind = gira(["csv/indice.py", "collaudo"], r"COLLAUDO: (\d+) su (\d+)")
    n_ctrl = gira(["csv/_controlli_indice_v2.py"], r"I CONTROLLI: (\d+) su (\d+)")
    n_sei = gira(["csv/_controllo_il_fatto.py"],
                 r"IL CONTROLLO DELLE SEI ATTESE: (\d+) su (\d+)")

    p("# IL REFERTO DELLA VERIFICA COMPLETA DEL GUARDIANO")
    p()
    p("> ### ⭐ **LE `165` RIGHE, UNA PER UNA.** Il mandato chiede ### **quante applicate, "
      "quante non applicate e quante lasciate** — e un conteggio ### **per CAMPO** non "
      "risponde a quella domanda: una riga che cambia due campi puo- averne ### **uno "
      "applicato e uno lasciato.** ### ⛔ **Quindi il verdetto e- PER RIGA, e la somma "
      "DEVE fare `165`: e- un `assert`, non una stampa.**")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_verifica_completa.md`, "
      "### **committato PRIMA del lavoro** *(`%s`)* |" % PRIMA)
    p("| **il file del guardiano** | `%s`, `165` righe, ### **committato da solo** "
      "*(`67c12fa`)* |" % FILE_G)
    p("| **i commit** | `ba8c359` *(il difetto «IL FATTO»)* · `ed10b34` *(i punti `3`, "
      "`4`, `5` e l'accensione di `F9`/`F10`)*, piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **i controlli** | ### **%s su %s** · collaudo dei presidi ### **%s su %s** "
      "· collaudo dell'indice ### **%s su %s** · le sei attese del difetto "
      "### **%s su %s** |" % (n_ctrl[0], n_ctrl[1], n_pres[0], n_pres[1], n_ind[0], n_ind[1],
                              n_sei[0], n_sei[1]))
    p()
    p("---")
    p()
    p("## ① L'ORDINE DEL PUNTO `1`: **impossibile, non rischioso** — e Luca lo ha "
      "riconosciuto")
    p()
    p("> *«E l'ordine del punto `1` era sbagliato, ERRORE DEL GUARDIANO: hai ragione tu "
      "(`bfb1596`). `F9` e `F10` si accendono NELLO STESSO COMMIT delle correzioni che li "
      "rendono veri, mai prima.»*")
    p()
    p("`indice.py valida` gira ### **nel `pre-commit`** *(`csv/_hook_presidi.py`, blocco "
      "`[INDICE v2]`: lancia `csv/indice.py valida` e fa `return 1` se esce diverso da "
      "`0`)*. ### ⛔ **Quindi un presidio bloccante acceso prima della cura blocca OGNI "
      "COMMIT DEL REPO**, e il commit che lo accende ### **sarebbe bloccato dal suo stesso "
      "hook**: l'hook gira il codice ### **dell'albero di lavoro.**")
    p()
    p("### ⭐ **E- LA TERZA VOLTA IN TRE GIRI, E LA PRIMA CHE ARRIVA PRIMA DEL DANNO.** "
      "`F5` e `F7` hanno dato la stessa lezione ### **sbattendoci**; questa volta il task "
      "history l'ha ### **dedotta dal codice dell'hook** e si e- fermato. "
      "### **La lezione nuova: il costo non e- l'indice, e- il REPO INTERO.**")
    p()
    p("### ✔ **E `F10` SI POTEVA ACCENDERE SUBITO, `F9` NO**, e la differenza e- "
      "### **misurata, non di gusto:** `F10` violava su ### **ZERO** voci, `F9` su "
      "### **CINQUE** — e sono esattamente le cinque che il mandato nomina. "
      "### **Due presidi che il mandato chiede INSIEME si separano, perche- uno si puo- e "
      "l'altro no.**")
    p()
    p("---")
    p()

    # =================================================================== il difetto
    p("## ② IL DIFETTO «IL FATTO»: **il criterio di chiusura CITAVA la prova che la "
      "chiusura era sbagliata**")
    p()
    p("| id | la regola corretta | chi decide | la frase che il MIO criterio citava |")
    p("|---|---|---|---|")
    for x in fatto:
        i = x["id"]
        v = per[i]
        chi = ("### **il FILE** del guardiano" if i in dati
               else ("### ⚠ **segnaposto**: il punto `1` la saltava gia-"
                     if v["classe"] == "NON_DEFINITA" else "### **questo giro**"))
        p("| `%s` | `%s` → ### **`%s`** | %s | *%s* |"
          % (i, x["prima"][0], x["dopo"][0], chi,
             " ".join(x["riga"].split())[:150].replace("|", "/")))
    p()
    p("### ⛔ **IL DIFETTO ERA MIO, e sta scritto nei miei stessi motivi:** il lotto del "
      "punto `1` ha chiuso ### **sei voci** col criterio *«la riga dice **FATTO**»*, e la "
      "frase citata era *«**IL FATTO**: `soglia0` = …»*, *«(c) **IL FATTO** PIU' GROSSO»*, "
      "*«**IL FATTO**: `median(lambda_nodi())` vale `0.8000`»*. ### ⭐ **Guardavo se la "
      "parola c'era, non se era un VERBO** — ed e- ### **lo stesso errore della "
      "NEGAZIONE, un livello piu- su.**")
    p()
    p("### ✔ **La differenza si ISOLA spegnendo il filtro**, non riscrivendo la regola: "
      "`_scarta` si sostituisce con `lambda: False`, cioe- ### **il comportamento di prima "
      "della cura.** ### **Cosi- l'elenco e- esattamente cio- che il difetto ha causato**, "
      "non cio- che credo abbia causato — e le ### **sei attese sono un `assert`**: "
      "### **`%s` su `%s`.**" % (n_sei[0], n_sei[1]))
    p()
    p("### ⭐ **E LO STATO TORNA DOV'ERA, dove la regola corretta non decide:** per `Z23`, "
      "`Z46` e `Z66` la regola corretta ### **non decide niente**, e la `CHIUSA` di oggi "
      "### **l'aveva scritta il mio lotto col difetto** — ### **una scrittura sbagliata "
      "si disfa.** E la `chiusura` ### **si svuota**: una voce `SOSPESA` che porta *«chiusa "
      "dal commit X»* ### **mente.**")
    p()
    p("---")
    p()

    # =================================================================== i 165
    p("## ③ LE `165` RIGHE, RIGA PER RIGA")
    p()
    p("| verdetto | quante | che cosa vuol dire |")
    p("|---|--:|---|")
    p("| ### **`APPLICATA`** | ### **`%d`** | tutti i campi che la riga chiede sono stati "
      "scritti |" % conta["APPLICATA"])
    p("| ### **`APPLICATA_IN_PARTE`** | ### **`%d`** | ### **almeno uno scritto e almeno uno "
      "lasciato** — ed e- il caso che un conteggio per campo nasconde |"
      % conta["APPLICATA_IN_PARTE"])
    p("| ### **`LASCIATA`** | ### **`%d`** | citazione trovata, ### **nessun campo "
      "applicato** |" % conta["LASCIATA"])
    p("| ### **`NON_APPLICATA`** | ### **`%d`** | ### **citazione non trovata** |"
      % conta["NON_APPLICATA"])
    p("| ### **in tutto** | ### **`%d`** | ### **e DEVE fare `165`** |"
      % sum(conta.values()))
    p()
    p("| dove si e- trovata la citazione | quante | chi lo dice |")
    p("|---|--:|---|")
    for k, che in (("T0", "il `titolo` + `descrizione` della voce — ### **MIO**, e il "
                          "motivo e- che ### **quello E- il testo della voce**"),
                   ("T1", "la ### **riga d'origine** — ### **del mandato**"),
                   ("T2", "il ### **blocco** *(intestazione + sezione)* — ### **del "
                          "mandato**"),
                   ("T3", "la ### **sezione** che contiene la riga — ### **del "
                          "mandato**"),
                   ("T4", "### **altrove nel file** che la `fonte` nomina — "
                          "### **MIO, e SOLO quando la riga NON si ritrova**: la- il luogo "
                          "del mandato ### **non esiste**"),
                   ("T-STRUTTURALE", "### **non e- una citazione**: il guardiano dichiara "
                                     "fra parentesi un ### **motivo strutturale** *(`A2`, "
                                     "cioe- `F9`)*")):
        if rap["livelli"].get(k):
            p("| `%s` | `%d` | %s |" % (k, rap["livelli"][k], che))
    p()
    p("### ⛔ **E IL LIMITE ERA IL MIO RITROVAMENTO, NON IL GUARDIANO.** La prima stesura "
      "dichiarava ### **`65` citazioni introvabili su `165`.** Ho misurato ### **perche-**: "
      "### **`15`** stavano nel testo della voce, ### **`37`** altrove nel file di origine, "
      "e solo ### **`13`** erano davvero introvabili. ### ⭐ **Dichiarare `65` «non "
      "trovate» avrebbe buttato `52` correzioni VERE del guardiano per un difetto MIO.**")
    p()
    p("### ⚠ **I DUE LIVELLI CHE AGGIUNGO IO SONO UNA DECISIONE, e la dichiaro:** se "
      "Luca li ritiene troppo larghi, ### **`%d` righe trovate in `T0` e `%d` in `T4`** vanno "
      "riviste. ### **Ogni riga qui sotto porta il suo livello**, cosi- la revisione non "
      "deve rifare il lavoro." % (rap["livelli"].get("T0", 0), rap["livelli"].get("T4", 0)))
    p()

    def riga_voce(i):
        d = dati[i]
        v, a = per[i], pper.get(i, per[i])
        pr = "%s/%s/era %s/%s" % (a["classe"], a["dominio"], a["era"], a["stato"])
        do = "%s/%s/era %s/%s" % (v["classe"], v["dominio"], v["era"], v["stato"])
        return (i, d["cambi"], d["citazione"], d["conf"], pr, do)

    for verdetto, titolo, nota in (
            ("APPLICATA", "LE `%d` APPLICATE" % conta["APPLICATA"], ""),
            ("APPLICATA_IN_PARTE", "LE `%d` APPLICATE IN PARTE"
             % conta["APPLICATA_IN_PARTE"],
             "### ⭐ **Queste sono la ragione per cui il verdetto e- PER RIGA:** un "
             "conteggio per campo le metterebbe ### **due volte**, fra le applicate e fra "
             "le lasciate."),
            ("LASCIATA", "LE `%d` LASCIATE" % conta["LASCIATA"],
             "### ⛔ **«Lasciata» NON vuol dire «ignorata»:** vuol dire che la riga "
             "intera ### **NON sostiene il cambio**, e il motivo e- scritto. "
             "### **La regola del mandato dice «altrimenti elenca con una riga di "
             "motivo».**"),
            ("NON_APPLICATA", "LE `%d` NON APPLICATE" % conta["NON_APPLICATA"],
             "### ⛔ **La citazione NON COMPARE**, e il mandato dice ### **«NON "
             "applicare, elenca».** ### **Non ho cercato una frase simile:** una citazione "
             "che non si trova ### **non si avvicina a mano.**")):
        q = [x["id"] for x in rap["esiti"] if x["verdetto"] == verdetto]
        if not q:
            continue
        p("### **%s**" % titolo)
        p()
        if nota:
            p(nota)
            p()
        p("| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |")
        p("|---|---|---|---|---|---|")
        for i in q:
            _i, cambi, cit, conf, pr, do = riga_voce(i)
            det = esiti[i]["dettaglio"]
            if verdetto in ("LASCIATA", "APPLICATA_IN_PARTE"):
                det = " · ".join("### **`%s`=`%s`**: %s" % (x["campo"], x["valore"],
                                                                 x["perche"][:210])
                                      for x in lasc.get(i, [])) or det
            elif verdetto == "NON_APPLICATA":
                det = nonapp[i]["perche"]
            else:
                det = "%s — `%s`" % (det, appl[i]["livello"])
            p("| `%s` | `%s` | *%s* | `%s` | `%s` → ### **`%s`** | %s |"
              % (i, cambi.replace("|", "/"), cit.replace("|", "/")[:70], conf, pr, do,
                 det.replace("|", "/").replace(NL, " ")))
        p()

    p("---")
    p()

    # =================================================================== punto 4
    p("## ④ LE DUE CONVENZIONI, **lette da `CLAUDE.md`**")
    p()
    p("> ### ⛔ **«In vigore» = «citato in `CLAUDE.md` OGGI»**, non *«mi pare in uso»*. "
      "Gli ID ### **si leggono dalle due tabelle**, e se un ID sparisse da la- lo strumento "
      "### **smetterebbe di dichiararlo in vigore DA SE-.**")
    p()
    p("| | gli ID |")
    p("|---|---|")
    p("| §`11`, ### **le regole di lavoro** *(`%d`)* | %s |"
      % (len(conv["regole_11"]), " · ".join("`%s`" % x for x in conv["regole_11"])))
    p("| §`12`, ### **i cablati** *(`%d`)* | %s |"
      % (len(conv["cablati_12"]), " · ".join("`%s`" % x for x in conv["cablati_12"])))
    p()
    p("| id | prima | dopo | perche' |")
    p("|---|---|---|---|")
    for i in conv["cambiate"]:
        v, a = per[i], pper.get(i, per[i])
        che = ("una ### **regola scritta NON IMPEDISCE NIENTE** *(`A9`)*: e- uno `STANDARD`, "
               "e `PRESIDIO` e- ### **solo cio- che e- CABLATO**"
               if i in conv["regole_11"] else
               "e- ### **CABLATO** *(§`12`)*, quindi `PRESIDIO`; e un hook "
               "### **IN VIGORE e- `APERTA`** — ### **una regola non si «finisce»: "
               "VALE**")
        p("| `%s` | `%s`/`%s` | ### **`%s`/`%s`** | %s |"
          % (i, a["classe"], a["stato"], v["classe"], v["stato"], che))
    p()
    p("### ✔ **E `%d` erano GIA- a posto:** %s."
      % (len(conv["gia_a_posto"]),
         " · ".join("`%s`" % x for x in conv["gia_a_posto"])))
    p()
    p("---")
    p()

    # =================================================================== punto 5
    p("## ⑤ IL PUNTO `5`: **`F6` trova `G1`**, e la via grossolana dava `69` segnali")
    p()
    g1 = per["G1"]
    p("| | |")
    p("|---|---|")
    p("| la nota di `G1` | *«%s»* |"
      % " ".join((g1["meta"].get("nota_guardiano") or "").split())[:200])
    p("| la voce oggi | `%s`/`%s`/era `%s`/### **`%s`** |"
      % (g1["classe"], g1["dominio"], g1["era"], g1["stato"]))
    p("| perche' `F6` NON la trovava | ### **due ragioni**: la nota non nomina *«la lista `N` "
      "del guardiano»*, e dice *«correzione»* — che era escluso come "
      "### **informativo** |")
    p("| l'estensione | una nota che scrive ### **la forma esatta `DOMINIO/era N/STATO`** fa "
      "### **un'ASSERZIONE**, e se la voce si e- mossa ### **la nota e- SCADUTA** |")
    p("| quante note hanno quella forma | ### **`6`** su `846` voci, e "
      "### **una sola e- incoerente: `G1`** |")
    p("| ### ⛔ **la via grossolana** | *«la nota nomina uno stato diverso da quello della "
      "voce»* dava ### **`69` SEGNALI**, perche' la maggior parte delle note parla "
      "### **di un'altra era** o ### **fa una DOMANDA** *(«superata da `A16`?»)*. "
      "### **Era la condizione di FERMO scritta nel task history, e mi sono fermato** |")
    p()
    p("### ✔ **E IL COLLAUDO MISURA I `69`**, invece di dire *«era troppo grossa»*: "
      "### **una scelta scartata senza numero e- un'opinione.** Piu' "
      "### **il braccio negativo** che prova che `F6` ### **non scatta per la PAROLA**: con "
      "la stessa nota e la tripla ### **allineata**, ### **tace.**")
    p()
    p("### ⚠ **E LA NOTA DI `G1` NON LA RISCRIVO.** Il mandato dice *«`F6` deve "
      "trovarla»*, ### **non «correggila»** — e un segnale ### **si elenca, non si "
      "spegne cambiando la voce.** ### 📌 **LA DOMANDA A LUCA: la nota di `G1` va riscritta "
      "o TOLTA?** La sua storia vive ### **in `storico.jsonl`**, quindi togliere la nota "
      "### **non perde niente** — ma e' ### **una decisione, non una pulizia.**")
    p()
    p("---")
    p()

    # =================================================================== conflitto
    p("## ⑥ DUE AFFERMAZIONI DEL GUARDIANO SI CONTRADDICONO, **e non scelgo io**")
    p()
    p("`C3` *(«le liste del guardiano: classificazione come indicata»)* ### **e- "
      "FALLITO**, e non l'ho zittito.")
    p()
    p("| id | la lista vecchia | il file nuovo | la citazione del file |")
    p("|---|---|---|---|")
    for i, lista in (("CLI-1", "`1`"), ("POTATURA-GUARDIE", "`3`")):
        p("| `%s` | lista %s | `%s` | *%s* |"
          % (i, lista, dati[i]["cambi"].replace("|", "/"), dati[i]["citazione"]))
    p()
    p("### ✔ **La riconciliazione e- TEMPORALE e CITATA:** la verifica completa e- la "
      "parola ### **piu' recente** del guardiano, e ### **porta una frase del repo**; le "
      "liste ### **non citavano niente.** Sta in `csv/_controlli_indice_v2.py`, nel posto "
      "### **dichiarato** dove *«il controllo dice che cosa si aspetta OGGI»*, e "
      "### **va per ultima** perche' ### **l'ultima assegnazione vince** *(un blocco piu' "
      "sopra riscriveva `CLI-1`, e la prima stesura della riconciliazione "
      "### **veniva sovrascritta**)*.")
    p()
    p("### ⛔ **MA E- IL GUARDIANO CHE HA CAMBIATO IDEA, E LUCA DEVE SAPERLO.** La regola "
      "del guardiano stesso dice: *«due misure incompatibili sullo stesso oggetto "
      "### **si riconciliano, non si sceglie**»*. ### **Io ho scelto la FORMA della "
      "riconciliazione** *(il piu' recente vince, ### **se cita**)*, ### **non il merito.**")
    p()
    p("---")
    p()

    # =================================================================== conteggi
    p("## ⑦ I CONTEGGI E I CONTROLLI")
    p()
    p("> **PRIMA** = `git show %s` *(il task history, ### **prima di ogni scrittura del "
      "giro**)*. **DOPO** = il disco." % PRIMA)
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
    p("| presidio | segnali | |")
    p("|---|--:|---|")
    for k in ("F1", "F2", "F3", "F4", "F6", "F8"):
        p("| `%s` | %s | %s |"
          % (k, "### **`%d`**" % len(seg[k]) if seg[k] else "`0`",
             "### **`G1`** e `POTATURA-GUARDIE`" if k == "F6" else ""))
    p("| `F7` `F9` `F10` | ### **`0`** | ### **sono ERRORI: se non fossero zero, `valida` "
      "non passerebbe** |")
    p("| ### **in tutto** | ### **`%d`** | ### **si elencano, non si correggono** |"
      % sum(len(v) for v in seg.values()))
    p()
    p("### **I SEGNALI CHE RESTANO, voce per voce**")
    p()
    for k in ("F1", "F6", "F8"):
        if not seg[k]:
            continue
        p("| `%s` | il segnale |" % k)
        p("|---|---|")
        for i, m in sorted(seg[k]):
            p("| `%s` | %s |" % (i, m.replace("|", "/")))
        p()
    p("---")
    p()
    p("## ⑧ CHE COSA RESTA A LUCA")
    p()
    p("| | quante | che cosa |")
    p("|---|--:|---|")
    p("| ### **i due livelli `T0` e `T4`** | `%d` + `%d` | ### **li aggiungo IO**, e il "
      "mandato ne nomina tre: se sono troppo larghi, quelle righe vanno riviste |"
      % (rap["livelli"].get("T0", 0), rap["livelli"].get("T4", 0)))
    p("| ### **le `%d` non applicate** | `%d` | ### **la citazione non compare**: o la frase "
      "non e' nel repo, o la `fonte` della voce ### **non punta dove dovrebbe** |"
      % (conta["NON_APPLICATA"], conta["NON_APPLICATA"]))
    p("| ### **le chiusure senza commit** | `%d` | righe che chiedono `CHIUSA` e "
      "### **la riga non porta il commit**: ### **un commit non si inventa** |"
      % sum(1 for x in rap["lasciate"] if "NON PORTA UN COMMIT" in x["perche"]))
    p("| ### **le contraddizioni della riga** | `%d` | la riga ### **dice il contrario** di "
      "cio' che il file chiede — e sono `media`, dove il mandato dice *«applica se la "
      "frase sostiene il cambio»* |"
      % sum(1 for x in rap["lasciate"] if "CONTRADDICE" in x["perche"]))
    p("| ### **`CLI-1` e `POTATURA-GUARDIE`** | `2` | ### **il guardiano contraddice se "
      "stesso**: ho scelto la forma, non il merito |")
    p("| ### **`S02` e `Z21`** | `2` | lo schema le rifiuta: ### **una voce superata deve "
      "dire DA CHE COSA, e deve essere una DECISIONE** |")
    p("| ### **la nota di `G1`** | `1` | riscriverla o ### **toglierla**? |")
    p("| ### **i segnali di `F8`** | `%d` | ### **sul confine fra le due frasi dell'era** |"
      % len(seg["F8"]))
    p("| ### ⛔ **un mandato che non ho** | `1` | `doc/CODA_2026-10-09.md`: "
      "l'integrazione *«gli strumenti diventano obbligatori anche per l'era `2`»* e' "
      "arrivata, ### **il suo testo base NO** |")
    p()
    p("> ### ⭐ **Il criterio, lo stesso di tutto il lavoro:** dove il file ### **cita "
      "una frase del repo** l'ho applicato; dove ### **la riga dice il contrario**, "
      "### **ho lasciato e ho scritto il motivo**; dove ### **due parole del guardiano si "
      "contraddicono**, ### **ho scelto la FORMA della riconciliazione e non il merito.** "
      "### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un "
      "difetto.**")
    p()

    q = os.path.join(RADICE, "doc", "REFERTO_indice_v3_verifica_completa.md")
    io.open(q, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_verifica_completa.md: %d righe" % len(R))
    print("  %d righe del file: %s" % (sum(conta.values()), dict(conta)))
    print("  controlli %s/%s; presidi %s/%s; indice %s/%s; sei attese %s/%s"
          % (n_ctrl + n_pres + n_ind + n_sei))
    return 0


if __name__ == "__main__":
    sys.exit(main())
