# -*- coding: utf-8 -*-
r"""**LA RISPOSTA DEL VUOTO A UNA SORGENTE FERMA** — *`L2`, quarto pezzo.*

> **Mandato di Luca del 2026-10-15.** Il task history sta in
> `doc/TASK_HISTORY/2026-10-15_l2_risposta_statica.md`, ### **committato PRIMA di questo
> file.** ### ⛔ **Il motore NON si tocca, la tabella NON si tocca: tutto qui dentro.**

## ⛔⛔ PERCHE' QUESTA MISURA ESISTE — *un difetto di protocollo dei tre pezzi precedenti*

### **La sorgente NON ERA FERMA.** Il grumo si disperde *(larghezza da `0.894` a `~3.6`-`4.1`
sul toro `7x7`, misurato in `74ba200`)*, e ### **con una sorgente che si muove la risposta di
primo ordine e' un'onda che si media a zero: resta solo il secondo ordine, `beta^2`** — ed e'
esattamente cio' che i tre pezzi hanno misurato *(esponente `= 2 x` quello di `beta`)*.
### ⭐⭐ **E la gravita' di una massa e' il suo campo STATICO.** ### **Qui la sorgente sta
ferma, e la risposta statica si isola.**

## ⛔⛔ LA SORGENTE CONGELATA E' UNO STRUMENTO DI MISURA, NON UNA LEGGE

### **E' la <<massa di prova>> della fisica:** un corpo che ### **genera il campo e non lo
subisce.** ### ⚠ **Viola la conservazione PER COSTRUZIONE** — la `rho` che il vuoto vede
### **non cambia mai** — e per questo ### **non puo' stare in nessuna tabella: vive in
questo file.**

### ⛔ **E IL MODO DI CONGELARE E' QUELLO DELL'INTEGRAZIONE DEL GUARDIANO** *(dopo
`e01e46f`)*: ### **il termine legge una FOTOGRAFIA FISSA di `rho`**, presa al tick `0`, in
### **entrambe le meta'** della saturazione — e `psi` ### **si ripristina a ogni tick.**
### 📌 **Il perche' sta in `_termine_statico`, e NON e' un'assunzione: e' misurato** dai
bracci `(3)` e `(3-bis)`. ### ⭐ **E il mio metodo di `e01e46f`** *(`rho` ricalcolata dalla
`psi` corrente)* ### **resta come CONTROLLO**: il braccio `(e)` riporta ### **la differenza
fra i due profili**, che e' cio' che il punto `2` dell'integrazione chiede.

## 📌 IL VERSO E' UNO SOLO, PER COSTRUZIONE

### **`materia -> vuoto`.** La retroazione ### **`vuoto -> materia` e' ESCLUSA dal
congelamento**, quindi ### ⛔ **questa misura non dice NIENTE sul verso opposto**, e un suo
risultato ### **non si puo' usare per affermare la bidirezionalita'.**

## ⚠ LE FORME E LA DENSITA' NON SI RIDEFINISCONO QUI

### **`_alpha_beta` e `densita_materia` si IMPORTANO da `_misura_forme_l2.py`:** le quattro
forme hanno ### **una sola definizione in tutto il repo**, e due copie divergerebbero
*(par.`9-ter`: a parita' di effetto si preferisce togliere, non aggiungere)*.

Gira con:  python primo_ordine/_misura_statica_l2.py
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA DAL REFERTO**
# ### ⭐ **IL TORO E' `31x31`, e il motivo e' il BUDGET MISURATO** *(`0.760` ms/tick su
# ### `7x7`, `1.224` su `15x15`, `1.813` su `21x21`, `2.998` su `31x31`)*: il mandato chiede
# ### *<<almeno `15x15`, o il massimo del budget>>*, e ### **un profilo in distanza vuole un
# ### DECENNIO di `r`** -- la distanza toroidale massima diventa ### **`30`**, non `6`.
LATI = (31, 31)
TICK = 2000
TICK_SCAN = 1200
FINESTRE = 10
# ### ⛔ **LE TRE ACCENSIONI:** `0` e- ### **DI COLPO**, `100` e `800` sono le due rampe
# ### liscie che il mandato chiede. ### **Due valori di `T` servono proprio perche- il
# ### risultato NON deve dipendere da `T`.**
T_ACCENSIONE = (0, 100, 800)
T_SCAN = 100
# ### ⚠ **IL TRANSITORIO: una cosa che ho AGGIUNTO scrivendo il codice, e la dichiaro.**
# ### Il task history diceva *<<la finestra comincia al tick `T`>>*; ma con l-accensione
# ### ### **DI COLPO** (`T = 0`) la finestra comincerebbe ### **dentro il transitorio**, e
# ### misurerei l-onda invece dello stato stazionario. ### ✅ **Quindi la finestra comincia a
# ### `T + 200`**, uguale per tutte e tre le accensioni -- e ### **il confronto fra i tre `T`
# ### E- il controllo che il transitorio sia finito.**
TRANSITORIO = 200
DTAU = (0.5, 0.25)
X_SCAN = (0.01, 0.03, 0.1, 0.3, 1.0)
X_RIF = 1.0
VUOTO = 1.0
RAGGIO = 1
SEME = 7
FORME = ("S1", "S2", "S3", "S4")
# ### ⭐ **LA SEPARAZIONE fra le due sorgenti della SOVRAPPOSIZIONE:** `10` archi, cioe-
# ### ### **molto piu- di `2 x RAGGIO`**, e il codice VERIFICA che i due grumi siano
# ### disgiunti invece di assumerlo.
SEP = 10
# ### ⛔ **LA SOVRAPPOSIZIONE SI MISURA A DUE INTENSITA-, e il motivo e- un numero:** a
# ### `x = 1` la risposta e- ### **SATURA** *(`|dLambda|` arriva a `~3.9` su `Lambda = 4`,
# ### cioe- il vuoto e- quasi tutto cacciato)*, e ### **una sovrapposizione provata solo
# ### la- misurerebbe la saturazione invece della linearita-.**
X_SOVR = (1.0, 0.1)
_BASE = {}
_CHI = {}
# ### ⭐ **`rho` ALL'INIZIO E ALLA FINE dell'ultima corsa.** ### ⚠ **Perche' un canale
# ### laterale e non un valore di ritorno:** la larghezza del grumo serve a UN SOLO
# ### braccio, e aggiungerla al ritorno vorrebbe dire ### **cambiare dieci punti di
# ### chiamata**; rifare il giro dei tick in un secondo posto vorrebbe dire
# ### ### **due cicli da tenere d'accordo**, che e' peggio. ### **Si legge SUBITO dopo la
# ### corsa, e il braccio che la usa lo dice.**
ULTIMA = {}


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


# ============================================================== l'accensione e la scena
def rampa(passo, t_acceso):
    """### `s(t)`: la rampa ### **LISCIA** da `0` a `1` su `t_acceso` tick.

    ### ⭐ **`s = (1 - cos(pi t/T))/2`**, che vale `0` a `t = 0`, `1` a `t = T`, e ha
    ### **derivata nulla a ENTRAMBI gli estremi** — cioe' il vuoto segue lo stato
    stazionario ### **senza che l'accensione stessa lo faccia oscillare.**
    ### 📌 **`T = 0` e' l'accensione DI COLPO**, e la funzione lo dice con `1.0`.
    """
    if t_acceso <= 0 or passo >= t_acceso:
        return 1.0
    return 0.5 * (1.0 - np.cos(np.pi * float(passo) / float(t_acceso)))


def nodo_di(lati, coordinate):
    """### L'indice del nodo da coordinate, ### **nella convenzione di `scena_l2.coord`.**"""
    v = 0
    for a, k in zip(lati, coordinate):
        v = v * a + (int(k) % a)
    return v


