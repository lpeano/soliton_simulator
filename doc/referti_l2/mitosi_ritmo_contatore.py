# -*- coding: utf-8 -*-
r"""**IL RITMO DEL CONTATORE NEL TEMPO SUI PRIMI `20` ARCHI, E LA PROIEZIONE DEL PRIMO SCATTO** *(la nota di Luca `2026-11-21` `13:57`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `16.4`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_ritmo_contatore.py --base E:\soliton_simulator\controllo\mitosi_rami --fino 40000 > doc/referti_l2/mitosi_ritmo_contatore.txt

**E' la v2 di `mitosi_proiezione_scatto.py`** *(`fb65af6c`, gia' usato: non si riscrive)*: in piu' **il ritmo per tratti di `2500` tick** *(la misura chiesta: il raddrizzarsi del tempo attorno al mattone)*, **le proiezioni col calo LINEARE ed ESPONENZIALE del ritmo**, **il `tau` CRITICO**, e il limite `--fino` come argomento.
**I primi `20` archi:** i `20` col `|Theta|` maggiore **all'ultimo stato del tronco** *(se c'e' `scatto.json`: lo stato prima della prima nascita)*. **I tratti:** i confini ai multipli di `2500` dal primo stato salvato all'ultimo, piu' l'ultimo stato; **il ritmo** di un tratto = la differenza di `|Theta|` diviso i tick. **Su C2-EXT** *(dopo lo scatto, lo stesso grafo)* gli stessi archi; ### **NON su MITOSI** *(dopo una nascita gli indici cambiano)*.
**Le proiezioni**, per arco, dai suoi ultimi `4` tratti *(il ritmo al centro del tratto)*: **LINEARE** *(`r(k) = r0 + s (k - kU)`: il guadagno `r0 D + s D^2 / 2`; **mai** se `r0^2 / (2 |s|)` non basta)*; **ESPONENZIALE** *(`r(k) = r0 exp(-(k - kU) / tau)`, `tau` dal fit di `log r`: il guadagno `r0 tau (1 - exp(-D / tau))`; **mai** se `r0 tau` non basta)*; **il `tau` CRITICO** = quanto manca a `2 pi` diviso `r0` *(lo scatto arriva, nel modello esponenziale, se e solo se `tau` e' maggiore)*. `r0` = il ritmo dei fit all'ultimo stato `kU`.
### **SONO PROIEZIONI, non misure.**
"""
import argparse
import glob
import hashlib
import json
import math
import os
import sys

import numpy as np

_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "csv")
if _CSV not in sys.path:
    sys.path.insert(0, _CSV)
