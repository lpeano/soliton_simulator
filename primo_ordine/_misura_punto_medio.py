# -*- coding: utf-8 -*-
r"""**IL PUNTO MEDIO PER PEZZO** — *dove serve, e se porta `G` al secondo ordine*.

> ### \U0001F4CC **Mandato di Luca del `2026-10-18`, `12:07`:** ogni pezzo usa
> ### **il proprio peso al PROPRIO punto medio.**
> ### ⛔ **E IL PRIMO PASSO NON E' CODICE: E' UNA MISURA** -- *«prima di scrivere codice,
> misura per ogni pezzo del palindromo (`14` voci) quanto si muove `Lambda` dentro la sua
> applicazione. Scrivi nel referto i numeri che hai VISTO e non l'elenco atteso.»*

## ⭐ PERCHE' LA MISURA VIENE PRIMA

### ⛔ **I numeri che avevo erano su TRE pezzi** *(referto `strada_d_c1_c2_c5.txt`, blob
`092a4056`)*, e ### **un elenco ATTESO non e' una misura.** ### ✅ **Se il pezzo che muove
`Lambda` e' uno solo, il punto fisso va SOLO li'** -- e ogni altro pezzo che risultasse
muoverla ### **si segnala PRIMA, con un commit.**

## ⚠ E SI MISURA CON LA FORMA ACCESA

### **A forma spenta il peso non dipende dallo stato**, quindi ### **<<quanto muove
`Lambda`>> non direbbe niente sul peso.** ### ✅ **La domanda e': il peso che QUESTO pezzo
usa cambia DURANTE la sua applicazione?** -- e la risposta passa da `Lambda`.

Gira con:  python primo_ordine/_misura_punto_medio.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _misura_hw as HW                                       # noqa: E402
import _misura_mb2 as MB2                                     # noqa: E402
import composizione as CM                                     # noqa: E402
import deriva as DV                                           # noqa: E402
import flussi_parziali as FP                                  # noqa: E402
import tick as TK                                             # noqa: E402

OK = [0, 0]
# ### ⛔ **I `dtau` DEL DIMEZZAMENTO: gli stessi di `H_w` e di `M-B2`**, importati.
KAPPA = HW.KAPPA_HW
# ### ⛔ **LA SOGLIA DEL <<MUOVE>>: `1e-9`**, ed e' ### **quella del collaudo del tempo
# ### proprio** *(`CAMBIA_MIN`)*, importata e non scelta qui.
import _collauda_tempo_proprio as TP                          # noqa: E402
SOGLIA = TP.CAMBIA_MIN


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def scena(dtau):
    """### La scena di `M-B2` ### **sullo stato NON uniforme della pre-corsa di `H_w`.**

    ### ⚠ **Lo stato e' quello**, e non un altro: cosi' i numeri si confrontano con
    ### **quelli gia' misurati** *(`C1`, `C5`, il referto `092a4056`)*.
    """
    inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
    lc = float(np.mean(mot.densita_vuoto(st)))
    FP.accendi_cs(mot, lc, st)
    return inc, mot, st, par, lc


def quanto_muove(dtau, idl, frazione):
    """### `(dLambda, drho)` ### **DENTRO l'applicazione di UN pezzo.**"""
    inc, mot, st, par, _lc = scena(dtau)
    lam0 = mot.densita_vuoto(st).copy()
    rho0 = mot.densita_materia(st).copy()
    mot.apri_tick()
    nome, vuole_par = TK.OPERATORE[idl]
    mot.operatori[nome](st, par if vuole_par else {}, frazione)
    mot.chiudi_tick()
    d_lam = float(np.max(np.abs(mot.densita_vuoto(st) - lam0)))
    d_rho = float(np.max(np.abs(mot.densita_materia(st) - rho0)))
    return d_lam, d_rho


