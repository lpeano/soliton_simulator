# -*- coding: utf-8 -*-
r"""**PERCHE' IL LAPSE ALLARGA IL SOLITONE: DUE MATTONI (MG) CON `rho_c` DIVERSO** *(Luca `2026-11-13` `23:22`; le scelte L1-L5 del guardiano su delega; il task history
`doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `10`)*.

    python csv/solitone/mattone_rhoc.py prepara --caso MGdoppio|MGmezzo --registro mattone-<caso>     (lo stdout nello scratchpad)
    python csv/solitone/mattone_rhoc.py raggio_MG > doc/referti_l2/mattone/raggio_MG.txt                (dagli stati salvati di (MG), nessuna corsa)
    python csv/solitone/mattone_rhoc.py referto > doc/referti_l2/mattone/rhoc.txt

### **I casi** *(i nomi: `/` non sta in un nome di file)*: **(MGx2) = `MGdoppio`, `rho_c = 454117.149728`** *(il lapse piu' debole)*; **(MG/2) = `MGmezzo`, `rho_c = 113529.287432`** *(piu' forte)*.
**IDENTICI a (MG) salvo `rho_c`:** **TBS a `10000`, `L 81`, la rampa `sin^2` in `4000` tick + `1000` pieni, solo il lapse** *(`mattone.Campi`, il caso `MG`; `mattone.py` NON si tocca)*.
### **In piu'** *(L3)*: **ogni `50` tick il RAGGIO** *(la radice del secondo momento di `rho` attorno al centro, dentro `R_T_RAGGIO = 28`: il `R_t` di TBS a `10000`, FISSO per tutti, dichiarato)* **e `N` al centro**
*(`mot.cs / s` del tick vero al nodo del centro)*. ### **Il collasso** *(L4)*: **il picco oltre `2` volte l'iniziale: la corsa si ferma, si scrive; non e' un errore.**
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402

RHO_C_MG = 227058.574864                # ### il rho_c ASSOLUTO di (MG) e dei bracci di P6
CASI = {"MGdoppio": 454117.149728, "MGmezzo": 113529.287432}   # ### L1 (Luca 23:22)
R_T_RAGGIO = 28.0                       # ### L3: dentro R_t; il R_t di TBS a 10000 (il collaudo del mattone), FISSO (mio, dichiarato)
COLLASSO = 2.0                          # ### L4: il picco oltre 2 volte l'iniziale
SOGLIA_A, GRADUALE_A = 0.75, 0.6        # ### L4: le soglie del guardiano (dichiarate)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def raggio(Z, rho, c):
    """### **L3:** `sqrt(somma rho r^2 / somma rho)` per `r <= R_T_RAGGIO` dal centro `c`."""
    from solitone import toro as TO
    pos = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"])
    r2 = pos[:, 0] ** 2 + pos[:, 1] ** 2
    m = r2 <= R_T_RAGGIO ** 2
    return float(math.sqrt(np.sum(rho[m] * r2[m]) / np.sum(rho[m])))


def nodo_centro(Z, c):
    L = Z["L"]
    return (int(round(c[0])) % L) * L + int(round(c[1])) % L


