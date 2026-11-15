# -*- coding: utf-8 -*-
r"""**LE PROVE DELLA PARTENZA A CALDO** *(7-bis; Luca `2026-11-15` `12:04`, A2-A3; `12:09`: decide il rapporto dei giri; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.2`)*.

    python csv/solitone/prova_caldo.py --registro prova-caldo > <scratchpad>/prova_caldo.txt     (poi doc/referti_l2/mattone/prova_caldo.txt)

**Il mattone di `L 162`** *(`L162_MGU_03000`, `U` dal campo)* **da solo nella scena di S162, il bordo da `R_A 60`, G+U, il tick di `mattone.Campi`** *(come `fase_simmetria.py`)*:
- **(i)** **`200` tick a FREDDO e `200` a CALDO dallo stesso stato** *(`lapse_caldo.accendi`)*: **la differenza relativa massima per chiave SCRITTA; DEVE: il picco, il raggio e il centro uguali entro `1e-8` relativo**
*(il centro: la distanza fra i due centri diviso il raggio, mia, dichiarata)*;
- **(ii)** **il numero MEDIO di giri del punto fisso per tick** *(LA MISURA CHE DECIDE; a caldo senza il primo tick, che parte a freddo; anche con)* **e la DISTRIBUZIONE** *(Luca `12:12`: in quanti tick basta un giro, due, ...; il minimo, la media, il massimo; oltre il `90%` con un giro, scritto in chiaro)*; **il tempo per tick accanto, la macchina CARICA, dichiarato;**
- **(iii)** **la ripartenza al bit a caldo:** **lo stato, il campo e `cs_prec` al tick `150` della corsa a caldo; da li' `50` tick = il tick `200` della corsa a caldo AL BIT** *(esclusa `h_int`)*. **DEVE.**
### **A3:** **il rapporto dei giri** *(a freddo / a caldo)* **almeno `1.3`: la partenza a caldo per le corse col lapse NUOVE; sotto: si scrive.**
"""
import argparse
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
import lapse_caldo as LC  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_cottura_U as CU  # noqa: E402
import mattone_rhoc as MR  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

N_TICK, K_SALVA = 200, 150
TOLL_FORMA = 1e-8
SOGLIA_GIRI = 1.3
CHIAVI = ("psi_h", "phi_h", "rho", "Lambda", "campo_E", "campo_A")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  DEVE PASSARE: %-100s %s   %s" % (che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def distribuzione(nome, giri):
    """### **Luca `12:12`:** in quanti tick basta UN giro *(quello di verifica)*, in quanti due, tre, ...; il minimo, la media, il massimo; oltre il `90%` con un giro: scritto in chiaro."""
    g = np.asarray(giri, dtype=int)
    v, c = np.unique(g, return_counts=True)
    print("    %s: %d tick; il minimo %d, la media %.4f, il massimo %d; la distribuzione: %s" % (nome, len(g), g.min(), g.mean(), g.max(), ", ".join("%d giri: %d tick" % (a, b) for a, b in zip(v, c))))
    f1 = float(np.mean(g == 1))
    if f1 > 0.9:
        print("    ### %s: IN PIU' DEL 90%% DEI TICK BASTA UN GIRO (%.1f%%)" % (nome, 100.0 * f1))