def chi_allineato(lati, m):
    """### Lo spinore allineato per ogni estremita', ### **in cache per taglia.**

    ### ⚠ **La costruzione e' quella di `scena_l2`, non una mia:** si chiama la sua
    funzione, che ### **verifica l'autovalore** invece di assumerlo.
    """
    import scena_l2 as SC
    ch = (lati, m)
    if ch not in _CHI:
        _CHI[ch] = SC.spinore_allineato(SC.versori_geometrici(lati, m))
    return _CHI[ch]


def metti_grumi(st, inc, lati, centri, raggio, ampiezza):
    """### I grumi sui nodi `centri`, ### **identici a quello di `scena_l2.scena`.**

    ### ⛔ **E i grumi DEVONO essere disgiunti**, altrimenti la sovrapposizione misurerebbe
    una densita' doppia invece di due sorgenti: ### **si verifica, non si assume.**
    """
    import scena_l2 as SC
    chi = chi_allineato(lati, inc.m)
    st["psi_h"].fill(0)
    quanti = 0
    dentro = set()
    for c in centri:
        mio = set()
        for d, nodi in SC.anelli(lati, c).items():
            if d <= raggio:
                mio.update(nodi)
        assert not (mio & dentro), (
            "i grumi su %r si SOVRAPPONGONO: la sovrapposizione misurerebbe una densita'"
            " doppia, non due sorgenti" % (centri,))
        dentro.update(mio)
        quanti += len(mio)
    assert quanti == len(dentro)
    for h in range(2 * inc.m):
        if int(inc.nodo[h]) in dentro:
            st["psi_h"][h] = float(ampiezza) * chi[h]
    return sorted(dentro)


