r"""**IL SEGNO DELLA GRAVITA' DEI RAMI: il limite a `s` piccolo, l'unicita' dello zero universale, energia contro inerzia** *(solo misure, in memoria)*.

> ### ⛔ **Il task history e' `2026-10-23_segno_gravita.md`** *(la famiglia degli zeri sulla carta, le previsioni, il metodo, i criteri)*. ### **`leggi.yaml`, l'impronta, la convenzione nel
> repo e il nucleo intatti.** ### **Importati, non copiati:** `_zero_simmetrico`, `_forza_da_cs`, `_scala_e_zero`, `_gravita_collettiva`, `_universalita_massa`.

### **PARTE A:** ### **la famiglia `exp(i theta (I - P)) e^{-i lambda theta}`** *(il pezzo di oggi a `(1 - lambda) f`, poi l'alternativa a `lambda f`)*: ### **`a_H/a_RG` per ogni ramo, la
linearita' in `lambda`, `lambda*`.** ### **PARTE B:** ### **la forza a `s0` piccolo con lo zero simmetrico** *(`_forza_da_cs.corsa`)* ### **e il limite `s0 -> 0`.** ### **PARTE C:** ### **`E0`, `M`,
il loro segno, `E0 M/v_p^2`, e dove sta il salto fra due bande.**

Gira con:  python csv/_segno_gravita.py > doc/referti_l2/segno_gravita.txt
"""
import contextlib
import io
import json
import os
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LAMBDA = (0.0, 0.25, 0.5, 0.75, 1.0)
S0_A = (0.3, 0.5, 0.9)
EPS = (0.0, 0.5)
ETA_H = (1e-3, 1e-2)
S0_B = (0.05, 0.1, 0.2)
ETA_B = (0.0, 5e-4, 1e-3, 5e-3, 1e-2)
LX_B = (256, 512)
S0_LIM = (0.05, 0.1, 0.2, 0.3, 0.4, 0.5)
S_C = (0.05, 0.1, 0.2, 0.3, 0.5, 0.9)
FORME_D = ("S1", "S3", "S4")
S0_D = (0.3, 0.5)
N_D = (1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0)
LARGHEZZA_MIN = 4.0
LAM0 = 4.0
TOLL_LIN = 0.05
TOLL_6E = 1e-9
TOLL_UGUALI = 1e-6
J_ZS = os.path.join(RADICE, "doc", "referti_l2", "zero_simmetrico.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "segno_gravita.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4f"):
    return "--" if x is None else fm % x


@contextlib.contextmanager
def convenzione_lambda(lam):
    """### **`exp(i theta (I - P)) e^{-i lambda theta}`**: ### **il pezzo di oggi a `(1 - lambda) f`, poi quello dell'alternativa a `lambda f`** *(il meccanismo di
    `convenzione_simmetrica`, che e' `lambda = 1/2`; a `lambda 0` e `1` un pezzo solo)*."""
    import _gravita_collettiva as GC
    import flussi_parziali as FP
    if lam == 0.0:
        yield
        return
    g0, hp0, hf0 = FP.grover, FP.hop_psi, FP.hop_phi
    with GC.convenzione_alternativa():
        ga, hpa, hfa = FP.grover, FP.hop_psi, FP.hop_phi
    if lam == 1.0:
        FP.grover, FP.hop_psi, FP.hop_phi = ga, hpa, hfa
    else:
        def comp(oggi, alt):
            def f(mot, x, frazione):
                oggi(mot, x, (1.0 - lam) * frazione)
                return alt(mot, x, lam * frazione)
            return f
        FP.grover, FP.hop_psi, FP.hop_phi = comp(g0, ga), comp(hp0, hpa), comp(hf0, hfa)
    try:
        yield
    finally:
        FP.grover, FP.hop_psi, FP.hop_phi = g0, hp0, hf0


def h_su_rg(lam, eps, s0, eta, g):
    """### `a_H/a_RG = s0 (segno/Dt) d omega(0)/ds` nella lettura `lambda` *(le formule di `557d94d6`; il ramo seguito con l'`omega(0)` bersaglio spostato di `2 pi lambda s`)*."""
    import _forza_da_cs as F
    sm, sp = s0 * (1.0 - eta), s0 * (1.0 + eta)
    with convenzione_lambda(lam):
        rm = F.segui(F.rami(sm, eps)[0], dict(g, omega0=F.avvolgi(g["omega0"] + 2.0 * np.pi * lam * sm)))
        rp = F.segui(F.rami(sp, eps)[0], dict(g, omega0=F.avvolgi(g["omega0"] + 2.0 * np.pi * lam * sp)))
    dw = F.avvolgi(rp["omega0"] - rm["omega0"]) / (sp - sm)
    return float(s0 * g["segno"] * dw / g["Dt"]), float(dw)


# =====================================================================================
#   PARTE A
# =====================================================================================
def parte_A():
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    import _zero_simmetrico as ZS
    print("### PARTE A -- L'UNICITA' DELLO ZERO UNIVERSALE: a_H/a_RG per ogni ramo massivo, lambda %s, s0 %s, eps %s, eta %s" % (LAMBDA, S0_A, EPS, ETA_H))
    tab = {}
    for eps in EPS:
        for s0 in S0_A:
            for g in GC.gruppi(F.rami(s0, eps)[0]):
                nr = ZS.nome_curv(g)
                for eta in ETA_H:
                    vals = [h_su_rg(lam, eps, s0, eta, g) for lam in LAMBDA]
                    y = np.array([v[0] for v in vals])
                    m, q = np.polyfit(LAMBDA, y, 1)
                    res = float(np.max(np.abs(y - (m * np.array(LAMBDA) + q))) / max(float(np.max(np.abs(y))), 1e-300))
                    rec = {"tipo": "lambda", "eps": eps, "s0": s0, "ramo": nr, "eta": eta, "H_su_RG": {str(l): v[0] for l, v in zip(LAMBDA, vals)},
                           "d_omega0_ds": {str(l): v[1] for l, v in zip(LAMBDA, vals)}, "pendenza": float(m), "intercetta": float(q), "residuo": res}
                    tab[(eps, s0, nr, eta)] = rec
                    scrivi(rec)
                    print("  eps %-3g s0 %-4g %-18s eta %-5g: a_H/a_RG %s | retta %+.5f lambda %+.5f | residuo %.1e"
                          % (eps, s0, nr, eta, " ".join("%g:%+.4f" % (l, v[0]) for l, v in zip(LAMBDA, vals)), m, q, res))
                    sys.stdout.flush()
    print("### lambda*: dove i due rami di eps 0 coincidono, e eps 0.5 a quel lambda")
    stelle = []
    for s0 in S0_A:
        for eta in ETA_H:
            due = [v for k, v in tab.items() if k[0] == 0.0 and k[1] == s0 and k[3] == eta]
            if len(due) != 2:
                print("  s0 %g eta %g: a eps 0 %d rami, non 2" % (s0, eta, len(due)))
                continue
            a, b = due
            ls = (b["intercetta"] - a["intercetta"]) / (a["pendenza"] - b["pendenza"])
            v0 = a["pendenza"] * ls + a["intercetta"]
            altri = {k[2]: v["pendenza"] * ls + v["intercetta"] for k, v in tab.items() if k[0] == 0.5 and k[1] == s0 and k[3] == eta}
            rec = {"tipo": "lambda_stella", "s0": s0, "eta": eta, "lambda_stella": float(ls), "H_su_RG_eps0": float(v0),
                   "eps05": {n: float(x) for n, x in altri.items()}, "scarto_eps05": {n: float(abs(x - v0) / abs(v0)) for n, x in altri.items()}}
            stelle.append(rec)
            scrivi(rec)
            print("  s0 %-4g eta %-5g: lambda* %.9f (|lambda* - 1/2| %.2e), a_H/a_RG di eps 0 a lambda* %+.5f | eps 0.5: %s"
                  % (s0, eta, ls, abs(ls - 0.5), v0, "; ".join("%s %+.4f (scarto %.3f)" % (n, x, abs(x - v0) / abs(v0)) for n, x in altri.items())))
    return tab, stelle


# =====================================================================================
#   PARTE B
# =====================================================================================
def parte_B():
    import _forza_da_cs as F
    import _zero_simmetrico as ZS
    print("### PARTE B -- IL LIMITE A s PICCOLO (zero simmetrico; s0 %s; eta %s; Lx %s; W = Lx/16, T <= Lx/4, finestra |<x> - x0| < Lx/32)" % (S0_B, ETA_B, LX_B))
    corse, prev = {}, {}
    for eps in EPS:
        c0 = F.catena_principale(eps)
        for s0 in S0_LIM:
            lista0, BB0, _ = F.rami(s0, eps)
            for rg in F.righe_del_ramo(lista0, F.bersaglio(c0, s0)):
                nr = ZS.nome_curv(rg)
                sg = "+" if rg["segno"] > 0 else "-"
                for eta in ETA_H:
                    prev[(eps, s0, sg, eta)] = (nr, h_su_rg(0.5, eps, s0, eta, rg)[0])
                if s0 not in S0_B:
                    continue
                try:
                    Q = F.spazio_del_ramo(BB0, rg)[0]
                except AssertionError as err:
                    print("  eps %g s0 %g %s: RAMO NON DEFINITO (%s)" % (eps, s0, nr, str(err)[:100]))
                    scrivi({"tipo": "ramo_non_definito", "eps": eps, "s0": s0, "ramo": nr, "perche": str(err)})
                    continue
                print("  eps %g s0 %g %s: Dt/v %.4f contro 1/W %s" % (eps, s0, nr, rg["Dt"] / rg["v"], " ".join("%.4f (Lx %d)" % (16.0 / L, L) for L in LX_B)))
                for Lx in LX_B:
                    for eta in ETA_B:
                        with ZS.convenzione_simmetrica():
                            r = F.corsa(Lx, eps, s0, eta, Q)
                        r.update(ramo=nr, segno=sg)
                        corse[(eps, s0, sg, Lx, eta)] = r
                        scrivi(dict(r, tipo="corsa"))
    righe = []
    for (eps, s0, sg, Lx, eta), r in sorted(corse.items()):
        if eta not in ETA_H:
            continue
        h = corse[(eps, s0, sg, Lx, eta / 2.0)]
        lin = r["a"] / h["a"] if r["a"] is not None and h["a"] else None
        lin_ok = lin is not None and abs(lin / 2.0 - 1.0) < TOLL_LIN
        nr, hr = prev[(eps, s0, sg, eta)]
        dsdx = -s0 * eta * 2.0 * np.pi / Lx
        a_RG = -r_v(eps, s0, sg) ** 2 * dsdx / s0
        rec = {"tipo": "forza", "eps": eps, "s0": s0, "ramo": nr, "segno": sg, "Lx": Lx, "eta": eta, "a_mis": r["a"], "sigma_a": r["sigma_a"], "a_RG": a_RG,
               "mis_su_RG": None if r["a"] is None else r["a"] / a_RG, "H_su_RG": hr, "mis_su_H": None if r["a"] is None else (r["a"] / a_RG) / hr,
               "lin": lin, "leggibile": bool(r["leggibile"] and lin_ok), "fuori_max": r["fuori_max"], "punti": r["punti"],
               "a_su_sigma": None if r["a"] is None or not r["sigma_a"] else abs(r["a"]) / r["sigma_a"]}
        righe.append(rec)
        scrivi(rec)
        print("  eps %-3g s0 %-4g %-18s Lx %d eta %-5g: a %s (+- %s, |a|/sigma %s) | a/a_RG %s a/a_H %s a_H/a_RG %+.4f | lin %s | fuori %.3f | %s"
              % (eps, s0, nr, Lx, eta, f_(r["a"], "%+.4e"), f_(r["sigma_a"], "%.1e"), f_(rec["a_su_sigma"], "%.1f"), f_(rec["mis_su_RG"], "%+.3f"),
                 f_(rec["mis_su_H"], "%+.3f"), hr, f_(lin, "%.3f"), r["fuori_max"] or 0.0, "" if rec["leggibile"] else "### NON SI LEGGE"))
    return corse, righe, prev


def parte_D():
    """### **La scelta delle norme**: ### **le due piu' piccole di `N_D` con lo stato LEGATO e largo `>= 4` archi a tutti e due gli `s0`** *(eps 0, il ramo a curvatura `-`,
    `c = c_di`, `solitone()` di `_gravita_collettiva`)*. ### **Se non ce ne sono, si scrive e la parte `D` si ferma qui.**"""
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    print("### PARTE D -- IL SOLITONE IN UN GRADIENTE: la scelta delle norme (N %s, larghezza >= %g archi, s0 %s, eps 0, curvatura -)" % (N_D, LARGHEZZA_MIN, S0_D))
    rami = {}
    for s0 in S0_D:
        g = [x for x in GC.gruppi(F.rami(s0, 0.0)[0]) if x["segno"] < 0][0]
        rami[s0] = g
        sig = np.sqrt(abs(GC.c_di(g)) / s0)
        print("  s0 %g: c %+.5f, sigma = sqrt(|c|/s) %.3f archi; la scatola del risolutore R = %g sigma = %.2f archi, la dispersione oltre R/5 = %.2f archi"
              % (s0, GC.c_di(g), sig, GC.R_SIGMA, GC.R_SIGMA * sig, GC.R_SIGMA * sig / 5.0))
        scrivi({"tipo": "scatola_D", "s0": s0, "c": GC.c_di(g), "sigma": float(sig), "R": float(GC.R_SIGMA * sig)})
    scelte = {}
    for forma in FORME_D:
        buone = []
        for N in N_D:
            qq = {s0: GC.solitone(forma, GC.c_di(rami[s0]), s0, N, LAM0) for s0 in S0_D}
            ok = all(q["stato"] == "CONVERGE" and q["esiste"] == "LEGATO" and q["larghezza"] >= LARGHEZZA_MIN for q in qq.values())
            scrivi({"tipo": "norma_D", "forma": forma, "N": N, "ok": ok, "stati": {str(s0): {k: q[k] for k in ("esiste", "stato", "larghezza", "mu", "x_centro")} for s0, q in qq.items()}})
            print("  %-2s N %-6g: %s | %s" % (forma, N, "SCELTA POSSIBILE" if ok else "no",
                  "; ".join("s0 %g %s larghezza %.2f mu %+.3f" % (s0, q["esiste"], q["larghezza"], q["mu"]) for s0, q in qq.items())))
            if ok:
                buone.append(N)
        scelte[forma] = buone[:2]
        print("  %-2s: le norme scelte %s" % (forma, buone[:2] if buone else "NESSUNA: per questa forma un solitone legato largo >= 4 archi a tutti e due gli s0 non c'e'"))
    scrivi({"tipo": "scelte_D", "scelte": scelte})
    if not any(scelte.values()):
        print("  ### LA PARTE D SI FERMA QUI: per NESSUNA forma c'e' un solitone legato largo >= 4 archi; i controlli della parte D (eta 0, lo specchio, il puo'-fallire)"
              " NON SONO ESEGUIBILI e non si contano")
    else:
        print("  ### LA PARTE D SI FERMA QUI: ci sono norme scelte, ma la dinamica del solitone NON e' in questo strumento (dichiarato nel referto)")
    return scelte


_V = {}


def r_v(eps, s0, sg):
    return _V[(eps, s0, sg)]


def main(argv):
    del argv
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    import _presidio
    import _scala_e_zero as Z
    import _universalita_massa as UM
    import _zero_simmetrico as ZS
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL SEGNO DELLA GRAVITA' DEI RAMI: il limite a s piccolo, l'unicita' dello zero universale, energia contro inerzia")
    print("=" * 100)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py", "csv/_universalita_massa.py", "csv/_forza_da_cs.py", "csv/_stabilita_lineare.py",
                                     "csv/_gravita_collettiva.py", "csv/_scala_e_zero.py", "csv/_zero_simmetrico.py", "csv/_segno_gravita.py",
                                     "doc/referti_l2/zero_simmetrico.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); le letture lambda SOLO in memoria; i blob nel repo: %s"
          % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LAMBDA %s; S0_A %s; EPS %s; ETA_H %s; S0_B %s; ETA_B %s; LX_B %s; S0_LIM %s; S_C %s; TOLL_LIN %g; TOLL_6E %g; TOLL_UGUALI %g"
          % (LAMBDA, S0_A, EPS, ETA_H, S0_B, ETA_B, LX_B, S0_LIM, S_C, TOLL_LIN, TOLL_6E, TOLL_UGUALI))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    warnings.simplefilter("ignore")
    # ---------------------------------------------------------------- A
    tab, stelle = parte_A()
    assert F.committata(J_ZS), "il jsonl di 6e022419 non e' committato e pulito"
    zs = [json.loads(l) for l in io.open(J_ZS, encoding="utf-8")]
    rif = {(r["convenzione"], r["eps"], r["s0"], r["ramo"], r["eta"]): r["H_su_RG"] for r in zs if r["tipo"] == "forza"}
    peg, n = 0.0, 0
    for (eps, s0, nr, eta), rec in tab.items():
        for lam, cv in (("0.0", "oggi"), ("0.5", "simm")):
            v = rif.get((cv, eps, s0, nr, eta))
            if v is not None:
                n += 1
                peg = max(peg, abs(rec["H_su_RG"][lam] - v) / max(abs(v), 1e-300) if v else abs(rec["H_su_RG"][lam]))
    esito("DEVE PASSARE: a lambda 0 e 0.5, a_H/a_RG = 6e022419 entro %g (%d valori)" % (TOLL_6E, n), n > 0 and peg < TOLL_6E, "il peggiore %.2e" % peg)
    due = [(k, v) for k, v in tab.items() if k[0] == 0.0]
    fin, uguali = True, []
    for s0 in S0_A:
        for eta in ETA_H:
            dd = [v["H_su_RG"]["0.0"] for k, v in due if k[1] == s0 and k[3] == eta]
            if len(dd) == 2:
                fin = fin and all(np.isfinite(dd))
                if abs(dd[0] - dd[1]) <= TOLL_UGUALI * max(abs(dd[0]), abs(dd[1])):
                    uguali.append((s0, eta))
    esito("DEVE FALLIRE: <<a lambda 0 i due rami di eps 0 hanno lo stesso a_H/a_RG>> (per la chiave giusta: valori finiti)", fin and not uguali,
          "; ".join("s0 %g: %s" % (s0, " / ".join("%+.4f" % v["H_su_RG"]["0.0"] for k, v in due if k[1] == s0 and k[3] == 1e-3)) for s0 in S0_A))
    res = max(v["residuo"] for v in tab.values())
    esito("PUO' FALLIRE: la linearita' in lambda, residuo relativo < 1e-6 (ogni ramo, s0, eps, eta)", res < 1e-6, "il peggiore %.2e" % res)
    dl = max((abs(r["lambda_stella"] - 0.5) for r in stelle), default=float("inf"))
    esito("PUO' FALLIRE: |lambda* - 1/2| < 1e-6 a ogni s0 (e eta)", len(stelle) > 0 and dl < 1e-6, "il peggiore %.2e" % dl)
    # ---------------------------------------------------------------- B
    for eps in EPS:
        c0 = F.catena_principale(eps)
        for s0 in S0_LIM:
            for rg in F.righe_del_ramo(F.rami(s0, eps)[0], F.bersaglio(c0, s0)):
                _V[(eps, s0, "+" if rg["segno"] > 0 else "-")] = rg["v"]
    corse, righe, prev = parte_B()
    zero = [r for k, r in corse.items() if k[1] == 0.1 and k[4] == 0.0]
    esito("DEVE PASSARE: eta 0 a s0 0.1, |a| sotto il rumore del fit (%d righe)" % len(zero), len(zero) > 0 and all(r["a"] is not None and F.nullo(r) for r in zero),
          "; ".join("%s Lx %d: a %s sigma %s" % (r["ramo"], r["Lx"], f_(r["a"], "%+.1e"), f_(r["sigma_a"], "%.1e")) for r in zero))
    print("### TROPPO LENTO? (a eta 1e-2, |a| < 2 sigma_a su tutte le righe)")
    lenti = []
    for s0 in S0_B:
        rr = [r for r in righe if r["s0"] == s0 and r["eta"] == 1e-2]
        lento = bool(rr) and all(r["a_su_sigma"] is None or r["a_su_sigma"] < 2.0 for r in rr)
        if not rr:
            print("  s0 %g: NON VALUTATO (nessuna riga a eta 1e-2)" % s0)
            continue
        if lento:
            lenti.append(s0)
        print("  s0 %g: %s (|a|/sigma %s)" % (s0, "TROPPO LENTO" if lento else "si misura", ", ".join(f_(r["a_su_sigma"], "%.1f") for r in rr)))
        scrivi({"tipo": "lento", "s0": s0, "lento": lento})
    print("### IL LIMITE s0 -> 0 di a_H/a_RG (zero simmetrico, eta 1e-3) e di a_mis/a_RG (righe leggibili, Lx 256; s0 0.3 e 0.5 da 6e022419)")
    zsf = {(r["eps"], r["s0"], "+" if "curv +" in r["ramo"] else "-", r["Lx"], r["eta"]): r for r in zs if r["tipo"] == "forza" and r["convenzione"] == "simm"}
    for eps in EPS:
        for sg in ("+", "-"):
            pts = [(s0, prev[(eps, s0, sg, 1e-3)][1]) for s0 in S0_LIM if (eps, s0, sg, 1e-3) in prev]
            if len(pts) < 3:
                continue
            X, Y = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
            l2, l1 = float(np.polyval(np.polyfit(X, Y, 2), 0.0)), float(np.polyval(np.polyfit(X, Y, 1), 0.0))
            mm = [(r["s0"], r["mis_su_RG"]) for r in righe if r["eps"] == eps and r["segno"] == sg and r["Lx"] == 256 and r["leggibile"] and r["s0"] not in lenti]
            mm += [(k[1], v["mis_su_RG"]) for k, v in zsf.items() if k[0] == eps and k[2] == sg and k[3] == 256 and v["leggibile"]]
            mm = sorted(mm)
            lm = None
            if len({s for s, _ in mm}) >= 3:
                lm = float(np.polyval(np.polyfit([s for s, _ in mm], [y for _, y in mm], 2), 0.0))
            rec = {"tipo": "limite", "eps": eps, "segno": sg, "punti_H": pts, "limite_H_grado2": l2, "limite_H_grado1": l1, "punti_mis": mm, "limite_mis_grado2": lm}
            scrivi(rec)
            print("  eps %-3g curv %s: a_H/a_RG %s | s0 -> 0: grado 2 %+.4f, grado 1 %+.4f | a_mis/a_RG su %d punti: grado 2 %s"
                  % (eps, sg, " ".join("%g:%+.4f" % p for p in pts), l2, l1, len(mm), f_(lm)))
    # ---------------------------------------------------------------- D (la scelta)
    parte_D()
    # ---------------------------------------------------------------- C
    print("### PARTE C -- ENERGIA CONTRO INERZIA (zero simmetrico, lato 64): E0, M, il segno, E0 M / v_p^2 = omega omega''/v^2")
    vero = ZS.JSONL
    ZS.JSONL = JSONL
    try:
        rc = []
        for eps in EPS:
            rr, _ = ZS.righe_rami("simm", eps)
            rc += [r for r in rr if r["s"] in S_C]
    finally:
        ZS.JSONL = vero
    for r in sorted(rc, key=lambda r: (r["eps"], r["s"], r["ramo"])):
        print("  eps %-3g s %-4g %-18s: E0 %s M %+.4f | segno E0 M %s | E0 M/v_p^2 %s" % (r["eps"], r["s"], r["ramo"], f_(r["E0"]), r["M"],
              "--" if r["E0"] is None else ("NEGATIVO" if r["E0"] * r["M"] < 0 else "positivo"), f_(r["Q"])))
    print("### DOVE STA IL SALTO: per ogni coppia di rami, il minimo lungo k della distanza fra le bande, e la fase del punto medio")
    for eps in EPS:
        for s in S_C:
            with ZS.convenzione_simmetrica():
                lista, ph, _A = Z.rami_a(64, s, eps)
            gg = GC.gruppi(lista)
            idx = [[r for r in lista if abs(r["omega0"] - g["omega0"]) <= GC.TOLL_DISTINTI and r["omega1"] in g["omega1"]][0]["ramo"] for g in gg]
            for i in range(len(gg)):
                for j in range(i + 1, len(gg)):
                    a, b = ph[:, idx[i]], ph[:, idx[j]]
                    d = np.abs((a - b + np.pi) % (2.0 * np.pi) - np.pi)
                    m = int(np.argmin(d))
                    c = F.avvolgi(a[m] + F.avvolgi(b[m] - a[m]) / 2.0)
                    rec = {"tipo": "salto", "eps": eps, "s": s, "rami": [ZS.nome_curv(gg[i]), ZS.nome_curv(gg[j])], "m": m, "k_su_pi": 2.0 * m / 64.0,
                           "distanza": float(d[m]), "fase_centro": float(c), "vicino": "pi" if abs(c) >= np.pi / 2 else "0"}
                    scrivi(rec)
                    print("  eps %-3g s %-4g %s / %s: il minimo a k = %.4f pi, distanza %.5f, fase %+.5f -> vicino a %s"
                          % (eps, s, rec["rami"][0], rec["rami"][1], rec["k_su_pi"], rec["distanza"], c, rec["vicino"]))
    print("=" * 100)
    print("IL SEGNO DELLA GRAVITA': %d su %d controlli   %s  (il verdetto di fisica sono le tabelle e il limite)"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
