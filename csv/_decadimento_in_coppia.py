# -*- coding: utf-8 -*-
r"""**IL DECADIMENTO IN COPPIA** *(il mandato di Luca delle `13:02` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_decadimento_in_coppia.md`)*:
### **(1)** i conti: `x alpha'(x)` per anello, la fase della coppia a `K` per `s` piccolo, `2 - pi - 2 mu`;
### **(2)** il filtro su UNA piatta sola *(`P0` o `Ppi`)*, `S1` `s 0.3`, `600` tick; ### **(3)** Newton ripreso a `s 0.075` e, se converge, il tasso.

> ### **Lo stato ripreso in `db/modo_s/`** *(ignorato: il dato e' il comando)*; ### **la storia in `doc/referti_l2/modo_s/`.**

    python csv/_decadimento_in_coppia.py --cerca
    python csv/_decadimento_in_coppia.py --referto > doc/referti_l2/decadimento_in_coppia.txt
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

CASI_XA = ("S1_s0.300", "S1_s0.150")
S_FASE = (0.3, 0.15, 0.075, 0.0375)
R_MAX = 24
ANELLI_MODO = (12, 13)
FILTRI = (("solo P0", (6, 7, 8, 9)), ("solo Ppi", (0, 1, 2, 3)))
T_FILTRO = 600
CASO_075 = "S1_s0.075"
NOME_RIPRESO = "S1_s0.075_ripreso"
MAX_NEWTON = 60
TOLL_RES = 1e-9
FATTORE_RUMORE = 1e3           # ### la finestra di dfb5ab7e
TOLL_ACC = 1e-6
TOLL_NORMA = 1e-10
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


def conto_xa(nome):
    import _diagnosi_s4 as D
    import _energia_del_legame as EL
    import _modo_al_variare_di_s as MS
    import _screening_forme_s3 as SF
    _n, forma, s, N = MS.caso(nome)
    psi0, mu, cj, ok = MS.carica(nome)
    esito("DEVE PASSARE: %s, lo stato fermo = la ricerca (sha1), e fermo" % nome, ok and cj["convergito"], "%.3e" % cj["residuo_finale"])
    with D.configura(forma, s, N):
        _rec, z, _phi0, _p = MS.scena(forma, s, N)
        z["st"]["psi_h"][...] = psi0
        rho, lam = EL.densita(z["inc"], z["st"])
    x = np.where(lam > 0, rho / np.where(lam > 0, lam, 1.0), 0.0)
    xa = SF.acc_mano(forma, x)
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    k = np.floor(np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])).astype(int)
    qn = np.bincount(k)
    xam = np.bincount(k, weights=xa) / np.maximum(qn, 1)
    xm = np.bincount(k, weights=x) / np.maximum(qn, 1)
    r_max = int(np.argmax(xam[:R_MAX + 1]))
    print("  %s: x alpha'(x) medio per anello, r 0..%d: %s" % (nome, R_MAX, " ".join("%.4f" % v for v in xam[:R_MAX + 1])))
    print("  %s: x medio per anello, r 10..16: %s" % (nome, " ".join("r%d %.3g" % (r, xm[r]) for r in range(10, 17))))
    print("  %s: il massimo %.4f all'anello %d; gli anelli del modo %s: %s" % (nome, xam[r_max], r_max, ANELLI_MODO, " ".join("%.4f" % xam[r] for r in ANELLI_MODO)))
    return r_max


def filtro_una(etichetta, indici):
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _filtro_bande_piatte as FB
    import _modo_al_variare_di_s as MS
    nome = "S1_s0.300"
    _n, forma, s, N = MS.caso(nome)
    psi0, mu, cj, ok = MS.carica(nome)
    print("-" * 130)
    print("### (2) IL FILTRO %s: %s, %d tick" % (etichetta.upper(), nome, T_FILTRO))
    with D.configura(forma, s, N):
        _rec, z, phi0, _p = MS.scena(forma, s, N)
        L = MS.L
        n = z["inc"].n
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
        fl = FB.Filtro(Z, L, n)
        fl.tieni = np.ones(12)
        fl.tieni[list(indici)] = 0.0
        M0 = float(np.sum(np.abs(psi0) ** 2))
        psi0f = fl(psi0)
        psi0f *= math.sqrt(M0 / float(np.sum(np.abs(psi0f) ** 2)))
        print("  lo stato fermo filtrato una volta: |psi0f - psi0| / |psi0| %.4e" % (float(np.linalg.norm(psi0f - psi0)) / math.sqrt(M0)))
        ogni = int(round(FB.PASSO_FIS / s))
        t_da = int(round(FB.T_DA_FIS / s))
        psi = psi0.copy()
        Dd, Df = {}, {}
        tolta = []
        for t in range(1, T_FILTRO + 1):
            psi = MS.tick(z, phi0, psi, forma)
            q = fl(psi)
            nt = float(np.sum(np.abs(q) ** 2))
            tolta.append((M0 - nt) / M0)
            psi = q * math.sqrt(M0 / nt)
            if t % ogni == 0 and t >= t_da:
                rot = np.exp(1j * mu * s * t)
                Dd[t] = rot * psi - psi0
                Df[t] = rot * psi - psi0f
        tl = np.array(tolta)
        print("  la norma tolta per tick: il primo %.3e; la media degli ultimi %d tick %.3e; il totale %.4e" % (tl[0], 10 * ogni, float(tl[-10 * ogni:].mean()), float(tl.sum())))
        v = MS.Vista(z, psi0)
    ts = sorted(Dd)
    r1 = cj["residuo_finale"]
    t1 = FB.esame(nome, ts, Df, math.sqrt(M0), r1, s, v, Z, L, "%s, D rispetto a psi0f" % etichetta)
    return t1


def cerca():
    """### **Newton ripreso dallo stato di `dfb5ab7e`** *(il metodo di `_modo_al_variare_di_s.cerca`)*, ### **al piu' `MAX_NEWTON` passi.**"""
    from scipy.sparse.linalg import LinearOperator, gmres
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _stato_fermo as SFM
    _n, forma, s, N = MS.caso(CASO_075)
    p0, mu, cj, ok = MS.carica(CASO_075)
    assert ok, "lo stato di partenza NON e' quello di dfb5ab7e"
    with D.configura(forma, s, N):
        _rec, z, phi0, _p = MS.scena(forma, s, N)
        A = DV.matrice(z, phi0, DV.AMP) * np.exp(-1j * MS.ALPHA0[forma] * s)
        L = MS.L
        n = z["inc"].n
        Nn = float(np.sum(np.abs(p0) ** 2))
        fo = p0.shape
        m = p0.size

        def da_x(x):
            return (x[:m] + 1j * x[m:2 * m]).reshape(fo), float(x[2 * m])

        def F(x):
            psi, mu_ = da_x(x)
            R = (MS.tick(z, phi0, psi, forma) - np.exp(-1j * mu_ * s) * psi).ravel() / math.sqrt(Nn)
            return np.concatenate([R.real, R.imag, [(float(np.sum(np.abs(psi) ** 2)) - Nn) / Nn]])

        def residuo(psi, mu_):
            return float(np.linalg.norm(MS.tick(z, phi0, psi, forma) - np.exp(-1j * mu_ * s) * psi) / np.linalg.norm(psi))

        x = np.concatenate([p0.ravel().real, p0.ravel().imag, [mu]])
        F0 = F(x)
        storia = [{"passo": 0, "residuo": residuo(p0, mu), "mu": mu, "gmres": 0, "dimezzamenti": 0}]
        print("  ripreso: passo 0, residuo %.3e, mu %+.9f" % (storia[0]["residuo"], mu))
        sys.stdout.flush()
        s0 = time.time()
        for it in range(1, MAX_NEWTON + 1):
            if storia[-1]["residuo"] < TOLL_RES:
                break
            nx = float(np.linalg.norm(x))
            B = np.linalg.inv(A - np.exp(-1j * float(x[2 * m]) * s) * np.eye(12))
            conti = [0]

            def prec(y):
                c = (y[:m] + 1j * y[m:2 * m]).reshape(n, 12)
                f = np.fft.fft2(c.reshape(L, L, 12), axes=(0, 1))
                g = np.fft.ifft2(np.einsum("abij,abj->abi", B, f), axes=(0, 1)).reshape(-1)
                return np.concatenate([g.real, g.imag, [y[2 * m]]])

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
            print("  ripreso: passo %d, residuo %.3e, mu %+.9f, GMRES %d, dimezzamenti %d (%.0f s)" % (it, storia[-1]["residuo"], mu, conti[0], k, time.time() - s0))
            sys.stdout.flush()
        psi, mu = da_x(x)
        psi *= math.sqrt(Nn / float(np.sum(np.abs(psi) ** 2)))
        r = residuo(psi, mu)
    os.makedirs(MS.STATI, exist_ok=True)
    f = os.path.join(MS.STATI, "fermo_%s.npz" % NOME_RIPRESO)
    tmp = os.path.join(MS.STATI, "fermo_%s_tmp.npz" % NOME_RIPRESO)
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, f)
    riga = {"caso": NOME_RIPRESO, "partenza_sha": cj["sha"], "forma": forma, "s": s, "N": Nn, "mu": mu, "residuo_finale": r, "storia": storia,
            "secondi": time.time() - s0, "sha": SFM.sha(psi), "convergito": r < TOLL_RES}
    fj = os.path.join(MS.PUNTI, "cerca_%s.json" % NOME_RIPRESO)
    assert not os.path.exists(fj), fj
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    with open(fj, "xb") as fh:
        fh.write(dati)
    print("  ripreso: residuo finale %.3e, mu %+.9f; %s" % (r, mu, "CONVERGE" if r < TOLL_RES else "NON CONVERGE"))


