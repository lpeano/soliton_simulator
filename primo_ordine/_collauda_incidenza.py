# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL SOTTO-PEZZO `5a` — **la struttura compatta, nei DUE VERSI.**

### ⭐ **LA DOMANDA A CUI RISPONDE, in una riga:** *i derivati coincidono con `(ii, jj)`
**dopo OGNI crescita**, e il raddoppio **non perde un arco**?*

### ⛔ **E LA COSA CHE QUESTO COLLAUDO DEVE IMPEDIRE E' PRECISA:** che `nodo`, `offset`,
`estremita` diventino **una seconda verita'** accanto al grafo. ### **Un derivato che
divergeva vorrebbe dire che e' un dato indipendente, e allora SI TOGLIE.**

### ⚠ **E OGNI BRACCIO CHE <<DEVE FALLIRE>> SI VERIFICA SULLA CHIAVE GIUSTA:** un braccio
che cattura un'eccezione qualunque **non sa di quale eccezione si tratta.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import incidenza as IN                                        # noqa: E402

OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))


def _anello(n):
    """### Un anello di `n` nodi: ### **grado `2` ovunque**, nessun doppione."""
    ii = np.arange(n, dtype=IN.INDICE)
    jj = (ii + 1) % n
    return ii, jj


def _coerente(inc):
    """### L'INVARIANTE: i derivati **coincidono con `(ii, jj)`**, ricalcolati da zero.

    ### ⛔ **Si ricalcola da `(ii, jj)` e si confronta AL BIT**, invece di controllare
    qualche proprieta': ### **una proprieta' puo' valere anche per una struttura
    sbagliata**, l'uguaglianza no.
    """
    nodo, offset, estremita = IN._derivati(inc.ii, inc.jj, inc.n)
    return (np.array_equal(inc.nodo, nodo) and np.array_equal(inc.offset, offset)
            and np.array_equal(inc.estremita, estremita))


