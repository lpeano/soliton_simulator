# -*- coding: utf-8 -*-
r"""`M2` — **GLI STATI STAZIONARI AUTOCONSISTENTI**, e `FERMO` se l'iterazione non converge.

> ## ⛔ **IL PUNTO DEL MANDATO:** invece di partire da una forma qualunque, si **cerca** uno
> ## stato stazionario non lineare. ### **Se non c'e', non lo si trova** — e questo e' il
> ## modo di non confondere *«il mio grumo iniziale si disperde»* con *«non esistono grumi»*.

**L'ITERAZIONE, dichiarata:**

| | il passo |
|---|---|
| `1` | si **CONGELA** il contributo non lineare calcolato da `psi`: gli angoli `ang_k` del flusso diventano **numeri**, e il passo diventa **LINEARE** |
| `2` | si costruisce la **matrice** del passo congelato *(applicandolo alla base, come `camminata2.matrice_passo`)* |
| `3` | fra i suoi autovettori si prende il **piu' LOCALIZZATO** *(rapporto di partecipazione minimo)* con quasi-energia **nel buco o al bordo di banda** di `M0` |
| `4` | si **riscala** per avere l'`x0` voluto, si ricalcola `ang_k`, e si torna al `1` |

### ⛔ **E LA FASE GLOBALE SI FISSA PRIMA DI CONFRONTARE:** un autovettore e' definito **a
meno di una fase**, quindi `max|psi_nuovo - psi_vecchio|` senza fissarla ### **non
converge mai** — e sarebbe un `FERMO` per la ragione sbagliata.

### ⛔ **FERMO SE NON CONVERGE**, come il punto medio implicito di `interferenza3.py`:
tolleranza **`dim * eps`**, al piu' **`MAX_GIRI`** giri, e ### **il numero dei giri si
DICHIARA.**

### ⚠ **E IL COSTO SI DICHIARA:** ogni giro costa **una `eig`**, cioe' `~1.5` s a
`dim = 832` e `~36` s a `dim = 3468`. ### **Percio' la griglia intera gira su `n = 120`**, e
sulle taglie grandi ### **solo i casi che hanno convertito** — e se non convergono, non c'e'
niente da riprovare.

### ⚠ **NESSUN `clip`, NESSUNA costante tarata.** `MAX_GIRI` e' **un budget dichiarato**,
non un parametro di una legge: oltre quello ### **si FERMA e si scrive**, non si taglia.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import interferenza3 as I3                                     # noqa: E402
import nonlineare2 as N2                                       # noqa: E402
import saturazione3 as S3                                      # noqa: E402
import scena as SC                                             # noqa: E402
import segni1 as S1                                            # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import _spettro as SP                                          # noqa: E402

EPS = float(np.finfo(float).eps)
MAX_GIRI = 64
# ### ⛔ **LA GRIGLIA DI `x0`, DICHIARATA** *(task history, `t`)*.
X0_GRIGLIA = (0.125, 0.5, 1.0, 2.0, 8.0)


class NonConverge(Exception):
    """### **FERMO:** non si prosegue con un'iterazione che non converge."""


def _angoli_congelati(psi, phi, sc, geo, variante, dtau):
    """### Gli angoli del flusso, **calcolati da `psi` e poi CONGELATI.**

    Ritorna `(ang_per_estremita, segno)`: `ang` e' l'angolo di rotazione attorno a `n`, e
    il ### **segno** e' quello della variante.
    """
    seg = -1.0 if variante.startswith("-") else 1.0
    lam = V3.lambda_nodo(phi, sc)
    if variante.endswith("N"):
        h = N2.elicita_nodo(psi, sc, geo)
    else:
        h = I3.elicita_interferenza(psi, sc, geo)
    al, _be = S3.pezzi(h, lam)
    return (seg * al * dtau)[sc["nodo"]]


def _passo_congelato(psi0, phi, sc, geo, variante, dt, eps):
    """### Il passo con gli angoli **congelati**: e' ### **LINEARE in `psi`.**

    ### ⭐ **La composizione resta quella del `v3`** *(Strang)*: mezzo angolo, passo
    lineare, mezzo angolo.
    """
    ang = _angoli_congelati(psi0, phi, sc, geo, variante, dt)

    def passo(v):
        x = S3._ruota_attorno_a_n(v, geo, 0.5 * ang)
        x = C2.passo2(x, sc, geo, np.ones(sc["n"]), dt, eps)
        return S3._ruota_attorno_a_n(x, geo, 0.5 * ang)
    return passo


