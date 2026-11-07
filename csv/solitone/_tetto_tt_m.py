# -*- coding: utf-8 -*-
r"""**`TT-M`, LA MISURA DELL'ECCESSO SUL TETTO DI `Omega`** *(Luca `2026-11-07` `10:06`, la decisione `1`; il task history `doc/TASK_HISTORY/2026-11-07_cura_tetto_omega.md`, sez. `2`)*: [[TETTO-OMEGA-SENZA-ARROTONDAMENTO]]

    python csv/solitone/_tetto_tt_m.py > doc/referti_l2/tetto_omega_tt_m.txt

### **Solo misura, PRIMA della cura:** gira la carta IS3 *(`carta_statiche.cs_onde`, la scena del suo referto)* **con `energia_pesata.controlla_tetto` AVVOLTO** *(l'originale chiamato
dentro, invariato: la dinamica non cambia, e l'`assert` alza come prima)*: **per ogni chiamata** `(|Omega_k| - tetto_k) / (u tetto_k)` *(`u = eps / 2`)*, **il massimo, il nodo**;
**dove l'eccesso e' positivo:** `nrm_phi`, `pu_phi`, i rapporti `|per_nodo| / tn` e `|arco| / ta` del nodo *(la premessa `3`: il tetto ESATTO dove `pu_phi = 0` e le fasi sono opposte)*.
### ⚠ **Dichiarato:** l'avvolgimento legge lo stato dal frame di `applica` *(`mot`, `st`, `par`)*: **e' una misura, non un sigillo.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

U = float(np.finfo(float).eps) / 2.0
CHIAMATE = []


def main():
    import _presidio
    _presidio.avvia(__file__)
    import energia_pesata as EP
    _presidio.avvia(EP.__file__)
    from solitone import carta_statiche as CS
    originale = EP.controlla_tetto

    def avvolto(omega_k, tetto_k, dove):
        r = (np.abs(omega_k) - tetto_k) / (U * np.where(tetto_k > 0.0, tetto_k, np.inf))
        k = int(np.argmax(np.abs(omega_k) - tetto_k))
        ecc = float(np.abs(omega_k[k]) - tetto_k[k])
        rec = {"dove": dove, "ecc": ecc, "k": k, "r_max": float(np.max(r)), "tetto_k": float(tetto_k[k]), "tetto_max": float(np.max(tetto_k)), "n_pos": int(np.sum(np.abs(omega_k) - tetto_k > 0.0))}
        if ecc > 0.0:
            fr = sys._getframe(1).f_locals
            mot, st, par = fr["mot"], fr["st"], fr["par"]
            pn, pa = EP.termini_di_h(mot, st, par)
            tn = mot._b("ep_tetto_nodo", (mot.inc.n,), float).copy()
            ta = mot._b("ep_tetto_arco", (mot.inc.m,), float).copy()
            nrm_phi = mot._b("ep_nrm_phi", (mot.inc.n,), float).copy()
            S_phi = np.zeros(mot.inc.n, dtype=complex)
            np.add.at(S_phi, mot.inc.nodo, st["phi_h"])
            est = np.flatnonzero(np.asarray(mot.inc.nodo) == k)
            archi = est // 2
            w = st["phi_h"].reshape(mot.inc.m, 2)
            cosr = [float(np.real(np.conj(w[a, 0]) * w[a, 1]) / (abs(w[a, 0]) * abs(w[a, 1]))) if abs(w[a, 0]) * abs(w[a, 1]) > 0 else float("nan") for a in archi]
            rec.update({"nrm_phi": float(nrm_phi[k]), "pu_phi": float(abs(S_phi[k]) ** 2 / mot.inc.grado[k]), "pn_su_tn": float(abs(pn[k]) / tn[k]) if tn[k] > 0 else float("nan"),
                        "pa_su_ta": [float(abs(pa[a]) / ta[a]) if ta[a] > 0 else float("nan") for a in archi], "cos_arco": cosr, "psi_max": float(np.max(np.abs(st["psi_h"])))})
        CHIAMATE.append(rec)
        return originale(omega_k, tetto_k, dove)
    EP.controlla_tetto = avvolto
    errore = None
    try:
        CS.cs_onde()
    except AssertionError as e:
        errore = str(e)
    finally:
        EP.controlla_tetto = originale
    print("=" * 130)
    print("TT-M: %d chiamate di controlla_tetto; u = eps/2 = %.3e; l'assert %s" % (len(CHIAMATE), U, "ALZA: " + errore[:160] if errore else "NON alza"))
    if CHIAMATE:
        rm = max(c["r_max"] for c in CHIAMATE)
        print("  il massimo su tutte le chiamate di (|Omega_k| - tetto_k) / (u tetto_k): %.3f; le chiamate con eccesso > 0: %d" % (rm, sum(1 for c in CHIAMATE if c["ecc"] > 0.0)))
        for i, c in enumerate(CHIAMATE):
            if c["ecc"] > 0.0 or i < 3 or i == len(CHIAMATE) - 1:
                print("  #%d %s: eccesso %.3e al nodo %d (tetto_k %.6e, il tetto massimo %.6e), in u tetto_k %.3f; nodi sopra %d" % (i, c["dove"], c["ecc"], c["k"], c["tetto_k"], c["tetto_max"], c["r_max"], c["n_pos"]))
                if "nrm_phi" in c:
                    print("     nrm_phi %.17e pu_phi %.3e |per_nodo|/tn %.17f; gli archi del nodo |arco|/ta %s cos(fase relativa) %s; max|psi| %.3e"
                          % (c["nrm_phi"], c["pu_phi"], c["pn_su_tn"], ["%.17f" % x for x in c["pa_su_ta"]], ["%+.6f" % x for x in c["cos_arco"]], c["psi_max"]))
    print("ESITO: misura, nessun verdetto (la lettura nel task history della cura)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
