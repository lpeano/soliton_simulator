# -*- coding: utf-8 -*-
r"""**S3bis: LA PROVA DELL'ENERGIA DI `chi` RIFATTA, VEDENTE** *([M2357-V3-S3bis]: la nota del guardiano delle `01:35`, il promemoria delle `01:55`; la carta `doc/TASK_HISTORY/2026-11-21_lorentz_locale.md`, sez. `5`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_s3bis.py tutte > doc/referti_l2/chi_v2_s3bis.txt

**(a) `chi` DA SOLO** sul toro `48` *(la sorgente gaussiana fissa, ampiezza e larghezza dal mattone a C2 `k 3000`; `chi = pi = 0`; `2000` tick col passo v2)*: `H` con `pi^2 / 2f` contro `H` con `pi^2 / 2`. **(b) IL BILANCIO DEL SETTORE `chi` SUL MATTONE:** la corsa di `chi_mattone_v3.corsa` *(la scena di S3)* con una COPIA riga per riga di `chi_tick_v2.tick_chi_v2` che registra le due forze; `DH_chi` di ogni tick contro il lavoro `W`; lo stato a `k 250` AL BIT contro la corsa S3 col passo v2. **Le definizioni sono quelle della carta, sez. `5.1`; l'energia discreta del salto di rana e' un'aggiunta dichiarata (sez. `5.2`), non un criterio.**
"""
import json
import math
import os
import shutil
import sys
import types

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import chi_mattone_v3 as CMV3  # noqa: E402
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402
import chi_parametri_v2 as CP2  # noqa: E402

DIR_B = os.path.join(CMV3.DIR_PROVA, "s3bis_b")
RIF_B = os.path.join(CMV3.DIR_PROVA, "s3_v2", "stato_00250.npz")
REG = []


# ====================================================================== (a)
def sorgente_dal_mattone():
    """### `(A, sigma, m0, m0 del meta, r_1/2, i profili)` dalla scena di `chi_mattone_v3.corsa` a `k 0` *(prepara di C2)*."""
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    from solitone import toro as TO
    MT, CV = PS.MT, PS.CV
    PS.presidi()
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        s = float(Z["s"])
        C0 = PS.PO.campi(Z, rho_c, e)
        e0 = float(C0.e0)
        P, m0p = CV2.parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, "C2")
        _C, _meta = CSB.prepara(Z, 186, False, rho_c, e, t0)
        c = MT.centro_di(Z, MT.rho_di(Z))
        u = CT.u_di(mot, Z["st"], Z["par"], s, e0)
        r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"]).T[:2])
        Z["metti"]()
    m0 = float(np.mean(u))
    c0n = int(np.argmin(r))
    A = float(u[c0n] - m0)
    prof = [A]
    R = 1
    while True:
        w = (r >= R - 0.5) & (r < R + 0.5)
        y = float(np.mean(u[w] - m0))
        prof.append(y)
        if y / A <= 0.5:
            break
        R += 1
        assert R < 80, "nessuna meta' altezza entro 80 archi"
    y1, y2 = prof[R - 1] / A, prof[R] / A
    rm = (R - 1) + (y1 - 0.5) / (y1 - y2)
    sigma = rm / math.sqrt(2.0 * math.log(2.0))
    return A, sigma, m0, m0p, rm, prof, P, float(r[c0n]), [float(x) for x in c]


