# -*- coding: utf-8 -*-
r"""**I GIRI DEL PUNTO FISSO DEL LAPSE: BASTANO 2 O 3?** *(Luca `2026-11-15` `14:23`; SOLO LETTURA, nessun codice del simulatore cambiato)*.

    python csv/solitone/giri_lapse.py > doc/referti_l2/mattone/giri_lapse.txt

### **(1) dal codice:** **il numero di giri NON e' fisso: `tick_lapse.cs_al_centro` itera finche' `max |nuovo - prec| <= EPS_CS max |nuovo|`, `EPS_CS = 8 eps`** *(`primo_ordine/tick.py`, il nucleo)*, **al piu' `GIRI_MAX = 120`.**
### **(2)** **il mattone di `L 162`** *(`L162_MGU_03000`, `U` dal campo)* **da solo nella scena di S162, il bordo da `R_A 60`, G+U, `20` tick col tick di `mattone.Campi`.** **In ogni tick:** **il `cs` di OGNI giro** *(una copia di
`cs_al_centro` riga per riga che li tiene, e che si puo' FERMARE al giro `g`: in memoria, come `lapse_caldo.py`)*; **la differenza `max |cs_g - cs_finale|` sui nodi, assoluta e relativa a `max |cs_finale|`; e lo stato DOPO il tick se ci si fosse
fermati al giro `g = 1, 2, 3`** *(lo stesso tick rifatto da una copia dello stato e del campo)* **contro quello vero: la differenza relativa per chiave** *(`max |a - b| / max |b|`; `h_int` esclusa)*. **La corsa prosegue sempre con il tick VERO.**
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402
from solitone import tick_lapse as TL  # noqa: E402

N_TICK = 20
CHIAVI = ("psi_h", "phi_h", "rho", "Lambda", "campo_E", "campo_A")
_ORIG = TL.cs_al_centro
REG = {"cs": [], "ferma": None, "giri": None}


def cs_al_centro_giri(mot, st, par, s, legge, senza_reazione, omega=1.0, giri_max=None, storia=None):
    """### **`tick_lapse.cs_al_centro` riga per riga**; tiene il `cs` di ogni giro; se `REG["ferma"]` e' `g`, rende il `cs` del giro `g`."""
    TK = TL.TK
    meta = TK.meta_del_palindromo()
    prec = TL.cs_di(mot, st, s, legge)
    REG["cs"] = []
    for giri in range(1, (TK.GIRI_MAX if giri_max is None else giri_max) + 1):
        copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
        mot.cs = prec
        mot.lambda_c = None
        if not senza_reazione:
            TL.reazione(mot, copia, par, s, legge, 0.5)
        TK.percorri_tick(copia, mot, par, (), None, meta)
        nuovo = TL.cs_di(mot, copia, s, legge)
        REG["cs"].append(nuovo.copy())
        scarto = float(np.max(np.abs(nuovo - prec)))
        if storia is not None:
            storia.append(scarto)
        if REG["ferma"] == giri:
            REG["giri"] = giri
            return nuovo, giri
        if scarto <= TK.EPS_CS * float(np.max(np.abs(nuovo))):
            REG["giri"] = giri
            return nuovo, giri
        prec = nuovo if omega == 1.0 else prec + omega * (nuovo - prec)
    raise AssertionError("il punto fisso NON converge in %d giri" % giri)


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    for m in ("mattone", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_QUI, "tick_lapse.py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    t_s = int(ct["t"])
    print("=" * 130)
    print("I GIRI DEL PUNTO FISSO DEL LAPSE (Luca 14:23): %s da solo nella scena di S162, il bordo da R_A %g, G+U, %d tick" % (ct["file"], MTR.R_A_SCENA, N_TICK))
    print("### (1) DAL CODICE: NON un numero fisso: tick_lapse.cs_al_centro si ferma a max|nuovo - prec| <= EPS_CS max|nuovo|, EPS_CS = %.3e (8 eps, primo_ordine/tick.py), al piu' GIRI_MAX = %d" % (TL.TK.EPS_CS, TL.TK.GIRI_MAX))
    print("=" * 130)
    TL.cs_al_centro = cs_al_centro_giri
    try:
        with MT.scena(MT.CORSA_162, MT.T_162) as Z:
            c0 = Z["bordo"]["c0"]
            Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
            with np.load(ct["file"]) as d:
                Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
                A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
            C = MT.Campi(Z, "MGU", rho_c, e)
            C.campo.A[...] = A0
            C.campo.E[...] = E0
            C.campo.e = e
            C.e_prec = e
            U1.scrivi_U(Z["mot"], C.campo)

            def foto():
                out = {x: Z["st"][x].copy() for x in Z["chiavi"]}
                out.update(campo_A=C.campo.A.copy(), campo_E=C.campo.E.copy(), U=Z["mot"].geo.U.copy())
                return out

            def rimetti(f):
                for x in Z["chiavi"]:
                    Z["st"][x][...] = f[x]
                C.campo.A[...] = f["campo_A"]
                C.campo.E[...] = f["campo_E"]
                Z["mot"].geo.U[...] = f["U"]
            TAB = {g: {x: [] for x in CHIAVI} for g in (1, 2, 3)}
            DCS = {g: [] for g in (1, 2, 3, 4)}
            GIRI = []
            for k in range(1, N_TICK + 1):
                prima = foto()
                ep = C.e_prec
                REG["ferma"] = None
                C.tick(k, t_s + k, 1.0, e)
                vero = foto()
                css = list(REG["cs"])
                GIRI.append(REG["giri"])
                fin = css[-1]
                den = float(np.max(np.abs(fin)))
                riga = []
                for g in range(1, len(css) + 1):
                    dg = float(np.max(np.abs(css[g - 1] - fin)))
                    if g <= 4:
                        DCS[g].append((dg, dg / den))
                    riga.append("g%d %.3e (%.3e)" % (g, dg, dg / den))
                tr = []
                for g in (1, 2, 3):
                    if g >= len(css):
                        continue
                    rimetti(prima)
                    C.e_prec = ep
                    REG["ferma"] = g
                    C.tick(k, t_s + k, 1.0, e)
                    alt = foto()
                    for x in CHIAVI:
                        den_x = float(np.max(np.abs(vero[x]))) or 1.0
                        TAB[g][x].append(float(np.max(np.abs(alt[x] - vero[x]))) / den_x)
                    tr.append("fermo a %d: psi_h %.2e rho %.2e campo_E %.2e" % (g, TAB[g]["psi_h"][-1], TAB[g]["rho"][-1], TAB[g]["campo_E"][-1]))
                rimetti(vero)
                C.e_prec = e
                REG["ferma"] = None
                print("    k %2d: %d giri; |cs_g - cs_finale| (relativo): %s; lo stato dopo il tick: %s" % (k, GIRI[-1], "; ".join(riga), "; ".join(tr)))
                sys.stdout.flush()
            Z["metti"]()
    finally:
        TL.cs_al_centro = _ORIG
    print("-" * 130)
    print("### I GIRI per tick: %s" % sorted(set(GIRI)))
    print("### |cs_g - cs_finale|, il massimo sui %d tick (assoluto, relativo a max|cs|):" % N_TICK)
    for g in (1, 2, 3, 4):
        if DCS[g]:
            print("    giro %d: %.3e, %.3e" % (g, max(x[0] for x in DCS[g]), max(x[1] for x in DCS[g])))
    print("### LO STATO DOPO IL TICK se ci si fosse fermati al giro g, contro quello vero (4 giri): la differenza relativa per chiave, il massimo sui %d tick" % N_TICK)
    print("    %-8s %s" % ("fermo a", " ".join("%11s" % x for x in CHIAVI)))
    for g in (1, 2, 3):
        if TAB[g]["psi_h"]:
            print("    giro %-3d %s" % (g, " ".join("%11.3e" % max(TAB[g][x]) for x in CHIAVI)))
    print("    (il riferimento: l'arrotondamento di un tick e' dell'ordine di 1e-15 - 1e-13; la differenza fra la partenza a caldo e a freddo dopo 200 tick: campo_E 4.0e-12, psi_h 1.2e-14, prova_caldo.txt)")
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
