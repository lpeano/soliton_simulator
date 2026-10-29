# -*- coding: utf-8 -*-
r"""**IL MENU PER LA DECISIONE SULLE BANDE PIATTE** *(SULLA CARTA E DAL CODICE; il mandato di Luca delle `19:12` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_bande_piatte_menu.md`)*: ### **conti sul tick libero, mai nel nucleo; nessuna corsa.**
### **(1) il punto di mezzo** *(il primo ordine contro le bande; le prove di simmetria)*; ### **(2) `Q_S` e le valli;** ### **(3) gli stati compatti delle piatte;**
### **(4) la strada (B) sul tick libero ricomposto in memoria dai generatori dei pezzi.**

    python csv/_bande_piatte.py --referto > doc/referti_l2/bande_piatte.txt
"""
import contextlib
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

FORMA = "S1"
N = 1e6
S_PUNTO1 = (0.3, 0.15, 0.075)
S_MENU = 0.15
EPS_TABELLA = 0.5              # ### PARAMETRI di CAMM-MONETA-SPIN (leggi.yaml)
J_LEGAME, J_MONETA, J_GROVER, J_SPOST = 0, 2, 3, 4    # ### le posizioni in composizione.ORDINE, la prima meta'
PPI, A_, P0, B_ = (0, 1, 2, 3), (4, 5), (6, 7, 8, 9), (10, 11)
DELTA_B1 = (0.8, -0.4)         # ### gli spostamenti della somma P0 + Ppi chiesti dal mandato
# ### (nome, il centro, il raggio minimo e massimo): i nodi a distanza fra i due raggi
GRAPPOLI = (("1 nodo", (0.0, 0.0), -1.0, 0.01), ("triangolo", (0.5, math.sqrt(3.0) / 6.0), -1.0, 0.6), ("rombo", (0.25, math.sqrt(3.0) / 4.0), -1.0, 0.9),
            ("esagono", (0.0, 0.0), 0.5, 1.01), ("esagono+centro", (0.0, 0.0), -1.0, 1.01), ("due anelli", (0.0, 0.0), -1.0, 2.01))
SOGLIA_NULLO = 1e-10
SOGLIA_RANGO = 1e-8
TOLL_RICOSTRUZIONE = 1e-12
TOLL_GENERATORI = 1e-10
RAPPORTO_S2 = (3.0, 5.0)
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


def mm(*X):
    r = X[0]
    for y in X[1:]:
        r = np.einsum("abij,abjk->abik", r, y)
    return r


@contextlib.contextmanager
def scena(s):
    import _diagnosi_s4 as D
    import _modo_al_variare_di_s as MS
    with D.configura(FORMA, s, N):
        _rec, z, phi0, _p = MS.scena(FORMA, s, N)
        yield z, phi0


def pezzo(z, phi0, j, eps, conv):
    """### **Il mezzo pezzo `j` della prima meta' dell'ordine, solo** *(`percorri_tick` con `salta` = tutti gli altri id e `quanti = j + 1`)*, ### **per `k`.**"""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    ids = [x[0] for x in CM.ORDINE]
    salta = tuple(sorted(set(ids) - {ids[j]}))
    par = dict(z["par"])
    par["eps"] = eps
    L, n = z["L"], z["inc"].n
    A = np.empty((L, L, 12, 12), dtype=complex)
    for c in range(12):
        p = np.zeros((n, 12), dtype=complex)
        p[0, c] = DV.AMP
        z["st"]["psi_h"][...] = p.reshape(z["st"]["psi_h"].shape)
        z["st"]["phi_h"][...] = phi0
        with SF.forma(FORMA), BE.conv(conv):
            TK.percorri_tick(z["st"], z["mot"], par, salta, None, j + 1)
        R = z["st"]["psi_h"].reshape(n, 12).copy() / DV.AMP
        A[:, :, :, c] = np.fft.fft2(R.reshape(L, L, 12), axes=(0, 1))
    return A


def pezzi(s, eps=0.0, conv="simm"):
    import _dove_va_la_materia as DV
    with scena(s) as (z, phi0):
        P = {j: pezzo(z, phi0, j, eps, conv) for j in (J_LEGAME, J_MONETA, J_GROVER, J_SPOST)}
        A = DV.matrice(z, phi0, DV.AMP) if (eps == 0.0 and conv == "simm") else None
    T = mm(P[J_LEGAME], P[J_MONETA], P[J_GROVER], P[J_SPOST], P[J_SPOST], P[J_GROVER], P[J_MONETA], P[J_LEGAME])
    return P, T, A


