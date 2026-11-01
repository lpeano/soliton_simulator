# -*- coding: utf-8 -*-
r"""**LE MISURE** *(le espressioni di `_congelato_lungo.punto`, `_salti_nel_cuore.campione` e `lunghezza_arco`, `_modo_lento.Bande`, la riga `D` di `_coppia_di_B.lunga`,
`_livelli_piatti.forma_pendenze`, `_modo_di_R.vita`, `_consolida_B.limite`)*.

### **Il cuore:** la finestra NETTA `f_win` *(i nodi entro `w_in`)* e la LISCIA `f_liscia` *(una rampa larga un arco `h`: senza i salti di un nodo che attraversa il bordo, `salti_nel_cuore.txt`)*.
### **L'alone:** `1 - f_3w0`. ### **La vita:** il primo `tau` con `|D|/|psi0| >= SOGLIA_VITA` *(Luca `20:46`)*.
### **Il periodo dai cambi di segno VUOLE IL PASSO** *(nessun default)* **e restituisce gli ALIAS compatibili coi campioni:** ### **un alias non si riconosce dai campioni da soli** *(`03142636`)*.
"""
import math

import numpy as np

from . import RADICE  # noqa: F401  (i percorsi)

SOGLIA_VITA = 1e-2              # ### la soglia della vita (Luca 20:46) = la saturazione di _strada_b_lati e _modo_lento
SIGMA_FORMA = 3.0               # ### il 3 sigma di doc/PATTERN_DI_PROVA.md (P1-sexies), il criterio aggiunto della forma (= _livelli_piatti.SIGMA_FORMA)
GRUPPI_LIMITE = {"piatte": ("P0", "Ppi"), "A": ("A",)}   # ### = _consolida_B.GRUPPI


# ====================================================================== IL CUORE, LA LARGHEZZA, L'ALONE, IL BARICENTRO
def punto(z, t, w_in, w0, s):
    """### **`w`, il cuore netto `f_win`, `f_3w0`, il picco, `M`** *(la densita' di `_energia_del_legame.densita`)*."""
    import _energia_del_legame as EL
    rho, _l = EL.densita(z["inc"], z["st"])
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    w = math.sqrt(float(rho @ np.sum((z["pos"] - c) ** 2, axis=1)) / M)
    return {"t": t, "tau": t * s, "w": w, "f_win": float(rho[d <= w_in].sum()) / M, "f_3w0": float(rho[d <= 3.0 * w0].sum()) / M, "picco": float(rho.max()), "M": M}


def alone(pt):
    return 1.0 - pt["f_3w0"]


def lunghezza_arco(z):
    """### **La MEDIANA delle lunghezze degli archi** *(gli archi che chiudono il toro hanno la distanza non periodica)*."""
    nd = np.asarray(z["inc"].nodo)
    p = z["pos"]
    ll = np.hypot(p[nd[0::2], 0] - p[nd[1::2], 0], p[nd[0::2], 1] - p[nd[1::2], 1])
    return float(np.median(ll))


def campione(z, t, w_in, h):
    """### **Il baricentro `(x, y)`, `w`, il cuore netto `f_win` e il liscio `f_liscia`** *(la rampa `clip((w_in + h/2 - d)/h, 0, 1)`)*."""
    import _energia_del_legame as EL
    rho, _l = EL.densita(z["inc"], z["st"])
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    w = math.sqrt(float(rho @ np.sum((z["pos"] - c) ** 2, axis=1)) / M)
    g = np.clip((w_in + 0.5 * h - d) / h, 0.0, 1.0)
    return {"t": t, "x": float(c[0]), "y": float(c[1]), "w": w, "f_win": float(rho[d <= w_in].sum()) / M, "f_liscia": float(rho @ g) / M}


# ====================================================================== LE BANDE DI D E LE ROTAZIONI
class Bande:
    """### **I proiettori di gruppo di banda** *(un gruppo intero: indipendente dalla base dentro il gruppo)*; `Z` da `DV.autovettori(DV.matrice(...))` **della scena**."""

    def __init__(self, Z, L):
        import _dove_va_la_materia as DV
        self.Z, self.L = Z, L
        self.valle, self.nomi, _dK, _dk = DV.geometria(L)
        self.gruppi = dict(DV.GRUPPI)

    def coeff(self, d):
        f = np.fft.fft2(d.reshape(self.L, self.L, 12), axes=(0, 1))
        return np.einsum("abji,abj->abi", self.Z.conj(), f)

    def parte(self, c, nomi):
        idx = [i for g in nomi for i in self.gruppi[g]]
        return np.einsum("abij,abj->abi", self.Z[..., idx], c[..., idx])

    def frazioni(self, d):
        """### **La frazione di `|d|^2` per gruppo** *(la riga `D` delle corse)*."""
        c = self.coeff(d)
        pk = np.abs(c) ** 2
        tot = float(pk.sum())
        return {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in self.gruppi.items()}

    def misura(self, d, nomi):
        """### **La parte nelle bande `nomi`:** la frazione di `|d|^2`, `q = <x, sigma_z x>/<x, x>`, i pesi per valle."""
        c = self.coeff(d)
        tot = float(np.sum(np.abs(c) ** 2))
        f = self.parte(c, nomi)
        p = np.abs(f) ** 2
        n2 = float(p.sum())
        q = float(p[..., 0::2].sum() - p[..., 1::2].sum()) / n2
        idx = [i for g in nomi for i in self.gruppi[g]]
        pk = np.sum(np.abs(c[..., idx]) ** 2, axis=-1)
        val = {nv: float(pk[self.valle == v].sum()) / n2 for v, nv in enumerate(self.nomi)}
        return {"frazione": n2 / tot, "q": q, "valli": val}

    def rotazione(self, d1, d2, nomi, dtau):
        """### **`-arg<x(t), x(t + dtau)>/dtau`:** l'energia della parte rispetto a `mu`, per unita' di tempo; ### **definita modulo `2 pi/dtau`** *(lo stesso limite del campionamento)*."""
        a = self.parte(self.coeff(d1), nomi)
        b = self.parte(self.coeff(d2), nomi)
        v = complex(np.vdot(a, b))
        return -math.atan2(v.imag, v.real) / dtau


