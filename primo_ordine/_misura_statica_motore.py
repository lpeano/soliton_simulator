# -*- coding: utf-8 -*-
r"""**LA RISPOSTA STATICA CON LA LEGGE NEL MOTORE** — *e il confronto con `S3`.*

> **Punto `2(c)` del mandato di Luca del `2026-10-15`** *(quinto pezzo di `L2`)*:
> *«La risposta statica (il protocollo della fotografia, `ebf5317`) rigirata con la legge
> NEL MOTORE e non per sostituzione: segno, pendenza a `x` piccolo, sovrapposizione a
> `x = 0.01`. Deve coincidere con `S3` di `ebf5317`: confronta i numeri.»*

## ⭐⭐ COME SI FA LA FOTOGRAFIA QUANDO LA LEGGE STA NEL MOTORE

### **Nel quarto pezzo la fotografia era DENTRO il termine sostituito:** `agisci.foto`
teneva una `rho` fissa. ### ⛔ **Col termine nel motore non si puo':** il motore legge
`mot.densita_materia(st)`, cioe' ### **la `psi` del momento.**
### ✅ **E la via c'e', ed e' l'ALTRA opzione che il mandato del quarto pezzo offriva:**
`congela = "pezzo"` ### **ripristina `psi` DOPO OGNI PEZZO**, quindi il termine del motore
### **vede sempre `rho(psi0)`** — che e' ### **esattamente la fotografia.**
### 📌 **E non e' un'equivalenza supposta: nel quarto pezzo il braccio `(3-ter)` ha
misurato che, con la fotografia, `psi` LIBERA da' lo stesso `Lambda(t)` AL BIT**
*(`0.000e+00`)*, perche' ### **la saturazione e' l'unico canale `materia -> vuoto`.**

## ⛔ CHE COSA SI CONFRONTA, E CON QUALI NUMERI

I numeri di riferimento sono quelli di ### **`S3` nel referto `ebf5317`**
*(`doc/referti_l2/risposta_statica_tre_intensita.txt`, blob `429c2441`)*, e stanno
### **scritti qui sotto come costanti**: ### ⚠ **ricopiati da un referto COMMITTATO**, e
il confronto dice ### **di quanto differiscono**, non se sono «uguali a occhio».

Gira con:  python primo_ordine/_misura_statica_motore.py
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import statica_protocollo as PR                               # noqa: E402

OK = [0, 0]
# ### ⛔ **LA LEGGE E' QUELLA DEL MOTORE: NIENTE SOSTITUZIONE.** ### **E' il punto `2(c)`.**
PR.SOSTITUISCI = False
# ### ⭐ **E IL CONGELAMENTO E' PER PEZZO**, che e' la fotografia quando la legge sta nel
# ### motore *(il perche' sta in testa al modulo)*.
CONGELA = "pezzo"
# ### ⛔ **I NUMERI DI `S3` DAL REFERTO `ebf5317`** *(blob `429c2441`)*: ### **ricopiati da
# ### un referto COMMITTATO**, e il confronto dice ### **di quanto si discostano.**
S3_SEGNO = {0.5: (-3.919142e+00, 1.017e-02), 0.25: (-3.947374e+00, 5.935e-03)}
S3_PENDENZA = {0.5: 1.106, 0.25: 1.110}
S3_SOVRA = {0.5: (0.0193, 0.0040), 0.25: (0.0115, 0.0009)}
# ### ⚠ **LA BANDA DEL CONFRONTO E' MIA, e la dichiaro:** `3` barre del referto sul segno
# ### *(la stessa soglia con cui il verso e' stato letto)*, `0.05` sulla pendenza e
# ### `0.01` sullo scarto della sovrapposizione. ### **Non e' una soglia di fisica: e' il
# ### margine entro cui dico <<coincide>>.**
BANDA_PENDENZA = 0.05
BANDA_SOVRA = 0.01
# ### ⛔⛔ **I CRITERI DEL `2-bis`, DAL MANDATO** *(errore `n.3`, `2026-10-16`)*:
# ### ### **le due traiettorie coincidono entro `1e-10` su `2000` tick, e le MEDIE
# ### entro `0.1` barre** -- e il caso che ### **DEVE fallire** e-
# ### ### **l-accensione diversa da UNA SOLA PARTE** *(piu- di `3` barre a
# ### `dtau = 0.25`)*.
# ### ⚠ **E `0.1` barre e- PIU' STRETTO delle `3` di prima:** non e- una banda
# ### allargata, e- ### **una banda STRINGATA dal mandato** dopo che il difetto dello
# ### strumento e- stato trovato.
TRAIETTORIE_MAX = 1e-10
BARRE_MEDIE = 0.1
BARRE_MUST_FAIL = 3.0
# ### ⚠ **I TICK DEL CONO, dichiarati:** il cono e- una proprieta- ### **per tick**, quindi
# ### ### **non serve una corsa lunga** -- serve il MASSIMO su abbastanza tick.
TICK_CONO = 300


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def profilo(dtau, x, tick, acceso, centri):
    """### I profili a blocchi di `dLambda`, ### **con la legge DEL MOTORE.**"""
    b, _dr, _dt, per = PR.base(dtau, tick)
    a, drho, dtot, _p = PR.corri(dtau, x, "MOTORE", tick, acceso, centri,
                                 congela=CONGELA)
    return PR.blocchi(a - b, PR.inizio_finestra(acceso), PR.FINESTRE), per, drho, dtot


