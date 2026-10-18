# -*- coding: utf-8 -*-
r"""I FLUSSI PARZIALI — **il tempo proprio locale DENTRO il Grover e lo spostamento.**

> **Decisioni di Luca del 2026-10-15** *(registrate in `af3e40c`)*:
> **`B-3`** il tempo proprio dell'arco e' la **MEDIA ARMONICA** dei due nodi;
> **`B-4`** `omega` si fissa col raccordo **`omega · dtau_rif = pi`**, con `dtau_rif` il
> tempo proprio dell'**orologio piu' veloce**, e **UN SOLO `omega`** per lo spostamento e
> per il Grover.

## ⭐ PERCHE' QUESTE SONO LE FORME, e non sono scelte

### **Il Grover e lo spostamento di oggi sono INVOLUZIONI HERMITIANE**, cioe' **flussi di
un generatore locale presi all'angolo `pi`** — e questo e' un fatto algebrico, non una
lettura:

```
S_U = [[0, U^dagger], [U, 0]]   e' hermitiana E unitaria   ==>   S_U^2 = I
P-  = (I - S_U)/2               e' un PROIETTORE
exp(i pi P-) = I - 2 P- = S_U                  <- lo SPOSTAMENTO e' il flusso a theta = pi
G   = 2 P_u - I = exp(i pi (I - P_u))          <- il GROVER e' il flusso a theta = pi
```

### ✅ **Quindi i flussi parziali NON sono un'approssimazione dell'operatore di oggi: sono
l'operatore di oggi letto all'angolo giusto.** A `theta = pi` tornano **esattamente** i
due di prima, e il raccordo si misura **AL BIT** *(`M-B1`)*.

## ⛔ `dtau_rif` E' **UN'UNITA'**, E NON IL MASSIMO CORRENTE

### ⚠ **La frase di `B-4` ha due letture, e una e' esclusa DAI CRITERI DI USCITA:**
- **`dtau_rif = max(dtau)` ricalcolato** renderebbe un riscalamento **uniforme** di `dtau`
  **INERTE** *(`s = dtau/max(dtau) = 1` sempre)*, e allora
  ### **`_collauda_tempo_proprio.py` non potrebbe MAI passare** e **`M-B2` sarebbe vuota**;
- **`dtau_rif` = il TETTO DEL CONO**, l'orologio piu' veloce **POSSIBILE** *(`B-5`)*, cioe'
  ### **UN'UNITA' DI TEMPO**: e' questa.

### ⭐⭐ **E LA CONSEGUENZA E' CHE `omega` NON COMPARE IN QUESTO FILE.** Con `dtau_rif = 1`
il raccordo da' `omega = pi`, e nel codice resta **solo `theta = pi · dtau`**:
### ✅ **nessuna costante nuova** *(`CARTA-FISICA-SIMULATORE/F10`)*, e il numero `pi`
### **non e' una manopola: e' il raccordo.**

### ⛔ **E `theta <= pi` E' VERO PER COSTRUZIONE, NON PER UN TETTO** *(`A11`)*: `s <= 1`
viene da `dtau <= dtau_rif`, che e' **il cono**. ### **Un `dtau` oltre il cono non si
taglia: ALZA** — perche' quella scena sta **fuori dal modello**, e tagliarla
**nasconderebbe l'errore invece di trovarlo.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)


# ====================================================================== IL PUNTO UNICO
# ### ⭐ **TUTTO CIO' CHE LEGGE IL TEMPO PROPRIO PASSA DA QUI**, e il mandato lo chiede
# ### ### **per `L2`**: la' `cs` dovra' VARIARE, e deve poterlo fare ### **in un posto
# ### solo.** ### ⛔ **Una legge che calcolasse il suo `dtau` da se- sarebbe un secondo
# ### posto**, e il secondo posto e- esattamente cio- che rende impossibile cambiarlo.
def dtau_rif(mot):
    """### `dtau_rif`: **l'orologio piu' veloce POSSIBILE**, cioe' ### **l'UNITA'.**

    ### ⛔ **NON e' `max(dtau)`**, e il perche' sta nell'intestazione: col massimo
    corrente **due criteri di uscita su quattro sarebbero VUOTI.**
    ### ⚠ **Prende `mot` e non lo usa**, ed e' voluto: ### **a `L2` il tetto del cono
    potra' dipendere dalla configurazione**, e allora la firma e' gia' quella giusta —
    ### **chi chiama non cambia.**
    """
    assert mot is not None, (
        "`dtau_rif` vuole il motore anche se oggi non lo legge: la firma e' quella che"
        " servira' a `L2`, e un `None` qui vorrebbe dire che chi chiama non ha un motore")
    return 1.0


def dtau_nodo(mot):
    """### Il tempo proprio **PER NODO** — ### **l'unico posto da cui si legge.**

    ### ⛔ **E verifica la taglia**, che costa `O(1)`: dopo una crescita `inc.n` cambia e
    `dtau` **no** *(`cresci()` non lo estende)*, e senza questo controllo la differenza
    uscirebbe come un `IndexError` lontano da qui — ### **o, peggio, come un numero.**
    """
    d = mot.dtau
    assert d.shape == (mot.inc.n,), (
        "`dtau` ha forma %r e i nodi sono %d: dopo una crescita `dtau` NON si estende da"
        " solo, e un `dtau` di un'altra taglia darebbe numeri che sembrano buoni"
        % (d.shape, mot.inc.n))
    # ### ⛔⛔ **IL RAMO DELLA FORMA `cs`** *(`D0`, `2026-10-17`)*: ### **`mot.cs`
    # ### e- `None` finche- Luca non decide `Lambda_c`**, e allora questo ritorna
    # ### ### **`mot.dtau` TALE E QUALE** -- cioe- ### **il passo di oggi AL BIT.**
    # ### ✅ **Il ramo NON e- un default:** `None` vuol dire ### **la forma non c-e-**,
    # ### non ### **<<`Lambda_c` vale zero>>** -- e la differenza e' nel docstring di `cs`.
    # ### ⚠ **E quando c-e-, `dtau_k = cs_k * dt` e- il POSTO che `F7` cabla**: uno
    # ### solo, non sette.
    if mot.cs is None:
        return d
    eff = mot._b("fp_dtau_cs", (mot.inc.n,), float)
    np.multiply(d, mot.cs, out=eff)
    return eff


def cs(lam, lambda_c, fuori):
    """### `cs_k = Lambda_k / (Lambda_k + Lambda_c)` — ### **la velocita- locale della luce.**

    ### ⛔⛔ **`lambda_c` SI PASSA, SEMPRE: NESSUN VALORE PREDEFINITO**
    *(`D0` del mandato del `2026-10-16`)*. ### **Finche- Luca non decide il valore, questa
    funzione non si puo- chiamare per sbaglio** -- e il motore gira con ### **la forma
    SPENTA**, cioe- il passo di oggi ### **AL BIT.**

    ### ✅ **E NON SERVE NESSUN PAVIMENTO** *(`A11`)*: la forma sta in ### **`[0, 1)`
    per costruzione** -- `Lambda >= 0` e `Lambda_c > 0` danno `0 <= cs < 1`, e
    ### **`cs < 1` viene dalla FORMA, non da un taglio.**

    ### ⚠ **E `Lambda = 0` da- `cs = 0` ESATTO**, che e- ### **il valore della forma**
    e non un pavimento. ### ⛔ **MA L-ASSERT DEL CONO** *(`_nel_cono`)* ### **pretende
    `s > 0`**, e con `cs = 0` quel nodo avrebbe ### **un orologio fermo**: l-assert
    ### **lo RIFIUTA.** ### **Misurato il `2026-10-17`:** nelle scene di `M-B1` il minimo
    di `Lambda` su `250` tick e- ### **`5.6e-02`**, e ### **`Lambda = 0` non si presenta
    mai** -- quindi l-assert ### **non scatta.** ### **Non l-ho cambiato, e il caso resta
    una domanda per Luca.**
    """
    assert lambda_c > 0.0, (
        "`lambda_c` vale %r: la scala del vuoto e- UNA SCALA, quindi POSITIVA -- e a"
        " `lambda_c = 0` la forma darebbe `Lambda/Lambda`, cioe- `1` dove c-e- vuoto e"
        " `0/0` dove non ce n-e-. ### La forma SPENTA non si ottiene con uno ZERO: si"
        " ottiene NON ACCENDENDOLA (`mot.cs is None`)" % (lambda_c,))
    np.add(lam, lambda_c, out=fuori)
    np.divide(lam, fuori, out=fuori)
    return fuori


def accendi_cs(mot, lambda_c, st):
    """### Accende la forma `cs` ### **sullo stato DI ADESSO**, e pretende `lambda_c`.

    ### ⚠ **STA QUI E NON NEL MOTORE, e il motivo e' `P-MOD`:** `motore.py` era a
    ### **`726` righe su un tetto di `700`**, e ### **oltre si DIVIDE, non si allunga.**
    ### ✅ **E questo e' il posto giusto comunque:** il tempo proprio ### **vive in
    questo modulo** *(`dtau_nodo`, `s_nodo`, `s_arco`)*, e `cs` ### **e' il tempo proprio.**

    ### ⛔⛔ **QUESTA E' LA VARIANTE <<`cs` A INIZIO PASSO>>, e il mandato dice che
    e' SBAGLIATA:** `cs` dipende da `Lambda`, che ### **cambia DURANTE il passo**, quindi un
    `cs` letto all'inizio ### **rompe il palindromo.**
    ### ✅ **La variante GIUSTA e' `D2`** *(`cs` dallo stato al CENTRO del palindromo, a
    punto fisso)*, e ### **questa resta perche' `D2` la usa come IL CASO CHE DEVE
    FALLIRE:** deve ### **perdere il secondo ordine** e la simmetria.
    ### ⚠ **Quindi non e' un ripiego: e' il TERMINE DI CONFRONTO**, e il docstring lo
    dice perche' nessuno la usi credendola la forma buona.
    """
    lam = mot.densita_vuoto(st)
    mot.cs = cs(lam, lambda_c, mot._b("fp_cs", (mot.inc.n,), float)).copy()
    # ### ⛔⛔ **E IL NUMERO SI METTE INSIEME AL VETTORE** *(`2026-10-18`)*:
    # ### `CAMM-FASE-VUOTO` ha bisogno di ### **`cs'(Lambda)`**, che si calcola da
    # ### ### **`Lambda_c`** e non da `cs`. ### ⚠ **Un `cs` senza il suo `lambda_c`
    # ### e' una forma di cui non si sa la derivata**, e il pezzo nuovo
    # ### ### **non girerebbe** -- in silenzio.
    mot.lambda_c = float(lambda_c)
    return mot.cs


def spegni_cs(mot):
    """### Rimette la forma SPENTA: ### **il passo di oggi AL BIT.**

    ### ⛔ **E spegne ENTRAMBI**, perche' sono ### **una cosa sola**: lasciare
    `lambda_c` acceso con `cs` spento vorrebbe dire ### **una derivata senza la sua
    funzione.**
    """
    mot.cs = None
    mot.lambda_c = None


# ### ⛔⛔ **LA TOLLERANZA DEI PUNTI FISSI, E STA QUI PERCHE- SIA UNA**
# ### *(`2026-10-18`)*: `tick.EPS_CS` *(il punto fisso di `cs` al centro, `D2`)*
# ### ### **la legge da qui**, e il punto medio del peso d-arco usa ### **la stessa.**
# ### ⚠ **Due numeri uguali in due posti DIVERGONO.** ### ✅ **E e- un numero di
# ### METODO, non di fisica:** dice ### **quando due giri coincidono AGLI ULP**, e
# ### ### **non cambia nessun risultato.**
EPS_PUNTO_FISSO = 8.0 * float(np.finfo(float).eps)
# ### ⛔ **IL TETTO DEI GIRI DEL PESO, e NON e- una manopola:** e- ### **il numero
# ### oltre il quale si DICHIARA che non converge**, come `GIRI_MAX` di `tick.py`.
# ### ⚠ **Il massimo MISURATO sta nel referto**, accanto a questo numero.
GIRI_MAX_PESO = 120


def s_nodo(mot):
    """### `s = dtau/dtau_rif` **per nodo**, e ### **`s <= 1` si ASSERISCE, non si taglia.**

    ### ⚠ **La divisione per `1.0` e' ESATTA**, quindi oggi `s` e' `dtau` **al bit** — e
    cio' conta: e' cio' che rende `M-B1` possibile.
    """
    d = dtau_nodo(mot)
    s = mot._b("fp_s_nodo", (mot.inc.n,), float)
    np.divide(d, dtau_rif(mot), out=s)
    _nel_cono(s, "nodo")
    return s


def s_arco(mot):
    """### `s` **per ARCO**: la **MEDIA ARMONICA** di `B-3`, divisa per `dtau_rif`.

    ### ⭐ **E LA FORMA NON E' QUELLA OVVIA, PER UN MOTIVO MISURATO:**

    ```
    la forma ovvia   2 d_i d_j / (d_i + d_j)   NON da' `d` quando d_i = d_j = d
                     (sbaglia per d = 0.1, 0.2, 0.4;  e' esatta per 0.25, 0.31, 0.37)
    questa forma     S/2 - D^2/(2S)            con S = d_i + d_j,  D = d_i - d_j
                     da' `d` AL BIT quando d_i = d_j, perche' D = 0 e S/2 = 2d/2 = d
    ```

    ### ⛔ **E LA TRAPPOLA CHE CI STAVA SOTTO:** con la scena a `dtau = 0.25` *(quella di
    `bande` e di `segno`)* la forma ovvia **avrebbe passato `M-B1`**, e il difetto sarebbe
    uscito **dopo, su un'altra scena.**
    ### ✅ **E le due coincidono entro `7.2` ulp** su `100000` coppie casuali, e questa e'
    **simmetrica in `i <-> j` AL BIT** — cioe' ### **il tempo proprio dell'arco non dipende
    da quale capo si chiama `ii`.**
    """
    d = dtau_nodo(mot)
    m, nodo = mot.inc.m, mot.inc.nodo
    due = mot._b("fp_d_capi", (m, 2), float)
    np.take(d, nodo, out=due.reshape(-1))
    a, b = due[:, 0], due[:, 1]
    S = mot._b("fp_S", (m,), float)
    # ### ⭐ **`D` NON HA UN BUFFER SUO: va dentro `b`**, che dopo la somma ### **non
    # ### serve piu-.** ### ⚠ **E l-ordine conta:** la SOMMA prima, perche- la
    # ### differenza ### **distrugge `b`.**
    np.add(a, b, out=S)
    D = b
    np.subtract(a, b, out=D)
    # ### `H = S/2 - D^2/(2S)`, ### **in posto e senza temporanei nuovi**
    np.multiply(D, D, out=D)
    np.divide(D, S, out=D)
    np.multiply(S, 0.5, out=S)
    np.divide(D, 2.0, out=D)
    np.subtract(S, D, out=S)
    np.divide(S, dtau_rif(mot), out=S)
    _nel_cono(S, "arco")
    return S


def _nel_cono(s, dove):
    """### ⛔ **IL CONO, ASSERITO: `0 < s <= 1`.** ### **Non e' un clip** *(`A11`)*.

    ### ⚠ **E le due meta' dicono due errori DIVERSI:** `s <= 0` vuol dire **un tempo
    proprio nullo o negativo** *(un orologio fermo o che va indietro)*, `s > 1` vuol dire
    ### **una scena FUORI DAL CONO** — e il secondo e' il caso che `B-5` esclude
    **per costruzione.**
    """
    mi = float(np.min(s))
    ma = float(np.max(s))
    assert mi > 0.0, (
        "un `s` del %s vale %.17g <= 0: un tempo proprio nullo o negativo e' un orologio"
        " fermo o che va indietro, e NON si corregge con un pavimento" % (dove, mi))
    assert ma <= 1.0, (
        "un `s` del %s vale %.17g > 1, cioe' `dtau > dtau_rif`: quella scena sta FUORI DAL"
        " CONO (`B-5`: il tick e' l'orologio piu' veloce possibile), e il rimedio e'"
        " CAMBIARE LA SCENA -- non tagliare il `dtau`, che nasconderebbe l'errore" % dove)


# ====================================================================== LA FASE ESATTA
def espi(s, z, lavoro):
    """### `e^{i pi s}` — ### **ESATTA a `s = 0` e a `s = 1`**, e li' sta tutto.

    ### ⛔ **`np.exp(1j*np.pi)` NON VA:** da' `-1 + 1.2246467991473532e-16j`, e quel
    `1.2e-16` ### **ucciderebbe l'identita' al bit** di `M-B1`.

    ### ⭐ **E IL MALE STA NEL SENO, NON NEL COSENO** *(misurato)*:
    `np.cos(np.pi) = -1.0` **esatto**, `np.sin(np.pi) = 1.2246467991473532e-16` **no**.

    ### ✅ **QUINDI LA CURA E' UN'IDENTITA', NON UN CASO PARTICOLARE:** per `s` in `[0, 1]`
    vale `sin(pi s) = sin(pi (1 - s))`, e ### **`1 - s` e' ESATTO per `s >= 0.5`** *(lemma
    di Sterbenz)*; riducendo con `r = min(s, 1-s)` si ha `r = 0` **esatto** a `s = 1`,
    quindi `sin(pi r) = 0` **esatto**.
    ### ⛔ **Nessun `if s == 1`:** un ramo speciale a `theta = pi` farebbe passare `M-B1`
    ### **collaudando il ramo invece del codice.**
    """
    assert z.shape == s.shape and lavoro.shape == s.shape, (
        "`espi` scrive in posto: `s` %r, `z` %r e `lavoro` %r devono avere la STESSA"
        " forma" % (s.shape, z.shape, lavoro.shape))
    # ### il SENO, dalla riduzione: ### **`r = min(s, 1-s)`**, esatta a `s = 1`
    np.subtract(1.0, s, out=lavoro)
    np.minimum(s, lavoro, out=lavoro)
    np.multiply(lavoro, np.pi, out=lavoro)
    np.sin(lavoro, out=z.imag)
    # ### il COSENO, ### **diretto**: `cos(pi)` e' gia' esatto
    np.multiply(s, np.pi, out=lavoro)
    np.cos(lavoro, out=z.real)
    return z


def _frazione_valida(frazione):
    """### ⛔ **`0 < frazione <= 1`**, e ### **non e' l'assert di prima.**

    ### ⚠ **PRIMA questi pezzi RIFIUTAVANO una frazione diversa da `1`**, e il motivo
    scritto era giusto: ### **la radice di una riflessione non e' una riflessione.**
    ### ✅ **Con i flussi parziali quella frase NON E' PIU' VERA:** un'involuzione e' un
    flusso all'angolo `pi`, e ### **la sua <<radice>> e' il flusso a `pi/2`** — esiste, ed
    e' unitaria. ### **Quindi l'assert cambia di contenuto, non si toglie:** resta a
    vietare una frazione **nulla, negativa o maggiore di `1`**, che non ha senso in una
    composizione.
    """
    f = float(frazione)
    assert 0.0 < f <= 1.0, (
        "`frazione` vale %r: una frazione di passo sta in `(0, 1]` -- `<= 0` non e' un"
        " passo, e `> 1` vorrebbe dire INTEGRARE PIU' DEL PASSO" % (frazione,))
    return f


def z_nodo(mot, frazione):
    """### `e^{i theta}` **per nodo**, con `theta = pi · s_nodo · frazione`."""
    f = _frazione_valida(frazione)
    s = s_nodo(mot)
    # ### ⛔ **SEMPRE, anche a `f = 1`: `s * 1.0` e- ESATTO**, e un ramo
    # ### ### **farebbe collaudare il ramo invece del codice.**
    np.multiply(s, f, out=s)
    z = mot._b("fp_z_nodo", (mot.inc.n, 1), complex)
    return espi(s.reshape(-1, 1), z, mot._b("fp_w_nodo", (mot.inc.n, 1), float))


