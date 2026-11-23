# -*- coding: utf-8 -*-
r"""**[M0326-G] FH ALLA PROVA: EOTVOS, LA TENUTA LUNGA, LA COPPIA, IL SEGNO DI m_E** *(la carta `doc/CARTA_FH.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fh_suite.py eotvos_tenuta --forma FH --scala 0.8
    E:\python\py3132\python.exe doc/referti_l2/fh_suite.py eotvos_caduta --forma FH --scala 0.8 --coll V2
    E:\python\py3132\python.exe doc/referti_l2/fh_suite.py tenuta_lunga --forma FH          (10000 tick da k 1500; riparte dall'ultimo stato se c'e')
    E:\python\py3132\python.exe doc/referti_l2/fh_suite.py coppia_stampo                     (S5: F0, d 35, dallo stampo, 2000 tick)
    E:\python\py3132\python.exe doc/referti_l2/fh_suite.py segno_mE                          (S6: F0, A uniforme e A0 = +0.010, 200 tick)
    E:\python\py3132\python.exe doc/referti_l2/fh_suite.py lettura --cosa eotvos > doc/referti_l2/eotvos_FH.txt      (cosa: eotvos, tenuta, coppia, segno)

**Come la forma entra nelle scene di ieri** *(la carta sez. 0)*: `MV.scegli(forma)` e `_screening_forme_s3.pezzi_di` sostituito IN MEMORIA con una funzione che rende i `pezzi` del NUCLEO, prima di aprire la scena; `eotvos.py` ed `eotvos_v2.py` non si toccano *(si chiamano `eotvos.orologio(scala, "N1")` e `eotvos_v2.caduta(scala, coll)` con `eotvos.BASE` spostato su `M0326/eotvos_<forma>`)*. **La tenuta lunga:** `fondo_suite_v2.carica` *(lo stato a `k 1500`)*, gli stati ogni `250` col campo, `omega` per tick, la ripresa dall'ultimo stato. **La coppia:** `gravita_fase.prepara` con `gravita_fase.D = 35` in memoria e le fasi `0, 0`, il tick V0, `D(k)` ogni `10`. **Il segno:** `A <- A + A0 (a . x)`, `e A0 = +0.010`, `U` riscritto; il controllo che il capo `0` dell'arco del motore sia `ii` del campo.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import massa_calcio as MC  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import fondo_suite_v2 as FS  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0326")
K_LUNGA, K_COPPIA, K_SEGNO = 10000, 2000, 200
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "massa_calcio.py", "torneo_tenuta.py", "fondo_suite_v2.py", "eotvos.py", "eotvos_v2.py", "gravita_fase.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def con_forma(forma):
    """### la forma del nucleo nelle scene di ieri: `MV.scegli(forma)` e `pezzi_di` -> i `pezzi` del NUCLEO *(in memoria)*."""
    import _screening_forme_s3 as SF
    MV, P0 = TT.nucleo()
    MV.scegli(forma)
    SF.pezzi_di = lambda _nome: P0
    print("### la forma del nucleo nella scena: %s (MV.ATTIVA %s; pezzi_di -> %s.%s)" % (forma, MV.ATTIVA, P0.__module__, P0.__qualname__))
    return MV, P0


def eotvos_tenuta(forma, scala):
    import eotvos as EV
    avvia()
    con_forma(forma)
    EV.BASE = os.path.join(BASE, "eotvos_%s" % forma)
    return EV.orologio(scala, "N1")


def eotvos_caduta(forma, scala, coll):
    import eotvos as EV
    import eotvos_v2 as EV2
    avvia()
    con_forma(forma)
    EV.BASE = os.path.join(BASE, "eotvos_%s" % forma)
    return EV2.caduta(scala, coll)


