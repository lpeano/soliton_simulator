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
import tick as TK                                           # noqa: E402

OK = [0, 0]
# ### ⛔ **L-ELENCO ATTESO DEI VIOLATORI, SCRITTO A MANO E NON CALCOLATO.** ### **Se fosse
# ### calcolato, il collaudo direbbe sempre <<tutto come previsto>>** -- e non vedrebbe ne-
# ### un violatore NUOVO ne- uno che sparisce senza che la strada `(B)` sia stata fatta.
# ### ⭐⭐ **SVUOTATO IL `2026-10-15`, A STRADA `(B)` FATTA** *(mandato di Luca)*:
# ### ### **i violatori attesi sono ZERO**, e da adesso ### **un violatore FA FALLIRE IL
# ### `pre-commit`** -- perche- il braccio `(1)` confronta VISTI con ATTESI, e `main`
# ### torna `1` quando un braccio fallisce.
# ### ⛔ **E LA PROVA CHE FALLISCE DAVVERO E- STATA FATTA, non supposta** *(`A9`)*:
# ### rimettendo per prova il Grover a tick fisso, il collaudo ha detto
# ### ### **<<1 violatore su 7>>** ed e- tornato `1`, cioe- ### **il `pre-commit` si e-
# ### fermato per QUEL pezzo.** ### **Poi la prova e- stata togliere.**
VIOLATORI_ATTESI = ()
# ### ⛔⛔ **I PEZZI CHE ESISTONO SOLO CON LA FORMA `cs` ACCESA** *(`2026-10-18`)*:
# ### `CAMM-FASE-VUOTO` ha coefficiente `cs'(Lambda)`, e ### **a forma spenta NON C'E'**
# ### -- quindi a forma spenta ### **non dipende da `dtau` perche' non dipende da NIENTE.**
# ### ⚠ **Misurarlo a forma spenta direbbe <<VIOLATORE>> di un pezzo che non gira**, ed
# ### e' ### **un falso-zero.** ### ✅ **Si misura dove ESISTE: con la forma accesa**, e
# ### `Lambda_c` ### **derivata dalla scena** *(`A1`)*, non scelta.
SOLO_CON_CS = ("CAMM-FASE-VUOTO",)
RAPPORTO_CS = 1.0
# ### ⛔⛔ **I PEZZI CHE ESISTONO SOLO CON LA FORMA `cs` ACCESA** *(`2026-10-18`)*:
# ### `CAMM-FASE-VUOTO` ha coefficiente `cs'(Lambda)`, e ### **a forma spenta NON C'E'**
# ### -- quindi a forma spenta ### **non dipende da `dtau` perche' non dipende da NIENTE.**
# ### ⚠ **Misurarlo a forma spenta direbbe <<VIOLATORE>> di un pezzo che non gira**, ed
# ### e' ### **un falso-zero.** ### ✅ **Si misura dove ESISTE: con la forma accesa**, e
# ### `Lambda_c` ### **derivata dalla scena** *(`A1`)*, non scelta.
SOLO_CON_CS = ("CAMM-FASE-VUOTO",)
RAPPORTO_CS = 1.0
# ### ⛔⛔ **I PEZZI CHE ESISTONO SOLO CON LA FORMA `cs` ACCESA** *(`2026-10-18`)*:
# ### `CAMM-FASE-VUOTO` ha coefficiente `cs'(Lambda)`, e ### **a forma spenta NON C'E'**
# ### -- quindi a forma spenta ### **non dipende da `dtau` perche' non dipende da NIENTE.**
# ### ⚠ **Misurarlo a forma spenta direbbe <<VIOLATORE>> di un pezzo che non gira**, ed
# ### e' ### **un falso-zero.** ### ✅ **Si misura dove ESISTE: con la forma accesa**, e
# ### `Lambda_c` ### **derivata dalla scena** *(`A1`)*, non scelta.
SOLO_CON_CS = ("CAMM-FASE-VUOTO",)
RAPPORTO_CS = 1.0
CAMBIA_MIN = 1e-9


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-56s %s   %s" % (che[:56], "PASSA" if passa else "### FALLISCE", nota))


