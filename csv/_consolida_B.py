# -*- coding: utf-8 -*-
r"""**IL SOLITONE SU `B` A `Gamma` REGGE: CONSOLIDARE** *(UNA PROVA, NESSUNA MODIFICA AL NUCLEO; il mandato di Luca delle `15:58` del `2026-10-31`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-31_consolida_B.md`)*:
### **(1) il limite superiore del tasso dalle bande di `D` della corsa di `a8e0e43b`; (2) la stessa corsa fino a `tau 20000`; (3) la robustezza dall'inviluppo, senza Newton (`N 3e5`, `N 3e6`, `N 1e6` su `L 120`, il controllo `N 1e6` su `L 81`);**
### **(4) Newton col vincolo che fissa la rotazione dentro la coppia.** ### **Importa `_coppia_di_B` (la coppia, il residuo, la partenza di `B`) e `_massimo_di_B` (la scena a `eps`, le misure).**

    python csv/_consolida_B.py --limite > doc/referti_l2/consolida_B/limite_3000.txt
    python csv/_consolida_B.py --lunga                  # un pezzo; si ripete finche' dice "finita"
    python csv/_consolida_B.py --robusta N3e5           # un pezzo; idem N3e6, N1e6_L120, N1e6_L81
    python csv/_consolida_B.py --vincolo e0 > doc/referti_l2/consolida_B/vincolo_e0.txt      # idem e05
    python csv/_consolida_B.py --referto > doc/referti_l2/consolida_B.txt
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

import _coppia_di_B as CB                                      # noqa: E402

MB = CB.MB
LP = CB.LP
S = CB.S
N = CB.N
L = CB.L
EPS = CB.EPS_LUNGA
NOME_EPS = "e05"
T_TOT = int(math.ceil(20000.0 / S))     # ### tau 20000 in tutto (Luca: 113000 tick in piu'; arrotondato a 20000 pieni)
PEZZO = 10000
T_ROBUSTA = CB.T_LUNGA                  # ### 3000 unita' di tempo
ROBUSTE = {"N3e5": (3e5, None), "N3e6": (3e6, None), "N1e6_L120": (1e6, MB.L_GRANDE), "N1e6_L81": (1e6, L)}   # ### None: L 81, o L 120 se w > L/6; N1e6_L81 il controllo DICHIARATO
OGNI = CB.OGNI
OGNI_D = CB.OGNI_D
ESAME = CB.ESAME
FINESTRA = CB.FINESTRA
GRUPPI = {"piatte": ("P0", "Ppi"), "A": ("A",)}
TASSI_NOTI = (("la mista (modo_di_R.txt)", 0.0079), ("il modo lento (modo_lento.txt)", 0.0331), ("la coppia di piatte (decadimento_in_coppia.txt)", 0.139))   # ### dichiarati, dai referti citati
TOLL_BLOCH = CB.TOLL_BLOCH
TOLL_NORMA = CB.TOLL_NORMA
TOLL_PARTENZA = 1e-12                   # ### la norma della partenza, il vincolo alla partenza, sigma_z di q1 a eps 0 (1e-10)
TOLL_SZ = 1e-10
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "consolida_B")
DIR_NPZ = os.path.join(RADICE, "db", "consolida_B")
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


def pezzi(cartella, prefisso):
    pz = sorted([LP.leggi(os.path.join(cartella, n)) for n in os.listdir(cartella) if n.startswith(prefisso) and n.endswith(".jsonl")], key=lambda x: x["t0"])
    for x, y in zip(pz, pz[1:]):
        assert x["t1"] == y["t0"], ("un buco fra i pezzi", prefisso, x["t1"], y["t0"])
        if "sha_ripresa" in y:
            assert x["sha_fine"] == y["sha_ripresa"], ("la ripresa non e' la fine del pezzo prima", prefisso, y["t0"])
    return pz


def serie_B():
    """### **La corsa di `B` intera:** i pezzi di `a8e0e43b` *(`_coppia_di_B`)* **e quelli di qui, che li continuano.**"""
    return pezzi(CB.DIR_JSON, "lunga_B_") + pezzi(DIR_JSON, "lunga_B_")


