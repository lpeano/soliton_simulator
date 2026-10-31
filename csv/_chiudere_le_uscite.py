# -*- coding: utf-8 -*-
r"""**CHIUDERE LE USCITE** *(SULLA CARTA, DAL CODICE E SUL CAMMINO LIBERO; il mandato di Luca delle `00:38` del `2026-10-31`, con le aggiunte delle `00:44` e `00:50`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-31_chiudere_le_uscite.md`)*: ### **conti sul tick libero a `eps 0.5` (il caso principale) e a `eps 0`; nessuna corsa di solitoni.**
### **(1)-(3) le uscite (n0), (n1), (n2), (n2-misto) per ogni `mu` in `[E0, E0 + g]`, sui punti della banda e sul piano dei pesi; (4) le cariche; (5) le piatte che si muovono e la moneta.**

    python csv/_chiudere_le_uscite.py > doc/referti_l2/chiudere_le_uscite.txt
"""
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

import _bande_piatte as BP                                     # noqa: E402

S = BP.S_MENU
OMEGA = 2.0 * math.pi / S       # ### le quasi-energie sono definite modulo 2 pi/s
EPS = (BP.EPS_TABELLA, 0.0)     # ### il caso principale per primo (Luca 00:38)
W = (0.05, 0.2)                 # ### la larghezza W di 99b679bc, i due lati
GRUPPI = (("Ppi", BP.PPI), ("A", BP.A_), ("P0", BP.P0), ("B", BP.B_))
PIATTE = ("P0", "Ppi")
DISPERSIVE = ("A", "B")
G_LISTA = (0.25, 0.5, 1.0, 1.5, 2.0)
PESI = tuple(0.25 * k for k in range(1, 9))   # ### a_n/pi e b_a/pi in 0.25 .. 2
TOLL_RICOMPOSTO = 1e-10
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


# ====================================================================== IL TICK LIBERO
class Libero:
    """### **I generatori e la moneta a un `eps`, dai mezzi pezzi di `_bande_piatte`; il tick coi pesi `(a, b)`.**"""

    def __init__(self, eps):
        P, T, _A = BP.pezzi(S, eps)
        self.eps = eps
        self.X_G, self.R_S = BP.generatori(P, S)
        self.M = P[BP.J_MONETA]
        self.T_oggi = T
        self.L = T.shape[0]

    def tick(self, a, b):
        return BP.ricomposto(self.X_G, self.R_S, S, a, b, self.M)

    def E(self, a, b):
        return BP.fasi(self.tick(a, b), S)


def gruppi_di(E):
    return {g: (float(E[..., list(i)].min()), float(E[..., list(i)].max())) for g, i in GRUPPI}


def cartesiano(L):
    import _solitoni_triangoli as STR
    A = np.array([STR.A1, STR.A2])
    B = 2.0 * math.pi * np.linalg.inv(A).T
    return A, B


def gradiente(Eb, L):
    """### **`|grad_k E|` sul reticolo** *(differenze centrate negli indici, convertite in coordinate cartesiane)*."""
    _A, B = cartesiano(L)
    di = (np.roll(Eb, -1, axis=0) - np.roll(Eb, 1, axis=0)) / 2.0
    dj = (np.roll(Eb, -1, axis=1) - np.roll(Eb, 1, axis=1)) / 2.0
    Minv = np.linalg.inv(np.array([B[0], B[1]]) / L)
    gx = Minv[0, 0] * di + Minv[0, 1] * dj
    gy = Minv[1, 0] * di + Minv[1, 1] * dj
    return np.hypot(gx, gy)


# ====================================================================== LE CONDIZIONI
def distanza(iv, jv):
    """### **La distanza fra due intervalli, modulo `OMEGA`** *(negativa = si sovrappongono, di quanto)*."""
    best = None
    for k in (-1, 0, 1):
        a0, a1 = iv[0] + k * OMEGA, iv[1] + k * OMEGA
        d = max(jv[0] - a1, a0 - jv[1])
        best = d if best is None else min(best, d)
    return best


