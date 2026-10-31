# -*- coding: utf-8 -*-
r"""**IL SOLITONE SU `B` A `Gamma`: LA SCELTA DENTRO LA COPPIA E LA CORSA LUNGA ANCHE SENZA STATO FERMO** *(UNA PROVA, NESSUNA MODIFICA AL NUCLEO; il mandato di Luca delle `13:52` del `2026-10-31`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-31_coppia_di_B.md`)*:
### **(1) `q(theta, phi) = cos(theta) q1 + e^{i phi} sin(theta) q2` sulla coppia di `B` a `Gamma`, lo stesso inviluppo: il residuo per tick su una griglia `7 x 8`; (2) Newton dalla scelta migliore;**
### **(3) a `eps 0.5` due corse di `20000` tick: `B` (lo stato fermo o il migliore) e `AK` (`A` a `K` dallo stato iniziale della scena).** ### **Importa `_massimo_di_B` (la scena a `eps`, la partenza, Newton).**

    python csv/_coppia_di_B.py --griglia > doc/referti_l2/coppia_di_B/griglia.txt
    python csv/_coppia_di_B.py --cerca e05 > doc/referti_l2/coppia_di_B/cerca_e05.txt      # idem e0
    python csv/_coppia_di_B.py --lunga B                # un pezzo; si ripete finche' dice "finita"; idem AK
    python csv/_coppia_di_B.py --referto > doc/referti_l2/coppia_di_B.txt
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

import _massimo_di_B as MB                                     # noqa: E402

LP = MB.LP
S = MB.S
N = MB.N
L = MB.L_SCENA
TETA = tuple(i * (math.pi / 2.0) / 6.0 for i in range(7))
FI = tuple(j * 2.0 * math.pi / 8.0 for j in range(8))
CHI = FI                        # ### il controllo: le 8 fasi globali di q1 (una simmetria esatta del tick)
FATTORE = LP.FATTORE_DEROGA     # ### dipende se max - min > 10 s0
TOLL_ORTO = 1e-12
TOLL_BLOCH = MB.TOLL_BLOCH
T_LUNGA = 20000                 # ### 3000 unita' di tempo a s 0.15
PEZZO = MB.PEZZO
OGNI = MB.OGNI
OGNI_D = MB.OGNI_D
ESAME = MB.ESAME
FINESTRA = LP.FINESTRA          # ### 500 unita' di tempo
EPS_LUNGA = 0.5
CORSE = ("B", "AK")
TOLL_NORMA = MB.TOLL_NORMA
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "coppia_di_B")
DIR_NPZ = os.path.join(RADICE, "db", "coppia_di_B")
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


def coppia(z, phi0):
    """### **`q1`, `q2`: le due colonne della base QR di `MB.bloch_B`** *(le stesse righe, tutte e due le colonne)*; `E0`, la matrice di `Gamma`."""
    import _dove_va_la_materia as DV
    A = DV.matrice(z, phi0, DV.AMP)
    G = A[0, 0]
    lam, V = np.linalg.eig(G)
    E = -np.angle(lam) / S
    o = np.argsort(E)
    top = [int(o[-2]), int(o[-1])]
    Q = np.linalg.qr(V[:, top])[0]
    return Q[:, 0], Q[:, 1], float(np.mean(E[top])), G


def ritratto(z, q):
    """### **`sigma_z`, l'elicita' media `sum_e q_e^+ (sigma.n_e) q_e` (`n_e` il versore dell'arco, `mot.geo.n`), il peso per estremita'.**
    ### ⚠ **Le `6` righe del blocco sono la CELLA, non il nodo** *(3 archi, le due estremita' di ciascuno: `inc.nodo[:6]` = `0, 81, 0, 1, 0, 82`)*: ### **per uno stato di `Gamma`, uniforme, il peso sulle estremita' della cella e' quello su ogni nodo.**"""
    inc = z["inc"]
    assert np.all(inc.nodo[0:6:2] == inc.nodo[0]), "le estremita' pari del blocco 0 non stanno sullo stesso nodo"
    n = z["mot"].geo.n[:6]
    assert np.allclose(n[0::2], -n[1::2], atol=1e-12), "le due estremita' di un arco non hanno versori opposti"
    qe = q.reshape(6, 2)
    sz = float(np.sum(np.abs(qe[:, 0]) ** 2 - np.abs(qe[:, 1]) ** 2))
    el = 0.0
    for e in range(6):
        nx, ny, nz = n[e]
        H = np.array([[nz, nx - 1j * ny], [nx + 1j * ny, -nz]])
        el += float(np.real(np.vdot(qe[e], H @ qe[e])))
    return {"sigma_z": sz, "elicita": el, "estremita": [float(x) for x in np.sum(np.abs(qe) ** 2, axis=1)], "n": [[float(x) for x in v] for v in n]}


