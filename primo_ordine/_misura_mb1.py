# -*- coding: utf-8 -*-
r"""`M-B1` — **IL RACCORDO AL BIT, PEZZO PER PEZZO, contro `717bb60`.**

> **Criterio RIFORMULATO da Luca il 2026-10-15** *(12:43)*: *«a `theta = pi` **OGNI PEZZO**
> coincide **AL BIT** con l'operatore di `717bb60` (involuzioni). Il passo intero palindromo
> **NON** si confronta al bit col passo di `717bb60`: riporta la loro distanza su 250 tick
> **come informazione, non come criterio**.»*

## ⛔ PERCHE' E' STATO RIFORMULATO — **un mio errore, e vale scriverlo qui**

### **La prima versione pretendeva il PASSO INTERO al bit.** ### ⚠ **E quella, insieme a
`M-B2`, era impossibile:** `M-B2` chiede una composizione **di secondo ordine**, cioe'
**palindroma**, e un passo palindromo **non e'** il passo di `717bb60` *(i pezzi non
commutano)*.
### ⛔ **I due criteri si escludevano, e io li avevo riportati dalla mappa SENZA
CONTROLLARLI** — me ne sono accorto **solo dopo averli misurati entrambi.**
### ✅ **La riformulazione e' di Luca:** il raccordo si misura **dove ha senso**, cioe'
### **sui PEZZI**, che sono le involuzioni di prima.

## ⭐ COME

### **Per ogni pezzo, UNA applicazione sola** su una scena a `dtau = 1` *(cioe'
`theta = pi`)*, e si confrontano **i BYTE GREZZI** di `psi_h` e `phi_h`.
### 📌 **E i pezzi sono TUTTI SEI**, non i quattro cambiati: ### **la moneta e la
saturazione sono il CONTROLLO** — non sono stati toccati, quindi **devono** coincidere, e se
non coincidessero vorrebbe dire che ho cambiato qualcosa che non volevo cambiare.

### ⛔ **E il <<prima>> si prende da un `git worktree`** del commit, non da una copia nel
file: in un albero nudo `_presidio` ### **rifiuta di girare**, e ha ragione.

## 📌 LA CONFIGURAZIONE INTERA E' NELLE COSTANTI DEL MODULO

### `DTAU`, `TICK`, `SCENE`, `NORMA`, `VUOTO_MODULO`, `SU2`: **tutte in cima e tutte
stampate**, che e' cio' che il presidio dei referti pretende.
### ⚠ **E `dtau = 1.0` NON e' un numero scelto: e' `dtau_rif`**, l'unita' del raccordo.

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

DTAU = 1.0
TICK = 250
SCENE = ((16, 7), (12, 11))
NORMA = "locale"
VUOTO_MODULO = 2.0
SU2 = True
# ### ⛔ **I SEI PEZZI, per `id` di legge**: i quattro cambiati ### **piu- i due di
# ### controllo** *(la moneta e la saturazione, che non sono stati toccati)*.
PEZZI = ("CAMM-GROVER", "CAMM-SPOSTAMENTO", "CAMM-GROVER-VUOTO",
         "CAMM-SPOSTAMENTO-VUOTO", "CAMM-MONETA-SPIN", "CAMM-SATURAZIONE")


def timbra(b):
    return hashlib.sha1(b).hexdigest()[:12]


def _byte(st):
    return (np.ascontiguousarray(st["psi_h"]).tobytes()
            + np.ascontiguousarray(st["phi_h"]).tobytes())


def un_pezzo(idl, nn, seme):
    """### I byte dopo **UNA** applicazione del pezzo `idl`, a `theta = pi`."""
    import deriva as DV
    nome, vuole_par = DV.OPERATORE[idl]
    _i, mot, st, par = DV.scena(nn, seme, DTAU, norma=NORMA,
                                vuoto_modulo=VUOTO_MODULO, su2=SU2)
    mot.apri_tick()
    mot.operatori[nome](st, par if vuole_par else {}, 1)
    mot.chiudi_tick()
    return _byte(st)


def il_passo(nn, seme):
    """### I byte dopo `TICK` tick del passo **intero**, qualunque sia l'ordine."""
    import deriva as DV
    _i, mot, st, par = DV.scena(nn, seme, DTAU, norma=NORMA,
                                vuoto_modulo=VUOTO_MODULO, su2=SU2)
    for _t in range(TICK):
        DV.tick(st, mot, par)
    return _byte(st), (st["psi_h"].copy(), st["phi_h"].copy())


def scrivi(dove):
    """### Scrive i byte di **ogni pezzo** e del **passo intero**, durante la corsa."""
    import composizione as CM
    with open(dove, "wb") as f:
        f.write(len(CM.ORDINE).to_bytes(4, "little"))
        f.write(CM.IMPRONTA.encode("ascii"))
        print("  l'ordine di questo albero: %d pezzi, impronta %s"
              % (len(CM.ORDINE), CM.IMPRONTA))
        for nn, seme in SCENE:
            for idl in PEZZI:
                b = un_pezzo(idl, nn, seme)
                f.write(len(b).to_bytes(8, "little"))
                f.write(b)
                f.flush()
                print("    nn=%-4d seme=%-4d %-24s sha1-BYTE %s"
                      % (nn, seme, idl, timbra(b)))
            b, dati = il_passo(nn, seme)
            f.write(len(b).to_bytes(8, "little"))
            f.write(b)
            np.save(dove + ".psi.%d.%d.npy" % (nn, seme), dati[0])
            np.save(dove + ".phi.%d.%d.npy" % (nn, seme), dati[1])
            f.flush()
            print("    nn=%-4d seme=%-4d %-24s sha1-BYTE %s"
                  % (nn, seme, "(il passo intero)", timbra(b)))
    return 0


