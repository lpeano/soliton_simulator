r"""L'AUTOINTERAZIONE DELL'INTERFERENZA — **dall'era `1`, portata nella camminata.**

**Decisione di Luca, `2026-10-11`.** L'era `1` ha `H_int = -(mu/2) sum_k |Psi_k|^2`, derivato in
una forza sulle fasi, e il suo commento dice: **<<la forma NON e' scelta: e' la derivata di
`|Psi|^2` rispetto a `phi`>>**.

> ## ⭐ **`S_k` E' IL CAMPO DI INTERFERENZA, E NON E' UN'ANALOGIA.**
> Dopo lo spostamento le estremita' del nodo `k` contengono le ampiezze **appena arrivate dai
> vicini**, ### **gia' trasportate con `U` nel riferimento di `k`** — quindi
> ### **`S_k = somma_a psi_{k,a}`** *(la somma della moneta di Grover)* e'
> ### **locale al nodo** *(nessuna lettura dei vicini)* e ### **covariante di gauge**
> *(`S -> g_k S`)*.

### ⭐ **E LA <<COERENZA>> DELL'ERA `1` DIVENTA UN'OSSERVABILE SENZA SCELTE:**
**`c_k = |S_k|^2 / (d_k rho_k)`**, in **`[0, 1]`** per Cauchy-Schwarz. ### ⚠ **E non e' la
media sui vicini**, che l'era `1` aveva **scartato** *(il guscio in antifase la abbatte)*: e'
**l'allineamento col campo locale**, che e' quello che il commento dell'era `1` usa.

| | la forma | `x` | sotto `C` | che cosa deve fare |
|---|---|---|---|---|
| **`(E)`** | il porto **letterale** | `\|S_k\|^2 / Lambda_k` | ### **PARI** | ### ⛔ **DEVE ROMPERE** `C` |
| **`(D)`** | l'**ELICITA' DELL'INTERFERENZA** | `h^S_k / Lambda_k` | ### **DISPARI** | ### ✅ **la candidata** |

con **`h^S_k = somma_a Re[psi_a^dag (sigma.n_a) S_k]`**.

### ⛔ **NIENTE FORMA CHIUSA, e il motivo e' preciso:** nel `v3` il flusso conserva `h` perche'
**ruota attorno a `n`**; qui **`S` e' una SOMMA**, quindi ruotare un'estremita' **cambia `S`** e
con lui il generatore. ### ✅ **Percio': PUNTO MEDIO IMPLICITO PER NODO** — locale, simmetrico,
e ### **la norma si conserva ESATTAMENTE**, perche' il campo e' `-i A(psi_m) psi_m` con
**`A` hermitiana** *(`h^S = psi^dag M psi` con `M_ab = (sigma.n_a + sigma.n_b)/2`)*.

### ⚠ **TOLLERANZA E ITERAZIONI DICHIARATE:** `n_est * eps` e **`64`** — ed e' il valore che
`primo_ordine/config/prova.yaml` usa gia' per il punto medio implicito dell'era `2`:
**un precedente, non un gusto.** ### ⛔ **E se non converge, SI FERMA.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import saturazione3 as S3                                      # noqa: E402
import vuoto3 as V3                                            # noqa: E402

EPS = float(np.finfo(float).eps)
# ### ⛔ **LE DUE COSTANTI DEL PUNTO MEDIO, DICHIARATE E DERIVATE.**
ITERAZIONI = 64


def _tolleranza(sc):
    """### `n_est * eps`: ### **lo stesso conteggio di operazioni delle altre soglie.**"""
    return 2 * sc["m"] * EPS


def campo_S(psi, sc):
    """### `S_k = somma_a psi_{k,a}`: ### **il campo di interferenza locale.**"""
    S = np.zeros((sc["n"], 2), dtype=complex)
    np.add.at(S, sc["nodo"], psi)
    return S