def residuo(z, phi0, psi):
    import _modo_al_variare_di_s as MS
    T = MS.tick(z, phi0, psi, LP.FORMA)
    lam = complex(np.vdot(psi, T) / np.vdot(psi, psi))
    return float(np.linalg.norm(T - lam * psi) / np.linalg.norm(psi)), -math.atan2(lam.imag, lam.real) / S


def stato_q(inv, q, shape):
    p = inv[:, None] * q[None, :]
    p *= math.sqrt(N / float(np.sum(np.abs(p) ** 2)))
    return p.reshape(shape)


# ====================================================================== (1) LA GRIGLIA
def griglia():
    fj = os.path.join(DIR_JSON, "griglia.json")
    assert not os.path.exists(fj), fj
    print("### (1) LA SCELTA DENTRO LA COPPIA: q(theta, phi) = cos(theta) q1 + e^{i phi} sin(theta) q2, l'inviluppo di S1; theta %s; phi %s; il residuo per tick |T psi - lambda psi|/|psi|"
          % (" ".join("%.4f" % x for x in TETA), " ".join("%.4f" % x for x in FI)))
    out = {}
    for nome, eps in MB.CASI.items():
        with MB.scena(N, L, eps) as (_rec, z, phi0, pK):
            n = z["inc"].n
            inv = np.linalg.norm(pK.reshape(n, 12), axis=1)
            q1, q2, E0, G = coppia(z, phi0)
            o = float(max(abs(np.vdot(q1, q2)), abs(np.vdot(q1, q1) - 1), abs(np.vdot(q2, q2) - 1)))
            esito("DEVE PASSARE: %s, q1 e q2 ortonormali entro %g" % (nome, TOLL_ORTO), o < TOLL_ORTO, "%.1e" % o)
            rq = {k: ritratto(z, q) for k, q in (("q1", q1), ("q2", q2))}
            print("  --- %s (eps %g): E0 %+.6f" % (nome, eps, E0))
            for k, r in rq.items():
                print("    %s: sigma_z %+.5f, l'elicita' media %+.5f, le 6 estremita' %s" % (k, r["sigma_z"], r["elicita"], " ".join("%.4f" % x for x in r["estremita"])))
            print("    i versori n_e delle 6 estremita' del nodo 0: %s" % "  ".join("(%+.3f %+.3f %+.3f)" % tuple(v) for v in rq["q1"]["n"]))
            rz = [residuo(z, phi0, stato_q(inv, np.exp(1j * c) * q1, pK.shape))[0] for c in CHI]
            s0 = float(max(rz) - min(rz))
            print("    il controllo (q1 per 8 fasi globali): il residuo %.10e .. %.10e, lo scarto s0 %.2e" % (min(rz), max(rz), s0))
            tab, bloch = [], 0.0
            for th in TETA:
                for fi in FI:
                    q = math.cos(th) * q1 + np.exp(1j * fi) * math.sin(th) * q2
                    bloch = max(bloch, float(np.linalg.norm(G @ q - np.exp(-1j * E0 * S) * q)))
                    r, mu = residuo(z, phi0, stato_q(inv, q, pK.shape))
                    tab.append({"theta": th, "phi": fi, "residuo": r, "mu": mu})
                    if th == 0.0:
                        break       # ### a theta 0 phi non conta: un punto solo
            esito("DEVE PASSARE: %s, ogni q(theta, phi) e' autovettore di A(Gamma) entro %g" % (nome, TOLL_BLOCH), bloch < TOLL_BLOCH, "%.1e" % bloch)
            rr = np.array([x["residuo"] for x in tab])
            dip = float(rr.max() - rr.min()) > FATTORE * s0
            mi = tab[int(np.argmin(rr))]
            print("    la griglia (%d punti; a theta 0 uno solo): il residuo per theta (righe) e phi (colonne):" % len(tab))
            for th in TETA:
                riga = [x["residuo"] for x in tab if x["theta"] == th]
                print("      theta %.4f: %s" % (th, " ".join("%.4e" % v for v in riga)))
            print("    ### il residuo da %.4e a %.4e (max - min %.2e contro %g s0 = %.2e): %s; il minimo a theta %.4f phi %.4f (residuo %.4e, mu %+.6f; q1 da solo %.4e)"
                  % (rr.min(), rr.max(), rr.max() - rr.min(), FATTORE, FATTORE * s0, "DIPENDE DALLA SCELTA" if dip else "### NON DIPENDE: LA ROTAZIONE DENTRO LA COPPIA E' UNA DIREZIONE LIBERA",
                     mi["theta"], mi["phi"], mi["residuo"], mi["mu"], tab[0]["residuo"]))
            out[nome] = {"eps": eps, "E0": E0, "ritratto": rq, "s0": s0, "griglia": tab, "dipende": dip, "minimo": mi}
    LP.scrivi_nuovo(fj, out)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


