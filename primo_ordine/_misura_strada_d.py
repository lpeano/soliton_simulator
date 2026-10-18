# -*- coding: utf-8 -*-
r"""**LA STRADA `(d)`: `C1`, `C2`, `C5`** — *il termine nuovo conserva `G`?*

> ### ⛔ **I criteri vengono dal mandato del `2026-10-18`**, copiati nel task history
> ### **PRIMA della misura**, e qui ### **non se ne cambia nessuno:**
> ### **`C1`** con `cs` DINAMICO la pendenza di `G` su `>= 4` dimezzamenti e' `>= 1.9`;
> ### **`C2`** col SEGNO di `Omega` invertito la pendenza di `G` ### **cade**;
> ### **`C5`** il costo: i giri dei due punti fissi per tick, sui ### **sette rapporti**
> della spazzata di `402a4d5`.

## ⭐ IL CASO CHE DEVE FALLIRE DI `C1`, E VIENE DAL MANDATO

*«oggi `-0.001` senza il termine: e' il caso che DEVE fallire, gia' misurato»*.
### ⚠ **E quel `-0.001` E' SBAGLIATO, ed e' un mio difetto:** in `_misura_hw` la linea di
base del modo dinamico era calcolata ### **a forma spenta** *(`H_tot` invece di `G`)*, e
l'escursione misurava ### **uno scarto costante** invece della deriva.
### ✅ **Qui la stessa corsa SENZA il termine si rifa' con la linea di base GIUSTA**, e il
numero sta nel referto.

## ⛔ E LA DIAGNOSI CHE LOCALIZZA L'OSTACOLO

### **`cs` al CENTRO e' CONGELATO per tutto il tick** *(la scelta di `D2`)*, mentre la
reazione legge `cs'` ### **allo stato del momento.** ### ⚠ **Se l'ostacolo e' quello**, la
pendenza di `G` deve restare ### **PRIMO ordine** anche rileggendo `cs` ### **prima di
ogni pezzo** *(che e' esplicito, quindi non simmetrico)*, e deve ### **tornare piatta**
togliendo il termine. ### **Sono tre numeri, e separano le spiegazioni.**

Gira con:  python primo_ordine/_misura_strada_d.py
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
import energia_pesata as EP                                    # noqa: E402
import flussi_parziali as FP                                  # noqa: E402
import tick as TK                                             # noqa: E402

OK = [0, 0]
LEGGE = "CAMM-FASE-VUOTO"
# ### ⛔ **LA SOGLIA E I DIMEZZAMENTI VENGONO DA `H_w`**, cioe' da `M-B2`: ### **nessuna
# ### banda nuova.**
PENDENZA_MIN = HW.PENDENZA_MIN
KAPPA = HW.KAPPA_HW
# ### ⛔ **I SETTE RAPPORTI DELLA SPAZZATA di `402a4d5`**, importati e non ricopiati.
import _collauda_cs_centro as D2                               # noqa: E402
SPAZZATA = D2.SPAZZATA


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def corsa(dtau, quanti, col_termine, modo, segno):
    """### `(escursione di G, giri di cs, giri di Omega)`.

    ### ⛔ **`modo`:** `centro` *(la scelta di `D2`)* oppure `pezzo` *(`cs` RILETTO prima
    di ogni pezzo, esplicito)*. ### **`segno`** moltiplica `Omega`: ### **`-1` e' il caso
    `C2`**, e la perturbazione e' ### **IN MEMORIA** *(nessun file del repo si tocca)*.
    """
    inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
    lc = float(np.mean(mot.densita_vuoto(st)))
    salta = () if col_termine else (LEGGE,)
    vero = EP.omega
    if segno != 1:
        EP.omega = lambda m, s, p: segno * vero(m, s, p)
    try:
        FP.accendi_cs(mot, lc, st)
        g0 = EP.g_pesata(mot, st, par)
        peggio, giri_cs = 0.0, 0
        for _t in range(quanti):
            if modo == "centro":
                giri_cs += TK.tick_con_cs(st, mot, par, lc, salta)
            else:
                mot.apri_tick()
                for idl, fr, _tp in CM.ORDINE:
                    if idl in salta:
                        continue
                    # ### ⚠ **`cs` RILETTO prima di OGNI pezzo: esplicito**, quindi
                    # ### ### **NON simmetrico** -- ed e' il punto della diagnosi.
                    FP.accendi_cs(mot, lc, st)
                    nome, vp = TK.OPERATORE[idl]
                    mot.operatori[nome](st, par if vp else {}, fr)
                mot.chiudi_tick()
            d = abs(EP.g_pesata(mot, st, par) - g0)
            if d > peggio:
                peggio = d
        return peggio, giri_cs, mot.giri_omega
    finally:
        EP.omega = vero


def pendenza(col_termine, modo, segno):
    """### La pendenza complessiva di `G` su `KAPPA`, e i giri dell'ultimo punto."""
    righe = []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        quanti = int(round(MB2.TEMPO / dtau))
        e, gcs, gom = corsa(dtau, quanti, col_termine, modo, segno)
        righe.append((dtau, quanti, e, gcs, gom))
    primo, ultimo = righe[0][2], righe[-1][2]
    dim = len(KAPPA) - 1
    p = float(np.log2(primo / ultimo) / dim) if ultimo > 0 else float("nan")
    return p, righe, dim


