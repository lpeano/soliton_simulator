r"""**LA LUCE SUI TRIANGOLI: i modi senza massa del settore del vuoto e del sistema accoppiato, e il cono di tutti i settori** *(solo in memoria; [[DECISIONE-SOLO-TRIANGOLI]],
[[LUCE-VINCOLO-LAMPI-GAMMA]])*.

> ### ⛔ **Il task history e' `2026-10-23_triangoli_luce.md`** *(la lettura del codice, il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta, la convenzione nel repo e il
> nucleo intatti.** ### **Importati, non copiati:** `_triangoli` *(`scarto_c6`, `scena_toro`, `scena`, `camminata`)*, `_triangoli_bassa_energia` *(`matrice`, `un_pezzo`)*, `_triangoli_forza` *(`v_max`,
> `matrice_L`, `coppia_K`, `conv`, le soglie del fronte)*, `_stabilita_triangoli.green`, `_stabilita_lineare` *(`copia`, `passo`)*, `_screening_forme_s3.forma`, `_scala_e_zero` *(`H_eff`, `S_LISTA`)*.

### **A** *(il vuoto da solo)* · ### **B** *(il sistema accoppiato, la Green di un tick nel riferimento che ruota)* · ### **C** *(il cono di tutti i settori)*.

Gira con:  python csv/_triangoli_luce.py > doc/referti_l2/triangoli_luce.txt
"""
import io
import json
import math
import os
import subprocess
import sys
import time
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

RIF_BASSA = "8781162c"
RIF_FATTORE = "7daa8840"
NB = 12
NV = 6
L = 48
S_A = (0.02, 0.05, 0.1, 0.3, 0.5)
CONV = ("simm", "oggi")
PUNTI = {"Gamma": (0, 0), "K": (16, 16), "K'": (32, 32), "M": (24, 0)}
K_DISP = (1e-3, 2e-3, 4e-3)
DIREZIONI = 16
TOLL_LIV = 1e-9
TOLL_PIATTA = 1e-9
LB = 48
S_B = (0.05, 0.1, 0.3)
X_B = (1e-4, 1e-3, 1e-2)
FORME = ("S1", "S3", "S4")
EPS_REL = 1e-6
M_LINEA = 6
S_C = (0.05, 0.3, 0.5)
TOLL_C6 = 1e-12
TOLL_PEZZO = 1e-12
TOLL_GREEN = 1e-12
TOLL_RIF = 1e-9
TOLL_LUCE = 0.05
J = np.array([[1.0, 0.0], [-0.5, math.sqrt(3.0) / 2.0]])
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_luce.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-90s %s   %s" % (che[:90], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4f"):
    return "--" if x is None else fm % x


def av(x):
    return float((x + np.pi) % (2.0 * np.pi) - np.pi)


def git_jsonl(rif, rel):
    return [json.loads(x) for x in subprocess.run(["git", "show", "%s:%s" % (rif, rel)], capture_output=True, cwd=RADICE, check=True).stdout.decode("utf-8").splitlines() if x.strip()]


# =====================================================================================
#   IL BLOCCO DEL VUOTO
# =====================================================================================
def vuoto(s, nome, lato=L):
    import _triangoli_bassa_energia as BE
    A = BE.matrice(0.0, s, lato, nome)
    return A[:, :, NB:, NB:].copy(), float(max(np.abs(A[..., :NB, NB:]).max(), np.abs(A[..., NB:, :NB]).max()))


