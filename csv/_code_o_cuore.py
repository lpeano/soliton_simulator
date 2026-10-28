# -*- coding: utf-8 -*-
r"""**CODE O CUORE: DA DOVE VIENE LA DERIVA DEL CONGELATO** *(il rilievo di Luca dopo le `14:27` del `2026-10-28`; [[VUOTO-SUL-FONDO]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-28_rilettura_buca_e_deriva.md`, `2-bis (a)`)*: ### **`(a)` lo stato perde CODE, o `(b)` `S1` e' instabile e cambia il CUORE?**
### **Il congelato alla taglia grande** *(`N 1e6`, `L 81`, zero simmetrico)* ### **per `600` di tempo fisico a `s 0.075` e a `s 0.3`:** ### **la larghezza, la frazione entro `w_in`
(assoluta e relativa) e entro `3 w0`, il picco, ogni `3` di tempo fisico; la forma della crescita nei quattro quarti.**

    python csv/_code_o_cuore.py > doc/referti_l2/code_o_cuore.txt
"""
import io
import json
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

TAU = 600.0
OGNI_TAU = 3.0
QUARTI = (0.0, 150.0, 300.0, 450.0, 600.0)
SOGLIA_REL = 0.95              # ### la soglia di Luca, letta sulla frazione RELATIVA (dichiarato nel task history, 2-bis (a))
RIF_075 = os.path.join(RADICE, "doc", "referti_l2", "solitone_con_la_buca", "grande_fondo_congelato.jsonl")
RIF_03 = os.path.join(RADICE, "doc", "referti_l2", "solitone_vuoto_congelato.jsonl")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def corsa(s):
    import _deriva_congelato as DC
    import _energia_del_legame as EL
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    rec = DC.prepara(s)
    z = DC.nuovo(rec, "fondo")
    phi0 = z["st"]["phi_h"].copy()
    w0 = rec["larghezza"]
    T = int(round(TAU / s))
    ogni = int(round(OGNI_TAU / s))
    serie = []
    t0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        w_in = DC.forma(z, w0)[0]

        def punto(t):
            rho, _l = EL.densita(z["inc"], z["st"])
            M = float(rho.sum())
            c = (rho @ z["pos"]) / M
            d = np.hypot(z["pos"][:, 0] - c[0], z["pos"][:, 1] - c[1])
            w = math.sqrt(float(rho @ np.sum((z["pos"] - c) ** 2, axis=1)) / M)    # ### la stessa espressione di forma_m: il confronto e' al bit
            return {"t": t, "tau": t * s, "w": w, "f_win": float(rho[d <= w_in].sum()) / M, "f_3w0": float(rho[d <= 3.0 * w0].sum()) / M, "picco": float(rho.max())}
        serie.append(punto(0))
        for t in range(1, T + 1):
            DC.tick_congelato(z, phi0)
            if t % ogni == 0 or t in (20, 40):
                serie.append(punto(t))
    return {"s": s, "w0": w0, "w_in": w_in, "T": T, "serie": serie, "secondi": time.time() - t0}


def pendenze(r):
    """### **La pendenza media di `w / w_in` nel tempo fisico in ogni quarto** *(dai punti ai capi del quarto)*."""
    per = {round(x["tau"], 9): x["w"] / r["w_in"] for x in r["serie"]}
    out = []
    for a, b in zip(QUARTI, QUARTI[1:]):
        out.append((per[round(b, 9)] - per[round(a, 9)]) / (b - a))
    return out


def main():
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    s_vero = VC.S
    try:
        print("=" * 130)
        print("CODE O CUORE: il congelato, N 1e6 L 81 zero simm, %g di tempo fisico a s 0.075 e a s 0.3; ogni %g di tempo fisico" % (TAU, OGNI_TAU))
        print("=" * 130)
        print("  la configurazione: TAU %g OGNI_TAU %g QUARTI %s SOGLIA_REL %g (sulla frazione entro w_in RELATIVA al valore iniziale); il passo: %d pezzi, impronta %s"
              % (TAU, OGNI_TAU, QUARTI, SOGLIA_REL, len(CM.ORDINE), CM.IMPRONTA))
        print("  le due letture di Luca: (a) CODE: la frazione entro w_in resta, la crescita rallenta fino a fermarsi, cala con s piu' piccolo; (b) CUORE: il cuore cambia, la crescita non si ferma o accelera, non dipende da s")
        print("-" * 130)
        rr = {}
        for s in (0.075, 0.3):
            rr[s] = corsa(s)
        a = json.loads(io.open(RIF_075, encoding="utf-8").read())
        wa = {x["t"]: x["larghezza"] for x in a["serie"]}
        mio = {x["t"]: x["w"] for x in rr[0.075]["serie"]}
        com = sorted(set(wa) & set(mio))
        esito("DEVE PASSARE (k1): s 0.075, le larghezze ai tick comuni = grande_fondo_congelato AL BIT", all(wa[t] == mio[t] for t in com), "%d tick comuni" % len(com))
        b = [json.loads(y) for y in io.open(RIF_03, encoding="utf-8").read().split("\n") if y.strip()]
        b = [x for x in b if x.get("tipo") == "corsa" and x.get("modo") == "congelato" and x.get("zero") == "simm" and x.get("L") == 81 and x.get("N") == 1e6]
        wb = {int(x[0]): x[1] for x in b[0]["serie"]} if len(b) == 1 else {}
        mio3 = {x["t"]: x["w"] for x in rr[0.3]["serie"]}
        com3 = sorted(set(wb) & set(mio3))
        esito("DEVE PASSARE (k2): s 0.3, le larghezze ogni 20 tick = 74f99039 simm L 81 congelato AL BIT", len(b) == 1 and bool(com3) and all(wb[t] == mio3[t] for t in com3),
              "%d tick comuni; lo scarto massimo %.2e" % (len(com3), max(abs(wb[t] - mio3[t]) for t in com3) if com3 else float("nan")))
        print("-" * 130)
        for s, r in rr.items():
            ser = r["serie"]
            f0 = ser[0]["f_win"]
            print("### s %g: w0 del risolutore %.4f, w_in sul toro %.4f; %d tick (%.0f s)" % (s, r["w0"], r["w_in"], r["T"], r["secondi"]))
            for x in ser:
                if x["t"] in (0, 20, 40) or abs(x["tau"] / 75.0 - round(x["tau"] / 75.0)) < 1e-9:
                    print("  tau %6.1f (tick %5d): w/w_in %.5f; frazione entro w_in %.5f (relativa %.5f), entro 3 w0 %.6f; picco %.4e (relativo %.5f)"
                          % (x["tau"], x["t"], x["w"] / r["w_in"], x["f_win"], x["f_win"] / f0, x["f_3w0"], x["picco"], x["picco"] / ser[0]["picco"]))
            p = pendenze(r)
            forma = "RALLENTA" if all(u > v for u, v in zip(p, p[1:])) else ("ACCELERA" if all(u < v for u, v in zip(p, p[1:])) else "NON MONOTONA")
            fmin = min(x["f_win"] / f0 for x in ser)
            print("  la pendenza di w/w_in per unita' di tempo fisico nei quarti %s: %s -> %s" % (QUARTI, ["%.3e" % v for v in p], forma))
            print("  la frazione entro w_in relativa: minimo %.5f (soglia %g); il picco relativo alla fine %.5f" % (fmin, SOGLIA_REL, ser[-1]["picco"] / ser[0]["picco"]))
        print("-" * 130)
        print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    finally:
        VC.S = s_vero
    return 0


if __name__ == "__main__":
    sys.exit(main())
