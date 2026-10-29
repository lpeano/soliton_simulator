# -*- coding: utf-8 -*-
r"""**LA STRADA (B): IL LATO `r > 1`, LA SPALLA DI `r 0.65`, LE CORSE ANCHE SENZA STATO FERMO ESATTO** *(UNA DIAGNOSI, NON UNA CURA; il mandato di Luca delle `22:25` del `2026-10-29`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-29_strada_b_lati.md`)*:
### **i pesi, la scena e Newton da `csv/_strada_b_r.py`** *(invariati)*; ### **i file di `r 1.5247` si chiamano `r1.52`** *(`_strada_b_r.nome_r`)*.

    python csv/_strada_b_lati.py --cerca 1.5247 > doc/referti_l2/strada_b/cerca_1.5247.txt
    python csv/_strada_b_lati.py --forma 0.69 > doc/referti_l2/strada_b/forma_0.69.txt     # idem 0.65, 1.5247
    python csv/_strada_b_lati.py --lunga                # un pezzo; si ripete fino alla fine
    python csv/_strada_b_lati.py --referto > doc/referti_l2/strada_b_lati.txt
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

import _strada_b_r as SB                                       # noqa: E402

R_ALTO = 1.5247                # ### la riga (B1) di b5fd8ecc
R_TUTTI = (0.65, 0.69, R_ALTO)
R_LUNGA = (R_ALTO, 0.69)       # ### l'ordine del mandato: la prima la cui forma non e' esponenziale
R_MAX = 24
SPALLA = (14, 17)              # ### la spalla di r 0.65 (Luca, dal referto di af1758fd)
K_S1 = (13, 16)                # ### (s1): un incrocio di c1 su P0 fra gli anelli k, k+1 con k in 13..16
T_FIS = 180.0
PASSO_FIS = 3.0
T_ISTANTI = (90.0, 180.0)
SATURAZIONE = 1e-2
FATTORE_DEROGA = 10.0          # ### la deroga di 6c720842: la finestra da 10 volte il residuo
TOLL_PIATTA = 1e-9
TOLL_NORMA = 1e-10
TOLL_RICOMPOSTO = 1e-10
T_MAX = 20000
PEZZO = 2000
OGNI = 10
FINESTRA = 500.0
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
    with open(fj, "xb") as fh:
        fh.write(dati)


def leggi(fj):
    return json.loads(io.open(fj, encoding="utf-8").read())


def stato(r):
    """### **Lo stato di Newton a `r`** *(fermo o no)*: `(psi, mu, json)`; ### **lo sha1 DEVE coincidere.**"""
    c = SB.carica(r)
    assert c is not None, "nessuna ricerca a r %r" % r
    assert c[3], "lo stato sul disco a r %r NON e' quello della ricerca (sha1)" % r
    return c[0], c[1], c[2]


def cerca(r):
    assert r == R_ALTO, "il mandato chiede Newton solo a r %g" % R_ALTO
    SB.cerca(r)


# ====================================================================== (1) IL CONTO PER ANELLO
def rayleigh(z, phi0, psi, forma, s, r):
    import _modo_al_variare_di_s as MS
    with SB.pesi(r):
        q = MS.tick(z, phi0, psi, forma)
    lam = complex(np.vdot(psi, q) / np.vdot(psi, psi))
    return -math.atan2(lam.imag, lam.real) / s


def anelli(z, psi, forma):
    import _energia_del_legame as EL
    import _screening_forme_s3 as SF
    z["st"]["psi_h"][...] = psi
    rho, lam = EL.densita(z["inc"], z["st"])
    al = SF.pezzi_di(forma)(rho, lam)[0]
    M = float(rho.sum())
    c = (rho @ z["pos"]) / M
    d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
    k = np.floor(d).astype(int)
    qn = np.maximum(np.bincount(k), 1)
    return np.bincount(k, weights=rho) / qn, np.bincount(k, weights=al) / qn


def incroci(v):
    return [k for k in range(len(v) - 1) if v[k] * v[k + 1] < 0.0]


