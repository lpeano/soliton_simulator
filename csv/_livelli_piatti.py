# -*- coding: utf-8 -*-
r"""**LA REGOLA DEI LIVELLI PIATTI E LA PROVA DI UN SOLITONE CHE LA RISPETTA** *(UNA PROVA, NON UNA CURA; il mandato di Luca delle `09:31` del `2026-10-30`, con l'integrazione delle `09:33`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-30_livelli_piatti.md`)*:
### **i pesi `a_n = pi`, `b_a = r pi` e la saturazione `g` del legame `alpha = g x^2/(1 + x^2)` cambiati IN MEMORIA, rimessi all'uscita** *(il gemello `beta` scalato dello stesso `g`)*;
### **Newton col metodo di `_strada_b_r.cerca`; la forma della crescita di `_strada_b_lati.giudica`; l'esame di `_modo_lento.analizza`.**

    python csv/_livelli_piatti.py --previsioni > doc/referti_l2/livelli_piatti/previsioni.txt
    python csv/_livelli_piatti.py --cerca R_1e6 > doc/referti_l2/livelli_piatti/cerca_R_1e6.txt   # idem X1, X2, R_3e5, R_3e6
    python csv/_livelli_piatti.py --breve R_1e6 > doc/referti_l2/livelli_piatti/breve_R_1e6.txt   # idem le altre
    python csv/_livelli_piatti.py --lunga               # un pezzo; si ripete fino alla fine (senza stato di ripresa, lo RICOSTRUISCE dai pezzi scritti)
    python csv/_livelli_piatti.py --cerca R_3e6_t > doc/referti_l2/livelli_piatti/cerca_R_3e6_t.txt   # la ripresa (Luca 13:22): la tappa a N 2e6; idem X1_p (al piu' 10 passi), R_3e5_t (Luca 16:26: la tappa a N 6e5)
    python csv/_livelli_piatti.py --collaudo-forma > doc/referti_l2/livelli_piatti/collaudo_forma.txt  # il criterio aggiunto della forma sui casi noti
    python csv/_livelli_piatti.py --referto > doc/referti_l2/livelli_piatti.txt
"""
import contextlib
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

import _modo_lento as ML                                       # noqa: E402
import _strada_b_lati as SL                                    # noqa: E402
import _strada_b_r as SB                                       # noqa: E402

FORMA = "S1"
S = 0.15
N_RIF = 1e6                    # ### la N di dfb5ab7e (S1_s0.150)
CONFIG = {"R_1e6": (0.6, 0.5, 1e6), "X1": (1.0, 0.5, 1e6), "X2": (0.6, 1.0, 1e6), "R_3e5": (0.6, 0.5, 3e5), "R_3e6": (0.6, 0.5, 3e6)}
PARTENZA = {"R_1e6": None, "X1": None, "X2": None, "R_3e5": "R_1e6", "R_3e6": "R_1e6"}   # ### None = dfb5ab7e riscalato
# ### LA RIPRESA (il testo di Luca delle 13:22, mandato alle 15:45): nomi nuovi, perche' scrivi_nuovo non riscrive; le vecchie ricerche e brevi restano, dichiarate
PASSI_X1 = 10                  # ### «al piu' 10 passi in piu'» (Luca, 13:22)
RIPRESE = {"R_3e6_t": {"come": "R_3e6", "partenza": "R_1e6", "tappa_N": 2e6, "passi": None},     # ### la tappa a N 2e6, NON scritta; passi None = SB.MAX_NEWTON
           "X1_p": {"come": "X1", "partenza": "X1", "tappa_N": None, "passi": PASSI_X1},
           "R_3e5_t": {"come": "R_3e5", "partenza": "R_1e6", "tappa_N": 6e5, "passi": None}}   # ### Luca 16:26 (d): per continuazione, la tappa a N 6e5, NON scritta
SIGMA_FORMA = 3.0              # ### il 3 sigma di doc/PATTERN_DI_PROVA.md (P1-sexies), per il criterio aggiunto della forma
LETTURA = {"R_1e6": ("R_1e6",), "R_3e5": ("R_3e5_t", "R_3e5"), "R_3e6": ("R_3e6_t", "R_3e6"), "X1": ("X1",), "X2": ("X2",)}   # ### per le letture: la prima che ha la breve; X1 da X1 (Luca 16:26: X1_p non e' nell'ordine)
W_LISTA = (0.05, 0.2)          # ### la larghezza per quanto di 99b679bc, il lato stretto
L_SCENA = 81
FRAZ_LARGO = 1.0 / 6.0         # ### oltre L/6 la corsa a L 120 (il mandato)
T_BREVE = 300.0
PASSO_BREVE = 3.0
OGNI_D = 5
FATTORE_DEROGA = 10.0
T_MAX = 20000
PEZZO = 2000
OGNI = 10
OGNI_LUNGA_D = 20
FINESTRA = 500.0
TOLL_NORMA = 1e-10
TOLL_RICOMPOSTO = 1e-10
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "livelli_piatti")
DIR_NPZ = os.path.join(RADICE, "db", "livelli_piatti")
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


def scrivi_nuovo(fj, riga):
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(fj), exist_ok=True)
    with open(fj, "xb") as fh:
        fh.write(dati)


def leggi(fj):
    return json.loads(io.open(fj, encoding="utf-8").read())


# ====================================================================== LA CONFIGURAZIONE IN MEMORIA
@contextlib.contextmanager
def configurazione(r, g):
    """### **`FP.z_nodo` per `a_n/pi = 1`, `FP.z_arco` per `b_a/pi = r`; `SF.pezzi_di` con `(g alpha, g beta)`; rimessi all'uscita** *(a `r 1`, `g 1` i fattori sono `1.0`)*."""
    import flussi_parziali as FP
    import _screening_forme_s3 as SF
    zn0, za0, pd0 = FP.z_nodo, FP.z_arco, SF.pezzi_di
    FP.z_nodo = lambda mot, frazione: zn0(mot, frazione * 1.0)
    FP.z_arco = lambda mot, frazione: za0(mot, frazione * r)

    def pd(nome):
        p = pd0(nome)

        def q(rho, lam):
            a, b = p(rho, lam)
            return g * a, g * b
        return q
    SF.pezzi_di = pd
    try:
        yield math.pi, r * math.pi
    finally:
        FP.z_nodo, FP.z_arco, SF.pezzi_di = zn0, za0, pd0


