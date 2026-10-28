# -*- coding: utf-8 -*-
r"""**IL SOLITONE CON LA SUA BUCA: LA RAMPA DEL VUOTO** *(il mandato di Luca delle `22:59` del `2026-10-27`, parte `1`; [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]],
[[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-10-28_solitone_con_la_buca.md`)*: ### **dallo stato di `76eecbf5` col vuoto congelato, i pezzi del vuoto
e la rotazione gemella del legame sul vuoto si accendono con `r(t) = sin^2(pi t / (2 T_r))`, poi il tick intero.** ### **Le scene: il fondo `F0` e il vuoto uniforme; `S1`, lo zero
simmetrico, `cs` spento, `s 0.075`; le taglie `N 1e6 L 81` e `N 1e5 L 48`.**
### **L'AGGIUNTA DI LUCA DELLE `09:58`: la rampa PRINCIPALE e' la tanh `r = 1/2 [1 + tanh((t - t0)/tau)]`, `tau = T_r/10`, `r(0) = 1e-8`, il tick intero da `r > 1 - 1e-8`;**
### **il `sin^2` resta come CONFRONTO agli stessi `T_r`; per entrambe l'energia iniettata dalla rampa.**

> ### **In memoria; nessun file del nucleo.** ### ⛔ **LA RAMPA E' UNO STRUMENTO DI PREPARAZIONE DELLO STATO, NON UNA LEGGE** *(il mandato)*.
> ### ⚠ **`tick_rampa` E' UN SECONDO PERCORSO DEL TICK** *(il difetto per cui `tick.py` esiste)*: ### **si accetta solo col controllo `(k0)`:** ### **a `r = 1` da' lo
> stato di `tick.percorri_tick` AL BIT.** ### **A `r = 0` un pezzo del vuoto si SALTA:** ### **`_frazione_valida` vieta la frazione `0`, e a `theta = 0` il pezzo e' l'identita'.**

Le corse si fanno a pezzi, una per invocazione, e ognuna appende la sua riga al jsonl:
    python csv/_solitone_con_la_buca.py --controlli
    python csv/_solitone_con_la_buca.py --corsa <grande|piccola> <fondo|uniforme> <congelato|zero|tanh25|tanh100|tanh400|sin225|sin2100|sin2400>
Il referto, dalle righe del jsonl:
    python csv/_solitone_con_la_buca.py --referto > doc/referti_l2/solitone_con_la_buca.txt
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

PARTI = os.path.join(RADICE, "doc", "referti_l2", "solitone_con_la_buca")   # ### il jsonl, una riga per file
OGNI_E = 4                     # ### i conti per regione ogni 4 controlli della forma (e a t = 0, alla fine della rampa, a T_MAX): il peso del jsonl
RIF_76 = os.path.join(RADICE, "doc", "referti_l2", "solitone_dal_fondo.jsonl")
TAGLIE = {"grande": (1e6, 81), "piccola": (1e5, 48)}    # ### la seconda: la coppia di solitone_vuoto_congelato.txt
SCENE = ("fondo", "uniforme")
T_RAMPE = (25.0, 100.0, 400.0)  # ### il mandato, in tempo fisico
FORME = ("tanh", "sin2")       # ### la tanh e' la principale, il sin^2 il confronto (Luca, 2026-10-28 09:58)
R_CAPI = 1e-8                  # ### la tanh: r(0) = 1e-8, e il tick intero quando r supera 1 - 1e-8 (Luca, 09:58)
MODI_RAMPA = tuple("%s%g" % (f, T) for f in FORME for T in T_RAMPE)
ZERO = "simm"
LAM_ZERO = 0.5
S_CORSA = 0.075
TAU_DOPO = 800.0               # ### il tempo fisico dopo la rampa (il mandato: almeno 800)
TAU_RIF = 600.0                # ### l'orizzonte del congelato di 76eecbf5, e di r = 0
OGNI_TAU = 3.0                 # ### i conti e la forma ogni 3 di tempo fisico (come 76eecbf5)
R_VICINO = 2.0
R_CENTRO = 0.5                 # ### il centro della buca: r <= w_in / 2
TICK_K0 = 20
PEZZI_VUOTO = ("CAMM-GROVER-VUOTO", "CAMM-SPOSTAMENTO-VUOTO", "CAMM-FASE-VUOTO")
TOLL_NORMA = 1e-10
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


def scrivi(r, nome):
    """### **Una corsa, un file di una riga** *(le corse girano in parallelo e a pezzi: nessuno scrive nel file di un altro)*; ### **un file che c'e' gia' NON si riscrive.**"""
    os.makedirs(PARTI, exist_ok=True)
    p = os.path.join(PARTI, nome + ".jsonl")
    assert not os.path.exists(p), ("la corsa c'e' gia'", p)
    dati = (json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    with open(p, "xb") as f:
        f.write(dati)


def righe():
    if not os.path.isdir(PARTI):
        return []
    return [json.loads(io.open(os.path.join(PARTI, n), encoding="utf-8").read()) for n in sorted(os.listdir(PARTI)) if n.endswith(".jsonl")]


def t0_tanh(T_r):
    """### `t0` della tanh: ### **`r(0) = R_CAPI`, cioe' `t0 = tau atanh(1 - 2 R_CAPI)`, `tau = T_r / 10`** *(Luca, `09:58`)*."""
    return (T_r / 10.0) * math.atanh(1.0 - 2.0 * R_CAPI)


def rampa(t, forma, T_r, s):
    """### `r` al CENTRO del tick `t`.

    ### **`tanh`** *(la principale, Luca `09:58`)*: ### **`1/2 [1 + tanh((t_c - t0)/tau)]`, e `1` dal primo tick in cui supera `1 - R_CAPI`.**
    ### **`sin2`** *(il confronto)*: ### **`sin^2(pi t_c / (2 T_r))` per `t_c < T_r`, poi `1`.**
    """
    tc = (t + 0.5) * s
    if forma == "tanh":
        r = 0.5 * (1.0 + math.tanh((tc - t0_tanh(T_r)) / (T_r / 10.0)))
        return 1.0 if r > 1.0 - R_CAPI else r
    assert forma == "sin2", forma
    if tc >= T_r:
        return 1.0
    return math.sin(math.pi * tc / (2.0 * T_r)) ** 2


def materia_vuoto_rampa(mot, st, frazione, r):
    """### **Le righe di `materia_vuoto.applica`, con la fase `beta` su `phi` per la frazione per `r`** *(la rotazione gemella del legame sul vuoto)*; ### **`alpha` su `psi` intera.**"""
    import flussi_parziali as FP
    import materia_vuoto as MV
    rho = mot.densita_materia(st)
    lam = mot.densita_vuoto(st)
    al, be = MV.pezzi(rho, lam)
    nodo = mot.inc.nodo
    f = float(frazione)
    dtau = FP.dtau_nodo(mot)
    fas = mot._b("mv_fas", (st["psi_h"].shape[0],), float)
    esp = mot._b("mv_esp", fas.shape, st["phi_h"].dtype)
    np.take(al * dtau * f, nodo, out=fas)
    np.multiply(fas, -1j, out=esp)
    np.exp(esp, out=esp)
    np.multiply(st["psi_h"], esp.reshape(-1, 1), out=st["psi_h"])
    if r > 0.0:
        np.take(be * dtau * (f * r), nodo, out=fas)
        np.multiply(fas, -1j, out=esp)
        np.exp(esp, out=esp)
        np.multiply(st["phi_h"], esp, out=st["phi_h"])
    mot.applicazioni["CAMM-MATERIA-VUOTO"] += 1
    return st


def tick_rampa(st, mot, par, r):
    """### **Il tick nell'ordine della tabella, coi pezzi del vuoto a frazione per `r`** *(saltati a `r = 0`)*."""
    import composizione as CM
    import tick as TK
    mot.apri_tick()
    for idl, frazione, _tipo in CM.ORDINE:
        nome, vuole_par = TK.OPERATORE[idl]
        if idl == "CAMM-MATERIA-VUOTO":
            materia_vuoto_rampa(mot, st, frazione, r)
        elif idl in PEZZI_VUOTO:
            if r > 0.0:
                mot.operatori[nome](st, par if vuole_par else {}, frazione * r)
        else:
            mot.operatori[nome](st, par if vuole_par else {}, frazione)
    mot.chiudi_tick()


def prepara(taglia):
    """### **Il risolutore a `S_CORSA` e la scena della taglia** *(le righe di `_solitone_dal_fondo.prepara`, con `N` e `L` della taglia)*."""
    import _energia_del_legame as EL
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    N, L_toro = TAGLIE[taglia]
    VC.S = S_CORSA
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(S_CORSA)
        ls = MPS.largo(VC.FORMA, cc, S_CORSA, N)
    finally:
        MPS.LAM0 = vero
    rec = {"larghezza": ls["larghezza"], "c": cc, "mu": ls["mu"], "fattore": (L_toro - 0.1) / ls["larghezza"]}
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, rec["fattore"], rec)
    assert L == L_toro, (taglia, L, L_toro)
    incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
    Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
    return rec, Eu / Mu


