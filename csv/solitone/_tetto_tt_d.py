# -*- coding: utf-8 -*-
r"""**`TT-D` E `TT-F`, LA CURA DEL TETTO DI `Omega` SUL CODICE CURATO** *(il task history `doc/TASK_HISTORY/2026-11-07_cura_tetto_omega.md`, sez. `6.4`)*: [[TETTO-OMEGA-SENZA-ARROTONDAMENTO]]

    python csv/solitone/_tetto_tt_d.py > doc/referti_l2/tetto_omega_tt_d.txt

- **`TT-D`** *(DEVE PASSARE)*: **la carta IS3** *(`carta_statiche.cs_onde`)* **col controllo curato:** ### **l'eccesso massimo in unita' di `u tetto_k` sta sotto la tolleranza**
  *(`ulp_del_tetto(6) / u`, `~27`)* **e IS3 gira OLTRE l'`assert` del tetto** *(se si ferma per un'ALTRA ragione, si stampa)*.
- **`TT-F`** *(DEVE FALLIRE)*: **la scala vecchia di `7395cd9a`** *(solo il nodo; la COPIA dichiarata di `csv/_tolleranza_omega.py`, `Q7`, con la firma nuova)* **messa APPOSTA sulla scena
  di `C5` a `Lambda_c = 0.8`:** ### **il controllo curato ALZA**, e **l'eccesso in unita' di `u tetto`** si stampa.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

U = float(np.finfo(float).eps) / 2.0
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def main():
    import _presidio
    _presidio.avvia(__file__)
    import energia_pesata as EP
    _presidio.avvia(EP.__file__)
    from solitone import carta_statiche as CS
    originale = EP.controlla_tetto
    reg = []

    def avvolto(omega_k, tetto_k, grado_max, dove):
        r = (np.abs(omega_k) - tetto_k) / (U * np.where(tetto_k > 0.0, tetto_k, np.inf))
        reg.append((dove, float(np.max(r)), int(grado_max)))
        return originale(omega_k, tetto_k, grado_max, dove)
    print("=" * 130)
    print("TT-D, TT-F: la tolleranza a grado 6 = %.6f u (u = eps/2 = %.3e)" % (EP.ulp_del_tetto(6) / U, U))
    print("=" * 130)
    print("### TT-D: la carta IS3 col controllo curato")
    EP.controlla_tetto = avvolto
    err = None
    try:
        CS.cs_onde()
    except Exception as e:      # ### una misura: si stampa chi ferma IS3, qualunque sia
        err = "%s: %s" % (type(e).__name__, str(e)[:300])
    finally:
        EP.controlla_tetto = originale
    tol = EP.ulp_del_tetto(6) / U
    rmax = max(x[1] for x in reg) if reg else float("nan")
    print("  %d chiamate di controlla_tetto; i gradi %s; l'eccesso massimo %.3f u tetto_k; la sopra zero %d; IS3 %s"
          % (len(reg), sorted({x[2] for x in reg}), rmax, sum(1 for x in reg if x[1] > 0.0), "si ferma: " + err if err else "arriva in fondo"))
    esito("DEVE PASSARE: TT-D l'eccesso massimo sulla scena di IS3 entro la tolleranza (%.3f u)" % tol, bool(reg) and rmax <= tol, "%.3f u" % rmax)
    esito("DEVE PASSARE: TT-D IS3 non si ferma sul controllo del tetto", not (err and "TETTO di `Omega`" in err), err[:120] if err else "")
    print("### TT-F: la scala VECCHIA di 7395cd9a (solo il nodo) messa APPOSTA sulla scena di C5 a Lambda_c 0.8 (la copia di _tolleranza_omega.q7, con la firma nuova)")
    import _tolleranza_omega as TO_
    vero_tetto = EP.tetto_omega
    scatto = {"si": False, "r": 0.0}

    def tetto_vecchio(mot, st, par):
        lam = EP._per_nodo(mot, np.abs(st["phi_h"]) ** 2, np.empty(mot.inc.n))
        psi = st["psi_h"]
        rho = EP._per_nodo(mot, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2, np.empty(mot.inc.n))
        csp = EP.cs_primo(lam, mot.lambda_c, np.empty(mot.inc.n))
        return np.full(mot.inc.n, float(np.max(np.abs(csp) * EP.OMEGA_H * (lam + rho))))

    def controlla(om, tt, g, dove):
        scatto["r"] = max(scatto["r"], float(np.max((np.abs(om) - tt) / (U * tt))))
        try:
            originale(om, tt, g, dove)
        except AssertionError:
            scatto["si"] = True
            raise
    EP.tetto_omega, EP.controlla_tetto = tetto_vecchio, controlla
    try:
        msg = TO_._corsa_c5(0.8, EP.applica)
    finally:
        EP.tetto_omega, EP.controlla_tetto = vero_tetto, originale
    esito("DEVE FALLIRE: TT-F con la scala VECCHIA il controllo curato NON alza", scatto["si"], "l'eccesso %.3e u tetto; %s" % (scatto["r"], msg or "### nessuno ha alzato"))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
