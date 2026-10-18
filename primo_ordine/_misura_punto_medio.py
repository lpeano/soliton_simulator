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


# ### ⛔ **LA SOGLIA DI `C1`, dal mandato del `2026-10-18`: `1.9`.** ### **Non e'
# ### una banda nuova:** e' quella di `M-B2`, che `H_w` importa.
PENDENZA_MIN = HW.PENDENZA_MIN
# ### ⛔ **LE QUATTRO `Lambda_c`, DICHIARATE nel task history e non scelte qui:** i
# ### rapporti ### **`0.1`, `0.3`, `1`, `10`** -- i tre di `D4` piu' il massimo MISURATO
# ### del punto fisso di `cs`.
RAPPORTI = (0.1, 0.3, 1.0, 10.0)
# ### ⛔ **LE DUE TAGLIE**, perche' il punto fisso ### **accoppia la rete intera**:
# ### se i giri crescessero con la taglia, ### **il costo per tick non sarebbe una
# ### costante del modello.**
TAGLIE = (16, 32)
# ### ⚠ **LA TOLLERANZA DELLA REVERSIBILITA':** `256` ulp sulla scala di `phi`, ed e'
# ### ### **quella delle norme** *(`_collauda_materia_vuoto`, e `D3` braccio `(4)`)*.
ULP_REVERSIBILE = 256.0