# ====================================================================== (1) IL LIMITE SUPERIORE DEL TASSO
def limite(pz):
    """### **Per `piatte` e `A`: la frazione `f` di `|D|^2` e l'ampiezza `a = sqrt(f) nD`** *(in unita' di `|psi0|`, come i tassi noti)*; ### **i limiti (lett), (a0), (amin), (pend); il dichiarato e' il piu' grande fra (a0), (amin), (pend).**"""
    dd = [d for x in pz for d in x["D"]]
    s = pz[0]["s"]
    tau = np.array([d["t"] * s for d in dd])
    nD = np.array([d["nD"] for d in dd])
    T = float(tau[-1] - tau[0])
    out = {"tau0": float(tau[0]), "tau1": float(tau[-1]), "campioni": len(dd), "gruppi": {}}
    for g, bb in GRUPPI.items():
        f = np.array([sum(d["bande"][b] for b in bb) for d in dd])
        a = np.sqrt(f) * nD
        im, ix = int(np.argmin(a)), int(np.argmax(f))
        h = tau >= tau[0] + 0.5 * T
        r = {"f0": float(f[0]), "f_max": float(f[ix]), "tau_f_max": float(tau[ix]), "f1": float(f[-1]),
             "a0": float(a[0]), "a_min": float(a[im]), "tau_a_min": float(tau[im]), "a_max": float(a.max()), "a1": float(a[-1]),
             "lett": float(math.log(f[-1] / f[0]) / T), "da_a0": float(math.log(a[-1] / a[0]) / T),
             "da_amin": float(math.log(a[-1] / a[im]) / (tau[-1] - tau[im])) if tau[-1] > tau[im] else float("-inf"),
             "pend": float(np.polyfit(tau[h], np.log(a[h]), 1)[0])}
        r["limite"] = max(r["da_a0"], r["da_amin"], r["pend"])
        out["gruppi"][g] = r
    return out


def stampa_limite(lm):
    print("  %d campioni, tau %.1f .. %.1f" % (lm["campioni"], lm["tau0"], lm["tau1"]))
    for g, r in lm["gruppi"].items():
        print("    %-6s la frazione di |D|^2: %.3e (tau %.0f) .. il massimo %.3e (tau %.0f) .. %.3e; l'ampiezza sqrt(f) nD: %.3e .. il minimo %.3e (tau %.0f) .. il massimo %.3e .. %.3e"
              % (g, r["f0"], lm["tau0"], r["f_max"], r["tau_f_max"], r["f1"], r["a0"], r["a_min"], r["tau_a_min"], r["a_max"], r["a1"]))
        print("    %-6s i limiti: (lett) ln(f1/f0)/T %+.3e; (a0) ln(a1/a0)/T %+.3e; (amin) ln(a1/a_min)/(T - tau_min) %+.3e; (pend) ln a sulla seconda meta' %+.3e; ### IL LIMITE %.3e -- %s"
              % (g, r["lett"], r["da_a0"], r["da_amin"], r["pend"], r["limite"], "; ".join("%s %g: %.1f volte sotto" % (k, v, v / r["limite"]) if r["limite"] > 0 else "%s %g" % (k, v) for k, v in TASSI_NOTI)))


def limite_3000():
    fj = os.path.join(DIR_JSON, "limite_3000.json")
    assert not os.path.exists(fj), fj
    pz = pezzi(CB.DIR_JSON, "lunga_B_")
    assert pz and pz[-1]["t1"] == CB.T_LUNGA, "la corsa di a8e0e43b non e' intera"
    print("### (1) IL LIMITE SUPERIORE DEL TASSO dalla corsa di B a Gamma di a8e0e43b (eps %g, %d tick; la partenza %s)" % (EPS, CB.T_LUNGA, pz[0]["partenza"]))
    print("  ### la frazione scende perche' D cresce lineare in B: il limite sull'AMPIEZZA (i tassi noti sono dell'ampiezza: t_vita = ln(1e-2/seme)/gamma); (lett) e' la formula alla lettera")
    lm = limite(pz)
    stampa_limite(lm)
    os.makedirs(DIR_JSON, exist_ok=True)
    LP.scrivi_nuovo(fj, lm)


# ====================================================================== LE CORSE (2) E (3)
def q_migliore():
    """### **La scelta migliore a `eps 0.5`** *(`griglia.json`)* **sulla scena di riferimento** *(`N 1e6`, `L 81`)*, **e il suo partner nella coppia.**"""
    gr = LP.leggi(os.path.join(CB.DIR_JSON, "griglia.json"))[NOME_EPS]
    th, fi = gr["minimo"]["theta"], gr["minimo"]["phi"]
    with MB.scena(N, L, EPS) as (_rec, z, phi0, _p):
        q1, q2, _E0, _G = CB.coppia(z, phi0)
    return math.cos(th) * q1 + np.exp(1j * fi) * math.sin(th) * q2, -math.sin(th) * q1 + np.exp(1j * fi) * math.cos(th) * q2, th, fi


