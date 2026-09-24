# -*- coding: utf-8 -*-
"""La regola dell'ASSENZA diventa STANDARD (si' esplicito di Luca, 2026-09-24)."""
import io
import re
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


P = "doc/PATTERN_DI_PROVA.md"
t = io.open(P, encoding="utf-8", newline="").read()

# --- la riga 9 fra gli STANDARD, subito prima del richiamo alle regole di altrove
RIGA9 = (
    u"| **9** | **Un'ASSENZA si dichiara solo da una ricerca sull'INTERO FILE o dall'AST.** "
    u"Mai da una finestra di righe, mai da un `in` sul testo. | *decisione di Luca, 2026-09-24* "
    u"· `2070aab` | **TRE casi in un giorno, e sbagliano nei DUE versi opposti:** `S10` "
    u"*(dedotto da un contatore, senza verificare né dove stesse né il valore del flag — "
    u"**ritirato**)* · `T1` di `E4-LAM` *(`\"_lam_attivo\" not in sorg` trova le sue occorrenze "
    u"nei **COMMENTI** → **`FAIL` falso su codice corretto**)* · `D37` *(cercato in una finestra "
    u"di **28 righe**, la voce stava a `:257` → **chiave duplicata**, codice morto in silenzio)*. "
    u"| ogni affermazione di assenza porta **il comando che l'ha prodotta**, e quel comando "
    u"**non ha un intervallo di righe**. Per una domanda su un riferimento di **codice**: "
    u"**l'AST**, non un `in`. |")

V = "\n### Le regole che valgono qui e stanno già altrove"
t = s1(t, V, "\n" + RIGA9 + V)

# --- la sezione IN PROVA torna vuota, e si dichiara DOVE e' andata la regola
i0 = t.index("## IN PROVA")
i1 = t.index("## RESPINTE")
NUOVA = (u"## IN PROVA\n\n"
         u"*(nessuna)*\n\n"
         u"> **La regola sull'ASSENZA è stata PROMOSSA a `STANDARD` il 2026-09-24**, col **sì "
         u"esplicito di Luca** — **riga `9`**. È rimasta `IN PROVA` meno di un'ora, e non perché "
         u"fosse ovvia: perché aveva **tre casi reali già misurati** nel giorno stesso.\n"
         u">\n"
         u"> **⚠ E IL SUO LIMITE RESTA QUELLO DICHIARATO QUANDO ERA `IN PROVA`, la promozione "
         u"non lo cancella:** **non è un presidio** *(`A9`)*. Non impedisce nulla: è un **obbligo "
         u"di forma verificabile dal destinatario**. **Cosa la renderebbe un presidio:** un "
         u"controllo che rifiuti, nei referti generati, le parole *«non esiste» / «manca» / "
         u"«assente»* se non accompagnate da un comando **senza intervallo di righe**. **NON è "
         u"scritto**, e la regola non va chiamata presidio finché non lo è.\n\n")
t = t[:i0] + NUOVA + t[i1:]
N += 1

io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# controllo: quante righe STANDARD ci sono ora
n_std = len(re.findall(r"^\| \*\*\d+\*\* \|", t, re.M))
print("%d sostituzioni. Righe STANDARD ora: %d" % (N, n_std))
