# -*- coding: utf-8 -*-
r"""**LE MISURE DELLA GIRANDOLA CON `chi` -- LA V4** *(i film interi oltre `k 6000` restano FUORI dal repo, in `E:\soliton_simulator\controllo\girandola_blocchi`, la richiesta di Luca dopo le `12:12`; la carta della girandola sez. `8`: qui il film si cerca nel repo e poi li'; l'isotropia salta i film leggeri; il resto la v3 riga per riga)*. **LA V3:** *(l'avvolgimento da `psi_h`: la v2 leggeva la chiave `psi` degli stati, tutta ZERO -- un falso zero, il mio errore, 38876f34; il sottocomando `isotropia` [M0333-ISO1], la carta della girandola sez. `5`; il resto la v2 riga per riga)*. **LA V2:** *(la decisione di Luca delle `03:48`: la forma delle pale `a = (l1 - l2)/(l1 + l2)`, `e` solo lettura, il caso noto (c) in `[0.125, 0.16]`; il caso noto IN FASE, `-658`; le scene scelte con `--scene`; la tabella t120 contro t000 [M0333-M]; la carta della girandola sez. `4`; il resto la v1 riga per riga)*. **LA V1: [M0329-M1/M2/M3] LE MISURE DELLA GIRANDOLA CON `chi`** *(il mandato di Luca `2026-11-22` `03:29`; la carta `doc/TASK_HISTORY/2026-11-22_girandola_chi.md`, sez. `2`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/girandola_chi_v4.py caso_noto > doc/referti_l2/girandola_chi_v4_caso_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/girandola_chi_v4.py giro --da 0 --fino 2000 --scene t120 t120r28 t000 > doc/referti_l2/girandola_chi_v4.txt
    E:\python\py3132\python.exe doc/referti_l2/girandola_chi_v4.py isotropia --k 2000 > doc/referti_l2/girandola_chi_isotropia.txt

**IL CASO NOTO PRIMA** *(sulle mappe del 15/11, `doc/referti_l2/mattone/triangolo_t120_mappe.npz` e `triangolo_flussi.npz`)*: **se non passa, lo script si ferma prima dei numeri nuovi.** **Poi, per i due tronchi** *(i file del film `doc/referti_l2/film/girandola_<scena>_<da>_<fino>.npz`, piu' `psi` dagli stati salvati per l'avvolgimento)*: (a) la rotazione, (b) i centri nei due modi, (c) le pale, (d) la circolazione, (e) il buco, (f) `chi`; **M3** il confronto; **M2** (d) ed (e) sul mattone della corsa nuova a `k 2000`.
"""
import argparse
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

CHI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI")
REF = os.path.join(_QUI, "mattone")
FILM = os.path.join(_QUI, "film")
FUORI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "girandola_blocchi")      # ### V4


def trova(nome):
    """### V4: il film nel repo, se no fuori."""
    for d in (FILM, FUORI):
        if os.path.exists(os.path.join(d, nome)):
            return os.path.join(d, nome)
    raise AssertionError("il film %s non e' ne' nel repo ne' in %s: FERMO" % (nome, FUORI))
SCENE = ("t120", "t120r28")
ANELLI_G = ((0, 3), (3, 6), (6, 10), (10, 16), (16, 30), (0, 45))
ANELLI_P = ((0, 6), (6, 12), (12, 18))
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  %-112s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def cart(c):
    """### coordinate di reticolo -> cartesiane."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    return float(c[0]) * np.asarray(A1, float)[:2] + float(c[1]) * np.asarray(A2, float)[:2]


def scarti(m1, m2, c, L):
    from solitone import toro as TO
    return TO.scarti(np.asarray(m1, float), np.asarray(m2, float), float(c[0]), float(c[1]), L)[:, :2]


def circ(d, Jx, Jy, a, b):
    r = np.hypot(d[:, 0], d[:, 1])
    s = (r >= a) & (r < b)
    return float(np.sum(d[s, 0] * Jy[s] - d[s, 1] * Jx[s]))


def pala(d, rho, u):
    """### `(e, e2, l'angolo dell'asse dalla radiale u, il raggio quadratico medio)` entro `18`."""
    r = np.hypot(d[:, 0], d[:, 1])
    s = r <= 18.0
    w = rho[s]
    T = (d[s][:, :, None] * d[s][:, None, :] * w[:, None, None]).sum(axis=0)
    lam, vec = np.linalg.eigh(T)
    l1, l2 = float(lam[1]), float(lam[0])
    v = vec[:, 1]
    ang = math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1]))
    ang = (ang + 90.0) % 180.0 - 90.0
    if ang == -90.0:
        ang = 90.0
    return math.sqrt(max(0.0, 1.0 - l2 / l1)), (l1 - l2) / (l1 + l2), ang, math.sqrt(float(np.sum(w * r[s] ** 2) / np.sum(w)))


