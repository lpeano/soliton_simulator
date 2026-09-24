# -*- coding: utf-8 -*-
"""La scheda 8 del registro: TORSIONE -> SPINORE, il ponte inverso. E la scheda di CURA 1."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()
assert "nome=torsione-spinore" not in t

SCHEDA = u"""

---

<!-- SCHEDA nome=torsione-spinore funzioni=_passo_spinoriale flag=TW_SPINORE,SYNC_SPINORE,SPIN_LARMOR,SPIN_FEEDBACK -->

# ⑧ TORSIONE → SPINORE — **il ponte INVERSO**

> **Scheda aperta il 2026-09-24 per `CURA 1b`.** È l'unica legge del registro che esiste
> **per essere bloccata**, non per essere applicata.

## LA FORMA, dal codice

```
:3095   _twh = self.tw[mask] / (2.0 * max(PHI_CRIT, 1e-9))
:3097   _otw = np.zeros((n, 3));  _degt = np.zeros(n)
:3098   np.add.at(_otw, ii, _axis * _twh[:, None])          # mutazione IN PLACE
:3099   np.add.at(_otw, jj, _axis * _twh[:, None])
:3100   omega_new = omega_new + _otw / np.maximum(_degt[:, None], 1.0)
```

**Il verso è: `tw` → `omega_s` → `_psi_spinor`.** La **torsione**, che prende la sua scala da
`phi`, **scrive lo SPINORE**.

## PERCHÉ È IL VERSO SBAGLIATO

**È la classe `INVERSA` della mappa del `4pi`** *(`csv/_test_fork/_diag_D/MAPPA_4PI.md`:
`:3100` e la sua conseguenza `:3264`, le **uniche due** su 139 punti)*.

| | |
|---|---|
| il `4pi` di `_psi_spinor` | **`VERA`**: un oggetto di spin 1/2 torna in sé dopo `4pi`. È fisica |
| il `4pi` di `phi` | **`DICHIARATA`**: una **convenzione del codice** |
| `tw` | **`EREDITATA`**: prende la scala da `phi` |

**Quindi `TW_SPINORE` fa scrivere il `4pi` VERO dal `4pi` FINTO.** E la freccia causale del
par.4 di `CLAUDE.md` dice l'opposto: *«i nodi guidano, gli archi ricordano»* — **se in un test
gli spinori diventano passivi (il link li comanda) → BUG, da rilevare, non l'obiettivo.**

## E IL COMMENTO È FALSO, che è una ragione in più

Il commento (`:705-709`, `:2146-2148`) dice che la torsione *«pilota il Bloch di `tw/2`»*, cioè
un **ANGOLO**. **Il codice somma `tw/(2·PHI_CRIT)` a `omega_new`, che è una VELOCITÀ
ANGOLARE**: l'angolo effettivo è **`1.564e-03` rad/passo** contro i **`9.827e-01`** dichiarati,
**fattore `628.3 = 2π/DT`** — *un'unità di misura mancante, non un'approssimazione*.
E il termine finisce in **`self.omega_s`**, la **memoria persistente**, mentre il commento di
`SYNC_SPINORE` dice, **dello stesso blocco**, che metterci un torque *«darebbe
accumulo/divergenza»*. **Unico fra i termini del blocco, `_otw` NON è diviso per l'inerzia.**
→ `doc/REFERTO_tw_spinore.md`, fronte `W`.

## ✅ NON HA MAI GIRATO — **misurato, non supposto**

**`TW_SPINORE = False` in 9 run su 11 ricostruibili**, e **`--tw-spinore` non compare in
nessun lanciatore committato** a nessuno di quei commit
*(`csv/_test_fork/_RICOSTRUZIONE_config.txt`, `Z128`)*. I due non ricostruiti sono i due
`controllo`, che non lasciano snapshot.

> **Nessuna misura di questo programma è contaminata da questa legge.** È il motivo per cui
> bloccarla **non ritira nulla**.

## LA CURA — `CURA 1b`: **il simulatore RIFIUTA DI PARTIRE**

**Decisione di Luca, 2026-09-24.** `TW_SPINORE` resta **nel codice, spento, e BLOCCATO**: se
qualcuno lo accende, il simulatore **si ferma con la ragione**.

**Perché un blocco e non la cancellazione:** par.10 — *«il codice di una legge esclusa non si
cancella mai: resta spento, ed è l'evidenza che spiega perché esiste il suo sostituto»*.
`TW_SPINORE` esiste **perché** `SPIN_LARMOR` fallisce: cancellarlo farebbe perdere il
**perché**.

**Perché un blocco e non un semplice default spento:** il default è già spento, e **non ha
impedito nulla** — `A9`: *un presidio che non impedisce non è un presidio*. Un flag che
introduce il **verso sbagliato del ponte** non deve poter essere acceso **per sbaglio**, e
oggi basterebbe `--tw-spinore`.

**Che cosa NON è:** non è una cura di un difetto misurato, perché **la legge non ha mai
girato e quindi non ha prodotto nulla da curare**. È un **presidio strutturale**, e va detto
così invece di contarlo fra le cure.

## COSA NON SI SA DERIVARE — **dichiarato** *(`A12` regola 4)*

**Se un ponte torsione → spinore possa esistere AFFATTO, in qualche forma.**
L'architettura a un solo ponte dice che la torsione va **ricavata dal trasporto degli
spinori** *(olonomia SU(2))*, non dalle differenze di `phi`. **In quell'architettura la
domanda cambia**: la torsione sarebbe già una proprietà degli spinori trasportati, e una
retroazione su `omega_s` **non sarebbe più un ponte inverso** — sarebbe dinamica interna.
**Non lo so derivare oggi, e non lo decido: è la domanda che il `CHECKPOINT` mette a Luca.**
"""
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + SCHEDA + "\n")
print("scheda 8 (torsione-spinore) scritta")
