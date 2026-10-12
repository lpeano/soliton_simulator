# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL FLUSSO DI SATURAZIONE — **esatto, quindi il suo inverso lo ANNULLA.**

### ⭐ **IL BRACCIO CHE CONTA:** il flusso e' **ESATTO**, non un integratore — una rotazione
e una fase, e nient'altro. ### **Quindi `frazione = +f` seguito da `frazione = -f` deve
riportare lo stato AL BIT**, o entro pochi ulp. ### ⛔ **Un integratore NON passerebbe
questo braccio**, ed e' il modo di provare che qui non c'e' troncamento.

### ⚠ **E il secondo braccio e' quello che la decisione su `phi` ha reso possibile:** la
parte su `phi` **gli da' una FASE**, e su un reale **non esisterebbe**.
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import incidenza as IN                                        # noqa: E402
import motore as MO                                           # noqa: E402
import saturazione as SAT                                     # noqa: E402
import stato as ST                                            # noqa: E402

OK = [0, 0]
EPS = float(np.finfo(float).eps)


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))


def _banco(nn, seme):
    """### Un anello con geometria **non banale** e stato casuale.

    ### ⛔ **I versori NON sono tutti `z`:** l'elicita' e' `s . n`, e con `n` costante
    ### **una geometria scambiata darebbe lo stesso numero** — cioe' il braccio
    **non potrebbe fallire**.
    """
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=nn)
    r = np.random.default_rng(seme)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    # ### ⭐ **il vuoto con MODULO e FASE**, come il banco lo costruisce: senza la fase,
    # ### la parte su `phi` ### **non avrebbe niente da ruotare.**
    st["phi_h"][...] = np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.31), "numpy")
    return inc, st, mot


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL FLUSSO DI SATURAZIONE (`P1`) -- ESATTO, e il suo inverso lo ANNULLA")
    print("=" * 100)

    # ======================================= (0) LE FUNZIONI, PURE, SUI NUMERI
    x = np.array([-3.0, -0.5, 0.0, 0.5, 3.0])
    esito("le funzioni sono PURE e si provano sui NUMERI: `G` e' DISPARI",
          bool(np.allclose(SAT.G(-x), -SAT.G(x), atol=0)),
          "### `G(x) = x - arctan x`, e la disparita' e' esatta al bit")
    esito("### e `G'` e' PARI e LIMITATA fra `0` e `1`: e' LA SATURAZIONE",
          bool(np.allclose(SAT.Gp(-x), SAT.Gp(x), atol=0))
          and bool(np.all((SAT.Gp(x) >= 0.0) & (SAT.Gp(x) <= 1.0))),
          "### `G'(x) = x^2/(1+x^2)`: senza il limite a `1` la rotazione crescerebbe"
          " senza fine")
    esito("### e `b` e' DISPARI", bool(np.allclose(SAT.b(-x), -SAT.b(x), atol=0)),
          "### `b = dN/dLambda`, e la sua disparita' e' cio' che fa funzionare `C`")
    # ### ⛔ **IL LIMITE, e NON e- un pavimento:** dove `Lambda == 0` ESATTO le funzioni
    # ### prendono ### **il valore che hanno la-**, e si verifica ### **contro il limite
    # ### calcolato a mano**, non contro se stesse.
    h = np.array([-2.0, 2.0])
    al0, be0 = SAT.pezzi(h, np.zeros(2))
    esito("### (0) il LIMITE `Lambda -> 0`: `G' = 1` e `b = -(pi/2) sign(h)`",
          bool(np.allclose(al0, 1.0, atol=0))
          and bool(np.allclose(be0, -SAT.PIMEZZI * np.sign(h), atol=0)),
          "### e' il valore che la funzione PRENDE la', non un pavimento")
    # ### ✅ **E IL VERSO OPPOSTO: con `Lambda > 0` NON si usa il limite.**
    al1, _b1 = SAT.pezzi(h, np.array([1.0, 1.0]))
    esito("### e con `Lambda > 0` il limite NON si usa: `G'(2) = 0.8`",
          bool(np.allclose(al1, 0.8, rtol=1e-12)),
          "### %r: senza questo braccio, il limite potrebbe essere usato SEMPRE"
          % al1.tolist())

    # ======================================= (1) L'INVERSO ANNULLA, AL BIT
    print()
    inc, st, mot = _banco(24, 13)
    esito("il collaudo ha MATERIA: `psi` e `phi` non sono nulli, e `phi` HA UNA FASE",
          float(np.sum(np.abs(st["psi_h"]) ** 2)) > 1.0
          and float(np.std(np.angle(st["phi_h"]))) > 0.1,
          "### senza la fase di `phi`, la parte su `phi` non avrebbe niente da ruotare")
    prima_p = st["psi_h"].copy()
    prima_f = st["phi_h"].copy()
    mot.apri_tick()
    mot.operatori["CAMM-SATURAZIONE"](st, {}, 0.5)
    dopo_p = st["psi_h"].copy()
    esito("### (1) il flusso CAMBIA lo stato: non e' l'identita'",
          float(np.max(np.abs(dopo_p - prima_p))) > 1e-3,
          "### scarto %.3e: un flusso che non cambia niente passerebbe ogni braccio"
          % float(np.max(np.abs(dopo_p - prima_p))))
    mot.operatori["CAMM-SATURAZIONE"](st, {}, -0.5)
    mot.chiudi_tick()
    dp = float(np.max(np.abs(st["psi_h"] - prima_p)))
    df = float(np.max(np.abs(st["phi_h"] - prima_f)))
    sp = float(np.max(np.abs(prima_p)))
    esito("### (1) e l'INVERSO lo ANNULLA: `psi` torna entro pochi ulp",
          dp <= 256 * EPS * sp,
          "### scarto %.3e su scala %.3e, cioe' %.1f ulp -- un INTEGRATORE non"
          " passerebbe" % (dp, sp, dp / (EPS * sp)))
    esito("### e `phi` torna anche lui: la FASE si annulla",
          df <= 256 * EPS,
          "### scarto %.3e: e' la parte che su un `phi` REALE non esisterebbe" % df)

    # ======================================= (2) LA NORMA, E CHE COSA CONSERVA
    print()
    _i2, s2, m2 = _banco(20, 21)
    n0p = float(np.sum(np.abs(s2["psi_h"]) ** 2))
    n0f = float(np.sum(np.abs(s2["phi_h"]) ** 2))
    m2.apri_tick()
    m2.operatori["CAMM-SATURAZIONE"](s2, {}, 1)
    m2.chiudi_tick()
    n1p = float(np.sum(np.abs(s2["psi_h"]) ** 2))
    n1f = float(np.sum(np.abs(s2["phi_h"]) ** 2))
    esito("### (2) la NORMA di `psi` si conserva: e' una rotazione",
          abs(n1p - n0p) / n0p <= 4096 * EPS,
          "### scarto relativo %.3e" % (abs(n1p - n0p) / n0p))
    esito("### (2) e la NORMA di `phi` si conserva: e' una FASE, non un trasferimento",
          abs(n1f - n0f) / n0f <= 4096 * EPS,
          "### scarto relativo %.3e -- lo scambio diretto di NORMA romperebbe il gauge,"
          " ed e' GIA' misurato" % (abs(n1f - n0f) / n0f))

    # ======================================= (3) DUE META' FANNO L'INTERO
    print()
    _i3, s3, m3 = _banco(16, 7)
    pr = (s3["psi_h"].copy(), s3["phi_h"].copy())
    m3.apri_tick()
    m3.operatori["CAMM-SATURAZIONE"](s3, {}, 1)
    m3.chiudi_tick()
    intero = (s3["psi_h"].copy(), s3["phi_h"].copy())
    s3["psi_h"][...], s3["phi_h"][...] = pr
    m3.apri_tick()
    m3.operatori["CAMM-SATURAZIONE"](s3, {}, 0.5)
    m3.operatori["CAMM-SATURAZIONE"](s3, {}, 0.5)
    m3.chiudi_tick()
    # ### ⭐ **DUE META- FANNO L-INTERO AL BIT, e la MISURA mi ha corretto.**
    # ### ⚠ **Qui avevo scritto il contrario:** *<<fra le due meta- lo stato e-
    # ### cambiato, quindi `h` e `Lambda` sono ricalcolati e l-angolo della seconda meta-
    # ### non e- quello della prima>>*. ### **La misura dice `0.8` ulp**, cioe- ### **AL
    # ### BIT.**
    # ### ✅ **E IL MOTIVO E- FISICO, ed e- piu- forte del mio sospetto: il
    # ### flusso CONSERVA I PROPRI COEFFICIENTI.** La rotazione attorno a `n` conserva
    # ### ### **`s . n`** *(e- la componente lungo l-asse di rotazione)*, e la fase su
    # ### `phi` conserva ### **`|phi|^2`** -- quindi `h` e `Lambda` ### **non cambiano**,
    # ### e l-angolo della seconda meta- E- quello della prima.
    # ### ⛔ **Cioe- il flusso non e- <<esatto a stato fisso>>: e- ESATTO**, e
    # ### questo e- il braccio che lo prova.
    d = float(np.max(np.abs(s3["psi_h"] - intero[0])))
    sc = float(np.max(np.abs(intero[0])))
    esito("### (3) DUE META- FANNO L-INTERO al bit: il flusso e- ESATTO",
          d <= 256 * EPS * sc,
          "### scarto %.3e su scala %.3e, cioe- %.1f ulp -- e qui avevo previsto il"
          " CONTRARIO" % (d, sc, d / (EPS * sc)))
    # ### ⭐ **E LA CAUSA SI PROVA DIRETTAMENTE**, invece di dedurla: `h` e
    # ### `Lambda` ### **non cambiano** sotto il flusso. ### **Un braccio sull-effetto
    # ### dice CHE funziona; questo dice PERCHE-.**
    _i3b, s3b, m3b = _banco(20, 99)
    h0 = m3b.elicita(s3b).copy()
    l0 = m3b.densita_vuoto(s3b).copy()
    m3b.apri_tick()
    m3b.operatori["CAMM-SATURAZIONE"](s3b, {}, 1)
    m3b.chiudi_tick()
    dh = float(np.max(np.abs(m3b.elicita(s3b) - h0)))
    dl = float(np.max(np.abs(m3b.densita_vuoto(s3b) - l0)))
    sh = float(np.max(np.abs(h0)))
    esito("### (3) e la CAUSA: il flusso CONSERVA `h` e `Lambda`, i suoi coefficienti",
          dh <= 256 * EPS * sh and dl <= 256 * EPS * float(np.max(np.abs(l0))),
          "### |dh| %.3e (%.1f ulp), |dLambda| %.3e: la rotazione attorno a `n` conserva"
          " `s.n`, e la fase conserva `|phi|^2`" % (dh, dh / (EPS * sh), dl))

    # ======================================= (4) I DUE OSSERVATORI
    print()
    _i4, s4, m4 = _banco(12, 3)
    h = m4.elicita(s4)
    lam = m4.densita_vuoto(s4)
    esito("### (4) `h_int` e `Lambda` sono scritti NELLO STATO, non tornati a parte",
          h is s4["h_int"] and lam is s4["Lambda"],
          "### sono VARIABILI della tabella: se il motore ne tenesse una copia, le due"
          " divergerebbero")
    esito("### e `Lambda` e' la somma di `|phi|^2` per nodo, verificata a mano",
          bool(np.allclose(float(lam.sum()),
                           float(np.sum(np.abs(s4["phi_h"]) ** 2)), rtol=1e-12)),
          "### la somma sui nodi fa la norma intera: %.6f" % float(lam.sum()))
    esito("### e `h_int` e' la somma dell'elicita' per nodo, e NON e' nulla",
          float(np.max(np.abs(h))) > 1e-3,
          "### max |h| = %.4f: con `h = 0` la saturazione sarebbe spenta e ogni"
          " braccio passerebbe" % float(np.max(np.abs(h))))

    # ======================================= (5) IL CASO CHE DEVE FALLIRE
    print()
    # ### ⚠ **QUI AVEVO SCRITTO UN BRACCIO SBAGLIATO, e il collaudo me l-ha
    # ### detto:** pretendevo che il flusso ### **alzasse fuori da un tick.** ### **Non
    # ### alza, e NON DEVE:** il tick e- il contatore delle ### **CRESCITE**, e nessuno
    # ### dei sei pezzi lo chiede -- solo `cresci()`. ### ⛔ **Un braccio che
    # ### pretende una cosa che il codice non promette non prova niente: prova solo che
    # ### io non avevo letto.**
    # ### ✅ **AL SUO POSTO il caso che DEVE davvero fallire: un `dtau` della
    # ### taglia sbagliata**, che e- l-errore che ### **si propagherebbe in silenzio.**
    _i5, s5, m5 = _banco(8, 1)
    try:
        MO.Motore(_i5, m5.geo, s5, np.zeros(3), "numpy")
        passa, nota = False, "### NON ha alzato"
    except AssertionError as e:
        passa = "PER NODO" in str(e)
        nota = "### e per la chiave giusta" if passa else "### %r" % str(e)[:50]
    esito("### DEVE fallire: un `dtau` che non ha una riga per NODO", passa, nota)
    # ### ⛔ **E il flusso con una `frazione` di `0`: NON alza, ed e- GIUSTO** --
    # ### ### **mezzo flusso e- un flusso**, e zero e- l-identita-. ### **Il braccio sta
    # ### qui perche- i cinque pezzi unitari INVECE alzano**, e la differenza
    # ### ### **non e- un caso: e- la differenza fra un flusso e un-involuzione.**
    _i6, s6, m6 = _banco(8, 2)
    pr6 = s6["psi_h"].copy()
    m6.operatori["CAMM-SATURAZIONE"](s6, {}, 0)
    esito("### e con `frazione = 0` il flusso NON alza, ed e' l'IDENTITA'",
          float(np.max(np.abs(s6["psi_h"] - pr6))) == 0.0,
          "### i cinque pezzi unitari INVECE alzano: e' la differenza fra un flusso e"
          " un'involuzione")

    print("=" * 100)
    print("IL FLUSSO DI SATURAZIONE: %d su %d   ### %s"
          % (OK[0], OK[1], "TUTTI PASSATI" if OK[0] == OK[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
