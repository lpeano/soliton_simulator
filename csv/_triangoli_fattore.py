r"""**IL FATTORE 1.63-1.68 SUI TRIANGOLI: il pacchetto non fermo e l'impulso iniziale, e la scomposizione `F = R_t Q_b L`** *(solo in memoria; [[DECISIONE-SOLO-TRIANGOLI]],
[[PACCHETTO-K-NON-FERMO]])*.

> ### ⛔ **Il task history e' `2026-10-23_triangoli_fattore.md`** *(il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta, la convenzione nel repo e il nucleo intatti.**
> ### **Importati, non copiati:** `_triangoli_forza` *(`coppia_K`, `modo`, `matrice_L`, `v_max`, `v_fronte`, `tori`, e la correzione: `blocchi`, `A_di`, `theta_di`, `spazi_banda`, `pacchetto_banda`,
> `frazioni`, `corsa_con`)*, `_forza_da_cs` *(`pacchetto`, `fit_moto`)*, `_universalita_massa.blob`.

### **0** *(il pacchetto non fermo: le varianti, il tremolio di Dirac, l'avvio brusco e graduale)* · ### **A** *(`R_t`, `Q_b`, `L` dagli spettri)* · ### **B** *(la conferma dinamica col pacchetto di banda)*.

Gira con:  python csv/_triangoli_fattore.py > doc/referti_l2/triangoli_fattore.txt
"""
import io
import json
import math
import os
import subprocess
import sys
import time
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

RIF = "cbcb99c7"
NB = 12
EPS = (0.0, 0.5)
S0_P0 = (0.1, 0.5)
LX0 = 96
ETA0 = 1e-3
BATTIMENTI = 10
S_A = (0.02, 0.05, 0.1, 0.2, 0.3, 0.5)
KMAX = (0.1, 0.3)
NK = 200
N_RAMO = 400
S0_B = (0.05, 0.1, 0.3)
LX_B = (96, 192)
ETA_B = (0.0, 1e-3, -1e-3, 1e-2, -1e-2)
TOLL_ID = 1e-9
TOLL_RIF = 1e-6
TOLL_FERMO = 0.01
TOLL_VV = 0.01
PUO_RT = 0.01
PUO_QB = 0.05
PUO_F = 0.05
PUO_GRAD = 0.02
TOLL_CONT = 1e-9
TOLL_PORT = 1e-12
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_fattore.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-90s %s   %s" % (che[:90], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4f"):
    return "--" if x is None else fm % x


def av(x):
    return float((x + np.pi) % (2.0 * np.pi) - np.pi)


def periodo_dominante(tt, res):
    """### Il periodo del picco della trasformata del residuo *(senza la componente nulla)*."""
    if len(res) < 8:
        return None
    sp = np.abs(np.fft.rfft(res - np.mean(res)))
    fr = np.fft.rfftfreq(len(res), d=(tt[1] - tt[0]))
    j = int(np.argmax(sp[1:])) + 1
    return float(1.0 / fr[j])


def fit_con_oscillazione(tt, xx, Om):
    """### `x0 + v0 t + a t^2/2 + A cos(Om t) + B sin(Om t)`: `a` e l'ampiezza."""
    X = np.stack([np.ones_like(tt), tt, 0.5 * tt * tt, np.cos(Om * tt), np.sin(Om * tt)], axis=1)
    c, *_ = np.linalg.lstsq(X, xx, rcond=None)
    return float(c[2]), float(math.hypot(c[3], c[4]))


