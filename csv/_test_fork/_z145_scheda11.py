# -*- coding: utf-8 -*-
"""Scheda 11: IL FRENO DIVENTA LA LEGGE. La cura proposta di D31."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()
assert "nome=freno-legge" not in t

SCHEDA = u"""

---

<!-- SCHEDA nome=freno-legge funzioni=_smorza flag=SCALA_MIN,SCALA_MIN_PASSO,LAM -->

# ⑪ IL FRENO DIVENTA LA LEGGE — **la cura proposta di `D31`**

> **Decisione di Luca, 2026-09-24: SCHEDA ORA, CODICE SOLO DOPO LA PROVA DI `CURA 2`.**
> **Qui non si tocca una riga di codice.**

## 0. LA LEGGE, nelle parole di Luca

> ### **«Nessun arco sotto `LAM`, e l'avvicinamento al minimo è ASINTOTICO: rallenta sempre
> ### di più, senza mai toccarlo.»**

**Che cosa vuol dire, in una riga:** più l'arco è vicino al minimo, più **ogni suo movimento**
viene rallentato. **Al confine la mobilità va a zero**: l'arco si avvicina a `LAM` per sempre
senza toccarlo, come una curva che si avvicina al suo asintoto. **Lontano dal confine la
mobilità torna quasi piena.**

**✅ LA LEGGE È GIUSTA. ❌ LA REALIZZAZIONE NO.**

## 1. IL FRENO DI OGGI — `_smorza`, `:3607-3618`

```python
scende = dx < 0.0
fatt   = max(0.0, 1.0 - LAM / prima)          # = (d - LAM)/d  =  LA MOBILITA'
eff    = np.where(scende, dx * fatt, dx)      # <-- SOLO la discesa
```

Con **`u = d − LAM`** *(la distanza dal minimo)* e **`m = u/d`** *(la mobilità)*:

| verso | oggi | è asintotico? |
|---|---|:--:|
| **discesa** `dx < 0` | `u ← u·(1 + dx/d)`, cioè incremento `dx·m` | **SÌ** — `m → 0` al confine |
| **salita** `dx > 0` | `u ← u + dx` — **identità esatta, nessun rallentamento** | **NO** |

> **È tutta qui l'asimmetria, ed è il cricchetto di `D31`.**

## 2. LA DERIVA DI OGGI — **primo ordine, e MASSIMA AL CONFINE**

Rumore simmetrico: `dx = +a` e `dx = −a` con probabilità `1/2`.

```
E[Δu]  =  ½·(+a)  +  ½·(−a·m)  =  (a/2)·(1 − m)  =  (a/2)·(LAM/d)
```

| | |
|---|---|
| **ordine nel rumore** | **PRIMO** — lineare in `a` |
| **al confine** *(`d → LAM`)* | `LAM/d → 1` ⇒ **`E[Δu] → a/2`: la deriva è MASSIMA proprio dove il vincolo morde** |
| **lontano** *(`d ≫ LAM`)* | `LAM/d → 0` ⇒ la deriva svanisce |

> **Il cricchetto spinge gli archi LONTANO dal muro, e spinge di più quanto più sono vicini.**
> È la forma esatta di ciò che `Z113` ha dimostrato *(deriva `+1.582064e-03` contro l'attesa
> derivata `+1.582007e-03`, scarto `0.0 %`)* e che i bilanci misurano: il termine **FRENO** vale
> **`+117 %`** di `Δ(Σd0)` nel riferimento di `G4`. **Un freno che AGGIUNGE lunghezza è un
> motore.**

## 3. LA FORMA PROPOSTA — **la stessa mobilità nei DUE versi, in forma esatta**

```
(d − LAM)  ←  (d − LAM) · exp(dx / d)
```

cioè, tenendo l'interfaccia di `_smorza` *(che ritorna un INCREMENTO)*:

```
eff  =  u · (exp(dx / d) − 1)              # e il chiamante fa d += eff, come oggi
```

### **LE TRE PROPRIETÀ, verificate sulla formula**