def vuoto_iniziale(scena, inc, L):
    import _solitone_dal_fondo as SDF
    import scena_l2 as SL
    if scena == "fondo":
        return SDF.fondo_con_fasi(inc, L, SDF.FASI[0][1])
    assert scena == "uniforme", scena
    return np.full(2 * inc.m, SL.VUOTO_PER_ESTREMITA, dtype=complex)


def corsa(taglia, scena, modo):
    """### **Una corsa:** `modo` e' `congelato` *(il tick intero e `phi` rimesso a `phi0` a fine tick, come `76eecbf5`)*, `zero` *(`r = 0` per sempre)*, o `T_r`."""
    import _energia_del_legame as EL
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    N, _L = TAGLIE[taglia]
    rec, e_K = prepara(taglia)
    s = S_CORSA
    if modo in ("congelato", "zero"):
        forma_r, T_r, t_rampa, T_MAX = None, None, 0, int(round(TAU_RIF / s))
    else:
        assert modo in MODI_RAMPA, modo
        forma_r = "tanh" if modo.startswith("tanh") else "sin2"
        T_r = float(modo[len(forma_r):])
        t_rampa = next(t for t in range(10 ** 7) if rampa(t, forma_r, T_r, s) == 1.0)
        T_MAX = t_rampa + int(round(TAU_DOPO / s))
    OGNI = int(round(OGNI_TAU / s))
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, rec["fattore"], rec)
    st["phi_h"][...] = vuoto_iniziale(scena, inc, L)
    phi0 = st["phi_h"].copy()
    w0 = rec["larghezza"]
    grado = inc.grado.astype(float)

    def forma_m():
        rho, lam = EL.densita(inc, st)
        M = float(rho.sum())
        c = (rho @ pos) / M
        w2 = float(rho @ np.sum((pos - c) ** 2, axis=1)) / M
        fr = float(rho[np.hypot(pos[:, 0] - c[0], pos[:, 1] - c[1]) <= STR.RAGGIO_FRAZ * w0].sum()) / M
        return math.sqrt(w2), fr, float(rho.max()), lam / grado
    w_in, _f, _p, _l = forma_m()
    vic = rr <= R_VICINO * w_in
    cen = rr <= R_CENTRO * w_in
    bor = (rr > w_in) & vic
    mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(inc.n, dtype=bool)}

    def buca(le):
        lc, lb, ll = float(le[cen].mean()), float(le[bor].mean()), float(le[~vic].mean())
        # ### la larghezza col secondo momento di |deficit|: CAMBIATA DOPO LA PROVA (la tanh25 a N 1e5 ha dato una GOBBA, deficit negativo; annotato nel task history)
        d = ll - le[vic]
        sd = math.fsum(d.tolist())
        sa = math.fsum(np.abs(d).tolist())
        w = math.sqrt(math.fsum((np.abs(d) * rr[vic] ** 2).tolist()) / sa) if sa > 0 else None
        return {"centro": lc, "bordo": lb, "lontano": ll, "profondita": 1.0 - lc / ll, "deficit": sd, "larghezza": w}
    serie, gA = [], []
    vita, rotta_in_rampa = None, None
    prec_d2 = None
    phi_fermo = True
    t0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(ZERO):
        for t in range(T_MAX + 1):
            c = LC.conti_per_nodo(inc, mot, st, e_K, LAM_ZERO)
            d2 = math.fsum(c["tot"][vic].tolist())
            if prec_d2 is not None:
                gA.append((t, d2 - prec_d2))
            prec_d2 = d2
            if t % OGNI == 0 or t in (t_rampa, T_MAX):
                w, fr, pk, le = forma_m()
                rotto = abs(w / w_in - 1.0) > STR.TOLL_LARGH or fr < STR.FRAZ_MIN
                if rotto and t < t_rampa and rotta_in_rampa is None:
                    rotta_in_rampa = t
                if rotto and t >= t_rampa and vita is None:
                    vita = t - t_rampa
                x = {"t": t, "larghezza": w, "frazione": fr, "picco": pk, "buca": buca(le), "M": math.fsum(c["M"].tolist()), "V": math.fsum(c["V"].tolist())}
                if t % (OGNI * OGNI_E) == 0 or t in (t_rampa, T_MAX):
                    x["E"] = LC.per_regione(c, mas)
                serie.append(x)
            if t < T_MAX:
                if modo == "congelato":
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                    st["phi_h"][...] = phi0
                elif modo == "zero":
                    tick_rampa(st, mot, par, 0.0)
                    phi_fermo &= st["phi_h"].tobytes() == phi0.tobytes()
                else:
                    tick_rampa(st, mot, par, rampa(t, forma_r, T_r, s))
    dM = max(abs(x["M"] - serie[0]["M"]) / serie[0]["M"] for x in serie)
    dV = max(abs(x["V"] - serie[0]["V"]) / serie[0]["V"] for x in serie)
    sc = N * abs(e_K)
    g = np.array([x[1] for x in gA])
    tt = np.array([x[0] for x in gA])
    pr, do = tt <= t_rampa, tt > t_rampa
    A = {"entrate_rampa": float(g[pr & (g > 0)].sum()) / sc, "uscite_rampa": float(g[pr & (g < 0)].sum()) / sc,
         "entrate_dopo": float(g[do & (g > 0)].sum()) / sc, "uscite_dopo": float(g[do & (g < 0)].sum()) / sc, "tick_entrata_dopo": int(np.sum(do & (g > 0))), "tick_dopo": int(do.sum())}
    # ### L'ENERGIA INIETTATA DALLA RAMPA (Luca, 09:58): i conti del libro alla fine della rampa meno quelli a t = 0, in N |e_K(0)|
    er = [x for x in serie if x["t"] == t_rampa][0]["E"]
    iniettata = {reg: {k: (er[reg][k] - serie[0]["E"][reg][k]) / sc for k in ("vuo", "cin", "leg", "tot")} for reg in mas}
    return {"taglia": taglia, "N": N, "L": L, "scena": scena, "modo": modo, "forma": forma_r, "T_r": T_r, "t0": t0_tanh(T_r) if forma_r == "tanh" else None,
            "t_rampa": t_rampa, "iniettata": iniettata, "T_MAX": T_MAX, "s": s, "w0": w0, "mu": rec["mu"], "e_K": e_K,
            "w_in": w_in, "vita_dopo_rampa": vita, "tau_vita_dopo_rampa": vita * s if vita is not None else None, "rotta_in_rampa": rotta_in_rampa,
            "phi_fermo": phi_fermo if modo == "zero" else None, "dM": dM, "dV": dV, "strada_A": A, "serie": serie, "secondi": time.time() - t0}


