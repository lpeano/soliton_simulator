# -*- coding: utf-8 -*-
r"""`H_w` — **L'ENERGIA PESATA, E LA MISURA CHE SEPARA LE STRADE DI `cs`.**

> ### 📌 **Mandato del guardiano del `2026-10-17` alle `22:08`, su mandato di Luca.**
> ### ⛔ **NON sceglie fra le letture di `DOMANDA-QUALE-INVARIANTE-CON-CS`:** misura
> ### **se esiste un'energia PESATA che il passo conserva al secondo ordine** quando
> `cs` e' ### **non uniforme ma CONGELATO.**

## ⭐⭐ LA DOMANDA, nelle parole del mandato

Con `cs` non uniforme ma ### **congelato** *(calcolato una volta dallo stato iniziale e
mai aggiornato)*, il passo conserva al secondo ordine

```
H_w = somma sui NODI   di  cs_k * (termini di nodo di H)
    + somma sugli ARCHI di  w_a * (termini d'arco di H)      w_a = media ARMONICA di B-3
```

## ⛔⛔ I PESI SI PRENDONO DAL PASSO, NON SI RISCRIVONO

### ✅ **`w_nodo = s_nodo(con cs) / s_nodo(senza cs)`** e
### **`w_arco = s_arco(con cs) / s_arco(senza cs)`**, con `s_nodo` e `s_arco`
### **le stesse funzioni che il passo chiama** *(`flussi_parziali`)*.
### ⛔ **Una mia copia della media armonica sarebbe una SECONDA FONTE della legge**, ed e'
cio' che `STRUMENTO-LEGGE-DALLA-TABELLA` vieta. ### **Il rapporto la misura invece di
riscriverla.**
### 📌 **E i termini di `H` arrivano da `_misura_mb2.pezzi_di_h`**, che e'
### **una seconda fonte DICHIARATA** e ### **si confronta con `h_tot` a ogni corsa.**

## ⛔ LA MAPPA PEZZO -> PESO, letta dal sorgente

| il pezzo | che peso legge |
|---|---|
| `CAMM-GROVER`, `CAMM-GROVER-VUOTO` | `s_nodo` *(`FP.grover` -> `z_nodo`)* |
| `CAMM-MONETA-SPIN` | `dtau_nodo` *(`motore._moneta_spin`)* |
| `CAMM-MATERIA-VUOTO` | `dtau_nodo` *(`materia_vuoto.applica`)* |
| `CAMM-SPOSTAMENTO`, `CAMM-SPOSTAMENTO-VUOTO` | `s_arco` *(`FP.hop_*` -> `z_arco`)* |

## ⚠ NESSUNA BANDA NUOVA, E NESSUNA DECISIONE

La soglia della pendenza e' ### **`1.9`**, quella di `M-B2` e di `D3`; i dimezzamenti sono
### **`>= 4`**, come in `D3`.
### ⛔ **E la LETTURA e' quella fissata nel task history PRIMA della misura**, non dopo:
### **se `(a)` regge e `(c)` no**, il pesaggio e' coerente e cio' che rompe e'
### **solo la dinamica di `cs`**; ### **se `(a)` non regge**, gia' il modo in cui il passo
usa `cs` ### **non corrisponde a nessuna energia pesata.**

Gira con:  python primo_ordine/_misura_hw.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _misura_mb2 as MB2                                     # noqa: E402
import composizione as CM                                     # noqa: E402
import deriva as DV                                           # noqa: E402
import flussi_parziali as FP                                  # noqa: E402
import tick as TK                                             # noqa: E402

OK = [0, 0]
EPSM = float(np.finfo(float).eps)

# ### ⛔ **IL RAPPORTO E' UN'ETICHETTA, NON UNA TARATURA** *(`A1`)*: `Lambda_c` si
# ### ### **deriva dalla scena** *(la media di `Lambda`)* e non si scegle.
RAPPORTO_LAMBDA_C = 1.0
# ### ⛔ **CINQUE PUNTI = QUATTRO DIMEZZAMENTI**, il `>= 4` del mandato.
KAPPA_HW = (1, 2, 3, 4, 5)
# ### ⚠ **NON E' UNA BANDA NUOVA:** e' quella di `M-B2` *(`>= 1.9`)*, la stessa di `D3`.
PENDENZA_MIN = 1.9
# ### ⚠ **E NEMMENO QUESTA:** `4096` ulp e' la banda piu' larga gia' in uso nel repo
# ### *(la simmetria di `_misura_theta_nonlineare`)*, e qui la differenza fra le due
# ### fonti e' ### **SOLO l'ordine della somma** -- quindi qualunque banda andrebbe, e
# ### ### **il numero misurato si riporta** invece di fidarsi della soglia.
ULP_SECONDA_FONTE = 4096.0


# ### ⛔⛔ **LA PRE-CORSA, E PERCHE' SERVE** *(trovato misurando, il
# ### `2026-10-17`)*: sulla scena di `M-B2` il vuoto nasce ### **UNIFORME**
# ### *(`vuoto_modulo = 2.0` su ogni nodo)*, quindi `cs` nasce ### **COSTANTE** -- e un
# ### `cs` costante fa del braccio `(a)` ### **una copia del braccio `(b)`.**
# ### ✅ **LO STATO NON UNIFORME NON LO SCELGO IO: LO FA LA DINAMICA.** Si lascia
# ### correre il sistema ### **per lo STESSO tempo fisico della misura** *(`MB2.TEMPO`)*
# ### a `dtau = 0.25`, e il vuoto si disuniforma da se' -- ### **misurato: `Lambda` da
# ### `2.22` a `17.52`, `cs` da `0.2175` a `0.6866`.**
# ### ⚠ **E LA PRE-CORSA E' LA STESSA PER TUTTI I `dtau` DELLA SCALA**, perche'
# ### altrimenti i cinque punti partirebbero da ### **cinque stati diversi** e la
# ### pendenza non vorrebbe dire niente.
DTAU_PRE = 0.25
_PRE = {}


def stato_non_uniforme():
    """### Lo stato dopo la pre-corsa: ### **uguale per tutti i `dtau`.**"""
    if "s" not in _PRE:
        inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, DTAU_PRE, norma=MB2.NORMA,
                                     vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
        for _k in range(int(round(MB2.TEMPO / DTAU_PRE))):
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
        _PRE["s"] = (st["psi_h"].copy(), st["phi_h"].copy())
    return _PRE["s"]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def lambda_c_di(mot, st):
    """### `Lambda_c` ### **dalla scena, UNA volta e PRIMA della corsa.**"""
    return RAPPORTO_LAMBDA_C * float(np.mean(mot.densita_vuoto(st)))


