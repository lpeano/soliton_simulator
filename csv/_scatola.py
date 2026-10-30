# -*- coding: utf-8 -*-
r"""**LA REGOLA CON L'USCITA MISTA E LA PROVA DELLA SCATOLA** *(UNA PROVA, NON UNA CURA; il mandato di Luca delle `22:11` del `2026-10-30`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-30_scatola.md`)*:
### **(1) per `r 1`, `r 1.5247`, `X1`, (R): le uscite (n2) e (n2-misto) aperte o chiuse sullo spettro libero, senza corse;**
### **(3) (R) `N 1e6` sul toro `L 120`: lo stato fermo dallo stato di `L 81` messo al centro; la corsa a pezzi fino a `|D|/|psi0| >= 1e-2`; il tasso contro `L 81`.**

    python csv/_scatola.py --uscite > doc/referti_l2/scatola/uscite.txt
    python csv/_scatola.py --cerca > doc/referti_l2/scatola/cerca_L120.txt
    python csv/_scatola.py --pezzo                     # un pezzo; si ripete finche' dice "finita"
    python csv/_scatola.py --referto > doc/referti_l2/scatola.txt
"""
import contextlib
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

import _livelli_piatti as LP                                   # noqa: E402

NOME = "R_1e6"
L_GRANDE = 120
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "scatola")
F_STATO = os.path.join(LP.DIR_NPZ, "fermo_%s_L%d.npz" % (NOME, L_GRANDE))
F_RIPRESA = os.path.join(LP.DIR_NPZ, "scatola_%s_L%d.npz" % (NOME, L_GRANDE))
SOGLIA = 1e-2                  # ### la soglia della vita (Luca 22:11, decisa)
TAU_MAX = 3000.0               # ### «al piu' 3000 unita' di tempo» (Luca 22:11)
ESAME = 40                     # ### i D dei 40 tick prima della fine di un pezzo, in memoria: l'esame di 795d2c81
SIGMA = 3.0                    # ### il 3 sigma di doc/PATTERN_DI_PROVA.md
# ### (1) i casi gia' misurati: (nome, la FAMIGLIA dei pesi dello stato, r, g, da dove, il tasso misurato, la sua uscita)
# ### le famiglie (Luca 00:21): "lp" = _livelli_piatti (a_n = pi, b_a = r pi, il legame g); "sb" = _strada_b_r (a = pi/sqrt(1 - r + r^2), b = r a, mu0 = pi/2, g 1)
CASI = (("r 1", "lp", 1.0, 1.0, "dfb5ab7e (S1_s0.150)", 0.151, "coppia di piatte"),
        ("r 1.5247", "sb", 1.5247, 1.0, "_strada_b_r cerca_r1.52", 0.033, "coppia di piatte"),
        ("X1", "lp", 1.0, 0.5, "cerca_X1.json", 0.061, "coppia di piatte"),
        ("(R)", "lp", 0.6, 0.5, "cerca_R_1e6.json", 0.0079, "mista (P0 + A)"))
PIATTE = ("P0", "Ppi")
DISPERSIVE = ("A", "B")
TOLL_RES_REL = 1e-6            # ### il residuo ricalcolato coi pesi della riga contro quello registrato, relativo


def stato_di(nome):
    """### **`(psi, mu, il residuo registrato dalla sua ricerca)`.**"""
    import _modo_al_variare_di_s as MS
    import _strada_b_r as SB
    if nome == "r 1":
        psi, mu, cj, ok = MS.carica("S1_s0.150")
    elif nome == "r 1.5247":
        psi, mu, cj, ok = SB.carica(1.5247)
    else:
        psi, mu, cj = LP.stato("X1" if nome == "X1" else NOME)
        ok = True
    assert ok, nome
    return psi, mu, cj["residuo_finale"]


@contextlib.contextmanager
def famiglia(fam, r, g):
    """### **La scena e i pesi della famiglia:** `lp` = `LP.scena` + `LP.configurazione(r, g)`; `sb` = `SB.scena` + `SB.pesi(r)`."""
    import _strada_b_r as SB
    if fam == "lp":
        with LP.scena(LP.N_RIF) as (_rec, z, phi0, _p), LP.configurazione(r, g):
            yield z, phi0
    else:
        assert g == 1.0, "la famiglia sb ha il legame di S1 com'e'"
        with SB.scena() as (_rec, z, phi0, _p, _forma, _s), SB.pesi(r):
            yield z, phi0


