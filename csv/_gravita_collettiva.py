r"""**LA GRAVITA' COLLETTIVA SULLA CARTA: la frequenza a riposo della materia legata al variare di `s`** *(`S1`, `S3`, `S4`; spettri e stati stazionari, nessuna dinamica lunga)*.

> ### ⛔ **Il task history e' `2026-10-23_gravita_collettiva.md`** *(le verifiche nel codice, il metodo, le previsioni e i criteri, fissati prima)*. ### **`dtau`, `eps`, `cs` e la
> forma della non linearita' SOLO nella scena, in memoria**; ### **`leggi.yaml` e l'impronta intatti.** ### **Importati, non copiati:** `_forza_da_cs` *(`rami`, `spazio_del_ramo`,
> `segui`, `avvolgi`)*, `_stabilita_lineare` *(`scena`, `passo`, `green`, `copia`)*, `_screening_forme_s3` *(`forma`, `pezzi_di`)*.

### **LIVELLO 1:** ### **lo stato uniforme `a * e(k = 0)` di ogni ramo massivo, a `x = rho0/Lambda0`**: ### **la stazionarieta' per settore, `omega_tot`, la scomposizione
`omega_ramo(0) + alpha s`, la pendenza `d ln omega_tot/d ln s`, lo stato piu' basso, la stabilita'** *(la Green di un tick nel riferimento che ruota)*. ### **LIVELLO 2:** ### **il
solitone efficace `mu u = -c lap u + s alpha(u^2) u`** *(radiale in `2d`, flusso di gradiente normalizzato implicito)*, ### **`omega_sol = omega0 + mu`, la larghezza, la densita' al
centro, la pendenza**; ### **il controllo a `c` costante.**

Gira con:  python csv/_gravita_collettiva.py > doc/referti_l2/gravita_collettiva.txt
"""
import io
import json
import os
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

FORME = ("S1", "S3", "S4")
X_DI = {"S1": (0.01, 0.3, 1.0), "S3": (1e-4, 0.1, 1.0), "S4": (0.01, 0.3, 1.0)}
S_LISTA = (0.85, 0.9, 0.95, 0.99, 1.0)
EPS_LISTA = (0.0, 0.5)
LATI = (32, 64)
N_LISTA = (1.0, 10.0, 100.0)
H = 1e-3                       # la differenza relativa in s
TOLL_DISTINTI = 1e-6
TOLL_STAZ = 1e-12
TOLL_UNO = 1e-9
TOLL_UNO_2 = 1e-6
EPS_REL = 1e-7
SOGLIA_STABILE = 1e-3 * 0.4018  # _lineare_s1_s4: 1e-3 del massimo di riferimento R2 (decisione delle 18:09)
S_CONTROLLO = 0.9              # c del ramo basso a eps 0, s 0.9: il controllo che puo' fallire
R_SIGMA, DR_SIGMA = 12.0, 1.0 / 40.0   # la griglia radiale in unita' di sigma_rif = sqrt(|c|/s); R tale che la coda gaussiana resti rappresentabile
MAX_IT = 20000
JSONL = os.path.join(RADICE, "doc", "referti_l2", "gravita_collettiva.jsonl")
NON_DEFINITI = set()
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


# =====================================================================================
#   GLI SPETTRI: ogni ramo massivo, raggruppato per (Dt, omega(0))
# =====================================================================================
_CACHE = {}


def spettro(s, eps):
    import _forza_da_cs as F
    if (s, eps) not in _CACHE:
        _CACHE[(s, eps)] = F.rami(s, eps)
    return _CACHE[(s, eps)]


