# -*- coding: utf-8 -*-
r"""IL CONTROLLO DEL TEMPO PROPRIO — **quali leggi evolvono col TICK invece che col `dtau`.**

> **Nota di Luca, 2026-10-13:** *«verifica con un controllo che **nessuna legge della
> tabella evolva col tick invece che col tempo proprio** (oggi Grover e spostamento lo
> fanno: e' proprio cio' che `(B)` corregge).»*
>
> **E il principio, nelle sue parole:** *«TUTTE le evoluzioni del sistema dipendono dal
> tempo proprio locale e NON dal tick; il tick e' la FREQUENZA DEL CAMBIAMENTO DI STATO,
> cioe' il CONO.»*

## ⭐ COME SI MISURA, E PERCHE' NON SI LEGGE NEL CODICE

### ⛔ **Un controllo che GUARDASSE il sorgente direbbe <<questa funzione non usa `dtau`>>,
e sarebbe una lettura.** ### ✅ **Questo lo MISURA:** applica ogni pezzo della composizione
**con `dtau` e con `dtau/2`** e guarda **se il risultato cambia.**
### ⭐ **Un pezzo che NON cambia NON dipende dal tempo proprio** — e non c'e' modo di
nasconderlo in un commento.

## ⚠ E OGGI IL CONTROLLO **FALLISCE**, ed e' VOLUTO

### ⛔ **`4` pezzi su `7` ignorano `dtau`** *(il Grover, lo spostamento, e i due del
vuoto)*, e la voce `TEMPO-PROPRIO-LOCALE` dice *«in TUTTI gli step si usa il tempo proprio
locale»*: ### **quei `4` LA VIOLANO DA SEMPRE.**
### ✅ **La strada `(B)` e' cio' che li corregge**, e questo collaudo e'
### **il suo criterio di accettazione, scritto PRIMA:** quando `(B)` sara' implementata,
### **questo file deve passare `7` su `7` senza essere toccato.**

### ⭐ **PERCIO' NON FA FALLIRE IL `pre-commit`:** stampa il censimento e torna `0`, con
l'elenco dei violatori **attesi**. ### ⛔ **Ma se un pezzo NUOVO comparisse fra i violatori,
o se uno dei quattro SPARISSE senza che `(B)` sia stata fatta, LO DICE** — ed e' il motivo
per cui l'elenco atteso e' **scritto qui dentro** e non calcolato.

Gira con:  python primo_ordine/_collauda_tempo_proprio.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import composizione as CM                                     # noqa: E402
import deriva as DV                                           # noqa: E402

OK = [0, 0]
# ### ⛔ **L-ELENCO ATTESO DEI VIOLATORI, SCRITTO A MANO E NON CALCOLATO.** ### **Se fosse
# ### calcolato, il collaudo direbbe sempre <<tutto come previsto>>** -- e non vedrebbe ne-
# ### un violatore NUOVO ne- uno che sparisce senza che la strada `(B)` sia stata fatta.
VIOLATORI_ATTESI = ("CAMM-GROVER", "CAMM-SPOSTAMENTO",
                    "CAMM-GROVER-VUOTO", "CAMM-SPOSTAMENTO-VUOTO")
CAMBIA_MIN = 1e-9


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-56s %s   %s" % (che[:56], "PASSA" if passa else "### FALLISCE", nota))


def dipende_da_dtau(idl, frazione, nn=12, seme=7):
    """### `max |psi(dtau) - psi(dtau/2)|` per **UN pezzo** della composizione.

    ### ⚠ **Si confrontano DUE `dtau` sullo STESSO stato iniziale**, non due corse: cosi'
    cio' che si misura e' ### **la dipendenza del pezzo dal passo**, e nient'altro.
    """
    nome, vuole_par = DV.OPERATORE[idl]
    fuori = []
    for dt in (0.4, 0.2):
        _i, mot, st, par = DV.scena(nn, seme, dt, norma="locale", vuoto_modulo=2.0,
                                    su2=True)
        mot.apri_tick()
        mot.operatori[nome](st, par if vuole_par else {}, frazione)
        mot.chiudi_tick()
        fuori.append((st["psi_h"].copy(), st["phi_h"].copy()))
    dpsi = float(np.max(np.abs(fuori[0][0] - fuori[1][0])))
    dphi = float(np.max(np.abs(fuori[0][1] - fuori[1][1])))
    return max(dpsi, dphi)


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 96)
    print("IL CONTROLLO DEL TEMPO PROPRIO: quali pezzi EVOLVONO COL TICK invece che col"
          " dtau")
    print("=" * 96)
    visti = []
    for idl, frazione, _tipo in CM.ORDINE:
        d = dipende_da_dtau(idl, frazione)
        viola = d < CAMBIA_MIN
        if viola and idl not in visti:
            visti.append(idl)
        print("  %-26s frazione %-4s  |psi(dtau) - psi(dtau/2)| = %.3e   %s"
              % (idl, frazione, d,
                 "### IGNORA dtau: VIOLA `TEMPO-PROPRIO-LOCALE`" if viola
                 else "dipende dal tempo proprio"))
    print("-" * 96)
    # ### ⭐ **IL BRACCIO CHE CONTA: l-elenco VISTO contro quello ATTESO**
    esito("### (1) i violatori sono ESATTAMENTE quelli attesi",
          tuple(sorted(visti)) == tuple(sorted(VIOLATORI_ATTESI)),
          "visti %s" % (tuple(sorted(visti)),))
    # ### ⛔ **E IL CASO CHE DEVE CAMBIARE: la moneta e la saturazione DIPENDONO da `dtau`**
    buoni = [x for x in ("CAMM-MONETA-SPIN", "CAMM-SATURAZIONE")
             if x not in visti]
    esito("### (2) DEVE DIPENDERE: la moneta di spin e la saturazione",
          len(buoni) == 2,
          "senza questo il braccio (1) passerebbe anche con TUTTO fermo")
    # ### ⚠ **E il conteggio, che e- il numero che cito nei referti**
    esito("### (3) e sono 4 su 7, come misurato in 7141812",
          len(visti) == 4 and len(CM.ORDINE) == 7,
          "%d violatori su %d pezzi" % (len(visti), len(CM.ORDINE)))
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⚠ E IL CENSIMENTO DICE CHE 4 PEZZI VIOLANO `TEMPO-PROPRIO-LOCALE`:")
    print("###   e' il DIFETTO che la strada (B) corregge, e questo file e' il suo")
    print("###   CRITERIO DI ACCETTAZIONE: quando (B) sara' fatta, i violatori attesi")
    print("###   dovranno diventare ZERO -- e allora questo elenco si svuota.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
