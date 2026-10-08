# -*- coding: utf-8 -*-
"""IL PROTOTIPO AL PRIMO ORDINE — un banco per `A16`, FUORI dal simulatore.

### ⛔ **NON IMPORTA `soliton_simulator.py`, e lo ASSERISCE** *(non e' una promessa:
`_niente_simulatore()` guarda `sys.modules` e FERMA)*.

LA FORMA, da `A16`:

    psi_k in C^2,  phi_k SI LEGGE da psi_k  (non e' una variabile)
    H(psi) = - somma_archi w_ij ( <psi_i|U_ij|psi_j> + c.c. )  +  (g/2) somma_k |psi_k|^4
    i dpsi_k/dt = dH/dpsi_k*  =  - somma_{j~k} w_kj U_kj psi_j  +  g |psi_k|^2 psi_k

### ⚠ **`w` e `U` SONO FISSI, ED E' UNA VIOLAZIONE DICHIARATA DI `A16.3`:** sono memorie
congelate. `A16.3` vuole memorie come gradi di liberta' lenti DENTRO `H`, con la loro parte di
energia. ### **Questa e' la PRIMA versione, e la memoria dinamica e' il passo successivo --
decisione di Luca.**

Criteri e previsioni: `doc/TASK_HISTORY/2026-10-08_proto-primo-ordine.md`, committato PRIMA.
"""
import io
import json
import os
import sys
import time

import numpy as np

# ============================================================================
#   ### 📌 **IL PRESIDIO DELL ENCODING, FATTO A MANO -- e la NONA volta che serve**
# ============================================================================
# ### ⛔ **`# -*- coding: utf-8 -*-` NON BASTA:** riguarda il SORGENTE, non lo STDOUT.
#   Su Windows la console e' `cp1252` e un `print` con un carattere fuori da quella
#   tabella ### **SOLLEVA**, e porta giu' la corsa.
#   ### ⚠ **E` SUCCESSO QUI, alla prima corsa del collaudo:** `UnicodeEncodeError` su
#   `⛔`, ### **dopo** che `(a)` e `(b)` erano passati -- e li ho persi.
#   ### **Il repo ha `csv/_presidio.py` che fa questo, ma il prototipo NON deve
#   dipendere da `csv/`: quindi fa da se' l equivalente, e lo DICHIARA.**
for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                          # noqa: BLE001
        pass

_QUI = os.path.dirname(os.path.abspath(__file__))
FUORI = os.path.join(_QUI, "uscite")
NL = chr(10)

# ============================================================================
#   I NUMERI DEL BANCO — ### **dichiarati QUI, non scelti dopo**
# ============================================================================
N_NODI = 400                 # ### nell'intervallo 300-500 del mandato
LATO = 1.0                   # ### il cubo
R_ARCO = 0.22                # ### arco se d <= R; da' grado medio ~16, e SI MISURA
LAM_P = R_ARCO / 2.0         # ### la scala del peso: w = exp(-d/LAM_P)
SIGMA_PACCO = 2.0 * R_ARCO   # ### la larghezza del pacchetto iniziale
G_SCANSIONE = (0.0, -2.0, -5.0, -10.0, -20.0)    # ### CINQUE valori, dichiarati prima
# ============================================================================
#   ### ⭐ **I NUMERI DEL MARE** *(esperimento 2, idea di Luca)*
# ============================================================================
# ### ⛔ **`RHO_0 = 1`, E IL PERCHE' CONTA:** con norma totale `1` si avrebbe
#   `rho_0 = 1/400 = 0.0025`, e il termine non lineare `g*rho_0` sarebbe `0.05` a
#   `g = -20` contro una scala di salto `~5`: ### **la non linearita' sarebbe
#   NEGLIGIBILE per costruzione, e non succederebbe niente.** Con `rho_0 = 1` il
#   confronto e' `g` contro `~5`. ### **E' un numero di banco, ed e' dichiarato.**
RHO_0 = 1.0
EPS_MARE = 0.01            # ### il disturbo di fase, in radianti
PASSI_MARE = 5000          # ### `T = PASSI_MARE * DT = 10`, riportato in unita' di `t_c`
CAMPIONI_MARE = 50         # ### ogni quanti passi si campiona per la VITA dei grumi
SOGLIA_GRUMO = 3.0         # ### `rho > 3 * media`: la soglia del mandato
SEMI = (11, 12, 13)          # ### TRE semi. ### **`P3` NON e' soddisfatta, e si dice**
DT = 0.002                   # ### il passo
PASSI = 4000                 # ### la corsa dell'esperimento
TOLL_ITER = 1e-13            # ### la tolleranza del punto medio: MOLTO sotto 1e-8
MAX_ITER = 60                # ### e il tetto, con il numero di iterazioni MISURATO
# ### ⭐ **I DUE BRACCI (integrazione del guardiano, 2026-10-08):** un campo `SU(2)`
#   casuale ### **localizza da se'** *(Anderson con flusso di gauge casuale)*, quindi il
#   confronto a `g = 0` ### **non distingue** il disordine del GRAFO da quello di `U`.
#   ### ➜ **Due bracci separano le due sorgenti.**
BRACCI = ("U-CASO", "U-UNO")
P = []


_SCRIVI_SU = [None]


def stampa(s=""):
    """### ⚠ **E SI SCRIVE MAN MANO, non alla fine:** il crash di encoding della prima
    corsa ha portato via `(a)` e `(b)`, che erano GIA' passati. Un referto che esiste solo
    se il programma finisce ### **non e' un referto.**
    """
    P.append(s)
    print(s, flush=True)
    if _SCRIVI_SU[0]:
        try:
            io.open(_SCRIVI_SU[0], "w", encoding="utf-8").write(NL.join(P) + NL)
        except Exception:                                          # noqa: BLE001
            pass


def riga(c="-", n=104):
    stampa(c * n)


def _niente_simulatore():
    """### ⛔ **IL CONTROLLO CHE IL PROTOTIPO NON IMPORTI IL SIMULATORE.**

    Non e' una dichiarazione: guarda `sys.modules` e ### **FERMA** se lo trova.
    """
    cattivi = [m for m in sys.modules if "soliton_simulator" in m]
    if cattivi:
        raise SystemExit("[FERMO] il prototipo ha importato il simulatore: %r" % cattivi)
    return True


