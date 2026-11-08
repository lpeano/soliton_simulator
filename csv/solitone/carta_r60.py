# -*- coding: utf-8 -*-
r"""**LA SIMMETRIA `R60` DEL TICK SUGLI SPINORI** *(Luca `2026-11-08` `12:30`; il task history `doc/TASK_HISTORY/2026-11-08_simmetria_R60.md`)*. [[PIANO-2D-3D]]

    python csv/solitone/carta_r60.py > doc/referti_l2/simmetria_r60.txt

### **La scena della corsa a `L = 12`** *(`V.scena` sotto `CA.con_L`; `cs` spento, il vuoto `F3`, `U = I`)*. **`Rk` = la rotazione di `60 k` gradi attorno al nodo `0`:** i nodi
`(m1, m2) -> (m1 - m2, m1)` *(`k` volte)*, l'estremita' di direzione uscente `j` *(`0 .. 5`, a `60` gradi)* nell'estremita' di direzione `j + k` del nodo immagine, e una `S` `12 x 12`
per nodo nella base locale *(direzione x spin)*. ### **La `S` derivata:** la permutazione delle direzioni `x` `S60^k`, `S60 = exp(-i (pi/6) sigma_z)`.
### **I controlli di servizio** `C1` *(la mappa e' una permutazione, manda archi in archi, `R60^6 = I`)*, `C2` *(`n` dell'immagine = `R60 n`)*, `C3` *(`dtau`, `s_a` invarianti)*.
### **La ricerca** *(R2)*: sulla parte LINEARE del tick *(senza `CAMM-MATERIA-VUOTO`)*, le `S` con `T R_S x = R_S T x` su `5` vettori casuali: il nucleo dalla SVD, per `R60`, `R120`,
`R180` *(e `R60` senza la moneta, per dire chi fissa `S`)*. ### **La prova sul tick INTERO:** `5` stati *(i semi `1 .. 5`)*, `N_T` tick, `||T^N(R x) - R T^N(x)|| / ||x||` contro la
soglia derivata `2 x 14 x N_T x 10 eps`; **DEVE FALLIRE** `F1` la sola permutazione, `F2` `S60^dag`; **il controllo** `P`: `R180 x sigma_z` col metodo nuovo.
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

L_R60 = 12                     # ### Luca 12:30: L piccolo (12 o il piu' piccolo in cui il tick e' definito)
SEMI = (1, 2, 3, 4, 5)         # ### il mandato: almeno 5 stati coi semi dichiarati
N_T = 10                       # ### il N_TICK di carta_d0
FLOP_PEZZO = 10                # ### la sez. 2 del task history: le operazioni per componente di un pezzo, al piu'
EPS = float(np.finfo(float).eps)
SOGLIA = 2 * 14 * N_T * FLOP_PEZZO * EPS     # ### 6.2e-13: due corse, 14 pezzi, N_T tick
SV_REL = 1e-10                 # ### il nucleo: i valori singolari sotto sigma_max x 1e-10 (si stampano tutti i piccoli)
TBS_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_100000_completo.npz")
S60 = np.diag([np.exp(-1j * math.pi / 6.0), np.exp(1j * math.pi / 6.0)])
SZ = np.diag([1.0 + 0j, -1.0])

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def estremita_per_direzione(inc, nv):
    """### `ext[v, j]`: l'estremita' del nodo `v` con direzione uscente `j` *(l'angolo di `n` diviso `60` gradi)*; ALZA se un nodo non ha le sei direzioni."""
    ang = np.degrees(np.arctan2(nv[:, 1], nv[:, 0]))
    j = np.rint(ang / 60.0).astype(int) % 6
    assert float(np.max(np.abs(ang - 60.0 * np.rint(ang / 60.0)))) <= 1e-9, "una direzione non e' a multipli di 60 gradi"
    ext = -np.ones((inc.n, 6), dtype=np.int64)
    ext[inc.nodo, j] = np.arange(2 * inc.m)
    assert np.all(ext >= 0) and len(np.unique(ext)) == 2 * inc.m, "un nodo non ha le sei direzioni, una per estremita'"
    return ext