# ====================================================================== (2) NEWTON DALLA SCELTA MIGLIORE
def cerca(nome):
    import _stato_fermo as SFM
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome)
    assert not os.path.exists(fj), fj
    gr = LP.leggi(os.path.join(DIR_JSON, "griglia.json"))[nome]
    assert gr["dipende"], "la rotazione dentro la coppia e' una direzione libera: si scrive e non si insiste (il task history, punto 2)"
    eps, th, fi = MB.CASI[nome], gr["minimo"]["theta"], gr["minimo"]["phi"]
    with MB.scena(N, L, eps) as (_rec, z, phi0, pK):
        inv = np.linalg.norm(pK.reshape(z["inc"].n, 12), axis=1)
        q1, q2, E0, _G = coppia(z, phi0)
        p0 = stato_q(inv, math.cos(th) * q1 + np.exp(1j * fi) * math.sin(th) * q2, pK.shape)
    print("### (2) NEWTON DALLA SCELTA MIGLIORE: %s (eps %g), theta %.4f phi %.4f (residuo per tick %.4e); _livelli_piatti.newton, il criterio di 26300537 (%g, %d passi)"
          % (nome, eps, th, fi, gr["minimo"]["residuo"], LP.SB.TOLL_RES, LP.SB.MAX_NEWTON))
    with MB.newton_a(eps):
        psi, mu, rf, storia, sec = LP.newton(MB.R_, MB.G_, N, p0, "%s-coppia" % nome, LP.SB.MAX_NEWTON, L)
    with MB.scena(N, L, eps) as (rec, z, phi0, _p):
        m = MB.misure(z, phi0, rec, psi)
    os.makedirs(DIR_NPZ, exist_ok=True)
    tmp = os.path.join(DIR_NPZ, "fermo_%s_tmp.npz" % nome)
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, os.path.join(DIR_NPZ, "fermo_%s.npz" % nome))
    riga = {"nome": nome, "eps": eps, "L": L, "theta": th, "phi": fi, "E0": E0, "mu": mu, "mu_meno_E0": mu - E0, "residuo_finale": rf, "convergito": rf < LP.SB.TOLL_RES,
            "largo": m["w"] > L * LP.FRAZ_LARGO, "sha": SFM.sha(psi), "storia": storia, "secondi": sec, "misure": m}
    LP.scrivi_nuovo(fj, riga)
    print("  %s: %s (residuo %.3e), mu %+.9f (mu - E0 %+.5f); w %.3f, cuore %.5f, picco %.2f, alpha del cuore %.5f; la storia %s"
          % (nome, "FERMO" if riga["convergito"] else "NON CONVERGE: lo stato migliore, dichiarato", rf, mu, mu - E0, m["w"], m["f_win"], m["picco"], m["alpha_cuore"],
             " ".join("%.1e" % p["residuo"] for p in storia)))


# ====================================================================== (3) LE CORSE LUNGHE
def partenza_corsa(chi):
    """### **`B`:** lo stato fermo del punto `2` se c'e', altrimenti il residuo piu' basso fra il punto `2` e `ab7226e7`; ### **`AK`:** lo stato iniziale della scena a `eps 0.5`, `mu` di Rayleigh."""
    import _stato_fermo as SFM
    if chi == "AK":
        with MB.scena(N, L, EPS_LUNGA) as (_rec, z, phi0, pK):
            _r, mu = residuo(z, phi0, pK)
        return pK, mu, "lo stato iniziale della scena (l'inviluppo per Q_K e la fase di K), mu di Rayleigh"
    cand = []
    nome = [k for k, v in MB.CASI.items() if v == EPS_LUNGA][0]
    fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome)
    if os.path.exists(fj):
        cj = LP.leggi(fj)
        with np.load(os.path.join(DIR_NPZ, "fermo_%s.npz" % nome)) as fe:
            psi, mu = fe["psi_h"].copy(), float(fe["mu"])
        assert SFM.sha(psi) == cj["sha"]
        cand.append((cj["residuo_finale"], psi, mu, "il punto 2 (cerca_%s.json, %s)" % (nome, "FERMO" if cj["convergito"] else "NON FERMO")))
    psi, mu, cj = MB.stato(nome)
    cand.append((cj["residuo_finale"], psi, mu, "ab7226e7 (massimo_di_B cerca_%s_L81.json, NON FERMO)" % nome))
    r, psi, mu, da = min(cand, key=lambda x: x[0])
    return psi, mu, "%s, residuo %.3e" % (da, r)


