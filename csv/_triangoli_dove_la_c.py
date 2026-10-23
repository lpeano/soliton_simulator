r"""**DOVE NASCE UN MODO SENZA MASSA SUI TRIANGOLI (LA `c` DEL MODELLO): il regime `s -> 1`, la moneta, la particella vestita dal vuoto** *(solo spettri, in memoria;
[[DECISIONE-SOLO-TRIANGOLI]], [[LUCE-VINCOLO-LAMPI-GAMMA]], [[SPAZIOTEMPO-3PIU1]])*.

> ### ⛔ **Il task history e' `2026-10-24_triangoli_dove_la_c.md`** *(il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta, la convenzione nel repo e il nucleo intatti.**
> ### **Importati, non copiati:** `_triangoli_dove_la_luce.riga` *(le parti `A` e `B`)*, `_triangoli` *(`scena`, `celle`, `ruota60`)*, `_triangoli_forza` *(`coppia_K`, `blocchi`, `spazi_banda`, `conv`, `v_max`, `matrice_L`)*,
> `_triangoli_fattore.ramo_lungo`, `_stabilita_triangoli.perturba`, `_stabilita_lineare` *(`copia`, `passo`)*, `_screening_forme_s3` *(`forma`, `_ab`)*.

### **«Modo senza massa», non «luce»** *(la precisazione di Luca)*. ### **LE PAROLE:** ### **«il limite `s <= 1`», «il regime `s -> 1`», «`v_max`».**

Gira con:  python csv/_triangoli_dove_la_c.py > doc/referti_l2/triangoli_dove_la_c.txt
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
RIF_LUCE = "77f9f850"
NB = 12
NV = 6
LC = 48
S_A = (0.5, 0.7, 0.9, 0.95, 0.99, 0.999, 1.0)
S_B = (0.05, 0.3, 0.5, 0.9)
EPS_B = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0, math.pi / 2.0)
S_C = (0.1, 0.3, 0.5)
EPS_C = (0.0, 0.5)
X_C = (1e-4, 1e-3, 1e-2, 1e-1)
X_ZERO = 1e-8
FORME = ("S1", "S3", "S4")
E_REL = 1e-4
J_MAX = 4
M_LINEA = 6
TOLL_RIF = 1e-9
TOLL_VMAX = 1e-6
TOLL_C6 = 1e-12
TOLL_C3 = 1e-9
TOLL_STAZ = 1e-12
TOLL_NUDA = 1e-4
TOLL_UNO = 0.01
TOLL_5 = 0.05
STABILE = 1e-6
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_dove_la_c.jsonl")
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
#   PARTE C -- LA PARTICELLA VESTITA DAL VUOTO
# =====================================================================================
def scena_onda(eps, s, x, u, q):
    """### La scena coi triangoli, `psi = e^{i (K + q).r} u` riscalata a `rho/Lambda = x`, `phi = 1`; ### **`q` lungo `theta_1`.**"""
    import _triangoli as T
    vero = T.EPS_MONETA
    T.EPS_MONETA = eps
    try:
        inc, mot, st, par = T.scena(T.TRIANGOLI, LC, s, T.X)
    finally:
        T.EPS_MONETA = vero
    n = inc.n
    m1, m2 = (np.arange(n) // LC).astype(float), (np.arange(n) % LC).astype(float)
    ph = (2.0 * np.pi / 3.0 + q) * m1 + 2.0 * np.pi / 3.0 * m2
    st["psi_h"][...] = (np.exp(1j * ph)[:, None] * u[None, :]).reshape(st["psi_h"].shape)
    lv = float(np.mean(mot.densita_vuoto(st)))
    rh = float(np.mean(mot.densita_materia(st)))
    st["psi_h"] *= math.sqrt(x * lv / rh)
    return inc, mot, st, par, ph


def un_tick(st, mot, par, forma):
    """### Un tick del passo intero con la forma in memoria, zero simmetrico: ### **le due fasi globali e i residui della stazionarieta'.**"""
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    import _triangoli_forza as TF
    with SF.forma(forma), TF.conv("simm"):
        d = SL.copia(st)
        SL.passo(d, mot, par, False, (), 0.0)
    out = {}
    for k in ("psi_h", "phi_h"):
        a, b = st[k].reshape(-1), d[k].reshape(-1)
        c = np.vdot(a, b) / np.vdot(a, a).real
        out[k] = (float(-np.angle(c)), float(np.linalg.norm(b - c * a) / np.linalg.norm(a)))
    return out


def famiglia(eps, s, x, b, spazi, forma):
    """### Le onde piane `e^{i (K+q).r} u(q)`, `q = 2 pi j/LC`, `j` in `(-J_MAX..J_MAX)`: ### **`omega(q)` di un tick** *(la particella VESTITA)*, ### **`omega(0)`, `omega''` col Richardson** *(cartesiano `x 3/4`)*, ### **`v_b`,
    il fit iperbolico** *(`j` da `0` a `J_MAX`)*, ### **il residuo peggiore della stazionarieta'.**"""
    k1 = 2.0 * np.pi / LC
    w, res = {}, 0.0
    for j in range(-J_MAX, J_MAX + 1):
        q = k1 * j
        Qq = spazi[q]
        u = Qq @ (Qq.conj().T @ b["Q"][:, 0])
        u = u / np.linalg.norm(u)
        inc, mot, st, par, _ph = scena_onda(eps, s, x, u, q)
        r = un_tick(st, mot, par, forma)
        w[j] = r["psi_h"][0]
        res = max(res, r["psi_h"][1], r["phi_h"][1])
        if j == 0:
            ov = r["phi_h"][0]
    for j in range(-J_MAX, J_MAX + 1):
        w[j] = w[0] + av(w[j] - w[0])
    om2 = (-w[2] + 16 * w[1] - 30 * w[0] + 16 * w[-1] - w[-2]) / (12 * k1 * k1) * 0.75
    kk = np.array([j * k1 * 2.0 / math.sqrt(3.0) for j in range(0, J_MAX + 1)])
    y = np.array([w[j] ** 2 - w[0] ** 2 for j in range(0, J_MAX + 1)])
    c, *_ = np.linalg.lstsq(np.stack([kk ** 2, kk ** 4], axis=1), y, rcond=None)
    return {"omega0": w[0], "omega_vuoto": ov, "omega2": float(om2), "v_b": math.sqrt(w[0] * om2) if w[0] * om2 > 0 else None,
            "v_fit": math.sqrt(c[0]) if c[0] > 0 else None, "staz": res}


def nuda(eps, s, b):
    """### La particella NUDA: le fasi della camminata sola a `K + q` *(`_triangoli_fattore.ramo_lungo`)*, ### **lo stesso Richardson e la stessa `v_b`.**"""
    import _triangoli_fattore as TFa
    import _triangoli_forza as TF
    k1 = 2.0 * np.pi / LC
    qq, ww = TFa.ramo_lungo(TF.blocchi(eps, s), b["Q"], b["w"], 2 * k1, 2)
    w0, w1, w2 = ww
    om2 = (-w2 + 16 * w1 - 30 * w0 + 16 * w1 - w2) / (12 * k1 * k1) * 0.75
    return {"omega0": float(w0), "omega2": float(om2), "v_b": math.sqrt(w0 * om2) if w0 * om2 > 0 else None}


def green_gauge(st, mot, par, ph, forma):
    """### La Green di un tick NEL GAUGE `delta psi = e^{i K.r} eta`, ### **differenze CENTRATE** *(`e = E_REL` della scala)*: `R(q)` `(LC, LC, 36, 36)` sulle coordinate reali di `eta` e `delta phi`."""
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli as T
    import _triangoli_forza as TF
    n = LC * LC
    nc = NB + NV
    gauge = np.concatenate([np.repeat(np.exp(-1j * ph)[:, None], NB, axis=1), np.ones((n, NV))], axis=1)
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))

    def risposta(j, e):
        p = SL.copia(st)
        ST.perturba(p, j, e, 3)
        with SF.forma(forma), TF.conv("simm"):
            SL.passo(p, mot, par, False, (), 0.0)
        z = T.celle(p, n, 3) * gauge
        return np.concatenate([z.real, z.imag], axis=1)
    R = np.empty((LC, LC, 2 * nc, 2 * nc), dtype=complex)
    for j in range(2 * nc):
        e = E_REL * scale[0 if (j % nc) < NB else 1]
        dd = (risposta(j, e) - risposta(j, -e)) / (2.0 * e)
        R[:, :, :, j] = np.fft.fft2(dd.reshape(LC, LC, 2 * nc), axes=(0, 1))
    return R


