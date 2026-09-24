# -*- coding: utf-8 -*-
"""La correzione del grafo: l'orologio viene dallo SPINORE. + (3) e (4) IN CODA. + INVENTARIO."""
import hashlib
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


B = hashlib.sha1(io.open("csv/_test_fork/_sonda_fallback_psispin.py", "rb").read()).hexdigest()[:8]
BM = hashlib.sha1(io.open("csv/_test_fork/_mappa_4pi.py", "rb").read()).hexdigest()[:8]

# ---------------------------------------------------------------- INVENTARIO
P = "doc/INVENTARIO_strumenti.md"
t = io.open(P, encoding="utf-8", newline="").read()
anc = "| **`csv/_test_fork/_mappa_4pi.py`** |"
i0 = t.index(anc)
riga = t[i0:t.index("\n", i0)]
V = ("\n| **`csv/_test_fork/_sonda_fallback_psispin.py`** | **`" + B + "`** | "
     "`python csv/_test_fork/_sonda_fallback_psispin.py` *(`SONDA_PASSI` per cambiare i "
     "passi; default 30)* | "
     "**QUANTE VOLTE SCATTA IL FALLBACK `:3394`**, l'UNICO punto in cui `phi` entra nella "
     "catena dell'orologio. **NON modifica il simulatore:** avvolge `calcola_psi` e valuta la "
     "STESSA condizione di `:3393` prima di ogni chiamata. **`P5`: un fallback mai misurato e' "
     "un comportamento sconosciuto** — i precedenti sono `_cs_nodo_prev` al `71.88 %` e "
     "`_psi_spin_prec` al `95.33 %`, per mesi. **MISURATO: `3` su `441` (`0.68 %`), alle "
     "invocazioni `1-2-3`.** | `csv/_test_fork/_sonda_fallback_psispin.txt` |")
t = s1(t, riga, riga + V)
t = s1(t, "| **`csv/_test_fork/_mappa_4pi.py`** | **`9a53f27b`** |",
       "| **`csv/_test_fork/_mappa_4pi.py`** | **`" + BM + "`** *(era `9a53f27b`: grafo "
       "corretto, l'orologio viene dallo SPINORE)* |")
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- CODA: (3) e (4) in coda
P = "doc/STATO_RUN.md"
t = io.open(P, encoding="utf-8", newline="").read()
V2 = "<!-- INDIRIZZO:FINE -->"
NU2 = u"""## ⏳ IN CODA, e NON bloccano le cure *(`A12` regola 1)*

**Decisione di Luca, 2026-09-24.** Due lavori del prompt unico **vanno in coda**, perché sono
**misure** e `A12` dice che una misura nuova non passa davanti a una cura derivabile:

| | lavoro | perché è in coda |
|--:|---|---|
| **(3)** | **`S08`: che cos'è `phi`** — la catena che lo aggiorna, e se si ottiene dalla fase globale `U(1)` dello spinore *(il Bloch è caduto: `Z121`)* | è una **misura**, e la sua risposta **non cambia** nessuna delle tre cure |
| **(4)** | **LA MAPPA DEI TEMPI** — ogni lettore di `r`, `dt_n`, `tau_pp`, `d/cs`, e l'anello `A6` | idem. **E una parte è già fatta:** la provenienza dell'orologio è nel grafo della mappa del `4pi`, misurata |

> **Servono per la torsione dal trasporto `SU(2)`**, che è **dopo** il `CHECKPOINT`.

<!-- INDIRIZZO:FINE -->"""
t = s1(t, V2, NU2)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉞ **Il grafo corretto: l'OROLOGIO viene dallo SPINORE, non da `phi`**

> **Rilievo tuo**, e la misura lo conferma con un margine che non lascia dubbi.

**Dal codice:** il ramo **vivo** di `ritmo()` (`:2628-2629`) legge
`np.angle(psi_spin[:,0]) − np.angle(_psi_spin_prec[:,0])`, e **`psi_spin` è costruito a
`:3398` dallo snapshot `_psi_spinor`**:

```
psi_spin = mat(w) @ (amp * _psi_spinor)
```

**`phi` entra in quella catena in UN SOLO punto**, il fallback `:3393-3394`:

```python
if _psp is None or len(_psp) < _n:
    _psp = np.zeros((_n, 2), complex);  _psp[:, 0] = np.exp(1j * self.phi[:_n])
```

### **Quante volte scatta: `3` su `441`, e tutte e tre all'avvio**

| | |
|---|--:|
| invocazioni di `calcola_psi` con `CAMPO_SPINORIALE` acceso | **441** |
| di cui il fallback è scattato | **3** — **`0.68 %`** |
| perché `_psi_spinor` era **assente** | `0` |
| perché era più **corto** di `n` | `3` |
| **quando** | invocazioni **`1, 2, 3`** |
| forma al fallimento `(len, n)` | `(0, 2391)` × 3 |

**È il transitorio del primo passo, quando `_psi_spinor` non esiste ancora, e dopo la terza
invocazione non scatta più.** Il criterio di lettura era **scritto nel codice della sonda prima
di girarla**, e non aveva soglie da scegliere: *zero → il grafo si corregge; solo alle prime
invocazioni → transitorio, grafo corretto comunque; sparso sul run → il grafo NON si corregge,
ed è un reperto*.

> **La domanda non era retorica:** i precedenti di questa famiglia sono **`_cs_nodo_prev` al
> `71.88 %`** e **`_psi_spin_prec` al `95.33 %`**, per mesi, in silenzio. **Qui è `0.68 %` e
> solo all'avvio.**

### **Cosa cambia nel grafo, e cosa NON cambia**

**Cambia:** la freccia **`phi → TEMPI` sparisce a regime**. L'orologio è
**`SPINORE → psi_spin → r`**. E la freccia **`SPINORE → phi`** resta, ma va **letta nel verso
giusto**: `_phc`/`phivel`/`omega_clk` fanno **avanzare** `phi`, quindi **`phi` è una
conseguenza dello spinore**, non una sorgente.

**Non cambia:** `tw` **prende ancora la sua scala da `phi`** *(`:4675`, `dph = _wphi(phi[i] −
phi[j])`)*, e da `tw` dipendono **mitosi, Schwinger e repulsione**. **Il difetto che l'indirizzo
descrive resta intero.**

**E una cosa che il grafo diceva male:** avevo messo `ritmo` fra i figli di `tw`. È vero **solo
del ramo `TEMPO_SEGNO`** (`r = 1 + mean|tw|/PHI_CRIT`), **che non gira** *(`Z130`)*. Da `tw`
restano **`tau_pp`** e, indirettamente, la repulsione.

### ⏳ **E (3) `S08` e (4) la mappa dei tempi vanno IN CODA** *(`A12` regola 1)*

Sono **misure**, e la loro risposta **non cambia nessuna delle tre cure**. Servono per la
**torsione dal trasporto `SU(2)`**, che è **dopo** il `CHECKPOINT`.
"""
assert "Il grafo corretto: l'OROLOGIO viene dallo SPINORE" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. sonda %s, mappa %s" % (N, B, BM))