def inviluppo(z, pK, q, N_):
    inv = np.linalg.norm(pK.reshape(z["inc"].n, 12), axis=1)
    p = inv[:, None] * q[None, :]
    p *= math.sqrt(N_ / float(np.sum(np.abs(p) ** 2)))
    return p.reshape(pK.shape)


def l_robusta(nome):
    """### **`L` della corsa:** quello dichiarato, o `L 120` se la `w` della partenza a `L 81` supera `L/6`."""
    N_, L_ = ROBUSTE[nome]
    if L_ is not None:
        return L_, None
    q = q_migliore()[0]
    with MB.scena(N_, L, EPS) as (rec, z, phi0, pK):
        w = MB.misure(z, phi0, rec, inviluppo(z, pK, q, N_))["w"]
    return (MB.L_GRANDE if w > L * LP.FRAZ_LARGO else L), w


def partenza_robusta(nome):
    N_ = ROBUSTE[nome][0]
    L_, w81 = l_robusta(nome)
    q, _qp, th, fi = q_migliore()
    with MB.scena(N_, L_, EPS) as (rec, z, phi0, pK):
        _q1, _q2, E0, G = CB.coppia(z, phi0)
        p = inviluppo(z, pK, q, N_)
        r, mu = CB.residuo(z, phi0, p)
        m = MB.misure(z, phi0, rec, p)
    info = {"N": N_, "L": L_, "w_a_L81": w81, "theta": th, "phi": fi, "E0": E0, "bloch": float(np.linalg.norm(G @ q - np.exp(-1j * E0 * S) * q)),
            "norma": abs(float(np.sum(np.abs(p) ** 2)) / N_ - 1.0), "residuo": r, "mu": mu, "misure": m}
    return p, mu, N_, L_, info, "l'inviluppo di N %.0e per la scelta migliore (theta %.4f phi %.4f), SENZA Newton, L %d; mu di Rayleigh" % (N_, th, fi, L_)


