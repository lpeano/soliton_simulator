# -*- coding: utf-8 -*-
r"""**DOVE VA LA MATERIA CHE IL CUORE PERDE** *(le risposte di Luca delle `20:52` del `2026-10-28`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-28_dove_va_la_materia.md`)*: ### **nessuna corsa: gli stati salvati.**
### **La materia sul toro, in impulso, proiettata sugli autovettori del tick LIBERO** *(il congelato con `S1` a ampiezza `1e-6`: il legame spento; il vuoto fermo)*;
### **i pesi per BANDA, per VALLE, per `|k - K|`; lo stato intero, il CUORE e l'ANELLO** *(finestre lisce)*.

> ### **Gli stati:** `db/congelato_lungo/` *(`_congelato_lungo.py --pezzo`)*, `db/diagnosi_s4/` *(`_diagnosi_s4.py --pezzo`)*: ### **il dato e' il comando.**

    python csv/_dove_va_la_materia.py --referto > doc/referti_l2/dove_va_la_materia.txt
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

# ### gli stati: (etichetta, forma, s, N, L)
STATI = (("S1_s0.30_L81", "S1", 0.3, 1e6, 81), ("S1_s0.30_L120", "S1", 0.3, 1e6, 120),
         ("S4_s0.30_L81", "S4", 0.3, 1e7, 81), ("S4_s0.30_L120", "S4", 0.3, 1e7, 120), ("S4_s0.99_L81", "S4", 0.99, 1e7, 81))
AMP = 1e-6
SPESSORE = 1.0                 # ### lo spessore delle finestre spaziali: un arco (la grana)
GRUPPI = (("Ppi", (0, 1, 2, 3)), ("A", (4, 5)), ("P0", (6, 7, 8, 9)), ("B", (10, 11)))
N_RADIALE = 12                 # ### gli anelli in |k - K| stampati
TOLL_UNIT = 1e-12
TOLL_LIN = 1e-9
TOLL_FASI = 1e-9
TOLL_PARSEVAL = 1e-12
TOLL_TICK = 1e-9
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


def carica(et, forma, s, N, L):
    """### **`(z, phi0, rec, psi iniziale, psi finale)`** *(`n x 12`)*: ### **l'iniziale ricostruito, il finale dal disco col controllo dello `sha1`.**"""
    import _congelato_lungo as CL
    import _diagnosi_s4 as D
    rec, z = D.iniziale(forma, s, L)
    phi0 = z["st"]["phi_h"].copy()
    n = z["inc"].n
    p0 = z["st"]["psi_h"].reshape(n, 12).copy()
    if forma == "S1":
        f = os.path.join(CL.STATI, CL.nome(L, "uniforme") + ".npz")
        righe, _p = CL.serie(L, "uniforme")
    else:
        c = [x for x in D.CORSE if D.nome(x) == et][0]
        f = os.path.join(D.STATI, D.nome(c) + ".npz")
        righe, _p = D.serie(c)
    dati = np.load(f)
    ok = CL.sha(dati["psi_h"]) == righe[-1]["sha_fine"] and int(dati["t"]) == righe[-1]["t1"]
    p1 = dati["psi_h"].reshape(n, 12).copy()
    return z, phi0, rec, p0, p1, ok, int(dati["t"]), righe[0]["w_in"], righe[0]["w0"]


def un_tick(z, phi0, psi):
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    n = z["inc"].n
    z["st"]["psi_h"][...] = psi.reshape(z["st"]["psi_h"].shape)
    z["st"]["phi_h"][...] = phi0
    with SF.forma("S1"), BE.conv(DC.ZERO):
        DC.tick_congelato(z, phi0, VC.VUOTO)
    return z["st"]["psi_h"].reshape(n, 12).copy()


def matrice(z, phi0, amp):
    """### **`A(k)` `(L, L, 12, 12)`:** ### **le risposte a un impulso di ampiezza `amp` nel nodo `0`, componente per componente, `fft2`.**"""
    L = z["L"]
    n = z["inc"].n
    A = np.empty((L, L, 12, 12), dtype=complex)
    for c in range(12):
        p = np.zeros((n, 12), dtype=complex)
        p[0, c] = amp
        R = un_tick(z, phi0, p) / amp
        A[:, :, :, c] = np.fft.fft2(R.reshape(L, L, 12), axes=(0, 1))
    return A


