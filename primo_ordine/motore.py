# -*- coding: utf-8 -*-
"""SOTTO-PEZZO `5b` DEL MOTORE — **IL DOPPIO CONTENITORE, E LE SCRITTURE IN POSTO.**

> ### ⛔ **Il mandato, alla lettera:** *«doppio contenitore per psi e phi con scritture
> in-place, punto unico di scrittura, cache che portano la loro taglia, contatori dei
> ripieghi»*.

### ⭐ **CHE COS'E', in una riga:** tiene lo stato, **la sua copia di servizio**, e
**tutti i buffer temporanei** — e li tiene **con la loro taglia addosso**, cosi' un
cambio di taglia **non puo' riusare un buffer vecchio**.

## ⛔ IL DIFETTO CHE QUESTO MODULO ESISTE PER IMPEDIRE

Una **cache fra due passi** che **non porta la sua taglia**: il grafo cresce, il buffer
resta della taglia di prima, e `numpy` **non se ne accorge** se la forma e' compatibile.
### **Il risultato e' sbagliato senza sembrarlo**, che e' la forma peggiore.
### ✅ **Qui ogni buffer e' una chiave `(nome, forma, tipo)`:** una taglia nuova e'
**un'altra chiave**, quindi **non esiste il caso <<riuso quello vecchio>>.**

## ⚠ CHE COSA VIENE DA FUORI, E PERCHE'

| | |
|---|---|
| **la geometria** | `n[2m, 3]` *(un versore per estremita')* e `U[m, 2, 2]` *(il trasporto di ogni arco)*. ### ⛔ **NON la calcola questo modulo**, e non e' pigrizia: **da dove nasce la geometria nell'era `2` e' una decisione aperta** — e un motore che se la inventasse **nasconderebbe quella decisione** |
| **`dtau`** | un tempo proprio **per nodo**. ### ⚠ **La sua forma non e' decisa** *(e' il posto `A1` della carta)*: qui entra come **dato**, non come formula |
| **la sommatoria** | `"numpy"` oppure `"esatta"`. ### ⭐ **NON ha un valore di comodo**: con `numpy` la somma dipende dall'**ordine** in virgola mobile, con `fsum` e' **esatta** — e in aritmetica esatta i due danno **lo stesso numero**. ### **E' una scelta di SOMMATORIA, non una manopola di fisica** |

## ⛔ LA REGOLA DEL TICK: `cresci()` **AL PIU' UNA VOLTA**

### ⚠ **E viene da una misura, non da un gusto.** La capacita' col raddoppio risparmia
**solo le riallocazioni di `ii` e `jj`**; `cresci()` **ricostruisce comunque** i derivati
con un `argsort`, cioe' **`O(m log m)` A CHIAMATA** — misurato: **~`30` ms a `1e5`
archi**, **~`0.3` s a `1e6`**.

### ⭐ **QUINDI le nascite e le morti di un tick SI RACCOLGONO**, e la struttura si
ricostruisce **una volta sola**. ### ⛔ **E non e' un consiglio:** `apri_tick()` azzera
il contatore, `chiudi_tick()` **ALZA se `cresci()` e' stata chiamata piu' di una volta**,
e **un braccio di collaudo lo pretende**. ### **Chiamare `cresci()` due volte in un tick
non e' piu' lento: e' un ERRORE che si ferma.**

### ⛔ **E IL FLUSSO DI SATURAZIONE NON E' QUI DENTRO PER INTERO:** la sua parte su `phi`
**da' una fase a `phi`**, e **il tipo di `phi` e' una domanda aperta per Luca** *(la
tabella lo dice reale, il banco lo tiene complesso)*. ### ✅ **I cinque pezzi unitari
invece ci sono tutti**, perche' **non dipendono da quella risposta**: lavorano su
qualunque tipo lo stato dichiari.

Gira con:  python primo_ordine/motore.py   (le allocazioni per tick, misurate)
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import flussi_parziali as FP                                  # noqa: E402
import incidenza as IN                                        # noqa: E402
import saturazione as SAT                                     # noqa: E402

# ### ⚠ **I MODI DI SOMMARE, a vocabolario CHIUSO.** Un terzo modo si aggiunge qui, e
# ### ### **chi passa una stringa fuori elenco ALZA** invece di prendere un default.
SOMMATORIE = ("numpy", "esatta")

# ### ⛔ **GLI OPERATORI CHE IL MOTORE OFFRE, e l-elenco e- quello della TABELLA.** Se la
# ### tabella nomina un operatore che non sta qui, il legame generato ### **ALZA** -- e
# ### quello e- lo stato normale finche- l-operatore non e- scritto.
OPERATORI = ("moneta_spin", "grover", "spostamento_trasporto",
             "grover_scalare", "spostamento_scalare")

# ### ⛔ **I FLUSSI SI CERCANO PER `id` DI LEGGE, non per nome di operatore**, e
# ### non e- una mia scelta: il legame generato per un `flusso` fa `quale = ID`, mentre
# ### quello di un `pezzo_unitario` fa `quale = OPERATORE`. ### **Il motivo e- che un
# ### flusso NON ha un operatore in tabella: ha un GENERATORE**, e il generatore e- scritto
# ### nella sua riga.
FLUSSI = ("CAMM-SATURAZIONE",)

# ### ⛔ **E LE FUNZIONI DELLA SATURAZIONE STANNO IN `saturazione.py`**, perche-
# ### questo file ha superato ### **il tetto di `700` righe** quando il flusso e- entrato:
# ### la regola dice ### **oltre, SI DIVIDE, NON SI ALLUNGA.**


def _versori_validi(n):
    """### I versori sono **unitari**? ### **Si misura, non si assume.**

    ### ⛔ **E la tolleranza e' DERIVATA e non scelta:** `8 * eps` del tipo, cioe'
    ### **quanto puo' sbagliare la radice di una somma di tre quadrati** -- e' la stessa
    soglia che il banco usa per la stessa cosa.
    """
    eps = float(np.finfo(n.dtype).eps)
    return float(np.max(np.abs(np.linalg.norm(n, axis=1) - 1.0))) <= 8 * eps


class Geometria(object):
    """### `n` per estremita' e `U` per arco. ### **Validate alla nascita, non dopo.**"""

    def __init__(self, n, U):
        n = np.ascontiguousarray(n, dtype=float)
        U = np.ascontiguousarray(U, dtype=complex)
        assert n.ndim == 2 and n.shape[1] == 3, (
            "`n` e' un versore per ESTREMITA': forma attesa (2m, 3), avuta %r" % (n.shape,))
        assert U.ndim == 3 and U.shape[1:] == (2, 2), (
            "`U` e' un trasporto 2x2 per ARCO: forma attesa (m, 2, 2), avuta %r"
            % (U.shape,))
        assert n.shape[0] == 2 * U.shape[0], (
            "le estremita' sono il doppio degli archi: `n` ne dichiara %d e `U` %d archi"
            % (n.shape[0], U.shape[0]))
        assert _versori_validi(n), (
            "un versore NON unitario: `exp(-i a sigma.n) = cos a I - i sin a (sigma.n)`"
            " vale solo se |n| = 1, e con |n| != 1 la moneta NON E' PIU' UNITARIA")
        # ### ⛔ **E `U` UNITARIA SI MISURA**, perche- ### **e- cio- che rende lo
        # ### spostamento unitario**: senza, la norma non si conserva -- e si vedrebbe
        # ### subito, ma ### **si vedrebbe DOPO**, lontano da qui.
        ident = np.einsum("aji,ajk->aik", np.conj(U), U)
        sbaglio = float(np.max(np.abs(ident - np.eye(2))))
        assert sbaglio <= 1e-12, (
            "una `U` NON unitaria (scarto %.3e): `U^dagger U = I` e' cio' che rende lo"
            " spostamento unitario, e senza quella la norma NON si conserva" % sbaglio)
        self.n = n
        self.U = U

    @property
    def m(self):
        return int(self.U.shape[0])


