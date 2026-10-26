# -*- coding: utf-8 -*-
r"""**I SOLITONI ESISTONO SUI TRIANGOLI?** *(la parte 2 del mandato della massa collettiva; [[PROGETTO-MASSA-COLLETTIVA]], [[INDIRIZZO-MASSA-COLLETTIVA]], [[DECISIONE-LINEARE]])*: ### **`(A)` il risolutore
d'inviluppo di `9a6955f3` con la curvatura della coppia dei triangoli; `(B)` la dinamica sul toro a triangoli col tick intero e la forma in memoria: la stabilita' e il tempo di vita.**

> ### ⛔ **Il task history e' `2026-10-26_solitoni_triangoli.md`.** ### **In memoria; nessun file del nucleo; `S3` resta nel nucleo.**
> ### **Importati, non copiati:** `_modi_pi_e_solitoni` *(`largo`)*, `_gravita_collettiva` *(`profilo`, `c_di`, `gruppi`)*, `_forza_da_cs.rami`, `_materia_leggera` *(`fam_s`, `bande_coppia`, `curvatura`, `griglia`)*,
> `_triangoli_forza.coppia_K`, `_screening_forme_s3.forma`, `scena_l2.scena_toro`, `tick.tick`.

Gira con:  python csv/_solitoni_triangoli.py > doc/referti_l2/solitoni_triangoli.txt
"""
import io
import json
import math
import os
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

S_C = (0.3, 0.5, 0.7, 0.9, 0.95, 0.99)
N_C = (10.0, 100.0, 1e3, 1e4, 1e5, 1e6, 1e7)
FORME = ("S1", "S3", "S4")
LAM0_TRI = 6.0
LAM0_QUA = 4.0
LARGHEZZA_MIN = 4.0
FATTORI_L = (12.0, 18.0)
T_MAX = 2000
OGNI = 20
TOLL_LARGH = 0.20
FRAZ_MIN = 0.8
RAGGIO_FRAZ = 3.0
TOLL_RIPRO = 1e-12
TOLL_NORMA = 1e-10
TOLL_VITA = 0.20
JSONL = os.path.join(RADICE, "doc", "referti_l2", "solitoni_triangoli.jsonl")
VECCHIO = ("9a6955f3", "doc/referti_l2/modi_pi_e_solitoni.jsonl")
OK = [0, 0]
FALLITE = []
A1 = np.array([1.0, 0.0])
A2 = np.array([-0.5, math.sqrt(3.0) / 2.0])
AREA_NODO = math.sqrt(3.0) / 2.0


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def c_quadrato(s):
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    g = [x for x in GC.gruppi(F.rami(s, 0.0)[0]) if x["segno"] < 0][0]
    return GC.c_di(g)


def c_triangoli(s):
    """### `c = (1/2) d^2 w/dk^2` del ramo BASSO della coppia a `K`, `w` la fase per tick: `(c_x, c_y, w0)`."""
    import _materia_leggera as ML
    f = ML.fam_s(s)
    G = ML.griglia(f, 24)
    _bu, bd, _p, mk = ML.bande_coppia(f, G)
    fac = np.pi * s
    cx = 0.5 * fac * ML.curvatura(f, bd, (1, 0))
    cy = 0.5 * fac * ML.curvatura(f, bd, (0, 1))
    return float(cx), float(cy), float(fac * mk[bd])


def esistenza(griglia, lam0):
    import _modi_pi_e_solitoni as MPS
    vero = MPS.LAM0
    MPS.LAM0 = lam0
    out = []
    try:
        for s in S_C:
            if griglia == "quadrato":
                c, cy, w0 = c_quadrato(s), None, None
            else:
                c, cy, w0 = c_triangoli(s)
            for forma in FORME:
                for N in N_C:
                    q = MPS.largo(forma, c, s, N)
                    rec = {"tipo": "esistenza", "griglia": griglia, "lam0": lam0, "forma": forma, "s": s, "N": N, "c": c, "c_y": cy, "w0": w0,
                           "verdetto": q["verdetto"], "larghezza": q["larghezza"], "mu": q["mu"], "x_centro": q["x_centro"], "giri": q["giri"]}
                    out.append(rec)
                    scrivi(rec)
                    print("  %-9s LAM0 %g %-2s s %-4g N %-7g: %-28s larghezza %9.3f archi  mu %+.4f  x_centro %.3g  (c %+.6f%s)"
                          % (griglia, lam0, forma, s, N, q["verdetto"][:28], q["larghezza"], q["mu"], q["x_centro"], c, "" if cy is None else ", c_y %+.6f, w0 %+.6f" % (cy, w0)))
                    sys.stdout.flush()
    finally:
        MPS.LAM0 = vero
    return out


