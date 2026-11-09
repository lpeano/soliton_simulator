# -*- coding: utf-8 -*-
r"""**T4-B, (t-b) E (t-a)** *(Luca `2026-11-09` `10:47`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `16.4`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t4b_sfondo.py > doc/referti_l2/u1_t4b_sfondo.txt

**(t-b):** il banco di `u1_t4b.py` con lo SFONDO DEL CAMPO AZZERATO: un tick di riferimento senza perturbazione registra la sorgente `J_rif` di ogni spostamento; nei tick
perturbati il campo riceve `E <- E - e (J - J_rif)` *(una copia di `_u1_prototipo.avvolto` con quella riga cambiata)*. La pendenza `p` di `ln V` contro `ln eps` come `u1_t4b_fase.py`.
**(t-a), sullo sfondo VERO:** `T4B-L'`, `T4B-P'` sui versi (->) e (<- ampiezza); `T4B-F'` *(DEVE FALLIRE: T4B-L' sul verso della fase)*. **La lettura di (t-b):** `b-s` o `b-m`.
"""
import contextlib
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL_L = 1e-6                  # ### sez. 16.4 (come T4B-L)
FATT_PAV = 1000.0              # ### sez. 16.4 (come u1_t4b_fase)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


@contextlib.contextmanager
def avvolto_senza_sfondo(U1, mot, campo, J_rif, registra):
    """### Le righe di `_u1_prototipo.avvolto`; ### **la sorgente meno quella del riferimento** *(`registra`: il tick di riferimento, che la REGISTRA e la toglie a se stesso)*."""
    op = mot.operatori
    vero_sp, vero_sv = op["spostamento_trasporto"], op["spostamento_scalare"]
    conta = [0]
    quale = [0]
    m = campo.m

    def sp(st, par, fr):
        v = st["psi_h"].reshape(m, 2, 2)
        prima = np.sum(np.abs(v[:, 0, :]) ** 2, axis=1)
        out = vero_sp(st, par, fr)
        J = np.sum(np.abs(v[:, 0, :]) ** 2, axis=1) - prima
        if registra:
            J_rif.append(J.copy())
        campo.E -= campo.e * (J - J_rif[quale[0]])
        quale[0] += 1
        return out

    def sv(st, par, fr):
        out = vero_sv(st, par, fr)
        conta[0] += 1
        if conta[0] % 2 == 1:
            campo.deriva(0.5)
            campo.deriva(0.5)
            U1.scrivi_U(mot, campo)
        return out
    op["spostamento_trasporto"], op["spostamento_scalare"] = sp, sv
    try:
        yield
    finally:
        op["spostamento_trasporto"], op["spostamento_scalare"] = vero_sp, vero_sv


def con_sfondo_azzerato(B, U1):
    """### Rimpiazza `B.tick` con quello senza sfondo; il riferimento registrato al primo tick, senza perturbazione."""
    J_rif = []

    def tick(dA=None, dE=None, dpsi=None):
        st, c = B.st, B.c
        for k, v in B.foto.items():
            st[k][...] = v
        c.A[...] = B.A0 + (0 if dA is None else dA)
        c.E[...] = B.E0 + (0 if dE is None else dE)
        if dpsi is not None:
            st["psi_h"][...] += dpsi
        U1.scrivi_U(B.mot, c)
        with avvolto_senza_sfondo(U1, B.mot, c, J_rif, registra=not J_rif):
            U1.tick(st, B.mot, B.par, c)
        return st["psi_h"].copy(), c.A.copy(), c.E.copy()
    _p, a0, e0 = tick()
    B.tick = tick
    return float(np.max(np.abs(a0))), float(np.max(np.abs(e0))), len(J_rif)


