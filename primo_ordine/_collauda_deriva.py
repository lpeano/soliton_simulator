# -*- coding: utf-8 -*-
r"""IL COLLAUDO DELLA DERIVA — **e presidia soprattutto che la misura ABBIA MATERIA.**

### ⛔ **IL DIFETTO CHE QUESTO COLLAUDO IMPEDISCE E' UN FALSO-ZERO, e l'ho fatto:** la
prima versione della misura normalizzava `psi` su tutto il grafo, e allora
`x = |h_k|/Lambda_k ~ 1/(2m)`. Siccome `G(x) = x - arctan x` va come `x^3/3`, il termine
del vuoto valeva **`~1e-5`**: ### **la saturazione era PRATICAMENTE SPENTA, e una
<<conservazione>> misurata la' non distingue <<`E` si conserva>> da <<il termine non
c'e'>>.**

### ⭐ **Quindi il braccio `1` non e' un contorno: e' il braccio PIU' IMPORTANTE.**

| | il braccio | che cosa **esclude** |
|---|---|---|
| `1` | **MATERIA**: nel regime di misura `x` e' di ordine `1`, non `1e-3` | ### **il FALSO-ZERO**: la saturazione spenta |
| `2` | il **primo termine** e' conservato **esattamente** dal solo pezzo lineare | che `E` non sia quella che credo |
| `3` | ### ⛔ **DEVE CAMBIARE:** il primo termine **sotto `N`** | che il braccio `2` passi perche' **niente si muove** |
| `4` | `Lambda_k` e' **esattamente invariante** sotto la camminata del vuoto, con `|phi|` uniforme | che la decomposizione di `(c)` dica qualcosa quando **non dice niente** |
| `5` | ### ⛔ **DEVE CAMBIARE:** la stessa cosa con `|phi|` **non uniforme** | che il braccio `4` sia un **FALSO-ZERO dello strumento** |
| `6` | la **sorgente per nodo** e' **`O(1)` in `dtau`**, non `O(dtau^2)` | — |
| `7` | ### ⛔ **DEVE FERMARE:** una legge dell'ordine di composizione **non mappata** | che un pezzo del tick **non giri in silenzio** |

Gira con:  python primo_ordine/_collauda_deriva.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import composizione as CM                                     # noqa: E402
import deriva as DV                                           # noqa: E402
import energia as EN                                          # noqa: E402

OK = [0, 0]
EPS = float(np.finfo(float).eps)
# ### ⚠ **LE SOGLIE, FISSATE QUI:** una soglia dentro un braccio e' ### **una soglia che
# ### si puo- aggiustare dopo aver visto il numero.**
X_MINIMO = 0.1          # ### sotto questo la saturazione e- SPENTA: falso-zero
ULP_MAX = 1000.0
CAMBIA_MIN = 1e-6
RAPPORTO_O1 = 2.0       # ### `O(dtau^2)` darebbe `~4`; `O(1)` da- `~1`


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 96)
    print("IL COLLAUDO DELLA DERIVA: LA MATERIA PRIMA DI TUTTO, E I TRE CASI CHE DEVONO"
          " CAMBIARE")
    print("=" * 96)

    # ### (1) LA MATERIA: `x` di ordine `1` nel regime di misura
    _i, mot, st, _p = DV.scena(16, 7, 0.2, norma="locale", vuoto_modulo=2.0)
    x = DV.satura(st, mot)
    esito("### (1) MATERIA: nel regime di misura `x = |h|/Lambda` e- di ordine 1",
          x >= X_MINIMO, "x_max = %.4f   (sotto %.2f sarebbe un FALSO-ZERO)"
          % (x, X_MINIMO))
    _i2, mot2, st2, _p2 = DV.scena(16, 7, 0.2, norma="globale")
    x2 = DV.satura(st2, mot2)
    esito("### (1-bis) e il regime `globale` E- quello vacuo, come dichiarato",
          x2 < X_MINIMO, "x_max = %.5f: la- `G ~ x^3/3 ~ 0`" % x2)

    # ### (2) il PRIMO termine sotto il SOLO pezzo lineare: un-IDENTITA-
    _i3, mot3, st3, par = DV.scena(16, 7, 0.2, norma="locale", vuoto_modulo=2.0)
    p0, _v0 = DV.due_termini(st3, mot3, par)
    mot3.apri_tick()
    for nome in ("moneta_spin", "grover", "spostamento_trasporto"):
        mot3.operatori[nome](st3, par if nome == "moneta_spin" else {}, 1)
    mot3.chiudi_tick()
    p1, _v1 = DV.due_termini(st3, mot3, par)
    d = abs(p1 - p0)
    ulp = d / (EPS * max(abs(p0), 1.0))
    esito("### (2) il PRIMO termine: il pezzo lineare lo conserva ESATTAMENTE",
          ulp < ULP_MAX, "|Delta| = %.3e su %.4f  (%.1f ulp)" % (d, p0, ulp))

    # ### (3) DEVE CAMBIARE: lo stesso termine sotto `N`
    _i4, mot4, st4, par4 = DV.scena(16, 7, 0.2, norma="locale", vuoto_modulo=2.0)
    q0, _w0 = DV.due_termini(st4, mot4, par4)
    mot4.apri_tick()
    mot4.operatori["CAMM-SATURAZIONE"](st4, {}, 1)
    mot4.chiudi_tick()
    q1, _w1 = DV.due_termini(st4, mot4, par4)
    esito("### (3) DEVE CAMBIARE: il primo termine sotto `N` NON e- conservato",
          abs(q1 - q0) > CAMBIA_MIN,
          "|Delta| = %.3e: senza questo il braccio (2) sarebbe un FALSO-UNO"
          % abs(q1 - q0))

    # ### (4) e (5) `Lambda` sotto la camminata del vuoto, nei due casi
    lu = DV.lambda_sotto_vuoto(uniforme=True)
    lnu = DV.lambda_sotto_vuoto(uniforme=False)
    esito("### (4) con `|phi|` UNIFORME `Lambda_k` e- esattamente invariante",
          lu < 1e-12, "max |Delta Lambda| = %.3e" % lu)
    esito("### (5) DEVE CAMBIARE: con `|phi|` NON uniforme",
          lnu > CAMBIA_MIN, "max |Delta Lambda| = %.3e: la misura SA vedere" % lnu)

    # ### (6) la SORGENTE per nodo e- `O(1)` in `dtau`
    mm = []
    for dt in (0.2, 0.05):
        s, _dE, _po, _sa = DV.sorgente_per_nodo(dtau=dt, vuoto_modulo=2.0)
        mm.append(float(np.max(np.abs(s))))
    rap = mm[0] / mm[1] if mm[1] > 0 else float("inf")
    esito("### (6) la SORGENTE per nodo e- `O(1)` in `dtau`, non `O(dtau^2)`",
          rap < RAPPORTO_O1,
          "rapporto su un fattore 4 di `dtau`: %.3f  (`O(dtau^2)` darebbe ~16)" % rap)

    # ### (7) DEVE FERMARE: una legge dell-ordine NON mappata
    salvato = dict(DV.OPERATORE)
    rotto = False
    try:
        DV.OPERATORE.pop(CM.ORDINE[2][0])
        _i5, mot5, st5, par5 = DV.scena(8, 7, 0.2)
        DV.tick(st5, mot5, par5)
    except AssertionError:
        rotto = True
    finally:
        DV.OPERATORE.clear()
        DV.OPERATORE.update(salvato)
    esito("### (7) DEVE FERMARE: una legge dell-ordine di composizione non mappata",
          rotto, "un pezzo del tick che non gira e- un tick diverso")

    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
