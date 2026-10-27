# -*- coding: utf-8 -*-
r"""**LA TORSIONE DEL VUOTO NELLA SUA FORMA D'ENERGIA** *([[TORSIONE-DEL-VUOTO]], [[PROGETTO-MITOSI]]; la risposta di Luca delle `16:58`; il task history
`doc/TASK_HISTORY/2026-10-27_torsione_energia.md`)*: ### **per ogni arco `theta_E = -s sum_t (eps_i - eps_j)`**, ### **`eps_k = (e_v(k) + 2 pi lambda Lambda_k)/Lambda_k`
l'energia del vuoto per unita' di norma al nodo** *(`_energia_del_legame.per_nodo`)*; ### **sul solitone `S1` col tick intero, `cs` spento:** ### **il ritmo
contro la distanza, il primo arco a `2 pi`, il freno.**

> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_energia_del_legame` *(`stato`, `per_nodo`, `densita`)*, `_torsione_del_vuoto.per_classe`,
> `_solitone_vuoto_congelato` *(`S`, `FORMA`)*, `_solitoni_triangoli`, `_modi_pi_e_solitoni.largo`, `_screening_forme_s3.forma`, `_triangoli_bassa_energia.conv`, `tick.percorri_tick`.

Gira con:  python csv/_torsione_energia.py > doc/referti_l2/torsione_energia.txt
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

JSONL = os.path.join(RADICE, "doc", "referti_l2", "torsione_energia.jsonl")
T_MAX = 2000
FATTORE = 12.0
CASI = (1e5, 1e6)
LAM_ZERO = 0.5                 # ### lo zero simmetrico: il suo lambda
ZERO = "simm"                  # ### e il suo NOME: `_triangoli_bassa_energia.conv` prende il nome, e con un numero da' la convenzione di oggi (il mio errore, 2026-10-27)
R_VICINO = 2.0                 # ### `VICINO`: `r_a <= R_VICINO w_in` (come `15df5c63`)
GUSCI = (2.0, 4.0, 8.0)        # ### i gusci `[2 w, 4 w)`, `[4 w, 8 w)`, `>= 8 w`
FINESTRA = 250
OK = [0, 0]
FALLITE = []
AVVERTENZA = ("la fase gira come l'energia solo per uno stato a energia definita; per un vuoto disturbato e' un'approssimazione, "
              "e la misura in fase non leggibile (76e85c0a) non e' una smentita dell'ipotesi (Luca, 16:58)")


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


def eps_nodo(inc, mot, st):
    """### **`eps_k = (e_v(k) + 2 pi lambda Lambda_k)/Lambda_k`:** ### **l'energia del vuoto per unita' di norma al nodo** *(la materia a zero in `per_nodo`)*, ### **e `Lambda_k`.**"""
    import _energia_del_legame as EL
    _rho, lam = EL.densita(inc, st)
    ev = EL.per_nodo(inc, mot, st, "psi_h")
    return (ev + 2 * math.pi * LAM_ZERO * lam) / lam, lam


