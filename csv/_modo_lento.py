# -*- coding: utf-8 -*-
r"""**LA LEZIONE DELLE BANDE PIATTE E IL MODO LENTO A `r 1.5247`, CON LE CONSERVAZIONI NEL DECADIMENTO** *(UNA DIAGNOSI, NON UNA CURA; i mandati di Luca delle `09:09` e `09:16`
del `2026-10-30`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-30_lezione_e_modo_lento.md`)*:
### **i pesi, la scena e gli stati da `csv/_strada_b_r.py` e `csv/_strada_b_lati.py`** *(invariati)*; ### **`r 1` da `csv/_modo_instabile.Mappa`** *(i `600` tick di `5f06dbfb`, rigenerati al bit)*.

    python csv/_modo_lento.py --modo       # r 1.5247: 4400 tick dallo stato fermo, D ogni 5 tick fra 3000 e 4400
    python csv/_modo_lento.py --uno        # r 1: i 600 tick di 5f06dbfb, D ogni 2 tick da 200
    python csv/_modo_lento.py --referto > doc/referti_l2/modo_lento.txt
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

import _strada_b_lati as SL                                    # noqa: E402
import _strada_b_r as SB                                       # noqa: E402

R_ALTO = 1.5247
R_LEZIONE = (1.0, 0.65, 0.69, R_ALTO)   # ### 0.69: la fettina tarata, etichettata
T_FINE = 4400                  # ### tempo 660 a s 0.15
OGNI_PUNTO = 10
OGNI_D = 5                     # ### 0.75 unita' di tempo: sotto Nyquist per una rotazione di ~1.8 (il task history)
T_D_DA = 3000                  # ### tempo 450
FATTORE_DEROGA = 10.0          # ### la finestra da 10 volte la deriva lineare della corsa breve
SATURAZIONE = 1e-2
ANELLI_M1 = (12, 13)           # ### (m1): l'anello maggiore di |D|^2 e' il 12 o il 13
T1_FINE = 600                  # ### r 1: i tick di 5f06dbfb
T1_DA = 200
OGNI1_D = 2                    # ### 0.6 unita' di tempo a s 0.3
FATTORE_RUMORE1 = 1e3          # ### r 1: la finestra di 5f06dbfb, da 1e3 volte il residuo
TOLL_CONS = 1e-10
DT_ALIAS = (3.0,)             # ### il passo di 5f06dbfb (10 tick a s 0.3) e di _modo_al_variare_di_s (PASSO_FIS 3 a ogni s): AGGIUNTO DOPO I NUMERI
R_PROFILO = 24
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "modo_lento")
DIR_NPZ = os.path.join(RADICE, "db", "modo_lento")
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


def q_s(psi):
    """### **`N_su - N_giu` e `M`** *(`sigma_z = diag(1, -1, ...)`: la seconda colonna di `psi_h` e' la componente giu')*."""
    p = np.abs(psi.reshape(-1, 12)) ** 2
    return float(p[:, 0::2].sum() - p[:, 1::2].sum()), float(p.sum())


# ====================================================================== LE PARTI DI BANDA
class Bande:
    """### **I proiettori di gruppo di banda** *(un gruppo intero di `DV.GRUPPI`: indipendente dalla base dentro il gruppo)* ### **e le valli di `DV.geometria`.**"""

    def __init__(self, Z, L):
        import _dove_va_la_materia as DV
        self.Z, self.L = Z, L
        self.valle, self.nomi, _dK, _dk = DV.geometria(L)
        self.gruppi = dict(DV.GRUPPI)

    def coeff(self, d):
        f = np.fft.fft2(d.reshape(self.L, self.L, 12), axes=(0, 1))
        return np.einsum("abji,abj->abi", self.Z.conj(), f)

    def parte(self, c, nomi):
        idx = [i for g in nomi for i in self.gruppi[g]]
        return np.einsum("abij,abj->abi", self.Z[..., idx], c[..., idx])

    def misura(self, d, nomi):
        """### **La parte nelle bande `nomi`:** norma^2 *(frazione di `|d|^2`)*, `q = <x, sigma_z x>/<x, x>`, i pesi per valle."""
        c = self.coeff(d)
        tot = float(np.sum(np.abs(c) ** 2))
        f = self.parte(c, nomi)
        p = np.abs(f) ** 2
        n2 = float(p.sum())
        q = float(p[..., 0::2].sum() - p[..., 1::2].sum()) / n2
        idx = [i for g in nomi for i in self.gruppi[g]]
        pk = np.sum(np.abs(c[..., idx]) ** 2, axis=-1)
        val = {nv: float(pk[self.valle == v].sum()) / n2 for v, nv in enumerate(self.nomi)}
        return {"frazione": n2 / tot, "q": q, "valli": val}

    def rotazione(self, d1, d2, nomi, dtau):
        """### **`-arg<x(t), x(t + dtau)>/dtau`:** l'energia della parte rispetto a `mu`, per unita' di tempo."""
        a = self.parte(self.coeff(d1), nomi)
        b = self.parte(self.coeff(d2), nomi)
        v = complex(np.vdot(a, b))
        return -math.atan2(v.imag, v.real) / dtau