def srotola(a):
    out = [a[0]]
    for g in a[1:]:
        out.append(out[-1] + (g - out[-1] + 180.0) % 360.0 - 180.0)
    return out


def angoli(cen, G):
    return [math.degrees(math.atan2(c[1] - G[1], c[0] - G[0])) for c in cen]


# ====================================================================== IL CASO NOTO
NODO_162 = None


def fase_dei_nodi(psi_h, nodo):
    """### V3: per ogni nodo `psi_h` del suo PRIMO mezzo arco *(l'indice piu' basso)*: `(n, 2)` complesso."""
    nodo = np.asarray(nodo)
    _u, primo = np.unique(nodo, return_index=True)
    return psi_h[primo]


def toro_nodo(L):
    """### gli archi `3 v + a` del toro di lato `L` *(come `esporta_film.toro`)*, `nodo` intrecciato."""
    v = np.arange(L * L)
    m1, m2 = v // L, v % L
    jj = np.stack([((m1 + 1) % L) * L + m2, m1 * L + (m2 + 1) % L, ((m1 + 1) % L) * L + (m2 + 1) % L], axis=1).reshape(-1)
    nodo = np.empty(6 * L * L, dtype=np.int64)
    nodo[0::2], nodo[1::2] = np.repeat(v, 3), jj
    return nodo


def caso_noto():
    print("=" * 130)
    print("IL CASO NOTO (le mappe del 15/11; la carta sez. 2): la rotazione +5.1, +5.1, +5.2 (0.1); le pale a k 2000 e in [0.13, 0.16], l'asse -51 (3); l'anello 10-16 delle sfasate a k 0 -574 (1%)")
    print("=" * 130)
    fm, ff = os.path.join(REF, "triangolo_t120_mappe.npz"), os.path.join(REF, "triangolo_flussi.npz")
    print("### %s sha1 %s; %s sha1 %s" % (os.path.basename(fm), sha1(fm)[:8], os.path.basename(ff), sha1(ff)[:8]))
    M = np.load(fm)
    L = int(M["L"])
    m1, m2 = M["m1"].astype(float), M["m2"].astype(float)
    tk = [int(t) for t in M["tick"]]
    cen_k = [[cart(c) for c in M["centri"][i]] for i in range(len(tk))]
    rot = []
    for j in range(3):
        a = srotola([angoli(cen_k[i], np.mean(cen_k[i], axis=0))[j] for i in range(len(tk))])
        rot.append(a[tk.index(2000)] - a[0])
    print("### (a) la rotazione del t120 a k 2000 (i centri delle mappe, attorno alla loro media): %s gradi" % ", ".join("%+.3f" % x for x in rot))
    i2 = tk.index(2000)
    rho = M["rho"][i2].astype(float)
    G = np.mean(cen_k[i2], axis=0)
    ps = []
    for j in range(3):
        d = scarti(m1, m2, M["centri"][i2][j], L)
        ps.append(pala(d, rho, cen_k[i2][j] - G))
    print("### (c) le pale a k 2000: la misura a = (l1 - l2)/(l1 + l2) %s; la lettura e = sqrt(1 - l2/l1) %s; l'asse dalla radiale %s gradi; il raggio quadratico medio %s" % (
        ", ".join("%.4f" % p[1] for p in ps), ", ".join("%.4f" % p[0] for p in ps), ", ".join("%+.2f" % p[2] for p in ps), ", ".join("%.3f" % p[3] for p in ps)))
    F = np.load(ff)
    cm = np.mean(F["sfasati_centri_00000"].astype(float), axis=0)
    d = scarti(F["m1"], F["m2"], cm, int(F["L"]))
    an = circ(d, F["sfasati_Jx_00000"].astype(float), F["sfasati_Jy_00000"].astype(float), 10, 16)
    print("### (d) l'anello 10-16 delle sfasate a k 0, attorno alla media dei centri %s: %+.3f" % (["%.3f" % x for x in cm], an))
    cf = np.mean(F["fase_centri_00000"].astype(float), axis=0)                                       # ### V2: il caso noto IN FASE (M0333)
    anf = circ(scarti(F["m1"], F["m2"], cf, int(F["L"])), F["fase_Jx_00000"].astype(float), F["fase_Jy_00000"].astype(float), 10, 16)
    print("### (d) l'anello 10-16 IN FASE a k 0, attorno alla media dei centri %s: %+.3f" % (["%.3f" % x for x in cf], anf))
    esito("CASO NOTO (a): la rotazione dei tre vertici entro 0.1 da +5.1, +5.1, +5.2", all(abs(x - y) <= 0.1 for x, y in zip(rot, (5.1, 5.1, 5.2))), ", ".join("%+.3f" % x for x in rot))
    esito("CASO NOTO (c): le tre a in [0.125, 0.16] e gli assi entro 3 da -51 (Luca 03:48)", all(0.125 <= p[1] <= 0.16 and abs(p[2] + 51.0) <= 3.0 for p in ps), ", ".join("%.4f" % p[1] for p in ps))
    esito("CASO NOTO (d): l'anello 10-16 delle sfasate a k 0 entro l'1% da -574", abs(an + 574.0) <= 5.74, "%+.3f" % an)
    esito("CASO NOTO (d) IN FASE: l'anello 10-16 a k 0 entro l'1% da -658 (M0333)", abs(anf + 658.0) <= 6.58, "%+.3f" % anf)
    return all(ok for _c, ok in ESITI)