def coerenza(psi, sc):
    """### `c_k = |S_k|^2 / (d_k rho_k)`, in `[0, 1]`: ### **la <<coerenza>> dell'era `1`.**"""
    S = campo_S(psi, sc)
    rho = CM.rho_nodo(psi, sc)
    den = sc["grado"] * rho
    out = np.zeros(sc["n"], dtype=float)
    buoni = den > 0.0
    out[buoni] = np.sum(np.abs(S[buoni]) ** 2, axis=1) / den[buoni]
    return out


def _sigma_n(psi, geo):
    """`(sigma.n_a) psi_a`, per estremita'."""
    n = geo["n"]
    out = np.empty_like(psi)
    out[:, 0] = n[:, 2] * psi[:, 0] + (n[:, 0] - 1j * n[:, 1]) * psi[:, 1]
    out[:, 1] = (n[:, 0] + 1j * n[:, 1]) * psi[:, 0] - n[:, 2] * psi[:, 1]
    return out


def elicita_interferenza(psi, sc, geo):
    """### `h^S_k = somma_a Re[psi_a^dag (sigma.n_a) S_k]`.

    ### ✅ **E- invariante di gauge** *(ruotando ANCHE i versori)* e
    ### **DISPARI sotto `C`** — le due derivazioni stanno nel task history, e il collaudo
    ### **le misura.**
    """
    S = campo_S(psi, sc)
    sn = _sigma_n(psi, geo)                      # (sigma.n_a) psi_a
    # ### `psi_a^dag (sigma.n_a) S_k` = coniugato di `(sigma.n_a psi_a)` per `S_k`
    z = np.sum(np.conj(sn) * S[sc["nodo"]], axis=1)
    out = np.zeros(sc["n"], dtype=float)
    np.add.at(out, sc["nodo"], np.real(z))
    return out


def _gradiente_D(psi, sc, geo):
    """`dh^S/dpsi_a* = ((sigma.n_a) S_k + T_k)/2`, con `T_k = somma_b (sigma.n_b) psi_b`."""
    S = campo_S(psi, sc)
    sn = _sigma_n(psi, geo)
    T = np.zeros((sc["n"], 2), dtype=complex)
    np.add.at(T, sc["nodo"], sn)
    # ### `(sigma.n_a) S_k`: la matrice dell-estremita- applicata al campo del nodo
    fin = {"n": geo["n"]}
    sS = _sigma_n(S[sc["nodo"]], fin)
    return 0.5 * (sS + T[sc["nodo"]])


def _x_e_pezzi(psi, phi, sc, geo, quale):
    """`(x, G'(x), b(x))` per nodo, con il limite `Lambda -> 0` del `v3`."""
    lam = V3.lambda_nodo(phi, sc)
    if quale == "D":
        num = elicita_interferenza(psi, sc, geo)
    else:
        num = np.sum(np.abs(campo_S(psi, sc)) ** 2, axis=1)
    al, be = S3.pezzi(num, lam)
    return num, lam, al, be


def flusso_implicito(psi, phi, sc, geo, dtau, quale="D"):
    """### **IL PUNTO MEDIO IMPLICITO PER NODO**, iterato fino alla macchina.

    ### ⛔ **E FERMA se non converge:** <<procedere col meglio che ho>> sarebbe
    ### **un errore silenzioso**, e un errore silenzioso in un passo ### **sporca tutta la
    corsa.**
    """
    tol = _tolleranza(sc)
    dt_est = dtau[sc["nodo"]].reshape(-1, 1) if np.ndim(dtau) else dtau
    dt_nod = dtau if np.ndim(dtau) else np.full(sc["n"], dtau)
    p1, f1 = psi.copy(), phi.copy()
    for giro in range(ITERAZIONI):
        pm = 0.5 * (psi + p1)
        fm = 0.5 * (phi + f1)
        _num, _lam, al, be = _x_e_pezzi(pm, fm, sc, geo, quale)
        if quale == "D":
            campo = al[sc["nodo"]].reshape(-1, 1) * _gradiente_D(pm, sc, geo)
        else:
            campo = al[sc["nodo"]].reshape(-1, 1) * campo_S(pm, sc)[sc["nodo"]]
        p2 = psi - 1j * dt_est * campo
        f2 = phi - 1j * (be * dt_nod)[sc["nodo"]] * fm
        scarto = max(float(np.max(np.abs(p2 - p1))), float(np.max(np.abs(f2 - f1))))
        p1, f1 = p2, f2
        if scarto <= tol:
            return p1, f1
    raise SystemExit("[FERMO] il punto medio implicito NON converge: scarto %.3g dopo %d "
                     "iterazioni, tolleranza %.3g" % (scarto, ITERAZIONI, tol))