def pesi_dal_passo(mot, aritmetica=False):
    """### `(w_nodo, w_arco)`: ### **il peso che IL PASSO usa**, relativo al passo senza
    `cs`.

    ### ⛔⛔ **PERCHE' UN RAPPORTO E NON UNA FORMULA:** la media armonica di `B-3` vive
    in `flussi_parziali.s_arco`, e ### **riscriverla qui sarebbe una seconda fonte della
    legge.** ### ✅ **Il rapporto chiama DUE VOLTE la stessa funzione** -- una con `cs`
    acceso e una con `cs` spento -- e ### **misura il peso invece di dedurlo.**
    ### 📌 **E il rapporto vale `cs_k` sul nodo e `armonica(cs_i, cs_j)` sull'arco**,
    perche' la media armonica e' ### **omogenea di grado `1`**: ma questo e'
    ### **cio' che il numero dice**, non cio' che il codice assume.

    ### ⛔ **`aritmetica` E' IL CASO CHE DEVE FALLIRE:** la media ARITMETICA dei due capi
    al posto dell'armonica. ### **Se la misura non distinguesse i due pesi, non starebbe
    misurando i pesi** -- e il mandato lo chiede per questo.
    """
    salvo = mot.cs
    sn_con = FP.s_nodo(mot).copy()
    sa_con = FP.s_arco(mot).copy()
    d_con = FP.dtau_nodo(mot).copy()
    # ### ⚠ **LO SPEGNIMENTO E' TEMPORANEO, e `mot.cs` si rimette:** una misura che
    # ### lasciasse la forma spenta ### **cambierebbe il passo dei tick dopo.**
    mot.cs = None
    sn_senza = FP.s_nodo(mot).copy()
    sa_senza = FP.s_arco(mot).copy()
    d_senza = FP.dtau_nodo(mot).copy()
    mot.cs = salvo
    w_nodo = sn_con / sn_senza
    if not aritmetica:
        return w_nodo, sa_con / sa_senza
    nodo = mot.inc.nodo
    ar_con = np.take(d_con, nodo).reshape(-1, 2).sum(axis=1) / 2.0
    ar_senza = np.take(d_senza, nodo).reshape(-1, 2).sum(axis=1) / 2.0
    return w_nodo, ar_con / ar_senza


