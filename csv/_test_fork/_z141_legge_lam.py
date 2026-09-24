# -*- coding: utf-8 -*-
"""La legge di LAM e' STRUTTURALE (Luca), cs non puo' essere zero, e niente clamp in CURA 2."""
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


# ================================================================ (1) la scheda 9
P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()

A = u"""### ❌ **CORREZIONE MIA: i clamp NON sono «due che spariscono». È UNO che sparisce e UNO che NASCE.**"""
B = u"""### ✅ **DECISIONE DI LUCA, 2026-09-24: NON SI SCRIVE NESSUN CLAMP. È UNA LEGGE.**

> ### **«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema» è una
> ### LEGGE, non una garanzia che dipende da un flag.**

**Quindi in `CURA 2` `tau_arco = d / cs_arco` si scrive COSÌ, senza `np.maximum`.** Se uno dei
due fosse zero, **il livello NUMERICO di `C5` alza un'eccezione con la riga esatta**:
`np.seterr(over='raise', divide='raise', invalid='raise')` a **`:7382`**. **È `A11` fatto bene:
un limite che protegge da un errore si sostituisce con il RILEVAMENTO dell'errore.**

#### ① **`d ≥ LAM`: L'INVARIANTE ESISTE — MA È GATED SU UN FLAG, ed è il difetto**

`DOMINI['d'] = ('lam', …)` e `DOMINI['d0'] = ('lam', …)` **ci sono** (`:215-216`). Ma il
controllo, a **`:3702`**, è:

```python
_lam_attivo = SCALA_MIN or SCALA_MIN_PASSO        # :3657
…
if _lam_attivo:
    cattivo = ~fin | (vf < LAM * (1.0 - 1e-12));  regola = '>= LAM, con la scala minima accesa'
else:
    cattivo = ~fin | (vf <= 0.0);                 regola = '> 0 (scala minima SPENTA)'
```

> **Una LEGGE verificata solo quando un flag è acceso non è una legge: è un'opzione.**
> **→ va reso INCONDIZIONATO**, ed è la voce `E4-LAM` della coda: **non lo faccio in `CURA 2`**,
> perché cambierebbe il comportamento di una configurazione diversa da quella dei run *(a flag
> spenti, un `d < LAM` oggi passa e domani fermerebbe il run)*, **e quella è una decisione di
> Luca su `C5`, non un pezzo di questa cura.**
>
> **Per `CURA 2` non serve:** nei run `SCALA_MIN_PASSO` è **acceso**, quindi l'invariante
> controlla `d ≥ LAM` **davvero**, e **misurato**: `min(d) = 0.800000 = LAM` esatto, `0` archi
> sotto su `526302`.

#### ② **`cs` NON PUÒ ESSERE ZERO — derivato dal codice, non misurato**

```python
_scala      = max(_Lam, 1e-30) / GAMMA_TURBO**2
cs_floor    = CS_M / (1.0 + sqrt(_I) * sqrt(1.0/_scala))      # > 0: il denominatore e' >= 1
cs_floor    = min(cs_floor, CS_M)                             # quindi 0 < cs_floor <= CS_M
transizione = 0.5 * (1.0 + tanh(1.0 - u_nodo))                # in (0, 1) STRETTO
return        cs_floor + (CS_M - cs_floor) * transizione      # >= cs_floor > 0
```

**`cs ∈ (0, CS_M]` PER COSTRUZIONE**, e `cs_arco` è la **media armonica di due numeri
positivi**, dunque **positiva**. *(La misura concorda e non serve alla dimostrazione:
`min(cs) = 4.3465e-01`, **`0` zeri esatti** su `2660` nodi.)*

> **Quindi è un INVARIANTE, non un caso da contare** — e si aggiunge a `DOMINI`:
> `'_cs_nodo_prev': ('pos', …)`. **Legge soltanto: su un run sano non cambia un bit.**
> **Nel ramo `CS_DINAMICO` spento `cs_arco = CS_M` costante**, quindi positivo anche lì.

### ❌ **E RESTA LA MIA CORREZIONE SUL CONTO DEI CLAMP, perché il primo pezzo era giusto**"""
t = s1(t, A, B)

# il clamp "nuovo" non esiste piu': si aggiorna la tabella
A2 = u"""| `max(tau_arco, 1e-12)` | — | **NASCE, ed è VIVO** | ⚠ **UN CLAMP IN PIÙ, non in meno** |"""
B2 = (u"| `max(tau_arco, 1e-12)` | — | **NON SI SCRIVE** *(decisione di Luca)* | **`d ≥ LAM` è una "
      u"legge e `cs > 0` è derivato: al posto del clamp c'è l'INVARIANTE** |")