def blocchi_di(V):
    n = V.shape[0]
    AR = np.fft.ifft2(V, axes=(0, 1))
    m = np.arange(n)
    m = np.where(m > n // 2, m - n, m)
    return [(int(m[i]), int(m[j]), AR[i, j]) for i in range(n) for j in range(n) if float(np.abs(AR[i, j]).max()) > 1e-14]


def V_di(bl, t1, t2):
    return sum(B * np.exp(-1j * (t1 * r1 + t2 * r2)) for r1, r2, B in bl)


def fasi(M):
    return np.sort(-np.angle(np.linalg.eigvals(M)))


def livelli(w):
    out = []
    for x in np.sort(w):
        if out and abs(x - out[-1][0]) < TOLL_LIV:
            out[-1][1] += 1
        else:
            out.append([float(x), 1])
    return out


def dispersione(bl, punto, w0, molt):
    """### Da un punto speciale, lungo `DIREZIONI` direzioni: ### **i `molt` livelli piu' vicini a `w0` a `k` in `K_DISP`** *(cartesiano)*, ### **`delta omega`, l'esponente** *(fra il primo e il terzo `k`)*,
    ### **la pendenza al `k` piu' piccolo.**"""
    t0 = 2.0 * np.pi * np.array(punto, dtype=float) / L
    per_dir = []
    for phi_ in np.linspace(0.0, np.pi, DIREZIONI, endpoint=False):
        n_ = np.array([math.cos(phi_), math.sin(phi_)])
        dd = []
        for k in K_DISP:
            th = t0 + J @ (k * n_)
            w = -np.angle(np.linalg.eigvals(V_di(bl, th[0], th[1])))
            d = np.sort(np.abs([av(x - w0) for x in w]))[:molt]
            dd.append(d)
        dd = np.array(dd)
        per_dir.append(dd)
    per_dir = np.array(per_dir)                                  # (dir, k, molt)
    rami = []
    for j in range(molt):
        d1, d3 = per_dir[:, 0, j], per_dir[:, 2, j]
        if float(np.max(d3)) < 1e-12:
            rami.append({"tipo": "piatto", "esponente": None, "pendenza": None, "anisotropia": None, "delta_max": float(np.max(d3))})
            continue
        p = float(np.median(np.log(d3 / np.maximum(d1, 1e-300)) / math.log(K_DISP[2] / K_DISP[0])))
        tipo = "lineare" if 0.9 <= p <= 1.1 else ("quadratico" if 1.9 <= p <= 2.1 else "altro")
        sl = d1 / K_DISP[0]
        rami.append({"tipo": tipo, "esponente": p, "pendenza": float(np.mean(sl)) if tipo == "lineare" else None,
                     "anisotropia": float((np.max(sl) - np.min(sl)) / np.mean(sl)) if tipo == "lineare" else None,
                     "curvatura": float(np.mean(2.0 * per_dir[:, 2, j] / K_DISP[2] ** 2)) if tipo == "quadratico" else None, "delta_max": float(np.max(d3))})
    return rami


def fronte_vuoto(s):
    """### Il fronte di un impulso su `phi` a un nodo *(le `6` componenti uguali)*, ### **toro `L_FRONTE x L_FRONTE`, zero simmetrico, le soglie di `_triangoli_forza`.**"""
    import _triangoli as T
    import _triangoli_forza as TF
    vero = T.EPS_MONETA
    T.EPS_MONETA = 0.0
    try:
        inc, mot, st, par = T.scena_toro(T.TRIANGOLI, (TF.L_FRONTE, TF.L_FRONTE), s, T.X)
    finally:
        T.EPS_MONETA = vero
    n = inc.n
    Lf = TF.L_FRONTE
    m1, m2 = np.arange(n) // Lf, np.arange(n) % Lf
    d1 = (m1 + Lf // 2) % Lf - Lf // 2
    d2 = (m2 + Lf // 2) % Lf - Lf // 2
    r = np.hypot(d1 - 0.5 * d2, math.sqrt(3.0) / 2.0 * d2)
    o = np.argsort(r, kind="stable")
    for k in st:
        st[k][...] = 0
    st["phi_h"].reshape(n, NV)[0] = 1.0 / math.sqrt(NV)
    fr = {}
    with TF.conv("simm"):
        for t in range(1, max(TF.T_FRONTE) + 1):
            T.camminata(st, mot, par)
            if t in TF.T_FRONTE:
                w = np.abs(st["phi_h"].reshape(n, NV)) ** 2
                w = np.sum(w, axis=1)
                w = w / w.sum()
                coda = np.cumsum(w[o][::-1])[::-1]
                fr[t] = {thr: float(r[o][int(np.argmax(coda < thr))]) for thr in TF.SOGLIE}
    t0, t1 = TF.T_FRONTE
    dentro = max(max(d.values()) for d in fr.values()) < TF.DENTRO * Lf * math.sqrt(3.0) / 4.0
    return {str(thr): (fr[t1][thr] - fr[t0][thr]) / (t1 - t0) for thr in TF.SOGLIE}, dentro


def parte_A():
    import _scala_e_zero as Z
    import _triangoli as T
    import _triangoli_bassa_energia as BE
    print("### PARTE A -- IL VUOTO DA SOLO (materia nulla; lato %d; la dispersione lungo %d direzioni a k %s)" % (L, DIREZIONI, K_DISP))
    peg_c6, peg_fuori, out = 0.0, 0.0, {}
    for s in S_A:
        for nome in CONV:
            V, fuori = vuoto(s, nome)
            peg_fuori = max(peg_fuori, fuori)
            peg_c6 = max(peg_c6, float(T.scarto_c6(V)))
            bl = blocchi_di(V)
            W = -np.angle(np.linalg.eigvals(V))
            liv_G = livelli(W[0, 0])
            piatte = [w for w, m_ in liv_G if all(np.min(np.abs([av(x - w) for x in W[i, j]])) < TOLL_PIATTA for i in range(L) for j in range(L))]
            tocchi = []
            for pn, pk in PUNTI.items():
                for w, m_ in livelli(W[pk]):
                    if m_ > 1 or abs(av(w)) < TOLL_LIV:
                        rami = dispersione(bl, pk, w, m_)
                        if all(r["tipo"] == "piatto" for r in rami):
                            continue
                        tocchi.append({"punto": pn, "livello": w, "molteplicita": m_, "rami": rami})
            # ### la v di Einstein della banda dispersiva semplice a Gamma (col simmetrico: +pi s)
            ein = None
            if nome == "simm":
                for w, m_ in liv_G:
                    if m_ == 1:
                        r = dispersione(bl, (0, 0), w, 1)[0]
                        if r["tipo"] == "quadratico":
                            ein = {"livello": w, "curvatura": r["curvatura"], "v_b": math.sqrt(abs(w) * r["curvatura"]), "v_b_su_s": math.sqrt(abs(w) * r["curvatura"]) / s}
            rec = {"tipo": "vuoto", "s": s, "conv": nome, "livelli": {pn: livelli(W[pk]) for pn, pk in PUNTI.items()}, "piatte": piatte, "tocchi": tocchi, "einstein": ein}
            out[(s, nome)] = rec
            scrivi(rec)
            print("  s %-4g %-4s: i livelli %s | piatte %s" % (s, nome, " | ".join("%s %s" % (pn, " ".join("%+.4f(%d)" % (w, m_) for w, m_ in lv)) for pn, lv in rec["livelli"].items()),
                                                         " ".join("%+.4f" % w for w in piatte)))
            for tc in tocchi:
                print("     tocco a %s, livello %+.5f (x%d): %s" % (tc["punto"], tc["livello"], tc["molteplicita"], "; ".join(
                    "%s esp %s pend/s %s aniso %s" % (r["tipo"], f_(r["esponente"], "%.3f"), f_(r["pendenza"] and r["pendenza"] / s, "%.4f"), f_(r["anisotropia"], "%.1e")) for r in tc["rami"])))
            if ein:
                print("     Einstein della banda dispersiva a Gamma (+pi s): curvatura %.5f, v_b,vuoto/s %.4f" % (ein["curvatura"], ein["v_b_su_s"]))
            sys.stdout.flush()
    esito("DI SERVIZIO: il blocco materia-vuoto della camminata e' nullo", peg_fuori == 0.0, "%.1e" % peg_fuori)
    esito("DEVE PASSARE: lo spettro del vuoto invariante per 60 gradi (scarto_c6 sul cerchio) entro %g, ogni s e convenzione" % TOLL_C6, peg_c6 < TOLL_C6, "il peggiore %.2e" % peg_c6)
    # ---- un pezzo solo, sul blocco del vuoto
    SS = (Z.S_LISTA[0],) + tuple(x for x in Z.S_LISTA if x > Z.S_LISTA[0])
    peg = 0.0
    for pz in ("CAMM-GROVER-VUOTO", "CAMM-SPOSTAMENTO-VUOTO"):
        for (a, b) in ((0, 0), (1, 0)):
            Hs = {}
            for x in SS:
                with BE.un_pezzo(pz):
                    B = BE.matrice(0.0, x, 16, "oggi")[a, b, NB:, NB:]
                lam, VV = np.linalg.eig(B)
                Hs[x] = Z.H_eff(VV, -np.angle(lam), x)
            n0 = np.linalg.norm(Hs[SS[0]])
            d = max(float(np.linalg.norm(Hs[x] - Hs[SS[0]]) / n0) for x in SS) if n0 > 0 else 0.0
            peg = max(peg, d)
            print("  un pezzo solo, %s a k %s: delta(s) massimo %.1e (||H_eff|| %.3f)" % (pz, (a, b), d, n0))
    esito("DEVE PASSARE: un pezzo solo (GROVER-VUOTO, SPOSTAMENTO-VUOTO) sul blocco del vuoto, delta(s) < %g" % TOLL_PEZZO, peg < TOLL_PEZZO, "il peggiore %.1e" % peg)
    # ---- il fronte del solo vuoto
    fronti = {}
    for s in S_A:
        vf, dentro = fronte_vuoto(s)
        fronti[s] = vf
        scrivi({"tipo": "fronte_vuoto", "s": s, "v_fronte": vf, "dentro": dentro})
        print("  il fronte del vuoto a s %g: %s%s" % (s, " ".join("thr %s: /s %.4f" % (k, v / s) for k, v in vf.items()), "" if dentro else " ### FUORI DAL TORO"))
    return out, fronti


# =====================================================================================
#   PARTE B -- IL SISTEMA ACCOPPIATO
# =====================================================================================
def base_uniforme(s, x, nome):
    """### La materia uniforme sul vettore della banda alta della coppia a `Gamma` *(oggi `0`, doppio: il primo)*, a `rho/Lambda = x`; `phi = 1`. ### La stazionarieta' di un tick."""
    import _stabilita_lineare as SL
    import _triangoli as T
    import _triangoli_bassa_energia as BE
    A = BE.matrice(0.0, s, 6, "oggi")
    lam, V = np.linalg.eig(A[0, 0, :NB, :NB])
    w = -np.angle(lam)
    i0 = [i for i in range(NB) if abs(av(w[i])) < TOLL_LIV]
    assert len(i0) == 2, "il livello 0 a Gamma non e' doppio: %s" % w
    e = V[:, i0[0]]
    vero = T.EPS_MONETA
    T.EPS_MONETA = 0.0
    try:
        inc, mot, st, par = T.scena(T.TRIANGOLI, LB, s, T.X)
    finally:
        T.EPS_MONETA = vero
    n = inc.n
    if x > 0.0:
        st["psi_h"][...] = np.tile(e, n).reshape(st["psi_h"].shape)
        lv = float(np.mean(mot.densita_vuoto(st)))
        rh = float(np.mean(mot.densita_materia(st)))
        st["psi_h"] *= math.sqrt(x * lv / rh)
    else:
        st["psi_h"][...] = 0.0
    return inc, mot, st, par


def rotazioni(st, dopo):
    out = {}
    for k in ("psi_h", "phi_h"):
        a, b = st[k].reshape(-1), dopo[k].reshape(-1)
        nn = np.vdot(a, a).real
        if nn == 0.0:
            out[k] = (0.0, 0.0)
            continue
        c = np.vdot(a, b) / nn
        out[k] = (float(-np.angle(c)), float(np.linalg.norm(b - c * a) / math.sqrt(nn)))
    return out


def parte_B(pa):
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli_forza as TF
    print("### PARTE B -- IL SISTEMA ACCOPPIATO (la Green di un tick, lato %d, eps_rel %g, nel riferimento che ruota; la base: la banda alta della coppia a Gamma)" % (LB, EPS_REL))
    # ---- a materia nulla: il blocco phi -> phi contro A_v
    nc = NB + NV
    idx = list(range(NB, nc)) + list(range(nc + NB, 2 * nc))
    peg = 0.0
    for s in S_B:
        for nome in CONV:
            inc, mot, st, par = base_uniforme(s, 0.0, nome)
            with TF.conv(nome):
                R, _ = ST.green(st, mot, par, (), LB, (1.0, 1.0), 1.0, 3)
            Vv, _f = vuoto(s, nome, LB)
            # ### ⚠ la Green lavora sulle coordinate REALI: la sua trasformata accoppia `k` e `-k` -- `Re` e `Im` della mappa in spazio reale danno `(V(k) + V(-k)*)/2` e `(V(k) - V(-k)*)/2i`
            ii = (-np.arange(LB)) % LB
            Vm = np.conj(Vv[ii][:, ii])
            Re_, Im_ = 0.5 * (Vv + Vm), (Vv - Vm) / 2j
            Rr = np.block([[Re_, -Im_], [Im_, Re_]])
            peg = max(peg, float(np.abs(R[:, :, idx][:, :, :, idx] - Rr).max()))
    esito("DEVE PASSARE: a materia nulla il blocco phi -> phi della Green = il blocco del vuoto entro %g" % TOLL_GREEN, peg < TOLL_GREEN, "il peggiore %.1e" % peg)
    righe = []
    for forma in FORME:
        for s in S_B:
            for x in X_B:
                for nome in CONV:
                    t0 = time.time()
                    inc, mot, st, par = base_uniforme(s, x, nome)
                    with SF.forma(forma), TF.conv(nome):
                        dopo = SL.copia(st)
                        SL.passo(dopo, mot, par, False, (), 0.0)
                        rot = rotazioni(st, dopo)
                        scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
                        R, _ = ST.green(st, mot, par, (), LB, scale, EPS_REL, 3)
                    om, ov = rot["psi_h"][0], rot["phi_h"][0]
                    P = np.zeros((2 * nc, 2 * nc))
                    for c in range(nc):
                        w = om if c < NB else ov
                        P[c, c], P[c, c + nc], P[c + nc, c], P[c + nc, c + nc] = math.cos(w), -math.sin(w), math.sin(w), math.cos(w)
                    lam = np.linalg.eigvals(np.matmul(P, R))
                    lnm = np.log(np.max(np.abs(lam), axis=-1))
                    tasso = float(np.max(lnm)) / s
                    kk = np.unravel_index(int(np.argmax(lnm)), lnm.shape)
                    # ### i rami piu' bassi lungo theta_1 da Gamma
                    ang = [np.sort(np.abs(np.angle(lam[m, 0]))) for m in range(M_LINEA + 1)]
                    zeri = int(np.sum(ang[0] < 1e-6))
                    kc = [2.0 * np.pi * m / LB * 2.0 / math.sqrt(3.0) for m in range(M_LINEA + 1)]
                    # ### il primo ramo che a Gamma e' nullo e a k > 0 no: l'angolo al posto zeri (le coppie +- contano due)
                    j = 0
                    while j < len(ang[1]) and ang[1][j] < 1e-9:
                        j += 1
                    rami = []
                    for q in range(j, min(j + 4, len(ang[1])), 2):
                        y = [float(ang[m][q]) for m in range(1, M_LINEA + 1)]
                        p = math.log(y[3] / y[0]) / math.log(kc[4] / kc[1]) if y[0] > 0 else None
                        rami.append({"angoli": y, "esponente": p, "v_su_s": y[0] / kc[1] / s})
                    rec = {"tipo": "accoppiato", "forma": forma, "s": s, "x": x, "conv": nome, "rotazioni": rot, "tasso": tasso, "k_tasso": [int(kk[0]), int(kk[1])], "zeri_Gamma": zeri,
                           "rami": rami}
                    scrivi(rec)
                    righe.append(rec)
                    print("  %s s %-4g x %-6g %-4s: staz psi %.1e phi %.1e | tasso %+.3e a k %s | zeri a Gamma %d | i rami bassi: %s (%.0f s)"
                          % (forma, s, x, nome, rot["psi_h"][1], rot["phi_h"][1], tasso, rec["k_tasso"], zeri,
                             "; ".join("ang(m=1) %.2e esp %s v/s %.4f" % (r["angoli"][0], f_(r["esponente"], "%.2f"), r["v_su_s"]) for r in rami), time.time() - t0))
                    sys.stdout.flush()
    return righe


# =====================================================================================
#   PARTE C -- IL CONO DI TUTTI I SETTORI
# =====================================================================================
def parte_C(fronti):
    import _triangoli_forza as TF
    print("### PARTE C -- IL CONO DI TUTTI I SETTORI (v_max della materia e del vuoto: _triangoli_forza.v_max; il vuoto al posto della materia, un'identita' nel resto)")
    fat = {(r["eps"], r["s"]): r for r in git_jsonl(RIF_FATTORE, "doc/referti_l2/triangoli_fattore.jsonl") if r.get("tipo") == "fattori" and r["banda"] == 0}
    righe = []
    for s in S_C:
        vm, _k, _w = TF.v_max(TF.matrice_L(0.0, s))
        V, _f = vuoto(s, "simm")
        A2 = np.zeros((L, L, NB + NV, NB + NV), dtype=complex)
        A2[:, :, :NV, :NV] = V
        A2[:, :, NV:NB, NV:NB] = np.eye(NB - NV)
        vv, kv, wv = TF.v_max(A2)
        vb = fat[(0.0, s)]["fattori"]["v_b"]["c"]
        cono = max(vm, vv)
        rec = {"tipo": "cono", "s": s, "v_max_materia": vm, "v_max_vuoto": vv, "k_vuoto": list(kv), "cono": cono, "v_b": vb, "cono_su_v_b": cono / vb,
               "v_fronte_vuoto": fronti.get(s)}
        scrivi(rec)
        righe.append(rec)
        print("  s %g: v_max materia/s %.4f  vuoto/s %.4f (a k %s)  il cono/s %.4f | v_b/s %.4f (%s) | cono/v_b %.4f" % (s, vm / s, vv / s, kv, cono / s, vb / s, RIF_FATTORE, cono / vb))
        sys.stdout.flush()
    return righe


def main(argv):
    del argv
    import _presidio
    import _triangoli_forza as TF
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 110)
    print("LA LUCE SUI TRIANGOLI: i modi senza massa del vuoto e del sistema accoppiato, e il cono di tutti i settori")
    print("=" * 110)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py", "csv/_triangoli_forza.py", "csv/_triangoli_fattore.py",
                                     "csv/_stabilita_triangoli.py", "csv/_stabilita_lineare.py", "csv/_screening_forme_s3.py", "csv/_scala_e_zero.py", "csv/_zero_simmetrico.py",
                                     "csv/_triangoli_luce.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: RIF %s %s; L %d; S_A %s; CONV %s; PUNTI %s; K_DISP %s; DIREZIONI %d; LB %d; S_B %s; X_B %s; FORME %s; EPS_REL %g; M_LINEA %d; S_C %s;"
          % (RIF_BASSA, RIF_FATTORE, L, S_A, CONV, PUNTI, K_DISP, DIREZIONI, LB, S_B, X_B, FORME, EPS_REL, M_LINEA, S_C))
    print("    TOLL_LIV %g TOLL_PIATTA %g TOLL_C6 %g TOLL_PEZZO %g TOLL_GREEN %g TOLL_RIF %g TOLL_LUCE %g; il fronte: L %d, T %s, soglie %s"
          % (TOLL_LIV, TOLL_PIATTA, TOLL_C6, TOLL_PEZZO, TOLL_GREEN, TOLL_RIF, TOLL_LUCE, TF.L_FRONTE, TF.T_FRONTE, TF.SOGLIE))
    print("-" * 110)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    pa, fronti = parte_A()
    # ---- DEVE FALLIRE: la materia a eps 0 ha un modo senza massa
    rif = [r for r in git_jsonl(RIF_BASSA, "doc/referti_l2/triangoli_bassa_energia.jsonl") if r.get("tipo") == "salto_minimo" and r["eps"] == 0.0 and r["s"] == 0.05]
    b0, b1 = TF.coppia_K(0.0, 0.05)
    salto = abs(b1["w"] - b0["w"])
    chiave = bool(rif) and abs(salto - rif[0]["salto"]) < TOLL_RIF
    esito("DEVE FALLIRE: <<la materia a eps 0 ha un modo senza massa>> (il salto della coppia a K < 1e-6, s 0.05; la chiave: = %s entro %g)" % (RIF_BASSA, TOLL_RIF),
          chiave and not salto < 1e-6, "il salto %.6f (%s: %s)" % (salto, RIF_BASSA, f_(rif[0]["salto"] if rif else None, "%.6f")))
    lin = [(s, nome, tc, r) for (s, nome), rec in pa.items() for tc in rec["tocchi"] for r in tc["rami"] if r["tipo"] == "lineare"]
    lin05 = [z for z in lin if z[0] == 0.05]
    esito("PUO' FALLIRE: esiste un modo senza massa LINEARE del vuoto a s 0.05", bool(lin05), "%d rami lineari a s 0.05 (in tutto %d)" % (len(lin05), len(lin)))
    vl = [r["pendenza"] / 0.05 for _s, _n, _t, r in lin05]
    esito("PUO' FALLIRE: |v_luce/s - 0.785|/0.785 < %g a s 0.05 (la luce va a v_b)" % TOLL_LUCE, bool(vl) and all(abs(v - 0.785) / 0.785 < TOLL_LUCE for v in vl),
          " ".join("%.4f" % v for v in vl) or "nessun v_luce: nessun modo lineare")
    print("-" * 110)
    parte_B(pa)
    print("-" * 110)
    rc = parte_C(fronti)
    esito("PUO' FALLIRE: il cono di tutti i settori >= v_b (ogni s di C)", all(r["cono"] >= r["v_b"] for r in rc), " ".join("%.4f" % r["cono_su_v_b"] for r in rc))
    print("=" * 110)
    print("LA LUCE SUI TRIANGOLI: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
