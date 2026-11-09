# -*- coding: utf-8 -*-
r"""**D0-D4, IL PUNTO FISSO DI `cs` COL SOLITONE: LA DIAGNOSI DEL METODO** *(sul ramo laterale; il progetto `doc/TASK_HISTORY/2026-11-07_punto_fisso_cs_solitone.md`; i cambi
`doc/TASK_HISTORY/2026-11-09_laterale_mb.md` sez. `8`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/carta_punto_fisso.py > doc/referti_l2/punto_fisso_cs.txt

**La mappa:** `F(x) = FP.cs(densita_vuoto(lo stato al CENTRO del palindromo avanzato con mot.cs = x), Lambda_c)` *(le righe di `tick.cs_al_centro`, mezzo palindromo su una COPIA)*.
**`Lambda_c = Lambda_vuoto (1 - s) / s`** *(la decisione (P), derivata)*. **Le scene:** lo stato di `TBS` a `0`, `10000`, `100000`, `200000` tick *(ogni sha contro il jsonl)*.
**D0** l'iterazione semplice *(e `tick.cs_al_centro` stesso)*; **D1** dove *(gli anelli)*; **D2** la jacobiana a differenze finite *(la potenza, i dischi)*; **D3** Anderson e Newton-Krylov;
**D4** la continuazione in `Lambda_c = 34 x 2^k` su `TBS` a `10000`. **I DEVE:** `PF-V`, `PF-E`, `PF-U`, `PF-F` *(il progetto, sez. `2`)*.
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

CORSA = "TBS"
TICK_SCENE = (0, 10000, 100000, 200000)        # ### sez. 8, il cambio 1
TICK_D4 = 10000                                 # ### sez. 8, il cambio 2
K_D4 = tuple(range(10, -1, -1))                 # ### il progetto: Lambda_c = 34 x 2^k, k = 10 .. 0
N_POT = 30                                      # ### il progetto, D2 (a)
R_DISCO = 2.0                                   # ### il progetto, D2 (b)
SEME = 2026
EPS = float(np.finfo(float).eps)
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


class Mappa:
    """### **`F(x)`, le righe di `tick.cs_al_centro`** *(una COPIA dello stato, `mot.cs = x`, mezzo palindromo)*; **conta le valutazioni.**"""

    def __init__(self, st, mot, par, lambda_c):
        import flussi_parziali as FP
        import tick as TK
        self.FP, self.TK = FP, TK
        self.st, self.mot, self.par, self.lc = st, mot, par, float(lambda_c)
        self.meta = TK.meta_del_palindromo()
        self.fp = np.zeros(mot.inc.n)
        self.n = 0

    def x0(self):
        self.mot.lambda_c = self.lc
        return self.FP.cs(self.mot.densita_vuoto(self.st), self.lc, self.fp).copy()

    def __call__(self, x):
        self.n += 1
        self.mot.lambda_c = self.lc
        copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in self.st.items()}
        self.mot.cs = np.asarray(x, dtype=float).copy()
        self.TK.percorri_tick(copia, self.mot, self.par, (), None, self.meta)
        return self.FP.cs(self.mot.densita_vuoto(copia), self.lc, self.fp).copy()


def semplice(F, giri):
    """### **D0: l'iterazione semplice di Picard** *(il criterio del nucleo `EPS_CS`)*: `(x, giri o None, la serie degli scarti, x prima dell'ultimo)`."""
    import tick as TK
    prec = F.x0()
    serie = []
    for g in range(1, giri + 1):
        nuovo = F(prec)
        sc = float(np.max(np.abs(nuovo - prec)))
        serie.append(sc)
        if sc <= TK.EPS_CS * float(np.max(np.abs(nuovo))):
            return nuovo, g, serie, prec
        prec_, prec = prec, nuovo
    return prec, None, serie, prec_