t = s1(t, A2, B2)
A3 = (u"**Perché è vivo:** `tau_arco = d/cs_arco` si annulla se `d = 0`, e **`d ≥ LAM` vale solo con\n"
      u"`SCALA_MIN` oppure `SCALA_MIN_PASSO` accesi** *(il pavimento di `_nasce`)*. **È una dipendenza,\n"
      u"e va dichiarata.**")
B3 = (u"**Il primo pezzo resta vero e utile:** `max(tau_pp, 1e-12)` era **codice morto**, e "
      u"accorgersene è il tipo di cosa che `A11` chiede. **Il secondo pezzo è caduto**: non nasce "
      u"nessun clamp, perché `d ≥ LAM` è una **legge** e `cs > 0` è **derivato**.")
t = s1(t, A3, B3)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ================================================================ (2) D31 e la coda
P = "doc/STATO_RUN.md"
t = io.open(P, encoding="utf-8", newline="").read()
i0 = t.index("| **D31** ")
fine = t.index("\n", i0)
riga = t[i0:fine]
NU = riga.rstrip()
if NU.endswith("|"):
    NU = NU[:-1]
NU += (u" **✅✅ DECISIONE DI LUCA, 2026-09-24 — E RIBALTA IL MODO DI LEGGERE `D31`:** "
       u"*«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema»* è una "
       u"**LEGGE**, e **deve diventare STRUTTURALE**: sempre accesa, **candidata all'epoca 3**. "
       u"**LA LEGGE E' GIUSTA. L'IMPLEMENTAZIONE NO.** "
       u"**La realizzazione di quella legge OGGI e' il FRENO A SENSO UNICO, cioe' esattamente "
       u"`D31`:** si frena la discesa e non la salita, e da li' viene il cricchetto "
       u"*(dimostrato sulla formula, `Z113`, deriva `+1.582064e-03` contro l'attesa derivata "
       u"`+1.582007e-03`, scarto `0.0 %`)*. "
       u"**QUINDI `D31` NON SI CURA TOGLIENDO IL PAVIMENTO:** il pavimento e' la legge. **Si cura "
       u"cambiando COME lo si realizza**, e la forma giusta non e' un freno asimmetrico. "
       u"**⚠ E OGGI LA LEGGE NON E' NEMMENO VERIFICATA SEMPRE:** l'invariante `d >= LAM` di `C5` "
       u"e' **gated** su `SCALA_MIN or SCALA_MIN_PASSO` (`:3657`, `:3702`); a flag spenti degrada "
       u"a `d > 0`. **Una legge verificata solo quando un flag e' acceso non e' una legge: e' "
       u"un'opzione.** → voce `E4-LAM`. |")
t = t[:i0] + NU + t[fine:]

# la voce E4-LAM in coda
i1 = t.index("| **S13** |")
f1 = t.index("\n", i1)
E4 = (u"\n| **E4-LAM** | **LA LEGGE «NESSUNA LUNGHEZZA SOTTO `LAM`» DEVE DIVENTARE STRUTTURALE** "
      u"— sempre accesa, **candidata all'epoca 3** *(decisione di Luca, 2026-09-24)* | "
      u"**DUE cose, distinte:** ① l'**INVARIANTE** `d >= LAM` di `C5` va reso "
      u"**INCONDIZIONATO** *(oggi è gated su `SCALA_MIN or SCALA_MIN_PASSO`, `:3702`, e a flag "
      u"spenti degrada a `d > 0`)*; ② la **REALIZZAZIONE** della legge va cambiata, perché oggi "
      u"è il **freno a senso unico** = **`D31`** | "
      u"**in attesa — NON è parte di `CURA 2`.** Rendere l'invariante incondizionato "
      u"**cambierebbe il comportamento di una configurazione diversa da quella dei run**: a flag "
      u"spenti un `d < LAM` oggi **passa**, domani **fermerebbe il run** con riga e indici. "
      u"**È una decisione su `C5`, e la prende Luca.** "
      u"**Per `CURA 2` non serve:** nei run `SCALA_MIN_PASSO` è acceso, l'invariante controlla "
      u"`d >= LAM` davvero, e **misurato: `min(d) = 0.800000 = LAM` esatto, `0` archi sotto su "
      u"`526302`**. |")
t = t[:f1] + E4 + t[f1:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
N += 2
print("%d sostituzioni: scheda 9, D31, E4-LAM." % N)
