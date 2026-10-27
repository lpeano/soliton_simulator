# -*- coding: utf-8 -*-
r"""**IL SOLITONE `S1` COL VUOTO DEL FONDO** *(la parte 2 `(c-iii)` del mandato dopo `15df5c63`, la scelta di Luca delle `18:45`; [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]];
il task history `doc/TASK_HISTORY/2026-10-27_vuoto_sul_fondo.md`, paragrafi `5` e `5-bis`)*: ### **il solitone di `_energia_del_legame.stato`** *(`N 1e6`, `L 81`)* ### **sul
flusso costante del fondo** *(quattro scelte di fase, dichiarate)*, ### **col vuoto congelato e col tick intero, A `s 0.075`** *(il risolutore a quel passo; la scelta
dichiarata dopo `regime_del_passo.txt`)*: ### **la vita, i conti per regione, la strada `A` sul disco `2 w_in`; il controllo positivo a `s 0.3`.**

> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_energia_del_legame` *(`stato`, `densita`)*, `_libro_dei_conti` *(`conti_per_nodo`, `per_regione`)*,
> `_vuoto_sul_fondo` *(`fondo_uniforme`, `energia`)*, `_scomposizione_solitone`, `_solitoni_triangoli`, `_solitone_vuoto_congelato` *(`S` cambiato IN MEMORIA)*, `_screening_forme_s3.forma`,
> `_triangoli_bassa_energia.conv`, `tick.percorri_tick`.

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
L_TORO = 81
ZERO = "simm"
LAM_ZERO = 0.5
S_RIF = 0.3                    # ### il passo di 15df5c63: il controllo positivo k3
S_CORSA = 0.075                # ### il passo delle corse (regime_del_passo.txt, 99eb7a42: la deviazione di H_tot sotto l'1% della perdita del vuoto)
TAU = 600.0                    # ### il tempo fisico: 2000 tick a s 0.3
OGNI_TAU = 3.0                 # ### i conti per regione ogni 3 di tempo fisico (10 tick a s 0.3)
OGNI_VITA_TAU = 6.0            # ### la vita ogni 6 di tempo fisico (20 tick a s 0.3)
R_VICINO = 2.0
VITA_RIF = 320                 # ### la vita di 15df5c63 (N 1e6, L 81, simm, il tick intero, s 0.3), in tick
FATTORE_P1 = 4.0               # ### la previsione del mandato: 4 volte la vita col vuoto uniforme, allo stesso s, in tempo fisico
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


def prepara(s):
    """### **Il risolutore a questo `s`** *(`VC.S` IN MEMORIA, come `_regime_del_passo`)*: `rec`, `e_K`, e la scena sul toro `L_TORO`."""
    import _energia_del_legame as EL
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    VC.S = s
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(s)
        ls = MPS.largo(VC.FORMA, cc, s, N)
    finally:
        MPS.LAM0 = vero
    rec = {"larghezza": ls["larghezza"], "c": cc, "mu": ls["mu"], "fattore": (L_TORO - 0.1) / ls["larghezza"]}
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, rec["fattore"], rec)
    assert L == L_TORO, (s, L)
    incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
    Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
    return rec, Eu / Mu, inc, mot, st