def braccio_strumento():
    """### `(0)` **lo strumento fa cio' che dice**: niente sostituzione, `rho` ferma."""
    print("-" * 96)
    print("### (0) LO STRUMENTO: la legge e' QUELLA DEL MOTORE, e `rho` sta FERMA")
    quale = PR.pezzo_del_passo()
    esito("(0) il pezzo del passo si legge dalla TABELLA", quale == "CAMM-MATERIA-VUOTO",
          "e' `%s`: se un giorno cambia, questa misura lo dice" % quale)
    esito("(0) e NON si sostituisce niente", PR.SOSTITUISCI is False,
          "SOSTITUISCI = False: gira l'operatore del MOTORE")
    # ### ⚠ **`200` tick e NON i blocchi:** qui si guardano solo `rho` e la deriva, e
    # ### con il transitorio a `200` la finestra dei blocchi avrebbe ### **una riga.**
    _lam, drho, dtot, _per = PR.corri(0.5, PR.X_RIF, "MOTORE", 200, 0, (0,),
                                      congela=CONGELA)
    esito("(0) `rho` resta FERMA col congelamento per PEZZO", drho == 0.0,
          "max |rho(t) - rho(0)| = %.1e su 200 tick: e' la FOTOGRAFIA" % drho)
    esito("(0) e la somma di `|phi|^2` deriva poco", dtot <= 1e-9,
          "deriva %.3e su 200 tick" % dtot)
    # ### ⛔⛔ **I DUE CASI CHE DEVONO FALLIRE DELLO STRUMENTO** *(integrazione del
    # ### guardiano, `2026-10-16`)*: il primo assert che avevo scritto era
    # ### ### **UN FALSO-UNO** *(`callable(...)`, sempre vero)*, e questi due bracci sono
    # ### la prova che ### **adesso gli assert ALZANO DAVVERO.**
    # ### ① **la rampa senza la MARCA, END-TO-END:** si sostituisce `_con_rampa` con
    # ### una versione che ### **NON marca**, e si chiama `corri` con `acceso > 0`.
    # ### ⚠ **La prima stesura di questo braccio provava la CONDIZIONE a mano**, non il
    # ### cablaggio: ### **cosi- invece passa da `corri`.**
    salva = PR._con_rampa
    passa, nota = False, "NON ha alzato: l-assert e- ancora un falso-uno"
    try:
        def _senza_marca(op, ag):
            def avvolto(st_, parametri, frazione):
                return op(st_, parametri, frazione * PR.rampa(ag.passo, ag.acceso))
            return avvolto
        PR._con_rampa = _senza_marca
        PR.corri(0.5, PR.X_RIF, "MOTORE", 20, 10, (0,), congela=CONGELA)
    except AssertionError as e:                               # noqa: BLE001
        passa, nota = True, "### ha alzato: %s" % str(e)[:52]
    finally:
        PR._con_rampa = salva
    esito("### (0) DEVE fallire: il pezzo del motore SENZA la marca della rampa",
          passa, nota)
    # ### ② **i tre parametri del termine sostituito, con `SOSTITUISCI = False`.**
    passa2, nota2 = False, "NON ha alzato: sarebbero IGNORATI in silenzio"
    try:
        PR.corri(0.5, PR.X_RIF, "MOTORE", 20, 0, (0,), beta_zero=True, congela=CONGELA)
    except AssertionError as e:                               # noqa: BLE001
        passa2, nota2 = True, "### ha alzato: %s" % str(e)[:52]
    esito("### (0) DEVE fallire: `beta_zero` con `SOSTITUISCI = False`", passa2, nota2)


