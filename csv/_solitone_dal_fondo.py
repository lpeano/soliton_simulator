# -*- coding: utf-8 -*-
r"""**IL SOLITONE `S1` COL VUOTO DEL FONDO** *(la parte 2 `(c-iii)` del mandato dopo `15df5c63`, la scelta di Luca delle `18:45`; [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]];
il task history `doc/TASK_HISTORY/2026-10-27_vuoto_sul_fondo.md`, paragrafo `5`)*: ### **il solitone di `_energia_del_legame.stato`** *(`N 1e6`, `L 81`)* ### **sul flusso
costante del fondo** *(quattro scelte di fase, dichiarate)*, ### **col vuoto congelato e col tick intero: la vita, i conti per regione, la strada `A` sul disco `2 w_in`.**

> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_energia_del_legame` *(`stato`)*, `_libro_dei_conti` *(`conti_per_nodo`, `per_regione`)*,
> `_vuoto_sul_fondo` *(`fondo_uniforme`, `energia`)*, `_scomposizione_solitone`, `_solitoni_triangoli`, `_solitone_vuoto_congelato`, `_screening_forme_s3.forma`, `_triangoli_bassa_energia.conv`, `tick.percorri_tick`.

Gira con:  python csv/_solitone_dal_fondo.py > doc/referti_l2/solitone_dal_fondo.txt
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

JSONL = os.path.join(RADICE, "doc", "referti_l2", "solitone_dal_fondo.jsonl")
N = 1e6
FATTORE = 12.0
ZERO = "simm"
LAM_ZERO = 0.5
T_MAX = 2000
OGNI = 10
OGNI_VITA = 20
R_VICINO = 2.0
VITA_RIF = 320                 # ### la vita di 15df5c63 (N 1e6, L 81, simm, il tick intero)
VITA_P1 = 1280                 # ### la previsione del mandato: 4 volte la vita di oggi
DIREZIONI = ((0, 1), (1, 0), (1, 1))
FASI = (("F0", (0.0, 0.0, 0.0)), ("F1", (0.0, 2 * math.pi / 3, 4 * math.pi / 3)), ("F2", (0.0, math.pi / 2, math.pi)), ("F3", (0.0, 0.0, math.pi)))
MODI = ("congelato", "intero")
TOLL_NORMA = 1e-10
TOLL_FONDO = 1e-12
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


def fondo_con_fasi(inc, L, fasi):
    """### **Il flusso costante per direzione con una fase per direzione:** ### **la coda `+e^{i theta_d}`, la testa `-e^{i theta_d}`.**"""
    n = inc.n
    v = np.arange(n)
    m1, m2 = v // L, v % L
    phi = np.zeros(2 * inc.m, dtype=complex)
    for a in range(inc.m):
        i, j = int(inc.nodo[2 * a]), int(inc.nodo[2 * a + 1])
        d = ((int(m1[j] - m1[i]) + L // 2) % L - L // 2, (int(m2[j] - m2[i]) + L // 2) % L - L // 2)
        pos = d if (d[0] > 0 or (d[0] == 0 and d[1] > 0)) else (-d[0], -d[1])
        c = np.exp(1j * fasi[DIREZIONI.index(pos)])
        segno = 1.0 if pos == d else -1.0
        phi[2 * a] = segno * c
        phi[2 * a + 1] = -segno * c
    return phi


def corsa(rec, e_K, phi_iniziale, modo):
    import _energia_del_legame as EL
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, FATTORE, rec)
    st["phi_h"][...] = phi_iniziale
    phi0 = st["phi_h"].copy()
    w0 = rec["larghezza"]

    def forma_m():
        rho, _l = EL.densita(inc, st)
        M = float(rho.sum())
        c = (rho @ pos) / M
        w2 = float(rho @ np.sum((pos - c) ** 2, axis=1)) / M
        fr = float(rho[np.hypot(pos[:, 0] - c[0], pos[:, 1] - c[1]) <= STR.RAGGIO_FRAZ * w0].sum()) / M
        return math.sqrt(w2), fr
    w_in, _f = forma_m()
    vic = rr <= R_VICINO * w_in
    mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(inc.n, dtype=bool)}
    serie, gA = [], []
    vita, vita20 = None, None
    prec_d2 = None
    t0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        for t in range(T_MAX + 1):
            c = LC.conti_per_nodo(inc, mot, st, e_K, LAM_ZERO)
            d2 = math.fsum(c["tot"][vic].tolist())
            if prec_d2 is not None:
                gA.append((t, d2 - prec_d2))
            prec_d2 = d2
            if t % OGNI == 0:
                w, fr = forma_m()
                rotto = abs(w / w_in - 1.0) > STR.TOLL_LARGH or fr < STR.FRAZ_MIN
                if vita is None and rotto:
                    vita = t
                if vita20 is None and rotto and t % OGNI_VITA == 0:
                    vita20 = t
                serie.append({"t": t, "larghezza": w, "frazione": fr, "E": LC.per_regione(c, mas)})
            if t < T_MAX:
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                if modo == "congelato":
                    st["phi_h"][...] = phi0
    e0 = serie[0]["E"]["totale"]
    dM = max(abs(x["E"]["totale"]["M"] - e0["M"]) / e0["M"] for x in serie)
    dV = max(abs(x["E"]["totale"]["V"] - e0["V"]) / e0["V"] for x in serie)
    return {"L": L, "w_in": w_in, "vita": vita, "vita20": vita20, "dM": dM, "dV": dV, "serie": serie, "gA": gA, "secondi": time.time() - t0}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _energia_del_legame as EL
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _vuoto_sul_fondo as VSF
    import composizione as CM
    import scena_l2 as SL
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL SOLITONE S1 COL VUOTO DEL FONDO (c-iii): quattro fasi del flusso costante, il vuoto congelato e il tick intero; la vita, i conti per regione, la strada A sul disco 2 w_in")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_solitone_dal_fondo.py", "csv/_energia_del_legame.py", "csv/_libro_dei_conti.py", "csv/_vuoto_sul_fondo.py",
                                     "primo_ordine/tick.py", "primo_ordine/materia_vuoto.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: N %g FATTORE %g ZERO %s LAM_ZERO %g T_MAX %d OGNI %d OGNI_VITA %d R_VICINO %g VITA_RIF %d VITA_P1 %d DIREZIONI %s FASI %s MODI %s TOLL_NORMA %g TOLL_FONDO %g; S %g FORMA %s; cs spento"
          % (N, FATTORE, ZERO, LAM_ZERO, T_MAX, OGNI, OGNI_VITA, R_VICINO, VITA_RIF, VITA_P1, DIREZIONI, [(n, tuple(round(x, 6) for x in f)) for n, f in FASI], MODI, TOLL_NORMA, TOLL_FONDO, VC.S, VC.FORMA))
    print("  ### F0 (le tre fasi uguali) e' la SCELTA dichiarata di Luca (18:45); F1-F3 la famiglia, dichiarata prima. La cautela: H_tot col legame S1 deriva (ENERGIA-NON-CONSERVATA-S1)")
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(VC.S)
        rec = {"larghezza": MPS.largo(VC.FORMA, cc, VC.S, N)["larghezza"], "c": cc}
    finally:
        MPS.LAM0 = vero
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, FATTORE, rec)
    incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
    Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
    e_K = Eu / Mu
    sc = N * abs(e_K)
    print("  N %g L %d: e_K(0) %+.6f; l'unita' N |e_K(0)| = %.6e" % (N, L, e_K, sc))
    # ------------------------------------------------------------------ i controlli k0, k1
    f0_ref, _d = VSF.fondo_uniforme(inc, L, SL.VUOTO_PER_ESTREMITA)
    vuoti = {nome: fondo_con_fasi(inc, L, f) for nome, f in FASI}
    esito("DEVE PASSARE (k0): il flusso F0 = _vuoto_sul_fondo.fondo_uniforme AL BIT", vuoti["F0"].tobytes() == f0_ref.tobytes(), "")
    ok1, n1 = True, []
    for nome, ph in vuoti.items():
        s = dict(st)
        s["psi_h"] = np.zeros_like(st["psi_h"])
        s["phi_h"] = ph
        e = VSF.energia(mot, s, "phi_h", "tutto") / float(np.sum(np.abs(ph) ** 2))
        ok1 &= abs(e + 2 * math.pi) <= TOLL_FONDO
        n1.append("%s %.12f" % (nome, e))
    esito("DEVE PASSARE (k1): ogni vuoto del fondo ha E/V = -2 pi entro %g" % TOLL_FONDO, ok1, "; ".join(n1))
    print("-" * 130)
    # ------------------------------------------------------------------ le corse
    casi = [("uniforme", "intero", np.full(2 * inc.m, SL.VUOTO_PER_ESTREMITA, dtype=complex))]
    casi += [(nome, modo, vuoti[nome]) for nome, _f in FASI for modo in MODI]
    ris = {}
    for nome, modo, ph in casi:
        r = corsa(rec, e_K, ph, modo)
        ris[(nome, modo)] = r
        e0 = r["serie"][0]["E"]
        tv = r["vita20"] if r["vita20"] is not None else T_MAX
        ev = [x for x in r["serie"] if x["t"] == tv][0]["E"]
        ef = r["serie"][-1]["E"]
        g = np.array([x[1] for x in r["gA"]])
        tt = np.array([x[0] for x in r["gA"]])
        pr, do = tt <= tv, tt > tv
        A = {"entrate_vita": float(g[pr & (g > 0)].sum()) / sc, "uscite_vita": float(g[pr & (g < 0)].sum()) / sc,
             "entrate_dopo": float(g[do & (g > 0)].sum()) / sc, "uscite_dopo": float(g[do & (g < 0)].sum()) / sc, "tick_entrata_dopo": int(np.sum(do & (g > 0))), "tick_dopo": int(do.sum())}
        print("### %-8s %-9s (L %d, w_in %.4f): vita %s (ogni 20: %s); dM %.1e dV %.1e (%.0f s)" % (nome, modo, r["L"], r["w_in"], r["vita"], r["vita20"], r["dM"], r["dV"], r["secondi"]))
        for t_, e_ in (("alla vita %d" % tv, ev), ("a T_MAX", ef)):
            for reg in ("totale", "vicino", "lontano"):
                print("  %-14s %-8s: vuoto %+.4e  cinetica %+.4e  legame %+.4e  H_tot %+.4e" % (t_, reg, e_[reg]["vuo"] - e0[reg]["vuo"], e_[reg]["cin"] - e0[reg]["cin"], e_[reg]["leg"] - e0[reg]["leg"], e_[reg]["tot"] - e0[reg]["tot"]))
        print("  la strada A sul disco 2 w_in (N |e_K(0)|): fino alla vita entrate %+.4e uscite %+.4e; dopo entrate %+.4e uscite %+.4e (%d tick in entrata su %d)"
              % (A["entrate_vita"], A["uscite_vita"], A["entrate_dopo"], A["uscite_dopo"], A["tick_entrata_dopo"], A["tick_dopo"]))
        scrivi({"tipo": "corsa", "vuoto": nome, "modo": modo, "L": r["L"], "w_in": r["w_in"], "vita": r["vita"], "vita20": r["vita20"], "dM": r["dM"], "dV": r["dV"],
                "strada_A": A, "serie": r["serie"], "secondi": r["secondi"]})
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (k2): M e V entro %g in ogni corsa" % TOLL_NORMA, all(r["dM"] <= TOLL_NORMA and r["dV"] <= TOLL_NORMA for r in ris.values()),
          "dM max %.1e dV max %.1e" % (max(r["dM"] for r in ris.values()), max(r["dV"] for r in ris.values())))
    ru = ris[("uniforme", "intero")]
    esito("DEVE PASSARE (k3): il controllo positivo: col vuoto uniforme la vita (ogni 20) = %d di 15df5c63" % VITA_RIF, ru["vita20"] == VITA_RIF, "vita20 %s" % ru["vita20"])
    p1, n_p1, p2, n_p2 = True, [], True, []
    for nome, _f in FASI:
        r = ris[(nome, "intero")]
        v = r["vita20"]
        p1 &= v is None or v > VITA_P1
        n_p1.append("%s %s" % (nome, v if v is not None else "oltre %d" % T_MAX))
        tv = v if v is not None else T_MAX
        dv = [x for x in r["serie"] if x["t"] == tv][0]["E"]["totale"]["vuo"] - r["serie"][0]["E"]["totale"]["vuo"]
        p2 &= dv > 0
        n_p2.append("%s %+.3e" % (nome, dv))
    esito("PUO' FALLIRE (p1): col fondo e il tick intero il solitone vive oltre %d tick (a ogni fase)" % VITA_P1, p1, "; ".join(n_p1), deve=False)
    esito("PUO' FALLIRE (p2): il vuoto PRENDE energia dalla materia (Delta E_vuoto > 0 sul toro alla vita, a ogni fase)", p2, "; ".join(n_p2), deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
