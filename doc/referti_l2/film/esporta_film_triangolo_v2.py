# -*- coding: utf-8 -*-
r"""**[M0329-F1] IL FILM LEGGERO DELLA GIRANDOLA: I DUE TRONCHI DEL TRIANGOLO PER BLOCCHI, COL FLUSSO E I CENTRI** *(il mandato di Luca `2026-11-22` `03:29`; la carta `doc/TASK_HISTORY/2026-11-22_girandola_chi.md`, sez. `1-2`; SOLA LETTURA, nessuna corsa toccata; la v1, `esporta_film_triangolo.py`, senza `J` e senza i centri, non si e' girata)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/film/esporta_film_triangolo_v2.py --quale t120 --da 0 --fino 2000 --out doc/referti_l2/film/girandola_t120_00000_02000.npz
    E:\python\py3132\python.exe doc/referti_l2/film/esporta_film_triangolo_v2.py --quale t120r28 --da 0 --fino 2000 --out doc/referti_l2/film/girandola_t120r28_00000_02000.npz

**Gli stati:** con `--da 0`, `k 0` RICOSTRUITO con `triangolo_chi_v3.prepara` *(nessun tick; i vertici e `m0` confrontati col `meta` della corsa)*; poi ogni stato salvato di `CHI/triangolo/<quale>` con `--da < k <= --fino` *(lo sha1 controllato)*. **Per stato:** `rho`, `chi`, `Jx`, `Jy` per nodo; `absE` *(`|campo_E|`)* e `J` per arco; **i centri** *(cartesiani, dal baricentro `G0` dei tre vertici)*: il baricentro di `rho` e il nodo di `rho` massimo di ogni settore di `120` gradi. **Il flusso:** lo strumento di `triangolo_flussi.py` *(una COPIA dello stato, `U` dal campo, `spostamento_trasporto` a frazione `0.5`)*, **col `cs = s N(chi)` dello stato e la fase (a) prima dello spostamento, come nel tick**. **Una volta:** `ii`, `jj`, `m1`, `m2`, `x`, `y`, i vertici, `G0`. `float32`, compresso; sopra `50 MB` si ferma.
"""
import argparse
import glob
import hashlib
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RL2 = os.path.dirname(_QUI)
if _RL2 not in sys.path:
    sys.path.insert(0, _RL2)
import triangolo_chi_v3 as T3  # noqa: E402