def corsa(rec, e_K, phi_iniziale, modo, s):
    import _energia_del_legame as EL
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    assert VC.S == s, (VC.S, s)
    T_MAX = int(round(TAU / s))
    OGNI = int(round(OGNI_TAU / s))
    OGNI_VITA = int(round(OGNI_VITA_TAU / s))
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, rec["fattore"], rec)
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
    return {"L": L, "s": s, "w_in": w_in, "vita": vita, "vita20": vita20, "tau_vita": vita20 * s if vita20 is not None else None, "T_MAX": T_MAX,
            "dM": dM, "dV": dV, "serie": serie, "gA": gA, "secondi": time.time() - t0}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _solitone_vuoto_congelato as VC
    import _vuoto_sul_fondo as VSF
    import composizione as CM
    import scena_l2 as SL
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL SOLITONE S1 COL VUOTO DEL FONDO (c-iii): quattro fasi del flusso costante, il vuoto congelato e il tick intero, a s %g; la vita, i conti per regione, la strada A sul disco 2 w_in" % S_CORSA)
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_solitone_dal_fondo.py", "csv/_energia_del_legame.py", "csv/_libro_dei_conti.py", "csv/_vuoto_sul_fondo.py",
                                     "primo_ordine/tick.py", "primo_ordine/materia_vuoto.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: N %g L_TORO %d ZERO %s LAM_ZERO %g S_RIF %g S_CORSA %g TAU %g OGNI_TAU %g OGNI_VITA_TAU %g R_VICINO %g VITA_RIF %d FATTORE_P1 %g DIREZIONI %s FASI %s MODI %s TOLL_NORMA %g TOLL_FONDO %g; FORMA S1; cs spento"
          % (N, L_TORO, ZERO, LAM_ZERO, S_RIF, S_CORSA, TAU, OGNI_TAU, OGNI_VITA_TAU, R_VICINO, VITA_RIF, FATTORE_P1, DIREZIONI, [(n, tuple(round(x, 6) for x in f)) for n, f in FASI], MODI, TOLL_NORMA, TOLL_FONDO))
    print("  ### F0 (le tre fasi uguali) e' la SCELTA dichiarata di Luca (18:45); F1-F3 la famiglia, dichiarata prima. ### IL PASSO s %g: dichiarato (regime_del_passo.txt, 99eb7a42); il controllo positivo a s %g" % (S_CORSA, S_RIF))
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    s_vero = VC.S
    try:
        rec0, e_K0, inc0, _m0, _s0 = prepara(S_RIF)
        print("  s %g: il risolutore: larghezza %.4f, mu %.6f, fattore %.4f; e_K(0) %+.6f" % (S_RIF, rec0["larghezza"], rec0["mu"], rec0["fattore"], e_K0))
        r0 = corsa(rec0, e_K0, np.full(2 * inc0.m, SL.VUOTO_PER_ESTREMITA, dtype=complex), "intero", S_RIF)
        print("### il CONTROLLO POSITIVO a s %g, il vuoto uniforme, il tick intero: vita %s (ogni 20: %s); dM %.1e dV %.1e (%.0f s)" % (S_RIF, r0["vita"], r0["vita20"], r0["dM"], r0["dV"], r0["secondi"]))
        scrivi({"tipo": "controllo", "s": S_RIF, "vita": r0["vita"], "vita20": r0["vita20"], "dM": r0["dM"], "dV": r0["dV"]})
        rec, e_K, inc, mot, st = prepara(S_CORSA)
        sc = N * abs(e_K)
        print("  s %g: il risolutore: larghezza %.4f, mu %.6f, fattore %.4f; e_K(0) %+.6f; l'unita' N |e_K(0)| = %.6e" % (S_CORSA, rec["larghezza"], rec["mu"], rec["fattore"], e_K, sc))
        f0_ref, _d = VSF.fondo_uniforme(inc, L_TORO, SL.VUOTO_PER_ESTREMITA)
        vuoti = {nome: fondo_con_fasi(inc, L_TORO, f) for nome, f in FASI}
        esito("DEVE PASSARE (k0): il flusso F0 = _vuoto_sul_fondo.fondo_uniforme AL BIT", vuoti["F0"].tobytes() == f0_ref.tobytes(), "")
        ok1, n1 = True, []
        for nome, ph in vuoti.items():
            s_ = dict(st)
            s_["psi_h"] = np.zeros_like(st["psi_h"])
            s_["phi_h"] = ph
            e = VSF.energia(mot, s_, "phi_h", "tutto") / float(np.sum(np.abs(ph) ** 2))
            ok1 &= abs(e + 2 * math.pi) <= TOLL_FONDO
            n1.append("%s %.12f" % (nome, e))
        esito("DEVE PASSARE (k1): ogni vuoto del fondo ha E/V = -2 pi entro %g" % TOLL_FONDO, ok1, "; ".join(n1))
        print("-" * 130)
        casi = [("uniforme", "intero", np.full(2 * inc.m, SL.VUOTO_PER_ESTREMITA, dtype=complex))]
        casi += [(nome, modo, vuoti[nome]) for nome, _f in FASI for modo in MODI]
        ris = {}
        for nome, modo, ph in casi:
            r = corsa(rec, e_K, ph, modo, S_CORSA)
            ris[(nome, modo)] = r
            e0 = r["serie"][0]["E"]
            tv = r["vita20"] if r["vita20"] is not None else r["T_MAX"]
            ev = [x for x in r["serie"] if x["t"] == tv][0]["E"]
            ef = r["serie"][-1]["E"]
            g = np.array([x[1] for x in r["gA"]])
            tt = np.array([x[0] for x in r["gA"]])
            pr, do = tt <= tv, tt > tv
            A = {"entrate_vita": float(g[pr & (g > 0)].sum()) / sc, "uscite_vita": float(g[pr & (g < 0)].sum()) / sc,
                 "entrate_dopo": float(g[do & (g > 0)].sum()) / sc, "uscite_dopo": float(g[do & (g < 0)].sum()) / sc, "tick_entrata_dopo": int(np.sum(do & (g > 0))), "tick_dopo": int(do.sum())}
            print("### %-8s %-9s (L %d, w_in %.4f, %d tick): vita %s (ogni 20 di s 0.3: %s; tempo fisico %s); dM %.1e dV %.1e (%.0f s)"
                  % (nome, modo, r["L"], r["w_in"], r["T_MAX"], r["vita"], r["vita20"], "%.1f" % r["tau_vita"] if r["tau_vita"] is not None else "-", r["dM"], r["dV"], r["secondi"]))
            for t_, e_ in (("alla vita %d" % tv, ev), ("a T_MAX", ef)):
                for reg in ("totale", "vicino", "lontano"):
                    print("  %-15s %-8s: vuoto %+.4e  cinetica %+.4e  legame %+.4e  H_tot %+.4e" % (t_, reg, e_[reg]["vuo"] - e0[reg]["vuo"], e_[reg]["cin"] - e0[reg]["cin"], e_[reg]["leg"] - e0[reg]["leg"], e_[reg]["tot"] - e0[reg]["tot"]))
            print("  la strada A sul disco 2 w_in (N |e_K(0)|): fino alla vita entrate %+.4e uscite %+.4e; dopo entrate %+.4e uscite %+.4e (%d tick in entrata su %d)"
                  % (A["entrate_vita"], A["uscite_vita"], A["entrate_dopo"], A["uscite_dopo"], A["tick_entrata_dopo"], A["tick_dopo"]))
            sys.stdout.flush()
            scrivi({"tipo": "corsa", "vuoto": nome, "modo": modo, "s": S_CORSA, "L": r["L"], "w_in": r["w_in"], "vita": r["vita"], "vita20": r["vita20"], "tau_vita": r["tau_vita"],
                    "dM": r["dM"], "dV": r["dV"], "strada_A": A, "serie": r["serie"], "secondi": r["secondi"]})
    finally:
        VC.S = s_vero
    print("-" * 130)
    print("### I CRITERI")
    tutte = list(ris.values()) + [r0]
    esito("DEVE PASSARE (k2): M e V entro %g in ogni corsa" % TOLL_NORMA, all(r["dM"] <= TOLL_NORMA and r["dV"] <= TOLL_NORMA for r in tutte),
          "dM max %.1e dV max %.1e" % (max(r["dM"] for r in tutte), max(r["dV"] for r in tutte)))
    esito("DEVE PASSARE (k3): il controllo positivo a s %g: col vuoto uniforme la vita (ogni 20) = %d di 15df5c63" % (S_RIF, VITA_RIF), r0["vita20"] == VITA_RIF, "vita20 %s" % r0["vita20"])
    ru = ris[("uniforme", "intero")]
    soglia = FATTORE_P1 * ru["tau_vita"] if ru["tau_vita"] is not None else None
    p1, n_p1, p2, n_p2 = True, [], True, []
    for nome, _f in FASI:
        r = ris[(nome, "intero")]
        tvv = r["tau_vita"]
        p1 &= soglia is not None and (tvv is None or tvv > soglia)
        n_p1.append("%s %s" % (nome, "%.1f" % tvv if tvv is not None else "oltre %g" % TAU))
        tv = r["vita20"] if r["vita20"] is not None else r["T_MAX"]
        dv = [x for x in r["serie"] if x["t"] == tv][0]["E"]["totale"]["vuo"] - r["serie"][0]["E"]["totale"]["vuo"]
        p2 &= dv > 0
        n_p2.append("%s %+.3e" % (nome, dv))
    esito("PUO' FALLIRE (p1): col fondo e il tick intero la vita (tempo fisico) oltre %g volte quella col vuoto uniforme a s %g (%s), a ogni fase" % (FATTORE_P1, S_CORSA, "%.1f" % ru["tau_vita"] if ru["tau_vita"] is not None else "-"),
          p1, "; ".join(n_p1), deve=False)
    esito("PUO' FALLIRE (p2): il vuoto PRENDE energia dalla materia (Delta E_vuoto > 0 sul toro alla vita, a ogni fase)", p2, "; ".join(n_p2), deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