def z_arco_da_s(mot, s, frazione):
    """### `e^{i theta}` **per arco**, con `s` ### **DATA invece che letta dallo stato.**

    ### ⛔⛔ **PERCHE- ESISTE** *(`2026-10-18`, il punto medio per pezzo)*: il
    pezzo d-arco del vuoto ### **muove `Lambda` DENTRO la propria applicazione**
    *(misurato: `O(dtau)`, rapporti `2.019`-`1.986` al dimezzare)*, quindi il peso che usa
    ### **va valutato al punto medio** -- e per farlo serve ### **poterglielo DARE.**
    ### ✅ **E le operazioni sono LE STESSE di prima, nello stesso ordine:** e- cio-
    che tiene il braccio `0` ### **al bit.**
    ### ⚠ **`s` VIENE CONSUMATA** *(si moltiplica in posto per la frazione)*: chi la
    riusa ### **passa una copia.**
    """
    f = _frazione_valida(frazione)
    # ### ⛔ **SEMPRE, anche a `f = 1`: `s * 1.0` e- ESATTO**, e un ramo
    # ### ### **farebbe collaudare il ramo invece del codice.**
    np.multiply(s, f, out=s)
    z = mot._b("fp_z_arco", (mot.inc.m, 1), complex)
    return espi(s.reshape(-1, 1), z, mot._b("fp_w_arco", (mot.inc.m, 1), float))


