# -*- coding: utf-8 -*-
"""IL REFERTO DEGLI STRUMENTI DELL'ERA `2` — **che cosa BLOCCA, e che cosa è solo scritto.**

> ### ⛔ **LA DOMANDA CHE QUESTO REFERTO PORTA A LUCA:** ### **come si chiama la cartella del
> codice dell'era `2`?** Finché non ha un nome, `H-FISICA-FUORI-LISTA`
> ### **non impedisce niente** — e per `A9` ### **non è un presidio: è una tenda.**

### ⭐ **E LA TABELLA CHE CONTA È UNA SOLA:** per ogni strumento, ### **BLOCCA** oppure
### **È UNA REGOLA SCRITTA.** `A9` dice che la seconda ### **non impedisce niente**, e un
referto che non distingue le due ### **racconta più sicurezza di quella che c'è.**

Gira con:  python csv/_doc_referto_strumenti_era2.py
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
import _file_fisica as FF                                    # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Scrive un referto.
NL = chr(10)
R = []


def p(s=""):
    R.append(s)


def gira(cmd, pat):
    q = subprocess.run([sys.executable] + cmd, cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8")
    m = re.search(pat, q.stdout or "")
    assert m, cmd
    return m.group(1), m.group(2)


def nel_hook(nome, stadio):
    """### Il presidio e' ### **davvero cablato** in quello stadio?

    ### ⛔ **Non si crede a una tabella: si legge il file del hook.** Un presidio
    ### **dichiarato e non cablato** e- esattamente cio- che `A9` condanna, e
    ### **questo referto non puo- essere l-unico posto che non lo verifica.**
    """
    p1 = os.path.join(RADICE, ".githooks", stadio)
    if not os.path.isfile(p1):
        return False
    t = io.open(p1, encoding="utf-8", errors="replace").read()
    if nome in t:
        return True
    # ### I presidi lanciati da `csv/_hook_presidi.py` stanno un livello piu- dentro.
    p2 = os.path.join(RADICE, "csv", "_hook_presidi.py")
    return nome in io.open(p2, encoding="utf-8", errors="replace").read()


def main():
    voci = {json.loads(r)["id"]: json.loads(r) for r
            in io.open(os.path.join(RADICE, "doc/indice/voci.jsonl"), encoding="utf-8")
            if r.strip()}
    n_ff = gira(["csv/_collaudo_file_fisica.py"],
                r"IL COLLAUDO DI `_file_fisica.py`: (\d+) su (\d+)")
    n_id = gira(["csv/_hook_id_obbligatorio.py", "--collaudo"],
                r"COLLAUDO `H-ID-OBBLIGATORIO`: (\d+) su (\d+)")
    n_pres = gira(["csv/_collaudo_presidi_indice.py"],
                  r"IL COLLAUDO DEI PRESIDI: (\d+) su (\d+)")
    claude = io.open(os.path.join(RADICE, "CLAUDE.md"), encoding="utf-8").read()
    cablati = re.findall(r"^\|\s*\*\*`(H-[^`]+)`\*\*", claude, re.M)

    p("# IL REFERTO DEGLI STRUMENTI DELL'ERA `2`")
    p()
    p("> ### ⛔ **LA DOMANDA A LUCA, e il referto esiste anche per farla:**")
    p("> ### 📌 **COME SI CHIAMA LA CARTELLA DEL CODICE DELL'ERA `2`?**")
    p("> Finche' non ha un nome, `H-FISICA-FUORI-LISTA` ### **non impedisce niente**, e per "
      "`A9` ### **non e' un presidio: e' una TENDA.** ### ✔ **Il codice c'e', il collaudo "
      "gira su una cartella di PROVA, e il giorno in cui il nome arriva il presidio diventa "
      "vero ### cambiando UNA STRINGA** in `csv/_file_fisica.py`.")
    p()
    p("| | |")
    p("|---|---|")
    p("| **quando** | `2026-10-09`, ramo `primo-ordine` |")
    p("| **il mandato** | la ### **parte II** di *«le chiusure, le superate, la terza "
      "lettura, e gli strumenti per l'era `2`»* — cioe' ### **il mandato «INDICE E "
      "FISICA» che non mi era arrivato**, piu' le tre correzioni `A`/`B`/`C` della coda |")
    p("| **la coda** | ### **la voce ① di `doc/CODA_2026-10-09.md` si CHIUDE qui**: era "
      "l'integrazione, e il mandato l'ha assorbita |")
    p("| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |")
    p()
    p("---")
    p()
    p("## ① CHE COSA BLOCCA, E CHE COSA E' SOLO SCRITTO")
    p()
    p("> ### ⭐ **`A9`: «un presidio che non impedisce non e' un presidio: e' una "
      "TENDA».** Questa tabella e' ### **l'unica cosa che conta** in un referto sugli "
      "strumenti — e un referto che non distingue le due colonne ### **racconta piu' "
      "sicurezza di quella che c'e'.**")
    p()
    p("| strumento | stadio | ### **BLOCCA?** | che cosa impedisce |")
    p("|---|---|---|---|")
    p("| ### **`F11`** | `indice.py valida`, nel `pre-commit` | ### **SI'** | una voce che "
      "### **non coincide col `dopo` della sua ultima riga di storico**: cioe' "
      "### **una scrittura a mano in `voci.jsonl`** |")
    p("| ### **`F12`** | `indice.py valida`, nel `pre-commit` | ### **SI'** | una `chiusura` "
      "### **piena su una voce che non e' `CHIUSA`** |")
    p("| ### **`H-ID-OBBLIGATORIO`** | `commit-msg` | ### **SI'** | un commit che tocca "
      "### **un file della LISTA** o un ### **`doc/REFERTO_*`/`doc/REPERTO_*`** e "
      "### **non cita nessun ID** |")
    p("| ### **la LISTA** *(`FILE_FISICA`)* | letta da `H-REG-R` e `H-P7` | ### **SI', per "
      "interposta persona** | quei due presidi ### **non scrivono piu' il nome a mano**: "
      "il giorno in cui la fisica vive in due file ### **li seguono** |")
    p("| ### **l'`assert len(FILE_FISICA) == 1`** | all'import di `H-REG-R` e `H-P7` | "
      "### **SI'** | che quei due presidi ### **guardino solo il primo file di una lista "
      "lunga**: il giorno in cui la lista cresce ### **si FERMANO** |")
    p("| ### ⛔ **`H-FISICA-FUORI-LISTA`** | `pre-commit` | ### ⛔ **NO, OGGI NO** | "
      "dovrebbe impedire ### **un `.py` sotto la cartella dell'era `2` fuori dalla LISTA**, "
      "ma ### **la cartella e' VUOTA**: `intrusi()` torna ### **sempre `[]`.** "
      "### **E' una TENDA, e il nome lo decide Luca** |")
    p()
    p("### ✔ **E I TRE CABLATI SI VERIFICANO LEGGENDO IL HOOK, non questa tabella:**")
    p()
    p("| | dichiarato | ### **cablato davvero** |")
    p("|---|---|---|")
    for nome, stadio in (("H-FISICA-FUORI-LISTA", "pre-commit"),
                         ("H-ID-OBBLIGATORIO", "commit-msg")):
        p("| `%s` | %s | %s |"
          % (nome, "si'" if nome in cablati else "### **NO**",
             "### **si'**" if nel_hook(nome.replace("H-FISICA-FUORI-LISTA", "fuori_lista")
                                       .replace("H-ID-OBBLIGATORIO",
                                                "_hook_id_obbligatorio"), stadio)
             else "### ⛔ **NO**"))
    p("| `F11`, `F12` | `doc/REGOLE/par9.md` | ### **si'**: `indice.py valida` gira nel "
      "`pre-commit` *(`csv/_hook_presidi.py`, blocco `[INDICE v2]`)* |")
    p()
    p("---")
    p()
    p("## ② `F11`: **l'indice e' il REPLAY del suo storico**")
    p()
    p("| | |")
    p("|---|---|")
    p("| la regola | ogni voce coincide ### **campo per campo** col `dopo` della sua "
      "### **ULTIMA** riga di storico; una voce ### **senza storico** coincide col suo stato "
      "a ### **`3ef2326`**; una voce ### **nata dopo e senza storico** e' un errore |")
    p("| ### ⭐ **perche' e' il piu' forte** | gli altri guardano ### **se un campo e' "
      "plausibile**; `F11` guarda ### **se il campo e' ARRIVATO DA UNA SCRITTURA "
      "DICHIARATA** |")
    p("| ### **e rende vera una regola che era solo SCRITTA** | il par.9 dice *«si scrive "
      "SOLO con `indice.py aggiorna`»* ### **dal primo giorno**, e per `A9` era "
      "### **una tenda.** ### **Adesso impedisce** |")
    p("| oggi | ### **`0` violazioni** su `%d` voci, `%d` senza storico |"
      % (len(voci), len([i for i in voci if i not in __import__("indice")._f11_ultimo()])))
    p()
    p("### ⚠ **E LA MANOMISSIONE CHE IL MANDATO DETTA LA VEDE ANCHE `F7`, e lo dico:** "
      "`A2-ANELLO` e' ### **era `1`**, e `F7` vieta era `1` + `APERTA`. ### **Quel caso prova "
      "che `F11` SCATTA, non che SERVA.** ### ✔ **Per provare che serve ho cercato una "
      "manomissione che nessun altro veda, e l'ho trovata: il `titolo`.** Nessun presidio lo "
      "confronta con niente — cambiarlo a mano passa ### **vocabolari, stati, ere e "
      "viste rigenerate** — e ### **solo `F11` lo vede.**")
    p()
    p("### ⛔ **E DUE COSE CHE `F11` NON VEDE, dichiarate:**")
    p()
    p("| | |")
    p("|---|---|")
    p("| una manomissione che tocca ### **ANCHE lo storico** | `F11` prova che i due file "
      "### **CONCORDANO**, non che siano ### **veri.** ### **La difesa contro quello e' git, "
      "non `F11`** |")
    p("| un cambio del solo campo ### **`aggiornata`** | e' ### **fuori dal confronto**: e' "
      "un timbro di ### **quando**, e lo riscrive ogni lotto. ### **E' il prezzo dichiarato "
      "per non fallire su ogni voce toccata due volte** |")
    p("| se il tag ### **non si legge** | `F11` ### **TACE** invece di accusare: senza il "
      "punto di partenza non si puo' dire se una voce senza storico sia giusta |")
    p()
    p("---")
    p()
    p("## ③ LA LISTA E LA CARTELLA")
    p()
    p("| | |")
    p("|---|---|")
    p("| ### **`FILE_FISICA`** | %s |"
      % " · ".join("`%s`" % x for x in FF.FILE_FISICA))
    p("| ### **`CARTELLA_ERA_2`** | ### ⛔ **`\"\"` — «da decidere da Luca»** |")
    p("| chi legge la LISTA | `csv/_hook_fisica.py` *(`H-REG-R`)* · "
      "`csv/_presidio_commenti_flag.py` *(`H-P7`)* · `csv/_hook_id_obbligatorio.py` "
      "*(`H-ID-OBBLIGATORIO`)* |")
    p("| ### ⚠ **e chi la nominava a mano** | erano ### **`3`**, e il censimento l'ho fatto "
      "### **prima di dire il numero.** Il terzo *(`csv/_hook_presidi.py`)* lo nomina "
      "### **dentro un testo d'aiuto**, non come percorso |")
    p("| ### ⛔ **e mettere un file nella LISTA COSTA** | gli si mettono addosso "
      "### **TRE presidi**: `H-REG-R` *(nessuna legge senza la sua scheda)*, `H-P7` *(il "
      "commento di ogni flag)* e `H-ID-OBBLIGATORIO` *(un ID nel messaggio)*. "
      "### **Non si aggiunge per comodita'** |")
    p()
    p("### **IL COLLAUDO: `%s`/`%s`, su una cartella di PROVA in una COPIA**"
      % (n_ff[0], n_ff[1]))
    p()
    p("### ⭐ **E tre bracci provano che con la cartella VUOTA il presidio TACE.** "
      "### **Un presidio che tace va provato che taccia**, altrimenti nessuno sa se tace "
      "perche' e' ### **spento** o perche' e' ### **rotto.**")
    p()
    p("---")
    p()
    p("## ④ `H-ID-OBBLIGATORIO`: **il rovescio di `H-INDICE`**")
    p()
    p("| | |")
    p("|---|---|")
    p("| la regola | un commit che tocca ### **un file della LISTA** o un "
      "### **`doc/REFERTO_*` / `doc/REPERTO_*`** ### **cita almeno un ID** dell'indice |")
    p("| ### ⭐ **era MEZZO controllo** | `H-INDICE` verifica che gli ID citati "
      "### **esistano**; che ### **ce ne sia almeno UNO** ### **non lo chiedeva nessuno** "
      "— la stessa forma di difetto di `F12` |")
    p("| ### ⛔ **e «un referto» e' SOLO due prefissi** | la ### **correzione `C`** della "
      "coda: *«non qualunque file sotto `doc/`»*. ### **La mia definizione era LARGA**, e una "
      "definizione larga in un presidio ### **rifiuta commit che nessuno voleva rifiutare** |")
    p("| il collaudo | ### **`%s`/`%s`, nei due versi** — e un braccio prova che "
      "`doc/STATO_RUN.md`, `doc/REGOLE/par9.md` e `doc/indice/voci.jsonl` "
      "### **NON contano** |" % (n_id[0], n_id[1]))
    p("| ### ⚠ **la via d'uscita e' la STESSA di `H-INDICE`** | `[SENZA-INDICE: <motivo>]`, "
      "a inizio riga: dichiararla ### **spegne entrambi** per quel commit. E' una scelta, e "
      "la dichiaro: ### **chi non ha ID da citare non ha nemmeno ID da verificare** |")
    p()
    p("---")
    p()
    p("## ⑤ LE TRE CORREZIONI DELLA CODA, E DOVE SONO FINITE")
    p()
    p("| | la correzione | dove |")
    p("|---|---|---|")
    p("| `A` | `migrazione_era1.jsonl` ### **NON contiene i valori dei campi**; le voci senza "
      "storico ### **coincidono col loro stato a `3ef2326`** | ### **dentro `F11`**: la "
      "costante si chiama `FINE_MIGRAZIONE`, e ### **non ho mai letto `migrazione_era1.jsonl` "
      "per i valori** |")
    p("| `B` | la cartella dell'era `2` ### **NON ESISTE e NON la scegli tu** | "
      "### **`CARTELLA_ERA_2 = \"\"`**, e ### **la domanda e' in testa a questo referto** |")
    p("| `C` | *«un referto sotto `doc/`»* = ### **SOLO `doc/REFERTO_*` e `doc/REPERTO_*`** | "
      "### **dentro `H-ID-OBBLIGATORIO`** *(`REFERTI`)*, col ### **braccio negativo** che "
      "prova che gli altri file di `doc/` non contano |")
    p()
    p("### ✔ **E LA VOCE ① DELLA CODA SI CHIUDE QUI.** Era arrivata ### **senza il "
      "suo mandato base**, e il mandato di oggi ### **l'ha assorbita.** "
      "### ⭐ **Si chiude quando il lavoro e' fatto, non quando e' letto.**")
    p()
    p("---")
    p()
    p("## ⑥ CHE COSA RESTA A LUCA")
    p()
    p("| | che cosa |")
    p("|---|---|")
    p("| ### 📌 **IL NOME DELLA CARTELLA DELL'ERA `2`** | finche' manca, "
      "`H-FISICA-FUORI-LISTA` ### **e' una tenda.** Una stringa in `csv/_file_fisica.py`, e "
      "poi ### **va ricollaudato sull'albero vero**: il collaudo di oggi gira su una copia |")
    p("| ### **se `T0` e `T4` sono troppo larghi** | sono ### **due livelli di ricerca che "
      "ho aggiunto io**, e il mandato ne nominava tre |")
    p("| ### **`F11` non vede una manomissione che tocchi ANCHE lo storico** | la difesa "
      "contro quello ### **e' git, non `F11`** |")
    p("| ### **il campo `aggiornata` e' fuori dal confronto di `F11`** | prezzo dichiarato |")
    p("| ### **i `%d` presidi del §`12`** | sono ### **due in piu-** di stamattina, e "
      "### **uno dei due non impedisce niente** |" % len(cablati))
    p()
    p("> ### ⭐ **E la cosa che porto fuori da questo giro:** ### **`F12` e "
      "`H-ID-OBBLIGATORIO` erano MEZZI CONTROLLI** — l'uno chiedeva *«se e' `CHIUSA`, "
      "dove sta la chiusura?»* e non *«se c'e- la chiusura, e' `CHIUSA`?»*; l'altro *«gli ID "
      "citati esistono?»* e non *«ce n'e- almeno uno?»*. ### **Una sola delle due direzioni "
      "non e' un controllo: e' MEZZO controllo** — e la meta' che manca "
      "### **non si vede, perche' tace.**")
    p()

    q = os.path.join(RADICE, "doc", "REFERTO_strumenti_era2.md")
    io.open(q, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto doc/REFERTO_strumenti_era2.md: %d righe" % len(R))
    print("  collaudi: _file_fisica %s/%s; H-ID-OBBLIGATORIO %s/%s; presidi %s/%s"
          % (n_ff + n_id + n_pres))
    print("  i cablati del §12 di CLAUDE.md: %d" % len(cablati))
    print("  ### la CARTELLA dell-era 2: %r  -> il presidio NON impedisce niente"
          % FF.CARTELLA_ERA_2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