def terzo():
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _filtro_bande_piatte as FB
    import _modo_al_variare_di_s as MS
    import _stato_fermo as SFM
    _n, forma, s, N = MS.caso(CASO_075)
    print("-" * 130)
    print("### (3) NEWTON RIPRESO A s %g (dallo stato di dfb5ab7e, sha1 9744446c), al piu' %d passi" % (s, MAX_NEWTON))
    fj = os.path.join(MS.PUNTI, "cerca_%s.json" % NOME_RIPRESO)
    if not os.path.exists(fj):
        print("  la ricerca e' IN CORSA (python csv/_decadimento_in_coppia.py --cerca): questo referto e' intermedio")
        return None, None
    cj = json.loads(io.open(fj, encoding="utf-8").read())
    fe = np.load(os.path.join(MS.STATI, "fermo_%s.npz" % NOME_RIPRESO))
    print("  la storia: %s" % " ".join("%.1e" % p["residuo"] for p in cj["storia"]))
    esito("DEVE PASSARE: lo stato ripreso sul disco = quello della ricerca (sha1); la partenza = 9744446c", SFM.sha(fe["psi_h"]) == cj["sha"] and cj["partenza_sha"].startswith("9744446c"), "")
    esito("DEVE PASSARE: Newton ripreso a s 0.075 sotto %g" % TOLL_RES, cj["convergito"], "%.3e in %d passi; mu %+.9f" % (cj["residuo_finale"], len(cj["storia"]) - 1, cj["mu"]))
    if not cj["convergito"]:
        return None, cj["mu"]
    psi0, mu = fe["psi_h"].copy(), float(fe["mu"])
    with D.configura(forma, s, N):
        _rec, z, phi0, _p = MS.scena(forma, s, N)
        v = MS.Vista(z, psi0)
        ogni = int(round(MS.PASSO_FIS / s))
        t_fine = int(round(MS.T_FIS / s))
        t_da = int(round(MS.T_DA_FIS / s))
        M0 = float(np.sum(np.abs(psi0) ** 2))
        psi = psi0.copy()
        Dd = {}
        dM = 0.0
        for t in range(1, t_fine + 1):
            psi = MS.tick(z, phi0, psi, forma)
            if t % ogni == 0:
                dM = max(dM, abs(float(np.sum(np.abs(psi) ** 2)) / M0 - 1.0))
                if t >= t_da:
                    Dd[t] = np.exp(1j * mu * s * t) * psi - psi0
        esito("DEVE PASSARE: M conservata nella corsa a s 0.075 entro %g" % TOLL_NORMA, dM < TOLL_NORMA, "%.1e" % dM)
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
    vecchio = FB.FATTORE_RUMORE
    FB.FATTORE_RUMORE = FATTORE_RUMORE
    try:
        t3 = FB.esame(CASO_075, sorted(Dd), Dd, math.sqrt(M0), cj["residuo_finale"], s, v, Z, MS.L, "s 0.075, D rispetto allo stato fermo ripreso")
    finally:
        FB.FATTORE_RUMORE = vecchio
    return t3, mu


