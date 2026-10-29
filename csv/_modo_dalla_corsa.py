# -*- coding: utf-8 -*-
r"""**IL MODO INSTABILE LETTO DALLA CORSA** *(il mandato di Luca delle `09:21` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_modo_dalla_corsa.md`)*: ### **`600` tick dallo stato fermo di `L 81`** *(al bit con `26300537`)*;
### **lo scostamento `D(t) = e^{i mu s t} psi(t) - psi0`: il tasso, la rotazione, la forma;** ### **la conferma con Arnoldi su `G^10`, partendo da `D(450)`.**

    python csv/_modo_dalla_corsa.py --referto > doc/referti_l2/modo_dalla_corsa.txt
"""
import io
import json
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

T_FINE = 600
T_DA = 200
OGNI = 10
FATTORE_RUMORE = 1e3           # ### la finestra comincia sopra FATTORE_RUMORE volte il residuo dello stato fermo
SATURAZIONE = 1e-2             # ### e finisce prima di |D|/|psi0| = SATURAZIONE
T_FORMA = (400, 450, 500)
T_RIF = 450
K_AUT = 2
NCV = 20
TOLL_ARNOLDI = 1e-6
RIAVVII = 20
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def forma(mp, Z, d, etichetta):
    import _dove_va_la_materia as DV
    import _modo_instabile as MI
    d = d / float(np.linalg.norm(d))
    dr, df = MI.per_nodo(mp, d)
    wd, kk = MI.armoniche(mp, dr)
    wf, _k = MI.armoniche(mp, df)
    pr = np.bincount(kk, weights=np.sum(np.abs(d.reshape(mp.n, 12)) ** 2, axis=1))
    pr = pr / pr.sum()
    Pk = DV.pesi(d.reshape(mp.n, 12), np.ones(mp.n), Z, MI.L)
    tot = float(Pk.sum())
    print("  %s: le armoniche di drho:  %s" % (etichetta, " ".join("m%d %.4f" % (mm, wd[mm]) for mm in range(MI.M_MAX + 1))))
    print("  %s: le armoniche della fase: %s" % (etichetta, " ".join("m%d %.4f" % (mm, wf[mm]) for mm in range(MI.M_MAX + 1))))
    print("  %s: le bande: %s" % (etichetta, "  ".join("%s %.5f" % (nome, float(Pk[:, :, list(idx)].sum()) / tot) for nome, idx in DV.GRUPPI)))
    print("  %s: il profilo radiale di |D|^2, r 0..%d: %s" % (etichetta, MI.R_PROFILO, " ".join("%.4f" % x for x in pr[:MI.R_PROFILO + 1])))
    return wd, wf


