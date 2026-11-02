# -*- coding: utf-8 -*-
r"""**I TEST DELL'ACCENSIONE LENTA** *(il task history `2026-11-02_accensione_lenta`, `A1`, `A2` secondo la decisione (i) di Luca)*: ### **sulla scena di BG-F-0.15, dalla sua partenza.**"""
import numpy as np

from . import accensione as AC

TICK = 20                      # ### i tick dei confronti (la diagnostica di 25614c34)
TOLL_PSI_A2 = 1e-12            # ### A2: |psi - psi_avanza|/|psi| (la decisione (i); il task history, sez. 6-bis: cento volte la differenza misurata)
LAM_MEZZO = 0.5                # ### A0: un lam intermedio deve differire da entrambi
TOLL_ESATTO = 1e-9             # ### A7, A8: una retta esatta (l'arrotondamento del fit)


def _stato(z):
    return {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}


def _rimetti(z, A):
    for k, v in A.items():
        z["st"][k][...] = v


def gira(esito):
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import composizione as CM
    import tick as TK
    print("### L'ACCENSIONE LENTA (csv/solitone/accensione.py): la scena di BG-F-0.15 dalla partenza; TICK %d TOLL_PSI_A2 %g LAM_MEZZO %g" % (TICK, TOLL_PSI_A2, LAM_MEZZO))
    sol, vuoto, s = V.CORSE["BG-F-0.15"]
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        salvato = _stato(z)
        p0, _info = V.partenza(sol, z, phi0, pK, s)
        _rimetti(z, salvato)
        z["st"]["psi_h"][...] = p0
        A = _stato(z)
        R = {}
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in range(TICK):
                TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
            R["intero"] = _stato(z)
            _rimetti(z, A)
            for t in range(TICK):
                CL.avanza(z, phi0, 1)
            R["congelato"] = _stato(z)
            _rimetti(z, A)
            for t in range(TICK):
                AC.tick_acceso(z, 1.0)
            R["lam1"] = _stato(z)
            _rimetti(z, A)
            phi_bit = True
            for t in range(TICK):
                AC.tick_acceso(z, 0.0)
                phi_bit = phi_bit and z["st"]["phi_h"].tobytes() == phi0.tobytes()
            R["lam0"] = _stato(z)
            _rimetti(z, A)
            for t in range(TICK):
                AC.tick_acceso(z, LAM_MEZZO)
            R["mezzo"] = _stato(z)
            _rimetti(z, A)
    a1 = all(R["lam1"][k].tobytes() == R["intero"][k].tobytes() for k in A)
    esito("DEVE PASSARE: A1 con lam = 1 il tick dell'accensione e' il tick intero (tick.percorri_tick) AL BIT, %d tick, ogni chiave" % TICK, a1,
          "chiavi diverse: %s" % ([k for k in A if R["lam1"][k].tobytes() != R["intero"][k].tobytes()] or "nessuna"))
    dpsi = float(np.linalg.norm(R["lam0"]["psi_h"] - R["congelato"]["psi_h"]) / np.linalg.norm(R["congelato"]["psi_h"]))
    esito("DEVE PASSARE: A2 (la decisione (i)) con lam = 0 phi resta phi0 AL BIT a ogni tick, e psi = _congelato_lungo.avanza entro %g (%d tick)" % (TOLL_PSI_A2, TICK),
          phi_bit and R["lam0"]["phi_h"].tobytes() == R["congelato"]["phi_h"].tobytes() and dpsi <= TOLL_PSI_A2,
          "phi al bit %s; |dpsi|/|psi| %.2e (la causa: la rotazione di beta e il ritorno a phi0 nel congelato, un ulp sul modulo)" % (phi_bit, dpsi))
    d1 = float(np.linalg.norm(R["mezzo"]["psi_h"] - R["intero"]["psi_h"]))
    d0 = float(np.linalg.norm(R["mezzo"]["psi_h"] - R["congelato"]["psi_h"]))
    esito("DEVE FALLIRE: A0 con lam = %g psi coincide col tick intero o col congelato entro %g" % (LAM_MEZZO, TOLL_PSI_A2), not min(d1, d0) / float(np.linalg.norm(p0)) <= TOLL_PSI_A2,
          "|dpsi| dal tick intero %.3e, dal congelato %.3e" % (d1, d0))
    vite(esito)


def vite(esito):
    """### **`A7`, `A8`** *(Luca, dopo `bfee5330`)*: ### **la vita dal cuore a blocchi e il tempo dell'alone, su serie scritte a mano.**"""
    print("### LA VITA A BLOCCHI E L'ALONE (accensione.vita_a_blocchi, tempo_alone): serie a mano; TOLL_ESATTO %g" % TOLL_ESATTO)
    tau = np.arange(0.0, 10000.0, 0.5)
    f = 1.0 - tau / 20000.0
    v = AC.vita_a_blocchi(tau, f, 0.0)
    rif = 1.0 - 499.75 / 20000.0                     # ### la media del primo blocco (i campioni 0 .. 999.5)
    atteso = 0.25 + 20000.0 * (1.0 - 0.5 * rif)        # ### la retta delle medie contro i centri: 1 - (c - 0.25)/20000
    esito("DEVE PASSARE: A7 un cuore lineare: la vita estrapolata dalle medie a blocchi e' quella esatta (entro %g)" % TOLL_ESATTO,
          v["misurata"] is None and v["estrapolata"] is not None and abs(v["estrapolata"] / atteso - 1.0) <= TOLL_ESATTO,
          "estrapolata %s, attesa %.6f; il riferimento %.9f (atteso %.9f)" % (v["estrapolata"], atteso, v["rif"], rif))
    f = np.where(tau < 3000.0, 1.0, 0.3)
    v = AC.vita_a_blocchi(tau, f, 0.0)
    esito("DEVE PASSARE: A7-M un cuore che scende sotto meta' nel blocco 3000 .. 4000: misurata al suo centro, 3500", v["misurata"] == 3500.0, "misurata %s" % v["misurata"])
    t6 = np.arange(0.0, 6001.0, 1.5)
    bb = AC.medie_a_blocchi(t6, np.ones_like(t6), 1000.0)
    esito("DEVE PASSARE: A7-B i campioni fino a 6000 dal blocco 1000: 5 blocchi completi (6000 .. 7000 ha un campione solo, fuori)", len(bb) == 5,
          "blocchi %s" % [(a, b) for a, b, _m in bb])
    v = AC.vita_a_blocchi(tau, 0.5 + tau / 20000.0, 0.0)
    esito("DEVE FALLIRE: A7-F un cuore che SALE da' una vita (misurata o estrapolata)", not (v["misurata"] or v["estrapolata"]),
          "misurata %s estrapolata %s pendenza %+.4e" % (v["misurata"], v["estrapolata"], v["pendenza"]))
    t_a, p_a, mis = AC.tempo_alone(tau, 0.001 + 2.5e-6 * tau, 0.0, tau[-1], 0.1)
    esito("DEVE PASSARE: A8 un alone lineare 0.001 + 2.5e-3 per 1000: il 10%% a 39600 (entro %g)" % TOLL_ESATTO,
          not mis and t_a is not None and abs(t_a / 39600.0 - 1.0) <= TOLL_ESATTO, "tempo %s, pendenza %+.4e" % (t_a, p_a))
    t_a, p_a, mis = AC.tempo_alone(tau, 0.02 - 1e-6 * tau, 0.0, tau[-1], 0.1)
    esito("DEVE FALLIRE: A8-F un alone che CALA da' un tempo al 10%", t_a is None, "tempo %s, pendenza %+.4e" % (t_a, p_a))
