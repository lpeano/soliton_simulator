# -*- coding: utf-8 -*-
r"""**IL SOLITONE COL VUOTO CONGELATO** *(la parte 1 del mandato del 2026-10-27; [[SOLITONI-TRIANGOLI]], [[PROGETTO-MASSA-COLLETTIVA]])*: ### **il solitone `S1` di `bcbd1f40` col tick intero, col vuoto congelato
e senza legame, con lo zero di oggi e con lo zero simmetrico: e' la risposta del vuoto a disfarlo?**

> ### ⛔ **Il task history e' `2026-10-27_solitone_vuoto_congelato.md`.** ### **In memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_solitoni_triangoli` *(`c_triangoli`, `profilo_u`, le costanti)*, `_modi_pi_e_solitoni.largo`, `_triangoli_bassa_energia.conv`, `_screening_forme_s3.forma`, `_triangoli_forza.coppia_K`,
> `scena_l2.scena_toro`, `tick.percorri_tick`. ### **La corsa e' quella di `_solitoni_triangoli.dinamica`, con DUE parametri in piu'** *(il modo e lo zero)* ### **e la risposta del vuoto.**

Gira con:  python csv/_solitone_vuoto_congelato.py > doc/referti_l2/solitone_vuoto_congelato.txt
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

FORMA = "S1"
S = 0.3
CASI = ((1e6, (12.0, 18.0)), (1e5, (12.0, 18.0)))
VITA_RIF = {1e6: 320, 1e5: 140}
ROT_RIF = -1.101
MODI = ("intero", "congelato", "senza_legame")
ZERI = ("oggi", "simm")
VUOTO = ("CAMM-GROVER-VUOTO", "CAMM-SPOSTAMENTO-VUOTO", "CAMM-FASE-VUOTO")
LEGAME = ("CAMM-MATERIA-VUOTO",)
TOLL_VITA = 0.20
TOLL_ROT = 1e-2
TOLL_NORMA = 1e-10
TOLL_ZERO = 1e-12
FATTORE_VITA = 4.0
L_ZERO = 12
T_ZERO = 50
T_PENDENZA = 200
JSONL = os.path.join(RADICE, "doc", "referti_l2", "solitone_vuoto_congelato.jsonl")
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


def salta_di(modo):
    return {"intero": (), "congelato": VUOTO, "senza_legame": LEGAME}[modo]


def controllo_zero():
    """### Vuoto e legame spenti, `s` uniforme, uno stato casuale: la densita' coi due zeri."""
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import scena_l2 as SL
    import tick as TK
    out = {}
    for z in ZERI:
        inc, mot, st, par = SL.scena_toro("triangoli", (L_ZERO, L_ZERO), 1.0, 0.1)
        mot.cs = np.full(inc.n, S)
        mot.lambda_c = None
        par = dict(par)
        par["eps"] = 0.0
        rng = np.random.default_rng(3)
        st["psi_h"][...] = rng.normal(size=st["psi_h"].shape) + 1j * rng.normal(size=st["psi_h"].shape)
        with BE.conv(z):
            for _ in range(T_ZERO):
                TK.percorri_tick(st, mot, par, VUOTO + LEGAME, None, len(CM.ORDINE))
        rho = np.zeros(inc.n)
        np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        out[z] = rho
    return float(np.max(np.abs(out["oggi"] - out["simm"])) / np.max(out["oggi"])), out["oggi"].tobytes() == out["simm"].tobytes()