def misura(T4B, T4F, U1, bl, B, EPS3):
    """### Le righe di `u1_t4b_fase.main`: `V[(d, nk, verso, banda, eps)]`."""
    V = {}
    c = B.c
    n, m, L = c.n, c.m, T4B.L
    nodo = B.mot.inc.nodo
    psi0 = B.foto["psi_h"]
    for d in T4B.DIREZ:
        for nk in T4B.N_K:
            t1, t2 = 2 * math.pi * nk * d[0] / L, 2 * math.pi * nk * d[1] / L
            bk = T4B.bande_k(U1, bl, t1, t2)[0]
            fase = t1 * B.m1 + t2 * B.m2
            cosn = np.cos(fase)[nodo]
            for pnome, fatt in (("<-fase", 1j), ("<-ampiezza", 1.0)):
                dpsi = fatt * psi0 * cosn[:, None]
                dpsi = dpsi / float(np.sqrt(np.sum(np.abs(dpsi) ** 2)))
                for ep in EPS3:
                    for b, v in T4F.indietro(T4B, U1, B, bl, t1, t2, dpsi, ep).items():
                        V[(d, nk, pnome, b, ep)] = v
            for nm in ("fotone", "ottica"):
                u = bk[nm][1][0]
                u = u * np.exp(-1j * np.angle(u[int(np.argmax(np.abs(u)))]))
                x = np.zeros(2 * m)
                for i in range(6):
                    x[T4F.indici(m, n, i)] = np.real(u[i] * np.exp(1j * fase))
                nx = float(np.sqrt(np.sum(x * x)))
                for ep in EPS3:
                    pp = B.tick(dA=ep * x[:m] / nx, dE=ep * x[m:] / nx)[0]
                    pm = B.tick(dA=-ep * x[:m] / nx, dE=-ep * x[m:] / nx)[0]
                    V[(d, nk, "->", nm, ep)] = float(np.sqrt(np.sum(np.abs(pp - pm) ** 2))) / (2 * ep)
    return V