def _termine_statico(nome, senza_alpha, beta_zero):
    """### Il termine candidato, ### **sostituito a runtime e con la RAMPA su `beta`.**

    ### ⛔ **La rampa moltiplica `beta`, non `alpha`**, perche' e' cio' che il mandato
    chiede.

    ### ⭐⭐ **E `agisci.foto` E' LA FOTOGRAFIA DI `rho`** *(integrazione del guardiano del
    `2026-10-15`, dopo `e01e46f`)*: se c'e', ### **il termine la usa IN ENTRAMBE LE META'
    della saturazione**, invece di ricalcolare `rho` dalla `psi` corrente.
    ### ⛔ **Perche' serve, ed e' una cosa che ho MISURATO prima di saperla:** col passo
    ### **PALINDROMO** la saturazione agisce ### **due volte** *(posizioni `0` e `11` di
    `composizione.ORDINE`)*, e fra le due girano ### **Grover e spostamento su `psi`** —
    quindi la seconda meta' leggeva una `rho` ### **GIA' SPOSTATA**, e la sorgente era
    ferma ### **solo ai CONFINI dei tick.**
    ### ✅ **Con la fotografia il vuoto vede la STESSA `rho` in ogni istante**, che e' cio'
    che un campo ### **STATICO** richiede. ### ⚠ **`Lambda` invece resta CORRENTE, e deve:
    e' l'incognita.**
    """
    import flussi_parziali as FP
    import _misura_forme_l2 as MF

    def agisci(st, parametri, frazione):
        mot = agisci.mot
        rho = agisci.foto if agisci.foto is not None else MF.densita_materia(mot, st)
        lam = mot.densita_vuoto(st)
        with np.errstate(divide="ignore", invalid="ignore"):
            x = np.where(lam > 0, rho / np.where(lam > 0, lam, 1.0), 0.0)
        if agisci.visto is not None:
            # ### ⭐ **`rho` COME IL TERMINE LA VEDE, a ogni CHIAMATA:** serve al braccio
            # ### `(3-bis)`, che deve dire ### **a quale delle due applicazioni per tick**
            # ### nasce la differenza fra `alpha` e `alpha = 0`.
            agisci.visto.append(rho.copy())
        al, be = MF._alpha_beta(nome, x)
        # ### ⚠ **dove `rho = 0` la fase di `psi` NON VUOL DIRE NIENTE** *(`psi = 0`)*:
        # ### `alpha = 0`. ### **Singolarita- ELIMINABILE, come nel terzo pezzo.**
        al = np.where(rho > 0, al, 0.0)
        al = np.where(np.isfinite(al), al, 0.0)
        be = np.where(np.isfinite(be), be, 0.0)
        if senza_alpha:
            al = np.zeros_like(al)
        if beta_zero:
            be = np.zeros_like(be)
        dtau = FP.dtau_nodo(mot)
        f = float(frazione)
        s = rampa(agisci.passo, agisci.acceso)
        nodo = mot.inc.nodo
        st["psi_h"] *= np.exp(-1j * np.take(al * dtau * f, nodo)).reshape(-1, 1)
        st["phi_h"] *= np.exp(-1j * np.take(be * dtau * f * s, nodo))
        mot.applicazioni["CAMM-SATURAZIONE"] += 1
        return st

    return agisci


def _avvolgi(op, psi0):
    """### L-operatore, col ripristino di `psi` ### **SUBITO DOPO.**

    ### ⭐ **Cosi- `psi` e- ferma DENTRO il tick, non solo ai suoi confini** -- ed e-
    ### **l-ALTRA opzione che il mandato offriva** *(<<i pezzi su `psi` non si
    applicano>>)*, ottenuta ### **senza classificare i pezzi**: se un pezzo muove `psi`,
    il ripristino lo annulla; se non la muove, non cambia niente.
    """
    def avvolto(st, parametri, frazione):
        r = op(st, parametri, frazione)
        dove = r if isinstance(r, dict) else st
        dove["psi_h"][...] = psi0
        return dove
    return avvolto


