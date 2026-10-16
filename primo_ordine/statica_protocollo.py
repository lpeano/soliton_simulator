# -*- coding: utf-8 -*-
r"""**LO STRUMENTO DELLA RISPOSTA STATICA** — *la scena, la rampa, il passo, le barre.*

> ### ⛔⛔ **PERCHE' QUESTO MODULO ESISTE, e il motivo e' MISURATO:** quando il punto
> `2(c)` del quinto pezzo ha chiesto la stessa misura ### **con la legge NEL MOTORE**,
> `_misura_statica_l2.py` e' arrivato a ### **`728` righe**, oltre ### **il tetto di
> `700`** — e la regola dice ### **oltre, SI DIVIDE, NON SI ALLUNGA.**

### ⭐ **E IL TAGLIO E' QUELLO GIUSTO: qui sta LO STRUMENTO** *(la scena, la rampa,
il congelamento, il passo, le medie a blocchi)*, ### **la' stanno LE MISURE** *(i bracci
e i loro verdetti)*. ### **Due file che rispondono a due domande diverse: <<come si
misura>> e <<che cosa si e' misurato>>.**

### ⛔⛔ **LA SORGENTE CONGELATA E' UNO STRUMENTO DI MISURA, NON UNA LEGGE:** e' la
### **<<massa di prova>>** della fisica — un corpo che ### **genera il campo e non lo
subisce.** ### ⚠ **Viola la conservazione PER COSTRUZIONE**, e percio'
### **non entra in nessuna tabella: vive qui.**

### ⭐ **E `SOSTITUISCI` E' L'INTERRUTTORE DEL PUNTO `2(c)`:** a `True` il pezzo del
passo si ### **sostituisce a runtime** *(le quattro forme candidate)*; a `False`
### **gira la legge DEL MOTORE**, che e' cio' che il mandato chiede per il confronto.

Non si gira da solo: e' il modulo che `_misura_statica_l2.py` e
`_misura_statica_motore.py` usano.
"""
import os
import sys

import numpy as np
import tick as TK

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

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
# ### ⛔ **LA SOVRAPPOSIZIONE SI MISURA A TRE INTENSITA-, e il motivo e- un numero:** a
# ### `x = 1` la risposta e- ### **SATURA** *(`|dLambda|` arriva a `~3.9` su `Lambda = 4`,
# ### cioe- il vuoto e- quasi tutto cacciato)*, e ### **una sovrapposizione provata solo
# ### la- misurerebbe la saturazione invece della linearita-.**
# ### ⚠⚠ **E `0.01` E- ARRIVATA DOPO LA PRIMA CORSA, con il suo numero:** a `x = 0.1`
# ### ### **`S2`, `S3` e `S4` sono GIA- SATURE** *(`|dLambda| = 3.8` su `4`)*, quindi la-
# ### il confronto ### **non distingue <<non si sovrappone>> da <<e- satura>>.** A
# ### `x = 0.01` invece `S2` vale `0.63` su `4`, ### **cioe- e- fuori dalla saturazione.**
# ### ✅ **Non e- una soglia aggiustata per far passare un braccio: e- una SCENA
# ### AGGIUNTA perche- quella di prima rispondeva a un-altra domanda.**
X_SOVR = (1.0, 0.1, 0.01)
# ### ⛔⛔ **IL PEZZO CHE SI SOSTITUISCE SI LEGGE DALLA TABELLA, e non si scrive a
# ### mano, per un difetto PAGATO il `2026-10-16`:** questo file sostituiva
# ### ### **`mot.operatori["CAMM-SATURAZIONE"]`** per nome, e quando la legge e- stata
# ### ### **sostituita da `CAMM-MATERIA-VUOTO`** la sostituzione finiva su un operatore
# ### ### **che il passo NON CHIAMA PIU-** -- cioe- la misura girava con la legge del
# ### motore e il parametro `forma` ### **non faceva niente, in silenzio.**
# ### ✅ **Adesso il pezzo e- IL FLUSSO CHE STA NELL-ORDINE**, e una legge nuova entra
# ### da sola.