@contextlib.contextmanager
def scena(N, L=L_SCENA):
    import _diagnosi_s4 as D
    with D.configura(FORMA, S, N):
        rec, z = D.iniziale(FORMA, S, L)
        yield rec, z, z["st"]["phi_h"].copy(), z["st"]["psi_h"].copy()


def libero(r):
    """### **Il tick libero coi pesi `(pi, r pi)`, dai generatori ricomposti** *(`_bande_piatte.ricomposto`)*: `(E, P0, Ppi, A(K), la curvatura di A a K)`."""
    import _bande_piatte as BP
    with scena(N_RIF) as (_rec, z, phi0, _p):
        P = {j: BP.pezzo(z, phi0, j, 0.0, "simm") for j in (BP.J_GROVER, BP.J_SPOST)}
        X_G, R_S = BP.generatori(P, S)
        A = BP.ricomposto(X_G, R_S, S, math.pi, r * math.pi)
    E = np.sort(-np.angle(np.linalg.eigvals(A)) / S, axis=-1)
    L = E.shape[0]
    iK = (L // 3, L // 3)
    cur = E[iK[0] + 1, iK[1]][4] + E[iK[0] - 1, iK[1]][4] - 2.0 * E[iK][4]
    return A, E, float(E[..., 6:10].mean()), float(E[..., 0:4].mean()), float(E[iK][4]), float(cur)


def distanza(x, lo, hi):
    """### **La distanza con segno da `[lo, hi]`:** positiva fuori, negativa dentro; e il lato."""
    if x < lo:
        return lo - x, "sotto"
    if x > hi:
        return x - hi, "sopra"
    return -min(x - lo, hi - x), "DENTRO"


def livelli(P0, Ppi):
    return (("P0", P0), ("Ppi", Ppi), ("(P0+Ppi)/2", 0.5 * (P0 + Ppi)), ("(P0+P0)/2", P0), ("(Ppi+Ppi)/2", Ppi))


# ====================================================================== (0) LE PREVISIONI
def previsioni():
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    fj = os.path.join(DIR_JSON, "previsioni.json")
    assert not os.path.exists(fj), fj
    print("### (0) LE PREVISIONI, PRIMA DI NEWTON: il tick libero a s %g coi pesi (pi, r pi); J = [E0, E0 + g], E0 = A(K); W %s per quanto" % (S, W_LISTA))
    p0, _mu, _cj, ok = MS.carica("S1_s0.150")
    esito("DEVE PASSARE: lo stato di dfb5ab7e sul disco = la ricerca (sha1)", ok, "")
    with scena(N_RIF) as (_rec, z, phi0, _p):
        q0 = MS.tick(z, phi0, p0, FORMA)
        with configurazione(1.0, 1.0):
            q1 = MS.tick(z, phi0, p0, FORMA)
    esito("DEVE PASSARE: a r 1, g 1 il tick dello stato di dfb5ab7e = quello di oggi, AL BIT", bool(np.array_equal(q0, q1)), "")
    _A1, _E1, _a, _b, _c, cur1 = libero(1.0)
    out = {"W": list(W_LISTA), "configurazioni": {}}
    for nome, (r, g, N) in CONFIG.items():
        A, E, P0, Ppi, EK, cur = libero(r)
        with scena(N_RIF) as (_rec, z, phi0, _p), configurazione(r, g):
            Am = DV.matrice(z, phi0, DV.AMP)
        d = float(np.abs(Am - A).max())
        esito("DEVE PASSARE: %s, il tick coi pesi in memoria = il tick ricomposto entro %g" % (nome, TOLL_RICOMPOSTO), d < TOLL_RICOMPOSTO, "%.1e" % d)
        a, b = math.pi, r * math.pi
        mu0_1 = 0.5 * math.sqrt(a * a - a * b + b * b)
        riga = {"r": r, "g": g, "N": N, "P0": P0, "Ppi": Ppi, "E0": EK, "mu0_tick": -EK, "mu0_primo": mu0_1, "curvatura_su_r1": cur / cur1, "livelli": {}}
        for tipo, (E0, P0_, Ppi_) in (("tick", (EK, P0, Ppi)), ("primo", (-mu0_1, (b - a) / 2.0, -(a + b) / 2.0))):
            lo, hi = E0, E0 + g
            dl = {nm: distanza(x, lo, hi) for nm, x in livelli(P0_, Ppi_)}
            alias = min(abs(x + k * 2.0 * math.pi / S - c) for nm, x in livelli(P0_, Ppi_) for k in (-1, 1) for c in (lo, hi))
            mm = min(v[0] for v in dl.values())
            riga["livelli"][tipo] = {"J": [lo, hi], "distanze": {k: list(v) for k, v in dl.items()}, "margine": mm, "alias_min": alias}
            print("  %-6s r %.2f g %.2f N %.0e [%s]: E0 %+.5f, J [%+.4f, %+.4f]; %s; IL MARGINE MINIMO %+.4f (%s); le copie modulo 2 pi/s a %.1f"
                  % (nome, r, g, N, tipo, E0, lo, hi, "; ".join("%s %+.4f %s %.4f" % (k, x, v[1], v[0]) for (k, x), v in zip(livelli(P0_, Ppi_), dl.values())),
                     mm, ", ".join("%s W %g" % ("fuori da" if mm > w else "DENTRO", w) for w in W_LISTA), alias))
        print("  %-6s la massa: la curvatura di A a K %.4f di r 1 (a_n b_a/pi^2 %.4f); mu0 %.5f (tick) %.5f (primo ordine), r 1 pi/2"
              % (nome, cur / cur1, a * b / math.pi ** 2, -EK, mu0_1))
        out["configurazioni"][nome] = riga
    scrivi_nuovo(fj, out)


# ====================================================================== (1) NEWTON
def stato(nome):
    """### **`(psi, mu, json)` dello stato di `nome`;** ### **lo sha1 DEVE coincidere.**"""
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome)
    if not os.path.exists(fj):
        return None
    cj = leggi(fj)
    with np.load(os.path.join(DIR_NPZ, "fermo_%s.npz" % nome)) as fe:
        psi, mu = fe["psi_h"].copy(), float(fe["mu"])
    assert SFM.sha(psi) == cj["sha"], "lo stato di %s sul disco NON e' quello della ricerca" % nome
    return psi, mu, cj


