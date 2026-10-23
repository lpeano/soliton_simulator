r"""**IL VERSO E L'INTENSITA' DELLA FORZA DA `cs`: un pacchetto di materia in un gradiente di `cs`** *(la camminata sola, il quadrato su un toro rettangolare)*.

> ### ⛔ **Il task history e' `2026-10-23_forza_da_cs.md`** *(le verifiche, il metodo, le tre formule della previsione e i criteri, fissati prima)*. ### **`cs` per
> nodo SOLO nella scena, in memoria** *(`mot.cs` array, `mot.lambda_c = None`)*; ### **`leggi.yaml` e l'impronta intatti.** ### **`matrice()` e `rami_seguiti()` di
> `csv/_massa_vicino_al_cono.py`, `spettro()`, `catene()` e `blob()` di `csv/_universalita_massa.py` IMPORTATI**, non copiati.

### **PARTE `A`** *(la previsione, dai soli spettri uniformi)*: ### **la catena principale** *(la `catena 0`)*, ### **ogni suo `omega(0)` distinto come riga**, ### **`a_prev`,
`a_prev[Dt]`, `a_H`, `a_RG`** e i rapporti -> `doc/referti_l2/forza_da_cs_previsione.jsonl`. ### **PARTE `B`** *(la corsa)*: ### **legge la previsione committata e non la
ricalcola**; ### **il pacchetto `e * gaussiana` a `Lx/4`, fermo, il baricentro circolare a ogni tick, il fit `x0 + v0 t + a t^2/2`**, ### **i cinque controlli** ->
`doc/referti_l2/forza_da_cs.jsonl`.

Gira con:  python csv/_forza_da_cs.py A > doc/referti_l2/forza_da_cs_previsione.txt
           python csv/_forza_da_cs.py B > doc/referti_l2/forza_da_cs.txt
"""
import io
import json
import os
import subprocess
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

