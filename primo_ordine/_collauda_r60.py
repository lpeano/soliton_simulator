# -*- coding: utf-8 -*-
"""`R60` -- **LE ROTAZIONI DEL RETICOLO COMMUTANO COL TICK DEL NUCLEO**

> ### ⛔ **La decisione di Luca del `2026-11-08` `14:19` (v1):** `R180 x sigma_z` e `R60 x S60`
> nella suite, coi loro DEVE FALLIRE. ### **E la nota (n1) delle `15:51`:** **dopo v2 il
> collaudo gira sul tick del NUCLEO, senza importare da `csv/`** *(resta `_presidio`, come in
> ogni collaudo del nucleo)*. **Il task history:**
> `doc/TASK_HISTORY/2026-11-08_zero_simmetrico_nel_nucleo.md`; **la carta che li ha misurati
> per prima:** `csv/solitone/carta_r60.py` *(`doc/referti_l2/simmetria_r60.txt`)*.

## I CASI *(fissati prima)*

- **(s)** la `S` DERIVATA *(la permutazione delle sei estremita' `x` `S60 = exp(-i pi/6 sigma_z)`)*
  e' il nucleo, di dimensione `1`, delle `S` `12 x 12` che commutano con la parte lineare del
  tick *(senza i pezzi che leggono `rho`)*;
- **(a)** `R60 x S60` commuta col tick INTERO, `N_T` tick, sui semi dichiarati: `r <= SOGLIA`;
- **(b)** `R180 x sigma_z` lo stesso;
- **(c)** ### **DEVE FALLIRE:** `R60` con la sola permutazione *(`S = I` sullo spin)*;
- **(d)** ### **DEVE FALLIRE:** `R180` con `U = 1`.

**La scena:** `scena_l2.scena_toro("triangoli", (L, L), DTAU, X)` *(il toro del nucleo, `cs`
spento, `U = I`, `eps` dalla tabella)*; ### **il vuoto `F3` scritto dalla sua definizione**
*(per l'arco lungo l'asse `a` la coda `+e^{i theta_a}`, la testa `-e^{i theta_a}`, `theta` =
`0`, `0`, `pi` per gli assi `(1,0)`, `(0,1)`, `(1,1)`: la stessa di
`csv/_solitone_dal_fondo.fondo_con_fasi`)*. **`SOGLIA = 2 x 14 x N_T x 10 eps`.**

Gira con:  python primo_ordine/_collauda_r60.py
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402

L_R60 = 12
DTAU = 0.15                    # il passo delle corse dell'era 2 (s = 0.15)
X = 1.0                        # la materia della scena, sovrascritta dagli stati casuali
SEMI = (1, 2)
N_T = 10
FLOP_PEZZO = 10
EPS = float(np.finfo(float).eps)
SOGLIA = 2 * 14 * N_T * FLOP_PEZZO * EPS
SV_REL = 1e-10
FASI_F3 = (0.0, 0.0, math.pi)  # per gli assi (1,0), (0,1), (1,1): F3
S60 = np.diag([np.exp(-1j * math.pi / 6.0), np.exp(1j * math.pi / 6.0)])
SZ = np.diag([1.0 + 0j, -1.0])
OK = [0, 0]


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-96s %s   %s" % (che[:96], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def estremita_per_direzione(inc, nv):
    """`ext[v, j]`: l'estremita' del nodo `v` con direzione uscente `j` (l'angolo di `n` diviso 60 gradi)."""
    ang = np.degrees(np.arctan2(nv[:, 1], nv[:, 0]))
    j = np.rint(ang / 60.0).astype(int) % 6
    assert float(np.max(np.abs(ang - 60.0 * np.rint(ang / 60.0)))) <= 1e-9, "una direzione non e' a multipli di 60 gradi"
    ext = -np.ones((inc.n, 6), dtype=np.int64)
    ext[inc.nodo, j] = np.arange(2 * inc.m)
    assert np.all(ext >= 0) and len(np.unique(ext)) == 2 * inc.m, "un nodo non ha le sei direzioni"
    return ext


def mappa_nodi(L, k):
    """Il nodo immagine per R(60 k) attorno al nodo 0: (m1, m2) -> (m1 - m2, m1)."""
    v = np.arange(L * L)
    m1, m2 = v // L, v % L
    for _ in range(k % 6):
        m1, m2 = (m1 - m2) % L, m1 % L
    return m1 * L + m2


def applica(x, ext, nm, S):
    """R_S su x (per estremita', (2m, c)): il vettore locale del nodo v, per S, nel nodo nm[v]."""
    c = x.shape[1]
    X_ = x[ext].reshape(ext.shape[0], 6 * c)
    out = np.empty_like(x)
    out[ext[nm]] = (X_ @ S.T).reshape(ext.shape[0], 6, c)
    return out


def S_derivata(k, spin):
    """La permutazione j -> j + k delle direzioni, per spin."""
    P = np.zeros((6, 6))
    for j in range(6):
        P[(j + k) % 6, j] = 1.0
    return np.kron(P, spin)


def vuoto_f3(inc):
    """F3: per l'arco 3v + a la coda +e^{i theta_a}, la testa -e^{i theta_a}."""
    k = np.arange(inc.m)
    c = np.exp(1j * np.asarray(FASI_F3)[k % 3])
    phi = np.empty(2 * inc.m, dtype=complex)
    phi[0::2], phi[1::2] = c, -c
    return phi


def main(argv):
    del argv
    import composizione as CM
    import scena_l2 as SL
    import tick as TK
    _presidio.avvia(__file__)
    print("=" * 100)
    print("R60: LE ROTAZIONI DEL RETICOLO COMMUTANO COL TICK DEL NUCLEO (L %d, dtau %g, N_T %d, semi %s, SOGLIA %.3e)" % (L_R60, DTAU, N_T, SEMI, SOGLIA))
    print("=" * 100)
    ids = [i for i, _f, _t in CM.ORDINE]
    inc, mot, st, par = SL.scena_toro("triangoli", (L_R60, L_R60), DTAU, X)
    L = L_R60
    ext = estremita_per_direzione(inc, mot.geo.n)
    st["phi_h"][...] = vuoto_f3(inc)
    chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
    base = {k: st[k].copy() for k in chiavi}

    def rimetti():
        for k in chiavi:
            st[k][...] = base[k]

    salta = tuple(i for i in ("CAMM-MATERIA-VUOTO", "CAMM-FASE-VUOTO") if i in ids)

    def lineare(x):
        st["psi_h"][...] = x
        mot.apri_tick()
        for idl, fr, _t in CM.ORDINE:
            if idl in salta:
                continue
            nome, vp = TK.OPERATORE[idl]
            mot.operatori[nome](st, par if vp else {}, fr)
        mot.chiudi_tick()
        return st["psi_h"].copy()

    def tick_n(x):
        st["psi_h"][...] = x[0]
        st["phi_h"][...] = x[1]
        for _ in range(N_T):
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
        return st["psi_h"].copy(), st["phi_h"].copy()

    def R(x, k, spin):
        nm = mappa_nodi(L, k)
        return (applica(x[0], ext, nm, S_derivata(k, spin)),
                applica(x[1].reshape(-1, 1), ext, nm, S_derivata(k, np.eye(1))).reshape(-1))

    # -------------------------------------------------------------- (s) la S derivata
    rng = np.random.default_rng(SEMI[0])
    xs = [rng.normal(size=st["psi_h"].shape) + 1j * rng.normal(size=st["psi_h"].shape) for _ in SEMI]
    nm1 = mappa_nodi(L, 1)
    righe = []
    for x in xs:
        rimetti()
        Tx = lineare(x)
        col = []
        for a in range(12):
            for b in range(12):
                E = np.zeros((12, 12))
                E[a, b] = 1.0
                rimetti()
                col.append((lineare(applica(x, ext, nm1, E)) - applica(Tx, ext, nm1, E)).ravel())
        righe.append(np.array(col).T)
    _u, sv, vh = np.linalg.svd(np.vstack(righe), full_matrices=False)
    dim = int(np.sum(sv <= sv[0] * SV_REL))
    Sd = S_derivata(1, S60)
    Sf = np.conj(vh[-1]).reshape(12, 12)
    cos_ = abs(np.vdot(Sd.ravel(), Sf.ravel())) / (np.linalg.norm(Sd) * np.linalg.norm(Sf))
    esito("(s) il nucleo di R60 sulla parte lineare ha dimensione 1 ed e' la S derivata (entro 1e-10)", dim == 1 and abs(cos_ - 1.0) <= 1e-10,
          "dim %d, coseno %.15f" % (dim, cos_))
    # -------------------------------------------------------------- (a)-(d) il tick intero
    casi = (("(a) R60 x S60", 1, S60, True), ("(b) R180 x sigma_z", 3, SZ, True),
            ("### (c) DEVE FALLIRE: R60 con la sola permutazione", 1, np.eye(2, dtype=complex), False),
            ("### (d) DEVE FALLIRE: R180 con U = 1", 3, np.eye(2, dtype=complex), False))
    res = {c[0]: [] for c in casi}
    for seme in SEMI:
        rg = np.random.default_rng(seme)
        x = ((rg.normal(size=st["psi_h"].shape) + 1j * rg.normal(size=st["psi_h"].shape)) / math.sqrt(2.0), base["phi_h"].copy())
        nx = math.sqrt(float(np.sum(np.abs(x[0]) ** 2) + np.sum(np.abs(x[1]) ** 2)))
        rimetti()
        Tx = tick_n(x)
        for nome, k, spin, _deve in casi:
            rimetti()
            a = tick_n(R(x, k, spin))
            b = R(Tx, k, spin)
            res[nome].append(math.sqrt(float(np.sum(np.abs(a[0] - b[0]) ** 2) + np.sum(np.abs(a[1] - b[1]) ** 2))) / nx)
    rimetti()
    for nome, _k, _s, deve in casi:
        if deve:
            esito("%s commuta col tick intero, %d tick, ogni seme: r <= %.2e" % (nome, N_T, SOGLIA), max(res[nome]) <= SOGLIA, "il massimo %.2e" % max(res[nome]))
        else:
            esito("%s: r <= %.2e" % (nome, SOGLIA), min(res[nome]) > SOGLIA, "il minimo %.2e" % min(res[nome]))
    print("=" * 100)
    print("R60: %d su %d  %s" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
