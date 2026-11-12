# -*- coding: utf-8 -*-
r"""**B1 RIDISEGNATO: PERCHE' `cs` MIN SCENDE SUL TORO PURO** *(sul ramo laterale; Luca `2026-11-10` `13:42`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `27.4`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/b1_profilo.py --corsa i  > doc/referti_l2/b1_i_profilo.txt
    python csv/solitone/b1_profilo.py --corsa iv > doc/referti_l2/b1_iv_rampa.txt
    python csv/solitone/b1_profilo.py --corsa ii > doc/referti_l2/b1_ii_t0.txt

**F1 di T2** *(il rilassamento esatto, `r = 1 - e^{-omega_v}`, (q2); le funzioni di `carta_f1` e `carta_f1_lunga`, importate)*, **il bordo SPENTO** *(il solo `TK.percorri_tick`, come T2)*. **Ogni `50` tick il profilo per anelli** *(`campo.anelli` dal centro
di `rho` alla partenza)*: **`cs` min, `cs` medio, `Lambda` medio;** **`cs` min col raggio.** **Il fronte** *(l'anello del minimo del profilo di `cs` MIN, sez. `27.4.6`)*, **il fit lineare sul tratto in moto, le letture.** **Le velocita' di confronto** *(sez. `27.4.1`)*:
**la risposta lineare del tick intero attorno a `psi = 0`, `phi = F3`** *(differenze SIMMETRICHE, `a = 1e-6`: l'errore quadratico si cancella)*, **`A(k)`, le velocita' di gruppo per Hellmann-Feynman, il cono.**
**(i)** `TBS` a `10000`, F1 tutto insieme *(T2 col profilo; F1-V; (i-B) al bit contro il codice di T2; (i-F) deve fallire)*. **(iv)** la rampa `lambda_k = sin^2(pi k / 2K)`, `K = 1000`, sul valore verso cui F1 rilassa *((iv-B) `K = 1` contro il codice di T2)*.
**(ii)** `TBS` a `t 0` *(mai assorbita)*, F1 tutto insieme.
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_f1 as F1  # noqa: E402
from solitone import carta_f1_lunga as F1L  # noqa: E402
from solitone import carta_punto_fisso as CPF  # noqa: E402

N_TICK = 5000                  # ### sez. 27.4.3 (Luca: 5000 tick)
N_RIPIEGO = 3000               # ### il tetto di 60 minuti, come T2
TETTO_S = 3600.0               # ### Luca: 60 minuti
OGNI_P = 50                    # ### Luca: il profilo ogni 50 tick
TICK_B = (100, 1000)           # ### Luca: (i-B), (iv-B) ai tick 100 e 1000
DIST = 1e-12                   # ### Luca: (i-F), cs disturbato di 1e-12 su un nodo
K_RAMPA = 1000                 # ### Luca: (iv), K = 1000 tick
A_IMP = 1e-6                   # ### sez. 27.4.1: l'ampiezza dell'impulso
TOLL_LIN = 1e-6                # ### sez. 27.4.1: la linearita' complessa
FATT_V = 0.2                   # ### Luca (f1): entro il 20%
RMS_1, RMS_2, IND_1, IND_2, MIN_CAMP = 1.0, 2.0, 1.0, 2.0, 3   # ### sez. 27.4.2 (mie, in anelli)
P_H1, P_H2, P_Q1, CSMIN_Q1, P_Q2 = -0.2, -0.05, -0.05, 1e-3, 0.3   # ### Luca: (h1), (h2), (q1), (q2)
CORSE = {"i": "b1_i_profilo.txt", "iv": "b1_iv_rampa.txt", "ii": "b1_ii_t0.txt"}
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def bersaglio(L, s, k, K):
    """### **Il valore verso cui F1 rilassa al tick `k`:** `L` stesso per `k >= K` *(F1 pieno, AL BIT)*, `s + lambda_k (L - s)` nella rampa."""
    from solitone import accensione as AC
    if k >= K:
        return L
    return s + AC.lam_di(k, K) * (L - s)