def z_arco(mot, frazione):
    """### `e^{i theta}` **per arco**, col peso ### **letto dallo stato di ADESSO.**"""
    return z_arco_da_s(mot, s_arco(mot), frazione)


def s_arco_da_lambda(mot, lam):
    """### Il peso d-arco ### **che si avrebbe con QUESTA `Lambda`.**

    ### ⛔ **Serve al punto medio**, e ### **non riscrive niente:** mette `cs` di
    quella `Lambda` ### **nel motore per il tempo di una lettura**, chiama
    ### **la stessa `s_arco` che il passo chiama**, e ### **rimette `cs` com-era.**
    ### ⚠ **E pretende `mot.lambda_c`:** senza il numero ### **`cs` non si calcola**,
    e il punto medio ### **non esiste.**
    """
    salvo = mot.cs
    mot.cs = cs(lam, mot.lambda_c, mot._b("fp_cs_pm", (mot.inc.n,), float)).copy()
    try:
        return s_arco(mot).copy()
    finally:
        mot.cs = salvo


# ====================================================================== I DUE FLUSSI
def grover(mot, vista, frazione):
    """### `G(theta) = P_u + e^{i theta} (I - P_u)` sul NODO, ### **IN POSTO.**

    ### ⭐ **Una funzione per `psi` E per `phi`**, perche' la forma e' **la stessa**: cio'
    che cambia e' solo **quante componenti ha il campo** — `2` per lo spinore, `1` per il
    vuoto. ### ✅ **`vista` e' `(2m, c)`**, e per il vuoto e' `phi.reshape(-1, 1)`, che e'
    ### **una VISTA**: scriverci dentro scrive `phi`.

    ### ⛔ **E L'ORDINE DELLE DUE ULTIME RIGHE NON E' UNO STILE:** `presa + z·campo`, con
    `presa` PRIMA, e' cio' che a `theta = pi` da' **esattamente** `np.subtract(presa,
    campo)` di oggi — ### **`x + (-y)` e `x - y` sono la STESSA operazione IEEE**, mentre
    `z·campo + presa` sarebbe un'altra somma.
    """
    n, nodo = mot.inc.n, mot.inc.nodo
    c = vista.shape[1]
    S = mot._b("fp_S_campo_%d" % c, (n, c), vista.dtype)
    mot._somma_per_nodo(vista, S)
    z = z_nodo(mot, frazione)
    # ### il peso del Grover parziale: ### **`(1 - e^{i theta})/grado`**, e a `theta = pi`
    # ### e- ### **`2/grado`**, cioe- il peso di oggi ### **al bit.**
    w = mot._b("fp_w_grover", (n, 1), complex)
    np.subtract(1.0, z, out=w)
    np.divide(w, mot.inc.grado.reshape(-1, 1), out=w)
    presa = mot._b("fp_presa_%d" % c, vista.shape, vista.dtype)
    np.take(S, nodo, axis=0, out=presa)
    np.multiply(presa, np.take(w, nodo, axis=0,
                               out=mot._b("fp_w_h", (vista.shape[0], 1), complex)),
                out=presa)
    # ### ⭐ **E `z` ALLE ESTREMITA- RIUSA `fp_w_h`**, perche- dopo la riga di sopra
    # ### ### **il peso non serve piu-**: un buffer in meno, ### **e zero precisione
    # ### persa** -- e- una riscrittura, non un-approssimazione.
    np.multiply(vista, np.take(z, nodo, axis=0,
                               out=mot._b("fp_w_h", (vista.shape[0], 1), complex)),
                out=vista)
    np.add(presa, vista, out=vista)
    return vista