| | | |
|---|---|:--:|
| **(a) SIMMETRICA** | lo stesso fattore per `dx > 0` e `dx < 0`. **Un arco vicino al minimo è «viscoso»: si muove poco in entrambi i versi** | ✅ |
| **(b) MAI SOTTO `LAM`, per QUALUNQUE passo** | `exp(·) > 0` sempre ⇒ `u_new > 0` **strettamente**, anche per `dx → −∞`. **L'arco si avvicina a `LAM` per sempre senza toccarlo** | ✅ |
| **(c) LOCALE** | lontano da `LAM`: `u ≈ d` ⇒ `u_new ≈ d·exp(dx/d) ≈ d + dx` — **tende all'identità** | ✅ |

### **E AL PRIMO ORDINE È ESATTAMENTE LA MOBILITÀ DI OGGI**

```
u·(exp(dx/d) − 1)  =  u·(dx/d)  +  O(dx²)  =  dx·m  +  O(dx²)
```

**Cioè: il fattore non cambia, cambia il VERSO IN CUI SI APPLICA.** Non è una legge nuova: è
**la stessa legge, resa simmetrica**.

### ⚠ **E UN GUADAGNO CHE OGGI NON C'È: il vincolo vale anche A METÀ PASSO**

Oggi `u ← u(1 + dx/d)` diventa **negativo** se `dx < −d`, e il conto è immediato. Il
`max(0, …)` protegge il **fattore**, non il **risultato**. Oggi quel caso è solo **contato**
*(`_g_sm_patol`)*. **Con l'esponenziale non può succedere**, e il vincolo vale **a ogni
scrittura**, non solo al controllo di fine passo.

## 4. LA DERIVA RESIDUA — **secondo ordine, nulla al confine, decade lontano**

Stesso rumore simmetrico `dx = ±a`:

```
E[u_new]  =  u · ½·(e^{a/d} + e^{−a/d})  =  u · cosh(a/d)

E[Δu]     =  u · (cosh(a/d) − 1)  =  u · a²/(2d²)  +  O(a⁴)
```

| | oggi | proposta |
|---|---|---|
| **ordine nel rumore** | **primo**: `(a/2)·(LAM/d)` | **SECONDO**: `u·a²/(2d²)` |
| **al confine** `d → LAM` | **`→ a/2`, MASSIMA** | **`→ 0`** *(perché `u → 0`)* |
| **lontano** `d ≫ LAM` | `→ 0` | `→ a²/(2d)`, decade come `1/d`; **in termini RELATIVI `a²/(2d²)`** |

### **IL RAPPORTO FRA LE DUE, e da' una CONDIZIONE**

```
  nuova / oggi  =  [u·a²/(2d²)] / [(a/2)·(LAM/d)]  =  a·u / (d·LAM)  =  a·(d−LAM) / (d·LAM)
```

* **al confine** `d → LAM`: il rapporto **→ 0**. La proposta è **incomparabilmente migliore
  proprio dove oggi la deriva è massima**;
* **lontano** `d ≫ LAM`: il rapporto **→ `a / LAM`**.

> ### ❗ **QUINDI LA PROPOSTA È MIGLIORE OVUNQUE SE E SOLO SE `a < LAM`**
> cioè **se il passo tipico di rumore è più piccolo della scala minima**.
> **`LAM = 0.8`. Il valore di `a` NON È MISURATO**, e va misurato prima di cablare: è la
> prima cosa che la verifica deve dire. *(`A12` regola 4: dichiarato, non assunto.)*

## 5. ❌ **PERCHÉ NON `exp(dx/u)`** — la variabile `log(d − LAM)`

La scelta «naturale» sarebbe far evolvere **liberamente** `log u`, cioè `u ← u·exp(dx/u)`.
**È SBAGLIATA, e il motivo è un conto:** vicino al confine `u → 0`, quindi **una spinta in su
piccola diventa un salto enorme** — `exp(a/u) → ∞`. **Una spinta LIMITATA produrrebbe uno
spostamento ILLIMITATO**, che è la firma di `A11`.

**Con `exp(dx/d)` non succede**, perché `d ≥ LAM > 0` **per legge**, quindi l'esponente è
**limitato da `|dx|/LAM`**.