def conf(nome):
    """### **`(r, g, N)`: una ripresa ha quelli della configurazione che riprende.**"""
    return CONFIG[RIPRESE[nome]["come"]] if nome in RIPRESE else CONFIG[nome]


def partenza(nome):
    import _modo_al_variare_di_s as MS
    N = conf(nome)[2]
    da_chi = RIPRESE[nome]["partenza"] if nome in RIPRESE else PARTENZA[nome]
    if da_chi is None:
        p0, _mu, cj, ok = MS.carica("S1_s0.150")
        assert ok, "dfb5ab7e"
        da = "dfb5ab7e (sha1 %s)" % cj["sha"][:8]
    else:
        st = stato(da_chi)
        assert st is not None, "manca lo stato di partenza %s" % da_chi
        p0 = st[0]
        da = "%s (sha1 %s)" % (da_chi, st[2]["sha"][:8])
    return p0 * math.sqrt(N / float(np.sum(np.abs(p0) ** 2))), da


def newton(r, g, N, p0, etichetta, passi):
    """### **Il metodo di `_strada_b_r.cerca`, invariato, coi contesti della configurazione.**"""
    from scipy.sparse.linalg import LinearOperator, gmres
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    with scena(N) as (_rec, z, phi0, _p), configurazione(r, g):
        A = DV.matrice(z, phi0, DV.AMP) * np.exp(-1j * MS.ALPHA0[FORMA] * S)
        L = z["L"]
        n = z["inc"].n
        Nn = float(np.sum(np.abs(p0) ** 2))
        fo = p0.shape
        m = p0.size

        def T(psi):
            return MS.tick(z, phi0, psi, FORMA)
        lam = complex(np.vdot(p0, T(p0)) / np.vdot(p0, p0))
        mu = -math.atan2(lam.imag, lam.real) / S

        def da_x(x):
            return (x[:m] + 1j * x[m:2 * m]).reshape(fo), float(x[2 * m])

        def F(x):
            psi, mu_ = da_x(x)
            R = (T(psi) - np.exp(-1j * mu_ * S) * psi).ravel() / math.sqrt(Nn)
            return np.concatenate([R.real, R.imag, [(float(np.sum(np.abs(psi) ** 2)) - Nn) / Nn]])

        def residuo(psi, mu_):
            return float(np.linalg.norm(T(psi) - np.exp(-1j * mu_ * S) * psi) / np.linalg.norm(psi))

        x = np.concatenate([p0.ravel().real, p0.ravel().imag, [mu]])
        F0 = F(x)
        storia = [{"passo": 0, "residuo": residuo(p0, mu), "mu": mu, "gmres": 0, "dimezzamenti": 0}]
        print("  %s: passo 0, residuo %.3e, mu %+.9f" % (etichetta, storia[0]["residuo"], mu))
        sys.stdout.flush()
        s0 = time.time()
        migliore = (storia[0]["residuo"], p0.copy(), mu)
        for it in range(1, passi + 1):
            if storia[-1]["residuo"] < SB.TOLL_RES:
                break
            nx = float(np.linalg.norm(x))
            B = np.linalg.inv(A - np.exp(-1j * float(x[2 * m]) * S) * np.eye(12))
            conti = [0]

            def prec(y):
                c = (y[:m] + 1j * y[m:2 * m]).reshape(n, 12)
                f = np.fft.fft2(c.reshape(L, L, 12), axes=(0, 1))
                gg = np.fft.ifft2(np.einsum("abij,abj->abi", B, f), axes=(0, 1)).reshape(-1)
                return np.concatenate([gg.real, gg.imag, [y[2 * m]]])

            def jv(y):
                v = prec(y)
                nv = float(np.linalg.norm(v))
                if nv == 0.0:
                    return np.zeros_like(v)
                h = MS.H_REL * (1.0 + nx) / nv
                conti[0] += 1
                return (F(x + h * v) - F(x - h * v)) / (2.0 * h)
            Aop = LinearOperator((2 * m + 1, 2 * m + 1), matvec=jv, dtype=float)
            y, _info = gmres(Aop, -F0, rtol=MS.GMRES_RTOL, restart=MS.GMRES_RESTART, maxiter=MS.GMRES_MAXITER)
            dx = prec(y)
            nf0 = float(np.linalg.norm(F0))
            passo, k = 1.0, 0
            while True:
                xn = x + passo * dx
                Fn = F(xn)
                if float(np.linalg.norm(Fn)) < nf0 or k >= MS.DIMEZZA:
                    break
                passo *= 0.5
                k += 1
            x, F0 = xn, Fn
            psi, mu = da_x(x)
            storia.append({"passo": it, "residuo": residuo(psi, mu), "mu": mu, "gmres": conti[0], "dimezzamenti": k})
            if storia[-1]["residuo"] < migliore[0]:
                migliore = (storia[-1]["residuo"], psi.copy(), mu)
            print("  %s: passo %d, residuo %.3e, mu %+.9f, GMRES %d, dimezzamenti %d (%.0f s)" % (etichetta, it, storia[-1]["residuo"], mu, conti[0], k, time.time() - s0))
            sys.stdout.flush()
        _rm, psi, mu = migliore
        psi = psi * math.sqrt(Nn / float(np.sum(np.abs(psi) ** 2)))
        rf = residuo(psi, mu)
    return psi, mu, rf, storia, time.time() - s0


