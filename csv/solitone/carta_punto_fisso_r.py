# -*- coding: utf-8 -*-
r"""**(r-D5): `F` RESA DEFINITA, D3 RIFATTO A `34`, LA CONTINUAZIONE FINE** *(sul ramo laterale; Luca `2026-11-09` `08:56`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `12`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/carta_punto_fisso_r.py > doc/referti_l2/punto_fisso_cs_r.txt

**La scelta dichiarata:** **il punto medio di `Omega` risolto con un metodo ROBUSTO dentro la mappa di prova:** prima `energia_pesata.applica` del nucleo, IDENTICA; se alza perche' il punto
medio non converge, Newton-Krylov su `omega(fase a meta' con w) - w` collo stesso criterio e gli stessi controlli del tetto; se anche quello non converge, `OmegaNonEsiste`, contata.
**`s > 0` NON si impone.** **Il nucleo non si tocca:** `EP.applica` sostituita solo dentro un `with`.
**D4-R:** NK da `Lambda_c 272` a `34` a passi `2^{-1/4}` su `TBS` a `10000`. **D3-R:** Anderson e NK a `34` sulle quattro scene, da `x0`.
**I DEVE:** `R-B`, `R-V`, `PF-E`, `R-E-F` *(DEVE FALLIRE)*, `PF-F` *(DEVE FALLIRE)*.
**R1-R3** *(Luca `09:59`, la sez. `13`)*: a ogni scena, prima di D3-R, il profilo radiale di `Lambda` e `cs/s`, la forma della direzione instabile di D2, l'anello del guscio; la lettura `g1`/`g2`/`g-a`.
"""
import contextlib
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

LC_ALTO = 272.0                                  # ### sez. 12: dove D4 converge (34 x 2^3)
PASSI_D4R = 12                                   # ### sez. 12: 2^{-1/4} x 12 = 1/8
MAXITER = 200                                    # ### come D3
EPS = CPF.EPS
CONTO = {"robusto": 0, "non_esiste": 0}
LETTURE_R2 = {}
OK = [0, 0]
FALLITE = []


class OmegaNonEsiste(Exception):
    pass


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


@contextlib.contextmanager
def omega_robusto():
    """### `energia_pesata.applica` con il ripiego: le righe del nucleo, poi NK solo se il punto medio non converge."""
    import energia_pesata as EP
    from scipy import optimize as OP
    vera = EP.applica

    def applica(mot, st, par, frazione):
        try:
            return vera(mot, st, par, frazione)
        except AssertionError as e:
            if "il punto medio di `Omega` NON CONVERGE" not in str(e):
                raise
        # ### `vera` ha rimesso phi = salvo prima di alzare: lo stato e' quello di partenza
        tau = float(mot.dtau[0]) * float(frazione)
        phi = st["phi_h"]
        salvo = phi.copy()
        w0 = EP.omega(mot, st, par).copy()
        tetto = EP.tetto_omega(mot, st, par)
        grado_max = int(mot.inc.grado.max())
        scala = float(np.max(tetto))

        def G(w):
            np.multiply(salvo, np.exp(-1j * (w * (tau * 0.5))[mot.inc.nodo]), out=phi)
            return EP.omega(mot, st, par) - w
        try:
            w = np.asarray(OP.newton_krylov(G, w0, f_tol=EP.EPS_OMEGA * scala, maxiter=MAXITER), dtype=float)
            res = float(np.max(np.abs(G(w))))
            if not EP.entro_tolleranza(res, scala):
                raise OmegaNonEsiste("NK interno: il residuo %.3e oltre la tolleranza" % res)
        except Exception as e:
            phi[...] = salvo
            CONTO["non_esiste"] += 1
            if isinstance(e, OmegaNonEsiste):
                raise
            raise OmegaNonEsiste("il punto medio di `Omega` non esiste qui (NK interno: %s)" % (type(e).__name__ + " " + str(e)[:60]))
        np.multiply(salvo, np.exp(-1j * (w * (tau * 0.5))[mot.inc.nodo]), out=phi)
        EP.controlla_tetto(w, EP.tetto_omega(mot, st, par), grado_max, "Omega finale (NK interno)")
        np.multiply(salvo, np.exp(-1j * (w * tau)[mot.inc.nodo]), out=phi)
        mot.giri_omega = -1
        CONTO["robusto"] += 1
        return st
    EP.applica = applica
    try:
        yield
    finally:
        EP.applica = vera