def nucleo(F):
    """### `tick.cs_al_centro` stesso, sullo stato vero rimesso dopo: `(giri o None, il messaggio)`."""
    import tick as TK
    salv = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in F.st.items()}
    try:
        _c, g = TK.cs_al_centro(F.st, F.mot, F.par, F.lc, np.zeros(F.mot.inc.n), ())
        return g, ""
    except Exception as e:      # ### il nucleo ALZA se non converge: e' il dato, non un errore dello script
        return None, str(e)[:120]
    finally:
        for k, v in salv.items():
            if hasattr(v, "copy"):
                F.st[k][...] = v


def jv(F, x, Fx, v):
    h = math.sqrt(EPS) * float(np.max(np.abs(x)))
    return (F(x + h * v) - Fx) / h


def potenza(F, x, n):
    """### **D2 (a)**: `n` prodotti `J v`; `(|J v| / |v|, <v, J v> / <v, v>)` all'ultimo."""
    Fx = F(x)
    v = np.random.default_rng(SEME).standard_normal(len(x))
    v /= np.linalg.norm(v)
    rap = ray = float("nan")
    for _ in range(n):
        w = jv(F, x, Fx, v)
        rap = float(np.linalg.norm(w))
        ray = float(np.dot(v, w))
        v = w / rap
    return rap, ray


def dischi(F, x, centri, pos):
    """### **D2 (b)**: la contrazione locale `|J v|_disco / |v|` su un disco di raggio `R_DISCO` attorno a ogni centro *(una perturbazione uniforme sul disco)*."""
    Fx = F(x)
    out = []
    for nome, c in centri:
        msk = np.hypot(*(pos - pos[c]).T) <= R_DISCO
        v = msk.astype(float)
        v /= np.linalg.norm(v)
        w = jv(F, x, Fx, v)
        out.append((nome, int(msk.sum()), float(np.linalg.norm(w[msk])), float(np.linalg.norm(w))))
    return out