def corri(dtau, x, forma, tick, acceso, centri, senza_alpha=False, beta_zero=False,
          congela="tick", visto=None, sorgente="foto"):
    """### `(Lambda(t), max|drho|, max|dSomma|phi|^2|, per_anello)`.

    ### ⛔ **`congela` vale `"tick"`, `"pezzo"` o `"no"`**, e sono ### **le due opzioni
    del mandato piu- il caso che DEVE muoversi**:
    ### ① `"tick"` -- `psi` si ripristina ### **dopo ogni tick** *(la scelta
    DICHIARATA)*; ### ② `"pezzo"` -- ### **dopo ogni pezzo**, cioe- `psi` e- ferma anche
    DENTRO il tick; ### ③ `"no"` -- ### **non si congela**, e serve al braccio `(2)`:
    senza di lui *<<`rho` costante>>* sarebbe ### **un FALSO-ZERO.**

    ### ⛔⛔ **E `sorgente` E' LA COSA CHE IL GUARDIANO HA CORRETTO:**
    ### ⭐ `"foto"` — il termine usa ### **una fotografia FISSA di `rho`**, presa al tick
    `0`, ### **in entrambe le meta' della saturazione**: e' ### **il metodo PRIMARIO**,
    perche' per un campo statico il vuoto deve vedere ### **la stessa `rho` in ogni
    istante**; ### ⚠ `"corrente"` — il termine ricalcola `rho` dalla `psi` del momento, ed
    e' ### **il mio metodo di `e01e46f`**: resta come ### **CONTROLLO**, perche' il punto
    `2` dell'integrazione chiede ### **la differenza fra i due profili.**
    """
    assert sorgente in ("foto", "corrente"), (
        "`sorgente` vale `foto` o `corrente`: e- IL METODO, e un default nascosto"
        " renderebbe illeggibile quale dei due ha prodotto un numero (%r)" % (sorgente,))
    assert congela in ("tick", "pezzo", "no"), (
        "`congela` vale `tick`, `pezzo` o `no`, e non ha un valore di comodo: e- LO"
        " STRUMENTO, e un default nasconderebbe quale strumento ha misurato (%r)"
        % (congela,))
    import deriva as DV
    import scena_l2 as SC
    import _misura_forme_l2 as MF
    inc, mot, st, par, _c, per = SC.scena(dtau, VUOTO, 0.0, RAGGIO, False,
                                          True, False, SEME, 1, lati=LATI)
    if centri:
        metti_grumi(st, inc, LATI, centri, RAGGIO, float(np.sqrt(x)) * VUOTO)
    vero = mot.operatori["CAMM-SATURAZIONE"]
    ag = _termine_statico(forma, senza_alpha, beta_zero)
    ag.mot = mot
    ag.acceso = int(acceso)
    ag.passo = 0
    ag.visto = visto
    ag.foto = None
    mot.operatori["CAMM-SATURAZIONE"] = ag
    salvati = dict(mot.operatori)
    try:
        psi0 = st["psi_h"].copy()
        if congela == "pezzo":
            for quale in list(mot.operatori):
                mot.operatori[quale] = _avvolgi(mot.operatori[quale], psi0)
        rho0 = MF.densita_materia(mot, st)
        if sorgente == "foto":
            # ### ⭐ **LA FOTOGRAFIA**, presa UNA volta e mai piu' toccata.
            ag.foto = rho0.copy()
        tot0 = float(np.sum(np.abs(st["phi_h"]) ** 2))
        lam = np.empty((tick + 1, mot.inc.n), dtype=float)
        lam[0] = mot.densita_vuoto(st)
        drho = 0.0
        dtot = 0.0
        for t in range(tick):
            ag.passo = t
            DV.tick(st, mot, par)
            if congela in ("tick", "pezzo"):
                st["psi_h"][...] = psi0
            lam[t + 1] = mot.densita_vuoto(st)
            drho = max(drho, float(np.max(np.abs(MF.densita_materia(mot, st) - rho0))))
            dtot = max(dtot, abs(float(np.sum(np.abs(st["phi_h"]) ** 2)) - tot0))
        ULTIMA["rho0"] = rho0
        ULTIMA["rho_fine"] = MF.densita_materia(mot, st)
    finally:
        mot.operatori.clear()
        mot.operatori.update(salvati)
        mot.operatori["CAMM-SATURAZIONE"] = vero
    return lam, drho, dtot, per


def base(dtau, tick):
    """### Il vuoto SENZA sorgente, ### **in cache per `(dtau, tick)`.**

    ### ⭐ **Non dipende dalla forma ne' dall'accensione:** con `psi = 0` si ha `x = 0`, e
    ### **tutte e quattro le forme danno `beta(0) = 0`** — quindi il termine non fa niente,
    e la base e' ### **il vuoto libero.**
    """
    ch = (dtau, tick)
    if ch not in _BASE:
        _BASE[ch] = corri(dtau, 0.0, "S1", tick, 0, ())
    return _BASE[ch]


# ====================================================================== le medie a blocchi
def blocchi(campo, inizio, finestre):
    """### I profili per nodo, ### **mediati in `finestre` BLOCCHI di tempo.**

    ### ⛔ **La barra si prende FRA i blocchi, non fra i tick:** i tick sono correlati, e
    una barra presa su di loro ### **sottostima** *(il metodo e' quello dei tre pezzi)*.
    """
    c = campo[inizio:]
    t = c.shape[0]
    assert t >= finestre, "finestra di %d tick per %d blocchi" % (t, finestre)
    b = [int(round(t * i / float(finestre))) for i in range(finestre + 1)]
    return np.array([np.mean(c[b[i]:b[i + 1]], axis=0) for i in range(finestre)])


def barra(valori):
    """### `(media, barra)` da un vettore di valori ### **UNO PER BLOCCO.**"""
    v = np.asarray(valori, dtype=float)
    return (float(np.mean(v)),
            float(np.std(v, ddof=1)) / np.sqrt(v.size) if v.size > 1 else float("nan"))


def su_nodi(prof, nodi):
    """### `(media, barra)` di un profilo a blocchi, ### **mediato sui nodi dati.**"""
    return barra(np.mean(prof[:, nodi], axis=1))


def inizio_finestra(acceso):
    """### Il primo indice della finestra: ### **dopo la rampa E dopo il transitorio.**"""
    return int(acceso) + TRANSITORIO