def residuo(z, phi0, psi, mu):
    import _modo_al_variare_di_s as MS
    return float(np.linalg.norm(MS.tick(z, phi0, psi, LP.FORMA) - np.exp(-1j * mu * LP.S) * psi) / np.linalg.norm(psi))


def spettro(z, phi0):
    """### **Lo spettro libero** *(`DV.matrice` a `AMP`, dentro la famiglia)*: ### **per gruppo l'intervallo `[min, max]` di `E = fase/s`** *(`ALPHA0` di `S1` = `0`)*."""
    import _dove_va_la_materia as DV
    ph, _Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
    E = ph / LP.S
    return {gr: (float(E[..., list(idx)].min()), float(E[..., list(idx)].max())) for gr, idx in DV.GRUPPI}


def sovrapposti(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


# ====================================================================== (1) LE USCITE
def uscite():
    print("### (1) LE USCITE SULLO SPETTRO LIBERO (la regola corretta di Luca 22:11): (n2-misto) [2 mu - F - g, 2 mu - F] contro A, B; (n2) 2 mu - F_i - F_j in [0, 2 g]")
    print("    (Luca 00:21: OGNI riga coi pesi della famiglia dello stato che legge; DEVE: il residuo del tick dello stato coi pesi della riga = quello della sua ricerca, entro %g relativo)" % TOLL_RES_REL)
    for nome, fam, r, g, da, tasso, tipo in CASI:
        psi, mu, res_reg = stato_di(nome)
        with famiglia(fam, r, g) as (z, phi0):
            res = residuo(z, phi0, psi, mu)
            sp = spettro(z, phi0)
        LP.esito("DEVE PASSARE: %s, i pesi della riga (famiglia %s) sono quelli dello stato: il residuo ricalcolato = il registrato" % (nome, fam), abs(res / res_reg - 1.0) < TOLL_RES_REL, "%.6e contro %.6e" % (res, res_reg))
        if nome == "r 1.5247":
            with famiglia("lp", r, g) as (z, phi0):
                res_sb = residuo(z, phi0, psi, mu)
            LP.esito("DEVE FALLIRE: r 1.5247 coi pesi della famiglia SBAGLIATA (lp: a_n = pi, b_a = r pi), l'errore di c6ad04ac", not (abs(res_sb / res_reg - 1.0) < TOLL_RES_REL), "%.3e contro %.3e" % (res_sb, res_reg))
        F = {p: 0.5 * (sp[p][0] + sp[p][1]) for p in PIATTE}
        print("  --- %s: famiglia %s, r %.4f g %.2f mu %+.5f (%s); il tasso misurato %.4f (%s)" % (nome, fam, r, g, mu, da, tasso, tipo))
        print("      le bande libere: %s; le piatte larghe %s" % ("  ".join("%s [%+.5f, %+.5f]" % (k, v[0], v[1]) for k, v in sp.items()), "  ".join("%s %.1e" % (p, sp[p][1] - sp[p][0]) for p in PIATTE)))
        for p in PIATTE:
            iv = (2.0 * mu - F[p] - g, 2.0 * mu - F[p])
            ap = [b for b in DISPERSIVE if sovrapposti(iv, sp[b])]
            print("      (n2-misto) %-3s F %+.5f: il partner in [%+.5f, %+.5f] -> %s" % (p, F[p], iv[0], iv[1], ("APERTA con " + ", ".join(ap)) if ap else "chiusa"))
            if nome == "(R)" and p == "P0":
                LP.esito("DEVE PASSARE: (R) P0, l'intervallo del guardiano [-1.609, -1.109] entro 1e-3", abs(iv[0] + 1.609) < 1e-3 and abs(iv[1] + 1.109) < 1e-3, "[%+.4f, %+.4f]" % iv)
                LP.esito("DEVE PASSARE: (R) P0, la mista con A APERTA (il partner misurato a -1.607 dentro A)", "A" in ap, "")
        for i, p in enumerate(PIATTE):
            for q in PIATTE[i:]:
                x = 2.0 * mu - F[p] - F[q]
                dentro = 0.0 <= x <= 2.0 * g
                print("      (n2) %-3s + %-3s: 2 mu - F_i - F_j %+.5f contro [0, 2 g = %.2f] -> %s" % (p, q, x, 2.0 * g, ("APERTA, a alpha %.4f" % (x / 2.0)) if dentro else "chiusa, %.4f fuori" % (x - 2.0 * g if x > 2.0 * g else -x)))
            x = mu - F[p]
            print("      (n1) %-3s: mu - F %+.5f contro [0, g = %.2f] -> %s" % (p, x, g, "APERTA" if 0.0 <= x <= g else "chiusa"))


# ====================================================================== (3) LO STATO SUL TORO GRANDE
def baricentro_indici(psi, L):
    """### **La media circolare degli indici `(i, j)`, pesata con `|psi|^2` per nodo.**"""
    p = np.sum(np.abs(psi.reshape(L, L, 12)) ** 2, axis=2)
    c = []
    for asse in (0, 1):
        th = 2.0 * math.pi * np.arange(L) / L
        w = p.sum(axis=1 - asse)
        c.append((math.atan2(float((w * np.sin(th)).sum()), float((w * np.cos(th)).sum())) % (2.0 * math.pi)) * L / (2.0 * math.pi))
    return c


def metti(psi81, L81, L, c_dest):
    c = baricentro_indici(psi81, L81)
    a = np.roll(psi81.reshape(L81, L81, 12), (L81 // 2 - int(round(c[0])), L81 // 2 - int(round(c[1]))), axis=(0, 1))
    g = np.zeros((L, L, 12), dtype=complex)
    o = (int(round(c_dest[0])) - L81 // 2, int(round(c_dest[1])) - L81 // 2)
    ii = (np.arange(L81) + o[0]) % L
    jj = (np.arange(L81) + o[1]) % L
    g[np.ix_(ii, jj)] = a
    return g, c, o


def cerca():
    import _stato_fermo as SFM
    os.makedirs(DIR_JSON, exist_ok=True)
    fj = os.path.join(DIR_JSON, "cerca_L%d.json" % L_GRANDE)
    assert not os.path.exists(fj), fj
    r, g, N = LP.CONFIG[NOME]
    psi81, mu81, cj81 = LP.stato(NOME)
    with LP.scena(N, L_GRANDE) as (_rec, z, _phi0, p_ini):
        shape = p_ini.shape
        c_dest = baricentro_indici(p_ini, L_GRANDE)
        pos = z["pos"]
    with LP.scena(N, LP.L_SCENA) as (_rec, z81, _phi0, _p):
        pos81 = z81["pos"]
    g120, c81, o = metti(psi81, LP.L_SCENA, L_GRANDE, c_dest)
    n120, n81 = float(np.sum(np.abs(g120) ** 2)), float(np.sum(np.abs(psi81) ** 2))
    LP.esito("DEVE PASSARE: il blocco messo sul toro %d conserva la norma (entro l'ordine della somma, 1e-14 relativo)" % L_GRANDE, abs(n120 / n81 - 1.0) < 1e-14, "%.17g / %.17g" % (n120, n81))
    # ### i reticoli coincidono: la differenza di posizione fra due nodi vicini e' la stessa sui due tori
    d81 = pos81[1] - pos81[0]
    d120 = pos[1] - pos[0]
    dL81 = pos81[LP.L_SCENA] - pos81[0]
    dL120 = pos[L_GRANDE] - pos[0]
    LP.esito("DEVE PASSARE: i passi del reticolo coincidono sui due tori (il nodo +1 e il nodo +L)", bool(np.allclose(d81, d120, atol=1e-12) and np.allclose(dL81, dL120, atol=1e-12)), "%s %s | %s %s" % (d81, d120, dL81, dL120))
    print("  il baricentro (indici) di L 81 %s, della scena L %d %s; il blocco a partire da %s" % (["%.2f" % x for x in c81], L_GRANDE, ["%.2f" % x for x in c_dest], o))
    p0 = g120.reshape(shape)
    p0 = p0 * math.sqrt(N / float(np.sum(np.abs(p0) ** 2)))
    psi, mu, rf, storia, sec = LP.newton(r, g, N, p0, "%s-L%d" % (NOME, L_GRANDE), LP.SB.MAX_NEWTON, L_GRANDE)
    os.makedirs(LP.DIR_NPZ, exist_ok=True)
    tmp = F_STATO.replace(".npz", "_tmp.npz")
    np.savez(tmp, psi_h=psi, mu=mu)
    os.replace(tmp, F_STATO)
    riga = {"nome": NOME, "L": L_GRANDE, "r": r, "g": g, "N": N, "partenza": "%s L 81 (sha1 %s), il blocco centrato" % (NOME, cj81["sha"][:8]), "mu_L81": mu81,
            "mu": mu, "residuo_finale": rf, "convergito": rf < LP.SB.TOLL_RES, "sha": SFM.sha(psi), "storia": storia, "secondi": sec}
    LP.scrivi_nuovo(fj, riga)
    print("  %s L %d: residuo finale %.3e, mu %+.9f (L 81: %+.9f); %s" % (NOME, L_GRANDE, rf, mu, mu81, "CONVERGE" if rf < LP.SB.TOLL_RES else "NON CONVERGE: lo stato migliore, dichiarato"))


def stato_grande():
    import _stato_fermo as SFM
    cj = LP.leggi(os.path.join(DIR_JSON, "cerca_L%d.json" % L_GRANDE))
    with np.load(F_STATO) as fe:
        psi, mu = fe["psi_h"].copy(), float(fe["mu"])
    assert SFM.sha(psi) == cj["sha"], "lo stato di L %d sul disco NON e' quello della ricerca" % L_GRANDE
    return psi, mu, cj


# ====================================================================== (3) LA CORSA A PEZZI
def nome_pezzo(t0):
    return os.path.join(DIR_JSON, "corsa_L%d_%05d.jsonl" % (L_GRANDE, t0))


def pezzo():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _modo_instabile as MI
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    r, g, N = LP.CONFIG[NOME]
    psi0, mu, _cj = stato_grande()
    S = LP.S
    with LP.scena(N, L_GRANDE) as (rec, z, phi0, _p), LP.configurazione(r, g):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = LP.ML.Bande(Z, z["L"])
        E = ph / S + MS.ALPHA0[LP.FORMA]
        n0 = float(np.linalg.norm(psi0))
        t0 = 0
        punti, dd = [], []
        if os.path.exists(F_RIPRESA):
            with np.load(F_RIPRESA) as dati:
                t0 = int(dati["t"])
                z["st"]["psi_h"][...] = dati["psi_h"]
            prec = LP.leggi(nome_pezzo(t0 - LP.PEZZO))
            assert prec["sha_fine"] == SFM.sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
            if prec["D"][-1]["nD"] >= SOGLIA or t0 * S >= TAU_MAX:
                print("  la corsa L %d: finita (|D|/|psi0| %.3e a tau %.1f)" % (L_GRANDE, prec["D"][-1]["nD"], t0 * S))
                return
        else:
            z["st"]["psi_h"][...] = psi0
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                p = CL.punto(z, 0, w_in, w0)
            p["tau"] = 0.0
            punti.append(p)
        t1 = t0 + LP.PEZZO
        Ds = {}
        s0 = time.time()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(t0 + 1, t1 + 1):
                CL.avanza(z, phi0, 1)
                if t % LP.OGNI == 0:
                    p = CL.punto(z, t, w_in, w0)
                    p["tau"] = t * S
                    punti.append(p)
                if t % LP.OGNI_LUNGA_D == 0 or t > t1 - ESAME:
                    D = np.exp(1j * mu * S * t) * z["st"]["psi_h"] - psi0
                    if t % LP.OGNI_LUNGA_D == 0:
                        c = bande.coeff(D)
                        pk = np.abs(c) ** 2
                        tot = float(pk.sum())
                        dd.append({"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}})
                    if t > t1 - ESAME:
                        Ds[t] = D
        # ### PRIMA lo sha e la ripresa: MI.armoniche, qui sotto, rimette psi0 in z (il suo uso per gli anelli)
        sha_fine = SFM.sha(z["st"]["psi_h"])
        tmp = F_RIPRESA.replace(".npz", "_tmp.npz")
        np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
        # ### l'esame di 795d2c81 sui D dei 40 tick prima della fine (solo numeri su disco)
        ts = sorted(Ds)
        rot = {gr: [bande.rotazione(Ds[a], Ds[b], (gr,), S) for a, b in zip(ts, ts[1:])] for gr in ("P0", "A", "Ppi", "B")}
        vista = MS.Vista(z, psi0)
        _w, kk = MI.armoniche(vista, np.ones(vista.n))
        r_ = np.arange(int(kk.max()) + 1)

        def raggio(x):
            pp = np.bincount(kk, weights=np.sum(np.abs(x.reshape(-1, 12)) ** 2, axis=1), minlength=len(r_))
            return float((r_ * pp).sum() / pp.sum())

        def reale(d, nomi):
            return np.fft.ifft2(bande.parte(bande.coeff(d), nomi), axes=(0, 1)).reshape(-1, 12)
        dfin = Ds[ts[-1]]
        esame = {"rot": {gr: {"media": float(np.mean(v)), "dev": float(np.std(v))} for gr, v in rot.items()},
                 "somma_P0_A": {"media": float(np.mean(np.array(rot["P0"]) + np.array(rot["A"]))), "dev": float(np.std(np.array(rot["P0"]) + np.array(rot["A"])))},
                 "E": {gr: float(np.mean(rot[gr])) + mu for gr in ("P0", "A")},
                 "bande_libere": {gr: [float(E[..., list(idx)].min()), float(E[..., list(idx)].max())] for gr, idx in bande.gruppi.items()},
                 "raggio": {"A": raggio(reale(dfin, ("A",))), "P0": raggio(reale(dfin, ("P0",))), "psi0": raggio(psi0), "uniforme": float((r_ * np.bincount(kk, minlength=len(r_))).sum() / len(kk))}}
        riga = {"nome": NOME, "L": L_GRANDE, "r": r, "g": g, "N": N, "t0": t0, "t1": t1, "s": S, "mu": mu, "w0": w0, "w_in": w_in, "punti": punti, "D": dd, "esame": esame,
                "sha_fine": sha_fine, "secondi": time.time() - s0}
        LP.scrivi_nuovo(nome_pezzo(t0), riga)
        os.replace(tmp, F_RIPRESA)
    print("  la corsa L %d: tick %d -> %d, w/w_in %.5f, cuore %.5f, |D|/|psi0| %.3e (A %.3f P0 %.3f); rot P0 %+.4f A %+.4f (%.0f s)"
          % (L_GRANDE, t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], dd[-1]["nD"], dd[-1]["bande"]["A"], dd[-1]["bande"]["P0"], esame["rot"]["P0"]["media"], esame["rot"]["A"]["media"], riga["secondi"]))


def ripresa_al_bit(pz):
    """### **I pezzi ripartono AL BIT** *(Luca 00:21)*: ### **la corsa rifatta dallo stato fermo `L 120` fino all'ultimo `t1`, lo `sha` a ogni fine pezzo = `sha_fine` committato; lo stato di ripresa sul disco = l'ultimo.**"""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    r, g, N = LP.CONFIG[NOME]
    psi0, _mu, _cj = stato_grande()
    fine = {x["t1"]: x["sha_fine"] for x in pz}
    s0 = time.time()
    with LP.scena(N, L_GRANDE) as (_rec, z, phi0, _p), LP.configurazione(r, g):
        z["st"]["psi_h"][...] = psi0
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(1, max(fine) + 1):
                CL.avanza(z, phi0, 1)
                if t in fine:
                    LP.esito("DEVE PASSARE: la corsa su L %d rifatta: lo stato al tick %d = sha_fine del pezzo committato (AL BIT)" % (L_GRANDE, t), SFM.sha(z["st"]["psi_h"]) == fine[t], fine[t][:8])
    with np.load(F_RIPRESA) as dati:
        LP.esito("DEVE PASSARE: lo stato di ripresa sul disco (t %d) = l'ultimo sha_fine" % int(dati["t"]), int(dati["t"]) == max(fine) and SFM.sha(dati["psi_h"]) == fine[max(fine)], "")
    print("  la corsa rifatta: %d tick in %.0f s" % (max(fine), time.time() - s0))


# ====================================================================== IL REFERTO
def tasso(tau, nD, attesa):
    """### **La finestra di `5f06dbfb`** *(da `FATTORE_DEROGA` volte la deriva attesa a `SOGLIA`)*; ### **l'errore: il piu' grande fra la `sigma` del fit e meta' della differenza fra le due meta'.**"""
    basso = LP.FATTORE_DEROGA * attesa * np.maximum(tau, LP.S)
    fin = [i for i in range(len(tau)) if basso[i] < nD[i] < SOGLIA]
    if len(fin) < 6:
        return None
    i0, i1 = fin[0], fin[-1]
    x, y = tau[i0:i1 + 1], np.log(nD[i0:i1 + 1])
    (g, a), cov = np.polyfit(x, y, 1, cov=True)
    h = len(x) // 2
    g1 = np.polyfit(x[:h], y[:h], 1)[0]
    g2 = np.polyfit(x[h:], y[h:], 1)[0]
    err = max(float(math.sqrt(cov[0, 0])), 0.5 * abs(g2 - g1))
    return {"tau": (float(x[0]), float(x[-1])), "campioni": len(x), "gamma": float(g), "a": float(a), "sigma_fit": float(math.sqrt(cov[0, 0])), "meta": (float(g1), float(g2)), "err": err}


def serie(righe):
    dd = [d for x in righe for d in x["D"]]
    s = righe[0]["s"]
    return np.array([d["t"] for d in dd], dtype=float) * s, np.array([d["nD"] for d in dd]), dd


def referto():
    print("=" * 130)
    print("LA PROVA DELLA SCATOLA (Luca 22:11): R_1e6 (r 0.6, g 0.5, s %g, N 1e6) su L %d contro L 81; la soglia della vita |D|/|psi0| >= %g (decisa)" % (LP.S, L_GRANDE, SOGLIA))
    print("  la configurazione: L_GRANDE %d SOGLIA %g TAU_MAX %g ESAME %d SIGMA %g; da _livelli_piatti: PEZZO %d OGNI %d OGNI_LUNGA_D %d FATTORE_DEROGA %g; da _strada_b_r: MAX_NEWTON %d TOLL_RES %g"
          % (L_GRANDE, SOGLIA, TAU_MAX, ESAME, SIGMA, LP.PEZZO, LP.OGNI, LP.OGNI_LUNGA_D, LP.FATTORE_DEROGA, LP.SB.MAX_NEWTON, LP.SB.TOLL_RES))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (s1) il tasso uguale a L 81 entro gli errori: il decadimento misto e' fisico; (s2) il tasso cambia con L: la radiazione che torna conta; (s3) altro")
    print("=" * 130)
    cj = LP.leggi(os.path.join(DIR_JSON, "cerca_L%d.json" % L_GRANDE))
    stato_grande()
    c81_ = LP.leggi(os.path.join(LP.DIR_JSON, "cerca_%s.json" % NOME))
    LP.esito("DEVE PASSARE: lo stato su L %d ha il residuo di L 81 (dai .json committati, %g relativo)" % (L_GRANDE, TOLL_RES_REL), abs(cj["residuo_finale"] / c81_["residuo_finale"] - 1.0) < TOLL_RES_REL, "%.6e contro %.6e" % (cj["residuo_finale"], c81_["residuo_finale"]))
    LP.esito("DEVE PASSARE: lo stato su L %d ha il mu di L 81 (entro 1e-12)" % L_GRANDE, abs(cj["mu"] - c81_["mu"]) < 1e-12, "%+.12f contro %+.12f" % (cj["mu"], c81_["mu"]))
    print("### LO STATO SU L %d: %s (residuo %.3e), mu %+.9f (L 81 %+.9f); la storia %s" % (L_GRANDE, "FERMO" if cj["convergito"] else "NON FERMO", cj["residuo_finale"], cj["mu"], cj["mu_L81"],
                                                                                      " ".join("%.1e" % p["residuo"] for p in cj["storia"])))
    c81 = LP.leggi(os.path.join(LP.DIR_JSON, "cerca_%s.json" % NOME))
    pz = sorted([LP.leggi(os.path.join(DIR_JSON, n)) for n in os.listdir(DIR_JSON) if n.startswith("corsa_L%d_" % L_GRANDE)], key=lambda x: x["t0"])
    for x, y in zip(pz, pz[1:]):
        assert x["t1"] == y["t0"], ("un buco", x["t1"], y["t0"])
    p81 = sorted([LP.leggi(os.path.join(LP.DIR_JSON, n)) for n in os.listdir(LP.DIR_JSON) if n.startswith("lunga_%s_" % NOME) and n.endswith(".jsonl")], key=lambda x: x["t0"])
    print("### LA CORSA SU L %d: %d pezzi, tick %d -> %d" % (L_GRANDE, len(pz), pz[0]["t0"], pz[-1]["t1"]))
    for x in pz:
        e = x["esame"]
        print("  pezzo %05d: |D| a fine %.3e (A %.3f P0 %.3f Ppi %.3f); cuore %.5f; rot P0 %+.4f A %+.4f somma %+.4f (dev %.4f); E_A %+.4f, E_P0 %+.4f; raggi A %.2f P0 %.2f psi0 %.2f uniforme %.2f"
              % (x["t0"], x["D"][-1]["nD"], x["D"][-1]["bande"]["A"], x["D"][-1]["bande"]["P0"], x["D"][-1]["bande"]["Ppi"], x["punti"][-1]["f_win"], e["rot"]["P0"]["media"], e["rot"]["A"]["media"],
                 e["somma_P0_A"]["media"], e["somma_P0_A"]["dev"], e["E"]["A"], e["E"]["P0"], e["raggio"]["A"], e["raggio"]["P0"], e["raggio"]["psi0"], e["raggio"]["uniforme"]))
    ripresa_al_bit(pz)
    print("  le bande libere su L %d: %s" % (L_GRANDE, "  ".join("%s [%+.4f, %+.4f]" % (k, v[0], v[1]) for k, v in pz[-1]["esame"]["bande_libere"].items())))
    tg = {}
    for chi, righe, cc in (("L %d" % L_GRANDE, pz, cj), ("L 81", p81, c81)):
        tau, nD, dd = serie(righe)
        sopra = np.nonzero(nD >= SOGLIA)[0]
        tw = tasso(tau, nD, cc["residuo_finale"] / LP.S)
        fn = LP.forma_pendenze(tau, nD)
        tg[chi] = tw
        print("### %s: la vita (il primo tau con |D|/|psi0| >= %g) %s; la forma col criterio aggiunto %s" % (chi, SOGLIA, ("%.1f" % tau[sopra[0]]) if len(sopra) else "MAI (fino a %.0f)" % tau[-1], fn["forma"]))
        if tw is None:
            print("  la finestra: meno di 6 campioni")
            continue
        dentro = [d for d, x in zip(dd, tau) if tw["tau"][0] <= x <= tw["tau"][1]]
        print("  la finestra tau %.0f .. %.0f, %d campioni: gamma %.5f; sigma del fit %.5f, le due meta' %.5f e %.5f: l'errore %.5f; il seme efficace %.2e; dentro A %.3f P0 %.3f Ppi %.3f"
              % (tw["tau"][0], tw["tau"][1], tw["campioni"], tw["gamma"], tw["sigma_fit"], tw["meta"][0], tw["meta"][1], tw["err"], math.exp(tw["a"]),
                 float(np.mean([d["bande"]["A"] for d in dentro])), float(np.mean([d["bande"]["P0"] for d in dentro])), float(np.mean([d["bande"]["Ppi"] for d in dentro]))))
    print("### LA LETTURA, COL CRITERIO SCRITTO PRIMA")
    a, b = tg.get("L %d" % L_GRANDE), tg.get("L 81")
    if a is None or b is None:
        print("  LA LETTURA: (s3) -- una finestra manca")
    else:
        dg = a["gamma"] - b["gamma"]
        e = math.sqrt(a["err"] ** 2 + b["err"] ** 2)
        print("  gamma L %d %.5f +- %.5f; L 81 %.5f +- %.5f; la differenza %+.5f, %g sigma combinati = %.5f" % (L_GRANDE, a["gamma"], a["err"], b["gamma"], b["err"], dg, SIGMA, SIGMA * e))
        print("  LA LETTURA: %s" % ("(s1) il tasso uguale entro gli errori" if abs(dg) <= SIGMA * e else "(s2) il tasso cambia con L: %+.5f (%+.1f %%), %s" % (dg, 100.0 * dg / b["gamma"], "piu' lento sul toro grande" if dg < 0 else "piu' rapido sul toro grande")))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; fallite: %s" % (LP.OK[0], LP.OK[1], LP.FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        if argv == ["--uscite"]:
            uscite()
        elif argv == ["--cerca"]:
            cerca()
        elif argv == ["--pezzo"]:
            pezzo()
        elif argv == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    print("controlli: %d/%d; fallite: %s" % (LP.OK[0], LP.OK[1], LP.FALLITE))
    return 0 if LP.OK[0] == LP.OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
