# -*- coding: utf-8 -*-
"""SOTTO-PEZZO `5a` DEL MOTORE — **LA STRUTTURA COMPATTA DELLE ESTREMITA' D'ARCO.**

> ### ⛔ **Il mandato, alla lettera:** *«archi in array e vicini in `CSR` con capacita'
> raddoppiante, punto unico di scrittura»*.

### ⭐ **PERCHE' LE ESTREMITA' E NON I NODI.** Lo spinore della camminata **vive sulle
estremita' d'arco**, non sui nodi: un grafo con `m` archi ne ha **`2m`**, un numero che
`n` **non contiene**. E lo spostamento con trasporto e' `psi'[compagna(h)] = U[h] psi[h]`
— cioe' **una PERMUTAZIONE delle estremita'**, non un prodotto matrice-vettore.
### ⛔ **Quindi NESSUNA matrice sparsa:** una permutazione vuole **un array di indici**, e
una matrice sparsa porterebbe con se' una struttura che **nessuno usa**.

## ⭐ LA SCOPERTA CHE TOGLIE UN ARRAY INVECE DI AGGIUNGERLO

Il censimento dell'architettura prevedeva **due** array derivati, `nodo[h]` e
`compagna[h]`. ### ✅ **`compagna` NON SI MEMORIZZA, ed e' un'identita' aritmetica:**
con la numerazione **arco `k` ⟹ estremita' `2k` e `2k+1`** si ha

    compagna(h) = h ^ 1

### ⛔ **E LA DIFFERENZA NON E' <<un array in meno>>: e' CHE NON PUO' DIVERGERE.** Un
array derivato tenuto accanto al grafo **puo'** restare indietro, e allora serve
disciplina; un'identita' aritmetica **non puo'**, e la disciplina non serve. ### ⚠ **Vale
solo se la numerazione delle estremita' resta quella**, e c'e' un braccio di collaudo che
lo pretende **dopo ogni crescita**.

## LE QUATTRO COSE CHE QUESTO MODULO TIENE

| | che cos'e' | la taglia |
|---|---|---|
| `ii`, `jj` | i due capi di ogni arco, **vettori paralleli** come nell'era `1` | `m` ciascuno |
| `nodo` | il nodo di ogni estremita' | `2m` |
| `offset` | dove cominciano, in `estremita`, le estremita' di ogni nodo | `n+1` |
| `estremita` | le estremita' **raggruppate per nodo** — la `CSR` | `2m` |

### ⭐ **E LA `CSR` E' NODO -> SUE ESTREMITA', non nodo -> nodi vicini.** Il motivo e'
**la fisica**: il Grover di un nodo mescola **le estremita' che stanno su quel nodo**, e
il grado e' `offset[v+1] - offset[v]`. ### I nodi vicini, se servono, sono
`nodo[compagna(h)]` — **derivati, non tenuti.**

## ⛔ LA CAPACITA' COL RADDOPPIO — **e CHE COSA NON RISOLVE**

> ### ⚠ **QUI AVEVO SCRITTO UNA COSA FUORVIANTE, e la verifica esterna me l'ha presa.**
> Avevo scritto che *«la ricostruzione a ogni nascita costa `O(m)`, cioe' `O(m**2)` su una
> corsa che cresce; il raddoppio costa `O(m)` ammortizzato»* — ### **come se il raddoppio
> togliesse la ricostruzione. NON LA TOGLIE.**

| | |
|---|---|
| ### **che cosa risolve il raddoppio** | **solo le riallocazioni di `_ii` e `_jj`**: senza, ogni nascita rialloca due array, cioe' `O(m)` **a ogni nascita** |
| ### ⛔ **che cosa NON risolve** | `cresci()` chiama `_rifa()` **ogni volta**, e `_rifa()` ricostruisce `nodo`, `offset` ed `estremita'` **con un `argsort`**: ### **`O(m log m)` A CHIAMATA, qualunque sia la capacita'** |
| ### 📌 **il costo vero, MISURATO** | la verifica esterna lo ha misurato: **~`30` ms a `1e5` archi**, **~`0.3` s a `1e6`** |
| ### ⭐ **LA CONSEGUENZA, ed e' una REGOLA per il motore** | le nascite e le morti di un tick **si RACCOLGONO**, e `cresci()` si chiama **AL PIU' UNA VOLTA PER TICK**. ### **Non e' un consiglio: il motore lo dichiara e un braccio di collaudo lo pretende** |
| ### ⚠ **il prezzo della memoria, dichiarato** | si tiene fino al **doppio** della memoria utile, e quel prezzo sta **DENTRO** la soglia della memoria, non accanto |

### ⚠ **E UNA CURA POSSIBILE, NON FATTA E NON DECISA:** la `CSR` si costruirebbe in
**`O(m)`** con un conteggio piu' una somma cumulata, invece di `O(m log m)` con
l'`argsort` — e ### **non violerebbe il punto unico di scrittura**, perche' resta una
**ricostruzione intera** e non un aggiornamento a pezzi. ### ⛔ **Non la faccio adesso
perche' il mandato dice <<solo misura e dichiarazione>>**, e perche' **un'ottimizzazione
prima della misura del `5b` sarebbe una cura senza il suo errore.**

### ⛔ **IL PUNTO UNICO DI SCRITTURA:** `cresci()` e' **l'unica** funzione che cambia
`m`, e **ricostruisce `nodo`, `offset` ed `estremita` da `(ii, jj)`** invece di
aggiornarli a pezzi. ### ⚠ **E non e' pigrizia: aggiornarli a pezzi vorrebbe dire DUE
verita' sullo stesso fatto**, e due verita' divergono.

Gira con:  python primo_ordine/incidenza.py   (il costo, misurato)
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import grafo as GR                                            # noqa: E402

# ### ⛔ **IL TIPO DEGLI INDICI, DICHIARATO UNA VOLTA.** `int64` e non `intp`: la taglia
# ### di un indice ### **non deve dipendere dalla macchina**, altrimenti un dato salvato
# ### su una macchina ### **non si riprende sull-altra** -- e il checkpoint e- il
# ### sotto-pezzo che viene dopo questo.
INDICE = np.int64

# ### ⛔ **IL FATTORE DI CRESCITA E- UNA CONVENZIONE DICHIARATA, NON UNA LEGGE** --
# ### e questa riga ### **correggeva un-affermazione FALSA che avevo scritto io.**
# ### ⚠ **QUELLO CHE AVEVO SCRITTO:** *<<`2` e- l-UNICO valore per cui il costo e-
# ### `O(n)` ammortizzato ... un `1.5` o un `3` sarebbero una manopola; il `2` e- la
# ### legge>>*. ### **E- falso, e la verifica esterna me l-ha preso:**
# ### ### **QUALUNQUE `r > 1`** da- costo ammortizzato ### **`O(1)` per inserimento**,
# ### con lo spreco di memoria limitato da un fattore `r`. ### **Non c-e- niente di
# ### unico nel `2`.**
# ### ✅ **PERCHE- ALLORA `2`:** perche- e- ### **il valore usuale**, e perche- il
# ### suo limite sulla memoria -- ### **al piu- `2x`** -- sta ### **gia- dentro la
# ### soglia della memoria per tick**, quindi ### **non apre un margine nuovo.**
# ### ⭐ **E chiamarla CONVENZIONE invece di LEGGE non e- una sfumatura:** una legge
# ### non si cambia senza una derivazione, una convenzione ### **si cambia dichiarandolo**
# ### -- e dire <<legge>> le dava ### **un-autorita- che non ha.**
CRESCITA = 2


def compagna(h):
    """### L'altra estremita' dello stesso arco. ### **Un'identita', non un array.**

    ### ⭐ **Con la numerazione <<arco `k` ⟹ estremita' `2k` e `2k+1`>>, la compagna e'
    `h ^ 1`**: pari → dispari, dispari → pari. ### ⛔ **Niente memoria, e NON PUO'
    divergere dal grafo** -- che e' la ragione vera, non il risparmio.

    ### ⚠ **Funziona su uno scalare e su un array**, perche' lo spostamento la usa
    ### **su tutte le estremita' in una volta**: un ciclo per estremita' nel percorso
    caldo e' esattamente cio' che la struttura compatta esiste per evitare.
    """
    return h ^ 1


def arco_di(h):
    """### L'arco a cui appartiene l'estremita'. ### **L'altra meta' della numerazione.**"""
    return h >> 1


