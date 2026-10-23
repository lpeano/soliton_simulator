r"""**I TRIANGOLI, SECONDO GRADINO: la forza sul modo a `K`** *(il toro rettangolare, la velocita' del cono, la corsa, l'universalita', la moneta e lo zero; solo in memoria;
[[DECISIONE-SOLO-TRIANGOLI]])*.

> ### ⛔ **Il task history e' `2026-10-23_triangoli_forza.md`** *(il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta, la convenzione nel repo e il nucleo
> intatti.** ### **Importati, non copiati:** `_triangoli` *(`scena_toro`, `toro_spostamenti`, `matrice_tick`, `scarto_c6`, `camminata`)*, `_triangoli_bassa_energia` *(`matrice`, `curvatura`,
> `continua`)*, `_forza_da_cs` *(`pacchetto`, `fit_moto`, `norma_fuori`, `nullo`)*, `_zero_simmetrico.convenzione_simmetrica`, `_universalita_massa.blob`.

### **0** *(gli strumenti, contro `8781162c` letto con `git show`, in memoria)* · ### **A** *(`v_max`, `v_fronte`, `v_fit`, e `a_H/a_RG` con ciascuna)* · ### **B** *(la corsa sui tori `A` e
`B`)* · ### **C** *(`lambda*`, la differenza delle `a_H` a `lambda = 1/2`, il centro della coppia)*.

Gira con:  python csv/_triangoli_forza.py > doc/referti_l2/triangoli_forza.txt
"""
import contextlib
import io
import json
import math
import os
import subprocess
import sys
import time
import types
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

RIF = "8781162c"                # ### il commit di riferimento della parte 0 e del primo gradino
L = 48
LF = 6
NB = 12
KL, KF = (16, 16), (2, 2)       # ### `K` al lato `L` e al lato `LF`
S_A = (0.05, 0.1, 0.3, 0.5)
EPS_AB = (0.0, 0.5)
EPS_C = (0.25, 0.5, 1.0)
L_FRONTE = 192                 # ### annotazione 1: a 64 il fronte a s 0.5 girava intorno al toro
DENTRO = 0.9
T_FRONTE = (50, 100)
SOGLIE = (1e-2, 1e-4, 1e-6)
LX = (96, 192)
LY = 6
LX_B = 96
ETA = (0.0, 1e-3, -1e-3, 1e-2, -1e-2)
ETA_B = (0.0, 1e-2, -1e-2)
CONV = ("simm", "oggi")
PERIODI = 10
PASSO_EPS = 0.05
TOLL_LIV = 1e-9
TOLL_DEG = 1e-7
DIREZIONI = 61
TOLL_BIT_SPETTRO = 1e-14
TOLL_C6 = 1e-12
TOLL_C6_UGUALE = 1e-14
TOLL_UNITA = 1e-3
TOLL_RIF = 1e-6
TOLL_CONV = 1e-10
TOLL_SPECCHIO = 0.05
TOLL_STESSA = 0.05
PUO1 = (0.9, 1.1)
PUO2 = (0.8, 1.2)
F_A = math.sqrt(3.0) / 2.0
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_forza.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-88s %s   %s" % (che[:88], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4f"):
    return "--" if x is None else fm % x


def av(x):
    return float((x + np.pi) % (2.0 * np.pi) - np.pi)


def conv(nome):
    import _zero_simmetrico as ZS
    return ZS.convenzione_simmetrica() if nome == "simm" else contextlib.nullcontext()


def tori():
    """### I due tori: ### **`A`** *(lati lungo `a1`, `a2`: il gradiente normale ad `a2`, a `30` gradi)*, ### **`B`** *(la base `a1`, `a2 - a1`: il gradiente normale ad `a2 - a1`, a `60`
    gradi, parallelo a un legame)*. ### **`f`: la distanza lungo il gradiente per unita' di `m1`.** ### **La fase di `K` per nodo: `K.a1 = K.a2 = 2 pi/3`.**"""
    import _triangoli as T
    return {"A": {"spost": T.TRIANGOLI[0], "f": F_A, "fase_K": lambda m1, m2: 2.0 * np.pi * (m1 + m2) / 3.0},
            "B": {"spost": ((1, 0), (1, 1), (2, 1)), "f": 0.5, "fase_K": lambda m1, m2: 2.0 * np.pi * m1 / 3.0}}


# =====================================================================================
#   PARTE 0 -- GLI STRUMENTI, CONTRO IL COMMIT DI RIFERIMENTO
# =====================================================================================
def modulo_al(rel, nome):
    """### Il modulo `rel` come era al commit `RIF`, ### **letto con `git show` ed eseguito in memoria** *(nessun file scritto)*."""
    src = subprocess.run(["git", "show", "%s:%s" % (RIF, rel)], capture_output=True, cwd=RADICE, check=True).stdout.decode("utf-8")
    m = types.ModuleType(nome)
    m.__file__ = os.path.join(RADICE, rel)
    exec(compile(src, m.__file__, "exec"), m.__dict__)
    return m


def byte_attr(o, pre=""):
    """### I BYTE di ogni attributo *(array: tipo, forma, byte; scalari: `repr`; oggetti: i loro attributi)*."""
    out = {}
    if isinstance(o, np.ndarray):
        out[pre] = (o.dtype.str, o.shape, o.tobytes())
    elif isinstance(o, dict):
        for k in sorted(o):
            out.update(byte_attr(o[k], pre + "/" + str(k)))
    elif isinstance(o, (int, float, str, bool, type(None))):
        out[pre] = repr(o)
    elif isinstance(o, (list, tuple)):
        for i, x in enumerate(o):
            out.update(byte_attr(x, pre + "[%d]" % i))
    elif hasattr(o, "__dict__"):
        for k in sorted(vars(o)):
            if k == "st":
                continue                        # ### lo stato e' confrontato a parte, nella tupla
            out.update(byte_attr(getattr(o, k), pre + "." + k))
    else:
        out[pre] = repr(type(o))
    return out


