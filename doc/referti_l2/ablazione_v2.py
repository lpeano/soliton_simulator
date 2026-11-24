# -*- coding: utf-8 -*-
r"""**[M1658-A] L'ABLAZIONE (iii): GROVER -> LA MONETA DI FOURIER A SEI VIE** *(Luca: «SI', in memoria, con lo stesso metodo»; la carta `doc/CARTA_fondo_giusto.md`, sez. `4-bis`; `ablazione.py` e' usato e non si riscrive: qui le sue funzioni, e una variante in piu')*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/ablazione_v2.py > doc/referti_l2/ablazione_v2.txt

**(iii):** la voce `grover` di `mot.operatori` sostituita IN MEMORIA: `F(theta/2)` due volte, poi `conj(z_nodo(f/2))` *(le righe di `flussi_parziali.grover` con `_grover_mezzo` -> la Fourier)*; `F(theta) = e^{i theta H_F/pi}`, `H_F = -i log F` *(il ramo principale)*; `F_ab = omega^{ab}/sqrt 6` sulle sei estremita' del nodo in senso antiorario da `A1`, l'identita' sullo spin. **Tutte le varianti di `ablazione.py` di nuovo** *((0) il caso noto al bit; la v1 legge (i), (ii), (iv), (iv-b) per K5)* **e (iii) in coda.**
"""
import contextlib
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import ablazione as AB  # noqa: E402

TC, CS = AB.TC, AB.CS


def fourier():
    w = np.exp(2j * np.pi / 6)
    F = np.array([[w ** (a * b) for b in range(6)] for a in range(6)]) / math.sqrt(6.0)
    mu, U = np.linalg.eig(F)
    U, _r = np.linalg.qr(U)
    lam = np.angle(np.diag(U.conj().T @ F @ U))
    H = U @ np.diag(lam) @ U.conj().T
    H = 0.5 * (H + H.conj().T)
    return F, H


def estremita(Z):
    """### `E[v, a]` = il mezzo arco del nodo `v` nella direzione `a` *(`a * 60` gradi da `A1`, antiorario)*."""
    from solitone import toro as TO
    mot, L = Z["mot"], Z["L"]
    nodo = np.asarray(mot.inc.nodo)
    altro = nodo[np.arange(len(nodo)) ^ 1]
    A1, A2 = TO.vettori()
    d1 = ((np.asarray(Z["m1"])[altro] - np.asarray(Z["m1"])[nodo] + 0.5 * L) % L) - 0.5 * L
    d2 = ((np.asarray(Z["m2"])[altro] - np.asarray(Z["m2"])[nodo] + 0.5 * L) % L) - 0.5 * L
    v = d1[:, None] * np.asarray(A1, float)[:2] + d2[:, None] * np.asarray(A2, float)[:2]
    ang = np.degrees(np.arctan2(v[:, 1], v[:, 0])) % 360.0
    a = np.rint(ang / 60.0).astype(int) % 6
    assert float(np.max(np.abs(ang - 60.0 * np.rint(ang / 60.0)))) < 1e-9, "una direzione NON e' un multiplo di 60 gradi"
    n = mot.inc.n
    E = -np.ones((n, 6), dtype=np.int64)
    E[nodo, a] = np.arange(len(nodo))
    assert np.all(E >= 0) and np.all(np.bincount(nodo, minlength=n) == 6), "un nodo NON ha una estremita' per direzione"
    return E


@contextlib.contextmanager
def grover_fourier(Z):
    import flussi_parziali as FP
    mot = Z["mot"]
    F, H = fourier()
    lamH, VH = np.linalg.eigh(H)
    E = estremita(Z)
    nodo = np.asarray(mot.inc.nodo)
    vecchio = mot.operatori["grover"]

    def mezzo(psi, h):
        z = np.asarray(FP.z_nodo(mot, h)).reshape(-1)
        assert np.all(z == z[0]), "z NON uniforme"
        th = float(np.angle(z[0]))
        M = VH @ np.diag(np.exp(1j * th * lamH / np.pi)) @ VH.conj().T
        X = psi[E]
        psi[E] = np.einsum("ab,nbc->nac", M, X)

    def nuovo(st, par, frazione):
        h = 0.5 * float(frazione)
        psi = st["psi_h"]
        mezzo(psi, h)
        mezzo(psi, h)
        z = np.asarray(FP.z_nodo(mot, h)).reshape(-1)
        psi *= np.conj(z)[nodo][:, None]
        return psi
    Mpi = VH @ np.diag(np.exp(1j * lamH)) @ VH.conj().T
    print("    la Fourier: |F(pi) - F| %.2e; |F F^dag - I| %.2e; gli autovalori di H_F %s" % (float(np.max(np.abs(Mpi - F))), float(np.max(np.abs(F @ F.conj().T - np.eye(6)))), " ".join("%+.4f" % x for x in lamH)))
    mot.operatori["grover"] = nuovo
    try:
        yield
    finally:
        mot.operatori["grover"] = vecchio


def risposta_fourier():
    """### `ablazione.risposta` riga per riga, col Grover della materia sostituito."""
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    A_IMP = T4B.A_IMP
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    with TC.scena() as Z:
        mot, st = Z["mot"], Z["st"]
        n, L, s = mot.inc.n, Z["L"], float(Z["s"])
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        base = {x: st[x].copy() for x in Z["chiavi"]}
        A0, E0_, U0 = C.campo.A.copy(), C.campo.E.copy(), mot.geo.U.copy()
        R = np.zeros((n, 12, 12), dtype=complex)
        with grover_fourier(Z):
            for j in range(12):
                us = []
                for f in (1.0, -1.0):
                    for x in Z["chiavi"]:
                        st[x][...] = base[x]
                    p = np.zeros((n, 12), dtype=complex)
                    p[0, j] = f * A_IMP
                    st["psi_h"][...] = p.reshape(st["psi_h"].shape)
                    C.campo.A[...], C.campo.E[...] = A0, E0_
                    mot.geo.U[...] = U0
                    mot.lambda_c = None
                    AB.tick_abl(Z["z"], C.campo, s, e0, np.ones(n), ())
                    us.append(st["psi_h"].reshape(n, 12).copy())
                R[:, :, j] = (us[0] - us[1]) / (2 * A_IMP)
        d0 = TO.scarti(Z["m1"], Z["m2"], 0.0, 0.0, L)[:, :2]
        for x in Z["chiavi"]:
            st[x][...] = base[x]
        Z["metti"]()
    sup = np.nonzero(np.abs(R).reshape(n, -1).max(axis=1) > 0.0)[0]
    return R[sup], d0[sup]


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "ablazione.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1658-A] L'ABLAZIONE (iii): GROVER -> FOURIER (la carta sez. 4-bis): (0) il caso noto e (iii)")
    print("=" * 130)
    vecchia = AB.risposta

    def risposta(salta, zero):
        return risposta_fourier() if salta == ("FOURIER",) else vecchia(salta, zero)
    AB.risposta = risposta
    AB.VARIANTI = AB.VARIANTI + (("iii", "Grover -> la moneta di Fourier a sei vie (il ramo principale)", ("FOURIER",), False),)
    return AB.main()


if __name__ == "__main__":
    sys.exit(main())