L_SPETTRO = 64                 # il lato degli spettri uniformi (quello di 51f45268 e 44d4963d)
S_PREV = (0.85, 0.9, 0.95, 0.99)
S0_LISTA = (0.9, 0.95, 0.99)
EPS_LISTA = (0.0, 0.5)
ETA_CORSA = (0.0, 5e-4, 1e-3, -1e-3, 5e-3, 1e-2, -1e-2)
ETA_MODULI = (5e-4, 1e-3, 5e-3, 1e-2)
ETA_CONTROLLI = (1e-3, 1e-2)
LX_LISTA = (128, 256)
LY = 4
PORTANTE = None                # (kx, ky) del pacchetto: None = a riposo a k = 0 (com'era); csv/_modi_pi_e_solitoni.py la imposta in memoria per i modi a k = pi
TOLL_FIT = 0.05                # il fit di un ramo massivo (44d4963d)
TOLL_DISPERSIVO = 0.1          # |v_g| per tempo proprio (51f45268)
TOLL_OMEGA = 1e-9              # lo stesso autovalore a k = 0
TOLL_DISTINTI = 1e-6           # due omega(0), o due Dt, distinti
TOLL_SPECCHIO = 1e-6
TOLL_LIN = 0.05
TOLL_TAGLIE = 0.05
SOGLIA_SALTO = 0.01            # le taglie: solo Dt > 0.01 per tick (scelta di Luca)
NORMA_FUORI = 0.10
PAVIMENTO = 1e-12
MIN_PUNTI = 6
TOLL_NORMA = 1e-10
REF = os.path.join(RADICE, "doc", "referti_l2")
PREV_JSONL = os.path.join(REF, "forza_da_cs_previsione.jsonl")
JSONL = os.path.join(REF, "forza_da_cs.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def avvolgi(w):
    return float((w + np.pi) % (2.0 * np.pi) - np.pi)


# =====================================================================================
#   PARTE A -- GLI SPETTRI UNIFORMI E LA PREVISIONE
# =====================================================================================
def rami(s, eps):
    """### I rami massivi validi a `cs = s` uniforme *(`dtau = 1`)*: `Dt`, `v`, `omega(0)`, la curvatura; e il blocco `8 x 8` a `k = 0`."""
    import _massa_vicino_al_cono as MV
    import _moneta_massa as MM
    L = L_SPETTRO
    A = MV.matrice(L, 1.0, eps, s)
    ph = MV.rami_seguiti(A, L)
    kk = 2.0 * np.pi * np.arange(L // 2 + 1) / L
    vg = np.gradient(ph, kk, axis=0)
    sel = kk <= 0.25 * np.pi + 1e-12
    out = []
    for b in range(8):
        if float(np.max(np.abs(vg[:, b]))) / s <= TOLL_DISPERSIVO:
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Dt, v, sc = MM.fit_massa(kk[sel], ph[sel, b] - ph[0, b])
        if not np.isfinite(Dt) or not sc <= TOLL_FIT or not 1e-9 < Dt <= np.pi:
            continue
        curv = float(2.0 * (ph[1, b] - ph[0, b]) / kk[1] ** 2)
        out.append({"ramo": b, "Dt": float(Dt), "v": float(v), "omega0": avvolgi(ph[0, b]), "omega1": avvolgi(ph[1, b]), "curv_fd": curv,
                    "segno": 1.0 if curv > 0 else -1.0, "scarto": float(sc)})
    fuori = float(max(np.abs(A[0, 0, :8, 8:]).max(), np.abs(A[0, 0, 8:, :8]).max()))
    return out, (A[0, 0, :8, :8].copy(), A[1, 0, :8, :8].copy()), fuori


def catena_principale(eps):
    """### La `catena 0` di `catene()` su `spettro()` a `S_LISTA`, lato `L_SPETTRO`."""
    import _universalita_massa as UM
    per_s = {s: UM.spettro(L_SPETTRO, s, eps)[0] for s in UM.S_LISTA}
    return UM.catene(per_s)[0]


def bersaglio(c0, s):
    """### Il `Dt` della catena `0` al punto di `S_LISTA` piu' vicino a `s`."""
    k = min(c0, key=lambda q: abs(q - s))
    return c0[k]


def righe_del_ramo(lista, Dt_rif):
    """### I rami col `Dt` piu' vicino a `Dt_rif` *(e i loro degeneri)*, raggruppati per `omega(0)` distinto: una riga per gruppo."""
    if not lista:
        return []
    best = min(lista, key=lambda r: abs(r["Dt"] - Dt_rif) / Dt_rif)
    scelti = [r for r in lista if abs(r["Dt"] - best["Dt"]) <= TOLL_DISTINTI * best["Dt"]]
    gruppi = []
    for r in sorted(scelti, key=lambda r: r["omega0"]):
        if gruppi and abs(r["omega0"] - gruppi[-1][0]["omega0"]) <= TOLL_DISTINTI:
            gruppi[-1].append(r)
        else:
            gruppi.append([r])
    righe = []
    for i, g in enumerate(gruppi):
        nome = "unico" if len(gruppi) == 1 else ("basso" if i == 0 else ("alto" if i == len(gruppi) - 1 else "medio%d" % i))
        righe.append({"nome": nome, "omega0": g[0]["omega0"], "Dt": float(np.mean([r["Dt"] for r in g])),
                      "v": float(np.mean([r["v"] for r in g])), "segno": g[0]["segno"],
                      "segni_concordi": all(r["segno"] == g[0]["segno"] for r in g), "copie": len(g),
                      "omega1": [r["omega1"] for r in g],
                      "rami": [r["ramo"] for r in g]})
    return righe


def segui(lista, riga):
    """### A un altro `s`: fra i rami col `Dt` piu' vicino a quello della riga, quello con `omega(0)` piu' vicino."""
    best = min(lista, key=lambda r: abs(r["Dt"] - riga["Dt"]) / riga["Dt"])
    vicini = [r for r in lista if abs(r["Dt"] - best["Dt"]) <= TOLL_DISTINTI * best["Dt"]]
    return min(vicini, key=lambda r: abs(avvolgi(r["omega0"] - riga["omega0"])))


def spazio_proprio(B, omega0):
    """### La base ortonormale dello spazio proprio di `B` con `-angle(lambda) = omega0` entro `TOLL_OMEGA`."""
    lam, V = np.linalg.eig(B)
    sel = [i for i in range(len(lam)) if abs(avvolgi(-np.angle(lam[i]) - omega0)) <= TOLL_OMEGA]
    assert sel, "nessun autovalore con omega = %r" % omega0
    Q, _ = np.linalg.qr(V[:, sel])
    return Q


def spazio_del_ramo(BB, riga):
    """### Lo spazio del RAMO a `k -> 0`: ### **a `k = 0` lo spazio proprio con `omega(0)` puo' contenere ALTRI rami** *(non massivi, degeneri li')*;
    ### **i vettori del ramo al primo `k` lungo `x`** *(`omega(k_1)`)* ### **proiettati sullo spazio a `k = 0`** ne danno il limite. ### **Il rango deve essere
    il numero delle copie.**"""
    B0, B1 = BB
    Q0 = spazio_proprio(B0, riga["omega0"])
    lam, V = np.linalg.eig(B1)
    sel = sorted({i for w1 in riga["omega1"] for i in range(len(lam)) if abs(avvolgi(-np.angle(lam[i]) - w1)) <= TOLL_DISTINTI})
    P = Q0 @ (Q0.conj().T @ V[:, sel])
    U, sv, _ = np.linalg.svd(P, full_matrices=False)
    rango = int(np.sum(sv > 0.5 * sv[0]))
    assert rango == riga["copie"], "lo spazio del ramo ha rango %d, le copie sono %d (valori singolari %s)" % (rango, riga["copie"], sv)
    return U[:, :rango], Q0.shape[1], [float(x) for x in sv]


def parte_A():
    import _universalita_massa as UM
    print("### PARTE A -- LA PREVISIONE SEMICLASSICA, DAI SOLI SPETTRI UNIFORMI (lato %d, dtau 1, cs = s)" % L_SPETTRO)
    io.open(PREV_JSONL, "w", encoding="utf-8").close()
    scrivi = lambda r: io.open(PREV_JSONL, "a", encoding="utf-8").write(json.dumps(r) + "\n")   # noqa: E731
    scrivi({"tipo": "testata", "blobs": {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py",
                                                                 "csv/_universalita_massa.py", "csv/_forza_da_cs.py")}})
    cache = {}

    def R(s, eps):
        if (s, eps) not in cache:
            cache[(s, eps)] = rami(s, eps)
        return cache[(s, eps)]
    for eps in EPS_LISTA:
        c0 = catena_principale(eps)
        print("  eps %g: la catena 0 (lato %d): %s" % (eps, L_SPETTRO, ", ".join("s %g Dt %.5f" % (s, c0[s]) for s in sorted(c0))))
        scrivi({"tipo": "catena0", "eps": eps, "Dt": {str(s): c0[s] for s in sorted(c0)}})
        # ---- 1. la tabella del mandato
        print("  ### 1. omega(0), Dt, v, curvatura della catena principale -- eps %g" % eps)
        for s in S_PREV:
            lista, _B, fuori = R(s, eps)
            for rg in righe_del_ramo(lista, bersaglio(c0, s)):
                print("    s %-5g ramo %-6s: omega(0) %+.6f  Dt %.6f  v %.5f  curvatura %+d (copie %d, segni concordi %s)  [blocchi fuori diagonale %.1e]"
                      % (s, rg["nome"], rg["omega0"], rg["Dt"], rg["v"], int(rg["segno"]), rg["copie"], rg["segni_concordi"], fuori))
                scrivi(dict(rg, tipo="spettro", s=s, eps=eps, fuori_diagonale=fuori))
        # ---- 2-5. le previsioni
        print("  ### 2-5. a_prev, a_prev[Dt], a_H, a_RG -- eps %g (a per Lx 128 e eta > 0; a scala come eta/Lx)" % eps)
        for s0 in S0_LISTA:
            lista0, B0, _ = R(s0, eps)
            for rg in righe_del_ramo(lista0, bersaglio(c0, s0)):
                Q, dim0, sv = spazio_del_ramo(B0, rg)
                print("    s0 %-4g %-6s: lo spazio a k = 0 con omega(0) %+.6f ha dimensione %d; quello del ramo %d (valori singolari %s)"
                      % (s0, rg["nome"], rg["omega0"], dim0, Q.shape[1], ", ".join("%.3f" % x for x in sv)))
                scrivi({"tipo": "vettore", "s0": s0, "eps": eps, "ramo": rg["nome"], "omega0": rg["omega0"], "dim_k0": dim0,
                        "valori_singolari": sv, "Q_re": Q.real.tolist(), "Q_im": Q.imag.tolist()})
                for eta in ETA_MODULI:
                    sm, sp = s0 * (1.0 - eta), s0 * (1.0 + eta)
                    rm, rp = segui(R(sm, eps)[0], rg), segui(R(sp, eps)[0], rg)
                    dw = avvolgi(rp["omega0"] - rm["omega0"]) / (sp - sm)
                    dlnD = (np.log(rp["Dt"]) - np.log(rm["Dt"])) / (sp - sm)
                    nulla = abs(rg["omega0"]) < TOLL_OMEGA or abs(rp["omega0"]) < TOLL_OMEGA or abs(rm["omega0"]) < TOLL_OMEGA
                    dlnW = None if nulla else float((np.log(abs(rp["omega0"])) - np.log(abs(rm["omega0"]))) / (sp - sm))
                    v2 = rg["v"] ** 2
                    w2 = rg["segno"] * v2 / rg["Dt"]
                    per_lx = {}
                    for Lx in LX_LISTA:
                        dsdx = -s0 * eta * 2.0 * np.pi / Lx
                        a_RG = -v2 * dsdx / s0
                        a_prev = None if dlnW is None else -v2 * dlnW * dsdx
                        a_prevDt = -v2 * dlnD * dsdx
                        a_H = -w2 * dw * dsdx
                        per_lx[str(Lx)] = {"ds_dx": dsdx, "a_RG": a_RG, "a_prev": a_prev, "a_prevDt": a_prevDt, "a_H": a_H}
                    q = per_lx["128"]
                    rap = lambda a: None if a is None else a / q["a_RG"]                            # noqa: E731
                    verso = lambda r: "--" if r is None else ("verso cs BASSO" if r > 0 else "verso cs ALTO")   # noqa: E731
                    rec = {"tipo": "previsione", "s0": s0, "eps": eps, "ramo": rg["nome"], "eta": eta, "omega0": rg["omega0"],
                           "Dt": rg["Dt"], "v": rg["v"], "segno_curv": rg["segno"], "d_omega0_ds": float(dw),
                           "d_lnDelta_ds": dlnW, "d_lnDt_ds": float(dlnD), "a_H_nulla": abs(dw) < TOLL_OMEGA,
                           "per_Lx": per_lx, "r_prev": rap(q["a_prev"]), "r_prevDt": rap(q["a_prevDt"]), "r_H": rap(q["a_H"]),
                           "D_su_v": rg["Dt"] / rg["v"]}
                    scrivi(rec)
                    if eta in ETA_CONTROLLI:
                        f = lambda x: "    --    " if x is None else "%+.3e" % x                     # noqa: E731
                        print("    s0 %-4g %-6s eta %-6g: d omega0/ds %+.4f  d lnDelta/ds %s  d lnDt/ds %+.3f | a_prev %s  a_prev[Dt] %s  a_H %s  a_RG %s"
                              % (s0, rg["nome"], eta, dw, f(dlnW), dlnD, f(q["a_prev"]), f(q["a_prevDt"]), f(q["a_H"]), f(q["a_RG"])))
                        print("        a/a_RG: prev %s (%s)  prev[Dt] %s (%s)  H %s (%s);  D/v %.4f contro 1/W %.4f (Lx 128)"
                              % (f(rec["r_prev"]), verso(rec["r_prev"]), f(rec["r_prevDt"]), verso(rec["r_prevDt"]),
                                 f(rec["r_H"]), verso(rec["r_H"]), rec["D_su_v"], 16.0 / 128))
                    sys.stdout.flush()
    print("  la previsione e' in %s: si COMMITTA prima della parte B" % os.path.relpath(PREV_JSONL, RADICE))


# =====================================================================================
#   PARTE B -- LA CORSA
# =====================================================================================
def committata(p):
    rel = os.path.relpath(p, RADICE).replace("\\", "/")
    t = subprocess.run(["git", "ls-files", "--error-unmatch", rel], capture_output=True, cwd=RADICE).returncode == 0
    d = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], capture_output=True, cwd=RADICE).returncode == 0
    return t and d