def main():
    import _presidio
    import _u1_prototipo as U1
    import _triangoli_forza as TF
    from solitone import u1_t4b as T4B
    from solitone import u1_t4b_fase as T4F
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(os.path.join(_QUI, "u1_t4b.py"))
    _presidio.avvia(os.path.join(_QUI, "u1_t4b_fase.py"))
    _presidio.avvia(__file__)
    estar = U1.E_PROVA[1]
    EPS3 = T4F.EPS3
    print("=" * 130)
    print("T4-B, (t-b) E (t-a) (sez. 16.4): L %d, s %g, e* %.10f, eps %s, conv %s; k = 2 pi n d / L, n %s, d %s" % (T4B.L, T4B.S, estar, EPS3, T4B.CONV, list(T4B.N_K), T4B.DIREZ))
    print("=" * 130)
    bl, _f, _r = U1.blocchi_campo(T4B.S)
    lne = np.log(np.array(EPS3))
    righe = [("<-fase", "fotone"), ("<-fase", "ottica"), ("<-fase", "gauge"), ("<-ampiezza", "fotone"), ("<-ampiezza", "ottica"), ("->", "fotone"), ("->", "ottica")]
    RIS = {}
    with TF.conv(T4B.CONV):
        for quale in ("vero", "azzerato"):
            B = T4B.Banco(U1, estar)
            if quale == "azzerato":
                amax, emax, nj = con_sfondo_azzerato(B, U1)
                print("### (t-b) lo sfondo azzerato: %d sorgenti registrate nel tick di riferimento; il campo del riferimento dopo un tick max|A| %.1e max|E| %.1e (deve essere 0)" % (nj, amax, emax))
            _p0, a0, e0 = B.tick()
            scala = {"<-": float(np.sqrt(np.sum(a0 * a0) + np.sum(e0 * e0))), "->": float(np.sqrt(np.sum(np.abs(_p0) ** 2)))}
            V = misura(T4B, T4F, U1, bl, B, EPS3)
            print("-" * 130)
            if quale == "azzerato":
                # ### lo sfondo e' zero: cio' che si sottrae in (<-) e' la sola risposta alla perturbazione (~ eps x V totale): il pavimento e' RELATIVO, 1000 eps_macchina x (V fotone + ottica + gauge) a quel k e quel eps
                print("### lo sfondo AZZERATO: il pavimento di (<-) relativo alla risposta totale a ogni k e eps; quello di (->) con la scala %.6f" % scala["->"])
            else:
                print("### lo sfondo VERO: le scale del pavimento: (<-) %.3e, (->) %.6f" % (scala["<-"], scala["->"]))
            print("  %6s %3s | %s" % ("d", "n", " | ".join("%-21s" % ("%s %s" % r) for r in righe)))
            P = {}
            for d in T4B.DIREZ:
                for nk in T4B.N_K:
                    pezzi = []
                    for (ver, b) in righe:
                        y = np.array([V[(d, nk, ver, b, ep)] for ep in EPS3])
                        if quale == "azzerato" and ver.startswith("<-"):
                            pav = FATT_PAV * np.finfo(float).eps * np.array([sum(V[(d, nk, ver, bb, ep)] for bb in ("fotone", "ottica", "gauge")) for ep in EPS3])
                        else:
                            pav = FATT_PAV * np.finfo(float).eps * scala[ver[:2]] / np.array(EPS3)
                        tl = abs(y[0] - y[1]) / y[0] if y[0] > 0 else float("nan")
                        if np.any(y <= pav):
                            P[(d, nk, ver, b)] = (None, tl, y[0])
                            pezzi.append("%-21s" % ("pav (V %.1e)" % y[0]))
                        else:
                            p = float(np.polyfit(lne, np.log(y), 1)[0])
                            P[(d, nk, ver, b)] = (p, tl, y[0])
                            pezzi.append("%-21s" % ("p %+.3f L %.1e" % (p, tl)))
                    print("  %6s %3d | %s" % ("%d,%d" % d, nk, " | ".join(pezzi)))
            RIS[quale] = P
    print("-" * 130)

    def sopra(qu, ver, b):
        return [v for (d, nk, vv, bb), v in RIS[qu].items() if vv == ver and bb == b and v[0] is not None]
    # ------------------------------------------------------------------ (t-b): la lettura
    nf = len(sopra("azzerato", "<-fase", "fotone")) + len(sopra("azzerato", "<-fase", "ottica"))
    nfv = len(sopra("vero", "<-fase", "fotone")) + len(sopra("vero", "<-fase", "ottica"))
    print("  (t-b) fotone e ottica in fase sopra il pavimento: sfondo vero %d k su 48, sfondo azzerato %d k su 48" % (nfv, nf))
    print("  LA LETTURA DI (t-b): (%s)" % ("b-s: la parte che restava e' dello SFONDO" if nf == 0 else "b-m: resta con lo sfondo azzerato: e' della risposta della materia al campo"))
    # ------------------------------------------------------------------ (t-a), sullo sfondo vero
    for ver in ("->", "<-ampiezza"):
        for b in ("fotone", "ottica"):
            ss = sopra("vero", ver, b)
            tot = len([1 for (d, nk, vv, bb) in RIS["vero"] if vv == ver and bb == b])
            peg = max(v[1] for v in ss) if ss else float("nan")
            esito("T4B-L' %s %s: |V(1e-4) - V(5e-5)| / V(1e-4) <= %g a ogni k sopra il pavimento" % (ver, b, TOLL_L), bool(ss) and peg <= TOLL_L, "%d k su %d; il peggiore %.2e" % (len(ss), tot, peg))
    for ver in ("->", "<-ampiezza"):
        tutti = [v for (d, nk, vv, bb), v in RIS["vero"].items() if vv == ver and bb == "fotone"]
        esito("T4B-P' il fotone (%s): V sopra %g x il pavimento con la scala a ogni k" % (ver, FATT_PAV), all(v[0] is not None for v in tutti), "il minimo V %.4e; sotto il pavimento %d k" % (min(v[2] for v in tutti), sum(v[0] is None for v in tutti)))
    ssf = sopra("vero", "<-fase", "fotone") + sopra("vero", "<-fase", "ottica")
    esito("T4B-F' T4B-L' applicato al verso della fase (fotone e ottica)", bool(ssf) and max(v[1] for v in ssf) <= TOLL_L, "%d k sopra il pavimento; il peggiore %s" % (len(ssf), ("%.2e" % max(v[1] for v in ssf)) if ssf else "-"), deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
