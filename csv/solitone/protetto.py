# -*- coding: utf-8 -*-
r"""**IL SOLITONE PROTETTO** *(le espressioni di `_livelli_piatti.scena`, `_massimo_di_B.scena`, `_vuoto_vivo_B.scena`, `_coppia_di_B.coppia`, `_coppia_di_B.residuo`,
`_consolida_B.q_migliore` e `inviluppo`, `_vuoto_vivo_B.partenza`)*: ### **`N`, `eps`, `s`, `L` e la forma come argomenti.**

### **La coppia** e' il livello piu' alto di `A(Gamma)` *(doppio)*, la base QR delle sue due colonne; **`E0 = fase/s`, con `s` della scena** *(`CB.coppia` divideva per il `S` del modulo,
### e `_vuoto_vivo_B.partenza` correggeva con `E0 * CB.S / s`: qui la conversione si fa una volta)*.
### **La scelta dentro la coppia** `q = cos(theta) q1 + e^{i phi} sin(theta) q2` *(theta, phi da `griglia.json` di `_coppia_di_B`)*.
### ⚠ **`DV.matrice` scrive `z["st"]` e lo rimette** *(la guardia di `6c5da5e8`)*; **`mu_rayleigh` fa un tick e lascia `psi_h` scritto:** chi continua nella stessa scena lo rimette.
"""
import contextlib
import json
import math
import os

import numpy as np

from . import RADICE

GRIGLIA = os.path.join(RADICE, "doc", "referti_l2", "coppia_di_B", "griglia.json")


# ====================================================================== LE SCENE
@contextlib.contextmanager
def scena_riferimento(N, L, eps, s, forma):
    """### **La scena di `_livelli_piatti.scena` (`_diagnosi_s4.iniziale`) con `eps` in memoria** *(come `_massimo_di_B.scena`)*: `(rec, z, phi0, pK)`."""
    import _diagnosi_s4 as D
    with D.configura(forma, s, N):
        rec, z = D.iniziale(forma, s, L)
        z["par"]["eps"] = eps
        yield rec, z, z["st"]["phi_h"].copy(), z["st"]["psi_h"].copy()


@contextlib.contextmanager
def scena_vuoto(N, L, eps, s, forma, vuoto):
    """### **La scena di `_vuoto_vivo_B.scena`:** `_deriva_congelato.prepara` a questo `s`, il vuoto `vuoto` *(`"uniforme"` o `"fondo"`)*, `eps` in memoria: `(rec, z, phi0, pK)`."""
    import _deriva_congelato as DC
    import _diagnosi_s4 as D
    with D.configura(forma, s, N):
        rec = DC.prepara(s)
        rec["fattore"] = (L - 0.1) / rec["larghezza"]
        z = DC.nuovo(rec, vuoto)
        assert z["L"] == L, (z["L"], L)
        z["par"]["eps"] = eps
        yield rec, z, z["st"]["phi_h"].copy(), z["st"]["psi_h"].copy()


# ====================================================================== LA COPPIA E LA SCELTA
def coppia(z, phi0, s):
    """### **`(q1, q2, E0, G)`:** le due colonne QR del livello piu' alto di `A(Gamma)`, `E0 = ` la media delle due fasi diviso `s`, `G = A(Gamma)`."""
    import _dove_va_la_materia as DV
    A = DV.matrice(z, phi0, DV.AMP)
    G = A[0, 0]
    lam, V = np.linalg.eig(G)
    E = -np.angle(lam) / s
    o = np.argsort(E)
    top = [int(o[-2]), int(o[-1])]
    Q = np.linalg.qr(V[:, top])[0]
    return Q[:, 0], Q[:, 1], float(np.mean(E[top])), G


def griglia(nome_eps):
    """### **`(theta, phi)` della scelta migliore** *(il minimo di `griglia.json`, `nome_eps` = `"e05"` o `"e0"`)*."""
    with open(GRIGLIA, encoding="utf-8") as f:
        gr = json.loads(f.read())[nome_eps]
    return gr["minimo"]["theta"], gr["minimo"]["phi"]


def scelta(q1, q2, theta, phi):
    """### **La scelta dentro la coppia e il suo partner** *(ortogonale)*."""
    return math.cos(theta) * q1 + np.exp(1j * phi) * math.sin(theta) * q2, -math.sin(theta) * q1 + np.exp(1j * phi) * math.cos(theta) * q2


def bloch(G, q, E0, s):
    """### **`|G q - e^{-i E0 s} q|`:** quanto `q` e' uno stato della coppia."""
    return float(np.linalg.norm(G @ q - np.exp(-1j * E0 * s) * q))


# ====================================================================== I COSTRUTTORI
def inviluppo(z, pK, q, N):
    """### **`B` a `Gamma`:** la norma per nodo di `pK` *(lo stato di `A` a `K` della scena)* per lo spinore `q`, normalizzato a `N`."""
    inv = np.linalg.norm(pK.reshape(z["inc"].n, 12), axis=1)
    p = inv[:, None] * q[None, :]
    p *= math.sqrt(N / float(np.sum(np.abs(p) ** 2)))
    return p.reshape(pK.shape)