TETTO = 50e6


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_RL2, "triangolo_chi_v3.py"))
    _presidio.avvia(os.path.normpath(os.path.join(_RL2, "..", "..", "csv", "solitone", "triangolo_flussi.py")))
    _presidio.avvia(__file__)
    import chi_tick as CT
    import chi_tick_v2 as CV2
    import _u1_prototipo as U1
    from solitone import toro as TO
    ap = argparse.ArgumentParser()
    ap.add_argument("--quale", choices=T3.QUALI, required=True)
    ap.add_argument("--da", type=int, required=True)
    ap.add_argument("--fino", type=int, required=True)
    ap.add_argument("--out", required=True)
    x = ap.parse_args(argv)
    d = os.path.join(T3.BASE, x.quale)
    fs = sorted((f for f in glob.glob(os.path.join(d, "stato_*.npz")) if os.path.exists(f + ".sha1") and x.da < int(os.path.basename(f)[6:-4]) <= x.fino), key=lambda f: int(os.path.basename(f)[6:-4]))
    assert fs and int(os.path.basename(fs[-1])[6:-4]) == x.fino, "lo stato di k %d non c'e' ancora" % x.fino
    MT = T3.moduli()[0]
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    D = {}
    ks = []
    with T3.scena() as Z:
        mot = Z["mot"]
        n, L = mot.inc.n, Z["L"]
        nodo = np.asarray(mot.inc.nodo, dtype=np.int64)
        A1, A2 = TO.vettori()
        A1, A2 = np.asarray(A1, dtype=float)[:2], np.asarray(A2, dtype=float)[:2]
        vett = np.stack([A1, A2, A1 + A2])
        m1, m2 = np.asarray(Z["m1"], dtype=float), np.asarray(Z["m2"], dtype=float)
        xy = m1[:, None] * A1[None, :] + m2[:, None] * A2[None, :]
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        sp = mot.operatori["spostamento_trasporto"]
        cs_scena = np.array(mot.cs, copy=True) if hasattr(mot.cs, "__len__") else mot.cs
        stati = []
        info = None
        if x.da == 0:
            C, info = T3.prepara(Z, x.quale)
            P, m0 = CV2.parametri_v2(Z, None, None, rho_c, e, MT.G2.T0, float(Z["s"]), float(C.e0), stato={q: Z["st"][q].copy() for q in Z["chiavi"]})
            chi0 = CT.chi_statico(mot, Z["st"], Z["par"], P, CT.Laplaciano(mot), m0)
            stati.append((0, {q: Z["st"][q].copy() for q in Z["chiavi"]}, np.array(C.campo.A, copy=True), np.abs(np.asarray(C.campo.E)), chi0, {"kappa": P.kappa, "s": P.s, "e0": P.e0, "m0": m0}, None))
            Z["metti"]()
        for f in fs:
            h = sha1(f)
            assert open(f + ".sha1", encoding="utf-8").read().split()[0] == h, "lo sha1 di %s NON coincide" % f
            with np.load(f) as z:
                meta = json.loads(str(z["meta"]))
                stati.append((int(meta["k"]), {q: z[q].copy() for q in Z["chiavi"]}, z["campo_A"].copy(), np.abs(z["campo_E"]), z["chi"].copy(), meta["parametri"], (os.path.basename(f), h, meta)))
        V = np.asarray(stati[-1][6][2]["centri"] if stati[-1][6] else info["centri"], dtype=float)
        if info is not None:
            for s_ in stati[1:]:
                assert [list(map(int, v)) for v in s_[6][2]["centri"]] == [list(map(int, v)) for v in info["centri"]], "i vertici del k 0 ricostruito NON sono quelli della corsa: FERMO"
                assert s_[5]["m0"] == stati[0][5]["m0"], "m0 ricostruito %r contro %r della corsa" % (stati[0][5]["m0"], s_[5]["m0"])
        G0 = (float(V[:, 0].mean()), float(V[:, 1].mean()))
        xyn = TO.scarti(m1, m2, G0[0], G0[1], L)[:, :2]
        angn = np.degrees(np.arctan2(xyn[:, 1], xyn[:, 0]))
        xyv = np.array([TO.scarti(np.array([v[0]]), np.array([v[1]]), G0[0], G0[1], L)[0, :2] for v in V])
        angv = np.degrees(np.arctan2(xyv[:, 1], xyv[:, 0]))
        sett = [np.abs(((angn - angv[j]) + 180.0) % 360.0 - 180.0) < 60.0 for j in range(3)]
        for k, dati, A, absE, chi, pm, chiave in stati:
            rho = np.bincount(nodo, weights=np.sum(np.abs(dati["psi_h"]) ** 2, axis=1), minlength=n)
            bari = np.array([(xyn[s_] * rho[s_][:, None]).sum(axis=0) / rho[s_].sum() for s_ in sett])
            mass = np.array([xyn[np.nonzero(s_)[0][int(np.argmax(rho[s_]))]] for s_ in sett])
            Z["metti"](dati)
            cam.A[...] = A
            N = np.exp(-float(pm["kappa"]) * chi)
            mot.cs = float(pm["s"]) * N
            mot.lambda_c = None
            CT.fase_a(mot, Z["st"], float(pm["e0"]), N)
            U1.scrivi_U(mot, cam)
            m = cam.m
            prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
            sp(Z["st"], Z["par"], 0.5)
            J = np.sum(np.abs(Z["st"]["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
            Z["metti"]()
            mot.cs = cs_scena
            mot.lambda_c = None
            Jn = (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)
            sfx = "_%06d" % k
            D["rho" + sfx], D["chi" + sfx] = rho.astype(np.float32), np.asarray(chi).astype(np.float32)
            D["Jx" + sfx], D["Jy" + sfx], D["J" + sfx], D["absE" + sfx] = Jn[:, 0].astype(np.float32), Jn[:, 1].astype(np.float32), J.astype(np.float32), np.asarray(absE).astype(np.float32)
            D["centri_bari" + sfx], D["centri_max" + sfx] = bari.astype(np.float32), mass.astype(np.float32)
            ks.append(k)
            print("    k %6d %s: la somma di J_a %+.3e; |J| per nodo il massimo %.4e; i centri (baricentri di rho, dal G0) %s; (rho massimo) %s" % (
                k, ("%s sha1 %s" % (chiave[0], chiave[1][:8])) if chiave else "(ricostruito)", float(J.sum()), float(np.max(np.hypot(Jn[:, 0], Jn[:, 1]))),
                [["%.3f" % q for q in c] for c in bari], [["%.1f" % q for q in c] for c in mass]))
    D.update(k=np.array(ks, dtype=np.int32), L=np.array(L), ii=nodo[0::2].astype(np.int32), jj=nodo[1::2].astype(np.int32), m1=m1.astype(np.float32), m2=m2.astype(np.float32),
             x=xy[:, 0].astype(np.float32), y=xy[:, 1].astype(np.float32), vertici=V.astype(np.int32), G0=np.array(G0, dtype=np.float32), quale=np.array(x.quale))
    os.makedirs(os.path.dirname(x.out) or ".", exist_ok=True)
    np.savez_compressed(x.out, **D)
    sz = os.path.getsize(x.out)
    print("### %s: %.2f MB; %d stati (k %s); i vertici %s; G0 %s" % (x.out, sz / 1e6, len(ks), ks, V.astype(int).tolist(), ["%.3f" % q for q in G0]))
    assert sz <= TETTO, "sopra i 50 MB: FERMO"
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