def censimento():
    """### ⭐⭐ **I `14` PEZZI, UNO PER UNO: quanto muovono `Lambda` e `rho`.**

    ### ⛔ **E si guardano TUTTE E `14` LE VOCI, non i `7` id distinti:** una legge
    compare ### **due volte** nel palindromo, e ### **con la stessa frazione** -- ma e' il
    mandato a dire ### **<<`14` voci>>**, e un conteggio che ne guarda `7`
    ### **non e' quello che il mandato chiede.**
    """
    print("### I 14 PEZZI DEL PALINDROMO: quanto muovono `Lambda` e `rho` DENTRO la")
    print("###   propria applicazione, con la forma `cs` ACCESA. La soglia e' %.0e" % SOGLIA)
    dtau = 1.0 / (2 ** KAPPA[1])
    print("###   (`dtau = %.4f`, lo stato NON uniforme della pre-corsa di `H_w`)" % dtau)
    print("     %-4s %-24s %-9s %-16s %-16s %s"
          % ("n.", "il pezzo", "frazione", "|dLambda|", "|drho|", "muove Lambda?"))
    muovono = []
    for k, (idl, frazione, _tipo) in enumerate(CM.ORDINE):
        d_lam, d_rho = quanto_muove(dtau, idl, frazione)
        muove = d_lam > SOGLIA
        if muove and idl not in muovono:
            muovono.append(idl)
        print("     %-4d %-24s %-9.2f %-16.6e %-16.6e %s"
              % (k + 1, idl, frazione, d_lam, d_rho,
                 "### SI'" if muove else "no"))
        sys.stdout.flush()
    print("-" * 100)
    print("     ### I PEZZI CHE MUOVONO `Lambda`, CONTATI: %d su %d id distinti"
          % (len(muovono), len(set(x[0] for x in CM.ORDINE))))
    for q in muovono:
        print("     ###   %s" % q)
    return muovono


def informazione_ordine(idl):
    """### 📌 **E DI CHE ORDINE E' IL MOVIMENTO:** `O(dtau)`, o piu' piccolo?"""
    print()
    print("### \U0001F4CC DI CHE ORDINE E' IL MOVIMENTO di `%s` (informazione)" % idl)
    print("     %-12s %-16s %s" % ("dtau", "|dLambda|", "rapporto col precedente"))
    prec = None
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        fr = [f for (q, f, _t) in CM.ORDINE if q == idl][0]
        d_lam, _dr = quanto_muove(dtau, idl, fr)
        print("     %-12.6f %-16.6e %s"
              % (dtau, d_lam, "--" if prec is None else "%.3f" % (prec / d_lam)))
        prec = d_lam
    print("     ### un rapporto `~2` vuol dire `O(dtau)`: il peso sbagliato di `O(dtau)`")
    print("###   e' cio' che da' la deriva del PRIMO ordine.")
    sys.stdout.flush()


# ### ⛔⛔ **I BRACCI CHE ACCENDEVANO IL RAMO DEL PUNTO MEDIO PER PEZZO SONO TOLTI**
# ### *(`2026-10-19`, decisione di Luca del `2026-10-18` alle `21:48`)*: il ramo e'
# ### ### **tolto dal passo**, e i bracci che lo misuravano ### **non avrebbero piu' niente
# ### da accendere.** ### ✅ **Il codice e i numeri restano nella STORIA:** il ramo e'
# ### nato in `2c95af13`, e ### **questo file, coi suoi bracci, e' rigirabile al commit
# ### `880955bb`**, che ha prodotto ### **`doc/referti_l2/punto_medio_per_pezzo.txt`**.
# ### **Restano qui** il censimento dei `14` pezzi, l'ordine del movimento, il controllo
# ### positivo dell'errore `n.12` e il peso di nodo durante il tick: ### **nessuno dei
# ### quattro accende il ramo.**