# =====================================================================================
#   PARTE 0 -- IL PACCHETTO NON FERMO E L'IMPULSO INIZIALE
# =====================================================================================
def parte_0():
    import _forza_da_cs as FC
    import _triangoli_forza as TF
    print("### PARTE 0 -- IL PACCHETTO NON FERMO E L'IMPULSO INIZIALE (Lx %d, eta %g; T = max(Lx/4, ceil(10 x 2 pi/delta_min)); la rampa %d battimenti)" % (LX0, ETA0, BATTIMENTI))
    print("  la simmetria di 120 gradi dell'inviluppo: NON si applica (sui tori a striscia l'inviluppo dipende solo da m1, la rotazione non e' una simmetria del toro)")
    TR = TF.tori()
    Lx = LX0
    peg_port = 0.0
    for toro in ("A", "B"):
        fk = TR[toro]["fase_K"]
        # ### la portante periodica: e^{i K.T} per i due periodi del toro
        for (d1, d2) in ((Lx, 0), (0, TF.LY)):
            m1, m2 = np.array([0.0, float(d1)]), np.array([0.0, float(d2)])
            ph = fk(m1, m2)
            peg_port = max(peg_port, abs(np.exp(1j * (ph[1] - ph[0])) - 1.0))
    esito("DI SERVIZIO: la portante e^{i K.r} periodica sui due tori (|e^{i K.T} - 1| per i due periodi)", peg_port < TOLL_PORT, "%.1e" % peg_port)
    righe = []
    for toro in ("A", "B"):
        tr = TR[toro]
        f = tr["f"]
        n = Lx * TF.LY
        m1 = (np.arange(n) // TF.LY).astype(float)
        m2 = (np.arange(n) % TF.LY).astype(float)
        x0, W = Lx / 4.0, Lx / 16.0
        qs = TF.q_della_striscia(Lx)
        for eps in EPS:
            for s0 in S0_P0:
                bande = TF.coppia_K(eps, s0)
                bl = TF.blocchi(eps, s0)
                spazi = [TF.spazi_banda(bl, b["Q"], toro, qs) for b in bande]
                salto = abs(bande[1]["w"] - bande[0]["w"])
                for q_, b in enumerate(bande):
                    t0 = time.time()
                    md = TF.modo(eps, s0, b)
                    Tm = max(Lx // 4, int(math.ceil(TF.PERIODI * 2.0 * np.pi / b["delta_min"])))
                    Tr = int(math.ceil(BATTIMENTI * 2.0 * np.pi / b["delta_min"]))
                    aH = -md["omega2_cart"] * md["dw_simm"] * (-s0 * ETA0 * 2.0 * np.pi / Lx) / f ** 2
                    base = FC.pacchetto(m1, x0, W, b["Q"][:, 0], tr["fase_K"](m1, m2))
                    varianti = {"base": (base, False), "centro": (FC.pacchetto(m1, x0 + 2.0 / 3.0, W, b["Q"][:, 0], tr["fase_K"](m1, m2)), False),
                                "2W": (FC.pacchetto(m1, x0, 2.0 * W, b["Q"][:, 0], tr["fase_K"](m1, m2)), False), "lineare": (base, True),
                                "banda": (TF.pacchetto_banda(toro, Lx, x0, W, b["Q"], spazi[q_], m1, m2), True)}
                    print("  %s eps %g s0 %g banda %d: w %+.4f salto %.4f (2 pi/salto %.1f) delta_min %.4f (2 pi/delta_min %.1f) T %d rampa %d"
                          % (toro, eps, s0, q_, b["w"], salto, 2 * np.pi / salto, b["delta_min"], 2 * np.pi / b["delta_min"], Tm, Tr))
                    for nome, (cel, lin) in varianti.items():
                        fb, fp, fr = TF.frazioni(cel, toro, Lx, spazi[q_], spazi[1 - q_])
                        z, tz, xz = TF.corsa_con(toro, Lx, eps, s0, 0.0, cel, "simm", Tm, 0, lin)
                        p, tp, xp = TF.corsa_con(toro, Lx, eps, s0, ETA0, cel, "simm", Tm, 0, lin)
                        m, _tm, _xm = TF.corsa_con(toro, Lx, eps, s0, -ETA0, cel, "simm", Tm, 0, lin)
                        dif, ss = 0.5 * (p["a"] - m["a"]), 0.5 * (p["a"] + m["a"])
                        X = np.stack([np.ones_like(tz), tz, 0.5 * tz * tz], axis=1)
                        res = xz - X @ np.linalg.lstsq(X, xz, rcond=None)[0]
                        per = periodo_dominante(tz, res)
                        a_s, A_s = fit_con_oscillazione(tp, xp, salto)
                        a_d, A_d = fit_con_oscillazione(tp, xp, b["delta_min"])
                        rec = {"tipo": "variante", "toro": toro, "eps": eps, "s0": s0, "banda": q_, "variante": nome, "lineare": lin, "frazioni": [fb, fp, fr],
                               "v0": z["v0"], "a0": z["a"], "sigma_a0": z["sigma_a"], "tremolio": z["residuo_max"], "periodo_residuo": per,
                               "periodo_salto": 2 * np.pi / salto, "periodo_delta_min": 2 * np.pi / b["delta_min"], "a_piu": p["a"], "a_meno": m["a"], "differenziale": dif,
                               "semisomma": ss, "a0_su_dif": z["a"] / dif, "dif_su_aH": dif / aH, "gamma0": p["gamma0"], "gamma_medio": p["gamma_medio"],
                               "dif_su_aH_gamma": dif / (aH * p["gamma_medio"]), "a_osc_salto": a_s, "ampiezza_salto": A_s, "a_osc_dmin": a_d, "ampiezza_dmin": A_d, "a_H": aH}
                        if nome in ("base", "banda"):
                            gp, _a, _b = TF.corsa_con(toro, Lx, eps, s0, ETA0, cel, "simm", Tm, Tr, lin)
                            gm, _a, _b = TF.corsa_con(toro, Lx, eps, s0, -ETA0, cel, "simm", Tm, Tr, lin)
                            dg = 0.5 * (gp["a"] - gm["a"])
                            rec.update(graduale={"differenziale": dg, "dif_su_aH": dg / aH, "gamma_medio": gp["gamma_medio"], "dif_su_aH_gamma": dg / (aH * gp["gamma_medio"]),
                                                 "semisomma": 0.5 * (gp["a"] + gm["a"])})
                        scrivi(rec)
                        righe.append(rec)
                        g = rec.get("graduale")
                        print("    %-7s fraz (banda %.4f altra %.1e resto %.1e) | eta 0: v0 %+.2e a0 %+.2e +- %.1e tremolio %.1e periodo %s | dif %+.3e a0/dif %+.4f semis-a0 %+.1e | "
                              "dif/a_H %.4f /(a_H <g>) %.4f (g0 %.4f <g> %.4f) | con oscillazione a salto %+.4f ampiezza %.1e, a delta_min %+.4f ampiezza %.1e%s"
                              % (nome, fb, fp, fr, z["v0"], z["a"], z["sigma_a"], z["residuo_max"], f_(per, "%.1f"), dif, z["a"] / dif, ss - z["a"], dif / aH,
                                 rec["dif_su_aH_gamma"], p["gamma0"], p["gamma_medio"], (a_s - p["a"]) / p["a"], A_s, (a_d - p["a"]) / p["a"], A_d,
                                 "" if not g else " | GRADUALE: dif/a_H %.4f /(a_H <g>) %.4f (<g> %.4f)" % (g["dif_su_aH"], g["dif_su_aH_gamma"], g["gamma_medio"])))
                        sys.stdout.flush()
                    print("    (%.0f s)" % (time.time() - t0))
    ban = [r for r in righe if r["variante"] == "banda"]
    peg = max(abs(r["a0_su_dif"]) for r in ban)
    esito("DEVE PASSARE (la prova della correzione): il pacchetto di banda, |a(eta 0)| sotto l'1%% del differenziale a eta %g, i due tori (%d)" % (ETA0, len(ban)), peg < TOLL_FERMO, "il peggiore %.2e" % peg)
    banA = [r for r in ban if r["toro"] == "A"]
    ok = all(abs(r["graduale"]["dif_su_aH"] - 1.0) <= PUO_GRAD for r in banA)
    esito("PUO' FALLIRE: con l'avvio graduale a_mis/a_H entro %g da 1 (il pacchetto di banda, toro A), a_H/a_RG invariato (dagli spettri, per costruzione)" % PUO_GRAD, ok,
          " ".join("%.4f" % r["graduale"]["dif_su_aH"] for r in banA))
    return righe


# =====================================================================================
#   PARTE A -- LA SCOMPOSIZIONE DEL FATTORE
# =====================================================================================
def ramo_lungo(bl, Q, w0, qmax, N):
    """### La fase del ramo lungo la normale ad `a2` da `K` *(toro `A`)*, ### **seguita per sovrapposizione del vettore**: `q` *(in theta)* e `omega(q)`."""
    import _triangoli_forza as TF
    qq = np.linspace(0.0, qmax, N + 1)
    V = Q[:, [0]]
    w = w0
    out = [w0]
    for q in qq[1:]:
        lam, VV = np.linalg.eig(TF.A_di(bl, *TF.theta_di("A", q)))
        j = int(np.argmax(np.abs(VV.conj().T @ V)[:, 0]))
        w = w + av(-np.angle(lam[j]) - w)
        out.append(w)
        V = VV[:, [j]]
    return qq, np.array(out)


def parte_A(p0):
    import _triangoli_forza as TF
    print("### PARTE A -- LA SCOMPOSIZIONE F = R_t Q_b L (zero simmetrico; il fit omega^2 - omega(0)^2 = v_b^2 k^2 + b k^4, k cartesiano lungo la normale ad a2, k_max %s, %d punti)" % (KMAX, NK))
    rif = [json.loads(x) for x in subprocess.run(["git", "show", "%s:doc/referti_l2/triangoli_forza.jsonl" % RIF], capture_output=True, cwd=RADICE,
                                                  check=True).stdout.decode("utf-8").splitlines() if x.strip()]
    vel = {(r["eps"], r["s"], r["banda"]): r for r in rif if r.get("tipo") == "velocita"}
    righe, peg_id, peg_rif, n_rif, peg_cont, vm_bit = [], 0.0, 0.0, 0, 0.0, None
    for eps in EPS:
        for s in S_A:
            t0 = time.time()
            vm, kvm, _w = TF.v_max(TF.matrice_L(eps, s))
            if (eps, s, 0) in vel:
                vf = vel[(eps, s, 0)]["v_fronte"]
                fonte_f = RIF
                if s == 0.3 and eps == 0.0:
                    vm_bit = vm == vel[(eps, s, 0)]["v_max"]
            else:
                vf = TF.v_fronte(eps, s)[0]
                fonte_f = "nuova"
            bl = TF.blocchi(eps, s)
            for q_, b in enumerate(TF.coppia_K(eps, s)):
                md = TF.modo(eps, s, b)
                w0, om, dws = md["w"], md["omega2_cart"], md["dw_simm"]
                peg_cont = max(peg_cont, abs(w0 - (md["omega_cont"] + np.pi * s)))
                fit = {}
                for km in KMAX:
                    qq, ww = ramo_lungo(bl, b["Q"], w0, km * math.sqrt(3.0) / 2.0, NK)
                    k = qq * 2.0 / math.sqrt(3.0)
                    y = ww ** 2 - w0 ** 2
                    X = np.stack([k ** 2, k ** 4], axis=1)
                    c, *_ = np.linalg.lstsq(X, y, rcond=None)
                    qual = float(np.max(np.abs(y - X @ c)) / max(float(np.max(np.abs(y))), 1e-300))
                    fit[str(km)] = {"v_b": float(math.sqrt(c[0])) if c[0] > 0 else None, "b": float(c[1]), "qualita": qual}
                qq, ww = ramo_lungo(bl, b["Q"], w0, np.pi, N_RAMO)
                k = qq * 2.0 / math.sqrt(3.0)
                v_ramo = float(np.max(np.abs(np.diff(ww) / np.diff(k))))
                vb = fit[str(KMAX[0])]["v_b"]
                R_t = s * dws / w0
                Q_b = w0 * om / vb ** 2
                cand = {"v_max": vm, "v_fit": md["v_fit"], "v_ramo": v_ramo, "v_b": vb, **{"v_fronte_%s" % kk: v for kk, v in vf.items()}}
                fat = {}
                for nome, c_ in cand.items():
                    Lc = (vb / c_) ** 2
                    F = s * om * dws / c_ ** 2
                    peg_id = max(peg_id, abs(F - R_t * Q_b * Lc) / abs(F))
                    fat[nome] = {"c": c_, "c_su_s": c_ / s, "L": Lc, "F": F}
                if eps == 0.0 and s in (0.3, 0.5) and (eps, s, q_) in vel:
                    h = vel[(eps, s, q_)]["H_su_RG"]["simm"]
                    for nome in ("v_max", "v_fit"):
                        n_rif += 1
                        peg_rif = max(peg_rif, abs(fat[nome]["F"] - h[nome]) / abs(h[nome]))
                rec = {"tipo": "fattori", "eps": eps, "s": s, "banda": q_, "omega0": w0, "dw_ds": dws, "omega2": om, "anisotropia": md["anisotropia"], "fit": fit,
                       "v_ramo": v_ramo, "R_t": R_t, "Q_b": Q_b, "Q_b_kmax2": w0 * om / fit[str(KMAX[1])]["v_b"] ** 2 if fit[str(KMAX[1])]["v_b"] else None,
                       "fattori": fat, "fronte": fonte_f}
                scrivi(rec)
                righe.append(rec)
                print("  eps %g s %-4g banda %d: omega0 %+.5f d omega/ds %+.4f omega'' %+.5f (aniso %.1e) | fit k_max %s: v_b/s %s b %s qualita' %s | v_ramo/s %.4f | R_t %.5f Q_b %.5f (k_max 2: %s)"
                      % (eps, s, q_, w0, dws, om, md["anisotropia"], "/".join(str(x) for x in KMAX), "/".join(f_(fit[str(x)]["v_b"] and fit[str(x)]["v_b"] / s, "%.4f") for x in KMAX),
                         "/".join("%+.3e" % fit[str(x)]["b"] for x in KMAX), "/".join("%.1e" % fit[str(x)]["qualita"] for x in KMAX), v_ramo / s, R_t, Q_b, f_(rec["Q_b_kmax2"], "%.5f")))
                print("      " + " | ".join("%s: c/s %.4f L %.4f F %.4f" % (nn, d["c_su_s"], d["L"], d["F"]) for nn, d in fat.items()))
                sys.stdout.flush()
            print("    (eps %g s %g: %.0f s; il fronte: %s)" % (eps, s, time.time() - t0, fonte_f))
    esito("DEVE PASSARE: F = R_t Q_b L entro %g relativo, ogni riga e ogni c" % TOLL_ID, peg_id <= TOLL_ID, "il peggiore %.1e" % peg_id)
    esito("DEVE PASSARE: F(v_max) e F(v_fit) a s 0.3, 0.5, eps 0 = gli a_H/a_RG simmetrici di %s entro %g (%d valori)" % (RIF, TOLL_RIF, n_rif), n_rif == 8 and peg_rif <= TOLL_RIF,
          "il peggiore %.1e" % peg_rif)
    esito("DI SERVIZIO: omega(0) principale = la fase continua + pi s entro %g" % TOLL_CONT, peg_cont <= TOLL_CONT, "%.1e" % peg_cont)
    esito("DI SERVIZIO: v_max a s 0.3, eps 0 = quella di %s al bit" % RIF, bool(vm_bit), "")
    sel = [r for r in righe if r["eps"] == 0.0 and r["s"] == 0.3]
    vere = [abs(r["fattori"]["v_fit"]["c"] - r["fattori"]["v_max"]["c"]) <= TOLL_VV * r["fattori"]["v_max"]["c"] for r in sel]
    chiave = all(r["fattori"]["v_fit"]["c"] > 0 and r["fattori"]["v_max"]["c"] > 0 for r in sel)
    esito("DEVE FALLIRE: <<v_fit e v_max coincidono entro l'1%% a s 0.3>> (eps 0, le due bande; la chiave: tutte e due finite e positive)", not any(vere) and chiave and len(sel) == 2,
          " ".join("v_fit/v_max %.4f" % (r["fattori"]["v_fit"]["c"] / r["fattori"]["v_max"]["c"]) for r in sel))
    pic = [r for r in righe if r["s"] <= 0.1]
    esito("PUO' FALLIRE: R_t entro %g da 1 a s <= 0.1 (ogni eps, banda)" % PUO_RT, all(abs(r["R_t"] - 1) <= PUO_RT for r in pic), " ".join("%.5f" % r["R_t"] for r in pic))
    esito("PUO' FALLIRE: Q_b entro %g da 1 a s <= 0.1 (k_max %g)" % (PUO_QB, KMAX[0]), all(abs(r["Q_b"] - 1) <= PUO_QB for r in pic), " ".join("%.5f" % r["Q_b"] for r in pic))
    esito("PUO' FALLIRE: con c = v_b, F entro %g da 1 a s <= 0.1" % PUO_F, all(abs(r["fattori"]["v_b"]["F"] - 1) <= PUO_F for r in pic),
          " ".join("%.5f" % r["fattori"]["v_b"]["F"] for r in pic))
    print("### IL LIMITE A s -> 0 (la lineare dai due s piu' piccoli, la quadratica dai tre)")
    for eps in EPS:
        for q_ in (0, 1):
            rr = [r for r in righe if r["eps"] == eps and r["banda"] == q_]
            for nome, fn in (("R_t", lambda r: r["R_t"]), ("Q_b", lambda r: r["Q_b"]), ("L(v_max)", lambda r: r["fattori"]["v_max"]["L"]),
                             ("L(v_fit)", lambda r: r["fattori"]["v_fit"]["L"]), ("F(v_max)", lambda r: r["fattori"]["v_max"]["F"]), ("v_b/v_max", lambda r: r["fattori"]["v_b"]["c"] / r["fattori"]["v_max"]["c"])):
                y = [fn(r) for r in rr]
                xs = [r["s"] for r in rr]
                lin = y[0] - xs[0] * (y[1] - y[0]) / (xs[1] - xs[0])
                quad = float(np.polyval(np.polyfit(xs[:3], y[:3], 2), 0.0))
                scrivi({"tipo": "limite", "eps": eps, "banda": q_, "che": nome, "y": y, "s": xs, "lineare": lin, "quadratica": quad})
                print("  eps %g banda %d %-10s: %s | lineare %.5f quadratica %.5f" % (eps, q_, nome, " ".join("%.5f" % v for v in y), lin, quad))
    return righe


# =====================================================================================
#   PARTE B -- LA CONFERMA DINAMICA
# =====================================================================================
def parte_B(ra):
    import _triangoli_forza as TF
    print("### PARTE B -- LA CONFERMA DINAMICA (toro A, eps 0, il pacchetto di banda, il baricentro lineare, l'avvio brusco)")
    righe = []
    f = TF.tori()["A"]["f"]
    for s0 in S0_B:
        bande = TF.coppia_K(0.0, s0)
        bl = TF.blocchi(0.0, s0)
        fat = {r["banda"]: r for r in ra if r["eps"] == 0.0 and abs(r["s"] - s0) < 1e-12}
        for Lx in LX_B:
            n = Lx * TF.LY
            m1 = (np.arange(n) // TF.LY).astype(float)
            m2 = (np.arange(n) % TF.LY).astype(float)
            qs = TF.q_della_striscia(Lx)
            for q_, b in enumerate(bande):
                md = TF.modo(0.0, s0, b)
                Tm = max(Lx // 4, int(math.ceil(TF.PERIODI * 2.0 * np.pi / b["delta_min"])))
                cel = TF.pacchetto_banda("A", Lx, Lx / 4.0, Lx / 16.0, b["Q"], TF.spazi_banda(bl, b["Q"], "A", qs), m1, m2)
                rs = {eta: TF.corsa_con("A", Lx, 0.0, s0, eta, cel, "simm", Tm, 0, True)[0] for eta in ETA_B}
                for eta in (1e-3, 1e-2):
                    dif, ss = 0.5 * (rs[eta]["a"] - rs[-eta]["a"]), 0.5 * (rs[eta]["a"] + rs[-eta]["a"])
                    dsdm = -s0 * eta * 2.0 * np.pi / Lx
                    aH = -md["omega2_cart"] * md["dw_simm"] * dsdm / f ** 2
                    g = rs[eta]["gamma_medio"]
                    rRG = {nome: dif / (-d["c"] ** 2 * (dsdm / s0) / f ** 2) for nome, d in fat[q_]["fattori"].items()}
                    rec = {"tipo": "conferma", "s0": s0, "Lx": Lx, "banda": q_, "eta": eta, "differenziale": dif, "semisomma": ss, "a0": rs[0.0]["a"], "sigma_a0": rs[0.0]["sigma_a"],
                           "a0_su_dif": rs[0.0]["a"] / dif, "dif_su_aH": dif / aH, "gamma_medio": g, "dif_su_aH_gamma": dif / (aH * g), "dif_su_aRG": rRG,
                           "specchio_grezzo": abs(abs(rs[eta]["a"]) - abs(rs[-eta]["a"])) / max(abs(rs[eta]["a"]), abs(rs[-eta]["a"]))}
                    scrivi(rec)
                    righe.append(rec)
                    print("  s0 %-4g Lx %d banda %d eta %-6g T %d: dif %+.4e semis %+.2e a0 %+.2e (a0/dif %.1e) | dif/a_H %.4f /(a_H <g>) %.4f (<g> %.4f) | dif/a_RG: %s | specchio grezzo %.4f"
                          % (s0, Lx, q_, eta, Tm, dif, ss, rs[0.0]["a"], rec["a0_su_dif"], dif / aH, rec["dif_su_aH_gamma"], g, " ".join("%s %.4f" % (k, v) for k, v in rRG.items()),
                             rec["specchio_grezzo"]))
                    sys.stdout.flush()
    sel = [r for r in righe if r["eta"] == 1e-3]
    peg = max(abs(r["a0_su_dif"]) for r in sel)
    esito("DEVE PASSARE: parte B, il pacchetto corretto, |a(eta 0)| sotto l'1%% del differenziale a eta 1e-3 (%d)" % len(sel), peg < TOLL_FERMO, "il peggiore %.2e" % peg)
    return righe


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 110)
    print("IL FATTORE 1.63-1.68 SUI TRIANGOLI: il pacchetto non fermo e l'impulso iniziale, e la scomposizione F = R_t Q_b L")
    print("=" * 110)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py", "csv/_triangoli_forza.py", "csv/_forza_da_cs.py",
                                     "csv/_zero_simmetrico.py", "csv/_gravita_collettiva.py", "csv/_modi_pi_e_solitoni.py", "csv/_moneta_massa.py", "csv/_universalita_massa.py",
                                     "csv/_triangoli_fattore.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: RIF %s; EPS %s; S0_P0 %s; LX0 %d; ETA0 %g; BATTIMENTI %d; S_A %s; KMAX %s; NK %d; N_RAMO %d; S0_B %s; LX_B %s; ETA_B %s;"
          % (RIF, EPS, S0_P0, LX0, ETA0, BATTIMENTI, S_A, KMAX, NK, N_RAMO, S0_B, LX_B, ETA_B))
    print("    TOLL_ID %g TOLL_RIF %g TOLL_FERMO %g TOLL_VV %g PUO_RT %g PUO_QB %g PUO_F %g PUO_GRAD %g TOLL_CONT %g TOLL_PORT %g"
          % (TOLL_ID, TOLL_RIF, TOLL_FERMO, TOLL_VV, PUO_RT, PUO_QB, PUO_F, PUO_GRAD, TOLL_CONT, TOLL_PORT))
    print("-" * 110)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    p0 = parte_0()
    print("-" * 110)
    ra = parte_A(p0)
    print("-" * 110)
    parte_B(ra)
    print("=" * 110)
    print("IL FATTORE SUI TRIANGOLI: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