# ====================================================================== i cinque controlli
def braccio_base():
    print("-" * 96)
    print("### (1) IL VUOTO DI RIFERIMENTO su %s: senza sorgente, dev'essere STAZIONARIO"
          % (LATI,))
    for dtau in DTAU:
        lam, _dr, dtot, _per = base(dtau, TICK)
        d = float(np.max(np.abs(lam - lam[0])))
        esito("(1) vuoto libero fermo a dtau = %.2f" % dtau, d <= 1e-12,
              "max |Lambda(t) - Lambda(0)| = %.3e su %d tick, e la somma |phi|^2 deriva di"
              " %.3e" % (d, TICK, dtot))


def braccio_congelamento():
    print("-" * 96)
    print("### (2) IL CONGELAMENTO FA QUALCOSA? rho con e SENZA il ripristino")
    print("###     (senza questo braccio <<rho costante>> sarebbe un FALSO-ZERO:")
    print("###      e' costante perche' LO IMPONGO, e devo mostrare che altrimenti cambia)")
    import scena_l2 as SC
    per = SC.anelli(LATI, 0)
    d2 = np.zeros(LATI[0] * LATI[1], dtype=float)
    for d, nodi in per.items():
        d2[nodi] = float(d) ** 2
    for congela in ("tick", "no"):
        lam, drho, dtot, _p = corri(0.5, X_RIF, "S1", 400, 0, (0,), congela=congela)
        esito("(2) ripristino %s: max |rho(t) - rho(0)|"
              % ("a ogni TICK" if congela == "tick" else "SPENTO"),
              (drho == 0.0) if congela == "tick" else (drho > 1e-3),
              "%.3e su 400 tick  (atteso: %s)"
              % (drho, "ESATTAMENTE 0" if congela == "tick" else
                 "> 1e-3, cioe' la sorgente SI MUOVE"))
        # ### la larghezza, dal canale laterale `ULTIMA`, letta SUBITO dopo la corsa
        r0, r1 = ULTIMA["rho0"], ULTIMA["rho_fine"]
        print("      larghezza di rho (raggio quadratico medio): t=0 %.4f   t=400 %.4f"
              % (float(np.sqrt(np.sum(d2 * r0) / np.sum(r0))),
                 float(np.sqrt(np.sum(d2 * r1) / np.sum(r1)))))
        sys.stdout.flush()


def braccio_alpha():
    """### **(3) `alpha` conta?** — *la previsione, il controllo, e DOVE nasce.*"""
    print("-" * 96)
    print("### (3) alpha NON PUO' CONTARE: col metodo della FOTOGRAFIA deve valere AL BIT")
    print("###     e col MIO metodo (rho corrente) il mandato non lo garantiva: si misura")
    print("###     la differenza, e si dice A QUALE delle due applicazioni per tick nasce.")
    for forma in ("S1", "S2"):
        for sorgente in ("foto", "corrente"):
            a, _d1, _t1, _p = corri(0.5, X_RIF, forma, 200, 0, (0,), sorgente=sorgente)
            b, _d2, _t2, _p2 = corri(0.5, X_RIF, forma, 200, 0, (0,), senza_alpha=True,
                                     sorgente=sorgente)
            d = float(np.max(np.abs(a - b)))
            if sorgente == "foto":
                esito("(3) %s FOTO: alpha = 0 da' lo STESSO Lambda(t)" % forma, d == 0.0,
                      "max |differenza| = %.3e su 200 tick  (0 = identico AL BIT)" % d)
            else:
                print("      %s rho CORRENTE: max |differenza| = %.3e   <- il mio metodo"
                      " di e01e46f" % (forma, d))
                sys.stdout.flush()
    # ### ⭐ **(3-bis) E DOVE NASCE: la saturazione agisce DUE volte per tick** *(ordine
    # ### PALINDROMO)*, e fra le due girano ### **Grover e spostamento su `psi`.** Quindi
    # ### con `rho` corrente la ### **SECONDA** meta- legge una `rho` spostata.
    # ### ✅ **Si misura `rho` COME IL TERMINE LA VEDE, chiamata per chiamata.**
    import composizione as CM
    quante = sum(1 for idl, _f, _t in CM.ORDINE if idl == "CAMM-SATURAZIONE")
    esito("(3-bis) la saturazione agisce DUE volte per tick", quante == 2,
          "%d applicazioni in composizione.ORDINE su %d pezzi: e' il PALINDROMO"
          % (quante, len(CM.ORDINE)))
    for sorgente in ("corrente", "foto"):
        vA, vB = [], []
        corri(0.5, X_RIF, "S2", 3, 0, (0,), visto=vA, sorgente=sorgente)
        corri(0.5, X_RIF, "S2", 3, 0, (0,), senza_alpha=True, visto=vB, sorgente=sorgente)
        sc = [float(np.max(np.abs(x - y))) for x, y in zip(vA, vB)]
        print("      %-9s rho vista dal termine, chiamata per chiamata (3 tick):"
              " %s" % (sorgente, "  ".join("#%d %.1e" % (i + 1, s)
                                           for i, s in enumerate(sc))))
        sys.stdout.flush()
        if sorgente == "corrente":
            esito("(3-bis) con rho CORRENTE la differenza nasce alla SECONDA"
                  " applicazione", len(sc) >= 2 and sc[0] == 0.0 and sc[1] > 0.0,
                  "chiamata 1: %.1e (identica)   chiamata 2: %.1e (diversa)"
                  % (sc[0], sc[1]) if len(sc) >= 2 else "meno di 2 chiamate")
        else:
            esito("(3-bis) con la FOTOGRAFIA ogni chiamata vede la STESSA rho",
                  all(s == 0.0 for s in sc),
                  "massimo su %d chiamate: %.1e" % (len(sc), max(sc) if sc else 0.0))
    # ### ✅ **(3-ter) E con la fotografia il RIPRISTINO di `psi` non conta per il vuoto:**
    # ### se la saturazione e- ### **l-unico canale `materia -> vuoto`**, allora
    # ### ### **`psi` LIBERA deve dare lo stesso `Lambda(t)` AL BIT.**
    a, _d1, _t1, _p = corri(0.5, X_RIF, "S1", 200, 0, (0,))
    b, _d2, _t2, _p2 = corri(0.5, X_RIF, "S1", 200, 0, (0,), congela="no")
    d = float(np.max(np.abs(a - b)))
    esito("(3-ter) FOTO: psi LIBERA da' lo stesso Lambda(t) AL BIT", d == 0.0,
          "max |differenza| = %.3e -> la saturazione E' l'unico canale materia->vuoto" % d)


