# -*- coding: utf-8 -*-
"""Z127: E1 NON PASSA. Il punto 2 del par.D cade, e D36 e' acclarato."""
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
A = "\n| **Z125** \U0001f7e5`DIFETTO DI METODO, MIO`"
i0 = t.index(A)
riga = t[i0:t.index("\n", i0 + 1)]
Z = ("\n| **Z127** \U0001f7e5`LA LETTURA CADE` ⏳`[archivi delle cure · PROVA]` | "
     "**`E1` NON PASSA: CON `FASE_2PI` LA GENERAZIONE DI MATERIA SI FERMA. E LA MIA PREVISIONE "
     "ERA SBAGLIATA NEL VERSO, non nell'ampiezza** (2026-09-24, giro CORTO di 120 passi, "
     "`444.7 s`; blob `445e2896`, seme `42`; `csv/_test_fork/_f2p_corto`, test in "
     "`csv/_test_fork/_f2p_corto_TEST_E.txt`) | "
     "**I NUMERI, contro il riferimento allo STESSO passo 120:** "
     "**mitosi `203` nascite in `62` EVENTI → `70` nascite in `1` SOLO evento** · "
     "**Schwinger `53` nascite in `28` eventi → `0` in `0` eventi** · "
     "`n` `2647` → **`2461`, FERMO per tutti e 20 i frame** *(2391 alla semina + 70 del "
     "singolo evento)* · `archi` `526282` → `526043`. "
     "**IL BILANCIO CHIUDE (`4.041e-14`) e `E4` PASSA** *(`max(phi) = 6.282066 < 2pi`)*: "
     "**la cura fa esattamente cio' che dichiara su `phi`. E' la FISICA A VALLE che si "
     "spegne.** | "
     "**PERCHE', ed e' MISURATO non congetturato: `tw` NON E' LA STESSA GRANDEZZA NEI DUE "
     "BRACCI.** "
     "mediana `1.78474` → `1.07472` *(`0.60`)* · media `2.31782` → `1.17595` *(`0.51`)* · "
     "`p99` `6.39139` → `3.14656` *(`0.49`)* · **`MAX` `34.34544` → `4.37278`, cioe' "
     "`1.3919 pi`**. "
     "**ARCHI SOPRA LA SOGLIA: `>= 2pi` `7047` → `0`; `>= 3pi` `952` → `0`; `>= 4pi` `878` "
     "→ `0`.** "
     "**LA SOGLIA NUOVA E' `2pi = 6.28319` E IL MASSIMO DI `|tw|` E' `4.37278`: NESSUN ARCO LA "
     "RAGGIUNGE MAI, e la campana non si accende.** "
     "*(I `70` nati del singolo evento vengono dalla CODA della campana, che e' «quasi zero» "
     "lontano dalla soglia, non zero, su `526043` archi.)* | "
     "**❌ E L'ERRORE E' MIO, ed e' un ERRORE DI POPOLAZIONE (`A3`): HO MISURATO GLI ARCHI SUL "
     "BRACCIO SPENTO E APPLICATO IL CONTO AL BRACCIO ACCESO, dove la grandezza che definisce le "
     "finestre — `tw` — E' PROPRIO QUELLA CHE CAMBIA.** Previsto **`5x`-`100x` in PIU'**, "
     "misurato **`0.345x`**: **sbagliato nel VERSO.** *(E il `49.46x` / `82.36x` delle finestre "
     "restava giusto come conto: era la POPOLAZIONE su cui lo applicavo a essere l'altra.)* | "
     "**✅ COSA QUESTO DA', e vale piu' della previsione sbagliata: `E1` HA GIUDICATO LA CREPA "
     "CHE LUCA AVEVA DICHIARATO LUI STESSO** — *«l'argomento della soglia vale per una "
     "differenza ISTANTANEA, ma `tw` e' un ACCUMULO che decade»*. **La crepa e' REALE e "
     "MISURATA.** "
     "**Il punto 2 del par.D (`soglia0 = 2pi`) NON REGGE, e si scrive invece di aggiustarlo "
     "al volo** (par.5). **→ `D36`.** "
     "**E `E1b` PASSA** *(`n` `2461` contro il tetto `10x` = `26470`)*: **non esplode, MUORE** — "
     "il verso opposto a quello che temevo quando ho messo il giro corto. "
     "**LIMITI: UN seme, UNA scena, 120 passi, UN solo snapshot** — quindi la parte *«`n` "
     "cresce»* di `E1a` non e' nemmeno VALUTABILE su un run a uno snapshot, e cio' che decide "
     "e' il conto degli EVENTI (`1` contro `62`, `0` contro `28`), non `n`. |")
