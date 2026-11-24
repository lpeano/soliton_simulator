# -*- coding: utf-8 -*-
r"""**[M0428] L'AVVOLGIMENTO COL CASO NOTO DEL 15/11, IL SEGNO DELL'ANELLO 10-16, IL CASO NOTO VERO DEGLI ARCHI MATURI** *(l'ordine dei lavori di Luca `2026-11-22` `04:28`; la carta della girandola sez. `6` e la carta del triangolo sez. `7`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/notte_m0428.py avvolgimento > doc/referti_l2/girandola_avvolgimento.txt
    E:\python\py3132\python.exe doc/referti_l2/notte_m0428.py segno > doc/referti_l2/girandola_segno.txt
    E:\python\py3132\python.exe doc/referti_l2/notte_m0428.py t4 > doc/referti_l2/triangolo_chi_t4_caso_noto.txt

**avvolgimento** [M0428-W]: lo stato `0` delle sfasate e del triangolo in fase del 15/11, RICOSTRUITI come in `triangolo_flussi.py`; la fase di `psi_h` *(il primo mezzo arco di ogni nodo)* sul cerchio di raggio `5` attorno alla media dei tre centri: **1** nelle sfasate *(il caso noto)*, **0** in fase *(il deve-fallire)*. **segno** [M0428-S]: (a) l'anello `10-16` a `k 0` del t120 con lo strumento del film *(`cs = s N(chi)`, la fase (a))* e con quello del 15/11 *(il `cs` della scena, nessuna fase)*; (b) lo stesso anello sulle sfasate del 15/11 ricostruite *(`-574`)*; (c) la serie del t120 dal film. **t4** [M2357-T4]: sul mattone con `chi` della fisica vecchia *(`CHI/mattone`, gli stati `250 ... 3000`)* i `20` archi con `|Theta|` piu' alto a `k 3000` contro la media nel tempo di `|D(dtau cs)|` *(`d_i - d_j`, `cs = s exp(-kappa chi)` di ogni stato)*: `16` su `20` e il rango `>= 0.9`; DEVE FALLIRE con il solo stato di `k 3000`.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ESITI = []
CHI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI")


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  %-112s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def fine():
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def fase_nodi(psi_h, nodo):
    _u, primo = np.unique(np.asarray(nodo), return_index=True)
    return psi_h[primo]


def avvolto(psi_n, xyn, c, R=5.0):
    th = np.linspace(0.0, 2.0 * math.pi, 72, endpoint=False)
    nn = [int(np.argmin(np.hypot(*(xyn - (c + R * np.array([math.cos(t), math.sin(t)]))).T))) for t in th]
    k = int(np.argmax([float(np.sum(np.abs(psi_n[nn, i]) ** 2)) for i in range(psi_n.shape[1])]))
    ph = np.angle(psi_n[nn, k])
    dd = np.diff(np.concatenate([ph, ph[:1]]))
    return float(np.sum((dd + math.pi) % (2.0 * math.pi) - math.pi)) / (2.0 * math.pi), k


def anello(xyn, Jn, c, a=10.0, b=16.0):
    d = xyn - c
    r = np.hypot(*d.T)
    s = (r >= a) & (r < b)
    return float(np.sum(d[s, 0] * Jn[s, 1] - d[s, 1] * Jn[s, 0]))


def stato0_15_11(Z, v):
    """### lo stato 0 di (T-fase) o (T-sfasati) del 15/11: le righe di `triangolo_flussi.main`. `(C, centri)`."""
    import mattone as MT
    import mattone_triangolo as MTR
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    FR = [MTR.francobollo(k) for k in MTR.VARIANTI[v]]
    centri = MTR.posti(Z["bordo"]["c0"], FR, L)
    MT.vuoto_fresco(Z, t0)
    phi_F3 = st["phi_h"].copy()
    vuoto = {x: st[x].copy() for x in Z["chiavi"]}
    soli = []
    for fr, c in zip(FR, centri):
        for x in Z["chiavi"]:
            st[x][...] = vuoto[x]
        MT.incolla(Z, fr, c, True)
        soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
    psi, phi = soli[0][0].copy(), soli[0][1].copy()
    for s_ in soli[1:]:
        psi = psi + s_[0]
        phi = phi * (s_[1] / phi_F3)
    st["psi_h"][...] = psi
    st["phi_h"][...] = phi
    C = MT.Campi(Z, "MGU", rho_c, e)
    rho = MT.rho_di(Z)
    C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
    return C, centri


