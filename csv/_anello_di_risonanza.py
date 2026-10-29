# -*- coding: utf-8 -*-
r"""**L'ANELLO DI RISONANZA E IL TERZO PASSO** *(il mandato di Luca delle `12:11` del `2026-10-29`; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-29_anello_di_risonanza.md`)*:
### **(1)-(3)** per ogni anello dello stato fermo la frequenza locale delle bande piatte *(il tick libero piu' il legame, che e' uno scalare per nodo: `alpha(rho/Lambda) s` per tick)*
### contro quella del solitone, e dove le condizioni si incrociano; ### **(4)** `S1` `s 0.075` dallo stato di `dfb5ab7e`, `180` unita' di tempo, l'esame di `dfb5ab7e` con la finestra in deroga.

    python csv/_anello_di_risonanza.py --referto > doc/referti_l2/anello_di_risonanza.txt
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

CASI_CONTO = ("S1_s0.300", "S1_s0.150")
CASO_TERZO = "S1_s0.075"
R_MAX = 24
PERIODO = 11.45                # ### il periodo del modo (dfb5ab7e), in unita' di tempo
FATTORE_RUMORE_DEROGA = 10.0   # ### la deroga del terzo passo (il task history)
SATURAZIONE = 1e-2
T_FIS = 180.0
T_DA_FIS = 60.0
PASSO_FIS = 3.0
SOGLIE_FORMA = (1e-4, 1e-3)
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


def avvolgi(x):
    return (x + math.pi) % (2.0 * math.pi) - math.pi


def incroci(vals):
    return [r for r in range(len(vals) - 1) if vals[r] == vals[r] and vals[r + 1] == vals[r + 1] and vals[r] * vals[r + 1] < 0.0 and abs(vals[r] - vals[r + 1]) < math.pi]   # ### non il salto dell'avvolgimento


def conto(nome):
    import _diagnosi_s4 as D
    import _energia_del_legame as EL
    import _modo_al_variare_di_s as MS
    import _screening_forme_s3 as SF
    import flussi_parziali as FP
    _n, forma, s, N = MS.caso(nome)
    print("-" * 130)
    psi0, mu, cj, ok = MS.carica(nome)
    print("### %s: %s, s %g, N %g; mu %+.9f; ph_sol = mu s = %+.6f per tick" % (nome, forma, s, N, mu, mu * s))
    esito("DEVE PASSARE: %s, lo stato fermo sul disco = quello della ricerca (sha1), e fermo" % nome, ok and cj["convergito"], "%.3e" % cj["residuo_finale"])
    with D.configura(forma, s, N):
        rec, z, phi0, _p0 = MS.scena(forma, s, N)
        dt = FP.dtau_nodo(z["mot"])
        esito("DEVE PASSARE: %s, dtau = s su ogni nodo" % nome, bool(np.all(dt == s)), "min %g max %g" % (dt.min(), dt.max()))
        z["st"]["psi_h"][...] = psi0
        rho, lam = EL.densita(z["inc"], z["st"])
        al = SF.pezzi_di(forma)(rho, lam)[0]
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    k = np.floor(d).astype(int)
    qn = np.bincount(k)
    ra = np.bincount(k, weights=rho) / np.maximum(qn, 1)
    am = np.bincount(k, weights=al) / np.maximum(qn, 1)
    phs = mu * s
    om = 2.0 * math.pi * s / PERIODO
    print("  r: rho medio / picco dell'anello, alpha medio; ph_P0 = alpha s, ph_Ppi = -pi s + alpha s; (c1) ph_p - ph_sol; (c2) ph_p + ph_p' - 2 ph_sol (avvolte, per tick); Omega del modo %.5f per tick" % om)
    tab = {"c1_P0": [], "c1_Ppi": [], "c2_P0P0": [], "c2_P0Ppi": [], "c2_PpiPpi": [], "m_P0": [], "m_Ppi": []}
    picco = float(ra.max())
    for r in range(R_MAX + 1):
        a = float(am[r])
        p0, pp = a * s, -math.pi * s + a * s
        v = {"c1_P0": avvolgi(p0 - phs), "c1_Ppi": avvolgi(pp - phs), "c2_P0P0": avvolgi(2 * p0 - 2 * phs), "c2_P0Ppi": avvolgi(p0 + pp - 2 * phs),
             "c2_PpiPpi": avvolgi(2 * pp - 2 * phs), "m_P0": abs(avvolgi(p0 - phs)) - om, "m_Ppi": abs(avvolgi(pp - phs)) - om}
        for kk in tab:
            tab[kk].append(v[kk])
        print("  r %2d: rho/picco %.4e  alpha %.5f | c1 P0 %+.5f  Ppi %+.5f | c2 P0+P0 %+.5f  P0+Ppi %+.5f  Ppi+Ppi %+.5f | |c1| - Omega: P0 %+.5f  Ppi %+.5f"
              % (r, ra[r] / picco, a, v["c1_P0"], v["c1_Ppi"], v["c2_P0P0"], v["c2_P0Ppi"], v["c2_PpiPpi"], v["m_P0"], v["m_Ppi"]))
    print("  GLI INCROCI (un cambio di segno fra l'anello r e r+1):")
    out = {}
    for kk in ("c1_P0", "c1_Ppi", "c2_P0P0", "c2_P0Ppi", "c2_PpiPpi", "m_P0", "m_Ppi"):
        x = incroci(tab[kk])
        out[kk] = x
        print("    %-10s %s" % (kk, ("fra gli anelli " + ", ".join("%d-%d" % (r, r + 1) for r in x)) if x else "nessuno"))
    return out


def terzo():
    import _diagnosi_s4 as D
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _modo_instabile as MI
    _n, forma, s, N = MS.caso(CASO_TERZO)
    print("-" * 130)
    psi0, mu, cj, ok = MS.carica(CASO_TERZO)
    print("### IL TERZO PASSO: %s, s %g; dallo stato di dfb5ab7e (residuo %.3e, NON fermo secondo il criterio); mu %+.9f" % (CASO_TERZO, s, cj["residuo_finale"], mu))
    esito("DEVE PASSARE: %s, lo stato sul disco = quello della ricerca (sha1)" % CASO_TERZO, ok, "%s" % cj["sha"][:8])
    with D.configura(forma, s, N):
        rec, z, phi0, _p0 = MS.scena(forma, s, N)
        v = MS.Vista(z, psi0)
        ogni = int(round(PASSO_FIS / s))
        t_fine = int(round(T_FIS / s))
        t_da = int(round(T_DA_FIS / s))
        M0 = float(np.sum(np.abs(psi0) ** 2))
        psi = psi0.copy()
        Dd = {}
        dM = 0.0
        s0 = time.time()
        for t in range(1, t_fine + 1):
            psi = MS.tick(z, phi0, psi, forma)
            if t % ogni == 0:
                dM = max(dM, abs(float(np.sum(np.abs(psi) ** 2)) / M0 - 1.0))
                if t >= t_da:
                    Dd[t] = np.exp(1j * mu * s * t) * psi - psi0
        esito("DEVE PASSARE: %s, M conservata entro %g" % (CASO_TERZO, TOLL_NORMA), dM < TOLL_NORMA, "%.1e; %d tick in %.0f s" % (dM, t_fine, time.time() - s0))
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
    n0 = math.sqrt(M0)
    ts = sorted(Dd)
    nD = np.array([float(np.linalg.norm(Dd[t])) / n0 for t in ts])
    print("  |D|/|psi0| ogni %d tick da %d: %s" % (ogni, t_da, " ".join("%.1e" % x for x in nD)))
    basso = FATTORE_RUMORE_DEROGA * cj["residuo_finale"]
    fin = [i for i in range(len(ts)) if basso < nD[i] < SATURAZIONE]
    if len(fin) < 3:
        print("  la finestra (in deroga: fra %.1e e %.0e) ha %d campioni: il tasso non si misura" % (basso, SATURAZIONE, len(fin)))
        return None
    a, b = fin[0], fin[-1]
    tt = np.array(ts[a:b + 1], dtype=float)
    pend = float(np.polyfit(tt, np.log(nD[a:b + 1]), 1)[0])
    loc = [(math.log(nD[i + 1]) - math.log(nD[i - 1])) / (2.0 * ogni) / s for i in range(max(a, 1), min(b, len(ts) - 2) + 1)]
    print("  la finestra (in DEROGA: fra %.1e e %.0e): t %d .. %d (tempo %.0f .. %.0f); il tasso %.5f per tick, %.5f per unita' di tempo; le pendenze locali da %.4f a %.4f"
          % (basso, SATURAZIONE, ts[a], ts[b], ts[a] * s, ts[b] * s, pend, pend / s, min(loc) if loc else float("nan"), max(loc) if loc else float("nan")))
    tc = ts[(a + b) // 2]
    proj = [float(np.real(np.vdot(Dd[tc], Dd[t]))) / (float(np.linalg.norm(Dd[tc])) * float(np.linalg.norm(Dd[t]))) for t in ts[a:b + 1]]
    cambi = [i for i in range(1, len(proj)) if proj[i - 1] * proj[i] < 0.0]
    if len(cambi) >= 2:
        print("  il periodo: %.2f unita' di tempo (%d cambi); 2 pi / |mu| %.3f" % (2.0 * ogni * float(np.mean(np.diff(cambi))) * s, len(cambi), 2 * math.pi / abs(mu)))
    else:
        print("  %d cambi di segno: il periodo non si misura" % len(cambi))
    istanti = []
    for so in SOGLIE_FORMA:
        cc = [t for t, x in zip(ts, nD) if x >= so]
        if cc:
            istanti.append(cc[0])
    istanti.append(ts[b])
    for t in sorted(set(istanti)):
        dd = Dd[t] / float(np.linalg.norm(Dd[t]))
        dr, _df = MI.per_nodo(v, dd)
        wd, kk = MI.armoniche(v, dr)
        prd = np.bincount(kk, weights=np.sum(np.abs(dd.reshape(v.n, 12)) ** 2, axis=1))
        prd = prd / prd.sum()
        top = np.argsort(-prd)[:3]
        Pk = DV.pesi(dd.reshape(v.n, 12), np.ones(v.n), Z, MS.L)
        tot = float(Pk.sum())
        print("  t %d (tempo %.0f, |D|/|psi0| %.1e): gli anelli maggiori %s; le bande %s; le armoniche di drho %s"
              % (t, t * s, float(np.linalg.norm(Dd[t])) / n0, ", ".join("r %d %.3f" % (k, prd[k]) for k in top),
                 "  ".join("%s %.3f" % (g, float(Pk[:, :, list(idx)].sum()) / tot) for g, idx in DV.GRUPPI), " ".join("m%d %.3f" % (mm, wd[mm]) for mm in range(MI.M_MAX + 1))))
    return pend / s


def referto():
    print("=" * 130)
    print("L'ANELLO DI RISONANZA E IL TERZO PASSO (Luca 12:11): la frequenza locale delle piatte per anello contro quella del solitone; S1 s 0.075 dallo stato di dfb5ab7e")
    print("=" * 130)
    print("  la configurazione: CASI_CONTO %s CASO_TERZO %s R_MAX %d PERIODO %g FATTORE_RUMORE_DEROGA %g SATURAZIONE %g T_FIS %g T_DA_FIS %g PASSO_FIS %g SOGLIE_FORMA %s TOLL_NORMA %g"
          % (CASI_CONTO, CASO_TERZO, R_MAX, PERIODO, FATTORE_RUMORE_DEROGA, SATURAZIONE, T_FIS, T_DA_FIS, PASSO_FIS, SOGLIE_FORMA, TOLL_NORMA))
    print("  IL PUNTO 1 (dal codice, il task history): il legame e' exp(-i alpha(rho/Lambda) dtau f) uguale su tutte le 12 componenti del nodo, due volte con f 0.5: alpha s per tick su ogni banda")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (r1) un incrocio negli anelli 12-13 a tutte e due le s; (r2) altrove; (r3) nessuno; (r4) altro. Il terzo passo: il terzo punto della serie 0.139, 0.151")
    for nome in CASI_CONTO:
        conto(nome)
    t3 = terzo()
    print("-" * 130)
    print("### LA SERIE DEL TASSO per unita' di tempo: s 0.3 0.13870, s 0.15 0.15108 (dfb5ab7e); s 0.075 %s" % (("%.5f" % t3) if t3 is not None else "--"))
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
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