def gruppi(lista):
    """### I rami raggruppati per le FASI PROPRIE `omega(0)` e `omega(k_1)` distinte entro `TOLL_DISTINTI`: una riga per gruppo, nel formato di `_forza_da_cs`.

    ### ⚠ **Non per il `Dt` del FIT** *(`d222af13`)*: ### **due copie degeneri hanno fasi proprie uguali, ma `Dt` del fit diversi fino a `~1e-6`** *(il rumore del fit)*."""
    out = []
    for r in sorted(lista, key=lambda r: (r["omega0"], r["omega1"])):
        for g in out:
            if abs(r["omega0"] - g[0]["omega0"]) <= TOLL_DISTINTI and abs(r["omega1"] - g[0]["omega1"]) <= TOLL_DISTINTI:
                g.append(r)
                break
        else:
            out.append([r])
    righe = []
    for g in out:
        righe.append({"omega0": g[0]["omega0"], "Dt": float(np.mean([r["Dt"] for r in g])), "v": float(np.mean([r["v"] for r in g])),
                      "segno": g[0]["segno"], "copie": len(g), "omega1": [r["omega1"] for r in g],
                      "nome": "Dt %.4f w0 %+.4f" % (g[0]["Dt"], g[0]["omega0"])})
    return righe


def ramo_a(s, eps, riga):
    """### La riga seguita a un altro `s` *(`_forza_da_cs.segui`)*, col suo gruppo e il suo spazio."""
    import _forza_da_cs as F
    lista, BB, _ = spettro(s, eps)
    r = F.segui(lista, riga)
    g = [x for x in gruppi(lista) if abs(x["omega0"] - r["omega0"]) <= TOLL_DISTINTI and r["omega1"] in x["omega1"]][0]
    return g, BB


# =====================================================================================
#   LIVELLO 1 -- LO STATO UNIFORME
# =====================================================================================
def scena(L, s, eps, e, x):
    import _stabilita_lineare as SL
    vero = SL.EPS_MONETA
    SL.EPS_MONETA = eps
    try:
        inc, mot, st, par = SL.scena(L, 1.0, SL.X)
    finally:
        SL.EPS_MONETA = vero
    n = inc.n
    mot.cs = np.full(n, float(s))
    mot.lambda_c = None
    st["psi_h"][...] = np.tile(e, n).reshape(st["psi_h"].shape)
    lam = float(np.mean(mot.densita_vuoto(st)))
    rho = float(np.mean(mot.densita_materia(st)))
    if x > 0.0:
        st["psi_h"] *= np.sqrt(x * lam / rho)
    else:
        st["psi_h"][...] = 0.0
    rho_v = mot.densita_materia(st)
    lam_v = mot.densita_vuoto(st)
    xr = float(np.max(np.abs(rho_v / lam_v - x)))
    return inc, mot, st, par, float(np.mean(rho_v)), float(np.mean(lam_v)), xr


def un_tick(forma, L, s, eps, e, x):
    """### Un tick del passo intero; `omega_tot` della materia e `omega_v` del vuoto, e lo scarto dalla stazionarieta' per settore."""
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    inc, mot, st, par, rho, lam, xr = scena(L, s, eps, e, x)
    p = SL.copia(st)
    with SF.forma(forma):
        SL.passo(p, mot, par, False, (), 0.0)
    out = {"rho0": rho, "Lambda0": lam, "x_scarto": xr}
    for k, nome in (("psi_h", "m"), ("phi_h", "v")):
        a, b = st[k].reshape(-1), p[k].reshape(-1)
        nn = np.vdot(a, a).real
        if nn == 0.0:
            out["omega_" + nome], out["staz_" + nome] = None, 0.0
            continue
        c = np.vdot(a, b) / nn
        out["omega_" + nome] = float(-np.angle(c))
        out["staz_" + nome] = float(np.linalg.norm(b - c * a) / np.sqrt(nn))
    return out, (inc, mot, st, par)


def stabilita(forma, L, s, scena_, om, ov):
    """### `gamma` per tempo proprio dalla Green di un tick nel riferimento che ruota: `R' = Phi^{-1} R`."""
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    _inc, mot, st, par = scena_
    scale = (float(np.max(np.abs(st["psi_h"]))) or 1.0, float(np.max(np.abs(st["phi_h"]))) or 1.0)
    with SF.forma(forma):
        R, _ = SL.green(st, mot, par, False, (), 0.0, L, scale, EPS_REL)
    nc = SL.NC
    P = np.zeros((2 * nc, 2 * nc))
    for c in range(nc):
        w = om if c < 8 else ov
        w = 0.0 if w is None else w
        P[c, c], P[c, c + nc], P[c + nc, c], P[c + nc, c + nc] = np.cos(w), -np.sin(w), np.sin(w), np.cos(w)
    lam = np.linalg.eigvals(np.matmul(P, R))
    lnm = np.log(np.max(np.abs(lam), axis=-1))
    i = np.unravel_index(int(np.argmax(lnm)), lnm.shape)
    g = float(lnm[i]) / s
    return {"gamma": g, "k_max": [int(i[0]), int(i[1])], "stabile": g < SOGLIA_STABILE}