MAPPE = {"identita'": {"Gamma": "Gamma", "K": "K", "K'": "K'"},
         "+K": {"Gamma": "K", "K": "K'", "K'": "Gamma"},
         "-K": {"Gamma": "K'", "K": "Gamma", "K'": "K"},
         "riflessione per K (2K - k)": {"K": "K", "K'": "Gamma", "Gamma": "K'"},
         "riflessione per K' (2K' - k)": {"K'": "K'", "K": "Gamma", "Gamma": "K"}}


def confronto_valli(vP0, vPpi):
    """### **Le valli di `D_Ppi` contro quelle di `D_P0` portate da ciascuna mappa:** la somma delle differenze assolute."""
    out = {}
    for nm, m in MAPPE.items():
        pred = {k: 0.0 for k in vP0}
        for k, v in vP0.items():
            pred[m[k]] += v
        out[nm] = float(sum(abs(pred[k] - vPpi[k]) for k in vPpi))
    return out


# ====================================================================== L'ANALISI DEI D SALVATI
def analizza(ts, nD, tD, Ds, s, psi0, bande, vista, basso_di, etichetta):
    import _modo_instabile as MI
    tau = np.array(ts, dtype=float) * s
    nD = np.array(nD)
    basso = np.array([basso_di(x) for x in tau])
    fin = [i for i in range(len(ts)) if basso[i] < nD[i] < SATURAZIONE]
    out = {"finestra": None}
    print("  [%s] la finestra: da %s volte la deriva/il rumore a %g: %d campioni" % (etichetta, "la regola", SATURAZIONE, len(fin)))
    if len(fin) < 3:
        return out
    i0, i1 = fin[0], fin[-1]
    x, y = tau[i0:i1 + 1], np.log(nD[i0:i1 + 1])
    g, a = np.polyfit(x, y, 1)
    out["finestra"] = {"tau": [float(x[0]), float(x[-1])], "campioni": int(i1 - i0 + 1), "basso": [float(basso[i0]), float(basso[i1])],
                       "tasso": float(g), "scarto_max": float(np.abs(y - (a + g * x)).max())}
    salvati = [t for t in tD if ts[i0] <= t <= ts[i1]]
    out["salvati_in_finestra"] = len(salvati)
    if len(salvati) < 3:
        return out
    ts_ = np.array(salvati, dtype=float) * s
    nf = np.array([math.sqrt(bande.misura(Ds[t], ("P0", "Ppi"))["frazione"]) * float(np.linalg.norm(Ds[t])) for t in salvati]) / float(np.linalg.norm(psi0))
    gf, af = np.polyfit(ts_, np.log(nf), 1)
    out["tasso_piatte"] = {"tasso": float(gf), "scarto_max": float(np.abs(np.log(nf) - (af + gf * ts_)).max())}
    dr = Ds[salvati[-1]]
    pr = [float(np.real(np.vdot(dr, Ds[t]))) / (float(np.linalg.norm(dr)) * float(np.linalg.norm(Ds[t]))) for t in salvati]
    cambi = [i for i in range(1, len(pr)) if pr[i - 1] * pr[i] < 0.0]
    dt = salvati[1] - salvati[0]
    out["periodo"] = {"cambi": len(cambi), "tick": (2.0 * dt * float(np.mean(np.diff(cambi)))) if len(cambi) >= 2 else None}
    if out["periodo"]["tick"] is not None:
        out["periodo"]["tau"] = out["periodo"]["tick"] * s
    rot = {}
    for g_ in ("P0", "Ppi"):
        v = [bande.rotazione(Ds[a_], Ds[b_], (g_,), (b_ - a_) * s) for a_, b_ in zip(salvati, salvati[1:])]
        rot[g_] = {"media": float(np.mean(v)), "dev": float(np.std(v)), "min": float(np.min(v)), "max": float(np.max(v))}
    somma = [bande.rotazione(Ds[a_], Ds[b_], ("P0",), (b_ - a_) * s) + bande.rotazione(Ds[a_], Ds[b_], ("Ppi",), (b_ - a_) * s) for a_, b_ in zip(salvati, salvati[1:])]
    rot["somma"] = {"media": float(np.mean(somma)), "dev": float(np.std(somma))}
    out["rotazioni"] = rot
    ist = [salvati[0], salvati[len(salvati) // 2], salvati[-1]]
    out["istanti"] = {}
    _w, kk = MI.armoniche(vista, np.ones(vista.n))          # ### solo per gli anelli kk
    for t in ist:
        d = Ds[t]
        dd = d / float(np.linalg.norm(d))
        prd = np.bincount(kk, weights=np.sum(np.abs(dd.reshape(vista.n, 12)) ** 2, axis=1))
        prd = prd / prd.sum()
        dr_, df_ = MI.per_nodo(vista, dd)
        wd, _k = MI.armoniche(vista, dr_)
        wf, _k = MI.armoniche(vista, df_)
        parti = {g_: bande.misura(d, (g_,)) for g_ in ("Ppi", "A", "P0", "B")}
        piatte = bande.misura(d, ("P0", "Ppi"))
        out["istanti"][str(t)] = {
            "tau": t * s, "nD": float(np.linalg.norm(d)) / float(np.linalg.norm(psi0)),
            "bande": {g_: parti[g_]["frazione"] for g_ in parti},
            "anelli": [[int(k), float(prd[k])] for k in np.argsort(-prd)[:3]],
            "profilo": [float(x_) for x_ in prd[:R_PROFILO + 1]],
            "armoniche_drho": [float(x_) for x_ in wd], "armoniche_fase": [float(x_) for x_ in wf],
            "q": {"D": q_s(d)[0] / q_s(d)[1], "P0": parti["P0"]["q"], "Ppi": parti["Ppi"]["q"], "piatte": piatte["q"], "A": parti["A"]["q"]},
            "valli": {"P0": parti["P0"]["valli"], "Ppi": parti["Ppi"]["valli"]},
            "mappe": confronto_valli(parti["P0"]["valli"], parti["Ppi"]["valli"])}
    a0 = bande.misura(psi0, ("A",))
    out["psi0"] = {"q": q_s(psi0)[0] / q_s(psi0)[1], "q_A": a0["q"], "frazione_A": a0["frazione"], "valli_A": a0["valli"]}
    return out


# ====================================================================== (2) r 1.5247
def modo():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    fj = os.path.join(DIR_JSON, "modo_%s.json" % SB.nome_r(R_ALTO))
    assert not os.path.exists(fj), fj
    rif = {}
    w_in_rif = None
    for t0 in range(0, T_FINE, SL.PEZZO):
        x = leggi(os.path.join(SB.DIR_JSON, "lunga_%s_%05d.jsonl" % (SB.nome_r(R_ALTO), t0)))
        w_in_rif = x["w_in"] if w_in_rif is None else w_in_rif
        rif.update({p["t"]: p for p in x["punti"]})
    fr = leggi(os.path.join(SB.DIR_JSON, "forma_%s.json" % SB.nome_r(R_ALTO)))
    psi0, mu, cj = SL.stato(R_ALTO)
    print("  r %.4f: lo stato sha1 %s, residuo %.3e, mu %+.9f; la deriva della corsa breve %.3e + %.3e tau" % (R_ALTO, cj["sha"][:8], cj["residuo_finale"], mu, fr["c"], fr["v"]))
    with SB.scena() as (rec, z, phi0, _p, _forma, s), SB.pesi(R_ALTO):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))[1]
        z["st"]["psi_h"][...] = psi0
        n0 = float(np.linalg.norm(psi0))
        Q0, M0 = q_s(psi0)
        ts, nD, cons = [], [], 0.0
        Ds = {}
        alpunto, confr = True, 0
        s0 = time.time()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(1, T_FINE + 1):
                CL.avanza(z, phi0, 1)
                if t % OGNI_PUNTO == 0:
                    p = CL.punto(z, t, w_in, w0)
                    alpunto = alpunto and all(p[k] == rif[t][k] for k in ("w", "f_win", "f_3w0", "picco", "M"))
                    confr += 1
                if t % OGNI_D == 0:
                    psi = z["st"]["psi_h"]
                    Q, M = q_s(psi)
                    cons = max(cons, abs(Q - Q0) / M0, abs(M - M0) / M0)
                    D = np.exp(1j * mu * s * t) * psi - psi0
                    ts.append(t)
                    nD.append(float(np.linalg.norm(D)) / n0)
                    if t >= T_D_DA:
                        Ds[t] = D
        sec = time.time() - s0
        print("  r %.4f: %d tick in %.0f s; i punti al bit con lunga_%s: %s (%d confronti); w_in %s; Q_S e M entro %.1e"
              % (R_ALTO, T_FINE, sec, SB.nome_r(R_ALTO), alpunto, confr, "uguale" if w_in == w_in_rif else "DIVERSO", cons))
        os.makedirs(DIR_NPZ, exist_ok=True)
        tD = sorted(Ds)
        np.savez(os.path.join(DIR_NPZ, "D_%s.npz" % SB.nome_r(R_ALTO)), t=np.array(tD), D=np.array([Ds[t] for t in tD]))
        bande = Bande(Z, MS.L)
        vista = MS.Vista(z, psi0)
        an = analizza(ts, nD, tD, Ds, s, psi0, bande, vista, lambda x: FATTORE_DEROGA * (fr["c"] + fr["v"] * x), "r %.4f" % R_ALTO)
    riga = {"r": R_ALTO, "s": s, "mu": mu, "sha": cj["sha"], "residuo": cj["residuo_finale"], "alpunto": alpunto, "confronti": confr, "w_in_uguale": w_in == w_in_rif,
            "cons": cons, "secondi": sec, "t": ts, "nD": nD, "deriva": [fr["c"], fr["v"]], "analisi": an}
    scrivi_nuovo(fj, riga)
    stampa(riga)