def corsa(st, mot, par, lc, cs0, n_tick, rr, kan, nk, s, K, tieni=()):
    """### **Il ciclo di `carta_f1_lunga.corsa`** *(lo stesso ordine delle operazioni)* **con la rampa** `bersaglio(L, s, k + 1, K)` **e il profilo ogni `OGNI_P` tick.** `tieni`: i tick a cui si tiene `cs` intero."""
    import composizione as CM
    import energia_pesata as EP
    import flussi_parziali as FP
    import tick as TK
    fp = np.zeros(mot.inc.n)
    cs = cs0.copy()
    calore = 0.0
    camp, presi, lam_m = [], {}, []
    pmin, pmed, plam = [], [], []
    cnt = np.bincount(kan, minlength=nk).astype(float)
    with F1.cs_primo_zero(True):
        for k in range(1, n_tick + 1):
            phi0 = st["phi_h"].copy()
            mot.cs = cs.copy()
            mot.lambda_c = float(lc)
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            r = 1.0 - np.exp(-F1.omega_v(phi0, st["phi_h"], mot.inc.nodo, mot.inc.n))
            lam = mot.densita_vuoto(st)
            L = FP.cs(lam, lc, fp).copy()
            g0 = EP.g_pesata(mot, st, par)
            cs1 = F1.rilassa(cs, bersaglio(L, s, k + 1, K), r)
            mot.cs = cs1.copy()
            g1 = EP.g_pesata(mot, st, par)
            calore += float(g1 - g0)
            cs = cs1
            i = int(np.argmin(cs))
            if cs[i] <= 0.0:
                raise F1L.Muro("tick %d: cs min %.3e <= 0 al nodo %d, il raggio %.2f, Lambda locale %.6f" % (k, float(cs[i]), i, float(rr[i]), float(lam[i])))
            lam_m.append(float(lam.mean()))
            if k in tieni:
                presi[k] = cs.copy()
            if k % OGNI_P == 0:
                mn = np.full(nk, np.inf)
                np.minimum.at(mn, kan, cs)
                md = np.where(cnt > 0, np.bincount(kan, weights=cs, minlength=nk) / np.maximum(cnt, 1.0), np.nan)
                pmin.append(mn)
                pmed.append(md)
                plam.append(np.where(cnt > 0, np.bincount(kan, weights=lam, minlength=nk) / np.maximum(cnt, 1.0), np.nan))
                camp.append({"t": k, "cs_min": float(cs[i]), "raggio": float(rr[i]), "r_f": int(np.argmin(mn)), "r_med": int(np.nanargmin(md)),
                             "r_max": float(r.max()), "norma": float(np.sum(np.abs(st["psi_h"]) ** 2)), "calore": calore, "cs_media": float(cs.mean())})
    return {"camp": camp, "presi": presi, "lam_media": np.array(lam_m), "pmin": np.array(pmin), "pmed": np.array(pmed), "plam": np.array(plam), "cnt": cnt}