def braccio_segno():
    """### `(a)` **IL SEGNO**, e il confronto con `S3`."""
    print("-" * 96)
    print("### (a) IL SEGNO di dLambda sulla sorgente, contro S3 di ebf5317")
    for dtau in PR.DTAU:
        t0 = time.time()
        pr, per, _dr, _dt = profilo(dtau, PR.X_RIF, PR.TICK, PR.T_SCAN, (0,))
        dentro = [v for d, nodi in per.items() if d <= PR.RAGGIO for v in nodi]
        m, s = PR.su_nodi(pr, dentro)
        rm, rs = S3_SEGNO[dtau]
        barre = abs(m) / s if s > 0 else float("nan")
        print("  dtau=%.2f  MOTORE %+.6e +- %.3e (%.1f barre)   S3 %+.6e +- %.3e"
              "   [%.1f s]" % (dtau, m, s, barre, rm, rs, time.time() - t0))
        esito("(a) dtau=%.2f: il verso e' quello di `S3`, e a >= 3 barre" % dtau,
              m < 0 and rm < 0 and barre >= 3.0,
              "il vuoto SI RITIRA in entrambi, e il mio e' a %.1f barre" % barre)
        # ### ⛔ **E IL CONFRONTO VERO: la differenza in BARRE DEL REFERTO.**
        d = abs(m - rm) / max(rs, 1e-300)
        esito("(a) dtau=%.2f: il numero COINCIDE entro %.1f barre del referto"
              % (dtau, BARRE_MEDIE), d <= BARRE_MEDIE,
              "differenza %.3e, cioe' %.3f barre del referto -- e la banda e' quella"
              " STRETTA del mandato, non la mia di prima" % (abs(m - rm), d))


def braccio_pendenza():
    """### `(b)` **LA PENDENZA a `x` piccolo**, e il confronto con `S3`."""
    print("-" * 96)
    print("### (b) LA PENDENZA log-log in x (0.01 -> 0.03), contro S3 di ebf5317")
    for dtau in PR.DTAU:
        vals, barre = [], []
        b, _dr, _dt, per = PR.base(dtau, PR.TICK_SCAN)
        dentro = [v for d, nodi in per.items() if d <= PR.RAGGIO for v in nodi]
        for x in PR.X_SCAN[:2]:
            a, _d2, _t2, _p = PR.corri(dtau, x, "MOTORE", PR.TICK_SCAN, PR.T_SCAN, (0,),
                                       congela=CONGELA)
            prof = PR.blocchi(a - b, PR.inizio_finestra(PR.T_SCAN), PR.FINESTRE)
            m, s = PR.su_nodi(prof, dentro)
            vals.append(m)
            barre.append(s)
        pend = float(np.log(abs(vals[1]) / abs(vals[0]))
                     / np.log(PR.X_SCAN[1] / PR.X_SCAN[0]))
        rif = S3_PENDENZA[dtau]
        print("  dtau=%.2f  dLambda: %g:%+.3e  %g:%+.3e   pendenza MOTORE %.3f   S3 %.3f"
              % (dtau, PR.X_SCAN[0], vals[0], PR.X_SCAN[1], vals[1], pend, rif))
        esito("(b) dtau=%.2f: la pendenza COINCIDE con `S3` entro %.2f"
              % (dtau, BANDA_PENDENZA), abs(pend - rif) <= BANDA_PENDENZA,
              "mia %.3f contro %.3f: differenza %.4f" % (pend, rif, abs(pend - rif)))


def braccio_sovrapposizione():
    """### `(c)` **LA SOVRAPPOSIZIONE a `x = 0.01`**, e il confronto con `S3`."""
    print("-" * 96)
    nb = PR.nodo_di(PR.LATI, (PR.SEP, 0))
    print("### (c) LA SOVRAPPOSIZIONE a x = 0.01 (nodi 0 e %d), contro S3" % nb)
    for dtau in PR.DTAU:
        b, _dr, _dt, per = PR.base(dtau, PR.TICK_SCAN)
        ini = PR.inizio_finestra(PR.T_SCAN)
        pz = {}
        for nome, centri in (("A", (0,)), ("B", (nb,)), ("AB", (0, nb))):
            a, _d2, _t2, _p = PR.corri(dtau, 0.01, "MOTORE", PR.TICK_SCAN, PR.T_SCAN,
                                       centri, congela=CONGELA)
            pz[nome] = PR.blocchi(a - b, ini, PR.FINESTRE)
        somma = pz["A"] + pz["B"]
        resto = pz["AB"] - somma
        nr = np.sqrt(np.sum(resto ** 2, axis=1))
        ns = np.sqrt(np.sum(somma ** 2, axis=1))
        mr, sr = PR.barra(nr / np.where(ns > 0, ns, np.nan))
        rm, rs = S3_SOVRA[dtau]
        print("  dtau=%.2f  scarto MOTORE %.4f +- %.4f   S3 %.4f +- %.4f"
              % (dtau, mr, sr, rm, rs))
        esito("(c) dtau=%.2f: lo scarto COINCIDE con `S3` entro %.3f"
              % (dtau, BANDA_SOVRA), abs(mr - rm) <= BANDA_SOVRA,
              "mio %.4f contro %.4f: differenza %.4f" % (mr, rm, abs(mr - rm)))