def nome_pezzo(chi, t0):
    return os.path.join(DIR_JSON, "lunga_%s_%05d.jsonl" % (chi, t0))


def lunga(chi):
    """### **Le righe di `MB.lunga`, con la partenza di `partenza_corsa`;** ### **lo stato di ripresa DEVE essere la fine del pezzo prima** *(sha1)*."""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    assert chi in CORSE, chi
    f_rip = os.path.join(DIR_NPZ, "lunga_%s.npz" % chi)
    psi0, mu, da = partenza_corsa(chi)
    with MB.scena(N, L, EPS_LUNGA) as (rec, z, phi0, _p):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = LP.ML.Bande(Z, z["L"])
        E = ph / S
        n0 = float(np.linalg.norm(psi0))
        t0 = 0
        punti, dd = [], []
        if os.path.exists(f_rip):
            with np.load(f_rip) as dati:
                t0 = int(dati["t"])
                z["st"]["psi_h"][...] = dati["psi_h"]
            prec = LP.leggi(nome_pezzo(chi, t0 - PEZZO))
            assert prec["sha_fine"] == SFM.sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
        else:
            assert not os.path.exists(nome_pezzo(chi, 0)), "pezzi scritti ma nessuno stato di ripresa"
            z["st"]["psi_h"][...] = psi0
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                p = CL.punto(z, 0, w_in, w0)
            p["tau"] = 0.0
            punti.append(p)
        if t0 >= T_LUNGA:
            print("  la corsa lunga %s: finita" % chi)
            return
        t1 = min(t0 + PEZZO, T_LUNGA)
        Ds = {}
        s0 = time.time()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
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
        riga = {"corsa": chi, "partenza": da, "sha_partenza": SFM.sha(psi0), "eps": EPS_LUNGA, "L": L, "N": N, "t0": t0, "t1": t1, "s": S, "mu": mu, "w0": w0, "w_in": w_in,
                "punti": punti, "D": dd, "esame": esame, "sha_fine": sha_fine, "secondi": time.time() - s0}
        LP.scrivi_nuovo(nome_pezzo(chi, t0), riga)
        os.replace(tmp, f_rip)
    print("  la corsa lunga %s: tick %d -> %d, w/w_in %.5f, cuore %.5f, picco %.2f, |D|/|psi0| %.3e (%s); rot %s (%.0f s)"
          % (chi, t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], punti[-1]["picco"], dd[-1]["nD"], " ".join("%s %.3f" % kv for kv in dd[-1]["bande"].items()),
             " ".join("%s %+.4f" % (k, v["media"]) for k, v in esame["rot"].items()), riga["secondi"]))


# ====================================================================== IL REFERTO
def finestre(chi):
    pz = sorted([LP.leggi(os.path.join(DIR_JSON, n)) for n in os.listdir(DIR_JSON) if n.startswith("lunga_%s_" % chi)], key=lambda x: x["t0"])
    if not pz:
        return None
    for x, y in zip(pz, pz[1:]):
        assert x["t1"] == y["t0"], ("un buco fra i pezzi", chi, x["t1"], y["t0"])
    assert len(set(p["sha_partenza"] for p in pz)) == 1, "i pezzi di %s non hanno la stessa partenza" % chi
    pts = [p for x in pz for p in x["punti"]]
    dd = [d for x in pz for d in x["D"]]
    w_in = pz[0]["w_in"]
    tau = np.array([p["tau"] for p in pts])
    out = []
    a0 = 0.0
    while a0 < tau[-1] - 1e-9:
        m = (tau >= a0 - 1e-9) & (tau <= a0 + FINESTRA + 1e-9)
        cu = np.array([p["f_win"] for p in pts])[m]
        md = [d for d in dd if a0 - 1e-9 <= d["t"] * S <= a0 + FINESTRA + 1e-9]
        out.append({"a": a0, "b": a0 + FINESTRA, "cuore": (float(cu[0]), float(cu[-1])), "pendenza": float(np.polyfit(tau[m], cu, 1)[0]),
                    "oscilla": (float(cu.min()), float(cu.max())),
                    "w": (pts[int(np.nonzero(m)[0][0])]["w"] / w_in, pts[int(np.nonzero(m)[0][-1])]["w"] / w_in),
                    "alone": (1.0 - pts[int(np.nonzero(m)[0][0])]["f_3w0"], 1.0 - pts[int(np.nonzero(m)[0][-1])]["f_3w0"]),
                    "picco": float(np.mean([p["picco"] for p, k in zip(pts, m) if k])), "D": md[-1] if md else None})
        a0 += FINESTRA
    dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
    return {"pezzi": pz, "finestre": out, "dM": dM, "fine": pz[-1]["t1"], "cuore0": pts[0]["f_win"], "cuore1": pts[-1]["f_win"], "w_fine": pts[-1]["w"] / w_in}