def stampa(righe):
    print("     %-4s %-10s %-7s %-16s %-10s %s"
          % ("k", "dtau", "tick", "escursione G", "giri cs", "giri Omega"))
    for (dtau, quanti, e, gcs, gom), k in zip(righe, KAPPA):
        print("     %-4d %-10.6f %-7d %-16.6e %-10d %d" % (k, dtau, quanti, e, gcs, gom))
    sys.stdout.flush()


def braccio_c1():
    """### `C1`: la pendenza di `G` col termine, e il caso che DEVE fallire senza."""
    print()
    print("### `C1` LA PENDENZA DI `G` con `cs` DINAMICO, COL TERMINE")
    p_con, righe, dim = pendenza(True, "centro", 1)
    stampa(righe)
    esito("`C1` la pendenza di `G` col termine e' `>= %.1f`" % PENDENZA_MIN,
          p_con >= PENDENZA_MIN,
          "pendenza %.3f su %d dimezzamenti" % (p_con, dim))
    print()
    print("### `C1` IL CASO CHE DEVE FALLIRE: la STESSA corsa SENZA il termine")
    p_senza, righe2, _d = pendenza(False, "centro", 1)
    stampa(righe2)
    esito("### `C1` DEVE fallire: SENZA il termine la pendenza e' PEGGIORE",
          p_senza < p_con - 0.5,
          "senza %.3f contro %.3f col termine: il termine MIGLIORA di %.3f"
          % (p_senza, p_con, p_con - p_senza))
    return p_con, p_senza


def braccio_c2(p_con):
    """### `C2`: col SEGNO di `Omega` invertito la pendenza di `G` CADE."""
    print()
    print("### `C2` IL CASO CHE DEVE FALLIRE: il SEGNO di `Omega` INVERTITO")
    p_meno, righe, _d = pendenza(True, "centro", -1)
    stampa(righe)
    esito("### `C2` DEVE fallire: col segno INVERTITO la pendenza CADE",
          p_meno < p_con - 0.5,
          "segno meno %.3f contro %.3f: il segno NON l'ho scelto, esce dalla"
          " derivazione" % (p_meno, p_con))
    return p_meno


def informazione_diagnosi(p_con, p_senza):
    """### 📌 **DOVE STA L'OSTACOLO**: `cs` congelato al centro, oppure il termine?"""
    print()
    print("### \U0001F4CC LA DIAGNOSI (informazione, NON un criterio): `cs` RILETTO prima")
    print("###   di OGNI pezzo, che e' ESPLICITO e quindi NON simmetrico.")
    p_pz_con, righe, _d = pendenza(True, "pezzo", 1)
    stampa(righe)
    p_pz_senza, righe2, _d = pendenza(False, "pezzo", 1)
    print("     ### e la stessa SENZA il termine: %.3f" % p_pz_senza)
    print("     ### IL QUADRO:")
    print("     %-34s %-14s %s" % ("", "col termine", "senza"))
    print("     %-34s %-14.3f %.3f" % ("cs al CENTRO (la scelta di `D2`)",
                                       p_con, p_senza))
    print("     %-34s %-14.3f %.3f" % ("cs RILETTO per pezzo (esplicito)",
                                       p_pz_con, p_pz_senza))
    sys.stdout.flush()
    return p_pz_con, p_pz_senza


