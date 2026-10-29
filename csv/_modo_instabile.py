# -*- coding: utf-8 -*-
r"""**IL MODO INSTABILE DELLO STATO FERMO DI S1** *(il mandato di Luca delle `08:24` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_modo_instabile.md`)*: ### **lo spettro della mappa del tick linearizzata sullo stato fermo salvato** *(`L 81`)*,
### **nel sistema che ruota** *(`G = e^{i mu s} T`)*, ### **reale-lineare; Arnoldi a modulo massimo su `G^P`;** ### **la forma del modo** *(armoniche angolari, profilo, bande)*;
### **il controllo indipendente a `450` tick.**

> ### **Lo stato fermo:** `db/stato_fermo/fermo_L81.npz` *(`python csv/_stato_fermo.py --cerca 81`: il dato e' il comando)*.

    python csv/_modo_instabile.py --referto > doc/referti_l2/modo_instabile.txt
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

L = 81
P = 10                         # ### tick per prodotto
H_REL = 1e-5
K_AUT = 6
NCV = 40
TOLL_ARNOLDI = 1e-8
RIAVVII = 30
M_MAX = 12                     # ### le armoniche angolari m = 0 .. M_MAX
ANELLO = 1.0
R_PROFILO = 30
T_CONTROLLO = 450
TOLL_LIN = 1e-4
SEME = 20261029
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


class Mappa:
    """### **`G^P` e la sua linearizzazione attorno allo stato fermo** *(il vettore reale: parte reale e parte immaginaria)*."""

    def __init__(self):
        import _stato_fermo as SFM
        self.SFM = SFM
        self.rec, self.z, self.phi0, _p0 = SFM.scena(L)
        cj = json.loads(io.open(os.path.join(SFM.PUNTI, "cerca_L%d.json" % L), encoding="utf-8").read())
        fe = np.load(os.path.join(SFM.STATI, "fermo_L%d.npz" % L))
        self.sha_ok = SFM.sha(fe["psi_h"]) == cj["sha"]
        self.psi0 = fe["psi_h"].copy()
        self.mu = float(fe["mu"])
        self.forma = self.psi0.shape
        self.m = self.psi0.size
        self.n = self.z["inc"].n
        self.rot = np.exp(1j * self.mu * SFM.S)
        self.conti = 0

    def G(self, psi, quanti):
        for _t in range(quanti):
            psi = self.rot * self.SFM.tick(self.z, self.phi0, psi)
            self.conti += 1
        return psi

    def a_psi(self, v):
        return (v[:self.m] + 1j * v[self.m:]).reshape(self.forma)

    def a_v(self, psi):
        p = psi.ravel()
        return np.concatenate([p.real, p.imag])

    def jv(self, v, rel=H_REL):
        nv = float(np.linalg.norm(v))
        h = rel * float(np.linalg.norm(self.psi0)) / nv
        d = self.a_psi(v)
        return self.a_v(self.G(self.psi0 + h * d, P) - self.G(self.psi0 - h * d, P)) / (2.0 * h)


def armoniche(mp, f):
    """### **La potenza delle armoniche `m = 0 .. M_MAX` di un campo reale per nodo** *(per anelli attorno al baricentro dello stato fermo)*: ### **`m >= 1` conta `+m` e `-m`.**"""
    import _energia_del_legame as EL
    z = mp.z
    z["st"]["psi_h"][...] = mp.psi0
    rho = EL.densita(z["inc"], z["st"])[0]
    c = (rho @ z["pos"]) / float(rho.sum())
    dx, dy = z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1]
    r, th = np.hypot(dx, dy), np.arctan2(dy, dx)
    k = np.floor(r / ANELLO).astype(int)
    W = np.zeros(M_MAX + 1)
    for mm in range(M_MAX + 1):
        C = np.bincount(k, weights=f * np.cos(mm * th)) + 1j * np.bincount(k, weights=f * np.sin(mm * th))
        W[mm] = float(np.sum(np.abs(C) ** 2)) * (1.0 if mm == 0 else 2.0)
    return W / W.sum(), k


def per_nodo(mp, d):
    """### **`drho` e la fase per nodo:** ### **`2 Re` e `2 Im` di `sum conj(psi0) dpsi`** *(le `12` componenti del nodo)*."""
    q = np.sum(np.conj(mp.psi0.reshape(mp.n, 12)) * d.reshape(mp.n, 12), axis=1)
    return 2.0 * q.real, 2.0 * q.imag


