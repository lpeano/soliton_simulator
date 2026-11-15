# -*- coding: utf-8 -*-
r"""**D2: IL MOTORE NUMBA, FUNZIONE PER FUNZIONE, AL BIT** *(Luca `2026-11-15` `18:08`, N1; la carta `doc/TASK_HISTORY/2026-11-15_motore_numba.md`)*.

    E:\python\py3132\python.exe csv/solitone/prova_numba_d2.py > doc/referti_l2/motore_numba_d2.txt     (NUMBA_CACHE_DIR su E:, PYTHONNOUSERSITE=1, TMP su E:)

**Nella scena di S162 col mattone di `L 162`** *(`L162_MGU_03000`)*:
- **(a) il ciclo `motore_numba.add_at` contro `np.add.at`:** **su `inc.nodo` vero, `v` reali `(2m,)` e complessi `(2m, 2)` e `(2m,)`** *(lo stato vero e numeri casuali, `fuori` che parte da zero e da numeri casuali)*; **a `1` filo e a `6`: AL BIT;**
- **(b) le funzioni del tick sullo stesso stato, switch spento contro acceso:** **`energia_pesata.termini_di_h`** *(`per_nodo`, `per_arco`)*, **`Motore.elicita`, `densita_materia`, `densita_vuoto`, `_somma_per_nodo`: AL BIT;**
- **(c) i ripieghi del ciclo** *(quante chiamate sono passate dal numpy di oggi)*; **i tempi** *(la prima chiamata, cioe' la compilazione, A PARTE: N6)*.
### **DEVE PASSARE: (a) e (b) AL BIT.** **Se no: scritto il perche'** *(N1)*.
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

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  DEVE PASSARE: %-100s %s   %s" % (che[:100], "PASSA" if passa else "### FALLISCE", nota))
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
    print("D2, IL MOTORE NUMBA FUNZIONE PER FUNZIONE (Luca 18:08, N1): %s; sys.executable %s; NUMBA_CACHE_DIR %s" % (ct["file"], sys.executable, os.environ.get("NUMBA_CACHE_DIR")))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        import motore_numba as MN
        import energia_pesata as EP
        print("### dopo l'import di motore_numba a switch spento: 'numba' in sys.modules = %s (D1: deve essere False)" % ("numba" in sys.modules))
        esito("a switch spento numba NON importato (D1)", "numba" not in sys.modules, "")
        with np.load(ct["file"]) as d:
            Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
            A0 = d["campo_A"].copy()
        C = MT.Campi(Z, "MGU", rho_c, e)
        C.campo.A[...] = A0
        U1.scrivi_U(Z["mot"], C.campo)
        mot, st, par = Z["mot"], Z["st"], Z["par"]
        nodo = np.asarray(mot.inc.nodo)
        n = mot.inc.n
        rng = np.random.default_rng(11)
        psi, phi = st["psi_h"].copy(), st["phi_h"].copy()
        casi = [("reale (2m,) |psi|^2", np.sum(np.abs(psi) ** 2, axis=1), (n,), float),
                ("complesso (2m, 2) psi", psi, (n, 2), complex),
                ("complesso (2m,) phi", phi, (n,), complex),
                ("reale (2m,) casuale", rng.standard_normal(len(nodo)), (n,), float),
                ("complesso (2m, 2) casuale", rng.standard_normal((len(nodo), 2)) + 1j * rng.standard_normal((len(nodo), 2)), (n, 2), complex)]
        import motore as MO
        orig = {nome: (getattr(MO.Motore, nome) if mod == "motore" else getattr(EP, nome)) for mod, _c, nome in MN.SOSTITUITE}
        t_c = time.time()
        info = MN.accendi_numba(1)
        cambiate = all((getattr(MO.Motore, nome) if mod == "motore" else getattr(EP, nome)) is not orig[nome] for mod, _c, nome in MN.SOSTITUITE)
        esito("W1: a switch acceso le %d funzioni SOSTITUITE (non gli stessi oggetti)" % len(MN.SOSTITUITE), cambiate, "")
        print("### accendi_numba(1): %s" % info)
        a0 = np.zeros((n,))
        MN.add_at(a0, nodo, np.ones(len(nodo)))
        print("### la prima chiamata (la compilazione o la cache): %.2f s (N6: esclusa dai tempi)" % (time.time() - t_c))
        for fili in (1, 6):
            MN.accendi_numba(fili)
            for nome, v, forma, tipo in casi:
                for partenza in ("zero", "casuale"):
                    f0 = np.zeros(forma, dtype=tipo) if partenza == "zero" else (rng.standard_normal(forma) + (1j * rng.standard_normal(forma) if tipo is complex else 0)).astype(tipo)
                    a, b = f0.copy(), f0.copy()
                    np.add.at(a, nodo, v)
                    MN.add_at(b, nodo, v)
                    esito("(a) add_at = np.add.at AL BIT: %s, fuori da %s, %d fili" % (nome, partenza, fili), np.array_equal(a, b) and np.array_equal(np.signbit(a.real), np.signbit(b.real)),
                          "max |diff| %.3e" % float(np.max(np.abs(a - b))))
        # ---------------------------------------------------------------- (b) le funzioni del tick
        MN.spegni()
        rimesse = all((getattr(MO.Motore, nome) if mod == "motore" else getattr(EP, nome)) is orig[nome] for mod, _c, nome in MN.SOSTITUITE)
        esito("W1: spegni() rimette gli oggetti funzione ORIGINALI (is)", rimesse, "")
        esito("W1: spegni() toglie _MN_add_at dai moduli", "_MN_add_at" not in MO.__dict__ and "_MN_add_at" not in EP.__dict__, "")

        def leggi():
            pn, pa = EP.termini_di_h(mot, st, par)
            out = {"termini_di_h.per_nodo": pn.copy(), "termini_di_h.per_arco": pa.copy(), "elicita": mot.elicita(st).copy(),
                   "densita_materia": mot.densita_materia(st).copy(), "densita_vuoto": mot.densita_vuoto(st).copy()}
            f = np.zeros((n, 2), dtype=complex)
            out["_somma_per_nodo"] = mot._somma_per_nodo(st["psi_h"], f).copy()
            return out
        spento = leggi()
        for fili in (1, 6):
            MN.accendi_numba(fili)
            c0 = MN._STATO["chiamate"]
            acceso = leggi()
            print("### (b) a %d fili: le chiamate del ciclo %d, i ripieghi %d" % (fili, MN._STATO["chiamate"] - c0, MN._STATO["ripieghi"]))
            for k in spento:
                esito("(b) %s: switch acceso (%d fili) = spento AL BIT" % (k, fili), np.array_equal(spento[k], acceso[k]), "max |diff| %.3e" % float(np.max(np.abs(spento[k] - acceso[k]))))
            MN.spegni()
        # ---------------------------------------------------------------- (c) i tempi
        print("-" * 130)
        print("### (c) I TEMPI di np.add.at contro add_at (la compilazione esclusa; la macchina CARICA)")
        for fili in (1, 6):
            MN.accendi_numba(fili)
            for nome, v, forma, tipo in casi[:3]:
                a = np.zeros(forma, dtype=tipo)
                t = time.perf_counter()
                for _r in range(20):
                    np.add.at(a, nodo, v)
                t_np = (time.perf_counter() - t) / 20
                t = time.perf_counter()
                for _r in range(20):
                    MN.add_at(a, nodo, v)
                t_nb = (time.perf_counter() - t) / 20
                print("    %d fili, %-26s np.add.at %.4f s, add_at %.4f s, il rapporto %.1f" % (fili, nome, t_np, t_nb, t_np / t_nb))
            MN.spegni()
        print("### lo stato: %s" % MN.stato())
        Z["metti"]()
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s" % (OK[0], OK[1], FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