def pendenza(fm, f0, fp, sm, s0, sp):
    """### `d ln |f| / d ln s`: centrata se ci sono tutti e due i vicini, all'indietro se no."""
    if fp is None:
        a, b, ta, tb = fm, f0, sm, s0
    else:
        a, b, ta, tb = fm, fp, sm, sp
    if a == 0.0 or b == 0.0:
        return None
    return float((np.log(abs(b)) - np.log(abs(a))) / (np.log(tb) - np.log(ta)))


def livello_1():
    import _forza_da_cs as F
    import _screening_forme_s3 as SF
    print("### LIVELLO 1 -- LO STATO UNIFORME (ogni ramo massivo; lati %s; x %s; s %s; eps %s)" % (LATI, X_DI, S_LISTA, EPS_LISTA))
    righe1, mf, dp = [], [], []
    for eps in EPS_LISTA:
        for s in S_LISTA:
            lista, BB, _ = spettro(s, eps)
            gg = gruppi(lista)
            if not gg:
                print("  eps %g s %g: NESSUN RAMO MASSIVO (il gap e' nullo)" % (eps, s))
                scrivi({"tipo": "livello1_vuoto", "eps": eps, "s": s})
                continue
            sm = s * (1.0 - H)
            sp = None if s >= 1.0 else s * (1.0 + H)
            for g in gg:
                # ### ⚠ **lo spazio del ramo puo' NON essere definito** *(il rango al primo `k` diverso dalle copie: al cono, `eps 0, s 1`, i `Dt`
                # ### sono `~1e-9`, rumore su un cono senza massa -- `d222af13`, la diagnosi corretta qui)*: ### **si scrive, non si misura.**
                try:
                    Q, _d0, _sv = F.spazio_del_ramo(BB, g)
                    gm, BBm = ramo_a(sm, eps, g)
                    Qm = F.spazio_del_ramo(BBm, gm)[0]
                    if sp is not None:
                        gp, BBp = ramo_a(sp, eps, g)
                        Qp = F.spazio_del_ramo(BBp, gp)[0]
                except AssertionError as err:
                    print("  eps %g s %g %-24s: RAMO NON DEFINITO (%s)" % (eps, s, g["nome"], str(err)[:110]))
                    scrivi({"tipo": "ramo_non_definito", "eps": eps, "s": s, "ramo": g["nome"], "Dt": g["Dt"], "perche": str(err)})
                    NON_DEFINITI.add((eps, s, g["nome"]))
                    continue
                # ---- il caso che deve fallire: la sola omega_ramo(0), rho0 = 0
                if eps == 0.0 and abs(g["omega0"]) > 1e-9 and sp is not None:
                    p_lin = pendenza(gm["omega0"], g["omega0"], gp["omega0"], sm, s, sp)
                    mf.append({"s": s, "ramo": g["nome"], "pendenza": p_lin})
                for forma in FORME:
                    for x in X_DI[forma]:
                        for L in LATI:
                            r0, sc0 = un_tick(forma, L, s, eps, Q[:, 0], x)
                            rm_, _ = un_tick(forma, L, sm, eps, Qm[:, 0], x)
                            rp_ = un_tick(forma, L, sp, eps, Qp[:, 0], x)[0] if sp is not None else None
                            pz = SF.pezzi_di(forma)

                            def assoluta(rr, ss, w0):
                                al = float(pz(np.array([rr["rho0"]]), np.array([rr["Lambda0"]]))[0][0])
                                nl_f = al * ss
                                nl = nl_f + F.avvolgi(rr["omega_m"] - w0 - nl_f)
                                return w0 + nl, nl, F.avvolgi(rr["omega_m"] - w0 - nl_f), al
                            w_tot, nl, scomp, al = assoluta(r0, s, g["omega0"])
                            w_m, nl_m, _, _ = assoluta(rm_, sm, gm["omega0"])
                            if rp_ is not None:
                                w_p, nl_p, _, _ = assoluta(rp_, sp, gp["omega0"])
                            else:
                                w_p = nl_p = None
                            p_tot = pendenza(w_m, w_tot, w_p, sm, s, sp)
                            p_nl = pendenza(nl_m, nl, nl_p, sm, s, sp)
                            stb = stabilita(forma, L, s, sc0, r0["omega_m"], r0["omega_v"])
                            rec = {"tipo": "livello1", "forma": forma, "eps": eps, "s": s, "x": x, "lato": L, "ramo": g["nome"],
                                   "omega_ramo0": g["omega0"], "Dt": g["Dt"], "segno_curv": g["segno"], "copie": g["copie"],
                                   "alpha": al, "omega_tot": w_tot, "omega_misurata": r0["omega_m"], "omega_vuoto": r0["omega_v"],
                                   "staz_materia": r0["staz_m"], "staz_vuoto": r0["staz_v"], "scomposizione": scomp,
                                   "x_scarto": r0["x_scarto"], "pendenza_tot": p_tot, "pendenza_nl": p_nl, **stb}
                            righe1.append(rec)
                            scrivi(rec)
                            if eps == 0.0 and abs(g["omega0"]) <= 1e-9 and sp is not None:
                                dp.append(rec)
                            print("  %-2s eps %-3g s %-4g x %-6g lato %d %-24s: w_tot %+.6f (w_ramo %+.6f + alpha s %+.6f) | staz %.1e/%.1e scomp %.1e |"
                                  " d ln w/d ln s %s (nl %s) | gamma %.2e %s"
                                  % (forma, eps, s, x, L, g["nome"], w_tot, g["omega0"], nl, r0["staz_m"], r0["staz_v"], abs(scomp),
                                     "--" if p_tot is None else "%+.6f" % p_tot, "--" if p_nl is None else "%+.9f" % p_nl,
                                     stb["gamma"], "STABILE" if stb["stabile"] else "instabile"))
                            sys.stdout.flush()
    return righe1, mf, dp