def riga_D(bande, D, n0, t):
    """### **La riga `D` delle corse:** `t`, `|D|/|psi0|`, le frazioni per gruppo."""
    return {"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": bande.frazioni(D)}


def periodo_dai_cambi(pr, passo):
    """### **Il periodo dai cambi di segno della serie `pr`, campionata ogni `passo`** *(nelle unita' di `passo`)*: `2 passo <diff(cambi)>`.
    ### **Accanto, gli ALIAS:** ogni periodo vero `T'` con `1/T' = |1/T +- k/passo|` *(`k = 1, 2`)* da' gli STESSI campioni; ### **il limite di Nyquist e' `2 passo`.**
    ### **Non sceglie:** chi lo usa scioglie l'ambiguita' con un'altra misura *(le rotazioni per banda)*."""
    cambi = [i for i in range(1, len(pr)) if pr[i - 1] * pr[i] < 0.0]
    if len(cambi) < 2:
        return {"cambi": len(cambi), "periodo": None, "nyquist": 2.0 * passo, "alias": []}
    T = 2.0 * passo * float(np.mean(np.diff(cambi)))
    f = 1.0 / T
    alias = sorted(1.0 / abs(f + k / passo) for k in (-2, -1, 1, 2) if abs(f + k / passo) > 0.0)
    return {"cambi": len(cambi), "periodo": T, "nyquist": 2.0 * passo, "alias": alias}


# ====================================================================== LA FORMA, LA VITA, IL TASSO
def forma_pendenze(tau, nD, saturazione):
    """### **Le pendenze locali `l = d ln|D|/dt`** *(`np.gradient`)* **sui campioni sotto `saturazione`, esclusi il primo e l'ultimo; il fit `l = gamma + b/t`:**
    ### **ESPONENZIALE se `gamma - SIGMA_FORMA sigma_gamma > 0` e `gamma t_ultimo > 1`; altrimenti la potenza `t^b`, LINEARE se `b` arrotondato e' `1`.**"""
    loc = np.gradient(np.log(nD), tau)
    idx = [i for i in range(1, len(nD) - 1) if nD[i] < saturazione]
    if len(idx) < 3:
        return {"forma": None, "campioni": len(idx)}
    t, ll = tau[idx], loc[idx]
    X = np.column_stack([np.ones_like(t), 1.0 / t])
    coef = np.linalg.lstsq(X, ll, rcond=None)[0]
    res = ll - X @ coef
    cov = float(res @ res) / max(len(t) - 2, 1) * np.linalg.inv(X.T @ X)
    g, b = float(coef[0]), float(coef[1])
    sg, sb = float(np.sqrt(cov[0, 0])), float(np.sqrt(cov[1, 1]))
    if g - SIGMA_FORMA * sg > 0 and g * float(t[-1]) > 1.0:
        f = "esponenziale"
    else:
        f = "lineare" if int(round(b)) == 1 else "potenza t^%d" % int(round(b))
    return {"forma": f, "gamma": g, "sigma_gamma": sg, "b": b, "sigma_b": sb, "t_ultimo": float(t[-1]), "campioni": len(idx)}


def vita(tau, nD):
    """### **Il primo `tau` con `|D|/|psi0| >= SOGLIA_VITA`**, o `None` se non ci arriva."""
    sopra = np.nonzero(nD >= SOGLIA_VITA)[0]
    return float(tau[sopra[0]]) if len(sopra) else None


def limite(dd, s):
    """### **Il limite superiore del tasso sull'ampiezza** *(dalle righe `D`)*: per `piatte` e `A` la frazione `f` di `|D|^2` e `a = sqrt(f) nD`;
    ### **(lett), (a0), (amin), (pend); il dichiarato e' il piu' grande fra (a0), (amin), (pend).**"""
    tau = np.array([d["t"] * s for d in dd])
    nD = np.array([d["nD"] for d in dd])
    T = float(tau[-1] - tau[0])
    out = {"tau0": float(tau[0]), "tau1": float(tau[-1]), "campioni": len(dd), "gruppi": {}}
    for g, bb in GRUPPI_LIMITE.items():
        f = np.array([sum(d["bande"][b] for b in bb) for d in dd])
        a = np.sqrt(f) * nD
        im, ix = int(np.argmin(a)), int(np.argmax(f))
        h = tau >= tau[0] + 0.5 * T
        r = {"f0": float(f[0]), "f_max": float(f[ix]), "tau_f_max": float(tau[ix]), "f1": float(f[-1]),
             "a0": float(a[0]), "a_min": float(a[im]), "tau_a_min": float(tau[im]), "a_max": float(a.max()), "a1": float(a[-1]),
             "lett": float(math.log(f[-1] / f[0]) / T), "da_a0": float(math.log(a[-1] / a[0]) / T),
             "da_amin": float(math.log(a[-1] / a[im]) / (tau[-1] - tau[im])) if tau[-1] > tau[im] else float("-inf"),
             "pend": float(np.polyfit(tau[h], np.log(a[h]), 1)[0])}
        r["limite"] = max(r["da_a0"], r["da_amin"], r["pend"])
        out["gruppi"][g] = r
    return out