# ====================================================================== I TRONCHI
def misura_scena(q, da, fino):
    f = trova("girandola_%s_%05d_%05d.npz" % (q, da, fino))
    print("=" * 130)
    print("LA GIRANDOLA %s, IL BLOCCO k %d-%d (%s, sha1 %s)" % (q, da, fino, os.path.basename(f), sha1(f)[:8]))
    print("=" * 130)
    F = np.load(f)
    L = int(F["L"])
    assert list(F["ii"][:6]) == [0, 0, 0, 1, 1, 1], "gli archi non sono 3 v + a: il flusso per nodo non vale"
    m1, m2 = F["m1"].astype(float), F["m2"].astype(float)
    G0 = F["G0"].astype(float)
    xyn = scarti(m1, m2, G0, L)
    ks = [int(k) for k in F["k"]]
    R = {"k": ks, "rot": [], "rotm": [], "e": [], "asse": [], "rqm": [], "anelli": [], "lati": [], "raggio": [], "latim": [], "buco": [], "avv": {}}
    a_b, a_m = [], []
    for k in ks:
        s = "_%06d" % k
        rho, chi = F["rho" + s].astype(float), F["chi" + s].astype(float)
        Jx, Jy = F["Jx" + s].astype(float), F["Jy" + s].astype(float)
        cb, cmx = F["centri_bari" + s].astype(float), F["centri_max" + s].astype(float)
        Gk, Gm = cb.mean(axis=0), cmx.mean(axis=0)
        a_b.append(angoli(cb, Gk))
        a_m.append(angoli(cmx, Gm))
        lati = [float(np.hypot(*(cb[a] - cb[b]))) for a, b in ((0, 1), (1, 2), (2, 0))]
        latim = [float(np.hypot(*(cmx[a] - cmx[b]))) for a, b in ((0, 1), (1, 2), (2, 0))]
        raggio = float(np.mean([np.hypot(*(c - Gk)) for c in cb]))
        d = xyn - Gk
        an = [circ(d, Jx, Jy, a, b) for a, b in ANELLI_G]
        ps, anp, chip = [], [], []
        for j in range(3):
            dj = xyn - cb[j]
            ps.append(pala(dj, rho, cb[j] - Gk))
            anp.append([circ(dj, Jx, Jy, a, b) for a, b in ANELLI_P])
            chip.append(float(chi[int(np.argmin(np.hypot(*dj.T)))]))
        r = np.hypot(*d.T)
        buco = float(rho[r <= 2.0].mean())
        anel = float(np.median(rho[(r >= 11.0) & (r < 13.0)]))
        chiG = float(chi[int(np.argmin(r))])
        lato = [float(chi[int(np.argmin(np.hypot(*(xyn - (cb[0] + t * (cb[1] - cb[0]))).T)))]) for t in np.linspace(0.0, 1.0, 41)]
        R["lati"].append(lati)
        R["latim"].append(latim)
        R["raggio"].append(raggio)
        R["e"].append([p[1] for p in ps])                                                    # ### V2: a, la misura di Luca 03:48
        R["buco"].append(buco / anel)
        R["asse"].append([p[2] for p in ps])
        R["rqm"].append([p[3] for p in ps])
        R["anelli"].append(an)
        print("  k %5d  G_k %s (dal G0)  (a) i lati %s, col rho massimo %s; il raggio medio %.3f" % (k, ["%+.3f" % x for x in Gk], ", ".join("%.3f" % x for x in lati), ", ".join("%.2f" % x for x in latim), raggio))
        print("           (b) i centri (baricentri) %s; (rho massimo) %s" % ([["%+.2f" % x for x in c] for c in cb], [["%+.1f" % x for x in c] for c in cmx]))
        print("           (c) le pale: a = (l1-l2)/(l1+l2) %s; la lettura e %s; l'asse %s gradi; il raggio quadratico medio %s" % (
            ", ".join("%.4f" % p[1] for p in ps), ", ".join("%.4f" % p[0] for p in ps), ", ".join("%+.2f" % p[2] for p in ps), ", ".join("%.3f" % p[3] for p in ps)))
        print("           (d) attorno a G_k: %s" % "; ".join("%d-%d %+.4e" % (a, b, v) for (a, b), v in zip(ANELLI_G, an)))
        print("           (d) attorno alle pale: %s" % " | ".join(", ".join("%d-%d %+.3e" % (a, b, v) for (a, b), v in zip(ANELLI_P, x)) for x in anp))
        print("           (e) il buco: rho entro 2 %.4e; la mediana dell'anello 11-13 %.4e; il rapporto %.4e" % (buco, anel, buco / anel))
        print("           (f) chi al centro %.6f; ai centri delle pale %s; lungo il lato 0-1 (41 punti) min %.6f, max %.6f, ai capi %.6f e %.6f, a meta' %.6f" % (
            chiG, ", ".join("%.6f" % x for x in chip), min(lato), max(lato), lato[0], lato[-1], lato[20]))
    for nome, aa in (("rot", a_b), ("rotm", a_m)):
        for j in range(3):
            s_ = srotola([x[j] for x in aa])
            R[nome].append([v - s_[0] for v in s_])
    print("  (a) la rotazione (gradi, dal primo stato del blocco; i baricentri): %s" % "; ".join("k %d: %s" % (k, ", ".join("%+.3f" % R["rot"][j][i] for j in range(3))) for i, k in enumerate(ks)))
    print("  (a) la rotazione (il rho massimo): %s" % "; ".join("k %d: %s" % (k, ", ".join("%+.2f" % R["rotm"][j][i] for j in range(3))) for i, k in enumerate(ks)))
    return R, F, xyn


