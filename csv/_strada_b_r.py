# -*- coding: utf-8 -*-
r"""**LA STRADA (B) CON `r < 1` CURA IL SOLITONE `S1`?** *(UNA DIAGNOSI, NON UNA CURA; il mandato di Luca delle `19:58` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_strada_b_r.md`)*: ### **i pesi del nodo e dell'arco cambiati IN MEMORIA, mai nel nucleo.**
### **`flussi_parziali.z_nodo` e `z_arco` avvolti: la frazione per `a_n/pi` e `b_a/pi`, `a_n = pi/sqrt(1 - r + r^2)`, `b_a = r a_n`** *(`mu0 = pi/2` fisso)*; ### **rimessi all'uscita.**

    python csv/_strada_b_r.py --cerca 0.65 > doc/referti_l2/strada_b/cerca_0.65.txt
    python csv/_strada_b_r.py --breve 0.65 > doc/referti_l2/strada_b/breve_0.65.txt
    python csv/_strada_b_r.py --corsa 0.65            # un pezzo; si ripete fino alla fine
    python csv/_strada_b_r.py --referto > doc/referti_l2/strada_b_r.txt
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

CASO = "S1_s0.150"
R_LISTA = (0.65, 0.69)
R_CARTA = (0.65, 0.69, 1.0)
MAX_NEWTON = 30
TOLL_RES = 1e-9
T_FIS = 180.0
T_DA_FIS = 60.0
PASSO_FIS = 3.0
TASSO_CORSA = 0.02             # ### il mandato: la corsa lunga solo se il tasso breve e' <= 0.02
T_MAX = 20000                  # ### 3000 unita' di tempo a s 0.15
PEZZO = 2000
OGNI = 10
FINESTRA = 500.0
TICK_BIT = 10
TOLL_NORMA = 1e-10
TOLL_RICOMPOSTO = 1e-10
R_ANELLI = 24
DIR_NPZ = os.path.join(RADICE, "db", "strada_b")
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "strada_b")
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


def pesi_di(r):
    """### **`(a_n, b_a)` per unita' di tempo:** `mu0 = (1/2) sqrt(a^2 - a b + b^2) = pi/2` fisso."""
    a = math.pi / math.sqrt(1.0 - r + r * r)
    return a, r * a


@contextlib.contextmanager
def pesi(r):
    """### **`FP.z_nodo` e `FP.z_arco` con la frazione per `a_n/pi` e `b_a/pi`, rimessi all'uscita** *(a `r = 1` il fattore e' `1.0`: la stessa frazione al bit)*."""
    import flussi_parziali as FP
    a, b = pesi_di(r)
    fn, fb = a / math.pi, b / math.pi
    zn0, za0 = FP.z_nodo, FP.z_arco
    FP.z_nodo = lambda mot, frazione: zn0(mot, frazione * fn)
    FP.z_arco = lambda mot, frazione: za0(mot, frazione * fb)
    try:
        yield a, b
    finally:
        FP.z_nodo, FP.z_arco = zn0, za0


def nome_r(r):
    return "r%.2f" % r


def carica(r):
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome_r(r))
    if not os.path.exists(fj):
        return None
    cj = json.loads(io.open(fj, encoding="utf-8").read())
    fe = np.load(os.path.join(DIR_NPZ, "fermo_%s.npz" % nome_r(r)))
    return fe["psi_h"].copy(), float(fe["mu"]), cj, SFM.sha(fe["psi_h"]) == cj["sha"]


@contextlib.contextmanager
def scena():
    import _diagnosi_s4 as D
    import _modo_al_variare_di_s as MS
    _n, forma, s, N = MS.caso(CASO)
    with D.configura(forma, s, N):
        rec, z, phi0, p0 = MS.scena(forma, s, N)
        yield rec, z, phi0, p0, forma, s


