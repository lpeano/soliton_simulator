r"""**LE TRE MISURE CHE COMPLETANO IL QUINTO PEZZO** — *il cono, la divergenza, gli stati.*

> **Punto `A` del mandato unico di Luca del `2026-10-16`.** I criteri sono
> ### **fissati NEL MANDATO**, prima della misura, e qui si scrivono accanto a ogni
> braccio: ### ⛔ **una banda non si allarga per far passare un braccio.**

## ⭐ I TRE BRACCI, E CHE COSA DECIDE CIASCUNO

| | il braccio | il criterio, **dal mandato** |
|---|---|---|
| `A1` | **il CONO a `dtau` piu' fini** *(`0.50`, `0.25`, `0.125`, `0.0625`)* | ### **rapporto `<= 1` a OGNI `dtau`.** ### ⛔ **Se supera `1`, e' una violazione del cono della legge in tabella: si relaziona e IL PUNTO `D` NON SI FA** |
| `A2` | **la CURVA della divergenza** fra i due protocolli statici, tick per tick | ### **nessuna conclusione di fisica**: solo numeri *(la lettura e' di Luca)*. ### **Controllo che DEVE dare un'altra risposta: due copie IDENTICHE restano a `0.0` AL BIT** |
| `A3` | **la simmetria su PIU' STATI** *(`>= 8` semi, alcuni con nodi a `rho = 0`)* | ### **`<= 8` ulp ovunque**, ai tre `dtau`, e ### **i due casi che devono fallire restano** |

### ⛔ **E IL CONO SI LEGGE SU `rho` E NON SU `Lambda`**, come in `371731f`: sulla scena di
riferimento `phi` e' ### **uniforme**, quindi il passo LIBERO lascia `Lambda`
### **esattamente ferma** — e un rapporto con zero al denominatore ### **non e' un numero.**

Gira con:  python primo_ordine/_misura_completa_l2.py
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _misura_theta_n as TN                                  # noqa: E402
import _misura_theta_nonlineare as TNL                        # noqa: E402
import statica_protocollo as PR                               # noqa: E402

OK = [0, 0]
EPSM = float(np.finfo(float).eps)
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA**
DTAU_CONO = (0.5, 0.25, 0.125, 0.0625)
TICK_CONO = 300
TICK_DIV = 200
DTAU_DIV = (0.5, 0.25)
# ### ⭐ **OTTO SEMI, e i primi quattro hanno NODI VUOTI** *(`rho = 0`)*: il mandato chiede
# ### *«alcuni con nodi a `rho = 0`»*, e ### **senza di loro il caso del LIMITE non sarebbe
# ### nella misura.**
SEMI = (11, 23, 37, 41, 53, 67, 71, 89)
VUOTI_PER_SEME = {11: (0, 4), 23: (2,), 37: (1, 5, 7), 41: (8,)}
ULP_SIMMETRIA = 8.0


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


# ====================================================================== A1: il cono
def _salto(dtau, forma, extra):
    """### `max |rho(t+1) - rho(t)|`, ### **a materia LIBERA** *(come `371731f`)*."""
    PR.corri(dtau, PR.X_RIF, forma, TICK_CONO, 0, (0,), congela="no", **extra)
    return float(PR.ULTIMA["salto_rho"])


def braccio_cono():
    print("-" * 96)
    print("### (A1) IL CONO a dtau FINI: max |d rho_k| col termine contro SENZA")
    print("###      criterio DAL MANDATO: rapporto <= 1 a OGNI dtau")
    fuori = {}
    for dtau in DTAU_CONO:
        t0 = time.time()
        PR.SOSTITUISCI = False
        con = _salto(dtau, "MOTORE", {})
        PR.SOSTITUISCI = True
        senza = _salto(dtau, "S3", {"senza_alpha": True, "beta_zero": True})
        PR.SOSTITUISCI = False
        rap = con / senza if senza else float("nan")
        fuori[dtau] = rap
        print("  dtau=%.4f  col termine %.6e   senza %.6e   -> rapporto %.4f   [%.1f s]"
              % (dtau, con, senza, rap, time.time() - t0))
        esito("(A1) dtau=%.4f: rapporto <= 1" % dtau, rap <= 1.0,
              "%.4f -- sopra `1` sarebbe UNA VIOLAZIONE DEL CONO, e il punto `D` non si fa"
              % rap)
    print("  ### I RAPPORTI, uno per uno: %s"
          % "  ".join("%.4f" % fuori[d] for d in DTAU_CONO))
    return fuori