Q = 2.0 * math.pi
TRATTO = 2500
N_ARCHI = 20
N_FIT = 4


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def theta(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        return d["theta_a"].copy()


def stati(d):
    """### solo gli stati col loro `.sha1` *(la corsa lo scrive DOPO lo stato: uno stato senza e' a meta' scrittura)*."""
    return {int(os.path.basename(f)[6:11]): f for f in glob.glob(os.path.join(d, "stato_*.npz")) if os.path.exists(f + ".sha1")}


def confini(ks):
    k0, kU = min(ks), max(ks)
    c = [k0] + [k for k in range((k0 // TRATTO + 1) * TRATTO, kU, TRATTO) if k in ks] + [kU]
    return sorted(set(c))


def ritmi(F, cc, archi):
    T = {k: np.abs(theta(F[k])[archi]) for k in cc}
    R = np.array([(T[cc[j + 1]] - T[cc[j]]) / (cc[j + 1] - cc[j]) for j in range(len(cc) - 1)])
    mid = np.array([(cc[j] + cc[j + 1]) / 2.0 for j in range(len(cc) - 1)])
    return T, R, mid


def proietta(th, r, mid, kU):
    """### `(k lineare, k esponenziale, tau, tau critico, r0)` per un arco: dai suoi ultimi `N_FIT` tratti."""
    rem = Q - th
    x, y = mid[-N_FIT:] - kU, r[-N_FIT:]
    s, r0 = np.polyfit(x, y, 1)
    if s >= 0:
        kl = kU + rem / r0 if r0 > 0 else math.inf
    else:
        disc = r0 * r0 + 2.0 * s * rem
        kl = kU + (-r0 + math.sqrt(disc)) / s if disc >= 0 else math.inf
    if np.all(y > 0):
        b, a = np.polyfit(x, np.log(y), 1)
        r0e = math.exp(a)
        tau = -1.0 / b if b < 0 else math.inf
        if math.isinf(tau):
            ke = kU + rem / r0e
        else:
            ke = kU - tau * math.log(1.0 - rem / (r0e * tau)) if rem < r0e * tau else math.inf
        tc = rem / r0e
    else:
        tau = ke = tc = r0e = math.nan
    return kl, ke, tau, tc, r0, r0e


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--fino", type=int, required=True)
    x = ap.parse_args(argv)
    dT = os.path.join(x.base, "TRONCO")
    F = stati(dT)
    sj = None
    if os.path.exists(os.path.join(dT, "scatto.json")):
        with open(os.path.join(dT, "scatto.json"), encoding="utf-8") as fh:
            sj = json.load(fh)
    kU = max(F)
    fU = F[kU] if sj is None else sj["file"]
    U = theta(fU)
    archi = np.argsort(-np.abs(U))[:N_ARCHI]
    print("=" * 130)
    print("IL RITMO DEL CONTATORE SUI PRIMI %d ARCHI, E LA PROIEZIONE DEL PRIMO SCATTO (Luca 2026-11-21 13:57); il limite --fino %d" % (N_ARCHI, x.fino))
    print("=" * 130)
    print("### il tronco: %d stati, da k %d a k %d; lo scatto: %s" % (len(F), min(F), kU, "a k %d (%s)" % (sj["k"], os.path.basename(sj["file"])) if sj else "NESSUNO"))
    print("### i primi %d archi (|Theta| maggiore a %s), la soglia %.4f:" % (N_ARCHI, os.path.basename(fU), Q))
    print("    " + ", ".join("%d %.4f" % (a, abs(U[a])) for a in archi))
    cc = confini(F)
    T, R, mid = ritmi(F, cc, archi)
    print("### IL RITMO DI |Theta| PER TRATTO (1e-4 per tick), il tronco:")
    print("    il tratto      " + "  ".join("%11s" % ("%d-%d" % (cc[j], cc[j + 1])) for j in range(len(cc) - 1)))
    for i, a in enumerate(archi):
        print("    l'arco %6d " % a + "  ".join("%11.4f" % (R[j, i] * 1e4) for j in range(len(cc) - 1)))
    print("    la media      " + "  ".join("%11.4f" % (R[j].mean() * 1e4) for j in range(len(cc) - 1)))
    print("    il ritmo dell'ultimo tratto sul primo: la media dei %d %.4f" % (N_ARCHI, float(np.mean(R[-1] / R[0]))))
    if sj is None:
        print("### LE PROIEZIONI (dagli ultimi %d tratti di ogni arco; r0 al k %d):" % (N_FIT, kU))
        print("    l'arco    |Theta|   r0 lin (1e-4)  k LINEARE   r0 esp (1e-4)   tau      tau CRITICO   k ESPONENZIALE")
        P = []
        for i, a in enumerate(archi):
            kl, ke, tau, tc, r0, r0e = proietta(T[kU][i], R[:, i], mid, kU)
            P.append((kl, ke, tau, tc))
            print("    %6d   %.4f    %9.4f     %9s    %9.4f    %9.0f    %9.0f      %9s" % (
                a, T[kU][i], r0 * 1e4, "mai" if math.isinf(kl) else "%.0f" % kl, r0e * 1e4, tau, tc, "mai" if math.isinf(ke) else "%.0f" % ke))
        kl = min(p[0] for p in P)
        ke = min(p[1] for p in P)
        print("### IL PRIMO dei %d: LINEARE a k %s; ESPONENZIALE a k %s; entro k %d: %d col lineare, %d con l'esponenziale" % (
            N_ARCHI, "mai" if math.isinf(kl) else "%.0f" % kl, "mai" if math.isinf(ke) else "%.0f" % ke, x.fino,
            sum(1 for p in P if p[0] <= x.fino), sum(1 for p in P if p[1] <= x.fino)))
        k0 = cc[-2]
        v = (np.abs(U) - np.abs(theta(F[k0]))) / (kU - k0)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(v > 0, (Q - np.abs(U)) / v, np.inf)
        i = int(np.argmin(t))
        print("### TUTTI GLI ARCHI, il ritmo costante dell'ultimo tratto (k %d-%d): il primo a 2 pi l'arco %d a k %.0f; entro k %d: %d archi" % (
            k0, kU, i, kU + t[i], x.fino, int(np.sum(kU + t <= x.fino))))
    dC = os.path.join(x.base, "C2EXT")
    if sj is not None and os.path.isdir(dC) and stati(dC):
        FC = stati(dC)
        FC[int(sj["k"])] = sj["file"]
        cC = confini(FC)
        _, RC, _ = ritmi(FC, cC, archi)
        print("### IL RITMO SU C2-EXT (gli stessi archi, dallo scatto; 1e-4 per tick):")
        print("    il tratto      " + "  ".join("%11s" % ("%d-%d" % (cC[j], cC[j + 1])) for j in range(len(cC) - 1)))
        print("    la media      " + "  ".join("%11.4f" % (RC[j].mean() * 1e4) for j in range(len(cC) - 1)))
    print("### SONO PROIEZIONI, non misure; MITOSI non c'e' (gli indici degli archi cambiano dopo una nascita).")
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