def cerca(r):
    """### **Newton sulla mappa coi pesi** *(il metodo di `_modo_al_variare_di_s.cerca`)*, ### **dallo stato fermo a `r = 1` di `dfb5ab7e`.**"""
    from scipy.sparse.linalg import LinearOperator, gmres
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome_r(r))
    assert not os.path.exists(fj), "il .json c'e' gia': %s" % fj
    p0, mu0_, cj0, ok = MS.carica(CASO)
    assert ok and cj0["convergito"], "lo stato a r = 1 NON e' quello di dfb5ab7e"
    with scena() as (_rec, z, phi0, _p, forma, s), pesi(r) as (a, b):
        print("  r %.2f: a_n %.6f b_a %.6f; la partenza: lo stato fermo a r 1 (sha1 %s, mu %+.9f)" % (r, a, b, cj0["sha"][:8], mu0_))
        A = DV.matrice(z, phi0, DV.AMP) * np.exp(-1j * MS.ALPHA0[forma] * s)
        L = MS.L
        n = z["inc"].n
        Nn = float(np.sum(np.abs(p0) ** 2))
        fo = p0.shape
        m = p0.size

        def T(psi):
            return MS.tick(z, phi0, psi, forma)
        lam = complex(np.vdot(p0, T(p0)) / np.vdot(p0, p0))
        mu = -math.atan2(lam.imag, lam.real) / s

        def da_x(x):
            return (x[:m] + 1j * x[m:2 * m]).reshape(fo), float(x[2 * m])

        def F(x):
            psi, mu_ = da_x(x)
            R = (T(psi) - np.exp(-1j * mu_ * s) * psi).ravel() / math.sqrt(Nn)
            return np.concatenate([R.real, R.imag, [(float(np.sum(np.abs(psi) ** 2)) - Nn) / Nn]])

        def residuo(psi, mu_):
            return float(np.linalg.norm(T(psi) - np.exp(-1j * mu_ * s) * psi) / np.linalg.norm(psi))

        x = np.concatenate([p0.ravel().real, p0.ravel().imag, [mu]])
        F0 = F(x)
        storia = [{"passo": 0, "residuo": residuo(p0, mu), "mu": mu, "gmres": 0, "dimezzamenti": 0}]
        print("  r %.2f: passo 0, residuo %.3e, mu %+.9f" % (r, storia[0]["residuo"], mu))
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
            print("  r %.2f: passo %d, residuo %.3e, mu %+.9f, GMRES %d, dimezzamenti %d (%.0f s)" % (r, it, storia[-1]["residuo"], mu, conti[0], k, time.time() - s0))
            sys.stdout.flush()
        psi, mu = da_x(x)
        psi *= math.sqrt(Nn / float(np.sum(np.abs(psi) ** 2)))
        rf = residuo(psi, mu)
    os.makedirs(DIR_NPZ, exist_ok=True)
    os.makedirs(DIR_JSON, exist_ok=True)
    tmp = os.path.join(DIR_NPZ, "fermo_%s_tmp.npz" % nome_r(r))
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, os.path.join(DIR_NPZ, "fermo_%s.npz" % nome_r(r)))
    riga = {"r": r, "a_n": a, "b_a": b, "partenza_sha": cj0["sha"], "forma": forma, "s": s, "N": Nn, "mu": mu, "residuo_finale": rf, "storia": storia,
            "secondi": time.time() - s0, "sha": SFM.sha(psi), "convergito": rf < TOLL_RES}
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    with open(fj, "xb") as fh:
        fh.write(dati)
    print("  r %.2f: residuo finale %.3e, mu %+.9f; %s" % (r, rf, mu, "CONVERGE" if rf < TOLL_RES else "NON CONVERGE"))