def corsa(prefisso, N_, L_, psi0, mu, da, t_fine, info, rip0=None):
    """### **Le righe di `_coppia_di_B.lunga`** *(la stessa scena, gli stessi punti, `D` e l'esame)* **a pezzi di `PEZZO`;** ### **`rip0`: lo stato e il tick da cui la serie riparte** *(la fine di `a8e0e43b`)*."""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    os.makedirs(DIR_JSON, exist_ok=True)
    os.makedirs(DIR_NPZ, exist_ok=True)
    f_rip = os.path.join(DIR_NPZ, "%s.npz" % prefisso)
    with MB.scena(N_, L_, EPS) as (rec, z, phi0, _p):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), conv0(DC):
            w_in = DC.forma(z, w0)[0]
        ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = LP.ML.Bande(Z, z["L"])
        E = ph / S
        n0 = float(np.linalg.norm(psi0))
        punti, dd = [], []
        if os.path.exists(f_rip):
            with np.load(f_rip) as dati:
                t0 = int(dati["t"])
                z["st"]["psi_h"][...] = dati["psi_h"]
            prec = [x for x in pezzi(DIR_JSON, prefisso + "_") if x["t1"] == t0]
            assert len(prec) == 1, "nessun pezzo finisce al tick dello stato di ripresa"
            prec = prec[0]
        elif rip0 is not None:
            t0 = rip0[1]
            z["st"]["psi_h"][...] = rip0[0]
            prec = None
        else:
            t0 = 0
            z["st"]["psi_h"][...] = psi0
            with SF.forma(VC.FORMA), conv0(DC):
                p = CL.punto(z, 0, w_in, w0)
            p["tau"] = 0.0
            punti.append(p)
            prec = None
        sha_rip = SFM.sha(z["st"]["psi_h"])
        if prec is not None:
            assert prec["sha_fine"] == sha_rip, "lo stato salvato NON e' quello della fine del pezzo prima"
        if t0 >= t_fine:
            print("  la corsa %s: finita" % prefisso)
            return
        t1 = min(t0 + PEZZO, t_fine)
        Ds = {}
        s0 = time.time()
        with SF.forma(VC.FORMA), conv0(DC):
            for t in range(t0 + 1, t1 + 1):
                CL.avanza(z, phi0, 1)
                if t % OGNI == 0:
                    p = CL.punto(z, t, w_in, w0)
                    p["tau"] = t * S
                    punti.append(p)
                if t % OGNI_D == 0 or t > t1 - ESAME:
                    D = np.exp(1j * mu * S * t) * z["st"]["psi_h"] - psi0
                    if t % OGNI_D == 0:
                        c = bande.coeff(D)
                        pk = np.abs(c) ** 2
                        tot = float(pk.sum())
                        dd.append({"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}})
                    if t > t1 - ESAME:
                        Ds[t] = D
        sha_fine = SFM.sha(z["st"]["psi_h"])
        tmp = f_rip.replace(".npz", "_tmp.npz")
        np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
        ts = sorted(Ds)
        rot = {gr: [bande.rotazione(Ds[a], Ds[b], (gr,), S) for a, b in zip(ts, ts[1:])] for gr in ("Ppi", "A", "P0", "B")}
        esame = {"rot": {gr: {"media": float(np.mean(v)), "dev": float(np.std(v))} for gr, v in rot.items()},
                 "E": {gr: float(np.mean(v)) + mu for gr, v in rot.items()},
                 "bande_libere": {gr: [float(E[..., list(idx)].min()), float(E[..., list(idx)].max())] for gr, idx in bande.gruppi.items()}}
        riga = {"corsa": prefisso, "partenza": da, "sha_partenza": SFM.sha(psi0), "sha_ripresa": sha_rip, "eps": EPS, "L": L_, "N": N_, "t0": t0, "t1": t1, "s": S, "mu": mu,
                "w0": w0, "w_in": w_in, "info": info, "punti": punti, "D": dd, "esame": esame, "sha_fine": sha_fine, "secondi": time.time() - s0}
        LP.scrivi_nuovo(os.path.join(DIR_JSON, "%s_%06d.jsonl" % (prefisso, t0)), riga)
        os.replace(tmp, f_rip)
    print("  la corsa %s: tick %d -> %d, w/w_in %.5f, cuore %.5f, alone %.5f, picco %.2f, |D|/|psi0| %.3e (%s); rot %s (%.0f s)"
          % (prefisso, t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], 1.0 - punti[-1]["f_3w0"], punti[-1]["picco"], dd[-1]["nD"],
             " ".join("%s %.2e" % kv for kv in dd[-1]["bande"].items()), " ".join("%s %+.4f" % (k, v["media"]) for k, v in esame["rot"].items()), riga["secondi"]))


def conv0(DC):
    import _triangoli_bassa_energia as BE
    return BE.conv(DC.ZERO)


def lunga():
    """### **(2) `B` dalla fine di `a8e0e43b`, al bit:** lo sha1 della fine DEVE essere `sha_fine` dell'ultimo pezzo; `psi0` e `mu` di `_coppia_di_B.partenza_corsa("B")`, lo sha1 DEVE essere `sha_partenza`."""
    import _stato_fermo as SFM
    vecchi = pezzi(CB.DIR_JSON, "lunga_B_")
    assert vecchi and vecchi[-1]["t1"] == CB.T_LUNGA, "la corsa di a8e0e43b non e' intera"
    psi0, mu, _da = CB.partenza_corsa("B")
    assert SFM.sha(psi0) == vecchi[0]["sha_partenza"], "psi0 NON e' la partenza di a8e0e43b"
    assert mu == vecchi[0]["mu"], "mu NON e' quello di a8e0e43b"
    with np.load(os.path.join(CB.DIR_NPZ, "lunga_B.npz")) as dati:
        assert int(dati["t"]) == CB.T_LUNGA
        fine = dati["psi_h"].copy()
    assert SFM.sha(fine) == vecchi[-1]["sha_fine"], "lo stato di db/coppia_di_B NON e' la fine di a8e0e43b"
    corsa("lunga_B", N, L, psi0, mu, "la fine di a8e0e43b al bit (la partenza %s)" % vecchi[0]["partenza"], T_TOT, {}, rip0=(fine, CB.T_LUNGA))


def robusta(nome):
    assert nome in ROBUSTE, nome
    psi0, mu, N_, L_, info, da = partenza_robusta(nome)
    corsa("robusta_%s" % nome, N_, L_, psi0, mu, da, T_ROBUSTA, info)


# ====================================================================== (4) NEWTON COL VINCOLO
def newton_bordo(eps, p0, qp, passi):
    """### **`_livelli_piatti.newton` COPIATO, col bordo:** le incognite `(psi, mu, lambda)`; `T psi - e^{-i mu s} psi + lambda u = 0`, la norma, `<u, psi> = 0`; ### **`u` il campo uniforme di `qp`.**
    ### **Il residuo e' quello SENZA `lambda`** *(lo stato fermo vero)*."""
    from scipy.sparse.linalg import LinearOperator, gmres
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    with MB.scena(N, L, eps) as (_rec, z, phi0, _p), LP.configurazione(MB.R_, MB.G_):
        A = DV.matrice(z, phi0, DV.AMP) * np.exp(-1j * MS.ALPHA0[LP.FORMA] * S)
        Lz = z["L"]
        n = z["inc"].n
        Nn = float(np.sum(np.abs(p0) ** 2))
        fo = p0.shape
        m = p0.size
        u = np.broadcast_to(qp, (n, 12)).reshape(fo) / math.sqrt(n)
        sN = math.sqrt(Nn)

        def T(psi):
            return MS.tick(z, phi0, psi, LP.FORMA)
        lam = complex(np.vdot(p0, T(p0)) / np.vdot(p0, p0))
        mu = -math.atan2(lam.imag, lam.real) / S

        def da_x(x):
            return (x[:m] + 1j * x[m:2 * m]).reshape(fo), float(x[2 * m]), complex(x[2 * m + 1], x[2 * m + 2])

        def F(x):
            psi, mu_, la = da_x(x)
            R = (T(psi) - np.exp(-1j * mu_ * S) * psi + la * sN * u).ravel() / sN
            c = complex(np.vdot(u, psi)) / sN
            return np.concatenate([R.real, R.imag, [(float(np.sum(np.abs(psi) ** 2)) - Nn) / Nn, c.real, c.imag]])

        def residuo(psi, mu_):
            return float(np.linalg.norm(T(psi) - np.exp(-1j * mu_ * S) * psi) / np.linalg.norm(psi))

        x = np.concatenate([p0.ravel().real, p0.ravel().imag, [mu, 0.0, 0.0]])
        F0 = F(x)
        c0 = abs(complex(np.vdot(u, p0))) / sN
        storia = [{"passo": 0, "residuo": residuo(p0, mu), "mu": mu, "lambda": 0.0, "vincolo": c0, "gmres": 0, "dimezzamenti": 0}]
        print("  passo 0, residuo %.3e, mu %+.9f, il vincolo %.1e" % (storia[0]["residuo"], mu, c0))
        sys.stdout.flush()
        s0 = time.time()
        migliore = (storia[0]["residuo"], p0.copy(), mu, 0j)
        for it in range(1, passi + 1):
            if storia[-1]["residuo"] < LP.SB.TOLL_RES:
                break
            nx = float(np.linalg.norm(x))
            B = np.linalg.inv(A - np.exp(-1j * float(x[2 * m]) * S) * np.eye(12))
            conti = [0]

            def prec(y):
                c = (y[:m] + 1j * y[m:2 * m]).reshape(n, 12)
                f = np.fft.fft2(c.reshape(Lz, Lz, 12), axes=(0, 1))
                gg = np.fft.ifft2(np.einsum("abij,abj->abi", B, f), axes=(0, 1)).reshape(-1)
                return np.concatenate([gg.real, gg.imag, y[2 * m:]])

            def jv(y):
                v = prec(y)
                nv = float(np.linalg.norm(v))
                if nv == 0.0:
                    return np.zeros_like(v)
                h = MS.H_REL * (1.0 + nx) / nv
                conti[0] += 1
                return (F(x + h * v) - F(x - h * v)) / (2.0 * h)
            Aop = LinearOperator((2 * m + 3, 2 * m + 3), matvec=jv, dtype=float)
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
            psi, mu, la = da_x(x)
            cv = abs(complex(np.vdot(u, psi))) / sN
            storia.append({"passo": it, "residuo": residuo(psi, mu), "mu": mu, "lambda": abs(la), "vincolo": cv, "gmres": conti[0], "dimezzamenti": k})
            if storia[-1]["residuo"] < migliore[0]:
                migliore = (storia[-1]["residuo"], psi.copy(), mu, la)
            print("  passo %d, residuo %.3e, mu %+.9f, |lambda| %.2e, il vincolo %.1e, GMRES %d, dimezzamenti %d (%.0f s)" % (it, storia[-1]["residuo"], mu, abs(la), cv, conti[0], k, time.time() - s0))
            sys.stdout.flush()
        _rm, psi, mu, la = migliore
        psi = psi * math.sqrt(Nn / float(np.sum(np.abs(psi) ** 2)))
        rf = residuo(psi, mu)
    return psi, mu, la, rf, storia, time.time() - s0, c0


def vincolo(nome):
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "vincolo_%s.json" % nome)
    assert not os.path.exists(fj), fj
    eps = MB.CASI[nome]
    with MB.scena(N, L, eps) as (rec, z, phi0, pK):
        q1, q2, E0, _G = CB.coppia(z, phi0)
        if nome == NOME_EPS:
            gr = LP.leggi(os.path.join(CB.DIR_JSON, "griglia.json"))[nome]
            th, fi = gr["minimo"]["theta"], gr["minimo"]["phi"]
            q, qp, cosa = math.cos(th) * q1 + np.exp(1j * fi) * math.sin(th) * q2, -math.sin(th) * q1 + np.exp(1j * fi) * math.cos(th) * q2, "la scelta migliore (theta %.4f phi %.4f), il partner ortogonale nullo" % (th, fi)
        else:
            q, qp, cosa = q1, q2, "q1 (spin su), lo spin giu' q2 nullo"
        sz = CB.ritratto(z, q)["sigma_z"]
        p0 = inviluppo(z, pK, q, N)
        m_in = MB.misure(z, phi0, rec, p0)
    print("### (4) NEWTON COL VINCOLO: %s (eps %g), %s; il bordo: lambda u, u il campo uniforme del partner; il criterio %g, %d passi" % (nome, eps, cosa, LP.SB.TOLL_RES, LP.SB.MAX_NEWTON))
    if nome != NOME_EPS:
        esito("DEVE PASSARE: a eps 0 q1 e' tutto spin su: sigma_z = 1 entro %g" % TOLL_SZ, abs(sz - 1.0) < TOLL_SZ, "%+.12f" % sz)
    psi, mu, la, rf, storia, sec, c0 = newton_bordo(eps, p0, qp, LP.SB.MAX_NEWTON)
    esito("DEVE PASSARE: il vincolo vale alla partenza entro %g" % TOLL_PARTENZA, c0 < TOLL_PARTENZA, "%.1e" % c0)
    with MB.scena(N, L, eps) as (rec, z, phi0, _p):
        m = MB.misure(z, phi0, rec, psi)
    giu = float(np.sum(np.abs(psi.reshape(-1, 6, 2)[:, :, 1]) ** 2) / np.sum(np.abs(psi) ** 2))
    os.makedirs(DIR_NPZ, exist_ok=True)
    tmp = os.path.join(DIR_NPZ, "vincolo_%s_tmp.npz" % nome)
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, os.path.join(DIR_NPZ, "vincolo_%s.npz" % nome))
    riga = {"nome": nome, "eps": eps, "L": L, "N": N, "cosa": cosa, "sigma_z_partenza": sz, "E0": E0, "mu": mu, "mu_meno_E0": mu - E0, "residuo_finale": rf,
            "convergito": rf < LP.SB.TOLL_RES, "lambda": abs(la), "vincolo_partenza": c0, "spin_giu": giu, "sha": SFM.sha(psi), "storia": storia, "secondi": sec,
            "misure_partenza": m_in, "misure": m, "esito": [OK[0], OK[1], FALLITE]}
    LP.scrivi_nuovo(fj, riga)
    print("  %s: %s (residuo %.3e), mu %+.9f (mu - E0 %+.5f), |lambda| %.2e; w %.3f, cuore %.5f, picco %.2f; il peso di spin giu' %.3e; la partenza w %.3f, cuore %.5f"
          % (nome, "FERMO" if riga["convergito"] else "NON CONVERGE: lo stato migliore, dichiarato", rf, mu, mu - E0, abs(la), m["w"], m["f_win"], m["picco"], giu, m_in["w"], m_in["f_win"]))
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