def cerca(nome):
    """### **La ricerca diretta; se non converge, UNA tappa a meta' strada** *(`r` e `g` a meta' fra `r 1`, `g 1` e la destinazione, dalla stessa partenza)*; ### **altrimenti lo stato migliore, dichiarato.**"""
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome)
    assert not os.path.exists(fj), fj
    r, g, N = conf(nome)
    p0, da = partenza(nome)
    print("  %s: r %.2f g %.2f N %.0e; la partenza %s, riscalata alla norma" % (nome, r, g, N, da))
    tentativi = []
    rip = RIPRESE.get(nome)
    if rip is not None and rip["tappa_N"] is not None:
        # ### la tappa in N (Luca 13:22): dalla partenza riscalata a tappa_N, poi la destinazione dallo stato della tappa riscalato; ### la tappa resta IN MEMORIA
        Nt = rip["tappa_N"]
        print("  %s: la tappa a N %.0e (non si scrive su disco)" % (nome, Nt))
        pt, mut, rft, stt, sect = newton(r, g, Nt, p0 * math.sqrt(Nt / N), "%s-tappa-N" % nome, SB.MAX_NEWTON)
        tentativi.append({"via": "tappa N %.0e" % Nt, "residuo": rft, "mu": mut, "passi": len(stt) - 1, "storia": stt, "secondi": sect})
        p0 = pt * math.sqrt(N / float(np.sum(np.abs(pt) ** 2)))
        da = "%s, poi la tappa a N %.0e (residuo %.3e)" % (da, Nt, rft)
    passi = rip["passi"] if (rip is not None and rip["passi"] is not None) else SB.MAX_NEWTON
    psi, mu, rf, storia, sec = newton(r, g, N, p0, nome, passi)
    tentativi.append({"via": "diretta" if rip is None else "dalla tappa N" if rip["tappa_N"] is not None else "ripresa, al piu' %d passi" % passi, "residuo": rf, "passi": len(storia) - 1, "storia": storia, "secondi": sec})
    if rf >= SB.TOLL_RES and rip is None and PARTENZA[nome] is None:
        rm, gm = 0.5 * (1.0 + r), 0.5 * (1.0 + g)
        print("  %s: la diretta NON converge (%.3e): la tappa a meta' strada r %.2f g %.2f" % (nome, rf, rm, gm))
        pm, mum, rfm, stm, secm = newton(rm, gm, N, p0, "%s-tappa" % nome, SB.MAX_NEWTON)
        tentativi.append({"via": "tappa r %.3f g %.3f" % (rm, gm), "residuo": rfm, "passi": len(stm) - 1, "storia": stm, "secondi": secm})
        psi2, mu2, rf2, st2, sec2 = newton(r, g, N, pm, "%s-dalla-tappa" % nome, SB.MAX_NEWTON)
        tentativi.append({"via": "dalla tappa", "residuo": rf2, "passi": len(st2) - 1, "storia": st2, "secondi": sec2})
        if rf2 < rf:
            psi, mu, rf = psi2, mu2, rf2
    os.makedirs(DIR_NPZ, exist_ok=True)
    tmp = os.path.join(DIR_NPZ, "fermo_%s_tmp.npz" % nome)
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, os.path.join(DIR_NPZ, "fermo_%s.npz" % nome))
    riga = {"nome": nome, "r": r, "g": g, "N": N, "partenza": da, "mu": mu, "residuo_finale": rf, "convergito": rf < SB.TOLL_RES, "sha": SFM.sha(psi), "tentativi": tentativi}
    scrivi_nuovo(fj, riga)
    print("  %s: residuo finale %.3e, mu %+.9f; %s" % (nome, rf, mu, "CONVERGE" if rf < SB.TOLL_RES else "NON CONVERGE: lo stato migliore, dichiarato"))


# ====================================================================== (2) LE CORSE BREVI
def breve(nome):
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    fj = os.path.join(DIR_JSON, "breve_%s.json" % nome)
    assert not os.path.exists(fj), fj
    r, g, N = conf(nome)
    psi0, mu, cj = stato(nome)
    with scena(N) as (_rec, z, phi0, _p), configurazione(r, g):
        Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))[1]
        n0 = float(np.linalg.norm(psi0))
        Q0, M0 = ML.q_s(psi0)
        t_fine = int(round(T_BREVE / S))
        ogni = int(round(PASSO_BREVE / S))
        psi = psi0.copy()
        t3, nD3, t5, nD5, Ds, cons = [], [], [], [], {}, 0.0
        s0 = time.time()
        for t in range(1, t_fine + 1):
            psi = MS.tick(z, phi0, psi, FORMA)
            if t % OGNI_D == 0 or t % ogni == 0:
                D = np.exp(1j * mu * S * t) * psi - psi0
                nd = float(np.linalg.norm(D)) / n0
                if t % ogni == 0:
                    t3.append(t)
                    nD3.append(nd)
                    Q, M = ML.q_s(psi)
                    cons = max(cons, abs(Q - Q0) / M0, abs(M - M0) / M0)
                if t % OGNI_D == 0:
                    t5.append(t)
                    nD5.append(nd)
                    Ds[t] = D.astype(np.complex64).astype(np.complex128)
        sec = time.time() - s0
        print("  %s: %d tick in %.0f s; Q_S e M entro %.1e" % (nome, t_fine, sec, cons))
        riga = {"nome": nome, "r": r, "g": g, "N": N, "s": S, "sha": cj["sha"], "residuo": cj["residuo_finale"], "convergito": cj["convergito"], "mu": mu, "dn": cons,
                "t": t3, "nD": nD3, "t5": t5, "nD5": nD5, "secondi": sec}
        riga.update(SL.giudica(riga))
        att = cj["residuo_finale"] / S
        an = ML.analizza(t5, nD5, sorted(Ds), Ds, S, psi0, ML.Bande(Z, z["L"]), MS.Vista(z, psi0), lambda x: FATTORE_DEROGA * att * max(x, S), nome)
        riga["analisi"] = an
    scrivi_nuovo(fj, riga)
    stampa_breve(riga)