# ====================================================================== (2bis) r 1: i D di 5f06dbfb
def uno():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _modo_instabile as MI
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    fj = os.path.join(DIR_JSON, "modo_r1_s0.3.json")
    assert not os.path.exists(fj), fj
    mp = MI.Mappa()
    S = mp.SFM.S
    assert mp.sha_ok, "lo stato fermo di r 1 sul disco NON e' quello della ricerca"
    r1 = float(np.linalg.norm(mp.G(mp.psi0, 1) - mp.psi0) / np.linalg.norm(mp.psi0))
    rifs = leggi(os.path.join(mp.SFM.PUNTI, "corsa_L%d_00000.jsonl" % MI.L))
    rif = {p["t"]: p for p in rifs["punti"]}
    w_in, w0 = rifs["w_in"], rifs["w0"]
    Z = DV.autovettori(DV.matrice(mp.z, mp.phi0, DV.AMP))[1]
    n0 = float(np.linalg.norm(mp.psi0))
    Q0, M0 = q_s(mp.psi0)
    psi = mp.psi0.copy()
    ts, nD, cons, Ds = [], [], 0.0, {}
    alpunto, confr = True, 0
    s0 = time.time()
    for t in range(1, T1_FINE + 1):
        psi = mp.SFM.tick(mp.z, mp.phi0, psi)
        if t % OGNI_PUNTO == 0:
            mp.z["st"]["psi_h"][...] = psi
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                pt = CL.punto(mp.z, t, w_in, w0)
            alpunto = alpunto and all(pt[k] == rif[t][k] for k in ("w", "f_win", "f_3w0", "picco", "M"))
            confr += 1
        if t % OGNI1_D == 0:
            Q, M = q_s(psi)
            cons = max(cons, abs(Q - Q0) / M0, abs(M - M0) / M0)
            D = np.exp(1j * mp.mu * S * t) * psi - mp.psi0
            ts.append(t)
            nD.append(float(np.linalg.norm(D)) / n0)
            if t >= T1_DA:
                Ds[t] = D
    sec = time.time() - s0
    print("  r 1 (s %g): %d tick in %.0f s; i punti al bit con 26300537: %s (%d confronti); Q_S e M entro %.1e; il residuo %.3e" % (S, T1_FINE, sec, alpunto, confr, cons, r1))
    os.makedirs(DIR_NPZ, exist_ok=True)
    tD = sorted(Ds)
    np.savez(os.path.join(DIR_NPZ, "D_r1_s0.3.npz"), t=np.array(tD), D=np.array([Ds[t] for t in tD]))
    bande = Bande(Z, MI.L)
    an = analizza(ts, nD, tD, Ds, S, mp.psi0, bande, mp, lambda x: FATTORE_RUMORE1 * r1, "r 1")
    riga = {"r": 1.0, "s": S, "mu": mp.mu, "residuo": r1, "alpunto": alpunto, "confronti": confr, "w_in_uguale": True, "cons": cons, "secondi": sec, "t": ts, "nD": nD, "analisi": an}
    scrivi_nuovo(fj, riga)
    stampa(riga)