def autovettori(A):
    """### **Schur a ogni `k`** *(`A` unitaria: `T` diagonale, `Z` ortonormale)*, ### **ordinati per fase `-arg`:** ### **`(fasi, Z)`.**"""
    from scipy.linalg import schur
    L = A.shape[0]
    ph = np.empty((L, L, 12))
    Z = np.empty((L, L, 12, 12), dtype=complex)
    for i in range(L):
        for j in range(L):
            T, V = schur(A[i, j], output="complex")
            f = -np.angle(np.diag(T))
            o = np.argsort(f)
            ph[i, j] = f[o]
            Z[i, j] = V[:, o]
    return ph, Z


def geometria(L):
    """### **Le valli** *(il punto piu' vicino fra `Gamma`, `K`, `K'`, con le immagini)* ### **e `|k - K|`.**"""
    import _solitoni_triangoli as STR
    Areal = np.array([STR.A1, STR.A2])
    B = 2.0 * np.pi * np.linalg.inv(Areal).T
    k1, k2 = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    kv = (k1[..., None] * B[0] + k2[..., None] * B[1]) / L
    punti = {"Gamma": np.zeros(2), "K": (B[0] + B[1]) / 3.0, "K'": 2.0 * (B[0] + B[1]) / 3.0}
    dist = {}
    for nome_, P in punti.items():
        d = np.full((L, L), np.inf)
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                Q = P + a * B[0] + b * B[1]
                d = np.minimum(d, np.hypot(kv[..., 0] - Q[0], kv[..., 1] - Q[1]))
        dist[nome_] = d
    nomi = ("Gamma", "K", "K'")
    valle = np.argmin(np.stack([dist[x] for x in nomi]), axis=0)
    return valle, nomi, dist["K"], float(np.linalg.norm(B[0])) / L


def finestre(z, rho, w_in, w0):
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    r = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    wc = 1.0 / (1.0 + np.exp(np.clip((r - w_in) / SPESSORE, -700, 700)))
    w3 = 1.0 / (1.0 + np.exp(np.clip((r - 3.0 * w0) / SPESSORE, -700, 700)))
    return {"intero": np.ones_like(r), "cuore": wc, "anello": w3 - wc}


def pesi(psi, W, Z, L):
    """### **I pesi `|<v_j(k)|psi_k>|^2`** *(`L x L x 12`)* ### **della materia nella finestra `W`, in frazione di `|psi|^2` dello stato INTERO.**"""
    f = np.fft.fft2((W[:, None] * psi).reshape(L, L, 12), axes=(0, 1))
    c = np.einsum("abji,abj->abi", Z.conj(), f)
    return np.abs(c) ** 2 / (L * L)


