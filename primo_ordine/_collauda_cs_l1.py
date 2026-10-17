# -*- coding: utf-8 -*-
r"""`D3` — **`L1` RESTA CHIUSO CON `cs` DINAMICO?** I quattro criteri, con la forma ACCESA.

> ### ⛔ **I CRITERI VENGONO DALLA TABELLA DI `D`** *(task history del `2026-10-17`)*, e
> ### **qui non se ne inventa nessuno:**
> ### **`0` violatori del tempo proprio** · ### **`M-B2` pendenza `>= 1.9` su `>= 4`
> dimezzamenti** · ### **`W A W A^-1 = 1` a `<= 8` ulp su `>= 8` stati** ·
> ### **norme `M` e `V` conservate.**

## ⭐⭐ COME SI EVITA DI RISCRIVERE UN CRITERIO

### ⛔ **Un criterio che vive in due posti DIVERGE**, ed e' la regola
`STRUMENTO-LEGGE-DALLA-TABELLA` applicata ### **ai criteri** invece che alle leggi.
### ✅ **Quindi qui si IMPORTA tutto cio' che e' un criterio:** `h_tot` e la scena di
`M-B2` da `_misura_mb2`, i ### **semi** e la ### **banda** da `_misura_completa_l2`,
`passo_cs` e `antiunitaria` da `_misura_theta_nonlineare`, il censimento dei pezzi da
`_collauda_tempo_proprio`.
### ⚠ **Si scrivono SOLO i cicli**, e il motivo e' un fatto letto prima di progettare:
### **`_misura_mb2.una_corsa` chiama `TK.tick`**, cioe' ### **la forma SPENTA** — e
accendere `cs` sul motore ### **non basta** a cambiare quel che quella funzione fa.

## ⛔⛔ `Lambda_c` NON E' UNA MANOPOLA

### **Si prende la MEDIA di `Lambda` sulla scena** *(rapporto `1`)*, ### **una volta e
PRIMA della corsa** — come il mandato del guardiano del `2026-10-17` chiede:
### **`Lambda_c` non si calcola MAI dallo stato DURANTE la corsa.**
### 📌 **E il rapporto e' un'ETICHETTA:** con un rapporto diverso i numeri sono altri, e
### **questo va detto invece di presentare un numero come se fosse IL numero.**

## ⭐ IL BRACCIO `0`, E PERCHE' VIENE PRIMA

### ⛔ **A forma SPENTA questo file deve dare gli stessi numeri degli strumenti
originali.** ### ⚠ **Senza quel braccio, un numero diverso non si saprebbe attribuire a
`cs` o a una mia riscrittura del ciclo** — e sarebbe ### **inutile.**

Gira con:  python primo_ordine/_collauda_cs_l1.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _collauda_tempo_proprio as TP                          # noqa: E402
import _misura_completa_l2 as CL2                             # noqa: E402
import _misura_mb2 as MB2                                     # noqa: E402
import _misura_theta_n as TN                                  # noqa: E402
import _misura_theta_nonlineare as TNL                        # noqa: E402
import composizione as CM                                     # noqa: E402
import corrente as CO                                         # noqa: E402
import deriva as DV                                           # noqa: E402
import energia_pesata as EP                                   # noqa: E402
import tick as TK                                             # noqa: E402

OK = [0, 0]
EPSM = float(np.finfo(float).eps)

# ### ⛔ **IL RAPPORTO E' UN'ETICHETTA, NON UNA TARATURA** *(`A1`)*: `Lambda_c` si
# ### ### **deriva dalla scena** e non si sceglie.
RAPPORTO_LAMBDA_C = 1.0
# ### ⛔ **CINQUE PUNTI = QUATTRO DIMEZZAMENTI**, che e' il `>= 4` del criterio.
# ### ⚠ **Misurato prima di fissarlo:** a `k = 3` una corsa con `cs` costa `0.3` s e
# ### ### **`11.2` giri di punto fisso per tick** -- quindi `k = 5` sta in un secondo, e
# ### ### **il criterio non e' stato scelto per far stare i tempi.**
KAPPA_D3 = (1, 2, 3, 4, 5)
PENDENZA_MIN = 1.9
# ### ⛔ **LA BANDA DELLE NORME:** `256` ulp sulla scala della norma stessa. ### ⚠ **E
# ### non e' una banda nuova: e' quella che `_collauda_materia_vuoto` usa per le norme.**
ULP_NORME = 256.0
TICK_NORME = 64


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def lambda_c_di(mot, st):
    """### `Lambda_c` ### **dalla scena, UNA volta e PRIMA della corsa.**"""
    return RAPPORTO_LAMBDA_C * float(np.mean(mot.densita_vuoto(st)))


