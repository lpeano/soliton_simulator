# -*- coding: utf-8 -*-
r"""**L1 DEL LORENTZ LOCALE: LE TRE VELOCITA' LIMITE DALLE FORMULE** *(il mandato di Luca `2026-11-21` sera; la carta `doc/TASK_HISTORY/2026-11-21_lorentz_locale.md`, sez. `2.2`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lorentz_velocita.py luce > doc/referti_l2/lorentz_velocita_luce.txt
    E:\python\py3132\python.exe doc/referti_l2/lorentz_velocita.py chi > doc/referti_l2/lorentz_velocita_chi.txt
    E:\python\py3132\python.exe doc/referti_l2/lorentz_velocita.py materia > doc/referti_l2/lorentz_velocita_materia.txt
    E:\python\py3132\python.exe doc/referti_l2/lorentz_velocita.py tabella > doc/referti_l2/lorentz_velocita.txt

**Le unita':** la distanza in ARCHI *(`a1`, `a2` di `toro.vettori`: il lato `1`)*, il tempo in TICK; **in tempo proprio: diviso `cs`.** Ogni settore scrive `doc/referti_l2/lorentz_velocita_<settore>.json`; **`tabella` li legge** *(nessun numero ricopiato)*.
**`luce`:** `s_a` del campo COME LO COSTRUISCE LA CORSA *(lo stato `k 3000` della corsa con `chi`, `controllo_senza_bordo.riprendi` -> `porto.campi`)*; il leapfrog del campo *(`spinta 1/2`, `deriva 1/2 + 1/2`, `spinta 1/2`)* e' `A(t+1) - 2 A(t) + A(t-1) = - (w/AREA) C^T C A(t)` *(il non compatto; il compatto a piccola ampiezza e' lo stesso)*, quindi **`cos omega = 1 - Omega^2/2`, `Omega^2 = (w/AREA) lambda(C^T C)_k`**; `lambda_k` dalla matrice di Bloch `3 x 3` *(lo stencil di `C^T C` sul toro `12 x 12`)*. **IL CASO NOTO PRIMA:** un'onda stazionaria del solo campo *(`_u1_prototipo.Campo`, `tick_campo`, toro `48 x 48`, `400` tick)*: `omega` misurata *(`cos omega = (c_{t+1} + c_{t-1}) / (2 c_t)`, la mediana)* = la formula entro `1e-6` relativo; **DEVE FALLIRE** la formula senza l'`AREA`. Poi `v = omega/|k|` e `v_g` a `|k|` piccoli, a `0`, `15`, `30` gradi.
**`chi`:** `lambda(k) = 2 somma_j (1 - cos k.e_j)` *(`e_j` = `a1`, `a2`, `a1 + a2`)*, `cos omega = 1 - (c2 lambda + m2)/2`; **IL CASO NOTO PRIMA:** un'onda stazionaria del solo `chi` *(il leapfrog di `tick_chi` con la sola forza `c2 Delta chi - m2 chi`, `chi_tick.Laplaciano` sul toro `48 x 48`, `400` tick)*, `m2 = 0` e `m2` della corsa, entro `1e-10`; **DEVE FALLIRE** `lambda` con due direzioni sole. Poi la pendenza senza massa e `v_g` con la massa.
**`materia`:** **IL CASO NOTO PRIMA: E1-R** *(`_triangoli_forza.v_max(matrice_L(0.5, 0.15))/0.15 = 0.588137` entro `1e-6`; DEVE FALLIRE contro `0.601963`, il valore a `eps 0`)*; poi `v_max(theta)` *(Hellmann-Feynman come `v_max`, proiettata su `theta`)* a `0`, `15`, `30` gradi; `|v_g|` vicino a `Gamma` sul ramo piu' basso; e `v_max` a `s' = s N(centro)` *(`N` dallo stato piu' recente della corsa con `chi`, il nodo del centro)*.
"""
import json
import math
import os
import sys
import types

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT  # noqa: E402