def mappa_nodi(L, k):
    v = np.arange(L * L)
    m1, m2 = v // L, v % L
    for _ in range(k % 6):
        m1, m2 = (m1 - m2) % L, m1 % L
    return m1 * L + m2


def applica(x, ext, nm, k, S):
    """### `R_S` su `x` *(per estremita', `(2m, c)`)*: **il vettore locale del nodo `v`** *(direzione x componente)* **va, moltiplicato per `S`, nel nodo `nm[v]`**; `S` agisce su `6 c`."""
    c = x.shape[1]
    X = x[ext].reshape(ext.shape[0], 6 * c)        # (n, 6c): la base locale
    Y = X @ S.T
    out = np.empty_like(x)
    out[ext[nm]] = Y.reshape(ext.shape[0], 6, c)
    return out


def S_derivata(k, spin):
    """### la permutazione `j -> j + k` delle direzioni `x` `spin` *(2 x 2)*."""
    P = np.zeros((6, 6))
    for j in range(6):
        P[(j + k) % 6, j] = 1.0
    return np.kron(P, spin)


def main():
    import _deriva_congelato as DC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import composizione as CM
    import flussi_parziali as FP
    import tick as TK
    from solitone import corsa_accensione as CA
    for m in ("__init__", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    t_ini = time.time()
    sol, vuoto, s = V.CORSE[CA.NOME]
    with np.load(TBS_LIB) as d:
        rho_tbs = float(np.mean(d["rho"]))
    print("=" * 130)
    print("LA SIMMETRIA R60 DEL TICK SUGLI SPINORI (Luca 12:30): la scena di %s a L %d (s %g, eps %g, vuoto %s, cs spento, U = I); N_T %d; SEMI %s; la soglia 2 x 14 x %d x %d eps = %.3e; SV_REL %g"
          % (CA.NOME, L_R60, s, V.EPS, vuoto, N_T, SEMI, N_T, FLOP_PEZZO, SOGLIA, SV_REL))
    print("  l'ampiezza degli stati casuali: rho medio per nodo di TBS a 100000 = %.6e (%s)" % (rho_tbs, TBS_LIB))
    print("=" * 130)
    ids = [idl for idl, _f, _t in CM.ORDINE]
    assert "CAMM-MATERIA-VUOTO" in ids and "CAMM-MONETA-SPIN" in ids, ids
    print("  l'ordine del tick (%d posizioni): %s" % (len(ids), ids))
    with CA.con_L(L_R60), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        st, inc, mot, par = z["st"], z["inc"], z["mot"], z["par"]
        L = int(z["L"])
        assert L == L_R60, (L, L_R60)
        nv = mot.geo.n
        ext = estremita_per_direzione(inc, nv)
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        print("  la scena: L %d, %d nodi, %d archi, %d estremita'; le chiavi %s; max|U - I| %.1e" % (L, inc.n, inc.m, 2 * inc.m, {k: st[k].shape for k in chiavi},
                                                                                              float(np.max(np.abs(mot.geo.U - np.eye(2)[None])))))
        # ------------------------------------------------------------------ C1, C2, C3
        nm1 = mappa_nodi(L, 1)
        dove = np.empty(2 * inc.m, dtype=np.int64)
        for j in range(6):
            dove[ext[:, j]] = ext[nm1, (j + 1) % 6]
        perm = np.array_equal(np.sort(dove), np.arange(2 * inc.m))
        archi = bool(np.all((dove[0::2] ^ 1) == dove[1::2]))
        p6 = np.arange(2 * inc.m)
        for _ in range(6):
            p6 = dove[p6]
        esito("DEVE PASSARE: C1 R60 sulle estremita' e' una permutazione, manda archi in archi, e R60^6 = I", perm and archi and np.array_equal(p6, np.arange(2 * inc.m)),
              "permutazione %s, archi %s" % (perm, archi))
        c, sn = math.cos(math.pi / 3.0), math.sin(math.pi / 3.0)
        Rn = np.array([[c, -sn, 0.0], [sn, c, 0.0], [0.0, 0.0, 1.0]])
        d2 = float(np.max(np.abs(nv[dove] - nv @ Rn.T)))
        esito("DEVE PASSARE: C2 n dell'estremita' immagine = R60 n (entro 8 eps)", d2 <= 8 * EPS, "%.2e; max|n_z| %.1e" % (d2, float(np.max(np.abs(nv[:, 2])))))
        dn = FP.dtau_nodo(mot).copy()
        sa = FP.s_arco(mot).copy()
        esito("DEVE PASSARE: C3 dtau per nodo e s_a per arco invarianti sotto R60 (al bit)", np.array_equal(dn[nm1], dn) and np.array_equal(sa[dove[0::2] // 2], sa),
              "dtau %s .. %s; s_a %s .. %s" % (dn.min(), dn.max(), sa.min(), sa.max()))

        def lineare(x):
            """### la parte LINEARE del tick su `psi_h` *(senza `CAMM-MATERIA-VUOTO`)*, `phi_h` della scena."""
            st["psi_h"][...] = x
            mot.apri_tick()
            for idl, fr, _t in CM.ORDINE:
                if idl in salta:
                    continue
                nome, vp = TK.OPERATORE[idl]
                mot.operatori[nome](st, par if vp else {}, fr)
            mot.chiudi_tick()
            return st["psi_h"].copy()

        # ### il vuoto F3 ESPLICITO (la versione 1 usava quello della scena: non dimostrato F3, la sez. 4.4 del task history)
        import _solitone_dal_fondo as SDF
        F3 = CA.vuoto_della_corsa(z, "TBS")
        assert CA.fasi_vuoto("TBS") == tuple(dict(SDF.FASI)["F3"]), CA.fasi_vuoto("TBS")
        print("  il vuoto della scena (V.scena) contro F3: |phi_scena - F3| / |F3| = %.3e; phi <- F3 (le fasi %s per gli assi %s)"
              % (float(np.linalg.norm(st["phi_h"] - F3) / np.linalg.norm(F3)), CA.fasi_vuoto("TBS"), SDF.DIREZIONI))
        st["phi_h"][...] = F3
        base = {k: st[k].copy() for k in chiavi}

        def rimetti():
            for k in chiavi:
                st[k][...] = base[k]

        # ------------------------------------------------------------------ R2: la ricerca
        NON_LINEARI = tuple(i for i in ("CAMM-MATERIA-VUOTO", "CAMM-FASE-VUOTO") if i in ids)
        print("  la parte lineare: l'ordine SENZA %s" % (NON_LINEARI,))
        rng = np.random.default_rng(SEMI[0])
        xs = [rng.normal(size=st["psi_h"].shape) + 1j * rng.normal(size=st["psi_h"].shape) for _ in SEMI]
        salta = NON_LINEARI
        a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
        with a_, b_:
            rimetti()
            t1 = lineare(xs[0])
            rimetti()
            t2 = lineare(xs[1])
            rimetti()
            t12 = lineare(xs[0] + (0.5 - 0.25j) * xs[1])
        rimetti()
        d4 = float(np.max(np.abs(t12 - t1 - (0.5 - 0.25j) * t2))) / float(np.max(np.abs(t12)))
        esito("DEVE PASSARE: C4 la parte lineare E' lineare: T(x + c y) = T x + c T y (entro %.1e relativo, la soglia della prova)" % SOGLIA, d4 <= SOGLIA, "%.2e" % d4)
        nucleo = {}
        a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
        with a_, b_:
            for k, senza in ((1, ()), (2, ()), (3, ()), (1, ("CAMM-MONETA-SPIN",))):
                salta = NON_LINEARI + senza
                nm = mappa_nodi(L, k)
                righe = []
                for x in xs:
                    rimetti()
                    Tx = lineare(x)
                    col = []
                    for a in range(12):
                        for b in range(12):
                            E = np.zeros((12, 12))
                            E[a, b] = 1.0
                            rimetti()
                            col.append((lineare(applica(x, ext, nm, k, E)) - applica(Tx, ext, nm, k, E)).ravel())
                    righe.append(np.array(col).T)
                Mx = np.vstack(righe)
                _u, sv, vh = np.linalg.svd(Mx, full_matrices=False)
                dim = int(np.sum(sv <= sv[0] * SV_REL))
                Sd = S_derivata(k, np.linalg.matrix_power(S60, k))
                cos_ = None
                if dim >= 1:
                    Sf = np.conj(vh[-1]).reshape(12, 12)
                    cos_ = abs(np.vdot(Sd.ravel(), Sf.ravel())) / (np.linalg.norm(Sd) * np.linalg.norm(Sf))
                nucleo[(k, senza)] = (dim, cos_)
                print("  R2 R%-3d %-22s: il nucleo ha dimensione %d; i 6 valori singolari piu' piccoli / sigma_max %s; |<S derivata, S trovata>| %s"
                      % (60 * k, "senza " + senza[0] if senza else "il tick lineare", dim, ["%.1e" % v for v in (sv[-6:] / sv[0])],
                         "%.15f" % cos_ if cos_ is not None else "-"))
                sys.stdout.flush()
        rimetti()
        esito("DEVE PASSARE: R2-a il nucleo di R60 ha dimensione 1 e il suo vettore e' la S derivata a meno di una fase (entro 1e-10)",
              nucleo[(1, ())][0] == 1 and nucleo[(1, ())][1] is not None and abs(nucleo[(1, ())][1] - 1.0) <= 1e-10, "dim %d, coseno %s" % nucleo[(1, ())])
        esito("DEVE PASSARE: R3 lo stesso metodo ritrova R180 x sigma_z (dimensione 1, la S derivata con S60^3 = -i sigma_z)",
              nucleo[(3, ())][0] == 1 and nucleo[(3, ())][1] is not None and abs(nucleo[(3, ())][1] - 1.0) <= 1e-10, "dim %d, coseno %s" % nucleo[(3, ())])
        print("  R2 LETTURA: senza la moneta il nucleo di R60 ha dimensione %d (con la moneta %d): %s"
              % (nucleo[(1, ("CAMM-MONETA-SPIN",))][0], nucleo[(1, ())][0], "la moneta e' cio' che fissa la S sullo spin" if nucleo[(1, ("CAMM-MONETA-SPIN",))][0] > nucleo[(1, ())][0] else "la moneta non cambia il nucleo"))

        # ------------------------------------------------------------------ la prova sul tick INTERO
        def tick_n(x):
            st["psi_h"][...] = x[0]
            st["phi_h"][...] = x[1]
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                for _ in range(N_T):
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            return st["psi_h"].copy(), st["phi_h"].copy()

        def R(x, k, spin):
            nm = mappa_nodi(L, k)
            return (applica(x[0], ext, nm, k, S_derivata(k, spin)), applica(x[1].reshape(-1, 1), ext, nm, k, S_derivata(k, np.eye(1))).reshape(-1))

        sig = math.sqrt(rho_tbs / 12.0)
        casi = (("R60 x S60", 1, S60), ("R120 x S60^2", 2, S60 @ S60), ("P: R180 x sigma_z", 3, SZ), ("F1: R60 x I", 1, np.eye(2, dtype=complex)), ("F2: R60 x S60^dag", 1, np.conj(S60).T))
        res = {n_: [] for n_, _k, _s in casi}
        resV = {n_: [] for n_, _k, _s in casi}
        for seme in SEMI:
            rg = np.random.default_rng(seme)
            x = ((rg.normal(size=st["psi_h"].shape) + 1j * rg.normal(size=st["psi_h"].shape)) * sig / math.sqrt(2.0), base["phi_h"].copy())
            nx = math.sqrt(float(np.sum(np.abs(x[0]) ** 2) + np.sum(np.abs(x[1]) ** 2)))
            rimetti()
            Tx = tick_n(x)
            for nome, k, spin in casi:
                rimetti()
                a = tick_n(R(x, k, spin))
                b = R(Tx, k, spin)
                r = math.sqrt(float(np.sum(np.abs(a[0] - b[0]) ** 2) + np.sum(np.abs(a[1] - b[1]) ** 2))) / nx
                res[nome].append(r)
                # ### (V): phi FISSO (F3), si ruota solo psi
                rimetti()
                aV = tick_n((R(x, k, spin)[0], x[1]))
                bV = R(Tx, k, spin)
                rp = math.sqrt(float(np.sum(np.abs(aV[0] - bV[0]) ** 2))) / nx
                cf = np.vdot(bV[1], aV[1]) / np.vdot(bV[1], bV[1])     # ### phi: contro R T phi A MENO DI UNA FASE GLOBALE (per R180: R F3 = -F3)
                rf = math.sqrt(float(np.sum(np.abs(aV[1] - cf * bV[1]) ** 2))) / nx
                resV[nome].append((math.hypot(rp, rf), rp, rf))
            print("  il seme %d: ||x|| %.4e; (L) r %s" % (seme, nx, {n_: "%.2e" % res[n_][-1] for n_ in res}))
            print("             (V) r (psi, phi) %s" % ({n_: "%.2e (%.1e, %.1e)" % resV[n_][-1] for n_ in resV}))
            sys.stdout.flush()
        rimetti()
        # ------------------------------------------------------------------ il vuoto ruotato, le quasi-energie
        RF3 = R((np.zeros_like(base["psi_h"]), F3), 1, S60)[1]
        print("  R60 F3 contro le 8 terne di fasi in {0, pi}^3 (gli assi %s), a meno di una fase globale:" % (SDF.DIREZIONI,))
        uguale = []
        for terna in [(a, b, c) for a in (0.0, math.pi) for b in (0.0, math.pi) for c in (0.0, math.pi)]:
            F = SDF.fondo_con_fasi(inc, L, terna)
            cc = np.vdot(F, RF3) / np.vdot(F, F)
            d_ = float(np.linalg.norm(RF3 - cc * F) / np.linalg.norm(RF3))
            if d_ <= 1e-12:
                uguale.append(terna)
            print("    %-28s |R60 F3 - c F| / |F| = %.2e (c = %.3f%+.3fi)" % ("(%s)" % ", ".join("pi" if v else "0" for v in terna), d_, cc.real, cc.imag))
        print("  R60 F3 = %s; R180 F3 = c F3 con |R180 F3 - c F3| / |F3| = %.2e"
              % (["(%s)" % ", ".join("pi" if v else "0" for v in tt) for tt in uguale] or "nessuna delle 8",
                 float(np.linalg.norm(R((np.zeros_like(base["psi_h"]), F3), 3, SZ)[1] + F3) / np.linalg.norm(F3))))

        def qe(F):
            rimetti()
            y = tick_n((np.zeros_like(base["psi_h"]), F))[1]
            lam = np.vdot(F, y) / np.vdot(F, F)
            return -math.atan2(lam.imag, lam.real) / N_T, float(np.linalg.norm(y - lam * F) / np.linalg.norm(F))
        q3, r3 = qe(F3)
        qr, rr_ = qe(RF3)
        print("  la quasi-energia del vuoto (psi = 0, %d tick): F3 omega %.15f (residuo %.1e); R60 F3 omega %.15f (residuo %.1e)" % (N_T, q3, r3, qr, rr_))
        rimetti()
        # ------------------------------------------------------------------ R6: S^6
        Sd = S_derivata(1, S60)
        S6 = np.linalg.matrix_power(Sd, 6)
        rg = np.random.default_rng(SEMI[0])
        y = rg.normal(size=base["psi_h"].shape) + 1j * rg.normal(size=base["psi_h"].shape)
        y0 = y.copy()
        nm1_ = mappa_nodi(L, 1)
        for _ in range(6):
            y = applica(y, ext, nm1_, 1, Sd)
        d6m = float(np.max(np.abs(S6 + np.eye(12))))
        d6s = float(np.linalg.norm(y + y0) / np.linalg.norm(y0))
        print("  R6: S^6 = -I (max|S^6 + I| %.1e); R60 sei volte su uno stato: |R^6 y + y| / |y| = %.1e; det S60 = %.15f%+.15fi"
              % (d6m, d6s, np.linalg.det(S60).real, np.linalg.det(S60).imag))
    print("=" * 130)
    esito("DEVE PASSARE: R6 S^6 = -I e R60^6 y = -y (entro %.1e: la materia cambia segno dopo un giro, con det S60 = 1)" % SOGLIA, d6m <= SOGLIA and d6s <= SOGLIA, "%.1e, %.1e" % (d6m, d6s))
    esito("DEVE PASSARE: R60 x S60 commuta col tick INTERO, %d tick, ogni seme: r <= %.2e" % (N_T, SOGLIA), max(res["R60 x S60"]) <= SOGLIA, "il massimo %.2e" % max(res["R60 x S60"]))
    esito("DEVE PASSARE: P R180 x sigma_z (la nota) col metodo nuovo e la STESSA soglia, ogni seme", max(res["P: R180 x sigma_z"]) <= SOGLIA, "il massimo %.2e" % max(res["P: R180 x sigma_z"]))
    esito("DEVE FALLIRE: F1 R60 con la sola permutazione (S = I sullo spin): r <= soglia, un seme qualunque", not min(res["F1: R60 x I"]) <= SOGLIA, "il minimo %.2e" % min(res["F1: R60 x I"]))
    esito("DEVE FALLIRE: F2 R60 con S60^dag (il verso sbagliato): r <= soglia, un seme qualunque", not min(res["F2: R60 x S60^dag"]) <= SOGLIA, "il minimo %.2e" % min(res["F2: R60 x S60^dag"]))
    print("  registrato: R120 x S60^2, il massimo %.2e" % max(res["R120 x S60^2"]))
    print("  (V) IL VUOTO F3 FISSO (si ruota solo psi): il massimo per caso %s" % {n_: "%.2e" % max(v[0] for v in resV[n_]) for n_ in resV})
    vL = max(res["R60 x S60"]) <= SOGLIA
    vV = max(v[0] for v in resV["R60 x S60"]) <= SOGLIA
    print("  LA LETTURA (sez. 4.2): (L) %s, (V) %s -> %s" % ("passa" if vL else "NON passa", "passa" if vV else "NON passa",
          "R60 piena, F3 invariante" if vL and vV else ("ROTTURA SPONTANEA: le leggi R60, il vuoto F3 no" if vL else "le leggi stesse rompono R60 (la lettura (b))")))
    esito("DEVE PASSARE: P (V) R180 x sigma_z col vuoto F3 FISSO (R180 F3 = -F3, una fase globale), ogni seme", max(v[0] for v in resV["P: R180 x sigma_z"]) <= SOGLIA,
          "il massimo %.2e" % max(v[0] for v in resV["P: R180 x sigma_z"]))
    esito("DEVE FALLIRE: F1-V la sola permutazione col vuoto fisso: r <= soglia", not min(v[0] for v in resV["F1: R60 x I"]) <= SOGLIA, "il minimo %.2e" % min(v[0] for v in resV["F1: R60 x I"]))
    print("  il tempo: %.0f s" % (time.time() - t_ini))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
