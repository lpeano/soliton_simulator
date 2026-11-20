# -*- coding: utf-8 -*-
r"""**IL CONTATORE DEL LAPSE: LA MEMORIA PER ARCO `Theta`** *(il ramo `mitosi`; mandato di Luca `2026-11-20` `10:31`, TODO 3; l'innesco (a), la carta della mitosi sez. `15.1`)*.

**La definizione** *(Luca `2026-11-17` `21:00`; letta sul codice in `doc/referti_l2/torsione_tempo_proprio.py` del ramo `primo-ordine`, `dtau_nodo` e `ritmo`, sha1 dei byte `TORSIONE_SHA1` sotto)*:
`Theta_a += pi * (dtau_nodo_i - dtau_nodo_j)` a ogni tick, `i = ii[a]`, `j = jj[a]`, **`dtau_nodo = mot.dtau * cs`**, `cs` il lapse del punto fisso del tick *(`lapse_caldo.cs_prec()`)*; **`omega = pi`, `dtau_rif = 1` dal modello.** **L'arco scatta a `|Theta_a| >= 2 pi`.** **Dichiarato come contatore della deriva fra orologi vicini, NON come olonomia** *(14.6-bis)*.
**La crescita** *(S2 del `2026-11-17` `21:00`)*: **gli archi nuovi da `Theta = 0`; l'arco diviso e' CONSUMATO** *(tolto con la sua memoria)*. **Lo stato:** `Theta` si salva e si riprende con lo stato *(la chiave `theta_a`)*: **P8, la ripresa al bit.**
**L'ordine** *(la carta della mitosi sez. `7`, l'ordine delle operazioni)*: **gli archi che scattano si leggono ORDINATI PER INDICE** *(determinismo)*.
"""
import math

import numpy as np

TORSIONE_SHA1 = "doc/referti_l2/torsione_tempo_proprio.py sul ramo primo-ordine (il blob al commit 52caa06a; la formula copiata qui sotto, riga per riga)"
CHIAVE = "theta_a"
QUANTO = 2.0 * math.pi


def ritmo(mot, cs):
    """### `pi (dtau_nodo_i - dtau_nodo_j)` per arco: le righe di `torsione_tempo_proprio.dtau_nodo` e `ritmo`."""
    assert np.all(mot.dtau == 1.0), "mot.dtau non e' 1: la definizione va riletta (la carta della torsione sez. 1.2)"
    d = np.asarray(mot.dtau, dtype=float) * np.asarray(cs, dtype=float)
    nodo = np.asarray(mot.inc.nodo)
    return math.pi * (d[nodo[0::2]] - d[nodo[1::2]])


class Contatore(object):
    """### `Theta` per arco: si accumula a ogni tick, cresce con il grafo, si salva con lo stato."""

    def __init__(self, theta):
        self.theta = np.array(theta, dtype=float)

    @classmethod
    def da_segmenti(cls, acc):
        """### `Theta` dalla somma dei segmenti, NELL'ORDINE dato (sequenziale: le righe di `innesco_stima.py`, `np.sum(..., axis=0)`)."""
        t = np.array(acc[0], dtype=float)
        for a in acc[1:]:
            t = t + a
        return cls(t)

    def accumula(self, mot, cs):
        r = ritmo(mot, cs)
        assert r.shape == self.theta.shape, "Theta ha %d archi, il grafo %d: il contatore non ha seguito la crescita" % (self.theta.size, r.size)
        self.theta += r

    def scattati(self):
        """### Gli archi con `|Theta| >= 2 pi`, ordinati per indice."""
        return np.nonzero(np.abs(self.theta) >= QUANTO)[0]

    def cresci(self, tieni, nuovi):
        """### Dopo `Motore.cresci(tieni, ...)`: gli archi tenuti col loro `Theta`, nell'ordine; i `nuovi` da `0`; i tolti CONSUMATI."""
        tieni = np.asarray(tieni)
        assert tieni.dtype == bool and tieni.size == self.theta.size, "tieni: una maschera booleana sugli archi di prima"
        self.theta = np.concatenate([self.theta[tieni], np.zeros(int(nuovi))])

    def salva(self, dati):
        dati[CHIAVE] = self.theta.copy()
        return dati

    @classmethod
    def riprendi(cls, d):
        return cls(np.array(d[CHIAVE], dtype=float))