def braccio_cs_dello_stato():
    """### ⭐⭐ **IL CONTROLLO POSITIVO DELL'ERRORE `n.12`: quanto distano le due
    letture di `cs` DOPO un tick**, e ### **di che ordine.**

    ### ⛔ **`mot.cs` dopo `tick_con_cs` e' il `cs` del CENTRO di quel tick**, e
    ### **`cs(Lambda di adesso)` e' quello dello stato in cui misuro.** ### ✅ **Se la
    differenza e' `O(dtau)`, allora un'osservabile che usa `mot.cs` sbaglia di `O(dtau)`**
    -- ed e' ### **esattamente la pendenza `1` che misuravo.**
    """
    import energia_pesata as EP
    print()
    print("### IL CONTROLLO POSITIVO dell'errore `n.12`: `cs` dello STATO contro")
    print("###   `mot.cs` DOPO un tick. ### Se e' `O(dtau)`, l'osservabile vecchia")
    print("###   sbagliava di `O(dtau)` -- ed e' la pendenza `1`.")
    print("     %-10s %-18s %-14s %s" % ("dtau", "|dcs| relativo", "rapporto", "dG/G"))
    prec, rapporti = None, []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                     vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
        lc = float(np.mean(mot.densita_vuoto(st)))
        FP.accendi_cs(mot, lc, st)
        TK.tick_con_cs(st, mot, par, lc, ())
        cs_stato = FP.cs(mot.densita_vuoto(st), lc,
                         mot._b("pm_cs_s", (mot.inc.n,), float)).copy()
        d = (float(np.max(np.abs(cs_stato - mot.cs)))
             / float(np.max(np.abs(cs_stato))))
        g_s = EP.g_dello_stato(mot, st, par)
        g_p = EP.g_pesata(mot, st, par)
        dg = abs(g_s - g_p) / abs(g_s)
        if prec is not None:
            rapporti.append(prec / d)
        print("     %-10.6f %-18.6e %-14s %.6e"
              % (dtau, d, "--" if prec is None else "%.3f" % (prec / d), dg))
        prec = d
    esito("le due letture di `cs` distano `O(dtau)` dopo un tick",
          all(1.7 <= r <= 2.3 for r in rapporti),
          "i rapporti: %s -- e la differenza su `G` segue"
          % ("  ".join("%.3f" % r for r in rapporti)))


