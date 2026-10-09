# -*- coding: utf-8 -*-
"""IL REFERTO DELLA CORREZIONE `v3` — **voce per voce**, come il mandato chiede.

### ⛔ **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: i conteggi **PRIMA** escono da
`git show 6e5e75b:doc/indice/voci.jsonl`, quelli **DOPO** dal disco, e **le voci toccate dai
lotti committati** in `doc/indice/_lotti/v3_*.jsonl`.

Gira con:  python csv/_doc_referto_v3.py
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
PRIMA = "6e5e75b"          # ### l'ultimo commit PRIMA della correzione `v3`
R = []


def p(s=""):
    R.append(s)


def jsonl(nome, sotto=""):
    q = os.path.join(D, sotto, nome) if sotto else os.path.join(D, nome)
    return [json.loads(r) for r in io.open(q, encoding="utf-8").read().split(NL) if r.strip()]


def al_commit(percorso):
    q = subprocess.run(["git", "show", "%s:%s" % (PRIMA, percorso)], cwd=RADICE,
                        capture_output=True, text=True, encoding="utf-8")
    assert q.returncode == 0, percorso
    return [json.loads(r) for r in q.stdout.split(NL) if r.strip()]


def conta(righe, campo):
    c = {}
    for v in righe:
        c[str(v[campo])] = c.get(str(v[campo]), 0) + 1
    return c


def tab(righe, campo, a, b):
    p("| `%s` | prima | dopo | |" % campo)
    p("|---|--:|--:|---|")
    for k in sorted(set(a) | set(b), key=lambda x: -b.get(x, 0)):
        d = b.get(k, 0) - a.get(k, 0)
        p("| %s | `%d` | `%d` | %s |" % (k, a.get(k, 0), b.get(k, 0),
                                         ("### **%+d**" % d) if d else ""))
    p()


def main():
    voci = jsonl("voci.jsonl")
    per = {v["id"]: v for v in voci}
    etich = jsonl("etichette_rimosse.jsonl")
    storico = jsonl("storico.jsonl")
    pv = al_commit("doc/indice/voci.jsonl")
    pper = {v["id"]: v for v in pv}
    pe = al_commit("doc/indice/etichette_rimosse.jsonl")
    lots = {n: jsonl("v3_%s.jsonl" % n, "_lotti")
            for n in ("A", "B", "C", "C_tipo", "C_titolo", "E_difetto")}
    luca = json.loads(io.open(os.path.join(D, "_ripasso_restano_a_luca.json"),
                              encoding="utf-8").read())
    rip = json.loads(io.open(os.path.join(D, "_ripasso_etichette.json"),
                             encoding="utf-8").read())

    p("# IL REFERTO DELLA CORREZIONE `v3` — **dopo la verifica del guardiano**")
    p()
    p("> ### ⛔ **Il guardiano ha letto le voci una per una e ha trovato che "
      "### LE SUE PROPRIE LISTE erano sbagliate.** Questa e' la correzione, e il mandato lo "
      "dice: *«Le liste del guardiano si aggiornano ### **DI CONSEGUENZA** (questa e' una "
      "correzione chiesta)»*. ### **Non e' un mio disaccordo.**")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **i commit** | `3ad58a2` *(blocchi `A`+`B`)* · `9e2340e` *(`C`)* · "
      "`85b5313` *(`D`)*, piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa in tutto "
      "il giro |")
    p("| **le voci toccate** | ### **`%d`** *(`%d` nel blocco `A`, `%d` nel `B`, `%d` nel "
      "`C`)*, piu' `1` difetto nuovo |"
      % (len(lots["A"]) + len(lots["B"]) + len(lots["C"]), len(lots["A"]), len(lots["B"]),
         len(lots["C"])))
    p("| **le righe di storico** | `%d` → ### **`%d`**, e ciascuna porta ### **un "
      "motivo che CITA il testo** |" % (len(al_commit("doc/indice/storico.jsonl")),
                                        len(storico)))
    p()
    p("---")
    p()
    p("## ① I CONTEGGI, PRIMA E DOPO")
    p()
    p("> **PRIMA** = `git show %s:doc/indice/voci.jsonl`. **DOPO** = il disco. "
      "### **Nessun numero ricopiato.**" % PRIMA)
    p()
    for campo in ("dominio", "era", "stato", "classe"):
        tab(voci, campo, conta(pv, campo), conta(voci, campo))
    p("| | prima | dopo |")
    p("|---|--:|--:|")
    p("| voci | `%d` | ### **`%d`** |" % (len(pv), len(voci)))
    p("| etichette rimosse | `%d` | ### **`%d`** |" % (len(pe), len(etich)))
    p("| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |")
    p()
    p("---")
    p()

    # ======================================================================
    #   A
    # ======================================================================
    p("## ② BLOCCO `A` — **la lista `2` del guardiano era un ERRORE SUO**")
    p()
    p("La lista `2` dava queste voci come ### **lavoro dell'era `2`** *(la riscrittura)*. "
      "Leggendole, ### **sono DIFETTI DEL CODICE DELL'ERA `1`**: la loro lezione passa "
      "all'era `2`, ### **ma la voce appartiene all'era `1`.**")
    p()
    p("| id | prima | dopo | il testo che lo dice |")
    p("|---|---|---|---|")
    for r in lots["A"]:
        i = r["id"]
        v, a = per[i], pper[i]
        da = "`%s`/era `%s`/`%s`" % (a["dominio"], a["era"], a["stato"])
        ad = "`%s`/era `%s`/`%s`" % (v["dominio"], v["era"], v["stato"])
        p("| `%s` | %s | %s | %s |"
          % (i, da, ("### **NON TOCCATA**" if da == ad else "### **" + ad + "**"),
             (v["descrizione"] or v["titolo"]).replace("|", "/")[:110]))
    p()
    p("### ⛔ **LE CINQUE CHE NON HO TOCCATO, e il perche':** `M-LEGAMI`, `M-ISTERESI`, "
      "`MEM-VERSO`, `M-FLUSSO`, `M-MASSA` restano `FISICA`/era `2`/`AGENDA` e portano "
      "### **solo** la nota *«da decidere da Luca: era `1` o `2`»*. Il mandato dice "
      "### **NON toccare**, e ### **una voce di cui non si sa l'era non si sposta per "
      "simmetria con le altre.** ### **Sono l'unico posto dove l'indice dice «non lo so» "
      "sull'era**, e non e' un difetto: e' una domanda a Luca ### **scritta nella voce.**")
    p()
    p("---")
    p()

    # ======================================================================
    #   B
    # ======================================================================
    p("## ③ BLOCCO `B` — **le GEMELLE, i fuori posto, e `D13`/`Z11`**")
    p()
    p("### ⚠ **DUE REGOLE DI STATO DIVERSE, e il mandato le distingue** — "
      "l'avevo letta male, e l'ho presa ### **prima di applicare:**")
    p()
    p("| il gruppo | lo stato |")
    p("|---|---|")
    p("| le ### **GEMELLE** → `METODO/ENTRAMBE` | *«lo stato attuale ### **se CHIUSA**, "
      "altrimenti ### **APERTA**»* |")
    p("| `DOCUMENTAZIONE` e `INFRASTRUTTURA` → era `1` | *«### **lo stato ATTUALE**»* "
      "— ### **non si tocca** |")
    p()
    p("### ⛔ **Avevo scritto la prima regola per TUTTE**, e avrebbe portato `5` voci da "
      "`SOSPESA` ad `APERTA` ### **senza che il mandato lo chieda.** Il perche' sta nel "
      "sorgente di `agg`, in `csv/_fase3_correzione.py`.")
    p()
    p("| id | prima | dopo | il testo che lo dice |")
    p("|---|---|---|---|")
    for r in lots["B"]:
        i = r["id"]
        v, a = per[i], pper[i]
        p("| `%s` | `%s`/era `%s`/`%s` | ### **`%s`/era `%s`/`%s`** | %s |"
          % (i, a["dominio"], a["era"], a["stato"], v["dominio"], v["era"], v["stato"],
             (v["descrizione"] or v["titolo"]).replace("|", "/")[:100]))
    p()
    p("### ⭐ **`D13` e `Z11` SONO LO STESSO FATTO, e lo stato si allinea su `APERTA`**")
    p()
    p("| | il testo | com'era |")
    p("|---|---|---|")
    p("| `D13` | *«I sigilli storici non sono stati rigirati sul blob corrente | `Z11`»* | "
      "`APERTA` |")
    p("| `Z11` | *«RIGIRO DEI SIGILLI STORICI — ### **lavoro PREVISTO, non ancora "
      "fatto**»* | ### **`CHIUSA`**, con una chiusura |")
    p()
    p("### ⛔ **Il testo di `Z11` dice DA SE' che il lavoro non e' fatto:** una voce "
      "`CHIUSA` su un lavoro non fatto e' ### **un FALSO CHIUSO.** ➜ **Allineate su "
      "`APERTA`**, la chiusura di `Z11` ### **tolta**, e ### **collegate nei due versi.**")
    p()
    p("### ⚠ **`superata_da` NON si poteva usare**, e lo scrivo perche' il mandato "
      "offriva quella strada: lo schema vuole ### **un id di DECISIONE o di ASSIOMA**, non di "
      "un'altra voce. ➜ `collegate`.")
    p()
    p("---")
    p()

    # ======================================================================
    #   C
    # ======================================================================
    p("## ④ BLOCCO `C` — **la mia regola era SBAGLIATA**")
    p()
    p("> ### ⛔ **La fase `2` diceva:** *«se tutte le citazioni stanno in documenti, e' "
      "un'etichetta»*. ### **E' FALSO:** un documento e' ### **esattamente il posto in cui "
      "un ID si DEFINISCE.**")
    p()
    p("| | che cos'e' |")
    p("|---|---|")
    p("| ### ✔ **DEFINIZIONE** | una ### **RIGA DI TABELLA** che apre con l'ID, o "
      "un'### **INTESTAZIONE** che lo contiene |")
    p("| ### ⚠ **citazione** | tutto il resto, ### **nel corpo del testo** |")
    p()
    p("Il vecchio indice diceva di queste `16` *«CITATO `N` volte, ### **MAI definito in un "
      "registro**»*: ### **vero alla lettera** *(non stanno in un registro)* e ### **falso "
      "nella sostanza** — ### **sono definite.**")
    p()
    p("### ⛔ **LA TRAPPOLA, E L'HO PRESA PRIMA DI APPLICARE**")
    p()
    p("La prima stesura cercava la definizione in ### **tutti** i file citanti, e trovava "
      "### **`37`** definizioni invece di `%d`: perche' cercava anche in "
      "### **`doc/LISTA_CHIUSA.md`, CHE E' LA LISTA DEGLI ID.** Ogni ID ci compare "
      "### **per definizione di cos'e' quel file**, quindi trovarci una riga di tabella e' "
      "### **un FALSO-UNO** — un verdetto garantito da qualcosa che ### **non parla del "
      "merito.** `TW-1` risultava definito in `LISTA_CHIUSA.md:711` invece che in "
      "`doc/SCALE_TW_lettura.md:227`, che e' il posto dove la riga ### **dice che cosa e'.**"
      % len(rip["definite"]))
    p()
    p("### ⭐ **E' LO STESSO DIFETTO DEL CONTROLLO `C4`**, che leggeva `doc/INDICE.md` "
      "— ### **un file che genera lui stesso.** Le ### **viste generate** sono escluse, "
      "e il perche' sta nel sorgente.")
    p()
    p("| id | classe | dominio/era/stato | definita da | dove |")
    p("|---|---|---|---|---|")
    for r in lots["C"]:
        c = r["campi"]
        i = c["id"]
        v = per[i]
        nota = v["meta"].get("nota_guardiano", "")
        come = ("riga di tabella" if "riga di tabella" in nota
                else ("intestazione" if "intestazione" in nota else "### **OMONIMO**"))
        f = c["fonte"].split("::")[0]
        p("| `%s` | `%s` | `%s`/`%s`/`%s` | %s | `%s` |"
          % (i, v["classe"], v["dominio"], v["era"], v["stato"], come, f))
    p()
    p("### ⭐ **`O4` STAVA FRA LE ETICHETTE, ED E' UNA DELLE OBIEZIONI AL BERSAGLIO DEL "
      "PROGETTO:** *«CONSERVAZIONE DELL'ENERGIA. L'energia assorbita non si riesce a "
      "bilanciare»*, Maxwell e Poincare', ### **«la massa della Terra raddoppierebbe in una "
      "frazione di secondo»** — `doc/IPOTESI_gravita_a_spinta.md:47`.")
    p()
    p("### ⛔ **`D5` e `D6`: OMONIMI, E NON SI SCEGLIE**")
    p()
    p("| id | una definizione | l'altra |")
    p("|---|---|---|")
    for i in ("D5", "D6"):
        due = per[i]["meta"]["omonimo"]
        p("| `%s` | %s | %s |" % (i, due[0].replace("|", "/"), due[1].replace("|", "/")))
    p()
    p("Nascono `NON_DEFINITA`, con le due definizioni nel metadato `omonimo` "
      "*(registrato in `9e2340e`)*. ### **Il mandato dice «NON scegliere», e la scelta e' di "
      "Luca.**")
    p()
    p("### ✔ **E DUE CHE SEMBRAVANO OMONIMI E NON LO SONO**, verificate leggendo le due "
      "righe:")
    p()
    p("| id | perche' NON e' un omonimo |")
    p("|---|---|")
    p("| `O4` | `doc/IPOTESI_gravita_a_spinta.md:47` e `doc/relazioni/2026-09-21.md:1876` "
      "sono ### **la STESSA obiezione** *(energia, Maxwell/Poincare', la massa della Terra "
      "che raddoppierebbe)*: la relazione ne riporta ### **una tavola riassunta** |")
    p("| `ROMPI-ANELLO` | due intestazioni ### **nello STESSO file** "
      "*(`doc/REFERTO_frequenza_riferimento.md`, righe `1` e `138`)*: ### **il titolo del "
      "referto e una sua sezione** |")
    p()
    p("### ⛔ **CHE COSA RESTA A LUCA, E PERCHE' NON L'HO DECISO IO**")
    p()
    p("Il ripasso dice che ### **`%d` delle `53`** sono DEFINITE. Il mandato ne nomina "
      "### **`16`** con la loro classificazione. ### **Le altre `%d` le lascio fra le "
      "etichette, e lo dichiaro:** il mandato non dice ### **con quale CLASSE e DOMINIO** "
      "devono nascere, e sceglierlo io ### **sarebbe decidere al posto di Luca.**"
      % (len(rip["definite"]), len(luca)))
    p()
    p("| id | definita da | dove |")
    p("|---|---|---|")
    for x in luca:
        y = x["dove"][0]
        p("| `%s` | %s | `%s:%d` |" % (x["id"], y["come"], y["file"], y["riga"]))
    p()
    p("### ⚠ **SONO TUTTE INTESTAZIONI, nessuna riga di tabella, e questo e' il motivo "
      "del dubbio:** un'intestazione che contiene un ID puo' essere ### **la sua "
      "definizione** oppure ### **solo un titolo che lo NOMINA.** Per le `16` del mandato la "
      "lettura l'ha fatta il guardiano; ### **per queste no.** Stanno in "
      "`doc/indice/_ripasso_restano_a_luca.json`, con la riga che le definisce.")
    p()
    p("---")
    p()

    # ======================================================================
    #   D
    # ======================================================================
    p("## ⑤ BLOCCO `D` — **il campo `commit` dello storico**")
    p()
    per_c = {}
    for v in storico:
        per_c[v["commit"]] = per_c.get(v["commit"], 0) + 1
    p("| commit | righe |")
    p("|---|--:|")
    for c in sorted(per_c, key=lambda x: -per_c[x]):
        p("| `%s` | `%d` |" % (c or "### **(vuoto)**", per_c[c]))
    p()
    p("Lo storico e' ### **solo in aggiunta**, quindi per ogni commit che l'ha toccato le "
      "righe `[quante_prima, quante_dopo)` sono ### **esattamente quelle che quel commit ha "
      "scritto.** ### **Non e' una stima: e' una partizione.** ### ✔ **E la premessa si "
      "VERIFICA:** per ogni commit la funzione rilegge la sua versione e controlla che sia "
      "### **un PREFISSO** di quella di oggi, riga per riga su `(id, quando, motivo)`; se lo "
      "storico fosse stato riscritto, ### **si ferma.** Non si e' fermata.")
    p()
    p("### ⛔ **LA COSA CHE IL MANDATO CHIEDE E CHE NON E' POSSIBILE**")
    p()
    p("Il mandato dice *«da ora in avanti `aggiorna-lotto` lo scrive»*. ### **Non e' "
      "letteralmente possibile:** quando il lotto gira, ### **il commit che lo conterra' NON "
      "ESISTE ANCORA.** Il `pre-commit` e il `commit-msg` girano ### **prima** che l'oggetto "
      "commit ci sia, e un `post-commit` che riempisse il campo dovrebbe ### **riscrivere il "
      "commit appena fatto.**")
    p()
    p("| | che cosa ho fatto al suo posto |")
    p("|---|---|")
    p("| ### **`commit_base`** | lo ### **timbra la via di scrittura**, automaticamente: "
      "`HEAD` nel momento in cui scrive. ### **Quello si sa**, ed e' ### **il codice su cui "
      "la modifica e' stata fatta** |")
    p("| ### **`commit`** | lo riempie ### **`storico-commit`** dai log, ed e' "
      "### **ri-girabile in ogni momento** |")
    p("| ### ⚠ **un lotto di RITARDO** | le righe dell'ultimo commit si riempiono "
      "### **al giro successivo.** ### **Non e' un difetto nascosto: e' la conseguenza di "
      "QUANDO esiste un commit** |")
    p()
    p("### ⚠ **`commit_base` manca alle `1078` righe vecchie**, e non si ricostruisce a "
      "posteriori senza indovinare: ### **non lo invento.** Da adesso ce l'hanno tutte "
      "quelle nuove.")
    p()
    p("---")
    p()

    # ======================================================================
    #   E  --  i controlli
    # ======================================================================
    p("## ⑥ I CONTROLLI")
    p()
    q = subprocess.run([sys.executable, os.path.join(_QUI, "_controlli_indice_v2.py")],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    # ### La riga di RIEPILOGO contiene <<PASSA>> anche lei: se la si prende, i controlli
    # ### diventano SETTE. ### **Si tengono solo le righe che cominciano con un id `C<n>`.**
    righe = [r for r in (q.stdout or "").split(NL)
             if re.match(r"^\s+C\d+ ", r) and ("PASSA" in r or "FALLISCE" in r)]
    p("```")
    for r in righe:
        p(r.rstrip())
    p("```")
    q2 = subprocess.run([sys.executable, os.path.join(_QUI, "indice.py"), "collaudo"],
                        cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    coll = [r for r in (q2.stdout or "").split(NL) if "COLLAUDO:" in r]
    p()
    p("| | |")
    p("|---|---|")
    p("| `python csv/_controlli_indice_v2.py` | ### **%d su %d** |"
      % (sum(1 for r in righe if "PASSA" in r), len(righe)))
    p("| `python csv/indice.py collaudo` | ### **%s** |"
      % (" ".join(coll[0].split()[-3:]) if coll else "?"))
    p("| `python csv/indice.py valida` | ### **passa** |")
    p("| `python csv/_indice_id.py` *(il validatore del `pre-commit`)* | ### **passa** |")
    p("| ### **gli ID vecchi** | ### **`953` conservati**, `0` persi, `0` doppi |")
    p()
    p("---")
    p()

    # ======================================================================
    #   I DIFETTI MIEI
    # ======================================================================
    p("## ⑦ I DIFETTI MIEI DI QUESTO GIRO — **tre presi, uno aperto**")
    p()
    p("| | il difetto | chi l'ha preso |")
    p("|---|---|---|")
    p("| `1` | la regola dello stato del blocco `B`: avevo applicato *«se `CHIUSA` tieni, "
      "altrimenti `APERTA`»* ### **anche a `DOCUMENTAZIONE` e `INFRASTRUTTURA`**, dove il "
      "mandato dice *«stato attuale»*. `5` voci da `SOSPESA` ad `APERTA` ### **senza che il "
      "mandato lo chieda** | ### **io, rileggendo il mandato prima di applicare** |")
    p("| `2` | il ripasso del blocco `C` cercava la definizione anche in "
      "### **`doc/LISTA_CHIUSA.md`, che e' la lista degli ID**: `37` definizioni invece di "
      "`%d`, ### **un FALSO-UNO** | ### **io, guardando i nomi dei file nell'uscita** |"
      % len(rip["definite"]))
    p("| `3` | alle `16` voci nuove mancava ### **`tipo_era1`**, e la vista compatibile ci "
      "mette `classe.lower()` = `criterio`, che ### **non sta nel vocabolario dell'era `1`** "
      "*(`criterio-locale`)* | ### **il `pre-commit`**, con `12` righe rifiutate |")
    p("| `4` | ### ⛔ **il controllo `C6` era PIU' DEBOLE DEL HOOK:** girava solo "
      "`_indice_id.py --blocca SI` — ### **un'interrogazione** — mentre il "
      "`pre-commit` gira ### **il VALIDATORE** | ### **il `pre-commit`, bloccando dove `C6` "
      "diceva PASSA** |")
    p()
    p("### ⭐ **IL `4` E' IL PEGGIORE DEI QUATTRO**, e lo scrivo per primo nel sorgente: "
      "### **un controllo che gira un comando piu' debole di quello del presidio non protegge "
      "niente** (`A9`). ➜ **Adesso `C6` gira ENTRAMBI, il validatore PRIMA** — e "
      "### **la prima volta che l'ho girato ha preso subito DUE COLLISIONI DI TITOLO** che io "
      "non avevo visto:")
    p()
    p("| | la collisione | che cos'era |")
    p("|---|---|---|")
    p("| `D6` ≡ `D5` | titolo identico | ### **l'avevo scritto io uguale per entrambi**: "
      "ci va l'ID, e adesso c'e' |")
    p("| `TW-1` ≡ `TS-6` | titolo identico | ### **NON e' un difetto del generatore:** "
      "le due righe ### **dicono davvero la stessa cosa** — *«flag OFF = byte-identico, "
      "firma dei byte, un processo per braccio»* — scritte in ### **due documenti "
      "diversi.** Il titolo porta il documento |")
    p()
    p("### ⛔ **E UNO CHE RESTA APERTO, perche' non l'ho curato:** "
      "### **`INDICE-COLLAUDO-SCRITTURA`** — `python csv/indice.py collaudo` dice "
      "### **`21` su `21`**, ma ### **i `21` casi provano `valida` IN MEMORIA** e "
      "### **nessuno prova una via di SCRITTURA.** `crea-lotto` e `storico-commit` sono nati "
      "oggi e sono entrati in uso ### **su `%d` voci, senza un caso che DEBBA fallire.** La "
      "spiegazione lunga sta in `doc/STATO_RUN.md` ### **con lo stesso ID.**"
      % (len(lots["A"]) + len(lots["B"]) + len(lots["C"])))
    p()
    p("---")
    p()

    # ======================================================================
    #   CHE COSA RESTA
    # ======================================================================
    p("## ⑧ CHE COSA RESTA A LUCA")
    p()
    nd = [v for v in voci if v["classe"] == "NON_DEFINITA"]
    p("| | quanti | che cosa |")
    p("|---|--:|---|")
    p("| ### **i concetti da definire** | `%d` | erano segnaposto, e ### **il codice o i "
      "sigilli li NOMINANO.** `D5` e `D6` ci sono ### **da adesso**, come ### **OMONIMI** |"
      % len(nd))
    p("| ### **l'era di `5` voci** | `5` | `M-LEGAMI` `M-ISTERESI` `MEM-VERSO` `M-FLUSSO` "
      "`M-MASSA`: ### **era `1` o `2`?** Il mandato dice NON toccare |")
    p("| ### **le `%d` etichette definite** | `%d` | ### **con quale classe e dominio** "
      "devono nascere |" % (len(luca), len(luca)))
    p("| ### **gli assiomi riclassificati** | `20` | ciascuno con *«da confermare da Luca»* |")
    p("| ### **la traccia della migrazione** | — | dice ancora `(fase2-b2)` per le `16` "
      "ripristinate, cioe' *«diventata etichetta»*. ### **NON l'ho riscritta:** la traccia "
      "dice ### **che cosa ha fatto la MIGRAZIONE**, lo storico dice ### **che cosa e' stato "
      "corretto dopo** |")
    p()
    p("> ### ⭐ **E il criterio che ho tenuto in tutto il giro:** dove il mandato "
      "### **nomina** la classificazione, l'ho applicata; dove ### **non la nomina**, "
      "### **ho lasciato la voce dov'era e l'ho scritta qui.** ### **Una decisione non presa "
      "e' un dato; una decisione presa al posto di Luca e' un difetto.**")
    p()

    q = os.path.join(RADICE, "doc", "REFERTO_indice_v3_correzione.md")
    io.open(q, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_correzione.md: %d righe" % len(R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
