# -*- coding: utf-8 -*-
"""**QUANTI SCRIPT DI `csv/` PRODUCONO UN REFERTO COMMITTATO E NON SI CHIAMANO `_sigillo_*`.**

**Il conteggio chiesto da Luca il 2026-10-02**, e ### **SOLO il conteggio**: questo script
### **non tocca `csv/_presidio.py` ne' `doc/ASSIOMI.md`.**

### PERCHE' SERVE *(voce `PRESIDIO-RIFIUTO-SOLO-SIGILLI`)*
`_presidio.avvia` ### **rifiuta di girare SOLO se il nome comincia con `_sigillo_`** *(`:121`)*;
per ogni altro script ### **timbra e prosegue.** ### ➜ **Quindi la protezione del par.7 copre i
sigilli e NON copre i diagnostici** — e la domanda e' **quanti** siano i diagnostici che
### **mettono un referto nel repo**, perche' per loro un numero puo' entrare in un commit ### **da
un blob che non e' quello committato.**

## LA DEFINIZIONE, dichiarata perche' il conteggio dipende da lei

| | |
|---|---|
| **lo script** | un `.py` sotto `csv/`, ### **escluso `csv/_archivio/`** *(i reperti, che non si rilanciano)* e `__pycache__` |
| **«SCRIVE»** | il sorgente contiene una **scrittura di file**: `open(..., "w")`, `json.dump`, `savefig`, `to_csv` |
| ### **«REFERTO COMMITTATO»** | esiste ### **almeno un file TRACCIATO da git** il cui percorso contiene lo **stem** dello script *(la convenzione del repo: `csv/_test_fork/_nome/...`)*, **oppure** lo script nomina un percorso **letterale** che risulta tracciato |

### ⚠ **I LIMITI, e si dichiarano invece di arrotondare il numero**
**①** la convenzione *«una cartella col nome dello script»* ### **non e' una regola cablata**: uno
script che scrive altrove ### **non viene contato**, e il conteggio e' percio' ### **una
sottostima**. **②** *«contiene `open(..., "w")`»* e' una regola ### **sulla SINTASSI**, ed e' la
forma d'errore che in questa sessione si e' ripetuta sette volte: ### **qui e' accettabile perche'
la domanda e' «quanti script POTREBBERO scrivere», non «quanti scrivono a ogni giro»** — e il
numero si legge come un **tetto superiore dei candidati** incrociato con un **fatto di git**.
**③** ### **non dice se quei referti siano STATI prodotti da un blob dirty:** dice **quanti script
sono nella classe in cui potrebbe succedere.**

COMANDO:  python csv/_conta_referti.py
ASCII puro nel codice.
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
sys.path.insert(0, _QUI)
import _presidio  # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
SCRIVE = (re.compile(r"""open\([^)]*["']w"""), re.compile(r"json\.dump"),
          re.compile(r"savefig"), re.compile(r"to_csv"))


def principale():
    q = subprocess.run(["git", "ls-files"], cwd=RADICE, capture_output=True)
    tracciati = [x.strip().replace(chr(92), "/") for x in q.stdout.decode("utf-8").split(NL)
                 if x.strip()]
    script = []
    for radice, _dirs, files in os.walk(os.path.join(RADICE, "csv")):
        rel = os.path.relpath(radice, RADICE).replace(chr(92), "/")
        if "__pycache__" in rel or rel.startswith("csv/_archivio"):
            continue
        for f in sorted(files):
            if f.endswith(".py"):
                script.append((rel + "/" + f, f[:-3]))
    righe = []
    for perc, stem in script:
        src = io.open(os.path.join(RADICE, perc), encoding="utf-8", errors="replace").read()
        scrive = any(r.search(src) for r in SCRIVE)
        # il referto committato: un file tracciato il cui percorso contiene lo stem, e che NON
        #   sia lo script stesso.
        ref = [x for x in tracciati
               if ("/" + stem + "/") in x or ("/" + stem + "_") in x or
               x.endswith("/" + stem + ".json") or x.endswith("/" + stem + ".txt")]
        ref = [x for x in ref if x != perc]
        righe.append({"script": perc, "stem": stem, "sigillo": stem.startswith("_sigillo_"),
                      "scrive": scrive, "referti_tracciati": len(ref),
                      "esempio": ref[0] if ref else None})
    tot = len(righe)
    sig = [x for x in righe if x["sigillo"]]
    non_sig = [x for x in righe if not x["sigillo"]]
    cand = [x for x in non_sig if x["scrive"]]
    con_ref = [x for x in cand if x["referti_tracciati"] > 0]
    sig_ref = [x for x in sig if x["referti_tracciati"] > 0]

    print("=" * 100)
    print("QUANTI SCRIPT DI csv/ PRODUCONO UN REFERTO COMMITTATO E NON SI CHIAMANO _sigillo_*")
    print("=" * 100)
    print("  (il conteggio chiesto da Luca il 2026-10-02. SOLO il conteggio: nessuna modifica")
    print("   a csv/_presidio.py ne' a doc/ASSIOMI.md.)")
    print("")
    print("  script `.py` sotto csv/ (escluso _archivio e __pycache__) ....... %d" % tot)
    print("  di cui chiamati `_sigillo_*` .................................... %d" % len(sig))
    print("  di cui NON chiamati `_sigillo_*` ................................ %d" % len(non_sig))
    print("     di questi, che SCRIVONO un file ............................. %d" % len(cand))
    print("  ### e di questi, con almeno un REFERTO TRACCIATO da git ........ %d"
          % len(con_ref))
    print("")
    print("  per confronto, i `_sigillo_*` con un referto tracciato .......... %d su %d"
          % (len(sig_ref), len(sig)))
    print("")
    print("  ### ➜ %d script NON coperti dal rifiuto del presidio mettono un referto nel repo,"
          % len(con_ref))
    print("        contro %d sigilli che lo sono. Il rapporto e' %s a 1."
          % (len(sig_ref), ("%.1f" % (len(con_ref) / max(len(sig_ref), 1)))))
    print("")
    print("  I LIMITI, dichiarati: la convenzione <<una cartella col nome dello script>> non e'")
    print("  cablata, quindi chi scrive altrove NON e' contato -> il numero e' una SOTTOSTIMA.")
    print("  E <<contiene open(...,'w')>> e' una regola sulla SINTASSI: si legge come un tetto")
    print("  dei CANDIDATI, incrociato con un fatto di git (il referto tracciato).")
    print("")
    print("  I PRIMI 25, per nome:")
    for x in sorted(con_ref, key=lambda z: z["script"])[:25]:
        print("    %-46s referti tracciati %3d   es. %s"
              % (x["script"], x["referti_tracciati"], (x["esempio"] or "")[:44]))
    if len(con_ref) > 25:
        print("    ... e altri %d" % (len(con_ref) - 25))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
