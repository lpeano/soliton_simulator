# -*- coding: utf-8 -*-
"""IL QUADRO UNICO -- tre elenchi nel `PUNTO DI RIPRESA` di `doc/STATO_RUN.md`. **Generato.**

Decisione di Luca, 2026-09-24: *«troppi fili aperti, il lavoro buono non deve perdersi per
strada»*.

  A. **ACQUISITO**            -- in codice **E** acceso nei run: flag, sigillo, prova, commit.
  B. **DECISO, NON IN CODICE** -- la decisione e il suo commit.
  C. **APERTO**               -- una riga per voce, col posto dove vive.

⚠ COSA E' GENERATO E COSA E' SCRITTO A MANO -- la stessa dichiarazione di `_cure_verificate.py`,
  perche' la differenza e' cio' che rende il quadro affidabile:

  GENERATO, a ogni giro, dal DISCO:
    * `A` intera: **importa `CURE` da `_cure_verificate.py`** (una sola fonte, non una copia),
      legge il **DEFAULT dal sorgente** e verifica **se il DRIVER accende il flag**, leggendo
      l'argv cablato in `csv/_test_fork/_scena_video.py`. **E' il campo che decide se una cura
      GIRA DAVVERO**, e la sezione `CURE VERIFICATE` esiste proprio perche' si sfalsa da solo;
    * per ogni voce di `B`: **la verifica che NON sia in codice**, cercando il suo marcatore
      nel sorgente. **Se un giorno c'e', la riga si segnala da sola** -- che e' il solo modo
      perche' `B` non diventi una lista di buoni propositi;
    * per ogni voce di `C` che porta un marcatore: **se esiste ancora**;
    * lo stato dei **RAMI**: `main` e la sua data, da `git`.

  SCRITTO A MANO (dati nel corpo di questo file, ciascuno col suo commit):
    * il TESTO delle decisioni di `B` e delle voci di `C`. **Un'interpretazione non si genera.**

**SI RIGIRA A OGNI COMMIT CHE CAMBIA UNA CURA O UNA DECISIONE** (Luca).
SOLA LETTURA sul simulatore: lo legge come TESTO, non lo importa.
ASCII PURO.
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
CODA = os.path.join(RADICE, "doc", "STATO_RUN.md")
INI, FIN = "<!-- QUADRO-INIZIO -->", "<!-- QUADRO-FINE -->"

# ---------------------------------------------------------------- B: deciso, non in codice
# (titolo, la decisione, dove vive, commit, marcatore che PROVEREBBE che e' in codice)
DECISO = [
    ("IL FRENO-LEGGE: la forma",
     "`(d - LAM) <- (d - LAM) * (1 + tanh(dx/d))`. Deriva **esattamente nulla**, e il suo unico "
     "prezzo -- la saturazione a `2` -- **si paga zero volte**: `max |dx|/d = 0.0531` su "
     "`125 731 076` campioni, **zero oltre `0.5`**.",
     "scheda (11) par.4-quinquies + `D31` nella `STATO` della scheda (1)",
     "`19cea14`", "1.0 + np.tanh"),
    ("`LAM` STRUTTURALE",
     "*«nessuna lunghezza sotto `LAM`»* deve diventare **strutturale**, non un freno che ci "
     "arriva. Oggi `E4-LAM` la **VERIFICA sempre** (`6/6`), ma la **realizzazione** e' ancora il "
     "freno a senso unico.",
     "`D31`, e il punto (2) di `E4-LAM`", "`e8d8ba1`", None),
    ("EPOCA 3 = i default nel sorgente",
     "i `default` dei flag delle cure **restano `False`** e si cambiano **all'epoca 3**. Fino "
     "ad allora **le accende il DRIVER**, run per run.",
     "questa sezione, colonna *driver* di `A`", "*(decisione di Luca, 2026-09-24)*", None),
    ("`CURA 3` -- `phi` su `2pi` con le soglie che la seguono",
     "nella **forma decisa**: frazioni che sul dominio `4pi` danno **ESATTAMENTE** i valori di "
     "oggi, flag spento, sigillo con **un processo per braccio**, giro corto contro `CURA 2`.",
     "mandato di Luca; scheda da scrivere", "*(mandato del 2026-09-24)*", "CURA_3"),
    ("`TW_SPINORE` bloccato PER SEMPRE",
     "e' **gia' in codice** come presidio (il simulatore **rifiuta di partire**), ma la "
     "decisione *«per sempre»* e' di Luca e va letta qui: **non e' una cura, e' un "
     "IMPEDIMENTO** -- la legge non ha mai girato, quindi non ha prodotto nulla da curare.",
     "`CURE VERIFICATE`, sezione *presidio strutturale*", "`dd82794a`", "[tw-spinore] RIFIUTO"),
]

# ---------------------------------------------------------------- C: aperto
# (voce, dove vive, marcatore da verificare o None)
APERTO = [
    ("**`S08`** -- il sito `S08_proj`: `proj` e' ADIMENSIONALE e viene sommato a una LUNGHEZZA; "
     "l'unica cosa che gli da' unita' e' il clip",
     "scheda (2) `memoria-del-moto`; `Z112`", "S08_proj"),
    ("**LA MAPPA DEI TEMPI** -- quanti tempi ha il sistema, e quali sono la stessa cosa con nomi "
     "diversi. **Sospesa dal `PROMPT UNICO`, mai ripresa**",
     "mandato del 2026-09-24, punto (4)", None),
    ("**`D33`** -- la repulsione che si spegne al tetto. **E' dentro il perimetro di `CURA 2`** "
     "e il criterio `R` l'ha sfiorato: `d0` si muove del `+-3 %`, non del `x2.5` previsto",
     "scheda (7) `mitosi-schwinger`", None),
    ("**CHI SPINGE CONTRO IL MURO** -- quali siti spingono `d` verso `LAM` e con che peso. Il "
     "bilancio dice **chi fa crescere `d0`**; questo chiede **chi la fa scendere**",
     "scheda (1) + il bilancio di `G4`", None),
    ("**IL CLAMP MORTO IN `_cs_arco_da_nodo`** -- `np.maximum(cs_i + cs_j, 1e-12)`. **Protegge "
     "da un errore, e `A11` dice di cercare l'errore**: `cs > 0` e' DERIVATO (`cs_floor > 0`), "
     "quindi il clamp non puo' mordere. **E' EREDITATO da `step()`, non l'ho aggiunto io** -- e "
     "la cura e' toglierlo **dal sito originale**, non solo dalla copia",
     "scheda (9) par.10.1; `:4791` e il metodo estratto", "cs_nodo[ii] + cs_nodo[jj], 1e-12"),
    ("**`S09`** -- l'orologio *non si sposta, si allarga*: il criterio va **riformulato** "
     "(rilievo di Luca sul `0746144`)", "`CURA 1`, referto dell'orologio", None),
    ("**`S11`** e **`S13`** -- sospetti mai promossi ne' chiusi", "coda dei sospetti", None),
    ("**IL PONTE VERO** -- la torsione presa dal **trasporto SU(2)**, non da `phi`. **E' il "
     "motivo per cui `TW_SPINORE` e' bloccato**: quel ponte era INVERSO. Il ponte giusto non "
     "esiste ancora",
     "mappa del `4pi`, le due voci `INVERSA`; scheda (8)", None),
    ("**IL MERGE DI `main`** -- `doc/PIANO_merge_main.md`. **`fork-su2` e' l'unico ramo vivo.** "
     "**E' una DECISIONE DI LUCA: si segnala, non si fa**", "`doc/PIANO_merge_main.md`", None),
    ("**`mean((dx/d)^2)` NON REGISTRATO** -- direbbe **di quanto** la forma piana sarebbe stata "
     "peggiore. **Costa ZERO run in piu'**: una somma, sugli stessi campioni",
     "scheda (11) par.4-quinquies", None),
    ("**LA LEGGE DI `CURA 2` E' SALVA PER L'ORDINE DELLE CHIAMATE, non per una guardia** -- "
     "`_r_nodo_mitosi` legge `_r_corrente` **prima** che la mitosi allunghi `n`. **Basta "
     "spostare una riga.** Le tre guardie hanno **zero salti**, e non per merito loro",
     "scheda (9) par.10; referto di `CURA 2` par.4", None),
]


def contiene(percorso, ago):
    try:
        return ago in io.open(percorso, encoding="utf-8", errors="replace").read()
    except Exception:
        return False


def default_di(sorg, flag):
    m = re.search(r"^%s\s*=\s*(True|False)\b" % re.escape(flag), sorg, re.M)
    return m.group(1) if m else "?"


def argv_driver():
    """Le opzioni cablate nel driver: e' cio' che decide se una cura GIRA DAVVERO."""
    t = io.open(DRIVER, encoding="utf-8", errors="replace").read()
    return set(re.findall(r'"(--[a-z0-9-]+)"', t)) | set(re.findall(r"'(--[a-z0-9-]+)'", t))


def opzione_di(flag):
    return "--" + flag.lower().replace("_", "-")


def rami():
    def g(*a):
        try:
            return subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True,
                                  text=True, encoding="utf-8", errors="replace").stdout.strip()
        except Exception:
            return "?"
    fuori = []
    for b in ("fork-su2", "main"):
        fuori.append((b, g("log", "-1", "--format=%h %ad", "--date=short", b)))
    return fuori


def main():
    sorg = io.open(SORGENTE, encoding="utf-8", errors="replace").read()
    opz = argv_driver()
    from _cure_verificate import CURE

    R = []
    W = lambda s: R.append(s)

    W(INI)
    W("")
    W("## IL QUADRO UNICO — **tre elenchi, GENERATI** *(decisione di Luca, 2026-09-24)*")
    W("")
    W("> *«Troppi fili aperti, il lavoro buono non deve perdersi per strada.»*")
    W("> **Generato da `csv/_quadro_unico.py`, e si rigira a ogni commit che cambia una cura o")
    W("> una decisione.** **Il DEFAULT e la colonna *driver* si leggono dal DISCO a ogni giro**;")
    W("> il testo delle decisioni e dei fronti e' **scritto a mano**, ciascuno col suo commit —")
    W("> *un'interpretazione non si genera, una condizione del codice si'.*")
    W("")

    # ------------------------------------------------------------------ A
    W("### A. ✅ ACQUISITO — **in codice E acceso nei run**")
    W("")
    W("| flag | cura | default | **il driver lo accende?** | sigillo |")
    W("|---|---|:--:|:--:|--:|")
    acceso = 0
    for c in CURE:
        flag, nome, sig = c[0], c[1], c[2]
        d = default_di(sorg, flag)
        o = opzione_di(flag)
        su = (d == "True") or (o in opz)
        acceso += 1 if su else 0
        W("| `%s` | %s | **`%s`** | %s | %s |"
          % (flag, nome, d,
             ("✅ **sì** *(`%s`)*" % o) if o in opz else
             ("✅ *(default `True`)*" if d == "True" else "❌ **NO**"), sig))
    W("")
    W("**Accese nei run: %d su %d.** *(Il `default` nel sorgente resta `False`: **i default si "
      "cambiano all'epoca 3**, voce `B`.)*" % (acceso, len(CURE)))
    W("")
    W("> **⚠ IL FATTO CHE QUESTA COLONNA RENDE VISIBILE:** una cura con `default False` e **senza")
    W("> la riga nell'argv del driver** *non gira*, e nessun sigillo se ne accorge — il sigillo")
    W("> certifica che il flag **funziona**, non che sia **acceso**. **La colonna si legge dal")
    W("> driver, non dalla mia memoria.**")
    W("")

    # ------------------------------------------------------------------ B
    W("### B. 🟨 DECISO DA LUCA, **non ancora in codice**")
    W("")
    W("| decisione | contenuto | dove vive | commit | **già in codice?** |")
    W("|---|---|---|--:|:--:|")
    for titolo, testo, dove, commit, marc in DECISO:
        if marc is None:
            stato = "— *(non verificabile da un marcatore)*"
        elif contiene(SORGENTE, marc):
            stato = "⚠ **SÌ — la riga va spostata in `A`**"
        else:
            stato = "no *(verificato dal sorgente)*"
        W("| **%s** | %s | %s | %s | %s |" % (titolo, testo, dove, commit, stato))
    W("")
    W("> **La colonna *già in codice* è GENERATA**: cerca il marcatore nel sorgente a ogni giro.")
    W("> **È il solo modo perché `B` non diventi una lista di buoni propositi**: il giorno in cui")
    W("> una decisione entra nel codice, **la riga si segnala da sola**.")
    W("")

    # ------------------------------------------------------------------ C
    W("### C. 🟥 APERTO — **una riga per voce, col posto dove vive**")
    W("")
    W("| | fronte | dove vive | esiste ancora? |")
    W("|--:|---|---|:--:|")
    for k, (voce, dove, marc) in enumerate(APERTO, 1):
        if marc is None:
            stato = "—"
        elif contiene(SORGENTE, marc):
            stato = "✅ **sì**"
        else:
            stato = "⚠ **no: la voce va rivista**"
        W("| `%d` | %s | %s | %s |" % (k, voce, dove, stato))
    W("")

    # ------------------------------------------------------------------ rami
    W("### I RAMI — **letti da `git` a ogni giro**")
    W("")
    W("| ramo | ultimo commit |")
    W("|---|---|")
    for b, riga in rami():
        W("| `%s` | %s |" % (b, riga or "*(assente in locale)*"))
    W("")
    W("> **`fork-su2` è l'unico ramo vivo.** **Il merge è una DECISIONE DI LUCA**")
    W("> *(`doc/PIANO_merge_main.md`)*: **si segnala, non si fa** — ed è la voce `9` di `C`.")
    W("")
    W(FIN)

    blocco = "\n".join(R)
    t = io.open(CODA, encoding="utf-8", newline="").read()
    if INI in t and FIN in t:
        i, j = t.index(INI), t.index(FIN) + len(FIN)
        t = t[:i] + blocco + t[j:]
        dove = "SOSTITUITO"
    else:
        anc = "## LO STATO DELLE CURE"
        assert t.count(anc) == 1, "ancora non unica: %d" % t.count(anc)
        t = t.replace(anc, blocco + "\n\n" + anc)
        dove = "INSERITO"
    io.open(CODA, "w", encoding="utf-8", newline="\n").write(t)
    print("quadro unico %s: %d cure (%d accese nei run), %d decisioni, %d fronti aperti"
          % (dove, len(CURE), acceso, len(DECISO), len(APERTO)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