def _alfa_beta(mot, z):
    """### `alpha = (1 + e^{i theta})/2`, `beta = (1 - e^{i theta})/2`.

    ### ⭐ **E' la riscrittura di `hop(theta) = I + (e^{i theta} - 1) P-` con
    `P- = (I - S)/2`**, fatta a mano:
    `I + (e^{i theta}-1)(I-S)/2 = alpha I + beta S`.
    ### ✅ **A `theta = pi`: `alpha = 0` ESATTO e `beta = 1` ESATTO**, quindi resta
    **`S`** — lo spostamento di oggi. ### **E le divisioni per `2` sono esatte.**
    """
    # ### ⭐ **`alpha` NON HA UN BUFFER SUO: si scrive SOPRA `z`**, e l-ordine e- cio-
    # ### che lo permette -- ### **`beta` PRIMA**, perche- `alpha` distrugge `z`.
    # ### ⛔ **E NON si ricava `alpha = 1 - beta`**, che sarebbe un buffer in meno
    # ### ancora: ### **`(1+z)/2 + (1-z)/2` NON fa `1` AL BIT** *(le due divisioni
    # ### arrotondano)*, e `M-B1` misura i byte.
    be = mot._b("fp_beta", z.shape, complex)
    np.subtract(1.0, z, out=be)
    np.divide(be, 2.0, out=be)
    al = z
    np.add(1.0, z, out=al)
    np.divide(al, 2.0, out=al)
    return al, be