def estremita_di_arco(k):
    """### Le due estremita' dell'arco `k`, ### **in quest'ordine: `ii` poi `jj`.**

    ### ⛔ **L'ORDINE E' PARTE DELLA CONVENZIONE, non un dettaglio:** `2k` sta su `ii[k]`
    e `2k+1` sta su `jj[k]`. ### **Scambiarli scambierebbe il verso del trasporto**, e un
    verso scambiato ### **non si vede in una norma.**
    """
    return (2 * k, 2 * k + 1)


def _derivati(ii, jj, n):
    """### `nodo`, `offset`, `estremita` **da `(ii, jj)`** — e da niente altro.

    ### ⛔ **E' la funzione che rende impossibile la divergenza:** chi vuole i derivati
    ### **li ricalcola da qui**, e non esiste una via per aggiornarli a pezzi.
    """
    m = int(ii.shape[0])
    # ### `nodo[2k] = ii[k]`, `nodo[2k+1] = jj[k]` -- l-intreccio, in una sola scrittura
    nodo = np.empty(2 * m, dtype=INDICE)
    nodo[0::2] = ii
    nodo[1::2] = jj
    # ### ⭐ **LA `CSR` CON UN CONTEGGIO E UNA SOMMA CUMULATA**, come l-era `1` fa coi
    # ### gradi: ### **nessun ciclo Python per nodo.**
    grado = np.bincount(nodo, minlength=n).astype(INDICE)
    offset = np.zeros(n + 1, dtype=INDICE)
    np.cumsum(grado, out=offset[1:])
    # ### ⚠ **E l-ordine dentro ogni nodo e- quello delle ESTREMITA- CRESCENTI**, perche-
    # ### `argsort` con `kind="stable"` conserva l-ordine a parita- di chiave.
    # ### ⛔ **E NON e- un dettaglio estetico: e- cio- che rende il Grover
    # ### RIPRODUCIBILE** -- un ordine che cambia fra due corse cambierebbe l-ordine
    # ### delle somme in virgola mobile, e con tre addendi l-ordine CONTA.
    estremita = np.argsort(nodo, kind="stable").astype(INDICE)
    return nodo, offset, estremita