def uscite(E0, g, sp, mu=None):
    """### **Per ogni `mu` in `[E0, E0 + g]`** *(o il solo `mu` dato)* **e `alpha` in `[0, g]`:** ### **la distanza di ogni condizione dall'essere vera** *(< 0: APERTA)*."""
    m0, m1 = (E0, E0 + g) if mu is None else (mu, mu)
    out = {}
    lo = m0 + 1e-9 if mu is None else m0
    for c in DISPERSIVE:
        out["(n0) mu in %s" % c] = distanza((lo, m1), sp[c])
    for p in PIATTE:
        F = sp[p]
        out["(n1) %s" % p] = distanza((m0 - F[1], m1 - F[0]), (0.0, g))
        for c in DISPERSIVE:
            out["(n2-misto) %s + %s" % (p, c)] = distanza((2 * m0 - F[1] - g, 2 * m1 - F[0]), sp[c])
    for i, p in enumerate(PIATTE):
        for q in PIATTE[i:]:
            Fp, Fq = sp[p], sp[q]
            out["(n2) %s + %s" % (p, q)] = distanza((2 * m0 - Fp[1] - Fq[1], 2 * m1 - Fp[0] - Fq[0]), (0.0, 2 * g))
    return out


def margine(u, c):
    """### **Il margine minimo SENZA la `(n0)` della banda di `E0`** *(a distanza `0` per costruzione: `mu` parte dal suo bordo; la prima stampa di `cc6b28d9` la contava, ed era un difetto mio)*."""
    return min(d for k, d in u.items() if k != "(n0) mu in %s" % c)


def giudizio(d):
    if d < 0:
        return "APERTA (dentro di %.4f)" % -d
    if d <= W[0]:
        return "SUL BORDO (%.4f: entro W %.2f)" % (d, W[0])
    if d <= W[1]:
        return "chiusa di %.4f (entro W %.2f)" % (d, W[1])
    return "CHIUSA (%.4f)" % d


