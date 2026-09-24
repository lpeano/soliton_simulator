# -*- coding: utf-8 -*-
"""(1c) RITIRO di S10, col reperto. E S11, il sospetto nuovo che ne emerge."""
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


# ---------------------------------------------------------------- CODA: S10 ritirata, S11 nuovo
P = "doc/STATO_RUN.md"
t = io.open(P, encoding="utf-8", newline="").read()
i0 = t.index("| **S10** |")
fine = t.index("\n", i0)
vecchia = t[i0:fine]
NUOVA = (
    "| **S10** ❌**RITIRATA il 2026-09-24** | ~~Il tetto `1.414213` di `r` viene da un ramo di "
    "`ritmo()` che NON GIRA~~ | — | **RITIRATA, e la premessa era sbagliata DUE VOLTE.** "
    "**① `_g_temposegno_tot` sale a `:4406`, PRIMA del controllo `if TEMPO_SEGNO`, e in una "
    "FUNZIONE DIVERSA da `ritmo()`**: conta le INVOCAZIONI, non il ramo attivo, e **varrebbe "
    "`600` comunque**. **② `TEMPO_SEGNO` e' `False` in TUTTI i run ricostruibili** *(9 su 11, "
    "`--tempo-segno` assente da ogni lanciatore committato)*, **quindi il ramo che chiamavo "
    "«vivo» e' MORTO e quello che chiamavo «morto» e' VIVO.** **Il tetto `1.414213` E' del ramo "
    "che gira, e `Z117`/`Z123` lo citavano CORRETTAMENTE.** → `Z130` |")
t = t[:i0] + NUOVA + t[fine:]

i1 = t.index("| **S10** ")
f1 = t.index("\n", i1)
S11 = ("\n| **S11** | **`r` E' SATURO AL SUO TETTO PER UN TERZO DEI NODI, e la quota CRESCE: "
       "`0.76 %` -> `29.57 %` in 600 passi** *(`A11` cor.6: un limite che satura e' un "
       "allarme)* | rimisurare la quota al tetto su **>= 4 semi** e a passi diversi, e "
       "**capire perche' `median(r)` oscilla di un fattore 4** *(`1.018` / `0.594` / `0.763` / "
       "`0.344` / `1.409` ai cinque istanti)* quando il gauge lo ancorerebbe a `1` | "
       "**in attesa — EMERSO dal ritiro di `S10`, e va IN CODA (`A12` regola 1).** "
       "**MISURATO** su `_g4_riferimento`, 1 seme, 5 istanti *(`_r_corrente` dagli snapshot, "
       "commit `bc30e626`)*: quota con `r > 0.999 * tetto` **`0.76` / `1.19` / `0.83` / `3.35` "
       "/ `29.57 %`**; `min(r)` al passo 360 vale **`1.414e-06`**, che e' la **firma dichiarata "
       "dal codice stesso** *(`f` identicamente nullo -> `x = 0`)*. "
       "**⚠ E NON E' UN DIFETTO DELLA CURA DELL'ANELLO ISTANTANEO:** il gauge e' il "
       "`median(|f|)` del passo **PRECEDENTE** *(cura di categoria D, 2026-09-18, che ha rotto "
       "il punto fisso di `A6`/`A3` DI PROPOSITO)*. Ricostruendo `r` col `median` CORRENTE si "
       "ottiene **mediana `1.000000` esatta**, cioe' il punto fisso pre-cura: **la differenza "
       "e' la cura, non un errore.** **Cio' che NON so e' perche' lo sfasamento produca una "
       "saturazione del 30 %**, e non lo inseguo adesso |")