# ====================================================================== LA STAMPA
def stampa(fr):
    an = fr["analisi"]
    s = fr["s"]
    et = "r %.4f" % fr["r"]
    print("  %s (s %g): mu %+.9f; il residuo %.3e; i punti al bit col riferimento: %s (%d confronti); Q_S e M entro %.1e" % (et, s, fr["mu"], fr["residuo"], fr["alpunto"], fr["confronti"], fr["cons"]))
    tau = np.array(fr["t"], dtype=float) * s
    nD = np.array(fr["nD"])
    passo = max(1, int(round(15.0 / (tau[1] - tau[0]))))
    print("    |D|/|psi0| ogni %.2f unita' di tempo (stampati ogni %d): %s" % (tau[1] - tau[0], passo, " ".join("%.0f:%.2e" % (tau[i], nD[i]) for i in range(0, len(tau), passo))))
    f = an["finestra"]
    if f is None:
        print("    LA FINESTRA: meno di 3 campioni: il tasso non si misura")
        return
    print("    LA FINESTRA: tempo %.2f .. %.2f, %d campioni (il basso da %.2e a %.2e, l'alto %g); IL TASSO %.5f per unita' di tempo (%.5f per tick); lo scarto massimo dalla retta %.3e"
          % (f["tau"][0], f["tau"][1], f["campioni"], f["basso"][0], f["basso"][1], SATURAZIONE, f["tasso"], f["tasso"] * s, f["scarto_max"]))
    if an.get("salvati_in_finestra", 0) < 3:
        print("    %d D salvati nella finestra: la forma non si misura" % an.get("salvati_in_finestra", 0))
        return
    print("    il tasso delle sole piatte (P0 + Ppi), sui D salvati nella finestra: %.5f (scarto massimo %.3e)" % (an["tasso_piatte"]["tasso"], an["tasso_piatte"]["scarto_max"]))
    pe = an["periodo"]
    print("    IL PERIODO dai cambi di segno di Re<D(t_rif), D(t)>: %s (%d cambi)" % (("%.2f tick, %.3f unita' di tempo" % (pe["tick"], pe["tau"])) if pe["tick"] is not None else "nessuno", pe["cambi"]))
    ro = an["rotazioni"]
    print("    LE ROTAZIONI PER BANDA (-arg<x(t), x(t+dt)>/dt, rispetto a mu): P0 %+.5f (dev %.1e, %+.4f .. %+.4f); Ppi %+.5f (dev %.1e, %+.4f .. %+.4f); LA SOMMA %+.5f (dev %.1e)"
          % (ro["P0"]["media"], ro["P0"]["dev"], ro["P0"]["min"], ro["P0"]["max"], ro["Ppi"]["media"], ro["Ppi"]["dev"], ro["Ppi"]["min"], ro["Ppi"]["max"], ro["somma"]["media"], ro["somma"]["dev"]))
    p0 = an["psi0"]
    print("    psi0: q %+.3e; la parte A %.5f di |psi0|^2, q_A %+.3e; le valli della parte A: %s" % (p0["q"], p0["frazione_A"], p0["q_A"], "  ".join("%s %.4f" % kv for kv in p0["valli_A"].items())))
    for t in sorted(an["istanti"], key=int):
        x = an["istanti"][t]
        print("    D a tempo %.2f (|D|/|psi0| %.3e):" % (x["tau"], x["nD"]))
        print("      le bande %s; gli anelli maggiori %s" % ("  ".join("%s %.4f" % kv for kv in x["bande"].items()), ", ".join("r %d %.4f" % (k, p) for k, p in x["anelli"])))
        print("      il profilo di |D|^2, r 0..%d: %s" % (R_PROFILO, " ".join("%.4f" % v for v in x["profilo"])))
        print("      le armoniche di drho: %s" % " ".join("m%d %.4f" % (m, v) for m, v in enumerate(x["armoniche_drho"])))
        print("      le armoniche della fase: %s" % " ".join("m%d %.4f" % (m, v) for m, v in enumerate(x["armoniche_fase"])))
        print("      Q_S per unita' di norma: D %+.3e, P0 %+.3e, Ppi %+.3e, le piatte %+.3e, A %+.3e" % (x["q"]["D"], x["q"]["P0"], x["q"]["Ppi"], x["q"]["piatte"], x["q"]["A"]))
        print("      le valli: P0 %s | Ppi %s" % ("  ".join("%s %.4f" % kv for kv in x["valli"]["P0"].items()), "  ".join("%s %.4f" % kv for kv in x["valli"]["Ppi"].items())))
        print("      le valli di Ppi contro quelle di P0 portate dalla mappa (somma delle differenze): %s" % "  ".join("%s %.4f" % kv for kv in x["mappe"].items()))