def corsa(Z, rho_c, n_tick, nome_reg, stato_ogni, caso, misura_ogni):
    """### **Il ciclo di `mattone.prepara`** *(COPIATO, dichiarato: la funzione non e' parametrica in `rho_c`)* **col caso `MG` e `rho_c` dato; in piu' il raggio e `N` al centro.** `(S, fermo)`."""
    import _vuoto_vivo_B as V
    C = MT.Campi(Z, "MG", rho_c, MT.PB.E_DECISO)
    S = {k: [] for k in ("k", "r", "c1", "c2", "rmax", "resp", "M", "E", "raggio", "N_c")}

    def misura(k, r):
        rho = MT.rho_di(Z)
        c = MT.centro_di(Z, rho)
        S["k"].append(k)
        S["r"].append(r)
        S["c1"].append(c[0])
        S["c2"].append(c[1])
        S["rmax"].append(float(rho.max()))
        S["resp"].append(MT.respiro(rho))
        S["M"].append(float(rho.sum()))
        S["E"].append(MT.energia(Z) if k % misura_ogni == 0 else float("nan"))
        S["raggio"].append(raggio(Z, rho, c))
        cs = np.asarray(Z["mot"].cs, dtype=float)
        S["N_c"].append(float(cs.reshape(-1)[nodo_centro(Z, c)] / Z["s"]) if cs.size > 1 else float(cs) / Z["s"])
    misura(0, 0.0)
    rmax0 = S["rmax"][0]
    fermo = None
    t1 = t_tappa = time.time()
    for k in range(1, n_tick + 1):
        r = MT.r_di(k)
        C.tick(k, MT.T_BASE + k, r, 0.0)
        if k % MT.OGNI == 0:
            misura(k, r)
            if k % 250 == 0:
                print("    k %5d  r %.6f  c (%.3f, %.3f)  rmax %.4e  raggio %.4f  N_c %.6f  respiro %.4f  M %.10e  (%.0f s)" % (
                    k, r, S["c1"][-1], S["c2"][-1], S["rmax"][-1], S["raggio"][-1], S["N_c"][-1], S["resp"][-1], S["M"][-1], time.time() - t1))
                sys.stdout.flush()
            if S["rmax"][-1] > COLLASSO * rmax0:
                fermo = "COLLASSO a k %d: il picco %.4e oltre %g volte l'iniziale %.4e (L4: un risultato, non un errore)" % (k, S["rmax"][-1], COLLASSO, rmax0)
                print("### %s" % fermo)
                break
        if stato_ogni and k % stato_ogni == 0:
            f = os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, k))
            np.savez(f, meta=np.array(json.dumps({"caso": caso, "k": k, "r": r, "rho_c": rho_c, "sha": V.shas(Z["z"])})), **{kk: Z["st"][kk] for kk in Z["chiavi"]})
            print("### lo stato a k %d: %s" % (k, f))
        adesso = time.time()
        if nome_reg and adesso - t_tappa >= MT.TAPPA_S:
            mem = MT.memoria_gb()
            MT.tappa(nome_reg, "k %d; %.3f s per tick dall'inizio; la memoria libera %.2f GB" % (k, (adesso - t1) / k, mem))
            t_tappa = adesso
            if mem < MT.MEM_MIN_GB:
                fermo = "la memoria libera %.2f GB sotto %g GB a k %d" % (mem, MT.MEM_MIN_GB, k)
                print("### FERMO: %s" % fermo)
                break
        if adesso - t1 > MT.TETTO_S:
            fermo = "il tetto di %g s a k %d" % (MT.TETTO_S, k)
            print("### FERMO: %s" % fermo)
            break
    return S, fermo


def prepara(caso, nome_reg):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mattone.py"))
    _presidio.avvia(__file__)
    rho_c = CASI[caso]
    t00 = time.time()
    print("=" * 130)
    print("IL MATTONE %s (Luca 23:22): come (MG) salvo rho_c %.6f (quello di (MG) %.6f, il rapporto %.3f); la rampa sin^2 in %d tick + %d pieni; il raggio dentro R %g; N al centro"
          % (caso, rho_c, RHO_C_MG, rho_c / RHO_C_MG, MT.K_RAMPA, MT.N_PIENO, R_T_RAGGIO))
    print("=" * 130)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        S, fermo = corsa(Z, rho_c, MT.K_RAMPA + MT.N_PIENO, nome_reg, MT.PEZZO, caso, MT.OGNI)
    os.makedirs(MT.DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(MT.DIR_REF, "%s_serie.npz" % caso), **{k: np.array(v) for k, v in S.items()})
    kk = np.array(S["k"])
    ult = kk >= kk[-1] - MT.N_PIENO
    resp = np.array(S["resp"])[ult]
    i4000 = [i for i, k in enumerate(S["k"]) if k == MT.K_RAMPA]
    print("-" * 130)
    print("### (%s) %d tick in %.0f s; il FERMO %s" % (caso, int(kk[-1]), time.time() - t00, fermo))
    print("    il picco da %.4e a %.4e: A = 1 - finale/iniziale = %.4f; il raggio da %.4f a %.4f; N al centro a piena rampa (k %d) %s; il respiro negli ultimi %d tick %.4f; la massa da %.10e a %.10e"
          % (S["rmax"][0], S["rmax"][-1], 1.0 - S["rmax"][-1] / S["rmax"][0], S["raggio"][0], S["raggio"][-1], MT.K_RAMPA,
             "%.6f" % S["N_c"][i4000[0]] if i4000 else "--", MT.N_PIENO, float(resp.max() - resp.min()), S["M"][0], S["M"][-1]))
    print("=" * 130)
    return 0