# ====================================================================== (0) il braccio 0
def braccio_zero():
    """### `(0)` **A FORMA SPENTA, i miei cicli sono quelli degli strumenti.**"""
    print()
    print("### (0) IL BRACCIO 0: a forma SPENTA i cicli di questo file sono quelli")
    print("###     degli strumenti originali. Senza, nulla di sotto si attribuisce.")
    k = KAPPA_D3[1]
    dtau = 1.0 / (2 ** k)
    tick = int(round(MB2.TEMPO / dtau))
    mia, h0 = una_corsa_cs(dtau, tick, None, "h_tot")
    loro, h0l = MB2.una_corsa(dtau, tick)
    # ### ⛔⛔ **L-ESCURSIONE AL BIT, `H(0)` AGLI ULP, E IL PERCHE- DELLA
    # ### DIFFERENZA** *(`2026-10-18`)*: da quando il criterio si legge su `G`, la linea
    # ### di base viene da ### **`energia_pesata.termini_di_h`** e quella di `M-B2` da
    # ### ### **`h_tot`** -- due fonti che sommano ### **NELLO STESSO ordine di grandezza
    # ### ma non nello stesso ORDINE**, e la somma di float ### **non commuta.**
    # ### ✅ **L-ESCURSIONE invece DEVE coincidere al bit**, perche- e- un massimo di
    # ### differenze e ### **lo scarto costante fra le due fonti si cancella.**
    esito("(0) `M-B2`: il mio ciclo a forma SPENTA e' il suo AL BIT",
          mia == loro and h0 == h0l,
          "escursione %.17g, `H(0)` %.17g: STESSO funzionale, STESSO ciclo" % (mia, h0))
    # ### ⭐ **E QUANTO DISTANO LE DUE FONTI, misurato e non supposto:** `G` a forma
    # ### spenta e `h_tot` ### **sommano gli STESSI termini in ordine DIVERSO.**
    _i0, m0, s0, p0 = DV.scena(MB2.NN, MB2.SEME, 0.25, norma=MB2.NORMA,
                               vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    _g, _h = EP.g_pesata(m0, s0, p0), MB2.h_tot(_i0, m0, s0, p0)
    _u = abs(_g - _h) / (float(np.finfo(float).eps) * abs(_h))
    esito("(0) e le DUE FONTI di `H` distano %.1f ulp (l'ordine della somma)" % _u,
          _u <= 4096.0,
          "`%.17g` contro `%.17g`: una somma di float NON COMMUTA" % (_g, _h))
    # ### e la simmetria: il mio ciclo contro `passo` di `_misura_theta_nonlineare`
    ii, jj, _nn = CO.toro(TN.LATI)
    P = TN._inversione(TN.LATI, ii, jj)
    d_mio = una_simmetria(TN.DTAU[1], CL2.SEMI[0], P, "spenta", None)
    _i, mot, st = TN.scena(TN.DTAU[1], True, True)
    s0 = TNL.stato_di_prova(mot, st, CL2.SEMI[0],
                            vuoti=CL2.VUOTI_PER_SEME.get(CL2.SEMI[0], ()))
    TNL.metti(st, TNL.antiunitaria(s0, P, inversa=True))
    TNL.passo(mot, st)
    TNL.metti(st, TNL.antiunitaria((st["psi_h"].copy(), st["phi_h"].copy()), P))
    fine = TNL.passo(mot, st)
    d_loro, _s = TNL.scarto(fine, s0)
    esito("(0) la simmetria: il mio ciclo a forma SPENTA e' il suo AL BIT",
          d_mio[0] == d_loro,
          "scarto %.6e contro %.6e" % (d_mio[0], d_loro))


# ====================================================================== (1) tempo proprio
def braccio_tempo_proprio():
    """### `(1)` **Con `cs` acceso, nessun pezzo smette di dipendere da `dtau`.**

    ### ⛔ **PERCHE' `cs` POTREBBE ROMPERLO, ed e' la ragione del braccio:**
    `dtau_nodo` restituisce ### **`dtau * cs`**, quindi un pezzo lo vede
    ### **moltiplicato** — e se `cs` dipendesse da `dtau` in modo da cancellarlo, il
    pezzo diventerebbe ### **indipendente dal tempo proprio.**
    ### ✅ **`cs = 0` non puo' succedere:** il vuoto nullo e' ### **vietato alla
    costruzione** *(decisione di Luca del `2026-10-17`)*.
    ### ⚠ **E su UN pezzo <<al centro del palindromo>> non ha senso** *(un pezzo non e'
    un tick)*: qui la forma e' ### **accesa sullo stato di partenza**, che e' la sola
    forma definita per un pezzo solo. ### **E lo dico invece di lasciarlo capire.**
    """
    print()
    print("### (1) IL TEMPO PROPRIO con `cs` ACCESO: 0 violatori, e sono 12 pezzi")
    visti = []
    deboli = []
    for idl, frazione, _t in CM.ORDINE:
        d = TP.dipende_da_dtau(idl, frazione, rapporto_cs=RAPPORTO_LAMBDA_C)
        if d <= TP.CAMBIA_MIN:
            visti.append((idl, frazione, d))
        else:
            deboli.append((idl, d))
    piu_debole = min(deboli, key=lambda r: r[1]) if deboli else ("--", 0.0)
    esito("(1) con `cs` acceso i violatori sono `0` su %d pezzi" % len(CM.ORDINE),
          not visti,
          "il piu' DEBOLE e' `%s` con %.3e (la soglia e' %.0e)"
          % (piu_debole[0], piu_debole[1], TP.CAMBIA_MIN))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE, e viene dal `2-septies`:** un pezzo col passo
    # ### del motore FISSO e' ### **indipendente da `dtau`**, e deve risultare violatore
    # ### ### **anche con `cs` acceso.**
    d = TP.dipende_da_dtau("CAMM-MATERIA-VUOTO", 0.5, dtau_fisso=0.3, rapporto_cs=RAPPORTO_LAMBDA_C)
    esito("### (1) DEVE fallire: col passo FISSO il pezzo e' VIOLATORE anche con `cs`",
          d <= TP.CAMBIA_MIN,
          "|differenza| = %.1e: senza questo, `(1)` passerebbe anche con la misura CIECA"
          % d)


# ====================================================================== (2) M-B2
def una_corsa_cs(dtau, tick, lambda_c, quale):
    """### `(escursione, H0)` ### **con `cs` al centro**, oppure a forma spenta.

    ### ⚠ **Il ciclo e' scritto qui perche' `MB2.una_corsa` chiama `TK.tick`**, cioe'
    la forma spenta: ### **`h_tot` e la scena si IMPORTANO**, e sono il criterio.
    """
    inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    lc = lambda_c_di(mot, st) if lambda_c == "dalla scena" else lambda_c
    # ### ⛔⛔ **IL CRITERIO `(2)` SI LEGGE SU `G`, NON SU `H_tot`**
    # ### *(decisione di Luca del `2026-10-18`, `00:07`, punto `1`)*: con `cs` NON
    # ### uniforme ### **`H_tot` non e' l'invariante** -- lo e' il generatore PESATO.
    # ### ✅ **E a forma SPENTA i due COINCIDONO** *(i pesi sono `1`)*, quindi il
    # ### braccio `0` di questo file ### **continua a confrontarsi con `M-B2`.**
    # ### ⚠ **E LA FORMA SI ACCENDE PRIMA DELLA LINEA DI BASE**, altrimenti `g0`
    # ### sarebbe ### **`H_tot`** e l'escursione misurerebbe ### **uno scarto costante**
    # ### invece della deriva -- e' il difetto che ho trovato in `_misura_hw` il
    # ### `2026-10-18`.
    import flussi_parziali as FP
    if lc is not None:
        FP.accendi_cs(mot, lc, st)
    # ### ⛔⛔ **`quale` NON HA UN VALORE DI COMODO** *(`2026-10-18`)*: il CRITERIO
    # ### si legge su ### **`G`** *(decisione di Luca)*, ma ### **il braccio `0` deve
    # ### confrontare LO STESSO FUNZIONALE di `M-B2`** -- altrimenti confronta
    # ### ### **due fonti che sommano in ordine diverso**, e la differenza *(misurata:
    # ### ### **`~2700` ulp sull'escursione**)* ### **non dice niente sul CICLO.**
    # ### ⚠ **E la frase che avevo scritto -- <<lo scarto costante si cancella in un
    # ### massimo di differenze>> -- ERA FALSA**, e la misura l'ha smentita subito.
    fun = EP.g_pesata if quale == "G" else (
        lambda m, s, p: MB2.h_tot(inc, m, s, p))
    h0 = fun(mot, st, par)
    peggio, giri = 0.0, 0
    for _t in range(tick):
        if lc is None:
            TK.tick(st, mot, par)
        else:
            giri += TK.tick_con_cs(st, mot, par, lc, ())
        d = abs(fun(mot, st, par) - h0)
        if d > peggio:
            peggio = d
    if lc is None:
        return peggio, h0
    return peggio, h0, giri, lc


def pendenza_mb2(modo, uniforme=None):
    """### La pendenza complessiva di `H_tot` su `KAPPA_D3`, ### **nel modo dato.**

    ### ⛔⛔ **`uniforme` E- LA PROVA CHE DISCRIMINA** *(aggiunta il `2026-10-17`,
    dopo che il criterio `(2)` e- FALLITO)*: con `cs` ### **COSTANTE su tutti i nodi** il
    passo e- lo ### **Strang di `c * H_tot`**, cioe- ### **lo stesso passo di oggi con il
    tempo riscalato** -- e la- `H_tot` ### **E- l-invariante**, quindi la pendenza
    ### **deve tornare `~2`.**
    ### ✅ **Se torna, il ciclo e- giusto e la causa e- LA NON UNIFORMITA- di `cs`;
    se non tornasse, il difetto sarebbe MIO.** ### **E- questo che separa le due
    spiegazioni**, e senza di lui il numero `-0.003` non direbbe quale delle due.
    """
    import flussi_parziali as FP
    righe = []
    for k in KAPPA_D3:
        dtau = 1.0 / (2 ** k)
        tick = int(round(MB2.TEMPO / dtau))
        if modo == "inizio":
            inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                         vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
            lc = lambda_c_di(mot, st)
            h0 = MB2.h_tot(inc, mot, st, par)
            peggio = 0.0
            for _t in range(tick):
                FP.accendi_cs(mot, lc, st)
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                d = abs(MB2.h_tot(inc, mot, st, par) - h0)
                if d > peggio:
                    peggio = d
            FP.spegni_cs(mot)
            righe.append((dtau, tick, peggio, 0))
        elif uniforme is not None:
            inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                         vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
            h0 = MB2.h_tot(inc, mot, st, par)
            peggio = 0.0
            for _t in range(tick):
                # ### ⚠⚠ **`cs` SI RIMETTE A OGNI TICK, E NON PERCHE- IL MOTORE LO AZZERI:**
                # ### ### **quel commento era SBAGLIATO, e l-avevo scritto io** *(corretto il
                # ### `2026-10-17`)*. ### ✅ **`chiudi_tick` NON tocca `cs`**, e l-ho
                # ### ### **verificato correndo**: dopo un tick `mot.cs` e- intatto.
                # ### ⚠ **Si rimette per rendere ESPLICITO che il peso di questo modo e-
                # ### COSTANTE**, cioe- che il ciclo non dipende da cio- che un tick
                # ### lascia dietro: ### **e- una riga che non serve, non una riga che cura.**
                mot.cs = np.full(mot.inc.n, float(uniforme))
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                d = abs(MB2.h_tot(inc, mot, st, par) - h0)
                if d > peggio:
                    peggio = d
            FP.spegni_cs(mot)
            righe.append((dtau, tick, peggio, 0))
        else:
            fuori = una_corsa_cs(dtau, tick, "dalla scena", "G")
            righe.append((dtau, tick, fuori[0], fuori[2]))
    primo, ultimo = righe[0][2], righe[-1][2]
    dim = len(KAPPA_D3) - 1
    pend = float(np.log2(primo / ultimo) / dim) if ultimo > 0 else float("nan")
    return pend, righe, dim


def braccio_mb2():
    """### `(2)` **`M-B2` con `cs` al centro: il secondo ordine su `H_tot`.**"""
    print()
    print("### (2) `M-B2` con `cs` AL CENTRO: la pendenza di `H_tot` su %d dimezzamenti"
          % (len(KAPPA_D3) - 1))
    pend, righe, dim = pendenza_mb2("centro")
    print("     %-4s %-10s %-7s %-14s %s" % ("k", "dtau", "tick", "escursione", "giri"))
    for (dtau, tick, err, giri), k in zip(righe, KAPPA_D3):
        print("     %-4d %-10.6f %-7d %-14.6e %d" % (k, dtau, tick, err, giri))
    esito("(2) la pendenza di `G` con `cs` al CENTRO e' `>= %.1f`" % PENDENZA_MIN,
          pend >= PENDENZA_MIN,
          "pendenza %.3f su %d dimezzamenti (a forma spenta `M-B2` da' 1.965 su 5)"
          % (pend, dim))
    # ### ⛔⛔ **LA DIAGNOSI, e NON e' un criterio:** con `cs` ### **UNIFORME**
    # ### il passo e' lo ### **Strang di `c * H_tot`**, e la' `H_tot` ### **E' l'invariante.**
    # ### ✅ **Se la pendenza torna `~2`, il ciclo e' giusto** e la causa del `(2)` e'
    # ### ### **la NON UNIFORMITA' di `cs`**; se non tornasse, ### **il difetto sarebbe
    # ### MIO.** ### **Senza questa prova il numero di sopra non dice QUALE delle due.**
    print("     LA DIAGNOSI (informazione, NON un criterio): `cs` UNIFORME")
    diag = {}
    for c in (1.0, 0.5):
        p_u, r_u, _d = pendenza_mb2("uniforme", uniforme=c)
        diag[c] = p_u
        print("     `cs` = %.2f su tutti i nodi -> pendenza %.3f   (%.3e -> %.3e)"
              % (c, p_u, r_u[0][2], r_u[-1][2]))
    esito("(2) LA DIAGNOSI: con `cs` UNIFORME la pendenza TORNA `>= %.1f`"
          % PENDENZA_MIN,
          min(diag.values()) >= PENDENZA_MIN,
          "`cs=1` %.3f e `cs=0.5` %.3f: il CICLO E' GIUSTO, e la causa del `(2)` e' che"
          " `H_tot` NON e' l'invariante di un `cs` che VARIA fra i nodi"
          % (diag[1.0], diag[0.5]))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: `cs` a INIZIO PASSO.**
    # ### ⛔⛔ **E QUESTO BRACCIO PRETENDE ANCHE CHE IL `(2)` SIA PASSATO**, e il
    # ### motivo e' che ### **un caso finto che fallisce mentre fallisce anche il caso
    # ### VERO non dimostra niente:** sarebbe ### **un FALSO-UNO.**
    # ### ✅ **Finche' il `(2)` e' rosso, questo DEVE essere rosso anche lui** -- e
    # ### non e' pessimismo, e' che ### **non ha materia.**
    pend_i, _r, _d = pendenza_mb2("inizio")
    esito("### (2) DEVE fallire: `cs` a INIZIO PASSO perde il secondo ordine",
          pend_i < PENDENZA_MIN and pend >= PENDENZA_MIN,
          "pendenza %.3f contro %.3f del caso vero: se il caso VERO e' rosso questo"
          " braccio NON HA MATERIA, e lo dice invece di passare" % (pend_i, pend))
    return pend, pend_i, diag


# ====================================================================== (3) la simmetria
def una_simmetria(dtau, seme, P, modo, lambda_c):
    """### `(scarto, scala)` di `W A W A^-1 s` da `s`, ### **nel modo dato.**"""
    import flussi_parziali as FP
    _i, mot, st = TN.scena(dtau, True, True)
    s0 = TNL.stato_di_prova(mot, st, seme, vuoti=CL2.VUOTI_PER_SEME.get(seme, ()))
    lc = lambda_c_di(mot, st) if lambda_c == "dalla scena" else lambda_c
    FP.spegni_cs(mot)
    TNL.metti(st, TNL.antiunitaria(s0, P, inversa=True))
    TNL.passo_cs(mot, st, modo, lc)
    TNL.metti(st, TNL.antiunitaria((st["psi_h"].copy(), st["phi_h"].copy()), P))
    fine = TNL.passo_cs(mot, st, modo, lc)
    FP.spegni_cs(mot)
    return TNL.scarto(fine, s0)


def braccio_simmetria():
    """### `(3)` **`W A W A^-1 = 1` su `8` stati, banda `8` ulp.**

    ### ⛔⛔ **E' IL BRACCIO CHE HO DICHIARATO PIU' FRAGILE PRIMA DI MISURARLO**, nel
    task history di `D3`: la banda e' ### **`8` ulp** *(`512` volte piu' stretta di
    quella della `PTheta`)*, e il punto fisso di `cs` ### **si ferma agli ulp**, cioe'
    ### **aggiunge un arrotondamento che la forma spenta non ha.**
    ### ⚠ **Se sfonda, il numero si riporta e LA BANDA RESTA `8`.**
    """
    print()
    print("### (3) LA SIMMETRIA con `cs` AL CENTRO: %d stati, banda %.0f ulp"
          % (len(CL2.SEMI), CL2.ULP_SIMMETRIA))
    ii, jj, _nn = CO.toro(TN.LATI)
    P = TN._inversione(TN.LATI, ii, jj)
    for dtau in (TN.DTAU[1], TN.DTAU[2]):
        peggio, dove = 0.0, None
        for seme in CL2.SEMI:
            d, sc = una_simmetria(dtau, seme, P, "centro", "dalla scena")
            u = d / (EPSM * sc)
            if u > peggio:
                peggio, dove = u, seme
        esito("(3) dtau=%.4f: `<= %.0f` ulp su tutti gli %d stati"
              % (dtau, CL2.ULP_SIMMETRIA, len(CL2.SEMI)),
              peggio <= CL2.ULP_SIMMETRIA,
              "il PEGGIO e' %.2f ulp (seme %s)" % (peggio, dove))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: `cs` a INIZIO PASSO**
    d, sc = una_simmetria(TN.DTAU[1], CL2.SEMI[0], P, "inizio", "dalla scena")
    esito("### (3) DEVE fallire: `cs` a INIZIO PASSO sfonda la banda",
          d > CL2.ULP_SIMMETRIA * EPSM * sc,
          "scarto %.3e, cioe' %.0f ulp" % (d, d / (EPSM * sc)))


# ====================================================================== (4) le norme
def braccio_norme():
    """### `(4)` **`M` e `V` con `cs` acceso: conservate, non <<quasi>>.**

    ### ⛔ **PERCHE' DEVONO:** `cs` ### **non aggiunge un termine** — scala il tempo
    proprio ### **dentro pezzi unitari per costruzione.** ### ⚠ **Se una delle due
    derivasse, `cs` entrerebbe DOVE NON DEVE**, e sarebbe un difetto, non un numero.
    """
    print()
    print("### (4) LE NORME `M` e `V` su %d tick con `cs` acceso" % TICK_NORME)
    _i, mot, st, par = DV.scena(MB2.NN, MB2.SEME, 0.25, norma=MB2.NORMA,
                                vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    lc = lambda_c_di(mot, st)
    m0 = float(np.sum(np.abs(st["psi_h"]) ** 2))
    v0 = float(np.sum(np.abs(st["phi_h"]) ** 2))
    for _t in range(TICK_NORME):
        TK.tick_con_cs(st, mot, par, lc, ())
    m1 = float(np.sum(np.abs(st["psi_h"]) ** 2))
    v1 = float(np.sum(np.abs(st["phi_h"]) ** 2))
    esito("(4) la norma `M` si conserva entro %.0f ulp" % ULP_NORME,
          abs(m1 - m0) <= ULP_NORME * EPSM * m0,
          "da %.9f a %.9f, cioe' %.1f ulp" % (m0, m1, abs(m1 - m0) / (EPSM * m0)))
    esito("(4) la norma `V` si conserva entro %.0f ulp" % ULP_NORME,
          abs(v1 - v0) <= ULP_NORME * EPSM * v0,
          "da %.9f a %.9f, cioe' %.1f ulp" % (v0, v1, abs(v1 - v0) / (EPSM * v0)))
    # ### ⭐ **E IL BRACCIO HA MATERIA: lo stato SI E' MOSSO.** ### ⚠ **Senza, due norme
    # ### uguali direbbero solo che non e' successo niente.**
    esito("(4) e il braccio HA MATERIA: `cs` NON e' uniforme",
          float(np.max(mot.cs) - np.min(mot.cs)) > 1e-6,
          "`cs` va da %.6f a %.6f: se fosse uniforme la forma non starebbe facendo"
          " niente" % (float(np.min(mot.cs)), float(np.max(mot.cs))))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 100)
    print("`D3`: `L1` RESTA CHIUSO CON `cs` DINAMICO? -- i quattro criteri della tabella")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  `M-B2`: nn = %d   seme = %d   T = %.1f   norma = %s   vuoto_modulo = %.1f"
          "   su2 = %s" % (MB2.NN, MB2.SEME, MB2.TEMPO, MB2.NORMA, MB2.VUOTO_MODULO,
                           MB2.SU2))
    print("  la simmetria: toro %s   semi %s   banda %.0f ulp   vuoti %s"
          % (TN.LATI, CL2.SEMI, CL2.ULP_SIMMETRIA, CL2.VUOTI_PER_SEME))
    print("  `Lambda_c` = %.1f x la MEDIA di `Lambda` sulla scena, calcolata UNA volta"
          " e PRIMA della corsa" % RAPPORTO_LAMBDA_C)
    print("  i dimezzamenti: k in %s   la pendenza minima: %.1f   le norme: %d tick,"
          " banda %.0f ulp" % (KAPPA_D3, PENDENZA_MIN, TICK_NORME, ULP_NORME))
    sys.stdout.flush()
    braccio_zero()
    braccio_tempo_proprio()
    pend, pend_i, diag = braccio_mb2()
    braccio_simmetria()
    braccio_norme()
    print("=" * 100)
    print("`D3`: %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E NESSUNA CONCLUSIONE DI FISICA: qui ci sono numeri. Che cosa voglia")
    print("###   dire <<`L1` resta chiuso>> e' una lettura, e la decide Luca.")
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