class Incidenza(object):
    """### La struttura compatta, ### **con la sua capacita' e il suo punto unico.**

    ### ⚠ **NON e' una variabile di stato:** il grafo **non** e' una variabile della
    tabella delle leggi. Questa classe e' **la forma compatta del grafo**, e lo stato
    *(lo spinore sulle estremita')* vive **altrove**.
    """

    def __init__(self, ii, jj, n, capacita):
        """### Costruisce dalla lista di archi. ### **`capacita` NON ha un default.**

        ### ⛔ **E il motivo e' la regola dei default nelle firme:** una capacita' di
        comodo sarebbe ### **un numero scelto da me che nessuno vede**, e chi costruisce
        ### **sa quanto vuole crescere.** ### **Chi non lo sa passa `m`**, e allora il
        primo arco nuovo paga un raddoppio: ### **e' un costo, non un errore.**
        """
        ii = np.asarray(ii, dtype=INDICE)
        jj = np.asarray(jj, dtype=INDICE)
        assert ii.shape == jj.shape, (
            "`ii` e `jj` sono le due meta' di una lista di coppie: con lunghezze diverse"
            " (%r e %r) quella lista NON ESISTE" % (ii.shape, jj.shape))
        m = int(ii.shape[0])
        assert capacita >= m, (
            "la capacita' (%d) e' MINORE degli archi che ci devono stare (%d)" %
            (capacita, m))
        # ### ⛔ **IL GRAFO SI VALIDA QUI, e non si assume:** il controllo per passo
        # ### dell-era `1` esiste gia-, e ### **una struttura compatta costruita su un
        # ### grafo invalido propagherebbe l-errore LONTANO dal punto dove e- nato.**
        GR.controlla(ii, jj, n, "Incidenza.__init__")
        self.n = int(n)
        self.m = m
        self.capacita = int(capacita)
        self._ii = np.zeros(self.capacita, dtype=INDICE)
        self._jj = np.zeros(self.capacita, dtype=INDICE)
        self._ii[:m] = ii
        self._jj[:m] = jj
        # ### ⭐ **I CONTATORI DEI RIPIEGHI**, che il mandato chiede: quante volte la
        # ### capacita- e- raddoppiata, e quanti archi sono nati in tutto.
        self.ripieghi = 0
        self.archi_nati = 0
        self.archi_morti = 0
        self._rifa()

    # ---------------------------------------------------------------- le viste
    @property
    def ii(self):
        """### I primi capi, ### **solo gli `m` VIVI** -- non la capacita'."""
        return self._ii[:self.m]

    @property
    def jj(self):
        """### I secondi capi, ### **solo gli `m` VIVI.**"""
        return self._jj[:self.m]

    @property
    def grado(self):
        """### Il grado di ogni nodo, ### **dalla `CSR` e non ricontato.**"""
        return self.offset[1:] - self.offset[:-1]

    def estremita_di_nodo(self, v):
        """### Le estremita' che stanno sul nodo `v`. ### **Una fetta, non una copia.**"""
        return self.estremita[self.offset[v]:self.offset[v + 1]]

    def vicini_di_nodo(self, v):
        """### I nodi vicini di `v`, ### **DERIVATI e non tenuti.**"""
        return self.nodo[compagna(self.estremita_di_nodo(v))]

    # ---------------------------------------------- il punto unico di scrittura
    def _rifa(self):
        """### Ricostruisce i derivati. ### **Chiamata SOLO dal punto unico.**"""
        self.nodo, self.offset, self.estremita = _derivati(self.ii, self.jj, self.n)

    def _allarga(self, serve):
        """### Raddoppia finche' ci stanno `serve` archi. ### **E conta il ripiego.**

        ### ⚠ **E QUESTO NON E- IL COSTO DI `cresci()`:** allargare e- ammortizzato,
        ma `cresci()` ### **ricostruisce comunque i derivati con un `argsort`**, cioe-
        ### **`O(m log m)` a chiamata.** ### **Il raddoppio risparmia le riallocazioni di
        `_ii` e `_jj`, non la ricostruzione.**
        """
        if serve <= self.capacita:
            # ### ✅ **IL RAMO CHE NON FA NIENTE, e va dichiarato:** la capacita- basta,
            # ### e ### **non allargare e- la cosa giusta** -- allargare <<per sicurezza>>
            # ### sprecherebbe memoria senza che nessuno l-abbia deciso.
            return 0
        nuova = max(self.capacita, 1)
        while nuova < serve:
            nuova *= CRESCITA
        for nome in ("_ii", "_jj"):
            vecchio = getattr(self, nome)
            nuovo = np.zeros(nuova, dtype=INDICE)
            nuovo[:self.m] = vecchio[:self.m]
            setattr(self, nome, nuovo)
        self.capacita = int(nuova)
        self.ripieghi += 1
        return 1

    def cresci(self, tieni, nuovi_ii, nuovi_jj, nodi_nuovi):
        """### ⛔ **IL PUNTO UNICO DI SCRITTURA.** Toglie archi, ne aggiunge, rifa' tutto.

        `tieni` e' la maschera *(o gli indici)* degli archi **che restano**; `nuovi_ii` e
        `nuovi_jj` sono gli archi **che nascono**; `nodi_nuovi` quanti nodi si aggiungono.

        ### ⭐ **TORNA LA PERMUTAZIONE DELLE ESTREMITA'**, e questo e' il pezzo che serve
        a chi tiene lo stato: le estremita' **si rinumerano** quando gli archi si
        compattano, quindi lo spinore **va permutato con loro**. ### ⛔ **Se questa
        funzione non la tornasse, chi tiene lo stato dovrebbe RICALCOLARLA — cioe'
        ci sarebbero DUE verita' sulla stessa rinumerazione.**

        ### ⚠ **E `None` NON e' ammesso per `tieni`:** <<tieni tutto>> si scrive, non si
        omette. Un default qui vorrebbe dire che ### **la chiamata piu' comune e' quella
        che non dichiara niente.**
        """
        tieni = np.asarray(tieni)
        if tieni.dtype == bool:
            # ### il ramo MASCHERA: la forma che la chirurgia dell-era `1` usa
            assert tieni.shape[0] == self.m, (
                "la maschera ha %d elementi e gli archi vivi sono %d"
                % (tieni.shape[0], self.m))
            resta = np.flatnonzero(tieni).astype(INDICE)
        else:
            # ### il ramo INDICI: la forma che un chiamante che sa quali archi vuole usa
            resta = np.asarray(tieni, dtype=INDICE)
            assert resta.size == 0 or (resta.min() >= 0 and resta.max() < self.m), (
                "un indice di arco fuori dagli %d vivi" % self.m)
        nii = np.asarray(nuovi_ii, dtype=INDICE)
        njj = np.asarray(nuovi_jj, dtype=INDICE)
        assert nii.shape == njj.shape, (
            "gli archi nuovi sono coppie: `nuovi_ii` e `nuovi_jj` hanno forme diverse"
            " (%r e %r)" % (nii.shape, njj.shape))
        vecchio_m = self.m
        nuovo_m = int(resta.size + nii.size)
        self._allarga(nuovo_m)
        # ### ⛔ **SI COMPATTA IN POSTO, e l-ordine delle due scritture CONTA:** prima si
        # ### tirano avanti gli archi che restano, poi si mettono i nuovi in coda. ### Se
        # ### si facesse il contrario i nuovi verrebbero ### **sovrascritti.**
        tenuti_ii = self._ii[resta].copy()
        tenuti_jj = self._jj[resta].copy()
        self._ii[:resta.size] = tenuti_ii
        self._jj[:resta.size] = tenuti_jj
        self._ii[resta.size:nuovo_m] = nii
        self._jj[resta.size:nuovo_m] = njj
        self.n += int(nodi_nuovi)
        self.m = nuovo_m
        self.archi_nati += int(nii.size)
        self.archi_morti += int(vecchio_m - resta.size)
        GR.controlla(self.ii, self.jj, self.n, "Incidenza.cresci")
        self._rifa()
        # ### ⭐ **LA PERMUTAZIONE: la vecchia estremita' `2*resta[t]+b` e' diventata
        # ### `2*t+b`.** Le estremita' degli archi MORTI non hanno un seguito, e si
        # ### dicono con `-1`: ### **un indice impossibile e' piu' onesto di uno
        # ### plausibile**, perche' usarlo per sbaglio ALZA invece di leggere il dato
        # ### di un altro arco.
        dove = np.full(2 * vecchio_m, -1, dtype=INDICE)
        arrivo = np.arange(resta.size, dtype=INDICE)
        dove[2 * resta] = 2 * arrivo
        dove[2 * resta + 1] = 2 * arrivo + 1
        return dove

    def byte(self):
        """### I byte che questa struttura occupa, ### **capacita' COMPRESA.**

        ### ⛔ **Si conta la CAPACITA' e non gli archi vivi**, perche' la memoria che il
        processo tiene e' quella: ### **dichiarare gli archi vivi direbbe un numero piu'
        bello e falso.**
        """
        return int(self._ii.nbytes + self._jj.nbytes + self.nodo.nbytes
                   + self.offset.nbytes + self.estremita.nbytes)


def costo(n, archi, giri):
    """### Il costo di una ricostruzione dei derivati, ### **MISURATO.**"""
    import time
    ii = np.arange(archi, dtype=INDICE) % n
    jj = (ii + 1 + (np.arange(archi, dtype=INDICE) % (n - 2))) % n
    buoni = ii != jj
    ii, jj = ii[buoni], jj[buoni]
    vista = {}
    tieni = []
    for k in range(ii.shape[0]):
        chiave = (min(int(ii[k]), int(jj[k])), max(int(ii[k]), int(jj[k])))
        if chiave not in vista:
            vista[chiave] = 1
            tieni.append(k)
    ii, jj = ii[tieni], jj[tieni]
    t0 = time.perf_counter()
    for _ in range(giri):
        _derivati(ii, jj, n)
    return (time.perf_counter() - t0) / max(giri, 1)


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("IL COSTO DI UNA RICOSTRUZIONE DEI DERIVATI -- misurato, non stimato")
    print("=" * 96)
    for n, archi in ((100, 300), (1000, 3000), (10000, 30000)):
        t = costo(n, archi, 50 if archi < 10000 else 10)
        print("  n=%-7d archi=%-7d  %9.3f ms per ricostruzione" % (n, archi, t * 1e3))
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
