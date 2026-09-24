# -*- coding: utf-8 -*-
"""(1d) Via l'affermazione 'ingresso 2pi, avvolgimento 4pi': era sbagliata, in TRE punti."""
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


CORREZIONE = (
    u"**⚠ CORREZIONE del 2026-09-24, rilievo di Luca, verificata dal sorgente: l'avvolgimento "
    u"NON C'ENTRA.** Con `TORS_4PI` acceso la torsione si avvolge con **`_w8` (`:4698`)**, la cui "
    u"finestra e' **`8π`** *(`_w8(a) = (a + 4π) % 8π - 4π`)*: **su incrementi piccoli e' "
    u"l'IDENTITA' e non fa nulla.** **A dimezzare `tw` e' l'INGRESSO:** `dph = self._wphi(...)` "
    u"(`:4675`) e `twp = self._w8(dph + twist_dip)`, e con `FASE_2PI` acceso `dph` sta in "
    u"**`(-π, π]`** *(e `|twist_dip| <= π` per costruzione, quindi la somma sta in `(-2π, 2π]` "
    u"e `_w8` la lascia intatta)*. "
    u"**CONSEGUENZA: `SCALE-TW` NON e' prerequisito di `D36`** — torna **in coda al suo posto** "
    u"*(`A12`)*. **Cio' che resta vero e' il difetto: la soglia e' in unita' assolute di `tw`, e "
    u"`tw` prende la sua scala da `phi`.**")

# ---------------------------------------------------------------- CODA: il punto di ripresa
P = "doc/STATO_RUN.md"
t = io.open(P, encoding="utf-8", newline="").read()
V = (u"**E `SCALE-TW` non è più un lavoro in coda: è il PREREQUISITO**, perché l'INGRESSO di\n"
     u"`tw` vive su `2π` e il suo AVVOLGIMENTO su `4π`.\n")
NU = (u"**⚠ E `SCALE-TW` NON è prerequisito di `D36`** — lo avevo scritto, **ed era sbagliato**:\n"
      u"con `TORS_4PI` la torsione si avvolge con **`_w8`**, finestra **`8π`**, che su incrementi\n"
      u"piccoli è **l'identità**. **A dimezzare `tw` è l'INGRESSO** *(`dph` e `twp` passano da\n"
      u"`_wphi` e stanno in `(-π, π]`)*. **`SCALE-TW` torna in coda al suo posto.**\n")
t = s1(t, V, NU)

# ---------------------------------------------------------------- CODA: la voce D36
V2 = (u"**→ `SCALE-TW` non e' piu' un lavoro in coda: e' il PREREQUISITO di questa cura.** |")
NU2 = CORREZIONE + u" |"
t = s1(t, V2, NU2)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- RELAZIONE (il paragrafo vecchio)
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
V3 = (u"> **oggi l'INGRESSO di `tw` vive su `2π` e il suo AVVOLGIMENTO su `4π`: due scale diverse\n"
      u"> nella stessa grandezza.** **`SCALE-TW` non è più un lavoro in coda: è il PREREQUISITO di\n"
      u"> questa cura.**")
NU3 = (u"> **⚠ QUESTA FRASE ERA SBAGLIATA, e la lascio leggibile con la correzione accanto**\n"
       u"> *(rilievo di Luca, 24/9)*: avevo scritto *«l'INGRESSO di `tw` vive su `2π` e il suo\n"
       u"> AVVOLGIMENTO su `4π`»*. **L'avvolgimento non c'entra:** con `TORS_4PI` la torsione si\n"
       u"> avvolge con **`_w8`**, finestra **`8π`**, che su incrementi piccoli è **l'identità**.\n"
       u"> **A dimezzare `tw` è l'INGRESSO.** → vedi la voce sotto.")
t = s1(t, V3, NU3)

REL = u"""
### ㉜ **(1d) «Ingresso `2π`, avvolgimento `4π`» era SBAGLIATO: l'avvolgimento non c'entra**

> **Rilievo tuo, verificato dal sorgente.** L'avevo scritto in **tre** punti *(punto di ripresa,
> voce `D36`, relazione)*, e da lì avevo concluso che **`SCALE-TW` fosse prerequisito di `D36`**.
> **Non lo è.**

**Cosa dice il sorgente:**

| | |
|---|---|
| `_w8` | `(a + 4π) % 8π − 4π` — finestra **`8π`**, quindi **identità** per `\|a\| < 4π` |
| `:4698` | `self.tw += self._w8(dph + twist_dip − self.twp) − dt_e*self.tw/_ttw` |
| `:4699` | `self.twp = self._w8(dph + twist_dip)` |
| `:4675` | **`dph = self._wphi(_phi_t[i] − _phi_t[j])`** |

**Con `FASE_2PI` acceso `dph` sta in `(-π, π]`**, e `\|twist_dip\| ≤ π` **per costruzione**
*(`twist_dip = π·0.5·(chi_i − chi_j)` con `\|chi_i − chi_j\| ≤ 2`)*: la somma sta in
`(-2π, 2π]`, **e `_w8` la lascia intatta**. **Quindi l'avvolgimento è inerte, e a dimezzare
`tw` è l'INGRESSO.**

> **Conseguenza: `SCALE-TW` torna IN CODA al suo posto** *(`A12`)*, e **non blocca `D36`**.
> **Ciò che resta vero è il difetto stesso:** la soglia della mitosi è in **unità assolute** di
> `tw`, e **`tw` prende la sua scala da `phi`**. Il difetto non dipendeva dall'argomento
> sbagliato — **ma l'argomento sbagliato aveva prodotto una PRIORITÀ sbagliata**, e quella sì.
"""
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. Corretta in 3 punti." % N)
