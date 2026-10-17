# -*- coding: utf-8 -*-
r"""**LA SIMMETRIA `(P Theta)` SUL PASSO INTERO, COL TERMINE NON LINEARE DENTRO.**

> **Punto `2(b)` del mandato di Luca del `2026-10-15`** *(quinto pezzo di `L2`)*:
> *«con `n` geometrici e `U = I`, `(P Theta) W (P Theta)^-1 = W^-1` deve ancora valere,
> ORA COL TERMINE NONLINEARE INCLUSO — sul passo intero, su uno stato di prova, non solo
> sulla parte lineare. Riporta lo scarto.»*

## ⛔⛔ PERCHE' SERVE UNA MISURA NUOVA, e non si estende quella di `L1`

`_misura_theta_n.py` costruisce `W` ### **come MATRICE**, applicando il passo ai vettori di
base — e ### **una matrice esiste solo se il passo e' LINEARE.** ### **Il termine di
`CAMM-MATERIA-VUOTO` non lo e'**: le sue fasi dipendono da `rho` e `Lambda`, cioe'
### **dallo stato.**
### ✅ **Quindi qui l'identita' si prova SU UNO STATO**, che e' esattamente cio' che il
mandato chiede: ### **`(P Theta) W (P Theta)^-1 s` contro `W^-1 s`.**

## ⛔⛔ `W^-1` NON SI PUO' COSTRUIRE, E L'IDENTITA' SI RISCRIVE

### **Il primo tentativo era `frazione -> -frazione`**, che inverte un flusso
*(`exp(-i a) exp(+i a) = 1`)* e, in algebra, anche un pezzo unitario
*(`G(theta)^-1 = G(-theta)`)*. ### ⛔ **MA I PEZZI UNITARI RIFIUTANO una frazione
negativa:** `flussi_parziali._frazione_valida` asserisce `0 < f <= 1` — ed e'
### **l'assert del CONO di `L1`**, non un capriccio: *«`<= 0` non e' un passo»*.
### ⚠ **Quindi `W^-1` NON e' esprimibile con l'API della tabella**, e lo dico invece di
aggirare un assert.

### ✅ **E L'IDENTITA' SI RISCRIVE IN UNA FORMA EQUIVALENTE CHE USA SOLO PASSI AVANTI:**

```
A W A^-1 = W^-1        <==>        W A W A^-1 = 1          con A = P Theta
```

*(si moltiplica a sinistra per `W`; le due sono la stessa affermazione)*.
### ⭐ **Cosi' la misura non ha bisogno di nessun passo indietro**, e il numero che riporta
e' ### **lo scarto fra `W A W A^-1 s` e `s`.**

## 📌 `Theta` SU `phi`, e il segno di `Theta^2`

### `Theta psi = i sigma_y psi^*` e ### **`Theta phi = phi^*`**: il vuoto e' uno scalare,
e per lui l'antiunitaria e' ### **la coniugazione.**
### ⚠ **`Theta^2 = -1` su `psi` e `+1` su `phi`**, quindi `(P Theta)^-1` ### **non e'
`(P Theta)`**: si implementa l'inversa ### **esplicitamente**, e il braccio `(0)` verifica
che ### **`A A^-1 = 1` AL BIT** invece di fidarsi del conto a mano.

Gira con:  python primo_ordine/_misura_theta_nonlineare.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _misura_theta_n as TN                                  # noqa: E402
import tick as TK                                             # noqa: E402

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA.** ### **La scena e' quella di
# ### `_misura_theta_n.py`** *(toro `3x3`, seme `7`, `eps = 0.5`)*, perche' e'
# ### ### **la scena in cui la simmetria della parte lineare E' MISURATA** -- cambiarla
# ### vorrebbe dire confrontare due cose diverse.
DTAU = (1.0, 0.5, 0.25)
SEME_STATO = 11
# ### ⭐ **E DUE NODI SI SVUOTANO, perche' `rho = 0` e' il caso delicato:** la' `alpha`
# ### non e' definita e il codice usa ### **il limite**. ### **Un braccio su uno stato
# ### tutto pieno non lo guarderebbe.**
NODI_VUOTI = (0, 4)
EPSM = float(np.finfo(float).eps)


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def stato_di_prova(mot, st, seme, vuoti=NODI_VUOTI):
    """### Uno stato casuale con ### **materia, vuoto, e due nodi VUOTI.**"""
    r = np.random.default_rng(seme)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = (r.normal(size=st["phi_h"].shape)
                        + 1j * r.normal(size=st["phi_h"].shape))
    nodo = np.asarray(mot.inc.nodo)
    for k in vuoti:
        st["psi_h"][nodo == k] = 0.0
    return (st["psi_h"].copy(), st["phi_h"].copy())