def tenuta_lunga(forma):
    avvia()
    MV, P0 = TT.nucleo()
    sorgente = {"FH": "FH", "S1": "F0"}[forma]
    d_out = os.path.join(BASE, "tenuta_lunga_%s" % forma)
    os.makedirs(d_out, exist_ok=True)
    fatti = sorted(int(f[6:12]) for f in os.listdir(d_out) if f.startswith("stato_") and f.endswith(".npz") and os.path.exists(os.path.join(d_out, f + ".sha1")))
    t1 = time.time()
    with TC.scena() as Z:
        C, info, _dxy, forma_, _X = FS.carica(Z, sorgente, 1500)
        assert forma_ == forma
        om = []
        k0 = 0
        if fatti:
            import gravita_due_corpi_misure as GM
            import _u1_prototipo as U1
            k0 = fatti[-1]
            X, _m = GM.leggi(os.path.join(d_out, "stato_%06d.npz" % k0))
            Z["metti"]({x: X[x] for x in Z["chiavi"]})
            C.campo.A[...] = X["campo_A"]
            C.campo.E[...] = X["campo_E"]
            U1.scrivi_U(Z["mot"], C.campo)
            om = list(np.load(os.path.join(d_out, "omega_%06d.npy" % k0)))
            assert len(om) == k0
            print("### LA RIPRESA P8: dallo stato a k %d (dopo k 1500 della tenuta), omega fino a %d" % (k0, len(om)))
        print("### tenuta lunga %s: %s (k %d); fino a %d; l'impronta %s" % (forma, info["file"], info["k_file"], K_LUNGA, TT.impronta(Z, C)[:12]))

        def salva(k):
            import hashlib
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.save(os.path.join(d_out, "omega_%06d.npy" % k), np.array(om))
            np.savez(fz, meta=np.array(json.dumps({"forma": forma, "k": k, "partenza": info["file"]})), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
        if not fatti:
            salva(0)

        def dopo(kk, prima):
            om.append(float(-np.angle(np.vdot(prima, Z["st"]["psi_h"]))))
            k = k0 + kk
            if k % 250 == 0:
                salva(k)
                print("    [stato] k %d omega %+.6f (%.0f s)" % (k, om[-1], time.time() - t1))
                sys.stdout.flush()
        FS._tick_loop(Z, C, forma, K_LUNGA - k0, dopo, MV, P0, np.ones(Z["n"]), False)
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_LUNGA - k0, time.time() - t1))
    return 0


def coppia_stampo():
    import gravita_fase as GF
    import gravita_due_corpi_d as GDD
    from solitone import toro as TO
    avvia()
    MV, P0 = TT.nucleo()
    GF.D = 35
    GDD.avvia()
    d_out = os.path.join(BASE, "coppia_F0_stampo_d35")
    os.makedirs(d_out, exist_ok=True)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info = GF.prepara(Z, 0)
        V = np.asarray(info["centri"], float)
        M = 0.5 * (V[0] + V[1])
        A1 = np.asarray(TO.vettori()[0], float)[:2]
        dxy = TO.scarti(Z["m1"], Z["m2"], M[0], M[1], L)[:, :2]
        lato = dxy @ (A1 / np.hypot(*A1))
        print("### la coppia F0 dallo stampo: d %d (la distanza dei vertici %.4f), le fasi %s; l'impronta %s" % (GF.D, info["distanza"], info["fasi_gradi"], TT.impronta(Z, C)[:12]))
        Ds = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = [(dxy[s_] * rho[s_][:, None]).sum(axis=0) / rho[s_].sum() for s_ in (lato < 0.0, lato >= 0.0)]
            Ds.append((kk, float(np.hypot(*(b[1] - b[0]))), float(rho.sum())))

        def dopo(kk, prima):
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: D %.4f (%.0f s)" % (kk, Ds[-1][1], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        FS._tick_loop(Z, C, "S1", K_COPPIA, dopo, MV, P0, np.ones(n), False)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"D": Ds, "info": {k: info[k] for k in ("centri", "distanza", "fasi_gradi")}}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_COPPIA, time.time() - t1))
    return 0


def segno_mE():
    import _u1_prototipo as U1
    from solitone import toro as TO
    avvia()
    MV, P0 = TT.nucleo()
    d_out = os.path.join(BASE, "segno_mE")
    os.makedirs(d_out, exist_ok=True)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = FS.carica(Z, "F0", 1500)
        assert np.array_equal(nodo[0::2], C.campo.ii) and np.array_equal(nodo[1::2], C.campo.jj), "il capo 0 dell'arco del motore NON e' ii del campo: FERMO"
        u = MC.asse_u(1)
        A1, A2 = TO.vettori()
        a1, a2 = np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]
        proj = np.array([a1 @ u, a2 @ u, (a1 + a2) @ u])
        e = float(C.campo.e)
        A0 = 0.010 / e
        C.campo.A[...] = C.campo.A + A0 * np.tile(proj, C.campo.n)
        U1.scrivi_U(mot, C.campo)
        print("### il segno di m_E: A uniforme e A0 = +0.010 (A0 %.6e, e %r), le proiezioni %s; il capo 0 = ii (controllato); l'impronta %s" % (A0, e, proj.tolist(), TT.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b @ u), float(rho.sum())))

        def dopo(kk, prima):
            if kk % 5 == 0:
                misura(kk)
        misura(0)
        FS._tick_loop(Z, C, forma, K_SEGNO, dopo, MV, P0, np.ones(n), False)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"serie": serie, "A0": A0, "e": e}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_SEGNO, time.time() - t1))
    return 0


def _leggi(nome):
    f = os.path.join(BASE, nome, "serie.json")
    if not os.path.exists(f + ".sha1"):
        return None
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f)
    return json.load(open(f, encoding="utf-8"))