def conto(etichetta, z, phi0, s, forma, r, psi, mu, P0, Ppi):
    ra, am = anelli(z, psi, forma)
    print("  [%s] r %.4f; mu %+.9f; P0 %+.6f, Ppi %+.6f per unita' di tempo" % (etichetta, r, mu, P0, Ppi))
    print("    anello: rho per nodo, alpha medio | c1 P0 + alpha - mu | c1 Ppi + alpha - mu | la coppia (P0 + alpha) + (Ppi + alpha) - 2 mu")
    tab = {"c1_P0": [], "c1_Ppi": [], "coppia": []}
    for k in range(R_MAX + 1):
        a = float(am[k])
        v = {"c1_P0": P0 + a - mu, "c1_Ppi": Ppi + a - mu, "coppia": P0 + Ppi + 2.0 * a - 2.0 * mu}
        for kk in tab:
            tab[kk].append(v[kk])
        print("    %2d: %12.5e  %.5f | %+.5f | %+.5f | %+.5f" % (k, ra[k], a, v["c1_P0"], v["c1_Ppi"], v["coppia"]))
    out = {}
    for kk in tab:
        out[kk] = incroci(tab[kk])
        print("    gli incroci %-7s %s" % (kk, ("fra gli anelli " + ", ".join("%d-%d" % (k, k + 1) for k in out[kk])) if out[kk] else "nessuno"))
    return out, ra


# ====================================================================== (3) LA FORMA DELLA CRESCITA
def forma(r):
    """### **`180` unita' di tempo dallo stato di Newton, fermo o no; `|D|/|psi0|` ogni `3`; le bande e gli anelli di `D` a `90` e `180`.**"""
    import _dove_va_la_materia as DV
    import _modo_al_variare_di_s as MS
    import _modo_instabile as MI
    fj = os.path.join(SB.DIR_JSON, "forma_%s.json" % SB.nome_r(r))
    assert not os.path.exists(fj), fj
    psi0, mu, cj = stato(r)
    print("  r %.4f: lo stato sha1 %s, residuo %.3e (%s), mu %+.9f" % (r, cj["sha"][:8], cj["residuo_finale"], "fermo" if cj["convergito"] else "NON fermo", mu))
    with SB.scena() as (_rec, z, phi0, _p, forma_, s), SB.pesi(r):
        A = DV.matrice(z, phi0, DV.AMP)
        _ph, Z = DV.autovettori(A)
        L = MS.L
        M0 = float(np.sum(np.abs(psi0) ** 2))
        n0 = math.sqrt(M0)
        ogni = int(round(PASSO_FIS / s))
        t_fine = int(round(T_FIS / s))
        ist = [int(round(x / s)) for x in T_ISTANTI]
        psi = psi0.copy()
        dn = 0.0
        ts, nD = [], []
        dove = {}
        s0 = time.time()
        for t in range(1, t_fine + 1):
            psi = MS.tick(z, phi0, psi, forma_)
            if t % ogni == 0:
                dn = max(dn, abs(float(np.sum(np.abs(psi) ** 2)) / M0 - 1.0))
                D = np.exp(1j * mu * s * t) * psi - psi0
                ts.append(t)
                nD.append(float(np.linalg.norm(D)) / n0)
                if t in ist:
                    v = MS.Vista(z, psi0)
                    dd = D / float(np.linalg.norm(D))
                    prd = np.bincount(MI.armoniche(v, MI.per_nodo(v, dd)[0])[1], weights=np.sum(np.abs(dd.reshape(v.n, 12)) ** 2, axis=1))
                    prd = prd / prd.sum()
                    Pk = DV.pesi(dd.reshape(v.n, 12), np.ones(v.n), Z, L)
                    tot = float(Pk.sum())
                    dove[str(t)] = {"anelli": [[int(k), float(prd[k])] for k in np.argsort(-prd)[:3]],
                                    "bande": [[g, float(Pk[:, :, list(idx)].sum()) / tot] for g, idx in DV.GRUPPI]}
        print("  r %.4f: %d tick in %.0f s; M entro %.1e" % (r, t_fine, time.time() - s0, dn))
    riga = {"r": r, "s": s, "sha": cj["sha"], "residuo": cj["residuo_finale"], "convergito": cj["convergito"], "mu": mu, "dn": dn, "t": ts, "nD": nD, "dove": dove}
    riga.update(giudica(riga))
    scrivi_nuovo(fj, riga)
    stampa_forma(riga)