def hop_psi(mot, psi, frazione):
    """### `hop(theta)` sull'arco **CON trasporto**: ### **`alpha I + beta S_U`.**

    ### ⛔ **E SERVONO DUE COPIE, non una come oggi:** oggi lo spostamento e' una
    PERMUTAZIONE, e per scambiare due lati basta salvarne **uno**. ### **Qui ogni lato
    nuovo dipende da ENTRAMBI i lati vecchi** *(`alpha` sul suo, `beta` sull'altro
    trasportato)*, quindi ### **salvarne uno solo distruggerebbe un dato che serve
    ancora** — e darebbe un risultato sbagliato senza sembrarlo.
    """
    m = mot.inc.m
    v = psi.reshape(m, 2, 2)
    U = mot.geo.U
    al, be = _alfa_beta(mot, z_arco(mot, frazione))
    # ### ⭐ **DUE buffer, non tre**, e l-ordine e- cio- che lo permette: il lato `1`
    # ### vecchio ### **si legge IN POSTO** *(`alpha v1` si scrive sopra `v1`)*, quindi
    # ### non serve copiarlo.
    t0 = mot._b("fp_psi_lato0", (m, 2), psi.dtype)
    tm = mot._b("fp_psi_misto", (m, 2), psi.dtype)
    t0[...] = v[:, 0, :]
    # ### lato `0` nuovo: ### **`alpha v0 + beta (U^dagger v1)`**, e ### **`v1` e-
    # ### ANCORA INTATTO** quando l-einsum lo legge
    np.einsum("aji,aj->ai", np.conj(U), v[:, 1, :], out=tm)
    np.multiply(tm, be, out=tm)
    np.multiply(t0, al, out=v[:, 0, :])
    np.add(v[:, 0, :], tm, out=v[:, 0, :])
    # ### lato `1` nuovo: ### **`alpha v1 + beta (U v0)`**, con `v0` ### **dalla copia**
    np.einsum("aij,aj->ai", U, t0, out=tm)
    np.multiply(tm, be, out=tm)
    np.multiply(v[:, 1, :], al, out=v[:, 1, :])
    np.add(v[:, 1, :], tm, out=v[:, 1, :])
    return psi