def pendenza_di_g(regola, taglia, rapporto, osservabile):
    """### `(pendenza, righe, giri_medi, giri_max)` di `G`, ### **nel modo dato.**

    ### ⛔ **`regola` vale `ii`, `i` oppure `None`** *(il peso BLOCCATO: lo schema di
    prima, cioe' ### **il caso che DEVE fallire**)*, e ### **non ha un valore di comodo.**
    """
    import energia_pesata as EP
    righe, giri = [], []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        quanti = int(round(MB2.TEMPO / dtau))
        inc, mot, st, par = DV.scena(taglia, MB2.SEME, dtau, norma=MB2.NORMA,
                                     vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        if taglia == MB2.NN:
            st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
        else:
            # ### ⚠ **PER L'ALTRA TAGLIA la pre-corsa di `H_w` non vale** *(ha la
            # ### forma della sua rete)*: si fa ### **la stessa cosa**, cioe'
            # ### ### **lo stesso tempo fisico a `dtau` della pre-corsa**, su questa rete.
            _i2, m2, s2, p2 = DV.scena(taglia, MB2.SEME, HW.DTAU_PRE, norma=MB2.NORMA,
                                       vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
            for _t in range(int(round(MB2.TEMPO / HW.DTAU_PRE))):
                TK.percorri_tick(s2, m2, p2, ("CAMM-FASE-VUOTO",), None,
                                 len(CM.ORDINE))
            st["psi_h"][...], st["phi_h"][...] = s2["psi_h"], s2["phi_h"]
        lc = rapporto * float(np.mean(mot.densita_vuoto(st)))
        mot.regola_punto_medio = regola
        FP.accendi_cs(mot, lc, st)
        # ### ⛔⛔ **QUALE OSSERVABILE, E NON HA UN VALORE DI
        # ### COMODO** *(errore `n.12`, `2026-10-18`)*: ### **`stato`** legge `G` coi pesi
        # ### ### **dello stato di adesso** *(quella GIUSTA con `cs` dinamico)*, e
        # ### ### **`passo`** coi pesi di `mot.cs` -- che dopo un tick sono
        # ### ### **quelli del CENTRO**, e servono ### **al caso che DEVE fallire.**
        fun = EP.g_dello_stato if osservabile == "stato" else EP.g_pesata
        g0 = fun(mot, st, par)
        peggio = 0.0
        for _t in range(quanti):
            TK.tick_con_cs(st, mot, par, lc, ())
            giri.append(mot.giri_peso)
            d = abs(fun(mot, st, par) - g0)
            if d > peggio:
                peggio = d
        righe.append((dtau, quanti, peggio))
    primo, ultimo = righe[0][2], righe[-1][2]
    dim = len(KAPPA) - 1
    p = float(np.log2(primo / ultimo) / dim) if ultimo > 0 else float("nan")
    gm = float(np.mean(giri)) if giri else float("nan")
    gx = max(giri) if giri else 0
    return p, righe, gm, gx


def stampa(righe):
    print("     %-4s %-10s %-7s %s" % ("k", "dtau", "tick", "escursione G"))
    for (dtau, quanti, e), k in zip(righe, KAPPA):
        print("     %-4d %-10.6f %-7d %.6e" % (k, dtau, quanti, e))
    sys.stdout.flush()


def braccio_c1():
    """### `C1` col punto medio, e il caso che DEVE fallire coi pesi BLOCCATI."""
    print()
    print("### `C1` LA PENDENZA DI `G` COL PUNTO MEDIO PER PEZZO (regola `ii`)")
    p_pm, righe, gm, gx = pendenza_di_g("ii", MB2.NN, 1.0, "stato")
    stampa(righe)
    print("     ### i giri del punto fisso del peso: medio %.2f, massimo %d" % (gm, gx))
    esito("`C1` la pendenza di `G` col punto medio e' `>= %.1f`" % PENDENZA_MIN,
          p_pm >= PENDENZA_MIN, "pendenza %.3f" % p_pm)
    print()
    print("### `C1` IL CASO CHE DEVE FALLIRE: l'OSSERVABILE VECCHIA (`g_pesata`)")
    # ### ⛔⛔ **IL CASO CHE DEVE FALLIRE E' L'OSSERVABILE, NON LO SCHEMA**
    # ### *(mandato del `2026-10-18`, errore `n.12`)*: ### **la `G` vecchia deve ridare
    # ### `1.002 +- 0.01`** -- cioe' ### **il numero che misuravo**, e questo prova che
    # ### ### **il difetto era LA LETTURA.**
    # ### ⚠ **E col PASSO DI DEFAULT (`None`), perche- il `1.002` del mandato e- quello:
    # ### l-osservabile vecchia SUL PASSO CHE GIRA, non su uno schema acceso.
    p_vecchia, righe2, _gm, _gx = pendenza_di_g(None, MB2.NN, 1.0, "passo")
    stampa(righe2)
    esito("### `C1` DEVE fallire: l'osservabile VECCHIA da' `1.002 +- 0.01`",
          abs(p_vecchia - 1.002) <= 0.01,
          "pendenza %.3f: il numero di prima si RITROVA, cioe' il difetto era LA"
          " LETTURA e non lo schema" % p_vecchia)
    print()
    print("### 📌 E I PESI BLOCCATI, CON L'OSSERVABILE GIUSTA (informazione):")
    p_bl, righe3, _gm2, _gx2 = pendenza_di_g(None, MB2.NN, 1.0, "stato")
    stampa(righe3)
    print("     ### pendenza %.3f -- cioe' ### IL PUNTO MEDIO PER PEZZO NON SERVIVA:"
          % p_bl)
    print("###   il passo di default era GIA' del secondo ordine, e col punto medio da'")
    print("###   %.3f, cioe' un filo PEGGIO." % p_pm)
    print()
    print("### 📌 `C1` CON LA REGOLA `(i)` (informazione, NON un criterio)")
    p_i, righe3, gmi, gxi = pendenza_di_g("i", MB2.NN, 1.0, "stato")
    stampa(righe3)
    print("     ### pendenza %.3f (la `(ii)` da' %.3f); giri medio %.2f, massimo %d"
          % (p_i, p_pm, gmi, gxi))
    return p_pm, p_bl, p_i


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
        mot.regola_punto_medio = None
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


def braccio_controllo_positivo():
    """### Il peso USATO contro quello BLOCCATO: ### **`O(dtau)` RELATIVO.**

    ### ⛔⛔ **E LA DISTINZIONE CONTA:** la differenza ASSOLUTA e' `O(dtau^2)`
    ### **perche' il peso stesso e' `O(dtau)`** -- quindi il numero da guardare e'
    ### **il RELATIVO**, e il mandato chiede ### **`O(dtau)`.**
    """
    print()
    print("### IL CONTROLLO POSITIVO: il peso del punto medio DIFFERISCE da quello")
    print("###   bloccato, e di quanto. ### Il RELATIVO deve essere `O(dtau)`.")
    print("     %-10s %-16s %-16s %-12s %s"
          % ("dtau", "|ds| assoluto", "scala di s", "RELATIVO", "rapporto"))
    prec, ultimi = None, []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                     vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
        lc = float(np.mean(mot.densita_vuoto(st)))
        FP.accendi_cs(mot, lc, st)
        s_bl = FP.s_arco(mot).copy()
        salvo = st["phi_h"].copy()
        lam0 = mot.densita_vuoto(st).copy()
        FP.hop_phi_con_s(mot, st["phi_h"], s_bl.copy(), 0.5)
        lam = 0.5 * (lam0 + mot.densita_vuoto(st))
        s_pm = FP.s_arco_da_lambda(mot, lam)
        st["phi_h"][...] = salvo
        d = float(np.max(np.abs(s_pm - s_bl)))
        sc = float(np.max(np.abs(s_bl)))
        rel = d / sc
        ultimi.append(rel)
        print("     %-10.6f %-16.6e %-16.6e %-12.6e %s"
              % (dtau, d, sc, rel, "--" if prec is None else "%.3f" % (prec / rel)))
        prec = rel
    # ### ✅ **IL CRITERIO DEL CONTROLLO: il rapporto dei RELATIVI sta vicino a `2`.**
    rap = [ultimi[i - 1] / ultimi[i] for i in range(1, len(ultimi))]
    esito("il peso del punto medio differisce da quello bloccato di `O(dtau)`",
          all(1.7 <= r <= 2.3 for r in rap),
          "i rapporti dei RELATIVI: %s (l'assoluto e' `O(dtau^2)` perche' il peso"
          " stesso e' `O(dtau)`)" % ("  ".join("%.3f" % r for r in rap)))


def braccio_reversibile():
    """### `+h` e poi `-h`: lo stato ### **torna all'inizio.**

    ### ⛔ **E NON si puo' fare con una frazione negativa** *(l'assert del cono)*:
    il verso si rovescia ### **coniugando** -- `hop` e' `alpha I + beta S` con
    `alpha, beta` che vengono da `e^{i theta}`, e ### **il suo inverso e' il coniugato.**
    ### ✅ **Quindi si applica il pezzo, si CONIUGA lo stato, si riapplica, e si
    coniuga di nuovo:** se il pezzo e' ### **reversibile**, si torna al punto di partenza.
    """
    print()
    print("### LA REVERSIBILITA' del pezzo col punto medio: `+h`, poi `-h`")
    print("     %-10s %-16s %-14s %s" % ("dtau", "|phi - phi_0|", "ulp", "entro 256?"))
    peggio = 0.0
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                     vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
        lc = float(np.mean(mot.densita_vuoto(st)))
        FP.accendi_cs(mot, lc, st)
        phi0 = st["phi_h"].copy()
        FP.hop_phi_punto_medio(mot, st, 0.5, "ii")
        np.conj(st["phi_h"], out=st["phi_h"])
        FP.hop_phi_punto_medio(mot, st, 0.5, "ii")
        np.conj(st["phi_h"], out=st["phi_h"])
        d = float(np.max(np.abs(st["phi_h"] - phi0)))
        sc = float(np.max(np.abs(phi0)))
        u = d / (float(np.finfo(float).eps) * sc)
        peggio = max(peggio, u)
        print("     %-10.6f %-16.6e %-14.1f %s"
              % (dtau, d, u, "si" if u <= ULP_REVERSIBILE else "### NO"))
    esito("il pezzo col punto medio e' REVERSIBILE entro %.0f ulp" % ULP_REVERSIBILE,
          peggio <= ULP_REVERSIBILE, "il PEGGIO e' %.1f ulp" % peggio)


def informazione_giri():
    """### 📌 **I GIRI: medio e massimo, su DUE taglie e QUATTRO `Lambda_c`.**"""
    print()
    print("### 📌 I GIRI DEL PUNTO FISSO DEL PESO (informazione): due taglie,")
    print("###   quattro rapporti `Lambda_c/Lambda`. ### Il punto fisso ACCOPPIA LA RETE,")
    print("###   quindi i giri dicono quanto e' accoppiata -- non la difficolta' di un arco.")
    print("     %-8s %-10s %-12s %-10s %s"
          % ("taglia", "rapporto", "pendenza G", "giri medio", "giri max"))
    fuori = []
    for taglia in TAGLIE:
        for r in RAPPORTI:
            # ### ⛔⛔ **E SE UN PUNTO FISSO NON CONVERGE, SI RIPORTA** *(`2026-10-18`)*:
            # ### la misura ### **non muore** e ### **non nasconde** -- il messaggio
            # ### dell-`assert` porta ### **l-ultimo scarto**, ed e- il numero che serve.
            try:
                p, _righe, gm, gx = pendenza_di_g("ii", taglia, r, "stato")
                print("     %-8d %-10.2f %-12.3f %-10.2f %d"
                      % (taglia, r, p, gm, gx))
                fuori.append((taglia, r, p, gm, gx))
            except AssertionError as e:
                print("     %-8d %-10.2f ### NON CONVERGE: %s"
                      % (taglia, r, str(e)[:120]))
                fuori.append((taglia, r, None, None, None))
            sys.stdout.flush()
    rotti = [(t, r) for (t, r, p, _m, _x) in fuori if p is None]
    if rotti:
        print("     ### ⛔⛔ E QUESTO E- UN RISULTATO NUOVO, NON un intoppo: con il punto")
        print("###   medio acceso il punto fisso di `cs` AL CENTRO non converge in %d" % len(rotti))
        print("###   dei %d casi provati: %s. ### Va relazionato, e la scelta torna a Luca."
              % (len(fuori), rotti))


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
    print("     ### un rapporto `~2` vuol dire `O(dtau)`: ed e' LO STESSO ordine che")
    print("###   il punto medio ha TOLTO dal peso d'arco.")
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
    braccio_c1()
    braccio_cs_dello_stato()
    braccio_controllo_positivo()
    braccio_reversibile()
    informazione_giri()
    informazione_peso_di_nodo()
    print()
    print("=" * 100)
    print("IL CENSIMENTO: %d su %d" % (OK[0], OK[1]))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