def giudica(riga):
    """### **La forma, scritta prima** *(il task history, sez. 2)*: ### **(L) `|D| = c + v t` contro (E) `ln|D| = a + gamma t`, sui campioni sotto la saturazione, nello scarto di `ln(|D|/fit)`.**"""
    s = riga["s"]
    tau = np.array(riga["t"], dtype=float) * s
    nD = np.array(riga["nD"])
    m = nD < SATURAZIONE
    out = {"campioni": int(m.sum()), "attesa_v": riga["residuo"] / s}
    if m.sum() < 3:
        out.update({"forma": None})
        return out
    x, y = tau[m], nD[m]
    v, c = np.polyfit(x, y, 1)
    fL = c + v * x
    sL = float(np.sqrt(np.mean(np.log(y / fL) ** 2))) if np.all(fL > 0) else float("inf")
    g, a = np.polyfit(x, np.log(y), 1)
    sE = float(np.sqrt(np.mean((np.log(y) - (a + g * x)) ** 2)))
    out.update({"v": float(v), "c": float(c), "scarto_L": sL, "gamma": float(g), "a": float(a), "scarto_E": sE, "forma": "esponenziale" if sE < sL else "lineare"})
    basso = FATTORE_DEROGA * riga["residuo"]
    fin = [i for i in range(len(nD)) if basso < nD[i] < SATURAZIONE]
    out["finestra"] = [basso, SATURAZIONE, len(fin)]
    out["tasso"] = None
    if out["forma"] == "esponenziale" and len(fin) >= 3:
        i0, i1 = fin[0], fin[-1]
        out["tasso"] = float(np.polyfit(tau[i0:i1 + 1], np.log(nD[i0:i1 + 1]), 1)[0])
        out["finestra_tau"] = [float(tau[i0]), float(tau[i1])]
    return out


def stampa_forma(fr):
    s = fr["s"]
    tau = np.array(fr["t"], dtype=float) * s
    nD = np.array(fr["nD"])
    print("  r %.4f: lo stato %s (residuo %.3e); mu %+.9f; M entro %.1e" % (fr["r"], "fermo" if fr["convergito"] else "NON fermo", fr["residuo"], fr["mu"], fr["dn"]))
    print("    |D|/|psi0| ogni %g unita' di tempo da %g: %s" % (PASSO_FIS, tau[0], " ".join("%.2e" % x for x in nD)))
    loc = np.gradient(np.log(nD), tau)
    print("    d ln|D|/dt (accanto 1/t) a tempo 15, 30, 60, 90, 120, 150, 180: %s"
          % "  ".join("%.4f (%.4f)" % (loc[i], 1.0 / tau[i]) for i in [int(np.argmin(np.abs(tau - x))) for x in (15, 30, 60, 90, 120, 150, 180)]))
    if fr["forma"] is None:
        print("    LA FORMA: %d campioni sotto %.0e: non si giudica" % (fr["campioni"], SATURAZIONE))
    else:
        print("    sotto %.0e: %d campioni; (L) |D| = %.3e + %.3e t, scarto %.4f; (E) ln|D| = %.3f + %.5f t, scarto %.4f; la pendenza attesa residuo/s %.3e (v / attesa %.3f)"
              % (SATURAZIONE, fr["campioni"], fr["c"], fr["v"], fr["scarto_L"], fr["a"], fr["gamma"], fr["scarto_E"], fr["attesa_v"], fr["v"] / fr["attesa_v"]))
        print("    LA FORMA: %s" % fr["forma"].upper())
        if fr["forma"] == "esponenziale":
            if fr["tasso"] is None:
                print("    il tasso nella finestra (in deroga, fra %.1e e %.0e): %d campioni, non si misura" % tuple(fr["finestra"]))
            else:
                print("    il tasso nella finestra (in deroga, fra %.1e e %.0e; tempo %.0f .. %.0f, %d campioni): %.5f per unita' di tempo (dfb5ab7e a r 1: 0.15108)"
                      % (fr["finestra"][0], fr["finestra"][1], fr["finestra_tau"][0], fr["finestra_tau"][1], fr["finestra"][2], fr["tasso"]))
    for t in sorted(fr["dove"], key=int):
        d = fr["dove"][t]
        print("    D a tempo %.0f: gli anelli maggiori %s; le bande %s" % (int(t) * s, ", ".join("r %d %.3f" % (k, p) for k, p in d["anelli"]), "  ".join("%s %.3f" % (g, p) for g, p in d["bande"])))