def corsa(Lx, eps, s0, eta, Q):
    """### Il pacchetto `e * gaussiana` a `Lx/4`, fermo; la camminata sola; il baricentro circolare, la norma fuori, a ogni tick."""
    import _stabilita_lineare as SL
    import scena_l2 as SC
    import statica_protocollo as PR
    inc, mot, st, par, _c, _p = SC.scena(1.0, PR.VUOTO, 0.0, PR.RAGGIO, False, True, False, PR.SEME, 1, lati=(Lx, LY))
    par["eps"] = float(eps)
    n = inc.n
    x = (np.arange(n) // LY).astype(float)
    cs = s0 * (1.0 + eta * np.cos(2.0 * np.pi * x / Lx))
    assert float(cs.max()) <= 1.0 and float(cs.min()) > 0.0, "un nodo fuori dal cono: s max %r" % float(cs.max())
    mot.cs = cs
    mot.lambda_c = None
    for k in st:
        st[k][...] = 0
    x0 = Lx / 4.0
    W = Lx / 16.0
    e = Q[:, 0]
    G = np.exp(-(x - x0) ** 2 / (2.0 * W * W))
    cel = G[:, None] * e[None, :]
    if PORTANTE is not None:
        # ### la PORTANTE `e^{i k.x}` del modo a `k`: ### **`A(k)` e' la trasformata con `e^{-i k x}`**, quindi lo stato di Bloch e' `e^{+i k x} u_k`
        cel = cel * np.exp(1j * (PORTANTE[0] * x + PORTANTE[1] * (np.arange(n) % LY)))[:, None]
    cel /= np.sqrt(np.sum(np.abs(cel) ** 2))
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    fase = np.exp(2j * np.pi * x / Lx)
    Tmax = Lx // 4
    tt, xx, fuori = [], [], []
    norma0 = None
    for t in range(Tmax + 1):
        if t:
            SL.passo(st, mot, par, False, (SL.S3,), 0.0)
        p = st["psi_h"].reshape(n, 8)
        w = np.sum(np.abs(p) ** 2, axis=1)
        tot = float(np.sum(w) + np.sum(np.abs(st["phi_h"]) ** 2))
        norma0 = tot if norma0 is None else norma0
        assert abs(tot - norma0) <= TOLL_NORMA * norma0, "la norma non si conserva: %r contro %r" % (tot, norma0)
        dx = ((Lx / (2.0 * np.pi) * np.angle(np.sum(w * fase))) - x0 + Lx / 2.0) % Lx - Lx / 2.0
        if abs(dx) >= Lx / 32.0:
            break
        inn = float(np.sum(np.abs(p @ Q.conj()) ** 2))
        tt.append(t)
        xx.append(float(dx))
        fuori.append(1.0 - inn / tot)
    tt, xx = np.array(tt, dtype=float), np.array(xx)
    r = {"Lx": Lx, "eps": eps, "s0": s0, "eta": eta, "punti": len(tt), "W": W, "Tmax": Tmax,
         "fuori_max": float(max(fuori)) if fuori else None, "spostamento_finale": float(xx[-1]) if len(xx) else None}
    if len(tt) < MIN_PUNTI:
        r.update(a=None, sigma_a=None, v0=None, leggibile=False, perche="meno di %d punti" % MIN_PUNTI)
        return r
    X = np.stack([np.ones_like(tt), tt, 0.5 * tt * tt], axis=1)
    coef, *_ = np.linalg.lstsq(X, xx, rcond=None)
    res = xx - X @ coef
    var = float(res @ res) / (len(tt) - 3)
    cov = var * np.linalg.inv(X.T @ X)
    r.update(a=float(coef[2]), sigma_a=float(np.sqrt(max(cov[2, 2], 0.0))), v0=float(coef[1]), x0_fit=float(coef[0]),
             residuo_max=float(np.max(np.abs(res))))
    leg = r["fuori_max"] <= NORMA_FUORI
    r.update(leggibile=leg, perche="" if leg else "norma fuori %.3f > %g" % (r["fuori_max"], NORMA_FUORI))
    return r


def nullo(r):
    return abs(r["a"]) <= 2.0 * r["sigma_a"] or abs(r["a"]) < PAVIMENTO


def parte_B():
    import _universalita_massa as UM
    print("### PARTE B -- LA CORSA (toro %s x %d, dtau 1, cs = s0 (1 + eta cos(2 pi x/Lx)), W = Lx/16, x0 = Lx/4, T <= Lx/4, finestra |<x> - x0| < Lx/32)"
          % ("/".join(str(L) for L in LX_LISTA), LY))
    assert committata(PREV_JSONL), "la previsione NON e' committata e pulita: la parte B non parte"
    print("  la previsione: %s, committata e pulita, blob %s" % (os.path.relpath(PREV_JSONL, RADICE), UM.blob(os.path.relpath(PREV_JSONL, RADICE))))
    P = [json.loads(l) for l in io.open(PREV_JSONL, encoding="utf-8")]
    vett = {(p["s0"], p["eps"], p["ramo"]): np.array(p["Q_re"]) + 1j * np.array(p["Q_im"]) for p in P if p["tipo"] == "vettore"}
    prev = {(p["s0"], p["eps"], p["ramo"], p["eta"]): p for p in P if p["tipo"] == "previsione"}
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi = lambda r: io.open(JSONL, "a", encoding="utf-8").write(json.dumps(r) + "\n")   # noqa: E731
    scrivi({"tipo": "testata", "blobs": {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py",
                                                                 "csv/_universalita_massa.py", "csv/_forza_da_cs.py",
                                                                 "doc/referti_l2/forza_da_cs_previsione.jsonl")}})
    M = {}
    for (s0, eps, ramo), Q in sorted(vett.items()):
        for Lx in LX_LISTA:
            for eta in ETA_CORSA:
                r = corsa(Lx, eps, s0, eta, Q)
                r["ramo"] = ramo
                M[(s0, eps, ramo, Lx, eta)] = r
                scrivi(dict(r, tipo="corsa"))
                print("  Lx %d eps %-3g s0 %-4g %-6s eta %+.0e: punti %3d  a %s +- %s  v0 %s  fuori %.2e  %s"
                      % (Lx, eps, s0, ramo, eta, r["punti"], "%+.4e" % r["a"] if r["a"] is not None else "--",
                         "%.1e" % r["sigma_a"] if r["sigma_a"] is not None else "--",
                         "%+.2e" % r["v0"] if r["v0"] is not None else "--", r["fuori_max"] if r["fuori_max"] is not None else float("nan"),
                         "" if r["leggibile"] else "### NON LEGGIBILE (" + r["perche"] + ")"))
                sys.stdout.flush()
    chiavi = sorted({(s0, eps, ramo, Lx) for (s0, eps, ramo, Lx, _e) in M})
    ha = lambda r: r["a"] is not None                                                              # noqa: E731
    # ---------------------------------------------------------------- i controlli
    print("### I CONTROLLI")
    falli = [k for k in chiavi if not (ha(M[k + (0.0,)]) and nullo(M[k + (0.0,)]))]
    esito("DEVE PASSARE: eta = 0, |a| <= 2 sigma_a o |a| < 1e-12, su %d righe" % len(chiavi), not falli,
          "; ".join("%s a %s sigma %s" % (k, M[k + (0.0,)]["a"], M[k + (0.0,)]["sigma_a"]) for k in falli))
    falli, peg = [], 0.0
    for k in chiavi:
        for eta in ETA_CONTROLLI:
            p, m = M[k + (eta,)], M[k + (-eta,)]
            if not (ha(p) and ha(m)) or p["a"] == 0.0:
                falli.append((k, eta, "nessun a"))
                continue
            rel = abs(abs(m["a"]) - abs(p["a"])) / abs(p["a"])
            peg = max(peg, rel)
            if not (np.sign(m["a"]) == -np.sign(p["a"]) and rel < TOLL_SPECCHIO):
                falli.append((k, eta, "%.2e" % rel))
    esito("DEVE PASSARE: lo specchio, a(-eta) = -a(eta) entro %g relativo" % TOLL_SPECCHIO, not falli,
          "il peggiore %.2e; %s" % (peg, "; ".join(str(f) for f in falli[:12])))
    falli, lin_ok = [], {}
    for k in chiavi:
        for eta in ETA_CONTROLLI:
            p, h = M[k + (eta,)], M[k + (eta / 2.0,)]
            q = p["a"] / h["a"] if ha(p) and ha(h) and h["a"] != 0.0 else None
            lin_ok[k + (eta,)] = q is not None and abs(q / 2.0 - 1.0) < TOLL_LIN
            if not lin_ok[k + (eta,)]:
                falli.append((k, eta, q))
    esito("DEVE PASSARE: la linearita', a(eta)/a(eta/2) = 2 entro il 5%", not falli,
          "; ".join("%s eta %g: %s" % (k, e, "--" if q is None else "%.4f" % q) for k, e, q in falli[:16]))
    righe_mf = [k for k in chiavi if not prev[(k[0], k[1], k[2], 1e-2)]["a_H_nulla"]]
    chiave_giusta = all(ha(M[k + (1e-2,)]) and np.isfinite(M[k + (1e-2,)]["a"]) and np.isfinite(M[k + (1e-2,)]["sigma_a"]) for k in righe_mf)
    tengono = [k for k in righe_mf if ha(M[k + (1e-2,)]) and nullo(M[k + (1e-2,)])]
    esito("DEVE FALLIRE: <<a = 0>> a eta 1e-2, su %d righe con a_H != 0 (e per la chiave giusta: a, sigma finiti)" % len(righe_mf),
          chiave_giusta and not tengono and len(righe_mf) > 0,
          "|a|/sigma_a: " + ", ".join("%.1e" % (abs(M[k + (1e-2,)]["a"]) / max(M[k + (1e-2,)]["sigma_a"], 1e-300)) for k in righe_mf if ha(M[k + (1e-2,)])))
    for k in chiavi:
        if k not in righe_mf and ha(M[k + (1e-2,)]):
            print("    la MISURA dove a_H = 0: %s eta 1e-2: a %+.4e, sigma_a %.1e, |a|/sigma_a %.2e" % (
                k, M[k + (1e-2,)]["a"], M[k + (1e-2,)]["sigma_a"], abs(M[k + (1e-2,)]["a"]) / max(M[k + (1e-2,)]["sigma_a"], 1e-300)))
    falli, peg, n_t = [], 0.0, 0
    for (s0, eps, ramo) in sorted({k[:3] for k in chiavi}):
        Dt = prev[(s0, eps, ramo, 1e-2)]["Dt"]
        for eta in (1e-3, -1e-3, 1e-2, -1e-2):
            a1, a2 = M[(s0, eps, ramo, 128, eta)], M[(s0, eps, ramo, 256, eta)]
            if not (ha(a1) and ha(a2)):
                continue
            g1, g2 = a1["a"] * 128, a2["a"] * 256
            rel = abs(g1 - g2) / max(abs(0.5 * (g1 + g2)), 1e-300)
            if Dt > SOGLIA_SALTO:
                n_t += 1
                peg = max(peg, rel)
                if rel >= TOLL_TAGLIE:
                    falli.append(((s0, eps, ramo, eta), "%.3f" % rel))
            else:
                print("    taglie SENZA criterio (Dt %.4f <= %g): %s eta %g: %.3f" % (Dt, SOGLIA_SALTO, (s0, eps, ramo), eta, rel))
    esito("TAGLIE (scelta di Luca): a * Lx a 128 e 256 entro il 5%%, catena principale, Dt > %g, su %d valori" % (SOGLIA_SALTO, n_t),
          not falli, "il peggiore %.3f; %s" % (peg, "; ".join(str(f) for f in falli[:12])))
    # ---------------------------------------------------------------- la tabella
    print("### LA TABELLA (eta > 0; per eta < 0 i segni si invertono): a_mis contro le tre previsioni e a_RG")
    tab = []
    for (s0, eps, ramo, Lx) in chiavi:
        for eta in ETA_CONTROLLI:
            r, p = M[(s0, eps, ramo, Lx, eta)], prev[(s0, eps, ramo, eta)]
            q = p["per_Lx"][str(Lx)]
            am = r["a"]
            div = lambda x, y: None if x is None or y in (None, 0.0) else x / y                      # noqa: E731
            riga = {"s0": s0, "eps": eps, "ramo": ramo, "Lx": Lx, "eta": eta, "a_mis": am, "sigma_a": r["sigma_a"],
                    "a_prev": q["a_prev"], "a_prevDt": q["a_prevDt"], "a_H": q["a_H"], "a_RG": q["a_RG"],
                    "mis_su_prev": div(am, q["a_prev"]), "mis_su_prevDt": div(am, q["a_prevDt"]), "mis_su_H": div(am, q["a_H"]),
                    "mis_su_RG": div(am, q["a_RG"]), "leggibile": bool(r["leggibile"] and lin_ok.get((s0, eps, ramo, Lx, eta), False)),
                    "verso_mis": None if am is None or nullo(r) else ("verso cs BASSO" if am / q["a_RG"] > 0 else "verso cs ALTO")}
            tab.append(riga)
            scrivi(dict(riga, tipo="tabella"))
            f = lambda x: "    --    " if x is None else "%+.3e" % x                                 # noqa: E731
            print("  Lx %d eps %-3g s0 %-4g %-6s eta %-5g: a_mis %s (+- %s) | prev %s prev[Dt] %s H %s RG %s | mis/RG %s mis/H %s | %s%s"
                  % (Lx, eps, s0, ramo, eta, f(am), "%.1e" % r["sigma_a"] if r["sigma_a"] is not None else "--",
                     f(q["a_prev"]), f(q["a_prevDt"]), f(q["a_H"]), f(q["a_RG"]), f(riga["mis_su_RG"]), f(riga["mis_su_H"]),
                     riga["verso_mis"] or "nessun verso (a nullo)", "" if riga["leggibile"] else "  ### NON SI LEGGE"))
    # ---------------------------------------------------------------- l'esponente
    print("### L'ESPONENTE: |a_mis/a_RG| contro s0/(1 - s0), fit log-log sui tre s0 (solo i punti leggibili, a non nullo)")
    for (eps, ramo) in sorted({(k[1], k[2]) for k in chiavi}):
        for Lx in LX_LISTA:
            for eta in ETA_CONTROLLI:
                pts = [(t["s0"], abs(t["mis_su_RG"])) for t in tab if t["eps"] == eps and t["ramo"] == ramo and t["Lx"] == Lx and t["eta"] == eta
                       and t["leggibile"] and t["mis_su_RG"] not in (None, 0.0) and t["verso_mis"]]
                if len(pts) >= 2:
                    X = np.log([s / (1.0 - s) for s, _ in pts])
                    Y = np.log([y for _, y in pts])
                    p_ = float(np.polyfit(X, Y, 1)[0])
                else:
                    p_ = None
                scrivi({"tipo": "esponente", "eps": eps, "ramo": ramo, "Lx": Lx, "eta": eta, "punti": len(pts), "p": p_})
                print("  eps %-3g %-6s Lx %d eta %-5g: %d punti, p %s" % (eps, ramo, Lx, eta, len(pts), "--" if p_ is None else "%.3f" % p_))
    print("### I TRIANGOLI: NON in questa misura -- _triangoli.scena fa solo il toro quadrato, e lo spettro (matrice, rami_seguiti, spettro) e' del quadrato")


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    parte = argv[1] if len(argv) > 1 else ""
    assert parte in ("A", "B"), "si gira con A (la previsione) o B (la corsa)"
    print("=" * 100)
    print("IL VERSO E L'INTENSITA' DELLA FORZA DA cs -- PARTE %s" % parte)
    print("=" * 100)
    print("  il passo: %d pezzi, impronta %s (intatto); la camminata sola (S3 saltata); cs per nodo in memoria, lambda_c None" % (len(CM.ORDINE), CM.IMPRONTA))
    print("  la configurazione: L_SPETTRO %d; S_PREV %s; S0 %s; EPS %s; ETA %s; LX %s; LY %d; TOLL_FIT %g; TOLL_DISPERSIVO %g; TOLL_OMEGA %g; TOLL_DISTINTI %g;"
          " SPECCHIO %g; LIN %g; TAGLIE %g; SALTO %g; NORMA_FUORI %g; PAVIMENTO %g; MIN_PUNTI %d; TOLL_NORMA %g"
          % (L_SPETTRO, S_PREV, S0_LISTA, EPS_LISTA, ETA_CORSA, LX_LISTA, LY, TOLL_FIT, TOLL_DISPERSIVO, TOLL_OMEGA, TOLL_DISTINTI,
             TOLL_SPECCHIO, TOLL_LIN, TOLL_TAGLIE, SOGLIA_SALTO, NORMA_FUORI, PAVIMENTO, MIN_PUNTI, TOLL_NORMA))
    print("-" * 100)
    sys.stdout.flush()
    if parte == "A":
        parte_A()
    else:
        parte_B()
        print("=" * 100)
        print("LA FORZA DA cs: %d su %d controlli   %s  (il verdetto di fisica e' il verso e la tabella)"
              % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
        print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
