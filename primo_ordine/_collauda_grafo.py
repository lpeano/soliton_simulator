# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL GRAFO VALIDO — **punto `4` della terza parte, nei DUE VERSI.**

### ⛔ **STA IN UN MODULO SUO, e me lo ha detto `P-MOD` rifiutando il commit:** il
collaudo deve costruire ### **lo stato come lo costruisce il driver**, quindi importa
`driver`, `passo`, `schema_config` e `stato` — e ### **`passo` importa `grafo`.**
### ⭐ **Dentro `grafo.py` quegli import sarebbero un CICLO**, e `P-MOD` lo rifiuta:
### **il collaudo di un modulo che sta IN FONDO alla catena degli import non puo- vivere
dentro quel modulo.** ### **E- lo stesso motivo per cui `_collauda_passo.py` esiste.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import driver as DRV                                        # noqa: E402
import grafo as GR                                          # noqa: E402
import passo as PA                                          # noqa: E402
import schema_config as CFG                                 # noqa: E402
import stato as ST                                          # noqa: E402

errori = GR.errori
controlla = GR.controlla
costo = GR.costo


def collaudo():
    import time
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEL GRAFO VALIDO -- nei DUE VERSI   (punto 4)")
    print("=" * 100)
    n = 9
    ii = np.arange(n - 1, dtype=int)
    jj = np.arange(1, n, dtype=int)
    print("  la scena della configurazione di prova: catena, %d nodi, %d archi"
          % (n, ii.size))
    print()
    # ------------------------------------------------------------------ il verso SANO
    esito("NON deve scattare: la CATENA del file di configurazione",
          errori(ii, jj, n, "prova") == [],
          "### se scattasse, sarebbe LA SCENA a essere sbagliata, non il presidio")
    ai = np.arange(n, dtype=int)
    aj = (np.arange(n, dtype=int) + 1) % n
    esito("NON deve scattare: l-ANELLO, l-altra scena del vocabolario",
          errori(ai, aj, n, "prova") == [],
          "### le DUE scene che `driver.py::grafo` sa costruire")
    esito("NON deve scattare: un grafo VUOTO",
          errori(np.array([], dtype=int), np.array([], dtype=int), n, "prova") == [],
          "### zero archi non e- un errore: e- `--nodi 0`, e il repo lo usa")
    # ------------------------------------------------------------------ i CINQUE casi
    esito("### DEVE scattare: un AUTO-ARCO",
          any("AUTO-ARCHI" in x for x in errori(
              np.append(ii, 3), np.append(jj, 3), n, "prova")),
          "### `i == j` non e- un accoppiamento: e- un termine di nodo TRAVESTITO")
    esito("### DEVE scattare: un DOPPIONE",
          any("DOPPI" in x for x in errori(
              np.append(ii, ii[0]), np.append(jj, jj[0]), n, "prova")),
          "### l-energia di quell-arco conterebbe DUE VOLTE")
    esito("### DEVE scattare: lo STESSO ARCO NEI DUE VERSI",
          any("DOPPI" in x for x in errori(
              np.append(ii, jj[0]), np.append(jj, ii[0]), n, "prova")),
          "`(%d,%d)` e `(%d,%d)`: ### il grafo e- NON ORIENTATO, e questo e- un doppione "
          "CHE NON SEMBRA UN DOPPIONE" % (ii[0], jj[0], jj[0], ii[0]))
    esito("### DEVE scattare: un INDICE FUORI INTERVALLO",
          any("FUORI da" in x for x in errori(
              np.append(ii, n + 5), np.append(jj, 0), n, "prova")),
          "### altrimenti `numpy` darebbe un `IndexError` LONTANO dal punto dove e- nato")
    esito("### DEVE scattare: le due liste di LUNGHEZZA DIVERSA",
          any("META-" in x for x in errori(np.append(ii, 1), jj, n, "prova")),
          "### `ii` e `jj` sono le due meta- di una lista di coppie")
    esito("### DEVE scattare: `controlla` FERMA, non segnala",
          _ferma(np.append(ii, 3), np.append(jj, 3), n),
          "### violazione -> FERMO, e il mandato lo chiede cosi-: non tronca, non corregge")
    print()
    # ------------------------------------------------------- la SIMMETRIA sotto scambio
    print("-" * 100)
    print("<<ARCHI SIMMETRICI>>, il secondo significato: LA FISICA tratta `(i,j)` e "
          "`(j,i)` allo stesso modo?")
    print("-" * 100)
    c = CFG.carica(os.path.join(_QUI, "config", "prova.yaml"))
    T = DRV.termini_attivi(c)
    gi, gj = DRV.grafo(c["scena"], c["nodi"])
    # ### ⛔ **LO STATO SI COSTRUISCE COME LO COSTRUISCE IL DRIVER**, non in un
    # ### modo mio: `ST.nuovo(n)` e poi il riempimento con `default_rng(seme)`.
    # ### ⚠ **Se lo costruissi diversamente, misurerei un altro sistema.**
    st = ST.nuovo(c["nodi"])
    rng = np.random.default_rng(c["seme"])
    for k in st:
        st[k][...] = (rng.normal(size=st[k].shape)
                      + 1j * rng.normal(size=st[k].shape))
    dritto, _ = PA.passo_globale(st, gi, gj, c["dt"], T, c["iterazioni"], c["toll"])
    storto, _ = PA.passo_globale(st, gj, gi, c["dt"], T, c["iterazioni"], c["toll"])
    assert set(dritto) == set(storto)
    scarto = max(float(np.max(np.abs(dritto[k] - storto[k]))) for k in dritto)
    esito("NON deve scattare: scambiati `ii` e `jj` su TUTTI gli archi, "
          "lo stato e- LO STESSO AL BIT", scarto == 0.0,
          "scarto massimo %.3e su %d grandezze. ### E- piu- forte del controllo per "
          "passo, e piu- costoso: per questo sta QUI e non nel passo"
          % (scarto, len(dritto)))
    print()
    # ------------------------------------------------------------------ il COSTO
    print("-" * 100)
    print("IL COSTO, MISURATO -- per il budget del punto 6")
    print("-" * 100)
    t_ctrl = costo(n=c["nodi"], archi=(gi, gj), giri=3000)
    t0 = time.perf_counter()
    for _ in range(200):
        PA.passo_globale(st, gi, gj, c["dt"], T, c["iterazioni"], c["toll"])
    t_passo = (time.perf_counter() - t0) / 200
    print("  il controllo: %.3f us   un passo GLOBALE: %.1f us   rapporto: %.4f%%"
          % (t_ctrl * 1e6, t_passo * 1e6, 100.0 * t_ctrl / t_passo))
    esito("### e il COSTO e- sotto il 10%% di un passo",
          t_ctrl < 0.10 * t_passo,
          "%.4f%%: ### un presidio che decuplicasse il costo SI SPEGNEREBBE IL PRIMO "
          "GIORNO, ed e- il difetto di `A9`" % (100.0 * t_ctrl / t_passo))
    print("=" * 100)
    print("IL COLLAUDO DEL GRAFO: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def _ferma(ii, jj, n):
    """### `True` se `controlla` ### **ferma davvero.**"""
    try:
        controlla(ii, jj, n, "prova")
    except AssertionError as e:
        return "IL GRAFO NON E- VALIDO" in str(e)
    return False


def main(argv):
    del argv
    return collaudo()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