# ====================================================================== (4) LA CORSA LUNGA
def scelta():
    """### **`r 1.5247` se la sua forma non e' esponenziale; altrimenti `r 0.69` se la sua non lo e'; altrimenti nessuna** *(il mandato)*."""
    for r in R_LUNGA:
        fj = os.path.join(SB.DIR_JSON, "forma_%s.json" % SB.nome_r(r))
        if not os.path.exists(fj):
            return None, "manca la forma a r %g" % r
        fr = leggi(fj)
        if fr["forma"] is not None and fr["forma"] != "esponenziale":
            return r, "la forma a r %g e' %s" % (r, fr["forma"])
    return None, "nessuna forma non esponenziale fra %s" % (R_LUNGA,)


def lunga():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    r, perche = scelta()
    assert r is not None, "la corsa lunga non parte: %s" % perche
    print("  la corsa lunga: r %.4f (%s)" % (r, perche))
    f_stato = os.path.join(SB.DIR_NPZ, "lunga_%s.npz" % SB.nome_r(r))
    with SB.scena() as (rec, z, phi0, _p, _forma, s), SB.pesi(r):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        t0 = 0
        punti = []
        if os.path.exists(f_stato):
            with np.load(f_stato) as dati:          # ### chiuso subito: su Windows un .npz aperto impedisce os.replace (il pezzo 02000, il mio errore)
                t0 = int(dati["t"])
                z["st"]["psi_h"][...] = dati["psi_h"]
            prec = leggi(os.path.join(SB.DIR_JSON, "lunga_%s_%05d.jsonl" % (SB.nome_r(r), t0 - PEZZO)))
            assert prec["sha_fine"] == SFM.sha(z["st"]["psi_h"]), "lo stato salvato NON e' quello della fine del pezzo prima"
        else:
            psi0, _mu, _cj = stato(r)
            z["st"]["psi_h"][...] = psi0
            p = CL.punto(z, 0, w_in, w0)
            p["tau"] = 0.0
            punti.append(p)
        if t0 >= T_MAX:
            print("  la corsa lunga %s: finita" % SB.nome_r(r))
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
        fp = os.path.join(SB.DIR_JSON, "lunga_%s_%05d.jsonl" % (SB.nome_r(r), t0))
        scrivi_nuovo(fp, riga)
        tmp = os.path.join(SB.DIR_NPZ, "lunga_%s_tmp.npz" % SB.nome_r(r))
        np.savez(tmp, psi_h=z["st"]["psi_h"], t=t1)
        os.replace(tmp, f_stato)
    print("  la corsa lunga %s: tick %d -> %d, w/w_in %.5f, cuore %.5f (%.0f s)" % (SB.nome_r(r), t0, t1, punti[-1]["w"] / w_in, punti[-1]["f_win"], riga["secondi"]))


