# -*- coding: utf-8 -*-
"""Z124: il sigillo di FASE_2PI, 6/6 -- e il BUCO del paragrafo E, dichiarato."""
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


# ------------------------------------------------------------------ RAMIFICAZIONI
P = "doc/RAMIFICAZIONI.md"
t = io.open(P, encoding="utf-8", newline="").read()
A = "\n| **Z123** \U0001f7e9`CHIUSA PER MISURA`"
i0 = t.index(A)
riga = t[i0:t.index("\n", i0 + 1)]
Z = ("\n| **Z124** \U0001f7e9`CHIUSA PER MISURA` ⏳`[archivi delle cure · SIGILLO]` | "
     "**IL SIGILLO DI `FASE_2PI`: `6/6` PASS, e il criterio che lo rende leggibile e' `T6`** "
     "(2026-09-22, finito alle 20:57; simulatore blob `445e2896`, due run da 120 passi, "
     "`348.2 s` + `331.5 s`; `csv/_seal_fork/_sig_fase_2pi/REFERTO.txt`) | "
     "**I SEI TEST:** "
     "**`T1`** il default e' **SPENTO**, letto dal sorgente · "
     "**`T2`** GATE dall'AST: **3 rami**, tutti in `_dphi` / `_wphi` / `mitosi` — e le altre "
     "21 sostituzioni **non sono ramificazioni**: passano da `_dphi()`/`_wphi()`, **un solo "
     "punto da cui tutti prendono il periodo** · "
     "**`T3`** **BYTE-INERTE spento: 206 campi identici, 0 diversi** · "
     "**`T4`** controllo positivo: acceso **103 campi diversi**, `n` `2461` → `2647` · "
     "**`T5`** il dominio e' davvero cambiato: acceso `max(phi) = 6.282066 < 2π = 6.283185` · "
     "**`T6`** **e spento NON lo e': `max(phi) = 12.565546`, SOPRA `2π`** | "
     "**`T6` E' IL TEST CHE RENDE `T5` LEGGIBILE, e senza di lui `T5` sarebbe vuoto:** se anche "
     "a flag spento `phi` stesse sotto `2π`, `T5` **passerebbe senza che il flag abbia fatto "
     "nulla**. E' `P1-sexies` applicato dentro il sigillo invece che solo al collaudo. "
     "**E I COLLAUDI SONO SEI, con DUE casi che devono fallire:** `K2` — `_w4` sulle stesse "
     "differenze e' **l'IDENTITA'** (`max|w4(a) - a| = 0.000e+00`), cioe' **il difetto `D34` e' "
     "riprodotto**; `K5` — **`+2π` su un dominio `2π` e' un'IDENTITA'** "
     "(`max|diff| = 8.882e-16`), **ed e' esattamente `D35`: il motivo per cui `+2π` NON e' "
     "un'antifase**. `K3` e' l'obbligo **(a)** del cor.7 di `A11`: lontano dal taglio i due "
     "coincidono a `8.882e-16`. | "
     "**⚠ E IL SIGILLO NON DICE CHE LA CURA SIA GIUSTA: dice che fa CIO' CHE DICHIARA.** "
     "Se `φ` debba vivere su `2π` lo decidono i test `E1`-`E4`, **e se uno fallisce la "
     "lettura CADE**. **Il default resta SPENTO.** "
     "**⚠ E UN BUCO MIO, trovato rileggendo dal disco: il §E non esiste nel repo oltre `E1` "
     "ed `E2`** — vedi `Z125`. |")
t = s1(t, riga, riga + Z)