def velocita(z, phi_v, cs_v, lc):
    """### **Sez. `27.4.1`:** la risposta lineare del tick intero *(F1, (q2), `cs = cs_v`)* attorno a `psi = 0`, `phi = phi_v`; `A(k)`; Hellmann-Feynman; il cono. ### **Lo stato di `z` si rimette.**"""
    import composizione as CM
    import tick as TK
    from scipy.linalg import eig
    from solitone import toro as TO
    st, mot, par, inc, Lt = z["st"], z["mot"], z["par"], z["inc"], z["L"]
    n = inc.n
    # ### la cella (come DV.matrice): i 3 archi che partono dal nodo x, le loro 6 estremita' (2 per arco, una in x e una in un vicino)
    assert inc.nodo.size == 6 * n and np.array_equal(inc.nodo[0::2], np.repeat(np.arange(n), 3)), "gli archi NON sono 3 per nodo, in ordine di nodo"
    npsi, nphi = st["psi_h"].size // n, st["phi_h"].size // n
    nc = npsi + nphi
    chiavi = [k for k, v in st.items() if isinstance(v, np.ndarray)]
    salvato = {k: st[k].copy() for k in chiavi}
    base_psi = np.zeros(st["psi_h"].shape, dtype=st["psi_h"].dtype)

    def un(dv):
        for kk in chiavi:
            st[kk][...] = salvato[kk]
        st["psi_h"][...] = base_psi
        st["phi_h"][...] = phi_v
        v = np.concatenate([st["psi_h"].reshape(n, npsi), st["phi_h"].reshape(n, nphi)], axis=1)
        v[0] += dv
        st["psi_h"][...] = v[:, :npsi].reshape(st["psi_h"].shape)
        st["phi_h"][...] = v[:, npsi:].reshape(st["phi_h"].shape)
        mot.cs = cs_v.copy()
        mot.lambda_c = float(lc)
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
        return np.concatenate([st["psi_h"].reshape(n, npsi), st["phi_h"].reshape(n, nphi)], axis=1).copy()

    try:
        with F1.cs_primo_zero(True):
            R = np.empty((n, nc, nc), dtype=complex)
            dev2, devi = 0.0, 0.0
            for c in range(nc):
                e = np.zeros(nc, dtype=complex)
                e[c] = 1.0
                r1 = (un(A_IMP * e) - un(-A_IMP * e)) / (2.0 * A_IMP)
                r2 = (un(2 * A_IMP * e) - un(-2 * A_IMP * e)) / (4.0 * A_IMP)
                ri = (un(1j * A_IMP * e) - un(-1j * A_IMP * e)) / (2j * A_IMP)
                sc = max(float(np.max(np.abs(r1))), 1e-300)
                dev2 = max(dev2, float(np.max(np.abs(r2 - r1))) / sc)
                devi = max(devi, float(np.max(np.abs(ri - r1))) / sc)
                R[:, :, c] = r1
    finally:
        for kk in chiavi:
            st[kk][...] = salvato[kk]
    vv = np.arange(n)
    d = TO.scarti(vv // Lt, vv % Lt, 0.0, 0.0, Lt)
    dist = np.hypot(d[:, 0], d[:, 1])
    sup = np.flatnonzero(np.any(np.abs(R) > 0.0, axis=(1, 2)))
    # ### il cono sui NODI VERI: l'estremita' di ogni componente (psi: (n, 12) -> estremita' 6x + j // 2; phi: (n, 6) -> 6x + j)
    est = np.concatenate([np.arange(npsi) // (npsi // 6), np.arange(nphi) // (nphi // 6)])
    cono = 0.0
    for c in range(nc):
        u = int(inc.nodo[est[c]])
        xs_, js_ = np.nonzero(np.abs(R[:, :, c]) > 0.0)
        w_ = inc.nodo[6 * xs_ + est[js_]]
        dd = TO.scarti(w_ // Lt, w_ % Lt, float(u // Lt), float(u % Lt), Lt)
        cono = max(cono, float(np.max(np.hypot(dd[:, 0], dd[:, 1]))))
    print("  LA RISPOSTA LINEARE (a %g, differenze simmetriche): %d componenti per nodo (%d di psi, %d di phi); la linearita' |R(2a) - R(a)| / max|R| %.2e, la linearita' complessa |R(ia)/i - R(a)| / max|R| %.2e (la soglia %g)"
          % (A_IMP, nc, npsi, nphi, dev2, devi, TOLL_LIN))
    print("  IL CONO: la distanza piu' grande dal nodo dell'impulso con R != 0: %.6f nodi per tick (%d nodi nel supporto)" % (cono, len(sup)))
    A1, A2 = TO.vettori()
    B = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
    Rs, ds = R[sup], d[sup]
    vmax = {"psi": (0.0, None), "phi": (0.0, None)}
    um = 0.0
    for m1 in range(Lt):
        for m2 in range(Lt):
            kv = (m1 * B[0] + m2 * B[1]) / Lt
            ph = np.exp(-1j * (ds @ kv))
            A = np.einsum("x,xij->ij", ph, Rs)
            dA = [np.einsum("x,xij->ij", -1j * ds[:, j] * ph, Rs) for j in (0, 1)]
            w, vl, vr = eig(A, left=True, right=True)
            um = max(um, float(np.max(np.abs(np.abs(w) - 1.0))))
            for b in range(nc):
                den = np.vdot(vl[:, b], vr[:, b])
                dl = [np.vdot(vl[:, b], dA[j] @ vr[:, b]) / den for j in (0, 1)]
                vg = np.array([-(dl[j] / w[b]).imag for j in (0, 1)])
                mod = float(np.hypot(*vg))
                chi = "psi" if float(np.sum(np.abs(vr[:npsi, b]) ** 2)) > 0.5 * float(np.sum(np.abs(vr[:, b]) ** 2)) else "phi"
                if mod > vmax[chi][0]:
                    vmax[chi] = (mod, (m1, m2, b))
    print("  A(k) unitaria: max ||lambda| - 1| %.2e" % um)
    lin = devi <= TOLL_LIN
    for chi in ("psi", "phi"):
        print("  LA VELOCITA' DI GRUPPO PIU' GRANDE delle bande di %s: %.6f nodi per tick (k della griglia %s, la banda %s)%s"
              % (chi, vmax[chi][0], vmax[chi][1][:2] if vmax[chi][1] else "-", vmax[chi][1][2] if vmax[chi][1] else "-", "" if lin else "  ### NON LEGGIBILE: la risposta NON e' lineare in senso complesso"))
    return {"cono": cono, "v_psi": vmax["psi"][0] if lin else None, "v_phi": vmax["phi"][0] if lin else None}


def fronte(camp, vel):
    """### **Sez. `27.4.2`:** il tratto in moto di `r_f`, il fit lineare, la lettura (f1)/(f2)."""
    tt = np.array([c["t"] for c in camp], float)
    rf = np.array([c["r_f"] for c in camp], float)
    j = int(np.argmax(rf))
    rm = np.array([c["r_med"] for c in camp], float)
    print("  IL FRONTE: r_f (l'anello del minimo del profilo di cs MIN, sez. 27.4.6) ai tick 50, 100, 200, 500, 1000, 2000, 5000: %s; il massimo %d al tick %d; (accanto: l'anello col cs MEDIO piu' basso: %s)"
          % (", ".join("%d" % rf[np.searchsorted(tt, t)] for t in (50, 100, 200, 500, 1000, 2000, 5000) if t <= tt[-1]), int(rf[j]), int(tt[j]),
             ", ".join("%d" % rm[np.searchsorted(tt, t)] for t in (50, 100, 200, 500, 1000, 2000, 5000) if t <= tt[-1])))
    if j + 1 < MIN_CAMP:
        print("  LA LETTURA: (f2) niente fronte: il tratto in moto ha %d campioni (meno di %d): il minimo non viaggia" % (j + 1, MIN_CAMP))
        return "f2"
    x, y = tt[:j + 1], rf[:j + 1]
    p, cov = np.polyfit(x, y, 1, cov=True)
    res = y - np.polyval(p, x)
    rms = float(np.sqrt(np.mean(res ** 2)))
    ind = float(max(0.0, -np.min(np.diff(y))))
    vf, ev = float(p[0]), float(math.sqrt(cov[0, 0]))
    print("  IL TRATTO IN MOTO: dal tick %d al %d (%d campioni); v_f %.5f +- %.5f nodi per tick; il RMS dei residui %.3f anelli; il passo all'indietro piu' grande %.0f anelli" % (x[0], x[-1], len(x), vf, ev, rms, ind))
    vicine = []
    for nome, v in (("il cono", vel["cono"]), ("v_g della materia (psi)", vel["v_psi"]), ("v_g del vuoto (phi)", vel["v_phi"]), ("v_max della materia a cs spento (bordo_riflessione, 0.58795 x s)", vel.get("cs_spento"))):
        if v:
            print("    contro %s %.5f: il rapporto %.4f" % (nome, v, vf / v))
            if abs(vf / v - 1.0) <= FATT_V:
                vicine.append(nome)
    if rms > RMS_2 or ind > IND_2:
        print("  LA LETTURA: (f2) niente fronte: il RMS %.3f o il passo all'indietro %.0f oltre %g anelli (salti)" % (rms, ind, RMS_2))
        return "f2"
    if rms <= RMS_1 and ind <= IND_1 and vicine:
        print("  LA LETTURA: (f1) c'e' un fronte: v_f %.5f entro il %d%% di %s" % (vf, int(100 * FATT_V), ", ".join(vicine)))
        return "f1"
    print("  LA LETTURA: caso intermedio: il RMS %.3f, il passo all'indietro %.0f, v_f %.5f %s" % (rms, ind, vf, "entro il 20%% di %s" % ", ".join(vicine) if vicine else "lontana da tutte le velocita'"))
    return "mezzo"


def stampa(ris, n, nk):
    print("    %7s %10s %8s %7s %5s %10s %24s %16s" % ("tick", "cs min", "raggio", "r_f", "r_med", "r max", "la norma", "il calore"))
    for c in ris["camp"]:
        print("    %7d %10.6f %8.2f %7d %5d %10.4f %24.12f %+16.6e" % (c["t"], c["cs_min"], c["raggio"], c["r_f"], c["r_med"], c["r_max"], c["norma"], c["calore"]))
    print("  I NODI PER ANELLO: %s" % " ".join("%d" % x for x in ris["cnt"]))
    for nome, chiave, fmt in (("cs MIN", "pmin", "%9.2e"), ("cs MEDIO", "pmed", "%9.2e"), ("Lambda MEDIO", "plam", "%9.5f")):
        print("  IL PROFILO, %s per anello (le colonne: gli anelli 0 .. %d; le righe: il tick)" % (nome, nk - 1))
        for c, row in zip(ris["camp"], ris[chiave]):
            print("    %5d %s" % (c["t"], " ".join(fmt % x for x in row)))
    sys.stdout.flush()


def pendenza3(ris, n):
    u3 = F1L.ultimo_terzo(ris["camp"], n)
    return 1000.0 * F1L.pendenza([c["t"] for c in u3], [math.log(c["cs_min"]) for c in u3])


def righe_t2():
    """### **Le righe della base di T2** *(il referto `carta_f1_lunga.txt`)*: `{tick: (cs min, raggio)}` come stringhe."""
    out, dentro = {}, False
    with open(os.path.join(solitone.RADICE, "doc", "referti_l2", "carta_f1_lunga.txt"), encoding="utf-8") as f:
        for l in f:
            if l.startswith("### la corsa BASE"):
                dentro = True
            elif l.startswith("### la corsa perturbata"):
                break
            elif dentro:
                p = l.split()
                if len(p) == 7 and p[0].isdigit() and p[1] == "-":
                    out[int(p[0])] = (p[2], p[3])
    return out


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import flussi_parziali as FP
    from solitone import campo as CP
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    quale = sys.argv[sys.argv.index("--corsa") + 1]
    assert quale in CORSE, "--corsa i | iv | ii"
    for m in ("__init__", "corsa_accensione", "toro", "campo", "accensione", "carta_punto_fisso", "carta_f1", "carta_f1_lunga"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0, _camp = CA.serie(CPF.CORSA)[:2]
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    t00 = time.time()
    print("=" * 130)
    print("B1 (sez. 27.4), LA CORSA (%s): %s; F1 (q2), il bordo SPENTO; %d tick; il profilo ogni %d tick" % (quale, {"i": "TBS a 10000, F1 tutto insieme", "iv": "TBS a 10000, la rampa K %d" % K_RAMPA, "ii": "TBS a t 0, F1 tutto insieme"}[quale], N_TICK, OGNI_P))
    print("=" * 130)
    n = N_TICK
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CPF.CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lam0 = mot.densita_vuoto(st).copy()
        lc = float(np.mean(lam0)) * (1.0 - s) / s
        print("### Lambda_c = %.12f; Lambda del vuoto %.17g; s %g" % (lc, float(lam0.mean()), s))
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            cs_v = FP.cs(lam0, lc, np.zeros(inc.n)).copy()
            t1 = time.time()
            vel = velocita(z, phi_v, cs_v, lc)
            print("    %.0f s" % (time.time() - t1))
            print("  v_max della materia a cs spento (bordo_riflessione.txt, banda B): 0.58795 per unita' di tempo, %.5f nodi per tick a s %g" % (0.58795 * s, s))
            vel_vec = dict(vel)
            vel_vec["cs_spento"] = 0.58795 * s
            if quale == "i":
                st["psi_h"][...] = 0.0
                st["phi_h"][...] = phi_v
                tempo = []
                prova = F1L.corsa(st, mot, par, lc, cs_v, F1L.N_STIMA, np.zeros(inc.n), tempo=tempo)
                del prova
                proiez = tempo[0] * (N_TICK + 1000 + 1000 + N_TICK)
                if proiez > TETTO_S:
                    n = N_RIPIEGO
                print("### il costo: %.4f s per tick; la proiezione delle quattro corse di (i): %.0f s: %s" % (tempo[0], proiez, "SOTTO il tetto, %d tick" % n if n == N_TICK else "### SOPRA il tetto: %d tick (dichiarato)" % n))
                st["psi_h"][...] = 0.0
                st["phi_h"][...] = phi_v
                vv = F1L.corsa(st, mot, par, lc, cs_v, n, np.zeros(inc.n))
                dcs_dl = lc / (float(lam0.mean()) + lc) ** 2
                print("  F1-V, LA LETTURA (Luca): dcs/dLambda = %.6e" % dcs_dl)
                tv = {c["t"]: c for c in vv["camp"]}
                for t in F1L.TICK_V + (n,):
                    dl = float(vv["lam_media"][t - 1] - lam0.mean())
                    att = dcs_dl * dl
                    mis = tv[t]["cs_media"] - float(cs_v.mean())
                    dentro = att != 0.0 and mis * att > 0 and 0.5 <= mis / att <= 2.0
                    print("    tick %5d: la deriva di Lambda %+.4e; di cs misurata %+.4e, attesa %+.4e; il rapporto %s: %s" % (t, dl, mis, att, "%.4f" % (mis / att) if att else "-", "ENTRO un fattore 2" if dentro else "### FUORI"))
        xs = stati[0 if quale == "ii" else CPF.TICK_D4]
        print("### la partenza: %s (t %d)" % (os.path.basename(xs["file"]), xs["t"]))

        def carica():
            with np.load(xs["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"
        carica()
        rho = np.zeros(inc.n)
        np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        nodi = np.arange(inc.n)
        Lt = z["L"]
        c1, c2 = TO.centro(rho, nodi // Lt, nodi % Lt, Lt)[:2]
        pos = TO.scarti(nodi // Lt, nodi % Lt, c1, c2, Lt)
        rr = np.hypot(pos[:, 0], pos[:, 1])
        kan, ra = CP.anelli(nodi // Lt, nodi % Lt, c1, c2, Lt, float("inf"))
        nk = int(kan.max()) + 1
        ic = int(np.argmin(rr))
        print("### il centro di rho (%.5f, %.5f); %d anelli; lo scarto massimo fra il raggio di T2 (hypot di scarti) e quello di campo.anelli: %.3e; il nodo del centro %d (r %.4f)"
              % (c1, c2, nk, float(np.max(np.abs(rr - ra))), ic, rr[ic]))
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            L0 = FP.cs(mot.densita_vuoto(st), lc, np.zeros(inc.n)).copy()
            if quale in ("i", "iv"):
                riga = righe_t2()
                carica()
                t1 = time.time()
                ref = F1L.corsa(st, mot, par, lc, L0, max(TICK_B), rr, tieni=True)
                print("### il riferimento: il codice di T2 (carta_f1_lunga.corsa), %d tick: %.0f s" % (max(TICK_B), time.time() - t1))
                ref_cs = {t: ref["cs"][t - 1] for t in TICK_B}
                del ref
            if quale == "i":
                carica()
                cs0 = L0.copy()
                cs0[ic] += DIST
                rf = corsa(st, mot, par, lc, cs0, max(TICK_B), rr, kan, nk, s, 1, tieni=TICK_B)
                t = max(TICK_B)
                esito("(i-F) cs disturbato di %g sul nodo %d al tick 0: cs al tick %d = quello del codice di T2 AL BIT" % (DIST, ic, t), np.array_equal(rf["presi"][t], ref_cs[t]),
                      "max|diff| %.3e" % float(np.max(np.abs(rf["presi"][t] - ref_cs[t]))), deve=False)
                del rf
            K = K_RAMPA if quale == "iv" else 1
            if quale == "iv":
                carica()
                rk = corsa(st, mot, par, lc, bersaglio(L0, s, 1, 1), max(TICK_B), rr, kan, nk, s, 1, tieni=TICK_B)
                esito("(iv-B) il ciclo a K = 1: cs ai tick %s = quello del codice di T2 AL BIT" % (TICK_B,), all(np.array_equal(rk["presi"][t], ref_cs[t]) for t in TICK_B),
                      "; ".join("tick %d max|diff| %.3e" % (t, float(np.max(np.abs(rk["presi"][t] - ref_cs[t])))) for t in TICK_B))
                del rk
                b1 = bersaglio(L0, s, 1, K)
                print("  la rampa agisce: al tick 1 max|cs - s| %.6e contro max|L - s| %.6e: il rapporto %.6e; lambda_1 = sin^2(pi/(2K)) %.6e" % (float(np.max(np.abs(b1 - s))), float(np.max(np.abs(L0 - s))),
                      float(np.max(np.abs(b1 - s))) / float(np.max(np.abs(L0 - s))), math.sin(0.5 * math.pi / K) ** 2))
            carica()
            t1 = time.time()
            print("### LA CORSA (%s), %d tick" % (quale, n))
            sys.stdout.flush()
            try:
                ris = corsa(st, mot, par, lc, bersaglio(L0, s, 1, K), n, rr, kan, nk, s, K, tieni=TICK_B)
            except F1L.Muro as e:
                print("  ### IL MURO: %s -- FERMO" % e)
                print("=" * 130)
                print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
                return 1
            print("    %.0f s" % (time.time() - t1))
        if quale == "i":
            esito("(i-B) cs ai tick %s = quello del codice di T2 AL BIT" % (TICK_B,), all(np.array_equal(ris["presi"][t], ref_cs[t]) for t in TICK_B),
                  "; ".join("tick %d max|diff| %.3e" % (t, float(np.max(np.abs(ris["presi"][t] - ref_cs[t])))) for t in TICK_B))
            tc = {c["t"]: c for c in ris["camp"]}
            esito("(i-B) cs min e il raggio ai tick %s come stringhe = le righe del referto di T2" % (TICK_B,), all(("%.6f" % tc[t]["cs_min"], "%.2f" % tc[t]["raggio"]) == riga[t] for t in TICK_B),
                  "; ".join("tick %d: %s %s contro %s %s" % ((t, "%.6f" % tc[t]["cs_min"], "%.2f" % tc[t]["raggio"]) + riga[t]) for t in TICK_B))
        stampa(ris, n, nk)
    print("-" * 130)
    fronte(ris["camp"], vel_vec)
    p3 = pendenza3(ris, n)
    mn = min(c["cs_min"] for c in ris["camp"])
    tmn = min(ris["camp"], key=lambda c: c["cs_min"])
    print("PENDENZA_ULTIMO_TERZO %+.6f" % p3)
    print("  la pendenza di ln(cs min) nell'ultimo terzo (la definizione di T2): %+.4f per 1000 tick; il minimo %.6e al tick %d, il raggio %.2f" % (p3, mn, tmn["t"], tmn["raggio"]))
    if quale == "iv":
        with open(os.path.join(solitone.RADICE, "doc", "referti_l2", CORSE["i"]), encoding="utf-8") as f:
            pi_ = float(next(l.split()[1] for l in f if l.startswith("PENDENZA_ULTIMO_TERZO")))
        print("  la pendenza di (i), dal suo referto: %+.4f" % pi_)
        if mn > CSMIN_Q1 and p3 > P_Q1:
            print("  LA LETTURA: (q1) la discesa era il colpo dell'accensione: cs min sopra %g, la pendenza %+.4f > %g" % (CSMIN_Q1, p3, P_Q1))
        elif abs(p3 - pi_) <= P_Q2 * abs(pi_):
            print("  LA LETTURA: (q2) la discesa e' come in (i) (%+.4f contro %+.4f, entro il %d%%): il colpo non la spiega" % (p3, pi_, int(100 * P_Q2)))
        else:
            print("  LA LETTURA: caso intermedio: cs min %.3e, la pendenza %+.4f contro %+.4f di (i)" % (mn, p3, pi_))
    if quale == "ii":
        if p3 <= P_H1:
            print("  LA LETTURA: (h1) la discesa c'e' (%+.4f <= %g): la storia del bordo non serve a spiegarla -- ### CON IL LIMITE DELLA SEZ. 27.4.3: anche il vuoto si e' acceso tutto insieme" % (p3, P_H1))
        elif p3 > P_H2:
            print("  LA LETTURA: (h2) la discesa manca o e' debole (%+.4f > %g): la storia del bordo conta" % (p3, P_H2))
        else:
            print("  LA LETTURA: caso intermedio (%+.4f fra %g e %g)" % (p3, P_H1, P_H2))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %d tick; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, n, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
