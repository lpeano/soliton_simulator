# -*- coding: utf-8 -*-
"""I criteri di E1-E4 fissati PRIMA del run, + S10, + il riscontro su E2/S06."""
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


# ---------------------------------------------------------------- REGISTRO: i criteri
P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()
V = ("3. **L'argomento della soglia vale per una differenza ISTANTANEA, ma `tw` è un ACCUMULO "
     "che\n   decade.** **È la crepa dichiarata da Luca stesso**, e `E1` è il suo giudice.")
NU = V + u"""

## I CRITERI DEI TEST, **fissati PRIMA di girare** *(par.5-septies)*

> **⚠ CHI HA SCRITTO QUALE TEST, e va detto perché due sono MIEI — è `Z125`.**
> Nel repo esistevano **solo `E1` ed `E2`**, e ho citato *«i quattro test `E1`-`E4`»* **undici
> volte** senza che `E3` ed `E4` fossero scritti da nessuna parte. **`E1` ed `E2` sono di Luca
> e non si toccano; `E3` ed `E4` li DERIVO, e Luca può sostituirli.**
> Lo strumento è **`csv/_test_fork/_f2p_test_E.py`**, e i criteri stanno **nel suo codice**,
> non solo qui *(`P1-ter`)*.

| test | di chi | criterio | **origine della soglia** |
|---|:--:|---|---|
| **`E1a`** la mitosi non muore | **Luca** | `_g_nati_mitosi > 0` e `n` cresce | il nullo: se la cura rompesse `fm`, le nascite sarebbero `0` |
| **`E1b`** la mitosi non esplode | **Luca** | `n` finale **< 10×** il riferimento, e il run **arriva** a 600 passi | **MISURATA: `178` archi per nodo** *(`526672 / 2959`)*. `10× n` = `~5.3M` archi = `10×` memoria e tempo: **oltre, il sistema non è simulabile, e QUELLA è l'esplosione**. **`MAX_NODI = 4000000` non serve: è una guardia di memoria, non di fisica** |
| **`E1c`** il **fattore** | *mio* | le nascite salgono di un fattore **fra `5×` e `100×`** | **DERIVATA dagli archi GIÀ SUL DISCO**: la campana ha il picco a `|tw| = soglia`, e la finestra **nuova** *(`tau` `2.0`-`2.5`)* contiene **`17113`** archi contro i **`346`** della vecchia *(`tau` `2.5`-`3.0`)* al passo 600 — **`49.46×`**. La banda è **un ordine per lato** perché la **larghezza** della campana non entra nel conto e **la mitosi CONSUMA la torsione** *(retroazione che smorza)*. **Questo test giudica ME, non la cura** |
| **`E2`** le coppie annichilano | **Luca** | **NON MISURABILE**, e si dichiara | vedi il blocco qui sotto |
| **`E3`** la finestra di `D33` | *mio* | si riporta la **popolazione** delle due finestre nei due bracci | il §E **stesso** dice *«non è una cura di `D33`, è un effetto, e va misurato»*. **Si RIPORTA, non si giudica** |
| **`E4`** i diagnostici di fase | *mio* | `max(φ) < 2π` nel braccio della cura | la **riserva ② di `Z120`**. **Il nullo è il sigillo:** a flag spento `max(φ) = 12.565546` |

### ❌ **`E2` NON È MISURABILE IN QUESTO RUN, e lo dichiaro invece di riportare uno zero**

**L'ANNICHILAZIONE VIVE SOLO DENTRO `ANTIFASE_ADD` (`:5351`), CHE È `False`.**
Il ramo che la cura tocca — **`:5499`** — è la **creazione di coppia alla Schwinger**, e lì
l'antifase decide se l'antiparticella è **DISTINGUIBILE** dalla particella nel campo: che è la
**precondizione** dell'annichilazione, **non l'annichilazione**.

**Riportare uno zero sarebbe leggere un'ASSENZA DI MECCANISMO come un'assenza di effetto** —
lo stesso errore del `max|A-B| = 0.000e+00` per **mancanza di confronto**.

**COSA SI MISURA AL SUO POSTO**, e il valore atteso **non è scelto**, è `|exp(i s) − 1|`:

| | `max|exp(i·anti) − exp(i·part)|` |
|---|--:|
| **spenta** — `+2π` su dominio `4π` | **`2.156e-15`** → **identica**: è `D35` |
| **accesa** — `+π` su dominio `2π` | **`2.000000`** → **opposta** |

> ### ⚠ **E LA CONSEGUENZA PER `S06` È PIÙ FORTE DELLA DOMANDA DI PARTENZA**
> Il «muro dell'1 %» **non si spiega con `D35` da solo**: il meccanismo che annichilerebbe
> **non gira**. **`S06` non si chiude con questa cura**, e per misurarlo servirebbe accendere
> `ANTIFASE_ADD` — che è un **ESPERIMENTO** *(par.10)*, **non fisica**, e va **chiesto a Luca**
> invece che deciso qui.

### ✅ **IL CONTROLLO DELL'INVOLUCRO È STATO FATTO PRIMA** *(`STANDARD ⑤`)*

Lo strumento puntato sul **riferimento CONTRO SE STESSO** dà **`2/4`**: `E1a` e `E1b`
**passano**, **`E1c` e `E4` NON passano** — perché il braccio della «cura» *è* il riferimento.
**I criteri non sono vuoti.** → `csv/_test_fork/_f2p_CONTROLLO_involucro.txt`

**E il controllo ha trovato un difetto prima del run:** `n` **non è una chiave** dello snapshot
*(si legge da `len(phi)`)*, e lo strumento si schiantava con `KeyError: 'n'`. **Su un run vero
lo schianto sarebbe arrivato dopo quaranta minuti.**"""
t = s1(t, V, NU)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- CODA: S10
P = "doc/STATO_RUN.md"
t = io.open(P, encoding="utf-8", newline="").read()
i0 = t.index("| **S09** |")
fine = t.index("\n", i0)
S10 = ("\n| **S10** | **Il tetto `1.414213` di `r` che ho citato in `Z117` e `Z123` viene da un "
       "ramo di `ritmo()` che NON GIRA** | leggere quale ramo di `ritmo()` restituisce il `r` "
       "che la fisica usa davvero, **contando le invocazioni dei due rami** *(i contatori di "
       "`A8` ci sono gia')*, e rileggere `Z117`/`Z123` con la risposta | **in attesa** — "
       "`TEMPO_SEGNO` e' **acceso** e `_g_temposegno_tot = 600`, quindi il ramo vivo e' "
       "**`r = 1 + mean|tw|/PHI_CRIT`**, che **non ha** il tetto `1.4142` della formula a "
       "bottleneck *(`x/sqrt(1+x^2)` normalizzata)*. **Misurato sul riferimento: `r` medio "
       "`1.3545`-`1.3689`, nessun tetto e nessun pavimento toccato.** **Non dico che `Z117`/"
       "`Z123` siano sbagliati: dico che NON SO da dove venga quel numero, e finche' non lo so "
       "non lo cito come se lo sapessi** |")
