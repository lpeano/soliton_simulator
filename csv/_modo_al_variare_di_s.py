# -*- coding: utf-8 -*-
r"""**IL MODO INSTABILE AL VARIARE DI `s`, E PER `S4`** *(il mandato di Luca delle `10:00` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_modo_al_variare_di_s.md`)*: ### **lo stato fermo sul reticolo con Newton** *(forma, `s`, `N` come argomenti)*;
### **una corsa di `180` unita' di tempo dallo stato fermo, in memoria; il tasso, il periodo, la forma del modo** *(l'esame di `_modo_dalla_corsa`, senza Arnoldi)*.

> ### **Gli stati fermi in `db/modo_s/`** *(ignorato da git: il dato e' il comando)*; ### **la storia di Newton in `doc/referti_l2/modo_s/`.** ### **`S1` a `s 0.3`: lo stato fermo di `_stato_fermo.py`.**

    python csv/_modo_al_variare_di_s.py --cerca <S1_s0.150|S1_s0.075|S4_s0.300>
    python csv/_modo_al_variare_di_s.py --referto > doc/referti_l2/modo_al_variare_di_s.txt
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
CASI = (("S1_s0.300", "S1", 0.3, 1e6), ("S1_s0.150", "S1", 0.15, 1e6), ("S1_s0.075", "S1", 0.075, 1e6), ("S4_s0.300", "S4", 0.3, 1e7))
NUOVI = ("S1_s0.150", "S1_s0.075", "S4_s0.300")
ALPHA0 = {"S1": 0.0, "S4": -math.pi}
TOLL_RES = 1e-9
MAX_NEWTON = 30
GMRES_RTOL = 1e-3
GMRES_RESTART = 60
GMRES_MAXITER = 10
DIMEZZA = 8
H_REL = 1e-5
T_FIS = 180.0
T_DA_FIS = 60.0
PASSO_FIS = 3.0
FATTORE_RUMORE = 1e3
SATURAZIONE = 1e-2
SOGLIE_FORMA = (1e-4, 1e-3)
TOLL_NORMA = 1e-10
RESPIRO = 11.1                 # ### il periodo dominante della corsa lunga (40061005)
STATI = os.path.join(RADICE, "db", "modo_s")
PUNTI = os.path.join(RADICE, "doc", "referti_l2", "modo_s")
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


def caso(nome):
    return [c for c in CASI if c[0] == nome][0]


def scena(forma, s, N):
    import _diagnosi_s4 as D
    rec, z = D.iniziale(forma, s, L)
    return rec, z, z["st"]["phi_h"].copy(), z["st"]["psi_h"].copy()


def tick(z, phi0, psi, forma):
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _triangoli_bassa_energia as BE
    z["st"]["psi_h"][...] = psi
    with SF.forma(forma), BE.conv(DC.ZERO):
        CL.avanza(z, phi0, 1)
    return z["st"]["psi_h"].copy()


def cerca(nome):
    """### **Newton sulla mappa del tick** *(il metodo di `_stato_fermo.cerca`, con forma, `s`, `N` come argomenti; il precondizionatore `e^{-i alpha(0) s} A(k)`)*."""
    from scipy.sparse.linalg import LinearOperator, gmres
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _stato_fermo as SFM
    _n, forma, s, N = caso(nome)
    with D.configura(forma, s, N):
        rec, z, phi0, p0 = scena(forma, s, N)
        A = DV.matrice(z, phi0, DV.AMP) * np.exp(-1j * ALPHA0[forma] * s)
        n = z["inc"].n
        Nn = float(np.sum(np.abs(p0) ** 2))
        fo = p0.shape
        m = p0.size
        lam = complex(np.vdot(p0, tick(z, phi0, p0, forma)) / np.vdot(p0, p0))
        mu = -math.atan2(lam.imag, lam.real) / s

        def da_x(x):
            return (x[:m] + 1j * x[m:2 * m]).reshape(fo), float(x[2 * m])

        def F(x):
            psi, mu_ = da_x(x)
            R = (tick(z, phi0, psi, forma) - np.exp(-1j * mu_ * s) * psi).ravel() / math.sqrt(Nn)
            return np.concatenate([R.real, R.imag, [(float(np.sum(np.abs(psi) ** 2)) - Nn) / Nn]])

        def residuo(psi, mu_):
            return float(np.linalg.norm(tick(z, phi0, psi, forma) - np.exp(-1j * mu_ * s) * psi) / np.linalg.norm(psi))

        x = np.concatenate([p0.ravel().real, p0.ravel().imag, [mu]])
        F0 = F(x)
        storia = [{"passo": 0, "residuo": residuo(p0, mu), "mu": mu, "gmres": 0, "dimezzamenti": 0}]
        print("  %s: passo 0, residuo %.3e, mu %+.9f" % (nome, storia[0]["residuo"], mu))
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
                h = H_REL * (1.0 + nx) / nv
                conti[0] += 1
                return (F(x + h * v) - F(x - h * v)) / (2.0 * h)
            Aop = LinearOperator((2 * m + 1, 2 * m + 1), matvec=jv, dtype=float)
            y, _info = gmres(Aop, -F0, rtol=GMRES_RTOL, restart=GMRES_RESTART, maxiter=GMRES_MAXITER)
            dx = prec(y)
            nf0 = float(np.linalg.norm(F0))
            passo, k = 1.0, 0
            while True:
                xn = x + passo * dx
                Fn = F(xn)
                if float(np.linalg.norm(Fn)) < nf0 or k >= DIMEZZA:
                    break
                passo *= 0.5
                k += 1
            x, F0 = xn, Fn
            psi, mu = da_x(x)
            storia.append({"passo": it, "residuo": residuo(psi, mu), "mu": mu, "gmres": conti[0], "dimezzamenti": k})
            print("  %s: passo %d, residuo %.3e, mu %+.9f, GMRES %d, dimezzamenti %d (%.0f s)" % (nome, it, storia[-1]["residuo"], mu, conti[0], k, time.time() - s0))
            sys.stdout.flush()
        psi, mu = da_x(x)
        psi *= math.sqrt(Nn / float(np.sum(np.abs(psi) ** 2)))
        r = residuo(psi, mu)
    os.makedirs(STATI, exist_ok=True)
    os.makedirs(PUNTI, exist_ok=True)
    f = os.path.join(STATI, "fermo_%s.npz" % nome)
    tmp = os.path.join(STATI, "fermo_%s_tmp.npz" % nome)
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, f)
    riga = {"caso": nome, "forma": forma, "s": s, "N": Nn, "L": L, "mu": mu, "residuo_finale": r, "storia": storia, "secondi": time.time() - s0,
            "sha": SFM.sha(psi), "convergito": r < TOLL_RES, "w0_risolutore": rec["larghezza"], "mu_risolutore": rec["mu"]}
    fj = os.path.join(PUNTI, "cerca_%s.json" % nome)
    assert not os.path.exists(fj), fj
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    with open(fj, "xb") as fh:
        fh.write(dati)
    print("  %s: residuo finale %.3e, mu %+.9f; %s" % (nome, r, mu, "CONVERGE" if r < TOLL_RES else "NON CONVERGE"))