t = t[:f1] + S11 + t[f1:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- RAMIFICAZIONI
P = "doc/RAMIFICAZIONI.md"
t = io.open(P, encoding="utf-8", newline="").read()
A = "\n| **Z127** \U0001f7e5`LA LETTURA CADE`"
i0 = t.index(A)
riga = t[i0:t.index("\n", i0 + 1)]
Z = ("\n| **Z130** \U0001f7e5`SOSPETTO RITIRATO, MIO` ⏳`[archivi delle cure · LETTURA]` | "
     "**`S10` E' RITIRATA: la premessa era sbagliata DUE VOLTE, e il tetto `1.414213` che avevo "
     "messo in dubbio E' quello del ramo che gira** (2026-09-24, dal sorgente e dalla "
     "ricostruzione, `csv/_test_fork/_RICOSTRUZIONE_config.txt`) | "
     "**IL PRIMO ERRORE, ed e' quello che Luca ha indicato:** `_g_temposegno_tot` sale a "
     "**`:4406`**, **PRIMA** del controllo `if TEMPO_SEGNO`, **e in una FUNZIONE DIVERSA da "
     "`ritmo()`**. Conta le **invocazioni**, non il ramo attivo: **varrebbe `600` con il flag "
     "acceso o spento.** Io avevo letto `_g_temposegno_tot = 600` come *«il ramo `TEMPO_SEGNO` "
     "ha girato 600 volte»*. | "
     "**IL SECONDO ERRORE, che il primo nascondeva, ed e' piu' grosso: `TEMPO_SEGNO` e' "
     "`False`.** In **9 run su 11** *(i due mancanti sono i `controllo`, senza snapshot)*, e "
     "`--tempo-segno` **non compare in nessun lanciatore committato** a nessuno di quei commit. "
     "**Quindi il ramo che chiamavo «vivo» (`r = 1 + mean|tw|/PHI_CRIT`) NON GIRA, e quello che "
     "chiamavo «morto» (il bottleneck `x/sqrt(1+x^2)` normalizzato) E' IL VIVO.** "
     "**Ho scambiato i due rami.** | "
     "**✅ CONSEGUENZA: `Z117` E `Z123` ERANO CORRETTI, e il mio dubbio no.** Il tetto del ramo "
     "vivo e' **`(1+1e-6)/(1/sqrt(2)+1e-6) = 1.414213`**, e si MISURA negli snapshot: "
     "`_r_corrente` ha **max `1.414212974`** al passo 600 e **min `1.414e-06`** al passo 360 — "
     "**esattamente la coppia che `Z117`/`Z123` citavano.** *(E il `1.414e-06` non e' un numero "
     "qualunque: e' `1e-6/(1/sqrt(2)+1e-6)`, cioe' `x = 0`, che il codice stesso chiama «la "
     "FIRMA DEL DIFETTO».)* | "
     "**LEZIONE DI METODO, ed e' `P1` sul mio stesso testo:** ho dedotto quale ramo girasse "
     "**da un contatore**, senza verificare **dove il contatore stesse** rispetto al controllo "
     "del flag, e **senza verificare il valore del flag**. **Due verifiche omesse nella stessa "
     "frase.** **Ed e' esattamente il caso che ha motivato il referto di configurazione** "
     "*(punto 1)*: se `CONFIGURAZIONE.txt` fosse esistito, `TEMPO_SEGNO = False` sarebbe stato "
     "**una riga da leggere** invece di una deduzione da sbagliare. "
     "**⚠ E UN SOSPETTO NUOVO NE ESCE, che va IN CODA e non si insegue (`A12` regola 1): "
     "`S11`** — la quota di nodi con `r` **al tetto** passa da **`0.76 %` a `29.57 %`** in 600 "
     "passi. |")
t = s1(t, riga, riga + Z)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉛ **(1c) `S10` è RITIRATA: la premessa era sbagliata DUE volte**

> **Reperto.** Il sospetto era mio, e il dubbio che gettava su `Z117`/`Z123` **non era
> fondato.**

**① L'errore che hai indicato tu.** `_g_temposegno_tot` sale a **`:4406`**, **prima** del
controllo `if TEMPO_SEGNO`, **e in una funzione diversa da `ritmo()`**. Conta le
**invocazioni**, non il ramo attivo: **varrebbe `600` col flag acceso o spento.** Io avevo
letto `= 600` come *«il ramo `TEMPO_SEGNO` ha girato 600 volte»*.

**② L'errore che il primo nascondeva, ed è più grosso: `TEMPO_SEGNO` è `False`.** In **9 run
su 11**, e `--tempo-segno` **non compare in nessun lanciatore committato**. **Quindi il ramo
che chiamavo «vivo» non gira, e quello che chiamavo «morto» è il vivo. Ho scambiato i due
rami.**

### ✅ **Quindi `Z117` e `Z123` erano corretti, e il mio dubbio no**

Il tetto del ramo vivo è **`(1+10⁻⁶)/(1/√2+10⁻⁶) = 1.414213`**, e **si misura**:

| passo | `min r` | `med r` | `max r` | nodi al tetto |
|--:|--:|--:|--:|--:|
| 120 | `0.000108711` | `1.018363` | `1.414212967` | `0.76 %` |
| 240 | `0.000070231` | `0.593971` | `1.414212936` | `1.19 %` |
| 360 | **`0.000001414`** | `0.763052` | `1.414209114` | `0.83 %` |
| 480 | `0.000047600` | `0.344277` | `1.414212577` | `3.35 %` |
| 600 | `0.010278019` | `1.408827` | `1.414212974` | **`29.57 %`** |

**Il `min` al passo 360 è `1.414e-06`**, che non è un numero qualunque: è
`10⁻⁶/(1/√2+10⁻⁶)`, cioè **`x = 0`** — quello che il codice stesso chiama *«la FIRMA DEL
DIFETTO»*. **È esattamente la coppia che `Z117`/`Z123` citavano.**

### **Lezione di metodo, ed è `P1` sul mio stesso testo**

Ho dedotto **quale ramo girasse da un contatore**, senza verificare **dove il contatore
stesse** rispetto al controllo del flag, e **senza verificare il valore del flag**. **Due
verifiche omesse nella stessa frase.**

> **Ed è il caso che ha motivato il referto di configurazione:** se `CONFIGURAZIONE.txt` fosse
> esistito, **`TEMPO_SEGNO = False` sarebbe stata una riga da leggere** invece di una deduzione
> da sbagliare.

### ⚠ **Un sospetto nuovo ne esce, e va IN CODA — `S11`**

**La quota di nodi con `r` al tetto passa da `0.76 %` a `29.57 %` in 600 passi**, e
`median(r)` oscilla di un **fattore 4** *(`1.018` / `0.594` / `0.763` / `0.344` / `1.409`)*
quando il gauge lo ancorerebbe a `1`. **`A11` cor.6: un limite che satura è un allarme.**

**E NON è un difetto della cura dell'anello istantaneo:** il gauge è il `median(|f|)` del passo
**precedente** *(categoria D, 18/9, che ha rotto il punto fisso di `A6`/`A3` **di proposito**)*.
Ricostruendo `r` col `median` **corrente** si ottiene **mediana `1.000000` esatta**, cioè il
punto fisso pre-cura: **la differenza è la cura, non un errore.**
**Ciò che non so è perché lo sfasamento produca una saturazione del 30 %, e non lo inseguo
adesso** *(`A12` regola 1)*.
"""
assert "(1c) `S10` è RITIRATA" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. S10 ritirata, Z130, S11." % N)