> **Era una mia proposta, e Luca l'ha corretta prima che diventasse codice.** Sta qui perché
> **il codice di una via scartata non si cancella: e' l'evidenza che spiega perché esiste
> quella scelta** *(par.10)*.

## 6. I LIMITI, CLASSIFICATI CON `A11`

| limite | oggi | con la proposta |
|---|---|---|
| `max(0.0, 1.0 - LAM/base)` | **protegge il FATTORE** dal diventare negativo quando `d < LAM` — cioè **da uno stato che `E4-LAM` ora VIETA** | **SPARISCE**: `d ≥ LAM` è un invariante verificato **sempre**, quindi `1 − LAM/d ≥ 0` è **derivato** |
| `pos = prima > 0` | protegge da `d = 0` | **SPARISCE per la stessa ragione**: `d ≥ LAM > 0` |
| *(nuovo)* overflow di `exp` | — | **NESSUN CLAMP.** `|dx|/d ≤ |dx|/LAM`, e se mai superasse `709` è **`np.seterr(over='raise')`** a fermarsi **con la riga** — la stessa scelta di `E4-LAM` |

> **Due limiti spariscono e nessuno nasce**, e questa volta **l'ho verificato** invece di
> dirlo *(è l'errore di `Z142`)*: entrambi proteggevano da `d < LAM`, che **ora è un
> invariante**.

## 7. LA VERIFICA, **sulla FORMULA, col test di `Z113`**

**Non un run: un conto**, come `Z113`. Lo strumento deve mostrare:

| | che cosa | criterio |
|---|---|---|
| **`V1`** | **quanto vale `a`**, il passo tipico di rumore, **misurato** | è il numero che decide la condizione `a < LAM` del par.4 |
| **`V2`** | la deriva di **oggi** sotto rumore simmetrico | deve **riprodurre `Z113`**: `≈ +1.582e-03` con i suoi parametri |
| **`V3`** | la deriva della **proposta**, stessa `a`, stessi `d` | deve essere **del secondo ordine**: raddoppiando `a` deve **quadruplicare**, non raddoppiare |
| **`V4`** | la deriva della proposta **al confine** *(`d → LAM`)* | **→ 0**, mentre quella di oggi **→ `a/2`** |
| **`V5`** | la deriva della proposta **lontano** | decade come `1/d` in assoluto, `1/d²` in relativo |
| **`V6`** | **il caso che DEVE fallire**: la forma `exp(dx/u)` | deve **esplodere** vicino al confine, e il test lo deve **mostrare** |
| **`V7`** | **mai sotto `LAM`**: una discesa enorme, `dx = −100·d` | oggi **attraversa**; la proposta **no**, per qualunque passo |

## 8. COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **che la deriva residua di secondo ordine sia TRASCURABILE.** So che è di second'ordine,
   nulla al confine e decrescente lontano. **Non so derivare che su `600` passi e `526` mila
   archi non si accumuli**: è una misura, non un teorema;
2. **il valore di `a`**, il passo tipico di rumore. **Senza, la condizione `a < LAM` non si può
   dichiarare vera** — ed è il punto `V1`;
3. **se la stessa forma vada applicata a `d0` come a `d`.** `_smorza` è chiamata per **entrambi**
   *(`quale` ∈ `{d, d0, d0_passo, …}`)*, e `d0` è una lunghezza di **riposo**: che debba obbedire
   alla stessa legge è **plausibile, non derivato**;
4. **chi spinge gli archi contro il muro.** La proposta toglie **il cricchetto del freno**, non
   la **causa** per cui gli archi ci arrivano. **Resta aperta e SEPARATA:** `D33` e `S05`.

> **E la cosa più importante, che non va persa:** **questa cura NON elimina la deriva. La
> abbassa di un ordine e la annulla dove oggi è massima.** Dire *«il cricchetto sparisce»*
> sarebbe falso: `cosh(x) ≥ 1` sempre, quindi `E[Δu] ≥ 0` **sempre**. **Cambia l'ORDINE, non il
> segno.**
"""
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + SCHEDA + "\n")
print("scheda 11 (freno-legge) scritta")