def riassunto(P, tot, valle, nomi, dK, dk, L):
    out = {}
    for g, idx in GRUPPI:
        out[g] = float(P[:, :, list(idx)].sum()) / tot
    pa = P[:, :, 4] + P[:, :, 5]
    for v, nv in enumerate(nomi):
        out["A@" + nv] = float(pa[valle == v].sum()) / tot
    kK = (L // 3, L // 3)
    kKp = (2 * L // 3, 2 * L // 3)
    fuori = np.ones((L, L), dtype=bool)
    fuori[kK] = False
    fuori[kKp] = False
    fuori[0, 0] = False
    out["A-basso"] = float(P[:, :, 4][fuori].sum()) / tot
    out["A-alto"] = float(P[:, :, 5][fuori].sum()) / tot
    out["A@puntoK"] = float(pa[kK]) / tot
    out["tutto@Gamma"] = float(P[0, 0].sum()) / tot
    mK = valle == nomi.index("K")
    b = np.floor(dK / dk + 0.5).astype(int)
    rad = [float(pa[mK & (b == i)].sum()) / tot for i in range(N_RADIALE)]
    out["radiale"] = rad
    out["dk_medio"] = float((pa[mK] * dK[mK]).sum() / max(pa[mK].sum(), 1e-300))
    return out


def stampa(et, quale, fin, r):
    print("  %-14s %-7s %-7s: A %.5f  B %.5f  P0 %.5f  Ppi %.5f | A@K %.5f  A@K' %.5f  A@Gamma %.5f | A-basso %.5f  A-alto %.5f  A@puntoK %.5f  tutto@Gamma %.2e | |k-K| medio in A@K %.5f"
          % (et, quale, fin, r["A"], r["B"], r["P0"], r["Ppi"], r["A@K"], r["A@K'"], r["A@Gamma"], r["A-basso"], r["A-alto"], r["A@puntoK"], r["tutto@Gamma"], r["dk_medio"]))


def referto():
    import _diagnosi_s4 as D
    import _triangoli_forza as TF
    print("=" * 130)
    print("DOVE VA LA MATERIA CHE IL CUORE PERDE (Luca 20:52): gli stati salvati sugli autovettori del tick libero; nessuna corsa nuova")
    print("=" * 130)
    print("  la configurazione: STATI %s AMP %g SPESSORE %g GRUPPI %s N_RADIALE %d TOLL_UNIT %g TOLL_LIN %g TOLL_FASI %g TOLL_PARSEVAL %g TOLL_TICK %g"
          % ([x[0] for x in STATI], AMP, SPESSORE, GRUPPI, N_RADIALE, TOLL_UNIT, TOLL_LIN, TOLL_FASI, TOLL_PARSEVAL, TOLL_TICK))
    print("  il riferimento: il tick congelato (VC.VUOTO saltati, phi rimesso) con la forma S1 a ampiezza %g (il legame spento), sulla scena di ogni stato; gli stati S1 a s 0.075 NON esistono" % AMP)
    print("  LE LETTURE, SCRITTE PRIMA: (i) la materia persa in B o nelle piatte; (ii) nella valle K'; (iii) in A, valle K, a |k - K| piu' grande; (iv) altro; S1 contro S4 a s 0.3")
    print("  le pesature: frazioni di |psi|^2 dello stato INTERO (cuore + anello + fuori = 1); A-basso / A-alto fuori dai punti K, K', Gamma (li' degeneri)")
    tabella = {}
    primo = True
    cache = {}
    for et, forma, s, N, L in STATI:
        print("-" * 130)
        with D.configura(forma, s, N):
            z, phi0, rec, p0, p1, ok, t, w_in, w0 = carica(et, forma, s, N, L)
            esito("DEVE PASSARE: %s, lo stato finale (tick %d) = sha_fine dell'ultimo pezzo" % (et, t), ok, "")
            chiave = (L, s)
            if chiave not in cache:
                A = matrice(z, phi0, AMP)
                U = np.einsum("abji,abjk->abik", A.conj(), A)
                du = float(np.abs(U - np.eye(12)).max())
                esito("DEVE PASSARE: L %d, s %g: A(k) unitaria entro %g" % (L, s, TOLL_UNIT), du < TOLL_UNIT, "%.1e" % du)
                if primo:
                    A2 = matrice(z, phi0, 2.0 * AMP)
                    dl = float(np.abs(A2 - A).max())
                    esito("DEVE PASSARE: L %d, s %g: A(k) lineare (ampiezza %g e %g) entro %g" % (L, s, AMP, 2 * AMP, TOLL_LIN), dl < TOLL_LIN, "%.1e" % dl)
                ph, Z = autovettori(A)
                co = TF.coppia_K(0.0, s)
                kK = (L // 3, L // 3)
                df = max(abs(ph[kK][4] - co[0]["w"]), abs(ph[kK][5] - co[0]["w"]), abs(ph[kK][10] - co[1]["w"]), abs(ph[kK][11] - co[1]["w"]))
                esito("DEVE PASSARE: L %d, s %g: le fasi a K (indici 4, 5, 10, 11) = coppia_K entro %g" % (L, s, TOLL_FASI), df < TOLL_FASI,
                      "%.1e (%.6f, %.6f)" % (df, co[0]["w"], co[1]["w"]))
                dp = max(float(np.abs(ph[:, :, :4] + math.pi * s).max()), float(np.abs(ph[:, :, 6:10]).max()))
                esito("DEVE PASSARE: L %d, s %g: le piatte (indici 0-3 a -pi s, 6-9 a 0) piatte entro %g" % (L, s, TOLL_FASI), dp < TOLL_FASI, "%.1e" % dp)
                Q = co[0]["Q"][:, 0]
                PA = Z[kK][:, 4:6]
                dq = abs(1.0 - float(np.linalg.norm(PA.conj().T @ Q) ** 2))
                esito("DEVE PASSARE: L %d, s %g: il Q dello stato iniziale sta nel sottospazio A a K entro %g" % (L, s, TOLL_PARSEVAL), dq < TOLL_PARSEVAL, "%.1e" % dq)
                cache[chiave] = (A, ph, Z)
            A, ph, Z = cache[chiave]
            valle, nomi, dK, dk = geometria(L)
            if primo:
                n = z["inc"].n
                pp = p0 * (AMP / float(np.abs(p0).max()))
                dopo = un_tick(z, phi0, pp)
                f = np.fft.fft2(pp.reshape(L, L, 12), axes=(0, 1))
                prev = np.fft.ifft2(np.einsum("abij,abj->abi", A, f), axes=(0, 1)).reshape(n, 12)
                dt = float(np.abs(prev - dopo).max() / np.abs(dopo).max())
                esito("DEVE PASSARE: un tick dello stato iniziale scalato (max %g) = A(k) applicata entro %g" % (AMP, TOLL_TICK), dt < TOLL_TICK, "%.1e" % dt)
                g = np.abs(p0 @ np.conj(co[0]["Q"][:, 0]))
                fase = np.exp(2j * np.pi * (z["m1"] + z["m2"]) / 3.0)
                pb = (g * fase)[:, None] * co[1]["Q"][:, 0][None, :]
                Pb = pesi(pb, np.ones(n), Z, L)
                wa, wb = float(Pb[:, :, 4:6].sum()), float(Pb[:, :, 10:12].sum())
                esito("DEVE PASSARE: uno stato col Q di +%.3f sta in B piu' che in A" % co[1]["w"], wb > wa, "B %.5f, A %.5f" % (wb / Pb.sum(), wa / Pb.sum()))
                primo = False
            for quale, psi in (("inizio", p0), ("fine", p1)):
                rho = np.zeros(z["inc"].n)
                rho += np.sum(np.abs(psi) ** 2, axis=1)
                tot = float(rho.sum())
                fin = finestre(z, rho, w_in, w0)
                somma = 0.0
                for nf in ("intero", "cuore", "anello"):
                    P = pesi(psi, fin[nf], Z, L)
                    if nf == "intero":
                        dpar = abs(float(P.sum()) / tot - 1.0)
                        esito("DEVE PASSARE: %s %s: i pesi sommano a |psi|^2 entro %g" % (et, quale, TOLL_PARSEVAL), dpar < TOLL_PARSEVAL, "%.1e" % dpar)
                    r = riassunto(P, tot, valle, nomi, dK, dk, L)
                    tabella[(et, quale, nf)] = r
                    stampa(et, quale, nf, r)
    print("-" * 130)
    a81, a120 = tabella[("S1_s0.30_L81", "inizio", "intero")], tabella[("S1_s0.30_L120", "inizio", "intero")]
    print("### LA DIVISIONE A-basso / A-alto (per indice di fase) dello STESSO stato iniziale S1 a L 81 e L 120: %.5f / %.5f contro %.5f / %.5f;"
          % (a81["A-basso"], a81["A-alto"], a120["A-basso"], a120["A-alto"]))
    print("    se diverse, la divisione per indice dipende dalla griglia in k e NON si legge: si legge il gruppo A intero")
    print("### LO SPETTRO RADIALE di A nella valle K, per anelli di |k - K| larghi un passo della griglia (frazioni di |psi|^2 dello stato intero)")
    for et, _f, _s, _N, _L in STATI:
        for quale in ("inizio", "fine"):
            for nf in ("cuore", "anello"):
                r = tabella[(et, quale, nf)]
                print("  %-14s %-7s %-7s: %s" % (et, quale, nf, " ".join("%.4f" % v for v in r["radiale"])))
    print("-" * 130)
    print("### LA DIFFERENZA fine - inizio (frazioni di |psi|^2 dello stato intero)")
    for et, _f, _s, _N, _L in STATI:
        for nf in ("intero", "cuore", "anello"):
            a, b = tabella[(et, "inizio", nf)], tabella[(et, "fine", nf)]
            print("  %-14s %-7s: A %+.5f  B %+.5f  P0 %+.5f  Ppi %+.5f | A@K %+.5f  A@K' %+.5f  A@Gamma %+.5f | A-basso %+.5f  A-alto %+.5f | |k-K| medio %+.5f"
                  % (et, nf, b["A"] - a["A"], b["B"] - a["B"], b["P0"] - a["P0"], b["Ppi"] - a["Ppi"], b["A@K"] - a["A@K"], b["A@K'"] - a["A@K'"], b["A@Gamma"] - a["A@Gamma"],
                     b["A-basso"] - a["A-basso"], b["A-alto"] - a["A-alto"], b["dk_medio"] - a["dk_medio"]))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    import _deriva_congelato as DC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        if argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