# --- Z125: il buco del paragrafo E
Z2 = ("\n| **Z125** \U0001f7e5`DIFETTO DI METODO, MIO` ⏳`[archivi delle cure · LETTURA]` | "
      "**IL §E NON ESISTE NEL REPO OLTRE `E1` ED `E2`: ho citato «i quattro test `E1`-`E4`» "
      "undici volte senza che `E3` ed `E4` fossero scritti da nessuna parte** (2026-09-24, "
      "verificato dal disco e **dal transcript**, non a memoria) | "
      "**COSA C'E' DAVVERO**, in `doc/REGISTRO_FISICA.md` sotto *«LE DOMANDE APERTE»*: "
      "**`E1`** *(la mitosi a `2π` funziona senza tarature?)* · **`E2`** *(le coppie "
      "annichilano?)* · e un **terzo punto che NON e' un test**, ma la crepa dichiarata da Luca "
      "*(l'argomento della soglia vale per una differenza ISTANTANEA, mentre `tw` e' un ACCUMULO "
      "che decade — e il suo giudice e' `E1`)*. **`E3` ed `E4` NON CI SONO:** cercati nei "
      "messaggi di Luca, nei miei, in `doc/` e in `RELAZIONE_PER_CLAUDE.md`. "
      "**E la mia frase in `RELAZIONE_PER_CLAUDE.md` — *«E3 `r` non tocca piu' il clip, `E4` "
      "lo spegnimento di `SPINORE_VIVO` conta»* — e' una RICOSTRUZIONE che non ho potuto "
      "verificare da nessuna fonte.** | "
      "**PERCHE' E' UN DIFETTO E NON UN'OMISSIONE:** « i quattro test » era diventato un "
      "**nome**, e un nome si trasporta senza riaprirlo — e' **`P1` esatto** "
      "*(l'associazione genera candidati, non conclusioni)*, sul mio stesso testo. **E la "
      "CODA lo aggravava:** la voce dell'**epoca 3** si chiama anch'essa **`E3`**, quindi "
      "`E3` denota **due cose diverse** nello stesso documento. | "
      "**COSA FACCIO, e lo dichiaro invece di inventare le parole di Luca:** i due test "
      "**`E1` ed `E2` sono di Luca e restano tali**; **`E3` ed `E4` li DERIVO da cio' che e' "
      "committato** — `E3` dall'effetto che il §E stesso dichiara *«va misurato»* (la "
      "finestra d'inversione di `D33` che si allarga da mezzo `π` a un `π` intero) e `E4` "
      "dalla riserva ② di `Z120` (i diagnostici di fase cambiano, e con essi il gauge di "
      "`S09`). **Sono MIEI, marcati come tali nel registro, e Luca puo' sostituirli.** "
      "**I criteri si fissano PRIMA di girare** *(par.5-septies)*. "
      "**E i test si rinumerano `E1`-`E4` → `Q1`-`Q4`? NO: si tiene `E1`/`E2` (sono di Luca) "
      "e si dichiara la collisione con la voce `E3` della coda.** |")
t = s1(t, riga + Z, riga + Z + Z2)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ------------------------------------------------------------------ RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉑ **Il sigillo di `FASE_2PI`: `6/6` PASS — e `T6` è il test che rende `T5` leggibile**

> Finito alle **20:57** del 22/9. Blob **`445e2896`**, due run da 120 passi
> *(`348.2 s` + `331.5 s`)*. Referto: `csv/_seal_fork/_sig_fase_2pi/REFERTO.txt`.

| | test | esito |
|---|---|---|
| `T1` | il default è spento, letto dal sorgente | **PASS** `FASE_2PI = False` |
| `T2` | GATE dall'AST | **PASS** `3` rami, tutti in `_dphi` / `_wphi` / `mitosi` |
| `T3` | byte-inerzia a flag spento | **PASS** **`206` campi identici, `0` diversi** |
| `T4` | controllo positivo | **PASS** `103` campi diversi, `n` `2461` → `2647` |
| `T5` | il dominio è cambiato | **PASS** acceso `max(φ) = 6.282066 < 2π` |
| `T6` | **e spento NON lo è** | **PASS** `max(φ) = 12.565546`, **sopra `2π`** |

**`T2` merita una riga**, perché il numero *`3` rami* per **21 sostituzioni** sembra un errore e
non lo è: le altre **non sono ramificazioni**. Passano da **`_dphi()`** e **`_wphi()`**, che
sono **un solo punto da cui tutti prendono il periodo** — ed è il motivo per cui il flag è
stato scritto così invece che con venti `if`.

