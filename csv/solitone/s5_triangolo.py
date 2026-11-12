# -*- coding: utf-8 -*-
r"""**S5.0 (e): QUANTA ENERGIA PUO' CONTENERE UN TRIANGOLO** *(sul ramo laterale; Luca `2026-11-11` `11:46`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.5`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_triangolo.py > doc/referti_l2/s5_triangolo.txt

**La scena di `TBS` a `L 81`, il vuoto `c F3`, `cs = s` uniforme** *(`N = 1`)*, `mot.lambda_c = None`. **L'energia si LEGGE da `energia_pesata.termini_di_h`** *(la fonte unica)*: il totale, e per nodo il nodo
piu' meta' dei suoi archi. **Il limite del tempo:** le quasi-energie del tick lineare *(`psi` e `phi`)* nella finestra `(-pi, pi]` per tick; la forma quadratica *(senza `N`)* ristretta a un
nodo e a un triangolo, per polarizzazione. **Il limite dello spazio:** `N(rho)` a `Lambda = 6`; il minimo e il massimo dell'energia di un triangolo a norma per nodo fissata, `phi` fisso, con lo zero
O1 *(di oggi)* e O4 *(il nodo meno la media dei `6` vicini)*. **Le domande (1)-(3), senza scegliere.**
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
from solitone import carta_punto_fisso as CPF  # noqa: E402

A_IMP = 1e-6                    # ### l'impulso del tick lineare (come b1_profilo)
N_NU = 6                        # ### sez. 31.5: sei norme geometriche
NU_MIN = 1e-3                   # ### sez. 31.5: il limite lineare
NU_VUOTO = 18.0                 # ### sez. 31.5: la norma del vuoto di un triangolo, 3 x 6
PARTENZE = 8                    # ### sez. 31.5 (il ripiego: quante ne stanno nel tetto, almeno 1; dichiarato)
MAXITER = 100                   # ### mio: il tetto dei giri di L-BFGS-B
TETTO_S = 3600.0                # ### sez. 31.5: il tetto di 60 minuti
RHO_TAB = (1e-3, 1e-2, 1e-1, 1.0, 6.0, 60.0, 600.0)   # ### la tabella di N(rho) a Lambda 6 (mia)
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


def main():
    from scipy.optimize import minimize
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import composizione as CM
    import energia_pesata as EP
    import materia_vuoto as MV
    import tick as TK
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    for m in ("__init__", "corsa_accensione", "bordo", "carta_punto_fisso"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata", "materia_vuoto"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0 = CA.serie(CPF.CORSA)[0]
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("S5.0 (e) (sez. 31.5): quanta energia puo' contenere un triangolo; cs = s = %g uniforme (N = 1), mot.lambda_c = None; le partenze %d (ripiego sopra %g s: quante ne stanno, almeno 1)" % (s, PARTENZE, TETTO_S))
    print("=" * 130)
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
        n, Lt, m = inc.n, z["L"], inc.m
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        forma_psi = st["psi_h"].shape
        phi_b = c * phi_v
        nodo = np.asarray(inc.nodo)
        coppie = nodo.reshape(m, 2)
        xs = stati[CPF.TICK_D4]
        with np.load(xs["file"]) as d:
            M_scena = float(np.sum(np.abs(d["psi_h"]) ** 2))
        # ------------------------------------------------------------------ i vicini e il triangolo
        vicini = [set() for _ in range(n)]
        for a_, b_ in coppie:
            if a_ != b_:
                vicini[int(a_)].add(int(b_))
                vicini[int(b_)].add(int(a_))
        gradi = sorted({len(v) for v in vicini})
        b0 = min(vicini[0])
        c0_ = min(vicini[0] & vicini[b0])
        tri = np.array([0, b0, c0_])
        est = np.flatnonzero(np.isin(nodo, tri))
        blocchi = [np.flatnonzero(nodo[est] == k) for k in tri]
        archi_tri = [a for a in range(m) if set(coppie[a].tolist()) <= set(tri.tolist())]
        print("### la scena: L %d, %d nodi, i gradi %s; il triangolo %s (%d estremita', %d per nodo; gli archi interni %s); la norma di materia di %s a %d: %.6f"
              % (Lt, n, gradi, tri.tolist(), len(est), len(blocchi[0]), archi_tri, os.path.basename(xs["file"]), CPF.TICK_D4, M_scena))

        def metti(psi, phi):
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = psi.reshape(forma_psi)
            st["phi_h"][...] = phi
            mot.cs = np.full(n, float(s))
            mot.lambda_c = None

        def energie(psi, phi):
            """### `(totale, e per nodo)`: `termini_di_h`, il nodo piu' meta' dei suoi archi."""
            metti(psi, phi)
            pn, pa = EP.termini_di_h(mot, st, par)
            e = pn.copy()
            np.add.at(e, coppie[:, 0], 0.5 * pa)
            np.add.at(e, coppie[:, 1], 0.5 * pa)
            return float(np.sum(pn)) + float(np.sum(pa)), e

        def o4(e):
            return np.array([e[k] - np.mean([e[j] for j in vicini[k]]) for k in tri])

        zero = np.zeros((nodo.size, 2), dtype=complex)
        t0 = time.time()
        E0, e0 = energie(zero, phi_b)
        print("### NOTA: termini_di_h da' H NON pesato; con N = 1 e cs = s uniforme G = s H: le energie qui sono in unita' di H")
        t_e = time.time() - t0
        print("### il vuoto c F3 (psi = 0): E totale %.10e; per nodo da %.10e a %.10e; un'energia costa %.4f s" % (E0, float(e0.min()), float(e0.max()), t_e))
        esito("la somma delle energie per nodo = il totale (entro 1e-9 relativo)", abs(float(np.sum(e0)) - E0) <= 1e-9 * abs(E0), "%.3e" % (float(np.sum(e0)) - E0))
        # ------------------------------------------------------------------ il limite del tempo: le bande del tick lineare
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            print("### IL LIMITE DEL TEMPO: le quasi-energie eps = -arg(lambda) del tick lineare (per tick; la finestra (-pi, pi])")
            for nome, nc in (("psi", 12), ("phi", 6)):
                R = np.zeros((n, nc, nc), dtype=complex)
                for j in range(nc):
                    usc = []
                    for f in (1.0, -1.0):
                        ps = zero.copy().reshape(n, 12)
                        ph = phi_b.copy().reshape(n, 6)
                        if nome == "psi":
                            ps[0, j] += f * A_IMP
                        else:
                            ph[0, j] += f * A_IMP
                        metti(ps, ph.reshape(-1))
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        usc.append(st["psi_h"].reshape(n, 12).copy() if nome == "psi" else st["phi_h"].reshape(n, 6).copy())
                    R[:, :, j] = (usc[0] - usc[1]) / (2 * A_IMP)
                Ak = np.fft.fft2(R.reshape(Lt, Lt, nc, nc), axes=(0, 1))
                lam = np.linalg.eigvals(Ak.reshape(-1, nc, nc))
                eps = -np.angle(lam)
                print("    %s: |lambda| fra %.12f e %.12f; eps fra %+.6f e %+.6f (la finestra (-pi, pi]: occupata %.4f); per unita' di tempo (eps / s) fra %+.6f e %+.6f"
                      % (nome, float(np.abs(lam).min()), float(np.abs(lam).max()), float(eps.min()), float(eps.max()), float(eps.max() - eps.min()) / (2 * math.pi), float(eps.min()) / s, float(eps.max()) / s))
            # ------------------------------------------------------------------ la forma quadratica su un nodo e su un triangolo
            def qforma(x, quali):
                """### la parte QUADRATICA dell'energia *(senza `N`)* di `psi` sulle estremita' `quali`; `x` reale `(2 * 2 * len(quali))`."""
                ps = zero.copy()
                v = x.reshape(2, -1)
                ps[quali] = (v[0] + 1j * v[1]).reshape(len(quali), 2)
                E, _e = energie(ps, phi_b)
                metti(ps, phi_b)
                lamv = mot.densita_vuoto(st).copy()
                rho = np.zeros(n)
                np.add.at(rho, nodo, np.sum(np.abs(ps) ** 2, axis=1))
                return E - E0 - float(np.sum(MV.N(rho, lamv) - MV.N(np.zeros(n), lamv)))

            print("### LA FORMA QUADRATICA (i Grover, la moneta, gli spostamenti; senza N) per unita' di norma, per polarizzazione")
            for nome, quali in (("un nodo", np.flatnonzero(nodo == tri[0])), ("il triangolo", est)):
                dd = 4 * len(quali)
                H = np.zeros((dd, dd))
                for i in range(dd):
                    for j in range(i, dd):
                        u = np.zeros(dd)
                        u[i] += 1.0
                        u[j] += 1.0
                        w = np.zeros(dd)
                        w[i] += 1.0
                        w[j] -= 1.0
                        H[i, j] = H[j, i] = (qforma(u, quali) - qforma(w, quali)) / 4.0
                ev = np.linalg.eigvalsh(H)
                x = np.random.default_rng(CPF.SEME).normal(size=dd)
                errq = abs(qforma(x, quali) - float(x @ H @ x)) / abs(float(x @ H @ x))
                print("    %s (%d reali): l'energia per unita' di norma fra %+.10f e %+.10f; il controllo su un vettore a caso %.2e" % (nome, dd, float(ev.min()), float(ev.max()), errq))
                esito("%s: la polarizzazione riproduce la forma su un vettore a caso (entro 1e-9)" % nome, errq <= 1e-9, "%.2e" % errq)
        # ------------------------------------------------------------------ il limite dello spazio: N(rho)
        print("### IL LIMITE DELLO SPAZIO: N(rho, Lambda = 6) per nodo (la forma %s), e N / rho" % VC.FORMA)
        for r_ in RHO_TAB:
            Nv = float(MV.N(np.array([r_]), np.array([6.0]))[0])
            print("    rho %10.4g: N %+.10e, N / rho %+.10f" % (r_, Nv, Nv / r_))
        # ------------------------------------------------------------------ il triangolo: min e max a norma per nodo fissata
        nus = np.geomspace(NU_MIN, M_scena, N_NU)
        nus = np.unique(np.sort(np.concatenate([nus, [NU_VUOTO]])))
        print("### IL TRIANGOLO: il minimo e il massimo dell'energia a norma per nodo fissata (nu / 3), phi = c F3 fisso; le norme nu %s" % ", ".join("%.4g" % v for v in nus))

        def stato(x, nu):
            v = x.reshape(2, -1)
            q = (v[0] + 1j * v[1]).reshape(len(est), 2)
            for bl in blocchi:
                q[bl] *= math.sqrt(nu / 3.0) / max(float(np.linalg.norm(q[bl])), 1e-300)
            ps = zero.copy()
            ps[est] = q
            return ps

        def obiettivo(x, nu, zero_, segno):
            _E, e = energie(stato(x, nu), phi_b)
            v = float(np.sum(e[tri])) if zero_ == "O1" else float(np.sum(o4(e)))
            return segno * v
        e_v = {"O1": float(np.sum(e0[tri])), "O4": float(np.sum(o4(e0)))}
        print("    il vuoto (psi = 0): il triangolo vale O1 %+.10e, O4 %+.10e" % (e_v["O1"], e_v["O4"]))
        npart = PARTENZE
        rg = np.random.default_rng(CPF.SEME)
        risultati = []
        prima = True
        for nu in nus:
            for zero_ in ("O1", "O4"):
                for segno, chi in ((1.0, "min"), (-1.0, "max")):
                    migl = None
                    for p in range(npart):
                        x0 = rg.normal(size=4 * len(est))
                        ts = time.time()
                        r = minimize(obiettivo, x0, args=(nu, zero_, segno), method="L-BFGS-B", options={"maxiter": MAXITER})
                        if prima:
                            t1 = time.time() - ts
                            stima = t1 * len(nus) * 2 * 2 * npart
                            prima = False
                            if stima > TETTO_S:
                                npart = max(1, min(PARTENZE, int(TETTO_S / (t1 * len(nus) * 2 * 2))))
                                print("    ### il tetto: la prima ottimizzazione %.1f s, la stima %.0f s oltre %g: le partenze scendono a %d (dichiarato)" % (t1, stima, TETTO_S, npart))
                        val = segno * float(r.fun)
                        if migl is None or segno * val < segno * migl[0]:
                            migl = (val, r.x.copy(), int(r.nit), bool(r.success))
                    val, xb, nit, ok = migl
                    ps = stato(xb, nu)
                    pe = np.sum(np.abs(ps[est]) ** 2, axis=1)
                    sz = np.sum(np.abs(ps[est, 0]) ** 2) - np.sum(np.abs(ps[est, 1]) ** 2)
                    risultati.append((nu, zero_, chi, val))
                    print("    nu %10.4g, %s, %s: %+.10e (per unita' di norma, tolto il vuoto %+.6f); %d giri, %s; lo stato: la norma per estremita' [%s], sigma_z %+.4f"
                          % (nu, zero_, chi, val, (val - e_v[zero_]) / nu, nit, "converge" if ok else "### non converge", " ".join("%.3f" % (x / nu) for x in pe), float(sz) / nu))
                    sys.stdout.flush()
    # ================================================================== le domande
    print("-" * 130)
    print("  LE DOMANDE (sez. 31.5), senza scegliere:")
    for zero_ in ("O1", "O4"):
        mn = min(v for nu, z_, chi, v in risultati if z_ == zero_ and chi == "min")
        mx = max(v for nu, z_, chi, v in risultati if z_ == zero_ and chi == "max")
        print("  (1) con %s: il minimo trovato su tutte le norme %+.6e, il massimo %+.6e" % (zero_, mn, mx))
    print("  (2) rho_max per nodo del triangolo (tutta la materia della scena nel triangolo) = M / 3 = %.6f; N_min = 1/(1 + rho_max/rho_c) > 0 per ogni rho_c > 0" % (M_scena / 3.0))
    print("  (3) le scale (NESSUNA scelta): rho_max %.6f; Lambda 6; vedi le tabelle sopra per N / rho e per le bande" % (M_scena / 3.0))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
