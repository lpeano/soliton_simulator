# -*- coding: utf-8 -*-
r"""**`C4`: LA RISPOSTA STATICA CON LA STRADA `(d)`** — *il vuoto si ritira ancora?*

> ### ⛔ **Il criterio viene dal mandato del `2026-10-18`:** *«la risposta STATICA (il
> protocollo di `371731f`, accensione dichiarata e uguale): il vuoto si ritira ancora
> vicino alla sorgente? Riporta verso, pendenza e sovrapposizione accanto ai numeri di
> oggi. ### **Se il verso si inverte, STOP e relaziona: e' fisica, la legge Luca.**»*

## ⭐ COME, E CHE COSA SI CONFRONTA

### ✅ **DUE corse col MEDESIMO protocollo** *(`statica_protocollo`, quello di
`371731f`)*: una ### **a forma SPENTA** *(i numeri di oggi)* e una
### **con la forma ACCESA** *(la strada `(d)`: `cs` dinamico e `CAMM-FASE-VUOTO`)*.
### ⛔ **E L'ACCENSIONE DELLA SORGENTE E' DICHIARATA E UGUALE** nelle due -- e' la
lezione dell'errore `n.3` del guardiano: ### **un confronto fra accensioni diverse non e'
un confronto.**

### 📌 **E LE LETTURE SONO QUELLE DI OGGI, importate e non riscritte:** la media di
`dLambda` sui nodi della sorgente con la sua ### **barra d'errore** *(i blocchi della
finestra)*, e il ### **profilo per anelli.**

Gira con:  python primo_ordine/_misura_statica_d.py
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import statica_protocollo as PR                               # noqa: E402

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE E' TUTTA IMPORTATA, e nessun numero e' inventato qui:**
# ### il `dtau`, l'accensione, la forma, il raggio, la finestra e i tick
# ### ### **vengono dal protocollo.**
DTAU = PR.DTAU[0]
ACCESO = PR.T_ACCENSIONE[1]
FORMA = "S3"
TICK = PR.TICK
# ### ⛔ **`Lambda_c` SI DERIVA DALLA SCENA** *(`A1`)*: e' ### **il vuoto della scena**
# ### *(`PR.VUOTO^2`, cioe' `Lambda` di un'estremita' libera, per il grado del nodo)*, e
# ### ### **non un numero scelto.** ### ⚠ **E il rapporto e' un'ETICHETTA.**
RAPPORTO = 1.0


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def lambda_c_della_scena():
    """### `Lambda_c` ### **dal vuoto della scena**, una volta e prima della corsa."""
    import scena_l2 as SC
    _i, mot, st, _p, _c, _per = SC.scena(DTAU, PR.VUOTO, 0.0, PR.RAGGIO, False,
                                         True, False, PR.SEME, 1, lati=PR.LATI)
    return RAPPORTO * float(np.mean(mot.densita_vuoto(st)))


def una_risposta(lc):
    """### `(media, barra, profilo, per, dentro)` ### **col protocollo di oggi.**"""
    t0 = time.time()
    b, _dr, _dt, _p = PR.base(DTAU, TICK, lambda_c=lc)
    a, drho, dtot, per = PR.corri(DTAU, PR.X_RIF, FORMA, TICK, ACCESO, (0,),
                                  lambda_c=lc)
    prof = PR.blocchi(a - b, PR.inizio_finestra(ACCESO), PR.FINESTRE)
    dentro = [v for d, nodi in per.items() if d <= PR.RAGGIO for v in nodi]
    m, s = PR.su_nodi(prof, dentro)
    print("     %-14s dLambda = %+.6e +- %.3e (%.1f barre)   rho fermo %.1e"
          "   somma |phi|^2 %.1e   [%.1f s]"
          % ("ACCESA" if lc is not None else "spenta", m, s,
             abs(m) / s if s > 0 else float("nan"), drho, dtot, time.time() - t0))
    sys.stdout.flush()
    return m, s, prof, per, dentro


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    lc = lambda_c_della_scena()
    print("=" * 100)
    print("`C4`: LA RISPOSTA STATICA CON LA STRADA `(d)` -- il vuoto si ritira ancora?")
    print("### Mandato del 2026-10-18. NESSUNA DECISIONE.")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata e IMPORTATA dal protocollo:")
    print("  lati = %s   vuoto = %.1f   seme = %d   raggio = %d   x = %.2f"
          % (PR.LATI, PR.VUOTO, PR.SEME, PR.RAGGIO, PR.X_RIF))
    print("  dtau = %.2f   forma = %s   tick = %d   accensione = %d (DICHIARATA e"
          " UGUALE nelle due corse)" % (DTAU, FORMA, TICK, ACCESO))
    print("  la finestra: da T+%d, %d blocchi   e il pezzo sostituito e' %s"
          % (PR.TRANSITORIO, PR.FINESTRE, PR.FLUSSO_SOSTITUITO))
    print("  `Lambda_c` = %.4f (%.1f x il vuoto medio della scena, DERIVATO)"
          % (lc, RAPPORTO))
    print("-" * 100)
    print("### LE DUE CORSE, col MEDESIMO protocollo:")
    m0, s0, p0, per, dentro = una_risposta(None)
    m1, s1, p1, _per, _d = una_risposta(lc)
    print("-" * 100)
    # ### ⛔⛔ **IL CRITERIO DEL MANDATO: IL VERSO.** ### **Se si inverte, STOP.**
    esito("`C4` il vuoto si RITIRA ancora: il VERSO non si inverte",
          (m0 < 0) == (m1 < 0),
          "spenta %+.3e, ACCESA %+.3e: %s"
          % (m0, m1, "lo STESSO verso" if (m0 < 0) == (m1 < 0)
             else "### IL VERSO SI E' INVERTITO: e' FISICA, e la legge Luca"))
    # ### ✅ **E le due risposte hanno MATERIA: le barre.**
    esito("`C4` e le due risposte hanno MATERIA (`>= 3` barre ciascuna)",
          abs(m0) >= 3 * s0 and abs(m1) >= 3 * s1,
          "spenta %.1f barre, ACCESA %.1f barre"
          % (abs(m0) / s0 if s0 > 0 else float("nan"),
             abs(m1) / s1 if s1 > 0 else float("nan")))
    print("-" * 100)
    print("### \U0001F4CC DI QUANTO CAMBIA (informazione, NON un criterio):")
    print("     il rapporto fra le due risposte: %.4f" % (m1 / m0 if m0 else float("nan")))
    print("     e la differenza: %+.6e (%.1f barre della spenta)"
          % (m1 - m0, abs(m1 - m0) / s0 if s0 > 0 else float("nan")))
    print("-" * 100)
    print("### \U0001F4CC IL PROFILO per anelli (informazione): dLambda(r)")
    print("     %6s %6s %18s %18s" % ("r", "nodi", "spenta", "ACCESA"))
    for d in sorted(per):
        nodi = per[d]
        a0, _e0 = PR.su_nodi(p0, nodi)
        a1, _e1 = PR.su_nodi(p1, nodi)
        print("     %6d %6d %+18.6e %+18.6e" % (d, len(nodi), a0, a1))
    print("=" * 100)
    print("`C4`: %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E NESSUNA DECISIONE: il verso e' FISICA, e la legge Luca.")
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
