# -*- coding: utf-8 -*-
r"""**LE USCITE** *(le espressioni di `_chiudere_le_uscite.uscite`, `_massimo_di_B.altre`, `_scatola.spettro` e `_scatola.residuo`)*.

### **Lo spettro ha UNA sola firma: dalla SCENA `(z, phi0)`** *(`DV.matrice` a `AMP`)*, **mai da pesi passati a mano** *(l'errore di `c6ad04ac`)*;
### **e quando si legge uno stato, il suo residuo registrato DEVE tornare** *(`stato_nella_scena`)*.
### **`Omega = 2 pi/s`: le quasi-energie sono definite modulo `Omega`, e `s` e' un argomento.**
"""
import itertools
import math

import numpy as np

from . import RADICE  # noqa: F401  (i percorsi)

GRUPPI = (("Ppi", (0, 1, 2, 3)), ("A", (4, 5)), ("P0", (6, 7, 8, 9)), ("B", (10, 11)))   # ### = _dove_va_la_materia.GRUPPI (il test lo asserisce)
PIATTE = ("P0", "Ppi")
DISPERSIVE = ("A", "B")
W = (0.05, 0.2)                 # ### la larghezza W di 99b679bc, i due lati (= _chiudere_le_uscite.W)
TOLL_RES_REL = 1e-6             # ### il residuo ricalcolato contro il registrato, relativo (= _scatola.TOLL_RES_REL)


def omega(s):
    return 2.0 * math.pi / s


def distanza(iv, jv, om):
    """### **La distanza fra due intervalli, modulo `om`** *(negativa = si sovrappongono, di quanto)*."""
    best = None
    for k in (-1, 0, 1):
        a0, a1 = iv[0] + k * om, iv[1] + k * om
        d = max(jv[0] - a1, a0 - jv[1])
        best = d if best is None else min(best, d)
    return best


def gruppi_di(E):
    """### **Per gruppo, `[min, max]` di `E`** *(`E` di forma `(..., 12)`)*."""
    return {g: (float(E[..., list(i)].min()), float(E[..., list(i)].max())) for g, i in GRUPPI}


def uscite(E0, g, sp, om, mu=None):
    """### **Per ogni `mu` in `[E0, E0 + g]`** *(o il solo `mu` dato)* **e `alpha` in `[0, g]`:** (n0), (n1), (n2-misto), (n2); ### **< 0: APERTA.**"""
    m0, m1 = (E0, E0 + g) if mu is None else (mu, mu)
    out = {}
    lo = m0 + 1e-9 if mu is None else m0
    for c in DISPERSIVE:
        out["(n0) mu in %s" % c] = distanza((lo, m1), sp[c], om)
    for p in PIATTE:
        F = sp[p]
        out["(n1) %s" % p] = distanza((m0 - F[1], m1 - F[0]), (0.0, g), om)
        for c in DISPERSIVE:
            out["(n2-misto) %s + %s" % (p, c)] = distanza((2 * m0 - F[1] - g, 2 * m1 - F[0]), sp[c], om)
    for i, p in enumerate(PIATTE):
        for q in PIATTE[i:]:
            Fp, Fq = sp[p], sp[q]
            out["(n2) %s + %s" % (p, q)] = distanza((2 * m0 - Fp[1] - Fq[1], 2 * m1 - Fp[0] - Fq[0]), (0.0, 2 * g), om)
    return out


def altre(E0, g, sp, om, mu=None):
    """### **(n3)** `3 mu - F_i - F_j - F_k` in `[0, 3 g]`; ### **le coppie di onde dispersive:** **(c0)** libere, **(c1)** una col legame, **(c2)** tutte e due."""
    m0, m1 = (E0, E0 + g) if mu is None else (mu, mu)
    out = {}
    for tr in itertools.combinations_with_replacement(PIATTE, 3):
        lo = sum(sp[p][0] for p in tr)
        hi = sum(sp[p][1] for p in tr)
        out["(n3) %s" % " + ".join(tr)] = distanza((3 * m0 - hi, 3 * m1 - lo), (0.0, 3 * g), om)
    for c, d in itertools.combinations_with_replacement(DISPERSIVE, 2):
        som = (sp[c][0] + sp[d][0], sp[c][1] + sp[d][1])
        for k, sott in (("c0", 0.0), ("c1", g), ("c2", 2 * g)):
            out["(%s) %s + %s" % (k, c, d)] = distanza((2 * m0 - sott, 2 * m1), som, om)
    return out


def tutte(E0, g, sp, om, mu=None):
    u = uscite(E0, g, sp, om, mu)
    u.update(altre(E0, g, sp, om, mu))
    return u


def per_costruzione(k, c):
    """### **Vere PER COSTRUZIONE:** la (n0) della banda di `E0` *(`mu` parte dal suo bordo)* e la (c2) `c + c` *(due quanti della banda col legame SONO il solitone)*."""
    return k in ("(n0) mu in %s" % c, "(c2) %s + %s" % (c, c))


def margine(u, c):
    """### **Il margine minimo senza le condizioni vere per costruzione:** `(il valore, la condizione)`."""
    return min((d, k) for k, d in u.items() if not per_costruzione(k, c))


def aperte(u, c):
    return [k for k, d in u.items() if d < 0 and not per_costruzione(k, c)]


def giudizio(d):
    if d < 0:
        return "APERTA (dentro di %.4f)" % -d
    if d <= W[0]:
        return "SUL BORDO (%.4f: entro W %.2f)" % (d, W[0])
    if d <= W[1]:
        return "chiusa di %.4f (entro W %.2f)" % (d, W[1])
    return "CHIUSA (%.4f)" % d


# ====================================================================== LO SPETTRO, DALLA SCENA
def spettro_scena(z, phi0, s):
    """### **Lo spettro libero DELLA SCENA** *(`DV.matrice` a `AMP`; la matrice scrive `z["st"]` e lo rimette)*: ### **per gruppo `[min, max]` di `E = fase/s`.**"""
    import _dove_va_la_materia as DV
    ph, _Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
    E = ph / s
    return {gr: (float(E[..., list(idx)].min()), float(E[..., list(idx)].max())) for gr, idx in DV.GRUPPI}


def residuo(z, phi0, psi, mu, s, forma):
    """### **`|T psi - e^{-i mu s} psi| / |psi|`** *(il tick congelato vero, `_modo_al_variare_di_s.tick`)*."""
    import _modo_al_variare_di_s as MS
    return float(np.linalg.norm(MS.tick(z, phi0, psi, forma) - np.exp(-1j * mu * s) * psi) / np.linalg.norm(psi))


def stato_nella_scena(z, phi0, psi, mu, s, forma, res_registrato):
    """### **Lo spettro della scena IN CUI lo stato e' stato trovato:** ### **DEVE** *(un `AssertionError`, non un avviso)* **il residuo ricalcolato = il registrato entro `TOLL_RES_REL`.**
    ### **Il residuo PRIMA dello spettro:** `MS.tick` scrive `psi_h`, la matrice lo rimette."""
    r = residuo(z, phi0, psi, mu, s, forma)
    assert abs(r / res_registrato - 1.0) < TOLL_RES_REL, "i pesi della scena NON sono quelli dello stato: il residuo %.6e contro il registrato %.6e" % (r, res_registrato)
    return spettro_scena(z, phi0, s), r