def a():
    import lorentz_velocita as LV
    print("=" * 130)
    print("(a) CHI DA SOLO SUL TORO 48 (la carta sez. 5.1): la sorgente gaussiana fissa dal mattone, chi = pi = 0, 2000 tick col passo v2")
    print("=" * 130)
    A, sigma, m0, m0p, rm, prof, P, rc, cen = sorgente_dal_mattone()
    print("### la sorgente dal mattone (prepara di C2, k 0 della corsa con chi): il centro della materia %s, il nodo centrale a r %.3f; m0 = media(u) %+.12e (m0 dei parametri v2 %+.12e: %s)" % (
        cen, rc, m0, m0p, "AL BIT" if m0 == m0p else "### DIVERSO, lo scarto %.1e" % abs(m0 - m0p)))
    print("### A = u(centro) - m0 = %+.12e; le medie per anelli di (u - m0) / A per R = 0..%d: %s" % (A, len(prof) - 1, ", ".join("%.4f" % (y / A) for y in prof)))
    print("### r_1/2 %.6f; sigma = r_1/2 / sqrt(2 ln 2) = %.6f" % (rm, sigma))
    L = 48
    ii, jj, _m1, _m2 = LV.toro(L)
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    Lp = CT.Laplaciano(types.SimpleNamespace(inc=types.SimpleNamespace(nodo=nodo, n=L * L)))
    pos = LV.posizioni(L)
    a1, a2 = LV.vettori()
    v0 = 24 * L + 24
    d = pos - pos[v0]
    r = np.min(np.stack([np.hypot(*(d + i * L * a1 + j * L * a2).T) for i in (-1, 0, 1) for j in (-1, 0, 1)]), axis=0)
    S = A * np.exp(-r * r / (2.0 * sigma * sigma))
    kappa, c2, m2 = CP2.KAPPA, P.c2, P.m2
    f = CV2.inerzia(0.15, c2)
    c0 = kappa * float(np.mean(S))
    print("### il toro 48 (n %d, archi %d); S max %+.6e al nodo (24, 24), min %+.6e; kappa %r, c2 %r, m2 %r, f %r, c0 = kappa media(S) %+.12e; dt 1" % (L * L, len(ii), S.max(), S.min(), kappa, c2, m2, f, c0))

    def forza(x):
        return c2 * Lp.delta(x) - m2 * x + kappa * np.exp(-kappa * x) * S - c0

    def pezzi(x, p, F):
        dch = x[Lp.ii] - x[Lp.jj]
        K = 0.5 * float(np.sum(p * p)) / f
        U = 0.5 * c2 * float(np.sum(dch * dch)) + 0.5 * m2 * float(np.sum(x * x)) + c0 * float(np.sum(x)) + float(np.sum(S * np.expm1(-kappa * x)))
        return K, U, float(np.sum(F * F))

    x = np.zeros(L * L)
    p = np.zeros(L * L)
    Fa = forza(x)
    K, U, F2 = pezzi(x, p, Fa)
    serie = [(0, K, U, F2)]
    for t in range(1, 2001):
        p += 0.5 * f * Fa
        x += 0.5 * p
        x += 0.5 * p
        Fb = forza(x)
        p += 0.5 * f * Fb
        Fa = Fb
        serie.append((t,) + pezzi(x, p, Fa))
    T = np.array([q[0] for q in serie])
    K = np.array([q[1] for q in serie])
    U = np.array([q[2] for q in serie])
    F2 = np.array([q[3] for q in serie])
    H = K + U
    Hv = f * K + U
    Ht = H - (f / 8.0) * F2
    Es = float(K.max())
    dH = float(np.max(np.abs(H - H[0]))) / Es
    dHv = float(np.max(np.abs(Hv - Hv[0]))) / Es
    dHt = float(np.max(np.abs(Ht - Ht[0]))) / Es
    fr = float(K.max()) / float(np.max(np.abs(U)))
    print("### E* = max K %.12e (al tick %d); max |U| %.12e; la frazione cinetica max K / max |U| %.4f; max chi %.6e, kappa max chi %.3e" % (Es, int(T[np.argmax(K)]), float(np.max(np.abs(U))), fr, float(np.max(np.abs(x))), kappa * float(np.max(np.abs(x)))))
    print("### max |H - H(0)| / E*: con pi^2/2f %.3e; con pi^2/2 (la vecchia) %.3e; L'AGGIUNTA MIA, l'energia discreta H - (f/8) somma F^2: %.3e" % (dH, dHv, dHt))
    print("### solo illustrazione: max |H - H(0)| / somma S (la diluizione evitata togliendo la costante) %.3e" % (float(np.max(np.abs(H - H[0]))) / abs(float(np.sum(S)))))
    for t in (0, 1, 2, 5, 10, 50, 100, 200, 500, 1000, 1500, 2000):
        print("    t %4d: K %+.12e  U %+.12e  H %+.6e  H vecchia %+.6e  H discreta %+.6e" % (t, K[t], U[t], H[t] - H[0], Hv[t] - Hv[0], Ht[t] - Ht[0]))
    CMV3.esito("(a) PASSA se max |H - H(0)| / E* <= 1e-9 (pi^2/2f, il criterio del mandato)", dH <= 1e-9, "%.3e" % dH)
    CMV3.esito("(a) DEVE FALLIRE: con pi^2/2 max |H - H(0)| / E* >= 1e-2", dHv >= 1e-2, "%.3e" % dHv)
    CMV3.esito("(a) la frazione cinetica max K / max |U| >= 0.1", fr >= 0.1, "%.4f" % fr)
    print("    (non un criterio: l'energia discreta del salto di rana, la carta sez. 5.2: %.3e)" % dHt)