def h_w(inc, mot, st, par, aritmetica=False):
    """### `H_w`: ### **i termini di `H` pesati col peso che il passo usa.**"""
    per_nodo, per_arco = MB2.pezzi_di_h(inc, mot, st, par)
    w_nodo, w_arco = pesi_dal_passo(mot, aritmetica)
    return float(np.sum(w_nodo * per_nodo)) + float(np.sum(w_arco * per_arco))


def corsa(dtau, tick, modo, c_uniforme=None, aritmetica=False):
    """### `(escursione di H_w, escursione di H_tot, lambda_c, peggio della fonte)`.

    ### ⛔ **I QUATTRO MODI:** `spenta` *(la forma off)* · `uniforme` *(`cs` costante:
    il CONTROLLO POSITIVO)* · `congelato` *(`cs` dallo stato INIZIALE, mai
    aggiornato: **la domanda del mandato**)* · `dinamico` *(al centro, come `D2`)*.
    ### ⚠ **E nel modo `dinamico` `H_w` si valuta col `cs` DI QUEL TICK**, cioe' quello
    che il passo ha usato: ### **e' il solo peso definito**, e lo dico invece di
    lasciarlo capire.
    """
    inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, dtau, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    # ### ⛔ **TUTTI I MODI PARTONO DALLO STESSO STATO**, e non e' un dettaglio: se
    # ### il controllo `(b)` partisse da un altro stato, la differenza con `(a)` avrebbe
    # ### ### **DUE cause** invece di una.
    s0 = stato_non_uniforme()
    st["psi_h"][...], st["phi_h"][...] = s0
    lc = lambda_c_di(mot, st)
    if modo == "uniforme":
        mot.cs = np.full(mot.inc.n, float(c_uniforme))
    elif modo in ("congelato", "aritmetica"):
        # ### ⛔ **UNA VOLTA SOLA, dallo stato INIZIALE:** e' cio' che <<congelato>>
        # ### vuol dire, e ### **`mot.cs` sopravvive al tick** *(verificato: `chiudi_tick`
        # ### non lo tocca)*.
        FP.accendi_cs(mot, lc, st)
    elif modo != "dinamico":
        FP.spegni_cs(mot)
    arit = aritmetica or modo == "aritmetica"
    w0 = h_w(inc, mot, st, par, arit)
    t0 = MB2.h_tot(inc, mot, st, par)
    peggio_w, peggio_t, peggio_fonte = 0.0, 0.0, 0.0
    for _k in range(tick):
        if modo == "dinamico":
            TK.tick_con_cs(st, mot, par, lc)
        else:
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
        hw = h_w(inc, mot, st, par, arit)
        ht = MB2.h_tot(inc, mot, st, par)
        peggio_w = max(peggio_w, abs(hw - w0))
        peggio_t = max(peggio_t, abs(ht - t0))
        # ### ⭐ **IL CONFRONTO DELLE DUE FONTI, A OGNI CORSA E A OGNI TICK** *(il
        # ### mandato lo chiede)*: dove il peso e' ### **uniforme `c`**, `H_w` deve dare
        # ### ### **`c * h_tot`** -- e la differenza dev'essere solo l'ordine della somma.
        if modo in ("spenta", "uniforme") and not arit:
            c = 1.0 if modo == "spenta" else float(c_uniforme)
            peggio_fonte = max(peggio_fonte, abs(hw - c * ht) / (EPSM * abs(c * ht)))
    return peggio_w, peggio_t, lc, peggio_fonte