def flusso(Z, cam, vett, chi=None, pm=None):
    """### `J` per nodo sullo stato in `Z`: lo strumento del 15/11 *(chi None: il `cs` della scena, nessuna fase)* o del film *(`cs = s N(chi)`, la fase (a))*. Lo stato si rimette."""
    import _u1_prototipo as U1
    import chi_tick as CT
    mot = Z["mot"]
    n = mot.inc.n
    salvo = {x: Z["st"][x].copy() for x in Z["chiavi"]}
    cs0, lc0 = mot.cs, getattr(mot, "lambda_c", None)
    if chi is not None:
        N = np.exp(-float(pm["kappa"]) * chi)
        mot.cs = float(pm["s"]) * N
        mot.lambda_c = None
        CT.fase_a(mot, Z["st"], float(pm["e0"]), N)
    U1.scrivi_U(mot, cam)
    m = cam.m
    prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
    mot.operatori["spostamento_trasporto"](Z["st"], Z["par"], 0.5)
    J = np.sum(np.abs(Z["st"]["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
    for x in Z["chiavi"]:
        Z["st"][x][...] = salvo[x]
    mot.cs, mot.lambda_c = cs0, lc0
    return (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)


def preparativi():
    import mattone as MT
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    A1, A2 = np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]
    return MT, TO, A1, A2, np.stack([A1, A2, A1 + A2])


def avvolgimento():
    import _presidio
    _presidio.avvia(__file__)
    MT, TO, A1, A2, vett = preparativi()
    print("=" * 130)
    print("[M0428-W] L'AVVOLGIMENTO SUGLI STATI 0 DEL 15/11 RICOSTRUITI (psi_h, il cerchio di raggio 5 attorno alla media dei tre centri)")
    print("=" * 130)
    W = {}
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        nodo = np.asarray(Z["mot"].inc.nodo)
        for v in ("sfasati", "fase"):
            _C, centri = stato0_15_11(Z, v)
            cm = np.mean(np.asarray(centri, float), axis=0)
            xyn = TO.scarti(Z["m1"], Z["m2"], cm[0], cm[1], L)[:, :2]
            rho = MT.rho_di(Z)
            r = np.hypot(*xyn.T)
            w, k = avvolto(fase_nodi(Z["st"]["psi_h"], nodo), xyn, np.zeros(2))
            W[v] = w
            print("### %s: i centri %s, la media %s; rho entro 2 %.4e; l'avvolgimento %+.4f (la componente %d)" % (v, [list(map(int, c)) for c in centri], ["%.3f" % x for x in cm], float(rho[r <= 2.0].mean()), w, k))
            Z["metti"]()
    esito("W CASO NOTO: le sfasate del 15/11 a k 0, l'avvolgimento 1", round(W["sfasati"]) == 1, "%+.4f" % W["sfasati"])
    esito("W DEVE FALLIRE: il triangolo in fase del 15/11 a k 0, l'avvolgimento NON 1 (0)", round(W["fase"]) == 0, "%+.4f" % W["fase"])
    return fine()


def segno():
    import _presidio
    import triangolo_chi_v4 as TC
    import chi_tick as CT
    import chi_tick_v2 as CV2
    _presidio.avvia(os.path.join(_QUI, "triangolo_chi_v4.py"))
    _presidio.avvia(__file__)
    MT, TO, A1, A2, vett = preparativi()
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    print("=" * 130)
    print("[M0428-S] IL SEGNO DELL'ANELLO 10-16: (a) il t120 a k 0 coi due strumenti; (b) le sfasate del 15/11 ricostruite; (c) la serie del t120 dal film")
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        # (b) le sfasate del 15/11
        C15, centri = stato0_15_11(Z, "sfasati")
        cm = np.mean(np.asarray(centri, float), axis=0)
        xyn = TO.scarti(Z["m1"], Z["m2"], cm[0], cm[1], L)[:, :2]
        cam.A[...] = C15.campo.A
        Jb = flusso(Z, cam, vett)
        b = anello(xyn, Jb, np.zeros(2))
        print("### (b) le sfasate del 15/11 a k 0 ricostruite, lo strumento del 15/11, attorno alla media dei centri %s: l'anello 10-16 %+.3f" % (["%.3f" % x for x in cm], b))
        Z["metti"]()
        # (a) il t120 a k 0
        C, info = TC.prepara(Z, "t120")
        P, m0 = CV2.parametri_v2(Z, None, None, rho_c, e, MT.G2.T0, float(Z["s"]), float(C.e0), stato={x: Z["st"][x].copy() for x in Z["chiavi"]})
        chi0 = CT.chi_statico(Z["mot"], Z["st"], Z["par"], P, CT.Laplaciano(Z["mot"]), m0)
        cam.A[...] = C.campo.A
        V = np.asarray(info["centri"], float)
        G0 = V.mean(axis=0)
        xy0 = TO.scarti(Z["m1"], Z["m2"], G0[0], G0[1], L)[:, :2]
        rho = MT.rho_di(Z)
        angn = np.degrees(np.arctan2(xy0[:, 1], xy0[:, 0]))
        angv = [math.degrees(math.atan2(*(TO.scarti(np.array([v[0]]), np.array([v[1]]), G0[0], G0[1], L)[0, 1::-1]))) for v in V]
        bari = [(xy0[s] * rho[s][:, None]).sum(axis=0) / rho[s].sum() for s in [np.abs(((angn - a) + 180.0) % 360.0 - 180.0) < 60.0 for a in angv]]
        Gk = np.mean(bari, axis=0)
        Jfilm = flusso(Z, cam, vett, chi0, {"kappa": P.kappa, "s": P.s, "e0": P.e0})
        J15 = flusso(Z, cam, vett)
        af, a15 = anello(xy0, Jfilm, Gk), anello(xy0, J15, Gk)
        print("### (a) il t120 a k 0 (ricostruito con prepara), attorno a G_k %s dal G0: lo strumento del film (cs = s N(chi), la fase (a)) %+.3f; lo strumento del 15/11 (il cs della scena, nessuna fase) %+.3f; lo scarto relativo %.2e" % (
            ["%.3f" % x for x in Gk], af, a15, abs(af - a15) / abs(a15)))
        Z["metti"]()
    esito("S (b) CASO NOTO: le sfasate del 15/11 ricostruite, l'anello 10-16 entro l'1% da -574", abs(b + 574.0) <= 5.74, "%+.3f" % b)
    esito("S (a): i due strumenti sul t120 a k 0 coincidono entro l'1%", abs(af - a15) <= 0.01 * abs(a15), "%+.3f contro %+.3f" % (af, a15))
    print("### (c) la serie del t120 dal film (doc/referti_l2/film/girandola_t120_00000_02000.npz), attorno a G_k:")
    F = np.load(os.path.join(_QUI, "film", "girandola_t120_00000_02000.npz"))
    m1, m2 = F["m1"].astype(float), F["m2"].astype(float)
    xyf = TO.scarti(m1, m2, float(F["G0"][0]), float(F["G0"][1]), int(F["L"]))[:, :2]
    serie = []
    for k in [int(x) for x in F["k"]]:
        Gk = F["centri_bari_%06d" % k].astype(float).mean(axis=0)
        serie.append((k, anello(xyf, np.stack([F["Jx_%06d" % k], F["Jy_%06d" % k]], axis=1).astype(float), Gk)))
    print("    %s" % "; ".join("k %d %+.3f" % x for x in serie))
    seg = sorted(set(np.sign([v for _k, v in serie])))
    print("### (c) il segno: %s" % ("SEMPRE POSITIVO, nessun cambio" if seg == [1.0] else ("SEMPRE NEGATIVO" if seg == [-1.0] else "CAMBIA")))
    return fine()


def t4():
    import _presidio
    import prova_scatola5 as PS
    from solitone import toro as TO
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2357-T4] IL CASO NOTO VERO DEGLI ARCHI MATURI (Luca 04:18): |Theta| a k 3000 contro la media nel tempo di |D(dtau cs)|; 16 su 20 e il rango >= 0.9; DEVE FALLIRE con il solo stato di k 3000")
    print("=" * 130)
    ks = list(range(250, 3001, 250))
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        nodo = np.asarray(mot.inc.nodo)
        ii, jj = nodo[0::2], nodo[1::2]
        dtau = np.asarray(mot.dtau, dtype=float)
        Dd = []
        th = None
        for k in ks:
            f = os.path.join(CHI, "mattone", "stato_%05d.npz" % k)
            assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
            with np.load(f) as z:
                meta = json.loads(str(z["meta"]))
                pm = meta["parametri"]
                d = dtau * float(pm["s"]) * np.exp(-float(pm["kappa"]) * z["chi"])
                Dd.append(np.abs(d[ii] - d[jj]))
                if k == ks[-1]:
                    th = np.abs(z["theta_a"])
        Z["metti"]()
    media = np.mean(Dd, axis=0)
    uno = Dd[-1]

    def confronto(y):
        t20, y20 = set(np.argsort(th)[::-1][:20].tolist()), set(np.argsort(y)[::-1][:20].tolist())
        ra, rb = np.argsort(np.argsort(th)), np.argsort(np.argsort(y))
        return len(t20 & y20), float(np.corrcoef(ra, rb)[0, 1])
    c_m, c_1 = confronto(media), confronto(uno)
    print("### gli stati %d ... %d (%d; k 0 non salvato); gli archi %d; max |Theta| %.6f" % (ks[0], ks[-1], len(ks), len(th), float(th.max())))
    print("### la media nel tempo: in comune coi 20 piu' maturi %d su 20, il rango (Spearman su tutti gli archi) %.4f" % c_m)
    print("### il solo stato di k 3000: %d su 20, il rango %.4f" % c_1)
    esito("T4 CASO NOTO: |Theta| contro la media nel tempo di |D(dtau cs)|, 16 su 20 e il rango >= 0.9", c_m[0] >= 16 and c_m[1] >= 0.9, "%d, %.4f" % c_m)
    esito("T4 DEVE FALLIRE: con il solo stato di k 3000 (meno di 16 su 20 o il rango sotto 0.9)", not (c_1[0] >= 16 and c_1[1] >= 0.9), "%d, %.4f" % c_1)
    return fine()


if __name__ == "__main__":
    cmd = sys.argv[1:]
    assert cmd and cmd[0] in ("avvolgimento", "segno", "t4"), "il comando: avvolgimento | segno | t4"
    sys.exit({"avvolgimento": avvolgimento, "segno": segno, "t4": t4}[cmd[0]]())
