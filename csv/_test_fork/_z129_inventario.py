# -*- coding: utf-8 -*-
"""Punto 2: INVENTARIO + relazione della ricostruzione."""
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


B = hashlib.sha1(io.open("csv/_test_fork/_ricostruisci_config.py", "rb").read()).hexdigest()[:8]

# ---------------------------------------------------------------- INVENTARIO
P = "doc/INVENTARIO_strumenti.md"
t = io.open(P, encoding="utf-8", newline="").read()
anc = "| **`csv/_configurazione.py`** |"
i0 = t.index(anc)
riga = t[i0:t.index("\n", i0)]
VOCE = (
    "\n| **`csv/_test_fork/_ricostruisci_config.py`** | **`%s`** | "
    "`python csv/_test_fork/_ricostruisci_config.py` | "
    "**LA RICOSTRUZIONE DELLA CONFIGURAZIONE DEI RUN GIA' FATTI**, tabella **generata** "
    "flag × run su **11 campagne** *(`G1`, `G2`, validazione 600, `G3` ×2, `G4` ×3, `G4-bis`, "
    "`D34`, `FASE_2PI` corto)*. **Tre fonti, e ogni cella porta la SUA:** l'**argv** dal "
    "driver committato a quel commit · il **banner** del log *(stato EFFETTIVO dal modulo, ma "
    "sono 24 flag su 123)* · il **default del blob di quel run** *(`git cat-file -p "
    "<commit>:soliton_simulator.py`)*, **valido solo se nessuna opzione lo cambia -- e questo "
    "si VERIFICA**, ricavando dall'AST di `_applica_flag` l'opzione che scrive quel flag e "
    "cercandola nei lanciatori committati. **Il commit di ogni run viene DALLO SNAPSHOT**, non "
    "dal log. **Le contraddizioni fra fonti si riportano ENTRAMBE**, e quelle che nessuna "
    "opzione spiega sono marcate `*** NON SPIEGATA ***`. **Cio' che non si ricostruisce e' "
    "`NON RICOSTRUITO`, col motivo.** **SOLA LETTURA.** | "
    "`csv/_test_fork/_RICOSTRUZIONE_config.txt` |" % B)
t = s1(t, riga, riga + VOCE)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉗ **La ricostruzione dei run già fatti: tabella generata flag × run** *(punto 2)*

> `csv/_test_fork/_ricostruisci_config.py` — **sola lettura**, `csv/_test_fork/_RICOSTRUZIONE_config.txt`.
> **11 campagne**, tre fonti, **ogni cella porta la sua**.

**La provenienza, e il `commit` viene DALLO SNAPSHOT** *(il timbro che il run si è messo da
solo)*, **non dal log**:

| campagna | commit | banner | modo |
|---|---|--:|---|
| `G1` video 6000 | `94e2ec07` | 15 flag | — |
| `G2` g2m | `2b0a19f9` | 15 flag | — |
| validazione 600 | `691b7e99` | **nessuno** | — |
| `G3` controllo | **NON RIC.** | 24 flag | `--controllo` |
| `G3` senza bifase | `abc5b49f` | 24 flag | `--prova` |
| `G4` controllo | **NON RIC.** | 24 flag | `--controllo` |
| `G4` riferimento | `bc30e626` | 24 flag | `--riferimento` |
| `G4` spegni | `49a4cb2e` | 24 flag | `--spegni` |
| `G4-bis` | `26c4165c` | 24 flag | `--spegni-tutto` |
| `D34` ritmo-wrap | `8ec9e248` | 24 flag | `--ritmo-wrap` |
| `FASE_2PI` corto | `b5e9a9ac` | 24 flag | `--fase-2pi-corto` |

**La corrispondenza campagna ↔ cartella è la sola cosa scritta a mano**, perché non è
derivabile — **e si verifica** contro la riga `modo --...` che il log stampa da sé. Le due
`NON RIC.` sono i due *controllo*, che **non lasciano snapshot** *(il `G4 controllo` cancella i
suoi `.pkl.gz` a ogni giro: è scratch)*.

**Il banner è la fonte più forte ma copre `24` flag su `123`**, ed è una **lista a mano** nel
driver, cresciuta nel tempo: per questo `G1`/`G2` ne hanno **15** e non 24.

**Per i flag fuori dal banner la ricostruzione è verificata, non assunta:** si ricava
**dall'AST di `_applica_flag`** l'opzione che scrive quel flag, e si cerca nei **lanciatori
committati a quel commit**. Se non c'è, il default vale — e il referto lo scrive.

### **Due difetti dello strumento, trovati dal suo stesso output**

**① Il glob cercava solo `scena_*.pkl.gz`.** `G1` e `G2` scrivono **`frame_*.pkl`** — senza
gzip, altro nome — e lo strumento li dava per **NON RICOSTRUITI**: **una lacuna dello
STRUMENTO letta come lacuna del DATO.** Corretto, e ora hanno il loro commit.

**② Una contraddizione restava `*** NON SPIEGATA ***`:** `CALORE_VETTORIALE`, banner `False`
contro default `True`. Cercavo l'opzione nel **valore assegnato**, ma lì c'è
`CALORE_VETTORIALE = False`, un **letterale**, dentro `if getattr(a, "calore_scal", False):`.
**L'opzione sta nella CONDIZIONE, non nel valore.** Ora si guardano entrambe, e **le
contraddizioni non spiegate sono zero**.

> **Vale la pena dirlo così: lo strumento stava segnalando come reperto un difetto PROPRIO.**
> È la ragione per cui *«non spiegata»* deve essere una **riga stampata** e non un silenzio.
"""
assert "La ricostruzione dei run già fatti" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. blob dello strumento: %s" % (N, B))
