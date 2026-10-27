# -*- coding: utf-8 -*-
r"""**LA TORSIONE DEL VUOTO SUGLI ARCHI, ATTORNO AL SOLITONE `S1`** *([[PROGETTO-MITOSI]], [[LIBRO-DEI-CONTI]], [[ENERGIA-DEL-LEGAME]]; il task history
`doc/TASK_HISTORY/2026-10-27_torsione_del_vuoto.md`)*: ### **la torsione `(a3)` di ogni arco** *(`arg(conj(phi[2a+1]) phi[2a])`, srotolata tick per tick)*
### **sul solitone `S1` col tick intero, `cs` spento e acceso** *(`tick.tick_con_cs`, `lambda_c` = la media di `Lambda` per nodo a `t 0`)*: ### **il ritmo
contro la distanza, contro `Delta cs` e contro `Delta e_vuoto` ai capi; il primo arco a `2 pi`; il freno per finestre.**

> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_energia_del_legame` *(`stato`, `per_nodo`)*, `_solitone_vuoto_congelato` *(`S`, `FORMA`)*,
> `_solitoni_triangoli`, `_modi_pi_e_solitoni.largo`, `_screening_forme_s3.forma`, `_triangoli_bassa_energia.conv`, `tick.percorri_tick`, `tick.tick_con_cs`.

Gira con:  python csv/_torsione_del_vuoto.py > doc/referti_l2/torsione_del_vuoto.txt
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

JSONL = os.path.join(RADICE, "doc", "referti_l2", "torsione_del_vuoto.jsonl")
T_MAX = 2000
FATTORE = 12.0
CASI = (1e5, 1e6)
LAM_ZERO = 0.5                 # ### lo zero simmetrico
RAPPORTO = 1.0                 # ### `lambda_c = RAPPORTO x` la media di `Lambda` per nodo a `t 0` (come `_vuoto_disturbato`)
R_VICINO = 2.0                 # ### `VICINO`: `r_a <= R_VICINO w_in` (come `15df5c63`)
FINESTRA = 250
OGNI_E = 10                    # ### `Delta e_vuoto` ogni `OGNI_E` tick (costa)
GUARDIA = math.pi / 2
SOGLIA_CORR = 0.9
SINT = ((0.7, True), (3.5, False))   # ### (il ritmo sintetico in rad per tick, se lo srotolamento deve tenere)
TOLL_SINT = 1e-12
OK = [0, 0]
FALLITE = []


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


class Contatore:
    """### **La torsione srotolata:** `theta += arg(z(t) conj(z(t-1)))`, ### **e il massimo dell'incremento** *(la guardia)*."""

    def __init__(self, z):
        self.z = z.copy()
        self.theta = np.zeros(z.shape)
        self.d_max = 0.0
        self.d_arco = np.zeros(z.shape)           # ### il massimo incremento per arco (la diagnosi della guardia)
        self.z_arco = np.abs(z).copy()            # ### il minimo di |z| per arco

    def avanza(self, z):
        d = np.angle(z * np.conj(self.z))
        self.d_max = max(self.d_max, float(np.max(np.abs(d))) if d.size else 0.0)
        np.maximum(self.d_arco, np.abs(d), out=self.d_arco)
        np.minimum(self.z_arco, np.abs(z), out=self.z_arco)
        self.theta += d
        self.z = z.copy()


def z_archi(st):
    v = st["phi_h"].reshape(-1, 2)
    return np.conj(v[:, 1]) * v[:, 0]