def flusso_D(psi, phi, sc, geo, dtau):
    """### **`(D)`**: l'elicita' dell'interferenza. ### **DISPARI sotto `C`.**"""
    return flusso_implicito(psi, phi, sc, geo, dtau, "D")


def flusso_E(psi, phi, sc, geo, dtau):
    """### **`(E)`**: il porto letterale su `|S|^2`. ### ⛔ **PARI: DEVE rompere `C`.**"""
    return flusso_implicito(psi, phi, sc, geo, dtau, "E")


LE_DUE_INTERF = (
    ("D", flusso_D, "l-ELICITA- DELL-INTERFERENZA: DISPARI sotto C, la candidata"),
    ("E", flusso_E, "il porto letterale su |S|^2: PARI, DEVE rompere C"),
)


if __name__ == "__main__":
    import camminata2 as C2
    import geometria as GE
    import scena as SC
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    geo = GE.scena_identita(sc)
    gauge = GE.scena_gauge_puro(sc, 11)
    psi = CM.stato_casuale(sc, 11)
    phi = V3.vuoto_fondo(sc)
    c = coerenza(psi, sc)
    print("  la coerenza c_k: min %.6f  max %.6f   (deve stare in [0,1])"
          % (c.min(), c.max()))
    h = elicita_interferenza(psi, sc, geo)
    print("  h^S_k: min %.4f  max %.4f" % (h.min(), h.max()))
    # ### la PARITA- sotto C, misurata
    hc = elicita_interferenza(C2.coniuga2(psi), sc, geo)
    print("  DISPARI sotto C?  max|h^S(C psi) + h^S(psi)| = %.3g"
          % float(np.max(np.abs(hc + h))))
    se = np.sum(np.abs(campo_S(psi, sc)) ** 2, axis=1)
    sec = np.sum(np.abs(campo_S(C2.coniuga2(psi), sc)) ** 2, axis=1)
    print("  e |S|^2 e- PARI?  max||S|^2(C psi) - |S|^2(psi)| = %.3g"
          % float(np.max(np.abs(sec - se))))
    # ### l-INVARIANZA DI GAUGE, misurata
    ruo = np.empty_like(psi)
    for e in range(2 * sc["m"]):
        k = int(sc["nodo"][e])
        ruo[e] = np.exp(1j * gauge["fi"][k]) * (gauge["g"][k] @ psi[e])
    hg = elicita_interferenza(ruo, sc, gauge)
    print("  INVARIANTE di gauge?  max|h^S - h^S'| = %.3g" % float(np.max(np.abs(h - hg))))
    hb = elicita_interferenza(ruo, sc, {"n": gauge["n_non_ruotati"]})
    print("  e SENZA ruotare i versori?  %.3g   ### deve essere GRANDE"
          % float(np.max(np.abs(h - hb))))
    # ### il PUNTO MEDIO: converge, conserva, e si inverte?
    for quale, f, _n in LE_DUE_INTERF:
        p1, f1 = f(psi, phi, sc, geo, np.full(sc["n"], 0.25))
        p0, f0 = f(p1, f1, sc, geo, np.full(sc["n"], -0.25))
        print("  (%s) norma psi %.3g  phi %.3g   e il ritorno: %.3g"
              % (quale, abs(CM.norma(p1) - CM.norma(psi)),
                 abs(V3.norma_vuoto(f1) - V3.norma_vuoto(phi)),
                 float(np.max(np.abs(p0 - psi)))))