def raggio_MG():
    """### **L3:** il raggio, il picco, `N` dalla legge al centro di (MG), dagli stati salvati `MG_01000` ... `MG_05000` *(e TBS a `10000` per `k 0`)*; **nessuna corsa.**"""
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mattone.py"))
    _presidio.avvia(__file__)
    print("=" * 110)
    print("IL RAGGIO DI (MG) DAGLI STATI SALVATI (L3; nessuna corsa): dentro R %g; N al centro dalla legge 1/(1 + rho max / rho_c), rho_c %.6f (dichiarato: (MG) non salvava cs)" % (R_T_RAGGIO, RHO_C_MG))
    print("=" * 110)
    out = []
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        for k in range(0, MT.K_RAMPA + MT.N_PIENO + 1, MT.PEZZO):
            if k:
                with np.load(os.path.join(MT.DIR_E, "MG_%05d.npz" % k)) as d:
                    Z["metti"]({kk: d[kk] for kk in Z["chiavi"]})
            else:
                Z["metti"]()
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            rg = raggio(Z, rho, c)
            r = MT.r_di(k) if k else 0.0
            N = 1.0 + r * (1.0 / (1.0 + float(rho.max()) / RHO_C_MG) - 1.0)
            out.append((k, float(rho.max()), rg, N, float(rho.sum())))
            print("    k %5d  r %.6f  il picco %.4e  il raggio %.4f  N_eff al centro (la legge) %.6f  la massa %.10e" % (k, r, rho.max(), rg, N, rho.sum()))
    np.savez_compressed(os.path.join(MT.DIR_REF, "MG_raggio.npz"), dati=np.array(out))
    print("=" * 110)
    return 0


def referto():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("PERCHE' IL LAPSE ALLARGA IL SOLITONE (Luca 23:22): (MG), (MGx2) = MGdoppio, (MG/2) = MGmezzo")
    print("=" * 130)
    righe = {}
    mg = np.load(os.path.join(MT.DIR_REF, "MG_raggio.npz"))["dati"]
    smg = np.load(os.path.join(MT.DIR_REF, "MG_serie.npz"))
    ult = smg["k"] >= smg["k"][-1] - MT.N_PIENO
    righe["MG"] = {"rho_c": RHO_C_MG, "k": mg[:, 0], "picco": mg[:, 1], "raggio": mg[:, 2], "N_c": mg[:, 3], "M": mg[:, 4],
                   "resp": float(smg["resp"][ult].max() - smg["resp"][ult].min()), "fermo": None}
    for caso, rc in CASI.items():
        f = os.path.join(MT.DIR_REF, "%s_serie.npz" % caso)
        if not os.path.exists(f):
            print("    %s: manca" % caso)
            continue
        s = np.load(f)
        ii = [i for i, k in enumerate(s["k"]) if k % MT.PEZZO == 0]
        ult = s["k"] >= s["k"][-1] - MT.N_PIENO
        righe[caso] = {"rho_c": rc, "k": s["k"][ii], "picco": s["rmax"][ii], "raggio": s["raggio"][ii], "N_c": s["N_c"][ii], "M": s["M"][ii],
                       "resp": float(s["resp"][ult].max() - s["resp"][ult].min()), "fermo": int(s["k"][-1]) < MT.K_RAMPA + MT.N_PIENO}
    print("    %-9s %12s  %-60s %-60s %-40s %8s %8s" % ("il caso", "rho_c", "il picco a k 0, 1000, ..., 5000", "il raggio", "N al centro", "A(f)", "respiro"))
    A = {}
    for caso, x in righe.items():
        A[caso] = 1.0 - x["picco"][-1] / x["picco"][0]
        print("    %-9s %12.3f  %-60s %-60s %-40s %8.4f %8.4f%s" % (caso, x["rho_c"], " ".join("%.0f" % v for v in x["picco"]), " ".join("%.3f" % v for v in x["raggio"]),
                                                              " ".join("%.4f" % v for v in x["N_c"]), A[caso], x["resp"], "  (fermato prima della fine)" if x["fermo"] else ""))
        print("    %-9s la massa: %s" % ("", " ".join("%.6e" % v for v in x["M"])))
    print("-" * 130)
    if "MGdoppio" in A:
        q = A["MGdoppio"] / A["MG"]
        if q >= SOGLIA_A:
            lett = "risposta a SOGLIA (compatibile col bilico)"
        elif q <= GRADUALE_A:
            lett = "risposta GRADUALE"
        else:
            lett = "INDECISO"
        print("  LA LETTURA L4 (le soglie del guardiano %g e %g, dichiarate): A(MGx2) / A(MG) = %.4f: %s" % (SOGLIA_A, GRADUALE_A, q, lett))
    if "MGmezzo" in righe:
        print("  (MG/2): %s" % ("COLLASSO (il picco oltre %g volte l'iniziale): un risultato" % COLLASSO if righe["MGmezzo"]["fermo"] else "nessun collasso: A = %.4f" % A["MGmezzo"]))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("prepara", "raggio_MG", "referto"))
    ap.add_argument("--caso", choices=tuple(CASI))
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.azione == "prepara":
        return prepara(x.caso, x.registro)
    return raggio_MG() if x.azione == "raggio_MG" else referto()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