def carica(nome):
    """### **Lo stato fermo, `mu`, la storia** *(`S1` a `s 0.3`: quelli di `_stato_fermo.py`)*."""
    import _stato_fermo as SFM
    if nome == "S1_s0.300":
        cj = json.loads(io.open(os.path.join(SFM.PUNTI, "cerca_L%d.json" % L), encoding="utf-8").read())
        fe = np.load(os.path.join(SFM.STATI, "fermo_L%d.npz" % L))
    else:
        cj = json.loads(io.open(os.path.join(PUNTI, "cerca_%s.json" % nome), encoding="utf-8").read())
        fe = np.load(os.path.join(STATI, "fermo_%s.npz" % nome))
    return fe["psi_h"].copy(), float(fe["mu"]), cj, SFM.sha(fe["psi_h"]) == cj["sha"]


class Vista:
    def __init__(self, z, psi0):
        self.z, self.psi0, self.n = z, psi0, z["inc"].n


def esame(nome):
    import _cuore_e_alone as CE
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _energia_del_legame as EL
    import _modo_instabile as MI
    _n, forma, s, N = caso(nome)
    print("-" * 130)
    psi0, mu, cj, ok = carica(nome)
    print("### %s: %s, s %g, N %g, L %d" % (nome, forma, s, N, L))
    esito("DEVE PASSARE: %s, lo stato fermo sul disco = quello della ricerca (sha1)" % nome, ok, "")
    esito("DEVE PASSARE: %s, il criterio di Newton (residuo < %g)" % (nome, TOLL_RES), cj["convergito"],
          "%.3e in %d passi; la storia: %s" % (cj["residuo_finale"], len(cj["storia"]) - 1, " ".join("%.1e" % p["residuo"] for p in cj["storia"])))
    if not cj["convergito"]:
        return None
    with D.configura(forma, s, N):
        rec, z, phi0, _p0 = scena(forma, s, N)
        v = Vista(z, psi0)
        z["st"]["psi_h"][...] = psi0
        rho = EL.densita(z["inc"], z["st"])[0]
        _M, _c, d = CE.baricentro(z, rho)
        pr = CE.anelli(rho, d)
        dpr = np.abs(np.diff(pr[:30]))
        kb = int(np.argmax(dpr))
        print("  mu %+.9f; 2 pi / |mu| = %.3f unita' di tempo; il respiro della corsa lunga %.1f; il risolutore: w0 %.4f, mu %+.6f" % (mu, 2 * math.pi / abs(mu), RESPIRO, rec["larghezza"], rec["mu"]))
        print("  il bordo: la pendenza massima del profilo per anelli |rho(k+1) - rho(k)| / picco = %.4f fra gli anelli %d e %d; il profilo / picco, r 0..20: %s"
              % (dpr[kb] / pr.max(), kb, kb + 1, " ".join("%.3f" % (x / pr.max()) for x in pr[:21])))
        ogni = int(round(PASSO_FIS / s))
        t_fine = int(round(T_FIS / s))
        t_da = int(round(T_DA_FIS / s))
        n0 = float(np.linalg.norm(psi0))
        M0 = float(np.sum(np.abs(psi0) ** 2))
        psi = psi0.copy()
        Dd = {}
        dM = 0.0
        s0 = time.time()
        for t in range(1, t_fine + 1):
            psi = tick(z, phi0, psi, forma)
            if t % ogni == 0:
                dM = max(dM, abs(float(np.sum(np.abs(psi) ** 2)) / M0 - 1.0))
                if t >= t_da:
                    Dd[t] = np.exp(1j * mu * s * t) * psi - psi0
        esito("DEVE PASSARE: %s, M conservata nella corsa entro %g" % (nome, TOLL_NORMA), dM < TOLL_NORMA, "%.1e; %d tick in %.0f s" % (dM, t_fine, time.time() - s0))
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
    ts = sorted(Dd)
    nD = np.array([float(np.linalg.norm(Dd[t])) / n0 for t in ts])
    print("  |D|/|psi0| ogni %d tick da %d: %s" % (ogni, t_da, " ".join("%.1e" % x for x in nD)))
    r1 = cj["residuo_finale"]
    fin = [i for i in range(len(ts)) if FATTORE_RUMORE * r1 < nD[i] < SATURAZIONE]
    out = {"nome": nome, "s": s, "mu": mu, "bordo": float(dpr[kb] / pr.max()), "anello_bordo": kb}
    if len(fin) < 3:
        print("  la finestra lineare ha %d campioni: il tasso non si misura" % len(fin))
        return out
    a, b = fin[0], fin[-1]
    tt = np.array(ts[a:b + 1], dtype=float)
    pend = float(np.polyfit(tt, np.log(nD[a:b + 1]), 1)[0])
    loc = [(math.log(nD[i + 1]) - math.log(nD[i - 1])) / (2.0 * ogni) / s for i in range(max(a, 1), min(b, len(ts) - 2) + 1)]
    print("  la finestra: t %d .. %d (tempo %.0f .. %.0f); il tasso %.5f per tick, %.5f per unita' di tempo; le pendenze locali per unita' di tempo da %.4f a %.4f"
          % (ts[a], ts[b], ts[a] * s, ts[b] * s, pend, pend / s, min(loc), max(loc)))
    tc = ts[(a + b) // 2]
    proj = [float(np.real(np.vdot(Dd[tc], Dd[t]))) / (float(np.linalg.norm(Dd[tc])) * float(np.linalg.norm(Dd[t]))) for t in ts[a:b + 1]]
    cambi = [i for i in range(1, len(proj)) if proj[i - 1] * proj[i] < 0.0]
    per = None
    if len(cambi) >= 2:
        per = 2.0 * ogni * float(np.mean(np.diff(cambi))) * s
        print("  il periodo dai cambi di segno della proiezione su D(%d): %.2f unita' di tempo (%d cambi); 2 pi / |mu| %.3f; il respiro %.1f" % (tc, per, len(cambi), 2 * math.pi / abs(mu), RESPIRO))
    else:
        print("  %d cambi di segno nella finestra: il periodo non si misura" % len(cambi))
    istanti = []
    for so in SOGLIE_FORMA:
        c = [t for t, x in zip(ts, nD) if x >= so]
        if c:
            istanti.append(c[0])
    istanti.append(ts[b])
    for t in sorted(set(istanti)):
        dd = Dd[t] / float(np.linalg.norm(Dd[t]))
        dr, df = MI.per_nodo(v, dd)
        wd, kk = MI.armoniche(v, dr)
        prd = np.bincount(kk, weights=np.sum(np.abs(dd.reshape(v.n, 12)) ** 2, axis=1))
        prd = prd / prd.sum()
        top = np.argsort(-prd)[:3]
        Pk = DV.pesi(dd.reshape(v.n, 12), np.ones(v.n), Z, L)
        tot = float(Pk.sum())
        print("  t %d (tempo %.0f, |D|/|psi0| %.1e): gli anelli maggiori di |D|^2 %s; le bande %s; le armoniche di drho %s"
              % (t, t * s, float(np.linalg.norm(Dd[t])) / n0, ", ".join("r %d %.3f" % (k, prd[k]) for k in top),
                 "  ".join("%s %.3f" % (g, float(Pk[:, :, list(idx)].sum()) / tot) for g, idx in DV.GRUPPI),
                 " ".join("m%d %.3f" % (mm, wd[mm]) for mm in range(MI.M_MAX + 1))))
    out.update({"tasso": pend / s, "periodo": per})
    return out


def referto():
    print("=" * 130)
    print("IL MODO INSTABILE AL VARIARE DI s, E PER S4 (Luca 10:00): lo stato fermo sul reticolo (Newton), %g unita' di tempo dallo stato fermo, l'esame di 5f06dbfb senza Arnoldi" % T_FIS)
    print("=" * 130)
    print("  la configurazione: L %d CASI %s ALPHA0 %s TOLL_RES %g MAX_NEWTON %d GMRES_RTOL %g GMRES_RESTART %d GMRES_MAXITER %d DIMEZZA %d H_REL %g T_FIS %g T_DA_FIS %g PASSO_FIS %g FATTORE_RUMORE %g SATURAZIONE %g SOGLIE_FORMA %s TOLL_NORMA %g RESPIRO %g"
          % (L, CASI, ALPHA0, TOLL_RES, MAX_NEWTON, GMRES_RTOL, GMRES_RESTART, GMRES_MAXITER, DIMEZZA, H_REL, T_FIS, T_DA_FIS, PASSO_FIS, FATTORE_RUMORE, SATURAZIONE, SOGLIE_FORMA, TOLL_NORMA, RESPIRO))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (A1) il tasso converge al calare di s; (A2) cambia molto con s; (B1) S4 non ha il modo: il bordo ripido di S1; (B2) S4 ha lo stesso modo; (C) il periodo segue 2 pi/|mu|, o no; (D) altro")
    righe = [esame(c[0]) for c in CASI]
    print("-" * 130)
    print("### LA SINTESI")
    for r in righe:
        if r is None:
            continue
        print("  %-10s s %.3f: il tasso %s per unita' di tempo; il periodo %s; 2 pi/|mu| %.3f; il bordo %.4f (anelli %d-%d)"
              % (r["nome"], r["s"], ("%.5f" % r["tasso"]) if r.get("tasso") is not None else "--", ("%.2f" % r["periodo"]) if r.get("periodo") else "--",
                 2 * math.pi / abs(r["mu"]), r["bordo"], r["anello_bordo"], r["anello_bordo"] + 1))
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
            assert argv[1] in NUOVI, argv
            cerca(argv[1])
        elif argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