def k0(taglia):
    """### **`(k0)`: il tick con la rampa a `r = 1` contro `tick.percorri_tick`, `TICK_K0` tick dal fondo: i byte di `psi` e `phi`.**"""
    import _energia_del_legame as EL
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    N, _L = TAGLIE[taglia]
    rec, _e = prepara(taglia)
    stati = []
    for via in ("nucleo", "rampa"):
        L, inc, mot, st, par, *_r = EL.stato(N, rec["fattore"], rec)
        st["phi_h"][...] = vuoto_iniziale("fondo", inc, L)
        with SF.forma(VC.FORMA), BE.conv(ZERO):
            for _t in range(TICK_K0):
                if via == "nucleo":
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                else:
                    tick_rampa(st, mot, par, 1.0)
        stati.append((st["psi_h"].tobytes(), st["phi_h"].tobytes()))
    return stati[0] == stati[1]


def testata():
    import _universalita_massa as UM
    import composizione as CM
    blobs = {p: UM.blob(p)["sha1-BYTE"] for p in ("soliton_simulator.py", "csv/_solitone_con_la_buca.py", "csv/_solitone_dal_fondo.py", "csv/_energia_del_legame.py",
                                                  "csv/_libro_dei_conti.py", "primo_ordine/tick.py", "primo_ordine/materia_vuoto.py", "primo_ordine/flussi_parziali.py")}
    return {"blobs": blobs, "impronta": CM.IMPRONTA, "pezzi": len(CM.ORDINE)}


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    s_vero = VC.S
    try:
        if argv[:1] == ["--controlli"]:
            esiti = {t: k0(t) for t in TAGLIE}
            print("  (k0) il tick con la rampa a r = 1 = tick.percorri_tick al bit (%d tick, dal fondo): %s" % (TICK_K0, esiti))
            scrivi({"tipo": "k0", "esiti": esiti, "testata": testata()}, "k0")
        elif argv[:1] == ["--corsa"]:
            taglia, scena, modo = argv[1], argv[2], argv[3]
            assert taglia in TAGLIE and scena in SCENE and modo in ("congelato", "zero") + MODI_RAMPA, argv
            nome = "%s_%s_%s" % (taglia, scena, modo)
            assert not os.path.exists(os.path.join(PARTI, nome + ".jsonl")), ("la corsa c'e' gia'", argv)
            r = corsa(taglia, scena, modo)
            r.update({"tipo": "corsa", "testata": testata()})
            print("  %s %s %s: L %d, w_in %.4f, %d tick (rampa %d): vita dopo la rampa %s, rotta in rampa %s; dM %.1e dV %.1e (%.0f s)"
                  % (taglia, scena, modo, r["L"], r["w_in"], r["T_MAX"], r["t_rampa"], r["vita_dopo_rampa"], r["rotta_in_rampa"], r["dM"], r["dV"], r["secondi"]))
            scrivi(r, nome)
        elif argv[:1] == ["--prova"]:
            taglia, scena, modo, quanti = argv[1], argv[2], argv[3], int(argv[4])
            global TAU_DOPO, TAU_RIF
            TAU_DOPO = TAU_RIF = quanti * S_CORSA
            r = corsa(taglia, scena, modo)
            print("  PROVA (non nel jsonl) %s %s %s: %d tick (rampa %d), dM %.1e dV %.1e, %.2f s per tick; l'ultima buca %s"
                  % (taglia, scena, modo, r["T_MAX"], r["t_rampa"], r["dM"], r["dV"], r["secondi"] / max(r["T_MAX"], 1), r["serie"][-1]["buca"]))
        elif argv[:1] == ["--referto"]:
            referto()
        else:
            raise SystemExit(__doc__)
    finally:
        VC.S = s_vero
    return 0


