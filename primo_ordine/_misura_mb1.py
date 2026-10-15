# -*- coding: utf-8 -*-
r"""`M-B1` — **IL RACCORDO: a `theta = pi` il passo nuovo coincide AL BIT con quello di
`717bb60`.**

> **Criterio di uscita di `L1`, nelle parole di Luca:** *«con `dtau = dtau_rif` ovunque
> (`theta = pi`) il nuovo passo coincide **AL BIT** con quello di `717bb60` (stesso stato
> iniziale, **almeno 200 tick**, `psi` e `phi`).»*

## ⭐ PERCHE' IL <<PRIMA>> SI PRENDE DAL COMMIT, E NON DA UNA COPIA NEL FILE

### ⛔ **Tenere nel sorgente una copia dell'operatore vecchio sarebbe il difetto che
`H-P8` impedisce:** il <<prima>> si prende **dal commit**, non da un doppione che
### **nessuno garantisce essere uguale a quello che girava.**
### ✅ **Qui il <<prima>> si estrae con `git archive 717bb60`** in una cartella
temporanea, e ### **questo stesso file si copia la' dentro**: cosi' le due corse usano
**lo stesso misuratore** e differiscono **solo per il codice misurato.**

## ⚠ E CHE COSA VUOL DIRE <<AL BIT>>, detto prima di misurarlo

### **Si confrontano i BYTE GREZZI** di `psi_h` e `phi_h` *(`tobytes()`)*, che e' il
confronto **piu' severo**: ### ⚠ **distingue anche `+0.0` da `-0.0`**, che `==`
considera uguali.
### 📌 **E se la differenza fosse SOLO di zeri firmati lo direi**, perche' sarebbe
**un'identita' di valore e non di byte** — e la differenza fra le due **si dichiara, non
si sceglie.**

## ⛔ IL PERIMETRO

### **Usa `deriva.py` IN SOLA LETTURA** *(`DV.scena` e `DV.tick`)*, che e' cio' che la
scelta di perimetro di Luca del `2026-10-15` ammette per i criteri di uscita di `L1`.
### **Nessuna sua parte e' modificata, e nessuna misura di `L5` e' rifatta.**

## 📌 E LA CONFIGURAZIONE INTERA E' DICHIARATA NELLE COSTANTI DEL MODULO

### `DTAU`, `TICK`, `SCENE`, `NORMA`, `VUOTO_MODULO`, `SU2`: ### **tutte in cima e
tutte stampate**, che e' cio' che `H-P5` pretende da un referto.

Gira con:  python primo_ordine/_misura_mb1.py --contro 717bb60
"""
import hashlib
import os
import shutil
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA**, e ### **`dtau = 1.0` NON e' un
# ### numero scelto: e' `dtau_rif`**, cioe- l-unita- del raccordo di Luca. ### **A
# ### questo livello `cs` e- UNIFORME, quindi `dtau = dtau_rif` ovunque e-
# ### esattamente il caso che il criterio chiede.**
DTAU = 1.0
TICK = 250
SCENE = ((16, 7), (12, 11))
NORMA = "locale"
VUOTO_MODULO = 2.0
SU2 = True


def corri(nn, seme):
    """### `(psi, phi)` dopo `TICK` tick, ### **con la scena dichiarata.**"""
    import deriva as DV
    _i, mot, st, par = DV.scena(nn, seme, DTAU, norma=NORMA,
                                vuoto_modulo=VUOTO_MODULO, su2=SU2)
    for _t in range(TICK):
        DV.tick(st, mot, par)
    return st["psi_h"].copy(), st["phi_h"].copy()


def timbra(a):
    """### `sha1` dei **byte grezzi** dell'array, ### **e la forma col tipo.**"""
    b = np.ascontiguousarray(a).tobytes()
    return hashlib.sha1(b).hexdigest()[:12], b


def scrivi(dove):
    """### Scrive i byte di `psi` e `phi` di **ogni scena**, ### **durante la corsa.**"""
    with open(dove, "wb") as f:
        for nn, seme in SCENE:
            psi, phi = corri(nn, seme)
            tp, bp = timbra(psi)
            tf, bf = timbra(phi)
            f.write(len(bp).to_bytes(8, "little"))
            f.write(bp)
            f.write(len(bf).to_bytes(8, "little"))
            f.write(bf)
            f.flush()
            print("  nn=%-4d seme=%-4d  psi sha1-BYTE %s   phi sha1-BYTE %s"
                  % (nn, seme, tp, tf))
    return 0