def metti(st, s):
    st["psi_h"][...], st["phi_h"][...] = s[0], s[1]
    return st


def passo(mot, st, solo_lineare=False):
    """### `W`: ### **il passo INTERO, dalla TABELLA**, e nient-altro.

    ### ⛔ **Non esiste un `verso = -1`**, e il motivo e- scritto in testa al modulo:
    i pezzi unitari ### **rifiutano una frazione negativa** *(l-assert del cono)*.
    """
    import composizione as CM
    import deriva as DV
    import motore as MO
    mot.apri_tick()
    for idl, fr, _t in CM.ORDINE:
        if solo_lineare and idl in MO.FLUSSI:
            continue
        nome, vuole_par = TK.OPERATORE[idl]
        mot.operatori[nome](st, {"eps": TN.EPS} if vuole_par else {}, fr)
    mot.chiudi_tick()
    return (st["psi_h"].copy(), st["phi_h"].copy())


def antiunitaria(s, P, inversa=False):
    """### `A = P Theta`, e ### **la sua INVERSA esplicita.**

    ### `Theta psi = i sigma_y psi^*` · `Theta phi = phi^*` · `P` ### **permuta le
    estremita'.**
    ### ⛔ **E `A^-1` NON e' `A`:** `Theta^2 = -1` su `psi`, quindi l'inversa porta
    ### **un segno meno sulla parte spinoriale** — e il braccio `(0)` lo MISURA.
    """
    psi = np.conj(s[0])
    psi = np.einsum("ij,aj->ai", 1.0j * TN.SY, psi)
    if inversa:
        psi = -psi
    phi = np.conj(s[1])
    return (psi[P, :].copy(), phi[P].copy())


def scarto(a, b):
    """### `max |a - b|` sulle due componenti, e ### **la scala.**"""
    d = max(float(np.max(np.abs(a[0] - b[0]))), float(np.max(np.abs(a[1] - b[1]))))
    s = max(float(np.max(np.abs(b[0]))), float(np.max(np.abs(b[1]))), 1e-300)
    return d, s