# ====================================================================== A2: la divergenza
def braccio_divergenza():
    print("-" * 96)
    print("### (A2) LA CURVA DELLA DIVERGENZA fra i due protocolli statici, 1..%d tick"
          % TICK_DIV)
    print("###      NESSUNA CONCLUSIONE DI FISICA: solo numeri, la lettura e' di Luca")
    fuori = {}
    for dtau in DTAU_DIV:
        # ### il protocollo di `ebf5317` *(`S3` sostituito, fotografia, congelamento per
        # ### tick)* contro quello del motore *(congelamento per PEZZO)*
        PR.SOSTITUISCI = True
        a3, _d1, _t1, _p1 = PR.corri(dtau, PR.X_RIF, "S3", TICK_DIV, 0, (0,),
                                     congela="tick")
        PR.SOSTITUISCI = False
        am, _d2, _t2, _p2 = PR.corri(dtau, PR.X_RIF, "MOTORE", TICK_DIV, 0, (0,),
                                     congela="pezzo")
        d = np.max(np.abs(a3 - am), axis=1)
        # ### ⛔ **IL CONTROLLO CHE DEVE DARE UN'ALTRA RISPOSTA: due copie IDENTICHE.**
        # ### ### **Senza di lui, <<cresce>> potrebbe essere il rumore del motore** invece
        # ### della differenza fra i due protocolli.
        am2, _d3, _t3, _p3 = PR.corri(dtau, PR.X_RIF, "MOTORE", TICK_DIV, 0, (0,),
                                      congela="pezzo")
        dd = float(np.max(np.abs(am - am2)))
        esito("(A2) dtau=%.2f: due copie IDENTICHE restano a `0.0` AL BIT" % dtau,
              dd == 0.0, "scarto %.1e: il motore e' DETERMINISTICO" % dd)
        # ### la curva, e la pendenza dell'esponenziale dove la differenza c'e'
        vivi = np.nonzero(d > 0.0)[0]
        if vivi.size < 20:
            esito("(A2) dtau=%.2f: la curva ha abbastanza punti" % dtau, False,
                  "solo %d tick con differenza non nulla" % vivi.size)
            continue
        t = vivi.astype(float)
        y = np.log10(d[vivi])
        # ### ⭐ **LA BARRA SI PRENDE A BLOCCHI**, come sempre: cinque fette del tratto, e
        # ### la deviazione fra le pendenze delle fette ### **diviso radice di cinque.**
        pend = float(np.polyfit(t, y, 1)[0])
        fette = np.array_split(np.arange(vivi.size), 5)
        pp = [float(np.polyfit(t[f], y[f], 1)[0]) for f in fette if f.size >= 4]
        barra = (float(np.std(pp, ddof=1)) / np.sqrt(len(pp))) if len(pp) > 1 else float("nan")
        fuori[dtau] = (pend, barra, float(d[vivi[0]]), float(d[-1]), int(vivi[0]))
        print("  dtau=%.2f  primo tick con differenza: %d (%.3e)   a %d tick: %.3e"
              % (dtau, vivi[0], d[vivi[0]], TICK_DIV, d[-1]))
        print("      pendenza di log10(scarto) per tick: %.5f +- %.5f   (fette: %s)"
              % (pend, barra, "  ".join("%.4f" % x for x in pp)))
        esito("(A2) dtau=%.2f: la pendenza e' POSITIVA e fuori dalla sua barra" % dtau,
              pend > 3.0 * barra if barra == barra else False,
              "%.5f contro %.5f: %.1f barre" % (pend, barra, pend / barra)
              if barra == barra else "barra non calcolabile")
        sys.stdout.flush()
    return fuori