# ============================================================================
#   IL GRAFO
# ============================================================================
def grafo(seme, n=N_NODI, lato=LATO, r=R_ARCO, u_identita=False):
    """Grafo geometrico casuale in `3D`: arco se `d_ij <= r`. ### **Il grado si
    MISURA.**

    ### ⭐ **`u_identita=True` da' il braccio `U-UNO`:** `U_ij = I` su tutti gli archi,
    ### **stesso grafo, stesse posizioni, stessi pesi** -- cambia ### **solo** il
    trasporto. ### ⛔ **E le estrazioni casuali di `U` si fanno COMUNQUE**, cosi' il
    `rng` avanza allo stesso modo nei due bracci e ### **il grafo e' IDENTICO**: se non
    lo facessi, i due bracci avrebbero grafi diversi e il confronto non isolerebbe `U`.
    """
    rng = np.random.default_rng(seme)
    pos = rng.uniform(0.0, lato, size=(n, 3))
    d2 = ((pos[:, None, :] - pos[None, :, :]) ** 2).sum(-1)
    iu = np.triu_indices(n, 1)
    m = d2[iu] <= r * r
    ii, jj = iu[0][m], iu[1][m]
    d = np.sqrt(d2[ii, jj])
    w = np.exp(-d / LAM_P)
    # --- ### `U_ij` in `SU(2)`, casuale ma ### **FISSA**, con `U_ji = U_ij^dag` per
    #     costruzione *(si usa `U` nel verso `i->j` e il coniugato trasposto nell'altro)*
    a = rng.normal(size=len(ii)) + 1j * rng.normal(size=len(ii))
    b = rng.normal(size=len(ii)) + 1j * rng.normal(size=len(ii))
    nn = np.sqrt(np.abs(a) ** 2 + np.abs(b) ** 2)
    a, b = a / nn, b / nn
    U = np.zeros((len(ii), 2, 2), complex)
    U[:, 0, 0] = a
    U[:, 0, 1] = -np.conj(b)
    U[:, 1, 0] = b
    U[:, 1, 1] = np.conj(a)
    if u_identita:
        # ### ⚠ **LE ESTRAZIONI SONO GIA' STATE FATTE, di proposito:** il grafo resta
        #   ### **identico** al braccio `U-CASO`, e cambia SOLO il trasporto.
        U[:] = 0.0
        U[:, 0, 0] = 1.0
        U[:, 1, 1] = 1.0
    grado = np.zeros(n, int)
    np.add.at(grado, ii, 1)
    np.add.at(grado, jj, 1)
    return {"pos": pos, "i": ii, "j": jj, "d": d, "w": w, "U": U, "n": n,
            "u_identita": bool(u_identita),
            "grado_medio": float(np.mean(grado)), "grado_min": int(grado.min()),
            "grado_max": int(grado.max()), "archi": int(len(ii)),
            "isolati": int(np.sum(grado == 0))}


def unitarie(G):
    """### ✔ **`U` E' UNITARIA, e si VERIFICA** *(non si assume dalla costruzione)*."""
    U = G["U"]
    I = np.eye(2)[None, :, :]
    p = np.einsum("kab,kcb->kac", U, np.conj(U))
    return float(np.max(np.abs(p - I)))


# ============================================================================
#   `H`, LA FORZA, E LE MISURE
# ============================================================================
def energia(G, psi, g):
    """`H = - somma_archi w (<psi_i|U|psi_j> + c.c.) + (g/2) somma |psi|^4`.

    ### ✔ **E` REALE PER COSTRUZIONE:** il termine d'arco e' `z + conj(z) = 2 Re(z)`, e
    questa e' esattamente l'hermitianita' che `U_ji = U_ij^dag` garantisce.
    """
    ii, jj, w, U = G["i"], G["j"], G["w"], G["U"]
    wi = np.conj(psi[ii])
    wj = psi[jj]
    ov = (wi[:, 0] * (U[:, 0, 0] * wj[:, 0] + U[:, 0, 1] * wj[:, 1])
          + wi[:, 1] * (U[:, 1, 0] * wj[:, 0] + U[:, 1, 1] * wj[:, 1]))
    lin = -2.0 * float(np.sum(w * np.real(ov)))
    # ### ⛔ **`|psi_k|^2` E' LA NORMA SPINORIALE DEL NODO, non il modulo di una
    #   componente:** `A16` scrive `(g/2) somma_k |psi_k|^4`, e in `C^2` quello e'
    #   `(|a_k|^2 + |b_k|^2)^2`.
    #   ### ⚠ **LA PRIMA STESURA SOMMAVA `|psi_kc|^4` PER COMPONENTE**, cioe' una `H`
    #   DIVERSA da quella di cui `forza` e' il gradiente -- e il collaudo (a) l'ha presa:
    #   deriva dell energia `2.408e-03`, ### **identica prima e dopo la cura sul gradiente
    #   discreto**, e un numero che non si muove dopo una cura dice che la cura non ha
    #   toccato la causa. ### **Era questa.**
    rho = np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2
    nl = 0.5 * g * float(np.sum(rho ** 2))
    return lin + nl


def forza(G, psi, g, rho_med=None):
    """`F_k = dH/dpsi_k*`, come ### **GRADIENTE DISCRETO** quando `rho_med` e' dato.

    ### **L'evoluzione e' `i dpsi/dt = F`**, cioe' `dpsi/dt = -i F`.

    ### ⛔ **IL `rho_med`, E PERCHE' C'E':** per uno schema `delta = -i dt F` con
    `delta = psi' - psi`, l'energia si conserva ### **esattamente** se `F` e' il
    ### **gradiente DISCRETO** di `H`, perche' allora

        DH = 2 Re[somma conj(delta) F] = 2 dt Re[i |F|^2] = 0

    Sulla parte ### **quadratica** il punto medio basta: `psi'* A psi' - psi* A psi
    = 2 Re[delta* A psi_mid]`. ### ⚠ **Sulla parte QUARTICA NO:** per
    `H_nl = (g/2) somma |psi|^4` serve

        G = g * rho_med * psi_mid      con   rho_med = (|psi|^2 + |psi'|^2) / 2

    e allora `2 Re[conj(delta) G] = (g/2) somma(|psi'|^4 - |psi|^4)` ### **esatto**.
    ### ⛔ **LA PRIMA STESURA USAVA `|psi_mid|^2`, e il collaudo (a) l'ha PRESA:**
    norma conservata a `3.706e-13` *(il moltiplicatore e' reale)* ma energia a
    ### **`2.408e-03`** contro una soglia di `1e-8`. ### **La cura e' DERIVATA, non tarata**
    *(e' lo schema di Delfour-Fortin-Payre)*.
    """
    ii, jj, w, U, n = G["i"], G["j"], G["w"], G["U"], G["n"]
    F = np.zeros((n, 2), complex)
    # --- ### `i -> j`: `U` ; ### `j -> i`: `U^dag`
    Upj = np.empty_like(psi[jj])
    Upj[:, 0] = U[:, 0, 0] * psi[jj][:, 0] + U[:, 0, 1] * psi[jj][:, 1]
    Upj[:, 1] = U[:, 1, 0] * psi[jj][:, 0] + U[:, 1, 1] * psi[jj][:, 1]
    Udi = np.empty_like(psi[ii])
    Udi[:, 0] = np.conj(U[:, 0, 0]) * psi[ii][:, 0] + np.conj(U[:, 1, 0]) * psi[ii][:, 1]
    Udi[:, 1] = np.conj(U[:, 0, 1]) * psi[ii][:, 0] + np.conj(U[:, 1, 1]) * psi[ii][:, 1]
    np.add.at(F, ii, -(w[:, None] * Upj))
    np.add.at(F, jj, -(w[:, None] * Udi))
    if rho_med is None:
        rho_med = np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2
    F += g * rho_med[:, None] * psi
    return F