def _compagna_vera(inc):
    """### La compagna **aritmetica** coincide con la compagna **del grafo**?

    ### ⭐ **E' il braccio che giustifica di NON memorizzare `compagna`:** per ogni
    estremita' `h`, `compagna(h)` deve stare **sullo stesso arco** e **sull'altro capo**.
    """
    h = np.arange(2 * inc.m, dtype=IN.INDICE)
    c = IN.compagna(h)
    stesso_arco = np.array_equal(IN.arco_di(c), IN.arco_di(h))
    altro_capo = bool(np.all(c != h))
    # ### e i due capi dell-arco `k` stanno sui nodi `ii[k]` e `jj[k]`, in quest-ordine
    capi = (np.array_equal(inc.nodo[0::2], inc.ii)
            and np.array_equal(inc.nodo[1::2], inc.jj))
    return stesso_arco and altro_capo and capi


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL SOTTO-PEZZO `5a`: LA STRUTTURA COMPATTA DELLE ESTREMITA'")
    print("=" * 100)

    # =================================================================== il caso SANO
    ii, jj = _anello(8)
    inc = IN.Incidenza(ii, jj, 8, capacita=8)
    esito("il caso SANO: i derivati coincidono con `(ii, jj)` alla costruzione",
          _coerente(inc), "### se questo fallisse, i bracci sotto non direbbero niente")
    esito("### e il collaudo ha MATERIA: ci sono archi e nodi",
          inc.m == 8 and inc.n == 8, "### m=%d n=%d: con zero archi tutto passerebbe"
                                     " PER VACUITA-" % (inc.m, inc.n))
    esito("il grado viene dalla `CSR` e su un anello fa `2` ovunque",
          bool(np.all(inc.grado == 2)), "### gradi: %r" % (sorted(set(inc.grado.tolist())),))
    esito("### la compagna ARITMETICA e' la compagna DEL GRAFO",
          _compagna_vera(inc), "### e' il braccio che giustifica di NON memorizzarla")
    esito("i vicini sono DERIVATI e su un anello sono i due adiacenti",
          sorted(inc.vicini_di_nodo(3).tolist()) == [2, 4],
          "### vicini di 3: %r" % sorted(inc.vicini_di_nodo(3).tolist()))
    # ### ⛔ **E LE ESTREMITA- DI UN NODO sono proprio quelle che lo nominano:** senza
    # ### questo braccio la `CSR` potrebbe essere ### **una permutazione qualunque.**
    buono = all(int(inc.nodo[h]) == v
                for v in range(inc.n) for h in inc.estremita_di_nodo(v).tolist())
    esito("### e OGNI estremita' nella fetta di `v` sta DAVVERO sul nodo `v`",
          buono, "### altrimenti la `CSR` sarebbe una permutazione qualunque")

    # ============================================= LA CRESCITA, e l-invariante DOPO
    print()
    # ### ⭐ **LA MITOSI, nella forma dell-era `1`:** un arco SPARISCE e due NASCONO.
    # ### Qui l-arco `0` (fra `0` e `1`) si divide col nodo nuovo `8`.
    tieni = np.ones(inc.m, dtype=bool)
    tieni[0] = False
    dove = inc.cresci(tieni, [0, 8], [8, 1], 1)
    esito("### DOPO UNA CRESCITA i derivati coincidono ANCORA con `(ii, jj)`",
          _coerente(inc), "### m=%d n=%d, nati=%d morti=%d"
                          % (inc.m, inc.n, inc.archi_nati, inc.archi_morti))
    esito("### e la compagna aritmetica REGGE la rinumerazione",
          _compagna_vera(inc), "### se non reggesse, `compagna` dovrebbe diventare"
                               " un array")
    esito("il nodo nuovo ha grado `2`: l'arco diviso gli lascia i due pezzi",
          int(inc.grado[8]) == 2, "### grado del nodo 8: %d" % int(inc.grado[8]))
    esito("### il conto degli archi torna: uno morto, due nati",
          inc.m == 9 and inc.archi_nati == 2 and inc.archi_morti == 1,
          "### m=%d" % inc.m)
    # ### ⛔ **LA PERMUTAZIONE TORNATA E- QUELLA VERA, e si verifica SUL DATO:** si
    # ### mette un-etichetta su ogni estremita- vecchia e si pretende che segua.
    vecchie = np.arange(2 * 8, dtype=IN.INDICE)
    arrivate = dove[vecchie]
    vive = arrivate >= 0
    esito("### la permutazione tornata porta ogni estremita' VIVA al suo posto nuovo",
          bool(np.all(arrivate[vive] >= 0)) and int(vive.sum()) == 2 * 7,
          "### %d estremita' vive su %d, e le 2 dell'arco morto valgono -1"
          % (int(vive.sum()), 2 * 8))
    # ### ⭐ **E IL CONTENUTO SEGUE: il nodo dell-estremita- di arrivo e- quello di
    # ### partenza.** ### **Senza questo braccio la permutazione potrebbe essere una
    # ### qualunque biiezione e passare.**
    nodo_prima = np.empty(2 * 8, dtype=IN.INDICE)
    nodo_prima[0::2] = ii
    nodo_prima[1::2] = jj
    buono = bool(np.all(inc.nodo[arrivate[vive]] == nodo_prima[vive]))
    esito("### e il NODO di ogni estremita' sopravvive alla rinumerazione",
          buono, "### altrimenti la permutazione sarebbe una biiezione qualunque")

    # ====================================================== IL RADDOPPIO, e il ripiego
    print()
    stretta = IN.Incidenza(*_anello(6), n=6, capacita=6)
    esito("### il collaudo del raddoppio ha MATERIA: la capacita' e' PIENA",
          stretta.capacita == stretta.m == 6 and stretta.ripieghi == 0,
          "### capacita'=%d m=%d: se avanzasse posto, il raddoppio non scatterebbe"
          % (stretta.capacita, stretta.m))
    stretta.cresci(np.ones(6, dtype=bool), [0, 6], [6, 3], 1)
    esito("### il RADDOPPIO e' scattato, e il contatore dei ripieghi lo dice",
          stretta.ripieghi == 1 and stretta.capacita >= 8,
          "### ripieghi=%d capacita'=%d" % (stretta.ripieghi, stretta.capacita))
    esito("### e il raddoppio NON HA PERSO UN ARCO: i derivati coincidono",
          _coerente(stretta) and stretta.m == 8, "### m=%d" % stretta.m)
    # ### ⚠ **E IL RAMO CHE NON ALLARGA, provato e non assunto:** con posto che avanza
    # ### il contatore ### **non deve muoversi** -- altrimenti <<ripieghi>> conterebbe
    # ### le crescite, non i ripieghi.
    prima = stretta.ripieghi
    stretta.cresci(np.ones(8, dtype=bool), [1], [4], 0)
    esito("### e con posto che AVANZA il ripiego NON si conta",
          stretta.ripieghi == prima and stretta.m == 9,
          "### ripieghi=%d (invariato), m=%d" % (stretta.ripieghi, stretta.m))

    # ============================================ I CASI CHE DEVONO FALLIRE
    print()
    for che, fai, chiave in (
            ("una capacita' MINORE degli archi",
             lambda: IN.Incidenza(*_anello(5), n=5, capacita=3), "capacita'"),
            ("`ii` e `jj` di lunghezza diversa",
             lambda: IN.Incidenza([0, 1], [1], 3, capacita=4), "meta' di una lista"),
            ("un AUTO-ARCO, che il grafo rifiuta",
             lambda: IN.Incidenza([0, 1], [0, 2], 3, capacita=4), "auto"),
            ("un DOPPIONE, che il grafo rifiuta",
             lambda: IN.Incidenza([0, 0], [1, 1], 3, capacita=4), "archi DOPPI"),
            ("una maschera della lunghezza SBAGLIATA",
             lambda: inc.cresci(np.ones(3, dtype=bool), [], [], 0), "maschera"),
            ("archi nuovi NON appaiati",
             lambda: inc.cresci(np.ones(inc.m, dtype=bool), [0, 1], [2], 0), "coppie"),
            ("un indice di arco FUORI dai vivi",
             lambda: inc.cresci(np.array([0, 999]), [], [], 0), "fuori")):
        try:
            fai()
            passa, nota = False, "### NON ha alzato: il caso NON e' impedito"
        except AssertionError as e:
            passa = chiave.lower() in str(e).lower()
            nota = ("### e per la chiave GIUSTA (%r)" % chiave if passa
                    else "### ha alzato, ma per un-altra ragione: %r" % str(e)[:60])
        except Exception as e:                                # noqa: BLE001
            passa, nota = False, "### eccezione SBAGLIATA: %r" % str(e)[:60]
        esito("### DEVE fallire: %s" % che, passa, nota)

    # ======================================================= i byte, e la capacita'
    print()
    esito("### i byte DICHIARANO la capacita' e non gli archi vivi",
          stretta.byte() > 0
          and stretta.byte() >= (stretta.capacita * 2 * 8),
          "### %d byte con capacita' %d: contare i vivi direbbe un numero piu' bello"
          " e falso" % (stretta.byte(), stretta.capacita))

    print("=" * 100)
    print("IL SOTTO-PEZZO `5a`: %d su %d   ### %s"
          % (OK[0], OK[1], "TUTTI PASSATI" if OK[0] == OK[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