t = s1(t, riga, riga + Z)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- CODA: D36
P = "doc/STATO_RUN.md"
t = io.open(P, encoding="utf-8", newline="").read()
i0 = t.index("| **D35** |")
fine = t.index("\n", i0)
D36 = ("\n| **D36** | **LA SOGLIA DELLA MITOSI E' IN UNITA' ASSOLUTE DI `tw`, MENTRE LA SCALA DI "
       "`tw` DIPENDE DAL DOMINIO DI `phi`: le due NON SI POSSONO CAMBIARE UNA PER VOLTA** "
       "(`:5152-5156`, `soglia0 = PHI_CRIT + twist_max` oppure `PHI_CRIT`) | "
       "**ACCLARATO PER MISURA, `Z127`** *(2026-09-24, blob `445e2896`, 120 passi, seme 42)*: "
       "portando `phi` su `2pi` **`|tw|` si dimezza** *(`p99` `6.391` → `3.147`; `MAX` `34.35` "
       "→ `4.37 = 1.39 pi`)* mentre la soglia scende solo di un terzo *(`3pi` → `2pi`)*: "
       "**gli archi sopra soglia passano da `7047` a `0`** e la generazione di materia si "
       "**ferma** *(mitosi `62` → `1` evento; Schwinger `28` → `0`)*. | "
       "**PERCHE' E' UN DIFETTO E NON UN ACCOPPIAMENTO LEGITTIMO:** una soglia in unita' "
       "**assolute** di una grandezza la cui scala e' fissata da una **convenzione** "
       "*(il dominio di avvolgimento)* **non e' una legge fisica: e' una manopola travestita**. "
       "La stessa famiglia di `A2`/`A3`. **E la crepa era GIA' DICHIARATA da Luca** — "
       "*l'argomento vale per una differenza ISTANTANEA, `tw` e' un ACCUMULO* — **e `E1` l'ha "
       "giudicata.** | "
       "**LA CURA CANDIDATA E' DERIVABILE, e NON la applico:** esprimere la soglia come "
       "**frazione del dominio** invece che in valore assoluto — se un arco porta una "
       "differenza fino a `_dphi()/2` e il quanto e' il dominio intero, la soglia e' "
       "`_dphi()/2` *(cioe' `pi` su `2pi`, `2pi` su `4pi`)*. **MA QUESTO CAMBIA IL PUNTO 2 DEL "
       "par.D, CHE E' UNA DECISIONE DI LUCA**, e la sua regola e' esplicita: *«se un test "
       "fallisce, la decisione cade E SI SCRIVE»*. **Scritta, non applicata.** "
       "**E va misurato PRIMA se `tw` si dimezzi DAVVERO per costruzione o per caso:** il "
       "censimento aveva lasciato `_w4`/`_w8` sulla torsione ACCUMULATA **fuori** dalla cura, "
       "di proposito *(era `SCALE-TW`)* — **quindi oggi l'INGRESSO di `tw` vive su `2pi` e il "
       "suo AVVOLGIMENTO su `4pi`: due scale diverse nella stessa grandezza.** "
       "**→ `SCALE-TW` non e' piu' un lavoro in coda: e' il PREREQUISITO di questa cura.** |")