def analisi_green(R, om, ov):
    nc = NB + NV
    P = np.zeros((2 * nc, 2 * nc))
    for c in range(nc):
        w = om if c < NB else ov
        P[c, c], P[c, c + nc], P[c + nc, c], P[c + nc, c + nc] = math.cos(w), -math.sin(w), math.sin(w), math.cos(w)
    lam = np.linalg.eigvals(np.matmul(P, R))
    lnm = np.log(np.max(np.abs(lam), axis=-1))
    k1c = 2.0 * np.pi / LC * 2.0 / math.sqrt(3.0)
    # ### il ramo per 0 a q = 0 lungo theta_1: l'angolo piu' piccolo NON nullo a ogni passo
    y = []
    for m in range(1, M_LINEA + 1):
        a = np.sort(np.abs(np.angle(lam[m, 0])))
        a = a[a > 1e-9]
        y.append(float(a[0]) if len(a) else 0.0)
    p = math.log(y[3] / y[0]) / math.log(4.0) if (y[0] > 0 and y[3] > 0) else None
    tipo = "lineare" if (p is not None and 0.9 <= p <= 1.1) else ("quadratico" if (p is not None and 1.8 <= p <= 2.2) else "altro")
    # ### v_max dell'accoppiato: lungo tre linee, gli autovalori di due q vicini ACCOPPIATI sul piano complesso (l'assegnamento ungherese: annotazione 1), la pendenza delle fasi accoppiate (una stima)
    from scipy.optimize import linear_sum_assignment
    vm = 0.0
    for linea, dk in (([(m, 0) for m in range(LC + 1)], k1c), ([(0, m) for m in range(LC + 1)], k1c), ([(m, m) for m in range(LC + 1)], k1c * math.sqrt(3.0))):
        for (a1, b1), (a2, b2) in zip(linea[:-1], linea[1:]):
            l1, l2 = lam[a1 % LC, b1 % LC], lam[a2 % LC, b2 % LC]
            r, c = linear_sum_assignment(np.abs(l1[:, None] - l2[None, :]))
            vm = max(vm, float(np.max(np.abs([av(x) for x in np.angle(l2[c]) - np.angle(l1[r])]))) / dk)
    return {"tasso": float(np.max(lnm)), "ramo": y, "esponente": p, "tipo": tipo, "v_suono": y[0] / k1c if tipo == "lineare" else None,
            "omega2_goldstone": 2.0 * y[0] / k1c ** 2 if tipo == "quadratico" else None, "v_max_stima": vm, "lam": lam}


