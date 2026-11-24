# -*- coding: utf-8 -*-
r"""**[M0528-R] LE LETTURE DEL LAPSE COME MOLTIPLICATORE** *(la carta `doc/CARTA_lapse_moltiplicatore.md`, sez. `4`; il task history `doc/TASK_HISTORY/2026-11-23_lapse_vincolo_codice.md`, sez. `2`: le letture fissate PRIMA dei numeri)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo_lettura.py > doc/referti_l2/lapse_vincolo.txt

**Sola lettura** dalle cartelle di `lapse_vincolo.py` *(`E:/soliton_simulator/controllo/M0528/`)* e dai riferimenti: [M1446] *(Eotvos V2, V3 senza vincolo)*, [M0908] *(`CHI/caduta/V0`, `V1` = V2V3, `V2`, `V3`)*, chi *(`CHI/mattone`, `k 2000`)*, [M0326-K] *(la coppia F0 in fase a `d 36`)*. **Una corsa che manca e' NON MISURATO**, mai ricavata.
**K1** il vuoto `max|N - 1|` *(AL BIT = `0.0`)*; il mattone `max|N(2000) - N(1500)|` *(dagli stati)* `< 1e-6`, `N` al nodo di `rho` massimo `< 1` per V2V3; il profilo `1 - N` agli anelli contro chi *(`serie_chi_02000`)* e la larghezza a meta' profondita' *(`(uN_R - uN_80)/(uN_0 - uN_80) = 1/2`, interpolata)*. **Il Pound-Rebka interno:** `omega` del centro e del bordo, medie su blocchi di `50` tick fra `k 500` e `2000`, la differenza con l'errore dai blocchi. **K2** il massimo delle iterazioni *(e quelle del primo tick, da freddo)*. **K3** `a` lungo `y` *(`eotvos_v2.a_caduta`)*; VERSO se `a - a(V0)` ha il segno di `chi` *(`+1`)*; NATURA se VERSO e `omega(centro) < omega(bordo)` oltre `2 sigma`. **K4** `eta = 2 (a1 - a2)/(a1 + a2)` col `sigma` di `eotvos_v2.lettura`; il cambio relativo contro il riferimento senza vincolo della stessa riga. **K5** `a` dal fit di `D(k)`; `A = (a_0 - a_180)/2`, `B = (a_0 + a_180)/2`; contro F0 e contro chi *(S15: `Delta a = +1.22e-6` a `d 39`, la sagoma, riscalato `x 39/36`: solo in fase)*. **La norma** relativa fra il primo e l'ultimo stato.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import lapse_vincolo as LV  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
RIF_EOTVOS = os.path.join(CTRL, "M1446", "eotvos")
RIF_CADUTA = os.path.join(CTRL, "CHI", "caduta")
RIF_CHI = os.path.join(CTRL, "CHI", "mattone")
RIF_COPPIA = os.path.join(CTRL, "M0326", "coppia_F0_stampo_d36", "serie.json")
DA_S15, D_S15 = 1.22e-06, 39.0            # ### la sagoma S15 (il test pulito, gravita_due_corpi.txt): Delta a di chi a d 39
RIGHE = ("V2", "V3", "V2V3")
COME_0908 = {"V2": "V2", "V3": "V3", "V2V3": "V1"}
ANELLI = (0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80)
OK = {}


def esito(che, ok, nota=""):
    OK[che] = ok
    print("  DEVE: %-112s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def leggi_json(f):
    import caduta_libera as CL
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f), "lo sha1 di %s NON coincide" % f
    return json.load(open(f, encoding="utf-8"))


def norma(d, k0, k1):
    import gravita_due_corpi_misure as GM
    v = []
    for k in (k0, k1):
        X, _m = GM.leggi(os.path.join(d, "stato_%06d.npz" % k))
        v.append(float(np.sum(np.abs(X["psi_h"]) ** 2)))
    return abs(v[1] / v[0] - 1.0)


def k1_vuoto():
    print("K1 IL VUOTO (TC.scena, il vuoto fresco, 500 tick; lapse_vincolo_vuoto.py):")
    for r in RIGHE:
        d = os.path.join(LV.BASE, "vuoto_v2_%s" % r)          # ### lapse_vincolo_vuoto.py (la v1 cadde: il controllo di Gauss con max rho = 0)
        f = os.path.join(d, "serie_000500.json")
        if not os.path.exists(f):
            esito("K1 vuoto %s: N = 1 AL BIT" % r, None)
            continue
        S = leggi_json(f)
        import gravita_due_corpi_misure as GM
        _X, m = GM.leggi(os.path.join(d, "stato_000000.npz"))
        print("    %s: max|psi_h| %.3e; u da %.17e a %.17e; max|N - 1| su 500 tick %.3e; le iterazioni max %d (il primo tick %d); %.2f s/tick" % (
            r, m["max_psi"], m["u_min"], m["u_max"], max(S["max_N_1"]), max(S["it"]), S["it"][0], float(np.mean(S["s_tick"]))))
        esito("K1 vuoto %s: N = 1 AL BIT a ogni tick" % r, max(S["max_N_1"]) == 0.0, "%.3e" % max(S["max_N_1"]))


def larghezza(u):
    x = np.array(ANELLI, float)
    y = (np.asarray(u) - u[-1]) / (u[0] - u[-1])
    for i in range(1, len(x)):
        if y[i] <= 0.5:
            return float(x[i - 1] + (x[i] - x[i - 1]) * (y[i - 1] - 0.5) / (y[i - 1] - y[i]))
    return math.nan


def k1_mattone():
    import gravita_due_corpi_misure as GM
    print("K1 IL MATTONE FERMO (il k 0 di C2, L 186, 2000 tick) E IL POUND-REBKA INTERNO:")
    with np.load(os.path.join(RIF_CHI, "serie_chi_02000.npz")) as z:
        chi_u = [float(z["uN_%d" % R][list(z["k"]).index(2000)]) for R in ANELLI]
    print("    chi a k 2000 (CHI/mattone):   1 - N agli anelli %s: %s; la larghezza a meta' %.2f" % (ANELLI, " ".join("%+.4e" % v for v in chi_u), larghezza(chi_u)))
    PR = {}
    for r in RIGHE:
        d = os.path.join(LV.BASE, "mattone_%s" % r)
        fz = os.path.join(d, "stato_02000.npz")
        if not os.path.exists(fz + ".sha1"):
            esito("K1 mattone %s" % r, None)
            continue
        with np.load(os.path.join(d, "serie_chi_02000.npz")) as z:
            ks = list(z["k"])
            mio = [float(z["uN_%d" % R][ks.index(2000)]) for R in ANELLI]
        X2, m2 = GM.leggi(fz)
        X1, _m1 = GM.leggi(os.path.join(d, "stato_01500.npz"))
        kap = float(m2["parametri"]["kappa"])
        N1, N2 = np.exp(-kap * X1["chi"]), np.exp(-kap * X2["chi"])
        var = float(np.max(np.abs(N2 - N1)))
        with np.load(os.path.join(d, "extra_02000.npz")) as z:
            E = {q: np.asarray(z[q]) for q in z.files}
        with np.load(os.path.join(d, "serie_02000.npz")) as z:
            Mn = np.asarray(z["M"])
        dn = abs(Mn[-1] / Mn[0] - 1.0)
        print("    %s a k 2000: 1 - N agli anelli %s; la larghezza a meta' %.2f; il rapporto a chi al centro %.4f" % (r, " ".join("%+.4e" % v for v in mio), larghezza(mio), mio[0] / chi_u[0]))
        print("       max|N(2000) - N(1500)| %.3e; 1 - N al centro (il nodo di rho massimo di C2, anello 0) %+.6e; la norma relativa da k 0 a 2000 %.2e; le iterazioni max %d (il primo tick, da freddo, %d); %.2f s/tick" % (
            var, mio[0], dn, int(E["it"].max()), int(E["it"][0]), float(E["s_tick"].mean())))
        esito("K1 mattone %s: N(r) stazionario, max|N(2000) - N(1500)| < 1e-6" % r, var < 1e-6, "%.3e" % var)
        if r == "V2V3":
            esito("K1 mattone V2V3 (Z1): N(centro) < 1", mio[0] > 0.0, "1 - N %+.4e" % mio[0])
        esito("K1 mattone %s: la norma entro 1e-12" % r, dn < 1e-12, "%.2e" % dn)
        esito("K2 mattone %s: le iterazioni < %d a ogni tick" % (r, LV.K2), int(E["it"].max()) < LV.K2, "%d" % int(E["it"].max()))
        oc, ob = E["om_c"][500:], E["om_b"][500:]
        bc, bb = oc.reshape(-1, 50).mean(axis=1), ob.reshape(-1, 50).mean(axis=1)
        dd = bc - bb
        PR[r] = (float(dd.mean()), float(dd.std(ddof=1) / math.sqrt(len(dd))))
        print("       il Pound-Rebka interno (k 500-2000, %d blocchi da 50): omega centro %.8f, bordo %.8f; centro - bordo %+.3e +- %.1e (%s)" % (
            len(dd), float(oc.mean()), float(ob.mean()), PR[r][0], PR[r][1], "il centro PIU' PIANO" if PR[r][0] < -2 * PR[r][1] else ("il centro PIU' VELOCE" if PR[r][0] > 2 * PR[r][1] else "uguali entro 2 sigma")))
    return PR


def caduta(r, sc, vinc):
    import eotvos_v2 as EV2
    if vinc is None:
        d = os.path.join(RIF_EOTVOS, "x%.1f" % sc, "caduta_" + r)
    else:
        d = os.path.join(LV.BASE, "caduta_%s_x%.1f_%s" % (r, sc, "vincolo" if vinc else "senza"))
    ac = EV2.a_caduta(d)
    if not ac:
        return None
    return ac[0][2], ac[0][3], d


def eta_di(a1, a2):
    eta = 2.0 * (a1[0] - a2[0]) / (a1[0] + a2[0])
    se = 2.0 * math.hypot(a1[1], a2[1]) * math.hypot(1.0, (a1[0] - a2[0]) / (a1[0] + a2[0])) / abs(a1[0] + a2[0])
    return eta, se


def k3_k4(PR):
    import eotvos_v2 as EV2
    print("K3 LA CADUTA x1.0 (### IL GRADIENTE RESTA IMPOSTO: N = N_imp x N_ris, la scena di [M0908]):")
    a0 = EV2.a_caduta(os.path.join(RIF_CADUTA, "V0"))
    print("    [M0908] V0 (N = 1): a %+.4e +- %.1e" % (a0[0][2], a0[0][3]))
    for r in RIGHE:
        ar = EV2.a_caduta(os.path.join(RIF_CADUTA, COME_0908[r]))
        x = caduta(r, 1.0, True)
        if x is None:
            esito("K3 caduta %s" % r, None)
            continue
        da = x[0] - a0[0][2]
        sd = math.hypot(x[1], a0[0][3])
        verso = da > 0.0
        print("    %s col vincolo: a %+.4e +- %.1e; a - a(V0) %+.4e +- %.1e: %s; senza il vincolo ([M0908] %s) a %+.4e +- %.1e, a - a(V0) %+.4e; il rapporto col/senza %.4f; la norma %.1e" % (
            r, x[0], x[1], da, sd, "VERSO N piu' basso" if verso else "VIA", COME_0908[r], ar[0][2], ar[0][3], ar[0][2] - a0[0][2], da / (ar[0][2] - a0[0][2]), norma(x[2], 0, 2000)))
        nat = verso and r in PR and PR[r][0] < -2 * PR[r][1]
        print("       K3 %s: %s%s" % (r, "VERSO" if verso else "VIA", "; NATURA (il centro batte piu' piano)" if nat else ("" if not verso else "; NON natura (il Pound-Rebka interno %s)" % ("non misurato" if r not in PR else "%+.2e +- %.1e" % PR[r]))))
    print("K4 EOTVOS (### IL GRADIENTE RESTA IMPOSTO): eta = 2 (a(x0.8) - a(x1.2))/(a(x0.8) + a(x1.2))")
    R4 = {}
    for r in RIGHE:
        v = [caduta(r, sc, True) for sc in (0.8, 1.2)]
        rif = [caduta(r, sc, None if r != "V2V3" else False) for sc in (0.8, 1.2)]
        if None in rif:
            print("    %s: il riferimento senza vincolo NON MISURATO" % r)
        else:
            er = eta_di(rif[0], rif[1])
            print("    %s senza vincolo: a x0.8 %+.4e +- %.1e, x1.2 %+.4e +- %.1e; eta %+.4e +- %.1e" % (r, rif[0][0], rif[0][1], rif[1][0], rif[1][1], er[0], er[1]))
        if None in v:
            esito("K4 Eotvos %s col vincolo" % r, None)
            continue
        ev = eta_di(v[0], v[1])
        print("    %s COL vincolo:   a x0.8 %+.4e +- %.1e, x1.2 %+.4e +- %.1e; eta %+.4e +- %.1e; la norma %.1e, %.1e" % (r, v[0][0], v[0][1], v[1][0], v[1][1], ev[0], ev[1], norma(v[0][2], 0, 2000), norma(v[1][2], 0, 2000)))
        if None not in rif:
            cr = ev[0] / er[0] - 1.0
            sc_ = math.hypot(ev[1] / er[0], ev[0] * er[1] / er[0] ** 2)
            R4[r] = (ev, er, cr, sc_)
            zona = "< 1%: LA PORTA G2" if abs(ev[0]) + 2 * ev[1] < 0.01 else ("fra 1% e 12%: MIGLIORA" if abs(ev[0]) + 2 * ev[1] < 0.12 else ">= 12%: LASCIA / PEGGIORA")
            print("       il cambio relativo eta_vinc/eta_rif - 1 = %+.4f +- %.4f (%s); eta - eta_rif %+.4e +- %.1e; K4 (con 2 sigma): %s" % (
                cr, sc_, "sale" if cr > 0 else "scende", ev[0] - er[0], math.hypot(ev[1], er[1]), zona))
    return R4


def k5():
    print("K5 LA COPPIA A d 36 (N_imp = 1: LA SORGENTE VERA), V2V3, 2000 tick:")
    import gravita_due_corpi_misure as GM
    A = {}

    def a_di(serie):
        D = serie["D"]
        ks = np.array([x[0] for x in D], float)
        Dv = np.array([x[1] for x in D], float)
        fb = GM.fit(ks, Dv)
        return fb[2], fb[3], abs(D[-1][2] / D[0][2] - 1.0), len(D)
    rif0 = json.load(open(RIF_COPPIA, encoding="utf-8"))
    A["F0_0"] = a_di(rif0)
    for nome, d in (("F0_180", "coppia_F0_180_senza"), ("V2V3_0", "coppia_V2V3_0_vincolo"), ("V2V3_180", "coppia_V2V3_180_vincolo")):
        f = os.path.join(LV.BASE, d, "serie_002000.json")
        if os.path.exists(f):
            A[nome] = a_di(leggi_json(f))
    for k, v in A.items():
        print("    %-9s a %+.4e +- %.1e (la norma %.1e, %d punti)" % (k, v[0], v[1], v[2], v[3]))
    out = {}
    for f in ("F0", "V2V3"):
        if f + "_0" in A and f + "_180" in A:
            a0, a1 = A[f + "_0"], A[f + "_180"]
            sA = 0.5 * math.hypot(a0[1], a1[1])
            out[f] = ((a0[0] - a1[0]) / 2.0, (a0[0] + a1[0]) / 2.0, sA)
            print("    %s: A %+.4e, B %+.4e (+- %.1e); abs(A/B) %.3f" % (f, out[f][0], out[f][1], sA, abs(out[f][0] / out[f][1])))
    if "F0" in out and "V2V3" in out:
        print("    V2V3 contro F0: A %.3f, B %.3f (il rapporto)" % (out["V2V3"][0] / out["F0"][0], out["V2V3"][1] / out["F0"][1]))
    if "V2V3_0" in A:
        da = A["V2V3_0"][0] - A["F0_0"][0]
        chi = DA_S15 * D_S15 / 36.0
        print("    in fase, il vincolo meno F0: Delta a %+.4e +- %.1e; chi (S15, +1.22e-6 a d 39, x 39/36) %+.4e: il rapporto %.3f" % (da, math.hypot(A["V2V3_0"][1], A["F0_0"][1]), chi, da / chi))
    return out


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "lapse_vincolo.py"))
    _presidio.avvia(__file__)
    print("=" * 140)
    print("[M0528-R] IL LAPSE COME MOLTIPLICATORE: LE LETTURE (la carta sez. 4; le letture fissate nel task history sez. 2)")
    print("### D1 (a): la media di N u tolta, somma chi = 0: N lontano dal mattone e' > 1, il profilo e' logaritmico. D3 (i): nella caduta e in Eotvos IL GRADIENTE RESTA IMPOSTO.")
    print("=" * 140)
    k1_vuoto()
    print("-" * 140)
    PR = k1_mattone()
    print("-" * 140)
    k3_k4(PR)
    print("-" * 140)
    k5()
    print("=" * 140)
    fall = [k for k, v in OK.items() if v is False]
    nm = [k for k, v in OK.items() if v is None]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s, %d NON MISURATI %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall, len(nm), nm))
    return 0


if __name__ == "__main__":
    sys.exit(main())
