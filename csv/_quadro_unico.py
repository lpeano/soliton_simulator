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
    ("**`S08`** -- **se `phi` non e' l'azimut del Bloch, CHE COS'E'?** `Z121` ha **refutato** "
     "la frase del docstring *(`R <= 0.18` contro un nullo di `0.016`, criterio `>= 0.90`)*, "
     "**ma non ha detto che cosa `phi` SIA**. **E' la domanda del PONTE VERO** *(voce 8)*, "
     "presa dall'altro capo",
     "`doc/STATO_RUN.md`, tabella dei sospetti, riga `S08`", None),
    ("**`S08_proj`** -- **NON e' `S08`, ed e' un'altra cosa**: `proj` e' ADIMENSIONALE e viene "
     "sommato a una LUNGHEZZA; l'unica cosa che gli da' unita' e' il clip *(`A11`)*. "
     "**Li avevo confusi nel primo quadro** *(rilievo di Luca)*",
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


def stato_dal_sigillo():
    """LO STATO EFFETTIVO, dal SIGILLO DEL DRIVER -- non dal testo del driver.

    ⚠ **LA VERSIONE PRECEDENTE CERCAVA IL NOME `"--peq-esatto"` NEL FILE, e lo TROVAVA**:
    la riga c'e', ma dentro una CONDIZIONE --
        `+ (["--peq-esatto"] if PEQESATTO == "on" else [])`
    con `PEQESATTO` che **di default vale `"off"`**. **Il nome e' presente, la cura NO.**
    Il quadro diceva `SI'` a SEI cure che l'invocazione nuda **non accende**, e lo diceva
    **mentre il sigillo del driver, nello stesso repo, stampava `NUDA = False` per quelle
    sei.** *(Rilievo di Luca, 2026-09-24.)*

    ### **E' lo `STANDARD 9` preso al contrario: ho dichiarato una PRESENZA da un `in` sul
    ### testo, dove serviva la CONDIZIONE.** La regola nomina le assenze; **una presenza
    ### dedotta da un `in` e' lo stesso errore col segno opposto.**

    Ora si legge **il REFERTO DEL SIGILLO**, che percorre `_cli()` + `_applica_flag(a)` in un
    processo nuovo e legge lo stato **DAL MODULO**. Se il referto manca, si DICHIARA: **non si
    indovina**.
    """
    p = os.path.join(RADICE, "csv", "_seal_fork", "_sig_driver_accende", "REFERTO.txt")
    if not os.path.exists(p):
        return None
    t = io.open(p, encoding="utf-8", errors="replace").read()
    fuori = {}
    for r in t.splitlines():
        m = re.match(r"^\s{2}([A-Z][A-Z0-9_]+)\s+(True|False|ASSENTE)\s+(True|False|ASSENTE)\b", r)
        if m:
            fuori[m.group(1)] = (m.group(2) == "True", m.group(3) == "True")
    return fuori or None


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
    sig = stato_dal_sigillo()
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
    if sig is None:
        W("> ⚠ **IL REFERTO DEL SIGILLO DEL DRIVER MANCA**, quindi la colonna *«il driver lo")
        W("> accende?»* **non si puo' generare**. Si dichiara invece di indovinare: gira")
        W("> `python csv/_seal_fork/_sigillo_driver_accende.py` e rigenera.")
        W("")
    W("| flag | cura | default | **NUDA** | **CAMPAGNA** | sigillo |")
    W("|---|---|:--:|:--:|:--:|--:|")
    acceso = 0
    nudo_no = []
    for c in CURE:
        flag, nome, s_sig = c[0], c[1], c[2]
        d = default_di(sorg, flag)
        vn, vc = (sig or {}).get(flag, (None, None))
        if vc:
            acceso += 1
        if vc and not vn:
            nudo_no.append(flag)
        sim = lambda v: "?" if v is None else ("✅" if v else "❌")
        W("| `%s` | %s | **`%s`** | %s | %s | %s |"
          % (flag, nome, d, sim(vn), sim(vc), s_sig))
    W("")
    W("> **LE DUE COLONNE SI LEGGONO DAL SIGILLO DEL DRIVER** — `_cli()` + `_applica_flag(a)`")
    W("> in un processo nuovo, stato letto **dal MODULO**. **NUDA** = i soli argomenti")
    W("> posizionali; **CAMPAGNA** = gli argomenti che `_g4_prova.py` passa davvero.")
    W("")
    W("**Accese in CAMPAGNA: %d su %d.** *(Il `default` nel sorgente resta `False`: **i default "
      "si cambiano all'epoca 3**, voce `B`.)*" % (acceso, len(CURE)))
    W("")
    if nudo_no:
        W("> ### ⚠ **ACCESE SOLO DAL COMANDO, NON DAL DRIVER: %d** — %s"
          % (len(nudo_no), ", ".join("`%s`" % x for x in nudo_no)))
        W("> **Non sono nel codice: sono nell'argv di CHI LANCIA**, e un comando che ne")
        W("> dimentica una gira su un sistema che si sa difettoso *(`P2`)* **senza che nessun")
        W("> sigillo se ne accorga**.")
    else:
        W("> ### ✅ **NUDA = CAMPAGNA: il driver accende TUTTE le cure approvate da sé.**")
        W("> **Un solo modo di lanciare**, e nessuna cura si puo' dimenticare *(decisione di")
        W("> Luca, 2026-09-24)*.")
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