def braccio_strumenti(dtau, P):
    """### `(0)` e `(1)`: ### **gli strumenti funzionano, e il braccio HA MATERIA.**"""
    inc, mot, st = TN.scena(dtau, True, True)
    s0 = stato_di_prova(mot, st, SEME_STATO)
    # ### (0) `A A^-1 = 1`
    d, sc = scarto(antiunitaria(antiunitaria(s0, P, inversa=True), P), s0)
    esito("(0) `A A^-1 = 1` AL BIT (`A = P Theta`)", d == 0.0,
          "scarto %.1e: l'inversa e' COSTRUITA, non assunta" % d)
    # ### (1) il termine NON lineare AGISCE: senza di lui il passo e- un altro
    metti(st, s0)
    con = passo(mot, st)
    metti(st, s0)
    senza = passo(mot, st, solo_lineare=True)
    d, sc = scarto(con, senza)
    esito("(1) il braccio HA MATERIA: il termine NON LINEARE cambia il passo",
          d > 1e-6, "|W - W_lineare| = %.3e su scala %.3e: se fosse 0 la misura non"
          " guarderebbe il termine" % (d, sc))
    rho = mot.densita_materia(metti(st, s0)).copy()
    esito("(1) e ci sono nodi con `rho = 0` E nodi con `rho > 0`",
          bool(np.any(rho == 0.0)) and bool(np.any(rho > 0.0)),
          "%d nodi vuoti su %d: il caso del LIMITE e' dentro la misura"
          % (int(np.sum(rho == 0.0)), rho.size))
    # ### ⛔ **E IL PASSO INDIETRO NON SI PUO- FARE: si MISURA che l-assert scatti**,
    # ### invece di scriverlo nel docstring e basta.
    passa, nota = False, "NON ha alzato: l-assert del cono non c-e- piu-"
    try:
        import deriva as DV
        metti(st, s0)
        mot.apri_tick()
        nome, _vp = TK.OPERATORE["CAMM-GROVER"]
        mot.operatori[nome](st, {}, -0.5)
        mot.chiudi_tick()
    except AssertionError as e:                               # noqa: BLE001
        passa, nota = True, "### ha alzato: %s" % str(e)[:58]
    esito("(2) DEVE alzare: un pezzo unitario a frazione NEGATIVA", passa, nota)


def braccio_simmetria(dtau, P):
    """### `(3)` **L'IDENTITA'**, e i due casi che ### **DEVONO fallire.**"""
    inc, mot, st = TN.scena(dtau, True, True)
    s0 = stato_di_prova(mot, st, SEME_STATO)
    # ### ⭐ **`W A W A^-1 s` contro `s`**: l-identita- in forma SOLO-AVANTI.
    metti(st, antiunitaria(s0, P, inversa=True))
    passo(mot, st)
    metti(st, antiunitaria((st["psi_h"].copy(), st["phi_h"].copy()), P))
    fine = passo(mot, st)
    d, sc = scarto(fine, s0)
    esito("(3) `W A W A^-1 = 1` col termine NON lineare (`A = P Theta`)",
          d <= 4096 * EPSM * sc,
          "scarto %.3e su scala %.3e, cioe' %.0f ulp" % (d, sc, d / (EPSM * sc)))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE `(a)`: `Theta` SENZA `P`.** In `L1`
    # ### ### **`Theta W Theta^-1 = W[-n]^-1`**, quindi senza l-inversione
    # ### ### **non deve tornare.**
    ident = np.arange(st["psi_h"].shape[0])
    metti(st, antiunitaria(s0, ident, inversa=True))
    passo(mot, st)
    metti(st, antiunitaria((st["psi_h"].copy(), st["phi_h"].copy()), ident))
    w2 = passo(mot, st)
    d2, sc2 = scarto(w2, s0)
    esito("### (3) DEVE fallire: `Theta` SENZA `P` non chiude l-identita-",
          d2 > 4096 * EPSM * sc2,
          "scarto %.3e, cioe' %.0f ulp: `P` SERVE" % (d2, d2 / (EPSM * sc2)))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE `(b)`: `U` CASUALE.** La derivazione di `L1` usa
    # ### ### **`U = I`**, e con una `U` qualunque l-identita- ### **non deve valere.**
    _i3, m3, s3 = TN.scena(dtau, True, False)
    t0 = stato_di_prova(m3, s3, SEME_STATO)
    metti(s3, antiunitaria(t0, P, inversa=True))
    passo(m3, s3)
    metti(s3, antiunitaria((s3["psi_h"].copy(), s3["phi_h"].copy()), P))
    w3 = passo(m3, s3)
    d3, sc3 = scarto(w3, t0)
    esito("### (3) DEVE fallire: con `U` CASUALE l'identita' si ROMPE",
          d3 > 4096 * EPSM * sc3,
          "scarto %.3e, cioe' %.0f ulp: `U = I` SERVE" % (d3, d3 / (EPSM * sc3)))
    return d, sc