def c3(lam):
    """### Gli autovalori a `q` e a `q` ruotato di `120` gradi *(due volte `_triangoli.ruota60`)*, accoppiati con l'assegnamento ungherese: lo scarto massimo."""
    import _triangoli as T
    from scipy.optimize import linear_sum_assignment
    B = T.ruota60(T.ruota60(lam))
    peg = 0.0
    for i in range(LC):
        for j in range(LC):
            D = np.abs(lam[i, j][:, None] - B[i, j][None, :])
            r, c = linear_sum_assignment(D)
            peg = max(peg, float(D[r, c].max()))
    return peg


def parte_C():
    import _triangoli_dove_la_luce as DL
    import _triangoli_forza as TF
    print("### PARTE C -- LA PARTICELLA VESTITA DAL VUOTO (la base e^{i K.r} u_K, il legame acceso; la cella di tre nodi come gauge; la Green centrata, e %g; lato %d; zero simmetrico)" % (E_REL, LC))
    k1 = 2.0 * np.pi / LC
    righe, peg_c3, nude_ok = [], 0.0, []
    for eps in EPS_C:
        for s in S_C:
            bande = TF.coppia_K(eps, s)
            bl = TF.blocchi(eps, s)
            # ### ⚠ v_max per il rapporto: quello NUDO di tutti i settori (annotazione 1: la stima dalla Green sbaglia agli incroci)
            vmax_nudo = DL.vmax_tutti(eps, s)["tutti"]
            for q_, b in enumerate(bande):
                spazi = TF.spazi_banda(bl, b["Q"], "A", [k1 * j for j in range(-J_MAX, J_MAX + 1)])
                nu = nuda(eps, s, b)
                print("  eps %g s %g banda %d: NUDA omega0 %+.6f omega'' %+.6f v_b/s %s | v_max nudo/s %.4f" % (eps, s, q_, nu["omega0"], nu["omega2"], f_(nu["v_b"] and nu["v_b"] / s, "%.5f"), vmax_nudo / s))
                for forma in FORME:
                    for x in ((X_ZERO,) if forma != "S3" else ()) + X_C:
                        t0 = time.time()
                        fa = famiglia(eps, s, x, b, spazi, forma)
                        rec = {"tipo": "vestita", "eps": eps, "s": s, "banda": q_, "forma": forma, "x": x, "famiglia": fa, "nuda": nu, "v_max_nudo": vmax_nudo}
                        if fa["staz"] > TOLL_STAZ:
                            rec["non_stazionaria"] = True
                            scrivi(rec)
                            righe.append(rec)
                            print("    %s x %-6g: ### NON STAZIONARIA (residuo %.1e): il punto NON si misura" % (forma, x, fa["staz"]))
                            continue
                        if x == X_ZERO:
                            nude_ok.append((forma, eps, s, q_, abs(fa["v_b"] - nu["v_b"]) / nu["v_b"] if (fa["v_b"] and nu["v_b"]) else float("inf")))
                            scrivi(rec)
                            righe.append(rec)
                            print("    %s x %-6g: omega0 %+.6f v_b/s %s -- contro la nuda %.1e" % (forma, x, fa["omega0"], f_(fa["v_b"] and fa["v_b"] / s, "%.5f"), nude_ok[-1][-1]))
                            continue
                        inc, mot, st, par, ph = scena_onda(eps, s, x, b["Q"][:, 0], 0.0)
                        R = green_gauge(st, mot, par, ph, forma)
                        an = analisi_green(R, fa["omega0"], fa["omega_vuoto"])
                        if forma == "S1" and x == X_C[-1]:
                            peg_c3 = max(peg_c3, c3(an["lam"]))
                        an.pop("lam")
                        rec.update(green=an, v_b_su_v_max=fa["v_b"] / vmax_nudo if fa["v_b"] else None,
                                   stabile=bool(an["tasso"] <= STABILE))
                        scrivi(rec)
                        righe.append(rec)
                        print("    %s x %-6g: staz %.1e | omega0 %+.6f (nuda %+.6f) omega'' %+.6f v_b/s %s v_fit/s %s | tasso %+.2e %s | il ramo per 0: %s esp %s %s | v_max stima/s %.4f (una lettura) | v_b/v_max nudo %s (%.0f s)"
                              % (forma, x, fa["staz"], fa["omega0"], nu["omega0"], fa["omega2"], f_(fa["v_b"] and fa["v_b"] / s, "%.5f"), f_(fa["v_fit"] and fa["v_fit"] / s, "%.5f"), an["tasso"],
                                 "STABILE" if rec["stabile"] else "instabile", an["tipo"], f_(an["esponente"], "%.2f"),
                                 "" if not an["v_suono"] else "v_suono/s %.5f" % (an["v_suono"] / s), an["v_max_stima"] / s, f_(rec["v_b_su_v_max"], "%.4f"), time.time() - t0))
                        sys.stdout.flush()
    return righe, peg_c3, nude_ok