def referto():
    from scipy.sparse.linalg import LinearOperator, eigs, ArpackNoConvergence
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _modo_instabile as MI
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    print("=" * 130)
    print("IL MODO INSTABILE LETTO DALLA CORSA (Luca 09:21): L %d, s 0.3, N 1e6; %d tick dallo stato fermo; D(t) = e^{i mu s t} psi(t) - psi0" % (MI.L, T_FINE))
    print("=" * 130)
    print("  la configurazione: T_FINE %d T_DA %d OGNI %d FATTORE_RUMORE %g SATURAZIONE %g T_FORMA %s T_RIF %d K_AUT %d NCV %d TOLL_ARNOLDI %g RIAVVII %d; da _modo_instabile: P %d H_REL %g M_MAX %d"
          % (T_FINE, T_DA, OGNI, FATTORE_RUMORE, SATURAZIONE, T_FORMA, T_RIF, K_AUT, NCV, TOLL_ARNOLDI, RIAVVII, MI.P, MI.H_REL, MI.M_MAX))
    print("  LE LETTURE DI LUCA (08:24), SCRITTE PRIMA: (a) m = 0 in A; (b) m >= 1 in A (quale); (c) peso in B o nelle piatte; (d) altro (per esempio un modo di sola fase)")
    print("-" * 130)
    mp = MI.Mappa()
    S = mp.SFM.S
    esito("DEVE PASSARE: lo stato fermo sul disco = quello della ricerca (sha1)", mp.sha_ok, "")
    r1 = float(np.linalg.norm(mp.G(mp.psi0, 1) - mp.psi0) / np.linalg.norm(mp.psi0))
    print("  il residuo dello stato fermo %.3e; mu %+.9f" % (r1, mp.mu))
    rifs = json.loads(io.open(os.path.join(mp.SFM.PUNTI, "corsa_L%d_00000.jsonl" % MI.L), encoding="utf-8").read())
    rif = {p["t"]: p for p in rifs["punti"]}
    w_in, w0 = rifs["w_in"], rifs["w0"]
    n0 = float(np.linalg.norm(mp.psi0))
    psi = mp.psi0.copy()
    D = {}
    alpunto = True
    s0 = time.time()
    for t in range(1, T_FINE + 1):
        psi = mp.SFM.tick(mp.z, mp.phi0, psi)
        if t % OGNI == 0:
            mp.z["st"]["psi_h"][...] = psi
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                pt = CL.punto(mp.z, t, w_in, w0)
            alpunto = alpunto and all(pt[k] == rif[t][k] for k in ("w", "f_win", "f_3w0", "picco", "M"))
            if t >= T_DA:
                D[t] = np.exp(1j * mp.mu * S * t) * psi - mp.psi0
    esito("DEVE PASSARE: i punti ogni %d tick fino a %d = la corsa di 26300537, AL BIT" % (OGNI, T_FINE), alpunto, "%.0f s" % (time.time() - s0))
    print("-" * 130)
    print("### IL TASSO")
    ts = sorted(D)
    nD = np.array([float(np.linalg.norm(D[t])) / n0 for t in ts])
    for i, t in enumerate(ts):
        loc = ""
        if 0 < i < len(ts) - 1:
            loc = "pendenza locale %+.5f per tick" % ((math.log(nD[i + 1]) - math.log(nD[i - 1])) / (2.0 * OGNI))
        print("  t %3d: |D|/|psi0| %.4e  %s" % (t, nD[i], loc))
    basso = FATTORE_RUMORE * r1
    fin = [i for i in range(len(ts)) if basso < nD[i] < SATURAZIONE]
    if fin:
        a, b = fin[0], fin[-1]
        while b > a and not (nD[b] < SATURAZIONE):
            b -= 1
        tt = np.array(ts[a:b + 1], dtype=float)
        pend, inter = np.polyfit(tt, np.log(nD[a:b + 1]), 1)
        res = np.log(nD[a:b + 1]) - (pend * tt + inter)
        print("  la finestra: t %d .. %d (|D|/|psi0| da %.2e a %.2e; i bordi %.1e e %.0e); la pendenza %.5f per tick, %.5f per unita' di tempo; lo scarto dalla retta max %.3e"
              % (ts[a], ts[b], nD[a], nD[b], basso, SATURAZIONE, pend, pend / S, float(np.abs(res).max())))
    print("### LA ROTAZIONE")
    dr = D[T_RIF]
    proj = []
    for i, t in enumerate(ts[:-1]):
        u, v = D[t], D[ts[i + 1]]
        c = complex(np.vdot(u, v)) / (float(np.linalg.norm(u)) * float(np.linalg.norm(v)))
        p = float(np.real(np.vdot(dr, D[t]))) / (float(np.linalg.norm(dr)) * float(np.linalg.norm(D[t])))
        proj.append(p)
        print("  t %3d -> %3d: Re<D, D'> / |D||D'| %+.5f  |<D, D'>| / |D||D'| %.5f  Re<D(%d), D(t)> / |..| %+.5f" % (t, ts[i + 1], c.real, abs(c), T_RIF, p))
    if fin:
        pp = np.array(proj[a:min(b, len(proj) - 1) + 1])
        cambi = [i for i in range(1, len(pp)) if pp[i - 1] * pp[i] < 0.0]
        if len(cambi) >= 2:
            per = 2.0 * OGNI * float(np.mean(np.diff(cambi)))
            print("  il periodo dai cambi di segno nella finestra: %.1f tick (%.2f unita' di tempo), %d cambi" % (per, per * S, len(cambi)))
        else:
            print("  nella finestra %d cambi di segno: nessun periodo misurabile" % len(cambi))
    print("-" * 130)
    print("### LA FORMA DI D (normalizzato)")
    A = DV.matrice(mp.z, mp.phi0, DV.AMP)
    _ph, Z = DV.autovettori(A)
    for t in T_FORMA:
        forma(mp, Z, D[t], "t %d" % t)
    print("-" * 130)
    print("### LA CONFERMA CON ARNOLDI su G^%d (NON un sigillo): k %d, ncv %d, tol %g, %d riavvii, partenza D(%d)" % (MI.P, K_AUT, NCV, TOLL_ARNOLDI, RIAVVII, T_RIF))
    op = LinearOperator((2 * mp.m, 2 * mp.m), matvec=mp.jv, dtype=float)
    v0 = mp.a_v(D[T_RIF])
    v0 = v0 / float(np.linalg.norm(v0))
    c0 = mp.conti
    s0 = time.time()
    try:
        lam, W = eigs(op, k=K_AUT, which="LM", ncv=NCV, tol=TOLL_ARNOLDI, maxiter=RIAVVII, v0=v0)
        conv = True
    except ArpackNoConvergence as e:
        lam, W = e.eigenvalues, e.eigenvectors
        conv = False
    print("  Arnoldi: %s; %d autovalori; %d tick; %.0f s" % ("converge" if conv else "NON converge", len(lam), mp.conti - c0, time.time() - s0))
    for i in range(len(lam)):
        l = lam[i]
        Q, _r = np.linalg.qr(np.array([W[:, i].real, W[:, i].imag]).T)
        ov = float(np.linalg.norm(Q.T @ v0) ** 2)
        print("  %d: lambda %+.6f %+.6fi, |lambda| %.6f; il tasso ln|lambda|/(%d s) %+.5f per unita' di tempo, %+.5f per tick; la fase per %d tick %+.5f; la sovrapposizione con D(%d) %.5f"
              % (i, l.real, l.imag, abs(l), MI.P, math.log(abs(l)) / (MI.P * S), math.log(abs(l)) / MI.P, MI.P, math.atan2(l.imag, l.real), T_RIF, ov))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if argv[:1] == ["--referto"]:
        referto()
    else:
        raise SystemExit(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