def hop_phi(mot, phi, frazione):
    """### `hop(theta)` sull'arco **SENZA trasporto**: il vuoto e' **NEUTRO.**

    ### ⛔ **E il <<senza `U`>> non e' una semplificazione:** `phi` non ha carica da
    trasportare, e dargli una `U` vorrebbe dire ### **dargli una carica che non ha.**
    ### ⭐ **Quindi `S` e' la permutazione pura**, e `hop` resta `alpha I + beta S`.
    """
    return hop_phi_con_s(mot, phi, s_arco(mot), frazione)


def hop_phi_punto_medio(mot, st, frazione, regola):
    """### ⭐⭐ **IL PEZZO DEL VUOTO COL PESO AL PROPRIO PUNTO MEDIO.**

    ### ⛔⛔ **PERCHE- SOLO QUESTO PEZZO** *(decisione di Luca del `2026-10-18`,
    `12:07`)*: ### **e- il SOLO dei `14` che muove `Lambda` dentro la propria
    applicazione** -- ### **CONTATO**, non supposto *(`1.99e+00` a `dtau = 0.25`, contro
    `0.0` o `5e-15` di tutti gli altri)*. ### **E il movimento e- `O(dtau)`**, che e-
    esattamente cio- che da- ### **la deriva del PRIMO ordine** di `G`.

    ### ✅ **LA REGOLA, DICHIARATA NEL TASK HISTORY PRIMA DEL CODICE:**
    ### **`(ii)` la MEDIA DEI DUE `Lambda`** -- `Lambda_medio = (Lambda_0 + Lambda_1)/2`.
    ### ⛔ **E NON la `(i)`** *(`Lambda` sul `phi` medio)*, perche-
    ### **`(phi_0 + phi_1)/2` NON E- UNO STATO DEL FLUSSO:** il pezzo e- una rotazione, e
    la media fra partenza e arrivo ha norma ### **`cos(theta/2)`** volte quella di
    partenza -- quindi la- `Lambda` e- ### **sistematicamente piu- piccola**, di
    `cos^2(theta/2)`. ### ⚠ **E- `O(h^2)`, ma e- UN BIAS CON UN SEGNO**, e fra due
    regole che costano uguale ### **si prende quella che non ce l-ha.**
    ### 📌 **E `regola` permette di misurare ANCHE la `(i)`**, come informazione:
    ### **non e- un criterio nuovo**, e ### **non ha un valore di comodo.**

    ### ⛔⛔ **E IL PUNTO FISSO NON E- PER ARCO: ACCOPPIA LA RETE INTERA.**
    `hop_phi` applica ### **tutti gli archi insieme**, e `Lambda_k` ### **somma i
    semiarchi di piu- archi** -- quindi il peso di un arco dipende da `Lambda` dei suoi
    due nodi, che dipendono da ### **tutti gli archi che li toccano.**
    ### ✅ **Quindi i giri misurano QUANTO E- ACCOPPIATA LA RETE**, non la difficolta-
    di un arco -- e il referto li riporta ### **su due taglie.**

    ### ⛔ **E se non converge entro `GIRI_MAX_PESO` ALZA**, perche- la regola dice
    ### **di relazionare e NON di scegliere un altro schema.**
    """
    assert regola in ("ii", "i"), (
        "`regola` vale `ii` (la media dei due `Lambda`, quella DICHIARATA) o `i`"
        " (`Lambda` sul `phi` medio, che si misura come INFORMAZIONE): un valore di"
        " comodo renderebbe illeggibile quale delle due ha prodotto un numero (%r)"
        % (regola,))
    phi = st["phi_h"]
    salvo = mot._b("fp_phi_pm", phi.shape, phi.dtype)
    salvo[...] = phi
    lam0 = mot.densita_vuoto(st).copy()
    # ### ✅ **LA PRIMA IPOTESI E- IL PESO BLOCCATO**, cioe- ### **lo schema di
    # ### prima**: cosi- il primo giro ### **riproduce il punto di partenza.**
    s = s_arco(mot).copy()
    giri = 0
    for giri in range(1, GIRI_MAX_PESO + 1):
        phi[...] = salvo
        hop_phi_con_s(mot, phi, s.copy(), frazione)
        if regola == "ii":
            lam = 0.5 * (lam0 + mot.densita_vuoto(st))
        else:
            # ### ⚠ **LA REGOLA `(i)`, SOLO PER INFORMAZIONE:** `Lambda` del `phi`
            # ### ### **MEDIO**, che NON e- uno stato del flusso.
            mezzo = 0.5 * (salvo + phi)
            vecchio = phi.copy()
            phi[...] = mezzo
            lam = mot.densita_vuoto(st).copy()
            phi[...] = vecchio
        nuovo = s_arco_da_lambda(mot, lam)
        scarto = float(np.max(np.abs(nuovo - s)))
        scala = float(np.max(np.abs(nuovo)))
        s = nuovo
        if scarto <= EPS_PUNTO_FISSO * scala:
            break
    else:
        phi[...] = salvo
        raise AssertionError(
            "il punto medio del PESO non converge in %d giri (ultimo scarto %.3e): la"
            " regola dice di RELAZIONARE coi numeri e NON di scegliere un altro schema,"
            " quindi questo ALZA invece di fermarsi a un valore qualunque"
            % (GIRI_MAX_PESO, scarto))
    # ### ✅ **E ADESSO IL PEZZO INTERO, dallo stato VERO, col peso del punto medio.**
    phi[...] = salvo
    hop_phi_con_s(mot, phi, s.copy(), frazione)
    mot.giri_peso = giri
    return phi


def hop_phi_con_s(mot, phi, s, frazione):
    """### `hop(theta)` sul vuoto, col peso ### **DATO.** ### **Il corpo di `hop_phi`.**"""
    m = mot.inc.m
    v = phi.reshape(m, 2)
    al, be = _alfa_beta(mot, z_arco_da_s(mot, s, frazione))
    a1 = al.reshape(-1)
    b1 = be.reshape(-1)
    # ### ⭐ **DUE buffer anche qui**, e per lo stesso motivo: il lato `1` vecchio si
    # ### usa ### **in posto.**
    t0 = mot._b("fp_phi_lato0", (m,), phi.dtype)
    tm = mot._b("fp_phi_misto", (m,), phi.dtype)
    t0[...] = v[:, 0]
    np.multiply(v[:, 1], b1, out=tm)
    np.multiply(t0, a1, out=v[:, 0])
    np.add(v[:, 0], tm, out=v[:, 0])
    np.multiply(t0, b1, out=tm)
    np.multiply(v[:, 1], a1, out=v[:, 1])
    np.add(v[:, 1], tm, out=v[:, 1])
    return phi