def braccio_nullo():
    print("-" * 96)
    print("### (4) IL CONTROLLO NULLO: beta = 0 -> dLambda = 0 esatto")
    for dtau in DTAU:
        b, _d, _t, _p = base(dtau, 200)
        a, _d2, _t2, _p2 = corri(dtau, X_RIF, "S1", 200, 0, (0,), beta_zero=True)
        d = float(np.max(np.abs(a - b)))
        esito("(4) beta = 0 a dtau = %.2f" % dtau, d <= 1e-14,
              "max |dLambda| = %.3e su 200 tick" % d)


# ====================================================================== le quattro domande
def braccio_segno():
    """### **(a) IL SEGNO** di `dLambda` sulla sorgente, e ### **(d) il PROFILO.**"""
    print("-" * 96)
    print("### (a) IL SEGNO di dLambda sulla sorgente, e per TRE accensioni")
    print("###     x = %.2f   %d tick   finestra da T+%d   %d blocchi"
          % (X_RIF, TICK, TRANSITORIO, FINESTRE))
    fuori = {}
    conservazione = 0.0
    for forma in FORME:
        for dtau in DTAU:
            for acceso in T_ACCENSIONE:
                t0 = time.time()
                b, _dr, _dt, per = base(dtau, TICK)
                a, drho, dtot, _p = corri(dtau, X_RIF, forma, TICK, acceso, (0,))
                conservazione = max(conservazione, dtot)
                prof = blocchi(a - b, inizio_finestra(acceso), FINESTRE)
                dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
                m, s = su_nodi(prof, dentro)
                tutti = list(range(prof.shape[1]))
                mt, _st = su_nodi(prof, tutti)
                fuori[(forma, dtau, acceso)] = (m, s, prof, per, dentro)
                print("  %s dtau=%.2f T=%-4d  dLambda = %+.6e +- %.3e (%.1f barre)"
                      "   somma-nodi %+.2e   rho fermo %.1e   [%.1f s]"
                      % (forma, dtau, acceso, m, s, abs(m) / s if s > 0 else float("nan"),
                         mt, drho, time.time() - t0))
                sys.stdout.flush()
    esito("(9) la somma di |phi|^2 e' CONSERVATA in ogni corsa",
          conservazione <= 1e-9,
          "deriva massima %.3e su tutte le corse del braccio (a)" % conservazione)
    return fuori


def braccio_profilo(segno):
    """### **(d) IL PROFILO in distanza** — *senza adattarlo a una legge.*"""
    print("-" * 96)
    print("### (d) IL PROFILO in distanza: dLambda(r) per anelli, e DOVE cambia segno")
    print("###     ⛔ NON lo adatto a log r: il mandato lo vieta, e un profilo si guarda")
    print("###        PRIMA di sceglierne la legge.")
    for forma in FORME:
        for dtau in DTAU:
            ch = (forma, dtau, T_SCAN)
            if ch not in segno:
                continue
            _m, _s, prof, per, _d = segno[ch]
            righe = []
            cambio = None
            primo = None
            for d in sorted(per):
                mm, ss = su_nodi(prof, per[d])
                if primo is None:
                    primo = mm
                if cambio is None and primo is not None and mm * primo < 0:
                    cambio = d
                if d <= 8 or d % 4 == 0:
                    righe.append("r=%-2d %+.3e+-%.1e" % (d, mm, ss))
            print("  %s dtau=%.2f  %s" % (forma, dtau, "  ".join(righe[:7])))
            print("      %s   cambio di segno a r = %s"
                  % ("  ".join(righe[7:]), cambio if cambio is not None else "MAI"))
            sys.stdout.flush()