# ====================================================================== IL REFERTO
def referto():
    import _bande_piatte as BP
    import _congelato_lungo as CL
    import _cuore_e_alone as CE
    import _deriva_congelato as DC
    import _modo_al_variare_di_s as MS
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    print("=" * 130)
    print("LA STRADA (B): IL LATO r > 1, LA SPALLA DI r 0.65, LE CORSE ANCHE SENZA STATO FERMO ESATTO (Luca 22:25; UNA DIAGNOSI); %s, L %d, eps 0, il congelato vero" % (SB.CASO, MS.L))
    print("=" * 130)
    print("  la configurazione: R_ALTO %g R_TUTTI %s R_LUNGA %s R_MAX %d SPALLA %s K_S1 %s T_FIS %g PASSO_FIS %g T_ISTANTI %s SATURAZIONE %g FATTORE_DEROGA %g TOLL_PIATTA %g TOLL_NORMA %g TOLL_RICOMPOSTO %g T_MAX %d PEZZO %d OGNI %d FINESTRA %g"
          % (R_ALTO, R_TUTTI, R_LUNGA, R_MAX, SPALLA, K_S1, T_FIS, PASSO_FIS, T_ISTANTI, SATURAZIONE, FATTORE_DEROGA, TOLL_PIATTA, TOLL_NORMA, TOLL_RICOMPOSTO, T_MAX, PEZZO, OGNI, FINESTRA))
    print("  da csv/_strada_b_r.py: i pesi in memoria (a_n = pi/sqrt(1 - r + r^2), b_a = r a_n), la scena, Newton (MAX_NEWTON %d, TOLL_RES %g); i file di r %g si chiamano %s" % (SB.MAX_NEWTON, SB.TOLL_RES, R_ALTO, SB.nome_r(R_ALTO)))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: a r 1.5247 (c1) nessuna crescita esponenziale e il cuore regge: (B) con r > 1 cura S1; (c2) nessuna esponenziale ma il cuore si svuota: un'altra causa;"
          " (c3) crescita esponenziale: lo scarto nel solitone non e' quello libero, o un'altra risonanza; (c4) altro. A r 0.65: (s1) la spalla e' la risonanza c1; (s2) no. A r 0.69: come c1-c4")
    with SB.scena() as (rec, z, phi0, p0, forma_, s):
        L = MS.L
        iK = (L // 3, L // 3)
        pz, mz, _cz, okz = MS.carica(SB.CASO)
        esito("DEVE PASSARE: lo stato fermo a r 1 = quello di dfb5ab7e (sha1)", okz, "")
        print("-" * 130)
        print("### (2a) IL TICK LIBERO A r %g, s %g" % (R_ALTO, s))
        P = {j: BP.pezzo(z, phi0, j, 0.0, "simm") for j in (BP.J_GROVER, BP.J_SPOST)}
        X_G, R_S = BP.generatori(P, s)
        _A1, E1, _a1, _b1 = SB.libero(z, phi0, s, 1.0)
        cur1 = E1[iK[0] + 1, iK[1]][4] + E1[iK[0] - 1, iK[1]][4] - 2.0 * E1[iK][4]
        lib = {}
        for r in (1.0,) + R_TUTTI:
            A, E, a, b = SB.libero(z, phi0, s, r)
            if r != 1.0:
                d = float(np.abs(BP.ricomposto(X_G, R_S, s, a, b) - A).max())
                esito("DEVE PASSARE: r %.4f, il tick coi pesi in memoria = il tick ricomposto dai generatori entro %g" % (r, TOLL_RICOMPOSTO), d < TOLL_RICOMPOSTO, "%.1e" % d)
            P0, Ppi, l0, lp = float(E[..., 6:10].mean()), float(E[..., 0:4].mean()), float(np.ptp(E[..., 6:10])), float(np.ptp(E[..., 0:4]))
            esito("DEVE PASSARE: r %.4f, le piatte piatte entro %g e uguali a (b_a - a_n)/2, -(a_n + b_a)/2 entro %g" % (r, TOLL_PIATTA, TOLL_PIATTA),
                  max(l0, lp, abs(P0 - (b - a) / 2.0), abs(Ppi + (a + b) / 2.0)) < TOLL_PIATTA, "larghezze %.1e %.1e; dalla formula %.1e %.1e" % (l0, lp, abs(P0 - (b - a) / 2.0), abs(Ppi + (a + b) / 2.0)))
            lib[r] = (P0, Ppi, a, b)
            cur = E[iK[0] + 1, iK[1]][4] + E[iK[0] - 1, iK[1]][4] - 2.0 * E[iK][4]
            print("  r %.4f: a_n %.6f b_a %.6f; P0 %+.6f, Ppi %+.6f; A(K) %+.6f; la coppia libera a K %+.5f; la curvatura di A a K %+.4e, rispetto a r 1 %.4f (a_n b_a/pi^2 %.4f)"
                  % (r, a, b, P0, Ppi, E[iK][4], BP.scarto_libero(E, iK), cur, cur / cur1, a * b / math.pi ** 2))
        print("-" * 130)
        print("### (1) IL CONTO c1 PER ANELLO (nessuna corsa): le frequenze per unita' di tempo; alpha dal profilo di ogni r")
        incr = {}
        prof = {}
        for r in R_TUTTI:
            P0, Ppi, _a, _b = lib[r]
            c = SB.carica(r)
            if r == R_ALTO:
                mu = rayleigh(z, phi0, pz, forma_, s, r)
                incr["r%.4f, il profilo di r 1" % r], prof["r 1 (dfb5ab7e)"] = conto("r %.4f, il profilo di r 1 (dfb5ab7e), mu di Rayleigh col tick di r %.4f" % (r, r), z, phi0, s, forma_, r, pz, mu, P0, Ppi)
                if c is not None:
                    esito("DEVE PASSARE: r %.4f, lo stato sul disco = la ricerca (sha1)" % r, c[3], "")
                    incr["r%.4f, il suo stato" % r], prof["r %.4f" % r] = conto("r %.4f, AGGIUNTO: lo stato di Newton del punto 2 (%s)" % (r, "fermo" if c[2]["convergito"] else "NON fermo"), z, phi0, s, forma_, r, c[0], c[1], P0, Ppi)
                continue
            assert c is not None, r
            esito("DEVE PASSARE: r %.4f, lo stato sul disco = la ricerca (sha1)" % r, c[3], "")
            incr["r%.4f" % r], prof["r %.4f" % r] = conto("r %.4f, lo stato di Newton (residuo %.3e, %s)" % (r, c[2]["residuo_finale"], "fermo" if c[2]["convergito"] else "NON fermo"), z, phi0, s, forma_, r, c[0], c[1], P0, Ppi)
        k65 = incr["r0.6500"]["c1_P0"]
        dentro = [k for k in k65 if K_S1[0] <= k <= K_S1[1]]
        print("  LA SPALLA DI r 0.65 (anelli %d-%d): gli incroci di c1 su P0 %s; (s1) se uno cade fra k, k+1 con k in %d..%d: %s"
              % (SPALLA[0], SPALLA[1], k65 or "nessuno", K_S1[0], K_S1[1], "(s1)" if dentro else "(s2)"))
        print("-" * 130)
        print("### (2b) LO STATO DI NEWTON A r %g" % R_ALTO)
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            z["st"]["psi_h"][...] = p0
            w_in = DC.forma(z, w0)[0]
        stati = [("r 1 (dfb5ab7e)", 1.0, pz, mz)]
        for r in R_TUTTI:
            c = SB.carica(r)
            if c is None:
                print("  r %.4f: NESSUNA RICERCA SUL DISCO" % r)
                continue
            cj = c[2]
            print("  r %.4f: Newton dallo stato a r 1: %d passi, residuo %.3e (%s), %.0f s; la storia del residuo: %s"
                  % (r, len(cj["storia"]) - 1, cj["residuo_finale"], "CONVERGE" if cj["convergito"] else "NON CONVERGE", cj["secondi"], " ".join("%.1e" % p["residuo"] for p in cj["storia"])))
            stati.append(("r %.4f" % r, r, c[0], c[1]))
        for nome_, r, psi, mu in stati:
            a, _b = SB.pesi_di(r)
            z["st"]["psi_h"][...] = psi
            pt = CL.punto(z, 0, w_in, w0)
            print("  %-16s mu %+.9f; lo scarto nel cuore 2 - a_n - 2 mu %+.5f; w/w_in %.5f, cuore f_win %.5f, entro 3 w0 %.5f, picco %.2f; 1 - |<a|b>|^2 da r 1 %.3e"
                  % (nome_, mu, 2.0 - a - 2.0 * mu, pt["w"] / w_in, pt["f_win"], pt["f_3w0"], pt["picco"], SFM.distanza(pz.ravel(), psi.ravel())))
        print("  il profilo per anelli (rho per nodo): " + "  ".join(prof))
        for k in range(R_MAX + 1):
            print("    %2d: %s" % (k, "  ".join("%12.5e" % prof[nm][k] for nm in prof)))
    print("-" * 130)
    print("### (3) LE CORSE BREVI (%g unita' di tempo), ANCHE DA STATI NON FERMI: LA FORMA DELLA CRESCITA" % T_FIS)
    for r in R_TUTTI:
        fj = os.path.join(SB.DIR_JSON, "forma_%s.json" % SB.nome_r(r))
        if not os.path.exists(fj):
            print("  r %.4f: nessuna corsa breve" % r)
            continue
        fr = leggi(fj)
        esito("DEVE PASSARE: r %.4f, M conservata entro %g nella corsa breve" % (r, TOLL_NORMA), fr["dn"] < TOLL_NORMA, "%.1e" % fr["dn"])
        stampa_forma(fr)
    print("-" * 130)
    print("### (4) LA CORSA LUNGA")
    r, perche = scelta()
    print("  la scelta: %s (%s)" % (("r %.4f" % r) if r is not None else "nessuna", perche))
    rif = []
    for n in sorted(os.listdir(SFM.PUNTI)):
        if n.startswith("corsa_L81_") and n.endswith(".jsonl"):
            rif.append(leggi(os.path.join(SFM.PUNTI, n)))
    rp_t = np.array([p["t"] * SFM.S for rr in rif for p in rr["punti"]])
    rp_c = np.array([p["f_win"] for rr in rif for p in rr["punti"]])

    def rif_cuore(x):
        i = int(np.argmin(np.abs(rp_t - x)))
        return "%.5f (tau %.0f)" % (rp_c[i], rp_t[i])
    righe = []
    for rr in R_LUNGA:
        for n in sorted(os.listdir(SB.DIR_JSON)):
            if n.startswith("lunga_%s_" % SB.nome_r(rr)) and n.endswith(".jsonl"):
                righe.append(leggi(os.path.join(SB.DIR_JSON, n)))
    if not righe:
        print("  nessuna corsa lunga")
    else:
        assert len(set(x["r"] for x in righe)) == 1 and righe[0]["r"] == r, "la corsa sul disco non e' quella della scelta"
        righe.sort(key=lambda x: x["t0"])
        for x, y in zip(righe, righe[1:]):
            assert x["t1"] == y["t0"], ("un buco fra i pezzi", x["t1"], y["t0"])
        pts = [p for x in righe for p in x["punti"]]
        print("  r %.4f: %d pezzi, tick %d -> %d%s" % (r, len(righe), righe[0]["t0"], righe[-1]["t1"], "" if righe[-1]["t1"] == T_MAX else " (NON FINITA)"))
        dM = max(abs(p["M"] - pts[0]["M"]) / pts[0]["M"] for p in pts)
        esito("DEVE PASSARE: r %.4f, M entro %g relativo nella corsa lunga" % (r, TOLL_NORMA), dM <= TOLL_NORMA, "%.1e" % dM)
        w_in = righe[0]["w_in"]
        tau = np.array([p["tau"] for p in pts])
        q = np.array([p["w"] / w_in for p in pts])
        cu = np.array([p["f_win"] for p in pts])
        al = np.array([1.0 - p["f_3w0"] for p in pts])
        pk = np.array([p["picco"] / pts[0]["picco"] for p in pts])
        a0 = 0.0
        while a0 < tau[-1] - 1e-9:
            m = (tau >= a0 - 1e-9) & (tau <= a0 + FINESTRA + 1e-9)
            print("  r %.4f, tau [%6.0f, %6.0f]: w/w_in da %.5f a %.5f (pendenza %+.3e); cuore da %.5f a %.5f (pendenza %+.3e); alone da %.5f a %.5f; picco relativo medio %.5f | r 1 (26300537, s 0.3): cuore da %s a %s"
                  % (r, a0, a0 + FINESTRA, q[m][0], q[m][-1], np.polyfit(tau[m], q[m], 1)[0], cu[m][0], cu[m][-1], np.polyfit(tau[m], cu[m], 1)[0], al[m][0], al[m][-1], pk[m].mean(),
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
        elif argv[:1] == ["--lunga"] and len(argv) == 1:
            lunga()
        elif argv[:1] in (["--cerca"], ["--forma"]) and len(argv) == 2:
            r = float(argv[1])
            assert r in R_TUTTI, "r %r non e' nel mandato %s" % (r, R_TUTTI)
            {"--cerca": cerca, "--forma": forma}[argv[0]](r)
        else:
            raise SystemExit(__doc__)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