def lettura(cosa):
    import gravita_due_corpi_misure as GM
    avvia()
    print("=" * 130)
    if cosa == "segno":
        print("[M0326-S] IL SEGNO DI m_E (la carta sez. 5)")
        r = _leggi("segno_mE")
        r0 = json.load(open(os.path.join(FS.BASE, "calcio_F0_k1500_%s" % MC.nome(0.0, 1), "serie.json"), encoding="utf-8"))
        r1 = json.load(open(os.path.join(FS.BASE, "calcio_F0_k1500_%s" % MC.nome(0.010, 1), "serie.json"), encoding="utf-8"))
        s = np.array(r["serie"])
        m = s[:, 0] >= 50
        b = np.polyfit(s[m, 0], s[m, 1], 1)
        v0 = MC.velocita(r0["serie"])[0]
        v1 = MC.velocita(r1["serie"])[0]
        vA = float(b[0])
        print("  A uniforme (e A0 = +0.010): v %+.4e; la deriva v0 %+.4e; v - v0 %+.4e" % (vA, v0, vA - v0))
        print("  il calcio k = +0.010: v %+.4e; v - v0 %+.4e" % (v1, v1 - v0))
        stesso = (vA - v0) * (v1 - v0) > 0
        print("  il segno: %s -> k_cin = k %s e A; m_E = %s16.61 (%s con I1)" % ("STESSO del calcio" if stesso else "OPPOSTO al calcio", "+" if stesso else "-", "+" if stesso else "-", "incoerente" if stesso else "COERENTE"))
        esito("K5: il segno di m_E dalle righe (negativo, k_cin = k - e A) confermato dal controllo", not stesso)
        print("  la norma %.9e -> %.9e" % (s[0, 2], s[-1, 2]))
    if cosa == "coppia":
        print("[M0326-K] IL CASO NOTO DELLA COPPIA (la carta sez. 4)")
        r = _leggi("coppia_F0_stampo_d35")
        ks = np.array([x[0] for x in r["D"]], float)
        D = np.array([x[1] for x in r["D"]], float)
        fb = GM.fit(ks, D)
        a, sa = fb[2], fb[3]
        print("  F0 in fase dallo stampo, d %.4f: D da %.4f a %.4f; a %+.4e +- %.1e (il residuo %.2e); la norma %.9e -> %.9e" % (r["info"]["distanza"], D[0], D[-1], a, sa, fb[4], r["D"][0][2], r["D"][-1][2]))
        for nome, rif in (("il mandato", -1.0e-06), ("1/d da -1.2603e-06 a d 39", -1.2603e-06 * 39.0 / 35.0), ("lo stato compatto (M0149)", -1.3867e-06)):
            print("    contro %s %+.4e: il rapporto %.3f" % (nome, rif, a / rif))
        esito("K1 S5: entro il 15%% di -1.0e-06", abs(a / -1.0e-06 - 1.0) <= 0.15, "(%+.3e)" % a)
    if cosa == "eotvos":
        import eotvos as EV
        import eotvos_v2 as EV2
        print("[M0326-Q] EOTVOS CON FH (la carta sez. 1): eta = 2 (a1 - a2)/(a1 + a2); contro F0 (M1446-Q: V2 0.120 +- 0.012, V3 0.138 +- 0.014)")
        for forma in ("FH", "S1"):
            b = os.path.join(BASE, "eotvos_%s" % forma)
            for sc in EV.SCALE:
                f = os.path.join(b, "x%.1f" % sc, "tenuta", "fase.npz")
                if os.path.exists(f + ".sha1"):
                    w, sw, rms, picco, norma = EV.omega_di(f)
                    print("  %s x %g la tenuta: omega %.10f +- %.1e (il residuo %.3e); il picco %.4e -> %.4e; la norma %.9e -> %.9e" % (forma, sc, w, sw, rms, picco[0], picco[-1], norma[0], norma[-1]))
                    if forma == "S1" and sc == 0.8:
                        w0, _s, _r, _p, _n = EV.omega_di(os.path.join(EV.BASE, "x0.8", "tenuta", "fase.npz"))
                        esito("K1: F0 x0.8 con lo script nuovo = la tenuta di ieri entro il 2%% (al bit atteso)", abs(w / w0 - 1.0) <= 0.02, "(%.10f contro %.10f)" % (w, w0))
            if forma == "FH":
                for coll in ("V2", "V3"):
                    acc = {}
                    for sc in EV.SCALE:
                        ac = EV2.a_caduta(os.path.join(b, "x%.1f" % sc, "caduta_" + coll))
                        if ac:
                            acc[sc] = (ac[0][2], ac[0][3])
                            print("  FH x %g caduta %s: a %+.4e +- %.1e (il residuo %.2e)" % (sc, coll, ac[0][2], ac[0][3], ac[0][4]))
                    if len(acc) == 2:
                        a1, a2 = acc[0.8], acc[1.2]
                        eta = 2.0 * (a1[0] - a2[0]) / (a1[0] + a2[0])
                        sq = (a1[0] + a2[0]) ** 2
                        se = math.hypot(4.0 * a2[0] / sq * a1[1], 4.0 * a1[0] / sq * a2[1])          # ### d eta/d a1 = 4 a2/(a1+a2)^2, d eta/d a2 = -4 a1/(a1+a2)^2
                        rif = {"V2": (0.120, 0.012), "V3": (0.138, 0.014)}[coll]
                        d = abs(eta) - rif[0]
                        sd = math.hypot(se, rif[1])
                        giud = "MIGLIORA" if d < -3 * sd else ("PEGGIORA" if d > 3 * sd else "LASCIA")
                        print("  FH %s: ETA = %+.4f +- %.4f; F0 %.3f +- %.3f; |eta_FH| - eta_F0 = %+.4f (%.1f sigma): %s" % (coll, eta, se, rif[0], rif[1], d, abs(d) / sd, giud))
    if cosa == "tenuta":
        print("[M0326-T] LA TENUTA LUNGA (la carta sez. 2): w, il picco, i pezzi ogni 250; K3; il respiro")
        with TC.scena() as Z:
            nodo = np.asarray(Z["mot"].inc.nodo)
            n, L = Z["n"], Z["L"]
            Z["metti"]()
        for forma in ("FH", "S1"):
            d = os.path.join(BASE, "tenuta_lunga_%s" % forma)
            if not os.path.isdir(d):
                continue
            fs = sorted(f for f in os.listdir(d) if f.startswith("stato_") and f.endswith(".npz"))
            ser = []
            for f in fs:
                w, p, mx, M = TT.misura(os.path.join(d, f), nodo, n, L)
                ser.append((int(f[6:12]), w, p, mx, M))
            ks = np.array([x[0] for x in ser])
            ws = np.array([x[1] for x in ser])
            print("  %s: %d stati, k fino a %d (+ 1500 della tenuta); la norma %.9e -> %.9e" % (forma, len(ser), ks[-1], ser[0][4], ser[-1][4]))
            print("    k:  %s" % " ".join("%5d" % x for x in ks[::4]))
            print("    w:  %s" % " ".join("%5.2f" % x for x in ws[::4]))
            wm = float(ws.mean())
            ok = all(x[2] == 1 for x in ser) and bool(np.all(np.abs(ws / wm - 1.0) <= 0.30))
            print("    K3: la media di w %.3f; w da %.3f a %.3f (%.1f%% / %.1f%%); i pezzi massimi %d: %s" % (wm, ws.min(), ws.max(), 100 * (ws.min() / wm - 1), 100 * (ws.max() / wm - 1), max(x[2] for x in ser), "REGGE" if ok else "NON REGGE"))
            x = ws - wm
            F = np.abs(np.fft.rfft(x))
            fr = np.fft.rfftfreq(len(x), d=250.0)
            j = int(np.argmax(F[1:])) + 1
            print("    il respiro: il picco dello spettro a %.1f tick (frequenza %.2e); l'ampiezza (max - min)/2 %.3f" % (1.0 / fr[j], fr[j], (ws.max() - ws.min()) / 2))
            if os.path.exists(os.path.join(d, "omega_%06d.npy" % ks[-1])):
                om = np.load(os.path.join(d, "omega_%06d.npy" % ks[-1]))
                print("    omega: la media %+.7f; [1, 1000] %+.7f; ultimi 1000 %+.7f" % (float(om.mean()), float(om[:1000].mean()), float(om[-1000:].mean())))
    print("=" * 130)
    return 0 if all(ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa_", choices=("eotvos_tenuta", "eotvos_caduta", "tenuta_lunga", "coppia_stampo", "segno_mE", "lettura"))
    ap.add_argument("--forma", choices=("FH", "S1"))
    ap.add_argument("--scala", type=float)
    ap.add_argument("--coll", choices=("V2", "V3"))
    ap.add_argument("--cosa", choices=("eotvos", "tenuta", "coppia", "segno"))
    a = ap.parse_args(argv)
    if a.cosa_ == "eotvos_tenuta":
        return eotvos_tenuta(a.forma, a.scala)
    if a.cosa_ == "eotvos_caduta":
        return eotvos_caduta(a.forma, a.scala, a.coll)
    if a.cosa_ == "tenuta_lunga":
        return tenuta_lunga(a.forma)
    if a.cosa_ == "coppia_stampo":
        return coppia_stampo()
    if a.cosa_ == "segno_mE":
        return segno_mE()
    return lettura(a.cosa)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