# =====================================================================================
#   LIVELLO 2 -- IL SOLITONE EFFICACE
# =====================================================================================
def solitone(forma, c, s, N, lam0):
    """### `mu u = -c lap u + s alpha(u^2) u`, radiale `2d`, norma `N`: il flusso di gradiente normalizzato implicito."""
    import _screening_forme_s3 as SF
    from scipy.linalg import solve_banded
    pz = SF.pezzi_di(forma)
    sg = 1.0 if c > 0 else -1.0
    ca = abs(c)
    sig = np.sqrt(ca / s)
    dr = DR_SIGMA * sig
    M = int(round(R_SIGMA / DR_SIGMA))
    r = (np.arange(M) + 0.5) * dr
    w = 2.0 * np.pi * r * dr
    rp, rm = r + 0.5 * dr, r - 0.5 * dr
    a_up = ca * rp / (r * dr * dr)
    a_dn = ca * rm / (r * dr * dr)
    a_dn[0] = 0.0
    diag_lap = a_up + a_dn                                    # -c lap u: diagonale + , fuori diagonale -
    u = np.exp(-r ** 2 / (2.0 * sig * sig))
    u *= np.sqrt(N / np.sum(w * u * u))
    tau = sig * sig / ca
    mu_v = None
    stato = "NON CONVERGE"
    for it in range(MAX_IT):
        rho = u * u
        V = sg * s * pz(rho, np.full_like(rho, lam0))[0]
        if not np.all(np.isfinite(V)):
            stato = "NON RAPPRESENTABILE (la coda sotto il doppio: alpha non finita)"
            break
        Hu = diag_lap * u - a_up * np.r_[u[1:], 0.0] - a_dn * np.r_[0.0, u[:-1]] + V * u
        mu = float(np.sum(w * u * Hu) / np.sum(w * u * u))
        Vs = V - float(np.min(V))
        ab = np.zeros((3, M))
        ab[0, 1:] = -tau * a_up[:-1]
        ab[1, :] = 1.0 + tau * (diag_lap + Vs)
        ab[2, :-1] = -tau * a_dn[1:]
        un = solve_banded((1, 1), ab, u)
        un *= np.sqrt(N / np.sum(w * un * un))
        du = float(np.sqrt(np.sum(w * (un - u) ** 2) / N))
        u = un
        if mu_v is not None and abs(mu - mu_v) < 1e-12 * max(1.0, abs(mu)) and du < 1e-10:
            stato = "CONVERGE"
            break
        mu_v = mu
    larg = float(np.sqrt(np.sum(w * r * r * u * u) / np.sum(w * u * u)))
    if larg > (M * dr) / 5.0:
        esiste = "DISPERSIONE"
    elif larg < 2.0 * dr:
        esiste = "COLLASSO"
    else:
        esiste = "LEGATO"
    return {"mu": sg * mu, "larghezza": larg, "rho_centro": float(u[0] ** 2), "x_centro": float(u[0] ** 2 / lam0), "stato": stato,
            "iterazioni": it + 1, "esiste": esiste, "inviluppo_lento": larg >= 2.0, "R": float(M * dr), "dr": dr}