def main(argv):
    del argv
    import _presidio
    import _triangoli_dove_la_luce as DL
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 110)
    print("DOVE NASCE UN MODO SENZA MASSA SUI TRIANGOLI (la c del modello): il regime s -> 1, la moneta, la particella vestita dal vuoto")
    print("=" * 110)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py", "csv/_triangoli_forza.py", "csv/_triangoli_fattore.py",
                                     "csv/_triangoli_luce.py", "csv/_triangoli_dove_la_luce.py", "csv/_stabilita_triangoli.py", "csv/_stabilita_lineare.py", "csv/_screening_forme_s3.py",
                                     "csv/_zero_simmetrico.py", "csv/_triangoli_dove_la_c.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: RIF %s %s %s; S_A %s; S_B %s; EPS_B %s; S_C %s; EPS_C %s; X_C %s; X_ZERO %g; FORME %s; E_REL %g; J_MAX %d; LC %d;"
          % (RIF_BASSA, RIF_FATTORE, RIF_LUCE, S_A, S_B, EPS_B, S_C, EPS_C, X_C, X_ZERO, FORME, E_REL, J_MAX, LC))
    print("    TOLL_RIF %g TOLL_VMAX %g TOLL_C6 %g TOLL_C3 %g TOLL_STAZ %g TOLL_NUDA %g TOLL_UNO %g TOLL_5 %g STABILE %g; a s = 1 la scena NON e' rifiutata: s = 1.0"
          % (TOLL_RIF, TOLL_VMAX, TOLL_C6, TOLL_C3, TOLL_STAZ, TOLL_NUDA, TOLL_UNO, TOLL_5, STABILE))
    print("-" * 110)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    DL.JSONL = JSONL                       # ### la riga di _triangoli_dove_la_luce scrive QUI
    print("### PARTE A -- IL REGIME s -> 1 (eps 0, la particella nuda; la riga di _triangoli_dove_la_luce)")
    ra = [DL.riga(0.0, s, "A") for s in S_A]
    print("### L'ANDAMENTO VERSO s = 1: l'esponente locale d ln|f(1) - f(s)| / d ln(1 - s) fra 0.9, 0.99, 0.999")
    for nome, fn in (("v_max/s", lambda r: r["v_max"]["tutti"] / r["s"]), ("v_b/s (K)", lambda r: r["v_b_su_s"][0]), ("salto a K", lambda r: r["coppia_K"]["salto"]),
                     ("salto attraverso pi", lambda r: r["coppia_pi"]["salto"])):
        y = {r["s"]: fn(r) for r in ra}
        ps = []
        for a, b in ((0.9, 0.99), (0.99, 0.999)):
            da, db = abs(y[1.0] - y[a]), abs(y[1.0] - y[b])
            ps.append(math.log(da / db) / math.log((1 - a) / (1 - b)) if da > 0 and db > 0 else None)
        scrivi({"tipo": "andamento", "che": nome, "y": {str(k): v for k, v in y.items()}, "esponenti": ps})
        print("  %-20s %s | a s = 1: %.5f | esponenti %s" % (nome, " ".join("%g:%.5f" % (k, v) for k, v in y.items()), y[1.0], " ".join(f_(p, "%.3f") for p in ps)))
    print("-" * 110)
    print("### PARTE B -- LA MONETA (la particella nuda; <<il modo massivo piu' basso>>: la coppia a K seguita in eps, dichiarato)")
    rb = []
    for eps in EPS_B:
        for s in S_B:
            if eps == 0.0 and s == 0.5:
                rb.append([r for r in ra if r["s"] == 0.5][0])
                continue
            rb.append(DL.riga(eps, s, "B" + (" ### eps 0.5, LA SCELTA DI LUCA" if eps == 0.5 else "")))
    print("-" * 110)
    rc, peg_c3, nude_ok = parte_C()
    print("-" * 110)
    print("### I CONTROLLI")
    rif_b = [r for r in git_jsonl(RIF_BASSA, "doc/referti_l2/triangoli_bassa_energia.jsonl") if r.get("tipo") == "salto_minimo" and r["eps"] == 0.0 and r["s"] == 0.3]
    rif_f = [r for r in git_jsonl(RIF_FATTORE, "doc/referti_l2/triangoli_fattore.jsonl") if r.get("tipo") == "fattori" and r["eps"] == 0.0 and r["s"] == 0.3 and r["banda"] == 0]
    rif_l = [r for r in git_jsonl(RIF_LUCE, "doc/referti_l2/triangoli_luce.jsonl") if r.get("tipo") == "cono" and r["s"] == 0.3]
    r03 = [r for r in rb if r["eps"] == 0.0 and r["s"] == 0.3][0]
    d1 = abs(r03["coppia_K"]["salto"] - rif_b[0]["salto"])
    d2 = abs(r03["coppia_K"]["bande"][0]["v_b"] - rif_f[0]["fattori"]["v_b"]["c"])
    d3 = abs(r03["v_max"]["materia"] - rif_l[0]["v_max_materia"])
    esito("DEVE PASSARE: a s 0.3, eps 0: il salto a K = %s, v_b = %s entro %g; v_max = %s entro %g" % (RIF_BASSA, RIF_FATTORE, TOLL_RIF, RIF_LUCE, TOLL_VMAX),
          d1 <= TOLL_RIF and d2 <= TOLL_RIF and d3 <= TOLL_VMAX, "%.1e %.1e %.1e" % (d1, d2, d3))
    tutte = ra + [r for r in rb if r not in ra]
    peg = max(r["c6"] for r in tutte)
    esito("DEVE PASSARE: lo spettro invariante per 60 gradi (sul cerchio) entro %g a ogni (eps, s), le due convenzioni" % TOLL_C6, peg < TOLL_C6, "il peggiore %.2e" % peg)
    esito("DEVE PASSARE: nella cella di tre nodi (la base a K: 120 gradi, non 60) lo spettro della Green invariante entro %g (S1, x %g)" % (TOLL_C3, X_C[-1]), peg_c3 < TOLL_C3, "il peggiore %.2e" % peg_c3)
    cattivi = [z for z in nude_ok if z[-1] > TOLL_NUDA]
    esito("DEVE PASSARE: parte C, a x %g v_b vestita = v_b nuda entro %g, S1 e S4 (S3 singolare: saltato)" % (X_ZERO, TOLL_NUDA), not cattivi,
          "; ".join("%s eps %g s %g b %d: %.1e" % z for z in cattivi[:4]) or "il peggiore %.1e" % max(z[-1] for z in nude_ok))
    lin03 = [x for nome in ("simm", "oggi") for sett in ("materia", "vuoto") for x in r03[nome][sett]["lineari"]]
    tocchi03 = sum(len(p["tocchi"]) for nome in ("simm", "oggi") for sett in ("materia", "vuoto") for p in r03[nome][sett]["punti"].values())
    esito("DEVE FALLIRE: <<a eps 0, s 0.3 esiste un modo lineare senza massa>> (la chiave: dei tocchi trovati, nessuno lineare)", tocchi03 > 0 and not lin03, "%d tocchi, %d lineari" % (tocchi03, len(lin03)))
    uno = ra[-1]
    esito("PUO' FALLIRE: a s = 1, eps 0, v_max/s entro %g da 1" % TOLL_UNO, abs(uno["v_max"]["tutti"] - 1.0) <= TOLL_UNO, "%.4f" % uno["v_max"]["tutti"])
    lin1 = [x for nome in ("simm", "oggi") for sett in ("materia", "vuoto") for x in uno[nome][sett]["lineari"]]
    esito("PUO' FALLIRE: a s = 1, eps 0, esiste un tocco lineare (un modo senza massa)", bool(lin1), "%d rami lineari, v/s %s" % (len(lin1), sorted({round(x["pendenza_su_s"], 4) for x in lin1})))
    buoni, nlin = [], 0
    for r in tutte:
        if r["s"] > 0.5:
            continue
        for nome in ("simm", "oggi"):
            for sett in ("materia", "vuoto"):
                for x in r[nome][sett]["lineari"]:
                    nlin += 1
                    for vb in r["v_b_su_s"]:
                        if abs(x["pendenza_su_s"] - vb) / vb < TOLL_5:
                            buoni.append((r["eps"], r["s"], x["pendenza_su_s"], vb))
    esito("PUO' FALLIRE: un (eps, s <= 0.5) con un modo lineare senza massa a velocita' entro il 5%% da v_b della coppia a K", bool(buoni), "%d lineari a s <= 0.5; %s" % (nlin, buoni[:4]))
    ok_c = [r for r in rc if r.get("stabile") and r.get("v_b_su_v_max") is not None and abs(r["v_b_su_v_max"] - 1.0) <= TOLL_5]
    esito("PUO' FALLIRE: parte C, un punto STABILE (tasso <= %g) con v_b vestita/v_max entro il 5%% da 1" % STABILE, bool(ok_c),
          "; ".join("%s x %g s %g eps %g b %d: %.4f" % (r["forma"], r["x"], r["s"], r["eps"], r["banda"], r["v_b_su_v_max"]) for r in ok_c[:4]) or
          "stabili %d; il loro v_b/v_max %s" % (sum(1 for r in rc if r.get("stabile")), sorted({round(r["v_b_su_v_max"], 3) for r in rc if r.get("stabile") and r.get("v_b_su_v_max")})[:6]))
    print("=" * 110)
    print("DOVE NASCE UN MODO SENZA MASSA: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