def referto():
    from scipy.sparse.linalg import LinearOperator, eigs, ArpackNoConvergence
    import _congelato_lungo as CL
    import _dove_va_la_materia as DV
    print("=" * 130)
    print("IL MODO INSTABILE DELLO STATO FERMO DI S1 (Luca 08:24): L %d, s 0.3, N 1e6; G = e^{i mu s} T, il congelato vero; Arnoldi su G^P" % L)
    print("=" * 130)
    print("  la configurazione: L %d P %d H_REL %g K_AUT %d NCV %d TOLL_ARNOLDI %g RIAVVII %d M_MAX %d ANELLO %g R_PROFILO %d T_CONTROLLO %d TOLL_LIN %g SEME %d"
          % (L, P, H_REL, K_AUT, NCV, TOLL_ARNOLDI, RIAVVII, M_MAX, ANELLO, R_PROFILO, T_CONTROLLO, TOLL_LIN, SEME))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (a) radiale (m = 0) in A: VK applicato male; (b) m >= 1 in A: un'instabilita' che il criterio radiale non vede; (c) peso in B o nelle piatte; (d) altro")
    print("-" * 130)
    mp = Mappa()
    S = mp.SFM.S
    esito("DEVE PASSARE: lo stato fermo sul disco = quello della ricerca (sha1)", mp.sha_ok, "")
    r1 = float(np.linalg.norm(mp.G(mp.psi0, 1) - mp.psi0) / np.linalg.norm(mp.psi0))
    esito("DEVE PASSARE: il residuo dello stato fermo |G psi0 - psi0| / |psi0| < 1e-9", r1 < 1e-9, "%.3e; mu %+.9f" % (r1, mp.mu))
    rng = np.random.default_rng(SEME)
    v = rng.standard_normal(2 * mp.m)
    j1, j2 = mp.jv(v, H_REL), mp.jv(v, 2.0 * H_REL)
    dl = float(np.linalg.norm(j1 - j2) / np.linalg.norm(j1))
    esito("DEVE PASSARE: J lineare (h e 2 h) entro %g su un vettore a caso" % TOLL_LIN, dl < TOLL_LIN, "%.1e; |J v|/|v| %.4f" % (dl, np.linalg.norm(j1) / np.linalg.norm(v)))
    vf = mp.a_v(1j * mp.psi0)
    rf = float(np.linalg.norm(mp.jv(vf) - vf) / np.linalg.norm(vf))
    esito("DEVE PASSARE: la fase: |J (i psi0) - i psi0| / |psi0| < 1e-6 (l'autovalore 1, esatto)", rf < 1e-6, "%.2e" % rf)
    sh = np.roll(mp.psi0.reshape(L, L, 12), 1, axis=0) - np.roll(mp.psi0.reshape(L, L, 12), -1, axis=0)
    vt = mp.a_v(0.5 * sh.reshape(mp.forma))
    rt = float(np.linalg.norm(mp.jv(vt) - vt) / np.linalg.norm(vt))
    print("  la traslazione lungo A1 (la derivata per differenze sul reticolo, approssimata): |J d - d| / |d| = %.3e (dopo %d tick)" % (rt, P))
    print("-" * 130)
    print("### LO SPETTRO (Arnoldi su G^%d, modulo massimo)" % P)
    op = LinearOperator((2 * mp.m, 2 * mp.m), matvec=mp.jv, dtype=float)
    s0 = time.time()
    c0 = mp.conti
    try:
        lam, W = eigs(op, k=K_AUT, which="LM", ncv=NCV, tol=TOLL_ARNOLDI, maxiter=RIAVVII, v0=rng.standard_normal(2 * mp.m))
        conv = True
    except ArpackNoConvergence as e:
        lam, W = e.eigenvalues, e.eigenvectors
        conv = False
    print("  Arnoldi: %s; %d autovalori; %d tick; %.0f s" % ("converge" if conv else "NON converge (gli autovalori convergiti)", len(lam), mp.conti - c0, time.time() - s0))
    esito("DEVE PASSARE: Arnoldi converge", conv, "")
    o = np.argsort(-np.abs(lam))
    lam, W = lam[o], W[:, o]
    for i, l in enumerate(lam):
        lt = abs(l) ** (1.0 / P)
        print("  %d: lambda(G^%d) %+.6f %+.6fi, |lambda| %.6f; per tick |lambda| %.6f, il tasso ln|lambda|/s %+.5f per unita' di tempo; la fase per %d tick %+.5f"
              % (i, P, l.real, l.imag, abs(l), lt, math.log(lt) / S, P, math.atan2(l.imag, l.real)))
    instabili = [i for i in range(len(lam)) if abs(lam[i]) > 1.0]
    print("  i modi con |lambda| > 1: %s" % instabili)
    print("-" * 130)
    A = DV.matrice(mp.z, mp.phi0, DV.AMP)
    _ph, Z = DV.autovettori(A)
    basi = []
    primo = []
    for i in instabili[:4]:
        print("### LA FORMA DEL MODO %d (tasso %+.5f)" % (i, math.log(abs(lam[i]) ** (1.0 / P)) / S))
        parti = [W[:, i].real, W[:, i].imag]
        Wd = np.zeros(M_MAX + 1)
        Wf = np.zeros(M_MAX + 1)
        prof = np.zeros(R_PROFILO + 1)
        bande = np.zeros(4)
        for x in parti:
            if float(np.linalg.norm(x)) == 0.0:
                continue
            basi.append(x)
            if i == instabili[0]:
                primo.append(x)
            d = mp.a_psi(x)
            dr, df = per_nodo(mp, d)
            wd, kk = armoniche(mp, dr)
            wf, _k = armoniche(mp, df)
            pe = float(np.sum(np.abs(d) ** 2))
            Wd += wd * pe
            Wf += wf * pe
            pr = np.bincount(kk, weights=np.sum(np.abs(d.reshape(mp.n, 12)) ** 2, axis=1))
            prof[:min(len(pr), R_PROFILO + 1)] += pr[:R_PROFILO + 1]
            Pk = DV.pesi(d.reshape(mp.n, 12), np.ones(mp.n), Z, L)
            for g, (_nome, idx) in enumerate(DV.GRUPPI):
                bande[g] += float(Pk[:, :, list(idx)].sum())
        Wd /= Wd.sum()
        Wf /= Wf.sum()
        print("  le armoniche angolari di drho (frazioni, m = 0 .. %d): %s" % (M_MAX, " ".join("m%d %.4f" % (mm, Wd[mm]) for mm in range(M_MAX + 1))))
        print("  le armoniche angolari della fase:                    %s" % " ".join("m%d %.4f" % (mm, Wf[mm]) for mm in range(M_MAX + 1)))
        print("  le bande (frazioni di |dpsi|^2): %s" % "  ".join("%s %.5f" % (DV.GRUPPI[g][0], bande[g] / bande.sum()) for g in range(4)))
        prof /= prof.sum()
        print("  il profilo radiale di |dpsi|^2 (frazioni per anello, r 0..%d): %s" % (R_PROFILO, " ".join("%.4f" % x for x in prof)))
    print("-" * 130)
    print("### IL CONTROLLO INDIPENDENTE: %d tick dallo stato fermo" % T_CONTROLLO)
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    psi = mp.psi0.copy()
    for _t in range(T_CONTROLLO):
        psi = mp.SFM.tick(mp.z, mp.phi0, psi)
    rifs = json.loads(io.open(os.path.join(mp.SFM.PUNTI, "corsa_L%d_00000.jsonl" % L), encoding="utf-8").read())
    w_in, w0 = rifs["w_in"], rifs["w0"]
    mp.z["st"]["psi_h"][...] = psi
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        pt = CL.punto(mp.z, T_CONTROLLO, w_in, w0)
    rif = [p for p in rifs["punti"] if p["t"] == T_CONTROLLO][0]
    esito("DEVE PASSARE: il punto del tick %d = quello della corsa di 26300537, AL BIT" % T_CONTROLLO, all(pt[k] == rif[k] for k in ("w", "f_win", "f_3w0", "picco", "M")), "")
    D = mp.a_v(np.exp(1j * mp.mu * S * T_CONTROLLO) * psi - mp.psi0)
    nd = float(np.linalg.norm(D))
    print("  |D| / |psi0| = %.3e" % (nd / float(np.linalg.norm(mp.psi0))))
    if basi:
        Q, _r = np.linalg.qr(np.array(basi).T)
        ov = float(np.linalg.norm(Q.T @ D) ** 2) / nd ** 2
        q1, _r = np.linalg.qr(np.array(primo).T)
        o1 = float(np.linalg.norm(q1.T @ D) ** 2) / nd ** 2
        print("  la sovrapposizione |P D|^2 / |D|^2: col modo di tasso piu' grande %.5f; coi modi instabili trovati (%d vettori reali) %.5f" % (o1, len(basi), ov))
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
