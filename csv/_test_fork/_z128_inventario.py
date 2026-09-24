# -*- coding: utf-8 -*-
"""INVENTARIO + README per il referto di configurazione (5-novies), col blob letto dal disco."""
import hashlib
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

N = 0


def s1(t, v, nu):
    global N
    assert t.count(v) == 1, "occ=%d per %r" % (t.count(v), v[:70])
    N += 1
    return t.replace(v, nu)


def blob(p):
    """sha1 dei BYTE GREZZI, letto DAL DISCO -- non `git hash-object` (C18)."""
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()[:8]


B_CFG = blob("csv/_configurazione.py")
B_DRV = blob("csv/_test_fork/_scena_video.py")
B_G4 = blob("csv/_test_fork/_g4_prova.py")
B_TE = blob("csv/_test_fork/_f2p_test_E.py")

# ---------------------------------------------------------------- INVENTARIO
P = "doc/INVENTARIO_strumenti.md"
t = io.open(P, encoding="utf-8", newline="").read()
anc = "| `csv/_test_fork/_g4_prova.py` | `b9642633` |"
i0 = t.index(anc)
riga = t[i0:t.index("\n", i0)]
VOCI = (
    "\n| **`csv/_configurazione.py`** | **`%s`** | `python csv/_configurazione.py` "
    "*(il COLLAUDO; il referto lo scrive il driver, non si invoca a mano)* | "
    "**IL REFERTO DI CONFIGURAZIONE DI UN RUN.** Scrive `CONFIGURAZIONE.txt` e `.json` nella "
    "cartella del run: **lo stato EFFETTIVO di tutti i flag di modulo, letto DAL MODULO dopo "
    "`_applica_flag`**, i due argv **VERBATIM** *(quello del processo e quello passato al "
    "simulatore, che NON sono lo stesso)*, `sha1` dei **byte grezzi** di simulatore e driver, "
    "seme, `HEAD` e se l'albero e' pulito. **I nomi vengono dall'AST** *(assegnamenti di "
    "MODULO con nome MAIUSCOLO: `123` trovati)*, **non da una lista a mano** -- nel driver ce "
    "n'era una di `24`. **Il driver RIFIUTA DI PARTIRE se non riesce a scriverlo.** "
    "**Collaudo `6/6`, con DUE casi che devono fallire** *(`K3`: letto PRIMA di "
    "`_applica_flag` darebbe il DEFAULT; `K5`: una `dest` inesistente deve SOLLEVARE)*, "
    "**piu' `K6`, che verifica DALL'AST che nel driver `scrivi()` venga DOPO "
    "`_applica_flag`** -- e `K6` ha davvero FALLITO prima che il cablaggio esistesse. | "
    "`<cartella del run>/CONFIGURAZIONE.txt` · `.json` |"
    % B_CFG)
VOCI2 = (
    "\n| **`csv/_test_fork/_f2p_test_E.py`** | **`%s`** | "
    "`python csv/_test_fork/_f2p_test_E.py _f2p_corto` *(l'argomento e' la cartella del "
    "braccio della cura; senza, usa `_f2p_prova`)* | "
    "**I TEST `E1`-`E4` DELLA CURA `FASE_2PI`, coi criteri fissati PRIMA.** `E1` ed `E2` sono "
    "di **Luca**; **`E3` ed `E4` sono MIEI, derivati e marcati come tali** *(`Z125`: il §E non "
    "esisteva oltre `E1`/`E2`)*. **`E2` e' dichiarato NON MISURABILE** *(l'annichilazione vive "
    "solo dentro `ANTIFASE_ADD = False`)*. **Collaudo `6/6`, con TRE casi che devono "
    "fallire.** **SOLA LETTURA su snapshot gia' scritti.** | "
    "`csv/_test_fork/_f2p_corto_TEST_E.txt` · `_f2p_CONTROLLO_involucro.txt` |"
    % B_TE)
# UNA sola sostituzione con entrambe le voci: la prima stesura ne faceva due, e la seconda
# non attaccava perche' la PRIMA aveva gia' cambiato l'ancora. L'`assert` di P1-quater l'ha
# presa; un `assert` globale l'avrebbe lasciata passare.
t = s1(t, riga, riga + VOCI + VOCI2)
# e il blob dello strumento TOCCATO va aggiornato, non lasciato stale
t = s1(t, "| `csv/_test_fork/_g4_prova.py` | `b9642633` |",
        "| `csv/_test_fork/_g4_prova.py` | **`%s`** *(era `b9642633`: aggiunti i modi "
        "`--fase-2pi` e `--fase-2pi-corto`)* |" % B_G4)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- README
P = "README.md"
t = io.open(P, encoding="utf-8", newline="").read()
V = "## 5. Varianti Velocity-Verlet"
NU = u"""## 4-bis. Il referto di configurazione dei run — **nessun run parte senza**

*(decisione di Luca, 2026-09-24)*

Ogni run lanciato attraverso `csv/_test_fork/_scena_video.py` scrive nella **cartella del
run** due file:

| file | contenuto |
|---|---|
| **`CONFIGURAZIONE.txt`** | leggibile: i flag che l'argv ha **cambiato** rispetto al default, poi **tutti** i flag e le costanti di modulo |
| **`CONFIGURAZIONE.json`** | gli stessi dati, per gli strumenti |

**Cosa contiene**, e ogni voce c'e' per un motivo:

- **lo stato EFFETTIVO di tutti i flag di modulo, letto DAL MODULO dopo `_applica_flag`** —
  non il default scritto nel sorgente. **Sono due cose diverse:** `SPINORE_CORRETTO` ha
  default `False` e vale `True` in ogni run del fork, perche' il driver cabla
  `--spinore-corretto`. Chi legge il sorgente conclude il contrario di chi legge il run;
- **i due argv VERBATIM**, che **non sono lo stesso**: quello con cui e' stato invocato il
  processo, e quello passato al simulatore dopo che il driver ha tolto le proprie opzioni;
- **`sha1` dei byte grezzi** di simulatore e driver *(**non** `git hash-object`: trappola
  CRLF)*, il **seme**, `HEAD`, e **se l'albero di git e' pulito**.

**L'elenco dei flag non e' scritto a mano: viene dall'AST** — gli assegnamenti a livello di
modulo con nome maiuscolo, **`123`** al momento in cui scrivo. La lista a mano che il driver
stampava a video ne aveva **`24`**, e una lista a mano invecchia in silenzio.

> **DEFAULT: sempre attivo, e non si spegne.** Il driver **rifiuta di partire** se non riesce
> a scrivere il referto. **Non e' byte-inerte sulla fisica** perche' non tocca la fisica:
> legge il modulo e scrive due file. **Nessun flag**, per la stessa ragione per cui non ce
> l'hanno le correzioni di difetto (par.10): non e' una legge, e' un presidio.

**Il collaudo si gira da solo:** `python csv/_configurazione.py` — **`6/6`**, con due casi che
**devono** fallire e un terzo, `K6`, che verifica **dall'AST** che nel driver la scrittura
venga **dopo** `_applica_flag`. *(Letta prima, la tabella mostrerebbe i default: esattamente
la bugia che il referto esiste per impedire. E `K6` ha davvero fallito finche' il cablaggio
non c'era.)*

## 5. Varianti Velocity-Verlet"""
t = s1(t, V, NU)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

print("%d sostituzioni. blob: _configurazione %s, _scena_video %s, _g4_prova %s, _f2p_test_E %s"
      % (N, B_CFG, B_DRV, B_G4, B_TE))