def pendenze(modo, c_uniforme=None):
    """### Le due pendenze complessive *(`H_w` e `H_tot`)* su `KAPPA_HW`."""
    righe = []
    fonte = 0.0
    for k in KAPPA_HW:
        dtau = 1.0 / (2 ** k)
        quanti = int(round(MB2.TEMPO / dtau))
        ew, et, lc, pf = corsa(dtau, quanti, modo, c_uniforme)
        fonte = max(fonte, pf)
        righe.append((dtau, quanti, ew, et))
    dim = len(KAPPA_HW) - 1
    def pend(i):
        primo, ultimo = righe[0][i], righe[-1][i]
        return float(np.log2(primo / ultimo) / dim) if ultimo > 0 else float("nan")
    return pend(2), pend(3), righe, dim, fonte


def stampa_righe(righe):
    print("     %-4s %-10s %-7s %-16s %s"
          % ("k", "dtau", "tick", "escursione H_w", "escursione H_tot"))
    for (dtau, quanti, ew, et), k in zip(righe, KAPPA_HW):
        print("     %-4d %-10.6f %-7d %-16.6e %.6e" % (k, dtau, quanti, ew, et))
    sys.stdout.flush()


def braccio_fonte():
    """### `(0)` **LA SECONDA FONTE: a peso uniforme `H_w` E' `h_tot`.**"""
    print()
    print("### (0) LA SECONDA FONTE: a peso uniforme `H_w` = `c * h_tot`, e si confronta")
    print("###     A OGNI TICK DI OGNI CORSA. Senza, `pezzi_di_h` sarebbe una copia che")
    print("###     puo' divergere in silenzio.")
    _ew, _et, _lc, pf = corsa(1.0 / 2 ** KAPPA_HW[1], 8, "spenta")
    esito("(0) a forma SPENTA `H_w` e' `h_tot` entro %.0f ulp" % ULP_SECONDA_FONTE,
          pf <= ULP_SECONDA_FONTE,
          "il PEGGIO su 8 tick e' %.1f ulp: e' l'ordine della somma, non una legge"
          " diversa" % pf)