# ====================================================================== IL REFERTO
def referto():
    import _modo_al_variare_di_s as MS
    print("=" * 130)
    print("LA LEZIONE DELLE BANDE PIATTE E IL MODO LENTO A r %g, CON LE CONSERVAZIONI NEL DECADIMENTO (Luca 09:09 e 09:16; UNA DIAGNOSI); %s, L %d, eps 0, il congelato vero" % (R_ALTO, SB.CASO, MS.L))
    print("=" * 130)
    print("  la configurazione: R_ALTO %g R_LEZIONE %s T_FINE %d OGNI_PUNTO %d OGNI_D %d T_D_DA %d FATTORE_DEROGA %g SATURAZIONE %g ANELLI_M1 %s T1_FINE %d T1_DA %d OGNI1_D %d FATTORE_RUMORE1 %g TOLL_CONS %g R_PROFILO %d"
          % (R_ALTO, R_LEZIONE, T_FINE, OGNI_PUNTO, OGNI_D, T_D_DA, FATTORE_DEROGA, SATURAZIONE, ANELLI_M1, T1_FINE, T1_DA, OGNI1_D, FATTORE_RUMORE1, TOLL_CONS, R_PROFILO))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: punto 2: (m1) D nelle piatte P0+Ppi agli anelli 12-13: la coppia locale, la regola del punto 1 confermata; (m2) altrove (dove): la regola non basta."
          " Punto 2bis: (n1) tutte le conservazioni tornano: il decadimento e' permesso (come un atomo eccitato); (n2) una non torna: quale, e perche' decade lo stesso")
    print("-" * 130)
    print("### (1) LA LEZIONE: LE TRE CONDIZIONI LUNGO IL PROFILO (nessuna corsa); P0, Ppi dal tick libero di ogni r; alpha dal profilo di ogni stato; r 0.69 = la fettina tarata")
    with SB.scena() as (_rec, z, phi0, _p0, forma_, s):
        pz, mz, _cz, okz = MS.carica(SB.CASO)
        esito("DEVE PASSARE: lo stato fermo a r 1 = quello di dfb5ab7e (sha1)", okz, "")
        tab = []
        for r in R_LEZIONE:
            _A, E, a, b = SB.libero(z, phi0, s, r)
            P0, Ppi = float(E[..., 6:10].mean()), float(E[..., 0:4].mean())
            if r == 1.0:
                psi, mu = pz, mz
            else:
                c = SB.carica(r)
                esito("DEVE PASSARE: r %.4f, lo stato sul disco = la ricerca (sha1)" % r, c[3], "")
                psi, mu = c[0], c[1]
            _ra, am = SL.anelli(z, psi, forma_)
            ac, ad = float(am[0]), float(am[SL.R_MAX])
            inc, _ra = SL.conto("r %.4f%s" % (r, ", LA FETTINA TARATA" if r == 0.69 else ""), z, phi0, s, forma_, r, psi, mu, P0, Ppi)
            tab.append((r, a, b, P0, Ppi, mu, ac, ad, inc))
        print("  IL RIASSUNTO: le tre condizioni nella coda (alpha della coda) e nel cuore (alpha del cuore); d = mu + mu0 - 1 col mu0 del primo ordine")
        for r, a, b, P0, Ppi, mu, ac, ad, inc in tab:
            mu0 = 0.5 * math.sqrt(a * a - a * b + b * b)
            co = (P0 + Ppi + 2.0 * ad - 2.0 * mu, P0 + Ppi + 2.0 * ac - 2.0 * mu)
            c0 = (P0 + ad - mu, P0 + ac - mu)
            cp = (Ppi + ad - mu, Ppi + ac - mu)
            print("  r %.4f: a_n %.4f b_a %.4f mu0 %.4f; mu %+.6f, d %+.5f; alpha coda %.5f, cuore %.5f | la coppia %+.4f -> %+.4f (%s) | c1 P0 %+.4f -> %+.4f (%s) | c1 Ppi %+.4f -> %+.4f (%s)"
                  % (r, a, b, mu0, mu, mu + mu0 - 1.0, ad, ac, co[0], co[1], ",".join("%d-%d" % (k, k + 1) for k in inc["coppia"]) or "nessuno",
                     c0[0], c0[1], ",".join("%d-%d" % (k, k + 1) for k in inc["c1_P0"]) or "nessuno", cp[0], cp[1], ",".join("%d-%d" % (k, k + 1) for k in inc["c1_Ppi"]) or "nessuno"))
    print("-" * 130)
    print("### (2) IL MODO LENTO A r %g: %d tick dallo stato fermo; D(t) = e^{i mu s t} psi(t) - psi0" % (R_ALTO, T_FINE))
    fj = os.path.join(DIR_JSON, "modo_%s.json" % SB.nome_r(R_ALTO))
    letto = {}
    if not os.path.exists(fj):
        print("  nessuna corsa")
    else:
        fr = leggi(fj)
        esito("DEVE PASSARE: r %.4f, i punti ogni %d tick = lunga_%s, AL BIT (gli strumenti accesi in corsa)" % (R_ALTO, OGNI_PUNTO, SB.nome_r(R_ALTO)), fr["alpunto"] and fr["w_in_uguale"], "%d confronti" % fr["confronti"])
        esito("DEVE PASSARE: r %.4f, Q_S e M conservate entro %g relativo" % (R_ALTO, TOLL_CONS), fr["cons"] < TOLL_CONS, "%.1e" % fr["cons"])
        stampa(fr)
        letto["alto"] = fr
    print("-" * 130)
    print("### (2bis) r 1: i %d tick di 5f06dbfb rigenerati (s 0.3, L 81); D ogni %d tick da %d" % (T1_FINE, OGNI1_D, T1_DA))
    fj = os.path.join(DIR_JSON, "modo_r1_s0.3.json")
    if not os.path.exists(fj):
        print("  nessuna corsa")
    else:
        fr = leggi(fj)
        esito("DEVE PASSARE: r 1, i punti ogni %d tick = 26300537, AL BIT" % OGNI_PUNTO, fr["alpunto"], "%d confronti" % fr["confronti"])
        esito("DEVE PASSARE: r 1, Q_S e M conservate entro %g relativo" % TOLL_CONS, fr["cons"] < TOLL_CONS, "%.1e" % fr["cons"])
        stampa(fr)
        letto["uno"] = fr
    print("-" * 130)
    print("### LE LETTURE, COI CRITERI SCRITTI PRIMA")
    if "alto" in letto and letto["alto"]["analisi"].get("istanti"):
        ist = letto["alto"]["analisi"]["istanti"]
        m1 = [x["bande"]["P0"] + x["bande"]["Ppi"] > x["bande"]["A"] + x["bande"]["B"] and x["anelli"][0][0] in ANELLI_M1 for x in ist.values()]
        print("  punto 2, r %.4f: ai tre istanti, P0+Ppi > A+B e l'anello maggiore in %s: %s -> %s" % (R_ALTO, ANELLI_M1, m1, "(m1)" if all(m1) else "(m2)"))
    for k, fr in letto.items():
        an = fr["analisi"]
        if not an.get("istanti"):
            print("  punto 2bis, %s: nessun istante" % k)
            continue
        qp = [x["q"]["piatte"] for x in an["istanti"].values()]
        disp = max(max(qp) - min(qp), TOLL_CONS)
        q0 = an["psi0"]["q"]
        qok = abs(float(np.mean(qp)) - q0) <= disp
        ro = an["rotazioni"]["somma"]
        eok = abs(ro["media"]) <= max(ro["dev"], TOLL_CONS)
        print("  punto 2bis, r %g: Q_S: q delle piatte %s contro q(psi0) %+.3e, la dispersione %.1e: %s; la quasi-energia: la somma delle rotazioni %+.5f, la dev %.1e: %s"
              % (fr["r"], " ".join("%+.3e" % v for v in qp), q0, disp, "TORNA" if qok else "NON TORNA", ro["media"], ro["dev"], "TORNA" if eok else "NON TORNA"))
        an_, bn_ = SB.pesi_di(fr["r"])
        F0, Fpi = (bn_ - an_) / 2.0, -(an_ + bn_) / 2.0
        rot = an["rotazioni"]
        print("    AGGIUNTO DOPO I NUMERI (nessuna lettura): q - 1 delle parti ai tre istanti %s; q(D) - 1 %s;"
              " alpha* dalle rotazioni (rot - F + mu): da P0 %.4f, da Ppi %.4f; l'alpha dove la coppia si annulla mu - (P0 + Ppi)/2 %.4f; il periodo 2 pi / |rot| medio %.3f"
              % (" | ".join("P0 %+.1e Ppi %+.1e A %+.1e" % (x["q"]["P0"] - 1.0, x["q"]["Ppi"] - 1.0, x["q"]["A"] - 1.0) for x in an["istanti"].values()),
                 " ".join("%+.1e" % (x["q"]["D"] - 1.0) for x in an["istanti"].values()),
                 rot["P0"]["media"] - F0 + fr["mu"], rot["Ppi"]["media"] - Fpi + fr["mu"], fr["mu"] - (F0 + Fpi) / 2.0,
                 2.0 * math.pi / ((abs(rot["P0"]["media"]) + abs(rot["Ppi"]["media"])) / 2.0)))
    print("-" * 130)
    print("### AGGIUNTO DOPO I NUMERI (nessuna lettura): IL PERIODO CHE SI VEDE CAMPIONANDO OGNI dt UN'OSCILLAZIONE DI PERIODO P (l'alias: 1 / |1/P - n/dt|, n l'intero piu' vicino a dt/P)")
    for k, fr in letto.items():
        rot = fr["analisi"].get("rotazioni")
        pe = fr["analisi"].get("periodo")
        if not rot:
            continue
        for nome_, P in (("2 pi/|rot| medio", 2.0 * math.pi / ((abs(rot["P0"]["media"]) + abs(rot["Ppi"]["media"])) / 2.0)), ("i cambi di segno", pe.get("tau") if pe else None)):
            if not P:
                continue
            print("  r %g, P %.3f (%s): campionato ogni %s -> %s" % (fr["r"], P, nome_, ", ".join("%g" % dt for dt in DT_ALIAS),
                  ", ".join("%.2f" % (1.0 / abs(1.0 / P - round(dt / P) / dt)) if abs(1.0 / P - round(dt / P) / dt) > 0 else "inf" for dt in DT_ALIAS)))
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
        elif argv == ["--modo"]:
            modo()
        elif argv == ["--uno"]:
            uno()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
