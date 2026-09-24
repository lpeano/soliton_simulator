# -*- coding: utf-8 -*-
"""CURA 1 in codice: la relazione, la voce del registro, D34 -> CURA IN CODICE."""
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


# ---------------------------------------------------------------- RAMIFICAZIONI
P = "doc/RAMIFICAZIONI.md"
t = io.open(P, encoding="utf-8", newline="").read()
A = "\n| **Z130** \U0001f7e5`SOSPETTO RITIRATO, MIO`"
i0 = t.index(A)
riga = t[i0:t.index("\n", i0 + 1)]
Z = ("\n| **Z134** \U0001f7e9`CURA IN CODICE` ⏳`[archivi delle cure · CURA]` | "
     "**`CURA 1` — L'OROLOGIO: `RITMO_WRAP_2PI` APPROVATA e accesa dal driver, `TW_SPINORE` "
     "BLOCCATO. Sigillo `6/6`** (2026-09-24, `csv/_seal_fork/_sig_cura1/REFERTO.txt`) | "
     "**(a) `RITMO_WRAP_2PI`:** fino a oggi era accendibile **solo in-process** — nessuna "
     "opzione da riga di comando — quindi **nessun run poteva accenderla**, e una cura che "
     "nessun run accende **e' un ramo morto**. Aggiunte **tre** cose, non una: l'opzione "
     "`--ritmo-wrap-2pi`, la riga in `_applica_flag`, **e `RITMO_WRAP_2PI` nel `global`** "
     "*(senza, l'assegnamento creerebbe una LOCALE e il flag resterebbe inerte in silenzio: "
     "e' il difetto gia' catalogato di `--tau-a`)*. **Il driver la passa in ogni run.** | "
     "**(b) `TW_SPINORE`:** il simulatore **RIFIUTA DI PARTIRE** se e' acceso, in "
     "`_applica_flag` *(`:7335`)*, col messaggio che **nomina la ragione** e dice **come "
     "riaprirlo** *(«una decisione di Luca, non la rimozione di questa riga»)*. **Il ramo "
     "resta** (par.10: il codice di una legge esclusa e' l'evidenza che spiega perche' esiste "
     "il suo sostituto). **In `_applica_flag` e non nel punto d'uso: li' il rifiuto arriva "
     "PRIMA che la scena nasca, quindi non lascia uno stato parziale sul disco.** | "
     "**IL SIGILLO, `6/6`:** `T1` l'opzione esiste **nel simulatore** e il **driver** la passa "
     "· `T2` dopo `_applica_flag` con l'argv del driver `RITMO_WRAP_2PI = True` · `T3` il "
     "default di `TW_SPINORE` e' `False` · **`T4` IL RIFIUTO SCATTA e NOMINA LA RAGIONE** "
     "*(cercata nel messaggio, non sperata)* · **`T5` e NON scatta senza il flag** — il "
     "controllo che rende `T4` leggibile, perche' un rifiuto che scatta SEMPRE bloccherebbe "
     "ogni run e passerebbe `T4` senza essere un presidio · **`T6` BYTE-INERTE: `206` campi "
     "identici, `0` diversi** contro `_val600`, con `RITMO_WRAP_2PI` **forzato spento** — "
     "isola il presidio dall'effetto VOLUTO di (a). "
     "**Collaudo `5/5` con TRE casi che devono fallire:** un rifiuto sotto un ALTRO flag non "
     "conta; un `if TW_SPINORE` che **non solleva** non e' un rifiuto *(un avviso non basta)*; "
     "un messaggio che **non nomina la ragione** non passa. | "
     "**⚠ ACCENDERE `RITMO_WRAP_2PI` NEL DRIVER NON E' BYTE-INERTE, ED E' IL PUNTO:** e' una "
     "**cura**, non un'opzione. **I numeri presi prima di oggi non si confrontano con quelli di "
     "dopo senza dirlo** (par.9-bis), e lo stato effettivo di ogni run sta in "
     "`CONFIGURAZIONE.txt`. **E `(b)` NON RITIRA NULLA:** `TW_SPINORE` era spento in 9 run su "
     "11 e `--tw-spinore` non compare in nessun lanciatore committato. |")
