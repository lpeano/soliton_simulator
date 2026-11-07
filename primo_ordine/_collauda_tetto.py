# -*- coding: utf-8 -*-
"""`D2-T` — **IL CONTROLLO DEL TETTO DI `Omega` CON LA TOLLERANZA DERIVATA** [[TETTO-OMEGA-SENZA-ARROTONDAMENTO]]

> ### ⛔ **La cura del `2026-11-07`** *(Luca `10:06`, la decisione `1`; il task history
> `doc/TASK_HISTORY/2026-11-07_cura_tetto_omega.md`, sez. `6`)*: `controlla_tetto` ammette
> ### **`(gamma_p + gamma_q) / (1 - gamma_q) tetto_k`**, `p = d + 7`, `q = d + 8`, **CONTATI
> dal codice** *(le profondita' delle due catene dopo le foglie comuni)*: ### **con `d = 6`
> circa `27 u`.** **Non e' una soglia scelta: e' l'errore in avanti.**

## I CASI *(fissati prima: la sez. `6.3` del task history)*

- **(a)** il fattore a `d = 6` e' `(gamma_13 + gamma_14) / (1 - gamma_14)`, **fra `27 u` e
  `27 u (1 + 1e-12)`**;
- **(b)** un tetto ESATTO superato di **un ulp** *(il caso di IS3)*: ### **NON alza**;
- **(c)** ### **DEVE FALLIRE:** un eccesso di un fattore `1 + 1e-12` *(un tetto sbagliato,
  l'errore `n.17` in piccolo)*: ### **ALZA**;
- **(d)** il confine: `0.5` volte la tolleranza **non alza**, `2` volte **alza**;
- **(e)** ### **DEVE FALLIRE:** il controllo VECCHIO *(tolleranza zero)* sul caso **(b)**
  ALZA -- **il caso (b) ha materia.**

Gira con:  python primo_ordine/_collauda_tetto.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import energia_pesata as EP                                   # noqa: E402

OK = [0, 0]
U = float(np.finfo(float).eps) / 2.0
GRADO = 6                     # ### i triangoli: ogni nodo ha grado `6`
TETTO = 8.011061e-01          # ### la scala del caso di IS3 (`TT-M`): un numero qualunque del suo ordine


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-90s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))


def alza(omega_k, tetto_k):
    try:
        EP.controlla_tetto(omega_k, tetto_k, GRADO, "collaudo")
        return False
    except AssertionError:
        return True


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("D2-T: IL CONTROLLO DEL TETTO DI `Omega` CON LA TOLLERANZA DERIVATA (grado %d)" % GRADO)
    print("=" * 100)
    f = EP.ulp_del_tetto(GRADO)
    esito("(a) il fattore a d = %d fra 27 u e 27 u (1 + 1e-12)" % GRADO, 27 * U <= f <= 27 * U * (1 + 1e-12), "%.6f u" % (f / U))
    t = np.full(4, TETTO)
    om = t.copy()
    om[2] = np.nextafter(TETTO, 2.0)
    esito("(b) un tetto ESATTO superato di UN ulp NON alza", not alza(om, t), "eccesso %.3e" % (om[2] - TETTO))
    om_f = t * (1.0 + 1e-12)
    esito("### (c) DEVE FALLIRE: un eccesso di un fattore 1 + 1e-12 ALZA", alza(om_f, t), "")
    esito("(d) 0.5 volte la tolleranza NON alza", not alza(t * (1.0 + 0.5 * f), t), "")
    esito("(d) 2 volte la tolleranza ALZA", alza(t * (1.0 + 2.0 * f), t), "")
    vecchio = float(np.max(np.abs(om) - t)) <= 0.0
    esito("### (e) DEVE FALLIRE: il controllo VECCHIO (tolleranza zero) sul caso (b) ALZA", not vecchio, "")
    try:
        EP.controlla_tetto(om_f, t, GRADO, "collaudo")
        msg = ""
    except AssertionError as e:
        msg = str(e)
    esito("(f) il messaggio nomina la tolleranza e il grado", "tolleranza" in msg and "grado 6" in msg, msg[:80])
    print("=" * 100)
    print("D2-T: %d su %d  %s" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