# ### ⛔⛔ **LA META- `PTheta` DEL CASO CHE DEVE FALLIRE DI `D2`**
# ### *(`2026-10-17`)*: il mandato di `D2` chiede che la variante ingenua
# ### *(`cs` letto a INIZIO PASSO)* perda ### **il secondo ordine E la simmetria
# ### `PTheta`.** ### **Il secondo ordine e- misurato in `_collauda_cs_centro.py`**;
# ### ### **la simmetria vive QUI**, perche- qui c-e- la permutazione delle estremita-
# ### e la scena in cui l-identita- e- MISURATA. ### ✅ **Riscriverla la- dentro
# ### sarebbe stato un SECONDO strumento per la stessa simmetria.**
#
# ### ⛔ **E `Lambda_c` NON E- UNA MANOPOLA** *(`A1`)*: si prende
# ### ### **la MEDIA di `Lambda` sullo stato di prova**, cioe- il rapporto
# ### `Lambda_c/Lambda_medio = 1` -- ### **un-ETICHETTA DERIVATA dalla scena**, non un
# ### numero scelto. ### ⚠ **E il mandato del guardiano lo dice:** nelle misure il
# ### rapporto ### **e- un-etichetta**, e `Lambda_c` ### **non si calcola MAI dallo stato
# ### durante la corsa** -- qui si calcola ### **PRIMA**, una volta, e poi e- FISSO.
RAPPORTO_LAMBDA_C = 1.0


def lambda_c_della_scena(mot, st):
    """### `Lambda_c` ### **dalla scena, una volta sola e PRIMA della corsa.**"""
    import numpy as _np
    return RAPPORTO_LAMBDA_C * float(_np.mean(mot.densita_vuoto(st)))


def passo_cs(mot, st, modo, lambda_c):
    """### `W` ### **con la forma `cs`**, nei due modi di `D2`.

    ### ⛔ **E PASSA DA `tick.py`, non da un ciclo mio:** `percorri_tick` esiste
    ### **perche- c-erano due percorsi del tick**, e un terzo qui dentro sarebbe
    ### **lo stesso difetto.**
    """
    import composizione as CM
    import flussi_parziali as FP
    par = {"eps": TN.EPS}
    if modo == "centro":
        TK.tick_con_cs(st, mot, par, lambda_c)
    elif modo == "inizio":
        FP.accendi_cs(mot, lambda_c, st)
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    else:
        TK.tick(st, mot, par)
    return (st["psi_h"].copy(), st["phi_h"].copy())


def identita_con_cs(mot, st, s0, P, modo, lambda_c):
    """### Lo scarto di `W A W A^-1 s` da `s`, ### **con la forma `cs` nel modo dato.**"""
    import flussi_parziali as FP
    FP.spegni_cs(mot)
    metti(st, antiunitaria(s0, P, inversa=True))
    passo_cs(mot, st, modo, lambda_c)
    metti(st, antiunitaria((st["psi_h"].copy(), st["phi_h"].copy()), P))
    fine = passo_cs(mot, st, modo, lambda_c)
    FP.spegni_cs(mot)
    return scarto(fine, s0)