def pezzo_del_passo():
    """### L-`id` del ### **FLUSSO che sta nell-ORDINE di composizione.**"""
    import composizione as CM
    import motore as MO
    dentro = [i for i, _f, _t in CM.ORDINE if i in MO.FLUSSI]
    assert dentro, (
        "nell-ordine di composizione NON c-e- nessun flusso: questa misura sostituisce"
        " UN FLUSSO, e senza di lui non ha niente da sostituire")
    uni = sorted(set(dentro))
    assert len(uni) == 1, (
        "nell-ordine ci sono %d flussi diversi (%s): questa misura ne sostituisce UNO,"
        " e quale sia diventa una DECISIONE -- non la prendo io" % (len(uni), uni))
    return uni[0]


# ### ⭐ **E SI PUO- NON SOSTITUIRE AFFATTO**, che e- il punto `2(c)` del quinto pezzo:
# ### ### **la legge NEL MOTORE**, non per sostituzione. ### **Chi vuole quel modo mette
# ### `SOSTITUISCI = False`**, e `_misura_statica_motore.py` lo fa.
SOSTITUISCI = True
_BASE = {}
_CHI = {}
# ### ⭐ **`rho` ALL'INIZIO E ALLA FINE dell'ultima corsa.** ### ⚠ **Perche' un canale
# ### laterale e non un valore di ritorno:** la larghezza del grumo serve a UN SOLO
# ### braccio, e aggiungerla al ritorno vorrebbe dire ### **cambiare dieci punti di
# ### chiamata**; rifare il giro dei tick in un secondo posto vorrebbe dire
# ### ### **due cicli da tenere d'accordo**, che e' peggio. ### **Si legge SUBITO dopo la
# ### corsa, e il braccio che la usa lo dice.**
ULTIMA = {}



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
        mot.applicazioni[agisci.quale] += 1
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