def fasi(T, s):
    """### **Le fasi per unita' di tempo, `-arg(lambda)/s`, ordinate a ogni `k`.**"""
    return np.sort(-np.angle(np.linalg.eigvals(T)) / s, axis=-1)


def generatori(P, s):
    """### **`2 P_u - I` e `R_S` dai mezzi pezzi** *(`U = cos(phi) I - i sin(phi) X`, `phi = pi s/4`)*."""
    f = math.pi * s / 4.0
    I = np.eye(12)
    X_G = 1j * (P[J_GROVER] - math.cos(f) * I) / math.sin(f)
    R_S = 1j * (P[J_SPOST] - math.cos(f) * I) / math.sin(f)
    return X_G, R_S


def ricomposto(X_G, R_S, s, alpha, beta, M=None):
    """### **`T = M G(alpha) S(beta) S(beta) G(alpha) M`** *(i mezzi pezzi `exp(-i s alpha/4 X_G)`, `exp(-i s beta/4 R_S)`)*."""
    I = np.eye(12)
    G = math.cos(s * alpha / 4.0) * I - 1j * math.sin(s * alpha / 4.0) * X_G
    S = math.cos(s * beta / 4.0) * I - 1j * math.sin(s * beta / 4.0) * R_S
    if M is None:
        return mm(G, S, S, G)
    return mm(M, G, S, S, G, M)


def c_di_k(X_G, R_S):
    """### **Gli autovalori di `P_u R_S P_u` su `ran P_u`** *(due per `k`: le due componenti di spin)*."""
    Pu = (X_G + np.eye(12)) / 2.0
    w, V = np.linalg.eigh(Pu)
    Vu = V[..., -2:]
    C = np.einsum("abji,abjk,abkl->abil", Vu.conj(), R_S, Vu)
    return np.sort(np.linalg.eigvalsh((C + np.conj(np.swapaxes(C, -1, -2))) / 2.0), axis=-1), float(np.abs(w[..., :-2]).max()), float(np.abs(w[..., -2:] - 1).max())