def braccio_due_metodi():
    """### **Il punto `2` dell'integrazione: i DUE metodi, e la differenza dei profili.**"""
    print("-" * 96)
    print("### (e) I DUE METODI A CONFRONTO: fotografia FISSA di rho contro rho CORRENTE")
    print("###     (il secondo e' il mio metodo di e01e46f: la sorgente ferma SOLO ai")
    print("###      confini dei tick. Se la differenza e' piccola, il prezzo che avevo")
    print("###      dichiarato era trascurabile; se no, conta la FOTOGRAFIA.)")
    for forma in FORME:
        dtau = DTAU[0]
        b, _dr, _dt, per = base(dtau, TICK_SCAN)
        ini = inizio_finestra(T_SCAN)
        pr = {}
        for sorgente in ("foto", "corrente"):
            a, _d2, _t2, _p = corri(dtau, X_RIF, forma, TICK_SCAN, T_SCAN, (0,),
                                    sorgente=sorgente)
            pr[sorgente] = blocchi(a - b, ini, FINESTRE)
        dentro = [vv for d, nodi in per.items() if d <= RAGGIO for vv in nodi]
        mf, sf = su_nodi(pr["foto"], dentro)
        mc, sc = su_nodi(pr["corrente"], dentro)
        # ### il profilo per anelli, e lo scarto FRA I DUE PROFILI
        rf = np.array([np.mean(np.mean(pr["foto"], axis=0)[per[d]]) for d in sorted(per)])
        rc = np.array([np.mean(np.mean(pr["corrente"], axis=0)[per[d]])
                       for d in sorted(per)])
        rel = (np.linalg.norm(rf - rc) / np.linalg.norm(rf)) if np.any(rf) else float("nan")
        print("  %s dtau=%.2f  sorgente: FOTO %+.4e +- %.1e   CORRENTE %+.4e +- %.1e"
              % (forma, dtau, mf, sf, mc, sc))
        print("      e lo scarto FRA I DUE PROFILI dLambda(r): %.4f relativo"
              " (su %d anelli)   stesso segno: %s"
              % (rel, rf.size, "SI'" if mf * mc > 0 else "### NO"))
        sys.stdout.flush()


def braccio_linearita():
    """### **(b) LA LINEARITA'**: pendenza `log`-`log` di `|dLambda|` in `x`."""
    print("-" * 96)
    print("### (b) LA LINEARITA' in x: pendenza log-log di |dLambda| sulla sorgente")
    print("###     x = %s   %d tick   T = %d   finestra da %d"
          % (X_SCAN, TICK_SCAN, T_SCAN, inizio_finestra(T_SCAN)))
    print("###     ATTESO se la risposta statica e' LINEARE in beta:")
    print("###       S1 ~ 3   S2 ~ 1   S3 ~ 1   S4 ~ 1.64   (l'esponente di beta)")
    print("###     e il DOPPIO se la risposta e' quadratica, come nei tre pezzi precedenti.")
    fuori = {}
    for forma in FORME:
        for dtau in DTAU:
            vals, barre = [], []
            b, _dr, _dt, per = base(dtau, TICK_SCAN)
            dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
            for x in X_SCAN:
                a, _d2, _t2, _p = corri(dtau, x, forma, TICK_SCAN, T_SCAN, (0,))
                prof = blocchi(a - b, inizio_finestra(T_SCAN), FINESTRE)
                m, s = su_nodi(prof, dentro)
                vals.append(m)
                barre.append(s)
            pend = []
            for i in range(len(X_SCAN) - 1):
                v1, v2 = vals[i], vals[i + 1]
                # ### ⛔ **la pendenza si legge solo se il SEGNO non cambia e i due valori
                # ### sono FUORI dalla loro barra:** altrimenti e- rumore, e un esponente
                # ### letto sul rumore ### **e- un numero senza provenienza.**
                if (v1 * v2 > 0 and abs(v1) > barre[i] and abs(v2) > barre[i + 1]):
                    pend.append("[%g->%g] %.3f"
                                % (X_SCAN[i], X_SCAN[i + 1],
                                   np.log(abs(v2) / abs(v1))
                                   / np.log(X_SCAN[i + 1] / X_SCAN[i])))
            fuori[(forma, dtau)] = (vals, barre, pend)
            print("  %s dtau=%.2f  dLambda: %s"
                  % (forma, dtau,
                     "  ".join("%g:%+.2e" % (x, v) for x, v in zip(X_SCAN, vals))))
            print("      pendenze LOCALI: %s"
                  % ("  ".join(pend) if pend else "### NON LEGGIBILE (segno che cambia o"
                     " valori dentro la barra)"))
            sys.stdout.flush()
    return fuori