def _con_rampa(op, ag):
    """### La legge ### **DEL MOTORE**, con la rampa dello STRUMENTO addosso.

    ### ⛔⛔ **PERCHE' ESISTE** *(errore `n.3` del guardiano, `2026-10-16`)*: la rampa
    viveva ### **solo nel termine sostituito**, quindi con `SOSTITUISCI = False` i due
    protocolli giravano ### **in condizioni diverse** — il motore ### **acceso di colpo**
    contro `S3` ### **con la rampa.** ### **Le `3.53` barre di `371731f` erano LA STORIA
    DELL'ACCENSIONE, non un'amplificazione.**

    ### ⭐ **E LA LEGGE NON SI TOCCA:** il termine entra con `exp(-i beta dtau f)`, e
    ### **moltiplicare la FRAZIONE per `s(t)` E' la rampa su `beta`** — la stessa cosa,
    fatta ### **dallo strumento.** ### ⚠ **E vale perche' `beta` entra SOLO nel prodotto
    `beta dtau f`:** se un giorno entrasse altrove, questa equivalenza cadrebbe, e
    ### **sta scritto qui.**
    """
    def avvolto(st, parametri, frazione):
        return op(st, parametri, frazione * rampa(ag.passo, ag.acceso))
    # ### ⛔⛔ **LA MARCA, E IL MOTIVO E' UN FALSO-UNO MIO** *(trovato dal guardiano il
    # ### `2026-10-16`)*: il primo assert diceva
    # ### `ag.acceso == 0 or callable(mot.operatori[quale])`, ed era ### **SEMPRE VERO**,
    # ### perche- ### **entrambi i rami installano un callable.** ### **La frase <<un
    # ### parametro che agisse solo da una parte adesso ALZA>> era FALSA.**
    # ### ✅ **Adesso l-operatore che porta la rampa SI MARCA**, e l-assert
    # ### ### **guarda la marca.**
    avvolto.rampa_dello_strumento = True
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
    quale = pezzo_del_passo()
    vero = mot.operatori[quale]
    ag = _termine_statico(forma, senza_alpha, beta_zero)
    ag.mot = mot
    ag.acceso = int(acceso)
    ag.passo = 0
    ag.visto = visto
    ag.foto = None
    ag.quale = quale
    # ### ⭐ **E IL TERMINE SOSTITUITO PORTA LA STESSA MARCA**, perche- la rampa la applica
    # ### ### **da se-** *(`s = rampa(agisci.passo, agisci.acceso)`)*: la marca dice
    # ### ### **<<qui la rampa agisce>>**, non ### **<<sono avvolto>>.**
    ag.rampa_dello_strumento = True
    if SOSTITUISCI:
        mot.operatori[quale] = ag
    else:
        # ### ⛔⛔ **LA RAMPA DEVE AGIRE ANCHE SULLA LEGGE DEL MOTORE** *(errore `n.3`,
        # ### `2026-10-16`)*: prima la rampa viveva ### **solo nel termine sostituito**, e
        # ### con `SOSTITUISCI = False` la sorgente era ### **accesa DI COLPO dal tick
        # ### `0`** -- cioe- il confronto fra i due protocolli girava ### **in condizioni
        # ### DIVERSE**, e le `3.53` barre erano ### **la storia dell-accensione.**
        # ### ⭐ **E SI FA SENZA TOCCARE LA LEGGE:** il termine entra con
        # ### `exp(-i beta dtau f)`, quindi ### **moltiplicare la FRAZIONE per `s(t)` E-
        # ### la rampa su `beta`** -- esattamente la stessa cosa, fatta ### **dallo
        # ### STRUMENTO.**
        mot.operatori[quale] = _con_rampa(vero, ag)
    # ### ⛔ **E UN PARAMETRO CHE AGISCE SOLO DA UNA PARTE ALZA**, non passa in silenzio:
    # ### ### **e- la lezione dell-errore `n.3`**, e qui e- un `assert` CHE GUARDA LA MARCA
    # ### *(il primo guardava `callable`, ed era ### **un FALSO-UNO**)*.
    assert ag.acceso == 0 or getattr(
        mot.operatori[quale], "rampa_dello_strumento", False), (
        "`acceso = %d` e il pezzo `%s` NON porta la marca `rampa_dello_strumento`: la"
        " rampa agirebbe solo da una parte, e un parametro cosi- NON CONFRONTA NIENTE"
        % (ag.acceso, quale))
    # ### ⛔⛔ **E I TRE PARAMETRI DEL TERMINE SOSTITUITO NON SI IGNORANO IN SILENZIO**
    # ### *(la stessa famiglia, trovata dal guardiano il `2026-10-16`)*: `senza_alpha`,
    # ### `beta_zero` e `visto` vivono ### **dentro `_termine_statico`**, quindi con
    # ### `SOSTITUISCI = False` ### **non avrebbero nessun effetto.**
    # ### ⭐ **E NON si applicano al motore**, perche- vorrebbe dire ### **toccare la
    # ### legge**: `senza_alpha` azzera `alpha` DENTRO il termine, e dall-esterno non si
    # ### esprime. ### ✅ **Quindi si ALZA**, che e- l-altra via che il mandato ammette.
    assert SOSTITUISCI or not (senza_alpha or beta_zero or visto is not None), (
        "`senza_alpha`, `beta_zero` e `visto` agiscono SOLO sul termine SOSTITUITO, e con"
        " `SOSTITUISCI = False` sarebbero IGNORATI IN SILENZIO: o si sostituisce il pezzo,"
        " o non si chiedono (senza_alpha=%r, beta_zero=%r, visto=%r)"
        % (senza_alpha, beta_zero, visto is not None))
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
        # ### ⭐ **IL SALTO DI `rho` PER TICK, che e- il CONO di `74ba200`:**
        # ### ### **quanto cambia lo STATO in un tick**, da confrontare col passo
        # ### LIBERO. ### ⚠ **Si guarda `rho` e non `Lambda`**, e il motivo e-
        # ### misurato: sulla scena di riferimento `phi` e- UNIFORME, quindi il passo
        # ### libero lascia `Lambda` ### **esattamente ferma** -- e un rapporto con
        # ### zero al denominatore ### **non e- un numero.**
        salto = 0.0
        rprec = rho0.copy()
        for t in range(tick):
            ag.passo = t
            TK.tick(st, mot, par)
            if congela in ("tick", "pezzo"):
                st["psi_h"][...] = psi0
            lam[t + 1] = mot.densita_vuoto(st)
            rora = MF.densita_materia(mot, st)
            salto = max(salto, float(np.max(np.abs(rora - rprec))))
            rprec = rora.copy()
            drho = max(drho, float(np.max(np.abs(rora - rho0))))
            dtot = max(dtot, abs(float(np.sum(np.abs(st["phi_h"]) ** 2)) - tot0))
        ULTIMA["rho0"] = rho0
        ULTIMA["salto_rho"] = salto
        ULTIMA["rho_fine"] = MF.densita_materia(mot, st)
    finally:
        mot.operatori.clear()
        mot.operatori.update(salvati)
        mot.operatori[quale] = vero
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