def norma(psi):
    return float(np.sum(np.abs(psi) ** 2))


def partecipazione(psi):
    """`PR = 1 / somma_k rho_k^2` con `somma rho = 1`: ### **i nodi su cui lo stato e'
    spalmato.**"""
    rho = np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2
    s = rho.sum()
    if s <= 0:
        return 0.0
    rho = rho / s
    return float(1.0 / np.sum(rho ** 2))


def fase_da_psi(psi):
    """### ⭐ **`phi` SI LEGGE DA `psi`, non e' una variabile** *(`A16.1`)*.

    `phi_k = 2 * arg(componente dominante)`, nel dominio `[0, 4 pi)`.
    ### **La convenzione si DICHIARA:** si prende la componente di modulo maggiore, cosi'
    `arg` e' ben definito anche al polo.
    """
    k = (np.abs(psi[:, 1]) > np.abs(psi[:, 0])).astype(int)
    comp = psi[np.arange(len(psi)), k]
    return (2.0 * np.angle(comp)) % (4.0 * np.pi)


# ============================================================================
#   L'INTEGRATORE — ### **PUNTO MEDIO IMPLICITO**
# ============================================================================
def passo_punto_medio(G, psi, g, dt=DT, toll=TOLL_ITER, maxit=MAX_ITER):
    """`psi' = psi - i dt F((psi + psi')/2)`, risolto per ### **iterazione di punto fisso**.

    ### ⭐ **PERCHE' QUESTO:** sulla parte ### **lineare** e' la trasformata di Cayley, che e'
    ### **unitaria ESATTAMENTE** -- la norma non deriva. E per una `H` reale e' ### **simmetrico
    nel tempo**, quindi l'errore sull'energia ### **non cresce** monotonamente.
    ### ⛔ **NON `RK4`:** non conserva la norma e la fa derivare, e su `10^4` passi la deriva
    sarebbe il risultato invece dell'errore.
    ### ⚠ **E IL COSTO E' DICHIARATO:** l'iterazione ha una tolleranza *(un numero)*, e
    ### **il numero di iterazioni si MISURA e si riporta.**
    """
    nuovo = psi.copy()
    it = 0
    rho0 = np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2
    for it in range(1, maxit + 1):
        mezzo = 0.5 * (psi + nuovo)
        # ### ⭐ **IL GRADIENTE DISCRETO: la densita' e' la MEDIA DEI DUE ESTREMI**,
        #   non quella al punto medio. ### **E' cio' che rende l'energia conservata
        #   ESATTAMENTE** *(vedi il docstring di `forza`)*.
        rho1 = np.abs(nuovo[:, 0]) ** 2 + np.abs(nuovo[:, 1]) ** 2
        cand = psi - 1j * dt * forza(G, mezzo, g, rho_med=0.5 * (rho0 + rho1))
        err = float(np.max(np.abs(cand - nuovo)))
        nuovo = cand
        if err <= toll:
            break
    return nuovo, it, err