class Motore(object):
    """### Lo stato, la sua copia di servizio, e ### **i buffer con la taglia addosso.**"""

    def __init__(self, inc, geo, st, dtau, sommatoria):
        """### ⛔ **Nessun argomento ha un valore di comodo**, e il motivo e' la regola
        dei default nelle firme: un default qui sarebbe ### **una scelta mia che nessuno
        vede.**
        """
        assert isinstance(inc, IN.Incidenza), (
            "il motore lavora sulla struttura compatta, non su `(ii, jj)` nudi")
        assert geo.m == inc.m, (
            "la geometria dichiara %d archi e la struttura ne ha %d: una geometria di"
            " un'altra taglia darebbe numeri che sembrano buoni" % (geo.m, inc.m))
        assert sommatoria in SOMMATORIE, (
            "`sommatoria` sta in %r, e non ha un valore di comodo: con `numpy` la somma"
            " dipende dall'ORDINE in virgola mobile, con `esatta` no -- e' una scelta"
            " che chi misura DEVE dichiarare" % (SOMMATORIE,))
        dtau = np.ascontiguousarray(dtau, dtype=float)
        assert dtau.shape == (inc.n,), (
            "`dtau` e' un tempo proprio PER NODO: forma attesa (%d,), avuta %r"
            % (inc.n, dtau.shape))
        self.inc = inc
        self.geo = geo
        self.st = st
        self.dtau = dtau
        self.sommatoria = sommatoria
        # ### ⭐ **LE CACHE, CON LA TAGLIA ADDOSSO:** la chiave e- `(nome, forma, tipo)`.
        # ### ### **Una taglia nuova e- un-ALTRA CHIAVE**, quindi non esiste il caso
        # ### <<riuso quello vecchio>>.
        self._buf = {}
        # ### ⚠ **I CONTATORI DEI RIPIEGHI**, che il mandato chiede: quante volte un
        # ### buffer e- stato ### **allocato** *(cioe- quante volte la taglia e-
        # ### cambiata)*, e quante volte ogni operatore e- stato applicato.
        self.ripieghi = 0
        self.applicazioni = dict((o, 0) for o in OPERATORI + FLUSSI)
        # ### ⛔ **IL CONTATORE DELLE CRESCITE DEL TICK, e il suo TETTO e- `1`.**
        # ### ⚠ **Comincia a `-1` e non a `0`**, e la differenza conta: `-1` vuol
        # ### dire ### **nessun tick aperto**, e crescere fuori da un tick e-
        # ### ### **un errore diverso** da crescere due volte dentro.
        self.cresciute_nel_tick = -1
        self.tick = 0
        self.cresciute = 0
        self.operatori = {
            "moneta_spin": self._moneta_spin,
            "grover": self._grover,
            "spostamento_trasporto": self._spostamento_trasporto,
            "grover_scalare": self._grover_scalare,
            "spostamento_scalare": self._spostamento_scalare,
            # ### ✅ **IL FLUSSO, per `id` di legge e non per nome di
            # ### operatore**: il legame generato di un `flusso` cerca ### **l-`ID`.**
            "CAMM-SATURAZIONE": self._saturazione,
        }

    # ------------------------------------------------------------------ le porte del tick
    def apri_tick(self):
        """### Apre un tick. ### **Azzera il contatore delle crescite.**"""
        assert self.cresciute_nel_tick < 0, (
            "un tick e' GIA' aperto: aprirne un altro perderebbe il conto delle crescite"
            " di quello di prima, e quel conto e' il presidio")
        self.cresciute_nel_tick = 0
        return self

    def chiudi_tick(self):
        """### Chiude il tick, e ### **ALZA se `cresci()` e' stata chiamata piu' di una
        volta.**

        ### ⛔ **PERCHE- FERMA invece di avvisare:** la ricostruzione costa
        `O(m log m)` ### **a chiamata** -- ~`30` ms a `1e5` archi, ~`0.3` s a `1e6` --
        quindi due crescite in un tick ### **raddoppiano il costo del tick senza che
        nessuno l-abbia deciso.** ### **Un costo che nessuno ha deciso e- un difetto, non
        una lentezza.**
        """
        assert self.cresciute_nel_tick >= 0, (
            "nessun tick aperto: `chiudi_tick` senza `apri_tick` non chiude niente")
        quante = self.cresciute_nel_tick
        self.cresciute_nel_tick = -1
        self.tick += 1
        assert quante <= 1, (
            "`cresci()` chiamata %d volte in un tick, e il tetto e' 1: le nascite e le"
            " morti di un tick SI RACCOLGONO, perche' ogni chiamata ricostruisce i"
            " derivati con un argsort -- O(m log m) A CHIAMATA, ~30 ms a 1e5 archi"
            % quante)
        return quante

    def cresci(self, tieni, nuovi_ii, nuovi_jj, nodi_nuovi, iniziali):
        """### La crescita, ### **dal motore**: conta, cresce, e **permuta lo stato.**

        ### ⭐ **E- qui e non sulla struttura perche- la struttura NON SA dello
        stato:** `Incidenza.cresci` torna la permutazione, e ### **qualcuno deve
        applicarla allo spinore** -- se non lo facesse il motore, lo stato e il grafo
        ### **si disallineerebbero in silenzio.**

        ## ⛔ `iniziali`: NESSUN DEFAULT DI FISICA, e SI BLOCCA senza

        ### ⛔ **ERA UNA SCELTA DI FISICA CHE AVEVO PRESO IO SENZA ACCORGERMENE:** le
        estremita- nuove nascevano con `psi_h = 0` e `phi_h = 0` *(`np.zeros`)*, e la
        verifica esterna l-ha trovata. ### **Va contro TRE decisioni di Luca:** *<<seme
        piu- vuoto di fondo>>* *(un arco nuovo con `phi = 0` nasce **SENZA vuoto**)*,
        *<<la natura del nato non si assegna>>* *(**zero e- un valore ASSEGNATO**)*, e il
        principio per cui le estremita- nuove nascono con un `phi` ### **DERIVATO dai
        genitori, mai zero per default.**

        ### ✅ **QUINDI `iniziali` ARRIVA DA CHI CHIAMA, cioe- DALLA LEGGE**, ed e- un
        dizionario `{nome: array}` con ### **una riga per estremita- nuova**. ### ⛔
        **E senza, SI BLOCCA:** `None` non vuol dire *<<zero>>*, vuol dire
        ### **<<nessuno ha deciso>>.**

        ### ⭐ **E LO ZERO RESTA AMMESSO, ma SCRITTO:** un collaudo che vuole zero
        ### **passa un array di zeri**, e la differenza e- tutta qui --
        ### **un default e- una decisione invisibile, un argomento esplicito e- una
        decisione dichiarata.**
        """
        nuove = 2 * int(np.asarray(nuovi_ii).size)
        if nuove:
            assert iniziali is not None, (
                "`cresci()` fa nascere %d estremita' e `iniziali` e' `None`: il motore"
                " NON HA UN DEFAULT DI FISICA. Con che `psi` e che `phi` nasce"
                " un'estremita' nuova e' una DECISIONE, e `None` non vuol dire <<zero>>:"
                " vuol dire <<nessuno ha deciso>>. ### Lo zero si ottiene PASSANDO un"
                " array di zeri, e allora e' dichiarato" % nuove)
            for nome in sorted(iniziali):
                a = np.asarray(iniziali[nome])
                assert a.shape[0] == nuove, (
                    "`iniziali[%r]` ha %d righe e nascono %d estremita': un valore"
                    " iniziale della taglia sbagliata si propagherebbe in silenzio"
                    % (nome, a.shape[0], nuove))
        assert self.cresciute_nel_tick >= 0, (
            "`cresci()` fuori da un tick: le crescite si contano PER TICK, e fuori da un"
            " tick quel conto non esiste")
        vecchio = 2 * self.inc.m
        dove = self.inc.cresci(tieni, nuovi_ii, nuovi_jj, nodi_nuovi)
        self.cresciute_nel_tick += 1
        self.cresciute += 1
        # ### ⛔ **E LO STATO SEGUE LA PERMUTAZIONE, estremita- per estremita-.** Le
        # ### estremita- NUOVE nascono ### **a zero**, e quelle MORTE ### **spariscono**:
        # ### il `-1` che la struttura usa per <<non ha un seguito>> ### **non si indicizza
        # ### mai**, perche- si parte dalle vecchie e non dalle nuove.
        vive = dove >= 0
        for nome in ("psi_h", "phi_h"):
            v = self.st.get(nome)
            if v is None:
                # ### il ramo VARIABILE ASSENTE: una tabella che non la dichiara e-
                # ### ### **legittima**, e pretenderla qui vorrebbe dire che il motore
                # ### sa quali leggi esistono -- ### **e non lo sa.**
                continue
            nuovo = np.zeros((2 * self.inc.m,) + v.shape[1:], dtype=v.dtype)
            nuovo[dove[vive]] = v[:vecchio][vive]
            # ### ⛔ **E LE ESTREMITA- NUOVE PRENDONO CIO- CHE LA LEGGE HA DECISO**,
            # ### non lo zero dell-allocazione. ### ⚠ **Lo `np.zeros` qui sopra e- un
            # ### ALLOCATORE e non una scelta di fisica:** ogni posto nuovo viene
            # ### ### **scritto subito dopo**, e il controllo della taglia in testa
            # ### garantisce che ### **non ne resti uno vuoto.**
            if nuove:
                # ### ⚠ **`nuovo_m` e- un locale di `Incidenza.cresci`, non di
                # ### qui:** dopo la crescita gli archi vivi sono `self.inc.m`, e
                # ### ### **i nuovi sono gli ULTIMI** -- quindi le loro estremita-
                # ### cominciano a `2*m - nuove`. ### **L-interprete me l-ha detto
                # ### subito**, invece di scrivere nel posto sbagliato.
                base = 2 * self.inc.m - nuove
                val = iniziali.get(nome)
                assert val is not None, (
                    "`iniziali` non porta %r, e lo stato lo ha: ogni variabile che vive"
                    " sulle estremita' DEVE dire con che valore nasce -- altrimenti"
                    " nascerebbe con lo zero dell'allocatore, che e' una scelta di"
                    " fisica presa dal motore" % nome)
                nuovo[base:base + nuove] = np.asarray(val, dtype=v.dtype)
            self.st[nome] = nuovo
        # ### ⚠ **E I BUFFER SI BUTTANO, perche- la taglia e- cambiata:** tenerli
        # ### sarebbe ### **esattamente il difetto della cache che non porta la taglia.**
        self._buf = {}
        return dove

    # ------------------------------------------------------- i buffer, e la loro taglia
    def _b(self, nome, forma, tipo):
        """### Un buffer. ### **La taglia fa parte della CHIAVE**, non del contenuto.

        ### ⛔ **E il ripiego si CONTA**, perche' un motore che rialloca a ogni tick
        ### **e' esattamente il difetto che la diagnosi della memoria cercava** -- e
        ### **un costo che nessuno conta non si vede.**
        """
        chiave = (nome, tuple(forma), np.dtype(tipo).str)
        b = self._buf.get(chiave)
        if b is None:
            # ### il ramo ALLOCA: la taglia e- nuova, quindi ### **non c-e- niente da
            # ### riusare** -- e riusare un buffer di un-altra taglia e- il difetto.
            b = np.empty(forma, dtype=tipo)
            self._buf[chiave] = b
            self.ripieghi += 1
        return b

    def byte(self):
        """### I byte dei buffer, ### **tutti**. ### Piu' quelli della struttura."""
        return int(sum(b.nbytes for b in self._buf.values()) + self.inc.byte())

    # --------------------------------------------------------- la somma per nodo
    def _somma_per_nodo(self, v, fuori):
        """### La somma di `v` **sulle estremita' di ogni nodo**, dentro `fuori`.

        ### ⭐ **DUE MODI, e la differenza e' MISURATA e non supposta:** con `numpy` la
        somma dipende dall'**ordine** in virgola mobile *(quindi una rinumerazione cambia
        gli ultimi bit)*; con `math.fsum` e' **esatta**. ### ⚠ **In aritmetica esatta i
        due danno lo STESSO numero.**
        """
        fuori.fill(0)
        if self.sommatoria == "numpy":
            # ### il ramo NUMPY: una sola chiamata vettoriale, ### **e l-ordine e- il
            # ### suo** -- e- la via che il banco congelato usa.
            np.add.at(fuori, self.inc.nodo, v)
            return fuori
        # ### il ramo ESATTO: `fsum` per nodo e per componente. ### ⚠ **Costa un
        # ### ciclo Python**, e per questo ### **si DICHIARA invece di essere il
        # ### default**: serve quando l-isotropia si vuole esatta AL BIT.
        off, est = self.inc.offset, self.inc.estremita
        piatto = fuori.reshape(fuori.shape[0], -1)
        vp = v.reshape(v.shape[0], -1)
        complesso = np.iscomplexobj(v)
        for k in range(self.inc.n):
            ee = est[off[k]:off[k + 1]]
            if ee.size == 0:
                # ### il ramo NODO ISOLATO: la somma e- ### **zero**, e `fsum` di una
                # ### sequenza vuota lo darebbe comunque -- ma ### **saltarlo e- piu-
                # ### chiaro di farlo dire a `fsum`.**
                continue
            for c in range(piatto.shape[1]):
                pezzi = vp[ee, c]
                if complesso:
                    piatto[k, c] = complex(
                        math.fsum(pezzi.real.tolist()), math.fsum(pezzi.imag.tolist()))
                else:
                    piatto[k, c] = math.fsum(pezzi.tolist())
        return fuori

    # ======================================================= I CINQUE PEZZI UNITARI
    def _grover(self, st, parametri, frazione):
        """### `(2/d) Somma - I` sulle estremita' del nodo, ### **IN POSTO.**

        ### ⭐ **E' UNITARIA PER QUALUNQUE GRADO**, perche' e' `2|u><u| - I` con `|u>`
        il vettore uniforme: **una riflessione**. ### ✅ **E' la ragione per cui la norma
        si conserva senza normalizzare niente** — nessuna cura dove non c'e' un errore.

        ### ⭐⭐ **E DAL `2026-10-15` E' UN FLUSSO PARZIALE** *(strada `(B)`, decisioni
        `B-3` e `B-4` di Luca)*: ### **`G(theta) = P_u + e^{i theta}(I - P_u)`** con
        **`theta = pi · dtau_nodo/dtau_rif`**.
        ### ⚠ **PRIMA QUESTA FUNZIONE RIFIUTAVA una frazione diversa da `1`**, col motivo
        *«la radice di una riflessione non e' una riflessione»*: ### **quel motivo era
        giusto e NON E' PIU' VERO** -- un'involuzione e' un flusso all'angolo `pi`, e la
        sua radice e' il flusso a `pi/2`, che esiste ed e' unitaria.
        ### ✅ **E a `theta = pi` torna ESATTAMENTE il `(2/d) Somma - I` di prima, AL
        BIT** *(e' cio' che `M-B1` misura)*.
        """
        FP.grover(self, st["psi_h"], frazione)
        self.applicazioni["grover"] += 1
        return st

    def _grover_scalare(self, st, parametri, frazione):
        """### La **stessa** moneta di Grover, sullo scalare del vuoto.

        ### ⭐ **E <<la stessa>> e' diventato LETTERALE:** dal `2026-10-15` chiama
        ### **la stessa funzione** dello spinore, su una **VISTA** `(2m, 1)` di `phi` --
        perche' la forma `G(theta) = P_u + e^{i theta}(I - P_u)` ### **non dipende da
        quante componenti ha il campo.** ### ✅ **E il mandato lo chiede: il tempo proprio
        vale per `psi` E per `phi`.**
        """
        phi = st["phi_h"]
        FP.grover(self, phi.reshape(-1, 1), frazione)
        self.applicazioni["grover_scalare"] += 1
        return st

    def _moneta_spin(self, st, parametri, frazione):
        """### `exp(-i eps dtau sigma.n)` per **ESTREMITA'**: spin e direzione si legano.

        ### ⭐ **E' ESATTA, non un'esponenziale numerica:** `exp(-i a sigma.n) =
        cos a I - i sin a (sigma.n)` perche' `(sigma.n)^2 = I` quando `|n| = 1`.
        ### ✅ **Quindi nessun errore di troncamento, e la forma e' UNITARIA al bit.**
        """
        eps = parametri.get("eps")
        assert eps is not None, (
            "la moneta di spin vuole `eps` dalla TABELLA: senza, il motore sceglierebbe"
            " un numero -- e un numero scelto dal motore non ha origine")
        psi = st["psi_h"]
        nodo, nn = self.inc.nodo, self.geo.n
        ang = self._b("ang", (psi.shape[0],), float)
        np.take(FP.dtau_nodo(self), nodo, out=ang)
        np.multiply(ang, float(eps) * float(frazione), out=ang)
        self._ruota_attorno_a_n(psi, ang)
        self.applicazioni["moneta_spin"] += 1
        return st

    def _ruota_attorno_a_n(self, psi, ang):
        """### `exp(-i ang (sigma.n))` per estremita', ### **in posto, con due temporanei.**

        ### ⛔ **DUE TEMPORANEI SONO NECESSARI, e non sono uno spreco:** `out[0]` dipende
        da `psi[1]` e `out[1]` da `psi[0]`, quindi scrivere la prima componente
        **distruggerebbe** cio' che serve alla seconda. ### **Un <<in posto>> ingenuo qui
        darebbe un risultato sbagliato senza sembrarlo.**
        """
        a0 = self._b("a0", (psi.shape[0],), psi.dtype)
        a1 = self._b("a1", (psi.shape[0],), psi.dtype)
        # ### ✅ **RIDUZIONE `(a)` del mandato della soglia: `cos` e `sin` in UN
        # ### SOLO buffer.** Il seno va nel suo, e ### **il coseno si scrive IN POSTO
        # ### dentro `ang`** -- si puo-, perche- dopo il seno ### **`ang` non serve piu-.**
        # ### ⭐ **`-0.125x` della memoria della scena, e ZERO perdita di
        # ### precisione:** e- una riscrittura, non un-approssimazione.
        # ### ⚠ **E L-ORDINE DELLE DUE RIGHE CONTA:** il seno PRIMA, perche- il
        # ### coseno ### **distrugge `ang`.** Scambiarle darebbe `cos` del `cos`.
        s = self._b("sin", ang.shape, float)
        np.sin(ang, out=s)
        c = ang
        np.cos(ang, out=c)
        nx, ny, nz = self.geo.n[:, 0], self.geo.n[:, 1], self.geo.n[:, 2]
        p0, p1 = psi[:, 0], psi[:, 1]
        # ### `(sigma.n) psi`, scritto a mano: ### **nessuna matrice 2x2 costruita.**
        np.multiply(nz, p0, out=a0)
        a0 += (nx - 1j * ny) * p1
        np.multiply(nx + 1j * ny, p0, out=a1)
        a1 -= nz * p1
        # ### e adesso si scrive, ### **dopo** che entrambi i temporanei esistono
        np.multiply(a0, -1j * s, out=a0)
        np.multiply(a1, -1j * s, out=a1)
        np.multiply(p0, c, out=p0)
        np.multiply(p1, c, out=p1)
        p0 += a0
        p1 += a1

    def _spostamento_trasporto(self, st, parametri, frazione):
        """### Scambia le due estremita' di ogni arco **trasportando**, tutte insieme.

        ### ⛔ **`U_jk = U_kj^dagger` NON e' una convenzione: e' cio' che rende lo
        spostamento UNITARIO.** ### Qui si tiene **una `U` per arco** e il verso
        contrario usa **la sua coniugata trasposta**: ### ✅ **cosi' la relazione non e'
        una disciplina, e' la rappresentazione.**

        ### ⭐⭐ **E DAL `2026-10-15` E' IL FLUSSO PARZIALE `alpha I + beta S_U`**
        *(strada `(B)`)*, con `alpha = (1 + e^{i theta})/2`, `beta = (1 - e^{i theta})/2`
        e ### **`theta = pi · dtau_arco/dtau_rif`**, dove `dtau_arco` e' ### **la MEDIA
        ARMONICA** dei due nodi *(`B-3`)*.
        ### ⚠ **E <<non e' un flusso>> era VERO e non lo e' piu':** `S_U` e' hermitiana E
        unitaria, quindi `exp(i pi P-) = S_U` con `P- = (I - S_U)/2` -- ### **lo
        spostamento E' un flusso, preso all'angolo `pi`.**
        ### ✅ **A `theta = pi`: `alpha = 0` e `beta = 1` ESATTI**, e resta la permutazione
        con trasporto di prima, **AL BIT**.
        """
        FP.hop_psi(self, st["psi_h"], frazione)
        self.applicazioni["spostamento_trasporto"] += 1
        return st

    def elicita(self, st):
        """### `h_k`: l'elicita' ### **sommata sulle estremita' del nodo.**

        ### ⭐ **E' `s_h . n_h`**, cioe' ### **lo spin proiettato sulla
        direzione** -- ed e' qui che la geometria entra nella saturazione.
        ### ⚠ **`s_h = psi^dag sigma psi` sono TRE NUMERI REALI**, e si scrivono
        a mano per non costruire tre matrici per estremita'.
        """
        psi = st["psi_h"]
        a, c = psi[:, 0], psi[:, 1]
        nn = self.geo.n
        ac = np.conj(a) * c
        # ### `s . n` in una riga: ### **niente array (2m, 3) costruito** -- e- la somma
        # ### ### **mentre si calcola**, quindi un buffer in meno.
        sn = self._b("sn", (psi.shape[0],), float)
        np.multiply(2.0 * np.real(ac), nn[:, 0], out=sn)
        sn += 2.0 * np.imag(ac) * nn[:, 1]
        sn += (np.abs(a) ** 2 - np.abs(c) ** 2) * nn[:, 2]
        h = st["h_int"]
        h.fill(0)
        np.add.at(h, self.inc.nodo, sn)
        return h

    def densita_vuoto(self, st):
        """### `Lambda_k`: la densita' del vuoto del nodo, ### **somma di `|phi|^2`.**

        ### ⛔ **E' LA SCALA RISPETTO A CUI LA SATURAZIONE SI MISURA**, ed e'
        per questo che ### **non serve nessuna costante**: la scala e' **RELAZIONALE**,
        cioe' presa dal sistema e non messa a mano.
        ### ⭐ **E il modulo quadro ha senso come enunciato solo perche' `phi` e'
        COMPLESSO** -- di un reale sarebbe il quadrato.
        """
        phi = st["phi_h"]
        lam = st["Lambda"]
        lam.fill(0)
        np.add.at(lam, self.inc.nodo, np.abs(phi) ** 2)
        return lam

    def _saturazione(self, st, parametri, frazione):
        """### **IL FLUSSO ESATTO di `N` per un tempo `frazione * dtau`.**

        ### ✅ **Una rotazione e una fase, e nient'altro:** niente integratore,
        niente passo interno, ### **niente troncamento** -- e il suo inverso e'
        `frazione -> -frazione`.

        ### ⛔ **E QUESTO E' UN FLUSSO, quindi PRENDE la frazione**, al contrario
        dei cinque pezzi unitari: `exp(-i a) exp(-i b) = exp(-i(a+b))`, quindi
        ### **due mezzi fanno l'intero** -- e la composizione di Strang lo usa
        ### **due volte a meta' passo.**

        ### ⚠ **E LA PARTE SU `phi` E' LA RAGIONE PER CUI `phi` DEVE ESSERE
        COMPLESSO:** `phi -> phi exp(-i beta dtau)` ### **da' una FASE a `phi`**, e su un
        reale ### **non esisterebbe.** *(Era la domanda che Luca ha deciso il
        `2026-10-12`.)*
        """
        h = self.elicita(st)
        lam = self.densita_vuoto(st)
        al, be = SAT.pezzi(h, lam)
        nodo = self.inc.nodo
        f = float(frazione)
        # ### l-angolo e la fase ### **per ESTREMITA-**, prese dal loro nodo
        ang = self._b("sat_ang", (st["psi_h"].shape[0],), float)
        dtau = FP.dtau_nodo(self)
        np.take(al * dtau * f, nodo, out=ang)
        self._ruota_attorno_a_n(st["psi_h"], ang)
        fas = self._b("sat_fas", (st["phi_h"].shape[0],), float)
        np.take(be * dtau * f, nodo, out=fas)
        # ### ⛔ **e la fase su `phi` si applica IN POSTO:** `exp(-i fas)` si
        # ### costruisce in un buffer complesso, e ### **non si alloca.**
        ef = self._b("sat_ef", fas.shape, st["phi_h"].dtype)
        np.multiply(fas, -1j, out=ef)
        np.exp(ef, out=ef)
        np.multiply(st["phi_h"], ef, out=st["phi_h"])
        self.applicazioni["CAMM-SATURAZIONE"] += 1
        return st

    def _spostamento_scalare(self, st, parametri, frazione):
        """### Lo scambio delle due estremita', ### **senza trasporto**: e' uno scalare.

        ### ⭐⭐ **E DAL `2026-10-15` E' IL FLUSSO PARZIALE `alpha I + beta S`**, con
        `S` ### **la permutazione PURA** *(il vuoto e' NEUTRO: non ha carica da
        trasportare, e dargli una `U` vorrebbe dire dargli una carica che non ha)*.
        ### ✅ **A `theta = pi` torna lo scambio di prima, AL BIT.**
        ### ⚠ **E <<in posto DAVVERO>> non si puo' piu':** ogni lato nuovo dipende da
        ### **ENTRAMBI** i lati vecchi, quindi la fetta rovesciata non basta.
        """
        FP.hop_phi(self, st["phi_h"], frazione)
        self.applicazioni["spostamento_scalare"] += 1
        return st


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    import stato as ST
    print("=" * 96)
    print("LE ALLOCAZIONI PER TICK -- misurate, non dichiarate")
    print("=" * 96)
    for nn in (64, 256, 1024):
        ii = np.arange(nn, dtype=IN.INDICE)
        jj = (ii + 1) % nn
        inc = IN.Incidenza(ii, jj, nn, capacita=nn)
        n_ver = np.zeros((2 * inc.m, 3), dtype=float)
        n_ver[:, 2] = 1.0
        U = np.zeros((inc.m, 2, 2), dtype=complex)
        U[:, 0, 0] = 1.0
        U[:, 1, 1] = 1.0
        st = ST.nuovo(nn, inc.m)
        st["psi_h"][0, 0] = 1.0
        mot = Motore(inc, Geometria(n_ver, U), st, np.full(nn, 0.1), "numpy")
        for _ in range(3):
            mot.operatori["grover"](st, {}, 1)
            mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
            mot.operatori["spostamento_trasporto"](st, {}, 1)
        primi = mot.ripieghi
        for _ in range(20):
            mot.operatori["grover"](st, {}, 1)
            mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
            mot.operatori["spostamento_trasporto"](st, {}, 1)
        print("  n=%-6d  buffer allocati: %d nei primi 3 tick, %d nei 20 dopo"
              "   byte: %d" % (nn, primi, mot.ripieghi - primi, mot.byte()))
    print("=" * 96)
    print("  ### ZERO allocazioni nei tick dopo i primi: e' la lettura che conta")
    print("=" * 96)
    print()
    print("=" * 96)
    print("UNA `cresci()` CONTRO UN PASSO, SULLO STESSO GRAFO -- il rapporto, MISURATO")
    print("=" * 96)
    print("  ### Il mandato della verifica esterna: se la ricostruzione supera il passo,")
    print("  ### SI DICHIARA come limite noto. ### NON si ottimizza adesso.")
    import time
    for nn in (1000, 10000, 100000):
        ii = np.arange(nn, dtype=IN.INDICE)
        jj = (ii + 1) % nn
        inc = IN.Incidenza(ii, jj, nn, capacita=2 * nn)
        n_ver = np.zeros((2 * inc.m, 3), dtype=float)
        n_ver[:, 2] = 1.0
        U = np.zeros((inc.m, 2, 2), dtype=complex)
        U[:, 0, 0] = 1.0
        U[:, 1, 1] = 1.0
        st = ST.nuovo(nn, inc.m)
        st["psi_h"][0, 0] = 1.0
        mot = Motore(inc, Geometria(n_ver, U), st, np.full(nn, 0.1), "numpy")
        # ### un passo = i tre pezzi su `psi`, cioe- cio- che un tick fa DAVVERO
        def _passo():
            mot.operatori["grover"](st, {}, 1)
            mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
            mot.operatori["spostamento_trasporto"](st, {}, 1)
        _passo()                                   # ### scalda i buffer: il primo ALLOCA
        giri = 20 if nn <= 10000 else 5
        t0 = time.perf_counter()
        for _ in range(giri):
            _passo()
        tp = (time.perf_counter() - t0) / giri
        # ### e una `cresci()` che NON cambia niente: ### **si misura la RICOSTRUZIONE**,
        # ### non la chirurgia -- cosi- il numero e- quello dell-`argsort`.
        tieni = np.ones(inc.m, dtype=bool)
        t0 = time.perf_counter()
        for _ in range(giri):
            mot.apri_tick()
            mot.cresci(tieni, [], [], 0, None)
            mot.chiudi_tick()
        tc = (time.perf_counter() - t0) / giri
        print("  n=%-7d m=%-7d  passo %8.3f ms   cresci() %8.3f ms   rapporto %6.2fx  %s"
              % (nn, inc.m, tp * 1e3, tc * 1e3, tc / tp,
                 "### LA RICOSTRUZIONE DOMINA" if tc > tp else "il passo domina"))
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