def main(argv):
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    for m in ("mattone", "mattone_cottura_U", "mattone_rhoc", "mattone_triangolo", "lapse_caldo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--registro")
    reg = ap.parse_args(argv).registro
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    t_s = int(ct["t"])
    print("=" * 130)
    print("LA PARTENZA A CALDO (7-bis; Luca 12:04, A2; 12:09): %s da solo nella scena di S162, il bordo da R_A %g, G+U; %d tick a freddo e a caldo; la ripartenza da %d; la soglia dei giri %g"
          % (ct["file"], MTR.R_A_SCENA, N_TICK, K_SALVA, SOGLIA_GIRI))
    print("### la macchina CARICA (tre corse lunghe in giro): il tempo per tick si scrive, non decide (Luca 12:09)")
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        with np.load(ct["file"]) as d:
            dati = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()

        def prepara(stato, A, E):
            Z["metti"](stato)
            C = MT.Campi(Z, "MGU", rho_c, e)
            C.campo.A[...] = A
            C.campo.E[...] = E
            C.campo.e = e
            C.e_prec = e
            U1.scrivi_U(Z["mot"], C.campo)
            return C

        def foto(C):
            out = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            out.update(campo_A=C.campo.A.copy(), campo_E=C.campo.E.copy())
            return out

        def gira(modo, C, k_da, k_a, cs=None, salva=None):
            LC.accendi(modo, cs)
            snap = None
            t1 = time.time()
            try:
                for k in range(k_da + 1, k_a + 1):
                    C.tick(k, t_s + k, 1.0, e)
                    if salva == k:
                        snap = (foto(C), LC.cs_prec())
                    if reg and k % 50 == 0:
                        MT.tappa(reg, "%s k %d; %.3f s per tick" % (modo, k, (time.time() - t1) / (k - k_da)))
            finally:
                giri = list(LC.STATO["giri"])
                LC.spegni()
            return foto(C), giri, (time.time() - t1) / (k_a - k_da), snap

        def forma(st):
            Z["metti"]({x: st[x] for x in Z["chiavi"]})
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            return float(rho.max()), MR.raggio(Z, rho, c), c
        # ---------------------------------------------------------------- (i), (ii)
        C = prepara(dati, A0, E0)
        fr, g_fr, t_fr, _s = gira("freddo", C, 0, N_TICK)
        print("### A FREDDO: %d tick, %.3f s per tick; i giri: la media %.4f (min %d, max %d)" % (N_TICK, t_fr, np.mean(g_fr), min(g_fr), max(g_fr)))
        C = prepara(dati, A0, E0)
        ca, g_ca, t_ca, snap = gira("caldo", C, 0, N_TICK, salva=K_SALVA)
        print("### A CALDO: %d tick, %.3f s per tick; i giri: la media %.4f (min %d, max %d); senza il primo tick (che parte a freddo) %.4f; il primo tick %d"
              % (N_TICK, t_ca, np.mean(g_ca), min(g_ca), max(g_ca), np.mean(g_ca[1:]), g_ca[0]))
        print("-" * 130)
        print("### (i) LO STATO FINALE, a caldo contro a freddo: la differenza relativa massima per chiave (max |caldo - freddo| / max |freddo|)")
        for x in CHIAVI:
            den = float(np.max(np.abs(fr[x]))) or 1.0
            print("    %-9s %.3e%s" % (x, float(np.max(np.abs(ca[x] - fr[x]))) / den, "   (AL BIT)" if np.array_equal(ca[x], fr[x]) else ""))
        pf, rf, cf = forma(fr)
        pc, rc, cc = forma(ca)
        dc = MT.distanza(Z["L"], cf, cc)
        esito("(i) il picco a caldo = a freddo entro %g relativo" % TOLL_FORMA, abs(pc - pf) / pf <= TOLL_FORMA, "%.3e (%.10e contro %.10e)" % (abs(pc - pf) / pf, pc, pf))
        esito("(i) il raggio a caldo = a freddo entro %g relativo" % TOLL_FORMA, abs(rc - rf) / rf <= TOLL_FORMA, "%.3e (%.10f contro %.10f)" % (abs(rc - rf) / rf, rc, rf))
        esito("(i) il centro a caldo = a freddo entro %g (la distanza / il raggio, mia)" % TOLL_FORMA, dc / rf <= TOLL_FORMA, "%.3e (la distanza %.3e)" % (dc / rf, dc))
        # ---------------------------------------------------------------- (iii)
        print("-" * 130)
        st150, cs150 = snap
        C = prepara({x: st150[x] for x in Z["chiavi"]}, st150["campo_A"], st150["campo_E"])
        ri, g_ri, _t, _s = gira("caldo", C, K_SALVA, N_TICK, cs=cs150)
        div = [x for x in list(Z["chiavi"]) + ["campo_A", "campo_E"] if x not in CU.CHIAVI_SERVIZIO and not np.array_equal(ri[x], ca[x])]
        esito("(iii) la ripartenza a caldo dal tick %d (lo stato, il campo e cs_prec) per %d tick = il tick %d della corsa a caldo AL BIT (esclusa h_int)" % (K_SALVA, N_TICK - K_SALVA, N_TICK), not div, "diverse: %s" % div)
        Z["metti"]()
    # ---------------------------------------------------------------- (ii), A3
    print("-" * 130)
    rap = float(np.mean(g_fr)) / float(np.mean(g_ca[1:]))
    rap_t = t_fr / t_ca
    print("### (ii) I GIRI: a freddo %.4f per tick, a caldo %.4f (senza il primo); IL RAPPORTO %.4f (la soglia %g); il tempo per tick %.3f contro %.3f s, il rapporto %.4f (la macchina CARICA: non decide)"
          % (np.mean(g_fr), np.mean(g_ca[1:]), rap, SOGLIA_GIRI, t_fr, t_ca, rap_t))
    print("### (ii) LA DISTRIBUZIONE DEI GIRI (Luca 12:12)")
    distribuzione("a freddo", g_fr)
    distribuzione("a caldo (senza il primo tick)", g_ca[1:])
    print("### A3: %s" % ("IL RAPPORTO DEI GIRI E' ALMENO %g: la partenza a caldo per le corse col lapse NUOVE (non al bit con le vecchie, dichiarato)" % SOGLIA_GIRI if rap >= SOGLIA_GIRI
                          else "IL RAPPORTO DEI GIRI E' SOTTO %g: la parte B col codice di oggi" % SOGLIA_GIRI))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s" % (OK[0], OK[1], FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