def stato_AK(pK):
    """### **`A` a `K`:** lo stato iniziale della scena *(l'inviluppo per `Q_K` e la fase di `K`)*, copiato."""
    return pK.copy()


def mu_rayleigh(z, phi0, p, s, forma):
    """### **`(mu, il residuo)`:** `lam = <p, T p>/<p, p>`, `mu = -arg(lam)/s`, il residuo `|T p - lam p|/|p|`."""
    import _modo_al_variare_di_s as MS
    T = MS.tick(z, phi0, p, forma)
    lam = complex(np.vdot(p, T) / np.vdot(p, p))
    return -math.atan2(lam.imag, lam.real) / s, float(np.linalg.norm(T - lam * p) / np.linalg.norm(p))


# ====================================================================== LE DECISIONI DI LUCA (01:27), PER LE PROVE NUOVE (01:28, punto 6)
# ### (7) eps: dalla TABELLA, letto, mai scritto a mano; eps 0 solo con ridotto=True, e dichiarato.
# ### (1) la forma: dalla TABELLA (dal 2026-11-01 16:52 il nucleo usa S1 dalla tabella; S3 opzione esplicita).
# ### le piatte, la strada (A): il costruttore predefinito e' l'inviluppo su B a Gamma; A a K con quale="AK".
def eps_tabella():
    """### **eps di `CAMM-MONETA-SPIN` dalla tabella** *(`_genera.carica`)*."""
    import _genera as GE
    leggi, _v, _o = GE.carica()
    voce = [x for x in leggi if x.get("id") == "CAMM-MONETA-SPIN"]
    assert len(voce) == 1, "CAMM-MONETA-SPIN non e' UNA voce della tabella"
    return float(voce[0]["parametri"]["eps"]["valore"])


def eps_della_prova(ridotto=False):
    """### **`(eps, la dichiarazione)`:** la tabella, o `0` col «caso ridotto» *(da stampare nel referto)*."""
    if ridotto:
        return 0.0, "CASO RIDOTTO: eps 0 (la moneta spenta), non il modello"
    return eps_tabella(), "eps %g dalla tabella (CAMM-MONETA-SPIN)" % eps_tabella()


def forma_predefinita():
    """### **La forma della TABELLA** *(`CAMM-MATERIA-VUOTO`, `parametri.forma`, dal modulo generato; Luca `16:52`)*: le corse la applicano con
    `_screening_forme_s3.forma`, cioe' con le espressioni di `csv/` che il nucleo ripete al bit."""
    import termini.camm_materia_vuoto as TMV
    return TMV.PARAMETRI["forma"]


@contextlib.contextmanager
def scena_prova(N, L, s, vuoto=None, ridotto=False):
    """### **La scena di una prova nuova:** eps e la forma dalle decisioni; `vuoto=None` la scena di riferimento, altrimenti `scena_vuoto`.
    ### **`(rec, z, phi0, pK, la dichiarazione)`.**"""
    eps, dich = eps_della_prova(ridotto)
    forma = forma_predefinita()
    cm = scena_riferimento(N, L, eps, s, forma) if vuoto is None else scena_vuoto(N, L, eps, s, forma, vuoto)
    with cm as (rec, z, phi0, pK):
        yield rec, z, phi0, pK, "%s; la forma %s" % (dich, forma)


GRIGLIA_PER_EPS = {0.5: "e05", 0.0: "e0"}      # ### le chiavi di griglia.json (= _massimo_di_B.CASI): la scelta migliore e' misurata solo a questi due eps


def partenza(z, phi0, pK, s, N, quale="BG"):
    """### **Il solitone di una prova nuova:** `"BG"` *(predefinito)* l'inviluppo per la scelta migliore della coppia di QUESTA scena, al suo eps; `"AK"` lo stato di `A` a `K`."""
    if quale == "AK":
        return stato_AK(pK)
    assert quale == "BG", quale
    q1, q2, _E0, _G = coppia(z, phi0, s)
    q, _qp = scelta(q1, q2, *griglia(GRIGLIA_PER_EPS[z["par"]["eps"]]))
    return inviluppo(z, pK, q, N)


# ====================================================================== L'UNITA' e_K (Luca, 2026-11-01, dopo 6052a2b4)
# ### e_K e' l'energia dell'onda libera nel massimo di banda: si misura col legame SPENTO esplicitamente, non col vuoto azzerato, e non
# ### dipende dalla forma del legame. ### Con S1 la N a Lambda 0 e' il limite N = rho (con S3 era 0): col vuoto azzerato e_K saliva di 1.
def _zero(rho, lam):
    return np.zeros(np.broadcast(np.asarray(rho, dtype=float), np.asarray(lam, dtype=float)).shape, dtype=float)


