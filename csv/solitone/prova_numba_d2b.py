# -*- coding: utf-8 -*-
r"""**D2 DEL SECONDO PASSO (W3): `_grover_mezzo`, `_hop_psi_mezzo`, `_ruota_attorno_a_n`** *(Luca `2026-11-15` `19:12`, W3; la carta `doc/TASK_HISTORY/2026-11-15_motore_numba.md`, sez. `12`)*.

    E:\python\py3132\python.exe csv/solitone/prova_numba_d2b.py > doc/referti_l2/motore_numba_d2b.txt     (NUMBA_CACHE_DIR su E:, PYTHONNOUSERSITE=1, TMP su E:)

**Nella scena di S162 col mattone di `L 162`** *(`L162_MGU_03000`, `U` dal campo)*: **per ognuna delle tre funzioni, la versione di oggi e quella del secondo passo sugli STESSI ingressi** *(copie dello stato vero; piu' un `psi` casuale)*,
**a `1` e a `6` fili: AL BIT, o la differenza relativa massima** *(N1: il perche' da scrivere)*. **I tempi** *(la compilazione a parte, N6)*.
"""
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402

RISULTATI = []


def confronta(nome, a, b):
    bit = bool(np.array_equal(a, b))
    den = float(np.max(np.abs(a))) or 1.0
    rel = float(np.max(np.abs(a - b))) / den
    RISULTATI.append((nome, bit, rel))
    print("  %-90s AL BIT %-5s la differenza relativa massima %.3e" % (nome[:90], bit, rel))
    sys.stdout.flush()


def main():
    import _presidio
    import _u1_prototipo as U1
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    print("=" * 130)
    print("D2 DEL SECONDO PASSO (Luca 19:12, W3): %s; sys.executable %s" % (ct["file"], sys.executable))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        import flussi_parziali as FP
        import motore as MO
        import motore_numba as MN
        with np.load(ct["file"]) as d:
            Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
            A0 = d["campo_A"].copy()
        C = MT.Campi(Z, "MGU", rho_c, e)
        C.campo.A[...] = A0
        U1.scrivi_U(Z["mot"], C.campo)
        mot, st = Z["mot"], Z["st"]
        rng = np.random.default_rng(5)
        psi0, phi0 = st["psi_h"].copy(), st["phi_h"].copy()
        psir = rng.standard_normal(psi0.shape) + 1j * rng.standard_normal(psi0.shape)
        ang0 = rng.uniform(-3.0, 3.0, psi0.shape[0])
        orig = {"g": FP._grover_mezzo, "h": FP._hop_psi_mezzo, "r": MO.Motore._ruota_attorno_a_n}

        def gira(fili):
            out = {}
            for nome_psi, p in (("psi vero", psi0), ("psi casuale", psir)):
                v = p.copy()
                FP._grover_mezzo(mot, v, 0.25)
                out["_grover_mezzo, " + nome_psi] = v
                v = p.copy()
                FP._hop_psi_mezzo(mot, v, 0.25)
                out["_hop_psi_mezzo, " + nome_psi] = v
                v, a = p.copy(), ang0.copy()
                mot._ruota_attorno_a_n(v, a)
                out["_ruota_attorno_a_n, " + nome_psi] = v
            v = phi0.copy()
            FP._grover_mezzo(mot, v.reshape(-1, 1), 0.25)
            out["_grover_mezzo, phi vero (2m, 1)"] = v
            return out
        oggi = gira(0)
        for fili in (1, 6):
            MN.accendi_numba(fili)
            t = time.time()
            MN.accendi_secondo_passo()
            gira(fili)
            print("### a %d fili: la prima chiamata (la compilazione o la cache) %.2f s" % (fili, time.time() - t))
            nuovo = gira(fili)
            for k in oggi:
                confronta("%s, %d fili" % (k, fili), oggi[k], nuovo[k])
            # ### i tempi: 10 ripetizioni ciascuna, oggi e numba
            for nome, fn in (("_grover_mezzo", lambda: FP._grover_mezzo(mot, psi0.copy(), 0.25)), ("_hop_psi_mezzo", lambda: FP._hop_psi_mezzo(mot, psi0.copy(), 0.25)),
                             ("_ruota_attorno_a_n", lambda: mot._ruota_attorno_a_n(psi0.copy(), ang0.copy()))):
                t = time.perf_counter()
                for _r in range(10):
                    fn()
                t_nb = (time.perf_counter() - t) / 10
                MN.spegni()
                t = time.perf_counter()
                for _r in range(10):
                    fn()
                t_np = (time.perf_counter() - t) / 10
                MN.accendi_numba(fili)
                MN.accendi_secondo_passo()
                print("    %d fili, %-20s oggi %.4f s, numba %.4f s, il rapporto %.2f (le copie dello stato comprese; la macchina CARICA)" % (fili, nome, t_np, t_nb, t_np / t_nb))
            MN.spegni()
        rimesse = FP._grover_mezzo is orig["g"] and FP._hop_psi_mezzo is orig["h"] and MO.Motore._ruota_attorno_a_n is orig["r"]
        print("### spegni() rimette le tre originali (is): %s" % rimesse)
        Z["metti"]()
    print("=" * 130)
    n_bit = sum(1 for _n, b, _r in RISULTATI if b)
    print("ESITO: %d su %d AL BIT; la differenza relativa massima fra quelli non al bit: %s" % (n_bit, len(RISULTATI), "%.3e" % max([r for _n, b, r in RISULTATI if not b]) if n_bit < len(RISULTATI) else "--"))
    return 0 if (n_bit == len(RISULTATI) and rimesse) else 1


if __name__ == "__main__":
    sys.exit(main())
