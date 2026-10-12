# -*- coding: utf-8 -*-
"""SOTTO-PEZZO `5c` DEL MOTORE — **CHECKPOINT E RIPRESA, e la ripresa coincide AL BIT.**

> ### ⛔ **Il mandato, alla lettera:** *«checkpoint e ripresa, salvataggio durante la
> corsa»*.

## ⭐ CHE COSA MANCAVA, E PERCHE' NON BASTAVA `timbro.py`

`timbro.py` ha gia' **`scrivi_atomico`**, **`salva`** e **`riprendi`**, e **si riusano** —
non si riscrivono. ### ⛔ **Ma salvano LO STATO e non IL GRAFO**, e **senza il grafo una
ripresa non vuol dire niente**: lo stato della camminata e' **dimensionato da `2m`**, e
riprendere lo stesso stato su **un altro grafo** sarebbe **un'altra corsa che sembra la
stessa misura** — che e' esattamente cio' che la ripresa rifiuta per la tabella.

### ✅ **QUINDI QUI SI SALVANO TRE COSE, e tutte e tre per la stessa ragione:**

| | che cosa | perche' **senza di lei la ripresa mente** |
|---|---|---|
| `1` | **lo stato** *(`psi_h`, `phi_h`, …)* | e' il dato della corsa |
| `2` | **il grafo** *(`ii`, `jj`, `n`, la capacita')* | lo stato **e' dimensionato da lui**: un grafo diverso ⟹ **un'altra corsa** |
| `3` | **la geometria** *(`n` per estremita', `U` per arco)* e **`dtau`** | la camminata **ci legge dentro a ogni tick**: una geometria diversa ⟹ **un'altra fisica** |
| `4` | **i contatori** *(ripieghi, crescite, tick, applicazioni, archi nati e morti)* | ### **un contatore che riparte da zero DICE UNA COSA FALSA** sulla corsa che continua |

### ⚠ **E LA GEOMETRIA SI SALVA INVECE DI CHIEDERLA DI NUOVO**, di proposito: chiederla
vorrebbe dire **fidarsi che chi riprende passi la stessa** — e ### **una ripresa che si
fida non e' una ripresa, e' una speranza.**

## ⛔ IL PREFISSO RISERVATO, E IL SUO PRESIDIO

Grafo, geometria e contatori vivono **nello stesso `npz`** dello stato, sotto il prefisso
**`__mot__`**. ### ⚠ **E un nome di stato che cominciasse con quel prefisso
sovrascriverebbe un pezzo del motore in silenzio:** quindi **si controlla**, e
### **un nome che collide ALZA.**

Gira con:  python primo_ordine/checkpoint.py   (il giro salva-riprendi, misurato)
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import incidenza as IN                                        # noqa: E402
import motore as MO                                           # noqa: E402
import timbro as TI                                           # noqa: E402

# ### ⛔ **IL PREFISSO RISERVATO.** Doppio underscore ai due lati: nessun nome di
# ### variabile della tabella lo usa, ### **e un controllo lo pretende** invece di
# ### fidarsi.
RISERVATO = "__mot__"

# ### ⚠ **I CONTATORI CHE DEVONO SOPRAVVIVERE, DICHIARATI UNO A UNO.** ### **Non si
# ### scoprono guardando gli attributi**: un attributo nuovo che nessuno ha deciso di
# ### salvare ### **sparirebbe alla ripresa senza che nessuno lo veda.**
CONTATORI_MOTORE = ("ripieghi", "cresciute", "tick")
CONTATORI_GRAFO = ("ripieghi", "archi_nati", "archi_morti")


def _controlla_nomi(st):
    """### Nessun nome di stato usa il prefisso riservato. ### **Si controlla, non si
    spera.**"""
    cattivi = [k for k in st if str(k).startswith(RISERVATO)]
    assert not cattivi, (
        "i nomi %r cominciano col prefisso riservato %r, e sovrascriverebbero un pezzo"
        " del motore IN SILENZIO: il prefisso si cambia qui, oppure la tabella rinomina"
        " quelle variabili" % (cattivi, RISERVATO))


def _impacchetta(mot):
    """### Lo stato **piu'** grafo, geometria e contatori, ### **in un dizionario solo.**"""
    _controlla_nomi(mot.st)
    d = dict(mot.st)
    inc, geo = mot.inc, mot.geo
    d[RISERVATO + "ii"] = inc.ii.copy()
    d[RISERVATO + "jj"] = inc.jj.copy()
    # ### ⚠ **`n`, `m` e la CAPACITA- sono SCALARI, e si salvano come array di uno:** un
    # ### `npz` tiene array, e ### **un array di uno e- piu- onesto di una stringa.**
    d[RISERVATO + "n"] = np.array([inc.n], dtype=IN.INDICE)
    d[RISERVATO + "capacita"] = np.array([inc.capacita], dtype=IN.INDICE)
    d[RISERVATO + "versori"] = geo.n.copy()
    d[RISERVATO + "trasporto"] = geo.U.copy()
    d[RISERVATO + "dtau"] = mot.dtau.copy()
    # ### la sommatoria e- una SCELTA, e una scelta che non si riprende
    # ### ### **cambierebbe i numeri senza che nessuno l-abbia deciso**
    d[RISERVATO + "sommatoria"] = np.array([MO.SOMMATORIE.index(mot.sommatoria)],
                                           dtype=IN.INDICE)
    d[RISERVATO + "cont_mot"] = np.array([getattr(mot, c) for c in CONTATORI_MOTORE],
                                          dtype=IN.INDICE)
    d[RISERVATO + "cont_gra"] = np.array([getattr(inc, c) for c in CONTATORI_GRAFO],
                                          dtype=IN.INDICE)
    d[RISERVATO + "applicazioni"] = np.array(
        [mot.applicazioni[o] for o in MO.OPERATORI], dtype=IN.INDICE)
    return d