**`T6` è il test che conta più di `T5`:** se anche a flag **spento** `φ` stesse sotto `2π`,
allora `T5` **passerebbe senza che il flag abbia fatto nulla**. È `P1-sexies` portato **dentro**
il sigillo, non solo nel collaudo.

**E i collaudi sono `6`, con DUE casi che devono fallire, e sono i due difetti:**
`K2` — `_w4` sulle stesse differenze è **l'identità** *(`max|w4(a) − a| = 0.000e+00`)*: **`D34`
riprodotto**. `K5` — **`+2π` su un dominio `2π` è un'identità** *(`8.882e-16`)*: **è `D35`**,
il motivo per cui `+2π` non è un'antifase. `K3` è l'obbligo **(a)** del cor.7 di `A11`.

> **⚠ Il sigillo non dice che la cura sia giusta: dice che fa ciò che dichiara.**
> Se `φ` debba vivere su `2π` lo decidono i test, e **se uno fallisce la lettura cade**.
> **Il default resta SPENTO.**

### ㉒ **UN BUCO MIO: il §E non esiste nel repo oltre `E1` ed `E2`**

> **Trovato rileggendo dal disco prima di girare la prova**, non a memoria — e **verificato
> anche sul transcript**, non solo sui documenti.

Ho scritto *«i quattro test `E1`-`E4`»* **undici volte**. Nel repo ci sono **due** test, in
`doc/REGISTRO_FISICA.md` sotto *«LE DOMANDE APERTE»*:

- **`E1`** — *la mitosi a `2π` funziona senza tarature?* Se fallisce **cade il punto 2 del §D**;
- **`E2`** — *le coppie annichilano?* Se resta `~0` con `+π`, **cade il punto 5** e `S06` perde
  la spiegazione che sembra avere;
- e un **terzo punto che non è un test**: la crepa che hai dichiarato tu stesso — *l'argomento
  della soglia vale per una differenza **istantanea**, mentre `tw` è un **accumulo** che decade*
  — e il suo giudice è `E1`.

**`E3` ed `E4` non ci sono.** Cercati nei tuoi messaggi, nei miei, in `doc/`, in questa
relazione. **E la frase che ho scritto io — *«`E3` `r` non tocca più il clip, `E4` lo
spegnimento di `SPINORE_VIVO` conta»* — è una ricostruzione che non ho potuto verificare da
nessuna fonte.**

**Perché è un difetto di metodo e non una dimenticanza:** *«i quattro test»* era diventato un
**nome**, e un nome si trasporta senza riaprirlo. È **`P1` esatto**, applicato al mio stesso
testo. **E la coda lo aggravava:** la voce dell'**epoca 3** si chiama anche lei **`E3`**.

**Cosa faccio, e lo dichiaro invece di inventare le tue parole:** `E1` ed `E2` **sono tuoi e
restano tuoi**; `E3` ed `E4` **li derivo da ciò che è committato**, e li marco come **miei** nel
registro:

- **`E3`** — dall'effetto che il §E **stesso** dichiara *«va misurato»*: con `φ` su `2π` la
  soglia della mitosi passa a `2π`, quindi `tau_soglia` da `2.5` a `2`, `centro` da `2.75` a
  `2.5`, e **l'inversione da `3.5π` a `3π`**: **la finestra di `D33` si allarga da mezzo `π` a
  un `π` intero**;
- **`E4`** — dalla riserva ② di `Z120`: **i diagnostici di fase cambiano per costruzione**, e
  fra loro c'è **il gauge `median(|f|)` di `S09`**, il sospetto aperto ieri.

**Puoi sostituirli**: sono derivati, non tuoi. **I criteri li fisso PRIMA di girare**
*(par.5-septies)*, nel commit che precede il run.
"""
assert "il §E non esiste nel repo" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. Z124 (sigillo 6/6), Z125 (il buco del paragrafo E)." % N)