def corsa(N, fattore, rec, modo, zero):
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _triangoli_bassa_energia as BE
    import _triangoli_forza as TF
    import composizione as CM
    import scena_l2 as SL
    import tick as TK
    w0 = rec["larghezza"]
    q, r, u = STR.profilo_u(FORMA, rec["c"], S, N, STR.LAM0_TRI, w0)
    L = int(3 * math.ceil(fattore * w0 / 3.0))
    inc, mot, st, par = SL.scena_toro("triangoli", (L, L), 1.0, 0.1)
    n = inc.n
    mot.cs = np.full(n, S)
    mot.lambda_c = None
    par = dict(par)
    par["eps"] = 0.0
    v = np.arange(n)
    m1, m2 = v // L, v % L
    d1 = (m1 - L // 2 + L // 2) % L - L // 2
    d2 = (m2 - L // 2 + L // 2) % L - L // 2
    pos = d1[:, None] * STR.A1 + d2[:, None] * STR.A2
    rr = np.hypot(pos[:, 0], pos[:, 1])
    g = np.interp(rr, r, u, right=0.0) * math.sqrt(STR.AREA_NODO)
    Q = TF.coppia_K(0.0, S)[0]["Q"][:, 0]
    cel = g[:, None] * Q[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
    cel *= math.sqrt(N / float(np.sum(np.abs(cel) ** 2)))
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    phi0 = st["phi_h"].copy()
    nodo = inc.nodo
    gr = np.bincount(nodo, minlength=n)
    i_c = int(np.argmin(rr))
    i_l = int(np.argmax(rr))

    def lam():
        x = np.zeros(n)
        np.add.at(x, nodo, np.abs(st["phi_h"]) ** 2)
        return x
    lam0 = lam()

    def misure():
        rho = np.zeros(n)
        np.add.at(rho, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        M = float(rho.sum())
        c = (rho @ pos) / M
        w2 = float(rho @ np.sum((pos - c) ** 2, axis=1)) / M
        fr = float(rho[np.hypot(pos[:, 0] - c[0], pos[:, 1] - c[1]) <= STR.RAGGIO_FRAZ * w0].sum()) / M
        la = lam()
        return {"M": M, "V": float(np.sum(np.abs(st["phi_h"]) ** 2)), "larghezza": math.sqrt(w2), "frazione": fr,
                "lam_centro": float(la[i_c] / gr[i_c]), "lam_lontano": float(la[i_l] / gr[i_l]), "lam_bit": la.tobytes() == lam0.tobytes()}

    def a_c():
        return complex(np.vdot(Q, st["psi_h"].reshape(n, 12)[i_c]))
    salta = salta_di(modo)
    serie, fasi = [], []
    m0 = misure()
    w_in = m0["larghezza"]
    vita = None
    t0 = time.time()
    with SF.forma(FORMA), BE.conv(zero):
        for t in range(STR.T_MAX + 1):
            if t % STR.OGNI == 0:
                mm = misure() if t else m0
                serie.append((t, mm))
                if vita is None and (abs(mm["larghezza"] / w_in - 1.0) > STR.TOLL_LARGH or mm["frazione"] < STR.FRAZ_MIN):
                    vita = t
            if t < STR.T_MAX:
                a0 = a_c()
                TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))
                if modo == "congelato":
                    st["phi_h"][...] = phi0
                a1 = a_c()
                if abs(a0) > 0 and abs(a1) > 0:
                    fasi.append(float(-np.angle(a1 / a0)))
    dM = max(abs(mm["M"] - m0["M"]) / m0["M"] for _t, mm in serie)
    dV = max(abs(mm["V"] - m0["V"]) / m0["V"] for _t, mm in serie)
    tt = np.array([t for t, _ in serie if t <= T_PENDENZA], dtype=float)
    lc = np.array([mm["lam_centro"] for t, mm in serie if t <= T_PENDENZA])
    fine = serie[-1][1]
    return {"tipo": "corsa", "N": N, "L": L, "fattore": fattore, "modo": modo, "zero": zero, "w_iniziale": w_in, "w_finale": fine["larghezza"], "frazione_finale": fine["frazione"],
            "vita": vita, "stabile": vita is None, "dM": dM, "dV": dV, "lam_bit": all(mm["lam_bit"] for _t, mm in serie),
            "rotazione": float(np.mean(fasi)) if fasi else None, "rotazione_dev": float(np.std(fasi)) if fasi else None,
            "lam_centro_0": m0["lam_centro"], "lam_centro_fine": fine["lam_centro"], "lam_lontano_fine": fine["lam_lontano"],
            "lam_pendenza": float(np.polyfit(tt, lc, 1)[0]) if len(tt) > 1 else None,
            "serie": [[t, mm["larghezza"], mm["frazione"], mm["lam_centro"], mm["lam_lontano"]] for t, mm in serie], "secondi": time.time() - t0}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _modi_pi_e_solitoni as MPS
    import _solitoni_triangoli as STR
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL SOLITONE COL VUOTO CONGELATO: S1 di bcbd1f40, il tick intero / il vuoto congelato / senza legame, lo zero di oggi e lo zero simmetrico")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_solitone_vuoto_congelato.py", "csv/_solitoni_triangoli.py", "csv/_zero_simmetrico.py", "csv/_screening_forme_s3.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: FORMA %s S %g CASI %s VITA_RIF %s ROT_RIF %g MODI %s ZERI %s VUOTO %s LEGAME %s TOLL_VITA %g TOLL_ROT %g TOLL_NORMA %g TOLL_ZERO %g FATTORE_VITA %g L_ZERO %d T_ZERO %d T_PENDENZA %d; da _solitoni_triangoli: LAM0_TRI %g T_MAX %d OGNI %d"
          % (FORMA, S, CASI, VITA_RIF, ROT_RIF, MODI, ZERI, VUOTO, LEGAME, TOLL_VITA, TOLL_ROT, TOLL_NORMA, TOLL_ZERO, FATTORE_VITA, L_ZERO, T_ZERO, T_PENDENZA, STR.LAM0_TRI, STR.T_MAX, STR.OGNI))
    print("  il vuoto congelato: saltati %s, e phi rimesso al valore dell'istante zero dopo ogni tick; senza legame: saltato %s" % (VUOTO, LEGAME))
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    rz, bz = controllo_zero()
    scrivi({"tipo": "controllo_zero", "scarto_relativo": rz, "al_bit": bz})
    esito("DEVE PASSARE (3): vuoto e legame spenti, s uniforme: la densita' coi due zeri entro %g relativo (al bit: %s)" % (TOLL_ZERO, bz), rz <= TOLL_ZERO, "%.2e" % rz)
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        c, cy, w0 = STR.c_triangoli(S)
        rec0 = {N: MPS.largo(FORMA, c, S, N) for N, _f in CASI}
    finally:
        MPS.LAM0 = vero
    ris = []
    for N, fattori in CASI:
        rec = {"larghezza": rec0[N]["larghezza"], "c": c, "w0": w0, "mu": rec0[N]["mu"]}
        print("### N %g: il risolutore %s, larghezza %.4f, mu %+.5f" % (N, rec0[N]["verdetto"], rec["larghezza"], rec["mu"]))
        for zero in ZERI:
            for modo in MODI:
                for fat in fattori:
                    d = corsa(N, fat, rec, modo, zero)
                    ris.append(d)
                    scrivi(d)
                    print("  N %-7g L %3d zero %-4s %-12s: larghezza %.3f -> %.3f, frazione %.3f; vita %s; dM %.1e dV %.1e%s; rotazione %+.6f; Lambda per estremita' al centro %.6f -> %.6f (pendenza %+.2e), lontano %.6f (%.0f s)"
                          % (N, d["L"], zero, modo, d["w_iniziale"], d["w_finale"], d["frazione_finale"], "STABILE fino a %d" % STR.T_MAX if d["stabile"] else "%d tick" % d["vita"],
                             d["dM"], d["dV"], "; Lambda al bit %s" % d["lam_bit"] if modo == "congelato" else "", d["rotazione"], d["lam_centro_0"], d["lam_centro_fine"],
                             d["lam_pendenza"] or 0.0, d["lam_lontano_fine"], d["secondi"]))
                    sys.stdout.flush()
    print("-" * 130)
    print("### I CRITERI")

    def trova(N, modo, zero):
        return [d for d in ris if d["N"] == N and d["modo"] == modo and d["zero"] == zero]
    ok1, n1 = True, []
    for N, _f in CASI:
        for d in trova(N, "intero", "oggi"):
            v_ok = d["vita"] is not None and abs(d["vita"] - VITA_RIF[N]) <= TOLL_VITA * VITA_RIF[N]
            r_ok = d["rotazione"] is not None and abs(d["rotazione"] - ROT_RIF) <= TOLL_ROT
            ok1 &= v_ok and r_ok
            n1.append("N %g L %d: vita %s, rot %+.4f" % (N, d["L"], d["vita"], d["rotazione"]))
    esito("DEVE PASSARE (1): (a) lo zero di oggi ridà la vita di bcbd1f40 entro il %g%% e la rotazione %g entro %g" % (100 * TOLL_VITA, ROT_RIF, TOLL_ROT), ok1, "; ".join(n1))
    ok2 = all(d["dM"] <= TOLL_NORMA and d["dV"] <= TOLL_NORMA for d in ris) and all(d["lam_bit"] for d in ris if d["modo"] == "congelato")
    esito("DEVE PASSARE (2): M e V entro %g in ogni corsa; Lambda al bit nel vuoto congelato" % TOLL_NORMA, ok2, "il peggiore dM %.1e dV %.1e" % (max(d["dM"] for d in ris), max(d["dV"] for d in ris)))
    ok4, n4 = True, []
    for N, _f in CASI:
        a = {d["L"]: d for d in trova(N, "intero", "oggi")}
        for d in trova(N, "congelato", "oggi"):
            va = a[d["L"]]["vita"] or STR.T_MAX
            # ### stabile fino a T_MAX implica la vita >= FATTORE_VITA x (a) quando (a) vive meno di T_MAX/FATTORE_VITA
            ok4 &= d["stabile"] and va * FATTORE_VITA <= STR.T_MAX
            n4.append("N %g L %d: %s" % (N, d["L"], "stabile" if d["stabile"] else "vita %d" % d["vita"]))
    esito("PUO' FALLIRE (4): (b) vive almeno %g volte (a) e resta entro il 20%% fino a T_MAX (zero di oggi, le due taglie)" % FATTORE_VITA, ok4, "; ".join(n4), deve=False)
    ok5, n5 = True, []
    for N, _f in CASI:
        a = {d["L"]: d for d in trova(N, "intero", "oggi")}
        for d in trova(N, "senza_legame", "oggi"):
            va, vc = a[d["L"]]["vita"] or STR.T_MAX + 1, d["vita"] if d["vita"] is not None else STR.T_MAX + 1
            ok5 &= vc < va
            n5.append("N %g L %d: %s contro %s" % (N, d["L"], vc, va))
    esito("PUO' FALLIRE (5): (c) si disperde piu' in fretta di (a) (zero di oggi, le due taglie)", ok5, "; ".join(n5), deve=False)
    print("### LA CONVERGENZA (le due taglie: lo stesso verdetto, la vita entro il %g%%)" % (100 * TOLL_VITA))
    for N, _f in CASI:
        for zero in ZERI:
            for modo in MODI:
                dd = trova(N, modo, zero)
                if len(dd) == 2:
                    a, b = dd
                    same = a["stabile"] == b["stabile"] and (a["stabile"] or abs(a["vita"] - b["vita"]) <= TOLL_VITA * max(a["vita"], b["vita"]))
                    print("  N %-7g zero %-4s %-12s: L %d %s, L %d %s -> %s" % (N, zero, modo, a["L"], "stabile" if a["stabile"] else a["vita"], b["L"], "stabile" if b["stabile"] else b["vita"], "CONVERGE" if same else "NON CONVERGE"))
                    scrivi({"tipo": "convergenza", "N": N, "zero": zero, "modo": modo, "converge": same})
    print("### LA LETTURA: lo zero simmetrico contro quello di oggi (la vita, a ogni taglia)")
    for N, _f in CASI:
        for modo in ("intero", "congelato"):
            for o, s_ in zip(trova(N, modo, "oggi"), trova(N, modo, "simm")):
                print("  N %-7g %-10s L %d: oggi %s, simmetrico %s" % (N, modo, o["L"], "stabile" if o["stabile"] else o["vita"], "stabile" if s_["stabile"] else s_["vita"]))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