# ============================================================================
#   IL COLLAUDO — ### **i quattro controlli del mandato**
# ============================================================================
def catena(n=160, passo=1.0):
    """Catena `1D`, `U = I`, ### **una sola componente attiva**: il banco della `DNLS`."""
    ii = np.arange(n - 1)
    jj = ii + 1
    U = np.zeros((n - 1, 2, 2), complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    return {"pos": (np.arange(n) * passo)[:, None], "i": ii, "j": jj,
            "d": np.full(n - 1, passo), "w": np.ones(n - 1), "U": U, "n": n,
            "grado_medio": 2.0 * (n - 1) / n, "grado_min": 1, "grado_max": 2,
            "archi": int(n - 1), "isolati": 0}


def solitone_discreto(n, x, x0, LARG, g, toll=1e-14, maxit=200):
    """### ⭐ **IL SOLITONE DISCRETO ESATTO, con Newton** -- e non il `sech`.

    Sulla catena l equazione STAZIONARIA della mia discretizzazione e'

        -(u_{k-1} + u_{k+1} - 2 u_k) + g |u_k|^2 u_k = mu u_k

    *(la diagonale `-2` e' tolta col fattore `e^{2it}`, come nel docstring di `(b)`)*.
    ### **Il `sech` e' la soluzione del limite CONTINUO**, non di questa: si parte da
    lui e si risolve con ### **Newton** su `u` reale, a `mu` FISSO.
    ### ✔ **E il residuo dell equazione si RESTITUISCE**, cosi' il collaudo verifica
    che il punto trovato sia ### **davvero** stazionario invece di fidarsi di Newton.
    """
    eta = 1.0 / LARG
    u = (eta * np.sqrt(2.0 / abs(g)) / np.cosh(eta * (x - x0)))
    # ### `mu` del limite continuo: `-eta^2` *(il solitone e' legato)*
    mu = -eta ** 2

    def resid(v):
        lap = np.zeros(n)
        lap[1:-1] = v[:-2] + v[2:] - 2.0 * v[1:-1]
        lap[0] = v[1] - 2.0 * v[0]
        lap[-1] = v[-2] - 2.0 * v[-1]
        return -lap + g * v ** 3 - mu * v

    it = 0
    for it in range(1, maxit + 1):
        r = resid(u)
        # ### la jacobiana: tridiagonale, e si risolve con `np.linalg.solve` *(n = 160:
        #   densa va benissimo, e NON e' il collo di bottiglia)*
        J = np.zeros((n, n))
        np.fill_diagonal(J, 2.0 + 3.0 * g * u ** 2 - mu)
        idx = np.arange(n - 1)
        J[idx, idx + 1] = -1.0
        J[idx + 1, idx] = -1.0
        du = np.linalg.solve(J, r)
        u = u - du
        if float(np.max(np.abs(du))) <= toll:
            break
    return u, mu, float(np.max(np.abs(resid(u)))), it


def collaudo():
    _niente_simulatore()
    esiti = []

    def prova(et, ok):
        esiti.append(bool(ok))
        stampa("  %s  %s" % ("ok  " if ok else "FALLITO", et))
        return bool(ok)

    os.makedirs(FUORI, exist_ok=True)
    _SCRIVI_SU[0] = os.path.join(FUORI, "collaudo.txt")
    riga("=")
    stampa("IL COLLAUDO DEL PROTOTIPO AL PRIMO ORDINE")
    riga("=")
    prova("il prototipo ### **NON ha importato il simulatore** *(guardato in `sys.modules`, "
          "non dichiarato)*", True)
    G = grafo(SEMI[0])
    stampa("  grafo: n = %d, archi = %d, grado medio %.2f (min %d, max %d), isolati %d"
           % (G["n"], G["archi"], G["grado_medio"], G["grado_min"], G["grado_max"],
              G["isolati"]))
    prova("grafo: ### `U` e' UNITARIA su tutti gli archi *(scarto massimo da `I`: `%.3e`)*"
          % unitarie(G), unitarie(G) < 1e-12)
    prova("grafo: ### **nessun nodo isolato** *(un nodo isolato non evolverebbe, e sarebbe un "
          "pezzo di stato fuori dalla dinamica)*", G["isolati"] == 0)
    # ---- ### **(a) NORMA ED ENERGIA su `10^4` passi**
    rng = np.random.default_rng(7)
    psi = (rng.normal(size=(G["n"], 2)) + 1j * rng.normal(size=(G["n"], 2)))
    psi /= np.sqrt(norma(psi))
    g = -5.0
    n0, e0 = norma(psi), energia(G, psi, g)
    t0 = time.time()
    its = []
    for _k in range(10000):
        psi, it, _e = passo_punto_medio(G, psi, g)
        its.append(it)
    dn = abs(norma(psi) - n0) / abs(n0)
    de = abs(energia(G, psi, g) - e0) / max(abs(e0), 1e-300)
    stampa("  (a) %d passi in %.1f s; iterazioni del punto medio: mediana %d, massimo %d"
           % (10000, time.time() - t0, int(np.median(its)), int(np.max(its))))
    prova("(a) ### **la NORMA si conserva**: deriva relativa `%.3e` su `10^4` passi "
          "*(soglia `1e-8`)*" % dn, dn < 1e-8)
    prova("(a) ### **l'ENERGIA si conserva**: deriva relativa `%.3e` su `10^4` passi "
          "*(soglia `1e-8`)*" % de, de < 1e-8)
    prova("(a) ### e l'iterazione ### **converge sempre** entro il tetto *(massimo %d su %d)*"
          % (int(np.max(its)), MAX_ITER), int(np.max(its)) < MAX_ITER)
    # ---- ### **(b) IL CONTROLLO POSITIVO: IL SOLITONE DELL EQUAZIONE CHE INTEGRO**
    #      ### \u26d4 **DUE GIRI SBAGLIATI, MIEI, PRIMA DI ARRIVARE QUI, e li scrivo:**
    #      `(1)` avevo normalizzato il `sech` a norma `1`, distruggendo la relazione
    #      ampiezza-larghezza che ### **fa** di quel profilo un solitone *(`3.373e-01`)*;
    #      `(2)` poi avevo chiamato il residuo <<discretizzazione spaziale>> e messo un test
    #      sulla LARGHEZZA che ### **non discriminava**, perche' scalavo `dt` come `LARG^2` e
    #      l errore temporale restava fisso ### **per costruzione**;
    #      `(3)` e il test sul `dt` ha dato ### **lo STESSO numero a quattro cifre**
    #      *(`1.903e-03` a `dt` e a `dt/2`, fattore `1.00`)*: una quantita' che non si muove
    #      dimezzando il passo ### **non e' un errore di integrazione.**
    #      ### \u2b50 **L IPOTESI CHE RESTAVA: il `sech` e' il solitone del limite CONTINUO,
    #      non uno stato stazionario dell equazione DISCRETA.** E un'ipotesi non e' una
    #      misura: si ### **COSTRUISCE** il solitone discreto esatto con Newton, si
    #      ### **VERIFICA** che sia stazionario, e si propaga ### **QUELLO.**
    C = catena()
    x = C["pos"][:, 0]
    x0 = x[len(x) // 2]
    gs = -1.0
    LARG = 8.0
    eta = 1.0 / LARG
    t_c = 1.0 / (eta ** 2)
    # ### il solitone CONTINUO, per misurare lo SCARTO fra continuo e discreto
    A = eta * np.sqrt(2.0 / abs(gs))
    cont = A / np.cosh(eta * (x - x0))
    u, mu, res_staz, nit = solitone_discreto(C["n"], x, x0, LARG, gs)
    prova("(b) ### **IL SOLITONE DISCRETO E' STAZIONARIO**, e si verifica: residuo "
          "dell equazione `%.3e` dopo `%d` passi di Newton *(soglia `1e-12`)*"
          % (res_staz, nit), res_staz < 1e-12)
    _sc_cd = float(np.max(np.abs(u - cont))) / max(float(np.max(np.abs(cont))), 1e-300)
    stampa("  (b) `mu` = %.6f, `max u` = %.6f *(continuo: %.6f)*, e lo SCARTO fra solitone "
           "CONTINUO e DISCRETO e' ### **%.3e**" % (mu, float(np.max(u)), float(np.max(cont)),
                                                    _sc_cd))
    psi1 = np.zeros((C["n"], 2), complex)
    psi1[:, 0] = u
    p_in = np.abs(psi1[:, 0]).copy()
    npassi = int(10.0 * t_c / DT)
    stampa("  (b) catena n = %d, LARG = %.1f, eta = %.5f, t_c = %.1f, dt = %.5f, "
           "passi = %d, norma = %.6f" % (C["n"], LARG, eta, t_c, DT, npassi, norma(psi1)))
    ps = psi1.copy()
    dev = []
    for _k in range(npassi):
        ps, _it, _e = passo_punto_medio(C, ps, gs)
        if _k % 2000 == 0:
            dev.append(float(np.max(np.abs(np.abs(ps[:, 0]) - p_in)))
                       / max(float(np.max(p_in)), 1e-300))
    p_out = np.abs(ps[:, 0])
    k_in, k_out = int(np.argmax(p_in)), int(np.argmax(p_out))
    sp = np.roll(p_out, k_in - k_out)
    scarto = float(np.max(np.abs(sp - p_in))) / max(float(np.max(p_in)), 1e-300)
    prova("(b) ### **IL SOLITONE DISCRETO SI PROPAGA INTATTO**: scarto massimo sul profilo "
          "`%.3e` dopo `10` tempi caratteristici *(soglia `1e-3`)*" % scarto, scarto < 1e-3)
    prova("(b) ### \u2b50 **E QUESTO DIMOSTRA L ATTRIBUZIONE del residuo di prima:** col "
          "`sech` CONTINUO lo scarto era `1.903e-03` *(e non calava ne' con `dt` ne' con la "
          "larghezza)*; col solitone ### **DELL EQUAZIONE** e' `%.3e`. ### \u27a5 **Quel "
          "residuo era lo SCARTO CONTINUO-DISCRETO, misurato `%.3e` sul profilo iniziale, "
          "non un difetto dello schema**" % (scarto, _sc_cd), scarto < 1.903e-03 / 10.0)
    stampa("  (b) la deviazione nel tempo *(ogni 2000 passi)*: %s"
           % " ".join("%.2e" % d for d in dev[:8]))
    prova("(b) ### e il `PR` ### **NON cresce**: da `%.2f` a `%.2f`"
          % (partecipazione(psi1), partecipazione(ps)),
          partecipazione(ps) < 1.1 * partecipazione(psi1))
    dtb = DT
    # ---- ### ⛔ **(c) IL CASO CHE DEVE FALLIRE: con `g = 0` si DISPERDE**
    ps0 = psi1.copy()
    for _k in range(npassi):
        ps0, _it, _e = passo_punto_medio(C, ps0, 0.0, dt=dtb)
    p0 = np.abs(ps0[:, 0])
    k0 = int(np.argmax(p0))
    sp0 = np.roll(p0, k_in - k0)
    sc0 = float(np.max(np.abs(sp0 - p_in))) / max(float(np.max(p_in)), 1e-300)
    pr_in, pr_0, pr_g = partecipazione(psi1), partecipazione(ps0), partecipazione(ps)
    prova("(c) ### ⛔ **DEVE FALLIRE -- con `g = 0` il profilo SI DISPERDE**: scarto `%.3e` "
          "*(contro `%.3e` con `g != 0`)*, e il `PR` va da `%.2f` a ### **`%.2f`** "
          "*(con `g != 0`: `%.2f`)*" % (sc0, scarto, pr_in, pr_0, pr_g), sc0 > 1e-2)
    # ---- ### **(d) LA DOPPIA COPERTURA**
    ps2 = psi1.copy()
    k_un = int(np.argmax(np.abs(ps2[:, 0])))
    e_pre = energia(C, ps2, gs)
    ps2[k_un] = -ps2[k_un]                     # ### `phi -> phi + 2 pi`  =>  `psi -> -psi`
    e_2pi = energia(C, ps2, gs)
    ps2[k_un] = -ps2[k_un]                     # ### e di nuovo: `+4 pi`  =>  identico
    e_4pi = energia(C, ps2, gs)
    prova("(d) ### **la DOPPIA COPERTURA si vede su `H`**: `phi_k + 2pi` su UN nodo cambia "
          "l'energia da `%.6f` a `%.6f` *(differenza `%.6f`)*" % (e_pre, e_2pi, e_2pi - e_pre),
          abs(e_2pi - e_pre) > 1e-9)
    prova("(d) ### e `phi_k + 4pi` la riporta ### **IDENTICA** *(scarto `%.3e`)*"
          % abs(e_4pi - e_pre), abs(e_4pi - e_pre) <= 1e-12 * max(abs(e_pre), 1.0))
    # ---- ### e che `phi` si LEGGA da `psi`
    _ph = fase_da_psi(ps)
    prova("`phi` SI LEGGE da `psi` e sta in `[0, 4pi)` *(min `%.4f`, max `%.4f`)*: "
          "### **non e' una variabile** *(`A16.1`)*"
          % (float(_ph.min()), float(_ph.max())),
          float(_ph.min()) >= 0.0 and float(_ph.max()) < 4.0 * np.pi + 1e-12)
    riga("-")
    stampa("  COLLAUDO: %d su %d" % (sum(esiti), len(esiti)))
    if not all(esiti):
        stampa("### FERMO: il collaudo NON chiude, e le corse NON partono.")
    return 0 if all(esiti) else 1


# ============================================================================
#   L'ESPERIMENTO
# ============================================================================
def mare(G, seme, eps=EPS_MARE, rho0=RHO_0):
    """### ⭐ **IL MARE: `|psi|` UGUALE su tutti i nodi, nessuna concentrazione.**

    `psi_k = e^{i phi_k / 2} * chi_0` con `chi_0 = (1, 0)` e
    `phi_k = phi_0 + disturbo`, disturbo uniforme in `[-eps, +eps]`.
    ### ⛔ **Il modulo e' COSTANTE:** `|psi_k|^2 = rho0` su ogni nodo. ### **Se un
    grumo nasce, nasce dall INTERFERENZA, non da una concentrazione messa a mano.**
    ### ⚠ **E con `eps = 0` il mare e' PERFETTAMENTE uniforme:** e' il caso che
    ### **deve fallire**, perche' la simmetria ### **non si rompe da sola.**
    """
    rng = np.random.default_rng(1000 + seme)
    n = G["n"]
    ph = rng.uniform(-eps, eps, size=n) if eps > 0 else np.zeros(n)
    psi = np.zeros((n, 2), complex)
    psi[:, 0] = np.sqrt(rho0) * np.exp(0.5j * ph)
    return psi


def grumi(G, psi, soglia=SOGLIA_GRUMO):
    """### ⭐ **I GRUMI: `rho > soglia * media`, in COMPONENTI CONNESSE SUL GRAFO.**

    ### ✔ **Per ciascuno si danno norma ed energia**, e l energia e' il termine non
    lineare dei suoi nodi ### **piu'** i salti con ### **ENTRAMBI** gli estremi dentro.
    ### ⛔ **I salti che ATTRAVERSANO il bordo NON si attribuiscono a nessun grumo** e si
    riportano ### **a parte**: metterli d autorita' dentro falserebbe il bilancio -- e
    e' la stessa regola delle tre classi di `D3`.
    """
    n = int(G["n"])
    rho = np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2
    med = float(np.mean(rho))
    dentro = rho > soglia * med
    if not np.any(dentro):
        return [], {"media_rho": med, "nodi_sopra_soglia": 0,
                    "rho_massimo_su_media": float(rho.max() / max(med, 1e-300))}
    # ### le componenti connesse del SOTTOGRAFO indotto, con una visita in ampiezza
    vicini = [[] for _ in range(n)]
    ii, jj = G["i"], G["j"]
    for a, b in zip(ii.tolist(), jj.tolist()):
        if dentro[a] and dentro[b]:
            vicini[a].append(b)
            vicini[b].append(a)
    visto = np.zeros(n, bool)
    comp = []
    for s in np.flatnonzero(dentro):
        if visto[s]:
            continue
        coda = [int(s)]
        visto[s] = True
        gr = []
        while coda:
            v = coda.pop()
            gr.append(v)
            for w2 in vicini[v]:
                if not visto[w2]:
                    visto[w2] = True
                    coda.append(w2)
        comp.append(sorted(gr))
    return comp, {"media_rho": med, "nodi_sopra_soglia": int(np.sum(dentro)),
                  "rho_massimo_su_media": float(rho.max() / max(med, 1e-300))}


def misura_grumi(G, psi, g, comp):
    """Per ogni grumo: norma, energia, nodo di picco. ### **E i salti di bordo A PARTE.**
    """
    ii, jj, w, U = G["i"], G["j"], G["w"], G["U"]
    rho = np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2
    wi = np.conj(psi[ii])
    wj = psi[jj]
    ov = (wi[:, 0] * (U[:, 0, 0] * wj[:, 0] + U[:, 0, 1] * wj[:, 1])
          + wi[:, 1] * (U[:, 1, 0] * wj[:, 0] + U[:, 1, 1] * wj[:, 1]))
    e_arco = -2.0 * w * np.real(ov)
    fuori = []
    bordo_tot = 0.0
    for gr in comp:
        ins = np.zeros(int(G["n"]), bool)
        ins[gr] = True
        a_dentro = ins[ii] & ins[jj]
        a_bordo = ins[ii] ^ ins[jj]
        nor = float(np.sum(rho[gr]))
        ene = float(np.sum(e_arco[a_dentro])) + 0.5 * g * float(np.sum(rho[gr] ** 2))
        bordo = float(np.sum(e_arco[a_bordo]))
        bordo_tot += bordo
        k_pic = int(gr[int(np.argmax(rho[gr]))])
        fuori.append({"nodi": len(gr), "norma": nor, "energia": ene,
                      "energia_per_norma": (ene / nor) if nor else None,
                      "salti_di_bordo": bordo, "nodo_picco": k_pic,
                      "rho_picco": float(rho[k_pic])})
    return fuori, bordo_tot


def pacchetto(G, sigma=SIGMA_PACCO):
    """Gaussiana centrata sul nodo piu' vicino al centro del cubo, ### **normalizzata**."""
    c = np.array([LATO / 2.0] * 3)
    d = np.linalg.norm(G["pos"] - c[None, :], axis=1)
    k0 = int(np.argmin(d))
    dk = np.linalg.norm(G["pos"] - G["pos"][k0][None, :], axis=1)
    amp = np.exp(-(dk / sigma) ** 2)
    psi = np.zeros((G["n"], 2), complex)
    psi[:, 0] = amp
    psi /= np.sqrt(norma(psi))
    return psi, k0


def corsa(g, seme, braccio="U-CASO", passi=PASSI):
    _niente_simulatore()
    if braccio not in BRACCI:
        raise SystemExit("[FERMO] braccio sconosciuto: %r. I due sono %r."
                         % (braccio, BRACCI))
    G = grafo(seme, u_identita=(braccio == "U-UNO"))
    psi, k0 = pacchetto(G)
    n0, e0 = norma(psi), energia(G, psi, g)
    pr0 = partecipazione(psi)
    ph_prec = fase_da_psi(psi)[k0]
    t0 = time.time()
    curva = []
    its = []
    dphi = []
    for k in range(1, passi + 1):
        psi, it, _e = passo_punto_medio(G, psi, g)
        its.append(it)
        ph = fase_da_psi(psi)[k0]
        _d = (ph - ph_prec + 2.0 * np.pi) % (4.0 * np.pi) - 2.0 * np.pi
        dphi.append(_d / DT)
        ph_prec = ph
        if k % 50 == 0 or k == passi:
            curva.append({"passo": k, "PR": partecipazione(psi),
                          "norma": norma(psi), "H": energia(G, psi, g)})
    rho = np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2
    return {"g": g, "seme": seme, "braccio": braccio, "passi": passi, "secondi": round(time.time() - t0, 1),
            "grafo": {k: G[k] for k in ("n", "archi", "grado_medio", "grado_min",
                                        "grado_max", "isolati", "u_identita")},
            "nodo_centro": k0,
            "PR_iniziale": pr0, "PR_finale": partecipazione(psi),
            "rapporto_PR": partecipazione(psi) / pr0 if pr0 else None,
            "norma_iniziale": n0, "norma_finale": norma(psi),
            "deriva_norma": abs(norma(psi) - n0) / abs(n0),
            "H_iniziale": e0, "H_finale": energia(G, psi, g),
            "deriva_H": abs(energia(G, psi, g) - e0) / max(abs(e0), 1e-300),
            "iterazioni_mediana": int(np.median(its)),
            "iterazioni_massimo": int(np.max(its)),
            # ### ⭐ **l'orologio di de Broglie** *(`A16.2`)*: `dphi/dt` al centro contro
            #   l'energia per particella
            "dphi_dt_centro_mediana": float(np.median(dphi)),
            "dphi_dt_centro_ultimo_quarto": float(np.median(dphi[3 * len(dphi) // 4:])),
            "H_su_norma": e0 / n0 if n0 else None,
            "rho_massimo_finale": float(rho.max()),
            "curva": curva}


def corsa_mare(g, seme, braccio="U-CASO", eps=EPS_MARE, passi=PASSI_MARE):
    """### ⭐ **L ESPERIMENTO DEL MARE: nasce un grumo dall INTERFERENZA?**

    ### **`t_c` NON e' quello del pacchetto:** e' il tempo dell INSTABILITA'
    MODULAZIONALE, che per la `NLS` focalizzante cresce come `1/(|g| rho_0)`.
    ### ⚠ **Per `g = 0` NON e' definito**, e si usa quello di `|g| = 5` -- dichiarato.

    ### **LA VITA DI UN GRUMO:** fra due campioni, un grumo ### **sopravvive** se ne
    esiste uno che ne sovrappone ### **almeno il `50 %`** dei nodi. Le catene di
    sopravvivenze danno la vita, e si riporta ### **in unita' di `t_c`.**
    """
    _niente_simulatore()
    if braccio not in BRACCI:
        raise SystemExit("[FERMO] braccio sconosciuto: %r." % (braccio,))
    G = grafo(seme, u_identita=(braccio == "U-UNO"))
    psi = mare(G, seme, eps=eps)
    n0_, e0 = norma(psi), energia(G, psi, g)
    pr0 = partecipazione(psi)
    # ### `t_c` dell instabilita' modulazionale, e per `g = 0` quello di `|g| = 5`
    g_rif = abs(g) if g != 0.0 else 5.0
    t_c = 1.0 / (g_rif * RHO_0)
    t0 = time.time()
    ph_prec = fase_da_psi(psi)
    curva = []
    vite = []            # ### le vite CHIUSE, in numero di campioni
    attivi = []          # ### i grumi vivi: {"nodi": set, "eta": campioni}
    its = []
    for k in range(1, passi + 1):
        psi, it, _e = passo_punto_medio(G, psi, g)
        its.append(it)
        if k % CAMPIONI_MARE and k != passi:
            continue
        comp, info = grumi(G, psi)
        mis, bordo = misura_grumi(G, psi, g, comp)
        ph = fase_da_psi(psi)
        _d = (ph - ph_prec + 2.0 * np.pi) % (4.0 * np.pi) - 2.0 * np.pi
        dphi = _d / (CAMPIONI_MARE * DT)
        ph_prec = ph
        # ### l OROLOGIO: `dphi/dt` al picco di ogni grumo contro `E/norma`
        for m in mis:
            m["dphi_dt_picco"] = float(dphi[m["nodo_picco"]])
        # ### LA VITA: sovrapposizione `>= 50 %` fra campioni consecutivi
        nuovi = [set(c) for c in comp]
        usati = set()
        prossimi = []
        for a in attivi:
            meglio, quale = 0.0, None
            for idx, s in enumerate(nuovi):
                if idx in usati or not a["nodi"]:
                    continue
                q = len(a["nodi"] & s) / float(len(a["nodi"]))
                if q > meglio:
                    meglio, quale = q, idx
            if quale is not None and meglio >= 0.5:
                usati.add(quale)
                prossimi.append({"nodi": nuovi[quale], "eta": a["eta"] + 1})
            else:
                vite.append(a["eta"])
        for idx, s in enumerate(nuovi):
            if idx not in usati:
                prossimi.append({"nodi": s, "eta": 1})
        attivi = prossimi
        curva.append({"passo": k, "t": k * DT, "t_su_tc": k * DT / t_c,
                      "PR": partecipazione(psi), "norma": norma(psi),
                      "H": energia(G, psi, g), "grumi": len(comp),
                      "nodi_sopra_soglia": info["nodi_sopra_soglia"],
                      "rho_massimo_su_media": info["rho_massimo_su_media"],
                      "media_rho": info["media_rho"],
                      "salti_di_bordo": bordo,
                      "dettaglio_grumi": mis[:8]})
    # ### le vite ancora APERTE alla fine: si contano, e si DICE che sono troncate
    vite_aperte = [a["eta"] for a in attivi]
    dt_camp = CAMPIONI_MARE * DT
    tutte = vite + vite_aperte
    return {"g": g, "seme": seme, "braccio": braccio, "eps": eps, "passi": passi,
            "secondi": round(time.time() - t0, 1),
            "t_c": t_c, "t_finale": passi * DT, "t_finale_su_tc": passi * DT / t_c,
            "g_effettivo": g * RHO_0, "rho_0": RHO_0,
            "grafo": {k: G[k] for k in ("n", "archi", "grado_medio", "u_identita")},
            "PR_iniziale": pr0, "PR_finale": partecipazione(psi),
            "rapporto_PR": partecipazione(psi) / pr0 if pr0 else None,
            "deriva_norma": abs(norma(psi) - n0_) / abs(n0_),
            "deriva_H": abs(energia(G, psi, g) - e0) / max(abs(e0), 1e-300),
            "iterazioni_massimo": int(np.max(its)),
            "grumi_finali": len(attivi),
            "grumi_massimo": max((c["grumi"] for c in curva), default=0),
            "rho_massimo_su_media_massimo": max(
                (c["rho_massimo_su_media"] for c in curva), default=None),
            "vite_chiuse": len(vite), "vite_aperte": len(vite_aperte),
            "vita_massima_campioni": max(tutte, default=0),
            "vita_massima_su_tc": (max(tutte, default=0) * dt_camp / t_c),
            "vita_mediana_su_tc": (float(np.median(tutte)) * dt_camp / t_c
                                   if tutte else 0.0),
            "dt_campione": dt_camp,
            "curva": curva}


def esperimento_mare():
    """### ⭐ **L ESPERIMENTO 2: due bracci, cinque `g`, tre semi, piu' il caso
    `eps = 0` che DEVE fallire.**
    """
    os.makedirs(FUORI, exist_ok=True)
    _SCRIVI_SU[0] = os.path.join(FUORI, "mare.txt")
    riga("=")
    stampa("L ESPERIMENTO DEL MARE -- nascono le masse dall interferenza?")
    riga("=")
    stampa("  i numeri: n = %d, rho_0 = %.3f, eps = %.4f rad, dt = %.4f, passi = %d "
           "(T = %.2f), campione ogni %d passi, soglia grumo = %.1f x media"
           % (N_NODI, RHO_0, EPS_MARE, DT, PASSI_MARE, PASSI_MARE * DT,
              CAMPIONI_MARE, SOGLIA_GRUMO))
    stampa("  ### rho_0 = 1 E NON la norma 1: con norma 1 sarebbe rho_0 = 0.0025 e "
           "g*rho_0 = 0.05 a g = -20, contro una scala di salto ~5 -- la non linearita' "
           "sarebbe NEGLIGIBILE PER COSTRUZIONE. E' un numero di banco, dichiarato.")
    stampa("  ### t_c = 1/(|g| rho_0), il tempo dell INSTABILITA' MODULAZIONALE. Per "
           "g = 0 non e' definito e si usa quello di |g| = 5, dichiarato.")
    fuori = {"esperimento": "mare", "bracci": list(BRACCI),
             "numeri": {"N_NODI": N_NODI, "RHO_0": RHO_0, "EPS_MARE": EPS_MARE,
                        "DT": DT, "PASSI_MARE": PASSI_MARE,
                        "CAMPIONI_MARE": CAMPIONI_MARE,
                        "SOGLIA_GRUMO": SOGLIA_GRUMO,
                        "G_SCANSIONE": list(G_SCANSIONE), "SEMI": list(SEMI)},
             "violazione_dichiarata": "w e U FISSI: memorie congelate, contro A16.3",
             "corse": [], "corse_eps_zero": []}
    t0 = time.time()
    for br in BRACCI:
        stampa()
        stampa("  --- braccio %s: U_ij %s"
               % (br, "CASUALE ma fissa" if br == "U-CASO" else "= IDENTITA'"))
        for g in G_SCANSIONE:
            for s in SEMI:
                r = corsa_mare(g, s, braccio=br)
                fuori["corse"].append(r)
                stampa("  %-7s g = %6.1f seme %d:  grumi max %2d  vita max %6.2f t_c  "
                       "rho_max/media %6.2f  PR %7.2f -> %7.2f  dN %.1e dH %.1e  %.1f s"
                       % (br, g, s, r["grumi_massimo"], r["vita_massima_su_tc"],
                          r["rho_massimo_su_media_massimo"], r["PR_iniziale"],
                          r["PR_finale"], r["deriva_norma"], r["deriva_H"],
                          r["secondi"]))
                if time.time() - t0 > 20 * 60:
                    stampa("### FERMO: oltre i 20 minuti. Le corse fatte SONO SALVATE.")
                    fuori["stato"] = "FERMATO sui 20 minuti"
                    io.open(os.path.join(FUORI, "mare.json"), "w",
                            encoding="utf-8").write(json.dumps(fuori,
                                                               ensure_ascii=False))
                    return 2
    # ---- ### ⛔ **IL CASO CHE DEVE FALLIRE: `eps = 0`**
    stampa()
    stampa("  --- ### ⛔ IL CASO CHE DEVE FALLIRE: eps = 0, mare PERFETTAMENTE "
           "uniforme. ### La simmetria NON si rompe da sola, e se si rompesse sarebbe "
           "UN DIFETTO DEL MIO CODICE, non fisica.")
    for br in BRACCI:
        for s in SEMI:
            r = corsa_mare(-10.0, s, braccio=br, eps=0.0)
            fuori["corse_eps_zero"].append(r)
            stampa("  %-7s g = -10.0 seme %d  eps = 0:  grumi max %d  "
                   "rho_max/media %.6f  PR %7.2f -> %7.2f"
                   % (br, s, r["grumi_massimo"],
                      r["rho_massimo_su_media_massimo"], r["PR_iniziale"],
                      r["PR_finale"]))
    fuori["stato"] = "DATI SALVATI"
    fuori["secondi_totali"] = round(time.time() - t0, 1)
    io.open(os.path.join(FUORI, "mare.json"), "w",
            encoding="utf-8").write(json.dumps(fuori, ensure_ascii=False))
    stampa("  ### I DATI DEL MARE SONO SALVATI (%.1f s in tutto)."
           % (time.time() - t0))
    return 0


def main(argv):
    a = argv[1:]
    os.makedirs(FUORI, exist_ok=True)
    if "--mare" in a:
        return esperimento_mare()
    if "--collaudo" in a:
        e = collaudo()
        io.open(os.path.join(FUORI, "collaudo.txt"), "w",
                encoding="utf-8").write(NL.join(P) + NL)
        return e
    riga("=")
    stampa("L'ESPERIMENTO: %d valori di `g` x %d semi" % (len(G_SCANSIONE), len(SEMI)))
    riga("=")
    stampa("  i numeri del banco: n = %d, R = %.3f, LAM_P = %.3f, sigma = %.3f, "
           "DT = %.4f, passi = %d" % (N_NODI, R_ARCO, LAM_P, SIGMA_PACCO, DT, PASSI))
    stampa("  g: %r      semi: %r      bracci: %r"
           % (list(G_SCANSIONE), list(SEMI), list(BRACCI)))
    stampa("  ### ⭐ I DUE BRACCI (integrazione del guardiano): `U-CASO` con `U` SU(2) "
           "casuale ma fissa, e `U-UNO` con `U = I`. ### Un campo SU(2) casuale "
           "LOCALIZZA DA SE' (Anderson con flusso di gauge), quindi il confronto a "
           "g = 0 da solo NON distingue il disordine del GRAFO da quello di U.")
    stampa("  ### E il grafo e' IDENTICO nei due bracci: le estrazioni casuali di `U` si "
           "fanno comunque, cosi' il `rng` avanza allo stesso modo.")
    stampa("  ### ⚠ `w` e `U` sono FISSI: violazione DICHIARATA di `A16.3` (memorie "
           "congelate). La memoria dinamica dentro `H` e' il passo successivo.")
    fuori = {"bracci": list(BRACCI),
             "numeri_del_banco": {"N_NODI": N_NODI, "LATO": LATO, "R_ARCO": R_ARCO,
                                  "LAM_P": LAM_P, "SIGMA_PACCO": SIGMA_PACCO,
                                  "DT": DT, "PASSI": PASSI, "TOLL_ITER": TOLL_ITER,
                                  "G_SCANSIONE": list(G_SCANSIONE), "SEMI": list(SEMI)},
             "violazione_dichiarata": "w e U FISSI: memorie congelate, contro A16.3",
             "corse": []}
    t0 = time.time()
    for br in BRACCI:
        stampa()
        stampa("  --- braccio %s: U_ij %s"
               % (br, "CASUALE ma fissa" if br == "U-CASO" else "= IDENTITA'"))
        for g in G_SCANSIONE:
            for s in SEMI:
                r = corsa(g, s, braccio=br)
                fuori["corse"].append(r)
                stampa("  %-7s g = %6.1f  seme %d:  PR %8.2f -> %8.2f  (x%.3f)   "
                       "deriva norma %.2e  H %.2e   iter mediana %d   %.1f s"
                       % (br, g, s, r["PR_iniziale"], r["PR_finale"],
                          r["rapporto_PR"], r["deriva_norma"], r["deriva_H"],
                          r["iterazioni_mediana"], r["secondi"]))
                # ### ⛔ **IL TETTO DEL MANDATO: 20 minuti. Se si supera, FERMO.**
                if time.time() - t0 > 20 * 60:
                    stampa("### FERMO: le corse hanno superato i 20 minuti, e il mandato "
                           "dice di fermarsi e scriverlo. Le corse fatte finora SONO "
                           "SALVATE.")
                    fuori["stato"] = "FERMATO sui 20 minuti"
                    io.open(os.path.join(FUORI, "esperimento.json"), "w",
                            encoding="utf-8").write(json.dumps(fuori,
                                                               ensure_ascii=False))
                    io.open(os.path.join(FUORI, "esperimento.txt"), "w",
                            encoding="utf-8").write(NL.join(P) + NL)
                    return 2
    fuori["stato"] = "DATI SALVATI"
    fuori["secondi_totali"] = round(time.time() - t0, 1)
    io.open(os.path.join(FUORI, "esperimento.json"), "w",
            encoding="utf-8").write(json.dumps(fuori, ensure_ascii=False))
    io.open(os.path.join(FUORI, "esperimento.txt"), "w",
            encoding="utf-8").write(NL.join(P) + NL)
    stampa("  ### I DATI SONO SALVATI (%.1f s in tutto)." % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