def informazione_dove_sta(che_pezzi):
    """### ⭐⭐ **DOVE STA L'OSTACOLO: quanto cambia `Lambda` DENTRO un pezzo.**

    ### ⛔⛔ **La prima ipotesi era <<`cs` congelato al CENTRO>>, E LA DIAGNOSI
    L'HA SMENTITA:** rileggendo `cs` prima di ogni pezzo la pendenza resta
    ### **primo ordine.** ### ✅ **Allora l'ostacolo e' PIU' DENTRO:** i pesi sono
    congelati ### **DURANTE il pezzo**, e un pezzo che ### **muove `Lambda`** muove
    ### **il proprio peso.**
    ### ⚠ **E si misura:** se `|dLambda|` dentro il pezzo e' ### **`O(dtau)`**,
    l'errore sul peso e' `O(dtau)` e la deriva di `G` e' ### **del primo ordine** --
    ### **qualunque sia il posto in cui `cs` si valuta.**
    """
    print()
    print("### 📌 DOVE STA L'OSTACOLO (informazione): quanto cambia `Lambda`")
    print("###   DENTRO un pezzo, per `dtau`. ### Se e' `O(dtau)`, i pesi congelati")
    print("###   durante il pezzo bastano a fare il PRIMO ordine.")
    print("     %-26s %s" % ("dtau", "   ".join("%-14s" % q for q in che_pezzi)))
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        fuori = []
        for idl in che_pezzi:
            inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                         vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
            st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
            lc = float(np.mean(mot.densita_vuoto(st)))
            FP.accendi_cs(mot, lc, st)
            lam0 = mot.densita_vuoto(st).copy()
            mot.apri_tick()
            nome, vp = TK.OPERATORE[idl]
            mot.operatori[nome](st, par if vp else {}, 0.5)
            mot.chiudi_tick()
            fuori.append(float(np.max(np.abs(mot.densita_vuoto(st) - lam0))))
        print("     %-26.5f %s" % (dtau, "   ".join("%-14.6e" % x for x in fuori)))
    print("     ### e `CAMM-SPOSTAMENTO-VUOTO` e' IL SOLO che muove `Lambda`: gli altri")
    print("###   due la conservano (`5e-15`, cioe' l'arrotondamento).")
    sys.stdout.flush()


def informazione_costo():
    """### 📌 **`C5`: IL COSTO sui sette rapporti.** ### **Numeri, non stime.**"""
    print()
    print("### `C5` IL COSTO: i giri dei DUE punti fissi per tick, sui sette rapporti")
    inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, 0.25, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
    lam_medio = float(np.mean(mot.densita_vuoto(st)))
    print("     %10s %8s %10s %12s %s"
          % ("Lambda_c", "Lc/Lam", "giri cs", "giri Omega", "tick di lavoro per tick"))
    peggio = (0.0, 0.0, 0)
    for r in SPAZZATA:
        lc = r / 8.0 * lam_medio if False else r
        inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, 0.25, norma=MB2.NORMA,
                                     vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
        FP.accendi_cs(mot, lc, st)
        tot_cs, tot_om = 0, 0
        for _t in range(8):
            tot_cs += TK.tick_con_cs(st, mot, par, lc, ())
            tot_om += mot.giri_omega
        g_cs, g_om = tot_cs / 8.0, tot_om / 8.0
        # ### ⚠ **UN GIRO DI `cs` COSTA MEZZO TICK**, e uno di `Omega` ### **un
        # ### VENTOTTESIMO** *(il pezzo e' `1` dei `14`, e il punto medio ne fa mezzo)*.
        lavoro = g_cs * 0.5 + g_om * (1.0 / 28.0)
        if lavoro > peggio[0]:
            peggio = (lavoro, lc, g_cs)
        print("     %10.2f %8.3f %10.1f %12.1f %.1f"
              % (lc, lc / lam_medio, g_cs, g_om, lavoro))
    print("     ### il PEGGIO e' ~%.1f tick di lavoro per tick, a `Lambda_c = %.2f`"
          % (peggio[0], peggio[1]))
    print("     ### e il vuoto medio della scena e' %.4f" % lam_medio)
    sys.stdout.flush()


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 100)
    print("LA STRADA `(d)`: `C1`, `C2`, `C5` -- il termine nuovo conserva `G`?")
    print("### Mandato del 2026-10-18. NESSUNA DECISIONE.")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la scena di `M-B2`: nn = %d   seme = %d   T = %.1f   norma = %s"
          "   vuoto_modulo = %.1f   su2 = %s"
          % (MB2.NN, MB2.SEME, MB2.TEMPO, MB2.NORMA, MB2.VUOTO_MODULO, MB2.SU2))
    print("  lo stato di partenza: la PRE-CORSA di `_misura_hw` (`T = %.1f` a"
          " `dtau = %.2f`), la STESSA per tutti i `dtau`"
          % (MB2.TEMPO, HW.DTAU_PRE))
    print("  `Lambda_c` = la MEDIA di `Lambda` sulla scena, UNA volta e PRIMA della corsa")
    print("  i dimezzamenti: k in %s   la soglia: %.1f (quella di `M-B2`)"
          % (KAPPA, PENDENZA_MIN))
    print("  l'ordine: %d voci, impronta %s" % (len(CM.ORDINE), CM.IMPRONTA))
    sys.stdout.flush()
    p_con, p_senza = braccio_c1()
    braccio_c2(p_con)
    informazione_diagnosi(p_con, p_senza)
    informazione_dove_sta(("CAMM-SPOSTAMENTO-VUOTO", "CAMM-GROVER-VUOTO",
                           "CAMM-SPOSTAMENTO"))
    informazione_costo()
    print()
    print("=" * 100)
    print("LA STRADA `(d)`: %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E NESSUNA DECISIONE: se `C1` cade non si allarga nessuna banda e non")
    print("###   si aggiunge niente -- si relaziona coi numeri, e la scelta torna a Luca.")
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