# ====================================================================== IL REFERTO
def finestre(pz):
    pts = [p for x in pz for p in x["punti"]]
    dd = [d for x in pz for d in x["D"]]
    w_in = pz[0]["w_in"]
    tau = np.array([p["tau"] for p in pts])
    cu_all = np.array([p["f_win"] for p in pts])
    out = []
    a0 = 0.0
    while a0 < tau[-1] - 1e-9:
        m = (tau >= a0 - 1e-9) & (tau <= a0 + FINESTRA + 1e-9)
        ii = np.nonzero(m)[0]
        cu = cu_all[m]
        md = [d for d in dd if a0 - 1e-9 <= d["t"] * pz[0]["s"] <= a0 + FINESTRA + 1e-9]
        out.append({"a": a0, "b": a0 + FINESTRA, "cuore": (float(cu[0]), float(cu[-1])), "pendenza": float(np.polyfit(tau[m], cu, 1)[0]), "oscilla": (float(cu.min()), float(cu.max())),
                    "w": (pts[ii[0]]["w"] / w_in, pts[ii[-1]]["w"] / w_in), "alone": (1.0 - pts[ii[0]]["f_3w0"], 1.0 - pts[ii[-1]]["f_3w0"]),
                    "picco": float(np.mean([pts[i]["picco"] for i in ii])), "D": md[-1] if md else None})
        a0 += FINESTRA
    dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
    return {"finestre": out, "dM": dM, "cuore0": float(cu_all[0]), "cuore1": float(cu_all[-1]), "w_fine": pts[-1]["w"] / w_in, "alone_max": max(1.0 - p["f_3w0"] for p in pts),
            "cuore_min": float(cu_all.min()), "cuore_max": float(cu_all.max()), "fine": pz[-1]["t1"]}