def salva(percorso, mot, passo, config, impronta_config):
    """### Salva **tutto**, con la scrittura atomica di `timbro.py`.

    ### ⭐ **E il TIMBRO lo fa `timbro.salva`**, che riusiamo: l'impronta della tabella,
    dei generati e della configurazione **sta la'**, e ### **averne due copie vorrebbe
    dire che una delle due resta indietro.**
    """
    return TI.salva(percorso, _impacchetta(mot), passo, config, impronta_config)


def riprendi(percorso, config, impronta_config):
    """### `(motore, passo)`, e ### **RIFIUTA se manca un pezzo.**

    ### ⛔ **Il rifiuto sulla TABELLA lo fa gia' `timbro.riprendi`**, e non si duplica:
    riprendere con una tabella diversa **continua una corsa che non e' quella**.
    ### ✅ **Qui si aggiunge il rifiuto sul GRAFO**: un file senza il grafo **non e' un
    checkpoint di una camminata**, e provare a indovinarlo sarebbe **inventare la scena.**
    """
    d, passo = TI.riprendi(percorso, config, impronta_config)
    manca = [k for k in ("ii", "jj", "n", "capacita", "versori", "trasporto", "dtau",
                         "sommatoria") if (RISERVATO + k) not in d]
    assert not manca, (
        "nel checkpoint `%s` mancano %r: uno stato senza il suo GRAFO e la sua GEOMETRIA"
        " non e' il checkpoint di una camminata, e indovinarli vorrebbe dire INVENTARE"
        " LA SCENA" % (percorso, manca))
    inc = IN.Incidenza(d[RISERVATO + "ii"], d[RISERVATO + "jj"],
                       int(d[RISERVATO + "n"][0]),
                       capacita=int(d[RISERVATO + "capacita"][0]))
    geo = MO.Geometria(d[RISERVATO + "versori"], d[RISERVATO + "trasporto"])
    st = dict((k, v) for k, v in d.items() if not str(k).startswith(RISERVATO))
    mot = MO.Motore(inc, geo, st, d[RISERVATO + "dtau"],
                    MO.SOMMATORIE[int(d[RISERVATO + "sommatoria"][0])])
    # ### ⛔ **E I CONTATORI SI RIMETTONO, perche' un contatore che riparte da zero
    # ### ### **dice una cosa falsa** sulla corsa che continua.** ### ⚠ **Tranne i
    # ### RIPIEGHI DEI BUFFER**: quelli ### **ricominciano davvero**, perche' i buffer
    # ### del processo nuovo ### **non esistono ancora** -- e dire il contrario
    # ### ### **nasconderebbe le allocazioni della ripresa.**
    cm = d.get(RISERVATO + "cont_mot")
    if cm is not None:
        for nome, val in zip(CONTATORI_MOTORE, cm.tolist()):
            if nome == "ripieghi":
                # ### il ramo RIPIEGHI: ### **NON si rimette**, ed e' dichiarato sopra
                continue
            setattr(mot, nome, int(val))
    cg = d.get(RISERVATO + "cont_gra")
    if cg is not None:
        for nome, val in zip(CONTATORI_GRAFO, cg.tolist()):
            setattr(inc, nome, int(val))
    ap = d.get(RISERVATO + "applicazioni")
    if ap is not None:
        for nome, val in zip(MO.OPERATORI, ap.tolist()):
            mot.applicazioni[nome] = int(val)
    return mot, passo


