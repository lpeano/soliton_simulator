# -*- coding: utf-8 -*-
"""Relazione: E4-LAM passa 6/6, D37 curato."""
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


# RAMIFICAZIONI
P = "doc/RAMIFICAZIONI.md"
t = io.open(P, encoding="utf-8", newline="").read()
A = "\n| **Z142** \U0001f7e5`REPERTO, DIFETTI MIEI`"
i0 = t.index(A)
riga = t[i0:t.index("\n", i0 + 1)]
Z = ("\n| **Z144** \U0001f7e9`CURA IN CODICE` ⏳`[archivi delle cure · CURA]` | "
     "**`E4-LAM` PASSA `6/6`: la legge `d >= LAM` si verifica SEMPRE, e `D37` e' curato nello "
     "stesso giorno in cui e' nato** (2026-09-24, `csv/_seal_fork/_sig_e4lam/REFERTO.txt`) | "
     "**LA CURA:** il controllo della forma `'lam'` non e' piu' dentro `if _lam_attivo`, e "
     "**`_lam_attivo` e' stato TOLTO** — dall'AST i riferimenti di **codice** sono **`[]`** "
     "*(nel TESTO compare 2 volte, e sono i COMMENTI che spiegano la rimozione: e' il "
     "difetto del criterio vecchio, `Z142`)*. **Prima, a flag spenti, la legge DEGRADAVA a "
     "`d > 0`.** | "
     "**I SEI TEST:** `T1` nessun riferimento di codice a `_lam_attivo` **dall'AST** · "
     "**`T1b` `DOMINI` non ha chiavi duplicate: `42` chiavi, `0` duplicate** — e' la cura di "
     "`D37`, e resta come **test permanente** · `T2` `cs` e' un invariante `pos` · "
     "**`T3` un arco sotto `LAM` a flag SPENTI FERMA IL RUN**, con riga, regola, indici e arco "
     "· **`T4` e con `d >= LAM` NON si ferma** — il controllo che rende `T3` leggibile · "
     "**`T5` BYTE-INERTE: `206` campi identici, `0` diversi** contro `_cura1_corto`. | "
     "**IL COLLAUDO E' `8/8`, CON QUATTRO CASI CHE DEVONO FALLIRE:** `K2` un arco sotto `LAM` a "
     "flag spenti **deve** fermarsi · `K4` la regola **VECCHIA** a flag spenti era `d > 0`, e "
     "`min(d) = 0.4 > 0`: **passava** · **`K5` `_lam_attivo` SOLO in un commento: l'AST dice "
     "`[]` mentre un `in` sul testo direbbe TROVATO** — riproduce il difetto del criterio "
     "vecchio · **`K7` un `DOMINI` con la chiave `'a'` due volte → `['a']`**. | "
     "**⚠ E COSA QUESTO NON DICE:** che `d >= LAM` sia la **REALIZZAZIONE** giusta della legge. "
     "Dice che la legge e' ora **VERIFICATA SEMPRE**. **La realizzazione di oggi e' il FRENO A "
     "SENSO UNICO, cioe' `D31`** — e la sua cura e' il lavoro successivo. "
     "**Il sistema aveva una legge giusta, realizzata male, e controllata solo a volte: ora "
     "almeno il controllo non dipende piu' da un flag.** |")
t = s1(t, riga, riga + Z)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉨ **`E4-LAM` passa `6/6`, e `D37` è curato nello stesso giorno in cui è nato**

> `csv/_seal_fork/_sig_e4lam/REFERTO.txt`. **Collaudo `8/8`, con QUATTRO casi che devono
> fallire.**

| | | |
|---|---|---|
| `T1` | `_lam_attivo` non ha più riferimenti di **codice** — **dall'AST: `[]`** | **PASS** |
| **`T1b`** | **`DOMINI` non ha chiavi duplicate: `42` chiavi, `0` duplicate** | **PASS** |
| `T2` | `cs` è un invariante `pos` | **PASS** |
| **`T3`** | **un arco sotto `LAM` a flag SPENTI ferma il run** | **PASS** |
| **`T4`** | e con `d ≥ LAM` **non** si ferma | **PASS** |
| **`T5`** | **byte-inerte: `206` campi identici, `0` diversi** | **PASS** |

**`T1` stampa anche quante volte il nome compare nel TESTO — `2`, e sono i commenti che
spiegano la rimozione.** Così la differenza fra le due letture resta **visibile nel referto**,
invece di essere una nota in un commit.

### **I quattro casi che devono fallire, perché sono la parte che vale**

| | |
|---|---|
| `K2` | un arco sotto `LAM` a flag spenti **deve** fermarsi |
| `K4` | la regola **vecchia** a flag spenti era `d > 0`, e `min(d) = 0.4 > 0`: **passava** |
| **`K5`** | **`_lam_attivo` solo in un commento: l'AST dice `[]`, un `in` direbbe TROVATO** — riproduce il difetto del criterio vecchio |
| **`K7`** | un `DOMINI` con la chiave `'a'` due volte → `['a']` |

### ✅ **`D37` curato, e la derivazione non è stata buttata**

La mia voce duplicata (`:226`) è **via**, e **la derivazione di `cs > 0` è stata SPOSTATA sulla
voce preesistente** invece di essere cancellata — col motivo per cui era nata e col perché era
un duplicato. **E `T1b` resta come test permanente:** qualunque chiave duplicata, d'ora in poi,
fa fallire il sigillo.

### ⚠ **Cosa questo NON dice**

**Non dice che `d ≥ LAM` sia la REALIZZAZIONE giusta della legge.** Dice che la legge è ora
**verificata sempre**.

> **La realizzazione di oggi è il freno a senso unico, cioè `D31`.** Il sistema aveva **una
> legge giusta, realizzata male, e controllata solo a volte**: ora almeno il controllo non
> dipende più da un flag. **Il punto ② di `E4-LAM` resta aperto**, ed è la scheda del
> freno-legge.
"""
assert "`E4-LAM` passa `6/6`" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. Z144 e relazione." % N)