def stampa_finestre(fw):
    for w in fw["finestre"]:
        d = w["D"]
        print("    tau [%5.0f, %5.0f]: cuore %.5f -> %.5f (pendenza %+.2e; fra %.5f e %.5f); w/w_in %.4f -> %.4f; alone %.5f -> %.5f; picco %.1f | D %s"
              % (w["a"], w["b"], w["cuore"][0], w["cuore"][1], w["pendenza"], w["oscilla"][0], w["oscilla"][1], w["w"][0], w["w"][1], w["alone"][0], w["alone"][1], w["picco"],
                 ("%.3e (%s)" % (d["nD"], " ".join("%s %.2e" % kv for kv in d["bande"].items()))) if d else "--"))


def referto():
    import _stato_fermo as SFM
    print("=" * 130)
    print("IL SOLITONE SU B A Gamma REGGE: CONSOLIDARE (Luca 15:58): S1, eps %g, s %g, r 1, g 1, il congelato vero" % (EPS, S))
    print("  la configurazione: N %.0e L %d T_TOT %d PEZZO %d T_ROBUSTA %d ROBUSTE %s OGNI %d OGNI_D %d ESAME %d FINESTRA %g GRUPPI %s TASSI_NOTI %s TOLL_BLOCH %g TOLL_NORMA %g TOLL_PARTENZA %g TOLL_SZ %g; "
          "da _livelli_piatti: MAX_NEWTON %d TOLL_RES %g FRAZ_LARGO %.4f; L_GRANDE %d"
          % (N, L, T_TOT, PEZZO, T_ROBUSTA, ROBUSTE, OGNI, OGNI_D, ESAME, FINESTRA, GRUPPI, TASSI_NOTI, TOLL_BLOCH, TOLL_NORMA, TOLL_PARTENZA, TOLL_SZ, LP.SB.MAX_NEWTON, LP.SB.TOLL_RES, LP.FRAZ_LARGO, MB.L_GRANDE))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (k1) regge in tutte le prove, il limite del tasso sotto la mista: protetto dall'energia; (k2) una prova decade: quale, quale uscita; (k3) altro")
    print("=" * 130)
    print("### (1) IL LIMITE SUPERIORE DEL TASSO: a tau 3000 (limite_3000.json)")
    fj = os.path.join(DIR_JSON, "limite_3000.json")
    if os.path.exists(fj):
        stampa_limite(LP.leggi(fj))
    print("-" * 130)
    print("### (2) LA CORSA PIU' LUNGA: B a Gamma, eps %g, fino a tick %d (tau %.1f)" % (EPS, T_TOT, T_TOT * S))
    pz = serie_B()
    nuovi = [x for x in pz if x["t0"] >= CB.T_LUNGA]
    if nuovi:
        esito("DEVE PASSARE: la ripresa e' la fine di a8e0e43b (sha1)", nuovi[0]["sha_ripresa"] == pz[len(pz) - len(nuovi) - 1]["sha_fine"], nuovi[0]["sha_ripresa"][:8])
        esito("DEVE PASSARE: ogni pezzo riparte dalla fine del precedente (sha1)", all(a["sha_fine"] == b["sha_ripresa"] for a, b in zip(nuovi, nuovi[1:])), "%d pezzi" % len(nuovi))
        esito("DEVE PASSARE: la stessa partenza (sha1 di psi0)", len(set(x["sha_partenza"] for x in pz)) == 1, pz[0]["sha_partenza"][:8])
        fw = finestre(pz)
        esito("DEVE PASSARE: M entro %g relativo dal tick 0" % TOLL_NORMA, fw["dM"] <= TOLL_NORMA, "%.1e" % fw["dM"])
        print("  --- B: %d pezzi (%d di a8e0e43b), tick %d%s; il cuore %.5f -> %.5f (fra %.5f e %.5f), w/w_in a fine %.4f, l'alone massimo %.5f"
              % (len(pz), len(pz) - len(nuovi), fw["fine"], "" if fw["fine"] >= T_TOT else " (NON FINITA)", fw["cuore0"], fw["cuore1"], fw["cuore_min"], fw["cuore_max"], fw["w_fine"], fw["alone_max"]))
        stampa_finestre(fw)
        for x in nuovi:
            print("    le rotazioni a fine pezzo %06d: %s" % (x["t0"], " ".join("%s %+.4f (E %+.4f)" % (k, v["media"], x["esame"]["E"][k]) for k, v in x["esame"]["rot"].items())))
        print("  il limite superiore del tasso, AGGIORNATO (tick 0 .. %d):" % fw["fine"])
        stampa_limite(limite(pz))
    else:
        print("  nessun pezzo")
    print("-" * 130)
    print("### (3) LA ROBUSTEZZA: dall'inviluppo, SENZA Newton, eps %g, %d tick (N1e6_L81: il controllo dichiarato)" % (EPS, T_ROBUSTA))
    for nome in ROBUSTE:
        pr = pezzi(DIR_JSON, "robusta_%s_" % nome)
        if not pr:
            print("  --- %s: nessuna corsa" % nome)
            continue
        info = pr[0]["info"]
        esito("DEVE PASSARE: %s, q autovettore di A(Gamma) della scena entro %g" % (nome, TOLL_BLOCH), info["bloch"] < TOLL_BLOCH, "%.1e" % info["bloch"])
        esito("DEVE PASSARE: %s, la norma della partenza = N entro %g" % (nome, TOLL_PARTENZA), info["norma"] < TOLL_PARTENZA, "%.1e" % info["norma"])
        fw = finestre(pr)
        esito("DEVE PASSARE: %s, M entro %g relativo" % (nome, TOLL_NORMA), fw["dM"] <= TOLL_NORMA, "%.1e" % fw["dM"])
        print("  --- %s: N %.0e, L %d%s; la partenza: residuo per tick %.3e, mu %+.6f (mu - E0 %+.5f), w %.3f, cuore %.5f; tick %d%s"
              % (nome, info["N"], info["L"], "" if info["w_a_L81"] is None else " (w a L 81 %.3f contro L/6 %.2f)" % (info["w_a_L81"], L * LP.FRAZ_LARGO), info["residuo"], info["mu"],
                 info["mu"] - info["E0"], info["misure"]["w"], info["misure"]["f_win"], fw["fine"], "" if fw["fine"] >= T_ROBUSTA else " (NON FINITA)"))
        print("    il cuore %.5f -> %.5f (fra %.5f e %.5f), w/w_in a fine %.4f, l'alone massimo %.5f" % (fw["cuore0"], fw["cuore1"], fw["cuore_min"], fw["cuore_max"], fw["w_fine"], fw["alone_max"]))
        stampa_finestre(fw)
        stampa_limite(limite(pr))
    print("-" * 130)
    print("### (4) NEWTON COL VINCOLO")
    for nome in MB.CASI:
        fj = os.path.join(DIR_JSON, "vincolo_%s.json" % nome)
        if not os.path.exists(fj):
            print("  %s: nessuna ricerca" % nome)
            continue
        cj = LP.leggi(fj)
        with np.load(os.path.join(DIR_NPZ, "vincolo_%s.npz" % nome)) as fe:
            ok = SFM.sha(fe["psi_h"]) == cj["sha"]
        esito("DEVE PASSARE: %s, lo stato sul disco = la ricerca (sha1)" % nome, ok, cj["sha"][:8])
        esito("DEVE PASSARE: %s, i DEVE della ricerca" % nome, not cj["esito"][2], "%d/%d" % (cj["esito"][0], cj["esito"][1]))
        print("  %s (%s): %s (residuo %.3e in %d passi), mu - E0 %+.5f, |lambda| %.2e, spin giu' %.3e; w %.3f, cuore %.5f; la storia %s"
              % (nome, cj["cosa"], "FERMO" if cj["convergito"] else "NON FERMO", cj["residuo_finale"], len(cj["storia"]) - 1, cj["mu_meno_E0"], cj["lambda"], cj["spin_giu"],
                 cj["misure"]["w"], cj["misure"]["f_win"], " ".join("%.1e" % p["residuo"] for p in cj["storia"])))
    print("-" * 130)
    print("### LE LETTURE: i numeri sono quelli sopra; la parola (k1)/(k2)/(k3) nella relazione")
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--limite" in argv:
        limite_3000()
    elif "--lunga" in argv:
        lunga()
    elif "--robusta" in argv:
        robusta(argv[argv.index("--robusta") + 1])
    elif "--vincolo" in argv:
        vincolo(argv[argv.index("--vincolo") + 1])
    elif "--referto" in argv:
        referto()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