def parte_0():
    import _forza_da_cs as FC
    import _triangoli as T
    print("### PARTE 0 -- GLI STRUMENTI (il codice di %s letto con git show, in memoria)" % RIF)
    T0 = modulo_al("csv/_triangoli.py", "_triangoli_al_rif")
    diversi, n_attr = [], 0
    for g, nome in ((T.TRIANGOLI, "triangoli"), (T.QUADRATO, "quadrato")):
        a = byte_attr(list(T0.scena(g, 12, 0.3, T0.X)))
        b = byte_attr(list(T.scena_toro(g, (12, 12), 0.3, T.X)))
        n_attr += len(a)
        diversi += ["%s %s" % (nome, k) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    bit, dsp = True, 0.0
    for eps in (0.0, 0.5):
        v0, v1 = T0.EPS_MONETA, T.EPS_MONETA
        T0.EPS_MONETA = T.EPS_MONETA = eps
        try:
            for s in (0.1, 0.5):
                A0 = T0.matrice_tick(T0.TRIANGOLI, 12, s)
                A1 = T.matrice_tick(T.TRIANGOLI, 12, s)
                bit = bit and bool(np.array_equal(A0, A1))
                dsp = max(dsp, float(np.max(np.abs(np.sort_complex(np.linalg.eigvals(A0)) - np.sort_complex(np.linalg.eigvals(A1))))))
        finally:
            T0.EPS_MONETA, T.EPS_MONETA = v0, v1
    esito("DEVE PASSARE: a lati uguali la scena_toro = la scena di %s AL BIT (%d attributi, triangoli e quadrato)" % (RIF, n_attr), not diversi, "diversi: %s" % (diversi[:4] or "nessuno"))
    esito("DEVE PASSARE: matrice_tick uguale al bit, lo spettro a k uguali entro %g (eps 0, 0.5; s 0.1, 0.5; lato 12)" % TOLL_BIT_SPETTRO, bit and dsp <= TOLL_BIT_SPETTRO,
          "al bit %s, lo spettro %.1e" % (bit, dsp))
    import _triangoli_bassa_energia as BE
    giusti, sbagliati, peg_d, peg_n = 0, 0, 0.0, 0.0
    for eps in (0.0, 0.25, 0.5, 1.0):
        for s in (0.05, 0.1, 0.3, 0.5, 0.9):
            for nome in CONV:
                A = BE.matrice(eps, s, 12, nome)
                v_, n_ = float(T0.scarto_c6(A)), float(T.scarto_c6(A))
                if v_ < TOLL_C6:
                    giusti += 1
                    peg_d = max(peg_d, abs(n_ - v_))
                else:
                    sbagliati += 1
                    peg_n = max(peg_n, n_)
                    print("    eps %g s %g %s: scarto_c6 di %s %.2e, nuovo %.2e" % (eps, s, nome, RIF, v_, n_))
    esito("DEVE PASSARE: scarto_c6 nuovo = vecchio entro %g dove il vecchio era < %g (%d casi)" % (TOLL_C6_UGUALE, TOLL_C6, giusti), giusti > 0 and peg_d <= TOLL_C6_UGUALE, "il peggiore %.1e" % peg_d)
    esito("DEVE PASSARE: dove il vecchio sbagliava (%d casi, a s 0.5 compreso) il nuovo < %g" % (sbagliati, TOLL_C6), sbagliati > 0 and peg_n < TOLL_C6, "il peggiore %.2e" % peg_n)
    s_q = float(T.scarto_c6(T.matrice_tick(T.QUADRATO, T.LATO, T.DTAU)))
    esito("DEVE FALLIRE (il caso di _triangoli): il quadrato NON ha i 60 gradi, scarto > 1e6 x 64 ulp x pi", s_q > 1e6 * 64 * T.EPS * np.pi, "%.3e" % s_q)
    F0 = modulo_al("csv/_forza_da_cs.py", "_forza_da_cs_al_rif")
    rng = np.random.default_rng(7)
    Q = rng.normal(size=(8, 1)) + 1j * rng.normal(size=(8, 1))
    Q /= np.linalg.norm(Q)
    uguali = True
    for port in (None, (np.pi, np.pi)):
        F0.PORTANTE = FC.PORTANTE = port
        try:
            r0, r1 = F0.corsa(128, 0.5, 0.9, 1e-2, Q), FC.corsa(128, 0.5, 0.9, 1e-2, Q)
        finally:
            F0.PORTANTE = FC.PORTANTE = None
        uguali = uguali and r0 == r1
    esito("DI SERVIZIO (il quadrato, esplicito): _forza_da_cs.corsa() dopo il riordino = quella di %s AL BIT (portante 0 e (pi, pi))" % RIF, uguali, "")
    scrivi({"tipo": "parte0", "attributi": n_attr, "diversi": diversi, "matrice_al_bit": bit, "spettro": dsp, "c6_giusti": giusti, "c6_diff": peg_d, "c6_sbagliati": sbagliati,
            "c6_nuovo_peggiore": peg_n, "c6_quadrato": s_q, "corsa_quadrato_al_bit": uguali})


# =====================================================================================
#   LA COPPIA A K E IL MODO
# =====================================================================================
def coppia_K(eps, s):
    """### La coppia a `K`: ### **a `eps 0` i due livelli doppi diversi da `0` e da `-pi s`**; ### **a `eps > 0` seguiti in `eps` a passi di `PASSO_EPS` per sovrapposizione dello spazio.**
    ### Ritorna, in ordine di fase *(zero simmetrico)*: `w`, `Q` *(12 x 2)*, `delta_min` *(la distanza a `K` dagli altri livelli)*."""
    import _triangoli_bassa_energia as BE

    def blocco(e):
        return BE.matrice(e, s, LF, "simm")[KF[0], KF[1], :NB, :NB]
    lam, V = np.linalg.eig(blocco(0.0))
    w = -np.angle(lam)
    idx = [i for i in range(NB) if abs(av(w[i])) > TOLL_LIV and abs(av(w[i] + np.pi * s)) > TOLL_LIV]
    gruppi = []
    for i in sorted(idx, key=lambda i: w[i]):
        if gruppi and abs(w[i] - w[gruppi[-1][0]]) <= TOLL_LIV:
            gruppi[-1].append(i)
        else:
            gruppi.append([i])
    assert [len(g) for g in gruppi] == [2, 2], "la coppia a K a eps 0: gruppi %s" % [len(g) for g in gruppi]
    Qs = [np.linalg.qr(V[:, g])[0] for g in gruppi]
    passi = int(math.ceil(eps / PASSO_EPS - 1e-12))
    for j in range(1, passi + 1):
        lam, V = np.linalg.eig(blocco(eps * j / passi))
        nuovi = []
        for Q in Qs:
            ov = np.linalg.norm(Q.conj().T @ V, axis=0)
            top = [int(x) for x in np.argsort(-ov)[:2]]
            assert ov[top[1]] > 0.5, "la continuazione in eps perde la banda: sovrapposizioni %s" % ov[top]
            nuovi.append(np.linalg.qr(V[:, top])[0])
        Qs = nuovi
    lam, V = np.linalg.eig(blocco(eps))
    w = -np.angle(lam)
    out = []
    for Q in Qs:
        ov = np.linalg.norm(Q.conj().T @ V, axis=0)
        top = [int(x) for x in np.argsort(-ov)[:2]]
        assert abs(w[top[0]] - w[top[1]]) <= TOLL_DEG, "il livello della banda non e' doppio: %s" % w[top]
        wq = float(np.mean(w[top]))
        dmin = float(min(abs(av(w[i] - wq)) for i in range(NB) if i not in top))
        out.append({"w": wq, "Q": np.linalg.qr(V[:, top])[0], "delta_min": dmin})
    return sorted(out, key=lambda r: r["w"])


_CACHE = {}


def matrice_L(eps, s):
    import _triangoli_bassa_energia as BE
    if (eps, s) not in _CACHE:
        _CACHE[(eps, s)] = BE.matrice(eps, s, L, "simm")
    return _CACHE[(eps, s)]


def modo(eps, s, banda):
    """### Al `K`: la curvatura *(theta e cartesiana)*, `v_fit` *(theta e cartesiana)*, `v_g`, `d omega/ds` *(oggi; la simmetrica `+ pi`)*."""
    import _triangoli_bassa_energia as BE
    cu = BE.curvatura(matrice_L(eps, s), KL[0], KL[1], banda["w"], banda["Q"])
    co = BE.continua(eps, s, KL, banda["Q"][:, [0]], "oggi")
    dw = (co["piu"] - co["meno"]) / (2.0 * BE.H * s)
    om = float(np.mean(cu["cart_autovalori"]))
    return {"w": banda["w"], "delta_min": banda["delta_min"], "h11": cu["h11"], "omega2_cart": om, "cart_autovalori": cu["cart_autovalori"], "anisotropia": cu["anisotropia"],
            "v_theta": cu["v"], "v_fit": cu["v"] * F_A, "v_g": cu["v_g"], "dw_oggi": float(dw), "dw_simm": float(dw + np.pi), "omega_cont": co["omega_cont"]}


# =====================================================================================
#   PARTE A -- LA VELOCITA' DEL CONO
# =====================================================================================
def v_max(A):
    """### La velocita' di gruppo massima su tutte le bande della materia e tutta la zona *(Hellmann-Feynman, archi per tick)*, e dove."""
    B = A[:, :, :NB, :NB]
    n = B.shape[0]
    AR = np.fft.ifft2(B, axes=(0, 1))
    m = np.arange(n)
    m = np.where(m > n // 2, m - n, m).astype(float)
    D1 = np.fft.fft2(AR * (-1j * m)[:, None, None, None], axes=(0, 1))
    D2 = np.fft.fft2(AR * (-1j * m)[None, :, None, None], axes=(0, 1))
    a1, a2 = np.array([1.0, 0.0]), np.array([-0.5, math.sqrt(3.0) / 2.0])
    dirs = [np.array([math.cos(t), math.sin(t)]) for t in np.linspace(0.0, np.pi, DIREZIONI)]
    lam, V = np.linalg.eig(B)
    best = (0.0, None, None)
    for i in range(n):
        for j in range(n):
            lv, vv = lam[i, j], V[i, j]
            usato = np.zeros(NB, dtype=bool)
            for b in range(NB):
                if usato[b]:
                    continue
                cl = [c for c in range(NB) if not usato[c] and abs(lv[c] - lv[b]) < TOLL_DEG]
                usato[cl] = True
                Q, _ = np.linalg.qr(vv[:, cl])
                M1 = 1j * np.conj(lv[b]) * (Q.conj().T @ D1[i, j] @ Q)
                M2 = 1j * np.conj(lv[b]) * (Q.conj().T @ D2[i, j] @ Q)
                if len(cl) == 1:
                    g = M1[0, 0].real * a1 + M2[0, 0].real * a2
                    v = float(math.hypot(g[0], g[1]))
                else:
                    v = 0.0
                    for d in dirs:
                        Mn = (d @ a1) * M1 + (d @ a2) * M2
                        v = max(v, float(np.max(np.abs(np.linalg.eigvalsh(0.5 * (Mn + Mn.conj().T))))))
                if v > best[0]:
                    best = (v, (i, j), float(-np.angle(lv[b])))
    return best


def v_fronte(eps, s):
    """### Il fronte di un impulso su un nodo *(la sovrapposizione uniforme dei 12 complessi)*, toro `L_FRONTE x L_FRONTE`, `cs = s` uniforme, zero simmetrico."""
    import _triangoli as T
    vero = T.EPS_MONETA
    T.EPS_MONETA = eps
    try:
        inc, mot, st, par = T.scena_toro(T.TRIANGOLI, (L_FRONTE, L_FRONTE), s, T.X)
    finally:
        T.EPS_MONETA = vero
    n = inc.n
    m1, m2 = np.arange(n) // L_FRONTE, np.arange(n) % L_FRONTE
    d1 = (m1 + L_FRONTE // 2) % L_FRONTE - L_FRONTE // 2
    d2 = (m2 + L_FRONTE // 2) % L_FRONTE - L_FRONTE // 2
    r = np.hypot(d1 - 0.5 * d2, math.sqrt(3.0) / 2.0 * d2)
    o = np.argsort(r, kind="stable")
    for k in st:
        st[k][...] = 0
    st["psi_h"].reshape(n, NB)[0] = 1.0 / math.sqrt(NB)
    fr = {}
    with conv("simm"):
        for t in range(1, max(T_FRONTE) + 1):
            T.camminata(st, mot, par)
            if t in T_FRONTE:
                w = np.sum(np.abs(st["psi_h"].reshape(n, NB)) ** 2, axis=1)
                w = w / w.sum()
                coda = np.cumsum(w[o][::-1])[::-1]
                fr[t] = {thr: float(r[o][int(np.argmax(coda < thr))]) for thr in SOGLIE}
    t0, t1 = T_FRONTE
    # ### ⚠ il fronte deve restare DENTRO il toro: il raggio del cerchio inscritto nella cella di Wigner-Seitz del toro e' `L sqrt3/4` (annotazione 1)
    dentro = max(max(d.values()) for d in fr.values()) < DENTRO * L_FRONTE * math.sqrt(3.0) / 4.0
    return {str(thr): (fr[t1][thr] - fr[t0][thr]) / (t1 - t0) for thr in SOGLIE}, fr, dentro


def parte_A():
    print("### PARTE A -- LA VELOCITA' DEL CONO (v_max: Hellmann-Feynman, lato %d; v_fronte: toro %d x %d, %s tick, soglie %s; v_fit: la coppia a K, x sqrt3/2)"
          % (L, L_FRONTE, L_FRONTE, T_FRONTE, SOGLIE))
    rif = [json.loads(x) for x in subprocess.run(["git", "show", "%s:doc/referti_l2/triangoli_bassa_energia.jsonl" % RIF], capture_output=True, cwd=RADICE,
                                                  check=True).stdout.decode("utf-8").splitlines() if x.strip()]
    out = {}
    peg_u, peg_r, n_r, fuori_toro = 0.0, 0.0, 0, []
    for eps in EPS_AB:
        for s in S_A:
            t = time.time()
            vm, kvm, wvm = v_max(matrice_L(eps, s))
            vf, fr, dentro = v_fronte(eps, s)
            if not dentro:
                fuori_toro.append("eps %g s %g" % (eps, s))
            modi = [modo(eps, s, b) for b in coppia_K(eps, s)]
            out[(eps, s)] = {"v_max": vm, "v_fronte": vf, "modi": modi}
            print("  eps %g s %g: v_max %.5f (v_max/s %.4f, a k %s, livello %+.4f) | v_fronte %s | (%.0f s)"
                  % (eps, s, vm, vm / s, kvm, wvm, " ".join("thr %g: %.5f (/s %.4f)" % (float(k), v, v / s) for k, v in vf.items()), time.time() - t))
            for q, md in enumerate(modi):
                peg_u = max(peg_u, abs(md["omega2_cart"] - 0.75 * md["h11"]) / abs(md["omega2_cart"]))
                rap = {"v_fit": md["v_fit"], "v_max": vm, **{"v_fronte_%s" % k: v for k, v in vf.items()}}
                hs = {}
                for c in CONV:
                    dws = md["dw_simm"] if c == "simm" else md["dw_oggi"]
                    hs[c] = {k: s * md["omega2_cart"] * dws / v ** 2 for k, v in rap.items()}
                hr = [r for r in rif if r.get("tipo") == "modo" and r.get("punto") == "K" and r["eps"] == eps and r["s"] == s and r.get("oggi")
                      and abs(r["fase_simm"] - md["w"]) < 1e-6]
                h_rif = hr[0]["oggi"]["H_su_RG"] if hr else None
                h_mio = s * (md["h11"] / md["v_theta"] ** 2) * md["dw_oggi"]
                if h_rif is not None:
                    n_r += 1
                    peg_r = max(peg_r, abs(h_mio - h_rif) / abs(h_rif))
                rec = {"tipo": "velocita", "eps": eps, "s": s, "banda": q, "v_max": vm, "k_v_max": list(kvm), "v_fronte": vf, "fronte": {str(t_): {str(k): v for k, v in d.items()} for t_, d in fr.items()},
                       "modo": md, "rapporti_v": {k: v / md["v_fit"] for k, v in rap.items()}, "H_su_RG": hs, "H_su_RG_rif": h_rif, "H_su_RG_theta": h_mio}
                scrivi(rec)
                print("    banda %d: w %+.4f  omega''_cart %+.5f  v_fit %.5f (/s %.4f)  v_g (%+.1e, %+.1e) | v_max/v_fit %.4f  v_fronte/v_fit %s"
                      % (q, md["w"], md["omega2_cart"], md["v_fit"], md["v_fit"] / s, md["v_g"][0], md["v_g"][1], vm / md["v_fit"],
                         " ".join("%.4f" % (v / md["v_fit"]) for v in vf.values())))
                for c in CONV:
                    print("      a_H/a_RG %-4s: con v_fit %+.4f | con v_max %+.4f | con v_fronte %s   [%s: %s]"
                          % (c, hs[c]["v_fit"], hs[c]["v_max"], " ".join("%+.4f" % hs[c]["v_fronte_%s" % k] for k in vf), RIF,
                             f_(h_rif) if c == "oggi" else "--"))
            sys.stdout.flush()
    esito("DI SERVIZIO: il fronte resta dentro il toro (raggio < %g x L sqrt3/4, ogni soglia e tempo)" % DENTRO, not fuori_toro, ", ".join(fuori_toro) or "")
    esito("DI SERVIZIO: l'autovalore cartesiano della curvatura = 3/4 h11 entro %g (la conversione delle unita')" % TOLL_UNITA, peg_u <= TOLL_UNITA, "il peggiore %.1e" % peg_u)
    esito("DI SERVIZIO: a_H/a_RG (oggi, v_fit) = quello di %s entro %g relativo, dove la coppia era a K (%d bande)" % (RIF, TOLL_RIF, n_r), n_r > 0 and peg_r <= TOLL_RIF, "il peggiore %.1e" % peg_r)
    return out


# =====================================================================================
#   PARTE B -- LA CORSA
# =====================================================================================
def corsa(toro, Lx, eps, s0, eta, Q, nome, Tmax):
    """### Il pacchetto `G(m) u_K e^{i K.r}` *(`_forza_da_cs.pacchetto`)* a `Lx/4`, fermo, nel profilo `cs = s0 (1 + eta cos(2 pi m1/Lx))`; la camminata sola; il baricentro circolare in `m1`."""
    import _forza_da_cs as FC
    import _triangoli as T
    tr = tori()[toro]
    vero = T.EPS_MONETA
    T.EPS_MONETA = eps
    try:
        inc, mot, st, par = T.scena_toro((tr["spost"], T.TRIANGOLI[1]), (Lx, LY), 1.0, T.X)
    finally:
        T.EPS_MONETA = vero
    n = inc.n
    m1 = (np.arange(n) // LY).astype(float)
    m2 = (np.arange(n) % LY).astype(float)
    cs = s0 * (1.0 + eta * np.cos(2.0 * np.pi * m1 / Lx))
    assert float(cs.max()) <= 1.0 and float(cs.min()) > 0.0, "un nodo fuori dal cono: %r" % float(cs.max())
    mot.cs = cs
    mot.lambda_c = None
    for k in st:
        st[k][...] = 0
    x0, W = Lx / 4.0, Lx / 16.0
    st["psi_h"][...] = FC.pacchetto(m1, x0, W, Q[:, 0], tr["fase_K"](m1, m2)).reshape(st["psi_h"].shape)
    fase = np.exp(2j * np.pi * m1 / Lx)
    tt, xx, fuori = [], [], []
    norma0 = None
    with conv(nome):
        for t in range(Tmax + 1):
            if t:
                T.camminata(st, mot, par)
            p = st["psi_h"].reshape(n, NB)
            w = np.sum(np.abs(p) ** 2, axis=1)
            tot = float(np.sum(w) + np.sum(np.abs(st["phi_h"]) ** 2))
            norma0 = tot if norma0 is None else norma0
            assert abs(tot - norma0) <= FC.TOLL_NORMA * norma0, "la norma non si conserva: %r contro %r" % (tot, norma0)
            dx = ((Lx / (2.0 * np.pi) * np.angle(np.sum(w * fase))) - x0 + Lx / 2.0) % Lx - Lx / 2.0
            if abs(dx) >= Lx / 32.0:
                break
            tt.append(t)
            xx.append(float(dx))
            fuori.append(FC.norma_fuori(p, Q, tot))
    tt, xx = np.array(tt, dtype=float), np.array(xx)
    r = {"toro": toro, "Lx": Lx, "eps": eps, "s0": s0, "eta": eta, "conv": nome, "punti": len(tt), "Tmax": Tmax, "W": W,
         "fuori_max": float(max(fuori)), "spostamento_finale": float(xx[-1])}
    if len(tt) < FC.MIN_PUNTI:
        r.update(a=None, sigma_a=None, v0=None, leggibile=False, perche="meno di %d punti" % FC.MIN_PUNTI)
        return r, xx
    r.update(FC.fit_moto(tt, xx))
    r.update(leggibile=r["fuori_max"] <= FC.NORMA_FUORI)
    return r, xx


def parte_B(velo):
    import _forza_da_cs as FC
    print("### PARTE B -- LA CORSA (toro A: lati (Lx, %d) lungo (a1, a2), Lx %s; toro B: base (a1, a2 - a1), lati (%d, %d); x0 = Lx/4, W = Lx/16; T = max(Lx/4, ceil(%d x 2 pi/delta_min)))"
          % (LY, LX, LX_B, LY, PERIODI))
    TR = tori()
    righe = []
    serv_conv = 0.0
    for eps in EPS_AB:
        for s0 in S_A:
            vel = velo[(eps, s0)]
            bande = coppia_K(eps, s0)
            for q, (b, md) in enumerate(zip(bande, vel["modi"])):
                Tm = int(math.ceil(PERIODI * 2.0 * np.pi / b["delta_min"]))
                print("  eps %g s0 %g banda %d: w %+.4f delta_min %.4f omega''_cart %+.5f d omega/ds oggi %+.4f simm %+.4f v_g (%+.1e, %+.1e)"
                      % (eps, s0, q, b["w"], b["delta_min"], md["omega2_cart"], md["dw_oggi"], md["dw_simm"], md["v_g"][0], md["v_g"][1]))
                for toro, lxs, etas in (("A", LX, ETA), ("B", (LX_B,), ETA_B)):
                    f = TR[toro]["f"]
                    for Lx in lxs:
                        T_ = max(Lx // 4, Tm)
                        tracce, base = {}, {}
                        for nome in CONV:
                            dws = md["dw_simm"] if nome == "simm" else md["dw_oggi"]
                            for eta in etas:
                                t = time.time()
                                r, xx = corsa(toro, Lx, eps, s0, eta, b["Q"], nome, T_)
                                if eta == 0.0:
                                    tracce[nome] = xx
                                    base[nome] = xx
                                # ### ⚠ LA MISURA DIFFERENZIALE (annotazione 1): ### **`x(eta) - x(0)`, la stessa partenza: ### toglie la deriva libera** *(sul toro `B` il pacchetto NON e' fermo)*
                                k_ = min(len(xx), len(base[nome]))
                                rd = FC.fit_moto(np.arange(k_, dtype=float), xx[:k_] - base[nome][:k_]) if (eta != 0.0 and k_ >= FC.MIN_PUNTI) else None
                                dsdm = -s0 * eta * 2.0 * np.pi / Lx
                                aH = -md["omega2_cart"] * dws * dsdm / f ** 2
                                aRG = {"v_fit": md["v_fit"], "v_max": vel["v_max"], **{"v_fronte_%s" % k: v for k, v in vel["v_fronte"].items()}}
                                aRG = {k: -v ** 2 * (dsdm / s0) / f ** 2 for k, v in aRG.items()}
                                r.update(banda=q, w=b["w"], a_H=aH, a_RG=aRG, nullo=bool(r["a"] is not None and FC.nullo(r)),
                                         a_diff=None if rd is None else rd["a"], sigma_a_diff=None if rd is None else rd["sigma_a"],
                                         r_H_diff=None if rd is None else rd["a"] / aH,
                                         r_H=None if (r["a"] is None or eta == 0.0) else r["a"] / aH,
                                         r_RG=None if (r["a"] is None or eta == 0.0) else {k: r["a"] / v for k, v in aRG.items()})
                                scrivi(dict(r, tipo="corsa"))
                                righe.append(r)
                                print("    %s Lx %d %-4s eta %+-6g T %d: a %s +- %s  v0 %s  (%s)  a_H %+.3e  a/a_H %s [differenziale %s]  a/a_RG(v_max) %s  a/a_RG(v_fit) %s | tremolio %.1e fuori %.1e%s (%.1f s)"
                                      % (toro, Lx, nome, eta, T_, f_(r["a"], "%+.3e"), f_(r["sigma_a"], "%.1e"), f_(r["v0"], "%+.1e"),
                                         "nullo" if r["nullo"] else ("verso cs BASSO" if (r["a"] or 0) * (eta or 1) > 0 else "verso cs ALTO"), aH,
                                         f_(r["r_H"]), f_(r["r_H_diff"]), f_(r["r_RG"] and r["r_RG"]["v_max"]), f_(r["r_RG"] and r["r_RG"]["v_fit"]),
                                         r.get("residuo_max", float("nan")), r["fuori_max"], "" if r["leggibile"] else " ### NON LEGGIBILE", time.time() - t))
                                sys.stdout.flush()
                        if len(tracce) == 2:
                            k_ = min(len(tracce["simm"]), len(tracce["oggi"]))
                            serv_conv = max(serv_conv, float(np.max(np.abs(tracce["simm"][:k_] - tracce["oggi"][:k_]))))
    return righe, serv_conv


def controlli_B(righe, serv_conv, velo):
    print("### I CONTROLLI DELLA CORSA")
    esito("DI SERVIZIO: a eta 0 la traccia nelle due convenzioni uguale entro %g (a cs uniforme la simmetrica e' una fase globale)" % TOLL_CONV, serv_conv <= TOLL_CONV, "%.1e" % serv_conv)
    nul = [r for r in righe if r["eta"] == 0.0 and r["toro"] == "A"]
    cattivi = [r for r in nul if not (r["leggibile"] and r["nullo"])]
    esito("DEVE PASSARE: eta 0, |a| sotto il rumore del fit (|a| <= 2 sigma_a), ogni eps, s0, banda, Lx, conv -- toro A (%d corse)" % len(nul), not cattivi,
          "; ".join("%s Lx %d eps %g s0 %g b %d %s: a %s +- %s" % (r["toro"], r["Lx"], r["eps"], r["s0"], r["banda"], r["conv"], f_(r["a"], "%+.2e"), f_(r["sigma_a"], "%.1e"))
                    for r in cattivi[:6]) or "il peggiore |a|/sigma %.2f" % max(abs(r["a"]) / r["sigma_a"] for r in nul))
    chiave = lambda r: (r["toro"], r["Lx"], r["eps"], r["s0"], r["banda"], r["conv"])           # noqa: E731
    per = {}
    for r in righe:
        per.setdefault(chiave(r), {})[r["eta"]] = r
    peg, cattivi, peg_d, dove_d = 0.0, [], 0.0, None
    for k, d in per.items():
        if k[0] != "A":
            continue
        for eta in (1e-3, 1e-2):
            if eta not in d:
                continue
            a, b = d[eta]["a"], d[-eta]["a"]
            ok = a is not None and b is not None and a * b < 0
            asim = abs(abs(a) - abs(b)) / max(abs(a), abs(b)) if ok else None
            peg = max(peg, asim if asim is not None else 9.0)
            ad, bd = d[eta]["a_diff"], d[-eta]["a_diff"]
            if ad is not None and bd is not None:
                x_ = abs(abs(ad) - abs(bd)) / max(abs(ad), abs(bd)) if ad * bd < 0 else 9.0
                if x_ > peg_d:
                    peg_d, dove_d = x_, (k, eta)
            if not ok or asim > TOLL_SPECCHIO:
                cattivi.append("%s eta %g: %s %s" % (k, eta, f_(a, "%+.2e"), f_(b, "%+.2e")))
    esito("DEVE PASSARE: il profilo specchiato, a cambia segno e |a| uguale entro il %g%% (ogni caso, toro A)" % (100 * TOLL_SPECCHIO), not cattivi, "; ".join(cattivi[:4]) or "il peggiore %.4f" % peg)
    print("  lettura (non un controllo): lo specchio DIFFERENZIALE sul toro A, il peggiore %.4f a %s" % (peg_d, dove_d))
    print("### IL TORO B (il gradiente parallelo a un legame, lungo Gamma-K: il pacchetto NON e' fermo, la deriva trigonale -- annotazione 1): letto, non un controllo")
    for k, d in sorted(per.items()):
        if k[0] != "B":
            continue
        z, p_, m_ = d[0.0], d[1e-2], d[-1e-2]
        asd = abs(abs(p_["a_diff"]) - abs(m_["a_diff"])) / max(abs(p_["a_diff"]), abs(m_["a_diff"]))
        print("  %s: eta 0: v0 %+.2e a %+.2e +- %.1e | grezzo a/a_H %+.4f %+.4f | differenziale a/a_H %+.4f %+.4f (specchio %.3f)"
              % (k, z["v0"], z["a"], z["sigma_a"], p_["r_H"], m_["r_H"], p_["r_H_diff"], m_["r_H_diff"], asd))
    # ---- DEVE FALLIRE: con lo zero di oggi le due bande hanno la stessa accelerazione
    vere, chiave_giusta, note = 0, True, []
    for Lx in LX:
        for s0 in S_A:
            for eta in (1e-3, 1e-2):
                b0, b1 = per[("A", Lx, 0.0, s0, 0, "oggi")][eta], per[("A", Lx, 0.0, s0, 1, "oggi")][eta]
                if not (b0["leggibile"] and b1["leggibile"]) or b0["nullo"] or b1["nullo"]:
                    chiave_giusta = False
                    continue
                stessa = abs(b1["a"] - b0["a"]) <= TOLL_STESSA * max(abs(b0["a"]), abs(b1["a"]))
                vere += 1 if stessa else 0
                note.append("s0 %g Lx %d eta %g: %+.2e %+.2e" % (s0, Lx, eta, b0["a"], b1["a"]))
    esito("DEVE FALLIRE: <<con lo zero di oggi le due bande hanno la stessa accelerazione>> (eps 0, toro A, ogni s0, Lx, eta > 0; per la chiave giusta: leggibili, non nulle)",
          vere == 0 and chiave_giusta, "vera %d volte; %s" % (vere, "; ".join(note[:4])))
    # ---- i due PUO' FALLIRE
    sel = [r for r in righe if r["toro"] == "A" and r["eps"] == 0.0 and r["s0"] == 0.05 and r["conv"] == "simm" and r["eta"] > 0]
    ok1 = bool(sel) and all(r["leggibile"] and r["r_H"] is not None and PUO1[0] <= r["r_H"] <= PUO1[1] and r["a"] > 0 for r in sel)
    esito("PUO' FALLIRE: eps 0, s0 0.05, zero simmetrico: a/a_H fra %g e %g, lo stesso verso, verso cs basso (%d corse)" % (PUO1[0], PUO1[1], len(sel)), ok1,
          " ".join("%.4f" % r["r_H"] for r in sel if r["r_H"] is not None))
    ok2 = bool(sel) and all(r["leggibile"] and r["r_RG"] is not None and PUO2[0] <= r["r_RG"]["v_max"] <= PUO2[1] for r in sel)
    esito("PUO' FALLIRE: la stessa portata, a/a_RG con la velocita' del cono (v_max) fra %g e %g" % PUO2, ok2, " ".join("%.4f" % r["r_RG"]["v_max"] for r in sel if r["r_RG"]))
    # ---- le tabelle: universalita', isotropia, il limite
    print("### L'UNIVERSALITA' FRA LE BANDE (a_1/a_0), FRA eps 0 E 0.5 (a/a_H), L'ISOTROPIA (toro B / toro A, a/a_H DIFFERENZIALE), eta > 0")
    for Lx in LX:
        for nome in CONV:
            for s0 in S_A:
                for eta in (1e-3, 1e-2):
                    cel = []
                    for eps in EPS_AB:
                        b0, b1 = per[("A", Lx, eps, s0, 0, nome)][eta], per[("A", Lx, eps, s0, 1, nome)][eta]
                        cel.append("eps %g: a_1/a_0 %s  a/a_H %s %s" % (eps, f_(b1["a"] / b0["a"] if b0["a"] else None), f_(b0["r_H"]), f_(b1["r_H"])))
                    u = [per[("A", Lx, 0.5, s0, q, nome)][eta]["r_H"] / per[("A", Lx, 0.0, s0, q, nome)][eta]["r_H"] for q in (0, 1)]
                    riga = {"tipo": "universalita", "Lx": Lx, "conv": nome, "s0": s0, "eta": eta, "eps05_su_eps0": u,
                            "bande": {str(eps): [per[("A", Lx, eps, s0, q, nome)][eta]["a"] for q in (0, 1)] for eps in EPS_AB}}
                    if Lx == LX_B and eta == 1e-2:
                        riga["B_su_A"] = {str(eps): [per[("B", Lx, eps, s0, q, nome)][eta]["r_H_diff"] / per[("A", Lx, eps, s0, q, nome)][eta]["r_H_diff"] for q in (0, 1)] for eps in EPS_AB}
                    scrivi(riga)
                    print("  Lx %d %-4s s0 %-4g eta %-6g | %s | (a/a_H)[eps 0.5]/(a/a_H)[eps 0] %.4f %.4f%s"
                          % (Lx, nome, s0, eta, " | ".join(cel), u[0], u[1],
                             "" if "B_su_A" not in riga else " | B/A (differenziale) " + " ".join("eps %s: %.4f %.4f" % (k, *v) for k, v in riga["B_su_A"].items())))
    print("### IL LIMITE A s0 -> 0 (toro A, Lx %d, eta 1e-2): l'estrapolazione LINEARE dai due s0 piu' piccoli e la QUADRATICA dai tre, tutte e due" % max(LX))
    for nome in CONV:
        for eps in EPS_AB:
            for q in (0, 1):
                for che in ("r_H", "v_max"):
                    y = [per[("A", max(LX), eps, s, q, nome)][1e-2] for s in S_A]
                    y = [r["r_H"] if che == "r_H" else r["r_RG"]["v_max"] for r in y]
                    lin = 2.0 * y[0] - y[1]
                    c = np.polyfit(S_A[:3], y[:3], 2)
                    quad = float(np.polyval(c, 0.0))
                    scrivi({"tipo": "limite", "conv": nome, "eps": eps, "banda": q, "che": che, "y": y, "lineare": lin, "quadratica": quad})
                    print("  %-4s eps %g banda %d %-12s: %s | a s0 -> 0: lineare %+.4f, quadratica %+.4f (differenza %.1e)"
                          % (nome, eps, q, "a/a_H" if che == "r_H" else "a/a_RG(v_max)", " ".join("%+.4f" % v for v in y), lin, quad, abs(lin - quad)))


# =====================================================================================
#   PARTE C -- LA MONETA E LO ZERO
# =====================================================================================
def parte_C():
    print("### PARTE C -- LA MONETA E LO ZERO (la coppia a K seguita in eps; lambda*_RG come %s, lambda*_H dalle a_H uguali; a lambda = 1/2 la differenza delle a_H)" % RIF)
    rif = [json.loads(x) for x in subprocess.run(["git", "show", "%s:doc/referti_l2/triangoli_bassa_energia.jsonl" % RIF], capture_output=True, cwd=RADICE,
                                                  check=True).stdout.decode("utf-8").splitlines() if x.strip()]
    pts, peg, n_r = [], 0.0, 0
    for eps in EPS_C:
        for s in S_A:
            m0, m1 = [modo(eps, s, b) for b in coppia_K(eps, s)]
            k0, k1 = m0["h11"] / m0["v_theta"] ** 2, m1["h11"] / m1["v_theta"] ** 2
            l_rg = (k1 * m1["dw_oggi"] - k0 * m0["dw_oggi"]) / (2.0 * np.pi * (k0 - k1))
            o0, o1 = m0["omega2_cart"], m1["omega2_cart"]
            l_h = (o1 * m1["dw_oggi"] - o0 * m0["dw_oggi"]) / (2.0 * np.pi * (o0 - o1))
            A0, A1 = o0 * m0["dw_simm"], o1 * m1["dw_simm"]
            da = (A1 - A0) / (0.5 * (A1 + A0))
            centro = 0.5 * (m0["w"] + m1["w"]) / s
            lr = [r["lambda_stella"] for r in rif if r.get("tipo") == "lambda_stella" and r["eps"] == eps and r["s"] == s and tuple(r["k"]) == KL]
            if lr:
                n_r += 1
                peg = max(peg, abs(lr[0] - l_rg))
            rec = {"tipo": "moneta", "eps": eps, "s": s, "lambda_RG": l_rg, "lambda_H": l_h, "diff_aH_simm": da, "centro_su_s": centro, "lambda_rif": lr[0] if lr else None,
                   "v_fit": [m0["v_fit"], m1["v_fit"]], "omega2_cart": [o0, o1], "dw_oggi": [m0["dw_oggi"], m1["dw_oggi"]]}
            scrivi(rec)
            pts.append(rec)
            print("  eps %-4g s %-4g: lambda*_RG %.8f (%s: %s)  lambda*_H %.8f | a lambda 1/2: (a_H1 - a_H0)/media %+.3e | centro/s %+.5f | v_fit %.5f %.5f  omega''_cart %+.5f %+.5f"
                  % (eps, s, l_rg, RIF, f_(lr[0] if lr else None, "%.8f"), l_h, da, centro, m0["v_fit"], m1["v_fit"], o0, o1))
            sys.stdout.flush()
    esito("DI SERVIZIO: lambda*_RG = quello di %s entro %g dove la coppia era a K (%d punti)" % (RIF, TOLL_RIF, n_r), n_r > 0 and peg <= TOLL_RIF, "il peggiore %.1e" % peg)
    X = np.array([[1.0, math.log(r["s"]), math.log(r["eps"])] for r in pts])
    for che, f in (("lambda*_RG - 1/2", lambda r: r["lambda_RG"] - 0.5), ("lambda*_H - 1/2", lambda r: r["lambda_H"] - 0.5), ("(a_H1 - a_H0)/media", lambda r: r["diff_aH_simm"]),
                   ("centro/s", lambda r: r["centro_su_s"])):
        y = np.array([f(r) for r in pts])
        if np.any(y == 0.0):
            print("  il fit di %s: un valore nullo, il logaritmo non c'e'" % che)
            continue
        c, *_ = np.linalg.lstsq(X, np.log(np.abs(y)), rcond=None)
        res = float(np.max(np.abs(np.log(np.abs(y)) - X @ c)))
        segni = sorted({"+" if v > 0 else "-" for v in y})
        scrivi({"tipo": "fit_moneta", "che": che, "c": float(c[0]), "p_s": float(c[1]), "q_eps": float(c[2]), "residuo_log_max": res, "segni": segni})
        print("  il fit di |%s| = e^c s^p eps^q: p %.3f  q %.3f  (e^c %.3e; il residuo in ln, massimo %.3f; i segni %s)" % (che, c[1], c[2], math.exp(c[0]), res, "".join(segni)))


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 110)
    print("I TRIANGOLI, SECONDO GRADINO: la forza sul modo a K (il toro rettangolare, la velocita' del cono, la corsa, l'universalita', la moneta e lo zero)")
    print("=" * 110)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py", "csv/_forza_da_cs.py", "csv/_zero_simmetrico.py",
                                     "csv/_gravita_collettiva.py", "csv/_modi_pi_e_solitoni.py", "csv/_moneta_massa.py", "csv/_universalita_massa.py", "csv/_triangoli_forza.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: RIF %s; L %d; LF %d; S_A %s; EPS_AB %s; EPS_C %s; L_FRONTE %d; DENTRO %g; T_FRONTE %s; SOGLIE %s; LX %s; LY %d; LX_B %d; ETA %s; ETA_B %s; PERIODI %d; PASSO_EPS %g;"
          % (RIF, L, LF, S_A, EPS_AB, EPS_C, L_FRONTE, DENTRO, T_FRONTE, SOGLIE, LX, LY, LX_B, ETA, ETA_B, PERIODI, PASSO_EPS))
    print("    TOLL_LIV %g TOLL_DEG %g DIREZIONI %d TOLL_BIT_SPETTRO %g TOLL_C6 %g TOLL_C6_UGUALE %g TOLL_UNITA %g TOLL_RIF %g TOLL_CONV %g TOLL_SPECCHIO %g TOLL_STESSA %g PUO1 %s PUO2 %s"
          % (TOLL_LIV, TOLL_DEG, DIREZIONI, TOLL_BIT_SPETTRO, TOLL_C6, TOLL_C6_UGUALE, TOLL_UNITA, TOLL_RIF, TOLL_CONV, TOLL_SPECCHIO, TOLL_STESSA, PUO1, PUO2))
    print("-" * 110)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    parte_0()
    print("-" * 110)
    velo = parte_A()
    print("-" * 110)
    righe, serv = parte_B(velo)
    controlli_B(righe, serv, velo)
    print("-" * 110)
    parte_C()
    print("=" * 110)
    print("I TRIANGOLI, SECONDO GRADINO: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