def braccio_cono():
    """### `(e)` **IL CONO: il cambio di STATO per tick contro il passo LIBERO.**

    ### ⛔ **Come in `74ba200`**, dove `S3` dava ### **`0.80` del passo libero**
    *(e `S2` lo VIOLAVA con `1.89`)*. ### ⚠ **Qui la legge e' NEL MOTORE e la materia
    e' LIBERA** *(`congela = "no"`)*: il cono riguarda ### **quanto cambia lo stato**, e
    una sorgente congelata non lo metterebbe alla prova.

    ### ⭐ **E il <<passo libero>> si ottiene NEUTRALIZZANDO il termine** *(entrambe le
    fasi a `1`)*, non togliendolo dalla tabella: ### **la tabella non si tocca.**
    """
    print("-" * 96)
    print("### (e) IL CONO: max |d rho_k| per tick, col termine contro SENZA")
    import numpy as _np
    for dtau in PR.DTAU:
        PR.SOSTITUISCI = False
        con = _cambio(dtau, "MOTORE", {})
        PR.SOSTITUISCI = True
        senza = _cambio(dtau, "S3", {"senza_alpha": True, "beta_zero": True})
        PR.SOSTITUISCI = False
        print("  dtau=%.2f  col termine %.6e   senza %.6e   -> rapporto %.3f"
              % (dtau, con, senza, con / senza if senza else float("nan")))
        esito("(e) dtau=%.2f: il termine NON fa cambiare lo stato PIU' del passo"
              " libero" % dtau, con <= senza,
              "rapporto %.3f: in `74ba200` `S3` dava 0.80, e `S2` VIOLAVA con 1.89"
              % (con / senza if senza else float("nan")))


def _cambio(dtau, forma, extra):
    """### `max |rho(t+1) - rho(t)|` su `TICK_CONO` tick, ### **a materia LIBERA.**"""
    import numpy as _np
    PR.corri(dtau, PR.X_RIF, forma, TICK_CONO, 0, (0,), congela="no", **extra)
    # ### ⛔ **SI GUARDA `rho` E NON `Lambda`, e il motivo e- MISURATO:** sulla scena di
    # ### riferimento `phi` e- ### **UNIFORME**, quindi il passo LIBERO lascia `Lambda`
    # ### ### **esattamente ferma** -- e il primo tentativo di questo braccio dava
    # ### ### **`rapporto nan`**, cioe- zero al denominatore. ### ✅ **`74ba200`
    # ### guardava `max |d rho_k|`**, ed e- quello che si legge qui.
    return float(PR.ULTIMA["salto_rho"])