def referto():
    import _modo_al_variare_di_s as MS
    import _screening_forme_s3 as SF
    import _triangoli_forza as TF
    print("=" * 130)
    print("IL DECADIMENTO IN COPPIA (Luca 13:02): (1) i conti; (2) il filtro su una piatta sola; (3) Newton ripreso a s 0.075")
    print("=" * 130)
    print("  la configurazione: CASI_XA %s S_FASE %s R_MAX %d ANELLI_MODO %s FILTRI %s T_FILTRO %d CASO_075 %s MAX_NEWTON %d TOLL_RES %g FATTORE_RUMORE %g TOLL_ACC %g TOLL_NORMA %g"
          % (CASI_XA, S_FASE, R_MAX, ANELLI_MODO, FILTRI, T_FILTRO, CASO_075, MAX_NEWTON, TOLL_RES, FATTORE_RUMORE, TOLL_ACC, TOLL_NORMA))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (p1) togliendo una sola piatta il modo non cresce, tutti e due i casi: in coppia; (p2) solo una delle due: un processo di una banda; (p3) nessuna delle due da sola; (p4) altro;"
          " (q1) il massimo di x alpha' negli anelli del modo; (q2) altrove; (b) ph_A(K)/s -> -pi/2 o no; (3) il tasso a s 0.075 contro 0.139 e 0.151")
    print("-" * 130)
    print("### (1a) x alpha'(x)")
    xs = np.array([1e-3, 0.1, 0.5, 1.0, 2.0, 10.0, 1e3])
    h = 1e-4                   # ### a x 1e3 un passo di 1e-6 perde le cifre nella differenza di alpha ~ 1
    fd = (SF._ab("S1", xs * (1 + h))[0] - SF._ab("S1", xs * (1 - h))[0]) / (2 * h)
    sc = float(np.max(np.abs(fd - SF.acc_mano("S1", xs)) / np.maximum(SF.acc_mano("S1", xs), 1e-300)))
    esito("DEVE PASSARE: acc_mano(S1) = x d alpha/dx per differenze di _ab, entro %g" % TOLL_ACC, sc < TOLL_ACC, "%.1e" % sc)
    for nome in CASI_XA:
        conto_xa(nome)
    print("-" * 130)
    print("### (1b) la fase di A a K per tick, divisa per s (coppia_K), contro -pi/2 = %.6f" % (-math.pi / 2))
    prec = None
    for s in S_FASE:
        w = TF.coppia_K(0.0, s)[0]["w"]
        sc = w / s + math.pi / 2
        print("  s %-7g: ph_A(K) %+.9f; / s %+.9f; lo scarto da -pi/2 %+.3e%s" % (s, w, w / s, sc, ("; il rapporto con lo scarto di prima %.4f" % (sc / prec)) if prec else ""))
        prec = sc
    print("-" * 130)
    print("### (1c) 2 - pi - 2 mu (la condizione c2 P0+Ppi nel cuore, alpha = 1, per unita' di tempo)")
    for nome in ("S1_s0.300", "S1_s0.150", "S1_s0.075"):
        _p, mu, cj, _ok = MS.carica(nome)
        print("  %s: mu %+.9f (%s, residuo %.1e); 2 - pi - 2 mu = %+.5f" % (nome, mu, "fermo" if cj["convergito"] else "NON fermo", cj["residuo_finale"], 2 - math.pi - 2 * mu))
    tassi = {}
    for et, idx in FILTRI:
        tassi[et] = filtro_una(et, idx)
    t3, mu3 = terzo()
    print("-" * 130)
    print("### LA SINTESI")
    print("  il filtro, il tasso per unita' di tempo (senza filtro 0.13870; con le due piatte insieme 0.00067): %s" % "; ".join("%s %s" % (k, ("%.5f" % v) if v is not None else "--") for k, v in tassi.items()))
    if mu3 is not None:
        print("  s 0.075 ripreso: mu %+.9f; 2 - pi - 2 mu = %+.5f; il tasso %s (la serie: 0.13870 a s 0.3, 0.15108 a s 0.15)" % (mu3, 2 - math.pi - 2 * mu3, ("%.5f" % t3) if t3 is not None else "--"))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        if argv[:1] == ["--cerca"]:
            cerca()
        elif argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