@contextlib.contextmanager
def legame_spento():
    """### **Il legame SPENTO, esplicitamente:** dentro, `N`, `alpha` e `beta` di `materia_vuoto` sono zero ovunque; all'uscita tornano quelle di prima.
    ### ⚠ **Funziona perche' il nucleo le chiama PER NOME DI MODULO** *(`energia_pesata.termini_di_h`, `materia_vuoto.pezzi`)*: lo si asserisce."""
    import energia_pesata as EP
    import materia_vuoto as MV
    assert EP.MV is MV, "energia_pesata non usa questo materia_vuoto: spegnere qui non spegnerebbe niente"
    prima = (MV.N, MV.alpha, MV.beta)
    MV.N, MV.alpha, MV.beta = _zero, _zero, _zero
    try:
        yield
    finally:
        MV.N, MV.alpha, MV.beta = prima


def e_K(z):
    """### **`e_K`: l'energia per norma dell'onda libera** *(lo stato uniforme di `A` a `K`)* **col legame spento:** lo storico `_vuoto_vivo_B.e_K_di`,
    non toccato, dentro `legame_spento()`."""
    import _vuoto_vivo_B as V
    with legame_spento():
        return V.e_K_di(z)


# ====================================================================== LA PARTENZA SIMMETRICA (Luca, dopo aad1435a e 21:14; il task history 2026-11-03_D0_ruotata_e_TS, sez. 8-9)
# ### R180 x sigma_z attorno a un centro d'inversione: sulla cella (P q)[a, s] = sigma_z q[a, 1 - s] (l'indice 4 a + 2 s + componente di reshape(n, 12)); la q nel settore di P
# ### scelto da Luca (q+), la fase globale con la componente di modulo massimo reale positiva (una convenzione, dichiarata); l'inviluppo sul NODO simmetrizzato.
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def matrice_P(U):
    """### **`P` sulla cella** *(12 x 12)*: `(P q)[a, s] = U q[a, 1 - s]`."""
    P = np.zeros((12, 12), dtype=complex)
    for a in range(3):
        for s in range(2):
            P[4 * a + 2 * s:4 * a + 2 * s + 2, 4 * a + 2 * (1 - s):4 * a + 2 * (1 - s) + 2] = U
    return P


def q_simmetrica(z, phi0, s, segno):
    """### **`(q, l'autovalore, G)`:** l'autovettore di `P` *(`sigma_z`)* nella coppia di `B` a `Gamma` con l'autovalore piu' vicino a `segno` *(`+1`: `q+`)*; la fase globale con la
    componente di modulo massimo reale positiva."""
    q1, q2, _E0, G = coppia(z, phi0, s)
    Q = np.stack([q1, q2], axis=1)
    M = Q.conj().T @ matrice_P(SIGMA_Z) @ Q
    w, W = np.linalg.eigh(0.5 * (M + M.conj().T))
    j = int(np.argmin(np.abs(w - segno)))
    q = Q @ W[:, j]
    q = q / np.linalg.norm(q)
    k = int(np.argmax(np.abs(q)))
    q = q * (np.conj(q[k]) / abs(q[k]))
    return q, float(w[j]), G


def densita_nodo(z, p):
    """### **`sum |p_e|^2` sulle estremita' di ogni nodo** *(`inc.nodo`)*."""
    r = np.zeros(z["inc"].n)
    np.add.at(r, z["inc"].nodo, np.sum(np.abs(p) ** 2, axis=1))
    return r


def centro_inversione(z, pK):
    """### **`m2`:** il centro d'inversione del reticolo *(`m2 / 2`: un nodo o il punto medio di un arco)* piu' vicino al centro periodico della densita' di `pK` per nodo."""
    from . import toro as TO
    L = z["L"]
    v = np.arange(z["inc"].n)
    c1, c2, _x, _y = TO.centro(densita_nodo(z, pK), v // L, v % L, L)
    return int(round(2 * c1)), int(round(2 * c2))


def partenza_simmetrica(z, pK, q, N, m2):
    """### **`psi[e] = inv(nodo(e)) q[a, s]`**, `inv(v) = sqrt((rho_K(v) + rho_K(R v)) / 2)` *(la densita' di `pK` per nodo simmetrizzata attorno a `m2 / 2`)*, normalizzata a `N`;
    `a = (e // 2) % 3` l'asse, `s = e % 2` l'estremita' *(`0` sul nodo, `1` sul vicino)*."""
    inc, L = z["inc"], z["L"]
    v = np.arange(inc.n)
    Rv = ((m2[0] - v // L) % L) * L + (m2[1] - v % L) % L
    rK = densita_nodo(z, pK)
    inv = np.sqrt(0.5 * (rK + rK[Rv]))
    e = np.arange(2 * inc.m)
    qe = q.reshape(3, 2, 2)[(e // 2) % 3, e % 2]
    p = inv[inc.nodo][:, None] * qe
    p *= math.sqrt(N / float(np.sum(np.abs(p) ** 2)))
    return p