def breve(r):
    """### **`180` unita' di tempo dallo stato fermo coi pesi; `D` rispetto allo stato fermo; l'esame di `dfb5ab7e`.**"""
    import _dove_va_la_materia as DV
    import _filtro_bande_piatte as FB
    import _modo_al_variare_di_s as MS
    fj = os.path.join(DIR_JSON, "breve_%s.json" % nome_r(r))
    assert not os.path.exists(fj), fj
    c = carica(r)
    assert c is not None and c[3] and c[2]["convergito"], "lo stato fermo a r %.2f non c'e' o non e' fermo: la corsa breve non parte" % r
    psi0, mu, cj, _ok = c
    print("  r %.2f: lo stato fermo sha1 %s, residuo %.3e, mu %+.9f" % (r, cj["sha"][:8], cj["residuo_finale"], mu))
    with scena() as (_rec, z, phi0, _p, forma, s), pesi(r):
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
        L = MS.L
        n0 = math.sqrt(float(np.sum(np.abs(psi0) ** 2)))
        ogni = int(round(PASSO_FIS / s))
        t_fine = int(round(T_FIS / s))
        t_da = int(round(T_DA_FIS / s))
        psi = psi0.copy()
        dn = 0.0
        Dd = {}
        s0 = time.time()
        for t in range(1, t_fine + 1):
            psi = MS.tick(z, phi0, psi, forma)
            dn = max(dn, abs(float(np.sum(np.abs(psi) ** 2)) / n0 ** 2 - 1.0))
            if t % ogni == 0 and t >= t_da:
                Dd[t] = np.exp(1j * mu * s * t) * psi - psi0
        print("  r %.2f: M conservata entro %.1e; %.0f s" % (r, dn, time.time() - s0))
        v = MS.Vista(z, psi0)
        tasso = FB.esame(nome_r(r), sorted(Dd), Dd, n0, cj["residuo_finale"], s, v, Z, L, nome_r(r))
    nD = [float(np.linalg.norm(Dd[t])) / n0 for t in sorted(Dd)]
    riga = {"r": r, "tasso": tasso, "dn": dn, "nD": nD, "t": sorted(Dd), "sha": cj["sha"]}
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    with open(fj, "xb") as fh:
        fh.write(dati)
    print("  r %.2f: il tasso %s; la corsa lunga %s" % (r, tasso, "SI'" if lunga_ammessa(riga) else "NO"))


def lunga_ammessa(br):
    """### **Il tasso breve `<= TASSO_CORSA`;** ### **se la finestra non ha `3` campioni** *(il tasso non si misura)*, **solo se `|D|` non ha mai raggiunto la saturazione** *(`D` non cresce)*."""
    import _filtro_bande_piatte as FB
    if br["tasso"] is not None:
        return br["tasso"] <= TASSO_CORSA
    return max(br["nD"]) < FB.SATURAZIONE


def corsa(r):
    """### **Un pezzo della corsa lunga, dallo stato salvato** *(o dallo stato fermo)*, ### **`PEZZO` tick coi pesi.**"""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    br = json.loads(io.open(os.path.join(DIR_JSON, "breve_%s.json" % nome_r(r)), encoding="utf-8").read())
    assert lunga_ammessa(br), "la corsa breve non ammette la lunga (il tasso %s, |D| massimo %.1e)" % (br["tasso"], max(br["nD"]))
    f_stato = os.path.join(DIR_NPZ, "corsa_%s.npz" % nome_r(r))
    with scena() as (rec, z, phi0, p0, forma, s), pesi(r):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        t0 = 0
        punti = []
        if os.path.exists(f_stato):
            dati = np.load(f_stato)
            t0 = int(dati["t"])
            z["st"]["psi_h"][...] = dati["psi_h"]
            prec = json.loads(io.open(os.path.join(DIR_JSON, "corsa_%s_%05d.jsonl" % (nome_r(r), t0 - PEZZO)), encoding="utf-8").read())
            assert prec["sha_fine"] == SFM.sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
        else:
            c = carica(r)
            assert c is not None and c[3] and c[2]["convergito"], "lo stato fermo non c'e' o non e' fermo"
            z["st"]["psi_h"][...] = c[0]
            punti.append(CL.punto(z, 0, w_in, w0))
        if t0 >= T_MAX:
            print("  corsa %s: finita" % nome_r(r))
            return
        t1 = min(t0 + PEZZO, T_MAX)
        s0 = time.time()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(t0 + 1, t1 + 1):
                CL.avanza(z, phi0, 1)
                if t % OGNI == 0:
                    p = CL.punto(z, t, w_in, w0)
                    p["tau"] = t * s
                    punti.append(p)
        riga = {"r": r, "t0": t0, "t1": t1, "s": s, "w0": w0, "w_in": w_in, "punti": punti, "sha_fine": SFM.sha(z["st"]["psi_h"]), "secondi": time.time() - s0}
        fp = os.path.join(DIR_JSON, "corsa_%s_%05d.jsonl" % (nome_r(r), t0))
        assert not os.path.exists(fp), fp
        dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
        with open(fp, "xb") as fh:
            fh.write(dati)
        tmp = os.path.join(DIR_NPZ, "corsa_%s_tmp.npz" % nome_r(r))
        np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
        os.replace(tmp, f_stato)
    print("  corsa %s: tick %d -> %d, w/w_in %.5f, cuore %.5f (%.0f s)" % (nome_r(r), t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], riga["secondi"]))