def punti_critici(E, L):
    """### **I punti della banda:** `Gamma`, `K`, `K'`, il quasi-`M` *(`(L//2, 0)`: `M` non e' sul reticolo dispari)*, ### **e il massimo e il minimo di ogni banda dispersiva.**"""
    K, Kp = BP.indici_K(L)
    simm = {"Gamma": (0, 0), "K": K, "K'": Kp, "M~": (L // 2, 0)}
    out = []
    for c, idx in GRUPPI:
        if c not in DISPERSIVE:
            continue
        for b in idx:
            Eb = E[..., b]
            for nome, ij in simm.items():
                out.append(("%s[%d] a %s" % (c, b, nome), float(Eb[ij]), c, b, ij))
            imax = np.unravel_index(np.argmax(Eb), Eb.shape)
            imin = np.unravel_index(np.argmin(Eb), Eb.shape)
            out.append(("%s[%d] il MASSIMO %s" % (c, b, tuple(int(x) for x in imax)), float(Eb[imax]), c, b, imax))
            out.append(("%s[%d] il MINIMO %s" % (c, b, tuple(int(x) for x in imin)), float(Eb[imin]), c, b, imin))
    return out


def curvatura(Eb, ij, L):
    i, j = ij
    return float(Eb[(i + 1) % L, j] + Eb[(i - 1) % L, j] - 2.0 * Eb[i, j])


# ====================================================================== (1), (2) LO SPETTRO DI OGGI
def oggi(lib):
    L = lib.L
    E = lib.E(math.pi, math.pi)
    sp = gruppi_di(E)
    print("  --- eps %g, r 1 (a_n = b_a = pi), g 1: le bande %s" % (lib.eps, "  ".join("%s [%+.5f, %+.5f] (larga %.4f)" % (k, v[0], v[1], v[1] - v[0]) for k, v in sp.items())))
    if lib.eps == 0.0:
        u = uscite(None, 1.0, sp, mu=-0.56602)
        esito("DEVE PASSARE: eps 0, r 1, mu -0.56602: (n2) P0 + Ppi a 0.0096 fuori, come uscite.txt (entro 1e-3)", abs(u["(n2) P0 + Ppi"] - 0.0096) < 1e-3, "%.5f" % u["(n2) P0 + Ppi"])
        u = uscite(None, 0.5, gruppi_di(lib.E(math.pi, 0.6 * math.pi)), mu=-0.86850)
        esito("DEVE PASSARE: eps 0, (R) (a_n = pi, b_a = 0.6 pi, g 0.5), mu -0.86850: (n2-misto) P0 + A APERTA", u["(n2-misto) P0 + A"] < 0, "%.5f" % u["(n2-misto) P0 + A"])
    for nome, E0, c, b, ij in punti_critici(E, L):
        u = uscite(E0, 1.0, sp)
        aperte = [k for k, d in u.items() if d < 0]
        print("    %-30s E0 %+.5f (curvatura %+.4f): %s" % (nome, E0, curvatura(E[..., b], ij, L), ("APERTE: " + "; ".join(aperte)) if aperte else
              "TUTTE CHIUSE, il margine (senza la n0 della sua banda) %s -- %s" % (giudizio(margine(u, c)), "; ".join("%s %.4f" % (k, d) for k, d in u.items()))))
    return E, sp


# ====================================================================== (3) LA REGIONE
def regione(lib):
    L = lib.L
    print("  --- eps %g: il piano a_n/pi x b_a/pi (%s), g in %s; per ogni punto: il massimo e il minimo di A e di B come E0" % (lib.eps, PESI, G_LISTA))
    chiusi, sempre = [], {}
    s0 = time.time()
    for a in PESI:
        for b in PESI:
            E = lib.E(a * math.pi, b * math.pi)
            sp = gruppi_di(E)
            vA = float(gradiente(E[..., BP.A_[0]], L).max())
            for c, idx in GRUPPI:
                if c not in DISPERSIVE:
                    continue
                for bi in idx:
                    Eb = E[..., bi]
                    for chi, ij in (("max", np.unravel_index(np.argmax(Eb), Eb.shape)), ("min", np.unravel_index(np.argmin(Eb), Eb.shape))):
                        for g in G_LISTA:
                            u = uscite(float(Eb[ij]), g, sp)
                            ap = [k for k, d in u.items() if d < 0]
                            for k in ap:
                                sempre[k] = sempre.get(k, 0) + 1
                            sempre["_tot"] = sempre.get("_tot", 0) + 1
                            if not ap:
                                chiusi.append((a, b, g, "%s[%d] %s" % (c, bi, chi), float(Eb[ij]), curvatura(Eb, ij, L), vA, margine(u, c), tuple(int(x) for x in ij)))
    print("    %d spettri in %.0f s" % (len(PESI) ** 2, time.time() - s0))
    tot = sempre.pop("_tot")
    print("    quante volte ogni uscita e' APERTA, su %d casi (punto, E0, g): %s" % (tot, "; ".join("%s %d" % kv for kv in sorted(sempre.items(), key=lambda x: -x[1]))))
    if not chiusi:
        print("    ### LA REGIONE E' VUOTA a eps %g: nessun (pesi, g, E0) con tutte le uscite chiuse" % lib.eps)
    else:
        print("    ### %d casi con TUTTE le uscite chiuse a eps %g; per margine (senza la n0 della sua banda): oltre W %.2f %d, fra %.2f e %.2f %d, sotto %.2f %d"
              % (len(chiusi), lib.eps, W[1], sum(x[7] > W[1] for x in chiusi), W[0], W[1], sum(W[0] < x[7] <= W[1] for x in chiusi), W[0], sum(x[7] <= W[0] for x in chiusi)))
        tipi = {}
        for x in chiusi:
            k = (x[3].split("[")[0], x[3].split()[-1], x[8])
            tipi.setdefault(k, []).append(x)
        for k, v in sorted(tipi.items(), key=lambda kv: -len(kv[1])):
            print("      la banda %s, il %s a %s: %d casi; il margine da %.4f a %.4f; g %s; (a, b) %s" % (k[0], k[1], k[2], len(v), min(x[7] for x in v), max(x[7] for x in v),
                  sorted(set(x[2] for x in v)), sorted(set((x[0], x[1]) for x in v))[:12]))
        oggi_ = [x for x in chiusi if x[0] == 1.0 and x[1] == 1.0]
        print("      i pesi di oggi (a = b = pi): %s" % ("; ".join("g %.2f %s E0 %+.4f margine %.4f" % (x[2], x[3], x[4], x[7]) for x in oggi_) or "nessun caso chiuso"))
    return chiusi


# ====================================================================== (4) LE CARICHE
def cariche(libs):
    import _livelli_piatti as LP
    import _modo_al_variare_di_s as MS
    import _dove_va_la_materia as DV
    print("### (4a) le cariche sul tick LIBERO")
    sz = np.diag([1.0, -1.0] * 6)
    for lib in libs:
        T = lib.T_oggi
        comm = float(np.abs(np.einsum("abij,jk->abik", T, sz) - np.einsum("ij,abjk->abik", sz, T)).max())
        print("  eps %g: ||[T(k), sigma_z]|| massimo sulla zona %.3e -> sigma_z (Q_S) %s dal tick libero" % (lib.eps, comm, "CONSERVATA" if comm < 1e-12 else "NON conservata"))
    print("  Q_AB = N_A - N_B e la valle: il tick libero e' LINEARE e invariante per traslazioni: ogni stato di Bloch evolve per una fase -> le popolazioni di banda e il momento sono CONSERVATE esattamente (per costruzione)")
    print("  col LEGAME di oggi (alpha di rho = sum delle 12 componenti, una fase per nodo): non lineare; conserva la norma (una fase) e il momento cristallino modulo il reticolo reciproco; NON le popolazioni di banda")
    print("### (4b) le uscite con la carica di banda Q_AB (il solitone: due quanti di A, Q_AB +2)")
    for nome, dopo in (("(n1) A -> piatta (un quanto)", "+1 -> 0 per il quanto: Q_AB 2 -> 1"), ("(n2) A + A -> piatta + piatta", "2 -> 0"),
                       ("(n2-misto) A + A -> piatta + A", "2 -> 1"), ("(n2-misto) A + A -> piatta + B", "2 -> -1")):
        print("  %-34s Q_AB %s: VIETATA se Q_AB conservata" % (nome, dopo))
    print("  sigma_z: il solitone tutto spin su (q 1); le uscite misurate hanno q(D) 1 (03142636): sigma_z NON vieta; la valle: 2K = k1 + k2 (la riflessione per K, misurata): NON vieta")
    print("### (4c) perche' oggi non protegge: la parte NON LINEARE del tick su psi0 di (R) e le sue frazioni di banda")
    r, g, N = LP.CONFIG["R_1e6"]
    psi0, mu, _cj = LP.stato("R_1e6")
    with LP.scena(N) as (_rec, z, phi0, _p), LP.configurazione(r, g):
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
        bande = LP.ML.Bande(Z, z["L"])
        L = z["L"]
        Tp = MS.tick(z, phi0, psi0, LP.FORMA)
        f = np.fft.fft2(psi0.reshape(L, L, 12), axes=(0, 1))
        Tl = np.fft.ifft2(np.einsum("abij,abj->abi", A, f), axes=(0, 1)).reshape(psi0.shape)
    d = Tp - Tl
    for chi, x in (("psi0", psi0), ("T(psi0) - T_lin psi0 (il legame)", d)):
        c = bande.coeff(x)
        pk = np.abs(c) ** 2
        tot = float(pk.sum())
        print("  %-34s |.|/|psi0| %.3e; %s" % (chi, float(np.linalg.norm(x)) / float(np.linalg.norm(psi0)), "  ".join("%s %.4e" % (gn, float(pk[..., list(idx)].sum()) / tot) for gn, idx in bande.gruppi.items())))
    fr = []
    for x in (psi0, d):
        c = bande.coeff(x)
        fr.append(float(np.sum(np.abs(bande.parte(c, ("P0", "Ppi"))) ** 2)) / float(np.sum(np.abs(c) ** 2)))
    print("  la frazione PIATTA (P0 + Ppi): del legame su psi0 %.4e, di psi0 stesso %.4e (il confronto: il legame accoppia il solitone alle piatte se la prima non e' al livello della seconda)" % (fr[1], fr[0]))


def localita(lib, Z):
    """### **`max |P_g(R)|` per distanza** *(il proiettore di gruppo nello spazio reale)*."""
    L = lib.L
    A, _B = cartesiano(L)
    ii = np.arange(L)
    ii = np.where(ii < L // 2 + 1, ii, ii - L)
    R = ii[:, None, None] * A[0] + ii[None, :, None] * A[1]
    dist = np.hypot(R[..., 0], R[..., 1])
    print("  eps %g: max_ab |P_g(R)_ab| per distanza |R| (0, 1, 2, 4, 8, 16, 32) e la pendenza di ln max|P| contro |R| fra 2 e 20:" % lib.eps)
    for g, idx in GRUPPI:
        Zg = Z[..., list(idx)]
        Pk = np.einsum("abik,abjk->abij", Zg, Zg.conj())
        Pr = np.fft.ifft2(Pk, axes=(0, 1))
        mx = np.abs(Pr).max(axis=(2, 3))
        tab = []
        for d0 in (0, 1, 2, 4, 8, 16, 32):
            m = np.abs(dist - d0) < 0.5
            tab.append(float(mx[m].max()) if m.any() else float("nan"))
        sel = (dist >= 2) & (dist <= 20)
        k = np.polyfit(dist[sel], np.log(np.maximum(mx[sel], 1e-300)), 1)[0]
        print("    %-3s %s; pendenza %+.3f" % (g, " ".join("%.2e" % x for x in tab), k))


# ====================================================================== (5) LE PIATTE CHE SI MUOVONO, LA MONETA
def piatte_e_moneta(libs, Es):
    import _dove_va_la_materia as DV
    print("### (5a) le piatte che si muovono (eps %g): la velocita' di gruppo massima, e il tempo per lasciare il bordo (~2 archi)" % EPS[0])
    lib = libs[0]
    E = Es[lib.eps]
    for g, idx in GRUPPI:
        if g not in PIATTE:
            continue
        v = max(float(gradiente(E[..., b], lib.L).max()) for b in idx)
        print("  %-3s v_max %.4e archi per unita' di tempo; 2/v_max %.0f unita' di tempo, contro 1/gamma %s" % (g, v, 2.0 / v if v > 0 else float("inf"), "  ".join("%.0f (%s)" % (1.0 / x, n) for n, x in (("r 1", 0.151), ("X1", 0.061), ("(R)", 0.008)))))
    print("### (5c) la moneta: exp(-i eps dtau sigma.n) per ESTREMITA' (motore._moneta_spin, CAMM-MONETA-SPIN): mescola i due stati di SPIN di ogni estremita', col versore n dell'arco")
    L = lib.L
    K, _Kp = BP.indici_K(L)
    for nome, ij in (("Gamma", (0, 0)), ("K", K)):
        for x in libs:
            e = np.sort(Es[x.eps][ij])
            sep = np.diff(e)
            print("  %-5s eps %g: %s; le separazioni minime fra livelli vicini %s" % (nome, x.eps, " ".join("%+.4f" % v for v in e), " ".join("%.4f" % v for v in np.sort(sep)[:3])))
    _A, B = cartesiano(L)
    sx = np.zeros((12, 12), dtype=complex)
    sy = np.zeros((12, 12), dtype=complex)
    for e_ in range(6):
        sx[2 * e_, 2 * e_ + 1] = sx[2 * e_ + 1, 2 * e_] = 1.0
        sy[2 * e_, 2 * e_ + 1], sy[2 * e_ + 1, 2 * e_] = -1j, 1j
    for x in libs:
        e_g = Es[x.eps][(0, 0)]
        e_k = Es[x.eps][K]
        print("  il gap fra le bande, eps %g: a Gamma Ppi (max %+.5f) e A (min %+.5f): %.5f; a K A (max %+.5f) e P0 (min %+.5f): %.5f; a K i due livelli di A %.2e, di P0 %.2e"
              % (x.eps, e_g[3], e_g[4], e_g[4] - e_g[3], e_k[5], e_k[6], e_k[6] - e_k[5], e_k[5] - e_k[4], e_k[9] - e_k[6]))
    print("  l'elicita' <sigma.k^> degli stati della banda A vicino a Gamma e a K (k relativo al punto), eps 0.5 contro 0:")
    for x in libs:
        _ph, Z = DV.autovettori(x.tick(math.pi, math.pi))
        for nome, c0 in (("Gamma", (0, 0)), ("K", K)):
            vals = []
            for di, dj in ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1)):
                ij = ((c0[0] + di) % L, (c0[1] + dj) % L)
                kk = (di * B[0] + dj * B[1]) / L
                kh = kk / np.linalg.norm(kk)
                Hs = kh[0] * sx + kh[1] * sy
                for b in BP.A_:
                    v = Z[ij][:, b]
                    vals.append(float(np.real(np.vdot(v, Hs @ v))))
            print("    eps %g, %-5s: <sigma.k^> delle due bande di A sui 6 vicini: %s" % (x.eps, nome, " ".join("%+.3f" % v for v in vals)))


def main():
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        print("=" * 130)
        print("CHIUDERE LE USCITE (Luca 00:38, 00:44, 00:50): il tick libero, s %g, Omega 2 pi/s %.4f; eps %s (0.5 il principale); W %s; nessuna corsa di solitoni" % (S, OMEGA, EPS, W))
        print("  LE LETTURE, SCRITTE PRIMA: (u1) una regione con tutte le uscite chiuse; (u2) vuota: quale resta aperta e perche'; (u3) una carica conservata con un legame locale le vieterebbe; (u4) il decadimento e' strutturale; (u5) la moneta cambia la risposta;"
              " la moneta: (e1) campo uniforme; (e2) massa di Dirac; (e3) altro; (e4) accoppiamento spin-direzione (elicita' o spin-orbita)")
        print("=" * 130)
        libs = [Libero(e) for e in EPS]
        for lib in libs:
            d = float(np.abs(lib.tick(math.pi, math.pi) - lib.T_oggi).max())
            esito("DEVE PASSARE: eps %g, il tick ricomposto coi pesi di oggi e la moneta = il tick dei pezzi (entro %g)" % (lib.eps, TOLL_RICOMPOSTO), d < TOLL_RICOMPOSTO, "%.1e" % d)
        print("### (1), (2) LO SPETTRO DI OGGI E I PUNTI DELLA BANDA (mu in [E0, E0 + g], alpha in [0, g])")
        Es = {}
        for lib in libs:
            Es[lib.eps], _sp = oggi(lib)
        print("### (3) LA REGIONE")
        for lib in libs:
            regione(lib)
        cariche(libs)
        print("### (4d) la localita' dei proiettori di banda (r 1)")
        for lib in libs:
            _ph, Z = DV.autovettori(lib.tick(math.pi, math.pi))
            localita(lib, Z)
        piatte_e_moneta(libs, Es)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; fallite: %s" % (OK[0], OK[1], FALLITE))
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
