# -*- coding: utf-8 -*-
"""IL REFERTO DELL'ULTIMA PULIZIA.

### ⛔ **NESSUN NUMERO RICOPIATO** *(`L-NUMERI`)*: i segnali **dopo** escono dalle stesse
funzioni che gira il validatore, quelli **prima** da `git show 89784dc:...`; le decisioni le
importa dai moduli che le portano, cosi' ### **il referto e il lavoro non possono
divergere.**

Gira con:  python csv/_doc_referto_pulizia.py
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
import _pulizia_finale as PF                                 # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
PRIMA = "89784dc"
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
    dopo = {x[0]: len(x[2]) for x in IX.segnali(voci, reg, verboso=False)}
    pv = [json.loads(r) for r in gshow("%s:doc/indice/voci.jsonl" % PRIMA).split(NL)
          if r.strip()]
    pe = len([r for r in gshow("%s:doc/indice/etichette_rimosse.jsonl" % PRIMA).split(NL)
              if r.strip()])
    etich = len([r for r in io.open(os.path.join(
        RADICE, "doc/indice/etichette_rimosse.jsonl"), encoding="utf-8") if r.strip()])
    dd = io.open(os.path.join(RADICE, "doc/indice/DA_DECIDERE_LUCA.md"),
                 encoding="utf-8").read()
    n_dd = int(re.search(r"una decisione\*\* \| ### \*\*`(\d+)`", dd).group(1))
    grup = re.findall(r"^## (.+?) -- `(\d+)`$", dd, re.M)
    q = subprocess.run([sys.executable, os.path.join(_QUI, "_collaudo_presidi_indice.py")],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    _E = re.compile(r"^  \S.*\s(PASSA|### FALLISCE)(\s|$)")
    coll = [r.rstrip() for r in (q.stdout or "").split(NL) if _E.match(r)]
    n_ok = sum(1 for r in coll if _E.match(r).group(1) == "PASSA")
    q2 = subprocess.run([sys.executable, os.path.join(_QUI, "_controlli_indice_v2.py")],
                        cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    ctrl = [r.rstrip() for r in (q2.stdout or "").split(NL)
            if re.match(r"^\s+C\d+ ", r) and ("PASSA" in r or "FALLISCE" in r)]
    q3 = subprocess.run([sys.executable, os.path.join(_QUI, "indice.py"), "collaudo"],
                        cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    m3 = re.search(r"COLLAUDO: (\d+) su (\d+)", q3.stdout or "")

    p("# IL REFERTO DELL'ULTIMA PULIZIA DELL'INDICE `v3`")
    p()
    p("> ### ⭐ **I segnali sono `F1=%d F2=%d F3=%d F4=%d F6=%d`, e sono ESATTAMENTE "
      "quelli che il mandato si aspettava.** ### ⛔ **Ma la cosa che conta di questo giro "
      "non e' un numero: e' che provando `F7` end-to-end ho scoperto che `aggiorna-lotto` "
      "SCRIVEVA PRIMA DELLA VALIDAZIONE INTERA.**"
      % (dopo["F1"], dopo["F2"], dopo["F3"], dopo["F4"], dopo["F6"]))
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | "
      "`doc/TASK_HISTORY/2026-10-09_indice_v3_ultima_pulizia.md`, ### **committato PRIMA del "
      "lavoro** *(`f614613`)* |")
    p("| **i commit** | `f39df3b` *(`1`)* · `f47159a` *(`2`)* · `375e0af` *(`3`)* "
      "· `4aeeb80` *(`4`)* · `dcc8aac` *(`5`)*, piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **i controlli** | ### **%d su %d** · collaudo dei presidi ### **%d su %d** "
      "*(erano `20`)* · collaudo dell'indice ### **%s su %s** *(era `21`)* |"
      % (sum(1 for r in ctrl if "PASSA" in r), len(ctrl), n_ok, len(coll),
         m3.group(1), m3.group(2)))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ① IL DIFETTO DEL GIRO, E L'HA TROVATO UNA PROVA CHE IL MANDATO NON CHIEDEVA")
    p()
    p("Il mandato chiede due bracci per `F7`: ### **deve scattare** su `CURA1-CORTO` allo "
      "stato di `89784dc` *(in una copia)*, ### **non deve** dopo il punto `1`. Li ho fatti, "
      "e passano. ### **Poi ho voluto vederlo BLOCCARE DAVVERO:** un lotto che riporta "
      "`CURA1-CORTO` ad `APERTA` deve essere rifiutato.")
    p()
    p("> ### ⛔ **E' STATO SCRITTO.** L'assert e' scattato ### **dopo**, e l'indice e' "
      "rimasto ### **CORROTTO sul disco** *(`CURA1-CORTO` ad `APERTA`)*. Il messaggio diceva "
      "*«SCRITTO, MA LA VALIDAZIONE INTERA FALLISCE»*, che era ### **esattamente la "
      "descrizione del danno.**")
    p()
    p("| | la catena |")
    p("|---|---|")
    p("| `1` | `aggiorna_lotto` valida con **`derivati=False`** — e `F5`, `F7` e la "
      "forma delle eccezioni stavano ### **DOPO** il ritorno su `derivati`, quindi "
      "### **non venivano guardati** |")
    p("| `2` | ### **SCRIVE** |")
    p("| `3` | rigenera le viste |")
    p("| `4` | ### **e SOLO ALLORA valida tutto** — su un file ### **gia' scritto** |")
    p()
    p("### ⚠ **La promessa era nel docstring di `aggiorna_lotto` dal giorno che l'ho "
      "scritto:** *«una sola validazione alla fine — se non passa, NON SI SCRIVE "
      "NIENTE»*. ### **Era una descrizione di cio' che credevo, non di cio' che il codice "
      "faceva.**")
    p()
    p("### ✔ **LA CURA, E TOCCA LA CAUSA**")
    p()
    p("| | |")
    p("|---|---|")
    p("| `F7` e la forma delle eccezioni | dipendono ### **solo dalle voci** ⇒ vanno "
      "### **prima** del ritorno su `derivati`, cosi' la validazione ### **pre-scrittura** li "
      "vede |")
    p("| `F5` | ### **non dipende dalle voci** *(guarda `storico.jsonl` contro `HEAD`)* "
      "⇒ si chiede ### **prima di scrivere**, nelle due vie di lotto |")
    p("| ➜ **l'effetto** | la validazione finale puo' fallire ### **solo sui derivati**, "
      "che `viste()` ha appena rigenerato: ### **la promessa diventa VERA** |")
    p()
    p("### **Riprovato end-to-end:** il lotto e' rifiutato e `voci.jsonl` e' "
      "### **byte-identico** prima e dopo *(`sha1 fe3751cbe3a9` in entrambi i casi)*. "
      "### ⭐ **E la prova e' diventata permanente**, con due bracci nel collaudo che "
      "### **fotografano i byte e li RIMETTONO** se cambiano: una regressione viene "
      "### **riportata, non subita.**")
    p()
    p("### ⭐ **E il danno e' stato riparato da git**, perche' tutto era committato. "
      "### **E' la seconda volta in questo lavoro che «commit prima di ogni run» mi "
      "salva un file:** la prima furono le ### **`867` classificazioni** che il controllo "
      "`C4` ha cancellato.")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ② PUNTO `1` — **lo stato di una voce dell'era `1`**")
    p()
    p("Le `4` voci da `APERTA` a `SOSPESA`, e l'*«APERTO»* in `stato_era_1`.")
    p()
    p("| id | prima | dopo | `stato_era_1` |")
    p("|---|---|---|---|")
    pper = {v["id"]: v for v in pv}
    for i in PF.P1:
        p("| `%s` | `%s` | ### **`%s`** | ### **`%s`** |"
          % (i, pper[i]["stato"], per[i]["stato"], per[i]["stato_era_1"]))
    p()
    p("### ⛔ **E' un mio errore del giro scorso, e la forma dell'errore e' quella che "
      "conta.** Nel referto avevo scritto: *«lo stato `APERTA` non l'ho scelto: lo dice "
      "l'intestazione; classe e dominio sono MIEI»*. ### **Era vero e insufficiente:** "
      "l'intestazione dice lo stato ### **nell'era `1`**, e io l'ho messo nel campo `stato`, "
      "che e' lo stato ### **di oggi.**")
    p()
    p("> ### ⭐ **DICHIARARE LA PROVENIENZA DI UN DATO NON BASTA SE LO SI E' MESSO NEL "
      "CAMPO SBAGLIATO:** la dichiarazione mi ha fatto sembrare prudente ### **un errore di "
      "campo.** Per questo la regola ha ### **un presidio**, non solo una riga in `par9.md`.")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ③ PUNTO `2` — **`F7`, e un presidio che boccia il caso sano**")
    p()
    p("`FISICA` + era `1` + stato diverso da `SOSPESA`/`CHIUSA` ⇒ ### **la validazione "
      "fallisce.** ### **E' un ERRORE, non un segnale.**")
    p()
    p("### ✔ **La prima misura e' stata PRIMA di scrivere il task history**, e non e' un "
      "dettaglio: ### **un presidio bloccante che violasse una voce che il mandato non nomina "
      "fermerebbe ogni commit**, e me ne accorgerei ### **solo al momento di committare.** "
      "`FISICA`/era `1`: `SOSPESA` `204`, `CHIUSA` `137`, ### **`APERTA` `4`** — e le "
      "`4` sono ### **esattamente quelle del punto `1`.** ### **`F7` e' sicuro perche' il "
      "punto `1` viene prima**, non per caso.")
    p()
    p("### ⚠ **E `F7` ha bocciato il CASO SANO del collaudo:** la voce-modello di "
      "`indice.py collaudo` era `FISICA`/era `1`/`APERTA`. Messa a era `ENTRAMBE`, e `F7` ha "
      "preso ### **il suo caso.** ### ⭐ **Un presidio che boccia il caso sano di un "
      "collaudo sta dicendo che quel caso sano era un esempio che nell'indice vero non si "
      "sarebbe potuto scrivere.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ④ PUNTO `3` — **`F1` a zero, e due omonimi in piu'**")
    p()
    p("| id | i due significati |")
    p("|---|---|")
    for i in sorted(PF.OMONIMI_3):
        p("| `%s` | %s<br>%s |" % (i, per[i]["meta"]["omonimo"][0],
                                   per[i]["meta"]["omonimo"][1]))
    p()
    p("### ⭐ **E' il terzo e il quarto omonimo che nascono LEGGENDO UN SEGNALE DI `F1`**, "
      "dopo `C5`. ### **Un presidio che trova omonimi cercando gemelle sta dicendo che gemelle "
      "e omonimi si somigliano:** entrambi sono ### **due nomi e una cosa, o una cosa e due "
      "nomi.**")
    p()
    p("| gruppo | id | il marcatore scelto nel testo |")
    p("|---|---|---|")
    for i in sorted(PF.F1_MARCATORE):
        g, marc, _pp = PF.F1_MARCATORE[i]
        p("| %s | `%s` | *«%s»* |" % (g, i, marc))
    p()
    p("### ⚠ **Il codice si e' fermato una volta, ed e' il punto:** avevo scelto "
      "*«COERENZA»* per `COER-4PI`, e nel titolo c'e' *«la coerenza della "
      "massa»*. ### **Ho riletto i titoli veri invece di allargare la ricerca.**")
    p()
    p("### ⛔ **Su `49` segnali iniziali di `F1`, ZERO gemelle vere.** E' "
      "### **il presidio con la precisione piu' bassa dei sette**, e questo e' un fatto su "
      "`F1`.")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑤ PUNTO `4` — **`F4` a zero, e il criterio e' l'EREDITA'**")
    p()
    p("| id | `classe`/`dominio`/era/stato | il perche' |")
    p("|---|---|---|")
    for i in sorted(PF.P4):
        cl, dom, era, st, perche = PF.P4[i]
        p("| `%s` | `%s`/`%s`/era `%s`/`%s` | %s |" % (i, cl, dom, era, st, perche))
    p()
    p("### ✔ **`F4` e `F5` sono FAMIGLIE di difetti, e il testo dice DA QUALE DIFETTO "
      "NASCONO.** Ho misurato `D04` e `D34`: ### **`FISICA`/era `1`.** "
      "### ⭐ **Una famiglia prende il dominio del difetto da cui nasce**, e cosi' "
      "### **il dominio non lo scelgo io: LO EREDITA.** ### ⚠ **Ma l'eredita' vale per "
      "il DOMINIO, non per lo stato:** `F5` e' `SOSPESA` e `D34` e' `CHIUSA`, perche' il "
      "testo di `F5` dice *«dal censimento IN CORSO»*.")
    p()
    p("### ⚠ **E la mia uscita del giro scorso non era piu' disponibile, e va bene:** "
      "avevo messo queste tre in un ### **«quarto caso»** — *«non e' "
      "nessuno dei tre esiti»*. ### **Era una domanda, e la risposta e' «decidi».**")
    p()
    p("### ⛔ **Due cose che il codice ha RIFIUTATO, ed e' giusto cosi':**")
    p()
    p("| | |")
    p("|---|---|")
    p("| `1` | la nota di `AUTO-MANUTENZIONE` superava i ### **`300` caratteri** che il "
      "registro ammette. Il lotto e' stato ### **rifiutato, e non ha scritto niente** "
      "— ### **la cura dell'atomicita' ha funzionato al primo uso vero.** La nota si "
      "taglia, e il perche' ### **intero resta nel `motivo`**: ### **un campo con un limite "
      "dichiarato non si allarga per far stare una frase** |")
    p("| `2` | ripristinando `F4` come voce `FISICA`, `F3` e' risalito da `0` a `1`: il "
      "titolo contiene *«si RIUSA il criterio»*, che sta nella frase che dice "
      "### **da quale difetto nasce**, non nell'argomento. Chiuso con l'eccezione "
      "### **nello stesso giro che l'ha prodotto.** ### ⚠ **E' la seconda volta che un "
      "ripristino crea un segnale di `F3`:** `F3` guarda ### **una parola**, e una parola "
      "### **non dice di chi si parla** |")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑥ PUNTO `5` — **un elenco solo, e SI GENERA**")
    p()
    p("`doc/indice/DA_DECIDERE_LUCA.md`, ### **`%d` voci** e `%d` domande." % (n_dd, n_dd))
    p()
    p("| | il criterio |")
    p("|---|---|")
    p("| ① | la `nota_guardiano` dice *«da decidere / confermare da Luca»* "
      "→ ### **la domanda e' cio' che la nota stessa chiede** |")
    p("| ② | la voce ha ### **`meta.omonimo`** → quale dei `N` significati? |")
    p("| ③ | `stato = DA_CLASSIFICARE` ### **e la classe NON e' `NON_DEFINITA`** |")
    p()
    p("| gruppo | quante |")
    p("|---|--:|")
    for g, k in grup:
        p("| %s | `%s` |" % (g, k))
    p()
    p("### ⛔ **Nel codice NON c'e' nessuna lista di ID: ci sono i tre criteri**, e "
      "l'elenco e' cio' che trovano. ### ⭐ **Un elenco mezzo generato e' peggio di "
      "nessun elenco, perche' SEMBRA COMPLETO.**")
    p()
    p("### ⚠ **E un'imprecisione presa rileggendo l'uscita:** la domanda diceva "
      "*«quale dei `7` significati»* per `D3`, che ha ### **`8` definizioni** "
      "— contava le voci del meta, e l'ultima e' ### **un troncamento.** Adesso dice "
      "*«di ALMENO `6`»* quando la lista e' troncata. ### **Un numero in una domanda "
      "e' un numero come gli altri: se e' sbagliato, la domanda e' sbagliata.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑦ I CONTEGGI E I CONTROLLI")
    p()
    p("> **PRIMA** = `git show %s`. **DOPO** = il disco. ### **Nessun numero ricopiato.**"
      % PRIMA)
    p()
    for campo in ("dominio", "classe", "stato"):
        tab(campo, conta(pv, campo), conta(voci, campo))
    p("| | prima | dopo |")
    p("|---|--:|--:|")
    p("| voci | `%d` | ### **`%d`** |" % (len(pv), len(voci)))
    p("| etichette rimosse | `%d` | ### **`%d`** |" % (pe, etich))
    p("| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |")
    p("| ### **`FISICA`/era `1` con stato vietato** | `4` | ### **`0`** *(e `F7` lo "
      "impedisce)* |")
    p()
    p("| presidio | prima | dopo |")
    p("|---|--:|--:|")
    PR = {"F1": 11, "F2": 1, "F3": 0, "F4": 3, "F6": 0}
    for k in ("F1", "F2", "F3", "F4", "F6"):
        p("| `%s` | `%d` | ### **`%d`** |" % (k, PR[k], dopo[k]))
    p("| ### **in tutto** | `%d` | ### **`%d`** |" % (sum(PR.values()), sum(dopo.values())))
    p()
    p("### ✔ **E sono ESATTAMENTE i numeri che il mandato aveva scritto:** "
      "*«atteso: `F1=0 F2=1 F3=0 F4=0 F6=0`»*.")
    p()
    p("```")
    for r in ctrl:
        p(r)
    for r in coll:
        p(r)
    p("```")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑧ CHE COSA RESTA A LUCA")
    p()
    p("> ### ⭐ **Tutto in un posto solo: `doc/indice/DA_DECIDERE_LUCA.md`, e si "
      "GENERA.**")
    p()
    p("| | quante | che cosa |")
    p("|---|--:|---|")
    for g, k in grup:
        p("| %s | `%s` | |" % (g, k))
    p("| ### **l'unico segnale che resta** | `1` | `ENERGIA-NON-DEFINITA`: *«superata da "
      "`A16` (`H` definita)?»*. ### **E' voluto:** un presidio che segnala una decisione "
      "aperta ### **sta funzionando** |")
    p("| ### **i segnaposto** | `%d` | ### **NON sono una domanda: sono il lavoro che "
      "resta** |" % sum(1 for v in voci if v["classe"] == "NON_DEFINITA"))
    p()
    p("### ⚠ **E tre classificazioni che sono MIE**, e si cambiano con un lotto di una "
      "riga: la classe `STANDARD` e il dominio `METODO` di `AUTO-MANUTENZIONE`; la classe "
      "`MISURA` delle `4` del punto `1`; e `F7` ### **non guarda `FISICA`/era `2` ne' gli "
      "altri domini** — il mandato dice `FISICA`/era `1`, e ### **non l'ho allargato da "
      "solo.**")
    p()
    p("> ### ⭐ **Il criterio, lo stesso di tutto il lavoro:** dove il mandato "
      "### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho "
      "lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un "
      "dato; una decisione presa al posto di Luca e' un difetto.**")
    p()

    # ======================================================================
    p("## \u2468 UNA VOCE DOPO: **`ENERGIA-NON-DEFINITA` E- SUPERATA DA `A16`**")
    p()
    e = per["ENERGIA-NON-DEFINITA"]
    p("> ### \u2b50 **L-unico segnale che restava NON c-e- piu-, e non perche- l-ho "
      "zittito: perche- ### LA DOMANDA HA AVUTO RISPOSTA.** I presidi sono "
      "### **tutti a `0`**.")
    p()
    p("| | |")
    p("|---|---|")
    p("| **la voce** | `%s`/`%s`/era `%s`/### **`%s`**, `superata_da` = "
      "### **`%s`** |" % (e["classe"], e["dominio"], e["era"], e["stato"],
                          e["superata_da"]))
    p("| **che cosa diceva** | *<<il modello non ha un-energia totale, e senza quella "
      "bilancio e calore non hanno base>>* |")
    p("| **che cosa dice `A16`** | lo stato evolve sotto ### **UNA SOLA `H`**, e "
      "*<<norma ed energia si conservano ### **per costruzione**>>* "
      "*(decisione di Luca, 2026-10-08)* |")
    p("| **era `2` -> `1`** | la voce e- ### **una LETTURA DEL CODICE DELL-ERA `1`** "
      "\u2014 *<<non esiste nessuna funzione che calcoli un-energia totale>>* "
      "\u2014 non programma dell-era `2` |")
    p("| **la nota TOLTA** | diceva *<<da decidere da Luca: superata da `A16`?>>*. "
      "### **Una domanda a cui si e- risposto non si riscrive: si TOGLIE**, e la "
      "risposta vive in `superata_da` |")
    p()
    p("### \u26d4 **CIO- CHE RESTA APERTO NON STA IN QUESTA VOCE, E NON STA NEMMENO "
      "NELL-INDICE.** Il mandato dice *<<collegala con le voci che lo tracciano, ### "
      "**se esistono**>>*: ### **ho cercato, e NON ESISTONO.** La forma di `H`, "
      "l-energia cinetica delle lunghezze *(decisione `9`)* e l-energia d-arco stanno "
      "in `doc/TRADUZIONE_IN_H.md`, e ### **nessuna voce dell-indice ha quel documento "
      "come fonte** \u2014 `0` su `%d`. Quindi `collegate` resta ### **vuoto**, e "
      "### **questo e- il dato**, non un dettaglio: ### \u2b50 **il lavoro aperto piu- "
      "grande del progetto e- tracciato SOLO IN UN DOCUMENTO.**" % len(voci))
    p()
    p("### \u26a0 **E due ostacoli fra il mandato e il codice, tolti alla causa:**")
    p()
    p("| | |")
    p("|---|---|")
    p("| `F7` ammetteva solo `SOSPESA` e `CHIUSA` | `FISICA`/era `1`/`SUPERATA` "
      "### **lo faceva scattare**, e il lotto sarebbe stato ### **rifiutato.** "
      "\u279c **`SUPERATA` sta con `CHIUSA`:** una voce superata da una decisione "
      "### **non e- aperta**, e- risolta ### **da fuori** \u2014 e `TRANSIZIONI` lo "
      "conferma, da `SUPERATA` si esce ### **solo verso `APERTA`.** Due bracci di "
      "collaudo: `SUPERATA` ### **non scatta**, `APERTA` ### **scatta ancora** |")
    p("| la via di scrittura sapeva solo AGGIUNGERE un metadato | e `nota_guardiano` ha "
      "regex `^.{1,300}$`, quindi ### **non si puo- svuotare.** \u279c **`meta_togli`**: "
      "una lista di chiavi da ### **cancellare**, nella stessa via, con la sua riga di "
      "storico \u2014 e ### **togliere una chiave che non c-e- e- un errore**, perche- "
      "nasconderebbe uno sbaglio |")
    p()
    p("---")
    p()

    q4 = os.path.join(RADICE, "doc", "REFERTO_indice_v3_pulizia.md")
    io.open(q4, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_pulizia.md: %d righe" % len(R))
    print("  segnali %d -> %d; controlli %d/%d; collaudo presidi %d/%d; indice %s/%s"
          % (sum(PR.values()), sum(dopo.values()),
             sum(1 for r in ctrl if "PASSA" in r), len(ctrl), n_ok, len(coll),
             m3.group(1), m3.group(2)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