def avvolgimento(q, k, Gk, xyn):
    f = os.path.join(CHI, "triangolo", q, "stato_%06d.npz" % k)
    if not os.path.exists(f + ".sha1"):
        return None
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as z:
        psi = fase_dei_nodi(z["psi_h"], NODO_162)                         # ### V3: da psi_h (la chiave psi e' zero)
    th = np.linspace(0.0, 2.0 * math.pi, 72, endpoint=False)
    nn = [int(np.argmin(np.hypot(*(xyn - (Gk + 5.0 * np.array([math.cos(t), math.sin(t)]))).T))) for t in th]
    c = int(np.argmax([float(np.sum(np.abs(psi[nn, i]) ** 2)) for i in range(psi.shape[1])]))
    ph = np.angle(psi[nn, c])
    dd = np.diff(np.concatenate([ph, ph[:1]]))
    w = float(np.sum((dd + math.pi) % (2.0 * math.pi) - math.pi)) / (2.0 * math.pi)
    return w, c


def mattone_solo(k):
    import prova_scatola5 as PS
    import chi_tick as CT
    import _u1_prototipo as U1
    from solitone import toro as TO
    MT, CV = PS.MT, PS.CV
    print("=" * 130)
    print("M2: IL MATTONE SOLO DELLA CORSA NUOVA (chi curato) A k %d: (d) e (e) attorno al centro del meta" % k)
    print("=" * 130)
    f = os.path.join(CHI, "mattone_v2", "stato_%05d.npz" % k)
    if not os.path.exists(f + ".sha1"):
        print("### %s NON c'e' ancora: M2 al giro dopo" % os.path.basename(f))
        return
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as z:
        X = {x: z[x].copy() for x in z.files}
    meta = json.loads(str(X.pop("meta")))
    pm = meta["parametri"]
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n, L = mot.inc.n, Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        assert list(nodo[0::2][:6]) == [0, 0, 0, 1, 1, 1], "gli archi non sono 3 v + a"
        A1, A2 = TO.vettori()
        vett = np.stack([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2], np.asarray(A1, float)[:2] + np.asarray(A2, float)[:2]])
        Z["metti"]({x: X[x] for x in Z["chiavi"]})
        C = PS.PO.campi(Z, rho_c, e, X["campo_A"], X["campo_E"])
        cs0 = mot.cs
        N = np.exp(-float(pm["kappa"]) * X["chi"])
        mot.cs = float(pm["s"]) * N
        mot.lambda_c = None
        CT.fase_a(mot, Z["st"], float(pm["e0"]), N)
        U1.scrivi_U(mot, C.campo)
        m = C.campo.m
        prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
        mot.operatori["spostamento_trasporto"](Z["st"], Z["par"], 0.5)
        J = np.sum(np.abs(Z["st"]["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
        Z["metti"]()
        mot.cs = cs0
        mot.lambda_c = None
        Jn = (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)
        rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        d = scarti(Z["m1"], Z["m2"], meta["centro"], L)
        an = [circ(d, Jn[:, 0], Jn[:, 1], a, b) for a, b in ANELLI_G]
        r = np.hypot(*d.T)
        print("### %s (sha1 %s), il centro %s" % (os.path.basename(f), sha1(f)[:8], ["%.3f" % x for x in meta["centro"]]))
        print("    (d) attorno al centro: %s" % "; ".join("%d-%d %+.4e" % (a, b, v) for (a, b), v in zip(ANELLI_G, an)))
        print("    (e) rho entro 2 %.4e; la mediana dell'anello 11-13 %.4e" % (float(rho[r <= 2.0].mean()), float(np.median(rho[(r >= 11.0) & (r < 13.0)]))))
        th = np.linspace(0.0, 2.0 * math.pi, 72, endpoint=False)
        nn = [int(np.argmin(np.hypot(*(d - 5.0 * np.array([math.cos(t), math.sin(t)])).T))) for t in th]
        psi = fase_dei_nodi(X["psi_h"], nodo)                             # ### V3: da psi_h
        c = int(np.argmax([float(np.sum(np.abs(psi[nn, i]) ** 2)) for i in range(psi.shape[1])]))
        ph = np.angle(psi[nn, c])
        dd = np.diff(np.concatenate([ph, ph[:1]]))
        print("    (e) l'avvolgimento sul cerchio di raggio 5 (la componente %d): %+.4f" % (c, float(np.sum((dd + math.pi) % (2.0 * math.pi) - math.pi)) / (2.0 * math.pi)))
        print("    il nucleo controrotante (l'anello 10-16 negativo e il 16-30 positivo): %s" % ("SI" if an[3] < 0.0 < an[4] else "NO"))


def confronto(Ra, Rb):
    print("=" * 130)
    print("M3: t120r28 CONTRO t120 ALLO STESSO k (uguali se la differenza delle medie e' entro la somma delle dispersioni max - min delle tre)")
    print("=" * 130)
    for i, k in enumerate(Ra["k"]):
        if k not in Rb["k"]:
            continue
        ib = Rb["k"].index(k)
        for nome, xa, xb in (("la rotazione", [Ra["rot"][j][i] for j in range(3)], [Rb["rot"][j][ib] for j in range(3)]),
                             ("a", Ra["e"][i], Rb["e"][ib]), ("l'asse", Ra["asse"][i], Rb["asse"][ib])):
            dm = abs(float(np.mean(xa)) - float(np.mean(xb)))
            tol = (max(xa) - min(xa)) + (max(xb) - min(xb))
            print("  k %5d  %-14s t120 %+.4f (disp %.4f)  t120r28 %+.4f (disp %.4f)  la differenza %.4f  %s" % (k, nome, np.mean(xa), max(xa) - min(xa), np.mean(xb), max(xb) - min(xb), dm, "UGUALI" if dm <= tol else "### DIVERSE"))
        print("  k %5d  gli anelli attorno a G_k, t120r28 / t120: %s" % (k, "; ".join("%d-%d %.4f" % (a, b, vb / va if va else float("nan")) for (a, b), va, vb in zip(ANELLI_G, Ra["anelli"][i], Rb["anelli"][ib]))))


def fase_contro(Ra, Rb):
    """### V2 [M0333-M]: t120 contro t000 a ogni k comune."""
    print("=" * 130)
    print("[M0333-M] t120 CONTRO t000 (il triangolo IN FASE): il buco, l'avvolgimento, gli anelli 6-10 e 10-16, i lati dal rho massimo, la rotazione")
    print("=" * 130)
    for i, k in enumerate(Ra["k"]):
        if k not in Rb["k"]:
            continue
        ib = Rb["k"].index(k)
        print("  k %5d  rho al centro / anello 11-13: t120 %.4e, t000 %.4e; l'avvolgimento: t120 %s, t000 %s" % (k, Ra["buco"][i], Rb["buco"][ib], Ra["avv"].get(k, "--"), Rb["avv"].get(k, "--")))
        print("           gli anelli 6-10: t120 %+.4e, t000 %+.4e; 10-16: t120 %+.4e, t000 %+.4e" % (Ra["anelli"][i][2], Rb["anelli"][ib][2], Ra["anelli"][i][3], Rb["anelli"][ib][3]))
        print("           i lati (rho massimo): t120 %s; t000 %s; la rotazione (i baricentri): t120 %s; t000 %s" % (
            ", ".join("%.2f" % x for x in Ra["latim"][i]), ", ".join("%.2f" % x for x in Rb["latim"][ib]), ", ".join("%+.3f" % Ra["rot"][j][i] for j in range(3)), ", ".join("%+.3f" % Rb["rot"][j][ib] for j in range(3))))


# ====================================================================== [M0333-ISO1] L'ISOTROPIA (la carta della girandola sez. 5)
GRANA = 1e-3


def M_inv():
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    M = np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]]).T
    return np.linalg.inv(M)