t = t[:fine] + S10 + t[fine:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
N += 1

# ---------------------------------------------------------------- RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉓ **I criteri di `E1`-`E4`, fissati PRIMA di girare — e `E2` non è misurabile**

> **Committati prima del run**, come par.5-septies chiede: il commit dei criteri deve essere
> **antenato** del commit del run. Strumento: `csv/_test_fork/_f2p_test_E.py`.

**`E1` ed `E2` sono tuoi. `E3` ed `E4` sono miei, derivati** *(è `Z125`)*, **e puoi
sostituirli.**

| test | criterio | **origine**, che non è una scelta |
|---|---|---|
| **`E1a`** | nascite `> 0`, `n` cresce | il nullo: se la cura rompesse `fm`, sarebbero `0` |
| **`E1b`** | `n` finale **< 10×** il riferimento | **`178` archi per nodo misurati** *(`526672/2959`)*: `10× n` ≈ `5.3M` archi = `10×` memoria e tempo, **e quella è l'esplosione**. `MAX_NODI = 4000000` non serve, è memoria non fisica |
| **`E1c`** | fattore fra **`5×`** e **`100×`** | **derivato dagli archi già sul disco: `49.46×`** |
| **`E3`** | si **riporta** la popolazione delle finestre | il §E dice *«è un effetto, va misurato»* |
| **`E4`** | `max(φ) < 2π` | il nullo è il sigillo: spento `12.565546` |

**Da dove viene il `49.46×`, ed è una previsione vera, non un'aspettativa:** la campana della
mitosi ha il **picco a `|tw| = soglia`** e si azzera al tetto `4π`. Abbassando la soglia da
`3π` a `2π`, la finestra che la campana copre passa da **`346` archi** *(`tau` `2.5`-`3.0`)* a
**`17113`** *(`tau` `2.0`-`2.5`)*, al passo 600 del riferimento. **La banda è un ordine per
lato** perché la larghezza della campana non entra nel conto **e la mitosi consuma la
torsione**. **`E1c` giudica me, non la cura.**

### ❌ **`E2` NON È MISURABILE, e non riporto uno zero al suo posto**

**L'annichilazione vive SOLO dentro `ANTIFASE_ADD` (`:5351`), che è `False`.** Il ramo che la
cura tocca — `:5499` — è la **creazione di coppia alla Schwinger**, dove l'antifase decide se
l'antiparticella è **distinguibile** dalla particella nel campo. **Precondizione, non
annichilazione.**

Quello che si misura, e il `2` **non è scelto** *(è `|exp(iπ) − 1|`)*:
**spenta `+2π` su `4π` → `2.156e-15`** *(identica: è `D35`)* · **accesa `+π` su `2π` →
`2.000000`** *(opposta)*.

> **⚠ E LA CONSEGUENZA PER `S06` È PIÙ FORTE DELLA DOMANDA:** il «muro dell'1 %» **non si
> spiega con `D35` da solo**, perché **il meccanismo che annichilerebbe non gira**.
> **`S06` non si chiude con questa cura.** Per misurarlo servirebbe accendere `ANTIFASE_ADD`,
> che è un **esperimento** *(par.10)*, non fisica: **te lo chiedo, non lo decido.**

### ㉔ **`S10`: il tetto `1.414213` di `r` viene da un ramo che non gira**

Cercando il gauge per `E4` ho letto `ritmo()`: **`TEMPO_SEGNO` è acceso** e
`_g_temposegno_tot = 600`, quindi il ramo vivo è **`r = 1 + mean|tw|/PHI_CRIT`** — che **non
ha** il tetto `1.4142`, perché quel tetto è della formula a bottleneck `x/√(1+x²)` **dell'altro
ramo**.

**Misurato sul riferimento:** `r` medio **`1.3545`–`1.3689`**, **nessun tetto e nessun
pavimento toccato**.

> **Non dico che `Z117` e `Z123` siano sbagliati: dico che NON SO da dove venga quel numero, e
> finché non lo so non lo cito come se lo sapessi.** → **`S10`**, coi contatori di `A8` già
> disponibili per rispondere. **E `E4` non è costruito su quel gauge**, appunto.

### ✅ **E il controllo dell'involucro ha trovato un difetto PRIMA del run**

Lo strumento puntato sul **riferimento contro se stesso** dà **`2/4`**: `E1a`/`E1b` passano,
**`E1c` e `E4` NON passano**, perché il braccio della «cura» *è* il riferimento. **I criteri non
sono vuoti.**

E nel farlo si è schiantato con **`KeyError: 'n'`**: `n` **non è una chiave** dello snapshot,
il numero di nodi si legge da `len(phi)`. **Su un run vero lo schianto sarebbe arrivato dopo
quaranta minuti** — ed è esattamente ciò per cui `STANDARD ⑤` esiste.
"""
assert "i criteri di `E1`-`E4`, fissati PRIMA" not in t.lower()
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. Criteri nel registro, S10 in coda, relazione." % N)