# ====================================================================== (b)
def tick_registrato(z, campo, P, Lp, X):
    """### `chi_tick_v2.tick_chi_v2` RIGA PER RIGA, con le due forze conservate e il bilancio del tick in `REG`."""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = z["mot"], z["st"], z["par"]
    dt = float(mot.dtau[0])
    assert np.all(mot.dtau == mot.dtau[0]), "dtau non uniforme: il salto di rana di chi vuole un dtau solo"
    chi_a, pi_a = X["chi"].copy(), X["pi"].copy()
    campo.spinta(0.5)
    Fa = CT.forza(mot, st, par, P, Lp, X["chi"])
    X["pi"] += (0.5 * dt * P.f) * Fa
    X["chi"] += (0.5 * dt) * X["pi"]
    N = np.exp(-P.kappa * X["chi"])
    mot.cs = P.s * N
    mot.lambda_c = None
    CT.fase_a(mot, st, P.e0, N)
    with UO.avvolto(mot, campo, True):
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    CT.fase_a(mot, st, P.e0, N)
    d = np.asarray(mot.dtau, dtype=float) * np.asarray(mot.cs, dtype=float)
    nodo = np.asarray(mot.inc.nodo)
    X["theta_a"] += math.pi * (d[nodo[0::2]] - d[nodo[1::2]])
    X["chi"] += (0.5 * dt) * X["pi"]
    Fb = CT.forza(mot, st, par, P, Lp, X["chi"])
    X["pi"] += (0.5 * dt * P.f) * Fb
    campo.spinta(0.5)
    REG.append(bilancio(chi_a, pi_a, X["chi"], X["pi"], Fa, Fb, P, Lp, dt))


def bilancio(chi_a, pi_a, chi_b, pi_b, Fa, Fb, P, Lp, dt):
    f = P.f
    Ga = Fa - (P.c2 * Lp.delta(chi_a) - P.m2 * chi_a - P.c0)
    Gb = Fb - (P.c2 * Lp.delta(chi_b) - P.m2 * chi_b - P.c0)
    dchi = chi_b - chi_a
    W = float(np.sum(dchi * 0.5 * (Ga + Gb)))
    dK = float(np.sum((pi_b - pi_a) * (pi_b + pi_a))) / (2.0 * f)
    da, db = chi_a[Lp.ii] - chi_a[Lp.jj], chi_b[Lp.ii] - chi_b[Lp.jj]
    dU = 0.5 * P.c2 * float(np.sum((db - da) * (db + da))) + 0.5 * P.m2 * float(np.sum(dchi * (chi_b + chi_a))) + P.c0 * float(np.sum(dchi))
    Cd = (dt * dt * f / 8.0) * (float(np.sum(Fb * Fb)) - float(np.sum(Fa * Fa)))
    return {"W": W, "dH": dK + dU, "dHv": f * dK + dU, "C": Cd, "dK": dK}


