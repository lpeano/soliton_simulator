# -*- coding: utf-8 -*-
r"""**DOVE VA L'ENERGIA DEL LEGAME?** *(il mandato del 2026-10-27 dopo le 10:58; [[SOLITONE-VUOTO-CONGELATO]], [[SCOMPOSIZIONE-ZERO-LAMBDA]])*: ### **il conto dell'energia nel tempo del solitone `S1` di `74f99039`,
col tick intero e col vuoto congelato, per pezzo** *(i costituenti, la cinetica, il legame `S1`, il vuoto, `H_tot`)* ### **e per regione** *(VICINO entro `2` larghezze iniziali, LONTANO)*; ### **e il fronte del vuoto.**

> ### ⛔ **Il task history e' `2026-10-27_energia_del_legame.md`.** ### **In memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_solitone_vuoto_congelato` *(`S`, `FORMA`, `CASI`, `VITA_RIF`, `VUOTO`)*, `_solitoni_triangoli`, `_modi_pi_e_solitoni.largo`, `_scomposizione_solitone` *(`stato_uniforme`, `parti`, `F1`)*,
> `_screening_forme_s3.forma`, `_triangoli_bassa_energia.conv`, `_triangoli_forza` *(`coppia_K`, `v_max`, `matrice_L`)*, `energia_pesata.termini_di_h`, `tick.percorri_tick`.
> ### **Lo stato ripete le righe di `_solitone_vuoto_congelato.corsa`, col parametro `N`** *(il criterio `0` le confronta col jsonl)*.

Gira con:  python csv/_energia_del_legame.py > doc/referti_l2/energia_del_legame.txt
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

OGNI = 10
OGNI_VITA = 20
R_VICINO = 2.0
SOGLIA_FRONTE = 1e-6
FRAZ_TORO = 0.8
MODI = ("intero", "congelato")
ZERI = (("simm", 0.5), ("oggi", 0.0))
TOLL_NORMA = 1e-10
TOLL_TAGLIE = 1e-3
TOLL_ZERI = 1e-6
FATTORE_DERIVA = 10.0
PAR = {"eps": 0.0}
RIF = os.path.join(RADICE, "doc", "referti_l2", "solitone_vuoto_congelato.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "energia_del_legame.jsonl")
PEZZI = ("cost", "cin", "leg", "vuo", "tot")
REGIONI = ("vicino", "lontano", "totale")
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


def stato(N, fattore, rec):
    """### Le righe di `_solitone_vuoto_congelato.corsa` che costruiscono la scena e lo stato, col parametro `N`."""
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_forza as TF
    import scena_l2 as SL
    w0 = rec["larghezza"]
    q, r, u = STR.profilo_u(VC.FORMA, rec["c"], VC.S, N, STR.LAM0_TRI, w0)
    L = int(3 * math.ceil(fattore * w0 / 3.0))
    inc, mot, st, par = SL.scena_toro("triangoli", (L, L), 1.0, 0.1)
    n = inc.n
    mot.cs = np.full(n, VC.S)
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
    Q = TF.coppia_K(0.0, VC.S)[0]["Q"][:, 0]
    cel = g[:, None] * Q[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
    cel *= math.sqrt(N / float(np.sum(np.abs(cel) ** 2)))
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    r_mat = float(rr[g > 0].max()) if np.any(g > 0) else 0.0
    return L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat


def densita(inc, st):
    rho = np.zeros(inc.n)
    np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    lam = np.zeros(inc.n)
    np.add.at(lam, inc.nodo, np.abs(st["phi_h"]) ** 2)
    return rho, lam


def per_nodo(inc, mot, st, campo_zero):
    """### `H_cam` per nodo col campo `campo_zero` messo a zero: ### **i termini di nodo, piu' meta' di ogni termine d'arco a ciascuno dei suoi due nodi.**"""
    import energia_pesata as EP
    s = dict(st)
    s[campo_zero] = np.zeros_like(st[campo_zero])
    pn, pa = EP.termini_di_h(mot, s, PAR)
    out = np.array(pn, dtype=float).copy()
    out += 0.5 * np.bincount(inc.nodo[0::2], weights=pa, minlength=inc.n)
    out += 0.5 * np.bincount(inc.nodo[1::2], weights=pa, minlength=inc.n)
    return out


def energie(inc, mot, st, vic, e_K, lam_z):
    """### **Per regione:** `M`, `V`, i costituenti `M e_K(lambda)`, la cinetica, il legame `S1`, il vuoto, `H_tot` *(a zero `lambda`: `+ 2 pi lambda` per unita' di norma, materia e vuoto)*."""
    import _scomposizione_solitone as SC
    rho, lam = densita(inc, st)
    assert np.all(lam > 0.0), "Lambda nullo in un nodo: il legame S1 non e' definito"
    em = per_nodo(inc, mot, st, "phi_h") + 2 * math.pi * lam_z * rho
    ev = per_nodo(inc, mot, st, "psi_h") + 2 * math.pi * lam_z * lam
    el = lam * SC.F1(rho / lam)
    ec = rho * (e_K + 2 * math.pi * lam_z)
    out = {}
    for nome, m in (("vicino", vic), ("lontano", ~vic), ("totale", np.ones(inc.n, dtype=bool))):
        M = float(rho[m].sum())
        Em, Ev, El, Ec = float(em[m].sum()), float(ev[m].sum()), float(el[m].sum()), float(ec[m].sum())
        out[nome] = {"M": M, "V": float(lam[m].sum()), "cost": Ec, "cin": Em - Ec, "leg": El, "vuo": Ev, "tot": Em + Ev + El}
    return out, lam


def corsa(N, fattore, rec, modo, zero, lam_z, e_K):
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = stato(N, fattore, rec)
    n = inc.n
    w0 = rec["larghezza"]

    def forma_m():
        rho, _l = densita(inc, st)
        M = float(rho.sum())
        c = (rho @ pos) / M
        w2 = float(rho @ np.sum((pos - c) ** 2, axis=1)) / M
        fr = float(rho[np.hypot(pos[:, 0] - c[0], pos[:, 1] - c[1]) <= STR.RAGGIO_FRAZ * w0].sum()) / M
        return math.sqrt(w2), fr
    w_in, _fr = forma_m()
    vic = rr <= R_VICINO * w_in
    gr = np.bincount(inc.nodo, minlength=n).astype(float)
    e0, lam0 = energie(inc, mot, st, vic, e_K, lam_z)
    lam0e = lam0 / gr
    phi0 = st["phi_h"].copy()
    salta = VC.VUOTO if modo == "congelato" else ()
    serie, fronte, vita, vita20 = [], [], None, None
    ev_bit = True
    r_toro = FRAZ_TORO * 0.5 * L * math.sqrt(3.0) / 2.0
    t0 = time.time()
    with SF.forma(VC.FORMA), BE.conv(zero):
        for t in range(STR.T_MAX + 1):
            if t % OGNI == 0:
                if t:
                    ee, lam = energie(inc, mot, st, vic, e_K, lam_z)
                else:
                    ee, lam = e0, lam0
                w, fr = forma_m()
                rotto = abs(w / w_in - 1.0) > STR.TOLL_LARGH or fr < STR.FRAZ_MIN
                if vita is None and rotto:
                    vita = t
                if vita20 is None and rotto and t % OGNI_VITA == 0:
                    vita20 = t
                ev_bit &= ee["totale"]["vuo"] == e0["totale"]["vuo"]
                dl = np.abs(lam / gr - lam0e)
                rf = float(rr[dl > SOGLIA_FRONTE].max()) if np.any(dl > SOGLIA_FRONTE) else 0.0
                fronte.append([t, rf])
                serie.append({"t": t, "larghezza": w, "frazione": fr, "E": ee})
            if t < STR.T_MAX:
                TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))
                if modo == "congelato":
                    st["phi_h"][...] = phi0
    dM = max(abs(x["E"]["totale"]["M"] - e0["totale"]["M"]) / e0["totale"]["M"] for x in serie)
    dV = max(abs(x["E"]["totale"]["V"] - e0["totale"]["V"]) / e0["totale"]["V"] for x in serie)
    deriva = max(abs(x["E"]["totale"]["tot"] - e0["totale"]["tot"]) for x in serie)
    pf = [(t, r) for t, r in fronte if R_VICINO * w_in < r < r_toro]  # ### dal bordo di VICINO: sul toro il profilo della materia non ha bordo (r_materia oltre meta' toro)
    vel = float(np.polyfit([p[0] for p in pf], [p[1] for p in pf], 1)[0]) if len(pf) >= 3 else None
    return {"tipo": "corsa", "N": N, "L": L, "fattore": fattore, "modo": modo, "zero": zero, "lambda": lam_z, "e_K": e_K, "w_iniziale": w_in, "r_materia": r_mat, "r_vicino": R_VICINO * w_in,
            "r_toro": r_toro, "vita": vita, "vita20": vita20, "dM": dM, "dV": dV, "vuoto_al_bit": ev_bit, "deriva_tot": deriva, "velocita_fronte": vel, "punti_fronte": len(pf),
            "fronte": fronte, "serie": serie, "secondi": time.time() - t0}


