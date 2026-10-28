# -*- coding: utf-8 -*-
r"""**LO STATO FERMO DI S1 SUL RETICOLO** *(il mandato di Luca delle `21:29` del `2026-10-28`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-28_stato_fermo_sul_reticolo.md`)*: ### **Newton sulla mappa del tick congelato** *(`VC.VUOTO` saltati, `phi` rimesso; `S1`, `s 0.3`, `N 1e6`)*,
### **`T psi = e^{-i mu s} psi` con `|psi|^2 = N`;** ### **il confronto con lo stato iniziale e finale di `40061005`;** ### **una corsa dello stato fermo, `L 81`, `3000` di tempo fisico.**

> ### **Gli stati in `db/stato_fermo/`** *(ignorato da git: il dato e' il comando)*; ### **la storia di Newton e i punti della corsa in `doc/referti_l2/stato_fermo/`.**

    python csv/_stato_fermo.py --cerca <81|120>
    python csv/_stato_fermo.py --pezzo                  (da ripetere: ogni volta il pezzo dopo, L 81)
    python csv/_stato_fermo.py --referto > doc/referti_l2/stato_fermo.txt
"""
import hashlib
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

S = 0.3
TAGLIE = (81, 120)
L_CORSA = 81
TOLL_RES = 1e-9                # ### il criterio di arresto, dichiarato prima
MAX_NEWTON = 30
GMRES_RTOL = 1e-3
GMRES_RESTART = 60
GMRES_MAXITER = 10
DIMEZZA = 8
H_REL = 1e-5                   # ### il passo della differenza centrata, relativo
T_MAX = 10000                  # ### 3000 di tempo fisico a s 0.3
PEZZO = 2000
OGNI = 10
FINESTRA = 500.0
TOLL_NORMA = 1e-10
STATI = os.path.join(RADICE, "db", "stato_fermo")
PUNTI = os.path.join(RADICE, "doc", "referti_l2", "stato_fermo")
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


def sha(a):
    return hashlib.sha1(a.tobytes()).hexdigest()


def scena(L):
    import _congelato_lungo as CL
    rec, z = CL.iniziale(L, "uniforme")
    return rec, z, z["st"]["phi_h"].copy(), z["st"]["psi_h"].copy()


def tick(z, phi0, psi_h):
    """### **`T`: un tick congelato vero** *(le righe di `_congelato_lungo.avanza` dentro i contesti di `_congelato_lungo.pezzo`)*."""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    z["st"]["psi_h"][...] = psi_h
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        CL.avanza(z, phi0, 1)
    return z["st"]["psi_h"].copy()


def residuo(z, phi0, psi_h, mu):
    Tp = tick(z, phi0, psi_h)
    return float(np.linalg.norm(Tp - np.exp(-1j * mu * S) * psi_h) / np.linalg.norm(psi_h)), Tp


