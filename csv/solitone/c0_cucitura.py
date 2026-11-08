# -*- coding: utf-8 -*-
r"""**LA CUCITURA ALLE RIPRESE: C0 (IMPULSO ALLA RIPRESA?) E C1 (L'INDIZIO DEI SALTI)** *(Luca `2026-11-08` `19:25`; il task history `doc/TASK_HISTORY/2026-11-07_allungamenti_coppia_30000.md`, sez. `7.7`)*. [[PIANO-2D-3D]]

    python csv/solitone/c0_cucitura.py > doc/referti_l2/c0_cucitura.txt

### **C0:** **lo stato completo di `TBS` al tick `100000`** *(l'inizio di un pezzo)*; **il ciclo della corsa** *(`AC.tick`, poi `BO.assorbi` con `c(t) F3` e gli accumulatori: le righe di
`corsa_accensione.corsa`, come `test_stato_completo.ciclo`)* **da `100000` a `120000` SENZA interruzione** *(attraverso il confine `110000`)*. **`C0-A`** *(prima del confine: la copia del
ciclo)*: **a `110000` = lo `sha_fine` registrato del pezzo**; **`C0`** *(dopo il confine)*: **a `120000` = lo stato registrato dalla corsa vera, ripresa a `110000`; AL BIT, ogni chiave.**
**Gli accumulatori del bordo contro i campioni del jsonl.** **C1:** **attorno a ogni confine di `TB3` e `TBS`: i campioni doppi o mancanti** *(il passo fra due `t`)*, **e il salto di
`E + E_ass` e della norma** *(`E.totale.M + M_ass`)* **contro la mediana di `|dx|`** *(oltre `5` volte si stampa: mio, una stampa)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"
TICK0 = 100000
CONFINE = 110000
TICK1 = 120000
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
ACC = ("M_ass", "V_ass", "E_ass")
SALTO = 5.0                    # ### C1, mio: una stampa oltre 5 volte la mediana di |dx|
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def c1(nome):
    from solitone import corsa_accensione as CA
    rr, camp = CA.serie(nome)[:2]
    t = np.array([c["t"] for c in camp])
    dt = np.diff(t)
    confini = sorted({r["t1"] for r in rr[:-1]})
    passo = int(np.median(dt))
    doppi = int(np.sum(dt == 0))
    salti_t = [(int(t[i]), int(dt[i])) for i in range(len(dt)) if dt[i] != passo]
    con_bordo = camp[0].get("bordo") and camp[0]["bordo"].get("E_ass") is not None
    E = np.array([c["E"]["totale"]["tot"] + (c["bordo"]["E_ass"] if con_bordo else 0.0) for c in camp])
    M = np.array([c["E"]["totale"]["M"] + (c["bordo"]["M_ass"] if con_bordo else 0.0) for c in camp])
    print("  C1 %s: %d campioni, il passo %d tick; campioni doppi %d; passi diversi dal passo %d %s; %d confini" % (nome, len(t), passo, doppi, len(salti_t), salti_t[:6], len(confini)))
    for nomeg, x in (("E + E_ass" if con_bordo else "E", E), ("la norma", M)):
        dx = np.abs(np.diff(x))
        med = float(np.median(dx))
        al = []
        for T in confini:
            i = int(np.searchsorted(t, T))
            if 0 < i < len(t):
                al.append((T, float(abs(x[i] - x[i - 1])) / med if med > 0 else float("inf")))
        fuori = [(T, r) for T, r in al if r > SALTO]
        print("     %-10s la mediana di |dx| %.3e; il salto al confine / la mediana: il massimo %.2f, la media %.2f; oltre %g: %s"
              % (nomeg, med, max(r for _T, r in al), float(np.mean([r for _T, r in al])), SALTO, fuori[:6] or "nessuno"))
    return doppi, salti_t


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    for m in ("__init__", "bordo", "accensione", "corsa_accensione", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA CUCITURA ALLE RIPRESE (Luca 19:25): C0 il ciclo della corsa CONTINUO da %d a %d attraverso il confine %d, contro la corsa vera di %s ripresa al confine; C1 i salti" % (TICK0, TICK1, CONFINE, CORSA))
    print("=" * 130)
    print("### C1 (l'indizio, dai jsonl)")
    for nome in ("TB3", "TBS"):
        c1(nome)
    sys.stdout.flush()
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr, camp = CA.serie(CORSA)[:2]
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    riga_a = [r for r in rr if r["t0"] == TICK0][0]
    riga_p = [r for r in rr if r["t1"] == TICK0][0]
    assert riga_a["t1"] == CONFINE, riga_a["t1"]
    camp_t = {c["t"]: c for c in camp}
    bor0 = rr[0]["bordo"]
    K = int(round(CA.CORSE[CORSA][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, inc, mot, par = z["st"], z["inc"], z["mot"], z["par"]
        g_e, _gn, _r = BO.g_estremita(z, bor0["c0"][0], bor0["c0"][1], bor0["R_A"], bor0["g_max"])
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        with np.load(FILE_LIB) as d:
            assert int(d["t"]) == TICK0
            for k in chiavi:
                st[k][...] = d[k]
        print("### C0: lo stato di %s a %d dalla libreria = lo stato registrato: %s" % (CORSA, TICK0, V.shas(z) == stati[TICK0]["sha"]))
        bor = {k: float(riga_p["bordo"][k]) for k in ACC}       # ### gli accumulatori alla fine del pezzo prima (t1 = TICK0)
        acc_d = {}

        def ciclo(t):
            AC.tick(z, t, K)
            e_pr = float(np.sum(LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"]))
            dM, dV = BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v)
            bor["M_ass"] += dM
            bor["V_ass"] += dV
            bor["E_ass"] += e_pr - float(np.sum(LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"]))
            if t in camp_t and t % 1000 == 0:
                acc_d[t] = max(abs(bor[k] - camp_t[t]["bordo"][k]) / max(abs(camp_t[t]["bordo"][k]), 1e-300) for k in ACC)
        a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
        with a_, b_:
            for t in range(TICK0 + 1, CONFINE + 1):
                ciclo(t)
        sh_c = V.shas(z)
        div_a = sorted(k for k in riga_a["sha_fine"] if sh_c.get(k) != riga_a["sha_fine"][k])
        esito("DEVE PASSARE: C0-A il ciclo continuo a %d (PRIMA del confine) = lo sha_fine registrato del pezzo %d -> %d, ogni chiave" % (CONFINE, TICK0, CONFINE), not div_a, "diverse %s" % div_a)
        a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
        with a_, b_:
            for t in range(CONFINE + 1, TICK1 + 1):
                ciclo(t)
        sh_d = V.shas(z)
        reg = stati[TICK1]["sha"]
        div = sorted(k for k in reg if sh_d.get(k) != reg[k])
        esito("DEVE PASSARE: C0 il ciclo continuo a %d (DOPO il confine %d) = lo stato registrato dalla corsa vera ripresa al confine, ogni chiave" % (TICK1, CONFINE), not div, "%d chiavi; diverse %s" % (len(reg), div))
        print("  gli accumulatori del bordo (continui) contro i campioni del jsonl, ogni 1000 tick: lo scarto relativo massimo %.3e (%d campioni; al confine e dopo: %s)"
              % (max(acc_d.values()), len(acc_d), {t: "%.1e" % v for t, v in sorted(acc_d.items()) if CONFINE - 1000 <= t <= CONFINE + 2000}))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