def corsa(N, rec, senza_materia):
    import _energia_del_legame as EL
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, FATTORE, rec)
    if senza_materia:   # ### il controllo `0`: la scena di `N`, la materia a zero (il profilo non si risolve a norma zero)
        st["psi_h"][...] = 0.0
    n = inc.n
    a0, a1 = inc.nodo[0::2], inc.nodo[1::2]
    r_a = 0.5 * (rr[a0] + rr[a1])
    rho, _l = EL.densita(inc, st)
    M = float(rho.sum())
    if M > 0:   # ### la larghezza come `_energia_del_legame.corsa.forma_m`: attorno al baricentro
        cm = (rho @ pos) / M
        w_in = math.sqrt(float(rho @ np.sum((pos - cm) ** 2, axis=1)) / M)
    else:
        w_in = None
    s = float(VC.S)
    theta = np.zeros(len(a0))
    th_prec = theta.copy()
    finestre = []
    primo = None
    lam_min = math.inf
    unita = None
    t0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        for t in range(T_MAX + 1):
            if t > 0 and t % FINESTRA == 0:
                finestre.append((theta - th_prec) / FINESTRA)
                th_prec = theta.copy()
            if primo is None:
                k = np.flatnonzero(np.abs(theta) >= 2 * math.pi)
                if k.size:
                    j = int(k[np.argmax(np.abs(theta[k]))])
                    primo = {"t": t, "arco": j, "r": float(r_a[j]), "quanti": int(k.size)}
            if t == T_MAX:
                break
            eps, lam = eps_nodo(inc, mot, st)
            lam_min = min(lam_min, float(lam.min()))
            theta += -s * (eps[a0] - eps[a1])
            phi0 = complex(st["phi_h"][0])
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            if t == 0 and senza_materia:   # ### la lettura `u`: la fase per tick di un'estremita' contro `-s eps`
                unita = {"fase": float(np.angle(complex(st["phi_h"][0]) / phi0)), "meno_s_eps": float(-s * eps[inc.nodo[0]])}
    return {"N": N, "L": L, "w_in": w_in, "r_a": r_a, "theta": theta, "omega": np.abs(theta) / T_MAX, "finestre": finestre, "primo": primo,
            "lam_min": lam_min, "unita": unita, "secondi": time.time() - t0}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _modi_pi_e_solitoni as MPS
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _torsione_del_vuoto as TV
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA TORSIONE DEL VUOTO NELLA SUA FORMA D'ENERGIA: per arco theta_E = -s sum_t (eps_i - eps_j), eps l'energia del vuoto per unita' di norma al nodo; il ritmo, il primo arco a 2 pi, il freno")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_torsione_energia.py", "csv/_torsione_del_vuoto.py", "csv/_energia_del_legame.py", "csv/_solitone_vuoto_congelato.py",
                                     "csv/_solitoni_triangoli.py", "primo_ordine/energia_pesata.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: T_MAX %d FATTORE %g CASI %s ZERO %s LAM_ZERO %g R_VICINO %g GUSCI %s FINESTRA %d; da _solitone_vuoto_congelato: S %g FORMA %s; cs SPENTO (PUNTO-FISSO-CS-SOLITONE)"
          % (T_MAX, FATTORE, CASI, ZERO, LAM_ZERO, R_VICINO, GUSCI, FINESTRA, VC.S, VC.FORMA))
    print("  L'UNITA': uno stato a energia definita E per unita' di norma gira di -s E per tick (74f99039, 762cb0e8); eps_k = (e_v(k) + 2 pi lambda Lambda_k)/Lambda_k; theta_E(a) = -s sum_t (eps_i - eps_j), i, j = inc.nodo[2a], inc.nodo[2a+1]")
    print("  ### L'AVVERTENZA: %s" % AVVERTENZA)
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA, "avvertenza": AVVERTENZA})
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(VC.S)
        recs = {N: {"larghezza": MPS.largo(VC.FORMA, cc, VC.S, N)["larghezza"], "c": cc} for N in CASI}
    finally:
        MPS.LAM0 = vero
    print("### IL VUOTO UNIFORME SENZA MATERIA (la scena di N %g, la materia a zero, %d tick)" % (CASI[0], T_MAX))
    r = corsa(CASI[0], recs[CASI[0]], True)
    mx = float(np.max(np.abs(r["theta"])))
    u = r["unita"]
    print("  L %d: max |theta_E| %.3e; Lambda min %.6f (%.0f s)" % (r["L"], mx, r["lam_min"], r["secondi"]))
    print("  (u) L'UNITA': la fase misurata di un'estremita' in un tick %+.12f; -s eps %+.12f; il rapporto %.12f" % (u["fase"], u["meno_s_eps"], u["fase"] / u["meno_s_eps"]))
    scrivi({"tipo": "vuoto", "L": r["L"], "max_theta": mx, "unita": u})
    esito("DEVE PASSARE (0): il vuoto uniforme senza materia: la somma zero al bit per %d tick" % T_MAX, mx == 0.0, "max |theta_E| %.1e" % mx)
    print("-" * 130)
    ris = {}
    for N in CASI:
        r = corsa(N, recs[N], False)
        ris[N] = r
        om = r["omega"]
        w = r["w_in"]
        vic = r["r_a"] <= R_VICINO * w
        pc = TV.per_classe(r["r_a"], om)
        cl = max(pc, key=lambda x: x[1])
        gu = []
        for i, g in enumerate(GUSCI):
            m = r["r_a"] >= g * w
            if i + 1 < len(GUSCI):
                m &= r["r_a"] < GUSCI[i + 1] * w
            gu.append((g, float(om[m].mean()) if np.any(m) else None, int(m.sum())))
        fin_t = [float(np.mean(np.abs(f))) for f in r["finestre"]]
        fin_v = [float(np.mean(np.abs(f[vic]))) for f in r["finestre"]]
        n2 = int(np.sum(np.abs(r["theta"]) >= 2 * math.pi))
        r["classe"], r["gusci"] = cl, gu
        print("### N %g L %d: w_in %.4f, VICINO r <= %.2f (%d archi su %d); Lambda min nel tempo %.3e (%.0f s)" % (N, r["L"], w, R_VICINO * w, int(vic.sum()), len(om), r["lam_min"], r["secondi"]))
        print("  omega per arco (rad per tick): la media %.3e, il massimo %.3e (all'arco %d, r %.2f); in VICINO %.3e, fuori %.3e"
              % (float(om.mean()), float(om.max()), int(np.argmax(om)), float(r["r_a"][np.argmax(om)]), float(om[vic].mean()), float(om[~vic].mean())))
        print("  la classe di distanza con la media piu' alta: r in [%d, %d), media %.3e (%d archi)" % (cl[0], cl[0] + 1, cl[1], cl[2]))
        print("  i gusci (da quante w_in, media, archi): %s" % "; ".join("%g %s %d" % (g, "%.3e" % v if v is not None else "-", k) for g, v, k in gu))
        print("  per classe (r, media omega, archi): %s" % "; ".join("%d %.2e %d" % x for x in pc))
        print("  2 pi: il primo %s; a T_MAX %d archi con |theta_E| >= 2 pi; max |theta_E| %.4f"
              % ("al tick %d, l'arco %d a r %.2f (%d archi insieme)" % (r["primo"]["t"], r["primo"]["arco"], r["primo"]["r"], r["primo"]["quanti"]) if r["primo"] else "MAI",
                 n2, float(np.max(np.abs(r["theta"])))))
        print("  il freno, la media di |omega| per finestra di %d tick: tutto %s; VICINO %s" % (FINESTRA, " ".join("%.2e" % x for x in fin_t), " ".join("%.2e" % x for x in fin_v)))
        scrivi({"tipo": "corsa", "N": N, "L": r["L"], "w_in": w, "lam_min": r["lam_min"], "omega_media": float(om.mean()), "omega_max": float(om.max()),
                "omega_vicino": float(om[vic].mean()), "omega_fuori": float(om[~vic].mean()), "classe_max": cl[0], "classi": pc, "gusci": gu,
                "primo_2pi": r["primo"], "archi_2pi": n2, "finestre_tutto": fin_t, "finestre_vicino": fin_v, "secondi": r["secondi"]})
    print("-" * 130)
    print("### I CRITERI")
    v1, n1 = True, []
    for N, r in sorted(ris.items()):
        cl, gu = r["classe"], r["gusci"]
        dentro = cl[0] + 1 <= R_VICINO * r["w_in"]
        vv = [v for _g, v, _k in gu]
        cala = all(x is not None for x in vv) and all(vv[i] > vv[i + 1] for i in range(len(vv) - 1))
        v1 &= dentro and cala
        n1.append("N %g la classe [%d, %d) contro VICINO %.2f; i gusci %s" % (N, cl[0], cl[0] + 1, R_VICINO * r["w_in"], " > ".join("%.2e" % x if x is not None else "-" for x in vv)))
    esito("PUO' FALLIRE (1): il ritmo e' massimo vicino al solitone (la classe piu' alta in VICINO) e cala con la distanza (i tre gusci decrescono)", v1, "; ".join(n1), deve=False)
    print("-" * 130)
    print("### L'AVVERTENZA: %s" % AVVERTENZA)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