def braccio_traiettorie():
    """### `(d)` **LE DUE TRAIETTORIE A PARITA' DI ACCENSIONE**, tick per tick.

    ### ⛔⛔ **RIFATTO IL `2026-10-16`, E LA VERSIONE DI PRIMA ERA UN FALSO-UNO**
    *(errore `n.3` del guardiano)*: girava con ### **`acceso = 0`**, cioe'
    ### **in condizioni DIVERSE dal braccio `(a)`** *(che usa `T_SCAN = 100`)*, e il suo
    *«al primo tick coincidono a `0.000e+00`»* ### **misurava un'altra cosa.**
    ### ⛔ **E la spiegazione che ne avevo tratto** — *«amplificazione in saturazione
    profonda»* — ### **E' RITIRATA:** le `3.53` barre erano ### **la storia
    dell'accensione.**

    ### ✅ **ADESSO LA RAMPA AGISCE DA ENTRAMBE LE PARTI** *(nello STRUMENTO, mai nella
    legge)*, e il braccio misura cio' che il mandato chiede: ### **le due traiettorie
    coincidono entro `1e-10` su `2000` tick.**
    ### ⛔ **E IL CASO CHE DEVE FALLIRE E' L'ACCENSIONE DIVERSA DA UNA SOLA PARTE:**
    la' lo scarto ### **ricompare**, ed e' la prova che il braccio ### **guarda davvero
    l'accensione.**
    """
    print("-" * 96)
    print("### (d) LE DUE TRAIETTORIE A PARITA' DI ACCENSIONE, su %d tick" % PR.TICK)
    print("###     criterio DAL MANDATO: coincidono entro %.0e" % TRAIETTORIE_MAX)
    import numpy as _np
    for dtau in PR.DTAU:
        PR.SOSTITUISCI = True
        a3, _d1, _t1, _p1 = PR.corri(dtau, PR.X_RIF, "S3", PR.TICK, PR.T_SCAN, (0,),
                                     congela="tick")
        PR.SOSTITUISCI = False
        am, _d2, _t2, _p2 = PR.corri(dtau, PR.X_RIF, "MOTORE", PR.TICK, PR.T_SCAN, (0,),
                                     congela=CONGELA)
        d = _np.max(_np.abs(a3 - am), axis=1)
        peggio = float(_np.max(d))
        print("  dtau=%.2f  |dLambda| fra i due protocolli: tick 1 %.3e   tick %d %.3e"
              "   PEGGIO su tutta la corsa %.3e"
              % (dtau, d[1], PR.TICK, d[-1], peggio))
        esito("(d) dtau=%.2f: le due traiettorie coincidono entro %.0e"
              % (dtau, TRAIETTORIE_MAX), peggio <= TRAIETTORIE_MAX,
              "peggio %.3e su %d tick: a PARITA' di accensione" % (peggio, PR.TICK))
        # ### ⛔⛔ **IL CASO CHE DEVE FALLIRE: L-ACCENSIONE DIVERSA DA UNA SOLA PARTE.**
        # ### ### **E- il difetto dell-errore `n.3`, rimesso di proposito**, e senza di lui
        # ### il braccio di sopra ### **non proverebbe che l-accensione conta.**
        PR.SOSTITUISCI = False
        amz, _d3, _t3, _p3 = PR.corri(dtau, PR.X_RIF, "MOTORE", PR.TICK, 0, (0,),
                                      congela=CONGELA)
        dz = float(_np.max(_np.abs(a3 - amz)))
        barre = dz / 1.014e-02
        print("      e con l-accensione SOLO da una parte (il motore di colpo):"
              " peggio %.3e" % dz)
        esito("### (d) DEVE fallire: accensione diversa da UNA SOLA PARTE (dtau=%.2f)"
              % dtau, barre > BARRE_MUST_FAIL,
              "scarto %.3e, cioe' %.1f barre del referto: E- LA STORIA"
              " DELL-ACCENSIONE" % (dz, barre))
    PR.SOSTITUISCI = False


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    t0 = time.time()
    print("=" * 96)
    print("LA RISPOSTA STATICA CON LA LEGGE NEL MOTORE -- punto 2(c) del quinto pezzo")
    print("### La legge e' CAMM-MATERIA-VUOTO del MOTORE: NESSUNA sostituzione.")
    print("### La fotografia e' il congelamento di `psi` DOPO OGNI PEZZO.")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s = %d nodi   TICK = %d (%d nella scansione)"
          % (PR.LATI, PR.LATI[0] * PR.LATI[1], PR.TICK, PR.TICK_SCAN))
    print("  dtau = %s   T = %d   transitorio = %d   finestre = %d   x del verso = %.2f"
          % (PR.DTAU, PR.T_SCAN, PR.TRANSITORIO, PR.FINESTRE, PR.X_RIF))
    print("  raggio = %d   seme = %d   vuoto = %.1f   separazione = %d"
          % (PR.RAGGIO, PR.SEME, PR.VUOTO, PR.SEP))
    print("  ### IL RIFERIMENTO: `S3` nel referto di ebf5317 (blob 429c2441).")
    sys.stdout.flush()
    braccio_strumento()
    braccio_segno()
    braccio_pendenza()
    braccio_sovrapposizione()
    braccio_traiettorie()
    braccio_cono()
    print("=" * 96)
    print("  %d su %d   [corsa intera: %.1f s]" % (OK[0], OK[1], time.time() - t0))
    print("### ⛔ E SE UN NUMERO NON COINCIDE, la legge in tabella NON e' la legge che e'")
    print("###   stata misurata: e' il criterio del mandato, e non si aggiusta.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