def contorno(rho, L, c):
    """### `R(theta)` in `360` direzioni attorno a `c` *(coordinate di reticolo reali)*: il primo raggio in cui `rho` interpolato scende sotto `max / 2`."""
    Mi = M_inv()
    th = np.radians(np.arange(360.0))
    rr = np.arange(0.0, 45.0 + 1e-9, 0.05)
    X = rr[None, :] * np.cos(th)[:, None]
    Y = rr[None, :] * np.sin(th)[:, None]
    u = c[0] + Mi[0, 0] * X + Mi[0, 1] * Y
    v = c[1] + Mi[1, 0] * X + Mi[1, 1] * Y
    u0, v0 = np.floor(u), np.floor(v)
    fu, fv = u - u0, v - v0
    i, j = u0.astype(np.int64) % L, v0.astype(np.int64) % L
    ip, jp = (i + 1) % L, (j + 1) % L
    r = lambda a, b: rho[a * L + b]
    su = fu >= fv
    val = np.where(su, (1.0 - fu) * r(i, j) + (fu - fv) * r(ip, j) + fv * r(ip, jp), (1.0 - fv) * r(i, j) + (fv - fu) * r(i, jp) + fu * r(ip, jp))
    meta = 0.5 * float(rho.max())
    R = np.empty(360)
    for q in range(360):
        sotto = np.nonzero(val[q] < meta)[0]
        sotto = sotto[sotto > 0]
        assert sotto.size, "il contorno non si chiude entro 45 nella direzione %d" % q
        b = int(sotto[0])
        a = b - 1
        R[q] = rr[a] + (val[q, a] - meta) / (val[q, a] - val[q, b]) * (rr[b] - rr[a])
    return R, th