def _matrice(passo, dim):
    """La matrice di un passo, **applicandolo alla base.**"""
    M = np.zeros((dim, dim), dtype=complex)
    b = np.zeros((dim // 2, 2), dtype=complex)
    for j in range(dim):
        b[:] = 0.0
        b[j // 2, j % 2] = 1.0
        M[:, j] = np.asarray(passo(b)).reshape(-1)
    return M


def _scala_a_x0(psi, phi, sc, geo, variante, x0):
    """### Riscala `psi` per avere l'`x0` voluto. ### **`h` e' QUADRATICA nell'ampiezza.**"""
    lam = V3.lambda_nodo(phi, sc)
    if variante.endswith("N"):
        h = N2.elicita_nodo(psi, sc, geo)
    else:
        h = I3.elicita_interferenza(psi, sc, geo)
    buoni = lam > 0.0
    if not np.any(buoni):
        return psi
    x = float(np.max(np.abs(h[buoni] / lam[buoni])))
    return psi * math.sqrt(x0 / x) if x > 0 else psi


def _fissa_fase(nuovo, vecchio):
    """### Fissa la fase globale di `nuovo` su `vecchio`. ### **Senza questo NON converge.**"""
    z = complex(np.vdot(vecchio, nuovo))
    if abs(z) == 0.0:
        return nuovo
    return nuovo * np.exp(-1j * np.angle(z))


def _scegli(M, sc, bersagli, spaziatura):
    """### L'autovettore **piu' LOCALIZZATO** con quasi-energia vicino a un bersaglio.

    `bersagli` sono le quasi-energie **nel buco o al bordo di banda** trovate da `M0`.
    ### ⛔ **Se nessun autovalore cade entro `3` spaziature da un bersaglio, si prende il
    piu' localizzato IN ASSOLUTO e SI DICHIARA**, perche' *«non c'e' un bersaglio»* e' un
    risultato e non un errore.
    """
    lam, vec = np.linalg.eig(M)
    om = np.angle(lam)
    pr = np.array([SP.partecipazione(vec[:, j], sc) for j in range(M.shape[0])])
    vicino = np.zeros(M.shape[0], dtype=bool)
    for b in bersagli:
        d = np.abs(np.angle(np.exp(1j * (om - b))))
        vicino |= (d < 3.0 * spaziatura)
    if np.any(vicino):
        idx = [j for j in range(M.shape[0]) if vicino[j]]
        j = min(idx, key=lambda q: pr[q])
        return vec[:, j], float(om[j]), float(pr[j]), True
    j = int(np.argmin(pr))
    return vec[:, j], float(om[j]), float(pr[j]), False


def cerca(sc, geo, variante, x0, bersagli, spaziatura, dt=1.0, eps=0.5,
          seme=11, max_giri=MAX_GIRI):
    """### L'iterazione autoconsistente. ### **Alza `NonConverge` se non converge.**"""
    dim = 4 * sc["m"]
    phi = V3.vuoto_fondo(sc, V3.LAMBDA0, seme)
    # ### il punto di partenza: il grumo del `v3`, cosi- il confronto e- con cio- che c-era
    import _letture3 as L3
    st, _dentro, _d = L3.grumo(sc, geo, 0, 1, x0, seme=seme)
    psi = st["psi"]
    storia = []
    for giro in range(1, max_giri + 1):
        passo = _passo_congelato(psi, phi, sc, geo, variante, dt, eps)
        M = _matrice(passo, dim)
        v, om, pr, nel_bersaglio = _scegli(M, sc, bersagli, spaziatura)
        v = v.reshape(-1, 2)
        v = v / math.sqrt(CM.norma(v))
        v = _scala_a_x0(v, phi, sc, geo, variante, x0)
        v = _fissa_fase(v, psi)
        scarto = float(np.max(np.abs(v - psi)))
        storia.append({"giro": giro, "scarto": scarto, "quasi_energia": om,
                       "partecipazione": pr, "nel_bersaglio": bool(nel_bersaglio)})
        psi = v
        if scarto <= dim * EPS:
            return {"psi": psi, "phi": phi}, {"giri": giro, "scarto": scarto,
                                              "quasi_energia": om,
                                              "partecipazione": pr,
                                              "nel_bersaglio": bool(nel_bersaglio),
                                              "storia": storia[-4:]}
    raise NonConverge(
        "### FERMO: `%s`, x0 = %g: l-iterazione NON converge in %d giri "
        "(scarto %.3g, soglia %.3g)" % (variante, x0, max_giri, storia[-1]["scarto"],
                                        dim * EPS))


def prova_dinamica(st, sc, geo, variante, rag, tick, dt=1.0, eps=0.5):
    """### LA PROVA DINAMICA: col passo **VERO**, non congelato.

    Ritorna la frazione di norma che resta entro `rag` archi, col passo **non lineare** e
    col passo ### **LINEARE**, che e' il confronto che conta.
    """
    d = SC.distanze(sc, 0)
    dentro = (d >= 0) & (d <= rag)
    uno = np.ones(sc["n"], dtype=float)
    fuori = {}
    for et, fl in ((variante, S1.flusso_di(variante)), ("lineare", None)):
        z = {"psi": st["psi"].copy(), "phi": st["phi"].copy()}
        for _ in range(tick):
            z = C3.passo3(z, sc, geo, uno, dt, eps, fl)
        rho = CM.rho_nodo(z["psi"], sc)
        tot = float(np.sum(rho))
        fuori[et] = (float(np.sum(rho[dentro]) / tot) if tot > 0 else float("nan"))
    return fuori


if __name__ == "__main__":
    import geometria as GE
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    sc = SC.irregolare(120)
    geo = GE.scena_identita(sc)
    dim = 4 * sc["m"]
    spaz = 2.0 * math.pi / dim
    print("  dim %d, spaziatura media %.4g, soglia di convergenza %.3g"
          % (dim, spaz, dim * EPS))
    print("  %-6s %-7s %-10s %-14s %-14s %s"
          % ("var", "x0", "giri", "scarto", "quasi-energia", "partecipazione"))
    for variante in ("+N", "-N"):
        for x0 in (0.5, 8.0):
            try:
                st, info = cerca(sc, geo, variante, x0, [0.0, math.pi], spaz,
                                 max_giri=8)
                print("  %-6s %-7g %-10d %-14.3g %-14.4f %.1f"
                      % (variante, x0, info["giri"], info["scarto"],
                         info["quasi_energia"], info["partecipazione"]))
            except NonConverge as e:
                print("  %-6s %-7g %s" % (variante, x0, e))
