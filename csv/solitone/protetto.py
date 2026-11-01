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