def braccio_cs(dtau, P):
    """### `(5)`-`(6)`-`(7)`: ### **la `PTheta` con `cs`, e la variante che DEVE romperla.**

    ### ⛔⛔ **I CRITERI SONO QUELLI GIA- FISSATI**, e non ne nasce uno nuovo:
    la banda e- ### **la stessa del braccio `(3)`** *(`4096` ulp)*, e il verdetto atteso
    e- quello scritto nel task history di `D` ### **prima del codice**:
    ### **`cs` al CENTRO conserva la simmetria, `cs` a INIZIO PASSO la rompe.**
    """
    import flussi_parziali as FP
    inc, mot, st = TN.scena(dtau, True, True)
    s0 = stato_di_prova(mot, st, SEME_STATO)
    lam_c = lambda_c_della_scena(mot, metti(st, s0))
    # ### ⭐ **`(5)` IL CONTROLLO CHE RENDE SENSATO IL CONFRONTO:** con la forma
    # ### SPENTA il percorso di `tick.py` e- ### **il passo di questo file AL BIT.**
    # ### ⚠ **Senza questo braccio, `(6)` e `(7)` confronterebbero DUE CAMMINI**, e
    # ### un-eventuale differenza non direbbe niente su `cs`.
    FP.spegni_cs(mot)
    metti(st, s0)
    a_mano = passo(mot, st)
    FP.spegni_cs(mot)
    metti(st, s0)
    da_tick = passo_cs(mot, st, "spenta", lam_c)
    d5, _s5 = scarto(a_mano, da_tick)
    esito("(5) a forma SPENTA il passo di `tick.py` e' questo AL BIT", d5 == 0.0,
          "scarto %.1e: `(6)` e `(7)` confrontano LO STESSO cammino, non due" % d5)
    # ### ✅ **`(6)` `cs` AL CENTRO: la simmetria REGGE**
    d6, s6 = identita_con_cs(mot, st, s0, P, "centro", lam_c)
    esito("(6) con `cs` al CENTRO `W A W A^-1 = 1` REGGE",
          d6 <= 4096 * EPSM * s6,
          "scarto %.3e su scala %.3e, cioe' %.0f ulp (Lambda_c = %.4f, rapporto %.1f)"
          % (d6, s6, d6 / (EPSM * s6), lam_c, RAPPORTO_LAMBDA_C))
    # ### ⛔ **`(7)` IL CASO CHE DEVE FALLIRE: `cs` a INIZIO PASSO**
    d7, s7 = identita_con_cs(mot, st, s0, P, "inizio", lam_c)
    esito("### (7) DEVE fallire: `cs` a INIZIO PASSO ROMPE la simmetria",
          d7 > 4096 * EPSM * s7,
          "scarto %.3e, cioe' %.0f ulp: e' %.0fx la banda, e il palindromo e' rotto"
          % (d7, d7 / (EPSM * s7), d7 / (4096 * EPSM * s7)))
    return d6, s6, d7, s7