t = t[:fine] + D36 + t[fine:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
N += 1

# ---------------------------------------------------------------- RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉕ **`E1` NON PASSA: con `FASE_2PI` la generazione di materia SI FERMA**

> Giro **CORTO**, 120 passi, `444.7 s`. Blob `445e2896`, seme `42`.
> **Il bilancio CHIUDE (`4.041e-14`) e `E4` PASSA:** la cura fa *esattamente* ciò che
> dichiara su `φ`. **È la fisica a valle che si spegne.**

| | riferimento *(soglia `3π`)* | con la cura *(soglia `2π`)* |
|---|--:|--:|
| **mitosi** | `203` nascite in **`62` eventi** | `70` nascite in **`1` solo evento** |
| **Schwinger** | `53` nascite in **`28` eventi** | **`0` in `0` eventi** |
| `n` | `2647` | **`2461`, FERMO per tutti e 20 i frame** |

### **PERCHÉ, ed è misurato: `tw` non è la stessa grandezza nei due bracci**

| `|tw|` | RIF | CUR | rapporto |
|---|--:|--:|--:|
| mediana | `1.78474` | `1.07472` | `0.60` |
| media | `2.31782` | `1.17595` | `0.51` |
| `p99` | `6.39139` | `3.14656` | `0.49` |
| **MAX** | `34.34544` | **`4.37278` = `1.3919 π`** | `0.13` |

| archi con | RIF | CUR |
|---|--:|--:|
| `|tw| ≥ 2π` | `7047` | **`0`** |
| `|tw| ≥ 3π` | `952` | **`0`** |
| `|tw| ≥ 4π` | `878` | **`0`** |

> **LA SOGLIA NUOVA È `2π = 6.28319` E IL MASSIMO DI `|tw|` È `4.37278`.**
> **Nessun arco la raggiunge mai, e la campana non si accende.**
> *(I `70` nati del singolo evento vengono dalla CODA della campana — «quasi zero» lontano
> dalla soglia, non zero — su `526043` archi.)*

### ❌ **E L'ERRORE È MIO: un ERRORE DI POPOLAZIONE (`A3`)**

Avevo previsto **`5×`-`100×` in PIÙ**. Misurato: **`0.345×`**. **Sbagliato nel VERSO, non
nell'ampiezza.**

**Ho misurato gli archi sul braccio SPENTO e applicato il conto al braccio ACCESO, dove la
grandezza che definisce le finestre — `tw` — è proprio quella che cambia.** Il `49.46×` delle
finestre era giusto **come conto**: era la **popolazione** su cui lo applicavo a essere l'altra.
**È la stessa famiglia dell'errore che il par.9 chiama «errore di popolazione»**, e l'avevo
scritta io stesso nei criteri: *«la banda è un ordine per lato perché la mitosi consuma la
torsione»* — **avevo visto la retroazione e non avevo visto che `tw` stesso si dimezza.**

### ✅ **Cosa questo dà, e vale più della previsione sbagliata**

**`E1` ha giudicato la crepa che avevi dichiarato tu stesso** — *«l'argomento della soglia vale
per una differenza ISTANTANEA, ma `tw` è un ACCUMULO che decade»*. **La crepa è reale e
misurata.**

**Il punto 2 del §D (`soglia0 = 2π`) NON REGGE.** E la tua regola è esplicita: *«se un test
fallisce, la decisione cade e si scrive»*. **L'ho scritta, non l'ho aggiustata al volo** (par.5).

**→ `D36`, acclarato:** la soglia della mitosi è in **unità assolute** di `tw`, mentre la
**scala** di `tw` dipende dal **dominio di `φ``. Una soglia in unità assolute di una grandezza
la cui scala è fissata da una **convenzione** non è una legge: **è una manopola travestita.**

**LA CURA CANDIDATA È DERIVABILE E NON L'HO APPLICATA:** esprimere la soglia come **frazione
del dominio** — `_dphi()/2`, cioè `π` su `2π` e `2π` su `4π`. **Ma questo cambia il punto 2
del §D, che è una tua decisione.**

> **⚠ E PRIMA VA MISURATA UNA COSA CHE HO LASCIATO DENTRO DI PROPOSITO:** il censimento aveva
> tenuto `_w4`/`_w8` sulla torsione **ACCUMULATA** fuori dalla cura *(era `SCALE-TW`)*. Quindi
> **oggi l'INGRESSO di `tw` vive su `2π` e il suo AVVOLGIMENTO su `4π`: due scale diverse
> nella stessa grandezza.** **`SCALE-TW` non è più un lavoro in coda: è il PREREQUISITO di
> questa cura.**

**E `E1b` PASSA:** `n` `2461` contro il tetto `10×` = `26470`. **Non esplode: MUORE** — il verso
opposto a quello che temevo quando ho messo il giro corto. **Ma il giro corto è servito
comunque: `444.7 s` invece dei `~2200 s` del run vero.**

**LIMITI, e uno è un difetto del mio criterio:** UN seme, UNA scena, 120 passi, **UN solo
snapshot** — quindi la parte *«`n` cresce»* di `E1a` **non è nemmeno valutabile** su un run a
uno snapshot. **Ciò che decide è il conto degli EVENTI** (`1` contro `62`, `0` contro `28`),
**non `n`.**

**MI FERMO QUI, come par.5 impone:** il fallimento è committato, e **non ho lanciato il run a
600 passi.** La scelta è tua — la trovi nella coda sotto `D36`.
"""
assert "`E1` NON PASSA: con `FASE_2PI` la generazione" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. Z127, D36, relazione." % N)