def b():
    print("=" * 130)
    print("(b) IL BILANCIO DEL SETTORE CHI SUL MATTONE (la carta sez. 5.1): la corsa di S3 col tick registrato, 250 tick da k 0 (C2 k 3000); il bilancio sui tick 1-200")
    print("=" * 130)
    if os.path.isdir(DIR_B):
        shutil.rmtree(DIR_B)
    CV2.tick_chi_v2 = tick_registrato                                   # ### la COPIA registrata al posto del tick v2, SOLO in questo processo
    _k, _fin, _s = CMV3.corsa(250, None, DIR_B)
    f_mio = os.path.join(DIR_B, "stato_00250.npz")
    assert open(RIF_B + ".sha1", encoding="utf-8").read().split()[0] == CMV3.CM.sha1(RIF_B), "lo sha1 del riferimento %s NON coincide" % RIF_B
    with np.load(f_mio) as d1, np.load(RIF_B) as d2:
        k1, k2 = sorted(d1.files), sorted(d2.files)
        diverse = [q for q in k1 if q != "meta" and not np.array_equal(d1[q], d2[q])]
        m1, m2 = json.loads(str(d1["meta"])), json.loads(str(d2["meta"]))
    al_bit = k1 == k2 and not diverse
    print("### lo stato a k 250 col tick registrato contro %s (sha1 %s): le chiavi %s; %s; il meta %s" % (
        os.path.relpath(RIF_B, CMV3.DIR_PROVA), CMV3.CM.sha1(RIF_B)[:8], "uguali" if k1 == k2 else "### DIVERSE", "AL BIT su %d chiavi" % (len(k1) - 1) if not diverse else "### DIVERSE: %s" % diverse, "uguale" if m1 == m2 else "### diverso"))
    CMV3.esito("(b) la copia del tick e' la stessa dinamica: lo stato a k 250 AL BIT con la corsa S3 v2", al_bit)
    B = REG[:200]
    W = np.array([q["W"] for q in B])
    dH = np.array([q["dH"] for q in B])
    dHv = np.array([q["dHv"] for q in B])
    Cd = np.array([q["C"] for q in B])
    R, Rv, Rt = dH - W, dHv - W, dH - W - Cd
    rw = float(np.sqrt(np.mean(W * W)))
    r1, rv1, rt1 = (float(np.max(np.abs(x) / np.abs(W))) for x in (R, Rv, Rt))
    print("### %d tick registrati (il bilancio sui primi 200); |W|: min %.3e, mediana %.3e, max %.3e, rms %.3e; i cambi di segno di W %d" % (
        len(REG), float(np.min(np.abs(W))), float(np.median(np.abs(W))), float(np.max(np.abs(W))), rw, int(np.sum(np.sign(W[1:]) != np.sign(W[:-1])))))
    print("### max |R| / |W| per tick: con pi^2/2f %.3e; con pi^2/2 %.3e; L'AGGIUNTA MIA, R meno il termine discreto (dt^2 f / 8) D somma F^2: %.3e" % (r1, rv1, rt1))
    print("### con rms(W) al denominatore: max |R| %.3e; max |R vecchio| %.3e; max |R - C| %.3e" % (float(np.max(np.abs(R))) / rw, float(np.max(np.abs(Rv))) / rw, float(np.max(np.abs(Rt))) / rw))
    for t in (1, 2, 5, 10, 50, 100, 150, 200):
        q = B[t - 1]
        print("    tick %3d: W %+.6e  DH_chi %+.6e  R %+.3e  R vecchio %+.3e  il termine discreto %+.3e  R - termine %+.3e" % (t, q["W"], q["dH"], q["dH"] - q["W"], q["dHv"] - q["W"], q["C"], q["dH"] - q["W"] - q["C"]))
    CMV3.esito("(b) PASSA se max |R| / |W| <= 1e-6 per tick (pi^2/2f, il criterio del mandato)", r1 <= 1e-6, "%.3e" % r1)
    CMV3.esito("(b) DEVE FALLIRE: con pi^2/2 il residuo almeno 10 volte piu' grande", rv1 >= 10.0 * r1, "%.3e contro %.3e" % (rv1, r1))
    print("    (non un criterio: il residuo meno il termine discreto del salto di rana, la carta sez. 5.2: %.3e)" % rt1)


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "chi_mattone_v3.py"))
    _presidio.avvia(__file__)
    assert sys.argv[1:] == ["tutte"], "il comando: chi_s3bis.py tutte"
    a()
    b()
    return CMV3.fine()


if __name__ == "__main__":
    sys.exit(main())