# ====================================================================== A3: la simmetria
def braccio_simmetria():
    print("-" * 96)
    print("### (A3) LA SIMMETRIA `W A W A^-1 = 1` su %d stati, ai tre dtau" % len(SEMI))
    print("###      criterio DAL MANDATO: <= %.0f ulp ovunque" % ULP_SIMMETRIA)
    import corrente as CO
    ii, jj, nn = CO.toro(TN.LATI)
    P = TN._inversione(TN.LATI, ii, jj)
    peggio = {}
    for dtau in TN.DTAU:
        ulp_max, dove = 0.0, None
        for seme in SEMI:
            _i, mot, st = TN.scena(dtau, True, True)
            vuoti = VUOTI_PER_SEME.get(seme, ())
            s0 = TNL.stato_di_prova(mot, st, seme, vuoti=vuoti)
            TNL.metti(st, TNL.antiunitaria(s0, P, inversa=True))
            TNL.passo(mot, st)
            TNL.metti(st, TNL.antiunitaria(
                (st["psi_h"].copy(), st["phi_h"].copy()), P))
            fine = TNL.passo(mot, st)
            d, sc = TNL.scarto(fine, s0)
            u = d / (EPSM * sc)
            if u > ulp_max:
                ulp_max, dove = u, seme
        peggio[dtau] = (ulp_max, dove)
        print("  dtau=%.4f  il PEGGIO su %d semi: %.2f ulp (seme %s)"
              % (dtau, len(SEMI), ulp_max, dove))
        esito("(A3) dtau=%.4f: <= %.0f ulp su tutti gli stati" % (dtau, ULP_SIMMETRIA),
              ulp_max <= ULP_SIMMETRIA,
              "peggio %.2f ulp, sul seme %s" % (ulp_max, dove))
    # ### ⛔ **E I DUE CASI CHE DEVONO FALLIRE RESTANO**, su uno stato con nodi vuoti
    _i, mot, st = TN.scena(TN.DTAU[1], True, True)
    s0 = TNL.stato_di_prova(mot, st, SEMI[0], vuoti=VUOTI_PER_SEME[SEMI[0]])
    ident = np.arange(st["psi_h"].shape[0])
    TNL.metti(st, TNL.antiunitaria(s0, ident, inversa=True))
    TNL.passo(mot, st)
    TNL.metti(st, TNL.antiunitaria((st["psi_h"].copy(), st["phi_h"].copy()), ident))
    w2 = TNL.passo(mot, st)
    d2, sc2 = TNL.scarto(w2, s0)
    esito("### (A3) DEVE fallire: `Theta` SENZA `P`", d2 > ULP_SIMMETRIA * EPSM * sc2,
          "scarto %.3e: `P` SERVE" % d2)
    _i3, m3, s3 = TN.scena(TN.DTAU[1], True, False)
    t0 = TNL.stato_di_prova(m3, s3, SEMI[0], vuoti=VUOTI_PER_SEME[SEMI[0]])
    TNL.metti(s3, TNL.antiunitaria(t0, P, inversa=True))
    TNL.passo(m3, s3)
    TNL.metti(s3, TNL.antiunitaria((s3["psi_h"].copy(), s3["phi_h"].copy()), P))
    w3 = TNL.passo(m3, s3)
    d3, sc3 = TNL.scarto(w3, t0)
    esito("### (A3) DEVE fallire: con `U` CASUALE", d3 > ULP_SIMMETRIA * EPSM * sc3,
          "scarto %.3e: `U = I` SERVE" % d3)
    return peggio


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    t0 = time.time()
    print("=" * 96)
    print("LE TRE MISURE CHE COMPLETANO IL QUINTO PEZZO -- punto A del mandato unico")
    print("### I CRITERI SONO DEL MANDATO, fissati PRIMA della misura.")
    print("=" * 96)
    print("  (A1) toro %s   %d tick   x = %.2f   dtau = %s"
          % (PR.LATI, TICK_CONO, PR.X_RIF, DTAU_CONO))
    print("  (A2) %d tick   dtau = %s   i due protocolli: `S3`+foto+tick contro"
          " MOTORE+pezzo" % (TICK_DIV, DTAU_DIV))
    print("  (A3) toro %s   %d semi %s   dtau = %s   nodi vuoti: %s"
          % (TN.LATI, len(SEMI), SEMI, TN.DTAU, VUOTI_PER_SEME))
    sys.stdout.flush()
    cono = braccio_cono()
    braccio_divergenza()
    braccio_simmetria()
    print("=" * 96)
    print("  %d su %d   [corsa intera: %.1f s]" % (OK[0], OK[1], time.time() - t0))
    if any(v > 1.0 for v in cono.values()):
        print("### ⛔⛔ IL CONO E' VIOLATO a qualche dtau: il punto `D` NON SI FA, e la")
        print("###    relazione lo dice. E' il criterio del mandato.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
