# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL SOTTO-PEZZO `5c` — **la ripresa coincide AL BIT, o non e' una ripresa.**

### ⭐ **IL BRACCIO CHE CONTA:** si fa girare una corsa, si salva **a meta'**, si finisce;
poi si **riprende dal checkpoint** e si finisce **di nuovo**. ### ⛔ **I due stati finali
devono coincidere AL BIT** — non *«entro una tolleranza»*: una ripresa che perde un bit
**non e' una ripresa, e' una corsa diversa che sembra la stessa misura.**

### ⚠ **E OGNI BRACCIO CHE <<DEVE FALLIRE>> SI VERIFICA SULLA CHIAVE GIUSTA.**
"""
import io
import json
import os
import sys
import tempfile

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import checkpoint as CH                                       # noqa: E402
import incidenza as IN                                        # noqa: E402
import motore as MO                                           # noqa: E402
import stato as ST                                            # noqa: E402

OK = [0, 0]
CFG, IMP = {"prova": True}, "collaudo-5c"


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))


def _motore(nn, seme):
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=2 * nn)
    r = np.random.default_rng(seme)
    # ### ⭐ **VERSORI CASUALI E NORMALIZZATI, non `z` dovunque:** con `n = z` i versori
    # ### salvati sarebbero ### **tutti uguali**, e un salvataggio che li scambiasse
    # ### ### **passerebbe comunque.**
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    # ### e un trasporto UNITARIO ma NON banale: una fase per arco su ogni banda
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = np.exp(1j * r.normal(size=inc.m))
    U[:, 1, 1] = np.exp(1j * r.normal(size=inc.m))
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = r.normal(size=st["phi_h"].shape)
    # ### ⛔ **E IL `dtau` E- IN VALORE ASSOLUTO, dal 2026-10-15, perche- UN TEMPO
    # ### PROPRIO NON PUO- ESSERE NEGATIVO.** ### ⚠ **Prima era `r.normal(...) * 0.1`
    # ### nudo, cioe- ### GAUSSIANO: circa META- DEI NODI aveva un `dtau` NEGATIVO**,
    # ### e nessuno se ne era accorto perche- ### **nulla lo controllava.** ### Lo ha
    # ### trovato l-assert del cono *(un orologio che va indietro)*, non una lettura.
    # ### ✅ **E resta NON UNIFORME**, che e- cio- che questo collaudo vuole: il
    # ### checkpoint deve riportare ### **un `dtau` diverso per nodo.**
    mot = MO.Motore(inc, MO.Geometria(nv, U), st,
                    np.abs(r.normal(size=nn)) * 0.1, "numpy")
    return mot


def _tick(mot):
    mot.apri_tick()
    mot.operatori["grover"](mot.st, {}, 1)
    mot.operatori["moneta_spin"](mot.st, {"eps": 0.5}, 1)
    mot.operatori["spostamento_trasporto"](mot.st, {}, 1)
    mot.chiudi_tick()


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL SOTTO-PEZZO `5c`: CHECKPOINT E RIPRESA")
    print("=" * 100)
    tmp = tempfile.gettempdir()
    p = os.path.join(tmp, "_collauda_5c.npz")
    for q in (p, p + ".timbro.json", p + ".parziale"):
        if os.path.exists(q):
            os.remove(q)

    # ====================================== (1) LA RIPRESA COINCIDE AL BIT
    mot = _motore(48, 17)
    esito("il collaudo ha MATERIA: lo stato NON e' nullo e la geometria NON e' banale",
          float(np.sum(np.abs(mot.st["psi_h"]) ** 2)) > 1.0
          and float(np.std(mot.geo.n)) > 0.1,
          "### con versori tutti uguali un salvataggio che li scambiasse passerebbe")
    for _ in range(5):
        _tick(mot)
    CH.salva(p, mot, 5, CFG, IMP)
    for _ in range(7):
        _tick(mot)
    diretto = dict((k, v.copy()) for k, v in mot.st.items())
    ripreso, passo = CH.riprendi(p, CFG, IMP)
    esito("### (1) il passo salvato si riprende: %d" % passo, passo == 5,
          "### senza il passo, la corsa ripresa non sa DOVE era")
    for _ in range(7):
        _tick(ripreso)
    scarti = dict((k, float(np.max(np.abs(ripreso.st[k] - diretto[k]))))
                  for k in diretto)
    esito("### (1) i due stati finali coincidono AL BIT",
          all(v == 0.0 for v in scarti.values()),
          "### scarti: %r -- non <<entro una tolleranza>>: AL BIT"
          % {k: v for k, v in scarti.items() if v != 0.0} or "### tutti ZERO")
    esito("### e il GRAFO ripreso coincide: `(ii, jj)`, `n`, capacita'",
          np.array_equal(ripreso.inc.ii, mot.inc.ii)
          and np.array_equal(ripreso.inc.jj, mot.inc.jj)
          and ripreso.inc.n == mot.inc.n and ripreso.inc.capacita == mot.inc.capacita,
          "### senza il grafo lo stato sarebbe di un'ALTRA corsa")
    esito("### e la GEOMETRIA ripresa coincide AL BIT: versori e trasporto",
          np.array_equal(ripreso.geo.n, mot.geo.n)
          and np.array_equal(ripreso.geo.U, mot.geo.U)
          and np.array_equal(ripreso.dtau, mot.dtau),
          "### una geometria diversa sarebbe un'ALTRA fisica")
    esito("### e la SOMMATORIA si riprende: e' una scelta, non un dettaglio",
          ripreso.sommatoria == mot.sommatoria,
          "### `%s`: cambiarla cambierebbe i numeri senza che nessuno l'abbia deciso"
          % ripreso.sommatoria)

    # ====================================== (2) I CONTATORI, E QUELLO CHE NON SI RIMETTE
    print()
    r2, _ = CH.riprendi(p, CFG, IMP)
    esito("### (2) i contatori dei TICK e delle CRESCITE si riprendono",
          r2.tick == 5 and r2.cresciute == 0,
          "### tick=%d: un contatore che riparte da zero DICE UNA COSA FALSA sulla"
          " corsa che continua" % r2.tick)
    esito("### e le APPLICAZIONI di ogni operatore si riprendono",
          r2.applicazioni["grover"] == 5 and r2.applicazioni["moneta_spin"] == 5,
          "### grover=%d moneta=%d" % (r2.applicazioni["grover"],
                                       r2.applicazioni["moneta_spin"]))
    # ### ⛔ **E I RIPIEGHI DEI BUFFER **NON** SI RIMETTONO, ed e- dichiarato:** i
    # ### buffer del processo nuovo ### **non esistono ancora**, e dire il contrario
    # ### ### **nasconderebbe le allocazioni della ripresa.**
    esito("### (2) e i RIPIEGHI dei buffer NON si rimettono, perche' ricominciano",
          r2.ripieghi == 0,
          "### i buffer del processo nuovo NON esistono: dire il contrario"
          " nasconderebbe le allocazioni della ripresa")

    # ====================================== (3) IL SALVATAGGIO DURANTE LA CORSA
    print()
    pp = os.path.join(tmp, "_collauda_5c_corsa.npz")
    for q in (pp, pp + ".timbro.json"):
        if os.path.exists(q):
            os.remove(q)
    m3 = _motore(24, 3)
    sal = CH.Salvataggi(pp, 4, CFG, IMP)
    fatti = 0
    for k in range(12):
        _tick(m3)
        fatti += 1 if sal.forse(m3, k) else 0
    esito("### (3) salva ogni 4 tick su 12: %d salvataggi" % fatti,
          fatti == 3 and sal.salvati == 3,
          "### i tick 4, 8 e 12: il conto sta sui TICK DEL MOTORE, non su una"
          " variabile mia -- due contatori della stessa cosa divergono")
    # ### ⚠ **E DUE CHIAMATE NELLO STESSO TICK SALVANO UNA VOLTA SOLA:** la seconda
    # ### ### **costerebbe come la prima**, e salvare due volte lo stesso tick
    # ### ### **non aggiunge niente.**
    prima = sal.salvati
    esito("### e due `forse` nello stesso tick salvano UNA VOLTA SOLA",
          sal.forse(m3, 12) is False and sal.salvati == prima,
          "### la seconda scrittura costerebbe come la prima, e non aggiungerebbe nulla")
    esito("### e la scrittura e' ATOMICA: nessun `.parziale` resta sul disco",
          not os.path.exists(pp + ".parziale"),
          "### un riavvio a meta' non deve lasciare un file che SEMBRA un checkpoint")
    esito("### e il TIMBRO sta accanto, in un `json` leggibile",
          os.path.exists(pp + ".timbro.json")
          and "passo" in json.load(io.open(pp + ".timbro.json", encoding="utf-8")),
          "### uno stato senza timbro NON SI PUO' riprendere: non si sa che codice"
          " lo ha prodotto")

    # ====================================== (4) I CASI CHE DEVONO FALLIRE
    print()
    # ### (a) una CONFIGURAZIONE diversa: il rifiuto viene da `timbro.riprendi`, e
    # ### ### **non si duplica** -- ma ### **si PROVA**, perche- un rifiuto che nessuno
    # ### prova e- una tenda.
    try:
        CH.riprendi(p, {"prova": True}, "un-altra-impronta")
        passa, nota = False, "### NON ha alzato: una corsa diversa passerebbe"
    except AssertionError as e:
        passa = "RIFIUTA" in str(e)
        nota = "### e per la chiave giusta" if passa else "### %r" % str(e)[:50]
    esito("### DEVE fallire: riprendere con un'IMPRONTA DI CONFIGURAZIONE diversa",
          passa, nota)
    # ### (b) un file SENZA il grafo: e- lo stato nudo che `timbro.salva` scriverebbe
    ps = os.path.join(tmp, "_collauda_5c_nudo.npz")
    import timbro as TI
    TI.salva(ps, {"psi_h": np.zeros((4, 2), dtype=complex)}, 0, CFG, IMP)
    try:
        CH.riprendi(ps, CFG, IMP)
        passa, nota = False, "### NON ha alzato: la scena verrebbe INVENTATA"
    except AssertionError as e:
        passa = "INVENTARE LA SCENA" in str(e)
        nota = "### e per la chiave giusta" if passa else "### %r" % str(e)[:50]
    esito("### DEVE fallire: un checkpoint SENZA il grafo e la geometria", passa, nota)
    # ### (c) un nome di stato col PREFISSO RISERVATO
    m4 = _motore(8, 1)
    m4.st[CH.RISERVATO + "ii"] = np.zeros(3)
    try:
        CH.salva(p, m4, 0, CFG, IMP)
        passa, nota = False, "### NON ha alzato: sovrascriverebbe IN SILENZIO"
    except AssertionError as e:
        passa = "prefisso riservato" in str(e)
        nota = "### e per la chiave giusta" if passa else "### %r" % str(e)[:50]
    esito("### DEVE fallire: un nome di stato col PREFISSO RISERVATO", passa, nota)
    # ### (d) `ogni` sotto `1`
    for cattivo in (0, -3):
        try:
            CH.Salvataggi(pp, cattivo, CFG, IMP)
            passa, nota = False, "### NON ha alzato"
        except AssertionError as e:
            passa = "vale almeno 1" in str(e)
            nota = "### e per la chiave giusta" if passa else "### %r" % str(e)[:50]
        esito("### DEVE fallire: `Salvataggi` con `ogni = %d`" % cattivo, passa, nota)

    for q in (p, p + ".timbro.json", pp, pp + ".timbro.json", ps, ps + ".timbro.json"):
        if os.path.exists(q):
            os.remove(q)
    print("=" * 100)
    print("IL SOTTO-PEZZO `5c`: %d su %d   ### %s"
          % (OK[0], OK[1], "TUTTI PASSATI" if OK[0] == OK[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