def profilo_u(forma, c, s, N, lam0, w):
    import _gravita_collettiva as GC
    import _modi_pi_e_solitoni as MPS
    dr = w / MPS.PUNTI_PER_W
    M = int(np.ceil(10.0 * w / dr))
    q, r, u = GC.profilo(forma, c, s, N, lam0, dr, M, w)
    return q, r, u


def dinamica(forma, s, N, rec, fattore):
    """### Il profilo sul toro a triangoli, il tick intero col legame acceso e la forma in memoria."""
    import _screening_forme_s3 as SF
    import _triangoli_forza as TF
    import scena_l2 as SL
    import tick as TK
    w0 = rec["larghezza"]
    q, r, u = profilo_u(forma, rec["c"], s, N, LAM0_TRI, w0)
    L = int(3 * math.ceil(fattore * w0 / 3.0))
    inc, mot, st, par = SL.scena_toro("triangoli", (L, L), 1.0, 0.1)
    n = inc.n
    mot.cs = np.full(n, float(s))
    mot.lambda_c = None
    par = dict(par)
    par["eps"] = 0.0
    v = np.arange(n)
    m1, m2 = v // L, v % L
    d1 = (m1 - L // 2 + L // 2) % L - L // 2
    d2 = (m2 - L // 2 + L // 2) % L - L // 2
    pos = d1[:, None] * A1 + d2[:, None] * A2
    rr = np.hypot(pos[:, 0], pos[:, 1])
    g = np.interp(rr, r, u, right=0.0) * math.sqrt(AREA_NODO)
    Q = TF.coppia_K(0.0, s)[0]["Q"][:, 0]
    cel = g[:, None] * Q[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
    cel *= math.sqrt(N / float(np.sum(np.abs(cel) ** 2)))
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    nodo = inc.nodo

    def misure():
        rho = np.zeros(n)
        np.add.at(rho, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        M = float(rho.sum())
        c = (rho @ pos) / M
        w2 = float(rho @ np.sum((pos - c) ** 2, axis=1)) / M
        fr = float(rho[np.hypot(pos[:, 0] - c[0], pos[:, 1] - c[1]) <= RAGGIO_FRAZ * w0].sum()) / M
        V = float(np.sum(np.abs(st["phi_h"]) ** 2))
        centro = st["psi_h"].reshape(n, 12)[int(np.argmin(rr))]
        a = complex(np.vdot(Q, centro))
        return {"M": M, "V": V, "larghezza": math.sqrt(w2), "picco": float(rho.max()), "frazione": fr, "c": [float(c[0]), float(c[1])], "a": a}
    serie = []
    fasi = []
    i_c = int(np.argmin(rr))

    def a_centro():
        return complex(np.vdot(Q, st["psi_h"].reshape(n, 12)[i_c]))
    m0 = misure()
    w_in = m0["larghezza"]
    vita = None
    t0 = time.time()
    with SF.forma(forma):
        for t in range(T_MAX + 1):
            if t % OGNI == 0:
                mm = misure() if t else m0
                serie.append((t, mm))
                bad = abs(mm["larghezza"] / w_in - 1.0) > TOLL_LARGH or mm["frazione"] < FRAZ_MIN
                if bad and vita is None:
                    vita = t
            if t < T_MAX:
                a0 = a_centro()
                TK.tick(st, mot, par)
                a1 = a_centro()
                if abs(a0) > 0 and abs(a1) > 0:
                    fasi.append(float(-np.angle(a1 / a0)))
    dM = max(abs(mm["M"] - m0["M"]) / m0["M"] for _t, mm in serie)
    dV = max(abs(mm["V"] - m0["V"]) / m0["V"] for _t, mm in serie)
    fine = serie[-1][1]
    return {"tipo": "dinamica", "forma": forma, "s": s, "N": N, "L": L, "fattore": fattore, "w0_risolutore": w0, "larghezza_iniziale": w_in, "larghezza_finale": fine["larghezza"],
            "picco_iniziale": m0["picco"], "picco_finale": fine["picco"], "frazione_finale": fine["frazione"], "vita": vita, "stabile": vita is None,
            "dM": dM, "dV": dV, "rotazione_media": float(np.mean(fasi)) if fasi else None, "rotazione_dev": float(np.std(fasi)) if fasi else None,
            "rotazione_prevista_simm": (rec["w0"] or 0.0) + rec["mu"], "rotazione_prevista_oggi": float(np.angle(np.exp(1j * ((rec["w0"] or 0.0) - np.pi * s + rec["mu"])))),
            "serie": [[t, mm["larghezza"], mm["picco"], mm["frazione"]] for t, mm in serie], "secondi": time.time() - t0}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("I SOLITONI ESISTONO SUI TRIANGOLI? (A) il risolutore d'inviluppo con la curvatura della coppia dei triangoli; (B) la dinamica sul toro, il tick intero, la forma in memoria")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_solitoni_triangoli.py", "csv/_modi_pi_e_solitoni.py", "csv/_gravita_collettiva.py", "csv/_materia_leggera.py", "csv/_screening_forme_s3.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: S_C %s N_C %s FORME %s LAM0_TRI %g LAM0_QUA %g LARGHEZZA_MIN %g FATTORI_L %s T_MAX %d OGNI %d TOLL_LARGH %g FRAZ_MIN %g RAGGIO_FRAZ %g TOLL_RIPRO %g TOLL_NORMA %g TOLL_VITA %g"
          % (S_C, N_C, FORME, LAM0_TRI, LAM0_QUA, LARGHEZZA_MIN, FATTORI_L, T_MAX, OGNI, TOLL_LARGH, FRAZ_MIN, RAGGIO_FRAZ, TOLL_RIPRO, TOLL_NORMA, TOLL_VITA))
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    # ### il controllo 1: il quadrato contro 9a6955f3
    vecchi = {}
    testo = subprocess.check_output(["git", "show", "%s:%s" % VECCHIO], cwd=RADICE).decode("utf-8")
    for l in testo.splitlines():
        if l.strip():
            d = json.loads(l)
            if d.get("tipo") == "solitone_largo":
                vecchi[(d["forma"], d["s"], d["N"])] = d
    print("### (A) IL QUADRATO DI SERVIZIO, LAM0 %g (il controllo contro %s)" % (LAM0_QUA, VECCHIO[0]))
    qua = esistenza("quadrato", LAM0_QUA)
    ok1, peg = True, 0.0
    for rr_ in qua:
        d = vecchi.get((rr_["forma"], rr_["s"], rr_["N"]))
        if d is None or d["verdetto"] != rr_["verdetto"]:
            ok1 = False
            continue
        for k in ("mu", "larghezza"):
            a, b = rr_[k], d[k]
            if a is None or b is None or (isinstance(a, float) and math.isnan(a)):
                ok1 &= (a is None and b is None) or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b))
                continue
            e = abs(a - b) / max(abs(b), 1e-300)
            peg = max(peg, e)
            ok1 &= e <= TOLL_RIPRO
    esito("DEVE PASSARE (1): il risolutore sul QUADRATO riproduce %s (verdetto, mu, larghezza entro %g relativo, %d righe)" % (VECCHIO[0], TOLL_RIPRO, len(vecchi)), ok1 and len(qua) == len(vecchi), "il peggiore %.1e" % peg)
    print("### (A) I TRIANGOLI, LAM0 %g e %g" % (LAM0_TRI, LAM0_QUA))
    tri6 = esistenza("triangoli", LAM0_TRI)
    tri4 = esistenza("triangoli", LAM0_QUA)

    def primo(tab, forma):
        b = [x for x in tab if x["forma"] == forma and x["verdetto"] == "LEGATO" and x["larghezza"] >= LARGHEZZA_MIN]
        if not b:
            return None
        s1 = min(x["s"] for x in b)
        return min([x for x in b if x["s"] == s1], key=lambda x: x["N"])
    print("### IL PRIMO s CON UNO STATO LEGATO LARGO >= %g ARCHI" % LARGHEZZA_MIN)
    primi = {}
    for nome, tab in (("quadrato LAM0 4", qua), ("triangoli LAM0 6", tri6), ("triangoli LAM0 4", tri4)):
        for forma in FORME:
            p = primo(tab, forma)
            if nome == "triangoli LAM0 6":
                primi[forma] = p
            print("  %-18s %-2s: %s" % (nome, forma, "nessuno" if p is None else "s %g, N %g, larghezza %.3f, mu %+.4f" % (p["s"], p["N"], p["larghezza"], p["mu"])))
            scrivi({"tipo": "primo", "dove": nome, "forma": forma, "primo": p})
    # ### (B) la dinamica
    print("### (B) LA DINAMICA SUL TORO A TRIANGOLI (il tick intero, il legame acceso, la forma in memoria; T_MAX %d)" % T_MAX)
    din = []
    for forma in FORME:
        p = primi[forma]
        if p is None:
            print("  %-2s: nessun solitone largo da far girare" % forma)
            continue
        casi = [p]
        stretti = [x for x in tri6 if x["forma"] == forma and x["s"] == p["s"] and x["verdetto"] == "LEGATO" and x["larghezza"] < LARGHEZZA_MIN]
        if stretti:
            casi.append(max(stretti, key=lambda x: x["larghezza"]))
        for rec in casi:
            for fat in FATTORI_L:
                d = dinamica(forma, rec["s"], rec["N"], rec, fat)
                din.append(d)
                scrivi(d)
                print("  %-2s s %g N %-7g L %3d (%g w0): larghezza %.3f -> %.3f, picco %.4g -> %.4g, frazione finale %.3f; vita %s; dM %.1e dV %.1e; rotazione per tick %s (dev %s) contro la prevista %+.6f (lo zero simmetrico) / %+.6f (oggi) (%.0f s)"
                      % (forma, rec["s"], rec["N"], d["L"], fat, d["larghezza_iniziale"], d["larghezza_finale"], d["picco_iniziale"], d["picco_finale"], d["frazione_finale"],
                         "STABILE fino a %d" % T_MAX if d["stabile"] else "%d tick" % d["vita"], d["dM"], d["dV"],
                         "%+.6f" % d["rotazione_media"] if d["rotazione_media"] is not None else "-", "%.1e" % d["rotazione_dev"] if d["rotazione_dev"] is not None else "-",
                         d["rotazione_prevista_simm"], d["rotazione_prevista_oggi"], d["secondi"]))
                sys.stdout.flush()
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (2): la dinamica conserva M e V entro %g relativo" % TOLL_NORMA, all(d["dM"] <= TOLL_NORMA and d["dV"] <= TOLL_NORMA for d in din) if din else True,
          " ".join("%.1e/%.1e" % (d["dM"], d["dV"]) for d in din))
    p1 = primi.get("S1")
    s1_dyn = [d for d in din if d["forma"] == "S1" and p1 is not None and d["N"] == p1["N"] and d["s"] == p1["s"]]
    esito("PUO' FALLIRE (3): con S1 a s 0.3 un solitone largo >= %g archi sui triangoli (LAM0 %g), STABILE alle due taglie" % (LARGHEZZA_MIN, LAM0_TRI),
          p1 is not None and p1["s"] == 0.3 and bool(s1_dyn) and all(d["stabile"] for d in s1_dyn),
          "primo %s; %s" % ("nessuno" if p1 is None else "s %g N %g w %.3f" % (p1["s"], p1["N"], p1["larghezza"]), " ".join("L %d %s" % (d["L"], "stabile" if d["stabile"] else "vita %d" % d["vita"]) for d in s1_dyn)), deve=False)
    p4 = primi.get("S4")
    esito("PUO' FALLIRE (4): con S4 solo da s 0.7, come sul quadrato", p4 is not None and p4["s"] == 0.7, "nessuno" if p4 is None else "s %g N %g" % (p4["s"], p4["N"]), deve=False)
    n10 = [x for x in tri6 if x["forma"] == "S1" and x["N"] == 10.0]
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA (5): a N 10 S1 lega sui triangoli; la chiave: a N 10 S1 DISPERDE a ogni s (LAM0 %g)" % LAM0_TRI,
          bool(n10) and all(x["verdetto"].startswith("DISPERSIONE") for x in n10), " ".join("s %g %s" % (x["s"], x["verdetto"][:10]) for x in n10))
    print("### LA CONVERGENZA DELLA DINAMICA (le due taglie: lo stesso verdetto, la vita entro il %g%%)" % (100 * TOLL_VITA))
    for forma in FORME:
        for N in sorted({d["N"] for d in din if d["forma"] == forma}):
            dd = [d for d in din if d["forma"] == forma and d["N"] == N]
            if len(dd) == 2:
                a, b = dd
                same = a["stabile"] == b["stabile"] and (a["stabile"] or abs(a["vita"] - b["vita"]) <= TOLL_VITA * max(a["vita"], b["vita"]))
                print("  %-2s N %g: L %d %s, L %d %s -> %s" % (forma, N, a["L"], "stabile" if a["stabile"] else a["vita"], b["L"], "stabile" if b["stabile"] else b["vita"], "CONVERGE" if same else "NON CONVERGE"))
                scrivi({"tipo": "convergenza", "forma": forma, "N": N, "converge": same})
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