def pearson(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if np.std(x) == 0.0 or np.std(y) == 0.0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def corsa(N, rec, cs_acceso, senza_materia):
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
    rho = np.zeros(n)
    np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    M = float(rho.sum())
    if M > 0:   # ### la larghezza come `_energia_del_legame.corsa.forma_m`: attorno al baricentro
        cm = (rho @ pos) / M
        w_in = math.sqrt(float(rho @ np.sum((pos - cm) ** 2, axis=1)) / M)
    else:
        w_in = None
    lc = RAPPORTO * float(np.mean(mot.densita_vuoto(st))) if cs_acceso else None
    cont = Contatore(z_archi(st))
    zmin = float(np.min(np.abs(cont.z)))
    dcs = np.zeros(len(a0))
    dev = np.zeros(len(a0))
    n_ev = 0
    finestre = []
    th_prec = cont.theta.copy()
    primo = None
    giri = []
    t0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(LAM_ZERO):
        for t in range(T_MAX + 1):
            if t % OGNI_E == 0 and M > 0:
                ev = EL.per_nodo(inc, mot, st, "psi_h")
                dev += np.abs(ev[a0] - ev[a1])
                n_ev += 1
            if t > 0 and t % FINESTRA == 0:
                finestre.append((cont.theta - th_prec) / FINESTRA)
                th_prec = cont.theta.copy()
            if primo is None:
                k = np.flatnonzero(np.abs(cont.theta) >= 2 * math.pi)
                if k.size:
                    j = int(k[np.argmax(np.abs(cont.theta[k]))])
                    primo = {"t": t, "arco": j, "r": float(r_a[j]), "quanti": int(k.size)}
            if t == T_MAX:
                break
            if cs_acceso:
                try:
                    g = TK.tick_con_cs(st, mot, par, lc, ())
                except AssertionError as e:
                    raise AssertionError("al tick %d: %s" % (t, e))
                giri.append(g)
            else:
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            cont.avanza(z_archi(st))
            zmin = min(zmin, float(np.min(np.abs(cont.z))))
            cs = np.asarray(mot.cs, float)
            dcs += np.abs(cs[a0] - cs[a1])
    om = cont.theta / T_MAX
    return {"N": N, "L": L, "cs_acceso": cs_acceso, "lambda_c": lc, "w_in": w_in, "r_a": r_a, "omega": om, "theta": cont.theta, "d_max": cont.d_max, "z_min": zmin,
            "d_arco": cont.d_arco, "z_arco": cont.z_arco, "dcs": dcs / T_MAX, "dev": dev / n_ev if n_ev else None, "finestre": finestre, "primo": primo, "giri_max": max(giri) if giri else None,
            "secondi": time.time() - t0}


def per_classe(r_a, x):
    k = np.floor(r_a).astype(int)
    out = []
    for c in range(int(k.max()) + 1):
        m = k == c
        if np.any(m):
            out.append((c, float(np.mean(x[m])), int(m.sum())))
    return out


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _modi_pi_e_solitoni as MPS
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA TORSIONE DEL VUOTO SUGLI ARCHI ATTORNO AL SOLITONE S1: il ritmo per arco contro la distanza, contro Delta cs e Delta e_vuoto ai capi; il primo arco a 2 pi; il freno")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_torsione_del_vuoto.py", "csv/_energia_del_legame.py", "csv/_solitone_vuoto_congelato.py", "csv/_solitoni_triangoli.py",
                                     "primo_ordine/tick.py", "primo_ordine/flussi_parziali.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: T_MAX %d FATTORE %g CASI %s LAM_ZERO %g RAPPORTO %g R_VICINO %g FINESTRA %d OGNI_E %d GUARDIA %.6f SOGLIA_CORR %g SINT %s TOLL_SINT %g; da _solitone_vuoto_congelato: S %g FORMA %s"
          % (T_MAX, FATTORE, CASI, LAM_ZERO, RAPPORTO, R_VICINO, FINESTRA, OGNI_E, GUARDIA, SOGLIA_CORR, SINT, TOLL_SINT, VC.S, VC.FORMA))
    print("  la torsione dell'arco a: arg(conj(phi_h[2a+1]) phi_h[2a]) srotolata tick per tick; il ritmo omega_a = theta_a(T_MAX)/T_MAX rad per tick; r_a la media delle distanze dei due nodi")
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    print("### LO SROTOLAMENTO SU FASI SINTETICHE")
    for w, tiene in SINT:
        tt = np.arange(T_MAX + 1)
        c = Contatore(np.exp(1j * w * tt[:1]))
        for t in tt[1:]:
            c.avanza(np.exp(1j * w * np.array([t])))
        rit = float(c.theta[0]) / T_MAX
        if tiene:
            esito("DEVE PASSARE (s1): un ritmo sintetico di %g rad per tick si srotola entro %g, la guardia non scatta" % (w, TOLL_SINT),
                  abs(rit - w) <= TOLL_SINT and c.d_max < GUARDIA, "ritmo %.15f d_max %.4f" % (rit, c.d_max))
        else:
            esito("DEVE PASSARE (s2): un ritmo sintetico di %g rad per tick (oltre pi) fa scattare la guardia" % w, c.d_max > GUARDIA, "ritmo letto %.6f d_max %.4f" % (rit, c.d_max))
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(VC.S)
        recs = {N: {"larghezza": MPS.largo(VC.FORMA, cc, VC.S, N)["larghezza"], "c": cc} for N in CASI}
    finally:
        MPS.LAM0 = vero
    print("-" * 130)
    print("### IL VUOTO UNIFORME SENZA MATERIA (la scena di N %g, la materia a zero, %d tick)" % (CASI[0], T_MAX))
    ok0, n0 = True, []
    for acc in (False, True):
        r = corsa(CASI[0], recs[CASI[0]], acc, True)
        mx = float(np.max(np.abs(r["theta"])))
        ok0 &= mx == 0.0
        n0.append("cs %s max|theta| %.1e" % ("acceso" if acc else "spento", mx))
        print("  N 0 L %d cs %-6s: max |theta| %.3e; d_max %.3e; |z| min %.6f; lambda_c %s (%.0f s)" % (r["L"], "acceso" if acc else "spento", mx, r["d_max"], r["z_min"], r["lambda_c"], r["secondi"]))
        scrivi({"tipo": "vuoto", "L": r["L"], "cs_acceso": acc, "max_theta": mx, "d_max": r["d_max"]})
    esito("DEVE PASSARE (0): il vuoto uniforme senza materia: la torsione zero al bit, cs spento e acceso", ok0, "; ".join(n0))
    print("-" * 130)
    ris = {}
    for N in CASI:
        for acc in (False, True):
            try:
                r = corsa(N, recs[N], acc, False)
            except AssertionError as e:
                print("  ### N %g cs %s: IL PUNTO FISSO DI cs ALZA: %s" % (N, acc, e))
                scrivi({"tipo": "alza", "N": N, "cs_acceso": acc, "errore": str(e)})
                continue
            ris[(N, acc)] = r
            om = np.abs(r["omega"])
            vic = r["r_a"] <= R_VICINO * r["w_in"]
            pc = per_classe(r["r_a"], om)
            cl = max(pc, key=lambda x: x[1])
            c_cs = pearson(om, r["dcs"]) if acc else None
            c_ev = pearson(om, r["dev"])
            fin_t = [float(np.mean(np.abs(f))) for f in r["finestre"]]
            fin_v = [float(np.mean(np.abs(f[vic]))) for f in r["finestre"]]
            n2 = int(np.sum(np.abs(r["theta"]) >= 2 * math.pi))
            print("### N %g L %d cs %s (lambda_c %s): w_in %.4f, VICINO r <= %.2f (%d archi su %d); d_max %.4f; |z| min %.6f; i giri del punto fisso max %s (%.0f s)"
                  % (N, r["L"], "ACCESO" if acc else "spento", "%.6f" % r["lambda_c"] if acc else "None", r["w_in"], R_VICINO * r["w_in"], int(vic.sum()), len(om), r["d_max"], r["z_min"], r["giri_max"], r["secondi"]))
            fuori_g = r["d_arco"] > GUARDIA
            if np.any(fuori_g):
                print("  ### LA GUARDIA: %d archi su %d con un incremento oltre pi/2, a r da %.2f a %.2f; il loro |z| minimo da %.2e a %.2e (gli altri archi: |z| minimo da %.2e)"
                      % (int(fuori_g.sum()), len(om), float(r["r_a"][fuori_g].min()), float(r["r_a"][fuori_g].max()), float(r["z_arco"][fuori_g].min()), float(r["z_arco"][fuori_g].max()),
                         float(r["z_arco"][~fuori_g].min())))
            print("  |omega| per arco: la media %.3e, il massimo %.3e (all'arco %d, r %.2f); in VICINO %.3e, fuori %.3e"
                  % (float(om.mean()), float(om.max()), int(np.argmax(om)), float(r["r_a"][np.argmax(om)]), float(om[vic].mean()), float(om[~vic].mean())))
            print("  la classe di distanza con la media piu' alta: r in [%d, %d), media %.3e (%d archi)" % (cl[0], cl[0] + 1, cl[1], cl[2]))
            print("  per classe (r, media |omega|, archi): %s" % "; ".join("%d %.2e %d" % x for x in pc))
            print("  la correlazione di |omega| con Delta cs: %s; con Delta e_vuoto: %s" % ("%.4f" % c_cs if c_cs is not None else "-", "%.4f" % c_ev if c_ev is not None else "-"))
            if acc:
                print("  Delta cs per arco (mediato nel tempo): la media %.3e, il massimo %.3e" % (float(r["dcs"].mean()), float(r["dcs"].max())))
            print("  2 pi: il primo %s; a T_MAX %d archi con |theta| >= 2 pi; max |theta| %.4f"
                  % ("al tick %d, l'arco %d a r %.2f (%d archi insieme)" % (r["primo"]["t"], r["primo"]["arco"], r["primo"]["r"], r["primo"]["quanti"]) if r["primo"] else "MAI",
                     n2, float(np.max(np.abs(r["theta"])))))
            print("  il freno, la media di |omega| per finestra di %d tick: tutto %s; VICINO %s" % (FINESTRA, " ".join("%.2e" % x for x in fin_t), " ".join("%.2e" % x for x in fin_v)))
            scrivi({"tipo": "corsa", "N": N, "L": r["L"], "cs_acceso": acc, "lambda_c": r["lambda_c"], "w_in": r["w_in"], "d_max": r["d_max"], "z_min": r["z_min"], "giri_max": r["giri_max"],
                    "archi_oltre_guardia": int(fuori_g.sum()), "omega_media": float(om.mean()), "omega_max": float(om.max()), "omega_vicino": float(om[vic].mean()), "omega_fuori": float(om[~vic].mean()),
                    "classe_max": cl[0], "classi": pc, "corr_cs": c_cs, "corr_ev": c_ev, "primo_2pi": r["primo"], "archi_2pi": n2, "finestre_tutto": fin_t, "finestre_vicino": fin_v,
                    "secondi": r["secondi"]})
    print("-" * 130)
    print("### I CRITERI")
    g_ok = all(r["d_max"] < GUARDIA for r in ris.values())
    esito("DEVE PASSARE (g): in ogni corsa col solitone l'incremento per tick sotto pi/2 (lo srotolamento valido)", g_ok and len(ris) == 2 * len(CASI),
          "; ".join("N %g cs %s %.4f" % (N, a, r["d_max"]) for (N, a), r in sorted(ris.items())) + ("" if len(ris) == 2 * len(CASI) else " -- CORSE MANCANTI"))
    v1, n1 = True, []
    v2, n2_ = True, []
    for N in CASI:
        r = ris.get((N, True))
        if r is None:
            v1 = v2 = False
            continue
        om = np.abs(r["omega"])
        cl = max(per_classe(r["r_a"], om), key=lambda x: x[1])
        dentro = cl[0] + 1 <= R_VICINO * r["w_in"]
        v1 &= dentro
        n1.append("N %g la classe [%d, %d) contro VICINO %.2f" % (N, cl[0], cl[0] + 1, R_VICINO * r["w_in"]))
        c = pearson(om, r["dcs"])
        v2 &= c is not None and c > SOGLIA_CORR
        n2_.append("N %g %s" % (N, "%.4f" % c if c is not None else "-"))
    esito("PUO' FALLIRE (1): con cs acceso il ritmo e' massimo vicino al solitone (la classe di distanza con la media piu' alta in VICINO)", v1, "; ".join(n1), deve=False)
    esito("PUO' FALLIRE (2): con cs acceso il ritmo e' proporzionale a Delta cs (Pearson > %g)" % SOGLIA_CORR, v2, "; ".join(n2_), deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