def nk(F, x_ini):
    from scipy import optimize as OP
    n0 = F.n
    try:
        x = np.asarray(OP.newton_krylov(lambda y: F(y) - y, x_ini.copy(), f_tol=8.0 * EPS * float(np.max(np.abs(x_ini))), maxiter=MAXITER), dtype=float)
        return x, F.n - n0, ""
    except Exception as e:
        return None, F.n - n0, type(e).__name__ + ": " + str(e)[:90]


def anderson(F, x_ini):
    from scipy import optimize as OP
    n0 = F.n
    try:
        x = np.asarray(OP.anderson(lambda y: F(y) - y, x_ini.copy(), f_tol=8.0 * EPS * float(np.max(np.abs(x_ini))), maxiter=MAXITER), dtype=float)
        return x, F.n - n0, ""
    except Exception as e:
        return None, F.n - n0, type(e).__name__ + ": " + str(e)[:90]


def guscio(F, x, lam, rho, inc, L, s):
    """### **R1-R3** *(Luca `09:59`; la sez. `13`)*: il profilo radiale di `Lambda` e di `cs/s`, `r_min`; la forma della direzione instabile (la potenza di D2, lo stesso seme);
    il fattore sull'anello `[r_min - 2, r_min + 2]`. Rende la lettura `g1`, `g2` o `g-a`."""
    from solitone import toro as TO
    vv = np.arange(inc.n)
    m1, m2 = vv // L, vv % L
    c1, c2 = TO.centro(rho, m1, m2, L)[:2]
    pos = TO.scarti(m1, m2, c1, c2, L)
    r = np.hypot(pos[:, 0], pos[:, 1])
    w = math.sqrt(float(np.sum(rho * r * r) / np.sum(rho)))
    cs_s = F.FP.cs(lam, F.lc, F.fp) / s
    b = np.floor(r).astype(int)
    nb = int(b.max()) + 1
    cnt = np.bincount(b, minlength=nb).astype(float)
    lam_r = np.bincount(b, weights=lam, minlength=nb) / np.maximum(cnt, 1)
    cs_r = np.bincount(b, weights=cs_s, minlength=nb) / np.maximum(cnt, 1)
    validi = cnt > 0
    r_min = int(np.flatnonzero(validi)[np.argmin(lam_r[validi])])
    # ### R2: la potenza di D2 (le righe di carta_punto_fisso.potenza), col vettore
    Fx = F(x)
    v = np.random.default_rng(CPF.SEME).standard_normal(len(x))
    v /= np.linalg.norm(v)
    for _ in range(CPF.N_POT):
        wv = CPF.jv(F, x, Fx, v)
        rap = float(np.linalg.norm(wv))
        ray = float(np.dot(v, wv))
        v = wv / rap
    v2 = v * v
    v2_r = np.bincount(b, weights=v2, minlength=nb) / np.maximum(cnt, 1)
    r_pk = int(np.flatnonzero(validi)[np.argmax(v2_r[validi])])
    gus = (r >= r_min - 2) & (r <= r_min + 2)
    den = r < r_min - 2
    print("  R1 (il centro di rho, w %.3f; i dischi di D2: raggio %g intorno ai nodi piu' vicini a r 0, w, 2w e al piu' lontano): r_min di Lambda %d; Lambda e cs/s per anello:" % (w, CPF.R_DISCO, r_min))
    print("      %s" % "  ".join("%d:%.3f/%.3f" % (k, lam_r[k], cs_r[k]) for k in range(nb) if cnt[k] > 0 and k <= r_min + 12))
    print("  R4 (stampa) sul guscio [%d, %d]: Lambda min %.4f, cs/s min %.4f; al centro (r < 1) Lambda %.4f cs/s %.4f" % (r_min - 2, r_min + 2, float(lam[gus].min()), float(cs_s[gus].min()), float(lam[r < 1].mean()), float(cs_s[r < 1].mean())))
    print("  R2 la direzione instabile (|Jv|/|v| %.6f, <v,Jv>/<v,v> %+.6f): v^2 medio per nodo, per anello: %s" % (rap, ray, "  ".join("%d:%.2e" % (k, v2_r[k]) for k in range(nb) if cnt[k] > 0 and k <= r_min + 12)))
    print("  R2 il massimo del profilo a r %d; la quota di |v|^2 nel guscio %.3f, dentro %.3f, fuori %.3f" % (r_pk, float(v2[gus].sum()), float(v2[den].sum()), float(v2[~gus & ~den].sum())))
    u = gus.astype(float)
    u /= np.linalg.norm(u)
    wu = CPF.jv(F, x, Fx, u)
    print("  R3 l'anello del guscio [%d, %d] (%d nodi): |Jv|_anello/|v| %.4f (tutto %.4f)" % (r_min - 2, r_min + 2, int(gus.sum()), float(np.linalg.norm(wu[gus])), float(np.linalg.norm(wu))))
    g = "g1" if r_min - 2 <= r_pk <= r_min + 2 else ("g2" if r_pk < r_min - 2 else "g-a")
    print("  LA LETTURA R2: (%s)" % g)
    return g