t = s1(t, riga, riga + Z)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- CODA: D34 -> CURA IN CODICE
P = "doc/STATO_RUN.md"
t = io.open(P, encoding="utf-8", newline="").read()
i0 = t.index("| **D34** |")
fine = t.index("\n", i0)
v = t[i0:fine]
t = t[:i0] + v.replace("| **D34** |", "| **D34** ✅`CURATO IN CODICE il 2026-09-24` |", 1) + \
    (" **LA CURA E' IN CODICE E IL DRIVER LA ACCENDE IN OGNI RUN** *(`--ritmo-wrap-2pi`, "
     "`Z134`, sigillo `6/6`)*. **Approvata da Luca.** Il default nel sorgente resta `False`, "
     "come tutte le cure pre-epoca-3: il braccio di confronto si ottiene **omettendo il "
     "flag**, e `CONFIGURAZIONE.txt` mostra quale dei due e' girato." ) + t[fine:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
N += 1

# ---------------------------------------------------------------- RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉟ **`CURA 1` È IN CODICE: sigillo `6/6`** — l'orologio

> `csv/_seal_fork/_sig_cura1/REFERTO.txt`. **Prima cura che entra in codice con la tua
> approvazione.**

### **(a) `RITMO_WRAP_2PI`: servivano TRE cose, non una**

**Fino a oggi era accendibile solo in-process:** non esisteva nessuna opzione da riga di
comando, quindi **nessun run poteva accenderla**. Una cura che nessun run accende **è un ramo
morto**, e il sigillo lo controlla in `T1`.

| | |
|---|---|
| l'opzione **`--ritmo-wrap-2pi`** | nel simulatore |
| la riga in **`_applica_flag`** | `RITMO_WRAP_2PI = bool(getattr(a, "ritmo_wrap_2pi", False))` |
| **`RITMO_WRAP_2PI` nel `global`** | **senza, l'assegnamento creerebbe una LOCALE e il flag resterebbe inerte in silenzio** — è il difetto già catalogato di `--tau-a` |
| il **driver** lo passa | `csv/_test_fork/_scena_video.py`, in ogni run |

### **(b) `TW_SPINORE`: il simulatore RIFIUTA DI PARTIRE**

Il rifiuto sta in **`_applica_flag`** (`:7335`), **non nel punto d'uso**, e la ragione è
precisa: **lì arriva prima che la scena nasca**, quindi non lascia uno stato parziale sul
disco. Un rifiuto dentro `step()` lo farebbe.

**Il messaggio nomina la ragione** *(il ponte inverso, `:3090-3100`, la scheda ⑧, il referto col
commento falso)* **e dice come riaprirlo:** *«una decisione di Luca, non la rimozione di questa
riga»*. **Il ramo resta** — par.10: il codice di una legge esclusa è l'evidenza che spiega
perché esiste il suo sostituto.

### **Il sigillo, `6/6`, e due test sono il controllo l'uno dell'altro**

| | | |
|---|---|---|
| `T1` | l'opzione esiste **nel simulatore** *e* il **driver** la passa | **PASS** |
| `T2` | dopo `_applica_flag` con l'argv del driver, `RITMO_WRAP_2PI = True` | **PASS** |
| `T3` | il default di `TW_SPINORE` è `False` | **PASS** |
| **`T4`** | **il rifiuto SCATTA** e **nomina la ragione** *(cercata nel messaggio, non sperata)* | **PASS** |
| **`T5`** | **e NON scatta senza il flag** | **PASS** |
| **`T6`** | **BYTE-INERTE: `206` campi identici, `0` diversi** | **PASS** |

**`T5` è quello che rende `T4` leggibile:** un rifiuto che scatta **sempre** bloccherebbe ogni
run e **passerebbe `T4` senza essere un presidio**.

**`T6` isola il presidio dall'effetto VOLUTO di `(a)`:** gira 120 passi con `RITMO_WRAP_2PI`
**forzato spento**, cioè nella configurazione di **prima**, e confronta con `_val600`. **`0`
campi diversi** dice che il rifiuto non ha effetti collaterali.

**Collaudo `5/5`, con TRE casi che devono fallire:** un rifiuto sotto un **altro** flag non
conta; un `if TW_SPINORE` che **non solleva** non è un rifiuto *(un avviso non basta)*; un
messaggio che **non nomina la ragione** non passa.

> ### ⚠ **Accendere `RITMO_WRAP_2PI` nel driver NON è byte-inerte, ed è il punto**
> È una **cura**, non un'opzione. **I numeri presi prima di oggi non si confrontano con quelli
> di dopo senza dirlo** *(par.9-bis)*, e lo stato effettivo di ogni run sta in
> `CONFIGURAZIONE.txt`.
> **E `(b)` non ritira nulla:** `TW_SPINORE` era spento in **9 run su 11** e `--tw-spinore` non
> compare in nessun lanciatore committato.
"""
assert "`CURA 1` È IN CODICE" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. Z134, D34 curato, relazione." % N)