def c_di(g):
    return g["segno"] * g["v"] ** 2 / g["Dt"] / 2.0


def gausson(c, s, N, lam0):
    """### La formula chiusa del logaritmo puro `alpha = ln(rho/Lambda) + 1` *(il limite `rho << Lambda` di `S3`)*, `c < 0`."""
    return s * (np.log(N * s / (np.pi * abs(c))) - 1.0 - np.log(lam0))


def livello_2(lam0):
    import _screening_forme_s3 as SF
    print("### LIVELLO 2 -- IL SOLITONE EFFICACE (N %s; griglia R = %g sigma, dr = %g sigma, sigma = sqrt(|c|/s))" % (N_LISTA, R_SIGMA, DR_SIGMA))
    # ---- il controllo del risolutore: il logaritmo puro contro la gaussiana esatta
    vero = SF.pezzi_di

    def log_puro(nome):
        def pz(rho, lam):
            rho = np.asarray(rho, dtype=float)
            al = np.zeros_like(rho)
            v = rho > 0.0
            al[v] = np.log(rho[v] / np.asarray(lam, dtype=float)[v]) + 1.0
            return al, np.zeros_like(rho)
        return pz
    SF.pezzi_di = log_puro
    try:
        rr = solitone("LOG", -0.8, 0.9, 10.0, lam0)
    finally:
        SF.pezzi_di = vero
    ge = gausson(-0.8, 0.9, 10.0, lam0)
    esito("DI SERVIZIO: il risolutore sul logaritmo puro = la gaussiana esatta (c -0.8, s 0.9, N 10), entro 1e-6 relativo",
          rr["stato"] == "CONVERGE" and abs(rr["mu"] - ge) < 1e-6 * abs(ge), "mu %.10f contro %.10f; larghezza %.5f contro %.5f"
          % (rr["mu"], ge, rr["larghezza"], np.sqrt(0.8 / 0.9)))
    righe2 = []
    for eps in EPS_LISTA:
        for s in S_LISTA:
            lista, _BB, _ = spettro(s, eps)
            sm = s * (1.0 - H)
            sp = None if s >= 1.0 else s * (1.0 + H)
            for g in gruppi(lista):
                if (eps, s, g["nome"]) in NON_DEFINITI:
                    continue
                gm = ramo_a(sm, eps, g)[0]
                gp = ramo_a(sp, eps, g)[0] if sp is not None else None
                for forma in FORME:
                    for N in N_LISTA:
                        r0 = solitone(forma, c_di(g), s, N, lam0)
                        rm_ = solitone(forma, c_di(gm), sm, N, lam0)
                        rp_ = solitone(forma, c_di(gp), sp, N, lam0) if gp is not None else None
                        w0 = g["omega0"] + r0["mu"]
                        wm = gm["omega0"] + rm_["mu"]
                        wp = gp["omega0"] + rp_["mu"] if rp_ is not None else None
                        ok = all(q is None or (q["stato"] == "CONVERGE" and q["esiste"] == "LEGATO") for q in (r0, rm_, rp_))
                        p = pendenza(wm, w0, wp, sm, s, sp) if ok else None
                        rec = {"tipo": "livello2", "forma": forma, "eps": eps, "s": s, "N": N, "ramo": g["nome"], "c": c_di(g),
                               "omega_ramo0": g["omega0"], "omega_sol": w0, "pendenza": p, **r0}
                        righe2.append(rec)
                        scrivi(rec)
                        print("  %-2s eps %-3g s %-4g N %-5g %-24s: c %+.4f | %s %s | mu %+.6f w_sol %+.6f larghezza %.3f x_centro %.3g%s | d ln w/d ln s %s"
                              % (forma, eps, s, N, g["nome"], c_di(g), r0["esiste"], r0["stato"], r0["mu"], w0, r0["larghezza"], r0["x_centro"],
                                 "" if r0["inviluppo_lento"] else " (L'INVILUPPO LENTO NON VALE)", "--" if p is None else "%+.6f" % p))
                        sys.stdout.flush()
    # ---- il controllo che puo' fallire: c costante, omega0 = 0
    l9 = spettro(S_CONTROLLO, 0.0)[0]
    basso = [g for g in gruppi(l9) if abs(g["omega0"]) <= 1e-9][0]
    cfix = c_di(basso)
    print("### IL CONTROLLO CHE PUO' FALLIRE: c costante %.6f (ramo basso, eps 0, s %g), omega0 = 0" % (cfix, S_CONTROLLO))
    ctr = []
    for forma in FORME:
        for N in N_LISTA:
            for s in S_LISTA:
                sm = s * (1.0 - H)
                sp = None if s >= 1.0 else s * (1.0 + H)
                q0, qm = solitone(forma, cfix, s, N, lam0), solitone(forma, cfix, sm, N, lam0)
                qp = solitone(forma, cfix, sp, N, lam0) if sp is not None else None
                ok = all(q is None or (q["stato"] == "CONVERGE" and q["esiste"] == "LEGATO") for q in (q0, qm, qp))
                p = pendenza(qm["mu"], q0["mu"], qp["mu"] if qp else None, sm, s, sp) if ok else None
                ctr.append({"forma": forma, "N": N, "s": s, "pendenza": p, "esiste": q0["esiste"], "mu": q0["mu"]})
                scrivi({"tipo": "controllo_c_costante", "forma": forma, "N": N, "s": s, "pendenza": p, **q0})
                print("  %-2s N %-5g s %-4g: %s mu %+.6f larghezza %.3f | d ln mu/d ln s %s" % (
                    forma, N, s, q0["esiste"], q0["mu"], q0["larghezza"], "--" if p is None else "%+.6f" % p))
    return righe2, ctr


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _universalita_massa as UM
    import composizione as CM
    print("=" * 100)
    print("LA GRAVITA' COLLETTIVA SULLA CARTA: la frequenza a riposo della materia legata al variare di s (S1, S3, S4)")
    print("=" * 100)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py", "csv/_universalita_massa.py", "csv/_forza_da_cs.py",
                                     "csv/_stabilita_lineare.py", "csv/_screening_forme_s3.py", "csv/_gravita_collettiva.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); dtau 1, cs = s per nodo in memoria, lambda_c None; i blob nel repo: %s"
          % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: FORME %s; X %s; S %s; EPS %s; LATI %s; N %s; H %g; TOLL_DISTINTI %g; TOLL_STAZ %g; TOLL_UNO %g; TOLL_UNO_2 %g;"
          " EPS_REL %g; SOGLIA_STABILE %g; S_CONTROLLO %g; R_SIGMA %g; DR_SIGMA %g; MAX_IT %d"
          % (FORME, X_DI, S_LISTA, EPS_LISTA, LATI, N_LISTA, H, TOLL_DISTINTI, TOLL_STAZ, TOLL_UNO, TOLL_UNO_2, EPS_REL, SOGLIA_STABILE,
             S_CONTROLLO, R_SIGMA, DR_SIGMA, MAX_IT))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        righe1, mf, dp = livello_1()
    lam0 = righe1[0]["Lambda0"]
    print("### I CONTROLLI DEL LIVELLO 1")
    peg = max(max(r["staz_materia"], r["staz_vuoto"]) for r in righe1)
    esito("DI SERVIZIO: la stazionarieta' per settore entro %g, su %d stati" % (TOLL_STAZ, len(righe1)), peg < TOLL_STAZ, "il peggiore %.2e" % peg)
    peg = max(abs(r["scomposizione"]) for r in righe1)
    esito("DI SERVIZIO: la scomposizione omega_tot = omega_ramo(0) + alpha s entro %g" % TOLL_STAZ, peg < TOLL_STAZ, "il peggiore %.2e" % peg)
    peg = max(r["x_scarto"] for r in righe1)
    esito("DI SERVIZIO: rho0/Lambda0 = x entro %g" % TOLL_STAZ, peg < TOLL_STAZ, "il peggiore %.2e" % peg)
    peg = max((abs(r["pendenza_nl"] - 1.0) for r in dp if r["pendenza_nl"] is not None), default=float("inf"))
    esito("DEVE PASSARE: eps 0 ramo basso, la pendenza della sola parte non lineare = 1 entro %g, su %d stati" % (TOLL_UNO, len(dp)),
          len(dp) > 0 and all(r["pendenza_nl"] is not None for r in dp) and peg < TOLL_UNO, "il peggiore |p - 1| %.2e" % peg)
    finite = all(m["pendenza"] is not None and np.isfinite(m["pendenza"]) for m in mf)
    tengono = [m for m in mf if m["pendenza"] is not None and abs(m["pendenza"] - 1.0) < TOLL_UNO]
    esito("DEVE FALLIRE: <<pendenza = 1>> sul ramo alto di eps 0 a rho0 = 0 (e per la chiave giusta: pendenze finite), su %d punti" % len(mf),
          finite and len(mf) > 0 and not tengono, "; ".join("s %g: %+.4f" % (m["s"], m["pendenza"]) for m in mf if m["pendenza"] is not None))
    print("### LO STATO PIU' BASSO A OGNI (forma, eps, s, x), lato %d" % LATI[0])
    for forma in FORME:
        for eps in EPS_LISTA:
            for s in S_LISTA:
                for x in X_DI[forma]:
                    rr = [r for r in righe1 if r["forma"] == forma and r["eps"] == eps and r["s"] == s and r["x"] == x and r["lato"] == LATI[0]]
                    if rr:
                        b = min(rr, key=lambda r: r["omega_tot"])
                        scrivi({"tipo": "piu_basso", "forma": forma, "eps": eps, "s": s, "x": x, "ramo": b["ramo"], "omega_tot": b["omega_tot"],
                                "stabile": b["stabile"], "gamma": b["gamma"]})
                        print("  %-2s eps %-3g s %-4g x %-6g: %-24s w_tot %+.6f, %s (gamma %.2e)" % (
                            forma, eps, s, x, b["ramo"], b["omega_tot"], "STABILE" if b["stabile"] else "instabile", b["gamma"]))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        righe2, ctr = livello_2(lam0)
    print("### IL CONTROLLO DEL LIVELLO 2")
    leg = [c for c in ctr if c["pendenza"] is not None]
    fuori = [c for c in leg if abs(c["pendenza"] - 1.0) >= TOLL_UNO_2]
    esito("PUO' FALLIRE: c costante e omega0 = 0, la pendenza di omega_sol = 1 entro %g, su %d punti legati" % (TOLL_UNO_2, len(leg)),
          len(leg) > 0 and not fuori, "; ".join("%s N %g s %g: %+.4f" % (c["forma"], c["N"], c["s"], c["pendenza"]) for c in fuori[:12]))
    print("=" * 100)
    print("LA GRAVITA' COLLETTIVA: %d su %d controlli   %s  (il verdetto di fisica e' la tabella delle pendenze)"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