def pfe(F, x, che):
    res = float(np.max(np.abs(F(x) - x)))
    return esito("PF-E %s: |F(x) - x| <= 8 eps |x|" % che, res <= 8 * EPS * float(np.max(np.abs(x))), "%.3e" % res)


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
    for m in ("__init__", "corsa_accensione", "toro", "carta_punto_fisso"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    import tick as TK
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr, _camp = CA.serie(CPF.CORSA)[:2]
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    t00 = time.time()
    print("=" * 130)
    print("(r-D5), F RESA DEFINITA (il punto medio di Omega robusto dentro la mappa di prova): %s; D4-R da Lambda_c %g a passi 2^(-1/4) x %d a %d tick; D3-R a 34 su %s; maxiter %d"
          % (CPF.CORSA, LC_ALTO, PASSI_D4R, CPF.TICK_D4, CPF.TICK_SCENE, MAXITER))
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
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        # ------------------------------------------------------------------ Lambda_c, R-V e R-B sul vuoto
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lc = float(np.mean(mot.densita_vuoto(st))) * (1.0 - s) / s
        print("### Lambda_c = %.12f (la decisione (P))" % lc)
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            Fv = CPF.Mappa(st, mot, par, lc)
            xv0 = Fv.x0()
            yn = Fv(xv0)
            with omega_robusto():
                yr = Fv(xv0)
                xs, gs, _s, _p = CPF.semplice(Fv, TK.GIRI_MAX)
                esito("R-V l'iterazione semplice sul vuoto F3, F definita: cs = s entro 8 eps relativo", gs is not None and float(np.max(np.abs(xs - s))) <= 8 * EPS * s, "%.3e" % float(np.max(np.abs(xs - s))))
                for nome, met in (("Anderson", anderson), ("Newton-Krylov", nk)):
                    x, nv, msg = met(Fv, xv0)
                    esito("R-V %s sul vuoto F3, F definita: cs = s entro 8 eps relativo" % nome, x is not None and float(np.max(np.abs(x - s))) <= 8 * EPS * s,
                          ("%.3e (%d valutazioni)" % (float(np.max(np.abs(x - s))), nv)) if x is not None else msg)
            esito("R-B sul vuoto F3: F con Omega robusto = F del nucleo, al bit", np.array_equal(yn, yr), "max %.1e" % float(np.max(np.abs(yn - yr))))

        def carica(t):
            xs_ = stati[t]
            with np.load(xs_["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            assert all(SFM.sha(st[k]) == v for k, v in xs_["sha"].items() if k in st), "lo stato NON e' quello registrato"
        # ------------------------------------------------------------------ D4-R
        print("-" * 130)
        carica(CPF.TICK_D4)
        print("### D4-R su %s a %d tick: la continuazione fine da Lambda_c %g" % (CPF.CORSA, CPF.TICK_D4, LC_ALTO))
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            F = CPF.Mappa(st, mot, par, LC_ALTO)
            xa, ga, _s, _p = CPF.semplice(F, TK.GIRI_MAX)
            print("  a %g: l'iterazione semplice del nucleo %s" % (LC_ALTO, ("converge in %d giri" % ga) if ga else "NON converge"))
            assert ga is not None, "a Lambda_c %g la semplice non converge: D4 diceva 41 giri" % LC_ALTO
            yn = F(xa)
            with omega_robusto():
                yr = F(xa)
            esito("R-B a Lambda_c %g: F con Omega robusto = F del nucleo, al bit" % LC_ALTO, np.array_equal(yn, yr), "max %.1e" % float(np.max(np.abs(yn - yr))))
            xp, lc_ok = xa, LC_ALTO
            with omega_robusto():
                for j in range(1, PASSI_D4R + 1):
                    lcj = LC_ALTO * 2.0 ** (-j / 4.0)
                    Fj = CPF.Mappa(st, mot, par, lcj)
                    r0, n0, t0 = dict(CONTO), Fj.n, time.time()
                    xj, nv, msg = nk(Fj, xp)
                    if xj is not None:
                        res = float(np.max(np.abs(Fj(xj) - xj)))
                        rap, ray = CPF.potenza(Fj, xj, 15)
                        print("    j %2d Lambda_c %9.4f: NK converge (%d valutazioni, %.0f s); |F(x)-x| %.2e; |Jv|/|v| %.4f <v,Jv>/<v,v> %+.4f; cs min %.6f max %.6f; dal passo prima %.2e; Omega robusto %d, non esiste %d"
                              % (j, lcj, nv, time.time() - t0, res, rap, ray, float(xj.min()), float(xj.max()), float(np.max(np.abs(xj - xp))), CONTO["robusto"] - r0["robusto"], CONTO["non_esiste"] - r0["non_esiste"]))
                        xp, lc_ok = xj, lcj
                    else:
                        print("    j %2d Lambda_c %9.4f: NK NON converge (%d valutazioni, %.0f s): %s; Omega robusto %d, non esiste %d"
                              % (j, lcj, nv, time.time() - t0, msg, CONTO["robusto"] - r0["robusto"], CONTO["non_esiste"] - r0["non_esiste"]))
                        try:
                            rap, ray = CPF.potenza(Fj, xp, 15)
                            print("      al punto del passo prima: |Jv|/|v| %.4f <v,Jv>/<v,v> %+.4f" % (rap, ray))
                        except Exception as e:
                            print("      al punto del passo prima: la potenza alza (%s)" % type(e).__name__)
                        break
                print("  D4-R: l'ultimo Lambda_c dove il ramo c'e' %.4f%s" % (lc_ok, " (arrivato a 34)" if abs(lc_ok - lc) < 1e-9 else ""))
                if abs(lc_ok - lc) < 1e-9:
                    pfe(CPF.Mappa(st, mot, par, lc), xp, "D4-R a 34")
        # ------------------------------------------------------------------ D3-R
        for t in CPF.TICK_SCENE:
            print("-" * 130)
            carica(t)
            t0 = time.time()
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                F = CPF.Mappa(st, mot, par, lc)
                x0 = F.x0()
                # ### R1-R3 (Luca 09:59) dallo stesso x di D2: la semplice del nucleo, GIRI_MAX giri
                xd, _g, _s, _p = CPF.semplice(F, TK.GIRI_MAX)
                rho = np.zeros(inc.n)
                np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
                LETTURE_R2[t] = guscio(F, xd, mot.densita_vuoto(st), rho, inc, z["L"], s)
                with omega_robusto():
                    if t == CPF.TICK_SCENE[0]:
                        res0 = float(np.max(np.abs(F(x0) - x0)))
                        esito("R-E-F PF-E sul punto di partenza x0 a 34 (non e' un punto fisso)", res0 <= 8 * EPS * float(np.max(np.abs(x0))), "%.3e" % res0, deve=False)
                    print("### D3-R su %s a %d tick, Lambda_c %.6f, da x0" % (CPF.CORSA, t, lc))
                    for nome, met in (("Anderson", anderson), ("Newton-Krylov", nk)):
                        r0 = dict(CONTO)
                        x, nv, msg = met(F, x0)
                        rob = "Omega robusto %d, non esiste %d" % (CONTO["robusto"] - r0["robusto"], CONTO["non_esiste"] - r0["non_esiste"])
                        if x is None:
                            print("  D3-R %s: NON converge (%d valutazioni): %s; %s" % (nome, nv, msg, rob))
                        else:
                            print("  D3-R %s: converge (%d valutazioni); cs min %.6f max %.6f; %s" % (nome, nv, float(x.min()), float(x.max()), rob))
                            pfe(F, x, "D3-R %s a %d" % (nome, t))
            print("  (%s a %d: %d valutazioni di F, %.0f s)" % (CPF.CORSA, t, F.n, time.time() - t0))
    # ------------------------------------------------------------------ PF-F: le righe di carta_punto_fisso.main
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
        g27n, msg27 = CPF.nucleo(CPF.Mappa(st27, mot27, par27, lc27))
    esito("PF-F l'iterazione semplice del nucleo sulla scena del 27/10 converge", g27n is not None, msg27[:60], deve=False)
    print("=" * 130)
    print("R2, LE LETTURE PER SCENA: %s" % ", ".join("%d: (%s)" % kv for kv in sorted(LETTURE_R2.items())))
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; Omega robusto %d volte, non esiste %d volte; %.0f s in tutto"
          % (OK[0], OK[1], len(FALLITE), FALLITE, CONTO["robusto"], CONTO["non_esiste"], time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