def stampa_breve(fr):
    SL.stampa_forma(dict(fr, dove={}))
    an = fr["analisi"]
    if an.get("finestra") is None:
        print("    l'esame (5f06dbfb): nessuna finestra fra 10 volte la deriva attesa e 1e-2")
        return
    ML.stampa({"analisi": an, "s": fr["s"], "r": fr["r"], "mu": fr["mu"], "residuo": fr["residuo"], "alpunto": True, "confronti": 0, "cons": fr["dn"], "t": fr["t5"], "nD": fr["nD5"]})
    if an.get("rotazioni"):
        ro = an["rotazioni"]
        print("    IL PERIODO (le rotazioni per banda; D campionato ogni %d tick, %.2f unita' di tempo): 2 pi/|rot| medio %.3f; il periodo dai cambi di segno qui sopra NON entra nelle letture (l'integrazione delle 10:06)"
              % (OGNI_D, OGNI_D * fr["s"], 2.0 * math.pi / ((abs(ro["P0"]["media"]) + abs(ro["Ppi"]["media"])) / 2.0)))


# ====================================================================== (3) LA CORSA LUNGA
def lunga():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    nome = "R_1e6"
    r, g, N = CONFIG[nome]
    f_stato = os.path.join(DIR_NPZ, "lunga_%s.npz" % nome)
    psi0, mu, _cj = stato(nome)
    with scena(N) as (rec, z, phi0, _p), configurazione(r, g):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))[1]
        bande = ML.Bande(Z, z["L"])
        n0 = float(np.linalg.norm(psi0))
        t0 = 0
        punti, dd = [], []
        if os.path.exists(f_stato):
            with np.load(f_stato) as dati:
                t0 = int(dati["t"])
                z["st"]["psi_h"][...] = dati["psi_h"]
            prec = leggi(os.path.join(DIR_JSON, "lunga_%s_%05d.jsonl" % (nome, t0 - PEZZO)))
            assert prec["sha_fine"] == SFM.sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
        elif os.path.exists(os.path.join(DIR_JSON, "lunga_%s_%05d.jsonl" % (nome, 0))):
            # ### NESSUNO STATO DI RIPRESA ma pezzi gia' scritti (Luca 16:00: la ripresa a 4000 scartata): lo stato si RICOSTRUISCE
            # ### da psi0 in memoria, e alla fine di ogni pezzo esistente lo sha DEVE essere il suo sha_fine
            z["st"]["psi_h"][...] = psi0
            while os.path.exists(os.path.join(DIR_JSON, "lunga_%s_%05d.jsonl" % (nome, t0))):
                prec = leggi(os.path.join(DIR_JSON, "lunga_%s_%05d.jsonl" % (nome, t0)))
                with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                    CL.avanza(z, phi0, prec["t1"] - t0)
                assert prec["sha_fine"] == SFM.sha(z["st"]["psi_h"]), "lo stato ricostruito a %d NON e' la fine del pezzo %05d" % (prec["t1"], t0)
                print("  la corsa lunga %s: lo stato ricostruito a tick %d = sha_fine del pezzo %05d (%s)" % (nome, prec["t1"], t0, prec["sha_fine"][:8]))
                t0 = prec["t1"]
        else:
            z["st"]["psi_h"][...] = psi0
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                p = CL.punto(z, 0, w_in, w0)
            p["tau"] = 0.0
            punti.append(p)
        if t0 >= T_MAX:
            print("  la corsa lunga %s: finita" % nome)
            return
        t1 = min(t0 + PEZZO, T_MAX)
        s0 = time.time()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(t0 + 1, t1 + 1):
                CL.avanza(z, phi0, 1)
                if t % OGNI == 0:
                    p = CL.punto(z, t, w_in, w0)
                    p["tau"] = t * S
                    punti.append(p)
                if t % OGNI_LUNGA_D == 0:
                    D = np.exp(1j * mu * S * t) * z["st"]["psi_h"] - psi0
                    c = bande.coeff(D)
                    pk = np.abs(c) ** 2
                    tot = float(pk.sum())
                    dd.append({"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}})
        riga = {"nome": nome, "r": r, "g": g, "N": N, "t0": t0, "t1": t1, "s": S, "w0": w0, "w_in": w_in, "punti": punti, "D": dd, "sha_fine": SFM.sha(z["st"]["psi_h"]), "secondi": time.time() - s0}
        scrivi_nuovo(os.path.join(DIR_JSON, "lunga_%s_%05d.jsonl" % (nome, t0)), riga)
        tmp = os.path.join(DIR_NPZ, "lunga_%s_tmp.npz" % nome)
        np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
        os.replace(tmp, f_stato)
    print("  la corsa lunga %s: tick %d -> %d, w/w_in %.5f, cuore %.5f, |D|/|psi0| %.3e (%.0f s)" % (nome, t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], dd[-1]["nD"], riga["secondi"]))


# ====================================================================== IL REFERTO
# ====================================================================== IL CRITERIO AGGIUNTO DELLA FORMA (Luca 13:22, punto 6)
def forma_pendenze(tau, nD):
    """### **Le pendenze locali `l = d ln|D|/dt`** *(`np.gradient`, come le stampa `SL.stampa_forma`)* **sui campioni sotto la saturazione, esclusi il primo e l'ultimo; il fit `l = gamma + b/t`:**
    ### **ESPONENZIALE se `gamma - SIGMA_FORMA sigma_gamma > 0` e `gamma t_ultimo > 1`; altrimenti la potenza `t^b`, LINEARE se `b` arrotondato e' `1`** *(il task history, `6-pre`)*."""
    loc = np.gradient(np.log(nD), tau)
    idx = [i for i in range(1, len(nD) - 1) if nD[i] < SL.SATURAZIONE]
    if len(idx) < 3:
        return {"forma": None, "campioni": len(idx)}
    t, ll = tau[idx], loc[idx]
    X = np.column_stack([np.ones_like(t), 1.0 / t])
    coef = np.linalg.lstsq(X, ll, rcond=None)[0]
    res = ll - X @ coef
    cov = float(res @ res) / max(len(t) - 2, 1) * np.linalg.inv(X.T @ X)
    g, b = float(coef[0]), float(coef[1])
    sg, sb = float(np.sqrt(cov[0, 0])), float(np.sqrt(cov[1, 1]))
    if g - SIGMA_FORMA * sg > 0 and g * float(t[-1]) > 1.0:
        f = "esponenziale"
    else:
        f = "lineare" if int(round(b)) == 1 else "potenza t^%d" % int(round(b))
    return {"forma": f, "gamma": g, "sigma_gamma": sg, "b": b, "sigma_b": sb, "t_ultimo": float(t[-1]), "campioni": len(idx)}


def stampa_pendenze(fn, vecchia):
    if fn["forma"] is None:
        print("    LA FORMA, IL CRITERIO AGGIUNTO: %d campioni utili sotto %.0e: non si giudica" % (fn["campioni"], SL.SATURAZIONE))
        return
    print("    LA FORMA, IL CRITERIO AGGIUNTO: %s -- l = gamma + b/t su %d campioni: gamma %.5f +- %.5f, gamma t_ultimo %.3f (t_ultimo %.1f), b %.4f +- %.4f; il vecchio alla lettera: %s"
          % (fn["forma"].upper(), fn["campioni"], fn["gamma"], fn["sigma_gamma"], fn["gamma"] * fn["t_ultimo"], fn["t_ultimo"], fn["b"], fn["sigma_b"], vecchia))


def collaudo_forma():
    """### **Il collaudo, PRIMA dei casi** *(`P1-sexies`; il task history `6-pre`)*: sulla griglia `t = 3 .. 300` ogni `3`; ### **i campioni con `|D| <= 0` tolti** *(il caso con l'intercetta negativa scritto nel task history e' negativo per `t < 5.07`: annotato)*."""
    tau = np.arange(1, int(round(T_BREVE / PASSO_BREVE)) + 1) * PASSO_BREVE
    casi = (("|D| = 1e-8 t", 1e-8 * tau, "lineare"),
            ("|D| = -1.774e-8 + 3.502e-9 t (i numeri di breve_R_1e6; il caso che il criterio vecchio sbaglia)", -1.774e-8 + 3.502e-9 * tau, "lineare"),
            ("|D| = 1e-8 e^{0.06 t}", 1e-8 * np.exp(0.06 * tau), "esponenziale"),
            ("|D| = 1e-8 (t + e^{0.0331 t}) (il tasso del modo lento col seme lineare)", 1e-8 * (tau + np.exp(0.0331 * tau)), "esponenziale"),
            ("|D| = 1e-8 (il caso nullo: niente cresce)", 1e-8 + 0.0 * tau, "potenza t^0"))
    for nome, y, atteso in casi:
        m = y > 0
        fn = forma_pendenze(tau[m], y[m])
        esito("DEVE dare %s: %s" % (atteso.upper(), nome), fn["forma"] == atteso,
              "%s; %d campioni > 0; gamma %.5f +- %.5f, gamma t_ultimo %.3f, b %.4f +- %.4f" % (fn["forma"], int(m.sum()), fn["gamma"], fn["sigma_gamma"], fn["gamma"] * fn["t_ultimo"], fn["b"], fn["sigma_b"]))


def referto():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    print("=" * 130)
    print("LA REGOLA DEI LIVELLI PIATTI E LA PROVA DI UN SOLITONE CHE LA RISPETTA (Luca 09:31, integrazione 09:33; UNA PROVA): S1, s %g, eps 0, il congelato vero; a_n = pi, b_a = r pi, alpha = g x^2/(1+x^2)" % S)
    print("=" * 130)
    print("  la configurazione: CONFIG %s PARTENZA %s W_LISTA %s L_SCENA %d FRAZ_LARGO %.4f T_BREVE %g PASSO_BREVE %g OGNI_D %d FATTORE_DEROGA %g T_MAX %d PEZZO %d OGNI %d OGNI_LUNGA_D %d FINESTRA %g TOLL_NORMA %g TOLL_RICOMPOSTO %g; da _strada_b_r: MAX_NEWTON %d TOLL_RES %g"
          % (CONFIG, PARTENZA, W_LISTA, L_SCENA, FRAZ_LARGO, T_BREVE, PASSO_BREVE, OGNI_D, FATTORE_DEROGA, T_MAX, PEZZO, OGNI, OGNI_LUNGA_D, FINESTRA, TOLL_NORMA, TOLL_RICOMPOSTO, SB.MAX_NEWTON, SB.TOLL_RES))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (p1) le tre (R) senza modo esponenziale e le due (X) col modo previsto: la regola confermata, la forma generale confermata per n = 1 e n = 2;"
          " (p2) una (R) decade: la regola incompleta (quale uscita; quale termine della forma generale manca); (p3) una (X) non decade: troppo severa (di quanto; quale termine);"
          " (p4) nella corsa lunga (R) il cuore regge o si svuota lentamente (dove va D)")
    print("-" * 130)
    fp = os.path.join(DIR_JSON, "previsioni.json")
    prev = leggi(fp) if os.path.exists(fp) else None
    print("### (0) LE PREVISIONI (scritte prima di Newton: previsioni.json)")
    if prev:
        for nome, c in prev["configurazioni"].items():
            for tipo in ("primo", "tick"):
                lv = c["livelli"][tipo]
                print("  %-6s [%s] J [%+.4f, %+.4f]; %s; il margine %+.4f" % (nome, tipo, lv["J"][0], lv["J"][1], "; ".join("%s %s %.4f" % (k, v[1], v[0]) for k, v in lv["distanze"].items()), lv["margine"]))
            print("  %-6s la massa %.4f di r 1; mu0 %.5f" % (nome, c["curvatura_su_r1"], c["mu0_tick"]))
    print("-" * 130)
    print("### (1) GLI STATI FERMI")
    stati = {}
    for nome in list(CONFIG) + list(RIPRESE):
        r, g, N = conf(nome)
        st = stato(nome)
        if st is None:
            print("  %s: nessuna ricerca" % nome)
            continue
        psi, mu, cj = st
        esito("DEVE PASSARE: %s, lo stato sul disco = la ricerca (sha1)" % nome, True, "")
        for tt in cj["tentativi"]:
            print("  %s, %s: %d passi, residuo %.3e; la storia %s" % (nome, tt["via"], tt["passi"], tt["residuo"], " ".join("%.1e" % p["residuo"] for p in tt["storia"])))
        with scena(N) as (rec, z, phi0, _p), configurazione(r, g):
            w0 = rec["larghezza"]
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                w_in = DC.forma(z, w0)[0]
                z["st"]["psi_h"][...] = psi
                pt = CL.punto(z, 0, w_in, w0)
            cp = RIPRESE[nome]["come"] if nome in RIPRESE else nome
            P0, Ppi = (prev["configurazioni"][cp]["P0"], prev["configurazioni"][cp]["Ppi"]) if prev else (None, None)
            _ra, am = SL.anelli(z, psi, FORMA)
            print("  %s: %s (residuo %.3e), mu %+.9f; la partenza %s; w %.3f (L/6 %.2f: %s; w/L %.3f, il bordo del toro), cuore f_win %.5f, picco %.2f; alpha del cuore %.5f (g %.2f), della coda %.5f"
                  % (nome, "FERMO" if cj["convergito"] else "NON FERMO, lo stato migliore", cj["residuo_finale"], mu, cj["partenza"], pt["w"], L_SCENA * FRAZ_LARGO,
                     "dentro" if pt["w"] <= L_SCENA * FRAZ_LARGO else "### OLTRE: L 120", pt["w"] / L_SCENA, pt["f_win"], pt["picco"], float(am[0]), g, float(am[SL.R_MAX])))
            if P0 is not None:
                inc, _ra = SL.conto(nome, z, phi0, S, FORMA, r, psi, mu, P0, Ppi)
                stati[nome] = {"inc": inc, "alpha_cuore": float(am[0])}
    print("-" * 130)
    print("### (2-pre) IL CRITERIO AGGIUNTO DELLA FORMA (Luca 13:22, punto 6; scritto nel task history PRIMA dei casi): le pendenze locali d ln|D|/dt contro 1/t, il fit l = gamma + b/t;"
          " ESPONENZIALE se gamma - %g sigma > 0 e gamma t_ultimo > 1, altrimenti la potenza t^b (LINEARE se b arrotondato e' 1)" % SIGMA_FORMA)
    collaudo_forma()
    print("### (2) LE CORSE BREVI (%g unita' di tempo)" % T_BREVE)
    brevi = {}
    for nome in list(CONFIG) + list(RIPRESE):
        fj = os.path.join(DIR_JSON, "breve_%s.json" % nome)
        if not os.path.exists(fj):
            print("  %s: nessuna corsa breve" % nome)
            continue
        fr = leggi(fj)
        esito("DEVE PASSARE: %s, Q_S e M conservate entro %g nella corsa breve" % (nome, TOLL_NORMA), fr["dn"] < TOLL_NORMA, "%.1e" % fr["dn"])
        print("  --- %s (r %.2f, g %.2f, N %.0e)" % (nome, fr["r"], fr["g"], fr["N"]))
        stampa_breve(fr)
        fr["forma_nuova"] = forma_pendenze(np.array(fr["t"], dtype=float) * fr["s"], np.array(fr["nD"]))
        stampa_pendenze(fr["forma_nuova"], fr.get("forma"))
        brevi[nome] = fr
    print("  NOTA (Luca 16:26, senza lettura nuova): X1 decade per la coppia col tasso 0.061 (a g 1, r 1: 0.151): un indizio che la larghezza W scali col legame g")
    print("-" * 130)
    print("### (3) LA CORSA LUNGA (R_1e6)")
    righe = sorted([leggi(os.path.join(DIR_JSON, n)) for n in os.listdir(DIR_JSON) if n.startswith("lunga_R_1e6_") and n.endswith(".jsonl")] if os.path.isdir(DIR_JSON) else [], key=lambda x: x["t0"])
    if not righe:
        print("  nessuna corsa lunga")
    else:
        for x, y in zip(righe, righe[1:]):
            assert x["t1"] == y["t0"], ("un buco fra i pezzi", x["t1"], y["t0"])
        pts = [p for x in righe for p in x["punti"]]
        dd = [d for x in righe for d in x["D"]]
        print("  R_1e6: %d pezzi, tick %d -> %d%s" % (len(righe), righe[0]["t0"], righe[-1]["t1"], "" if righe[-1]["t1"] == T_MAX else " (NON FINITA)"))
        dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
        esito("DEVE PASSARE: R_1e6, M entro %g relativo nella corsa lunga" % TOLL_NORMA, dM <= TOLL_NORMA, "%.1e" % dM)
        rif = [leggi(os.path.join(SFM.PUNTI, n)) for n in sorted(os.listdir(SFM.PUNTI)) if n.startswith("corsa_L81_") and n.endswith(".jsonl")]
        rp = {round(p["t"] * SFM.S, 6): p["f_win"] for rr in rif for p in rr["punti"]}
        alto = [leggi(os.path.join(SB.DIR_JSON, n)) for n in sorted(os.listdir(SB.DIR_JSON)) if n.startswith("lunga_r1.52_") and n.endswith(".jsonl")]
        ra = {round(p["tau"], 6): p["f_win"] for rr in alto for p in rr["punti"]}

        def vicino(dz, x):
            if not dz:
                return float("nan")
            k = min(dz, key=lambda y: abs(y - x))
            return dz[k]
        w_in = righe[0]["w_in"]
        tau = np.array([p["tau"] for p in pts])
        q = np.array([p["w"] / w_in for p in pts])
        cu = np.array([p["f_win"] for p in pts])
        al = np.array([1.0 - p["f_3w0"] for p in pts])
        pk = np.array([p["picco"] / pts[0]["picco"] for p in pts])
        td = np.array([d["t"] * S for d in dd])
        a0 = 0.0
        while a0 < tau[-1] - 1e-9:
            m = (tau >= a0 - 1e-9) & (tau <= a0 + FINESTRA + 1e-9)
            md = (td >= a0 - 1e-9) & (td <= a0 + FINESTRA + 1e-9)
            ultimo = [dd[i] for i in np.nonzero(md)[0]][-1] if md.any() else None
            print("  tau [%5.0f, %5.0f]: w/w_in %.5f -> %.5f; cuore %.5f -> %.5f (pendenza %+.3e); alone %.5f -> %.5f; picco medio %.5f | r 1 (26300537) cuore %.5f -> %.5f | r 1.5247 cuore %.5f -> %.5f | D a fine finestra %s"
                  % (a0, a0 + FINESTRA, q[m][0], q[m][-1], cu[m][0], cu[m][-1], np.polyfit(tau[m], cu[m], 1)[0], al[m][0], al[m][-1], pk[m].mean(),
                     vicino(rp, a0), vicino(rp, a0 + FINESTRA), vicino(ra, a0), vicino(ra, a0 + FINESTRA),
                     ("%.3e (%s)" % (ultimo["nD"], "  ".join("%s %.3f" % kv for kv in ultimo["bande"].items()))) if ultimo else "--"))
            a0 += FINESTRA
    print("-" * 130)

    def modo(nome, quale):
        an = brevi[nome]["analisi"]
        ist = an.get("istanti") or {}
        ist = {k: ist[k] for k in sorted(ist, key=int)[:-1]}          # ### l'integrazione delle 10:06: l'istante al bordo alto (la saturazione) non entra
        if not ist:
            return None
        if quale == "coppia":
            return all(x["bande"]["P0"] + x["bande"]["Ppi"] > x["bande"]["A"] + x["bande"]["B"] for x in ist.values())
        return all(x["bande"]["P0"] > x["bande"]["Ppi"] + x["bande"]["A"] + x["bande"]["B"] for x in ist.values())
    print("### LE LETTURE, COI CRITERI SCRITTI PRIMA (la forma: il criterio aggiunto delle 13:22; quello vecchio, alla lettera, accanto)")
    scelta = {k: next((n for n in v if n in brevi), None) for k, v in LETTURA.items()}
    for k, n in scelta.items():
        if n is None:
            print("  %s: nessuna corsa breve" % k)
            continue
        fn, fv = brevi[n]["forma_nuova"]["forma"], brevi[n].get("forma")
        extra = "; il modo previsto (la coppia) agli istanti: %s" % modo(n, "coppia") if k == "X1" else "; il modo previsto (P0 da sola) agli istanti: %s" % modo(n, "P0") if k == "X2" else ""
        print("  %s: si legge %s (stato %s); la forma, il criterio aggiunto: %s; il vecchio alla lettera: %s%s%s"
              % (k, n, "FERMO" if brevi[n]["convergito"] else "NON FERMO", fn, fv, extra, "" if (fn is None or fv is None or fn == fv) else "   ### I DUE CRITERI DANNO FORME DIVERSE"))
    giudicate = all(scelta[k] is not None and brevi[scelta[k]]["forma_nuova"]["forma"] is not None for k in LETTURA)
    esp = {k: brevi[n]["forma_nuova"]["forma"] == "esponenziale" for k, n in scelta.items() if n is not None}
    if not giudicate:
        print("  LA LETTURA: NON SI FA -- una configurazione senza breve o con la forma che non si giudica: %s"
              % [k for k in LETTURA if scelta[k] is None or brevi[scelta[k]]["forma_nuova"]["forma"] is None])
    else:
        r_ok = not any(esp[k] for k in LETTURA if k.startswith("R_"))
        x_ok = esp["X1"] and esp["X2"] and modo(scelta["X1"], "coppia") and modo(scelta["X2"], "P0")
        print("  LA LETTURA: %s" % ("(p1)" if (r_ok and x_ok) else " ".join(x for x, c in (("(p2)", not r_ok), ("(p3)", not x_ok)) if c)))
    print("-" * 130)
    print("### LE LETTURE COL SOLO CRITERIO VECCHIO, ALLA LETTERA (stampate come prima; NON usate)")
    esp = {nome: (fr["forma"] == "esponenziale") for nome, fr in brevi.items()}
    for nome in CONFIG:
        if nome not in brevi:
            continue
        extra = ""
        if nome == "X1":
            extra = "; il modo previsto (la coppia) agli istanti: %s" % modo(nome, "coppia")
        if nome == "X2":
            extra = "; il modo previsto (P0 da sola) agli istanti: %s" % modo(nome, "P0")
        print("  %s: la forma %s%s" % (nome, brevi[nome]["forma"], extra))
    if all(k in brevi for k in CONFIG):
        r_ok = not any(esp[k] for k in CONFIG if k.startswith("R_"))
        x_ok = esp["X1"] and esp["X2"] and modo("X1", "coppia") and modo("X2", "P0")
        print("  LA LETTURA: %s" % ("(p1)" if (r_ok and x_ok) else " ".join(x for x, c in (("(p2)", not r_ok), ("(p3)", not x_ok)) if c)))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        if argv == ["--referto"]:
            referto()
        elif argv == ["--previsioni"]:
            previsioni()
        elif argv == ["--lunga"]:
            lunga()
        elif argv == ["--collaudo-forma"]:
            collaudo_forma()
            print("%d/%d PASSANO; fallite: %s" % (OK[0], OK[1], FALLITE))
            return 0 if OK[0] == OK[1] else 1
        elif argv[:1] in (["--cerca"], ["--breve"]) and len(argv) == 2:
            assert argv[1] in CONFIG or argv[1] in RIPRESE, argv[1]
            {"--cerca": cerca, "--breve": breve}[argv[0]](argv[1])
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
