# -*- coding: utf-8 -*-
r"""**LE POSIZIONI E LA SCENA CHE CRESCE** *(il ramo `mitosi`, B4; mandato di Luca `2026-11-20` `10:31`; la carta della mitosi sez. `0`, `5`)*.

**Che cosa assumeva la scena** *(`mattone.scena`, `convergenza.scena_L`)*: `m1 = v // L`, `m2 = v % L` *(gli INDICI del toro come coordinate)*, `righe = argsort(nodo).reshape(n, 6)` *(il grado `6`)*, e i vettori per estremita' del bordo *(`g_e`, `phi_v`)* della taglia di oggi.
**Che cosa fa questo modulo:**
- **`righe(inc)`:** la matrice `n x 6` **dalla CSR del nucleo** *(`inc.estremita`, che E' `argsort(nodo, kind="stable")`: `incidenza._derivati`)*; **se un nodo NON ha grado `6`, RIFIUTA** *(la matrice non esiste)*;
- **`nuova(m1, m2, i, j, L)`:** **la posizione del nodo nato sull'arco `i -> j`: il PUNTO MEDIO**, con l'immagine piu' vicina sul toro *(le coordinate in unita' di `A1`, `A2`, come `m1`, `m2`: `toro.scarti` e `toro.centro` le accettano non intere)*;
- **`cresci(Z, i, j, dove)`:** dopo `Motore.cresci`, **la scena segue il grafo:** `n`, `nodo`, le posizioni *(da qui in poi FLOAT)*, `g_e` *(il bordo e' TOLTO: si accetta solo `g_e = 0`, e le estremita' nuove a `0` = nessun bordo)*; ### **cio' che NON puo' crescere RIFIUTA da qui in poi** *(`Rifiutato`)*: `righe` *(il grado non e' piu' `6`)*, `phi_v` *(il vuoto di riferimento del bordo)*, `stato` e `metti` *(lo stato di partenza della scena, della taglia vecchia)*, `g_nodo`.
**Perche' rifiutare e non lasciare:** un array della taglia vecchia **indicizza in silenzio** *(un indice dentro la taglia vecchia non da' errore)*: **un dato scaduto e' peggio di un errore.**
"""
import numpy as np


class Rifiutato(object):
    """### Un dato della scena che dopo la crescita NON esiste piu': ogni uso alza, col perche'."""

    def __init__(self, nome, perche):
        self.nome, self.perche = nome, perche

    def _alza(self, *_a, **_k):
        raise RuntimeError("Z[%r] non esiste dopo la crescita del grafo: %s" % (self.nome, self.perche))

    __getitem__ = __setitem__ = __call__ = __len__ = __iter__ = __array__ = _alza

    def __getattr__(self, x):
        if x in ("nome", "perche"):
            raise AttributeError(x)
        self._alza()


def righe(inc):
    """### `n x 6` dalla CSR del nucleo; RIFIUTA se un nodo non ha grado `6`."""
    g = np.asarray(inc.grado)
    if not np.all(g == 6):
        raise RuntimeError("righe: il grafo non e' regolare di grado 6 (gradi %s): la matrice n x 6 non esiste" % sorted(set(g.tolist())))
    return np.asarray(inc.estremita).reshape(inc.n, 6)


def nuova(m1, m2, i, j, L):
    """### Il punto medio dell'arco `i -> j`, con l'immagine piu' vicina, riportato in `[0, L)`."""
    d1 = ((float(m1[j]) - float(m1[i]) + 0.5 * L) % L) - 0.5 * L
    d2 = ((float(m2[j]) - float(m2[i]) + 0.5 * L) % L) - 0.5 * L
    return (float(m1[i]) + 0.5 * d1) % L, (float(m2[i]) + 0.5 * d2) % L


RIFIUTATI = {
    "righe": "il grado non e' piu' 6 (la CSR e' inc.offset, inc.estremita)",
    "phi_v": "il vuoto di riferimento del bordo e' della taglia vecchia (il bordo e' tolto)",
    "stato": "lo stato di partenza della scena e' della taglia vecchia",
    "metti": "lo stato di partenza della scena e' della taglia vecchia: la scena non si rimette",
    "g_nodo": "il peso del bordo per nodo e' della taglia vecchia (il bordo e' tolto)",
}


def cresci(Z, i, j, nodi_nuovi):
    """### La scena dopo `Motore.cresci` (un nodo nuovo sull'arco `i -> j`): `n`, `nodo`, le posizioni, `g_e`; il resto RIFIUTA."""
    inc = Z["mot"].inc
    assert nodi_nuovi == 1, "una nascita per tick, un nodo (D-M4)"
    assert inc.n == Z["n"] + 1, "il grafo non e' cresciuto di un nodo: cresci va chiamato DOPO Motore.cresci"
    g = Z.get("g_e")
    if g is not None and not isinstance(g, Rifiutato):
        assert float(np.max(np.abs(g))) == 0.0, "il bordo NON e' tolto (g_e non nullo): la crescita col bordo non e' definita"
        Z["g_e"] = np.zeros(2 * inc.m, dtype=np.asarray(g).dtype)
    p1, p2 = nuova(Z["m1"], Z["m2"], i, j, Z["L"])
    Z["m1"] = np.concatenate([np.asarray(Z["m1"], dtype=float), [p1]])
    Z["m2"] = np.concatenate([np.asarray(Z["m2"], dtype=float), [p2]])
    Z["n"] = inc.n
    Z["nodo"] = np.asarray(inc.nodo)
    for k, perche in RIFIUTATI.items():
        if k in Z:
            Z[k] = Rifiutato(k, perche)
    Z["cresciuto"] = Z.get("cresciuto", 0) + 1
    return p1, p2