DIR_M = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "mattone")
F3 = os.path.join(DIR_M, "stato_03000.npz")
S_CORSA, EPS_CORSA = 0.15, 0.5
RIF_E1, RIF_EPS0 = 0.588137, 0.601963
THETA = (0.0, 15.0, 30.0)
KK = (1e-2, 1e-3, 1e-4)
L_ST, L_ONDA, T_ONDA = 12, 48, 400
PARTE_G = 0.99356                  # ### doc/referti_l2/u1_prototipo.txt, PARTE G: v/cs medio (la prova di proporzionalita' FALLITA: 1.14e-01)
OK = []


def esito(che, passa, nota=""):
    OK.append((che, bool(passa)))
    print("  %-118s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))


def vettori():
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    return np.asarray(A1, dtype=float)[:2], np.asarray(A2, dtype=float)[:2]


def toro(L):
    """### gli archi `3 v + a` da `v = m1 L + m2` verso `a1`, `a2`, `a1 + a2` *(come `mitosi_film.toro`)*; le posizioni di reticolo."""
    v = np.arange(L * L)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    return np.repeat(v, 3), np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1), m1, m2


def posizioni(L):
    a1, a2 = vettori()
    _ii, _jj, m1, m2 = toro(L)
    return m1[:, None] * a1 + m2[:, None] * a2


def k_griglia(n1, n2, L):
    """### `k` con `k . a1 = 2 pi n1 / L`, `k . a2 = 2 pi n2 / L`."""
    a1, a2 = vettori()
    A = np.array([a1, a2])
    return np.linalg.solve(A, 2.0 * np.pi * np.array([n1, n2], dtype=float) / L)


def scrivi(nome, D):
    with open(os.path.join(_QUI, "lorentz_velocita_%s.json" % nome), "w", encoding="utf-8") as fh:
        json.dump(D, fh, indent=1)


def leggi(nome):
    with open(os.path.join(_QUI, "lorentz_velocita_%s.json" % nome), encoding="utf-8") as fh:
        return json.load(fh)


def misura_omega(serie):
    c = np.asarray(serie)
    sel = np.nonzero(np.abs(c[1:-1]) > 0.1 * np.max(np.abs(c)))[0] + 1
    cw = (c[sel + 1] + c[sel - 1]) / (2.0 * c[sel])
    return float(np.arccos(np.clip(np.median(cw), -1.0, 1.0))), float(np.max(cw) - np.min(cw))