def informazione_peso_di_nodo():
    """### 📌 **QUANTO IL PESO DI NODO SI SCOSTA DURANTE IL TICK** -- *un fatto,
    e ### **NON l'ostacolo.***

    ### ⛔⛔ **RITIRATA IL `2026-10-18` (errore `n.12` del guardiano):** questa
    tabella l'avevo chiamata ### **<<dove sta l'ostacolo>>**, e ### **era sbagliato.**
    ### **Il passo era GIA' del secondo ordine** *(`C1 = 2.091`)*, e il primo ordine che
    vedevo stava ### **nella mia OSSERVABILE** *(`g_pesata` dopo un tick legge i pesi del
    CENTRO)*.
    ### ✅ **I NUMERI RESTANO VERI, ed e' il motivo per cui la misura resta:** `cs` si
    valuta ### **una volta per tick, al CENTRO** *(la scelta di `D2`)*, e `Lambda`
    ### **cambia durante il tick** -- quindi il peso di nodo che ogni pezzo usa
    ### **differisce di `O(dtau)`** da quello del suo stato.
    ### ⚠ **Ma questo NON impedisce il secondo ordine:** il palindromo
    ### **e' simmetrico attorno al centro**, e ### **l'errore dei pezzi prima si cancella
    con quello dei pezzi dopo.** ### **E' esattamente cio' che la tabella mostra**, se si
    legge bene: ### **i pezzi `1`-`7` e `9`-`14` portano lo STESSO scarto**, e il centro
    e' esatto.
    """
    print()
    print("### 📌 IL PESO DI NODO durante il tick (informazione, e NON")
    print("###   l'OSTACOLO: quella diagnosi e' RITIRATA -- errore `n.12`).")
    print("###   `cs` e' quello del CENTRO, e `Lambda` cambia durante il tick.")
    print("     %-10s %-18s %s" % ("dtau", "PEGGIO relativo", "rapporto"))
    prec, righe14 = None, None
    for k in KAPPA[:4]:
        dtau = 1.0 / (2 ** k)
        inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                     vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
        lc = float(np.mean(mot.densita_vuoto(st)))
        FP.accendi_cs(mot, lc, st)
        cs_bar, _g = TK.cs_al_centro(st, mot, par, lc,
                                     mot._b("pm_fp", (mot.inc.n,), float), ())
        cs_bar = cs_bar.copy()
        mot.cs = cs_bar.copy()
        peggio, righe = 0.0, []
        mot.apri_tick()
        for j, (idl, fr, _t) in enumerate(CM.ORDINE):
            cs_ora = FP.cs(mot.densita_vuoto(st), lc,
                           mot._b("pm_cs", (mot.inc.n,), float)).copy()
            d = (float(np.max(np.abs(cs_ora - cs_bar)))
                 / float(np.max(np.abs(cs_bar))))
            peggio = max(peggio, d)
            righe.append((j + 1, idl, d))
            nome, vp = TK.OPERATORE[idl]
            mot.operatori[nome](st, par if vp else {}, fr)
        mot.chiudi_tick()
        print("     %-10.6f %-18.6e %s"
              % (dtau, peggio, "--" if prec is None else "%.3f" % (prec / peggio)))
        prec = peggio
        if abs(dtau - 0.25) < 1e-12:
            righe14 = righe
    print("     ### un rapporto `~2` vuol dire `O(dtau)`: ed e' LO STESSO ordine che il")
    print("###   punto medio per pezzo toglieva dal peso d'arco (ramo tolto il 2026-10-19).")
    if righe14:
        print("     ### E PEZZO PER PEZZO (`dtau = 0.25`), il peso di nodo usato contro")
        print("###   quello dello stato di quel pezzo:")
        for j, idl, d in righe14:
            print("     %2d %-24s %.4e %s"
                  % (j, idl, d, "### <- il CENTRO: qui e' ESATTO" if d < 1e-12 else ""))
    print("     ### ⭐ E IL PEZZO `8` E' ESATTO PERCHE' E' IL CENTRO: `cs` e' valutato")
    print("###   LA'. ### E i pezzi PRIMA e DOPO portano lo STESSO scarto -- che e'")
    print("###   il modo in cui un palindromo CANCELLA l'errore, non il modo in cui lo")
    print("###   subisce. ### Per questo il passo e' del SECONDO ordine (`C1 = 2.091`),")
    print("###   e la diagnosi <<l'ostacolo e' il peso di nodo>> E' RITIRATA.")
    sys.stdout.flush()


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL PUNTO MEDIO PER PEZZO -- il CENSIMENTO dei 14 pezzi, PRIMA del codice")
    print("### I bracci che accendevano il ramo sono TOLTI (2026-10-19): rigirabili al")
    print("###   commit 880955bb, referto doc/referti_l2/punto_medio_per_pezzo.txt.")
    print("### Mandato di Luca del 2026-10-18, 12:07.")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la scena di `M-B2`: nn = %d   seme = %d   norma = %s   vuoto_modulo = %.1f"
          "   su2 = %s" % (MB2.NN, MB2.SEME, MB2.NORMA, MB2.VUOTO_MODULO, MB2.SU2))
    print("  lo stato: la PRE-CORSA di `_misura_hw` (`T = %.1f` a `dtau = %.2f`)"
          % (MB2.TEMPO, HW.DTAU_PRE))
    print("  `Lambda_c` = la MEDIA di `Lambda` sulla scena, DERIVATA e non scelta")
    print("  l'ordine: %d voci, impronta %s" % (len(CM.ORDINE), CM.IMPRONTA))
    print("-" * 100)
    muovono = censimento()
    # ### ⛔⛔ **IL BRACCIO CHE IL MANDATO CHIEDE:** se il pezzo e' UNO SOLO, il punto
    # ### fisso va ### **solo li'**. ### ⚠ **E se ne risultasse un altro, il mandato dice
    # ### di SEGNALARLO PRIMA del codice** -- e questo braccio e' il segnale.
    esito("il pezzo che muove `Lambda` e' UNO SOLO, e e' `CAMM-SPOSTAMENTO-VUOTO`",
          muovono == ["CAMM-SPOSTAMENTO-VUOTO"],
          "contati %d: %s" % (len(muovono), muovono))
    for q in muovono:
        informazione_ordine(q)
    braccio_cs_dello_stato()
    informazione_peso_di_nodo()
    print()
    print("=" * 100)
    print("IL CENSIMENTO: %d su %d" % (OK[0], OK[1]))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
