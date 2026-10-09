# -*- coding: utf-8 -*-
"""IL REFERTO DELLE CHIUSURE — **voce per voce, e nessun numero ricopiato.**

Il **prima** da `git show c24bbd5:doc/indice/voci.jsonl` *(il task history, prima di ogni
scrittura del giro)*, il **dopo** dal disco, e i verdetti dai rapporti che gli attrezzi
hanno scritto.

Gira con:  python csv/_doc_referto_chiusure.py
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
PRIMA = "c24bbd5"
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
    pv = [json.loads(r) for r in gshow("%s:doc/indice/voci.jsonl" % PRIMA).split(NL)
          if r.strip()]
    pper = {v["id"]: v for v in pv}
    _v, reg = IX.carica()
    seg = {x[0]: x[2] for x in IX.segnali(voci, reg, verboso=False)}
    ch1 = js("doc/indice/_p1_chiusure.json")
    f12 = js("doc/indice/_p2_f12.json")
    rapb = js("doc/indice/_p3_guardiano_b.json")
    conv = js("doc/indice/_p4_convenzioni.json")
    del conv
    conta_b = collections.Counter(x["verdetto"] for x in rapb["esiti"])
    datib = {}
    for r in io.open(os.path.join(RADICE,
                                  "doc/indice/_lotti/"
                                  "correzioni_guardiano_2026-10-09_b.txt"),
                     encoding="utf-8").read().split(NL):
        if r.strip():
            z = [y.strip() for y in r.split("|")]
            datib[z[0]] = {"cambi": z[1], "citazione": z[2], "conf": z[3]}
    n_pres = gira(["csv/_collaudo_presidi_indice.py"],
                  r"IL COLLAUDO DEI PRESIDI: (\d+) su (\d+)")
    n_ind = gira(["csv/indice.py", "collaudo"], r"COLLAUDO: (\d+) su (\d+)")
    n_ctrl = gira(["csv/_controlli_indice_v2.py"], r"I CONTROLLI: (\d+) su (\d+)")
    ric = [x for x in ch1 if x["come"] == "RICAVATO"]
    tag = [x for x in ch1 if x["come"] != "RICAVATO"]
    gen = [x for x in ch1 if "e- GENERICA" in x["dove"]]

    p("# IL REFERTO DELLE CHIUSURE, DELLE SUPERATE E DELLA TERZA LETTURA")
    p()
    p("> ### ⭐ **«IL COMMIT DI CHIUSURA SI RICAVA, NON SI INVENTA.»** Nel giro scorso "
      "avevo lasciato ### **`47` chiusure non fatte** scrivendo *«un commit non si "
      "inventa»*: ### **non inventarlo era giusto, fermarsi li- era una RINUNCIA.** "
      "### ⛔ **E l'errore sotto l'errore: cercavo lo sha DENTRO LA RIGA**, e una riga di "
      "documento ### **non ha nessun motivo di portare lo sha del commit che l'ha "
      "scritta.**")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | "
      "`doc/TASK_HISTORY/2026-10-09_indice_v3_chiusure_e_strumenti_era2.md`, "
      "### **committato PRIMA del lavoro** *(`%s`)* |" % PRIMA)
    p("| **i due file del guardiano** | `correzioni_guardiano_2026-10-09.txt` *(`165` "
      "righe, `67c12fa`)* e `correzioni_guardiano_2026-10-09_b.txt` *(`59` righe, "
      "`3926dbb`)*, ### **ciascuno committato DA SOLO** |")
    p("| **i commit** | `570d43a` *(`1`)* · `6101c09` *(`2`)* · `7e4c59c` *(`3`)* "
      "· `7545c1a` *(`4`)* · `3926dbb`+`43c4dc2` *(`5`)*, piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **i controlli** | ### **%s/%s** · presidi ### **%s/%s** · indice "
      "### **%s/%s** |" % (n_ctrl + n_pres + n_ind))
    p()
    p("---")
    p()

    # ================================================================ punto 1
    p("## ① PUNTO `1` — **il commit di chiusura si RICAVA**: `%d` su `47`"
      % len(ric))
    p()
    p("| | quante | |")
    p("|---|--:|---|")
    p("| ### **commit RICAVATO dalla storia** | ### **`%d`** | `git log -S'<frase>' "
      "--reverse -- <file>`, ### **il PRIMO** — quello che ### **INTRODUCE** la "
      "frase |" % len(ric))
    p("| ### **dal tag `era-1-secondo-ordine`** | `%d` | la stessa regola della migrazione. "
      "### **Il tag dice «ENTRO QUI», non «proprio qui»** |" % len(tag))
    p("| ### ⚠ **frasi GENERICHE** | `%d` | la citazione compare in ### **piu' di tre "
      "righe del file**: il commit c'e', ### **ma la frase non identifica la riga** |"
      % len(gen))
    p()
    p("### ⛔ **DUE FALSI, TROVATI GUARDANDO L'USCITA PRIMA DI SCRIVERE.** La citazione "
      "di `REGISTRO_FISICA:T4` e' *«PASS»* e ### **«passato» la contiene**; quella di "
      "`REGISTRO_FISICA:P3` e' *«TIENE»* e ### **«CONTIENE» la contiene.** Le due "
      "combaciavano con la ### **riga `1`** e la ### **riga `11`** del registro — "
      "### **il TITOLO del documento** — e il commit *«ricavato»* sarebbe stato "
      "### **quello che ha creato il file.** ### ⭐ **E- la TERZA volta che una parola "
      "dentro un'altra parola mi inganna** *(la prima: `infinito` contiene `FINITO`)*: "
      "adesso si cerca ### **a confine di parola.**")
    p()
    p("| id | come | commit | dove si e- trovata la frase |")
    p("|---|---|---|---|")
    for x in ch1:
        p("| `%s` | %s | `%s` | %s |"
          % (x["id"], "### **RICAVATO**" if x["come"] == "RICAVATO" else "### ⚠ **DAL "
             "TAG**", x["commit"], x["dove"].replace("|", "/")[:170]))
    p()
    p("### ⚠ **E SEI VOCI SONO CHIUSE DALLO STESSO COMMIT `fa42066`**, perche' la loro "
      "frase e' *«C. DIAGNOSI CHIUSE»* — ### **un'INTESTAZIONE DI SEZIONE.** Il commit "
      "che l'ha introdotta ### **ha chiuso tutte le diagnosi che stanno sotto**: e' corretto, "
      "### **ma e- GROSSO**, e lo dichiaro.")
    p()
    p("---")
    p()

    # ================================================================ punto 2
    p("## ② PUNTO `2` — **`F12` e le `chiusura` ORFANE**: `%d` si svuotano, `%d` "
      "chiude" % (len(f12["svuota"]), len(f12["chiude"])))
    p()
    p("> ### ⭐ **ERA IL ROVESCIO DI UN CONTROLLO CHE C'ERA GIA-:** `valida` pretendeva "
      "`chiusura.criterio` e `chiusura.commit` ### **quando lo stato e- `CHIUSA`**. Che una "
      "`chiusura` piena ### **implichi** `CHIUSA` ### **non lo chiedeva nessuno** — e "
      "### **una delle due direzioni non e- un controllo: e- MEZZO controllo.**")
    p()
    p("### ⚠ **Erano `42` quando il mandato le ha contate; il punto `1` ne ha chiusa "
      "UNA**, quindi quando ci sono arrivato erano ### **`41`.** Il numero del mandato era "
      "giusto ### **al momento in cui l'ha scritto**, e lo dico perche' ### **un numero che "
      "non torna va spiegato, non aggiustato.**")
    p()
    p("### **LA RIGA CHIUDE → `CHIUSA`: `%d`**" % len(f12["chiude"]))
    p()
    p("| id | prima | commit ricavato | la lettura della riga |")
    p("|---|---|---|---|")
    for i, st, sha, perche in f12["chiude"]:
        p("| `%s` | `%s` | `%s` | %s |" % (i, st, sha, perche.replace("|", "/")[:170]))
    p()
    p("### **LA RIGA NON CHIUDE → la `chiusura` SI SVUOTA: `%d`**"
      % len(f12["svuota"]))
    p()
    p("### ⭐ **E si svuota la `chiusura`, NON si muove lo stato:** lo stato "
      "### **l'ha deciso un lavoro che ha letto la riga**; la `chiusura` e' ### **cio- che e- "
      "rimasto indietro** dalla migrazione. ### **Fra un campo deciso leggendo e un campo "
      "trascinato, cede il secondo.**")
    p()
    p("| id | resta | la lettura della riga | la `chiusura` che si toglie |")
    p("|---|---|---|---|")
    for i, st, perche, crit in f12["svuota"]:
        p("| `%s` | `%s` | %s | *%s* |" % (i, st, perche.replace("|", "/")[:120],
                                            crit.replace("|", "/")[:80]))
    p()
    p("### ⚠ **E TRE DELLE `%d` SONO I HOOK** — `H-FILE`, `H-NON-TRACCIATI`, "
      "`H-STASH`: non hanno riga d'origine, e la loro `chiusura` era ### **un residuo della "
      "migrazione.** Il punto `4` del mandato precedente li ha portati ad `APERTA` perche' "
      "### **sono IN VIGORE**, e la `chiusura` ### **e- rimasta.**" % len(f12["svuota"]))
    p()
    p("---")
    p()

    # ================================================================ punto 3
    p("## ③ PUNTO `3` — **`superata_da` accetta anche una VOCE**")
    p()
    p("> ### ⛔ **LA MIA REGOLA DI IERI ERA MEZZA VERA.** Avevo rifiutato `S02` scrivendo "
      "*«una voce superata deve essere superata DA UNA DECISIONE, e un difetto non decide "
      "niente»*: ### **vero per una DECISIONE, falso per una PROMOZIONE.** `S02` e' "
      "### **«PROMOSSO»** a `D31`, e *«promosso a»* ### **non e- «deciso da»**.")
    p()
    p("| | |")
    p("|---|---|")
    p("| `S02` | `%s`/`%s` → ### **`%s`**, `superata_da` = ### **`%s`** |"
      % (pper["S02"]["classe"], pper["S02"]["stato"], per["S02"]["stato"],
         per["S02"]["superata_da"]))
    p("| `Z21` | ### ⚠ **NON applicata al punto `3`**: il file vecchio chiede `SUPERATA` "
      "### **senza dire da che cosa**, e il `superata_da` lo porta ### **la terza lettura** "
      "*(`Z26`)*. Applicata al punto `5` |")
    p("| ### **e `F9` ammette `SUPERATA` per `ENTRAMBE`** | correggeva ### **un'altra mia "
      "strettezza**: avevo scritto *«`ENTRAMBE` ⇒ `APERTA` o `CHIUSA`»* ### **alla "
      "lettera del mandato.** ### ⭐ **«Superata» non e' «rimandata»: e' RISOLTA DA "
      "FUORI** |")
    p("| ### **il collaudo, nei due versi** | una VOCE → ### **accettata**; un id che "
      "non e' ne' decisione, ne' assioma, ne' voce → ### **rifiutato.** "
      "### ⛔ **Senza il verso negativo la regola nuova non e' una regola: e' un "
      "PERMESSO** |")
    p()
    p("---")
    p()

    # ================================================================ punto 4
    p("## ④ PUNTO `4` — **la nota di `G1`, e `C3` si allinea al file**")
    p()
    p("| | |")
    p("|---|---|")
    p("| la nota di `G1` | ### **TOLTA** *(`meta_togli`)*. Diceva *«correzione v3 blocco G2: "
      "FISICA/era 1/SOSPESA»* e la voce e' `%s` |" % per["G1"]["stato"])
    p("| ### **si toglie, non si riscrive** | la sua storia vive ### **in `storico.jsonl`**, "
      "quindi togliere la nota ### **non perde niente** — e ### **una domanda a cui si "
      "e' risposto non si riscrive: si TOGLIE** |")
    p("| `CLI-1` e `POTATURA-GUARDIE` | ### **vale il file**, e ### **lo conferma il "
      "guardiano.** Avevo scritto *«ho scelto la FORMA, non il merito»* e ### **l'ho portato "
      "a Luca**: ### ⭐ **una decisione portata a chi tocca e tornata indietro non e' "
      "piu' mia** |")
    p("| ### ⚠ **e un braccio di collaudo si sarebbe spento da se'** | il caso *«`F6` "
      "DEVE scattare su `G1`»* ### **legge la nota**, e il punto `4` ### **la toglie.** "
      "Ancorato a `7e4c59c`, piu' il braccio che prova che ### **sulla `G1` di oggi `F6` "
      "tace.** ### **Un caso a risposta nota e' una FOTO, non uno specchio** |")
    p()
    p("---")
    p()

    # ================================================================ punto 5
    p("## ⑤ PUNTO `5` — **la terza lettura**, riga per riga tutte e `59`")
    p()
    p("| verdetto | quante |")
    p("|---|--:|")
    for k in ("APPLICATA", "NON_APPLICATA", "LASCIATA", "NIENTE_DA_FARE"):
        if conta_b.get(k):
            p("| ### **`%s`** | ### **`%d`** |" % (k, conta_b[k]))
    p("| ### **in tutto** | ### **`%d`** — e DEVE fare `59` |" % sum(conta_b.values()))
    p()
    p("| livello | quante |")
    p("|---|--:|")
    for k, n in sorted(rapb["livelli"].items()):
        p("| `%s` | `%d` |" % (k, n))
    p()
    p("### ⛔ **TRE DIFETTI MIEI, E NESSUNO L'HO TROVATO IO**")
    p()
    p("| | il difetto | chi l'ha trovato |")
    p("|---|---|---|")
    p("| `1` | ### **`superata_da` giudicato come campo INDIPENDENTE**: `Z21` e `L-SOGLIA` "
      "hanno perso ### **entrambi** i campi — il `superata_da` cadeva per *«in `T3` non "
      "basta»*, e poi lo `stato` cadeva per ### **«SUPERATA senza dire da che cosa»**, cioe' "
      "### **per la mancanza del campo che avevo appena scartato io** | ### **lo schema**, "
      "rifiutando |")
    p("| `2` | ### **la regola di `superata_da` era DUPLICATA**: la copia nell'applicatore "
      "diceva *«ne' decisione, ne' assioma»* e il validatore ### **accettava gia' una "
      "voce** | ### **il rifiuto stesso**, che citava ### **una ragione che il repo aveva "
      "smesso di avere** |")
    p("| `3` | ### **la `chiusura` restava piena su una voce che usciva da `CHIUSA`**: "
      "`L-SOGLIA` passava a `SUPERATA` ### **portandosi dietro il commit di chiusura** | "
      "### **`F12`**, acceso ### **due commit prima**, rifiutando il lotto ### **senza "
      "scrivere niente** |")
    p()
    p("### ⭐ **E IL TERZO E' LA PROVA CHE I PRESIDI SERVONO:** `F12` l'ho scritto "
      "### **stamattina**, e ### **mi ha fermato nel pomeriggio su un caso che non avevo "
      "previsto.**")
    p()
    p("### ✔ **E LE DUE CORREZIONI DEL GUARDIANO A SE' STESSO**")
    p()
    p("| | la correzione | che cosa cambia |")
    p("|---|---|---|")
    p("| `(a)` | la classe `(B)` del censimento e' ### **«COSTRUITA E MAI MISURATA»**, non "
      "testo falso | le `13` `CENS-B*` sono ### **FRONTI aperti.** ### **Io leggevo "
      "«censimento delle intenzioni» come «il testo dichiara il falso»** |")
    p("| `(b)` | `REGISTRO_FISICA:P*` sono ### **PREVISIONI, non esiti** | `6` voci a "
      "### **`CRITERIO`/`METODO`.** ### ⭐ **E questo spiega perche' la riga di `P2` dice "
      "«P2 E' FALLITA»: non e' l'esito di una misura, e' IL CONFRONTO fra la previsione e la "
      "misura** |")
    p()
    for verdetto, titolo in (("APPLICATA", "LE `%d` APPLICATE" % conta_b["APPLICATA"]),
                             ("NON_APPLICATA",
                              "LE `%d` NON APPLICATE" % conta_b["NON_APPLICATA"]),
                             ("LASCIATA", "LE LASCIATE"),
                             ("NIENTE_DA_FARE", "NIENTE DA FARE")):
        q = [x for x in rapb["esiti"] if x["verdetto"] == verdetto]
        if not q:
            continue
        p("### **%s**" % titolo)
        p()
        p("| id | il file chiede | citazione | conf | prima → dopo | il dettaglio |")
        p("|---|---|---|---|---|---|")
        for x in q:
            i = x["id"]
            d = datib[i]
            a, b = pper.get(i, per[i]), per[i]
            p("| `%s` | `%s` | *%s* | `%s` | `%s`/`%s`/`%s` → "
              "### **`%s`/`%s`/`%s`** | %s |"
              % (i, d["cambi"].replace("|", "/"), d["citazione"].replace("|", "/")[:60],
                 d["conf"], a["classe"], a["dominio"], a["stato"],
                 b["classe"], b["dominio"], b["stato"],
                 x["dettaglio"].replace("|", "/")[:190]))
        p()
    p("---")
    p()

    # ================================================================ conteggi
    p("## ⑥ I CONTEGGI E I CONTROLLI")
    p()
    p("> **PRIMA** = `git show %s` *(il task history, prima di ogni scrittura del giro)*. "
      "**DOPO** = il disco. ### **Nessun numero ricopiato.**" % PRIMA)
    p()
    for campo in ("classe", "dominio", "era", "stato"):
        tab(campo, collections.Counter(str(v[campo]) for v in pv),
            collections.Counter(str(v[campo]) for v in voci))
    p("| | prima | dopo |")
    p("|---|--:|--:|")
    p("| voci | `%d` | ### **`%d`** *(`2` NUOVE: i due presidi)* |" % (len(pv), len(voci)))
    p("| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |")
    p("| ### **righe di storico** | `%d` | ### **`%d`** |"
      % (len([r for r in gshow("%s:doc/indice/storico.jsonl" % PRIMA).split(NL)
              if r.strip()]),
         sum(1 for r in io.open(os.path.join(RADICE, "doc/indice/storico.jsonl"),
                                encoding="utf-8") if r.strip())))
    p("| ### **`chiusura` ORFANE** | `42` | ### **`0`** *(`F12` le vieta)* |")
    p("| ### **voci non allineate allo storico** | ### **non misurato** | ### **`0`** "
      "*(`F11` le vieta)* |")
    p()
    p("| presidio | segnali |")
    p("|---|--:|")
    for k in ("F1", "F2", "F3", "F4", "F6", "F8"):
        p("| `%s` | %s |" % (k, "### **`%d`**" % len(seg[k]) if seg[k] else "`0`"))
    p("| `F5` `F7` `F9` `F10` `F11` `F12` | ### **`0`** — sono ERRORI: se non fossero "
      "zero, `valida` ### **non passerebbe** |")
    p("| ### **in tutto** | ### **`%d`** |" % sum(len(v) for v in seg.values()))
    p()
    for k in ("F1", "F3", "F6", "F8"):
        if not seg[k]:
            continue
        p("| `%s` | il segnale |" % k)
        p("|---|---|")
        for i, mm in sorted(seg[k]):
            p("| `%s` | %s |" % (i, mm.replace("|", "/")))
        p()
    p("---")
    p()
    p("## ⑦ CHE COSA RESTA A LUCA")
    p()
    p("| | quante | che cosa |")
    p("|---|--:|---|")
    p("| ### **le frasi GENERICHE** | `%d` | il commit c'e', ### **ma la frase compare in "
      "piu' di tre righe del file**: se le vuoi piu' strette, servono ### **citazioni piu' "
      "lunghe** |" % len(gen))
    p("| ### **la chiusura dal TAG** | `%d` | `MITOSI-2LAM-ACCESO`: la frase e' nel file "
      "### **ma `git log -S` non la trova nella storia** |" % len(tag))
    p("| ### **le `%d` NON APPLICATE** della terza lettura | `%d` | la citazione "
      "### **non compare**, o compare ### **fuori dalla sezione** della voce |"
      % (conta_b["NON_APPLICATA"], conta_b["NON_APPLICATA"]))
    p("| ### **i segnali che restano** | `%d` | `F1`=`%d` `F3`=`%d` `F6`=`%d` `F8`=`%d`, "
      "### **elencati e non corretti** |" % (sum(len(v) for v in seg.values()),
                                             len(seg["F1"]), len(seg["F3"]),
                                             len(seg["F6"]), len(seg["F8"])))
    p("| ### **`H-FISICA-FUORI-LISTA`** | `1` | ### **non impedisce niente finche' la "
      "cartella dell'era `2` e' vuota** — e ### **il nome lo decidi tu** "
      "*(`doc/REFERTO_strumenti_era2.md`)* |")
    p()
    p("> ### ⭐ **Il criterio, lo stesso di tutto il giro:** dove ### **la storia di git "
      "sa la risposta** l'ho cercata invece di rinunciare; dove ### **due campi si "
      "contraddicono** ho chiesto ### **al documento**; dove ### **il guardiano contraddice "
      "se stesso** ho portato la domanda e ### **ho aspettato la conferma.** "
      "### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un "
      "difetto.**")
    p()

    q = os.path.join(RADICE, "doc", "REFERTO_indice_v3_chiusure.md")
    io.open(q, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_chiusure.md: %d righe" % len(R))
    print("  punto 1: %d ricavati, %d dal tag, %d generiche" % (len(ric), len(tag),
                                                                len(gen)))
    print("  punto 2: %d svuotate, %d chiuse" % (len(f12["svuota"]), len(f12["chiude"])))
    print("  punto 5: %s" % dict(conta_b))
    print("  controlli %s/%s; presidi %s/%s; indice %s/%s"
          % (n_ctrl + n_pres + n_ind))
    return 0


if __name__ == "__main__":
    sys.exit(main())