def braccio_c(dtau):
    """### **`(4)` LA `C` SUL FLUSSO NUOVO**, che nessuna misura copriva.

    ### ⛔⛔ **PERCHE' C'E': il banco congelato mi ha avvisato.**
    `proto_camminata/nonlineare2.fase_pari2` e' la fase proporzionale a `rho`, e il suo
    docstring dice ### **<<PARI sotto `C` ==> ROMPE `C`>>**; `fase_elicita` *(con `h`)* e'
    ### **DISPARI e commuta con `C`.** ### **Quindi il cambio di sorgente CAMBIA la parita'
    del termine**, e `_misura_c_flussi.py` ### **copre solo i quattro pezzi unitari**, non
    il flusso.

    ### ⭐ **E I DUE CRITERI SONO DIVERSI, ed e' il punto:**
    ### `C Op C^-1 = Op^-1` *(la `CT`, cio' che il passo PALINDROMO usa)* e
    ### `C Op C^-1 = Op` *(commutare con `C`)*. ### **Una fase PARI soddisfa il primo, una
    DISPARI il secondo** — e qui si misurano ### **entrambi**, senza decidere quale conti.
    """
    import _misura_c_flussi as CF
    _i, mot, st = TN.scena(dtau, True, True)
    s0 = stato_di_prova(mot, st, SEME_STATO)
    nome = "CAMM-MATERIA-VUOTO"
    # ### `Op(f) s`  e  `Op(-f) s`
    metti(st, s0)
    mot.apri_tick()
    mot.operatori[nome](st, {}, 1)
    mot.chiudi_tick()
    diretto = (st["psi_h"].copy(), st["phi_h"].copy())
    metti(st, s0)
    mot.apri_tick()
    mot.operatori[nome](st, {}, -1)
    mot.chiudi_tick()
    inverso = (st["psi_h"].copy(), st["phi_h"].copy())
    # ### `C Op C^-1 s`: si applica `C`, il pezzo, e `C` di nuovo *(`C^2 = -1` su `psi`,
    # ### e il segno si PORTA nel confronto invece di nascondersi in un valore assoluto)*
    metti(st, s0)
    CF.c_completa(mot, st)
    mot.apri_tick()
    mot.operatori[nome](st, {}, 1)
    mot.chiudi_tick()
    CF.c_completa(mot, st)
    # ### `C^2 = -1` su `psi` e `+1` su `phi`
    coniugato = (-st["psi_h"].copy(), st["phi_h"].copy())
    da, sa = scarto(coniugato, inverso)
    esito("(4) `C Op C^-1 = Op^-1` sul flusso NUOVO (la `CT`)",
          da <= 4096 * EPSM * sa,
          "scarto %.3e su scala %.3e, cioe' %.0f ulp" % (da, sa, da / (EPSM * sa)))
    db, sb = scarto(coniugato, diretto)
    esito("### (4) e `C Op C^-1 = Op` NON vale [ATTESO NO]",
          db > 4096 * EPSM * sb,
          "scarto %.3e: la sorgente `rho` e' PARI sotto `C`, quindi il flusso"
          " ROVESCIA invece di COMMUTARE" % db)


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import corrente as CO
    print("=" * 96)
    print("LA SIMMETRIA `(P Theta)` SUL PASSO INTERO, COL TERMINE NON LINEARE DENTRO")
    print("### Punto 2(b) del mandato del quinto pezzo di L2.")
    print("=" * 96)
    ii, jj, nn = CO.toro(TN.LATI)
    P = TN._inversione(TN.LATI, ii, jj)
    print("  LA CONFIGURAZIONE: toro %s = %d nodi, %d archi   n GEOMETRICI, U = I"
          % (TN.LATI, nn, len(ii)))
    print("  dtau = %s   eps = %.1f   seme della scena = %d   seme dello stato = %d"
          % (DTAU, TN.EPS, TN.SEME, SEME_STATO))
    print("  nodi SVUOTATI (per il caso `rho = 0`): %s" % (NODI_VUOTI,))
    print("  ### `Theta psi = i sigma_y psi*`, `Theta phi = phi*`, `P` = inversione")
    sys.stdout.flush()
    fuori, con_cs = {}, {}
    for dtau in DTAU:
        print("-" * 96)
        print("### dtau = %.4f" % dtau)
        braccio_strumenti(dtau, P)
        fuori[dtau] = braccio_simmetria(dtau, P)
        braccio_c(dtau)
        con_cs[dtau] = braccio_cs(dtau, P)
    print("=" * 96)
    print("### LO SCARTO DELL'IDENTITA', per `dtau`")
    for dtau in DTAU:
        d, sc = fuori[dtau]
        print("  dtau = %.4f   scarto %.3e   scala %.3e   %.0f ulp"
              % (dtau, d, sc, d / (EPSM * sc)))
    print("=" * 96)
    print("### LA `PTheta` CON LA FORMA `cs`, nei due modi di `D2`")
    for dtau in DTAU:
        d6, s6, d7, s7 = con_cs[dtau]
        print("  dtau = %.4f   al CENTRO %6.0f ulp   a INIZIO PASSO %9.0f ulp"
              % (dtau, d6 / (EPSM * s6), d7 / (EPSM * s7)))
    print("###   e la banda e' 4096 ulp, LA STESSA del braccio (3):"
          " non ne nasce una nuova")
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E NESSUNA CONCLUSIONE DI FISICA: qui ci sono numeri. Che cosa voglia")
    print("###   dire una simmetria del passo e' una decisione di Luca.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