def robusti(F, x_ini):
    """### **D3**: Anderson e Newton-Krylov su `G = F(x) - x`, `f_tol = 8 eps max|x|`; `{nome: (x o None, valutazioni, il messaggio)}`."""
    from scipy import optimize as OP
    tol = 8.0 * EPS * float(np.max(np.abs(x_ini)))
    out = {}
    for nome, met in (("Anderson", OP.anderson), ("Newton-Krylov", OP.newton_krylov)):
        n0 = F.n
        try:
            x = met(lambda y: F(y) - y, x_ini.copy(), f_tol=tol, maxiter=200)
            out[nome] = (np.asarray(x, dtype=float), F.n - n0, "")
        except Exception as e:
            out[nome] = (None, F.n - n0, type(e).__name__ + ": " + str(e)[:80])
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
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    import tick as TK
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr, _camp = CA.serie(CORSA)[:2]
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    print("=" * 130)
    print("D0-D4, IL PUNTO FISSO DI cs COL SOLITONE (il laterale): %s a %s tick; D4 a %d, k %s; N_POT %d R_DISCO %g; EPS_CS %.3e GIRI_MAX %d" % (CORSA, TICK_SCENE, TICK_D4, K_D4, N_POT, R_DISCO, TK.EPS_CS, TK.GIRI_MAX))
    print("=" * 130)
    t00 = time.time()
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        L = z["L"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        vv = np.arange(inc.n)
        m1, m2 = vv // L, vv % L
        # ------------------------------------------------------------------ Lambda_c derivato, PF-V sul vuoto F3 da solo
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lam_v = float(np.mean(mot.densita_vuoto(st)))
        lc = lam_v * (1.0 - s) / s
        print("### Lambda_c = Lambda_vuoto (1 - s) / s = %.12f x %.12f = %.12f (la decisione (P); atteso 34)" % (lam_v, (1.0 - s) / s, lc))
        a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
        with a_, b_:
            Fv = Mappa(st, mot, par, lc)
            xv, gv, serv, _p = semplice(Fv, TK.GIRI_MAX)
            print("  PF-V, il vuoto F3: l'iterazione semplice %s giri; cs min %.15f max %.15f" % (gv, float(xv.min()), float(xv.max())))
            esito("PF-V l'iterazione semplice sul vuoto F3 da solo: cs = s ovunque entro 8 eps relativo", gv is not None and float(np.max(np.abs(xv - s))) <= 8 * EPS * s, "%.3e" % float(np.max(np.abs(xv - s))))
            rv = robusti(Fv, Fv.x0())
            for nome, (x, nv, msg) in rv.items():
                ok = x is not None and float(np.max(np.abs(x - s))) <= 8 * EPS * s
                esito("PF-V %s sul vuoto F3: cs = s ovunque entro 8 eps relativo" % nome, ok, ("%.3e (%d valutazioni)" % (float(np.max(np.abs(x - s))), nv)) if x is not None else msg)
        # ------------------------------------------------------------------ le scene
        for t in TICK_SCENE:
            xs = stati[t]
            with np.load(xs["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            ok_sha = all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st)
            print("-" * 130)
            print("### %s a %d tick (t %.0f): lo stato = lo sha registrato: %s" % (CORSA, t, t * s, ok_sha))
            assert ok_sha, "lo stato NON e' quello registrato"
            rho = np.zeros(inc.n)
            np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            c1, c2 = TO.centro(rho, m1, m2, L)[:2]
            pos = TO.scarti(m1, m2, c1, c2, L)
            r = np.hypot(pos[:, 0], pos[:, 1])
            w = math.sqrt(float(np.sum(rho * r * r) / np.sum(rho)))
            lam = mot.densita_vuoto(st)
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                F = Mappa(st, mot, par, lc)
                t0 = time.time()
                x, g, serie, prec = semplice(F, TK.GIRI_MAX)
                dt_f = (time.time() - t0) / max(F.n, 1)
                gn, msg = nucleo(F)
                print("  D0: l'iterazione semplice %s; tick.cs_al_centro %s; %.3f s per valutazione di F" % (("converge in %d giri" % g) if g else "NON converge in %d giri" % TK.GIRI_MAX,
                                                                                                     ("converge in %d giri" % gn) if gn else "ALZA (%s)" % msg, dt_f))
                print("      gli scarti, giro per giro (i primi 8 e gli ultimi 8): %s ... %s" % (" ".join("%.2e" % q for q in serie[:8]), " ".join("%.2e" % q for q in serie[-8:])))
                esito("D0-N la copia della mappa = il nucleo: lo stesso numero di giri (o tutti e due non convergono)", g == gn, "copia %s, nucleo %s" % (g, gn))
                # D1
                d1 = np.abs(x - prec)
                anelli = (("r < w", r < w), ("w..2w", (r >= w) & (r < 2 * w)), ("2w..4w", (r >= 2 * w) & (r < 4 * w)), ("> 4w", r >= 4 * w))
                tot = float(np.sum(d1 ** 2)) or 1.0
                print("  D1 (w %.3f): %s" % (w, "; ".join("%s: %d nodi, quota %.3f, max %.2e, Lambda %.4f cs %.5f rho %.3e" % (nm, int(mk.sum()), float(np.sum(d1[mk] ** 2)) / tot, float(d1[mk].max()) if mk.any() else 0.0,
                                                                                                                   float(lam[mk].mean()), float(x[mk].mean()), float(rho[mk].mean())) for nm, mk in anelli)))
                # D2
                rap, ray = potenza(F, x, N_POT)
                ic = int(np.argmin(r))
                centri = [("centro", ic), ("r = w", int(np.argmin(np.abs(r - w)))), ("r = 2w", int(np.argmin(np.abs(r - 2 * w)))), ("vuoto", int(np.argmax(r)))]
                dd = dischi(F, x, centri, pos)
                print("  D2 (a) la potenza, %d prodotti: |J v|/|v| %.6f, <v, J v>/<v, v> %+.6f" % (N_POT, rap, ray))
                print("  D2 (b) i dischi di raggio %g: %s" % (R_DISCO, "; ".join("%s (%d nodi) %.4f (tutto %.4f)" % q for q in dd)))
                # D3
                rb = robusti(F, x)
                for nome, (xr, nv, msgr) in rb.items():
                    if xr is None:
                        print("  D3 %s: NON converge (%d valutazioni): %s" % (nome, nv, msgr))
                        continue
                    res = float(np.max(np.abs(F(xr) - xr)))
                    esito("PF-E %s a %d: |F(x) - x| <= 8 eps |x|" % (nome, t), res <= 8 * EPS * float(np.max(np.abs(xr))), "%.3e (%d valutazioni; da D0 %.3e)" % (res, nv, float(np.max(np.abs(xr - x)))))
                xa, xn = rb["Anderson"][0], rb["Newton-Krylov"][0]
                if xa is not None and xn is not None:
                    dist = float(np.max(np.abs(xa - xn)))
                    if rap < 1.0:
                        lim = 2 * 8 * EPS * float(np.max(np.abs(xa))) / (1.0 - rap)
                        esito("PF-U a %d: i due metodi entro 2 x 8 eps |x| / (1 - rho)" % t, dist <= lim, "%.3e (il limite %.3e, rho %.4f)" % (dist, lim, rap))
                    else:
                        print("  PF-U a %d: rho %.4f >= 1, il limite non esiste: la distanza %.3e (senza verdetto, dichiarato)" % (t, rap, dist))
                # D4
                if t == TICK_D4:
                    print("  D4, la continuazione in Lambda_c = %.6f x 2^k (questa scena):" % lc)
                    xp = None
                    for k in K_D4:
                        F4 = Mappa(st, mot, par, lc * 2 ** k)
                        x4, g4, s4, _ = semplice(F4, TK.GIRI_MAX)
                        rap4, ray4 = potenza(F4, x4, 15)
                        n0 = F4.n
                        from scipy import optimize as OP
                        try:
                            xk = OP.newton_krylov(lambda y: F4(y) - y, (xp if xp is not None else x4).copy(), f_tol=8.0 * EPS * float(np.max(np.abs(x4))), maxiter=200)
                            dk = float(np.max(np.abs(xk - x4)))
                            xp = xk
                            nk = "NK %d valutazioni, da D0 %.2e" % (F4.n - n0, dk)
                        except Exception as e:
                            nk = "NK non converge (%s)" % type(e).__name__
                        print("    k %2d Lambda_c %12.4f: semplice %s; |J v|/|v| %.4f <v,Jv>/<v,v> %+.4f; cs vuoto %.6f; %s" % (k, lc * 2 ** k, ("%d giri" % g4) if g4 else "NON converge (ultimo scarto %.2e)" % s4[-1],
                                                                                                                    rap4, ray4, float(x4[r >= 4 * w].mean()), nk))
            print("  (%s a %d: %d valutazioni di F, %.0f s)" % (CORSA, t, F.n, time.time() - t0))
    # ------------------------------------------------------------------ PF-F: la scena del 27/10
    print("-" * 130)
    import _energia_del_legame as EL
    import _modi_pi_e_solitoni as MPS
    import _solitoni_triangoli as STR
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(VC.S)
        rec27 = {"larghezza": MPS.largo(VC.FORMA, cc, VC.S, 1e5)["larghezza"], "c": cc}
    finally:
        MPS.LAM0 = vero
    L27, inc27, mot27, st27, par27 = EL.stato(1e5, 12.0, rec27)[:5]
    lc27 = 1.0 * float(np.mean(mot27.densita_vuoto(st27)))
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        F27 = Mappa(st27, mot27, par27, lc27)
        g27n, msg27 = nucleo(F27)
    print("### PF-F la scena del 27/10 (S1, N 1e5, L %d, lambda_c %.6f): tick.cs_al_centro %s" % (L27, lc27, ("converge in %d giri" % g27n) if g27n else "ALZA (%s)" % msg27))
    esito("PF-F l'iterazione semplice del nucleo sulla scena del 27/10 converge", g27n is not None, msg27[:60], deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