class Salvataggi(object):
    """### Il salvataggio **DURANTE la corsa**: ogni `ogni` tick, e **non piu' spesso.**

    ### ⛔ **`ogni` NON ha un valore di comodo**, e il motivo e' che **salvare costa**:
    un `npz` di una scena grande e' **centinaia di MB**, e chi misura **deve scegliere**
    quanto spesso pagarlo. ### **Un default qui sarebbe una scelta mia che nessuno vede.**

    ### ⚠ **E il conto si tiene sui TICK DEL MOTORE, non su una variabile mia:** due
    contatori della stessa cosa **divergono**.
    """

    def __init__(self, percorso, ogni, config, impronta_config):
        assert int(ogni) >= 1, (
            "`ogni` e' un numero di tick e vale almeno 1: con %r non si salverebbe mai,"
            " e <<mai>> si scrive non chiamando questa classe" % (ogni,))
        self.percorso = percorso
        self.ogni = int(ogni)
        self.config = config
        self.impronta_config = impronta_config
        self.salvati = 0
        self._ultimo = None

    def forse(self, mot, passo):
        """### Salva **se e' il momento**, e torna `True` se ha salvato."""
        if mot.tick == self._ultimo or (mot.tick % self.ogni) != 0:
            # ### il ramo NON E- IL MOMENTO, e il primo pezzo della condizione e-
            # ### ### **contro il doppio salvataggio**: chiamare `forse` due volte nello
            # ### stesso tick ### **non deve salvare due volte**, e la seconda scrittura
            # ### ### **costerebbe come la prima.**
            return False
        salva(self.percorso, mot, passo, self.config, self.impronta_config)
        self.salvati += 1
        self._ultimo = mot.tick
        return True


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    import time
    import stato as ST
    print("=" * 96)
    print("IL GIRO SALVA-RIPRENDI -- il costo, MISURATO")
    print("=" * 96)
    cfg, imp = {"prova": True}, "prova"
    for nn in (256, 4096):
        ii = np.arange(nn, dtype=IN.INDICE)
        jj = (ii + 1) % nn
        inc = IN.Incidenza(ii, jj, nn, capacita=nn)
        nv = np.zeros((2 * inc.m, 3), dtype=float)
        nv[:, 2] = 1.0
        U = np.zeros((inc.m, 2, 2), dtype=complex)
        U[:, 0, 0] = 1.0
        U[:, 1, 1] = 1.0
        st = ST.nuovo(nn, inc.m)
        st["psi_h"][0, 0] = 1.0
        mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.1), "numpy")
        p = os.path.join(os.environ.get("TEMP") or ".", "_chk_%d.npz" % nn)
        t0 = time.perf_counter()
        salva(p, mot, 7, cfg, imp)
        ts = time.perf_counter() - t0
        t0 = time.perf_counter()
        riprendi(p, cfg, imp)
        tr = time.perf_counter() - t0
        byte = os.path.getsize(p)
        for q in (p, p + ".timbro.json"):
            if os.path.exists(q):
                os.remove(q)
        print("  n=%-6d m=%-6d  salva %7.2f ms   riprendi %7.2f ms   file %9d byte"
              % (nn, inc.m, ts * 1e3, tr * 1e3, byte))
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