def libero(z, phi0, s, r):
    import _dove_va_la_materia as DV
    with pesi(r) as (a, b):
        A = DV.matrice(z, phi0, DV.AMP)
    E = np.sort(-np.angle(np.linalg.eigvals(A)) / s, axis=-1)
    return A, E, a, b


def referto():
    import _bande_piatte as BP
    import _congelato_lungo as CL
    import _cuore_e_alone as CE
    import _deriva_congelato as DC
    import _energia_del_legame as EL
    import _modo_al_variare_di_s as MS
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    print("=" * 130)
    print("LA STRADA (B) CON r < 1 CURA IL SOLITONE S1? (Luca 19:58; UNA DIAGNOSI): i pesi del nodo e dell'arco in memoria; %s, L %d, eps 0, il congelato vero" % (CASO, MS.L))
    print("=" * 130)
    print("  la configurazione: CASO %s R_LISTA %s R_CARTA %s MAX_NEWTON %d TOLL_RES %g T_FIS %g T_DA_FIS %g PASSO_FIS %g TASSO_CORSA %g T_MAX %d PEZZO %d OGNI %d FINESTRA %g TICK_BIT %d TOLL_NORMA %g TOLL_RICOMPOSTO %g R_ANELLI %d"
          % (CASO, R_LISTA, R_CARTA, MAX_NEWTON, TOLL_RES, T_FIS, T_DA_FIS, PASSO_FIS, TASSO_CORSA, T_MAX, PEZZO, OGNI, FINESTRA, TICK_BIT, TOLL_NORMA, TOLL_RICOMPOSTO, R_ANELLI))
    print("  i pesi: a_n = pi/sqrt(1 - r + r^2), b_a = r a_n (mu0 = pi/2 fisso); lo scarto nel cuore = 2 - a_n - 2 mu per unita' di tempo (scritto prima)")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (c1) a r 0.65 il modo non cresce e il cuore regge: (B) con r < 1 cura S1; (c2) il modo non cresce ma il cuore si svuota: un'altra causa;"
          " (c3) il modo cresce ancora: lo scarto nel solitone non e' quello libero; (c4) altro")
    print("-" * 130)
    print("### (0) SULLA CARTA: i vincoli (v1), (v2) nelle loro formule")
    for r in R_CARTA:
        a, b = pesi_di(r)
        mu0 = 0.5 * math.sqrt(a * a - a * b + b * b)
        x = math.sqrt(a * b) / (4.0 * math.pi)
        print("  r %.2f: a_n/pi %.6f b_a/pi %.6f mu0/pi %.6f; lo scarto libero pi (1 - 1/sqrt(1 - r + r^2)) %+.6f; x = sqrt(a_n b_a)/(4 pi) %.6f (la parte 2 vuole 0.25 al vuoto di riferimento); pi x %.6f; pi/(4 sqrt r) di A1 %.6f"
              % (r, a / math.pi, b / math.pi, mu0 / math.pi, math.pi * (1.0 - 1.0 / math.sqrt(1.0 - r + r * r)), x, math.pi * x, math.pi / (4.0 * math.sqrt(r))))
    print("  (pi/4)^2 = %.6f" % ((math.pi / 4.0) ** 2))
    with scena() as (rec, z, phi0, p0, forma, s):
        L = MS.L
        iK = (L // 3, L // 3)
        print("-" * 130)
        print("### (2) IL CAMBIO IN MEMORIA: a r 1, %d tick dallo stato fermo di dfb5ab7e, con e senza l'avvolgimento" % TICK_BIT)
        pz, _mz, _cz, okz = MS.carica(CASO)
        esito("DEVE PASSARE: lo stato fermo a r 1 = quello di dfb5ab7e (sha1)", okz, "")
        q1 = pz.copy()
        q2 = pz.copy()
        for _t in range(TICK_BIT):
            q1 = MS.tick(z, phi0, q1, forma)
        with pesi(1.0):
            for _t in range(TICK_BIT):
                q2 = MS.tick(z, phi0, q2, forma)
        esito("DEVE PASSARE: a r 1 il tick in memoria = il tick di oggi AL BIT (%d tick)" % TICK_BIT, q1.tobytes() == q2.tobytes(), "")
        print("-" * 130)
        print("### (1) IL TICK LIBERO COI PESI, s %g" % s)
        A1, E1, _a1, _b1 = libero(z, phi0, s, 1.0)
        P = {j: BP.pezzo(z, phi0, j, 0.0, "simm") for j in (BP.J_GROVER, BP.J_SPOST)}
        X_G, R_S = BP.generatori(P, s)
        cur1 = E1[iK[0] + 1, iK[1]][4] + E1[iK[0] - 1, iK[1]][4] - 2.0 * E1[iK][4]
        for r in (1.0,) + R_LISTA:
            A, E, a, b = libero(z, phi0, s, r)
            Tr = BP.ricomposto(X_G, R_S, s, a, b)
            d = float(np.abs(Tr - A).max())
            if r != 1.0:
                esito("DEVE PASSARE: r %.2f, il tick coi pesi in memoria = il tick ricomposto dai generatori entro %g" % (r, TOLL_RICOMPOSTO), d < TOLL_RICOMPOSTO, "%.1e" % d)
            cur = E[iK[0] + 1, iK[1]][4] + E[iK[0] - 1, iK[1]][4] - 2.0 * E[iK][4]
            print("  r %.2f: P0 in [%+.6f, %+.6f], Ppi in [%+.6f, %+.6f]; A(K) %+.6f; lo scarto libero a K %+.5f; la curvatura di A a K %+.4e, rispetto a r 1 %.4f (a_n b_a/pi^2 %.4f)"
                  % (r, E[..., 6:10].min(), E[..., 6:10].max(), E[..., 0:4].min(), E[..., 0:4].max(), E[iK][4], BP.scarto_libero(E, iK), cur, cur / cur1, a * b / math.pi ** 2))
        print("-" * 130)
        print("### (3) GLI STATI FERMI COI PESI")
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            z["st"]["psi_h"][...] = p0
            w_in = DC.forma(z, w0)[0]
        stati = [("r 1.00 (dfb5ab7e)", 1.0, pz, _mz)]
        for r in R_LISTA:
            c = carica(r)
            if c is None:
                print("  r %.2f: NESSUNA RICERCA SUL DISCO" % r)
                continue
            psi, mu, cj, ok = c
            esito("DEVE PASSARE: r %.2f, lo stato sul disco = la ricerca (sha1)" % r, ok, "")
            print("  r %.2f: Newton dallo stato a r 1: %d passi, residuo %.3e (%s), %.0f s; la storia del residuo: %s"
                  % (r, len(cj["storia"]) - 1, cj["residuo_finale"], "CONVERGE" if cj["convergito"] else "NON CONVERGE", cj["secondi"], " ".join("%.1e" % p["residuo"] for p in cj["storia"])))
            stati.append(("r %.2f" % r, r, psi, mu))
        prof = {}
        for nome_, r, psi, mu in stati:
            a, _b = pesi_di(r)
            z["st"]["psi_h"][...] = psi
            pt = CL.punto(z, 0, w_in, w0)
            rho = EL.densita(z["inc"], z["st"])[0]
            _M, _c, d = CE.baricentro(z, rho)
            prof[nome_] = CE.anelli(rho, d)
            dist = SFM.distanza(pz.ravel(), psi.ravel())
            print("  %-18s mu %+.9f; lo scarto nel cuore 2 - a_n - 2 mu %+.5f; w/w_in %.5f, cuore f_win %.5f, entro 3 w0 %.5f, picco %.2f, FWHM %.4f; 1 - |<a|b>|^2 da r 1 %.3e"
                  % (nome_, mu, 2.0 - a - 2.0 * mu, pt["w"] / w_in, pt["f_win"], pt["f_3w0"], pt["picco"], CE.fwhm(prof[nome_]), dist))
        print("  il profilo per anelli (rho per nodo): " + "  ".join(prof))
        for k in range(R_ANELLI + 1):
            print("    r %2d: %s" % (k, "  ".join("%12.5e" % prof[nm][k] for nm in prof)))
    print("-" * 130)
    print("### (4) LE CORSE BREVI (%g unita' di tempo; gli esami completi in doc/referti_l2/strada_b/breve_<r>.txt)" % T_FIS)
    brevi = {}
    for r in R_LISTA:
        fj = os.path.join(DIR_JSON, "breve_%s.json" % nome_r(r))
        if not os.path.exists(fj):
            print("  r %.2f: nessuna corsa breve" % r)
            continue
        br = json.loads(io.open(fj, encoding="utf-8").read())
        brevi[r] = br
        esito("DEVE PASSARE: r %.2f, M conservata entro %g nella corsa breve" % (r, TOLL_NORMA), br["dn"] < TOLL_NORMA, "%.1e" % br["dn"])
        print("  r %.2f: il tasso %s (dfb5ab7e a r 1: 0.15108); |D|/|psi0| a tempo 60, 120, 180: %.1e %.1e %.1e"
              % (r, ("%.5f" % br["tasso"]) if br["tasso"] is not None else "-- (la finestra non ha 3 campioni)", br["nD"][0], br["nD"][len(br["nD"]) // 2], br["nD"][-1]))
    print("-" * 130)
    print("### (5) LA CORSA LUNGA")
    rif = []
    for n in sorted(os.listdir(SFM.PUNTI)):
        if n.startswith("corsa_L81_") and n.endswith(".jsonl"):
            rif.append(json.loads(io.open(os.path.join(SFM.PUNTI, n), encoding="utf-8").read()))
    rp_t = np.array([p["t"] * SFM.S for rr in rif for p in rr["punti"]])
    rp_c = np.array([p["f_win"] for rr in rif for p in rr["punti"]])

    def rif_cuore(x):
        if rp_t.size == 0:
            return "--"
        i = int(np.argmin(np.abs(rp_t - x)))
        return "%.5f (tau %.0f)" % (rp_c[i], rp_t[i])
    for r in R_LISTA:
        righe = []
        for n in sorted(os.listdir(DIR_JSON)) if os.path.isdir(DIR_JSON) else []:
            if n.startswith("corsa_%s_" % nome_r(r)) and n.endswith(".jsonl"):
                righe.append(json.loads(io.open(os.path.join(DIR_JSON, n), encoding="utf-8").read()))
        if not righe:
            print("  r %.2f: nessuna corsa lunga" % r)
            continue
        righe.sort(key=lambda x: x["t0"])
        for x, y in zip(righe, righe[1:]):
            assert x["t1"] == y["t0"], ("un buco fra i pezzi", x["t1"], y["t0"])
        pts = [p for x in righe for p in x["punti"]]
        print("  r %.2f: %d pezzi, tick %d -> %d%s" % (r, len(righe), righe[0]["t0"], righe[-1]["t1"], "" if righe[-1]["t1"] == T_MAX else " (NON FINITA)"))
        dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
        esito("DEVE PASSARE: r %.2f, M entro %g relativo nella corsa lunga" % (r, TOLL_NORMA), dM <= TOLL_NORMA, "%.1e" % dM)
        w_in = righe[0]["w_in"]
        tau = np.array([p["tau"] for p in pts])
        q = np.array([p["w"] / w_in for p in pts])
        cu = np.array([p["f_win"] for p in pts])
        al = np.array([1.0 - p["f_3w0"] for p in pts])
        pk = np.array([p["picco"] / pts[0]["picco"] for p in pts])
        a0 = 0.0
        while a0 < tau[-1] - 1e-9:
            m = (tau >= a0 - 1e-9) & (tau <= a0 + FINESTRA + 1e-9)
            pw = np.polyfit(tau[m], q[m], 1)[0]
            pc = np.polyfit(tau[m], cu[m], 1)[0]
            print("  r %.2f, tau [%6.0f, %6.0f]: w/w_in da %.5f a %.5f (pendenza %+.3e); cuore da %.5f a %.5f (pendenza %+.3e); alone da %.5f a %.5f; picco relativo medio %.5f | r 1 (26300537, s 0.3): cuore da %s a %s"
                  % (r, a0, a0 + FINESTRA, q[m][0], q[m][-1], pw, cu[m][0], cu[m][-1], pc, al[m][0], al[m][-1], pk[m].mean(),
                     rif_cuore(tau[m][0]), rif_cuore(tau[m][-1])))
            a0 += FINESTRA
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
        elif argv[:1] in (["--cerca"], ["--breve"], ["--corsa"]) and len(argv) == 2:
            r = float(argv[1])
            assert r in R_LISTA, "r %r non e' nel mandato %s" % (r, R_LISTA)
            {"--cerca": cerca, "--breve": breve, "--corsa": corsa}[argv[0]](r)
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
