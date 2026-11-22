# -*- coding: utf-8 -*-
r"""**[M2357-T4] LO SBLOCCO DEL CASO NOTO VERO DEGLI ARCHI MATURI** *(la decisione di Luca delle `09:08` del `2026-11-22`; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `3`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/t4_sblocco.py > doc/referti_l2/t4_sblocco.txt

**I dati** *(le righe di `notte_m0428_v3.t4`)*: `CHI/mattone`, gli stati `250 ... 3000`; `|Theta|` a `k 3000`; `|d_i - d_j|` per arco con `d = dtau s exp(-kappa chi)`, la media sui `12` stati. **Il criterio di Luca:** il rango fra `|Theta|` e la media sui `1000` archi piu' maturi `>= 0.9`, **E** i `20` archi con la media piu' alta hanno `|Theta| >= 0.99 T20` *(`T20` il `20`-esimo `|Theta|` piu' alto)*. **DEVE FALLIRE** con il solo stato di `k 3000` al posto della media.
"""
import hashlib
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
CHI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI")
N_MATURI = 1000                   # ### Luca 09:08
SOGLIA_RANGO = 0.9                # ### Luca 09:08
ENTRO = 0.01                      # ### Luca 09:08: entro l'1% della soglia dei 20
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def rango(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def criterio(th, y):
    """### `(rango sui 1000, il minimo di |Theta| sui 20 scelti da y, T20, quanti dei 20 in comune, il rango su tutti)`."""
    m = np.argsort(th)[::-1][:N_MATURI]
    t20 = np.argsort(th)[::-1][:20]
    T20 = float(th[t20[-1]])
    s20 = np.argsort(y)[::-1][:20]
    return rango(th[m], y[m]), float(th[s20].min()), T20, len(set(t20.tolist()) & set(s20.tolist())), rango(th, y)


def main():
    import _presidio
    import prova_scatola5 as PS
    _presidio.avvia(os.path.join(_QUI, "notte_m0428_v3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2357-T4] LO SBLOCCO DEL CASO NOTO VERO (Luca 09:08): il rango sui %d archi piu' maturi >= %.1f E i 20 scelti dalla media con |Theta| >= %.2f T20; DEVE FALLIRE col solo k 3000" % (N_MATURI, SOGLIA_RANGO, 1.0 - ENTRO))
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
    print("### gli stati %d ... %d (%d; k 0 non salvato); gli archi %d; max |Theta| %.6f" % (ks[0], ks[-1], len(ks), len(th), float(th.max())))
    out = {}
    for nome, y in (("la media nel tempo", media), ("il solo stato di k 3000", uno)):
        r1000, mn, T20, comuni, rtutti = criterio(th, y)
        ok = r1000 >= SOGLIA_RANGO and mn >= (1.0 - ENTRO) * T20
        out[nome] = (ok, r1000, mn, T20)
        print("### %s: il rango sui %d piu' maturi %.6f (su tutti %.6f); T20 %.8f; il minimo di |Theta| sui 20 scelti %.8f = %.6f T20; in comune coi 20 piu' maturi %d su 20: %s" % (
            nome, N_MATURI, r1000, rtutti, T20, mn, mn / T20, comuni, "I DUE CONTROLLI PASSANO" if ok else "CADE"))
    esito("T4 CASO NOTO (Luca 09:08): la media, il rango sui 1000 >= 0.9 E i 20 scelti entro l'1%% di T20", out["la media nel tempo"][0], "(%.6f, %.6f T20)" % (out["la media nel tempo"][1], out["la media nel tempo"][2] / out["la media nel tempo"][3]))
    esito("T4 DEVE FALLIRE: col solo stato di k 3000 almeno uno dei due controlli cade", not out["il solo stato di k 3000"][0], "(%.6f, %.6f T20)" % (out["il solo stato di k 3000"][1], out["il solo stato di k 3000"][2] / out["il solo stato di k 3000"][3]))
    print("-" * 130)
    print("ESITO: %d/%d" % (sum(ok for _c, ok in ESITI), len(ESITI)))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