def indici_K(L):
    return (L // 3, L // 3), (2 * L // 3, 2 * L // 3)


def scarto_libero(E, iK):
    return float(np.mean(E[iK][list(P0)]) + np.mean(E[iK][list(PPI)]) - 2.0 * np.mean(E[iK][list(A_)]))


def simmetrie(E):
    L = E.shape[0]
    meno = (-np.arange(L)) % L
    Em = E[meno][:, meno]

    def d(X, Y):
        return float(np.abs(np.sort(X, axis=-1) - np.sort(Y, axis=-1)).max())
    senza = list(A_) + list(P0) + list(B_)
    return {"E(k) = E(-k)": d(E, Em), "E -> -E (tutte)": d(E, -E), "E -> -E (senza Ppi)": d(E[..., senza], -E[..., senza]),
            "E -> -pi - E (stesso k)": d(E, -math.pi - E), "E -> -pi - E (k -> -k)": d(E, -math.pi - Em),
            "A(k) = -B(k)": d(E[..., list(A_)], -E[..., list(B_)]), "A(k) = -B(-k)": d(E[..., list(A_)], -Em[..., list(B_)])}


def punto1():
    print("-" * 130)
    print("### (1) IL PUNTO DI MEZZO: il primo ordine H1 = (alpha/2)(2 P_u - I) + (beta/2) R_S, alpha = beta = pi")
    scarti_formula = {}
    for s in S_PUNTO1:
        P, T, A = pezzi(s)
        L = T.shape[0]
        iK, iK2 = indici_K(L)
        esito("DEVE PASSARE: s %g, il tick ricomposto dai mezzi pezzi = A(k) entro %g" % (s, TOLL_RICOSTRUZIONE), float(np.abs(T - A).max()) < TOLL_RICOSTRUZIONE, "%.1e" % float(np.abs(T - A).max()))
        print("  s %g: il legame nel tick libero |L - I| %.1e; la moneta (eps 0) |M - I| %.1e" % (s, float(np.abs(P[J_LEGAME] - np.eye(12)).max()), float(np.abs(P[J_MONETA] - np.eye(12)).max())))
        X_G, R_S = generatori(P, s)
        I = np.eye(12)
        print("  s %g: X_G^2 = I %.1e, R_S^2 = I %.1e, hermitiani %.1e %.1e; la variazione di X_G sulla zona %.1e (le 12 componenti della cella non sono le estremita' di un solo nodo)"
              % (s, float(np.abs(mm(X_G, X_G) - I).max()), float(np.abs(mm(R_S, R_S) - I).max()), float(np.abs(X_G - np.conj(np.swapaxes(X_G, -1, -2))).max()),
                 float(np.abs(R_S - np.conj(np.swapaxes(R_S, -1, -2))).max()), float(np.abs(X_G - X_G[0, 0]).max())))
        c, e0, e1 = c_di_k(X_G, R_S)
        print("  s %g: P_u proiettore (autovalori 0 e 1 entro %.1e %.1e); c(k): le due componenti uguali entro %.1e; c(K) %+.6f, c(K') %+.6f, min %+.6f, max %+.6f"
              % (s, e0, e1, float(np.abs(c[..., 0] - c[..., 1]).max()), c[iK][0], c[iK2][0], float(c.min()), float(c.max())))
        E = fasi(A, s)
        fA = -0.5 * np.sqrt(2.0 * math.pi ** 2 * (1.0 + c))
        dA = float(np.abs(np.sort(E[..., list(A_)], axis=-1) - np.sort(fA, axis=-1)).max())
        dB = float(np.abs(np.sort(E[..., list(B_)], axis=-1) - np.sort(-fA, axis=-1)).max())
        dP0 = float(np.abs(E[..., list(P0)] - 0.0).max())
        dPpi = float(np.abs(E[..., list(PPI)] + math.pi).max())
        scarti_formula[s] = max(dA, dB)
        print("  s %g: le bande contro il primo ordine: A %.3e, B %.3e; le piatte: P0 contro 0 %.1e, Ppi contro -pi %.1e" % (s, dA, dB, dP0, dPpi))
        print("  s %g: A(K) %+.6f (+pi/2: %+.3e), A(K') %+.6f (+pi/2: %+.3e); B(K) %+.6f; la banda A in [%+.4f, %+.4f], B in [%+.4f, %+.4f]"
              % (s, E[iK][4], E[iK][4] + math.pi / 2, E[iK2][4], E[iK2][4] + math.pi / 2, E[iK][10], E[..., 4:6].min(), E[..., 4:6].max(), E[..., 10:12].min(), E[..., 10:12].max()))
        print("  s %g: lo scarto libero E_P0 + E_Ppi - 2 E_A per unita' di tempo: a K %+.4e, a K' %+.4e" % (s, scarto_libero(E, iK), scarto_libero(E, iK2)))
        for nome, v in simmetrie(E).items():
            print("  s %g: la prova %-26s lo scarto massimo %.3e" % (s, nome, v))
    r = scarti_formula[0.15] / scarti_formula[0.075]
    print("  lo scarto dal primo ordine: %s; i rapporti %.4f %.4f" % ("  ".join("s %g %.3e" % (s, scarti_formula[s]) for s in S_PUNTO1), scarti_formula[0.3] / scarti_formula[0.15], r))
    esito("DEVE PASSARE: il primo ordine entro O(s^2) (il rapporto fra s 0.15 e s 0.075 in %s)" % (RAPPORTO_S2,), RAPPORTO_S2[0] < r < RAPPORTO_S2[1], "%.4f" % r)


def punto2():
    print("-" * 130)
    print("### (2) Q_S E LE VALLI, a s %g" % S_MENU)
    sz = np.diag([1.0, -1.0] * 6)
    for eps in (0.0, EPS_TABELLA):
        _P, T, _A = pezzi(S_MENU, eps)
        comm = float(np.abs(np.einsum("abij,jk->abik", T, sz) - np.einsum("ij,abjk->abik", sz, T)).max())
        print("  eps %g: ||[T(k), sigma_z]|| massimo sulla zona %.3e" % (eps, comm))


def compatti(T, s, lam, nome):
    """### **I vettori con `T v = lam v` ESATTO, supportati su un grappolo di nodi;** ### **poi il rango delle loro traslazioni a ogni `k`.**"""
    import _solitoni_triangoli as STR
    L = T.shape[0]
    Rb = np.fft.ifft2(T, axes=(0, 1))
    off = [(a, b) for a in range(L) for b in range(L) if float(np.abs(Rb[a, b]).max()) > 1e-12]
    off = [((a + L // 2) % L - L // 2, (b + L // 2) % L - L // 2) for a, b in off]
    print("  [%s] il tick in spazio reale: %d blocchi 12x12 non nulli, gli spostamenti %s" % (nome, len(off), sorted(off)))
    trovati, ultimo = None, None
    for gnome, centro, rmin, rmax in GRAPPOLI:
        C = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if rmin < np.hypot(*(a * STR.A1 + b * STR.A2 - np.array(centro))) <= rmax]
        righe = sorted({(c[0] + o[0], c[1] + o[1]) for c in C for o in off})
        ri = {r: i for i, r in enumerate(righe)}
        Mx = np.zeros((12 * len(righe), 12 * len(C)), dtype=complex)
        for j, c in enumerate(C):
            for o in off:
                r = (c[0] + o[0], c[1] + o[1])
                Mx[12 * ri[r]:12 * ri[r] + 12, 12 * j:12 * j + 12] += Rb[o[0] % L, o[1] % L]
            Mx[12 * ri[c]:12 * ri[c] + 12, 12 * j:12 * j + 12] -= lam * np.eye(12)
        _u, sv, Vh = np.linalg.svd(Mx)
        nul = int(np.sum(sv < SOGLIA_NULLO * sv[0])) + max(0, Mx.shape[1] - len(sv))
        print("  [%s] il grappolo %-10s %2d nodi: gli stati compatti %d (il valore singolare piu' piccolo %.1e)" % (nome, gnome, len(C), nul, sv[-1] / sv[0]))
        if nul > 0 and trovati is None:
            trovati = (gnome, C, Vh[-nul:].conj())
        if nul > 0:
            ultimo = (gnome, C, Vh[-nul:].conj())
    if trovati is None:
        print("  [%s] nessuno stato compatto fino a %s" % (nome, GRAPPOLI[-1][0]))
        return None
    gmin, nmin, smin = trovati[0], len(trovati[1]), trovati[2].shape[0]
    gnome, C, V = ultimo
    k1, k2 = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    Vk = np.zeros((L, L, 12, V.shape[0]), dtype=complex)
    for j, c in enumerate(C):
        fase = np.exp(-2j * np.pi * (k1 * c[0] + k2 * c[1]) / L)
        Vk += fase[:, :, None, None] * V[:, 12 * j:12 * j + 12].T[None, None]
    res = float(np.abs(np.einsum("abij,abjm->abim", T, Vk) - lam * Vk).max())
    sv = np.linalg.svd(Vk, compute_uv=False)
    rango = np.sum(sv > SOGLIA_RANGO * sv[..., :1], axis=-1)
    u, cnt = np.unique(rango, return_counts=True)
    bassi = [(int(a), int(b)) for a, b in zip(*np.nonzero(rango < 4))]
    print("  [%s] il grappolo minimo: %s (%d nodi, %d stati); le traslazioni degli stati del grappolo %s: T v(k) = lam v(k) entro %.1e; il rango a ogni k: %s; i k sotto 4 (%d): %s"
          % (nome, gmin, nmin, smin, gnome, res, dict(zip(u.tolist(), cnt.tolist())), len(bassi), bassi[:12]))
    return gmin, nmin, smin, bassi


def punto3():
    print("-" * 130)
    print("### (3) GLI STATI COMPATTI DELLE PIATTE, a s %g" % S_MENU)
    _P, T, A = pezzi(S_MENU)
    out = {}
    for nome, lam in (("P0", 1.0 + 0j), ("Ppi", np.exp(1j * math.pi * S_MENU))):
        out[nome] = compatti(A, S_MENU, lam, nome)
    return out


def punto4():
    print("-" * 130)
    print("### (4) LA STRADA (B) sul tick libero ricomposto, a s %g" % S_MENU)
    s = S_MENU
    P, T, A = pezzi(s)
    X_G, R_S = generatori(P, s)
    L = T.shape[0]
    iK, iK2 = indici_K(L)
    T0 = ricomposto(X_G, R_S, s, math.pi, math.pi)
    esito("DEVE PASSARE: alpha = beta = pi ridà A(k) entro %g" % TOLL_GENERATORI, float(np.abs(T0 - A).max()) < TOLL_GENERATORI, "%.1e" % float(np.abs(T0 - A).max()))
    E0 = fasi(A, s)

    def riga(nome, E):
        cur = (E[iK[0] + 1, iK[1]][4] + E[iK[0] - 1, iK[1]][4] - 2.0 * E[iK][4])
        print("  %-44s scarto libero a K %+.4f (spostato di %+.4f); A(K) %+.5f (di %+.2e); la curvatura di A a K %+.3e (era %+.3e); P0 in [%+.4f, %+.4f], Ppi in [%+.4f, %+.4f]"
              % (nome, scarto_libero(E, iK), scarto_libero(E, iK) - scarto_libero(E0, iK), E[iK][4], E[iK][4] - E0[iK][4], cur,
                 E0[iK[0] + 1, iK[1]][4] + E0[iK[0] - 1, iK[1]][4] - 2.0 * E0[iK][4], E[..., 6:10].min(), E[..., 6:10].max(), E[..., 0:4].min(), E[..., 0:4].max()))
    riga("oggi (alpha = beta = pi)", E0)
    print("  (B1) il rapporto nodo/arco, con mu0 = (1/2) sqrt(alpha^2 - alpha beta + beta^2) = pi/2 fisso: alpha = pi - delta, beta la radice vicina a pi")
    for dlt in DELTA_B1:
        al = math.pi - dlt
        be = 0.5 * (al + math.sqrt(4.0 * math.pi ** 2 - 3.0 * al ** 2))
        E = fasi(ricomposto(X_G, R_S, s, al, be), s)
        riga("(B1) delta %+.1f: alpha %.4f beta %.4f r %.4f" % (dlt, al, be, be / al), E)
    print("  (B2) la moneta della tabella, eps %g" % EPS_TABELLA)
    P5, T5, _ = pezzi(s, EPS_TABELLA)
    E5 = fasi(T5, s)
    riga("(B2) eps %g" % EPS_TABELLA, E5)
    print("  (B2) eps %g: lo spettro a K %s; a Gamma %s; la larghezza di ogni indice sulla zona %s"
          % (EPS_TABELLA, np.round(E5[iK], 4).tolist(), np.round(E5[0, 0], 4).tolist(), np.round(E5.max(axis=(0, 1)) - E5.min(axis=(0, 1)), 4).tolist()))
    print("  (B3) un altro ordine palindromo (eps 0: la moneta e' l'identita')")
    for s3 in (S_MENU, 0.075):
        Pq, Tq, Aq = pezzi(s3)
        Eq = fasi(Aq, s3)
        G, S = Pq[J_GROVER], Pq[J_SPOST]
        for nome, Tx in (("S G G S", mm(S, G, G, S)), ("G S S G (oggi)", mm(G, S, S, G))):
            Ex = fasi(Tx, s3)
            print("  (B3) s %g, %-16s lo scarto libero a K %+.4e (spostato di %+.3e rispetto a oggi)" % (s3, nome, scarto_libero(Ex, iK), scarto_libero(Ex, iK) - scarto_libero(Eq, iK)))
    print("  (B4) la convenzione")
    _Po, To, _Ao = pezzi(s, 0.0, "oggi")
    Eo = fasi(To, s)
    print("  (B4) oggi: lo scarto libero a K %+.4e (simm %+.4e); A(K) %+.5f (simm %+.5f)" % (scarto_libero(Eo, iK), scarto_libero(E0, iK), Eo[iK][4], E0[iK][4]))


def referto():
    print("=" * 130)
    print("IL MENU PER LA DECISIONE SULLE BANDE PIATTE (Luca 19:12): conti sul tick libero di %s, L 81; nessuna corsa" % FORMA)
    print("=" * 130)
    print("  la configurazione: FORMA %s N %g S_PUNTO1 %s S_MENU %g EPS_TABELLA %g J (legame, moneta, Grover, spostamento) %s PPI %s A %s P0 %s B %s DELTA_B1 %s GRAPPOLI %s SOGLIA_NULLO %g SOGLIA_RANGO %g TOLL_RICOSTRUZIONE %g TOLL_GENERATORI %g RAPPORTO_S2 %s"
          % (FORMA, N, S_PUNTO1, S_MENU, EPS_TABELLA, (J_LEGAME, J_MONETA, J_GROVER, J_SPOST), PPI, A_, P0, B_, DELTA_B1, GRAPPOLI, SOGLIA_NULLO, SOGLIA_RANGO, TOLL_RICOSTRUZIONE, TOLL_GENERATORI, RAPPORTO_S2))
    print("  la convenzione degli strumenti: simm (exp(i theta (I - 2P)/2)); le fasi per unita' di tempo -arg(lambda)/s; la prima ricerca (eps 0) e' quella di tutte le scene di S1")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: per ciascun punto il fatto; per (B) quante modifiche minime e il loro costo nel punto 2")
    punto1()
    punto2()
    punto3()
    punto4()
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
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