def braccio_sovrapposizione():
    """### **(c) LA SOVRAPPOSIZIONE**: `dL(A+B)` contro `dL(A) + dL(B)`, nodo per nodo."""
    print("-" * 96)
    nb = nodo_di(LATI, (SEP, 0))
    print("### (c) LA SOVRAPPOSIZIONE: due sorgenti a distanza %d (nodi 0 e %d)"
          % (SEP, nb))
    print("###     dLambda(A+B) contro dLambda(A) + dLambda(B), NODO PER NODO")
    for forma in FORME:
        for dtau in DTAU:
          for xs in X_SOVR:
            b, _dr, _dt, per = base(dtau, TICK_SCAN)
            ini = inizio_finestra(T_SCAN)
            pr = {}
            for nome, centri in (("A", (0,)), ("B", (nb,)), ("AB", (0, nb))):
                a, _d2, _t2, _p = corri(dtau, xs, forma, TICK_SCAN, T_SCAN, centri)
                pr[nome] = blocchi(a - b, ini, FINESTRE)
            somma = pr["A"] + pr["B"]
            resto = pr["AB"] - somma
            # ### la norma per blocco, cosi- la barra viene dai BLOCCHI
            nr = np.sqrt(np.sum(resto ** 2, axis=1))
            ns = np.sqrt(np.sum(somma ** 2, axis=1))
            rel = nr / np.where(ns > 0, ns, np.nan)
            mr, sr = barra(rel)
            pmax = float(np.max(np.abs(np.mean(resto, axis=0)))
                         / max(float(np.max(np.abs(np.mean(somma, axis=0)))), 1e-300))
            print("  %s dtau=%.2f x=%.2f  scarto relativo = %.4f +- %.4f"
                  "   (nodo peggiore %.4f)" % (forma, dtau, xs, mr, sr, pmax))
            sys.stdout.flush()


# ====================================================================== il giro
def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    t0 = time.time()
    print("=" * 96)
    print("LA RISPOSTA DEL VUOTO A UNA SORGENTE FERMA -- L2, quarto pezzo.")
    print("### LA SORGENTE CONGELATA E' UNO STRUMENTO (la <<massa di prova>>), NON UNA")
    print("### LEGGE: viola la conservazione PER COSTRUZIONE, e non entra in nessuna")
    print("### tabella. IL MOTORE NON SI TOCCA.")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s = %d nodi   TICK = %d (%d nella scansione)"
          % (LATI, LATI[0] * LATI[1], TICK, TICK_SCAN))
    print("  accensioni T = %s (0 = DI COLPO)   transitorio = %d   finestre = %d"
          % (T_ACCENSIONE, TRANSITORIO, FINESTRE))
    print("  dtau = %s   x = %s   x del verso = %.2f   separazione = %d"
          % (DTAU, X_SCAN, X_RIF, SEP))
    print("  raggio = %d   seme = %d   vuoto = %.1f   forme = %s"
          % (RAGGIO, SEME, VUOTO, FORME))
    print("  ### IL CONGELAMENTO: psi si RIPRISTINA a ogni tick (scelta DICHIARATA).")
    print("  ### CORSA LUNGA: sta FUORI dal pre-commit, come misura DICHIARATA.")
    sys.stdout.flush()
    braccio_base()
    braccio_congelamento()
    braccio_alpha()
    braccio_nullo()
    segno = braccio_segno()
    braccio_profilo(segno)
    braccio_due_metodi()
    braccio_linearita()
    braccio_sovrapposizione()
    print("=" * 96)
    print("### IL VERDETTO SUL SEGNO, forma per forma (accensione T = %d)" % T_SCAN)
    for forma in FORME:
        for dtau in DTAU:
            ch = (forma, dtau, T_SCAN)
            if ch not in segno:
                continue
            m, s = segno[ch][0], segno[ch][1]
            barre = abs(m) / s if s > 0 else float("nan")
            esito("(a) %s a dtau=%.2f: dLambda fuori da 3 barre" % (forma, dtau),
                  barre >= 3.0,
                  "dLambda = %+.4e +- %.3e (%.1f barre) -> %s"
                  % (m, s, barre,
                     ("il vuoto si ACCUMULA" if m > 0 else "il vuoto SI RITIRA")
                     if barre >= 3 else "indeciso"))
    print("=" * 96)
    print("  %d su %d   [corsa intera: %.1f s]" % (OK[0], OK[1], time.time() - t0))
    print("### ⛔ E LA FORMA NON SI DECIDE QUI: la tabella NON e' toccata, e la scelta")
    print("###   fra S1-S4 (o altro) e' di Luca, coi numeri di questa misura.")
    print("### ⛔ E IL VERSO E' UNO SOLO (materia -> vuoto): il congelamento ESCLUDE la")
    print("###   retroazione, quindi questa misura non dice niente sul verso opposto.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