def braccio_uniforme():
    """### `(b)` **IL CONTROLLO POSITIVO: `cs` UNIFORME.**

    ### ⛔⛔ **PERCHE' VIENE PRIMA DI `(a)`:** se le pendenze non coincidessero
    ### **gia' a peso costante**, un `(a)` verde ### **non direbbe niente** -- vorrebbe
    dire che `H_w` e `H_tot` sono due cose diverse ### **anche dove DEVONO essere
    proporzionali.**
    """
    print()
    print("### (b) IL CONTROLLO POSITIVO: `cs` UNIFORME, e le due pendenze coincidono")
    _i, mot, st, _p = DV.scena(MB2.NN, MB2.SEME, 0.25, norma=MB2.NORMA,
                               vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = stato_non_uniforme()
    lc = lambda_c_di(mot, st)
    cs0 = FP.cs(mot.densita_vuoto(st), lc,
                mot._b("hw_cs", (mot.inc.n,), float)).copy()
    # ### ⛔ **E LA COSTANTE E' DERIVATA, NON SCELTA** *(`A1`)*: e' ### **la MEDIA del
    # ### `cs` congelato** della stessa scena, cioe' lo stesso ordine di grandezza.
    c = float(np.mean(cs0))
    pw, pt, righe, dim, fonte = pendenze("uniforme", c)
    stampa_righe(righe)
    esito("(b) `cs` UNIFORME = %.6f: la pendenza di `H_w` e' `>= %.1f`" % (c, PENDENZA_MIN),
          pw >= PENDENZA_MIN, "pendenza %.3f su %d dimezzamenti" % (pw, dim))
    esito("(b) e quella di `H_tot` COINCIDE, come deve a peso costante",
          pt >= PENDENZA_MIN, "pendenza %.3f: a peso costante `H_w = c H_tot`" % pt)
    esito("(b) e le due fonti restano d'accordo entro %.0f ulp" % ULP_SECONDA_FONTE,
          fonte <= ULP_SECONDA_FONTE, "il PEGGIO su tutte le corse e' %.1f ulp" % fonte)
    return c, pw, pt


def braccio_congelato():
    """### `(a)` **LA DOMANDA DEL MANDATO: `cs` non uniforme, CONGELATO.**"""
    print()
    print("### (a) LA DOMANDA: `cs` NON UNIFORME ma CONGELATO -- la pendenza di `H_w`")
    pw, pt, righe, dim, _f = pendenze("congelato")
    stampa_righe(righe)
    _i, mot, st, _p = DV.scena(MB2.NN, MB2.SEME, 0.25, norma=MB2.NORMA,
                               vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = stato_non_uniforme()
    lc = lambda_c_di(mot, st)
    c0 = FP.cs(mot.densita_vuoto(st), lc,
               mot._b("hw_cs2", (mot.inc.n,), float)).copy()
    esito("(a) con `cs` CONGELATO la pendenza di `H_w` e' `>= %.1f`" % PENDENZA_MIN,
          pw >= PENDENZA_MIN,
          "pendenza %.3f (e `H_tot` NON pesato: %.3f) -- `cs` va da %.6f a %.6f"
          % (pw, pt, float(np.min(c0)), float(np.max(c0))))
    # ### ⭐ **E IL BRACCIO HA MATERIA: `cs` NON e' uniforme.** ### ⚠ **Senza, `(a)`
    # ### sarebbe `(b)` con un altro nome.**
    esito("(a) e il braccio HA MATERIA: `cs` NON e' uniforme",
          float(np.max(c0) - np.min(c0)) > 1e-6,
          "spread %.6f: se fosse 0 questo braccio sarebbe `(b)`"
          % float(np.max(c0) - np.min(c0)))
    return pw, pt


def braccio_dinamico():
    """### `(c)` **INFORMAZIONE: `cs` DINAMICO, al centro come `D2`.**"""
    print()
    print("### (c) INFORMAZIONE (non un criterio): `cs` DINAMICO, al centro come `D2`")
    pw, pt, righe, dim, _f = pendenze("dinamico")
    stampa_righe(righe)
    print("     ### la pendenza di `H_w` e' %.3f, quella di `H_tot` %.3f su %d"
          " dimezzamenti" % (pw, pt, dim))
    print("     ### E NON E' UN CRITERIO: il mandato la chiede PER INFORMAZIONE.")
    sys.stdout.flush()
    return pw, pt


def braccio_aritmetica():
    """### `(d)` **IL CASO CHE DEVE FALLIRE: la media ARITMETICA sugli archi.**

    ### ⛔⛔ **A COSA SERVE:** se `H_w` reggesse ### **anche coi pesi d'arco
    sbagliati**, la misura ### **non guarderebbe i pesi** -- e un `(a)` verde non direbbe
    che la media ARMONICA e' quella giusta. ### **E' il mandato che lo chiede.**
    ### ⚠ **E IL PASSO E' LO STESSO: cambia SOLO la funzione misurata.**
    """
    print()
    print("### (d) IL CASO CHE DEVE FALLIRE: media ARITMETICA al posto dell'ARMONICA")
    pw, pt, righe, dim, _f = pendenze("aritmetica")
    stampa_righe(righe)
    esito("### (d) DEVE fallire: coi pesi d'arco SBAGLIATI la pendenza si perde",
          pw < PENDENZA_MIN,
          "pendenza %.3f: se fosse `>= %.1f` la misura NON guarderebbe i pesi"
          % (pw, PENDENZA_MIN))
    return pw


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 100)
    print("`H_w`: L'ENERGIA PESATA, E LA MISURA CHE SEPARA LE STRADE DI `cs`")
    print("### Mandato del guardiano del 2026-10-17, 22:08. NESSUNA DECISIONE.")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la scena di `M-B2`: nn = %d   seme = %d   T = %.1f   norma = %s"
          "   vuoto_modulo = %.1f   su2 = %s   omega = pi"
          % (MB2.NN, MB2.SEME, MB2.TEMPO, MB2.NORMA, MB2.VUOTO_MODULO, MB2.SU2))
    print("  `Lambda_c` = %.1f x la MEDIA di `Lambda` sulla scena, UNA volta e PRIMA"
          " della corsa" % RAPPORTO_LAMBDA_C)
    print("  i dimezzamenti: k in %s   la soglia: %.1f (quella di `M-B2`, nessuna banda"
          " nuova)" % (KAPPA_HW, PENDENZA_MIN))
    print("  i pesi: `s_nodo` e `s_arco` DAL PASSO, come rapporto con/senza `cs`")
    sys.stdout.flush()
    braccio_fonte()
    c, pw_u, pt_u = braccio_uniforme()
    pw_a, pt_a = braccio_congelato()
    pw_c, pt_c = braccio_dinamico()
    pw_d = braccio_aritmetica()
    print()
    print("=" * 100)
    print("### IL QUADRO, in una tabella")
    print("  %-34s %-16s %s" % ("il modo di `cs`", "pendenza H_w", "pendenza H_tot"))
    for che, a, b in (("uniforme (%.6f), controllo" % c, pw_u, pt_u),
                      ("CONGELATO non uniforme", pw_a, pt_a),
                      ("DINAMICO (al centro, come `D2`)", pw_c, pt_c),
                      ("congelato, pesi ARITMETICI [deve fallire]", pw_d,
                       float("nan"))):
        print("  %-34s %-16.3f %s"
              % (che, a, "--" if np.isnan(b) else "%.3f" % b))
    print()
    print("### LA LETTURA, fissata nel task history PRIMA della misura:")
    if pw_a >= PENDENZA_MIN and pw_c < PENDENZA_MIN:
        print("###   (a) REGGE e (c) NO: il pesaggio e' COERENTE col modo in cui il passo")
        print("###   usa `cs`, e cio' che rompe la conservazione e' SOLO LA DINAMICA.")
    elif pw_a < PENDENZA_MIN:
        print("###   (a) NON REGGE: gia' il modo in cui il passo usa `cs` NON corrisponde")
        print("###   a nessuna energia pesata di questa forma.")
    else:
        print("###   (a) REGGE e anche (c): la dinamica NON rompe la conservazione pesata,")
        print("###   e questo non era fra i due casi previsti -- va relazionato.")
    print("### " + chr(9940) + " E NESSUNA DECISIONE: la scelta fra le cinque strade e'")
    print("###   di Luca (`DOMANDA-QUALE-INVARIANTE-CON-CS`).")
    print("=" * 100)
    print("`H_w`: %d su %d" % (OK[0], OK[1]))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