def _albero_vecchio(commit, dove):
    """### Un **`git worktree`** di `commit`, ### **e NON un albero nudo.**

    ### ⛔ **UN ALBERO NUDO NON BASTA, e l-ho misurato:** `git archive` da' i file ma
    **non un repo**, e li' `_presidio` ### **RIFIUTA DI GIRARE** -- la barriera vede
    `core.hooksPath` non impostato e si ferma. ### ✅ **E ha ragione:** un misuratore che
    gira dove i presidi non esistono ### **misurerebbe senza sorveglianza.**
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


def _leggi(dove):
    """### `(n_pezzi, impronta, [blocchi])` dal file scritto da `scrivi`."""
    b = open(dove, "rb").read()
    n = int.from_bytes(b[:4], "little")
    imp = b[4:20].decode("ascii")
    k = 20
    fuori = []
    while k < len(b):
        L = int.from_bytes(b[k:k + 8], "little")
        k += 8
        fuori.append(b[k:k + L])
        k += L
    return n, imp, fuori


def contro(commit):
    """### Il confronto **pezzo per pezzo**, piu' la distanza del passo intero."""
    radice = os.path.dirname(_QUI)
    fuori = os.path.join(os.environ.get("TEMP", radice), "mb1")
    if not os.path.isdir(fuori):
        os.makedirs(fuori)
    vecchio = _albero_vecchio(commit, os.path.join(fuori, "albero"))
    qui, la = os.path.join(fuori, "ora.bin"), os.path.join(fuori, "prima.bin")
    print("### (1) QUESTO ALBERO:")
    scrivi(qui)
    shutil.copyfile(os.path.abspath(__file__),
                    os.path.join(vecchio, "primo_ordine", "_misura_mb1.py"))
    print("### (2) %s, dal worktree:" % commit[:7])
    r = subprocess.run([sys.executable, os.path.join("primo_ordine", "_misura_mb1.py"),
                        "--scrivi", la], cwd=vecchio, capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace"))
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-3000:])
        print("### ⛔ la corsa su %s e' FALLITA" % commit[:7])
        return 1
    na, ia, ba = _leggi(qui)
    nb, ib, bb = _leggi(la)
    print("-" * 96)
    print("  l'ORDINE: adesso %d pezzi (impronta %s) -- %s %d pezzi (impronta %s)"
          % (na, ia, commit[:7], nb, ib))
    assert len(ba) == len(bb), (len(ba), len(bb))
    # ### ⭐ **IL CRITERIO: i PEZZI.** L-ultimo blocco di ogni scena e- il passo intero,
    # ### ### **e NON e- un criterio**: e- un numero da riportare.
    quanti, rotti = 0, []
    k = 0
    for nn, seme in SCENE:
        for idl in PEZZI:
            quanti += 1
            if ba[k] != bb[k]:
                rotti.append((nn, seme, idl))
            k += 1
        k += 1  # ### il passo intero, che NON e- un criterio
    print("-" * 96)
    if rotti:
        print("### ⛔ `M-B1` FALLISCE: %d pezzi su %d NON coincidono al bit: %s"
              % (len(rotti), quanti, rotti))
    else:
        print("### ✅ `M-B1` PASSA: TUTTI i %d pezzi coincidono AL BIT (6 pezzi x %d scene)"
              % (quanti, len(SCENE)))
    # ------------------------------------------------- l-INFORMAZIONE, non il criterio
    print("-" * 96)
    print("### 📌 INFORMAZIONE (NON un criterio): la distanza fra il passo PALINDROMO di")
    print("###   adesso e il passo di %s, su %d tick." % (commit[:7], TICK))
    for nn, seme in SCENE:
        pa = np.load(qui + ".psi.%d.%d.npy" % (nn, seme))
        pb = np.load(la + ".psi.%d.%d.npy" % (nn, seme))
        fa = np.load(qui + ".phi.%d.%d.npy" % (nn, seme))
        fb = np.load(la + ".phi.%d.%d.npy" % (nn, seme))
        dp = float(np.max(np.abs(pa - pb)))
        df = float(np.max(np.abs(fa - fb)))
        sc = max(float(np.max(np.abs(pb))), float(np.max(np.abs(fb))))
        print("###   nn=%-4d seme=%-4d  max|d psi| = %.6e   max|d phi| = %.6e"
              "   su scala %.3e" % (nn, seme, dp, df, sc))
    print("###   E NON E' UN DIFETTO: i pezzi NON COMMUTANO, quindi una composizione")
    print("###   palindroma NON PUO' dare il passo di una composizione che non lo era.")
    return 1 if rotti else 0


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if argv and argv[0] == "--scrivi":
        return scrivi(argv[1])
    print("=" * 96)
    print("M-B1: IL RACCORDO AL BIT, PEZZO PER PEZZO -- dtau = dtau_rif = %.1f" % DTAU)
    print("=" * 96)
    print("  LA CONFIGURAZIONE: dtau = %.1f   tick = %d   scene = %s   norma = %s"
          "   vuoto_modulo = %.1f   su2 = %s" % (DTAU, TICK, SCENE, NORMA,
                                                 VUOTO_MODULO, SU2))
    if argv and argv[0] == "--contro":
        return contro(argv[1])
    scrivi(os.path.join(os.environ.get("TEMP", "."), "mb1_solo.bin"))
    print("### ⚠ senza `--contro <commit>` questa e' UNA SOLA corsa: nessun confronto")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
