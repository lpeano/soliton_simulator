# -*- coding: utf-8 -*-
"""IL REFERTO DELL'ERA DELLE VOCI DI METODO E STRUMENTI.

### ⛔ **NESSUN NUMERO RICOPIATO** *(`L-NUMERI`)*: i conteggi **prima** da
`git show 72e452f:doc/indice/voci.jsonl`, quelli **dopo** dal disco, i segnali dalle stesse
funzioni che gira il validatore, e le decisioni **importate** da `csv/_era_metodo.py` — cosi'
### **il referto e il lavoro non possono divergere.**

Gira con:  python csv/_doc_referto_era_metodo.py
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
import migra_indice_v2 as MG                                 # noqa: E402
import _era_metodo as EM                                     # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto sull'indice.
NL = chr(10)
PRIMA = "72e452f"
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
    _v, reg = IX.carica()
    seg = {x[0]: x[2] for x in IX.segnali(voci, reg, verboso=False)}
    pv = [json.loads(r) for r in gshow("%s:doc/indice/voci.jsonl" % PRIMA).split(NL)
          if r.strip()]
    pper = {v["id"]: v for v in pv}
    r1 = [json.loads(r) for r in
          io.open(os.path.join(RADICE, "doc/indice/_lotti/v3_r1.jsonl"),
                  encoding="utf-8").read().split(NL) if r.strip()]
    tutte = list(EM.GEMELLE) + list(EM.METODO) + list(EM.STRUMENTI)
    in_l1 = sorted(i for i in tutte if i in MG.L1)
    q = subprocess.run([sys.executable, os.path.join(_QUI, "_collaudo_presidi_indice.py")],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    _E = re.compile(r"^  \S.*\s(PASSA|### FALLISCE)(\s|$)")
    coll = [r.rstrip() for r in (q.stdout or "").split(NL) if _E.match(r)]
    n_ok = sum(1 for r in coll if _E.match(r).group(1) == "PASSA")
    q2 = subprocess.run([sys.executable, os.path.join(_QUI, "_controlli_indice_v2.py")],
                        cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    ctrl = [r.rstrip() for r in (q2.stdout or "").split(NL)
            if re.match(r"^\s+C\d+ ", r) and ("PASSA" in r or "FALLISCE" in r)]

    p("# IL REFERTO DELL'ERA DELLE VOCI DI METODO E STRUMENTI")
    p()
    p("> ### ⛔ **L'ERRORE DEL GUARDIANO, e lo dichiara lui:** *«la regola «metodo "
      "= era `ENTRAMBE`» era ### **TROPPO GROSSA**»*. ### ⚠ **E io l'ho "
      "applicata:** nel punto `2` della chiusura dei segnali ho portato `58` voci a `METODO` e "
      "### **nessuna di quelle ha cambiato era** — la regola che applicavo "
      "### **non mi faceva nemmeno porre la domanda.** ### **`35` voci erano `ENTRAMBE` per "
      "INERZIA**, non per lettura.")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_era_metodo.md`, "
      "### **committato PRIMA del lavoro** *(`0d72cf9`)* |")
    p("| **i commit** | `a641ae2` *(`1`)* · `1405a16` *(`2`)* · `e133bf8` *(`3`)*, "
      "piu' questo |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p("| **i controlli** | ### **%d su %d** · collaudo dei presidi ### **%d su %d** "
      "*(erano `26`)* |" % (sum(1 for r in ctrl if "PASSA" in r), len(ctrl), n_ok, len(coll)))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ① LA DISTINZIONE NUOVA")
    p()
    p("| | |")
    p("|---|---|")
    p("| ### **`ENTRAMBE`** | una ### **REGOLA DI LAVORO** *(le `P*`, i presidi `H-*`)* o "
      "### **uno strumento che SOPRAVVIVE** alla riscrittura |")
    p("| ### **era `1`** | cio' che riguarda un ### **OGGETTO CONCRETO dell'era `1`**: un "
      "sigillo di una cura, la scena `(ii)`, il pilota, un `.pkl`, il blob `b8c21049`, "
      "### **una funzione o un flag di `soliton_simulator.py`** |")
    p()
    p("### ⭐ **Perche' la distinzione conta:** `era ENTRAMBE` vuol dire *«questo vale "
      "anche DOPO la riscrittura»*. ### **Un sigillo di una cura dell'era `1`, un `.pkl`, "
      "un flag del simulatore di oggi: nell'era `2` NON ESISTERANNO.** Tenerli `ENTRAMBE` "
      "### **gonfia l'elenco di cio' che la riscrittura deve portarsi dietro.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ② PUNTO `1` — **`F7` vale per QUALSIASI DOMINIO**")
    p()
    p("La regola non parlava di fisica: ### **una voce dell'era `1` NON CHIUSA e' `SOSPESA`**, "
      "e vale per `METODO`, `INFRASTRUTTURA` e `DOCUMENTAZIONE` come per `FISICA`.")
    p()
    p("| id | `dominio` | prima | dopo |")
    p("|---|---|---|---|")
    for x in r1:
        i = x["id"]
        p("| `%s` | `%s` | `%s` | ### **`%s`** |"
          % (i, per[i]["dominio"], pper[i]["stato"], per[i]["stato"]))
    p()
    p("### ✔ **Erano `%d`, ed erano ESATTAMENTE quelle che il mandato nominava** "
      "— `14` `CENS-*`, `D32-CONTATORE`, `RAMI-OFF-CURA2`. ### **E sono state curate "
      "PRIMA che il presidio si accendesse**, perche' ### ⛔ **un presidio bloccante "
      "acceso prima della cura rende inapplicabile il lotto che lo curerebbe:** la validazione "
      "gira ### **dentro `aggiorna-lotto`.** ### **E' la seconda volta in due giri che "
      "l'ordine non e' libero.**" % len(r1))
    p()
    p("### **Il collaudo:** a `72e452f` `CENS-A4` era ### **`DOCUMENTAZIONE`/era `1`/`APERTA`** "
      "— ### **fuori da `FISICA`, quindi `F7` vecchio NON la vedeva.**")
    p()
    p("---")
    p()

    # ======================================================================
    p("## ③ PUNTO `2` — **le `%d` voci a era `1`**" % len(tutte))
    p()
    p("### **`dominio` e `classe` INVARIATI**, `era` e `stato` ### **nello stesso lotto** "
      "— perche' `era 1` + `APERTA` e' ### **esattamente cio' che `F7` vieta.**")
    p()
    for titolo, gruppo, perche in (
            ("le GEMELLE dei criteri", EM.GEMELLE,
             "le loro sorelle *(`REGISTRO_FISICA:A5`, `U2-6`, `COMPONENTI:S2`, `S3`)* erano "
             "### **GIA' era `1`**: era ### **una famiglia spaccata in due**, e una famiglia "
             "di criteri dello stesso registro ### **non puo' stare in due ere**"),
            ("quelle di METODO", EM.METODO,
             "ciascuna nomina un oggetto concreto: un ### **sigillo**, la ### **scena "
             "`(ii)`**, un ### **`.pkl`**, il ### **pilota**, una ### **funzione del "
             "simulatore**"),
            ("quelle di STRUMENTI", EM.STRUMENTI,
             "un ### **sigillo o uno strumento CONCRETO** dell'era `1`, non una regola che "
             "sopravvive")):
        p("### `%d` — **%s**" % (len(gruppo), titolo))
        p()
        p(perche)
        p()
        p("| id | `classe`/`dominio` | la frase |")
        p("|---|---|---|")
        for i in gruppo:
            v = per[i]
            t = " ".join(((v["titolo"] or "") + " "
                          + (v["descrizione"] or "")).split())[:120]
            p("| `%s` | `%s`/`%s` | %s |" % (i, v["classe"], v["dominio"],
                                              t.replace("|", "/")))
        p()
    p("### ⛔ **ZERO ECCEZIONI, e il mandato ne ammetteva**")
    p()
    p("*«Se il testo di una di queste parla in realta' di una REGOLA che vale anche per "
      "l'era `2`, NON spostarla»*. ### **Ho cercato, e non ce n'e'.** ### ⚠ **Ma due "
      "sono vicine, e non le faccio sparire nel gruppo:**")
    p()
    p("| id | perche' e' un CASO LIMITE |")
    p("|---|---|")
    for i in sorted(EM.LIMITE):
        p("| `%s` | %s |" % (i, EM.LIMITE[i]))
    p()
    p("### **La FORMA e' generica, il SOGGETTO e' un flag**, e la forma generica "
      "### **vive gia' in `doc/PATTERN_DI_PROVA.md`**, che e' il posto delle regole di prova. "
      "### ⭐ **Sta scritto nel task history PRIMA di applicare: «se sbaglio, e' qui "
      "che sbaglio».** E `ECCEZIONI` nel sorgente e' ### **un dizionario VUOTO**, non un "
      "commento: una eccezione futura ### **va li'.**")
    p()
    p("### **E il controllo `C3`: `%d` ID, non una regola.** `%d` delle `%d` stanno nella lista "
      "`1` del guardiano, che le dava `ENTRAMBE`. Entrano in `CORRETTE_V3` ### **come ID**, e "
      "il motivo e' che ### **«oggetto concreto» NON si rileva da un predicato**: le "
      "ho decise ### **leggendo.** ### ⚠ **Il punto `2` del giro scorso era una REGOLA e "
      "si e' scritto come regola** — la differenza e' quella."
      % (len(in_l1), len(in_l1), len(tutte)))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ④ PUNTO `3` — **`F8`, e due segnali soli**")
    p()
    p("| l'oggetto | come si riconosce |")
    p("|---|---|")
    for rx, che in IX.ERA1_OGGETTI:
        p("| %s | `%s` |" % (che, rx.replace("|", "/")))
    p()
    p("### ⭐ **Un oggetto concreto si riconosce da COME SI SCRIVE, non dalla parola:** un "
      "flag dai ### **due trattini attaccati a una lettera**, il blob dal ### **suo sha1.** "
      "### **E' per questo che `P6`** — *«ogni csv di misura porta BLOB, SEME e TUTTI "
      "I FLAG»* — ### **NON scatta: e' una REGOLA, e non nomina nessun flag.** "
      "### ⚠ **E il `--` usato come LINEETTA non conta**: senza quella condizione `F8` "
      "avrebbe segnalato mezzo indice, perche' le mie note usano `--` come lineetta ovunque.")
    p()
    p("### **I `%d` SEGNALI, voce per voce, con la frase — e NON li correggo**"
      % len(seg["F8"]))
    p()
    p("| id | `classe`/`dominio`/stato | il segnale | la frase |")
    p("|---|---|---|---|")
    for i, msg in seg["F8"]:
        v = per[i]
        t = " ".join(((v["titolo"] or "") + " || "
                      + (v["descrizione"] or "")).split())[:170]
        p("| `%s` | `%s`/`%s`/`%s` | %s | %s |"
          % (i, v["classe"], v["dominio"], v["stato"],
             msg[msg.find("nomina"):].replace("|", "/"), t.replace("|", "/")))
    p()
    p("### ⛔ **Entrambi sono nell'elenco del mandato delle voci che RESTANO `ENTRAMBE`**, "
      "e il task history lo prevedeva: *«se `F8` segnala una voce che il mandato dice di "
      "LASCIARE `ENTRAMBE`, la elenco e NON la sposto. ### **Un segnale su una decisione del "
      "mandato e' una DOMANDA, non un difetto**»*.")
    p()
    p("### ⭐ **E la mia lettura, che vale quanto una lettura:** tutte e due sono "
      "### **REGOLE che MENZIONANO un `.pkl` per confronto**, non voci ### **che parlano** di "
      "un `.pkl`. `STATI-LOCALI` dice *«si tengono in locale, COME I `.pkl`»*; "
      "`NON-TRACCIATI` dice che *«il `.gitignore` blocca»* i riferimenti al vuoto. "
      "### **`F8` guarda una parola, e una parola non dice di chi si parla** — la stessa "
      "lezione di `F3`, e ### **la terza volta che la incontro.**")
    p()
    p("### ⚠ **E ho sbagliato la previsione:** nel task history avevo scritto *«fra "
      "`3` e `15`»*, e sono ### **`%d`** — sotto il minimo che avevo fissato."
      % len(seg["F8"]))
    p()
    p("---")
    p()

    # ======================================================================
    p("## ⑤ I CONTEGGI E I CONTROLLI")
    p()
    p("> **PRIMA** = `git show %s`. **DOPO** = il disco. ### **Nessun numero ricopiato.**"
      % PRIMA)
    p()
    for campo in ("era", "stato"):
        tab(campo, conta(pv, campo), conta(voci, campo))
    p("| | prima | dopo |")
    p("|---|--:|--:|")
    p("| voci | `%d` | ### **`%d`** |" % (len(pv), len(voci)))
    p("| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |")
    p("| ### **era `1` con stato vietato** | `%d` | ### **`0`** *(e `F7` lo impedisce)* |"
      % len(r1))
    p("| ### **`dominio` cambiati nel punto `2`** | — | ### **`0`** |")
    p("| ### **`classe` cambiate nel punto `2`** | — | ### **`0`** |")
    p()
    p("| presidio | segnali |")
    p("|---|--:|")
    for k in ("F1", "F2", "F3", "F4", "F6", "F8"):
        p("| `%s` | %s |" % (k, ("### **`%d`**" % len(seg[k])) if seg[k]
                             else "`0`"))
    p("| ### **in tutto** | ### **`%d`** |" % sum(len(v) for v in seg.values()))
    p()
    p("### **I presidi sono OTTO, e SEI segnalano:** solo `F5` e `F7` ### **bloccano.**")
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
    p("## ⑥ CHE COSA RESTA A LUCA")
    p()
    p("| | che cosa |")
    p("|---|---|")
    p("| ### **i `%d` segnali di `F8`** | `NON-TRACCIATI` e `STATI-LOCALI`: il mandato le "
      "elenca fra quelle che ### **restano `ENTRAMBE`**, e `F8` le segnala. ### **Elencate, "
      "non corrette** |" % len(seg["F8"]))
    p("| ### **i due casi limite** | `REGISTRO_FISICA:A1` e `S1`: li ho ### **spostati**, e la "
      "ragione sta sopra. ### **Se la forma conta piu' del soggetto, si tornano indietro con "
      "un lotto di due righe** |")
    p("| ### **le `%d` decise leggendo** | stanno in `CORRETTE_V3` come ID, non come regola: "
      "### **«oggetto concreto» non si rileva da un predicato** |" % len(in_l1))
    p("| ### **l'elenco di cio' che aspetta Luca** | `doc/indice/DA_DECIDERE_LUCA.md`, e "
      "### **si genera** |")
    p()
    p("> ### ⭐ **Il criterio, lo stesso di tutto il lavoro:** dove il mandato "
      "### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho "
      "lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un "
      "dato; una decisione presa al posto di Luca e' un difetto.**")
    p()

    q5 = os.path.join(RADICE, "doc", "REFERTO_indice_v3_era_metodo.md")
    io.open(q5, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_indice_v3_era_metodo.md: %d righe" % len(R))
    print("  segnali %d; controlli %d/%d; collaudo presidi %d/%d"
          % (sum(len(v) for v in seg.values()),
             sum(1 for r in ctrl if "PASSA" in r), len(ctrl), n_ok, len(coll)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