def cerca(L):
    """### **Newton sulla mappa del tick:** ### **incognite `psi` e `mu`; GMRES senza matrice, `J v` per differenza CENTRATA;**
    ### **precondizionato a destra con `(A(k) - lambda)^{-1}`, `A(k)` il tick libero di `_dove_va_la_materia.matrice`;** ### **il passo dimezzato se il residuo non cala.**"""
    from scipy.sparse.linalg import LinearOperator, gmres
    import _dove_va_la_materia as DV
    rec, z, phi0, p0 = scena(L)
    A = DV.matrice(z, phi0, DV.AMP)
    n = z["inc"].n
    N = float(np.sum(np.abs(p0) ** 2))
    forma = p0.shape
    m = p0.size
    lam = complex(np.vdot(p0, tick(z, phi0, p0)) / np.vdot(p0, p0))
    mu = -math.atan2(lam.imag, lam.real) / S

    def a_x(psi, mu_):
        v = psi.ravel()
        return np.concatenate([v.real, v.imag, [mu_]])

    def da_x(x):
        return (x[:m] + 1j * x[m:2 * m]).reshape(forma), float(x[2 * m])

    def F(x):
        psi, mu_ = da_x(x)
        R = (tick(z, phi0, psi) - np.exp(-1j * mu_ * S) * psi).ravel() / math.sqrt(N)
        return np.concatenate([R.real, R.imag, [(float(np.sum(np.abs(psi) ** 2)) - N) / N]])

    x = a_x(p0, mu)
    F0 = F(x)
    storia = []
    r0, _ = residuo(z, phi0, p0, mu)
    storia.append({"passo": 0, "residuo": r0, "mu": mu, "gmres": 0, "tick": 1, "dimezzamenti": 0})
    print("  L %d: passo 0, residuo %.3e, mu %+.9f" % (L, r0, mu))
    sys.stdout.flush()
    conti = [0]
    s0 = time.time()
    for it in range(1, MAX_NEWTON + 1):
        if storia[-1]["residuo"] < TOLL_RES:
            break
        nx = float(np.linalg.norm(x))
        B = np.linalg.inv(A - np.exp(-1j * float(x[2 * m]) * S) * np.eye(12))

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
            conti[0] += 2
            return (F(x + h * v) - F(x - h * v)) / (2.0 * h)
        Aop = LinearOperator((2 * m + 1, 2 * m + 1), matvec=jv, dtype=float)
        c0 = conti[0]
        y, _info = gmres(Aop, -F0, rtol=GMRES_RTOL, restart=GMRES_RESTART, maxiter=GMRES_MAXITER)
        dx = prec(y)
        ng = conti[0] - c0
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
        r, _ = residuo(z, phi0, psi, mu)
        storia.append({"passo": it, "residuo": r, "mu": mu, "gmres": ng // 2, "tick": ng + k + 2, "dimezzamenti": k})
        print("  L %d: passo %d, residuo %.3e, mu %+.9f, GMRES %d, dimezzamenti %d (%.0f s)" % (L, it, r, mu, ng // 2, k, time.time() - s0))
        sys.stdout.flush()
    psi, mu = da_x(x)
    psi *= math.sqrt(N / float(np.sum(np.abs(psi) ** 2)))
    r, _ = residuo(z, phi0, psi, mu)
    os.makedirs(STATI, exist_ok=True)
    os.makedirs(PUNTI, exist_ok=True)
    f = os.path.join(STATI, "fermo_L%d.npz" % L)
    tmp = os.path.join(STATI, "fermo_L%d_tmp.npz" % L)
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, f)
    riga = {"L": L, "s": S, "N": N, "mu": mu, "residuo_finale": r, "storia": storia, "secondi": time.time() - s0, "sha": sha(psi),
            "convergito": r < TOLL_RES}
    fj = os.path.join(PUNTI, "cerca_L%d.json" % L)
    assert not os.path.exists(fj), fj
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    with open(fj, "xb") as fh:
        fh.write(dati)
    print("  L %d: residuo finale %.3e (rinormalizzato), mu %+.9f; %s" % (L, r, mu, "CONVERGE" if r < TOLL_RES else "NON CONVERGE"))


def pezzo():
    import _congelato_lungo as CL
    L = L_CORSA
    rec, z, phi0, p0 = scena(L)
    w0 = rec["larghezza"]
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        w_in = DC.forma(z, w0)[0]                      # ### la w_in dello stato iniziale di 40061005: le grandezze confrontabili
    f_stato = os.path.join(STATI, "corsa_L%d.npz" % L)
    t0 = 0
    punti = []
    if os.path.exists(f_stato):
        dati = np.load(f_stato)
        t0 = int(dati["t"])
        z["st"]["psi_h"][...] = dati["psi_h"]
        prec = json.loads(io.open(os.path.join(PUNTI, "corsa_L%d_%05d.jsonl" % (L, t0 - PEZZO)), encoding="utf-8").read())
        assert prec["sha_fine"] == sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
    else:
        cj = json.loads(io.open(os.path.join(PUNTI, "cerca_L%d.json" % L), encoding="utf-8").read())
        assert cj["convergito"], "lo stato NON e' fermo (residuo %.3e): evolverlo e' una decisione di Luca" % cj["residuo_finale"]
        fe = np.load(os.path.join(STATI, "fermo_L%d.npz" % L))
        assert sha(fe["psi_h"]) == cj["sha"], "lo stato fermo NON e' quello della ricerca"
        z["st"]["psi_h"][...] = fe["psi_h"]
        punti.append(CL.punto(z, 0, w_in, w0))
    if t0 >= T_MAX:
        print("  corsa L %d: finita" % L)
        return
    t1 = min(t0 + PEZZO, T_MAX)
    s0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        for t in range(t0 + 1, t1 + 1):
            CL.avanza(z, phi0, 1)
            if t % OGNI == 0:
                punti.append(CL.punto(z, t, w_in, w0))
    riga = {"L": L, "t0": t0, "t1": t1, "w0": w0, "w_in": w_in, "punti": punti, "sha_fine": sha(z["st"]["psi_h"]), "secondi": time.time() - s0}
    fp = os.path.join(PUNTI, "corsa_L%d_%05d.jsonl" % (L, t0))
    assert not os.path.exists(fp), fp
    dati = (json.dumps(riga, sort_keys=True) + "\n").encode("utf-8")
    with open(fp, "xb") as fh:
        fh.write(dati)
    tmp = os.path.join(STATI, "corsa_L%d_tmp.npz" % L)
    np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
    os.replace(tmp, f_stato)
    print("  corsa L %d: tick %d -> %d, w/w_in %.5f, cuore %.5f (%.0f s)" % (L, t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], riga["secondi"]))


def distanza(a, b):
    return 1.0 - abs(complex(np.vdot(a, b))) ** 2 / (float(np.vdot(a, a).real) * float(np.vdot(b, b).real))


def referto():
    import _congelato_lungo as CL
    import _cuore_e_alone as CE
    import _energia_del_legame as EL
    import _triangoli_forza as TF
    print("=" * 130)
    print("LO STATO FERMO DI S1 SUL RETICOLO (Luca 21:29): Newton sulla mappa del tick congelato vero; S1, s %g, N 1e6, zero simmetrico, cs spento, il vuoto uniforme" % S)
    print("=" * 130)
    print("  la configurazione: S %g TAGLIE %s L_CORSA %d TOLL_RES %g MAX_NEWTON %d GMRES_RTOL %g GMRES_RESTART %d GMRES_MAXITER %d DIMEZZA %d H_REL %g T_MAX %d PEZZO %d OGNI %d FINESTRA %g TOLL_NORMA %g"
          % (S, TAGLIE, L_CORSA, TOLL_RES, MAX_NEWTON, GMRES_RTOL, GMRES_RESTART, GMRES_MAXITER, DIMEZZA, H_REL, T_MAX, PEZZO, OGNI, FINESTRA, TOLL_NORMA))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (a) lo stato fermo piu' largo dell'iniziale, piu' vicino al finale, e evoluto il cuore regge: l'assestamento; (b) esiste ma evoluto si svuota: VK sbaglia sul reticolo;"
          " (c) non si trova con la norma data; (d) altro")
    wK = TF.coppia_K(0.0, S)[0]["w"]
    for L in TAGLIE:
        print("-" * 130)
        cj = json.loads(io.open(os.path.join(PUNTI, "cerca_L%d.json" % L), encoding="utf-8").read())
        print("### L %d: LA RICERCA (Newton)" % L)
        for p in cj["storia"]:
            print("  passo %2d: residuo %.3e  mu %+.9f  GMRES %4d  dimezzamenti %d" % (p["passo"], p["residuo"], p["mu"], p["gmres"], p["dimezzamenti"]))
        esito("DEVE PASSARE: L %d, il residuo finale sotto %g (il criterio di arresto)" % (L, TOLL_RES), cj["convergito"], "%.3e in %d passi, %.0f s" % (cj["residuo_finale"], len(cj["storia"]) - 1, cj["secondi"]))
        rec, z, phi0, p0 = scena(L)
        fe = np.load(os.path.join(STATI, "fermo_L%d.npz" % L))
        pf = fe["psi_h"]
        esito("DEVE PASSARE: L %d, lo stato fermo sul disco = quello della ricerca (sha1)" % L, sha(pf) == cj["sha"], "")
        N = float(np.sum(np.abs(p0) ** 2))
        dn = abs(float(np.sum(np.abs(pf) ** 2)) / N - 1.0)
        esito("DEVE PASSARE: L %d, la norma dello stato fermo = N entro 1e-12" % L, dn < 1e-12, "%.1e" % dn)
        r_f, _ = residuo(z, phi0, pf, float(fe["mu"]))
        r_0 = cj["storia"][0]["residuo"]
        print("  il residuo ricalcolato dello stato %s: %.3e (lo stato iniziale: %.3e)" % ("FERMO" if cj["convergito"] else "QUASI FERMO (il criterio non e' raggiunto)", r_f, r_0))
        esito("DEVE PASSARE: L %d, il residuo ricalcolato = quello della ricerca" % L, abs(r_f - cj["residuo_finale"]) <= 1e-12 + 1e-9 * cj["residuo_finale"], "%.3e" % r_f)
        d1 = np.load(os.path.join(CL.STATI, CL.nome(L, "uniforme") + ".npz"))
        righe, _p = CL.serie(L, "uniforme")
        esito("DEVE PASSARE: L %d, lo stato finale di 40061005 = sha_fine" % L, CL.sha(d1["psi_h"]) == righe[-1]["sha_fine"], "")
        p1 = d1["psi_h"]
        w_in, w0 = righe[0]["w_in"], righe[0]["w0"]
        mu_f = float(fe["mu"])
        print("  mu: lo stato fermo %+.9f; lo stato iniziale (la fase di <psi, T psi>) %+.9f; -mu s - w_K(A) per lo stato fermo %+.6f, per l'iniziale %+.6f; mu del risolutore %+.6f"
              % (mu_f, cj["storia"][0]["mu"], -mu_f * S - wK, -cj["storia"][0]["mu"] * S - wK, rec["mu"]))
        stati = (("iniziale", p0), ("fermo", pf), ("finale", p1))
        prof = {}
        for nome_, p in stati:
            z["st"]["psi_h"][...] = p
            pt = CL.punto(z, 0, w_in, w0)
            rho = EL.densita(z["inc"], z["st"])[0]
            _M, c, d = CE.baricentro(z, rho)
            prof[nome_] = CE.anelli(rho, d)
            print("  %-9s: w %.4f (w/w_in %.4f), cuore f_win %.5f, entro 3 w0 %.5f, picco per nodo %.2f, FWHM %.4f, il baricentro (%+.2e, %+.2e)"
                  % (nome_, pt["w"], pt["w"] / w_in, pt["f_win"], pt["f_3w0"], pt["picco"], CE.fwhm(prof[nome_]), c[0], c[1]))
        for (a, pa), (b, pb) in ((stati[0], stati[1]), (stati[1], stati[2]), (stati[0], stati[2])):
            print("  la distanza 1 - |<a|b>|^2: %-9s - %-9s %.5e" % (a, b, distanza(pa, pb)))
        print("  il profilo per anelli, r 0..24 (rho per nodo):")
        for k in range(0, 25):
            print("    r %2d: iniziale %12.5e  fermo %12.5e  finale %12.5e" % (k, prof["iniziale"][k], prof["fermo"][k], prof["finale"][k]))
    print("-" * 130)
    print("### LA CORSA DELLO STATO FERMO, L %d, il congelato vero, %d tick (tempo fisico %g)" % (L_CORSA, T_MAX, T_MAX * S))
    righe = []
    if os.path.isdir(PUNTI):
        for n in sorted(os.listdir(PUNTI)):
            if n.startswith("corsa_L%d_" % L_CORSA) and n.endswith(".jsonl"):
                righe.append(json.loads(io.open(os.path.join(PUNTI, n), encoding="utf-8").read()))
    righe.sort(key=lambda r: r["t0"])
    for a, b in zip(righe, righe[1:]):
        assert a["t1"] == b["t0"], ("un buco fra i pezzi", a["t1"], b["t0"])
    pts = [p for r in righe for p in r["punti"]]
    if not righe:
        print("  la corsa NON e' partita: lo stato non e' fermo secondo il criterio (il task history, sezione 6)")
    else:
        esito("DEVE PASSARE: la corsa e' completa (%d tick)" % T_MAX, righe[-1]["t1"] == T_MAX, "")
    if pts:
        dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
        esito("DEVE PASSARE: M entro %g relativo" % TOLL_NORMA, dM <= TOLL_NORMA, "%.1e" % dM)
        w_in = righe[0]["w_in"]
        b40 = {p["t"]: p for r in CL.serie(L_CORSA, "uniforme")[0] for p in r["punti"]}
        tau = np.array([p["tau"] for p in pts])
        q = np.array([p["w"] / w_in for p in pts])
        cu = np.array([p["f_win"] for p in pts])
        al = np.array([1.0 - p["f_3w0"] for p in pts])
        pk = np.array([p["picco"] / pts[0]["picco"] for p in pts])
        a = 0.0
        while a < tau[-1] - 1e-9:
            m = (tau >= a - 1e-9) & (tau <= a + FINESTRA + 1e-9)
            pw = np.polyfit(tau[m], q[m], 1)[0]
            pc = np.polyfit(tau[m], cu[m], 1)[0]
            t_a, t_b = int(round(tau[m][0] / S)), int(round(tau[m][-1] / S))
            print("  tau [%6.0f, %6.0f]: w/w_in da %.5f a %.5f (pendenza %+.3e); cuore da %.5f a %.5f (pendenza %+.3e); alone da %.5f a %.5f; picco relativo medio %.5f | 40061005: cuore da %.5f a %.5f"
                  % (a, a + FINESTRA, q[m][0], q[m][-1], pw, cu[m][0], cu[m][-1], pc, al[m][0], al[m][-1], pk[m].mean(), b40[t_a]["f_win"], b40[t_b]["f_win"]))
            a += FINESTRA
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    s_vero = VC.S
    try:
        if argv[:1] == ["--cerca"]:
            L = int(argv[1])
            assert L in TAGLIE, L
            cerca(L)
        elif argv[:1] == ["--pezzo"]:
            pezzo()
        elif argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.S = s_vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