def delta(d, t, reg, pz):
    a = [x for x in d["serie"] if x["t"] == t]
    return a[0]["E"][reg][pz] - d["serie"][0]["E"][reg][pz] if a else None


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_forza as TF
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("DOVE VA L'ENERGIA DEL LEGAME: il conto dell'energia nel tempo del solitone S1 di 74f99039, tick intero e vuoto congelato, per pezzo e per regione; il fronte del vuoto")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_energia_del_legame.py", "csv/_solitone_vuoto_congelato.py", "csv/_scomposizione_solitone.py", "csv/_solitoni_triangoli.py",
                                     "primo_ordine/energia_pesata.py", "doc/referti_l2/solitone_vuoto_congelato.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: OGNI %d OGNI_VITA %d R_VICINO %g SOGLIA_FRONTE %g FRAZ_TORO %g MODI %s ZERI %s TOLL_NORMA %g TOLL_TAGLIE %g TOLL_ZERI %g FATTORE_DERIVA %g; da _solitone_vuoto_congelato: S %g FORMA %s CASI %s VITA_RIF %s VUOTO %s; T_MAX %d"
          % (OGNI, OGNI_VITA, R_VICINO, SOGLIA_FRONTE, FRAZ_TORO, MODI, ZERI, TOLL_NORMA, TOLL_TAGLIE, TOLL_ZERI, FATTORE_DERIVA, VC.S, VC.FORMA, VC.CASI, VC.VITA_RIF, VC.VUOTO, STR.T_MAX))
    print("  l'energia: H_tot = H_cam(psi) + H_cam(phi) + sum Lambda F_1(rho/Lambda) (S1); a zero lambda + 2 pi lambda per unita' di norma (materia e vuoto, 0fb93b8c); i costituenti M e_K(lambda), la cinetica H_cam(psi) - M e_K")
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    rif = {}
    for l in io.open(RIF, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "corsa":
            rif[(d["N"], d["L"], d["modo"], d["zero"])] = d
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        c, _cy, _w0 = STR.c_triangoli(VC.S)
        recs = {N: MPS.largo(VC.FORMA, c, VC.S, N) for N, _f in VC.CASI}
    finally:
        MPS.LAM0 = vero
    vm = float(TF.v_max(TF.matrice_L(0.0, VC.S))[0])
    print("  v_max della coppia a s %g: %.6f archi per tick (il cono: 1)" % (VC.S, vm))
    ris = []
    ok0, n0 = True, []
    for N, fattori in VC.CASI:
        rec = {"larghezza": recs[N]["larghezza"], "c": c}
        e_K = None
        for fat in fattori:
            for zero, lam_z in ZERI:
                for modo in MODI:
                    if e_K is None:
                        _L, _i, _m, _s, _p, _pos, _rr, Q, m1, m2, _r = stato(N, fat, rec)
                        incu, motu, stu = SC.stato_uniforme(_L, Q, m1, m2)
                        Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
                        e_K = Eu / Mu
                        print("### N %g: la larghezza del risolutore %.4f; e_K(0) %+.6f" % (N, rec["larghezza"], e_K))
                    d = corsa(N, fat, rec, modo, zero, lam_z, e_K)
                    ris.append(d)
                    scrivi(d)
                    rf = rif.get((N, d["L"], modo, zero))
                    b0 = rf is not None and rf["w_iniziale"] == d["w_iniziale"] and rf["vita"] == d["vita20"]
                    ok0 &= b0
                    n0.append("N %g L %d %s %s vita %s/%s" % (N, d["L"], modo, zero, d["vita20"], rf["vita"] if rf else "-"))
                    tv = VC.VITA_RIF[N]
                    print("  N %-7g L %3d %-9s zero %-4s: vita %s (ogni 20: %s; 74f99039 %s); dM %.1e dV %.1e; il vuoto al bit %s; la deriva di H_tot %.3e; il fronte %s archi/tick (%d punti; r vicino %.1f, r toro %.1f; r materia %.1f) (%.0f s)"
                          % (N, d["L"], modo, zero, d["vita"], d["vita20"], rf["vita"] if rf else "-", d["dM"], d["dV"], d["vuoto_al_bit"], d["deriva_tot"],
                             "%.4f" % d["velocita_fronte"] if d["velocita_fronte"] is not None else "-", d["punti_fronte"], d["r_vicino"], d["r_toro"], d["r_materia"], d["secondi"]))
                    for t in (tv, STR.T_MAX):
                        for reg in REGIONI:
                            print("      Delta E a t %4d %-8s: %s" % (t, reg, "  ".join("%s %+.4e" % (pz, delta(d, t, reg, pz)) for pz in PEZZI)))
                    sys.stdout.flush()
    print("-" * 130)
    print("### LA LETTURA (lo zero simmetrico, il tick intero): il verso dello scambio, vicino; l'energia che arriva lontano")
    for d in ris:
        if d["modo"] == "intero" and d["zero"] == "simm":
            for t in (VC.VITA_RIF[d["N"]], STR.T_MAX):
                dl, dv, dc = delta(d, t, "vicino", "leg"), delta(d, t, "vicino", "vuo"), delta(d, t, "vicino", "cin")
                print("  N %-7g L %3d t %4d: vicino il legame %+.4e, il vuoto %+.4e, la cinetica %+.4e, i costituenti %+.4e; lontano il totale %+.4e (il vuoto %+.4e, il legame %+.4e)"
                      % (d["N"], d["L"], t, dl, dv, dc, delta(d, t, "vicino", "cost"), delta(d, t, "lontano", "tot"), delta(d, t, "lontano", "vuo"), delta(d, t, "lontano", "leg")))
            print("  N %-7g L %3d: il fronte del vuoto %s archi/tick, contro v_max %.4f" % (d["N"], d["L"], "%.4f" % d["velocita_fronte"] if d["velocita_fronte"] is not None else "-", vm))
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (0): lo stato a t 0 e la vita (ogni 20 tick) = il jsonl di 74f99039, per ogni N, L, modo e zero", ok0, "; ".join(n0))
    ok1 = all(d["dM"] <= TOLL_NORMA and d["dV"] <= TOLL_NORMA for d in ris) and all(d["vuoto_al_bit"] for d in ris if d["modo"] == "congelato")
    esito("DEVE PASSARE (1): M e V entro %g; col vuoto congelato l'energia del vuoto costante al bit" % TOLL_NORMA, ok1,
          "dM %.1e dV %.1e" % (max(d["dM"] for d in ris), max(d["dV"] for d in ris)))
    ok2, peg2 = True, 0.0
    ok3, peg3 = True, 0.0
    for N, fattori in VC.CASI:
        for zero, _lz in ZERI:
            for modo in MODI:
                a, b = [d for d in ris if d["N"] == N and d["zero"] == zero and d["modo"] == modo]
                sc = N * abs(a["e_K"])
                for t in (VC.VITA_RIF[N], STR.T_MAX):
                    for pz in PEZZI:
                        x = abs(delta(a, t, "totale", pz) - delta(b, t, "totale", pz)) / sc
                        peg2 = max(peg2, x)
                        ok2 &= x <= TOLL_TAGLIE
        for fat in fattori:
            for modo in MODI:
                s_, o_ = [d for d in ris if d["N"] == N and d["fattore"] == fat and d["modo"] == modo]
                sc = N * abs(s_["e_K"])
                for t in (VC.VITA_RIF[N], STR.T_MAX):
                    for reg in REGIONI:
                        for pz in PEZZI:
                            corr = 0.0
                            if pz in ("cost", "tot"):
                                corr += 2 * math.pi * (s_["lambda"] - o_["lambda"]) * delta(o_, t, reg, "M")
                            if pz in ("vuo", "tot"):
                                corr += 2 * math.pi * (s_["lambda"] - o_["lambda"]) * delta(o_, t, reg, "V")
                            x = abs(delta(s_, t, reg, pz) - delta(o_, t, reg, pz) - corr) / sc
                            peg3 = max(peg3, x)
                            ok3 &= x <= TOLL_ZERI
    esito("DEVE PASSARE (2): le differenze nel tempo dei pezzi (totale, alla vita e a T_MAX) alle due taglie entro %g di N |e_K(0)|" % TOLL_TAGLIE, ok2, "il peggiore %.2e" % peg2)
    esito("DEVE PASSARE (3): le differenze nel tempo coi due zeri uguali entro %g di N |e_K(0)|, tolto 2 pi lambda volte la differenza di norma" % TOLL_ZERI, ok3, "il peggiore %.2e" % peg3)
    ok4, n4 = True, []
    for d in ris:
        if d["modo"] == "intero":
            b = [x for x in ris if x["N"] == d["N"] and x["L"] == d["L"] and x["zero"] == d["zero"] and x["modo"] == "congelato"][0]
            ok4 &= d["deriva_tot"] <= FATTORE_DERIVA * b["deriva_tot"]
            n4.append("N %g L %d %s %.2e/%.2e" % (d["N"], d["L"], d["zero"], d["deriva_tot"], b["deriva_tot"]))
    esito("PUO' FALLIRE (4): H_tot nel tick intero entro %g volte la deriva del vuoto congelato" % FATTORE_DERIVA, ok4, "; ".join(n4), deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE, "v_max": vm})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