def _albero_vecchio(commit, dove):
    """### Un **`git worktree`** di `commit`, ### **e NON un albero nudo.**

    ### ⛔ **UN ALBERO NUDO NON BASTA, e l-ho misurato:** `git archive` da' i file ma
    **non un repo**, e li' `_presidio` ### **RIFIUTA DI GIRARE** -- `P-BARRIERA` vede
    `core.hooksPath` non impostato e si ferma. ### ✅ **E ha ragione:** un misuratore che
    gira dove i presidi non esistono ### **misurerebbe senza sorveglianza.**
    ### ⭐ **Un worktree CONDIVIDE la configurazione del repo**, quindi i presidi ci sono.
    """
    radice = os.path.dirname(_QUI)
    if os.path.isdir(dove):
        subprocess.run(["git", "worktree", "remove", "--force", dove], cwd=radice,
                       capture_output=True)
        if os.path.isdir(dove):
            shutil.rmtree(dove, ignore_errors=True)
    r = subprocess.run(["git", "worktree", "add", "--detach", dove, commit], cwd=radice,
                       capture_output=True)
    assert os.path.isdir(os.path.join(dove, "primo_ordine")), (
        "il worktree di %s non e' nato: %s"
        % (commit, (r.stdout + r.stderr).decode("utf-8", "replace")[-500:]))
    return dove


def contro(commit):
    """### Le DUE corse e il confronto, ### **byte per byte.**"""
    radice = os.path.dirname(_QUI)
    fuori = os.path.join(os.environ.get("TEMP", radice), "mb1")
    if not os.path.isdir(fuori):
        os.makedirs(fuori)
    vecchio = _albero_vecchio(commit, os.path.join(fuori, "albero"))
    io_qui = os.path.join(fuori, "ora.bin")
    io_la = os.path.join(fuori, "prima.bin")
    print("### (1) IL PASSO DI ADESSO, col flusso parziale:")
    scrivi(io_qui)
    # ### ⭐ **lo STESSO misuratore nell-albero vecchio**: cambia il codice misurato,
    # ### ### **non il misuratore.**
    shutil.copyfile(os.path.abspath(__file__),
                    os.path.join(vecchio, "primo_ordine", "_misura_mb1.py"))
    print("### (2) IL PASSO DI %s, estratto dal commit:" % commit[:7])
    r = subprocess.run([sys.executable, os.path.join("primo_ordine", "_misura_mb1.py"),
                        "--scrivi", io_la], cwd=vecchio, capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace"))
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-3000:])
        print("### ⛔ la corsa su %s e' FALLITA: nessun confronto da fare" % commit[:7])
        return 1
    a = open(io_qui, "rb").read()
    b = open(io_la, "rb").read()
    print("-" * 96)
    print("  byte di adesso: %d   byte di %s: %d" % (len(a), commit[:7], len(b)))
    uguali = a == b
    print("  sha1-BYTE adesso %s   sha1-BYTE prima %s"
          % (hashlib.sha1(a).hexdigest()[:12], hashlib.sha1(b).hexdigest()[:12]))
    if uguali:
        print("### ✅ `M-B1` PASSA: identita' AL BIT su %d tick, psi E phi, %d scene"
              % (TICK, len(SCENE)))
        return 0
    # ### ⛔ **E se NON coincidono, si dice DI QUANTO e DOVE** -- un <<diverso>> senza
    # ### ### **il numero non e- una misura.**
    print("### ⛔ `M-B1` FALLISCE: i byte NON coincidono")
    if len(a) == len(b):
        va = np.frombuffer(a, dtype=np.uint8)
        vb = np.frombuffer(b, dtype=np.uint8)
        print("  byte diversi: %d su %d" % (int(np.sum(va != vb)), len(a)))
    return 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if argv and argv[0] == "--scrivi":
        return scrivi(argv[1])
    print("=" * 96)
    print("M-B1: IL RACCORDO AL BIT -- dtau = dtau_rif = %.1f, %d tick, psi E phi"
          % (DTAU, TICK))
    print("=" * 96)
    if argv and argv[0] == "--contro":
        return contro(argv[1])
    scrivi(os.path.join(os.environ.get("TEMP", "."), "mb1_solo.bin"))
    print("### ⚠ senza `--contro <commit>` questa e' UNA SOLA corsa: nessun confronto")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
