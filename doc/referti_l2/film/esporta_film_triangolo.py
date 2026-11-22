# -*- coding: utf-8 -*-
r"""**IL FILM LEGGERO DEI DUE TRONCHI DEL TRIANGOLO** *(la richiesta di Luca `2026-11-22` `03:21`: sola lettura, nessuna corsa toccata; la copia nuova di `esporta_film.py` del ramo `mitosi-chi`, `8da155e5`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/film/esporta_film_triangolo.py --quale t120 --fino 2000 --out doc/referti_l2/film/triangolo_t120.npz
    E:\python\py3132\python.exe doc/referti_l2/film/esporta_film_triangolo.py --quale t120r28 --fino 2000 --out doc/referti_l2/film/triangolo_t120r28.npz

**Gli stati:** `k 0` RICOSTRUITO con `triangolo_chi_v3.prepara` *(nessun tick: il tronco non salva `k 0`; `chi` al profilo statico, `E` da Gauss, come all'avvio del tronco; i vertici confrontati col `meta` degli stati salvati)*, poi **ogni stato salvato** di `CHI/triangolo/<quale>` fino a `--fino`, ciascuno con lo sha1 controllato. **Per stato:** `rho` per nodo *(dalle estremita', come `esporta_film`)*, `chi` per nodo, **`|E|` per ARCO** *(`campo_E`, il valore assoluto: il campo vive sugli archi)*. **Una volta:** gli archi `ii`, `jj` *(dal motore della scena di S162)*, le posizioni del disegno `m1`, `m2` *(il punto e' `m1 a1 + m2 a2`)*, i tre vertici. **`float32`** *(gli indici `int32`)*, compresso; **sopra `50 MB` si ferma** *(nessun dimezzamento previsto qui: a mano circa `0.5 MB` per stato)*.
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
    _presidio.avvia(__file__)
    import chi_tick as CT
    import chi_tick_v2 as CV2
    ap = argparse.ArgumentParser()
    ap.add_argument("--quale", choices=T3.QUALI, required=True)
    ap.add_argument("--fino", type=int, required=True)
    ap.add_argument("--out", required=True)
    x = ap.parse_args(argv)
    d = os.path.join(T3.BASE, x.quale)
    fs = sorted((f for f in glob.glob(os.path.join(d, "stato_*.npz")) if os.path.exists(f + ".sha1") and int(os.path.basename(f)[6:-4]) <= x.fino), key=lambda f: int(os.path.basename(f)[6:-4]))
    assert fs and int(os.path.basename(fs[-1])[6:-4]) == x.fino, "lo stato di k %d non c'e' ancora" % x.fino
    MT = T3.moduli()[0]
    D = {}
    with T3.scena() as Z:
        mot = Z["mot"]
        n = mot.inc.n
        nodo = np.asarray(mot.inc.nodo, dtype=np.int64)
        L = Z["L"]
        C, info = T3.prepara(Z, x.quale)
        P, m0 = CV2.parametri_v2(Z, None, None, MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0, float(Z["s"]), float(C.e0), stato={q: Z["st"][q].copy() for q in Z["chiavi"]})
        chi0 = CT.chi_statico(mot, Z["st"], Z["par"], P, CT.Laplaciano(mot), m0)
        rho0 = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
        E0 = np.abs(np.asarray(C.campo.E))
        Z["metti"]()
    ks = [0]
    D["rho_%06d" % 0], D["chi_%06d" % 0], D["absE_%06d" % 0] = rho0.astype(np.float32), chi0.astype(np.float32), E0.astype(np.float32)
    for f in fs:
        h = sha1(f)
        assert open(f + ".sha1", encoding="utf-8").read().split()[0] == h, "lo sha1 di %s NON coincide" % f
        with np.load(f) as z:
            meta = json.loads(str(z["meta"]))
            assert [list(map(int, v)) for v in meta["centri"]] == [list(map(int, v)) for v in info["centri"]], "i vertici del k 0 ricostruito NON sono quelli della corsa: FERMO"
            assert abs(meta["parametri"]["m0"] - m0) == 0.0, "m0 ricostruito %r contro %r della corsa" % (m0, meta["parametri"]["m0"])
            k = int(meta["k"])
            rho = np.bincount(nodo, weights=np.sum(np.abs(z["psi_h"]) ** 2, axis=1), minlength=n)
            D["rho_%06d" % k] = rho.astype(np.float32)
            D["chi_%06d" % k] = z["chi"].astype(np.float32)
            D["absE_%06d" % k] = np.abs(z["campo_E"]).astype(np.float32)
        ks.append(k)
        print("    %s sha1 %s: k %d" % (os.path.basename(f), h[:8], k))
    v = np.arange(n)
    D.update(k=np.array(ks, dtype=np.int32), L=np.array(L), ii=nodo[0::2].astype(np.int32), jj=nodo[1::2].astype(np.int32),
             m1=(v // L).astype(np.float32), m2=(v % L).astype(np.float32), vertici=np.array(info["centri"], dtype=np.int32), quale=np.array(x.quale))
    os.makedirs(os.path.dirname(x.out) or ".", exist_ok=True)
    np.savez_compressed(x.out, **D)
    sz = os.path.getsize(x.out)
    print("### %s: %.2f MB; %d stati (k %s); i vertici %s; m0 %+.12e (il k 0 ricostruito = quello della corsa: AL BIT)" % (x.out, sz / 1e6, len(ks), ks, info["centri"], m0))
    assert sz <= TETTO, "sopra i 50 MB: FERMO"
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