def referto():
    import _stato_fermo as SFM
    print("=" * 130)
    print("LA SCELTA DENTRO LA COPPIA E LA CORSA LUNGA ANCHE SENZA STATO FERMO (Luca 13:52): il massimo di B a Gamma, S1, N %.0e, s %g, r 1, g 1, il congelato vero, L %d" % (N, S, L))
    print("  la configurazione: TETA %s FI %s FATTORE %g TOLL_ORTO %g TOLL_BLOCH %g T_LUNGA %d PEZZO %d OGNI %d OGNI_D %d ESAME %d FINESTRA %g EPS_LUNGA %g CORSE %s TOLL_NORMA %g; da _strada_b_r: MAX_NEWTON %d TOLL_RES %g"
          % (["%.4f" % x for x in TETA], ["%.4f" % x for x in FI], FATTORE, TOLL_ORTO, TOLL_BLOCH, T_LUNGA, PEZZO, OGNI, OGNI_D, ESAME, FINESTRA, EPS_LUNGA, CORSE, TOLL_NORMA, LP.SB.MAX_NEWTON, LP.SB.TOLL_RES))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (q1) il residuo dipende dalla scelta e una scelta fa convergere Newton; (q2) la rotazione dentro la coppia e' libera: col vincolo converge o no;"
          " (q3) il cuore di B a Gamma RESTA mentre quello di A a K si svuota; (q4) il cuore di B si svuota: quale uscita; (q5) altro")
    print("=" * 130)
    gr = LP.leggi(os.path.join(DIR_JSON, "griglia.json"))
    print("### (1) LA SCELTA DENTRO LA COPPIA (griglia.json)")
    for nome, x in gr.items():
        rr = [p["residuo"] for p in x["griglia"]]
        print("  %s (eps %g): q1 sigma_z %+.5f elicita' %+.5f; q2 sigma_z %+.5f elicita' %+.5f; il residuo %.4e .. %.4e (s0 %.2e): %s; il minimo theta %.4f phi %.4f (%.4e)"
              % (nome, x["eps"], x["ritratto"]["q1"]["sigma_z"], x["ritratto"]["q1"]["elicita"], x["ritratto"]["q2"]["sigma_z"], x["ritratto"]["q2"]["elicita"], min(rr), max(rr), x["s0"],
                 "DIPENDE" if x["dipende"] else "NON DIPENDE (direzione libera)", x["minimo"]["theta"], x["minimo"]["phi"], x["minimo"]["residuo"]))
    print("-" * 130)
    print("### (2) NEWTON DALLA SCELTA MIGLIORE")
    stati = {}
    for nome in MB.CASI:
        fj = os.path.join(DIR_JSON, "cerca_%s.json" % nome)
        if not os.path.exists(fj):
            print("  %s: nessuna ricerca%s" % (nome, "" if gr[nome]["dipende"] else " (la rotazione e' libera: non si insiste)"))
            continue
        cj = LP.leggi(fj)
        with np.load(os.path.join(DIR_NPZ, "fermo_%s.npz" % nome)) as fe:
            ok = SFM.sha(fe["psi_h"]) == cj["sha"]
        esito("DEVE PASSARE: %s, lo stato sul disco = la ricerca (sha1)" % nome, ok, cj["sha"][:8])
        m = cj["misure"]
        print("  %s: %s (residuo %.3e in %d passi), mu - E0 %+.5f; w %.3f, cuore %.5f; la storia %s"
              % (nome, "FERMO" if cj["convergito"] else "NON FERMO", cj["residuo_finale"], len(cj["storia"]) - 1, cj["mu_meno_E0"], m["w"], m["f_win"], " ".join("%.1e" % p["residuo"] for p in cj["storia"])))
        stati[nome] = cj
    print("-" * 130)
    print("### (3) LE CORSE LUNGHE (eps %g, %d tick; le finestre di %g)" % (EPS_LUNGA, T_LUNGA, FINESTRA))
    fw = {}
    for chi in CORSE:
        f = finestre(chi)
        if f is None:
            print("  %s: nessuna corsa" % chi)
            continue
        esito("DEVE PASSARE: %s, M entro %g relativo nella corsa" % (chi, TOLL_NORMA), f["dM"] <= TOLL_NORMA, "%.1e" % f["dM"])
        print("  --- %s: la partenza %s; %d pezzi, tick %d%s" % (chi, f["pezzi"][0]["partenza"], len(f["pezzi"]), f["fine"], "" if f["fine"] >= T_LUNGA else " (NON FINITA)"))
        for w in f["finestre"]:
            d = w["D"]
            print("    tau [%5.0f, %5.0f]: cuore %.5f -> %.5f (pendenza %+.3e; fra %.5f e %.5f); w/w_in %.5f -> %.5f; alone %.5f -> %.5f; picco medio %.2f | D %s"
                  % (w["a"], w["b"], w["cuore"][0], w["cuore"][1], w["pendenza"], w["oscilla"][0], w["oscilla"][1], w["w"][0], w["w"][1], w["alone"][0], w["alone"][1], w["picco"],
                     ("%.3e (%s)" % (d["nD"], " ".join("%s %.3f" % kv for kv in d["bande"].items()))) if d else "--"))
        for x in f["pezzi"]:
            print("    le rotazioni a fine pezzo %05d: %s" % (x["t0"], " ".join("%s %+.4f (E %+.4f)" % (k, v["media"], x["esame"]["E"][k]) for k, v in x["esame"]["rot"].items())))
        fw[chi] = f
    rif = [LP.leggi(os.path.join(SFM.PUNTI, n)) for n in sorted(os.listdir(SFM.PUNTI)) if n.startswith("corsa_L81_") and n.endswith(".jsonl")]
    rp = [(p["t"] * SFM.S, p["f_win"]) for rr in rif for p in rr["punti"]]
    if rp:
        print("  il contesto (26300537, s %g, eps 0, dallo stato fermo di A a K): il cuore %.5f a tau %.0f, %.5f a tau %.0f" % (SFM.S, rp[0][1], rp[0][0], rp[-1][1], rp[-1][0]))
    print("-" * 130)
    print("### LE LETTURE (i numeri accanto: \"resta\" e \"si svuota\" non hanno soglia)")
    for nome, x in gr.items():
        cj = stati.get(nome)
        if x["dipende"] and cj is not None:
            print("  %s: il residuo DIPENDE dalla scelta; Newton dalla migliore: %s -> %s" % (nome, "FERMO" if cj["convergito"] else "NON FERMO (%.3e)" % cj["residuo_finale"], "(q1)" if cj["convergito"] else "(q1) no: la scelta non basta"))
        elif not x["dipende"]:
            print("  %s: la rotazione dentro la coppia e' LIBERA: (q2), senza vincolo (non si insiste)" % nome)
        else:
            print("  %s: dipende, nessuna ricerca" % nome)
    if "B" in fw and "AK" in fw:
        b, a = fw["B"], fw["AK"]
        print("  la corsa: B il cuore %.5f -> %.5f (w/w_in %.4f a fine); AK %.5f -> %.5f (w/w_in %.4f); le pendenze per finestra B %s | AK %s"
              % (b["cuore0"], b["cuore1"], b["w_fine"], a["cuore0"], a["cuore1"], a["w_fine"], " ".join("%+.1e" % w["pendenza"] for w in b["finestre"]), " ".join("%+.1e" % w["pendenza"] for w in a["finestre"])))
        print("  ### (q3) se B resta e AK si svuota; (q4) se B si svuota (le bande di D qui sopra); i numeri sono questi: la parola nella relazione")
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--griglia" in argv:
        griglia()
    elif "--cerca" in argv:
        cerca(argv[argv.index("--cerca") + 1])
    elif "--lunga" in argv:
        lunga(argv[argv.index("--lunga") + 1])
    elif "--referto" in argv:
        referto()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