def dipende_da_dtau(idl, frazione, nn=12, seme=7, dtau_fisso=None,
                    rapporto_cs=None):
    """### `max |psi(dtau) - psi(dtau/2)|` per **UN pezzo** della composizione.

    ### ⚠ **Si confrontano DUE `dtau` sullo STESSO stato iniziale**, non due corse: cosi'
    cio' che si misura e' ### **la dipendenza del pezzo dal passo**, e nient'altro.

    ### ⛔⛔ **`dtau_fisso` SERVE AL CASO CHE DEVE FALLIRE** *(punto `3` del mandato
    unico del `2026-10-17`)*: con un valore, il passo del motore si ### **FISSA dopo aver
    costruito la scena**, quindi ### **il pezzo diventa INDIPENDENTE da `dtau`** e
    ### **deve risultare VIOLATORE.**
    ### ⛔⛔ **`rapporto_cs` SERVE A `D3`** *(`2026-10-17`)*: accende la forma `cs`
    ### ### **sullo stato di partenza**, con `Lambda_c = rapporto_cs * media(Lambda)` --
    ### cioeè ### **DERIVATA dalla scena**, non un numero scelto (`A1`).
    ### ⚠ **E su UN pezzo <<al centro del palindromo>> non ha senso** *(un pezzo non e- un
    ### tick)*: ### **la sola forma definita per un pezzo solo e- quella a stato di
    ### partenza**, e lo si dice invece di lasciarlo capire.
    ### ⭐ **E QUESTO NON TOCCA IL CENSIMENTO DI OGGI:** senza il parametro il ramo
    ### ### **non esiste**, e i numeri di questo file ### **sono quelli di prima.**
    ### ✅ **E la perturbazione e- IN MEMORIA, su una scena costruita qui:** nessun file
    del repo si tocca. ### ⚠ **Misurato il `2026-10-17`: con `mot.dtau` fisso la
    differenza e- `0.0` ESATTO** -- cioe- l-operatore lo legge ### **a ogni corsa**, e il
    braccio ### **NON e- vacuo.**
    """
    nome, vuole_par = TK.OPERATORE[idl]
    fuori = []
    for dt in (0.4, 0.2):
        _i, mot, st, par = DV.scena(nn, seme, dt, norma="locale", vuoto_modulo=2.0,
                                    su2=True)
        if dtau_fisso is not None:
            # ### ⛔ **IL RAMO DEL CASO CHE DEVE FALLIRE**, e non c-e- altra via: il
            # ### passo vive ### **nel motore**, e un pezzo lo legge da la-.
            mot.dtau[:] = dtau_fisso
        if rapporto_cs is not None:
            # ### ⛔ **IL RAMO DI `D3`:** la forma si accende QUI, e ### **`Lambda_c` esce
            # ### dalla scena** -- una volta, e prima del pezzo.
            import flussi_parziali as FP
            FP.accendi_cs(mot, rapporto_cs * float(np.mean(mot.densita_vuoto(st))), st)
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
    visti, guardati = [], []
    for idl, frazione, _tipo in CM.ORDINE:
        guardati.append((idl, frazione))
        # ### ⛔ **IL RAMO DEI PEZZI CHE VIVONO SOLO CON LA FORMA:** si accende,
        # ### e ### **lo si dice nella riga del censimento.**
        d = dipende_da_dtau(idl, frazione,
                            rapporto_cs=(RAPPORTO_CS if idl in SOLO_CON_CS
                                         else None))
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
    # ### ⛔⛔ **IL BRACCIO `(2)` RISCRITTO IL `2026-10-17`, e prima era un
    # ### FALSO-UNO PER META-.** Diceva *<<la moneta e LA SATURAZIONE dipendono da
    # ### `dtau`>>* nominandole ### **a mano** -- e `CAMM-SATURAZIONE` ### **non e- nell-
    # ### ordine dal `2026-10-15`**, quindi ### **non viene MAI misurata**, quindi
    # ### ### **non e- mai fra i violatori**, quindi ### **il braccio la contava BUONA.**
    # ### ⚠ **Meta- del braccio era soddisfatta DALL-ASSENZA.**
    # ### ✅ **Adesso i pezzi si leggono DALLA TABELLA**, e il braccio dice
    # ### ### **<<TUTTI i pezzi che GIRANO dipendono da `dtau`>>**, col numero piu- piccolo
    # ### misurato accanto.
    per_pezzo = {}
    for idl, frazione in guardati:
        # ### ⛔ **IL RAMO DEI PEZZI CHE VIVONO SOLO CON LA FORMA:** si accende,
        # ### e ### **lo si dice nella riga del censimento.**
        d = dipende_da_dtau(idl, frazione,
                            rapporto_cs=(RAPPORTO_CS if idl in SOLO_CON_CS
                                         else None))
        per_pezzo[idl] = min(per_pezzo.get(idl, d), d)
    peggio = min(per_pezzo.values()) if per_pezzo else 0.0
    quale = [k for k, v in per_pezzo.items() if v == peggio]
    esito("### (2) DEVE DIPENDERE: TUTTI i pezzi che GIRANO, letti dalla tabella",
          bool(per_pezzo) and peggio >= CAMBIA_MIN,
          "%d pezzi distinti dall-ordine; il piu- debole e- %s con %.3e (la soglia e- %.0e)"
          % (len(per_pezzo), quale[0] if quale else "-", peggio, CAMBIA_MIN))
    # ### ⛔⛔ **IL CASO CHE DEVE FALLIRE, ed e- il CONTROLLO POSITIVO VERO del
    # ### braccio `(1)`:** il `(1)` dice *<<i violatori sono esattamente quelli attesi>>* con
    # ### ### **ZERO attesi**, e passerebbe ### **anche se la misura non sapesse VEDERE una
    # ### violazione.** ### ✅ **Rendendo un pezzo dell-ordine INDIPENDENTE da `dtau`, la
    # ### misura DEVE vederlo** -- e questo esclude quel caso.
    idl0, fraz0 = guardati[0]
    d_fisso = dipende_da_dtau(idl0, fraz0, dtau_fisso=0.4)
    esito("### (2) DEVE fallire: un pezzo dell-ordine reso INDIPENDENTE da `dtau`",
          d_fisso < CAMBIA_MIN,
          "`%s` col passo del motore FISSO: |differenza| = %.1e, cioe- VIOLATORE -- senza"
          " questo il braccio (1) passerebbe anche con la misura CIECA" % (idl0, d_fisso))
    # ### ⚠ **E il conteggio, che e- il numero che cito nei referti**
    # ### ⚠ **IL CONTEGGIO SI LEGGE DALL-ELENCO, non da un letterale:** prima qui
    # ### c-era ### **`4`** scritto a mano, e svuotando l-elenco ### **sarebbe diventato
    # ### una SECONDA cosa da cambiare a mano.** ### ✅ **Cosi- il numero SEGUE la
    # ### decisione**, e l-unica cosa scritta a mano resta ### **l-elenco.**
    # ### ⚠ **E ANCHE IL NUMERO DEI PEZZI SI LEGGE DALLA COMPOSIZIONE**, dal
    # ### 2026-10-15: prima qui c-era ### **`7`** scritto a mano, e quando l-ordine e-
    # ### diventato ### **PALINDROMO (12 pezzi)** questo braccio e- fallito ### **per il
    # ### letterale, non per la fisica.** ### ⛔ **Un numero scritto a mano in un
    # ### collaudo diventa un secondo posto da aggiornare**, ed e- lo stesso difetto che
    # ### l-elenco dei violatori aveva. ### ✅ **Cio- che il braccio pretende DAVVERO e-
    # ### che OGNI pezzo della composizione sia stato guardato**, e quello si dice senza
    # ### nessun letterale.
    esito("### (3) e sono %d violatori su %d pezzi, tutti guardati"
          % (len(VIOLATORI_ATTESI), len(CM.ORDINE)),
          len(visti) == len(VIOLATORI_ATTESI) and len(guardati) == len(CM.ORDINE),
          "%d violatori su %d pezzi, e %d pezzi guardati"
          % (len(visti), len(CM.ORDINE), len(guardati)))
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ✅ E IL CENSIMENTO DICE CHE ZERO PEZZI VIOLANO `TEMPO-PROPRIO-LOCALE`:")
    print("###   la strada (B) e' stata fatta il 2026-10-15, e questo file da CRITERIO")
    print("###   DI ACCETTAZIONE e' diventato UN PRESIDIO: un pezzo che tornasse a")
    print("###   evolvere col tick FA FALLIRE il pre-commit, e la prova che fallisce")
    print("###   davvero e' stata fatta rimettendo un pezzo a tick fisso.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