def armoniche(R, th):
    c = {m: complex(np.mean(R * np.exp(-1j * m * th))) for m in (0, 3, 6)}
    A0 = abs(c[0])
    d6 = (-math.degrees(np.angle(c[6])) / 6.0) % 60.0
    return 2.0 * abs(c[3]) / A0, 2.0 * abs(c[6]) / A0, d6, min(d6, 60.0 - d6), A0


def centro_rho(rho, m1, m2, ref, L):
    d = scarti(m1, m2, ref, L)
    s_ = np.hypot(*d.T) <= 45.0
    off = (d[s_] * rho[s_][:, None]).sum(axis=0) / rho[s_].sum()
    Mi = M_inv()
    return np.array([ref[0] + Mi[0] @ off, ref[1] + Mi[1] @ off])


def massimi(rho, L):
    g = rho.reshape(L, L)
    vic = [np.roll(np.roll(g, a, 0), b, 1) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))]
    loc = np.all([g > x for x in vic], axis=0) & (g >= 0.5 * g.max())
    return int(loc.sum())


def forma(nome, rho, L, ref):
    m = np.arange(L * L)
    m1, m2 = (m // L).astype(float), (m % L).astype(float)
    c = centro_rho(rho, m1, m2, ref, L)
    R, th = contorno(rho, L, c)
    a3, a6, d6, asse6, A0 = armoniche(R, th)
    d = scarti(m1, m2, c, L)
    r = np.hypot(*d.T)
    s_ = rho >= 0.5 * rho.max()
    rqm = math.sqrt(float(np.sum(rho[s_] * r[s_] ** 2) / np.sum(rho[s_])))
    nm = massimi(rho, L)
    print("    %-34s il centro %s; R medio (A0) %.4f; A3/A0 %.3e; A6/A0 %.3e; il massimo di A6 a %.2f gradi, dall'asse %.2f; rqm %.4f, la massa %.6e; i massimi locali %d" % (
        nome, ["%.3f" % x for x in c], A0, a3, a6, d6, asse6, rqm, float(np.sum(rho[s_])), nm))
    return {"A0": A0, "a3": a3, "a6": a6, "asse6": asse6, "rqm": rqm, "nmax": nm}


def isotropia(ks):
    print("=" * 130)
    print("[M0333-ISO1] L'ISOTROPIA (la carta della girandola sez. 5): il contorno a meta' del massimo in 360 direzioni, A3/A0, A6/A0, la fase di A6; la grana %g" % GRANA)
    print("=" * 130)
    L = 162
    m = np.arange(L * L)
    m1, m2 = (m // L).astype(float), (m % L).astype(float)
    cc = (81.3, 80.7)
    r = np.hypot(*scarti(m1, m2, cc, L).T)
    disco = np.exp(-r * r / (2.0 * 13.0 * 13.0))
    d = scarti(m1, m2, cc, L)
    a = 15.0 * math.cos(math.radians(30.0))
    esa = np.ones(L * L)
    for k in range(6):
        nrm = np.array([math.cos(math.radians(30.0 + 60.0 * k)), math.sin(math.radians(30.0 + 60.0 * k))])
        esa[d @ nrm > a] = 0.0
    print("### IL CASO NOTO (costruiti a mano sul toro di L 162, attorno a %s)" % (cc,))
    fd = forma("il disco (sigma 13)", disco, L, cc)
    fe = forma("l'esagono (raggio 15, vertici sugli assi)", esa, L, cc)
    esito("ISO CASO NOTO: il disco isotropo, A3/A0 e A6/A0 sotto la grana", fd["a3"] < GRANA and fd["a6"] < GRANA, "%.2e, %.2e" % (fd["a3"], fd["a6"]))
    esito("ISO CASO NOTO DEVE FALLIRE come isotropo: l'esagono, A6/A0 sopra 10 grane e la fase di A6 entro 5 gradi da un asse", fe["a6"] > 10.0 * GRANA and fe["asse6"] <= 5.0, "%.2e, dall'asse %.2f" % (fe["a6"], fe["asse6"]))
    if not all(ok for _c, ok in ESITI):
        print("### IL CASO NOTO DELL'ISOTROPIA NON PASSA: nessun numero nuovo. FERMO")
        return
    fv = os.path.join(_RADICE, "..", "wt_mitosi_chi", "doc", "referti_l2", "film", "mattone_chi.npz")
    fv = os.path.normpath(fv)
    V = np.load(fv) if os.path.exists(fv) else None
    print("### il riferimento: il mattone vecchio, %s (sha1 %s)" % (fv, sha1(fv)[:8] if V is not None else "NON TROVATO"))
    nodo186 = toro_nodo(186)
    for k in ks:
        print("  k %d" % k)
        T = None
        for d_, f in sorted((d_, f) for d_ in (FILM, FUORI) if os.path.isdir(d_) for f in os.listdir(d_)):            # ### V4
            if f.startswith("girandola_t000_") and f.endswith(".npz") and "leggero" not in f:
                F = np.load(os.path.join(d_, f))
                if k in [int(x) for x in F["k"]]:
                    T = forma("il t000 (%s)" % f, F["rho_%06d" % k].astype(float), int(F["L"]), F["G0"].astype(float))
                    break
        if T is None:
            print("    il t000: nessun file del film con k %d" % k)
        fm = os.path.join(CHI, "mattone_v2", "stato_%05d.npz" % k)
        Mn = None
        if os.path.exists(fm + ".sha1"):
            assert open(fm + ".sha1", encoding="utf-8").read().split()[0] == sha1(fm), "lo sha1 di %s NON coincide" % fm
            with np.load(fm) as z:
                rho = np.bincount(nodo186, weights=np.sum(np.abs(z["psi_h"]) ** 2, axis=1), minlength=186 * 186)
                cen = json.loads(str(z["meta"]))["centro"]
            Mn = forma("il mattone nuovo (%s)" % os.path.basename(fm), rho, 186, cen)
        else:
            print("    il mattone nuovo: lo stato di k %d non c'e'" % k)
        if V is not None and "rho_%06d" % k in V.files:
            forma("il mattone vecchio (il film)", V["rho_%06d" % k].astype(float), int(V["L"]), V["centro"].astype(float))
        if T is not None and Mn is not None:
            print("    LA TABELLA t000 / il mattone nuovo: A6/A0 %.3e / %.3e (il rapporto %.3f); A3/A0 %.3e / %.3e; rqm %.3f / %.3f; (R_mattone / R_fuso)^2 %.3f; i massimi %d / %d" % (
                T["a6"], Mn["a6"], T["a6"] / Mn["a6"], T["a3"], Mn["a3"], T["rqm"], Mn["rqm"], (Mn["A0"] / T["A0"]) ** 2, T["nmax"], Mn["nmax"]))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("giro")
    g.add_argument("--da", type=int, required=True)
    g.add_argument("--fino", type=int, required=True)
    g.add_argument("--scene", nargs="+", choices=("t120", "t120r28", "t000"), required=True)     # ### V2
    sub.add_parser("caso_noto")
    iso = sub.add_parser("isotropia")                                             # ### V3
    iso.add_argument("--k", type=int, nargs="+", required=True)
    x = ap.parse_args(argv)
    if x.cmd == "isotropia":
        isotropia(x.k)
        print("-" * 130)
        for c, ok in ESITI:
            print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
        print("=" * 130)
        return 0 if all(ok for _c, ok in ESITI) else 1
    if x.cmd == "caso_noto":
        ok = caso_noto()
        print("=" * 130)
        return 0 if ok else 1
    if not caso_noto():
        print("### IL CASO NOTO NON PASSA: nessun numero nuovo (la carta sez. 2). FERMO")
        print("=" * 130)
        return 1
    R = {}
    global NODO_162
    for q in x.scene:
        Rq, F, xyn = misura_scena(q, x.da, x.fino)
        NODO_162 = np.empty(2 * len(F["ii"]), dtype=np.int64)
        NODO_162[0::2], NODO_162[1::2] = F["ii"], F["jj"]
        for k in Rq["k"]:
            if k == 0:
                print("  (e) l'avvolgimento a k 0: lo stato ricostruito non e' salvato, non letto")
                continue
            Gk = F["centri_bari_%06d" % k].astype(float).mean(axis=0)
            w = avvolgimento(q, k, Gk, xyn)
            print("  (e) l'avvolgimento a k %d sul cerchio di raggio 5 attorno a G_k: %s" % (k, "%+.4f (la componente %d), arrotondato %d" % (w[0], w[1], round(w[0])) if w else "lo stato non c'e'"))
            if w:
                Rq["avv"][k] = "%+.4f" % w[0]
        R[q] = Rq
    if "t120" in R and "t120r28" in R:
        confronto(R["t120"], R["t120r28"])
    if "t120" in R and "t000" in R:
        fase_contro(R["t120"], R["t000"])
    mattone_solo(x.fino)
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