def referto():
    import _solitoni_triangoli as STR
    tutte = righe()
    corse = {(x["taglia"], x["scena"], x["modo"]): x for x in tutte if x.get("tipo") == "corsa"}
    k0r = [x for x in tutte if x.get("tipo") == "k0"]
    attese = [(t, "fondo", m) for t in TAGLIE for m in ("congelato", "zero")] + [(t, sc, m) for t in TAGLIE for sc in SCENE for m in MODI_RAMPA]
    print("=" * 130)
    print("IL SOLITONE CON LA SUA BUCA: la rampa del vuoto, la PRINCIPALE r(t) = 1/2 [1 + tanh((t - t0)/tau)] (Luca 09:58), il CONFRONTO r(t) = sin^2(pi t / (2 T_r)) agli stessi T_r,"
          " poi il tick intero; il fondo F0 e il vuoto uniforme; S1, zero simmetrico, cs spento, s %g" % S_CORSA)
    print("=" * 130)
    print("  la configurazione: TAGLIE %s SCENE %s T_RAMPE %s ZERO %s LAM_ZERO %g S_CORSA %g TAU_DOPO %g TAU_RIF %g OGNI_TAU %g R_VICINO %g R_CENTRO %g TICK_K0 %d PEZZI_VUOTO %s TOLL_NORMA %g;"
          " la vita: TOLL_LARGH %g FRAZ_MIN %g RAGGIO_FRAZ %g (_solitoni_triangoli); FORMA S1; cs spento"
          % (TAGLIE, SCENE, T_RAMPE, ZERO, LAM_ZERO, S_CORSA, TAU_DOPO, TAU_RIF, OGNI_TAU, R_VICINO, R_CENTRO, TICK_K0, PEZZI_VUOTO, TOLL_NORMA, STR.TOLL_LARGH, STR.FRAZ_MIN, STR.RAGGIO_FRAZ))
    print("  le forme %s (la tanh la principale, il sin^2 il confronto; Luca 09:58); R_CAPI %g; la tanh: tau = T_r/10, t0 = tau atanh(1 - 2 R_CAPI): %s"
          % (FORME, R_CAPI, "; ".join("T_r %g: tau %g t0 %.6f r(0) %.3e" % (T, T / 10.0, t0_tanh(T), 0.5 * (1.0 + math.tanh(-t0_tanh(T) / (T / 10.0)))) for T in T_RAMPE)))
    testate = {json.dumps(x["testata"], sort_keys=True) for x in tutte if "testata" in x}
    print("  le testate delle righe (blob sha1-BYTE, impronta): %d distinte" % len(testate))
    for t_ in sorted(testate):
        print("    %s" % t_)
    manca = [a for a in attese if a not in corse]
    print("  le corse: %d su %d; mancano %s" % (len(attese) - len(manca), len(attese), manca))
    print("-" * 130)
    for a in attese:
        r = corse.get(a)
        if r is None:
            continue
        print("### %-7s %-8s %-9s (N %g L %d, w_in %.4f, %d tick, rampa %d): vita dopo la rampa %s (tempo fisico %s); rotta in rampa %s; dM %.1e dV %.1e (%.0f s)"
              % (r["taglia"], r["scena"], r["modo"], r["N"], r["L"], r["w_in"], r["T_MAX"], r["t_rampa"], r["vita_dopo_rampa"],
                 "%.1f" % r["tau_vita_dopo_rampa"] if r["tau_vita_dopo_rampa"] is not None else "oltre", r["rotta_in_rampa"], r["dM"], r["dV"], r["secondi"]))
        e0 = r["serie"][0]
        for x in r["serie"]:
            if x["t"] in (0, r["t_rampa"], r["T_MAX"]) or x is r["serie"][len(r["serie"]) // 2]:
                b = x["buca"]
                print("  t %6d: larghezza/w_in %.4f picco %.4e frazione %.4f; la buca: centro %.6f bordo %.6f lontano %.6f profondita %+.3e larghezza %s"
                      % (x["t"], x["larghezza"] / r["w_in"], x["picco"], x["frazione"], b["centro"], b["bordo"], b["lontano"], b["profondita"],
                         "%.3f" % b["larghezza"] if b["larghezza"] is not None else "-"))
        ef = r["serie"][-1]["E"]
        for reg in ("totale", "vicino", "lontano"):
            print("  a T_MAX  %-8s: vuoto %+.4e  cinetica %+.4e  legame %+.4e  H_tot %+.4e" % (reg, ef[reg]["vuo"] - e0["E"][reg]["vuo"], ef[reg]["cin"] - e0["E"][reg]["cin"],
                                                                                              ef[reg]["leg"] - e0["E"][reg]["leg"], ef[reg]["tot"] - e0["E"][reg]["tot"]))
        if r["forma"] is not None:
            for reg in ("totale", "vicino", "lontano"):
                i_ = r["iniettata"][reg]
                print("  l'energia iniettata dalla rampa (N |e_K(0)|) %-8s: vuoto %+.4e  cinetica %+.4e  legame %+.4e  H_tot %+.4e" % (reg, i_["vuo"], i_["cin"], i_["leg"], i_["tot"]))
        A = r["strada_A"]
        print("  la strada A sul disco 2 w_in (N |e_K(0)|): in rampa entrate %+.4e uscite %+.4e; dopo entrate %+.4e uscite %+.4e (%d tick in entrata su %d)"
              % (A["entrate_rampa"], A["uscite_rampa"], A["entrate_dopo"], A["uscite_dopo"], A["tick_entrata_dopo"], A["tick_dopo"]))
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (k0): il tick con la rampa a r = 1 = tick.percorri_tick AL BIT (%d tick, dal fondo, le due taglie)" % TICK_K0,
          bool(k0r) and all(all(x["esiti"].values()) for x in k0r), "%s" % [x["esiti"] for x in k0r])
    g = corse.get(("grande", "fondo", "congelato"))
    rif = [x for x in (json.loads(y) for y in io.open(RIF_76, encoding="utf-8").read().split("\n") if y.strip()) if x.get("tipo") == "corsa" and x["vuoto"] == "F0" and x["modo"] == "congelato"]
    ok1 = g is not None and len(rif) == 1 and [x["larghezza"] for x in g["serie"] if x["t"] % 40 == 0] == [x["larghezza"] for x in rif[0]["serie"]]
    esito("DEVE PASSARE (k1): il congelato di 76eecbf5 ridato AL BIT (la serie delle larghezze di F0 congelato, N 1e6)", ok1, "")
    presenti = [corse[a] for a in attese if a in corse]
    esito("DEVE PASSARE (d1): M e V entro %g in ogni corsa" % TOLL_NORMA, bool(presenti) and all(r["dM"] <= TOLL_NORMA and r["dV"] <= TOLL_NORMA for r in presenti),
          "dM max %.1e dV max %.1e" % (max(r["dM"] for r in presenti), max(r["dV"] for r in presenti)) if presenti else "")
    ok2, n2 = True, []
    for t in TAGLIE:
        z, c = corse.get((t, "fondo", "zero")), corse.get((t, "fondo", "congelato"))
        if z is None or c is None:
            ok2 = False
            continue
        ok2 &= bool(z["phi_fermo"]) and ((c["vita_dopo_rampa"] is not None) or (z["vita_dopo_rampa"] is None))
        dw = max(abs(a["larghezza"] - b["larghezza"]) / b["larghezza"] for a, b in zip(z["serie"], c["serie"]))
        n2.append("%s: phi fermo %s, vita zero %s congelato %s; la distanza massima delle larghezze %.2e (lettura)" % (t, z["phi_fermo"], z["vita_dopo_rampa"], c["vita_dopo_rampa"], dw))
    esito("DEVE PASSARE (d2): con r = 0 per sempre lo stato resta quello del congelato (phi fermo al bit; non si rompe se il congelato non si rompe)", ok2, "; ".join(n2))
    p1, n1 = True, []
    for t in TAGLIE:
        r = corse.get((t, "fondo", "tanh400"))
        if r is None:
            p1 = False
            continue
        dopo = [x for x in r["serie"] if x["t"] >= r["t_rampa"]]
        dmax = max(abs(x["larghezza"] / r["w_in"] - 1.0) for x in dopo)
        p1 &= dmax <= STR.TOLL_LARGH
        n1.append("%s: scarto massimo %.3f" % (t, dmax))
    esito("PUO' FALLIRE (p1): col fondo e la tanh a T_r 400 la larghezza entro il 20%% di quella iniziale per gli %g dopo la rampa, alle due taglie" % TAU_DOPO, p1, "; ".join(n1), deve=False)

    def chiave(v):
        return float("inf") if v is None else v
    p2, n2 = True, []
    for t in TAGLIE:
        v = [corse.get((t, "fondo", "tanh%g" % T)) for T in T_RAMPE]
        if None in v:
            p2 = False
            continue
        k = [chiave(x["vita_dopo_rampa"]) for x in v]
        p2 &= all(a <= b for a, b in zip(k, k[1:])) and k[-1] > k[0]
        n2.append("%s: %s" % (t, [x["vita_dopo_rampa"] for x in v]))
    esito("PUO' FALLIRE (p2): col fondo e la tanh la vita dopo la rampa non decresce con T_r e a 400 supera quella a 25, alle due taglie", p2, "; ".join(n2), deve=False)
    print("-" * 130)
    print("### LA LETTURA DI LUCA (09:58): la tanh contro il sin^2, agli stessi T_r -- la vita dopo la rampa e l'energia iniettata (H_tot sul toro, N |e_K(0)|)")
    for t in TAGLIE:
        for sc in SCENE:
            for T in T_RAMPE:
                a, b = corse.get((t, sc, "tanh%g" % T)), corse.get((t, sc, "sin2%g" % T))
                if a is None or b is None:
                    continue
                print("  %-7s %-8s T_r %3g: vita tanh %s sin2 %s; iniettata tanh %+.4e sin2 %+.4e"
                      % (t, sc, T, a["vita_dopo_rampa"], b["vita_dopo_rampa"], a["iniettata"]["totale"]["tot"], b["iniettata"]["totale"]["tot"]))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