# ------------------------------------------------------------------------------------------ la luce
def stencil_CtC(L, s_a):
    import _u1_prototipo as U1
    ii, jj, m1, m2 = toro(L)
    c = U1.Campo(ii, jj, (L, L), 1.0, "noncompatto", np.full(len(ii), s_a))
    C = c.matrice_rot()
    M = C.T @ C
    a1, a2 = vettori()
    st = []
    for a in range(3):
        for q in np.nonzero(M[a])[0]:
            v, b = int(q) // 3, int(q) % 3
            d1 = ((v // L) + L // 2) % L - L // 2
            d2 = ((v % L) + L // 2) % L - L // 2
            st.append((a, b, d1 * a1 + d2 * a2, float(M[a, q])))
    return st, c


def Mk(st, k):
    M = np.zeros((3, 3), dtype=complex)
    for a, b, R, val in st:
        M[a, b] += val * np.exp(1j * float(k @ R))
    return M


def fotone(st, k, w, area):
    lam = np.sort(np.linalg.eigvalsh(0.5 * (Mk(st, k) + Mk(st, k).conj().T)))
    gauge = lam[0]
    lam_f = lam[1]                                      # ### il ramo che va a zero (il fotone); lam[2] l'ottico
    Om2 = w * lam_f / area
    return math.acos(1.0 - 0.5 * Om2), gauge, lam


def luce():
    import _presidio
    import _u1_prototipo as U1
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    MT = PS.MT
    PS.presidi()
    print("=" * 140)
    print("L1 (b), LA LUCE U(1) (la carta sez. 2.2): s_a del campo della corsa, il leapfrog per k, il caso noto dell'onda stazionaria")
    print("=" * 140)
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, meta, cs, sh = CSB.riprendi(Z, F3, False, MT.rho_c_assoluto(), MT.PB.E_DECISO)
        s_a = np.asarray(C.campo.s_a, dtype=float)
        forma = C.campo.forma
        w_c = np.asarray(C.campo.w, dtype=float)
        print("### il campo della corsa (ripreso da %s come la corsa lo costruisce): forma %s; s_a uniforme %s, %r .. %r; w %r .. %r; mot.cs alla costruzione %s; L_SU_LS %r, AREA %r" % (
            os.path.basename(F3), forma, bool(np.all(s_a == s_a[0])), float(s_a.min()), float(s_a.max()), float(w_c.min()), float(w_c.max()), "None" if Z["mot"].cs is None else "presente", U1.L_SU_LS, U1.AREA))
        Z["metti"]()
    s0 = float(s_a[0])
    st, c12 = stencil_CtC(L_ST, s0)
    w = float(c12.w[0])
    # ### IL CASO NOTO: l'onda stazionaria
    ii, jj, m1, m2 = toro(L_ONDA)
    c48 = U1.Campo(ii, jj, (L_ONDA, L_ONDA), 1.0, "noncompatto", np.full(len(ii), s0))
    assert np.array_equal(c48.ii, ii) and np.array_equal(c48.jj, jj), "il campo non ha gli archi 3 v + a"
    k = k_griglia(1, 0, L_ONDA)
    om_f, gauge, lam = fotone(st, k, w, U1.AREA)
    lv, V = np.linalg.eigh(0.5 * (Mk(st, k) + Mk(st, k).conj().T))
    vec = V[:, 1]
    r = posizioni(L_ONDA)
    fase = np.exp(1j * (r @ k))
    modo = np.real(np.repeat(fase, 3) * np.tile(vec, L_ONDA * L_ONDA))
    c48.A[...] = 1e-3 * modo
    c48.E[...] = 0.0
    serie = []
    for _t in range(T_ONDA + 1):
        if _t:
            U1.tick_campo(c48)
        serie.append(float(c48.A @ modo) / float(modo @ modo))
    om_m, sp = misura_omega(serie)
    err = abs(om_m - om_f) / om_f
    om_falsa = math.acos(1.0 - 0.5 * w * lam[1])
    print("### IL CASO NOTO: l'onda stazionaria del fotone sul toro %dx%d, k (1, 0) |k| %.6f, %d tick: omega misurata %.12f, formula %.12f (lo scarto %.1e; la dispersione delle stime %.1e); il modo di gauge lambda %.1e" % (
        L_ONDA, L_ONDA, float(np.linalg.norm(k)), T_ONDA, om_m, om_f, err, sp, gauge))
    esito("CASO NOTO: omega dell'onda stazionaria = la formula del leapfrog entro 1e-6 relativo", err <= 1e-6, "%.1e" % err)
    esito("DEVE FALLIRE: la formula senza l'AREA (omega %.6f)" % om_falsa, abs(om_m - om_falsa) / om_m > 1e-3, "%.1e" % (abs(om_m - om_falsa) / om_m))
    if not all(p for _c, p in OK):
        print("### il caso noto non passa: niente velocita' in tabella")
        return 1
    out = {"s_a": s0, "w": w, "forma": forma, "area": U1.AREA, "theta": {}}
    print("### LA VELOCITA' DEL FOTONE (archi per tick), v = omega/|k| e v_g = d omega/d|k|:")
    for th in THETA:
        d = np.array([math.cos(math.radians(th)), math.sin(math.radians(th))])
        righe = []
        for kk in KK:
            om, _g, _l = fotone(st, kk * d, w, U1.AREA)
            h = kk * 1e-3
            vg = (fotone(st, (kk + h) * d, w, U1.AREA)[0] - fotone(st, (kk - h) * d, w, U1.AREA)[0]) / (2 * h)
            righe.append((kk, om / kk, vg))
        out["theta"][str(th)] = {"v": righe[-1][1], "v_g": righe[-1][2], "v_su_s_a": righe[-1][1] / s0}
        print("  theta %4.1f: %s" % (th, "; ".join("|k| %.0e: v %.10f, v_g %.10f (v/s_a %.8f)" % (kk, v_, g_, v_ / s0) for kk, v_, g_ in righe)))
    vs = [out["theta"][str(t)]["v"] for t in THETA]
    out["v_luce"] = vs[0]
    out["anisotropia"] = (max(vs) - min(vs)) / float(np.mean(vs))
    print("### v_luce a k -> 0: %.10f archi per tick = %.8f s_a; l'anisotropia (0, 15, 30 gradi) %.1e; la parte G (un pacchetto a k finito, cs variabile) dava v/cs medio %.5f" % (
        out["v_luce"], out["v_luce"] / s0, out["anisotropia"], PARTE_G))
    vero = abs(out["v_luce"] / s0 - 1.0) <= 0.02
    print("### P-L2 (v_luce/s_a a k -> 0 entro 0.02 da 1): %s (%.6f)" % ("VERA" if vero else "FALSA", out["v_luce"] / s0))
    out["P_L2"] = vero
    scrivi("luce", out)
    print("=" * 140)
    return 0


# ------------------------------------------------------------------------------------------ chi
def lam_chi(k, dirs):
    return float(sum(2.0 * (1.0 - math.cos(float(k @ e))) for e in dirs))


def omega_chi(k, c2, m2, dirs):
    return math.acos(1.0 - 0.5 * (c2 * lam_chi(k, dirs) + m2))


def chi():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    a1, a2 = vettori()
    dirs = (a1, a2, a1 + a2)
    c2, m2c = CT.C_CHI ** 2, (1.0 / CT.PORTATA) ** 2
    print("=" * 140)
    print("L1 (c), CHI (la carta sez. 2.2): c2 %r, m2 %r (la corsa), il Laplaciano L = D D^T del triangolare, il leapfrog di tick_chi" % (c2, m2c))
    print("=" * 140)
    ii, jj, m1, m2_ = toro(L_ONDA)
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    Lp = CT.Laplaciano(types.SimpleNamespace(inc=types.SimpleNamespace(nodo=nodo, n=L_ONDA * L_ONDA)))
    r = posizioni(L_ONDA)
    k = k_griglia(1, 0, L_ONDA)
    for m2 in (0.0, m2c):
        x = np.cos(r @ k)
        p = np.zeros_like(x)
        serie = []
        for _t in range(T_ONDA + 1):
            if _t:
                p += 0.5 * (c2 * Lp.delta(x) - m2 * x)
                x += 0.5 * p
                x += 0.5 * p
                p += 0.5 * (c2 * Lp.delta(x) - m2 * x)
            serie.append(float(x @ np.cos(r @ k)) / float(np.cos(r @ k) @ np.cos(r @ k)))
        om_m, sp = misura_omega(serie)
        om_f = omega_chi(k, c2, m2, dirs)
        om_2 = omega_chi(k, c2, m2, dirs[:2])
        err = abs(om_m - om_f) / om_f
        print("### IL CASO NOTO (m2 %r): l'onda stazionaria di chi sul toro %dx%d, k (1, 0), %d tick: omega misurata %.14f, formula %.14f (lo scarto %.1e; la dispersione %.1e)" % (
            m2, L_ONDA, L_ONDA, T_ONDA, om_m, om_f, err, sp))
        esito("CASO NOTO (m2 %r): omega dell'onda stazionaria di chi = la formula entro 1e-10" % m2, err <= 1e-10, "%.1e" % err)
        esito("DEVE FALLIRE (m2 %r): lambda con due direzioni sole (omega %.6f)" % (m2, om_2), abs(om_m - om_2) / om_m > 1e-3, "%.1e" % (abs(om_m - om_2) / om_m))
    if not all(p for _c, p in OK):
        print("### il caso noto non passa: niente velocita' in tabella")
        return 1
    out = {"c2": c2, "m2": m2c, "theta": {}}
    print("### LA VELOCITA' DI CHI (archi per tick): senza massa v = omega/|k|; con la massa v_g = d omega/d|k|:")
    for th in THETA:
        d = np.array([math.cos(math.radians(th)), math.sin(math.radians(th))])
        righe = []
        for kk in KK:
            v0 = omega_chi(kk * d, c2, 0.0, dirs) / kk
            h = kk * 1e-3
            vg = (omega_chi((kk + h) * d, c2, m2c, dirs) - omega_chi((kk - h) * d, c2, m2c, dirs)) / (2 * h)
            righe.append((kk, v0, vg))
        out["theta"][str(th)] = {"v_senza_massa": righe[-1][1], "v_g_con_massa": righe[-1][2], "v_g_con_massa_1e-2": righe[0][2]}
        print("  theta %4.1f: %s" % (th, "; ".join("|k| %.0e: senza massa %.10f, v_g con m2 %.3e" % (kk, v_, g_) for kk, v_, g_ in righe)))
    vs = [out["theta"][str(t)]["v_senza_massa"] for t in THETA]
    out["v_chi"] = vs[0]
    out["c_sqrt_3_2"] = math.sqrt(c2 * 1.5)
    out["anisotropia"] = (max(vs) - min(vs)) / float(np.mean(vs))
    print("### v_chi senza massa a k -> 0: %.10f archi per tick (c sqrt(3/2) = %.10f); l'anisotropia %.1e; con la massa v_g -> 0 a k -> 0 (portata 1/m = %g archi)" % (
        out["v_chi"], out["c_sqrt_3_2"], out["anisotropia"], CT.PORTATA))
    scrivi("chi", out)
    print("=" * 140)
    return 0


# ------------------------------------------------------------------------------------------ la materia
def v_max_dir(A, thetas):
    """### `_triangoli_forza.v_max` riga per riga, ma la velocita' PROIETTATA su `theta` *(il massimo con segno su `k` e sulle bande)*."""
    import _triangoli_forza as TF
    B = A[:, :, :TF.NB, :TF.NB]
    n = B.shape[0]
    AR = np.fft.ifft2(B, axes=(0, 1))
    m = np.arange(n)
    m = np.where(m > n // 2, m - n, m).astype(float)
    D1 = np.fft.fft2(AR * (-1j * m)[:, None, None, None], axes=(0, 1))
    D2 = np.fft.fft2(AR * (-1j * m)[None, :, None, None], axes=(0, 1))
    a1, a2 = np.array([1.0, 0.0]), np.array([-0.5, math.sqrt(3.0) / 2.0])
    dirs = [np.array([math.cos(math.radians(t)), math.sin(math.radians(t))]) for t in thetas]
    lam, V = np.linalg.eig(B)
    best = [0.0] * len(dirs)
    for i in range(n):
        for j in range(n):
            lv, vv = lam[i, j], V[i, j]
            usato = np.zeros(TF.NB, dtype=bool)
            for b in range(TF.NB):
                if usato[b]:
                    continue
                cl = [c for c in range(TF.NB) if not usato[c] and abs(lv[c] - lv[b]) < TF.TOLL_DEG]
                usato[cl] = True
                Q, _ = np.linalg.qr(vv[:, cl])
                M1 = 1j * np.conj(lv[b]) * (Q.conj().T @ D1[i, j] @ Q)
                M2 = 1j * np.conj(lv[b]) * (Q.conj().T @ D2[i, j] @ Q)
                for q, d in enumerate(dirs):
                    Mn = (d @ a1) * M1 + (d @ a2) * M2
                    best[q] = max(best[q], float(np.max(np.linalg.eigvalsh(0.5 * (Mn + Mn.conj().T)))))
    return best


def n_centro():
    import glob
    from solitone import toro as TO
    fs = sorted((f for f in glob.glob(os.path.join(DIR_M, "stato_*.npz")) if os.path.exists(f + ".sha1")), key=lambda f: int(os.path.basename(f)[6:-4]))
    f = fs[-1]
    import hashlib
    with open(f, "rb") as fh:
        assert hashlib.sha1(fh.read()).hexdigest() == open(f + ".sha1", encoding="utf-8").read().split()[0]
    with np.load(f) as d:
        meta = json.loads(str(d["meta"]))
        chi_ = d["chi"].copy()
    _ii, _jj, m1, m2 = toro(186)
    r = np.hypot(*TO.scarti(m1.astype(float), m2.astype(float), meta["centro"][0], meta["centro"][1], 186).T[:2])
    c0n = int(np.argmin(r))
    kappa = float(meta["parametri"]["kappa"])
    return os.path.basename(f), int(meta["k"]), c0n, float(chi_[c0n]), math.exp(-kappa * float(chi_[c0n]))


def materia():
    import _presidio
    import _triangoli_forza as TF
    _presidio.avvia(__file__)
    print("=" * 140)
    print("L1 (a), LA MATERIA (la carta sez. 2.2): la matrice di Bloch del passo a cs = s uniforme (_triangoli_bassa_energia.matrice, eps %g, lato %d), Hellmann-Feynman" % (EPS_CORSA, TF.L))
    print("=" * 140)
    A = TF.matrice_L(EPS_CORSA, S_CORSA)
    v0, dove, fase = TF.v_max(A)
    e1 = v0 / S_CORSA
    print("### IL CASO NOTO E1-R: v_max/s a eps %g, s %g: %.8f (in %s, la fase %.6f) contro %.6f" % (EPS_CORSA, S_CORSA, e1, dove, fase, RIF_E1))
    esito("CASO NOTO E1-R: v_max/s = %.6f entro 1e-6" % RIF_E1, abs(e1 - RIF_E1) <= 1e-6, "%.8f" % e1)
    esito("DEVE FALLIRE: contro %.6f (eps 0) entro 1e-6" % RIF_EPS0, abs(e1 - RIF_EPS0) > 1e-6, "%.1e" % abs(e1 - RIF_EPS0))
    if not all(p for _c, p in OK):
        print("### il caso noto non passa: niente velocita' in tabella")
        return 1
    vd = v_max_dir(A, THETA)
    print("### v_max proiettata (archi per tick): %s; /s: %s; l'anisotropia %.2e" % (
        ", ".join("%g gradi %.8f" % (t, v) for t, v in zip(THETA, vd)), ", ".join("%.8f" % (v / S_CORSA) for v in vd), (max(vd) - min(vd)) / float(np.mean(vd))))
    # ### il ramo piu' basso vicino a Gamma: la banda con la fase piu' vicina a 0 a Gamma, la sua |v_g| al primo k della griglia
    B = A[:, :, :TF.NB, :TF.NB]
    lam0 = np.linalg.eigvals(B[0, 0])
    b0 = int(np.argmin(np.abs(np.angle(lam0))))
    print("### il ramo piu' basso a Gamma: la fase %.6f (per tick); la materia ha massa: v_g -> 0 a k -> 0 (la velocita' limite e' v_max, la carta sez. 1 punto 5)" % float(np.angle(lam0[b0])))
    f, k_st, c0n, chi_c, N_c = n_centro()
    s1 = S_CORSA * N_c
    A1 = TF.matrice_L(EPS_CORSA, s1)
    v1 = TF.v_max(A1)[0]
    print("### N AL CENTRO del mattone con chi: lo stato %s (k %d), il nodo %d, chi %.6f, N %.8f (1 - N %.4e); cs = s N = %.8f" % (f, k_st, c0n, chi_c, N_c, 1.0 - N_c, s1))
    print("### v_max a cs = s N: %.8f archi per tick, v_max/cs %.8f (al vuoto %.8f)" % (v1, v1 / s1, e1))
    out = {"s": S_CORSA, "eps": EPS_CORSA, "v_max": v0, "v_max_su_s": e1, "theta": dict(zip(map(str, THETA), vd)), "stato_N": f, "k_N": k_st, "nodo_centro": c0n, "chi_centro": chi_c,
           "N_centro": N_c, "s_centro": s1, "v_max_centro": v1, "v_max_su_cs_centro": v1 / s1}
    scrivi("materia", out)
    print("=" * 140)
    return 0


# ------------------------------------------------------------------------------------------ la tabella
def tabella():
    import _presidio
    _presidio.avvia(__file__)
    Lu, Ch, Ma = leggi("luce"), leggi("chi"), leggi("materia")
    s, sN, N = Ma["s"], Ma["s_centro"], Ma["N_centro"]
    print("=" * 140)
    print("L1, LA TABELLA DELLE TRE VELOCITA' (dai json di luce, chi, materia; la carta sez. 2.2)")
    print("=" * 140)
    righe = {"vuoto (cs = s = %.4f)" % s: (s, Ma["v_max"], Lu["v_luce"], Ch["v_chi"]),
             "centro (cs = s N = %.6f, N %.6f)" % (sN, N): (sN, Ma["v_max_centro"], Lu["v_luce"], Ch["v_chi"])}
    print("  %-38s %14s %14s %14s | %12s %12s %12s | %10s %10s" % ("", "materia", "luce", "chi", "mat/cs", "luce/cs", "chi/cs", "mat/luce", "chi/luce"))
    rap = {}
    for nome, (cs_, vm, vl, vc) in righe.items():
        print("  %-38s %14.10f %14.10f %14.10f | %12.8f %12.8f %12.8f | %10.6f %10.6f" % (nome, vm, vl, vc, vm / cs_, vl / cs_, vc / cs_, vm / vl, vc / vl))
        rap[nome] = (vm / vl, vc / vl, vm / cs_, vl / cs_, vc / cs_)
    print("  (archi per tick; /cs = archi per unita' di tempo proprio; la materia: v_max, la velocita' di gruppo massima; chi: la pendenza senza massa; la luce: il fotone a k -> 0)")
    (rm0, rc0, a0, b0, c0), (rm1, rc1, a1, b1, c1) = rap.values()
    print("### P-L3 (|v_materia/v_luce - 1| > 0.05 al vuoto): %s (%.6f)" % ("VERA" if abs(rm0 - 1.0) > 0.05 else "FALSA", rm0))
    print("### P-L4 (|v_chi/v_luce - 1| > 0.10): %s (%.6f)" % ("VERA" if abs(rc0 - 1.0) > 0.10 else "FALSA", rc0))
    d_rm = abs(rm1 / rm0 - 1.0)
    d_lu = abs(b1 / b0 - 1.0)
    print("### P-L5 (i rapporti in tempo proprio cambiano fra il vuoto e il centro fra 0.1 e 10 volte 1 - N = %.3e): materia/luce %.3e, luce/cs %.3e, chi/cs %.3e -> %s" % (
        1.0 - N, d_rm, d_lu, abs(c1 / c0 - 1.0), "VERA" if 0.1 * (1.0 - N) <= d_rm <= 10.0 * (1.0 - N) and d_rm > 0.0 else "FALSA"))
    print("### P-L2 (dalla luce): %s" % ("VERA" if Lu["P_L2"] else "FALSA"))
    print("=" * 140)
    return 0


def main(argv):
    quale = argv[0] if argv else ""
    f = {"luce": luce, "chi": chi, "materia": materia, "tabella": tabella}.get(quale)
    assert f is not None, "uso: lorentz_velocita.py luce | chi | materia | tabella"
    r = f()
    print("-" * 140)
    for che, p in OK:
        print("  %-118s %s" % (che, "PASSA" if p else "### FALLISCE"))
    return r if r else (0 if all(p for _c, p in OK) else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
